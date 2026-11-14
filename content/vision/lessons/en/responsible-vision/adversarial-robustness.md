---
lesson_id: "adversarial-robustness"
course_id: "responsible-vision"
lang: "en"
order_index: 1
title: "Adversarial Robustness"
description: "FGSM, PGD, threat models, transfer attacks and the defenses that survive scrutiny."
meta_title: "Adversarial Robustness - Responsible Vision"
meta_description: "Learn adversarial examples, FGSM and PGD attacks, threat models, transferability, adversarial training and certified robustness."
meta_keywords: "adversarial examples, FGSM, PGD, adversarial training, robust accuracy, certified robustness, threat model"
---

A small, carefully chosen perturbation can change a confident prediction while remaining invisible to a human. This is not a curiosity about one model; it is a property of the geometry of learned decision boundaries, and it matters wherever perception controls a decision.

## Threat models

A robustness claim is meaningless without a threat model. The standard specification is:

- **Perturbation norm**: how the change is measured, usually $\ell_\infty$ or $\ell_2$.
- **Budget**: the maximum allowed change, for example $\epsilon = 8/255$ for 8-bit images.
- **Access**: white-box (gradients available), black-box (only outputs) or transfer (a surrogate model).
- **Goal**: targeted (force a specific class), untargeted (any wrong class), or a downstream objective.

An $\ell_\infty$ budget bounds each pixel's change; an $\ell_2$ budget bounds total change. An attack that succeeds under one norm may fail under another. Reporting "robust" without these parameters is not a claim that can be evaluated.

:::single-choice{#threat-model} Why is a robustness result meaningless without a threat model?

::option[Because robustness is defined relative to allowed perturbations and attacker capabilities]{#threat-definition .correct explanation="Without specifying the norm, budget, access and goal, there is no well-defined set of perturbations the claim covers."}
::option[Because all attacks are equally strong]{#attacks-equal explanation="Attacks differ substantially in strength and assumptions; the budget and access determine which are applicable."}
::option[Because robustness is a property of the dataset only]{#robust-dataset explanation="Robustness depends on the model, the distribution and the admissible perturbations, not the dataset alone."}
:::

## Fast gradient sign method

The simplest attack linearises the loss and takes a step in the sign of the gradient:

$$x_{\text{adv}} = x + \epsilon \cdot \operatorname{sign}\left(\nabla_x \mathcal{L}(f(x), y)\right)$$

For an $\ell_\infty$ budget, the sign step is optimal for a first-order approximation. It is cheap: one backward pass. It is also weak, because the linear approximation is only valid locally.

FGSM illustrates the mechanism. The model's decision boundary is close to the data in some direction, and the gradient identifies that direction. High-dimensional inputs make it easy to find a small change that crosses the boundary, because there are many directions to choose from.

:::single-choice{#fgsm-step} Why does FGSM use the sign of the gradient rather than the gradient itself?

::option[Because under an L-infinity budget, the optimal first-order perturbation puts the full budget into each coordinate with the sign of the gradient]{#fgsm-sign .correct explanation="Maximising a linear function subject to a box constraint gives a corner solution, which is the sign step."}
::option[Because the gradient magnitude is unreliable]{#fgsm-magnitude explanation="The magnitude is meaningful, but the constraint makes the corner solution optimal for the linear approximation."}
::option[Because sign makes the perturbation larger than the budget]{#fgsm-budget explanation="The sign step is scaled by epsilon, so it respects the budget by construction."}
:::

## Projected gradient descent

PGD iterates the FGSM step and projects back onto the allowed set after each iteration:

$$x^{t+1} = \Pi_{\mathcal{B}(x, \epsilon)}\left(x^t + \alpha \cdot \operatorname{sign}\left(\nabla_x \mathcal{L}(f(x^t), y)\right)\right)$$

With random initialisation and enough iterations, PGD is a strong first-order attack and is the standard baseline for evaluating adversarial training. A model that resists PGD at a given budget is considered robust against first-order white-box attacks at that budget, though not against all possible attacks.

The projection depends on the norm. For $\ell_\infty$ it clips each coordinate; for $\ell_2$ it scales the perturbation vector; for other norms it requires a corresponding projection. The step size and iteration count are part of the attack specification and must be reported.

:::single-choice{#pgd-projection} What does the projection step in PGD enforce?

::option[That the perturbed image remains within the allowed norm ball around the original]{#pgd-ball .correct explanation="Iterative steps can leave the feasible set, so projection returns the point to the budget-constrained region."}
::option[That the perturbation is imperceptible to humans]{#pgd-perceptual explanation="The budget is a proxy for imperceptibility, not a guarantee; projection enforces the specified norm constraint."}
::option[That the attack remains targeted]{#pgd-target explanation="The target is set by the loss; projection only enforces the perturbation constraint."}
:::

## Transferability and black-box attacks

Adversarial examples often transfer between models trained on the same task. An attacker can generate perturbations on a surrogate model and apply them to an unknown target. Transfer is stronger when models share architecture, training data or preprocessing, and weaker across very different models.

Query-based black-box attacks estimate gradients from output probabilities or use decision-based methods that only need the predicted label. These require many queries, which can be detected or rate-limited, but they demonstrate that hiding gradients is not a defence.

Physical-world attacks add another layer: printed patches, projected light or modified objects that survive camera capture, viewpoint changes and compression. These are harder to construct but more relevant to security than pixel-level perturbations.

:::single-choice{#transfer-attack} What makes an adversarial perturbation more likely to transfer to an unknown model?

::option[Similar training data, architecture or preprocessing between the surrogate and the target]{#transfer-similarity .correct explanation="Transfer exploits shared features and decision structure, which are more similar when models are trained similarly."}
::option[A larger perturbation budget than the threat model allows]{#transfer-budget explanation="Exceeding the budget changes the threat model and does not explain transfer within it."}
::option[Using a targeted rather than untargeted attack]{#transfer-target explanation="Targeted attacks are generally harder to transfer because they require a specific output class."}
:::

## Defences and what they actually achieve

Adversarial training is the most reliable empirical defence. It augments each batch with adversarial examples and trains on them, which flattens and expands the decision boundary near the data. It is expensive, because generating attacks multiplies training cost, and it typically reduces clean accuracy.

Certified defences provide a guarantee: for a given input, they certify that no perturbation within a radius changes the prediction. Randomized smoothing is the most scalable approach, training a classifier on noisy inputs and certifying a radius around each prediction. The guarantee is strong but the certified radius may be small, and the base classifier is smoothed rather than the original.

Many proposed defences were later broken because they relied on obfuscated gradients. Gradient masking, stochastic preprocessing and non-differentiable components can make an attack fail without making the model robust. The standard test is to evaluate with a strong adaptive attack that accounts for the defence.

:::single-choice{#gradient-masking} A defence makes gradients unavailable to the attacker. Why is this not sufficient evidence of robustness?

::option[Because adaptive attacks can use transfer, queries or differentiable approximations to bypass the masking]{#masking-bypass .correct explanation="Obfuscation raises the cost of attack but does not remove the vulnerability; adaptive evaluation often recovers near-original attack success."}
::option[Because gradients are never useful to attackers]{#gradients-useless explanation="Gradients are the basis of the strongest first-order attacks, which is why masking them is attempted."}
::option[Because the model becomes undifferentiable and therefore safe]{#undifferentiable-safe explanation="Non-differentiability does not imply robustness; it can be approximated or circumvented."}
:::

## Reporting robust accuracy

Robust accuracy is measured under a specified attack. Report the attack, its budget, its iterations, its random restarts and whether it is white-box or transfer. An unexplained robust accuracy number is not comparable to another.

Also report clean accuracy and the trade-off. Adversarial training usually lowers clean accuracy; a defence that preserves both is valuable, and one that sacrifices clean performance for a marginal robustness gain may not be worth deploying.

Finally, distinguish robustness to a norm ball from robustness to real-world corruptions. These are different distributions. A model can be certified against $\ell_\infty$ perturbations and still fail on rain, motion blur or a new camera.

:::callout{type="warning" title="The evaluation is the claim"}
Robustness numbers are only as meaningful as the attack used to produce them. Prefer published, adaptive evaluations and independent replication over self-reported numbers from a new defence. A defence that has not been attacked adaptively has not been tested.
:::

## Summary

You can now evaluate robustness claims and understand the limits of defences.

1. Specify a threat model with norm, budget, access and goal.
2. Explain FGSM and PGD and why PGD is the standard baseline.
3. Describe transfer and query-based black-box attacks.
4. Distinguish empirical from certified robustness.
5. Report robust accuracy with the attack that produced it.
