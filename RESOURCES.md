# Resources & references

This is the reading list behind the curriculum. It is curated rather than scraped: each entry is something the lessons actually rely on. Links point to the original authors; nothing here is mirrored.

> **Provenance.** The structure of this list was cross-checked against four public collections: [developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) (machine-learning, MLOps and AI red-teaming tracks), [free-programming-books](https://github.com/EbookFoundation/free-programming-books) (books and courses), [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (from-scratch implementations) and [awesome-computer-vision](https://github.com/jbhuang0604/awesome-computer-vision). The annotations and grouping are original to Vision Journey.

## Books

- **Richard Szeliski**, *Computer Vision: Algorithms and Applications*, 2nd edition — the broadest modern textbook, with a free PDF from the author. Start here for geometry and image processing.
- **Simon Prince**, *Understanding Deep Learning* — free, rigorous and unusually clear on the probabilistic and optimisation ideas behind modern models.
- **David Forsyth & Jean Ponce**, *Computer Vision: A Modern Approach* — the classical feature-and-geometry canon.
- **Hartley & Zisserman**, *Multiple View Geometry in Computer Vision* — the reference for projective geometry, calibration and reconstruction.
- **Goodfellow, Bengio & Courville**, *Deep Learning* — dated in places, still the best treatment of the fundamentals.
- **Gonzalez & Woods**, *Digital Image Processing* — the standard for filtering, morphology and radiometry.
- **Shalev-Shwartz & Ben-David**, *Understanding Machine Learning* — learning theory for when you need to know what a generalisation bound actually says.
- **Kevin Murphy**, *Probabilistic Machine Learning* — a reference for the probabilistic framing that generative vision depends on.
- **Programming Computer Vision with Python** — a free draft applying the classical pipeline in code, listed in free-programming-books.

## Courses and lectures

- **Stanford CS231n**, *Convolutional Neural Networks for Visual Recognition* — course notes remain the clearest single explanation of the deep-vision stack.
- **First Principles of Computer Vision** (Shree Nayar, Columbia) — exceptional derivations of the classical material, from radiometry to stereo.
- **Michigan EECS 498-007 / 598-005**, *Deep Learning for Computer Vision* (Justin Johnson) — implementation-first lectures on backpropagation, CNNs and detection.
- **Hugging Face Community Computer Vision Course** — free, modern, and strong on transformers and multimodal models; listed in free-programming-books.
- **fast.ai**, *Practical Deep Learning for Coders* — top-down, code-first introduction; useful for building intuition before theory.
- **NVIDIA Deep Learning Institute** self-paced courses — practical GPU and deployment material, listed in free-programming-books.
- **OpenCV and PyTorch official tutorials** — the reference for API behaviour, especially preprocessing and export.

## Primary papers, in the order the curriculum meets them

**Foundations**

- Roberts (1963), *Machine Perception of Three-Dimensional Solids*.
- Marr & Hildreth (1980), *Theory of Edge Detection*.
- Lucas & Kanade (1981), *An Iterative Image Registration Technique with an Application to Stereo Vision*.
- Canny (1986), *A Computational Approach to Edge Detection*.
- Harris & Stephens (1988), *A Combined Corner and Edge Detector*.
- Otsu (1979), *A Threshold Selection Method from Gray-Level Histograms*.
- Shi & Tomasi (1994), *Good Features to Track*.
- Lowe (2004), *Distinctive Image Features from Scale-Invariant Keypoints*.
- Viola & Jones (2001), *Rapid Object Detection using a Boosted Cascade of Simple Features*.
- Dalal & Triggs (2005), *Histograms of Oriented Gradients for Human Detection*.
- Zhang (2000), *A Flexible New Technique for Camera Calibration*.

**Deep vision**

- LeCun et al. (1998), *Gradient-Based Learning Applied to Document Recognition*.
- Deng et al. (2009), *ImageNet: A Large-Scale Hierarchical Image Database*.
- Krizhevsky, Sutskever & Hinton (2012), *ImageNet Classification with Deep Convolutional Neural Networks*.
- Simonyan & Zisserman (2015), *Very Deep Convolutional Networks for Large-Scale Image Recognition*.
- Szegedy et al. (2015), *Going Deeper with Convolutions*.
- He et al. (2016), *Deep Residual Learning for Image Recognition*.
- Ioffe & Szegedy (2015), *Batch Normalization*.
- Long, Shelhamer & Darrell (2015), *Fully Convolutional Networks for Semantic Segmentation*.
- Ronneberger, Fischer & Brox (2015), *U-Net: Convolutional Networks for Biomedical Image Segmentation*.
- Ren et al. (2015), *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*.
- Redmon et al. (2016), *You Only Look Once: Unified, Real-Time Object Detection*.
- Lin et al. (2017), *Focal Loss for Dense Object Detection*.
- He et al. (2017), *Mask R-CNN*.
- Carion et al. (2020), *End-to-End Object Detection with Transformers*.

**Representation learning and generative models**

- Vaswani et al. (2017), *Attention Is All You Need*.
- Dosovitskiy et al. (2021), *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*.
- Liu et al. (2021), *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*.
- Chen et al. (2020), *A Simple Framework for Contrastive Learning of Visual Representations* (SimCLR).
- He et al. (2020), *Momentum Contrast for Unsupervised Visual Representation Learning* (MoCo).
- Grill et al. (2020), *Bootstrap Your Own Latent* (BYOL).
- Caron et al. (2021), *Emerging Properties in Self-Supervised Vision Transformers* (DINO).
- He et al. (2022), *Masked Autoencoders Are Scalable Vision Learners*.
- Radford et al. (2021), *Learning Transferable Visual Models From Natural Language Supervision* (CLIP).
- Oquab et al. (2024), *DINOv2: Learning Robust Visual Features without Supervision*.
- Kingma & Welling (2014), *Auto-Encoding Variational Bayes*.
- Goodfellow et al. (2014), *Generative Adversarial Networks*.
- Arjovsky, Chintala & Bottou (2017), *Wasserstein GAN*.
- Ho, Jain & Abbeel (2020), *Denoising Diffusion Probabilistic Models*.
- Song et al. (2021), *Score-Based Generative Modeling through Stochastic Differential Equations*.
- Rombach et al. (2022), *High-Resolution Image Synthesis with Latent Diffusion Models*.
- Mildenhall et al. (2020), *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*.
- Kerbl et al. (2023), *3D Gaussian Splatting for Real-Time Radiance Field Rendering*.
- Kirillov et al. (2023), *Segment Anything*.

**Robustness and evaluation**

- Szegedy et al. (2014), *Intriguing Properties of Neural Networks*.
- Goodfellow, Shlens & Szegedy (2015), *Explaining and Harnessing Adversarial Examples*.
- Madry et al. (2018), *Towards Deep Learning Models Resistant to Adversarial Attacks*.
- Hendrycks & Dietterich (2019), *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*.
- Selvaraju et al. (2017), *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization*.
- Sundararajan, Taly & Yan (2017), *Axiomatic Attribution for Deep Networks*.
- Gebru et al. (2021), *Datasheets for Datasets*.
- Mitchell et al. (2019), *Model Cards for Model Reporting*.

## Datasets and benchmarks

| Dataset | What it is for | Note |
|---|---|---|
| MNIST, CIFAR-10/100 | Small-object classification baselines | Fast to train; saturated, so use them for debugging not claims |
| ImageNet (ILSVRC) | Large-scale classification | The historical driver of the deep era; check for pretraining contamination |
| Pascal VOC, COCO | Detection and segmentation | COCO's AP averaging over IoU thresholds is the modern default |
| ADE20K, Cityscapes | Semantic segmentation | Scene and driving domains respectively |
| LVIS, Open Images, Objects365 | Long-tail and large-vocabulary detection | Useful for measuring rare-class behaviour |
| KITTI, nuScenes | Autonomous driving, 3D perception | Calibrated multi-sensor data |
| ScanNet, DTU, Mip-NeRF 360 | 3D reconstruction and novel view synthesis | Common NeRF and splatting benchmarks |
| ImageNet-C, ImageNet-A, ImageNet-R, ImageNet-Sketch | Corruption, adversarial, rendition and sketch shift | Report alongside in-distribution accuracy |
| Waterbirds, CelebA | Spurious correlation and attribute bias | Use with care; the latter has well-documented ethical issues |
| CheXpert, Camelyon17, ISIC | Medical imaging | Domain shift and label noise are central, not incidental |
| LAION-5B and web-scraped corpora | Vision-language pretraining | Large, unfiltered and ethically contested; provenance is a requirement |

Dataset licences differ and often do not cover biometric processing or surveillance. Check the terms before training on people.

## Tooling

**Training and models** — PyTorch, torchvision, timm, Detectron2, MMDetection, Ultralytics YOLO, Kornia, Albumentations, scikit-image, OpenCV.

**Export and inspection** — ONNX, ONNX Runtime, TensorRT, TFLite, Core ML, [Netron](https://netron.app) (open source, by Lutz Roeder).

**3D** — COLMAP, Open3D, nerfstudio, gsplat.

**Data and experiments** — FiftyOne, DVC, Hydra, Weights & Biases or MLflow, FAISS for embedding search.

**Deployment** — ONNX Runtime, TensorRT, Triton Inference Server, TorchServe, mobile runtimes.

## Lists and communities

- [awesome-computer-vision](https://github.com/jbhuang0604/awesome-computer-vision) — papers, datasets and code by subfield.
- [awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning) — broad tooling index, linked from the awesome list.
- [developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) — visual roadmaps for ML, MLOps and AI engineering.
- [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) — from-scratch neural network implementations in many languages.
- [Papers with Code](https://paperswithcode.com) historically linked papers to implementations; verify availability before relying on it.
- Venues: CVPR, ICCV, ECCV (vision); NeurIPS, ICML, ICLR (learning); SIGGRAPH (graphics and 3D). Read the reviews and reproducibility checklists, not only the abstracts.

## A note on link rot

Resources move. If a link is dead, search the title and author rather than the URL; most of these are archived in several places. Contributions that replace a dead link with a stable one are welcome — see CONTRIBUTING.md in the repository.
