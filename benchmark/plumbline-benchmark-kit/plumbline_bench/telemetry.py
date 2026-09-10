"""Conservative session-local cost extraction; unknown coverage is never zero cost.

Input tokens include cached input. Reasoning output is a subset of billed output.
Cumulative token counters are differenced per thread, never summed as snapshots.
Raw stdout turn.completed is a ROOT-ONLY fallback, not a child-inclusive bill.
"""
from __future__ import annotations
import json
from pathlib import Path

TOKEN_FIELDS=('input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens')

def pricing_model(prices, model):
    aliases={'gpt-reserve':'gpt-5.6-luna'}
    aliases.update(prices.get('model_aliases',{}))
    return aliases.get(model,model)

def rows(path):
    try:
        with Path(path).open(encoding='utf-8',errors='replace') as f:
            for line in f:
                try:
                    value=json.loads(line)
                    if isinstance(value,dict): yield value
                except json.JSONDecodeError: continue
    except OSError: return

def counters(value):
    return {k:int(value.get(k,0) or 0) for k in TOKEN_FIELDS}

def find_values(obj,key):
    if isinstance(obj,dict):
        if key in obj: yield obj[key]
        for val in obj.values(): yield from find_values(val,key)
    elif isinstance(obj,list):
        for val in obj: yield from find_values(val,key)

def thread_log(path, prices):
    record={'id':None,'role':None,'parent_id':None,'model':None,'effort':None,
            'tokens':dict.fromkeys(TOKEN_FIELDS,0),'cost_estimate_usd':0.0,
            'cold_estimate_usd':0.0,'requests':[],'warnings':[], 'terminal':False}
    previous=dict.fromkeys(TOKEN_FIELDS,0)
    for event in rows(path):
        payload=event.get('payload') or {}
        if not isinstance(payload,dict): continue
        kind=event.get('type')
        if kind=='session_meta':
            record['id']=payload.get('id') or payload.get('session_id')
            record['parent_id']=next(find_values(payload,'parent_thread_id'),None)
            record['role']=payload.get('agent_role') or next(find_values(payload,'agent_type'),None)
            record['model']=payload.get('model') or record['model']
        if kind=='turn_context':
            record['model']=payload.get('model') or record['model']
            if payload.get('service_tier') not in (None,'default','standard'):
                record['warnings'].append('non-Standard service tier requires a matching price adapter')
            record['effort']=payload.get('effort') or payload.get('reasoning_effort') or record['effort']
        if payload.get('type') in ('task_complete','task_completed','turn_complete','turn_completed'):
            record['terminal']=True
        if payload.get('type')!='token_count': continue
        info=payload.get('info') or {}
        total=info.get('total_token_usage')
        if not isinstance(total,dict): continue
        if not all(k in total for k in ('input_tokens','cached_input_tokens','output_tokens')):
            record['warnings'].append('missing token fields: cannot assume zero cached/input/output usage')
        current=counters(total)
        if any(current[k]<previous[k] for k in TOKEN_FIELDS):
            record['warnings'].append('counter decreased: unsupported reset or inherited history')
            previous=current; continue
        delta={k:current[k]-previous[k] for k in TOKEN_FIELDS}; previous=current
        if not any(delta.values()): continue
        record['tokens']={k:record['tokens'][k]+delta[k] for k in TOKEN_FIELDS}
        last=info.get('last_token_usage') or {}
        input_size=last.get('input_tokens')
        # When the whole delta is small, every constituent request must also be small.
        threshold=prices.get('long_context_threshold',272000)
        if input_size is None and delta['input_tokens']<=threshold:
            input_size=delta['input_tokens']
        priced_model=pricing_model(prices,record['model'])
        request={'model':record['model'],'pricing_model':priced_model,'effort':record['effort'],**delta,
                 'input_context_tokens':input_size,'cache_write_tokens':last.get('cache_write_tokens')}
        record['requests'].append(request)
        rate=prices['models'].get(priced_model)
        if rate is None or input_size is None:
            record['warnings'].append('unknown model price or per-request context tier'); continue
        cached=delta['cached_input_tokens']; total_input=delta['input_tokens']
        if cached<0 or cached>total_input or delta['reasoning_output_tokens']>delta['output_tokens']:
            record['warnings'].append('inconsistent token fields'); continue
        long=input_size>threshold; ri=rate['input']*(2 if long else 1)
        rc=rate['cached_input']*(2 if long else 1); ro=rate['output']*(1.5 if long else 1)
        # This estimate uses the published input/cache-read/output rates, excludes
        # unobservable cache writes and hosted tools. It is NOT an invoice.
        record['cost_estimate_usd']+=((total_input-cached)*ri+cached*rc+delta['output_tokens']*ro)/1e6
        record['cold_estimate_usd']+=(total_input*ri+delta['output_tokens']*ro)/1e6
    return record

def collect(home, events, prices, root_model=None, *, finished=False):
    parsed={}; expected_children=set(); root_id=None; fallback=None; tool_events=0; spawn_calls=set()
    completed=False
    for e in rows(events):
        if e.get('type')=='thread.started': root_id=e.get('thread_id')
        if e.get('type')=='turn.completed': fallback=e.get('usage'); completed=True
        item=e.get('item') or {}
        if e.get('type')=='item.completed' and item.get('type') not in ('agent_message','reasoning'):
            tool_events+=1
        # Known child-identification fields; no speculative descendant counts from text.
        for key in ('receiver_thread_ids','child_thread_ids'):
            for value in find_values(e,key):
                if isinstance(value,list): expected_children.update(str(x) for x in value)
        for value in find_values(e,'child_thread_id'):
            if isinstance(value,str): expected_children.add(value)
    for folder in ('sessions','archived_sessions'):
        for path in (Path(home)/folder).rglob('*.jsonl'):
            for raw in rows(path):
                payload=raw.get('payload') or {}
                if isinstance(payload,dict) and payload.get('type')=='function_call' and payload.get('name') in ('spawn_agent','functions.spawn_agent'):
                    spawn_calls.add(payload.get('call_id') or str(path)+str(payload))
                if isinstance(payload,dict) and payload.get('type')=='function_call_output':
                    output=payload.get('output')
                    if isinstance(output,str):
                        try: output=json.loads(output)
                        except json.JSONDecodeError: output={}
                    if isinstance(output,dict) and isinstance(output.get('agent_id'),str):
                        expected_children.add(output['agent_id'])
            rec=thread_log(path,prices)
            if rec['id']:
                # A second copy of a rollout does not represent a second bill.
                old=parsed.get(rec['id'])
                if old is None or sum(rec['tokens'].values())>sum(old['tokens'].values()):
                    parsed[rec['id']]=rec
    warnings=[]
    if root_id not in parsed:
        warnings.append('root rollout unavailable; stdout fallback is not complete telemetry')
        if fallback:
            parsed['root-fallback']={'id':root_id or 'unknown','role':'root','parent_id':None,
                'model':root_model,'effort':'medium','tokens':counters(fallback),
                'cost_estimate_usd':None,'cold_estimate_usd':None,'requests':[],
                'warnings':['root-only cumulative stdout usage'],'terminal':completed}
    for ident, rec in parsed.items():
        if ident==root_id: rec['role']='root'; rec['terminal']=rec['terminal'] or completed
        if not rec['requests']: warnings.append(f'no priced request evidence for {ident}')
        warnings.extend(f'{ident}: {x}' for x in rec['warnings'])
        if finished and not rec['terminal']: warnings.append(f'no terminal receipt for {ident}')
    missing=expected_children-set(parsed)
    if missing: warnings.append('missing child rollouts: '+','.join(sorted(missing)))
    children=[x for x in parsed.values() if x['id']!=root_id and x['role']!='root']
    if len(spawn_calls)>len(children): warnings.append('spawn calls exceed observed child rollouts; failed spawns require explicit reconciliation')
    if children and any(not x['parent_id'] for x in children):
        warnings.append('child parent linkage missing')
    total={k:sum(x['tokens'][k] for x in parsed.values()) for k in TOKEN_FIELDS}
    known=sum(x['cost_estimate_usd'] or 0 for x in parsed.values())
    return {'coverage':'complete-observed' if parsed and not warnings else 'incomplete',
            'coverage_note':'Rollouts observed in a dedicated per-run home; not a provider billing reconciliation.',
            'root_thread_id':root_id,'threads':list(parsed.values()),'worker_count':len(children),
            'tokens':total,'tool_events':tool_events,'warnings':warnings,
            'observed_cost_estimate_usd':known if parsed else None,
            'cost_estimate_usd':known if parsed and not warnings else None,
            'cold_estimate_usd':sum(x['cold_estimate_usd'] or 0 for x in parsed.values()) if parsed and not warnings else None,
            'cost_basis':'Published Standard input/cache-read/output rates; cache-write and hosted-tool fees excluded; not actual account debit.',
            'cache_write_coverage':'not-established','actual_account_debit':None}
