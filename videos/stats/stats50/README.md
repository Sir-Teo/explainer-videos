# Statistics, Built — Part 50: Minimax Theory: the Limits of Estimation

Part 50 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eighth part of Stage IV, the PhD core.

It opens with Farrell (1972) and Stone (1980): with s derivatives in d dimensions, no method of any kind can estimate a
function faster than n^{−2s/(2s+d)}. The part asks how well anyone can estimate, with any method, and builds both halves
of the answer:
- the Gaussian sequence model, and why it stands for regression and density estimation (Brown & Low; Nussbaum);
- Pinsker's exact minimax risk over ellipsoids, its linear rule and its least favourable Gaussian prior;
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

The Coverage Board gains five rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| pointwise CI, MSE-optimal bandwidth | a peak at x₀, n = 2,000 | 95% | 92.5% | broken |
| pointwise CI, undersmoothed (bandwidth / 4) | a peak at x₀, n = 2,000 | 95% | 95.7% | kept |
| pointwise CI, Lepski's bandwidth | a peak at x₀, n = 2,000 | 95% | 44.7% | broken |
| higher criticism, asymptotic critical value | null N(0, 1), n = 2,000 | size 5% | 35.2% | broken |
| higher criticism, simulated critical value | null N(0, 1), n = 2,000 | size 5% | 5.2% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats50.compute   # once (about a minute)
python tools/build.py stats50 -q l                         # fast 480p preview
python tools/build.py stats50                              # 1080p30 -> renders/stats50.mp4
python tools/qa_scene.py stats50 Fano
python tools/lecture_length.py stats50 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Farrell and Stone | KDE MSE at a point, n = 100 → 6,400: slope -0.70 (→ −4/5); d = 8: n^(−1/3) |
| 1 | The Gaussian sequence model | ε = 1/√n; Brown–Low and Nussbaum equivalence |
| 2 | Pinsker's theorem | ratio to P(α)C^{2/(2α+1)}ε^{4α/(2α+1)}: 0.886 (ε = 0.1) → 0.9945 (ε = 0.001); P(1) = 0.9086 |
| 3 | Le Cam | two-point bound slope −0.80 against the KDE's −0.76; gap ≈ 10^{0.95} |
| 4 | Fano | Varshamov–Gilbert, d = 24: 2,907 points (guarantee 8); soft thresholding ≈ 1.8 × s log(ep/s) |
| 5 | Assouad | Hölder regression bound slopes -0.67 (s = 1) and -0.73 (s = 2) |
| 6 | Upper bounds | risk / R* at ε = 0.003: Pinsker 1.01, best truncation 1.41, block JS 1.21, soft 5.17 |
| 7 | Lepski | Lepski / oracle MSE: 2.3 (smooth), 2.6 (cusp); motorcycle windows 2, 2, 12 ms |
| 8 | Minimax testing | HC power at β = 0.6, r = 0.3: 0.83 (max test 0.42); β = 0.9, r = 0.8: 0.27 (0.54) |
| 9 | Gaps | planted clique, n = 400: edge-count power 0.46 at k = 30, 0.85 at k = 40; 2 log₂ n ≈ 17, √n = 20 |
| 10 | The Board | coverage: MSE-optimal 92.5%, undersmoothed 95.7%, Lepski 44.7%; HC size 35.2% vs 5.2% |
| 11 | Outro | — |

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
   - Minimizing over c gives Pinsker's taper: the worst case is spread, not concentrated, once c is optimal.
2. **The Gaussian prior's Bayes rule.**
   - With θ_k ~ N(0, τ_k²) and y_k | θ_k ~ N(θ_k, ε²), the posterior mean is τ_k²y_k/(τ_k² + ε²).
   - Its Bayes risk is Σ τ_k²ε²/(τ_k² + ε²). With τ_k² = ε²(μ/a_k − 1)₊ the weights are (1 − a_k/μ)₊, Pinsker's.
3. **Le Cam's bound.**
   - max_j E_j(θ̂ − θ_j)² ≥ ½(E₀ + E₁); define ψ = 1{|θ̂ − θ₁| < |θ̂ − θ₀|}. If ψ errs, |θ̂ − θ_j| ≥ δ.
   - So the average risk ≥ (δ²/2)(P₀(ψ = 1) + P₁(ψ = 0)) ≥ (δ²/2)(1 − TV(P₀, P₁)).
4. **TV between normals.**
   - The densities cross at d/2, so TV = P₀(X > d/2) − P_d(X > d/2) = 2Φ(d/2) − 1.
   - KL = d²/2, so √(KL/2) = d/2. With x = d/2, 2Φ(x) − 1 = 2∫₀ˣ φ ≤ 2xφ(0) = x√(2/π) ≤ x, which is Pinsker's
     inequality for this pair.
5. **Farrell's construction.**
   - |f₁(x₀) − f₀(x₀)| = h = Lw^s; χ²(f₁, f₀) ≍ h²w, so the n-sample TV stays below 1/2 when n h² w ≍ 1.
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
