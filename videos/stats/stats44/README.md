# Statistics, Built — Part 44: Martingales, Markov Chains and Brownian Motion

Part 44 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the second part of Stage IV, the PhD core. In 1913 Andrei Markov counted the
vowels and consonants in the first 20,000 letters of Pushkin's *Eugene Onegin* to show that the law of large numbers
does not need independence. This part builds the theory of randomness that unfolds in time:
- conditional expectation, martingales, optional stopping, Ville's inequality and martingale convergence;
- concentration (Azuma, McDiarmid, Freedman) and the martingale CLT;
- Markov chains on general spaces, with drift, minorization, coupling and mixing times;
- Brownian motion, Donsker's invariance principle, the law of the iterated logarithm, and counting processes.

It keeps promises from earlier parts:
- **Part 17** used AR(1) and the unit root; chapter 7 gives the martingale CLT behind the first and chapter 11 the
  Dickey–Fuller law behind the second.
- **Part 27** used MCMC standard errors and R-hat; chapters 8 and 9 prove when a chain's average obeys a CLT.
- **Part 40** used Greenwood's formula and the log-rank test; chapter 13 shows the martingales underneath.
- **Part 43** warned that Kolmogorov's extension theorem cannot see continuity; chapter 10 builds Brownian motion
  directly.

**Built in this part:**
- **`statkit.chains`** ([`explainer/stats/kit/chains.py`](../../../explainer/stats/kit/chains.py)), tested in
  `tests/test_stats_kit_chains.py`:
  - **Markov's chain:** the two-state fit with stationary law and lag-1 correlation; the variance of block counts
    under a chain.
  - **Mixing:** total variation; stationary laws; the lazy walk on a cycle and on the hypercube (exactly, by Hamming
    weight); distance-to-stationarity curves and mixing times; spectral gaps; the coupling time on the cycle; the
    Bayer–Diaconis exact total variation of riffle shuffles, by Eulerian numbers.
  - **Martingales and walks:** Pólya's return probabilities; gambler's ruin and its expected duration; betting
    (likelihood-ratio) paths; the Azuma and McDiarmid bounds; Pólya's urn.
  - **Brownian motion:** Schauder functions and the Lévy–Ciesielski construction; quadratic and total variation;
    the Dickey–Fuller law by simulation; the LIL envelope.
  - **MCMC and AR(1):** batch-means standard errors; AR(1) least squares with an intercept; a random-walk Metropolis
    chain on N(0, 1).
- **The betting paths** (`BettingPaths` in `explainer/stats/viz.py`), the part's instrument: a fan of likelihood-ratio
  (wealth) paths on a log scale, with Ville's threshold 1/α drawn in and the paths that cross it lit up.

**Data.**
- From the Museum:
  - Pushkin's *Eugene Onegin*: the first 20,000 Cyrillic letters, as vowels and consonants
    (`explainer/stats/data/onegin_vc.txt`, rebuilt from the text on lib.ru). It gives 8,639 vowels, 1,109 vowel–vowel and
    3,831 consonant–consonant pairs, against Markov's 8,638, 1,104 and 3,827 (his table is in `museum.MARKOV_1913`).
  - The 6-MP trial's placebo arm (Freireich et al. 1963, via Gehan 1965).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| AR(1) least squares, 90% interval for φ | φ = 0.5, n = 200 | 89.7% | kept |
| AR(1) least squares, 90% interval for φ | φ = 0.98, n = 100 | 70.5% | broken (near a unit root) |
| MCMC mean, batch-means SE, 90% | RWM on N(0, 1), 20,000 steps | 90.5% | kept |
| MCMC mean, i.i.d. SE, 90% | RWM on N(0, 1), 20,000 steps | 27.3% | broken |
| betting test, reject at wealth 10 (size 10%) | a fair coin watched for 1,000 tosses | 8.9% false alarms | kept |
| z test at every 10th toss (size 10%) | a fair coin watched for 1,000 tosses | 59.9% false alarms | broken |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats44.compute   # once (a few minutes)
python tools/build.py stats44 -q l                         # fast 480p preview
python tools/build.py stats44                              # 1080p30 -> renders/stats44.mp4
python tools/qa_scene.py stats44 Maximal
python tools/lecture_length.py stats44 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Markov counts the vowels of *Onegin* | P(V \| V) = 0.128, P(V \| C) = 0.663; π = 0.432; block variance 5.25 vs 24.5 (i.i.d.) and 7.56 (chain) |
| 1 | Conditional expectation | Borel's paradox: 6,460 wedge points vs 10,065 geodesic-band points approaching the same half-meridian |
| 2 | Martingales | likelihood ratios: median wealth 1.4 × 10⁻⁹ after 1,000 tosses, theoretical mean 1 (Monte Carlo 0.98 at 20 tosses); finite-urn calibrated KS p = 0.7421 |
| 3 | Optional stopping | roulette 10 → 20: 0.259; 50 → 100: 0.0051; 100 → 200: 2.7 × 10⁻⁵; doubling: ruin 0.0016, EV −0.67 |
| 4 | Maximal inequalities and Ville | 8.2% of 4,000 null paths ever reach wealth 10 (≤ 10%) |
| 5 | Martingale convergence | upcrossings; Pólya's urn settles; reverse martingales and the strong law |
| 6 | Martingale concentration | empty bins: mean 367.7, SD 9.9; McDiarmid scale proxy ≈ 16, not the actual SD |
| 7 | The martingale CLT | AR(1): φ = 0.5 covered 89.9%, skew −0.22; φ = 0.98 covered 70.0%, skew −1.25 |
| 8 | Markov chains on general spaces | RWM: τ = 23; SE 0.0022 (i.i.d.) vs 0.0104 (batch means) |
| 9 | Coupling and mixing | cycle n = 20: t_mix 38, relaxation 40.9; hypercube t_mix 16 (d = 10), 91 (d = 40); 7 shuffles: TV 0.334 |
| 10 | Brownian motion | Σ(ΔB)² = 0.911 at 1,024 pieces, 0.992 at 65,536; Σ\|ΔB\| = 24.5 → 203.7 |
| 11 | Donsker's invariance principle | reflection 0.311 vs 0.317; Dickey–Fuller 5% point −1.95; 68% of t's negative |
| 12 | The law of the iterated logarithm | ratios of the running maximum to √(2n log log n): 0.76–1.27 |
| 13 | Counting processes | 200 lifetimes, 118 events; 6-MP placebo Nelson–Aalen 3.53 (SE 1.25) at 23 weeks |
| 14 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Hook.** Markov's fitted chain has lag-1 correlation −0.53: vowels avoid vowels. The variance of the vowel count in
  200 blocks of 100 letters is 5.25, a fifth of the i.i.d. 24.5 and close to the chain's 7.56. Markov reported
  dispersion ratios of 0.208 and about 0.3; the rebuilt text gives 0.214 and 0.308.
- **Chapter 1.**
  - E[X | 𝒢] is defined by Radon–Nikodym (Kolmogorov 1933) and, in L², is the orthogonal projection onto
    𝒢-measurable variables: the best predictor.
  - The tower property, taking out what is known, and the conditional variance decomposition.
  - Borel's paradox: the same half-meridian {y = 0, x > 0}, with angle φ = atan2(z, x), is approached by a longitude wedge or a geodesic band. Their limiting angle densities are cos(φ)/2 and 1/π on (−π/2, π/2). The limiting set alone does not specify a conditional law. A regular conditional law is only unique almost everywhere in the conditioning value.
- **Chapter 2.**
  - Martingales, sub- and supermartingales; the Doob decomposition into a martingale and a predictable compensator.
  - Under the null, a likelihood ratio is a martingale with mean one, yet almost every path goes to zero (KL 0.0204
    per toss): the mean is carried by rare large paths.
  - Pólya's urn: its bounded share martingale has a Beta(1,1) limit. The figure uses 24 long paths and 2,000 independent urns at 600 draws. At that finite horizon the 601 possible shares are exactly uniform on a lattice. The KS distance is 0.0146847, calibrated against that law with 9,999 multinomial null runs: p = 0.7421 (Monte Carlo SE 0.00438), not evidence proving a limit theorem.
- **Chapter 3.**
  - Optional stopping holds for bounded stopping times; for uniformly integrable stopped martingales at an almost surely finite time; or for uniformly bounded increments with E τ < ∞. Integrable increments alone are insufficient.
  - Fair ruin: P(reach b) = a/b and E τ = a(b − a): 100, 2,500 and 10,000 spins.
  - Unfair ruin by de Moivre's martingale (q/p)^S.
  - Doubling with a 1,023-unit bank and 10 losing bets (1 through 512): ruin probability 0.0016 at roulette odds, EV −0.67. Without a
    bank limit, the needed credit has median 1 but maximum 1,048,575 in 200,000 independent strategy cycles.
- **Chapter 4.**
  - Doob's maximal inequality and Doob's L² inequality.
  - Ville (1939): for a nonnegative martingale with mean one, P(sup M ≥ 1/α) ≤ α. This gives anytime-valid tests:
    the betting paths stay valid under continuous monitoring.
  - E-values and p-values: 1/max₀≤k≤n M_k is an anytime-valid p-value including M₀ = 1; a current reciprocal must be capped at 1. Products require independent or conditionally valid factors. Continuing the same valid process differs from selecting a new bet after observing its result.
- **Chapter 5.** The upcrossing inequality gives convergence of L¹-bounded martingales almost surely; uniform
  integrability gives L¹ convergence. Lévy's upward theorem uses the sigma-algebra generated by all finite information sets. Reverse-martingale convergence proves the iid integrable strong law. De Finetti additionally needs conditional factorization of all bounded indicator products, outlined here.
- **Chapter 6.**
  - Azuma–Hoeffding for bounded differences.
  - McDiarmid's bounded-difference inequality, with constant 2 from Hoeffding's lemma on a known range.
  - Freedman's Bernstein-type inequality, which uses the predictable variation.
- **Chapter 7.**
  - McLeish's martingale CLT: conditional variances converge in probability and a conditional Lindeberg condition
    holds.
  - For the AR(1) score Σ x_{t−1}ε_t it gives √n(φ̂ − φ) ⇒ N(0, 1 − φ²). For every fixed |φ| < 1 it remains valid under the stationary moment assumptions. At φ = 0.98 and n = 100 the approximation is poor; a unit root or local-to-unity sequence changes the normalization and limit.
- **Chapter 8.**
  - Harris chains; small sets and minorization; Foster–Lyapunov drift conditions.
  - With psi-irreducibility, aperiodicity, the small-set drift/minorization conditions and Eπ|f|^(2+δ) < ∞, the MCMC CLT has variance σ²τ. The displayed τ is a positive-lag truncation at 60, and the 30-batch SE is a finite approximation. Consistency of batch means needs both batch length and number to grow.
  - Mengersen–Tweedie: random-walk Metropolis is geometrically ergodic only for light-tailed targets.
- **Chapter 9.**
  - Total variation; the coupling inequality.
  - The lazy cycle of 20 mixes in about n² steps; the hypercube in about (d/2) log d.
  - The spectral gap bounds the relaxation time.
  - Bayer–Diaconis: the riffle-shuffle distances fall off a cliff near (3/2) log₂ 52; after 7 shuffles TV = 0.334.
  - Pólya's recurrence: returns within 10⁴ steps 0.987 in 1D, 0.713 in 2D, 0.327 in 3D (limit 0.3405).
- **Chapter 10.**
  - Lévy–Ciesielski: Schauder tents built on Haar wavelets converge uniformly.
  - Scaling; nowhere differentiability (Paley–Wiener–Zygmund 1933); three martingales.
  - Exit problems: P = b/(a + b), E τ = ab.
  - Quadratic variation 1, total variation infinite.
- **Chapter 11.**
  - Donsker (1951): centered iid walks with finite positive variance, standardized by σ√n, converge as step paths in D[0,1] with J₁ topology, or as linearly interpolated paths in C[0,1]. Functionals must be continuous at almost every Brownian path.
  - The reflection principle: P(max ≥ 1) = 2P(B₁ ≥ 1) = 0.317, simulated 0.311.
  - The Brownian bridge and Kolmogorov–Smirnov (to Part 48).
  - The Dickey–Fuller statistic converges to a functional of Brownian motion: with neither an intercept nor a trend its 5% point is about −1.95 (ρ form −8.06), versus −1.645 for a standard normal. Adding an intercept gives about −2.86. The derivation also needs Σ ε²/n → σ² by the LLN; Donsker alone does not give the stochastic-integral limit.
- **Chapter 12.**
  - Khinchin (1924): limsup S_n/√(2n log log n) = 1 almost surely.
  - Strassen's functional law; the proof by exponential maximal bounds and Borel–Cantelli on geometric blocks.
  - For sample-mean-centered intervals with a root-n asymptotic boundary, all-time coverage requires an iterated-logarithm factor; this is not a universal claim about every test or interval shape. The plotted finite-window maxima do not converge to 1 as the endpoint increases with a fixed initial cutoff.
- **Chapter 13.**
  - N − Λ is a martingale with predictable variation Λ (Aalen 1978), the Doob–Meyer decomposition.
  - Nelson–Aalen targets H*(t) = ∫₀ᵗ1{Y(s)>0}λ(s)ds. Its predictable bracket uses the true hazard; Σ d/Y² estimates that bracket. Recorded-week ties use the grouped-event convention.
  - The log-rank statistic is a martingale integral.
  - Rebolledo's CLT requires a deterministic continuous bracket limit and Lindeberg/small-jump control. It supports normalized KM/NA estimators, log-rank scores and regular Cox coefficient estimates under independent censoring, predictable entry, adequate risk sets and their other regularity conditions.

## Sources

- **Markov and the dependent law of large numbers.**
  - A. A. Markov, *Izv. Fiz.-Mat. Obshch. Kazan* 15 (1906); *Bull. Acad. Imp. Sci. St.-Pétersbourg* 7 (1913),
    transl. *Science in Context* 19 (2006).
  - B. Hayes, "First links in the Markov chain", *American Scientist* 101 (2013).
- **Conditional expectation and martingales.**
  - A. N. Kolmogorov (1933); É. Borel, *Éléments de la théorie des probabilités* (1909).
  - J. Ville, *Étude critique de la notion de collectif* (1939); J. L. Doob, *Stochastic Processes* (1953).
  - G. Pólya, *Math. Ann.* 84 (1921); F. Eggenberger & G. Pólya, *Z. Angew. Math. Mech.* 3 (1923).
- **Concentration and the martingale CLT.**
  - K. Azuma, *Tôhoku Math. J.* 19 (1967); W. Hoeffding, *JASA* 58 (1963); C. McDiarmid, *Surveys in Combinatorics*
    (1989).
  - D. Freedman, *Ann. Probab.* 3 (1975); D. McLeish, *Ann. Probab.* 2 (1974); P. Hall & C. Heyde, *Martingale Limit
    Theory and Its Application* (1980).
  - H. B. Mann & A. Wald, *Econometrica* 11 (1943); D. Dickey & W. Fuller, *JASA* 74 (1979).
- **Markov chains and mixing.**
  - S. Meyn & R. Tweedie, *Markov Chains and Stochastic Stability* (2nd ed. 2009); K. Mengersen & R. Tweedie,
    *Ann. Stat.* 24 (1996).
  - G. Roberts & J. Rosenthal, *Probab. Surveys* 1 (2004); C. Geyer, *Stat. Sci.* 7 (1992).
  - D. Bayer & P. Diaconis, *Ann. Appl. Probab.* 2 (1992); D. Levin, Y. Peres & E. Wilmer, *Markov Chains and Mixing
    Times* (2nd ed. 2017).
- **Brownian motion and Donsker.**
  - N. Wiener, *J. Math. Phys.* 2 (1923); R. Paley, N. Wiener & A. Zygmund, *Math. Z.* 37 (1933); P. Lévy (1948);
    Z. Ciesielski, *Studia Math.* 20 (1961).
  - M. Donsker, *Mem. AMS* 6 (1951); A. Khinchin, *Fund. Math.* 6 (1924); V. Strassen, *Z. Wahrsch.* 3 (1964).
- **Counting processes.**
  - O. Aalen, *Ann. Stat.* 6 (1978); R. Rebolledo, *Z. Wahrsch.* 51 (1980).
  - P. K. Andersen, Ø. Borgan, R. Gill & N. Keiding, *Statistical Models Based on Counting Processes* (1993).
  - E. Freireich et al., *Blood* 21 (1963); E. Gehan, *Biometrika* 52 (1965).
- **Books.** D. Williams, *Probability with Martingales* (1991); R. Durrett, *Probability: Theory and Examples* (5th ed.
  2019).

## Problems and solutions

1. **Conditional expectation as the best predictor.**
   - Assume X ∈ L²; let Y = E[X | 𝒢] and Z ∈ L²(𝒢).
   - E(X − Z)² = E(X − Y)² + 2E[(X − Y)(Y − Z)] + E(Y − Z)².
   - Y − Z is 𝒢-measurable, so E[(X − Y)(Y − Z)] = E[(Y − Z) E(X − Y | 𝒢)] = 0.
   - Hence E(X − Z)² = E(X − Y)² + E(Y − Z)² ≥ E(X − Y)². Equality holds iff Z = Y almost surely, which gives
     uniqueness.
2. **The expected length of a fair game.**
   - S_n² − n is a martingale for a ±1 walk.
   - τ, the exit time from (0, b) started at a, has E τ < ∞ (a geometric bound: from anywhere, b straight steps exit),
     and the stopped process is dominated by b² + τ.
   - So optional stopping gives E S_τ² − E τ = S₀² = a².
   - E S_τ² = b² · P(hit b) = b² · a/b = ab, so E τ = ab − a² = a(b − a).
3. **De Moivre's martingale.**
   - E[(q/p)^{S_{n+1}} | ℱ_n] = (q/p)^{S_n} [p (q/p) + q (p/q)] = (q/p)^{S_n} (q + p) = (q/p)^{S_n}.
   - Stopping at 0 or b (bounded paths) gives (q/p)^a = P_b (q/p)^b + (1 − P_b).
   - So P(reach b) = (1 − (q/p)^a) / (1 − (q/p)^b). For roulette (p = 18/38), a = 10 and b = 20, this is 0.259.
4. **A two-state chain.**
   - Balance: π₁(1 − a) = π₀ b, so π₁ = b / (1 − a + b).
   - The second eigenvalue of P is a − b, so E[X_k | X₀] − π₁ = (a − b)^k (X₀ − π₁) (true at k = 1 by direct check,
     then by the Markov property).
   - So under stationary initialization, Cov(X₀, X_k) = (a − b)^k Var X₀ and the lag-k correlation is (a − b)^k.
   - For *Onegin*, a = 0.128 and b = 0.663: π₁ = 0.663 / 1.535 = 0.432 and the lag-1 correlation is −0.534.
5. **McDiarmid for empty bins.**
   - Z = f(X₁, …, X_n), where X_i is ball i's bin, independent.
   - Moving one ball can empty at most one bin and fill at most one, so Z changes by at most 1: c_i = 1.
   - McDiarmid: P(|Z − EZ| ≥ t) ≤ 2 exp(−2t² / Σ c_i²) = 2 exp(−2t²/n).
   - For n = 1,000 the bound is below 0.05 only for t ≥ 43, but the simulated SD is 9.9: valid but loose.
6. **The Nelson–Aalen variance.**
   - Ĥ(t) − H*(t) = ∫₀ᵗ J(s)/Y(s) dM(s), where J = 1(Y > 0), H*(t) = ∫₀ᵗJ(s)λ(s)ds, and M = N − ∫Yλ. Assume a nonexplosive continuous-time intensity model with no simultaneous individual events and sufficient integrability.
   - The integrand is predictable, so the integral is a martingale with predictable variation
     ∫ J/Y² d⟨M⟩ = ∫ J/Y² · Y λ ds = ∫ J λ / Y ds.
   - Replacing the compensator increment Yλ ds by dN gives ∫J/Y² dN = Σ d_j/Y_j², an observed-event bracket estimator. With individual unit jumps it is the optional variation. Aggregated simultaneous jumps have squared jump sizes instead; ties in recorded times need a grouping convention, and the log-rank variance uses its tied-event finite-population correction.

## Glossary

- **Conditioning.**
  - Conditional expectation; the tower property; Radon–Nikodym derivative; L² projection; Borel's paradox: what you
    know.
  - Filtration; adapted, predictable; stopping time; stopped process: information in time.
- **Martingales.**
  - Martingale, sub- and supermartingale; Doob decomposition; compensator; predictable and optional variation: fair
    games.
  - Optional stopping; gambler's ruin; de Moivre's martingale; Wald's identities: when to quit.
  - Doob's maximal inequality; Ville's inequality; e-value; anytime-valid test: how high a game climbs.
  - Upcrossings; martingale convergence; uniform integrability; Lévy's upward theorem; reverse martingale: limits.
  - Azuma–Hoeffding; McDiarmid; Freedman; Doob martingale: concentration.
  - Martingale CLT; conditional Lindeberg condition; unit root: normal limits.
- **Markov chains.**
  - Transition kernel; stationary law; reversibility; Harris chain; small set; minorization; drift (Foster–Lyapunov);
    geometric ergodicity; asymptotic variance; batch means: MCMC theory.
  - Total variation; coupling; mixing time; spectral gap; relaxation time; cutoff; recurrence and transience:
    forgetting the start.
- **Continuous time.**
  - Brownian motion; Wiener measure; Schauder functions; scaling; quadratic variation; reflection principle; Brownian
    bridge: the continuous random walk.
  - Invariance principle; Donsker's theorem; Dickey–Fuller law; law of the iterated logarithm; Strassen's law: the walk
    from far away.
  - Counting process; intensity; Doob–Meyer decomposition; Nelson–Aalen; Rebolledo's CLT: survival underneath.

## Where it comes back

- **Part 45**: Rao–Blackwell as a conditional expectation; sufficiency as a σ-algebra; Brown's link between admissibility
  and the recurrence of Brownian motion (chapter 9's Pólya).
- **Part 47**: the score is a martingale: the asymptotics of the MLE, along dependent sequences too.
- **Part 48**: empirical processes: Donsker for whole classes of functions; the Brownian bridge behind
  Kolmogorov–Smirnov.
- **Part 53**: posterior consistency, beyond Doob's theorem.
- **Part 54**: McDiarmid for the generalization gap of learned predictors.
- **Part 58**: Ville's inequality at work: e-values, confidence sequences, bandits and Freedman's inequality.


## QA scope

The [scientific review and verification receipts](../../../docs/qa/evidence/stats44-polish-20261107/source-review.md) document regenerated inputs, independent reference checks and corrected theorem conditions. The recorded English endpoint/native/motion and representative narrated-preview checkpoint is complete. Chinese narration/caption tables, full listening and final narrated masters remain open production gates.
