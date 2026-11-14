---
lesson_id: section-06-challenges
course_id: lecture-03
lang: en
order_index: 6
title: Challenges
description: 'Slides 89–111 of lecture 3: 14 slides from the original deck.'
meta_title: Challenges — Lecture 3
meta_description: Slide-by-slide walkthrough of Challenges, lecture 3.
meta_keywords: Challenges, lecture 3, slides
---

## Challenges

:::slide{src="../../slides/lecture-03/slide-089.webp" n="89"} Challenges

- Motivation. Computations are expensive, any way to reduce complexity?
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

:::slide{src="../../slides/lecture-03/slide-090.webp" n="90"} Attention-based tricks

- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-095.webp" n="95"} Reusing computations with KV caching

- Motivation. New token needs to interact with all previous tokens.
- a cute teddy bear is reading
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-100.webp" n="100"} Reusing computations with KV caching

- Motivation. New token needs to interact with all previous tokens.
- Idea. Keep keys and values in a cache.
- From cache From cache
:::

:::slide{src="../../slides/lecture-03/slide-101.webp" n="101"} Reusing computations with KV caching

- Motivation. New token needs to interact with all previous tokens.
- Idea. Keep keys and values in a cache.
- Cache Cache
- KV caching = Key-Value Caching
:::

:::slide{src="../../slides/lecture-03/slide-103.webp" n="103"} Sharing attention heads

- Number of Number of Number of
- query heads key heads value heads
- Number of Number of Number of
- In vanilla MHA, = = = h
- query heads key heads value heads
:::

:::slide{src="../../slides/lecture-03/slide-104.webp" n="104"} Sharing attention heads

- Idea. Share key/value attention heads within groups of queries
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-105.webp" n="105"} Sharing attention heads

- Multi-Query Attention
- (MQA)
- Group-Query Attention
- (GQA)
- Multi-Head Attention
- (MHA)
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-106.webp" n="106"} Sharing attention heads with GQA

- Number of Number of Number of
- query heads key heads value heads
- = h = G < h = G < h
:::

:::slide{src="../../slides/lecture-03/slide-107.webp" n="107"} Manage memory with PagedAttention

- Observation. Lots of memory waste when storing KV cache.
- Figure from " Eﬃcient Memory Management for Large Language Model Serving with PagedAttention ", by Kwon et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-108.webp" n="108"} Manage memory with PagedAttention

- Idea. Store K and V in non-contiguous space to minimize wasted memory.
- Figure from " Eﬃcient Memory Management for Large Language Model Serving with PagedAttention ", by Kwon et al., 2023.
:::

:::slide{src="../../slides/lecture-03/slide-109.webp" n="109"} Reduce memory of KV cache with latent attention

- Goal. Reduce dimension of K and V stored in memory.
- too big
:::

:::slide{src="../../slides/lecture-03/slide-110.webp" n="110"} Reduce memory of KV cache with latent attention

- Solution. Store compressed representations instead!
- big small
- x h
- " DeepSeek-V2: A Strong, Economical, and Eﬃcient Mixture-of-Experts Language Model ", by DeepSeek, 2023.
:::

:::slide{src="../../slides/lecture-03/slide-111.webp" n="111"} Reduce memory of KV cache with latent attention

- BEFORE
- teddy bear
- x h
- " DeepSeek-V2: A Strong, Economical, and Eﬃcient Mixture-of-Experts Language Model ", by DeepSeek, 2023.
:::
