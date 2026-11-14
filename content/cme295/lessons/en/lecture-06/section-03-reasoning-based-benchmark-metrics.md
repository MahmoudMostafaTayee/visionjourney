---
lesson_id: section-03-reasoning-based-benchmark-metrics
course_id: lecture-06
lang: en
order_index: 3
title: Reasoning-based benchmark metrics
description: 'Slides 47–97 of lecture 6: 14 slides from the original deck.'
meta_title: Reasoning-based benchmark metrics — Lecture 6
meta_description: Slide-by-slide walkthrough of Reasoning-based benchmark metrics,
  lecture 6.
meta_keywords: Reasoning-based benchmark metrics, lecture 6, slides
---

## Reasoning-based benchmark metrics

:::slide{src="../../slides/lecture-06/slide-047.webp" n="47"} Reasoning-based benchmark metrics

- Pass@k. For use cases where checking is easy / can aﬀord higher latency
- Pass@1. For use cases where we care about a single generation
- Cons@k. "Consensus at k", equivalent to comparing the answer from
- majority voting with the ground truth
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-048.webp" n="48"} Reasoning models

- Transformers &
- Scaling with RL
- Large Language
- GRPO
- Models Applications
:::

:::slide{src="../../slides/lecture-06/slide-053.webp" n="53"} Develop "test-time scaling"

- Idea. Incentivize model to reason before answering.
- Considerations.
- Reasoning chain is hard to write from scratch (SFT data by hand impractical)
- Don't want to limit the model to human-written reasoning
- Natural veriﬁable reward ("did it solve the problem?" → "yes" or "no")
- Let's try RL!
:::

:::slide{src="../../slides/lecture-06/slide-056.webp" n="56"} Reward 1: verify that CoT is there

- <think>
- </think>
- ANSWER
- Template Sample response
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-058.webp" n="58"} Reward 2: verify that solution is correct

- Test case #1 ✅
- Test case #2 ✅
- Test case #c ✅
- It is 2025 now. Subtract the
- birth year from the current
- year: 2025-2020=5. 5
- Answer: 5
- Code veriﬁcation Math veriﬁcation
:::

:::slide{src="../../slides/lecture-06/slide-062.webp" n="62"} Run RL on "veriﬁable" rewards

- Rewards
- formatting
- ( think delimiters?)
- accuracy
- (correct solution?)
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::

:::slide{src="../../slides/lecture-06/slide-065.webp" n="65"} Control thinking at inference time

- Problem. Not all prompts are equal
- Ideas to control "thinking".
- Dynamic budget
- Context awareness
- " Token-Budget-Aware LLM Reasoning ", Han et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-066.webp" n="66"} Control thinking at inference time

- Problem. Not all prompts are equal
- Ideas to control "thinking".
- Dynamic budget
- Context awareness
- Budget forcing
- " s1: Simple test-time scaling ", Muennighoﬀ et al., 2025.
:::

:::slide{src="../../slides/lecture-06/slide-067.webp" n="67"} Control thinking at inference time

- Problem. Not all prompts are equal
- Ideas to control "thinking".
- Dynamic budget
- Context awareness
- Budget forcing
- "Continuous" thoughts
- " Training Large Language Models to Reason in a Continuous Latent Space ", Hao et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-068.webp" n="68"} Reasoning models

- Transformers &
- Scaling with RL
- Large Language
- GRPO
- Models Applications
:::

:::slide{src="../../slides/lecture-06/slide-072.webp" n="72"} Common RL algorithm for reasoning

- GRPO = Group Relative Policy Optimization
- Don't deviate too much
- Maximize advantages
- from old / base model
- Advantage ~ Reward - Avg(reward of group)
- Big diﬀerence compared to PPO!
- " DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models ", Shao et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-092.webp" n="92"} Comparison between GRPO and PPO

- Similarities. Ratio, clipping
- GRPO
- PPO
- Figure from " DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models ", Shao et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-094.webp" n="94"} Comparison between GRPO and PPO

- Diﬀerences. KL penalty, advantage estimation
- GRPO
- PPO
- Figure from " DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models ", Shao et al., 2024.
:::

:::slide{src="../../slides/lecture-06/slide-097.webp" n="97"} "Increasing output length" phenomenon

- Observation. Response length keeps on increasing with RL training
- " DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning ", DeepSeek-AI, 2025.
:::
