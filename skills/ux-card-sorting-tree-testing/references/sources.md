# Sources used (card sorting and tree testing)

| Source | What it provides | Part improved |
|---|---|---|
| NN/g, Card Sorting: Uncover Users' Mental Models - https://www.nngroup.com/articles/card-sorting-definition/ | 30-50 cards; 15+ qualitative, 30-50 quantitative; instructions; naming groups afterward; closing questions; recommends avoiding hybrid and preferring tree test over closed; limits | SKILL (variants, cards, session), card-sorting-details |
| NN/g, Tree Testing - https://www.nngroup.com/articles/tree-testing/ | Task types, wording, tree in a spreadsheet, qualitative vs quantitative, limitations, IA recipe | SKILL (tree test), tree-testing-details |
| Maze, Card Sorting guide - https://maze.co/guides/card-sorting/ | Open/closed/hybrid, moderated vs not, samples 15-30 / 30+, dendrogram | Choosing a variant, sample |
| Maze, Card Sorting Analysis - https://maze.co/guides/card-sorting/analysis/ | Analysis steps, standardizing categories, overuse, cross-categorization, report | Analysis |
| Maze, Tree Testing - https://maze.co/guides/ux-research/tree-testing/ | Metrics, first click, 50 per group, 60-80/80-90/90+ reference attributed to NN/g, sequence with other methods | Tree testing, thresholds |
| Lyssna, Card Sorting Guide - https://www.lyssna.com/guides/card-sorting/data-analysis/ | 30-40 cards, 15-30 participants, pilot 3-5, 80/60 thresholds, pitfalls | Quantities, thresholds |
| UXtweak, Analysis of Card Sorting Results - https://www.uxtweak.com/card-sorting/results/ | 50% cut, standardization, matrices, respondent-centric analysis | Manual analysis and script |
| UXtweak, Online vs Offline - https://www.uxtweak.com/card-sorting/online-vs-offline/ | Pros/cons of paper and online | Choosing a format |
| UXmatters, Dancing with the Cards - https://www.uxmatters.com/mt/archives/2010/09/dancing-with-the-cards-quick-and-dirty-analysis-of-card-sorting-data.php | Spreadsheet matrix method, 10% threshold, one level, presenting to clients | Manual analysis |
| IxDF, Card Sorting guide - https://www.interaction-design.org/literature/article/the-pros-and-cons-of-card-sorting-in-ux-research | Limitations, Delphi, tree-card-tree sequence | Edge cases, recipe |
| User Interviews, Field Guide Card Sorting - https://www.userinterviews.com/ux-research-field-guide-chapter/card-sorting | Team vs individual (Donna Spencer), generative vs evaluative | Edge cases |
| Uxcel, Card Sorting lesson - https://app.uxcel.com/courses/ux-research/card-sorting-237 | 30-60 cards, 15-20 min session | Quantities |
| Dovetail, Card sorting - https://dovetail.com/ux/card-sorting/ | 10-15 users minimum, 5-30 min limit, eliminate "Misc" | Quantities |
| Secret Stache - https://www.secretstache.com/blog/card-sorting-usability-testing/ | 40-80 cards (outlier range), unique words | Quantities |
| Toptal, Card Sorting: Better Information Architecture (M. Bowers, upd. Dec 2025) - https://www.toptal.com/designers/ia/card-sorting | 30-70 card range, 15-30 participants, "uncertain" group, think aloud, qualitative vs quantitative analysis, "reverse card sort". Text retrieved via browser, summary | card-sorting-details sections 1 and 7 |

Read without new contributions: PageFlows (d0374bb1c1), Miro templates (templates only).
Note: the text of several pages was truncated; it was completed with additional reading of NN/g, Maze and Lyssna.

## Added in v2
- `quick-synthesis.md`: simplification of UXmatters' matrix method (above) and the Lyssna/UXtweak thresholds already cited. The spreadsheet formula is our own and was not tested in every spreadsheet application.
- `iterative-cycle.md`: sequence from NN/g (open card sort then tree test) and IxDF (tree-test baseline); the stop criterion and the round cap are our own practice.
- `card-and-task-quality.md`: lists supported by NN/g (30-50 cards, tasks without clues, gardening example) and Lyssna; the rules in `check_study.py` are our own heuristics. No new figures.
