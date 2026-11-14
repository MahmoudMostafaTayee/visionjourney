---
lesson_id: "tensors-and-linear-algebra"
course_id: "math-for-vision"
lang: "en"
order_index: 1
title: "Tensors and Linear Algebra"
description: "Vectors, matrices, rank, eigendecomposition and the SVD — then PCA and convolution written as linear maps."
meta_title: "Tensors and Linear Algebra for Vision - Mathematics for Vision"
meta_description: "Build the linear algebra used in computer vision: matrix maps, rank, SVD, covariance, PCA and convolution as a linear operator."
meta_keywords: "linear algebra for vision, SVD, PCA, covariance matrix, tensor, einsum, convolution matrix"
---

Every image is a tensor, every geometric transform a matrix, and every learned layer a parameterised map between vector spaces. The vocabulary is not decoration: it tells you which operations are invertible, which directions are well conditioned, and how many degrees of freedom a model really has.

## Vectors, norms and inner products

A vector in $\mathbb{R}^n$ can be read as a point, a displacement, or a feature descriptor. The inner product

$$\langle u, v \rangle = u^\top v = \sum_i u_i v_i$$

measures alignment, and induces the Euclidean norm $\lVert u \rVert_2 = \sqrt{\langle u,u\rangle}$. Cosine similarity normalises that alignment to a scale-free number, which is why embeddings are compared with it.

Different norms encode different notions of size. The $\ell_1$ norm is robust and sparse-inducing through its use as a regulariser; the $\ell_2$ norm is smooth and rotation-invariant; the $\ell_\infty$ norm bounds the worst coordinate. In adversarial robustness these choices become threat models: an $\ell_\infty$ perturbation budget of 8/255 allows every pixel to move slightly, while an $\ell_2$ budget concentrates the change.

Matrix norms describe how a linear map amplifies vectors. The spectral norm is the largest singular value, and it is the natural quantity for bounding how much a layer can stretch its input — the basis of Lipschitz-based robustness arguments.

:::single-choice{#norm-choice} Why is the $\ell_\infty$ norm the usual budget in image adversarial attacks?

::option[Because it bounds the maximum change to any single pixel, matching a per-pixel imperceptibility constraint]{#linf-meaning .correct explanation="An L-infinity budget caps the largest coordinate change, which corresponds directly to a maximum per-pixel intensity shift."}
::option[Because it measures the total number of changed pixels]{#linf-count explanation="That would be an L-zero count. L-infinity bounds magnitude, not sparsity."}
::option[Because it equals the Euclidean length of the perturbation]{#linf-euclid explanation="L-infinity and L-2 coincide only for vectors with a single nonzero component."}
:::

## Matrices as maps

An $m \times n$ matrix $A$ maps $\mathbb{R}^n$ to $\mathbb{R}^m$. Its rank is the dimension of the image; its null space is the set of vectors mapped to zero. A square matrix is invertible exactly when its null space is trivial.

The singular value decomposition writes any matrix as

$$A = U \Sigma V^\top$$

where $U$ and $V$ are orthogonal and $\Sigma$ is diagonal with non-negative singular values sorted by magnitude. Geometrically, the map rotates, scales along orthogonal axes, and rotates again. The condition number $\sigma_{\max}/\sigma_{\min}$ measures how much the map distorts: a large condition number means small input changes can produce large output changes, and linear systems involving $A$ become numerically unstable.

Truncating the SVD to the top $k$ singular values gives the best rank-$k$ approximation in both Frobenius and spectral norm (Eckart–Young). This is the mathematical basis of low-rank compression, including the low-rank adapters used to fine-tune large vision and language models.

:::single-choice{#svd-rank} What does truncating an SVD to the largest k singular values produce?

::option[A random projection that preserves distances approximately]{#svd-random explanation="Random projections are a different construction. Truncated SVD is the optimal deterministic low-rank approximation."}
::option[The best rank-k approximation of the matrix in Frobenius norm]{#svd-best .correct explanation="Eckart–Young states that dropping the smallest singular values minimises reconstruction error among all rank-k matrices."}
::option[An exact inverse of the original matrix]{#svd-inverse explanation="Truncation discards information, so the result is generally not invertible or exact."}
:::

## Covariance, PCA and whitening

Given centred data vectors $x_i \in \mathbb{R}^d$, the covariance matrix is

$$C = \frac{1}{n}\sum_i x_i x_i^\top = \frac{1}{n} X^\top X$$

Its eigenvectors are the principal directions of variation and its eigenvalues are the variances along them. Projecting onto the top $k$ eigenvectors minimises reconstruction error — PCA is truncated SVD of the centred data matrix.

For images, PCA on patches yields basis functions that look like oriented edges and gratings, an early and still instructive result: the statistics of natural images contain the structure that convolutional filters later learned. Whitening rescales the principal axes to unit variance, which removes correlations and often speeds up optimisation, at the cost of amplifying noise in low-variance directions.

:::single-choice{#pca-whitening} What does whitening do to a dataset's covariance matrix?

::option[It makes the covariance the identity by rotating to principal axes and rescaling each variance to one]{#whitening-identity .correct explanation="Whitening combines the PCA rotation with per-axis scaling, removing both correlation and scale differences."}
::option[It makes every feature uniformly distributed]{#whitening-uniform explanation="Whitening equalises second moments, not the full distribution; marginals can remain non-uniform."}
::option[It removes the mean but keeps the covariance unchanged]{#whitening-mean explanation="Removing the mean is centring, which is a separate step performed before whitening."}
:::

## Tensors and index notation

A tensor is a multidimensional array with a shape and an index convention. An image batch in PyTorch has shape $N \times C \times H \times W$; a feature map from a convolution has shape $N \times C' \times H' \times W'$. Getting the index order right is not cosmetic — it determines memory layout, kernel efficiency and whether a reshape preserves meaning.

Einstein notation makes contractions explicit. A batch matrix multiply written as `b i j, b j k -> b i k` states exactly which axis is summed. In NumPy or PyTorch, `einsum` is often clearer and less error-prone than a chain of reshapes and transposes, and it is a good way to check that two implementations agree.

Broadcasting is the other source of subtle bugs. Adding a tensor of shape $C \times 1 \times 1$ to one of shape $N \times C \times H \times W$ applies per-channel bias, which is intended. Accidentally broadcasting over the batch dimension produces a result with the wrong shape and silently wrong semantics.

:::callout{type="warning" title="Shapes are assertions"}
Write down expected shapes as comments or assertions at every stage of a new model. Most implementation bugs in vision are shape bugs that did not raise an error because broadcasting or reshaping made them legal.
:::

## Convolution as a structured matrix

A convolution is linear, so it can be written as a matrix multiply: each output pixel is an inner product between a shifted patch of the input and the kernel. The resulting matrix is sparse, banded and Toeplitz-like, with the same weights repeated at every position.

This view explains parameter sharing precisely. A dense layer between two $H \times W$ images would have $H^2W^2$ weights; a convolution has $k^2$ weights reused at every location. The reduction is not an approximation but a constraint on the linear map, and that constraint encodes translation equivariance.

It also explains the cost. Explicitly forming the Toeplitz matrix is wasteful; practical implementations use implicit GEMM or direct tiling. When you read that a convolution is "just a matrix multiply", the useful content is that it is a highly structured one with exploitable sparsity.

## Summary

You can now express vision operations in the language of linear maps and reason about their structure.

1. Choose a norm appropriate to the error model or threat model.
2. Interpret rank, conditioning and the SVD geometrically.
3. Derive PCA as truncated SVD of a covariance matrix.
4. Use explicit index notation to avoid silent broadcasting and reshape errors.
5. Explain parameter sharing in convolution as a constraint on a linear map.
