# Statistics, Built — Part 45: The Theory of Estimation

Part 45 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the third part of Stage IV, the PhD core. The part opens with Charles Stein's
result at the Third Berkeley Symposium (1954–55, published 1956): for three or more normal means, the sample means are
inadmissible. It asks what "best" means for an estimator, and answers in three stages:
- **Wald's decision theory** gives the language: risk, admissibility, minimax and Bayes rules, risk sets and complete
  classes.
- **Sufficiency, completeness and equivariance** say when a best estimator exists within a natural class.
- **Stein's paradox**, explained by Brown (1971) through the recurrence of Brownian motion, shows where that search
  ends. Strawderman's proper Bayes minimax rules and Robbins's empirical Bayes show what to do instead.

It keeps two promises:
- **Part 9** called the UMVUE best and proved the Cramér–Rao bound, but only among unbiased estimators. Chapters 1–8
  set out what "best" means in general, prove Lehmann–Scheffé, and show where unbiasedness is absurd.
- **Part 25** showed James–Stein winning on Efron and Morris's hitters, by simulation and a sketch. Chapters 10–13 give
  exact risks, the reason for three dimensions, and proper Bayes minimax rules.

**Built in this part:**
- **`statkit.decision`** ([`explainer/stats/kit/decision.py`](../../../explainer/stats/kit/decision.py)), tested in
  `tests/test_stats_kit_decision.py`:
  - **Finite decision problems:** every non-randomized rule and its risk point; the lower boundary of the convex risk
    set; Bayes rules for a prior; the minimax rule and least favourable prior by linear programming.
  - **Exact risks:** binomial rules (X + a)/(n + a + b) and their Bayes risks; c·Σ(x − x̄)² for σ²; the absurd unbiased
    (−1)^X, the MLE e^{−2X} and 1(X even).
  - **Exponential families:** A, A′, A″ and the Legendre conjugate A* for the Bernoulli, Poisson and normal families,
    with a numerical Legendre transform.
  - **Sufficiency and ancillarity:** the tank estimators' exact SDs and the law of the maximum; Rao–Blackwell given
    the maximum; Cox's two instruments; the uniform location interval given the range.
  - **Information bounds:** Cramér–Rao and second-order Bhattacharyya bounds for θ²; the Chapman–Robbins bound for
    U(0, θ).
  - **Equivariance:** Pitman's location estimator by numerical integration.
  - **Normal means:** James–Stein's exact risk as a Poisson mixture; SURE; Baranchik's family; Strawderman's posterior
    shrinkage by incomplete gamma functions; Brown's integrals and Brownian hitting probabilities.
  - **Empirical Bayes:** Robbins's formula, the gamma-Poisson fit, and the Poisson NPMLE by EM.
- **The risk-set explorer** (`RiskSet` in `explainer/stats/viz.py`), the part's instrument. It draws the risk points of
  a two-state problem, the convex hull of randomized rules, the admissible lower edge, Bayes supporting lines and the
  equal-risk diagonal.

**Data.**
- From the Museum:
  - Ruggles and Brodie's (1947) tank estimates;
  - Efron and Morris's 1970 hitters;
  - one year's claims on 9,461 automobile insurance policies (Efron & Hastie 2016, Table 6.1; new, as
    `museum.INSURANCE_CLAIMS`).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows, all nominal 90% intervals:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| Cox's instruments, unconditional interval | given the precise instrument (SD 1) | 100.0% | conservative |
| Cox's instruments, unconditional interval | given the rough instrument (SD 10) | 80.1% | broken |
| Cox's instruments, conditional interval | given either instrument | 89.9% | kept |
| uniform location, interval given the range | U(θ − ½, θ + ½), n = 5 | 89.7% | kept |
| James–Stein ± 1.645, the large mean | p = 10, θ = (0, …, 0, 5) | 65.8% | broken |
| James–Stein ± 1.645, a zero mean | p = 10, θ = (0, …, 0, 5) | 96.5% | conservative |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats45.compute   # once (under a minute)
python tools/build.py stats45 -q l                         # fast 480p preview
python tools/build.py stats45                              # 1080p30 -> renders/stats45.mp4
python tools/qa_scene.py stats45 RiskSets
python tools/lecture_length.py stats45 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Stein's paradox, 1956 | James–Stein risk 2 at θ = 0 for every p ≥ 3, below p everywhere |
| 1 | Decision theory | Bin(16): max risk 0.0156 (X/n) vs 0.0100 (minimax); Bayes risks 0.0104 / 0.0093 / 0.0100 |
| 2 | Risk sets | 16 rules; minimax 0.404 on the diagonal; least favourable prior 0.672 |
| 3 | Complete class theorems | Beta(ε, ε) rules → X/n; σ²: 0.222 (unbiased), 0.190 (MLE), 0.182 (n + 1) |
| 4 | Exponential families | KL(0.3 ‖ 0.7) = Bregman gap = 0.3389 |
| 5 | Sufficiency in general | the uniform range, ancillary, mean (n − 1)/(n + 1) = 0.667 |
| 6 | Rao–Blackwell and Lehmann–Scheffé | tanks: SD 173 → 70 → 43; (−1)^X: MSE 1 − e^{−4λ} |
| 7 | Ancillarity and Basu | x̄, s² correlation −0.02 (exponential 0.70); Cox: 100% / 80%; uniform 42% → 100% by range |
| 8 | Information inequalities | s² efficiency 0.8–0.98; Chapman–Robbins / UMVUE 0.72 → 0.65 |
| 9 | Equivariance | Pitman ÷ median: 0.72, 0.90, 0.35, 0.83 (normal, Laplace, uniform, Cauchy) |
| 10 | Stein's lemma, SURE, James–Stein | lemma 0.4636 vs 0.4642 (exact 0.4639); hitters SURE 6.1, loss 5.0 vs 17.6 |
| 11 | Why three dimensions | ∫ r^{1−p}: R − 1, log R, 1 − 1/R; BM return 1, 1, ½ |
| 12 | Minimaxity and admissibility | p = 5 at θ = 0: 1.99 (JS), 1.39 (positive part), 0.90 (Strawderman) |
| 13 | Empirical Bayes theory | Robbins 0.168, 0.363, 0.527, …, 6.0; NPMLE raw risk 0.26 → 0.165; population oracle risk 0.14852 |
| 14 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Hook.**
  - X ~ N_p(θ, I) under squared error. X has risk p; James–Stein (1 − (p − 2)/‖X‖²)X has exact risk p − (p − 2)²
    E[1/(p − 2 + 2K)] with K ~ Poisson(‖θ‖²/2).
  - The guarantee is for the total loss, even for unrelated coordinates.
- **Chapter 1.**
  - Loss, rules, risk functions, admissibility.
  - Bin(16) under squared error: X/n, Laplace's (X + 1)/(n + 2), and the flat rule (X + 2)/20 with constant risk
    1/(4(1 + √n)²) = 0.01.
  - The flat rule beats X/n only for 0.20 < p < 0.80 at n = 16, 0.29–0.71 at n = 100, and 0.38–0.62 at n = 1,000.
  - No rule is uniformly best: the stopped clock δ ≡ θ₀ has zero risk at θ₀.
- **Chapter 2.**
  - A coin is fair (p = .5) or biased (p = .8); X is the number of heads in 3 tosses. Calling a fair coin biased costs
    1; missing a biased coin costs 2. That gives 2⁴ = 16 rules.
  - The lower edge has corners at the threshold rules "biased if X ≥ c": (0, 2), (0.125, 0.976), (0.5, 0.208),
    (0.875, 0.016), (1, 0).
  - The Bayes rules for π = 0.25, 0.5, 0.75 are c = 1, 2, 3.
  - Minimax: R₁ = R₂ = 0.4042, mixing c = 3 (0.255) and c = 2 (0.745). The least favourable prior is 0.672 on fair.
- **Chapter 3.**
  - A finite-Bayes-risk rule unique up to sets null under every model law is admissible. Prior-predictive uniqueness alone needs additional support/continuity conditions in general models.
  - In the finite-state, finite-outcome, finite-action randomized problem, the compact convex risk polytope gives the minimax and complete-class conclusions. Finite Θ alone is not a substitute for the needed conditions in arbitrary decision problems.
  - Complete-class limit and generalized Bayes representations require the relevant model, loss, compactness and regularity assumptions. Pointwise limits of Bayes rules alone need not be admissible.
  - X/n is the limit of proper Beta(ε,ε) rules. Haldane's formal posterior mean applies only at interior counts; at X = 0 or n the improper posterior needs the limiting convention.
  - Blyth's (1951) method shows X is admissible in one dimension.
  - c·Σ(x − x̄)² with n = 10: MSE/σ⁴ is 0.222, 0.190 and 0.182 for c = 1/9, 1/10, 1/11. Stein (1964) showed that even
    the last is inadmissible.
- **Chapter 4.**
  - A(η) is convex, with A′ = E T and A″ = Var T = I(η). The MLE matches means. Bernoulli: at η = 0.8, μ = 0.690.
  - The conjugate A*(μ) is minus the entropy, with (A*)′ = (A′)⁻¹.
  - The supremum of the parameter-dependent log-likelihood per observation is A*(T̄); retain the base-density constant for the full likelihood. A finite interior MLE requires T̄ in the image of the mean map. Identifying that image with the convex-support interior additionally requires the full minimal steep regular-family conditions.
  - KL is the Bregman divergence of A*. The deviance is 2n·D_{A*}(T̄, μ̂₀).
  - Poisson: X̄ attains the bound; log λ has no unbiased estimator.
  - Pitman–Koopman–Darmois (1935–36) assumes regular smooth iid models/statistics and common support; arbitrary measurable encodings of the sample into one number are excluded.
- **Chapter 5.**
  - Halmos–Savage factorization for a family dominated by a common sigma-finite measure, via a countable dominating mixture.
  - Lehmann–Scheffé's test for minimal sufficiency. A catalogue: complete for the normal, Poisson, binomial and
    U(0, θ); not for U(θ, θ + 1), N(θ, θ²), Cauchy or Laplace.
  - The uniform range has law Beta(n − 1, 2) for every θ.
  - Full-rank exponential families are complete, by uniqueness of the Laplace transform.
- **Chapter 6.**
  - Rao–Blackwell, via the variance decomposition and Jensen's inequality.
  - Tanks (N = 300, k = 6): E[2X₁ − 1 | M] = M(k + 1)/k − 1. Exact SDs: 173.2 (one serial), 70.1 (moments), 42.9
    (UMVUE); simulated 173.7 / 70.1 / 42.4.
  - Ruggles and Brodie: 169 vs 1,000 vs 122 (June 1940); 244 vs 1,550 vs 271 (June 1941); 327 vs 1,550 vs 342 (August
    1942).
  - (−1)^X is the UMVUE of e^{−2λ}. 1(X even) dominates it, and the MLE e^{−2X} is better still (max MSE 0.30 on λ ≤ 3).
- **Chapter 7.**
  - Basu (1955): with σ known, x̄ and s² are independent; the correlation over 4,000 samples (800 displayed) is −0.02, against 0.70 for
    exponential data.
  - Cox (1958): the unconditional half-width is 12.82, covering 100% given SD 1 and 80% given SD 10. The conditional
    intervals are ±1.645 and ±16.4.
  - Uniform location, n = 5: the midrange ± 0.184 covers 90% overall, but 42% for small ranges and 100% for large
    ones. The analytic unconditional half-width is (1 − 0.1^(1/n))/2 = 0.1845213, independently checked in simulation (90.0545% overall). Conditional on R, the fixed-parameter midrange error is uniform on [−(1−R)/2,(1−R)/2], giving exact 90% conditional coverage. This differs from calling the parameter random given the observed order statistics.
  - Birnbaum (1962) uses particular formulations of mixture conditionality and sufficiency. Observed information can approximate conditional precision in regular models; it is not generally ancillary or uniformly preferable to expected information.
- **Chapter 8.**
  - Multiparameter Cramér–Rao, by a Schur complement. Normal: s² efficiency (n − 1)/n.
  - Bhattacharyya (1946) for θ²: 4θ²/n + 2/n², attained.
  - Chapman–Robbins (1951) for U(0, θ): the ratio to the UMVUE falls from 0.72 (n = 2) to 0.65 (n = 100), tending to
    max s²/(e^s − 1) = 0.648.
  - Hodges's superefficiency.
- **Chapter 9.**
  - Location equivariance gives constant risk. Pitman (1939): the best equivariant rule, generalized Bayes for the
    flat prior.
  - n = 5, MSE of mean / median / Pitman:
    - normal 0.203 / 0.283 / 0.203;
    - Laplace 0.398 / 0.347 / 0.314;
    - uniform 0.0166 / 0.0352 / 0.0122;
    - Cauchy ∞ / 1.15 / 0.96.
  - The uniform midrange's exact MSE 1/(2(n + 1)(n + 2)) against the mean's 1/(12n).
  - Normal location-scale model with unknown μ and σ: under relative squared variance loss, the best location-scale-equivariant rule is SSE/(n+1), generalized Bayes under right Haar dμ dσ/σ. Its action is E[σ^(−2)|x]/E[σ^(−4)|x], not E[σ²|x]. With known μ = 0, the pure-scale answer is Σx²/(n+2).
  - Invariant-minimax and admissibility conclusions need their model conditions. For the identity-covariance normal-mean problem, X is minimax and admissible exactly for p ≤ 2. The proper normal priors N(0,τ²I) have Bayes risk pτ²/(1+τ²) → p, establishing the minimax lower bound.
- **Chapter 10.**
  - Stein's lemma; SURE = p + 2∇·g + ‖g‖².
  - For James–Stein, SURE = p − (p − 2)²/‖X‖².
  - p = 10: exact risk curve and the simulated positive part.
  - At θ = (1, …, 1): mean SURE 6.25, mean loss 6.40, exact risk 6.21.
  - Efron–Morris (arcsine scale, shrinking to the mean with p − 3): factor 0.209, SURE 6.13; squared validation error 5.00 (JS) vs 17.57 (raw) against noisy remaining-season averages. SURE is an approximate Gaussian-model risk estimate using early data only, not an exact unbiased estimate of finite-binomial validation error or a documented prediction made in 1970.
- **Chapter 11.**
  - Tweedie's formula, δ_π = x + ∇ log m.
  - Under Brown's recurrence/admissibility regularity conditions, use the diffusion dY = ½∇ log m dt + dB. For the spherical examples,
    ∫^∞ dr/(r^{p−1} m(r)) = ∞.
  - The flat prior is admissible iff p ≤ 2.
  - Brownian motion from radius 2 reaches the unit ball with probability → 1, 1, ½ in 1, 2, 3 dimensions.
  - Capacity.
  - For p ≥ 3 and 0 ≤ k < p, priors ‖θ‖^(−k) give the stated radial criterion, admissible when k ≥ p−2. The restriction k < p keeps the prior locally integrable at zero. The harmonic-prior admissible/minimax statement uses p ≥ 3.
- **Chapter 12.**
  - Baranchik (1970): SURE = p − (p − 2)²r(2 − r)/s − 4(p − 2)r′. For p ≥ 3, locally absolutely continuous nondecreasing 0 ≤ r ≤ 2, and the required integrability, this makes the rule minimax. The plotted capped r is piecewise smooth, not smooth at its knot.
  - Strawderman (1971): a proper prior that is minimax for p ≥ 5.
  - Risks at ‖θ‖² = 0, 4, 10, 20, 40:

    | Rule | 0 | 4 | 10 | 20 | 40 |
    |---|---|---|---|---|---|
    | James–Stein | 1.99 | 3.46 | 4.19 | 4.56 | 4.77 |
    | positive part | 1.39 | 3.24 | 4.15 | 4.56 | 4.77 |
    | Baranchik | 1.76 | 3.10 | 4.07 | 4.55 | 4.77 |
    | Strawderman | 0.90 | 2.57 | 3.97 | 4.78 | 4.98 |

  - Lindley (1962); limited translation (Efron & Morris 1972).
- **Chapter 13.**
  - Robbins (1956), E[θ | x] = (x + 1)f(x + 1)/f(x). On the insurance claims: 0.168, 0.363, 0.527, 1.333, 1.429, 6.000,
    1.750.
  - The gamma prior (shape 0.70, scale 0.31) gives a linear rule, log-likelihood −5,348.0.
  - The NPMLE (Kiefer & Wolfowitz 1956; Lindsay 1983) gives a monotone rule, log-likelihood −5,340.703496. The continuous-support directional-score certificate bounds the remaining log-likelihood gap by 0.000505; the mixing measure need not be unique.
  - Sparse normal means (10% at 4), risk per coordinate at n = 50, 200, 1,000, 5,000:
    - James–Stein: 0.60, 0.57, 0.59, 0.59;
    - GMLEB: 0.26, 0.14, 0.16, 0.165;
    - oracle Monte Carlo risks: 0.13, 0.13, 0.15, 0.164. The population oracle risk is constant at 0.14852383, computed by independent quadrature. Excess risks of the grid estimator are 0.125996, 0.016576, 0.008635 and 0.000785, with 12, 12, 12 and 4 independent runs. The plot shows ±2 Monte Carlo SE bars. This finite-grid, finite-iteration approximation does not itself inherit all Jiang–Zhang asymptotic regret guarantees.
  - f- and g-modeling (Efron 2014).

## Sources

- **Decision theory.**
  - A. Wald, *Ann. Math. Stat.* 10 (1939); *Statistical Decision Functions* (1950).
  - J. von Neumann, *Math. Ann.* 100 (1928); J. von Neumann & O. Morgenstern (1944).
  - C. Blyth, *Ann. Math. Stat.* 22 (1951); L. Le Cam, *Ann. Math. Stat.* 26 (1955).
- **Sufficiency, completeness and ancillarity.**
  - R. A. Fisher, *Phil. Trans. A* 222 (1922); P. Halmos & L. Savage, *Ann. Math. Stat.* 20 (1949).
  - E. Lehmann & H. Scheffé, *Sankhyā* 10 (1950), 15 (1955).
  - C. R. Rao, *Bull. Calcutta Math. Soc.* 37 (1945); D. Blackwell, *Ann. Math. Stat.* 18 (1947).
  - D. Basu, *Sankhyā* 15 (1955); D. Cox, *Ann. Math. Stat.* 29 (1958).
  - A. Birnbaum, *JASA* 57 (1962); B. Efron & D. Hinkley, *Biometrika* 65 (1978).
- **Exponential families and information.**
  - E. Pitman, *Proc. Camb. Phil. Soc.* 32 (1936); B. Koopman, *Trans. AMS* 39 (1936); G. Darmois, *C. R. Acad. Sci.*
    200 (1935).
  - O. Barndorff-Nielsen, *Information and Exponential Families* (1978); L. Brown, *Fundamentals of Statistical
    Exponential Families* (1986).
  - A. Bhattacharyya, *Sankhyā* 8 (1946); D. Chapman & H. Robbins, *Ann. Math. Stat.* 22 (1951).
- **Equivariance.** E. Pitman, *Biometrika* 30 (1939); M. Girshick & L. Savage, *Proc. Second Berkeley Symp.* (1951);
  C. Stein, *Ann. Math. Stat.* 30 (1959); L. Brown, *Ann. Math. Stat.* 37 (1966).
- **Shrinkage.**
  - C. Stein, *Proc. Third Berkeley Symp.* 1 (1956); W. James & C. Stein, *Proc. Fourth Berkeley Symp.* 1 (1961).
  - C. Stein, *Ann. Inst. Stat. Math.* 16 (1964); *Ann. Stat.* 9 (1981); A. Baranchik, *Ann. Math. Stat.* 41 (1970).
  - L. Brown, *Ann. Math. Stat.* 42 (1971); W. Strawderman, *Ann. Math. Stat.* 42 (1971).
  - D. Lindley, discussion, *JRSS B* 24 (1962); B. Efron & C. Morris, *JASA* 67 (1972), 68 (1973), 70 (1975).
- **Empirical Bayes.**
  - H. Robbins, *Proc. Third Berkeley Symp.* 1 (1956); J. Kiefer & J. Wolfowitz, *Ann. Math. Stat.* 27 (1956).
  - B. Lindsay, *Ann. Stat.* 11 (1983); W. Jiang & C.-H. Zhang, *Ann. Stat.* 37 (2009).
  - R. Koenker & I. Mizera, *JASA* 109 (2014); B. Efron, *Stat. Sci.* 29 (2014).
  - B. Efron & T. Hastie, *Computer Age Statistical Inference* (2016).
- **Books.**
  - E. Lehmann & G. Casella, *Theory of Point Estimation* (2nd ed. 1998); J. Berger, *Statistical Decision Theory and
    Bayesian Analysis* (2nd ed. 1985).
  - T. Ferguson, *Mathematical Statistics: A Decision Theoretic Approach* (1967); R. Keener, *Theoretical Statistics*
    (2010).

## Problems and solutions

1. **The binomial minimax rule.**
   - With a = √n/2, the MSE of (X + a)/(n + 2a) is [np(1 − p) + a²(1 − 2p)²]/(n + 2a)².
   - The numerator is np − np² + (n/4)(1 − 4p + 4p²) = n/4, the same for every p. So the risk is
     n/(4(n + √n)²) = 1/(4(1 + √n)²).
   - The rule is the posterior mean under Beta(a, a), so it is Bayes with constant risk. By chapter 2's theorem, no
     rule has smaller maximum risk: its maximum equals its Bayes risk, which is the smallest possible average.
2. **Completeness of the uniform maximum.**
   - M = max X_i has density n t^{n−1}/θⁿ on (0, θ).
   - If E_θ g(M) = 0 for all θ, then ∫₀^θ g(t) t^{n−1} dt = 0 for all θ. Differentiating gives g(θ)θ^{n−1} = 0 for
     almost every θ, so g = 0.
   - E M = nθ/(n + 1), so (n + 1)M/n is unbiased and, by Lehmann–Scheffé, the UMVUE.
3. **The absurd unbiased estimator.**
   - Unbiasedness means Σ_x δ(x) e^{−λ} λ^x/x! = e^{−2λ}, that is Σ_x δ(x) λ^x/x! = e^{−λ} = Σ_x (−1)^x λ^x/x! for
     every λ > 0.
   - Power series that agree on an interval have equal coefficients, so δ(x) = (−1)^x.
4. **Basu for the range.**
   - With σ = 1 known, X̄ is complete sufficient for μ (a full-rank exponential family).
   - The range X_(n) − X_(1) is unchanged by shifting every observation, so its law does not involve μ: it is
     ancillary.
   - By Basu's theorem the two are independent, for every μ.
5. **Pitman for a shifted exponential.**
   - ∏ f(x_i − t) = exp(−Σ x_i + nt) for t < m = min x_i, and 0 otherwise.
   - So θ̂_P = ∫_{−∞}^m t e^{nt} dt / ∫_{−∞}^m e^{nt} dt = m − 1/n. It is unbiased, since E min X_i = θ + 1/n.
6. **The SURE-optimal shrinkage.**
   - For p ≥ 3, X ∼ N_p(θ,I) and x ≠ 0, let g = −c x/‖x‖²: ‖g‖² = c²/‖x‖² and ∇·g = −c(p − 2)/‖x‖².
   - So SURE = p + (c² − 2c(p − 2))/‖x‖². This is minimized at c = p − 2 for every x, giving p − (p − 2)²/‖x‖².
   - The expected value of this minimized SURE is James–Stein's risk.

## Glossary

- **Decision theory.**
  - Loss; decision rule; risk function; admissible, inadmissible, dominated: the vocabulary.
  - Minimax; Bayes risk; Bayes rule; least favourable prior; equalizer rule; randomized rule; risk set: the
    criteria.
  - Complete class; generalized Bayes rule; Blyth's method; Haldane's prior: which rules to consider.
- **Data reduction.**
  - Natural parameter; cumulant function A; mean-value parameter; Legendre conjugate A*; Bregman divergence; curved
    family: exponential families.
  - Sufficient, minimal sufficient, complete, boundedly complete; factorization (Halmos–Savage); ancillary: data
    reduction.
  - Rao–Blackwellization; UMVUE; Lehmann–Scheffé; Basu's theorem; conditionality principle; likelihood principle:
    using it.
- **Bounds and symmetry.**
  - Fisher information matrix; Cramér–Rao bound; efficiency; orthogonal parameters; Bhattacharyya bound;
    Chapman–Robbins bound; superefficiency: information bounds.
  - Location and scale family; equivariant rule; Pitman estimator; Haar measure: symmetry.
- **Shrinkage and empirical Bayes.**
  - Stein's lemma; SURE; James–Stein; positive part; Baranchik's family; Strawderman's prior; harmonic prior;
    limited translation: shrinkage.
  - Tweedie's formula; Brown's recurrence criterion; capacity: why three dimensions.
  - Robbins's formula; f- and g-modeling; NPMLE (Kiefer–Wolfowitz); GMLEB; regret: empirical Bayes.

## Where it comes back

- **Part 46**: risk sets and least favourable priors for tests; Neyman–Pearson as a Bayes rule; Lehmann's UMPU tests.
- **Part 47**: the local asymptotic minimax theorem (Hájek, Le Cam) replaces the Cramér–Rao bound.
- **Part 50**: minimax rates, by the methods of Le Cam, Assouad and Fano.
- **Part 52**: shrinkage and empirical Bayes in high dimensions.
- **Part 53**: the frequentist risk of Bayes rules as the sample grows.


## Numerical and QA scope

Pitman estimates use exact normal/uniform formulas and whole-line adaptive quadrature split at observations for Laplace/Cauchy errors. A fixed median-centered integration window can miss the normal likelihood peak on extreme samples. The finite simulation percentages describe the displayed samples, not exact population improvements.

Robbins frequency ratios are plug-in estimates, not unbiased estimators. Posterior mean monotonicity here is a property of the Poisson-mixture model; next-year prediction also assumes stable policy rates, conditional independence and equal exposure. A discrete NPMLE with at most the number of distinct observations exists; the mixing law need not be unique. Poisson optimization has a likelihood-gap certificate, whereas the normal empirical Bayes illustration remains a 221-point, 1,500-iteration EM approximation.

Coverage Board rows retain actual independent sample counts and empirical Monte Carlo uncertainty, including the two instrument-selected subsets. The interval example uses positive-part James–Stein. SURE assumptions, selection optimism, noisy batting validation targets and the distinction between expected risk and realized error are explicit. The SURE scatter shows all 400 replicates, including negative risk estimates.

See the [scientific review and verification receipts](../../../docs/qa/evidence/stats45-polish-20261107/source-review.md). The recorded English endpoint/native/motion and representative narrated-preview checkpoint is complete. Chinese narration/caption tables, continuous listening and final bilingual masters remain open.
