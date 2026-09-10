from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def now(): return datetime.now(timezone.utc).isoformat()

def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    os.replace(temp,path)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def hashes(root):
    root=Path(root)
    return {str(p.relative_to(root)).replace('\\','/'):sha(p)
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()
            and not any(x in p.parts for x in ('.git','__pycache__')) and p.suffix!='.pyc'}

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()

def command(args, *, cwd=None, env=None, timeout=60, check=True):
    p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,capture_output=True,
                     text=True,encoding='utf-8',errors='replace',timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f'Command failed ({p.returncode}): {args[0]}\n{p.stderr[-2000:]}')
    return p

def safe_environment():
    # Never forward provider keys/auth state to candidate tests or external grading.
    names=('PATH','SystemRoot','WINDIR','COMSPEC','PATHEXT','TEMP','TMP','TMPDIR',
           'LANG','LC_ALL','SYSTEMDRIVE','NUMBER_OF_PROCESSORS')
    env={k:os.environ[k] for k in names if k in os.environ}
    env.update(PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    return env

def git(repo,*args,check=True):
    return command(['git','-C',repo,*args],check=check)

def init_git(repo):
    git(repo,'init','-q')
    git(repo,'config','user.name','Benchmark Local')
    git(repo,'config','user.email','benchmark@localhost')
    git(repo,'config','commit.gpgsign','false')
    git(repo,'config','core.autocrlf','false')
    hooks=Path(repo)/'.git/benchmark-empty-hooks'; hooks.mkdir(exist_ok=True)
    git(repo,'config','core.hooksPath',str(hooks.resolve()))
    git(repo,'add','--all'); git(repo,'commit','-qm','Frozen benchmark fixture')
    return git(repo,'rev-parse','HEAD').stdout.strip()

def grade(candidate, task, output):
    p=command([sys.executable,'-I',ROOT/'plumbline_bench/grader_process.py',
               '--candidate',candidate,'--task',task,'--output',output],
              cwd=Path(output).parent,env=safe_environment(),timeout=30,check=False)
    if not Path(output).exists():
        return {'passed':False,'grader_error':p.stderr[-3000:], 'exit_code':p.returncode}
    return read_json(output)
