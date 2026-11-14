---
lesson_id: section-02-rl-formulation-for-llms
course_id: lecture-05
lang: en
order_index: 2
title: RL formulation for LLMs
description: 'Slides 27–46 of lecture 5: 10 slides from the original deck.'
meta_title: RL formulation for LLMs — Lecture 5
meta_description: Slide-by-slide walkthrough of RL formulation for LLMs, lecture 5.
meta_keywords: RL formulation for LLMs, lecture 5, slides
---

## RL formulation for LLMs

:::slide{src="../../slides/lecture-05/slide-027.webp" n="27"} RL formulation for LLMs

- LLM
- Input so far
- Reward
- Next token
- Tokens
- Policy
:::

:::slide{src="../../slides/lecture-05/slide-028.webp" n="28"} RL formulation for LLMs

- LLM
- Input so far
- Reward
- Next token
- Tokens
- Probability of next token
:::

:::slide{src="../../slides/lecture-05/slide-030.webp" n="30"} RL formulation for LLMs

- Idea. Learn so that aligns with human preferences
- LLM
- Input so far
- Human
- preference
- Next token
- Tokens
- Probability of next token
:::

:::slide{src="../../slides/lecture-05/slide-033.webp" n="33"} RLHF overview

- RLHF = Reinforcement Learning from Human Feedback
- ⚖ Step 1 – Reward modeling: Distinguish good from bad!
- Input: (prompt , response )
- Output: quantitative score
- ⚙ Step 2 – Reinforcement learning: Align the model!
- Input: prompt
- Output: response
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::

:::slide{src="../../slides/lecture-05/slide-037.webp" n="37"} Step 1: Reward modeling

- Idea. Know which answers are bad and which are good via Reward Model.
- Suggest a new activity I could do with my teddy bear. prompt
- Of course! Teddy bears not only make awesome
- companions for a delightful sleep, but can also be
- great buddies for fun activities. How about you RM
- both watch a movie together?
- I'd suggest you do not spend
- much time with your teddy RM
- bear at all.
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::

:::slide{src="../../slides/lecture-05/slide-039.webp" n="39"} Step 1: Reward modeling

- Bradley-Terry formulation. Probability that better than is deﬁned as:
- where rewards of respectively
- " The rank analysis of incomplete block designs: I. the method of paired comparisons ", Bradley et al., 1952.
:::

:::slide{src="../../slides/lecture-05/slide-041.webp" n="41"} Step 1: Reward modeling

- Training. Learn based on pairwise preference data
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-05/slide-042.webp" n="42"} Step 1: Reward modeling

- Data.
- O(10,000) observations
- label = human rating (which is where the "HF" from RLHF comes from)
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::

:::slide{src="../../slides/lecture-05/slide-043.webp" n="43"} Step 1: Reward modeling

- Data.
- O(10,000) observations
- label = human rating (which is where the "HF" from RLHF comes from)
- Model.
- Pretrained LLM with classiﬁcation head (instead of next token prediction)
- Encoder-only: BERT and the like via [CLS] projection
- " RewardBench: Evaluating Reward Models for Language Modeling ", Lambert et al., 2024.
:::

:::slide{src="../../slides/lecture-05/slide-046.webp" n="46"} Step 2: Reinforcement learning

- Idea. Change weights of LLM to penalize bad answers and promote good answers
- via Reinforcement Learning using the Reward Model.
- I'd suggest you
- Suggest a new do not spend
- activity I much time with
- could do with LLM
- your teddy bear
- my teddy bear.
- at all.
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::
