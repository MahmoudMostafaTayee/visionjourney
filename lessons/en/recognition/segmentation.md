---
lesson_id: "segmentation"
course_id: "recognition"
lang: "en"
order_index: 3
title: "Semantic and Instance Segmentation"
description: "Dense prediction with FCNs and U-Net, instance masks with Mask R-CNN, and the metrics that catch boundary and class-imbalance failures."
meta_title: "Semantic and Instance Segmentation - Recognition"
meta_description: "Learn fully convolutional networks, U-Net skip connections, Mask R-CNN, panoptic segmentation, Dice and IoU metrics and class imbalance."
meta_keywords: "semantic segmentation, U-Net, FCN, Mask R-CNN, panoptic segmentation, Dice loss, mIoU"
---

Segmentation assigns a label to every pixel. That makes the output spatially dense, the memory cost high and the evaluation sensitive to boundaries and class imbalance. The architectural response is an encoder-decoder that combines semantic context with spatial precision.

## Fully convolutional networks

The first deep segmentation models replaced the classifier head of a recognition network with convolutional layers, producing a spatial output map. This is the fully convolutional network idea: the network is trained on dense labels and can process inputs of varying size.

The naive version loses resolution through pooling and stride, so the output is coarse. The fix is to recover resolution by upsampling, and to combine coarse semantic features with fine spatial features from earlier layers. Skip connections make that combination possible.

:::model{src="unet-mini"} U-Net Mini: skips across the bottleneck
Trace the two downsampling paths and the two upsampling paths. The concatenation nodes merge decoder features with encoder features of the same resolution, restoring detail that the bottleneck compressed away.
:::

## U-Net and skip connections

U-Net (2015), developed for biomedical image segmentation, has a symmetric encoder-decoder with skip connections at each resolution. The encoder extracts context; the decoder restores spatial detail; the skips provide the high-frequency information that pooling discarded.

The design is remarkably effective with limited data, which is why it remains the default for medical, satellite and scientific segmentation. Variants add residual blocks, attention gates, dense connections or transformer bottlenecks, but the U-shape persists.

The concatenation detail matters. Adding features requires matching channel counts; concatenation allows the decoder to learn how much of each source to use. Most U-Net implementations concatenate, then apply a convolution to fuse.

:::single-choice{#unet-skip} What information do U-Net's skip connections primarily restore?

::option[High-resolution spatial detail lost during downsampling]{#unet-detail .correct explanation="Encoder features at matching resolution carry fine spatial information that the bottleneck compressed; the skips pass it directly to the decoder."}
::option[Additional semantic context from deeper layers]{#unet-context explanation="Context comes from the bottleneck and deeper encoder stages; the skips provide the complementary fine detail."}
::option[The class weights for imbalanced data]{#unet-weights explanation="Class weighting is a loss-level technique, unrelated to skip connections."}
:::

## Instance and panoptic segmentation

Semantic segmentation does not distinguish two instances of the same class. Instance segmentation predicts a separate mask per object. Mask R-CNN extends Faster R-CNN with a mask branch that predicts a binary mask for each region of interest, using RoIAlign to sample features without quantisation error.

The mask branch is small and operates per region, so the cost scales with the number of proposals. The design decouples mask prediction from box classification, which improves accuracy and simplifies training.

Panoptic segmentation unifies the two: every pixel gets a class label, and countable objects also get an instance identity. "Stuff" classes such as sky, road and grass are labelled semantically; "things" such as people and cars are labelled per instance. Panoptic quality combines recognition quality and segmentation quality into one measure.

The Segment Anything Model (SAM) reframed segmentation as promptable: given points, boxes or masks, it produces a mask. It was trained on a very large prompt-mask dataset and generalises to unseen objects without task-specific training, which shifts the design question from fixed classes to interactive prompting.

:::single-choice{#panoptic} What distinguishes panoptic segmentation from semantic segmentation?

::option[It also separates individual countable objects, giving each an instance identity]{#panoptic-instances .correct explanation="Panoptic output labels every pixel and additionally distinguishes separate instances of thing classes."}
::option[It produces bounding boxes instead of masks]{#panoptic-boxes explanation="Panoptic segmentation produces dense masks with instance identities, not just boxes."}
::option[It only works on videos]{#panoptic-video explanation="Panoptic segmentation applies to images; video panoptic adds temporal consistency as an extension."}
:::

## Metrics and class imbalance

Pixel accuracy is the fraction of correctly labelled pixels. It is misleading when one class dominates: predicting background everywhere can yield 95 percent accuracy on a dataset where objects occupy five percent of pixels.

Intersection over Union per class, averaged over classes (mIoU), is the standard. For class $c$,

$$\text{IoU}_c = \frac{TP_c}{TP_c + FP_c + FN_c}$$

and mIoU is the mean over classes. It penalises both missed regions and false positives and weights each class equally, which exposes failures on rare classes.

The Dice coefficient is closely related:

$$\text{Dice} = \frac{2|A \cap B|}{|A| + |B|}$$

Dice and IoU are monotonically related but not identical; Dice weights the intersection more heavily. Dice loss is popular in medical imaging because it directly optimises overlap and is less sensitive to foreground-background imbalance than plain cross-entropy.

Boundary quality is a separate concern. A mask can have high IoU while its boundary is systematically shifted, which matters for measurement tasks. Boundary IoU and Hausdorff distance evaluate contour accuracy and are worth reporting when the application depends on edges.

:::single-choice{#miou-motivation} Why is mIoU preferred to pixel accuracy for segmentation evaluation?

::option[Because it averages per-class overlap, so a dominant background class cannot hide failures on small classes]{#miou-classes .correct explanation="Averaging IoU per class gives each class equal weight, exposing poor performance on rare or small objects."}
::option[Because it is faster to compute]{#miou-speed explanation="Both metrics are cheap; the difference is sensitivity to class imbalance."}
::option[Because it measures inference latency]{#miou-latency explanation="IoU is an accuracy measure, unrelated to runtime."}
:::

## Practical considerations

Memory is the binding constraint. A 1024x1024 image with 150 classes and a float32 output tensor is large before any loss computation. Techniques include downsampling the output and upsampling with a learned or bilinear decoder, cropping training patches, mixed precision and gradient checkpointing.

Class imbalance requires active handling: weighted losses, sampling strategies that oversample rare classes, or losses such as Dice and Tversky that focus on overlap. The right choice depends on whether rare classes are rare because of physics (a defect that occurs seldom) or because of annotation policy.

Annotation quality dominates results. Segmentation labels are expensive and noisy at boundaries. Inter-annotator agreement sets an upper bound on measurable performance, and evaluating against a single annotator can reward a model for reproducing that annotator's idiosyncrasies rather than the true boundary.

:::callout{type="warning" title="Check the label pipeline"}
Visualise a random sample of ground-truth masks overlaid on images. Misaligned masks, class-index errors and inconsistent boundary conventions are common and can cost more accuracy than any architecture change.
:::

## Summary

You can now build and evaluate dense prediction systems.

1. Explain the encoder-decoder and skip-connection rationale.
2. Distinguish semantic, instance and panoptic segmentation.
3. Compute IoU, Dice and mIoU and choose a loss for imbalance.
4. Recognise annotation quality and boundary conventions as first-order factors.
