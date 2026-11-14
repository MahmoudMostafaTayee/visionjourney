---
lesson_id: "object-detection"
course_id: "recognition"
lang: "en"
order_index: 2
title: "Object Detection"
description: "Boxes, anchors, assignment, non-maximum suppression and the mAP protocol, from R-CNN to DETR."
meta_title: "Object Detection - Recognition"
meta_description: "Learn two-stage and one-stage detectors, anchors, label assignment, NMS, IoU, focal loss, DETR set prediction and mAP evaluation."
meta_keywords: "object detection, YOLO, Faster R-CNN, anchor, non-maximum suppression, IoU, mAP, DETR, focal loss"
---

Detection predicts a variable number of boxes with class labels. That change from one label per image to a set of objects forces new machinery: a way to propose locations, a way to assign targets, a way to remove duplicates and a metric that accounts for localisation quality.

## Boxes and IoU

A box is usually parameterised by its centre, width and height, or by two corners. Comparing two boxes requires a measure of overlap. Intersection over Union is

$$\text{IoU}(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

IoU is scale-invariant but insensitive to small shifts on large boxes. It is also undefined when both boxes have zero area. Variants such as GIoU, DIoU and CIoU add penalties for disjointness, centre distance and aspect ratio, which provide gradients even when boxes do not overlap.

:::demo{id="iou"} IoU, thresholds and the detection decision
Drag the predicted box and change the IoU threshold. The same prediction is a true positive at a lenient threshold and a false positive at a strict one. This dependence is why mAP is reported across a range of IoU values.
:::

:::single-choice{#iou-threshold} Why can the same predicted box be a true positive at IoU 0.5 and a false positive at IoU 0.75?

::option[Because the true-positive criterion requires IoU above the chosen threshold, which the box may fail at the stricter level]{#iou-threshold-effect .correct explanation="A match is defined relative to a threshold, so localisation quality determines whether a detection counts at each operating point."}
::option[Because IoU is not symmetric]{#iou-symmetry explanation="IoU is symmetric; the asymmetry is in the evaluation threshold, not the measure."}
::option[Because the class label changes with the threshold]{#iou-class explanation="The threshold governs localisation matching, not the predicted class."}
:::

## Two-stage detectors

R-CNN (2014) proposed regions with a classical algorithm, cropped and resized each, and ran a CNN classifier on every crop. It was accurate but extremely slow because the CNN ran thousands of times per image.

Fast R-CNN shared the convolutional computation across the whole image and used region-of-interest pooling to extract a fixed-size feature per proposal. Faster R-CNN replaced the external proposal algorithm with a region proposal network trained end-to-end, making the whole pipeline differentiable.

The two-stage design separates *where* from *what*: a proposal stage generates class-agnostic candidate boxes, and a second stage classifies and refines each. This is accurate, especially for small objects, but slower than one-stage methods because of the per-region computation.

## One-stage detectors

YOLO (2015) reframed detection as a single regression problem over a grid. Each cell predicts boxes and class scores directly. SSD used multiple feature maps at different resolutions with default boxes of various aspect ratios. RetinaNet introduced the focal loss to address the extreme foreground-background imbalance that made dense one-stage detectors underperform.

Focal loss modifies cross-entropy with a modulating factor:

$$\text{FL}(p_t) = -\alpha_t (1-p_t)^\gamma \log p_t$$

When a sample is well classified, $p_t$ is near one and the factor $(1-p_t)^\gamma$ suppresses its contribution. The effect is to concentrate training on hard, misclassified examples, which are mostly the rare foreground anchors.

Anchor-free detectors removed the anchor hyperparameters. FCOS predicts distances to the box edges from each foreground location; CenterNet predicts object centres and sizes. These designs simplify assignment and reduce the number of tuned constants.

:::single-choice{#focal-loss} What imbalance does focal loss address?

::option[The overwhelming number of easy background locations relative to foreground objects]{#focal-imbalance .correct explanation="Dense detectors produce far more negatives than positives; down-weighting easy examples stops them from dominating the gradient."}
::option[The imbalance between different object classes]{#focal-classes explanation="Focal loss is about example difficulty, not class frequency, although class weighting can be combined with it."}
::option[The imbalance between box regression and classification losses]{#focal-tasks explanation="Loss balancing across tasks is a separate weighting issue; focal loss modulates per-example confidence."}
:::

## Assignment and NMS

Training needs a target for each prediction. Anchor-based methods assign anchors to ground-truth boxes by IoU thresholds, which requires careful tuning: too high and few anchors are positive, too low and boxes are poorly localised. Modern methods use dynamic assignment, matching predictions to ground truth by cost, which improves stability.

At inference, many predictions overlap the same object. Non-maximum suppression sorts by score, keeps the highest, and removes boxes whose IoU with it exceeds a threshold. Soft-NMS decays scores instead of removing boxes, which helps in crowded scenes. NMS is a hard-coded post-processing step, and its threshold is a deployment parameter, not a detail.

DETR took a different route: it predicts a fixed set of boxes and uses Hungarian matching to assign predictions to ground truth one-to-one. With one-to-one assignment, no duplicate suppression is needed. The cost is slow convergence, which later work addressed with denoising and improved matching.

:::single-choice{#detr-nms} Why does DETR not require non-maximum suppression?

::option[Because its set-prediction loss assigns each ground-truth object to exactly one prediction, discouraging duplicates]{#detr-one-to-one .correct explanation="One-to-one Hungarian matching trains the model to produce a single prediction per object, so duplicates are not selected."}
::option[Because it predicts only one box per image]{#detr-one-box explanation="DETR predicts a fixed set of boxes, typically far more than the number of objects."}
::option[Because it uses a stricter IoU threshold during training]{#detr-threshold explanation="The difference is the assignment rule, not a threshold value."}
:::

## Evaluation: precision, recall and mAP

A detection is a true positive if its class matches and its IoU with an unmatched ground-truth box exceeds the threshold. Matching is usually greedy by score. Precision is the fraction of detections that are correct; recall is the fraction of ground-truth objects found.

Average precision summarises the precision-recall curve for one class. The curve is built by varying the score threshold, and AP is the area under the interpolated curve. Mean average precision averages AP over classes. COCO's primary metric averages AP over IoU thresholds from 0.5 to 0.95 in steps of 0.05, which rewards precise localisation rather than merely finding the object.

This protocol has consequences. A model tuned for IoU 0.5 can look strong on VOC-style mAP and mediocre on COCO. Small, medium and large objects are reported separately because performance differs sharply by scale. Always state the dataset, the IoU range and whether the metric is AP50, AP75 or AP[.5:.95].

:::single-choice{#coco-ap} What does COCO's AP[.5:.95] reward relative to AP50?

::option[Consistently precise localisation across a range of IoU thresholds]{#coco-precision .correct explanation="Averaging over strict thresholds penalises loose boxes that would pass only at IoU 0.5."}
::option[Faster inference]{#coco-speed explanation="The metric measures detection quality, not runtime."}
::option[Better classification of small objects only]{#coco-small explanation="Scale-specific AP is reported separately; the aggregate averages over all sizes and thresholds."}
:::

:::callout{type="insight" title="Post-processing is part of the model"}
NMS threshold, score threshold, maximum detections per image and box clipping all change the reported metric. Record them with the model. A detector compared at different NMS settings is not comparable, even if the network weights are identical.
:::

## Summary

You can now design and evaluate a detector with attention to its actual failure modes.

1. Compute IoU and explain threshold-dependent matching.
2. Compare two-stage, one-stage, anchor-free and set-prediction designs.
3. Explain focal loss and the assignment problem.
4. Interpret AP, AP50 and COCO's averaged AP correctly.
