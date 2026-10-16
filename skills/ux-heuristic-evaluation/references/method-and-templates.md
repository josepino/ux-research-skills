# Step-by-step method, workbook and templates

## Contents
When it fits · Prepare the team · Document · Scope · Evaluate independently · Consolidate · Spreadsheet template · NN/g workbook · Consolidation script · Complements (cognitive walkthrough, desirability)

## When it fits (and when not)
- It detects obvious problems of an interface (prototypes, physical products, games, virtual reality, voice interfaces), especially early and on a low budget, because it needs no participant recruiting.
- It does not replace research with users: design depends on context. It complements: a heuristic evaluation before a usability test tells you which elements to put to the test.
- It is also good training: practice on products that are not yours to sharpen your eye.
- Other (domain-specific) heuristic sets can be used in addition to Nielsen's 10.

## Prepare the team
1. **3 to 5 independent evaluators** on the same interface: each person, however expert, misses problems (NN/g). If there is only one person (such as Claude evaluating), declare it as a limitation and do not promise full coverage. Details of solo vs panel and the team checklist: `references/panel-vs-solo.md`.
2. Each evaluator reads the 10 heuristics beforehand. If it is the team's first time, do a collective practice round on a simple design (e.g. a weather app) to align expectations.

## Document
Options: NN/g's interactive PDF workbook, a spreadsheet (one observation per row with its heuristic) or a digital whiteboard (Miro/Mural) with a space per evaluator and notes stuck on screenshots.
**Key rule**: nobody sees others' notes until finishing their own; otherwise the independence that gives the method its value is lost.

## Scope
The narrower, the more detailed and manageable. Narrow by: a task, a section, a user group (if very different) and a device type. For the first time or large products, start narrow. Fill in the header: product, user, task, device (e.g. Banana Republic / shoppers / buy a shirt / mobile).

## Evaluate independently
- Reserve about 60 to 120 minutes per evaluator (NN/g: 1-2 hours).
- **Two passes**: first walk through the task only to learn the system, without evaluating. Second pass: look for elements that violate any of the 10 heuristics, and note incident + recommendation under the matching heuristic.
- Example entry: "Product text overlaid on the photos in the listing" (heuristic 8) -> recommendation: solid or semi-transparent background behind the text.
- Not everything that violates a heuristic must be fixed: see "When to break a heuristic" in `heuristics.md`.

## Consolidate
After the individual evaluations, group (affinity diagram) similar problems and discuss: where do we agree and where not? What is most harmful to the experience? What is most problematic for the business? What do we need more data on and what to prioritize in the next usability test? What to do in the short and long term? Doubtful findings or those with very different severities between evaluators go to user testing.

## Spreadsheet template (columns)
One tab per heuristic (plus Intro and Totals), with the columns of the example template (see `sources.md`): # · Observations · Result · Severity · Details · Notes · Page · Screen · UXR ticket. Replicate that structure as CSV for the script.

## Consolidation script
`scripts/consolidate_findings.py` merges each evaluator's CSV (columns `where, problem, heuristic, severity, recommendation`; Spanish aliases `donde, problema, heuristica, severidad, recomendacion` also work; heuristic 1-10, severity 0-4), groups by place + heuristic, computes average severity and agreement among evaluators, marks what only one evaluator saw and lists severity disagreements of 2 or more points. Use:
```
python3 scripts/consolidate_findings.py eval_ana.csv eval_ben.csv --output summary.md --lang en
```
Sample inputs: `assets/sample-findings-ana.csv`, `assets/sample-findings-ben.csv` (English) and `assets/sample-findings-carla.es.csv` (Spanish). Limitation: it groups by the exact text of `where`; unify screen names beforehand.

## NN/g workbook (structure)
Header: evaluator, date, product, task. For each heuristic: short definition, 2 guiding questions, and two columns (Issues / Recommendations). Workbook questions per heuristic (paraphrased): 1 does it clearly communicate its status? quick feedback? · 2 will the user know the terminology? do controls follow real-world conventions? · 3 can you go back a step? are exits easy to discover? cancel? undo/redo? · 4 does it follow industry conventions? consistent visual treatments? · 5 does it avoid slips with helpful constraints? warn before risky actions? · 6 does it keep what is important visible? contextual help? · 7 are there accelerators (shortcuts, gestures)? personalization? · 8 does it focus on the essential? has distractions been removed? · 9 does it use traditional error visuals (bold, red)? offer an immediate fix? · 10 is help searchable? does it appear in context?

## Complements
- **Cognitive walkthrough**: evaluates learnability; NN/g has a separate article (not read here).
- **Desirability study** (for heuristic 8 when the debate is "I like it / I don't"): participants choose, from a set of adjectives (e.g. confusing, trustworthy, overwhelming, easy to use), those that describe each visual direction and explain why; qualitative version (small samples, not quantitative) and quantitative (survey with embedded images). It measures attitude and does not predict real behavior. It brings the target audience's voice against the opinion of the designer or decision maker (source: Rohrer, 2008).
