---
lesson_id: section-06-cross-pollination-between-modalities
course_id: lecture-09
lang: en
order_index: 6
title: Cross-pollination between modalities
description: 'Slides 101–117 of lecture 9: 14 slides from the original deck.'
meta_title: Cross-pollination between modalities — Lecture 9
meta_description: Slide-by-slide walkthrough of Cross-pollination between modalities,
  lecture 9.
meta_keywords: Cross-pollination between modalities, lecture 9, slides
---

## Cross-pollination between modalities

:::slide{src="../../slides/lecture-09/slide-101.webp" n="101"} Cross-pollination between modalities

- Trend. Modalities trade ideas on concepts that work
- Architecture.
- "Diﬀusion" training for text output
- " Large Language Diﬀusion Models ", Nie et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-102.webp" n="102"} Cross-pollination between modalities

- Trend. Modalities trade ideas on concepts that work
- Architecture.
- "Diﬀusion" training for text output
- Transformers to deal with images
- " Scalable Diﬀusion Models with Transformers ", Peebles et al., 2022.
:::

:::slide{src="../../slides/lecture-09/slide-103.webp" n="103"} Cross-pollination between modalities

- Trend. Modalities trade ideas on concepts that work
- Architecture.
- "Diﬀusion" training for text output
- Transformers to deal with images
- Input representation. DeepSeek-OCR
- " DeepSeek-OCR: Contexts Optical Compression ", Wei et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-104.webp" n="104"} Cross-pollination between modalities

- Trend. Modalities trade ideas on concepts that work
- Architecture.
- "Diﬀusion" training for text output
- Transformers to deal with images
- Input representation. DeepSeek-OCR
- Tricks. RoPE variants (e.g. image: Multimodal Scalable RoPE)
- " Qwen-Image Technical Report ", Wu et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-106.webp" n="106"} Back to the basics

- Foundational research still very much ongoing.
- Microscopic level. Design choices still widely very across papers.
- Optimizers: AdamW vs. MuonClip vs. others ● Activation functions
- Normalization? ● MoE vs. not
- MHA/MQA/GQA design choices ● Number of layers
- " Kimi K2: Open Agentic Intelligence ", Kimi Team, 2025.
:::

:::slide{src="../../slides/lecture-09/slide-107.webp" n="107"} Back to the basics

- Foundational research still very much ongoing.
- Microscopic level. Design choices still widely very across papers.
- Optimizers: AdamW vs. MuonClip vs. others ● Activation functions
- Normalization? ● MoE vs. not
- MHA/MQA/GQA design choices ● Number of layers
- "Fuel". Future streams of high-quality data?
- " The Curse of Recursion: Training on Generated Data Makes Models Forget ", Shumailov et al., 2023.
:::

:::slide{src="../../slides/lecture-09/slide-108.webp" n="108"} Back to the basics

- Foundational research still very much ongoing.
- Microscopic level. Design choices still widely very across papers.
- Optimizers: AdamW vs. MuonClip vs. others ● Activation functions
- Normalization? ● MoE vs. not
- MHA/MQA/GQA design choices ● Number of layers
- "Fuel". Future streams of high-quality data?
- Taking a step back. Transformer = best architecture?
:::

:::slide{src="../../slides/lecture-09/slide-109.webp" n="109"} Interest in pushing through new frontiers

- Until now. Focus on best performance.
- " LLM Arena Pareto Frontier: Performance vs Cost (April 2025) ", screenshot taken on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-09/slide-110.webp" n="110"} Interest in pushing through new frontiers

- More and more? Focus on the best quality/cost trade-oﬀ.
- " LLM Arena Pareto Frontier: Performance vs Cost (April 2025) ", screenshot taken on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-09/slide-113.webp" n="113"} Hardware optimization

- Observation. Current GPUs optimize for matrix-vector/matrix-matrix operations.
- Challenges. Transformer blocks have special needs:
- Attention requires frequent KV reads/writes
- Memory movement dominates cost on GPUs
- Idea. "Natively" support attention operations in hardware:
- Store KV cache in dedicated cells
- Use analog signals to model computations
- " Analog in-memory computing attention mechanism for fast and energy-eﬃcient large language models ", Leroux et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-114.webp" n="114"} Hardware optimization

- Figures adapted from " Analog in-memory computing attention mechanism for fast and energy-eﬃcient large language models ", Leroux et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-115.webp" n="115"} Hardware optimization

- Observation. Current GPUs optimize for matrix-vector/matrix-matrix operations.
- Challenges. Transformer blocks have special needs:
- Attention requires frequent KV reads/writes
- Memory movement dominates cost on GPUs
- Idea. "Natively" support attention operations in hardware:
- Store KV cache in dedicated cells
- Use analog signals to model computations
- Results. Up to ~ 100x latency/ ~ 70,000x energy savings with respect to Nvidia's H100.
- " Analog in-memory computing attention mechanism for fast and energy-eﬃcient large language models ", Leroux et al., 2025.
:::

:::slide{src="../../slides/lecture-09/slide-116.webp" n="116"} Daily life has already dramatically changed by LLMs

- Today. Many uses already.
- Some key applications:
- Coding ("true" coding, text-to-query)
- General conversational assistant (common facts, web search)
- Creativity
- Learning
- ...
:::

:::slide{src="../../slides/lecture-09/slide-117.webp" n="117"} More use cases to be expected

- Tomorrow .
- Democratization of existing agents (e.g. Google Workspace launch)
- " Introducing Google Workspace Studio: Automate everyday work with AI agents ", Google Workspace, December 3, 2025.
:::
