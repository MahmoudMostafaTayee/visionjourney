---
lesson_id: section-06-why-bert
course_id: lecture-02
lang: en
order_index: 6
title: Why "BERT"?
description: 'Slides 62–82 of lecture 2: 14 slides from the original deck.'
meta_title: Why "BERT"? — Lecture 2
meta_description: Slide-by-slide walkthrough of Why "BERT"?, lecture 2.
meta_keywords: Why "BERT"?, lecture 2, slides
---

## Why "BERT"?

:::slide{src="../../slides/lecture-02/slide-062.webp" n="62"} Why "BERT"?

- BERT = Bidirectional Encoder Representations from Transformers
- " BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding ", Devlin et al., 2018.
:::

:::slide{src="../../slides/lecture-02/slide-067.webp" n="67"} Why "BERT"?

- BERT = Bidirectional Encoder Representations from Transformers
- Not bidirectional
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-068.webp" n="68"} Why "BERT"?

- ELMo paper BERT paper
- [submitted in Feb 2018] [submitted in Oct 2018]
- " BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding ", Devlin et al., 2018. [BERT paper]
- " Deep contextualized word representations ", Peters et al., 2018 [ELMo paper]
:::

:::slide{src="../../slides/lecture-02/slide-069.webp" n="69"} Why "BERT"?

- Elmo Bert
- For more background: Sesame Street , Wikipedia.
:::

:::slide{src="../../slides/lecture-02/slide-070.webp" n="70"} BERT and encoder-only models

- Idea. Keep only encoders + leverage encoded embeddings to make predictions.
- encoded
- Project embedding
- embedding
- ENCODER
- [CLS] A cute teddy bear is reading . [SEP]
- " BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding ", Devlin et al., 2018.
:::

:::slide{src="../../slides/lecture-02/slide-073.webp" n="73"} BERT and encoder-only models

- Strategy.
- Step 1: Pretraining with proxy tasks (MLM and NSP)
- Step 2: Finetuning for given end task
- Discussion.
- Pros Cons
- Finetuning does not need a lot of data ● Not suited for a range of tasks (e.g. text
- Good performance generation)
- Finetuning is a required step
- Variants. RoBERTa, DistilBERT, ALBERT
- " BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding ", Devlin et al., 2018.
:::

:::slide{src="../../slides/lecture-02/slide-075.webp" n="75"} BERT architecture

- Original transformer (2017)
- BERT (2018)
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-076.webp" n="76"} Input processing

- WordPiece algorithm
- Tokenizer trained on a training set beforehand
- Vocabulary size: ~ 30,000
- Great at detecting common particles
- NSP / MLM task processing
- Add [CLS] token at the beginning of the input
- Separate consecutive segments with the
- [SEP] token and put another one at the end
- Use [MASK] to mask inputs
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-077.webp" n="77"} Input embedding

- Input embeddings
- Gigantic lookup table
- Learns an embedding for each word of the
- vocabulary
- Positional encoding
- Helps the network associate tokens with a position
- Encoding either learnt or ﬁxed with cosines and sines
- (new!) Segment encoding
- Shared embedding for a segment
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-078.webp" n="78"} Encoder-only model

- Model
- Encoder part of the original transformers paper
- Goal
- Represent input data with features (hopefully)
- needed for NLP tasks
- Leverage the Transformer’s self-attention
- mechanism
- Use learned embedding towards
- classiﬁcation-oriented tasks
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-079.webp" n="79"} Proxy task: Masked Language Modeling

- Idea. 15% of input tokens are set up for prediction where:
- 80% are masked
- 10% are changed to a random word
- 10% are unchanged
- Beneﬁts
- Network learns language modeling based on
- contextual information
- Regularization reﬂects probabilistic nature of
- language
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-080.webp" n="80"} Proxy task: Next Sentence Prediction

- Idea. Pick two sentences from the corpus, where:
- 50% of the time, they follow each other
- 50% of the time, they do not follow each other
- Task. Predict if they actually follow each other.
- Beneﬁts
- Network implicitly learns to detect useful contextual
- information
- Easy classiﬁcation task that does not require any
- labels
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-081.webp" n="81"} Hyperparameters

- Model.
- L Layers.
- H Hidden layer size aka dimension of embeddings.
- A Attention heads operating in parallel.
- L Data.
- A ● Language-speciﬁc / multilingual. Languages on which
- the model has been trained on.
- H ● Cased / uncased. Whether inputs are converted to
- lowercase or not.
- Figure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-02/slide-082.webp" n="82"} Some numbers

- L H A Parameters
- BERT-Tiny 2 128 2 4M
- BERT-Mini 4 256 4 11M
- BERT-Small 4 512 8 30M
- A BERT-Medium 8 512 8 42M
- BERT-Base 12 768 12 110M
- BERT-Large 24 1024 16 340M
- Left ﬁgure adapted from “ Attention Is All You Need ”, Vaswani et al., 2017. Parameters in the right table were computed in this paper.
:::
