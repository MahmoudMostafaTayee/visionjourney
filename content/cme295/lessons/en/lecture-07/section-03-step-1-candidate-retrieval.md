---
lesson_id: section-03-step-1-candidate-retrieval
course_id: lecture-07
lang: en
order_index: 3
title: 'Step 1: candidate retrieval'
description: 'Slides 47–80 of lecture 7: 14 slides from the original deck.'
meta_title: 'Step 1: candidate retrieval — Lecture 7'
meta_description: 'Slide-by-slide walkthrough of Step 1: candidate retrieval, lecture
  7.'
meta_keywords: 'Step 1: candidate retrieval, lecture 7, slides'
---

## Step 1: candidate retrieval

:::slide{src="../../slides/lecture-07/slide-047.webp" n="47"} Step 1: candidate retrieval

- Objective. Select potentially-relevant candidates via search across knowledge base
- Method 3. Search based on hybrid combination of semantics and BM25
- […] Huggy likes to work downstairs […]
- [...] Where is Paris located? [...]
- Where is Cuddly?
- [...] he was in a cuddly mood [...]
- [ …] Cuddly spends most days surrounded by
- books [...]
:::

:::slide{src="../../slides/lecture-07/slide-051.webp" n="51"} Extensions that can help with initial retrieval

- Mitigate discrepancy in nature of embeddings
- Prompt Where is Cuddly? Chunks
- Cuddly is in…
- Fake
- document
- " Precise Zero-Shot Dense Retrieval without Relevance Labels ", Gao et al., 2022.
:::

:::slide{src="../../slides/lecture-07/slide-053.webp" n="53"} Extensions that can help with initial retrieval

- Mitigate discrepancy in nature of embeddings
- Contextualize document chunks
- Context 1
- Chunk 1
- Chunk 1
- … …
- Context n
- Chunk n
- Chunk n
- Introducing Contextual Retrieval , Anthropic team, 2024.
:::

:::slide{src="../../slides/lecture-07/slide-055.webp" n="55"} Extensions that can help with initial retrieval

- Mitigate discrepancy in nature of embeddings
- Prompt caching
- Contextualize document chunks
- <document>
- {WHOLE_DOCUMENT}
- </document>
- Here is the chunk we want to situate within the whole document:
- {CHUNK_CONTENT}
- Please give a short succinct context to situate this chunk within the overall
- document for the purposes of improving search retrieval of the chunk. Answer
- only with the succinct context and nothing else.
- Introducing Contextual Retrieval , Anthropic team, 2024.
:::

:::slide{src="../../slides/lecture-07/slide-057.webp" n="57"} Extensions that can help with initial retrieval

- Mitigate discrepancy in nature of embeddings
- Contextualize document chunks
- OpenAI model pricing page , screenshot taken on November 10th, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-060.webp" n="60"} Step 2: ranking

- Objective. Provide ﬁnal relevance score using more sophisticated (re-)ranker
- "cross-encoder"
- Query
- relevance
- Encoder
- score
- Chunk
- Suggested reading: " Cross-Encoders ", SBERT.net
:::

:::slide{src="../../slides/lecture-07/slide-062.webp" n="62"} Step 2: ranking

- Objective. Provide ﬁnal relevance score using more sophisticated (re-)ranker
- User prompt
- Chunk d Chunk a 1
- Chunk b Chunk b 2
- Re-Ranker
- Chunk a Chunk c 3
- Chunk c Chunk d 4
:::

:::slide{src="../../slides/lecture-07/slide-066.webp" n="66"} Quantify performance of retrieval

- Setup. Evaluate if retrieved chunks are relevant
- Top k
- User prompt
- Relevant
- Chunks
:::

:::slide{src="../../slides/lecture-07/slide-071.webp" n="71"} Quantify performance of retrieval

- Setup. Evaluate if retrieved chunks are relevant
- Ranking Normalized Discounted Cumulative Gain at k (NDCG@k)
- … …
- with
- k+1
- … …
- if ranking was perfect
:::

:::slide{src="../../slides/lecture-07/slide-072.webp" n="72"} Quantify performance of retrieval

- Setup. Evaluate if retrieved chunks are relevant
- Ranking Normalized Discounted Cumulative Gain at k (NDCG@k)
- Reciprocal Rank at k (RR@k)
- … …
- k+1
- … …
- rank of the ﬁrst relevant chunk
:::

:::slide{src="../../slides/lecture-07/slide-076.webp" n="76"} Quantify performance of retrieval

- Setup. Evaluate if retrieved chunks are relevant
- Ranking Normalized Discounted Cumulative Gain at k (NDCG@k)
- Reciprocal Rank at k (RR@k)
- … …
- Recall at k
- Precision at k
- k+1
- … …
:::

:::slide{src="../../slides/lecture-07/slide-077.webp" n="77"} RAG

- Transformers &
- Tool calling
- Large Language
- Agents
- Models
:::

:::slide{src="../../slides/lecture-07/slide-079.webp" n="79"} Motivation

- ID Field …
- 123 Obs …
- … … …
- Unstructured Structured
- RAG
:::

:::slide{src="../../slides/lecture-07/slide-080.webp" n="80"} Idea

- Function
- def get_data(
- id, field, ...
- ID Field … ):
- 123 Obs … # Logic.
- … … …
- return result
:::
