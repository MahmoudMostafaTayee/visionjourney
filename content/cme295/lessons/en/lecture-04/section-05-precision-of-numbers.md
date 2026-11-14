---
lesson_id: section-05-precision-of-numbers
course_id: lecture-04
lang: en
order_index: 5
title: Precision of numbers
description: 'Slides 73–90 of lecture 4: 12 slides from the original deck.'
meta_title: Precision of numbers — Lecture 4
meta_description: Slide-by-slide walkthrough of Precision of numbers, lecture 4.
meta_keywords: Precision of numbers, lecture 4, slides
---

## Precision of numbers

:::slide{src="../../slides/lecture-04/slide-073.webp" n="73"} Precision of numbers

- 2.70 15402…
- 1.20 15432…
- 2.40 24402…
- -0.70 55120…
- -1.70 67140…
- 0.27 41131…
- -1.53 12410…
- 0.40 25222…
:::

:::slide{src="../../slides/lecture-04/slide-075.webp" n="75"} Representation of a ﬂoat

- Sign Exponent Mantissa
- FP16
- 1 5 10
- (Floating-Point 16)
- FP32
- 1 8 23
- (Floating-Point 32)
- FP64
- 1 11 52
- (Floating-Point 64)
- BFLOAT16
- 1 8 7
- (Brain Float 16)
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-04/slide-077.webp" n="77"} Example of a GPU

- 🔻 🐇
- Lower precision → Faster processing
- " NVIDIA H100 Tensor Core GPU ", NVIDIA website.
:::

:::slide{src="../../slides/lecture-04/slide-078.webp" n="78"} Mixed precision training

- Objective. Speed up training and decrease memory requirements
- " Mixed Precision Training ", Micikevicius et al., 2017.
:::

:::slide{src="../../slides/lecture-04/slide-081.webp" n="81"} Mixed precision training

- Objective. Speed up training and decrease memory requirements
- Forward pass. Activations in low precision
- Backwards pass. Gradient updates in low precision
- Weights update. Keep weights in high precision
:::

:::slide{src="../../slides/lecture-04/slide-082.webp" n="82"} Pretraining

- Transformers &
- Training optimizations
- Large Language
- Supervised ﬁnetuning
- Models Parameter-eﬃcient ﬁnetuning
:::

:::slide{src="../../slides/lecture-04/slide-083.webp" n="83"} What we covered in the ﬁrst part of this lecture

- Initialized model
- Pretraining
- Model with "basic
- knowledge" about
- language, code, etc.
:::

:::slide{src="../../slides/lecture-04/slide-085.webp" n="85"} Pretrained model behavior

- Teddy bears are often
- made of materials like
- Can I put my
- Pretrained polyester and cotton,
- teddy bear in
- LLM with plastic eyes and
- the washer?
- sometimes small
- accessories.
:::

:::slide{src="../../slides/lecture-04/slide-086.webp" n="86"} Remedy

- Initialized model
- Pretraining Finetuning
- Model with "basic
- Model tuned for
- knowledge" about
- speciﬁc tasks
- language, code, etc.
:::

:::slide{src="../../slides/lecture-04/slide-088.webp" n="88"} Supervised ﬁnetuning

- SFT = Supervised FineTuning
- Idea. Change the model behavior by tuning its weights
- Strategy.
- Collect pairs of input/outputs with desired behavior (aka SFT data)
- Train using next word prediction objective given the input
- Special case. SFT on instruction-following data: "Instruction tuning"
:::

:::slide{src="../../slides/lecture-04/slide-089.webp" n="89"} Instruction tuning overview

- Goal. "Graduate" the model to being a helpful assistant.
- " Finetuned language models are zero-shot learners ", Wei et al., 2022.
:::

:::slide{src="../../slides/lecture-04/slide-090.webp" n="90"} Instruction tuning overview

- Goal. "Graduate" the model to being a helpful assistant.
- Story writing Lists generation
- Write a short story about a teddy bear who likes to read List three fun activities a teddy bear might do on a rainy
- poetry. day.
- Once upon a time, a bear, Teddy, stumbled upon verses Sure!
- from Attar. The bear became so captivated with the 1. Read poetry with friends.
- rhythm of the poem's sentences that he got ﬁlled with 2. Be cute.
- happiness. 3. Hug its owner tightly.
- Poem creation Explanation
- Create a poem about my cute teddy bear. Explain why a teddy bear is a great friend.
- Soft and cuddly, full of charm, A teddy bear is a great friend because it provides comfort
- Always keeps me safe from harm, and companionship. Its soft fur and cuddly nature is
- With button eyes and fur so neat, perfect for hugs. Teddy bears are always there in both
- My teddy bear is oh so sweet. happy and sad moments.
:::
