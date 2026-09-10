# DA-1: authorization completeness and atomic bulk changes

Harden this in-memory document service and its local request adapter. No authentication
server, database, migration framework, audit framework or network service is required.
Context is trusted input from the caller; body fields are untrusted. Tests invoke BOTH
service methods directly and the adapter. Existing trusted setup methods remain available.

## Acceptance contract
A01. Roles: viewer can read/export; editor additionally can update/bulk_update;
owner additionally can delete. Legacy membership value True is equivalent to owner.
False, None, missing membership, and unknown role values deny every operation.
A02. All five user-facing operations enforce membership AND operation permission at the
service boundary on every call. A role change/revocation takes effect immediately.
A03. Only documents in ctx.workspace are visible, including to owners of a different
workspace. Unknown and cross-workspace ids raise the same AccessDenied type.
A04. Bulk update validates the complete request and every authorization before mutating.
For any rejected batch (including a later invalid id), no document changes.
A05. Bulk input is a list of unique (id, text) pairs. Duplicate ids, malformed pairs,
non-string ids/text, or non-list batch input raise ValueError and change nothing.
Successful results preserve input order and contain independent record copies.
A06. Single update accepts string text (including empty and Unicode); invalid text
raises ValueError without mutation. Returned read/update/export/bulk records are copies.
A07. Export is all-or-nothing authorization, preserves requested id order, and never
returns cross-workspace records. Repeated ids are allowed for export.
A08. Empty bulk/export still check operation permission. Authorized empty calls return [].
No user-facing mutation changes document id or workspace.
A09. api.dispatch trusts ctx only; body fields named user/workspace/role cannot elevate
privileges. Map AccessDenied to {status:403,error:'forbidden'} and ValueError to
{status:400,error:'invalid input'}. Preserve existing success and unknown-action shapes.
A10. Preserve existing setup and public method signatures and existing tests. No new
runtime dependency. Add focused tests for alternate entry paths and partial failure.

For payloads that are BOTH malformed and unauthorized, either ValueError or AccessDenied
is acceptable; the no-mutation guarantee is mandatory. Direct dictionary mutation through
trusted setup attributes is outside scope. Thread safety is outside scope.
