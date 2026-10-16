# Sources used in this skill

All were read in downloaded text. New figures in the skill come from these pages.

| Title and URL | What it provides | Where it is used |
|---|---|---|
| NN/g, "How Many Test Users in a Usability Study?" https://www.nngroup.com/articles/how-many-test-users/ | 5 users qualitative; at least 20 quant, 15 card sorting, 39 eye tracking; overlapping segments 3-4 per group; ROI; real average 11 | sample-size.md, SKILL.md section 2, script |
| NN/g, "How Many Participants for Quantitative Usability Studies" https://www.nngroup.com/articles/summary-quant-sample-sizes/ | 40 for quant (39/21/28/15 binary; 47/26/33/19 continuous), assumptions | sample-size.md sections 4-5, script. Contradicts the older "at least 20" |
| UXtweak, "Usability Studies: How Many Participants Are Enough" https://blog.uxtweak.com/usability-studies-how-many-participants-are-enough/ | Faulkner table (5 → 55% minimum/85%; 10 → 82%), 3-7 users, pilot of 1-2, e-commerce about 35% with 5 | sample-size.md sections 2-3 |
| Lyssna, "Recruiting User Research Participants" https://www.lyssna.com/blog/recruiting-user-research-participants/ | Customers vs non-customers, channel and timing table, segmentation, quant 20-30, video screener | SKILL.md sections 1 and 4, screener |
| Lyssna, "Incentives for Research Participants" https://www.lyssna.com/blog/incentives-for-research-participants/ | Types, ranges by method, coercion, alternatives | incentives.md |
| User Interviews, "The Ultimate Guide to User Research Incentives" https://www.userinterviews.com/blog/the-ultimate-guide-to-user-research-incentives | Data from 25,000+ sessions: $/hour, fill rate, no-show | incentives.md section 4 |
| User Interviews, "How to Recruit Good Participants for User Research" https://www.userinterviews.com/ux-research-field-guide-chapter/find-good-research-participants | When to recruit customers vs outsiders, criteria, participant burnout | SKILL.md sections 1, 4 |
| Lyssna, "What is a screener survey?" https://www.lyssna.com/blog/screener-survey/ | At most 10 questions, logic, tone, pilot | screener-template.md |
| ConsentKit/Participant Kit, "How to write great UX research screener surveys" https://consentkit.com/ux-research-screener | Wide-to-narrow funnel, disqualified people with extra questions, screener ethics/accessibility | screener-template.md |
| IxDF, "What is Participant Screening?" https://www.interaction-design.org/literature/topics/participant-screening | Psychographic criteria, non-revealing questions, floaters, verification, channels | screener-template.md, SKILL.md sections 3-4 |
| Nightingale, "Participant Screening ... Step-by-Step" https://nightingaledesignresearch.com/insights/participant-screening-for-effective-research-a-step-by-step-guide/ | Steps: goals, existing data, criteria, screener, pilot, iterate | SKILL.md sections 1 and 3 |
| NN/g, "Obtaining Consent for User Research" https://www.nngroup.com/articles/informed-consent/ (and #consent-form) | Consent content, modular, exceptions, guardian, copy | consent-template.md, SKILL.md section 6 |
| NN/g, sample consent form (PDF) https://media.nngroup.com/media/articles/attachments/NNg_Example_Consent_Form.pdf | Structure of a real consent form | consent-template.md |
| NN/g, "How to Conduct Usability Studies for Accessibility" https://www.nngroup.com/reports/how-to-conduct-usability-studies-accessibility/ | Only the paid report's summary page: in-person sessions with the usual technology, 40 tips | accessibility-in-research.md section 8 (limited content) |
| Dscout, "Accessible User Research Part 1" https://dscout.com/people-nerds/accessible-user-research-1 | Prior audit, two ways to include, timing, budget, location | accessibility-in-research.md sections 1-3, 7 |
| Dscout, "Accessible User Research Part 2" https://dscout.com/people-nerds/accessible-user-research-2 | Recruiting by technology, prototype fidelity, materials, pilot | accessibility-in-research.md sections 4-9 |
| Dscout, "Inclusive research guidelines" https://help.dscout.com/hc/en-us/articles/360048893651-Inclusive-Research-Guidelines | Language, recruit by behavior, retraumatization, adjustments message | accessibility-in-research.md section 10 |
| Dscout, "Inclusive and Accessible UX: Starter Syllabus" https://dscout.com/people-nerds/inclusive-and-accessible-ux-a-starter-syllabus | Only mentions free templates (adjustments checklist, inclusive screener questions) | A hint to expand; no content of its own |
| Optimal Workshop, "Recruitment" https://www.optimalworkshop.com/product/participant-recruitment | Commercial page; no methodological content | Not used |

## Added in the v2 review (communications, scored screener, panel hygiene)
| Title and URL | What it provides | Where it is used |
|---|---|---|
| Great Question, "26 Claude skills for UX research" (Screener builder and Panel data steward skills) https://greatquestion.co/ | Ideas: separate hard filters from preferences, attention questions, variants of the same value, corrections only with human approval. Rewritten, not copied | scored-screener.md, panel-hygiene.md |
| UXR Strategist (N. Anderson), skill catalog: Screener Builder, Participant Communications, Consent Form Builder | Only the catalog idea (which communications to cover) | participant-emails.md |
| rampstackco/ux-research (Recruit) | Idea of required inputs and routing | SKILL.md |
| GDPR, art. 5.1 (c) data minimization and (e) storage limitation https://gdpr-info.eu/art-5-gdpr/ (checked 2026) | The only new regulatory reference; adjust to local law | panel-hygiene.md section 4 |

Note: no new figures were added. The reminder timings (24 h and 1 h), the score weights, the waiting period between studies and the interview range of 5-8 are heuristics of ours, not published standards. The list of job-title abbreviations in `scripts/panel_hygiene.py` is an awareness aid, not a source-backed taxonomy.
