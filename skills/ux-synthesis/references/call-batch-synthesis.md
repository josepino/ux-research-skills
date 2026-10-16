# Synthesis of a batch of calls or transcripts

Use when there are several calls (sales, support, discovery) or interviews that nobody has reread together and you need a defensible summary before the deep thematic analysis.

## Contents
1. Before starting · 2. Work in batches · 3. Validated and invalidated assumptions · 4. Recurring requests · 5. Contradictions and weak signals · 6. Summary template · 7. Limits

## 1. Before starting
- Clean transcripts, with a consistent speaker label and pseudonymized (`ux-transcript-prep`).
- A written list of the team's **assumptions and hypotheses**, made before reading. Without the list there is nothing to validate and confirmation bias creeps in.
- One ID per call and per participant, with date and segment.

## 2. Work in batches
With many calls, synthesize in batches of 10 to 12 and then synthesize the batch outputs (a practical guideline from Great Question for AI-assisted flows; it is not a methodological limit, it is so context does not get diluted). Each batch produces the same template; the final step only merges templates and does not go back to transcripts. Check that every quote in the final summary exists in its original transcript.

## 3. Validated and invalidated assumptions
For each assumption on the list:
| Assumption | Verdict | Evidence (calls, n of N) | Quote | Confidence |
|---|---|---|---|---|
| "First-time buyers compare at least 3 vendors" | Invalidated | 2/14 compare; the rest buy from the first to answer | "I asked one for a quote and that was it" (L7) | Medium |

Possible verdicts: **validated**, **invalidated**, **mixed** (depends on segment) and **no evidence** (the topic did not come up; this is not the same as invalidated). An invalidated assumption goes first in the summary: it changes the most decisions.

## 4. Recurring requests (ranked by frequency, not recency)
1. Extract each request verbatim with the call ID.
2. Group by **underlying need**, not by the requested feature ("export to Excel", "send weekly report" and "share with my boss" can be one need).
3. Count **distinct participants**, not mentions: a person who repeats it across three calls counts once.
4. Rank from most to fewest participants. What was mentioned in the last call weighs the same as what was mentioned in the first. To highlight something recent, do it in a separate column ("new in the last batch").
5. Note severity and segment: a request from a few people that blocks a task deserves mention even if it ranks low (`pattern-threshold.md`).

| Need | Participants (n of N) | Example requests | Segment | Severity |
|---|---|---|---|---|

## 5. Contradictions and weak signals
- **Contradictions:** two groups of calls holding opposite things. Check segment, moment and task (step 6 of `SKILL.md`) before deciding which one "wins". They are often the most valuable.
- **Weak signals:** themes with 1-2 participants that seem significant. List them in a separate section ("to investigate") without calling them a pattern.
- **Surprises:** what nobody on the team anticipated.

## 6. Summary template (one page)
1. Scope: number of calls, dates, segments, what it does not cover.
2. Validated / invalidated / mixed assumptions (table in section 3).
3. Recurring requests (table in section 4), top 5.
4. Contradictions and signals to investigate.
5. The decision or study that follows.

## 7. Limits
Sales or support calls are not research interviews: they are biased by the reason for contact (someone calling support has a problem). Label the source and do not extrapolate to "all users". A batch summary is the first step; it does not replace coding and review by a second person.
