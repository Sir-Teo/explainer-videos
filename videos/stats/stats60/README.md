# Statistics, Built — Part 60: Robustness and Distribution Shift

Part 60 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fifth part of Stage V, the research frontier.

It opens with Recht, Roelofs, Schmidt & Shankar (2019). They rebuilt ImageNet's test set from new images, following the
original collection process as closely as they could, and every model they tested lost between 11 and 14 points of
top-1 accuracy. The models kept their order, so this was not overfitting to a reused test set. A small, invisible
change in the distribution had done it. The part covers the two ways the standing assumption, data from the
distribution of interest, breaks: some of the data are wrong, or all of the data are right but come from elsewhere.
- Tukey's depth (1975) on Old Faithful: the depth map, the Tukey median, its breakdown point, and Chen, Gao & Ren's
  (2018) minimax optimality under Huber contamination. Its cost is time exponential in the dimension.
- Efficient robust means (Diakonikolas, Kamath, Kane, Li, Moitra & Stewart 2016; Lai, Rao & Vempala 2016):
  - the (2, …, 2) attack, against which the mean and the coordinatewise and geometric medians all err like ε√d;
  - the spectral filter and why a small top eigenvalue certifies the mean;
  - sum-of-squares, and the SQ lower bound ε√log(1/ε) (Diakonikolas, Kane & Stewart 2017).
- List-decodable learning (Charikar, Steinhardt & Valiant 2017): a list of ⌈1/α⌉ candidates when only α of the data
  are inliers, with its two lower bounds.
- Heavy tails: median of means (Nemirovski & Yudin; Alon, Matias & Szegedy), the δ-dependence theorem (Devroye,
  Lerasle, Lugosi & Oliveira 2016), tournaments (Lugosi & Mendelson 2019) and Hopkins's (2020) efficient version, and
  Catoni.
- Covariate shift (Shimodaira 2000) on NHANES: importance weights estimated by a classifier, Kish's effective sample
  size, clipping, KMM and KLIEP, the doubly robust form, and weighted conformal.
- Label shift on the Wisconsin biopsies: classify and count and its attenuation, Forman's adjusted count, BBSE (Lipton,
  Wang & Smola 2018), the Saerens–Latinne–Decaestecker EM, and recalibration.
- Distributionally robust optimization:
  - φ-divergence, Wasserstein and group uncertainty sets;
  - χ² DRO as variance regularization (Duchi & Namkoong) and the KL dual;
  - the square-root lasso as a Wasserstein DRO (Blanchet, Kang & Murthy);
  - fairness without demographics (Hashimoto et al. 2018) and Hu et al.'s (2018) caveat.
- Invariance: invariant causal prediction (Peters, Bühlmann & Meinshausen 2016), anchor regression (Rothenhäusler,
  Meinshausen, Bühlmann & Peters 2021), and IRM with its critiques.
- Transfer learning:
  - Ben-David et al.'s (2010) bound, Kpotufe & Martinet's (2021) transfer exponent, and Cai & Wei (2021);
  - Trans-Lasso (Li, Cai & Li 2022), with negative transfer simulated;
  - domain-adversarial networks and their failure under label shift.
- Detecting shift: the MMD (Gretton et al. 2012), classifier two-sample tests (Lopez-Paz & Oquab 2017), Failing Loudly
  (Rabanser, Günnemann & Lipton 2019), and tests for harmful shift (Podkopaev & Ramdas 2022).
- Five open problems.

It keeps two promises:
- **Part 30** built robust estimators of location and scale in one dimension. Chapters 1–4 take robustness into many
  dimensions, efficiently.
- **Part 57**'s weighted conformal assumed the shift's weights were known. Chapters 5–6 estimate them and count the
  price.

**Built in this part:**
- **`statkit.shift`** ([`explainer/stats/kit/shift.py`](../../../explainer/stats/kit/shift.py)), tested in
  `tests/test_stats_kit_shift.py`:
  - Tukey depth in the plane and the Tukey median;
  - the contamination attack, Weiszfeld's geometric median, the spectral filter, and a robust-means harness;
  - list decoding by clustering, and median of means with the geometric median;
  - Kish's effective sample size, weighted intervals, and logistic density-ratio estimation;
  - BBSE and EM for label shift;
  - χ² and KL distributionally robust risks by duality (the χ² case checked against mean + √(2ρ Var), the KL case
    against a brute-force tilt);
  - anchor regression (OLS at γ = 1, IV as γ → ∞, both tested) and ICP;
  - the two-step Trans-Lasso;
  - the unbiased MMD with its permutation test.
- **The depth map** (`DepthMap` in `explainer/stats/viz.py`), the part's instrument. It shades every cell of a grid by
  its Tukey depth, plots the data, and marks centres such as the Tukey median and the mean, so robust and non-robust
  centres can be compared as outliers arrive.

**Data.**
- From the Museum:
  - Old Faithful (Azzalini & Bowman 1990), with 30 planted points;
  - NHANES (age, sex, BMI, systolic pressure), with a simulated young-skewed selection;
  - the Wisconsin breast cancer biopsies (Wolberg, Street & Mangasarian 1995), with a simulated label shift.
- The rest is seeded simulation.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Unweighted interval, shifted sample | NHANES pressure, young-skewed n = 600 | 95% | 0.0% | broken |
| Importance-weighted interval | NHANES pressure, young-skewed n = 600 | 95% | 95.5% | kept |
| Classify-and-count prevalence interval | biopsies, 37% → 70% malignant | 95% | 85% | broken |
| BBSE label-shift interval | biopsies, 37% → 70% malignant | 95% | 95% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats60.compute   # once (a few minutes)
python tools/build.py stats60 -q l                         # fast 480p preview
python tools/build.py stats60                              # 1080p30 -> renders/stats60.mp4
python tools/qa_scene.py stats60 Depth
python tools/lecture_length.py stats60 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Recht et al. | ImageNetV2: every model 11–14 points lower; NHANES (N = 5,176, mean SBP 126.19): samples of 600 with mean age 35 (population 50); unweighted mean 118.8, 0% coverage; weighted 126.2, 95.5% |
| 1 | Depth | Old Faithful, 272 eruptions, depth over 720 directions: Tukey median (3.81, 7.44), depth 0.41; mean (3.49, 7.09); 30 planted points move the mean 0.45 and the Tukey median 0.10 |
| 2 | The filter | n = 2,000, ε = 0.1, the (2, …, 2) attack: d = 100 errors mean 2.01, coordinatewise median 1.41, geometric median 1.14, filter 0.22 (oracle 0.21); d = 200: 2.85, 2.02, 1.61, 0.35; at ε = 0.2 (d = 100) filter 0.27, all planted points and 9% of the clean removed |
| 3 | List decoding | 90 inliers (30%) and three clusters of 70: the mean is 1.90 from (1, 1); the best of four candidates 0.23, as close as the inliers' own mean |
| 4 | Heavy tails | n = 600, d = 20, t₂.₅, 400 samples: mean error median 0.374, 99th percentile 0.640; geometric median of 30 block means 0.350, 0.496 |
| 5 | Covariate shift | 400 young-skewed samples of 600: unweighted 118.83 (sd 0.62), 0% coverage; classifier-weighted (age, age², sex, BMI; 2,000 unlabelled adults) 126.19 (sd 1.22), 95.5%; Kish n_eff ≈ 291 |
| 6 | Label shift | 300 repetitions, train 250 (37% malignant), hold out 150, target 100 at 70%: classify and count 0.647, BBSE 0.700 (sd 0.055), EM 0.691 (sd 0.038); interval coverage 85% vs 95%; a score of 0.40 becomes 0.73 |
| 7 | DRO | SBP on sex and BMI fit on ages 18–39: MSE (10 mm Hg)² 1.24, 4.55 (40–59), 9.19 (60–80); χ² worst case 2.16, 3.09, 4.17, 5.39 at ρ = 0.05, 0.2, 0.5, 1; KL 2.63, 4.90, 8.51, 13.69; KL certifies 40–59 at ρ ≈ 0.18 and 60–80 at ρ ≈ 0.56 |
| 8 | Invariance | ICP, three environments: p-values ∅ 5 × 10⁻¹⁷⁹, {X₁} 1.00, {X₂} 1.0 × 10⁻⁸, {X₁, X₂} 2.0 × 10⁻¹⁶, so Ŝ = {X₁}; anchor regression with test shift 3: test MSE 10.52 (γ = 0), 5.13 (OLS), 3.54, 2.54, 2.47 (γ = 10), 2.76 (γ = 50) |
| 9 | Transfer | p = 200, s = 10, n_S = 1,000: similar source (5 shifts of 0.15), n_T = 50: target-only 2.00, pooled 0.135, Trans-Lasso 0.136; dissimilar (shifts of 1), n_T = 400: pooled 2.06, target 0.325, Trans-Lasso 0.246 |
| 10 | Detecting shift | 300 vs 300 on age, BMI, sex: MMD² 0.100, p = 1/301; two population samples p = 0.87; classifier accuracy 0.65, p ≈ 1 × 10⁻⁷ |
| 11 | Open problems | — |
| 12 | Outro | — |

## Sources

- **The hook.** B. Recht, R. Roelofs, L. Schmidt & V. Shankar, ICML (2019).
- **Depth.** J. Tukey, *Proc. ICM* (1975); D. Donoho & M. Gasko, *Ann. Stat.* 20 (1992); M. Chen, C. Gao & Z. Ren,
  *Ann. Stat.* 46 (2018).
- **Efficient robustness.**
  - I. Diakonikolas, G. Kamath, D. Kane, J. Li, A. Moitra & A. Stewart, FOCS (2016);
  - K. Lai, A. Rao & S. Vempala, FOCS (2016);
  - I. Diakonikolas, D. Kane & A. Stewart, FOCS (2017);
  - I. Diakonikolas & D. Kane, *Algorithmic High-Dimensional Robust Statistics* (2023).
- **List decoding.** M. Charikar, J. Steinhardt & G. Valiant, STOC (2017).
- **Heavy tails.**
  - A. Nemirovski & D. Yudin (1983); N. Alon, Y. Matias & M. Szegedy, STOC (1996);
  - S. Minsker, *Bernoulli* 21 (2015);
  - L. Devroye, M. Lerasle, G. Lugosi & R. Oliveira, *Ann. Stat.* 44 (2016);
  - G. Lugosi & S. Mendelson, *Ann. Stat.* 47 (2019) and *Found. Comput. Math.* 19 (2019);
  - S. Hopkins, *Ann. Stat.* 48 (2020); O. Catoni, *Ann. IHP* 48 (2012).
- **Covariate shift.**
  - H. Shimodaira, *J. Stat. Plan. Inference* 90 (2000); L. Kish, *Survey Sampling* (1965);
  - J. Huang, A. Smola, A. Gretton, K. Borgwardt & B. Schölkopf, NeurIPS (2006);
  - M. Sugiyama et al., *Ann. Inst. Stat. Math.* 60 (2008).
- **Label shift.**
  - G. Forman, ECML (2005);
  - M. Saerens, P. Latinne & C. Decaestecker, *Neural Computation* 14 (2002);
  - Z. Lipton, Y.-X. Wang & A. Smola, ICML (2018);
  - B. Schölkopf et al., ICML (2012).
- **DRO.**
  - A. Ben-Tal, D. den Hertog, A. De Waegenaere, B. Melenberg & G. Rennen, *Management Science* 59 (2013);
  - J. Duchi & H. Namkoong, *JMLR* 20 (2019) and *Ann. Stat.* 49 (2021);
  - P. Mohajerin Esfahani & D. Kuhn, *Math. Programming* 171 (2018);
  - J. Blanchet & K. Murthy, *Math. Oper. Res.* 44 (2019); J. Blanchet, Y. Kang & K. Murthy, *J. Appl. Prob.* 56 (2019);
  - S. Sagawa, P. W. Koh, T. Hashimoto & P. Liang, ICLR (2020);
  - T. Hashimoto, M. Srivastava, H. Namkoong & P. Liang, ICML (2018);
  - W. Hu, G. Niu, I. Sato & M. Sugiyama, ICML (2018).
- **Invariance.**
  - J. Peters, P. Bühlmann & N. Meinshausen, *JRSS B* 78 (2016);
  - D. Rothenhäusler, N. Meinshausen, P. Bühlmann & J. Peters, *JRSS B* 83 (2021);
  - M. Arjovsky, L. Bottou, I. Gulrajani & D. Lopez-Paz, arXiv:1907.02893 (2019);
  - E. Rosenfeld, P. Ravikumar & A. Risteski, ICLR (2021);
  - I. Gulrajani & D. Lopez-Paz, ICLR (2021).
- **Transfer.**
  - S. Ben-David, J. Blitzer, K. Crammer, A. Kulesza, F. Pereira & J. Vaughan, *Machine Learning* 79 (2010);
  - S. Kpotufe & G. Martinet, *Ann. Stat.* 49 (2021); T. Cai & H. Wei, *Ann. Stat.* 49 (2021);
  - S. Li, T. Cai & H. Li, *JRSS B* 84 (2022);
  - Y. Ganin et al., *JMLR* 17 (2016); H. Zhao, R. Tachet des Combes, K. Zhang & G. Gordon, ICML (2019).
- **Detection.**
  - A. Gretton, K. Borgwardt, M. Rasch, B. Schölkopf & A. Smola, *JMLR* 13 (2012);
  - D. Lopez-Paz & M. Oquab, ICLR (2017);
  - S. Rabanser, S. Günnemann & Z. Lipton, NeurIPS (2019);
  - A. Podkopaev & A. Ramdas, ICLR (2022);
  - F. Liu et al., ICML (2020).
- **Open problems.** P. W. Koh et al. (WILDS), ICML (2021); J. Miller et al., ICML (2021).
- **Data.** A. Azzalini & A. Bowman, *Appl. Stat.* 39 (1990); NHANES (CDC); W. Wolberg, W. Street & O. Mangasarian
  (1995).

## Problems and solutions

1. **The contaminated median.** With mass ε at +∞, the median m solves (1 − ε)Φ(m) = ½, so m = Φ⁻¹(1/(2(1 − ε))).
   Expanding, 1/(2(1 − ε)) ≈ ½ + ε/2, and Φ⁻¹(½ + u) ≈ u/φ(0), so m ≈ ε/(2φ(0)) = ε√(π/2) ≈ 1.25ε. In d coordinates
   under the (c, …, c) attack, each coordinate moves by about this much, so the coordinatewise median's error is about
   1.25ε√d.
2. **Importance weighting.**
   - Since Q(dx, dy) = q(x)P(dy | x) dx and P(dx, dy) = p(x)P(dy | x) dx, we have E_P[w f] = ∫∫ (q/p) f p P(dy | x) dx
     = E_Q[f].
   - The Hájek estimator Σwᵢyᵢ/Σwᵢ with constant outcome variance σ² has variance about σ²Σwᵢ²/(Σwᵢ)². That is
     σ²/n_eff with n_eff = (Σw)²/Σw².
3. **Classify and count.**
   - E[q̂_CC] = P(ŷ = 1) = P(ŷ = 1 | y = 1)q + P(ŷ = 1 | y = 0)(1 − q) = q TPR + (1 − q) FPR. Solving gives
     q = (q̂_CC − FPR)/(TPR − FPR).
   - With two classes, BBSE's system C w = μ has C = [[(1 − FPR)(1 − p), (1 − TPR)p], [FPR(1 − p), TPR p]] and
     μ = (1 − q̂_CC, q̂_CC). Solving and forming q = w₁p gives the same expression.
4. **The χ² worst case.**
   - Maximize Σqᵢℓᵢ subject to Σqᵢ = 1 and (n/2)Σ(qᵢ − 1/n)² ≤ ρ.
   - With qᵢ = 1/n + vᵢ, Σvᵢ = 0, the objective is ℓ̄ + Σvᵢ(ℓᵢ − ℓ̄).
   - By Cauchy–Schwarz this is at most ℓ̄ + ‖v‖‖ℓ − ℓ̄‖ = ℓ̄ + √(2ρ/n)·√(n Var̂ ℓ) = ℓ̄ + √(2ρ Var̂ ℓ). The bound is
     attained at v ∝ ℓ − ℓ̄, which is feasible while every qᵢ ≥ 0.
5. **Anchor regression's limits.**
   - With W = I − (1 − √γ)P_A, the objective is ‖W(y − Xb)‖². At γ = 1, W = I, which is OLS.
   - As γ → ∞, the term γ‖P_A(y − Xb)‖² dominates, so the solution minimizes ‖P_A(y − Xb)‖², which is two-stage least
     squares. Under just identification it is the IV estimator (A′X)⁻¹A′y.
6. **The classifier's odds.** Pool n₀ source and n₁ target points. Bayes' rule gives c(x) = n₁q(x)/(n₀p(x) + n₁q(x)),
   so c/(1 − c) = n₁q(x)/(n₀p(x)) and (n₀/n₁)·c/(1 − c) = q(x)/p(x).

## Glossary

- **Robustness.**
  - Contamination: Huber's model; the strong model; breakdown point.
  - Depth: halfspace depth; the Tukey median.
  - Efficient estimators: geometric median; the spectral filter; sum-of-squares; SQ lower bound.
  - List decoding.
  - Heavy tails: median of means; tournaments; δ-dependence; Catoni's estimator.
- **Shift.**
  - Kinds of shift: covariate shift; label shift; posterior drift; concept shift.
  - Covariate shift: importance weight; density ratio; overlap; Kish's effective sample size.
  - Label shift: classify and count; adjusted count; BBSE; the EM correction.
- **Guarding.**
  - DRO: uncertainty set; φ-divergence ball; Wasserstein ball; group DRO; variance regularization.
  - Invariance: invariant causal prediction; anchor regression; IRM.
  - Transfer: transfer exponent; Trans-Lasso; negative transfer; domain adaptation.
- **Detection.** MMD; characteristic kernel; classifier two-sample test; harmful shift.

## Where it comes back

- **Part 61**: Wasserstein distances, studied in their own right.
- **Part 62**: transporting causal effects across populations.
- **Part 63**: robustness and differential privacy.
- **Part 64**: large models, out-of-distribution accuracy, and the accuracy line.
- **Part 65**: the dissertation's robustness checks.
