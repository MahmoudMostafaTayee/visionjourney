---
lesson_id: "training-dynamics"
course_id: "neural-networks-from-scratch"
lang: "en"
order_index: 3
title: "Training Dynamics"
description: "Initialisation, normalisation, regularisation, augmentation and the debugging checklist for deep vision models."
meta_title: "Training Dynamics - Neural Networks from Scratch"
meta_description: "Learn weight initialisation, batch normalisation, dropout, weight decay, augmentation, overfitting diagnosis and training debugging for vision models."
meta_keywords: "weight initialisation, batch normalisation, dropout, weight decay, data augmentation, overfitting, debugging training"
---

Two networks with identical architecture can differ by ten points of accuracy because of initialisation, normalisation and augmentation. Training dynamics is the study of those choices: how signal and gradients propagate, how the model is regularised, and how to tell what is actually wrong.

## Initialisation

Weights cannot be initialised to zero, because every unit in a layer would compute the same output and receive the same gradient, breaking symmetry permanently. They cannot be initialised too large either, because activations and gradients grow exponentially with depth.

The goal is to preserve variance across layers. For a layer with fan-in $n_{\text{in}}$, Xavier or Glorot initialisation uses variance $2/(n_{\text{in}} + n_{\text{out}})$ and was designed for symmetric activations such as tanh. He initialisation uses variance $2/n_{\text{in}}$, accounting for ReLU halving the variance by zeroing negative activations.

Biases are usually initialised to zero, with exceptions such as the forget gate of an LSTM or the final layer of a residual block, where a small positive or zero bias improves early training.

:::single-choice{#init-variance} Why does He initialisation use a variance of 2 divided by fan-in rather than 1 divided by fan-in?

::option[Because ReLU zeroes about half its inputs, halving the variance, so the factor of two compensates]{#he-factor .correct explanation="The factor restores the variance lost by the ReLU's zeroing of negative activations, keeping signal scale stable across layers."}
::option[Because two is the optimal number of layers]{#he-two explanation="The constant comes from the activation's statistics, not from a depth choice."}
::option[Because biases are initialised separately]{#he-bias explanation="Bias initialisation is independent and does not explain the factor."}
:::

## Normalisation

Batch normalisation standardises each channel using the mean and variance computed over the batch and spatial dimensions, then applies a learned scale and shift:

$$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \qquad y = \gamma \hat{x} + \beta$$

It was introduced to reduce internal covariate shift, but the more robust explanation for its effectiveness is that it smooths the loss landscape, allowing larger learning rates and making initialisation less critical.

Batch normalisation has a well-known problem at inference: the statistics must come from somewhere. Frameworks maintain running averages accumulated during training, which creates a train/test discrepancy if the running estimates are poor or if the test batch distribution differs. It also couples samples within a batch, which is problematic for small batches and for distributed training.

Layer normalisation normalises across features for each sample independently, which removes the batch dependency and is the default in transformers. Group normalisation divides channels into groups, offering a middle ground that works well for small-batch detection and segmentation. Instance normalisation normalises each channel per sample and is common in style transfer.

:::single-choice{#bn-inference} What must be handled carefully when moving a batch-normalised network to inference?

::option[The layer must use fixed running statistics rather than statistics computed from the current batch]{#bn-running .correct explanation="Training uses batch statistics; inference uses accumulated running estimates, so mismatched or missing statistics cause a train/test gap."}
::option[The learned scale and shift must be removed]{#bn-remove explanation="The affine parameters are part of the trained model and must remain."}
::option[The epsilon must be set to zero]{#bn-epsilon explanation="Epsilon is a stability constant and must stay nonzero to avoid division by zero."}
:::

## Regularisation

Overfitting is diagnosed by a growing gap between training and validation performance. The remedies attack different causes.

Weight decay penalises the norm of the parameters, discouraging large weights and effectively limiting the complexity of the function. In AdamW the decay is decoupled from the adaptive update, which makes it behave as intended.

Dropout randomly zeroes activations during training, forcing the network to avoid co-adaptation. At inference the activations are scaled to preserve expected magnitude. Dropout is less common in modern convolutional networks, which rely more on augmentation and weight decay, but remains standard in classifier heads and some transformer variants.

Early stopping halts training when validation performance stops improving, which is a cheap and reliable regulariser. Learning-rate schedules and exponential moving averages of weights (EMA) also improve final performance by averaging over the noise of stochastic updates.

:::single-choice{#weight-decay} What does weight decay actually constrain?

::option[The magnitude of the parameters, which limits how extreme the learned function can become]{#wd-magnitude .correct explanation="Penalising the parameter norm shrinks the function class and reduces sensitivity to noise, trading bias for variance."}
::option[The number of active neurons]{#wd-neurons explanation="That is closer to dropout's effect; weight decay acts on parameter magnitudes."}
::option[The learning rate during late training]{#wd-lr explanation="Weight decay is a loss term, not a schedule, although it interacts with the learning rate."}
:::

## Augmentation is the strongest regulariser in vision

For images, data augmentation often matters more than architectural choices. Random crops, horizontal flips, colour jitter, scale changes and rotation synthesise plausible variations and teach invariance.

Mixup and CutMix go further, blending pairs of images and labels. Mixup encourages linear behaviour between samples; CutMix forces the model to use partial evidence. Both improve calibration and robustness, at the cost of longer training.

Augmentation must match the deployment distribution. Horizontal flipping is wrong for text, traffic signs and many medical images. Aggressive cropping can remove small objects and teach the detector that they do not exist. Random erasing can destroy the only evidence of a class. The augmentation policy is a set of assumptions about what should be invariant, and those assumptions should be written down.

:::single-choice{#augmentation-assumption} A team adds random horizontal flips to a dataset of digit images. Why might this hurt?

::option[Because flipping changes the semantic class for digits such as 3, 7 and 9, teaching the wrong invariance]{#flip-digits .correct explanation="Augmentation asserts an invariance; if the label changes under the transform, the model learns to confuse distinct classes."}
::option[Because flipping reduces the effective dataset size]{#flip-size explanation="Flipping increases the number of distinct training examples; the issue is label correctness."}
::option[Because convolutions cannot process flipped images]{#flip-conv explanation="Convolutions are not restricted by orientation; the problem is semantic, not architectural."}
:::

## A debugging checklist

When a model does not train, the cause is usually one of a small set of issues. Work through them in order, because each is cheaper to test than the next.

1. **Overfit a single batch.** If the model cannot drive the loss to near zero on ten examples, the architecture or the loss is wrong.
2. **Check the input pipeline.** Visualise decoded images and labels. Channel order, value range, normalisation statistics and label mapping are common culprits.
3. **Check the loss reduction.** Mean versus sum changes the effective learning rate.
4. **Check for dead units.** A large fraction of zero activations may indicate an excessive learning rate or a bad initialisation.
5. **Check gradient norms.** Exploding gradients need clipping; vanishing gradients need normalisation or a different activation.
6. **Check the evaluation path.** An accidental `train()` during evaluation, or a forgotten `no_grad`, can invalidate every metric.

:::callout{type="insight" title="Loss curves are evidence"}
A flat loss means the model is not learning. A loss that decreases then jumps means instability. A training loss that falls while validation rises means overfitting. A validation loss lower than training loss often means augmentation is applied only during training, which is expected but should be verified.
:::

## Summary

You can now diagnose and fix the common failure modes of training.

1. Choose an initialisation that preserves variance for the activation used.
2. Select a normalisation scheme appropriate to batch size and architecture.
3. Apply weight decay, dropout and early stopping for the right reasons.
4. Design augmentation from an explicit invariance assumption.
5. Debug a non-training model with a systematic checklist.
