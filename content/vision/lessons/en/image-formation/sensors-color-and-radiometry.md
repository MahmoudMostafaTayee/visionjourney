---
lesson_id: "sensors-color-and-radiometry"
course_id: "image-formation"
lang: "en"
order_index: 2
title: "Sensors, Colour and Radiometry"
description: "How photons become numbers: Bayer filters, demosaicing, colour spaces, gamma, white balance and the noise model behind every image."
meta_title: "Sensors, Colour and Radiometry - Image Formation"
meta_description: "Learn how image sensors sample colour, how demosaicing and gamma work, and how exposure and noise shape the pixel values vision models consume."
meta_keywords: "image sensor, Bayer filter, demosaicing, colour space, gamma, white balance, sensor noise, dynamic range"
---

A digital image is not a window onto the world; it is the output of a measurement pipeline with a specific spectral response, exposure and noise model. Two cameras photographing the same scene can produce very different arrays of numbers. Understanding why prevents a whole class of silent bugs.

## From photons to electrons

A silicon photosite converts incoming photons into electrons with a quantum efficiency that depends on wavelength. The accumulated charge is read out, amplified and digitised. Three physical quantities govern the result:

- **Illumination** — how much light falls on the scene.
- **Aperture** — how much of that light the lens admits.
- **Exposure time** — how long charge accumulates.

Together they determine the sensor's exposure. Increase any of them and the signal rises; push too far and the photosite saturates, clipping to the maximum code value. Reduce too far and the signal approaches the read noise floor.

The noise is not uniform. Photon arrival is a Poisson process, so shot noise has standard deviation proportional to the square root of the signal. Read noise adds a roughly constant term, and dark current adds a temperature-dependent offset. A useful approximation is

$$\sigma^2 \approx \alpha I + \beta$$

where $I$ is the signal and $\alpha, \beta$ depend on the sensor and gain. This is why bright regions look clean and shadows look grainy, and why denoisers are evaluated across ISO settings rather than at one.

:::single-choice{#noise-model} Why does noise become more visible in dark regions of an image?

::option[Because the sensor applies less amplification to dark pixels]{#amp-dark explanation="Amplification is applied uniformly; the issue is the signal-to-noise ratio, not a per-pixel gain decision."}
::option[Because shot noise scales with the square root of the signal while read noise stays roughly constant]{#snr-dark .correct explanation="In dark regions the signal is small, so the fixed read-noise floor is a large fraction of it, lowering the signal-to-noise ratio."}
::option[Because dark pixels are quantised more coarsely]{#quant-dark explanation="Quantisation is uniform for a given bit depth. The dominant effect is the ratio of noise to signal."}
:::

## Colour is a construction

A single photosite measures intensity over a broad spectral band; it cannot distinguish wavelengths. Colour vision is recovered by comparing responses across spectrally different filters.

Most consumer sensors place a colour filter array over the grid, usually a Bayer pattern with twice as many green as red or blue photosites. Each pixel therefore measures only one channel, and the missing values are interpolated by a demosaicing algorithm. The interpolation is a reconstruction, not a measurement, and it produces characteristic artefacts near high-frequency edges — colour fringing and zippering.

The choice of primary filters defines the camera's colour space. Sensor RGB is device-dependent: the same physical colour produces different values on different cameras. Colour management converts through a device-independent space such as CIE XYZ or CIELAB, using a measured colour matrix.

sRGB, the most common output space, applies a nonlinear transfer function. Its roughly 2.2 gamma encodes more precision in dark tones, where human vision is more sensitive. This matters computationally: averaging or interpolating sRGB values is not the same as averaging light. For photometric operations you should linearise first.

:::single-choice{#gamma-linearise} Why must an image be linearised before computing a physically meaningful average of radiance?

::option[Because sRGB values are stored as integers]{#integer-issue explanation="Integer storage is a precision issue; the nonlinearity is the substantive one."}
::option[Because the sRGB transfer function is nonlinear, so code values are not proportional to light intensity]{#gamma-nonlinear .correct explanation="Averaging nonlinear code values over-weights dark tones. Converting to linear light makes the arithmetic match the physics."}
::option[Because demosaicing already averaged the channels]{#demosaic-average explanation="Demosaicing reconstructs missing channels; it does not make the encoding linear."}
:::

:::demo{id="histogram"} Exposure, contrast and the tonal histogram
The histogram is the distribution of intensities. Watch how exposure shifts it, contrast stretches it, and gamma bends the midtones. The clipped-pixel readout is the practical warning: once values hit the ends, the detail is gone.
:::

## White balance and the colour constancy problem

The colour of light varies. Daylight is bluish, tungsten is orange, shade is blue. The human visual system discounts the illuminant, so a white sheet looks white under both. A camera must either measure or assume the illuminant to render colour consistently.

Auto white balance estimates the illuminant from image statistics — grey-world assumes the average scene is neutral, white-patch assumes the brightest pixel is white. Both fail on scenes that violate the assumption, such as a wall of green foliage or a sunset.

For computer vision this is not only an aesthetic issue. A classifier trained on white-balanced photographs may see a shift in the distribution when deployed on raw sensor data or under unusual lighting. Colour augmentation during training is a cheap way to reduce that sensitivity, but it does not restore information lost by clipping.

:::single-choice{#white-balance} Why does grey-world white balance fail on a scene dominated by one colour?

::option[Because it assumes the average scene reflectance is neutral, which that scene violates]{#grey-world-fail .correct explanation="The estimator infers the illuminant from the assumption that channel averages should match. A uniformly green scene breaks that assumption and biases the correction."}
::option[Because it requires a calibrated colour chart in every image]{#grey-chart explanation="Grey-world uses image statistics only; a chart would be a different, more reliable calibration procedure."}
::option[Because it operates in linear space and colour must be corrected in gamma space]{#grey-space explanation="Operating in linear space is correct for radiometry. The failure here is the scene assumption, not the space."}
:::

## Dynamic range and high dynamic range imaging

The ratio between the brightest and darkest recordable values is the dynamic range. A typical 8-bit image stores about 8 stops after encoding; a good sensor captures 12 to 14 stops linearly. Scenes routinely exceed that: a window next to a dim interior can span 15 stops.

Clipping is irreversible. Once a photosite saturates, no post-processing recovers the highlight. This is why exposure bracketing and HDR capture exist, and why vision datasets differ in how they handle highlights. For a detection model, an overexposed region is simply a region with no texture, which can look like a valid background.

The practical lesson is to treat the sensor as part of the model. If your training data was captured with one exposure policy and your deployment uses another, you have a distribution shift before any algorithm runs.

:::callout{type="warning" title="Preprocessing is part of the model"}
Resizing, gamma, white balance and JPEG compression all change the input distribution. When a model underperforms in production, compare the preprocessing pipeline first — a mismatch there is more common than an architectural bug.
:::

## Summary

You can now explain how physical light becomes the numeric array a vision model consumes.

1. Relate illumination, aperture and exposure time to signal and clipping.
2. Use the shot-noise plus read-noise model to explain why shadows are noisy.
3. Describe demosaicing, colour spaces and the need to linearise before photometric computation.
4. Explain colour constancy and the assumptions behind auto white balance.
5. Recognise clipping and dynamic range as irreversible information loss.
