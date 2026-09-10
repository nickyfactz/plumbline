"""The CLI prints exactly one JSON job record on success."""
import argparse
import json
from jobs import Store

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('database')
    parser.add_argument('action', choices=['submit', 'start', 'complete', 'fail', 'get'])
    parser.add_argument('job_id')
    args = parser.parse_args(argv)
    store = Store(args.database)
    try:
        result = getattr(store, args.action)(args.job_id)
        print(json.dumps(result, sort_keys=True))
    finally:
        store.close()

if __name__ == '__main__':
    main()
