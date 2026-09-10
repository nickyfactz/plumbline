# Fixture development

Python 3.11+; standard library only. Run `python -m unittest discover -s tests -v`.
The implementation-ready contract is `TASK.md`; current execution state is `PLAN.md`.
Preserve existing public signatures and behavior except where TASK.md explicitly changes it.
Keep work in this checkout. No network, new dependency, external service, or deployment is needed.
Do not inspect other benchmark runs, controller files, reference implementations, or external graders.
Do not change TASK.md or remove/weaken the existing tests. New tests belong under tests/.
Use your normal available workflow; there is no requirement to create a particular number of tests or files.
