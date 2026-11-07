# Statistics, Built — Part 9: Estimation

Part 9 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Part 8 showed how a statistic varies from
sample to sample. This part asks where good estimators come from, how to improve them, and how good any of them can be.

It opens with the German tank problem. In the Second World War, Allied statisticians estimated German tank production
from the serial numbers on captured tanks, and came much closer than conventional intelligence. Ruggles & Brodie
(1947) give, for example, 169 vs 1,000 vs 122 (statistical estimate, intelligence, German records) for June 1940.
From there the part covers:
- estimators as recipes, graded by their sampling distributions;
- the method of moments (Pearson 1894);
- maximum likelihood (Fisher 1912, 1922): likelihood curves sharpening, the score, invariance, the boundary MLE,
  Newton's method;
- consistency by Kullback–Leibler, asymptotic normality, the standard error from the curvature, and where the theory
  breaks (Neyman–Scott);
- sufficiency and the factorization theorem;
- Rao–Blackwell, which turns the tank moment estimator into the scaled maximum;
- completeness, Lehmann–Scheffé and the UMVUE ("the maximum plus the average gap");
- Fisher information, as the score's variance, as curvature, and as the curvature of KL;
- the Cramér–Rao bound by Cauchy–Schwarz, its geometry, when it is attained, and how the tanks beat it (rate 1/k);
- comparing estimators on an MSE board under three worlds.

Every number on screen is computed in [`compute.py`](compute.py). The Museum supplies:
- the tank figures (`museum.TANKS`, from Ruggles & Brodie 1947);
- Bortkiewicz's horse kicks (`museum.HORSEKICK_*`, Part 3).

Everything else is a seeded simulation or an exact calculation, and is tagged as such.

**Built in this part:** the tank factory game, [`explainer/stats/kit/estimation.py`](../../../explainer/stats/kit/estimation.py)
(tested in `tests/test_stats_kit_estimation.py`). `tank_game(recipe, N, k, reps, model)` grades any estimator of N,
given as a function of a `(reps, k)` array of captured serials, on simulated factories. It reports the bias, the SD
and the RMSE; bias and RMSE include Monte Carlo errors, under the textbook model (`"uniform"`) or a world the recipe did not assume
(`"newer"`: sequential capture weights increase from 1 to 3; `"offset"`: serials start at 1,001). The module also has `newton`
and `observed_information`. The `TankFactory` picture is in `explainer/stats/viz.py`.

| RMSE, N = 300, k = 5 | uniform | newer | offset |
|---|---|---|---|
| 2x̄ − 1 | 76.7 | 87.9 | 2,001 |
| max (MLE) | 64.0 | 48.0 | 951 |
| m(1 + 1/k) − 1 (UMVUE) | **49.8** | **42.0** | 1,200 |
| (m − m₁)(k + 1)/(k − 1) − 1 | 79.6 | 83.0 | **79.0** |

## Build it

```bash
python -m videos.stats.stats9.compute          # once: every computed item (seconds; cached in .cache/stats9)
python tools/build.py stats9 -q l              # fast 480p preview
python tools/build.py stats9                   # 1080p30 -> renders/stats9.mp4
python tools/qa_scene.py stats9 CramerRao      # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats9 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | The German tank problem | Ruggles & Brodie's story and table; the factory in miniature; objectives. | 169 / 1,000 / 122; 244 / 1,550 / 271; 327 / 1,550 / 342. One factory, N = 300, serials 4, 25, 70, 98, 208, 214: 2x̄ − 1 = 205, max 214, UMVUE 249 |
| 1 | Estimators as recipes | Model, estimator, estimate; three factories; the sampling distributions of three recipes; RMSE against k; where recipes come from. | k = 6: SD 70 (2x̄ − 1), RMSE 56 (max, bias −42), SD 43 (UMVUE); rates 1/√k vs 1/k |
| 2 | The method of moments | Pearson's crabs; the recipe; a gamma fit; the tanks by moments; MoM vs MLE; the delta method; GMM. | x̄ = 4.80, s² = 7.35 → α̂ = 3.14, β̂ = 1.53 (truth 2.5, 2); SD 0.621 vs 0.523, efficiency 0.71 |
| 3 | Maximum likelihood | Fisher 1912/1922; the likelihood as a flipped pmf; sharpening with n; the score; the horse kicks; the tank likelihood; invariance. | 7 of 10: L = 0.009, 0.117, 0.267, 0.057 at p = 0.3, 0.5, 0.7, 0.9; λ̂ = 122/200 = 0.61; expected 108.7, 66.3, 20.2, 4.1, 0.6 vs 109, 65, 22, 3, 1; e^(−0.61) = 0.543 |
| 4 | Likelihoods in practice | The normal (divisor n) and its likelihood surface; the exponential; the uniform's boundary MLE; Newton on the gamma shape, with quadratic convergence. | λ̂ = 0.591 (12 waits); θ̂ = 9.24 (8 draws); Newton errors 8.3 × 10⁻⁴, 2.3 × 10⁻⁷, 1.8 × 10⁻¹⁴ |
| 5 | How good is the MLE? | Average log-likelihoods converge (Wald 1949); KL ≥ 0 by Jensen; asymptotic normality by Taylor + CLT + Slutsky; SE from the curvature; simulation check; small-n skew; regularity and its failures. | horse kicks: J = 327.9, SE 0.0552, CI [0.502, 0.718]; Poisson SDs 0.187/0.187 (n = 20) … 0.0265/0.0265 (n = 1,000) |
| 6 | Sufficiency | Ten orders of two heads; the definition; Alice and Bob; factorization (discrete proof); a catalogue; the tanks' maximum; minimal sufficiency and Pitman–Koopman–Darmois. | P(each order ∣ S = 2) = 0.1 for p = 0.2, 0.5, 0.8 |
| 7 | Rao–Blackwell | Rao 1945, Blackwell 1947; the theorem; proof by Eve's law and Jensen; P(X = 0) for Poisson; the tank moment estimator collapsing onto the UMVUE; Rao–Blackwellization elsewhere. | SD 0.500 → 0.134 (variance ÷ 14); tanks SD 70.4 → 42.3 |
| 8 | The best unbiased estimator | Three roads to one estimator; completeness; Lehmann–Scheffé; the tank maximum is complete (triangular system); the average gap; exponential families; the absurd UMVUE (−1)ˣ. | gaps 3, 20, 44, 27, 109, 5; average 34.7; 214 + 34.7 = 248.7 |
| 9 | Fisher information | E u = 0; I = Var u = −E u′; forty score curves; a catalogue; the coin; reparametrization and the log-odds; the information matrix and nuisance parameters; KL's curvature. | score at λ₀: variance 26.1 vs n/λ = 28.6 (40 samples) |
| 10 | The Cramér–Rao bound | Rao, Cramér, Fréchet, Darmois, Aitken & Silverstone; the statement; the proof by Cauchy–Schwarz; the geometric picture; attainment means an exponential family; the exponential rate; the tanks beat it; biased estimators and Hodges. | exponential: UMVUE at n/(n − 2) × the bound (1.67 at n = 5, 1.02 at n = 100); tanks: SD 13.8 vs 33.5 at k = 20 for a 1/√k rate matched at k = 2 |
| 11 | Comparing estimators | The MSE board under three worlds; the MSE-optimal multiple of m; the tank factory game; efficiency versus robustness. | the table above; a* = 1.167: RMSE 49.7 vs 50.4 |
| 12 | Outro | Recap, payoffs, problems, references, the Transcript, Part 10's question. | — |

## Sources

- **Tanks.**
  - R. Ruggles & H. Brodie, "An empirical approach to economic intelligence in World War II", *JASA* 42 (1947).
  - L. Goodman, "Serial number analysis", *JASA* 47 (1952).
- **Moments.**
  - K. Pearson, *Phil. Trans. R. Soc. A* 185 (1894).
  - L. P. Hansen, *Econometrica* 50 (1982).
- **Likelihood.**
  - R. A. Fisher, *Messenger of Mathematics* 41 (1912); *Phil. Trans. R. Soc. A* 222 (1922).
  - A. Wald, *Ann. Math. Stat.* 20 (1949).
  - J. Neyman & E. Scott, *Econometrica* 16 (1948).
  - P. Zehna, *Ann. Math. Stat.* 37 (1966).
  - S. Kullback & R. Leibler, *Ann. Math. Stat.* 22 (1951).
  - S. Stigler, "The epic story of maximum likelihood", *Stat. Sci.* 22 (2007).
- **Sufficiency and unbiasedness.**
  - J. Neyman, *Giorn. Ist. Ital. Attuari* 6 (1935); P. Halmos & L. J. Savage, *Ann. Math. Stat.* 20 (1949).
  - C. R. Rao, *Bull. Calcutta Math. Soc.* 37 (1945).
  - D. Blackwell, *Ann. Math. Stat.* 18 (1947).
  - E. Lehmann & H. Scheffé, *Sankhyā* 10 (1950), 15 (1955).
  - E. Pitman (1936); B. Koopman (1936); G. Darmois (1935).
  - A. Gelfand & A. F. M. Smith, *JASA* 85 (1990).
- **Bounds.**
  - H. Cramér, *Mathematical Methods of Statistics* (1946).
  - M. Fréchet (1943); A. Aitken & H. Silverstone (1942).
  - L. Le Cam, *Univ. Calif. Publ. Stat.* 1 (1953), on Hodges' estimator.
- **Textbooks.**
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), chs. 6–7.
  - E. Lehmann & G. Casella, *Theory of Point Estimation* (2nd ed., 1998).
  - J. Rice, *Mathematical Statistics and Data Analysis* (3rd ed., 2007), ch. 8.
  - L. Wasserman, *All of Statistics* (2004), ch. 9.

## Problems and solutions

**1. Moments for the Beta.**

*Solution.* With m = x̄, matching E X = α/(α + β) = m and Var X = m(1 − m)/(α + β + 1) = v gives
α + β = m(1 − m)/v − 1 =: c. So α̂ = m·c and β̂ = (1 − m)·c. This needs v < m(1 − m), and v > 0; these hold for a nonconstant sample in (0, 1) when v uses divisor n.

**2. The Pareto.**

*Solution.* ℓ(θ) = n log θ − (θ + 1)Σ log xᵢ, so U(θ) = n/θ − Σ log xᵢ and θ̂ = n/Σ log xᵢ. Next, −∂²/∂θ² log p = 1/θ²,
so I(θ) = 1/θ² and SE(θ̂) ≈ θ̂/√n. (log X is exponential with rate θ, so θ̂ is chapter 4's exponential MLE in
disguise.)

**3. The uniform.**

*Solution.* p_θ(x) = θ⁻ⁿ 1{M ≤ θ} · 1{min xᵢ ≥ 0}, so M is sufficient by factorization. M has density n mⁿ⁻¹/θⁿ on
(0, θ). If E_θ g(M) = 0 for all θ, then ∫₀^θ g(m) mⁿ⁻¹ dm = 0 for all θ. Differentiating in θ gives g(θ)θⁿ⁻¹ = 0, so
g = 0 almost everywhere, and M is complete. Since E M = nθ/(n + 1), the UMVUE is (n + 1)M/n by Lehmann–Scheffé.

**4. A Rao–Blackwellized probability.**

*Solution.* 1{X₁ ≤ c} is unbiased for Φ(c − μ), and X̄ is complete and sufficient. For n > 1, (X₁, X̄) is bivariate normal with
Cov(X₁, X̄) = 1/n = Var X̄, so X₁ ∣ X̄ ~ N(X̄, 1 − 1/n). Hence

E(1{X₁ ≤ c} ∣ X̄) = Φ((c − X̄)/√(1 − 1/n)),

the UMVUE. It is not the plug-in Φ(c − X̄), which is biased.

**5. The Cramér–Rao bound for a normal variance.**

*Solution.* log p = −log σ − x²/(2σ²) + const, so u = −1/σ + x²/σ³ and I(σ) = Var(X²)/σ⁶ = 2σ⁴/σ⁶ = 2/σ². For
ψ(σ) = σ², ψ′ = 2σ, and the bound is (2σ)²/(n · 2/σ²) = 2σ⁴/n. The estimator (1/n)Σxᵢ² is unbiased with variance
2σ⁴/n, so the bound is attained. This is the exponential-family case: T = Σxᵢ², estimating its own mean. With μ
unknown, s² has variance 2σ⁴/(n − 1) and does not attain it.

**6. The tank estimator is unbiased.**

*Solution.* P(m = j) = C(j − 1, k − 1)/C(N, k), and j·C(j − 1, k − 1) = k·C(j, k). By the hockey-stick identity,
Σⱼ₌ₖᴺ C(j, k) = C(N + 1, k + 1). So

E m = k·C(N + 1, k + 1)/C(N, k) = k(N + 1)/(k + 1),

and E[m(1 + 1/k) − 1] = (N + 1) − 1 = N.

## Where it comes back

| Idea | Returns in |
|---|---|
| likelihood, the MLE, Fisher information | 10, 14, 22, 24, 47 |
| Newton's method, Fisher scoring, EM | 21, 24, 27 |
| sufficiency, exponential families | 22, 45 |
| Rao–Blackwell, conditioning | 18, 27, 45 |
| completeness, the UMVUE | 45 |
| Cramér–Rao, efficiency | 45, 47, 49, 50 |
| irregular rates, superefficiency | 47, 50 |
| misspecification, robustness | 22, 30, 60 |
| the tank factory game, statkit | every part that grades an estimator |
