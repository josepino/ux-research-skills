# Proto-persona with assumption tags

When to read: when the team needs to align now and there is not yet enough research, or when deciding whether a proto-persona can be called a validated persona.

It serves to **align the team today** when there is not enough research yet, without anyone confusing what we believe with what we know. It is used before researching, not instead of researching.

## Contents
1. Tag convention (unified) · 2. Template · 3. How to build it in one session · 4. From proto-persona to validated persona · 5. Example · 6. Mistakes

## 1. Tag convention (unified)
| Tag | Means | Equivalents accepted by `lint_artifact.py` |
|---|---|---|
| `[ASSUMPTION—VALIDATE]` | We believe it but have not checked it; it must be validated with evidence | `[Hypothesis]` (older convention of this skill), Spanish `[SUPUESTO—VALIDAR]` and `[Hipótesis]`; the dash may be —, – or - |
| `[DATA]` | Backed by a concrete source (state which) | `[E#]`, `[Quote]`, `[Obs]`, Spanish `[DATO]`, `[Cita]` |
| `[Inf]` | Our inference from data | none |
Rule: **nothing without a tag**. In proto-personas most lines will be assumptions, and that is fine: what is not fine is failing to say so. In new artifacts prefer `[ASSUMPTION—VALIDATE]` because it says what to do; `[Hypothesis]` remains valid in existing ones.

## 2. Template
```markdown
# Proto-persona: [name and role]
Status: Proto-persona (team assumptions) · Date: YYYY-MM-DD · Version: v1 · Base: workshop with [who], no research (n=0) + [existing sources, if any]
Review before: ____ · Owner: ____

| Field | Content | Tag |
|---|---|---|
| Who they are (role, context of use) | ... | [ASSUMPTION—VALIDATE] |
| What they try to achieve (goal) | ... | |
| What makes it hard (pain/obstacle) | ... | |
| How they solve it today (behavior) | ... | |
| A quote that sums them up (only if real) | "..." | [DATA] E1 |
| Who decides / influences | ... | |
| What would make them choose us or leave us | ... | |
| Typical usage scenario | ... | |

## How we validate each assumption
| Assumption | How we validate it | Evidence that confirms/refutes it | Owner | Date |

## Gaps
- ...
## Decisions it enables (and which it does NOT)
- Good for: aligning the team, building the screener, preparing interviews. Not for: deciding big investments.
```
Avoid loose demographics ("30-45 years old, lives in a city, has a dog") unless they explain a behavior; prefer goal, obstacle and context of use. Do not invent quotes: with no real data, leave the field empty. Translate the headings and labels to the user's language when producing the deliverable.

## 3. How to build it in one session (about 60 min, our heuristic)
1. **Define the purpose** (which decision does it support?) and the segment.
2. **Pour out individually** what each person believes (5 min, silently) and then group.
3. **Tag** each line: do we have real data behind it? If yes, state which; if not, `[ASSUMPTION—VALIDATE]`.
4. **Rank the assumptions by risk:** what would happen if we were wrong? The highest-risk and least-evidenced are validated first.
5. **Define how to validate** the 3-5 riskiest (interviews, survey, analytics, support). Move to the plan with `ux-research-plan`.

## 4. From proto-persona to validated persona
Suggested criterion (our heuristic, combining the guidance in `personas.md` sections 3 and 4). It becomes a validated persona only when ALL of these hold:
- There are **interviews or observation with people from the segment**, and the central assumptions (goal, obstacle, current behavior) were confirmed, refuted or rewritten with evidence.
- You triangulated with **at least one other source** (analytics, support, survey, sales) or stated why not.
- **No critical assumption** (one that would change a decision) remains unvalidated; minor ones may stay tagged.
- Reasonable saturation was reached: the last sessions no longer add new fields (`personas.md` section 4 shows how many interviews different sources suggest, from 5 to 10 per type).
- Someone outside the workshop checked the traceability (every claim points to a source).
When it passes, change the status to "Research-based (n=__)", replace the tags with sources, bump the version and record which assumptions fell: that is a valuable result. If any condition is missing, the persona stays a proto-persona even if it already has partial data.
`python3 scripts/lint_artifact.py proto.md` warns if it says "Validated" but still keeps many assumptions.

## 5. Example (summarized, fictional)
Marta, administrator of a clinic. Goal: fill the schedule without phone calls [ASSUMPTION—VALIDATE]. Pain: patients cancel at the last minute [DATA] E1 (support tickets, 14 cases). Decides the purchase together with the medical director [ASSUMPTION—VALIDATE]. First step: interview 5 administrators to validate who decides.

## 6. Mistakes
- Tagging everything [DATA] because "the whole team knows it".
- Turning the proto-persona into a poster without the assumption tags.
- Validating only what confirms what we believed.
- Leaving it without a review date.
