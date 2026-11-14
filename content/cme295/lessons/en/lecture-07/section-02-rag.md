---
lesson_id: section-02-rag
course_id: lecture-07
lang: en
order_index: 2
title: RAG
description: 'Slides 10–45 of lecture 7: 14 slides from the original deck.'
meta_title: RAG — Lecture 7
meta_description: Slide-by-slide walkthrough of RAG, lecture 7.
meta_keywords: RAG, lecture 7, slides
---

## RAG

:::slide{src="../../slides/lecture-07/slide-010.webp" n="10"} RAG

- Transformers &
- Tool calling
- Large Language
- Agents
- Models
:::

:::slide{src="../../slides/lecture-07/slide-013.webp" n="13"} Motivation

- Knowledge of LLM constrained to pretraining data
- Screenshot of OpenAI's GPT-5 model card , taken on November 9th, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-015.webp" n="15"} Motivation

- Knowledge of LLM constrained to pretraining data
- Limited context size
- Screenshot of OpenAI's GPT-5 model card , taken on November 9th, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-017.webp" n="17"} Motivation

- Knowledge of LLM constrained to pretraining data
- Limited context size
- LLM gets distracted by useless information
- GitHub repo containing " Needle in a Haystack - Pressure Testing LLMs " tests, Kamradt, 2023.
:::

:::slide{src="../../slides/lecture-07/slide-019.webp" n="19"} Motivation

- Knowledge of LLM constrained to pretraining data
- Limited context size
- LLM gets distracted by useless information
- Pricing is per input/output token
:::

:::slide{src="../../slides/lecture-07/slide-021.webp" n="21"} Overview

- RAG = Retrieval-Augmented Generation
- Idea. Augment prompt with relevant pieces of information.
- " Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks ", Lewis et al., 2020.
:::

:::slide{src="../../slides/lecture-07/slide-024.webp" n="24"} Overview

- RAG = Retrieval-Augmented Generation
- Idea. Augment prompt with relevant pieces of information.
- Figure from " Super Study Guide: Transformers & Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-07/slide-028.webp" n="28"} Retrieve, Generate, Augment

- 1. Retrieve relevant document via similarity operation across the knowledge base
- User prompt
- 2. Augment prompt with retrieved information
- Retrieved info
- User prompt
- User prompt
- 3. Generate response
- Retrieved info
- LLM Response
- User prompt
:::

:::slide{src="../../slides/lecture-07/slide-029.webp" n="29"} Focus on retrieval stage

- 1. Retrieve relevant document via similarity operation across the knowledge base
- User prompt
- 2. Augment prompt with retrieved information
- Retrieved info
- User prompt
- User prompt
- 3. Generate response
- Retrieved info
- LLM Response
- User prompt
:::

:::slide{src="../../slides/lecture-07/slide-033.webp" n="33"} Prerequisite: Create knowledge base

- Document 1 Document 2 …
- Document 1
- Document 2 0.48
- … 0.33
- -0.51
- Collect Divide Embed
- Hyperparameters. Embedding size, chunk size, overlap between chunks
:::

:::slide{src="../../slides/lecture-07/slide-035.webp" n="35"} Retrieval overview

- 🎣 Step 1 – Candidate retrieval: Select potentially-relevant candidates
- Maximize recall
- Semantic embeddings and optionally keyword-based methods
- 💯 Step 2 – Ranking: Give ﬁnal relevance score
- Maximize precision
- Re-ranking on smaller set of candidates
:::

:::slide{src="../../slides/lecture-07/slide-042.webp" n="42"} Step 1: candidate retrieval

- Objective. Select potentially-relevant candidates via search across knowledge base
- Method 1. Semantic search using embeddings-based similarity
- "bi-encoder"
- 0.48
- Query Encoder …
- -0.51 similarity similarity
- operation score
- -0.82
- Chunk Encoder …
- -0.43
- " Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks ", Reimers et al., 2019.
:::

:::slide{src="../../slides/lecture-07/slide-043.webp" n="43"} Step 1: candidate retrieval

- Objective. Select potentially-relevant candidates via search across knowledge base
- Method 1. Semantic search using embeddings-based similarity
- […] Huggy likes to work downstairs […]
- [...] Where is Paris located? [...]
- Where is Cuddly?
- [...] he was in a cuddly mood [...]
- [ …] Cuddly spends most days surrounded by
- books [...]
:::

:::slide{src="../../slides/lecture-07/slide-045.webp" n="45"} Step 1: candidate retrieval

- Objective. Select potentially-relevant candidates via search across knowledge base
- Method 2. Search based on keywords matching via BM25
- […] Huggy likes to work downstairs […]
- [...] Where is Paris located? [...]
- Where is Cuddly?
- [...] he was in a cuddly mood [...]
- [ …] Cuddly spends most days surrounded by
- books [...]
:::
