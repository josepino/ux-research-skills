# Moderator scorecard

Read this file when you are about to interpret the output of `moderator_scorecard.py` or help someone improve how they moderate.

## Contents
1. What it is for and what it is not for
2. What the script measures
3. How to read each metric
4. Precautions
5. What to do with the results
6. Habits the script cannot see

## 1. What it is for and what it is not for
It serves a person reviewing **their own** moderation and practicing. It also serves coaching that person asked for. It is **not** a performance metric, nor a comparison between people, nor an evaluation of colleagues or vendors: it is heuristic, depends on transcript quality and measures only what is visible in the text. Using it for rankings or evaluations turns a learning tool into a control tool and makes people moderate for the metric.

## 2. What it measures
- % of words and turns per speaker, and words per turn.
- Longest moderator turn (and of the others) and a list of long turns.
- Cut-off turns (ending in "—", "--" or an end marker such as `[interrupted]`; or the next turn starting with `[interrupts]` / `[interrumpe]`, or carrying an overlap marker such as `[crosstalk]` / `[se superponen]`) and who spoke next. English and Spanish markers are recognized.
- Moderator questions, with heuristic alerts: possibly closed (starts with a verb that invites yes/no, in English or Spanish), a "tag" that invites agreement ("right?", "don't you think?", "¿no?", "¿verdad?", "¿vio?"), possibly loaded or suggestive (an adjective inside the question, "surely", "obviously", "seguro que"), options offered ("A or B?" / "¿A o B?") and turns with three or more questions in a row.
- A descriptive count of filler/hedge words in the moderator's turns.

## 3. How to read each metric
- **Speech share (interview)**: as a practice reference, the participant should talk well over half of the time; the script warns if the moderator passes ~35% of the words (our heuristic threshold, not a norm). A high percentage is not always bad (introductions, explaining the task) but it is an invitation to check whether you filled silences or over-explained.
- **Speech share (usability / think-aloud)**: do not compare it with the interview goal. During tasks the participant works in silence or thinks aloud and the moderator hardly speaks, by design. Look at the quality of interventions: that they do not guide or give the answer. For the method, `ux-usability-testing`.
- **Long turns**: was it a necessary instruction or a product explanation, an opinion of yours, or several questions together?
- **Interruptions**: only the marked ones count. If the tool does not mark overlaps, a zero does not prove there were none. Listen to the passages where the participant was left mid-sentence.
- **Questions with alerts**: they are clues to re-listen. A closed question can be fine to confirm a fact; a question with an adjective ("did you find it difficult?") installs the answer. Rephrase openly: "tell me how that task went" (more in `ux-interview-guide`).

## 4. Precautions
- **Speaker labels**: one wrong label inverts or distorts everything. Before reading the numbers, check against the audio a few turns from each stretch.
- **Automatic transcription**: question marks and punctuation are added by the engine; if they are missing, questions are not detected.
- With more than two speakers (groups, observers who speak) the percentages change meaning.
- A number from a single session says nothing; look at trends across several, and always with your own listening.

## 5. What to do with the results
1. Choose **one** thing to practice in the next session (for example, wait three seconds before stepping in, or replace closed questions with "tell me about...").
2. Re-listen to the 2-3 flagged fragments and decide whether they really led the participant.
3. If a key answer came after a loaded question, treat it with caution in the analysis and note it in the limitations (`ux-ethics-bias-review`, `ux-insight-qa`).
4. Share the scorecard with someone else only if you decide to.

## 6. Habits the script cannot see
Tone, rhythm, silences you left, facial expressions, whether you avoided reacting to answers, whether you filled in with "right, right". A colleague who watches the recording with you adds what the text does not show.
