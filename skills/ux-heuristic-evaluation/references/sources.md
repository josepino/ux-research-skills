# Sources used for ux-heuristic-evaluation

All read in the downloaded text (no figures from other sources were added, except the W3C checks noted below). The 0-4 severity scale in SKILL.md is Nielsen's classic scale; none of the pages read defines it, so it has no citation here.

| Title and URL | What it provides | Part of the skill improved |
|---|---|---|
| NN/g, How to Conduct a Heuristic Evaluation (Moran and Gordon, 2023) https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/ | Steps (prepare, evaluate alone, consolidate), 3-5 evaluators, 1-2 hours, narrow scope, two passes, independence, consolidation questions, exceptions | SKILL.md procedure; method-and-templates.md; script |
| NN/g, Heuristic Evaluation Workbook (PDF) https://media.nngroup.com/media/articles/attachments/Heuristic_Evaluation_Workbook_-_Nielsen_Norman_Group.pdf | Workbook structure and 2 guiding questions per heuristic | method-and-templates.md; heuristics.md |
| Heuristic Evaluation Template (Google Sheets, read-only) https://docs.google.com/spreadsheets/d/1Skb-K0MfiNzgCeF02eUo02DNAmBAHuoDhLvS9qieexY/edit | Template columns (observation, result, severity, details, notes, page, screen, ticket) | method-and-templates.md |
| NN/g, 10 Usability Heuristics (Nielsen, rev. 2024) https://www.nngroup.com/articles/ten-usability-heuristics/ | Current definitions and tips per heuristic; slips vs mistakes; Jakob's Law | heuristics.md |
| NN/g, User Control and Freedom (#3) https://www.nngroup.com/articles/user-control-and-freedom/ | Back/Cancel/Close/Undo, typical failures, discoverability of undo | heuristics.md (3) |
| NN/g, Consistency and Standards (#4) https://www.nngroup.com/articles/consistency-and-standards/ | Internal/external consistency, layers, periodic reviews | heuristics.md (4) |
| NN/g, Preventing User Errors: Slips https://www.nngroup.com/articles/slips/ | Constraints, suggestions, defaults, tolerant formatting | heuristics.md (5) |
| NN/g, Memory Recognition and Recall https://www.nngroup.com/articles/recognition-and-recall/ | Recognition vs recall, patterns, critique of initial tutorials | heuristics.md (6) |
| NN/g, Flexibility and Efficiency of Use (#7) https://www.nngroup.com/articles/flexibility-efficiency-heuristic/ | Novices vs experts, accelerators, personalization, duplication | heuristics.md (7) |
| NN/g, Match Between System and Real World (#2) https://www.nngroup.com/articles/match-system-real-world/ | Familiar language, natural mapping, metaphors | heuristics.md (2) |
| NN/g, Help and Documentation (#10) https://www.nngroup.com/articles/help-and-documentation/ | Proactive/reactive help, push vs pull | heuristics.md (10) |
| NN/g, Error-Message Guidelines https://www.nngroup.com/articles/error-message-guidelines/ | Visibility, communication and efficiency guidelines; 350 million with color deficiency | error-messages-and-language.md |
| NN/g, Plain Language Is for Everyone (Loranger, 2017) https://www.nngroup.com/articles/plain-language-experts/ | Reading levels, sentence length, jargon | error-messages-and-language.md |
| UX Writing Hub, Error message examples https://uxwritinghub.com/error-message-examples/ | 10 error microcopy guidelines; 14 words/90% figure (secondary, attributed to the American Press Institute, unverified) | error-messages-and-language.md |
| Uxcel, Usability Heuristics https://app.uxcel.com/courses/ux-research/usability-heuristics-553 | Summary: 1990 original, 1994 refined; examples (Netflix, 10-minute calendar, caps lock) | heuristics.md |
| XDStrategy, Desirability Studies (Rohrer, 2008) https://www.xdstrategy.com/desirability-studies/ | Method to measure aesthetic response (heuristic 8) | method-and-templates.md |
| CXL, Error Messages: Examples, Best Practices & Common Mistakes (A. Birkett, 2022, upd. 2023) https://cxl.com/blog/error-messages/ | 4 failures, preventive microcopy, 4 H's, inline validation (2009 study, small sample), measuring form errors. Text retrieved via browser, summary (truncated at the conclusion) | error-messages-and-language.md (inline validation and measurement section) |

## Pages assigned without useful contribution
- https://designerup.co/blog/helping-users-mental-flexibility-through-ux-design/ : about psychological flexibility/mindfulness of the designer; does not help heuristic evaluation ("flexibility" is not heuristic 7).
- Medium, Tamera Atu, "Less is More: The Minimalist Approach in UI/UX Case Study" (2023) https://medium.com/@atutamera/less-is-more-the-minimalist-approach-in-ui-ux-case-study-6845f15e6165 : lists brand examples and a quote, with no evidence or evaluable criteria; the claim that less clutter gives more conversions is unsupported. Nothing incorporated; for heuristic 8 the questions in `heuristics.md` still apply.

## Added in v2
- W3C, Understanding SC 1.4.3 Contrast (Minimum) - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html - 4.5:1 normal text; 3:1 large text (18 pt or 14 pt bold). Improved: `accessibility-basics.md`.
- W3C, Understanding SC 2.4.7 Focus Visible - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html - level AA, see the focused element with the keyboard. Improved: `accessibility-basics.md`.
- W3C, WCAG 2.2 Quick Reference - https://www.w3.org/WAI/WCAG22/quickref/ - titles and levels of 1.1.1 (A), 1.4.1 (A), 3.3.1 (A), 3.3.2 (A), 2.4.7 (AA) and 2.5.8 Target Size (Minimum) (AA, 24 by 24 CSS pixels); verified 2026-10-14. Improved: `accessibility-basics.md`.
- `panel-vs-solo.md`: 3-5 evaluators and timings from NN/g (sources above); the coordination checklist is our own practice.
- `microcopy-before-after.md`: our own examples (English and Spanish), supported by NN/g Error-Message Guidelines principles. No new figures.
