from __future__ import annotations
import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from .util import ROOT,read_json,write_json
from .runner import config_load,doctor,prepare,recover,run_campaign
from .report import build_report


def main():
    parser=argparse.ArgumentParser(description='Stage, execute and score compact Codex implementation benchmarks.')
    parser.add_argument('--config',default=str(ROOT/'config.local.json'))
    sub=parser.add_subparsers(dest='action',required=True)
    sub.add_parser('init-config'); sub.add_parser('selftest'); sub.add_parser('doctor')
    p=sub.add_parser('prepare');p.add_argument('--preset',choices=('pilot','full'),default='pilot')
    p.add_argument('--repeat',type=int,default=1);p.add_argument('--models',help='Comma-separated labels')
    p=sub.add_parser('run');p.add_argument('--campaign',default='latest');p.add_argument('--max-runs',type=int)
    for name in ('status','report','recover'):
        p=sub.add_parser(name);p.add_argument('--campaign',default='latest')
    p=sub.add_parser('import-charges');p.add_argument('--campaign',default='latest');p.add_argument('--file',required=True)
    args=parser.parse_args()
    try:
        if args.action=='init-config':
            path=Path(args.config)
            if path.exists(): print(str(path)+' already exists; left unchanged');return 0
            path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'config.example.json',path)
            print(path);return 0
        if args.action=='selftest':
            return subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],cwd=ROOT).returncode
        cfg=config_load(args.config)
        if args.action=='doctor': print(json.dumps(doctor(cfg),indent=2));return 0
        if args.action=='prepare':
            print(prepare(cfg,args.preset,args.repeat,args.models.split(',') if args.models else None));return 0
        campaign=Path(read_json(Path(cfg['state_root'])/'latest.json')['campaign']) if args.campaign=='latest' else Path(args.campaign).resolve()
        if args.action=='run':
            if args.max_runs is not None and args.max_runs<1: raise ValueError('--max-runs must be positive')
            result=run_campaign(campaign,args.max_runs)
        elif args.action=='recover': result=recover(campaign)
        elif args.action=='import-charges':
            charges=read_json(args.file)
            ids={x['id'] for x in read_json(campaign/'campaign.json')['matrix']}
            for entry in charges:
                if entry.get('run_id') not in ids or not entry.get('evidence') or not entry.get('unit'):
                    raise ValueError('Every charge needs a known run_id, unit and authoritative evidence reference')
                if isinstance(entry.get('amount'),bool) or not isinstance(entry.get('amount'),(int,float)) or not math.isfinite(entry['amount']) or entry['amount']<0:
                    raise ValueError('Charge amount must be a non-negative number')
            write_json(campaign/'account-charges.json',charges)
            result=build_report(campaign)
        else: result=build_report(campaign)
        print(json.dumps({'campaign':str(campaign),'recorded':result['completed_runs'],'planned':result['planned_runs'],
                          'report':str(campaign/'report.html')},indent=2));return 0
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError,KeyError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 2
