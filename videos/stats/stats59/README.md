# Statistics, Built — Part 59: High-Dimensional Asymptotics

Part 59 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fourth part of Stage V, the research frontier.

It opens with Sur & Candès (2019). In a logistic regression with one variable for every five observations and signal
strength γ² = Var(x′β) = 5, the MLE overestimates every coefficient by a factor α⋆ = 1.499. Its spread is σ⋆ = 4.74
against the textbook's 3.88, and twice the log likelihood ratio for a null coefficient is 1.487 χ²₁, not χ²₁. The part
asks what happens to classical statistics when p and n grow together, and answers exactly:
- the proportional regime: the scaling, least squares' σ²κ/(1 − κ), the Marchenko–Pastur law, the Sur–Candès system
  solved by root finding and quadrature (checked against the paper), the MLE's existence boundary (Candès & Sur 2020),
  universality;
- random-matrix tools: Stieltjes transforms and inversion, the leave-one-column-out derivation, MP moments, free
  convolution (Voiculescu) by Pastur's equation, against a simulated Wigner-plus-diagonal matrix, subordination;
- exact ridge and ridgeless risk (Dobriban & Wager 2018; Hastie, Montanari, Rosset & Tibshirani 2022), the optimal
  penalty, double descent derived and simulated, why the peak, benign interpolation;
- M-estimation in high dimensions (El Karoui et al. 2013; Bean et al. 2013; Donoho & Montanari 2016): least absolute
  deviations beats least squares at small κ and loses at large κ, even for Laplace errors;
- approximate message passing (Donoho, Maleki & Montanari 2009) and state evolution (Bayati & Montanari 2011), shown
  in the state-evolution cobweb, the Donoho–Tanner curve from state evolution, Bolthausen's conditioning;
- Gordon's comparison (1985) and the CGMT (Thrampoulidis, Oymak & Hassibi 2015), least squares and ridge worked, the
  lasso's equations;
- the replica method: the scalar channel, Bayes-optimal AMP against the lasso, hard phases, the proofs (Barbier et al.
  2019);
- random features and kernels (Rahimi & Recht 2007; Mei & Montanari 2022): double descent in a two-layer network with a
  frozen first layer, Gaussian equivalence, the kernel staircase;
- corrected inference: the rescaled LRT, the debiased MLE and its intervals, estimating γ (ProbeFrontier, SLOE), and a
  semi-synthetic test on the Wisconsin biopsies' correlated design, measured on the held-out linear predictor;
- five open problems.

It keeps two promises:
- **Part 22** said the MLE is efficient and 2 log LR ⇒ χ², with p fixed. Chapters 1 and 9 give the proportional
  limits and the corrections.
- **Part 52** gave high-dimensional rates up to constants. Chapters 3–8 give exact errors, constants included.

**Built in this part:**
- **`statkit.amp`** ([`explainer/stats/kit/amp.py`](../../../explainer/stats/kit/amp.py)), tested in
  `tests/test_stats_kit_amp.py`:
  - the logistic proximal map, and the Sur–Candès system in (α, σ, λ) by root finding with 81 × 81 Gauss–Hermite
    quadrature (it reproduces the paper's κ = 0.1 and κ = 0.2 values to four digits), the global-null system, and the
    MLE's existence boundary;
  - the logistic MLE by damped Newton and the LRT for one coefficient;
  - the Marchenko–Pastur Stieltjes transform and density, exact ridge bias, variance and risk, the optimal penalty, the
    ridgeless risk, and a ridge/ridgeless simulator;
  - AMP for the lasso, its state evolution, the minimax-threshold Donoho–Tanner curve (identical to Part 32's), the
    lasso's best-threshold MSE;
  - the Bayes-optimal denoiser and MMSE for a three-point prior, and Bayes-optimal state evolution;
  - free convolution of a semicircle with a ±1 law by Pastur's equation;
  - least absolute deviations by linear programming, and random-features ridge regression.
- **The state-evolution cobweb** (`StateEvolution` in `explainer/stats/viz.py`), the part's instrument: the map
  τ²_t ↦ τ²_{t+1}, the diagonal, the staircase of iterates from τ²₀, the fixed point, and an algorithm's measured
  iterates on top, so AMP's trajectory can be checked against the theory step by step.

**Data.**
- From the Museum: the Wisconsin breast cancer design (30 standardized features), with simulated logistic outcomes.
- The rest is exact arithmetic (quadrature, root finding) or seeded simulation.

The Coverage Board gains two rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| LRT with the χ²₁ approximation | logistic, p/n = 0.2, γ² = 5 | 5% | 8.6% | broken |
| LRT rescaled by κσ⋆²/λ⋆ | logistic, p/n = 0.2, γ² = 5 | 5% | 3.8% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats59.compute   # once (about two minutes)
python tools/build.py stats59 -q l                         # fast 480p preview
python tools/build.py stats59                              # 1080p30 -> renders/stats59.mp4
python tools/qa_scene.py stats59 AMP
python tools/lecture_length.py stats59 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Sur and Candès | n = 2,000, p = 400, β ∈ {−10, 0, 10}: fitted slope 1.478 (α⋆ = 1.499); null spread 4.59 (σ⋆ = 4.74; textbook 3.88); 500 LRTs at n = 1,000: χ²₁ size 8.6% (2.6% at 1%), rescaled 3.8% (0.4%) |
| 1 | The proportional regime | OLS: σ²κ/(1 − κ); MP at κ = 0.5: eigenvalues 0.088–2.87 (edges 0.086, 2.91); γ² = 5: α⋆ 1.073, 1.168, 1.299, 1.499, 1.871 and factor 1.073, 1.166, 1.294, 1.487, 1.840 at κ = 0.05–0.25; no solution at 0.3; the MLE exists for κ < 0.501 (γ = 0), 0.326 (γ² = 5); global null κ = 0.2: factor 1.268, χ² size ≈ 8% |
| 2 | Random matrices | MP moments at κ = ½: mean 1, SD 0.71, mean inverse 2, top edge 2.91; Wigner (N = 1,500, s² = ¼) plus ±1 diagonal against the free convolution |
| 3 | Ridge | γ = ½, r²/σ² = 4: λ⋆ = 0.125, risk 0.702 (theory = simulation at n = 400); γ = 2: optimal risk 2.56; ridgeless: 1 (γ = ½), 9 (0.9), 3 (2), 3.33 (4); simulated 0.99, 9.99, 2.97, 3.33 |
| 4 | M-estimation | Laplace errors, n = 400: κ = 0.1 LAD 0.085 vs OLS 0.102; κ = 0.5 LAD 1.15 vs OLS 1.03 |
| 5 | AMP | n = 1,000, p = 2,000, ε = 0.1, σ² = 0.01, θ = 1.5: τ²₁ 0.129 (SE 0.131), τ²₃ 0.079 (0.079); MSE after 25 iterations 0.019 |
| 6 | Gordon | least squares from the auxiliary problem: a² = σ²κ/(1 − κ) |
| 7 | Replicas | ε = 0.1 three-point prior, σ² = 10⁻⁴: Bayes-AMP recovers from δ ≈ 0.30, the lasso from δ = 0.329; at δ = 0.2: MSE 0.075 vs 0.084; posterior means 0.05 (r = 0.5) and 0.29 (r = 1) at τ = ½ |
| 8 | Random features | n = 300, d = 30, ReLU: ridgeless peak 2,750 at N = n; error 0.23 at N = 2,500; λ = 10⁻³ removes the peak; ReLU Hermite coefficients 0.40, 0.5, μ⋆² ≈ 0.09 |
| 9 | Corrected inference | rescaled LRT; debiased interval example (3.8, 16.2) vs textbook (7.4, 22.6); breast cancer design, n = 150, γ² = 5: held-out predictor slope median 1.53, mean 1.64 (80% between 1.09 and 2.25) vs Gaussian theory 1.50 |
| 10 | Open problems | — |
| 11 | Outro | — |

## Sources

- **The hook.** P. Sur & E. Candès, *PNAS* 116 (2019); E. Candès & P. Sur, *Ann. Stat.* 48 (2020); P. Sur, Y. Chen &
  E. Candès, *PTRF* 175 (2019); T. Cover, *IEEE Trans. Electronic Computers* 14 (1965).
- **Random matrices.** V. Marchenko & L. Pastur, *Mat. Sbornik* (1967); L. Pastur, *Teoret. Mat. Fiz.* (1972);
  D. Voiculescu (1985–91); P. Biane (1998); Z. Bai & J. Silverstein, *Spectral Analysis of Large Dimensional Random
  Matrices* (2010); J. Mingo & R. Speicher, *Free Probability and Random Matrices* (2017).
- **Ridge.** E. Dobriban & S. Wager, *Ann. Stat.* 46 (2018); T. Hastie, A. Montanari, S. Rosset & R. Tibshirani,
  *Ann. Stat.* 50 (2022).
- **M-estimation.** N. El Karoui, D. Bean, P. Bickel, C. Lim & B. Yu, *PNAS* 110 (2013); D. Bean, P. Bickel,
  N. El Karoui & B. Yu, *PNAS* 110 (2013); D. Donoho & A. Montanari, *PTRF* 166 (2016).
- **AMP.** D. Donoho, A. Maleki & A. Montanari, *PNAS* 106 (2009); M. Bayati & A. Montanari, *IEEE Trans. Inf. Theory*
  57 (2011) and 58 (2012); E. Bolthausen, *Comm. Math. Phys.* 325 (2014); D. Thouless, P. Anderson & R. Palmer, *Phil.
  Mag.* 35 (1977).
- **Gordon.** Y. Gordon, *Israel J. Math.* 50 (1985); C. Thrampoulidis, S. Oymak & B. Hassibi, COLT (2015).
- **Replicas.** M. Mézard, G. Parisi & M. Virasoro, *Spin Glass Theory and Beyond* (1987); J. Barbier, F. Krzakala,
  N. Macris, L. Miolane & L. Zdeborová, *PNAS* 116 (2019); G. Reeves & H. Pfister, ISIT (2016); M. Mézard &
  A. Montanari, *Information, Physics, and Computation* (2009).
- **Random features.** A. Rahimi & B. Recht, NeurIPS (2007); S. Mei & A. Montanari, *CPAM* 75 (2022); N. El Karoui,
  *Ann. Stat.* 38 (2010).
- **Corrections.** S. Yadlowsky, T. Yun, C. McLean & A. D'Amour, NeurIPS (2021); P. Bellec & C.-H. Zhang, *Bernoulli*
  (2022); N. El Karoui & E. Purdom, *JMLR* 19 (2018).
- **Data.** W. Wolberg, W. Street & O. Mangasarian (1995).

## Problems and solutions

1. **Least squares.** Given X, Cov(β̂) = σ²(X′X)⁻¹, so E‖β̂ − β‖² = σ² E tr (X′X)⁻¹. For Gaussian rows, X′X is
   Wishart(n, I_p) and E (X′X)⁻¹ = I_p/(n − p − 1), so the trace is p/(n − p − 1) → κ/(1 − κ).
2. **Marchenko–Pastur.** Write S = Σ_i x_i x_i′/n. The identity tr (S − z)⁻¹ S − z tr (S − z)⁻¹ = p, the
   Sherman–Morrison formula for each x_i, and concentration of x_i′(S₋ᵢ − z)⁻¹x_i/n around (p/n) m give
   p = n(1 − 1/(1 + κm)) + zpm. Rearranged, κzm² − (1 − κ − z)m + 1 = 0.
3. **Optimal ridge.** Differentiating bias + variance in λ, and using the MP equation to eliminate m″, gives the
   stationarity condition r²λ = σ²γ, so λ⋆ = γσ²/r². This is also the Bayes posterior mean under a normal prior of total
   energy r², which minimizes the risk among all estimators for that prior.
4. **Ridgeless, γ > 1.** The minimum-norm solution is the projection of β onto the row space plus the noise fitted
   there. The row space has dimension n of p, so the unseen part contributes r²(1 − 1/γ). The noise contributes
   σ² tr (XX′)⁻¹, whose limit by the MP law with ratio 1/γ is σ²/(γ − 1).
5. **Gordon for least squares.** The auxiliary objective after optimizing directions is f(a) = √(a² + σ²)√n − a√p.
   Setting f′ = 0 gives a/√(a² + σ²) = √κ, so a² = σ²κ/(1 − κ).
6. **AMP's fixed points.** At a fixed point, x = η(x + A′z; θτ) and z = y − Ax + z⟨η′⟩/δ. So z(1 − ⟨η′⟩/δ) = y − Ax,
   and A′z lies in the subdifferential of θτ‖x‖₁ at x. Then A′(y − Ax) = (1 − ⟨η′⟩/δ) A′z ∈ λ ∂‖x‖₁ with
   λ = θτ(1 − ⟨η′⟩/δ), which is the lasso's optimality condition.

## Glossary

- **The regime.** Proportional asymptotics; κ = p/n; signal strength γ²; inflation α⋆; σ⋆; rescaled LRT; separability;
  universality.
- **Random matrices.** Marchenko–Pastur law; Stieltjes transform; resolvent; inversion formula; free probability; free
  convolution; R-transform; Pastur's equation; subordination.
- **Risk.** Ridge; ridgeless; minimum-norm interpolator; interpolation threshold; double descent; benign overfitting;
  GCV.
- **Algorithms and comparisons.** Approximate message passing; Onsager correction; state evolution; cobweb; fixed
  point; Donoho–Tanner curve; Gordon's inequality; CGMT; auxiliary problem.
- **Physics.** Free energy; replica trick; replica symmetry; scalar channel; MMSE; Bayes-optimal AMP; hard phase;
  statistical-computational gap; interpolation proof.
- **Networks.** Random features; Gaussian equivalence; Hermite coefficients; kernel limit; lazy regime; feature
  learning.

## Where it comes back

- **Part 60**: robust estimation in high dimensions, and distribution shift.
- **Part 61**: the sample complexity of optimal transport.
- **Part 62**: high-dimensional causal adjustment.
- **Part 64**: the theory of large models, beyond the lazy regime.
- **Part 65**: the dissertation's simulation study.
