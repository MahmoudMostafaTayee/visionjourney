---
lesson_id: "computation-graphs-and-netron"
course_id: "model-inspection"
lang: "en"
order_index: 1
title: "Computation Graphs and Netron"
description: "ONNX as an exchange format, shape inference, export pitfalls, and a workflow for reading a real network graph."
meta_title: "Computation Graphs and Netron - Model Inspection"
meta_description: "Learn ONNX graphs, opsets, shape inference, Netron inspection, export pitfalls, NCHW versus NHWC and how to verify an architecture visually."
meta_keywords: "ONNX, Netron, computation graph, shape inference, opset, model export, NCHW, NHWC"
---

The architecture in a paper is a diagram. The architecture in a deployment is a graph of typed operations with concrete shapes. Exporting between the two is where assumptions become visible, and inspecting the graph is the fastest way to find out what a model actually computes.

## What ONNX represents

ONNX is an open format for machine-learning graphs. A model file contains:

- a graph of nodes, each with an operator type, named inputs and outputs, and attributes;
- initializers, the learned weights, stored as tensors;
- value information, the declared shapes and types of intermediate tensors;
- metadata, including the producer, the opset version and the input/output signature.

The opset version defines which operators and semantics are available. A model exported at opset 17 may use operators that an older runtime does not implement. Checking the opset is the first step when a model fails to load somewhere.

ONNX is an exchange format, not a training format. It captures the forward computation. Training-specific behaviour such as dropout and batch-norm statistics is folded or fixed at export time, which is exactly why export discrepancies appear.

:::single-choice{#onnx-opset} Why can a model work in one runtime and fail in another despite being valid ONNX?

::option[Because the runtimes support different opset versions and operator sets]{#opset-support .correct explanation="The opset defines operator semantics; a runtime that implements an older opset may not support the operators used by the model."}
::option[Because ONNX files are not portable]{#not-portable explanation="ONNX is designed for portability; the limitation is runtime operator coverage, not the format itself."}
::option[Because the weights are stored in a proprietary format]{#proprietary-weights explanation="ONNX stores weights as standard tensors; the issue is graph semantics and runtime support."}
:::

## Shape inference

Shape inference propagates declared input shapes through the graph to compute the shape of every intermediate tensor. It is how the Model Lab viewer knows that a convolution produces a specific channel, height and width.

Static shapes make deployment efficient because memory can be allocated ahead of time. Dynamic shapes, marked with symbolic dimensions, allow variable batch size or resolution at the cost of runtime flexibility. Many export bugs are shape bugs: a reshape assumes a fixed batch size, a flatten hard-codes a spatial dimension, or a transpose permutes the wrong axes.

When inference fails, the error usually identifies the node where consistency broke. Read it literally: it names the tensor and the incompatible dimensions. Then walk backwards to the operation that produced the wrong shape.

:::single-choice{#dynamic-shape} What is the cost of exporting with dynamic spatial dimensions?

::option[The runtime must handle variable shapes, which can prevent some ahead-of-time optimisations]{#dynamic-cost .correct explanation="Static shapes allow memory planning and kernel selection; dynamic dimensions require more flexible, sometimes slower execution paths."}
::option[The model loses accuracy]{#dynamic-accuracy explanation="Dynamic shapes affect execution and optimisation, not the numerical result."}
::option[The weights must be retrained]{#dynamic-retrain explanation="Shape flexibility does not change the learned parameters."}
:::

## Reading the graph

A systematic pass over a graph reveals most architecture errors.

1. **Check the input.** Rank, channel order and value range. A model expecting NCHW will produce wrong results silently if fed NHWC.
2. **Follow the stem.** The first convolution usually reduces resolution and increases channels. Compare against the paper's reported stem.
3. **Count the blocks.** Collapse repeated motifs and count stages. A ResNet-50 should have specific repeat counts per stage; a mismatch means a copy-paste error.
4. **Trace the skips.** Residual and dense connections appear as extra edges. Verify that Add or Concat nodes have the shapes they require.
5. **Check the head.** Global pool, flatten, linear, and the output dimension equal to the number of classes.
6. **Find the parameter-heavy nodes.** The graph viewer shows parameter counts per node; the classifier or the deepest stage usually dominates.

:::model{src="mobilenet-block"} Mobile inverted residual stack
This graph has four inverted residual blocks. Find the depthwise convolution in each: its group attribute equals its channel count, which is what makes it depthwise. Then find the pointwise projections and the residual Adds where the block is not downsampling.
:::

## Export pitfalls

The differences between a training model and an exported graph are a reliable source of production bugs.

**Training/eval mode.** Dropout and batch normalisation behave differently in each. Exporting a model left in training mode produces a graph with stochastic or batch-dependent behaviour. Always call `eval()` before export.

**Folding.** Constant folding and batch-norm folding can change the graph structure. Folding batch norm into a preceding convolution is a standard optimisation, and it removes the normalisation nodes that a reviewer might expect to see. That is fine, but it means the exported graph is not a literal translation of the training code.

**Unsupported operators.** Custom layers may export as a generic operator or fail. Check the graph for nodes with a custom domain; they will not run on a standard runtime.

**Precision.** Exporting in float16 halves the file size and can speed up inference, but it introduces numerical differences. Validate accuracy after conversion, not before.

**Preprocessing.** The exported model usually expects normalised tensors, not raw images. The resize, crop, normalisation and channel order must match training exactly. This is the most common cause of a correct graph producing wrong predictions.

:::single-choice{#eval-mode} Why must a model be in evaluation mode before export?

::option[Because dropout and batch normalisation behave differently in training and inference]{#eval-mode .correct explanation="Training mode uses stochastic dropout and batch statistics; inference mode uses deterministic scaling and running statistics, which is what the exported graph should encode."}
::option[Because evaluation mode removes the weights]{#eval-weights explanation="Evaluation mode does not remove weights; it changes the behaviour of specific layers."}
::option[Because export is only supported for evaluation metrics]{#eval-metrics explanation="Export concerns the forward graph, not the metric computation."}
:::

## Netron as a verification tool

Netron renders ONNX, TFLite, CoreML, TensorFlow and PyTorch files as interactive graphs. Clicking a node shows its attributes, input and output shapes, and the associated weights. The sidebar lists the model's inputs, outputs and metadata.

A practical workflow:

1. Export the model with a fixed dummy input.
2. Open it in Netron and check the input and output signatures.
3. Collapse the graph to the block level and compare with the paper's diagram.
4. Inspect suspicious nodes: reshape, transpose, concat and slice are the usual sources of shape errors.
5. Compare parameter counts against the reported total.
6. Run a numerical parity check between the original framework and the exported model on the same input.

The Model Lab on this site uses the same graph data to render an offline explorer, so you can inspect the exported models even without access to Netron. Both views are useful: Netron shows operator attributes and weights in depth, while the explorer shows the architecture's structure at a glance.

:::callout{type="insight" title="Parity before performance"}
Before profiling or optimising an exported model, verify numerical parity with the source model on a fixed input. A fast model that computes something slightly different is not a valid optimisation. A maximum absolute difference on the order of 1e-5 for float32 is a reasonable starting tolerance.
:::

## Summary

You can now inspect and verify a real vision architecture.

1. Explain what an ONNX graph contains and why opsets matter.
2. Use shape inference and read shape errors.
3. Walk a graph stem to head, checking blocks and skip connections.
4. Avoid the common export pitfalls.
5. Verify parity between source and exported model.
