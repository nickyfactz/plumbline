"""The CLI prints exactly one JSON job record on success."""
import argparse
import json
from jobs import Store

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('database')
    parser.add_argument('action', choices=['submit', 'start', 'complete', 'fail', 'get', 'cancel', 'ack-cancel', 'retry'])
    parser.add_argument('job_id')
    parser.add_argument('--request-id')
    args = parser.parse_args(argv)
    if args.action == 'retry' and not args.request_id:
        parser.error('retry requires --request-id')
    store = Store(args.database)
    try:
        method = getattr(store, args.action.replace('-', '_'))
        result = method(args.job_id, args.request_id) if args.action == 'retry' else method(args.job_id)
        print(json.dumps(result, sort_keys=True))
    finally:
        store.close()

if __name__ == '__main__':
    main()
