---
lesson_id: section-08-stitching-all-the-pieces-together-with-an-exampl
course_id: lecture-01
lang: en
order_index: 8
title: Stitching all the pieces together with an example
description: 'Slides 96–135 of lecture 1: 14 slides from the original deck.'
meta_title: Stitching all the pieces together with an example — Lecture 1
meta_description: Slide-by-slide walkthrough of Stitching all the pieces together
  with an example, lecture 1.
meta_keywords: Stitching all the pieces together with an example, lecture 1, slides
---

## Stitching all the pieces together with an example

:::slide{src="../../slides/lecture-01/slide-096.webp" n="96"} Stitching all the pieces together with an example

- position-aware embedding
- [BOS] A cute teddy bear is reading . [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-104.webp" n="104"} Stitching all the pieces together with an example

- Q K V
- encoder
- Wq Wk Wv
- PAUSE position-aware
- embeddings
- matrix
- [BOS] A cute teddy bear is reading . [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-105.webp" n="105"} Stitching all the pieces together with an example

- [BOS]
- cute
- teddy bear
- is
- reading
- [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-107.webp" n="107"} Stitching all the pieces together with an example

- teddy bear
- [BOS] reading
- [BOS] [EOS]
- cute
- A is
- A .
- cute
- teddy bear
- is
- reading
- [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-109.webp" n="109"} Stitching all the pieces together with an example

- [BOS]
- . . .
- cute
- teddy bear
- . . .
- is
- . . .
- reading
- [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-111.webp" n="111"} Stitching all the pieces together with an example

- weighted average of values
- with weights being a function of
:::

:::slide{src="../../slides/lecture-01/slide-114.webp" n="114"} Stitching all the pieces together with an example

- ... Wo
- Q K V
- h x encoder
- Wq Wk Wv
- position-aware
- embeddings
- matrix
- [BOS] A cute teddy bear is reading . [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-116.webp" n="116"} Stitching all the pieces together with an example

- context-aware
- encoded
- embeddings
- Feed forward network
- encoder
- Self-attention layer
- position-aware
- embeddings matrix
- [BOS] A cute teddy bear is reading . [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-117.webp" n="117"} Stitching all the pieces together with an example

- context-aware
- encoded
- embeddings
- ENCODER
- position-aware
- embeddings matrix
- [BOS] A cute teddy bear is reading . [EOS]
:::

:::slide{src="../../slides/lecture-01/slide-128.webp" n="128"} Stitching all the pieces together with an example

- [0.001, 0.0003, …, 0.4, …, 0.002]
- encoded
- embedding
- Softmax layer
- Feed forward network
- ENCODER decoder
- Encoder - Decoder
- attention layer
- Self-attention layer
- A cute teddy bear
- is reading.
- [BOS]
:::

:::slide{src="../../slides/lecture-01/slide-129.webp" n="129"} Stitching all the pieces together with an example

- Un
- encoded
- embedding
- Softmax layer
- Feed forward network
- ENCODER decoder
- Encoder - Decoder
- attention layer
- Self-attention layer
- A cute teddy bear
- is reading.
- [BOS]
:::

:::slide{src="../../slides/lecture-01/slide-133.webp" n="133"} Stitching all the pieces together with an example

- Un ours en peluche mignon lit [EOS]
- encoded
- embedding
- ENCODER DECODER
- A cute teddy bear
- is reading.
- [BOS] Un ours en peluche mignon lit
:::

:::slide{src="../../slides/lecture-01/slide-134.webp" n="134"} Stitching all the pieces together with an example

- encoded Un ours en peluche mignon lit.
- embedding
- ENCODER DECODER
- A cute teddy bear is reading.
:::

:::slide{src="../../slides/lecture-01/slide-135.webp" n="135"} Thank you for your attention!

:::
