# Cycle: card sort -> tree -> tree test -> adjust

Read this when you must build or redesign a structure and want a process with a stop criterion. Basis: NN/g recommends an open card sort and then a tree test; IxDF proposes, if the current IA fails, measuring first with a tree test (baseline), then a card sort, and repeating the tree test with similar tasks (see `sources.md`). The stop criterion and the round cap are our own practice.

## The cycle
1. **Baseline (if a site already exists)**: tree test of the current tree with 5-10 real tasks. Keep success, directness and where the people who failed went.
2. **Open card sort**: how do they group and name? (`quick-synthesis.md` or `scripts/cardsort_matrix.py`).
3. **Candidate tree**: turn the agreed groups into a hierarchy of labels, one to three levels. Decide which problem cards are duplicated (cross-link) and which are renamed. If there are two proposals, build two trees.
4. **Tree test**: same tasks as the baseline (or similar), with the correct answer defined beforehand. See `scripts/tree_test_summary.py`.
5. **Read the failures**: which wrong path did they choose? which label attracted them? which task had the lowest success? Each failure points to a change: rename, move or duplicate.
6. **Adjust and repeat** only what changed, with new participants (anyone who saw the tree has learned where things are).
7. **Stop** when the criteria you set *beforehand* are met (our example: every critical task passes the agreed threshold and no dominant wrong path appears) or when you must decide by a deadline; document the remaining risk.

## Rules
- One variable per round: if you change everything at once you do not know what improved.
- If you compare two trees with the same tasks, assign each participant to a single tree (between-subjects).
- Combine it with a usability test of the final design: the tree does not measure the visual interface (`ux-usability-testing`).
- Set a round cap (for example, three) to avoid iterating forever.
