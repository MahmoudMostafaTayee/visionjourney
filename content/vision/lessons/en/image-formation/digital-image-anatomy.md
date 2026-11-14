---
lesson_id: "digital-image-anatomy"
course_id: "image-formation"
lang: "en"
order_index: 3
title: "The Anatomy of a Digital Image"
description: "Sampling, aliasing, quantisation, channels, layouts and the tensor conventions that decide what a model can resolve."
meta_title: "The Anatomy of a Digital Image - Image Formation"
meta_description: "Understand sampling and the Nyquist limit, quantisation, bit depth, channel layouts, normalisation and image tensor conventions in vision."
meta_keywords: "image sampling, Nyquist, aliasing, quantisation, bit depth, NCHW, NHWC, image tensor"
---

An image file is a rectangular array of numbers plus a set of conventions about what those numbers mean. Confusing the conventions — channel order, value range, colour space, layout — accounts for a large share of real-world vision failures. This lesson makes the conventions explicit.

## Sampling and the Nyquist limit

A sensor discretises a continuous light field on a grid. The sampling theorem states that a signal can be reconstructed exactly only if it contains no frequencies above half the sampling rate. That limit is the Nyquist frequency.

Above it, frequencies alias: a high-frequency pattern is recorded as a lower-frequency one that was not present in the scene. The classic visual is a fine checkerboard or fabric weave producing moiré. Once aliased, the pattern is indistinguishable from a genuine low-frequency structure, so no post-processing can remove it.

The practical consequence is that you must low-pass filter *before* downsampling. Averaging pixels, as in area interpolation, is a crude but valid anti-aliasing filter. Nearest-neighbour resizing samples without filtering and therefore aliases. This is why a model trained on images resized with nearest-neighbour can learn spurious high-frequency texture.

:::single-choice{#nyquist-aliasing} What is the correct order of operations when reducing an image's resolution?

::option[Downsample first, then apply a blur to remove the artefacts]{#blur-after explanation="Aliasing has already folded high frequencies into low ones. Blurring afterwards removes real detail without restoring the original signal."}
::option[Low-pass filter first, then sample on the coarser grid]{#filter-first .correct explanation="Removing frequencies above the new Nyquist limit before sampling prevents them from folding into the retained band."}
::option[Sample at the original rate and rely on the network to ignore aliasing]{#learn-aliasing explanation="Networks can become sensitive to aliasing rather than invariant to it; the information is corrupted, not merely noisy."}
:::

## Quantisation and bit depth

Each sample is stored with finite precision. An 8-bit channel has 256 levels; 10-bit has 1024; 16-bit has 65536. Quantisation error behaves like additive noise of roughly uniform distribution with standard deviation about $1/\sqrt{12}$ of a code step.

Bit depth matters most in the shadows, where the signal is small. A 10-bit capture retains four times as many levels per stop, which is why HDR and scientific imaging use it. For display and most pretrained models, 8 bits is standard, but the preprocessing pipeline should be aware that repeated 8-bit round trips accumulate error.

Floating-point images are common in intermediate representations. A float32 tensor can hold linear radiance without banding, and normalising to a zero-mean unit-variance range makes optimisation better conditioned. The convention differs between ecosystems: PyTorch vision models typically expect inputs scaled to the range zero to one and then normalised by dataset statistics, while some older pipelines expect zero to 255. Feeding the wrong range is a silent accuracy loss.

:::single-choice{#value-range} A model trained with inputs in the range zero to one receives images in the range zero to 255. What is the likely symptom?

::option[The model outputs nonsense immediately with a clear error]{#loud-failure explanation="Shape and dtype checks pass; the failure is numerical and often silent, appearing as poor accuracy."}
::option[The first layer saturates, gradients vanish, and accuracy collapses]{#saturation .correct explanation="Large pre-activations push nonlinearities into saturation, destroying gradient flow. The model runs but performs badly."}
::option[Nothing changes because the network normalises internally]{#auto-normalise explanation="Most models do not adapt their input scale automatically; the normalisation statistics were fixed during training."}
:::

## Channels, layouts and the tensor contract

A colour image has three or four channels. The storage layout decides how they are arranged in memory:

- **HWC** — height, width, channels; the convention in most image libraries and in TensorFlow.
- **CHW** — channels first; the convention in PyTorch.
- **NHWC / NCHW** — the same with a leading batch dimension.

The layout affects performance because memory access patterns differ. Convolution implementations often prefer channels-last on tensor cores and channels-first on other backends, which is why conversion is a standard optimisation step.

Channel order also matters. OpenCV loads images in BGR order by default; most other libraries use RGB. A model trained on RGB will see swapped red and blue channels if fed an OpenCV array, which is a distribution shift that is easy to miss and hard to diagnose.

:::single-choice{#layout-conversion} A PyTorch model expects NCHW but receives a batch in NHWC. Which conversion is required?

::option[Swap the first and last dimensions, then verify the batch and channel counts]{#layout-permute .correct explanation="Permuting from NHWC to NCHW reorders the axes. It must be a permutation, not a reshape, or channel values will be mixed."}
::option[Reshape the tensor to the expected number of elements]{#layout-reshape explanation="A reshape preserves memory order and would scramble the spatial structure. The operation must permute axes."}
::option[Normalise the values and the layout will resolve itself]{#layout-normalise explanation="Normalisation is independent of axis order and cannot fix a permuted tensor."}
:::

## Resolution is not detail

Two images can have the same pixel count and carry different amounts of information. A sharp 4K image of a distant bird may contain fewer resolvable features of the bird than a 1080p image taken closer. What matters is the sampling rate relative to the object, sometimes called the number of pixels on target.

This is why detection benchmarks report performance by object size. Small objects occupy few pixels, so the convolution's receptive field and the feature stride determine whether the object can be represented at all. Upsampling an image after capture does not create detail; it only interpolates.

The same logic applies to augmentation. Random cropping reduces pixels on target, and aggressive downscaling can destroy small objects entirely. A training pipeline that crops at a different scale than deployment changes what the model can see.

:::callout{type="insight" title="Information cannot be created by interpolation"}
Super-resolution networks can produce plausible detail, but they are generating, not recovering. For measurement tasks, the honest question is whether the required information was sampled at capture time.
:::

## Summary

You can now reason about an image as a sampled, quantised, channel-organised tensor rather than a picture.

1. Apply the Nyquist limit and explain why filtering must precede downsampling.
2. Relate bit depth and quantisation error to shadow detail and dynamic range.
3. Identify HWC versus CHW layouts and RGB versus BGR channel order as sources of silent failure.
4. Distinguish pixel count from resolvable detail and relate it to object scale.
