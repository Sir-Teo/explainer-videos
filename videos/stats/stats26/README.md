# Statistics, Built — Part 26: Bayesian Data Analysis

Part 26 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the sixth part of Stage III, Master's. Part 15 laid down Bayes's machinery for
one parameter with a prior chosen by hand. This part builds, fits, checks and defends Bayesian models with many
parameters: hierarchies justified by exchangeability, priors chosen for reasons, tests and decisions, and the
workflow that makes the result trustworthy.

It opens with Rubin's (1981) eight schools: SAT coaching experiments in eight high schools, with estimated effects
28, 8, −3, 7, −1, 1, 18, 12 and standard errors 9 to 18 points.
- No pooling believes each estimate; complete pooling gives one effect, 7.7 ± 4.1. Cochran's Q = 4.7 on 7 df
  (p = 0.70) cannot reject equal effects.
- Part 25's empirical Bayes estimates τ̂ = 0 and collapses to complete pooling.
- The hierarchical model averages over τ instead.

From there the part covers:
- **The upgrade.**
  - Part 15's assumptions; exchangeability (Part 5) and de Finetti's theorem as the justification for the hierarchy.
  - Conditional exchangeability with covariates; hierarchies in practice (MRP, genes, sport, meta-analysis).
- **Hierarchical models.**
  - The three-level model and its factorization: p(τ | y) on a wide nonuniform grid checked against infinite-range integration, then μ | τ and θ | μ, τ, giving independent draws with a checked numerical approximation for τ and exact conditional normal draws.
  - The τ explorer. τ's posterior median is 5.2, 95% interval [0.2, 20.8], mode 0.
  - Posterior medians: A 10.2 [−2.2, 31.6], C 6.7, E 5.6; μ has mean 7.9.
  - P(θ_A > θ_C) = 0.68; P(A is the best school) = 0.25, against 1/8 a priori.
- **Priors.**
  - Jeffreys's rule and its invariance; Beta(½, ½) on the p and logit scales.
  - Reference priors (Bernardo 1979; σ⁻¹ gives Student's t); weakly informative priors (Gelman 2006).
  - τ's posterior under four priors (medians):

    | Prior | All eight schools | Schools A–C |
    |---|---|---|
    | uniform on τ | 5.2 | 23.0 |
    | half-Cauchy(25) | 4.8 | 10.9 |
    | inv-gamma(1, 1) on τ² | 1.2 | 1.2 |
    | inv-gamma(.001, .001) | 0.6 | 1.0 |

  - An improper posterior from a flat prior on log τ.
- **Conjugate families.**
  - Exponential families; Diaconis–Ylvisaker linear posterior mean characterizations under regularity; priors as pseudo-data.
  - The World's doctor visits with a Gamma(4, 1) prior: posterior means 3.50, 1.83, 1.38, 2.83 and 2.15 for 1 to
    1,000 adults (truth 2.24). The n = 100 interval [2.51, 3.17] misses, because the Poisson model is wrong.
  - The predictive is a negative binomial.
- **Bernstein–von Mises.**
  - The statement and Laplace's argument.
  - A Poisson rate's posterior against N(λ̂, λ̂/n): full-support TV 0.084, 0.028 and 0.008 at n = 3, 30 and 300.
  - Exact coverage of the Jeffreys interval: 98.3% at n = 1, 95.2% at n = 100.
  - Failures: few groups and the eight schools' τ (mode on the boundary), Neyman–Scott, nonparametric priors.
- **Bayes factors.**
  - Definition; the Kass–Raftery scale; the normal point null in closed form.
  - z = 2.5, n = 50 (p = 0.012): BF₀₁ = 0.33 with τ = σ, at best 0.18, and 311 at τ = 1,000 (Bartlett).
  - BIC 0.31 against the unit-information prior's 0.33.
  - Model averaging; cautions.
- **Lindley's paradox.**
  - The PEAR random event generator: 52,263,470 of 104,490,000, z = 3.61, p = 0.0003. Jefferys's uniform-prior BF₀₁ is
    11.9, so P(H₀ | y) = 0.92.
  - Why: the alternative spreads its predictions over [0, 1].
  - At fixed p = 0.05, BF₀₁ grows like √n: 0.58 at n = 10, 4.7 at 1,000, 464 at 10⁷.
  - Sellke–Bayarri–Berger: p = 0.05 leaves P(H₀ | y) ≥ 0.29.
- **Occam's razor.**
  - MacKay's picture. The evidence for polynomial degree on 20 points from a cubic peaks at degree 3 (log evidence
    −6.47), while the maximized log likelihood keeps rising.
  - A gentle razor under N(0, 1) coefficient priors; the Occam factor and BIC; type II maximum likelihood.
- **Decisions.**
  - Expected utility (Savage 1954); losses giving the mean, median, mode and quantiles.
  - Bayes risk and Wald's complete class theorem.
  - Should a ninth school adopt coaching? P(θ_new > 5) = 0.66 and the expected gain is 2.93 points.
  - EVPI 2.20; EVSI of a pilot with SE 10 is 1.23, by direct normal-mixture integration.
- **Checking.**
  - Posterior predictive p-values. The eight schools pass on the maximum (0.48), minimum (0.17) and SD (0.78).
  - Of 500 adults, 43% had no visits. No Poisson replicate matches that zero fraction (0 of 2,000); a proper negative-binomial posterior check gives 0.47 for this feature.
  - Double use of the data.
  - Prior predictive checks for a logistic regression: N(0, 10²) priors put 83% of predictions below 1% or above 99%,
    against 6% for N(0, 1).
- **Workflow.**
  - Gelman et al. (2020); computational checks (R̂, ESS, divergences).
  - Simulation-based calibration catches a halved variance (χ² p ≈ 10⁻¹³⁷) and a wrong prior mean (p ≈ 10⁻²⁷⁰). The
    correct code passes (p = 0.09).
  - Three Board rows; sensitivity analysis.
- **The argument.**
  - History from Bayes to Gelfand & Smith; coherence (Dutch books, Cox, Savage).
  - The likelihood principle: 9 heads and 3 tails give p = 0.073 or 0.033 depending on the stopping rule, with the same
    posterior.
  - Objections; calibrated Bayes (Box, Rubin, Little); the schools side by side.
- **The Dirichlet process.**
  - Ferguson (1973) and conjugacy; stick-breaking for α = 1 and 5.
  - The Chinese restaurant (30 customers, 5 tables). E K_n ≈ α log(1 + n/α): 9.8 and 38.5 tables at n = 10,000. A
    simulated restaurant of 200 with α = 2 has 12 tables (expected 9.8).
  - DP mixtures; Gaussian processes; Part 53.

Every number on screen is computed in [`compute.py`](compute.py):
- the eight schools and the PEAR data are the Museum's;
- doctor visits and schools are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.bayes` II** ([`explainer/stats/kit/bayes.py`](../../../explainer/stats/kit/bayes.py)), checked in
  `tests/test_stats_kit_bayes2.py`:
  - the hierarchical normal model (`hier_normal`: τ's marginal posterior on a grid, conditional means and independent numerical draws);
  - `bf01_normal`; the Sellke–Bayarri–Berger bound;
  - Bayesian linear regression's evidence and posterior;
  - simulation-based calibration;
  - the Chinese restaurant process, its expected table count, and stick-breaking.
- **The τ explorer** (`TauExplorer` in `explainer/stats/viz.py`): the schools' conditional means against τ above τ's
  posterior, with a moving cursor.
- **The Museum**: `EIGHT_SCHOOLS` / `eight_schools()`, and the PEAR counts `PEAR_N`, `PEAR_S`.

The Coverage Board gains three rows:

| Method | Setting | Independent sets / intervals | Achieved | Verdict |
|---|---|---|---|---|
| no pooling, ȳ_j ± 1.96σ_j | 8 of the World's schools, 10 pupils each | 1,000 / 8,000 | 94.7% | kept |
| complete pooling | 8 schools, 10 pupils each | 1,000 / 8,000 | 31.9% | broken |
| hierarchical, 95% credible | 8 schools, 10 pupils each | 1,000 / 8,000 | 93.8% | broken |

The hierarchical numerical intervals are 11% narrower than no pooling's. Monte Carlo error is estimated across
1,000 independent dataset-level coverage averages, retaining the dependence among eight intervals within a fit.
Prior-average calibration requires a proper prior and its joint generative model; it is not guaranteed by the
improper-flat-hyperprior fit used here or by the finite World's school population.

## Build it

```bash
python -m videos.stats.stats26.compute         # once (seconds; cached in .cache/stats26)
python tools/build.py stats26 -q l             # fast 480p preview
python tools/build.py stats26                  # 1080p30 -> renders/stats26.mp4
python tools/qa_scene.py stats26 Hierarchy
python tools/lecture_length.py stats26 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The eight schools, 1981 | pooled 7.7 ± 4.1; Q 4.7, p 0.70; τ̂_EB = 0 |
| 1 | Upgrade: what Part 15 assumed | exchangeability; de Finetti |
| 2 | Hierarchical models | τ median 5.2 [0.2, 20.8]; A 10.2 [−2.2, 31.6]; P(A > C) 0.68; P(A best) 0.25 |
| 3 | Priors | medians 5.2 / 4.8 / 1.2 / 0.6 (eight), 23.0 / 10.9 / 1.2 / 1.0 (three) |
| 4 | Conjugate and exponential families | 3.50 → 2.15; the n = 100 interval misses 2.24 |
| 5 | Bernstein–von Mises | TV 0.084 / 0.028 / 0.008; coverage 98.3% → 95.2% |
| 6 | Bayes factors | BF₀₁ 0.33, min 0.18, 311 at τ = 1,000; BIC 0.31 |
| 7 | Lindley's paradox | PEAR p 0.0003, BF₀₁ 11.9, P(H₀) 0.92; 0.58 → 464; SBB 0.29 |
| 8 | Occam's razor, built in | the evidence peaks at degree 3 |
| 9 | Decisions | P 0.66; gain 2.93; EVPI 2.20; EVSI 1.23 |
| 10 | Checking | p_B 0.48 / 0.17 / 0.78; zeros 43%: Poisson 0/2,000 exceedances, NB 0.47; 83% vs 6% extreme |
| 11 | Workflow | SBC p 0.09 / 10⁻¹³⁷ / 10⁻²⁷⁰; Board 94.7 / 31.9 / 93.8% |
| 12 | The argument, honestly | 0.073 vs 0.033 under two stopping rules |
| 13 | Bayesian nonparametrics, first look | 5 tables of 30; 12 of 200 (9.8 expected) |
| 14 | Outro | — |

## Sources

- **History.**
  - D. Rubin, *J. Educational Statistics* 6 (1981); D. Alderman & D. Powers, *American Educational Research J.* 17
    (1980).
  - R. Jahn, B. Dunne & R. Nelson, *J. Scientific Exploration* 1 (1987); W. Jefferys, *J. Scientific Exploration* 4
    (1990). Some later sources print 52,263,471 successes.
  - S. B. McGrayne, *The Theory That Would Not Die* (2011).
- **Foundations.**
  - B. de Finetti (1931, 1937); E. Hewitt & L. Savage, *Trans. AMS* 80 (1955); R. Cox, *Am. J. Physics* 14 (1946);
    L. Savage, *The Foundations of Statistics* (1954).
  - A. Birnbaum, *JASA* 57 (1962); D. Lindley & L. Phillips, *The American Statistician* 30 (1976); A. Wald (1950).
- **Priors.**
  - H. Jeffreys, *Proc. R. Soc. A* 186 (1946) and *Theory of Probability* (1939); J. Bernardo, *JRSS B* 41 (1979);
    J. Berger & J. Bernardo (1992); A. Gelman, *Bayesian Analysis* 1 (2006).
  - P. Diaconis & D. Ylvisaker, *Ann. Stat.* 7 (1979); S. Dalal & W. Hall, *JRSS B* 45 (1983).
- **Asymptotics.** L. Le Cam (1953); D. Freedman, *Ann. Math. Stat.* 34 (1963); P. Diaconis & D. Freedman, *Ann. Stat.*
  14 (1986).
- **Testing and models.**
  - R. Kass & A. Raftery, *JASA* 90 (1995); M. Bartlett, *Biometrika* 44 (1957); D. Lindley, *Biometrika* 44 (1957).
  - T. Sellke, M. J. Bayarri & J. Berger, *The American Statistician* 55 (2001); G. Schwarz, *Ann. Stat.* 6 (1978);
    R. Kass & L. Wasserman, *JASA* 90 (1995).
  - D. MacKay, *Neural Computation* 4 (1992); J. Hoeting, D. Madigan, A. Raftery & C. Volinsky, *Stat. Sci.* 14 (1999).
- **Decisions.** H. Raiffa & R. Schlaifer, *Applied Statistical Decision Theory* (1961).
- **Checking and workflow.**
  - D. Rubin, *Ann. Stat.* 12 (1984); A. Gelman, X.-L. Meng & H. Stern, *Statistica Sinica* 6 (1996).
  - G. Box, *JRSS A* 143 (1980); R. Little, *The American Statistician* 60 (2006).
  - S. Talts, M. Betancourt, D. Simpson, A. Vehtari & A. Gelman, arXiv:1804.06788 (2018); A. Gelman et al., *Bayesian
    Workflow*, arXiv:2011.01808 (2020).
  - A. Gelman & D. Rubin, *Stat. Sci.* 7 (1992); A. Vehtari et al., *Bayesian Analysis* 16 (2021).
- **Nonparametrics.**
  - T. Ferguson, *Ann. Stat.* 1 (1973); J. Sethuraman, *Statistica Sinica* 4 (1994); C. Antoniak, *Ann. Stat.* 2 (1974).
  - M. Escobar & M. West, *JASA* 90 (1995); J. Pitman (2006).
- **Books.**
  - A. Gelman, J. Carlin, H. Stern, D. Dunson, A. Vehtari & D. Rubin, *Bayesian Data Analysis* (3rd ed., 2013).
  - R. McElreath, *Statistical Rethinking* (2nd ed., 2020).
  - C. Robert, *The Bayesian Choice* (2nd ed., 2007).

## Problems and solutions

**1. The marginal posterior of τ.**

*Solution.* Integrate the effects out first: y_j | μ, τ ~ N(μ, σ_j² + τ²) independently. So
p(μ, τ | y) ∝ p(τ) Π_j (σ_j² + τ²)^{−1/2} exp{−(y_j − μ)²/2(σ_j² + τ²)}.
- **Complete the square in μ.** With w_j = 1/(σ_j² + τ²), Σ w_j(y_j − μ)² = Σ w_j(y_j − μ̂)² + (Σ w_j)(μ − μ̂)², where
  μ̂ = Σ w_j y_j / Σ w_j.
- **Integrate μ out.** The Gaussian integral gives (2π/Σ w_j)^{1/2} = (2π V_μ)^{1/2}.
- **The result.** p(τ | y) ∝ p(τ) V_μ^{1/2} Π_j (σ_j² + τ²)^{−1/2} exp{−(y_j − μ̂)²/2(σ_j² + τ²)}.

**2. Jeffreys's invariance.**

*Solution.* With ℓ(θ) the log likelihood and θ = h(η), the score is dℓ/dη = (dℓ/dθ)(dθ/dη). Therefore
I(η) = E{(dℓ/dη)²} = I(θ)(dθ/dη)², and √I(η) = √I(θ)|dθ/dη|. That is exactly the change-of-variables rule for a
density: Jeffreys's prior for η is the transform of Jeffreys's prior for θ.

**3. The Poisson–gamma posterior mean.**

*Solution.* The posterior is Gamma(a + Σx, b + n), whose mean is (a + nx̄)/(b + n) = {b/(b + n)}(a/b) + {n/(b + n)}x̄.
That is a weighted average of the prior mean a/b and x̄, with the prior worth b observations.

**4. The normal Bayes factor.**

*Solution.* Under H₀, ȳ ~ N(0, v) with v = σ²/n; under H₁, ȳ ~ N(0, v + τ²). So
BF₀₁ = √{(v + τ²)/v} exp{−ȳ²/2v + ȳ²/2(v + τ²)} = √(1 + nτ²/σ²) exp{−(z²/2) nτ²/(σ² + nτ²)}, with z = ȳ/√v. As
τ → ∞ the exponent tends to −z²/2 while the square root grows without bound, so BF₀₁ → ∞ for any fixed data:
Bartlett's paradox.

**5. The median and absolute loss.**

*Solution.* E|a − θ| = ∫_{θ<a} (a − θ)p(θ)dθ + ∫_{θ>a} (θ − a)p(θ)dθ. Its derivative in a is P(θ < a) − P(θ > a), which is
negative below the median and positive above it. So the expected loss is minimized at the posterior median.

**6. The expected number of tables.**

*Solution.* Customer i + 1 (i = 0, …, n − 1) opens a new table with probability α/(α + i), whatever happened before.
K_n is the sum of these indicators, so E K_n = Σ_{i=0}^{n−1} α/(α + i). The sum behaves like ∫₀ⁿ α/(α + t) dt =
α log(1 + n/α).

## Glossary

- **Hierarchical model; hyperparameter; hyperprior**: parameters drawn from a population whose parameters have their
  own prior.
- **Exchangeability; de Finetti's theorem**: beliefs unchanged by relabelling; infinitely extendible exchangeable sequences admit mixtures of iid laws; a normal mixing population is an additional modelling choice.
- **Partial pooling; no pooling; complete pooling**: estimates between the separate and the combined.
- **Jeffreys prior; reference prior; weakly informative prior; improper prior/posterior**:
  - √det I(θ), invariant under reparametrization;
  - the prior maximizing expected information gain;
  - a prior that rules out only the absurd;
  - a non-normalizable density, acceptable only if the posterior normalizes.
- **Conjugate prior; Diaconis–Ylvisaker**: a prior family closed under updating; linear posterior mean characterizations require regularity and boundary conditions.
- **Bernstein–von Mises theorem**: posteriors become normal around the MLE with inverse-information variance.
- **Bayes factor; marginal likelihood (evidence); BIC; Bartlett's paradox; model averaging**:
  - the ratio of evidences;
  - p(y | M);
  - −2ℓ̂ + k log n;
  - an arbitrarily diffuse specified alternative can favor the null for fixed data;
  - averaging over models by their posterior probabilities.
- **Lindley's paradox; Sellke–Bayarri–Berger bound**: significant results that favour the null in large samples;
  BF₀₁ ≥ −e p log p for the specified continuous-p-value/Beta-mixture alternative class.
- **Occam factor; type II maximum likelihood**: posterior width over prior width; maximizing the evidence over
  hyperparameters.
- **Expected utility; Bayes rule; Bayes risk; complete class; EVPI; EVSI; pre-posterior analysis**:
  - the criterion for decisions and the rule it gives;
  - risk averaged over the prior;
  - admissible rules are (limits of) Bayes rules;
  - the value of perfect and of sample information;
  - deciding by simulating the study.
- **Posterior predictive check; p_B; prior predictive check**: comparing data with replicates from the fitted (or
  prior) model.
- **Simulation-based calibration; R̂; effective sample size; divergence**: necessary prior-averaged rank checks, which can miss some coding errors;
  MCMC diagnostics.
- **Dutch book; coherence; likelihood principle; calibrated Bayes**:
  - sure-loss bets;
  - consistency with the probability rules;
  - inference depends on the data only through the likelihood;
  - Bayesian models judged by frequency properties.
- **Dirichlet process; stick-breaking; Chinese restaurant process**: a prior on distributions; its atoms' weights; its
  partition of the data.

## Where it comes back

| Idea | Returns in |
|---|---|
| computing posteriors: MCMC, HMC, Neal's funnel | 27 |
| LOO, WAIC, BIC, stacking | 28 |
| shrinkage priors: the horseshoe | 32 |
| empirical Bayes for many tests | 33 |
| decisions in experiments | 35 |
| Gaussian processes | 39 |
| decision theory, admissibility | 45 |
| Bernstein–von Mises proved; Bayesian nonparametrics | 53 |
| the Coverage Board | every part; 65 |


## Scientific and numerical qualifications checked in QA

The three-school uniform-prior posterior has about **32.86% probability above 40**. The old grid stopped there,
giving a truncated median of 13.7. Infinite-range integration gives median 23.0486 and 95th percentile 285.2375.
The revised grid extends to one million; its omitted three-school uniform-prior tail is about 0.00143%, and its
CDF agrees with the adaptive reference. The eight-school uniform-prior omitted mass above 40 is about 0.119%.
Posterior plots of competing priors now use log-tau density with the correct Jacobian, without flattened peaks.
Quantiles retain the tails outside the plotted range. Grid integration and tau draws are numerical approximations,
not exact continuous-posterior calculations.

Finite exchangeability alone does not imply an iid mixture, and de Finetti does not imply a normal population
described solely by mu and tau. Infinite extendibility, the population family and the hyperprior are stated
separately. An inverse-gamma density mode near zero does not mean its entire prior mass concentrates there;
small-parameter inverse gammas also have extreme tails. Reference priors use an ordered asymptotic
posterior-to-prior information criterion.

Conjugate mean identities and their converses need regularity. Pseudo-data counts depend on the parameter
convention; the variance update shown assumes a known mean. Logistic models can have formal conjugate families
without convenient normalizers, while normal coefficient priors are not conjugate. A missed interval alone is not
a model diagnosis. The Poisson predictive is more dispersed than a Poisson at the same predictive mean, not more
dispersed than every Poisson distribution.

Bernstein–von Mises assumes a correctly specified regular fixed-dimensional model, posterior concentration,
interior identifiable truth, nonsingular information and a positive continuous prior locally. Posterior width
has root-n scale; the general theorem does not supply a universal rate for prior influence. Full-support TV
includes negative normal support and tails beyond the plotting window. High-dimensional/nonparametric
counterexamples do not preclude positive results for particular priors and functionals.

Bayes factors compare specified prior predictive models. The 0.18 minimum is within the zero-centered normal
alternative family, not all possible priors. BIC drops prior-dependent order-one terms. Stacking changes the
weighting criterion but component predictions still depend on priors. The PEAR calculations assume iid binary
trials and a specified model pair; a posterior probability of p = 0.5 is not a causal probability that intention
had no effect. The recorded counts have a one-success discrepancy across historical secondary sources; both
repository counts are stated, and high-precision arithmetic checks the selected version. The fixed-p curve now
uses matching integer sample sizes. Sellke–Bayarri–Berger calibration is explicitly limited to a continuous
uniform null p-value and the stated Beta(xi,1)-mixture alternative class, with model prior odds stated.

Occam's evidence-to-maximum-likelihood ratio is at most one. A posterior/prior width ratio is an approximation
under a concentrated unimodal posterior and locally flat prior, not a universal standard-deviation inequality.
Polynomial evidence depends on the coefficient basis, units, prior and assumed known noise. Its peak at the
generating degree is a seeded example, not a guarantee of discovering truth.

Zero-one loss selects a maximum posterior **mass** for a discrete parameter. Exact-match zero-one loss does not
select a mode from a continuous distribution. Expected utility and complete-class representation theorems require
their full assumptions. Coaching decisions use a hypothetical linear utility and an exchangeable new school,
within the specified model. Direct mixture integration replaces the biased/coarsened in-sample binned pilot
calculation; EVSI lies between zero and EVPI and has the correct zero/infinite-noise limits.

The negative-binomial predictive check now uses a proper posterior on log mean and log shape, with normal priors
N(log 3,1) and N(0,1.5 squared), and a checked two-dimensional grid. Bootstrap parameters are no longer described as
posterior draws. Zero Poisson exceedances are reported as a simulation count, not a mathematically zero tail
probability. Matching one discrepancy is not proof of model correctness. Prior distributions of conditional
logistic risks are distinguished from marginal prior-predictive outcomes: symmetry gives marginal probability
one half for each fixed predictor vector, even when conditional risks tend to extremes.

SBC needs a proper prior and suitable independent posterior draws; uniform marginal ranks are necessary and can
miss errors. R-hat, effective sample size and divergences are diagnostic screens, not proofs of mode coverage.
Grid calculations require mesh and tail checks. Model-based prior-average coverage requires a proper prior;
the Board records empirical simulation uncertainty at the independent-dataset level.

Coherence arguments require the additional Cox/Savage axioms and do not select a unique prior or likelihood.
Proportional likelihoods give the same posterior for a fixed prior and ignorable stopping/selection. Both Bayesian
and frequentist methods can handle related parameters and repeated-use guarantees under assumptions. Gibbs
sampling enabled many difficult models without guaranteeing feasible computation for every posterior.

DP conjugacy is for direct iid draws from G; in a noisy hierarchy it is conditional on latent effects. The first
30 stick weights are displayed at their actual widths, with remaining probability shown separately. Mixture
cluster counts remain uncertain and depend on the model and concentration parameter; they are not guaranteed
true-component counts.

Local geometric curve clipping retains viewport intersections and missing gaps, while preserving paths usable
by dashed animations. Continuous listening, Chinese narration/caption tables and final masters remain open.
