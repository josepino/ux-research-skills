# Error messages and plain language (heuristics 2, 5 and 9)

## Contents
Definition · Visibility · Communication · Efficiency · Extreme cases · Inline validation and measurement · Evaluation rubric · Example rewrite · Plain language (heuristic 2)

Use this guide when the report has findings about errors, form validation or interface text. Errors are a quality component of usability and are often an "afterthought" for teams, which is why they yield many findings. More before/after pairs in English and Spanish: `references/microcopy-before-after.md`.

Useful definition: error message = a system-generated interruption that informs of an incomplete, incompatible or undesirable situation.

## Visibility (is it seen and tied to the problem?)
- **Close to the source**: the indicator next to the field that failed; a faint message far from the field is a finding.
- **Redundant and accessible indicators**: bold text/highlight, high contrast, and red is the convention, combined with an icon and border. Never color alone nor animation alone: NN/g cites about 350 million people with color vision deficiency.
- **According to impact**: "good to know" notices with a label, toast or banner; the blocking modal is reserved for serious errors.
- **Not too early**: showing the error before the person finishes is a hostile pattern (like grading an exam before they answer). Do not treat skipping a field as an error; inline validation does help in fields where getting it right first time is unlikely.

## Communication (is it understood and does it help?)
- Human language; codes only as optional technical detail (e.g. a dropdown).
- Concise, precise description: "An error occurred" says nothing. But avoid technical precision that does not match the user's mental model.
- Constructive advice: not only the problem but how to solve it (e.g. "out of stock": when it returns, or offer an email alert).
- Positive tone, no blame: avoid words like "invalid", "illegal", "incorrect" and phrases like "you did not...". Focus on what is missing or the threshold.
- Humor: minimal; it gets old if the error is frequent. Avoid "Oops!", ALL CAPS and excessive exclamation marks.
- Specific button actions ("Yes, update") and explain what happens to progress with each choice; ambiguous buttons are "trap buttons".
- Brevity: a study cited by a UX writing source (attributed to the American Press Institute) associates sentences of 14 words or fewer with 90% comprehension; take it as guidance, not a hard rule (secondary source, unverified).

## Efficiency (does it protect the user's effort?)
- Prevent the probable (warn if they mention an attachment and there is no file).
- **Keep what was entered**: never empty the form; correct on top of what was typed. Better if only the fields with errors need correcting.
- Reduce correction effort: propose options (e.g. if city and postal code do not match, a button with the matching city).
- Educate concisely, with a link to more detail if needed (do not overdo it).
- Avoid a long error list above the form: use inline validation; it is also worse for screen readers.

## Extreme cases
If the system goes down entirely (overloaded server) and there is no recourse, an apology combined with something novel can save the moment (end-of-experience effect); it is exceptional and hard to do well, especially if data is at risk.

## Inline validation, preventive microcopy and measurement (CXL)
Contributions from a CXL blog (summary retrieved via browser; partial). They reinforce the above; the difference lies in the nuances noted.
- **Four frequent failures**: ambiguity (a "Nope" does not say which field failed), blaming or condescending, poor placement (generic error far from the field, or just an underline that is easy to miss, as in the Netflix case cited) and unclear expectations (saying "that email is already registered" without offering to recover the account or sign in).
- **Error summary above the form**: a long list magnifies severity and leads to abandonment (matches "Avoid a long error list" above). If there is no inline validation, indicate clearly where the error is.
- **Preventive microcopy**: a short clarification before submitting avoids errors (e.g. reminding to use the card's billing address, or "enter a single number" if the field does not accept ranges). It is a heuristic 5 finding if the expected format is never stated and only rejected on submit.
- **Nuance on humor**: here it says "minimal" (gets old if the error is frequent). CXL admits a light tone if it fits brand and context (a 404 page is the typical place) but warns it can frustrate. There is no deep contradiction: never humor in errors that block payments, data or critical tasks.
- **The "4 H's" (UXmas, via CXL)**: Human, Helpful, optional Humor, Humble (take the blame, apologize, offer a solution). Useful mnemonic for writing; not a standard.
- **Inline validation data**: CXL cites a 2009 test by Luke Wroblewski, with a small sample, that reported +22% success, -22% errors, +31% satisfaction, -42% time and -47% eye fixations versus validating on submit. It is a single small, second-hand study: use it as an order of magnitude and do not cite it as a firm figure. The "not too early" warning above still applies.
- **Measuring form errors**: form analytics (average corrections per person who starts the form, corrections per field), path exploration in Google Analytics (repeated steps signal friction) and JavaScript errors as custom events. Used to decide which fields to prioritize and to verify improvements.
- **Claim not used**: the blog attributes a cortisol increase to errors; it was not incorporated because there is no verifiable source in the summary.

## Quick rubric to score a message (0 = no, 1 = partly, 2 = yes)
| Criterion | 0-2 |
|---|---|
| Visible and close to the source, not only color | |
| Clear language, no codes or jargon | |
| Describes the concrete problem | |
| Offers a solution or shortcut | |
| No blame, no misplaced humor | |
| Keeps what was entered | |
| Appears at the right moment | |
Total /14. This rubric is our own, inspired by the cited guides (NN/g has its own, not read here).

## Example rewrite
- Before: "Error 502: invalid input." / After: "We couldn't find that email address. Check that it looks like name@example.com."
- Before: "Oops! Something went wrong." / After: "We couldn't save your changes. Your data is still here; try again in a few minutes."

## Plain language (heuristic 2, applicable to all text)
- Identify the audience; choose words familiar to *that* audience; remove brand jargon, idioms and slang.
- Experts also prefer clear, scannable language. Jargon is acceptable only if the specialist group truly shares it; explain a term before using it if in doubt.
- Sentences of 15 to 20 words at most; one idea per paragraph; for the web use much less text than on paper (NN/g suggests under 50% of the words of a print publication).
- Reading level: NN/g recommends 6th to 8th grade for the general public and 10th to 12th for experts; above 12th demands too much effort. Measure it with readability tools (note: grade metrics are for English; for Spanish use indices such as Fernandez-Huerta/INFLESZ, a point that does not come from the sources read).
