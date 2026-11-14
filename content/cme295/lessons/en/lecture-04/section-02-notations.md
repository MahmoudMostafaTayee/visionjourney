---
lesson_id: section-02-notations
course_id: lecture-04
lang: en
order_index: 2
title: Notations
description: 'Slides 19–36 of lecture 4: 11 slides from the original deck.'
meta_title: Notations — Lecture 4
meta_description: Slide-by-slide walkthrough of Notations, lecture 4.
meta_keywords: Notations, lecture 4, slides
---

## Notations

:::slide{src="../../slides/lecture-04/slide-019.webp" n="19"} Notations

- FLOPs
- FLoating-point OPerations
- Computational performance
- FLOPS or FLOP/s
- FLoating-point OPerations
- per Second
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-021.webp" n="21"} Takeaways

- Scaling.
- Sample eﬃciency.
- " Scaling Laws for Neural Language Models ", Kaplan et al., 2020.
:::

:::slide{src="../../slides/lecture-04/slide-023.webp" n="23"} Takeaways

- Scaling.
- Sample eﬃciency.
- Chinchilla law.
- " Training Compute-Optimal Large Language Models ", Hoﬀmann et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-027.webp" n="27"} Challenges

- Cost. Learned knowledge.
- (At least) millions of dollars ● "Knowledge cutoﬀ"
- Takes time ● Hard to edit knowledge
- Environment / electricity ● "Plagiarism"
- https://platform.openai.com/docs/models/gpt-5 , screenshot taken on October 14, 2025.
:::

:::slide{src="../../slides/lecture-04/slide-028.webp" n="28"} Pretraining

- Transformers &
- Training optimizations
- Large Language
- Supervised ﬁnetuning
- Models Parameter-eﬃcient ﬁnetuning
:::

:::slide{src="../../slides/lecture-04/slide-031.webp" n="31"} Setup of LLM training

- (Many) GPU(s)!
- “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-04/slide-032.webp" n="32"} Recap of LLM training

- Initialization
- Model parameters. O(billions) - O(100s of billions)
- LLM
:::

:::slide{src="../../slides/lecture-04/slide-033.webp" n="33"} Recap of LLM training

- Forward pass . Compute loss.
- Activations. Needed to compute the loss.
- LLM
- Function of model size, batch size, context
- length
:::

:::slide{src="../../slides/lecture-04/slide-034.webp" n="34"} Recap of LLM training

- Backwards pass . Compute gradients.
- Gradients. Needed for weights update.
- LLM
:::

:::slide{src="../../slides/lecture-04/slide-035.webp" n="35"} Recap of LLM training

- Weights update . Update model parameters.
- Optimizer state. Updates the weights.
- LLM
- Adam optimizer
- with:
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
- Suggested readings: " Decoupled Weight Decay Regularization ", Loshchilov et al., 2017 ; " Adam: A Method for Stochastic Optimization ", Kingma et al., 2014.
:::

:::slide{src="../../slides/lecture-04/slide-036.webp" n="36"} Bottleneck: memory

- " NVIDIA H100 Tensor Core GPU ", NVIDIA website.
:::
