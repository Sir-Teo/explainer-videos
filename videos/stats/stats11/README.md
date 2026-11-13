# Statistics, Built — Part 11: Honest Intervals

Part 11 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first part of Stage II, Bachelor's: Methods. Part 10 asked whether an
effect is real. This part asks how big it is, and what "95% confident" promises.

It opens with the textbook (Wald) interval for a proportion. Its exact coverage zigzags below 95% as n grows. At
p = 0.005 it covers 94.5% with n = 591 and 79.2% with n = 592 (Brown, Cai & DasGupta 2001). From there the part
covers:
- Neyman's definition, and the interval rain;
- pivots, including the continuous IID approximation to the tank problem's [214, 353], and shortest vs equal-tailed intervals;
- Neyman's belt and the test–interval duality;
- the binomial family, with exact coverage curves;
- likelihood intervals and the rule of three;
- discreteness, mid-p, Garwood's Poisson interval and the order-statistic median interval;
- Fieller's ratio sets, which can be the whole line (and must be, by Gleser & Hwang);
- simultaneous intervals (Bonferroni, Scheffé, the DKW band);
- prediction and tolerance intervals, with Wilks' order statistics;
- credible vs confidence intervals, with Welch's 1939 paradox;
- the Coverage Board's protocol, stated formally.

Exact pivot claims require the stated IID model: normal samples for t, chi-squared and F (independent samples for F), exponential waiting times for the rate, and jointly normal means with known covariance for the displayed z-Fieller sets. The World's height intervals are model approximations. Wilson, Agresti–Coull, Jeffreys and Wilks likelihood intervals have approximate nominal coverage, not a uniform 95% guarantee. Means and minima of coverage curves refer to the displayed parameter grid, not a confidence coefficient over the whole parameter space.

The DKW simulation checks the exact sup distance between the sample and finite-World CDFs over all jump points and both limits. The pointwise comparison checks 200 nominal Wald intervals; those also fail marginally in the tails, so the comparison does not isolate multiplicity. The credible-interval comparison uses the unmodified equal-tailed Jeffreys posterior, distinct from the boundary-modified interval recommended for frequentist coverage. The rule of three is a one-sided 95% bound; the two-sided Poisson zero-event bound is 3.69.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- Binomial and Poisson coverages are exact sums over the outcomes.
- Heights, incomes and the screening condition come from the World (seed 1662).
- Everything else is a seeded simulation.

**Built in this part:**
- **`statkit.intervals`** ([`explainer/stats/kit/intervals.py`](../../../explainer/stats/kit/intervals.py)):
  Wald, Wilson, Agresti–Coull, Clopper–Pearson, Jeffreys and likelihood-ratio intervals for a proportion;
  `binom_coverage` and `binom_width` (exact); the t, variance and rate pivots; Fieller; the DKW band; prediction
  intervals; Wilks' order-statistic coverage. It is tested in `tests/test_stats_kit_intervals.py` (against SciPy, and
  coverage against simulation).
- **`IntervalRain`** (in `explainer/stats/viz.py`): intervals falling against the truth, with a running tally.

The Coverage Board gains seven rows, all simulated (R = 10,000 draws, seed 11000; the exact sums at p = 0.05, n = 50 are 91.99% for Wald and 88.53% for Jeffreys, each about two Monte Carlo SEs above its simulated row):

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| Wald | proportion 0.05, n = 50 | 91.41% | broken |
| Wilson | proportion 0.05, n = 50 | 96.05% | conservative |
| Agresti–Coull | proportion 0.05, n = 50 | 96.05% | conservative |
| Clopper–Pearson | proportion 0.05, n = 50 | 98.58% | conservative |
| Jeffreys | proportion 0.05, n = 50 | 87.78% | broken (p = 0.05 falls in one of its dips) |
| t prediction interval | a new man's height, n = 10 | 95.03% | kept |
| t prediction interval | a new income, n = 19 | 93.89% | broken |

## Build it

```bash
python -m videos.stats.stats11.compute         # once (about a minute; cached in .cache/stats11)
python tools/build.py stats11 -q l             # fast 480p preview
python tools/build.py stats11                  # 1080p30 -> renders/stats11.mp4
python tools/qa_scene.py stats11 Binomial
python tools/lecture_length.py stats11 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers |
|---|---|---|---|
| 0 | The sawtooth | The Wald formula; exact coverage against n at p = 0.2 and against p at n = 50; BCD (2001); objectives. | 81.5–95.4% at p = 0.2; 591 vs 592: 94.5% vs 79.2%; mean over the displayed p grid 90.7% |
| 1 | Neyman's promise | Neyman (1937); the definition; the interval rain on the World's men; what 95% does not mean; one-sided bounds; levels and widths; planning a poll. | 93 of 100; 94.9% of 10,000; mean width 9.9 cm; n = 1,068 after rounding up for ±3% |
| 2 | Pivots | The recipe; five pivots and their checks; equal tails vs shortest; the tanks; the asymptotic pivot and its failures. | rate 95.4%, F 94.9%; tanks [214, 353]; shortest σ² interval 16% shorter |
| 3 | Inverting tests | The duality theorem; Neyman's belt at n = 20; Clopper–Pearson from it; Wald's pinched belt; the p-value function; which test gives which interval. | x = 7: [0.154, 0.592] (Wald [0.141, 0.559]) |
| 4 | The binomial family | Wilson, Clopper–Pearson, Agresti–Coull, Jeffreys; Wilson's derivation; six exact coverage curves; sawtooths against n; widths; the World's rare condition; advice. | grid means 90.7 / 95.2 / 95.8 / 96.9 / 95.0 / 94.8%; 4 of 300 |
| 5 | Likelihood intervals | Six intervals for 2 of 30; the skewed likelihood; invariance and log-odds; agreement at large n (horse kicks); the rule of three. | LR [0.011, 0.192]; 3/n vs 1 − 0.05^(1/n) |
| 6 | Discreteness | Why coverage jumps; exact 95% coverage at every p is impossible without randomization; mid-p; Garwood's Poisson interval; the order-statistic median interval; guaranteed versus approximate nominal coverage. | CP grid mean 97.5%, mid-p 95.9% (n = 25); Garwood min 95.6%, Wald 85% on average; (X₍₆₎, X₍₁₅₎) 95.9% |
| 7 | Ratios: Fieller | Where ratios arise; Fieller's quadratic; four cases (bounded, skewed, two rays, the whole line); the g index; Gleser & Hwang (1987). | g = 0.04, 0.79, 1.33, 6.0 |
| 8 | Simultaneous intervals | 0.95ᵏ; Bonferroni; ten intervals simulated; Scheffé (1953); the DKW band on 100 heights; band vs pointwise. | 60% vs 95%; ε = 0.136; whole-CDF band 95.85% vs 200 pointwise Wald intervals jointly 0.8% |
| 9 | Prediction and tolerance | CI vs PI for the next man; the PI pivot; skewed incomes; the log scale; Wilks (1941); tolerance intervals. | 49.8% vs 95.1%; incomes 93.7%, log scale ≈ 95%; order statistics 89.6% vs 90% |
| 10 | Credible vs confidence | The Jeffreys posterior; frequentist coverage of credible intervals; HPD vs equal tails; Welch (1939); the moral. | unmodified equal-tailed Jeffreys posterior: grid mean 95.0%, flat 95.2%; at p = 0.01: 98.6% vs 91.1%; Welch 0.5 = 0.25 × 1 + 0.75 × ⅓ |
| 11 | The Coverage Board, formally | ADEMP; the Monte Carlo SE and verdict rule; choosing R; Part 11's rows; four lessons. | SE 0.22% at R = 10,000 |
| 12 | Outro | Recap, payoffs, problems, references, the Transcript. | — |

## Sources

- **Foundations.** J. Neyman, *Phil. Trans. A* 236 (1937); R. A. Fisher, *Proc. Camb. Phil. Soc.* 26 (1930).
- **Proportions.**
  - E. B. Wilson, *JASA* 22 (1927).
  - C. Clopper & E. S. Pearson, *Biometrika* 26 (1934).
  - A. Agresti & B. Coull, *Am. Stat.* 52 (1998).
  - L. Brown, T. Cai & A. DasGupta, *Stat. Sci.* 16 (2001).
- **Counts and discreteness.**
  - F. Garwood, *Biometrika* 28 (1936).
  - W. Stevens, *Biometrika* 37 (1950).
  - H. Lancaster, *JASA* 56 (1961).
  - W. Thompson, *Ann. Math. Stat.* 7 (1936).
  - J. Hanley & A. Lippman-Hand, *JAMA* 249 (1983).
- **Ratios.** E. Fieller, *JRSS B* 16 (1954); L. Gleser & J. T. Hwang, *Ann. Stat.* 15 (1987).
- **Simultaneous and prediction.**
  - H. Scheffé, *Biometrika* 40 (1953).
  - A. Dvoretzky, J. Kiefer & J. Wolfowitz, *Ann. Math. Stat.* 27 (1956); P. Massart, *Ann. Prob.* 18 (1990).
  - S. Wilks, *Ann. Math. Stat.* 12 (1941).
- **Credible vs confidence.** B. L. Welch, *Ann. Math. Stat.* 10 (1939).
- **Simulation protocol.** T. Morris, I. White & M. Crowther, *Stat. Med.* 38 (2019).
- **Textbooks.**
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), ch. 9.
  - E. Lehmann & J. Romano, *Testing Statistical Hypotheses* (4th ed., 2022).
  - A. Agresti, *Categorical Data Analysis* (3rd ed., 2013).
  - G. Hahn & W. Meeker, *Statistical Intervals* (2nd ed., 2017).

## Problems and solutions

**1. Wilson after zero successes.**

*Solution.* With p̂ = 0 and z = 1.96, the centre is (z²/2)/(n + z²) = 1.921/23.84 = 0.0806. The half-width is
z√(z²/(4n²))/(1 + z²/n) = 0.0806. So the interval is [0, 0.161]. The Wald interval is [0, 0]: it claims certainty
from twenty observations.

**2. The exponential pivot.**

*Solution.* λXᵢ ~ Exp(1), and a sum of n independent Exp(1) variables is Gamma(n, 1), whatever λ is. So
P(G₀.₀₂₅ ≤ λΣXᵢ ≤ G₀.₉₇₅) = 0.95 and λ ∈ [G₀.₀₂₅/Σxᵢ, G₀.₉₇₅/Σxᵢ]. With n = 5 the quantiles are 1.623 and 10.242.
For Σxᵢ = 10 the interval is [0.162, 1.024].

**3. Zero events in 200.**

*Solution.* The exact upper limit solves (1 − p)²⁰⁰ = 0.05, giving p = 1 − 0.05^(1/200) = 0.01487. The rule of three
gives 3/200 = 0.015.

**4. Confidence vs prediction.**

*Solution.* t₉,₀.₉₇₅ = 2.262.
- **CI:** 176 ± 2.262 · 7/√10 = 176 ± 5.0 = [171.0, 181.0].
- **PI:** 176 ± 2.262 · 7 · √1.1 = 176 ± 16.6 = [159.4, 192.6].

**5. Fieller.**

*Solution.* (ȳ − ρx̄)² ≤ z²(1 + ρ²) gives (16 − 3.84)ρ² − 64ρ + (64 − 3.84) ≤ 0. The roots are
(64 ± √(4096 − 4 · 12.16 · 60.16))/24.32, so ρ ∈ [1.225, 4.039]. The set is bounded because g = 3.84/16 = 0.24 < 1.
The delta method gives 2 ± 1.96 · √(1 + 4)/4 = [0.904, 3.096], which is symmetric and too far left.

**6. Welch's example.**

*Solution.* Take θ = 0. D = X₁ − X₂ has the triangular density 1 − |d| on [−1, 1], so
P(|D| ≥ ½) = 2∫_{½}^{1}(1 − d) dd = ¼.
- If |D| ≥ ½, both draws are within ½ of θ and more than ½ apart, so θ lies between them: the interval certainly
  covers.
- The unconditional coverage is P(X₁ < θ < X₂ or X₂ < θ < X₁) = ½. Then ½ = ¼ · 1 + ¾ · c, so c = ⅓.

## Where it comes back

| Idea | Returns in |
|---|---|
| intervals by inverting tests | 12, 14, 46 |
| likelihood and profile intervals | 14, 22 |
| bootstrap intervals | 16, 47 |
| simultaneous bands | 12, 29, 48 |
| prediction, conformal | 19, 34, 57 |
| credible intervals | 15, 26, 53 |
| Fieller, weak identification | 37, 46 |
| the Coverage Board | every part; 65 |
