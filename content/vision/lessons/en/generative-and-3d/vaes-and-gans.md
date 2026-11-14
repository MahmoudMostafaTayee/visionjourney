---
lesson_id: "vaes-and-gans"
course_id: "generative-and-3d"
lang: "en"
order_index: 1
title: "VAEs and GANs"
description: "Two ways to learn an image distribution: variational inference with a latent code, and adversarial training with a learned critic."
meta_title: "VAEs and GANs - Generative and 3D Vision"
meta_description: "Learn variational autoencoders, the ELBO and reparameterisation trick, generative adversarial networks, mode collapse and FID evaluation."
meta_keywords: "variational autoencoder, VAE, ELBO, reparameterisation, GAN, mode collapse, WGAN, FID"
---

A generative model learns the distribution of images, not just a decision boundary. That lets it sample, interpolate, inpaint and provide priors for inverse problems. Two families dominated before diffusion: variational autoencoders and generative adversarial networks.

## Variational autoencoders

A VAE encodes an image into a distribution over a latent variable $z$, then decodes a sample from that distribution back into an image. The encoder outputs the mean and log-variance of a Gaussian, and the decoder maps $z$ to a reconstruction.

Training maximises the evidence lower bound:

$$\log p(x) \geq \mathbb{E}_{q(z|x)}\left[\log p(x|z)\right] - D_{\mathrm{KL}}\left(q(z|x)\,\|\,p(z)\right)$$

The first term rewards reconstruction. The second term pulls the approximate posterior toward the prior, which regularises the latent space and makes sampling possible. The tension between the two terms is the central design issue: too much regularisation produces blurry reconstructions, too little produces a latent space with holes.

The reparameterisation trick makes the sampling differentiable: instead of sampling $z \sim \mathcal{N}(\mu, \sigma^2)$ directly, compute $z = \mu + \sigma \odot \epsilon$ with $\epsilon \sim \mathcal{N}(0, I)$. Gradients then flow through $\mu$ and $\sigma$.

The standard VAE loss is often blurry because the Gaussian likelihood corresponds to mean squared error, and the KL term compresses information. Posterior collapse occurs when the decoder ignores the latent code and the KL term drives the posterior to the prior.

:::single-choice{#vae-elbo} What does the KL term in the VAE objective do?

::option[It pulls the encoded distribution toward the prior, regularising the latent space so samples are meaningful]{#vae-kl .correct explanation="Matching the prior makes the aggregate posterior cover the latent space, which is what allows sampling and interpolation."}
::option[It measures reconstruction error directly]{#vae-recon explanation="Reconstruction is the first term; the KL term compares distributions."}
::option[It ensures the decoder is invertible]{#vae-invertible explanation="VAEs are not invertible; the KL term imposes a distributional constraint, not invertibility."}
:::

## Generative adversarial networks

A GAN trains a generator to produce images and a discriminator to distinguish generated from real. The generator improves by fooling the discriminator; the discriminator improves by detecting fakes. The objective is a minimax game:

$$\min_G \max_D \; \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z}[\log(1 - D(G(z)))]$$

At the equilibrium, the generator matches the data distribution and the discriminator cannot do better than chance. In practice, training is unstable: the generator can collapse to a few modes, the discriminator can become too strong, and gradients can vanish.

Wasserstein GANs replace the classification objective with an Earth Mover distance, using a critic constrained to be Lipschitz. This provides smoother gradients and reduces mode collapse. Gradient penalty terms enforce the constraint in practice.

Mode collapse is the characteristic GAN failure: the generator produces a limited set of outputs that fool the discriminator, ignoring much of the data distribution. Minibatch discrimination, unrolled GANs and diverse architectures help, but the problem is not fully solved.

:::single-choice{#gan-mode-collapse} What is mode collapse in a GAN?

::option[The generator produces a narrow set of outputs that fool the discriminator while ignoring much of the data distribution]{#mode-collapse .correct explanation="The objective rewards fooling the discriminator, not coverage, so the generator can converge to a few high-probability modes."}
::option[The discriminator memorises the training set]{#mode-memorise explanation="Memorisation is a different failure; mode collapse concerns the generator's output diversity."}
::option[The latent space becomes too large]{#mode-latent explanation="Latent dimension can influence training, but mode collapse is about output coverage, not latent size."}
:::

## Evaluating generative models

Likelihood is not directly comparable across model families, because VAEs and GANs define different densities. Two widely used proxies are sample quality and distribution distance.

The Fréchet Inception Distance embeds real and generated images with a pretrained network, fits Gaussians to both feature sets, and computes

$$\text{FID} = \lVert \mu_r - \mu_g \rVert^2 + \operatorname{Tr}\left(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2}\right)$$

Lower is better. FID rewards both fidelity and diversity, but it depends on the feature extractor and is biased for small sample sizes. Inception Score measures classifiability and diversity but is less sensitive to intra-class variation and is easy to game.

Neither metric measures whether a generated image is physically plausible, correctly composed or useful for a downstream task. For scientific and medical generation, task-specific validation is essential.

:::single-choice{#fid-meaning} What does FID compare?

::option[The distributions of deep features for real and generated images]{#fid-features .correct explanation="FID fits Gaussians to feature embeddings from a pretrained network and measures their Fréchet distance."}
::option[Pixel-wise mean squared error between real and generated images]{#fid-pixels explanation="FID operates in a learned feature space, not pixel space, and does not require paired images."}
::option[The number of distinct modes produced by the generator]{#fid-modes explanation="FID is sensitive to mode dropping through the covariance term, but it does not count modes explicitly."}
:::

## What each family is good for

VAEs provide a smooth, structured latent space and a principled likelihood bound. They are useful for compression, representation learning and anomaly detection, where a calibrated notion of typicality matters. Their samples are blurry, but their latent structure is reliable.

GANs produce sharp samples and remain competitive for real-time synthesis and style transfer. They are harder to train, offer no likelihood, and can silently drop modes. Their discriminator is sometimes reused as a perceptual loss or a feature extractor.

Diffusion models, covered next, combine stable training with high sample quality and have largely displaced GANs for high-fidelity image generation. The conceptual inheritance remains: the VAE's latent space and the GAN's adversarial critique both reappear in modern systems.

:::callout{type="warning" title="Generated data is not free data"}
Synthetic images can augment training, but they carry the biases and failure modes of the generator. A detector trained on synthetic data may learn generator artefacts rather than object structure. Validate on real data from the deployment distribution.
:::

## Summary

You can now explain and evaluate the two classical generative families.

1. Derive the ELBO and explain the reconstruction-regularisation trade-off.
2. Use the reparameterisation trick and diagnose posterior collapse.
3. Describe adversarial training, its instability and mode collapse.
4. Interpret FID and Inception Score and state their limits.
