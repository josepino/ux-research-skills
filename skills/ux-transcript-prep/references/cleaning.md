# Cleaning for analysis

Read this file when you must decide what to remove from a transcript and what not, set the speaker format, segment, or write a session header.

## Contents
1. Principle: cleaning reduces noise, it does not edit the participant
2. What is normalized, what is removed and what is kept
3. Speaker labels
4. Evident errors: mark, do not correct
5. Segmentation by blocks and by time
6. Session header (template)
7. What `prepare_transcript.py` does and does not do

## 1. Principle
Cleaning exists so the analysis reads better, not so the participant sounds better. Every silent edit is an invisible interpretive decision. So the rule is: remove mechanical noise (timestamps, hesitation sounds with no content), keep everything that can carry meaning, and flag anything doubtful so a person decides.

## 2. What to do with each thing
| Element | Decision | Why |
|---|---|---|
| Inconsistent speaker labels ("Speaker 1", "Ana", "A. Perez") | Normalize with an explicit map (original -> normalized) | Otherwise counts and per-speaker searches fail |
| Timestamps | Remove if you will no longer use them; **keep them** if you will build clips or cite with a reference | They break reading, but they let you return to the audio |
| Hesitation sounds ("um", "uh", "er", "hmm" / "eh", "em", "mm") | Remove only if the analysis is about content; keep in think-aloud or if hesitation matters | Sometimes the hesitation is the finding |
| Discourse fillers with content ("you know", "I mean", "like" / "o sea", "este", "bueno", "¿vio?") | **Do not remove by default.** The script removes them only with `--strip-discourse-fillers` (and only when set off by commas) or by name with `--extra-fillers` | They are real words and sometimes mark evasion or uncertainty; "like", "este" and "bueno" are also ordinary content words |
| Hedges ("I guess", "maybe", "kind of" / "creo que", "tal vez", "capaz", "más o menos") | Keep; the report only counts them | Uncertainty is data |
| Pauses, laughter, sighs, emphasis, long silences | Keep (`[laughs]`, `(pause)`, `[pause 4 s]`) | Emotional and rhythm information |
| Verbatim quotes | Do not touch | They are literal evidence; used later in reports |
| Repetitions ("that that") | Keep and flag | May be stammering or emphasis |
| Swearing, slang, regionalisms, grammar errors | Keep | Part of how that person speaks |
| Overlapping voices | Mark `[overlap]` / `[se superponen]` or cut the turn with "—" | The scorecard and the interruption analysis need it |

## 3. Speaker labels
- Moderator: one single label across all sessions (for example `Moderator`). Participants: the code (`P01`, `P02`...) from the start, not the name.
- Build a CSV `original,normalized` per session (or one per tool, if the pattern repeats) and pass it with `--normalize-speakers`. The report lists labels left unmapped.
- Automatic tools get speakers wrong, especially when voices overlap or someone speaks little: check a sample against the audio (start, middle and end) before trusting any count.
- If there are observers or interpreters, give them their own label; otherwise their phrases get attributed to the participant.

## 4. Evident errors: mark, do not correct
If "thanks for the charge" clearly was "thanks for the charger", do not change it quietly. Leave the original word and add `[sic? charger]` or `[inaudible]`. Note in the header how many marks there are. Listen to the audio of passages you will quote. That way whoever reads later knows what is said and what is inferred.

## 5. Segmentation
- **By blocks**: if there was a guide, insert one heading per block (`## Block 2: Current use`), taken from the guide or marked by the moderator at topic changes. It makes it easier to compare the same question across participants.
- **By time**: if there are no blocks, cut about every 10 minutes (our heuristic) with the timestamp of the cut, so fragments can be located in the audio and huge documents avoided.
- **By tasks** in usability: one heading per task with its observed result in the header (without judging). For usability design and analysis itself, `ux-usability-testing`.
- If you paste into an AI with a context limit, segment first: whole blocks, never cut mid-turn.

## 6. Session header (descriptive, no interpretation)
```
Session: S01 | Participant: P01 | Date: 2026-03-04 | Duration: 52 min
Method: semi-structured interview | Moderator: M1 | Observers: 2 (O1, O2)
Blocks covered: 1, 2, 3 (block 4 not reached)
Consents: participate yes | audio yes | video no | anonymous quotes yes | AI use: [fill in]
Incidents: connection drop min 14-16; weak audio min 31-34 ([inaudible] x3)
Transformations applied: labels normalized; timestamps removed; pseudonymized (counts by type only, no names; see separate map)
```
Translate the labels to the user's language. What does NOT go in the header: "the participant seemed uninterested", "good session". That is interpretation; if relevant it goes in the debrief notes (`ux-research-ops`).

## 7. What `prepare_transcript.py` does and does not do
Does: parse "Speaker: text" lines with optional timestamps at the start or next to the label; join continuation lines; normalize labels with a map; remove timestamps and sound fillers (English and Spanish); optionally remove comma-delimited discourse fillers; merge consecutive turns by the same speaker; verify that quoted text stayed identical; count hedges (kept); report changes and things to review.
Does not: correct words, detect transcription errors by meaning, separate speakers by voice, or pseudonymize (for that, `pseudonymize.py`). Always try it first on one session and read the whole result.
