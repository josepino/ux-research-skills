# Review checklist and common mistakes

## Four qualities of a good report (User Interviews)
1. **Engaging:** direct quotes, clips, interactive content. If it hooks people, it gets shared and more research gets requested.
2. **Actionable:** goes back to the original question and to the decisions in the plan; makes clear what to do.
3. **Tailored to the audience:** strategy and business for executives, detail for the team; fits the time available; separate formats for mixed audiences.
4. **Objective:** data and evidence first; the researcher's judgment is flagged as such.

## Pre-delivery checklist
Run `ux-insight-qa` first (insights, themes, quotes, numbers), then this list.
- [ ] A decision or action is requested explicitly, with a date.
- [ ] One-page executive summary that makes sense without reading the rest, in plain language.
- [ ] 3-5 findings (not 15); each with evidence (n of N, quote, clip, chart).
- [ ] Objectives and the product metric at the start.
- [ ] Methodology and participants in a few lines; limitations stated.
- [ ] Every recommendation links to a finding, is specific and is prioritized.
- [ ] It says what we do NOT know and which study is missing.
- [ ] Observation, interpretation and recommendation are kept apart.
- [ ] Participants are pseudonymized; consistent with the consent given.
- [ ] No internal jargon (or a glossary); no spelling errors (they hurt credibility).
- [ ] Appendices and a link to the repository; consistent file name.
- [ ] The presentation was rehearsed with someone outside the project.
- [ ] The report is written in the audience's language and the HTML renders correctly (`scripts/render_report.py`).

## Common mistakes
| Mistake | Fix |
|---|---|
| Data dump / "academic novel" | A report is a highlight reel of what matters most; the rest goes to the appendix or repository |
| Showing the process instead of what was found | Conclusions and next step first; method brief |
| Crowded slides, busy design | One idea per slide, key phrases, one strong visual |
| Getting lost in minor details | Explain how the findings benefit the product and the business |
| Vague or personal-taste recommendations | Tie to data; make the change concrete |
| UX jargon | Simple, almost conversational language |
| No narrative structure | Problem -> finding -> why it matters -> way forward |
| No preparation | Rehearse; anticipate objections |
| Percentages everywhere with a small n | Say "X of N" and talk about patterns |
| Report without a link to the raw material | Link to the repository with tags |

## Typical objections and how to answer
- **"n is small / not statistically significant."** Explain how participants were chosen and why qualitative research looks for patterns and reasons (the why), not for population percentages. Acknowledge the limit openly: skeptics worry more about overconfidence (Condens, citing a Dropbox researcher). If you need to quantify, propose a follow-up survey or test.
- **"That's just your opinion."** Show the clip or the original quote and the frequency ("X of N"); separate evidence from judgment.
- **"Why aren't we prioritizing something else?"** Go back to the criteria: severity, frequency, impact/effort, business goal.
- **Stakeholders don't read the report.** Less text, a one-page summary, a short presentation, clips; involve them during the study (Condens argues this works better than relying on the presentation alone) and build trust beforehand.

## Bias in the presentation
Watch how you phrase conclusions: say what the results show and what they do not show, and how to continue. Remember that research raises certainty about a hypothesis but does not deliver absolute truths.
