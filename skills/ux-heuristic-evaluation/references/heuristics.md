# The 10 usability heuristics: guiding questions, warning signs and nuances

Based on Nielsen and Molich (original version of 1990, refined by Nielsen in 1994; NN/g updated names and examples, last revision 2024). They are general rules ("heuristics"), not specific guidelines: they help detect *candidate* problems, not dictate the solution.

## Contents
How to use this guide · 1 Visibility · 2 Real world · 3 Control · 4 Consistency · 5 Prevention · 6 Recognition · 7 Flexibility · 8 Minimalism · 9 Errors · 10 Help · When to break a heuristic · Quick checklist

## How to use this guide
For each step of the task, go through the 10 key questions. Log an observation only if you can point to **where** it is and **what is seen**. A heuristic violation is not always a problem to fix: it depends on context and alternatives (see "When to break a heuristic").

### 1. Visibility of system status
Keep users informed with appropriate feedback within a reasonable time. Without feedback comes the "did I tap the button?".
- Is the current state communicated? Does feedback arrive quickly after each action (color change, progress animation, sound, vibration, notification)?
- No action with consequences should run without telling the user.
- Does the user know where they are in a process (step 2 of 4)? Are there preventive warnings such as "Caps Lock is on" while typing, instead of waiting for the error?
- Example of correct state: the Send button goes from disabled to active when the form is complete.

### 2. Match between system and the real world
- Does the user understand the terms without googling them? Is there internal jargon, invented brand names, idioms?
- Do controls follow real-world conventions and map to the desired result (natural mapping)?
- Is information in natural, logical order? Do icons represent what the user thinks they do?
- Underlying question: did the vocabulary come from user research or from the team's heads? (you are not the user.)
- Plain language for experts too: see `references/error-messages-and-language.md`.

### 3. User control and freedom
- The four exit controls: **Back** (one step), **Cancel** (abandon the task), **Close** (close a view) and **Undo/Redo**.
- Warning signs: a disabled browser Back button or one that loses work; a "Back" that actually cancels everything (e.g. forces redoing the search); full-screen overlays where browser Back leaves the page instead of closing the overlay; a hidden exit or one in an unexpected place (the X is expected top right).
- Prefer text labels (Back, Close) to ambiguous icons. On mobile, an X can be read as Close or as Cancel: if it does both, label it or warn what happens to the changes.
- Undo is not just a button: removing an item from the cart is also undo. For bursts of actions, offer multi-step undo. Discoverable undo (visible in a menu/bar) beats hidden undo (iOS shake gesture, a snackbar that lasts a few seconds).

### 4. Consistency and standards
- **Internal** (within the product or family of products) and **external** (web/platform/industry conventions). Jakob's Law: users spend most of their time on *other* products and bring their expectations.
- Layers to review: visual (icons, images), page/button placement and layout (is the primary always on the right? how is "required" marked?), input data (same date/phone format; prefer a standard date picker), content and tone of voice (does it match marketing?).
- A design system helps but does not guarantee consistency: over time people forget rarely used elements and interpret the ambiguous differently. Recommend periodic design reviews and, about once a year, a cross-cutting consistency review (source: NN/g).
- Breaking a convention is justified only with user evidence, not with "we want something different".

### 5. Error prevention
- Two types: **slips** (unconscious action from lack of attention; typical in highly practiced tasks) and **mistakes** (goal formed from a wrong mental model). The first step is never to blame the user: if the error is easy to make, the defect is in the design.
- Against slips: helpful constraints (return date cannot be before departure), suggestions (autocomplete/search suggestions), good defaults, tolerant formatting (accept spaces/dashes and format as you type).
- Against mistakes: remove memory loads, support undo, warn before risky actions.
- Prioritize: first prevent high-cost errors (deletion, payments, sending), then the small frustrations.
- Bad pattern: a generic confirmation dialog for everything; people learn to ignore it. Reserve confirmations for what is irreversible.

### 6. Recognition rather than recall
- Recognizing (seeing and choosing) is easier than recalling (generating from scratch) because there are more cues. Classic pure recall: username and password; terminal commands; unmarked gestures.
- Helpful patterns: history and recently viewed, favorites/saved lists, autocomplete and search suggestions, previews, reuse of data already entered (shipping address as billing), contextual help instead of a long initial tutorial (nobody memorizes a tutorial).
- Edge case: hamburger menu. Hiding navigation violates this heuristic; on mobile the cost is usually accepted for the space. Note it, do not automatically mark it as a serious error.

### 7. Flexibility and efficiency of use
- Two axes: **several paths** to the same task (search, browse, recommendations) and **accelerators** (keyboard shortcuts, gestures, macros) that do not get in the way of novices.
- An accelerator must be discoverable but discreet: e.g. show the shortcut next to the command in the menu. Unmarked gestures are hardly discoverable.
- Personalization/customization: few users use it; do not depend on it. Automatic personalization is expensive and annoying if it goes wrong; role-based works well in enterprise tools.
- Beware of duplicating the same function in many places: it increases what must be learned. There is tension between flexibility and duplication; decide it with evidence.
- A system only for novices slows frequent users (endless wizards); one only for experts is hard to learn.

### 8. Aesthetic and minimalist design
- Every extra unit of information competes with the relevant ones and lowers their visibility. It does not mean flat or "ugly" design: it means visuals support the main goal.
- Check: is there unreadable text over images (e.g. a white price over a photo)? Decorative elements, blurry images, unexplained technical terms? Is progressive disclosure applied (common first, advanced on demand)? Is there hierarchy, balance, proximity, white space?
- Pleasantness raises tolerance for minor problems, but clarity is not traded for aesthetics.
- To measure real aesthetic response (not opinion), the tool is a desirability study (see `references/sources.md` and the section in `method-and-templates.md`).

### 9. Help users recognize, diagnose and recover from errors
Summary: simple language (no codes), precise problem, constructive solution and a noticeable visual. Full guide with criteria and rubric in `references/error-messages-and-language.md`.

### 10. Help and documentation
- Ideally it is not needed; when it is, it must be easy to search, task-focused, with concrete steps and short.
- **Proactive** (before the problem: onboarding, tooltips, templates, wizards) and **reactive** (FAQ, documentation, videos, support). Proactive help scenarios: first use, novices gaining mastery, existing users facing a redesign.
- "Push" disclosures (tips that appear unrelated to the goal) are usually ignored; "pull" ones (contextual to what the person does) work better. Push ones must be dismissible and the help must remain accessible later.
- Reactive help: visible, working search (a support center without a search box is a warning sign), scannable content (lists, hierarchy, keywords), categories, most-viewed content highlighted, video as a complement and never the only format.

## When to break a heuristic (and when not)
- Heuristics are guides, not laws; there are rare, context-dependent exceptions. Nielsen warns, paraphrased, not to bet that your design is one of them. Before knowingly violating one, research with users.
- That is why in the report distinguish *confirmed violation that harms the task* from *violation with an acceptable trade-off* (e.g. hamburger on mobile). This avoids false positives.

## Quick checklist
```markdown
| Heuristic | Met? (Yes/Partly/No) | Evidence (where/what is seen) | Sev. 0-4 |
|---|---|---|---|
| 1 Visibility of status | | | |
| 2 System and real world | | | |
| 3 Control and freedom | | | |
| 4 Consistency and standards | | | |
| 5 Error prevention | | | |
| 6 Recognition > recall | | | |
| 7 Flexibility and efficiency | | | |
| 8 Aesthetic and minimalist | | | |
| 9 Recovering from errors | | | |
| 10 Help and documentation | | | |
```
