import json
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from jobs import Store, StateError

class Acceptance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = str(Path(self.tmp.name)/'jobs.db')
        self.s = Store(self.path); self.addCleanup(self.s.close)
        self.s.submit('j')
    def failed(self, name='j'):
        self.s.start(name); self.s.fail(name)
    def test_J01_queued_cancel_idempotent(self):
        for _ in range(3): self.assertEqual(self.s.cancel('j')['state'],'cancelled')
        self.assertEqual(self.s.history('j'),[{'number':1,'state':'cancelled'}])
    def test_J02_running_ack(self):
        self.s.start('j')
        for _ in range(2): self.assertEqual(self.s.cancel('j')['state'],'cancelling')
        for _ in range(2): self.assertEqual(self.s.ack_cancel('j')['state'],'cancelled')
        self.assertEqual(self.s.history('j')[-1]['state'],'cancelled')
    def test_J03_cancel_precedence(self):
        self.s.start('j'); self.s.cancel('j')
        for op in (self.s.complete,self.s.fail,self.s.start):
            with self.assertRaises(StateError): op('j')
        self.assertEqual(self.s.get('j')['state'],'cancelling')
    def test_J03_terminal_transitions(self):
        self.s.start('j'); self.s.complete('j')
        for op in (self.s.cancel,self.s.ack_cancel,self.s.start):
            with self.assertRaises(StateError): op('j')
        with self.assertRaises(KeyError): self.s.cancel('missing')
    def test_J04_retry_history(self):
        self.failed(); self.s.retry('j','one'); self.failed(); self.s.retry('j','two')
        self.assertEqual(self.s.get('j'),{'id':'j','state':'queued','attempt':3})
        self.assertEqual(self.s.history('j'),[{'number':1,'state':'failed'},
                         {'number':2,'state':'failed'},{'number':3,'state':'queued'}])
    def test_J05_replay_after_later_failure(self):
        self.failed(); self.s.retry('j','one'); self.failed()
        self.assertEqual(self.s.retry('j','one')['state'],'failed')
        self.assertEqual(len(self.s.history('j')),2)
        self.s.retry('j','two')
        self.assertEqual(self.s.retry('j','one')['attempt'],3)
    def test_J05_invalid_key_not_consumed_and_scoped(self):
        for value in ('',None,4):
            with self.assertRaises(ValueError): self.s.retry('j',value)
        with self.assertRaises(StateError): self.s.retry('j','r')
        self.failed(); self.assertEqual(self.s.retry('j','r')['attempt'],2)
        self.s.submit('k'); self.failed('k')
        self.assertEqual(self.s.retry('k','r')['attempt'],2)
    def test_J06_transaction_failure(self):
        self.failed()
        writes = [0]
        def deny_second_write(action, *args):
            if action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE):
                writes[0] += 1
                if writes[0] == 2: return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        self.s.db.set_authorizer(deny_second_write)
        with self.assertRaises(sqlite3.Error): self.s.retry('j','key')
        self.s.db.set_authorizer(None)
        self.assertEqual(self.s.get('j')['state'],'failed')
        self.assertEqual(len(self.s.history('j')),1)
        self.assertEqual(self.s.retry('j','key')['attempt'],2)
    def test_J06_cancel_failure(self):
        writes = [0]
        def deny_second_update(action, *args):
            if action == sqlite3.SQLITE_UPDATE:
                writes[0] += 1
                if writes[0] == 2: return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        self.s.db.set_authorizer(deny_second_update)
        with self.assertRaises(sqlite3.Error): self.s.cancel('j')
        self.s.db.set_authorizer(None)
        self.assertEqual(self.s.get('j')['state'],'queued')
    def test_J07_concurrent_duplicate(self):
        self.failed(); barrier=threading.Barrier(2)
        def work():
            s=Store(self.path)
            try:
                barrier.wait(timeout=5)
                return s.retry('j','same')['attempt']
            finally: s.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(work); b=pool.submit(work)
            self.assertEqual([a.result(timeout=8),b.result(timeout=8)],[2,2])
        self.assertEqual(len(self.s.history('j')),2)
    def test_J08_persistence(self):
        self.failed(); self.s.retry('j','one'); self.s.start('j')
        other=Store(self.path)
        try:
            self.assertEqual(other.retry('j','one')['state'],'running')
            self.assertEqual(len(other.history('j')),2)
        finally: other.close()
    def test_J08_legacy_schema(self):
        path=str(Path(self.tmp.name)/'old.db')
        db=sqlite3.connect(path)
        db.executescript("""CREATE TABLE jobs(id TEXT PRIMARY KEY,state TEXT NOT NULL,attempt INTEGER NOT NULL);
        CREATE TABLE attempts(job_id TEXT NOT NULL,number INTEGER NOT NULL,state TEXT NOT NULL,PRIMARY KEY(job_id,number));
        INSERT INTO jobs VALUES('old','failed',1); INSERT INTO attempts VALUES('old',1,'failed');""")
        db.close(); s=Store(path)
        try: self.assertEqual(s.retry('old','r')['attempt'],2)
        finally: s.close()
    def test_J10_cli(self):
        import jobs
        cli=Path(jobs.__file__).parent/'cli.py'
        def run(action,*args):
            p=subprocess.run([sys.executable,str(cli),self.path,action,'j',*args],
                             capture_output=True,text=True,timeout=8)
            self.assertEqual(p.returncode,0,p.stderr); return json.loads(p.stdout)
        self.assertEqual(run('cancel')['state'],'cancelled')
        self.assertEqual(run('ack-cancel')['state'],'cancelled')
        # A separate failed job exercises retry option parsing.
        self.s.submit('x'); self.failed('x')
        p=subprocess.run([sys.executable,str(cli),self.path,'retry','x','--request-id','r'],
                         capture_output=True,text=True,timeout=8)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)['attempt'],2)
