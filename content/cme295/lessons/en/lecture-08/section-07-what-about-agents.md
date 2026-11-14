---
lesson_id: section-07-what-about-agents
course_id: lecture-08
lang: en
order_index: 7
title: What about agents?
description: 'Slides 153–170 of lecture 8: 14 slides from the original deck.'
meta_title: What about agents? — Lecture 8
meta_description: Slide-by-slide walkthrough of What about agents?, lecture 8.
meta_keywords: What about agents?, lecture 8, slides
---

## What about agents?

:::slide{src="../../slides/lecture-08/slide-153.webp" n="153"} What about agents?

- 𝜏 -bench = Tool-Agent-User Interaction Benchmark
- Characteristics. A given set of database schema, APIs and policies across 2
- domains:
- Airline agent
- 500 users, 300 ﬂights, 2000 reservations
- ~ 10 tools and 50 tasks
- Retail agent
- 500 users, 50 products, 1000 orders
- ~ 10 tools and 115 tasks
- Evaluation criteria. Maximize reward and pass^k.
- Hardcoded match
- " τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains ", Yao et al., 2024.
:::

:::slide{src="../../slides/lecture-08/slide-154.webp" n="154"} What about agents?

- Sample.
- " τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains ", Yao et al., 2024.
:::

:::slide{src="../../slides/lecture-08/slide-157.webp" n="157"} Metric for consistency/reliability

- Pass^k = "Probability that all k attempts succeed"
- Attempt #1 #2 … #n
- Successful Unsuccessful
- " τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains ", Yao et al., 2024.
:::

:::slide{src="../../slides/lecture-08/slide-158.webp" n="158"} In the news!

- Gemini 3 launch,
- 3 days ago*
- *No pun intended.
- " A new era of intelligence with Gemini 3 ", Pichai et al., November 18, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-159.webp" n="159"} In the news!

- reasoning
- coding
- tool use
- knowledge
- " A new era of intelligence with Gemini 3 ", Pichai et al., November 18, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-160.webp" n="160"} Proﬁle

- Role of benchmarks.
- A projection of performance across a given axis
- Diﬀerent models may be good at diﬀerent
- things
- " Swallow LLM Leaderboard v2 > Post-trained models ", screenshot taken on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-161.webp" n="161"} Proﬁle

- Role of benchmarks.
- A projection of performance across a given axis
- Diﬀerent models may be good at diﬀerent
- things
- Examples. Each person may have their own
- empirical "facts":
- Claude's Sonnet models: coding
- Gemini's Flash models: cheap
- ...
:::

:::slide{src="../../slides/lecture-08/slide-163.webp" n="163"} Pareto frontier

- Deﬁnition. Pareto curve = set of solutions that "optimizes" a trade-oﬀ.
- Possible trade-oﬀs.
- quality vs. cost/latency
- quality vs. safety
- quality vs. context length
- " LLM Arena Pareto Frontier: Performance vs Cost (April 2025) ", screenshot taken on November 18th, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-165.webp" n="165"} Beware of data contamination

- Problem. Benchmark's clues may be contained in the training set
- Precautions.
- Use an identiﬁer such as a hash
- Google's BIG-bench GitHub page at ﬁle google/BIG-bench/docs/doc.md , 2025.
:::

:::slide{src="../../slides/lecture-08/slide-166.webp" n="166"} Beware of data contamination

- Problem. Benchmark's clues may be contained in the training set
- Precautions.
- Use an identiﬁer such as a hash
- For tools, use a blocklist
- Model Evaluation - Approach, Methodology & Results, Gemini 3 Pro , Google, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-167.webp" n="167"} Beware of data contamination

- Problem. Benchmark's clues may be contained in the training set
- Precautions.
- Use an identiﬁer such as a hash
- For tools, use a blocklist
- Evaluate on newer test versions!
- " A new era of intelligence with Gemini 3 ", Pichai et al., November 18, 2025.
:::

:::slide{src="../../slides/lecture-08/slide-168.webp" n="168"} Limitations

- "When a measure becomes a target, it
- ceases to be a good measure."
- -Goodhart's Law
- p.308 of "‘ Improving ratings’: audit in the British University system ", Strathern, 1997.
:::

:::slide{src="../../slides/lecture-08/slide-169.webp" n="169"} Limitations

- "When a measure becomes a target, it
- ceases to be a good measure."
- -Goodhart's Law
- Lessons.
- Should not over-index on benchmarks
- Need for ~ organic perspectives to complete the picture: Chatbot Arena
- ...just try a few models out yourself!
:::

:::slide{src="../../slides/lecture-08/slide-170.webp" n="170"} Thank you for your attention!

:::
