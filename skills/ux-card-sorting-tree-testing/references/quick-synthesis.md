# Quick synthesis of a small card sort, with no tool

Read this when you have few participants (5-15) and cards (up to ~40) and want a result today with a spreadsheet. It is a simplified version of the co-occurrence matrix method (see UXmatters and UXtweak in `sources.md`); if you have `scripts/cardsort_matrix.py`, it does steps 3-5 for you.

**When it is NOT enough**: more than ~40 cards or ~30 participants, or if you need a dendrogram: use the script or a tool.

## Steps
1. **Put the data in long format.** One row per card and participant: `participant, group, card` (the same CSV the script uses).
2. **Standardize group names.** Merge "Contact"/"Contact us"/"Get in touch" into one and note the rule in a separate column so it can be reviewed. Do not keep categories created by a single person as separate findings.
3. **Build the co-occurrence matrix.** Rows and columns = cards; each cell = participants who put both cards in the same group. Spreadsheet recipe: sheet "Data" with cards in A2:A41 and one column per participant (B..K) holding the standardized group of that card (give each unsorted card a unique marker such as ?P1, so two unsorted cards do not count as a match). Sheet "Matrix" with the same cards in A2:A41 (same row order as Data) and the card names across row 1 (B1 onward). Cell B2:
   `=SUMPRODUCT(--(Data!$B2:$K2=INDEX(Data!$B$2:$K$41,MATCH(B$1,Data!$A$2:$A$41,0),0)))/COLUMNS(Data!$B2:$K2)`
   and fill right and down. This gives the share of participants directly.
4. **Format as percent** and add conditional color (green >= 80%, yellow 60-80%, none < 60%).
5. **Look for blocks**: reorder rows and columns until green squares appear. Each square is a candidate group. Lyssna reference: >= 80% strong link, 60-80% moderate, < 60% no consensus (UXtweak cuts at 50%). With 8 people, 60% is 5: do not over-interpret.
6. **Spot problem cards**: with no strong link (orphans), or split between two blocks (confusing label, or needs access from two places).
7. **Name the groups** with the names participants used most (count repetitions); avoid "Misc" in the final menu.
8. **Split or merge** to a reasonable group size and write a one-level tree proposal.
9. **Note what is missing**: segments that grouped differently, closing-question comments, and what to validate with a tree test (`iterative-cycle.md`).

## What to deliver
The colored matrix, the proposal of named groups, the list of problem cards and the warning about n.
