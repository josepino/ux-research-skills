# Repository, taxonomy and file names: detail

Read this when you must build, choose a tool for, tag or maintain a repository, or define a naming convention.

## Contents
1. What it is and what it includes
2. Two types: document library vs insight database
3. Possible functions (pick 1-2 to start)
4. How to build it (steps)
5. Taxonomy and tags
6. Tools
7. Maintenance and cleanup
8. Permissions and privacy
9. File naming convention
10. Atomic research

## 1. What it is and what it includes
A central place for research artifacts so that others can use them (NN/g). It usually includes: reports; insights as entities of their own; study materials (plan, screener); recordings, clips and transcripts; raw notes. It can also add support or sales feedback. Maze adds: the repo's mission and vision, a research roadmap, methods and SOPs, tools and templates, findings with takeaways and tags, and raw data in a read-only zone to avoid accidental deletion.
Quality test (quote from Mia Mishek, Pax8, via Maze): if someone needs the repo explained to them, it is not doing its job.
Difference from "folders in Drive" (Lyssna): a repo organizes by themes and insights, has full-text search, consistent tags and collaboration; folders are searched by file name.

## 2. Document library vs insight database (NN/g)
| | Document library | Insight database |
|---|---|---|
| Pros | Easy to contribute to and maintain | Insights are easy to find |
| Cons | Hard to search for specific insights | Loading is laborious; insights without context; must be updated or retired |
Core trade-off: discoverability vs loading effort. They can be combined: each insight links to the folder of the study it came from. For a small team, start with a library + an insights spreadsheet with tags.

## 3. Functions (Condens)
Centralize existing data; gather all feedback (support, reviews, sales); speed up the process (analysis and archiving are the same task, the insight stays tied to its evidence); analyze collaboratively; democratize access (curate "top 5 stories" and findings by product, decide whether to open all the data or only the curated part); a participant base (tied to data for recruiting and to delete everything about a person if they ask). Define three things: who uses it, who maintains it, which functions.
Condens's own warning: the term "repository" is used with different meanings.

## 4. How to build it
NN/g (4 steps): 1) get buy-in (value, ROI if there is budget); 2) research before choosing (how they research today, what questions stakeholders ask, what tools they already have); 3) start simple and iterate (few broad tags, import the most useful first, test the taxonomy with card sorting or tree testing); 4) onboarding and advocacy (reminders, training; expect resistance to change).
Lyssna (6 steps): goals and stakeholders; tools; standardize inputs (names, mandatory metadata, structure); taxonomy and governance; train; maintain.
Adoption attributes (NN/g): easy to access, flexible permissions, intuitive navigation or tags, reliable search, exportable/integrated (e.g. share to Slack or Teams).

## 5. Taxonomy and tags
- Tag types (Lyssna): topic, user segment, method, product area. Maze adds country, feedback type, journey stage.
- Few broad tags at the start; they can change over time (NN/g).
- Define the terms with stakeholders and align with internal glossaries (Maze).
- Governance: an owner of the list, a process to propose new tags; review entries without tags periodically (User Interviews).
- Documentation fields per study suggested by Maze: key insights, quotes, priorities, criticality, sources, solutions considered.

## 6. Tools
Three most used families, per an NN/g survey (more than 400 responses): collaboration (Confluence, SharePoint), research platforms (Dovetail, EnjoyHQ, Condens, Great Question), databases (Notion, Airtable). Choose by what the team already uses. Maze: a well-documented Drive folder or Notion can serve as well as a dedicated tool. Free templates mentioned by User Interviews: Polaris (Airtable, popularized atomic "nuggets"), OneFootball's Notion, Pivotal's Trello. Miro offers a repository template on a board (searchable with Cmd+F). Prices and offers on those pages change: verify them before recommending.
For participant data, prefer tools with access roles and deletion tied to the person.

## 7. Maintenance and cleanup (User Interviews)
- Map feedback channels and where each is stored; automate intake (e.g. Zapier) so loading is easy.
- Assess currency: old research can lead to deciding with obsolete data (example: the pricing page has since changed). If it is no longer current, archive with a date and reason. Kate Towsey (Atlassian): the answer is "it depends".
- Audit tools: what is used, what is paid for but unused, which integrations are missing.
- Review missing tags when closing each project.

## 8. Permissions and privacy
Normally the repo should not be public (NN/g): it may hold confidential designs or recordings with identifiable data. Roles (researchers edit, stakeholders read only), access logs and anonymization (Lyssna). A repo that links participant to data makes deletion requests easier to serve (Condens). Connection with consent and retention: `ux-ethics-bias-review`.

## 9. Naming convention (Harvard Data Management, adapted from Briney)
- Define it **before** accumulating files; document it in a README next to the files.
- Most important first (alphabetical order rules); if you search by date, date first.
- ISO 8601 date `YYYYMMDD` or `YYYY-MM-DD` so it sorts chronologically; with time: `YYYYMMDDThhmm`.
- Sequential numbers with leading zeros (001, 002… 010).
- No spaces or special characters; separate with hyphen, underscore or capitals; alphanumerics, hyphens and underscores only.
- Version at the end: `_v01`, `_v02` (or version date).
- 2-3 letter codes for categories, documented.
- Recommended length: 40-50 characters. If the name carries too much metadata, move it to a master spreadsheet.
- Anti-pattern: `Eric notes.txt`, `Final FINAL last version.docx`; User Interviews adds including project, date and participant number in notes.
Nuances from Palko (UX Planet, 2019; summary): the convention also protects against losses from folders with non-semantic names that someone deletes believing them irrelevant, and eases handoff to other people or teams. Beware of versioning in the name (`_v01`): he himself notes that tools with built-in version control (Figma, Abstract, Plant for Sketch) make it partly unnecessary; for research files (notes, reports) it is still useful. His typical counterarguments ("it takes time", "it kills creativity") are solved by habit. Example folder order for notes (Kumar): topic / moderator_participant_date / note-taker_file; it is an alternative to putting everything in the file name.
This skill's scheme: `YYYY-MM-DD_study_type_pNN_vNN.ext` (see SKILL.md). Spanish-speaking teams can use `AAAA-MM-DD_estudio_tipo_pNN_vNN.ext` (`create_study_structure.py --lang es`).

## 10. Atomic research
An approach where knowledge is split into reusable "nuggets"/insights, each with linked evidence (NN/g, Maze, User Interviews). It costs more to load but improves discoverability. Do not demand it from teams of 1-2 people without maintenance time.
