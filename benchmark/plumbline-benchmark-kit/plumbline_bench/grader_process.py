"""Trusted grader entrypoint. Launched outside the candidate with a sanitized environment."""
from __future__ import annotations
import argparse
import importlib.util
import json
import sys
import time
import unittest
from pathlib import Path

class Capture(unittest.TestResult):
    def __init__(self):
        super().__init__(); self.checks=[]
    def addSuccess(self,test):
        super().addSuccess(test); self.checks.append({'id':test.id(),'status':'pass'})
    def addFailure(self,test,err):
        super().addFailure(test,err); self.checks.append({'id':test.id(),'status':'fail','detail':self._exc_info_to_string(err,test)})
    def addError(self,test,err):
        super().addError(test,err); self.checks.append({'id':test.id(),'status':'error','detail':self._exc_info_to_string(err,test)})
    def addSkip(self,test,reason):
        super().addSkip(test,reason); self.checks.append({'id':test.id(),'status':'skip','detail':reason})
    def addSubTest(self,test,subtest,err):
        super().addSubTest(test,subtest,err)
        if err:
            self.checks.append({'id':subtest.id(),'status':'fail','detail':self._exc_info_to_string(err,test)})

def load_file(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return unittest.defaultTestLoader.loadTestsFromModule(module)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--candidate',required=True); p.add_argument('--task',required=True)
    p.add_argument('--output',required=True); a=p.parse_args()
    root=Path(__file__).resolve().parents[1]; candidate=Path(a.candidate).resolve()
    sys.path.insert(0,str(candidate))
    result={}; started=time.monotonic()
    for label,path in [('regression',root/'fixtures'/a.task/'tests/test_existing.py'),
                       ('acceptance',root/'graders'/f'{a.task}.py')]:
        try:
            suite=load_file(path,'benchmark_'+label); capture=Capture(); suite.run(capture)
            result[label]={'passed':capture.wasSuccessful() and not capture.skipped,
                           'tests':capture.testsRun,'checks':capture.checks}
        except Exception as exc:
            result[label]={'passed':False,'tests':0,'checks':[],
                           'load_error':f'{type(exc).__name__}: {exc}'}
    result['passed']=all(x['passed'] for x in result.values())
    result['seconds']=time.monotonic()-started
    Path(a.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0

if __name__=='__main__': raise SystemExit(main())
