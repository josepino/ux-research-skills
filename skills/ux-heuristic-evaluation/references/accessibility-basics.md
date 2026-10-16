# Basic accessibility cross-check

Read this when the material shows problems with contrast, focus, labels or use of color. **It does not replace an accessibility (WCAG) audit**: it helps to name which heuristic breaks and to decide when to request a full audit with assistive technologies and people with disabilities.

| What fails | Heuristic that breaks | How to write it in the finding | Related WCAG criterion |
|---|---|---|---|
| Text or icons with low contrast | 1 (status cannot be seen) and 6 (you must remember what cannot be read) | "The gray-on-white text in step 2 is hard to read" + screenshot | 1.4.3 Contrast (Minimum), AA: 4.5:1 normal text, 3:1 large text (18 pt or 14 pt bold) (W3C) |
| Keyboard focus invisible or in illogical order | 1 (you cannot tell where you are) and 7 (the keyboard is an accelerator) | "With Tab you cannot see which button is active" | 2.4.7 Focus Visible, AA (W3C) |
| Fields without a label (placeholder only) | 6 (the cue is lost when typing), 5 and 9 | "The placeholder disappears when typing; there is no persistent label" | 3.3.2 Labels or Instructions, A |
| Color as the only indicator (error only in red) | 1, 9 | "The error is signaled only with red, with no text or icon" (NN/g cites about 350 million people with color vision deficiency) | 1.4.1 Use of Color, A |
| Buttons/icons without an accessible name | 4 and 10 | "The magnifier icon has no alternative text" | 1.1.1 Non-text Content, A |
| Tiny touch targets | 5 (slip errors) | "Buttons are so close together that it is hard to hit the right one" | 2.5.8 Target Size (Minimum), AA (WCAG 2.2): 24 by 24 CSS pixels |
| Error announced only visually | 9 | "A screen reader does not announce the message" | 3.3.1 Error Identification, A |

Criterion numbers, titles and levels were checked against the W3C WCAG 2.2 Quick Reference on 2026-10-14; the contrast ratios and focus criterion come from the W3C "Understanding" pages (see `sources.md`).

## How to use it in an evaluation
- Tag these cases "A11y" in addition to the heuristic.
- Assign severity by impact: an invisible focus blocks anyone who does not use a mouse.
- Recommend a tool-based check (contrast checkers, screen reader) for what is critical, and a specialist audit before claiming any conformance.
- In the report, write "possible accessibility barrier" rather than "fails WCAG": a heuristic review cannot establish conformance.
