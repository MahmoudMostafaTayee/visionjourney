---
lesson_id: "vision-language-models"
course_id: "attention-and-ssl"
lang: "en"
order_index: 3
title: "Vision-Language Models"
description: "CLIP-style contrastive alignment, zero-shot classification, captioning and the evaluation of multimodal systems."
meta_title: "Vision-Language Models - Attention and Self-Supervision"
meta_description: "Learn CLIP contrastive pretraining, zero-shot classification, BLIP-2, LLaVA, visual grounding and how to evaluate multimodal vision models."
meta_keywords: "CLIP, vision-language model, zero-shot classification, BLIP-2, LLaVA, visual grounding, multimodal evaluation"
---

Language is a dense, compositional supervision signal that is already attached to most images on the web. Aligning images and text in a shared embedding space turns natural language into a classifier, a retrieval query and an interface for generation.

## Contrastive image-text pretraining

CLIP trains an image encoder and a text encoder to place matching image-text pairs close together and mismatched pairs far apart. For a batch of $N$ pairs, it computes an $N \times N$ matrix of cosine similarities and applies a symmetric cross-entropy loss along both axes.

The batch is the negative pool, so a large batch is essential: with 32k pairs, each image is contrasted against 32k texts. This is why CLIP-style training is compute-hungry but conceptually simple. The learned space is surprisingly structured: "a photo of a dog" lands near dog images, and compositional prompts such as "a photo of a dog playing frisbee" move the embedding in a meaningful direction.

CLIP is not generative. It scores compatibility; it does not produce captions or answer questions. Its importance is as a representation and as a zero-shot classifier.

:::single-choice{#clip-objective} What does CLIP's contrastive objective align?

::option[Image embeddings and text embeddings, so matching pairs have high similarity]{#clip-align .correct explanation="The symmetric loss treats each pair as positive and all other batch combinations as negatives, creating a shared embedding space."}
::option[Image embeddings and class labels, using a fixed vocabulary]{#clip-labels explanation="CLIP uses free-form text, not a fixed label set; the text encoder processes arbitrary prompts."}
::option[Image pixels and generated captions from a language model]{#clip-generation explanation="CLIP does not generate text; it encodes images and text separately for comparison."}
:::

## Zero-shot classification

To classify with CLIP, embed the class names as text prompts, embed the image, and choose the class with the highest similarity. This is zero-shot: no training examples for the target classes are required.

Prompt engineering matters more than it should. "a photo of a {class}" often outperforms the bare class name because it matches the distribution of web captions. Prompt ensembles average over several templates, which reduces variance.

The approach has characteristic failure modes. It struggles with fine-grained distinctions that require expert knowledge, counts, spatial relations and negation. It inherits the biases of its training data, including associations between people and occupations. And its accuracy is sensitive to the class vocabulary: adding a plausible but wrong class can redistribute probability mass.

:::single-choice{#clip-zero-shot} Why does prompt formatting affect zero-shot CLIP accuracy?

::option[Because the text encoder was trained on caption-like sentences, so prompt distribution affects the embedding]{#clip-prompt .correct explanation="Prompts that resemble training captions land in a better-supported region of the text embedding space."}
::option[Because the image encoder changes with the prompt]{#clip-image-encoder explanation="The image embedding is independent of the text prompt; only the text embedding changes."}
::option[Because zero-shot classification retrains the model per prompt]{#clip-retrain explanation="No retraining occurs; the prompt only changes the text embedding used for comparison."}
:::

## Grounding, captioning and visual question answering

Grounded models connect language to image regions. Referring expression comprehension locates the object described by a phrase; phrase grounding links each phrase to a box. These tasks require spatial alignment, not just global similarity.

Captioning models generate a textual description. Early systems used a CNN encoder and an LSTM decoder with attention; modern systems use a vision encoder and a language model decoder, often pretrained on large image-text corpora.

Visual question answering (VQA) takes an image and a question and produces an answer. Large vision-language models such as BLIP-2 and LLaVA connect a frozen vision encoder to a language model through a learned projection or querying mechanism, and instruction-tune on multimodal data.

The architecture pattern is consistent: a vision encoder produces tokens, a projector maps them into the language model's embedding space, and the language model generates text conditioned on both. Freezing the encoders reduces training cost but limits adaptation.

:::single-choice{#vlm-projector} What is the role of the projection layer in a LLaVA-style model?

::option[It maps vision tokens into the language model's embedding space so they can be attended to as context]{#projector-role .correct explanation="The language model operates on embeddings; the projector aligns the visual feature dimension and semantics to that space."}
::option[It compresses the image into a single class label]{#projector-class explanation="The output is a sequence of visual tokens, not a class label."}
::option[It replaces the language model's attention]{#projector-attention explanation="The language model's attention remains; the projector only adapts the visual input."}
:::

## Evaluation and hallucination

Captioning is evaluated with BLEU, METEOR, CIDEr and SPICE, which compare generated text to references. These metrics reward n-gram overlap and are weak proxies for correctness; a fluent but wrong caption can score well. Learned metrics such as CLIPScore measure image-text compatibility and correlate better with human judgement, but they inherit CLIP's blind spots.

VQA accuracy is usually measured against human consensus, with partial credit when multiple annotators disagree. This is necessary because many questions are ambiguous. Reporting a single accuracy without the annotator agreement rate hides that ambiguity.

Hallucination is the central failure mode of generative vision-language models: the model describes objects that are not present, or answers confidently from language priors rather than the image. Mitigations include grounding supervision, contrastive decoding, citation of regions, and evaluation on counterfactual or adversarial images.

:::single-choice{#vlm-hallucination} A captioning model describes a dog that is not in the image. What is the most direct evaluation to detect this failure?

::option[Check whether generated object mentions are grounded in detected or annotated regions]{#grounding-eval .correct explanation="Grounding evaluation verifies that mentioned entities correspond to image evidence, exposing unsupported claims."}
::option[Measure BLEU against a single reference caption]{#bleu-eval explanation="BLEU measures n-gram overlap and can reward fluent hallucinations if references are similar in style."}
::option[Measure inference latency]{#latency-eval explanation="Latency says nothing about factual grounding."}
:::

## Building with multimodal models

For retrieval, embed images and text and use approximate nearest-neighbour search. For classification, use prompt ensembles and validate on a labelled subset. For generation, constrain outputs with grounding or retrieval, and log the evidence used.

Always evaluate on your own distribution. A model that scores well on COCO captions may fail on medical images, engineering diagrams or low-resource languages. The benchmark measures a particular data distribution, and deployment measures another.

:::callout{type="insight" title="Language is a prior and a liability"}
A vision-language model can answer questions that the image alone cannot support, because language models are trained to produce plausible text. That same capacity produces confident errors. Design interfaces that show evidence, allow correction and make uncertainty visible.
:::

## Summary

You can now use and critique vision-language models.

1. Explain CLIP's contrastive objective and the role of batch negatives.
2. Perform zero-shot classification and reason about prompt sensitivity.
3. Describe how projectors connect vision encoders to language models.
4. Evaluate captioning and VQA with awareness of metric limitations.
5. Detect and mitigate hallucination through grounding.
