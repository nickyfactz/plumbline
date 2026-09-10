import copy
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import config

class Acceptance(unittest.TestCase):
    def test_C01_legacy_and_mixed(self):
        self.assertEqual(config.resolve({'timeout':8})['timeout'],8)
        for doc in ({'global':{},'timeout':4},{'global':{},'other':{}},[]):
            with self.assertRaises(ValueError): config.resolve(doc)
    def test_C02_precedence(self):
        self.assertEqual(config.resolve({'global':{'timeout':9},'workspace':{'timeout':4},
                                        'project':{'theme':'dark'}}),
                         {'timeout':4,'theme':'dark','retries':2})
    def test_C02_null_and_zero(self):
        self.assertEqual(config.resolve({'global':{'timeout':4},'project':{'timeout':None}})['timeout'],None)
        self.assertEqual(config.resolve({'project':{'timeout':0}})['timeout'],0)
    def test_C03_origin(self):
        self.assertEqual(config.resolve({'global':{'timeout':8},'project':{'theme':None}},with_origin=True),
            {'values':{'timeout':8,'theme':None,'retries':2},
             'origins':{'timeout':'global','theme':'project','retries':'default'}})
        self.assertEqual(config.resolve({'theme':'dark'},with_origin=True)['origins']['theme'],'global')
    def test_C04_validate_shadowed(self):
        for value in (True,-1,'4',2.3):
            with self.assertRaises(ValueError):
                config.resolve({'global':{'timeout':value},'project':{'timeout':5}})
        for doc in ({'workspace':None},{'project':[]},{'global':{'bad':None}},
                    {'global':{'theme':'weird'},'project':{'theme':'light'}}):
            with self.assertRaises(ValueError): config.validate(doc)
    def test_C05_empty_and_null(self):
        for doc in ({},{'global':{},'workspace':{}},{'retries':None}):
            self.assertIsNone(config.validate(doc))
            config.resolve(doc)
    def test_C06_no_mutation(self):
        doc={'global':{'timeout':4},'project':{'theme':'dark'}}; saved=copy.deepcopy(doc)
        defaults=copy.deepcopy(config.DEFAULTS)
        a=config.resolve(doc,with_origin=True); a['values']['timeout']=100; a['origins']['theme']='bad'
        self.assertEqual(doc,saved); self.assertEqual(config.DEFAULTS,defaults)
        self.assertEqual(config.resolve(doc,with_origin=True)['origins']['theme'],'project')
        self.assertEqual(config.resolve({})['timeout'],30)
    def test_C07_roundtrip_structure(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config.json'; doc={'global':{'timeout':9},'project':{'timeout':None}}
            config.dump(doc,p); self.assertEqual(json.loads(p.read_text()),doc)
            self.assertEqual(config.load(p)['timeout'],None)
            self.assertEqual(config.load(p,with_origin=True)['origins']['timeout'],'project')
    def test_C07_invalid_does_not_clobber(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.json'; p.write_text('KEEP')
            with self.assertRaises(ValueError): config.dump({'global':{'bad':1}},p)
            self.assertEqual(p.read_text(),'KEEP')
    def test_C08_io_errors(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.json'
            with self.assertRaises(FileNotFoundError): config.load(p)
            p.write_text('{')
            with self.assertRaises(ValueError): config.load(p)
    def test_C09_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.json'; p.write_text('{"workspace":{"timeout":null}}')
            cli=Path(config.__file__).parent/'cli.py'
            for args in ([str(p),'--show-origin'],['--show-origin',str(p)]):
                result=subprocess.run([sys.executable,str(cli),*args],capture_output=True,text=True,timeout=5)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads(result.stdout)['origins']['timeout'],'workspace')
            result=subprocess.run([sys.executable,str(cli),str(p)],capture_output=True,text=True,timeout=5)
            self.assertEqual(json.loads(result.stdout)['timeout'],None)
    def test_C02_C03_exhaustive_small_cross_product(self):
        missing=object()
        for combo in itertools.product((missing,None,0,11), repeat=3):
            doc={}; expected=30; origin='default'
            for scope,val in zip(('global','workspace','project'),combo):
                doc[scope]={} if val is missing else {'timeout':val}
                if val is not missing: expected=val; origin=scope
            got=config.resolve(doc,with_origin=True)
            self.assertEqual((got['values']['timeout'],got['origins']['timeout']),(expected,origin))
