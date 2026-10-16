# Triangulation across methods

## Contents
1. What it is and when it is worth it · 2. Topic x method matrix · 3. How to reconcile · 4. A theme that appears in only one method · 5. Output template · 6. Mistakes

## 1. What it is and when it is worth it
Triangulating means using more than one source, metric or analyst so a conclusion does not depend on the weaknesses of a single method. NN/g (Whitenton, 2021) gives three variants: several methods on the same activity (quantitative, qualitative, expert review), several metrics (satisfaction, time, revenue) and several analysts (a second person reviews your themes). A typical pair: analytics shows many errors and support logs explain which ones; an interview reveals a surprising motivation and a survey measures how common it is. The more expensive or hard to reverse the decision (a full redesign), the more it justifies combining methods.

## 2. Topic x method matrix
One row per theme, one column per method. In each cell: how many participants (or which metric) back it and whether the evidence is **attitudinal** (what they say) or **behavioral** (what they do).

| Theme | Interviews (n=8) | Usability tests (n=6) | Survey (n=210) | Analytics | Reading |
|---|---|---|---|---|---|
| Surprise shipping cost | 5/8 mention it | 4/6 stall at step 3 | 41% cite it as a reason to abandon | drop at the payment step | Convergent: act |
| Hard-to-find filters | 3/8 | 5/6 cannot find them | not asked | low filter use | Behavior stronger than speech: investigate why they do not say it |
| Lack of trust in payment | 4/8 | 0/6 | 12% | - | Said but not observed: hypothesis to test |

(Example figures invented to illustrate the format; they are not real data.) With `scripts/analyze_notes.py` and a `method` column in the CSV you get a version of this matrix with distinct participants per cell.

## 3. How to reconcile when methods disagree
Questions, in order:
1. **Do they measure the same thing?** A survey measures stated opinion; a test measures behavior in a task; analytics measures behavior without context. Differing is not contradicting.
2. **Same population and moment?** Samples from different segments explain many differences; note profile and date of each source.
3. **Which is the what and which the why?** Let quantitative say how much and where, and qualitative say why. If the qualitative why cannot explain the quantitative data, a source is missing.
4. **Is there a known bias?** Social desirability in interviews, self-selection in surveys, guided tasks in tests (`ux-ethics-bias-review`).
5. **When behavior and speech differ, behavior rules for describing what happens**, and speech remains evidence of perception and expectations (perceived trust can be real even if it does not change the click).
6. If nothing resolves it, record the disagreement as an open finding and propose the minimum study that closes it. NN/g does not offer a procedure for conflicts between methods; this order is our heuristic.

## 4. A theme that appears in only one method
Do not discard it or promote it: label it.
- **Interviews only:** may be anecdote or social desirability. Contrast with a short survey or a test task.
- **Tests only:** may be an artifact of the task or prototype. Ask in the next round whether it happens unguided.
- **Analytics only:** a what without a why; find 5-6 sessions or recordings that explain it.
- **Survey only:** without context; cut it with an interview of those who answered at the extremes.
If the theme is severe (blocks a task), it rises in priority even with a single source. It is reported as a "single-source signal", not a pattern.

## 5. Output template
- **Research question** and the decision it informs.
- **Sources** with n, date and segment.
- **Topic x method matrix** and reading (convergent / partial / divergent / single source).
- **Convergent findings** (high confidence) -> insights and recommendations.
- **Divergences** with the most likely explanation and how it would be tested.
- **What cannot be concluded.**

## 6. Mistakes
- Adding participants from different methods as if they were one sample: report n per method.
- Using one method only to "confirm" the other: actively look for what contradicts it.
- Triangulating with sources that share the same bias (three surveys of the same panel).
- Presenting percentages from a small qualitative sample next to those from a large survey in the same column.

Before delivering the insights, run them through `ux-insight-qa`. If the input is usability tests, the dedicated analysis is in `ux-usability-testing`.
