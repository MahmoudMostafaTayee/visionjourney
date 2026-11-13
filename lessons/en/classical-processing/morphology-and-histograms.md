---
lesson_id: "morphology-and-histograms"
course_id: "classical-processing"
lang: "en"
order_index: 3
title: "Morphology and Histograms"
description: "Shapes on binary and grey images, connected components, Otsu thresholding and contrast enhancement that does not invent detail."
meta_title: "Morphology and Histograms - Classical Image Processing"
meta_description: "Learn erosion, dilation, opening and closing, connected components, Otsu thresholding, watershed and histogram equalisation."
meta_keywords: "mathematical morphology, erosion, dilation, opening, closing, Otsu, connected components, CLAHE"
---

Thresholding turns a grey image into a set of pixels. Once you have a set, you can manipulate its shape directly. Morphology is the algebra of those manipulations, and it remains the fastest way to clean up a segmentation before measurement.

## Binary morphology

Let $A$ be a binary set of foreground pixels and $B$ a structuring element — a small shape such as a 3x3 square or a cross. Erosion keeps a pixel only if the entire structuring element fits inside the foreground:

$$A \ominus B = \{z \mid B_z \subseteq A\}$$

Dilation keeps a pixel if the structuring element touches the foreground:

$$A \oplus B = \{z \mid B_z \cap A \neq \emptyset\}$$

Erosion shrinks foreground and removes small objects; dilation grows foreground and fills small holes. The two are duals under complementation, which is why the same code with an inverted image produces the opposite effect.

Opening is erosion followed by dilation. It removes small protrusions and isolated specks while preserving the overall size of larger objects. Closing is dilation followed by erosion. It fills small holes and connects nearby components. The order matters: opening cannot restore what erosion removed, but it restores the shape of what survived.

:::single-choice{#opening-effect} A segmentation has salt noise, isolated single-pixel foreground specks. Which operation removes them while leaving large objects roughly unchanged?

::option[Closing, because it fills gaps]{#closing-salt explanation="Closing grows foreground, so it would enlarge rather than remove isolated specks."}
::option[Opening, because erosion eliminates structures smaller than the structuring element and dilation restores the rest]{#opening-salt .correct explanation="Erosion deletes specks smaller than the element; the following dilation regrows the surviving larger shapes to approximately their original size."}
::option[Dilation, because it merges the specks into objects]{#dilation-salt explanation="Dilation would merge specks with nearby objects and enlarge everything, not remove noise."}
:::

## The structuring element is the hypothesis

The structuring element encodes a shape prior. A horizontal line element preserves horizontal strokes and removes vertical ones. A disk treats all orientations equally and is the usual choice for isotropic cleanup. A large element removes large structures, so scale selection is a modelling decision, not a preprocessing detail.

Grey-scale morphology replaces the set operations with min and max over a neighbourhood. Erosion becomes a local minimum filter; dilation a local maximum. This is useful for background estimation: an opening with a large element removes bright structures smaller than the element, leaving an estimate of the dark background. Subtracting that estimate is the basis of top-hat filtering for small bright objects.

:::single-choice{#tophat} What does a white top-hat transform (original minus opening) isolate?

::option[Bright structures smaller than the structuring element]{#tophat-bright .correct explanation="Opening removes small bright features; subtracting the opened image leaves those features as a residual."}
::option[Dark structures larger than the structuring element]{#tophat-dark explanation="That is closer to a black top-hat, which uses closing instead of opening."}
::option[The average intensity of the image]{#tophat-average explanation="Top-hat is a spatial residual, not a global statistic."}
:::

## Thresholding and connected components

Otsu's method chooses the threshold that maximises between-class variance of the intensity histogram, which is equivalent to minimising within-class variance for a two-class model. It assumes a bimodal histogram and fails gracefully when the assumption is wrong — it still returns a threshold, but one that may split a single mode.

Adaptive thresholding computes a local threshold per region, which handles uneven illumination such as a scanned page with a shadow. The local window size becomes a parameter: too small and flat regions amplify noise, too large and illumination variation is not corrected.

Once binarised, connected-component labelling assigns a unique label to each maximal connected foreground region. This converts a pixel set into objects with measurable properties: area, bounding box, centroid, perimeter, orientation and moments. For many industrial tasks this is the entire algorithm, and it is deterministic, explainable and fast.

:::single-choice{#otsu-assumption} Otsu's method performs poorly on an image with a single dominant intensity mode. Why?

::option[Because it assumes two classes with separable intensity distributions]{#otsu-bimodal .correct explanation="The criterion maximises separation between two class means, which is not meaningful when the histogram has one mode."}
::option[Because it requires a colour image]{#otsu-colour explanation="Otsu operates on intensities or per-channel histograms; colour is not the limitation."}
::option[Because it uses spatial connectivity]{#otsu-spatial explanation="Otsu is a histogram method and ignores spatial arrangement entirely."}
:::

## Histogram equalisation and its limits

Histogram equalisation applies a monotonic mapping that makes the intensity histogram approximately uniform. It increases global contrast, which can reveal structure in underexposed regions. Because the mapping is monotonic, it does not reorder intensities, so it cannot create new edges — but it can amplify noise in regions that occupied few bins.

Contrast-limited adaptive histogram equalisation divides the image into tiles, equalises each with a clip limit, and interpolates between tiles. The clip limit is what prevents noise amplification: bins above the limit are redistributed before the mapping is computed. CLAHE is standard in medical and scientific imaging, and it is a common augmentation in vision training pipelines.

The caution is epistemic. Enhanced contrast makes an image easier for a human to interpret, but it does not add information. A model trained on CLAHE-processed medical images may learn to rely on enhancement artefacts, and a downstream measurement may change because the mapping is nonlinear.

:::callout{type="warning" title="Enhancement is not evidence"}
Contrast enhancement changes the display dynamic range, not the acquired signal. If a measurement depends on intensity, record whether enhancement was applied and keep the raw data.
:::

## Summary

You can now clean and measure binary regions with operations whose behaviour you can predict.

1. Apply erosion, dilation, opening and closing and explain their order effects.
2. Choose a structuring element that encodes a shape or scale prior.
3. Use Otsu, adaptive thresholding and connected components, knowing their assumptions.
4. Apply CLAHE and explain why it can amplify noise and change measurements.
