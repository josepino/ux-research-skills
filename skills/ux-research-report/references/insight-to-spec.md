# From insight to specification

An insight that does not change what gets built remains a curiosity. This bridge turns insights into requests that design and engineering can pick up without reinterpreting them.

## Contents
1. "So what?" gate · 2. How Might We... · 3. Brief for design · 4. Ticket for engineering · 5. Observable acceptance criteria · 6. Example · 7. Mistakes

## 1. "So what?" gate (before specifying)
For each insight, answer in writing. If any answer is "I don't know", it does not move on to specification.
1. Which concrete decision does it change? (what gets done differently)
2. Who makes it, and by when?
3. What evidence supports it (X of N, methods, quotes) and what do we not know?
4. What happens if nothing is done? (risk)
An insight that fails the gate is not deleted: it goes to the "to investigate" list or the knowledge base. Review insights and quotes with `ux-insight-qa` before turning them into requests.

## 2. How Might We... (HMW)
Format: "How might we [achieve the user outcome] when [context/obstacle]?" Good questions are neither so broad that they give no direction ("improve checkout") nor so narrow that they already contain the solution ("add a green button"). Write 2-3 per insight, anchored in the need, not in a feature. They feed ideation with design; they are not yet a specification.

## 3. Brief for design
```
Insight: [one sentence, with evidence X of N]
User and context: [segment, moment in the journey]
Problem to solve (not the solution): [...]
How might we...? (2-3)
Known constraints: [technical, legal, brand]
How we will know it improved: [metric or observable behavior]
Material: [report, clips, journey]
```

## 4. Ticket for engineering
```
Change: [what, where]
Observed problem: [steps to reproduce, who, in what context]
Severity: blocks / hinders / annoys
Acceptance criteria (observable): see section 5
Out of scope: [...]
How it gets verified with users afterwards: [follow-up test, metric]
```

## 5. Observable acceptance criteria
They must be checkable by looking at the product or at a person using it, with no interpretation.
| Weak | Observable |
|---|---|
| "Checkout is clearer" | "On the payment screen, the total including shipping is visible without scrolling before the card is entered" |
| "Filters are easy to find" | "In a test with N people from the segment, most find the size filter unaided on the first task" (define N and what "most" means with the team) |
| "Better error message" | "The error names the field that failed and how to fix it; it uses no codes" |
If the improvement is measured with users, agree on the metric beforehand (success, time, SEQ) with `ux-usability-testing`. Do not invent numeric targets without a basis: if there is no baseline, the criterion is observable behavior or "improvement over the current measurement".

## 6. Example (fictional data)
Insight: "First-time buyers abandon when they only see the shipping cost on the last step (5 of 8 in interviews; 4 of 6 in the test)."
- Gate: changes the checkout priority; the PM decides before the next cycle; we do not know whether it happens on mobile.
- HMW: "How might we show the total cost from the cart so nobody is surprised at payment?"
- Criterion: "The cart shows the estimated shipping cost before the first payment step."
- Follow-up: repeat the task with 5-6 people and review the abandonment analytics at that step.

## 7. Mistakes
- Jumping from insight to solution without asking about the problem.
- Criteria such as "more intuitive".
- Sending engineering the whole report instead of the ticket.
- Promising numeric impact ("+25% conversion") without a basis.
