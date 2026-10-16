# Key concepts (quick reference)

## Contents
1. Why do research
2. Strategy and Lean UX
3. Nielsen's 10 heuristics
4. Researcher biases
5. Methods
6. Participant numbers
7. Mental models
8. Qualitative vs quantitative
9. Behavioral vs attitudinal (expanded)
10. Jakob's Law and conventions
11. Process and types of research
12. Parking lot in workshops
13. Contradictory data
14. Empathy, buy-in and real data

## 1. Why do research
Benefits: identify problems early, align with real needs, reduce risk, decide better, prioritize, differentiate, improve accessibility, give the team confidence, optimize ROI, adapt to the market. Consequences of not researching: products that solve no problem, are hard to use, or are useful but confusing. Data alone is not enough: it must be interpreted, assumptions tested, and action taken.

Basic steps: clear objectives -> identify resources -> choose method -> collect data -> analyze. Be empathetic by asking: why do they want to achieve something? how can they achieve it? what happens next?

## 2. Strategy and Lean UX
- New product: attract users, discover the value. Existing product: retain, grow customers, test innovations.
- Stakeholders: executives (budget, sign-off), leaders (seniors, VP of design), implementers (designers, devs).
- When? Continuously and from the start: discovery -> validation -> post-launch.
- Plan: objectives, key questions, methods and analysis, expected results, schedule.
- Lean UX: start from stakeholder assumptions -> basic prototype -> validate with users. Cycle: identify problem -> state the need -> make assumptions -> create a hypothesis -> test it.

## 3. Nielsen's 10 heuristics
1 Visibility of system status · 2 Match between system and the real world · 3 User control and freedom · 4 Consistency and standards · 5 Error prevention · 6 Recognition rather than recall · 7 Flexibility and efficiency of use · 8 Aesthetic and minimalist design · 9 Help users recognize, diagnose and recover from errors · 10 Help and documentation.

## 4. Biases
Confirmation (only seeing what confirms my ideas) · false consensus (assuming everyone thinks like me) · recency (the last thing in the session weighs more) · primacy (the first participant weighs more) · implicit (unconscious stereotypes) · sunk cost (continuing to invest because I already invested). In surveys: leading questions, sampling bias, question order, unbalanced scales. They are not eliminated, they are managed: record sessions, two observers, breaks between sessions, open questions, list assumptions beforehand.

## 5. Methods
Qualitative: competitor analysis, content audit, card sorting, ethnography, contextual inquiry, diary studies, heuristic evaluation, participatory design, in-depth interviews, usability tests.
Quantitative: A/B and multivariate tests, eye tracking, surveys, SUS, web analytics, usability benchmark, tree testing, desirability studies.

Axes for choosing: qualitative (why/how) vs quantitative (how many/how much) · attitudinal (what they say) vs behavioral (what they do) · project stage · context of use (natural, scripted, limited, without using the product, combined) · time and budget. Needs -> observation, interviews, surveys, diaries. Wants -> A/B, focus groups, rapid prototyping.

## 6. Participant numbers (NN/g references)
- Qualitative usability: ~5 per round/segment.
- Quantitative studies: at least ~20.
- Card sorting: ~15 per user group.
- Eye tracking (reliable heatmaps): ~39.
These are references, not laws: adjust for segments and variability.

## 7. Mental models
What the user believes about how a system works, shaped by prior experience. Everyone has their own (designers too, with knowledge bias). Fit the product to existing models unless there is a clear justification; a new product challenges models and has to teach. There is inertia: change only with a reason. Card sorting helps reveal the designer-user gap.

## 8. Qualitative vs quantitative
Qualitative: answers why/how; strength: depth; limit: bias and subjective interpretation; small sample. Quantitative: answers what/how many/how much; strength: measurable and generalizable; limit: does not explain the why. They complement each other (mixed methods, e.g. the Spotify Shortcuts case, verified: neutral A/B + qualitative studies with participants -> human decision; see `cases.md` section 8).

## 9. Behavioral vs attitudinal (expanded)
- Behavioral = what they do (observation, eye tracking, heatmaps, funnels, session recordings). Attitudinal = what they say or feel (interviews, surveys, focus groups, reviews). Attitudinal data is not obtained through passive analytics (Centercode).
- It is not the same as qual/quant: there is qualitative behavioral (watching recordings one by one) and quantitative attitudinal (surveys).
- Limits: behavioral does not explain motivation; attitudinal is subjective and hard to generalize. Spontaneous and solicited feedback weigh differently (LogRocket).
- A usability test collects both; it has small samples and an observer effect.

## 10. Jakob's Law and conventions
Users expect your site to work like the ones they already know (Nielsen, 2000). Conventions: search at the top, logo on the left that goes home, cart, native scroll. Innovate in content, not in structure. Labels: descriptive, no invented terms, no overlaps, based on mental models and validated with card sorting/tree testing (NN/g). Note on older material: some course-style material suggests ~5 users per round; a practical guide (Butterfly) proposes 5 to 8 per segment for task-based tests; they do not conflict, they are pragmatic ranges.

## 11. Process and types of research
- Study steps (Alida, 11): pre-research, planning, desk research, documentation, recruiting, collection, analysis, insights, reporting, dissemination, data maintenance. Short version (IxDF): question, method, recruit, do, analyze, present.
- Types by moment: discovery, descriptive, evaluative, monitoring.
- NN/g (via IxDF): discover (contextual inquiry, diaries), explore (card sorting, journey maps), test (usability, accessibility), listen (surveys, analytics).
- Measure: motivations, goals, needs, tasks and pain points.
- Constraint triangle (scope, cost, time): if you cut time or budget, scope or quality gives (Asana).

## 12. Parking lot in workshops
A visible, shared list of off-agenda topics. It works with reserved time (last 20-30 min or a meeting 1-2 days later), explained rules, affinity grouping, an owner and date per item, and inclusion in the minutes (NN/g). Without these it becomes a graveyard of ideas.

## 13. Contradictory data
Before deciding, audit the methodology (participants, tasks, logistics, analysis). Perception is not objective performance; change creates initial rejection. Triangulate (NN/g).

## 14. Empathy, buy-in and real data
- Good research questions (Yang, UX Planet): specific, focused and relevant, feasible with your resources, actionable, and still open to the method. Research informs design, it does not deliver the solution: explore and iterate.
- "You are not the user": research lets you set assumptions aside. Involving PMs, devs and data scientists (taking notes in interviews, analysis workshops, sharing findings) builds shared understanding; without sharing insights, researching is not enough.
- Decide with data and with human judgment: if the A/B is neutral, it is valid to decide with qualitative evidence and an understanding of people (Spotify case). Tests measure short periods compared with life with the product.
- Prototypes with real data (not just realistic) avoid late surprises (Namahn, Dropbox). In AI products the UI should reflect probability and allow "I don't know".
