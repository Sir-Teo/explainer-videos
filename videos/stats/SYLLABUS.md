# Statistics, Built: the syllabus (plan of record, draft 1)

The goal is a graduate course in mathematical statistics on video, **as comprehensive and as technical as the
standard texts and as close to the current research frontier as possible**, which also tells **how statistics
became what it is**. It is made to the standard of *Analysis, Built* and *AI, Built*: in English and Chinese, every
derivation on screen, every number computed or cited, rendering on macOS and Linux.

Scale: 36 parts of **50–60 minutes** each, about 33 hours in all. That is roughly 15–18 chapters per part, about
250k narration words per language, and 5–6k lines of scene code per part.

The series is made by **one agent working through the parts in order** (no subagents or workflows). It follows the
procedures in [`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md), adapted in §1 below.

Contents:

1. The standard every part meets
2. The World
3. The Coverage Board
4. The Museum
5. statkit
6. Part by part
7. Phases
8. Progress

## 1. The standard every part meets

**A chapter is a lecture segment of 3–4 minutes.** It runs in this order:

1. A motivating question, failure or historical moment.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("Jensen", "tower property", "Cauchy–Schwarz",
   "complete the square", "union bound", "Taylor to second order").
4. A computed experiment that checks the result, usually on the World, sometimes on Museum data.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**

- A cold-open hook (2–4 min): the historical problem the part answers, with its people, place and year.
- An objectives card, theorem and definition cards, and at least one complete proof on screen.
- **One build.** A tool or toy the part constructs and the viewer watches working (a statkit module, a simulator, a
  game).
- **Coverage Board rows** for every interval or test the part introduces (§3).
- A problem set: 5–6 problems, about 90 s on screen, with full solutions in the part's README in English and
  Chinese.
- A reference card: textbooks, the classic papers, and the frontier papers.
- An outro that recaps the part and poses the next part's question, so the parts read as one story.

**The history thread.** Each idea is credited with its people and year. Each part opens with its era on the
timeline strip (`explainer.stats.timeline`, 1650–2030). The disputes are told as disputes: Gauss and Legendre,
Pearson and Fisher, Fisher and Neyman, Bayesians and frequentists, Fisher on smoking, the credibility revolution,
the replication crisis. Uncomfortable history is acknowledged where it is part of the record, such as the eugenic
aims of Galton, Pearson and Fisher, or where a classic dataset was published.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources (journal articles,
arXiv, official reports) up to the writing date. Items below marked *(verify)* are specific numbers or recent results
that must be confirmed in the primary source before they go on screen. If a claim cannot be checked, it is not used.

**Numbers are real.**

- Computed numbers come from the part's `compute.py`, cached under `.cache/statsN/`. Published numbers are cited on
  screen.
- Tags: `computed`, `simulated` (the World), `historical data` (the Museum, with source), `illustrative`,
  `schematic`.
- The narration follows the data. Where the story depends on a result, the verdict is computed and the sentence
  branches on it (LECTURE_GUIDE "Narration follows the data"). A bootstrap interval that covers 93.1% is reported
  as 93.1%.
- CPU budget: ≤ 2 h per part. Coverage simulations are vectorized in numpy, 10,000 replications by default and
  2,000 when one replication is expensive.
- Named exceptions are resumable (`CACHE.partial`) and seeded: the Donoho–Tanner sweep (25), the NUTS runs (19),
  the random-matrix sweeps (24) and the full board (36).
- Scene assertions use tolerances.

**Visual standard** (3Blue1Brown manner). Continuity over cuts, in-place derivations (`cmath` + `morph`, `ladder` +
`why`), colour as meaning, a narrating camera, and live quantities.

Colour tokens (`explainer/stats/style.py`), fixed for the whole series:

| Token | Meaning |
|---|---|
| `C.TRUTH` (gold) | θ, μ, the true curve |
| `C.EST` (blue) | θ̂, fitted curves |
| `C.DATA` (white) | observations |
| `C.NULL` (grey) | H₀ and the null distribution |
| `C.ALT` (teal) | H₁ |
| `C.PRIOR` (purple), `C.LIK` (green), `C.POST` (orange) | prior, likelihood, posterior |
| `C.RESID` (red) | residuals and errors |
| `C.TREAT` (coral), `C.CTRL` (sky) | treated units, controls |
| `C.KEPT` (green), `C.BROKEN` (red), `C.CONS` (blue) | Board verdicts |
| `C.MISSING` | hollow markers |

New instruments, in `explainer/stats/viz.py`:

| Instrument | What it shows | First used |
|---|---|---|
| `SamplingMachine` | population → sample (dots fly out) → statistic → a growing histogram of the sampling distribution | 1, 7 |
| `IntervalRain` | intervals falling against the truth line; misses turn red; a live coverage counter | 7, 11 |
| `NSpace` | a sample as a vector in Rⁿ (n = 3, camera orbit): projections, residuals, χ² as length² | 1, 7, 14 |
| `BeltConstruction` | Neyman's confidence belt in the (θ, x) plane, read horizontally | 11 |
| `LikelihoodLandscape` | 3D log-likelihood with score, curvature, profile ridge and the test trinity | 9, 10 |
| `BayesUpdate` | prior × likelihood → posterior, pointwise product then renormalization | 18 |
| `GaltonBoard` | balls through pegs into bins (physics, seeded) | 5 |
| `ShrinkageField` | estimates in 3D pulled toward a target, with the risk readout | 12, 17 |
| `KernelSum` | KDE as a sum of bumps, with a bandwidth slider | 23 |
| `InfluenceProbe` | drag one point; mean, median, Huber, OLS and LTS respond | 14, 22 |
| `BootstrapResampler` | copies drawn with replacement; the bootstrap world beside the real one | 21 |
| `SpectrumBulk` | eigenvalue histogram against Marchenko–Pastur; the BBP outlier | 24 |
| `L1Geometry` | ℓq balls (2D and 3D) meeting elliptical contours; soft-threshold maps | 25 |
| `PValueSea` | thousands of p-values sorted, with the BH line sweeping | 26 |
| `CausalGraph` | DAGs with association pulses along open paths; blocking and colliders | 29, 30 |
| `ScienceTable` | the potential-outcomes table, half its cells hidden (in the World, revealed) | 28 |
| `KalmanEllipses` | predict and update as moving, shrinking Gaussian ellipses | 31 |
| `KMStaircase` | survival steps with the risk set leaving (events vs censoring) | 33 |
| `FieldSurface` | a kriging or GP surface in 3D with variance shading and sample sites | 32 |
| `BettingPaths` | many wealth processes against Ville's 1/α ceiling; confidence sequences narrowing | 6, 35 |
| `Board` | the Coverage Board itself (§3) | 7 onward |

**Bilingual standard (as *AI, Built*).**

- Every narration line has its `narration_zh.json` entry, and each part has a `zh_lines.py` template table.
- Every on-screen string is in `stats_text_zh.json`, and `tools/collect_text.py --check statsN` is clean.
- The terms are in `STATS_ZH_GUIDE.md`, seeded with the standard Chinese terminology (置信区间, 假设检验, 极大似然估计,
  充分统计量, 一致最小方差无偏估计, 收缩估计, 经验贝叶斯, 自助法, 刀切法, 稳健统计, 核密度估计, 错误发现率,
  共形预测, 倾向得分, 工具变量, 断点回归, 双重差分, 合成控制, 删失, 风险函数, 克里金, 变差函数, 序贯检验,
  e 值, 置信序列, …) and extended for every new term.

**Gates per part:**

- `tools/lecture_length.py`: an estimate before render and the measured length after. It fails under 50 min (the
  series target is 50–60).
- `contact_sheet.py`, `dead_air.py`, `collect_text.py --check`, `check_narration.py`.
- `tests/test_stats_*`: statkit against references, World invariants, and Board reproducibility.
- The QA evidence loop of *AI, Built* (`qa_series.py --series stats`).

## 2. The World

`explainer/stats/world.py`: `World(seed=1662)`. The population is generated lazily and in chunks, so that building
it fits in memory on a laptop. It is deterministic given the seed and the World's version, and every attribute's
generating law is documented in the module.

The point is pedagogical. In real data the truth is hidden; in the World every parameter, every potential outcome
and every missing value is known. Every method in the series can therefore be graded, not just applied.
`world.truth(name)` returns the exact population value: means, regression coefficients, the ATE and CATE function,
the hazard, and the field.

| Block | What it holds | Used in |
|---|---|---|
| Geography | 10 regions → 200 towns → households, with (x, y) locations | 17, 32, 34 |
| People | 1,000,000 residents: age, sex, household, town | everywhere |
| Inheritance | heights for 50,000 families (bivariate normal with known heritability; Galton-style) | 1, 4, 14 |
| Money | incomes: a log-normal body with a Pareto tail (known α); households | 1, 3, 7, 21, 34 |
| Schools | 400 schools, students with test scores (school effects, known τ²) | 12, 17 |
| Health | a disease (1% prevalence) and a screening test (known sensitivity and specificity); blood pressure with nonlinear age effects | 2, 16 |
| Treatment | uptake confounded by age and health; Y(0) and Y(1) for everyone; heterogeneous effects; an instrument (distance to a clinic) | 28–30 |
| Policies | a staggered town-level rollout (DiD) and a scholarship at a test-score cutoff (RD) | 30 |
| Lifetimes | Weibull hazards with covariates and frailty; censoring by study end and dropout | 33 |
| Environment | a Matérn pollution field over the map; daily readings at 300 stations | 32 |
| Time | regional daily series: ARMA + seasonality + a change point; a random-walk pair for spurious regression | 31, 35 |
| Surveys | response propensities correlated with income and opinion; a vote intention | 34 |
| Missingness | MCAR, MAR and MNAR masks on chosen variables, each with known mechanism | 34 |
| Errors | data-entry contamination (known rate), measurement error on chosen variables | 14, 22, 34 |
| Genome | 10,000 binary markers in linkage blocks; a trait with 20 causal markers | 25, 26 |
| Expression | 5,000 "genes", 100 with real differences | 26 |
| Factory | serial-numbered production (the tank game); a process with drift | 8, 35 |

Sampling designs are `world.sample(n, design=...)`: simple random, stratified, cluster, PPS, quota, and
self-selected (with the response propensity).

## 3. The Coverage Board

`explainer/stats/board.py`. Each row is `{part, method, setting, nominal, coverage, mc_band, mean_width,
verdict}`.

**The protocol.**

- Replications: R = 10,000 independent samples from the World by default, from seeded streams
  (`numpy.random.SeedSequence(part, row)`).
- Verdicts against the nominal level (95% coverage, or 5% size for tests), with MC standard error √(0.95 · 0.05 / R)
  ≈ 0.22%:
  - **kept** within ±3 MC standard errors;
  - **broken** below;
  - **conservative** above (for tests, the size is compared with 5%).
- Width or power is shown alongside, because an interval that covers by being enormous has kept the promise
  uselessly.
- Each part writes its rows to `.cache/statsN/board.json`. `board.load_all()` gathers them; the Board on screen
  shows the current part's rows lit and the earlier rows dim.

**Planned rows** (the exact settings are fixed in each part's syllabus entry). The verdicts listed are expectations
from the literature. The narration states the measured verdict, whatever it is.

| Part | Rows |
|---|---|
| 7 | z with known σ; z with s at n = 5; t at n = 5; t on skewed incomes at n = 20 and n = 500; the F-test for variances under non-normality (size) |
| 10 | Student vs Welch with unequal variances (size); KS with estimated parameters vs Lilliefors (size); Wald vs LR in small-n logistic (size) |
| 11 | binomial at p = 0.05, n = 50: Wald, Wilson, Agresti–Coull, Clopper–Pearson, Jeffreys; profile-likelihood vs Wald for a rate |
| 13 | Wald CI for a log-odds near the boundary; Hodges-type post-test estimators at local alternatives |
| 14 | classical OLS SE vs HC0/HC3 under heteroskedasticity; iid SE vs cluster-robust on clustered data; few clusters: CR vs wild cluster bootstrap |
| 15 | randomization test (size); split-plot analyzed as a CRD (size) |
| 16 | Poisson SE under overdispersion vs quasi-Poisson and sandwich; logistic Wald vs profile CIs |
| 17 | DerSimonian–Laird vs Hartung–Knapp with 5 studies; Satterthwaite fixed-effect CIs |
| 18 | credible intervals under the true prior vs a wrong prior (frequentist coverage at fixed θ) |
| 20 | naive CI after AIC selection vs data splitting |
| 21 | bootstrap percentile, basic, t and BCa on skewed data at n = 15; the bootstrap for a maximum |
| 22 | t vs Wilcoxon under 10% contamination (size and power); mean vs Hodges–Lehmann CIs |
| 23 | KDE pointwise CI at the MSE-optimal bandwidth vs robust bias-corrected |
| 24 | Hotelling T² as p/n grows (size and power) vs Chen–Qin |
| 25 | naive post-lasso CI vs debiased lasso vs exact post-selection |
| 26 | realized FDR of BH under independence and dependence; BY; marginal CIs for selected effects vs FCR-adjusted |
| 27 | split conformal; conformal under covariate shift, unweighted vs weighted; naive "predictions as data" vs classical vs PPI; random-forest IJ intervals |
| 28 | naive difference under confounding; difference in means; Neyman's variance (conservative); Lin's adjustment; a cluster trial analyzed per person |
| 29 | regression with misspecified outcome model; IPW; AIPW under the four Kang–Schafer scenarios; ML plug-in vs DML |
| 30 | 2SLS Wald with a weak instrument vs Anderson–Rubin; TWFE under staggered heterogeneous effects vs Callaway–Sant'Anna; conventional vs robust bias-corrected RD |
| 31 | iid CI for an autocorrelated mean vs HAC (Newey–West); the t-test in a spurious regression |
| 32 | kriging prediction intervals with estimated vs true covariance; misspecified smoothness |
| 33 | ignoring censoring; KM Greenwood plain vs log-log at small n |
| 34 | complete-case under MAR; single vs multiple imputation; a self-selected 50% sample vs an SRS of 1,000; MRP; DP-noised small-area counts |
| 35 | a fixed-n CI under continuous peeking; a Hoeffding CS vs a betting CS (time-uniform); the naive CI after Thompson sampling vs adaptive weighting |
| 36 | naive vs clustered error bars for a benchmark; unpaired vs paired model comparisons |

## 4. The Museum

`explainer/stats/museum.py` holds the historical datasets as typed Python data, each with its citation, the page or
table it came from, and a provenance note. The policy:

- **Published before 1931 or a US government work.** Transcribed from the original and stored in the repo:
  Graunt, Arbuthnot, Laplace's births, Quetelet, Snow, Galton, Weldon/Pearson, Bortkiewicz, Cushny–Peebles/Student,
  Yule, Newcomb, Michelson, Mendel, Darwin's *Zea mays*, Toussoun's Nile minima, NOAA Mauna Loa CO₂, NPS geyser
  records, and the Challenger Commission's O-ring table.
- **Modern small published tables** (Efron–Morris, the eight schools, the law-school sample, Freireich/Gehan, the
  Berkeley totals, Literary Digest figures, Card–Krueger means). Transcribed as facts with citation, after checking
  that this is permissible.
- **Modern datasets with a license.** Downloaded at compute time from the original source with a checksum, as *AI,
  Built* fetches Gutenberg (NSW/LaLonde, Prop 99, the prostate microarray, Old Faithful if not NPS). If
  redistribution or use is unclear, a World analogue is used instead, and the screen says so.
- Every dataset goes into `docs/CREDITS.md`.

## 5. statkit

`explainer/stats/kit/` is a small library written for reading: short functions, docstrings that cite the
derivation's part and chapter, and numpy/scipy only. Each module has a test file that checks it against SciPy and,
for models, statsmodels (a test-only dependency).

| Module | Contents | Part |
|---|---|---|
| `random` | a PCG-style generator; inverse CDF, rejection, Box–Muller, Marsaglia–Tsang, alias method | 3 |
| `ecdf`, `gof` | ECDF, DKW band, KS (exact and asymptotic), Anderson–Darling, Lilliefors | 5, 6, 10 |
| `estimate` | moments, plug-in, delta-method SEs | 7 |
| `mle` | Newton/Fisher scoring, observed information, profile likelihood, EM | 9 |
| `tests` | z, t, Welch, χ², G, Fisher exact, permutation, TOST | 10 |
| `intervals` | binomial family, likelihood intervals, Fieller, Scheffé, tolerance | 11 |
| `shrink` | James–Stein, SURE, empirical Bayes, Tweedie, NPMLE | 12 |
| `ols` | QR least squares, influence diagnostics, HC0–HC3, cluster-robust, quantile regression (LP) | 14 |
| `design` | ANOVA tables, factorial effects (Yates), fractional factorials, D-optimal design | 15 |
| `glm` | IRLS for the exponential dispersion family, deviance, quasi-likelihood, Firth, GEE | 16 |
| `mixed` | LMM by profiled REML, BLUPs, Laplace GLMM | 17 |
| `bayes`, `ppl` | conjugate updates, grid posteriors; a tiny probabilistic programming language (autodiff log density from `explainer/ai/autodiff.py`, NUTS, R̂/ESS, SBC) | 18, 19 |
| `select` | AIC/BIC/Cp, CV/GCV, PSIS-LOO, stacking | 20 |
| `bootstrap` | percentile, basic, t, BCa, wild, block, m-out-of-n | 21 |
| `ranks`, `robust` | Wilcoxon (exact), Mann–Whitney, Hodges–Lehmann, Huber/biweight M, LTS (FAST-LTS), MCD, median-of-means | 22 |
| `smooth` | KDE (Silverman, LSCV, Sheather–Jones), local linear, smoothing spline (Reinsch), PAVA | 23 |
| `multi` | Hotelling, PCA, factor analysis, CCA, MDS, Ledoit–Wolf, graphical lasso | 24 |
| `sparse` | coordinate-descent lasso and elastic net paths, debiased lasso, polyhedral post-selection | 25 |
| `multiple` | Holm, Hochberg, BH, BY, Storey, local fdr, knockoffs | 26 |
| `conformal`, `ppi` | split, jackknife+, CV+, CQR, weighted, adaptive conformal; PPI and PPI++ | 27 |
| `causal` | difference in means with Neyman SE, Lin, IPW, AIPW, cross-fitted DML, a causal forest | 28, 29 |
| `quasi` | 2SLS, Anderson–Rubin, local-linear RD with robust bias correction, Callaway–Sant'Anna, synthetic control | 30 |
| `ts` | ARMA likelihood, Yule–Walker, periodogram and multitaper, Dickey–Fuller, GARCH(1,1), Kalman filter and RTS smoother | 31 |
| `spatial` | variogram, kriging, Matérn likelihood, Vecchia, Ripley's K | 32 |
| `survival` | Kaplan–Meier, Nelson–Aalen, log-rank, Cox (Breslow/Efron ties), Aalen–Johansen | 33 |
| `survey`, `mi` | Horvitz–Thompson, stratified and cluster SEs, raking, GREG; MICE-lite with Rubin's rules | 34 |
| `sequential` | SPRT, alpha spending, mixture and betting confidence sequences, e-BH, CUSUM | 35 |
| `evals` | clustered and paired eval errors, Bradley–Terry with sandwich SEs | 36 |

## 6. Part by part

Lengths are targets. Each part's chapter list is locked at its frontier sweep; content decides.

### Act I · Data and Chance

#### Part 1 · The Shape of Data (~52 min; the pilot)
*Question:* what can you know about what you cannot see?
*Story:* Graunt turns a list of deaths into knowledge of the living, and we build a world whose truth we know. Then
we find that every summary we compute jiggles from sample to sample. A statistic is random, so we need the language
of chance (→ Part 2).

0. **Hook: the Bills of Mortality (1662).**
   - Graunt's tables of christenings and burials, the plague years, and the male surplus at birth (tested in Part
     10).
   - His estimate of London's size, and Halley's Breslau life table (1693).
1. **Populations and samples.** Parameters vs statistics; the gap between them as the subject of the series; the
   "95% promise" and the empty Coverage Board.
2. **Building the World.**
   - Its design (§2), and why a known truth makes honest teaching possible.
   - The `simulated` tag. A tour of the World's map, families, incomes, schools and clinics.
3. **Pictures first.**
   - Dot plots and histograms. Bin width as a choice: Sturges (1926), Scott (1979), Freedman–Diaconis (1981). The
     same data told as three stories.
   - The bin-width rules are derived in Part 23.
4. **The centre as an optimization.**
   - The mean minimizes Σ(xᵢ − c)². The median minimizes Σ|xᵢ − c|: the subgradient as a tug-of-war between the
     points on either side. The mode is the limit of 0–1 loss, and the midrange the L∞ centre.
   - The Lᵖ centre sliding as p goes from 1 to ∞ (animated).
   - The Fréchet mean on a circle: averaging clock times.
5. **Spread.**
   - Σ(xᵢ − c)² = Σ(xᵢ − x̄)² + n(x̄ − c)², the first variance decomposition (Pythagoras in Rⁿ, drawn with
     `NSpace`).
   - The standard deviation, MAD and IQR. Chebyshev's guarantee (proved in Part 5).
6. **Quantiles and the ECDF.** The staircase; the quantile function as its generalized inverse; Tukey's five
   numbers and the box plot (1970/1977); what counts as an outlier.
7. **Shape.**
   - Skewness. Kurtosis as a measure of tails rather than peakedness (Westfall 2014).
   - Pareto's income law (1896) in the World's incomes: log scales, and the gap between mean and median.
8. **Comparing with a model.**
   - The QQ plot (Wilk & Gnanadesikan 1968). Why a straight line means the same family up to location and scale
     (derived), and how to read curvature as skew or heavy tails.
   - Quetelet's 5,738 Scottish chests (1846) against the normal.
9. **Transformations.** Log, square root, Box–Cox (1964), whose likelihood comes in Part 9. Variance-stabilizing
   transforms for Poisson (√) and binomial (arcsine) data (derived by the delta method in Part 5).
10. **Two variables.**
    - Covariance; correlation as the cosine between centred vectors (the geometry in Rⁿ); |r| ≤ 1 by
      Cauchy–Schwarz.
    - Correlation is not slope; restriction of range.
11. **Same statistics, different pictures.**
    - Anscombe's quartet (1973), computed.
    - *Built:* the Matejka–Fitzmaurice (2017) simulated-annealing morph, holding the means, SDs and r to two
      decimals while a cloud morphs from a circle to the word STATS.
12. **Traps of aggregation.** Simpson's paradox in the World (a treatment that helps in every region and hurts
    overall; resolved in Part 29); Robinson's ecological fallacy (1950).
13. **Graphical integrity.** Playfair (1786), Nightingale's rose (1858), Minard (1869); Cleveland & McGill's (1984)
    ranking of graphical perception; misleading axes.
14. **The sample is random.** Twenty samples of 100 from the World: the histograms jitter, the means jitter. The
    `SamplingMachine` runs for the first time.
15. **Outro.** The map of the series (eight acts and a finale), the problems, and the references.

*Built:* the World (v1); the same-statistics morph engine.
*Computed:* World summaries against their truths; Anscombe's statistics; the morph's statistics, asserted within
0.01; Quetelet's normal fit; Simpson's reversal in the World.
*Data:* Graunt (1662); Quetelet (1846); Anscombe (1973).
*Visuals:* the Lᵖ centre gliding as p changes; Rⁿ Pythagoras; the dino-to-STATS morph; the first samples flying
out of the World.

#### Part 2 · Chance, Counted (~55)
*Question:* how do you reason exactly about what might happen?
*Story:* an interrupted dice game in 1654 forces the invention of expected value. Paradoxes force the invention of
sample spaces. A courtroom shows what a transposed conditional costs. And random variables arrive with
distributions whose shapes need naming (→ Part 3).

0. **Hook: the problem of points.** A game to three interrupted at 2–1: how to split the stake? Fermat's
   enumeration vs Pascal's recursion (1654), both computed.
1. **Before axioms.** Cardano; Galileo's three dice (why a total of 10 comes up more often than 9: 27 ways vs 25,
   enumerated); Huygens (1657) and expectation.
2. **Counting.** Permutations, combinations, multinomials, stars and bars; the counting visual of choosing seats.
3. **Bertrand's paradox (1889).** Three "random chords" give 1/3, 1/2 and 1/4 (simulated). "Random" needs a
   measure.
4. **Kolmogorov's axioms (1933).**
   - σ-algebras, and why not every set gets a probability (Vitali; cross-reference *Analysis, Built* Part 5).
   - Consequences:
     - inclusion–exclusion;
     - derangements → 1/e (the hat-check problem, computed);
     - continuity of probability;
     - the union bound.
5. **Conditioning.** Renormalizing a slice; the multiplication rule; the law of total probability as a tree.
6. **Bayes' theorem.**
   - The odds form and the likelihood ratio.
   - The World's screening test (1% prevalence, 95% accuracy) and natural frequencies (Gigerenzer).
7. **The prosecutor's fallacy.**
   - The Sally Clark case (1999; Royal Statistical Society statement 2001; conviction quashed 2003): the false
     independence behind "1 in 73 million" and the transposed conditional.
   - Told with care, from the published record.
8. **Monty Hall** (Selvin 1975; vos Savant 1990). Conditioning on the host's protocol, and variants where the answer
   changes (an ignorant host), all enumerated exactly.
9. **Independence.**
   - Pairwise but not mutual (Bernstein's tetrahedron); conditional independence.
   - Simpson as a conditioning phenomenon.
10. **Random variables.** Functions on Ω; the distribution as a push-forward; CDFs (right-continuity, limits);
    discrete, continuous, mixed and singular (the Cantor distribution; cross-reference *Analysis* Part 1's Cantor
    function).
11. **Expectation.**
    - The layer-cake formula E X = ∫₀^∞ P(X > t) dt (horizontal vs vertical slicing); LOTUS; linearity.
    - The indicator method:
      - the expected number of fixed points of a permutation is 1;
      - expected birthday coincidences;
      - the coupon collector's nH_n (computed).
12. **Variance and moments.**
    - Var of sums.
    - St. Petersburg (D. Bernoulli 1738): infinite expectation, running sample means drifting upward, log utility.
13. **Generating functions, first look.** The pgf of dice sums; convolution as multiplication of polynomials.
14. **What probability means.**
    - Frequentist, logical and subjective readings (von Mises, Keynes, Ramsey, de Finetti).
    - The Dutch book argument (de Finetti 1937) recovering the axioms; Cox's theorem (1946).
15. **Outro.**

*Built:* an exact probability engine on finite sample spaces, using Python fractions. It enumerates Pascal–Fermat,
Galileo, Monty Hall and the derangements, and is checked against simulation.
*Visuals:* the sample space as a square being sliced and renormalized; Bertrand's three chord machines side by
side; layer-cake expectation.

#### Part 3 · The Family of Distributions (~56)
*Question:* why do the same few shapes keep appearing?
*Story:* deaths by horse kick follow a formula, and every distribution turns out to be a relative of a few others.
The family tree is assembled arrow by arrow, and then we generate every member from a single uniform random number.
One variable at a time is not enough (→ Part 4).

0. **Hook: Bortkiewicz (1898).** 200 corps-years of Prussian cavalry deaths: 109, 65, 22, 3, 1, against Poisson(0.61):
   108.7, 66.3, 20.2, 4.1, 0.6.
1. **Bernoulli → binomial.** Pascal's triangle as lattice paths; mean and variance by indicators.
2. **The law of rare events.** Binomial(n, λ/n) → Poisson (derived); Le Cam's inequality (total variation ≤ Σpᵢ²).
3. **Waiting.** Geometric and negative binomial; memorylessness; the negative binomial as a gamma–Poisson mixture
   (overdispersion returns in Part 16).
4. **Without replacement.**
   - The hypergeometric (Fisher's exact test comes in Part 10).
   - Capture–recapture (Lincoln–Petersen), run on the World's lake.
5. **Continuous time.** The Poisson process; exponential gaps; the gamma as the wait for the k-th event; the
   inspection paradox (why your bus wait is longer than average), computed.
6. **The normal, three ways.**
   - de Moivre (1733) from the binomial via Stirling.
   - Gauss (1809): the only error law for which the mean is the best estimate (his argument, derived).
   - Herschel–Maxwell: rotation invariance plus independence forces exp(−r²) (2D picture).
   - The Gaussian integral in polar coordinates.
7. **Transformations.**
   - The CDF method; the Jacobian in 1D and 2D; Box–Muller derived.
   - The log-normal (Galton & McAlister 1879) as a multiplicative CLT.
8. **The sampling family.**
   - χ² (sums of squared normals; Helmert 1876), Student's t, F (Snedecor).
   - Cauchy as t₁ and as a spinning lighthouse's beam on a wall.
   - Beta and gamma relations.
9. **Order statistics.**
   - The density of the k-th; uniform order statistics are Beta.
   - The maximum (the German tank problem, Part 8); spacings and Rényi's exponential representation.
10. **Heavy tails.** Pareto (1896), Zipf; log–log plots and their misuse (Clauset, Shalizi & Newman 2009); log-normal
    vs Pareto.
11. **Generating functions.**
    - The pgf, mgf and characteristic function (Fourier; cross-reference *Analysis* Part 9).
    - Moments from derivatives; uniqueness; sums by products.
    - The Cauchy's e^{−|t|}.
12. **Mixtures and hierarchies.** Beta-binomial, gamma–Poisson, normal scale mixtures → t; hierarchy as a modelling
    idea (Parts 17–18).
13. **Exponential families, first look.** h(x) exp(ηT(x) − A(η)); which of the family are members; why A′(η) is the
    mean (Part 8 develops this).
14. **The family tree** (Leemis & McQueston 2008). The relationship map assembled on screen, each arrow lit as it is
    derived in this part.
15. **One uniform to rule them all.**
    - *Built:* our own PCG-style generator. RANDU's points falling on 15 planes in 3D (Marsaglia 1968), with the
      camera turning until the planes appear.
    - Samplers from one uniform:
      - inverse CDF;
      - rejection (von Neumann 1951);
      - Box–Muller;
      - Marsaglia–Tsang gamma;
      - Walker's alias method.
    - Each sampler is tested by χ² and KS against SciPy.
16. **Outro.**

*Data:* Bortkiewicz (1898).
*Visuals:* the binomial-to-Poisson morph; the Herschel–Maxwell rotation; the RANDU planes; the family tree.

#### Part 4 · Many Variables at Once (~55)
*Question:* what does knowing one thing tell you about another?
*Story:* Galton finds ellipses in a table of heights and discovers regression to the mean. Conditional expectation
turns out to be a projection. The Gaussian's conditionals are linear, so regression is born from geometry, and
exchangeability prepares the way for Bayes. Averages of many variables come next (→ Part 5).

0. **Hook: Galton (1886).** 928 adult children of 205 families; the smoothed table's ellipses (with J. D. Hamilton
   Dickson's surface); "regression towards mediocrity".
1. **Joint, marginal, conditional.** Tables and densities; slicing a 3D density surface and renormalizing the
   slice.
2. **Dependence.** Uncorrelated is not independent (X and X²); the covariance matrix is positive semidefinite
   (proof).
3. **Conditional expectation as projection.**
   - E[Y | X] is the best predictor in mean square: a projection in L² (cross-reference *Analysis* Part 6).
   - The tower property. Kolmogorov's 1933 definition via Radon–Nikodym, sketched.
4. **Eve's law.** Var Y = E Var(Y | X) + Var E(Y | X) as Pythagoras in L²; R² as the share of variance explained.
5. **The multivariate normal.**
   - An affine image of iid normals; its density by the Jacobian; ellipsoids from the eigen-decomposition (3D
     camera tour).
   - Marginals are normal. Uncorrelated implies independent only for a jointly normal pair (with a counterexample).
6. **Conditioning a Gaussian.**
   - The Schur complement, derived by completing the square.
   - The conditional mean is linear in x and the conditional variance is constant: regression is born.
7. **Regression to the mean.**
   - The slope ρσ_y/σ_x. Galton's families recomputed.
   - The sophomore slump; Kahneman's flight instructors; why uncontrolled before–after studies fool us.
8. **Three lines through one ellipse.** Y on X, X on Y, and the major axis.
9. **Many-dimensional change of variables.** The Jacobian; sums by convolution, ratios; the Gaussian in polar
   coordinates (Rayleigh radius, uniform angle).
10. **Latent variables.** A two-component Gaussian mixture surface; marginalizing a latent class.
11. **Copulas.**
    - Sklar's theorem (1959) via the probability integral transform.
    - Gaussian, Clayton and Gumbel copulas: same marginals, different tails; the tail-dependence coefficient.
    - The Gaussian copula in credit pricing (Li 2000) and why zero tail dependence mattered in 2008.
12. **Exchangeability.**
    - Pólya's urn simulated: the limiting fraction is Beta.
    - de Finetti (1931): exchangeable means a mixture of iid, the bridge to Bayes (Part 18). The finite version
      (Diaconis & Freedman 1980).
13. **Measuring dependence.** Pearson, Spearman, Kendall, mutual information, distance correlation (Székely, Rizzo
    & Bakirov 2007) and maximal correlation (Rényi 1959), each run on a gallery of shapes to see which detects
    what.
14. **The simplex.** The multinomial and the Dirichlet; categorical dependence; the simplex as a triangle of
    densities.
15. **Outro.**

*Built:* a Gaussian slicer (cut the density in 3D and watch the conditional appear); a Pólya urn machine.
*Data:* Galton (1886) via Hanley's (2004) transcription of the notebooks.
*Visuals:* the density surface sliced; L² projection; the Schur complement morphing into a regression line.

#### Part 5 · The Laws of Averages (~58)
*Question:* why does averaging work, how fast, and when does it fail?
*Story:* 787 guesses at an ox's weight land within 1% of the truth. We prove why, measure how fast, and break it with
heavy tails. Then we meet the other limit law, for maxima, which decides how high Dutch dikes are built. Dependence
is next (→ Part 6).

0. **Hook: Galton's ox (1907).** 787 tickets; median 1,207 lb against 1,198 lb.
1. **Inequalities as guarantees.** Markov (the area argument), Chebyshev, Jensen (the chord picture),
   Cauchy–Schwarz, Hölder.
2. **Modes of convergence.**
   - Almost sure, in probability, in Lᵖ, in distribution, and the implication diagram.
   - Counterexamples: the typewriter sequence (in probability, not a.s.) and n·1{U < 1/n} (a.s. to 0, not in L¹),
     both animated.
3. **The weak law.**
   - Chebyshev's proof.
   - Jacob Bernoulli's golden theorem (1713) and his 25,550 trials for "moral certainty", against Hoeffding's bound
     and the exact answer (computed).
4. **The strong law.**
   - Both Borel–Cantelli lemmas; the proof with a fourth moment; Etemadi's idea (1981).
   - Borel's normal numbers (1909).
5. **The fundamental theorem of statistics.**
   - Glivenko–Cantelli (1933), proved with a grid of quantiles.
   - DKW (1956) with Massart's constant 2 (1990).
   - *Built:* the DKW band.
6. **Concentration.**
   - Chernoff by exponentiating; Hoeffding's lemma derived; Bernstein.
   - Sub-Gaussian and sub-exponential tails, compared with exact tails.
7. **The CLT, seen.** Repeated convolution of a lopsided distribution; *Built:* a Galton board (seeded physics, pegs
   and bins).
8. **The CLT, proved.** Characteristic functions; a second-order expansion; Lévy's continuity theorem; Lindeberg–Feller
   and Lyapunov conditions; what fails without a variance.
9. **How fast.**
   - Berry–Esseen: |Fₙ − Φ| ≤ Cρ/(σ³√n) with C ≤ 0.4748 (Shevtsova 2011).
   - The Edgeworth correction for skewness, beating the normal approximation at n = 10 (computed; returns in Part
     21).
10. **The toolkit.** Slutsky, continuous mapping, the delta method (derived, explaining Part 1's
    variance-stabilizing transforms), the second-order delta method.
11. **Many dimensions.** The Cramér–Wold device; multinomial → χ² (Pearson's statistic, Part 10).
12. **When averages fail.**
    - The running mean of Cauchy data never settles (computed).
    - Stable laws (Lévy), the generalized CLT for α < 2, domains of attraction.
13. **Maxima, not sums.**
    - Fisher–Tippett–Gnedenko, with max-stability giving the GEV family (Gumbel, Fréchet, Weibull); the
      generalized Pareto for exceedances (Pickands; Balkema–de Haan); return levels.
    - The 1953 North Sea flood and the Delta Works' design standard (van Dantzig 1956). Fit to the World's river
      maxima.
14. **The law of the iterated logarithm** (Khinchin 1924). The √(2n log log n) envelope over a thousand paths;
    anytime-valid inference comes back to it (Part 35).
15. **Large deviations.** Cramér's theorem (1938), the rate function as a Legendre transform (the convex conjugate
    drawn), Sanov's theorem with KL as the rate (cross-reference *AI, Built* Part 1).
16. **Outro.**

*Visuals:* the Galton board in slow motion; the typewriter sequence; convolution powers morphing into the bell; the
LIL envelope; the Legendre transform.

#### Part 6 · Fair Games: Markov Chains and Martingales (~56)
*Question:* what can be said about randomness that unfolds in time?
*Story:* Markov counts vowels in Pushkin to win an argument about independence. Seven shuffles randomize a deck. A
drunk man finds his way home but a drunk bird may not. No betting system beats a fair game, and that last fact,
Ville's inequality, will later rebuild hypothesis testing (Part 35). The language of chance is complete, so we turn
it around and go from data back to the world (→ Part 7).

0. **Hook: Markov (1913).** 20,000 letters of *Eugene Onegin* classified as vowel or consonant, to refute Nekrasov's
   claim that the law of large numbers needs independence. The count is recomputed on the original Russian (public
   domain) and on an English novel.
1. **Markov chains.** Transition matrices; n-step transitions as matrix powers; the chain drawn as a graph with flowing
   probability mass.
2. **Stationary distributions.**
   - Left eigenvectors; Perron–Frobenius for irreducible aperiodic chains.
   - Detailed balance and reversibility; random walks on graphs; PageRank (Brin & Page 1998).
3. **The ergodic theorem.** A law of large numbers without independence (Markov's point); the Markov chain CLT and
   the integrated autocorrelation time, which the MCMC diagnostics of Part 19 use.
4. **Mixing.**
   - Total variation; the spectral gap; coupling (Doeblin 1938).
   - Riffle shuffles (Bayer & Diaconis 1992): the exact total-variation curve via rising sequences, with its cutoff
     near seven shuffles (computed).
5. **Recurrence.**
   - Pólya (1921): a walk returns in 1D and 2D but not in 3D (return probability ≈ 0.3405, computed).
   - It reappears in Stein's paradox (Part 12, Brown 1971).
6. **Martingales.**
   - Fair games and conditional expectation.
   - Examples:
     - the random walk;
     - products of mean-one factors;
     - **likelihood ratios under the null** (the key to Part 35);
     - the Doob martingale of revealed information.
7. **Optional stopping.**
   - Why doubling bets fails: finite credit, and the expected loss.
   - Doob's optional stopping theorem and its conditions; gambler's ruin derived, fair and biased.
8. **Ville's inequality (1939).** P(sup_t M_t ≥ 1/α) ≤ α for a nonnegative martingale starting at 1: "you cannot get
   rich betting against a true hypothesis". Drawn with `BettingPaths`.
9. **Martingale convergence.** The upcrossing argument (visual); Pólya's urn converges (Part 4 revisited); posteriors
   are martingales (Doob 1949; Part 18).
10. **Martingale concentration.** Azuma–Hoeffding, McDiarmid's bounded differences (empty bins, computed), Freedman's
    inequality.
11. **Counting processes.** The Poisson process, its compensator Λ(t), and N(t) − Λ(t) as a martingale: the machinery
    of survival analysis (Part 33).
12. **Brownian motion.**
    - The scaling limit of random walks (Donsker 1951).
    - Continuity, nowhere-differentiability and quadratic variation (cross-reference *Stochastic Calculus,
      Visualized*).
    - The reflection principle and the law of the maximum.
13. **The empirical process.**
    - √n(Fₙ − F) → the Brownian bridge (Doob 1949; Donsker 1952).
    - The Kolmogorov distribution derived through the reflection principle.
    - *Built:* the Kolmogorov–Smirnov test from scratch (Kolmogorov 1933; Smirnov 1939), checked against SciPy.
14. **Outro.** Act I recap: the language of chance, complete.

*Visuals:* Onegin's letters flowing through a two-state chain; the shuffle cutoff; walks in 1D, 2D and 3D with
returns lit; martingale paths and Ville's ceiling; the empirical process wiggling into a Brownian bridge.

### Act II · Inference

#### Part 7 · From Sample to Population (~55)
*Question:* how much does an estimate wobble, and how can one sample tell you?
*Story:* a brewer with four barley samples finds that the normal table lies. Fisher sees the answer as geometry in
n dimensions. The first rows of the Coverage Board go up, one green and one red. Of the many possible estimators,
which ones keep all the information (→ Part 8)?

0. **Hook: Student (1908).** Gosset at Guinness. Before proving the t-distribution he simulated it: 3,000 criminals'
   measurements on cards, shuffled into 750 samples of 4. We redo his experiment on 3,000 World residents.
1. **Sampling distributions.** The `SamplingMachine` on the World; the standard error; σ/√n; why 1,000 people
   suffice for a nation (the finite-population correction is Part 34).
2. **The n − 1.** E s² = σ² derived. The residual vector lives in an (n − 1)-dimensional subspace: degrees of
   freedom as dimension (`NSpace`).
3. **The geometry of a normal sample (Fisher 1915, 1925).**
   - Spherical symmetry. Projecting y onto 1 gives ȳ, and the orthogonal residual gives s².
   - x̄ ⟂ s² proved by a rotation. Camera tour with n = 3.
4. **χ².** The squared length of a spherical Gaussian (Helmert 1876); (n − 1)s²/σ² ~ χ²ₙ₋₁; Cochran's theorem
   (1934): orthogonal projections split a χ².
5. **Student's t.** Z/√(χ²/ν), its density by integrating out the denominator; Gosset's simulation against the
   formula; Fisher's 1925 proof.
6. **F.** A ratio of χ²s; comparing variances; a preview of ANOVA.
7. **Bias, variance, MSE.**
   - MSE = bias² + variance.
   - Biased estimators can win: the n + 1 divisor minimizes the MSE of a normal variance (computed). A first
     glimpse of shrinkage (Part 12).
8. **Consistency and plug-in.** Functionals T(F) estimated by T(Fₙ): mean, variance, quantiles, correlation. Plug-in
   is the bootstrap's philosophy (Part 21).
9. **The method of moments** (Pearson 1894). Gamma and beta fits; its inefficiency, which will lose to likelihood
   (Part 9).
10. **Standard errors for nonlinear statistics.**
    - The delta method for a ratio (income per household).
    - Laplace's 1802 estimate of the population of France: a ratio estimator with his own error analysis, an early
      confidence statement.
11. **Finite populations.** Without replacement; the finite-population correction 1 − n/N derived; the
    hypergeometric variance.
12. **The Coverage Board opens.** (Rows below; these ship as the first board.)
13. **Robustness of normal theory.** The t-test is fairly robust; the F-test for variances is not (Box 1953),
    measured as its size under non-normality.
14. **Outro.**

*Board rows:* x̄ ± 1.96σ/√n (kept); x̄ ± 1.96 s/√n at n = 5 (broken); the t-interval at n = 5 (kept); the
t-interval on skewed incomes at n = 20 (broken) and n = 500 (kept); the F-test's size (broken).
*Data:* Student (1908); Laplace (1802).

#### Part 8 · Data Reduction: Sufficiency and the Best Unbiased Estimator (~55)
*Question:* when does a summary keep everything the data know?
*Story:* serial numbers on captured tanks reveal Germany's production better than spies did. Sufficiency,
completeness and Rao–Blackwell produce the best unbiased estimator; Cramér–Rao says how good any can be, and the
tank problem breaks even that. These ideas need a general recipe (→ Part 9).

0. **Hook: the German tank problem.**
   - Serial numbers of captured tanks against intelligence estimates and, after the war, the German records
     (Ruggles & Brodie 1947; exact figures *(verify)*).
   - The game: k serials drawn from {1, …, N}.
1. **Naive estimators.** 2·mean − 1 and the maximum m, with their sampling distributions computed live.
2. **Sufficiency (Fisher 1922).** The conditional law of the data given T is free of θ. Coin flips: every
   arrangement of a given count is equally likely, so the order carries nothing.
3. **The factorization theorem** (Fisher–Neyman; Halmos–Savage 1949), proved in the discrete case. Examples: the
   normal (x̄, s²), the uniform maximum, the Poisson sum.
4. **Minimal sufficiency.** The likelihood-ratio criterion; the coarsest partition of the sample space (visual); the
   Cauchy location family reduces only to the order statistics.
5. **Exponential families in depth.**
   - Convex natural parameter space; convex A(η) by Hölder; moments as derivatives of A; Fisher information =
     A″(η); the mean-value parametrization.
   - Pitman–Koopman–Darmois: a sufficient statistic of fixed dimension forces an exponential family (under
     regularity).
6. **Rao–Blackwell** (Rao 1945; Blackwell 1947). Conditioning on a sufficient statistic never hurts (Jensen). The
   tank estimator 2X₁ − 1 is Rao–Blackwellized into the UMVUE live.
7. **Completeness and Lehmann–Scheffé (1950).**
   - The tank UMVUE m(k + 1)/k − 1 derived.
   - When unbiasedness is silly: the UMVUE of e^{−2λ} from one Poisson observation is (−1)^X.
8. **Ancillarity and Basu (1955).** Complete sufficient statistics are independent of ancillaries: x̄ ⟂ s² a third
   time. Cox's two instruments (1958) and the conditionality principle.
9. **Fisher information.** The score has mean 0 and variance I(θ) (derived); information as curvature; additivity;
   reparametrization.
10. **Cramér–Rao** (Rao 1945; Cramér 1946).
    - Proof by Cauchy–Schwarz between the estimator and the score; attainment exactly for exponential families in
      the mean-value parameter.
    - The tank problem beats it: the support depends on N, so the variance falls like 1/n², not 1/n (computed).
11. **Many parameters.** The information matrix; the cost of nuisance parameters (efficient information as a Schur
    complement), which returns in semiparametrics (Part 13).
12. **Equivariance.** Location and scale invariance; the Pitman estimator; minimum-risk equivariant estimators.
13. **Sufficiency and information theory.** The data-processing inequality; sufficient statistics preserve KL and
    mutual information (Kullback 1959; cross-reference *AI, Built* Part 1).
14. **Outro.** An MSE board for the tank estimators.

*Built:* the tank factory: a serial-numbered production line in the World, and a game grading the viewer's
estimator against the UMVUE.

#### Part 9 · Likelihood (~58)
*Question:* which parameter makes the data least surprising, and how sure is that?
*Story:* Pearson splits 1,000 crabs into two species by solving a ninth-degree polynomial. Fisher's likelihood and
Dempster, Laird and Rubin's EM do it better, and we watch the likelihood's curvature become the standard error. An
estimate is not a decision: when is a difference real (→ Part 10)?

0. **Hook: Weldon's crabs (1893) and Pearson's nonic (1894).** A lopsided histogram, two hidden species, the method
   of moments; Fisher (1912, 1922) proposes maximum likelihood.
1. **The likelihood function.** A function of θ, not a density in θ; log-likelihood curves sharpening with n.
2. **The MLE.** Score equations; invariance; normal, Poisson, exponential; the uniform's boundary MLE.
3. **Consistency (Wald 1949).** The expected log-likelihood is maximized at θ₀ because KL ≥ 0 (Gibbs); the argmax of a
   random curve converges (visual).
4. **Asymptotic normality.** Expand the score to first order; a CLT for the score, an LLN for the Hessian; √n(θ̂ − θ)
   → N(0, I⁻¹), each step on the ladder.
5. **Observed vs expected information** (Efron & Hinkley 1978). Standard errors as the inverse curvature of the
   fitted parabola.
6. **Computing.** Newton–Raphson and Fisher scoring. Failure: the Cauchy location likelihood has several local
   maxima (drawn).
7. **Nuisance parameters.**
   - The profile likelihood (walking the ridge of a 3D surface).
   - Neyman–Scott (1948): the MLE of σ² with incidental parameters converges to σ²/2 (computed).
8. **EM** (Dempster, Laird & Rubin 1977).
   - Latent species for the crabs: the E-step and M-step; Jensen's lower bound touching the log-likelihood
     (cross-reference *AI, Built* Part 7).
   - Monotonicity proved. The rate of convergence equals the fraction of missing information (Louis 1982 standard
     errors).
   - The crabs refit: EM against Pearson's moments.
9. **When likelihood misbehaves.**
   - Gaussian-mixture likelihoods are unbounded as σ → 0 at a data point (visual spike).
   - Boundary parameters (½χ²₀ + ½χ²₁; Part 17). Label switching.
10. **Misspecification** (Huber 1967; White 1982). The MLE converges to the KL projection; the sandwich A⁻¹BA⁻¹
    derived; when the information equality fails (two curvatures, drawn).
11. **Beyond full likelihood.** Quasi-likelihood (Part 16), composite and pseudo-likelihood (Besag 1975; Part 32),
    and M-estimation (Part 13).
12. **The likelihood principle.**
    - Birnbaum (1962): sufficiency plus conditionality give the likelihood principle.
    - Binomial vs negative-binomial stopping: the same likelihood, different p-values (Lindley & Phillips 1976). This
      is the fault line between the schools (Parts 18, 35).
13. **Pure likelihood inference** (Royall 1997). Support intervals at 1/8 and 1/32, and their relation to χ² cutoffs.
14. **Transformations.** The Box–Cox profile likelihood (Part 1) and the Jacobian's place in the likelihood.
15. **Information geometry, a glimpse.** The Fisher metric (Rao 1945); KL ≈ ½δᵀIδ locally; the natural gradient
    (cross-reference *AI, Built* Part 11).
16. **Outro.**

*Built:* statkit.mle (Newton, scoring, observed-information SEs, profile likelihood, EM); the crabs fitted both ways.
*Data:* Weldon/Pearson (1894).
*Visuals:* the `LikelihoodLandscape` sharpening with n; EM's lower bounds climbing the curve; the mixture spike.

#### Part 10 · Significance (~58)
*Question:* when is a pattern too strong to be chance?
*Story:* eighty-two years of more boys than girls, and a lady who claims to taste the order of milk and tea. Fisher's
p-value and Neyman–Pearson's error rates are two philosophies that became one procedure. A test says yes or no, but
how big is the effect, and how sure are we of its size (→ Part 11)?

0. **Hook: Arbuthnot (1710) and the lady tasting tea (Fisher 1935).** (1/2)⁸² ≈ 2.1 × 10⁻²⁵; eight cups, four with
   milk first: 1/70.
1. **Fisher's logic.** The null hypothesis, a test statistic, a tail probability; Arbuthnot's sign test recomputed.
2. **Exact tests by design.** The tea's permutation distribution (hypergeometric); Fisher's exact test; the
   randomization that makes it valid (Parts 15, 28).
3. **p-values formally.**
   - P_θ₀(T ≥ t_obs). Uniform under H₀ (the probability integral transform, proved).
   - Stochastically smaller under H₁: the p-value's distribution under alternatives, drawn for several effect sizes.
4. **Neyman & Pearson (1933).** Two kinds of error, size and power; the power function; testing as a decision.
5. **The Neyman–Pearson lemma.** Proof as a fractional knapsack: buy the sample points with the best
   likelihood-ratio per unit of α. Randomized tests for discrete data.
6. **UMP tests.** Monotone likelihood ratio and Karlin–Rubin (1956); no UMP two-sided test; unbiased tests and the
   t-test's optimality (Lehmann).
7. **The likelihood ratio test.** Wilks' theorem (1938) from the quadratic expansion; Bartlett's correction.
8. **The trinity.**
   - Wald, score (Rao 1948) and LR, drawn as horizontal, slope and vertical distances on one log-likelihood.
   - Equivalent asymptotically, different in samples. Wald's non-invariance; the Hauck–Donner effect (1977),
     computed.
9. **Pearson's χ² (1900).**
   - Derived as a score test and through the multinomial CLT; degrees of freedom with estimated parameters (Fisher's
     1922 correction).
   - Mendel's peas and Fisher's (1936) "too good to be true", recomputed as a left-tail probability.
10. **Contingency tables.** The independence test, G², Fisher vs χ², and the Yates correction dispute.
11. **Two samples.** Student vs Welch (1947); the Behrens–Fisher problem; Board rows.
12. **Power and sample size.**
    - Noncentral distributions; n for 80% power.
    - Underpowered studies and the winner's curse: type M and type S errors (Gelman & Carlin 2014), computed.
13. **What p-values are not.**
    - p ≠ P(H₀ | data). The dance of the p-values (Cumming).
    - The ASA statement (2016). The Sellke–Bayarri–Berger bound −e·p·log p (2001), previewing Part 18.
14. **Continuous goodness of fit.** KS (Part 6), Anderson–Darling (1952), Cramér–von Mises; estimated parameters
    break KS's null (Lilliefors, computed); Shapiro–Wilk (1965).
15. **Equivalence testing** (TOST; Schuirmann 1987): showing there is no meaningful difference.
16. **Outro.**

*Board rows:* Student vs Welch; KS with estimated parameters vs Lilliefors; Wald vs LR sizes in small-sample logistic
regression.
*Built:* a permutation machine (shuffling labels, the null distribution piling up); statkit.tests.
*Data:* Arbuthnot (1710); Mendel (1866); Fisher (1935).

#### Part 11 · Honest Intervals (~55)
*Question:* what does "95% confident" promise, and which intervals keep the promise?
*Story:* the textbook interval for a proportion fails in a sawtooth. Neyman's construction repairs it, Fieller shows
that an honest interval must sometimes be infinite, and the Coverage Board becomes the series' running judge. If
many estimators are honest, which is best (→ Part 12)?

0. **Hook.** The Wald interval p̂ ± 1.96√(p̂(1 − p̂)/n), whose exact coverage, computed by summing binomial
   probabilities, zigzags below 95% as n changes (Brown, Cai & DasGupta 2001).
1. **Neyman (1937).** Procedures with P_θ(θ ∈ C(X)) ≥ 1 − α for all θ; `IntervalRain` on the World.
2. **Pivots.** Exact intervals for a normal μ and σ², a ratio of variances, an exponential rate.
3. **Inverting tests.** Neyman's belt in the (θ, x) plane, read horizontally (`BeltConstruction`); the duality
   between tests and intervals.
4. **The binomial family.** Wilson (1927) by inverting the score test (the quadratic, derived); Agresti–Coull (1998);
   Clopper–Pearson (1934), exact and conservative; Jeffreys; all with exact coverage curves.
5. **Likelihood intervals.** Wald vs profile likelihood; invariance; the log-odds scale; zero events and the rule of
   three (3/n, derived).
6. **Discreteness.** Exact coverage is impossible for discrete data; randomized intervals; mid-p.
7. **Fieller (1954).**
   - A ratio of means gives intervals that are bounded, the whole line, or two rays (the quadratic inequality,
     drawn).
   - Gleser & Hwang (1987): any procedure that is always finite has coverage zero somewhere. Infinite intervals are
     necessary.
8. **Bounded parameters.** The flip-flop problem; Feldman & Cousins (1998) and likelihood-ratio ordering for
   neutrino-mass limits; the belt computed.
9. **Simultaneous intervals.** Bonferroni; Scheffé (1953) as the shadow of an ellipsoid; Working–Hotelling; the DKW
   band for a whole CDF.
10. **Prediction and tolerance.** Prediction intervals vs confidence intervals; Wilks' (1941) distribution-free
    tolerance limits from order statistics, the ancestor of conformal prediction (Part 27).
11. **Fiducial and confidence distributions.** Fisher's fiducial argument (1930) and its failures; modern
    confidence distributions (Xie & Singh 2013; Schweder & Hjort 2016); the p-value function.
12. **Credible vs confidence.**
    - Where they agree (a normal mean, flat prior) and where they part.
    - Welch's (1939) uniform example: a 95% interval that, on some samples, certainly contains θ. Relevant subsets
      (Buehler 1959).
13. **The Coverage Board, formally.**
    - The protocol of §3: replications, MC bands, verdicts, width.
    - The rows from Parts 7–11.
14. **Outro.**

*Board rows:* Wald, Wilson, Agresti–Coull, Clopper–Pearson and Jeffreys at p = 0.05, n = 50; Wald vs profile
likelihood for a Poisson rate.
*Built:* statkit.intervals; `board.py` in full.

#### Part 12 · The Shock of Shrinkage: Decision Theory and Stein's Paradox (~58)
*Question:* can you do better than estimating each thing by its own average?
*Story:* Efron and Morris predict eighteen batting averages, and shrinking them toward each other wins. Wald's
decision theory says what "better" means. Stein's paradox says the obvious estimator is inadmissible in three
dimensions, for the same reason a random walk escapes in three dimensions. Empirical Bayes turns out to be the
formula at the heart of diffusion models. In large samples, what exactly is optimal (→ Part 13)?

0. **Hook: Efron & Morris (1975).** 18 major-league hitters after 45 at-bats; predicting their season averages;
   James–Stein cuts the total squared error severalfold (recomputed from the published table).
1. **Decision theory (Wald 1950).** Actions, loss, the risk function R(θ, δ); risk curves cross, so nothing is
   uniformly best.
2. **Admissibility, minimax, Bayes.** The risk set for a two-point parameter: its convex hull, Bayes rules as
   supporting lines, minimax as the corner (drawn).
3. **Bayes rules.**
   - Posterior mean, median and mode for squared, absolute and 0–1 loss (Part 1's optimization view again).
   - Bayes rules are admissible. Wald's complete class theorem.
4. **Least favourable priors.** The binomial estimator with √n/2 pseudo-counts has constant risk and is minimax (its
   flat risk curve).
5. **Stein (1956).** In d ≥ 3, X is inadmissible for a normal mean under total squared error, even when the
   coordinates are unrelated.
6. **Stein's lemma.** E[(X − θ)g(X)] = E g′(X) by integration by parts; SURE (Stein 1981), an unbiased estimate of
   risk.
7. **James–Stein (1961).** (1 − (d − 2)/‖X‖²)X; risk d − (d − 2)²E[1/‖X‖²] via SURE; the positive part (Baranchik
   1964); shrinking toward the grand mean; risk curves for d = 3, 10, 100.
8. **Why three dimensions?**
   - E‖X‖² = ‖θ‖² + d, so X is too long.
   - Brown (1971): admissibility ↔ recurrence of Brownian motion, the same dimension count as Pólya's walk (Part 6).
9. **The baseball data.** James–Stein vs MLE vs the season's remainder; the Clemente problem (shrinkage hurts the
   outlier) and limited translation (Efron & Morris 1972).
10. **Empirical Bayes (Robbins 1956).** Estimate the prior from the data; James–Stein as empirical Bayes under a
    normal prior (Efron & Morris 1973).
11. **Robbins and Tweedie.**
    - Robbins' formula (x + 1)f(x + 1)/f(x) for Poisson data.
    - Tweedie's formula E[θ | x] = x + σ²(log f)′(x), derived: the score of the marginal, which is what a diffusion
      model learns (cross-reference *AI, Built* Part 21).
12. **Nonparametric empirical Bayes.** The Kiefer–Wolfowitz NPMLE (1956) by convex optimization (Koenker & Mizera
    2014); g-modelling vs f-modelling (Efron 2014).
13. **Selection and the winner's curse.** Tweedie corrects the top of a league table (Efron 2011), on the World's
    hospitals with noisy mortality rates.
14. **Shrinkage everywhere.** Ridge (25), random effects (17), priors (18); the Bayes–frequentist truce in decision
    theory (Berger).
15. **Outro.**

*Built:* `ShrinkageField` (3D shrinkage with live risk); the World's hospital league table, ranked raw and shrunk.
*Data:* Efron & Morris (1975).

#### Part 13 · Asymptopia: Large-Sample Theory and Optimality (~58)
*Question:* what is the best possible estimator, and why is "best" so hard to define?
*Story:* Hodges builds an estimator that beats the MLE at one point. Le Cam shows the price, a bump of risk just
beside that point, and proves that in large samples every regular model looks like a single Gaussian observation.
The MLE is optimal in a precise local minimax sense. Act II closes, and models of how variables relate come next
(→ Part 14).

0. **Hook: Hodges' estimator (1951).** The MLE snapped to 0 when |x̄| < n^{−1/4}: superefficient at 0. Its risk at θ =
   c/√n is a tall bump (computed).
1. **Stochastic order** (O_p, o_p) and the toolkit recalled.
2. **M- and Z-estimators** (Huber 1964). The MLE, least squares, the median, quantiles and Huber as one family.
3. **Consistency.** Uniform laws of large numbers; Glivenko–Cantelli classes and bracketing (visual); the argmax
   theorem.
4. **Asymptotic normality.** The sandwich A⁻¹BA⁻ᵀ for Z-estimators (Part 9's misspecification as a special case);
   the Bahadur representation of quantiles (1966) and the density at the quantile.
5. **Influence functions** (Hampel 1974). The derivative of a functional toward a point mass; the IF of the mean,
   median and Huber; variance = E IF²; the von Mises expansion and the functional delta method.
6. **U-statistics** (Hoeffding 1948).
   - The Hájek projection (an L² projection again) and asymptotic normality.
   - Examples: the sample variance, Wilcoxon, Kendall's τ, Gini's mean difference. Degenerate kernels and χ²
     mixtures.
7. **Hodges dissected.** Pointwise vs local (θₙ = h/√n) behaviour; the bump measured.
8. **Local asymptotic normality** (Le Cam 1960). log dP_{θ₀+h/√n}/dP_{θ₀} → hΔ − ½h²I. Every regular model looks like
   a Gaussian shift (likelihood ratios converging to parabolas).
9. **Contiguity.** Le Cam's first and third lemmas; local power against h/√n alternatives (computed).
10. **Optimality.** Hájek's convolution theorem (1970): every regular estimator's limit is N(0, I⁻¹) plus independent
    noise. The local asymptotic minimax theorem (Hájek 1972): Hodges' bump is unavoidable.
11. **Relative efficiency.** Pitman's ARE via local power; Bahadur efficiency in brief.
12. **Semiparametric models.**
    - A finite-dimensional target with an infinite-dimensional nuisance.
    - The efficient influence function as a projection onto the orthocomplement of the nuisance tangent space
      (drawn); the efficiency bound.
    - The partially linear model (Robinson 1988), the stepping stone to double machine learning (Part 29).
13. **Higher order.** Edgeworth expansions; the Bartlett correction; saddlepoint approximations (Daniels 1954),
    accurate at n = 5 (computed).
14. **When asymptotics fail.** Non-regular models (the uniform maximum: rate n, exponential limit); boundaries; the
    bootstrap's role (Part 21); proportional asymptotics p/n → γ (Part 25).
15. **Outro.** Act II recap; the Board so far.

*Built:* a risk-bump explorer (Hodges, hard thresholding, pre-test estimators under local alternatives).

### Act III · Models

#### Part 14 · Least Squares (~60)
*Question:* how do you fit a line through noise, and how sure are you of its slope?
*Story:* Gauss finds a lost asteroid, and a priority war follows. Least squares is a projection, Gauss–Markov makes
it optimal, and the classical standard errors turn out to lie whenever the noise is uneven or clustered. A
regression on observational data cannot tell cause from correlation, so we must design the data (→ Part 15).

0. **Hook: Ceres (1801).** Piazzi loses it behind the Sun; Gauss, 24, predicts where it will reappear and it is
   found on New Year's Eve. Legendre publishes least squares in 1805; Gauss claims it in 1809.
1. **The principle.** The normal equations. Why squares: normal errors make least squares the MLE (Gauss); absolute
   errors give median regression (Boscovich 1757, Laplace).
2. **Geometry.** y ∈ Rⁿ and the column space of X; the hat matrix H = X(XᵀX)⁻¹Xᵀ, symmetric and idempotent;
   orthogonal residuals (`NSpace`, n = 3, p = 2).
3. **Gauss–Markov** (Gauss 1821; Markov). OLS is BLUE (the difference of estimators is orthogonal); Aitken's GLS
   (1935).
4. **Normal theory.**
   - β̂ ~ N(β, σ²(XᵀX)⁻¹); s² ⟂ β̂; t-tests.
   - Nested F-tests as Pythagoras (RSS₀ − RSS₁), derived geometrically; R² and adjusted R².
5. **Frisch–Waugh–Lovell (1933).** A coefficient as the regression of residualized y on residualized x, making
   "controlling for" concrete (partial regression plots); the omitted-variable bias formula.
6. **Interpreting coefficients.** Units, interactions, polynomial and spline bases (Part 23), categorical codings;
   extrapolation.
7. **Bands.** Confidence vs prediction bands; Working–Hotelling.
8. **Collinearity.** Variance inflation factors from FWL; the elongated confidence ellipse with coefficients
   trading off; condition numbers; ridge, previewed.
9. **Diagnostics.** Leverage hᵢᵢ (Σhᵢᵢ = p), studentized residuals, Cook's distance (1977), DFBETAS; the
   `InfluenceProbe`, dragging one point around.
10. **Heteroskedasticity.**
    - The classical SE fails.
    - Eicker (1967), Huber (1967), White (1980); HC1–HC3 (MacKinnon & White 1985).
    - Board rows.
11. **Clustered errors.**
    - The Moulton factor (1990); cluster-robust SEs (Liang & Zeger 1986; Arellano 1987).
    - Too few clusters, and the wild cluster bootstrap (Cameron, Gelbach & Miller 2008).
    - Board rows.
12. **Weighted and generalized least squares.** Feasible GLS; iterative reweighting (the bridge to Part 16).
13. **Errors in variables.**
    - Attenuation λ = σ²ₓ/(σ²ₓ + σ²ᵤ), derived.
    - Hubble's 1929 velocity–distance fit as a historical case. Deming regression and total least squares via the
      SVD.
14. **Quantile regression** (Koenker & Bassett 1978). Check loss and linear programming; fanning quantile lines on
    the World's heteroskedastic data.
15. **Numerics.** Never invert XᵀX: Householder QR, Cholesky, SVD; the condition number squared; the Longley (1967)
    benchmark.
16. **Models as approximations** (Buja et al. 2019). Without linearity, OLS estimates the best linear predictor, and
    the sandwich is its correct SE.
17. **Outro.**

*Built:* statkit.ols (QR, influence, HC and cluster SEs, quantile regression), checked against statsmodels.

#### Part 15 · Experiments by Design (~58)
*Question:* how should data be collected so that the answer is unambiguous?
*Story:* Fisher arrives at Rothamsted to sift seventy years of wheat records that cannot answer anything. He
invents randomization, blocking and factorial design, and the analysis of variance becomes Pythagoras. Then on to
response surfaces, optimal designs and the A/B tests that run the web. Outcomes are not always normal (→ Part 16).

0. **Hook: Rothamsted (1919).** The Broadbalk wheat records since 1843; Fisher's *Studies in Crop Variation* (1921).
1. **Three principles.** Replication, randomization, local control; Peirce & Jastrow's (1884) randomized experiment;
   Fisher (1926, 1935).
2. **Randomization as the basis of inference.** The randomization distribution; why randomizing balances hidden
   covariates in expectation (World, with hidden fertility).
3. **One-way ANOVA.** SST = SSB + SSW as Pythagoras in Rⁿ; the F-test derived; ANOVA = regression on indicators.
4. **Contrasts.** Orthogonal contrasts; Tukey's HSD (studentized range, 1953), Scheffé, Dunnett.
5. **Blocking.** Randomized complete blocks; the variance reduction measured; paired designs; Darwin's *Zea mays*
   (15 pairs) with Fisher's permutation test (1935).
6. **Latin squares** (Euler's officers; Fisher), Graeco-Latin and Youden squares; crossover designs.
7. **Factorial designs.**
   - Main effects and interactions as orthogonal contrasts in 2^k; Yates' algorithm (1937); interaction plots.
   - Why one-factor-at-a-time misses a ridge (computed).
8. **Fractional factorials** (Finney 1945; Box & Hunter 1961). 2^{k−p}, defining relations, aliasing and resolution
   (half a cube's corners lit in 3D); Plackett–Burman (1946).
9. **Response surfaces** (Box & Wilson 1951). Steepest ascent, central composite designs, canonical analysis of the
   quadratic (3D surface tour).
   - *Built:* optimizing a hidden recipe in the World's bakery.
10. **Split plots and nesting.** Whole plots vs subplots and two error strata; the classic analysis error (Board);
    variance components (Part 17).
11. **Optimal design.**
    - Information matrices; D-, A- and G-optimality.
    - Kiefer–Wolfowitz equivalence (1960): the variance function touches p at the support points. Quadratic
      regression on [−1, 1] puts 1/3 at −1, 0, 1 (drawn).
12. **Power and sample size.** Noncentrality; Cohen's d (1988); the minimum detectable effect.
13. **Covariate adjustment.** ANCOVA; Freedman's (2008) critique and Lin's (2013) interacted answer (Part 28).
14. **Online experiments** (Kohavi, Tang & Xu 2020).
    - CUPED (Deng et al. 2013) as control variates and regression adjustment, with variance reduction 1 − ρ².
    - Sample-ratio mismatch; interference and cluster randomization; novelty effects.
15. **Balance by design.** Rerandomization (Morgan & Rubin 2012); covariate-adaptive allocation; Student's (1938)
    defence of balanced designs against Fisher.
16. **Outro.** Sequential designs come in Part 35.

*Built:* a field-trial simulator (a farm with a fertility gradient, with designs compared by efficiency); statkit.design.
*Data:* Darwin (1876) via Fisher (1935).

#### Part 16 · Beyond the Normal: Generalized Linear Models (~58)
*Question:* how do you regress a yes/no, a count or a rate?
*Story:* the night before Challenger, a chart left out the flights with no damage. Logistic regression on all 23
flights sees the danger at 31°F. One algorithm, IRLS, fits a whole family of models, and the same tables hide
Simpson's paradox. Data come in groups within groups (→ Part 17).

0. **Hook: 27 January 1986.** The teleconference chart; all 23 flights; the launch temperature of 31°F (Dalal,
   Fowlkes & Hoadley 1989; Tufte 1997).
1. **Why not least squares on 0/1.** Probabilities outside [0, 1] and built-in heteroskedasticity; the linear
   probability model's place.
2. **The exponential dispersion family.** Variance functions V(μ); canonical links; Nelder & Wedderburn (1972).
3. **Logistic regression.**
   - Log-odds and odds ratios; latent-variable views (probit: Bliss 1934; logit: Berkson 1944).
   - The Challenger fit with a profile-likelihood interval at 31°F, and the extrapolation caveat.
4. **IRLS derived.** Fisher scoring = weighted least squares on a working response, step by step; a projection in a
   weighted metric.
5. **Deviance.** Twice the log-likelihood ratio to the saturated model; analysis of deviance; Pearson, deviance and
   randomized quantile residuals (Dunn & Smyth 1996).
6. **Separation** (Albert & Anderson 1984). The likelihood rising forever (drawn); Firth (1993) as a Jeffreys
   penalty.
7. **Counts and rates.** Poisson regression with offsets; Bortkiewicz's corps revisited.
8. **Overdispersion.** Quasi-likelihood (Wedderburn 1974) from the mean–variance relation alone; the negative
   binomial (Part 3's gamma–Poisson); zero inflation (Lambert 1992); Board rows.
9. **Tables.**
   - Simpson's paradox in the Berkeley admissions (Bickel, Hammel & O'Connell 1975), with mosaic plots flipping.
   - Log-linear models for three-way tables; Cochran–Mantel–Haenszel (1959).
10. **Case–control sampling.** Why logistic slopes survive outcome-dependent sampling (Prentice & Pyke 1979);
    Cornfield (1951); Doll & Hill (1950).
11. **Multinomial and ordinal.** Baseline-category logits; proportional odds (McCullagh 1980) with latent cutpoints.
12. **GEE** (Liang & Zeger 1986). Marginal models, working correlations, sandwich SEs; population-averaged vs
    subject-specific effects (Part 17).
13. **Scoring predictions.** ROC/AUC (= Mann–Whitney, Part 22); calibration curves; the Brier decomposition (Murphy
    1973); Hosmer–Lemeshow; proper scoring rules (Gneiting & Raftery 2007).
14. **High-dimensional logistic regression** (Sur & Candès 2019). With p/n = 0.1 the MLE is inflated and the LRT is
    not χ² (computed).
15. **The rest of the family.** Gamma GLMs for costs; Tweedie compound Poisson–gamma for insurance claims.
16. **Outro.**

*Built:* statkit.glm (IRLS, deviance, quasi-likelihood, Firth, GEE), checked against statsmodels; a Challenger
dashboard.
*Data:* the Challenger O-ring table (Presidential Commission 1986); Berkeley totals (Bickel et al. 1975).

#### Part 17 · Borrowing Strength: Hierarchical and Mixed Models (~58)
*Question:* how do you estimate many related things at once?
*Story:* eight schools ran an SAT coaching programme. Taken separately the estimates are too noisy, and pooled they
are too blunt. Partial pooling, built from random effects, BLUP and REML, is Part 12's shrinkage in disguise, and
it runs everything from cattle breeding to census estimates to meta-analysis. The random effect has a prior, so we
have been half Bayesian all along (→ Part 18).

0. **Hook: the eight schools** (Rubin 1981). Effects 28, 8, −3, 7, −1, 1, 18, 12 with SEs 15, 10, 16, 11, 9, 11, 10,
   18.
1. **Three estimates.** No pooling, complete pooling, partial pooling (the shrinkage plot from Part 12).
2. **Random effects.** Variance components (Fisher 1918); the intraclass correlation; the design effect.
3. **The linear mixed model.**
   - y = Xβ + Zu + ε with V = ZGZᵀ + R; GLS for β.
   - BLUP from Henderson's mixed-model equations (derived; Henderson's dairy cattle); "That BLUP is a good thing"
     (Robinson 1991).
4. **ML vs REML** (Patterson & Thompson 1971). The likelihood of error contrasts; the n − 1 generalized.
5. **The eight schools by REML.** τ̂ = 0 on the boundary and a flat profile for τ; why Bayesians use half-normal or
   half-Cauchy priors (Gelman 2006). Full Bayes is in Part 19.
6. **Inference.** Satterthwaite and Kenward–Roger degrees of freedom; testing a variance on the boundary with
   ½χ²₀ + ½χ²₁ (Self & Liang 1987), computed.
7. **Longitudinal data.** Random intercepts and slopes (Laird & Ware 1982); growth curves of the World's children;
   AR(1) and compound symmetry; spaghetti plots.
8. **Crossed and nested effects.** Students in schools, items × raters; the Minnesota radon example (Price, Nero &
   Gelman 1996; Gelman & Hill); group-level predictors.
9. **Fixed vs random effects.** The within/between decomposition; Hausman (1978); Mundlak's device (1978); a
   dictionary between the economics and statistics vocabularies.
10. **GLMMs.**
    - The integral over u; Laplace and adaptive Gauss–Hermite quadrature (drawn); PQL bias (Breslow & Clayton 1993).
    - Conditional vs marginal odds ratios, and the attenuation factor (Zeger, Liang & Albert 1988).
11. **Smoothing as a mixed model** (Ruppert, Wand & Carroll 2003). Penalized splines are random effects; GAMs (Hastie
    & Tibshirani 1990; Wood 2017) with REML smoothness selection (Wood 2011).
12. **Small-area estimation.** Fay–Herriot (1979) and the Census Bureau's county estimates; EBLUP; MSE (Prasad & Rao
    1990).
13. **Meta-analysis.**
    - Fixed vs random effects; DerSimonian–Laird (1986); τ² and I² (Higgins & Thompson 2002).
    - Hartung–Knapp–Sidik–Jonkman (Board rows). Funnel plots (Part 26).
14. **Item response theory.** The Rasch model (1960) as a GLMM: ability and difficulty. It returns for AI benchmarks
    in Part 36.
15. **Outro.**

*Built:* statkit.mixed (profiled REML, BLUPs, Laplace GLMM), checked against statsmodels; the World's schools.
*Data:* the eight schools (Rubin 1981).

### Act IV · Bayes

#### Part 18 · Inverse Probability: Bayesian Inference (~58)
*Question:* what should you believe after seeing the data?
*Story:* a ball rolled on a billiard table becomes the first posterior. Laplace computes the odds that boys
outnumber girls. Priors are argued over, Bernstein–von Mises shows the schools agree in large samples, and Lindley's
paradox shows where they never will. Posteriors rarely have closed forms (→ Part 19).

0. **Hook: Bayes's billiard table (1763).** A hidden ball, later balls landing left or right; the Beta posterior.
   Laplace's rule of succession; Laplace's Paris births 1745–1770 and his posterior probability that boys are more
   likely (figures *(verify)*).
1. **The machinery.** Prior × likelihood ∝ posterior (`BayesUpdate`); the evidence; sequential updating equals batch
   updating.
2. **Conjugacy.**
   - Beta–binomial, gamma–Poisson, normal–normal (precision-weighted averages, derived), normal–inverse-gamma,
     Dirichlet–multinomial.
   - Diaconis & Ylvisaker (1979): linear posterior means characterize conjugacy in exponential families.
3. **Summaries and predictions.** Mean, median and MAP from loss (Part 12); equal-tailed vs HPD intervals; posterior
   predictive distributions (beta-binomial).
4. **Priors.**
   - Elicited and conjugate; weakly informative.
   - Jeffreys (1946) from invariance (derived via Fisher information); reference priors (Bernardo 1979).
   - Improper priors and improper posteriors (a computed failure); sensitivity analysis.
5. **The normal model in full.** Unknown μ and σ²: the marginal posterior of μ is a Student t, so Bayes recovers the
   t-interval without a pivot.
6. **Bernstein–von Mises.**
   - The posterior → N(θ̂, I⁻¹/n): the posterior and the sampling distribution of the MLE overlap (computed).
   - Where it fails: nonparametric (Freedman 1963; Diaconis & Freedman 1986), boundary.
7. **Doob's consistency (1949)** via martingale convergence (Part 6).
8. **Bayes factors** (Jeffreys 1939; Kass & Raftery 1995). The evidence ratio; sensitivity to the prior's width.
9. **Lindley's paradox (1957).** p ≈ 0.01 and a Bayes factor favouring H₀ as n grows (computed), with a historical
   example from the random-event-generator literature (Jefferys 1990, figures *(verify)*).
10. **Occam's razor, built in.** The evidence spreads its mass over datasets (MacKay 1992; cross-reference *AI,
    Built* Part 7).
11. **Hierarchical Bayes.** Hyperpriors; exchangeability and de Finetti (Part 4) as the justification; the eight
    schools' posterior over τ on a grid.
12. **Decisions.** Expected utility; the value of information; a clinical decision worked through.
13. **Frequentist properties.**
    - Credible intervals at fixed θ: calibrated on average under the true prior, broken at the extremes under a
      wrong one (Board).
    - Probability-matching priors (Welch & Peers 1963).
14. **The argument, honestly.**
    - Fisher's hostility. Jeffreys, de Finetti, Savage (1954), Lindley; the MCMC revival (McGrayne 2011).
    - Cox's theorem and coherence as justifications.
    - Where the schools converge (BvM) and where they do not (testing, high dimensions).
15. **Bayesian nonparametrics.** The Dirichlet process (Ferguson 1973): stick-breaking and the Chinese restaurant
    (animated); DP mixtures; GP priors (Part 32).
16. **Outro.**

*Built:* the billiard table (physical simulation and its posterior); statkit.bayes (conjugate and grid posteriors).
*Data:* Laplace's Paris births.

#### Part 19 · Sampling the Posterior: Monte Carlo and MCMC (~60)
*Question:* how do you compute an integral you cannot do, in a hundred dimensions?
*Story:* at Los Alamos in 1953 a random walk computes the physics of hard disks. Metropolis, Gibbs and Hamilton's
mechanics become the engines of Bayesian statistics. We build our own probabilistic programming language, watch
NUTS fail in Neal's funnel, then fix it by reparametrizing. Any model can now be fitted, so which one should we
believe (→ Part 20)?

0. **Hook: Metropolis, the Rosenbluths and the Tellers (1953).** MANIAC; hard disks; Boltzmann weights from a random
   walk.
1. **Monte Carlo integration.** Error σ/√n in any dimension; Buffon's needle (1777) as the first Monte Carlo; grids
   vs Monte Carlo in high dimension.
2. **Variance reduction.**
   - Antithetic variates, control variates (CUPED again), stratification.
   - Importance sampling: the optimal proposal derived; effective sample size; heavy-tailed weights failing; PSIS
     (Vehtari et al.).
3. **Rejection sampling** in high dimension; adaptive rejection (Gilks & Wild 1992).
4. **MCMC.** A chain whose stationary law is the posterior; detailed balance (Part 6).
5. **Metropolis–Hastings.** The acceptance ratio from detailed balance; random-walk proposals; the 0.234 rule
   (Roberts, Gelman & Gilks 1997); a walker on a banana posterior.
6. **Gibbs** (Geman & Geman 1984; Gelfand & Smith 1990). Full conditionals; data augmentation (Tanner & Wong 1987);
   Albert–Chib (1993) probit; zigzags under correlation.
7. **Diagnostics.** Traces, autocorrelation, ESS (Part 6's asymptotic variance), R̂ (Gelman & Rubin 1992;
   rank-normalized, Vehtari et al. 2021); good and bad chains computed.
8. **Hamiltonian Monte Carlo** (Duane et al. 1987; Neal 2011).
   - Momentum and energy; the leapfrog integrator is symplectic, so volume is preserved and the acceptance step is
     simple.
   - A puck sliding over the negative log-posterior in 3D.
9. **NUTS** (Hoffman & Gelman 2014). The U-turn criterion; step-size and mass-matrix adaptation; divergences as a
   symptom of geometry.
10. **Neal's funnel and the eight schools.** Centred vs non-centred parametrizations (Papaspiliopoulos, Roberts &
    Sköld 2007); divergences counted before and after.
11. **Built: a tiny probabilistic programming language.**
    - Models written in Python; log densities differentiated by *AI, Built*'s autodiff (`explainer/ai/autodiff.py`).
    - NUTS, R̂, ESS, and checks against closed-form posteriors: "a Stan in 400 lines".
12. **Sequential Monte Carlo.** Particle filters (Gordon, Salmond & Smith 1993); resampling and degeneracy;
    tempering for static posteriors (Del Moral, Doucet & Jasra 2006); the evidence for free.
13. **Approximations.**
    - Laplace (Tierney & Kadane 1986); INLA (Rue, Martino & Chopin 2009).
    - Variational inference: the ELBO, mean-field CAVI derived; reverse KL is mode-seeking and underestimates
      variance (against NUTS); ADVI; Pareto-k̂ diagnostics (Yao et al. 2018).
14. **Without a likelihood.**
    - ABC (Tavaré et al. 1997; Pritchard et al. 1999; Beaumont et al. 2002) and the sufficiency of summaries
      (Part 8).
    - Neural posterior estimation (Papamakarios & Murray 2016; Cranmer, Brehmer & Louppe 2020).
    - Simulation-based calibration (Talts et al. 2018), which checks any sampler.
15. **Exact sampling.** Coupling from the past (Propp & Wilson 1996) on an Ising model; unbiased MCMC by couplings
    (Jacob, O'Leary & Atchadé 2020).
16. **Outro.**

*Built:* statkit.ppl with NUTS (the part's main build); SBC rank histograms as a diagnostic board.

#### Part 20 · Which Model? Checking, Comparing, Averaging (~55)
*Question:* how do you choose a model without fooling yourself?
*Story:* fifty columns of pure noise produce a "significant" regression once the best are kept. Training error is
optimistic, and we derive by exactly how much. AIC, BIC, cross-validation, LOO and WAIC are each derived; singular
models break BIC; and averaging can beat choosing. All of this depends on models, so can computation stand in for
assumptions (→ Part 21)?

0. **Hook: Freedman's paradox (1983).** 100 observations and 50 noise predictors. Screen at p < 0.25, refit, and get a
   significant F with several "significant" coefficients (computed).
1. **All models are wrong** (Box 1976). Prediction vs explanation; polynomial overfitting, with in-sample error
   falling and out-of-sample error rising.
2. **Optimism.** Training error's optimism 2σ²·df/n (Efron 1986); degrees of freedom as Σcov(ŷᵢ, yᵢ)/σ² (Efron 2004,
   via Stein's lemma).
3. **Mallows' Cp (1973) and AIC (Akaike 1973).** AIC as an asymptotically unbiased estimate of expected KL, derived;
   TIC under misspecification; AICc (Hurvich & Tsai 1989).
4. **BIC (Schwarz 1978).** The Laplace approximation of the evidence, derived; consistency vs efficiency, and Yang's
   (2005) impossibility of having both.
5. **Cross-validation.** LOO (Stone 1974) and k-fold; LOO for linear smoothers via hᵢᵢ, and GCV (Craven & Wahba
   1979); CV's variance; what CV estimates (Bates, Hastie & Tibshirani 2024).
6. **Model checking.** Posterior predictive checks (Rubin 1984; Gelman, Meng & Stern 1996); prior predictive checks;
   the double use of data.
7. **Bayesian LOO.** PSIS-LOO (Vehtari, Gelman & Gabry 2017) with Pareto-k̂; WAIC (Watanabe 2010); DIC's flaws.
8. **Singular models.** For mixtures and neural networks BIC fails; Watanabe's real log canonical threshold λ replaces
   d/2 (computed on a two-component mixture).
9. **MDL** (Rissanen 1978). Two-part codes and normalized maximum likelihood; model choice as compression
   (cross-reference *AI, Built* Part 1).
10. **Averaging instead of choosing.** Bayesian model averaging (Hoeting et al. 1999) in the M-closed world; stacking
    (Wolpert 1992; Breiman 1996; Yao et al. 2018), compared on the World.
11. **Inference after selection.** A naive CI after AIC selection (Board: broken) vs data splitting (kept, wider);
    Part 26 goes further.
12. **Subset selection.** Stepwise regression's sins (Harrell); best subset by mixed-integer optimization (Bertsimas,
    King & Mazumder 2016) vs the lasso (Hastie, Tibshirani & Tibshirani 2020).
13. **Bayesian workflow** (Gelman et al. 2020). Build, check and expand; simulation-based calibration; forking paths
    inside the workflow.
14. **Calibrated forecasts.** PIT histograms; log score and CRPS; Dawid's prequential principle (1984).
15. **Outro.**

*Built:* a model-selection bench (one dataset, every criterion, the chosen models compared against the World's
truth); statkit.select.

### Act V · Fewer Assumptions

#### Part 21 · Pulling Yourself Up: The Bootstrap and Resampling (~55)
*Question:* can the sample stand in for the population it came from?
*Story:* Efron asks for the standard error of a correlation from 15 law schools and answers by resampling. Edgeworth
expansions explain which bootstrap intervals are accurate. The German tank breaks the bootstrap, and m-out-of-n
repairs it. But what if the model is wrong in the tails (→ Part 22)?

0. **Hook: Efron (1979).** The law-school sample, 15 pairs of LSAT and GPA with r = 0.776. What is its standard
   error, with no formula?
1. **The jackknife** (Quenouille 1949; Tukey 1958). Leave-one-out bias correction and variance; pseudo-values; its
   failure for the median.
2. **The bootstrap principle.** The real world F → X → θ̂ mirrored by F̂ → X* → θ̂* (`BootstrapResampler`); the
   law-school SE; Monte Carlo error vs bootstrap error.
3. **Why it works.** Plug-in consistency (Bickel & Freedman 1981); the ideal bootstrap as an enumeration of
   C(2n − 1, n) distinct resamples.
4. **Intervals.** Normal, basic, percentile (Efron 1981) and studentized; coverage on skewed World incomes (Board).
5. **BCa (Efron 1987).** The bias correction z₀ and the acceleration a derived (a from the jackknife skewness of the
   influence function); transformation-respecting.
6. **Second-order accuracy** (Hall 1988, 1992). Edgeworth expansions show that bootstrap-t and BCa are O(1/n) while
   the percentile interval is O(1/√n).
7. **When it fails.**
   - The uniform maximum: P(θ̂* = θ̂) → 1 − 1/e ≈ 0.632.
   - Repairs: the m-out-of-n bootstrap (Bickel, Götze & van Zwet 1997) and subsampling (Politis & Romano 1994).
   - Also: infinite variance (Athreya 1987); boundaries.
8. **Regression.** Resampling pairs vs residuals; the wild bootstrap (Wu 1986; Mammen 1993); the wild cluster
   bootstrap (Board, from Part 14).
9. **Dependent data.** The block bootstrap (Künsch 1989) and the stationary bootstrap (Politis & Romano 1994); block
   length (Part 31).
10. **Testing.** Bootstrap tests vs permutation tests (plug-in vs exchangeability); the double bootstrap (Beran
    1987).
11. **Prediction error.** The .632 (Efron 1983) and .632+ (Efron & Tibshirani 1997) estimators; out-of-bag error.
12. **Bagging** (Breiman 1996). Averaging an unstable procedure over bootstrap samples (a tree, computed).
13. **The Bayesian bootstrap** (Rubin 1981). Dirichlet weights; the DP limit; the weighted likelihood bootstrap
    (Newton & Raftery 1994).
14. **Scale and high dimension.** The bag of little bootstraps (Kleiner et al. 2014); the Gaussian multiplier
    bootstrap for maxima of many means (Chernozhukov, Chetverikov & Kato 2013).
15. **Outro.**

*Built:* statkit.bootstrap, checked against `scipy.stats.bootstrap`.
*Data:* the law-school sample (Efron & Tibshirani 1993).

#### Part 22 · When the Model Is Wrong: Ranks and Robustness (~58)
*Question:* what survives when the assumptions break?
*Story:* Tukey shows that 1% contamination topples the standard deviation. Ranks give exact tests that never lose
more than 13.6% efficiency, Huber solves the minimax problem, and high breakdown estimators refuse to be dragged. A
2016 breakthrough makes robustness possible in high dimensions. Next, robust location gives way to whole curves
(→ Part 23).

0. **Hook: Tukey (1960) and Newcomb (1882).** The contaminated normal flips which scale estimator is better. Newcomb's
   66 speed-of-light measurements with two wild values (Stigler 1977).
1. **Newcomb's data.** Mean, median and trimmed means; Stigler's verdict on real data.
2. **Ranks.** Under H₀ ranks are a uniform random permutation, giving exact distribution-free nulls; the sign test.
3. **Wilcoxon's signed rank (1945).** The exact null from the generating function ∏(1 + t^k)/2, derived; the normal
   limit.
4. **Mann–Whitney (1947).** U counts pairs; U/(mn) estimates P(X < Y), the ROC area; exact nulls; ties.
5. **Efficiency.**
   - Pitman ARE of Wilcoxon vs t: 3/π ≈ 0.955 at the normal, derived.
   - Hodges & Lehmann (1956): at least 0.864 for every distribution, by optimizing over densities; unbounded above.
   - Normal scores (Chernoff & Savage 1958) never do worse than t.
6. **Hodges–Lehmann (1963).** The median of Walsh averages and its CI by inverting Wilcoxon.
7. **More rank methods.** Kruskal–Wallis (1952), Friedman (1937), Spearman's ρ and Kendall's τ as U-statistics,
   Jonckheere, rank regression (Jaeckel 1972).
8. **Robustness formalized.**
   - Gross-error neighbourhoods; the influence function and sensitivity curve (`InfluenceProbe`); gross-error
     sensitivity.
   - Breakdown points (Hampel 1971; Donoho & Huber 1983): 0 for the mean, ½ for the median.
9. **Huber (1964).**
   - The minimax M-estimator over ε-contaminated normals: the least favourable law is normal in the middle and
     exponential in the tails (derived).
   - ψ-functions: Huber, Tukey's biweight, Hampel's three-part; IRLS.
10. **Scale.** MAD (×1.4826); Qn and Sn (Rousseeuw & Croux 1993); joint location–scale.
11. **Robust regression.**
    - Leverage defeats M-estimators. LMS (Rousseeuw 1984), LTS, S- (Rousseeuw & Yohai 1984) and MM-estimators (Yohai
      1987: 50% breakdown with 95% efficiency).
    - A line that refuses to be dragged.
12. **Robust multivariate.** MCD (Rousseeuw 1985; FAST-MCD 1999); robust Mahalanobis distances; masking and
    swamping (visual).
13. **Heavy-tailed means.**
    - Median-of-means (Nemirovsky & Yudin 1983; Jerrum, Valiant & Vazirani 1986; Alon, Matias & Szegedy 1996):
      sub-Gaussian deviations from a variance alone, derived.
    - Catoni (2012); Lugosi & Mendelson (2019).
14. **High-dimensional robust statistics** (Diakonikolas et al. 2016; Lai, Rao & Vempala 2016). Naive estimators pay
    √d; filtering reaches error O(ε√log(1/ε)); data poisoning in ML.
15. **Outro.**

*Board rows:* t vs Wilcoxon under contamination (size and power); mean vs Hodges–Lehmann intervals.
*Built:* statkit.ranks and statkit.robust (exact Wilcoxon, Huber, biweight, FAST-LTS, MCD, median-of-means), checked
against SciPy and statsmodels; the `InfluenceProbe`.
*Data:* Newcomb (1882) via Stigler (1977).

#### Part 23 · Smoothing: Densities and Curves (~58)
*Question:* how do you estimate a whole curve, and how much data does that take?
*Story:* does Old Faithful have two humps or three? Bias and variance trade off at the rate n^{−4/5}, which is proved
optimal. Splines, wavelets and shape constraints each buy something, and in many dimensions the curse arrives. With
many variables we need structure (→ Part 24).

0. **Hook: Old Faithful.** Waiting times between eruptions; histograms with different bins tell different stories;
   Silverman's (1981) test for the number of modes.
1. **The histogram as an estimator.** Bias ∝ h, variance ∝ 1/(nh); MISE-optimal h ∝ n^{−1/3} (Scott, Freedman–
   Diaconis derived, completing Part 1); averaged shifted histograms (Scott 1985).
2. **Kernel density estimation** (Rosenblatt 1956; Parzen 1962).
   - A sum of bumps (`KernelSum`, with the bandwidth slider).
   - Bias h²f″μ₂/2, variance R(K)f/(nh); h* ∝ n^{−1/5} and the rate n^{−4/5}, on the ladder.
3. **The optimal kernel.** Epanechnikov (1969) by the calculus of variations; the Gaussian's efficiency (≈ 95%); the
   bandwidth matters more than the kernel.
4. **Choosing h.** Silverman's rule of thumb; least-squares cross-validation (Rudemo 1982; Bowman 1984); Sheather–Jones
   plug-in (1991); on Old Faithful and the World.
5. **The curse of dimensionality.** The rate n^{−4/(4+d)}, and the sample size needed for fixed accuracy as d grows
   (Silverman's table, recomputed).
6. **Regression smoothers.** Nadaraya–Watson (1964); boundary and design bias; local linear (Fan 1992; Fan & Gijbels
   1996); LOESS (Cleveland 1979), with a sliding window fitting tiny lines.
7. **Splines.**
   - Knots and B-splines (de Boor); regression splines.
   - The smoothing-spline theorem (Schoenberg 1964; Reinsch 1967): the minimizer of Σ(y − f)² + λ∫f″² is a natural
     cubic spline with knots at the data (derived by integration by parts).
8. **The smoother matrix.** ŷ = Sy; effective degrees of freedom tr S; the Demmler–Reinsch eigenbasis, with wiggly
   components shrunk (ridge and James–Stein again).
9. **Choosing λ.** GCV, REML (Part 17), Cp.
10. **RKHS.** The representer theorem (Kimeldorf & Wahba 1970); smoothing splines and kernel ridge as one; the GP as
    the Bayesian twin (Part 32).
11. **Wavelets and adaptivity.**
    - Haar to Daubechies; sparsity in the wavelet domain.
    - VisuShrink's σ√(2 log n) from Gaussian maxima, derived; SureShrink (Donoho & Johnstone 1994, 1995).
    - The Doppler, Bumps and Blocks test functions.
12. **Minimax rates.**
    - n^{−2s/(2s+d)} for s-smooth functions (Stone 1982).
    - Lower bounds by Le Cam's two points, Fano and Assouad (a hypercube of bumps, drawn): no estimator does better.
13. **Inference for curves.** Pointwise intervals and the bias problem; undersmoothing; robust bias-corrected
    intervals (Calonico, Cattaneo & Farrell 2018) (Board); simultaneous bands with a Gumbel limit (Bickel &
    Rosenblatt 1973).
14. **Shape constraints.** Isotonic regression and pool-adjacent-violators (Brunk 1955); the Grenander estimator
    (1956) with its n^{−1/3} rate and Chernoff's distribution (1964); log-concave MLEs (Cule, Samworth & Stewart
    2010).
15. **Escaping the curse.** Additive models and backfitting (Buja, Hastie & Tibshirani 1989), single-index models,
    projection pursuit (Friedman & Stuetzle 1981); trees and forests (Part 27).
16. **Outro.**

*Built:* statkit.smooth (KDE with three bandwidth selectors, local linear, Reinsch smoothing spline, PAVA).
*Data:* Old Faithful (NPS records if public domain; otherwise a documented dataset, license checked).

### Act VI · Many Variables, Many Questions

#### Part 24 · Many Variables: Multivariate Analysis and Random Matrices (~58)
*Question:* what structure hides in a cloud of many correlated variables, and when is it an illusion?
*Story:* PCA on pure noise finds "large components". The classical multivariate toolkit of Wishart, Hotelling,
Fisher and Spearman meets random matrix theory, where an eigenvalue bulk forms and a real signal pops out only
beyond a sharp threshold. When variables outnumber observations, we need sparsity (→ Part 25).

0. **Hook: noise with structure.** n = 1,000, p = 500, identity covariance: the sample eigenvalues spread from
   (1 − √½)² ≈ 0.09 to (1 + √½)² ≈ 2.91.
1. **The data matrix.** The mean vector and covariance; Mahalanobis distance (1936) as the ellipse's metric.
2. **Wishart (1928).** The law of S; the Bartlett decomposition (1933); *Built:* a Wishart sampler.
3. **Hotelling's T² (1931).**
   - The multivariate t as the maximum over directions of a t² (union–intersection, Roy 1953; via Cauchy–Schwarz,
     with a rotating projection).
   - Two-sample T²; MANOVA's four statistics as functions of eigenvalues.
4. **PCA in depth** (Pearson 1901; Hotelling 1933). Maximum variance and best low rank (Eckart–Young;
   cross-reference *AI, Built* Part 3); scores, loadings, biplots (Gabriel 1971); scaling choices; scree plots.
5. **Factor analysis** (Spearman 1904; Thurstone). Σ = ΛΛᵀ + Ψ; rotation indeterminacy and varimax (Kaiser 1958);
   ML factor analysis; Heywood cases; FA vs PCA.
6. **Canonical correlation** (Hotelling 1936). A generalized eigenproblem; principal angles between subspaces.
7. **Discriminant analysis** (Fisher 1936; Rao 1948). The between/within Rayleigh quotient; LDA vs QDA. The history
   is acknowledged, including where Fisher published.
8. **Multidimensional scaling** (Torgerson 1952). Double centring gives PCA. *Built:* the map of the World's towns
   recovered from road distances alone.
9. **Marchenko–Pastur (1967).** The law derived via the Stieltjes transform (sketched); histograms converging for γ =
   0.1, 0.5, 1, 2; Wigner's semicircle (1955) as its cousin.
10. **The spiked model and BBP** (Baik, Ben Arous & Péché 2005).
    - A spike ℓ is visible only if ℓ > 1 + √γ; the outlier sits at ℓ(1 + γ/(ℓ − 1)).
    - The eigenvector overlap formula (Paul 2007). The spike popping out of the bulk as ℓ crosses the threshold.
11. **The largest eigenvalue.** Tracy–Widom (1994) fluctuations at scale n^{−2/3}; Johnstone (2001) on testing
    structure in PCA.
12. **High-dimensional covariance.**
    - Ledoit–Wolf (2004) linear shrinkage, derived, and nonlinear shrinkage.
    - Optimal hard thresholding of singular values (Gavish & Donoho 2014: 4/√3 for square matrices).
13. **Sparse precision matrices.**
    - Zeros of Σ⁻¹ ⇔ conditional independence (Schur complements, Part 4).
    - The graphical lasso (Friedman, Hastie & Tibshirani 2008); neighbourhood selection (Meinshausen & Bühlmann
      2006). The World's hidden dependency network recovered.
14. **Sparse PCA and a computational barrier.** Zou, Hastie & Tibshirani (2006); d'Aspremont et al. (2007); the
    statistical–computational gap via planted clique (Berthet & Rigollet 2013).
15. **High-dimensional testing.** T² loses its power as p → n (Bai & Saranadasa 1996); the Chen–Qin (2010) test
    (Board).
16. **Outro.**

*Built:* the random-matrix lab (`SpectrumBulk`); the map from distances; statkit.multi.

#### Part 25 · More Variables Than Data: Sparsity (~60)
*Question:* how can you solve for 1,000 unknowns from 100 equations?
*Story:* Candès reconstructs a phantom image exactly from far too few measurements, and it seems impossible until ℓ1
geometry explains it. The lasso's theory has sharp phase transitions and oracle inequalities; naive inference after
the lasso fails and debiasing fixes it; and in proportional asymptotics interpolation can generalize. Once we select
variables, we are asking thousands of questions (→ Part 26).

0. **Hook: Candès's phantom (2004).** A Shepp–Logan phantom recovered from a few radial Fourier lines by
   total-variation minimization (Candès, Romberg & Tao 2006). We reproduce it.
1. **p > n.** Infinitely many least-squares solutions; structure is needed.
2. **Ridge** (Hoerl & Kennard 1970; Tikhonov 1943). SVD shrinkage d²/(d² + λ); ridge as a normal prior and as data
   augmentation; the ridge trace; degrees of freedom.
3. **From ℓ0 to ℓ1.** Best subset is combinatorial; convex relaxation; ℓq balls morphing from q = 2 to q = ½ in 3D.
4. **The lasso** (Tibshirani 1996; Chen, Donoho & Saunders 1998).
   - The diamond and the octahedron meeting elliptical contours (`L1Geometry`).
   - Soft-thresholding in the orthogonal case via subgradients; the KKT conditions.
5. **Computing it.** Coordinate descent (Friedman et al. 2007, 2010), derived; LARS (Efron et al. 2004) and the
   piecewise-linear path (animated); warm starts.
6. **Sparsity and Bayes.** The Laplace prior's mode is sparse but its posterior mean is not (Park & Casella 2008);
   the horseshoe (Carvalho, Polson & Scott 2010); shrinkage profiles compared.
7. **Compressed sensing.** RIP (Candès & Tao 2005) and the null-space property; random matrices satisfy RIP at n ≳
   s log(p/s); *Built:* the phantom.
8. **Phase transitions.** The Donoho–Tanner (2009) diagram, computed over (δ = n/p, ρ = s/n); AMP's state evolution
   predicting the curve (Donoho, Maleki & Montanari 2009; Bayati & Montanari 2011).
9. **Lasso theory.**
   - The restricted eigenvalue condition (Bickel, Ritov & Tsybakov 2009).
   - The oracle inequality ‖β̂ − β‖² ≲ σ²s log p/n with λ ≥ 2‖Xᵀε‖∞/n (union bound, Part 5), derived.
   - Support recovery and irrepresentability (Zhao & Yu 2006; Wainwright 2009).
10. **The penalty zoo.** Elastic net (Zou & Hastie 2005), group lasso (Yuan & Lin 2006), fused lasso (Tibshirani et
    al. 2005), adaptive lasso (Zou 2006), SCAD (Fan & Li 2001), MCP (Zhang 2010); their thresholding functions
    animated.
11. **Choosing λ.** CV and the one-standard-error rule; stability selection (Meinshausen & Bühlmann 2010).
12. **Inference after the lasso, I.** Naive post-lasso intervals (Board: broken); the debiased lasso (Zhang & Zhang
    2014; van de Geer et al. 2014; Javanmard & Montanari 2014), derived; Board: kept.
13. **Inference after the lasso, II.** Double selection (Belloni, Chernozhukov & Hansen 2014); exact post-selection
    inference via the polyhedral lemma and truncated Gaussians (Lee et al. 2016) (Board).
14. **Proportional asymptotics.** Ridgeless least squares and double descent (Hastie, Montanari, Rosset & Tibshirani
    2022), the peak at γ = 1 computed; benign overfitting (Bartlett et al. 2020); cross-reference *AI, Built* Part 8.
15. **Low rank.** Matrix completion with the nuclear norm (Candès & Recht 2009); SoftImpute (Mazumder, Hastie &
    Tibshirani 2010).
16. **Outro.**

*Built:* statkit.sparse (coordinate-descent paths, debiased lasso, polyhedral inference); the phantom recovery; the
Donoho–Tanner diagram (resumable sweep).

#### Part 26 · Thousands of Questions: Multiple Testing, Selection and Replication (~58)
*Question:* ask enough questions and chance will answer some. Which answers are real?
*Story:* a dead salmon "responds" to photographs in an fMRI scanner. Benjamini and Hochberg change what it means to
control error, knockoffs build fake variables to catch false ones, and a simulator shows how forking paths
manufacture discoveries. Then the replication crisis, measured. Can prediction instead of inference come with
honest guarantees (→ Part 27)?

0. **Hook: the dead salmon** (Bennett et al. 2009/2010). Voxels "active" in a dead fish without multiplicity
   correction.
1. **The problem.** m tests at 5%; the World's 5,000-gene study with 100 real effects; the p-value histogram as a
   uniform with a spike (`PValueSea`).
2. **Familywise error.** Bonferroni, Šidák; Holm (1979) via closed testing (Marcus, Peritz & Gabriel 1976); Hochberg
   and Simes (1986); Westfall–Young permutation (1993).
3. **The false discovery rate** (Benjamini & Hochberg 1995).
   - The BH line sweeping the sorted p-values.
   - FDR ≤ (m₀/m)q under independence, proved; PRDS and Benjamini–Yekutieli (2001).
4. **Adaptive FDR.** Estimating π₀ (Storey 2002); q-values; weighted BH.
5. **The empirical Bayes view** (Efron 2001, 2010).
   - The two-groups model; local fdr = π₀f₀/f; BH as tail-area Fdr.
   - The prostate microarray (Singh et al. 2002; 6,033 genes); the empirical null (Efron 2004).
6. **FDR is an average.** The false discovery proportion's spread, and dependence (computed; Board).
7. **Knockoffs** (Barber & Candès 2015; model-X, Candès et al. 2018). Variables exchangeable with the real ones; the
   knockoff filter and its FDR proof via coin-flip signs; the World's genome with the lasso.
8. **Selective inference.** The winner's curse; conditioning on selection (Fithian, Sun & Taylor 2014); data
   splitting vs carving vs fission (Leiner et al.), with power compared.
9. **The garden of forking paths** (Gelman & Loken 2013).
   - Researcher degrees of freedom (Simmons, Nelson & Simonsohn 2011).
   - *Built:* a p-hacking simulator (optional stopping, covariate choice, outlier rules, subgroups) driving the false
     positive rate far above 5% on the World.
10. **The replication crisis.**
    - Ioannidis (2005): the PPV from power, prior odds and α, derived.
    - The Open Science Collaboration (2015); Camerer et al. (2018); Bem (2011).
11. **Publication bias.** The file drawer (Rosenthal 1979); funnel plots and Egger's test (1997); p-curve (Simonsohn,
    Nelson & Simmons 2014); selection models (Hedges 1984; Andrews & Kasy 2019); a biased literature simulated.
12. **Remedies, argued.**
    - Preregistration and registered reports (Nosek et al. 2018; Chambers 2013).
    - α = 0.005 (Benjamin et al. 2018) and its rebuttal (Lakens et al. 2018); "abandon significance" (McShane et
      al. 2019); the ASA statements.
13. **Online FDR.** α-investing (Foster & Stine 2008); LORD (Javanmard & Montanari 2018); e-BH (Part 35).
14. **The false coverage rate** (Benjamini & Yekutieli 2005). Intervals for selected parameters (Board).
15. **Outro.**

*Built:* statkit.multiple (Holm, Hochberg, BH, BY, Storey, local fdr, knockoffs); the p-hacking simulator.
*Data:* the prostate microarray (Singh et al. 2002; license checked; otherwise the World's expression study).

#### Part 27 · The Two Cultures: Prediction, Calibration and Conformal Inference (~58)
*Question:* can a black-box prediction come with an honest guarantee?
*Story:* Breiman tells statisticians that algorithms have won. Forests and boosting turn out to be statistical
estimators with their own inference. Conformal prediction gives any model finite-sample coverage using only
exchangeability and ranks, and prediction-powered inference turns ML guesses into valid estimates. But a model that
predicts well can be useless for deciding what to do (→ Part 28).

0. **Hook: Breiman (2001), "Statistical Modeling: The Two Cultures."** Data models vs algorithmic models; his
   consulting stories; the replies of Cox and Efron.
1. **Explain or predict?** The Rashomon effect; Shmueli (2010).
2. **The decomposition of prediction error.** Approximation vs estimation (cross-reference *AI, Built* Part 8).
3. **Trees** (CART; Breiman et al. 1984). Recursive partitioning as an adaptive histogram; cost-complexity pruning;
   instability.
4. **Forests.**
   - Bagging plus feature subsampling; the variance ρσ² + (1 − ρ)σ²/B; consistency (Scornet, Biau & Vert 2015).
   - Permutation importance and its correlation bias (Strobl et al. 2007, 2008).
   - Intervals by the infinitesimal jackknife (Wager, Hastie & Efron 2014) (Board).
5. **Boosting as statistics.** Stagewise additive modelling (Friedman, Hastie & Tibshirani 2000; Friedman 2001);
   shrinkage and early stopping as regularization.
6. **What CV estimates** (Bates, Hastie & Tibshirani 2024). The procedure's error, not the fitted model's; nested CV.
7. **Calibration.** Reliability diagrams; Platt, isotonic (PAVA from Part 23) and temperature scaling (Guo et al.
   2017); the bias of calibration-error estimates.
8. **Conformal I.**
   - Exchangeability (Part 4) + ranks (Part 22) = finite-sample coverage.
   - Split conformal (Papadopoulos et al. 2002; Lei et al. 2018): the ⌈(n + 1)(1 − α)⌉-th residual, coverage in
     [1 − α, 1 − α + 1/(n + 1)] (derived).
   - Wilks' tolerance limits as its ancestor. Board: kept, for any model and any distribution.
9. **Conformal II.** Full conformal (Vovk, Gammerman & Shafer 2005); jackknife+ and CV+ (Barber et al. 2021);
   conformal quantile regression (Romano, Patterson & Candès 2019) with adaptive widths.
10. **Conformal III: the limits.**
    - Exact conditional coverage is impossible (Vovk 2012; Foygel Barber et al. 2021).
    - Mondrian (group-conditional) conformal; guarantees over function classes (Gibbs, Cherian & Candès 2023);
      adaptive prediction sets for classifiers (Romano, Sesia & Candès 2020).
11. **Conformal under shift.**
    - Weighted conformal for covariate shift (Tibshirani et al. 2019) (Board: unweighted broken, weighted kept).
    - Beyond exchangeability (Barber et al. 2023); adaptive conformal inference online (Gibbs & Candès 2021).
12. **Risk control.** Conformal risk control and learn-then-test (Angelopoulos et al.), as multiple testing
    (Part 26).
13. **Prediction-powered inference** (Angelopoulos, Bates, Fannjiang, Jordan & Zrnic 2023).
    - The rectifier derived; PPI++ (Angelopoulos, Duchi & Zrnic 2023).
    - Board: "predictions as data" broken; classical kept but wide; PPI kept and narrower.
14. **Interpretation as estimation.** Partial dependence (Friedman 2001); SHAP (Lundberg & Lee 2017) as Shapley values
    (1953): what they estimate, marginal vs conditional; LOCO importance (Lei et al. 2018).
15. **Outro.** Asthma patients predicted to be at low risk of pneumonia death, because they had received aggressive
    care (Caruana et al. 2015). Prediction is not intervention.

*Built:* statkit.conformal (split, jackknife+, CV+, CQR, weighted, ACI) and statkit.ppi; a forest with IJ variances.

### Act VII · Causes

#### Part 28 · What If? Potential Outcomes and Randomized Experiments (~58)
*Question:* what does it mean for one thing to cause another, and why does randomization let us find out?
*Story:* the 1954 polio trial ran two designs side by side, and only the randomized one told the truth. Neyman's
potential outcomes make causation precise, and the World, uniquely, shows both outcomes for every person. We cover
randomization inference, Neyman's variance, noncompliance and LATE, interference, and surrogates that kill. When you
cannot randomize (→ Part 29)?

0. **Hook: the Salk trial (1954).** The observed-control design vs the randomized placebo design; consent correlated
   with income and susceptibility; the published rates (Francis 1955; Meier 1972; Freedman, Pisani & Purves).
1. **Potential outcomes** (Neyman 1923; Rubin 1974). Y(1), Y(0), unit effects; Holland's (1986) fundamental problem:
   the `ScienceTable` with half its cells hidden, and in the World, revealed.
2. **Estimands and SUTVA.** ATE, ATT, CATE; no interference, one version of treatment; "no causation without
   manipulation".
3. **Why randomization works.** Assignment ⟂ potential outcomes; the difference in means is unbiased (derived); naive
   difference = ATT + selection bias, measured on the World's confounded treatment.
4. **Fisher's sharp null.** Exact randomization p-values by enumerating assignments; inverting for constant effects.
5. **Neyman's repeated sampling.** The finite-population variance; the unidentifiable Var(τᵢ) and the conservative
   estimator, derived (Board: conservative).
6. **Stratified and paired experiments.** Blocking's variance reduction; matched pairs.
7. **Adjustment.** Freedman (2008) and Lin (2013): interactions plus HC SEs never hurt asymptotically (Board).
8. **Cluster randomization.** Design effects and the ICC; analyze at the unit of randomization (Board: per-person
   analysis broken).
9. **Noncompliance.**
   - ITT; principal strata (Frangakis & Rubin 2002).
   - LATE = ITT_Y/ITT_D under monotonicity (Imbens & Angrist 1994; Angrist, Imbens & Rubin 1996), derived.
10. **Interference.** Herd immunity; exposure mappings (Aronow & Samii 2017); two-stage randomization (Hudgens &
    Halloran 2008).
11. **Subgroups.** ISIS-2's astrological signs (1988); honest subgroup discovery with sample splitting.
12. **A short history of the RCT.**
    - Lind's scurvy (1747); Peirce & Jastrow (1884); Fisher; the MRC streptomycin trial (1948).
    - Blinding and placebos; equipoise and research ethics.
    - Platform trials (RECOVERY 2020).
13. **Surrogates.** CAST (1989): suppressed arrhythmias, more deaths; Prentice's criteria (1989); the surrogate
    paradox.
14. **External validity.** Transporting a trial to a target population (Stuart et al. 2011; Pearl & Bareinboim
    2014; Dahabreh et al. 2019), by reweighting the World's trial to the whole World.
15. **Outro.**

*Board rows:* the naive difference (broken); the difference in means (kept); Neyman's variance (conservative); Lin
(kept); a cluster trial analyzed per person (broken).
*Built:* the World's clinic, a trial simulator with both potential outcomes visible; statkit.causal (part 1).
*Data:* the Salk trial tables (published).

#### Part 29 · Causes Without Experiments (~60)
*Question:* when you cannot randomize, what can still be learned about causes, and what does it cost in assumptions?
*Story:* LaLonde throws away an experiment's controls and asks econometrics to recover the answer, and it fails.
Graphs say what to adjust for. Propensity scores, double robustness and debiased machine learning do the adjusting.
Sensitivity analysis says how wrong we might be, and smoking shows how a causal case was won without a trial.
Sometimes nature randomizes for us (→ Part 30).

0. **Hook: LaLonde (1986).** The NSW experimental benchmark against non-experimental estimates from survey controls,
   which miss wildly. Dehejia & Wahba (1999) with propensity scores; Smith & Todd (2005) on fragility.
1. **Confounding** in the World; unconfoundedness and overlap.
2. **Causal graphs** (Wright 1921; Pearl 1995, 2000). Chains, forks, colliders; d-separation (`CausalGraph`, with
   association pulses).
3. **The back-door criterion.** The adjustment formula, derived. What not to adjust for: colliders (Berkson 1946),
   mediators, M-bias; the Table 2 fallacy (Westreich & Greenland 2013).
4. **Front door and do-calculus.** The front-door formula; Pearl's three rules (1995) and completeness (Shpitser &
   Pearl 2006; Huang & Valtorta 2006); SWIGs (Richardson & Robins 2013).
5. **Simpson resolved.** One table, two correct answers, depending on the graph.
6. **Outcome modelling.** g-computation (Robins 1986); model dependence and extrapolation without overlap (computed).
7. **Propensity scores** (Rosenbaum & Rubin 1983).
   - The balancing theorem, derived.
   - Matching, subclassification (Cochran 1968: five strata remove most of the bias), balance diagnostics.
8. **Inverse probability weighting.** Unbiasedness (Horvitz–Thompson again, Part 34); extreme weights and trimming
   (Crump et al. 2009); Board.
9. **Double robustness.**
   - AIPW (Robins, Rotnitzky & Zhao 1994), derived; the four Kang–Schafer (2007) scenarios computed.
   - The efficient influence function of the ATE (Hahn 1998), from Part 13.
10. **Double/debiased ML** (Chernozhukov et al. 2018).
    - Neyman orthogonality: first-order insensitivity to nuisance errors, derived; cross-fitting.
    - TMLE (van der Laan & Rubin 2006). Board: ML plug-in broken, DML kept.
11. **Heterogeneous effects.** S-, T-, X- (Künzel et al. 2019), R- (Nie & Wager 2021) and DR-learners (Kennedy 2023);
    causal forests with honesty (Wager & Athey 2018), graded against the World's true CATE.
12. **Sensitivity.** Cornfield's inequality (1959); Rosenbaum's Γ; E-values (VanderWeele & Ding 2017), derived;
    omitted-variable-bias contours (Cinelli & Hazlett 2020).
13. **Smoking and lung cancer.** Doll & Hill (1950, 1954); Fisher's constitutional hypothesis (1958); Cornfield's
    reply; Hill's viewpoints (1965).
14. **Treatments over time.** Treatment–confounder feedback; marginal structural models (Robins, Hernán & Brumback
    2000); target-trial emulation (Hernán & Robins 2016).
15. **Causal discovery.** The PC algorithm (Spirtes, Glymour & Scheines); Markov equivalence classes; LiNGAM (Shimizu
    et al. 2006); invariant causal prediction (Peters, Bühlmann & Meinshausen 2016); the limits.
16. **LaLonde revisited.** Modern estimators on the NSW data and the decisive role of overlap (Imbens & Xu, recent
    re-analysis *(verify)*).
17. **Outro.**

*Built:* statkit.causal (IPW, AIPW, cross-fitted DML, a causal forest).
*Data:* NSW/LaLonde (Dehejia–Wahba sample; license checked).

#### Part 30 · Natural Experiments: Instruments, Discontinuities and Differences (~60)
*Question:* when the world runs an experiment by accident, how do you read it?
*Story:* two water companies' pipes ran down the same London streets, and Snow counted the dead. Instruments,
cutoffs and differences-in-differences each borrow a piece of randomization. A 2021 revolution showed that the
standard panel regression can get the sign wrong. Data in time come next (→ Part 31).

0. **Hook: Snow's Grand Experiment (1854).** Southwark & Vauxhall vs Lambeth; 315 vs 37 deaths per 10,000 houses (Snow
   1855, Table IX).
1. **The credibility revolution.** Leamer (1983), "Let's take the con out of econometrics"; Angrist & Pischke (2010);
   the 2021 Nobel.
2. **Instrumental variables.**
   - Wright (1928) on supply and demand; relevance and exclusion in a DAG; Wald's estimator; 2SLS as two
     projections.
   - The draft lottery (Angrist 1990); quarter of birth (Angrist & Krueger 1991).
3. **LATE, observationally.** Compliers and their characteristics (Abadie 2003).
4. **Weak instruments.**
   - Bias toward OLS (Bound, Jaeger & Baker 1995); the F > 10 rule (Staiger & Stock 1997); Stock–Yogo; the tF
     procedure (Lee et al. 2022).
   - Anderson–Rubin (1949) (Board: 2SLS Wald broken, AR kept).
5. **More instruments.** Overidentification (Sargan–Hansen); LIML; judge designs; Mendelian randomization (Katan 1986;
   Davey Smith & Ebrahim 2003) and pleiotropy (MR-Egger, Bowden et al. 2015).
6. **Regression discontinuity** (Thistlethwaite & Campbell 1960).
   - Identification by continuity, derived; local linear estimation at a boundary (Part 23).
   - Bandwidths (Imbens & Kalyanaraman 2012); robust bias-corrected intervals (Calonico, Cattaneo & Titiunik 2014)
     (Board).
   - *Built:* the World's scholarship cutoff.
7. **RD validity.** Manipulation tests (McCrary 2008; Cattaneo, Jansson & Ma 2020); placebo cutoffs; fuzzy RD as IV;
   close elections (Lee 2008); kinks.
8. **Difference-in-differences.** The 2×2 (Snow recast; Card & Krueger 1994); parallel trends; event studies; the
   Ashenfelter dip.
9. **DiD inference.** Serial correlation and placebo laws (Bertrand, Duflo & Mullainathan 2004); clustering at the
   policy level; few treated clusters (Conley & Taber 2011).
10. **Staggered adoption.**
    - TWFE as a weighted average with negative weights (Goodman-Bacon 2021; de Chaisemartin & D'Haultfœuille 2020).
      On the World's staggered policy, TWFE gets the sign wrong (computed).
    - Callaway & Sant'Anna (2021), Sun & Abraham (2021), Borusyak, Jaravel & Spiess (2024) (Board).
11. **Parallel trends, stress-tested.** Problems with pre-testing (Roth 2022); honest DiD (Rambachan & Roth 2023).
12. **Synthetic control** (Abadie & Gardeazabal 2003; Abadie, Diamond & Hainmueller 2010).
    - California's Proposition 99; donor weights on a simplex; placebo-in-space inference.
    - Augmented synthetic control (Ben-Michael, Feller & Rothstein 2021).
13. **Synthetic DiD** (Arkhangelsky et al. 2021) as the unifier; matrix completion for panels (Athey et al. 2021;
    Part 25).
14. **Panel data.** Fixed effects and first differences; the within transformation as FWL; Nickell bias (1981);
    Arellano–Bond (1991).
15. **Partial identification** (Manski 1990). No-assumption bounds; monotone treatment response; Lee bounds for
    attrition (2009): what can be said with less.
16. **Outro.**

*Built:* statkit.quasi (2SLS, AR, robust RD, Callaway–Sant'Anna, synthetic control); the World's natural experiments.
*Data:* Snow (1855); Card & Krueger summary means; Prop 99 (replication data, license checked).

### Act VIII · Data with Structure

#### Part 31 · Time Series: Memory, Spectra and the Hidden State (~60)
*Question:* how do you do statistics when each observation remembers the last?
*Story:* Yule finds that marriages in the Church of England "predict" mortality, and invents autoregression to
explain sunspots. Unit roots have non-normal limits built from Brownian motion, volatility clusters, the Nile
remembers for centuries, and Kalman's filter tracks what cannot be seen. Space comes next (→ Part 32).

0. **Hook: Yule (1926, 1927).** C of E marriages vs mortality, 1866–1911, r ≈ 0.95; AR(2) fitted to Wolf's sunspots.
1. **Stationarity.**
   - The autocovariance and its positive definiteness; the ACF; ergodicity (Part 6).
   - The effective sample size of an AR(1) mean, derived (Board: the iid CI broken; HAC kept).
2. **Linear processes.** MA, AR, ARMA; causality and invertibility from the roots of φ(z) (the unit circle, drawn);
   Wold (1938).
3. **Pseudo-cycles.** Complex AR(2) roots; Slutsky (1927): sums of random shocks look like business cycles.
4. **Fitting.** ACF/PACF signatures; Yule–Walker, derived; Durbin–Levinson; exact Gaussian likelihood; Box & Jenkins
   (1970); Ljung–Box (1978).
5. **Forecasting.** Best linear prediction as projection; error variance growing with the horizon; intervals; MASE and
   Diebold–Mariano (1995); the M-competitions' lessons (simple methods and combinations are hard to beat).
6. **Spectra.**
   - The spectral density as the Fourier transform of γ (Herglotz; cross-reference *Analysis* Part 9).
   - The periodogram (Schuster 1898) is inconsistent (computed); Bartlett, Welch (1967), multitaper (Thomson 1982).
   - The sunspot cycle recovered.
7. **Seasonality and trend.** STL (Cleveland et al. 1990); seasonal ARIMA; exponential smoothing in state-space form
   (Hyndman et al. 2002).
8. **Unit roots.**
   - Dickey–Fuller (1979): the t-statistic's limit as a functional of Brownian motion, derived via Donsker (Part 6);
     the distribution computed.
   - KPSS (1992).
9. **Spurious regression** (Granger & Newbold 1974; Phillips 1986). Two independent random walks give exploding
   t-statistics (Board).
   - Cointegration (Engle & Granger 1987) and error correction; the drunk and her dog (Murray 1994).
10. **Volatility.** Stylized facts of returns; ARCH (Engle 1982); GARCH(1,1) (Bollerslev 1986) with its likelihood
    and persistence; VaR backtests (Kupiec 1995).
11. **Long memory.** Hurst's Nile (1951) and the R/S statistic; ARFIMA (Granger & Joyeux 1980; Hosking 1981); the
    Nile minima, 622–1284 (Toussoun 1925).
12. **The Kalman filter (1960).**
    - Derived as Gaussian conditioning (Part 4), with `KalmanEllipses`.
    - The local-level model on the Nile's annual flow, 1871–1970, and its drop around 1899 (Cobb 1978; Durbin &
      Koopman). The Kalman gain as shrinkage.
13. **Smoothing and learning.** The RTS smoother (1965); the prediction-error decomposition of the likelihood; EM for
    state-space models (Shumway & Stoffer 1982); structural time series (Harvey 1989); Apollo navigation (McGee &
    Schmidt 1985).
14. **Beyond linear-Gaussian.** EKF and UKF; particle filters for stochastic volatility (Part 19); regime switching
    (Hamilton 1989).
15. **Many series.** VARs (Sims 1980); Granger causality (1969) as predictability, not causation (a computed
    counterexample); impulse responses.
16. **Frontier.** Pretrained forecasting models and how to evaluate them honestly (leakage, rolling origins) *(verify
    current models)*; adaptive conformal intervals for series (Part 27).
17. **Outro.**

*Built:* statkit.ts (ARMA likelihood, spectra, Dickey–Fuller, GARCH, Kalman filter and RTS smoother), checked
against statsmodels.
*Data:* Yule (1926); Yule's sunspot series as published; the Nile (historical records); Toussoun (1925); NOAA Mauna
Loa CO₂.

#### Part 32 · Space: Spatial Statistics and Gaussian Processes (~58)
*Question:* how do you predict a value where nobody measured, and how sure can you be?
*Story:* a mining engineer estimates gold grades from boreholes. Kriging is the best linear predictor, Matérn says
how smooth the world is, and some parameters cannot be learned no matter how densely you sample. Sparse precision
matrices and an SPDE make it scale, point patterns test for clustering, and Gaussian processes bring it into machine
learning. Next, time measured to an event (→ Part 33).

0. **Hook: Krige (1951) on the Witwatersrand; Matheron's (1963) theory.**
1. **Spatial data.** Tobler's first law (1970); geostatistical, areal and point data; the World's pollution field.
2. **Random fields.** Stationarity and isotropy; Bochner's theorem (positive definite ⇔ nonnegative spectral
   measure).
3. **The variogram.** Nugget, sill, range; empirical and robust variograms (Cressie & Hawkins 1980); fitting.
4. **Kriging.**
   - The BLUP with a Lagrange multiplier for unbiasedness, derived; simple, ordinary and universal kriging.
   - The variance map (`FieldSurface`); kriging = the GP posterior mean (cross-reference *AI, Built* Part 7).
5. **Matérn (1960).**
   - Smoothness ν and its spectral density; Stein's (1999) case for Matérn; the screening effect.
   - Infill asymptotics: only σ²/ρ^{2ν} is identifiable (Zhang 2004), shown as the likelihood ridge.
6. **Likelihood estimation.** ML and REML for covariance parameters (Part 17); the O(n³) cost.
7. **Scaling up.** Tapering; low-rank predictive processes (Banerjee et al. 2008); Vecchia (1988) and NNGP (Datta et
   al. 2016). *Built:* a Vecchia GP on 100,000 World locations.
8. **GMRFs and the SPDE link** (Rue & Held 2005; Lindgren, Rue & Lindström 2011). Matérn fields as solutions of
   (κ² − Δ)^{α/2}x = W, sketched; INLA.
9. **Areal data.**
   - Moran's I (1950), Geary's C (1954); CAR and SAR (Besag 1974).
   - BYM disease mapping (Besag, York & Mollié 1991) as partial pooling (Part 17); the modifiable areal unit problem.
10. **Point processes.**
    - Intensities; Ripley's K and L with simulation envelopes; clustering (Neyman–Scott, Thomas) vs inhibition
      (Strauss); log-Gaussian Cox processes (Møller et al. 1998).
    - Snow's cholera map as a point pattern.
11. **Spatial confounding.** Adding a spatial random effect changes the fixed effects (Hodges & Reich 2010).
12. **Space–time.** Separable vs nonseparable covariances (Gneiting 2002); kriging the World's pollution through time.
13. **Gaussian processes in ML** (Rasmussen & Williams 2006). Kernels as priors over functions; marginal likelihood;
    Bayesian optimization; emulators for computer experiments (Sacks et al. 1989; Kennedy & O'Hagan 2001).
14. **Honest spatial prediction.** Kriging intervals with estimated vs true parameters and misspecified smoothness
    (Board).
15. **Outro.**

*Built:* statkit.spatial (variograms, kriging, Matérn likelihood, Vecchia, Ripley's K).

#### Part 33 · Time to Event: Survival Analysis (~58)
*Question:* how do you average lifetimes you have not finished watching?
*Story:* a leukemia trial ends with many patients still in remission. Kaplan and Meier's product-limit estimator,
Aalen's martingales and Cox's partial likelihood build the theory, and then the traps: hazard ratios that mislead,
immortal time, competing risks, frailty. Censoring is one kind of missing data; who else is missing (→ Part 34)?

0. **Hook: Freireich et al. (1963).** The 6-MP trial's 21 pairs, with remission times censored at analysis (Gehan
   1965).
1. **Lifetimes.** S(t), the hazard h = f/S, H, and S = e^{−H}, derived; Graunt (1662) and Halley (1693) again;
   Gompertz (1825).
2. **Censoring and truncation.** Right, left and interval; independent censoring; why dropping or miscoding censored
   cases biases (Board).
3. **Kaplan–Meier (1958).** The product-limit estimator derived; the shrinking risk set (`KMStaircase`); KM as an
   NPMLE; redistribute-to-the-right (Efron 1967).
4. **Greenwood's formula (1926)** via the delta method; log-log intervals (Board).
5. **Nelson–Aalen** (Nelson 1969; Aalen 1978) and Breslow.
6. **Counting processes.** N(t) − ∫Y(s)h(s)ds is a martingale (Aalen 1978); Rebolledo's martingale CLT (1980); all
   the asymptotics at once (Andersen, Borgan, Gill & Keiding 1993).
7. **The log-rank test** (Mantel 1966; Peto & Peto 1972). O − E summed over risk sets via the hypergeometric,
   derived; weighted versions (Fleming–Harrington); crossing hazards.
8. **Cox (1972).** The partial likelihood ("of those at risk, why this one?"), derived; the baseline drops out; Cox
   (1975); ties (Breslow; Efron 1977).
9. **Checking Cox.** Schoenfeld residuals (1982) and the Grambsch–Therneau test (1994); time-varying coefficients;
   strata.
10. **What hazard ratios mean.** Built-in selection and noncollapsibility (Hernán 2010; Martinussen, Vansteelandt &
    Andersen 2020): constant individual effects, a drifting population HR (computed); RMST (Royston & Parmar 2013).
11. **Immortal time** (Suissa 2008). The Oscar-winners longevity debate (Redelmeier & Singh 2001; Sylvestre et al.
    2006), recomputed on the World.
12. **Parametric and AFT models.** Exponential, Weibull, log-normal, log-logistic; Buckley–James (1979).
13. **Competing risks.** Cause-specific vs subdistribution hazards (Fine & Gray 1999); Aalen–Johansen; why 1 − KM
    overestimates (computed).
14. **Frailty.** Gamma frailty (Vaupel, Manton & Stallard 1979): the population hazard falls as the frail die first;
    multi-state models; recurrent events (Andersen & Gill 1982).
15. **Prediction.** Concordance (Harrell 1982; Uno et al. 2011); IPCW Brier scores (Graf et al. 1999); random survival
    forests (Ishwaran et al. 2008); conformal survival bounds (Candès, Lei & Ren 2023).
16. **Outro.**

*Built:* statkit.survival (KM, Nelson–Aalen, log-rank, Cox with Breslow/Efron ties, Aalen–Johansen), checked against
statsmodels.
*Data:* Freireich/Gehan (published table).

#### Part 34 · Who's Missing? Surveys, Missing Data and Selection (~60)
*Question:* your data are a sample of someone. Who is missing, and does it matter?
*Story:* 2.4 million ballots lose to 50,000 interviews. Meng's identity shows why size cannot buy back a tiny
selection bias. Neyman's design-based inference, Horvitz–Thompson, raking and MRP fix samples, and Rubin's missing
data theory, multiple imputation and Heckman fix datasets. Differential privacy adds missingness on purpose. So far
the sample size was fixed in advance; what if you watch the data arrive (→ Part 35)?

0. **Hook: the *Literary Digest* (1936).** About 10 million ballots mailed and 2.4 million returned predicted Landon;
   Roosevelt won about 61%. Gallup's far smaller sample called it.
1. **What went wrong.** Frame bias and nonresponse (Squire 1988), recreated on the World: 2.4 million self-selected
   vs 1,000 random.
2. **Meng's identity (2018).** Error = data defect correlation × √((N − n)/n) × σ, derived exactly; the effective
   sample size of a huge biased sample (computed).
3. **Design-based inference** (Neyman 1934). Randomness from the design, not a model; Kiær's representative method
   (1895); Bowley.
4. **Horvitz–Thompson (1952).** Unbiasedness from inclusion probabilities; its variance (Sen–Yates–Grundy); Basu's
   elephants (1971).
5. **Stratification.** Variance reduction; Neyman allocation n_h ∝ N_hS_h (derived); post-stratification.
6. **Clusters and stages.** Kish's design effect 1 + (m − 1)ρ; PPS (Hansen & Hurwitz 1943); systematic sampling.
7. **Using auxiliary information.**
   - Laplace's ratio estimator (1802) again; GREG (Särndal, Swensson & Wretman 1992).
   - Calibration (Deville & Särndal 1992) and raking (Deming & Stephan 1940), with iterative proportional fitting
     animated.
8. **Nonresponse and polls.** Propensity weighting; "Dewey defeats Truman" (1948) and quota sampling; the 2016 and
   2020 polling errors (AAPOR reviews); total survey error.
9. **MRP** (Gelman & Little 1997; Park, Gelman & Bafumi 2004). The Xbox poll (Wang, Rothschild, Goel & Gelman 2015);
   MRP on the World's self-selected sample (Board).
10. **Missingness mechanisms** (Rubin 1976). MCAR, MAR, MNAR; ignorability for likelihood inference, derived; graphical
    views (Mohan & Pearl 2021).
11. **The easy methods and their sins.** Complete cases (Board: broken under MAR); mean imputation shrinks variance;
    LOCF.
12. **Likelihood under MAR.** EM for a multivariate normal with holes (Part 9); FIML.
13. **Multiple imputation** (Rubin 1987).
    - Proper imputation; Rubin's rules T = Ū + (1 + 1/m)B, derived; the fraction of missing information;
      Barnard–Rubin degrees of freedom.
    - Chained equations (van Buuren); congeniality (Meng 1994). Board: kept.
14. **Weighting = causal inference.** IPW and AIPW for missing outcomes (Robins, Rotnitzky & Zhao 1994): a missing
    value is a missing potential outcome (Part 29).
15. **MNAR.** Heckman's selection model (1979) and the inverse Mills ratio, derived; pattern mixtures; δ-adjusted
    tipping-point analyses; Manski bounds (Part 30).
16. **Measurement error.** Spearman's attenuation correction (1904); regression calibration; SIMEX (Cook & Stefanski
    1994), with its extrapolation animated; misclassification.
17. **Noise on purpose.**
    - Randomized response (Warner 1965) as local privacy; differential privacy (Dwork, McSherry, Nissim & Smith 2006)
      and the Laplace mechanism, derived.
    - The 2020 US Census TopDown algorithm (Abowd et al. 2022) and its statistical cost for small areas, recreated
      on the World's towns.
18. **Outro.**

*Built:* statkit.survey (HT, stratified and cluster SEs, raking, GREG) and statkit.mi (chained equations with Rubin's
rules); the World's polling firm.
*Data:* Literary Digest and Gallup figures (published).

### Finale

#### Part 35 · Watching as You Go: Sequential and Anytime-Valid Inference (~58)
*Question:* what if you look at the data every day and stop when it looks good?
*Story:* a Navy captain complains that ordnance tests run long after the answer is obvious, and Wald invents the
sequential probability ratio test. Peeking breaks every fixed-sample promise; alpha spending patches it for
clinical trials; and Ville's 1939 inequality, through betting, e-values and confidence sequences, rebuilds testing
so that you may look whenever you like. Last, what all of this means when the questions are about AI (→ Part 36).

0. **Hook: the Statistical Research Group (1943).** Schuyler's complaint; Wald's SPRT, classified until 1945 (Wallis
   1980). The modern A/B-test dashboard refreshed hourly.
1. **The peeking problem.** Checking a t-test after every observation and stopping at p < 0.05: the false-positive
   rate climbs toward 1 (the LIL, Part 5) (Armitage, McPherson & Rowe 1969; computed; Board).
2. **Wald's SPRT.**
   - A likelihood-ratio walk between barriers; A ≈ (1 − β)/α and B ≈ β/(1 − α), derived.
   - Wald's identity for the expected sample size; savings over fixed n (computed); optimality (Wald & Wolfowitz
     1948).
3. **Group sequential trials.** Pocock (1977), O'Brien–Fleming (1979), Lan–DeMets spending (1983) in the Brownian
   picture; stopping for benefit or futility; the bias of estimates after early stopping (computed).
4. **The Bayesian view.** The posterior ignores the stopping rule (the likelihood principle, Part 9), but its error
   rates do not (computed). The debate presented fairly.
5. **Test martingales.** Ville (Part 6) as betting: wealth against H₀; P(sup W ≥ 1/α) ≤ α (`BettingPaths`).
6. **Testing by betting** (Shafer 2021; Shafer & Vovk). e-values as payoffs; calibrators between p and e (Vovk & Wang
   2021); combining e-values by averaging and multiplying.
7. **Building e-processes.**
   - Likelihood ratios; mixtures (Robbins 1970); universal inference by the split LRT (Wasserman, Ramdas &
     Balakrishnan 2020).
   - GROW e-values (Grünwald, de Heide & Koolen 2024); Kelly betting (1956) and online betting strategies.
8. **Confidence sequences.**
   - Darling & Robbins (1967); time-uniform boundaries at the LIL rate (Howard et al. 2021).
   - Betting confidence sequences for bounded means (Waudby-Smith & Ramdas 2024), tighter than Hoeffding (computed;
     Board).
9. **Anytime-valid A/B tests.** mSPRT and always-valid p-values (Johari et al. 2017, 2022); asymptotic confidence
   sequences *(verify current reference)*.
10. **Sequential multiple testing.** e-BH (Wang & Ramdas 2022) under arbitrary dependence; online FDR (Part 26).
11. **Change points.**
    - CUSUM (Page 1954) as repeated SPRTs; Lorden's criterion (1971) and optimality (Moustakides 1986);
      Shiryaev–Roberts.
    - Bayesian online change-point detection (Adams & MacKay 2007); PELT (Killick, Fearnhead & Eckley 2012); the
      World's factory drift.
12. **Adaptive experiments.** Thompson (1933); Robbins (1952); the Lai–Robbins bound (1985); regret vs inference
    (cross-reference *AI, Built* Part 26).
13. **Inference after adaptivity.** Sample means are biased under bandit sampling (Nie et al. 2018); adaptively
    weighted estimators (Hadad et al. 2021); batched bandits (Zhang, Janson & Murphy 2020) (Board).
14. **Adaptive trials and ethics.** Play-the-winner (Zelen 1969); the ECMO trials (Bartlett et al. 1985; Ware 1989).
15. **Outro.**

*Built:* statkit.sequential (SPRT, spending functions, mixture and betting CSs, mSPRT, e-BH, CUSUM); the World's A/B
platform, which the viewer can peek at.

#### Part 36 · What Can We Honestly Claim? Statistics in the Age of AI (~58; the finale)
*Question:* when machines make the predictions, generate the data and grade each other, what does honest uncertainty
look like?
*Story:* Graunt's ledger has become a leaderboard. Benchmarks are samples, arenas are logistic regressions, labels
come from models, data from generators, and every lesson of the series applies. The complete Coverage Board shows
which promises held, and we return to Graunt.

0. **Hook: a leaderboard.** 85.2% against 84.7%: is the difference real? Back to Graunt's question.
1. **Benchmarks are samples.** Questions drawn from a population of questions; standard errors; clustered questions
   (Miller 2024) (Board: naive broken, clustered kept).
2. **Paired comparisons.** Two models on the same items; McNemar; power for evaluations; leaderboard multiplicity
   (Part 26).
3. **Arenas.** Bradley–Terry (1952) and Elo as logistic regression (Part 16); sandwich and bootstrap intervals
   (Chiang et al. 2024); "style control" as covariate adjustment *(verify)*.
4. **Item response theory for benchmarks.** The Rasch model (Part 17); small benchmarks via IRT *(verify: Polo et al.
   2024)*.
5. **Adaptive reuse of test sets.** The reusable holdout and Thresholdout (Dwork et al. 2015); the Ladder (Blum &
   Hardt 2015); privacy as a defence (Part 34).
6. **Labels from models.** PPI for measurement (Part 27); design-based supervised learning (Egami et al. 2023); an
   LLM judge's biases treated as measurement error (Part 34).
7. **Synthetic data.**
   - Sampling from a fitted model is a parametric bootstrap (Part 21).
   - Model collapse (Shumailov et al. 2024) as iterated estimation error: refitting a Gaussian to its own samples,
     the variance follows a multiplicative random walk with negative drift and collapses (derived and computed).
8. **Uncertainty for language models.** Calibration of model confidence (Kadavath et al. 2022); conformal methods for
   generation and factuality *(verify: Quach et al. 2024; Mohri & Hashimoto 2024)*.
9. **Watermarks as hypothesis tests.** Pivotal statistics and p-values (Kirchenbauer et al. 2023; statistical
   frameworks *(verify)*).
10. **Simulation-based inference in science** (Part 19). Amortized posteriors and their calibration failures (Hermans
    et al. 2022).
11. **Generative models as density estimators** (Part 23). The score at the heart of diffusion is Tweedie's formula
    (Part 12); statistical rates for diffusion models *(verify)*.
12. **Causal questions about AI.** A/B tests of deployed models (Part 15); interference in marketplaces; long-term
    outcomes via a surrogate index (Athey et al. 2019).
13. **Open problems.** Inference under adaptivity; causal inference at scale; high-dimensional inference beyond
    sparsity; robustness to distribution shift; reproducibility in ML research; privacy and utility; "50 years of data
    science" (Donoho 2017).
14. **The full Coverage Board.**
    - Every promise tested in the series: kept, broken, conservative.
    - Its lessons in one table: assumptions matter; asymptotics take time; selection and adaptivity break naive
      intervals; design beats analysis; honest methods exist for almost everything, if you use them.
15. **Back to Graunt.** The series in one picture; the timeline lit from 1662 to now.

*Built:* statkit.evals (clustered and paired standard errors, Bradley–Terry with sandwich SEs); the full board
(`board.load_all()`).

## 7. Phases

0. **Infrastructure** (one session):
   - The toolchain in this container: Python 3.12 venv, manim, TeX Live with xelatex and CJK, ffmpeg (README
     setup). Manim and TeX are not installed here yet.
   - `explainer/stats/`: `__init__.py` (ACTS, PARTS, `series_map`, timeline, `chapter_card`, payoff and reference
     cards), `style.py`, `viz.py` (the instruments above, built as Part 1 needs them, the rest as their parts
     arrive), `world.py`, `board.py`, `museum.py`, and `kit/`.
   - `videos/stats/__init__.py`, `STATS_ZH_GUIDE.md`, `stats_text_zh.json`, `stats_upload.json`.
   - Tools:
     - `BILINGUAL` in `tools/make.py` gains `stats`;
     - `qa_series.py`, `qa_report.py`, `qa_motion.py` and `qa_audio.py` lose their hard-coded `ai` and take
       `--series stats`;
     - `package_uploads.py --series stats`.
   - Root `README.md` table row and a `CLAUDE.md` bullet.
   - `tests/test_stats_world.py` (reproducibility and the truth table) and `tests/test_stats_board.py`.
   - A silent en + zh smoke render of a test scene.
1. **Pilot: Part 1.** It introduces the World, the Board (empty), the timeline, `SamplingMachine` and `NSpace`, so it
   tests the series' devices. It is delivered in English and Chinese with previews and contact sheets. **Review
   with the user**, then lock the standard.
2. **Roll-out in order, Parts 2 → 36.** Each part goes through:
   - the frontier sweep and the Museum's license checks;
   - locking the chapter list;
   - `compute.py` and its statkit module, with tests;
   - English scenes, then the QA gates;
   - Chinese narration and text, then the QA gates;
   - commit and push.

   Expect one part per one or two long sessions.

## 8. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| — | master plan (this file) | — |
