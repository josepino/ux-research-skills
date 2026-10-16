# Threshold for calling a theme a "pattern"

There is no official number. Sources propose practical rules that give different results depending on how many people you interviewed. Show the discrepancy, choose a rule before looking at the data and declare it in the report.

## Contents
1. The rules in circulation · 2. Where they disagree · 3. Recommended practical rule by n · 4. How to count · 5. Exceptions · 6. How to report it

## 1. The rules in circulation
| Rule | Source | Nature |
|---|---|---|
| "3 independent mentions" for something to count as an insight; a single voice is flagged as such | Collective Brain interview kit (public skill, 2026) | Practical guideline from a commercial source |
| "A third of the sample (rounded up)" said something similar => trend; e.g. 3 of 7, 5 of 15 | Nikki Anderson, Dscout People Nerds (2022) | A practitioner's personal routine; she herself says it is not an exact science |
| There is no minimum percentage or count that turns something into a theme; it is analyst judgment and you must declare how prevalence was measured | Braun and Clarke, thematic analysis (guide published by the authors) | Methodological position of the academic source |
| Repetition, consistency across user types and impact, not just majority | Looppanel (already cited in `sources.md`) | Qualitative criterion |
| With very small groups (fewer than 5-6), treat each session as a case | Maze (already cited in `sources.md`) | Practical guideline |

## 2. Where they disagree
With the table below, generated with `python3 scripts/analyze_notes.py --threshold-table`:
| N | 3 mentions | One third | The stricter |
|---|---|---|---|
| 5 | 3 | 2 | 3 |
| 8 | 3 | 3 | 3 |
| 12 | 3 | 4 | 4 |
| 20 | 3 | 7 | 7 |
- With **small n (<= 8)** the "third" is more permissive than or equal to "3 mentions": with 5 participants, 2 would already be a trend by the third but not by the other rule. The risk there is over-interpretation.
- With **large n (>= 10)** "3 mentions" falls short: 3 of 20 is 15%, and the third requires 7. The risk there is calling a minority view a pattern.
- Neither rule looks at severity or segment, and Braun and Clarke remind us that counting does not decide whether something is a theme.

## 3. Recommended practical rule by n (our heuristic, combining the above)
| Sample size | Use | What to do with what falls below |
|---|---|---|
| n < 6 per segment | No numeric threshold: individual cases; report "X of N" and be explicit that these are signals | Everything is a signal to contrast |
| 6 <= n <= 9 | **At least 3 independent participants**, appearing in more than one profile or task if there are several | 1-2 participants: "signal"; 2 with high severity: "review" |
| n >= 10 | **The greater of 3 participants and one third of the sample** (rounded up) | Below the threshold but severe or in a key segment: "relevant minority" |
| Any n with several methods | Also backed by more than one method (`triangulation-across-methods.md`) | Single-method theme: "single source" |
The one-third rule and Nielsen's rule on problem coverage point to different things: Nielsen (2000) estimates that 5 users find about 85% of usability problems if each finds on average 31% (model 1-(1-0.31)^n) and recommends 3 users per category when there are three or more groups; that sizes usability test samples, it does not decide what a pattern is. For thematic saturation, Guest, Bunce and Johnson (2006) found saturation within the first 12 interviews in a homogeneous study, and Hagaman and Wutich (2017) found that 20 to 40 were needed for meta-themes across sites; take this as a sign that with heterogeneous groups you should look per segment.

## 4. How to count
- **Distinct participants**, not mentions or notes (the script does this).
- "Independent" means they did not influence each other (not teammates talking about the same thing, nor two sessions from the same account).
- Count once whoever mentions it spontaneously and, separately, whoever confirms it when you asked; report both numbers ("3 spontaneous, 2 after prompting").
- Count behavior (what they did) and attitude (what they said) separately.

## 5. Exceptions
A single person can be enough to act if the problem is severity 3 (blocks the task or carries a legal, safety or accessibility risk). Then it is not a "pattern", it is a "critical case": say so.

## 6. How to report it
One line in the method: "A theme is considered a pattern if at least 3 independent participants and one third of the sample mention it, whichever is greater; themes below that are reported as signals." Always show "X of N". With AI, ask it to count distinct participants and verify by hand.
