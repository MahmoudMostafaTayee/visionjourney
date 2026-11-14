---
lesson_id: section-05-deepseek-r1-s-training-recipe
course_id: lecture-06
lang: en
order_index: 5
title: DeepSeek R1 's training recipe
description: 'Slides 132–148 of lecture 6: 7 slides from the original deck.'
meta_title: DeepSeek R1 's training recipe — Lecture 6
meta_description: Slide-by-slide walkthrough of DeepSeek R1 's training recipe, lecture
  6.
meta_keywords: DeepSeek R1 's training recipe, lecture 6, slides
---

## DeepSeek R1 's training recipe

:::slide{src="../../slides/lecture-06/slide-132.webp" n="132"} DeepSeek R1 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 "Small-scale" SFT with reasoning data
- 3 GRPO with reasoning data
- ~ same RL process as with R1-Zero
- Reward = Formatting + accuracy + language consistency
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-135.webp" n="135"} DeepSeek R1 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 "Small-scale" SFT with reasoning data
- 3 GRPO with reasoning data
- 4 "Large-scale" SFT with reasoning and non-reasoning data
- ~ 600k pairs
- ~ 200k pairs
- Maths, coding, logic
- "General" data
- Rejection sampling of "R1 so far"
- Mostly reuses V3 SFT data
- responses via rules + V3 judge
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-138.webp" n="138"} DeepSeek R1 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 "Small-scale" SFT with reasoning data
- 3 GRPO with reasoning data
- 4 "Large-scale" SFT with reasoning and non-reasoning data
- 5 GRPO with reasoning and non-reasoning data: R1
- "General" data
- Maths, coding, logic Mostly reuses V3 RL data
- Reward = Formatting + accuracy Reward = helpfulness + harmlessness
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-141.webp" n="141"} DeepSeek R1 's results

- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-144.webp" n="144"} And what about distillation?

- Distillation seen in lecture 2 Distillation used here
- generate entire
- R1 responses
- targeted
- R1-Distill
- Goal: match next token distribution Goal: SFT-learn reasoning traces
- Figures from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-147.webp" n="147"} And what about distillation?

- Results.
- Competitive
- "Good" use of compute
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-148.webp" n="148"} Thank you for your attention!

:::
