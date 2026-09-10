# Repeat and compare

For a later Plumbline or Codex release, create a **new campaign**, retaining the same fixture and grader bytes. Leave old reports and dated pricing snapshots intact. Record the old/new Codex build, plugin revision, root IDs, worker profiles, hook hash, permissions, pricing basis, and limits.

Run all 24 cells for a broad host/plugin comparison, or all three tasks on a selected tier with three fresh repetitions (18 attempts) for an economical variance check. Separate new model comparisons from worker-profile tuning. A profile or hook change is a changed treatment, not a pure orchestrator comparison.

Commands:

```text
python bench.py prepare --preset full --models terra --repeat 3
python bench.py run --max-runs 2
python bench.py run
```

Budget boundaries may still stop that campaign early. Never increase limits merely because a preferred workflow has not yet passed.

The controller can compare `report.json` and `scorecards.csv` from two campaign paths without calling another model. Join on task, root ID, arm, and repeat. Confirm fixture/grader compatibility first. Report both matched transitions (PASS→FAIL, FAIL→PASS) and cost/time differences, with the changed host/plugin/profile dimensions stated. Do not pool historical and new runs as though they were concurrent randomized trials.

One fresh observation per cell is smoke evidence. More repeats show variability but three tasks still do not support claims of universal superiority. Repeat both arms rather than selectively retrying only surprising losses. There are no implementation retries in the scored protocol; new repeats start from the same unfinished baseline.

A campaign interrupted for a host problem is not repaired in place by changing the frozen runner. Keep that record, repair the adapter, and make a new campaign. An ordinary pause between completed runs may continue the same campaign safely. `run` skips finalized cells; it does not restart them. `recover` records interrupted attempts and never resumes their candidate conversation.

No-Ponytail or forced-single studies are explicitly distinct series. Keep their labels visible in any aggregate chart.
