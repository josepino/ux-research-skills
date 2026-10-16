# Templates

When to read: when producing a deliverable. Templates are in English; translate headings and labels to the user's language when producing the deliverable.

Evidence convention: `[E1]`, `[E2]`... point to the source list in the header; `[Quote]` = verbatim text with the participant id, never a paraphrase (a paraphrase or a goal derived from a quote takes `[Inf][E#]`);  `[Obs]` = observed; `[Inf]` = inferred; `[ASSUMPTION—VALIDATE]` = unvalidated assumption (equivalent to the older `[Hypothesis]`; Spanish `[SUPUESTO—VALIDAR]`/`[Hipótesis]` also accepted); `[DATA]` = equivalent to a concrete source (see `proto-persona.md`). A note without a tag is not delivered.

## Contents
1. Persona (full)
2. Quick 4-factor persona
3. Proto-persona (hypothesis)
4. Empathy map (4 quadrants + pains/gains)
5. Empathy map for research planning (confidence 1-3)
6. Journey map
7. Experience map
8. Hypothesis map (workshop)
9. Mental model gaps
10. Short completed example (journey)
11. Traceability table

## 1. Persona (full)
```markdown
# [Fictional name] - [archetype in 3-5 words]
Status: Validated | Proto-persona (hypothesis) · Date: YYYY-MM-DD · Version: v1 · Review before: ____
Evidence base: n=__ interviews, __ surveys, analytics __, support __ · Sources: [E1] ... [E3]
Photo: realistic, fitting the persona (no celebrities)

**Quote:** "..." [Quote]
**Design-relevant profile:** role/occupation · age/location only if it changes decisions · experience with [product/category]
**Context of use:** by choice or work obligation · frequency · device(s) · where and when · how much time they have
**Goals and tasks:** 1... 2...  (what success means)
**Behaviors:** ... [Obs]
**Frustrations / concerns:** ... (speed, accuracy, trust...)
**Motivations (the why):** ...
**Accessibility / assistive technologies (if applicable, as a usage attribute):** ...
**Typical scenario:** ...
**What we would do differently knowing this (design implications):** ...
**Derived recruiting criteria:** ...
**Segment in analytics:** how to identify them (event/property)
**Gaps:** what we do not know yet
```

## 2. Quick 4-factor persona
```markdown
# [Name] - [role]  (Status/Date/n)
| Prior knowledge | Context | Problem (tangible) | Motivation (deeper) |
|---|---|---|---|
| | | | |
```

## 3. Proto-persona (hypothesis)
```markdown
# [Name] (HYPOTHESIS - to be validated) · Date · Workshop participants: __
Who we think they are: ...
What we think they want to achieve / what hurts: ... [ASSUMPTION—VALIDATE]
How we validate it: 5 interviews with profile __ (criteria: __); recruiting source: __
Decisions it must NOT support yet: ...
Next research step: ... · What would make it validated: ...
```
Spanish equivalents when the user writes in Spanish: Brechas de información, Decisiones que habilita, Siguiente paso de investigación, Base de evidencia, Estado.
Full version and the rule for becoming validated: `proto-persona.md`.

## 4. Empathy map
```markdown
User/segment: ____ (1 map per persona) · Situation: ____ · Date/version: ____ · Status: Research-based (n=__) | Hypothesis
| SAYS (verbatim quotes) | THINKS (first person; include what they do not say and why) |
|---|---|
| "..." [Quote][E2] | ... [Inf] |
| DOES (observed; include assistive technologies) | FEELS (adjective: reason) |
| ... [Obs][E1] | Anxious: doesn't know if the payment went through [Inf] |
| PAINS (obstacles, risks) | GAINS (what success is) |
| | |
Contradictions between quadrants (to investigate): ...
Information gaps / next questions: ...
Themes (clusters): ...
```

## 5. Empathy map for research planning
```markdown
| Item | Quadrant | Confidence (1 low · 2 medium · 3 high) | Source |
|---|---|---|---|
| | | | |
What we do not know / what we are least sure about -> questions for the next study:
```

## 6. Journey map
```markdown
Actor (persona): ... · Scenario / goal: ... · Expectations: ...
Status: Current | Future · Base: Hypothesis | Research (n=__) · Fidelity: Low | High · Date/version
| | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|---|---|
| Actions (narrative) | | | | | |
| Thoughts / questions (quotes) | | | | | |
| Emotion (1 very negative - 5 very positive) + reason | | | | | |
| Touchpoints / channels | | | | | |
| Pains | | | | | |
| Moments of truth | | | | | |
| Opportunities | | | | | |
| Owner / metric | | | | | |
Evidence per phase: ...  ·  What we do differently: ...  ·  Gaps: ...
```
Opportunities table (ranked by impact, evidence per opportunity):
| # | Opportunity (How might we...?) | Phase | Evidence (n of N, method, source) | Impact | Effort | Owner |
|---|---|---|---|---|---|---|

Example phases (choose by case): e-commerce discover/try/buy/use/support; B2B purchase/adoption/retention/expansion/advocacy; big purchase engage/inform/research/evaluate/justify. Workshop to build it with the team: `journey-workshop-5-questions.md`.

## 7. Experience map
```markdown
Generic experience: "how people achieve ____" (no assumed product) · Base: ____ · Date
| Stages (verb in -ing form) | ... |
|---|---|
| Goals | |
| Behaviors | |
| Feelings + / - | |
| Opportunities / unmet needs | |
Beliefs (outside the flow): ...
```

## 8. Hypothesis map (workshop)
```markdown
Team (5-6) · Stretch of the journey: ____
Orthodoxies (internal beliefs): ...
Hypothetical persona (name, age, profession, goal): ...
| Step/touchpoint | Interaction with the company | "I think" vs "I say" | Emotion | Moment of truth | Internal process/rule |
|---|---|---|---|---|---|
What we will ask customers to contrast: ...
(Do not show this map to customers during interviews.)
```

## 9. Mental model gaps
```markdown
| Concept / task | They expect (quote, n) | The product does | Gap | Evidence | Action (align / teach / stop distinguishing) | Priority |
|---|---|---|---|---|---|---|
```

## 10. Short completed example (illustrative, hypothesis)
```markdown
Actor: Marta, clinic administrator · Scenario: switching online scheduling provider · Status: Current · Base: Hypothesis (workshop)
| | Research | Try | Migrate | Use |
|---|---|---|---|---|
| Actions | Compares 3 sites [ASSUMPTION—VALIDATE] | Asks for a demo [ASSUMPTION—VALIDATE] | Exports appointments to a spreadsheet [ASSUMPTION—VALIDATE] | Enters appointments daily |
| Thoughts | "Will my data be lost?" | "Will my team use it?" | "I don't have time" | "Where is the report?" |
| Emotion (1-5) + reason | 3: curious | 4: enthusiastic | 2: fear of losing data | 3: neutral |
| Pains | Unclear pricing | | Manual import | Hidden report |
| Opportunity | Simple pricing table | | Guided importer | Shortcut to the report |
Validation plan: 6 interviews with administrators who migrated in the last 12 months.
```

## 11. Traceability table
```markdown
| ID | Claim in the artifact | Tag | Source(s) | Participants (n of N) | Method |
|---|---|---|---|---|---|
```
How to use it: `from-synthesis-to-persona-and-journey.md`.
