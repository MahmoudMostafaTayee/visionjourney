---
lesson_id: section-07-finetuning-evolution
course_id: lecture-04
lang: en
order_index: 7
title: Finetuning evolution
description: 'Slides 109–126 of lecture 4: 11 slides from the original deck.'
meta_title: Finetuning evolution — Lecture 4
meta_description: Slide-by-slide walkthrough of Finetuning evolution, lecture 4.
meta_keywords: Finetuning evolution, lecture 4, slides
---

## Finetuning evolution

:::slide{src="../../slides/lecture-04/slide-109.webp" n="109"} Finetuning evolution

- After. LoRA ﬁnetuning optimizes the full matrix of weights
- A r B
- " LoRA: Low-Rank Adaptation of Large Language Models ", Hu et al., 2021.
:::

:::slide{src="../../slides/lecture-04/slide-112.webp" n="112"} Beneﬁt of LoRA: swap matrices = swap tasks

- + x Spam detection task
- W B A
- spam spam
- + x Sentiment extraction task
- W B A
- sentiment sentiment
- + x Translation task
- W B A
- translation translation
:::

:::slide{src="../../slides/lecture-04/slide-113.webp" n="113"} Locations where to apply LoRA

- Originally. As experimented in the original
- paper.
- " LoRA: Low-Rank Adaptation of Large Language Models ", Hu et al., 2021.
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-04/slide-114.webp" n="114"} Locations where to apply LoRA

- Updated guidance. As done and
- recommended nowadays.
- most important location
- " LoRA Without Regret ", Schulman et al., 2025.
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-04/slide-116.webp" n="116"} Training dynamics

- "Fun" facts. Beware of training diﬀerences:
- LoRA needs a higher learning rate than full ﬁne-tuning
- empirical
- LoRA does poorly on large batch size compared to full ﬁne-tuning
- empirical
- " LoRA Without Regret ", Schulman et al., 2025..
:::

:::slide{src="../../slides/lecture-04/slide-120.webp" n="120"} QLoRA

- Idea. Quantize all frozen weights to relieve memory bottleneck.
- + x
- W B A
- stored quantized stored in full precision
- computations in full precision
- QLoRA: Eﬃcient Finetuning of Quantized LLMs , Dettmers et al., 2023.
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-04/slide-121.webp" n="121"} Eﬃcient quantization

- Trick. Use 4-bit NormalFloat (NF4) to best split the space
- Uniform distribution cutoﬀs Based on Normal quantiles
- INT8 NF4
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-123.webp" n="123"} Quantization...

- No quantization Single quantization Double quantization
- Weights
- Quantization
- constants
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-124.webp" n="124"} Quantization...

- Single quantization Double quantization
- Weights
- Quantization
- constants
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-125.webp" n="125"} ...done two times!

- Single quantization Double quantization
- Weights
- Quantization
- constants
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-126.webp" n="126"} QLoRA

- Idea. Quantize all frozen weights to relieve memory bottleneck.
- Beneﬁts.
- VRAM savings enable ﬁnetuning on smaller GPUs, and faster
- Better trade-oﬀ memory resources/quality
- QLoRA: Eﬃcient Finetuning of Quantized LLMs , Dettmers et al., 2023.
:::
