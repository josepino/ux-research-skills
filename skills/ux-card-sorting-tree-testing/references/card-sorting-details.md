# Card sorting: operational detail

## Contents
1. Number of cards and participants (sources disagree)
2. Instruction template
3. Closing questions
4. Manual analysis step by step (no tool)
5. Agreement thresholds
6. Edge cases and common mistakes
7. Qualitative and quantitative data, and how to report (Toptal)

## 1. Number of cards and participants
Sources disagree; choose according to the case and state the range used:

| Topic | NN/g | Lyssna | Uxcel | Secret Stache | Maze |
|---|---|---|---|---|---|
| Cards | 30-50 | 30-40 (fewer than 30 gives little data; more than 50 tires) | 30-60 | 40-80 | - |
| Participants, qualitative | at least 15 | 15-30 | - | - | 15-30 |
| Participants, quantitative | 30-50 | - | - | - | 30+ |

Toptal (secondary summary) adds another range: 30-70 cards and 15-30 participants, noting that beyond ~30 participants the picture does not improve substantially in card sorting (different from NN/g's quantitative 30-50; they are different approaches: state which one you use).

- Dovetail suggests 10-15 users as a "representative" minimum and a time limit of 5 to 30 min; Uxcel suggests 15-20 min sessions (+5 if they did not finish).
- NN/g warns: with more than 50 cards people tire and dump everything into one "Misc" group; it is not known whether that is confusion or fatigue. If you have more content, split into several studies or sample.
- More participants never hurt; the numbers are about budget. If you see no patterns, recruit more.
- Pilot: first with the team and then with 3-5 outside people (Lyssna); NN/g also recommends a pilot to validate quantity and label clarity.

## 2. Instruction template (adapted from NN/g)
"Thank you for taking part. It will take about [X] minutes. You will organize cards into groups according to the similarities you see. There are no right or wrong ways. You can think aloud.
1) Look at all the cards. 2) Make groups that make sense to you: they can be different sizes, there is no ideal number, and you can rearrange whenever you like. 3) If you do not understand a card, set it aside instead of putting it in a group at random. 4) At the end, give each group a name."
- Group names are requested AFTER grouping, so as not to condition the sorting.
- In unmoderated studies, the instructions are all you have: be extra clear (UXtweak).
(Translate the template to the participants' language.)

## 3. Closing questions (NN/g, Uxcel)
- Which cards were especially easy or hard to place?
- Could any go in two or more groups?
- Why did you leave these ungrouped?
- Scale 1 (very easy) to 5 (very hard): how easy was it to group?
- Moderated: "I saw you put X in Z, can you tell me why?"
- Even if the study is quantitative and unmoderated, run a few moderated sessions: they explain why a card was hard (unclear label vs unrelated topic).

## 4. Manual analysis step by step
Combines Maze, UXtweak/Banus and UXmatters:
1. Eyeball: groups that repeat, overused categories (too broad), cards that appear in several categories (need multiple access).
2. Clean: move paper results into a spreadsheet (participant, card, category, notes); exclude participants who abandoned. Many incompletes = confusing study.
3. Standardize category names in open/hybrid ("Contact" = "Contact us"; "Plans" = "Pricing") and do not take categories created by only one person.
4. Matrix: rows = cards, columns = common categories, cells = % of participants. Use colors to read better.
5. Discard low percentages (UXmatters used 10% to show only the substantial; UXtweak/Banus recommends deleting what is under 50% and reordering).
6. Reorder cards under their most-voted category and look at the distribution: what is the split between groups?
7. Decide: where to place, where to cross-link, where to duplicate, which label to change. An even split between two groups = confusing label, repeated content or need for double access.
Automatic tools give: similarity matrix (pairs), standardized agreement/grouping matrix (card x category), dendrogram, popular placements matrix (closed) and participant-centered analysis (detects segments with different strategies, UXtweak).
Script: `python3 scripts/cardsort_matrix.py data.csv --agreement`. No-tool version for small studies: `references/quick-synthesis.md`.

## 5. Agreement thresholds
- Lyssna: 80% or more = strong link, groupable; 60-80% = moderate, validate; under 60% = no consensus (clarify labels or accept the ambiguity).
- UXtweak/Banus: cut at 50% for manual analysis.
- They are tool heuristics, not laws. With a small sample (15), 60% is only 9 people.

## 6. Edge cases and common mistakes
- Repeated words in cards ("Toyota Camry", "Toyota Matrix") make people group by the word (NN/g, Lyssna).
- Card sorting gives a single layer: it does not validate hierarchies or paths. With paper you can build subgroups if you let people; many online tools do not (UXmatters, NN/g).
- The names participants propose are not your final labels: they lack the site's context (NN/g). And an "Other" category coming out of the sort is avoided by people in a real menu (NN/g).
- Card sorting is content-centered, not task-centered: it does not tell you whether the structure works (IxDF, User Interviews). That is why it is validated with a tree test.
- IxDF advises against using it as the only input to build an IA from scratch: results are inconsistent. Use it as an input, not a verdict.
- Team sorting (Donna Spencer via User Interviews): the discussion among participants can be worth more than the result, but there is a risk that one person dominates (groupthink).
- Modified-Delphi (IxDF): each participant starts from the previous one's structure and refines it; useful to converge on consensus.
- Paper: allows special populations (children, accessibility per NN/g), seeing body language and building subgroups. Online: fast, cheap, many participants but without seeing the interaction or asking (UXtweak).
- Two user groups (e.g. customers vs. administrators) may have different models: analyze by segment.
- Presenting to stakeholders: a dendrogram is hard to explain; a percentage matrix in a colored spreadsheet worked better (UXmatters).

## 7. Qualitative and quantitative data, and how to report (Toptal)
Partial summary of a Toptal blog; no new findings on the method, only practical nuances.
- Thinking aloud while sorting gives the *why* of each association; ask for group names only at the end (matches section 2) and clarify they reflect how people sort, not necessarily the final label.
- Keep everything in digital format per participant (categories, notes, recordings) so no information is lost.
- Separate the qualitative (why, comments) from the quantitative (how often two cards go together, how many people created the same category name); review notes and recordings of everyone to detect unexpected themes.
- With similarity matrices and dendrograms from tools, beware of conclusions the data do not support (see sections 5 and 6).
- Report: simple, with context notes for people who are not researchers (see section 6 on presenting to stakeholders).
- Terminology: Toptal calls the tree test a "reverse card sort" (given categories, navigated top-down); elsewhere in this skill it is treated as its own method.
