from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from plumbline_bench.telemetry import collect,thread_log
from plumbline_bench.util import ROOT,read_json

P=read_json(ROOT/'pricing/2026-09-05-standard.json')

def write(path,values):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(x)+'\n' for x in values))

def events(ident,model,counts,parent=None):
    data=[{'type':'session_meta','payload':{'id':ident,'source':{'parent_thread_id':parent}}},
          {'type':'turn_context','payload':{'model':model,'effort':'medium'}}]
    for i,c,o,r in counts:
        data.append({'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':
                    {'input_tokens':i,'cached_input_tokens':c,'output_tokens':o,'reasoning_output_tokens':r}}}})
    data.append({'type':'event_msg','payload':{'type':'task_complete'}})
    return data

class Telemetry(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.home=Path(self.tmp.name)
    def test_cumulative_dedup_and_reasoning_subset(self):
        path=self.home/'one.jsonl';write(path,events('r','gpt-5.6-sol',[(1000,500,100,80),(1000,500,100,80),(1500,500,150,100)]))
        r=thread_log(path,P)
        self.assertEqual(r['tokens']['input_tokens'],1500)
        self.assertAlmostEqual(r['cost_estimate_usd'],(1000*4+500*.4+150*20)/1e6)
    def test_mixed_root_worker_prices(self):
        write(self.home/'sessions/r.jsonl',events('r','gpt-5.6-sol',[(1000,0,100,80)]))
        write(self.home/'sessions/w.jsonl',events('w','gpt-5.6-luna',[(1000,0,100,80)],parent='r'))
        e=self.home/'events.jsonl';write(e,[{'type':'thread.started','thread_id':'r'},
                                        {'type':'item.completed','item':{'type':'collab_agent_tool_call','receiver_thread_ids':['w']}},
                                        {'type':'turn.completed','usage':{}}])
        u=collect(self.home,e,P,finished=True)
        self.assertEqual(u['coverage'],'complete-observed');self.assertEqual(u['worker_count'],1)
        self.assertAlmostEqual(u['cost_estimate_usd'],.006+.00032)
    def test_reserve_uses_luna_pricing_alias(self):
        path=self.home/'reserve.jsonl';write(path,events('r','gpt-reserve',[(1000,500,100,20)]))
        result=thread_log(path,P)
        self.assertAlmostEqual(result['cost_estimate_usd'],.00023)
        self.assertEqual(result['requests'][0]['pricing_model'],'gpt-5.6-luna')
    def test_root_only_stdout_suppresses_price(self):
        e=self.home/'events.jsonl';write(e,[{'type':'thread.started','thread_id':'r'},
             {'type':'turn.completed','usage':{'input_tokens':900,'output_tokens':20}}])
        self.assertIsNone(collect(self.home,e,P)['cost_estimate_usd'])
    def test_missing_child_suppresses_price(self):
        write(self.home/'sessions/r.jsonl',events('r','gpt-5.6-sol',[(100,0,10,0)]))
        e=self.home/'events.jsonl';write(e,[{'type':'thread.started','thread_id':'r'},
             {'type':'item.completed','item':{'receiver_thread_ids':['missing']}}])
        self.assertIsNone(collect(self.home,e,P)['cost_estimate_usd'])
    def test_archived_copy_not_double_counted(self):
        value=events('r','gpt-5.6-luna',[(100,0,10,0)])
        write(self.home/'sessions/r.jsonl',value);write(self.home/'archived_sessions/r.jsonl',value)
        e=self.home/'events.jsonl';write(e,[{'type':'thread.started','thread_id':'r'}])
        self.assertEqual(collect(self.home,e,P)['tokens']['input_tokens'],100)
    def test_unknown_model_and_reset_not_silently_priced(self):
        p=self.home/'r.jsonl';write(p,events('r','unknown',[(100,0,10,0),(50,0,5,0)]))
        result=thread_log(p,P);self.assertTrue(result['warnings'])
    def test_long_context_is_per_request_not_session_total(self):
        data=events('r','gpt-6-astra',[(200000,0,100,0),(400000,0,200,0)])
        p=self.home/'r.jsonl';write(p,data)
        self.assertAlmostEqual(thread_log(p,P)['cost_estimate_usd'],4.01)
        data=events('r','gpt-6-astra',[(300000,0,100,0)])
        data[2]['payload']['info']['last_token_usage']={'input_tokens':300000}
        write(p,data)
        self.assertAlmostEqual(thread_log(p,P)['cost_estimate_usd'],6.0075)
