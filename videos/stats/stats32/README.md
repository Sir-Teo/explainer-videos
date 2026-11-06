# Statistics, Built — Part 32: Sparsity

Part 32 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the twelfth part of Stage III, Master's. Part 31 ended with variables
outnumbering observations. This part asks how to solve for many unknowns from few equations, by betting that most of
them are zero:
- ridge, the ℓq family and the lasso;
- the lasso's computation and tuning;
- its relatives and its Bayesian counterparts;
- compressed sensing;
- honest inference after selection;
- matrix completion.

Its instrument is the phantom (`PhantomPanel`): an image panel of greyscale pixels for the Shepp–Logan phantom, its
k-space mask and its reconstructions, on a common scale. Its kit is `statkit.sparse`.

It opens with Candès's 2004 experiment (Candès, Romberg & Tao 2006). The modified Shepp–Logan phantom (128 × 128) is
measured on 22 radial lines of its Fourier transform, 20.6% of the coefficients:
- the minimum-energy (zero-filled) reconstruction has a relative error of 48.2%;
- minimum total variation, by Chambolle–Pock, recovers it exactly: errors 19.2%, 4.6%, 0.22%, 1.2 × 10⁻⁵ and
  1.6 × 10⁻¹⁰ after 20, 100, 400, 1,500 and 4,000 iterations;
- only 4.6% of horizontal neighbours differ: the image is sparse in its jumps.

From there the part covers:
- **The upgrade of Part 19**, the p > n problem and the s log(p/s) count (≈ 76 for p = 20,000, s = 10).
- **Ridge** (Hoerl & Kennard 1970) on the diabetes data of Efron, Hastie, Johnstone & Tibshirani (2004): 442
  patients, 10 baseline variables.
  - Total cholesterol and LDL correlate 0.90; least squares gives them −37.7 and +22.7 per SD; ridge (λ = 10) gives
    −11.3 and +1.8.
  - Singular values 42.2 … 1.95 (condition number 21.7). Shrinkage factors at λ = 10 are 0.99 … 0.78, 0.28; at
    λ = 1,000 they are 0.64 … 0.004.
  - The weakest direction is −0.71·tc + 0.56·ldl + …; the ridge trace against df.
  - Ridge as a normal prior; Hoerl and Kennard's existence theorem (dMSE/dλ at 0 = −2σ²Σd_j⁻⁴ < 0).
- **From ℓ0 to ℓ1.**
  - Best subset and hard thresholding; 2⁶⁴ = 1.8 × 10¹⁹ subsets (585 years at 10⁹ fits a second); Natarajan's
    NP-hardness (1995).
  - The ℓq balls; the octahedron; ℓ1 as the convex envelope of ℓ0 on the box.
- **The lasso** (Tibshirani 1996).
  - The KKT conditions; λ_max = ‖Xᵀy‖∞/n.
  - Soft, hard and ridge thresholding; the diamond touching at a corner (1.5, 0) where the disc touches at
    (1.42, 0.47).
  - Uniqueness, at most min(n, p) nonzeros, df = E#{nonzero} (Zou, Hastie & Tibshirani 2007); the bias of λ.
- **Computing the path.** Coordinate descent with warm starts, active sets and strong rules (glmnet). LARS and its
  lasso modification. On the diabetes data:
  - the order of entry is BMI, log triglycerides, blood pressure, HDL, sex, glucose, total cholesterol, TC/HDL, LDL,
    age;
  - HDL drops out at s = 0.810 and returns at 0.827, the only difference from pure LARS;
  - at s = 1, OLS on unit-norm columns: (−10.0, −239.8, 519.8, 324.4, −792.2, 476.7, 101.0, 177.1, 751.3, 67.6),
    matching the paper's Table 1.
- **The penalty zoo.**
  - Elastic net. With three near-copies (correlation 0.96), the lasso takes two in turn and the elastic net shares the
    effect.
  - Group lasso (block soft thresholding); fused lasso (RMSE 0.23 against 0.55 raw on a three-step signal); adaptive
    lasso; SCAD and MCP and their thresholding rules.
  - Support recovery: 200 data sets, n = 100, p = 200, eight effects of 0.5–1, AR(0.5) design, common
    λ = 1.1√(2 log p/n):

    | Penalty | True found (of 8) | False included | Exact support | ‖β̂ − β‖² |
    |---|---|---|---|---|
    | lasso | 7.02 | 2.74 | 3.0% | 1.50 |
    | adaptive lasso | 7.71 | 2.75 | 8.5% | 0.35 |
    | SCAD | 7.07 | 1.88 | 8.0% | 1.34 |
    | MCP | 7.16 | 0.40 | 32.5% | 0.84 |

- **Choosing λ** on the LARS paper's 64-term quadratic model (main effects, interactions, squares of the standardized
  variables).
  - 10-fold CV: the minimum (λ = 2.94) keeps 15 terms with CV MSE 2,957, against 5,906 with none. The one-SE rule
    (λ = 5.82) keeps 11: sex, BMI, BP, HDL, LTG, age×sex, age×BP, age×glucose, BMI×BP, BMI² and glucose².
  - CV is not selection-consistent.
  - Stability selection (60 half-samples) finds 9 terms with Π ≥ 0.8: sex, BMI, BP, HDL, LTG, glucose, age×sex,
    BMI×BP and glucose².
- **Bayesian sparsity.**
  - The lasso is the Laplace posterior mode. Its posterior mean is never zero and biased by λ; the Bayesian lasso
    (Park & Casella 2008).
  - The horseshoe (Carvalho, Polson & Scott 2010) and its Beta(½, ½) shrinkage.
  - 200 normal means, 10 at 5:

    | Estimate | Total squared error |
    |---|---|
    | observations | 203 |
    | universal soft threshold (3.26) | 86 |
    | Bayesian lasso | 74 |
    | horseshoe (τ̂ ≈ 0.21) | 31 |

  - Spike-and-slab.
- **Compressed sensing.**
  - Basis pursuit against least norm, for p = 200, n = 60 Gaussian measurements and s = 10. ℓ1 is exact (7.7 × 10⁻¹³);
    ℓ2 has 85% error.
  - The null space property, derived; RIP (Candès & Tao 2005); random matrices need n ≳ s log(p/s).
  - The empirical phase transition (p = 100, 20 trials per cell) against Donoho–Tanner's curve, with ρ(0.5) = 0.386.
  - The phantom against the number of radial lines:

    | Lines | Fraction measured | Minimum energy | Minimum TV |
    |---|---|---|---|
    | 4 | 3.1% | 73.5% | 74.4% |
    | 8 | 6.9% | 66.2% | 57.9% |
    | 12 | 10.7% | 59.4% | 27.7% |
    | 16 | 14.2% | 56.0% | 3.7% |
    | 22 | 20.6% | 48.2% | 1.4 × 10⁻⁸ |
    | 30 | 27.3% | 41.8% | 8.9 × 10⁻¹¹ |

- **Inference after the lasso.**
  - Naive post-lasso intervals; the winner's curse. With n = 100, p = 200 and λ = √(2 log p/n), the 0.25 effect is
    selected 23% of the time, with mean estimate 0.34 when selected.
  - The debiased lasso with nodewise regression (van de Geer, Bühlmann, Ritov & Dezeure 2014; Zhang & Zhang 2014;
    Javanmard & Montanari 2014).
  - Double selection (Belloni, Chernozhukov & Hansen 2014): single selection estimates 0.71 and double selection
    0.49, for α = 0.5.
  - PoSI and selective inference, pointing to Part 56.
- **Matrix completion.**
  - The Netflix Prize; the nuclear norm as the convex envelope of rank (Fazel 2002).
  - SoftImpute (Mazumder, Hastie & Tibshirani 2010) on a 120 × 90 rank-4 matrix with 30% of its entries observed
    with noise. The best λ = 3 gives held-out error 27.6%. Singular values 133, 113, 93, 70 become 114, 96, 76, 57;
    the next are 8 and 6.
  - Candès & Recht's recovery theorem; incoherence.

Data:
- the diabetes data (Efron et al. 2004, as distributed with scikit-learn) are the Museum's;
- the phantom is Shepp & Logan's (1974) in Toft's modified form;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.sparse`** ([`explainer/stats/kit/sparse.py`](../../../explainer/stats/kit/sparse.py)), checked in
  `tests/test_stats_kit_sparse.py`:
  - **Ridge and lasso:** ridge by the SVD; the lasso, elastic net and adaptive lasso by coordinate descent along a
    warm-started path; KKT checks; the exact LARS and LARS-lasso paths.
  - **Other penalties:** soft, hard, SCAD and MCP rules and their coordinate descent; the group lasso.
  - **Tuning:** CV with the one-SE rule; stability selection.
  - **Bayesian sparsity:** Laplace and horseshoe shrinkage profiles; Gibbs samplers for the Bayesian lasso and the
    horseshoe.
  - **Compressed sensing:** basis pursuit by LP; the Donoho–Tanner curve and empirical phase grid; the Shepp–Logan
    phantom, radial masks and TV recovery.
  - **Inference and matrices:** naive post-selection OLS, the debiased lasso, single and double selection; SoftImpute.
- **The Museum** gains `diabetes()`.
- **The phantom** (`PhantomPanel` in `explainer/stats/viz.py`).

The Coverage Board gains five rows. 95% intervals, 1,000 data sets each:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| naive post-lasso CIs, every selected variable | n = 100, p = 200, 6 true effects (5,651 intervals) | 75.1% | broken |
| debiased lasso | β_j = 0.25 | 95.6% | kept |
| debiased lasso | β_j = 0 | 95.7% | kept |
| single selection, treatment effect | n = 100, p = 100, 5 confounders | 9.2% | broken |
| double selection, treatment effect | same | 94.2% | kept |

Naive intervals for false positives cover 0 only 25% of the time. For the 0.25 effect, given that it is selected, they
cover 92%.

## Build it

```bash
python -m videos.stats.stats32.compute         # once (a few minutes)
python tools/build.py stats32 -q l             # fast 480p preview
python tools/build.py stats32                  # 1080p30 -> renders/stats32.mp4
python tools/qa_scene.py stats32 Compressed
python tools/lecture_length.py stats32 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Candès's phantom | 20.6% of k-space; 48% vs 1.6 × 10⁻¹⁰ |
| 1 | Upgrade: what Part 19 shrank | s log(p/s) ≈ 76 |
| 2 | Ridge | −37.7/+22.7 → −11.3/+1.8; condition number 22 |
| 3 | From ℓ0 to ℓ1 | 2⁶⁴ subsets, 585 years |
| 4 | The lasso | corner (1.5, 0) vs (1.42, 0.47) |
| 5 | Computing the path | 12 steps; HDL leaves at 0.81 |
| 6 | The penalty zoo | MCP 0.40 false vs lasso 2.74 |
| 7 | Choosing λ | 15 / 11 terms; 9 stable |
| 8 | Bayesian sparsity | SSE 203 / 86 / 74 / 31 |
| 9 | Compressed sensing | ρ(0.5) = 0.386; 16 lines 3.7%, 22 exact |
| 10 | Inference after the lasso | 75.1% vs 95.6%; 9.2% vs 94.2% |
| 11 | Matrix completion | held-out 27.6%; rank 4 at λ = 15 |
| 12 | Outro | — |

## Sources

- **Ridge and subsets.**
  - A. Hoerl & R. Kennard, *Technometrics* 12 (1970); A. Hoerl, *Chem. Eng. Prog.* 58 (1962).
  - G. Furnival & R. Wilson, *Technometrics* 16 (1974); B. Natarajan, *SIAM J. Comput.* 24 (1995).
  - D. Bertsimas, A. King & R. Mazumder, *Ann. Stat.* 44 (2016).
- **The lasso and its computation.**
  - L. Breiman, *Technometrics* 37 (1995); R. Tibshirani, *JRSS B* 58 (1996).
  - S. Chen, D. Donoho & M. Saunders, *SIAM J. Sci. Comput.* 20 (1998).
  - B. Efron, T. Hastie, I. Johnstone & R. Tibshirani, *Ann. Stat.* 32 (2004).
  - J. Friedman, T. Hastie, H. Höfling & R. Tibshirani, *Ann. Appl. Stat.* 1 (2007); J. Friedman, T. Hastie &
    R. Tibshirani, *J. Stat. Softw.* 33 (2010).
  - R. Tibshirani et al., *JRSS B* 74 (2012) (strong rules); P. Tseng, *JOTA* 109 (2001).
  - H. Zou, T. Hastie & R. Tibshirani, *Ann. Stat.* 35 (2007); R. Tibshirani, *EJS* 7 (2013).
- **Penalties.**
  - H. Zou & T. Hastie, *JRSS B* 67 (2005); M. Yuan & Y. Lin, *JRSS B* 68 (2006).
  - R. Tibshirani, M. Saunders, S. Rosset, J. Zhu & K. Knight, *JRSS B* 67 (2005); L. Rudin, S. Osher & E. Fatemi,
    *Physica D* 60 (1992); N. Johnson, *JCGS* 22 (2013).
  - H. Zou, *JASA* 101 (2006); J. Fan & R. Li, *JASA* 96 (2001); C.-H. Zhang, *Ann. Stat.* 38 (2010).
  - P. Breheny & J. Huang, *Ann. Appl. Stat.* 5 (2011); N. Simon, J. Friedman, T. Hastie & R. Tibshirani, *JCGS* 22
    (2013).
- **Tuning.** N. Meinshausen & P. Bühlmann, *Ann. Stat.* 34 (2006), *JRSS B* 72 (2010); C. Leng, Y. Lin & G. Wahba,
  *Stat. Sinica* 16 (2006).
- **Bayes.**
  - T. Park & G. Casella, *JASA* 103 (2008); C. Carvalho, N. Polson & J. Scott, *Biometrika* 97 (2010).
  - E. Makalic & D. Schmidt, *IEEE SPL* 23 (2016); T. Mitchell & J. Beauchamp, *JASA* 83 (1988); E. George &
    R. McCulloch, *JASA* 88 (1993).
- **Compressed sensing.**
  - E. Candès, J. Romberg & T. Tao, *IEEE Trans. IT* 52 (2006); D. Donoho, *IEEE Trans. IT* 52 (2006).
  - E. Candès & T. Tao, *IEEE Trans. IT* 51 (2005); E. Candès, *C. R. Acad. Sci.* 346 (2008).
  - A. Cohen, W. Dahmen & R. DeVore, *JAMS* 22 (2009); R. Baraniuk et al., *Constr. Approx.* 28 (2008).
  - M. Rudelson & R. Vershynin, *CPAM* 61 (2008); D. Donoho & J. Tanner, *Phil. Trans. A* 367 (2009); D. Donoho,
    A. Maleki & A. Montanari, *PNAS* 106 (2009).
  - L. Shepp & B. Logan, *IEEE Trans. Nucl. Sci.* 21 (1974); A. Chambolle & T. Pock, *JMIV* 40 (2011).
- **Inference.**
  - S. van de Geer, P. Bühlmann, Y. Ritov & R. Dezeure, *Ann. Stat.* 42 (2014); C.-H. Zhang & S. Zhang, *JRSS B* 76
    (2014).
  - A. Javanmard & A. Montanari, *JMLR* 15 (2014); A. Belloni, V. Chernozhukov & C. Hansen, *Rev. Econ. Stud.* 81
    (2014).
  - R. Berk, L. Brown, A. Buja, K. Zhang & L. Zhao, *Ann. Stat.* 41 (2013); J. Lee, D. Sun, Y. Sun & J. Taylor,
    *Ann. Stat.* 44 (2016).
- **Matrices.**
  - M. Fazel, PhD thesis, Stanford (2002); E. Candès & B. Recht, *Found. Comput. Math.* 9 (2009); E. Candès &
    T. Tao, *IEEE Trans. IT* 56 (2010).
  - B. Recht, *JMLR* 12 (2011); R. Mazumder, T. Hastie & R. Tibshirani, *JMLR* 11 (2010); R. Bell & Y. Koren, *SIGKDD
    Explorations* 9 (2007).
- **Books.**
  - T. Hastie, R. Tibshirani & M. Wainwright, *Statistical Learning with Sparsity* (2015).
  - P. Bühlmann & S. van de Geer, *Statistics for High-Dimensional Data* (2011).
  - S. Foucart & H. Rauhut, *A Mathematical Introduction to Compressive Sensing* (2013).
  - T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning* (2nd ed., 2009).

## Problems and solutions

**1. Ridge through the SVD.**

*Solution.* With X = UDVᵀ, XᵀX + λI = V(D² + λI)Vᵀ, so β̂_λ = V(D² + λI)⁻¹DUᵀy. The fit is Xβ̂_λ =
UD(D² + λI)⁻¹DUᵀy = Σ_j u_j d_j²/(d_j² + λ) u_jᵀy. The hat matrix H_λ = U diag(d_j²/(d_j² + λ)) Uᵀ has trace
Σ_j d_j²/(d_j² + λ).

**2. Soft thresholding.**

*Solution.* The function f(b) = ½(b − z)² + λ|b| is strictly convex, and 0 ∈ ∂f(b) = b − z + λ∂|b|.
- If b > 0, then b = z − λ, which needs z > λ.
- If b < 0, then b = z + λ, which needs z < −λ.
- If b = 0, then z ∈ λ[−1, 1], i.e. |z| ≤ λ.

Together, b = sign(z)(|z| − λ)₊.

**3. Where the path begins.**

*Solution.* At β = 0 the gradient of the loss is −Xᵀy/n, and the subdifferential of λ‖β‖₁ is λ[−1, 1]ᵖ. So
0 ∈ −Xᵀy/n + λ[−1, 1]ᵖ iff |x_jᵀy|/n ≤ λ for every j, i.e. λ ≥ ‖Xᵀy‖∞/n. By convexity, a point satisfying the
optimality condition is a minimizer.

**4. The null space property.**

*Solution.* Let x be supported on S. Any other feasible point is z = x + h with 0 ≠ h ∈ null(A). Then
‖z‖₁ = ‖x_S + h_S‖₁ + ‖h_{S^c}‖₁ ≥ ‖x_S‖₁ − ‖h_S‖₁ + ‖h_{S^c}‖₁ > ‖x_S‖₁ = ‖x‖₁, using the reverse triangle
inequality and then the hypothesis. So x is the unique minimizer.

**5. The Laplace posterior mean.**

*Solution.* The posterior density is π(θ | y) ∝ exp(−(y − θ)²/2 − λ|θ|), and the mean is
E(θ | y) = ∫θ π / ∫π. Write the numerator as ∫θ e^{−(y−θ)²/2} e^{−λ|θ|} dθ. For y > 0, pair θ with −θ: the
integrand at θ > 0 exceeds the magnitude at −θ, because e^{−(y−θ)²/2} > e^{−(y+θ)²/2} when yθ > 0. So the
numerator is strictly positive. Likewise it is negative for y < 0, so E(θ | y) ≠ 0 whenever y ≠ 0. (The
closed form in `laplace_posterior_mean` writes the posterior as a mixture of two truncated normals.)

**6. Singular value thresholding.**

*Solution.* Minimize ½‖Z − W‖²_F + λ‖Z‖_*. Write W = UΣVᵀ. For any Z with singular values s, von Neumann's
inequality gives ⟨Z, W⟩ ≤ Σ s_iσ_i. So ½‖Z − W‖² ≥ ½Σ(s_i − σ_i)², with equality when Z shares W's singular vectors.
The problem therefore reduces to min_s Σ[½(s_i − σ_i)² + λs_i] over s_i ≥ 0. The solution is s_i = (σ_i − λ)₊, so the
minimizer is Z = U(Σ − λI)₊Vᵀ.

## Glossary

- **Sparsity; support; the bet on sparsity; s log(p/s)**: few nonzero coefficients, which ones, and how much data
  finding them needs.
- **Ridge; shrinkage factor; effective degrees of freedom; ridge trace**: ℓ2 penalization and its anatomy.
- **Best subset; ℓ0; hard thresholding; convex envelope**: counting and its tightest convex relaxation.
- **Lasso; subgradient; KKT conditions; soft thresholding; λ_max**: ℓ1 penalization and its optimality conditions.
- **Coordinate descent; warm start; active set; strong rule; LARS; equiangular vector; forward stagewise**: how the
  path is computed.
- **Elastic net; grouping effect; group lasso; fused lasso; total variation; adaptive lasso; oracle property; SCAD;
  MCP**: the penalty zoo.
- **One-SE rule; selection consistency; stability selection; selection probability**: choosing λ for prediction or
  selection.
- **Laplace prior; Bayesian lasso; horseshoe; shrinkage factor κ; spike-and-slab**: Bayesian sparsity.
- **Basis pursuit; null space property; restricted isometry property; phase transition; incoherence**: compressed
  sensing.
- **Winner's curse; naive post-selection inference; debiased lasso; nodewise regression; double selection; PoSI**:
  inference after selection.
- **Nuclear norm; singular value thresholding; SoftImpute; matrix completion**: sparsity of the spectrum.

## Where it comes back

| Idea | Returns in |
|---|---|
| thousands of tests after screening | 33 |
| conformal intervals around sparse fits | 34 |
| double machine learning | 36 |
| Fano bounds and s log(p/s); sparse PCA's barrier | 50 |
| concentration and the RIP for random matrices | 51 |
| oracle inequalities; support recovery; low-rank recovery | 52 |
| posterior contraction for sparse priors | 53 |
| selective inference and PoSI | 56 |
| AMP, state evolution and the phase transition | 59 |
| the Coverage Board | every part; 65 |
