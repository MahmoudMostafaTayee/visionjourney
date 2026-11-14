---
lesson_id: section-05-motivation-for-standardized-protocol
course_id: lecture-07
lang: en
order_index: 5
title: Motivation for standardized protocol
description: 'Slides 110–128 of lecture 7: 14 slides from the original deck.'
meta_title: Motivation for standardized protocol — Lecture 7
meta_description: Slide-by-slide walkthrough of Motivation for standardized protocol,
  lecture 7.
meta_keywords: Motivation for standardized protocol, lecture 7, slides
---

## Motivation for standardized protocol

:::slide{src="../../slides/lecture-07/slide-110.webp" n="110"} Motivation for standardized protocol

- Goal. Avoid duplication of tool implementations
- LLM 1 Tool 1
- LLM 2 Tool 2
- LLM 3 Tool 3
:::

:::slide{src="../../slides/lecture-07/slide-112.webp" n="112"} Standardization: MCP

- MCP = Model Context Protocol
- Idea. Connect tools/data to LLMs in a standard way
- LLM 1 Tool 1
- LLM 2 MCP Tool 2
- LLM 3 Tool 3
- " Introducing the Model Context Protocol ", Anthropic, 2024.
:::

:::slide{src="../../slides/lecture-07/slide-113.webp" n="113"} Standardization: MCP

- MCP host
- MCP server
- MCP client
- User
- Tools Prompts Resources
- " About MCP > Architecture overview ", Anthropic, 2024.
:::

:::slide{src="../../slides/lecture-07/slide-114.webp" n="114"} Standardization: MCP

- Claude Desktop
- Book provider
- MCP client MCP server
- "Recommend a new Personal
- Find ﬁnd_title
- collection
- poetry book to my teddy
- bear" recommend_
- Recommend Top books
- taste
- " About MCP > Architecture overview ", Anthropic, 2024.
:::

:::slide{src="../../slides/lecture-07/slide-115.webp" n="115"} RAG

- Transformers &
- Tool calling
- Large Language
- Agents
- Models
:::

:::slide{src="../../slides/lecture-07/slide-117.webp" n="117"} Deﬁnition

- "An agent is a system that autonomously
- pursues goals and completes tasks on a
- user's behalf."
:::

:::slide{src="../../slides/lecture-07/slide-119.webp" n="119"} High-level idea

- Traditional
- Question LLM Answer
- Reasoning
- Question LLM Reasoning Answer
- Agent
- Question LLM Calls LLM Answer
:::

:::slide{src="../../slides/lecture-07/slide-120.webp" n="120"} Overview

- ReAct = Reason + Act
- Input Output
- Observe
- Act Plan
- " ReAct: Synergizing Reasoning and Acting in Language Models ", Yao et al., 2022.
:::

:::slide{src="../../slides/lecture-07/slide-121.webp" n="121"} ReAct in action

- Input
- My teddy bear is cold.
- Please do something.
- Examples:
- Manually entered (e.g. user question)
- External event (e.g. metric going beyond a threshold)
:::

:::slide{src="../../slides/lecture-07/slide-122.webp" n="122"} ReAct in action

- The user's teddy bear is cold, which may
- be due to the current temperature of the
- room, which is currently unknown.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Synthesize previous actions + explicitly state what is currently known
- including own knowledge
- Reasoning-heavy step to ﬁgure out what is needed
:::

:::slide{src="../../slides/lecture-07/slide-123.webp" n="123"} ReAct in action

- The user's teddy bear is cold, which may
- be due to the current temperature of the
- room, which is currently unknown.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Plan
- Determine the temperature
- of the room.
- Detail what tasks need to be accomplished and what tools to call
:::

:::slide{src="../../slides/lecture-07/slide-125.webp" n="125"} ReAct in action

- The user's teddy bear is cold, which may
- be due to the current temperature of the
- room, which is currently unknown.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Act Plan
- Determine the temperature
- get_current_room_temperature () of the room.
- Perform an action via an API
- Look for info in a database of documents
:::

:::slide{src="../../slides/lecture-07/slide-126.webp" n="126"} ReAct in action

- The user's teddy bear is cold, which may
- be due to the current temperature of the
- room, which is currently unknown.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Act Plan
- Determine the temperature
- get_current_room_temperature () of the room.
:::

:::slide{src="../../slides/lecture-07/slide-128.webp" n="128"} ReAct in action

- The temperature in the room is
- currently 65F. This is about 5F less
- than an average temperature. We need
- to increase the room temperature.
- Input
- Observe
- My teddy bear is cold.
- Please do something.
- Act Plan
- Determine the temperature
- get_current_room_temperature () of the room.
:::
