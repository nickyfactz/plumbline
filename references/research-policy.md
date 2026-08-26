# Research policy

## Route the question first

Research repository facts before asking factual questions. Inspect the nearest `AGENTS.md`, canonical docs, relevant code and tests, configuration, current Git state, and only the history that can distinguish the current behavior. Use the repository's terminology.

During Shape, classify each unresolved item before deciding whether to ask the user:

- **Repository fact:** inspect the local repository.
- **External capability or design question:** research the available landscape before asking the user to choose an option.
- **Product decision:** present the evidence and ask the user one material question.
- **Fog:** keep a vague or premature possibility parked until it can be stated precisely.

Do not make the user supply the option space for a capability request. If the request asks what could exist, how a product usually handles something, or which existing tools or patterns are viable, run a bounded external research pass first. Skip external research for small local work, settled designs, or requests whose outcome does not depend on outside facts.

## Source and evidence rules

Use external primary sources for current or version-specific behavior, standards, security guidance, and platform mechanics. Prefer official documentation, standards, or the source repository. Use reputable product or design sources for interaction patterns, and inspect package or project evidence for ecosystem options. Check maintenance, licensing, cost, and security implications when they could change the recommendation.

Record concise findings and evidence rather than transcripts. A useful research finding names the question, the finding, the source URL or repository/version, why it matters to the product decision, and any remaining uncertainty. Record retrieval dates or versions when freshness matters.

## Delegation and bounds

Delegate noisy read-heavy exploration to the matching project-local `researcher` when the repository has one and the brief is bounded. The researcher is report-only: it does not edit the repository, active specification, or plan; it does not run Git operations; and it never spawns children. Use one researcher by default and parallelize only independent questions after their boundaries are clear.

Ask for a compact decision packet: conclusion, exact paths/symbols or sources,
material constraints, residual uncertainty, and recommended next action. The
main thread verifies only facts needed for product judgment or integration; it
does not repeat the worker's broad search.

If no project-local researcher is available, the main thread performs the bounded research directly. Never select a personal or global agent as fallback.

Bound the search. Stop when the evidence is sufficient to formulate the next safe product question or choose the next safe action; do not build an exhaustive catalog. Record URLs, commits, commands, and observed results for facts that affect the plan. Do not turn research into permanent architecture copied into an agent or prompt; point to the canonical source instead.
