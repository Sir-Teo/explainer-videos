# AI, Built — Part 11: Going Downhill

## Source-only QA handoff

This branch carries reviewed scene, mathematical wording, translation and replay/layout repairs.
It excludes scientific producer changes, datasets, numerical caches, weights and private QA artifacts.
The original `compute.py`, `charopt.py` and `nets.py` are unchanged. In particular, source/layout repairs
do not correct the original SOAP basis/state implementation or certify its historical rankings.

Scene loading is cache-only: missing or incompatible inputs must stop rather than launch training.
For the other products, structural readability is not recipe or input-provenance certification;
the integration owner must verify that provenance separately before accepting their rendered use.
The `race`, `ns` and `schedule` products are deliberately unavailable through scene loading in this
source-only tree. Their corrected producer and numerical provenance need separate review and integration;
placing a legacy cache under one of those names is insufficient. Dependent chapters, including the recap,
therefore cannot be accepted as rendered output from this public tree.

The acceptance here is the outgoing source/tests and narrow shared-caption compatibility. Prior selected
visual checks used separately retained inputs and exact source versions; they are not public-tree render
acceptance. Continuous playback, actual listening, speech synchronization and final 4K remain pending.
Only the designated integration owner should reconcile shared captions and cross-part scientific recipes
before rendering. The computed-result paragraphs below remain historical records, not newly certified runs.

Part 11 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)): the optimizers that train real models, from Cauchy's steepest descent (1847) to
Muon in production (2026). Gradient descent's rates derived and checked on quadratics; momentum and acceleration;
stochastic gradients, their temperature η/B and the edge of stability; AdaGrad, RMSProp and Adam derived; why weight
decay is not L2; the natural gradient, K-FAC, Shampoo and SOAP; Muon as steepest descent under the spectral norm, and
Newton–Schulz as a polynomial on singular values; a fair race between six optimizers on our own character model;
schedules (warmup, cosine, warmup–stable–decay and the river valley), weight averaging and schedule-free training;
keeping training stable (QK-clip, gradient clipping, weight decay's norm equilibrium); and the optimizer race of
2024–26. Every model is trained by `compute.py` on the CPU (PyTorch), several seeds where a comparison is made.
Part 12 covers the critical batch, μP and WSD in scaling-law runs, Part 18 loss spikes and stability at scale, and
Part 9 backpropagation; this part links to them rather than repeating them.

The workhorse is a small character model (`charopt.py`: 8 characters of context, 16-number character vectors, 256
tanh units and a residual 256 × 256 hidden layer, 167 characters) trained on Part 1's thirty novels and scored in bits
per character on held-out text. `compute.char_data` is its data; Parts 12 and 16 import it too.

About 57 minutes: a hook, sixteen chapters and an outro (56.6 min in the silent low-quality build; Chinese 57.9).

## Outline

* **Racing downhill.** Gradient descent, the heavy ball, Adam and Lion on Rosenbrock's valley in 3D, each at its best
  of 25 learning rates, 150 steps; how we got here, 1847–2026 (Cauchy 1847; Robbins & Monro 1951; Polyak 1964;
  Nesterov 1983; backpropagation with momentum 1986; AdaGrad 2011; RMSProp 2012; Adam 2014; Shampoo 2018; Muon and
  AlgoPerf 2024; MuonClip and Kimi K2 2025; DeepSeek-V4 2026); the plan.
* **1. Gradient descent, derived.** Cauchy (1847); L-smoothness and strong convexity drawn as two bowls; the descent
  lemma, the Polyak–Łojasiewicz step and the linear rate (1 − 1/κ)^k; the convex O(1/k) bound against gradient descent
  on a quadratic with curvatures 1 … 10⁻⁶; iterations against κ = 1 … 1,000 in 50 dimensions, and the measured late
  contraction against 1 − 1/κ; pause and predict: a step just over 2/L.
* **2. The heavy ball and Nesterov.** Polyak (1964); the recurrence and its characteristic roots, the tuned
  √β = (√κ − 1)/(√κ + 1) derived; Nesterov (1983) and the O(1/k²) bound against our convex quadratic; Nemirovski &
  Yudin's lower bound; iterations against κ for all three (slopes), measured contraction against derived; the heavy
  ball's failure on non-quadratic convex losses (Lessard, Recht & Packard 2016).
* **3. Stochastic gradients.** The batch gradient's mean and covariance Σ/B; Robbins & Monro (1951) and Σηₖ = ∞,
  Σηₖ² < ∞; Part 6's two-weight logistic regression (Austen against Dickens): full-batch, 16-page and 1-page paths;
  the cloud of a constant step against a step shrinking like 1/k (5 seeds); the workhorse era (Rumelhart, Hinton &
  Williams 1986; LeCun et al. 1998; AlexNet 2012).
* **4. Noise as temperature.** SGD as an Euler–Maruyama step of dθ = −∇L dt + √(η/B) Σ^{1/2} dW (Li, Tai & E 2017;
  Mandt, Hoffman & Blei 2017); the stationary covariance (discrete Lyapunov equation; tr S ≈ (η/2B) tr(H⁻¹C));
  measured on 4 learning rates × 6 batch sizes × 3 seeds against the prediction; the linear scaling rule (Goyal et al.
  2017) and Adam's square-root rule (Malladi et al. 2022); the critical batch (Part 12); sharp and flat minima (Keskar
  et al. 2017) and the reparametrization catch (Dinh et al. 2017).
* **5. The edge of stability.** Stability of a step on a bowl, ηλ < 2; pause and predict; full-batch gradient descent
  on Part 9's spirals at η = 0.05 and 0.1, the sharpness by power iteration on Hessian-vector products every 40 steps,
  replayed with the loss (Cohen et al. 2021); progressive sharpening and self-stabilization (Damian, Nichani & Lee
  2022); the edge for momentum, (2 + 2β)/η, and for Adam, 38/η (Cohen et al. 2022).
* **6. AdaGrad, RMSProp, Adam.** AdaGrad (Duchi, Hazan & Singer 2011); RMSProp (Tieleman & Hinton, Lecture 6e, 2012);
  Adam (Kingma & Ba 2014) and its bias correction derived, on one real weight's first 60 gradients; the first step
  with and without the corrections ((1 − β₁)/√(1 − β₂) ≈ 3.16η); the sign limit and every weight's step at steps 1, 100
  and 1,000 of our model; Lion, found by program search (Chen et al. 2023).
* **7. Weight decay is not L2.** L2 and decoupled decay are the same for SGD and different in Adam, derived
  (Loshchilov & Hutter 2017); AdamW against Adam + L2 on a 128-unit model that sees only 50,000 characters: held-out
  bits over 5 learning rates × 6 strengths each, the best of each from 3 seeds, and the training curves.
* **8. The natural gradient and K-FAC.** Gradient descent depends on how the weights are written (two
  parametrizations of the same loss); steepest descent under a ruler M; the Fisher and the natural gradient (Amari
  1998), shown invariant on the two-weight loss; K-FAC's Kronecker factors derived (Martens & Grosse 2015); gradient
  descent, Adam, damped K-FAC (sampled model-label factors) and a damped full-Fisher natural gradient on the spirals
  (a 2–24–24–2 network, the best of 5 rates each, 3 seeds), with a sample-space Woodbury solve for the natural
  direction and the decision maps replayed.
* **9. Shampoo and SOAP.** Full-matrix AdaGrad and Shampoo's two factors (Gupta, Koren & Singer 2018); Shampoo without
  memory is UVᵀ (Bernstein & Newhouse 2024); why it took years (roots, damping, grafting); AlgoPerf 2024 (Distributed
  Shampoo ≈ 28% faster than the baseline; Kasimbeg et al. 2025); SOAP, Adam in Shampoo's eigenbasis (Vyas et al. 2024).
* **10. Muon, derived.** A real gradient's singular values (a few dominate); Muon (Jordan et al. 2024); steepest
  descent under the spectral norm, ΔW = −ηUVᵀ, derived; one recipe and three norms (normalized gradient descent, sign
  descent, Muon); the practical recipe with Moonlight's 0.2 √max(m, n) scale (Liu et al. 2025), checked against our
  own Adam's typical step.
* **11. Newton–Schulz.** One round is a polynomial on every singular value, derived; the classical cubic, Jordan's
  quintic (3.4445, −4.7750, 2.0315) and (2, −1.5, 0.5); the real gradient's 256 singular values round by round, a
  cobweb for one of them; the scalar polynomial against the matrix iteration; DeepSeek-V4's hybrid (8 + 2 rounds) on
  the gradient and on the trained weight matrix; band and worst-distance summaries use the current largest n,
  with n fixed by the initial count above 1% of the initial largest value, rather than tracking the same initial directions or
  reporting full-spectrum worst error; the Polar Express (Amsel et al. 2025).
* **12. The race, run fairly.** SGD with momentum, AdamW, Lion, Shampoo, SOAP and Muon on the character model: the
  same data order, 3,000 steps, warmup and cosine for all; 6 initial learning rates each (seed 0), up to 3
  factor-two edge extensions per optimizer, the selected rate rerun from 2 more seeds; the sweeps, the race replayed with its spread, what the models write at checkpoints, and the time per step.
* **13. Schedules and the river valley.** Warmup (Goyal et al. 2017; Kalra & Barkeshli 2024), cosine (Loshchilov &
  Hutter 2016), warmup–stable–decay (Zhai et al. 2022; Hu et al. 2024); the river valley (Wen et al. 2024) as a
  computed toy with constant, small constant, cosine and WSD schedules (20 seeds), the loss split into river and hill
  against the stationary prediction; AdamW with cosine schedules of 1,000, 2,000 and 4,000 steps against one
  constant run with a cool-down branch at each length (2 seeds).
* **14. Without a schedule.** Iterate averaging (Ruppert 1988; Polyak & Juditsky 1992) on Chapter 3's cloud; an EMA
  of the constant run's weights against its cool-down; schedule-free AdamW (Defazio et al. 2024; AlgoPerf's
  self-tuning winner, ≈ 8%), its interpolation, and one run of it scored at every length against the scheduled runs.
* **15. Keeping training stable.** A one-layer transformer on our books trained too fast: the largest attention score
  runs away (Muon at η = 0.03 and 0.12, AdamW at 0.05; 2 seeds each); QK-clip derived (Kimi K2's MuonClip, τ = 100) and
  applied; gradient clipping (Pascanu, Mikolov & Bengio 2013); weight decay's equilibrium for a scale-invariant matrix
  derived (van Laarhoven 2017; Kosson, Messmer & Jaggi 2024) and measured at three decay strengths.
* **16. The optimizer race, 2024 to 2026.** AlgoPerf, Moonlight's ~2×, Kimi K2's MuonClip, GLM-4.5, DeepSeek-V4's
  Muon; the careful benchmarks (Wen, Hall, Ma & Liang 2025: speedups ≤ 1.4× at 0.1B, 1.1× at 1.2B; NVIDIA 2026);
  successors (Polar Express, Dion, Dion3, SOAP variants, 2026 preprints); the lesson: tune the baseline, equal
  budgets, several seeds.
* **Recap, problems, and what comes next** (Part 12, *The Mathematics of Scale*), references.

## Source checks

From the repo root:

```
python -m unittest discover -s tests -p 'test_ai11*.py' -v
python -m unittest discover -s tests -p 'test_text_tables.py' -v
```

These source checks use extracted code and explicitly synthetic fixtures; they do not train models, produce
scientific outcomes, render video or synthesize narration. The original generation and build commands are not
acceptance steps for this source-only tree. In particular, an end-to-end build can explicitly invoke the
unchanged original producers; it must not be used to bypass the scene-loader gate or imply corrected science.

The historical `compute.py` estimate was about 2.5 CPU-hours on one thread (the race about an hour, the
weight-decay grid and the schedules about 15 minutes each). Every run is seeded; the long items save each
finished run (`CACHE.partial`) and resume;
`AI11_WORKERS=4` runs their pieces in four processes (`spawn`), `AI11_THREADS` sets torch's threads per process
(default 1). Nothing sets torch's thread count at import time.

### Race protocol and metric domains

A fresh six-optimizer race schedules 48–66 runs (144,000–198,000 requested updates), including
six initial seed-0 rates, up to three edge extensions, and two additional selected-rate seeds per optimizer.
An edge optimum can remain after the cap; rates are the best tried, not guaranteed global optima.
The inherited runtime estimate above is not a bound for a separately corrected producer.

Curves score the first 20,000 validation predictions (requiring 20,008 characters); tuning and final standings
use the full 100,000-character validation slice, which has 99,992 scored predictions after the eight-character
context. Final standings show the mean and observed min–max across three seeds, not a significance interval.
Text is sampled from seed 0 at the shown steps. Its adjacent bits are interpolated from the validation curve:
step 100 lies between evaluations 0/150, and step 1,000 between 900/1,050.

Each timing bar is the optimizer's mean per-step loop time across its three selected-rate seeds divided by
AdamW's corresponding mean, not a mean of paired ratios. Time per step is amortized timed-loop wall time,
including 20 periodic prefix validations and four
72-character continuations in a completed 3,000-step run; initial evaluation/writing and final full-slice
evaluation are excluded. It is not optimizer-kernel timing. Runs share initialization and batches within each
seed; text sampling uses its own fixed Torch generator and does not consume the training-batch RNG.
The historical results below retain their original provenance; no corrected race cache is supplied by this note.

<!-- results -->
## Computed results

These numerical paragraphs are inherited records from the video-making source. Their numbers and rankings are
retained; they are not certified here as fresh runs or recovered outcome artifacts. The legacy SOAP ranking does
not validate a corrected SOAP implementation: the separately reviewed basis/state correction is isolated, and
its synthetic checks do not establish full reference-optimizer equivalence or corrected training performance.

*(from `.cache/ai11/` on the machine that made the video; the narration branches on whichever way they come out.)*

Numbers from the run that made the video (Linux, one thread, a shared machine):

* **Racing downhill.** Rosenbrock's valley (b = 5) from (−1.5, 2.2), 150 steps, the best of 25 rates each: Adam
  (η = 0.68) under 0.01 after 30 steps, the heavy ball (0.0147) after 41, Lion (0.032) after 122, gradient descent
  (0.032) after 141.
* **Gradient descent.** Steps to a millionth of the starting objective gap for κ = 1 … 1,000 in 50 dimensions: 1, 14, 46,
  126, 373, 978, 2,745 (slope 0.89 on log axes; 1.01 with η = 2/(L + μ)); the late geometric-mean √(f − f*) ratio at κ = 1,000:
  0.9990 measured, 0.9990 derived. On the convex quadratic (curvatures 1/i², 1,000 dimensions) the gap stays under
  L‖x₀ − x*‖²/2k at every one of 2,000 steps.
* **Momentum.** At κ = 1,000: 187 steps for the heavy ball and 142 for Nesterov against 2,745 (slopes 0.58 and 0.46);
  late geometric-mean √(f − f*) ratios 0.9418 (root modulus 0.9387) and 0.9702 (root modulus 0.9684). On the convex
  quadratic Nesterov ends with a gap 118 times smaller than gradient descent's and stays under 2L‖x₀ − x*‖²/(k + 1)².
* **SGD.** Part 6's 448 training pages: the stationary cloud's RMS distance 0.49 at batch 1 and 0.13 at batch 16
  (3.8 times narrower). One page per step for 20,000 steps (5 seeds): the squared distance stalls at 0.33 with a
  constant step and reaches 0.00025 with η₀/(1 + k/100).
* **Temperature.** 4 rates × 6 batch sizes × 3 seeds: E‖w − w*‖² against η/B has slope 1.00 on log axes; measured
  over the discrete-Lyapunov prediction 0.93 … 1.14; tr(H⁻¹C) = 1.90.
* **Edge of stability.** η = 0.05: the sharpness first passes 90% of 2/η = 40 at step 1,520; second-half median 39.7,
  maximum 42.6. η = 0.1: at step 280; median 19.9 (2/η = 20), maximum 20.1.
* **Adam.** Without bias correction the first step would be 3.16η; with it, 99.99% of the weights move by more than 0.9η
  at step 1; the median move is 0.13η at step 100 and 0.16η at step 1,000.
* **Natural gradient.** The 2–24–24–2 network (722 weights), 300 full-batch steps, the best of 5 rates, 3 seeds:
  median training loss after 100 steps 0.00013 (natural gradient, η = 0.3), 0.014 (Adam, 0.1), 0.045 (K-FAC, 0.1),
  4.2 (gradient descent, 3.0, still unstable then); at 300 steps 0.0, 0.0071, 0.0060 and 0.0080. The two
  parametrizations' natural-gradient paths differ by 2 × 10⁻¹⁶; gradient descent's by 4.4.
* **Spikes.** One-layer transformer, 2,000 steps, 2 seeds (held-out bits / largest recorded pre-update forward score,
  sampled every 10 steps): Muon η = 0.03: 2.86, 2.88
  / 883, 1,152; η = 0.12: 2.97, 3.16 / 25,703, 24,233; η = 0.12 with QK-clip τ = 100: 2.88, 2.92 / 146, 139. AdamW
  η = 0.05: 3.69, 3.82 / 179,276, 230,454; with gradient clipping at 1: 2.89, 3.61 (one seed rescued); with QK-clip:
  2.96, 3.39.
* **Equilibrium.** A LayerNorm after the second hidden matrix, AdamW η = 0.003 constant, 4,000 steps: ‖W‖ = 26.9,
  12.7, 6.6 at λ = 0.1, 0.4, 1.6 against 29.5, 15.0, 7.2 predicted (within 15%; 6.8, 3.4, 1.6 without the momentum
  factor); fitted power −0.51 against −0.5; the update's cosine with W −0.05 … −0.18.
* **Newton–Schulz.** The second hidden matrix's gradient at step 300 of AdamW (132 singular values above 1% of the
  largest): after Jordan's 5 rounds they lie in 0.76 … 1.20; the classical cubic leaves its worst 0.35 from one after 12
  rounds; DeepSeek-V4's hybrid (8 + 2) ends within 0.0018 of one. The trained weight matrix (241 above 1%): 0.69 …
  1.20, 0.67, 0.0005. The scalar polynomial on the singular values matches the matrix iteration to 2 × 10⁻⁶.
* **The race.** 3,000 steps, warmup and cosine, each optimizer's best rate (the grid extended to 7 rates for Lion),
  3 seeds, held-out bits on all 100,000 characters (mean, min–max): SOAP 2.334 (2.331–2.336, η = 0.008), Muon 2.341
  (2.339–2.344, 0.008), Shampoo 2.351 (2.349–2.354, 0.008), SGD with momentum 2.407 (2.399–2.416, 0.2), AdamW 2.453
  (2.434–2.474, 0.008), Lion 2.604 (2.578–2.624, 0.0032). Time per step relative to AdamW on this CPU: SGD 0.8×,
  Lion 1.4×, Shampoo 1.8×, SOAP 2.1×, Muon 2.1×.
* **Schedules.** AdamW at the race's best rate (0.008), 2 seeds, held-out bits on all 100,000 characters: cosine runs
  of 1,000, 2,000 and 4,000 steps 2.629, 2.502, 2.414; the constant run's cool-down branches (the last fifth decayed
  linearly to zero) 2.665, 2.566, 2.491; the constant run without decay 2.674 at 4,000. Here the cosine wins at every
  length, by 0.04–0.08 bits, and the narration says so. The shared 4,000-step trunk plus its three cooldowns
  require 5,400 updates per seed, versus 7,000 for three independent runs, excluding evaluation overhead.
* **River valley.** The toy (A = 4, σ = 1, η₀ = 0.25, 400 steps, 20 seeds): final loss 0.211 constant, 0.194 small
  constant, 0.036 cosine, 0.024 WSD; the constant rate's hill loss 0.128 against 0.125 predicted.
* **Averaging and schedule-free.** An EMA (β = 0.998) of the constant run's weights at step 4,000: 2.510 and 2.459
  against the raw weights' 2.620 and 2.553 (20,000 characters), about half of what the cool-down gained.
  Schedule-free AdamW (best of 0.5, 1, 2, 4 × AdamW's rate: 2×), one run per seed, on the same 20,000 characters at
  1,000, 2,000, 4,000 steps: 2.485, 2.351, 2.245, against cosine 2.556, 2.412, 2.305 and WSD 2.593, 2.489, 2.391; on
  all 100,000 at 4,000 steps 2.370 against cosine 2.414.
* **Weight decay.** 128 units, 50,000 training characters, 2,000 steps; 5 learning rates × 6 strengths for each:
  best AdamW (η = 0.016, λ = 0.3, the largest rate tried) 2.801 over 3 seeds (2.793–2.807); best Adam + L2 (η =
  0.008, λ = 0.001) 2.832 (2.826–2.838); no decay at its best rate 2.944. AdamW's best strength moves from 0 to 0.3
  across the learning rates.

## Fact-check notes

Checked against primary sources on 30 October 2026:

* AlgoPerf (Kasimbeg et al., ICLR 2025, arXiv 2502.15015): 18 submissions from 10 teams; external tuning won by
  Distributed Shampoo, "≈28% faster model training" across the eight base workloads (score 0.7784 against the NAdamW
  baseline's 0.5707); self-tuning won by Schedule-Free AdamW, "≈8% faster" than the self-tuning baseline.
* Muon (Keller Jordan's post, 8 December 2024): MomentUm Orthogonalized by Newton–Schulz; coefficients (3.4445,
  −4.7750, 2.0315), 5 steps, chosen to maximize the slope at zero with the limit values in about [0.7, 1.3]; the
  earlier baseline (2, −1.5, 0.5); NanoGPT speedrun 1.35×; FLOP overhead below 1% (0.7% NanoGPT, 0.5% Llama 405B);
  Bernstein & Newhouse's observation that Shampoo without accumulation is the orthogonalized gradient.
* Moonlight (Liu et al., arXiv 2502.16982, February 2025): weight decay and a per-parameter update scale; "~2×
  computational efficiency" against AdamW in compute-optimal training; a 3B-activated / 16B-total MoE on 5.7T tokens.
  The 0.2 √max(m, n) scale is the one Kimi K2's report gives for MuonClip.
* Kimi K2 (arXiv 2507.20534, July 2025): MuonClip, τ = 100, per-head S_max, W_q and W_k each scaled by √γ (for MLA,
  the head-specific parts; the shared rotary key untouched); 1.04T total and 32B activated parameters; "pre-trained on
  15.5 trillion tokens with zero loss spike"; vanilla Muon's logits "quickly exceed a magnitude of 1000" in a
  mid-scale run. Part 18 has its 12.7%-of-heads figure.
* DeepSeek-V4 (arXiv 2606.19348, 26 April 2026): Muon for most modules, AdamW for the embedding, the prediction head,
  mHC's static biases and gating factors and the RMSNorm weights; hybrid Newton–Schulz, 10 iterations, 8 with
  (3.4445, −4.7750, 2.0315) and 2 with (2, −1.5, 0.5) "which stabilize the singular values precisely at 1"; RMSNorm on
  queries and KV entries instead of QK-Clip; Muon momentum 0.95, weight decay 0.1, update RMS rescaled to 0.18.
* GLM-4.5 (2025) trained with Muon: as checked for Part 18.
* Wen, Hall, Ma & Liang, *Fantastic Pretraining Optimizers and Where to Find Them* (arXiv 2509.02046, September 2025;
  v3 October 2026): eleven optimizers (AdamW, NAdamW, Mars, Cautious, Lion, Adam-mini, Muon, Scion, Kron, Soap,
  Sophia), 0.1B–1.2B parameters, 1–8× Chinchilla data; claimed speedups 1.4–2×; tuning one hyperparameter of the
  GPT-3 recipe up to 2× on a 100M model; no optimizer above about 1.4× after tuning; matrix-based optimizers 1.4× at
  0.1B falling to 1.1× at 1.2B; Muon best at low data ratios, Soap and Kron at 8×. The bar chart in Chapter 16 draws
  these three numbers only.
* NVIDIA, Khona et al., *SOAP, Muon, and Beyond: Pushing LLM Pretraining Scales* (arXiv 2607.20548, July 2026):
  hybrid Mamba–Transformer MoEs up to 8B active / 72B total on 1T tokens; stable training at batches up to 100M tokens
  "where AdamW degrades"; mixed task-level comparisons (single company source).
* SOAP (Vyas et al., arXiv 2409.11321): over 40% fewer iterations and over 35% less wall-clock time than AdamW, about
  20% better than Shampoo, at 360M and 660M parameters in the large-batch regime (the authors' own measurement).
* Lion (Chen et al., arXiv 2302.06675): program search; only the momentum kept; a smaller learning rate than Adam
  because of the sign's larger update norm (no multiplier is claimed on screen).
* Dion (Ahn et al., Microsoft, arXiv 2504.05295, 2025); Dion3 (Amsel et al., Microsoft Research, August 2026: "reducing
  optimizer step time by up to 6x" at Muon's loss); the Polar Express (Amsel, Persson, Musco & Gower, arXiv
  2505.16932, ICLR 2026); MONA (arXiv 2605.26842), MUON+ (arXiv 2602.21545), T-MUON (arXiv 2610.24938) are named only,
  as preprints whose claims are their authors'.
* Historical: Cauchy, *Méthode générale pour la résolution des systèmes d'équations simultanées* (Comptes rendus 25,
  1847); Robbins & Monro (Ann. Math. Statist. 1951, University of North Carolina); Polyak (1964); Nesterov (1983);
  Rumelhart, Hinton & Williams (1986, with a momentum term α); LeCun, Bottou, Orr & Müller, *Efficient BackProp*
  (1998); Krizhevsky, Sutskever & Hinton (2012: SGD, batch 128, momentum 0.9, weight decay 0.0005, the learning rate
  divided by 10 when the validation error stopped improving); RMSProp's formula from Lecture 6e of Hinton's Coursera
  course (2012); Goyal et al. (2017: batch 8,192, one hour, gradual warmup).

## References

Books: J. Nocedal & S. J. Wright, *Numerical Optimization* (2006); Y. Nesterov, *Lectures on Convex Optimization*
(2018); L. Bottou, F. E. Curtis & J. Nocedal, *Optimization Methods for Large-Scale Machine Learning* (2018); S. J. D.
Prince, *Understanding Deep Learning* (2023), chapter 6.

Papers: Cauchy (1847); Robbins & Monro (1951); Polyak (1964); Nesterov (1983); Nemirovski & Yudin (1983); Rumelhart,
Hinton & Williams (1986); Ruppert (1988); Polyak & Juditsky (1992); Amari (1998); LeCun et al. (1998); Duchi, Hazan &
Singer (2011); Tieleman & Hinton (2012); Pascanu, Mikolov & Bengio (2013); Kingma & Ba (2014); Martens & Grosse
(2015); Carlson et al. (2015); Lessard, Recht & Packard (2016); Loshchilov & Hutter (2016, 2017); Goyal et al. (2017);
Keskar et al. (2017); Dinh et al. (2017); Li, Tai & E (2017); Mandt, Hoffman & Blei (2017); van Laarhoven (2017);
Smith & Le (2018); Gupta, Koren & Singer (2018); Cohen et al. (2021, 2022); Damian, Nichani & Lee (2022); Malladi et
al. (2022); Zhai et al. (2022); Chen et al. (2023); Bernstein & Newhouse (2024); Jordan et al. (2024); Vyas et al.
(2024); Hu et al. (2024); Wen et al. (2024); Defazio et al. (2024); Kalra & Barkeshli (2024); Kosson, Messmer & Jaggi
(2024); Kasimbeg et al. (2025); Liu et al. (2025); Kimi Team (2025); Amsel et al. (2025); Ahn et al. (2025); Wen, Hall,
Ma & Liang (2025); DeepSeek-AI (2026); Khona et al. (2026).

## Problems, with solutions

**1. Gradient descent's linear rate.** For an L-smooth f, show f(x − ∇f(x)/L) ≤ f(x) − ‖∇f(x)‖²/2L. If also
‖∇f‖² ≥ 2μ(f − f*), deduce f(x_k) − f* ≤ (1 − μ/L)^k (f(x₀) − f*).

*Solution.* L-smoothness gives the quadratic upper bound f(y) ≤ f(x) + ∇f(x)ᵀ(y − x) + (L/2)‖y − x‖². Put
y = x − ∇f(x)/L: f(y) ≤ f(x) − ‖∇f‖²/L + ‖∇f‖²/2L = f(x) − ‖∇f‖²/2L. Subtract f* and use the
Polyak–Łojasiewicz inequality ‖∇f‖² ≥ 2μ(f(x) − f*): f(y) − f* ≤ (f(x) − f*) − (μ/L)(f(x) − f*) = (1 − μ/L)(f(x) − f*).
Induction on k gives the claim. (μ-strong convexity implies the inequality: minimize its lower bowl over y.)

**2. The heavy ball, tuned.** On f = (λ/2)x², x_{k+1} = (1 + β − ηλ)x_k − βx_{k−1}. Show that nonreal roots of
z² − (1 + β − ηλ)z + β have modulus √β. Find η, β putting all λ ∈ [μ, L] in this equal-modulus regime, allowing
repeated real roots at its endpoints. Estimate the steps from the dominant root factors for κ = 10⁴ and a 10⁶-fold
objective-gap reduction, against gradient descent with η = 1/L. Explain the limitation of this estimate.

*Solution.* The product of the two roots is β; nonreal roots are conjugate, so |z|² = z z̄ = β. They are nonreal when
(1 + β − ηλ)² < 4β, with the same modulus at equality. The equal-modulus regime is
(1 − √β)² ≤ ηλ ≤ (1 + √β)². Put ημ = (1 − √β)² and ηL = (1 + √β)². Dividing gives
√β = (√κ − 1)/(√κ + 1) and η = 4/(√L + √μ)². For κ = 10⁴, ρ = √β = 99/101. Ignoring polynomial and initialization
prefactors, the gap envelope decays like ρ²ᵏ: k ≈ ln 10⁶ / (−2 ln(99/101)) ≈ 345. Repeated endpoint roots can give
position terms (a + bk)ρᵏ, so this is an asymptotic estimate, not a per-step contraction or guaranteed finite count.
GD's slowest position mode has factor 1 − 10⁻⁴, giving the gap-reduction estimate
ln 10⁶ / [−2 ln(1 − 10⁻⁴)] ≈ 69,000, about two hundred times larger.

**3. SGD's stationary variance.** SGD on f = (λ/2)x² with gradient noise of variance σ²/B: show the stationary
variance is ησ²/(Bλ(2 − ηλ)), and that it depends on η and B only through η/B when ηλ ≪ 1.

*Solution.* x_{k+1} = (1 − ηλ)x_k − ηξ_k with E ξ = 0, Var ξ = σ²/B, independent of x_k. In the stationary state
V = (1 − ηλ)²V + η²σ²/B, so V(2ηλ − η²λ²) = η²σ²/B and V = ησ²/(Bλ(2 − ηλ)). For ηλ ≪ 1, V ≈ (η/B)·σ²/(2λ): only
the ratio η/B enters. (In d dimensions this is the Lyapunov equation of Chapter 4, tr S ≈ (η/2B) tr(H⁻¹C).)

**4. Steepest steps under three norms.** Show that min over ‖Δ‖_∞ ≤ η of gᵀΔ is −η‖g‖₁, attained at −η sign(g), and
that min over ‖Δ‖₂→₂ ≤ η of ⟨G, Δ⟩ is −η‖G‖_* (the nuclear norm, the sum of the singular values), attained at −ηUVᵀ.

*Solution.* gᵀΔ = Σᵢ gᵢΔᵢ ≥ −Σᵢ |gᵢ||Δᵢ| ≥ −η Σᵢ |gᵢ|, with equality when every Δᵢ = −η sign(gᵢ). For matrices write
G = Σᵢ σᵢ uᵢvᵢᵀ; then ⟨G, Δ⟩ = Σᵢ σᵢ uᵢᵀΔvᵢ, and |uᵢᵀΔvᵢ| ≤ ‖Δ‖₂ ≤ η for unit uᵢ, vᵢ, so ⟨G, Δ⟩ ≥ −η Σᵢ σᵢ. The step
Δ = −ηUVᵀ has spectral norm η and uᵢᵀΔvᵢ = −η for every i, so it attains the bound.

**5. Newton–Schulz near one.** For p(σ) = (3/2)σ − (1/2)σ³, show p(1) = 1, p′(1) = 0, and that e = 1 − σ obeys
e ↦ (3/2)e² + O(e³). For q(σ) = 2σ − (3/2)σ³ + (1/2)σ⁵ show q′(1) = 0 too, and find c in e ↦ c e². Which starts
faster from small σ?

*Solution.* p(1) = 3/2 − 1/2 = 1, p′(σ) = 3/2 − (3/2)σ², so p′(1) = 0. Expanding, p(1 − e) = 1 − (3/2)e² + (1/2)e³:
the new error is (3/2)e² − (1/2)e³, quadratic convergence. For q: q(1) = 2 − 3/2 + 1/2 = 1, q′(σ) = 2 − (9/2)σ² +
(5/2)σ⁴, q′(1) = 0, q″(σ) = −9σ + 10σ³, q″(1) = 1, so q(1 − e) = 1 + e²/2 + O(e³): the new signed error is
−e²/2 + O(e³), hence c = −1/2. Its magnitude has leading term e²/2 (the value overshoots one slightly), three times
smaller than the cubic's leading error. Near zero p(σ) ≈ 1.5σ and q(σ) ≈ 2σ:
q starts faster, and Jordan's quintic, with slope 3.4445, faster still, at the price of not converging to 1.

**6. Weight decay's equilibrium, a correlated-update model.** Let W_{t+1} = (1 − ηλ)W_t − ηu_t, with stationary
zero-mean updates satisfying E⟨u_t, u_{t+k}⟩ = U²β^{|k|}, where U² = E‖u_t‖² and 0 ≤ β < 1. Show the equilibrium
E‖W‖² ≈ (ηU²/2λ)(1 + β)/(1 − β) when 0 < ηλ ≪ 1 − β. Do not assume uₜ ⟂ Wₜ.

*Solution.* With a = 1 − ηλ and |a| < 1, unrolling gives W_t = a^t W_0 − η Σ_{m=0}^{t−1} a^m u_{t−1−m};
the finite-second-moment initial transient dies out. By the assumed autocorrelation,
E‖W_t‖² → η²U² Σ_{m,n≥0} a^{m+n} β^{|m−n|} = η²U² (1 + aβ)/((1 − a²)(1 − aβ)).
When ηλ ≪ 1 − β, use 1 − a² ≈ 2ηλ and (1 + aβ)/(1 − aβ) ≈ (1 + β)/(1 − β) to obtain the stated approximation.
For fixed U² and β, the RMS norm scales like √(η/λ). Setting β = β₁ = 0.9 gives the model's factor 19; this is an
approximate correlation model for Chapter 15's AdamW measurements, not a theorem that actual AdamW updates have
exactly that autocorrelation. No measured values or numerical producers are changed by this correction.

Gradient orthogonality under scale invariance does not imply that a momentum update is orthogonal to the current
weights; see [Kosson, Messmer & Jaggi (2024), §3.1](https://arxiv.org/html/2305.17212v3#S3.SS1). If exact uₜ ⟂ Wₜ
were imposed instead, the squared-norm recurrence would give η²U²/(1 − a²), without the correlation multiplier.

## 习题与解答

**1. 梯度下降的线性收敛。** 对 L-光滑的 f，证明 f(x − ∇f(x)/L) ≤ f(x) − ‖∇f(x)‖²/2L。若还有
‖∇f‖² ≥ 2μ(f − f*)，推出 f(x_k) − f* ≤ (1 − μ/L)^k (f(x₀) − f*)。

*解答。* L-光滑给出二次上界 f(y) ≤ f(x) + ∇f(x)ᵀ(y − x) + (L/2)‖y − x‖²。取 y = x − ∇f(x)/L：
f(y) ≤ f(x) − ‖∇f‖²/L + ‖∇f‖²/2L = f(x) − ‖∇f‖²/2L。两边减去 f*，再用波利亚克–洛亚谢维奇不等式
‖∇f‖² ≥ 2μ(f(x) − f*)：f(y) − f* ≤ (1 − μ/L)(f(x) − f*)。对 k 归纳即得。（μ-强凸蕴含这个不等式：对 y 最小化下方的碗。）

**2. 调好参数的重球法。** 在 f = (λ/2)x² 上，x_{k+1} = (1 + β − ηλ)x_k − βx_{k−1}。证明 z² − (1 + β − ηλ)z + β 的
非实根模长为 √β。求出 η、β，使所有 λ ∈ [μ, L] 都处于等模区，允许端点出现实重根。对 κ = 10⁴、目标差距缩小 10⁶ 倍，
用主导根因子估计步数，并与 η = 1/L 的梯度下降比较。说明这个估计的局限。

*解答。* 两根之积为 β；非实根互为共轭，所以 |z|² = z z̄ = β。非实根的条件是 (1 + β − ηλ)² < 4β；等号处的实重根也有相同模长。
等模区为 (1 − √β)² ≤ ηλ ≤ (1 + √β)²。令 ημ = (1 − √β)²，ηL = (1 + √β)²，得到
√β = (√κ − 1)/(√κ + 1)，η = 4/(√L + √μ)²。κ = 10⁴ 时 ρ = √β = 99/101。忽略多项式与初始化的前置因子，
差距包络按 ρ²ᵏ 衰减：k ≈ ln 10⁶ / (−2 ln(99/101)) ≈ 345。端点重根可能产生位置项 (a + bk)ρᵏ，所以这是渐近估计，
不是每步收缩因子，也不是保证达到的有限步数。梯度下降最慢的位置模态因子是 1 − 10⁻⁴，相应的差距缩减估计为
ln 10⁶ / [−2 ln(1 − 10⁻⁴)] ≈ 69000，约为重球法估计的两百倍。

**3. SGD 的平稳方差。** 在 f = (λ/2)x² 上做 SGD，梯度噪声方差为 σ²/B：证明平稳方差是 ησ²/(Bλ(2 − ηλ))，并说明
ηλ ≪ 1 时它只通过 η/B 依赖于 η 和 B。

*解答。* x_{k+1} = (1 − ηλ)x_k − ηξ_k，E ξ = 0，Var ξ = σ²/B，与 x_k 独立。平稳时 V = (1 − ηλ)²V + η²σ²/B，
所以 V(2ηλ − η²λ²) = η²σ²/B，V = ησ²/(Bλ(2 − ηλ))。ηλ ≪ 1 时 V ≈ (η/B)·σ²/(2λ)：只出现比值 η/B。（d 维时就是第4章的
李雅普诺夫方程，tr S ≈ (η/2B) tr(H⁻¹C)。）

**4. 三种范数下的最陡一步。** 证明在 ‖Δ‖_∞ ≤ η 上 gᵀΔ 的最小值是 −η‖g‖₁，在 −η sign(g) 处取到；在 ‖Δ‖₂→₂ ≤ η 上
⟨G, Δ⟩ 的最小值是 −η‖G‖_*（核范数，奇异值之和），在 −ηUVᵀ 处取到。

*解答。* gᵀΔ = Σᵢ gᵢΔᵢ ≥ −Σᵢ |gᵢ||Δᵢ| ≥ −η Σᵢ |gᵢ|，当每个 Δᵢ = −η sign(gᵢ) 时取等号。对矩阵写 G = Σᵢ σᵢ uᵢvᵢᵀ；
于是 ⟨G, Δ⟩ = Σᵢ σᵢ uᵢᵀΔvᵢ，而对单位向量 |uᵢᵀΔvᵢ| ≤ ‖Δ‖₂ ≤ η，所以 ⟨G, Δ⟩ ≥ −η Σᵢ σᵢ。Δ = −ηUVᵀ 的谱范数是 η，
且对每个 i 都有 uᵢᵀΔvᵢ = −η，所以达到这个界。

**5. 1附近的牛顿–舒尔茨迭代。** 对 p(σ) = (3/2)σ − (1/2)σ³，证明 p(1) = 1、p′(1) = 0，并且 e = 1 − σ 满足
e ↦ (3/2)e² + O(e³)。对 q(σ) = 2σ − (3/2)σ³ + (1/2)σ⁵，证明 q′(1) = 0 也成立，并求 e ↦ c e² 中的 c。从小的 σ 出发，
哪个起步更快？

*解答。* p(1) = 3/2 − 1/2 = 1，p′(σ) = 3/2 − (3/2)σ²，所以 p′(1) = 0。展开得 p(1 − e) = 1 − (3/2)e² + (1/2)e³：新的
误差是 (3/2)e² − (1/2)e³，二次收敛。对 q：q(1) = 1，q′(σ) = 2 − (9/2)σ² + (5/2)σ⁴，q′(1) = 0，q″(σ) = −9σ + 10σ³，
q″(1) = 1，所以 q(1 − e) = 1 + e²/2 + O(e³)：新的有符号误差是 −e²/2 + O(e³)，因此 c = −1/2。
误差大小的首项是 e²/2（值略微越过1），是三次多项式首项的三分之一。在0附近
p(σ) ≈ 1.5σ，q(σ) ≈ 2σ：q 起步更快；乔丹的五次多项式斜率是 3.4445，更快，代价是不收敛到1。

**6. 权重衰减的平衡：相关更新模型。** 令 W_{t+1} = (1 − ηλ)W_t − ηu_t，更新平稳且均值为零，并满足
E⟨u_t, u_{t+k}⟩ = U²β^{|k|}，其中 U² = E‖u_t‖²、0 ≤ β < 1。证明 0 < ηλ ≪ 1 − β 时，平衡值
E‖W‖² ≈ (ηU²/2λ)(1 + β)/(1 − β)。不要假设 uₜ ⟂ Wₜ。

*解答。* 令 a = 1 − ηλ、|a| < 1，展开得 W_t = a^t W_0 − η Σ_{m=0}^{t−1} a^m u_{t−1−m}；初始值二阶矩有限时，
初始瞬态衰减掉。由假定的自相关，E‖W_t‖² → η²U² Σ_{m,n≥0} a^{m+n} β^{|m−n|}
= η²U² (1 + aβ)/((1 − a²)(1 − aβ))。ηλ ≪ 1 − β 时，1 − a² ≈ 2ηλ，且
(1 + aβ)/(1 − aβ) ≈ (1 + β)/(1 − β)，得到所述近似。U²、β 固定时，均方根范数按 √(η/λ) 缩放。
取 β = β₁ = 0.9，模型给出因子19；这是对第15章 AdamW 测量的近似相关模型，并不证明真实更新恰有这样的自相关。
这项更正不改变任何测量值或数值计算程序。

尺度不变性下梯度与权重正交，并不意味着动量更新也与当前权重正交，见
[Kosson、Messmer 与 Jaggi（2024）第3.1节](https://arxiv.org/html/2305.17212v3#S3.SS1)。若另行严格要求 uₜ ⟂ Wₜ，
范数平方递推会给出 η²U²/(1 − a²)，不带相关性乘数。

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| steepest descent | 最速下降 |
| L-smooth, μ-strongly convex | L-光滑，μ-强凸 |
| condition number (κ) | 条件数（κ） |
| descent lemma, Polyak–Łojasiewicz inequality | 下降引理，波利亚克–洛亚谢维奇不等式 |
| linear convergence, contraction factor | 线性收敛，收缩因子 |
| heavy ball (Polyak momentum) | 重球法（波利亚克动量） |
| Nesterov's accelerated gradient, look-ahead | 涅斯捷罗夫加速梯度，前瞻 |
| lower bound (Nemirovski–Yudin) | 下界（涅米罗夫斯基–尤丁） |
| stochastic approximation (Robbins–Monro) | 随机逼近（罗宾斯–门罗） |
| stationary covariance, Lyapunov equation | 平稳协方差，李雅普诺夫方程 |
| temperature (η/B), linear scaling rule, square-root rule | 温度（η/B），线性缩放规则，平方根规则 |
| sharp minimum, flat minimum | 尖锐极小值，平坦极小值 |
| sharpness, edge of stability | 锐度，稳定性边缘 |
| progressive sharpening, self-stabilization | 渐进锐化，自稳定 |
| power iteration, Hessian-vector product | 幂迭代，黑塞–向量积 |
| AdaGrad, RMSProp, Adam, AdamW | AdaGrad，RMSProp，Adam，AdamW |
| bias correction | 偏差校正 |
| sign descent, Lion | 符号下降，Lion |
| L2 regularization, decoupled weight decay | L2正则化，解耦权重衰减 |
| natural gradient, Fisher information matrix | 自然梯度，费希尔信息矩阵 |
| Kronecker product, K-FAC | 克罗内克积，K-FAC |
| preconditioner, preconditioning | 预条件子，预条件 |
| Shampoo, grafting, SOAP, eigenbasis | Shampoo，嫁接，SOAP，特征基 |
| orthogonalization, polar factor (UVᵀ) | 正交化，极分解因子（UVᵀ） |
| spectral norm, nuclear norm | 谱范数，核范数 |
| Muon, Newton–Schulz iteration | Muon，牛顿–舒尔茨迭代 |
| hybrid Newton–Schulz | 混合牛顿–舒尔茨迭代 |
| AlgoPerf, external tuning, self-tuning | AlgoPerf，外部调参，自调参 |
| learning-rate sweep, grid edge | 学习率扫描，网格边缘 |
| warmup, cosine schedule, warmup–stable–decay (WSD) | 预热，余弦调度，预热–稳定–衰减（WSD） |
| river valley, river and hill loss | 河谷，河损失与山坡损失 |
| cool-down branch | 冷却分支 |
| iterate averaging (Polyak–Ruppert), EMA of weights | 迭代平均（波利亚克–鲁珀特），权重的指数移动平均 |
| schedule-free optimization | 免调度优化 |
| attention logit (score) growth, QK-clip, MuonClip | 注意力分数增长，QK-Clip，MuonClip |
| gradient clipping | 梯度裁剪 |
| scale invariance, norm equilibrium, effective learning rate | 尺度不变性，范数平衡，有效学习率 |
