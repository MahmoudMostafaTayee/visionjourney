---
lesson_id: "receptive-fields-and-design"
course_id: "convolutional-networks"
lang: "en"
order_index: 3
title: "Receptive Fields and Architectural Bias"
description: "How far a unit can see, why stride changes the field exponentially, and what convolutional priors buy and cost."
meta_title: "Receptive Fields and Architectural Bias - Convolutional Networks"
meta_description: "Compute receptive fields and effective receptive fields, and understand the inductive biases of convolution versus attention."
meta_keywords: "receptive field, effective receptive field, translation equivariance, inductive bias, convolution design"
---

A convolutional unit does not see the whole image. It sees a patch whose size is determined by the kernel sizes and strides before it. That patch is the receptive field, and it sets a hard limit on what the unit can represent.

## Computing the receptive field

Start with a field of one pixel and a jump of one. For each layer with kernel size $k$ and stride $s$:

$$r \leftarrow r + (k - 1) \cdot j, \qquad j \leftarrow j \cdot s$$

where $r$ is the receptive field and $j$ is the jump, the distance in input pixels between adjacent output positions. For a stack of 3x3 convolutions with stride one, the field grows linearly: after $L$ layers, $r = 1 + 2L$.

Introducing stride changes the growth rate. After a stride-two layer, the jump doubles, so each subsequent kernel covers twice as much input. This is why a ResNet with four downsampling stages has a receptive field of hundreds of pixels despite using only 3x3 kernels.

The output size at the same time shrinks: $H_{\text{out}} = \lfloor (H - k)/s \rfloor + 1$. Resolution and field are traded against each other, and the trade is the central design tension in dense prediction.

:::single-choice{#rf-growth} Three stacked 3x3 convolutions with stride one produce what receptive field?

::option[7x7, because each additional 3x3 layer extends the field by two pixels on each side]{#rf-seven .correct explanation="Starting at 1, each 3x3 layer adds 2, giving 7 after three layers, equivalent to a single 7x7 kernel but with fewer parameters."}
::option[9x9, because three layers of size three multiply]{#rf-nine explanation="Receptive fields add along the path; they do not multiply by the kernel size."}
::option[3x3, because the kernel size does not change]{#rf-three explanation="The effective field accumulates across layers even when each kernel is 3x3."}
:::

:::demo{id="receptive"} Receptive field calculator
Adjust depth, kernel size and stride. The highlighted square is the input region that one output unit depends on. Watch how stride multiplies the jump and makes the field grow much faster than depth alone.
:::

## Effective versus theoretical receptive field

The theoretical receptive field is the full set of input pixels that can influence a unit. The effective receptive field is the region that actually does influence it, weighted by gradient magnitude. Empirically, the effective field is much smaller than the theoretical one and is roughly Gaussian, concentrated near the centre.

This distinction matters. A network may in principle integrate context from the whole image, but in practice its predictions may depend mostly on a local patch. Methods that need long-range context — scene classification, global object relations — cannot assume the field is used merely because it exists.

Attention addresses this directly by allowing every position to interact with every other in one layer. The cost is quadratic in the number of tokens, which is why vision transformers use patch embeddings and windowed attention at high resolution.

:::single-choice{#effective-rf} Why is the effective receptive field usually smaller than the theoretical one?

::option[Because gradient contributions decay with distance, so distant pixels influence the output weakly]{#effective-decay .correct explanation="Repeated convolution and nonlinearity attenuate the influence of far-away inputs, concentrating sensitivity near the centre."}
::option[Because the theoretical field is computed incorrectly]{#effective-formula explanation="The theoretical formula is correct for the dependency graph; the difference is in the magnitude of influence."}
::option[Because pooling removes the outer pixels]{#effective-pooling explanation="Pooling changes resolution but does not by itself explain the gradient-weighting effect."}
:::

## What convolution assumes

A convolution hard-codes three priors:

- **Locality** — nearby pixels are more related than distant ones.
- **Translation equivariance** — a shifted input produces a shifted feature map.
- **Weight sharing** — the same pattern detector is useful everywhere.

These priors are correct for textures, edges and object parts, and they make CNNs sample-efficient. They are wrong for tasks where global position carries meaning, such as detecting that an object is centred, or where a pattern only makes sense in a specific spatial arrangement.

Attention replaces the locality prior with content-based routing, and replaces weight sharing with position-dependent projections. It is more flexible and needs more data to learn the invariances that convolution gets for free. This is the trade-off at the heart of the CNN-versus-transformer debate, and it explains why hybrid models and strong augmentation are common.

:::single-choice{#conv-prior} What does translation equivariance mean for a convolutional layer?

::option[A shift of the input produces a corresponding shift of the output feature map]{#equivariance .correct explanation="Because the same kernel is applied at every position, translating the input translates the response rather than changing it."}
::option[The output is unchanged by any input transformation]{#invariance explanation="That is invariance, a stronger property achieved later by pooling or global aggregation."}
::option[The layer can only detect objects at the image centre]{#centre-bias explanation="Convolution applies everywhere; the prior is locality and sharing, not a centre preference."}
:::

## Designing for a task

For classification, a large receptive field at the final stage is desirable, and global pooling removes the need for precise spatial alignment. For dense prediction, resolution must be preserved, so architectures use dilated convolutions, encoder-decoder skips or feature pyramids to combine large fields with fine detail.

Dilated convolution inserts gaps in the kernel, increasing the field without reducing resolution. A 3x3 kernel with dilation two covers a 5x5 area with nine weights. Stacking dilations at increasing rates produces exponential field growth with linear parameter cost, which is the basis of atrous spatial pyramid pooling.

For small objects, the constraint is different: the object must occupy enough pixels after downsampling. A feature stride of 32 means an object smaller than 32 pixels may vanish entirely. Detection architectures therefore use high-resolution feature levels, and augmentation must preserve small-object scale.

:::callout{type="insight" title="Match the field to the evidence"}
Ask what evidence a prediction requires. A texture classifier needs a local patch; a scene classifier needs global layout; a detector needs both. Then check whether the architecture's field and resolution can actually deliver that evidence.
:::

## Summary

You can now compute receptive fields and reason about architectural priors.

1. Apply the receptive field recurrence for depth, kernel and stride.
2. Distinguish theoretical from effective receptive field.
3. State the locality, equivariance and sharing priors of convolution.
4. Choose dilation, skips or attention to match the evidence a task needs.
