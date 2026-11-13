---
lesson_id: "diffusion-models"
course_id: "generative-and-3d"
lang: "en"
order_index: 2
title: "Diffusion Models"
description: "The forward noising process, the learned reverse process, classifier-free guidance and latent diffusion."
meta_title: "Diffusion Models - Generative and 3D Vision"
meta_description: "Learn DDPM forward and reverse processes, the noise-prediction objective, classifier-free guidance, latent diffusion and sampling."
meta_keywords: "diffusion model, DDPM, denoising, classifier-free guidance, latent diffusion, score matching, sampling"
---

Diffusion models generate images by learning to reverse a gradual noising process. The forward process is fixed and destroys structure step by step; the reverse process is learned and reconstructs structure one denoising step at a time. The result is stable training and state-of-the-art sample quality.

## The forward process

Given a clean image $x_0$, the forward process adds Gaussian noise over $T$ steps:

$$q(x_t \mid x_{t-1}) = \mathcal{N}\left(\sqrt{1-\beta_t}\, x_{t-1},\ \beta_t I\right)$$

The schedule $\beta_t$ controls how quickly signal is destroyed. A useful property is that the marginal at any step has a closed form:

$$x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1-\bar\alpha_t}\, \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)$$

where $\bar\alpha_t = \prod_{s=1}^{t}(1-\beta_s)$. This means you can jump directly to any noise level during training without simulating every step, which is what makes training efficient.

:::demo{id="diffusion"} Forward noising at an adjustable timestep
The slider controls the signal-to-noise ratio. Early in the process the image is nearly intact; late, almost all structure is gone. The reverse model must learn to invert this degradation, not to generate from nothing in one step.
:::

:::single-choice{#forward-closed-form} Why is the closed-form marginal for x_t important for training?

::option[It allows sampling any noise level directly, avoiding a step-by-step forward simulation]{#closed-form .correct explanation="Training can pick a random timestep and compute x_t in one shot from x_0 and noise, which is much cheaper."}
::option[It makes the forward process learnable]{#forward-learnable explanation="The forward process is fixed by the schedule; only the reverse process is learned."}
::option[It removes the need for a noise schedule]{#no-schedule explanation="The schedule determines the coefficients in the closed form; it is still required."}
:::

## The reverse process

The reverse process is parameterised as a Gaussian whose mean is predicted by a network:

$$p_\theta(x_{t-1} \mid x_t) = \mathcal{N}\left(\mu_\theta(x_t, t),\ \Sigma_\theta(x_t, t)\right)$$

Rather than predicting the mean directly, the standard parameterisation predicts the noise $\epsilon_\theta(x_t, t)$ that was added. The simplified training objective is

$$\mathcal{L} = \mathbb{E}_{t, x_0, \epsilon}\left[\lVert \epsilon - \epsilon_\theta(x_t, t) \rVert^2\right]$$

This is a denoising regression: given a noisy image and the timestep, predict the noise. It is stable, scales well and does not require adversarial training.

Predicting noise is equivalent to predicting the score of the data distribution up to a scaling factor. This connection to score matching explains why diffusion can be formulated as a stochastic differential equation and sampled with numerical integrators.

:::single-choice{#noise-prediction} What does the standard diffusion network predict during training?

::option[The noise that was added to the clean image at the sampled timestep]{#predict-noise .correct explanation="The regression target is epsilon, and the reverse step uses the prediction to estimate the denoised image."}
::option[The class label of the image]{#predict-class explanation="Class conditioning is optional; the core objective is noise regression."}
::option[The next image in a sequence]{#predict-next explanation="Diffusion is not an autoregressive next-frame model; it denoises the same image across timesteps."}
:::

## Guidance and conditioning

Unconditional diffusion samples from the data distribution. To condition on a class or a text prompt, the model must incorporate the condition. Classifier guidance uses the gradient of an external classifier to steer samples toward a class; classifier-free guidance trains a single model both with and without the condition and interpolates between the two predictions at sampling time:

$$\hat\epsilon = \epsilon_\theta(x_t, \varnothing) + s\left(\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \varnothing)\right)$$

The guidance scale $s$ trades diversity for fidelity. A high scale produces samples that match the prompt strongly but reduces variety and can introduce saturation artefacts. Most text-to-image systems expose this as a tunable parameter.

:::single-choice{#cfg-scale} What does increasing the classifier-free guidance scale do?

::option[It strengthens conditioning at the cost of sample diversity and can introduce artefacts]{#cfg-effect .correct explanation="The extrapolation amplifies the conditional direction, improving prompt adherence but narrowing the distribution."}
::option[It increases the number of sampling steps]{#cfg-steps explanation="Guidance affects the direction of each step, not the step count."}
::option[It removes the need for a noise schedule]{#cfg-schedule explanation="The schedule remains essential; guidance modifies the predicted noise."}
:::

## Latent diffusion and efficiency

Diffusing in pixel space at high resolution is expensive: every denoising step operates on a full-resolution image. Latent diffusion first trains an autoencoder that compresses images into a lower-dimensional latent space, then runs the diffusion process in that space and decodes the result.

This reduces compute by orders of magnitude while preserving perceptual quality, because the autoencoder handles the high-frequency detail and the diffusion model handles semantics. Stable Diffusion popularised this design and made high-quality text-to-image generation feasible on consumer hardware.

Architecturally, the denoiser is often a U-Net with cross-attention to text embeddings, or a transformer (DiT) operating on latent patches. DiTs scale better with model size and have become the backbone of several state-of-the-art systems.

Sampling speed is an active area. DDIM and other deterministic samplers reduce the number of steps; distillation methods train a student to produce good samples in one or a few steps. The trade-off is between sample quality, diversity and latency.

:::single-choice{#latent-diffusion} Why does latent diffusion reduce compute?

::option[Because the denoising network operates on a compressed latent representation rather than full-resolution pixels]{#latent-compute .correct explanation="Spatial dimensions are much smaller in the latent space, so each step costs far less while the decoder restores detail."}
::option[Because it skips the noise schedule]{#latent-schedule explanation="The diffusion process still has a schedule; only the space it operates in changes."}
::option[Because it uses a GAN discriminator instead of a denoiser]{#latent-gan explanation="Latent diffusion still uses a denoising objective; the autoencoder is separate from the diffusion model."}
:::

## What diffusion is used for in vision

Beyond image synthesis, diffusion models serve as priors for inverse problems: inpainting, super-resolution, deblurring and colourisation. They can be conditioned on text, segmentation maps, depth, poses or reference images, which makes them a general conditional generator.

In 3D, diffusion has been applied to novel view synthesis, texture generation and scene completion. Video diffusion extends the framework with temporal attention, producing temporally coherent samples.

The limitations are real. Sampling is slow relative to a single forward pass, the models are large, and they can reproduce training-data biases. Attribution, watermarking and provenance are active concerns, and the distinction between generating a plausible image and generating a true one remains essential.

:::callout{type="insight" title="Likelihood is not truth"}
A diffusion model assigns high probability to images that look like its training data. It does not verify that a depicted event occurred. For evidence-bearing imagery, provenance metadata and cryptographic signing matter more than perceptual realism.
:::

## Summary

You can now explain diffusion from the forward process to guidance and deployment.

1. Write the forward process and its closed-form marginal.
2. Explain the noise-prediction objective and its relation to denoising.
3. Apply classifier-free guidance and interpret the scale.
4. Explain latent diffusion's compute advantage.
5. Recognise diffusion as a conditional prior for inverse problems.
