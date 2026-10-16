# Metrics, outcome vs output and honest attribution

When to read it: when defining which metric a finding moves, writing research objectives, or reporting impact.

## Finding -> business metric map
Do it **before researching** and look at it again when prioritizing findings. For each study question:

| If the finding is about... | Candidate business metric | Leading indicator (fast) | Lagging indicator (slow) |
|---|---|---|---|
| Discovery/purchase | Conversion, revenue | Success rate on the purchase task in tests | Funnel conversion |
| Onboarding | Activation | Time to first action, errors in the step | 30-day retention |
| Recurring use | Retention, engagement | Use of the feature in the first weeks | Churn |
| Confusion/help | Support cost | Queries per topic in the first weeks | Total tickets per user |
| Rework | Development cost | Late changes avoided | Rework hours per delivery |
| Satisfaction | Loyalty | SEQ/UMUX-Lite after the change | NPS or another relationship measure |

The metric examples are a generic guide (our own heuristic); use the ones your company already measures. If something is not measured, say so: defining how to measure it is already a result. Also think about the cost of not acting (users who leave, support, rework).

## Leading vs lagging
- **Leading:** changes soon and gives warning. Example: task success in a test with the prototype. Useful for deciding fast, but it predicts, it does not prove.
- **Lagging:** the business outcome. It takes time and is influenced by many things.
Define both and the date when you will look at each.

## Outcome vs output
- **Output:** studies done, reports, sessions. Measures activity.
- **Outcome:** decisions changed, errors avoided, metrics moved. Measures value.
Reporting only output makes research look like a deliverables service; reporting outcome requires the decision log.

### Research objectives and OKRs (outline)
- Objective: "That decisions in [area] are made with evidence from users."
- Possible key results (choose those you can measure): proportion of recommendations with a recorded decision within X weeks; proportion of the quarter's decisions with research evidence; change in a product metric associated with implemented recommendations; estimated rework savings (labeled "own estimate").
- Avoid "run N studies" as the only key result.
Target numbers come from your baseline, not from other people's benchmarks.

## Honest attribution
1. **Correlation is not causation.** If conversion rose after the change, so did everything else that happened that month: campaigns, seasonality, other changes.
2. **Prefer comparisons:** A/B test, gradual rollout, before/after with a group without the change. Without a comparison, write "associated with".
3. **Contribution, not exclusivity.** An improvement usually has several authors; say what the research contributed (identified the problem, changed the design, avoided a bad option).
4. **Declare what you do not know:** sample size, period, what other changes there were, what remains to be measured.
5. **Do not add up.** Summing the effects of several changes while attributing them all to research inflates the total.
6. **Famous cases (button, McAfee, etc.) are anecdotes from other companies**, not promises for yours (see `business-case.md`).
7. **Avoided value also counts**, but it is hypothetical: "we avoided building X" is labeled as an estimate and the assumption is explained.
8. The evidence behind the impact must be solid; if you doubt it, go through ux-insight-qa before claiming anything.
