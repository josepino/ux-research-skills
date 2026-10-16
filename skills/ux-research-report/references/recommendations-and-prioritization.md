# Recommendations and prioritization

## What makes a recommendation good
1. **Tied to a finding and to data** (what we observed, how many of N, quote or clip).
2. **Specific and actionable**: a concrete change, where, and how it is measured.
   - Vague: "improve navigation" / "improve checkout".
   - Concrete: "reorder the main menu according to the preference order from the card sort"; "add a progress bar showing how many steps remain in checkout" (examples adapted from Survicate).
3. **Realistic** for the team's resources, time and budget; an ideal solution nobody can implement does not help (Ramotion).
4. **With a research next step** when the data falls short (e.g. validate with an A/B test or a follow-up test after the change).
5. Optional: phrased as "How might we...?" to open ideation.

## Actionable vs. non-actionable insight
Idea from User Interviews: "users are dissatisfied" is no use. Better:
- *"They struggle to find the support pages (information architecture)"* -> next steps: highlight support, or run tree testing to decide where it lives.
- *"They are dissatisfied with onboarding but we do not know which part"* -> it does not say what to change in the product, but it enables a specific next study on onboarding.

## Prioritization
Two combinable lenses (Entropik, Uxcel):
- **Severity x frequency:** does it prevent completing the task or just create friction? How many users does it affect? High severity + high frequency first. Example from the source: not being able to add to the cart weighs far more than not being able to read a description without zooming.
- **Impact vs. effort:** high impact/low effort first (e.g. change a CTA's text before redesigning the page). The more effort, the more impact is needed to justify it. Prioritize together with product and design representatives.
- **Business impact:** findings tied to a measurable result (lost conversion, support cost) are usually prioritized above cosmetic or minor ones. Connect findings to the company goal (e.g. retention) to get support and resources.
- A 2x2 matrix helps the discussion (Miro's Eisenhower template is urgent/important: useful as an analogy, but for recommendations impact/effort usually fits better).

Suggested table: `# | Recommendation | Evidence | Severity | Frequency | Impact | Effort | Priority | Owner`.

## Beware of projections
Some blog templates include estimates such as "could raise conversion by up to 25%" or "add USD 250,000". They are illustrative examples, not data. In a real report, include a projection only if there is an explicit basis (current metric, assumptions) and label it as an estimate.

## Minimal example of a recommendation block
> **R1 (high).** Show the estimated shipping cost before the payment step.
> Evidence: [n] of [N] participants were surprised by the cost [complete]; abandonment at payment: [metric].
> How to measure: abandonment rate at payment before/after; follow-up test with 5-8 people.
