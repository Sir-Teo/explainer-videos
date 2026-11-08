# Statistics, Built — Part 64: Statistics in the Age of AI

Part 64 of [the 65-part course](../README.md). Every example is constructed arithmetic or seeded simulation, with no real model evaluated and no API calls. Published empirical results are attributed to their original papers rather than represented as new experiments.

## Audited demonstrations

[Local checked kernels](checked.py) implement this part's numerical corrections; shared kit behavior remains available for comparison.

- **Headline:** replace rejection-searching for a desired benchmark with an explicitly constructed 2x2 table: both correct 776, A only 76, B only 71, neither 77. Scores are 85.2% and 84.7%; paired 95% interval (-1.88, 2.88) percentage points; exact McNemar p=0.74159. A separate 4,000-benchmark latent-probit simulation gives strict order reversals 33.30% (MC SE 0.75 points), and **117 ties**, now counted rather than hardcoded zero. The reversal probability depends on the joint score model, not just the two marginal accuracies.
- **Clusters and pairs:** use numerical quadrature for the logistic-normal population mean 0.74855368 and exact design effect 2.74589, ICC 0.19399, rather than a large simulation as truth. Latent baseline .8 is not the marginal accuracy. Analytic benchmark SD 0.022734 and empirical repeated-benchmark SD 0.023098 are distinguished. Coverage is 76.00% iid versus 94.55% CR1 (MC SE 0.51 points). Paired coverage targets the exact .005 gap, not a noisy two-million-draw approximation: 98.90% unpaired versus 95.30% paired. Power at n=1,000 is 17.25% versus 31.00% with 400 repetitions; pairing benefits depend on covariance.
- **Arenas and rank:** check logistic convergence and information rank; require a strongly connected win graph for finite Bradley–Terry MLEs. Store full model/sandwich covariance and check contrast invariance to reference changes. Replace marginal-interval-overlap ranks with Bonferroni simultaneous pairwise Wald contrasts: the current asymptotic rank-one set is **[7]** (zero-based, model H). Marginal intervals are labeled separately; the reference's zero variance is parametrization, not an absolutely known strength. The H–G sandwich contrast covers 94.67% across 300 arenas (MC SE 1.30 points). Independent-battle sandwich/bootstrap do not correct voter/prompt clustering or selection. Style adjustment targets a conditional equal-length comparison; output length is not automatically a causal confounder. Elo permutation ranges are descriptive order sensitivity, not confidence intervals.
- **IRT:** replace unchecked alternating updates as a claimed joint MLE with bounded penalized joint optimization initialized by those updates. Final affine standardization preserves logits. Checked projected gradient 5.68e-05; objective 20169.69006, 1097 iterations. This is a local nonconvex optimum, not a global certificate. Conditional on one fitted item bank, 300 new-model full-benchmark RMSEs are 4.442, 3.387, 2.950 points for raw random 100, IRT random 100 and spread anchors. Their target is the realized full 1,000-item response mean, partly overlapping the anchor responses, not an independent superpopulation accuracy. The tinyBenchmarks under-two-point result is an empirical paper result, not an individual-model guarantee.
- **Holdout reuse:** use matched data seeds for reuse and the noisy-threshold comparison. The simplified Gaussian-correlation routine has unbounded queries, no persistent noisy threshold or finite exceptional-disclosure budget, so it is explicitly a **heuristic**, not formal Thresholdout or a DP certificate. Reuse reaches 63.35% while fresh accuracy stays around 50%; the heuristic reports 51.73–55.81% in five matched runs. Explain the formal bounded-query, budgeted algorithm separately. Private adaptive generalization is quantitative, not an unconditional inability to overfit. Familiarity contrasts are not proof of contamination without controls.
- **Judges:** PPI expectation/variance cancellation assumes a fixed independently fitted predictor and independent labeled/unlabeled draws from a common population, or a suitable alternative design. Normal intervals are asymptotic. Judge-only, human-only and PPI cover 2.60%, 94.25%, 94.80% across 2,000 experiments; MC SEs saved. Unequal-probability labeling can be valid with known positive probabilities and weighting. Human agreement is not a universal accuracy ceiling.
- **Collapse:** fix the hidden initial-fit off-by-one. Both experiments start with fitted mean zero and variance one, with a standardized initial sample for accumulation. Exactly E[V_t]=((n-1)/n)^t after t replacement refits; analytic log drift -0.10484722. Positive finite-time variances converge to zero; this is not finite-time absorption. Accumulation is a separate retained-pool process, and its behavior is not a theorem for every synthetic-data pipeline.
- **Conformal factuality:** require exchangeable whole responses, fixed scoring/decomposition and reliable labels. Claim dependence within a response is allowed. Strict thresholding handles ties, no-false-claim calibration responses and the infinite threshold. Empty retained answers count as safe. At alpha .1 safety is 89.925% (MC SE 0.148 points) and 56.140% of claims retained. MC errors are computed across 300 independent calibrations rather than treating their 200 shared-threshold tests as independent. The raw all-true probability is exact .8^8=0.16777216.
- **Watermarks:** exact binomial power is exact for the stated independent-indicator mixture only. Hashing, key reuse and repetitions do not establish that null for every human text. Use strict integer rejection boundaries and length-specific exact tails. Random token-type mixtures differ from fixed counts or arbitrary paraphrases. A z-tail is not posterior authorship probability. Distortion-free properties must name key/randomness averaging; the SynthID feedback experiment is evidence on measured quality, not exact equivalence by nonsignificance.
- **SBI:** compare residual-variance choices using the *same* fitted polynomial mean and fresh test pairs. Add an exact conjugate-posterior reference. At N=30, prior-predictive coverage is 67.09% in-sample versus 93.44% held-out RMS; MC SEs across 20 independent fits are saved. Held-out RMS is a heuristic and does not certify conditional posterior calibration. Uniform basic SBC ranks are necessary, not sufficient: a data-ignoring prior can pass.
- **Diffusion:** start each score's flow from its actual noised mixture, sharing component uniforms and Gaussian draws. Use 400 noise levels and check against 200: RMS refinements true/empirical/smoothed are 0.000104, 7.5e-05, 0.000101. Endpoint sigma .01 and numerical integration leave approximation error; empirical-score samples lie near rather than exactly on training atoms. Median nearest distances are 0.00576, 0.06088, 0.06052; equal distance is not a full generalization test. Remove density clipping. Nearly minimax theory needs the cited smoothness/network/training assumptions and logarithmic qualifications, not arbitrary networks.
- **Deployments:** match buyer count/supply per market so the global and market-randomized contrasts target the same finite-market distribution. Weighted allocation among demanders is stated. A/B mean 0.22542 (MC SE 0.00090); global 0.04958 (0.00042); market-randomized 0.05002 (0.00014). Twenty markets involve 80,000 buyers against 4,000 in one A/B market, so precision is not a fixed-budget design comparison. Plot bars are repeated-experiment SDs, not CIs for Monte Carlo means. Surrogate transport needs comparability as well as surrogacy and causal/overlap assumptions.

## Verification

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m videos.stats.stats64.compute --force
pytest -q tests/test_stats64_checked.py tests/test_stats_kit_evals.py
python tools/build.py stats64 -q l
python tools/lecture_length.py stats64 --floor 50
```

All 15 chapters reviewed; all 15 inputs regenerated; **23 checks pass** (16 audited local, seven legacy). Initial numerical-check failures and successful refinements are retained in the [evidence](../../../docs/qa/evidence/stats64-polish-20261107/README.md). Narration estimate 64.0 minutes. English sampled visual review complete; Chinese narration/caption tables, continuous listening/playback and final masters remain open.

## Sources

- **Benchmarks and pairs.** E. Miller, "Adding Error Bars to Evals", arXiv:2411.00640 (2024); Q. McNemar,
  *Psychometrika* 12 (1947); L. Kish, *Survey Sampling* (1965).
- **Arenas.**
  - E. Zermelo, *Math. Z.* 29 (1929); R. Bradley & M. Terry, *Biometrika* 39 (1952); D. Hunter, *Ann. Statist.* 32
    (2004);
  - W.-L. Chiang et al., "Chatbot Arena", ICML (2024); LMSYS, "Does style matter? Disentangling style and substance
    in Chatbot Arena" (28 August 2024).
- **IRT.** A. Birnbaum, in Lord & Novick, *Statistical Theories of Mental Test Scores* (1968); F. Lord (1980);
  F. Maia Polo et al., "tinyBenchmarks", ICML (2024).
- **Holdouts.** C. Dwork, V. Feldman, M. Hardt, T. Pitassi, O. Reingold & A. Roth, *Science* 349 (2015); A. Blum &
  M. Hardt, ICML (2015).
- **Labels from models.** A. Angelopoulos, S. Bates, C. Fannjiang, M. Jordan & T. Zrnic, *Science* 382 (2023);
  N. Egami, M. Hinck, B. Stewart & H. Wei, NeurIPS (2023); J. Cohen, *Educ. Psychol. Meas.* 20 (1960).
- **Collapse.** I. Shumailov et al., *Nature* 631 (2024); M. Gerstgrasser et al., "Is model collapse inevitable?"
  (2024).
- **Uncertainty.**
  - S. Kadavath et al., "Language models (mostly) know what they know" (2022); OpenAI, "GPT-4 technical report"
    (2023);
  - C. Mohri & T. Hashimoto, ICML (2024); V. Quach et al., ICLR (2024).
- **Watermarks.** J. Kirchenbauer et al., ICML (2023); R. Kuditipudi et al. (2023); S. Dathathri et al., *Nature* 634
  (2024).
- **Simulators.** K. Cranmer, J. Brehmer & G. Louppe, *PNAS* 117 (2020); J. Hermans et al., TMLR (2022); S. Talts et
  al. (2018).
- **Diffusion.**
  - J. Sohl-Dickstein et al., ICML (2015); Y. Song & S. Ermon, NeurIPS (2019); J. Ho, A. Jain & P. Abbeel, NeurIPS
    (2020); Y. Song et al., ICLR (2021);
  - H. Robbins (1956); K. Oko, S. Akiyama & T. Suzuki, ICML (2023).
- **Deployments.** R. Johari, H. Li, I. Liskovich & G. Weintraub, *Management Science* (2022); S. Athey, R. Chetty,
  G. Imbens & H. Kang (2019).
- **Open problems.** L. Cronbach & P. Meehl, *Psychol. Bull.* 52 (1955).

## Problems and solutions

1. **CR1 with singleton clusters.**
   - With G = n clusters of one, the cluster sums are the residuals rᵢ.
   - So SE² = n/(n − 1) · Σrᵢ²/n² = Σrᵢ²/(n(n − 1)) = s²/n.
2. **The paired variance and McNemar.**
   - ā − b̄ is the mean of dᵢ = aᵢ − bᵢ, so its variance is Var(d)/n = (σ_a² + σ_b² − 2σ_ab)/n.
   - dᵢ is 1, −1 or 0, so Σdᵢ = n₁₀ − n₀₁. Conditioning on the n₁₀ + n₀₁ discordant questions, each is equally
     likely to be +1 or −1 under the null, so the test uses only n₁₀ and n₀₁.
3. **Bradley–Terry.**
   - The log-likelihood is Σ[yₖ xₖ·θ − log(1 + e^{xₖ·θ})] with xₖ = e_i − e_j. Its Hessian is −Σ pₖ(1 − pₖ)xₖxₖᵀ,
     which is negative semidefinite, so it is concave.
   - Each xₖ sums to zero, so adding c to every θ leaves every xₖ·θ unchanged: only differences are identified.
4. **The Gaussian's collapse.**
   - Starting from fitted variance σ̂²₀=1, σ̂²ₜ = Π_{s ≤ t} χ²_{n−1,s}/n with independent factors, so E σ̂²ₜ = ((n − 1)/n)ᵗ.
   - log σ̂²ₜ / t → E log(χ²_{n−1}/n) by the strong law. By Jensen, that is below log((n − 1)/n) < 0, so
     log σ̂²ₜ → −∞ and σ̂²ₜ → 0 almost surely.
5. **Prediction-powered inference.**
   - E f̄_N = E f and E(y − f)‾ₙ = E y − E f, so the sum has expectation E y for a fixed predictor independent of the labeled/unlabeled samples, from a common target population. A predictor trained on these labels needs fitting-dependence control such as cross-fitting.
   - The two averages are over independent samples, so the variance is Var(f)/N + Var(y − f)/n.
6. **Tweedie.**
   - p_σ(y) = ∫ φ_σ(y − x)p(x)dx. Differentiating under the integral, ∇p_σ(y) = ∫ (x − y)/σ² · φ_σ(y − x)p(x)dx.
   - Dividing by p_σ(y) gives ∇log p_σ(y) = (E[x | y] − y)/σ². Rearranging gives the formula.


## Next

Part 65 puts the research workflow and course promises under review.
