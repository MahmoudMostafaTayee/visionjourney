---
lesson_id: section-05-terminology
course_id: lecture-03
lang: en
order_index: 5
title: Terminology
description: 'Slides 79–85 of lecture 3: 6 slides from the original deck.'
meta_title: Terminology — Lecture 3
meta_description: Slide-by-slide walkthrough of Terminology, lecture 3.
meta_keywords: Terminology, lecture 3, slides
---

## Terminology

:::slide{src="../../slides/lecture-03/slide-079.webp" n="79"} Terminology

- Is a teddy bear cute? LLM Yes.
- Context length
- Context size
- Window size
- Discussion. Orders of magnitude by:
- Input type
- Beware of "context rot"!
- Models
- " Context Rot: How Increasing Input Tokens Impacts LLM Performance ", Hong et al., 2025.
:::

:::slide{src="../../slides/lecture-03/slide-080.webp" n="80"} Main structure

- My teddy bear had a long day and
- Context
- needs a bedtime story.
- Generate a bedtime story that takes
- place in a specific location. Instructions
- Location: Country of teddy bears Input
- The story needs to be suitable for
- Constraints
- teddy bears that are tired.
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-082.webp" n="82"} In-context learning

- ICL = In-Context Learning
- Zero-shot learning Few-shot learning
- Question is asked without examples ● Prompt contains examples of input /
- Performance heavily depends on output
- performance of initial model ● Typically has a better performance
- " Language Models are Few-Shot Learners ", Brown et al., 2020.
:::

:::slide{src="../../slides/lecture-03/slide-083.webp" n="83"} In-context learning

- ICL = In-Context Learning
- Zero-shot learning Few-shot learning
- Question is asked without examples ● Prompt contains examples of input /
- Performance heavily depends on output
- performance of initial model ● Typically has a better performance
- Discussion. Showing examples in the prompt is generally better but:
- Requires eﬀort
- Increases computational complexity & cost
- Increases latency
:::

:::slide{src="../../slides/lecture-03/slide-084.webp" n="84"} Chain of thought

- Idea. Explaining reasoning helps in improving performance.
- Q: How old is this bear? A: It will be one
- A: The bear was born in year older than
- 2020. It is therefore 4. its age this year,
- LLM which was 4.
- Hence, it will be
- Q: How old will the bear
- 5.
- be next year?
- Discussion.
- Interpretability + explanation
- More tokens: higher cost and latency
- " Chain-of-Thought Prompting Elicits Reasoning in Large Language Models ", Wei et al., 2022.
:::

:::slide{src="../../slides/lecture-03/slide-085.webp" n="85"} Self-consistency

- Idea. Aggregating over reasoning paths improves performance.
- A: It will be one year
- older than its age this
- year, which was 4.
- Hence, it will be 5.
- A: The bear was born in
- LLM 2020. It will therefore 5
- be 5.
- A: Next year is 2024.
- The bear with then be 4.
- Discussion. Trade-oﬀ between performance and added cost.
- " Self-Consistency Improves Chain of Thought Reasoning in Language Models ", Wang et al., 2022.
:::
