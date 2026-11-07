# Statistics, Built — Part 18: Who Did You Ask? Sampling and Surveys

Part 18 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Every part so far trusted that the data were a
fair sample of something. This part asks how a sample comes to speak for a population, and what happens when it
doesn't.

It opens with the *Literary Digest* of 1936: 2.4 million ballots, Landon 57%, and a Roosevelt landslide. The World
reruns it with a new survey block: an election in which Blue, the challenger, has 38.2% of 741,311 adults. The
World's Digest mails the island's telephone-and-car registers (208,339 people), gets 34,588 ballots back, and finds
Blue at 58.0%. A simple random sample of 1,000 says 38.0%, with a 95% CI of [35.0, 41.0].

From there the part covers:
- **What went wrong.** Frame bias (+8.6 points: the listed are richer, and the rich vote Blue) and nonresponse bias
  (+11.2: Blue voters return 21% of ballots, Red voters 13%). Squire (1988). Gallup's forecast of the Digest's
  result. The total survey error.
- **Meng's identity.** The error of any sample is ρ_{R,Y} × √((1 − f)/f) × σ_Y, derived. For the World's Digest:
  ρ = 0.090, error 19.8 points exactly. Effective sample sizes: 34,588 ballots are worth 6 random voters; a
  self-selected half of the island (364,275 people) is worth 50. Error curves; the big-data paradox; two Board rows.
- **Design-based inference.** Kiær (1895), Bowley (1912), Neyman (1934) and Gini & Galvani's purposive sample. Fixed
  values with a random selection; finite population vs superpopulation; the lottery on the island map.
- **Simple random sampling.** The fpc derived; 2,000 polls of 1,000 (SD 1.52 points); why ±3 points needs about 1,100
  people whatever N; the fpc in a town of 1,114 (coverage 93.7% with it, 98.5% without); systematic sampling.
- **Stratification.** Mean income by register band; Neyman allocation derived (80 / 423 / 497 against proportional
  334 / 591 / 75); SE 1.80 (SRS), 1.44 (proportional), 0.76 (Neyman); stratifying the vote by region gains only
  1.5%; post-stratification.
- **Clusters and stages.** 20 towns × 50 adults; ICC 0.0156; Kish's design effect 1.76 (n_eff 567); naive vs
  cluster SE; probability proportional to size (Hansen & Hurwitz 1943) a standard deviation 174 times smaller for total income;
  multistage designs and replicate weights; two Board rows.
- **Horvitz–Thompson.** Unbiased for any design, checked over all 32 Poisson samples; the variance; Basu's elephants
  (1971); Hájek's estimator.
- **Ratio and regression estimators.** Laplace's 1802 estimate of France (28.35 people per birth); capture–recapture
  as a ratio; the World's register of last year's income (corr 0.95): SD 0.91 vs 3.04, worth a sample 11 times larger;
  GREG and calibration.
- **Weighting.** Design, nonresponse and calibration weights; response-propensity cells; raking (Deming & Stephan
  1940) animated; the raked Digest at 49.1% (Kish n_eff 16,941); MAR vs MNAR; one Board row.
- **Polls.** Quota sampling and 1948; falling response rates; a dialled poll in which raking fixes income-driven
  nonresponse (42.3 → 39.0%) but not vote-driven nonresponse (50.8 → 47.8%); 2016, 2020; the Xbox poll and MRP.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the election, the registers and who answers are the World's new survey block (seed 1662);
- incomes and towns are the World's;
- Laplace's, Gallup's and the polling-error figures are historical.

**Built in this part:**
- **The World's survey block** (`World.survey` in `explainer/stats/world.py`):
  - `vote_blue`, likelier with income, age and some regions;
  - `listed`, the telephone-and-car registers, likelier with income;
  - `propensity`, the chance of returning a mailed ballot, higher for Blue voters and the well-off;
  - `turnout`.

  Adding it changes no earlier block.
- **`statkit.survey`** ([`explainer/stats/kit/survey.py`](../../../explainer/stats/kit/survey.py)), checked in
  `tests/test_stats_kit_survey.py`:
  - the SRS mean with the fpc;
  - proportional and Neyman allocation, and stratified variances and means;
  - the ICC, Kish's design effect and effective sample size;
  - Hansen–Hurwitz and Horvitz–Thompson totals, and Poisson sampling;
  - ratio and regression estimators;
  - post-stratification, raking and weighted means;
  - Meng's identity.
- **The island map** (`IslandMap` in `explainer/stats/viz.py`): the World's coastline and 200 towns, sized by
  population and tinted by region, with highlighting for cluster samples.

The Coverage Board gains five rows: 95% intervals for Blue's share.

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| SRS of 1,000, Wald interval | the World's vote for Blue | 10,000 | 94.61% | kept |
| a self-selected half, n ≈ 364,000 | the World's vote for Blue | 200 | 0.00% | broken |
| 20 towns × 50, SRS formula | the World's vote for Blue | 10,000 | 84.35% | broken |
| 20 towns × 50, cluster SE | the World's vote for Blue | 10,000 | 93.43% | broken |
| Digest returns, raked | the World's vote for Blue | 200 | 0.00% | broken |

## Build it

```bash
python -m videos.stats.stats18.compute         # once (about a minute; cached in .cache/stats18)
python tools/build.py stats18 -q l             # fast 480p preview
python tools/build.py stats18                  # 1080p30 -> renders/stats18.mp4
python tools/qa_scene.py stats18 Meng
python tools/lecture_length.py stats18 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The *Literary Digest*, 1936 | truth 38.2%; listed 46.8%; returns 58.0% (34,588); SRS 38.0% [35.0, 41.0] |
| 1 | What went wrong | frame bias +8.6, nonresponse +11.2; return rates 20.6% Blue, 13.1% Red; median income 39k vs 56k listed; Gallup-style 3,000 → 489 replies, 59.3% Blue |
| 2 | Meng's identity | ρ = 0.0902, f = 0.0467, √((1−f)/f) = 4.52, σ = 0.486 → 0.1980; n_eff 6 and 50; Board 94.6%, 0% |
| 3 | Design-based inference | 29 of 214 districts (Gini & Galvani) |
| 4 | Simple random sampling | SD 1.52 vs 1.54; n ≈ 1,100 for ±3; town of 1,114: 93.7% vs 98.5% |
| 5 | Stratification | S_h 5.8, 17.2, 159.5; SE 1.80 / 1.44 / 0.76 (simulated 1.67 / 1.44 / 0.76); region strata gain 1.5% |
| 6 | Clusters and stages | ICC 0.0156, deff 1.76, n_eff 567; one sample 37.3%, SE 1.53 naive vs 1.59; Board 84.4%, 93.4%; PPS SD 0.22 M vs 38.1 M (SD ratio 174) |
| 7 | Horvitz–Thompson | 32 samples average exactly 24 |
| 8 | Ratio and regression estimators | Laplace 2,037,615 / 71,866 = 28.35 → 28.35 million; register ratio estimate 50.04 vs truth 49.48; SD 0.91 vs 3.04 |
| 9 | Weighting | raw 58.0% → raked 49.1%; weights 0.17–7.8; n_eff 16,941; Board 0% |
| 10 | Polls | Gallup 1948 Dewey 49.5 / Truman 44.5, result 45.1 / 49.6; MAR 42.3 → 39.0%, MNAR 50.8 → 47.8%; 2020 error 3.9 points |
| 11 | Outro | — |

## Sources

- **The *Digest* and the polls.**
  - P. Squire, "Why the 1936 *Literary Digest* poll failed", *Public Opinion Quarterly* 52 (1988).
  - F. Mosteller et al., *The Pre-election Polls of 1948* (SSRC, 1949).
  - AAPOR task force reports on the 2016 (2017) and 2020 (2021) election polls.
  - Pew Research Center, "Response rates in telephone surveys have resumed their decline" (2019).
  - W. Wang, D. Rothschild, S. Goel & A. Gelman, *Int. J. Forecasting* 31 (2015).
- **Sampling theory.**
  - A. Kiær (1895, ISI Bern); A. Bowley, *JRSS* 76 (1913); J. Neyman, *JRSS* 97 (1934); A. Tschuprow, *Metron* 2 (1923).
  - M. Hansen & W. Hurwitz, *Ann. Math. Stat.* 14 (1943); D. Horvitz & D. Thompson, *JASA* 47 (1952); A. R. Sen,
    *J. Indian Soc. Agric. Stat.* 5 (1953); F. Yates & P. Grundy, *JRSS B* 15 (1953).
  - D. Basu and J. Hájek, in *Foundations of Statistical Inference*, ed. V. Godambe & D. Sprott (1971).
  - W. E. Deming & F. Stephan, *Ann. Math. Stat.* 11 (1940); L. Kish, *Survey Sampling* (1965).
  - X.-L. Meng, *Ann. Appl. Stat.* 12 (2018).
  - P.-S. Laplace, *Théorie analytique des probabilités* (1812), book II, ch. 6.
- **Books.** S. Lohr, *Sampling: Design and Analysis* (3rd ed., 2022); W. Cochran, *Sampling Techniques* (3rd ed.,
  1977); C.-E. Särndal, B. Swensson & J. Wretman, *Model Assisted Survey Sampling* (1992); R. Groves et al., *Survey
  Methodology* (2nd ed., 2009).

## Problems and solutions

**1. The fpc in a town.**

*Solution.* Without the fpc, the SE is s/√n = 20/20 = 1.0. With it, multiply by √(1 − 400/2000) = √0.8: about 0.89.

**2. The covariance of inclusion indicators.**

*Solution.* P(Rᵢ = Rⱼ = 1) = n(n − 1)/(N(N − 1)), so Cov(Rᵢ, Rⱼ) = n(n − 1)/(N(N − 1)) − n²/N². Simplify with f = n/N:
f[(n − 1)/(N − 1) − f] = f(n − N)/(N(N − 1)) = −f(1 − f)/(N − 1).

**3. Neyman allocation for two strata.**

*Solution.* Here n_h ∝ N_h S_h ∝ S_h, so n₁ = 25 and n₂ = 75. Ignoring the fpc, with W₁ = W₂ = ½:
- **Neyman:** Var = ¼(1/25) + ¼(9/75) = 0.01 + 0.03 = 0.04.
- **Proportional:** n₁ = n₂ = 50, so Var = ¼(1/50) + ¼(9/50) = 0.05.

Neyman's allocation has 20% less variance.

**4. An effective sample size.**

*Solution.* n_eff = f/(1 − f)/ρ² = (0.01/0.99)/0.0001 ≈ 101. Whatever the population's size, the self-selected 1% is
comparable to about a hundred random people on this squared-error scale, ignoring the comparison SRS's finite-population correction.

**5. A design effect.**

*Solution.* deff = 1 + (30 − 1) × 0.05 = 2.45, so n_eff = 1,500/2.45 ≈ 612.

**6. Horvitz–Thompson is unbiased.**

*Solution.* Write T̂ = Σᵢ Rᵢyᵢ/πᵢ over the whole population. Then E[T̂] = Σᵢ E[Rᵢ]yᵢ/πᵢ = Σᵢ πᵢyᵢ/πᵢ = Σᵢ yᵢ = T. This
holds for any design, provided every πᵢ > 0; otherwise some units can never be seen.

## Glossary

- **Population, frame, sample**: who we want to describe; the list we sample from; whom we actually observe.
- **Coverage (frame) bias**: error from a frame that differs from the population.
- **Nonresponse bias**: error from response that depends on the answer.
- **Total survey error**: sampling, coverage, nonresponse and measurement error together.
- **Data defect correlation ρ_{R,Y}**: the population correlation of being in the data with the value; Meng's identity.
- **Effective sample size**: the size of an SRS with the same accuracy (Meng's; Kish's for weights; n/deff for
  clusters).
- **Design-based inference**: probability statements from the known selection mechanism, with fixed population values.
- **Purposive selection**: choosing units by judgment to resemble the population.
- **Finite-population correction**: the factor 1 − n/N in an SRS variance.
- **Systematic sampling**: every k-th unit from a random start.
- **Stratification; proportional and Neyman allocation**: sampling within known groups, with n_h ∝ N_h or ∝ N_h S_h.
- **Post-stratification**: weighting to known group shares after sampling.
- **Cluster and multistage sampling**: sampling groups (towns), then units within them.
- **Intraclass correlation; design effect**: within-cluster similarity; the variance ratio 1 + (m − 1)ρ.
- **PPS sampling; Hansen–Hurwitz estimator**: probability proportional to size, with replacement.
- **Inclusion probability πᵢ; design weight 1/πᵢ; Horvitz–Thompson estimator**: Σ yᵢ/πᵢ, unbiased for any design.
- **Hájek estimator**: the weighted mean Σ wᵢyᵢ/Σ wᵢ.
- **Ratio and regression estimators; GREG; calibration**: using auxiliary totals known for the population.
- **Raking (iterative proportional fitting)**: weighting to several margins at once.
- **MAR, MNAR**: response depending only on observed cells, or on the answer itself.
- **Quota sampling**: interviewers fill demographic quotas without random selection.
- **MRP**: multilevel regression and post-stratification.
- **Replicate weights**: alternative weight columns (jackknife, bootstrap) for design-based standard errors.

## Where it comes back

| Idea | Returns in |
|---|---|
| prediction and honest evaluation | 19 |
| a full analysis, question to report | 20 |
| multilevel models and MRP | 25 |
| inverse probability weighting for causal effects | 35 |
| missing data: MCAR, MAR, MNAR, imputation | 41 |
| the efficiency of weighting estimators | 49 |
| privacy for censuses | 63 |
| the Coverage Board | every part; 65 |

## Review clarifications

The cluster simulation deliberately samples towns uniformly and then 50 adults per town. Its unweighted mean overrepresents small towns; the narration identifies the residual bias. The equal-cluster design effect is a working approximation, and the town-based SE does not correct unequal inclusion probabilities.

The zero-variance Horvitz–Thompson ideal requires a fixed sample size and feasible positive inclusion probabilities proportional to the outcome. Independent Poisson inclusion still has random-size variance. The ratio plot now uses the exact cached sample behind its estimate; off-viewport points are omitted rather than relocated, and curves are clipped geometrically.

The raking animation performs four complete income/age rounds and reports their own discrepancy. The final Digest fit separately uses region, age and income. MAR in continuous predictors does not make coarse marginal raking exact. Kish's weight-only diagnostic and a plug-in weighted SE do not establish freedom from selection bias or a valid full design-based variance.

Historical checks: [Wang et al. (2015)](https://5harad.com/papers/forecasting-with-nonrepresentative-polls.pdf) distinguishes 750,148 interviews from 345,858 distinct Xbox respondents. [Meng (2018), author project summary](https://cces.gov.harvard.edu/publications/statistical-paradises-and-paradoxes-big-data-i-law-large-populations-big-data) describes the 2.3-million example as a hypothetical one-percent sample implied by the estimated defect correlation.
