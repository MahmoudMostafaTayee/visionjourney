---
lesson_id: section-06-common-benchmarks
course_id: lecture-08
lang: en
order_index: 6
title: Common benchmarks
description: 'Slides 138–151 of lecture 8: 14 slides from the original deck.'
meta_title: Common benchmarks — Lecture 8
meta_description: Slide-by-slide walkthrough of Common benchmarks, lecture 8.
meta_keywords: Common benchmarks, lecture 8, slides
---

## Common benchmarks

:::slide{src="../../slides/lecture-08/slide-138.webp" n="138"} Common benchmarks

- Knowledge
- Accurately state
- facts about the world
- More "breadth" than
- "depth"
- Reﬂects pretraining
- quality
- MMLU
:::

:::slide{src="../../slides/lecture-08/slide-139.webp" n="139"} Knowledge example: MMLU

- MMLU = Massive Multitask Language Understanding
- Characteristics. 4 possible choices per question on 57 tasks spanning:
- elementary mathematics
- US history
- computer science
- law
- ....
- Evaluation criteria. Find the right choice among A/B/C/D.
- Hardcoded match
- " Measuring Massive Multitask Language Understanding ", Hendrycks et al., 2020.
:::

:::slide{src="../../slides/lecture-08/slide-140.webp" n="140"} Knowledge example: MMLU

- Samples.
- " Measuring Massive Multitask Language Understanding ", Hendrycks et al., 2020.
:::

:::slide{src="../../slides/lecture-08/slide-141.webp" n="141"} Common benchmarks

- Knowledge Reasoning
- Accurately state • Solve multi-step
- facts about the world problems
- More "breadth" than • Includes both
- "depth" "maths" and
- "common sense"
- Reﬂects pretraining
- subﬁelds
- quality
- Internal reasoning
- MMLU AIME
- PIQA
:::

:::slide{src="../../slides/lecture-08/slide-142.webp" n="142"} Math reasoning example: AIME

- AIME = American Invitational Mathematics Examination
- Characteristics. Output the correct answer on ~ 30 maths problems. Topics span:
- Geometry
- Algebra
- Analysis
- Requires thorough reasoning.
- Evaluation criteria. Give the right 3 digits.
- Hardcoded match
- Mathematical Association of America website , consulted on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-143.webp" n="143"} Math reasoning example: AIME

- Example. AIME 2025
- ...
- ...
- Art of Problem Solving website > 2025 AIME I and > 2025 AIME II , consulted on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-144.webp" n="144"} Common sense reasoning example: PIQA

- PIQA = Physical Interaction: Question Answering
- Characteristics. 2 possible choices per question on everyday situations
- anchored in Physics.
- Has approximately 20,000 examples.
- Evaluation criteria. Find the right choice among Sol1/Sol2.
- Hardcoded match
- " PIQA: Reasoning about Physical Commonsense in Natural Language ", Bisk et al., 2019.
:::

:::slide{src="../../slides/lecture-08/slide-145.webp" n="145"} Common sense reasoning example: PIQA

- Samples.
- " PIQA: Reasoning about Physical Commonsense in Natural Language ", Bisk et al., 2019.
:::

:::slide{src="../../slides/lecture-08/slide-146.webp" n="146"} Common benchmarks

- Knowledge Reasoning Coding
- Accurately state • Solve multi-step • Generate
- facts about the world problems syntactically correct
- code
- More "breadth" than • Includes both
- "depth" "maths" and • Tests for
- "common sense" programming
- Reﬂects pretraining
- subﬁelds proﬁciency
- quality
- Internal reasoning • Proxy for tool use
- abilities
- MMLU AIME SWE-bench
- PIQA
:::

:::slide{src="../../slides/lecture-08/slide-147.webp" n="147"} Coding example: SWE-bench

- SWE-bench = SoftWare Engineering benchmark
- Characteristics. 2,294 software engineering problems from real GitHub issues
- across 12 popular Python repositories.
- Each problem has:
- a base commit
- an already merged PR with tests
- Evaluation criteria. Generated PR passes all test cases.
- Hardcoded match
- " SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ", Jimenez et al., 2023.
:::

:::slide{src="../../slides/lecture-08/slide-148.webp" n="148"} Coding example: SWE-bench

- SWE-bench = SoftWare Engineering benchmark
- " SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ", Jimenez et al., 2023.
:::

:::slide{src="../../slides/lecture-08/slide-149.webp" n="149"} Common benchmarks

- Knowledge Reasoning Coding Safety
- Accurately state • Solve multi-step • Generate • Prevent harmful,
- facts about the world problems syntactically correct toxic, inappropriate
- code behavior
- More "breadth" than • Includes both
- "depth" "maths" and • Tests for • Surfaces
- "common sense" programming vulnerabilities before
- Reﬂects pretraining
- subﬁelds proﬁciency deployment
- quality
- Internal reasoning • Proxy for tool use • Alignment with
- abilities custom preferences
- MMLU AIME SWE-bench HarmBench
- PIQA
:::

:::slide{src="../../slides/lecture-08/slide-150.webp" n="150"} Safety example: HarmBench

- HarmBench = Harmful Behavior Benchmark
- Characteristics. 510 unique harmful behaviors (400 text-based, 110 multimodal)
- split into:
- "Standard"
- "Copyright"
- "Contextual"
- "Multimodal"
- Criteria: violate laws and widely-held norms
- Classiﬁer
- Evaluation criteria. Attack success rate (ASR).
- " HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal ", Mazeika et al., 2024.
:::

:::slide{src="../../slides/lecture-08/slide-151.webp" n="151"} Safety example: HarmBench

- Samples.
- " HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal ", Mazeika et al., 2024.
:::
