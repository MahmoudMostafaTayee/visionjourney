---
lesson_id: "backpropagation-by-hand"
course_id: "neural-networks-from-scratch"
lang: "en"
order_index: 2
title: "Backpropagation by Hand"
description: "Derive and implement the backward pass of a two-layer network in NumPy, then verify it against finite differences."
meta_title: "Backpropagation by Hand - Neural Networks from Scratch"
meta_description: "Derive backpropagation for an MLP with ReLU and softmax cross-entropy, implement it in NumPy, and verify gradients numerically."
meta_keywords: "backpropagation derivation, numpy neural network, gradient check, softmax cross entropy, chain rule"
---

Backpropagation is reverse-mode automatic differentiation applied to a network. Reading the derivation once, implementing it in a few dozen lines, and checking it numerically builds an intuition that no framework abstraction provides.

## The forward pass

Take a two-layer network for $N$ samples with $D$ inputs, $H$ hidden units and $C$ classes:

$$Z_1 = X W_1 + b_1, \qquad H_1 = \max(0, Z_1)$$
$$Z_2 = H_1 W_2 + b_2, \qquad L = -\frac{1}{N}\sum_{i=1}^{N} \log p_{i,y_i}$$

with $p = \operatorname{softmax}(Z_2)$. The loss is the mean negative log-likelihood of the correct class.

Everything about the backward pass follows from this graph. We need $\partial L/\partial W_1$, $\partial L/\partial b_1$, $\partial L/\partial W_2$ and $\partial L/\partial b_2$.

## The backward pass

Start from the loss. For softmax cross-entropy, the gradient with respect to the logits is

$$\frac{\partial L}{\partial Z_2} = \frac{1}{N}(p - Y)$$

where $Y$ is the one-hot target matrix. This is the single most useful gradient identity in classification.

Then apply the chain rule through the affine layer $Z_2 = H_1 W_2 + b_2$:

$$\frac{\partial L}{\partial W_2} = H_1^\top \frac{\partial L}{\partial Z_2}, \qquad \frac{\partial L}{\partial b_2} = \sum_i \frac{\partial L}{\partial Z_2}[i]$$

The matrix dimensions confirm the formula: $H_1^\top$ is $H \times N$ and the incoming gradient is $N \times C$, producing $H \times C$, which matches $W_2$.

Propagate to the hidden layer:

$$\frac{\partial L}{\partial H_1} = \frac{\partial L}{\partial Z_2} W_2^\top$$

Then through the ReLU, whose derivative is one where the pre-activation was positive and zero elsewhere:

$$\frac{\partial L}{\partial Z_1} = \frac{\partial L}{\partial H_1} \odot \mathbb{1}[Z_1 > 0]$$

Finally the first affine layer:

$$\frac{\partial L}{\partial W_1} = X^\top \frac{\partial L}{\partial Z_1}, \qquad \frac{\partial L}{\partial b_1} = \sum_i \frac{\partial L}{\partial Z_1}[i]$$

:::single-choice{#relu-backward} How does the ReLU backward pass use the forward activation?

::option[It multiplies the incoming gradient by one where the pre-activation was positive and zero elsewhere]{#relu-mask .correct explanation="The derivative of max(0, z) is a mask. The forward sign is cached and reused as that mask."}
::option[It multiplies the incoming gradient by the activation value itself]{#relu-value explanation="That would be the derivative of a different function; ReLU's derivative is a 0/1 mask, not the output."}
::option[It passes the gradient through unchanged everywhere]{#relu-identity explanation="An inactive unit has zero derivative, so its gradient must be zeroed."}
:::

## The implementation

```python
def train_step(X, Y, params, lr=0.1):
    W1, b1, W2, b2 = params
    N = X.shape[0]

    Z1 = X @ W1 + b1
    H1 = np.maximum(0, Z1)
    Z2 = H1 @ W2 + b2

    Z2s = Z2 - Z2.max(axis=1, keepdims=True)
    logp = Z2s - np.log(np.exp(Z2s).sum(axis=1, keepdims=True))
    loss = -logp[np.arange(N), Y.argmax(axis=1)].mean()

    dZ2 = (np.exp(logp) - Y) / N
    dW2 = H1.T @ dZ2
    db2 = dZ2.sum(axis=0)
    dH1 = dZ2 @ W2.T
    dZ1 = dH1 * (Z1 > 0)
    dW1 = X.T @ dZ1
    db1 = dZ1.sum(axis=0)

    params = [W1 - lr * dW1, b1 - lr * db1, W2 - lr * dW2, b2 - lr * db2]
    return loss, params
```

Note that `Z1 > 0` is a boolean array; multiplying by it applies the mask. Note also that the bias gradient sums over the batch, because the bias is shared across samples. Getting either detail wrong produces a network that trains slowly or not at all, without raising an error.

:::single-choice{#bias-gradient} Why is the bias gradient a sum over the batch rather than an average or a matrix product?

::option[Because the same bias is added to every sample, so its gradient accumulates contributions from each]{#bias-sum .correct explanation="The bias has one parameter per output unit; each sample contributes a gradient, and the total derivative is their sum."}
::option[Because biases are not differentiable]{#bias-diff explanation="Biases are linear parameters and are trivially differentiable."}
::option[Because the loss is already averaged over the batch]{#bias-average explanation="The averaging is applied through dZ2; the bias still receives the sum of per-sample contributions, which is consistent with that scaling."}
:::

## Gradient checking

Before trusting the implementation, compare it to finite differences on a tiny input:

```python
def numeric_grad(f, params, idx, eps=1e-6):
    original = params[idx].copy()
    params[idx] = original + eps
    plus = f()
    params[idx] = original - eps
    minus = f()
    params[idx] = original
    return (plus - minus) / (2 * eps)
```

Use float64, a batch of two or three samples, and a handful of parameters. Compare the analytic and numeric gradients with a relative error:

$$\text{rel} = \frac{|g_a - g_n|}{\max(10^{-8}, |g_a| + |g_n|)}$$

A correct implementation gives values around $10^{-7}$ to $10^{-9}$. Values around $10^{-3}$ usually indicate a missing mask or a transposed matrix; values near one indicate a sign or shape error.

:::callout{type="warning" title="Check before you scale"}
Run the gradient check on the smallest possible model and batch. A bug that costs seconds to find at this scale can cost days to find after it has been buried under a training loop, a scheduler and data augmentation.
:::

## What the framework hides

PyTorch builds a graph of tensor operations during the forward pass and records a backward function for each. Calling `loss.backward()` traverses that graph in reverse, applying the vector-Jacobian products and accumulating gradients into `.grad`.

The framework does not change the mathematics. It removes the bookkeeping. The benefit is enormous: you can write new layers in terms of primitives and get correct gradients for free. The cost is that when something is wrong, you must reason about the same chain rule the framework is applying — which is precisely why deriving it by hand once is worth the effort.

:::single-choice{#framework-grad} What does `loss.backward()` actually do?

::option[It traverses the recorded computation graph in reverse, applying local derivatives and accumulating parameter gradients]{#backward-graph .correct explanation="Autograd stores the forward graph and each operation's backward function; backward runs them in reverse topological order."}
::option[It numerically perturbs every parameter to estimate the gradient]{#backward-numeric explanation="That would be finite differencing, which autograd avoids because it is far too slow."}
::option[It recomputes the forward pass with the labels flipped]{#backward-flip explanation="Backward propagation is a separate pass over the stored graph, not a modified forward pass."}
:::

## Summary

You can now derive, implement and verify a complete backward pass.

1. Write the forward pass of a two-layer network with explicit shapes.
2. Derive each gradient using the chain rule and confirm the dimensions.
3. Implement the step in NumPy, including the ReLU mask and bias summation.
4. Verify with central differences and interpret relative error.
