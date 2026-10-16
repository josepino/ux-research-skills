# Report templates

When producing a deliverable, translate headings and labels to the user's language (see `report-languages.md` for the HTML labels).

## Full report
```markdown
# [Study] - UX research report
**Date:** ... · **Team:** ... · **Version:** ...

## Executive summary
- Context in one sentence.
- Key findings (3-5):
  1. **[Insight]** - brief evidence.
- Main recommendations and the decision requested.

## 1. Purpose and objectives
## 2. Key product metrics
## 3. Methodology
| Method | Instrument | Dates | Mode |
## 4. Participants
total n · segments · selection criteria · recruitment · limitations
## 5. Findings
### 5.1 [Theme A]
**Finding:** ...
**Evidence:** n of N · data · quotes ("..." - P3)
**Implication:** ...
### 5.2 [Theme B] ...
## 6. Recommendations
| # | Recommendation | Evidence | Impact | Effort | Priority | Owner |
**"How might we..." questions**: ...
## 7. What we do not know / next studies
## 8. Appendices
Guide · questionnaire · consent form · codebook · repository links
```

## Presentation script (30-minute readout)
| # | Slide | Message | Evidence |
|---|---|---|---|
| 1 | Why we researched | Decision to inform | Metric |
| 2 | How | Method and sample | |
| 3 | Summary | 3-5 findings in one sentence | |
| 4-8 | One finding per slide | Title = conclusion | Quote/clip/chart |
| 9 | Recommendations | Prioritized | |
| 10 | Next steps | Who does what and when | |

## One-page summary (for executives)
```markdown
**Problem/decision:** ...
**What we did:** [method, n].
**What we found:** 3 bullets (with a figure).
**What we recommend:** 3 prioritized bullets + impact.
**What we need from you:** decision/resource + date.
```

## Executive summary: four elements (one page)
Problem being solved · key findings · main recommendations · potential impact. Place it right after the table of contents so it is the first thing read. Tip: include the real metric that motivated the study (e.g. "X% abandon at payment") and mark `[complete]` if you do not have it.

## Research statement (to open the report, 3 lines)
Problem we tackle · why it matters · how we investigated it. Avoid numeric goals without a basis.

## Finding per slide (pattern)
- **Title:** the conclusion.
- **Body:** brief description + quote ("..." - P3, age, segment) + how many people mentioned it (n of N).
- **Variants:** with a participant photo, with a curated video clip, with an analytics chart and quotes next to each group.

## Alternative "pyramid" structure: answers first
Conclusion and recommendations -> key findings -> evidence per theme -> method and participants -> appendices. Worked example in `pyramid-structure.md`.

## Readout message (Slack/email)
"We finished [study] with [n] people. Most important: 1) ..., 2) ..., 3) ... We recommend ... Report: [link]. Can we book 30 min to decide next steps?"

## Callouts and quotes in Markdown (for `scripts/render_report.py`)
```markdown
> [!insight] Short callout text.
> [!recommendation] Show the shipping cost in the cart.
> [!risk] Mobile was not tested.
> "Verbatim participant quote." - P4, first-time buyer
```
