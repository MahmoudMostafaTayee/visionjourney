---
lesson_id: "optimization-and-gradient-descent"
course_id: "math-for-vision"
lang: "en"
order_index: 3
title: "Optimisation and Gradient Descent"
description: "Loss surfaces, conditioning, momentum, adaptive methods and the schedules that make deep vision models converge."
meta_title: "Optimisation and Gradient Descent - Mathematics for Vision"
meta_description: "Learn gradient descent, momentum, Adam, learning-rate schedules, conditioning and regularisation for training computer vision models."
meta_keywords: "gradient descent, SGD, momentum, Adam, learning rate schedule, conditioning, loss landscape"
---

A trained model is the solution of an optimisation problem. The problem is high-dimensional, stochastic and non-convex, yet the same handful of algorithms work across vision, language and speech. Understanding why requires separating what is proved from what is empirically true.

## The objective

Training minimises an empirical risk

$$\theta^\star = \arg\min_\theta \frac{1}{n}\sum_{i=1}^{n} \ell(f_\theta(x_i), y_i) + \lambda R(\theta)$$

The first term measures fit to the data; the regulariser $R$ encodes prior beliefs about which solutions are plausible. For a convolutional network, $R$ is often weight decay, which penalises large weights and improves generalisation.

In practice the sum is approximated by a minibatch, producing a stochastic gradient. The gradient is unbiased if minibatches are sampled uniformly, but it is noisy, so the optimisation path is a random walk around the descent direction rather than a smooth curve.

:::single-choice{#empirical-risk} What does the regularisation term in the training objective encode?

::option[A prior preference over parameters that discourages complex or extreme solutions]{#reg-prior .correct explanation="The penalty expresses a belief about which explanations are plausible before seeing the data, trading training fit for generalisation."}
::option[The variance of the minibatch gradient]{#reg-variance explanation="Gradient noise is a property of stochastic sampling, not of the explicit penalty term."}
::option[A constraint that guarantees convexity]{#reg-convexity explanation="Most regularisers do not make a deep network's loss convex; they shape the solution within a non-convex landscape."}
:::

## Gradient descent and conditioning

The basic update is $\theta \leftarrow \theta - \eta \nabla L(\theta)$, with learning rate $\eta$. For a quadratic loss with Hessian $H$, convergence requires $\eta < 2/\lambda_{\max}$, and the rate depends on the condition number $\lambda_{\max}/\lambda_{\min}$.

An ill-conditioned problem produces a characteristic zig-zag: the gradient points steeply across a narrow valley and only slightly along it, so progress along the valley is slow. Vision losses are extremely ill-conditioned, with curvature ratios spanning many orders of magnitude. This is why plain gradient descent is rarely used at scale.

Momentum addresses the geometry by accumulating a velocity:

$$v \leftarrow \beta v - \eta \nabla L(\theta), \qquad \theta \leftarrow \theta + v$$

Consistent directions reinforce, oscillating directions cancel. The effective step size along a flat direction grows, and the method behaves like a heavy ball rolling through the valley. Nesterov momentum evaluates the gradient at the look-ahead point, which often improves stability.

:::single-choice{#momentum-effect} Why does momentum help on an ill-conditioned loss surface?

::option[It averages out gradient noise and amplifies consistent directions across iterations]{#momentum-average .correct explanation="Velocities accumulate along directions that repeatedly agree, while rapidly alternating components cancel, reducing zig-zag."}
::option[It makes the Hessian diagonal]{#momentum-hessian explanation="Momentum changes the iteration, not the curvature of the loss."}
::option[It guarantees convergence to the global minimum]{#momentum-global explanation="No first-order method guarantees a global minimum on a non-convex landscape."}
:::

:::demo{id="optimizer"} Gradient descent on an anisotropic valley
The contours are elongated, so curvature differs sharply by direction. Compare plain SGD with momentum, then increase the learning rate until the iterates overshoot. The path is the optimisation, not an abstraction.
:::

## Adaptive methods

Adam maintains per-parameter estimates of the first and second moments of the gradient and normalises the update by the second moment:

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \qquad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$

$$\theta_t = \theta_{t-1} - \eta \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}$$

The normalisation makes the effective step size roughly independent of gradient magnitude, which helps when different layers receive gradients of very different scales. Adam is a strong default for transformers and for rapid prototyping.

It is not universally better. Well-tuned SGD with momentum often generalises slightly better on convolutional vision benchmarks, and Adam's adaptive denominator can interact badly with weight decay unless decoupled, as in AdamW. The practical rule: use AdamW for transformers and fast experiments, SGD with momentum for long convolutional training runs where the last fraction of a percent matters.

:::single-choice{#adam-normalisation} What does Adam's division by the square root of the second moment do?

::option[It rescales each parameter's step by its recent gradient magnitude, making steps roughly scale-invariant]{#adam-scale .correct explanation="Parameters with consistently large gradients receive smaller steps, and rarely active parameters receive larger ones."}
::option[It removes the need to choose a learning rate]{#adam-no-lr explanation="Adam still has a base learning rate; the adaptation changes relative scaling, not the overall budget."}
::option[It guarantees the update direction is the true gradient direction]{#adam-direction explanation="The update is a normalised, momentum-smoothed estimate, not the exact gradient."}
:::

## Schedules, warmup and batch size

The learning rate is usually the most consequential hyperparameter. Large rates speed early progress but can destabilise; small rates converge slowly and may stall in flat regions. Standard schedules include step decay, cosine annealing and one-cycle policies.

Warmup — starting with a very small rate and increasing over the first few hundred or thousand iterations — is essential for transformers and large batches, because early gradients are large and the adaptive estimates are unreliable.

Batch size and learning rate are coupled. The linear scaling rule suggests multiplying the rate by the batch-size ratio, up to a limit; beyond it, warmup and layer-wise adaptive rates are needed. Large batches reduce gradient noise, which can hurt generalisation unless the schedule is lengthened to compensate.

:::single-choice{#warmup-reason} Why do large transformer training runs use a learning-rate warmup?

::option[To avoid unstable early updates while adaptive moment estimates and activations are still poorly scaled]{#warmup-stability .correct explanation="Early gradients are large and second-moment estimates unreliable, so a small initial rate prevents divergence."}
::option[To reduce the total number of training steps]{#warmup-steps explanation="Warmup adds steps; its purpose is stability, not speed."}
::option[To make the loss convex near the origin]{#warmup-convexity explanation="Warmup does not change the geometry of the loss, only the step sizes taken."}
:::

## Non-convexity, saddle points and what actually matters

Deep losses are non-convex, with many local minima, saddle points and flat regions. Classical worst-case guarantees do not apply. Empirically, however, over-parameterised networks have few bad local minima: most critical points encountered are saddles or flat regions, and stochastic noise helps escape them.

What matters more than reaching a global minimum is finding a solution with good generalisation. Flat minima — regions where the loss is insensitive to parameter perturbation — tend to generalise better, which motivates sharpness-aware methods and large-batch training recipes. This remains an active research area rather than settled theory.

:::callout{type="warning" title="Do not tune the learning rate last"}
Practitioners often treat the learning rate as a final tweak. It interacts with batch size, architecture depth, normalisation and augmentation. Tune it early, on a small run, and revisit it whenever any of those change.
:::

## Summary

You can now reason about the optimisation process rather than treating it as a black box.

1. Write the regularised empirical risk and explain each term.
2. Relate conditioning and momentum to the zig-zag behaviour of gradient descent.
3. Explain what Adam normalises and when SGD with momentum is preferable.
4. Design a warmup and schedule that matches batch size.
5. Recognise why non-convexity is not the obstacle it appears to be.
