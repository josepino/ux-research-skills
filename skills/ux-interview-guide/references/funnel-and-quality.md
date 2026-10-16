# Guide funnel and verifiable quality rules

**When to read it:** when you finish building or reviewing a guide, before going into the field. It is a pass/fail check; the *how* of wording is in `question-bank.md`. The idea is inspired by third-party interview kits (for example Collective Brain), rewritten; numbers labeled "our heuristic" do not come from an external source.

## Funnel
From broad to specific, and from easy to deep:
1. Entry: 2 easy personal questions.
2. Context: what the participant's situation is like today.
3. Core: concrete past episodes tied to the research question.
4. Deep dive: a bank of probes for the richest episodes (optional).
5. Closing: "anything I didn't ask?" and next steps.
Central content goes in the core, not at the end (if an answer runs long, the end gets cut).

## Verifiable checklist (each item can be ticked by looking at the document)
- [ ] No core question can be answered yes/no. Closed questions live only in the screener or as the opening of a "tell me about...".
- [ ] Every core question points to past behavior (an episode with an approximate date), not to opinion or hypothetical use.
- [ ] In discovery there are no questions about specific features; reaction to solutions belongs to `ux-usability-testing`.
- [ ] The guide survives a change of order: no question depends on another having come first (test it by moving two blocks).
- [ ] Every question maps to a research question; the ones that do not are cut.
- [ ] Every core question is marked must / nice / probe.
- [ ] The sum of timings fits the session with margin (see below).
- [ ] The linter ran (`scripts/lint_questions.py`) and each alert was resolved or justified.
- [ ] There was a pilot or rehearsal with someone outside the team.

## How many main questions fit in 45-60 min
- **Our heuristic:** about 8 to 12 main questions with probes for 45-60 min. The third-party kit reviewed (Collective Brain) sets a cap of 10 to 12; none of the other sources gives an equivalent figure.
- What the other sources do say (see `session-conduct.md` section 6): time matters more than quantity, and a few deep questions yield more than many shallow ones.
- Check with the pilot: if in rehearsal you do not reach the last must-ask question, there are too many questions.

## When a pattern counts: sources disagree
We show the disagreement instead of picking one:

| Rule | What it says | Origin and limits |
|---|---|---|
| "3 independent mentions" | A pattern becomes a finding with at least 3 participants saying it without influencing each other | Third-party interview kit (Collective Brain), no methodological justification on the page |
| Proportion | 1 of 8 may be noise; 6 of 8 is signal | Third-party skill (rampstackco, via Skills Directory): intuitive threshold, no source |
| Saturation | Stop when new interviews no longer bring new themes; cites saturation studies (Guest, Namey and Chen; Hennink and Kaiser) as a starting point, not a requirement | Mentioned in a Great Question catalog (second hand); we did not read the original studies |
| 5 users | 5 participants as a starting figure | NN/g, meant for usability (see `session-conduct.md` section 6); not an interview rule |

What to do about it (our heuristic): always report "n of N" and the segment (never just "several"); a pattern with 1-2 mentions is labeled "weak signal / to confirm"; do not declare a universal fixed threshold; decide the criterion in the plan and write it down before analyzing. For reporting findings, `ux-synthesis` and `ux-insight-qa`.
