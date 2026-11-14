---
lesson_id: section-05-current-approach-and-limitations
course_id: lecture-09
lang: en
order_index: 5
title: Current approach and limitations
description: 'Slides 81–98 of lecture 9: 9 slides from the original deck.'
meta_title: Current approach and limitations — Lecture 9
meta_description: Slide-by-slide walkthrough of Current approach and limitations,
  lecture 9.
meta_keywords: Current approach and limitations, lecture 9, slides
---

## Current approach and limitations

:::slide{src="../../slides/lecture-09/slide-081.webp" n="81"} Current approach and limitations

- Paradigm. AutoRegressive Modeling (ARM)
- A teddy bear is ?
- AutoRegressive LLM
- [BOS] A teddy bear is
- Problem. Inference-time generation is not parallelizable (although training is)
:::

:::slide{src="../../slides/lecture-09/slide-082.webp" n="82"} Alternative approach in the news

- Diﬀusion-based LLM , showcased by Google during I/O on May 20th 2025.
- Announcement on TechCrunch , November 6th 2025.
- Inception website , screenshot taken on November 26th 2025.
- ByteDance announcement , July 31st 2025.
:::

:::slide{src="../../slides/lecture-09/slide-086.webp" n="86"} Context on image generation models

- Intuition
- The sculpture is already complete within
- Noise is easy to sample the marble block, before I start my work.
- It is already there, I just have to chisel
- Learned transformation
- away the superﬂuous material.
- Mathematically well-deﬁned
- –Michelangelo
- Analogy. Building a sculpture
:::

:::slide{src="../../slides/lecture-09/slide-087.webp" n="87"} High-level goal of image generation models

- Goal
- Learn some transformation that goes
- from noise to desired data distribution
:::

:::slide{src="../../slides/lecture-09/slide-089.webp" n="89"} Intuition behind diﬀusion for images

- 1. Add noise to image (forward process)
- 2. Learn to denoise it (reverse process)
- " Denoising Diﬀusion Probabilistic Models ", Ho et al., 2020.
:::

:::slide{src="../../slides/lecture-09/slide-090.webp" n="90"} From image to text

- MASK
- Image Text
:::

:::slide{src="../../slides/lecture-09/slide-092.webp" n="92"} Intuition behind diﬀusion for text

- 1. Mask tokens with some probability (forward process)
- A teddy bear is reading A MASK bear is MASK MASK MASK MASK MASK MASK
- 2. Learn to unmask tokens (reverse process)
- MASK MASK MASK MASK MASK A MASK bear is MASK A teddy bear is reading
- " Denoising Diﬀusion Probabilistic Models ", Ho et al., 2020.
:::

:::slide{src="../../slides/lecture-09/slide-096.webp" n="96"} Diﬀusion in LLMs

- MDM = Masked Diﬀusion Model
- Decoding done in fewer forward passes!
- A teddy bear is reading
- Diffusion LLM
- MASK MASK MASK MASK MASK
- Suggested readings:
- - " Discrete Diﬀusion Modeling by Estimating the Ratios of the Data Distribution ", Lou et al., 2023.
- - " Simple and Eﬀective Masked Diﬀusion Language Models ", Sahoo et al., 2024.
- - " Large Language Diﬀusion Models ", Nie et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-098.webp" n="98"} Discussion

- Advantages.
- ⚡ 10x output tokens per second compared to ARM
- 💻 Better suited for some tasks
- Challenges and current work.
- Performance
- Adapt ARM-based techniques
:::
