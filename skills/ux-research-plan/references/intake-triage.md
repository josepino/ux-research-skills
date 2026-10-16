# Intake and triage of research requests

**When to read it**: someone (product, design, marketing, leadership) asks you for a study and you must decide whether it goes ahead, when and how. The idea is inspired by intake practices of research teams (see `sources.md`); the scoring rubric is our own heuristic.

## 1. Questions for the requester
Send them in writing before accepting. If they do not answer 1-4, the request is not yet a study.
1. **Decision**: what will you do differently depending on what we find out? Who decides?
2. **Date**: when is the decision made? (Not when you want "the results".)
3. **What is already known**: what data, studies, support tickets or analytics exist? What do they think the outcome will be?
4. **What changes depending on the result**: if the result is A, what happens? And if B? If both answers lead to the same action, the study is not needed.
5. **Who is the user** of interest and where can they be found.
6. **What was ruled out or already decided** (to avoid researching just to validate something already committed).
7. **Constraints**: budget, legal/privacy, tools, who helps.
8. **What would make the study fail**: misaligned stakeholders, no access to users.

## 2. Quick score (our heuristic)
Score from 1 (low) to 3 (high) and add up:
| Factor | 1 | 3 |
|---|---|---|
| Urgency | The decision is months away or has no date | There is a real, near date |
| Impact | Changes a detail or a small group | Touches a key flow, revenue or many users |
| Effort (inverted: 3 = cheap) | Weeks of fieldwork and hard recruiting | Solved in days with easy access |

Rough reading: 7-9 goes now; 5-6 goes to the backlog with a date; 3-4 is rejected or reformulated. It is an aid for conversation, not an exact calculation: explain the reasoning to the requester.

## 3. Four possible outcomes
- **Goes ahead as a full study**: moves to a plan (`SKILL.md`).
- **"No need to research, we already know"**: there is enough prior evidence (own study, support, analytics). Answer with that evidence cited and what is missing, if anything. It is a valid answer and saves budget.
- **"Run a quick test"**: the doubt is small and reversible. Example: 5 usability sessions of a prototype, a one-question in-app survey, an A/B test if there is traffic. Route to `ux-method-selector` or `ux-usability-testing`.
- **"Not now"**: no decision, no time to act, or no access to users. Note what would have to change to reopen it.

## 4. Reply to the requester
Answer in 4 lines: the decision we understood, what we will do (or not), when, and what we need from them. Keep the request and its outcome on record (see `ux-research-ops`).
