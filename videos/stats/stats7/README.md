# Statistics, Built — Part 7: Randomness on Demand

Part 7 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Every simulation in Parts 1–6 ran on a
machine that can only follow instructions. This part builds the randomness, shapes it into any distribution, and
learns to use it honestly. PCG stream parameters are distinct, rather than a proof of independent or nonoverlapping outputs. It ends with Markov chains, the engine of modern Bayesian computation.

It opens with John von Neumann's warning (1951) that arithmetic randomness is "a state of sin". It then turns
3,000 consecutive triples from IBM's RANDU in 3D until all of them fall on 15 planes (Marsaglia 1968). From there:
- linear congruential generators, their periods and lattices;
- PCG, and how generators are tested;
- the inverse CDF;
- rejection sampling;
- Box–Muller, Marsaglia–Tsang and Walker's alias table;
- Monte Carlo integration, from Buffon's needle to Lazzarini's;
- simulation studies with Monte Carlo standard errors;
- variance reduction;
- Markov chains, their stationary laws, PageRank, the seven-shuffle theorem and the Metropolis algorithm.

Numerical examples are cached in [`compute.py`](compute.py); small seeded harness, stratification, and chain demonstrations are evaluated in their scenes. The generators and samplers there are statkit's
own; the riffle-shuffle distances are exact. For a forward riffle with the deck listed in final order, rising sequences are one plus descents of the inverse permutation; inversion preserves the Eulerian counts used in TV. The d-ball comparison uses the same actual budget m^d for the grid error and exact Monte Carlo standard error. Displayed histograms retain omitted tail mass in their denominators. The control-variate comparison uses the known population coefficient 6(3−e), rather than fitting it to the same draws.

**Built in this part:** `statkit.random` ([`explainer/stats/kit/random.py`](../../../../explainer/stats/kit/random.py)),
tested against SciPy in [`tests/test_stats_kit_random.py`](../../../../tests/test_stats_kit_random.py). It contains:
- **generators:** `randu`, `lcg`, `PCG32`;
- **samplers:** `inverse_cdf`, `discrete_inverse`, `rejection`, `box_muller`, `marsaglia_tsang`, `AliasTable`;
- **the simulation-study harness:** `streams` (independent, reproducible generators), `mc_se`, and `simulate`, which
  reports bias, empirical SE and coverage, each with its Monte Carlo SE.

The harness provides the Coverage Board framework; empirical-SE MCSE uses a normal approximation across replicates. `NSpace.cloud` (in `explainer/stats/viz.py`) draws thousands of
points in a turnable ℝ³ with one updater.

## Build it

```bash
python -m videos.stats.stats7.compute          # once: every computed item (about a minute; cached in .cache/stats7)
python tools/build.py stats7 -q l              # fast 480p preview
python tools/build.py stats7                   # 1080p30 -> renders/stats7.mp4
python tools/qa_scene.py stats7 Hook           # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats7 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | A state of sin | Von Neumann (1951); his middle-square method and its cycles; RANDU's triples turned edge-on in 3D; PCG32's cube; the objectives. | 2100 → 4100 → 8100 → 6100 → 2100; 9x − 6y + z takes 15 integer values |
| 1 | Pseudo-random generators | Lehmer's LCG (1949); periods on a 64-hour clock and Hull–Dobell; the lattice of pairs and the spectral test; PCG32 in four lines; the Mersenne Twister; χ², runs and 3-D tests. | period 16 vs 64; RANDU 1-D χ² p = 0.89 but 3-D p = 5 × 10⁻³⁰; PCG32 p = 0.87, 0.16 |
| 2 | The inverse CDF | Proof; the exponential by −log(1 − U); 4,000 draws; discrete inversion; inverting the ECDF is resampling (the bootstrap); the normal's numerical quantile. | frequencies 0.10, 0.23, 0.30, 0.21, 0.15 vs 0.10, 0.25, 0.30, 0.20, 0.15 |
| 3 | Rejection sampling | Darts under Beta(2, 5); the proof; a Laplace envelope for the normal; adaptive rejection for log-concave densities; the curse of dimension. | kept 41.3% vs 1/M = 40.7%; normal from Laplace 76%; d-ball from cube: 79% (d = 2), 0.25% (10), 2.5 × 10⁻⁸ (20) |
| 4 | Special methods | Box–Muller animated and proved (Rayleigh radius); Marsaglia–Tsang gamma; Walker's alias table; multivariate normals by Cholesky. | gamma acceptance 98.7%, mean 2.51; alias frequencies within 0.003 of p |
| 5 | Monte Carlo integration | π by darts with the √n funnel; σ/√n in any dimension; grid vs MC for the d-ball; Halton points (quasi-MC); Buffon (1777); Lazzarini's suspicious 355/113. | 4,000 darts: 3.162; d = 10: grid error 61%, exact MC relative SE about 2.0% at the same rounded grid budget; Buffon SE at 3,408 throws: 0.051 |
| 6 | Simulation studies done right | ADEMP (Morris, White & Crowther 2019); Wald interval coverage for n = 30 against the exact sum and Wilson; Monte Carlo SEs and planning R; seeds, streams, common random numbers; `simulate`. | Wald coverage 46% at p = 0.02; MCSE 0.0034 at c = 0.95, R = 4,000; p = 0.1: 0.807 ± 0.006 |
| 7 | Variance reduction | Antithetic pairs; control variates (regression); stratified sampling; importance sampling for P(Z > 4); when importance sampling fails. | variance ÷32 (antithetic), ÷62 (control), ÷8 × 10⁵ (stratified); P(Z > 4): variance ÷6,700 |
| 8 | Markov chains | Markov's Onegin (1913) and its two-state chain; the weather chain; probability as a flowing fluid; the ergodic theorem along one path; geometric convergence by the second eigenvalue. | vowels: chain 0.432 vs count 43.2%; π = (19, 13, 9)/41; λ₂ = 0.462 |
| 9 | Stationary distributions | Left eigenvectors and Perron–Frobenius; detailed balance and reversibility; random walk on a graph (π ∝ degree); PageRank; periodicity. | PageRank (0.30, 0.15, 0.33, 0.02, 0.09, 0.05, 0.07) |
| 10 | Mixing: seven shuffles | The GSR riffle animated; rising sequences and the Bayer–Diaconis formula; total variation for 52 cards; a 5-card simulation check; the cutoff phenomenon. | TV: 1.000 (k ≤ 4), 0.924, 0.614, 0.334, 0.167, 0.085 |
| 11 | The Metropolis algorithm | Los Alamos (1953); the six-line algorithm; detailed balance; three step sizes on a two-humped target; Gibbs sampling, first look; lessons for Part 27. | acceptance 97% / 57% / 9%; means 2.05 / 0.89 / 0.89 vs truth 0.80 |
| 12 | Outro | Recap, payoffs, problems, references, the Transcript, Part 8's question. | — |

## Sources

- **Generators.**
  - J. von Neumann, "Various techniques used in connection with random digits", NBS Applied Math. Series 12 (1951).
  - D. H. Lehmer (1949, publ. 1951); T. Hull & A. Dobell, *SIAM Review* 4 (1962); R. Coveyou & R. MacPherson,
    *JACM* 14 (1967).
  - G. Marsaglia, "Random numbers fall mainly in the planes", *PNAS* 61 (1968).
  - M. Matsumoto & T. Nishimura, *ACM TOMACS* 8 (1998); M. E. O'Neill, "PCG…" (2014).
  - P. L'Ecuyer & R. Simard, "TestU01", *ACM TOMS* 33 (2007).
- **Samplers.**
  - G. Box & M. Muller, *Ann. Math. Statist.* 29 (1958); G. Marsaglia & T. Bray (1964).
  - G. Marsaglia & W. W. Tsang, *ACM TOMS* 26 (2000).
  - A. Walker, *Electronics Letters* 10 (1974); M. Vose, *IEEE TSE* 17 (1991).
  - W. Gilks & P. Wild, *Applied Statistics* 41 (1992); M. Wichura, AS 241 (1988).
- **Monte Carlo.**
  - G. Buffon, *Essai d'arithmétique morale* (1777); M. Lazzarini (1901), and N. T. Gridgeman, "Geometric
    probability and the number π", *Scripta Math.* 25 (1960).
  - J. Halton (1960); I. Sobol' (1967).
  - T. Morris, I. White & M. Crowther, *Statistics in Medicine* 38 (2019).
- **Markov chains.**
  - A. Markov (1906; 1913, on *Eugene Onegin*); B. Hayes, "First links in the Markov chain", *American Scientist* 101
    (2013).
  - S. Brin & L. Page (1998).
  - E. Gilbert (1955); J. Reeds (1981); D. Bayer & P. Diaconis, "Trailing the dovetail shuffle to its lair", *Ann.
    Appl. Probab.* 2 (1992).
- **MCMC.**
  - N. Metropolis, A. Rosenbluth, M. Rosenbluth, A. Teller & E. Teller, *J. Chem. Phys.* 21 (1953).
  - W. K. Hastings, *Biometrika* 57 (1970).
  - S. Geman & D. Geman (1984); A. Gelfand & A. Smith, *JASA* 85 (1990).
- **Textbooks.**
  - D. Knuth, *TAOCP* vol. 2 (3rd ed., 1997).
  - L. Devroye, *Non-Uniform Random Variate Generation* (1986).
  - C. Robert & G. Casella, *Monte Carlo Statistical Methods* (2nd ed., 2004).
  - A. Owen, *Monte Carlo Theory, Methods and Examples*.
  - D. Levin & Y. Peres, *Markov Chains and Mixing Times* (2nd ed., 2017).

## Problems and solutions

**1. Two periods.**

*Solution.* For x ↦ (5x + 3) mod 16, the Hull–Dobell conditions hold, so the period is the full 16:
- c = 3 is coprime to 16;
- a − 1 = 4 is divisible by 2, the only prime factor of 16;
- a − 1 is also divisible by 4, as it must be since 4 divides 16.

For x ↦ 5x mod 16 from 1, the sequence is 1, 5, 9, 13, 1, …, so the period is 4.

**2. Inversion.**

*Solution.*
- **Pareto:** F(x) = 1 − (x_m/x)^α for x ≥ x_m. Solving u = F(x) gives x = x_m (1 − u)^{−1/α}. Since 1 − U is also
  uniform, x_m U^{−1/α} works too.
- **Logistic:** u = 1/(1 + e^{−x}) gives x = log(u/(1 − u)).

**3. Rejection for 6x(1 − x).**

*Solution.* The density peaks at x = 1/2 with value 3/2, so M = 3/2. The acceptance rate is 1/M = 2/3, and the number
of darts per draw is geometric with mean M = 1.5.

**4. A Monte Carlo integral.** g(U) = √(1 − U²).

*Solution.* I = π/4. Then E g² = ∫₀¹ (1 − x²) dx = 2/3, so

Var g(U) = 2/3 − π²/16 = 0.0498,

and σ = 0.223. The standard error is σ/√n, so SE = 0.001 needs n = (0.223/0.001)², at least 49,817 using the unrounded variance. (Antithetic or
stratified sampling would cut this by a large factor.)

**5. A two-state chain.**

*Solution.* Assume 0 ≤ a,b ≤ 1. If a=b=0, P=I and every distribution is stationary. Otherwise solving πP = π gives π = (b/(a + b), a/(a + b)); detailed balance π₁a = π₂b gives the same answer at once.
The trace is 2 − a − b = 1 + λ₂, so λ₂ = 1 − a − b. When 0 < a+b < 2, the chain forgets its start geometrically at rate |1 − a − b|.
- When a + b = 1, it forgets in one step.
- When a = b = 1, it alternates for ever: periodic, with λ₂ = −1.

**6. Metropolis with an unnormalized f.**

*Solution.* For y ≠ x, the off-diagonal transition density is T(x → y) = q(y | x) min(1, f(y)/f(x)). Then

f(x) T(x → y) = q(y | x) min(f(x), f(y)).

This is symmetric in x and y because q is, so detailed balance holds and f/∫f is stationary, assuming 0 < ∫f < ∞. Ergodic convergence requires additional chain conditions. If f = c f̃ with c
unknown, then f(y)/f(x) = f̃(y)/f̃(x): the constant cancels, and the chain run with f̃ is the same chain.

## Where it comes back

| Idea | Returns in |
|---|---|
| statkit.random, the simulation harness, the Coverage Board | 8, 11, 16, 33 |
| Monte Carlo error, simulation-study design | 11, 16, 28, 59 |
| inversion of the ECDF: the bootstrap | 16 |
| importance sampling | 27, 28 |
| stratification | 18 |
| Markov chains, stationary laws, ergodicity | 17, 27, 44 |
| mixing and convergence diagnostics | 27, 53 |
| Metropolis, Gibbs, MCMC | 15, 26, 27 |
