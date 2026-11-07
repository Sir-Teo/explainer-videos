# Statistics, Built — Part 50: Minimax Theory: the Limits of Estimation

Part 50 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eighth part of Stage IV, the PhD core.

It opens with Farrell (1972) and Stone (1980): with s derivatives in d dimensions, no method of any kind can estimate a
function faster than n^{−2s/(2s+d)}. The part asks how well anyone can estimate, with any method, and builds both halves
of the answer:
- the Gaussian sequence model, and why it stands for regression and density estimation (Brown & Low; Nussbaum);
- Pinsker's exact **linear** minimax risk over ellipsoids and asymptotic unrestricted constant, its linear rule and its least favourable Gaussian prior;
- lower bounds by Le Cam's two points, Fano's packings and Assouad's hypercubes, on a workbench of hypotheses;
- upper bounds that match: blockwise James–Stein, thresholding and oracle inequalities, Besov balls;
- adaptation by Lepski's method, and its price for pointwise loss;
- minimax testing: Ingster's separation rates, the sparse-mixture detection boundary, higher criticism;
- statistical–computational gaps: planted clique, sparse PCA, best subset, low-degree evidence;
- honest intervals, on the Board.

It keeps three promises:
- **Part 29** chose bandwidths and found the rate n^{−4/5}, but took on trust that no smoother could do better.
  Chapters 3–5 prove it with Le Cam's, Fano's and Assouad's methods.
- **Part 47**'s local minimax theorem lives at the root-n scale. Chapter 2 finds an exact minimax constant at a
  nonparametric rate (Pinsker).
- **Part 49**'s efficiency bound assumed root-n was achievable. Chapter 3 shows when it is (the modulus of continuity)
  and, when it is not, the rest of the part finds the rate itself.

**Built in this part:**
- **`statkit.gsm`** ([`explainer/stats/kit/gsm.py`](../../../explainer/stats/kit/gsm.py)), tested in
  `tests/test_stats_kit_gsm.py`:
  - the Gaussian sequence model on Sobolev ellipsoids; Pinsker's linear minimax rule and risk, its least favourable
    prior and Pinsker's constant; the hardest θ;
  - projection, Pinsker, blockwise James–Stein, soft and hard thresholding;
  - TV, Hellinger and KL for normals and Bernoullis;
  - Le Cam's two-point bound for a density at a point, Fano's bound, a Varshamov–Gilbert packing, the sparse-means rate,
    Assouad's bound for Hölder regression;
  - Lepski's bandwidth choice; the detection boundary, higher criticism and the sparse mixture; a planted-clique
    generator with degree tests.
- **The lower-bound workbench** (`LowerBoundPacking` in `explainer/stats/viz.py`), the part's instrument: hypotheses
  as points with their separation discs, confusion lines between pairs the data cannot tell apart, and Assouad's
  hypercube with its neighbour edges.

**Data.**
- From the Museum: the motorcycle crash (Schmidt, Mattern & Schüler 1981; Silverman 1985).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows. Empirical MCSE is measured across independent datasets:

| Method | Setting | Nominal / benchmark | Achieved ± MCSE | Verdict |
|---|---|---|---|---|
| pointwise CI, \ MSE-optimal bandwidth | a peak at $x_0$, \ $n = 2{,}000$ | 95% | 92.53% ± 0.68% | broken |
| pointwise CI, \ undersmoothed (bandwidth / 4) | a peak at $x_0$, \ $n = 2{,}000$ | 95% | 95.67% ± 0.53% | kept |
| pointwise CI, \ Lepski's bandwidth | a peak at $x_0$, \ $n = 2{,}000$ | 95% | 44.33% ± 1.28% | broken |
| pointwise CI, bias-aware fixed bandwidth | known Gaussian noise; derivative-bounded class | 95% | 96.47% ± 0.48% | conservative |
| higher criticism, \ leading null scale (not 5-percent calibrated) | null $N(0,1)$, \ $n = 2{,}000$ | 5% comparison benchmark | 35.60% ± 0.87% | broken |
| higher criticism, \ simulated critical value | null $N(0,1)$, \ $n = 2{,}000$ | 5% | 5.13% ± 0.40% | kept |

Interval rows use 1,500 independent datasets at one peak. Only the bias-aware row has a stated class-wide finite-Gaussian guarantee; near-95% coverage at one function does not prove honesty. The HC leading scale is not a level-5% critical value; the 5% column is a comparison benchmark. HC calibration and evaluation use separate 3,000-dataset samples. Calibration uncertainty is separate from the displayed evaluation MCSE.

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats50.compute   # once (about a minute)
python tools/build.py stats50 -q l                         # fast 480p preview
python tools/build.py stats50                              # 1080p30 -> renders/stats50.mp4
python tools/qa_scene.py stats50 Fano
python tools/lecture_length.py stats50 --floor 50
```

## Chapters

| # | Chapter | Numbers and scope |
|---|---|---|
| 0 | Farrell and Stone | Normal KDE pointwise risk is an illustration; the 1.06 bandwidth is a normal-reference integrated-risk rule, not a pointwise optimum |
| 1 | The Gaussian sequence model | Discrete orthonormality versus continuous quadrature; Brown–Low/Nussbaum model, positivity and loss conditions |
| 2 | Pinsker | Linear-risk / asymptotic-formula ratio 0.8861 → 0.9945; worst-case projection ratio 3^(2/3) = 2.0801, equivalent to 3× the data |
| 3 | Le Cam | Valid C2 norm-one density pair; at n=4,000 lower bound 0.0000034; uniform KDE upper bound 0.0005965 |
| 4 | Fano | Random 24-bit packing: 2,907 candidates retained; existence lower bound 8; s log(ep/s) is a rate scale, not an exact lower constant |
| 5 | Assouad | Derivative-normalized Lipschitz/C2 bumps; exact finite-design Gaussian KL; conservative squared-loss reduction constant; finite C2 slopes are not yet asymptotic |
| 6 | Upper bounds | Selected-truth risks at ε=.003, divided by linear minimax risk: projection 1.41, block energy shrinker 1.21; not other estimators' worst-case risks |
| 7 | Lepski | Largest admissible rule, κ=2.2; exact fixed-design oracle risk; observed rule/oracle ratios 1.96 and 2.41 |
| 8 | Testing | Truncated CDF HC supremum includes t=1/n; global detection differs from almost-full support recovery (r>β in the specified rare/weak model) |
| 9 | Computation | Edge-count exact powers at k=30/40: 0.458/0.869; observed 0.513/0.860; conjectured asymptotic computational scales are not finite-n hardness thresholds |
| 10 | Honest intervals | h_opt=0.02, h_under=0.005; bias-aware h=0.02, bias bound 0.0546, radius 0.2751; HC leading scale 2.014, independently calibrated cutoff 3.193 |
| 11 | Outro | Six solutions; assumptions and asymptotic versus finite-sample scope retained |

## QA checkpoint

All twelve scenes, six solutions, twelve computations, shared toolkit and tests were read. All twelve inputs were regenerated; seventeen focused checks pass. All 133 motorcycle time/acceleration pairs agree exactly with an independent MASS data distribution. See the [scientific source review](../../../docs/qa/evidence/stats50-polish-20261107/source-review.md), input hashes and logs. The recorded English sampled visual checkpoint is complete; Chinese narration/captions, continuous listening and final masters remain open.

## Sources

- **Rates.** R. Farrell, *Ann. Math. Stat.* 43 (1972); C. Stone, *Ann. Stat.* 8 (1980), 10 (1982).
- **The sequence model and Pinsker.**
  - M. Pinsker, *Probl. Inf. Transm.* 16 (1980); L. Brown & M. Low, *Ann. Stat.* 24 (1996); M. Nussbaum, *Ann. Stat.*
    24 (1996).
  - S. Efromovich & M. Pinsker, *Autom. Remote Control* 45 (1984); T. Cai, *Ann. Stat.* 27 (1999); L. Cavalier &
    A. Tsybakov, *Probab. Theory Relat. Fields* 123 (2002).
- **Lower bounds.**
  - L. Le Cam, *Ann. Stat.* 1 (1973); R. Fano, *Transmission of Information* (1961); P. Assouad, *C. R. Acad. Sci.*
    296 (1983); B. Yu, in *Festschrift for Lucien Le Cam* (1997).
  - Y. Yang & A. Barron, *Ann. Stat.* 27 (1999); D. Donoho & R. Liu, *Ann. Stat.* 19 (1991).
- **Upper bounds and adaptation.**
  - D. Donoho & I. Johnstone, *Biometrika* 81 (1994); *JASA* 90 (1995); *Ann. Stat.* 26 (1998).
  - O. Lepski, *Theory Probab. Appl.* 35 (1990); A. Goldenshluger & O. Lepski, *Ann. Stat.* 39 (2011).
  - M. Low, *Ann. Stat.* 25 (1997); T. Armstrong & M. Kolesár, *Econometrica* 86 (2018).
- **Testing.** Yu. Ingster, *Probl. Inf. Transm.* 18 (1982); *Math. Methods Stat.* 6 (1997); J. Jin, PhD thesis
  (2003); D. Donoho & J. Jin, *Ann. Stat.* 32 (2004).
- **Computation.**
  - M. Jerrum, *Random Struct. Alg.* 3 (1992); N. Alon, M. Krivelevich & B. Sudakov, *Random Struct. Alg.* 13 (1998).
  - Q. Berthet & P. Rigollet, *COLT* (2013); Y. Zhang, M. Wainwright & M. Jordan, *COLT* (2014); S. Hopkins, PhD thesis
    (2018); M. Brennan & G. Bresler, *COLT* (2020).
- **Books.** A. Tsybakov, *Introduction to Nonparametric Estimation* (2009); I. Johnstone, *Gaussian Estimation:
  Sequence and Wavelet Models* (2019); E. Giné & R. Nickl (2016); Y. Polyanskiy & Y. Wu, *Information Theory: From
  Coding to Learning* (2024).

## Problems and solutions

1. **The worst θ for a linear rule.**
   - The risk of θ̂_k = c_k y_k is Σ(1 − c_k)²θ_k² + ε²Σc_k². Write u_k = a_kθ_k, so the constraint is Σu_k² ≤ C².
   - The first sum is Σ((1 − c_k)²/a_k²) u_k², maximized by putting all of C² on the k with the largest
     (1 − c_k)²/a_k²: sup = C² max_k (1 − c_k)²/a_k² + ε²Σc_k².
   - Minimizing over c gives Pinsker's taper: many boundary allocations over active coordinates are worst cases once c is optimal; a spread allocation is not unique. The exact finite-noise result is linear minimax, with unrestricted minimax equivalence asymptotic.
2. **The Gaussian prior's Bayes rule.**
   - With θ_k ~ N(0, τ_k²) and y_k | θ_k ~ N(θ_k, ε²), the posterior mean is τ_k²y_k/(τ_k² + ε²).
   - Its Bayes risk is Σ τ_k²ε²/(τ_k² + ε²). This Gaussian law is not supported on the ellipsoid; a lower bound for that bounded parameter space needs prior-radius slack and controlled conditioning/truncation. With τ_k² = ε²(μ/a_k − 1)₊ the weights are (1 − a_k/μ)₊, Pinsker's.
3. **Le Cam's bound.**
   - For |θ₁−θ₀|=2δ, max_j E_j(θ̂ − θ_j)² ≥ ½(E₀ + E₁); define ψ = 1{|θ̂ − θ₁| < |θ̂ − θ₀|}. If ψ errs, |θ̂ − θ_j| ≥ δ.
   - So the average risk ≥ (δ²/2)(P₀(ψ = 1) + P₁(ψ = 0)) ≥ (δ²/2)(1 − TV(P₀, P₁)).
4. **TV between normals.**
   - The densities cross at d/2, so For d≥0, TV = P_d(X > d/2) − P₀(X > d/2) = 2Φ(d/2) − 1.
   - KL = d²/2, so √(KL/2) = d/2. With x = d/2, 2Φ(x) − 1 = 2∫₀ˣ φ ≤ 2xφ(0) = x√(2/π) ≤ x, which is Pinsker's
     inequality for this pair.
5. **Farrell's construction.**
   - |f₁(x₀) − f₀(x₀)| = h = c_{b,f₀,L}w^s after checking support, positivity and derivative norms; use a compensating disjoint bump so ∫f₁=1; χ²(f₁, f₀) ≍ h²w, so the n-sample TV stays below 1/2 when n h² w ≍ 1.
   - That is n w^{2s+1} ≍ 1, w ≍ n^{−1/(2s+1)}, and the risk ≳ h² = w^{2s} ≍ n^{−2s/(2s+1)}.
6. **The maximum's boundary.**
   - Under the null, max X_i ≈ √(2 log n). The n^{1−β} signals have maximum ≈ √(2r log n) + √(2(1 − β) log n).
   - This exceeds √(2 log n) iff √r + √(1 − β) > 1, i.e. r > (1 − √(1 − β))², the boundary's very sparse branch.

## Glossary

- **The setting.**
  - Minimax risk; least favourable prior; Bayes risk as a lower bound: the game.
  - Gaussian sequence model; white noise model; Le Cam equivalence; Sobolev ellipsoid; Besov ball: the model.
- **Lower bounds.**
  - Total variation; Hellinger distance; Kullback–Leibler divergence; Pinsker's inequality; χ² divergence: comparing
    laws.
  - Le Cam's two-point method; modulus of continuity; Fano's inequality; packing; Varshamov–Gilbert bound; Assouad's
    lemma; hypercube; Yang–Barron: the methods.
- **Upper bounds.**
  - Linear estimator; Pinsker's theorem; projection estimator; blockwise James–Stein; soft and hard thresholding;
    universal threshold; oracle inequality; SURE: matching methods.
  - Adaptation; Lepski's method; the price of adaptation; honest interval; bias-aware interval: not knowing the class.
- **Testing and computation.**
  - Separation rate; Ingster's χ² test; sparse mixture; detection boundary; higher criticism: minimax testing.
  - Planted clique; sparse PCA; reduction; low-degree polynomials; statistical–computational gap: rates under a
    budget.

## Where it comes back

- **Part 51**: concentration of measure and chaining in high dimensions.
- **Part 52**: the lasso attains Fano's s log(p/s); restricted eigenvalues.
- **Part 53**: posterior contraction rates match the minimax rates.
- **Part 54**: learning-theory lower bounds, with VC dimension and Fano.
- **Part 63**: the minimax price of differential privacy.
