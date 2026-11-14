---
lesson_id: section-03-bottleneck-memory
course_id: lecture-04
lang: en
order_index: 3
title: 'Bottleneck: memory'
description: 'Slides 37–54 of lecture 4: 12 slides from the original deck.'
meta_title: 'Bottleneck: memory — Lecture 4'
meta_description: 'Slide-by-slide walkthrough of Bottleneck: memory, lecture 4.'
meta_keywords: 'Bottleneck: memory, lecture 4, slides'
---

## Bottleneck: memory

:::slide{src="../../slides/lecture-04/slide-037.webp" n="37"} Bottleneck: memory

- Limited memory, O(10s of GB)
- " NVIDIA H100 Tensor Core GPU ", NVIDIA website.
:::

:::slide{src="../../slides/lecture-04/slide-039.webp" n="39"} Data parallelism

- Idea.
- Divide batch of data across devices
- Model replicated on each device
- parameters
- … gradients
- optimizer state
- GPU 1 GPU n
:::

:::slide{src="../../slides/lecture-04/slide-042.webp" n="42"} Data parallelism with ZeRO

- Idea. Redundant information across devices
- ZeRO = Zero Redundancy Optimization
- Variations. ZeRO-2: Share optimizer state + gradients
- GPU 1 GPU n
- " ZeRO: Memory Optimizations Toward Training Trillion Parameter Models ", Rajbhandari et al., 2019.
:::

:::slide{src="../../slides/lecture-04/slide-043.webp" n="43"} Data parallelism with ZeRO

- Idea. Redundant information across devices
- ZeRO = Zero Redundancy Optimization
- Variations. ZeRO-3: Share optimizer state + gradients + parameters
- GPU 1 GPU n
- " ZeRO: Memory Optimizations Toward Training Trillion Parameter Models ", Rajbhandari et al., 2019.
:::

:::slide{src="../../slides/lecture-04/slide-044.webp" n="44"} Model parallelism

- Idea. Split the model computations across several devices
- Variations.
- Tensor Parallelism (TP).
- Pipeline Parallelism (PP).
- Sequence Parallelism (SP).
- Context Parallelism (CP).
- Expert Parallelism (EP).
- Suggested reading: " The Ultra-Scale Playbook: Training LLMs on GPU Clusters ", HuggingFace team, 2025.
:::

:::slide{src="../../slides/lecture-04/slide-047.webp" n="47"} Optimization via Flash Attention

- Strategy. Leverage components of GPU to speed up attention computations.
- Small and fast
- Big and slow SRAM
- CU
- HBM
- GPU
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-049.webp" n="49"} Standard self-attention computation

- Context. "Standard" self-attention computation
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-050.webp" n="50"} Standard self-attention computation

- LOAD Q, K from HBM by blocks
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-051.webp" n="51"} Standard self-attention computation

- Compute S
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-052.webp" n="52"} Standard self-attention computation

- WRITE S to HBM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-053.webp" n="53"} Standard self-attention computation

- READ S from HBM
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-054.webp" n="54"} Standard self-attention computation

- Compute P
- " FlashAttention: Fast and Memory-Eﬃcient Exact Attention with IO-Awareness ", Dao et al., 2022.
:::
