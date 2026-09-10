"""Local document service with explicit service-layer authorization."""
from dataclasses import dataclass

class AccessDenied(PermissionError):
    pass

@dataclass(frozen=True)
class Context:
    user: str
    workspace: str

class Service:
    def __init__(self):
        self.documents = {}
        self.memberships = {}

    def add_document(self, doc_id, workspace, text):
        self.documents[doc_id] = {'id':doc_id, 'workspace':workspace, 'text':text}

    def set_member(self, user, workspace, role):
        self.memberships[(user, workspace)] = role

    def _authorize(self, ctx, operation):
        role = self.memberships.get((ctx.user, ctx.workspace))
        if role is True:
            role = 'owner'
        allowed = {'viewer': {'read'}, 'editor': {'read','update'},
                   'owner': {'read','update','delete'}}
        if not isinstance(role, str) or operation not in allowed.get(role, set()):
            raise AccessDenied('not permitted')

    def _document(self, ctx, doc_id):
        self._authorize(ctx, 'read')
        doc = self.documents.get(doc_id)
        if doc is None or doc['workspace'] != ctx.workspace:
            raise AccessDenied('document unavailable')
        return doc

    def read(self, ctx, doc_id):
        return dict(self._document(ctx, doc_id))

    def update(self, ctx, doc_id, text):
        self._authorize(ctx, 'update')
        if not isinstance(text, str):
            raise ValueError('text must be a string')
        doc = self._document(ctx, doc_id)
        doc['text'] = text
        return dict(doc)

    def delete(self, ctx, doc_id):
        self._authorize(ctx, 'delete')
        self._document(ctx, doc_id)
        del self.documents[doc_id]

    def bulk_update(self, ctx, updates):
        self._authorize(ctx, 'update')
        if not isinstance(updates, list):
            raise ValueError('updates must be a list')
        seen = set()
        for pair in updates:
            if not isinstance(pair, (list,tuple)) or len(pair) != 2:
                raise ValueError('expected id/text pairs')
            doc_id, text = pair
            if not isinstance(doc_id, str) or not isinstance(text, str) or doc_id in seen:
                raise ValueError('invalid or duplicate update')
            seen.add(doc_id)
            self._document(ctx, doc_id)
        return [self.update(ctx, doc_id, text) for doc_id, text in updates]

    def export(self, ctx, doc_ids):
        self._authorize(ctx, 'read')
        return [self.read(ctx, doc_id) for doc_id in doc_ids]
