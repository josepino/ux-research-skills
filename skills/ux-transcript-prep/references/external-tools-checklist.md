# Checklist: before uploading transcripts to an external or AI tool

Read this file before pasting, uploading or connecting transcripts (pseudonymized or not) to a third-party service: AI assistants, transcription services, research repositories, shared spreadsheets. It is not legal advice; if in doubt, stop and consult legal or privacy.

## Contents
1. Blockers: if any is missing, do not upload
2. About the service
3. About the data
4. Local alternatives
5. Decision and record

## 1. Blockers
- [ ] **Consent**: the participants' form covers recording, transcribing and analyzing with third-party tools or AI. If it does not mention it, do not assume it (modular consent, see `ux-ethics-bias-review`).
- [ ] **Pseudonymization done and reviewed by a person** over the full text; the identity map stays outside the tool.
- [ ] **Retention and deletion**: you know how long the provider keeps what you upload and how it is deleted (including the copy in histories, backups and logs).
- [ ] **Training**: you confirmed in writing (the terms of the plan you actually use) whether the provider uses your data to train models and how to turn that off. Terms vary by plan (free, enterprise, API): check your account's.
- [ ] **Internal authorization**: your organization allows that tool for participant data.

## 2. About the service
- [ ] Agreement with the provider (data processing terms / processing agreement) when the tool processes personal data on behalf of your organization.
- [ ] Where the data are stored and processed (country/region) and whether there is transfer to other countries with their own requirements.
- [ ] Who at the provider can see the content (human review, support).
- [ ] Account controls: per-person access, two-factor, no shared accounts, activity log if available.
- [ ] What happens to your data if you cancel the account or the provider changes owner.
- [ ] Certifications or security reports the provider declares (they are its claims: ask for the documentation instead of trusting the marketing page).

## 3. About the data
- [ ] You upload only what the task needs (one block, not the whole study; only the relevant participant).
- [ ] No original audio or video unless needed.
- [ ] No sensitive data (health, personal finances, minors, etc.) unless the consent and the provider explicitly cover it.
- [ ] No identity map, no participant list and no contact data in the same thread or folder.
- [ ] Indirect data (unusual job titles, places) generalized or excluded (see `pseudonymization-and-privacy.md`).
- [ ] The tool's results are also treated as study data: stored in the authorized repository.

## 4. Local alternatives
When a blocker is missing, these options avoid sending data out:
- Transcribe and analyze with tools that run on your machine or your infrastructure (local or self-hosted transcription and language models). Ask your technical team to validate the installation; local models may perform worse.
- Do the sensitive parts by hand (coding, quote selection) and use external AI only on material already pseudonymized and generalized.
- Use this skill's scripts, which run without network and without dependencies.
- Ask participants for specific consent for external AI use, with the option to refuse without losing their participation.
A warning: "local" does not mean "safe". Encrypt the disk, restrict folders and delete temporary files.

## 5. Decision and record
Note in the repository, per study: which tool, which data (pseudonymization level), which account/plan, who authorized, date and when what was uploaded will be deleted. If you cannot complete the blockers, the decision is **do not upload** and use a local alternative.
