# Metrics, sample and analysis

Read this when planning the sample and when analyzing results.

## 1. Qualitative vs quantitative
- **Qualitative** (discover problems): 5 participants per round is NN/g's recommendation; more people return few new problems. Better several small rounds and fixing in between. With several user groups that behave differently, about 3-5 per group. In very low-cost contexts, as few as 2 per study can be optimal according to NN/g.
- **Quantitative** (measure, benchmark, compare versions): NN/g recommends about 40 participants for a success rate at 95% confidence and a ±15% margin of error. At 90% confidence about 28 suffice (±15%) or about 15 (±20%). Always report the interval/margin. Above ±20% is of little use.
- **Why it matters**: with n=5, "80% success" is 4 of 5 and can be anything from much less to nearly 100%. Report counts ("4 of 5"), not percentages or averages with false precision.

## 2. Metrics per task
| Metric | How | Watch out |
|---|---|---|
| Task success | Completed / partial / failed, with a written criterion | Record whether the moderator helped |
| Time on task | Seconds from start to finish | Only on successful tasks; with small n use the median and show the values; not with full think-aloud if you want pure times |
| Errors | Count and type (slips vs mistakes) | Define beforehand what counts as an error |
| SEQ (Single Ease Question) | After each task: "Overall, how difficult or easy was the task to complete?", 7-point scale (1-7); in Spanish, an equivalent translation | Reference average about 5.5 according to MeasuringU (more than 400 tasks); it is a perception, it does not replace success |
| UMUX-Lite | 2 agree/disagree items: "the system's capabilities meet my requirements" and "the system is easy to use" | Measures perceived usefulness and ease; to convert it to the SUS scale you need a regression equation (see sources) |
| SUS | 10 items at the end of the session | A global questionnaire, not per task; do not change the wording or you lose comparability; with small n it is indicative. Construction and scoring: `ux-survey-builder` |

NASA-TLX (workload): not verified in this skill; do not use formulas from memory. Consult the official source before using it.

Choose few metrics tied to the decision. For a benchmark NN/g suggests focusing on about 5-10 main tasks and keeping the same method across measurements so they can be compared.

## 3. Record during sessions
Per participant and task: result, time, number of errors, help received, verbatim quotes, moments of doubt and SEQ. Use the observation sheet in `templates.md` and a code per participant (P1, P2…), not names.

## 4. Analysis
1. **Problem list**: describe each problem as an observation (what they did, what happened, on which screen), not as a solution or opinion. Merge duplicates.
2. **Problem x participant matrix**: mark who had each problem. You see what happens to 1 of 5 and what to 4 of 5.
3. **Severity 0-4** (NN/g scale): 0 not a problem · 1 cosmetic · 2 minor · 3 major (high priority) · 4 catastrophic (fix before release). Combine three factors: **frequency** (how many suffered it), **impact** (how hard it is to overcome) and **persistence** (whether they suffer it once or always). Have several evaluators rate it and discuss differences of 2 points or more. Market impact is assessed separately.
4. **Script**: `python3 -I scripts/problems_matrix.py data.csv` with columns `participant,problem,severity` (Spanish `participante,problema,severidad` also works); it returns, per problem, how many participants had it, the average severity and a suggested order. The severity each observer assigns is an input; the final decision is the team's.
5. **Finding with evidence**: problem, how many, severity, quote or datum, probable cause, recommendation. Separate **observation** (what happened) from **interpretation** (why) and from **recommendation**.
6. **What worked** also goes in the report.
7. **Going deeper**: with many sessions or rich qualitative data, use `ux-synthesis`. To check whether what you see is supported, go back to the recordings.

## 5. Limits to declare
n, participant profile, version tested (prototype vs product), whether the moderator helped, what was not tested, and that qualitative results are not generalized with percentages.
