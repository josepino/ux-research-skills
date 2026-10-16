# Participant panel hygiene

A panel (the list of people who agreed to take part) degrades silently: empty fields, repeats, different values for the same thing. Result: the panel looks smaller than it is and filters badly.

## 1. What to check
| Problem | Example | Why it matters |
|---|---|---|
| Empty fields | 40% without "job title" | You cannot segment |
| Exact duplicates | The same row twice | You contact the same person twice |
| Duplicates by normalized email | `Ana.Perez@Example.com` and `ana.perez@example.com` | Same person with two records |
| Variants of a value | "Product Manager", "product manager", "PM", "Product Mgr." | Filtering by one misses the others |
| Old data | Contact with no activity for years | Bounces, expired consent |
| Overload | The same people in many studies | Fatigue and professional-style answers |

## 2. Run the report
```bash
python3 scripts/panel_hygiene.py panel.csv --email email --fields job_title,country --proposals proposed_changes.csv
```
- **It does not modify the original.** It reads the CSV and reports empty fields, duplicates (exact and by normalized email) and similar values grouped by simple normalization (lowercase, no accents or punctuation) and by `difflib`.
- With `--proposals` it writes a new CSV with columns `column, current_value, proposed_value, reason, approved` (Spanish headers with `--lang es`). It never overwrites existing files.
- Abbreviations and synonyms ("PM" ↔ "Product Manager") are not detected by shape: add them by hand in the proposals CSV. The report lists values that look like common job-title abbreviations (PM, PO, VP, SWE, Sr, Mgr, UXR and similar) so you can check them, but it never merges them on its own. Abbreviations vary by company and country (PM can mean product manager, project manager or prime minister), so a person must decide.
- English and Spanish headers both work for the email column (email, mail, correo). If the tool uses another separator or encoding, the script says so with a clear message.

## 3. Propose corrections without applying anything
1. Ask for an **export** of the panel (do not work on the live database) and keep an untouched copy.
2. Run the report and review each group of values. **Similar does not mean equal**: "Employed"/"Unemployed" or "Austria"/"Australia" are not merged.
3. A responsible person marks `approved=yes` on each row they accept, with the original copy available to undo.
4. Only then are changes applied, in the tool, recording the date and who approved. This skill neither applies changes nor deletes records.
5. For duplicates: decide which record is the main one and keep the most recent consent; do not combine sensitive data without review.
6. Prevent: closed lists in forms, a single email format and a "last contact" field.

## 4. Retention and deletion
- Keep identifiable data only while it serves the purpose the person consented to. The EU GDPR states this as "storage limitation" (art. 5.1.e) and data minimization (art. 5.1.c); if you operate in another country, check local law.
- Define in writing: what panel data is kept, for how long (your policy and what was consented set the period) and who can access it.
- Periodically review those who have not responded in a long time: ask whether they want to continue or remove them.
- On a deletion request or consent withdrawal: confirm identity, delete from the panel and from copies/exports you control, and reply confirming. **Confirm with a responsible person before deleting** identifiable data.
- Keep the identity table separate from notes and transcripts (`ux-research-ops`, `ux-ethics-bias-review`).

## 5. Cadence
Before a study with heavy recruiting, and regularly (the team decides the frequency). Also review segments with few people to know where to recruit next.
