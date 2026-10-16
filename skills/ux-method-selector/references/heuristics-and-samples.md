# Decision heuristics, stages, samples and mistakes

**When to read it**: you must justify the choice, adjust to a small budget or define a sample.

## Decision heuristics (why they work)

- **Start qualitative if you do not know what to ask; end quantitative if you need magnitude.** Interviews discover hypotheses; surveys/analytics size them.
- **Combine sayings and doings**: a survey (says) + analytics or a usability test (does) detects contradictions.
- **Needs** are researched by observing, interviewing, with surveys and diaries. **Wants** are explored with A/B tests, discussion groups and rapid prototyping.
- **Small budget**: heuristic evaluation, remote usability tests with 5 people, short surveys, online card sorting, analysis of existing data. "Lean UX" starts from assumptions and validates them with cheap prototypes.
- **If few people are available**: prefer qualitative; do not compute percentages with samples of 8.
- **Sharon's three questions (via Hall, 2017)**: what do they need? what do they want? can they use it? First understand what the product must do (needs/wants) and then whether it does it well (usability). Better to observe what they need or want than to ask directly. With interviews, the critical incident technique (concrete cases where it worked very well or very badly) gives vivid detail.
- **Lean tests without a lab** (Splitview, 2016, blog source): test anything (sketch, wireframe, prototype); guerrilla (go where your persona is and ask for a minute with the prototype), online surveys and unmoderated remote tests. A lab is an artificial environment; testing in the context of use usually gives more honest feedback. However, a sample that does not represent the users is worth little: rely on a well-defined persona/profile. Something lean is better than nothing, but it does not replace recruiting well.
- **New product** without users: competitors, discovery interviews, prototypes. **Existing product**: analytics, usability, in-app surveys, A/B.

## Stage and type of research (NN/g)

- **Strategize -> generative**: field, diaries, interviews, surveys, participatory design, concept testing.
- **Design -> formative**: card sorting, tree testing, usability tests (moderated or not, remote).
- **Launch and assess -> summative**: benchmark, unmoderated test, A/B, analytics, surveys.
Almost every project needs several methods: many teams repeat one or two out of habit. Detail and mixed methods in `references/nngroup-framework.md` (read it when you must justify the choice or design a combination).

## Reference sample sizes (with source)

- Qualitative usability: ~5 per round. Usability benchmark/quantitative: 40 or more (Contentsquare/NN/g).
- Eye tracking: >=30 if only heatmaps are analyzed; >=6 for replays with think-aloud (Smashing); IxDF suggests <=5 to detect problems: sources in tension, explain it.
- A/B: compute the sample beforehand with a calculator; aim for 95% confidence (HubSpot).
- Ethnography/diary: no figure in the sources; do not invent one.

## Common mistakes when choosing

- Using A/B to understand the *why* (it only says which performs better).
- Changing several variables in an A/B or stopping it at the first "winner".
- Relying only on what is stated (survey/focus group) for usability decisions.
- Running eye tracking without crossing it with think-aloud: it shows where people look, not why.
- Benchmark without a pilot or the same methodology between measurements.
- Mixing methods without anticipating that results may contradict each other.
