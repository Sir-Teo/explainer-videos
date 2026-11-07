# Statistics, Built — Part 43: Measure-Theoretic Probability

Part 43 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first part of Stage IV, the PhD core. In 1900 Hilbert asked for axioms of
probability (his sixth problem), and in 1933 Kolmogorov supplied them, on top of Lebesgue's measure. This part:
- builds the axioms: σ-algebras, measures, random variables, integrals, products;
- develops proofs and proof outlines for the strong law, Lévy continuity and Lindeberg–Feller; presents Stein bounds and a cited Berry–Esseen constant;
- then looks beyond the normal: stable laws, large deviations and extremes.

It keeps three promises from Stage I:
- **Part 2** used elementary event spaces; Vitali rules out extending rotation-invariant length to every subset of the interval (with choice). Atomic probabilities can be defined on all subsets.
- **Part 3** said the MGF determines the law; this part proves it, and shows that moments alone do not.
- **Part 6** proved the CLT by MGFs and stated the strong law and the Berry–Esseen rate; this part develops the strong-law/CLT arguments and explains the approximation rates; the published 0.4748 constant is stated rather than derived.

**Built in this part:**
- **`statkit.limits`, the weak-convergence lab** ([`explainer/stats/kit/limits.py`](../../../explainer/stats/kit/limits.py)),
  tested in `tests/test_stats_kit_limits.py`:
  - **Distances:**
    - Kolmogorov, exact for a lattice law against a continuous one;
    - Lévy's metric;
    - Wasserstein-1;
    - the Lévy–Prokhorov distance, bracketed between Lévy's below and the Ky Fan distance of the quantile coupling above
      (Strassen);
    - total variation between binomial and Poisson laws, with Le Cam's bound.
  - **Exact laws of standardized sums:** binomial, Poisson and gamma; Borel's binary digits; the quantile transform;
    the Cantor function.
  - **Bounds:**
    - Berry–Esseen with Shevtsova's 0.4748;
    - the Stein/zero-bias Wasserstein bound ρ/√n;
    - Stein's identity and the solution of Stein's equation.
  - **Characteristic functions:** empirical, numerical inversion, and Lévy's tail bound.
  - **Heavy tails and large deviations:** the Chambers–Mallows–Stuck stable sampler; Hill's tail index; Cramér's rate
    as a Legendre transform, with the Bernoulli rate (a KL divergence) and exact binomial tails.
  - **Extremes:** GEV laws, the classical norming constants and the exact law of a normalized maximum.
  - **Series:** the random harmonic series and the three series.
- **The convergence lab** (`ConvergenceLab` in `explainer/stats/viz.py`), the part's instrument: a law against its limit
  on CDF axes, with the Kolmogorov gap, Lévy's box and the Wasserstein area drawn in.

**Data.**
- From the Museum:
  - Bortkiewicz's (1898) horse kicks;
  - Bernoulli's urn (*Ars Conjectandi*, 1713);
  - the DAX, 1991–1998 (R's `EuStockMarkets`);
  - Port Pirie's annual maximum sea levels, 1923–1987 (Coles 2001).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows, all nominal 90% t intervals for a mean:

| Setting | Achieved | Verdict |
|---|---|---|
| Uniform(0, 1), n = 10 | 89.8% | kept |
| Exp(1), n = 10 | 85.6% | broken |
| Exp(1), n = 100 | 89.2% | broken (studentization/skewness; the leading CDF term cancels for symmetric two-sided coverage) |
| Exp(1), n = 1,000 | 89.9% | kept |
| Pareto, α = 2.5 (finite variance), n = 100 | 83.7% | broken |
| Pareto, α = 1.5 (infinite variance), n = 1,000 | 70.4% | broken in this simulation; Gaussian studentization is not asymptotically justified |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats43.compute   # once (under a minute)
python tools/build.py stats43 -q l                         # fast 480p preview
python tools/build.py stats43                              # 1080p30 -> renders/stats43.mp4
python tools/qa_scene.py stats43 Stein
python tools/lecture_length.py stats43 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Hilbert's sixth problem | 1900; the *Grundbegriffe*, 1933 |
| 1 | σ-algebras and measures | Vitali; the Cantor set's length (2/3)^k → 0 |
| 2 | Random variables as measurable maps | binary digits: shares 0.496–0.504; three 1s 0.127 |
| 3 | Integration | E X_n = 1, lim = 0; 1/X̄ consistent with infinite mean |
| 4 | Independence and products | the double series 0 ≠ 1 |
| 5 | Borel–Cantelli and the 0–1 laws | longest run 19.6 in 2^20 tosses |
| 6 | The strong law | ±1/j settles (0.0025); ±1/j^0.4 wanders |
| 7 | Weak convergence | Bin(10): Kolmogorov 0.123, Lévy 0.088, W 0.159; horse kicks pooled χ²₁ 0.063 |
| 8 | Characteristic functions | inversion to 0.0008; Heyde's equal moments |
| 9 | Lindeberg–Feller | KS 0.003 vs 0.057 (L_n = 0.75) |
| 10 | Stein's method and the rates | slopes −0.497 to −0.500; 84% vs 14% of the bound |
| 11 | Infinitely divisible and stable laws | c = 2.507; DAX kurtosis 6.3 → 1.2 → 0.36 |
| 12 | Large deviations | Bernoulli 25,550; Chernoff 9,171; CLT 6,498; safe at every later size from 6,520 |
| 13 | Extremes | 0.028 → 0.0003 vs 0.064 → 0.035; Port Pirie ξ̂ = −0.05, 100-year 4.69 m |
| 14 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Chapter 1.**
  - Vitali's set: rational shifts of one point from each class tile [0, 1), so no shift-invariant countably additive
    length exists on all subsets.
  - Then the Borel σ-algebra, the π–λ theorem (a CDF determines its law), and Carathéodory's extension.
  - The Cantor function is a singular CDF, completing Part 2's promise of Lebesgue's decomposition.
- **Chapter 2.** A random variable is a measurable map and its law a push-forward. One uniform yields infinitely many
  coins, hence any i.i.d. sequence; σ(X) is information (Doob–Dynkin).
- **Chapter 3.**
  - The layer-cake formula; MCT, Fatou, DCT.
  - Counterexamples: the escaping bump (E X_n = 1, X_n → 0); the typewriter (in L¹ but nowhere almost surely);
    X_n = n with probability 1/n (not UI).
  - Vitali's convergence theorem. A consistent estimator, 1/X̄ for Poisson data, has infinite expectation at every n.
- **Chapter 4.**
  - Independence of σ-algebras; Tonelli and Fubini.
  - The array a_mm = 1, a_m,m+1 = −1 sums to 0 by rows and to 1 by columns.
  - Kolmogorov's extension theorem; likelihoods as Radon–Nikodym derivatives.
- **Chapter 5.**
  - Borel–Cantelli I and II. Erdős–Rényi: the longest run of heads ≈ log₂ n (19.6 in 2^20 tosses).
  - The typing monkey: 27^−9 per block.
  - Kolmogorov's 0–1 law; Hewitt–Savage and Pólya's recurrence.
- **Chapter 6.**
  - The strong law and its converse (E|X| = ∞ ⇒ limsup |X̄_n| = ∞).
  - Kolmogorov's maximal inequality and three-series theorem: ±1/j converges (tail movement 0.0025); ±1/j^0.4 diverges.
  - Etemadi's four-step proof (pairwise independence suffices); Cauchy running means never settle.
- **Chapter 7.**
  - The portmanteau theorem. The lab's four distances for standardized binomials:

    | n | Kolmogorov | Lévy | Prokhorov ≤ (Ky Fan) | Wasserstein |
    |---|---|---|---|---|
    | 4 | 0.1875 | 0.1341 | 0.3357 | 0.2571 |
    | 10 | 0.1230 | 0.0880 | 0.2409 | 0.1594 |
    | 40 | 0.0627 | 0.0448 | 0.1367 | 0.0792 |
    | 160 | 0.0315 | 0.0225 | 0.0733 | 0.0395 |

  - Skorokhod's representation; tightness, Prokhorov and Helly (N(0, n²) loses its mass).
  - Bortkiewicz: 122 deaths in 200 corps-years, λ̂ = 0.61, pooled χ²₁ = 0.0628 (approximate p = 0.802), combining counts ≥ 2 before the reference test. Le Cam:
    d_TV(Bin(n, λ/n), Poi(λ)) = 0.0311, 0.0073, 0.0014 at n = 5, 20, 100, under λ²/n = 0.074, 0.019, 0.0037.
- **Chapter 8.**
  - Characteristic functions; inversion (the triangle recovered to 0.0008).
  - The MGF determines the law when finite near 0 (analytic continuation).
  - Heyde's f(x)[1 + 0.8 sin(2π log x)] has the lognormal's moments 1.6487, 7.3891, 90.017, 2980.96.
  - Lévy's continuity theorem via the tail bound (Cauchy, u = 1: 0.736 ≥ 0.295); Cramér–Wold.
- **Chapter 9.**
  - Lindeberg's theorem and Feller's converse; the replacement proof with its two Taylor remainders.
  - 20 equal uniforms: KS 0.003. Twenty signs with Var X_k = 4^k: the last holds 75% of the variance, L_n(1/2) → 0.75, and
    the limiting law is uniform (binary digits); each finite sum is on a lattice, KS 0.057.
- **Chapter 10.**
  - Stein's identity and equation; d_W ≤ ρ/√n; Berry–Esseen with C = 0.4748.
  - Exact Kolmogorov slopes: coin −0.497, coin(0.1) −0.496, Poisson −0.498, exponential −0.500. They reach 84%, 65%,
    32% and 14% of the bound.
  - At n = 30 the exponential is within 0.024 (bound 0.209), yet t intervals undercover.
- **Chapter 11.**
  - Lévy–Khintchine; stable laws; the generalized CLT.
  - Symmetric Pareto(3/2) sums: the characteristic function approaches exp(−2.507|t|^{3/2}) at rate n^{−1/3}.
  - DAX: 1,859 returns, kurtosis 6.3, 0.32% of days beyond 4 SD (normal 0.0063%), Hill α̂ 3.5–4.4. Complete nonoverlapping 5- and 20-day blocks (371 and 92) have sample excess kurtosis 1.234 and 0.372. Residual days are discarded.
- **Chapter 12.**
  - Chernoff and Cramér; the Bernoulli rate is KL(a‖p).
  - Bernoulli's urn (p = 0.6, ±0.02, 1000:1): exact 6,520 draws; CLT 6,498; Chernoff 9,171; Bernoulli 25,550.
  - Sanov.
- **Chapter 13.**
  - Max-stability and the Fisher–Tippett–Gnedenko theorem with its proof.
  - Exact distances: exponential = Pareto = uniform = 0.0280, 0.0027, 0.00027 at n = 10, 100, 1,000 (each is
    (1 − t/n)^n vs e^{−t}); the normal 0.064 → 0.035 at n = 10^5.
  - Port Pirie: ξ̂ = −0.050, μ̂ = 3.87, σ̂ = 0.198; the 100-year level is 4.69 m (Gumbel 4.77 m); the record 4.69 m
    (1934).

## Sources

- **Foundations.**
  - D. Hilbert, *Bull. AMS* 8 (1902, transl. of the 1900 address); A. N. Kolmogorov, *Grundbegriffe der
    Wahrscheinlichkeitsrechnung* (1933).
  - G. Vitali (1905); H. Lebesgue (1902); C. Carathéodory (1914); É. Borel, *Rend. Circ. Mat. Palermo* 27 (1909).
- **Laws of large numbers and 0–1 laws.**
  - A. N. Kolmogorov, *Math. Ann.* 99 (1928), 102 (1929); N. Etemadi, *Z. Wahrsch.* 55 (1981).
  - E. Hewitt & L. Savage, *Trans. AMS* 80 (1955); P. Erdős & A. Rényi, *J. Analyse Math.* 23 (1970); G. Pólya,
    *Math. Ann.* 84 (1921).
- **Weak convergence and characteristic functions.**
  - P. Lévy, *Calcul des probabilités* (1925); H. Cramér & H. Wold, *J. London Math. Soc.* 11 (1936).
  - Y. Prokhorov, *Theory Probab. Appl.* 1 (1956); A. Skorokhod, *Theory Probab. Appl.* 1 (1956).
  - C. Heyde, *JRSS B* 25 (1963); L. Le Cam, *Pacific J. Math.* 10 (1960); L. Bortkiewicz, *Das Gesetz der kleinen
    Zahlen* (1898).
- **The CLT and its rate.**
  - J. W. Lindeberg, *Math. Z.* 15 (1922); W. Feller, *Math. Z.* 40 (1935).
  - C. Stein, *Proc. Sixth Berkeley Symp.* 2 (1972); L. Goldstein, *J. Appl. Probab.* 47 (2010).
  - L. Chen, L. Goldstein & Q.-M. Shao, *Normal Approximation by Stein's Method* (2011); I. Shevtsova, arXiv:1111.6554
    (2011).
- **Beyond the normal.**
  - B. Mandelbrot, *J. Business* 36 (1963); J. Chambers, C. Mallows & B. Stuck, *JASA* 71 (1976); B. Hill, *Ann. Stat.*
    3 (1975).
  - H. Cramér, *Actualités Sci. Indust.* 736 (1938); I. Sanov, *Mat. Sb.* 42 (1957); A. Dembo & O. Zeitouni (2nd ed.
    1998).
  - R. A. Fisher & L. Tippett, *Proc. Camb. Phil. Soc.* 24 (1928); B. Gnedenko, *Ann. Math.* 44 (1943); S. Coles (2001).
- **Books.**
  - R. Durrett, *Probability: Theory and Examples* (5th ed. 2019); P. Billingsley, *Probability and Measure* (3rd ed.
    1995).
  - O. Kallenberg, *Foundations of Modern Probability* (3rd ed. 2021); D. Williams, *Probability with Martingales*
    (1991).

## Problems and solutions

1. **Rational half-lines generate the Borel sets.**
   - Let 𝒢 = σ{(−∞, q] : q ∈ ℚ}.
   - For real x, (−∞, x] = ⋂_{q ∈ ℚ, q > x} (−∞, q], a countable intersection, so it lies in 𝒢.
   - Hence (a, b] = (−∞, b] ∖ (−∞, a] ∈ 𝒢, and every open set is a countable union of such intervals, so 𝓑 ⊆ 𝒢.
   - The reverse inclusion is clear.
2. **The tail formula.**
   - X = ∫₀^∞ 1(X > t) dt pointwise.
   - Tonelli on Ω × [0, ∞) (a non-negative integrand) gives E X = ∫₀^∞ E 1(X > t) dt = ∫₀^∞ P(X > t) dt.
3. **Summable deviations.**
   - By Borel–Cantelli I, for each ε = 1/k, |X_n − X| > 1/k only finitely often, almost surely.
   - Intersecting over k (countably many null sets) gives X_n → X almost surely.
   - For convergence in probability, choose n_k with P(|X_{n_k} − X| > 2^{−k}) < 2^{−k}. This gives an almost surely
     convergent subsequence.
4. **Lindeberg for i.i.d. summands.**
   - With s_n² = nσ², L_n(ε) = E[X² 1(|X| > εσ√n)]/σ².
   - The integrand tends to 0 pointwise and is dominated by X², which is integrable, so L_n → 0 by DCT.
5. **Two Cramér rates.**
   - N(μ, σ²): Λ(t) = μt + σ²t²/2, so I(a) = sup_t (ta − μt − σ²t²/2) = (a − μ)²/(2σ²). The CLT's quadratic is exact
     here.
   - Poisson(λ): Λ(t) = λ(e^t − 1). The maximizer is t = log(a/λ), so I(a) = a log(a/λ) − a + λ.
6. **An exponential maximum's distance from the Gumbel law.**
   - (M_n − log n ≤ x) has probability (1 − e^{−x}/n)^n. With t = e^{−x}, this is (1 − t/n)^n = e^{n log(1 − t/n)}
     = e^{−t}(1 − t²/(2n) + O(n^{−2})).
   - So the gap is e^{−t} t²/(2n) + O(n^{−2}), maximized at t = 2: 2e^{−2}/n ≈ 0.271/n.
   - That gives 0.0271 at n = 10, against the exact 0.0280 in chapter 13's table, and 0.00271 at n = 100 (exact
     0.0027).

## Glossary

- **The foundations.**
  - σ-algebra; Borel sets; measure; probability space; π-system, λ-system; outer measure: the axioms' vocabulary.
  - Measurable map; law (push-forward); generated σ-algebra; filtration: random variables.
- **Integration and products.**
  - Simple function; Lebesgue integral; MCT, Fatou, DCT; uniform integrability; Vitali's theorem: integration.
  - Product measure; Tonelli, Fubini; Kolmogorov's extension theorem; Radon–Nikodym derivative: products and
    densities.
- **Limits of sequences.**
  - Limsup of events; Borel–Cantelli; tail σ-algebra; 0–1 law; exchangeable (symmetric) events: infinitely often.
  - Strong law; maximal inequality; three-series theorem; truncation: almost sure limits.
- **Weak convergence.**
  - Portmanteau; Kolmogorov, Lévy, Wasserstein, Lévy–Prokhorov and total-variation distances; coupling; Ky Fan
    distance; Skorokhod representation; tightness; Prokhorov's theorem; Helly selection: weak convergence.
  - Characteristic function; inversion; Lévy's continuity theorem; Cramér–Wold: transforms.
  - Triangular array; Lindeberg and Lyapunov conditions; Feller's converse; Stein's identity and equation; zero-bias
    coupling; Berry–Esseen: the CLT and its rate.
- **Beyond the normal.**
  - Infinitely divisible; Lévy measure; stable law; domain of attraction; regular variation; tail index: other limits.
  - Rate function; Legendre transform; Chernoff bound; Sanov's theorem: large deviations.
  - Max-stable; GEV; Gumbel, Fréchet, Weibull; return level: extremes.

## Where it comes back

- **Part 44**: conditional expectation, martingales, the ergodic theorem, Brownian motion.
- **Part 45**: sufficiency as a σ-algebra.
- **Part 46**: Stein's lemma and the KL exponent of tests.
- **Part 47**: the delta method and Edgeworth expansions, proved.
- **Part 48**: Donsker's theorem: weak convergence of whole processes.


## Scientific conditions and verification

The weak-lab binomial distances use lattice extrema, analytic normal quantile-cell integrals and bisection. The Prokhorov upper bound integrates the entire continuous quantile coupling rather than treating a finite quantile grid as a certified bound. General kit distance routines are grid approximations; gamma distances in the rate lab retain their numerical-grid interpretation. The maximum-distance table optimizes continuous CDF differences from exact distribution formulas; numerical tolerance remains.

For the urn, the event is the inclusive deviation |K/n − 3/5| ≥ 1/50. Integer arithmetic defines its boundaries. The first individually admissible size is 6,481, but lattice oscillations cause some later sizes to fail. The size safe for **every** larger n is 6,520: all sizes were checked through 9,171 and the monotone Chernoff envelope certifies the remainder. This replaces an arbitrary handful of later spot checks. The normal approximation remains 6,498; Bernoulli's historical bound is 25,550.

The SLLN converse uses every integer jump threshold; the Etemadi argument defines truncated sums and uses convergence of their expectations. The Lindeberg replacement proof operates on summands already divided by their total standard deviation. The converse needs Feller's maximal-variance condition. For symmetric two-sided t intervals the leading even-in-z studentized Edgeworth term cancels, so regular coverage error is generally O(1/n), despite the O(1/√n) one-sided CDF correction.

Stable domains generally need centering, slowly varying normalization and tail balance; pure n^(1/alpha) normalization is specific to examples such as the symmetric Pareto law. Hill estimates do not establish finite variance or a CLT for dependent DAX returns. Cramer needs an MGF near zero; Sanov gives interior/closure rate bounds, with equality for suitable rate-continuity sets. Bounded support alone does not establish an extreme-value domain. The displayed classical normal-maximum norming has logarithmic/log-log corrections; a universal pure 1/log(n) rate is not claimed.

The Port Pirie return level is a stationary fitted-model estimate with 1% annual exceedance probability, with parameter uncertainty unquantified in this illustration; it is not a guarantee about the next century. Stationarity, dependence and extreme-value model adequacy are the relevant assumptions. The course does not infer these assumptions from plotting annual maxima. [Scientific QA evidence](../../../docs/qa/evidence/stats43-polish-20261107/source-review.md) records computations, tests and primary data scope. Chinese narration/captions, continuous listening/playback and final narrated masters remain open.
