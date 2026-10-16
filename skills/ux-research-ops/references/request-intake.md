# Research request intake

A short form prevents studies with no decision behind them, duplicates, and "I need this by Friday" requests with no context. It does not replace the plan: when a request moves forward, the plan is written with `ux-research-plan`; here you only decide whether it gets in, when, and with what priority.

## Form (6-8 fields)
1. **Who is asking** and their team.
2. **Decision** that will be made with the result and the **deadline** of that decision.
3. **What we already know / what already exists** (search the repository first so you do not repeat work).
4. **Question** you want answered, in one sentence.
5. **Whom** we would need to hear from (if you know).
6. **What would change** depending on the answer (if nothing changes, the study is not needed).
7. **Risk**: minors, health, sensitive data, irreversible decision? (if yes, do not delegate; see `democratization.md`).
8. **Observers** from the team willing to take part.

## Triage
| Outcome | When | What follows |
|---|---|---|
| Answer with what already exists | There is evidence in the repository | Send the link |
| Quick study | Narrow question, near decision | Short plan (`ux-research-plan`) |
| Big study | Strategic decision or high uncertainty | Full plan + method (`ux-method-selector`) |
| Delegate with guardrails | Low risk, trained person | `democratization.md` |
| Decline / postpone | No associated decision or no capacity | Explain why and propose an alternative |
Priority: imminent decision, risk of being wrong, reach of the impact and effort (our criterion; weigh it with the team).

## Log template
```markdown
| Date | Requester | Decision and date | Question | Triage outcome | Owner | Link to plan |
```
Keep it in `01-plans/` or in the team's ticket tool.
