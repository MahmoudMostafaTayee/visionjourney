---
lesson_id: section-06-instruction-tuning-overview
course_id: lecture-04
lang: en
order_index: 6
title: Instruction tuning overview
description: 'Slides 91–108 of lecture 4: 14 slides from the original deck.'
meta_title: Instruction tuning overview — Lecture 4
meta_description: Slide-by-slide walkthrough of Instruction tuning overview, lecture
  4.
meta_keywords: Instruction tuning overview, lecture 4, slides
---

## Instruction tuning overview

:::slide{src="../../slides/lecture-04/slide-091.webp" n="91"} Instruction tuning overview

- Goal. "Graduate" the model to being a helpful assistant.
- Objective function. Predict next token given the input.
- Do X . Sure ...
- LLM
- [BOS] Do X . Sure
- " Finetuned language models are zero-shot learners ", Wei et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-092.webp" n="92"} Instruction tuning overview

- Goal. "Graduate" the model to being a helpful assistant
- Objective function. Predict next token given the input.
- Data mixtures. Can be both human-written and synthetic data.
- Assistant dialogs
- Synthetic instructions
- Maths, reasoning, code
- Safety alignment
- ...
:::

:::slide{src="../../slides/lecture-04/slide-093.webp" n="93"} Instruction tuning overview

- Goal. "Graduate" the model to being a helpful assistant
- Objective function. Predict next token given the input.
- Data mixtures. Can be both human-written and synthetic data.
- Model SFT size (# examples)
- Size. Thousands to millions of examples. GPT-3 13 thousands
- LLaMA 3 10 million
- " Language Models are Few-Shot Learners ", Brown et al., 2020. " The Llama 3 Herd of Models ", LLaMA team, 2024.
:::

:::slide{src="../../slides/lecture-04/slide-095.webp" n="95"} Behavior

- Can I put my Pretrained + No, it might get
- teddy bear in instruction damaged. Try hand
- the washer? tuned LLM washing instead.
:::

:::slide{src="../../slides/lecture-04/slide-096.webp" n="96"} Challenges

- Very high-quality data needed
- Sensitive to prompt distribution
- Generalization
- Diﬃcult to evaluate
- Computationally expensive
:::

:::slide{src="../../slides/lecture-04/slide-098.webp" n="98"} Benchmarks

- Dimensions.
- General knowledge: MMLU
- Basic reasoning: ARC-Challenge
- Math reasoning: GSM8K
- Code generation: HumanEval
- Validity. Recommended to train on the test task to compare across models.
- " Training on the Test Task Confounds Evaluation and Emergence ", Dominguez-Olmedo et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-099.webp" n="99"} "Real-life" feeling

- Idea. Websites like "Chatbot Arena"
- run A/B tests for user prompts.
- Screenshot taken on Tuesday, October 14, 2025 from LMArena > Leaderboard Overview, lmarena.ai/leaderboard .
:::

:::slide{src="../../slides/lecture-04/slide-101.webp" n="101"} "Real-life" feeling

- Beneﬁts. Puts a number on "vibes"
- Outstanding challenges.
- Unequal exposure of models/"cold start" problem
- Easy to "rig"
- User inability to accurately assess important aspects, e.g. factuality
- Personal preference bias (non-representative distribution)
- Safety penalization
- " Exploring and Mitigating Adversarial Manipulation of Voting-Based Leaderboards ", Huang et al., 2025.
:::

:::slide{src="../../slides/lecture-04/slide-102.webp" n="102"} "Real-life" feeling

- Beneﬁts. Puts a number on "vibes"
- Outstanding challenges.
- Unequal exposure of models/"cold start" problem
- Easy to "rig"
- User inability to accurately assess important aspects, e.g. factuality
- Personal preference bias (non-representative distribution)
- Safety penalization
- ...evaluation is a hard problem in itself!
:::

:::slide{src="../../slides/lecture-04/slide-103.webp" n="103"} What we'll see in Lecture 5

- Initialized model
- Pretraining Finetuning Preference tuning
- Model with "basic
- Model tuned for Model does not
- knowledge" about
- speciﬁc tasks misbehave as much
- language, code, etc.
:::

:::slide{src="../../slides/lecture-04/slide-104.webp" n="104"} Summary of lifecycle of an LLM

- Initialized model
- Pretraining Finetuning Preference tuning
- Model with "basic
- Model tuned for Model does not
- knowledge" about
- speciﬁc tasks misbehave as much
- language, code, etc.
- "Alignment" of the model
:::

:::slide{src="../../slides/lecture-04/slide-105.webp" n="105"} Pretraining

- Transformers &
- Training optimizations
- Large Language
- Supervised ﬁnetuning
- Models Parameter-eﬃcient ﬁnetuning
:::

:::slide{src="../../slides/lecture-04/slide-107.webp" n="107"} Parameter-eﬃcient ﬁnetuning with LoRA

- Context. SFT is resource intensive and not everyone has big GPUs.
- Idea. Low-Rank Adaptation (LoRA) approximates matrix with product of two
- low-rank matrices
- = + x
- W W B A
- Discussion.
- Fraction of parameters need to be trained with similar performance
- Other methods include preﬁx tuning and adapters
- " LoRA: Low-Rank Adaptation of Large Language Models ", Hu et al., 2021.
:::

:::slide{src="../../slides/lecture-04/slide-108.webp" n="108"} Finetuning evolution

- Before. "Regular" ﬁnetuning optimizes the full matrix of weights
:::
