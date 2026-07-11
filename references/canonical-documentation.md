# Canonical documentation

Repository documentation is discovered, not imposed. Find the project's routing guide, architecture docs, API/contracts, runbooks, user docs, and current-state ownership before adding anything. An established repository may use any structure.

At closeout, identify the exact docs affected by the new behavior. Update only canonical current-state documents; keep transient specs, plans, imported sources, and QA reports separate. A justified `no canonical change` is valid for internal or self-explanatory work.

If code and docs disagree, investigate which is current and why. Do not blindly overwrite the document or force code to match stale prose. Keep terminology consistent with the repository and point agents to canonical paths instead of copying mutable design into agent prompts.
