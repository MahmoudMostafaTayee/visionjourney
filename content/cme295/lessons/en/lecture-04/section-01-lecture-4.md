---
lesson_id: section-01-lecture-4
course_id: lecture-04
lang: en
order_index: 1
title: Lecture 4
description: 'Slides 1–18 of lecture 4: 12 slides from the original deck.'
meta_title: Lecture 4 — Lecture 4
meta_description: Slide-by-slide walkthrough of Lecture 4, lecture 4.
meta_keywords: Lecture 4, lecture 4, slides
---

## Lecture 4

:::slide{src="../../slides/lecture-04/slide-001.webp" n="1"} Lecture 4

- CME 295: Transformers &
- Large Language Models
- Afshine Amidi & Shervine Amidi
:::

:::slide{src="../../slides/lecture-04/slide-003.webp" n="3"} Logistics

- Midterm.
- When? Friday October 24th, 3:30pm - 5:00pm (duration: 1h30)
- Where? Thornton 110 (i.e. this classroom)
- Topics? Lecture 1 + 2 + 3 + 4
- Final.
- When? Wednesday December 10th, 7:00pm - 8:30pm (duration: 1h30)
- Where? Hewlett Teaching Center 201
- Topics? Lecture 5 + 6 + 7 + 8 + 9
:::

:::slide{src="../../slides/lecture-04/slide-006.webp" n="6"} Recap of last episode…

- FFNN 1
- x FFNN
- FFNN
- Figure from " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-007.webp" n="7"} Recap of last episode…

- FFNN 1
- x FFNN
- FFNN
- Inference optimizations. KV cache, PagedAttention, speculative decoding, GQA,
- multi-head latent attention, multi-token prediction
:::

:::slide{src="../../slides/lecture-04/slide-008.webp" n="8"} Pretraining

- Transformers &
- Training optimizations
- Large Language
- Supervised ﬁnetuning
- Models Parameter-eﬃcient ﬁnetuning
:::

:::slide{src="../../slides/lecture-04/slide-010.webp" n="10"} Paradigm shift

- Traditional ML. Given task, train model from scratch
- Transfer learning. Reuse trained model to some capacity
- Spam detection
- model
- Sentiment extraction
- model
- Translation
- model
:::

:::slide{src="../../slides/lecture-04/slide-013.webp" n="13"} Paradigm for LLM training

- LLM training. Train LLM to understand language, then tune it for end task
- 1 Pretraining 2 "Tuning"
- Spam detection
- model
- "Pretrained" model
- Sentiment extraction
- model
- Translation
- model
:::

:::slide{src="../../slides/lecture-04/slide-014.webp" n="14"} Pretraining overview

- Goal. Learn pattern of language and code
- English teddy_bear.py
- My cute teddy bear is reading by the window, his tiny class TeddyBear :
- paws holding a book almost bigger than him. The def __init__ (self, name):
- afternoon light dances across his soft fur as he turns each self. name = name
- page with great care…
- def hug (self):
- print ( f"{ self.name } gives a warm hug!" )
- Multi-lingual
- TeddyBear ( "Fluffy" ). hug ()...
- Mon ours en peluche est mon plus ﬁdèle compagnon.
- Toujours assis sur mon lit, il m’attend patiemment, prêt à
- écouter mes secrets…
- teddy_bear.go
- ﺖﺨﺗ ور ﻪﺸﯿﻤﻫ .ﺖﺴﻫ ﻦﻣ ﺖﺳود ﻦیﺮﺗ ﯽمﯿﻤﺻ ﻦﻣ یﺪﺗ سﺮﺧ
- ...هﺪﺑ شﻮﮔ ﻦﻣ یﺎﻫ ﻪﺼﻗ ﻪﺑ هﺮﺿﺎﺣ و ﻪتﺴﺸﻧ ﻦﻣ package main
- … func main(){
- println("Teddy bear hug!")
:::

:::slide{src="../../slides/lecture-04/slide-015.webp" n="15"} Pretraining overview

- Goal. Learn pattern of language and code
- Objective function. Predict next token
- A teddy bear is ?
- LLM
- [BOS] A teddy bear is
:::

:::slide{src="../../slides/lecture-04/slide-016.webp" n="16"} Pretraining overview

- Goal. Learn pattern of language and code
- Objective function. Predict next token
- Data mixtures.
- Web-scraped (e.g. Common Crawl, Wikipedia)
- Code (GitHub, StackOverﬂow)
- Teddy bear Wikipedia article , screenshot taken on October 14, 2025. A GitHub repo , screenshot taken on October 15, 2025.
:::

:::slide{src="../../slides/lecture-04/slide-017.webp" n="17"} Pretraining overview

- Goal. Learn pattern of language and code
- Objective function. Predict next token
- Data mixtures.
- Web-scraped (e.g. Common Crawl, Wikipedia)
- Code (GitHub, StackOverﬂow)
- Model Pretraining size (# tokens)
- Size. Approx. trillions of tokens GPT-3 300 billion
- LLaMA 3 15 trillion
- " Language Models are Few-Shot Learners ", Brown et al., 2020. " The Llama 3 Herd of Models ", LLaMA team, 2024.
:::

:::slide{src="../../slides/lecture-04/slide-018.webp" n="18"} Notations

- FLOPs
- FLoating-point OPerations
- Computational performance
- FLOPS or FLOP/s
- FLoating-point OPerations
- per Second
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::
