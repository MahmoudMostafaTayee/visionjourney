---
lesson_id: "privacy-fairness-and-ethics"
course_id: "responsible-vision"
lang: "en"
order_index: 2
title: "Privacy, Fairness and Ethics"
description: "Face recognition, surveillance, dataset consent, bias measurement and the documentation that makes a vision system accountable."
meta_title: "Privacy, Fairness and Ethics in Computer Vision - Responsible Vision"
meta_description: "Examine face recognition, surveillance, consent, dataset bias, fairness metrics, model cards and the governance of vision systems."
meta_keywords: "face recognition, surveillance, privacy, dataset consent, algorithmic fairness, bias, model card, governance"
---

Vision systems observe people. That makes privacy, consent, fairness and accountability technical requirements, not external constraints to be handled by a policy team after deployment. The choices are embedded in the data, the labels, the metric and the interface.

## Face recognition and surveillance

Face recognition systems convert faces into embeddings and compare them. The technology is accurate enough for some uses and unreliable enough to cause harm in others, particularly across demographics, poses, ages and lighting conditions.

The harm is not only misidentification. Even accurate systems enable surveillance at scale, which changes the power relationship between institutions and individuals. A model that works as specified can still be unacceptable in a given context.

Deployment questions that should precede a technical evaluation:

- Who is being observed, and did they consent?
- What decision does the output trigger, and can it be appealed?
- What is the cost of a false match versus a false non-match?
- Is the system subject to independent audit and retention limits?
- Is the use lawful in the relevant jurisdiction?

:::single-choice{#face-harm} Why is accuracy alone insufficient to justify a face recognition deployment?

::option[Because the system also creates surveillance power and risk of harm that accuracy does not address]{#surveillance-power .correct explanation="Even a highly accurate system can enable unacceptable monitoring or trigger decisions without recourse, which is a governance question."}
::option[Because face recognition is never accurate]{#never-accurate explanation="Accuracy varies by condition and demographic; the argument is about harms beyond error rates, not a blanket accuracy claim."}
::option[Because consent is irrelevant once data is public]{#consent-public explanation="Public availability does not imply consent for identification or surveillance, and legal regimes differ."}
:::

## Dataset consent and provenance

Vision datasets are often scraped from the web. The people depicted did not necessarily consent to being in a dataset, to having their image used for training, or to the downstream use of the resulting model.

Provenance documentation should record where the data came from, under what terms, when it was collected, what filtering was applied and what is known about its demographic composition. This is not bureaucracy: without it, a model cannot be audited for bias or rights violations.

Licensing is separate from consent. A Creative Commons licence on an image permits certain uses but does not necessarily permit biometric processing or surveillance. Dataset licences and model licences are distinct, and the obligations often propagate to derivatives.

:::single-choice{#provenance} Why does dataset provenance matter for model accountability?

::option[Because without knowing origin, terms and composition, bias and rights issues cannot be audited or remedied]{#provenance-audit .correct explanation="Provenance is the evidence base for checking consent, representation and licence compliance, and for tracing harms back to data."}
::option[Because provenance improves model accuracy directly]{#provenance-accuracy explanation="Provenance is a governance and audit property; it does not by itself change accuracy."}
::option[Because licences automatically transfer to model weights]{#licence-transfer explanation="Licence obligations vary and are not automatically resolved by training; they must be analysed explicitly."}
:::

## Measuring bias

Bias in vision has several distinct sources:

- **Representation bias**: some groups or conditions are under-represented in the data.
- **Label bias**: annotators apply inconsistent labels across groups.
- **Measurement bias**: the sensor or pipeline performs differently across skin tones, lighting or hardware.
- **Deployment bias**: the model is used in a context different from the one it was trained for.

Aggregate accuracy hides these. Report performance by subgroup, with confidence intervals. A model with 95 percent overall accuracy can be at 70 percent on a subgroup that matters, and the aggregate number will not show it.

Fairness metrics conflict. Demographic parity requires equal positive rates across groups; equalised odds requires equal true positive and false positive rates; predictive parity requires equal precision. These cannot all hold simultaneously when base rates differ, so the choice is a value judgement about which error is worse for whom.

:::single-choice{#fairness-conflict} Why can fairness metrics not all be satisfied at once?

::option[Because when base rates differ, equal positive rates and equal error rates impose incompatible constraints]{#fairness-impossible .correct explanation="The metrics encode different equalities; with unequal prevalence they cannot all hold, so the choice reflects a judgement about which disparity matters."}
::option[Because the metrics are mathematically undefined]{#fairness-undefined explanation="They are well defined; the conflict is structural, not a definitional gap."}
::option[Because models are always biased]{#always-biased explanation="The conflict is a property of the metrics and base rates, independent of any particular model."}
:::

## Documentation and accountability

Model cards and datasheets document intended use, training data, evaluation results, limitations and ethical considerations. They are not a substitute for evaluation, but they make claims checkable and create a record for later audit.

A useful model card answers:

1. What is the model for, and what is it not for?
2. What data was used, and what is known about its composition?
3. How was performance measured, on which subgroups, with what uncertainty?
4. What are the known failure modes and edge cases?
5. What monitoring, appeal and rollback mechanisms exist?

Accountability requires a named owner and a mechanism for affected people to contest a decision. A model without an appeal path is a system without recourse, regardless of its documentation.

:::callout{type="insight" title="Consent is a process, not a checkbox"}
Consent for data collection is not the same as consent for every downstream use. Systems that infer sensitive attributes, identify individuals or inform decisions about them require ongoing governance, not a one-time licence review.
:::

## Privacy-preserving techniques

Technical mitigations include:

- **De-identification**, which removes or alters identifying features but is often reversible.
- **Federated learning**, which trains on distributed data without centralising it, while still leaking information through gradients.
- **Differential privacy**, which bounds the influence of any single record and provides a formal guarantee at a cost to accuracy.
- **On-device processing**, which avoids transmitting raw data but does not eliminate the need for consent or retention limits.

None of these is sufficient alone. Differential privacy protects against a specific formal threat model; it does not prevent a model from encoding group-level disparities. Federated learning protects raw data centralisation but not inference from model updates.

:::single-choice{#dp-guarantee} What does differential privacy formally guarantee?

::option[That the output distribution changes only slightly when any single record is added or removed]{#dp-guarantee .correct explanation="The guarantee bounds the influence of one individual's data on the output, which limits what can be inferred about that individual."}
::option[That the model cannot be biased]{#dp-bias explanation="Differential privacy protects individual influence, not group fairness; bias can persist under the guarantee."}
::option[That all training data is encrypted]{#dp-encryption explanation="Differential privacy is a statistical guarantee about outputs, not an encryption scheme."}
:::

## Summary

You can now treat ethics and governance as engineering requirements.

1. Evaluate face recognition and surveillance in context, beyond accuracy.
2. Document data provenance, consent and licensing.
3. Measure bias by subgroup and choose fairness metrics deliberately.
4. Write model cards that make claims checkable.
5. Understand the scope and limits of privacy-preserving techniques.
