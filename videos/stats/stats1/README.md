# Statistics, Built — Part 1: The Shape of Data

Part 1 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). It is the first part of Stage I, Bachelor's: Foundations. It starts where
statistics started, with John Graunt reading London's Bills of Mortality in 1662, and builds the series' laboratory,
the World: a simulated population of one million whose truth we know. Then it looks at data before any probability:
- histograms, and the centre and spread of data as solutions of optimization problems;
- quantiles, shape and power-law tails, QQ plots and transformations;
- correlation as the cosine of an angle;
- how summaries mislead, and how pictures can.

It ends with the discovery that makes the rest of the series necessary: every summary of a sample is itself random.

Every number on screen is computed in [`compute.py`](compute.py), from the World (`explainer.stats.world`, seed 1662)
or from the Museum's historical tables (`explainer.stats.museum`, each with its source). Simulated data are tagged
`simulated`, historical data `historical data` with the source, and made-up examples `illustrative`.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the
[top-level README](../../README.md):

```bash
python -m videos.stats.stats1.compute          # once: every computed item (about a minute; cached in .cache/stats1)
python tools/build.py stats1 -q l              # fast 480p preview
python tools/build.py stats1                   # 1080p30 -> renders/stats1.mp4
python tools/qa_scene.py stats1 Center         # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats1 --floor 50
```

## Chapters (about 63 minutes, silent estimate)

| # | Scene | What it establishes | Computed or shown |
|---|---|---|---|
| 0 | `Hook` | Graunt (1662): the Bills of Mortality; burials exceed christenings, so London grows by migration; the male surplus (Graunt's 14 to 13); the first life table. The series' question, the five stages, Part 1's objectives. | Christenings, burials and plague deaths 1629–1710 (Arbuthnot 1710; Creighton); the 1665 plague (97,306 burials, 68,596 of plague); the sex ratio of Graunt's years (1.076); Graunt's table of 100 conceived. |
| 1 | `Populations` | Population and parameter (θ, gold); sample and statistic (θ̂, blue); the error θ̂ − θ; in real life θ is hidden; the 95% promise and the empty Coverage Board; colour is meaning. | One sample of 25 adult heights against the World's mean (169.50 cm); twenty 95% intervals, 18 covering. |
| 2 | `TheWorld` | Why build a world; the island of 200 towns in 10 regions; ages, heights, incomes; the truth table; reproducibility and stability (one random stream per block); the World teaches about methods, the Museum about history. | Town populations (Zipf); the age pyramid; heights (men 176.0, women 163.0); incomes (median 38,910, mean 49,484, top 1% share 6.8%). |
| 3 | `Pictures` | Tukey; dot plots; histograms (Pearson's name); the density scale (area = proportion); bin width as a variance–bias choice; Sturges, Scott, Freedman–Diaconis; the population laid over the sample. | 200 adult heights; bin widths 5.45, 6.37, 6.07 cm; the population density. |
| 4 | `Center` | The mean minimizes Σ(xᵢ − c)² (derived); the median minimizes Σ\|xᵢ − c\| (the tug of war); the median ignores distance, the mean does not; the Lᵖ family from median (p = 1) to midrange (p = ∞), and the mode as p → 0; the Fréchet mean on a clock. | Nine incomes (mean 52.8k, median 36.4k); Lᵖ centres of 200 incomes (41.7 → 185.1k; midrange 201.4k); the mode window; six bedtimes (arithmetic mean 11:58 am, Fréchet mean 11:58 pm). |
| 5 | `Spread` | Deviations sum to zero; variance as the average square; SD as its side; Pythagoras in R³: Σ(x − c)² = Σ(x − x̄)² + n(x̄ − c)²; MAD and IQR; Chebyshev's guarantee. | Seven heights (s = 7.17); three heights in R³; SD/MAD/IQR of heights (9.37/10.18/10.21) and incomes (56,852/22,743/24,707); shares within k SDs. |
| 6 | `Quantiles` | The ECDF; quantiles as its generalized inverse (the reflected staircase); Tukey's five numbers and box plot; outliers as a flag, not a verdict; regional box plots that differ only by chance. | 40 incomes (median 38.6k, five outliers); 300 incomes in each of 10 regions against the true regional medians. |
| 7 | `Shape` | Skewness and kurtosis (tails, not peaks: Westfall 2014); with a Pareto tail of exponent 2.1 the third and fourth moments do not exist, so the sample skewness never settles; the log scale; Pareto's law, the log–log slope and Hill's estimator. | Skewness 0.11 (heights) and 72 (incomes, 39.9 of it from one adult); skewness at n = 1,000 … 741,311; log-income skewness 0.26; slope −2.18, Hill 2.17, true α = 2.1. |
| 8 | `QQ` | Building a QQ plot; why a location–scale family gives a straight line (derived); Quetelet's chests; reading the bends: straight, convex (right skew), S-shaped (heavy tails). | 15 men's heights; Quetelet's 5,732 chests (Stigler's corrected table): intercept 39.85 = mean, slope 2.11 ≈ SD 2.07; QQ plots of men, incomes, t₃. |
| 9 | `Transform` | The Box–Cox family and its λ → 0 limit (derived); the histogram straightening as λ turns; the profile log-likelihood with its Jacobian; variance stabilization by √ for Poisson counts (delta method). | 300 incomes: skewness at λ = 1, ½, 0, −½; λ̂ = −0.09, likelihood interval −0.21 to 0.02; Poisson SDs 1.38 … 11.04 → 0.62 … 0.49. |
| 10 | `Correlation` | Quadrants, products, covariance, r; r as the cosine of the angle between centred vectors; −1 ≤ r ≤ 1 by Cauchy–Schwarz (proved); r is not the slope; restriction of range. | 400 World families (r = 0.46, slope 0.64, Galton's two-thirds); (2, 5, 8) and (3, 3.5, 7.5) at 24.2°, cos = 0.912 = r; the tallest quarter: r = 0.19. |
| 11 | `SameStats` | Anscombe's quartet; same statistics, different graphs by simulated annealing (Matejka & Fitzmaurice 2017); a summary as a projection. | The quartet's statistics; 142 World adults annealed into STATS and into a ring, the five statistics read live from every frame (each frame is a real snapshot of the search). |
| 12 | `Simpson` | Better in every group, worse overall; the weighted-average mechanism; which comparison is right depends on the causal story (Part 36); the ecological fallacy (Robinson 1950). | The World's clinic: 62.4% vs 73.7% overall; 87.2% vs 79.5% (mild), 47.6% vs 39.5% (severe); 63% vs 15% severe. |
| 13 | `Integrity` | Playfair's charts; Nightingale's rose (area, not radius); Minard's march; Cleveland & McGill's ranking of encodings; Tufte's lie factor. | Playfair's wheat and wages (1565–1821); Nightingale's monthly death rates (11,157 disease deaths in the first year); Minard's main column (340,000 → 100,000 → 4,000); a lie factor of 98. |
| 14 | `Random` | Every summary is random; the SamplingMachine; twenty samples' histograms; the sampling distribution of the mean and its standard error. | 20 + 2,000 samples of 100 heights: SD of the means 0.951 vs σ/√n = 0.937. |
| 15 | `Outro` | Recap in fourteen lines; where each idea returns; problems; references; the Transcript; Part 2's question. | — |

## Sources

* J. Graunt, *Natural and Political Observations Made upon the Bills of Mortality* (1662). J. Arbuthnot, "An argument
  for Divine Providence …", *Phil. Trans.* 27 (1710). Burials and plague deaths from C. Creighton, *A History of
  Epidemics in Britain*, as compiled by R. B. Campbell (2001), via the R package HistData (M. Friendly).
* A. Quetelet, *Lettres … sur la théorie des probabilités* (1846); the chest table as corrected by S. M. Stigler,
  *The History of Statistics* (1986), p. 208.
* F. Galton, "Regression towards mediocrity in hereditary stature" (1886). V. Pareto, *Cours d'économie politique*
  (1896). W. S. Robinson, "Ecological correlations and the behavior of individuals" (1950).
* G. Box & D. Cox, "An analysis of transformations" (1964). M. Wilk & R. Gnanadesikan, "Probability plotting methods
  for the analysis of data" (1968). F. Anscombe, "Graphs in statistical analysis" (1973).
* W. Playfair, *The Commercial and Political Atlas* (1786) and *A Letter on our Agricultural Distresses* (1821).
  F. Nightingale, *Notes on Matters Affecting the Health … of the British Army* (1858), data via Pearson & Short
  (2007). C. J. Minard (1869), data via L. Wilkinson, *The Grammar of Graphics*.
* W. Cleveland & R. McGill, "Graphical perception" (1984). E. Tufte, *The Visual Display of Quantitative Information*
  (1983). A. Clauset, C. Shalizi & M. Newman, "Power-law distributions in empirical data" (2009). P. Westfall,
  "Kurtosis as peakedness, 1905–2014. R.I.P." (2014). J. Matejka & G. Fitzmaurice, "Same stats, different graphs"
  (2017).
* Books: Tukey, *Exploratory Data Analysis* (1977); Freedman, Pisani & Purves, *Statistics*; Cleveland, *Visualizing
  Data*; Stigler, *The History of Statistics* and *The Seven Pillars of Statistical Wisdom*; Hacking, *The Taming of
  Chance*.

## Problems and solutions

**1. The median minimizes the sum of absolute deviations.**
Let f(c) = Σ|xᵢ − c|. Away from the data points, f is linear with slope
L(c) − R(c), the number of points below c minus the number above. Sort the data.
- *n odd* (n = 2m + 1): the slope is negative for c < x₍ₘ₊₁₎ and positive after, so the unique minimizer is the
  median x₍ₘ₊₁₎.
- *n even* (n = 2m): the slope is zero on the whole interval [x₍ₘ₎, x₍ₘ₊₁₎], and every point of it minimizes f. The
  minimizer is unique only when x₍ₘ₎ = x₍ₘ₊₁₎.

**2. Pythagoras for sums of squares.**
Write xᵢ − c = (xᵢ − x̄) + (x̄ − c) and square:

  Σ(xᵢ − c)² = Σ(xᵢ − x̄)² + 2(x̄ − c)Σ(xᵢ − x̄) + n(x̄ − c)².

The middle sum is zero, because deviations from the mean sum to zero. So
Σ(xᵢ − c)² = Σ(xᵢ − x̄)² + n(x̄ − c)², which is at least Σ(xᵢ − x̄)², with equality exactly when c = x̄.

**3. Summarizing 1, 2, 3, 4, 100.**
- Centre: mean 22, median 3.
- SD (divisor n): √1522 ≈ 39.0.
- MAD: the absolute deviations from the median are 2, 1, 0, 1, 97, whose median is 1. Scaled by 1.4826, ≈ 1.48.
- IQR: with numpy's interpolation, Q₁ = 2 and Q₃ = 4, so IQR = 2.

The median, MAD and IQR describe the four typical values. The mean and SD are dominated by the single 100, and
describe no observation at all.

**4. Correlation under a change of units.**
Let x′ = a + bx.
- Centring removes a, and both the covariance and s_x scale by |b| (the covariance with its sign, b). So
  r′ = b·cov / (|b| s_x s_y) = sign(b)·r: unchanged for b > 0, sign flipped for b < 0.
- The slope of y on x′ is cov/(b s_x²), the old slope divided by b.

**5. Building a Simpson reversal.**
Take mild cases with treated 90 of 100 recovering against untreated 800 of 1,000, and severe cases with treated 300
of 1,000 against untreated 20 of 100.
- Within each group the treatment is better: 90% vs 80%, and 30% vs 20%.
- Overall it is worse: treated (90 + 300)/1,100 = 35.5%, untreated (800 + 20)/1,100 = 74.5%.
- Each overall rate is a weighted average of its group rates. For the treated, (100/1,100)·0.9 + (1,000/1,100)·0.3;
  for the untreated, (1,000/1,100)·0.8 + (100/1,100)·0.2. The weights, the share of severe cases, are what differ.

**6. Stabilizing an exponential.**
By the delta method, SD(g(X)) ≈ |g′(μ)|·SD(X) = |g′(μ)|·μ. This is constant when g′(μ) ∝ 1/μ, that is g = log. In
fact, if X is exponential with mean μ, then log X = log μ + log E with E standard exponential. The spread of log X
does not depend on μ at all; only its location moves.
