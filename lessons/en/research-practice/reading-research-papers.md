---
lesson_id: "reading-research-papers"
course_id: "research-practice"
lang: "en"
order_index: 1
title: "Reading Research Papers"
description: "The three-pass method, how to read an ablation table, and how to tell what a paper actually claims from what its abstract implies."
meta_title: "Reading Research Papers - Research Practice"
meta_description: "Learn the three-pass paper reading method, how to interpret ablations and baselines, and how to evaluate computer vision research claims."
meta_keywords: "how to read a paper, three-pass method, ablation table, baseline, research claims, CVPR"
---

A vision paper is an argument, not an instruction manual. Its abstract states a claim, its method proposes a mechanism, and its experiments are evidence. Reading well means reconstructing the argument and asking whether the evidence supports it.

## The three-pass method

The first pass is a scan, taking five to ten minutes. Read the title, abstract, figures, table captions and conclusion. Answer: what problem, what claim, what evidence, and is it relevant to me? Most papers stop here, and that is correct — most are not relevant to your current question.

The second pass is an hour. Read the introduction, method and experiments, but skip derivations and appendices. Mark terms you do not understand and unstated assumptions. Answer: what exactly is new, what baselines were compared, and what is the strongest result? At the end, you should be able to summarise the paper to a colleague in three sentences.

The third pass is a day or more, for papers you intend to build on. Reconstruct the method from scratch, check the derivations, look for the code, and attempt a partial reproduction. At this depth you are looking for the gap between the described method and what the code actually does.

:::single-choice{#first-pass} What is the goal of the first pass over a paper?

::option[To decide quickly whether the paper is relevant enough to read further]{#first-pass-goal .correct explanation="A scan of the abstract, figures and conclusion is a triage step, filtering the literature before spending hours on a method."}
::option[To reproduce the experiments]{#first-pass-repro explanation="Reproduction requires the third pass and access to code and data."}
::option[To memorise every equation]{#first-pass-equations explanation="The first pass deliberately skips derivations; detail is reserved for later passes."}
:::

## Reading the claims precisely

Vision papers often make several distinct claims that get conflated in citation:

- **Existence**: a method can achieve a result under some conditions.
- **Comparison**: it is better than baseline B on benchmark D by margin M.
- **Generality**: it works across datasets, resolutions and architectures.
- **Mechanism**: the improvement is caused by the proposed component.

Only the first two are usually directly demonstrated. Generality requires multiple datasets and settings. Mechanism requires an ablation that isolates the component from confounders such as extra parameters, longer training or additional data.

When a paper says "our method improves accuracy by 3 points", ask: improved over what, trained for how long, with how much data, and at what compute? A method that adds parameters and trains longer may improve simply because it is larger.

:::single-choice{#claim-mechanism} A paper adds a new attention module and reports higher accuracy, but the module also adds 20 percent more parameters. What is missing to support the mechanism claim?

::option[An ablation controlling for parameter count and training budget]{#ablation-control .correct explanation="Without matching capacity and compute, the gain could come from the extra parameters rather than the proposed mechanism."}
::option[A larger test set]{#larger-test explanation="Test-set size affects precision of the estimate, not whether the mechanism is responsible."}
::option[A different backbone]{#different-backbone explanation="A different backbone tests generality, not the causal attribution of the gain."}
:::

## Reading an ablation table

An ablation table removes or varies components to attribute performance. A good table changes one factor at a time and holds everything else fixed. A weak table changes several factors together, which makes attribution impossible.

Look for:

- **Matched budgets.** Same epochs, same augmentation, same data, same compute.
- **Matched capacity.** Parameter counts reported next to accuracy.
- **Seed variance.** At least a few runs, or a stated reason why variance is negligible.
- **Incremental rows.** Each row adds one component, so the marginal contribution is visible.
- **A strong baseline.** The comparison should include a well-tuned simple method, not only the authors' previous work.

Ablations are often run at smaller scale for cost reasons. That is acceptable if the authors verify that the ranking holds at full scale, but it is a limitation worth noting.

:::single-choice{#ablation-quality} Which ablation design best supports a causal claim about a new loss term?

::option[Same architecture, data, schedule and compute, with only the loss term toggled]{#ablation-isolate .correct explanation="Holding all other factors constant isolates the loss as the only difference, which is what a causal claim requires."}
::option[The new loss plus a larger backbone plus longer training]{#ablation-confounded explanation="Multiple simultaneous changes make it impossible to attribute the gain to the loss."}
::option[The new loss evaluated on a different dataset than the baseline]{#ablation-dataset explanation="Changing the dataset as well confounds the comparison and prevents a clean attribution."}
:::

## Figures as evidence

Figures often carry the real argument. A qualitative comparison should show failures as well as successes; a paper that shows only favourable examples is selecting evidence. A plot of accuracy versus compute is more informative than a single operating point, because it reveals whether a method is genuinely more efficient or merely larger.

Attention maps and saliency visualisations are particularly prone to overinterpretation. They show where a model looked, not why it decided. Prefer ablations that intervene on the alleged mechanism: if removing the attended region does not change the prediction, the attention map is not the explanation.

:::callout{type="warning" title="Beware the cherry-picked figure"}
A single striking qualitative result is an existence proof, not a characterisation. Look for the failure cases, the per-class breakdown and the conditions under which the method was not evaluated.
:::

## Keeping up without drowning

The literature is too large to read exhaustively. A workable strategy:

1. Follow a small set of venues and labs rather than the whole arXiv firehose.
2. Maintain a question-driven reading list: read papers that bear on a specific problem you are working on.
3. Read surveys for maps, then primary sources for the claims you rely on.
4. Read the reviews and rebuttals for high-profile submissions; they often reveal the weaknesses faster than the paper does.
5. Reproduce one result per quarter. Nothing exposes the gap between description and implementation like running the code.

## Summary

You can now read a vision paper as an argument with evidence rather than as a set of claims to accept.

1. Apply the three-pass method and stop early when a paper is not relevant.
2. Separate existence, comparison, generality and mechanism claims.
3. Evaluate an ablation table for matched budgets and capacity.
4. Treat figures and attention maps as selected evidence.
