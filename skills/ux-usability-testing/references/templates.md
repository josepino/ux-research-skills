# Templates

Write these with English headings, and translate headings and labels to the user's language when producing deliverables.

## 1. Test plan
- **Product/version to test** and fidelity:
- **Decision the test informs**:
- **Research questions** (2-4), one row each:

| Question | Task | Metric | Decision it informs |
|---|---|---|---|

State any empty cell as a gap.

- **Type**: formative / summative · moderated / unmoderated · remote / in person
- **Participants**: profile, n per group, inclusion criteria (see `ux-participants-recruiting`)
- **Tasks** (table):

| # | Scenario (user's language) | Success criterion | Time/attempt cap | Metrics |
|---|---|---|---|---|

- **Questionnaires**: SEQ per task only if the team wants numbers · UMUX-Lite or SUS at the end (optional)
- **Setup and team**: device, tool, recording, moderator, observer
- **Schedule** (pilot, sessions, analysis, report) and **risks**
- **Ethics**: consent, data, recording (see `ux-ethics-bias-review`)

## 2. Moderation script
1. **Welcome** (3-5 min): "Thank you for coming. We are testing the product, not you; there are no wrong answers. You can stop whenever you like. Is it OK if we record the screen and your voice?" (confirm consent)
2. **Think-aloud + warm-up**: "While you work, say out loud what you look at, think and expect."
3. **Context** (optional, 2-3 questions): previous experience with similar products.
4. **Tasks** (read verbatim): T1 …; T2 …; after each: "what was the hardest or most confusing part?" (+ SEQ if numbers are wanted)
5. **Closing**: "What was best and worst?", "what would you change?", SUS/UMUX-Lite if applicable, thanks and incentive.
6. **Debrief** right away with the observer.

Reminders in the margin: do not help, do not defend, do not use adjectives; neutral silence; "what did you expect to happen?".

## 3. Observation sheet (one per participant)
Participant: P__ · Date · Moderator · Device

| Task | Result (success/partial/failure/helped) | Time | Errors | SEQ | What they did and said (quotes with minute) | Problem (ID) |
|---|---|---|---|---|---|---|

Other notes: surprises, comments about the prototype, things in the script to fix.

## 4. Problem matrix
CSV format for `scripts/problems_matrix.py`:
```
participant,problem,severity
P1,Cannot find the date filter,3
P2,Cannot find the date filter,3
```
Reading view:

| ID | Problem (observation) | P1 | P2 | P3 | P4 | P5 | Freq. | Sev. 0-4 | Recommendation |
|---|---|---|---|---|---|---|---|---|---|

## 5. Short report (1-2 pages)
1. **Summary**: what was tested, with whom, when, n, version.
2. **Top 3-5 problems** (ordered by severity and frequency): observation, evidence (x of n, quote), severity, recommendation.
3. **Metrics per task**: success (counts), time, SEQ; with small n do not present percentages as statistics.
4. **What worked well**.
5. **Next steps**: what to fix, what to retest and when.
6. **Limits**: sample, prototype, moderator help.
For a formal report: `ux-research-report`.
