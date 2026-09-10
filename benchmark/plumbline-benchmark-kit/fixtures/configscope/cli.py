import argparse
import json
from config import load

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('path')
    a = p.parse_args(argv)
    print(json.dumps(load(a.path), sort_keys=True))

if __name__ == '__main__':
    main()
