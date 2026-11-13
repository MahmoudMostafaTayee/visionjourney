---
lesson_id: "pinhole-and-projection"
course_id: "image-formation"
lang: "en"
order_index: 1
title: "Pinhole and Projection"
description: "Derive the camera projection, the thin-lens model, field of view and the geometry that every calibration routine inverts."
meta_title: "Pinhole and Projection - Image Formation"
meta_description: "Derive perspective projection, focal length, field of view, thin-lens focus and lens distortion in the camera model."
meta_keywords: "pinhole camera model, perspective projection, focal length, field of view, thin lens, lens distortion"
---

An image is a set of measurements of light arriving from a scene. Before anything can interpret those measurements, we need a model of how a point in the world maps to a point on the sensor. That model is the camera projection, and almost every geometric algorithm in vision depends on it.

## The pinhole model

Place a barrier with a tiny hole between the scene and a sensor plane at distance $f$. A world point $(X, Y, Z)$ emits rays in all directions; only the ray passing through the hole reaches the sensor. By similar triangles, it lands at

$$x = f\frac{X}{Z}, \qquad y = f\frac{Y}{Z}$$

with the image inverted relative to the scene. We usually absorb the sign flip by placing the image plane in front of the centre of projection (the "virtual image plane"), which gives the same equations without the minus signs.

The division by depth is the essential structure. It is why near objects appear large, why parallel lines converge, and why depth cannot be recovered from a single view without additional assumptions: the mapping $(X,Y,Z) \mapsto (x,y)$ is many-to-one.

In homogeneous coordinates the projection is linear:

$$\begin{bmatrix} x \\ y \\ 1 \end{bmatrix} \sim \begin{bmatrix} f & 0 & c_x \\ 0 & f & c_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}$$

The matrix is the intrinsic matrix $K$. It contains focal length in pixels and the principal point, and it is the object that camera calibration estimates.

:::single-choice{#projection-depth} Why can a single calibrated image not determine the depth of an arbitrary point?

::option[Because sensor noise destroys all depth information]{#noise-depth explanation="Noise degrades precision, but the fundamental limitation is geometric: many world points along the same ray project to the same pixel."}
::option[Because projection maps a whole ray of 3D points onto one pixel, so the inverse is not unique]{#ray-ambiguity .correct explanation="The mapping divides by depth, collapsing a ray to a point. Recovering depth requires a second view, a known object size, or a learned prior."}
::option[Because the focal length is unknown]{#unknown-focal explanation="Even with a perfectly known focal length the ambiguity remains; calibration removes scale error, not the ray ambiguity."}
:::

:::demo{id="pinhole"} Focal length, distance and magnification
Drag the focal length and object distance. Notice that the projected size scales linearly with focal length and inversely with distance, while the field of view depends only on focal length and sensor size.
:::

## Lenses, focus and the aperture trade-off

A pinhole produces a sharp image but almost no light. A lens collects a wide bundle of rays from each scene point and converges it to a point on the sensor. The thin-lens equation relates object distance $d_o$, image distance $d_i$ and focal length:

$$\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}$$

The lens focuses exactly one plane. Points at other depths project to a small disc rather than a point, called the circle of confusion. When that disc is smaller than a pixel, the point appears sharp. The range of depths satisfying this is the depth of field.

Aperture controls the trade-off. A wider aperture collects more light and narrows depth of field; a smaller aperture increases depth of field but reduces light and eventually introduces diffraction blur. This is the same aperture–exposure–blur triangle the camera obscura exposed, now with a lens in the middle.

Real lenses also distort. Radial distortion bends straight lines near the image border; the standard model writes the observed radius as $r_d = r(1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$ and may add tangential terms for decentring. Calibration estimates these coefficients alongside $K$.

:::single-choice{#depth-of-field} What happens to depth of field when the aperture is widened?

::option[It increases, because more light reaches the sensor]{#dof-wider explanation="More light is collected, but the cone of rays per scene point is wider, so defocus blurs faster with distance."}
::option[It decreases, because the circle of confusion grows faster with defocus]{#dof-narrow .correct explanation="A larger aperture increases the blur disc for out-of-focus points, so fewer depths remain acceptably sharp."}
::option[It is unchanged; depth of field depends only on focal length]{#dof-focal-only explanation="Focal length and subject distance also matter, but aperture is a primary control of depth of field."}
:::

## Field of view and the geometry of choice

For a sensor of width $w$, the horizontal field of view is $2\arctan(w / 2f)$. A 50 mm lens on a 36 mm full-frame sensor gives about 40 degrees; an 18 mm lens gives about 90. Focal length and sensor size are therefore not independent design choices: what matters is their ratio.

This has direct consequences for vision systems. A wide field of view covers more scene but reduces angular resolution and increases distortion. A narrow field of view gives detail but loses context and makes tracking brittle. Multi-camera rigs exist precisely to resolve that tension.

There is also a resolution consequence. The same scene sampled at a longer focal length produces more pixels per object, which improves small-object detection and depth precision. Cropping a wide image is not equivalent, because the information was never sampled.

:::callout{type="insight" title="Pixels are angle, not distance"}
The intrinsic matrix converts world directions into pixel coordinates. It does not know about metres. Any metric quantity — object size, speed, depth — requires either a known scale, a calibrated stereo baseline, or an assumption about the scene.
:::

## The full projection chain

A point in world coordinates reaches a pixel through a composition:

1. Rigid transform by the extrinsics: $X_c = R X_w + t$.
2. Perspective division and intrinsics: $p = K X_c$ up to scale.
3. Lens distortion applied in normalised or pixel coordinates.
4. Discretisation onto the sensor grid.

Calibration estimates $K$, distortion coefficients and, for multi-camera systems, the relative poses. The process typically uses a planar target with known geometry observed at several orientations, solving a linear system followed by nonlinear refinement that minimises reprojection error.

Reprojection error is the right diagnostic. A mean error around a fraction of a pixel indicates a good calibration; systematic residuals that grow toward the image border usually indicate an unmodelled distortion term or a bad target.

:::single-choice{#extrinsics-role} In the projection chain, what do the extrinsic parameters encode?

::option[The sensor's colour response]{#extrinsics-colour explanation="Colour response belongs to the sensor and its processing pipeline, not to camera pose."}
::option[The rigid rotation and translation between world coordinates and the camera]{#extrinsics-pose .correct explanation="Extrinsics place the camera in the world; intrinsics then map camera coordinates to pixels."}
::option[The lens distortion coefficients]{#extrinsics-distortion explanation="Distortion is usually grouped with intrinsics because it is a property of the lens-sensor assembly."}
:::

## Summary

You can now write and invert the basic camera model and reason about its design trade-offs.

1. Derive perspective projection from similar triangles and express it with the intrinsic matrix.
2. Explain why a single view loses depth and what can restore it.
3. Relate aperture, focal length and sensor size to light, focus and field of view.
4. Describe the intrinsic, extrinsic and distortion parameters estimated by calibration.
