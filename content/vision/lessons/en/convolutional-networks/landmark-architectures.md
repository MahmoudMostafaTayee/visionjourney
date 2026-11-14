---
lesson_id: "landmark-architectures"
course_id: "convolutional-networks"
lang: "en"
order_index: 2
title: "Landmark Architectures"
description: "LeNet to EfficientNet: the design ideas, parameter budgets and trade-offs behind the canonical CNN families."
meta_title: "Landmark CNN Architectures - Convolutional Networks"
meta_description: "Compare LeNet, AlexNet, VGG, GoogLeNet, ResNet, DenseNet, MobileNet and EfficientNet, with their design principles and costs."
meta_keywords: "LeNet, AlexNet, VGG, GoogLeNet, ResNet, DenseNet, MobileNet, EfficientNet, architecture design"
---

Architecture history is a sequence of answers to one question: how do you increase capacity without making optimisation or inference impractical? Each family contributed a structural idea that outlived its specific network.

## LeNet and the birth of the template

LeNet-5, developed by LeCun and colleagues in the late 1980s and 1990s, established the template: convolution, nonlinearity, pooling, repeated, followed by fully connected layers. It read handwritten digits at commercial scale.

Its parameter count was tiny by modern standards, and it operated on 32x32 grayscale inputs. The importance is conceptual: local receptive fields, shared weights and spatial subsampling encode the structure of images directly into the architecture.

## AlexNet and VGG: scale and simplicity

AlexNet (2012) kept the template but scaled it: five convolutional layers, three fully connected layers, 60 million parameters, ReLU, dropout and two GPUs. Its victory on ImageNet made the template the default.

VGG (2014) made a different point. Instead of large kernels, it used stacks of 3x3 convolutions. Two 3x3 convolutions have the same receptive field as one 5x5, but fewer parameters and an extra nonlinearity. Three 3x3 layers match a 7x7 receptive field with even better parameter efficiency. VGG's regularity — repeated blocks of 3x3 convolutions followed by pooling — made it easy to reason about and a popular backbone for transfer learning.

The cost was in the classifier. VGG's fully connected layers contained most of its 138 million parameters, which is why later architectures replaced them with global average pooling.

:::single-choice{#vgg-3x3} Why does VGG prefer stacked 3x3 convolutions to a single large kernel with the same receptive field?

::option[Because the stack has fewer parameters and more nonlinearities for the same spatial extent]{#vgg-stack .correct explanation="Two 3x3 layers use 18 weights per channel pair versus 25 for a 5x5, and apply two nonlinearities instead of one."}
::option[Because large kernels cannot be implemented efficiently]{#vgg-kernel-speed explanation="Large kernels are supported; the argument here is parameter efficiency and depth, not implementation limits."}
::option[Because 3x3 convolutions are rotation-invariant]{#vgg-rotation explanation="Neither 3x3 nor 5x5 convolutions are rotation-invariant; the comparison is about cost and depth."}
:::

## GoogLeNet and the inception idea

GoogLeNet (2014) introduced the inception module: parallel branches with different kernel sizes, concatenated along channels. The module lets the network choose its effective scale at each layer rather than committing to one.

To keep cost manageable, each branch begins with a 1x1 bottleneck that reduces channels. The architecture also replaced fully connected layers with global average pooling and used auxiliary classifiers during training to improve gradient flow.

The idea that survived is multi-scale processing within a block. It reappears in feature pyramids, atrous spatial pyramid pooling for segmentation, and multi-branch designs in modern backbones.

## ResNet and the residual revolution

ResNet (2015) addressed the degradation problem: very deep plain networks performed worse in training, not because of overfitting but because optimisation became difficult. The residual block learns $F(x)$ and outputs $F(x) + x$, giving gradients an identity path.

The block design matters. The basic block uses two 3x3 convolutions. The bottleneck block uses 1x1, 3x3, 1x1 with channel expansion, which is more efficient for deep networks. Downsampling blocks use a strided convolution on the shortcut so that dimensions match.

ResNet-50 has about 25 million parameters and roughly 4 billion MACs at 224x224. Its stage structure — stem, four stages with increasing channels and decreasing resolution, global pool, classifier — became the standard vocabulary for backbone design.

:::model{src="resnet-mini"} ResNet-Mini: identity shortcuts as graph edges
Find the Add nodes. Each one merges a residual branch with an identity path. In a full ResNet these repeats are collapsed into stages; here the graph is small enough to trace every edge.
:::

:::single-choice{#resnet-shortcut} In a ResNet downsampling block, why does the shortcut use a 1x1 strided convolution instead of a pure identity?

::option[Because the spatial size and channel count change, so the identity must be projected to match]{#resnet-projection .correct explanation="The residual addition requires equal shapes; a strided 1x1 projection aligns both resolution and channels."}
::option[Because identity connections cannot carry gradients]{#resnet-gradient explanation="Identity connections are precisely what carries gradients well; the projection exists for shape compatibility."}
::option[Because it adds nonlinearity to the shortcut]{#resnet-nonlinearity explanation="The projection is linear; the reason is dimensional matching, not nonlinearity."}
:::

## DenseNet, MobileNet and EfficientNet

DenseNet (2017) connected each layer to all subsequent layers within a block. Feature reuse reduces parameter count, because each layer only needs to add a small number of new channels. The cost is memory: concatenating all previous feature maps requires storing them.

MobileNet (2017) targeted efficiency with depthwise separable convolutions and two simple global hyperparameters that trade width and resolution against latency. MobileNetV2 added inverted residuals and linear bottlenecks; MobileNetV3 incorporated squeeze-and-excitation and neural-architecture search.

EfficientNet (2019) made scaling itself the object of study. Rather than scaling depth, width or resolution independently, compound scaling chooses a joint factor guided by a small grid search. The result was a family that matched or beat much larger networks at a fraction of the FLOPs.

The lesson is that accuracy is not a single-axis function of size. Where you spend parameters and pixels matters as much as how many you spend.

:::single-choice{#compound-scaling} What does compound scaling in EfficientNet do differently from scaling one dimension?

::option[It scales depth, width and input resolution together according to a fixed ratio]{#compound .correct explanation="Joint scaling avoids the diminishing returns of scaling only one axis and was found to be more efficient across model sizes."}
::option[It scales the batch size instead of the model]{#compound-batch explanation="Batch size is a training choice; compound scaling changes model and input dimensions."}
::option[It removes the need for architecture search]{#compound-nas explanation="EfficientNet used architecture search as a starting point and compound scaling on top; it did not eliminate search."}
:::

## What actually transfers

Architectural families differ less than their headline numbers suggest. Almost all modern backbones share: a convolutional stem, hierarchical stages with increasing channels, normalization, nonlinearities, residual or densely connected blocks, global pooling and a linear head.

When choosing a backbone for a new task, the decision is usually about the compute budget and the data regime, not about a decisive architectural advantage. A smaller model trained longer often beats a larger model trained briefly. A model pretrained on a domain closer to the target often beats a bigger model pretrained on a distant one.

:::callout{type="warning" title="Benchmarks are not deployments"}
ImageNet top-1 accuracy is measured at a fixed resolution with a fixed preprocessing pipeline. Your deployment may have different resolution, aspect ratio, class distribution and latency budget. Compare candidates on your own data, at your own operating point.
:::

## Summary

You can now place the major CNN families in a design lineage and choose among them deliberately.

1. Trace the LeNet template through AlexNet and VGG.
2. Explain the multi-scale motivation of inception modules.
3. Explain the residual block and its shape-matching variants.
4. Compare parameter efficiency of DenseNet, MobileNet and EfficientNet.
5. Select a backbone from compute and data constraints rather than leaderboard rank.
