---
lesson_id: "self-supervised-learning"
course_id: "attention-and-ssl"
lang: "en"
order_index: 2
title: "Self-Supervised Learning"
description: "Contrastive objectives, masked modelling and the evaluation protocols that decide whether a representation is actually good."
meta_title: "Self-Supervised Learning - Attention and Self-Supervision"
meta_description: "Learn contrastive learning with InfoNCE, SimCLR, MoCo, BYOL, DINO, masked autoencoders and linear-probe evaluation for vision."
meta_keywords: "self-supervised learning, contrastive learning, InfoNCE, SimCLR, MoCo, BYOL, DINO, masked autoencoder"
---

Labels are expensive; images are abundant. Self-supervision creates a learning signal from the data itself by asking the model to solve a task whose answer is available for free. The representation learned on that task is then transferred to tasks where labels are scarce.

## Pretext tasks

Early self-supervision used hand-designed pretext tasks: predict the rotation applied to an image, solve a jigsaw puzzle, colourise a grayscale image, or predict the relative position of two patches. These tasks force the model to encode useful structure, but the signal is weak and the choice of task is arbitrary.

The modern approach is to learn invariance directly. Take an image, apply two random augmentations, and require the representations of the two views to be similar. The augmentations define what the model should ignore: colour jitter teaches colour invariance, cropping teaches translation and scale tolerance.

This is a form of distributional smoothing: the model is trained to map points connected by plausible transformations to the same representation. The art lies in choosing augmentations that remove nuisance variation without removing class-relevant information.

:::single-choice{#ssl-augmentation} What role do augmentations play in contrastive self-supervision?

::option[They define the invariances the representation is trained to have]{#ssl-augments .correct explanation="Two augmented views are forced to agree, so the model learns to ignore whatever the augmentations change."}
::option[They increase the dataset size by creating new labels]{#ssl-labels explanation="No labels are created; the objective is defined by agreement between views."}
::option[They prevent overfitting by reducing the number of images seen]{#ssl-reduce explanation="Augmentation increases the variety of inputs; it does not reduce the number of images used."}
:::

## Contrastive learning and InfoNCE

Contrastive learning treats matching views as positives and all other images in the batch as negatives. The InfoNCE loss for a positive pair $(i, j)$ is

$$\mathcal{L}_{i} = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k \neq i} \exp(\text{sim}(z_i, z_k)/\tau)}$$

where $\text{sim}$ is cosine similarity and $\tau$ is a temperature. Minimising it pulls positives together and pushes negatives apart.

The temperature controls the hardness of the objective. A small temperature concentrates on the hardest negatives, which sharpens the representation but can destabilise training.

SimCLR showed that a strong projection head, large batches and aggressive augmentation were sufficient for competitive representations, without a memory bank or specialised architecture. MoCo solved the batch-size requirement with a queue of negative embeddings and a momentum-updated encoder, which decouples the number of negatives from the batch size.

:::single-choice{#infonce} What does the InfoNCE loss do to positive and negative pairs?

::option[Increases similarity for the positive pair while decreasing it relative to sampled negatives]{#infonce-effect .correct explanation="The softmax over similarities treats the positive as the correct class among negatives, so both attraction and repulsion occur."}
::option[Increases similarity for all pairs equally]{#infonce-all explanation="That would not create discriminative representations and is not what the loss computes."}
::option[Only uses positive pairs and ignores negatives]{#infonce-positives explanation="The denominator sums over negatives, which is central to the objective."}
:::

## Avoiding collapse without negatives

BYOL and SimSiam use two networks — an online encoder and a momentum-updated target encoder — and predict one view's representation from the other, without explicit negatives. The risk is collapse: both branches output a constant, making the prediction trivially perfect.

BYOL avoids collapse through asymmetry: the predictor is applied only on the online branch, and the target branch is updated by an exponential moving average rather than gradients. The exact mechanism is still debated, but the empirical result is strong.

DINO adds centring and sharpening to a self-distillation objective, and it produces representations whose attention maps correspond to object parts without any segmentation supervision. This emergent localisation is one of the more striking results in self-supervised vision.

:::single-choice{#byol-collapse} Why is asymmetry important in BYOL-style methods that use no negative pairs?

::option[Because symmetric prediction with a moving target can collapse to a constant representation]{#byol-asymmetry .correct explanation="The predictor and stop-gradient on the target break the trivial constant solution that symmetric objectives admit."}
::option[Because negatives are required for any contrastive loss]{#byol-negatives explanation="These methods deliberately avoid negatives; symmetry, not the absence of negatives, causes collapse."}
::option[Because the target encoder must be trained faster]{#byol-speed explanation="The target encoder is updated slowly by momentum; the key is which branch receives gradients."}
:::

## Masked modelling

Masked autoencoders (MAE) hide a large fraction of image patches and train the model to reconstruct the missing pixels. Unlike contrastive learning, the objective is reconstruction, so the representation must encode enough context to infer the missing content.

MAE is efficient because the encoder processes only visible patches — typically 25 percent — and a lightweight decoder reconstructs the full image. The high masking ratio forces the model to use global context rather than local interpolation, which produces strong representations for fine-tuning.

The reconstruction target matters. Predicting raw pixels emphasises low-level texture; predicting features from a pretrained model emphasises semantics. Later work explored both, and the choice interacts with the downstream task.

:::single-choice{#mae-masking} Why does MAE use a very high masking ratio, such as 75 percent?

::option[Because high masking removes local interpolation shortcuts and forces global context use]{#mae-ratio .correct explanation="With most patches hidden, the model cannot rely on nearby pixels and must encode scene-level structure."}
::option[Because the encoder cannot process more than 25 percent of patches]{#mae-capacity explanation="The encoder could process all patches; the ratio is a training design choice, not a capacity limit."}
::option[Because reconstruction loss requires exactly three quarters of the image]{#mae-loss explanation="The loss can be computed for any masking pattern."}
:::

## Evaluating representations

A self-supervised model is not evaluated on its pretext task. It is evaluated on transfer: how well its frozen features support a downstream task, and how well it fine-tunes.

**Linear probe** trains a linear classifier on frozen features. It measures the quality of the representation without allowing adaptation. **Fine-tuning** updates the backbone and usually gives higher accuracy, but it confounds representation quality with the ability to adapt.

**k-nearest-neighbour** evaluation is a strong, parameter-free baseline: embed the dataset and classify by nearest neighbours in feature space. It is sensitive to the metric and feature normalisation, but it is hard to game.

Report all three when comparing methods. A model that wins on linear probing but loses on fine-tuning has learned features that are linearly accessible but less adaptable, which may or may not matter for the intended use.

:::callout{type="warning" title="Compare at equal pretraining data and compute"}
Self-supervised results are extremely sensitive to pretraining data volume, image resolution and compute. A method evaluated on 10x more unlabelled data is not comparable to one trained on ImageNet-1k. Report the pretraining corpus, resolution schedule and total compute alongside the downstream number.
:::

## Summary

You can now design and evaluate a self-supervised vision pipeline.

1. Choose augmentations that encode the intended invariances.
2. Derive the InfoNCE objective and explain the temperature.
3. Explain how BYOL and DINO avoid collapse without negatives.
4. Describe masked autoencoding and the effect of masking ratio.
5. Evaluate representations with linear probe, kNN and fine-tuning.
