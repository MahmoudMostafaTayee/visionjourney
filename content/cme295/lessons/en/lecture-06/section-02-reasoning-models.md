---
lesson_id: section-02-reasoning-models
course_id: lecture-06
lang: en
order_index: 2
title: Reasoning models
description: 'Slides 15–46 of lecture 6: 14 slides from the original deck.'
meta_title: Reasoning models — Lecture 6
meta_description: Slide-by-slide walkthrough of Reasoning models, lecture 6.
meta_keywords: Reasoning models, lecture 6, slides
---

## Reasoning models

:::slide{src="../../slides/lecture-06/slide-015.webp" n="15"} Reasoning models

- Transformers &
- Scaling with RL
- Large Language
- GRPO
- Models Applications
:::

:::slide{src="../../slides/lecture-06/slide-017.webp" n="17"} Terminology

- Tentative deﬁnition
- Reasoning = Ability to solve a problem
- Not reasoning Reasoning
- "What is the course code of Stanford's "The bear was born in 2020. How old is
- Transformers & LLMs class?" this bear now?"
:::

:::slide{src="../../slides/lecture-06/slide-021.webp" n="21"} Core idea behind improving reasoning

- Strategy. Teach model to explain its reasoning before answering (Chain of Thought)
- Q: How old is this bear? A: It will be one
- A: The bear was born in year older than
- 2020. It is therefore 4. its age this year,
- LLM which was 4.
- Hence, it will be
- Q: How old will the bear
- 5.
- be next year?
- Idea for reasoning models: Do CoT but at a much larger scale.
- " Chain-of-Thought Prompting Elicits Reasoning in Large Language Models ", Wei et al., 2022.
:::

:::slide{src="../../slides/lecture-06/slide-024.webp" n="24"} Enhancing model reasoning abilities

- Until now
- Question LLM Answer
- New paradigm
- Reasoning
- Question LLM Answer
- chain
- Output = Reasoning + Answer
:::

:::slide{src="../../slides/lecture-06/slide-025.webp" n="25"} Reasoning model release is trendy

- Disclaimer: This timeline is not at scale for better readability. It is also there for illustrative purposes and should not be considered exhaustive.
- In particular, it shows the ﬁrst releases of popular AI labs.
- 2024 2025
- OpenAI DeepSeek Claude 3.7
- o1-preview R1 Sonnet
- 9/12 12/19 1/20 2/19 2/24 6/10
- Gemini 2.0 Grok 3 Magistral
- Flash Thinking Beta
- Public model release announcements on 2024-09-12 , 2024-12-19 , 2025-01-20 , 2025-02-19 , 2025-02-24 , 2025-06-10 .
:::

:::slide{src="../../slides/lecture-06/slide-028.webp" n="28"} How to spot a reasoning model

- "Thought summary"
- Complete chain of
- thought usually hidden
- Screenshot of a conversation with ChatGPT 5 Thinking, taken on November 3, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-030.webp" n="30"} How to spot a reasoning model

- Anthropic
- OpenAI
- Google
- OpenAI pricing page , Anthropic developer guide , Google developer guide . Screenshots taken on November 4th, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-033.webp" n="33"} Reasoning-based benchmarks

- Coding. Solve a coding problem, ﬁx a bug.
- Test case #1 ✅
- Test case #2 ✅
- def second_biggest_bear (bears): …
- You have n teddy bears in a
- line. Each bear has a size. largest = max (bears)
- return max ( Test case #t ✅
- Find the biggest bear that is b for b in bears
- smaller than the largest bear. if b < largest
- Problem Solution Veriﬁcation
:::

:::slide{src="../../slides/lecture-06/slide-034.webp" n="34"} Reasoning-based benchmarks

- Coding. Solve a coding problem, ﬁx a bug.
- Examples: HumanEval, CodeForces, SWE-bench
- Screenshot of the HumanEval dataset in HuggingFace Dataset , taken on November 3rd, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-037.webp" n="37"} Reasoning-based benchmarks

- Coding. Solve a coding problem, ﬁx a bug.
- Math. Solve a challenging math problem (e.g. olympiads)
- It is 2025 now. Subtract the
- The bear was born in 2020. birth year from the current
- How old is the bear now? year: 2025-2020=5. ✅ 5
- Veriﬁcation
- Answer: 5
- Problem Reasoning Ground truth
:::

:::slide{src="../../slides/lecture-06/slide-038.webp" n="38"} Reasoning-based benchmarks

- Coding. Solve a coding problem, ﬁx a bug.
- Math. Solve a challenging math problem (e.g. olympiads)
- Examples: AIME, GSM8K
- Screenshot of the AIME dataset in HuggingFace Dataset , taken on November 3rd, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-044.webp" n="44"} Reasoning-based benchmark metrics

- Pass@k = "Probability that at least 1 of k attempts succeeds"
- Attempt #1 #2 … #n
- Successful Unsuccessful
- Special
- case
- " Evaluating Large Language Models Trained on Code ", Chen et al., 2021.
:::

:::slide{src="../../slides/lecture-06/slide-045.webp" n="45"} Reasoning-based benchmark metrics

- Pass@k = "Probability that at least 1 of k attempts succeeds"
- " Evaluating Large Language Models Trained on Code ", Chen et al., 2021.
:::

:::slide{src="../../slides/lecture-06/slide-046.webp" n="46"} Reasoning-based benchmark metrics

- Pass@k. For use cases where checking is easy / can aﬀord higher latency
- Pass@1. For use cases where we care about a single generation
- " Evaluating Large Language Models Trained on Code ", Chen et al., 2021.
:::
