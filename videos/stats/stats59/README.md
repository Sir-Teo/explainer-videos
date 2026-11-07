# Statistics, Built — Part 59: High-Dimensional Asymptotics

Part 59 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fourth part of Stage V, the research frontier.

It opens with Sur & Candès (2019). In a logistic regression with one variable for every five observations and signal
strength γ² = Var(x′β) = 5, the Gaussian-model MLE has limiting inflation factor α⋆ = 1.499. Its spread is σ⋆ = 4.74
against the textbook's 3.88, and twice the log likelihood ratio for a null coefficient is 1.487 χ²₁, not χ²₁. The part
asks what happens to classical statistics when p and n grow together, and derives exact limiting formulas under stated assumptions:
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
  - the logistic proximal map, and the Sur–Candès system in (α, σ, λ) by root finding with 161 × 161 Gauss–Hermite
    quadrature (it reproduces the paper's κ = 0.1 and κ = 0.2 values to four digits), the global-null system, and the
    MLE's existence boundary;
  - the logistic MLE by damped Newton and the LRT for one coefficient;
  - the Marchenko–Pastur Stieltjes transform and density, exact ridge bias, variance and risk, the optimal penalty, the
    ridgeless risk, and a ridge/ridgeless simulator;
  - AMP for the lasso, its state evolution, the minimax-threshold Donoho–Tanner curve (identical to Part 32's), the
    lasso's best-threshold MSE;
  - the posterior-mean scalar denoiser and MMSE for a three-point prior, and Bayes-optimal state evolution;
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
| 1 | The proportional regime | OLS: σ²κ/(1 − κ); MP at κ = 0.5: eigenvalues 0.088–2.87 (edges 0.086, 2.91); γ² = 5: α⋆ 1.073, 1.168, 1.299, 1.499, 1.871 and factor 1.073, 1.166, 1.294, 1.487, 1.840 at κ = 0.05–0.25; at 0.3, α⋆ = 3.074 and LRT factor 2.952; the old solver failure did not imply nonexistence; the MLE exists for κ < 0.500 (γ = 0), 0.32559 (γ² = 5); global null κ = 0.2: factor 1.268, χ² size ≈ 8% |
| 2 | Random matrices | MP moments at κ = ½: mean 1, SD 0.71, mean inverse 2, top edge 2.91; Wigner (N = 1,500, s² = ¼) plus ±1 diagonal against the free convolution |
| 3 | Ridge | γ = ½, r²/σ² = 4: λ⋆ = 0.125, risk 0.702 (theory = simulation at n = 400); γ = 2: optimal risk 2.56; ridgeless: 1 (γ = ½), 9 (0.9), 3 (2), 3.33 (4); simulated 0.99, 9.99, 2.97, 3.33 |
| 4 | M-estimation | Laplace errors, n = 400: κ = 0.1 LAD 0.085 vs OLS 0.102; κ = 0.5 LAD 1.15 vs OLS 1.03 |
| 5 | AMP | n = 1,000, p = 2,000, ε = 0.1, σ² = 0.01, θ = 1.5: τ²₁ 0.129 (SE 0.131), τ²₃ 0.079 (0.079); MSE after 25 iterations 0.019 |
| 6 | Gordon | least squares from the auxiliary problem: a² = σ²κ/(1 − κ) |
| 7 | Replicas | three-point prior ε=.1, noise 1e−4: uninformative Bayes-denoising AMP first has MSE<.001 at sampled δ=.30; not the computed global replica MMSE. Noiseless lasso boundary δ=.32879; positive-noise lasso still has error |
| 8 | Random features | normalized paired/nested ReLU experiment, n=300,d=30: six-run ridgeless mean peak 480.8 (empirical SE 287.0), final mean 0.2635; λ=.001 final 0.0308; risk excludes test noise, target variance 1/30 |
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
   p + zpm = n(1 − 1/(1 + κm)). Rearranged, κzm² − (1 − κ − z)m + 1 = 0.
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

## QA reconciliation

Detailed [scientific source review](../../../docs/qa/evidence/stats59-polish-20261107/source-review.md):

All twelve English scenes, computation paths and legacy AMP helpers were reviewed. Twenty-three checks pass (19 local parameterized checks and four legacy tests). All twelve cached inputs were regenerated. Scientific source is reconciled; the recorded sampled visual checkpoint is complete; bilingual production approval remains open.

The logistic table incorrectly equated a failed numerical root with a nonexistent MLE. At kappa=.3, gamma^2=5, the corrected bracketed proximal map and bounded positive least-squares solve find alpha=3.07379, sigma=11.63229, lambda=13.74917 and LRT factor=2.95240. Independently integrating the existence objective gives boundary .32558861, so .3 is inside the asymptotic existence region. The gamma=0 boundary is exactly .5 instead of the former noisy .501 Monte Carlo estimate. Integrating the independent Z analytically leaves a smooth one-dimensional Gaussian integral. Root status and phase status are distinct. Increasing quadrature from 161 to 241 nodes changes the .3 LRT factor by about 1.24e-5; values at .1 match the published 1.1678, 3.3466 and .9605. Tests independently bracket logistic proximal roots through lambda=10000. Central-bracket safeguarding prevents the old unguarded Newton cycle for larger scales.

A linear program now checks complete or quasi separation before declaring a finite no-intercept logistic MLE. It maximizes total signed margin under nonnegative individual margins and bounded coefficients: a nonzero objective identifies a separating direction. Newton convergence additionally checks gradient and decrement rather than merely a small change in likelihood. Restricted likelihood fits reuse the full model's finite-existence check; a materially negative LRT raises. Independent likelihood optimization and explicit complete/quasi-separated examples test these cases. The 500 Gaussian LRT fits and 200 biopsy fits all have finite converged solutions in this run; attempts and failures are recorded rather than silently dropping them.

The logistic inflation factor is a limiting bias/centering result in the stated Gaussian example, not a claim that every realized coefficient overestimates its truth. Classical MLE unbiasedness is asymptotic under regularity, not exact finite-sample unbiasedness. The p/n failure argument uses nonvanishing total squared error, rather than a universal p/sqrt(n) Taylor remainder formula. The oracle gamma in these experiments is explicitly known; feasible ProbeFrontier/SLOE procedures are described rather than claimed implemented. SLOE estimates corrupted predictor variance from leave-one-out predictions. For our X_ij~N(0,1/n) scaling, sigma is the coordinate noise scale. In correlated Gaussian coordinates, tau_j=SD(sqrt(n)X_j | sqrt(n)X_-j); the debiased noise is sigma/(alpha tau_j). Dividing the center and noise by alpha means the corrected interval need not be wider than the textbook interval. A joint chi-squared correction is for a fixed number of null coordinates.

LRT size is .086 (empirical MCSE .01254) classically and .038 (.00855) after oracle rescaling. These are finite simulations, not exact .05 size. Board rows use empirical Monte Carlo errors. The arbitrary-covariance Gaussian extension is cited; general non-Gaussian dependence is not justified by matching two moments or a single semi-synthetic exercise. All 17070 biopsy feature values and all 569 diagnoses independently match UCI again. Held-out predictor slopes average 1.63848 (MCSE .03990), median 1.52999, with 10%--90% range 1.09383--2.24715. These fixed-design subsampling results do not establish confidence coverage or universality. Histogram out-of-range mass and failed fits are reported rather than folded into edge bins.

The MP derivation now removes one independent row outer-product from the p-by-p covariance. Its scaled quadratic form concentrates near kappa*m, not m. The trace identity 1+zm=m/(1+kappa m) gives the displayed quadratic. The inverse moment 1/(1-kappa) is for kappa<1; ratios above one have a zero atom. Stieltjes inversion at positive eta gives a Cauchy-smoothed density and requires separate accounting for atoms. Largest-eigenvalue and moment statements refer to the isotropic limiting model, not every finite sample covariance.

The red free-convolution comparison now uses the ordinary convolution of the actual semicircle and +/-1 spectral laws. The old Gaussian blur was not their ordinary spectral convolution. A cubic equation solves the deformed-Wigner Stieltjes transform, selecting its unique upper-half-plane root and checking the original Pastur equation residual. Independent mass/mean/second-moment checks recover 1,0,1.25 to the stated smoothing precision. Eta and maximum residual are retained. Finite eigenvalue histograms fluctuate, and a smoothed limiting density is not an exact finite-data fit.

Ridge risk uses the analytic derivative of the MP equation rather than finite differences susceptible to cancellation. For lambda>0, a=1-gamma+lambda, D=sqrt(a^2+4 gamma lambda), m' = m(gamma*m+1)/D, and m-lambda*m'=(1-lambda*m)/D. Independent continuous spectral quadrature, including the atom when gamma>1, checks squared bias and variance. Simulations retain per-replicate risks and Monte Carlo errors. The green optimal-ridge risk rises smoothly with dimension; the old narration said it never rises even though its plotted values did. Removing the interpolation spike is not a monotonic decrease. For r^2=4 and sigma^2=1, ridgeless risk beyond gamma=1 falls to 3 at gamma=2 and then rises toward 4. Divergence at the square threshold assumes positive observation noise. These are limiting excess prediction risks, excluding irreducible test noise, not exact finite-sample risks. Ridge penalty optimality is within this isotropic ridge family. Fixed-fold validation changes the training aspect ratio; LOOCV/GCV consistency is stated with assumptions.

The Laplace OLS/LAD experiment retains twelve independent draw-level errors and Monte Carlo errors at each ratio. The grey finite-n OLS expectation is p/(n-p-1), not exactly kappa/(1-kappa). The scalar M-estimation system needs the Gaussian design and loss/error hypotheses; it is not universal for every estimator. Effective held-out noise is epsilon+rZ, while in-sample fitted residuals also undergo the proximal transformation. The Laplace efficiency reversal does not establish that squared loss is optimal for every error distribution at all large ratios. LAD linear-program success and feasibility are checked.

Soft-threshold scalar MSE uses analytic truncated-normal moments. The former 81-node Gaussian quadrature sampled a nonsmooth threshold poorly. Piecewise adaptive integration independently checks four noise/threshold scales; the reference subdivides near zero as well as the kinks to avoid missing the normal mass on very distant integration intervals. State evolution uses the corrected moments. Bayes posterior means use log-sum-exp weights, preventing 0/0 for tiny noise or distant observations. Independent posterior-variance identities check scalar MMSE. Adaptive integration partitions posterior transition regions. Tiny positive MMSE can fall below double-precision range; displayed numerical zero is not exact recovery.

The lasso curve selects the best converged positive-penalty fixed point on the stated threshold grid. Candidates below the positive-penalty AMP threshold domain, unconverged recursions and nonpositive calibrated penalties are excluded. A separate independent coordinate-descent lasso agrees with converged AMP at lambda=theta*tau*(1-active/delta). The Donoho-Tanner sparsity crossing is solved by a bracketed root, delta=.32879351, rather than a coarse inverse interpolation. With positive measurement noise the blue curve does not recover exactly at that noiseless boundary. The gold curve is uninformative-initialized posterior-mean AMP, not a globally minimized replica potential or an automatically Bayes-optimal estimator. It first falls below MSE .001 on the displayed delta=.30 grid. The text distinguishes that algorithmic criterion, noise and grid resolution from information-theoretic MMSE and exact recovery. Prior mass .9 is eighteen times each signed .05 component, not nine.

AMP state evolution is an empirical proportional-limit theorem at every fixed iteration under design, denoiser and moment conditions. It does not require convergence for fixed-iteration prediction; identifying an estimator needs further convergence and limit arguments. Pseudo-observations are not literally independent Gaussian coordinates in a finite matrix. The lasso fixed-point correspondence requires the calibrated positive penalty. Two dense products here take about four million multiply-accumulate pairs/eight million elementary floating-point operations, rather than two million total operations. Fragility is related to design structure/conditioning; non-Gaussian entries alone need not cause divergence.

CGMT requires its admissible compact sets and continuity, convexity for the two-sided optimal-value conclusion, and a growth or restricted-value gap to transfer minimizer properties. Arbitrary auxiliary minimizer properties do not transfer automatically. Noncompact problems require localization. The ridge objective's 1/n normalization now matches its penalty elsewhere. Replica formulas and rigorous proofs are scoped to their models, rather than a guarantee for all nonconvex inference.

The random-feature experiment normalizes features by 1/sqrt(N), keeping a fixed ridge penalty consistent with a kernel limit. Penalties are paired on the same datasets and use nested feature draws across N, replacing independent unpaired simulations. It records six replicate error curves and empirical errors. Target variance is 1/d=1/30, noise variance .25; reported risk compares to the noiseless target and excludes irreducible test noise. The ridgeless mean peak is about 480.80 with empirical SE 286.98 across only six runs: the plot and narration acknowledge its instability near interpolation, rather than treating it as a precisely known risk. At 2500 features mean ridgeless/regularized risk is .26349/.03078 in this experiment.

Gaussian equivalence matches certain limiting spectral/risk quantities under activation/input/weight/target assumptions; it is not a distributional identity for each nonlinear feature. The primary random-feature theorem uses spherical inputs/weights, while our finite Gaussian-input simulation is an illustration without its theorem curve overlaid. More features with regularization need not always improve risk. Degree-versus-sample-size kernel staircases are model-dependent asymptotic transitions; the old statement that all quadratic targets are impossible at n=300,d=30 was too strong, particularly for low-rank targets. Open-problem statements acknowledge existing covariance, feature-learning, conformal and selective-inference results.

Persistent result headings and local segment clipping preserve genuine viewport crossings and missing breaks. Scatter values are not clamped. Ridge and RF plots include all observed/theoretical vertical values instead of flattening peaks at plot edges. The empirical biopsy histogram explicitly discloses values outside its plotted range.

The narration estimate is about 55 minutes. The recorded English sampled visual checkpoint is complete. Chinese narration/captions, continuous listening/full narrated playback and final bilingual masters remain open.
