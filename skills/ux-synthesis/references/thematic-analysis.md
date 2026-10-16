# Thematic analysis and coding (detail)

Read when you need to code transcripts/notes/open-ended answers, build a codebook, or decide whether thematic analysis is the right method. Sources in `sources.md`.

## Contents
1. When to use thematic analysis and when not
2. Inductive vs deductive (and the mixed approach)
3. Code types and naming convention
4. A useful codebook with examples and non-examples
5. How to know if something is a pattern
6. Consistency, bias and reflexivity
7. Time budget
8. Analyzing behavioral vs attitudinal data
9. Classic phases and the dashboards case (Toptal)

## 1. When yes and when no
- Yes: many transcripts/notes, open-ended survey answers, diaries, recordings of think-aloud tests, or to explain the "why" behind a metric (e.g. interview people who did not convert to understand a drop).
- No (or with caution), according to Maze: (a) a **very small sample** (fewer than 5-6 people per user group): treat each session as a case instead of forcing themes; (b) a **mainly quantitative** study (task success, conversion, satisfaction, how widespread a problem is): use quantitative methods; (c) if all that matters is **counting how many times** a word or theme appears, content analysis fits better.
- Isolated individual feedback (a lone comment from one person) is hard to turn into a pattern: a warning from a practitioner quoted by Maze.
- Other qualitative methods (to mention, not to apply by default): content analysis (frequency of themes/words), narrative (individual stories, useful for diaries), grounded theory, discourse analysis. Choose by objective and volume; the same dataset can give different design answers depending on the method (Uxcel).

## 2. Inductive vs deductive
| | Inductive | Deductive |
|---|---|---|
| Where themes come from | The data (bottom-up) | Hypotheses, a framework or prior studies |
| Use for | Exploring a new problem, discovering needs, the user's vocabulary | Validating assumptions, comparing against product pillars/JTBD, comparing studies over time |
| Risk | Scatters if there are no clear research questions | Forces data into prior boxes and misses the unexpected or contradictory |
- Mixed option (Contentsquare, Looppanel): start with a few codes derived from the research questions and leave room to create new codes while reading.
- **Reflexive thematic analysis** (inductive variant, per Maze): reread several times, code flexibly, and pause periodically to ask whether the themes reflect the data or your own biases. Themes are constructed, they do not "emerge" on their own.

## 3. Code types and names (Looppanel)
- Descriptive (topic: "navigation", "error message"), process (actions: "workaround", "abandons task"), emotion ("frustration", "confusion").
- Hierarchical: parent > child (Navigation > menu / search / breadcrumbs).
- Optional prefixes to sort: `BEHAVIOR_`, `EMOTION_`, `NEED_` (the source uses BEH_/FEEL_/NEED_).
- Specific but not hyper-fragmented: "payment error" is more useful than "error", but hundreds of codes overwhelm. Merging, deleting and renaming codes as you go is normal.
- Think up codes **before fieldwork** (Uxcel): derive them from objectives/hypotheses (e.g. testing a landing page: navigation, aesthetics, critical errors, recommendations). Findings outside the list are often the most valuable: do not ignore them.

## 4. A useful codebook
Columns: code | definition | **example** | **non-example** | who created it/date. Non-examples (Contentsquare) are what most helps two people code the same way. Keep it alive in the same file as the analysis.

Simple analysis table (Contentsquare, a PM case): one row per independent idea, columns for participant, quote, code; a 3-line summary at the end of each interview (positives, pains, opportunities); only afterwards themes and patterns. To automate this step from a CSV, see `scripts/analyze_notes.py`.

## 5. Is it a pattern?
Three checks (Looppanel): **repetition** (appears several times), **consistency** (across user types/scenarios) and **impact** (how much it affects). A pattern is not always a majority: a minority theme with high impact (blocks the task) deserves attention. In affinity, do not discard a small cluster just because it has few notes (NN/g). The numeric threshold is in `pattern-threshold.md`.

## 6. Consistency, bias and reflexivity
- A second person who evaluates codes and themes (Contentsquare, Uxcel, Looppanel). If the whole team agrees on everything without debate, suspect bias rather than real consensus (Uxcel).
- Write assumptions and hypotheses **before** fieldwork and revisit them when analyzing (Uxcel).
- Reflexive journal (Contentsquare): what prior ideas do I have about the topic? Which decisions were hard and why?
- Confirmation bias (looking only for what confirms) and the Hawthorne/observation effect (people change behavior when they feel observed). Triangulation (NN/g): several data sources, several approaches and several people analyzing.
- Binary positive/negative sentiment = over-reduction (Uxcel): loses nuance; use it only as orientation.

## 7. Time
Contentsquare rule of thumb: reserve at least as much analysis time as collection time (10 h of interviews -> at least 10 h of analysis). Summarizing each interview right after it ends avoids accumulating debt (Contentsquare, Looppanel: 10-15 min of note cleanup after each session). It is an empirical rule from one source, not a standard.

## 8. Behavioral vs attitudinal data (Uxcel)
- Attitudinal (interviews, diaries): code -> themes. What people say can differ from what they do: **the say/do gap is a signal to investigate, not noise**.
- Behavioral (sessions, recordings, analytics): look for anomalies (unexpected clicks, ignored features, rage clicks) and code actions ("skipped onboarding", "used search instead of navigation").
- Behavioral data says what happened, not why: follow up with an interview or short survey of those who dropped off.
- Example: "70% abandon at the same point" + "they say it's confusing" = actionable finding.

## 9. Classic phases and the dashboards case (Toptal)
Partial summary of a Toptal blog post (truncated at "defining themes"). Useful to order the process; the rules in sections 1-8 prevail.
**Six phases**: (1) familiarize yourself with the data (read and reread, transcribe or split into fragments; impressions, not conclusions); (2) generate initial codes (fragments that answer the study questions, moved to a sheet); (3) search for themes (patterns of codes related to the question; this is where most time goes); (4) review themes; (5) define and document themes, ideally with a **thematic map** showing relationships and the overall narrative; (6) deliverable.
- **Questions to review themes**: do they make sense against the research question? Are they concrete or too general? Do they overlap? Is a theme missing? Do not accept the first grouping.
- **Simple coding sheet**: columns Participant / Codes / Themes, rows by theme, sentence or natural pause, including non-verbal observations. With little data, the final themes may already emerge at review.
- **Coding is subjective**: "I'm juggling a lot of things" can be coded as time management, "busy" or "overwhelmed". Record the choice and, if it matters, cross-check with another person (see section 6).
- **Example of themes**: in a study of analytics dashboards nobody used, interviews produced four themes (personalization, data use, data stories and the current product); similar codes such as "improvements", "changes" and "personalization" were merged into "personalization". It is an illustrative single-source case.
- **Deliverable**: concise, logical, without repetition and telling a story; with recommendations backed by examples from the data, and with the original data, codes and themes at hand to show how the conclusion was reached.
- Difference of emphasis: Toptal proposes waiting until phase 3 to group; affinity practice (`affinity-step-by-step.md`) groups notes from the start. They are compatible depending on volume and method.
