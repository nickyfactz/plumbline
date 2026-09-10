from __future__ import annotations
import csv
import html
import json
import re
from collections import defaultdict
from pathlib import Path
from .telemetry import collect
from .util import ROOT,read_json,write_json,now


def report_usage(campaign,manifest,result):
    run=campaign/'runs'/result['id'];events=run/'events.jsonl';home=run/'codex-home'
    pricing=manifest.get('pricing')
    if not pricing or not events.is_file() or not home.is_dir(): return result.get('usage',{})
    pricing=dict(pricing);pricing['model_aliases']=dict(pricing.get('model_aliases',{}))
    pricing['model_aliases'].setdefault('gpt-reserve','gpt-5.6-luna')
    model=manifest.get('config',{}).get('models',{}).get(result['model_label'])
    return collect(home,events,pricing,model,finished=True)

def token_total(usage):
    tokens=usage.get('tokens',{})
    return tokens.get('input_tokens',0)+tokens.get('output_tokens',0)

def observed_cost(usage):
    value=usage.get('observed_cost_estimate_usd')
    if value is None: return usage.get('cost_estimate_usd')
    if token_total(usage)==0 and usage.get('warnings'): return None
    return value

def terminal_observed(usage):
    threads=usage.get('threads',[])
    return bool(threads) and all(thread.get('terminal') for thread in threads)

def task_scorecard(task):
    path=ROOT/'fixtures'/task/'TASK.md';title='';items={};current=None
    if not path.is_file(): return {'title':title,'items':items}
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped=line.strip()
        if line.startswith('# '): title=line[2:].strip()
        match=re.match(r'^([A-Z]\d{2})\.\s+(.*)$',stripped)
        if match:
            current=match.group(1);items[current]=match.group(2).strip()
        elif current and stripped and not stripped.startswith('#'):
            items[current]+=' '+stripped
    return {'title':title,'items':items}

def grader_checks(campaign,result,scorecard):
    path=campaign/'runs'/result['id']/'grader.json'
    if not path.is_file(): return {}
    grader=read_json(path);checks={}
    for suite in ('regression','acceptance'):
        for check in grader.get(suite,{}).get('checks',[]):
            check_id=check.get('id','');codes=[code for code in re.findall(r'(?<![A-Z0-9])([A-Z]\d{2})(?![A-Z0-9])',check_id) if code in scorecard['items']]
            detail=' '.join(str(check.get('detail','')).split())
            checks[(suite,check_id)]={'suite':suite,'id':check_id,'codes':codes,
                'description':' '.join(scorecard['items'][code] for code in codes) or ('Existing regression test' if suite=='regression' else 'Acceptance check'),
                'status':check.get('status'),'detail':detail}
    return checks

def markdown_text(value):
    return str(value or '').replace('|','\\|')

def check_status(check):
    return 'N/A' if check is None else str(check.get('status','unknown')).upper()

def check_detail(check):
    if not check or not check.get('detail'): return ''
    detail=check['detail'];return detail if len(detail)<=220 else detail[:217]+'...'

def validity_issue(result):
    issues=[]
    if result.get('protected_file_violations'): issues.append('protected: '+', '.join(result['protected_file_violations']))
    if result.get('root_profile_mismatch'): issues.append('root profile mismatch')
    if result.get('controller_integrity_changed'): issues.append('controller/grader changed')
    return '; '.join(issues)


def build_report(campaign):
    campaign=Path(campaign); manifest=read_json(campaign/'campaign.json')
    results=[read_json(p) for p in sorted((campaign/'runs').glob('*/result.json'))]
    usages={r['id']:report_usage(campaign,manifest,r) for r in results}
    charges=read_json(campaign/'account-charges.json') if (campaign/'account-charges.json').exists() else []
    groups=defaultdict(list)
    for r in results: groups[(r['model_label'],r['arm'])].append(r)
    summary=[]
    for (model,arm),runs in groups.items():
        successes=sum(r['status']=='PASS' for r in runs)
        behavioral_passes=sum(r.get('external_grade_passed') is True for r in runs)
        run_usages=[usages[r['id']] for r in runs]
        complete_costs=[u.get('cost_estimate_usd') for u in run_usages]
        observed_costs=[observed_cost(u) for u in run_usages]
        all_costs=all(value is not None for value in complete_costs)
        all_observed_costs=all(value is not None for value in observed_costs)
        total=sum(complete_costs) if all_costs else None
        observed_total=sum(observed_costs) if all_observed_costs else None
        elapsed=sum(r.get('wall_seconds',0) for r in runs)
        verified_seconds=[r['time_to_verified_seconds'] for r in runs if r.get('time_to_verified_seconds') is not None]
        summary.append({'model':model,'arm':arm,'attempts':len(runs),'passes':successes,
            'behavioral_passes':behavioral_passes,
            'pass_rate':successes/len(runs),'total_estimated_usd':total,
            'theoretical_total_usd':observed_total,
            'observed_cost_per_pass':observed_total/successes if observed_total is not None and successes else None,
            'complete_cost_per_pass':total/successes if total is not None and successes else None,
            'observed_seconds_per_pass':elapsed/successes if successes else None,
            'mean_success_seconds':sum(verified_seconds)/len(verified_seconds) if verified_seconds else None,
            'false_completions':sum(r.get('false_completion') is True for r in runs),
            'unknown_completion_claims':sum(r.get('completion_claim') is None for r in runs),
            'incomplete_cost_runs':sum(value is None for value in complete_costs)})
    attribution=[]
    for run in results:
        for thread in usages[run['id']].get('threads',[]):
            attribution.append({'run':run['id'],'thread':thread['id'],'role':thread.get('role'),
                'actual_model':thread.get('model'),'effort':thread.get('effort'),
                'estimated_usd':thread.get('cost_estimate_usd'),'tokens':thread.get('tokens'),
                'warnings':thread.get('warnings',[])})
    actual=[]
    for (model,arm),runs in groups.items():
        ids={x['id'] for x in runs}
        units={x['unit'] for x in charges if x['run_id'] in ids}
        for unit in units:
            matched=[x for x in charges if x['run_id'] in ids and x['unit']==unit]
            covered={x['run_id'] for x in matched}; successes=sum(x['status']=='PASS' for x in runs)
            complete=ids==covered; total=sum(x['amount'] for x in matched)
            actual.append({'model':model,'arm':arm,'unit':unit,'covered_runs':len(covered),
                           'total_runs':len(ids),'covered_amount':total,'complete':complete,
                           'actual_amount_per_pass':total/successes if complete and successes else None})
    pairs=defaultdict(dict)
    for r in results: pairs[(r['task'],r['model_label'],r['repeat'])][r['arm']]=r
    scorecards={task:task_scorecard(task) for task in {r['task'] for r in results}}
    pair_rows=[]
    scorecard_rows=[]
    for key,arms in pairs.items():
        a=arms.get('vanilla'); b=arms.get('plumbline')
        if not a or not b: continue
        ua=usages[a['id']];ub=usages[b['id']]
        ca=observed_cost(ua);cb=observed_cost(ub)
        delta=cb-ca if ca is not None and cb is not None else None
        pair_rows.append({'task':key[0],'model':key[1],'repeat':key[2],
                         'vanilla':a['status'],'plumbline':b['status'],
                         'vanilla_behavioral_grade':a.get('external_grade_passed'),
                         'plumbline_behavioral_grade':b.get('external_grade_passed'),
                         'vanilla_execution_complete':a['status']=='PASS',
                         'plumbline_execution_complete':b['status']=='PASS',
                         'vanilla_total_tokens':token_total(ua),'plumbline_total_tokens':token_total(ub),
                         'vanilla_tokens':ua.get('tokens',{}),'plumbline_tokens':ub.get('tokens',{}),
                         'vanilla_theoretical_usd':ca,'plumbline_theoretical_usd':cb,
                         'cost_delta_usd':delta,
                         'cost_delta_percent':delta/ca*100 if delta is not None and ca else None})
        vanilla_checks=grader_checks(campaign,a,scorecards[key[0]])
        plumbline_checks=grader_checks(campaign,b,scorecards[key[0]])
        for check_key in sorted(set(vanilla_checks)|set(plumbline_checks)):
            vanilla_check=vanilla_checks.get(check_key);plumbline_check=plumbline_checks.get(check_key)
            source=vanilla_check or plumbline_check
            scorecard_rows.append({'task':key[0],'model':key[1],'repeat':key[2],
                'suite':source['suite'],'check_id':source['id'],'codes':source['codes'],
                'description':source['description'],'vanilla_status':check_status(vanilla_check),
                'plumbline_status':check_status(plumbline_check),'vanilla_detail':check_detail(vanilla_check),
                'plumbline_detail':check_detail(plumbline_check)})
    report={'generated_at':now(),'campaign':manifest['id'],'planned_runs':len(manifest['matrix']),
            'completed_runs':len(results),'summary':summary,'paired_results':pair_rows,'imported_account_cost':actual,
            'disclosures':manifest['config']['disclosures'],'thread_attribution':attribution,
            'task_scorecards':scorecards,'scorecard_comparisons':scorecard_rows,
            'note':'Descriptive observed spend/pass, NOT a guaranteed expected retry cost. Small fixed task suite; no universal significance claim.'}
    write_json(campaign/'report.json',report)
    def fmt(x): return 'N/A' if x is None else f'{x:.4f}'
    def intfmt(x): return 'N/A' if x is None else f'{int(x):,}'
    def label(value): return 'N/A' if value is None else ('PASS' if value else 'FAIL')
    def claim(value): return 'UNKNOWN' if value is None else ('COMPLETE' if value else 'INCOMPLETE')
    def execution(result): return 'COMPLETE' if result['status']=='PASS' else 'STOPPED: '+result['status']
    lines=['# Plumbline benchmark report','',
           f"Campaign `{manifest['id']}` — {len(results)}/{len(manifest['matrix'])} runs recorded.",'',
           '**Execution success:** `status=PASS` only. A behavioral grade is reported separately because the grader runs after a stopped turn.',
           '**Cost basis:** observed Luna-equivalent rate-card estimates, not subscription credits or actual charges. Complete-priced totals remain suppressed when telemetry is incomplete.','',
           '| Root | Arm | Execution passes / attempts | Behavioral grades / attempts | Luna-equiv observed $ | Complete priced $ | Cost gaps |',
           '|---|---|---:|---:|---:|---:|---:|']
    for s in summary:
        lines.append(f"| {s['model']} | {s['arm']} | {s['passes']}/{s['attempts']} | {s['behavioral_passes']}/{s['attempts']} | {fmt(s['theoretical_total_usd'])} | {fmt(s['total_estimated_usd'])} | {s['incomplete_cost_runs']} |")
    lines+=['','## Matched arm comparisons','',
            '| Task | Root | Vanilla | Plumbline | Vanilla tokens | Plumbline tokens | Vanilla Luna-equiv $ | Plumbline Luna-equiv $ | Delta $ | Delta % |',
            '|---|---|---|---|---:|---:|---:|---:|---:|---:|']
    for pair in pair_rows:
        lines.append(f"| {pair['task']} | {pair['model']} | {pair['vanilla']} / {label(pair['vanilla_behavioral_grade'])} | {pair['plumbline']} / {label(pair['plumbline_behavioral_grade'])} | {intfmt(pair['vanilla_total_tokens'])} | {intfmt(pair['plumbline_total_tokens'])} | {fmt(pair['vanilla_theoretical_usd'])} | {fmt(pair['plumbline_theoretical_usd'])} | {fmt(pair['cost_delta_usd'])} | {fmt(pair['cost_delta_percent'])} |")
    lines+=['','## Task scorecards','']
    scorecard_groups=defaultdict(list)
    for row in scorecard_rows: scorecard_groups[(row['task'],row['model'],row['repeat'])].append(row)
    for key,rows in sorted(scorecard_groups.items()):
        contract=scorecards[key[0]]
        lines.append(f"### {key[0]} — {contract['title']} ({key[1]}, repeat {key[2]})")
        lines+=['','| Suite | Check | Requirement | Vanilla | Plumbline | Details |','|---|---|---|---|---|---|']
        for row in rows:
            codes='+'.join(row['codes']) or '—';details=[]
            if row['vanilla_detail']: details.append('V: '+row['vanilla_detail'])
            if row['plumbline_detail']: details.append('P: '+row['plumbline_detail'])
            lines.append(f"| {row['suite']} | {row['check_id'].split('.')[-1]} | {codes}: {markdown_text(row['description'])} | {row['vanilla_status']} | {row['plumbline_status']} | {markdown_text(' '.join(details))} |")
    lines+=['','## Mixed-model execution attribution','',
        '| Run | Role | Actual model | Effort | Observed estimated $ |',
        '|---|---|---|---|---:|']
    for item in attribution:
        amount=None if item['warnings'] else item['estimated_usd']
        lines.append(f"| {item['run']} | {item['role'] or 'unresolved'} | {item['actual_model'] or 'unresolved'} | {item['effort'] or 'unresolved'} | {fmt(amount)} |")
    if actual:
        lines+=['','## Evidence-backed imported account debit','',
                '| Root | Arm | Unit | Covered runs | Covered amount | Amount/pass (complete only) |',
                '|---|---|---|---:|---:|---:|']
        for item in actual:
            lines.append(f"| {item['model']} | {item['arm']} | {item['unit']} | {item['covered_runs']}/{item['total_runs']} | {fmt(item['covered_amount'])} | {fmt(item['actual_amount_per_pass'])} |")
    lines+=['','## Individual results','',
            '| Run | Task | Root | Arm | Execution | Grade | Claim | Acceptance | Validity issue | Input | Cached | Output | Luna-equiv observed $ | Complete priced $ | Workers | Terminal telemetry |',
            '|---|---|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
    flat=[]
    for r in results:
        u=usages[r['id']]; row={'run':r['id'],'task':r['task'],'root':r['model_label'],'arm':r['arm'],
            'status':r['status'],'wall_seconds':r.get('wall_seconds'),
            'verified_seconds':r.get('time_to_verified_seconds'),'estimated_usd':u.get('cost_estimate_usd'),
            'workers':u.get('worker_count'),'acceptance_passed_checks':r.get('acceptance_passed_checks'),
            'acceptance_tests':r.get('acceptance_tests'),'changed_production_files':r.get('quality',{}).get('changed_production_files'),
            'validity_issue':validity_issue(r),'theoretical_estimated_usd':observed_cost(u),'terminal_telemetry':terminal_observed(u),
            **{k:u.get('tokens',{}).get(k) for k in ('input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens')}}
        flat.append(row)
        lines.append(f"| {r['id']} | {r['task']} | {r['model_label']} | {r['arm']} | {execution(r)} | {label(r.get('external_grade_passed'))} | {claim(r.get('completion_claim'))} | {r.get('acceptance_passed_checks')}/{r.get('acceptance_tests')} | {markdown_text(row['validity_issue']) or '—'} | {intfmt(row['input_tokens'])} | {intfmt(row['cached_input_tokens'])} | {intfmt(row['output_tokens'])} | {fmt(row['theoretical_estimated_usd'])} | {fmt(row['estimated_usd'])} | {row['workers']} | {'yes' if row['terminal_telemetry'] else 'no'} |")
    lines+=['','## Interpretation and disclosure','',
        'Compare matched cohorts only: a budget-stopped partial matrix is not a fair aggregate win unless both arms cover the same task/model/repeat cells.',
        'BUDGET_EXHAUSTED is execution-incomplete even when the post-stop grader reports 12/12: the controller stopped the live turn before turn/completed, then graded the workspace. No completion claim or verified-success time is inferred.',
        'A failure has no time-to-success. Zero successes means cost/pass is undefined, never $0.',
        'All attempted runs remain in spend totals; infrastructure failures, timeouts and interrupted runs are visible.',
        'No hidden-grader feedback is returned to a candidate; there are no automatic implementation retries.',
        'PASS requires the external acceptance suite, preserved baseline regression suite, unchanged protected files and a successful public-test run.',
        'Code size and token counts are diagnostics, not rewards. No subjective judge contributes to PASS.',
        'A stock baseline may use native subagents. A forced-single baseline is separately labeled in the campaign configuration.',
        'Plumbline with Ponytail is a combined deployed-stack result, not isolated causal attribution to Plumbline.',
        'Do not infer unseen worker costs, exact account debits, cache-write charges, or improved maintainability from missing evidence.','',
        '```json',json.dumps(manifest['config']['disclosures'],indent=2),'```']
    (campaign/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if flat:
        with (campaign/'scorecards.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(flat[0])); writer.writeheader();writer.writerows(flat)
    if scorecard_rows:
        with (campaign/'scorecard-checks.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(scorecard_rows[0])); writer.writeheader();writer.writerows(scorecard_rows)
    # Self-contained browser report, no external scripts or assets.
    page='<!doctype html><meta charset="utf-8"><title>Plumbline benchmark</title><style>body{font:15px system-ui;max-width:1300px;margin:40px auto;padding:0 24px}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:9px;border-bottom:1px solid #ddd}pre{white-space:pre-wrap}h1{font-size:30px}</style>'
    page+='<h1>Plumbline benchmark</h1><p>'+html.escape(lines[2])+'</p><p>Observed execution cost per verified completion. Estimates; not account charges.</p>'
    page+='<table><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in ['Root','Arm','Passes','Attempts','Estimated $/pass','Cost gaps'])+'</tr>'
    for s in summary:
        page+='<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [s['model'],s['arm'],s['passes'],s['attempts'],fmt(s['observed_cost_per_pass']),s['incomplete_cost_runs']])+'</tr>'
    page+='</table><h2>Full report</h2><pre>'+html.escape('\n'.join(lines))+'</pre>'
    (campaign/'report.html').write_text(page,encoding='utf-8')
    return report
