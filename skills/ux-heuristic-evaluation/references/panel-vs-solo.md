# "Panel" mode vs "solo" mode (and a checklist for teams)

Read this when deciding how many evaluators to add, or when you will coordinate an evaluation with other people.

## When each mode fits
| | **Solo** (one person or Claude) | **Panel** (3-5 independent evaluators) |
|---|---|---|
| When | Small screen or flow, quick review before a design, no time or people | Large product, expensive decision, launch, or a team that needs convincing |
| Advantage | Fast and cheap; gives a first list and a hypothesis of what to test | Covers more problems (each person misses some); allows measuring agreement and discussing severities |
| Risk | Low coverage and the bias of a single view | Coordination cost; loses its value if evaluators contaminate each other |
| How to declare it | "Individual evaluation: limited coverage, add human evaluators if the decision matters" | Report the number of evaluators and the level of agreement |
Basis: NN/g recommends 3 to 5 independent evaluators (see `sources.md`). A finding seen by only one evaluator is not invalid: flag it for discussion.

## Checklist for running the panel with a team
Before
- [ ] Narrow scope in writing: product, critical task, user type, device.
- [ ] Same material for everyone (same prototype version or screenshots) and the same findings template.
- [ ] Everyone knows the 10 heuristics and the 0-4 severity scale (15 minutes of calibration with one example).
- [ ] Clear rules: evaluate alone, in two passes, without seeing others' notes.
During
- [ ] Each person delivers their CSV (columns of `consolidate_findings.py`: where, problem, heuristic, severity, recommendation).
- [ ] Nobody consults others until delivering.
After
- [ ] Consolidate with `python3 scripts/consolidate_findings.py eval_*.csv`.
- [ ] A 45-60 minute session to discuss differences of 2 or more severity points and findings seen by only one evaluator.
- [ ] Closing questions: where do we agree, what hurts the user most, what hurts the business most, what needs data, what do we do now and later.
- [ ] Final list with owner, severity and what to validate with users.
Timings (1-2 hours per evaluator) and closing questions come from NN/g; the rest of the checklist is our own practice.
