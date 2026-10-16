# Standard scales: which one to use and what you can (and cannot) claim

Read this when someone asks "should I use SUS, SEQ, NPS...?", when UMUX-Lite or SEQ must be scored, or before comparing a result with a benchmark. Scripts: `scripts/scales.py` (see `--help`). Verified against MeasuringU pages on 2026-10-14.

## Which one to choose
| Scale | What it measures | When | Items / scale | What it does NOT tell you |
|---|---|---|---|---|
| **SUS** | Perceived usability of a whole system | After using it for a while (prototype, product, post-launch); benchmarking and tracking | 10 items, 1-5 | What to fix or why |
| **UMUX-Lite** | Perceived usability, minimal version (capabilities + ease) | When 10 items do not fit; quick tracking | 2 items, 7 points (original, Lewis et al.) | Detail; coarser than SUS |
| **SEQ** | Perceived difficulty of **one task** | Immediately after each task in a usability test (`ux-usability-testing`) | 1 item, 7 points | State of the whole system |
| **NPS** | Stated willingness to recommend | Tracking the relationship with the brand/product | 1 item, 0-10 | Usability; people predict their behavior poorly |
| **CSAT** | Satisfaction with a specific interaction | After a purchase, ticket or delivery | 1 item, satisfaction scale | Causes or future use |
| **CES** | Perceived effort to get something done | After support or a transaction | 1 item, agree/effort scale | Quality of the offering |
The CSAT and CES definitions are general and have no specific source in this skill: check the exact wording of the tool you use. Task -> SEQ; system -> SUS (or UMUX-Lite if you must save items); relationship -> NPS; interaction -> CSAT/CES.

## Golden rules
1. **Do not change the wording or the scale points** if you want to compare with a benchmark: any change breaks comparability. Run `scales.py standard`.
2. A wrongly computed score still gives a plausible number between 0 and 100: nothing warns you. Sauro and Lewis reviewed 27 SUS datasets and found 3 miscoded (second-hand figure from a skills catalog by Great Question; not verified in the original work). So score with a script and document how reversed items were coded.
3. Report n, the scale used and which benchmark you compare against. With small n the margin is wide.
4. These scales measure what is perceived, not what happened in the task: cross them with success/time/errors.

## SUS
Formula, items and interpretation frameworks: `references/sus.md`. Reference average 68 (MeasuringU: 500 studies). The script's consistency checks are **our heuristics, not a published standard**:
- Identical answers on all 10 items: the questionnaire alternates positive and negative items, so "all 3" or "all 5" suggests automatic answering (or a coding error). Nine or more identical answers out of ten are flagged as possible straight-lining.
- Positive/negative pairs that measure almost the same thing (3-8, 2-3, 7-10, 4-7, 3-4) answered on the same side in a marked way (both >= 4 or both <= 2) in 2 or more pairs.
Flag, review the case (coding failure? distracted participant?) and report the score with and without those rows; never delete silently.

## UMUX-Lite
- Items (Lewis et al., per MeasuringU): "[This system's] capabilities meet my requirements" and "[This system] is easy to use". Original on a 7-point agree scale; MeasuringU uses 5 points to lean on its SUS norms, with an equation variant its page does not detail: the script **scores 7 points only**.
- Raw 0-100 = (item1 + item2 - 2) x 100/12.
- SUS-equivalent (Lewis et al. regression) = 0.65 x raw + 22.9. MeasuringU states more research is needed to confirm and refine it.
- Evidence cited by MeasuringU: alpha .86 (SUS .91), correlation with SUS r = .83 and with NPS r = .72; the regression predicted SUS with about 99% accuracy on a separate dataset.
- **Pending / unverified**: cutoffs or grades for UMUX-Lite (MeasuringU gives none; it converts to z-scores and percentiles and uses a "common threshold of 4" per item for a usability x usefulness quadrant) and the 5-point variant. Do not invent thresholds: compare against your own baseline.

## SEQ
- Wording (MeasuringU): "Overall, how difficult or easy was the task to complete?", 1 to 7 (usually only endpoints labeled), immediately after attempting the task.
- Historical average: between 5.3 and 5.6 over 400+ tasks and 10,000+ users, updated in 2019 (above the nominal midpoint of 4, typical for 7-point scales).
- Formal cutoffs: **none** in the source. The source's own rule of thumb: if the answer is below 5, briefly ask what made it hard. Compare task to task and round to round, not against an absolute number.

## NPS
% promoters (9-10) minus % detractors (0-6) (Drive Research). Unstable with few answers; if you change the scale, do not compare with benchmarks. NPS benchmark figures: not included for lack of a verified source.
