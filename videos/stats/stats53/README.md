# Statistics, Built — Part 53: Bayesian Asymptotics and Nonparametric Bayes

Part 53 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eleventh part of Stage IV, the PhD core.

It opens with Diaconis and Freedman (1986). In a symmetric location problem, a reasonable prior (a smooth prior on the
centre and a symmetrized Dirichlet process with a Cauchy base on the shape) has a posterior that never settles at the
true centre. The part asks when a posterior finds the truth, how fast, and whether its credible sets are honest:
- Doob's theorem (1949), proved by martingales, and Freedman's warning;
- Schwartz's theorem (1965): KL support plus tests; Barron–Schervish–Wasserman sieves;
- contraction rates (Ghosal, Ghosh & van der Vaart 2000), exact in the Gaussian sequence model, and the contraction
  ball;
- Bernstein–von Mises from LAN, priors merging, growing dimension;
- its infinite-dimensional failures (Cox 1993; Freedman 1999), BvM for smooth functionals, and Castillo & Rousseau's
  semiparametric BvM;
- Dirichlet processes, the Chinese restaurant, DP mixtures on Old Faithful, Pólya trees, Pitman–Yor;
- Gaussian-process priors through the RKHS and small-ball probabilities;
- adaptation by empirical and hierarchical Bayes;
- polished tails and inconvenient truths (Szabó, van der Vaart & van Zanten 2015), on the Board;
- spike-and-slab and the horseshoe: rates, shrinkage, and coverage by signal size (Board);
- misspecification (Kleijn & van der Vaart 2012), tempered and Gibbs posteriors, SafeBayes (Board).

It keeps three promises:
- **Part 26** said the prior washes out as data accumulate. Chapters 1–5 say when it does, at what rate, and when it
  does not.
- **Part 47**'s LAN gives the Bernstein–von Mises theorem in chapter 4.
- **Part 50**'s minimax rates are attained by posteriors in chapters 3 and 7–10, and bind them from below.

**Built in this part:**
- **`statkit.bnp`** ([`explainer/stats/kit/bnp.py`](../../../explainer/stats/kit/bnp.py)), tested in
  `tests/test_stats_kit_bnp.py`:
  - the Gaussian sequence model with Gaussian priors: posterior, exact risk and spread, credible-ball coverage, exact
    coverage of credible intervals for linear functionals, the marginal likelihood and empirical Bayes;
  - Bernstein–von Mises: TV between a Beta posterior and its normal approximation;
  - misspecification: Poisson credible intervals for overdispersed counts and a calibrated tempered posterior;
  - the Dirichlet process: posterior CDF and Beta bands, the Pólya urn, stick-breaking, and a collapsed Gibbs sampler
    for DP mixtures of normals (Neal's Algorithm 3);
  - sparse normal means: the spike-and-slab posterior with a Beta-binomial weight, its intervals; the horseshoe's
    posterior by quadrature.
- **The contraction ball** (`ContractionBall` in `explainer/stats/viz.py`), the part's instrument: the truth, posterior
  draws and a credible disc in a two-dimensional window onto parameter space, drawn at a fixed scale so that panels for
  different n compare.

**Data.**
- From the Museum: Newcomb's passage times (1882) and Old Faithful's eruptions.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| EB credible ball, polished truth | sequence model, β = 1, n = 10⁴ | 95% | 84.7% | broken |
| EB credible ball, growing-gap blocked truth | sequence model, β = 1, n = 10⁴ | 95% | 97.0% | kept |
| EB credible ball inflated 1.5×, polished truth | sequence model, β = 1, n = 10⁴ | 95% | 100% | conservative |
| horseshoe interval, intermediate signals | sparse means, θᵢ = 2.5, n = 400 | 95% | 64% | broken |
| Poisson credible interval, overdispersed counts | NB, mean 8, var 40, n = 200 | 95% | 62.3% | broken |
| tempered (generalized) posterior interval | NB, mean 8, var 40, n = 200 | 95% | 94.6% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats53.compute   # once (a few minutes)
python tools/build.py stats53 -q l                         # fast 480p preview
python tools/build.py stats53                              # 1080p30 -> renders/stats53.mp4
python tools/qa_scene.py stats53 Bands
python tools/lecture_length.py stats53 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Diaconis and Freedman | the symmetrized DP location model |
| 1 | Doob | 24 truths from a uniform prior: mean error 0.008 after 3,000 flips; a three-point prior: the truth's posterior → 1 |
| 2 | Schwartz | N(0, 1) data, a Uniform[1, 3] prior: posterior mean 1.114 (n = 10), 1.010 (100), 1.001 (1,000) |
| 3 | Contraction rates | β = 1: fitted slopes −0.249 (α = ½; theory −¼), −0.328 (α = 1; −⅓), −0.218 (α = 2; −⅕) |
| 4 | Bernstein–von Mises | TV, p = 0.3: 0.084 (n = 10) → 0.0023 (10⁴); p = 0.02: 0.018 at 10⁴; Beta(1, 1) vs Beta(20, 2): 0.87 → 0.11 |
| 5 | Semiparametric BvM | n = 10⁴, β = 1: credible ball 100% for α ≤ 1, 76% at 1.25, ≈ 0 from 1.5; Σk⁻¹θₖ ≈ 95% to α = 2, 58% at 3; Σk^−0.6 θₖ 20% at 3 |
| 6 | Dirichlet processes | Newcomb, n = 66; tables at n = 1,000: 12 (α = 1), 27 (5), 89 (25); Old Faithful: 5.79 occupied clusters on average across three chains; cluster-count R-hat 1.006, ESS 236 |
| 7 | Gaussian processes | exponents fitted from exact risks match min(α, β)/(1 + 2α); peak 0.330 at α = 1 |
| 8 | Adaptation | α̂: 1.46 (n = 10²) → 1.09 (10⁶); actual selected-estimator risk / fixed-candidate oracle 1.233 ± 0.050 → 0.999 ± 0.007 (MCSE; 200 datasets) |
| 9 | Credible sets | finite K = 1,500: polished coverage 80–86%; growing-gap blocked truth 52% (n = 300), 92.7% (1,000), 96.7% (30,000); independent radius calibration, not a finite proof of the infinite-dimensional impossibility theorem |
| 10 | High-dimensional Bayes | coverage of 95% intervals by signal size 0, 1, 2.5, 6: spike-and-slab 100, 32, 67, 91%; horseshoe 100, 49, 64, 91% |
| 11 | Misspecification | Poisson width 0.78, coverage 62.3%; tempered (η ≈ 0.2) width 1.75, coverage 94.6% |
| 12 | Outro | — |

## Sources

- **Consistency.** J. Doob, *Colloq. Int. CNRS* 13 (1949); L. Schwartz, *Z. Wahrsch.* 4 (1965); D. Freedman, *Ann.
  Math. Stat.* 34 (1963); P. Diaconis & D. Freedman, *Ann. Stat.* 14 (1986); A. Barron, M. Schervish & L. Wasserman,
  *Ann. Stat.* 27 (1999).
- **Rates.** S. Ghosal, J. Ghosh & A. van der Vaart, *Ann. Stat.* 28 (2000); S. Ghosal & A. van der Vaart, *Ann. Stat.*
  29 (2001); W. Shen, S. Tokdar & S. Ghosal, *Biometrika* 100 (2013); A. van der Vaart & H. van Zanten, *Ann. Stat.* 36
  (2008), 37 (2009); B. Knapik, A. van der Vaart & H. van Zanten, *Ann. Stat.* 39 (2011).
- **Bernstein–von Mises.** L. Le Cam (1953, 1986); D. Cox, *Ann. Stat.* 21 (1993); D. Freedman, *Ann. Stat.* 27 (1999);
  S. Ghosal, *J. Multivar. Anal.* 74 (2000); D. Bontemps, *Ann. Stat.* 39 (2011); I. Castillo & R. Nickl, *Ann. Stat.* 41
  (2013), 42 (2014); I. Castillo & J. Rousseau, *Ann. Stat.* 43 (2015); V. Rivoirard & J. Rousseau, *Bayesian Anal.* 7
  (2012); K. Ray & A. van der Vaart, *Ann. Stat.* 48 (2020).
- **Nonparametric priors.** T. Ferguson, *Ann. Stat.* 1 (1973); D. Blackwell & J. MacQueen, *Ann. Stat.* 1 (1973);
  J. Sethuraman, *Stat. Sinica* 4 (1994); A. Lo, *Ann. Stat.* 12 (1984); R. Neal, *JCGS* 9 (2000); S. Ghosal, J. Ghosh &
  R. V. Ramamoorthi, *Ann. Stat.* 27 (1999); M. Lavine, *Ann. Stat.* 20 (1992); J. Pitman & M. Yor, *Ann. Probab.* 25
  (1997); J. Miller & M. Harrison, *JMLR* 15 (2014).
- **Adaptation and coverage.** B. Knapik, B. Szabó, A. van der Vaart & H. van Zanten, *PTRF* 164 (2016); B. Szabó,
  A. van der Vaart & H. van Zanten, *Ann. Stat.* 43 (2015); R. Nickl & S. van de Geer, *Ann. Stat.* 41 (2013).
- **Sparse priors.** E. George & R. McCulloch, *JASA* 88 (1993); I. Castillo, J. Schmidt-Hieber & A. van der Vaart, *Ann.
  Stat.* 43 (2015); C. Carvalho, N. Polson & J. Scott, *Biometrika* 97 (2010); S. van der Pas, B. Kleijn & A. van der
  Vaart, *EJS* 8 (2014); S. van der Pas, B. Szabó & A. van der Vaart, *Bayesian Anal.* 12 (2017); V. Ročková & E. George,
  *JASA* 109 (2014); A. Bhattacharya et al., *JASA* 110 (2015); K. Ray & B. Szabó, *JASA* 117 (2022).
- **Misspecification.** B. Kleijn & A. van der Vaart, *EJS* 6 (2012); U. Müller, *Econometrica* 81 (2013); P. Bissiri,
  C. Holmes & S. Walker, *JRSS B* 78 (2016); N. Syring & R. Martin, *Biometrika* 106 (2019); P. Grünwald & T. van Ommen,
  *Bayesian Anal.* 12 (2017).
- **Data.** S. Newcomb (1891); S. Stigler, *Ann. Stat.* 5 (1977); W. Härdle, *Smoothing Techniques* (1991).
- **Books.** S. Ghosal & A. van der Vaart, *Fundamentals of Nonparametric Bayesian Inference* (2017); J. K. Ghosh &
  R. V. Ramamoorthi, *Bayesian Nonparametrics* (2003); E. Giné & R. Nickl (2016), ch. 7; N. Hjort, C. Holmes,
  P. Müller & S. Walker (eds.), *Bayesian Nonparametrics* (2010).

## Problems and solutions

1. **Doob for a finite prior.**
   - Π(θ | X) ∝ π(θ) exp(Σᵢ log p_θ(Xᵢ)).
   - For θ ≠ θ₀, (1/n) Σ log(p_θ/p_θ₀)(Xᵢ) → −KL(θ₀, θ) < 0 almost surely, so each wrong θ's posterior weight relative to
     θ₀'s is π(θ)/π(θ₀) · e^{−n KL + o(n)} → 0.
   - With finitely many θ, Π(θ₀ | X) → 1.
2. **The boundary posterior.**
   - The posterior is N(x̄, 1/n) truncated to [1, 3]. Since x̄ → 0, almost all of the untruncated mass lies below 1.
   - The truncated normal piles up at 1, with mean 1 + O(1/(n|x̄ − 1|)) → 1: the KL projection of 0 onto [1, 3].
3. **The sequence model's risk.**
   - θ̂ₖ = wₖYₖ = wₖθₖ + wₖZₖ/√n, so θ̂ₖ − θₖ = −(1 − wₖ)θₖ + wₖZₖ/√n.
   - Squaring and taking expectations: (1 − wₖ)²θₖ² + wₖ²/n. Sum over k.
4. **The Beta posterior's moments.**
   - The mean (a + k)/(a + b + n) = p̂ + O(1/n).
   - The variance (a + k)(b + n − k)/((a + b + n)²(a + b + n + 1)) = p̂(1 − p̂)/n + O(1/n²).
5. **Dirichlet-process moments.**
   - F(A) ~ Beta(αG₀(A), α(1 − G₀(A))), from the partition {A, Aᶜ}.
   - So E F(A) = G₀(A), and Var F(A) = G₀(A)(1 − G₀(A))/(α + 1).
6. **The tempered posterior's variance.**
   - Gamma(a + ηΣy, b + ηn) has variance (a + ηΣy)/(b + ηn)² ≈ ȳ/(ηn).
   - With η = μ/σ², this is ≈ σ²/n, the variance of ȳ: the sandwich, since for the mean parameter μ, the Poisson score is y/μ − 1 with variance σ²/μ² and the expected negative Hessian is 1/μ. The resulting sandwich variance is σ²/n. A scalar temperature does not generally match a multivariate sandwich covariance.

## Glossary

- **Consistency.**
  - Posterior consistency; Doob's theorem; KL support; exponentially consistent tests; sieve; Hellinger distance: when
    the posterior finds the truth.
  - Contraction rate; prior mass condition; entropy condition; small-ball probability; RKHS; concentration function:
    how fast.
- **Shape.**
  - Bernstein–von Mises; LAN; total variation; merging of opinions: parametric.
  - Credible ball; linear functional; semiparametric BvM; efficient influence function; multiscale norm:
    nonparametric.
- **Priors.**
  - Dirichlet process; base measure; concentration; Chinese restaurant; stick-breaking; DP mixture; Pólya tree;
    Pitman–Yor: on distributions.
  - Gaussian process; Matérn; squared exponential; length scale: on functions.
  - Spike-and-slab; complexity prior; horseshoe; global-local; Dirichlet–Laplace: on sparse vectors.
- **Adaptation and honesty.**
  - Empirical Bayes; marginal likelihood; hierarchical Bayes; polished tail; inconvenient truth; inflation: adaptive
    credible sets.
  - Misspecification; KL projection; sandwich; tempered (fractional) posterior; Gibbs posterior; SafeBayes: wrong
    models.

## Where it comes back

- **Part 54**: PAC-Bayes bounds for Gibbs posteriors.
- **Part 56**: credible sets after selection.
- **Part 58**: anytime-valid tests from Bayesian mixtures.
- **Part 62**: Bayesian causal inference with propensity-score priors.
- **Part 64**: the calibration of Bayesian deep learning.

## QA reconciliation

All thirteen scenes, twelve computations, six solutions, common helpers, the nonparametric-Bayes toolkit and its six tests were read. Twenty-one checks pass: fifteen independent numerical cases plus six toolkit checks. All twelve inputs regenerated. Old Faithful's 272 eruption/waiting pairs match an independent R distribution exactly in order; all 66 Newcomb passage times match as a multiset.

The Gaussian example sin(k)/k^(β+1/2) is a boundary hyperrectangle-regular sequence, not a member of the Sobolev-β ellipsoid: its weighted squared coefficients have a divergent harmonic sum. It belongs to Sobolev orders below β. Gaussian prior paths likewise typically lie below the nominal Sobolev order α. Exact finite-coordinate posterior-mean risk, posterior spread and an infinite-dimensional contraction theorem are distinguished. The GP-rate illustration fits finite-coordinate risk slopes, rather than directly verifying a full posterior contraction theorem.

The old blocked truth at starts 4^j had bounded multiplicative gaps and could satisfy a polished-tail condition with a larger window. It cannot substantiate the claimed counterexample. The replacement is the truncation of an infinite sequence with starts N_j = 2^(j(j+1)), whose gap ratios grow without bound. A test verifies empty fixed-ratio windows followed by positive future energy. The finite K = 1,500 experiment is not itself a proof of asymptotic failure: at n = 10,000 its achieved coverage is 97.0%, whereas the regular oscillating truth's coverage is 84.7%. The point is to report the experiment accurately, not force undercoverage at a predetermined n. The same datasets and radii now underlie the regular truth's original and 1.5-times-inflated Board rows.

Credible-ball radii use independent 12,000-draw Gaussian reference samples across each candidate-α grid, replacing 800 extra radius draws inside every selected dataset. Exact binomial order statistics provide simultaneous 95% uncertainty bounds for the candidate reference quantiles. Those bounds are propagated to coverage ranges. Dataset Monte Carlo errors are reported conditional on the reference calibration; calibration uncertainty is separately retained. Balls concern the stated retained coordinates (K = 3,000 in the semiparametric plot, K = 1,500 on the EB Board). Exact Gaussian functional coverage is distinguished from simulated ball coverage. The projected two-coordinate picture uses an exact Gaussian ellipse, rather than an approximate isotropic disc; inclusion of the truth in one seeded picture is not a coverage theorem.

Empirical-Bayes risk is now the actual squared error of the estimator selected on the same dataset. Averaging a fixed-α risk formula after selecting α ignores selection dependence and is retained only as a separate frozen-α surrogate. An independent analytic Gaussian-tail calculation verifies the difference. Two hundred datasets per n replace twenty, with risk-ratio Monte Carlo errors displayed. Finite risk ratios slightly below one can arise from sampling error or data-dependent adaptation and are not claimed to violate a lower bound.

At zero or all binomial successes, the MLE normal approximation is a point mass and its TV distance from a continuous Beta posterior is exactly one. The local implementation handles this explicitly and uses standardized adaptive quadrature for interior counts, checked against independent dense integration. Rounded counts near np are not an average over repeated binomial samples. Classical BvM needs more than LAN and a positive prior: nonsingular interior information and global posterior localization are explicit. Coverage is pointwise for regular sets, rather than automatic uniform honesty for arbitrary credible sets. Growing dimension alone is not universal failure; known-variance Gaussian regression with a flat prior is conditionally exact Gaussian for full-rank p < n. Strong-norm infinite-dimensional failures do not preclude weak-norm or functional BvM theorems.

The Schwartz proof now controls the test-weighted likelihood numerator, not the raw integral whose expectation need not decay. The rate neighbourhood controls both KL and the second log-likelihood-ratio moment, with testable metrics, sieves, a growing nε² and the appropriate convergence mode. Doob's theorem states its measurable-space and identifiability conditions. Generic inconsistency claims are scoped to their model/prior/topology setting. Posterior inconsistency does not imply every point estimator is inconsistent: a symmetric pair of modes can have its mean at the true centre. Failure of KL support is failure of a sufficient condition, not proof of inconsistency in every topology; a direct DP posterior can be weakly consistent for a continuous truth.

Newcomb's normal base uses fitted median/MAD hyperparameters, so the Beta intervals are conditional pointwise empirical-Bayes intervals. They are neither simultaneous bands nor the exact zero-concentration Bayesian bootstrap. The CDF grid includes observations and their left limits, preserving ties and jumps. DP-mixture NIG base hyperparameters are also fitted from the data. Three independent 1,000-sweep chains retain 700 draws each; occupied-cluster means are 5.929, 5.607 and 5.826, with rank-normalized split R-hat about 1.006 and bulk ESS about 236. These scalar diagnostics do not certify all latent variables or density convergence. The cluster histogram retains every observed count. Density modes, occupied clusters and a true mixture-component count are different quantities.

The horseshoe uses a global scale equal to the known sparse proportion, an oracle simulation choice. Its Gaussian-mixture quadrature is transformed to a bounded integration domain without an arbitrary finite log-scale cutoff; independent adaptive integration verifies posterior means and both interval endpoints. Spike-and-slab mixture quantiles preserve the exact zero atom even when the slab lies far away, fixing a bracket failure outside the displayed regime. Dataset/group coverage fractions and empirical Monte Carlo errors account for the shared spike-and-slab mixing weight. The horseshoe evaluates forty of the zero coordinates rather than all 360; this is disclosed. The Board's intermediate row records sixty independent datasets, not six hundred falsely independent studies. The demonstrated fixed Gaussian slab and Beta mixing prior are distinguished from the slab/model-size conditions in uniform contraction theorems. A fixed Gaussian slab retains 10% shrinkage for arbitrarily large signals; s log(n/s) denotes a squared Euclidean radius.

Misspecified BvM states its interior KL-projection and regularity assumptions. In the scalar overdispersed-Poisson example, the mean/variance temperature estimates the leading sandwich spread, but the 4,000-dataset coverage experiment is not an exact guarantee. The Gamma prior has shape/rate .01/.01. Scalar tempering cannot generally reproduce an entire multivariate sandwich covariance. Loss-based median posteriors and bootstrap calibration still need distributional regularity; SafeBayes predictive tuning is not synonymous with interval calibration. Semiparametric causal prior alignment, hierarchical averaging, adaptive L2 balls and supremum bands retain their distinct conditions and scopes.

Thirty-seven persistent theorem headings and a heading above delayed GP panels prepare the visual pass. A log(1+density) display includes the narrow boundary posterior peak; GP bands share limits derived from their full endpoints; the relative marginal-likelihood window is declared. Local curves preserve crossings and missing breaks. English endpoint/native/motion and representative narrated visual review remain pending. Chinese narration/captions, continuous listening and final masters remain open.
