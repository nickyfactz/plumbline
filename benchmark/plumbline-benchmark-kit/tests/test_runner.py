from __future__ import annotations
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from plumbline_bench.runner import agent_team_flags,app_server_command,app_server_thread_params,append_config,config_load,final_claim,prepare,run_campaign,validate_ponytail_seed
from plumbline_bench.util import ROOT,git,init_git,read_json,write_json

class Runner(unittest.TestCase):
    def test_config_and_default_baseline(self):
        c=config_load(ROOT/'config.example.json')
        self.assertEqual(c['root_effort'],'medium'); self.assertEqual(c['baseline_mode'],'stock')
        args=app_server_command(c,{'arm':'vanilla','model_label':'sol'})
        self.assertIn('app-server',args);self.assertIn('--stdio',args)
        self.assertNotIn('agents.enabled=false',args)
        c['baseline_mode']='single';args=app_server_command(c,{'arm':'vanilla','model_label':'sol'})
        self.assertIn('agents.enabled=false',args)

    def test_aggregate_token_limit_can_be_disabled(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'config.json';config=read_json(ROOT/'config.example.json')
            config['limits']['aggregate_tokens_per_run']=None;write_json(path,config)
            self.assertIsNone(config_load(path)['limits']['aggregate_tokens_per_run'])
    def test_uniform_role_profile_flags(self):
        c=config_load(ROOT/'config.example.json')
        c.update(root_effort='high',uniform_role_profiles=True)
        self.assertEqual(agent_team_flags(c,{'model_label':'luna'}),[
            '--update-agents','--model','gpt-5.6-luna','--reasoning-effort','high'])
    def test_completion_claim_requires_exact_marker(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'message';p.write_text('looks done')
            self.assertIsNone(final_claim(p))
            p.write_text('BENCHMARK_STATUS: COMPLETE');self.assertTrue(final_claim(p))
            p.write_text('BENCHMARK_STATUS: INCOMPLETE');self.assertFalse(final_claim(p))
    def test_append_config_and_no_schema_guessing(self):
        with tempfile.TemporaryDirectory() as d:
            append_config(Path(d),'[projects."/test"]\ntrust_level="trusted"')
            import tomllib
            self.assertEqual(tomllib.loads((Path(d)/'config.toml').read_text())['projects']['/test']['trust_level'],'trusted')
    def test_fake_transport_full_pipeline_and_resume(self):
        # Deliberately simulated transport: this tests mechanics, never model capability.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); plugin=root/'plugin';(plugin/'scripts').mkdir(parents=True)
            (plugin/'skills/plumbline-execute').mkdir(parents=True)
            (plugin/'skills/plumbline-execute/SKILL.md').write_text('test fixture, not the real plugin')
            (plugin/'scripts/install_router.py').write_text('import argparse\np=argparse.ArgumentParser();p.add_argument("--root");p.parse_args()\n')
            (plugin/'scripts/install_agent_team.py').write_text('import argparse\np=argparse.ArgumentParser();p.add_argument("--root");p.add_argument("--update-agents",action="store_true");a=p.parse_args()\nfrom pathlib import Path\nf=Path(a.root)/"AGENTS.md";f.write_text(f.read_text()+"\\nTest setup\\n")\n')
            init_git(plugin);commit=git(plugin,'rev-parse','HEAD').stdout.strip()
            auth=root/'auth';auth.mkdir();(auth/'auth.json').write_text('{"test":"not-a-real-credential"}')
            fake=root/'fake_codex.py'
            fake.write_text("""import json,os,sys
from pathlib import Path
if '--version' in sys.argv: print('mock-codex-1');raise SystemExit
if '--help' in sys.argv: print('--stdio');raise SystemExit
if 'plugin' in sys.argv: print('mock plugin installation');raise SystemExit
home=Path(os.environ['CODEX_HOME']);(home/'sessions').mkdir()
def send(value): print(json.dumps(value),flush=True)
for line in sys.stdin:
    request=json.loads(line);method=request.get('method')
    if method=='initialize':
        send({'jsonrpc':'2.0','id':request['id'],'result':{'userAgent':'mock','codexHome':str(home)}})
    elif method=='thread/start':
        model=request['params']['model']
        rows=[{'type':'session_meta','payload':{'id':'root'}},{'type':'turn_context','payload':{'model':model,'effort':'medium'}},{'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':1000,'cached_input_tokens':500,'output_tokens':100,'reasoning_output_tokens':20}}}},{'type':'event_msg','payload':{'type':'task_complete'}}]
        (home/'sessions/r.jsonl').write_text(''.join(json.dumps(x)+'\\n' for x in rows))
        thread={'id':'root','model':model,'reasoningEffort':None,'parentThreadId':None,'agentRole':None}
        send({'jsonrpc':'2.0','id':request['id'],'result':{'thread':thread,'model':model}})
        send({'jsonrpc':'2.0','method':'thread/started','params':{'thread':thread}})
    elif method=='turn/start':
        send({'jsonrpc':'2.0','id':request['id'],'result':{'turn':{'id':'turn','status':'inProgress'}}})
        send({'jsonrpc':'2.0','method':'thread/tokenUsage/updated','params':{'threadId':'root','turnId':'turn','tokenUsage':{'total':{'inputTokens':1000,'cachedInputTokens':500,'outputTokens':100,'reasoningOutputTokens':20},'last':{'inputTokens':1000,'cachedInputTokens':500,'outputTokens':100,'reasoningOutputTokens':20}}}})
        send({'jsonrpc':'2.0','method':'item/completed','params':{'threadId':'root','turnId':'turn','item':{'type':'agentMessage','id':'message','text':'BENCHMARK_STATUS: INCOMPLETE'}}})
        send({'jsonrpc':'2.0','method':'turn/completed','params':{'threadId':'root','turn':{'id':'turn','status':'completed'}}})
""")
            cfg=config_load(ROOT/'config.example.json');cfg.update(state_root=str(root/'state'),codex_command=[sys.executable,str(fake)],
                  plumbline_source=str(plugin),plumbline_ref=commit,auth_source_home=str(auth),ponytail_mode='off')
            campaign=prepare(cfg,'pilot')
            result=run_campaign(campaign)
            self.assertEqual(result['completed_runs'],2)
            outputs=[read_json(p) for p in (campaign/'runs').glob('*/result.json')]
            self.assertEqual([x['status'] for x in outputs],['FAIL','FAIL'])
            self.assertTrue(all(x['usage']['cost_estimate_usd'] is not None for x in outputs))
            self.assertTrue(all(not (p/'codex-home/auth.json').exists() for p in (campaign/'runs').iterdir()))
            self.assertTrue(all('sandbox = "elevated"' in (p/'codex-home/config.toml').read_text() for p in (campaign/'runs').iterdir()))
            for run in (campaign/'runs').iterdir():
                session=read_json(run/'app-server-session.json')
                self.assertEqual([x['method'] for x in session['requests']],['initialize','initialized','thread/start','turn/start'])
                thread=next(x for x in session['requests'] if x['method']=='thread/start')
                turn=next(x for x in session['requests'] if x['method']=='turn/start')
                self.assertEqual(Path(thread['params']['cwd']),run/'project')
                self.assertEqual(Path(turn['params']['cwd']),run/'project')
            self.assertEqual(run_campaign(campaign)['completed_runs'],2)
            self.assertTrue((campaign/'report.html').is_file())

    def test_scoped_git_permissions_do_not_use_legacy_sandbox(self):
        cfg=config_load(ROOT/'config.example.json')
        params=app_server_thread_params(cfg,{'arm':'vanilla','model_label':'terra'},Path('/tmp/project'))
        self.assertEqual(params['permissions'],'benchmark-local')
        self.assertNotIn('sandbox',params)
        self.assertNotIn('--dangerously-bypass-hook-trust',app_server_command(cfg,{'arm':'vanilla','model_label':'terra'}))

    def test_ponytail_claim_without_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            write_json(folder/'ponytail-evidence.json',{'verified':True,'target_agent_types':['implementer']})
            with self.assertRaises(RuntimeError):validate_ponytail_seed(folder)
