---
lesson_id: "interpretability"
course_id: "model-inspection"
lang: "en"
order_index: 2
title: "Interpretability"
description: "Saliency, Grad-CAM, integrated gradients and the difference between a plausible heatmap and evidence about a model's reasoning."
meta_title: "Interpretability - Model Inspection"
meta_description: "Learn saliency maps, Grad-CAM, integrated gradients, occlusion analysis, probing and how to validate explanations of vision models."
meta_keywords: "Grad-CAM, saliency map, integrated gradients, occlusion, feature visualization, probing, explainable AI"
---

An explanation should change what you believe about a model. Most heatmaps do not. They show where the output is locally sensitive, which is related to but not the same as the reason for a prediction. Learning to tell the difference is the core skill of interpretability.

## Saliency and its limits

The simplest attribution is the gradient of the predicted score with respect to the input:

$$S(x) = \left|\frac{\partial f_c(x)}{\partial x}\right|$$

Large values indicate pixels whose small change would most affect the score. This is a local, first-order sensitivity measure.

It has well-known problems. Gradients are noisy, they can be dominated by high-frequency texture, and they saturate in ReLU networks where the function is locally flat. A model can be confidently correct while its saliency map highlights an irrelevant region, because the gradient reflects sensitivity, not causal use.

Vanilla gradient saliency should be treated as a quick diagnostic, not as an explanation. It is cheap and useful for catching obvious preprocessing bugs, but it is not evidence that the model used a particular feature.

:::single-choice{#saliency-meaning} What does a large value in a gradient saliency map indicate?

::option[That a small change to that pixel would strongly change the output score]{#saliency-sensitivity .correct explanation="The map is a local derivative, so it measures sensitivity rather than the feature the model actually relies on."}
::option[That the pixel was causally necessary for the prediction]{#saliency-causal explanation="Sensitivity is not necessity; a pixel can be sensitive yet unused, or used yet locally flat."}
::option[That the pixel belongs to the predicted object]{#saliency-object explanation="Saliency can highlight background or texture, which is one reason it is unreliable as a segmentation cue."}
:::

## Grad-CAM

Grad-CAM uses the gradients flowing into a convolutional feature map to weight the channels, producing a coarse localisation map:

$$\alpha_k = \frac{1}{Z}\sum_{i,j}\frac{\partial y^c}{\partial A^k_{ij}}, \qquad L^c = \operatorname{ReLU}\left(\sum_k \alpha_k A^k\right)$$

The result is a low-resolution heatmap upsampled to the image. It is class-specific and tends to highlight regions that the model's deeper layers associate with the class.

Grad-CAM is popular because it produces visually plausible maps. That plausibility is also its danger: the map can look like a good explanation while missing the actual evidence. It is coarse by construction, so it cannot distinguish fine-grained cues, and it depends on the choice of layer. Changing the target layer changes the story.

More principled variants include Grad-CAM++ and score-CAM, which address weighting and gradient saturation. None of them solve the fundamental problem that a post-hoc map is not a proof of causal use.

:::single-choice{#gradcam-layer} Why does the choice of layer change a Grad-CAM explanation?

::option[Because different layers encode different levels of abstraction and spatial resolution]{#gradcam-layer .correct explanation="Early layers localise fine detail, deeper layers encode semantics at coarse resolution, so the weighted map differs substantially."}
::option[Because Grad-CAM retrains the model per layer]{#gradcam-retrain explanation="Grad-CAM is post-hoc and does not retrain; the layer choice only changes which activations are weighted."}
::option[Because the gradients are random]{#gradcam-random explanation="Gradients are deterministic for a fixed input and model, though they can be noisy."}
:::

## Integrated gradients and axiomatic attribution

Integrated gradients accumulates gradients along a path from a baseline to the input:

$$\text{IG}_i(x) = (x_i - x'_i)\int_{0}^{1}\frac{\partial f(x' + \alpha(x - x'))}{\partial x_i}\,d\alpha$$

It satisfies two desirable axioms: sensitivity (a feature that changes the output gets nonzero attribution) and implementation invariance (two functionally identical networks get the same attribution). These properties make it more defensible than raw gradients.

The baseline is a modelling choice and a frequent source of criticism. A black image, a blurred image and a random image produce different attributions. The baseline should represent "absence of evidence", which is task-dependent: black is reasonable for some images and meaningless for others.

:::single-choice{#ig-baseline} Why is the baseline choice important in integrated gradients?

::option[Because attribution is defined relative to the baseline, so it determines what counts as absence of evidence]{#ig-baseline .correct explanation="The method attributes the difference between the input and the baseline, so the baseline defines the reference point for the explanation."}
::option[Because the baseline determines the model's weights]{#ig-weights explanation="The model weights are fixed; only the integration path changes."}
::option[Because a nonzero baseline increases accuracy]{#ig-accuracy explanation="Attribution methods do not change the model's predictions."}
:::

## Occlusion and intervention

A more direct approach is to intervene: occlude a region and measure the change in output. If masking the object destroys the prediction, the model was using it. If masking the background changes nothing, the model was not relying on context.

Occlusion is expensive because it requires many forward passes, and it can create out-of-distribution inputs that the model was never trained on. A grey patch or a blurred patch may be more natural than black, but all occlusions are artificial.

The strongest evidence comes from interventions that respect the model's distribution: delete a feature, replace it with a plausible alternative, or counterfactually edit the image. Causal interpretability is harder than attribution, but it is closer to the question people actually care about.

## Probing and representation analysis

Probing trains a simple classifier on intermediate features to test whether a property is linearly decodable. If a probe can predict depth from layer 3 features, those features contain depth information. This does not prove the model uses that information for its task, but it characterises what is represented.

Probes are sensitive to capacity and regularisation. A high-capacity probe can memorise, while a weak probe can miss nonlinear encoding. Report probe architecture and compare against a control trained on shuffled labels.

Feature visualisation, which optimises inputs to maximise a neuron's activation, produces images that reveal what a unit responds to. These images are often aesthetically striking and occasionally misleading, because the optimisation can exploit adversarial directions rather than the unit's role in natural images.

:::single-choice{#probing-limit} What does a successful linear probe on a layer demonstrate?

::option[That the property is linearly decodable from that layer's features]{#probe-decodable .correct explanation="A probe shows information is present and accessible to a linear readout, not that the model uses it for its own prediction."}
::option[That the model's decision depends on the property]{#probe-causal explanation="Decodability is correlational; causal dependence requires an intervention on the property."}
::option[That the layer was trained with supervision for that property]{#probe-supervision explanation="Probes are trained after the fact and do not imply the original model was supervised for the property."}
:::

## Reporting explanations responsibly

An explanation is a claim, and it should be reported like one. State the method, the layer, the baseline, the random-seed variance and the sample size. Show failures, not only flattering examples. Compare against a control, such as a randomly initialised model or a model trained on shuffled labels, to see what a meaningless explanation looks like.

Never present a heatmap as proof that a model is safe or fair. A heatmap on a correct prediction can coexist with a model that relies on a spurious cue, because the map is generated post hoc and may reflect correlated rather than causal structure.

:::callout{type="warning" title="Explanation is not assurance"}
A plausible saliency map is not a safety certificate. For high-stakes deployment, validate behaviour with interventions, subgroup testing, and monitoring on the deployment distribution. Explanations can support an argument; they cannot replace evidence.
:::

## Summary

You can now use attribution methods while distinguishing explanation from evidence.

1. Interpret gradient saliency as local sensitivity, with its limitations.
2. Explain Grad-CAM's channel weighting and layer dependence.
3. State the axioms and baseline sensitivity of integrated gradients.
4. Design occlusion and probing analyses, knowing what each establishes.
5. Report explanations with controls and failure cases.
