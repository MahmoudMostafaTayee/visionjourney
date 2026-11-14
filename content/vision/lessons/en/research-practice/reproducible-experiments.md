---
lesson_id: "reproducible-experiments"
course_id: "research-practice"
lang: "en"
order_index: 2
title: "Reproducible Experiments"
description: "Seeds, configs, baselines, error bars and the logging discipline that makes a result trustworthy."
meta_title: "Reproducible Experiments - Research Practice"
meta_description: "Learn reproducible machine learning experiments: seeding, configuration management, baselines, variance, logging and compute accounting."
meta_keywords: "reproducibility, random seed, experiment tracking, baseline, error bars, ablation, compute budget"
---

A result that cannot be reproduced is an anecdote. Reproducibility is not a bureaucratic checkbox; it is the property that lets you distinguish a real effect from noise, a lucky seed or a pipeline bug.

## Sources of nondeterminism

Training a vision model involves randomness at several levels: weight initialisation, data shuffling, augmentation sampling, dropout, and the order of floating-point reductions on parallel hardware. Some of these can be fixed; some cannot be fixed cheaply.

Setting the Python, NumPy and framework seeds makes a run repeatable on the same hardware and software stack. Enabling deterministic algorithms removes some sources of nondeterminism at a performance cost. Full bitwise determinism across GPUs and library versions is usually not achievable, so reproducibility means statistical reproducibility: a rerun lands within the expected variance, not at the same digit.

Document the seeds, the framework version, the CUDA and driver versions, and the hardware. A result that depends on one specific stack is fragile, and knowing that is part of the result.

:::single-choice{#determinism} What does "reproducible" mean in practice for a GPU training run?

::option[An independent rerun reaches a result within the expected run-to-run variance]{#statistical-repro .correct explanation="Bitwise determinism is usually unattainable across hardware and library versions, so reproducibility is a statistical property with documented conditions."}
::option[Every floating-point operation produces an identical bit pattern]{#bitwise-repro explanation="That is bitwise determinism, which is a stronger and often impractical requirement."}
::option[The code runs without errors on a different machine]{#runs-anywhere explanation="Executing successfully is a prerequisite, not evidence that the result reproduces."}
:::

## Configuration as an artefact

Every hyperparameter that affects the result should live in a versioned configuration file, not in scattered constants. The config should record: dataset and split, preprocessing, augmentation policy, model architecture, initialisation, optimiser and schedule, batch size, precision, number of workers, and evaluation protocol.

The config is part of the scientific claim. Two runs that differ in an unrecorded augmentation setting are not comparable, even if the architecture is identical. Tools for experiment tracking help, but the discipline matters more than the tool: a plain YAML file committed alongside the code is often enough.

Avoid mutable defaults and implicit global state. A training script that reads an environment variable to decide the learning rate is reproducible only if the environment is recorded. Prefer explicit arguments with logged defaults.

:::single-choice{#config-role} Why should the full training configuration be versioned with the code?

::option[Because the configuration is part of the experimental claim, and an unrecorded change makes results incomparable]{#config-claim .correct explanation="Results are only comparable when all influential settings are known, so the config must be part of the recorded artefact."}
::option[Because config files make the code run faster]{#config-speed explanation="Configuration management affects reproducibility and clarity, not runtime performance."}
::option[Because frameworks require YAML files]{#config-framework explanation="Most frameworks accept arguments in many forms; the requirement is scientific, not technical."}
:::

## Baselines and controls

A baseline is the result you must beat to claim an improvement. It should be strong, well-tuned and evaluated under the same protocol. Beating a weak baseline is not evidence of progress.

Controls address specific confounds. If a method adds parameters, a parameter-matched baseline is the control. If it trains longer, a longer-trained baseline is the control. If it uses extra data, a baseline trained on the same extra data is the control. Without these, the comparison measures the confound as much as the method.

Report the baseline's tuning effort. A baseline tuned for one setting and a method tuned for ten is not a fair comparison, even if both are reported honestly. The reviewer's question is always: what would this baseline achieve with equal effort?

:::single-choice{#control-confound} A new method adds a branch and reports a 2-point gain. Which baseline best controls for the added capacity?

::option[A baseline with a parameter-matched extra branch that is not the proposed one]{#param-matched .correct explanation="Matching capacity isolates the proposed mechanism from the generic benefit of more parameters."}
::option[The original baseline with fewer parameters]{#original-baseline explanation="That is the unconfounded comparison, but it does not control for the capacity difference."}
::option[A larger version of the new method]{#larger-new explanation="Scaling the method further does not separate capacity from mechanism."}
:::

## Variance and error bars

A single run is a sample. Report mean and standard deviation over multiple seeds, or at least the range. Classification accuracy on a large test set has small binomial variance, but training variance across seeds is often larger than the reported improvement.

Error bars should state what they represent: standard deviation across seeds, standard error of the mean, or a confidence interval. These are different quantities, and conflating them is common. With three seeds, a standard deviation is a crude estimate; with one seed, there is no estimate at all.

For comparisons, a difference of means without a paired test can be misleading. Paired tests across seeds or across dataset folds reduce variance and are more sensitive to real effects. Report the effect size alongside the test result; statistical significance is not practical significance.

:::callout{type="warning" title="The one-seed result"}
A single-seed improvement of one or two points is often within run-to-run variance. Before building on a result, rerun it with different seeds. If the effect disappears, you have saved yourself months.
:::

## Logging and provenance

Log more than the loss. Record learning rate, gradient norm, activation statistics, throughput, memory use and validation metrics at a fixed cadence. When a run fails, these are the traces that explain why.

Log the data pipeline too: dataset version or hash, split definition, number of samples per class, and augmentation parameters. A silent change in the data pipeline can invalidate a comparison more thoroughly than any model change.

Keep artefacts: checkpoints, predictions on the validation set, and the exact evaluation command. A metric is only reproducible if the evaluation code and its inputs are preserved. Saving predictions makes it possible to re-evaluate without retraining, which is invaluable when the metric implementation changes.

:::single-choice{#logging-value} Why save validation predictions alongside model checkpoints?

::option[So metrics can be recomputed and compared without retraining when evaluation code changes]{#save-preds .correct explanation="Predictions are the interface between the model and the metric; preserving them makes re-evaluation cheap and auditable."}
::option[To reduce the checkpoint size]{#pred-size explanation="Saving predictions adds storage; the benefit is auditability, not size reduction."}
::option[Because predictions are needed for training]{#pred-training explanation="Training uses labels and gradients; saved predictions are for evaluation and analysis."}
:::

## Compute accounting

Report the compute used: GPU type, number of devices, wall-clock time and approximate cost. Compute is a hidden variable in comparisons. A method that reaches a result with ten times the compute is a different contribution from one that reaches it with the same budget.

Also report inference cost. A model that is 2 percent more accurate but 5 times slower may be worse for the deployment. Papers increasingly include latency and FLOPs, but the measurement conditions (batch size, precision, hardware, framework) matter and are often omitted.

:::callout{type="insight" title="Reproduction is a spectrum"}
State which parts you reproduced: the architecture, the training recipe, the reported metric, or the claimed mechanism. A partial reproduction that clearly labels what was verified is more useful than an ambiguous claim of success.
:::

## Summary

You can now design experiments that another lab could trust.

1. Distinguish bitwise from statistical reproducibility.
2. Version the full configuration as part of the claim.
3. Design parameter- and compute-matched controls.
4. Report variance correctly and avoid one-seed conclusions.
5. Preserve predictions and report compute and latency.
