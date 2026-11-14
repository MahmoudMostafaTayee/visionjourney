---
lesson_id: "convolution-and-filtering"
course_id: "classical-processing"
lang: "en"
order_index: 1
title: "Convolution and Filtering"
description: "Linear shift-invariant operators, kernels, separability and the frequency view that explains what a filter can and cannot do."
meta_title: "Convolution and Filtering - Classical Image Processing"
meta_description: "Learn convolution, correlation, kernel design, separable Gaussian filtering, boundaries and the Fourier interpretation of image filters."
meta_keywords: "convolution, image filtering, Gaussian blur, separable filter, Fourier transform, kernel"
---

Convolution is the most reused operation in vision. Classical pipelines use it to smooth, sharpen and differentiate; convolutional networks learn its weights. The mathematics is the same in both cases: a local weighted sum, applied at every position, with weights shared across space.

## Correlation and convolution

For a discrete image $I$ and kernel $K$ of size $k \times k$, cross-correlation computes

$$(I \star K)[i,j] = \sum_{u,v} I[i+u, j+v]\, K[u,v]$$

Convolution is the same expression with the kernel flipped: $(I * K)[i,j] = \sum_{u,v} I[i-u, j-v] K[u,v]$. For symmetric kernels the two coincide, which is why the distinction is often glossed over. It matters for asymmetric kernels such as derivative filters: flipping changes the sign of the response.

Most deep-learning frameworks implement cross-correlation and call it convolution. This is harmless for learned filters, because the network can learn the flipped version, but it matters when you port hand-designed kernels or compare against a signal-processing reference.

:::single-choice{#conv-vs-corr} A framework's "conv2d" layer does not flip the kernel. What is the practical consequence?

::option[Learned filters are unaffected in principle, but hand-designed asymmetric kernels behave differently]{#flip-matters .correct explanation="A network can absorb the flip into learned weights, while a fixed derivative kernel will produce the opposite sign unless manually flipped."}
::option[The layer computes a nonlinear operation]{#flip-nonlinear explanation="Convolution and correlation are both linear; the difference is index order, not linearity."}
::option[Gradients cannot flow through the layer]{#flip-gradient explanation="Autograd handles either formulation; the difference is the forward index convention."}
:::

## Kernels as hypotheses

A kernel encodes a local pattern hypothesis. The identity kernel returns the image; a box kernel averages neighbours; a Gaussian kernel weights nearby pixels more; a Laplacian kernel responds to local curvature; a Sobel kernel responds to horizontal or vertical intensity change.

Because the operation is linear, kernels compose by convolution. Blurring twice with a Gaussian of standard deviation $\sigma_1$ and then $\sigma_2$ is equivalent to a single Gaussian with $\sqrt{\sigma_1^2 + \sigma_2^2}$. This closure property is why Gaussians are the canonical smoothing family.

Separability is the practical consequence. A 2D Gaussian is the outer product of two 1D Gaussians, so a $k \times k$ convolution can be computed as two passes of cost $O(k)$ per pixel instead of $O(k^2)$. For a $31 \times 31$ kernel the saving is roughly fifteen-fold, which is why real-time blur is feasible.

:::single-choice{#separability} A 15x15 Gaussian is separable. How many multiply-accumulates per pixel does the separable implementation require, relative to the direct 2D convolution?

::option[The same number, because the kernel has the same coefficients]{#sep-same explanation="Separability changes the factorisation of the sum, not the coefficients, so the operation count falls dramatically."}
::option[Roughly 30 instead of 225, because two 1D passes replace one 2D pass]{#sep-cheaper .correct explanation="Each pass costs about 15 multiply-accumulates, so the total is about 30 rather than 225."}
::option[About 15, because only one dimension needs filtering]{#sep-one-dim explanation="Both dimensions must be filtered; skipping one leaves the image blurred in only one direction."}
:::

:::demo{id="convolution"} Kernels and feature maps
Switch between blur, sharpen, Sobel and Laplacian kernels. The output grid is the feature map: each cell is the inner product of a 3x3 patch with the kernel. Gain and brightness expose the normalisation question.
:::

## Boundaries and normalisation

At image borders, part of the kernel falls outside the image. The choices are to zero-pad, replicate the edge, reflect, or compute only where the kernel fits (valid convolution). Each produces different border statistics, and the difference propagates through a deep network.

Zero padding introduces an artificial dark border that a learned filter may respond to. Reflection avoids that discontinuity and is the usual default in classical filtering. In networks, padding is a design parameter because it controls output size: with kernel size $k$, padding $p$ and stride $s$, the output size is

$$H' = \left\lfloor \frac{H + 2p - k}{s} \right\rfloor + 1$$

Normalisation matters as much as the kernel. A box kernel of all ones sums nine pixels, so the output is nine times brighter unless divided by nine. Derivative kernels are usually zero-sum, so a constant region produces zero response. Getting this wrong makes a filter look like a brightness change rather than an operator.

:::callout{type="warning" title="Check the DC response"}
Sum your kernel. If the sum is not zero for an edge detector, it will respond to flat regions. If the sum is not one for a smoothing kernel, it will change brightness. This single check catches most kernel bugs.
:::

## The frequency view

The Fourier transform turns convolution into pointwise multiplication: $\mathcal{F}(I * K) = \mathcal{F}(I) \cdot \mathcal{F}(K)$. A kernel is therefore a filter in the frequency domain, and its Fourier transform is its frequency response.

A Gaussian is a low-pass filter: it attenuates high frequencies and preserves low ones. A Laplacian is a high-pass filter: it suppresses the constant component and amplifies rapid change. Sharpening is unsharp masking — subtract a blurred copy, which is a high-pass operation added back to the original.

This view predicts artefacts. A sharp cutoff in frequency space produces ringing in space, which is why ideal low-pass filters create Gibbs oscillations. Smooth transitions, like the Gaussian's, avoid them. It also predicts aliasing: a filter that does not attenuate above Nyquist will fold those frequencies down when the image is resampled.

:::single-choice{#frequency-view} What does a Gaussian blur do in the frequency domain?

::option[Attenuates high frequencies while preserving low frequencies]{#gauss-lowpass .correct explanation="The Gaussian's Fourier transform is another Gaussian centred at zero frequency, so it damps high-frequency content."}
::option[Removes low frequencies and keeps edges]{#gauss-highpass explanation="That describes a high-pass or sharpening operation; blurring does the opposite."}
::option[Leaves all frequencies unchanged but shifts phase]{#gauss-phase explanation="A Gaussian is zero-phase and does attenuate amplitude; it is not an all-pass filter."}
:::

## Filters in modern pipelines

Classical filters did not disappear. Data augmentation uses Gaussian blur, sharpening and colour jitter. Industrial inspection uses deterministic edge and blob detection because its behaviour can be certified. Optical flow and stereo preprocessing use smoothing to stabilise gradients. Even in deep networks, the first layer often learns Gabor-like oriented filters, which are close relatives of the classical bank.

The deeper lesson is architectural. A convolution hard-codes locality and translation equivariance. Whether the weights are designed or learned, those constraints determine what the layer can represent and how much data it needs.

## Summary

You can now treat filtering as a linear operator with a predictable frequency response.

1. Distinguish correlation from convolution and predict the sign effect.
2. Design kernels and verify their DC response and normalisation.
3. Use separability to compute large Gaussian filters efficiently.
4. Interpret smoothing, sharpening and edge detection as frequency-domain operations.
