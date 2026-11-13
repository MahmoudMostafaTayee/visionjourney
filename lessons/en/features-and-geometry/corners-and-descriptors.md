---
lesson_id: "corners-and-descriptors"
course_id: "features-and-geometry"
lang: "en"
order_index: 1
title: "Corners and Descriptors"
description: "The second-moment matrix, Harris and FAST detectors, and how SIFT builds scale-invariant descriptors from image structure."
meta_title: "Corners and Descriptors - Features, Matching and Geometry"
meta_description: "Learn Harris corner detection, FAST, scale-space, SIFT keypoints and descriptors, and the design of rotation-invariant features."
meta_keywords: "Harris corner detector, second moment matrix, FAST, SIFT, scale space, local descriptor"
---

A feature is a measurement that can be found again. Matching two images requires points whose neighbourhoods are distinctive and whose coordinates can be recovered despite translation, rotation, scale and illumination change. The classical answer is the corner detector plus the descriptor.

## Why corners

Consider a small window sliding over an image. In a flat region, moving it changes nothing. Along an edge, moving perpendicular changes the content but moving along the edge does not. At a corner, moving in any direction changes the content. Corners are therefore locally unambiguous in two dimensions.

Harris and Stephens formalised this with the second-moment matrix of image gradients over a window:

$$M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$$

The eigenvalues of $M$ describe how the window responds to displacement: both large means a corner, one large means an edge, both small means flat. Rather than compute eigenvalues, Harris uses the response

$$R = \det(M) - k\,\operatorname{tr}(M)^2$$

with $k$ typically between 0.04 and 0.06. The determinant is the product of eigenvalues and the trace is their sum, so the expression is large only when both are large.

:::single-choice{#harris-eigen} In the Harris second-moment matrix, what does it mean when both eigenvalues are large?

::option[The window content changes under displacement in every direction, indicating a corner]{#harris-corner .correct explanation="Large curvature in both principal directions means no small translation leaves the patch unchanged, which is the corner condition."}
::option[The window lies on a straight edge]{#harris-edge explanation="An edge has one large and one small eigenvalue: moving along the edge preserves the patch."}
::option[The window is flat and untextured]{#harris-flat explanation="A flat patch has both eigenvalues near zero."}
:::

## Detectors in practice

Harris is rotation-invariant but not scale-invariant: a corner detected at one resolution may disappear at another. Shi and Tomasi proposed using the smaller eigenvalue directly, which gives better tracking stability. FAST (Features from Accelerated Segment Test) compares a circle of pixels around a candidate and tests whether a contiguous arc is brighter or darker, which is extremely fast and became the default in real-time SLAM such as ORB-SLAM.

Detectors produce many overlapping responses, so the pipeline applies non-maximum suppression and often a spatial distribution constraint to avoid clustering all keypoints in one textured area. The number and spread of keypoints matter more than raw repeatability for downstream pose estimation.

:::single-choice{#fast-tradeoff} FAST is widely used in real-time systems. What does it sacrifice for speed?

::option[Repeatability under large scale change and robustness to noise, which later stages must compensate for]{#fast-tradeoff .correct explanation="FAST is a fast intensity test without scale-space or orientation reasoning, so it needs pyramids and descriptor-level robustness."}
::option[The ability to run on binary images]{#fast-binary explanation="FAST compares intensities and works on grayscale; binary operation is not the trade-off."}
::option[Rotation invariance of the detector response]{#fast-rotation explanation="FAST itself is not rotation-invariant, but the main speed trade-off is its lack of scale reasoning; orientation is added by descriptor stages."}
:::

## Scale space

An object's appearance depends on the distance and the resolution. To match across scales, features must be detected at a characteristic scale. Scale-space theory smooths the image with Gaussians of increasing $\sigma$ and analyses the differences.

The difference-of-Gaussians approximates the scale-normalised Laplacian, and its extrema across both space and scale mark blob-like structures. SIFT finds keypoints as extrema in a DoG pyramid, then refines their position and scale by fitting a quadratic to the local samples. Points with low contrast or strong edge response are rejected, because they are unstable under noise.

The result is a set of keypoints each with a location, a scale and, after orientation assignment, a canonical rotation. Assigning orientation from a histogram of gradient directions makes the descriptor rotation-invariant: the patch is described relative to the dominant gradient direction.

:::single-choice{#sift-scale} Why does SIFT detect keypoints in a scale-space pyramid rather than at a single resolution?

::option[So the same physical feature can be found at different distances and image resolutions]{#sift-pyramid .correct explanation="Scale-space extrema provide a characteristic scale, letting the descriptor normalise size and match across zoom changes."}
::option[To increase the number of keypoints for matching]{#sift-count explanation="The pyramid may produce more candidates, but its purpose is invariance to scale, not volume."}
::option[To remove the need for orientation assignment]{#sift-orientation explanation="Orientation assignment remains necessary and is a separate stage."}
:::

## The descriptor

A descriptor converts a local patch into a vector that is distinctive and stable. SIFT divides the patch into a 4x4 grid of cells, computes an 8-bin gradient orientation histogram in each, and normalises the resulting 128-dimensional vector. Normalisation reduces sensitivity to illumination gain, and clipping large values reduces sensitivity to saturation.

The design choices matter. Gradients are computed after smoothing, which suppresses noise. Orientation bins are interpolated, which makes the descriptor tolerant to small rotation errors. The spatial grid provides some robustness to local deformation, because each cell summarises a region rather than an exact pixel pattern.

ORB replaces the expensive SIFT descriptor with a binary string: BRIEF samples pairs of pixels and compares their intensities, producing a compact code compared by Hamming distance. Orientation is added by rotating the sampling pattern, and the result is fast enough for real-time tracking on CPUs. Binary descriptors trade some distinctiveness for speed and memory.

:::single-choice{#descriptor-normalisation} Why does SIFT normalise its descriptor vector and clip large components?

::option[To reduce sensitivity to illumination changes and to prevent a few strong gradients from dominating]{#sift-normalise .correct explanation="Global scaling is removed by normalisation, and clipping limits the influence of saturated or high-contrast gradients."}
::option[To make the descriptor rotation-invariant]{#sift-rotation explanation="Rotation invariance comes from orienting the patch before description, not from vector normalisation."}
::option[To reduce the descriptor to 128 bits]{#sift-bits explanation="SIFT is a 128-dimensional float vector; normalisation does not change its dimensionality or type."}
:::

## Learned local features

Modern detectors and descriptors are learned. SuperPoint trains a detector and descriptor jointly with homographic self-supervision; SuperGlue learns to match sets of keypoints with attention; LoFTR performs dense matching without detecting keypoints at all.

The classical concepts persist. Scale-space becomes multi-scale feature pyramids; orientation assignment becomes learned equivariance or augmentation; descriptor normalisation becomes contrastive training with hard negatives. What changed is that the invariance is learned from data rather than designed.

:::callout{type="insight" title="Repeatability is the metric"}
A detector is only as good as its repeatability: the fraction of keypoints found again under a transform. A descriptor is only as good as its matching precision at a given recall. Evaluate both separately before combining them.
:::

## Summary

You can now explain how classical features achieve invariance and what they trade away.

1. Derive the Harris response from the second-moment matrix.
2. Compare Harris, Shi-Tomasi and FAST in terms of invariance and speed.
3. Explain how scale-space extrema and orientation assignment produce SIFT keypoints.
4. Describe descriptor normalisation and the binary-descriptor alternative.
