# Statistics, Built — Part 22: Likelihood in Depth

Part 22 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the second part of Stage III, Master's. Part 9 introduced maximum likelihood
and made two promises: the estimator is consistent, and approximately normal with variance 1/(nI). This part proves
both, says exactly what they need, and shows what happens when each condition fails: when the parameters multiply,
when the likelihood has no maximum, when the truth sits on an edge, and when the model is simply wrong.

It opens in Naples in 1893. Walter Frank Raphael Weldon measured the forehead breadth of 1,000 shore crabs, found the histogram
lopsided, and asked Karl Pearson whether it was two normal curves added together. Pearson matched five moments and
solved a ninth-degree polynomial by hand. Our multistart numerical search finds two admissible moment solutions, A
(p = 0.533) and B (p = 0.424). B's sixth moment, 7.76 × 10⁻¹⁰, is closer to the data's 7.45, so B is the one
Pearson's rule would keep. An interior local EM fit to a midpoint-density approximation puts 43% of the crabs at 0.6317 (SD 0.0183) and 57% at
0.6546 (SD 0.0126). The unrestricted exact-value mixture likelihood has no global maximum; the grouped interval-probability
likelihood is a different, bounded problem. This local fit's log likelihood is 2567.58, against 2567.49 for moments B and 2540.97 for a single normal.

From there the part covers:
- **Consistency** (Wald 1949).
  - The average log likelihood converges to M(θ) = E log f(X; θ), and M(θ₀) − M(θ) is a KL divergence, so θ₀ is
    M's unique peak.
  - Average log-likelihood curves for one growing stream of Poisson counts at Bortkiewicz's rate 0.61 peak at
    1.1, 0.68, 0.638 and 0.6103 for n = 10, 100, 1,000 and 10,000.
  - Uniform convergence plus a well-separated peak gives consistency.
- **Asymptotic normality.**
  - Expand the score: the CLT for the numerator, the LLN for the denominator, Slutsky.
  - For the Cauchy (no mean, no variance), 4,000 samples of 50: the MLE's SD is 0.208 against a theory of 0.200; the
    median's is 0.229 against 0.222.
  - The variance ratio is 1.22. Cramér–Rao, and Hodges's fine print.
- **Observed vs expected information** (Efron & Hinkley 1978).
  - 8,000 Cauchy samples of 20, sorted into quarters by observed information J.
  - the safeguarded numerical location fit's Monte Carlo variance falls from 0.167 to 0.070, and 1/J tracks it (0.167 to 0.066). The expected
    information says 0.10 for every sample.
  - Ancillaries from location-equivariant estimates and conditional precision; observed information does not universally dominate in finite samples.
- **Many parameters.**
  - A gamma fitted to 150 of the World's incomes: shape 2.28, rate 0.0473, correlation 0.89.
  - The likelihood landscape, analytic nuisance ridge and profile likelihood. The joint two-parameter 95% drop is about 3.0; the one-target profile cutoff is 1.92.
  - Profile interval [1.83, 2.80] vs Wald [1.80, 2.76]; modified profiles. Profiling already accounts for nuisance uncertainty to first order; higher-order bias can remain.
- **The trinity.**
  - Wald, score and LR as three readings of one curve. For 14 of 20 against p = ½: W = 3.81, S = 3.20, Λ = 3.29,
    with p-values 0.051 to 0.074: all fail to reject at 5% in this example.
  - Inverting them gives the Wald, Wilson and LR intervals.
  - Hauck–Donner in logistic regression (n = 60): the Wald |z| peaks at 3.77 and falls back to 3.05 as the true slope
    rises to 7, while √Λ climbs to 7.87.
- **Neyman–Scott** (1948).
  - Pairs with their own means: the MLE of σ² converges to σ²/2.
  - 300 data sets of 1,000 pairs give 0.502 (truth 1); dividing by 2n gives 1.003.
  - Why this incidental-parameter profile fails; contrast/marginal and appropriate conditional likelihoods, REML.
    The Board uses inverse-profile-curvature SE sigma-squared-hat / sqrt(n). Growing nuisance dimension is not automatically inconsistent in every model.
- **EM** (Dempster, Laird & Rubin 1977).
  - E- and M-steps for the crabs; each crab split by its responsibility.
  - Jensen's lower bound, drawn along p: 0.90 → 0.82 → 0.73 → 0.64 → 0.57 → … → 0.43.
  - 1,622 iterations, linear convergence at rate 0.9936.
  - The missing-information principle and SEs from an implemented Louis information identity: SE(p̂) = 0.150, so p̂ = 0.43 ± 0.29.
- **When likelihood misbehaves.**
  - Under the midpoint-density approximation, put μ₁ on one assigned midpoint and shrink σ₁: the log likelihood passes the reported local fit's near σ₁ = 10⁻⁷ and rises 221 per
    decade (96 interval counts are assigned that artificial exact value). Actual grouped probabilities remain bounded. Cures.
  - Label switching: the swapped start converges to p = 0.567 with the labels exchanged.
  - Boundary nulls. A parametric bootstrap calibrates a specified two-start EM improvement statistic with
    component SDs constrained to at least 0.002, using the same procedure on observed and null data.
    Its 200 refits give a 95th percentile of 7.79 against the crabs' 53.21. Zero exceedances give a plus-one
    Monte Carlo estimate 1/201 = 0.00498, not an upper bound; the one-sided 95% binomial upper limit is 0.0149.
    The unrestricted global density-mixture LR is undefined, so this procedure is explicitly distinguished from it.
- **Misspecification** (Huber 1967; White 1982).
  - The KL projection: a log-normal fitted to 5,000 World incomes gets the median right (39.0k vs 38.9k) and the
    top tail wrong (0.07% over 300k vs 0.32%).
  - The sandwich derived and estimated.
  - Poisson regression of negative-binomial counts (mean 2.11, variance 6.60): the slope estimate is 0.472 (truth 0.4),
    but the model SE is 0.0333 against a sandwich SE of 0.0531 and a quasi-Poisson SE of 0.0497. The negative-binomial variance is mu + mu²/k,
    so constant-dispersion quasi-Poisson SEs are only an approximate comparison here, not guaranteed valid.
  - Two Board rows.
- **Quasi-, composite and pseudo-likelihood.**
  - Wedderburn's quasi-likelihood, with φ̂ = 2.22.
  - The Ising model on a 48 × 48 lattice: naive enumeration of Z sums over 2²³⁰⁴ ≈ 10⁶⁹³ patterns. Special zero-field two-dimensional
    models have exact methods; the state count alone does not prove computational impossibility.
  - Besag's pseudo-likelihood on 12 lattices at β = 0.3: mean 0.299, SD 0.013. Consistency needs identification, spatial asymptotics and ergodicity; finite Gibbs runs only approximate equilibrium.
    Composite covariance is a sandwich; its inverse is Godambe information and dependent-site scores need spatial covariance estimation.
- **The likelihood principle** (Birnbaum 1962).
  - Nine heads and three tails under two plans. Same likelihood, but the binomial p-value is 0.073 and the
    negative-binomial one is 0.033.
  - With the same fixed prior and these theta-free stopping rules, Beta(10, 4) for both: P(θ > ½) = 0.954.
    The shared sequence must have its third tail on toss 12. Informative sampling/selection needs modeling.
  - Sufficiency plus conditionality; Savage, Mayo, and the Board's stake in stopping rules.
- **Information geometry.**
  - Rao's metric; the normal family as a hyperbolic plane.
  - The geodesic from N(−2, 0.4²) to N(2, 0.4²) has Fisher length 5.6, against 10.0 for sliding the mean.
  - The natural gradient with full-sample information nI (unit step gives Fisher scoring) and Jeffreys's prior.
    Coordinate Euler steps are only locally invariant; drawn ellipses approximate small metric balls.
    Joint normal Jeffreys density is 1/sigma² in dmu dsigma and is improper.

Every number on screen is computed in [`compute.py`](compute.py):
- Weldon's crabs are the Museum's;
- incomes come from the World;
- the rest are seeded simulations or worked examples.

**Built in this part:**
- **`statkit.mle`** ([`explainer/stats/kit/mle.py`](../../../explainer/stats/kit/mle.py)), checked in
  `tests/test_stats_kit_mle.py`:
  - numerical Hessians;
  - the two-normal mixture likelihood, EM with its rate, and Pearson's moment equations (multistart solutions and the sixth
    moment);
  - the binomial trinity, logistic Wald/LR tests and profile intervals;
  - the gamma profile;
  - Neyman–Scott;
  - Poisson regression with model, sandwich and quasi-Poisson SEs;
  - the Cauchy MLE and observed information;
  - Ising Gibbs sampling and Besag's pseudo-likelihood.
- **The likelihood landscape** (`LikelihoodLandscape` in `explainer/stats/viz.py`): a `Landscape` whose contours are
  drawn at fixed drops below the peak, with its peak, profile ridge and profile curve.
- **The Museum**: Weldon's crabs as Pearson printed them (`CRAB_UPPER`, `CRAB_COUNT`, `crabs()`), checked against the
  `pearson` data of the CRAN package mixdist.

The Coverage Board gains five rows:

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| Wald CI, logistic slope | β = 2.5, n = 50 | 1,000 | 96.9% | kept |
| profile-likelihood CI | β = 2.5, n = 50 | 1,000 | 93.3% | kept |
| MLE of σ², Wald CI | Neyman–Scott, 200 pairs | 1,000 | 0.0% | broken |
| Poisson model SE | overdispersed counts, n = 400 | 1,000 | 76.9% | broken |
| sandwich SE | overdispersed counts, n = 400 | 1,000 | 93.3% | kept |

## Build it

```bash
python -m videos.stats.stats22.compute         # once (about six minutes; cached in .cache/stats22)
python tools/build.py stats22 -q l             # fast 480p preview
python tools/build.py stats22                  # 1080p30 -> renders/stats22.mp4
python tools/qa_scene.py stats22 EM
python tools/lecture_length.py stats22 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Weldon's crabs, 1893 | moments A p = 0.533, B p = 0.424; sixth moments 7.88, 7.76 vs 7.45; ML log lik 2567.58 |
| 1 | Upgrade: what Part 9 promised | six conditions; tanks: n(θ − θ̂)/θ → Exponential(1) |
| 2 | Consistency | peaks 1.1, 0.68, 0.638, 0.6103 → 0.61 |
| 3 | Asymptotic normality | Cauchy n = 50: SD 0.208 (0.200) vs median 0.229 (0.222); ratio 1.22 |
| 4 | Observed vs expected information | Var 0.167 → 0.070; 1/J 0.167 → 0.066; 1/(nI) = 0.10 |
| 5 | Many parameters | â = 2.28, b̂ = 0.0473, corr 0.89; profile [1.83, 2.80], Wald [1.80, 2.76] |
| 6 | The trinity | W 3.81, S 3.20, Λ 3.29; Hauck–Donner peak 3.77; Board 96.9% / 93.3% |
| 7 | Neyman–Scott | 0.502 vs 1.003; Board 0% |
| 8 | EM | p 0.90 → 0.82 → 0.73 → 0.64; 1,622 iterations; rate 0.9936; SE(p̂) 0.150 |
| 9 | When likelihood misbehaves | +221 per decade; swapped p = 0.567; constrained EM bootstrap 95th 7.79 vs 53.21 |
| 10 | Misspecification | tail 0.07% vs 0.32%; SE 0.0333 / 0.0531 / 0.0497; Board 76.9% / 93.3% |
| 11 | Quasi-, composite and pseudo-likelihood | φ̂ = 2.22; 10⁶⁹³ states; β̂ 0.299 ± 0.013 |
| 12 | The likelihood principle | p = 0.073 vs 0.033; P(θ > ½) = 0.954 |
| 13 | Information geometry, a glimpse | geodesic 5.6 vs 10.0 |
| 14 | Outro | — |

## Sources

- **History.**
  - W. F. R. Weldon, *Proc. Roy. Soc.* 54 (1893); K. Pearson, *Phil. Trans. A* 185 (1894).
  - R. A. Fisher, *Phil. Trans. A* 222 (1922); *Proc. Roy. Soc. A* 144 (1934).
  - A. Wald, *Ann. Math. Stat.* 20 (1949); J. Neyman & E. Scott, *Econometrica* 16 (1948).
  - C. R. Rao, *Bull. Calcutta Math. Soc.* 37 (1945); *Proc. Camb. Phil. Soc.* 44 (1948).
- **Methods.**
  - B. Efron & D. Hinkley, *Biometrika* 65 (1978); W. Hauck & A. Donner, *JASA* 72 (1977).
  - D. R. Cox & N. Reid, *JRSS B* 49 (1987); E. B. Andersen, *JRSS B* 32 (1970).
  - A. Dempster, N. Laird & D. Rubin, *JRSS B* 39 (1977); T. Louis, *JRSS B* 44 (1982).
  - R. Redner & H. Walker, *SIAM Review* 26 (1984); R. Hathaway, *Ann. Stat.* 13 (1985); J. Hartigan (1985);
    S. Self & K.-Y. Liang, *JASA* 82 (1987); J. Chen, X. Tan & R. Zhang, *Stat. Sinica* 18 (2008).
  - P. Huber (1967), *5th Berkeley Symposium*; H. White, *Econometrica* 48 (1980) and 50 (1982).
  - R. Wedderburn, *Biometrika* 61 (1974); J. Besag, *The Statistician* 24 (1975); B. Lindsay, *Contemp. Math.* 80
    (1988); C. Varin, N. Reid & D. Firth, *Stat. Sinica* 21 (2011).
  - A. Birnbaum, *JASA* 57 (1962); D. Mayo, *Stat. Sci.* 29 (2014); M. Evans, *EJS* 7 (2013).
  - S. Amari, *Neural Computation* 10 (1998); H. Jeffreys, *Proc. Roy. Soc. A* 186 (1946).
- **Books.**
  - Y. Pawitan, *In All Likelihood* (2001).
  - A. W. van der Vaart, *Asymptotic Statistics* (1998).
  - D. R. Cox, *Principles of Statistical Inference* (2006).
  - G. McLachlan & T. Krishnan, *The EM Algorithm and Extensions* (2nd ed., 2008).

## Problems and solutions

**1. Poisson score identities.**

*Solution.* log f = x log λ − λ − log x!, so U = x/λ − 1 and U' = −x/λ².
- **Mean.** E U = λ/λ − 1 = 0.
- **Variance.** Var U = Var(x)/λ² = 1/λ.
- **The identity.** −E U' = λ/λ² = 1/λ, so Var U = −E U' = I(λ).

**2. Neyman–Scott with m readings per group.**

*Solution.* The MLE of each μᵢ is the group mean x̄ᵢ, and σ̂² = (1/(nm)) Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)². Each group's sum of squares
has expectation (m − 1)σ², so E σ̂² = (m − 1)σ²/m. Being an average of n independent terms, σ̂² converges to that, not
to σ². Dividing by n(m − 1) instead fixes it, and is exactly what the marginal likelihood of the within-group
contrasts (or REML) gives. The bias vanishes only as m → ∞, not as n → ∞.

**3. The trinity by hand.**

*Solution.* p̂ = 0.7, n = 20, p₀ = 0.5.
- **Wald.** W = (0.7 − 0.5)² / (0.7 × 0.3/20) = 0.04/0.0105 = 3.81.
- **Score.** U(p₀) = (14 − 10)/(p₀(1 − p₀)) and nI(p₀) = 20/0.25, so S = (14 − 10)²/(20 × 0.25) = 16/5 = 3.20.
- **Likelihood ratio.** Λ = 2[14 log(0.7/0.5) + 6 log(0.3/0.5)] = 2[4.711 − 3.065] = 3.29.

**4. EM for the mixing proportion alone.**

*Solution.* With the components φ₁, φ₂ known, the E-step gives rᵢ = pφ₁(xᵢ)/(pφ₁(xᵢ) + (1 − p)φ₂(xᵢ)). The
expected complete-data log likelihood is Q(p) = Σ[rᵢ log p + (1 − rᵢ) log(1 − p)] + const, maximized at
p = Σrᵢ/n = r̄(pₜ). By Jensen, ℓ(p) ≥ ℓ(pₜ) + Q(p | pₜ) − Q(pₜ | pₜ), with equality at pₜ. Since pₜ₊₁ maximizes Q,
Q(pₜ₊₁ | pₜ) ≥ Q(pₜ | pₜ), so ℓ(pₜ₊₁) ≥ ℓ(pₜ).

**5. The sandwich for an intercept-only Poisson model.**

*Solution.* With log μ = β, the score is Uᵢ = yᵢ − e^β and the MLE is e^β̂ = ȳ.
- **The bread.** A = Σ e^β = nȳ.
- **The meat.** B = Σ(yᵢ − ȳ)² = ns², where s² = Σ(yᵢ − ȳ)²/n.
- **The sandwich.** Var(β̂) ≈ B/A² = ns²/(nȳ)² = s²/(nȳ²), so SE = √(s²/(nȳ²)).

The model-based SE is √(1/(nȳ)), and they agree exactly when s² = ȳ, that is when the counts show Poisson
dispersion.

**6. Alice and Bob.**

*Solution.*
- **Alice.** Under the fair coin, X ~ Binomial(12, ½), and P(X ≥ 9) = (220 + 66 + 12 + 1)/4096 = 299/4096 = 0.073.
- **Bob.** The number of heads H before the 3rd tail has P(H = h) = C(h + 2, 2)/2^{h+3}. Then
  P(H ≥ 9) = 1 − Σ_{h=0}^{8} C(h + 2, 2)/2^{h+3} = 134/4096 = 0.0327. Equivalently, it is the probability of at most
  two tails in the first eleven tosses: (1 + 11 + 55)/2048 = 67/2048.

## Glossary

- **Score; Fisher information; information identity**: ∂ log f/∂θ; its variance; Var U = −E U'.
- **Regularity conditions**: a sufficient checklist includes fixed support, interior truth, suitable integrable local derivative
  envelopes, identifiability, nonsingular information, fixed dimension and a true model; consistency and uniformity
  assumptions must also be verified in the applicable theorem.
- **Consistency; argmax theorem**: θ̂ → θ₀; the peak of a converging curve converges to the limit's peak.
- **Kullback–Leibler divergence**: E_g log(g/f) ≥ 0, zero only when f = g.
- **Asymptotic normality; efficiency**: √n(θ̂ − θ₀) → N(0, I⁻¹); attaining the Cramér–Rao bound in the limit.
- **Observed vs expected information**: −ℓ''(θ̂) for this sample; nI(θ̂), its average over samples.
- **Ancillary statistic; conditionality**: a statistic whose distribution is free of θ; judging by the experiment
  actually done.
- **Information matrix; profile likelihood; nuisance parameter**: curvature in every direction; ℓ maximized over the
  nuisance; a parameter we must estimate but do not care about.
- **Wald, score (Rao) and likelihood-ratio (Wilks) tests**: distance in SEs at θ̂; slope at θ₀; height drop.
- **Hauck–Donner effect**: the Wald statistic falling as the evidence grows.
- **Incidental parameters; Neyman–Scott problem**: parameters whose number grows with n; the inconsistent MLE they
  cause.
- **Marginal, conditional and restricted (REML) likelihood**: appropriate nuisance-free sampling likelihoods; profile likelihood is generally not itself a sampling density.
- **EM algorithm; responsibility; missing-information principle**: alternate expectation and maximization; the
  posterior probability of a label; I_obs = I_complete − I_missing.
- **Unbounded likelihood; label switching; boundary parameter**: a likelihood with no maximum; K! identical peaks;
  a null on the edge of the space, where Wilks fails.
- **Parametric bootstrap**: simulating from the fitted null model to get a reference distribution.
- **Misspecification; KL projection; sandwich (Huber–White)**: a model without the truth; its closest member;
  A⁻¹BA⁻¹/n for the estimator under IID regularity.
- **Quasi-likelihood; dispersion φ**: estimating equations from a mean and variance function; the variance multiple.
- **Composite and pseudo-likelihood; Godambe information**: products of likelihoods of pieces; Besag's product of
  conditionals; the sandwich that measures them.
- **Ising model; normalizing constant**: a lattice of ±1 spins; the sum Z that makes probabilities add to one.
- **Likelihood principle; sufficiency principle; stopping rule**: proportional likelihoods give the same evidence;
  equal sufficient statistics do; when to stop collecting data.
- **Fisher metric; geodesic; natural gradient; Jeffreys prior**: the information as a ruler; the shortest path; the
  gradient in that ruler; √det I.

## Where it comes back

| Idea | Returns in |
|---|---|
| clustered sandwiches; models as approximations | 23 |
| GLMs, quasi-likelihood, GEE | 24 |
| REML: Neyman–Scott cured | 25 |
| Jeffreys and reference priors | 26 |
| variational inference, EM's cousin | 27 |
| AIC as an estimate of KL | 28 |
| M-estimators and the sandwich | 30 |
| EM for missing data | 41 |
| LAN, Hodges and Le Cam | 47 |
| the Coverage Board | every part; 65 |


## QA status

All 15 chapters, numerical helpers and solutions have received scientific source review.
Eight independent Part 22 checks and 12 existing likelihood-kit checks pass (20 total).
The historical crab table matches all 29 rows of CRAN mixdist's published data, including
both open-ended tail classes. Details and current compute/source receipts are in
[the scientific evidence](../../../docs/qa/evidence/stats22-polish-20261107/scientific-review.md).
English visual verification follows; Chinese narration/captions, continuous listening
and final bilingual masters remain open.
