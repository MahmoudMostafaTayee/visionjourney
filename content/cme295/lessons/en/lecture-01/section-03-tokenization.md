---
lesson_id: section-03-tokenization
course_id: lecture-01
lang: en
order_index: 3
title: Tokenization
description: 'Slides 29–33 of lecture 1: 4 slides from the original deck.'
meta_title: Tokenization — Lecture 1
meta_description: Slide-by-slide walkthrough of Tokenization, lecture 1.
meta_keywords: Tokenization, lecture 1, slides
---

## Tokenization

:::slide{src="../../slides/lecture-01/slide-029.webp" n="29"} Tokenization

- A cute teddy bear is reading.
- arbitrary A cute teddy bear is reading .
:::

:::slide{src="../../slides/lecture-01/slide-031.webp" n="31"} Tokenization

- A cute teddy bear is reading.
- A cute teddy bear is reading .
- A cute teddy bear is reading .
- sub-word A cute ted ##dy bear is read ##ing .
:::

:::slide{src="../../slides/lecture-01/slide-032.webp" n="32"} Tokenization

- A cute teddy bear is reading.
- A cute teddy bear is reading .
- A cute teddy bear is reading .
- A cute ted ##dy bear is read ##ing .
- A _ c u t e _ t e d d y _ b e a r _ i s _ r e a d i n g .
:::

:::slide{src="../../slides/lecture-01/slide-033.webp" n="33"} Tokenization summary

- Method Pros Cons
- Simple ● Risk of OOV
- Word-level ● Interpretable ● Does not leverage
- knowledge of root
- Leverages common ● Risk of OOV, though less
- Subword-level
- preﬁxes and suﬃxes than word-level
- e.g. WordPiece, BPE
- Learned from the data
- Small chance of OOV ● Makes computations slower
- Character-level ● RoBUsT tO CASinG anD ● Embeddings not
- MIspeliNGs interpretable
:::
