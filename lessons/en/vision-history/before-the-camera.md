---
lesson_id: "before-the-camera"
course_id: "vision-history"
lang: "en"
order_index: 1
title: "Before the Camera"
description: "How optics, perspective and the desire to record light set up the questions computer vision would inherit."
meta_title: "Before the Camera - Vision History"
meta_description: "Explore the camera obscura, Renaissance perspective, the invention of photography and the first studies of motion and stereo."
meta_keywords: "camera obscura, Ibn al-Haytham, perspective, photography history, stereoscope, Muybridge"
---

Computer vision did not begin with computers. It began with a much older question: how can a three-dimensional, illuminated world produce a two-dimensional pattern that an observer can interpret? For a thousand years the answer was an instrument and a theory of light. Understanding that inheritance explains why the field still talks about projection, inversion and "recovering" structure.

## The camera obscura

The oldest working image-forming device is a dark room with a small hole in one wall. Light from each point of the outside scene passes through the aperture and lands on the opposite wall, where rays cross. The result is an inverted, dim, continuous image.

Ibn al-Haytham described the device systematically in his *Book of Optics* (written in the 11th century), arguing that light travels in straight lines from objects to the eye — an intromission theory that displaced earlier extramission accounts. His analysis is recognisably geometric: he treats the aperture as selecting a narrow bundle of rays, and he studies how the size of the hole trades brightness against sharpness.

That trade-off is the first imaging lesson. A pinhole small enough to produce a sharp image admits very little light, and if it becomes comparable to the wavelength of light, diffraction blurs it again. Every sensor design since has been a negotiation between the same three quantities: aperture, exposure time and blur.

:::single-choice{#camera-obscura-imaging} What does a pinhole camera actually produce on its back plane?

::option[A sharp image with infinite depth of field but very little light]{#pinhole-tradeoff .correct explanation="A small aperture keeps the projection sharp over a wide depth range, but admits so little light that exposure becomes long."}
::option[A fully three-dimensional reconstruction of the scene]{#pinhole-reconstruction explanation="The device records a two-dimensional projection. Depth information is lost, which is precisely why later vision had to recover it."}
::option[An image that is upright and brighter than the scene]{#pinhole-upright explanation="Rays cross at the aperture, so the projection is inverted and dimmer than the original scene."}
:::

## Perspective becomes a method

Renaissance artists did not merely paint what they saw; they constructed a geometry for it. Brunelleschi's demonstrations around 1420 and Alberti's *De pictura* (1435) formalised linear perspective: parallel lines in the world converge at a vanishing point, and equal world intervals map to unequal image intervals according to distance.

This is the projective geometry that a camera matrix encodes. The artist's construction — choose a station point, a picture plane, and draw the intersection of sight lines with that plane — is exactly a pinhole projection. When you later write $x = f X / Z$, you are writing the rule the painters discovered empirically.

Photography made the rule mechanical. Nicéphore Niépce produced a fixed heliographic image around 1826; Louis Daguerre announced the daguerreotype in 1839; William Henry Fox Talbot's calotype introduced the negative, and with it the possibility of unlimited positive prints. The significant shift was not aesthetic but epistemological: an image became a measurement that could be stored, duplicated and compared.

:::single-choice{#perspective-projection} In linear perspective, why do parallel railway tracks converge?

::option[Because the paint dries toward the horizon]{#paint-drying explanation="Convergence is a property of the projection geometry, not of the medium."}
::option[Because the projection divides world coordinates by depth]{#depth-division .correct explanation="Under perspective projection, image position is proportional to world position divided by distance, so far-away parallel lines approach the same vanishing point."}
::option[Because lenses bend parallel rays toward the centre]{#lens-bending explanation="The convergence occurs in the ideal pinhole model already, before any lens is introduced."}
:::

## Motion, stereo and the observer

Two nineteenth-century instruments pushed beyond the single static view. The stereoscope, described by Charles Wheatstone in 1838, presented each eye a slightly different drawing; the brain fused them into depth. That demonstrated that disparity between two projections carries three-dimensional information — the foundation of the stereo geometry you will derive later.

:::single-choice{#stereoscope-disparity} What did the stereoscope demonstrate about depth perception?

::option[That two slightly different projections can be fused into a depth percept]{#stereo-fusion .correct explanation="The device showed that disparity between the two views is sufficient for the observer to perceive depth."}
::option[That depth is inferred entirely from shading]{#stereo-shading explanation="Shading is a separate cue; the stereoscope isolated the effect of two viewpoints."}
::option[That depth requires motion of the observer]{#stereo-motion explanation="The stereoscope works with static drawings and no observer motion."}
:::

Eadweard Muybridge's motion studies in the 1870s and 1880s used banks of cameras to freeze a galloping horse. Étienne-Jules Marey developed a single-plate chronophotographic gun. Both made time discrete, which is the precondition for treating video as a sequence of frames rather than a continuous flow.

Meanwhile physiology was asking how the eye itself encodes colour and edge. Thomas Young (1802) and Hermann von Helmholtz (1852) proposed trichromatic receptors; Ewald Hering argued for opponent processing. Both accounts survive in modern colour spaces: RGB is trichromatic, while CIELAB's opponent axes echo Hering.

:::callout{type="insight" title="The pattern that repeats"}
Each era built an instrument, discovered the ambiguity it introduced, and then built mathematics to resolve it. Pinhole: depth is lost. Stereo: depth is recoverable from disparity. Photography: exposure and blur become variables. Computer vision inherits the entire agenda.
:::

By the time digital computers arrived, the conceptual pieces were ready: a projection model, a theory of colour, a notion of discrete frames, and the observation that two views constrain depth. What was missing was a way to compute descriptions from the measurements automatically.

## Summary

You can now situate the optical and geometric ideas that computer vision inherited.

1. Explain how a camera obscura forms an inverted image through ray crossing.
2. Relate Renaissance perspective to the division by depth in a projection.
3. Describe how the stereoscope and motion studies introduced disparity and discrete time.
4. Recognise the aperture–exposure–blur trade-off as an enduring imaging constraint.
