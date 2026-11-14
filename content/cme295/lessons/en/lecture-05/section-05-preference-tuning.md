---
lesson_id: section-05-preference-tuning
course_id: lecture-05
lang: en
order_index: 5
title: Preference tuning
description: 'Slides 93–111 of lecture 5: 12 slides from the original deck.'
meta_title: Preference tuning — Lecture 5
meta_description: Slide-by-slide walkthrough of Preference tuning, lecture 5.
meta_keywords: Preference tuning, lecture 5, slides
---

## Preference tuning

:::slide{src="../../slides/lecture-05/slide-093.webp" n="93"} Preference tuning

- Transformers &
- Data collection
- Large Language
- RLHF
- Models DPO
:::

:::slide{src="../../slides/lecture-05/slide-094.webp" n="94"} Motivation

- Limitations using RL
- 3 2 1
:::

:::slide{src="../../slides/lecture-05/slide-096.webp" n="96"} Motivation

- Limitations using RL
- Best-of-N is costly at inference time
- Why don't we train in a supervised fashion?
:::

:::slide{src="../../slides/lecture-05/slide-098.webp" n="98"} Supervised approach with DPO

- DPO = Direct Preference Optimization
- Rewrite the loss function in a supervised way:
- No need to train a separate reward model No r(x, y)!
- " Direct Preference Optimization: Your Language Model is Secretly a Reward Model ", Rafailov et al., 2023.
:::

:::slide{src="../../slides/lecture-05/slide-100.webp" n="100"} Supervised approach with DPO

- DPO = Direct Preference Optimization
- Rewrite the loss function in a supervised way:
- No need to train a separate reward model
- Operates directly on preference data
- Similar to the Bradley-Terry formulation with a special kind of reward!
- " Direct Preference Optimization: Your Language Model is Secretly a Reward Model ", Rafailov et al., 2023.
:::

:::slide{src="../../slides/lecture-05/slide-101.webp" n="101"} Supervised approach with DPO

- DPO = Direct Preference Optimization
- Rewrite the loss function in a supervised way:
- " Direct Preference Optimization: Your Language Model is Secretly a Reward Model ", Rafailov et al., 2023.
:::

:::slide{src="../../slides/lecture-05/slide-105.webp" n="105"} Where does the DPO formulation come from?

- 1 Start from PPO objective
- 2 Derive optimal policy
- 3 Identify a "reward" term
- 4 Write Bradley-Terry formulation for this "reward"
- w l
- l w
- l w
- " Direct Preference Optimization: Your Language Model is Secretly a Reward Model ", Rafailov et al., 2023.
:::

:::slide{src="../../slides/lecture-05/slide-106.webp" n="106"} Where does the DPO formulation come from?

- 1 Start from PPO objective
- 2 Derive optimal policy
- 3 Identify a "reward" term
- 4 Write Bradley-Terry formulation for this "reward"
- 5 "Infer" DPO loss function
- " Direct Preference Optimization: Your Language Model is Secretly a Reward Model ", Rafailov et al., 2023.
:::

:::slide{src="../../slides/lecture-05/slide-107.webp" n="107"} Use PPO-based RLHF or DPO?

- Ease of implementation.
- RLHF DPO
- Multi-stage training ● Supervised learning
- Needs extra models: reward ● Base model is the only extra
- model, value model, base model needed
- model
- Performance. No common absolute consensus. Varies from task to task and
- sensitive to implementation.
- " Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study ", Xu et al., 2024.
:::

:::slide{src="../../slides/lecture-05/slide-108.webp" n="108"} Behavior

- Can I put my Pretrained + No, it might get
- teddy bear in instruction damaged. Try hand
- the washer? tuned LLM washing instead.
:::

:::slide{src="../../slides/lecture-05/slide-110.webp" n="110"} Behavior

- Pretrained +
- It's better not to.
- Can I put my instruction
- Your teddy could get
- teddy bear in tuned +
- hurt! A gentle hand
- the washer? preference
- wash is safer.
- tuned LLM
:::

:::slide{src="../../slides/lecture-05/slide-111.webp" n="111"} Thank you for your attention!

:::
