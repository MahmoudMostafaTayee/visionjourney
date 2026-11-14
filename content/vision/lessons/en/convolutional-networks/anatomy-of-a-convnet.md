---
lesson_id: "anatomy-of-a-convnet"
course_id: "convolutional-networks"
lang: "en"
order_index: 1
title: "Anatomy of a Convolutional Network"
description: "Channels, strides, padding, pooling and the parameter and FLOP arithmetic that decides whether a design is feasible."
meta_title: "Anatomy of a Convolutional Network - Convolutional Networks"
meta_description: "Learn convolution arithmetic, output shape formulas, parameter counts, FLOPs, pooling, 1x1 bottlenecks and depthwise separable layers."
meta_keywords: "convolution arithmetic, output size, parameter count, FLOPs, pooling, 1x1 convolution, depthwise separable"
---

A modern CNN is a stack of tensor transformations. Each layer has a small number of design parameters, and those parameters determine the shape, cost and representational capacity of everything downstream. Being able to compute the shapes and costs by hand is the difference between copying an architecture and designing one.

## The convolution layer

A convolution layer has four architectural parameters:

- **kernel size** $k$, the spatial extent of each filter;
- **input channels** $C_{\text{in}}$ and **output channels** $C_{\text{out}}$;
- **stride** $s$, the step between applications;
- **padding** $p$, the border added to the input.

Its output spatial size follows

$$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} + 2p - k}{s} \right\rfloor + 1$$

and the same formula applies to width. A 224x224 input with $k=7$, $s=2$, $p=3$ produces 112x112, which is exactly the stem of ResNet. With $k=3$, $s=1$, $p=1$ the spatial size is preserved, which is why most residual blocks use that configuration.

The parameter count is

$$k^2 \cdot C_{\text{in}} \cdot C_{\text{out}} + C_{\text{out}}$$

and the multiply-accumulate count is

$$H_{\text{out}} \cdot W_{\text{out}} \cdot k^2 \cdot C_{\text{in}} \cdot C_{\text{out}}$$

For a 3x3 convolution from 256 to 256 channels at 56x56, the parameters are $9 \cdot 256 \cdot 256 \approx 590$ thousand, and the MACs are $56^2 \cdot 9 \cdot 256^2 \approx 1.85$ billion. That single layer is a substantial fraction of a ResNet-50's total compute, which is why channel count and spatial resolution dominate cost.

:::single-choice{#conv-cost-driver} For a fixed kernel size, which factor most strongly increases a convolution layer's FLOPs?

::option[The product of input channels, output channels and output spatial area]{#conv-cost .correct explanation="MACs scale linearly with each of those three factors, and the channel product is usually the largest lever."}
::option[The number of layers in the network]{#conv-depth explanation="Depth adds cost, but the question asks what drives a single layer's cost."}
::option[The batch size only]{#conv-batch explanation="Batch size scales cost linearly across all layers but is not part of the layer's per-sample cost."}
:::

:::model{src="demo-cnn"} A complete convolutional graph: Demo CNN
This is a real ONNX export. Follow the shapes from 1x1x28x28 through two convolutions and pools to the classifier. Click any node to inspect its operation, output shape and parameter count.
:::

## Pooling and downsampling

Pooling reduces spatial resolution. Max pooling keeps the strongest response in each window, which provides mild translation tolerance; average pooling smooths. A 2x2 max pool with stride two halves both spatial dimensions and has no learnable parameters.

Downsampling is essential for two reasons. It reduces compute quadratically with the scale factor, and it increases the receptive field of later layers so that deep units can integrate context. It also creates the coarse-to-fine hierarchy that makes classification efficient.

Strided convolution is an alternative to pooling. It learns the downsampling rather than fixing it, at the cost of introducing aliasing unless the stride-kernel combination satisfies the sampling conditions. Modern designs often prefer strided convolutions in the stem and pooling or stride in the stages.

Global average pooling collapses the final feature map to one vector per channel, replacing the large fully connected layers of early networks. It reduces parameters dramatically and makes the model less sensitive to input resolution, at the cost of discarding spatial information that some tasks need.

:::single-choice{#pooling-effect} What does a 2x2 max pool with stride two do to the receptive field of subsequent layers?

::option[It increases the effective receptive field because each subsequent feature covers more input area]{#pool-rf .correct explanation="Halving the resolution means one later pixel corresponds to twice the input extent, so the receptive field grows with each downsample."}
::option[It decreases the receptive field because information is discarded]{#pool-rf-decrease explanation="Discarding detail is a loss of information, but the spatial extent represented per unit grows."}
::option[It leaves the receptive field unchanged]{#pool-rf-same explanation="Resolution changes alter the mapping between feature coordinates and input coordinates, so the field changes."}
:::

## 1x1 convolutions and bottlenecks

A 1x1 convolution is a linear combination across channels at each spatial position. It has no spatial extent, so it cannot mix neighbouring pixels, but it can change channel count cheaply and add nonlinearity.

This makes it a bottleneck tool. Instead of a 3x3 convolution from 256 to 256 channels, a design may use 1x1 from 256 to 64, a 3x3 from 64 to 64, and a 1x1 from 64 to 256. The spatial convolution now operates on 64 channels, reducing its cost by a factor of sixteen, while the two 1x1 layers restore the channel dimension.

ResNet's bottleneck blocks use exactly this pattern, and Inception modules use 1x1 layers to reduce channels before parallel branches. The trade-off is depth and extra activations against a large reduction in multiply-accumulates.

:::single-choice{#bottleneck-purpose} What is the primary purpose of a 1x1 bottleneck in a residual block?

::option[To reduce channel count before an expensive 3x3 convolution, lowering compute]{#bottleneck-compute .correct explanation="The 1x1 projection compresses channels so the spatial convolution operates on fewer channels, then a second projection restores width."}
::option[To increase the spatial resolution]{#bottleneck-resolution explanation="1x1 convolutions do not change spatial dimensions; stride or pooling does that."}
::option[To replace the need for nonlinear activations]{#bottleneck-activation explanation="Bottlenecks usually include activations and do not replace them."}
:::

## Depthwise separable convolution

A standard convolution jointly learns spatial and channel mixing. A depthwise separable convolution splits the operation: a depthwise convolution applies one spatial filter per input channel, and a pointwise 1x1 convolution mixes channels.

For $k=3$, the cost falls from $9 C_{\text{in}} C_{\text{out}}$ to $9 C_{\text{in}} + C_{\text{in}} C_{\text{out}}$ per position. With $C_{\text{in}} = C_{\text{out}} = 256$, that is roughly a nine-fold reduction. MobileNet is built on this decomposition, and it is why mobile vision models can run in real time.

The trade-off is representational. Separating spatial and channel mixing reduces the hypothesis space, and depthwise convolutions are memory-bandwidth bound rather than compute bound, so the theoretical FLOP saving does not translate one-to-one into latency saving.

:::single-choice{#depthwise-saving} Why does a depthwise separable convolution reduce FLOPs so dramatically?

::option[Because the expensive spatial filter is applied per channel rather than across all channel pairs]{#depthwise-reason .correct explanation="Removing the cross-channel term from the spatial convolution leaves only the cheap pointwise mixing, cutting the dominant cost."}
::option[Because it uses a smaller kernel]{#depthwise-kernel explanation="The kernel size can stay the same; the saving comes from factorising channel mixing."}
::option[Because it skips the activation function]{#depthwise-activation explanation="Activations are still used; they are not the source of the saving."}
:::

## Reading the graph

The Model Lab viewer above shows the exported graph with real tensor shapes. Two habits make it useful.

First, trace the spatial dimension. It should shrink at stems and stage transitions, and stay constant inside a stage. An unexpected shrink indicates a stride or padding bug. Second, trace the channel dimension. It should increase as resolution decreases, roughly preserving the per-position feature budget.

Third, look for repeated motifs. A residual network is a stem, four stages of repeated blocks, a pool and a classifier. Once you can see the motif, a 150-layer graph becomes nine conceptual steps.

:::callout{type="insight" title="Compute the cost before you train"}
For a new architecture, compute the parameter count and MACs of the first three and last three layers. They usually account for most of the cost and most of the shape bugs. Do this before launching a training run.
:::

## Summary

You can now design a convolutional stack and estimate its cost before implementation.

1. Compute output shapes from kernel, stride and padding.
2. Compute parameter counts and multiply-accumulates for a layer.
3. Choose pooling, strided convolution or global pooling for a stated purpose.
4. Use 1x1 bottlenecks and depthwise separable convolutions to control cost.
5. Read a graph by tracing spatial and channel dimensions.
