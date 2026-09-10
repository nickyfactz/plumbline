"""Thin local request adapter, deliberately without a web server."""
from documents import AccessDenied

def dispatch(service, ctx, action, body):
    try:
        if action == 'read': result = service.read(ctx, body['id'])
        elif action == 'update': result = service.update(ctx, body['id'], body['text'])
        elif action == 'delete': result = service.delete(ctx, body['id'])
        elif action == 'bulk': result = service.bulk_update(ctx, body['updates'])
        elif action == 'export': result = service.export(ctx, body['ids'])
        else: return {'status':400, 'error':'unknown action'}
        return {'status':200, 'result':result}
    except AccessDenied:
        return {'status':403, 'error':'forbidden'}
    except ValueError:
        return {'status':400, 'error':'invalid input'}
