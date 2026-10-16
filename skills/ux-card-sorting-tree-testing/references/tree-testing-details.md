# Tree testing: operational detail

## Contents
1. Prepare the tree
2. Task types
3. Writing tasks
4. Sample, qualitative vs quantitative
5. Metrics and thresholds (with discrepancies)
6. Limitations
7. Combined IA recipe

## 1. Prepare the tree
- Include the whole global navigation level (and utility navigation if applicable), down to the lowest level where the resources you will ask about live (NN/g).
- Build it in a spreadsheet: home page in A1, levels going right, ONE category per row, and paste it into the tool (NN/g).
- Define the correct answer(s) for each task before launching, so success is calculated automatically.
- Modeling tip: you do not need to test two trees to compare placements (e.g. tomato under Fruits vs Vegetables): in a single tree you see how many clicked each. Use several trees only to compare LABELS, and then use a between-subjects design (each person sees only one version) (NN/g).

## 2. Task types (NN/g)
- Finding key business resources.
- "Sleight-of-hand": look for something uncommon to evaluate the information scent of the parent category (e.g. a company benefit to test the names in the HR area).
- Problem areas: categories proposed by stakeholders or with much disagreement in the card sort.
- Comparing alternative labels or placements.
- An easy warm-up task at the start: it serves as practice and, in unmoderated studies, to filter out inattentive people (if they fail the easy one, they probably did not read).

## 3. Writing tasks
Examples adapted from the New Mexico government case (NN/g), for the category "Starting a business":
- Bad: "Find information about starting a business" (repeats the label and gives away the answer).
- Bad: a long story with many details (people do not read and get distracted).
- Good: "You're thinking of opening a gardening service. See if there are resources that help you get started" (short scenario, without the keyword).
Rules: avoid tree terms, keep it brief, with motivation, random order, and a pilot to catch ambiguous tasks. Automatic clue check: `scripts/check_study.py --tasks tasks.txt --tree tree.txt`.

## 4. Sample, qualitative vs quantitative
- Qualitative: few participants, better moderated (the facilitator probes); good for iterating quickly at the start; NOT for statistics (NN/g).
- Quantitative: more sample; measures rates and times and lets you compare IA options (NN/g gives no number).
- Maze: at least 50 participants per user group (more if the tree is large or the base diverse). An earlier version of this skill said 30+: they are heuristics; state which you use and note that recruiting quality matters as much as quantity.
- NN/g recommends starting the quantitative study with a qualitative pilot: it validates tasks without bias and explains the why of the choices.
- If unmoderated, add a follow-up survey: mark difficult labels + an open question (NN/g).

## 5. Metrics and thresholds
- Success: % who reach the correct answer. Directness: went straight without wandering between categories (indicates label clarity). Time. First click: getting the first one right is associated with more success (Maze). Paths chosen by those who fail.
- Also check whether a category should be in two places (e.g. socks under footwear and accessories) (NN/g).
- Thresholds: Maze cites as a reference attributed to NN/g: 60-80% good, 80-90% very good, over 90% excellent. This figure could not be verified in the NN/g article read (it gives no numbers). The script uses its own, stricter scale (under 50 critical, 50-75 review, over 80 good). Always cite the source and do not treat them as a standard: they depend on the task (a hard or rare task tolerates less).
- With megamenus, focus on whether they pick the right first-level category, not just final success (NN/g).
- With few participants use the confidence interval the script prints: 3 of 4 successes is "75%" but the CI runs from ~30 to ~95%.

## 6. Limitations (NN/g)
- No context or comments in unmoderated mode.
- Most tools only accept leaves (lowest level) as the correct answer; on real sites a parent is sometimes a valid destination.
- No visual design or content: a megamenu shows subcategories at once and the tree test does not capture it.
- It does not measure visual usability or the real interaction; follow with a prototype.

## 7. Combined IA recipe
- NN/g: usability test of the current site (with finding tasks) -> card sorting to generate options -> tree test to choose the base hierarchy before writing content or designing.
- IxDF: if the current IA has problems, start with a tree test, then an open card sort, and repeat the tree test with similar tasks to compare against the original.
- Maze: tree test after defining the IA and before the high-fidelity prototype; combine it with first-click and, after implementing, with live A/B.
- Terminology: "reverse card sorting" is another name for tree testing (Maze, IxDF, NN/g), although Maze/UXtweak insist they are not equivalent.
