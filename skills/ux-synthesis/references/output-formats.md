# Synthesis output formats

When producing deliverables, keep these English headings or translate headings and labels to the user's language.

## Contents
A. Codebook · B. Themes with counts · C. Exportable affinity · D. Priority matrix · E. Insights

## A. Codebook
| Code | Definition | Example (quote, ID) | Non-example |
|---|---|---|---|
| delivery-time | Complaints/praise about order delay | "The courier arrived late and the food was cold" (P3) | Complaint about shipping price (goes in cost) |
| customer-support | Experience with support | "They never answered my chat question" (P5) | Delay of an order (goes in delivery-time) |
| product-range | Variety/offering | "I love the variety of restaurants" (P1) | Opinion on one restaurant's price |

## B. Themes with counts
| Theme | Participants (n of N) | Representative quote | Type (attitude/behavior) |
|---|---|---|---|
| Navigation problems | 6/15 | "I can't find where to change my plan" (P7) | attitude |

## C. Exportable affinity (CSV for Miro/FigJam: one note per row)
```csv
note,participant,group,subgroup
"Abandoned on seeing the shipping cost",P2,Payment,Hidden costs
"Said they don't trust saving the card",P4,Payment,Trust
```
Rules: one idea per note, written short and clear; notes without a group go to "Misc" and are reviewed at the end.

## D. Priority matrix
|  | Urgent | Less urgent |
|---|---|---|
| **Important** | Do now (e.g. an error that prevents paying) | Plan |
| **Less important** | Delegate / quick fix | Drop or monitor |

Detail table:
| Finding | Evidence | Frequency | Impact | Effort | Priority |
|---|---|---|---|---|---|

Automate B and D from a CSV of tagged notes (columns note, participant, tags; optional group, type, severity, effort): `python3 scripts/analyze_notes.py notes.csv --total-participants N`. Sample input: `assets/sample-notes.csv`.

## E. Insights and recommendations
| Insight | Evidence | Recommendation | HMW | Success metric |
|---|---|---|---|---|
| Users abandon at payment because they do not see the total cost beforehand | 6/8 sessions; 40% funnel abandonment | Show total cost in the cart | How might we show the total cost before payment without clutter? | Lower abandonment at payment |
