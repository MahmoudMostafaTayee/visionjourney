---
lesson_id: section-04-can-we-use-transformers-for-other-things
course_id: lecture-09
lang: en
order_index: 4
title: Can we use Transformers for other things?
description: 'Slides 44–69 of lecture 9: 17 slides from the original deck.'
meta_title: Can we use Transformers for other things? — Lecture 9
meta_description: Slide-by-slide walkthrough of Can we use Transformers for other
  things?, lecture 9.
meta_keywords: Can we use Transformers for other things?, lecture 9, slides
---

## Can we use Transformers for other things?

:::slide{src="../../slides/lecture-09/slide-044.webp" n="44"} Can we use Transformers for other things?

- Context
- Introduced in 2017 for machine translation
- Relies on self-attention
- Concepts of query, key, value
- Beneﬁts
- Weaker inductive biases
- More generalizability
- " Attention Is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-09/slide-045.webp" n="45"} Refresher on attention mechanism

- Concept of Query, Key, Value
- " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
:::

:::slide{src="../../slides/lecture-09/slide-047.webp" n="47"} Attention mechanism…

- Figure adapted from " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
:::

:::slide{src="../../slides/lecture-09/slide-048.webp" n="48"} Attention mechanism…for images!

- Figure adapted from " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
:::

:::slide{src="../../slides/lecture-09/slide-049.webp" n="49"} Adapting Transformer architecture for images

- How to adapt Transformer for
- image understanding tasks?
- " Attention Is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-09/slide-050.webp" n="50"} Adapting Transformer architecture for images

- Class
- probabilities
- Projection
- Figure adapted from " Attention Is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-09/slide-051.webp" n="51"} Vision Transformer

- ViT = Vision Transformer
- " An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale ", Dosovitskiy et al., 2020.
:::

:::slide{src="../../slides/lecture-09/slide-053.webp" n="53"} End-to-end example using ViT

- Linear D
:::

:::slide{src="../../slides/lecture-09/slide-058.webp" n="58"} End-to-end example using ViT

- position-aware embedding
- [CLS]
:::

:::slide{src="../../slides/lecture-09/slide-061.webp" n="61"} End-to-end example using ViT

- encoded embeddings
- ViT architecture
- ENCODER
- [CLS]
:::

:::slide{src="../../slides/lecture-09/slide-062.webp" n="62"} End-to-end example using ViT

- teddy bear
- Class
- FFN
- ViT architecture
- ENCODER
- [CLS]
:::

:::slide{src="../../slides/lecture-09/slide-063.webp" n="63"} VLM = Vision Language Model

- ? Very cute!
- How cute is this teddy bear?
:::

:::slide{src="../../slides/lecture-09/slide-064.webp" n="64"} Method 1: recycle decoder-only architecture

- "Typical" LLM Very cute!
- How cute is this teddy bear?
:::

:::slide{src="../../slides/lecture-09/slide-065.webp" n="65"} Method 1: recycle decoder-only architecture

- " Visual Instruction Tuning ", Liu et al., 2023.
:::

:::slide{src="../../slides/lecture-09/slide-067.webp" n="67"} Method 2: leverage cross-attention layer

- Very cute!
- Decoder with
- cross-attention
- How cute is this teddy bear?
:::

:::slide{src="../../slides/lecture-09/slide-068.webp" n="68"} Method 2: leverage cross-attention layer

- " The Llama 3 Herd of Models ", Llama Team, 2024.
:::

:::slide{src="../../slides/lecture-09/slide-069.webp" n="69"} Transformer-based architectures

- Transformers are actually used in a lot of diﬀerent places!
- Text generation. CME 295!
- Vision understanding. Vision Transformer (ViT)
- Image generation. Diﬀusion Transformer (DiT), MultiModal-DiT (MM-DiT), etc.
- and many others (recommendation, speech, etc.)
:::
