---
lesson_id: "open-problems"
course_id: "responsible-vision"
lang: "en"
order_index: 3
title: "Open Problems and How to Contribute"
description: "Where the field is genuinely stuck, which problems are measurement problems, and how to choose work that matters."
meta_title: "Open Problems in Computer Vision - Responsible Vision"
meta_description: "Survey open problems in computer vision: evaluation, 3D and video understanding, efficiency, data engines, world models and research strategy."
meta_keywords: "open problems computer vision, evaluation, world models, video understanding, data engine, research directions"
---

The field is not short of papers; it is short of reliable measurements and robust systems. The most valuable contributions often look unglamorous: a better benchmark, a careful failure analysis, a reproducible baseline, or a system that works under real constraints.

## Evaluation is the bottleneck

Benchmarks saturate. When top-1 accuracy differences shrink to fractions of a percent, the measurement noise and the benchmark's idiosyncrasies dominate. The community response has been to build harder benchmarks, but harder benchmarks are still proxies, and they are vulnerable to the same contamination and overfitting pressures.

What is under-developed:

- Evaluation under realistic distribution shift, with documented collection conditions.
- Metrics that reflect downstream costs rather than aggregate accuracy.
- Statistical protocols that account for multiple comparisons and leaderboard selection.
- Contamination detection for web-scale pretraining.
- Evaluation of composed systems, where errors propagate across components.

A researcher who builds a benchmark that isolates a real capability, with careful controls and a documented collection process, contributes more than another architecture that improves a saturated metric.

:::single-choice{#saturation} Why does benchmark saturation change what constitutes a useful contribution?

::option[Because small metric differences become dominated by noise and benchmark idiosyncrasies, so better measurement matters more than another marginal model]{#saturation-measurement .correct explanation="When the signal is near the noise floor, improving the measurement or the task definition produces more reliable knowledge than optimising the same proxy."}
::option[Because saturated benchmarks are useless and should be abandoned]{#abandon-benchmarks explanation="Saturated benchmarks still provide a common reference; the issue is that they no longer discriminate well."}
::option[Because accuracy no longer matters]{#accuracy-irrelevant explanation="Accuracy matters, but the measured differences may not be meaningful without better protocol and uncertainty quantification."}
:::

## 3D, video and embodied vision

Images are a projection; video adds time; embodiment adds action. Each extension introduces structure that current models handle imperfectly.

**3D** requires consistent geometry across views. Neural fields and Gaussian splatting have made novel view synthesis impressive, but metric reconstruction, dynamic scenes and unobserved regions remain hard. Pose estimation without markers, in the wild, is still fragile.

**Video** requires temporal reasoning: object permanence, causal ordering, action boundaries and long-range dependencies. Frame-level models miss these; video transformers are expensive; benchmarks often reward single-frame cues.

**Embodied vision** closes the loop between perception and action. A robot must perceive, plan and act under uncertainty, with a body that constrains what can be seen and done. Simulation-to-reality transfer, active perception and failure recovery are open problems.

:::single-choice{#embodied-gap} What makes embodied vision harder than passive image recognition?

::option[Because perception is coupled to action, and the agent must decide where to look and what to do under uncertainty]{#embodied-loop .correct explanation="The agent influences its observations and bears the consequences of errors, which adds planning, exploration and safety to perception."}
::option[Because embodied systems use different neural networks]{#embodied-arch explanation="Architectures overlap; the difficulty is the closed perception-action loop and its constraints."}
::option[Because robots cannot use cameras]{#embodied-cameras explanation="Robots use cameras extensively; the challenge is not sensor availability."}
:::

## Data engines and supervision

Model progress has been driven by data as much as architecture. The next bottleneck is building data engines: systems that collect, curate, label and evaluate data continuously, with quality control and provenance.

Relevant problems include:

- **Active learning**: which examples are most informative to label?
- **Weak and noisy supervision**: how to learn from captions, hashtags and click logs without inheriting their biases?
- **Synthetic data**: when does simulation help, and when does it teach artefacts?
- **Long-tail curation**: how to find and label rare but important cases?
- **Data attribution**: which training examples influenced a prediction, and what should be removed?

Data work is often undervalued in academic incentives, which is precisely why careful, well-documented datasets have outsized impact.

## Efficiency and sustainability

Compute is concentrated, energy is costly, and deployment is increasingly on constrained devices. Efficient vision is not only about mobile phones: it is about making research reproducible for labs without large clusters and making models runnable in low-resource settings.

Open problems include hardware-aware architecture search, training efficiency, data efficiency, and evaluation of the total environmental cost of a model lifecycle. A model that is 1 percent more accurate but requires a thousand times more compute is a different kind of contribution, and the field's incentives do not always reflect that.

:::single-choice{#efficiency-equity} Why is efficiency also an equity issue in vision research?

::option[Because expensive training and deployment exclude labs and users without large compute budgets]{#efficiency-access .correct explanation="If progress requires enormous compute, participation and deployment are limited to well-resourced actors, which shapes whose problems get solved."}
::option[Because efficient models are always less accurate]{#efficiency-accuracy explanation="Efficiency often trades some accuracy, but many efficient models are competitive; the equity point is about access."}
::option[Because energy use is unrelated to research practice]{#energy-irrelevant explanation="Training and inference consume energy, and the aggregate cost is a material part of the research ecosystem."}
:::

## World models and reasoning

A current frontier is models that learn a predictive model of the world and use it for planning, simulation and counterfactual reasoning. Vision is central because much of the evidence about the world is visual.

Open questions:

- Do current models learn causal structure or only correlations that support prediction?
- How can a model represent uncertainty and know when it does not know?
- Can a model plan in a learned latent space without drifting from reality?
- How should perception and reasoning be coupled: end-to-end, or as separate modules with interfaces?

These are not only architectural questions. They require evaluation that distinguishes genuine reasoning from pattern completion, which brings the discussion back to measurement.

## How to choose a problem

A practical heuristic:

1. **Pick a measurement problem.** If you cannot tell whether a method works, that is the first contribution.
2. **Work on a distribution that matters.** Medical, industrial, agricultural, accessibility and low-resource settings are under-served relative to their importance.
3. **Build a strong baseline.** Reproduce the best existing method before proposing a new one.
4. **Report failures.** A careful failure analysis is more useful than a favourable qualitative figure.
5. **Make it reproducible.** Release code, configs, seeds and evaluation scripts.
6. **Ask who is affected.** If the system makes decisions about people, the evaluation must include them.

:::callout{type="insight" title="The compounding advantage"}
Reproducible baselines, clean datasets and honest evaluations compound. They are used by everyone who follows, and they make every subsequent claim checkable. A small, careful contribution to measurement often outlasts a large, fragile contribution to a leaderboard.
:::

## Summary

You can now identify where the field is genuinely open and how to contribute credibly.

1. Recognise benchmark saturation and the value of better measurement.
2. Describe the open problems in 3D, video and embodied vision.
3. Explain data-engine challenges from active learning to attribution.
4. Connect efficiency to access and sustainability.
5. Choose research problems by measurement value, impact and reproducibility.
