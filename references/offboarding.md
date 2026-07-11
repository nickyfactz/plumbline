# Offboarding

The local router directory is Plumbline's only automatic repository activation boundary. Removing `.agents/skills/plumbline-router/` stops automatic routing.

Plugin uninstall removes the installed bundle, not files already created in a repository. Read-only offboarding should inventory the router, matching local ignore entries, Plumbline-owned project agents, active transient artifacts, canonical docs, and useful tests. With approval, remove only selected Plumbline-owned integration. Preserve canonical docs, accepted feature history, repository agents, and user tooling by default.

Do not create a state database, hidden cleanup script, or uninstall ceremony. If a user wants active specs/plans removed, route through accepted closeout so Git history and canonical truth remain coherent.
