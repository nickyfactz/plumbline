# CS-1: scoped configuration with provenance

Extend this local reader, not a service or framework. Standard library only.
`DEFAULTS` and the existing public function names remain.

## Acceptance contract
C01. Continue accepting legacy flat objects such as {"timeout": 9}. New scoped
objects may contain ONLY `global`, `workspace`, `project`, each an object. Presence
of any scope name selects scoped mode; mixing a scope name with a flat key is invalid.
C02. Effective precedence is defaults < global < workspace < project. Missing keys
inherit. Explicit JSON null (Python None) clears a value and stops inheritance.
C03. Extend `resolve(document, *, with_origin=False)` and `load(path, *, with_origin=False)`.
Default return is still a flat value dictionary. With origin enabled, return exactly
{"values": <flat dict>, "origins": <key-to-scope dict>}. Origins are `default`, `global`,
`workspace`, or `project`; legacy flat values have origin global. Null keeps its scope.
C04. Every scope and key is validated, including values shadowed by a later scope.
Unknown keys/scopes, non-object scopes, mixed mode, invalid theme, negative/non-int
numeric values, and bool-as-number raise ValueError. None is allowed for any known key.
C05. `validate(document)` now accepts either document format and follows C04; it
returns None on valid input. Empty documents and empty scopes are valid.
C06. Resolve/validate must not mutate caller data or DEFAULTS. Every result is independent;
mutating a returned values/origins dictionary cannot affect later calls.
C07. `dump(document, path)` validates then serializes the ORIGINAL structure and explicit
nulls, not effective values. Invalid input must leave an existing destination unchanged.
Whitespace/order are not graded. No new format/version envelope is permitted.
C08. `load` and dump round-trip both formats, including Unicode. Invalid JSON raises
ValueError (JSONDecodeError qualifies). Missing files keep FileNotFoundError.
C09. CLI adds `--show-origin`, emitting the C03 object as a single JSON line.
Without the flag, output is unchanged. Flags can occur before or after the input path.
C10. Add focused tests and preserve the existing regression suite and standard-library-only footprint.

No nested merging, environment variables, remote sources, schema library, or cache is required.
