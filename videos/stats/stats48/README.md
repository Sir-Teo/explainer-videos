# Statistics, Built — Part 48: Empirical Processes

Part 48 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the sixth part of Stage IV, the PhD core.

It opens with Doob's heuristic of 1949: √n(F_n − F) looks like a Brownian bridge, so Kolmogorov's 1933 law of
√n sup|F_n − F| should be the law of sup|B|. Donsker proved it in 1952, and making the proof airtight produced the theory
of empirical processes. The part asks for which classes of functions the law of large numbers and the central limit
theorem hold *uniformly*, and at what rate. It builds the answer in four steps:
- symmetrization and Rademacher averages (Glivenko–Cantelli classes);
- counting patterns (VC dimension, Sauer–Shelah);
- measuring size by covering and bracketing numbers (entropy);
- Dudley's chaining, which turns entropy into a uniform CLT (Donsker classes).

It then uses the theory on:
- concentration of the supremum (Talagrand, Bousquet, DKW);
- the functional delta method (the quantile and Kaplan–Meier processes);
- Z-estimators with nuisance parameters (the "footprint");
- rates of convergence and cube-root asymptotics (Grenander, Chernoff's distribution);
- empirical risk minimization;
- the bootstrap and multiplier empirical processes;
- the Kolmogorov–Smirnov test with estimated parameters (Durbin's process, the parametric bootstrap).

It keeps three promises:
- **Part 8** used the plug-in principle, F_n → F uniformly, on trust. Chapters 1–3 prove the Glivenko–Cantelli theorem
  three ways: symmetrization, VC counting, brackets.
- **Part 44** stated Donsker's invariance principle for random walks. Chapters 4–5 explain the empirical-process proof strategy
  and state the entropy theorems with their envelope and measurability conditions.
- **Part 47** took a uniform law of large numbers and the bootstrap empirical process on trust. Chapters 7, 11 and 12
  supply them.

**Built in this part:**
- **`statkit.empirical`** ([`explainer/stats/kit/empirical.py`](../../../explainer/stats/kit/empirical.py)), tested in
  `tests/test_stats_kit_empirical.py`; local repairs in `compute.py` are tested in `tests/test_stats48_polish.py`:
  - the Kolmogorov distribution (cdf, density, quantile) and KS statistics; Brownian bridges; empirical processes;
  - the exact Rademacher average of half-lines (the expected maximum of a simple random walk, by a local killed-walk spectral sum);
    Massart's finite-class lemma;
  - brute-force growth functions for half-lines, intervals, half-planes and rectangles; Sauer–Shelah;
  - greedy covering numbers; half-line brackets; random Lipschitz classes;
  - the dyadic chaining bound for Brownian motion; Dudley's integral; the sup over a dyadic net;
  - Bousquet's form of Talagrand's inequality; DKW with Massart's constant;
  - Durbin's variance for the estimated-parameter process (normal location–scale, exponential scale);
  - the mean absolute deviation's nuisance footprint;
  - Chernoff's distribution by simulation; the Grenander constant;
  - KS bands: Kolmogorov, exact, DKW, bootstrap, multiplier; the parametric-bootstrap KS test.
- **The chaining net** (`ChainingNet` in `explainer/stats/viz.py`), the part's instrument: Dudley's refining dyadic nets
  drawn as a tree of points tied to their parents, and, on a Brownian path, the level-k approximations with the links
  each level adds.

**Data.**
- From the Museum: Old Faithful's 272 waiting times; Newcomb's 66 passage times of light.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains seven rows:

| Method | Setting | Nominal | Achieved ± MCSE | Verdict |
|---|---|---|---|---|
| KS band from Kolmogorov's limit | N(0, 1) data, n = 20 | 95% | 96.35% ± 0.42% | conservative |
| KS band, exact finite-n quantile | N(0, 1) data, n = 20 | 95% | 95.45% ± 0.47% | kept |
| DKW band (Massart's constant) | N(0, 1) data, n = 20 | 95% | 96.35% ± 0.42% | conservative |
| KS band by the bootstrap | N(0, 1) data, n = 20 | 95% | 88.65% ± 0.71% | broken |
| KS band by the multiplier bootstrap | N(0, 1) data, n = 20 | 95% | 92.35% ± 0.59% | broken |
| KS test, estimated rate, Kolmogorov's table | exponential data, n = 30 | 5% | 0.60% ± 0.17% | conservative |
| KS test, estimated rate, parametric bootstrap | exponential data, n = 30 | 5% | 5.45% ± 0.51% | kept |

Each row uses 2,000 independent datasets. Band bootstraps use 499 resamples per dataset; the exponential test uses 199 and the finite-Monte-Carlo rank p-value. MCSE describes simulation uncertainty, separately from coverage or test calibration.

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats48.compute   # once (about a minute)
python tools/build.py stats48 -q l                         # fast 480p preview
python tools/build.py stats48                              # 1080p30 -> renders/stats48.mp4
python tools/qa_scene.py stats48 Chaining
python tools/lecture_length.py stats48 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Doob's heuristic | 95th percentile of √n D_n: 1.25 (n = 5), 1.34 (n = 100); Kolmogorov 1.358 |
| 1 | Glivenko–Cantelli classes | E D_n = 0.0272 vs 2R_n = 0.0783 at n = 1,000; √n E D_n → √(π/2) log 2 = 0.869 |
| 2 | VC classes | half-planes: n(n − 1) + 2 (92 at n = 10); 3 points shattered (8), a square not (14 of 16) |
| 3 | Entropy and bracketing | half-lines: 267 balls at ε = 0.05 (brackets 400); Lipschitz: 320 balls at ε = 0.08 |
| 4 | Chaining | E max over 2^K + 1 points → 0.788 (K = 10) vs √(2/π) = 0.798; union bound 3.72; chaining sum 3.85 |
| 5 | Donsker classes | exact 95% point √n D_n: 1.260, 1.315, 1.340 (n = 5, 20, 100); Old Faithful band ±0.082, D(normal) = 0.155 |
| 6 | Maximal inequalities | n = 100: 95% point of nD_n − E: 4.89 (McDiarmid 12.2, Bousquet 16.9); t ≤ 0.02 class: 1.48 (12.2, 6.5) |
| 7 | The functional delta method | quantile SDs 0.334 / 0.992 / 2.996 vs 1/3, 1, 3; KM SD at t = 1: 0.558 vs 0.560 |
| 8 | Nuisance parameters | MAD about the mean (Exp): n·Var 0.459 known, 0.778 estimated (simulated 0.466, 0.787); Newcomb SE 1.13 → 1.29 |
| 9 | Rates | Chernoff finite-grid SD 0.524 (reference 0.513); Grenander n^{1/3} SD 0.39–0.41 vs 0.418 |
| 10 | Learning | thresholds: 2E sup 0.057, excess risk 0.0014 at n = 1,000 (slope −1) |
| 11 | The bootstrap empirical process | 95% band coverage at n = 20: bootstrap 88%, multiplier 91%; at n = 100: 94% |
| 12 | KS with estimated parameters | normal n = 20: 0.192 vs Kolmogorov's 0.294, observed naive size 0.005% (2 / 40,000); Newcomb post hoc deletion: reference p = 0.21 (naive 0.64), not a calibrated selected-data test |
| 13 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Hook.**
  - √n D_n, 20,000 samples each: 95th percentiles 1.25 (n = 5), 1.32 (n = 20), 1.34 (n = 100), matching the exact
    finite-n law (1.260, 1.315, 1.340); Kolmogorov's limit 1.358.
  - Empirical-process paths at n = 20, 200, 5,000 beside a Brownian bridge.
- **Chapter 1.**
  - Glivenko–Cantelli defined; the class of finite sets fails (sup = 1 always).
  - Three sequences of D_n for n up to 5,000, inside a √(log log n / n) envelope (Chung 1949).
  - Symmetrization: E‖P_n − P‖ ≤ 2R_n. For half-lines R_n = E max_k |S_k| / n exactly:

    | n | 10 | 100 | 1,000 | 2,000 |
    |---|---|---|---|---|
    | E D_n (simulated) | 0.259 | 0.0855 | 0.0272 | 0.0194 |
    | 2R_n (exact) | 0.705 | 0.241 | 0.0783 | 0.0556 |

  - √n R_n → E sup|W| = √(π/2) = 1.253 (1.229 at n = 400). Massart's lemma √(2 log 2k / n).
- **Chapter 2.**
  - Growth functions by brute force (n = 10): half-lines 11, intervals 56, half-planes 92, rectangles ≥ 224 on random
    points, Sauer–Shelah with V = 4: 386, all subsets 1,024.
  - Haussler's covering bound; VC-subgraph classes; sin(ωx) has infinite VC dimension.
- **Chapter 3.**
  - Half-lines in L₂(uniform): greedy nets 7, 11, 25, 43, 89, 201, 267 at ε = 0.4 … 0.05; brackets ⌈1/ε²⌉ = 7 … 400.
  - 20,000 random 1-Lipschitz functions, sup norm: 5, 8, 14, 30, 64, 132, 320 balls at ε = 0.3 … 0.08 (log N ∝ 1/ε).
  - Entropy catalogue: indicator VC **uniform covering** entropy ≲ V log(1/ε), distinguished from bracketing entropy. Bounded monotone/Lipschitz and smoothness classes require their specified norms, domains and envelopes. For bounded Hölder balls on compact domains α > d/2 suffices; convex-set dimension claims assume a bounded regular region and regular sampling density. The actual square-root entropy integral must converge; little-o of ε⁻² is insufficient.
- **Chapter 4.**
  - Union bound over 2^K + 1 grid points: 1.18 (K = 0) … 3.72 (K = 10).
  - Simulated E max over the net: 0.405, 0.488, 0.564, … 0.788 (K = 0 … 10), toward √(2/π) = 0.798.
  - Chaining midpoint-correction bound: 1/√(2π) + Σ(k≥1) 2^{−(k+1)/2} √(2k log 2), about 3.85. Each maximum includes zero. Forty levels leave a rigorously bounded tail below 0.00001264. Dudley's integral for BM: √(π/2).
- **Chapter 5.**
  - Exact 95% points of √n D_n (Marsaglia, Tsang & Wang 2003): 1.260, 1.294, 1.315, 1.332, 1.340, 1.353 at
    n = 5, 10, 20, 50, 100, 1,000. The limit's test has size 2.7%, 3.4%, 3.9%, 4.3%, 4.5%, 4.9%.
  - Old Faithful (n = 272): band ±1.358/√272 = ±0.082; the fitted normal N(70.9, 13.6²) is 0.155 away.
- **Chapter 6.**
  - n = 100, 40,000 samples, E nD_n = 8.52. The centre E[nD_n] is estimated from these same draws (MCSE is recorded in the input). The plotted theoretical curves evaluated at that estimated centre are plug-in illustrations. 95% points of the fluctuation: simulated 4.89, McDiarmid 12.24,
    Bousquet 16.87 (σ² = 1/4: nothing to exploit).
  - Half-lines with t ≤ 0.02 (σ² = 0.0196): simulated 1.48, McDiarmid 12.24, Bousquet 6.54.
- **Chapter 7.**
  - Quantile process, Exp(1), n = 200: SDs 0.334, 0.579, 0.992, 1.724, 2.996 at p = 0.1 … 0.9 vs √(p/(1 − p)) = 0.333,
    0.577, 1, 1.732, 3.
  - Kaplan–Meier, Exp(1) times, Exp(½) censoring, n = 200, 3,000 samples: SDs 0.433, 0.520, 0.558, 0.536, 0.497 at
    t = 0.25 … 2 vs the limit 0.429, 0.523, 0.560, 0.531, 0.483.
- **Chapter 8.**
  - θ(c) = E|X − c|, slope 2F(c) − 1: zero at the median, 1 − 2/e = 0.264 at the mean of Exp(1).
  - n·Var (n = 200, 20,000 samples): about the median 0.614 known and estimated (simulated 0.623, 0.620); about the mean
    0.459 known, 0.778 estimated (simulated 0.466, 0.787), a factor 1.70.
  - Newcomb: MAD about the mean 5.42; SE 1.13 ignoring the footprint, 1.29 with it (slope −0.15), bootstrap 1.36. About
    the median 5.30 ± 1.14.
- **Chapter 9.**
  - The rate theorem; Kim & Pollard's cube-root limit.
  - Chernoff's distribution, 6,000 finite-window grid paths on [−2.5, 2.5] with 3,000 steps per side: SD 0.524 (Groeneboom & Wellner reference: 0.5133).
  - Grenander at x₀ = 1, Exp(1): constant 2|ff′/2|^{1/3} = 0.815; predicted SD 0.418; simulated 0.391, 0.406, 0.395 at
    n = 100, 1,000, 10,000.
- **Chapter 10.**
  - Thresholds, t₀ = 0.3, 20% label noise: 2E sup|R_n − R| = 0.398, 0.057, 0.042 at n = 20, 1,000, 2,000; ERM excess
    risk 0.059, 0.0014, 0.0007 (slope −1); VC bound 2.45, 0.49, 0.36.
- **Chapter 11.**
  - Giné–Zinn: bootstrap consistency ⇔ Donsker under envelope-integrability and measurability conditions. Gaussian multiplier CLT. Non-Hadamard differentiability alone does not prove bootstrap failure.
  - 95% band coverage (n = 20 / 100): Kolmogorov 95.2 / 95.9, exact 94.2 / 95.3, DKW 95.2 / 95.9, bootstrap 88.0 / 94.3,
    multiplier 91.0 / 94.2.
  - Old Faithful half-widths: 0.0823 (limit), 0.0817 (continuous-iid exact reference), 0.0823 (DKW), 0.0772 (tie-aware bootstrap), 0.0772 (tie-aware multiplier). These are iid references, not verified coverage for possibly dependent geyser waits.
- **Chapter 12.**
  - Durbin's variance Φ(1 − Φ) − φ² − (zφ)²/2: 0.0908 at z = 0 against 0.25 known (simulated 0.0909).
  - 95% points: normal, n = 20: 0.192 (Kolmogorov 0.294, observed naive size 0.005% (2 / 40,000)); exponential, n = 50: 0.151 (0.188, naive
    size 0.56%).
  - Newcomb normality: all 66, D = 0.231, p = 0.0014 naive, 0.0001 bootstrap (zero exceedances in 9,999 resamples); without the two outliers (64), D = 0.090,
    p = 0.64 naive, 0.21 fitted-normal reference; deletion is post hoc, so this is an influence comparison, not a calibrated test. The continuous-normal references ignore measurement rounding.

## QA checkpoint

All fourteen scenes and six solutions were read. Fourteen numerical inputs were regenerated; eighteen focused checks pass. The [source review](../../../docs/qa/evidence/stats48-polish-20261107/source-review.md) records numerical fixes, assumptions and independent data comparisons. The recorded English sampled visual checkpoint is complete; Chinese narration/captions, continuous listening and final masters remain open.

## Sources

- **Origins.**
  - A. Kolmogorov, *G. Ist. Ital. Attuari* 4 (1933); V. Glivenko, *G. Ist. Ital. Attuari* 4 (1933); F. Cantelli, same
    volume.
  - J. Doob, *Ann. Math. Stat.* 20 (1949); M. Donsker, *Ann. Math. Stat.* 23 (1952); K. L. Chung, *Trans. AMS* 67 (1949).
- **Combinatorics and entropy.**
  - V. Vapnik & A. Chervonenkis, *Theory Probab. Appl.* 16 (1971); N. Sauer, *J. Comb. Theory A* 13 (1972); S. Shelah,
    *Pacific J. Math.* 41 (1972); T. Cover, *IEEE Trans. Electron. Comput.* 14 (1965).
  - D. Haussler, *J. Comb. Theory A* 69 (1995); A. Kolmogorov & V. Tikhomirov, *Uspekhi* 14 (1959).
  - R. Dudley, *J. Funct. Anal.* 1 (1967); *Ann. Probab.* 6 (1978); M. Ossiander, *Ann. Probab.* 15 (1987); D. Pollard,
    *J. Austral. Math. Soc. A* 33 (1982).
- **Concentration.**
  - A. Dvoretzky, J. Kiefer & J. Wolfowitz, *Ann. Math. Stat.* 27 (1956); P. Massart, *Ann. Probab.* 18 (1990).
  - M. Talagrand, *Invent. Math.* 126 (1996); O. Bousquet, *C. R. Acad. Sci. Paris* 334 (2002).
- **Applications.**
  - R. Gill & S. Johansen, *Ann. Stat.* 18 (1990); J. Durbin, *Ann. Stat.* 1 (1973); H. Lilliefors, *JASA* 62 (1967).
  - U. Grenander, *Skand. Aktuarietidskr.* 39 (1956); B. Prakasa Rao, *Sankhyā A* 31 (1969); H. Chernoff, *Ann. Inst.
    Stat. Math.* 16 (1964); J. Kim & D. Pollard, *Ann. Stat.* 18 (1990); P. Groeneboom & J. Wellner, *J. Comput. Graph.
    Stat.* 10 (2001).
  - M. Banerjee & J. Wellner, *Ann. Stat.* 29 (2001); B. Sen, M. Banerjee & M. Woodroofe, *Ann. Stat.* 38 (2010).
  - E. Giné & J. Zinn, *Ann. Probab.* 18 (1990); V. Chernozhukov, D. Chetverikov & K. Kato, *Ann. Stat.* 41 (2013).
  - P. Bartlett, O. Bousquet & S. Mendelson, *Ann. Stat.* 33 (2005); G. Marsaglia, W. Tsang & J. Wang, *J. Stat. Softw.*
    8 (2003).
- **Books.**
  - A. van der Vaart & J. Wellner, *Weak Convergence and Empirical Processes* (1996; 2nd ed. 2023); M. Kosorok,
    *Introduction to Empirical Processes and Semiparametric Inference* (2008).
  - D. Pollard, *Convergence of Stochastic Processes* (1984); E. Giné & R. Nickl, *Mathematical Foundations of
    Infinite-Dimensional Statistical Models* (2016); R. Dudley, *Uniform Central Limit Theorems* (1999).

## Problems and solutions

1. **Symmetrization.**
   - Let X′ be an independent copy of the sample. Since P f = E′ P′_n f, Jensen gives
     E sup|P_n f − P f| ≤ E sup|P_n f − P′_n f|.
   - Each f(X_i) − f(X′_i) is symmetric and the pairs are independent, so multiplying by independent signs ε_i leaves
     the joint law unchanged.
   - Then sup|Σ ε_i (f(X_i) − f(X′_i))| ≤ sup|Σ ε_i f(X_i)| + sup|Σ ε_i f(X′_i)|, and the two terms have the same mean:
     E‖P_n − P‖ ≤ 2R_n.
2. **Intervals.**
   - Sort the points. An interval picks out a contiguous run x_(i), …, x_(j), and every run is achievable. There are
     n(n + 1)/2 runs plus the empty set.
   - At n = 2 that is 4 = 2²: two points are shattered. At n = 3 it is 7 < 8: the outer two points without the middle
     one cannot be picked out. So the VC dimension is 2.
3. **Brackets for half-lines.**
   - Choose −∞ = t₀ < t₁ < … < t_k = ∞ with F(t_j) − F(t_{j−1}) ≤ ε², which needs k = ⌈1/ε²⌉ (for continuous F).
   - The brackets [1{x ≤ t_{j−1}}, 1{x ≤ t_j}] have L₂(P) size at most ε and cover every 1{x ≤ t} for t in the corresponding closed interval, using endpoint conventions at ±∞. The continuous-F construction is sufficient here; for a general distribution use brackets allowing its atoms.
   - So sup_t (F_n(t) − F(t)) ≤ max_j (F_n(t_j−) − F(t_j−)) + ε², and similarly below. The maximum of finitely many
     terms goes to 0 a.s. by the strong law; since ε is arbitrary, sup|F_n − F| → 0 a.s.
4. **Dudley's integral for Brownian motion.**
   - In d(s, t) = √|s − t| a ball of radius ε contains an interval of length 2ε², so ⌈1/(2ε²)⌉ ≤ 1/ε² + 1 balls cover
     [0, 1].
   - ∫₀¹ √(log(1/ε²)) dε = √2 ∫₀¹ √(log(1/ε)) dε = √2 Γ(3/2) = √(π/2), which is finite: sample paths are continuous
     and E sup B is finite (in fact √(2/π)).
5. **The mean absolute deviation's footprint.**
   - For finite E|X| and no atom at c, θ(c) = E|X − c| has θ′(c) = 2F(c) − 1. This is mean absolute deviation, not the robust median absolute deviation. With ĉ = x̄, θ̂ − θ ≈ (P_n − P)|X − μ| + θ′(μ)(x̄ − μ), so
     IF(x) = |x − μ| − θ + (2F(μ) − 1)(x − μ).
   - For Exp(1), μ = 1, θ = 2/e, 2F(1) − 1 = 1 − 2/e. Var|X − 1| = E(X − 1)² − θ² = 1 − 4/e² = 0.459;
     Cov(|X − 1|, X − 1) = 0.472 (by quadrature). So n·Var = 0.459 + 2(0.264)(0.472) + 0.264² = 0.778.
6. **The estimated-parameter KS law is parameter-free.**
   - Write X_i = μ + σZ_i. Then x̄ = μ + σz̄ and s = σ s_z, so (X_i − x̄)/s = (Z_i − z̄)/s_z.
   - D = sup_x |F_n(x) − Φ((x − x̄)/s)| depends only on these standardized values (substitute x = μ + σu), hence only on
     Z: its law is the same for every (μ, σ).

## Glossary

- **The objects.**
  - Empirical measure P_n; empirical process 𝔾_n; function class; envelope; ℓ^∞(ℱ): random functions on a class.
  - Brownian bridge; P-Brownian bridge; Kolmogorov distribution; Doob's heuristic: the limits.
- **Uniform laws.**
  - Glivenko–Cantelli class; ghost sample; symmetrization; Rademacher average; Massart's lemma: the LLN, uniformly.
  - Shattering; growth function; VC dimension; Sauer–Shelah lemma; VC-subgraph class: counting patterns.
  - Covering number; metric entropy; bracket; bracketing number; uniform entropy: measuring size.
- **Uniform CLTs.**
  - Chaining; dyadic net; link; Dudley's entropy integral; sub-Gaussian process: suprema.
  - Donsker class; tightness; asymptotic equicontinuity; bracketing CLT; uniform-entropy CLT: the CLT, uniformly.
  - Bernstein's inequality; McDiarmid; Talagrand's inequality; Bousquet's constants; DKW; Massart's constant:
    concentration.
- **Uses.**
  - Functional delta method; quantile process; product integral; Kaplan–Meier process: smooth maps.
  - Nuisance parameter; footprint; Neyman orthogonality: plug-ins.
  - Rate theorem; modulus of continuity; cube-root asymptotics; Grenander estimator; Chernoff's distribution: slower
    rates.
  - Empirical risk minimization; excess risk; VC bound; localization: learning.
  - Bootstrap empirical process; Giné–Zinn theorem; multiplier bootstrap: resampling a process.
  - Estimated-parameter empirical process; Durbin's covariance; Lilliefors's test; parametric bootstrap: testing a
    family.

## Where it comes back

- **Part 49**: Donsker conditions for one-step estimators and TMLE; the footprint becomes Neyman orthogonality.
- **Part 50**: entropy turned into minimax rates, with Fano's and Le Cam's lower bounds.
- **Part 51**: concentration, chaining (Sudakov, generic chaining) and suprema in high dimensions.
- **Part 54**: statistical learning theory: VC, Rademacher and margin bounds.
- **Part 56**: multiplier bootstraps for simultaneous inference after selection.
