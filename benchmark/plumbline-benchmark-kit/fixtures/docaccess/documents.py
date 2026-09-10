"""Local document service. Context is constructed by trusted caller code."""
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
        """Trusted setup method, not a user-facing operation."""
        self.documents[doc_id] = {'id':doc_id, 'workspace':workspace, 'text':text}

    def set_member(self, user, workspace, role):
        """Trusted setup/admin seam. Legacy role True means owner."""
        self.memberships[(user, workspace)] = role

    def _document(self, ctx, doc_id):
        doc = self.documents.get(doc_id)
        if doc is None or doc['workspace'] != ctx.workspace:
            raise AccessDenied('document unavailable')
        if not self.memberships.get((ctx.user, ctx.workspace)):
            raise AccessDenied('membership required')
        return doc

    def read(self, ctx, doc_id):
        return dict(self._document(ctx, doc_id))

    def update(self, ctx, doc_id, text):
        doc = self._document(ctx, doc_id)
        doc['text'] = text
        return dict(doc)

    def delete(self, ctx, doc_id):
        self._document(ctx, doc_id)
        del self.documents[doc_id]

    def bulk_update(self, ctx, updates):
        return [self.update(ctx, doc_id, text) for doc_id, text in updates]

    def export(self, ctx, doc_ids):
        return [self.read(ctx, doc_id) for doc_id in doc_ids]
