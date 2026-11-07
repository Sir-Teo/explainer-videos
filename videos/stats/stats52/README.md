# Statistics, Built — Part 52: High-Dimensional Statistics

Part 52 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the tenth part of Stage IV, the PhD core.

It opens with principal components on pure noise. A thousand observations of five hundred independent variables have
a top sample eigenvalue of 2.92 and a bottom one of 0.085, where every true eigenvalue is 1. The first component
"explains" 2.9 times its true share, and its loadings point in a uniformly random direction. The part asks what can be
estimated, and how fast, when parameters outnumber observations:
- the lasso's oracle inequality under restricted eigenvalues (Bickel, Ritov & Tsybakov 2009), proved;
- support recovery: irrepresentability, the primal–dual witness and Wainwright's 2s log(p − s) threshold;
- decomposable regularizers (Negahban et al. 2012): one theorem for sparse, group, low-rank and GLM problems;
- low-rank recovery and matrix completion (Candès & Recht 2009; Koltchinskii, Lounici & Tsybakov 2011);
- covariance estimation by banding, thresholding and Ledoit–Wolf shrinkage;
- perturbation theory: Weyl, Davis–Kahan, Wedin;
- random-matrix laws from the Stieltjes transform: Marchenko–Pastur and Wigner's semicircle;
- spiked models: the BBP transition for eigenvalues and eigenvectors, on Harman's 24 tests (Board);
- Tracy–Widom fluctuations and Roy's largest-root test (Board);
- sparse PCA, its computational barrier, and neighbourhood selection for graphical models;
- inference by the debiased lasso, on the diabetes data with interactions, with explicit caveats about its full-model target, near-collinearity and unvalidated finite-sample coverage.

It keeps three promises:
- **Part 32** showed the lasso and basis pursuit working, by experiment. Chapters 1–3 prove the rates and say when the
  right variables are found.
- **Part 31**'s PCA and factor analysis assumed p fixed as n grows. Chapters 6–10 work with p/n fixed, and find a
  threshold below which ordinary-PCA directional overlap vanishes in the proportional isotropic-spike limit; other statistics or structural assumptions can retain information.
- **Part 51** built concentration, random matrices and Gaussian comparison as probability. Here they are the proofs:
  the maximum of p Gaussians sets λ, Gordon's inequality gives restricted eigenvalues, and matrix Bernstein drives
  matrix completion.

**Built in this part:**
- **`statkit.hdstat`** ([`explainer/stats/kit/hdstat.py`](../../../explainer/stats/kit/hdstat.py)), tested in
  `tests/test_stats_kit_hdstat.py`:
  - the Marchenko–Pastur density, its Stieltjes transform and the inversion; Wigner matrices and the semicircle;
  - the BBP limits of the top eigenvalue and of the eigenvector overlap, the inverse map, the spike's fluctuation,
    Anderson's interval and a BBP-corrected one;
  - Tracy–Widom distributions for β = 1 and 2 by Bornemann's quadrature of Fredholm determinants, with quantiles,
    moments and Johnstone's centring and scaling;
  - a rate-scale λ helper and oracle rate; the local simulation uses a corrected confidence-calibrated λ, the irrepresentable constant, signed support along the exact LARS path;
  - AR(1) covariances, banding, thresholding, Ledoit–Wolf, sin θ and the Davis–Kahan bound;
  - spiked and sparse-spiked samplers, diagonal thresholding, neighbourhood selection, chain precision matrices,
    low-rank matrices.
- **The random-matrix lab** (`SpectrumBulk` in `explainer/stats/viz.py`), the part's instrument: a spectrum's histogram
  (the bulk), its limiting law, the edges of the support, spikes as stems rising out of the bulk, and arrows for the
  BBP map.

**Data.**
- From the Museum: Harman's 24 psychological tests (Holzinger & Swineford 1939; Harman 1967), and the diabetes data of
  the LARS paper (Efron, Hastie, Johnstone & Tibshirani 2004).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Anderson's interval for a simple eigenvalue | spike 1 + ℓ = 4, n = 200, p = 100 | 95% | 63.6% | broken |
| BBP-corrected interval for the spike | spike 1 + ℓ = 4, n = 200, p = 100 | 95% | 95.5% | kept |
| normal test for a spike | null Σ = I, n = 200, p = 100 | size 5% | 100% | broken |
| Roy's test, Tracy–Widom calibration | null Σ = I, n = 200, p = 100 | size 5% | 4.2% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats52.compute   # once (about ten minutes)
python tools/build.py stats52 -q l                         # fast 480p preview
python tools/build.py stats52                              # 1080p30 -> renders/stats52.mp4
python tools/qa_scene.py stats52 Spikes
python tools/lecture_length.py stats52 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Noise with structure | n = 1,000, p = 500: eigenvalues 0.085 to 2.92 (MP edges 0.086, 2.914); top share 0.59% vs 0.20% |
| 1 | The oracle inequality | p = 500, s = 10: error 2.91 (n = 100) → 0.89 (n = 1,200), with a conditional-Gaussian 95% noise-event penalty including actual column norms; best tested λ at 0.125 × that conservative penalty |
| 2 | Support recovery | s = 8: P(exact signed support) at θ = 1: 50%, 43%, 40% for p = 128, 256, 512; 0% → 100% from θ = 0.4 to 2; irrepresentable 0.21 (100%) vs 1.51 (0%) |
| 3 | Decomposable regularizers | the instances table: ℓ₁, group, nuclear, sparse GLM |
| 4 | Matrix completion | 100 × 100, rank 3: dof 5.9%; median error 0.779 at 6%, 0.129 at 15%, 0.00478 at 30%; four trials, final λ = 0.05, checked proximal fixed-point residual < 2×10⁻⁷ |
| 5 | Covariance | AR(1) ρ = 0.7, p = 200, n = 50: sample 11.1, Ledoit–Wolf 4.4, oracle-tuned thresholding 3.5, oracle-tuned banding 2.3 (‖Σ‖ = 5.66) |
| 6 | Perturbation | n = 500, p = 200: sin θ 0.51 at ℓ = 2, 0.24 at ℓ = 8; Davis–Kahan vacuous until ℓ = 4; asymptotic BBP reference |
| 7 | Random-matrix laws | Stieltjes inversion at η = 0.2, 0.05, 10⁻⁶; Wigner n = 1,000: extremes −1.971, 1.984 |
| 8 | Spikes | γ = 1/2: threshold 0.707; ℓ = 3: top 4.73 (limit 4.67), overlap 0.82 (0.81); Harman: 2 eigenvalues above 1.98, spikes 7.95 and 1.69, assumed-model squared overlaps 0.97 and 0.52 (not validated for this correlation matrix); Kaiser keeps 5 |
| 9 | Tracy–Widom | n = 400, p = 200: scaled mean −1.18, SD 1.25 (TW₁ −1.207, 1.268); q₀.₉₅ = 0.979; Roy's size 4.8% |
| 10 | Sparse PCA, graphs | p = 1,000, k = 10, ℓ = 2: overlap² at n = 800, PCA 0.40, diagonal thresholding 0.79; chain p = 30: sampled mean true-edge rate reaches one from n = 100; fraction of absent edges selected ≤ 4%; not a guarantee of exact-graph recovery |
| 11 | The debiased lasso | diabetes, n = 442, p = 64: the lasso (one SE) keeps 8; bmi 23.7 → 27.0 [21.3, 32.8], ltg 20.9 → 27.4 [21.4, 33.4]; 5 main effects exclude zero (sex, bmi, bp, hdl, ltg); OLS intervals for tc, ldl, hdl, ltg are thousands wide |
| 12 | Outro | — |

## Sources

- **The lasso.**
  - R. Tibshirani, *JRSS B* 58 (1996); P. Bickel, Y. Ritov & A. Tsybakov, *Ann. Stat.* 37 (2009); G. Raskutti,
    M. Wainwright & B. Yu, *JMLR* 11 (2010).
  - P. Zhao & B. Yu, *JMLR* 7 (2006); H. Zou, *JASA* 101 (2006); M. Wainwright, *IEEE Trans. Inf. Theory* 55 (2009).
  - S. Negahban, P. Ravikumar, M. Wainwright & B. Yu, *Stat. Sci.* 27 (2012).
- **Low rank.** M. Fazel, PhD thesis (2002); E. Candès & B. Recht, *Found. Comput. Math.* 9 (2009); E. Candès & T. Tao,
  *IEEE Trans. Inf. Theory* 56 (2010); D. Gross, *IEEE Trans. Inf. Theory* 57 (2011); B. Recht, *JMLR* 12 (2011);
  V. Koltchinskii, K. Lounici & A. Tsybakov, *Ann. Stat.* 39 (2011); R. Mazumder, T. Hastie & R. Tibshirani, *JMLR* 11
  (2010).
- **Covariance.** P. Bickel & E. Levina, *Ann. Stat.* 36 (2008a, b); O. Ledoit & M. Wolf, *J. Multivar. Anal.* 88
  (2004), *Ann. Stat.* 40 (2012); C. Stein, Rietz lecture (1975).
- **Perturbation.** H. Weyl, *Math. Ann.* 71 (1912); C. Davis & W. Kahan, *SIAM J. Numer. Anal.* 7 (1970); P.-Å. Wedin,
  *BIT* 12 (1972); Y. Yu, T. Wang & R. Samworth, *Biometrika* 102 (2015).
- **Random matrices.**
  - V. Marchenko & L. Pastur, *Mat. Sb.* 72 (1967); E. Wigner, *Ann. Math.* 62 (1955); J. Silverstein & Z. Bai,
    *J. Multivar. Anal.* 54 (1995).
  - J. Baik, G. Ben Arous & S. Péché, *Ann. Probab.* 33 (2005); D. Paul, *Stat. Sinica* 17 (2007); Z. Bai & J. Yao,
    *Ann. IHP* 44 (2008).
  - C. Tracy & H. Widom, *Comm. Math. Phys.* 159 (1994), 177 (1996); I. Johnstone, *Ann. Stat.* 29 (2001);
    F. Bornemann, *Math. Comp.* 79 (2010); J. Baik, P. Deift & K. Johansson, *JAMS* 12 (1999).
  - S. Roy, *Ann. Math. Stat.* 24 (1953); S. Kritchman & B. Nadler, *Chemometr. Intell. Lab.* 94 (2008); A. Onatski,
    M. Moreira & M. Hallin, *Ann. Stat.* 41 (2013); N. Patterson, A. Price & D. Reich, *PLoS Genet.* 2 (2006).
- **Sparse PCA and graphs.** I. Johnstone & A. Lu, *JASA* 104 (2009); V. Vu & J. Lei, *Ann. Stat.* 41 (2013);
  A. d'Aspremont et al., *SIAM Rev.* 49 (2007); Q. Berthet & P. Rigollet, *Ann. Stat.* 41 (2013); N. Meinshausen &
  P. Bühlmann, *Ann. Stat.* 34 (2006); J. Friedman, T. Hastie & R. Tibshirani, *Biostatistics* 9 (2008); P. Ravikumar
  et al., *EJS* 5 (2011).
- **Inference.** K. Knight & W. Fu, *Ann. Stat.* 28 (2000); A. Chatterjee & S. Lahiri, *Proc. AMS* 138 (2010);
  C.-H. Zhang & S. Zhang, *JRSS B* 76 (2014); S. van de Geer, P. Bühlmann, Y. Ritov & R. Dezeure, *Ann. Stat.* 42
  (2014); A. Javanmard & A. Montanari, *JMLR* 15 (2014).
- **Data.** K. Holzinger & F. Swineford (1939); H. Harman, *Modern Factor Analysis* (1967); B. Efron, T. Hastie,
  I. Johnstone & R. Tibshirani, *Ann. Stat.* 32 (2004).
- **Books.** M. Wainwright, *High-Dimensional Statistics* (2019); P. Bühlmann & S. van de Geer, *Statistics for
  High-Dimensional Data* (2011); Z. Bai & J. Silverstein (2010); R. Couillet & Z. Liao (2022); T. Hastie,
  R. Tibshirani & M. Wainwright, *Statistical Learning with Sparsity* (2015).

## Problems and solutions

1. **The basic inequality.**
   - Optimality of β̂ against β*: (1/2n)‖y − Xβ̂‖² + λ‖β̂‖₁ ≤ (1/2n)‖ε‖² + λ‖β*‖₁.
   - With y = Xβ* + ε and Δ = β̂ − β*, this is (1/2n)‖XΔ‖² ≤ ⟨X^⊤ε/n, Δ⟩ + λ(‖β*‖₁ − ‖β̂‖₁).
   - Hölder gives ⟨X^⊤ε/n, Δ⟩ ≤ (λ/2)‖Δ‖₁. The triangle inequality gives ‖β*‖₁ − ‖β̂‖₁ ≤ ‖Δ_S‖₁ − ‖Δ_{S^c}‖₁.
   - So 0 ≤ (λ/2)(‖Δ_S‖₁ + ‖Δ_{S^c}‖₁) + λ(‖Δ_S‖₁ − ‖Δ_{S^c}‖₁), which gives ‖Δ_{S^c}‖₁ ≤ 3‖Δ_S‖₁.
2. **The noise's correlations.**
   - For fixed columns with ‖X_j‖² = n and independent homoskedastic Gaussian errors, each X_j^⊤ε/n ~ N(0, σ²/n), so P(|X_j^⊤ε/n| > t) ≤ 2e^{−nt²/(2σ²)}.
   - A union bound over j gives 2p e^{−nt²/(2σ²)}. Setting this equal to δ gives t = σ√(2 log(2p/δ)/n).
3. **The nuclear norm is decomposable.**
   - If A = U_A D_A V_A^⊤ and B = U_B D_B V_B^⊤ with U_A ⊥ U_B and V_A ⊥ V_B, then [U_A U_B] blockdiag(D_A, D_B) [V_A V_B]^⊤
     is an SVD of A + B.
   - So the singular values of A + B are those of A together with those of B, and the nuclear norms add.
4. **Davis–Kahan in two dimensions.**
   - The eigenvector of [[1 + δ, ε], [ε, 1]] is at angle θ with tan 2θ = 2ε/δ.
   - For small ε, sin θ ≈ ε/δ, against the bound 2ε/δ: right order, off by a factor of 2.
   - At ε = δ/2, θ = 22.5° and sin θ = 0.38, against the bound 1.
5. **The BBP map.**
   - ψ(ℓ) = 1 + ℓ + γ + γ/ℓ, so ψ′(ℓ) = 1 − γ/ℓ², which is zero at ℓ = √γ. There ψ(√γ) = (1 + √γ)², the bulk's edge.
   - Solving ψ(ℓ) = λ̂ gives ℓ² − (λ̂ − 1 − γ)ℓ + γ = 0. Take the larger root, ℓ = [c + √(c² − 4γ)]/2 with
     c = λ̂ − 1 − γ.
6. **Marchenko–Pastur from its quadratic.**
   - m = [−(z + γ − 1) + √((z + γ − 1)² − 4γz)]/(2γz), choosing the branch with Im m > 0.
   - The discriminant (z − 1 − γ)² − 4γ is negative exactly for z ∈ (a, b), with a, b = (1 ∓ √γ)².
   - There Im m(x + i0) = √((b − x)(x − a))/(2γx), and dividing by π gives the density.

## Glossary

- **Sparse regression.**
  - Oracle inequality; restricted eigenvalue; cone condition; basic inequality; restricted strong convexity: rates.
  - Support recovery; irrepresentable condition; primal–dual witness; beta-min condition; sign consistency:
    selection.
  - Decomposable regularizer; dual norm; subspace compatibility; group lasso; nuclear norm: the unified theory.
- **Matrices.**
  - Matrix completion; incoherence; degrees of freedom; SoftImpute: low rank.
  - Banding; thresholding; Ledoit–Wolf shrinkage; nonlinear shrinkage: covariances.
  - Weyl's inequality; eigengap; Davis–Kahan sin θ; Wedin's theorem: perturbation.
- **Random-matrix theory.**
  - Empirical spectral distribution; Stieltjes transform; resolvent; Marchenko–Pastur law; semicircle law;
    universality: the bulk.
  - Spiked covariance model; BBP transition; eigenvector overlap; Tracy–Widom law; Fredholm determinant; Roy's largest
    root; parallel analysis: the edge.
- **Structure and inference.**
  - Sparse PCA; diagonal thresholding; statistical–computational gap; neighbourhood selection; graphical lasso:
    structured spectra.
  - Debiased (desparsified) lasso; nodewise regression; one-step estimator; selective inference: intervals.

## Where it comes back

- **Part 53**: posterior contraction for sparse priors, at this part's rates.
- **Part 54**: learning bounds in high dimensions.
- **Part 56**: selective inference after the lasso.
- **Part 59**: the lasso's exact risk when p/n → δ, by the CGMT and approximate message passing.
- **Part 62**: causal adjustment for many confounders.

## QA reconciliation

All thirteen numerical items regenerated. Nineteen checks pass: thirteen independent numerical/runtime cases and six toolkit checks. The independently retrieved Harman correlation matrix and sample count match the Museum exactly; all 442×10 diabetes feature values and 442 outcomes match the official scikit-learn distribution.

The lasso simulation now uses λ = 2σ max_j‖X_j‖₂ √(2 log(2p/δ))/n, δ = .05, so the conditional Gaussian union bound implies λ ≥ 2‖Xᵀε/n‖∞ with probability at least .95. Every fit passes a KKT check. This replaces a helper whose default effective constant was too small to justify that guarantee. The empirical error curve now runs from 2.911 to 0.888, and its axes include all errors. The oracle penalty sweep is a finite experiment, not a guarantee that cross-validation preserves the noise event.

An explicit normalized full-rank design with irrepresentable value 1.2 nevertheless recovers the signed support for a constructed finite noise realization. It verifies why irrepresentability cannot be described as impossibility at every λ for every dataset. The threshold discussion now states asymptotic regime, beta-min, tuning and uniqueness conditions. Full-path success uses knowledge of the truth and is an oracle criterion. Thirty replicates per point and empirical Monte Carlo errors are retained.

Decomposability uses nested model and tangent spaces; the nuclear norm is not additive over every Frobenius-orthogonal pair. Independent matrix examples verify both the counterexample and the correct two-sided row/column orthogonality case. Logistic rates require local curvature and bounded parameter/design conditions. Low-rank completion states sampling, both singular-space incoherence conditions and bounded-entry/spikiness requirements. An accelerated proximal solver replaces unchecked 300-step fits. Every penalty level converges to a normalized fixed-point residual below 2×10⁻⁷, requiring up to 2,730 iterations in this run. Four-trial medians and a positive final penalty remain finite-run illustrations, not exact recovery or high-probability certificates. Full-observation solutions match independent singular-value shrinkage, and masked solutions pass an independent proximal fixed-point check.

Covariance comparisons explicitly identify oracle tuning. Gaussian operator-error scales include √(p/n)+p/n. Positive definiteness of shrinkage needs positive target variance and shrinkage intensity; hard banding/thresholding need not preserve it. Wedin's separation is not an arbitrary population eigengap. MP, BBP and Tracy–Widom statements distinguish limiting laws from finite-sample observations, density from point masses, ordinary PCA from all possible inference, and conditional computational evidence from unconditional lower bounds. Fredholm cutoff/order checks show errors below 2×10⁻⁵ at the checked points; the default β=1 cutoff is not certified to machine precision. Histograms preserve total sample mass.

Harman uses p/(n−1) for the centered Gaussian reference. Its correlation spectrum is not established to follow identity noise plus a few positive spikes. BBP-inverted spikes and squared overlaps are assumed-model illustrations, not validated estimates of true factor loadings or a factor count. Counting two eigenvalues above a reference edge is not an implemented calibrated sequential Kritchman–Nadler test. Sparse-PCA minimax rates include (1+ℓ)/ℓ² and a cap at one; plain diagonal thresholding does not generally attain that benchmark. Graph recovery also needs minimum edge strength, spectral control and incoherence, beyond a sample-count expression.

For diabetes, SVD-based least-squares covariance avoids unstable normal-equation inversion and includes the fitted intercept in residual degrees of freedom. An independent QR calculation agrees on an ill-conditioned example; rank-deficient designs are rejected. The actual 64-term design has condition number about 5,470. Main coefficients are conditional associations at zero centered values of other main predictors, not total or causal effects. The debiased estimator still targets the original full-model coefficient. Nodewise inverse residuals, conditional scales and selected sizes are recorded. A two-sparse near-collinearity example has substantially different coefficients but nearly indistinguishable joint Gaussian laws, illustrating why regularization cannot create missing information. Coefficient sparsity alone does not validate the narrow intervals: approximate-inverse, noise, design and bias-remainder conditions are also needed. Their nominal 95% finite-data coverage has not been established. Coordinatewise inference is distinguished from simultaneous and selected-model inference.

The four Board rates use empirical Monte Carlo errors across 2,000 independent datasets per setting. Coverage at one supercritical spike and size under one identity-noise null are finite simulations, not uniform or exact guarantees. Thirty persistent theorem headings and local viewport clipping prepare the visual pass. The recorded English sampled visual checkpoint is complete. Chinese narration/captions, continuous listening and final masters remain open.
