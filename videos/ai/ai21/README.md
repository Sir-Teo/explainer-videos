# AI, Built — Part 21: Diffusion and Flow

Part 21 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How models make things from noise, from the 2015 idea of destroying data slowly to
the diffusion language models of 2026. Part 20 ended with Langevin dynamics and the score; this part learns the score
at every noise level and follows it back. The Part 21 toy models are trained on a CPU: points in the plane, letter
pictures, and text. Earlier scoreboard rows use restored original results with their own target and context protocols;
published large-model results are attributed to their sources.

The data are Part 5's letters "AI" made into a smooth density, a mixture of 400 small Gaussians (`exact.py`), so that
the score, the best denoiser, the probability-flow ODE and flow matching's velocity field are all known exactly; the
experiments then measure every learned or discretized thing against the truth. Pictures are 20 x 20 capital letters
drawn from the system's fonts; text is Part 1's thirty novels, through Part 13's characters.

The picture-neighbor baseline uses at most 300 references from every seventh training picture, comparing each
with all training pictures and excluding exact zero distances. Counts depend on the reviewed font inputs. A mean
nearest-neighbor distance does not rule out individual copies.

## Chapters

* **From noise.** Our denoiser walks 300 points from noise into the letters; how we got here, 2015–2026; the plan.
* **1. Destroying data slowly.** The forward process (Sohl-Dickstein et al. 2015; DDPM's schedule); its closed form
  q(x_t | x_0) derived; checked on 20,000 points run through 1,000 steps (slope, leftover variance, whole clouds); the
  posterior q(x_{t-1} | x_t, x_0); the variance-preserving continuous form (Part 5's Ornstein–Uhlenbeck).
* **2. The bound, and guessing the noise.** The variational bound as a sum of KL terms; Gaussian KLs become weighted
  squared errors of a noise guess (Ho, Jain & Abbeel 2020); DDPM's weights λ_t, computed; the simple loss; our
  denoiser's training replayed (samples from the same noise at checkpoints, the loss).
* **3. Tweedie's formula.** The best squared-error guess is the posterior mean (1D picture); Tweedie's formula proved
  (Robbins 1956; Efron 2011); checked against brute-force quadrature (1D), Monte Carlo over 50,000 points (2D) and our
  network; the best denoiser's one-jump guesses blur at high noise.
* **4. Denoising score matching.** Explicit score matching and its trace (Hyvärinen 2005); Vincent's theorem (2011),
  proved; checked through training: loss = constant + error against the exact score, at four noise levels, three
  seeds; where the score is hardest; Song & Ermon (2019).
* **5. Running time backwards.** The VP SDE (Song et al. 2021); Anderson's reverse-time SDE (1982); the
  probability-flow ODE derived from Fokker–Planck; reverse SDE and ODE run with the exact score: paths, marginals
  against fresh samples at every time, the ODE run there and back.
* **6. DDPM and DDIM.** Both samplers with our network; DDIM's step derived, and shown to be Euler in (x/α, σ/α); η;
  distance from the data against the number of steps.
* **7. Noise schedules.** SNR and log-SNR of DDPM, cosine (Nichol & Dhariwal 2021), ours and flow matching; DDPM's
  terminal SNR (Lin et al. 2024); the continuous bound's invariance (Kingma et al. 2021); where training spends its
  noise levels; four schedules trained at equal budgets (three seeds), error against the exact denoiser by noise level
  and distance after sampling; four step spacings for three solvers.
* **8. EDM: preconditioning and Heun.** Karras et al. (2022): the σ-parameterization, dx/dσ = (x − D)/σ;
  preconditioning derived (c_in, c_skip, c_out) and measured on our data (target spread, error amplification); noise,
  clean-point and EDM targets trained at equal budgets (three seeds); Heun's method, and when it beats Euler.
* **9. DPM-Solver: an exact linear part.** Lu et al. (2022a, b): the exponential integrator derived; first order is DDIM;
  DPM-Solver++(2S) and DPM-Solver++(2M); Euler, DDIM, Heun, DPM-Solver++(2S), DPM-Solver++(2M) and DDPM compared with the
  exact denoiser (error against a high-resolution ODE reference by number of evaluations), then with our network.
* **10. Optimal transport and flow matching.** Monge (1781), Kantorovich (1942), Benamou–Brenier (2000); the optimal
  pairing of 1,500 points (Hungarian algorithm); flow matching (Lipman et al.; Liu et al.; Albergo & Vanden-Eijnden;
  2023) and the marginal-field theorem, proved and checked with the exact velocity at four times; straightness,
  kinetic energy and transport cost against the optimum; stochastic interpolants (Albergo, Boffi & Vanden-Eijnden
  2023): the diffusion path as an interpolant.
* **11. Rectified flow and reflow.** Flow matching's training replayed; reflow (Liu, Gong & Liu 2023) once and twice;
  minibatch OT pairs (Tong et al. 2024; Pooladian et al. 2023); straightness and distance by number of Euler steps,
  three seeds; InstaFlow, SD3, FLUX.1.
* **12. Distillation.** Progressive distillation (Salimans & Ho 2022), 64 → 1 steps, replayed round by round;
  consistency models (Song et al. 2023; sCM, Lu & Song 2025), consistency distillation replayed; distribution
  matching distillation (Yin et al. 2024a, b): the KL gradient as a difference of scores, derived and trained; all
  three at one step, three seeds. The small DMD demonstration isolates score-difference updates; the published
  DMD benchmark also used teacher-output regression.
* **13. One step from scratch.** MeanFlow (Geng et al. 2025): the average velocity and its identity, derived; shortcut
  models (Frans et al. 2024); both replayed; every one-step model of the part on one board, three seeds. Our MeanFlow
  uses a plain squared error, an adaptation of the paper's adaptively weighted loss; this comparison does not
  reproduce the paper's full training recipe. Both one-step networks use slower time features than the part's
  other networks, because MeanFlow differentiates the network along time (see `fewstep.py`).
* **14. Guidance.** Conditioning with label dropout (replayed); classifier guidance via Bayes (Dhariwal & Nichol
  2021); classifier-free guidance (Ho & Salimans 2022); negative-x fraction (a proxy for the A class), precision and recall swept over w for
  classifier-free guidance, classifier guidance (a noisy classifier we train) and autoguidance (Karras et al. 2024,
  with a weaker model of our own); three seeds.
* **15. From points to pictures.** A picture as a point in 400 dimensions; flow matching on letter pictures, replayed;
  one sample's journey; nearest-training-picture distances; latent diffusion (Rombach et al. 2022) and the image and
  video systems of 2022–2025 (architectures: Part 22).
* **16. Diffusion for discrete data.** D3PM (Austin et al. 2021): uniform and absorbing noise; masked diffusion's bound
  derived as a weighted cross-entropy and as an any-order autoregressive loss (Sahoo et al. 2024; Shi et al. 2024;
  Ou et al. 2024); checked exactly on a 4-letter language: the T-step bound, the weighted cross-entropy and the
  any-order average, for three models; the lineage (Uria et al. 2014; Hoogeboom et al. 2022; SEDD, Lou et al. 2024).
* **17. Diffusion language models.** LLaDA (Nie et al. 2025); our masked-diffusion model and an autoregressive model
  of exactly the same size, data, initial weights, batches and steps, two seeds each, training replayed (bits, fill-in,
  writing); three estimates of the bound; the model read left to right; the scoreboard row (a bound, in 64-character
  blocks); writing with fewer rounds (surest first, at random, in blocks), judged by the other seed's
  autoregressive model; block diffusion (Arriola et al. 2025), Mercury, Gemini Diffusion, Fast-dLLM, LLaDA2.0,
  DiffusionGemma (June 2026).
* **Outro.** Eight pictures from the part's results, where the ideas come back, six problems, Part 22's teaser,
  references.

## Reviewed inputs and source-only acceptance

This source change contains no render manifest, numerical results, datasets, model weights or rendered evidence.
The chapter descriptions specify the toy experiments and explanations; they are not new experiment receipts.
Continuous playback, actual listening, speech synchronization and production acceptance remain separate gates.
The stored-path animation uses linear interpolation between saved states, with no new model evaluations between
states. It follows the recorded polyline and does not establish continuous-time solver accuracy. Other Cairo
cached plays/waits can still advance the narration clock differently from encoded frame time; the helper aligns
only its own path phase. A successful render or source test does not prove audiovisual synchronization.

Scenes read `reviewed_inputs.py`, which never imports scientific producers, writes cache files, or computes on a
missing input. Missing, incompatible, changed or unreviewed inputs stop with `ReviewedInputError`. The text
scoreboard also reads Part 1/13 JSON through this guard; it does not call either upstream producer's `load`.
`AI21_QUICK=1` fixtures cannot be used as reviewed render inputs.

Before rendering, an independent operator must supply `.cache/ai21/render-manifest.json` after reviewing the actual
producer/input provenance, numerical outputs, populations and compatibility. Do not create an acceptance manifest
merely to bypass a missing-input error. The schema is:

- `schema_version: 1`, `part: "ai21"`.
- `compatibility_sources`: all six repository paths `videos/ai/ai21/{compute,exact,train2d,fewstep,discrete,textlm}.py`,
  each mapped to the complete reviewed SHA256 of the current compatible source. These pins are distinct from the
  identities of the source/input bytes that actually produced a historical artifact.
- `products`: entries for whichever of the 18 names in `compute.ITEMS` the requested scenes consume. Each entry
  declares `json: {bytes, sha256}`, `npz: null` or `{bytes, sha256, arrays: {name: {dtype, shape}}}`, and
  `review: {accepted: true, recipe, producer_sha256, input_sha256: {input_role: sha256}}`.
- Recipe is `original-recipe`, except `solvers` and `solvers_net` require `euler-common-start-v1`. That review must
  check the corrected common physical EDM start `80*z`, including VP start `80*z/sqrt(6401)`, preserve original
  outcomes separately, and independently check all affected metrics and picture arrays before accepting them.
  Renaming an old result or changing a recipe label does not establish those facts.
- `upstream`: optional `tf` and `scoreboard` descriptors for the historical `.cache/ai13/tf.json` and
  `.cache/ai1/scoreboard.json` metadata consumed by the text scoreboard. Each declares the same `json` identity and
  `review` provenance structure, with recipe `historical-original`. No upstream arrays or weights are loaded here.

The guard verifies finite JSON, complete hashes, exact byte counts, declared NPZ inventory/dtypes/shapes and numeric
finiteness; object arrays and JSON/NPZ key collisions are rejected. Files are read as regular files without following
symlinks through POSIX directory descriptors; unsupported platforms fail explicitly. A descriptor is the operator's
assertion about identified bytes, not proof of scientific correctness or training reproducibility. If a source or
input changes, review its compatibility and the affected numerical outcomes again.

`text_zh_reviewed.json` is a narrow shared-caption delta. The integrator must compose its 60 exact strings and four
regex entries individually into `videos/ai/ai_text_zh.json`, preserving unrelated entries and existing pattern order.
Resolve any conflicting translation explicitly. This branch does not replace that shared table or install an
in-memory overlay; `validate_captions("zh")` stops until all entries are present exactly once with matching values.
The part-local `narration_zh.json` contains translation fixtures; `zh_lines.py` provides computed-line templates.
Neither file is an experimental result receipt. Caption composition does not establish visual or audio acceptance.

After the independently reviewed inputs and Chinese caption composition are available, run from the repo root:

```sh
python tools/build.py ai21
python tools/build.py ai21 --lang zh
```

The scientific producer remains an explicit opt-in command, separate from reviewed rendering:

```sh
python -m videos.ai.ai21.compute
```

It can train models and load/compute dependencies, and does not issue a review manifest. No training or upstream
regeneration is performed by the guarded scene reads. The stock `make.py` wrapper is not a complete reviewed-input
acceptance workflow.

Focused tests use small analytic examples and synthetic temporary manifests only:

```sh
python -m pytest -q tests/test_ai21_scientific_contracts.py tests/test_ai21_motion_clock.py tests/test_ai21_reviewed_inputs.py
```

They check source/numerical identities, path endpoints/interpolation and read-only failure behavior. They do not
validate a real cache, a supplied operator manifest, the full training experiments, rendered playback or audio.

## References

Books: S. J. D. Prince, *Understanding Deep Learning* (2023), ch. 18; K. P. Murphy, *Probabilistic Machine Learning:
Advanced Topics* (2023), ch. 25; C. Villani, *Optimal Transport: Old and New* (2009). S. Dieleman's blog posts on
diffusion (sander.ai).

Papers: Sohl-Dickstein, Weiss, Maheswaranathan & Ganguli (2015); Ho, Jain & Abbeel, DDPM (2020); Song & Ermon (2019);
Song et al., Score-Based Generative Modeling through SDEs (2021); Anderson, Reverse-time diffusion equation models
(1982); Robbins (1956); Efron, Tweedie's formula and selection bias (2011); Hyvärinen (2005); Vincent (2011); Song,
Meng & Ermon, DDIM (2021); Nichol & Dhariwal (2021); Kingma, Salimans, Poole & Ho, VDM (2021); Lin, Liu, Li & Yang,
Common diffusion noise schedules and sample steps are flawed (2024); Karras, Aittala, Aila & Laine, EDM (2022); Karras
et al., Guiding a diffusion model with a bad version of itself (2024); Lu et al., DPM-Solver (2022) and DPM-Solver++
(2022); Benamou & Brenier (2000); Lipman et al., Flow Matching (2023); Liu, Gong & Liu, Rectified Flow (2023); Albergo &
Vanden-Eijnden (2023); Albergo, Boffi & Vanden-Eijnden, Stochastic Interpolants (2023); Tong et al. (2024);
Pooladian et al. (2023); Liu et al., InstaFlow (2023); Salimans & Ho, Progressive Distillation (2022); Song, Dhariwal,
Chen & Sutskever, Consistency Models (2023); Lu & Song, sCM (2025); Yin et al., DMD (2024) and DMD2 (2024); Geng,
Deng, Bai, Kolter & He, MeanFlow (2025); Frans, Hafner, Levine & Abbeel, Shortcut Models (2024); Dhariwal & Nichol,
Diffusion Models Beat GANs (2021); Ho & Salimans, Classifier-Free Guidance (2022); Rombach et al., Latent Diffusion
(2022); Peebles & Xie, DiT (2023); Esser et al., SD3 (2024); Black Forest Labs, FLUX.1 model cards (2024); Google
DeepMind, Veo 3 model card; Austin et al., D3PM (2021); Uria, Murray & Larochelle (2014); Hoogeboom et al.,
Autoregressive Diffusion Models (2022); Lou, Meng & Ermon, SEDD (2024); Sahoo et al., MDLM (2024); Shi et al., MD4
(2024); Ou et al., RADD (2024); Nie et al., LLaDA (2025); Arriola et al., Block Diffusion (2025); Inception Labs,
Mercury (2025); Google DeepMind, Gemini Diffusion (2025); Wu et al., Fast-dLLM (2025); Ant Group et al., LLaDA2.0
(2025); Google, DiffusionGemma (10 June 2026); Prabhudesai et al., Diffusion Beats Autoregressive in Data-Constrained
Settings (2025).

The text-model replay curves evaluate 64 held-out blocks (4,096 characters) at each checkpoint. The final comparison
uses 512 held-out blocks (32,768 characters) starting at validation offset 200,000. These are distinct evaluation
cohorts, so a replay curve endpoint need not equal the final comparison value. Diffusion entries estimate a loss
upper bound; autoregressive entries evaluate exact per-character loss.

Three-seed whiskers on the point-model comparison bars show the observed minimum and maximum; text-model
uncertainty bars explicitly show ±one standard error. The DPM solver picture row compares three candidate solvers
at about 12 evaluations with a separately labeled high-resolution reference that uses a larger budget. SDE/ODE
path-length statistics average each path’s total length after adding its 50 recorded segments.

Schedule invariance compares reparameterized denoisers expressed in signal-to-noise ratio under monotone schedules
with the same endpoints. It does not guarantee identical fixed-weight behavior or finite-training results.

## Problems

1. For q(x_t | x_{t-1}) = N(√(1−β_t) x_{t-1}, β_t I), show q(x_t | x_0) = N(√ᾱ_t x_0, (1−ᾱ_t) I) with ᾱ_t = ∏_{s≤t}(1−β_s).
2. For x = α x_0 + σ ε, prove Tweedie's formula E[x_0 | x] = (x + σ² ∇log p(x))/α, and deduce that the best noise
   guess is −σ ∇log p(x).
3. Prove that denoising score matching and explicit score matching differ by a constant independent of θ.
4. Show that DDIM's step x_s = α_s x̂_0 + σ_s ε̂ solves dx/dσ = (x − D)/σ exactly, in x/α and σ/α, when D = x̂_0 is constant
   over the step.
5. At a fixed noise level and with ideal conditional and unconditional scores, show that classifier-free guidance
   with weight w gives the score of the normalized density proportional to p_t(x) p_t(c | x)^w, and w = 1 gives the
   conditional score. This local identity does not establish the endpoint distribution of an entire guided trajectory.
6. For masked diffusion on n symbols, show C(n, k) ∫₀¹ t^{k−1}(1−t)^{n−k} dt = 1/k, and deduce that the bound is the
   any-order autoregressive loss.

### Solutions

1. By induction. Suppose x_{t−1} = √ᾱ_{t−1} x_0 + √(1−ᾱ_{t−1}) ε̄ with ε̄ standard normal. Then x_t = √(1−β_t) x_{t−1} +
   √β_t ε_t = √ᾱ_t x_0 + [√((1−β_t)(1−ᾱ_{t−1})) ε̄ + √β_t ε_t]. The bracket is a sum of independent Gaussians, so it is
   Gaussian with variance (1−β_t)(1−ᾱ_{t−1}) + β_t = 1 − (1−β_t)ᾱ_{t−1} = 1 − ᾱ_t. The base case t = 1 is the step
   itself.
2. p(x) = ∫ N(x; α x_0, σ² I) p(x_0) dx_0. Differentiating under the integral, ∇p(x) = ∫ (α x_0 − x)/σ² N(x; α x_0, σ²I)
   p(x_0) dx_0. Dividing by p(x), N p(x_0)/p(x) = p(x_0 | x), so ∇log p(x) = (α E[x_0 | x] − x)/σ², which rearranges to
   Tweedie's formula. Since ε = (x − α x_0)/σ, E[ε | x] = (x − α E[x_0 | x])/σ = −σ ∇log p(x), and the conditional mean
   minimizes the expected squared error.
3. Write J_D = ½E‖s(x̃) − ∇log q(x̃|x)‖² and J_E = ½E‖s(x̃) − ∇log q_σ(x̃)‖². Expanding, each is ½E‖s‖² minus a cross term
   plus a term without θ. The cross terms are equal: E_{q_σ}[s·∇log q_σ] = ∫ s·∇q_σ dx̃ = ∫∫ s·∇_x̃ q(x̃|x) p(x) dx dx̃ =
   E_{x,x̃}[s·∇log q(x̃|x)], using ∇log q = ∇q/q twice and q_σ = ∫ q(x̃|x) p(x) dx. So J_D − J_E does not depend on θ.
4. In x̃ = x/α and σ̃ = σ/α the state is x̃ = x_0 + σ̃ ε and the probability-flow ODE is dx̃/dσ̃ = (x̃ − D)/σ̃. With D
   constant, d(x̃ − D)/dσ̃ = (x̃ − D)/σ̃, so x̃ − D is proportional to σ̃: x̃_s = D + (σ̃_s/σ̃_t)(x̃_t − D). With
   ε̂ = (x̃_t − D)/σ̃_t this is x̃_s = D + σ̃_s ε̂; multiplying by α_s gives x_s = α_s D + σ_s ε̂, DDIM's step.
5. At fixed t, with exact scores and densities evaluated at that noise level, the guided score is ∇log p(x) + w(∇log p(x|c) − ∇log p(x)). By Bayes, ∇log p(x|c) − ∇log p(x) = ∇log p(c|x) (p(c)
   does not depend on x), so the guided score is ∇log p(x) + w ∇log p(c|x) = ∇log[p(x) p(c|x)^w]. At w = 1 it is
   ∇log p(x|c). (In ε or velocity form the same holds, since each is an affine function of the score at fixed t.)
6. ∫₀¹ t^{k−1}(1−t)^{n−k} dt = B(k, n−k+1) = (k−1)!(n−k)!/n!, and multiplying by C(n, k) = n!/(k!(n−k)!) leaves 1/k.
   The bound ∫₀¹ (1/t) E[Σ_{blanks} CE] dt sums over blank sets M of t^{|M|}(1−t)^{n−|M|}/t, so a set of size k gets weight
   1/(k C(n, k)): the bound is Σ_k E_{|M|=k}[(1/k) Σ_{i∈M} −log p(x_i | x_{∖M})]. In a uniformly random order, the step that
   reveals the j-th symbol has a uniformly random hidden set of size k = n − j + 1 and predicts a uniformly random member
   of it, so its expected loss is the same k-th term; summing over j gives the any-order autoregressive loss.

## 习题（中文）

1. 对 q(x_t | x_{t−1}) = N(√(1−β_t) x_{t−1}, β_t I)，证明 q(x_t | x_0) = N(√ᾱ_t x_0, (1−ᾱ_t) I)，其中 ᾱ_t = ∏_{s≤t}(1−β_s)。
2. 对 x = α x_0 + σ ε，证明特威迪公式 E[x_0 | x] = (x + σ² ∇log p(x))/α，并推出最佳的噪声猜测是 −σ ∇log p(x)。
3. 证明去噪分数匹配与显式分数匹配只相差一个与 θ 无关的常数。
4. 证明当 D = x̂_0 在一步之内不变时，DDIM 的一步 x_s = α_s x̂_0 + σ_s ε̂ 在坐标 x/α、σ/α 下精确地解出 dx/dσ = (x − D)/σ。
5. 在固定噪声时刻 t、条件与无条件分数均精确时，证明权重 w 的无分类器引导给出正比于 p_t(x) p_t(c | x)^w 的归一化密度的分数，
   且 w = 1 时等于条件分数。这个局部恒等式不保证整条引导轨迹的终点分布。
6. 对 n 个符号上的掩码扩散，证明 C(n, k) ∫₀¹ t^{k−1}(1−t)^{n−k} dt = 1/k，并推出这个损失上界等于对均匀随机揭示顺序取平均的自回归损失。

### 解答

1. 归纳法。设 x_{t−1} = √ᾱ_{t−1} x_0 + √(1−ᾱ_{t−1}) ε̄，ε̄ 为标准正态。则 x_t = √ᾱ_t x_0 + [√((1−β_t)(1−ᾱ_{t−1})) ε̄ + √β_t ε_t]。
   方括号里是两个独立高斯变量之和，仍是高斯变量，方差为 (1−β_t)(1−ᾱ_{t−1}) + β_t = 1 − ᾱ_t。t = 1 时就是那一步本身。
2. p(x) = ∫ N(x; α x_0, σ² I) p(x_0) dx_0。在积分号下求导得 ∇p(x) = ∫ (α x_0 − x)/σ² · N · p(x_0) dx_0；除以 p(x)，
   N p(x_0)/p(x) 就是后验 p(x_0 | x)，所以 ∇log p(x) = (α E[x_0 | x] − x)/σ²，移项即得特威迪公式。由 ε = (x − α x_0)/σ，
   E[ε | x] = (x − α E[x_0 | x])/σ = −σ ∇log p(x)，而条件均值使期望平方误差最小。
3. 记 J_D = ½E‖s(x̃) − ∇log q(x̃|x)‖²，J_E = ½E‖s(x̃) − ∇log q_σ(x̃)‖²。展开后，两者都是 ½E‖s‖² 减去一个交叉项，再加一个
   与 θ 无关的项。两个交叉项相等：E_{q_σ}[s·∇log q_σ] = ∫ s·∇q_σ dx̃ = ∫∫ s·∇_x̃ q(x̃|x) p(x) dx dx̃ = E_{x,x̃}[s·∇log q(x̃|x)]，
   用了两次 ∇log q = ∇q/q，以及 q_σ = ∫ q(x̃|x) p(x) dx。所以 J_D − J_E 与 θ 无关。
4. 在 x̃ = x/α、σ̃ = σ/α 下，状态为 x̃ = x_0 + σ̃ ε，概率流 ODE 为 dx̃/dσ̃ = (x̃ − D)/σ̃。D 不变时 d(x̃ − D)/dσ̃ = (x̃ − D)/σ̃，
   所以 x̃ − D 与 σ̃ 成正比：x̃_s = D + (σ̃_s/σ̃_t)(x̃_t − D)。记 ε̂ = (x̃_t − D)/σ̃_t，即 x̃_s = D + σ̃_s ε̂；乘以 α_s 得
   x_s = α_s D + σ_s ε̂，正是 DDIM 的一步。
5. 固定 t，使用该噪声时刻的精确分数与密度，引导后的分数函数是 ∇log p(x) + w(∇log p(x|c) − ∇log p(x))。由贝叶斯公式，∇log p(x|c) − ∇log p(x) = ∇log p(c|x)（p(c)
   与 x 无关），所以它等于 ∇log p(x) + w ∇log p(c|x) = ∇log[p(x) p(c|x)^w]。w = 1 时就是 ∇log p(x|c)。（在固定的 t 下，
   ε 或速度都是分数函数的仿射函数，所以结论同样成立。）
6. ∫₀¹ t^{k−1}(1−t)^{n−k} dt = B(k, n−k+1) = (k−1)!(n−k)!/n!，乘以 C(n, k) = n!/(k!(n−k)!) 就剩下 1/k。损失上界
   ∫₀¹ (1/t) E[Σ_空白 CE] dt 对每个空白集合 M 的权重是 t^{|M|}(1−t)^{n−|M|}/t 的积分，大小为 k 的集合得到权重 1/(k C(n, k))，
   所以损失上界等于 Σ_k E_{|M|=k}[(1/k) Σ_{i∈M} −log p(x_i | x_{∖M})]。在均匀随机的顺序里，揭开第 j 个符号的那一步，面对的是一个
   大小为 k = n − j + 1 的均匀随机隐藏集合，并预测其中均匀随机的一个，所以它的期望损失正是第 k 项；对 j 求和，就得到任意顺序
   自回归的损失。

## Glossary

| English | 中文 |
|---|---|
| diffusion model | 扩散模型 |
| forward process, reverse process | 前向过程，反向过程 |
| noise schedule; β_t; ᾱ_t (alpha bar) | 噪声调度；β_t；ᾱ_t（阿尔法拔） |
| variance preserving (VP) | 方差保持 |
| evidence lower bound (ELBO); negative ELBO (loss upper bound) | 证据下界（ELBO）；负ELBO（损失上界） |
| noise prediction (ε-prediction), the simple loss | 噪声预测（ε预测），简化损失 |
| denoiser D(x; σ) | 去噪器D(x; σ) |
| Tweedie's formula, posterior mean | 特威迪公式，后验均值 |
| score matching, denoising score matching | 分数匹配，去噪分数匹配 |
| stochastic differential equation (SDE), reverse-time SDE | 随机微分方程（SDE），反向时间SDE |
| probability-flow ODE | 概率流常微分方程（概率流ODE） |
| Fokker–Planck equation, continuity equation | 福克-普朗克方程，连续性方程 |
| DDPM, DDIM, ancestral sampling, η | DDPM，DDIM，祖先采样，η |
| signal-to-noise ratio (SNR), log-SNR, terminal SNR | 信噪比，对数信噪比，终端信噪比 |
| step spacing | （采样）步长间隔 |
| preconditioning (c_in, c_skip, c_out) | 预条件化（c_in，c_skip，c_out） |
| error amplification | 误差放大 |
| Euler's method, Heun's method, second order | 欧拉法，休恩法，二阶 |
| exponential integrator, integrating factor | 指数积分器，积分因子 |
| DPM-Solver, DPM-Solver++ (multistep) | DPM-Solver，DPM-Solver++（多步法） |
| network evaluations (NFE) | 网络调用次数（NFE） |
| sliced Wasserstein distance | 切片瓦瑟斯坦距离 |
| optimal transport, coupling, transport cost | 最优传输，耦合（配对），运输代价 |
| Benamou–Brenier formula, kinetic energy | 贝纳穆-布雷尼耶公式，动能 |
| flow matching; conditional and marginal velocity | 流匹配；条件速度与边缘速度 |
| marginal-field theorem | 边缘速度场定理 |
| stochastic interpolant | 随机插值 |
| rectified flow, reflow, straightness | 整流流，重流，直度 |
| minibatch optimal transport (OT-CFM) | 小批量最优传输 |
| distillation, teacher, student | 蒸馏，老师，学生 |
| progressive distillation | 渐进蒸馏 |
| consistency model, self-consistency, consistency distillation | 一致性模型，自洽性，一致性蒸馏 |
| distribution matching distillation (DMD) | 分布匹配蒸馏（DMD） |
| MeanFlow, average velocity | MeanFlow，平均速度 |
| shortcut model | 捷径模型 |
| Jacobian-vector product, stop-gradient | 雅可比-向量积，停止梯度 |
| classifier guidance, classifier-free guidance (CFG), guidance weight w | 分类器引导，无分类器引导（CFG），引导权重w |
| autoguidance | 自引导 |
| precision and recall (k-NN) | 精确率与召回率（k近邻） |
| latent diffusion, latents | 潜空间扩散，潜变量 |
| diffusion transformer (DiT) | 扩散Transformer（DiT） |
| discrete diffusion (D3PM), transition matrix | 离散扩散（D3PM），转移矩阵 |
| uniform noise, absorbing (mask) noise, mask token [M] | 均匀噪声，吸收态（掩码）噪声，掩码词元[M] |
| masked diffusion, weighted cross-entropy | 掩码扩散，加权交叉熵 |
| any-order autoregressive model | 任意顺序自回归模型 |
| a tight bound | 紧的界 |
| block diffusion | 块扩散 |
| surest-first unmasking (low-confidence remasking) | 最有把握优先的揭开（低置信度重掩码） |
| AR-judge bits per character; generative perplexity = 2^bpc | 自回归评判模型的每字符比特数；生成困惑度 = 2^每字符比特数 |
| diffusion language model (dLLM) | 扩散语言模型 |

QA metric conventions: cached `dpm2` denotes midpoint data-prediction DPM-Solver++(2S). Cached `floor` values are finite-sample reference baselines, not mathematical lower bounds. DSM scene consumers convert historical noise-error terms by `1/(2 sigma_t^2)` to the displayed half-squared-score loss without rewriting the training caches. The Euler VP initialization now represents the same physical start as the other solvers; the reviewed-input guard rejects legacy solver acceptance records. A new independent review must identify all affected rows and picture arrays while preserving original outcomes separately.

Guidance metric conventions: legacy `onA` is the fraction with `x < 0`, a left-region proxy rather than A membership; `spread` is mean radius about that subset's centroid. Metrics use 1,000 generated points per seed and a seeded 1,000-point real-A reference subset; panels show the first 500 points of seed 0. Reflow's loss plot is per-coordinate squared velocity error, with loss markers hidden until the first recorded update.
