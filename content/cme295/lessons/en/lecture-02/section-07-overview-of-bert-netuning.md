---
lesson_id: section-07-overview-of-bert-netuning
course_id: lecture-02
lang: en
order_index: 7
title: Overview of BERT ﬁnetuning
description: 'Slides 85–109 of lecture 2: 13 slides from the original deck.'
meta_title: Overview of BERT ﬁnetuning — Lecture 2
meta_description: Slide-by-slide walkthrough of Overview of BERT ﬁnetuning, lecture
  2.
meta_keywords: Overview of BERT ﬁnetuning, lecture 2, slides
---

## Overview of BERT ﬁnetuning

:::slide{src="../../slides/lecture-02/slide-085.webp" n="85"} Overview of BERT ﬁnetuning

- Goal. Leverage embeddings learned by BERT for a “sister” task
- Tricks
- Use weights from already massively pretrained model
- Freezing early layers: sometimes better trade-oﬀ complexity/performance
- Great results possible with minimal labeled data (depending on
- complexity/proximity to pretrained data distribution + objectives)
- Use cases
- Sequence classiﬁcation: e.g. sentiment extraction
- Token classiﬁcation: e.g. question answering
:::

:::slide{src="../../slides/lecture-02/slide-089.webp" n="89"} Finetuning: sentiment extraction

- Add [CLS] token as a placeholder for sentiment.
- [CLS] this teddy bear is so cute !
:::

:::slide{src="../../slides/lecture-02/slide-092.webp" n="92"} Finetuning: sentiment extraction

- position embedding
- embedding
- [CLS] this teddy bear is so cute ! [SEP] [PAD] [PAD] [PAD] [PAD] [PAD] [PAD]
- 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
:::

:::slide{src="../../slides/lecture-02/slide-093.webp" n="93"} Finetuning: sentiment extraction

- segment embedding
- position embedding
- embedding
- [CLS] this teddy bear is so cute ! [SEP] [PAD] [PAD] [PAD] [PAD] [PAD] [PAD]
- A A A A A A A A A B B B B B B
:::

:::slide{src="../../slides/lecture-02/slide-094.webp" n="94"} Finetuning: sentiment extraction

- position- and segment-aware embedding
- [CLS] this teddy bear is so cute ! [SEP] [PAD] [PAD] [PAD] [PAD] [PAD] [PAD]
:::

:::slide{src="../../slides/lecture-02/slide-097.webp" n="97"} Finetuning: sentiment extraction

- 1 Sentiment extraction task
- SE
- FFN
- Pretrained BERT architecture
- ENCODER
- [CLS] this teddy bear is so cute ! [SEP] [PAD] [PAD] [PAD] [PAD] [PAD] [PAD]
:::

:::slide{src="../../slides/lecture-02/slide-100.webp" n="100"} Takeaways and shortcomings

- Beneﬁts.
- State of the art results
- ~ True contextual representation of words
- Adaptable to many classiﬁcation tasks
- Applications. Widely used in the industry for anything related to encoding
- Limitations.
- Context window size is limited
- Computationally expensive: hard sell for low-latency/cost-sensitive applications
- Training paradigm is complex: MLM/NSP + ﬁnetuning
:::

:::slide{src="../../slides/lecture-02/slide-101.webp" n="101"} Trick: distillation

- "The soft targets contain
- almost all the knowledge."
- “ Dark knowledge ”, Hinton et al., 2014.
:::

:::slide{src="../../slides/lecture-02/slide-103.webp" n="103"} Trick: distillation

- Figures from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-02/slide-104.webp" n="104"} Variant for eﬃciency: DistilBERT

- ~1.6x faster
- BERT Base DistilBERT
- N=12 layers N=6 layers
- ~ 97% performance
- " DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter ", Sanh et al., 2019.
:::

:::slide{src="../../slides/lecture-02/slide-106.webp" n="106"} Variant for performance: RoBERTa

- Goal. Thorough analysis of directions of optimization
- Modeling
- Removing NSP/segment encodings: ~ no eﬀect!*
- Static → dynamic masking across epochs
- *DistilBERT had also removed it
- " RoBERTa: A Robustly Optimized BERT Pretraining Approach ", Liu et al., 2019.
:::

:::slide{src="../../slides/lecture-02/slide-108.webp" n="108"} Variant for performance: RoBERTa

- Goal. Thorough analysis of directions of optimization
- Modeling
- Removing NSP/segment encodings: ~ no eﬀect!
- Static → dynamic masking across epochs
- Data
- Richer: 16 GB → 160 GB of pretraining corpus size
- For longer: 1M steps of batch size 256 vs. 500k of batch size 8k
- Result. +4% across benchmarks with same architecture
- " RoBERTa: A Robustly Optimized BERT Pretraining Approach ", Liu et al., 2019.
:::

:::slide{src="../../slides/lecture-02/slide-109.webp" n="109"} Thank you for your attention!

:::
