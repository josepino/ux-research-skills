# Pseudonymization and privacy

Read this file when you must decide which data in a transcript identify someone, how to replace them, where to keep the map, what to do with indirect data, or place yourself in the general legal frame. This is not legal advice.

## Contents
1. Pseudonymizing is not anonymizing
2. Which data identify
3. How to replace
4. The identity map
5. Indirectly identifying data
6. What the script detects and what it does not
7. Legal frame, in general terms only
8. What cannot be pseudonymized

## 1. Pseudonymizing is not anonymizing
Pseudonymizing replaces identifiers with codes (`P01`), but a map exists that allows reversing it; the data remain personal while someone can re-identify. Truly anonymizing means nobody can re-identify even with additional data, and in qualitative interviews that is rarely certain (the content of what the person tells is already identifying). Frame the goal as "reduce the risk", not "it is now anonymous".

## 2. Which data identify
- **Direct**: first and last name, nickname, email, phone, username or @handle, address, national ID/passport/tax numbers or other document numbers, customer or account number, card, license plate, profile URL, IP, device ID, voice and face in the recording.
- **Contextual**: company, school, football team, neighborhood or small town, unusual job title, the specific date of an event, names of bosses, colleagues, relatives or customers mentioned (third parties who never consented).
- **Sensitive** (need more care even if they do not identify): health, sexual orientation, religion, ideology, immigration status, personal finances, minors.
- Names of **third parties** mentioned in the session are also pseudonymized: the interviewee consented, but their ex-boss did not.

## 3. How to replace
- Participants: `P01`, `P02`... one code per person, stable across all sessions and artifacts; do not use initials or fictitious names that suggest origin or gender.
- Third parties: `[PERSON_A]`, `[BOSS]`; companies: `[COMPANY_A]`, and if the industry matters for analysis, `[COMPANY_A, banking]` (generalize instead of deleting).
- Contacts and numbers: `[EMAIL_1]`, `[PHONE_1]`, `[URL_1]`, `[NUMBER_1]`, `[ADDRESS_1]` (the script does this; with `--lang es` the placeholders are `[TELEFONO_1]`, `[NUMERO_1]`, `[DIRECCION_1]`).
- Load all **variants** of each name in the CSV (full name, first name only, diminutive, misspelled by the transcription). Careful with names that are common words ("Rose", "Pilar", "Mora", "Rosa"): review each replacement.
- Apply pseudonymization also to speaker labels, the header, file names and already generated summaries.

## 4. The identity map
It is the most sensitive data of the study: whoever has it can reverse everything.
- Keep it **apart** from the text, in a place with access restricted to those who need it (ideally one or two people) and with an access log if the tool allows.
- Never upload it to the AI tool or attach it in the same thread or folder as the transcripts.
- Define when it is destroyed (at the end of the study, or when the consent's retention period expires) and who does it. If you no longer need to re-contact people or honor deletion requests, destroying it brings the data closer to anonymization.
- The script `pseudonymize.py` creates the map with owner-only read/write permissions (0600) on Unix-like systems, but that does not replace access control where you store it.

## 5. Indirectly identifying data
No mechanical rule solves them; decide case by case with the question "would someone in this person's circle recognize them by this?".
| Data | Options |
|---|---|
| Rare job title ("the only accessibility designer at company X") | Generalize ("senior designer") or remove the company |
| Small place | Generalize to a region or type of place ("town of fewer than 10 thousand inhabitants") |
| Unique date or event ("when the system went down on March 3") | Make it relative ("a few months ago") if the date is not needed |
| Combination of traits (age + trade + city) | Review the combination, not each datum alone; report ranges instead of exact values |
| Very particular story or distinctive anecdote | Ask the person if you want to quote it; paraphrase it or do not use it |
| Voice, face, screen background in the recording | The text does not solve this; restrict access to the original file |
When generalizing would destroy the analytic value of the datum, the path is to limit who sees the material, not to insist that "it is now anonymous".

## 6. What the script detects and what it does not
Detects by pattern: emails, URLs, @handles, phones (heuristic of 7 to 15 digits, excluding simple dates), long numbers of 6 or more digits in a row, SSN-like numbers, addresses of the form "123 Main Street" or "calle Mitre 123". It lists as candidates capitalized words in mid-sentence that are not in your CSV.
Does not detect: names without capitalization, nicknames, names spelled differently from the CSV, job titles, places without an address pattern, data written in words ("forty-three"), identifiers with their own formats, nor anything in the audio or video. It can give false positives (an 8-digit product code). **A human read of the result is always needed.**

## 7. Legal frame, in general terms only
- Many jurisdictions regulate personal data (in the EU, the GDPR; in California, the CPRA; in Latin America, national personal data protection laws, such as Argentine law 25.326 or Brazil's LGPD). Each defines what personal data is, legal bases, people's rights and deadlines; check the one that applies to your participants (usually where they live, not where your company is).
- Common ideas worth remembering: "personal data" are those that allow identifying someone directly or indirectly; pseudonymization reduces risk but those data still count as personal; a legal basis and a clear purpose are needed (for example consent); minimize data; limit the retention period; people can ask for access or deletion; using an external provider to process data usually requires a data processing agreement; transferring data to another country may have its own conditions.
- What to do: treat these points as flags to discuss with legal, the privacy officer (DPO) or the ethics committee. Consent criteria are in `ux-ethics-bias-review`.

## 8. What cannot be pseudonymized
If the study covers sensitive topics or vulnerable populations, or if the material has video/voice that is the evidence itself, decide before recording who has access, for how long, and whether an external tool is ruled out. It is better not to collect a datum than to protect it badly.
