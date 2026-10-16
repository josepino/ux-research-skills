# Quick per-participant synthesis

Use to synthesize right after each session ends (instead of piling everything up for the end) and to feed the later analysis. Times are our own reference, not a standard: adjust them to session length.

## Contents
1. When to use it · 2. Pace · 3. One-page template · 4. The quick-fix tag · 5. What to do with the sheets

## 1. When to use it
- Studies with few sessions and short deadlines, or when the team observes live.
- When there is a risk of forgetting nuance: memory degrades fast and the first sessions change what you look at in later ones.
It is the per-session version of the advice not to leave analysis for the end (`ux-research-ops` covers the daily debrief).

## 2. Pace (our heuristic)
| Step | Approximate time |
|---|---|
| Reread notes or recording at fast speed and fill in the sheet | 20-25 min |
| Choose 2-3 quotes and mark the video moments | 5-10 min |
| Compare with the previous participant's sheet (repeats? contradicts?) | 5 min |
Total: 30-40 min per session. Do it the same day; if deferred, the sheet loses detail.

## 3. One-page template
```
Participant: P__ · Segment: ____ · Date: ____ · Method: ____
Study objectives it touches: ____
1. What they did (behavior, observed):
2. What they said (attitude, quotes with timestamp):
3. What surprised us / contradicts our assumptions:
4. Problems or needs (one line each) · severity 1-3 · quick fix (yes/no):
5. Does it repeat anything from earlier participants? (codes)
6. Questions for the next session / adjustment to the guide:
Confidence in what was noted: high / medium / low (what is left to verify?)
```
Rule: observation and interpretation go in separate fields. If in doubt about a quote, go back to the recording. Translate the labels to the user's language when producing the sheet.

## 4. The quick-fix tag
Mark "quick fix" only if all three hold: (a) the problem is clear and observed, (b) the solution is cheap and reversible, (c) it does not depend on an open product decision. It lets the team correct a confusing text while the study continues, without waiting for the report. Keep a record (what changed and when), because changing the product mid-study affects what later participants see. Everything else waits for the joint analysis.

## 5. What to do with the sheets
At the end, pour the sheets into the notes CSV (one idea per row, with ID and tags) and run `scripts/analyze_notes.py` to count distinct participants. The sheets feed the analysis; they do not replace it. With 5-6 sessions or fewer per segment, treat each sheet as a case (step 1 of `SKILL.md`).
