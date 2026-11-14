---
lesson_id: section-04-increasing-output-length-phenomenon
course_id: lecture-06
lang: en
order_index: 4
title: '"Increasing output length" phenomenon'
description: 'Slides 101–130 of lecture 6: 14 slides from the original deck.'
meta_title: '"Increasing output length" phenomenon — Lecture 6'
meta_description: Slide-by-slide walkthrough of "Increasing output length" phenomenon,
  lecture 6.
meta_keywords: '"Increasing output length" phenomenon, lecture 6, slides'
---

## "Increasing output length" phenomenon

:::slide{src="../../slides/lecture-06/slide-101.webp" n="101"} "Increasing output length" phenomenon

- Small
- Big
:::

:::slide{src="../../slides/lecture-06/slide-105.webp" n="105"} "Increasing output length" phenomenon

- Bad
- Short output incentive!
- Long output
:::

:::slide{src="../../slides/lecture-06/slide-108.webp" n="108"} Mitigating "increasing length" phenomenon

- Problem.
- Remedy. Equalize token-level contributions
- DAPO
- " DAPO: An Open-Source LLM Reinforcement Learning System at Scale ", Yu et al., 2025.
:::

:::slide{src="../../slides/lecture-06/slide-111.webp" n="111"} Mitigating "increasing length" phenomenon

- Problem.
- Remedy. Equalize token-level contributions
- DAPO
- Dr. GRPO
- " Understanding R1-Zero-Like Training: A Critical Perspective ", Liu et al., 2025.
:::

:::slide{src="../../slides/lecture-06/slide-112.webp" n="112"} Exploration of other adjustments

- Bias linked to level of diﬃculty
- " Understanding R1-Zero-Like Training: A Critical Perspective ", Liu et al., 2025.
:::

:::slide{src="../../slides/lecture-06/slide-114.webp" n="114"} Exploration of other adjustments

- Bias linked to level of diﬃculty
- Encourage diversity
- " DAPO: An Open-Source LLM Reinforcement Learning System at Scale ", Yu et al., 2025.
:::

:::slide{src="../../slides/lecture-06/slide-115.webp" n="115"} Exploration of other adjustments

- Bias linked to level of diﬃculty
- Encourage diversity
- …among others!
:::

:::slide{src="../../slides/lecture-06/slide-116.webp" n="116"} Reasoning models

- Transformers &
- Scaling with RL
- Large Language
- GRPO
- Models Applications
:::

:::slide{src="../../slides/lecture-06/slide-119.webp" n="119"} Stitching it all together

- Base "Traditional" Reasoning
- model model models
- Proof of
- V3-Base V3 R1-Zero concept
- R1
- Full pipeline
:::

:::slide{src="../../slides/lecture-06/slide-122.webp" n="122"} DeepSeek R1-Zero 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- MoE
- ~ 671B total, ~ 37B active
- Figure from " DeepSeek-V3 Technical Report ", DeepSeek-AI, 2024.
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-124.webp" n="124"} DeepSeek R1-Zero 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 GRPO with reasoning data: R1-Zero
- A conversation between User and Assistant. The user asks a question, and the
- Assistant solves it. The assistant first thinks about the reasoning process
- in the mind and then provides the user with the answer. The reasoning
- process and answer are enclosed within <think> </think> and <answer>
- </answer> tags, respectively, i.e., <think> reasoning process here </think>
- <answer> answer here </answer>.
- User: <this placeholder is replaced by a reasoning query>
- Assistant:
- Template
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-126.webp" n="126"} DeepSeek R1-Zero 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 GRPO with reasoning data: R1-Zero
- Beneﬁts Challenges
- Reasoning abilities without Chains of reasoning have
- any SFT formatting and readability
- issues
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-128.webp" n="128"} DeepSeek R1 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- MoE
- ~ 671B total, ~ 37B active
- Figure from " DeepSeek-V3 Technical Report ", DeepSeek-AI, 2024.
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-130.webp" n="130"} DeepSeek R1 's training recipe

- 1 Pretrain model with "traditional" techniques: V3-Base
- 2 "Small-scale" SFT with reasoning data
- Data source: long CoTs generated with R1-Zero and rewritten by
- humans
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::
