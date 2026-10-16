# Log of research-influenced decisions

When to read it: when building the log, reviewing it with the team, or explaining to leadership what happened to the recommendations.

## What it is for
It turns "we did a study" into "the study influenced these decisions". It is also the memory of why something was rejected, so it is not re-argued and the study is not repeated.

## Fields (match the CSV columns)
| Field | What to write |
|---|---|
| date | When the recommendation was made (YYYY-MM-DD) |
| finding | The finding in one sentence, with a link to the report |
| recommendation | What is requested |
| decision | What was decided and who said so; if rejected, the reason |
| owner | Person who decides or executes (name or role, just one) |
| status | accepted, backlog, implemented, rejected or pending |
| metric | Which metric is expected to move |
| result | What was observed afterwards (or "no data"), with the attribution caveat |

The script also accepts the Spanish column names (fecha, hallazgo, recomendacion, decision, responsable, estado, metrica, resultado) and Spanish status values (aceptada, en backlog, implementada, rechazada, pendiente).

## Questions per recommendation
1. Who decides? (not "the team": a person or a specific forum).
2. Which decision is requested, in one sentence?
3. By when? What happens if it is delayed? (for example, it makes the sprint or the window is lost).
4. What is the status today and why?
5. Which metric would say whether it worked?

## Statuses
- **Pending:** nobody has decided. This is the status to watch: after a few weeks without movement, escalate to the right forum.
- **Accepted:** there is commitment, not yet built.
- **Backlog:** acknowledged, no date. Note the criterion to raise its priority.
- **Rejected:** with a reason (cost, legal, other priority, disagreement with the evidence). A rejection for "I do not trust the evidence" is a signal to review quality (ux-insight-qa).
- **Implemented:** move to measuring; fill in `result` when there is data.

## Cadence
A short review (15 min) every 2 to 4 weeks with product, and a quarterly synthesis for leadership. These frequencies are our own heuristic; adjust them to the delivery cycle. In each review: what moved to "implemented"?, what has been "pending" too long?, what is still unmeasured?

## What it looks like for leadership
A table with date, finding, decision, owner, status, metric and result, plus three numbers: how many recommendations were logged, how many were implemented and how many remain pending. The script `scripts/decision_log.py` generates it and warns about rows without owner, metric or date.

## Common mistakes
- Logging only the successes: the log loses credibility.
- Counting "accepted" as impact: impact happens when it is implemented and measured.
- A single status column with no reason.
- Attributing to the research decisions that were already made: note whether the research confirmed, changed or accelerated the decision.
