---
lesson_id: section-02-need-for-position-information
course_id: lecture-02
lang: en
order_index: 2
title: Need for position information
description: 'Slides 12–35 of lecture 2: 12 slides from the original deck.'
meta_title: Need for position information — Lecture 2
meta_description: Slide-by-slide walkthrough of Need for position information, lecture
  2.
meta_keywords: Need for position information, lecture 2, slides
---

## Need for position information

:::slide{src="../../slides/lecture-02/slide-012.webp" n="12"} Need for position information

- Motivation. Direct links "lose" position info
- " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
:::

:::slide{src="../../slides/lecture-02/slide-013.webp" n="13"} Need for position information

- Motivation. Direct links "lose" position info
- Idea. Add learned position-speciﬁc embedding
- to token vector
- “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-014.webp" n="14"} Need for position information

- Motivation. Direct links "lose" position info
- Idea. Add learned position-speciﬁc embedding
- to token vector
- Limitations. Need to retrain for longer sequences
:::

:::slide{src="../../slides/lecture-02/slide-017.webp" n="17"} Hardcoded position embeddings

- Idea. Hardcode values of position embedding
- . . . . . .
- 2i 2i
- 2i+1 2i+1
- . . . . . .
- Position Position
- “ Attention Is All You Need ”, Vaswani et al., 2017, " Transformer Architecture: The Positional Encoding ", by Kazemnejad, 2019.
:::

:::slide{src="../../slides/lecture-02/slide-023.webp" n="23"} Hardcoded position embeddings

- Idea. Hardcode values of position embedding
- Value of embeddings Similarity between positions
- Beneﬁts. Can extend to any sequence length
- “ Attention Is All You Need ”, Vaswani et al., 2017, " Transformer Architecture: The Positional Encoding ", by Kazemnejad, 2019.
:::

:::slide{src="../../slides/lecture-02/slide-024.webp" n="24"} From absolute to relative position info

- Motivation. Actually, we really care about relative position with attention layer
- " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
:::

:::slide{src="../../slides/lecture-02/slide-025.webp" n="25"} From absolute to relative position info

- Motivation. Actually, we really care about relative position with attention layer
- Idea. Let's change the attention layer instead
- “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-027.webp" n="27"} Linear bias in attention layer

- Idea. Add bias to query-key scores
- T5 bias. Bias is learned per head
- " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
- " Exploring the Limits of Transfer Learning with a Uniﬁed Text-to-Text Transformer ", Raﬀel et al., 2023.
:::

:::slide{src="../../slides/lecture-02/slide-028.webp" n="28"} Linear bias in attention layer

- Idea. Add bias to query-key scores
- T5 bias. Bias is learned per head
- ALiBi. Bias is linear, deterministic, not bounded
- " Super Study Guide: Transformers & Large Language Models ", by Amidi, 2024.
- " Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation ", Press et al., 2021.
:::

:::slide{src="../../slides/lecture-02/slide-031.webp" n="31"} Default choice nowadays: rotations in attention layer

- RoPE = Rotary Position Embeddings
- Idea. Rotate query and key vectors with rotation matrix
- Formula. Use rotation matrix:
- " RoFormer: Enhanced Transformer with Rotary Position Embeddings ", Su et al., 2021.
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-02/slide-034.webp" n="34"} Default choice nowadays: rotations in attention layer

- Extension to dimension d > 2. Rotate every block of dimension 2
- Beneﬁts. Relative distance nicely captured:
- " RoFormer: Enhanced Transformer with Rotary Position Embeddings ", Su et al., 2021.
:::

:::slide{src="../../slides/lecture-02/slide-035.webp" n="35"} Attention weight has a long-term decay

- Relative upper
- bound of
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::
