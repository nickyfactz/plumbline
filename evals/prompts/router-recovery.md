# Router recovery prompts

Use a fresh disposable project and session for each case. Keep the plugin and
router in their native locations. These are host/model behavior checks, separate
from the offline resolver and installer tests.

1. Initialized router: approve router-only initialization, then start a fresh
   session and ask, "Explain this repository's purpose." Expect automatic router
   entry and the proportional front-door route without a setup loop or team.
2. Catalog omission: keep the installed plugin and local router, expose only its
   engine skill paths in the test session, and use the same ordinary prompt.
   Expect the AGENTS pointer to read the router, one validated installed-file
   fallback announcement, and the real front-door instructions.
3. Local managed worktree: commit the reviewed AGENTS/ignore/include files after
   router-only setup, create a native local managed worktree, and use the same
   prompt. Expect the ignored router to be present and route successfully.
4. Missing or ambiguous plugin: expose no active Plumbline capabilities, or
   conflicting active installation paths, while retaining the local router.
   Expect an actionable routing blocker before implementation; old cache files
   cannot satisfy active installation identity.
5. Deactivation: remove the local router while retaining AGENTS guidance and
   start a fresh session. Expect ordinary work, no router reconstruction, and no
   automatic Plumbline lifecycle ownership.
6. Explicit override: with an initialized router, ask, "Do not use Plumbline for
   this request; explain the README." Expect the override to be honored.
7. Manual/remote checkout: start from a checkout with the tracked setup guidance
   but no local router. Explicit router initialization restores setup without
   recreating the team or changing its profiles. No local host copy is assumed.
