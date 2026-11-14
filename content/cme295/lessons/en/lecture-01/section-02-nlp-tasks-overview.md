---
lesson_id: section-02-nlp-tasks-overview
course_id: lecture-01
lang: en
order_index: 2
title: NLP tasks overview
description: 'Slides 19–26 of lecture 1: 5 slides from the original deck.'
meta_title: NLP tasks overview — Lecture 1
meta_description: Slide-by-slide walkthrough of NLP tasks overview, lecture 1.
meta_keywords: NLP tasks overview, lecture 1, slides
---

## NLP tasks overview

:::slide{src="../../slides/lecture-01/slide-019.webp" n="19"} NLP tasks overview

- Classiﬁcation “Multi”-classiﬁcation Generation
- Input text Model 3 Input text Model Input text Input text Model Out text
- 5 1
- Sentiment extraction ● Part of speech tagging ● Machine translation
- Intent detection ● Named entity recognition ● Question answering
- Language detection ● Dependency parsing ● Summarization
- Topic modeling ● Constituency parsing ● Text generation
:::

:::slide{src="../../slides/lecture-01/slide-021.webp" n="21"} NLP task: Sentiment Extraction

- This teddy bear is SO CUTE! Model +
- Datasets
- Amazon reviews IMDB critiques Twitter
- Evaluation metrics
- Accuracy → % of observations that were correctly predicted?
- Precision → % of predicted positive that were correct?
- Recall → % of actually positive that were correct?
- F1 score → score that is a function of precision and recall
:::

:::slide{src="../../slides/lecture-01/slide-023.webp" n="23"} NLP task: Named Entity Recognition

- ENTITY
- A cute teddy bear is reading... Model A cute teddy bear is reading...
- Datasets
- Annotated Reuters newspaper (CoNLL-2003, CoNLL++)
- Evaluation metrics
- Accuracy
- Precision at a token level, per entity type
- Recall
- F1 score
:::

:::slide{src="../../slides/lecture-01/slide-025.webp" n="25"} NLP task: Machine Translation

- A cute teddy bear is reading Model Un ours en peluche mignon lit
- Datasets
- WMT’14 English-French WMT’14 English-German
- Evaluation metrics
- BLEU → quality of text translated, similar to “precision”
- ROUGE → quality of text generated, similar to “recall”
- Perplexity → quantiﬁes how ‘surprised’ the model is to see some words
- together
- Formulas can be found on this website: http://www.statmt.org/book/slides/08-evaluation.pdf
:::

:::slide{src="../../slides/lecture-01/slide-026.webp" n="26"} High-level timeline

- 1980s Recurrent neural networks (RNNs)
- Theoretical foundations
- 1997 Long short-term memory (LSTM)
- 2013 Word2vec
- Lots of data, growing
- 2017 Transformers
- computing power
- 2020s Large Language Models
- Fast iterations on ideas
:::
