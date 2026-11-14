---
lesson_id: section-03-motivation
course_id: lecture-03
lang: en
order_index: 3
title: Motivation
description: 'Slides 18–31 of lecture 3: 8 slides from the original deck.'
meta_title: Motivation — Lecture 3
meta_description: Slide-by-slide walkthrough of Motivation, lecture 3.
meta_keywords: Motivation, lecture 3, slides
---

## Motivation

:::slide{src="../../slides/lecture-03/slide-018.webp" n="18"} Motivation

- Idea. Not all weights are useful in the forward pass
- Subset of the huge
- model
:::

:::slide{src="../../slides/lecture-03/slide-021.webp" n="21"} Motivation

- x 2
:::

:::slide{src="../../slides/lecture-03/slide-022.webp" n="22"} Motivation

- x 2
:::

:::slide{src="../../slides/lecture-03/slide-024.webp" n="24"} Overview of MoEs

- MoE = Mixture of Experts
- Dense MoE. Output is weighted
- average of all expert outputs.
- 0.1 1
- 0.8
- x 2
- 0.05
:::

:::slide{src="../../slides/lecture-03/slide-025.webp" n="25"} Overview of MoEs

- MoE = Mixture of Experts
- Sparse MoE. Output is weighted
- average of selected expert outputs.
- x 2
- n Via top-k selection
- " Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer ", Shazeer et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-028.webp" n="28"} MoE in Transformer-based models

- Routing done for each token!
- FFNN
- x FFNN
- FFNN
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-030.webp" n="30"} Training challenges include routing collapse

- Symptom. Same expert gets selected most of the time.
- "routing collapse"
- Remedy. Force other experts to be "part of the game" too via auxiliary loss:
- = fraction of tokens routed to expert i
- = average routing probability for expert i
- " " Switch Transformers: Scaling to Trillion Parameter Models with Simple and Eﬃcient Sparsity Switch Transformers: Scaling to Trillion Parameter Models with Simple and Eﬃcient Sparsity ", Fedus et al., 2021. ", Fedus et al., 2021.
:::

:::slide{src="../../slides/lecture-03/slide-031.webp" n="31"} Interpreting experts

- Each color represent an expert
- " Mixtral of Experts ", Jiang et al., 2024.
:::
