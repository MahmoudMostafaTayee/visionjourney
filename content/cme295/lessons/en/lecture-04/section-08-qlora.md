---
lesson_id: section-08-qlora
course_id: lecture-04
lang: en
order_index: 8
title: QLoRA
description: 'Slides 127–128 of lecture 4: 2 slides from the original deck.'
meta_title: QLoRA — Lecture 4
meta_description: Slide-by-slide walkthrough of QLoRA, lecture 4.
meta_keywords: QLoRA, lecture 4, slides
---

## QLoRA

:::slide{src="../../slides/lecture-04/slide-127.webp" n="127"} QLoRA

- Idea. Quantize all frozen weights to relieve memory bottleneck.
- Beneﬁts.
- VRAM savings enable ﬁnetuning on smaller GPUs, and faster
- Better trade-oﬀ memory resources/quality
- Orders of magnitude. Results reported out of LLaMA 65B:
- ~ 16x VRAM savings during ﬁnetuning
- Double quantization trick saves an extra ~ 6%
- QLoRA: Eﬃcient Finetuning of Quantized LLMs , Dettmers et al., 2023.
:::

:::slide{src="../../slides/lecture-04/slide-128.webp" n="128"} Thank you for your attention!

:::
