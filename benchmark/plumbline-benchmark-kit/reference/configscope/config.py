"""Scoped configuration with explicit-null and provenance semantics."""
import json

DEFAULTS = {'timeout': 30, 'theme': 'light', 'retries': 2}
SCOPES = ('global', 'workspace', 'project')

def _validate_values(values):
    if not isinstance(values, dict):
        raise ValueError('scope must be an object')
    for key, value in values.items():
        if key not in DEFAULTS:
            raise ValueError('unknown key: ' + key)
        if value is None:
            continue
        if key == 'theme':
            if value not in ('light', 'dark'):
                raise ValueError('theme must be light or dark')
        elif type(value) is not int or value < 0:
            raise ValueError('numeric values must be non-negative integers')

def _layers(document):
    if not isinstance(document, dict):
        raise ValueError('configuration must be an object')
    if any(scope in document for scope in SCOPES):
        if set(document) - set(SCOPES):
            raise ValueError('unknown or mixed scope')
        return [(name, document[name]) for name in SCOPES if name in document]
    return [('global', document)]

def validate(document):
    for _, values in _layers(document):
        _validate_values(values)

def resolve(document, *, with_origin=False):
    validate(document)
    values = dict(DEFAULTS)
    origins = dict.fromkeys(DEFAULTS, 'default')
    for scope, layer in _layers(document):
        values.update(layer)
        origins.update(dict.fromkeys(layer, scope))
    return {'values':values, 'origins':origins} if with_origin else values

def load(path, *, with_origin=False):
    with open(path, encoding='utf-8') as f:
        return resolve(json.load(f), with_origin=with_origin)

def dump(document, path):
    validate(document)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(document, f, sort_keys=True, ensure_ascii=False)
