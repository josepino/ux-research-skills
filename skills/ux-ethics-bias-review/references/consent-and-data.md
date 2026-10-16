# Consent, privacy and data (detail)

Read this file when you must draft or audit a consent form, decide whether one is needed, evaluate incentives, or review data handling (including AI and big data). Write deliverables in the user's language.

## Contents
1. What informed consent is and when a form is NOT needed
2. Anatomy of a consent form (9-part checklist)
3. Populations that cannot consent alone
4. Incentives: fair pay or coercion?
5. Participant data: life cycle
6. Big data and third-party data
7. AI in analysis: what to verify
8. Cases to discuss (Facebook 2012/2014, OkCupid 2014)

## 1. Informed consent
It is a two-way exchange: (a) the researcher explains what taking part involves and what consequences it may have; (b) the person understands it and decides voluntarily. The form is only the written proof of that exchange (NN/g).

Why written and not "I'll explain it verbally": it informs everyone with the same level of detail (participant 1 and participant 1000, with any researcher), leaves a trail, protects the participant if the plan changes, and forces you to think about what data you really need.

Common trap: an informal call does not require a form, but as soon as you transcribe quotes or share that person's data with the team, you are using their data in a way they did not accept. Ask for consent before recording or quoting.

**Reasonable exceptions** (NN/g): an A/B test (routine product use, the individual data point only adds to a statistic) needs no form; an intercept study needs no long form, but does need a short agreement screen saying how the information is used, stored, shared and deleted. If you intercept in a physical venue, get written permission from the establishment (in many countries soliciting on private property is illegal).

## 2. Anatomy of a consent form
1. High-level purpose: enough to inform without revealing hypotheses that bias. "Getting to know our customers" does not work; "improving this product" or "planning future services" does.
2. Format: activities, tasks, how data is collected, interaction with the researcher and a defined duration. Avoid "umbrella" consents with no end date (unspecific and abusable).
3. Voluntary participation clause and withdrawal without consequences at any time (signing "feels final"; reassure).
4. Data handling: is it anonymized and how much? Who has access and where is it stored? Is it published? When are raw recordings deleted? Can they ask you to delete them?
5. **Modular** consent: separate boxes to participate, to record audio, to record video and to publish. Someone who declines recording can still participate; this raises participation.
6. Compensation (if any): say it does not depend on performance or on giving positive feedback. In-person trick: pay at the start, right after the signature.
7. Guardian or responsible adult: their own signature block when the participant is a minor or an adult under guardianship.
8. Debrief sheet (optional): detail of the purpose handed out at the end so as not to condition behavior during the session.
9. Always hand over a signed copy and a contact for questions.

If you hide the brand or the objective for validity, reveal it as soon as possible and let the person withdraw their consent. If you foresee that many would withdraw on learning it, rethink the study (IxDF).

## 3. Who cannot consent alone (NN/g)
Minors, adults with cognitive impairment, people without literacy or without full capacity (for example under the effects of alcohol/drugs) need consent from the responsible person even if the risk is low. People in prison: voluntariness is rarely real; committee approval and a representative are usually required as well. Refer to legal/committee. In low-risk studies you can research sensitive topics or vulnerable populations, but with extra precautions and by communicating the possible impact in advance.

## 4. Incentives
- Coercion = a reward so high that someone takes part despite discomfort with the topic or without fitting the profile. Proportionality and freedom to choose are the criterion (Tremendous).
- Higher risk with vulnerable people (minors, people in financial difficulty) or when more long-term risk is accepted for an immediate payment.
- Product incentive/discount: can skew toward favorable opinions because participants want your product. Let them choose among several rewards with a cap.
- Pay promptly; it signals respect for their time. If recruiting is hard, perhaps the incentive is low for the effort.
- Two Tremendous/Lyssna sources give dollar ranges: take them as market reference, not as an ethical norm, and adjust to your country.
- A study cited by Tremendous (Singer, University of Michigan) reports that cash yields more response than other gifts and that prepayment yields more than a promise. It is survey evidence, not interview evidence.

## 5. Data life cycle
Collect only what is needed -> store with restricted access -> pseudonyms in quotes and reports -> explicit permission for images of homes, vehicles, offices -> share only with whom it was agreed -> delete what is irrelevant at the end. Practical rule (IxDF): imagine someone stole that data tomorrow; if it worries you, do not keep it. If local regulation applies (GDPR/CPRA, personal data laws), refer to legal/DPO. Screeners also require consent and compliance (Participant Kit, formerly Consent Kit).
Example of care: show photos and material to participants before publicizing a finding if they could be exposed (for example breaking safety procedures and losing their job).

For your own product analytics, "privacy-first" tools exist (Matomo, self-hosting): useful as an alternative when you do not want to send user data to third parties. This is the vendor's marketing claim; verify before recommending.

## 6. Big data and third-party data (Hurree, 2025)
- Consent: in big data you cannot inform about every future use; "broad consent" (authorizes secondary uses) and "tiered consent" (specific uses) emerged. Some consider them a dilution of the concept.
- A cited figure (Ofcom): 65% of internet users accept terms and conditions without reading them. That is why "it was in the T&Cs" is not informed consent.
- Conscious vs non-conscious transfer: in the second case (the person does not know it is collected) fuels the feeling of surveillance.
- Cross-referencing sources can reveal sensitive traits (orientation, ideology) that nobody handed over.
- Algorithmic bias: models trained on unbalanced data reproduce inequality (cited case: datasets of ~77% men and >83% light skin in facial recognition). Ask for diversity in data, audits and governance.
- Minimum practices: encryption, audits, training, fast breach detection and notice. Propose a data-use code of conduct.

## 7. AI in analysis (NN/g, 2023; the article links to newer NN/g guidance)
Early evaluation, with limitations that may have improved: check the date of the tool.
- Text only: do not analyze usability tests from the transcript alone; participants do not verbalize every click or micro-interaction.
- Vague summaries ("present the information clearly") and unprioritized because they do not know the study's goals or context.
- No verifiable quotes (session, minute, clip): demand traceability. If the tool mixes your notes with the transcript, the separation between interpretation and what was said is lost: an ethical reporting problem.
- "AI has no bias" is false: there are systemic, statistical and human biases (anchoring when using its results). It can, however, relieve confirmation bias when evaluating your own designs.
- Before uploading transcripts: is there consent for that processing? Was it anonymized? Does the provider train on your data?

## 8. Cases
- **Facebook (experiment 2012, published 2014)**: altered the tone of the feed of 689,000 users for a week; the effect was minimal but the scandal was large; a survey by The Guardian reported 84% lost trust (IxDF). No consent and possible emotional harm.
- **OkCupid (2014)**: showed inflated compatibility to low-compatibility pairs (with 30% real vs 90% shown, the chance of writing went from 14.2% to 16.9% according to Infobae) and then revealed the truth. Its co-founder defended that "every site experiments"; a lawyer quoted by the BBC warned of the risk to trust. Lesson: A/B tests being routine does not authorize manipulating information that affects personal decisions.
