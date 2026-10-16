# Survey design: bias, length, scales and question types

## Contents
1. Before writing: the crucial question
2. Length and timing (figures)
3. Response biases
4. Sampling biases
5. Order bias
6. Leading questions: examples
7. Question types: when to use each
8. Scales (size, balance, NPS)
9. Open questions: mistakes and analysis
10. Pilot test and edge cases
11. Carry-over effects between questions and option order (Alchemer)

## 1. Before writing: the crucial question
- Erika Hall (cited by User Interviews) calls the survey "the most dangerous method" because it is easy to launch and the numbers look like truth. Bad wording = bad data at scale, with no chance to ask a follow-up.
- Caroline Jarrett (cited by User Interviews): run every candidate question through four filters: what do you want to know, why, what decision will you make, and what number do you need. Formulate the **most crucial question** as: "We need to ask ___ so we can decide ___". If there is no decision, drop the question.
- Typical novice mistake: casting a huge net of questions and looking for the goal in the data afterwards.
- Every question must serve the goal; do not ask age or region if you will not segment (Qualtrics).
- A survey works better as an exploratory tool with open questions than as an idea "validator" (User Interviews).

## 2. Length and timing
| Data | Source |
|---|---|
| Rule of thumb of 10-15 questions; aim for under 10 minutes | Maze |
| 1st question ~75 s (includes intro); ~30 s/question for questions 3-10; ~25 s for 11-15; ~21 s for 16-25; ~19 s for 26-30. A 10-question survey takes ~5 min | SurveyMonkey (sample of ~100,000 surveys of 1-30 questions) |
| From 7-8 min drop-off rises; completion rate falls 5 to 20% (higher tolerance in work/school surveys than customer surveys) | SurveyMonkey |
| More questions, less time per question ("satisficing"): with more than 30 questions, about half the time per question | SurveyMonkey |
| Surveys over 25 min: abandonment more than 3 times higher than those under 5 min | SurveySensum (secondary citation) |
| Screener: 10 questions or fewer (Lyssna); 5-10 (Participant Kit) | Lyssna / Consent Kit |

Tactics: prioritize, conditional skips, remove redundancy, progress bar (SurveySensum, SurveyMonkey); if the goal justifies more, run another survey later (UX Mastery). For in-site surveys: 1-2 closed questions first, simple open ones, and a "cool-off" between invitations so the same people are not surveyed over and over (Contentsquare). In the intro text, say who you are and why you ask (Qualtrics).

## 3. Response biases (UXtweak, citing NN/g)
- **Acquiescence**: tendency to agree. Avoid "agree/disagree" scales except standardized instruments (Qualtrics).
- **Social desirability**: over-reporting what is well regarded. Mitigate with anonymity and contrast questions.
- **Recency**: the latest experience weighs most. Ask about concrete periods.
- **Extreme/neutral responding**: appears with boredom or with options that do not fit.
- **Confirmation and framing** (Contentsquare): looking only for what confirms; wording that pushes an answer ("what did you love most?").
- People wanting to please the researcher: also applies to your attitude and expression in sessions (UserTesting).
- Include "don't know / not applicable / other (specify)": forcing an answer distorts and inflates positives (UX Mastery, UXtweak, Lyssna).
- Reduce researcher bias: ask a "critical friend" to review, mix methods, recruit representatively (User Interviews). It reduces bias, it does not eliminate it.

## 4. Sampling biases (SurveyMonkey)
Undercoverage/exclusion · **self-selection** (people with strong opinions answer) · **survivorship** (only current customers skew positive) · **non-response** (due to length, structure or sensitive topics such as income or age) · recall · observer. Causes: poor method (convenience) or poor execution (no follow-up with non-responders). Classic case: the 1948 phone poll that "predicted" Dewey.
- Sauro (MeasuringU) lists strategies: simple random (ideal, hard), convenience, stratified, snowball (hard-to-reach populations), time-based sampling, sequential (start with a reasonable sample and expand according to the confidence interval), serial.
- Lyssna notes incentives can widen the sample beyond the usual volunteers (heavy users); see `incentives.md`.

## 5. Order bias (Qualtrics)
- Order anchors: the classic example of Soviet/American journalists where swapping the order changed support; and "priming" (ice cream -> favorite dessert).
- Randomize **unrelated** questions; group related ones in blocks and randomize within or between blocks.
- Do not randomize questions that depend on each other or have branching.
- Test with a small group before launching.
- Start with the easy; sensitive questions never first; the most complex in the middle, not at the end because of fatigue (Qualtrics). Demographics last (Typeform). Go from general to specific (UXtweak).

## 6. Leading questions: examples (UserTesting, UXtweak)
| Problem | Better |
|---|---|
| "Do you prefer the old version or this improved version?" | Call them version A and B |
| "Did you find this feature frustrating to use?" (suggests the emotion) | "Tell me what it was like to use it" / neutral scale |
| "What caused your navigation difficulties?" (presupposes the problem) | "What was it like to find what you were looking for?" |
| "Would you use this product if you had it at home?" (almost everyone says yes) | "How do you do this task today, without this tool?" |
Good ones: "What did you expect to happen when you tapped that button?" (if they already did), "What pros and cons do you see?". Trick: replace yes/no with "Tell me about a time when..." and check for unnecessary adjectives and adverbs (Qualtrics). Avoid emotionally charged words (UXtweak).
- Contrast note: UX Mastery recommends avoiding questions about behavior in surveys because better techniques exist; this skill suggests asking about **recent past** behavior rather than future intention. Both positions agree on distrusting self-report; for actual behavior use analytics or observation.

## 7. Question types (Typeform, Maze, Qualtrics)
- **Multiple choice**: max ~5 options, ideally ~4 (Maze, citing working memory); non-overlapping and exhaustive; include "other/none" (PlaytestCloud, Consent Kit).
- **Rating/Likert scales**: more information than yes/no (Qualtrics); rephrase yes/no as "how much/how often".
- **Matrix/grid**: Qualtrics discourages (cognitive load, poor on mobile); Typeform tolerates up to 5 rows.
- **Ranking**: max 5 items, not in long surveys.
- **Sliders/dropdowns**: problems on mobile; test them.
- **Open questions**: few (see section 9).
- **Yes/No (dichotomous)**: quick but less informative (Typeform/Qualtrics) and can be leading (Consent Kit).
- **Conditional**: reduce length and abandonment.
- Typeform publishes UX statement examples in true/false format (onboarding, navigation, feature comprehension, task flow, visual design); they work as item seeds, not as a validated instrument.

## 8. Scales
- Balanced, with labeled endpoints and a neutral (odd) midpoint (Qualtrics, UX Mastery). Real unbalanced example: "poor, satisfactory, good, excellent" leans positive.
- A 1-5 scale where 1 = "enjoyed a little" and 5 = "enjoyed a lot" has no negative pole (Contentsquare).
- **Size** (Drive Research): <=5 points format better on mobile; if answers pile up at 4-5, a larger scale gives more variation; for correlations/regressions more than 5 points are better; alternating short and long scales in surveys over 3-5 min reduces fatigue without confusion.
- **NPS**: 0-10 scale; promoters 9-10, detractors 0-6; NPS = % promoters - % detractors. Changing the scale (e.g. 4 points) breaks comparability with benchmarks (Drive Research). `scripts/scales.py nps` computes it.
- Age ranges without overlap (UX Mastery). Avoid double negatives.
- One idea per question: watch the word "and" (Qualtrics, UX Mastery). "Child-level" language and first person (User Interviews).

## 9. Open questions (Qualtrics, SmartSurvey, Typeform)
Common mistakes:
1. Too broad ("what changes did your company make in 5 years?") -> narrow it.
2. Unclear purpose ("why did you buy?") -> "what did you plan to use it for?".
3. Too much effort.
4. Two questions in one.
5. Requiring a minimum number of characters -> generates garbage.
6. Open where closed was enough ("where are you from?" -> dropdown).
7. Too many open questions: one open question costs as much as 4-6 closed ones; max ~5 unless people are highly motivated, spaced out.
8. Forcing an answer -> offer "not applicable / don't know" or allow skipping.
- Alternative for long answers: voice-to-text or video.
- Recent figure (Typeform): 34% of online panelists admitted using LLMs to answer open questions. Consider quality controls (see `incentives.md`).
- **Analysis**: first clean (out-of-profile, incomplete, nonsense), then code by themes (categories; word list or cloud as support, not as analysis) (SmartSurvey). Report % per theme + quotes.

## 10. Pilot test and edge cases
- At least 5 people to test (Qualtrics); ideally unrelated to the product, with no extra context; ask what they did not understand or which option was missing (UX Mastery, Maze).
- Launch first to a subset of the audience before the whole (UX Mastery).
- A/B test wordings if in doubt (Maze).
- Ask an outsider to review bias (UXtweak, Qualtrics).
- Test on mobile and desktop, and read aloud (Typeform).
- Brief context before specific questions (e.g. "Imagine that...") (Maze).
- Ethics: whether survey or experiment, state purpose and data use (Consent Kit: accessibility and informed consent). The OkCupid case (Infobae) illustrates the risk of manipulating users without telling them; for research ethics see `ux-ethics-bias-review`.

## 11. Carry-over effects between questions and option order (Alchemer)
Complements sections 3 and 5. Source: a vendor blog, text retrieved in summary form (partial); treat as indicative.
- **Assimilation**: a later answer moves toward earlier ones (if someone rated several specific aspects very well, the general question comes out inflated). **Contrast**: the inverse effect, an extreme answer is compensated by an opposite one. So the general question goes before the specific ones of the same dimension, or in separate blocks.
- **Carry-over from the previous question**: the classic Schwarz and Clore (1983) experiment shows that mentioning the weather before asking about life satisfaction changed how much weather influenced the answer; the lesson is that prior context contaminates judgment, not that you should mention the weather. Do not quote figures from that study from this summary.
- **Option order**: in self-administered surveys the first options tend to be chosen more; by phone or in person, the last. Randomize the order of nominal options (not of ordered scales: a 1-5 scale must keep its order).
- **Randomizing pages or questions** can break skip logic if follow-ups depend on earlier answers: randomize only independent blocks (matches Qualtrics, section 5).
- **Extreme responding by culture**: depending on cultural context, some people tend to extremes and others to the neutral point. When comparing countries or segments, do not interpret mean differences without considering it.
- **Demand characteristics**: people who guess the purpose of the survey adjust their answers; use a neutral intro about the goal, without revealing the hypothesis.
- Pretest with a small group to detect order, wording and comprehension problems (consistent with section 10).
