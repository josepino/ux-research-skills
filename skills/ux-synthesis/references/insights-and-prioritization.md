# Findings vs insights, insight quality and prioritization (detail)

Read when you need to write insights, check whether something is really an insight, prioritize findings, resolve contradictions or combine sources.

## Contents
1. Data -> finding -> insight
2. Quality tests for an insight
3. Template
4. Triangulation and cross-source reading
5. Contradictions
6. Prioritizing findings
7. What this is NOT: prioritizing research projects
8. Structure of a written synthesis

## 1. Data -> finding -> insight
- **Data**: unanalyzed observations (quotes, clicks, notes, survey answers). Can be qualitative or quantitative.
- **Finding**: a pattern across comparable data, stating what happened but not why. Qualitative -> thematic analysis; quantitative -> statistics. E.g. NPS = 40 with a margin of error of 10 (NN/g).
- **Insight**: an explanation of the pattern with context (prior research, business goals) that identifies an actionable opportunity. Not prescriptive: it narrows the design space so you can then test (NN/g).
- NN/g example: NPS rose after a redesign, but the difference was not significant (confidence intervals overlapped) and tests showed medical jargon and poor information scent -> recommend plain language.
- Lyssna example table: "65% abandoned at payment" (finding) vs "they abandon because the form creates security anxiety -> trust signals" (insight).
- Mind the definitions: NN/g calls "finding" what summarizes data and considers it context-free; Uism says a finding is a verifiable observation and the insight reveals an uncovered motivation, tension or need. They are compatible, but in the report fix one definition and keep it.

## 2. Quality tests
- The **"so what?"** test (Lyssna): if the answer only repeats the observation, dig deeper until you reach the need or motivation.
- Four questions (Uism): does it go beyond describing? Does it reveal a tension (e.g. security vs low friction)? Does it feel recognizably true to stakeholders? Does it guide an action?
- Six questions (Lyssna): is it new? Is it relevant to the project? Is it backed by data? Does it inspire direct action? Does it offer a fresh perspective? Is it simple to understand?
- Dovetail: reliable, understandable, user-centered, communicated and actionable insights (short sentences pointing to problem and solution).
- An insight is not a guess: it connects patterns from several data points and picks the explanation that covers them best (Uism). Validate against the raw data (Looppanel).

## 3. Template
`[Who/segment] + [does/feels X] + because + [motivation/need/tension] -> [opportunity/implication]` and then the evidence ("n of N", quote with ID, metric). Own example based on Uism: "People who cook with ready-made food add something fresh because they want to feel they care, without giving up speed -> how might we make convenient feel more caring?".

## 4. Triangulation and cross-source reading
- Triangulation (NN/g): multiple data sources, multiple analysis approaches and multiple analysts reduce one person's bias. Matrix and procedure: `triangulation-across-methods.md`.
- Dovetail: synthesizing different sources (surveys, tests, A/B, analytics, call-center notes, social comments, diaries) validates and reveals correlations; e.g. several comments say "slow", analytics shows *where*.
- Quantitative = what/how much; qualitative = why. Useful sequence: metric (60% abandonment) -> interview/survey aimed at those who abandoned (Uxcel, Contentsquare, Maze).
- Quantitative techniques the team may need (Uxcel): cross-tabulation, max-diff, conjoint, gap analysis, trend analysis, sentiment analysis. For quantitative usability metrics NN/g mentions samples of around 35 participants or more; do not use that size as a rule for qualitative studies.

## 5. Contradictions
- Between sources: cross-validate and review each source's context (Dovetail).
- Between say and do: a signal to investigate (Uxcel).
- Before discarding: different segments? Same task and conditions? Moderator influence? Analysis error?
- Do not report a contradiction as "noise" without having looked at the segment or context.

## 6. Prioritizing findings
- Anchor to the study objective: map each finding to an objective; if it connects to none, consider a separate study (Uxcel). E.g. in a yoga app whose objective is understanding why people drop out after week 1, "long, rigid sessions" is a priority and "I want meditation" is valuable but secondary.
- Criteria (Entropik, Looppanel, Dovetail): **severity** (does it prevent completing the task or just add friction?), **frequency** (how many users), **impact on business goals** (retention, conversion, support costs), **effort**. The greater the effort, the greater the impact needed to justify it.
- Impact/effort quadrant: high impact + low effort first (e.g. change a confusing CTA before redesigning the page). Discuss with product and design representatives: they estimate effort.
- Eisenhower (urgent/important) remains a valid frame; severity x frequency / effort is one way to make it operational. The script `scripts/analyze_notes.py` computes an example score (our own heuristic, not a standard from the sources).
- Dot voting for clusters if there is no consensus (NN/g).
- Stakeholders have different priorities (product, engineering); look for findings that unify objectives while keeping the user at the center (Entropik).

## 7. Prioritizing research projects (a different level)
UXinsight (Backbase) proposes criteria for choosing *which studies to run*: the team's willingness to change its mind, clarity of the decision to make, stakeholder alignment, cost/value ratio, timing of the need, exploratory/evaluative balance, and warning signs (a team that did not act on previous studies, low commitment, no time to act on the result). This belongs more to `ux-research-plan` / `ux-research-ops` than to this synthesis.

## 8. Structure of a written synthesis (Looppanel)
Executive summary -> context -> methodology -> findings/insights (most important first) -> recommendations (quick wins and strategic) -> appendices. Each insight with evidence (quote, metric, observation), business implication and a prioritized recommendation. Afterwards: ideation, roadmap, follow-up study and impact measurement. Example from the source: 20 interviews + usage by 1,000 users -> 15/20 frustrated with delivery times and 40% abandon after using search -> two distinct insights, each with its recommendation.
