---
lesson_id: section-04-next-token-prediction
course_id: lecture-03
lang: en
order_index: 4
title: Next token prediction
description: 'Slides 41–75 of lecture 3: 13 slides from the original deck.'
meta_title: Next token prediction — Lecture 3
meta_description: Slide-by-slide walkthrough of Next token prediction, lecture 3.
meta_keywords: Next token prediction, lecture 3, slides
---

## Next token prediction

:::slide{src="../../slides/lecture-03/slide-041.webp" n="41"} Next token prediction

- A teddy bear is ?
- LLM
- [BOS] A teddy bear is
:::

:::slide{src="../../slides/lecture-03/slide-044.webp" n="44"} Predicting next token

- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017. " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-046.webp" n="46"} Predicting next token with greedy decoding

- 1 st idea. Take token with highest predicted probability
- Limitations. Output not optimal, natural and/or diverse
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017. " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-051.webp" n="51"} Predicting next token with beam search

- 2 nd idea. Keep k paths that are the most likely
- 0.7
- cute
- 0.2
- teddy
- bear
- 0.2
- [BOS] cute
- fluffy
- the sleepy
- 0.6
- dog
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-055.webp" n="55"} Predicting next token with beam search

- 2 nd idea. Keep k paths that are the most likely
- cute kitten
- teddy teddy
- bear bear
- Ends at [EOS]
- [BOS] cute sloth
- fluffy
- the sleepy bear
- dog dog
- Limitations. Needs computations + lacks diversity/creativity
- Figure adapted from " Attention is All You Need ", Vaswani et al., 2017.
:::

:::slide{src="../../slides/lecture-03/slide-056.webp" n="56"} Predicting next token with sampling

- 3 rd idea. Sample next token from probability distribution:
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-058.webp" n="58"} Sampling strategies

- Top-k: Sample among top k most probable tokens
- k = 4
- Top-p: Random sample among smallest set of tokens with
- cumulative probability >= p
- p = 90%
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-059.webp" n="59"} Next token prediction

- But how are probabilities obtained?
:::

:::slide{src="../../slides/lecture-03/slide-061.webp" n="61"} Probability computation

- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-062.webp" n="62"} Temperature allows to tweak output probabilities

- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
:::

:::slide{src="../../slides/lecture-03/slide-064.webp" n="64"} Impact of temperature on probabilities

- Small T
- High T
- " Super Study Guide: Transformers and Large Language Models ", Amidi et al., 2024.
- Suggested reading: " Defeating Nondeterminism in LLM Inference ", He et al., 2025.
:::

:::slide{src="../../slides/lecture-03/slide-065.webp" n="65"} Constraining the output via guided decoding

- Motivation. Generate output in a speciﬁc format
- Desired output (JSON)
- Input prompt
- Generate a description of my
- 33-year old teddy bear who
- "first_name" : "teddy" ,
- likes reading.
- "last_name" : " bear" ,
- Do this in JSON format. "age" : 33 ,
- "hobby" : " reading"
:::

:::slide{src="../../slides/lecture-03/slide-075.webp" n="75"} Constraining the output via guided decoding

- Idea. Only allow "valid" next tokens
- road
- { sun , 10
- [BOS] the "first_name" : "Jane"
- } to "teddy"
:::
