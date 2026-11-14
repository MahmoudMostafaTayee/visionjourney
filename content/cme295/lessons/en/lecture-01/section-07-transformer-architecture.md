---
lesson_id: section-07-transformer-architecture
course_id: lecture-01
lang: en
order_index: 7
title: Transformer architecture
description: 'Slides 80–88 of lecture 1: 9 slides from the original deck.'
meta_title: Transformer architecture — Lecture 1
meta_description: Slide-by-slide walkthrough of Transformer architecture, lecture
  1.
meta_keywords: Transformer architecture, lecture 1, slides
---

## Transformer architecture

:::slide{src="../../slides/lecture-01/slide-080.webp" n="80"} Transformer architecture

- Attention layer (MHA)
- Self-attention (Encoder-Encoder,
- Decoder-Decoder)
- Encoder-Decoder attention layer
- Feed Forward Neural Network (FFNN)
- Positional Encoding (PE)
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-081.webp" n="81"} Input

- Overview
- Text is "tokenized"
- Learned embeddings for tokens
- Parameters
- V : vocabulary size
- d_model : embedding dimensions
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-082.webp" n="82"} ... with a trick!

- Positional encoding
- Idea:
- Add position information to inputs
- Can be either learned or hardcoded
- +1 max
- dot product
- osition osition
- P P
- -1 min
- Dimension Position
- Goal: let model understand relative input position
- Left ﬁgure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
- Right ﬁgures adapted from “ Transformer Architecture: The Positional Encoding ”, Kazemnejad, 2019.
:::

:::slide{src="../../slides/lecture-01/slide-083.webp" n="83"} Encoder

- Overview
- Encoder-Encoder attention / self-attention
- Feed Forward Neural Network
- Normalization layer
- Parameters
- N : layers stacked
- h : number of attention heads
- d_FF , d_key , d_value : sub-layer dimension
- d_model : embedding dimensions
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-084.webp" n="84"} Output "shifted right"

- Overview
- Learned embeddings for output tokens
- In practice, will start with [BOS] during
- translation
- Parameters
- V : vocabulary size
- d_model : embedding dimensions
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-085.webp" n="85"} Decoder

- Overview
- Decoder-Decoder attention / self-attention
- Encoder-Decoder attention
- Feed Forward Neural Network
- Normalization layer
- Parameters
- N : layers stacked
- h : number of attention heads
- d_FF , d_key , d_value : sub-layer dimension
- d_model : embedding dimensions
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-086.webp" n="86"} Output

- Overview
- Linear projection
- Classiﬁcation problem that outputs
- probability of belonging to a class, where
- class = word
- Parameters
- V : vocabulary size
- d_model : embedding dimensions
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-01/slide-087.webp" n="87"} Computational tricks

- Multi-head attention
- Idea:
- Run multiple self-attention layers in parallel
- Beneﬁts:
- Enables the model to capture diﬀerent
- attention features in parallel
- Comparison: multiple ﬁlters of a convolutional
- layer in computer vision
- Left ﬁgure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017. Right ﬁgure from “ VIP cheatsheets for Stanford’s CS 230 ”, Amidi, 2019.
:::

:::slide{src="../../slides/lecture-01/slide-088.webp" n="88"} Computational tricks

- Label smoothing
- Idea:
- 2015 vision paper : overconﬁdence is bad
- Introduce noise in true labels
- Beneﬁts:
- General technique that prevents overﬁtting
- Improves accuracy and BLEU score
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::
