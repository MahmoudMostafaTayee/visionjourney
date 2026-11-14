---
lesson_id: "calculus-and-autodiff"
course_id: "math-for-vision"
lang: "en"
order_index: 2
title: "Calculus and Automatic Differentiation"
description: "Jacobians, the chain rule, reverse-mode differentiation and the exact gradient computations behind a training step."
meta_title: "Calculus and Automatic Differentiation - Mathematics for Vision"
meta_description: "Learn Jacobians, the chain rule, forward and reverse mode automatic differentiation, and how autograd computes vision model gradients."
meta_keywords: "automatic differentiation, backpropagation, Jacobian, chain rule, reverse-mode, gradient checking"
---

Training a vision model means adjusting millions of parameters to reduce a scalar loss. The only practical way to know which direction to move is to compute the gradient of that loss with respect to every parameter. Automatic differentiation does this exactly, and understanding its mechanics is what separates tuning from debugging.

## Derivatives in many dimensions

For a scalar function of a vector, the gradient $\nabla f(x)$ collects the partial derivatives and points in the direction of steepest increase. For a vector-valued function $f: \mathbb{R}^n \to \mathbb{R}^m$, the derivative is the Jacobian $J \in \mathbb{R}^{m \times n}$ with entries $J_{ij} = \partial f_i / \partial x_j$.

The chain rule composes Jacobians: if $y = f(x)$ and $z = g(y)$, then

$$\frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} \frac{\partial y}{\partial x}$$

In deep networks the composition has hundreds of factors. Multiplying full Jacobians explicitly is infeasible; the key observation is that we never need the full matrix, only its product with a vector.

:::single-choice{#jacobian-size} Why is it impractical to form the full Jacobian of a deep network's output with respect to its parameters?

::option[Because Jacobians are only defined for scalar functions]{#jacobian-scalar explanation="Jacobians are defined for vector-valued functions; the issue is size, not definition."}
::option[Because its dimensions are output dimension times parameter count, which is enormous]{#jacobian-huge .correct explanation="For millions of parameters and high-dimensional outputs, storing that dense matrix is prohibitive, while vector-Jacobian products are cheap."}
::option[Because automatic differentiation cannot compute Jacobians]{#jacobian-autodiff explanation="Autodiff can compute Jacobian-vector and vector-Jacobian products; the full matrix is simply too large to materialise."}
:::

## Forward and reverse mode

Automatic differentiation evaluates derivatives by applying the chain rule to the sequence of primitive operations recorded in a computational graph. There are two directions.

**Forward mode** propagates derivatives from inputs to outputs. For each input direction, it computes a Jacobian-vector product at roughly the cost of one forward pass. It is efficient when there are few inputs and many outputs.

**Reverse mode** propagates from the scalar loss back to the inputs, computing vector-Jacobian products. One backward pass yields the gradient with respect to all parameters at about twice the cost of the forward pass. Since training has one scalar output and many parameters, reverse mode — backpropagation — is the right choice.

The asymmetry is the whole reason deep learning is computationally feasible. Forward mode would require one pass per parameter; reverse mode requires one pass total.

:::single-choice{#reverse-mode} Why is reverse-mode differentiation the standard for training neural networks?

::option[Because it computes all parameter gradients in one backward pass, independent of parameter count]{#reverse-efficient .correct explanation="Reverse mode's cost scales with the number of outputs, and training has a scalar loss, so a single sweep suffices."}
::option[Because it is more numerically accurate than forward mode]{#reverse-accuracy explanation="Both modes compute the same derivatives to similar precision; the difference is cost."}
::option[Because it avoids the chain rule]{#reverse-no-chain explanation="Reverse mode is an efficient application of the chain rule, not a way to avoid it."}
:::

## The graph and the vector-Jacobian product

Each primitive operation defines a local derivative. For $z = x \cdot y$, the local derivatives are $\partial z/\partial x = y$ and $\partial z/\partial y = x$. During the backward pass, an incoming gradient $\bar z$ is multiplied by these local derivatives and accumulated into the inputs:

$$\bar x \mathrel{+}= \bar z \cdot y, \qquad \bar y \mathrel{+}= \bar z \cdot x$$

Accumulation with `+=` matters because a tensor can feed multiple downstream operations; its gradient is the sum of the contributions along every path. This is the multivariable chain rule, and forgetting it is a common source of hand-derived gradient errors.

For a dense layer $y = Wx + b$ with upstream gradient $\bar y$, the gradients are $\bar W = \bar y x^\top$, $\bar x = W^\top \bar y$ and $\bar b = \bar y$. For a batch, these become matrix products with the batch dimension summed. Convolution's backward pass is a convolution with flipped kernels, which is why frameworks can implement it as another convolution call.

The softmax plus cross-entropy pair is worth memorising. For logits $z$, softmax probabilities $p$, and true class $c$, the gradient with respect to the logits is simply

$$\frac{\partial L}{\partial z} = p - y$$

where $y$ is the one-hot target. This clean form is why the combination is numerically and computationally preferred over applying a generic loss to probabilities.

:::single-choice{#softmax-gradient} For softmax followed by cross-entropy, what is the gradient with respect to the logits?

::option[The probability vector minus the one-hot target]{#softmax-grad .correct explanation="The Jacobian of softmax cancels the logarithm's derivative, leaving p minus y, which is cheap and numerically stable."}
::option[The log of the probability vector]{#softmax-log explanation="That would be an unstable and incorrect expression; the cancellation removes the logarithm."}
::option[The one-hot target divided by the probability]{#softmax-divide explanation="That resembles a naive derivative of the log but does not account for softmax's Jacobian."}
:::

## Gradient checking and numerical stability

Before trusting a custom layer, compare its analytic gradient to a finite-difference estimate:

$$\frac{\partial L}{\partial \theta_i} \approx \frac{L(\theta + \epsilon e_i) - L(\theta - \epsilon e_i)}{2\epsilon}$$

Use central differences and float64. The relative error should be around $10^{-7}$ for a correct implementation; larger errors indicate a bug or a numerical issue. The check is slow and is usually run on a small input, which is exactly the right trade-off.

Numerical stability is a separate concern. Probabilities can underflow, logarithms of zero diverge, and sums of many terms can lose precision. Frameworks provide log-sum-exp and stable cross-entropy implementations; use them rather than composing primitives by hand.

:::callout{type="insight" title="Know what autograd stores"}
Reverse mode requires the intermediate activations from the forward pass. That is why training memory scales with depth and batch size, and why gradient checkpointing trades compute for memory by recomputing activations during the backward pass.
:::

## Summary

You can now explain how gradients are computed and verify them when something is wrong.

1. Distinguish a Jacobian from the vector-Jacobian products actually computed.
2. Explain why reverse mode costs one pass regardless of parameter count.
3. Accumulate gradients correctly across multiple paths in a graph.
4. Recall the softmax cross-entropy gradient and the convolution backward rule.
5. Use central differences in float64 to check a custom gradient.
