# Templates

When to read it: when drafting messages, summaries, OKRs or the retro. Replace what is in brackets. Translate headings and labels to the user's language when producing deliverables.

## Language by audience
| Audience | Cares about | How to open |
|---|---|---|
| Leadership | Risk, money, timing, strategy | "We avoided [risk] before investing [amount/time]; [X] still needs to be decided by [date]." |
| Product | Decisions, priorities, metrics | "Two changes move [metric]; I propose ordering the backlog like this." |
| Design | What to change and why | "Participants [observed behavior]; let's change [element]." |
| Engineering | Scope, acceptance criteria | "Criterion: [x]% of users complete [task] without help in the acceptance test." |
| Support/sales | Fewer queries, objections | "This should reduce queries about [topic]." |
Use each area's vocabulary; do not explain the method unless it changes how much to trust the result.

## One-page impact summary
1. Period and studies included.
2. Recommendations: logged / implemented / backlog / rejected / pending.
3. Influenced decisions (3 to 5, one line each): what was decided, by whom, observed effect and attribution caveat.
4. Metrics: leading indicators already seen; lagging ones still to be measured (with date).
5. What we do not know.
6. What we ask for (decision or resource) and by when.

## Follow-up message for a recommendation
"Hi [name]: in the [date] report we recommended [X] because [finding in one sentence]. We need to know whether you [accept / put in backlog / discard] it and, in any case, the reason, so we can record it. Can we go over it in [meeting/date]?"

## Cycle-closing retro (30 to 90 days)
- Which recommendations were implemented and what was observed?
- Which were not and why (cost, priority, evidence, legal)?
- Which decision was made better or faster thanks to the research?
- What surprised us about how decisions are made here?
- What do we change in the next study (questions, format, who participates, timing of the report)?
- Actions with owner and date.

## Research OKR (outline)
Objective: [decisions of area X with evidence from users].
KR1: [% of recommendations with a recorded decision within N weeks].
KR2: [% of the quarter's decisions with cited evidence].
KR3: [product metric associated with implemented recommendations, using "associated with"].
Baseline: [own data or "to be measured in the first month"].

## Log (CSV)
`python3 scripts/decision_log.py --template > log.csv` generates the headers. Invented examples in `assets/sample-log.csv` (English) and `assets/sample-log.es.csv` (Spanish).
