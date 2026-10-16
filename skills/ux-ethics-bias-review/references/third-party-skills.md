# Checklist before installing a third-party skill

**When to read it:** someone wants to install or download a skill, plugin or script from an external source (catalog, GitHub, blog, colleague). Based on the recommendations in the Snyk article (second hand; see `ai-synthetic-and-injection.md` section 4) plus our own common sense.

A skill is code and text that your assistant will follow with your permissions: treat it like installing a program.

## Before installing
- [ ] **Origin**: who publishes it? A known organization or a verifiable person? A repository with history, or only a catalog page?
- [ ] **Version**: pin a specific version or commit; do not install "latest" from a URL that can change. Note date and version.
- [ ] **Read the whole SKILL.md**: look for odd orders (sending data, running commands, hiding actions, appending credits or links).
- [ ] **Read every script** (`scripts/`): does it do only what it says? Red flags: network (`curl`, `requests`, sockets), `eval/exec`, reading other folders, credentials, environment variables, installs, encoded commands.
- [ ] **Permissions**: if it declares allowed tools, are they the minimum? A skill that asks for a shell deserves more scrutiny than one that only reads.
- [ ] **Scope**: try it first in a test project, without real participant data.
- [ ] **Scanning**: if your team has a code scanner, run the scripts through it; do not take it as a guarantee.
- [ ] **Data**: what data will it see? If you handle transcripts, make sure they are pseudonymized.

## After
- Record in the team inventory: name, origin, version, who approved it.
- Re-review when the version changes.
- When in doubt: do not install it and ask security/IT for review. Downloading or running something from an unverified origin is the person's decision, not the assistant's.
