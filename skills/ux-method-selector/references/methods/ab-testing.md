# A/B testing (and multivariate)

**When to use it**: post-launch (or a product with traffic) to know which of two versions performs better on a behavioral metric. It does NOT explain the why: complement it with interviews, exit surveys or replays. With little traffic it does not work: use qualitative usability testing.

**Steps**
1. Define a primary metric and a hypothesis before building the variant.
2. Control (A) + challenger (B) that changes **a single variable** (multivariate is the exception and requires more traffic).
3. Prioritize high-impact elements (purchase flow, key layouts) over micro-adjustments.
4. Compute the sample size beforehand with a calculator; a small sample biases the result.
5. Split traffic randomly and in equal parts (50/50); run both at the same time, do not compare a peak week with a slow week; one test per campaign at a time.
6. Let it run until it reaches significance (hours to weeks depending on traffic).
7. Read the primary metric, not a "nice" secondary one (clicks) if it does not match the goal.
8. Segment (new/returning, mobile/desktop, channel) and record the learning.

**Thresholds (HubSpot)**: aim for >=95% confidence; 80% may be tolerated in low-risk tests or radical changes; small changes (button color) demand a stricter criterion. A difference like 16.04% vs 16.02% is not a winner. With no clear winner: mark "inconclusive", keep the original or iterate.

**Mistakes**: changing several things at once; stopping as soon as it is "winning"; picking a winner by a secondary metric; not measuring simultaneously; copying "best practices" without testing (your own audience may behave differently).

**Deliverable**: test sheet (hypothesis, variants, metric, sample, duration, result with confidence, decision, learning).

Note: an inconclusive A/B result is exactly the case where qualitative follow-up (for example interviews) completes the picture.
