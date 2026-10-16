# How many participants: figures, exceptions and contradictions

Contents: 1. Quick table · 2. Why 5 · 3. When more or fewer · 4. Quantitative tables · 5. Contradictions between sources

## 1. Quick table
| Study | Figure | Source |
|---|---|---|
| Qualitative usability | 5 per segment and round | NN/g (Nielsen, 2012) |
| Overlapping segments (e.g. novice/intermediate/expert) | 3-4 per group (e.g. 3+3+3 = 9, not 15) | NN/g 2012 |
| Agile teams with very little overhead | up to 2-3 per study, many studies | NN/g 2012; UXtweak |
| Consultancy or bigger budget | about 8 (NN/g itself runs them this way) | NN/g 2012 |
| Card sorting | at least 15 per user group | NN/g 2012 |
| Eye tracking (stable heatmaps) | 39 | NN/g 2012 |
| Quantitative, binary metric (success/conversion) | 39-40 (95% confidence, ±15%) | NN/g 2021 |
| Quantitative, continuous metrics only | 47 (95%, ±15%) | NN/g 2021 |
| Interviews | 5-8 per segment (common practice; the sources of this skill do not verify it; heuristic of ours) | practice |

## 2. Why 5 (and what does NOT justify more)
- The cost-benefit ratio collapses after about 5: new findings per person drop fast. Spend the extra budget on **more studies**, not on more users per study.
- Supporting data (Faulkner, cited by UXtweak): with 5 people you find at least about 55% of problems (mean about 85%); with 10, at least 82%; with 15, 90%. If a failure would have serious consequences, go to 10-15 to raise the floor.
- Weak arguments for more users (NN/g): "the site has millions of users" (the quality of a design element does not depend on how many people use it), "it has hundreds of features" (run several studies, each with few tasks; nobody endures more than a handful of tasks), "it is very profitable" (iterate more).
- Legitimate argument: audiences with truly different behaviors (doctors vs patients; buyer vs seller).
- A survey cited by NN/g found the real average was 11 participants per round, more than double the recommendation.

## 3. When more or fewer than 5
- **More**: very complex sites (UXtweak says that with 5 users an e-commerce site may reveal only about 35% of problems; that figure is from that source, not NN/g); several segments; high-risk screens.
- **Fewer**: agile iterations, cheap prototypes that are easy to test.
- **Separate pilot**: 1-2 people to validate tasks and script before launch; for accessibility, the pilot should include someone with accessibility needs (see `accessibility-in-research.md`).
- Time: UXtweak estimates 11-48 hours of total work for 5 participants (planning, sessions, analysis). Use only as an order of magnitude.

## 4. Quantitative: NN/g tables (2021)
Assumptions: population > 500, binary metric. Figures are rounded up in case someone must be discarded (cheaters or non-representative participants).

| Confidence | Margin of error | Binary | Continuous only (time, satisfaction) |
|---|---|---|---|
| 95% | ±15% | 39 | 47 |
| 95% | ±20% | 21 | 26 |
| 90% | ±15% | 28 | 33 |
| 90% | ±20% | 15 | 19 |

- They do not recommend margins above ±20%: the interval becomes useless.
- If you collect success + time + satisfaction, size for the binary metric; it works as a constraint for the others.
- For continuous metrics without a pilot, NN/g proposes assuming a standard deviation of about 52% of the mean (Nielsen's estimate for websites/intranets).
- Use `scripts/sample_size.py` to get the total to recruit with a margin.

## 5. Contradictions between sources (tell the user)
- **Quantitative**: NN/g 2012 says "at least 20"; NN/g 2021 says it recommended different figures over the years and now suggests 40 (30 if you accept 90% confidence); UXtweak says 20-40; Lyssna says 20-30. They are not errors: they depend on confidence and margin. Rule: 20 is a high-risk floor; to report percentages with backing, aim for 30-40.
- **Card sorting and eye tracking**: appear only in the 2012 NN/g article; the 2021 one does not update them.
- **Recruit more vs save**: UXtweak suggests about 10 may be the most cost-efficient point; NN/g insists on 5 per round and several rounds. Both agree on iterating.
