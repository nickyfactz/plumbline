from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from plumbline_bench.report import build_report
from plumbline_bench.util import write_json

class Reports(unittest.TestCase):
    def make(self, folder, costs, states):
        matrix=[]
        for index,(cost,status) in enumerate(zip(costs,states)):
            cell={'id':str(index),'task':'configscope','model_label':'terra','arm':'plumbline','repeat':index+1}
            matrix.append(cell)
            write_json(folder/'runs'/str(index)/'result.json',{**cell,'status':status,'wall_seconds':3,'usage':{'cost_estimate_usd':cost}})
        write_json(folder/'campaign.json',{'id':'offline-test','matrix':matrix,'config':{'disclosures':{'simulated':True}}})
    def test_failed_attempt_spend_is_not_dropped(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);self.make(folder,[2,3],['FAIL','PASS'])
            self.assertEqual(build_report(folder)['summary'][0]['observed_cost_per_pass'],5)
    def test_missing_cost_suppresses_group_price(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);self.make(folder,[None,3],['FAIL','PASS'])
            self.assertIsNone(build_report(folder)['summary'][0]['observed_cost_per_pass'])
    def test_no_pass_means_undefined_not_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);self.make(folder,[2],['FAIL'])
            self.assertIsNone(build_report(folder)['summary'][0]['observed_cost_per_pass'])
    def test_partial_account_coverage_has_no_cost_per_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);self.make(folder,[2,3],['FAIL','PASS'])
            write_json(folder/'account-charges.json',[{'run_id':'1','amount':3,'unit':'credits','evidence':'example-only'}])
            value=build_report(folder)['imported_account_cost'][0]
            self.assertFalse(value['complete']);self.assertIsNone(value['actual_amount_per_pass'])

    def test_behavioral_grade_does_not_promote_stopped_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);runs=folder/'runs';runs.mkdir()
            matrix=[]
            for index,(arm,status,cost) in enumerate((('vanilla','PASS',2),('plumbline','BUDGET_EXHAUSTED',3))):
                cell={'id':str(index),'task':'configscope','model_label':'terra','arm':arm,'repeat':1};matrix.append(cell)
                write_json(runs/str(index)/'result.json',{**cell,'status':status,'external_grade_passed':True,
                    'acceptance_passed_checks':12,'acceptance_tests':12,'usage':{'cost_estimate_usd':cost,
                    'tokens':{'input_tokens':100,'output_tokens':10}}})
            write_json(folder/'campaign.json',{'id':'offline-pair','matrix':matrix,'config':{'disclosures':{}}})
            pair=build_report(folder)['paired_results'][0]
            self.assertTrue(pair['vanilla_execution_complete'])
            self.assertFalse(pair['plumbline_execution_complete'])
            self.assertEqual(pair['plumbline_total_tokens'],110)
            self.assertEqual(pair['cost_delta_usd'],1)
