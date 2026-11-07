# Statistics, Built — Part 21: Optimization for Statistics

Part 21 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first part of Stage III, Master's. Almost every estimator in the course is
the solution of an optimization problem. This part is about how those problems are solved, how fast, and what their
shape says about the estimator.

It opens with George Dantzig, who in 1939 copied two open problems from Neyman's blackboard as homework and solved
them. Both formed his 1946 doctoral thesis; one became the Dantzig–Wald generalized Neyman–Pearson lemma, whose mathematics is linear-programming duality.
In 1947 Dantzig invented the simplex method. The World's bakery is a two-variable LP: the simplex walks
(0, 0) → (0, 7) → (4, 5), for profits 0 → 28 → 32, with shadow prices of 1, 0 and 2. Stigler's 1945 diet problem was
solved by Laderman in 1947 at $39.69 a year.

From there the part covers:
- **Convexity.** Definitions; chords and tangents; Jensen and KL ≥ 0. A concave logistic likelihood beside a Cauchy
  likelihood with two peaks (−1.28 and 4.0). The log-partition function is convex, so exponential families have
  concave likelihoods. Condition numbers set gradient descent's linear rate: κ = 10 gives about 22 steps per factor-ten reduction of a standard objective-gap bound,
  κ = 10⁴ about 23,000, under the stated smoothness, strong-convexity and step assumptions.
- **Lagrange and KKT.**
  - The multinomial MLE derived with a multiplier.
  - A binomial MLE under p ≤ ½: with 30/50 the constraint binds, multiplier 20; with 20/50 the multiplier is 0
    (complementary slackness).
  - The four KKT conditions; the lasso's subgradient conditions.
  - Isotonic regression of the World's vote on income by PAVA: 8 dips in 25 bins pooled into 12 blocks.
- **Duality.**
  - Weak and strong duality; the bakery's dual (14 + 0 + 18 = 32).
  - The Neyman–Pearson lemma as an LP on a binomial(20), 0.5 vs 0.7, at α = 0.05: reject at 15+, randomize 0.79 at
    14, power 0.568. The multiplier k = 5.18 is the likelihood ratio at 14.
  - Ridge's dual and kernels.
  - The lasso's duality gap as a stopping certificate: ten orders of magnitude in 120 coordinate updates.
- **Linear programming.**
  - A modern unconstrained LAD fit to Boscovich's five meridian arcs (1757), distinct from his historical
    fit with zero-sum signed errors: the LAD line passes through Quito and Lapland (slope 800, against 725 for
    least squares; absolute error 327 against 349).
  - LAD as an LP; Klee–Minty and Karmarkar.
  - The check function and quantile regression (Koenker & Bassett 1978). On Engel's 235 households the slopes run from
    0.40 (τ = 0.1) to 0.69 (τ = 0.9), and the lines fan out.
- **Newton and Fisher scoring.**
  - Logistic regression of the World's vote on uncentred log income, drawn on the likelihood's contours: Newton reaches
    the top in 5 steps (errors 4.1, 0.45, 0.012, 8.7 × 10⁻⁶, 4.5 × 10⁻¹²); gradient ascent is still 0.58 away after 400.
  - Plain Newton on the Cauchy likelihood converges to a minimum (0.76); with a line search it reaches the peak (3.99).
  - Gauss–Newton and Levenberg–Marquardt; remedies.
- **MM algorithms.** Exact touching surrogates give descent; convergence and rates require further conditions.
  - The descent property; the median by quadratic majorizers (9 → 7.09 → 6.86 → …).
  - EM (including the current-posterior entropy term), IRLS, Weiszfeld and SMACOF as MM.
  - Smoothed median-regression MM on Engel against the LP optimum; original check-loss monotonicity here is observed, not a general smoothing guarantee.
  - Bradley–Terry strengths for a toy season by Zermelo's iteration (Hunter 2004): 2.92, 1.10, 0.71, 0.44, with
    P(Harbour beats Quarry) = 0.87.
- **Coordinate descent.**
  - The soft-threshold update; a two-predictor lasso staircase on the objective's contours.
  - Sweeps to convergence grow from 5 to 635 as the correlation rises from 0 to 0.99.
  - glmnet's tricks; a non-separable penalty on which coordinate descent is stuck.
- **Proximal methods.** Proximal operators, with soft and hard thresholding. ISTA vs FISTA on a 40-predictor lasso
  with condition number 4,745: errors 10⁻¹·⁷ vs 10⁻⁴·⁸ after 400 steps, under their 1/k and 1/k² bounds. Nesterov's
  optimal worst-case order for the general smooth convex first-order oracle class, with bounded initial distance.
  The displayed optimum is a high-accuracy numerical reference; the hard-threshold map shows its jumps and set-valued ties.
- **ADMM.**
  - Splitting; the fused lasso on a four-level signal (λ = 0.5, 3, 20); both primal and dual residuals. A local banded solver factors the tridiagonal system once, with linear work per update.
  - Two-block convex ADMM needs regularity and a saddle point; distributed coefficient sharing alone is not a privacy guarantee.
- **Stochastic gradient.**
  - Robbins–Monro for a median (10.0 from a start of 0).
  - SGD's last iterate against the Polyak–Ruppert average for the World's vote, 20,000 adults.
  - A finite step-exponent study: the average is closest to the MLE near γ = ½, at 0.29 model-based SE.
    The endpoint γ = ½ is outside the classic square-summable-step condition; this finite experiment is not an efficiency theorem.
  - Minibatches, momentum, Adam, SVRG and SAGA, distinguishing velocity, adaptive scaling and variance reduction.
  - Two Board rows.
- **Optimization and inference.**
  - The observed information gives SE 0.183, against a bootstrap's 0.196.
  - A genuine profile likelihood over the intercept, its quadratic at the joint MLE and a marginal slope Wald interval.
  - Optimization error against statistical error: compare with SE/10, here first crossed after 1,013 iterations (Bottou & Bousquet).
    Deterministic algorithm error can bias an estimate; it cannot automatically be added in quadrature to sampling variance.
  - A sandwich preview: 0.0508 vs 0.0513, against a 400-replicate Monte Carlo SD of 0.0497. IID asymptotics and model assumptions are explicit.
  - Warnings read from the landscape.

Every number on screen is computed in [`compute.py`](compute.py):
- Boscovich's arcs and Engel's households are the Museum's;
- the vote is the World's survey block;
- the rest are seeded simulations or worked examples.

**Built in this part:**
- **`statkit.optim`** ([`explainer/stats/kit/optim.py`](../../../../explainer/stats/kit/optim.py)), checked in
  `tests/test_stats_kit_optim.py`:
  - Newton with backtracking, and the Cauchy location likelihood;
  - Fisher scoring for logistic regression;
  - the check loss, Hunter–Lange MM and the LP for quantile regression;
  - a dense simplex method that records its vertex path;
  - the Neyman–Pearson LP;
  - soft thresholding, ISTA/FISTA, coordinate descent and the duality gap for the lasso;
  - ADMM for the lasso and the fused lasso (this part uses a local banded TV solver recording both residuals);
  - SGD with Polyak–Ruppert averaging and Robbins–Monro;
  - PAVA and Bradley–Terry MM.
- **The landscape** (`Landscape` and `marching_squares` in `explainer/stats/viz.py`): level sets of any function or
  grid of two parameters, and optimizer paths across them.
- **The Museum**: Boscovich's arcs (`BOSCOVICH`) and Engel's households (`engel()`).

The Coverage Board gains two rows: 95% model-based Wald intervals after one pass of SGD.
The target is the logistic projection in the entire finite adult World (slope 0.5712857),
computed from the census score equation. Income-only logistic specification is imperfect;
its model-based curvature intervals need not have exactly 95% coverage even after accurate optimization.

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| SGD last iterate, Wald CI | logistic slope, the World's vote, n = 2,000 | 500 | 81.6% | broken |
| Polyak–Ruppert average, Wald CI | logistic slope, the World's vote, n = 2,000 | 500 | 93.0% | kept |

## Build it

```bash
python -m videos.stats.stats21.compute         # once (under a minute; cached in .cache/stats21)
python tools/build.py stats21 -q l             # fast 480p preview
python tools/build.py stats21                  # 1080p30 -> renders/stats21.mp4
python tools/qa_scene.py stats21 Newton
python tools/lecture_length.py stats21 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Dantzig's homework, 1939 | bakery 0 → 28 → 32, shadow prices 1 / 0 / 2; Stigler $39.93, optimum $39.69 |
| 1 | Convex sets and functions | Cauchy peaks −1.28, 4.0; κ = 10: 22 steps per digit |
| 2 | Lagrange and KKT | multipliers 20 and 0; PAVA: 8 dips, 12 blocks |
| 3 | Duality | 14 + 18 = 32; NP: power 0.568, φ(14) = 0.79, k = 5.18; gap 10⁻¹⁰ after 120 updates |
| 4 | Linear programming | Boscovich: LAD slope 800 vs 725, errors 327 vs 349; Engel slopes 0.40–0.69 |
| 5 | Newton and Fisher scoring | errors 4.1 → 0.45 → 0.012 → 8.7e−6 → 4.5e−12; gradient 0.58 after 400; Cauchy 0.76 vs 3.99 |
| 6 | MM algorithms | median 9 → 7.09 → 6.86 → 6.76; Bradley–Terry 2.92 / 1.10 / 0.71 / 0.44 |
| 7 | Coordinate descent | correlation 0.84; final (1.25, 0.10); sweeps 5 → 635 |
| 8 | Proximal methods | κ = 4,745; ISTA 0.0196, FISTA 1.5e−5 after 400 |
| 9 | ADMM | λ = 0.5, 3, 20; residual 10⁻²·⁸ after 400 |
| 10 | Stochastic gradient | Robbins–Monro 9.98; MLE 0.579 (SE 0.016); Board 81.6% / 93.0% |
| 11 | Optimization and inference | SE 0.183 vs bootstrap 0.196; 1,013 iterations to SE/10; sandwich 0.0513 |
| 12 | Outro | — |

## Sources

- **History.**
  - G. Dantzig, *Ann. Math. Stat.* 11 (1940); G. Dantzig & A. Wald, *Ann. Math. Stat.* 22 (1951).
  - G. Dantzig, "Linear programming", in *Activity Analysis of Production and Allocation* (1951).
  - G. Stigler, *J. Farm Economics* 27 (1945).
  - R. Boscovich (1757), as tabulated by S. Stigler, *The History of Statistics* (1986).
  - E. Zermelo, *Math. Zeitschrift* 29 (1929).
- **Methods.**
  - W. Karush (1939); H. Kuhn & A. Tucker (1951).
  - R. Koenker & G. Bassett, *Econometrica* 46 (1978); S. Portnoy & R. Koenker, *Stat. Sci.* 12 (1997).
  - V. Klee & G. Minty (1972); N. Karmarkar (1984).
  - D. Hunter & K. Lange, *JCGS* 9 (2000); D. Hunter, *Ann. Stat.* 32 (2004).
  - P. Tseng, *JOTA* 109 (2001); J. Friedman, T. Hastie & R. Tibshirani, *J. Stat. Software* 33 (2010).
  - A. Beck & M. Teboulle, *SIAM J. Imaging Sci.* 2 (2009); Y. Nesterov (1983).
  - S. Boyd, N. Parikh, E. Chu, B. Peleato & J. Eckstein, *Found. Trends ML* 3 (2011).
  - H. Robbins & S. Monro, *Ann. Math. Stat.* 22 (1951); D. Ruppert (1988); B. Polyak & A. Juditsky, *SIAM J. Control
    Optim.* 30 (1992).
  - L. Bottou & O. Bousquet, *NIPS* (2008); D. Kingma & J. Ba (2014).
- **Books.**
  - S. Boyd & L. Vandenberghe, *Convex Optimization* (2004).
  - K. Lange, *Optimization* (2nd ed., 2013) and *MM Optimization Algorithms* (2016).
  - J. Nocedal & S. Wright, *Numerical Optimization* (2nd ed., 2006).
  - R. Koenker, *Quantile Regression* (2005).

## Problems and solutions

**1. Logistic concavity.**

*Solution.* ℓ(β) = Σ[yᵢxᵢ'β − log(1 + e^{xᵢ'β})], so ∇ℓ = Σ(yᵢ − pᵢ)xᵢ and ∇²ℓ = −Σpᵢ(1 − pᵢ)xᵢxᵢ' = −X'WX. For
any v, v'X'WXv = Σ pᵢ(1 − pᵢ)(xᵢ'v)² ≥ 0, so the Hessian is negative semidefinite and ℓ is concave. It is strictly
concave if X has full column rank.

**2. Maximum entropy.**

*Solution.* The Lagrangian is −Σp log p − α(Σp − 1) − λ(Σkp − μ). Setting ∂/∂p_k = −log p_k − 1 − α − λk = 0 gives
p_k = e^{−1−α}e^{−λk} ∝ e^{−λk}, with α and λ fixed by the two constraints. This is an exponential family with
sufficient statistic k when a normalizable interior solution exists. On a finite support an interior feasible
mean gives this form; boundary constraints can force zeros or degenerate support with no finite multiplier.
On infinite support, feasibility, existence and a finite normalizing constant must also be checked.

**3. The bakery's dual.**

*Solution.* min 14y₁ + 24y₂ + 9y₃ subject to y₁ + 3y₂ + y₃ ≥ 3, 2y₁ + 2y₂ + y₃ ≥ 4, y ≥ 0.
- **Feasibility of y = (1, 0, 2).** 1 + 0 + 2 = 3 ≥ 3 and 2 + 0 + 2 = 4 ≥ 4.
- **Optimality.** Its value is 14 + 18 = 32, the primal value, so by weak duality both are optimal.
- **Complementary slackness.** The oven constraint is slack at x = (4, 5) (3·4 + 2·5 = 22 < 24), and y₂ = 0.

**4. Newton for an exponential rate.**

*Solution.* ℓ(λ) = n log λ − λS, so ℓ' = n/λ − S and ℓ'' = −n/λ². Newton gives λ₁ = λ₀ − ℓ'/ℓ'' = 2λ₀ − λ₀²x̄.
With λ̂ = 1/x̄, λ₁ − λ̂ = −x̄(λ₀ − λ̂)²: the error is squared at each step (quadratic convergence). λ₁ < 0 when
λ₀ > 2/x̄ = 2λ̂: a start more than twice the answer jumps to an impossible rate.

**5. The proximal operator of λ|x|.**

*Solution.* Minimize λ|x| + (x − v)²/2.
- **For x > 0.** The derivative λ + x − v vanishes at x = v − λ, which is valid if v > λ.
- **For x < 0.** Symmetrically, x = v + λ if v < −λ.
- **Otherwise.** The minimum is at the kink, x = 0, since 0 ∈ λ[−1, 1] − v exactly when |v| ≤ λ.

Together: x = sign(v)(|v| − λ)₊.

**6. Robbins–Monro step size.**

*Solution.* Near θ*, M(θ) ≈ f(θ*)(θ − θ*), so the recursion behaves like e_{k+1} ≈ (1 − a f/k)e_k + noise/k.
- **The noise term.** It contributes variance of order Σ a²/j² × Π(1 − af/i)², which is O(1/k) only if af > 1/2.
  At af = 1/2 the variance is O(log k / k); for 0 < af < 1/2 it is O(k^{−2af}),
  with a comparable initial-error contribution, slower than the usual 1/k variance.
- **For N(10, 3²).** f(10) = 1/(3√(2π)) ≈ 0.133, so a > 1/(2 × 0.133) ≈ 3.76; our a = 10 qualifies.
- **Optimal choice.** a = 1/f(θ*) gives the optimal asymptotic variance, τ(1 − τ)/f² per observation.

## Glossary

- **Convex set and function; strong convexity**: segments stay inside; chords lie above; curvature bounded below by
  m > 0.
- **Condition number κ**: L/m, the ratio of largest to smallest curvature; it sets first-order methods' rates.
- **Jensen's inequality**: f(EX) ≤ Ef(X) for convex f.
- **Lagrangian; multiplier**: the objective plus priced constraints; the price, a shadow price or sensitivity.
- **KKT conditions**: stationarity, primal and dual feasibility, complementary slackness.
- **Subgradient**: a slope that supports a non-differentiable convex function (for |x| at 0, anything in [−1, 1]).
- **Dual problem; weak and strong duality; duality gap**: the problem over prices; its value bounds the primal's;
  equality at the optimum; primal minus dual.
- **Linear program; simplex method; interior-point method**: linear objective and constraints; walking vertices;
  crossing the interior.
- **Least absolute deviations; check loss; quantile regression**: Σ|r|; ρ_τ; minimizing Σρ_τ over regression lines.
- **Newton's method; Fisher scoring; IRLS; Gauss–Newton**: quadratic models of the objective with the Hessian, the
  expected information, weighted least squares steps, or J'J.
- **Line search; trust region; quasi-Newton (BFGS)**: safeguards and Hessian approximations.
- **MM algorithm; majorizer; descent property**: minimize a surrogate that lies above and touches; never increase.
- **Coordinate descent; warm start; active set**: one variable at a time; solving along a λ path; cycling over
  non-zeros.
- **Proximal operator; ISTA; FISTA; Nesterov acceleration**: penalized nearest point; gradient step plus prox; with
  momentum and an O(1/k²) worst-case objective-gap bound under convex smooth/composite assumptions.
- **ADMM; consensus**: alternating updates of split variables with a running dual; parallel copies forced to agree.
- **Stochastic gradient; Robbins–Monro; Polyak–Ruppert averaging**: one-observation steps; steps with Σa = ∞,
  Σa² < ∞; averaging iterates for asymptotic efficiency under stability, moment and regularity conditions (typically 1/2 < γ < 1).
- **Observed information; sandwich**: −∇²ℓ at the optimum; A⁻¹BA⁻¹ when the model may be wrong.
- **Isotonic regression; PAVA**: least squares under an order constraint; pooling adjacent violators.
- **Bradley–Terry model**: P(i beats j) = gᵢ/(gᵢ + gⱼ).

## Where it comes back

| Idea | Returns in |
|---|---|
| EM; the likelihood in depth; the sandwich | 22 |
| IRLS for every GLM | 24 |
| mixed models: optimizing over variance components | 25 |
| Bayesian computation | 27 |
| the lasso's theory | 32 |
| empirical risk minimization | 54 |
| optimal transport as an LP | 61 |
| training neural networks | 64 |
| the Coverage Board | every part; 65 |

## QA status

Scientific corrections and independent numerical checks are recorded in
[the review evidence](../../../../docs/qa/evidence/stats21-polish-20261107/scientific-review.md).
English visual verification follows. Continuous listening, Chinese narration/captions and final bilingual masters remain open.
