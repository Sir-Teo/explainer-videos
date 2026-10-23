# AI, Built — Part 20: Four Ways to Generate

Part 20 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first part of Act IV, *Generation and Perception*. How a machine learns a
distribution it can sample from: the four families that work — autoregressive models, variational autoencoders,
generative adversarial networks, normalizing flows — and the older fifth, energy-based models, with their history from
Shannon's letter-by-letter English (1948) to one-step generators (2026), and how to judge them. Every model here is
trained on this computer, by `compute.py`, on the same data, so they can be compared: three densities in the plane (two
moons, a ring of eight Gaussians, a checkerboard) and MNIST digits averaged down to 14 × 14 pixels with 16 grey levels.
The five image models get the same budget of arithmetic, 6 × 10¹² floating-point operations of training each, counted
by PyTorch's own per-operation formulas, three seeds each.

* **Hook: digits nobody wrote.** Samples from four of our models side by side (PixelCNN, VAE, GAN, RealNVP); the
  question; the five answers; the plan.
* **1. The generative problem.** A generative model as a distribution to sample, evaluate and encode; maximum
  likelihood as minimum KL, E_p[−log q] = h(p) + KL(p‖q), with each toy's entropy h(p) computed as the floor every
  model is measured against; how we got here (Shannon 1948, Hopfield 1982, Boltzmann machines 1985, the Helmholtz
  machine 1995, deep belief nets 2006, VAEs, GANs, NICE and PixelCNN 2013–16, StyleGAN and neural ODEs 2018, diffusion
  beating GANs in 2021, next-scale prediction 2024); the families' trade-offs and the generative trilemma (Xiao,
  Kreis & Vahdat 2022); the test bench.
* **2. One pixel at a time.** The chain rule; an autoregressive model in the plane, p(x₁) p(x₂ | x₁), each factor a
  mixture of ten Gaussians, its conditional slices and its training replay; masked convolutions (NADE, MADE, PixelRNN,
  PixelCNN, WaveNet); the blind spot of stacked masks, computed as the gradient of one pixel's prediction with respect to
  every input pixel, and the two-stack layout that removes it (van den Oord et al. 2016b); our PixelCNN's training
  replayed (held-out bits per pixel and samples at each checkpoint, three seeds); one digit drawn pixel by pixel with
  its sixteen predicted probabilities; the cost of 196 sequential passes, measured against the GAN's one.
* **3. From Helmholtz machines to the VAE.** Latent-variable models and the intractable integral; the Helmholtz
  machine and the wake–sleep algorithm (Dayan, Hinton, Neal & Zemel 1995; Hinton, Dayan, Frey & Neal 1995); the ELBO
  derived (Jensen) with its gap KL(q(z|x)‖p(z|x)); the reparameterization trick and the Gaussian KL in closed form
  (Kingma & Welling 2013; Rezende, Mohamed & Wierstra 2014); our VAE (16-number code, discretized-logistic decoder over
  the 16 levels, after PixelCNN++).
* **4. Training a VAE: rate, distortion, collapse.** The two terms of the bound over training, with reconstructions and
  samples at each checkpoint; the ELBO and a 64-sample importance-weighted bound in bits per pixel; active code units; a
  VAE with a 2-number code, the test digits' codes replayed through training and the decoded grid; β-VAE (Higgins et
  al. 2017) at β = 0.25 … 8, two seeds each: the rate–distortion curve (Alemi et al. 2018), active units and samples;
  posterior collapse made to happen: in the plane, a factorized decoder keeps its rate while an autoregressive decoder's
  falls to zero (three seeds each); on digits, a VAE with a PixelCNN decoder, plain and with free bits (Kingma et al.
  2016), its rate over training and whether digits decoded from one code keep their identity (judged by the
  classifier); the VAE's blur on the ring.
* **5. The adversarial game.** The GAN value function (Goodfellow et al. 2014); the optimal discriminator
  D* = p/(p + q) and V(D*, G) = −log 4 + 2 JS(p‖q), derived; the saturating loss log(1 − D) against the non-saturating
  −log D, with the generator's measured early gradient norms; the non-saturating gradient as reverse KL minus 2 JS
  (Arjovsky & Bottou 2017); mode collapse on the ring, replayed (the discriminator's verdict under the generator's
  samples) for the seed that ended with the fewest modes; modes covered by the minimax and non-saturating losses over
  five seeds each.
* **6. Why GANs spiral.** min_x max_y xy: the rotating field, eigenvalues ±i; simultaneous steps spiral out by exactly
  √(1 + η²) per step (asserted), alternating steps orbit, extragradient (Korpelevich 1976) and optimistic steps
  (Daskalakis et al. 2018) spiral in; Mescheder, Geiger & Nowozin's Dirac-GAN (2018) with and without the R1 penalty;
  the ring GAN's mode occupancy, checkpoint by checkpoint.
* **7. Wasserstein GANs.** Arjovsky's parallel lines: Jensen–Shannon is flat at log 2 while W₁ = |θ|, both estimated by
  trained networks at seventeen offsets; the earth mover's distance (Monge 1781, Kantorovich 1942); Kantorovich–
  Rubinstein duality; weight clipping and the gradient penalty (Gulrajani et al. 2017); WGAN-GP on the ring against both
  GAN losses, five seeds each, same networks and generator steps; the price per generator step, counted.
* **8. GANs at scale: BigGAN, StyleGAN, inversion.** Our digit GAN replayed with its losses; DCGAN (2015), progressive
  growing (2017), BigGAN (2018: IS 166.5, FID 7.4 at 128², previous best 52.5 and 18.6), StyleGAN (mapping network,
  per-layer styles, noise, style mixing; schematic); the truncation trick measured on our GAN (precision, recall and FID
  against the truncation threshold); GAN inversion by gradient descent on z, four restarts per digit, against the VAE's
  encoder, and an interpolation (iGAN 2016, Image2StyleGAN 2019, DragGAN 2023).
* **9. Normalizing flows.** The change of variables in 1D and d dimensions (Tabak & Vanden-Eijnden 2010; Rezende &
  Mohamed 2015); affine coupling layers and their triangular Jacobian (NICE 2014, RealNVP 2017), the log-determinant
  checked against autograd's; the plane warped layer by layer by our 8-coupling flow (moons and checkerboard); training
  replayed and each toy's gap to its floor; RealNVP on digits at temperatures 1 and 0.7; Glow (2018) and TarFlow
  (Zhai et al., 2024/ICML 2025).
* **10. Neural ODEs and continuous flows.** Residual networks as Euler steps (Chen et al. 2018); the instantaneous change
  of variables d log p/dt = −tr(∂f/∂z), derived; Hutchinson's estimator (1989) and its variance for Gaussian and
  Rademacher probes, measured against the formulas; exact trace against one probe in 196 dimensions, timed; a
  continuous flow trained on the moons with the exact trace and with Hutchinson's estimator (FFJORD), three seeds each,
  both judged with the exact trace; 700 noise points carried along the learned field with the density at five times.
* **11. Hopfield and Boltzmann.** Hopfield's energy (1982) and why asynchronous updates never raise it; Hebb's rule;
  recall of a damaged digit replayed with its energy; capacity on random patterns against 0.138 N (Amit, Gutfreund &
  Sompolinsky 1985); correlated digits and mixture states; the modern softmax update (Krotov & Hopfield 2016; Ramsauer
  et al. 2020) as attention; the Boltzmann machine (Ackley, Hinton & Sejnowski 1985) and its two-phase learning rule;
  the 2024 Nobel Prize in Physics.
* **12. Contrastive divergence.** The restricted Boltzmann machine (Smolensky 1986), its factorized conditionals and
  free energy; the log-likelihood gradient as positive minus negative phase, derived; CD-k (Hinton 2002) and
  persistent CD (Tieleman 2008); with 16 hidden units the partition function is summed exactly over 2¹⁶ hidden states,
  so CD-1, CD-10 and PCD are compared on the true held-out log-likelihood, three seeds each; a 100-unit RBM's filters
  and Gibbs chains; exact samples of the 16-unit RBM; deep belief nets (2006).
* **13. Langevin dynamics and the score.** Energy-based models and their two-phase gradient (LeCun et al. 2006); in 2D,
  Z summed on a grid, so our energy models' likelihoods are exact; Langevin dynamics (1908) and the score
  ∇ log p = −∇E, with Z gone; persistent Langevin training (Du & Mordatch 2019) replayed on the ring; sampling from
  noise on all three toys; the failure on separated modes (two Gaussians weighted 0.2/0.8, exact score) and annealed
  Langevin (Song & Ermon 2019), toward score matching (Hyvärinen 2005; Vincent 2011) and Part 21; Equilibrium Matching
  (Wang & Du 2025).
* **14. Judging a generator.** Why likelihood isn't enough (Theis, van den Oord & Bethge 2016); FID derived as the
  Fréchet (W₂) distance between Gaussians, 1D first (Dowson & Landau 1982; Heusel et al. 2017), on the features of our
  own digit classifier (its penultimate layer, 128 numbers); checks: FID against added noise and blur, and its bias
  against the sample size; precision and recall by k-nearest-neighbour balls (Sajjadi et al. 2018; Kynkäänniemi et al.
  2019), drawn on the ring; every 2D family's precision and recall on the ring; a single Gaussian with the ring's mean
  and covariance (tiny Fréchet distance, low precision); memorization checked by nearest training digits.
* **15. Five models, one budget.** PixelCNN, VAE, GAN, WGAN-GP and RealNVP on 6 × 10¹² training FLOPs each: parameters,
  steps and digits seen; samples side by side; FID (mean and spread of three seeds), precision and recall; bits per
  pixel for the three likelihood models; which digits each model draws, by the classifier.
* **16. Where the families meet.** The 2021 turn (Dhariwal & Nichol: BigGAN-deep FID 6.95, precision 0.87, recall 0.28;
  guided ADM 4.59, 0.82, 0.52, ImageNet 256²); VQ-VAE (2017), VQGAN and DALL·E (2021): VAEs and GANs as tokenizers,
  autoregressive models over the tokens; our own VQ-VAE (49 tokens from 32 codes) with a small transformer prior; VAR's
  next-scale prediction (Tian et al. 2024: FID 1.73 vs 18.65, NeurIPS 2024 outstanding paper); GANs back inside fast
  samplers (ADD 2023, LADD 2024, DMD2 2024, R3GAN 2024, sCM 2024/25, drifting models 2026); the family tree.
* **Recap**, where it comes back, problems, Part 21's teaser, references.

## Running it

From the repo root:

```
python tools/make.py ai20                       # everything: the computations, then English and Chinese
python -m videos.ai.ai20.compute                # only the numbers (MNIST through Part 10's checked download)
python tools/build.py ai20                      # English
python tools/build.py ai20 --lang zh            # Chinese
AI20_SCALE=0.01 python -m videos.ai.ai20.compute   # a smoke test of every code path (into .cache/ai20_quick/)
```

Everything is seeded (`numpy` PCG64 and `torch.manual_seed`, one generator per run) and runs on one torch thread
(`AI20_THREADS` to change it); there is no multiprocessing. Every item made of several runs saves each run as it
finishes (`CACHE.partial`), so an interrupted computation resumes; trained weights go to `.cache/ai20/models/`. On a
busy 4-core machine the whole part computes in about two and a half hours of wall time; the longest items are the five
digit models (`pixelcnn`, `vae`, `gan`, `wgan`, `flow`, three seeds each, a few minutes per seed, PixelCNN's 196-pass
sampling included), `gan2d` (fifteen ring runs) and `cnf`. MNIST is read through Part 10's downloader
(`videos.ai.ai10.data`, checked against SHA-256); no other part's results are used.

## References

Books: I. Goodfellow, Y. Bengio & A. Courville, *Deep Learning* (2016), ch. 16–20; S. J. D. Prince, *Understanding Deep
Learning* (2023), ch. 14–17; K. P. Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023), part IV;
C. Villani, *Optimal Transport: Old and New* (2009).

Papers: C. E. Shannon (1948); J. J. Hopfield (1982); D. J. Amit, H. Gutfreund & H. Sompolinsky (1985); D. H. Ackley,
G. E. Hinton & T. J. Sejnowski (1985); P. Smolensky (1986); G. E. Hinton, *Training products of experts by minimizing
contrastive divergence* (2002); T. Tieleman (2008); G. E. Hinton, S. Osindero & Y.-W. Teh (2006); D. Krotov &
J. J. Hopfield (2016); H. Ramsauer et al., *Hopfield Networks is All You Need* (2020); P. Dayan, G. E. Hinton,
R. M. Neal & R. S. Zemel, *The Helmholtz Machine* (1995); G. E. Hinton, P. Dayan, B. J. Frey & R. M. Neal, *The
wake-sleep algorithm* (1995); D. P. Kingma & M. Welling, *Auto-Encoding Variational Bayes* (2013); D. J. Rezende,
S. Mohamed & D. Wierstra (2014); Y. Burda, R. Grosse & R. Salakhutdinov, *IWAE* (2016); S. R. Bowman et al. (2016);
D. P. Kingma et al., *IAF* (2016); X. Chen et al., *Variational Lossy Autoencoder* (2017); I. Higgins et al.,
*β-VAE* (2017); A. A. Alemi et al., *Fixing a Broken ELBO* (2018); H. Larochelle & I. Murray, *NADE* (2011);
M. Germain et al., *MADE* (2015); A. van den Oord, N. Kalchbrenner & K. Kavukcuoglu, *Pixel Recurrent Neural
Networks* (2016); A. van den Oord et al., *Conditional Image Generation with PixelCNN Decoders* (2016), *WaveNet*
(2016); T. Salimans et al., *PixelCNN++* (2017); I. Goodfellow et al., *Generative Adversarial Nets* (2014);
A. Radford, L. Metz & S. Chintala, *DCGAN* (2015); T. Salimans et al., *Improved Techniques for Training GANs* (2016);
M. Arjovsky & L. Bottou (2017); M. Arjovsky, S. Chintala & L. Bottou, *Wasserstein GAN* (2017); I. Gulrajani et al.,
*Improved Training of Wasserstein GANs* (2017); G. M. Korpelevich (1976); C. Daskalakis et al., *Training GANs with
Optimism* (2018); L. Mescheder, A. Geiger & S. Nowozin, *Which Training Methods for GANs do actually Converge?*
(2018); T. Miyato et al., *Spectral Normalization* (2018); H. Zhang et al., *SAGAN* (2018); T. Karras et al.,
*Progressive Growing of GANs* (2018); A. Brock, J. Donahue & K. Simonyan, *BigGAN* (2019); T. Karras, S. Laine &
T. Aila, *StyleGAN* (2019), and StyleGAN2 (2020), StyleGAN3 (2021); J.-Y. Zhu et al., *iGAN* (2016); R. Abdal, Y. Qin &
P. Wonka, *Image2StyleGAN* (2019); X. Pan et al., *DragGAN* (2023); Y. Huang et al., *The GAN is dead; long live the
GAN!* (2024); E. G. Tabak & E. Vanden-Eijnden (2010); D. J. Rezende & S. Mohamed, *Variational Inference with
Normalizing Flows* (2015); L. Dinh, D. Krueger & Y. Bengio, *NICE* (2014); L. Dinh, J. Sohl-Dickstein & S. Bengio,
*RealNVP* (2017); D. P. Kingma & P. Dhariwal, *Glow* (2018); S. Zhai et al., *Normalizing Flows are Capable Generative
Models* (2025); R. T. Q. Chen, Y. Rubanova, J. Bettencourt & D. Duvenaud, *Neural Ordinary Differential Equations*
(2018); W. Grathwohl et al., *FFJORD* (2019); M. F. Hutchinson (1989); Y. LeCun et al., *A Tutorial on Energy-Based
Learning* (2006); P. Langevin (1908); A. Hyvärinen, *Score Matching* (2005); P. Vincent (2011); Y. Du & I. Mordatch
(2019); E. Nijkamp et al. (2019); Y. Song & S. Ermon (2019); R. Wang & Y. Du, *Equilibrium Matching* (2025);
L. Theis, A. van den Oord & M. Bethge (2016); M. Heusel et al. (2017); D. C. Dowson & B. V. Landau (1982); M. S. M.
Sajjadi et al. (2018); T. Kynkäänniemi et al. (2019); G. Stein et al., *Exposing flaws of generative model evaluation
metrics* (2023); Z. Xiao, K. Kreis & A. Vahdat (2022); P. Dhariwal & A. Nichol, *Diffusion Models Beat GANs on Image
Synthesis* (2021); A. van den Oord, O. Vinyals & K. Kavukcuoglu, *VQ-VAE* (2017); P. Esser, R. Rombach & B. Ommer,
*Taming Transformers* (2021); A. Ramesh et al., *DALL·E* (2021); K. Tian et al., *Visual Autoregressive Modeling*
(2024); A. Sauer et al., *Adversarial Diffusion Distillation* (2023) and *LADD* (2024); T. Yin et al., *DMD2* (2024);
C. Lu & Y. Song, *sCM* (2025); M. Deng, H. Li, T. Li, Y. Du & K. He, *Generative Modeling via Drifting* (2026).
Data: Y. LeCun, C. Cortes & C. J. C. Burges, MNIST (1998). The 2024 Nobel Prize citation is the Royal Swedish Academy
of Sciences'.

## Problems, with solutions

**1. The optimal discriminator.** Show that for a fixed generator with distribution q, the best discriminator is
D* = p/(p + q), and that V(D*, G) = −log 4 + 2 JS(p‖q).

*Solution.* V = ∫ [p log D + q log(1 − D)] dx, and at each x the integrand a log y + b log(1 − y) has derivative
a/y − b/(1 − y), zero at y = a/(a + b); its second derivative is negative, so this is the maximum: D* = p/(p + q).
Substituting, V = E_p[log p/(p + q)] + E_q[log q/(p + q)]. Write p + q = 2m with m = (p + q)/2: each term is
E[log p/m] − log 2, so V = KL(p‖m) + KL(q‖m) − log 4 = 2 JS(p‖q) − log 4, minimized (at −log 4) exactly when q = p.

**2. The ELBO's gap, and collapse.** Show log p(x) − ELBO = KL(q(z|x)‖p(z|x)). If the decoder can represent p(x)
exactly without using z, show that q(z|x) = p(z) maximizes the ELBO.

*Solution.* ELBO = E_q[log p(x, z) − log q(z|x)] = E_q[log p(x) + log p(z|x) − log q(z|x)] = log p(x) −
KL(q(z|x)‖p(z|x)). If the decoder ignores z and equals p(x), then p(x|z) = p(x), the true posterior is the prior, and
the ELBO is log p(x) − KL(q(z|x)‖p(z)), at most log p(x) with equality for q(z|x) = p(z). Any use of z must buy more
reconstruction than it costs in KL; a decoder that needs nothing from z gets nothing for it.

**3. A coupling layer.** For y_a = x_a, y_b = x_b ⊙ exp(s(x_a)) + t(x_a), show log|det J| = Σᵢ sᵢ(x_a), and write the
inverse.

*Solution.* ∂y_a/∂x_a = I and ∂y_a/∂x_b = 0, so J is block lower-triangular with diagonal blocks I and
diag(exp(s(x_a))); its determinant is the product of the diagonal, exp(Σ sᵢ), positive. Inverse: x_a = y_a (copied),
then x_b = (y_b − t(y_a)) ⊙ exp(−s(y_a)); s and t are never inverted, only evaluated.

**4. Hutchinson's estimator.** Show E[εᵀAε] = tr A when E[εεᵀ] = I. For Rademacher ε (entries ±1), show the variance
is 2 Σ_{i≠j} S_ij², with S = (A + Aᵀ)/2.

*Solution.* E[εᵀAε] = Σ_ij A_ij E[εᵢεⱼ] = Σᵢ A_ii. Since εᵀAε = εᵀSε, write it as Σᵢ S_ii εᵢ² + Σ_{i≠j} S_ij εᵢεⱼ;
for signs εᵢ² = 1, so the first sum is the constant tr A, and the variance is that of Σ_{i≠j} S_ij εᵢεⱼ =
2 Σ_{i<j} S_ij εᵢεⱼ. The products εᵢεⱼ (i < j) have mean 0, variance 1 and are pairwise uncorrelated, so the
variance is 4 Σ_{i<j} S_ij² = 2 Σ_{i≠j} S_ij². (For Gaussian ε the diagonal terms vary too, adding 2 Σᵢ S_ii²: total
2‖S‖_F².)

**5. The RBM's conditionals.** For E(v, h) = −bᵀv − cᵀh − vᵀWh with binary units, derive p(h_j = 1 | v) =
σ(c_j + W_{:j}ᵀv) and the free energy F(v) = −bᵀv − Σⱼ log(1 + exp(c_j + W_{:j}ᵀv)).

*Solution.* p(h | v) ∝ exp(cᵀh + vᵀWh) = Πⱼ exp(h_j (c_j + W_{:j}ᵀv)): a product over j, so the h_j are independent
given v, each with p(h_j = 1 | v) = e^{aⱼ}/(1 + e^{aⱼ}) = σ(aⱼ), aⱼ = c_j + W_{:j}ᵀv. Summing h out,
Σ_h e^{−E(v,h)} = e^{bᵀv} Πⱼ (1 + e^{aⱼ}) = e^{−F(v)} with F as stated.

**6. The 2-Wasserstein distance between 1D Gaussians.** Show that W₂²(N(μ₁, σ₁²), N(μ₂, σ₂²)) = (μ₁ − μ₂)² +
(σ₁ − σ₂)².

*Solution.* In one dimension the optimal coupling is monotone, quantile to quantile: x₂ = μ₂ + (σ₂/σ₁)(x₁ − μ₁).
With x₁ = μ₁ + σ₁ζ, ζ ~ N(0, 1), x₁ − x₂ = (μ₁ − μ₂) + (σ₁ − σ₂)ζ, so E(x₁ − x₂)² = (μ₁ − μ₂)² + (σ₁ − σ₂)². This
is the d = 1 case of ‖μ₁ − μ₂‖² + tr(Σ₁ + Σ₂ − 2(Σ₁^{1/2}Σ₂Σ₁^{1/2})^{1/2}), FID's formula.

## 习题与解答

**1. 最优判别器。** 证明：对一个分布为q的固定生成器，最好的判别器是 D* = p/(p + q)，并且 V(D*, G) = −log 4 + 2 JS(p‖q)。

*解答。* V = ∫ [p log D + q log(1 − D)] dx；在每个x处，被积函数 a log y + b log(1 − y) 的导数是 a/y − b/(1 − y)，在
y = a/(a + b) 处为零，二阶导数为负，所以这是最大值：D* = p/(p + q)。代回去，V = E_p[log p/(p + q)] + E_q[log q/(p + q)]。
记 p + q = 2m，m = (p + q)/2：每一项都是 E[log p/m] − log 2，所以 V = KL(p‖m) + KL(q‖m) − log 4 = 2 JS(p‖q) − log 4，
当且仅当 q = p 时取到最小值 −log 4。

**2. ELBO的差距，以及坍缩。** 证明 log p(x) − ELBO = KL(q(z|x)‖p(z|x))。如果解码器不用z也能精确表示p(x)，证明
q(z|x) = p(z) 使ELBO最大。

*解答。* ELBO = E_q[log p(x, z) − log q(z|x)] = E_q[log p(x) + log p(z|x) − log q(z|x)] = log p(x) − KL(q(z|x)‖p(z|x))。
如果解码器忽略z、并且等于p(x)，那么 p(x|z) = p(x)，真实后验就是先验，ELBO = log p(x) − KL(q(z|x)‖p(z))，至多为log p(x)，
当 q(z|x) = p(z) 时取等号。任何对z的使用，换来的重建收益都必须超过它在KL上的代价；一个什么都不需要z的解码器，用z就什么也得不到。

**3. 耦合层。** 对 y_a = x_a，y_b = x_b ⊙ exp(s(x_a)) + t(x_a)，证明 log|det J| = Σᵢ sᵢ(x_a)，并写出逆变换。

*解答。* ∂y_a/∂x_a = I，∂y_a/∂x_b = 0，所以J是分块下三角矩阵，对角块是I和diag(exp(s(x_a)))；它的行列式等于对角线之积，
exp(Σ sᵢ)，为正。逆变换：x_a = y_a（直接复制），然后 x_b = (y_b − t(y_a)) ⊙ exp(−s(y_a))；s和t从不需要求逆，只需要计算。

**4. 哈钦森估计量。** 证明当 E[εεᵀ] = I 时 E[εᵀAε] = tr A。对拉德马赫ε（分量取±1），证明方差是 2 Σ_{i≠j} S_ij²，其中
S = (A + Aᵀ)/2。

*解答。* E[εᵀAε] = Σ_ij A_ij E[εᵢεⱼ] = Σᵢ A_ii。由于 εᵀAε = εᵀSε，把它写成 Σᵢ S_ii εᵢ² + Σ_{i≠j} S_ij εᵢεⱼ；
取正负号时 εᵢ² = 1，所以第一项是常数tr A，方差就是 Σ_{i≠j} S_ij εᵢεⱼ = 2 Σ_{i<j} S_ij εᵢεⱼ 的方差。乘积 εᵢεⱼ（i < j）
均值为0、方差为1，并且两两不相关，所以方差是 4 Σ_{i<j} S_ij² = 2 Σ_{i≠j} S_ij²。（对高斯ε，对角项也会变化，再加上
2 Σᵢ S_ii²：总共是 2‖S‖_F²。）

**5. RBM的条件分布。** 对二值单元的 E(v, h) = −bᵀv − cᵀh − vᵀWh，推导 p(h_j = 1 | v) = σ(c_j + W_{:j}ᵀv)，以及自由能
F(v) = −bᵀv − Σⱼ log(1 + exp(c_j + W_{:j}ᵀv))。

*解答。* p(h | v) ∝ exp(cᵀh + vᵀWh) = Πⱼ exp(h_j (c_j + W_{:j}ᵀv))：这是对j的乘积，所以给定v时各h_j独立，
p(h_j = 1 | v) = e^{aⱼ}/(1 + e^{aⱼ}) = σ(aⱼ)，其中 aⱼ = c_j + W_{:j}ᵀv。把h求和消掉，
Σ_h e^{−E(v,h)} = e^{bᵀv} Πⱼ (1 + e^{aⱼ}) = e^{−F(v)}，F如上所述。

**6. 一维高斯之间的2-瓦瑟斯坦距离。** 证明 W₂²(N(μ₁, σ₁²), N(μ₂, σ₂²)) = (μ₁ − μ₂)² + (σ₁ − σ₂)²。

*解答。* 在一维里，最优耦合是单调的，分位数对分位数：x₂ = μ₂ + (σ₂/σ₁)(x₁ − μ₁)。令 x₁ = μ₁ + σ₁ζ，ζ ~ N(0, 1)，则
x₁ − x₂ = (μ₁ − μ₂) + (σ₁ − σ₂)ζ，所以 E(x₁ − x₂)² = (μ₁ − μ₂)² + (σ₁ − σ₂)²。这正是FID公式
‖μ₁ − μ₂‖² + tr(Σ₁ + Σ₂ − 2(Σ₁^{1/2}Σ₂Σ₁^{1/2})^{1/2}) 在 d = 1 时的情形。

## Glossary (new terms in this part)

| English | 中文 |
|---|---|
| generative model | 生成模型 |
| sample, evaluate, encode | 采样，计算（概率），编码 |
| density estimation | 密度估计 |
| differential entropy, the floor h(p) | 微分熵，下限h(p) |
| two moons, ring of eight Gaussians, checkerboard | 双月，八个高斯组成的环（八峰环），棋盘格 |
| autoregressive model | 自回归模型 |
| mixture density network (mixture of Gaussians) | 混合密度网络（高斯混合） |
| NADE, MADE | NADE，MADE |
| PixelCNN, PixelRNN, WaveNet | PixelCNN，PixelRNN，WaveNet |
| masked convolution, mask A / mask B | 掩码卷积，A型掩码 / B型掩码 |
| receptive field, blind spot | 感受野，盲区 |
| vertical stack, horizontal stack | 竖直栈，水平栈 |
| bits per pixel | 每像素比特数 |
| latent variable, code z | 隐变量，编码z |
| prior, posterior | 先验，后验 |
| Helmholtz machine, recognition model | 亥姆霍兹机，识别模型 |
| wake–sleep algorithm | 醒-睡算法 |
| amortized inference | 摊销推断 |
| variational autoencoder (VAE) | 变分自编码器（VAE） |
| encoder, decoder | 编码器，解码器 |
| evidence lower bound (ELBO) | 证据下界（ELBO） |
| reparameterization trick | 重参数化技巧 |
| reconstruction term | 重建项 |
| rate, distortion, rate–distortion trade-off | 码率，失真，码率-失真权衡 |
| importance-weighted bound (IWAE) | 重要性加权下界（IWAE） |
| discretized logistic | 离散化逻辑斯谛分布 |
| active units | 活跃单元 |
| β-VAE, disentanglement | β-VAE，解耦 |
| posterior collapse | 后验坍缩 |
| free bits, KL annealing | 自由比特，KL退火 |
| generative adversarial network (GAN) | 生成对抗网络（GAN） |
| generator, discriminator | 生成器，判别器 |
| minimax game, value function | 极小极大博弈，值函数 |
| optimal discriminator | 最优判别器 |
| Jensen–Shannon divergence | 詹森-香农散度（JS散度） |
| saturating / non-saturating loss | 饱和损失 / 非饱和损失 |
| reverse KL | 反向KL散度 |
| mode collapse, mode dropping | 模式坍缩，模式丢失 |
| simultaneous / alternating gradient steps | 同时梯度步 / 交替梯度步 |
| extragradient, optimistic gradient descent | 外梯度法，乐观梯度下降 |
| Dirac-GAN, R1 penalty | 狄拉克GAN，R1惩罚 |
| two time-scale update rule (TTUR) | 双时间尺度更新规则（TTUR） |
| spectral normalization | 谱归一化 |
| Wasserstein distance, earth mover's distance | 瓦瑟斯坦距离，推土机距离 |
| transport plan, coupling | 运输方案，耦合 |
| Kantorovich–Rubinstein duality | 坎托罗维奇–鲁宾斯坦对偶 |
| 1-Lipschitz, critic | 1-利普希茨，评判器 |
| weight clipping, gradient penalty (WGAN-GP) | 权重截断，梯度惩罚（WGAN-GP） |
| DCGAN, progressive growing, BigGAN | DCGAN，渐进式增长，BigGAN |
| StyleGAN, mapping network, style, style mixing | StyleGAN，映射网络，风格，风格混合 |
| truncation trick | 截断技巧 |
| GAN inversion | GAN反演 |
| normalizing flow | 归一化流 |
| change of variables | 变量替换 |
| Jacobian determinant, log-determinant | 雅可比行列式，对数行列式 |
| coupling layer (affine), NICE, RealNVP, Glow | （仿射）耦合层，NICE，RealNVP，Glow |
| dequantization, logit transform | 去量化，logit变换 |
| temperature (sampling) | （采样）温度 |
| neural ODE, continuous normalizing flow | 神经ODE，连续归一化流 |
| instantaneous change of variables, divergence | 瞬时变量替换，散度 |
| trace, Hutchinson's estimator | 迹，哈钦森估计量 |
| Rademacher probe | 拉德马赫探针 |
| FFJORD | FFJORD |
| energy-based model, energy E | 能量模型（基于能量的模型），能量E |
| partition function (normalizer) Z | 配分函数（归一化常数）Z |
| Hopfield network, associative memory | 霍普菲尔德网络，联想记忆 |
| content-addressable memory | 按内容寻址的记忆 |
| capacity, spin glass, mixture state | 容量，自旋玻璃，混合态 |
| modern (dense) Hopfield network | 现代（稠密）霍普菲尔德网络 |
| Boltzmann machine, hidden / visible units | 玻尔兹曼机，隐藏 / 可见单元 |
| positive phase, negative phase | 正相，负相 |
| restricted Boltzmann machine (RBM), harmonium | 受限玻尔兹曼机（RBM），harmonium |
| free energy | 自由能 |
| Gibbs sampling | 吉布斯采样 |
| contrastive divergence (CD-k), persistent CD | 对比散度（CD-k），持续对比散度（PCD） |
| filters (of an RBM) | （RBM的）滤波器 |
| Langevin dynamics | 朗之万动力学 |
| score (function) | 分数函数 |
| replay buffer (of chains) | （链的）回放池 |
| annealed Langevin dynamics, noise levels | 退火朗之万动力学，噪声水平 |
| score matching, denoising score matching | 分数匹配，去噪分数匹配 |
| Equilibrium Matching | 均衡匹配 |
| Fréchet Inception Distance (FID) | 弗雷歇Inception距离（FID） |
| Fréchet distance, 2-Wasserstein distance | 弗雷歇距离，2-瓦瑟斯坦距离 |
| Inception Score | Inception分数 |
| features (of a classifier) | （分类器的）特征 |
| precision, recall (for generators) | 精确率，召回率（生成模型的） |
| memorization, nearest neighbour | 死记硬背（记忆），最近邻 |
| generative trilemma | 生成学习三难困境 |
| tokenizer, codebook, token | 分词器，码本，词元 |
| vector quantization (VQ-VAE), straight-through estimator | 向量量化（VQ-VAE），直通估计器 |
| perplexity (of a codebook) | （码本的）困惑度 |
| VQGAN, two-stage model | VQGAN，两阶段模型 |
| next-scale prediction (VAR) | 下一尺度预测（VAR） |
| distillation, adversarial diffusion distillation | 蒸馏，对抗扩散蒸馏 |
| consistency model | 一致性模型 |
| drifting model | 漂移模型 |
