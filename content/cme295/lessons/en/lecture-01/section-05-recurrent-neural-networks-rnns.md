---
lesson_id: section-05-recurrent-neural-networks-rnns
course_id: lecture-01
lang: en
order_index: 5
title: Recurrent Neural Networks (RNNs)
description: 'Slides 51–68 of lecture 1: 6 slides from the original deck.'
meta_title: Recurrent Neural Networks (RNNs) — Lecture 1
meta_description: Slide-by-slide walkthrough of Recurrent Neural Networks (RNNs),
  lecture 1.
meta_keywords: Recurrent Neural Networks (RNNs), lecture 1, slides
---

## Recurrent Neural Networks (RNNs)

:::slide{src="../../slides/lecture-01/slide-051.webp" n="51"} Recurrent Neural Networks (RNNs)

- Overview
- First introduced in the 80s
- Class of neural networks where connections form a temporal sequence
- General form
- Figure adapted from “VIP cheatsheets for Stanford’s CS 230”, Amidi. stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks
:::

:::slide{src="../../slides/lecture-01/slide-061.webp" n="61"} Recurrent Neural Networks (RNNs)

- cute teddy bear is reading
- A cute teddy bear is
:::

:::slide{src="../../slides/lecture-01/slide-062.webp" n="62"} Recurrent Neural Networks (RNNs)

- Classiﬁcation “Multi”-classiﬁcation Generation
- Input text Model 3 Input text Model Input text Input text Model Out text
- 5 1
- Sentiment Tags Translation
- Opinion Text Source
- Figure adapted from “VIP cheatsheets for Stanford’s CS 230”, Amidi. stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks
:::

:::slide{src="../../slides/lecture-01/slide-063.webp" n="63"} Long Short-Term Memory (LSTM)

- Overview
- Introduced in “ Long short-term memory ” (1997)
- Uses a more structured approach in the cell’s hidden state
- General form
- Figure adapted from “VIP cheatsheets for Stanford’s CS 230”, Amidi. stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks
:::

:::slide{src="../../slides/lecture-01/slide-064.webp" n="64"} Summary of main methods (non-exhaustive list)

- Method Pros Cons
- Very simple, yet ● Word order does not
- Word2vec
- powerful count
- Intuitive embeddings ● Embeddings not
- e.g. CBOW, Skip-gram
- context aware
- Word order matters ● Vanishing gradient
- Recurrent Neural Networks
- State-of-the-art results problem
- e.g. traditional RNN, LSTM ● Slow computations
:::

:::slide{src="../../slides/lecture-01/slide-068.webp" n="68"} History of attention

- Introduced in 2014
- Translation tasks had a real issue with long-term dependencies
- Seq2seq unable to "remember" what input sentence was saying
- Un ours en peluche mignon lit
- A cute teddy bear is reading
- " Neural Machine Translation by Jointly Learning to Align and Translate ”, Bahdanau et al., 2014.
:::
