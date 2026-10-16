# Topline and executive summary by audience

The same study is told differently depending on who decides. What changes is **what you open with**, **what evidence you show** and **what decision you ask for**; the findings do not change. If the finding changes with the audience, something is wrong.

## Contents
1. Audience matrix · 2. Topline template · 3. Templates by audience · 4. How to find out what each one needs · 5. Mistakes

## 1. Audience matrix
| Audience | Question they bring | Open with | Evidence that persuades | Decision requested | Typical format |
|---|---|---|---|---|---|
| **Product (PM)** | What do I build or stop building, and in what order? | Prioritized recommendations and the decision they unblock | Frequency (X of N), severity, impact on the roadmap metric | Prioritize / postpone / more research | 1-page summary + priority table |
| **Design** | Where and why does the experience break? | Journey moments with pain, and the why | Quotes, clips, annotated screenshots, journey, success rate per task | What to redesign first, what to explore | Full report + working session |
| **Engineering** | What exactly changes, and how do I know it is right? | Concrete changes, use cases and observable criteria | Reproduction of the problem, steps, short clip, severity | Estimate and commit | Ticket per change (see `insight-to-spec.md`) |
| **Leadership** | What business risk or opportunity is there, and what are you asking for? | Business impact, risk, decision requested | One real product metric + one concrete story | Approve resources / direction | 5-line or 1-page summary, 5 min in a meeting |
Basis for this split: report guides agree on adapting detail level and language to each audience (executives: business impact; development: what to change and where; design: the data behind the finding). It is the same idea as the "stakeholder briefs" in several kits.

## 2. Topline template (5 lines, for anyone)
1. **What we set out to learn:** one sentence.
2. **Short answer:** one sentence.
3. **Three things that matter:** findings with "X of N".
4. **What we recommend and what we ask:** decision + owner + date.
5. **What we do not know:** one sentence and the study that would close it.
It must be understandable without opening the report. Test it on someone outside the team.

## 3. Templates by audience
**PM**
```
Decision it informs: [...]
We recommend: 1) [change] - evidence X of N, high severity, estimated effort [...]
              2) [...]
For the roadmap: do now / test first / leave. Risk of not doing it: [...]
We ask: [prioritize A before B] by [date].
```
**Design**
```
Where it breaks: [phase/screen] - what they do vs. what they expected.
Why (quotes and clips): "..." (P3, segment) · clip 01:12-01:40
What to try: [How might we...?] x2-3
Material: full report, journey, curated recordings.
```
**Engineering**
```
Change 1: [concrete description and where] · Observed problem: [steps to reproduce]
Observable acceptance criterion: [...] · Severity: [blocks/hinders/annoys]
Edge cases seen: [...] · Not included: [...]
```
**Leadership**
```
Situation: [real metric, e.g. "X% abandon at payment" - [complete] if there is no data].
What we found: [one sentence with the cause].
What to do and what it costs not to: [risk/opportunity in their language: revenue, retention, risk].
Decision requested: [...] - next milestone: [...]
```

## 4. How to find out what each one needs
If stakeholder interviews were held during planning (`ux-research-plan`), reread them: they say which decision each person makes, how much time they have and how they prefer to receive information. If not, ask two things before writing: "what will you decide with this?" and "in what format do you actually read it?". For the later impact (was anything decided differently?), continue with `ux-research-impact`.

## 5. Mistakes
- Sending the same report to everyone and expecting each to find their part.
- Opening with the method for leadership or PMs.
- Showing engineering only conclusions without reproduction steps.
- Sweetening or hardening the finding depending on who hears it: emphasis changes, facts never do.
