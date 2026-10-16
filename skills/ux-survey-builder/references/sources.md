# Sources used (ux-survey-builder)

Pages read for this skill. Everything is paraphrased; figures from commercial blogs are indicative.

## SUS / metrics
- TeaCup Lab, "What is the SUS scale and how to use it" (Spanish) - https://www.teacuplab.com/es/blog/que-es-la-escala-sus-y-como-usarla-para-medir-la-usabilidad/ - formula, average 68, Sauro A-F grades, acceptability >70/<50, limits (perceived usability, sample). Improved: `sus.md`, `scripts/sus_score.py`.
- UXABLES, "Measure with the System Usability Scale (SUS)" (Spanish) - https://www.uxables.com/investigacion-ux/medir-con-el-sistema-de-escala-de-usabilidad-sus/ - adjective scale, [system/feature/product] placeholder, stages of use. Improved: `sus.md` (discrepancies).
- Drive Research, "Survey Scales: Choosing Between Large and Small Options" - https://www.driveresearch.com/market-research-company-blog/are-you-using-unbalanced-scales-stop-now-please/ - scale size, NPS definition. Improved: scales section, `nps`.

## Length and design
- SurveyMonkey, "How long should a survey be?" - https://www.surveymonkey.com/curiosity/survey_completion_times/ - time per question, drop-off from 7-8 min. Improved: Mode A step 4 and `design-and-bias.md` section 2.
- SurveySensum, "How long should a survey be" - https://www.surveysensum.com/blog/how-long-should-a-survey-be - abandonment in long surveys, shortening tactics (secondary figures).
- Maze, "How to write concise, bias-free UX survey questions" - https://maze.co/guides/ux-surveys/questions/ - 10-15 questions, <10 min, types, option limit, A/B of questions.
- Qualtrics, "How to create an effective survey" - https://www.qualtrics.com/blog/how-to-create-a-survey/ - 15 tips: grids, acquiescence, scales, order, pilot with 5 people.
- UX Mastery, "Better User Research Through Surveys" - https://uxmastery.com/better-user-research-through-surveys/ - logical flow, "don't know", overlaps, pilot and staged launch.
- User Interviews, "Surveys for UX Research" - https://www.userinterviews.com/ux-research-field-guide-chapter/surveys - Erika Hall, Caroline Jarrett's crucial question, wording. (Text truncated midway; later parts missing.)
- Contentsquare, "How to create a UX survey" - https://contentsquare.com/guides/ux/surveys/ - confirmation/framing, cool-off, in-site surveys.
- Typeform, "Types of survey questions" - https://www.typeform.com/blog/tips/types-of-questions/ - 12 types, limits (matrix, ranking), LLM-in-open-answers figure.
- Typeform, "UX survey questions: 41 examples" - https://www.typeform.com/blog/tips/user-experience-survey-questions - UX statements by category (item seeds). (Forrester ROI figures were not used.)

## Bias and leading questions
- UXtweak, "Survey response bias" - https://blog.uxtweak.com/survey-response-bias/ - acquiescence, social desirability, recency, extremes.
- UXtweak, "What are leading questions in UX?" - https://blog.uxtweak.com/what-are-leading-questions-in-ux/ - examples and rewrites.
- UserTesting, "How to avoid leading questions" - https://www.usertesting.com/blog/leading-questions-in-ux - good/leading examples, non-verbal language.
- Qualtrics, "Question order bias" - https://www.qualtrics.com/blog/biased-data-is-bad-data-how-to-think-about-question-order/ - randomizing by blocks and limits.
- SurveyMonkey, "Sampling bias" - https://www.surveymonkey.com/market-research/resources/sampling-bias/ - types of sampling bias.
- MeasuringU (Sauro), "7 S's of user research sampling" - https://measuringu.com/sampling-s/ - sampling strategies.
- User Interviews, "Bias in UX research" - https://www.userinterviews.com/blog/how-to-reduce-bias-in-ux-research - reducing (not eliminating) researcher bias.

## Open questions and analysis
- Qualtrics, "Open-ended questions" - https://www.qualtrics.com/experience-management/research/open-ended-questions/ - 8 common mistakes, maximum ~5 open questions.
- SmartSurvey, "How to analyse open ended questions" - https://www.smartsurvey.co.uk/blog/how-to-analyse-open-ended-questions - clean and code.

## Incentives and screeners
- HubSpot, "Survey incentives" - https://blog.hubspot.com/service/survey-incentives - when not to use, 5 steps, types (impact figures as order of magnitude).
- Survicate, "Survey incentive ideas" - https://survicate.com/blog/survey-incentive-ideas/ - 10-30%, B2B vs B2C, guaranteed vs draw.
- Lyssna, "Incentives for research participants" - https://www.lyssna.com/blog/incentives-for-research-participants/ - amounts per format (2026).
- User Interviews, "Guide to research incentives" - https://www.userinterviews.com/blog/the-ultimate-guide-to-user-research-incentives - USD 60-100/hour, no-shows (25,000+ sessions).
- Tremendous, "Research incentive programs" - https://www.tremendous.com/blog/research-incentive-programs/ - immediacy, integrity risks, reward range, taxation.
- Vantage Circle, "Survey incentives" - https://www.vantagecircle.com/en/blog/survey-incentives/ - table by duration (internal surveys), satisficing.
- Lyssna, "Screener survey" - https://www.lyssna.com/blog/screener-survey/ ; Participant Kit (formerly Consent Kit) - https://consentkit.com/ux-research-screener ; PlaytestCloud - https://start.playtestcloud.com/blog/the-art-of-player-recruitment - screener criteria and design.

## Second pass (text retrieved via browser, summary; partial)
- thestory.is, "System Usability Scale (SUS) - What is it? Why is it worth using it?" - https://thestory.is/en/journal/system-usability-scale-what-is-it/ - Likert 1932, English items, alternatives SUMI/SUPR-Q/QUIS, usability vs UX, corroborates 1986/John Brooke. Improved: `sus.md`. Truncated before calculation, advantages and sample.
- Alchemer, "Best Practices for Ordering Survey Questions" - https://www.alchemer.com/resources/blog/survey-question-order/ - assimilation/contrast, carry-over, option order, randomization, culture and extreme responding. Improved: `design-and-bias.md` section 11. Vendor blog; truncated in the pretest section.

## Reviewed with no contribution
- https://maze.co/blog/leading-questions/ - downloaded empty/unusable.
- https://www.voxco.com/blog/how-to-prevent-question-order-bias-in-surveys/ - the URL now shows an AI blog, not order bias.
- https://www.hubble.team/guide/ux-research-101-guide-to-surveys - menu/footer only.
- Tool home pages (LimeSurvey community, SurveyMonkey, Typeform and its product research template) - no methodological content.
- Infobae note on the OkCupid experiments (2014) - tangential (ethics).

## Standard scales (verified on the web on 2026-10-14)
- MeasuringU, "Measuring Usability: From the SUS to the UMUX-Lite" - https://measuringu.com/umux-lite/ - UMUX-Lite items, original 7-point scale, raw score, regression 0.65 x ... + 22.9 (Lewis et al.), alpha .86 (SUS .91), r = .83 with SUS, r = .72 with NPS, ~99% accuracy predicting SUS; no published grades (z-scores/percentiles and a "common threshold of 4" per item). Improved: `standard-scales.md`, `scales.py umux`.
- MeasuringU, "10 Things To Know About The Single Ease Question (SEQ)" - https://measuringu.com/seq10/ - wording, 7 points, average 5.3-5.6 (400+ tasks, 10,000+ users, updated May 2019), probe when below 5, no formal cutoffs. Improved: `standard-scales.md`, `scales.py seq`.
- MeasuringU, "Measuring Usability with the System Usability Scale (SUS)" - https://measuringu.com/sus/ - average 68 in 500 studies, A > 80.3, F < 51, formula. Improved: `sus.md`.
- Great Question, catalog of 26 skills, #24 "Instrument scorer" (external content read as data; second-hand) - Sauro and Lewis figure: 3 of 27 SUS datasets miscoded. Not verified in the original work; labeled as second-hand.
- The SUS consistency checks (identical answers, straight-lining, contradictory pairs) are **our heuristic**, with no source.
- Pending: UMUX-Lite cutoffs; the 5-point variant; official CSAT and CES definitions (no source cited).
