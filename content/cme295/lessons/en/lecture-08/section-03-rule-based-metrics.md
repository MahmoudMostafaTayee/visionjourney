---
lesson_id: section-03-rule-based-metrics
course_id: lecture-08
lang: en
order_index: 3
title: Rule-based metrics
description: 'Slides 28–37 of lecture 8: 6 slides from the original deck.'
meta_title: Rule-based metrics — Lecture 8
meta_description: Slide-by-slide walkthrough of Rule-based metrics, lecture 8.
meta_keywords: Rule-based metrics, lecture 8, slides
---

## Rule-based metrics

:::slide{src="../../slides/lecture-08/slide-028.webp" n="28"} Rule-based metrics

- Idea. Write labels once, and use it as reference
- Compare via rule-based metrics
- 📄 Human labels
- LLM
- seen as references
:::

:::slide{src="../../slides/lecture-08/slide-030.webp" n="30"} Common rule-based metrics

- METEOR. Metric for Evaluation of Translation with Explicit ORdering
- " METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments ", Banerjee et al., 2005.
:::

:::slide{src="../../slides/lecture-08/slide-032.webp" n="32"} Common rule-based metrics

- METEOR. Metric for Evaluation of Translation with Explicit ORdering
- BLEU. BiLingual Evaluation Understudy
- " BLEU: A Method for Automatic Evaluation of Machine Translation ", Papineni et al., 2002.
:::

:::slide{src="../../slides/lecture-08/slide-033.webp" n="33"} Common rule-based metrics

- METEOR. Metric for Evaluation of Translation with Explicit ORdering
- BLEU. BiLingual Evaluation Understudy
- ROUGE. Recall-Oriented Understudy for Gisting Evaluation
- Many variants (ROUGE-N, ROUGE-L, etc.) with suite of metrics
- " ROUGE: A Package for Automatic Evaluation of Summaries ", Lin et al., 2004.
:::

:::slide{src="../../slides/lecture-08/slide-035.webp" n="35"} Limitations

- Does not take into account stylistic variations
- A plush teddy bear can comfort a child during bedtime.
- Soft stuffed bears often help kids feel safe as they
- fall asleep.
- Many youngsters rest more easily at night when they
- cuddle a gentle toy companion.
:::

:::slide{src="../../slides/lecture-08/slide-037.webp" n="37"} Limitations

- Does not take into account stylistic variations
- Correlation with human rating is not that great
- Still requires human ratings!
:::
