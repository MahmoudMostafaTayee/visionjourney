---
lesson_id: "camera-geometry-and-stereo"
course_id: "features-and-geometry"
lang: "en"
order_index: 3
title: "Camera Geometry and Stereo"
description: "Epipolar constraints, calibration, rectification, disparity and triangulation: turning two views into depth."
meta_title: "Camera Geometry and Stereo - Features, Matching and Geometry"
meta_description: "Learn epipolar geometry, the essential and fundamental matrices, stereo rectification, disparity, triangulation and structure from motion."
meta_keywords: "epipolar geometry, essential matrix, fundamental matrix, stereo rectification, disparity, triangulation, bundle adjustment"
---

A single view collapses a ray to a point. Two views of the same point constrain it to the intersection of two rays. That is the entire basis of stereo, structure from motion and visual SLAM. The geometry is exact, which is why it remains the backbone of metric 3D vision even in the deep-learning era.

## The epipolar constraint

Consider a 3D point $X$ seen from two camera centres. The point, the two centres, and the two image points lie in a plane — the epipolar plane. The projection of the first camera's centre into the second image is the epipole, and the intersection of the epipolar plane with the second image is the epipolar line.

For a point $x$ in the first image, its correspondence $x'$ in the second must lie on the corresponding epipolar line. Algebraically,

$$x'^\top F x = 0$$

where $F$ is the $3 \times 3$ fundamental matrix, rank two and defined up to scale. For calibrated cameras, $F = K'^{-\top} E K^{-1}$, where $E = [t]_\times R$ is the essential matrix. The essential matrix has five degrees of freedom: three for rotation and two for the direction of translation, since scale is unobservable from image correspondences alone.

The constraint turns a 2D search into a 1D search. Instead of matching a point against the whole second image, you search along a line, which is both faster and far less ambiguous.

:::single-choice{#epipolar-benefit} What does the epipolar constraint give a matching algorithm?

::option[A one-dimensional search line instead of a two-dimensional search region]{#epipolar-1d .correct explanation="The correspondence must lie on the epipolar line, reducing the search space and the chance of ambiguous matches."}
::option[The absolute depth of the point]{#epipolar-depth explanation="Depth requires triangulation with a known baseline or additional constraints; the epipolar line alone does not fix it."}
::option[The intrinsic calibration of both cameras]{#epipolar-intrinsics explanation="The fundamental matrix can be estimated without intrinsics; calibration is a separate step."}
:::

## Calibration and rectification

Calibration estimates the intrinsic matrix and distortion from images of a known target. The standard method, due to Zhang, uses a planar pattern observed at several orientations: homographies between the plane and the image constrain the image of the absolute conic, from which intrinsics are recovered, followed by nonlinear refinement of all parameters including distortion.

Stereo rectification then warps both images so that epipolar lines become horizontal and corresponding rows align. This is a purely geometric transformation, often combined with distortion correction. After rectification, matching reduces to a one-dimensional search along rows, which is what makes dense stereo practical.

Rectification parameters depend on the relative pose between cameras, so a stereo rig must be calibrated as a pair, not as two independent cameras. Thermal drift, vibration or a bumped mount invalidates the calibration and produces systematic depth errors that look like noise.

:::single-choice{#rectification-purpose} What is the purpose of stereo rectification?

::option[To align epipolar lines with image rows, reducing correspondence search to one dimension]{#rectify-rows .correct explanation="After rectification, a point's match lies on the same row, so dense stereo can scan horizontally."}
::option[To remove lens distortion entirely]{#rectify-distortion explanation="Distortion correction is a related but separate step; rectification is about relative camera geometry."}
::option[To increase the stereo baseline]{#rectify-baseline explanation="Baseline is a physical property of the rig and cannot be changed by warping images."}
:::

## Disparity and depth

For a rectified pair with baseline $b$ and focal length $f$, a point at depth $Z$ projects with horizontal displacement

$$d = \frac{f b}{Z}, \qquad Z = \frac{f b}{d}$$

The disparity $d$ is measured in pixels. Larger baseline or focal length increases disparity for the same depth, improving precision but reducing the overlap between views and increasing occlusions.

The sensitivity is quadratic. Differentiating gives $\partial Z / \partial d = -Z^2 / (fb)$, so depth error grows with the square of distance. At one metre, a one-pixel disparity error might correspond to a few millimetres; at ten metres, to tens of centimetres. This is why stereo is precise up close and unreliable far away, and why long-range 3D sensing often uses active illumination or time of flight instead.

:::single-choice{#stereo-sensitivity} Why does stereo depth precision degrade quadratically with distance?

::option[Because disparity is inversely proportional to depth, so a fixed pixel error maps to a depth error growing as the square]{#stereo-quadratic .correct explanation="Differentiating Z = fb/d gives dZ/dd proportional to Z squared, so the same disparity error is far larger at distance."}
::option[Because the baseline shrinks with distance]{#stereo-baseline explanation="The baseline is fixed by the rig; it does not shrink with scene distance."}
::option[Because occlusion increases the number of invalid pixels]{#stereo-occlusion explanation="Occlusions reduce coverage but do not change the derivative of depth with respect to disparity."}
:::

:::demo{id="stereo"} Baseline, depth and disparity
The diagram shows two camera centres, a scene point and the corresponding image rows. Increase the baseline and the disparity grows at fixed depth; push the point further away and the same pixel error becomes a much larger depth error.
:::

## Triangulation and structure from motion

Given matched points and known camera matrices, triangulation finds the 3D point that projects closest to both observations. The linear method stacks the two projection equations and solves a homogeneous least-squares problem; the nonlinear method minimises reprojection error directly.

Structure from motion extends this to many views. The pipeline detects and matches features across images, estimates relative poses from essential matrices, triangulates points, and then jointly refines camera poses and 3D points by minimising reprojection error — bundle adjustment. The joint refinement is what makes the reconstruction consistent; incremental estimation alone accumulates drift.

Bundle adjustment is a sparse nonlinear least-squares problem. Its sparsity comes from the fact that each 3D point is observed by only a few cameras, which allows efficient elimination of the point parameters and a reduced camera system. This structure is why large reconstructions are tractable.

Visual SLAM adds a temporal constraint: the camera moves continuously, so poses are estimated incrementally and the map is maintained online. Modern systems combine classical geometry with learned features, learned depth priors and, increasingly, neural scene representations.

:::single-choice{#bundle-adjustment} What does bundle adjustment optimise?

::option[Camera poses and 3D point positions jointly, minimising reprojection error]{#ba-joint .correct explanation="It refines both sets of parameters together so that the projected model agrees with all observed image points."}
::option[Only the intrinsic calibration]{#ba-intrinsics explanation="Intrinsics may be included, but the core variables are poses and structure."}
::option[The descriptor matching thresholds]{#ba-descriptors explanation="Bundle adjustment operates on geometric residuals after correspondences are established."}
:::

## Where learned methods fit

Learned stereo networks predict disparity directly from rectified pairs, and they outperform classical block matching on textureless regions and repetitive patterns by using learned priors. Monocular depth networks predict depth from a single image, which is fundamentally ambiguous but statistically constrained by scene regularities.

These methods do not replace geometry. They produce depth maps that still need geometric consistency checks, and they are often trained with photometric or reprojection losses derived from the same epipolar geometry. A robust system combines a learned prior with a geometric verifier: the network proposes, and the geometry disposes.

:::callout{type="insight" title="Scale is the recurring ambiguity"}
Monocular structure from motion recovers geometry only up to an unknown scale. A stereo rig fixes scale through its baseline. An IMU fixes it through acceleration. A learned depth model fixes it through training data statistics. Every 3D system must answer: what sets the scale, and how is it validated?
:::

## Summary

You can now connect correspondences across views into metric 3D structure.

1. State and use the epipolar constraint and distinguish the essential and fundamental matrices.
2. Calibrate a camera and rectify a stereo pair.
3. Convert disparity to depth and explain the quadratic error growth.
4. Triangulate points and describe bundle adjustment's joint optimisation.
