# Statistics, Built — Part 55: The Qualifying Exam

Part 55 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the last part of Stage IV, the PhD core. Like Part 42, it adds no new method.

It opens with Hilbert's twenty-three problems (Paris, 1900): "as long as a branch of science offers an abundance of
problems, so long is it alive". Then the letter on the desk the night before the qualifying exam: twelve problems, drawing
on the core, and "a correct answer without its proof earns nothing". The problems are set in six
sittings, each posed on an exam card, paused, proved on screen, and drawn as a proof map:

1. **Borel–Cantelli** (43): M_n / log n → 1 a.s. for exponential maxima.
2. **Optional stopping, unbounded** (44): the walk stopped at +1 has E S_T = 1; gambler's ruin and Wald's identity.
3. **A UMVUE, and none** (45): (1 − 1/n)^T for e^{−λ}; no unbiased estimator of 1/p.
4. **Blyth's method** (45): X is admissible for a normal mean in one dimension; where the argument fails in two.
5. **Neyman structure** (46): the UMPU test of equal Poisson rates, on Snow's Table IX; an exact interval.
6. **LAN and local power** (47): the logistic location model; score, t and sign tests; the power envelope.
7. **Bracketing** (48): half-line indicators are Donsker; which smoothness classes are not.
8. **An influence function** (49): the median's, on Newcomb's passage times.
9. **Fano** (50): the sparse minimax rate σ² s log(d/s)/n, and soft thresholding's upper bound.
10. **Matrix Bernstein** (51): a confidence ball for a covariance; why the log d.
11. **The lasso's oracle inequality** (52): the basic inequality, the cone, compatibility; what it does not give.
12. **A contraction rate** (53): Gaussian priors in the sequence model; the general theorem.

Candidacy goes on the Transcript, and the research stage begins (→ Part 56).

It keeps two promises:
- **Part 42**'s comprehensive exam asked you to compute, fit and interpret, and assumed the methods were correct. This
  exam proves them.
- **Parts 43–54** were taught one at a time. The exam needs them together, and the proof maps show where each proof
  borrows from another part (the lasso from Part 51's Gaussian maxima, the median from Part 30's robustness, the
  contraction rate from Part 50's bias–variance split).

**Built in this part:**
- **`statkit.qual`** ([`explainer/stats/kit/qual.py`](../../../explainer/stats/kit/qual.py)), tested in
  `tests/test_stats_kit_qual.py`: the numbers each problem needs:
  - Borel–Cantelli sums and exceedances; the walk stopped at +1 by exact dynamic programming, its first-passage law,
    ruin;
  - the Poisson UMVUE's exact variance against the Cramér–Rao bound and the MLE; Blyth's ratio in d dimensions;
  - the conditional test of two Poisson rates, its UMPU form and its unconditional size; local power in the logistic
    model, theory and simulation;
  - half-line brackets and the bracketing integral; the median's influence function and a Wald interval with a kernel
    plug-in;
  - Fano's bound with a nontrivial disjoint-support fallback packing; exact Gaussian soft-thresholding risk;
  - matrix Bernstein for a bounded covariance (mean bound, confidence radius, simulation); the lasso by coordinate
    descent against its oracle inequality; exact posterior contraction in the sequence model.
- **The PhD problem bank:** the twelve exam problems and six more, each with a full solution, below.
- **The proof map** (`ProofMap` in `explainer/stats/viz.py`), the part's instrument: a proof's moves as a chain of
  boxes joined by arrows, each tagged with the part whose tool it uses. `light(k)` lights a move, `done()` seals the
  chain.

**Data.**
- From the Museum: Snow's Table IX (1855) and Newcomb's 66 passage times (1882).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| conditional binomial test, unrandomized | equal Poisson rates, λ = 5 | 5% (size) | 2.28% | conservative |
| UMPU test (randomized, Neyman structure) | equal Poisson rates, λ = 5 | 5% (size) | 5.39% | kept |
| median ± 1.96 IF-based SE (KDE plug-in) | t₃ data, n = 66 | 95% | 96.8% | conservative |
| matrix-Bernstein ball for Σ | Rademacher vectors, d = 50, n = 400 | 95% | 100% | conservative |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats55.compute   # once (under a minute)
python tools/build.py stats55 -q l                         # fast 480p preview
python tools/build.py stats55                              # 1080p30 -> renders/stats55.mp4
python tools/qa_scene.py stats55 ExamTesting
python tools/lecture_length.py stats55 --floor 50
```

## Chapters

| # | Sitting | Numbers |
|---|---|---|
| 0 | Hilbert, and the night before | — |
| 1 | Probability | exceedances of c log n in 10⁶ draws: 0 (c = 2), 4, the last at n = 82,878 (1.2), 13 (1), 69 (0.8); M_n/log n 2.83 → 1.013; P(T ≤ 4,001) = 0.987, E[T ∧ 4,001] = 99.9; ruin with a = 3, b = 7: 0.3, E T = 21 |
| 2 | Estimation | n = 10, λ = 2: UMVUE variance 0.00406, CR bound 0.00366, MLE MSE 0.00460; Blyth's ratio at τ = 300: 0.0084 (d = 1), → 4π (d = 2) |
| 3 | Testing and asymptotics | Snow: t = 1,361, expected 824, observed 1,263, z = 24.4, one-sided exact upper-tail P ≈ 10⁻¹⁶³, rate ratio 8.40 (6.84, 10.43); unrandomized size 0.0004 (λ = 1), 0.022 (5), 0.040 (50); local power at h = 3: 0.535, 0.504, 0.442 (simulated 0.526, 0.505, 0.434) |
| 4 | Empirical processes and efficiency | ceiling-entropy upper integral 1.37; Newcomb: median 27 (25.5, 28.5), SE 0.77; mean 26.21 (23.6, 28.8), SE 1.32; without outliers 27.75; modern value 33 |
| 5 | Minimax and HDP | s = 10, n = 100: rate 0.33 → 1.02, exact soft-thresholding risk, largest of four signal sizes, 0.567 → 1.944, Fano 0.000352 → 0.002908 for d = 10² → 10⁵; d = 50, n = 400: mean error 0.76, 95th percentile 0.84, MP edge 0.83, Bernstein mean bound 1.25, radius 1.72 |
| 6 | The lasso and the posterior | p = 500, s = 5, n = 200: normalized columns: prediction error 1.978 (conditional reference 35.7), ℓ₁ error 3.146 (conditional reference 76); compatibility φ² ≥ 1/2 is not verified; contraction slopes −0.4995, −0.6628, −0.4227 against −1/2, −2/3, −2/5 |
| 7 | Outro | — |

## Sources

- **Problems.** D. Hilbert, *Bull. AMS* 8 (1902), the English translation of the 1900 address; D. Cox & D. Hinkley,
  *Problems and Solutions in Theoretical Statistics* (1978).
- **Probability.** R. Durrett, *Probability: Theory and Examples* (5th ed. 2019), ch. 2, 4; D. Williams, *Probability
  with Martingales* (1991).
- **Estimation and testing.** C. Blyth, *Ann. Math. Stat.* 22 (1951); C. Stein, *Proc. Third Berkeley Symp.* (1956);
  L. Brown, *Ann. Math. Stat.* 42 (1971); E. Lehmann & G. Casella, *Theory of Point Estimation* (1998); E. Lehmann &
  J. Romano, *Testing Statistical Hypotheses* (2005), ch. 4.
- **Asymptotics.** L. Le Cam, *Univ. Calif. Publ. Stat.* 3 (1960); J. Hájek, *Z. Wahrsch.* 14 (1970); A. van der
  Vaart, *Asymptotic Statistics* (1998), ch. 7, 8, 14, 19, 25.
- **Empirical processes.** M. Donsker, *Ann. Math. Stat.* 23 (1952); M. Ossiander, *Ann. Probab.* 15 (1987);
  A. Kolmogorov & V. Tikhomirov, *Uspekhi* 14 (1959); A. van der Vaart & J. Wellner, *Weak Convergence and Empirical
  Processes* (2nd ed. 2023).
- **High dimensions.** D. Donoho & I. Johnstone, *Biometrika* 81 (1994); A. Tsybakov, *Introduction to Nonparametric
  Estimation* (2009); P. Rigollet & J.-C. Hütter, *High-Dimensional Statistics* (lecture notes, 2023), Lemma 4.14;
  J. Tropp, *Found. Comput. Math.* 12 (2012); R. Vershynin, *High-Dimensional Probability* (2018); S. van de Geer, *Proc.
  JSM* (2007); P. Bickel, Y. Ritov & A. Tsybakov, *Ann. Stat.* 37 (2009); P. Bühlmann & S. van de Geer, *Statistics for
  High-Dimensional Data* (2011), ch. 6.
- **Bayesian asymptotics.** S. Ghosal, J. Ghosh & A. van der Vaart, *Ann. Stat.* 28 (2000); B. Knapik, A. van der
  Vaart & H. van Zanten, *Ann. Stat.* 39 (2011).
- **Data.** J. Snow, *On the Mode of Communication of Cholera* (2nd ed. 1855), Table IX; S. Newcomb (1891);
  S. Stigler, *Ann. Stat.* 5 (1977).

## The problem bank: the exam's twelve

1. **Exponential maxima.**
   - Upper: P(X_n > c log n) = n^{−c}, summable for c > 1, so by Borel–Cantelli I, X_n ≤ c log n for all large n a.s.
     Then M_n ≤ max(M_N, c log n), so limsup M_n/log n ≤ c. Intersect over c = 1 + 1/k.
   - Lower: P(M_n ≤ c log n) = (1 − n^{−c})ⁿ ≤ exp(−n^{1−c}), summable for c < 1, so M_n > c log n eventually. Intersect
     over c = 1 − 1/k. (Independence is used only here.)
2. **The walk stopped at +1.**
   - S_{T∧n} is a martingale, so E S_{T∧n} = 0. By reflection, P(T > 2k − 1) = C(2k, k)/4^k ~ (πk)^{−1/2} → 0, so T < ∞
     a.s. and S_T = 1, E S_T = 1.
   - E S_{T∧n} = P(T ≤ n) + E[S_n; T > n] = 0 forces E[S_n; T > n] → −1: the family is not uniformly integrable, and
     E T = Σ P(T > n) = ∞.
   - Stopped at −a or b: |S_{T∧n}| ≤ max(a, b), so 0 = E S_T = bp − a(1 − p), p = a/(a + b); and S_n² − n is a
     martingale with bounded-increment, integrable-time conditions satisfied, so E T = E S_T² = ab.
3. **The Poisson UMVUE.**
   - T = ΣX_i is complete sufficient. X₁ | T ~ Bin(T, 1/n), so E[1{X₁ = 0} | T] = (1 − 1/n)^T, unbiased, hence the
     UMVUE by Lehmann–Scheffé.
   - E s^T = e^{nλ(s−1)} with s = (1 − 1/n)² gives Var = e^{−2λ}(e^{λ/n} − 1) > λe^{−2λ}/n, the CR bound for g(λ) =
     e^{−λ} with I = n/λ.
   - For Bin(n, p), E g(X) is a polynomial of degree ≤ n in p, and 1/p is not: no unbiased estimator exists.
4. **Blyth's method.**
   - If δ′ dominated X, then R(θ, δ′) ≤ 1 − ε on an interval I, by continuity of risk.
   - Use the **unnormalized** density q_τ(θ) = e^{−θ²/(2τ²)} and integrated risk r(q,δ) = ∫R(θ,δ)q(θ)dθ. The Bayes rule is δ_τ = τ²X/(1+τ²); its integrated-risk advantage is √(2π)τ/(1+τ²).
   - Then ε∫_I q_τ ≤ r(q_τ,X)−r(q_τ,δ′) ≤ r(q_τ,X)−r(q_τ,δ_τ): the left side tends to ε|I|, the right to 0.
   - In d = 2 the product tends to 4π; X is still admissible there (Stein; Brown, with flatter priors), and
     inadmissible for d ≥ 3.
5. **Snow's Table IX.**
   - p(x, y) ∝ exp(x log(λ₁/λ₂) + (x + y) log λ₂): given T = t, X ~ Bin(t, ρe₁/(ρe₁ + e₂)).
   - Under H₀, T is complete for the nuisance rate, so similarity implies E₀(φ | T=t)=α. Unbiasedness also gives E₀[(X−tp₀)φ | T=t]=0. The UMPU rule rejects outside two boundaries with randomization chosen to satisfy both constraints, at p₀=e₁/(e₁+e₂). For Snow these boundaries are 788 and 859, with rejection probabilities 0.91136 and 0.40046; the observed X=1263 is rejected with probability one.
   - Snow: 1,263 of 1,361 against 824 expected: z = 24.4. The reported upper-tail probability is one-sided. Separately, inverting equal-tailed **unrandomized** binomial tests gives Clopper–Pearson; this is not inversion of the randomized UMPU rule. Mapping p ↦ ρ = (p/(1 − p))
     e₂/e₁ gives 8.40 (6.84, 10.43).
6. **Local power.**
   - ℓ̇ = tanh(x/2) = 2F − 1, I = ∫₀¹(2u − 1)² du = 1/3; the model is DQM, hence LAN.
   - By the third lemma a statistic jointly normal with Δ_n, with covariance c, has limit N(hc, ·) under h/√n.
   - Score: c = √I, power 1 − Φ(z_α − h/√3). t-test: 1 − Φ(z_α − h√3/π). Sign test: 1 − Φ(z_α − h/2). AREs 9/π² and
     3/4. The score test attains the envelope (Neyman–Pearson in the limit experiment).
7. **Half-lines.**
   - Brackets [1{x ≤ t_{j−1}}, 1{x ≤ t_j}] at quantiles with P-mass ≤ ε² have L₂(P) size ≤ ε; there are ⌈1/ε²⌉.
   - ∫₀¹ √(log N_[](ε)) dε < ∞, so the class is Donsker (Ossiander).
   - Hölder-α on [0, 1]^d has log N_[] ≍ ε^{−d/α}: the sufficient entropy integral is finite when α>d/2 under a regular reference law such as uniform measure. Divergence of this test alone is not a converse Donsker theorem.
8. **The median.**
   - Along dP_t = (1 + tg) dP, F_t(m_t) = 1/2. Differentiating: E[1{X ≤ m} g] + f(m) ṁ = 0, so ṁ = E[ψ̃ g] with
     ψ̃ = (1/2 − 1{x ≤ m})/f(m). For a unique median with a continuous positive density, bounded mean-zero scores define valid local paths, and their closure gives the tangent space L₂⁰(P), so ψ̃ is efficient; Var ψ̃ =
     1/(4f(m)²).
   - Newcomb: median 27, f̂ = 0.080, SE 0.77, 95% (25.5, 28.5); the mean 26.21, SE 1.32.
9. **Fano for sparse means.**
   - A packing ω₁, …, ω_M with |ω_j| = s, Hamming ≥ s/2, log M ≥ (s/8) log(1+d/(2s)). Disjoint supports alternatively give M≥⌊d/s⌋; use the larger log-cardinality lower bound to ensure log M>log 2 even for small s, for 1≤s≤d/8. With θ_j = δω_j: separation² ≥
     sδ²/2, KL ≤ nsδ²/σ².
   - Fano: risk ≥ (sδ²/8)(1 − (nsδ²/σ² + log 2)/log M); with δ² = σ²(log M − log 2)/(2ns), risk ≥ σ²(log M −
     log 2)²/(32 n log M).
   - Soft thresholding at σ√(2 log d/n) has risk ≤ (2 log d + 1)(s + 1)σ²/n: this log d upper bound is not uniformly equivalent to log(d/s) over every sparsity regime. A threshold tuned to known s through log(d/s) gives the sparse rate; the sharp constant two requires an appropriate sparse asymptotic regime.
10. **Matrix Bernstein.**
    - Σ̂ − I = ΣZ_i, Z_i = (x_ix_iᵀ − I)/n, ‖Z_i‖ ≤ d/n; (xxᵀ)² = d xxᵀ gives ΣE Z_i² = ((d − 1)/n) I.
    - P(‖ΣZ_i‖ ≥ t) ≤ 2d exp(−(t²/2)/(v + Lt/3)); E‖ΣZ_i‖ ≤ √(2v log 2d) + L log(2d)/3.
    - The ball: t_δ = Lc/3 + √((Lc/3)² + 2vc), c = log(2d/δ).
11. **The lasso.**
    - Basic inequality, the event ‖Xᵀε/n‖_∞ ≤ λ/2 and the triangle inequality give (1/2n)‖XΔ‖² + (λ/2)‖Δ_{Sᶜ}‖₁ ≤
      (3λ/2)‖Δ_S‖₁, so Δ is in the cone ‖Δ_{Sᶜ}‖₁ ≤ 3‖Δ_S‖₁.
    - Compatibility: ‖Δ_S‖₁ ≤ √s‖XΔ‖/(√n φ). Hence ‖XΔ‖/√n ≤ 3λ√s/φ, ‖XΔ‖²/n ≤ 9sλ²/φ², ‖Δ‖₁ ≤ 4‖Δ_S‖₁ ≤
      12sλ/φ².
    - P(max_j |X_jᵀε/n| > λ/2) ≤ 2p e^{−nλ²/8σ²} = δ for λ = 2σ√(2 log(2p/δ)/n).
12. **Contraction.**
    - θ_k | Y ~ N(w_kY_k, λ_k/(1 + nλ_k)); E Π(‖θ − θ₀‖² | Y) = Σ(1 − w_k)²θ₀k² + Σw_k²/n + Σλ_k/(1 + nλ_k).
    - Split at N = n^{1/(1+2α)}: variance + spread ≍ N/n; bias² ≲ B N^{−2 min(α, β)}. Both are O(ε_n²); the variance can be smaller when the prior oversmooths.
    - Posterior Markov and then data expectation give E_θ₀Π(‖θ−θ₀‖>M_nε_n | Y) ≤ E_θ₀∫‖θ−θ₀‖²dΠ/(M_n²ε_n²) ≲ M_n⁻² → 0. An unconditional second moment does not provide this bound for each conditional dataset.

## The problem bank: six more

1. **Summable tails.** For each ε, Borel–Cantelli gives |X_n − X| ≤ ε eventually a.s.; intersect over ε = 1/k.
2. **Wald's second identity.** M_n = S_{T∧n}² − (T ∧ n) is a martingale, so E S_{T∧n}² = E(T ∧ n). Monotone convergence
   on the right and bounded convergence on the left (|S_{T∧n}| ≤ max(a, b)) give E T = E S_T² = ab.
3. **The one-sided binomial test.** By Neyman–Pearson and the monotone likelihood ratio in x, reject for X > c and with
   probability γ at X = c, with P(X > c) < α ≤ P(X ≥ c) under p₀ and γ = (α − P(X > c))/P(X = c).
4. **Glivenko–Cantelli.** Half-lines pick out at most n + 1 subsets of n points, so the VC dimension is 1 (no two points
   are shattered: the larger cannot be picked without the smaller). The VC bound gives sup_t |F_n(t) − F(t)| ≲
   √(log n/n) → 0 in probability, and Borel–Cantelli on the exponential tail upgrades it to almost surely.
5. **Le Cam's two-point bound.** For any θ̂, let ψ = 1{|θ̂ − θ₁| < |θ̂ − θ₀|}. Then E₀|θ̂ − θ₀| + E₁|θ̂ − θ₁| ≥
   (|θ₀ − θ₁|/2)(P₀(ψ = 1) + P₁(ψ = 0)) ≥ (|θ₀ − θ₁|/2)(1 − TV(P₀, P₁)); the maximum is at least half the sum.
6. **A Beta posterior.** Beta(1 + k, 1 + n − k) has mean p̂ + O(1/n) and variance p̂(1 − p̂)/n + O(n⁻²); Chebyshev under
   the posterior and E|p̂ − p₀|² = p₀(1 − p₀)/n give E Π(|p − p₀| > M_n n^{−1/2} | X) ≲ M_n^{−2} → 0.

## Glossary

- **Probability.** Borel–Cantelli I and II; almost surely; eventually; infinitely often; stopped martingale; optional
  stopping; uniform integrability; reflection principle; gambler's ruin; Wald's identities.
- **Estimation and testing.** Complete sufficient statistic; Rao–Blackwell; Lehmann–Scheffé; UMVUE; Cramér–Rao;
  admissibility; Blyth's method; Bayes risk; similar test; Neyman structure; UMPU; randomized test; Clopper–Pearson.
- **Asymptotics and empirical processes.** DQM; LAN; third lemma; local power; power envelope; Pitman ARE; limit
  experiment; convolution theorem; bracket; bracketing entropy and integral; Donsker class; Brownian bridge.
- **Efficiency.** Path; score; tangent space; pathwise derivative; gradient; efficient influence function.
- **High dimensions.** Packing; sparse Varshamov–Gilbert; Fano's inequality; soft thresholding; oracle inequality;
  matrix Bernstein; matrix variance; ε-net; basic inequality; cone; compatibility; irrepresentability; beta-min;
  conjugate posterior; contraction rate; prior mass; sieve; tests.
- **The exam.** Exam card; proof map; candidacy.

## Where it comes back

- **Part 56**: inference after selection, where the lasso's chosen variables need honest intervals.
- **Part 57**: distribution-free inference, where no model at all is assumed.
- **Part 58**: optional stopping made safe, with test martingales and e-values.
- **Part 59**: the lasso and the posterior when p and n grow together.
- **Part 65**: the dissertation.

## QA reconciliation

Twenty-one checks pass (17 local cases and four legacy tests). All thirteen numerical inputs were regenerated. Independent checks compare soft-thresholding risk with Gaussian quadrature, UMPU power with constrained linear programs, first-passage quantities with enumerated paths, sequence tails with a longer evaluation, and lasso fits with KKT residuals and the cone inequality. Snow's nine Table IX entries agree with the original 1855 text transcription on Project Gutenberg; all 66 Newcomb values agree as a multiset with the independent MASS distribution.

The binomial UMPU computation uses stable tail probabilities and centered first moments rather than dividing by tiny or zero endpoint masses across every boundary pair. Its saved size and unbiasedness constraints are verified directly, including Snow's n=1361 slice and degenerate n=0,1 cases. The displayed one-sided exact tail, the randomized UMPU decision, and the conservative Clopper–Pearson interval have distinct definitions. Similarity alone is not enough for UMPU optimality: the centered first-moment constraint is explicit. Snow's rate ratio is interpreted under the stipulated Poisson/exposure model.

The lasso design now actually has squared column norms n, matching the Gaussian noise-event proof. All 180 fits have KKT residual below 1.2e−12. Prediction and l1 errors at n=200 are 1.9783 and 3.1459, with stored dataset Monte Carlo errors; the noise event occurs in 29 of 30 replications there. The dashed curves still use a reference compatibility squared of one half. This condition is not certified for the random designs, so these are explicitly conditional benchmarks, not validated confidence bounds for every fit. Prediction scales as 1/n, while the l1 benchmark scales as 1/√n. Support-recovery discussion distinguishes uniform/asymptotic conditions from pointwise necessity; beta-min depends on the active Gram inverse, penalty and noise, plus off-support dual control.

Sparse Fano uses either the sparse combinatorial packing or a disjoint-support packing, whichever gives the larger valid lower bound. This avoids a vacuous log-cardinality constant for small sparsity. The table uses the sparsity-dependent threshold, not the universal log d threshold. Gaussian truncated moments now evaluate its risk exactly, avoiding simulation noise in a maximum over four signal amplitudes. That grid maximum is not a supremum over the entire sparse class. Universal-threshold oracle bounds, known-sparsity rates and sharp sparse-asymptotic equivalents are stated separately.

The posterior proof puts data expectation outside both sides of Markov's inequality. Variance and spread are bounded by the claimed squared rate; they need not be of that exact order when bias dominates. The numerical truth k^(-3/2) is a boundary hyperrectangle sequence, in Sobolev classes strictly below one, and is not the Sobolev-one truth in the theorem. Numerical sums over 100,000 coordinates are augmented by certified upper/lower remainder bounds for all three nonnegative series. The plotted midpoint differs by at most half the saved interval width; the maximum relative full interval width is below 4.7e−7. Corrected fitted slopes are −0.4995, −0.6628 and −0.4227. The GGV sufficient conditions include KL and second log-likelihood moment control, model-specific tests in the chosen metric, compatible constants and nε² tending to infinity.

Finite exceedance counts do not identify an eventual last exceedance. Raw points and running maxima are retained rather than clamped to a plotting edge. The bounded stopping-time argument derives integrability of ruin time by monotone and bounded convergence rather than assuming it in a circular invocation of Wald's identity. Blyth's normalized versus unnormalized risk convention is consistent. Strict UMVUE/CR comparisons are scoped to positive lambda. The half-line ceiling-entropy integral is distinguished from a relaxed analytic upper bound, and finite covers alone are not called a proof of Donsker convergence. Hölder entropy rates are scoped to regular reference measures; failure of a sufficient entropy test does not itself prove a CLT failure.

The median's bounded influence gives a first-order contamination calculation, not a finite-sample one-point displacement bound. Replacing a point can have twice the one-contamination effect. Its efficient tangent space is mean-zero L2, obtained by closure of bounded scores. KDE intervals on rounded Newcomb observations assume an underlying continuous measurement law; they do not account for apparatus bias or automatically target a physical constant. The t3 coverage experiment does not establish a unique smoothing explanation or universal conservatism. Board rows use empirical dataset-level Monte Carlo errors; zero empirical error after no observed failures does not establish population coverage one.

LAN power envelopes are scoped to positive local alternatives and asymptotic null level. Normal-critical-value finite-sample t/sign simulations need not have exact nominal size, and their Monte Carlo errors are saved. The matrix expected-norm constant is justified through the exponential-moment argument, rather than simple integration of a tail at the same constants. Its reference ball uses this model's variance/norm bounds, not an arbitrary covariance. Matrix Bernstein explicitly depends on dimension; the net bound includes d/n as well as √(d/n); Marchenko–Pastur supplies a proportional-asymptotic edge, not a finite-sample quantile guarantee.

The exam retains persistent lifted problem cards and proof maps. Local clipping preserves viewport crossings and missing breaks. English endpoint/native/motion and representative narrated review remain pending. Chinese narration/captions, continuous listening and final masters remain open.
