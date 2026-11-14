---
lesson_id: section-04-standard-self-attention-computation
course_id: lecture-04
lang: en
order_index: 4
title: Standard self-attention computation
description: 'Slides 55–72 of lecture 4: 10 slides from the original deck.'
meta_title: Standard self-attention computation — Lecture 4
meta_description: Slide-by-slide walkthrough of Standard self-attention computation,
  lecture 4.
meta_keywords: Standard self-attention computation, lecture 4, slides
---

## Standard self-attention computation

:::slide{src="../../slides/lecture-04/slide-055.webp" n="55"} Standard self-attention computation

- WRITE P to HBM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-056.webp" n="56"} Standard self-attention computation

- LOAD P, V from HBM by blocks
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-057.webp" n="57"} Standard self-attention computation

- Compute O
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-058.webp" n="58"} Standard self-attention computation

- WRITE O to HBM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-061.webp" n="61"} Flash Attention in action

- 1 st idea. Minimize read/writes to HBM with "tiling" via SRAM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-062.webp" n="62"} Flash Attention in action

- Trick. No need to compute the full before applying softmax.
- … …
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-068.webp" n="68"} Flash Attention in action

- Load blocks of Q, K, V to SRAM , compute block of O and write the result to HBM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-070.webp" n="70"} Flash Attention in the backwards pass

- 2 nd idea. Sometimes, it is better to recompute instead of storing
- Before After
- Store in the HBM Recompute with tiling via SRAM
- More FLOPs, but less runtime!!
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-071.webp" n="71"} Flash Attention in action

- Results. Flash Attention leads to a signiﬁcant speedup with exact computation
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-072.webp" n="72"} Precision of numbers

- 2.7015402…
- 1.20 15432…
- 2.4024402…
- -0.7055120…
- -1.7067140…
- 0.2741131…
- -1.5312410…
- 0.4025222…
:::
