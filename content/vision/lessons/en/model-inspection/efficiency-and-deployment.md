---
lesson_id: "efficiency-and-deployment"
course_id: "model-inspection"
lang: "en"
order_index: 3
title: "Efficiency and Deployment"
description: "FLOPs versus latency, pruning, quantisation, distillation, runtimes and the monitoring that keeps a deployed model honest."
meta_title: "Efficiency and Deployment - Model Inspection"
meta_description: "Learn model efficiency: FLOPs versus latency, pruning, post-training quantisation, knowledge distillation, ONNX Runtime, TensorRT and drift monitoring."
meta_keywords: "model efficiency, FLOPs, latency, pruning, quantisation, knowledge distillation, ONNX Runtime, TensorRT, drift"
---

A model that cannot meet its latency, memory or power budget is not deployable, regardless of its accuracy. Efficiency is an architectural property, a numerical property and a systems property, and optimising one can hurt another.

## FLOPs are not latency

Multiply-accumulate counts are a useful proxy for compute, but latency is determined by memory bandwidth, kernel efficiency, parallelisation and the framework. A depthwise convolution can have few FLOPs and still be slow because it reads and writes memory without enough arithmetic to hide the cost.

The roofline model makes the distinction concrete. An operation is compute-bound if its arithmetic intensity — FLOPs per byte moved — exceeds the hardware's ratio of peak compute to memory bandwidth. Otherwise it is memory-bound, and reducing FLOPs does not help.

This is why mobile architectures are designed around memory traffic as much as multiply-accumulates. It is also why a theoretically cheaper model can be slower in practice, and why benchmarks must measure latency on the target hardware with the target runtime.

:::single-choice{#roofline} Why can reducing FLOPs fail to reduce latency?

::option[Because the operation may be memory-bandwidth bound rather than compute bound]{#memory-bound .correct explanation="If the kernel spends most of its time moving data, fewer arithmetic operations do not shorten the critical path."}
::option[Because FLOPs are always measured incorrectly]{#flop-error explanation="FLOP counting is well defined; the mismatch is between arithmetic cost and system cost."}
::option[Because GPUs ignore small kernels]{#gpu-ignore explanation="GPUs execute them, but they may be dominated by launch and memory overhead rather than arithmetic."}
:::

## Pruning and sparsity

Pruning removes weights, channels or blocks. Unstructured pruning removes individual weights and produces sparse matrices, which require specialised hardware or libraries to translate into speed. Structured pruning removes entire channels or filters, which reduces dense tensor dimensions and is easier to accelerate.

The typical recipe is magnitude-based pruning followed by fine-tuning. Pruning at initialisation, as in lottery-ticket experiments, showed that sparse subnetworks can train to comparable accuracy, but the practical benefit for deployment depends on whether the sparsity is exploitable.

Channel pruning requires care: removing a channel changes the input dimension of the next layer, so the network must be rewritten consistently. Tools that prune without preserving shape compatibility produce models that fail at export.

:::single-choice{#structured-pruning} Why is structured pruning more useful for deployment than unstructured pruning?

::option[Because removing channels reduces dense tensor dimensions that standard hardware accelerates efficiently]{#structured-dense .correct explanation="Unstructured sparsity requires specialised kernels; structured pruning yields smaller dense layers that run fast on ordinary hardware."}
::option[Because structured pruning always preserves accuracy better]{#structured-accuracy explanation="Accuracy retention depends on the method and fine-tuning, not on the structure alone."}
::option[Because unstructured pruning does not reduce parameter count]{#unstructured-params explanation="It does reduce the count, but the resulting sparsity is hard to exploit for speed."}
:::

## Quantisation

Quantisation reduces numerical precision. Post-training quantisation converts a trained float model to int8 using calibration data to choose scales. Quantisation-aware training simulates the quantisation during training so the weights adapt to the reduced precision.

The main challenge is activation ranges. Weights are relatively well behaved, but activations can have long tails, and a single outlier can consume most of the range and destroy resolution for the rest. Per-channel scales, percentile calibration and keeping sensitive layers in higher precision are standard mitigations.

Quantisation can improve latency substantially on CPUs and edge accelerators, and it reduces memory footprint by up to four times. It also changes numerics, so accuracy must be validated on the target distribution, not just on the calibration set.

:::single-choice{#quantisation-outliers} Why do activation outliers make int8 quantisation difficult?

::option[Because a few large values stretch the scale, reducing resolution for the majority of values]{#quant-outliers .correct explanation="A shared scale must cover the maximum, so typical values end up represented with few effective bits."}
::option[Because int8 cannot represent zero]{#quant-zero explanation="Int8 with zero-point representation handles zero; the issue is dynamic range allocation."}
::option[Because quantisation only applies to weights]{#quant-weights-only explanation="Both weights and activations are quantised in most deployment schemes."}
:::

## Distillation

Knowledge distillation trains a smaller student to match a larger teacher. The student learns from soft targets, which carry information about class similarity that hard labels do not. The classic loss combines cross-entropy with a KL divergence between softened student and teacher distributions:

$$\mathcal{L} = (1-\alpha)\,\text{CE}(y, p_s) + \alpha \tau^2 \text{KL}(p_t^\tau \,\|\, p_s^\tau)$$

The temperature $\tau$ controls how much of the teacher's dark knowledge is exposed. A higher temperature softens both distributions and reveals more structure among the non-target classes.

Distillation is often combined with pruning and quantisation. A distilled student can be smaller, faster and sometimes more robust, because soft targets act as a regulariser. The teacher's errors are also transferred, so a biased teacher produces a biased student.

:::single-choice{#distillation-soft} What information do soft teacher targets provide that hard labels do not?

::option[Relative similarity between classes, which regularises the student and speeds learning]{#soft-targets .correct explanation="The teacher's probability distribution encodes which classes are confusable, giving a richer signal than a one-hot label."}
::option[The exact architecture of the teacher]{#teacher-arch explanation="The student architecture is chosen separately; only the output distribution is transferred."}
::option[A guarantee of higher accuracy than the teacher]{#teacher-guarantee explanation="A student can approach but rarely exceeds a stronger teacher, and no guarantee applies."}
:::

## Runtimes and deployment

An exported model must be executed by a runtime. ONNX Runtime provides cross-platform execution with graph optimisations. TensorRT compiles for NVIDIA GPUs with layer fusion and precision calibration. TFLite targets mobile and embedded devices. Core ML targets Apple hardware.

Each runtime has its own operator support, optimisation passes and precision behaviour. A model that runs well in one may fall back to slow generic kernels in another. Always benchmark on the target runtime and hardware, with the batch size and precision you will deploy.

Batching improves throughput by amortising kernel launch and memory overhead, but it increases latency and memory. Real-time systems often use batch size one with a carefully optimised pipeline; offline systems batch aggressively.

:::callout{type="insight" title="Measure the pipeline, not the model"}
Preprocessing, resizing, colour conversion and post-processing can dominate end-to-end latency for small models. A 2 ms network inside a 40 ms Python preprocessing loop is not a 2 ms system. Profile the whole pipeline before optimising the network.
:::

## Monitoring after deployment

A deployed model encounters a distribution that shifts over time: new camera hardware, seasonal lighting, changing object styles, updated preprocessing. Performance silently degrades.

Monitor input statistics, prediction distributions and, where labels are available, accuracy. Drift detectors flag changes in feature distributions before labels reveal an accuracy drop. Shadow deployments compare a candidate model against the incumbent on live traffic without affecting users.

Maintain a rollback path. A model update that improves an offline benchmark can degrade a production slice, and the ability to revert quickly is part of the deployment design, not an afterthought.

:::single-choice{#drift-monitoring} Why monitor input and prediction distributions when labels are delayed?

::option[Because distribution shift can be detected before ground-truth labels arrive, providing an early warning]{#drift-early .correct explanation="Unlabelled monitoring catches covariate shift early, whereas accuracy monitoring waits for labels that may take days."}
::option[Because labels are never needed once a model is deployed]{#no-labels-deployed explanation="Labels remain necessary to measure accuracy; distribution monitoring is an earlier, indirect signal."}
::option[Because prediction distributions are always stable]{#stable-preds explanation="Prediction distributions change under shift, which is precisely why they are monitored."}
:::

## Summary

You can now reason about efficiency as a system property and deploy with safeguards.

1. Distinguish compute-bound from memory-bound operations.
2. Choose structured pruning and validate shape consistency.
3. Apply post-training and aware quantisation, handling activation outliers.
4. Use distillation with soft targets and understand its limits.
5. Benchmark the full pipeline and monitor for drift after deployment.
