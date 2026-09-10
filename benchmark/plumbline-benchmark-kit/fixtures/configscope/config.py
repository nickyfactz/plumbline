"""A global-only JSON configuration reader."""
import json

DEFAULTS = {'timeout': 30, 'theme': 'light', 'retries': 2}

def validate(values):
    if not isinstance(values, dict):
        raise ValueError('configuration must be an object')
    for key, value in values.items():
        if key not in DEFAULTS:
            raise ValueError('unknown key: ' + key)
        if key == 'theme':
            if value not in ('light', 'dark'):
                raise ValueError('theme must be light or dark')
        elif type(value) is not int or value < 0:
            raise ValueError('numeric values must be non-negative integers')

def resolve(document):
    validate(document)
    return {**DEFAULTS, **document}

def load(path):
    with open(path, encoding='utf-8') as f:
        return resolve(json.load(f))

def dump(document, path):
    validate(document)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(document, f, sort_keys=True)
