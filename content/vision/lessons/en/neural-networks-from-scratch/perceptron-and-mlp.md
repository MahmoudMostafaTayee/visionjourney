---
lesson_id: "perceptron-and-mlp"
course_id: "neural-networks-from-scratch"
lang: "en"
order_index: 1
title: "Perceptrons and Multilayer Networks"
description: "From a linear threshold unit to a universal function approximator: activation functions, capacity and why depth helps."
meta_title: "Perceptrons and Multilayer Networks - Neural Networks from Scratch"
meta_description: "Learn the perceptron, activation functions, multilayer perceptrons, universal approximation and why hidden layers change what is representable."
meta_keywords: "perceptron, multilayer perceptron, activation function, universal approximation, ReLU, softmax"
---

The perceptron is the smallest learning machine: a weighted sum followed by a threshold. Its limits were famous before neural networks were practical, and the fix — stacking units with nonlinear activations — is still the core idea behind every modern vision model.

## The linear unit

A perceptron computes $y = \sigma(w^\top x + b)$ with a step function for $\sigma$. Geometrically, it places a hyperplane in input space and assigns a side to each class. Training adjusts the plane when a point is misclassified.

The linear unit is a powerful baseline and a useful diagnostic. If a linear model performs nearly as well as a deep network on your task, either the task is easy or the features are already informative. If it fails completely, the task requires interaction terms or nonlinear structure.

A logistic regression is the smooth version: $\sigma$ becomes the sigmoid and the loss becomes cross-entropy. The decision boundary is still linear, but the output is a probability and the gradient is well defined, which makes optimisation straightforward.

:::single-choice{#perceptron-limit} What can a single linear unit not represent?

::option[Any function whose classes are not linearly separable, such as XOR]{#linear-limit .correct explanation="A single hyperplane can separate only linearly separable sets; XOR requires at least two boundaries or a nonlinear feature."}
::option[Any binary classification task]{#linear-binary explanation="Many binary tasks are linearly separable, and the unit handles those."}
::option[Probabilities, because it outputs a hard decision]{#linear-probability explanation="The logistic version outputs probabilities; the limitation in question is representational, not probabilistic."}
:::

## Hidden layers and activations

Compose two linear maps and you get another linear map: $W_2(W_1 x) = (W_2 W_1)x$. Without a nonlinearity, depth collapses. The activation function is what makes the composition strictly more expressive.

Historically, sigmoid and tanh dominated. Both saturate: for large positive or negative inputs their derivative approaches zero, so gradients vanish in deep stacks. ReLU, $\max(0, x)$, avoids saturation on the positive side and has a constant derivative of one there, which made training deep networks practical. Its variants — LeakyReLU, ELU, GELU, SiLU — smooth or adjust the negative region.

GELU is the default in transformers, defined as $x \cdot \Phi(x)$ where $\Phi$ is the standard normal CDF. It behaves like a smooth ReLU and has become standard in vision transformers and modern convolutional blocks.

:::single-choice{#activation-role} Why does stacking linear layers without activations not increase representational power?

::option[Because the composition of linear maps is itself a linear map]{#linear-compose .correct explanation="Matrix multiplication is associative, so any stack of linear layers without nonlinearity collapses to a single matrix."}
::option[Because linear layers cannot have biases]{#linear-bias explanation="Biases shift the map but do not change its linearity."}
::option[Because gradients cannot flow through matrix multiplication]{#linear-gradient explanation="Gradients flow fine through linear layers; the problem is expressive power, not optimisation."}
:::

## Universal approximation and what it does not promise

The universal approximation theorem states that a network with a single hidden layer of sufficient width can approximate any continuous function on a compact domain to arbitrary accuracy. This is often cited as justification for neural networks, but it says nothing about:

- how many units are needed (the width may be exponential in input dimension),
- whether gradient descent will find the approximating weights,
- whether the approximation generalises beyond the training set.

Depth helps with the first point. Certain functions are representable with exponentially fewer parameters when composed hierarchically than when approximated by a shallow sum. Vision is a natural example: edges compose into textures, textures into parts, parts into objects.

:::single-choice{#uat-limits} What does the universal approximation theorem guarantee?

::option[That a wide enough one-hidden-layer network can approximate any continuous function on a compact domain]{#uat-existence .correct explanation="It is an existence result about representational capacity, with no claim about learnability, sample efficiency or generalisation."}
::option[That gradient descent will find the global optimum]{#uat-optimisation explanation="The theorem is about existence of weights, not about whether training discovers them."}
::option[That deeper networks always generalise better]{#uat-depth explanation="Depth can improve parameter efficiency, but the theorem makes no generalisation claim."}
:::

## Output layers and losses

The output layer encodes the task. For mutually exclusive classes, softmax converts logits into a probability distribution:

$$p_i = \frac{\exp(z_i)}{\sum_j \exp(z_j)}$$

Cross-entropy loss, $-\log p_y$, then penalises the negative log-probability of the correct class. The combination has the clean gradient $p - y$ derived in the previous course, which is why frameworks pair them in a single fused operation.

For multi-label tasks, each output is an independent sigmoid with binary cross-entropy. For regression, the output is linear and the loss is usually squared error. Choosing the wrong pairing — softmax with squared error, or a sigmoid for mutually exclusive classes — produces slow or unstable training rather than an outright error.

The softmax temperature controls the sharpness of the distribution. A temperature above one softens it, which is used in distillation and calibration; below one sharpens it. Logit normalisation matters because softmax is invariant to adding a constant to all logits.

:::single-choice{#softmax-pairing} Why is softmax paired with cross-entropy rather than with squared error?

::option[Because the combination yields a well-conditioned gradient and stable probabilities]{#softmax-ce .correct explanation="Cross-entropy's logarithm cancels softmax's exponential in the derivative, giving p minus y instead of a vanishing product."}
::option[Because squared error cannot be used with probability outputs]{#softmax-squared explanation="It can be used, but it produces small gradients when the model is confidently wrong, slowing learning."}
::option[Because softmax outputs are not differentiable]{#softmax-diff explanation="Softmax is differentiable; the issue is gradient quality, not differentiability."}
:::

## A minimal forward pass

A two-layer classifier in NumPy is short enough to read completely:

```python
import numpy as np

def forward(x, W1, b1, W2, b2):
    h = np.maximum(0, x @ W1 + b1)   # ReLU hidden layer
    z = h @ W2 + b2                  # logits
    z = z - z.max(axis=1, keepdims=True)  # stabilise softmax
    logp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return h, z, logp
```

The stabilisation step subtracts the maximum logit before exponentiation. Softmax is invariant to this shift, but without it large logits overflow to infinity. Every production implementation does the same thing, which is why you should never write the naive version.

The shapes tell the story. If `x` is $N \times D$, then `W1` is $D \times H$, `h` is $N \times H$, `W2` is $H \times C$, and `logp` is $N \times C$. Parameter count is $DH + H + HC + C$, which is why the first layer dominates for image-sized inputs.

:::callout{type="warning" title="Check the shapes before the math"}
A silent broadcasting error can make a network train to a plausible but wrong loss. Print shapes at the input, after each layer, and at the loss. This takes seconds and prevents days of confusion.
:::

## Summary

You can now construct a multilayer classifier and explain each design choice.

1. Explain the geometric limit of a single linear unit.
2. Justify the necessity of nonlinear activations and choose among ReLU variants.
3. State what universal approximation does and does not guarantee.
4. Pair output layers with losses correctly and implement a numerically stable softmax.
