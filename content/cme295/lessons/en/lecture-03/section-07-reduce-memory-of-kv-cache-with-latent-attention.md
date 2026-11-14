---
lesson_id: section-07-reduce-memory-of-kv-cache-with-latent-attention
course_id: lecture-03
lang: en
order_index: 7
title: Reduce memory of KV cache with latent attention
description: 'Slides 115–125 of lecture 3: 11 slides from the original deck.'
meta_title: Reduce memory of KV cache with latent attention — Lecture 3
meta_description: Slide-by-slide walkthrough of Reduce memory of KV cache with latent
  attention, lecture 3.
meta_keywords: Reduce memory of KV cache with latent attention, lecture 3, slides
---

## Reduce memory of KV cache with latent attention

:::slide{src="../../slides/lecture-03/slide-115.webp" n="115"} Reduce memory of KV cache with latent attention

- AFTER
- teddy bear
- shared
- x h
- " DeepSeek-V2: A Strong, Economical, and Eﬃcient Mixture-of-Experts Language Model ", by DeepSeek, 2023.
:::

:::slide{src="../../slides/lecture-03/slide-116.webp" n="116"} Token generation tricks

- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-117.webp" n="117"} Speeding up decoding with speculative decoding

- Idea. Use a draft (small) model to generate tokens validated by a target (big) model.
- " Accelerating Large Language Model Decoding with Speculative Sampling ", Chen et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-118.webp" n="118"} Speeding up decoding with speculative decoding

- P1 P2 ... Pk
- is cute and smart
- Draft LLM
- [BOS] my teddy bear
- " Accelerating Large Language Model Decoding with Speculative Sampling ", Chen et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-119.webp" n="119"} Speeding up decoding with speculative decoding

- Q1 Q2 ... Qk Qk+1
- Target LLM
- [BOS] my teddy bear is cute and smart
- " Accelerating Large Language Model Decoding with Speculative Sampling ", Chen et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-120.webp" n="120"} Speeding up decoding with speculative decoding

- Sampling algorithm. We distinguish the following cases:
- If Qi( ) >= Pi( ) token ✅
- token token
- Otherwise
- with probability Qi( ) / Pi( ) token ✅
- token token
- with probability 1 - Qi( ) / Pi( ) token ❌
- token token
- If a rejection happens, re-sample next token with distribution [Qi - Pi]+ and exit
- " Accelerating Large Language Model Decoding with Speculative Sampling ", Chen et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-121.webp" n="121"} Generate several tokens at once via MTP

- MTP = Multi-Token Prediction
- is cute and smart
- LLM
- [BOS] my teddy bear
- " Better & Faster Large Language Models via Multi-token Prediction ", Gloeckle et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-122.webp" n="122"} Generate several tokens at once via MTP

- Idea. Train k prediction heads: same draft and target models!
- t+1 t+2 ... t+k
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-123.webp" n="123"} Challenges

- Categories. Many dimensions to optimize for.
- "Exact" eﬃciency:
- Avoid redundancies
- Memory management
- Reformulate the math
- Approximations:
- Architectural changes
- Embeddings representations
- Token prediction
:::

:::slide{src="../../slides/lecture-03/slide-124.webp" n="124"} Challenges and some remedies

- Categories. Many dimensions to optimize for.
- "Exact" eﬃciency:
- KV cache
- Avoid redundancies
- PagedAttention
- Memory management
- Reformulate the math
- Speculative decoding
- Approximations:
- Grouped query attention
- Architectural changes
- Embeddings representations Latent attention
- Token prediction
- Multi-token prediction
:::

:::slide{src="../../slides/lecture-03/slide-125.webp" n="125"} Thank you for your attention!

:::
