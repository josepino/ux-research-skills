# Quality check for cards and tasks

Read this before launching a card sort or a tree test, or when auditing someone else's. Partly automated by `scripts/check_study.py` (warnings from practical rules of ours, not verdicts).

## Cards (card sorting)
- [ ] **One idea per card.** "Invoices and receipts" are two cards. The script warns on connectors and commas.
- [ ] **No clues**: two cards with the same keyword ("Order history", "Payment history") get grouped by the word, not the concept. Vary the name or accept the bias and note it.
- [ ] **User language**, no internal jargon or feature brand names.
- [ ] **Same level of detail**: do not mix "Help" with "Change the password from your phone".
- [ ] **Reasonable quantity**: 30-50 per NN/g; more than 50 tires people.
- [ ] **No duplicates or synonyms**.
- [ ] **Pilot** with 3-5 people: did anyone not understand a card? Did they run out of time?

## Tasks (tree testing)
- [ ] **Scenario with a motive** ("You're thinking of opening a gardening service and want to see resources to get started"), not a search command.
- [ ] **No exact words from the tree**: if the task says "payment method" and the tree has "Payment method", the person does text matching, not navigation. The script detects it with `--tree`.
- [ ] **One defined correct answer** in advance (or several valid ones, noted).
- [ ] **One task per goal**, 5-10 in total, with an easy warm-up task.
- [ ] **Covers the doubtful categories** from the card sort and the business-critical tasks.
- [ ] **Random order**, and no task reveals the answer to another.

## If the check fails
Fix the wording and rerun the pilot: a study with clues returns results that look good and are not.
