---
lesson_id: "matching-and-ransac"
course_id: "features-and-geometry"
lang: "en"
order_index: 2
title: "Matching and Robust Estimation"
description: "Nearest-neighbour matching, the ratio test, RANSAC and the linear algorithms for homographies and fundamental matrices."
meta_title: "Matching and Robust Estimation - Features, Matching and Geometry"
meta_description: "Learn feature matching, Lowe's ratio test, RANSAC, homography estimation with DLT and the eight-point algorithm for epipolar geometry."
meta_keywords: "feature matching, ratio test, RANSAC, homography, DLT, eight-point algorithm, fundamental matrix"
---

Two sets of keypoints are useless until they are paired. Matching produces candidate correspondences, most of which are wrong. Robust estimation finds the geometric model that the correct correspondences satisfy, and rejects the rest.

## Nearest-neighbour matching

The simplest matcher compares descriptors and keeps the nearest neighbour in the other image. With $N$ and $M$ descriptors, brute force costs $O(NM)$, which is acceptable for hundreds of features and prohibitive for millions. Approximate nearest-neighbour structures such as k-d trees and hierarchical navigable small-world graphs reduce the search cost at the price of small recall loss.

For binary descriptors, Hamming distance replaces Euclidean distance and is computed with population counts, which is extremely fast. For float descriptors, the inner product on normalised vectors is equivalent to cosine similarity and can be computed as a single matrix multiply, which is what GPU matchers do.

Mutual nearest-neighbour matching — keeping a pair only if each is the other's nearest neighbour — removes many ambiguous matches cheaply. It is a good default when the overlap is large.

:::single-choice{#ratio-test} Lowe's ratio test keeps a match only when the nearest neighbour is significantly closer than the second nearest. What failure mode does it target?

::option[Ambiguous matches in repetitive texture, where several descriptors are nearly equally good]{#ratio-ambiguous .correct explanation="If the second-best match is almost as close, the descriptor cannot distinguish the candidates, so the match is unreliable."}
::option[Matches that are geometrically impossible under a homography]{#ratio-geometry explanation="Geometry is enforced later by RANSAC; the ratio test is a descriptor-level confidence filter."}
::option[Matches with large pixel displacement]{#ratio-displacement explanation="Displacement is not directly considered by the ratio test, which compares descriptor distances."}
:::

## From matches to a model

A homography is a projective transformation of the plane, represented by a $3 \times 3$ matrix defined up to scale, so it has eight degrees of freedom. Each correspondence provides two linear equations. Four correspondences therefore determine a homography, and the direct linear transform stacks the equations into a matrix and solves for the null vector by SVD.

The eight-point algorithm does the same for the fundamental matrix, which encodes epipolar geometry between two uncalibrated views: each correspondence adds one linear constraint, and eight are sufficient. The raw solution is poorly conditioned, so Hartley's normalisation — translate the points to zero mean and scale so the average distance is $\sqrt{2}$ — is essential in practice. The result is refined by enforcing the rank-two constraint and then by nonlinear minimisation of the epipolar error.

These minimal solvers are the building blocks of robust estimation. They are fast but extremely sensitive to outliers, which is why they are used inside a sampling loop rather than on all matches at once.

:::single-choice{#homography-dof} How many point correspondences are minimally required to determine a homography?

::option[Two, because each point has two coordinates]{#homography-two explanation="Two points give four equations, fewer than the eight degrees of freedom of a homography."}
::option[Four, because each correspondence gives two independent equations]{#homography-four .correct explanation="A homography has eight degrees of freedom (nine entries minus scale), and four correspondences supply eight equations."}
::option[Eight, because the transform has nine entries]{#homography-eight explanation="Eight correspondences are the minimal set for the fundamental matrix, not the homography."}
:::

## RANSAC

RANSAC alternates between hypothesising a model from a minimal sample and counting how many matches agree with it. The steps are:

1. Sample the minimal number of correspondences.
2. Fit the model.
3. Count inliers whose residual is below a threshold.
4. Keep the model with the most inliers; refit on all inliers.

The probability that a sample is outlier-free is $p^k$, where $p$ is the inlier ratio and $k$ the sample size. The number of iterations needed to succeed with probability $\eta$ is

$$N = \frac{\log(1-\eta)}{\log(1-p^k)}$$

This formula explains why minimal solvers matter. Doubling the sample size from four to eight squares the outlier rejection burden: with a 50 percent inlier ratio, four-point RANSAC needs about 35 iterations for 99 percent confidence, while eight-point needs about 1,177.

:::single-choice{#ransac-iterations} Why does RANSAC's required iteration count grow so quickly with model complexity?

::option[Because the probability of drawing an all-inlier minimal sample falls exponentially with sample size]{#ransac-exponential .correct explanation="The success probability per sample is p to the power k, so larger minimal sets require far more iterations to reach the same confidence."}
::option[Because complex models are slower to fit]{#ransac-speed explanation="Fit time matters for runtime but not for the iteration count needed for a given confidence."}
::option[Because inlier thresholds must be larger for complex models]{#ransac-threshold explanation="Threshold choice affects inlier counts, but the exponential dependence on k is the dominant scaling."}
:::

## Thresholds and refinement

The inlier threshold is a modelling choice measured in pixels or in a geometric residual. Too tight and true correspondences are rejected; too loose and outliers contaminate the fit. A common approach is to set it from the measured reprojection noise, often around one or two pixels.

RANSAC returns a model, not an uncertainty. A complete pipeline refits the model on all inliers with a nonlinear least-squares solver, then reports the residual distribution and the number of inliers. A homography supported by twenty inliers with sub-pixel residuals is a much stronger claim than one supported by five with three-pixel residuals, even if both are "successful".

Degenerate configurations are another failure mode. Points on a line cannot determine a homography; points on a plane make the fundamental matrix non-unique. Detecting degeneracy requires checking the conditioning of the design matrix or comparing model hypotheses.

:::callout{type="warning" title="Inlier count is not proof"}
A model with many inliers can still be wrong if the inliers are concentrated in a small region or lie on a degenerate configuration. Visualise the inlier distribution and the residual map before trusting the estimate.
:::

## Summary

You can now build a correspondence pipeline and quantify its reliability.

1. Apply nearest-neighbour and ratio-test matching, including mutual matching.
2. Explain the degrees of freedom of a homography and the eight-point algorithm.
3. Compute the RANSAC iteration count from the inlier ratio and sample size.
4. Refit inliers and check for degenerate configurations.
