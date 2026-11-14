---
lesson_id: "benchmarking-and-ablation"
course_id: "research-practice"
lang: "en"
order_index: 3
title: "Benchmarking and Ablation"
description: "What a benchmark measures, how it is gamed, and how to design an evaluation that survives deployment."
meta_title: "Benchmarking and Ablation - Research Practice"
meta_description: "Critique computer vision benchmarks: dataset bias, leakage, metric choice, leaderboard overfitting, OOD evaluation and ablation design."
meta_keywords: "benchmark, dataset bias, leakage, leaderboard, out-of-distribution, ablation study, evaluation protocol"
---

A benchmark is a proxy for a capability. When the proxy is good, progress on it tends to produce real capability. When it is narrow, the field can optimise the proxy while the capability stagnates. Knowing which situation you are in is a research skill.

## What a benchmark encodes

Every benchmark encodes a task definition, a data distribution, a labelling policy and a metric. ImageNet encodes "assign one of 1000 noun categories to a centred object photograph". COCO encodes "detect and segment common objects in natural scenes". Cityscapes encodes "drive in German cities in daylight".

Each choice excludes something: unusual viewpoints, rare classes, night scenes, non-Western contexts, small objects, ambiguous labels. A model's benchmark score is a statement about that encoded distribution, not about vision in general.

The label policy matters as much as the images. If annotators label only the most salient object, a model that detects other correct objects is penalised. If annotators disagree, the metric has an irreducible noise floor. Reporting inter-annotator agreement makes that floor visible.

:::single-choice{#benchmark-proxy} What does a high score on a benchmark establish?

::option[Performance on the specific distribution, task definition and metric encoded by that benchmark]{#benchmark-scope .correct explanation="The score is a measurement under the benchmark's conditions; generalisation beyond them is a separate empirical question."}
::option[General visual competence across all conditions]{#benchmark-general explanation="Breadth is not implied by a single benchmark; it must be tested across distributions."}
::option[That the model is safe to deploy]{#benchmark-safety explanation="Deployment safety depends on failure costs, monitoring and the operational distribution, none of which the benchmark measures."}
:::

## Leakage and contamination

Leakage occurs when information from the test set influences training. Obvious forms include duplicate images across splits and labels derived from test metadata. Subtle forms include hyperparameter selection on the test set, prompt tuning on test examples, and pretraining on data that overlaps the benchmark.

Contamination is rampant in web-scale pretraining. A model may have seen benchmark images, captions or near-duplicates during pretraining. Detecting this requires deduplication against the benchmark and, ideally, held-out evaluation on data collected after the model's training cutoff.

Leaderboard overfitting is a related failure. When many teams iterate against the same test server, the test set becomes a validation set in practice. The reported best score is optimistic for the underlying capability, even if no one cheated.

:::single-choice{#leakage} A team tunes hyperparameters using the official test server and reports the best configuration. What is the problem?

::option[The test set has effectively become a validation set, so the reported score is optimistically biased]{#leaderboard-overfit .correct explanation="Repeated selection against the test metric overfits to its idiosyncrasies, inflating the estimate of generalisation."}
::option[Nothing; using the test server is the intended workflow]{#intended-workflow explanation="The intended workflow separates validation selection from a single test evaluation; repeated test queries violate that separation."}
::option[It reduces the variance of the estimate, which is desirable]{#variance-reduction explanation="It may reduce apparent variance but introduces selection bias, which is worse than noise."}
:::

## Metric choice

Accuracy, mAP, mIoU, FID and their variants encode different priorities. A metric is a value judgement: it says which errors matter and how much.

Accuracy weights all images equally. If a rare class is operationally critical, macro-averaged accuracy or per-class recall is more appropriate. mAP rewards both localisation and classification, with the IoU threshold setting how much localisation matters. mIoU weights classes equally, which is why it exposes failures on small classes.

Threshold-free metrics are not always better. A deployment has an operating point, chosen from a precision-recall trade-off based on the cost of false positives and false negatives. Reporting only the area under the curve hides the operating point that will actually be used.

:::single-choice{#metric-values} Why is the choice of metric a value judgement?

::option[Because it determines which errors are counted and how heavily, encoding priorities about harm and usefulness]{#metric-values .correct explanation="Different metrics weight false positives, false negatives and localisation quality differently, which reflects what the application cares about."}
::option[Because metrics are mathematically equivalent]{#metric-equivalent explanation="Different metrics produce different rankings; they are not equivalent."}
::option[Because all metrics are equally easy to compute]{#metric-cost explanation="Computational cost varies, but the substantive issue is what the metric values."}
:::

## Out-of-distribution evaluation

In-distribution accuracy does not predict robustness to distribution shift. Standard practice now includes:

- **Corruption benchmarks** such as ImageNet-C, which applies controlled noise, blur and weather.
- **Adversarial sets** that are visually similar but semantically altered.
- **Natural distribution shifts** such as sketches, paintings, cartoons and video-game renders.
- **Geographic and demographic shifts** that expose dataset bias.

A method that improves in-distribution accuracy may worsen robustness. Reporting both is the minimum; reporting the relationship between them is better. A small accuracy drop under shift can be acceptable if the model degrades gracefully, while a confident wrong prediction can be worse than an abstention.

:::single-choice{#ood-reporting} Why is in-distribution accuracy insufficient to characterise a vision model?

::option[Because deployment distributions differ from the benchmark, and models can degrade sharply under shift]{#ood-gap .correct explanation="Robustness is a separate property; a model can be accurate in-distribution and fragile under realistic distribution change."}
::option[Because in-distribution accuracy is always overestimated]{#ood-always explanation="It can be a valid estimate for that distribution; the issue is that the deployment distribution is different."}
::option[Because out-of-distribution data is easy to collect]{#ood-easy explanation="OOD data is often harder to collect and label, which is part of why it is underreported."}
:::

## Designing an evaluation

A credible evaluation states the question first, then chooses the data and metric to answer it. A typical structure:

1. **Claim.** What capability is being measured?
2. **Distributions.** In-distribution, shifted, adversarial and subgroup splits.
3. **Metrics.** Primary metric, secondary diagnostics, and the operating point.
4. **Baselines.** Strong, equally tuned, compute-matched.
5. **Variance.** Multiple seeds or folds, with intervals.
6. **Ablation.** One factor at a time, with a mechanism-focused intervention.
7. **Failure analysis.** A labelled sample of errors, with categories.

The failure analysis is often the most informative part and the most commonly omitted. Counting errors by type reveals whether a gain comes from fixing a real weakness or from exploiting a benchmark quirk.

:::callout{type="insight" title="Ablate the mechanism, not just the module"}
Removing a module shows that it helps. Intervening on its alleged mechanism — zeroing the attention map, shuffling the retrieved evidence, replacing the learned prior with a constant — shows why. The second is stronger evidence and is often more revealing when it fails.
:::

## Summary

You can now critique and design benchmarks rather than merely report scores.

1. State what a benchmark's distribution, labels and metric include and exclude.
2. Detect leakage, contamination and leaderboard overfitting.
3. Justify a metric in terms of the errors the application cares about.
4. Evaluate under distribution shift and report the operating point.
5. Structure an evaluation with baselines, variance, ablations and failure analysis.
