---
lesson_id: section-04-token-representations
course_id: lecture-01
lang: en
order_index: 4
title: Token representations
description: 'Slides 36–49 of lecture 1: 7 slides from the original deck.'
meta_title: Token representations — Lecture 1
meta_description: Slide-by-slide walkthrough of Token representations, lecture 1.
meta_keywords: Token representations, lecture 1, slides
---

## Token representations

:::slide{src="../../slides/lecture-01/slide-036.webp" n="36"} Token representations

- Motivation
- Naive (one-hot) encoding Learned embedding
- Figure adapted from “VIP cheatsheets for Stanford’s CS 230”, Amidi. stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks
:::

:::slide{src="../../slides/lecture-01/slide-037.webp" n="37"} Word2vec

- Overview
- Neural network with a proxy task over billions of words worth of text
- Learns an embedding layer
- Proxy tasks
- CBOW (continuous bag of words)
- ...A cute teddy bear is reading...
- Skip-gram
- ...A cute teddy bear is reading...
- Word2vec paper " Eﬃcient Estimation of Word Representations in Vector Space ", Mikolov et al., 2013.
:::

:::slide{src="../../slides/lecture-01/slide-038.webp" n="38"} Word2vec

- Architecture
- output size V
- hidden size d
- input size
:::

:::slide{src="../../slides/lecture-01/slide-042.webp" n="42"} Word2vec

- Example with predicting next word
- A cute teddy bear is reading
- [0.2, 0.4 , 0.1, 0.1, 0.1, 0.1]
- [0.2, 0.9]
- [1,0,0,0,0,0]
- A cute teddy bear is reading
:::

:::slide{src="../../slides/lecture-01/slide-046.webp" n="46"} Word2vec

- Example with predicting next word
- A cute teddy bear is reading
- [0.2, 0.2 , 0.2, 0.1, 0.2 , 0.1]
- [0.8, 0.4]
- [0,1,0,0,0,0]
- A cute teddy bear is reading
:::

:::slide{src="../../slides/lecture-01/slide-048.webp" n="48"} Word2vec

- Example with predicting next word
- A cute teddy bear is reading
- A cute teddy bear is reading
:::

:::slide{src="../../slides/lecture-01/slide-049.webp" n="49"} Word2vec

- A cute teddy bear is reading
- output size V
- hidden size d
- input size
- A cute teddy bear is reading
- Figure adapted from “VIP cheatsheets for Stanford’s CS 230”, Amidi. stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks
:::
