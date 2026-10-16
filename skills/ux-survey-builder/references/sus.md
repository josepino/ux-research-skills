# SUS: System Usability Scale

Answer scale for every item: **1 = Strongly disagree ... 5 = Strongly agree**. Keep the 10 items, their order and the 1-5 scale; the word "system" may be replaced by "website", "app", "product"...

| # | Statement (standard English wording) | Type |
|---|---|---|
| 1 | I think that I would like to use this system frequently | positive |
| 2 | I found the system unnecessarily complex | negative |
| 3 | I thought the system was easy to use | positive |
| 4 | I think that I would need the support of a technical person to be able to use this system | negative |
| 5 | I found the various functions in this system were well integrated | positive |
| 6 | I thought there was too much inconsistency in this system | negative |
| 7 | I would imagine that most people would learn to use this system very quickly | positive |
| 8 | I found the system very cumbersome to use | negative |
| 9 | I felt very confident using the system | positive |
| 10 | I needed to learn a lot of things before I could get going with this system | negative |

Spanish version (adaptation, no official translation): `references/sus-items-es.txt`.

## Calculation
- Odd items (1,3,5,7,9): contribution = answer - 1
- Even items (2,4,6,8,10): contribution = 5 - answer
- Score = sum x 2.5 (range 0-100). It is **not** a percentage.

## Interpretation (two frameworks from different sources; both indicative)

**Framework 1: grading curve (Sauro, as cited by TeaCup Lab).** Base: more than 5,000 users in about 500 studies; global average = 68.

| Score | Grade | Approx. position |
|---|---|---|
| 78.9 - 100 | A | top 15% |
| 72.6 - 78.8 | B | top 35% |
| 62.7 - 72.5 | C | top 65% |
| 51.7 - 62.6 | D | top 85% |
| 0 - 51.6 | F | worst group |

Acceptability (same source): > 70 acceptable; < 50 unacceptable; 50-70 marginal (roughly grades C-D).

**Cutoffs according to MeasuringU (page "sus", verified 2026-10-14)**: average of 500 studies = 68; A above 80.3 (top 10%); C = mean 68; F below 51 (bottom 15%). This differs from the TeaCup Lab cutoffs above (A >= 78.9): both approximate the same curve; cite the source you use and do not mix them. The script uses the TeaCup Lab table.

**Framework 2: adjective scale (UXABLES).** 0-26 worst imaginable; 27-50 poor; 51-70 "OK"; 71-80 good; 81-90 excellent; 91-100 best imaginable.

**Discrepancies to keep in mind**
- A 68 is "average" in Framework 1 but falls in "OK/marginal" in Framework 2. Pick one framework, cite it and do not mix them.
- An older table (<51 poor, 69-80 good, >80 excellent) was indicative and matches no source exactly: it is no longer used.
- Historical attribution: TeaCup Lab and thestory.is (secondary summary) say John Brooke, 1986, originally for electronic office systems; UXABLES says "Malcolm J. Brooke, 1996" (two sources against one; still unverified in a primary source). Cite 1986 / John Brooke only after verifying in a primary source.
- Official Spanish translation: none (TeaCup Lab). UXABLES proposes [system/function/product] as the placeholder.

## Good practice and limits
- Apply it to people who have already used the system, ideally right after use (TeaCup Lab). Keep the 10 items and their order: standardization is what allows comparison with other systems or with the same system over time.
- It measures **perceived** usability, which can differ from actual usability (e.g. someone believes they completed a purchase while the last step was missing). It does not say which problems exist or why: combine it with tests or interviews.
- Small sample = wide margin of error. Report n and range.
- Useful at different stages (prototype, final product, post-launch) for benchmarking and tracking (UXABLES).
- Methodological note: SUS uses agree/disagree, which Qualtrics discourages in general surveys because of acquiescence bias; in SUS this is mitigated by alternating positive and negative items.

## Additional context (thestory.is, partial summary)
- SUS is based on a 5-point Likert scale (Rensis Likert, 1932). Its 10 English items match the version above.
- Alternatives or complements cited: SUMI, SUPR-Q and QUIS; none covers every usability problem, each measures from one perspective. That source gives no criterion for choosing among them: consult a specific source.
- Usability is not the same as UX: usability (learnability, efficiency, memorability, errors, satisfaction) is part of the experience, which also includes usefulness, desirability and brand. A good SUS says nothing about usefulness or desirability.
- The source was truncated before its sections on advantages, disadvantages and sample size: nothing on those was taken from it.

## Scoring without errors
Three of 27 SUS datasets reviewed by Sauro and Lewis were miscoded (second-hand figure via a skills catalog; verify the original work before citing). Use `scripts/scales.py sus` to score and detect suspicious responses, and `scripts/scales.py standard` to check that the questionnaire keeps the wording. Comparison with UMUX-Lite, SEQ, NPS: `references/standard-scales.md`.
