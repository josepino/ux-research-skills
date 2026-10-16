# Tasks and moderation

Read this when writing tasks or building the script.

## 1. Writing tasks and scenarios
A good task gives a **motive and a context**, asks the participant for an **outcome** and does not reveal the path. The danger is measuring whether the person can read labels instead of whether the design is understandable.

Rules:
- **User's language**, not the product's. If the menu says "Billing", the task says "you need the receipt for what you paid last month".
- **No naming buttons, menus or steps** ("go to Settings > Profile" or "click…" ruin the task).
- **No prejudging adjectives**: "easy", "simply", "quick", "just".
- **Motives that do not reveal features**: "you want to renew in one click" tells the person the feature exists; state the need, not the solution.
- **A clear end point**: the person and the observer know when it is finished ("…until you see the confirmation on screen", "tell me the final price").
- **One goal per task**, realistic and with filler data if needed (dates, a fictional name).
- **Success criterion written before the session**: which screen or result counts as success, partial success or failure, and the time or attempt cap.
- **Test data**: for unmoderated tests list per task the data the tool needs (payee, amount, expected answer) and keep the wording true to the test environment (no "your own money" on test accounts).
- **Order**: from common to rare; an easy task first lowers tension. If tasks depend on each other, say so.

- **One register** in Spanish deliverables (voseo, tuteo or usted), matched to the user's message, across tasks and script.

| With clues | Without clues |
|---|---|
| Click "Reports" and look for this month's spending. | Your boss asks how much was spent last month. Find out. |
| Add a product to the cart with the blue button. | You want to buy these sneakers in size 42. Do it up to the point where you have paid. |
| It's easy: simply change your password. | You suspect someone knows your password. Do what you need to protect yourself. |

When naming a label is valid: testing one specific function, or expert users who use those terms; in that case leave that label out of the file you pass to the linter with `--labels`.

**Linter**: `python3 -I scripts/lint_tasks.py tasks.txt [--labels labels.txt]`. It flags product labels, numbered or chained steps, words like easy/simply/quick, click verbs and tasks with no end point. It detects clues in English and Spanish. It also gives soft alerts for singular/plural or stem matches of a label (receta / Recetas). It is a heuristic aid: confirm each alert. Exit code 0 means no alerts, 1 means alerts, 2 means an input error.

## 2. Moderation script
**Introduction (3-5 min)**: introduce yourself; explain that the product is being tested, not the person; that there are no right or wrong answers; that they can stop whenever they want; ask permission to record and confirm consent (see `ux-participants-recruiting`); say you will not be offended by criticism because you did not design this (even if you did).

**Think-aloud**: ask them to say out loud what they look at, think, expect and doubt while they work. A short example, or practicing with a warm-up task, helps, because talking to yourself is hard. Once tasks start, you speak little.

**During the tasks**
- Read the task exactly as written (or hand it over printed/in chat) so everyone receives the same.
- If they go quiet: "what are you thinking?" or "what did you expect to happen?". It is neutral and does not steer.
- If they ask "am I doing this right?" or "is it here?": hand the question back ("what would you do if you were on your own?" or "what do you expect to happen?").
- Wait: before intervening count to a few seconds; people often solve it themselves.
- If they are stuck for a long time, apply the criterion fixed beforehand: record failure (or success with help) and move to the next task. Note how much help there was.
- Record what they **do**, what they **say** and what they **expected**; behavior weighs more than opinion.

**What to say**: neutral prompts, "tell me more about that", "what do you see there?", "what did you think when…?".
**What NOT to say**: "it's easy", "there's a button there", "didn't you see the menu?", "very good", "that's a common mistake", adjectives about the product, or explaining or defending the design. Do not finish their sentences or nod enthusiastically when they get it right (it reinforces behavior).

**After each task (10-30 s)**: one difficulty question (SEQ, only when the team wants numbers) and "what was the hardest or most confusing part?".
**Closing**: open probes ("what was best and worst?", "what would you change?"), a global questionnaire if applicable (SUS or UMUX-Lite), thanks, incentive, what happens to the data.
**Debrief with the team** immediately afterwards (10-15 min): what surprised you, the 3 most serious problems you saw, what to change in the script for the next session. Note it while fresh.

## 3. Moderation by variant
- **Moderated remote**: test camera, audio and screen sharing beforehand; have a plan B if the connection fails; the participant shares their screen, not the moderator's.
- **Unmoderated**: you cannot re-ask, so tasks must be self-explanatory and the success criterion automatic (destination URL or an answer); run a pilot before launching.
- **Guerrilla/lean**: sessions of a few minutes where the audience is; one or two tasks; clear verbal consent; do not use it to measure times.
- **Prototype**: explain that not everything works; define which paths are active and where inactive clicks lead; prevent the participant from "filling in" the missing screen by imagining.
