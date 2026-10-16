# Mental models

When to read: when users' expectations about how the system works may differ from how it really works, or when planning a mental-model study.

## Contents
1. What it is (and what it is not)
2. Properties that matter when designing
3. Canonical examples
4. How to elicit them (from light to advanced)
5. What to do with a gap
6. Procedure and output
7. Common mistakes

## 1. What it is (and what it is not)
- What the user **believes** (or thinks they know) about how the system works; with it they predict what will happen and plan their actions. It is based on beliefs, not facts: it can be incomplete or plainly wrong. The idea goes back to Kenneth Craik (1943): we carry in our heads a small-scale model of how the world works.
- Mind the use of the term: here it means the **user's belief about the system**, not the collection of "mental models" as thinking frameworks for decisions (that sense appears in some generic blogs and does not apply).
- It matters less that it be accurate than that it be **accurate enough for the user to reach their goal** (especially in B2B, where they do not need to understand the backend). It also changes how they interpret the system's feedback, and therefore their decisions.
- Different from Indi Young's **mental model diagram** (a diagram of the user's steps, considerations and reasoning when completing a task): that is a technique to document them.

## 2. Properties that matter when designing
- **Each user has their own**, according to prior experience. There are shared themes (e.g. whoever presses the pedestrian crossing button once vs several times, depending on whether they believe presses accumulate), and in a study with pilots novices had more diverse models than experts, who resembled each other more.
- **Designer-user gap**: the team knows its creation in detail and thinks it easy to understand; users have less developed models and make more errors. Never assume your model is the user's.
- **Jakob's Law**: users spend most of their time on other sites and expect yours to work the same way. Much of your product's mental model comes from other products.
- **They change with experience**: with good design or training they improve (a mentioned example: the Nest thermostat's success is partly attributed to its interface matching users' models).
- **Inertia**: what people know well stays, even if it does not help. A single misconception can ruin an entire session: the user misreads everything that happens and never questions their base assumption. An argument for being conservative and innovating only when the new is clearly superior. If you innovate, you also face the challenge that users barely read instructions.
- **Use inertia instead of fighting it**: skeuomorphism (physical metaphors such as folders, cart, doors or maps in kids' apps) helps form the right model.

## 3. Canonical examples
- **Shopping cart**: the buyer controls what goes into the cart, as in a physical store. Adding shipping insurance without permission that has to be noticed and unchecked violates the model and is a deceptive pattern (sneaking / pre-selection).
- **Back button**: an "undo" to the previous screen is expected. It breaks the model when it goes up the app hierarchy, or when with an overlay open it goes back two steps instead of closing it.
- **Search bar**: a single box that searches everything is expected. Several boxes on the same page (one for logistics and another for research) lead to using the wrong one and concluding there are no results.
- **Ambiguous mini-roundabout** (unclear whether it is a roundabout or a junction): the design does not help choose the right model; lesson: besides aligning with a model, guide the user to use the intended one.
- **Uber**: innovative but aligned with how a taxi is expected to work (order, get picked up, ride, pay).
- **Norman doors**: the door that is pushed but looks like it should be pulled.

- **Interface metaphors and evolution (Babich, 2022, summary)**: they draw on knowledge from other domains (the first Books apps imitated a library; Calculator, a physical calculator). Models evolve: once the paradigm has been learned, people accept gradual changes (the move from iOS 7 to flat design). It is a nuance of the skeuomorphism point: it serves to **introduce** a new model, it need not be perpetuated.
- **"User error" as mismatch**: most errors arise because the system behaves differently from what was expected; if the user "feels stupid", the problem is the design's, not theirs.
- **Innovating with a learning cost**: think of value to the user against the learning curve; a new paradigm demands fast learning and strong motivation (high value compensates).

## 4. How to elicit them (from light to advanced)
| Method | What it gives | When |
|---|---|---|
| **Think-aloud** in usability tests | The user verbalizes what they think, believe and predict; mismatches between expectation and outcome reveal the model. Recurring across participants -> theme | First step if you suspect wrong models; often enough for design teams |
| **Retrospective interview** | Recalling past experiences: reasoning, pains, expectations, goals | When there is no stimulus to test or the experience is multichannel |
| **Observe and ask for an explanation** / ask them to narrate a recent process | The user's current model in their task (e.g. how they choose a car today before configuring one online) | Before designing |
| **"What would happen if...?" questions** | Predictions for different inputs (in ATMs, people were seen to believe very different things about the information stored on the card) | Systems with hidden rules |
| **Card sorting** | How they group concepts; reveals the model of an information space and lets you design navigation | IA, navigation |
| **Pairwise comparisons with closeness scoring** | A matrix of relationship strength between concepts | Complex systems; the study must be designed for this. Beware fatigue: 5 concepts = 10 pairs; 15 concepts = 105 (N·(N-1)/2). `scripts/lint_artifact.py --pairs N` computes it |
| **Pathfinder networks** | Visualize and statistically compare models across moments | Change over time; requires technical skill |

Choose by goal and needed precision: for quick design changes think-aloud or retrospectives are enough; for complex applications or those with a high risk of inaccurate models, formal methods. Also, a few think-aloud sessions are usually enough to start (NN/g). Formal studies require prior planning; think-aloud insights are incidental if the study was for another question.

## 5. What to do with a gap
Two options (NN/g):
1. **Adapt the system to the user's model** (assuming most have similar models). This is the default option: if they look for something in the wrong place, move it where they look. Card sorting helps decide the navigation.
2. **Improve the user's model**: explain better, clarify labels, teach earlier in the experience (onboarding, examples, tutorials, visual cues). Help should be brief and teach only the key concepts. If you challenge a model, the perceived value must justify the effort of adapting; if not, the user leaves for a product that matches their model.
A third way out: accept that users will not grasp a certain distinction and stop requiring it.

## 6. Procedure and output
1. Define the question (which part of the system, which task). If the team is not clear, start with think-aloud.
2. Elicit expectations with the right method (section 4) and record verbatim quotes.
3. Document the team's/real system's model ("how it truly works").
4. Compare and list gaps; prioritize by frequency and impact (errors, abandonment).
5. Decide: align (default) or teach (with justification and a communication plan).
6. Verify with another round of tests.

Output table:

| Concept / task | They expect (quote, n) | The product does | Gap | Evidence | Action (align / teach / stop distinguishing) | Priority |
|---|---|---|---|---|---|---|

## 7. Common mistakes
- Documenting the mental model as "what the team thinks the user thinks".
- Assuming a single mental model for everyone: look for the dominant models (NN/g: shared themes usually exist).
- Wanting to innovate the interaction when explaining better was enough.
- Fixing the interface without looking at where the expectation comes from (conventions from other sites).
- Basing the decision only on convention (Jakob's Law): it helps not to disorient, but confirm with your own users which convention they come from.
- Asking the user to describe the model in the abstract instead of observing a concrete task or memory.
