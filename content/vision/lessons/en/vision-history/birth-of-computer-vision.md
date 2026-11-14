---
lesson_id: "birth-of-computer-vision"
course_id: "vision-history"
lang: "en"
order_index: 2
title: "The Birth of Computer Vision"
description: "From Roberts' edge detector and the MIT Summer Vision Project to Marr's levels of analysis and the feature-engineering era."
meta_title: "The Birth of Computer Vision - Vision History"
meta_description: "Trace early computer vision: Roberts' blocks world, the MIT Summer Vision Project, Marr's computational theory, and the SIFT and HOG era."
meta_keywords: "computer vision history, Larry Roberts, MIT Summer Vision Project, David Marr, SIFT, HOG, Viola-Jones"
---

The first computer vision systems were built by people who believed the problem was mostly bookkeeping. Attach a camera to a computer, and the computer should describe what it sees. That optimism lasted about a decade, and its failure defined the research agenda for the next forty years.

## Blocks, edges and impossible optimism

In 1963 Larry Roberts published *Machine Perception of Three-Dimensional Solids*, generally treated as the first computer vision paper. His system detected edges in photographs of polyhedra, found lines and vertices, and matched them to wireframe models to recover three-dimensional structure. It worked because the world was constrained: clean edges, simple geometry, controlled lighting.

The 1966 MIT Summer Vision Project, associated with Seymour Papert and Marvin Minsky, proposed to solve visual object recognition in a single summer by assigning it to a handful of students. The proposal is a useful artefact because it makes the field's original assumptions explicit: that vision is a pipeline of separable subproblems, and that each subproblem is small.

Neither assumption held. Segmentation turned out to depend on recognition, recognition on context, and context on a model of the world. The summer project produced components that later mattered, but not a solution.

:::single-choice{#summer-project-assumption} What assumption most directly caused the MIT Summer Vision Project to underestimate the difficulty?

::option[That cameras would remain too expensive to use]{#camera-cost explanation="Cost was not the bottleneck; the project had cameras and students. The difficulty was conceptual."}
::option[That vision decomposes into independent subproblems each solvable in isolation]{#independence-assumption .correct explanation="Segmentation, recognition and 3D inference are mutually constraining. Treating them as a one-way pipeline hid the circular dependencies that make vision hard."}
::option[That computers lacked enough memory to store images]{#memory-assumption explanation="Memory limits were real but secondary. The failure was in the problem decomposition, not storage capacity."}
:::

## Marr's framework

David Marr's *Vision* (1982) gave the field its most durable conceptual structure. He distinguished three levels of analysis:

- **Computational theory** — what problem is being solved, and why is the solution correct?
- **Representation and algorithm** — which data structures and procedures implement it?
- **Implementation** — how is it realised in hardware?

Marr argued that edge detection should be studied as a computational problem with a stated goal, not as an ad hoc filter. His collaboration with Ellen Hildreth produced the Laplacian-of-Gaussian edge detector, and his primal sketch proposed an explicit representation of intensity changes, edges, bars and blobs at multiple scales.

Marr also formalised vision as *inverse optics*: the image is the result of a forward physical process, and vision must invert it. The inversion is ill-posed — many scenes produce the same image — so the solver must add constraints. That framing is still how you justify priors, regularisation and generative models.

:::single-choice{#marr-levels} A paper proposes a new loss function justified by the statistics of natural images. Which of Marr's levels is that primarily?

::option[Implementation, because a loss is code]{#loss-implementation explanation="The level concerns why the objective is the right one for the problem, not how it is executed on hardware."}
::option[Computational theory, because it states what makes a solution correct given the structure of the problem]{#loss-theory .correct explanation="Justifying an objective from image statistics is a claim about the computational problem and its constraints, which is Marr's top level."}
::option[Representation and algorithm, because losses define data structures]{#loss-representation explanation="A loss does not by itself specify the representation; the argument from natural-image statistics is about the problem's constraints."}
:::

## The feature-engineering era

From the late 1980s to roughly 2011, the dominant paradigm was a hand-designed pipeline: detect interest points, describe them, match or classify, and impose geometric consistency. Each stage was a research programme.

Lucas and Kanade (1981) introduced optical flow by local least squares. Canny (1986) derived an optimal edge detector from three explicit criteria. Harris and Stephens (1988) built a corner detector from the second-moment matrix. Lowe's SIFT (1999, extended 2004) combined scale-space extrema, orientation histograms and descriptor normalisation into an object-matching system that was remarkably robust.

For recognition, the pipeline ended in a classifier trained on engineered descriptors. Viola and Jones (2001) achieved real-time face detection with Haar-like features, integral images and cascaded classifiers. Dalal and Triggs (2005) showed that histogram-of-oriented-gradients descriptors plus a linear SVM were excellent for pedestrian detection. By 2010, the state of the art on many benchmarks was a combination of SIFT, Fisher vectors or HOG, and a linear model.

The pipeline was interpretable and data-efficient, but every stage was designed by hand and tuned separately. Errors compounded, and the features did not adapt to new domains.

:::single-choice{#feature-pipeline} In the pre-deep-learning pipeline, what was the role of the classifier?

::option[It discovered the features directly from raw pixels]{#classifier-discovers explanation="Features were engineered by hand. The classifier operated on descriptors produced by that fixed pipeline."}
::option[It mapped hand-designed descriptors to labels, with limited ability to improve the representation]{#classifier-maps .correct explanation="The classifier learned a decision boundary over fixed descriptors, so its ceiling was set by the quality of the hand-designed features."}
::option[It performed the camera calibration]{#classifier-calibration explanation="Calibration is a geometric estimation step, separate from the recognition classifier."}
:::

## Why the era ended

Two pressures built up. First, benchmarks grew: Caltech-101, then Pascal VOC in 2005, then ImageNet in 2009. Larger and more varied data punished features that were tuned to a narrow domain. Second, graphics processors became programmable, making large matrix computations cheap.

The feature era did not fail because its ideas were wrong. Scale-space, orientation histograms, robust estimation and geometric verification all survived inside deep systems. It failed because the representation was no longer the bottleneck once data and compute were abundant.

:::callout{type="warning" title="A caution about 'solved'"}
Every era has declared vision nearly solved. Roberts' blocks world looked complete for polyhedra; the feature pipeline looked complete for VOC; deep classifiers looked complete for ImageNet. Each victory was real but bounded. Ask always: solved on which distribution, under which assumptions?
:::

## Summary

You can now explain how the first generation of vision systems framed the problem and why that framing changed.

1. Describe Roberts' blocks-world system and its constraints.
2. Explain why the Summer Vision Project's decomposition failed.
3. Apply Marr's three levels of analysis to a research claim.
4. Identify the stages of the classical feature pipeline and their limitations.
