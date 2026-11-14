---
lesson_id: "nerf-and-3d-vision"
course_id: "generative-and-3d"
lang: "en"
order_index: 3
title: "Neural Fields and 3D Vision"
description: "Depth, point clouds, NeRF volume rendering, Gaussian splatting and the representations competing for the 3D stack."
meta_title: "Neural Fields and 3D Vision - Generative and 3D Vision"
meta_description: "Learn depth estimation, point clouds, NeRF volume rendering, Gaussian splatting, multi-view geometry and 3D generative models."
meta_keywords: "NeRF, neural radiance field, Gaussian splatting, depth estimation, point cloud, novel view synthesis, 3D reconstruction"
---

Images are projections; the world is three-dimensional. Recovering that third dimension from images is the oldest problem in vision, and the modern answers range from explicit geometry to neural fields that store a scene as a function.

## Depth representations

A depth map stores the distance from the camera to the visible surface at each pixel. It is a 2.5D representation: complete from one viewpoint, empty behind occlusions. Monocular depth estimation predicts it from a single image, which is fundamentally ambiguous in scale, so models learn statistical priors from training data.

Stereo and multi-view methods compute depth from geometric consistency. They require calibrated cameras and sufficient texture, but they provide metric scale and verifiable estimates. Learned stereo improves on classical block matching by using learned features and regularisation.

A point cloud is an unordered set of 3D points, often with colour or normals. It is the natural output of LiDAR and structure from motion. Processing point clouds requires permutation-invariant architectures such as PointNet, or voxelisation that reintroduces grid structure.

A mesh represents surfaces with vertices and faces. It is compact and renderable, but recovering a mesh from images requires solving topology, which is harder than predicting depth or occupancy.

:::single-choice{#depth-ambiguity} Why is monocular depth estimation fundamentally ambiguous?

::option[Because a single view does not determine scale and many 3D scenes project to the same image]{#mono-ambiguity .correct explanation="The projection loses depth, so an object twice as far and twice as large can produce the same image."}
::option[Because cameras cannot measure depth at all]{#no-depth explanation="Cameras measure light, but depth can be inferred from cues; the issue is ambiguity, not impossibility."}
::option[Because depth maps are quantised]{#depth-quantisation explanation="Quantisation limits precision but does not create the fundamental scale ambiguity."}
:::

## Neural radiance fields

NeRF represents a scene as a continuous function $F_\theta(x, y, z, \theta, \phi) \to (c, \sigma)$: given a 3D position and viewing direction, it returns colour and volume density. To render a pixel, a ray is cast through the scene, sampled at points, and the colours are integrated with the densities along the ray.

The rendering integral is approximated by quadrature:

$$\hat{C}(r) = \sum_{i=1}^{N} T_i \left(1 - e^{-\sigma_i \delta_i}\right) c_i, \qquad T_i = \exp\left(-\sum_{j<i}\sigma_j \delta_j\right)$$

The model is trained by minimising the difference between rendered and observed pixel colours across many views. Positional encoding of the input coordinates is essential, because a plain MLP struggles to represent high-frequency detail.

NeRF produces impressive novel view synthesis, but training and rendering are slow. Follow-up work reduced the cost with hash-grid encodings, factored representations and sparse voxel structures. The core idea — a differentiable rendering loss over a continuous scene function — remains.

:::single-choice{#nerf-rendering} How is a pixel colour produced in NeRF?

::option[By integrating colour and density samples along a camera ray]{#nerf-integral .correct explanation="Volume rendering accumulates transmittance-weighted colour contributions along the ray, which makes the process differentiable with respect to the scene function."}
::option[By rasterising triangles into the image plane]{#nerf-raster explanation="That describes mesh rasterisation; NeRF is a volumetric, ray-based representation."}
::option[By classifying a fixed grid of voxels]{#nerf-voxel explanation="Some variants use voxel grids for acceleration, but the rendering is still volumetric integration along rays."}
:::

## Gaussian splatting

3D Gaussian splatting represents a scene as a set of anisotropic 3D Gaussians, each with a position, covariance, opacity and colour (often expressed as spherical harmonics). Rendering projects the Gaussians onto the image plane and composites them in depth order.

The representation is explicit, which makes rendering extremely fast and allows real-time novel view synthesis. It is also editable: individual Gaussians can be moved, removed or recoloured. Training optimises the Gaussian parameters and adaptively densifies or prunes them to fit the scene.

The trade-off is memory and the need for good initialisation, usually from structure from motion. Unlike a neural field, the representation does not interpolate smoothly everywhere, which can produce artefacts at thin structures or in unobserved regions.

The competition between implicit neural fields and explicit primitives is a recurring pattern in graphics and vision. Implicit representations are compact and smooth; explicit ones are fast and editable. The right choice depends on whether the application needs rendering speed, editing or compact storage.

:::single-choice{#splatting-speed} Why is Gaussian splatting faster to render than a vanilla NeRF?

::option[Because it rasterises explicit primitives rather than integrating a network along every ray]{#splat-speed .correct explanation="Projection and compositing of Gaussians avoid many network evaluations per pixel, which is the dominant cost in NeRF."}
::option[Because it uses fewer training images]{#splat-data explanation="Data requirements are a training property; the speed advantage is in rendering."}
::option[Because it does not need camera poses]{#splat-poses explanation="Most splatting pipelines rely on poses from structure from motion, although pose-free variants exist."}
:::

## Multi-view geometry and poses

Both NeRF and splatting require camera poses, typically obtained from structure from motion. The pipeline detects features, matches them, estimates relative poses, triangulates points and refines everything with bundle adjustment.

Pose accuracy directly limits reconstruction quality. A small pose error produces blurry or ghosted renderings, because the model cannot reconcile inconsistent projections. This is why datasets such as those captured with a calibrated rig or with COLMAP preprocessing are standard.

Joint pose and scene optimisation is possible but harder: the optimisation landscape has many local minima. Recent work uses learned priors, depth supervision or inertial data to stabilise it.

## 3D generation

Generative 3D models produce objects or scenes from text, images or a single view. Approaches include:

- **Feed-forward** models that regress a representation such as a triplane, mesh or Gaussians from an image.
- **Score distillation** methods that optimise a 3D representation so its renderings score well under a pretrained 2D diffusion model.
- **Multi-view diffusion** that generates consistent views and then reconstructs geometry from them.

Each approach inherits assumptions. Score distillation can produce plausible views that are geometrically inconsistent; multi-view diffusion depends on the consistency of the generated views; feed-forward models are limited by the diversity of their training data.

:::callout{type="warning" title="Rendering is not measurement"}
A photorealistic novel view can be generated from an inconsistent or incomplete reconstruction. For engineering, medical or forensic use, validate geometry against independent measurements, not only against rendered appearance.
:::

## Summary

You can now compare the main 3D representations and their costs.

1. Explain depth ambiguity and the difference between monocular and geometric depth.
2. Write the NeRF rendering integral and explain positional encoding.
3. Describe Gaussian splatting and why it renders quickly.
4. Explain why camera poses and multi-view geometry remain essential.
5. Compare feed-forward, distillation and multi-view approaches to 3D generation.
