# Real and example cases (problem, method, result)

Note: the Spotify case (Shortcuts on Home) was verified against a Spotify Insights post (see section 8). The Postman case (search) remains UNVERIFIED: no retrieved page contains it; do not invent its data and ask for the source (https://www.yashshenai.com/postman-search) before citing it.

## Contents
1. Slack: redesign co-created with customers
2. Airbnb: check-in with photo/video (student case, NOT official)
3. Team with contradictory data (NN/g)
4. ClothezForU: when there is only quantitative data (LogRocket, fictional)
5. GitLab: researching AI features
6. Category labels (NN/g: label examples)
7. Jakob's Law: centered logos
8. Spotify: Shortcuts, neutral A/B and human decision
9. Real data in prototypes (Dropbox, Namahn)

## 1. Slack (official account from the Slack team)
- **Problem**: with growth, the interface became complex: a header with more than a dozen clicks and two search boxes; powerful features buried. Hard to measure with A/B tests of small changes.
- **Method**: a small team with disposable prototypes; a pilot co-designed in a shared channel with ~100 customers from the "champions" network; free-form conversation over weeks (sometimes a new version shipped in a day); then a benchmarking study with people who had never used Slack (tasks: send a message, search, join channels), comparing old and new versions.
- **Findings**: a channel's member count gives the "read the room" signal and should not be hidden; people discover useful features with a little education; search and history work better at the top; the floating compose button was ignored on desktop; right-click is used often; collapsible views should start open for people who do not know the product.
- **Result**: the second round matched or beat the previous design. Lesson: "obvious over clever, don't reinvent the wheel".
- **What it teaches**: mixed methods (qualitative co-design + task benchmarking), test with novices and experts, iterate fast, beware of changing people's daily environment.
- Limit: it is the team's own account, with no outcome figures.

## 2. Airbnb check-in (design course exercise, 2018)
- Make clear to learners: this is not Airbnb work; the authors had no company data.
- **Problem**: coordinating key handoff times is hard for hosts and guests; many enter without the owner; instructions by chat/SMS create uncertainty.
- **Method**: short interviews in cafes (non-representative sample, acknowledged), the author's personal experience (32 conversations with hosts, 13 trips), mind maps, Crazy 8, a screen prototype and tests with two mentor designers (acknowledged as not ideal).
- **Author's figures (anecdotal)**: ~70% of their check-ins were with help from third parties; 60% of a dozen acquaintances had at some point entered without the host. Do not generalize.
- **What it teaches**: how to frame the problem, state how you will know you solved it (Airbnb's "Arrival" rating criterion), acknowledge sample limits and biases (reflexivity). A good example of what is NOT quantitative evidence.

## 3. Contradictory data (Kate Moran, NN/g)
- **Situation**: a prototype reduces task times (quant), but in interviews users hate it.
- **What to do**: first review the methodology in four areas: participants (same profile? novices vs experts?), tasks (do they cover real use? how much prior exposure?), logistics (external and internal validity, moderators, confounders such as day/time) and analysis (statistical significance? time only for successful attempts, success rate, error types).
- **Interpretation**: perceived usability is not objective usability; people dislike change and there is an initial productivity dip; one minor thing can dominate opinion (peak-end effect).
- **Next steps**: beta with new employees, a learning study with several rounds, gradual rollout with opt-in. At one NN/g client the redesign took a year to perform better (anecdotal data point from the author).
- **Rule**: quantitative does not automatically override qualitative; triangulate.

## 4. ClothezForU (LogRocket, FICTIONAL company)
- A drop in sales after a redesign; quantitative-only analysis does not explain why and each role blames something different (images, diversity, copy).
- Lesson: behavior is the "what"; attitudes are the "why". An A/B test does not say which change caused the effect if you changed many things at once. Suggestion: usability test + a behavior-triggered survey (not only post-purchase).
- Use it as an example, stating that it is invented.

## 5. GitLab and AI features
See `ai-in-ux-research.md` section 7. Useful for: "how do I research an AI feature?" and "how do I avoid a solution looking for a problem?".

## 6. Navigation labels (NN/g)
Examples: "OMG!" on Airbnb is unclear compared with "Cabins" or "Tiny homes"; "Culture" misleading at Bon Appetit; invented names at Live Nation; overlapping categories at Delish; subcategories by product line at Behr instead of by benefit. Lesson: card sorting + tree testing, user language, function over form.

## 7. Centered logos (cited by Jakob Nielsen)
In a cited study, with a centered logo 24% failed to return to the home page with one click versus 4% with a left logo. Second-hand source (the law's author); use it as an example of the cost of breaking conventions.

## 8. Spotify Shortcuts (Nhi Ngo, Spotify Insights, 2020; the team's own account)
- **Context**: "Shortcuts" is an ML-driven space on Home showing what the algorithm believes are your current favorites. Product Insights worked with engineering, product and design using 1-2 week longitudinal studies and A/B tests to evaluate usability, recommendation quality and value (e.g. grid vs carousel). Qualitative work inspired A/B hypotheses and contextualized results.
- **Problem**: in early tests people could not explain why Shortcuts recommended what it did or predict how it would change; that hurt the value proposition (explainability).
- **Names tested**: "Listen Now" (what the model optimizes), "Shortcuts" (the feature), "Quick Access" (UX goal) and a time-of-day greeting ("Good morning/afternoon/evening").
- **Inconclusive A/B**: no significant change in consumption metrics after the usual 2 weeks ("too close to call"); according to the author this happens very often.
- **Human decision**: the designer recommended the greeting (feeling like "my" Home). The researcher had reservations because participants needed a direct explanation, but they saw surprise and delight at the greeting, and the team chose it.
- **Result**: the name forced improving explainability (users expected time-appropriate recommendations), so the model added time features. A one-month evaluative diary study after launch showed they understood Shortcuts quickly and grew fond of the greetings; at 6 months it was successful quantitatively and qualitatively (per the post).
- **Lesson**: when data does not decide, deciding with human judgment is valid; tests last less than real life with a product; prioritize user delight.
- **Nuances to teach**: (a) the account is the team's own, without figures; (b) older course-style material speaks of "A/B + interviews"; the post mentions longitudinal studies with participants and a post-launch diary and does not confirm "interviews" as such; (c) note that the human decision does not replace measuring: qualitative and quantitative evaluation followed.
- Useful for: neutral A/B, mixed methods, ML products and explainability.

## 9. Real data in design (Dropbox Design 2018; Namahn 2019)
- Dropbox: its Framer X prototyping kit was rebuilt with real data via APIs (translations to test localization, favicons, images, and the designer's own Dropbox content) to get closer to the final product and see people's real content; a quote cited: without real data "we fool ourselves" (Josh Puckett).
- Namahn (aviation apps): use real data, not "realistic" data; treat data as a stakeholder that tells a story (trends, delays, cancellations) and helps ask better questions; missing or wrong data shows up when you look at it. With AI, learn from probabilities: show confidence levels and prefer "I don't know" to a wrong answer.
- Sources are design blogs, not studies; the contribution is the principle, not figures. For research: ask engineering for data/API access and test prototypes with the participant's real content.
