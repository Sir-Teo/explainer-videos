# Statistics, Built — Part 63: Privacy and Fairness

Part 63 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eighth part of Stage V, the research frontier.

It opens with a governor's medical record. In the mid-1990s Massachusetts's Group Insurance Commission released state
employees' hospital records with names removed. Latanya Sweeney bought Cambridge's voter roll for twenty dollars,
joined the two on ZIP code, birth date and sex, and found Governor William Weld's records.
- **The general fact.** Sweeney (2000) estimated that about 87% of Americans in the 1990 census were unique by
  five-digit ZIP, sex and birth date. Golle (2006) found 63% with the 2000 census.
- **In the Museum's NHANES extract** (5,176 adults), age and sex single out nobody. Adding BMI to one decimal makes
  80.6% unique, and adding a blood pressure makes 99.6% unique.

The part asks how much protecting individuals costs the statistics, and what fairness can require:
- differential privacy (Dwork, McSherry, Nissim & Smith 2006):
  - neighbouring datasets, the Bayesian reading, randomized response (Warner 1965), and the Laplace mechanism;
  - classic against analytic Gaussian calibration (Balle & Wang 2018);
  - post-processing, composition and group privacy, the exponential mechanism, and what DP does not promise;
- DP as hypothesis testing:
  - Wasserman & Zhou (2010) and Kairouz, Oh & Viswanath (2015);
  - trade-off functions and Gaussian DP (Dong, Roth & Su 2022), shown on the new trade-off plot with a simulated
    membership attack;
  - the privacy central limit theorem;
- accountants:
  - the privacy-loss variable and advanced composition (Dwork, Rothblum & Vadhan 2010);
  - Rényi DP (Mironov 2017) and zCDP (Bun & Steinke 2016);
  - the census's ρ = 2.63 read as ε and as μ, and amplification by subsampling with the moments accountant;
- the cost of privacy:
  - central against local estimation of a proportion;
  - Duchi, Jordan & Wainwright's (2013) effective sample size nε²;
  - Cai, Wang & Zhang's (2021) d-dimensional rate, and the strong data-processing inequality;
- private inference:
  - noise-aware intervals (Karwa & Vadhan 2018; Ferrando, Wang & Sheldon 2022) on the Board;
  - clipping bias, private χ² tests (Gaboardi et al. 2016), and UMP private tests (Awan & Slavković 2018);
  - why published noise beats secret swapping;
- the 2020 Census (Abowd et al. 2022):
  - the Bureau's reconstruction of its 2010 tables, TopDown, and invariants;
  - a toy of the nonnegativity projection and its small-block bias;
  - the 2023 noisy measurement files, the redistricting debate (Kenny et al. 2021), Alabama's suit, and choosing ε
    (Abowd & Schmutte 2019);
- private learning:
  - DP-SGD (Abadi et al. 2016) on the Wisconsin biopsies, and memorization (Carlini et al. 2021);
  - membership inference (Shokri et al. 2017; Carlini et al. 2022) as a test;
  - auditing (Jagielski, Ullman & Oprea 2020; Nasr et al. 2021; Steinke, Nasr & Jagielski 2023), and DP's disparate
    impact (Bagdasaryan, Poursaeed & Shmatikov 2019);
- fairness criteria (Barocas, Hardt & Narayanan):
  - independence, separation (Hardt, Price & Srebro 2016) and sufficiency;
  - ProPublica's COMPAS data (Angwin et al. 2016): rates and calibration by race;
  - the pairwise conflicts;
- impossibility:
  - Chouldechova's (2017) identity, reproduced exactly on COMPAS;
  - Kleinberg, Mullainathan & Raghavan (2016);
  - the decision-theoretic view (Corbett-Davies et al. 2017), and rearrest as a biased label;
- multicalibration (Hébert-Johnson, Kim, Reingold & Rothblum 2018):
  - patching on COMPAS, with honest held-out evaluation;
  - its conformal twin (Gibbs, Cherian & Candès), multiaccuracy, outcome indistinguishability and omniprediction;
- causal fairness:
  - counterfactual fairness (Kusner, Loftus, Russell & Silva 2017) on a simulated policing model;
  - resolving variables and path-specific effects (Kilbertus et al. 2017; Nabi & Shpitser 2018);
  - the critique (Kohler-Hausmann 2019), fair policy learning, and delayed impact (Liu et al. 2018);
- five open problems.

It keeps two promises:
- **Part 18** published survey tables as if aggregates revealed nothing about anyone. Chapters 1–6 measure what each
  release leaks and what hiding it costs.
- **Part 19** judged a classifier by one error rate. Chapters 8–11 split the errors by group and ask which
  differences can be removed.

**Built in this part:**
- **`statkit.privacy`** ([`explainer/stats/kit/privacy.py`](../../../explainer/stats/kit/privacy.py)), tested in
  `tests/test_stats_kit_privacy.py`:
  - the Laplace mechanism, classic and analytic Gaussian calibration (with the exact δ), and randomized response
    with its debiasing;
  - basic and advanced composition, zCDP and its conversion, and Rényi accounting for Gaussians;
  - trade-off curves of (ε, δ)-DP, the Laplace mechanism and μ-GDP, and a simulated membership attack;
  - naive and noise-aware private proportions, and central against local MSE;
  - the nonnegative fixed-total projection;
  - noisy clipped gradient descent for logistic regression under zCDP;
  - group rates, calibration by group, and Chouldechova's identity;
  - multicalibration by patching, with replay on new data and calibration gaps.
- **The trade-off plot** (`TradeoffPlot` in `explainer/stats/viz.py`), the part's instrument. It draws privacy as a
  hypothesis test: type I error across and type II error up, the diagonal of guessing, a mechanism's trade-off curve
  with the attacker's forbidden zone beneath it, and individual attacks as points.

**Data.**
- From the Museum:
  - the NHANES extract;
  - the Wisconsin biopsies;
  - ProPublica's COMPAS data, new to the Museum. These are the 6,172 Broward County defendants left after
    ProPublica's filters, keeping age, sex, race, prior count, decile score and two-year rearrest, with names removed.
- The census budget and history are quoted from the Bureau and Abowd et al. (2022).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains two rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Wald interval on a DP-noised count | Laplace, ε = 0.1, n = 1,000 | 95% | 85.4% | broken |
| Noise-aware interval | Laplace, ε = 0.1, n = 1,000 | 95% | 95.2% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats63.compute   # once (a few minutes)
python tools/build.py stats63 -q l                         # fast 480p preview
python tools/build.py stats63                              # 1080p30 -> renders/stats63.mp4
python tools/qa_scene.py stats63 Testing
python tools/lecture_length.py stats63 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | A governor's record | NHANES, 5,176 adults: unique by age 0%, + sex 0% (126 classes), + BMI 80.6%, + blood pressure 99.6% |
| 1 | Differential privacy | one count, δ = 10⁻⁵: Laplace sd √2/ε; Gaussian σ at ε = 1, classic 4.84, analytic 3.73 |
| 2 | DP as testing | 1-GDP: power 0.26 at α = 0.05; a simulated attack (n = 100, σ = 0.01, 40,000 releases) on G₁ |
| 3 | Accountants | σ = 5, k = 1,000, δ = 10⁻⁵: basic ε 1,047, advanced 2,098, Rényi 50.4, zCDP 50.3; census ρ = 2.63 → ε ≈ 18.2 at δ = 10⁻¹⁰, μ ≈ 2.3 |
| 4 | The cost of privacy | p = 0.3, ε = 1, 20,000 runs: central MSE 9.5% above sampling at n = 100, 0.1% at 10,000; local ≈ 5× central |
| 5 | Private inference | p = 0.3, ε = 0.1: naive coverage 53.8% (n = 100), 83.5% (1,000); noise-aware 93.5–96.2%; Board 85.4% vs 95.2% |
| 6 | The 2020 Census | 400 blocks, noise sd 4, 200 runs: raw 4.9% negative, unbiased; projected: blocks under 5 people +0.70, larger slightly low |
| 7 | DP-SGD | Wisconsin, 400 train / 169 test: accuracy 0.887 at ε 0.37, 0.921 at 0.69, 0.965 at 1.2, 0.973 at 7.8; non-private 0.979 |
| 8 | Fairness criteria | COMPAS, 5,278 Black or white: base rates 0.523 vs 0.391; high 0.576 vs 0.331; FPR 0.423 vs 0.220; FNR 0.285 vs 0.496; PPV 0.650 vs 0.595 |
| 9 | Impossibility | Chouldechova's identity reproduces 0.423 and 0.220 exactly; base-rate odds ratio 1.71; shared PPV 0.62, FNR 0.39 force 0.41 vs 0.24 |
| 10 | Multicalibration | COMPAS, 4 groups × 5 bins, 15 patches; held-out gap 0.038 → 0.031 (in-sample 0.036 → 0.008); women 0.070 → 0.030, under 25 0.065 → 0.040 |
| 11 | Causal fairness | 20,000 simulated people: true gap −0.016; score on priors +0.084 (AUC 0.63), on the residual +0.002 (AUC 0.65) |
| 12 | Open problems | — |
| 13 | Outro | — |

## Sources

- **The hook.**
  - L. Sweeney, *J. Law Med. Ethics* 25 (1997); Sweeney, "Simple demographics often identify people uniquely",
    Carnegie Mellon Data Privacy Working Paper 3 (2000); Sweeney, *Int. J. Uncertainty, Fuzziness and Knowledge-Based
    Systems* 10 (2002); P. Golle, WPES (2006).
  - A. Narayanan & V. Shmatikov, IEEE S&P (2008); N. Homer et al., *PLoS Genetics* 4 (2008); I. Dinur & K. Nissim,
    PODS (2003).
  - J. Angwin, J. Larson, S. Mattu & L. Kirchner, "Machine Bias", ProPublica (2016); W. Dieterich, C. Mendoza &
    T. Brennan, Northpointe (2016).
- **Differential privacy.**
  - C. Dwork, F. McSherry, K. Nissim & A. Smith, TCC (2006); S. Warner, *JASA* 60 (1965);
  - C. Dwork & A. Roth, *Found. Trends Theor. Comput. Sci.* 9 (2014); B. Balle & Y.-X. Wang, ICML (2018);
  - F. McSherry & K. Talwar, FOCS (2007).
- **Testing and accounting.**
  - L. Wasserman & S. Zhou, *JASA* 105 (2010); P. Kairouz, S. Oh & P. Viswanath, ICML (2015);
  - J. Dong, A. Roth & W. Su, *JRSS B* 84 (2022);
  - C. Dwork, G. Rothblum & S. Vadhan, FOCS (2010); I. Mironov, CSF (2017); M. Bun & T. Steinke, TCC (2016).
- **The cost of privacy.** J. Duchi, M. Jordan & M. Wainwright, FOCS (2013) and *JASA* 113 (2018); T. Cai, Y. Wang &
  L. Zhang, *Ann. Statist.* 49 (2021).
- **Private inference.**
  - V. Karwa & S. Vadhan, ITCS (2018); C. Ferrando, S. Wang & D. Sheldon, AISTATS (2022);
  - M. Gaboardi, H. W. Lim, R. Rogers & S. Vadhan, ICML (2016); J. Awan & A. Slavković, NeurIPS (2018).
- **The census.**
  - J. Abowd et al., *Harvard Data Science Review*, Special Issue 2 (2022); the 2020 redistricting data's ρ = 2.63
    (2.56 persons, 0.07 housing units);
  - U.S. Census Bureau, release of the 2020 redistricting noisy measurement file (15 June 2023);
  - C. Kenny et al., *Science Advances* 7 (2021); *Alabama v. U.S. Department of Commerce* (M.D. Ala., three-judge
    court, June 2021);
  - J. Abowd & I. Schmutte, *American Economic Review* 109 (2019).
- **Private learning.**
  - M. Abadi et al., CCS (2016); N. Carlini et al., USENIX Security (2021); R. Shokri et al., IEEE S&P (2017);
  - N. Carlini et al., IEEE S&P (2022); M. Jagielski, J. Ullman & A. Oprea, NeurIPS (2020); M. Nasr et al., IEEE S&P
    (2021); T. Steinke, M. Nasr & M. Jagielski, NeurIPS (2023);
  - E. Bagdasaryan, O. Poursaeed & V. Shmatikov, NeurIPS (2019).
- **Fairness.**
  - S. Barocas, M. Hardt & A. Narayanan, *Fairness and Machine Learning* (MIT Press, 2023);
  - M. Hardt, E. Price & N. Srebro, NeurIPS (2016); A. Flores, K. Bechtel & C. Lowenkamp, *Federal Probation* 80
    (2016);
  - A. Chouldechova, *Big Data* 5 (2017); J. Kleinberg, S. Mullainathan & M. Raghavan, ITCS (2017; arXiv 2016);
  - S. Corbett-Davies, E. Pierson, A. Feller, S. Goel & A. Huq, KDD (2017).
- **Multicalibration.**
  - U. Hébert-Johnson, M. Kim, O. Reingold & G. Rothblum, ICML (2018); M. Kim, A. Ghorbani & J. Zou, AIES (2019);
  - C. Dwork et al., STOC (2021); P. Gopalan et al., ITCS (2022); I. Gibbs, J. Cherian & E. Candès, arXiv:2305.12616.
- **Causal fairness.**
  - M. Kusner, J. Loftus, C. Russell & R. Silva, NeurIPS (2017); N. Kilbertus et al., NeurIPS (2017);
  - R. Nabi & I. Shpitser, AAAI (2018); I. Kohler-Hausmann, *Northwestern Univ. Law Rev.* 113 (2019);
  - L. Liu, S. Dean, E. Rolf, M. Simchowitz & M. Hardt, ICML (2018).
- **Open problems.** T. Raghunathan, J. Reiter & D. Rubin, *J. Official Statistics* 19 (2003); D. Ensign et al.,
  FAT* (2018).

## Problems and solutions

1. **Randomized response.**
   - For a report r, P(r | x = 1)/P(r | x = 0) is π/(1 − π) or (1 − π)/π. With π = e^ε/(1 + e^ε), both lie in
     [e^{−ε}, e^ε], so the mechanism is ε-DP.
   - The report is 1 with probability q = πp + (1 − π)(1 − p) = (2π − 1)p + (1 − π). So
     p̂ = (q̂ − (1 − π))/(2π − 1) is unbiased.
   - Var(p̂) = q(1 − q)/(n(2π − 1)²).
2. **The Laplace mechanism.**
   - The output densities are (ε/2Δ)exp(−ε|z − f(D)|/Δ) and the same with f(D′).
   - Their ratio is exp(ε(|z − f(D′)| − |z − f(D)|)/Δ) ≤ exp(ε|f(D) − f(D′)|/Δ) ≤ e^ε, by the triangle inequality and
     the definition of Δ.
   - Integrating over any set S gives the definition.
3. **Gaussian trade-off curves.**
   - The outputs are N(f(D), σ²) and N(f(D′), σ²). Standardizing gives N(0, 1) against N(s/σ, 1), with
     |s| = |f(D) − f(D′)| ≤ Δ.
   - Testing a larger shift is easier, so the worst case is s = Δ and the curve is G_{Δ/σ}.
   - For two independent mechanisms the pair is N(0, I) against N((μ₁, μ₂), I). The likelihood ratio depends only on
     the projection onto (μ₁, μ₂)/‖μ‖, which is N(0, 1) against N(‖μ‖, 1). So the composition is G_{√(μ₁² + μ₂²)}.
4. **When central privacy becomes cheap.**
   - The privacy term is 2/(nε)² and the sampling term is p(1 − p)/n. The privacy share is a tenth when
     2/(nε)² = p(1 − p)/(9n), that is, n = 18/(ε²p(1 − p)).
   - At p = 0.3 and ε = 0.1 this is n ≈ 8,571.
5. **Chouldechova's identity.**
   - The true positives number PPV · H = (1 − FNR)pn, and the false positives (1 − PPV)H = FPR(1 − p)n, where H is the
     number labelled high.
   - Dividing, (1 − PPV)/PPV = FPR(1 − p)/((1 − FNR)p). Solving for FPR gives the identity.
6. **The impossibility.**
   - If both groups have the same PPV and FNR, then FPR_a/FPR_b = [p_a/(1 − p_a)]/[p_b/(1 − p_b)], provided the
     common factor (1 − PPV)(1 − FNR)/PPV is not zero.
   - The odds differ when the base rates differ, so the FPRs differ.
   - The factor vanishes only if PPV = 1, when both FPRs are zero, or FNR = 1, when the classifier catches no one and
     the identity degenerates. These are the trivial exceptions.

## Glossary

- **Privacy.**
  - Quasi-identifier; linkage attack; reconstruction attack.
  - Differential privacy; neighbouring datasets; ε, δ; sensitivity; Laplace and Gaussian mechanisms; analytic
    Gaussian; randomized response; exponential mechanism.
  - Post-processing; composition; group privacy.
- **Testing and accounting.** Trade-off function; f-DP; Gaussian DP (μ); privacy-loss variable; advanced
  composition; Rényi DP; zCDP (ρ); amplification by subsampling; moments accountant.
- **Costs and inference.** Central and local models; effective sample size nε²; strong data-processing inequality;
  noise-aware interval; clipping bias; TopDown; invariants; noisy measurement file.
- **Learning.** DP-SGD; per-example clipping; memorization; membership inference; LiRA; privacy auditing; canaries.
- **Fairness.**
  - Independence (demographic parity); separation (equalized odds); sufficiency (calibration within groups); base
    rate; FPR, FNR, PPV.
  - Chouldechova's identity; the Kleinberg–Mullainathan–Raghavan theorem; balance for the positive and negative
    classes.
  - Multicalibration; multiaccuracy; outcome indistinguishability; omniprediction.
  - Counterfactual fairness; resolving variable; path-specific effect; delayed impact.

## Where it comes back

- **Part 64**: test-set contamination as membership inference; model-made labels and their group-dependent errors;
  the reusable holdout, which is differential privacy applied to adaptive data analysis.
- **Part 65**: the dissertation's chapter on its data and the people they describe.
