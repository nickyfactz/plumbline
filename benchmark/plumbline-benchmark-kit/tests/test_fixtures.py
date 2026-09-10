from __future__ import annotations
import shutil
import tempfile
import unittest
from pathlib import Path
from plumbline_bench.util import ROOT,grade

class Fixtures(unittest.TestCase):
    def staged(self,task,reference):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        candidate=Path(temp.name)/'candidate';shutil.copytree(ROOT/'fixtures'/task,candidate)
        if reference:shutil.copytree(ROOT/'reference'/task,candidate,dirs_exist_ok=True)
        return candidate,Path(temp.name)/'grade.json'
    def test_all_baselines_keep_existing_behavior_but_fail_feature(self):
        for task in ('jobqueue','configscope','docaccess'):
            with self.subTest(task=task):
                c,o=self.staged(task,False);g=grade(c,task,o)
                self.assertTrue(g['regression']['passed']);self.assertFalse(g['passed'])
    def test_all_reference_implementations_pass(self):
        for task in ('jobqueue','configscope','docaccess'):
            with self.subTest(task=task):
                c,o=self.staged(task,True);self.assertTrue(grade(c,task,o)['passed'])
    def test_six_known_wrong_mutants_are_detected(self):
        mutants=[
            ('jobqueue','jobs.py',"{'running'}, 'complete'","{'running', 'cancelling'}, 'complete'"),
            ('jobqueue','jobs.py','if self.db.execute("SELECT 1 FROM retry_keys', 'if False and self.db.execute("SELECT 1 FROM retry_keys'),
            ('configscope','config.py','values.update(layer)','values.update({k:v for k,v in layer.items() if v is not None})'),
            ('configscope','config.py','for _, values in _layers(document):','for _, values in _layers(document)[-1:]:'),
            ('docaccess','documents.py',"role = self.memberships.get((ctx.user, ctx.workspace))", "role = self.memberships.get((ctx.user, ctx.workspace))\n        if operation == 'update': operation = 'read'"),
            ('docaccess','documents.py','            self._document(ctx, doc_id)\n','')]
        for task,file,old,new in mutants:
            with self.subTest(task=task,mutation=old):
                c,o=self.staged(task,True);p=c/file;src=p.read_text();self.assertIn(old,src)
                p.write_text(src.replace(old,new,1));self.assertFalse(grade(c,task,o)['passed'])
