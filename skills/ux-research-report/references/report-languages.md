# Report language and HTML labels

The report is written in the user's language. `scripts/render_report.py` only needs the interface labels (table of contents title, callout names, footer) in that language. English (`en`) and Spanish (`es`) are built in; for any other language, translate the dictionary below and pass it with `--labels`.

## Contents
1. Label keys · 2. Template to translate · 3. Workflow for other languages · 4. Right-to-left languages · 5. Callouts and quotes in Markdown

## 1. Label keys
| Key | Where it appears |
|---|---|
| `contents` | Title of the table of contents |
| `skip` | Accessibility "skip to content" link |
| `prepared_by` | Cover, before the author name |
| `date` | Cover, before the date |
| `generated_with` | Footer line |
| `print_hint` | Footer hint about printing / saving as PDF (screen only) |
| `callout_insight` | Label of `> [!insight]` blocks |
| `callout_recommendation` | Label of `> [!recommendation]` blocks |
| `callout_risk` | Label of `> [!risk]` blocks |
| `callout_note` | Label of `> [!note]` blocks |
| `cover_alt` | Alt text of the cover image |
| `table` | Accessible name of each table region |
| `missing_image` | Text shown when an embedded image file is not found |

Missing keys fall back to English; unknown keys are ignored with a warning. Values must be plain strings (no HTML).

## 2. Template to translate
The same file lives at `assets/labels.template.json`.
```json
{
  "contents": "Contents",
  "skip": "Skip to content",
  "prepared_by": "Prepared by",
  "date": "Date",
  "generated_with": "Generated with UX Research Skills",
  "print_hint": "Tip: use your browser's Print / Save as PDF (A4) for a paper copy.",
  "callout_insight": "Insight",
  "callout_recommendation": "Recommendation",
  "callout_risk": "Risk",
  "callout_note": "Note",
  "cover_alt": "Report cover illustration",
  "table": "Table",
  "missing_image": "Image not found"
}
```
Example in French (partial is fine): `{"contents": "Sommaire", "callout_insight": "Constat", "callout_recommendation": "Recommandation", "callout_risk": "Risque", "prepared_by": "Préparé par", "date": "Date"}`.

## 3. Workflow for other languages
1. Write the whole report in the user's language (headings, findings, recommendations). Keep participant quotes in the original language; add a translation next to them if the readers need it.
2. Copy the template, translate the values (never the keys) and save it as `labels.<code>.json`.
3. Run: `python3 scripts/render_report.py -i report.md -o report.html --lang <code> --labels labels.<code>.json`
4. Open the HTML once and check that the title, contents and callout labels read correctly.

## 4. Right-to-left languages
For `ar`, `he`, `fa` and `ur` the script sets `dir="rtl"` on the page and the layout mirrors automatically (contents column, quote bars, list indents). Write the Markdown normally in the right-to-left language.

## 5. Callouts and quotes in Markdown
```markdown
> [!insight] 5 of 8 participants mentioned the late shipping cost.
> [!recommendation] Show the estimated shipping cost in the cart.
> [!risk] Mobile was not tested.
> [!note] Fictional example data.

> Verbatim participant quote, on its own lines.
> — P4, first-time buyer
```
A blockquote that ends with a line starting with an em dash (or `--`) becomes a quote card with the attribution below it. Optional front matter at the top (`title`, `subtitle`, `author`, `date`) fills the cover; command-line options override it.
