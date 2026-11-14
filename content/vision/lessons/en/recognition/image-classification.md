---
lesson_id: "image-classification"
course_id: "recognition"
lang: "en"
order_index: 1
title: "Image Classification"
description: "Losses, transfer learning, augmentation and the evaluation details that decide whether a classifier number means anything."
meta_title: "Image Classification - Recognition"
meta_description: "Learn image classification training: transfer learning, fine-tuning, label smoothing, mixup, long-tailed data, calibration and top-k evaluation."
meta_keywords: "image classification, transfer learning, fine-tuning, label smoothing, mixup, calibration, top-k accuracy"
---

Classification assigns one label to a whole image. It is the simplest recognition task to state and the easiest to evaluate badly. Most of the engineering lies in the data pipeline, the transfer strategy and the evaluation protocol rather than the architecture.

## The standard recipe

A modern image classifier is a backbone followed by a global pooling and a linear head. Training minimises cross-entropy over minibatches, usually with label smoothing, strong augmentation and a cosine learning-rate schedule.

Label smoothing replaces the one-hot target with a mixture of the target and a uniform distribution:

$$y' = (1-\epsilon)\, y + \frac{\epsilon}{C}$$

This prevents the model from driving logits to extreme values, improves calibration and slightly regularises. It is standard in most strong training recipes.

Mixup and CutMix augment at the level of samples and labels. Mixup forms convex combinations of inputs and targets; CutMix pastes a patch from one image into another and mixes labels proportionally to area. Both reduce overconfidence and improve robustness, at the cost of longer training.

:::single-choice{#label-smoothing} What does label smoothing change about the training objective?

::option[It replaces one-hot targets with a mixture including a uniform component, limiting overconfidence]{#smoothing-target .correct explanation="The target becomes partly uniform, so the loss cannot be driven to zero by unbounded logits, which improves calibration."}
::option[It removes mislabelled examples from the dataset]{#smoothing-cleaning explanation="Label smoothing is a soft target transformation, not data cleaning."}
::option[It changes the number of classes]{#smoothing-classes explanation="The class set is unchanged; only the target distribution is softened."}
:::

## Transfer learning

Training from scratch requires large labelled datasets and long schedules. Most practical work starts from a pretrained backbone and adapts it. The two main strategies are linear probing and fine-tuning.

**Linear probing** freezes the backbone and trains only the final classifier. It measures the quality of the learned representation and is cheap. **Fine-tuning** updates some or all backbone parameters with a small learning rate. It usually improves accuracy when the target domain differs but risks catastrophic forgetting if the rate is too high or the dataset too small.

A common middle ground is gradual unfreezing: train the head first, then unfreeze the last stage, then earlier stages. Discriminative learning rates — smaller for early layers, larger for later ones — encode the intuition that early features are more generic and should change less.

Batch normalisation statistics need attention during fine-tuning. Freezing the backbone but leaving batch norm in training mode updates running statistics, which can degrade performance on small batches. Many recipes freeze batch norm explicitly when the backbone is frozen.

:::single-choice{#linear-probe} What does a linear probe measure?

::option[How linearly separable the frozen backbone's features are for the target task]{#probe-meaning .correct explanation="Only the final linear layer is trained, so performance reflects the representation quality rather than new feature learning."}
::option[The maximum accuracy achievable with fine-tuning]{#probe-max explanation="Fine-tuning can exceed a linear probe by adapting features; the probe is a lower bound and a diagnostic."}
::option[The inference latency of the backbone]{#probe-latency explanation="Latency is independent of whether the final layer is trained by probing or fine-tuning."}
:::

## Data is the bottleneck

Class imbalance is the norm. Long-tailed distributions mean a few classes have thousands of examples and most have a handful. Plain cross-entropy biases the model toward frequent classes. Remedies include class-balanced sampling, reweighted losses, logit adjustment and two-stage training that decouples representation learning from classifier balancing.

Spurious correlations are subtler. A model trained on photographs of animals may learn background context rather than the animal. A model trained on medical images from one hospital may learn scanner artefacts. These shortcuts produce high in-distribution accuracy and catastrophic failure under distribution shift.

Evaluating for spurious correlation requires datasets with controlled bias, such as Waterbirds or ImageNet-A, or systematic subgroup analysis. Reporting only aggregate accuracy hides the failure.

:::single-choice{#spurious-correlation} A classifier achieves high held-out accuracy but fails in a new hospital. What is the most likely explanation?

::option[It learned a shortcut correlated with the label in the original data, such as scanner or preprocessing artefacts]{#shortcut .correct explanation="Spurious features predict the training distribution but do not transfer, so in-distribution accuracy overstates real performance."}
::option[The model has too few parameters]{#capacity explanation="Capacity usually reduces underfitting; the described pattern is a distribution shift, not a capacity limit."}
::option[The learning rate was too low]{#lr explanation="Optimisation settings can affect accuracy but do not specifically produce domain-specific failure with high in-distribution performance."}
:::

## Evaluation that means something

Top-1 accuracy is the fraction of images whose highest-scoring class is correct. Top-5 counts a prediction as correct if the true class is among the five highest scores. Top-5 is easier and is often reported for ImageNet because fine-grained classes are genuinely ambiguous at low resolution.

Accuracy alone ignores confidence. Calibration measures whether predicted probabilities match observed frequencies: among predictions made with 0.9 confidence, roughly 90 percent should be correct. Modern deep networks are often overconfident, and temperature scaling — dividing logits by a fitted scalar — is a simple post-hoc fix.

Per-class accuracy and confusion matrices reveal systematic errors that aggregate accuracy hides. A model with 90 percent overall accuracy can be near chance on a minority class that matters. For deployment, report the metric that reflects the cost of each error type, not the one that is conventional in papers.

:::single-choice{#calibration} A model's 0.9-confidence predictions are correct only 70 percent of the time. What does this indicate?

::option[The model is overconfident and poorly calibrated, even if its accuracy is high]{#overconfident .correct explanation="Calibration compares stated confidence with empirical accuracy; a large gap means probabilities should not be interpreted as frequencies."}
::option[The model is underfitting]{#calibration-underfit explanation="Underfitting affects accuracy, but calibration is about the relationship between confidence and correctness."}
::option[The test set is too small to compute accuracy]{#calibration-size explanation="The statement describes a measured confidence-accuracy gap, which is a calibration issue regardless of test-set size."}
:::

## Practical checklist

Before reporting a classification result, verify the following.

1. **Split hygiene.** No near-duplicate images across train and test. This is common in scraped datasets and inflates accuracy substantially.
2. **Preprocessing parity.** Training and evaluation use the same resize, crop, colour and normalisation pipeline.
3. **Class mapping.** Label indices are consistent between dataset, model and reported metrics.
4. **Baseline.** Report a linear probe or a simple model, so the gain from complexity is visible.
5. **Subgroup breakdown.** Report accuracy by class, and by any protected or operationally important group.
6. **Confidence behaviour.** Check calibration and the accuracy at the operating threshold you will deploy.

:::callout{type="warning" title="Duplicates inflate everything"}
Near-duplicate images across splits are one of the most common causes of implausible accuracy. Hash images, check perceptual similarity, and inspect the nearest training neighbour of a few test images. If a test image is nearly identical to a training image, the benchmark is measuring memorisation.
:::

## Summary

You can now train, adapt and evaluate an image classifier with defensible numbers.

1. Apply label smoothing, mixup and strong augmentation for calibration and robustness.
2. Choose linear probing, fine-tuning or gradual unfreezing deliberately.
3. Handle long-tailed data and identify spurious shortcuts.
4. Report calibration, per-class accuracy and split hygiene alongside top-k accuracy.
