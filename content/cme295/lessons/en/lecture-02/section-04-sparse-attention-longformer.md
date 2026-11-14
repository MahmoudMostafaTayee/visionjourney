---
lesson_id: section-04-sparse-attention-longformer
course_id: lecture-02
lang: en
order_index: 4
title: 'Sparse attention: Longformer'
description: 'Slides 47–54 of lecture 2: 6 slides from the original deck.'
meta_title: 'Sparse attention: Longformer — Lecture 2'
meta_description: 'Slide-by-slide walkthrough of Sparse attention: Longformer, lecture
  2.'
meta_keywords: 'Sparse attention: Longformer, lecture 2, slides'
---

## Sparse attention: Longformer

:::slide{src="../../slides/lecture-02/slide-047.webp" n="47"} Sparse attention: Longformer

- cute . . . . .
- [CLS] A teddy bear
- [CLS]
- cute
- teddy bear
- . . . . .
- " Longformer: The Long-document Transformer ", Beltagy et al., 2020.
:::

:::slide{src="../../slides/lecture-02/slide-048.webp" n="48"} Leveraging local and global attention

- SWA = Sliding Window Attention
- cute . . .
- [CLS] A teddy bear
- [CLS] Variations include interleaving local and
- global attention layers
- cute
- teddy bear
- . . .
:::

:::slide{src="../../slides/lecture-02/slide-049.webp" n="49"} Leveraging local and global attention

- SWA = Sliding Window Attention
- cute . . .
- [CLS] A teddy bear
- [CLS]
- A Mistral 7B
- cute
- teddy bear
- . . .
- Right ﬁgure from Mistral 7B announcement , 2023.
:::

:::slide{src="../../slides/lecture-02/slide-050.webp" n="50"} Leveraging local and global attention

- SWA = Sliding Window Attention
- Similar to "receptive ﬁeld" in
- computer vision
- cute . . .
- [CLS] A teddy bear
- [CLS]
- A Mistral 7B
- cute
- teddy bear
- . . .
- " VIP Cheatsheet: Convolutional Neural Networks ", Amidi, 2018.
:::

:::slide{src="../../slides/lecture-02/slide-051.webp" n="51"} Sharing attention heads

- Idea. Share key/value attention heads within groups of queries
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-02/slide-054.webp" n="54"} Sharing attention heads

- Multi-Query Attention
- (MQA)
- Group-Query Attention
- (GQA)
- Multi-Head Attention
- (MHA)
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::
