# Question and probe bank

Use it to complete the guide. Pick few questions per block: the guide is a list of topics, not a questionnaire. Everything is paraphrased and adapted from the sources in `sources.md`. When producing a deliverable, write the questions in the user's language (a few Spanish equivalents are in section 7).

## Contents
1. Research question vs interview question
2. Questions by intent
3. "Vague -> specific" swaps
4. Probes
5. Questions to evaluate a concept or prototype
6. Edge cases
7. Spanish equivalents of common patterns

## 1. Research question vs interview question
- The research question (RQ) is what the team needs to know to decide; **it is not asked to the participant as is**. It must be specific, actionable and practical (Erika Hall; User Interviews).
- Example (Hall): RQ "how do families with school-age children decide how to spend their holidays?" becomes interview prompt "Tell me about your last trip, from planning it to coming back". One narrative prompt can cover several RQs.
- If the RQ starts with "how many / how much", ask for a quantitative method; if it starts with "how / what / why", use a qualitative interview.
- Choose the RQ first and the method after: "we will run a survey, what should we ask?" is the wrong order.
- Motivation and sensitive topics (health, money) are almost never asked head-on: infer them from concrete stories.

**Break the RQ into sub-questions (J. Hall, UX Planet, 2022; summary).** Before drafting, split the RQ into axes and ask 1-2 questions per axis: user role/profile (frequency, familiarity); context (when, where, with whom); motivation (what happened that made them want to reach the goal); solutions tried (what worked, what did not, why, unmet expectations); preparation and information sought; other people who influence the decision; obstacles, worries and problems (how they solved them, how long it took, what they did when it failed); what they would change or do not understand; alternatives and why they chose or discarded each. Example from the source (booking cinema tickets): "Do you remember the last time you went to the cinema?" -> "How and where did you get the ticket?" -> "What was your experience with that app?" -> "Are there other alternatives? Tell me more". Note: some of the source's sample questions ("normally...?", "do you like...?") break this skill's rules; use the axes pattern, not the literal wording.

## 2. Questions by intent
**Open / discover:** "Tell me about...", "Describe how you do...", "What tools do you use for...?", "Walk me through your last...".
**Understand tasks:** "Take me step by step: how do you do [task]?"; "What do you need to know and do to complete [task]?"; "How is [task A] different from [task B]?"
**Show instead of tell:** "Show me how you do it" (screen share); role play: "imagine I'm a colleague who knows nothing about [task], guide me so I can do it alone"; draw the process; complete a sentence. Helps people who think visually.
**Problems:** "What was the hardest or most frustrating part of...?", "How did it affect you?", "How did you solve or work around it?", "What worked well / what was a pleasure?" (asking for the positive too balances the data).
**Opinions (use with care, they suffer courtesy bias):** "What do you think of...?", "Some people say X and others say Y, what do you think?", "What would your colleague/partner say?".
**Person context:** "What role does [task] play in your day?", "How did you decide which product to use?", "How do you prefer to learn to use something new?".
**Closing:** "What didn't I ask that you think is important?", "Who else should I talk to?".

Three lenses to spread questions (Maze): problem, person, product. A balanced guide has all three.

## 3. "Vague -> specific" swaps
| Avoid | Ask |
|---|---|
| Generic ("how do you usually...?", "always", "never") | "When was the last time you...?" |
| Hypothetical ("could", "maybe") | "Tell me about your most recent project that involved..." |
| Future ("would you use...?") | "What did you do the last time you needed something like this?" |
| Indirect ("have you ever...?", "have you considered...?") | "What were you doing right before you decided...?" |
Why (OpinionX, drawing on Torres and The Mom Test): "usually" questions invite an idealized, vague version of oneself; anchored in the last episode, messy reality shows up (for example "I spent more time looking for what to watch than watching").
Other useful swaps: "How easy was...?" (loads a value) -> "Was it easy or hard to find X?" + "What made it that way?" (include both poles); "Why...?" can intimidate some people -> "What led you to click there?", "What were you thinking?".
Never ask "what do you want?" or "would you use it?": almost everyone says yes to a new product and the answer does not predict behavior.

## 4. Probes (rarely written in advance; put them at the top of the guide or on a card)
- "Tell me more about that." / "Can you expand?" / "What do you mean by that?"
- "Why is that important to you?" / "How did that make you feel?"
- Nested follow-ups: "When did it happen?", "How long did it take?", "Had it happened before?", "What did you do next?"
- 5 whys: repeat until answers stop adding something new; 5 is a guide, some threads run dry at 3.
- If the answer is vague, do not interpret it: ask "what do you mean?" or paraphrase it back as a question.
- Emotional labeling: "That sounds frustrating, is that right?" validates and opens the conversation.
- Idea from T. Nguyen (UX Collective, 2020; only the free preview was accessed, without the 32 examples): instead of preparing specific follow-ups, keep a few patterns in mind that tell you when to probe and how to word it openly and without bias. Typical beginner mistakes: closing, leading, not going into detail, switching topic abruptly.
- Mark each guide question as **must / nice / probe** (Lyssna): if time runs out you know what to cut.

## 5. Questions to evaluate a concept or prototype
- Avoid "would you buy / use it?". Ask: "What problem do you see this solving (or not)?", "In what recent situation would you have needed it?", "What surprised you?", "What did you expect to find here?".
- With several concepts, **rotate the order** across participants to mitigate primacy/recency bias (Lyssna).
- If there are tasks with a design, it is already a usability test (behavioral), not an interview (attitudinal): use `ux-usability-testing` or `ux-method-selector`. NN/g: the interview does not show a design and generates new knowledge; the test evaluates a design by watching real use.

## 6. Edge cases
- **Neurodivergence / cultural differences:** open and hypothetical questions can be hard; "could you show me...?" may be answered "yes, I can" because it is taken literally. If someone gets stuck, move to fact- and experience-based questions, or let them demonstrate instead of explain (Stéphanie Walter, citing reader comments).
- **Accessibility / remote:** do a "pre-call" to help them get into the tool; check the platform works with screen readers; use chat with participants who are hard of hearing; if there are surveys or diaries, test them keyboard-only (AnswerLab).
- **Participant who does not match the screener:** in the intro repeat 2-3 key screener questions; if the answers do not match, consider canceling. Same if they lack the right time or device (Lyssna, Maze).
- **Sensitive topic:** go through `ux-ethics-bias-review`; remind them they can pause or skip questions.

## 7. Spanish equivalents of common patterns
| English | Spanish (Rioplatense / neutral) |
|---|---|
| Tell me about the last time you... | Contame la última vez que... / Cuéntame la última vez que... |
| Walk me through... step by step | Caminame por... paso a paso |
| What was the hardest part? | ¿Qué fue lo más difícil? |
| What led you to...? | ¿Qué te llevó a...? |
| Tell me more about that | Contame más sobre eso |
| What didn't I ask that matters to you? | ¿Qué no te pregunté y te parece importante? |
