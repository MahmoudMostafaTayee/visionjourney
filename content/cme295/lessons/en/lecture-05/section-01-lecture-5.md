---
lesson_id: section-01-lecture-5
course_id: lecture-05
lang: en
order_index: 1
title: Lecture 5
description: 'Slides 1–26 of lecture 5: 14 slides from the original deck.'
meta_title: Lecture 5 — Lecture 5
meta_description: Slide-by-slide walkthrough of Lecture 5, lecture 5.
meta_keywords: Lecture 5, lecture 5, slides
---

## Lecture 5

:::slide{src="../../slides/lecture-05/slide-001.webp" n="1"} Lecture 5

- CME 295: Transformers &
- Large Language Models
- Afshine Amidi & Shervine Amidi
:::

:::slide{src="../../slides/lecture-05/slide-004.webp" n="4"} Recap of last episodes…

- Initialized model
- Pretraining Finetuning Preference tuning
- Model with "basic
- Model tuned for Model aligns with
- knowledge" about
- speciﬁc tasks (human) preferences
- language, code, etc.
:::

:::slide{src="../../slides/lecture-05/slide-005.webp" n="5"} Today's focus

- Initialized model
- Pretraining Finetuning Preference tuning
- Model with "basic
- Model tuned for Model aligns with
- knowledge" about
- speciﬁc tasks (human) preferences
- language, code, etc.
:::

:::slide{src="../../slides/lecture-05/slide-006.webp" n="6"} Preference tuning

- Transformers &
- Data collection
- Large Language
- RLHF
- Models DPO
:::

:::slide{src="../../slides/lecture-05/slide-009.webp" n="9"} Preference tuning

- Context. Model may misbehave. Need to inject negative signals.
- I'd suggest you do not
- Suggest a new activity I
- LLM spend much time with your
- could do with my teddy bear. SFT
- teddy bear at all.
- Idea. Collect preference pairs and train the model on it.
- Of course! Teddy bears not only make awesome
- companions for a delightful sleep, but can I'd suggest you do not
- also be great buddies for fun activities. How spend much time with your
- about you both watch a movie together? teddy bear at all.
:::

:::slide{src="../../slides/lecture-05/slide-013.webp" n="13"} Why preference tuning?

- Easier to compare (e.g. A better than B) than generate (e.g. generate A from
- scratch)
- Distribution is very important for SFT: easy to "mess up"
- Not scalable: data quality is very important and hard to get
- However, "model misbehaving" can also be a good wake-up call to check SFT
- data quality
:::

:::slide{src="../../slides/lecture-05/slide-014.webp" n="14"} Preference tuning

- Transformers &
- Data collection
- Large Language
- RLHF
- Models DPO
:::

:::slide{src="../../slides/lecture-05/slide-019.webp" n="19"} Preference data

- Observation = (prompt , response )
- Pointwise Pairwise Listwise
- Obs 1 0.4 Obs 1 < Obs 2 Obs 2 1
- Obs 2 0.9 Obs 1 > Obs 3 Obs 1 2
- Obs 3 0.1 Obs 1 > Obs 4 Obs 4 3
- Obs 4 0.2 Obs 2 > Obs 3 Obs 3 4
:::

:::slide{src="../../slides/lecture-05/slide-021.webp" n="21"} Recipe to get (pairwise) preference data

- 1. Generate pair of responses for the same prompt
- Input via logs / reference distribution
- Output via SFT model with / synthetic / rewrites
- 2. Label and
- Human rating
- Proxies (e.g. LLM-as-a-judge, BLEU, ROUGE, etc.)
- Variants: binary scale (better or worse) vs "nuanced" scale
:::

:::slide{src="../../slides/lecture-05/slide-022.webp" n="22"} Preference tuning

- Transformers &
- Data collection
- Large Language
- RLHF
- Models DPO
:::

:::slide{src="../../slides/lecture-05/slide-023.webp" n="23"} RL formulation

- Agent
- State
- Reward
- Action
- Environment
- Policy
:::

:::slide{src="../../slides/lecture-05/slide-024.webp" n="24"} RL formulation for LLMs

- LLM
- State
- Reward
- Action
- Environment
- Policy
:::

:::slide{src="../../slides/lecture-05/slide-025.webp" n="25"} RL formulation for LLMs

- LLM
- Input so far
- Reward
- Action
- Environment
- Policy
:::

:::slide{src="../../slides/lecture-05/slide-026.webp" n="26"} RL formulation for LLMs

- LLM
- Input so far
- Reward
- Next token
- Environment
- Policy
:::
