---
lesson_id: section-04-step-2-reinforcement-learning
course_id: lecture-05
lang: en
order_index: 4
title: 'Step 2: Reinforcement learning'
description: 'Slides 55–92 of lecture 5: 14 slides from the original deck.'
meta_title: 'Step 2: Reinforcement learning — Lecture 5'
meta_description: 'Slide-by-slide walkthrough of Step 2: Reinforcement learning, lecture
  5.'
meta_keywords: 'Step 2: Reinforcement learning, lecture 5, slides'
---

## Step 2: Reinforcement learning

:::slide{src="../../slides/lecture-05/slide-055.webp" n="55"} Step 2: Reinforcement learning

- Data.
- O(100,000) observations
- label = score given by reward model
- Model. Initialized at SFT model Avoid "reward hacking" + training instability
- Training. Change weights of policy (LLM) via objective function:
- Don't deviate too much
- Maximize rewards
- from base model
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::

:::slide{src="../../slides/lecture-05/slide-057.webp" n="57"} Common RL algorithm: PPO

- PPO = Proximal Policy Optimization
- Don't deviate too much
- Maximize rewards
- from base model
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-059.webp" n="59"} Common RL algorithm: PPO

- PPO = Proximal Policy Optimization
- Don't deviate too much
- Maximize rewards
- from base model
- " Training language models to follow instructions with human feedback ", Ouyang et al., 2022.
:::

:::slide{src="../../slides/lecture-05/slide-060.webp" n="60"} Common RL algorithm: PPO

- PPO = Proximal Policy Optimization
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-05/slide-065.webp" n="65"} PPO actually computes advantages (and not just rewards)

- Don't deviate too much
- Maximize advantages
- from base model
- Advantage ~ Reward - Baseline Value
- function
- Value function.
- Token-level
- What would be the reward if follow the policy
- Trained jointly with policy
- GAE method
- Label = reward
- Suggested reading: " High-Dimensional Continuous Control Using Generalized Advantage Estimation ", Schulman et al., 2015.
:::

:::slide{src="../../slides/lecture-05/slide-067.webp" n="67"} Variation 1: PPO-Clip

- Idea. Clip ratio between new and old policy to prevent large updates
- with
- Terminology. Confusing since it is an objective
- function (" maximize ") and NOT a loss.
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-068.webp" n="68"} Variation 1: PPO-Clip

- Idea. Clip ratio between new and old policy to prevent large updates
- with
- Terminology. Confusing since rewards noted "r".
- Here we are talking about the ratio .
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-070.webp" n="70"} Variation 1: PPO-Clip

- Idea. Clip ratio between new and old policy to prevent large updates
- with
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-073.webp" n="73"} Variation 2: PPO-KL Penalty

- Idea. Penalize diﬀerence in policy distributions
- Terminology.
- old = model from previous RL iteration
- ref = base model
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-074.webp" n="74"} Variation 2: PPO-KL Penalty

- Idea. Penalize diﬀerence in policy distributions
- Nowadays, KL divergence is with respect
- to ref (base model)
- " Proximal Policy Optimization Algorithms ", Schulman et al., 2017.
:::

:::slide{src="../../slides/lecture-05/slide-076.webp" n="76"} Alternatives of PPO

- Limitations of PPO.
- Need 4 models (policy, value, reward model, base)
- Is it worth it?
- Variants.
- REINFORCE
- GRPO
- … and many more!
- " DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models ", Shao et al., 2024.
:::

:::slide{src="../../slides/lecture-05/slide-082.webp" n="82"} Challenges with RL-based approach

- Requires training a reward model (2-stage process)
- Many hyperparameters to tune
- Training instability
- Metric to monitor training
- Need diversity in completions!
- Not abundantly clear why preference tuning absolutely needs RL
:::

:::slide{src="../../slides/lecture-05/slide-085.webp" n="85"} Workaround if we don't want to do RL

- BoN = Best of N
- Idea. Skip the RL step and leverage the reward model scores
- Strategy.
- Given a prompt, generate several outputs with SFT model
- Rank output with score given by reward model
- Take the best one
:::

:::slide{src="../../slides/lecture-05/slide-092.webp" n="92"} BoN in action

- Of course! Teddy bears not
- only make awesome companions
- for a delightful sleep, but 0.8
- RM 1
- can also be great buddies for
- fun activities. How about you
- both watch a movie together?
- Suggest a new
- activity I I'd suggest you do not spend
- could do with LLM much time with your teddy RM -2 3
- SFT
- my teddy bear at all.
- bear.
- Take your teddy bear on a 0.2
- RM 2
- picnic in your backyard.
:::
