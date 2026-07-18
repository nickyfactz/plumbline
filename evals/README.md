# Plumbline eval fixtures

These fixtures exercise the consent boundary and phase classification without requiring a real application. They are prompts and expected outcomes, not a replacement for Codex app UAT.

- `fixtures/uninitialized-repo/` demonstrates an ordinary repository with no local router.
- `fixtures/initialized-repo/` contains only the generated router boundary.
- `prompts/` contains small scenario inputs.
- `expected/` describes the allowed outcome and forbidden side effects.
- `prompts/resume-and-ownership.md` and its expected file cover evidence reuse, source drift, stale local integration, controller ownership, and delegation reporting.
