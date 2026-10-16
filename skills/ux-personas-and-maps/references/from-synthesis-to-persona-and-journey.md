# From synthesis to persona and journey, with traceability

When to read: when you have a synthesis (themes, quotes, insights) and need to turn it into a persona or journey without inventions creeping in.

The synthesis (`ux-synthesis`) produces themes, quotes and insights with participant IDs. A persona or journey is a **view** of that data for a concrete use. Traceability prevents inventions from slipping in along the way.

## Contents
1. What comes out of the synthesis and where it goes · 2. Traceability table · 3. Steps for a persona · 4. Steps for a journey · 5. Checks before delivering · 6. Mistakes

## 1. What comes out of the synthesis and where it goes
| Synthesis element | In the persona | In the journey |
|---|---|---|
| Behavior codes (what they do) | Current behavior, context of use | Actions per phase |
| Attitude codes (what they say, believe) | Goals, motivations, beliefs | Thoughts |
| Coded emotions | Frustrations and triggers | Emotion line ("adjective: reason") |
| Pains with severity and frequency | Main obstacles | Pain points |
| Insights and HMW | Needs | Opportunities |
| Differences between segments | What separates one persona from another | One map per actor |
| Quotes with ID | Representative quote (real) | Quotes per cell |

## 2. Traceability table
Build a support sheet (or an appendix) with one row per claim:
| ID | Claim in the artifact | Tag | Source(s) | Participants (n of N) | Method |
|---|---|---|---|---|---|
| A1 | "Compares three providers before deciding" | [DATA] | E1, E3 | 5/8 | Interviews |
| A2 | "Decides together with the medical director" | [ASSUMPTION—VALIDATE] | - | - | Internal workshop |
Each cell of the artifact cites the ID of this table (`[A1]`) or a source `[E#]`. If there is no row, there is no claim.

## 3. Steps for a persona
1. Select the segment by **behavior and goal**, not by age or gender (`personas.md`).
2. Take the themes that appear in that segment and check the pattern criterion (see the pattern threshold in `ux-synthesis` if you have it at hand; otherwise declare your own rule).
3. Write with the template (`templates.md`), each field with its traceability ID.
4. Fields without data: `[ASSUMPTION—VALIDATE]` or empty (`proto-persona.md`).
5. One real quote per persona, with a participant ID (never invented or "perfect").
6. Status, date, version and review (`personas.md` section 7).

## 4. Steps for a journey
1. One actor and one scenario; if there are personas, use a base persona.
2. Phases from observed behavior, not from our internal departments.
3. Pour in actions, thoughts, emotions and pains from the synthesis codes, with IDs.
4. Mark contradictions and gaps.
5. Opportunities from the prioritized HMWs, each with its evidence (`journey-workshop-5-questions.md`).
6. Validate with users before investing if the map started from hypotheses.

## 5. Checks before delivering
- `python3 scripts/lint_artifact.py file.md`: status, date, evidence base, share of tagged notes, gaps.
- Spot check: pick 5 claims at random and follow them to the original quote or data point.
- Pass insights and quotes through `ux-insight-qa` if the artifact will leave the team.
- If AI was used to organize: every claim must be traceable to real data; if not, `[ASSUMPTION—VALIDATE]`.

## 6. Mistakes
- Summarizing better than the data says ("everyone wants..." with 3 of 12).
- Mixing segments to "cover more".
- Losing the ID when copying the quote into the artifact.
- Delivering the artifact without the traceability table.
