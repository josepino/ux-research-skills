# research-profile.md: file format

One file per project in the working folder, named `research-profile.md`. Plain Markdown with `key: value` lines under fixed sections, so people and `scripts/validate_profile.py` can both read it. Keep it under 80 lines. Write values in the user's language, but keep the keys in English. Use `unknown` when a value is not known yet.

## Rules
- No participant personal data (names, emails, phones, recordings, IDs). Describe users as segments.
- No secrets, tokens, passwords or API keys.
- One line per field; separate multiple values with semicolons.
- Update `updated:` whenever the profile changes.

## Template
```markdown
# Research profile
<!-- Written by ux-research-onboarding. No participant personal data or secrets. -->
updated: YYYY-MM-DD
language: en            # language of deliverables: en, es, ...
audience: product team  # who reads the reports

## Researcher
mode: practitioner      # practitioner | learner | consultant
researcher_name: the name printed on reports as the UX Researcher
organization: company, agency or team name
role: UX researcher
experience: intermediate  # beginner | intermediate | advanced
team: team size and who is in it
research_today: how research is used today

## Project
product: what it is and who it serves
stage: validate         # discover | validate | post-launch
decisions_pending: decisions this research must inform; deadline
users: segments of users (not individuals)
user_access: easy | limited | none; how they are reached

## Constraints
time: e.g. 2 weeks per study
budget: e.g. no incentive budget
tools: e.g. Figma; Google Forms; Zoom
repository: where research is stored (name or location only)
privacy_rules: e.g. no recordings leave the company; GDPR
accessibility: needs of participants or deliverables

## Stakeholders
stakeholders: roles, e.g. product lead; design lead
convincing_evidence: e.g. short video clips; numbers; quotes

## Preferences
output_formats: e.g. 1-page summary; slides; markdown
detail_level: brief  # brief | standard | deep
tone: e.g. plain, direct
learning_goals: (learners only) what they want to learn

## Study log
- YYYY-MM-DD | study name | decision it informed | what to change in this profile
```

## Required fields (validator errors if missing or empty)
`updated`, `language`, `audience`, `researcher_name`, `role`, `experience`, `product`, `stage`, `decisions_pending`.

## Recommended fields (validator warns if missing)
`team`, `users`, `user_access`, `time`, `privacy_rules`, `convincing_evidence`, `output_formats`, `detail_level`.

## Allowed values
- `experience`: beginner, intermediate, advanced
- `stage`: discover, validate, post-launch (also accepted: unknown)
- `detail_level`: brief, standard, deep
- `mode`: practitioner, learner, consultant
- `user_access`: easy, limited, none (free text after the keyword is fine)
- `language`: a code such as en or es
