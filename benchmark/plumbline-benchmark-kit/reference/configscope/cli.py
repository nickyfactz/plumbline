import argparse
import json
from config import load

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('path')
    p.add_argument('--show-origin', action='store_true')
    a = p.parse_args(argv)
    print(json.dumps(load(a.path, with_origin=a.show_origin), sort_keys=True))

if __name__ == '__main__':
    main()
