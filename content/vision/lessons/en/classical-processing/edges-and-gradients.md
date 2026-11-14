---
lesson_id: "edges-and-gradients"
course_id: "classical-processing"
lang: "en"
order_index: 2
title: "Edges and Gradients"
description: "From the image gradient to Canny's four stages and the Laplacian-of-Gaussian, with the design criteria that make edges useful."
meta_title: "Edges and Gradients - Classical Image Processing"
meta_description: "Derive image gradients, Sobel and Laplacian operators, non-maximum suppression and the full Canny edge detection pipeline."
meta_keywords: "image gradient, Sobel, Laplacian of Gaussian, Canny edge detection, non-maximum suppression, hysteresis"
---

An edge is a place where intensity changes rapidly. That definition hides a chain of choices: how to differentiate a discrete image, how to decide which responses are meaningful, and how to turn a thick band of high gradient into a thin, connected curve.

## Differentiating a discrete image

The derivative of a continuous signal is a limit; a digital image has no such limit. The simplest approximation is a forward difference, $I(x+1) - I(x)$. Central differences are more accurate and symmetric:

$$\frac{\partial I}{\partial x} \approx \frac{I(x+1) - I(x-1)}{2}$$

Derivatives amplify noise, because noise is high-frequency by nature. The standard remedy is to smooth first, then differentiate. Since both are linear and shift-invariant, they compose into a single derivative-of-Gaussian kernel: smooth with $G_\sigma$, then take the gradient, or equivalently convolve with $\nabla G_\sigma$.

Sobel kernels approximate a smoothed derivative with a 3x3 stencil. The horizontal kernel is

$$\begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

which is a central difference in $x$ combined with a triangular smoothing in $y$. Prewitt uses uniform smoothing instead. Scharr optimises the coefficients for rotational symmetry. All are approximations to the same ideal operator.

:::single-choice{#smooth-before-differentiate} Why is smoothing applied before computing an image derivative?

::option[Because differentiation amplifies high-frequency noise, and smoothing attenuates it first]{#smooth-noise .correct explanation="A derivative has a high-pass response, so noise is amplified. Pre-smoothing with a low-pass kernel reduces that amplification."}
::option[Because smoothing increases the edge contrast]{#smooth-contrast explanation="Smoothing reduces contrast and widens edges; its purpose is noise suppression, not enhancement."}
::option[Because the derivative is undefined on discrete grids]{#smooth-discrete explanation="Discrete approximations exist; smoothing improves their signal-to-noise ratio rather than making them defined."}
:::

## Gradient magnitude and direction

For an image $I$, the gradient $\nabla I = (I_x, I_y)$ points in the direction of steepest increase. Its magnitude $\lVert \nabla I \rVert = \sqrt{I_x^2 + I_y^2}$ measures edge strength, and its direction $\theta = \operatorname{atan2}(I_y, I_x)$ is perpendicular to the edge orientation.

A common approximation replaces the square root with $|I_x| + |I_y|$ for speed. This changes the level sets from circles to diamonds, which mildly rotates the response, but it is often acceptable in embedded systems.

The gradient is not a segmentation. A textured region produces many strong gradients that are not object boundaries; a soft shadow produces a smooth ramp with weak gradient. This is why edge detection alone is a weak cue, and why classical systems combined it with region, colour and motion cues.

:::single-choice{#gradient-direction} If the image gradient at a pixel points horizontally, how is the edge oriented there?

::option[Vertically, perpendicular to the gradient]{#edge-perp .correct explanation="The gradient points across the edge, in the direction of maximal intensity change, so the edge itself runs perpendicular to it."}
::option[Horizontally, along the gradient]{#edge-parallel explanation="Along the gradient the intensity changes fastest, which crosses the edge rather than following it."}
::option[The orientation cannot be determined from the gradient]{#edge-unknown explanation="The gradient direction gives the edge normal directly, up to a sign."}
:::

:::demo{id="edges"} Threshold, operator and edge density
Sobel magnitude, Laplacian and Prewitt respond differently to the same scene. Lower the threshold and watch noise enter as spurious edges; raise it and thin structures disappear.
:::

## The Laplacian and its instability

The Laplacian $\nabla^2 I = I_{xx} + I_{yy}$ measures the divergence of the gradient. It is isotropic, which is attractive, but it is a second derivative and therefore even more noise-sensitive than a first derivative. Applied directly to a noisy image it produces mostly noise.

The Laplacian-of-Gaussian fixes this by smoothing first. Because convolution commutes, the LoG is a single kernel that is both a smoothed second derivative and a band-pass filter. Its response crosses zero at the edge centre, so edges are located by finding zero crossings rather than maxima. Marr and Hildreth built their edge theory on exactly this construction.

Zero crossings are appealing because they are thin by construction, but they can form closed contours that do not correspond to object boundaries. The LoG remains useful as a blob detector: at the scale matching a blob's size, the response is extremal, which is the basis of scale-space blob detection.

:::single-choice{#log-zero-crossing} Why does the Laplacian-of-Gaussian locate edges at zero crossings rather than at maxima of response?

::option[Because a second derivative changes sign across the edge centre]{#log-sign .correct explanation="The smoothed intensity profile has an inflection at the edge, where its second derivative passes through zero."}
::option[Because the Gaussian removes the edge entirely]{#log-removed explanation="The smoothed edge remains, with a finite width set by the Gaussian scale."}
::option[Because zero crossings are easier to threshold than maxima]{#log-easier explanation="The location is determined by the sign change of the second derivative, not by computational convenience."}
:::

## Canny's design criteria

Canny (1986) framed edge detection as an optimisation problem with three criteria: good detection (low false positive and false negative rate), good localisation (detected edges close to true edges), and a single response per edge. From these he derived an optimal 1D operator and then a practical 2D algorithm.

The practical pipeline has four stages:

1. **Smooth** with a Gaussian to suppress noise.
2. **Compute gradient** magnitude and direction with Sobel or a similar operator.
3. **Non-maximum suppression** — keep only pixels that are local maxima along the gradient direction, producing a thin edge map.
4. **Hysteresis thresholding** — start from strong edges above a high threshold, then grow along weak edges above a low threshold that are connected to strong ones.

The two thresholds are the important engineering detail. A single threshold either misses weak but real edges or admits noise. Hysteresis uses connectivity as evidence: a weak edge connected to a strong edge is likely real.

:::single-choice{#canny-hysteresis} What is the purpose of Canny's two-threshold hysteresis step?

::option[It keeps weak edges only when they are connected to strong ones, using connectivity as evidence]{#hysteresis-link .correct explanation="Strong edges seed the result; weak edges survive if they extend a strong contour, which suppresses isolated noise responses."}
::option[It applies the high threshold to the image centre and the low threshold to borders]{#hysteresis-spatial explanation="The thresholds are not spatially partitioned; the distinction is edge strength and connectivity."}
::option[It removes all weak edges regardless of context]{#hysteresis-remove explanation="That would be single-threshold behaviour and would break contours at weak sections."}
:::

## What edges are good for

Despite their limitations, edges remain a compact and interpretable representation. They support line and vanishing-point detection for geometric calibration, contour tracking, document scanning, industrial metrology and texture analysis. In deep pipelines, edge maps are used as auxiliary supervision, as input channels, and as a diagnostic for whether a model is relying on shape or texture.

The limitation is fundamental: an edge marks an intensity discontinuity, not a semantic boundary. Distinguishing an object outline from a shadow, a texture boundary or a painted stripe requires context. That is precisely the gap that learned representations were built to close.

## Summary

You can now implement and justify a complete edge detector.

1. Approximate derivatives on a discrete grid and explain why smoothing precedes them.
2. Relate gradient magnitude and direction to edge strength and orientation.
3. Explain the noise instability of the Laplacian and the role of the LoG.
4. Implement Canny's four stages and justify hysteresis thresholding.
