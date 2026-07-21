# Uninitialized fixture

This repository has no `.agents/skills/plumbline-router/` directory. Ordinary prompts must not automatically enter Plumbline. An explicit `$plumbline` front-door invocation hands off to `$plumbline-init` for a read-only setup proposal; explicit phase skills may still be used without creating the router.
