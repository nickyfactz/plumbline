from __future__ import annotations
import ast
import contextlib
import json
import os
import queue
import random
import shutil
import signal
import subprocess
import sys
import threading
import time
import tomllib
from pathlib import Path
from .util import ROOT,command,digest,git,grade,hashes,init_git,now,read_json,safe_environment,sha,write_json
from .telemetry import collect
from .report import build_report

ARMS=('vanilla','plumbline')
TASKS=('jobqueue','configscope','docaccess')


def config_load(path):
    path=Path(path).resolve(); cfg=read_json(path)
    for key in ('state_root','pricing_file','auth_source_home','ponytail_seed'):
        if cfg.get(key):
            val=Path(os.path.expandvars(os.path.expanduser(cfg[key])))
            cfg[key]=str((path.parent/val).resolve() if not val.is_absolute() else val)
    if cfg.get('permission_mode','scoped-profile') not in ('scoped-profile','workspace-write'):
        raise ValueError('Use scoped-profile or explicitly calibrated workspace-write permissions')
    if cfg.get('hook_trust_mode','persisted') not in ('persisted','audited-bypass'):
        raise ValueError('Unknown hook trust mode')
    if cfg['root_effort'] not in ('medium','high'):
        raise ValueError('root_effort must be medium or high')
    if cfg['root_effort']=='high' and not cfg.get('uniform_role_profiles'):
        raise ValueError('high root effort requires the disclosed uniform-role test-flight override')
    if cfg['baseline_mode'] not in ('stock','single'): raise ValueError('baseline_mode must be stock or single')
    if cfg['ponytail_mode'] not in ('required','off'): raise ValueError('ponytail_mode must be required or off')
    for name,value in cfg['limits'].items():
        if name=='aggregate_tokens_per_run' and value is None: continue
        if not isinstance(value,(int,float)) or value<=0: raise ValueError('limits must be positive')
    if cfg.get('extra_codex_args'):
        raise ValueError('v1 does not permit unreviewed arbitrary CLI overrides; adapt the named host adapter and version it instead')
    return cfg


def codex_env(home):
    env=os.environ.copy()
    # Remove ambient session routing/model overrides; do not copy the parent chat context.
    for key in list(env):
        if key.startswith('CODEX_') or key in ('OPENAI_API_KEY','OPENAI_BASE_URL','PYTHONPATH','PYTHONHOME'):
            env.pop(key,None)
    user=Path(home)/'_user'; user.mkdir(exist_ok=True)
    env.update(CODEX_HOME=str(home),HOME=str(user),USERPROFILE=str(user),
               PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    # Ponytail's installed hook is trusted and uses this documented matcher
    # to scope SubagentStart guidance to the Plumbline implementer role.
    env['PONYTAIL_SUBAGENT_MATCHER']='^implementer$'
    # API keys are deliberately not auto-forwarded into a writable task environment.
    return env


def copy_auth(cfg,home):
    source=Path(cfg.get('auth_source_home') or os.environ.get('CODEX_HOME') or Path.home()/'.codex')
    if not cfg.get('reuse_saved_auth',True):
        if not (home/'auth.json').exists(): raise RuntimeError('Authenticate the isolated home first; saved-auth reuse is disabled')
        return
    auth=source/'auth.json'
    if not auth.is_file():
        raise RuntimeError('No file-backed Codex login found. The controller must authenticate a dedicated benchmark home using the installed Codex login flow and set auth_source_home. Never print credentials.')
    shutil.copy2(auth,home/'auth.json')
    with contextlib.suppress(OSError): (home/'auth.json').chmod(0o600)


def doctor(cfg):
    report={'python':sys.version,'git':None,'codex':None,'checks':[]}
    if sys.version_info<(3,11): raise RuntimeError('Python 3.11+ is required')
    report['git']=command(['git','--version']).stdout.strip()
    report['codex']=command([*cfg['codex_command'],'--version']).stdout.strip()
    helptext=command([*cfg['codex_command'],'app-server','--help']).stdout
    if '--stdio' not in helptext: raise RuntimeError('Installed Codex lacks app-server stdio transport; update the host adapter, not task fixtures')
    report['app_server_help_sha256']=digest(helptext)
    report['checks'].append('fresh Codex app-server stdio sessions found; effective permissions need local calibration')
    command([*cfg['codex_command'],'plugin','marketplace','add','--help'])
    command([*cfg['codex_command'],'plugin','add','--help'])
    source=Path(cfg.get('auth_source_home') or os.environ.get('CODEX_HOME') or Path.home()/'.codex')
    report['saved_auth_available']=(source/'auth.json').is_file()
    report['prices_date']=read_json(cfg['pricing_file'])['snapshot_date']
    report['live_model_availability']='not tested by doctor; paid calibration is separate'
    return report


def snapshot_plugin(cfg):
    state=Path(cfg['state_root']); vendor=state/'vendor'/('plumbline-'+digest([cfg['plumbline_source'],cfg['plumbline_ref']])[:12])
    if not vendor.exists():
        vendor.parent.mkdir(parents=True,exist_ok=True)
        command(['git','clone','--no-hardlinks','--no-checkout',cfg['plumbline_source'],vendor],timeout=180)
        git(vendor,'checkout','--detach',cfg['plumbline_ref'])
    actual=git(vendor,'rev-parse','HEAD').stdout.strip()
    if git(vendor,'status','--porcelain').stdout.strip(): raise RuntimeError('Pinned plugin snapshot was modified')
    for path in ('scripts/install_router.py','scripts/install_agent_team.py','skills/plumbline-execute/SKILL.md'):
        if not (vendor/path).is_file(): raise RuntimeError('Plumbline installer layout changed; refresh adapter before spending usage')
    return vendor,actual


def append_config(home,text):
    target=home/'config.toml'; old=target.read_text(encoding='utf-8') if target.exists() else ''
    merged=old+'\n'+text+'\n'; tomllib.loads(merged)
    target.write_text(merged,encoding='utf-8')


def set_default_permissions(home,name):
    target=Path(home)/'config.toml'; old=target.read_text(encoding='utf-8') if target.exists() else ''
    config=tomllib.loads(old) if old else {}
    current=config.get('default_permissions')
    if current not in (None,name):
        raise RuntimeError(f'Dedicated seed selects default_permissions={current!r}; refresh it before using {name!r}')
    if current==name: return
    target.write_text(f'default_permissions = {json.dumps(name)}\n'+old,encoding='utf-8')


def validate_ponytail_seed(source):
    source=Path(source).resolve()
    if any(p.is_symlink() for p in source.rglob('*')):
        raise RuntimeError('Ponytail seed must contain no symlinks')
    for forbidden in ('AGENTS.md','AGENTS.override.md','agents','skills'):
        if (source/forbidden).exists():
            raise RuntimeError('Ponytail seed is not minimal: unrelated instructions/agents/skills present')
    evidence=read_json(source/'ponytail-evidence.json')
    if evidence.get('target_agent_types')!=['implementer'] or evidence.get('verified') is not True:
        raise RuntimeError('Ponytail needs verified implementer-only evidence')
    for key,hash_key in (('hook_path','hook_sha256'),('verification_receipt','verification_receipt_sha256')):
        relative=Path(evidence.get(key,''))
        file=(source/relative).resolve()
        if not str(relative) or relative.is_absolute() or not file.is_relative_to(source) or not file.is_file():
            raise RuntimeError('Ponytail evidence must reference actual relative files inside its seed')
        if sha(file)!=evidence.get(hash_key):
            raise RuntimeError('Ponytail evidence hash mismatch: '+key)
    if not evidence.get('source_version') or not evidence.get('negative_controls'):
        raise RuntimeError('Record hook version and root/research/review/QA negative controls')
    return evidence


def make_seed(cfg,vendor,arm):
    source_hashes=hashes(cfg['ponytail_seed']) if arm=='plumbline' and cfg.get('ponytail_seed') else {}
    folder=Path(cfg['state_root'])/'seeds'/('seed-'+digest([str(vendor),arm,cfg['ponytail_mode'],source_hashes])[:12])
    marker=folder/'bench-seed.json'
    if marker.exists(): return folder
    if folder.exists(): raise RuntimeError(f'Incomplete seed exists: {folder}. Inspect it; do not silently overwrite a potentially active seed.')
    folder.mkdir(parents=True)
    with contextlib.suppress(OSError): folder.chmod(0o700)
    if arm=='plumbline' and cfg['ponytail_mode']=='required':
        if not cfg.get('ponytail_seed'):
            raise RuntimeError('Ponytail is required: controller must create an isolated native plugin seed with the real implementer-only hook. See docs/HOST_SETUP.md; no invented hook is substituted.')
        src=Path(cfg['ponytail_seed']); evidence=validate_ponytail_seed(src)
        for p in src.iterdir():
            if p.name in ('auth.json','sessions','archived_sessions','history.jsonl','log','_user'): continue
            if p.is_symlink(): raise RuntimeError('Seed symlinks are not allowed')
            if p.is_dir(): shutil.copytree(p,folder/p.name)
            else: shutil.copy2(p,folder/p.name)
        rebase_seed_paths(folder,src)
    if arm=='plumbline':
        env=codex_env(folder)
        for cmd in ([*cfg['codex_command'],'plugin','marketplace','add',str(vendor)],
                    [*cfg['codex_command'],'plugin','add','plumbline@plumbline']):
            p=command(cmd,env=env,timeout=120)
            with (folder/'setup.log').open('a',encoding='utf-8') as f: f.write(p.stdout+p.stderr)
    # Scalar configuration is supplied on the exec command so it cannot collide with
    # native plugin registry tables. Only project trust entries are appended later.
    write_json(marker,{'arm':arm,'vendor':str(vendor),'ponytail':cfg['ponytail_mode'] if arm=='plumbline' else 'off','created_at':now()})
    return folder


def rebase_seed_paths(home,source):
    old=str(Path(source).resolve()); new=str(Path(home).resolve())
    for p in home.rglob('*'):
        if p.is_file() and p.suffix in ('.toml','.json') and p.name!='auth.json':
            text=p.read_text(encoding='utf-8')
            text=text.replace(old.replace('\\','\\\\'),new.replace('\\','\\\\')).replace(old,new)
            p.write_text(text,encoding='utf-8')


def prepare(cfg,preset='pilot',repeat=1,models=None):
    if repeat<1: raise ValueError('repeat must be positive')
    state=Path(cfg['state_root']); state.mkdir(parents=True,exist_ok=True)
    if state.is_relative_to(ROOT): raise ValueError('Run state must live OUTSIDE the benchmark kit')
    checks=doctor(cfg)
    if not checks['saved_auth_available']: raise RuntimeError('Saved authentication unavailable; complete local authentication before preparing paid runs')
    # Validate Ponytail before cloning/creating seeds, avoiding partially initialized arm state.
    if cfg['ponytail_mode']=='required' and not cfg.get('ponytail_seed'):
        raise RuntimeError('Controller must prepare the real Ponytail seed before prepare. See docs/HOST_SETUP.md.')
    vendor,commit=snapshot_plugin(cfg)
    seeds={arm:make_seed(cfg,vendor,arm) for arm in ARMS}
    model_labels=models or (['terra'] if preset=='pilot' else list(cfg['models']))
    for model in model_labels:
        if model not in cfg['models']: raise ValueError('Unknown model label '+model)
    tasks=['configscope'] if preset=='pilot' else list(TASKS)
    matrix=[]; rng=random.Random(20260905)
    for n in range(1,repeat+1):
        pairs=[(task,model) for task in tasks for model in model_labels]; rng.shuffle(pairs)
        if n == 1 and ('configscope','terra') in pairs:
            pairs.remove(('configscope','terra')); pairs.insert(0,('configscope','terra'))
        for index,(task,model) in enumerate(pairs):
            arms=ARMS if (index+n)%2 else tuple(reversed(ARMS))
            for arm in arms: matrix.append({'task':task,'model_label':model,'arm':arm,'repeat':n})
    if len(matrix)>cfg['limits']['max_total_runs']: raise ValueError('Matrix exceeds max_total_runs; explicitly revise budget/config for repetitions')
    identity=time.strftime('%Y%m%d-%H%M%S')+'-'+digest([matrix,now()])[:6]
    campaign=state/'campaigns'/identity; campaign.mkdir(parents=True)
    (campaign/'runs').mkdir()
    manifest={'id':identity,'created_at':now(),'config':cfg,'plugin_commit':commit,'plugin_snapshot':str(vendor),
              'seeds':{k:str(v) for k,v in seeds.items()},'seed_hashes':{k:hashes(v) for k,v in seeds.items()},'host':checks,
              'fixture_hashes':{t:hashes(ROOT/'fixtures'/t) for t in tasks},
              'grader_hashes':hashes(ROOT/'graders'),'controller_hashes':hashes(ROOT/'plumbline_bench'),
              'prompt_sha256':sha(ROOT/'prompts/task.txt'),
              'pricing':read_json(cfg['pricing_file']),'matrix':matrix,'preset':preset}
    manifest['config']['disclosures'].update({
        'baseline_mode':cfg['baseline_mode'],'ponytail':cfg['ponytail_mode'],
        'plugin_commit':commit,'runner':'codex app-server stdio; one fresh root thread per cell; not desktop UI automation',
        'cost_model':'Standard input/cache-read/output equivalent; not an actual account debit'})
    for index,cell in enumerate(matrix): cell['id']=f"{index+1:03d}-{cell['task']}-{cell['model_label']}-{cell['arm']}-r{cell['repeat']}"
    write_json(campaign/'campaign.json',manifest)
    write_json(state/'latest.json',{'campaign':str(campaign)})
    build_report(campaign)
    return campaign


def agent_team_flags(cfg,cell):
    flags=['--update-agents']
    if cfg.get('uniform_role_profiles'):
        flags += ['--model',cfg['models'][cell['model_label']],
                  '--reasoning-effort',cfg['root_effort']]
    return flags


def stage(manifest,cell,run):
    cfg=manifest['config']; candidate=run/'project'; home=run/'codex-home'
    shutil.copytree(ROOT/'fixtures'/cell['task'],candidate,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    seed=Path(manifest['seeds'][cell['arm']])
    if hashes(seed)!=manifest['seed_hashes'][cell['arm']]:
        raise RuntimeError('Frozen plugin/hook seed drifted; create a new campaign')
    shutil.copytree(seed,home,ignore=shutil.ignore_patterns('auth.json','sessions','archived_sessions','history.jsonl','log','_user'))
    rebase_seed_paths(home,seed); copy_auth(cfg,home)
    base=init_git(candidate)
    protected_before=hashes(candidate)
    setup_start=time.monotonic()
    if cell['arm']=='plumbline':
        vendor=Path(manifest['plugin_snapshot'])
        for script,flags in [('install_router.py',[]),
                             ('install_agent_team.py',agent_team_flags(cfg,cell))]:
            p=command([sys.executable,str(vendor/'scripts'/script),'--root',str(candidate),*flags],timeout=60)
            with (run/'setup.log').open('a',encoding='utf-8') as f: f.write(p.stdout+p.stderr)
        for relative,value in protected_before.items():
            if relative!='AGENTS.md' and sha(candidate/relative)!=value:
                raise RuntimeError('Plumbline setup changed a source/contract/test file before execution')
        git(candidate,'add','AGENTS.md')
        git(candidate,'commit','-qm','Stage approved workflow guidance')
    cfg_file=home/'config.toml'
    existing=tomllib.loads(cfg_file.read_text(encoding='utf-8')) if cfg_file.exists() else {}
    if os.name=='nt' and existing.get('windows',{}).get('sandbox')!='elevated':
        if 'windows' in existing:
            raise RuntimeError('Dedicated seed selects a non-elevated Windows sandbox; refresh it before running')
        # The elevated backend is required for the isolated Windows workspace policy.
        append_config(home,'[windows]\nsandbox = "elevated"')
        existing=tomllib.loads(cfg_file.read_text(encoding='utf-8'))
    trust_key=str(candidate.resolve())
    if trust_key not in existing.get('projects',{}):
        append_config(home,'[projects.'+json.dumps(trust_key)+']\ntrust_level = "trusted"')
    if cfg.get('permission_mode','scoped-profile')=='scoped-profile':
        if 'sandbox_mode' in existing or 'sandbox_workspace_write' in existing:
            raise RuntimeError('Remove legacy sandbox settings from the dedicated seed before using scoped-profile; never change global settings')
        # Explicit write boundary allows local checkpoint commits without opening
        # the rest of the filesystem to writes. Role intent remains unchanged.
        set_default_permissions(home,'benchmark-local')
        append_config(home,'[permissions.benchmark-local.filesystem]\n":root" = "read"\n'
            + json.dumps(str(ROOT/'graders'))+' = "deny"\n'
            + json.dumps(str(ROOT/'reference'))+' = "deny"\n'
            + '[permissions.benchmark-local.filesystem.":workspace_roots"]\n'
            + '"." = "write"\n".git" = "write"\n".codex" = "read"\n".agents" = "read"\n'
            + '[permissions.benchmark-local.network]\nenabled = false')
    # Local config and agent files are ignored by Plumbline; preserve separate hashes.
    profiles={}
    for p in (candidate/'.codex/agents').glob('*.toml'):
        profile=tomllib.loads(p.read_text(encoding='utf-8'))
        profiles[p.stem]={k:profile.get(k) for k in ('name','model','model_reasoning_effort','sandbox_mode')}
        profiles[p.stem]['sha256']=sha(p)
    initial=hashes(candidate)
    write_json(run/'setup.json',{'base_commit':base,'execution_start_commit':git(candidate,'rev-parse','HEAD').stdout.strip(),
        'setup_seconds':time.monotonic()-setup_start,'initial_hashes':initial,'roles':profiles,
        'seed_hashes':hashes(seed),'protected':{k:v for k,v in initial.items()
            if k=='TASK.md' or k.startswith('tests/') or k.startswith('.codex/') or k.startswith('.agents/') or k=='AGENTS.md'}})
    return candidate,home


def process_alive(pid):
    if os.name=='nt':
        import ctypes
        handle=ctypes.windll.kernel32.OpenProcess(0x1000,False,pid)
        if not handle: return False
        code=ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(handle,ctypes.byref(code))
        ctypes.windll.kernel32.CloseHandle(handle)
        return code.value==259
    try: os.kill(pid,0); return True
    except ProcessLookupError: return False
    except PermissionError: return True


def stop_process(proc):
    if proc.poll() is not None: return
    if os.name=='nt':
        command(['taskkill','/PID',str(proc.pid),'/T','/F'],check=False)
    else:
        os.killpg(proc.pid,signal.SIGTERM)
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: os.killpg(proc.pid,signal.SIGKILL)
    with contextlib.suppress(subprocess.TimeoutExpired): proc.wait(timeout=10)


def app_server_command(cfg,cell):
    args=[*cfg['codex_command']]
    if cell['arm']=='plumbline' and cfg.get('hook_trust_mode','persisted')=='audited-bypass':
        args.append('--dangerously-bypass-hook-trust')
    if cell['arm']=='vanilla' and cfg['baseline_mode']=='single': args += ['-c','agents.enabled=false']
    args += ['app-server','--stdio']
    return args


def app_server_thread_params(cfg,cell,candidate):
    params={'model':cfg['models'][cell['model_label']], 'cwd':str(Path(candidate).resolve()),
            'approvalPolicy':'never', 'serviceName':'plumbline-benchmark', 'serviceTier':'default'}
    if cfg.get('permission_mode','scoped-profile')=='scoped-profile':
        params['permissions']='benchmark-local'
    else:
        params['sandbox']='workspace-write'
    return params


def app_server_turn_params(cfg,cell,candidate,thread_id,prompt):
    return {'threadId':thread_id, 'input':[{'type':'text','text':prompt}],
            'cwd':str(Path(candidate).resolve()), 'model':cfg['models'][cell['model_label']],
            'effort':cfg['root_effort'], 'serviceTierForTurn':'default'}


def normalize_app_server_item(item):
    item=dict(item or {})
    item['type']={'agentMessage':'agent_message','functionCallOutput':'function_call_output',
                  'commandExecution':'command_execution','collabAgentToolCall':'collab_agent_tool_call',
                  'subAgentActivity':'sub_agent_activity'}.get(item.get('type'),item.get('type'))
    if 'receiverThreadIds' in item: item['receiver_thread_ids']=item['receiverThreadIds']
    if 'senderThreadId' in item: item['sender_thread_id']=item['senderThreadId']
    if 'agentThreadId' in item: item['child_thread_id']=item['agentThreadId']
    return item


def normalize_app_server_usage(value):
    value=value or {}
    return {'input_tokens':int(value.get('inputTokens',0) or 0),
            'cached_input_tokens':int(value.get('cachedInputTokens',0) or 0),
            'output_tokens':int(value.get('outputTokens',0) or 0),
            'reasoning_output_tokens':int(value.get('reasoningOutputTokens',0) or 0),
            'cache_write_tokens':int(value.get('cacheWriteInputTokens',0) or 0)}


def normalize_app_server_event(message):
    method=message.get('method'); params=message.get('params') or {}
    if method=='thread/started':
        thread=params.get('thread') or {}
        return {'type':'thread.started','thread_id':thread.get('id'),'thread':thread}
    if method=='thread/tokenUsage/updated':
        usage=params.get('tokenUsage') or {}
        return {'type':'event_msg','thread_id':params.get('threadId'),'turn_id':params.get('turnId'),
                'payload':{'type':'token_count','info':{
                    'total_token_usage':normalize_app_server_usage(usage.get('total')),
                    'last_token_usage':normalize_app_server_usage(usage.get('last'))}}}
    if method=='item/completed':
        return {'type':'item.completed','thread_id':params.get('threadId'),
                'turn_id':params.get('turnId'),'item':normalize_app_server_item(params.get('item'))}
    if method=='turn/completed':
        turn=params.get('turn') or {}
        return {'type':'turn.completed','thread_id':params.get('threadId'),'turn_id':turn.get('id'),
                'status':turn.get('status'),'error':turn.get('error')}
    if method=='thread/status/changed':
        return {'type':'thread.status','thread_id':params.get('threadId'),'status':params.get('status')}
    return None


def send_app_server(proc,message_id,method,params=None):
    message={'jsonrpc':'2.0','method':method}
    if message_id is not None: message['id']=message_id
    if params is not None: message['params']=params
    proc.stdin.write(json.dumps(message,separators=(',',':'))+'\n'); proc.stdin.flush()


def app_server_reader(proc,raw_file,inbox):
    for line in proc.stdout:
        raw_file.write(line); raw_file.flush()
        try: inbox.put(json.loads(line))
        except json.JSONDecodeError: inbox.put({'_app_server_raw':line.rstrip('\n')})
    inbox.put(None)


def final_claim(path):
    if not Path(path).is_file(): return None
    for line in reversed(Path(path).read_text(encoding='utf-8',errors='replace').splitlines()):
        if line.strip()=='BENCHMARK_STATUS: COMPLETE': return True
        if line.strip()=='BENCHMARK_STATUS: INCOMPLETE': return False
    return None


def quality(candidate,initial):
    current=hashes(candidate); changed=[p for p,h in current.items() if initial.get(p)!=h]
    production=[p for p in changed if p.endswith('.py') and not p.startswith(('tests/','.codex/','.agents/'))]
    syntax=[]; lines=0; branch_nodes=0; imports=set()
    local={p.stem for p in candidate.iterdir() if p.suffix=='.py' or p.is_dir()}
    for name in production:
        text=(candidate/name).read_text(encoding='utf-8');lines+=len(text.splitlines())
        try:
            tree=ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node,ast.Import): imports.update(a.name.split('.')[0] for a in node.names)
                elif isinstance(node,ast.ImportFrom) and node.level==0 and node.module: imports.add(node.module.split('.')[0])
            branch_nodes+=sum(isinstance(x,(ast.If,ast.For,ast.While,ast.Try,ast.IfExp,ast.BoolOp)) for x in ast.walk(tree))
        except SyntaxError as exc: syntax.append(f'{name}:{exc.lineno}')
    return {'changed_files':len(changed),'changed_production_files':len(production),
            'lines_in_changed_production_files':lines,'branch_nodes_in_changed_files':branch_nodes,
            'syntax_errors':syntax,'unexpected_import_roots':sorted(imports-set(sys.stdlib_module_names)-local),'note':'Descriptive size/branch diagnostics; not a maintainability score.'}


def finalize(manifest,cell,run,status,started,wall):
    cfg=manifest['config']; candidate=run/'project'; home=run/'codex-home'
    setup=read_json(run/'setup.json'); initial=setup['initial_hashes']
    current=hashes(candidate)
    modified=[p for p,h in setup['protected'].items() if current.get(p)!=h]
    modified += [p for p in current if p not in initial and p.startswith(('.codex/','.agents/'))]
    immutable_problem=hashes(ROOT/'graders')!=manifest['grader_hashes'] or hashes(ROOT/'plumbline_bench')!=manifest['controller_hashes']
    try: external=grade(candidate,cell['task'],run/'grader.json')
    except subprocess.TimeoutExpired: external={'passed':False,'grader_error':'timeout'}
    public_clock=time.monotonic()
    try:
        public=command([sys.executable,'-m','unittest','discover','-s','tests','-v'],
                       cwd=candidate,env=safe_environment(),check=False,timeout=30)
    except subprocess.TimeoutExpired:
        public=subprocess.CompletedProcess([],124,'','Candidate tests exceeded the 30-second grader budget')
    (run/'public-tests.log').write_text(public.stdout+public.stderr,encoding='utf-8')
    usage=collect(home,run/'events.jsonl',manifest['pricing'],cfg['models'][cell['model_label']],finished=True)
    claim=final_claim(run/'last-message.txt')
    root=next((x for x in usage['threads'] if x.get('role')=='root'),{})
    mismatch=(root.get('model') not in (None,cfg['models'][cell['model_label']]) or
              root.get('effort') not in (None,cfg['root_effort']))
    if modified or immutable_problem or mismatch: status='INVALID'
    elif status=='FINISHED': status='PASS' if external.get('passed') and public.returncode==0 else 'FAIL'
    q=quality(candidate,initial)
    if (q['syntax_errors'] or q['unexpected_import_roots']) and status=='PASS': status='FAIL'
    result={**cell,'started_at':started,'finished_at':now(),'status':status,'wall_seconds':wall,
            'time_to_verified_seconds':wall+external.get('seconds',0)+time.monotonic()-public_clock if status=='PASS' else None,
            'completion_claim':claim,'false_completion':claim and status=='FAIL',
            'external_grade_passed':external.get('passed',False),'public_tests_exit_code':public.returncode,
            'acceptance_tests':external.get('acceptance',{}).get('tests',0),
            'acceptance_passed_checks':sum(x['status']=='pass' for x in external.get('acceptance',{}).get('checks',[])),
            'baseline_tests':external.get('regression',{}).get('tests',0),
            'root_profile_mismatch':mismatch,'protected_file_violations':modified,'controller_integrity_changed':immutable_problem,
            'usage':usage,'quality':q,'plugin_commit':manifest['plugin_commit'],
            'worker_profiles':setup['roles'],'controller_setup_cost':'not measured; excluded from execution metric'}
    if cell['arm']=='vanilla' and cfg['baseline_mode']=='single' and usage['worker_count']:
        result['status']='INVALID';result['baseline_violation']='worker observed with forced-single baseline'
    if result['status']!='PASS':result['time_to_verified_seconds']=None
    (run/'diff.patch').write_text(git(candidate,'diff',setup['execution_start_commit'],'--','.').stdout,encoding='utf-8')
    (run/'git-status.txt').write_text(git(candidate,'status','--short').stdout,encoding='utf-8')
    (run/'commits.txt').write_text(git(candidate,'log','--oneline',setup['execution_start_commit']+'..HEAD').stdout,encoding='utf-8')
    write_json(run/'final-source-hashes.json',current)
    write_json(run/'new-files.json',{p:h for p,h in current.items() if p not in initial})
    result['workflow_evidence']={'configured_role_count':len(setup['roles']), 'observed_worker_count':usage['worker_count'],
        'observed_roles':sorted({x['role'] for x in usage['threads'] if x.get('role') and x['role']!='root'}),
        'activation_note':'Configured capability and observed usage are separate; controller must review activation evidence before attributing outcomes.'}
    write_json(run/'usage.json',usage);write_json(run/'result.json',result)
    # Only remove the private copied credential; never alter the source login.
    with contextlib.suppress(OSError): (home/'auth.json').unlink()
    return result


def run_app_server_session(manifest,cell,candidate,home,prompt,run):
    cfg=manifest['config']; argv=app_server_command(cfg,cell)
    events_path=run/'events.jsonl'; started=now(); clock=time.monotonic()
    status='FINISHED'; thread_id=None; turn_id=None; completed=False; last_message=None; protocol_error=None
    inbox=queue.Queue(); options={'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
    with (run/'app-server.jsonl').open('w',encoding='utf-8') as raw,(events_path).open('w',encoding='utf-8') as events,(run/'stderr.log').open('w',encoding='utf-8') as stderr:
        proc=subprocess.Popen(argv,cwd=candidate,env=codex_env(home),stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                              stderr=stderr,text=True,encoding='utf-8',bufsize=1,**options)
        write_json(run/'active.json',{'pid':proc.pid,'started_at':started,'run':cell['id'],'state':'running'})
        reader=threading.Thread(target=app_server_reader,args=(proc,raw,inbox),daemon=True); reader.start()
        requests=[]

        def send(message_id,method,params=None):
            requests.append({'id':message_id,'method':method,'params':params})
            send_app_server(proc,message_id,method,params)

        def record(event):
            if event:
                events.write(json.dumps(event,separators=(',',':'))+'\n');events.flush()

        def limits_reached():
            elapsed=time.monotonic()-clock
            usage=collect(home,events_path,manifest['pricing'],cfg['models'][cell['model_label']])
            tokens=usage['tokens']['input_tokens']+usage['tokens']['output_tokens']; limit=cfg['limits']
            reached=None
            if elapsed>limit['wall_seconds_per_run']: reached='TIMEOUT'
            elif limit.get('aggregate_tokens_per_run') is not None and tokens>limit['aggregate_tokens_per_run']: reached='BUDGET_EXHAUSTED'
            elif (usage['observed_cost_estimate_usd'] or 0)>limit['max_run_estimated_usd']: reached='BUDGET_EXHAUSTED'
            elif elapsed>limit['telemetry_grace_seconds'] and not usage['threads']: reached='TELEMETRY_UNAVAILABLE'
            return reached,elapsed,tokens

        send(1,'initialize',{'clientInfo':{'name':'plumbline-benchmark','title':'Plumbline Benchmark','version':'1.0'},
                             'capabilities':{'experimentalApi':True}})
        pending={1:'initialize'}; last_print=clock
        try:
            while True:
                try: message=inbox.get(timeout=1)
                except queue.Empty:
                    message=None if proc.poll() is not None else ...
                if message is ...:
                    reached,elapsed,tokens=limits_reached()
                    if time.monotonic()-last_print>15:
                        write_json(run/'heartbeat.json',{'elapsed_seconds':elapsed,'observed_tokens':tokens,'state':status})
                        print(f"{cell['id']}: {int(elapsed)}s, {tokens} observed tokens",flush=True);last_print=time.monotonic()
                    if reached: status=reached;break
                    continue
                if message is None:
                    if not completed and status=='FINISHED': status='HOST_ERROR'
                    break
                if '_app_server_raw' in message: continue

                event=normalize_app_server_event(message);record(event)
                message_id=message.get('id')
                if 'error' in message:
                    error=message['error'] or {};protocol_error=error.get('message') or str(error);status='HOST_ERROR';break
                if message_id in pending:
                    phase=pending.pop(message_id)
                    result=message.get('result') or {}
                    if phase=='initialize':
                        send(None,'initialized',{})
                        send(2,'thread/start',app_server_thread_params(cfg,cell,candidate));pending[2]='thread/start'
                    elif phase=='thread/start':
                        thread=(result.get('thread') or {})
                        thread_id=thread.get('id')
                        if not thread_id: protocol_error='thread/start returned no thread id';status='HOST_ERROR';break
                        record({'type':'thread.started','thread_id':thread_id,'thread':thread})
                        send(3,'turn/start',app_server_turn_params(cfg,cell,candidate,thread_id,prompt));pending[3]='turn/start'
                    elif phase=='turn/start':
                        turn_id=(result.get('turn') or {}).get('id')
                method=message.get('method'); params=message.get('params') or {}
                if method=='item/completed' and params.get('threadId')==thread_id:
                    item=params.get('item') or {}
                    if item.get('type')=='agentMessage' and isinstance(item.get('text'),str): last_message=item['text']
                if method=='thread/started' and thread_id is None:
                    thread_id=(params.get('thread') or {}).get('id')
                if method=='turn/completed' and params.get('threadId')==thread_id:
                    turn=params.get('turn') or {}; completed=True
                    turn_status=turn.get('status')
                    if isinstance(turn_status,dict): turn_status=turn_status.get('type')
                    status='FINISHED' if turn_status=='completed' else ('INTERRUPTED' if turn_status=='interrupted' else 'HOST_ERROR')
                    break
                reached,elapsed,tokens=limits_reached()
                if time.monotonic()-last_print>15:
                    write_json(run/'heartbeat.json',{'elapsed_seconds':elapsed,'observed_tokens':tokens,'state':status})
                    print(f"{cell['id']}: {int(elapsed)}s, {tokens} observed tokens",flush=True);last_print=time.monotonic()
                if reached: status=reached;break
        except KeyboardInterrupt:
            status='INTERRUPTED'
        finally:
            if completed and proc.poll() is None:
                with contextlib.suppress(OSError): proc.stdin.close()
                try: proc.wait(timeout=10)
                except subprocess.TimeoutExpired: stop_process(proc)
            elif proc.poll() is None:
                stop_process(proc)
            reader.join(timeout=2)
            with contextlib.suppress(OSError): proc.stdout.close()
            with contextlib.suppress(OSError): proc.stdin.close()
        write_json(run/'app-server-session.json',{'protocol':'jsonrpc-2.0','argv':argv,'requests':requests,
                    'thread_id':thread_id,'turn_id':turn_id,'status':status,'error':protocol_error})
    if last_message is not None: (run/'last-message.txt').write_text(last_message,encoding='utf-8')
    if not completed and status=='FINISHED': status='HOST_ERROR'
    return status,started,time.monotonic()-clock


def run_one(manifest,cell,campaign):
    cfg=manifest['config'];run=campaign/'runs'/cell['id'];run.mkdir()
    candidate,home=stage(manifest,cell,run)
    prompt=(ROOT/'prompts/task.txt').read_text(encoding='utf-8')
    (run/'prompt.txt').write_text(prompt,encoding='utf-8')
    argv=app_server_command(cfg,cell)
    write_json(run/'invocation.json',{'argv':argv,'cwd':str(candidate.resolve()),'model':cfg['models'][cell['model_label']],
        'prompt_sha256':digest(prompt),'fresh_session':True,'transport':'app-server-stdio',
        'thread_start':app_server_thread_params(cfg,cell,candidate),'turn_input_type':'text'})
    status,started,wall=run_app_server_session(manifest,cell,candidate,home,prompt,run)
    result=finalize(manifest,cell,run,status,started,wall)
    write_json(run/'active.json',{'pid':read_json(run/'active.json')['pid'],'state':'finished','finished_at':now()})
    return result


def run_campaign(campaign,max_runs=None):
    campaign=Path(campaign).resolve();manifest=read_json(campaign/'campaign.json');cfg=manifest['config']
    lock=campaign/'controller.lock'
    try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError: raise RuntimeError('Campaign locked. Use status/recover; never start a duplicate controller.')
    os.write(fd,str(os.getpid()).encode());os.close(fd)
    try:
        if hashes(ROOT/'graders')!=manifest['grader_hashes'] or hashes(ROOT/'plumbline_bench')!=manifest['controller_hashes']:
            raise RuntimeError('Controller/grader changed after freeze; create a new campaign')
        if any(hashes(ROOT/'fixtures'/task)!=h for task,h in manifest['fixture_hashes'].items()):
            raise RuntimeError('Fixture changed after freeze')
        snapshot=Path(manifest['plugin_snapshot'])
        if git(snapshot,'rev-parse','HEAD').stdout.strip()!=manifest['plugin_commit'] or git(snapshot,'status','--porcelain').stdout.strip():
            raise RuntimeError('Pinned Plumbline snapshot drifted')
        if sha(ROOT/'prompts/task.txt')!=manifest['prompt_sha256']:
            raise RuntimeError('Task prompt changed after freeze')
        current_host=command([*cfg['codex_command'],'--version']).stdout.strip()
        if current_host!=manifest['host']['codex']:
            raise RuntimeError('Codex build changed after freeze; use a new campaign')
        count=0
        for cell in manifest['matrix']:
            run=campaign/'runs'/cell['id']
            if (run/'result.json').exists(): continue
            if run.exists(): raise RuntimeError(f'Unfinalized run {cell["id"]}; use recover, not a rerun')
            previous=[read_json(p) for p in (campaign/'runs').glob('*/result.json')]
            if cfg['stop_on_telemetry_gap'] and any(r.get('usage',{}).get('coverage')!='complete-observed' for r in previous):
                print('Stopped: telemetry gap requires inspection; no additional paid calls.',flush=True);break
            if any(r['status'] in ('HOST_ERROR','SETUP_ERROR','HARNESS_ERROR','TELEMETRY_UNAVAILABLE','INVALID','INTERRUPTED') for r in previous):
                print('Stopped: infrastructure/integrity issue requires inspection.',flush=True);break
            spent=sum(r.get('usage',{}).get('observed_cost_estimate_usd') or 0 for r in previous)
            if spent+cfg['limits']['max_run_estimated_usd']>cfg['limits']['max_campaign_estimated_usd']:
                print('Stopped: remaining campaign budget is below the per-run reservation.',flush=True);break
            print('Starting '+cell['id'],flush=True)
            try:
                result=run_one(manifest,cell,campaign)
            except Exception as exc:
                run.mkdir(exist_ok=True)
                active=read_json(run/'active.json') if (run/'active.json').exists() else {}
                if active.get('pid') and process_alive(active['pid']):
                    raise RuntimeError('A candidate is still active after a controller error. Keep the lock/evidence and reconcile it before another run.') from exc
                usage=collect(run/'codex-home',run/'events.jsonl',manifest['pricing'],cfg['models'][cell['model_label']],finished=True)
                elapsed=read_json(run/'heartbeat.json').get('elapsed_seconds',0) if (run/'heartbeat.json').exists() else 0
                result={**cell,'status':'HARNESS_ERROR' if active else 'SETUP_ERROR','error':f'{type(exc).__name__}: {exc}',
                        'wall_seconds':elapsed,'started_at':active.get('started_at'),'usage':usage}
                write_json(run/'result.json',result)
                with contextlib.suppress(OSError): (run/'codex-home/auth.json').unlink()
            print(cell['id']+': '+result['status'],flush=True)
            build_report(campaign);count+=1
            if max_runs is not None and count>=max_runs: break
        return build_report(campaign)
    finally:
        with contextlib.suppress(OSError):lock.unlink()


def recover(campaign):
    campaign=Path(campaign);manifest=read_json(campaign/'campaign.json')
    lock=campaign/'controller.lock'
    if lock.exists():
        if process_alive(int(lock.read_text())): raise RuntimeError('Controller still running; do not duplicate it')
        lock.unlink()
    for cell in manifest['matrix']:
        run=campaign/'runs'/cell['id']
        if not run.exists() or (run/'result.json').exists(): continue
        active=read_json(run/'active.json') if (run/'active.json').exists() else {}
        if active.get('pid') and process_alive(active['pid']): raise RuntimeError('Candidate process still active; observe it rather than restarting')
        if (run/'setup.json').exists():
            elapsed=read_json(run/'heartbeat.json').get('elapsed_seconds',0) if (run/'heartbeat.json').exists() else 0
            finalize(manifest,cell,run,'INTERRUPTED',active.get('started_at'),elapsed)
        else:
            write_json(run/'result.json',{**cell,'status':'SETUP_ERROR','wall_seconds':0,
                       'error':'Interrupted during staging','usage':{'coverage':'incomplete','cost_estimate_usd':None}})
    return build_report(campaign)
