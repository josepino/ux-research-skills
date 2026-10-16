# Empathy map

When to read: when building or reviewing an empathy map, or deciding whether to use one.

## Contents
1. What it is and what it is not
2. Quadrants: how to fill them well
3. Variants
4. Process in 6 steps
5. Three moments of use
6. Common mistakes
7. Use of AI

## 1. What it is and what it is not
- A collaborative visualization of what we know about **one** user or segment. It externalizes knowledge to (1) create shared understanding and (2) help decide.
- It is **not chronological** (that is the journey): it captures a state of mind. It **does not replace the persona**: it is an organized way to visualize what you know about it. A useful relation is 1 to 1: one map per persona or user type.
- It can be fed by any qualitative method (interviews, field studies, diaries, open surveys, support tickets and calls, which capture spontaneous complaints). With no research it can still be sketched, but **marking evidence vs assumptions**.
- Two forms: **individual** (one real person, e.g. one interview) and **aggregated** (patterns from several users in the same segment; often a step before the persona).
- Origin: sources contradict each other. Some attribute the invention to Dave Gray (XPLANE) and others say Scott Matthews developed it in 2010 and Gray popularized it in *Gamestorming*. Cite with caution. Gray himself (Medium, 2017) says it was designed at XPLANE as part of Gamestorming (he does not mention Matthews in what was retrieved).
- Empathy map as an alternative to the persona: it is proposed to use the map (and Jobs To Be Done) when the persona risks fixing stereotypes, because it focuses on a user's thoughts, feelings and barriers without inventing a biography (see `personas.md` section 8).
- Speed: one guide claims a designer can sketch one in under 20 minutes; another speaks of a team in about 10 minutes for a quick version. Use them as an order of magnitude for the light version.

## 2. Quadrants: how to fill them well
The user or persona goes in the center; the quadrants can be filled in any order.

| Quadrant | What goes in | Good | Bad |
|---|---|---|---|
| **Says** | Verbatim quotes from the research, with the participant id (a paraphrase goes without quotation marks and takes `[E#]`) | "I always screenshot the confirmation because I don't trust the email will arrive" | "I want something reliable" (fits any product) |
| **Thinks** | Thoughts, motivations and needs in first person; **pay attention to what they think but do not say** and why (insecurity, politeness, embarrassment) | "Am I stupid for not understanding?" | Team opinions without a basis |
| **Does** | Observable behaviors: how they progress, detours, comparisons | "Keeps the competitor's pricing page open in another tab"; "reloads several times" | Intentions |
| **Feels** | Emotions: **adjective + reason** | "Anxious: doesn't know whether the payment went through" | "Frustrated" alone |

Practice notes:
- **Does** also captures the use of assistive technology (how they move through a form with a screen reader, when they switch to the keyboard). That way accessibility enters as behavior and not as an identity label.
- **Thinks** cells that are inferences go without quotation marks and carry `[Inf]`; `[Obs]` is reserved for what was observed, and interview statements take `[DATA]` or `[Quote]`.
- **Says/Thinks/Does** mix observed and inferred: Says and Does are observed directly; Thinks and Feels are inferences. Label them. For Thinks and Feels, body language, tone and chosen words are clues, but they remain inferences.
- If a participant filled in the map at the end of the session, their **Does** may be what they say they do, not what was observed: take it with caution.
- **Contradictions between quadrants** (a positive action with a negative emotion; says "I value simplicity" but picks the feature-heavy option) are the best starting points for research, because they often point to something the user did not articulate.
- If you hesitate between two quadrants (e.g. Thinks vs Feels), pick one and move on: the goal is not to leave dimensions out, not to classify perfectly.
- **A quadrant you cannot fill, or that is almost empty = missing research** before designing further.
- It helps derive **needs** (verbs, activities/desires, not nouns that would already be solutions) and **insights** by asking "why?" about odd, tense or contradictory behaviors.

## 3. Variants
- **With Goals** as a fifth quadrant (what the user wants to achieve, before and after the product).
- **Pains and Gains** below: obstacles/frustrations/risks versus desired outcomes and measure of success. They clarify where to start designing (pains = problems; gains = outcomes to design toward).
- **See / Hear** (6-section variant): influences from the environment. Hear = what family, friends, colleagues, media say; See = what they see in their environment, what others and competitors do. A practical experience: people often mix See and Hear and find it hard to express "Gain"; adapting labels to context is valid.
- **UX-oriented adaptation (Boag):** Tasks, Feelings, Influences, Pain points, Goals. Also, print the map as a visible **poster** in the organization so it is not forgotten.
- **Map filled in by the user** at the end of an interview or test: adds a complementary source and often reveals Thinks/Feels that had not come up before.

- **Dave Gray's updated canvas (2017, summary)**: starts from the premise that circulating versions degraded and reorders the map. Changes: (1) adds a **Goal** zone (who the subject is and what they need to *do*, phrased as observable behavior); (2) **numbers the sections** to mark sequence; (3) puts **Thinks and Feels in the center, inside the head**, to separate the observable (outside) from what is only inferred; (4) moves **Pains and Gains inside the head** (earlier versions put them in a bottom box) and (5) adds trigger questions to facilitate. Proposed sequence: Goal, then a clockwise pass over the external (See, Says, Does, Hear) and **only afterwards** the internal. For products or services, a complete map can feed a Value Proposition Canvas. In a later revision, Gray reworded the goal because "changing people's behavior" sounded manipulative and clashed with the aim of empathizing; widening the scope of inquiry avoids that bias.
- **Nuances against the above**: (a) NN/g says quadrants can be filled in any order; Gray prescribes external first, then internal. When working with little data his order helps (it avoids projecting thoughts before looking at behavior); it is not incompatible with the "pick one and move on" rule. (b) Pains and Gains: some variants put them below and others inside the head; what matters is that they are read as interpretation, not observation.

## 4. Process in 6 steps (based on NN/g)
1. **Scope and goal**: choose one user or persona (1 to 1). If the aim is aligning the team, have everyone there; if it is analyzing transcripts, set a time limit so several can be mapped.
2. **Materials**: whiteboard, sticky notes, markers (in person) or a shareable digital tool (Miro, Mural, etc.).
3. **Gather the qualitative research.** Each note on the map must be traceable to a concrete artifact (transcript line, recording moment, observation note). No source = assumption, and it is labeled.
4. **Individual generation**: each person reads the data and writes notes **without seeing the others'**, so first opinions do not anchor the group (Mural offers a "private mode" for this). One idea per note; optionally one color per quadrant.
5. **Convergence**: group similar notes within each quadrant, name each group with a theme ("validation from others", "workaround solutions") and discuss out loud: which data was left out? which themes repeat across all quadrants? which appear in only one? what gaps are there? With a facilitator. This is where alignment happens.
6. **Polish and plan**: add quadrants if you need more detail; include user, open questions, **date and version**; digitize; schedule when to return (next research planning).

## 5. Three moments of use (NN/g 2023)
- **Before researching**: the team dumps what they *believe* they know into the four quadrants (one note per idea). If it has been a long time since they researched, assign a **confidence of 1 (low), 2 (medium) or 3 (high)** to each item. Then ask: what do we not know? what are we least sure about? Those gaps are the next study's questions.
- **During research**: observers (even if they are not researchers) record with notes in four colors, one per observation. Afterwards: post-up and affinity diagram to extract themes.
- **After**: to communicate findings. It is more powerful as a collaborative workshop with the extended team, which also generates buy-in and ownership of the research.
General recommendation: start early in the design process, before defining requirements.

## 6. Common mistakes
- **Mapping assumptions as if they were research**: you end up with a record of the team's own beliefs. If it is pre-research, label "hypothesis" and plan the study that tests it.
- **Treating it as a deliverable**: it is exported, presented and filed. The value is in returning to it when a design decision is questioned.
- **Segment too broad** ("our customers"): contradictory notes that cannot be investigated.
- **Letting it age**: date it, version it and schedule a review.
- **Overly generic quotes** and **emotions without a reason** (see table).
- **Confusing it with an affinity diagram**: affinity groups loose notes; the empathy map organizes what we know about a user into fixed dimensions. They are often used in sequence.

## 7. Use of AI
AI can organize evidence you already have; it must not generate it. Before accepting a generated note: can I trace it to real evidence? would I call it a finding or an assumption if I had written it myself? (an NN/g criterion).
