# Personas

When to read: when building, choosing, sizing or maintaining personas.

## Contents
1. What it is and what it is not
2. Types and which to choose
3. Step-by-step process
4. How many personas and how many interviews (sources disagree)
5. What to include and what to leave out
6. Concrete uses
7. Maintenance and review
8. Risks and alternatives
9. Guiding questions for interviews

## 1. What it is and what it is not
- A fictional but realistic description of a typical user, **built from patterns in real data from several people** (not from a known customer or from imagination). It exploits the fact that people remember a concrete case better than a range of numbers.
- Main function: memorability and a shared vocabulary. In a meeting, the persona's name summarizes a set of goals and behaviors.
- **UX persona** (end users: what they need to achieve using the product) vs **marketing/buyer persona** (who decides the purchase: what they need to hear in order to buy). They may not coincide (the manager who approves the license vs the designer who uses it). An agency that uses both observed another practical difference: the UX persona is always evolving, while the marketing one is often fixed for a period (e.g. a year). Neither replaces the other.
- **Archetype** (a universal motivation pattern, based on psychology/narrative) is not a persona (detailed and specific to a segment). Archetypes serve long-term strategy; personas serve design decisions.
- A persona does NOT replace research: it is one of its end results, not the first step.
- **UX vs marketing nuance (Justinmind, 2018, summary)**: the marketing persona represents who *buys* (buying is not using) and focuses on demographics, goals and challenges, fears, values and buying habits; the UX one represents who *uses* and is built with field research. Example: a company making educational devices for children can have a marketing persona for the parents who buy and a UX persona for the child user (and also for the parents). Caution: that page cites marketing impact figures (sales percentages, traffic gains, ROI) whose origin cannot be verified in the summary; **do not use them as evidence** that personas "work".
- **Archetype vs stereotype** (Hosn, 2020): the archetype comes from meaningful behavior patterns; the stereotype from generalizations with no factual basis.

## 2. Types and which to choose
| Type | Basis | When to use | Risk |
|---|---|---|---|
| **Proto-persona** | The team's prior knowledge and assumptions (workshop, no new research) | Little time/resources; externalize assumptions; starting point for a research plan. Better than having none | Without real data: always label as a hypothesis and do not use it for big decisions |
| **Validated-lite** | Interviews only, n < 10 | Small research-based persona; state n and the limit in the header | Do not call it Validated; a persona name is a fictional label, say so |
| **Qualitative** | Interviews/observation, small or medium sample | Default case; does not take much time | Less generalizable |
| **Statistical / mixed** | Qual + quant with a large sample | Established product, need to size segments | Cost and maintenance |

Perspectives (Lene Nielsen, via IxDF): **goal-directed** (what the typical user wants to do and their preferred flow), **role-based** (the role in the organization matters; qual+quant data), **engaging** (uses stories and scenarios so the team feels it is real and uses it) and **fictional** (comes from the team's experience, not research; recognized as weak). Her "engaging" process has 10 steps that start with collecting data, forming a hypothesis about differences between users and getting the whole team to accept or reject it; they group into four parts: data, descriptions, scenarios (to analyze problems and ideate) and organizational acceptance. It is an ideal process: you do not need to complete all 10 in every project.

Useful historical frame: Alan Cooper's goal-directed design (1999) puts personas in the early stages (research, modeling, requirements) as the foundation for later decisions.

## 3. Step-by-step process (data-based)
1. **Define the purpose**: which decisions it will support (roadmap, onboarding, aligning teams). Check whether there is reusable data.
2. **Research**: interviews, surveys, field studies, longitudinal studies (NN/g); analytics and support as a complement (analytics says *what* they do, not *why*). Ideally 3 or more different sources (reports/competition, surveys, interviews; Pixel Research Lab). If you cannot talk to users, interview those who serve them (sales, support, customer success) and label it.
3. **Build a visible summary** of each interview (e.g. a spreadsheet with background, pains, motivations, the most relevant highlighted). It makes segments easier to see.
4. **Group** by behaviors, goals and context; merge similar clusters and drop the irrelevant ones. Compare clusters with each other: if two ask the same of the design, they are one persona; if one is too broad, split it.
5. **Write each persona with the same template** (so they can be told apart). A compact template proposed by UX studio uses four factors: **prior knowledge** (what they know about the product or category), **context** (where, when, how much time they have), **problem** (something tangible) and **motivation** (the deeper reason).
6. **Build them as a team**: people who take part believe, use and promote them more (NN/g). Ideally they observe sessions or watch videos.
7. **Validate**: contrast with stakeholders and, if you started from proto-personas, with real interviews. Do not stop at the impression-based prototype.
8. **Share and use** (section 6) and **schedule the review** (section 7).

## 4. How many personas and how many interviews (sources disagree)
There is no single number. Give the user the range and let them decide for their product.

| Source | Number of personas | Interviews |
|---|---|---|
| UX studio | 3 to 5 (fewer than 3 is shallow; more than 5, rethink segmentation) | At least 10 interviews |
| PlaybookUX | 1 or 2 | 5 users per persona type (e.g. 2 personas = 10 users) |
| Pixel Research Lab | MVP: 1 persona covering ~80% of the potential audience; established product: up to 3 | Triangulate at least 3 sources |
| UXPressia | depends on role | 5 to 30 per role; trends appear from about 5 interviews; stop when nothing new comes up |
| UXPin and Crystallize | 3 to 5 | n/a |
| Uxcel | 3 to 7 depending on real variation | n/a |

Practical criterion: **fewer personas than the team can remember**; merge groups with the same goals and drop small or peripheral segments. If there is more than one, define a **primary** and treat the rest as secondary. For "number of interviews" use saturation (no new themes appear) instead of a magic number.

## 5. What to include and what to leave out
**Include** (each element with a reason): name and realistic photo (not celebrities or unrealistic drawings; they help recall), a representative phrase or quote (not too witty: a "funny" persona loses seriousness), experience with the product or category, **context of use** (by choice or work obligation, frequency, device), goals and concerns when doing the tasks (speed, accuracy, completeness), frustrations, motivations, typical scenario, evidence base and date. In enterprise settings, add the role and the **decision makers/influencers in the buying process**, who may have different priorities from end users; integrations and compatibility also matter.

**Minimum fields of a basic persona** (Hosn, summary): goals (end result), motivations (the why, e.g. trusting the result will be good), frustrations, demographics only if relevant (age, place, gender; ethnicity, family or income only if they matter and with care), devices and a fictional name to refer to it. Add a **scenario**: if the persona is not trying to accomplish a task, the team does not know how to help (Kim Goodwin, via Roman).

**Leave out**: any data that does not change a decision. Illustrative example: favorite wine is useful in a forum for sommeliers, not in an intranet. Irrelevant details (a) compete for attention and (b) cost credibility: if the team sees something absurd, they distrust the rest. Do not invent details to "fill in" a thin template: that is the persona's imagination risk.

**Typical mistakes of weak personas** (Roman, 2019, summary): (1) they do not go beyond demographics; "millennial" only triggers the reader's stereotypes. Ignore demographics unless statistically relevant and tied to behaviors or feelings. (2) Half an hour is spent debating where the persona eats and little on what matters (what they think, feel, try to do and what stops them); brand logos invite irrelevant judgments. (3) **Invented quotes**: real ones are usually the strongest data and fake ones ("what I need is exactly what you sell") show. (4) Stock photos that cost credibility. (5) No scenario. (6) No research with people was done: then a persona should not be used to represent data.
- **Contradiction to keep in mind**: above, a realistic photo is recommended for memorability; Roman prefers **no photo over a stock one**, and Rohaise (2024) proposes removing photos of real people in abstract versions. Criterion: photo only if it is plausible and does not introduce bias; otherwise a neutral illustration or nothing.

## 6. Concrete uses
- Decide and prioritize ("which option serves Marta better?"); break ties in design discussions.
- Write concrete test scenarios ("Helen looks for organic eggs and adds them to her list" instead of "test the search").
- **Recruit**: the persona's attributes are screening criteria for usability studies.
- **Segment analytics**: measure how each persona behaves; if a segment does not behave as the persona predicts, the persona needs review; if a lot of traffic fits none, one may be missing.
- Expert reviews (what each persona would do in this task), without replacing user testing.
- Briefing agencies or consultants.
- Feed empathy maps and journey maps (a persona = the journey's actor).

## 7. Maintenance and review
A persona is a snapshot in time. Signs to review (NN/g 2016):
- **The business or technology changed** (pivot, new products, competitor changes that alter expectations).
- **The user base changed**: demographic composition, new or vanished segments; segmented analytics that does not match the persona; test users who do not resemble it; new themes in support.
- If you detect a mismatch, research before rewriting: it may be a design problem and not a persona problem.

Frequency observed in an NN/g survey of 156 professionals: 46% update every 1 to 4 years, 28% quarterly or more often, 26% every 5 years or never. Satisfaction with impact (scale 1 to 7): 5.5 with quarterly or more frequent review; 4.5 with review every 1 to 4 years; 3.9 with 5 years or never. The difference of the most frequent group from the others was statistically significant; the difference between the last two was not. It is **self-perception by professionals**, not causal proof. If you review often, communicate what changed and why, and remove old copies. Depending on the change: minor adjustment, refresh, or retire and replace.

## 8. Risks and alternatives
Cited risks: misleading fiction without data; an illusion of complete understanding and an excuse to stop researching; using them to decide when research was needed; stereotypes; maintenance cost; stakeholders who value only quantitative data. One author notes that much of the value lies in the **process of creating them** (hence involving the team) and that whoever uses them without having taken part fills gaps with their own biases.
Not every initiative needs personas: assess complexity, innovation potential and return. Alternatives or complements: **Jobs To Be Done** (motivation and problem instead of a character), **actors/roles** (in organizational systems), proto-personas and empathy maps.

### Inclusion and bias in personas (Rohaise, 2024, summary; one practitioner's opinion)
- Condensing a user base into one individual with a biography can **flatten diversity**, especially if done early. The warning: many default personas are young employees (25 to 40), so age-related needs (e.g. lower visual acuity) and accessibility are considered late, as a patch.
- Diversifying only the photo (changing ethnicity or gender) does not change the needs represented; you have to vary **needs and contexts**, not appearance.
- Non-essential details (brands, hobbies, family structure) plus fake quotes and stock photos weaken credibility and can exclude.
- Proposed alternatives: **Jobs To Be Done** (goals shared across diverse users, with functional, emotional and social dimensions; allows contradictory emotions that a persona cannot hold; in one case the solution met the personal and social needs and failed only on the functional one, a nuance the persona would not have shown), **empathy map**, **spectrum analysis** (compare ranges of characteristics without a fixed profile) and, if personas are insisted on, **abstract versions or archetypes** without prescribed family dynamics, invented personal data or real photos.
- Note: this is consistent with this skill's rule to segment by behavior; it does not mean every persona is harmful, but that how it is built matters. See also Roman 2019: the problem is doing it by inertia, not the tool.

## 9. Guiding questions for persona interviews
- Context: who are they? role, responsibilities, tools they use today to do their work and why those no longer suffice.
- Goal and obstacle: what are they trying to achieve? what is the main barrier? how do they define success?
- Recent behavior: ask them to tell about the last time they did it (a concrete story, not general opinions).
- Attitudes: what distrust or concern do they have (e.g. data protection), which brands or references do they use for that task.
- Hosn suggests that "why" questions give the best results (they reach what moves the person), and validating qualitative findings with a **survey** of more people, which confirms or discards hypotheses from the interviews. This matches the rule of starting with about 5 interviews and continuing until patterns appear.
- Prefer open questions that elicit stories over closed ones aimed at quantitative data.
