---
lesson_id: section-05-agentic-mindset
course_id: lecture-08
lang: en
order_index: 5
title: Agentic mindset
description: 'Slides 97–135 of lecture 8: 16 slides from the original deck.'
meta_title: Agentic mindset — Lecture 8
meta_description: Slide-by-slide walkthrough of Agentic mindset, lecture 8.
meta_keywords: Agentic mindset, lecture 8, slides
---

## Agentic mindset

:::slide{src="../../slides/lecture-08/slide-097.webp" n="97"} Agentic mindset

- Let's go back to the ReAct framework!
- Input Output
- Observe
- Act Plan
- " ReAct: Synergizing Reasoning and Acting in Language Models ", Yao et al., 2022.
:::

:::slide{src="../../slides/lecture-08/slide-098.webp" n="98"} Agentic mindset

- A typical agentic call...
- Input Output
- Observe
- Act Plan
- " ReAct: Synergizing Reasoning and Acting in Language Models ", Yao et al., 2022.
:::

:::slide{src="../../slides/lecture-08/slide-099.webp" n="99"} Agentic mindset

- ...sees multiple loops
- Observe
- Act Plan
:::

:::slide{src="../../slides/lecture-08/slide-100.webp" n="100"} Tool steps from Lecture 7

- 1. Let LLM ﬁnd argument for relevant function call
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- 2. Make function call
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- 3. Let LLM deduce conclusion based on results
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-08/slide-101.webp" n="101"} Failure modes

- 1. Tool prediction error
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- 2. Make function call
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- 3. Let LLM deduce conclusion based on results
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-08/slide-105.webp" n="105"} Tool prediction error: does not use tool

- Symptom. LLM directly issues a response.
- <function APIs> Sorry, I don't know where
- LLM
- Find a bear near me! I can find one.
- Potential causes.
- Tool router error
- Model doesn't know how to use the tool
- Remedies.
- Retrain the tool router
- SFT-train the model or better adjust the prompt associated to the target API
:::

:::slide{src="../../slides/lecture-08/slide-110.webp" n="110"} Tool prediction error: hallucinates tool

- Symptom. LLM uses a tool that doesn't exist.
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_bear ()
- Potential causes.
- Model is too weak
- API naming is not logical
- Instructions are unclear
- Remedies.
- Upgrade model
- Revamp the API
- Iterate on top-level instructions
:::

:::slide{src="../../slides/lecture-08/slide-114.webp" n="114"} Tool prediction error: uses the wrong tool

- Symptom. LLM uses another available tool.
- recipient = LocalBusiness
- <function APIs> and message = "may I buy a
- LLM
- Find a bear near me! teddy bear?"
- with send_message ()
- Potential causes.
- Tool router error
- Model chose to use the wrong tool
- Remedies.
- Retrain the tool router
- SFT-train the model or better adjust the prompt associated to the target API
:::

:::slide{src="../../slides/lecture-08/slide-118.webp" n="118"} Tool prediction error: infers wrong argument

- Symptom. LLM doesn't feed the right argument to the tool
- <function APIs> location = (0,-0)
- LLM
- Find a bear near me! with find_teddy_bear ()
- Potential causes.
- Argument cannot be inferred
- Model doesn't know how to use the tool
- Remedy.
- Introduce a helper tool and/or ensure the context carries the right information
- SFT-train the model or better adjust the prompt associated to the target API
:::

:::slide{src="../../slides/lecture-08/slide-119.webp" n="119"} Failure modes

- 1. Let LLM ﬁnd argument for relevant function call
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- 2. Tool call error
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- 3. Let LLM deduce conclusion based on results
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-08/slide-122.webp" n="122"} Tool call error: wrong response

- Symptom. The tool either returns a wrong response or an error
- find_teddy_bear (location) Backend ValueError: could not...
- Potential causes.
- The tool returns an incorrect value
- The tool errors instead of returning a value
- Please note that sometimes, errors could be legitimate (not standard practice).
- Remedy. Fix the tool implementation!
:::

:::slide{src="../../slides/lecture-08/slide-125.webp" n="125"} Tool call error: no response

- Symptom. The tool doesn't return anything.
- find_teddy_bear (location) Backend
- Often seen with: the ﬁnal response is hallucinated
- Cause. Either a bug or a "feature" of the tool implementation?
- Remedy.
- Return something, even if it's an empty JSON
- Emit meaningful tool outputs as a general rule
:::

:::slide{src="../../slides/lecture-08/slide-126.webp" n="126"} Failure modes

- 1. Let LLM ﬁnd argument for relevant function call
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- 2. Make function call
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- 3. Response generation error
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-08/slide-131.webp" n="131"} Response generation error: wrong response

- Symptom. Final response doesn't convey the tool's response
- Didn't find any
- {" name ": " Teddy ", … } LLM
- bear!
- Potential causes.
- Model lacks grounding capabilities
- Tool response spams the context window
- Tool response does not convey information meaningfully
- Remedies.
- Upgrade LLM in charge of synthesizing the response
- Trim information returned by the backend
- Make the tool output format descriptive
:::

:::slide{src="../../slides/lecture-08/slide-132.webp" n="132"} Summary

- Failures: does not use/hallucinates/uses the wrong tool, infers wrong argument
- <function APIs> location = (37.42,-122.17)
- LLM
- Find a bear near me! with find_teddy_bear ()
- Failures: wrong response, no response
- find_teddy_bear (location) Backend {" name ": " Teddy ", … }
- Failure: wrong response
- {" name ": " Teddy ", … } LLM response
:::

:::slide{src="../../slides/lecture-08/slide-135.webp" n="135"} Common issues: takeaway

- Modeling
- Weak reasoning, grounding capabilities
- Too much going on in the context window
- Tool modeling isn't right
- Tool
- Tool itself has a problem
- Output of the tool isn't interpretable
- ...special care and patience is need to debug and ﬁx issues!
:::
