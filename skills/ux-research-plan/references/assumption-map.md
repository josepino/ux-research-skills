# Assumption map

**When to read it**: there is an idea, solution or feature and the team "takes things for granted". It helps decide what to test first and with which cheap method.

## 1. List assumptions
Ask the team to complete "For this to work, it must be true that..." and write one sentence per assumption. Walking through the user journey step by step helps: at each step, what must be true?

## 2. Classify by category
| Category | Question | Example |
|---|---|---|
| **Desirability** | Do people want it? Do they have the problem? | "Managers want automatic weekly reports" |
| **Usability** | Will they be able to use it? | "They find the filter without help" |
| **Feasibility** | Can we build and sustain it? | "The vendor's API delivers real-time data" |
| **Business** | Is it profitable and does it fit the strategy? | "10% move to the paid plan" (example figure; use yours) |

Torres (Product Talk) uses five categories: desirable, viable, feasible, usable and ethical. If the case touches personal data, add "ethics" as its own category.

## 3. Separate what is known from what is believed
For each assumption ask "how do we know?": observed data (study, analytics) = **known**; opinion, anecdote or "it has always been like this" = **believed**. Note the source. An assumption with old evidence or evidence from another segment counts as "believed".

## 4. 2x2 matrix: risk x evidence
- Vertical axis: **risk** (if the assumption is false, how much does the idea break?).
- Horizontal axis: **evidence** (little -> a lot).

| | Little evidence | A lot of evidence |
|---|---|---|
| **High risk** | **Test first** | Monitor |
| **Low risk** | Test if cheap | Ignore for now |

## 5. Turn each priority assumption into a hypothesis
"We believe that [assumption] for [users]. We will know when [measurable signal] [threshold]." Define the threshold before seeing data and which decision is taken if it fails. Example: "We believe managers open the weekly report. We will know when at least 6 of 10 open it two weeks in a row in a prototype with real data" (example threshold, adjust to your context).

Choose the cheapest method that can refute it: past-behavior interview, prototype, one-question survey, existing data. Result: table assumption - category - known/believed - risk - hypothesis - signal - method.
