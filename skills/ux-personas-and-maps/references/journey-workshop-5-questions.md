# Journey map workshop in 5 questions

When to read: when the team wants to build a shared journey map in one session, starting from a synthesis (or from hypotheses).

A short workshop to go from synthesis to a shared map. It rests on the components NN/g describes for a journey map (actor, scenario and expectations, phases, actions/mindsets/emotions, opportunities; Gibbons, 2018). Each question adapts to what the team already knows; if someone answers "we don't know", it is noted as a gap and not invented.

## Contents
1. Before the workshop · 2. The 5 questions · 3. Output · 4. Afterwards · 5. Mistakes

## 1. Before the workshop
- Choose **one actor and one scenario** (one map per actor). Gather the synthesis (`ux-synthesis`) and, if it exists, the persona.
- Decide whether the map is **current** or **future**, and whether it starts from **hypotheses or research** (`journey-map.md` section 2).
- Invite design, product, engineering and customer support. It is a team session, not solitary work; alone it counts as a draft.
- Material: findings with source IDs, quotes, short clips.

## 2. The 5 questions (adaptive)
Ask the questions one at a time and wait for the answer. If the team already answered one through the synthesis, confirm it and move on.

**1. Who is the actor and what is the scenario?**
A specific person or segment, their goal and what they expect to get. Example: "Marta, administrator, is switching online scheduling providers; she expects not to lose appointments during the migration". If they answer "the users", ask for a segment. Label whether the actor is a validated persona or a proto-persona.

**2. What are the phases?**
Propose 4 to 6 high-level stages (discover, compare, decide, start using, keep using...). That number is the guideline of the playbook consulted (Claude Code Playbooks), not an NN/g rule: adjust it to your scenario. Phases are moments, not loose tasks. If 12 come out, group them.

**3. What does the actor do, think and feel in each phase, and where does it hurt?**
Per phase: actions, thoughts (better with a real quote), emotions as "adjective: reason" and pain points. Each cell carries a source (`[E#]`, `[Quote]`) or `[ASSUMPTION—VALIDATE]`. A cell without data is a gap, not a hole to fill with opinion. Mark where there is contradiction (says one thing, does another).

**4. What opportunities emerge, ranked by impact?**
One opportunity per pain or emotional peak, phrased as "How might we...?". For each, note: **evidence** (how many participants, from which method), **expected impact** (for the user and the business), **estimated effort** with engineering and **owner**. Rank by impact with the evidence in view; an opportunity without evidence goes to the bottom and is marked. The same playbook suggests 5 to 7 opportunities; it is a practical guideline: if many more come out, prioritization is missing.

**5. Who owns it, what do we decide and what is next?**
Owners per opportunity, decision taken, how it will be measured (metric or observable behavior) and what will be validated with users. Review date for the map.

## 3. Output
Use the journey template in `templates.md`. Header with actor, scenario, status (current/future), base (hypothesis/research n=__), date and version; body with phases x (actions, thoughts, emotions, pains); an opportunities table like this:
| # | Opportunity (How might we...?) | Phase | Evidence (n of N, method, source) | Impact | Effort | Owner |
Close with **Gaps**, **Decisions it enables** and **Next research step**. Add the traceability table from `from-synthesis-to-persona-and-journey.md` when the map comes from a synthesis.

## 4. Afterwards
Run `python3 scripts/lint_artifact.py map.md --type journey`. Share it somewhere visible, use it in concrete decisions and review it when the product changes. If it moves to design or engineering, continue with `ux-research-report`.

## 5. Mistakes
- A map with several actors.
- A workshop without prior research and the map treated as a finding.
- Opportunities without evidence or owner.
- A pretty map nobody reopens.
