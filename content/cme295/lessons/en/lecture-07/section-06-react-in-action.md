---
lesson_id: section-06-react-in-action
course_id: lecture-07
lang: en
order_index: 6
title: ReAct in action
description: 'Slides 130–150 of lecture 7: 14 slides from the original deck.'
meta_title: ReAct in action — Lecture 7
meta_description: Slide-by-slide walkthrough of ReAct in action, lecture 7.
meta_keywords: ReAct in action, lecture 7, slides
---

## ReAct in action

:::slide{src="../../slides/lecture-07/slide-130.webp" n="130"} ReAct in action

- The temperature in the room is
- currently 65F. This is about 5F less
- than an average temperature. We need
- to increase the room temperature.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Act Plan
- Increase the temperature
- get_current_room_temperature () by 5F.
:::

:::slide{src="../../slides/lecture-07/slide-132.webp" n="132"} ReAct in action

- The temperature in the room is
- currently 65F. This is about 5F less
- than an average temperature. We need
- to increase the room temperature.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Act Plan
- Increase the temperature
- increase_temperature ( value = 5 ) by 5F.
:::

:::slide{src="../../slides/lecture-07/slide-135.webp" n="135"} ReAct in action

- The thermostat is now set to 70F. This
- should be warm enough.
- Input Output
- Observe
- My teddy bear is cold. The thermostat is now
- Please do something. set to 70F. Your
- teddy bear soon feel
- warmer.
- Act Plan
- Increase the temperature
- increase_temperature ( value = 5 ) by 5F.
:::

:::slide{src="../../slides/lecture-07/slide-136.webp" n="136"} "Agentic" view

- Input Output
- My teddy bear is cold. The thermostat is now
- Thermostat agent
- Please do something. set to 70F. Your
- teddy bear soon feel
- warmer.
:::

:::slide{src="../../slides/lecture-07/slide-137.webp" n="137"} There can be agents for many things

- Occupancy
- agent
- Energy
- Thermostat
- management
- agent
- agent
- Air quality
- agent
:::

:::slide{src="../../slides/lecture-07/slide-138.webp" n="138"} How can agents communicate with each other?

- Occupancy
- agent
- Energy
- Thermostat
- management ?
- agent
- agent
- Air quality
- agent
:::

:::slide{src="../../slides/lecture-07/slide-139.webp" n="139"} Standardization: A2A

- A2A = Agent2Agent
- Occupancy
- agent
- A2A
- Energy
- Thermostat
- management A2A
- agent
- agent
- A2A
- Air quality
- agent
- " Announcing the Agent2Agent Protocol (A2A) ", Google, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-140.webp" n="140"} Standardization: A2A

- AgentSkill AgentCard AgentExecutor
- id= 'maintain_ name= 'thermostat async def
- comfort' id= 'prepare_ agent' execute( self , ...):
- home' id= 'optimize_
- description= url= 'http://path. # Logic.
- description= energy'
- 'Maintain a to.agent'
- Thermostat description=
- = comfortable T' 'Sets T to target version= '1.0.0' async def
- agent 'Reduces energy
- examples=[ by arrival' 'Set to skills=[ cancel( self , ...):
- examples=[ consumption' 'Warm
- focus mode while optimize_energy, # Logic.
- up the house to examples=[ 'Save
- I'm working' ] prepare_home,
- 70F when I am energy
- back' overnight' ] ]
- " Agent2Agent (A2A) Protocol Oﬃcial Speciﬁcation ", Google, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-141.webp" n="141"} Safety

- Risks.
- Potential for harm in the real world
- Example: data exﬁltration
- " ToolSword: Unveiling Safety Issues of Large Language Models in Tool Learning Across Three Stages ", Ye et al., 2024.
:::

:::slide{src="../../slides/lecture-07/slide-142.webp" n="142"} Safety

- Risks.
- Potential for harm in the real world
- Example: data exﬁltration
- Remediations.
- Training steps
- Inference safeguards
- Benchmarks, e.g. Agent-SafetyBench
- " Towards Tool Use Alignment of Large Language Models ", Chen et al., 2024.
:::

:::slide{src="../../slides/lecture-07/slide-143.webp" n="143"} Safety

- Risks.
- Potential for harm in the real world
- Example: data exﬁltration
- Remediations.
- Training steps
- Inference safeguards
- Benchmarks, e.g. Agent-SafetyBench
- ...very important topic!
:::

:::slide{src="../../slides/lecture-07/slide-144.webp" n="144"} Just yesterday in the news

- " Disrupting the ﬁrst reported AI-orchestrated cyber espionage campaign ", Anthropic, 2025.
:::

:::slide{src="../../slides/lecture-07/slide-149.webp" n="149"} Closing thoughts

- Hallucination is a (big) problem
- Reasoning abilities are a bottleneck
- Finetuning helps, but hard
- New capabilities are very welcome
- Evaluation is challenging
- Good to start simple, then iterate and progressively scale up
- Good to start with capable models, optimize on size later
- Transparency / observability helps with user trust and debuggability
:::

:::slide{src="../../slides/lecture-07/slide-150.webp" n="150"} Bonus: AI agents in your daily life

- agent
- Personal favorite use case: coding!
:::
