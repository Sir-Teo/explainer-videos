# Statistics, Built: the syllabus (plan of record, draft 2: from first course to PhD)

The goal is **a complete education in statistics on video, from a first undergraduate course to a PhD**. It is as
comprehensive and as technical as the standard texts at each level, and it ends at the research frontier. It also
tells how statistics became what it is. It is made to the standard of *Analysis, Built* and *AI, Built*: in English
and Chinese, every derivation on screen, every number computed or cited, rendering on macOS and Linux.

Scale: 65 parts of **50–60 minutes** each, about 60 hours in all. That is 14–18 chapters per part, about 470k
narration words per language, and 5–6k lines of scene code per part. The series is made by **one agent working
through the parts in order** (no subagents or workflows), following [`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md)
as adapted in §1.

Contents:

1. The standard every part meets
2. The World
3. The Coverage Board
4. The Museum
5. statkit
6. Part by part (Stages I–V)
7. Phases
8. Progress

## 1. The standard every part meets

**A chapter is a lecture segment of 3–4 minutes.** It runs in this order:

1. A motivating question, failure or historical moment.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("Jensen", "tower property", "Cauchy–Schwarz",
   "dominated convergence", "union bound", "Taylor to second order").
4. A computed experiment that checks the result, usually on the World, sometimes on Museum data.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**

- A cold-open hook (2–4 min): the historical problem the part answers, with its people, place and year.
- An objectives card listing prerequisites by part number, and the part's place on the Transcript.
- Theorem and definition cards, with at least one complete proof on screen.
- **One build.** A tool or toy the part constructs and the viewer watches working.
- **Coverage Board rows** for every interval or test the part introduces (§3).
- A problem set: 5–6 problems on screen, full solutions in the part's README in English and Chinese.
- A reference card: textbooks, the classic papers, and the frontier papers.
- An outro that recaps the part and poses the next part's question.

**Level policy.** The stage decides the rigour, prerequisites and problems.

| Stage | Assumes | Proofs | Problems |
|---|---|---|---|
| I–II (BSc) | calculus; matrices from Part 4 | every result derived at the level of Rice or Casella & Berger; limits used with care, not measure theory | computations, derivations, small data analyses |
| III (MSc) | Stages I–II; optimization from Part 21 | full derivations; asymptotic results stated with their conditions and proved in the regular case | derivations, simulations, real-data problems |
| IV (PhD core) | Stage III; *Analysis, Built* 1–6 for measure, Lᵖ and Hilbert space | theorem–proof with exact hypotheses; a counterexample for each condition that matters | qualifying-exam style proofs |
| V (PhD research) | Stage IV | the main theorem of each key paper, proved or sketched to its central idea; what is open | research-style problems, each with an open problem attached |

**The Spiral.** A result met earlier returns with an **upgrade card**: the earlier statement (with its part number),
what it quietly assumed, and what this part will prove. The Spiral table in the README is kept in step with the
syllabus.

**Milestone parts.** Parts 20, 42, 55 and 65 are the degree's milestones: the capstone analysis, the comprehensive
exam, the qualifying exam and the dissertation. They are lectures too, held to the same visual standard.
- The exams are worked problems. Each is posed, the viewer is invited to pause, and the solution is built step by
  step with its picture.
- The capstone and the dissertation are complete projects carried out on screen.

**The history thread.** Each idea is credited with its people and year, and each part opens on the timeline strip
(1650–2030). The disputes are told as disputes: Gauss and Legendre, Pearson and Fisher, Fisher and Neyman, Bayesians
and frequentists, Fisher on smoking, the credibility revolution, the replication crisis. Uncomfortable history is
acknowledged where it is part of the record, such as the eugenic aims of Galton, Pearson and Fisher, or where a
classic dataset was published.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the writing
date. Items marked *(verify)* are specific numbers or recent results that must be confirmed in the primary source
before they go on screen. A claim that cannot be checked is not used.

**Numbers are real.**

- Computed numbers come from the part's `compute.py`, cached under `.cache/statsN/`. Published numbers are cited on
  screen.
- Tags: `computed`, `simulated` (the World), `historical data` (the Museum, with source), `illustrative`,
  `schematic`.
- The narration follows the data. Where the story depends on a result, the verdict is computed and the sentence
  branches on it.
- CPU budget: ≤ 2 h per part. Coverage simulations are vectorized, 10,000 replications by default.
- Named exceptions are resumable and seeded: the NUTS runs (27), the Donoho–Tanner and AMP sweeps (32, 59), the
  random-matrix sweeps (52), the dissertation's study (65) and the full Board (65).
- Scene assertions use tolerances.

**Visual standard** (3Blue1Brown manner). Continuity over cuts, in-place derivations (`cmath` + `morph`, `ladder` +
`why`), colour as meaning, a narrating camera, live quantities.

Colour tokens (`explainer/stats/style.py`), fixed for the whole series:

| Token | Meaning |
|---|---|
| `C.TRUTH` (gold) | θ, the true curve |
| `C.EST` (blue) | θ̂, fitted curves |
| `C.DATA` (white) | observations |
| `C.NULL` (grey) | H₀ |
| `C.ALT` (teal) | H₁ |
| `C.PRIOR` (purple), `C.LIK` (green), `C.POST` (orange) | prior, likelihood, posterior |
| `C.RESID` (red) | residuals |
| `C.TREAT` (coral), `C.CTRL` (sky) | treated units, controls |
| `C.KEPT`, `C.BROKEN`, `C.CONS` | Board verdicts |
| `C.MISSING` | hollow markers |

New instruments, in `explainer/stats/viz.py`:

| Instrument | What it shows | First used |
|---|---|---|
| `SamplingMachine` | population → sample → statistic → a growing histogram of the sampling distribution | 1, 8 |
| `IntervalRain` | intervals falling against the truth line; misses turn red; a live coverage counter | 8, 11 |
| `NSpace` | a sample as a vector in Rⁿ (n = 3, camera orbit): projections, residuals, χ² as length² | 1, 4, 8, 12 |
| `BeltConstruction` | Neyman's confidence belt in the (θ, x) plane | 11, 46 |
| `LikelihoodLandscape` | 3D log-likelihood with score, curvature, profile ridge, the test trinity | 9, 22 |
| `BayesUpdate` | prior × likelihood → posterior | 15 |
| `GaltonBoard` | balls through pegs into bins | 6 |
| `ShrinkageField` | estimates pulled toward a target in 3D, with live risk | 25, 45 |
| `KernelSum` | KDE as a sum of bumps with a bandwidth slider | 16, 29 |
| `InfluenceProbe` | drag one point; estimators respond | 12, 30 |
| `BootstrapResampler` | resampling with replacement; the bootstrap world beside the real one | 16 |
| `SpectrumBulk` | eigenvalue histogram against Marchenko–Pastur; the BBP outlier | 52 |
| `L1Geometry` | ℓq balls meeting contours; soft-threshold maps | 19, 32 |
| `PValueSea` | thousands of p-values with the BH line sweeping | 33 |
| `CausalGraph` | DAGs with association pulses along open paths | 36, 62 |
| `CutoffLens` | a cutoff, a kernel window, two local fits and the jump between them | 37 |
| `ScienceTable` | potential outcomes, half hidden (in the World, revealed) | 35 |
| `KalmanEllipses` | predict and update as moving Gaussian ellipses | 38 |
| `KMStaircase` | survival steps with the risk set leaving | 40 |
| `FieldSurface` | a kriging or GP surface with variance shading | 39 |
| `BettingPaths` | wealth processes against Ville's 1/α ceiling; confidence sequences narrowing | 44, 58 |
| `TangentSpace` | a model as a surface, its tangent space, and an influence function projected onto it | 47, 49 |
| `LowerBoundPacking` | hypotheses packed as separated points with KL balls (Le Cam, Fano, Assouad) | 50 |
| `TransportFlow` | mass moving along Wasserstein geodesics; Sinkhorn's iterations | 61 |
| `Transcript` | the degree's transcript, with milestones | every outro |
| `Board` | the Coverage Board | 8 onward |

**Bilingual standard (as *AI, Built*).**

- Every narration line has its `narration_zh.json` entry and a `zh_lines.py` template.
- Every on-screen string is in `stats_text_zh.json`, and `collect_text.py --check statsN` is clean.
- The terms are in `STATS_ZH_GUIDE.md`, seeded with standard Chinese terminology (置信区间, 假设检验, 极大似然估计,
  充分统计量, 一致最小方差无偏估计, 收缩估计, 经验贝叶斯, 自助法, 稳健统计, 核密度估计, 错误发现率, 共形预测,
  倾向得分, 工具变量, 断点回归, 双重差分, 删失, 克里金, 测度论概率, 鞅, 经验过程, 半参数有效性, 极小极大,
  后验收缩, e 值, 置信序列, 最优传输, 差分隐私, …).

**Gates per part:**

- `tools/lecture_length.py` fails under 50 min.
- `contact_sheet.py`, `dead_air.py`, `collect_text.py --check`, `check_narration.py`.
- `tests/test_stats_*`: statkit against references, World invariants, Board reproducibility.
- The QA evidence loop of *AI, Built* (`qa_series.py --series stats`).

## 2. The World

`explainer/stats/world.py`: `World(seed=1662)`. It is generated lazily in chunks (it fits a laptop) and is
deterministic given the seed and the World's version. Every attribute's generating law is documented in the module,
and `world.truth(name)` returns the exact population value.

The point is pedagogical. In real data the truth is hidden; in the World every parameter, potential outcome and
missing value is known, so every method can be graded.

| Block | What it holds | Used in |
|---|---|---|
| Geography | 10 regions → 200 towns → households, with (x, y) locations | 18, 25, 31, 39 |
| People | 1,000,000 residents: age, sex, household, town | everywhere |
| Inheritance | heights for 50,000 families (bivariate normal with known heritability) | 1, 5, 12 |
| Money | incomes: a log-normal body with a Pareto tail; households | 1, 3, 8, 16, 18 |
| Schools | 400 schools with test scores (known school variance) | 25, 26 |
| Health | a disease and a screening test; blood pressure with nonlinear age effects | 2, 14, 20, 29 |
| Treatment | uptake confounded by age and health; Y(0), Y(1) for everyone; heterogeneous effects; an instrument; an unmeasured confounder with proxies | 35–37, 49, 62 |
| Policies | a staggered town-level rollout; a scholarship at a score cutoff; a dynamic treatment regime | 37, 62 |
| Lifetimes | Weibull hazards with covariates and frailty; censoring | 40 |
| Environment | a Matérn pollution field; 300 stations of daily readings | 39 |
| Time | daily series with ARMA, seasonality and change points; random-walk pairs | 17, 38, 58 |
| Surveys | response propensities correlated with income and opinion | 18, 41 |
| Missingness | MCAR, MAR and MNAR masks with known mechanisms | 41 |
| Errors | data-entry contamination; measurement error | 12, 23, 30, 41 |
| Genome | 10,000 markers in linkage blocks; 20 causal | 32, 33, 52, 56 |
| Expression | 5,000 "genes", 100 with real differences | 33, 56 |
| Factory | serial-numbered production; a process with drift | 9, 58 |
| Shifted worlds | a second region with covariate and label shift | 34, 57, 60 |
| Private records | the census microdata for the privacy chapters | 63 |

Sampling designs are `world.sample(n, design=...)`: simple random, stratified, cluster, PPS, quota, self-selected,
and adaptive (bandit).

## 3. The Coverage Board

`explainer/stats/board.py`. Each row is `{part, method, setting, nominal, coverage, mc_band, mean_width, verdict}`.

**The protocol.**

- R = 10,000 seeded replications from the World by default.
- Verdicts, within ±3 MC standard errors of nominal (≈ ±0.65% at R = 10,000): **kept** if inside the band, **broken**
  below, **conservative** above. For tests, the size is compared with 5%.
- Width or power is shown alongside.
- Each part writes `.cache/statsN/board.json`. Part 65 shows the whole Board.

**Planned rows.** The verdicts are expectations from the literature; the narration states the measured verdict,
whatever it is.

| Part | Rows |
|---|---|
| 8 | z with known σ; z with s at n = 5; t at n = 5; t on skewed incomes at n = 20 and 500; the F-test for variances under non-normality |
| 10 | Student vs Welch; a running t-test with peeking (size) |
| 11 | binomial at p = 0.05, n = 50: Wald, Wilson, Agresti–Coull, Clopper–Pearson, Jeffreys |
| 12 | classical vs HC3 under heteroskedasticity |
| 13 | randomization test (size); a split plot analyzed as a CRD |
| 14 | logistic Wald vs LR at small n; Poisson SE under overdispersion |
| 15 | credible intervals at fixed θ: the true prior vs a wrong prior |
| 16 | percentile vs BCa at n = 15 on skewed data; the bootstrap for a maximum; t vs Wilcoxon under contamination |
| 17 | the iid CI for an autocorrelated mean vs HAC; the t-test in a spurious regression |
| 18 | a 1,000-person SRS vs a self-selected half of the World |
| 22 | Wald vs profile for a rate; the model-based vs sandwich SE under misspecification |
| 23 | iid vs cluster-robust; few clusters with CR vs the wild cluster bootstrap; the naive slope under errors in variables |
| 24 | quasi-Poisson and sandwich vs naive; GEE with an exchangeable vs independence working model |
| 25 | DerSimonian–Laird vs Hartung–Knapp with 5 studies; Satterthwaite fixed-effect CIs |
| 26 | hierarchical credible intervals on the World's schools |
| 27 | SBC uniformity: NUTS vs mean-field VI |
| 28 | a naive CI after AIC selection vs data splitting |
| 29 | KDE pointwise CI at the MSE-optimal bandwidth vs robust bias-corrected |
| 30 | mean vs Hodges–Lehmann CIs under contamination |
| 31 | Hotelling T² as p/n grows |
| 32 | naive post-lasso vs debiased lasso |
| 33 | realized FDR of BH under independence and dependence; BY; FCR for selected effects |
| 34 | split conformal; unweighted vs weighted conformal under covariate shift; predictions-as-data vs classical vs PPI; forest IJ intervals |
| 35 | the naive difference; difference in means; Neyman's variance; Lin; a cluster trial analyzed per person; the fixed-n test in a sequential trial |
| 36 | outcome regression misspecified; IPW; AIPW under the four Kang–Schafer scenarios; ML plug-in vs DML |
| 37 | 2SLS with a weak instrument vs Anderson–Rubin; TWFE vs Callaway–Sant'Anna; conventional vs robust RD |
| 38 | the Dickey–Fuller test's size with the normal vs the DF table; the cointegration test |
| 39 | kriging intervals with estimated vs true covariance; misspecified smoothness |
| 40 | ignoring censoring; Greenwood plain vs log-log at small n |
| 41 | complete-case under MAR; single vs multiple imputation; MRP on a self-selected sample |
| 46 | Feldman–Cousins vs flip-flopping near a boundary; the Behrens–Fisher tests |
| 47 | bootstrap-t vs percentile (second-order); the Hodges and pre-test estimators at local alternatives |
| 48 | KS with estimated parameters vs the parametric-bootstrap band |
| 49 | plug-in vs one-step vs TMLE in a semiparametric model |
| 52 | the PCA spike's CI near the BBP threshold |
| 53 | nonparametric credible bands for smooth vs rough truths (Szabó, van der Vaart & van Zanten) |
| 56 | naive vs PoSI vs polyhedral vs data-fission intervals after selection |
| 57 | marginal vs group-conditional conformal; the t-interval over a heavy-tailed family (Bahadur–Savage) |
| 58 | Hoeffding vs betting confidence sequences (time-uniform); naive vs adaptively weighted CI after Thompson sampling |
| 59 | the classical logistic LRT at p/n = 0.2 vs the Sur–Candès rescaling |
| 60 | importance-weighted vs unweighted intervals under covariate shift; a label-shift correction |
| 62 | naive vs proximal under unmeasured confounding; a policy-value CI |
| 63 | a naive CI on DP-noised counts vs a DP-aware CI |
| 64 | naive vs clustered error bars for a benchmark; unpaired vs paired model comparisons |

## 4. The Museum

`explainer/stats/museum.py` holds the historical datasets as typed Python data, each with its citation, table or
page, and a provenance note. The policy:

- **Published before 1931, or US government works.** Transcribed into the repo: Graunt, Arbuthnot, Laplace's
  births, Quetelet, Snow, Galton, Weldon/Pearson, Bortkiewicz, Student, Yule, Newcomb, Mendel, Darwin's *Zea mays*,
  Toussoun's Nile, the *Federalist* texts (Gutenberg), NOAA CO₂, NPS geyser records, the Challenger table, NHANES
  (CDC).
- **Modern small tables** (Bliss, Efron–Morris, the eight schools, the law schools, Freireich/Gehan, Berkeley,
  Literary Digest, Card–Krueger means). Transcribed as facts with citation, after checking that this is permissible.
- **Licensed modern datasets** (NSW/LaLonde, Prop 99, the prostate microarray). Downloaded at compute time with a
  checksum. If use is unclear, a World analogue replaces the dataset and the screen says so.
- Every dataset goes into `docs/CREDITS.md`.

## 5. statkit

`explainer/stats/kit/` is a small library written for reading: short functions, docstrings that cite the part and
chapter of their derivation, and numpy/scipy only. Each module has tests against SciPy and, for models, statsmodels
(a test-only dependency).

| Module | Contents | Part |
|---|---|---|
| `random` | a PCG-style generator; inverse CDF, rejection, Box–Muller, Marsaglia–Tsang, alias; the simulation-study harness (seeds, MC error) | 7 |
| `estimate`, `tests`, `intervals` | moments, plug-in, delta method; z/t/Welch/χ²/exact/permutation; the binomial family, Fieller, tolerance | 8–11 |
| `ols` | QR least squares, influence, HC0–HC3, cluster-robust, wild bootstrap, quantile regression (LP) | 12, 23 |
| `design` | ANOVA, Yates, fractional factorials, D-optimal designs | 13 |
| `glm` | IRLS, deviance, quasi-likelihood, Firth, GEE, ordinal | 14, 24 |
| `bayes`, `ppl` | conjugate and grid posteriors; a tiny probabilistic programming language (autodiff log densities, NUTS, R̂/ESS, SBC) | 15, 26, 27 |
| `bootstrap`, `ranks` | percentile/basic/t/BCa, block, m-out-of-n; exact Wilcoxon, Mann–Whitney, Hodges–Lehmann | 16 |
| `ts` | ARMA likelihood, Yule–Walker, forecasting, Holt–Winters; spectra, Dickey–Fuller, GARCH, Kalman/RTS | 17, 38 |
| `survey` | HT, stratified and cluster SEs, raking, GREG | 18 |
| `learn` | CV, k-NN, naive Bayes, logistic classifier, CART | 19 |
| `optim` | Newton, scoring, MM, coordinate descent, proximal gradient, LP (simplex for small problems), ADMM | 21 |
| `mle` | profile likelihood, EM, observed information, sandwich | 22 |
| `mixed`, `shrink` | profiled REML, BLUPs, Laplace GLMM; James–Stein, SURE, empirical Bayes, NPMLE, Tweedie | 25 |
| `select` | AIC/BIC/Cp, CV/GCV, PSIS-LOO, stacking | 28 |
| `smooth` | KDE (three bandwidth selectors), local linear, Reinsch spline, PAVA, wavelet thresholding | 29 |
| `robust` | Huber/biweight, FAST-LTS, MCD, median-of-means | 30 |
| `multi` | Hotelling, PCA, FA, CCA, MDS, GMM-EM, graphical lasso | 31 |
| `sparse` | lasso/elastic-net paths, debiased lasso | 32 |
| `multiple` | Holm, Hochberg, BH, BY, Storey, local fdr, knockoffs | 33 |
| `conformal`, `ppi` | split, jackknife+, CV+, CQR, weighted, ACI, Mondrian, conformal p-values; PPI/PPI++ | 34, 57 |
| `causal` | Neyman, Lin, IPW, AIPW, cross-fitted DML, causal forest; proximal, policy learning | 35, 36, 62 |
| `quasi` | 2SLS, Anderson–Rubin, robust RD, Callaway–Sant'Anna, synthetic control | 37 |
| `spatial`, `survival`, `mi` | variograms, kriging, Vecchia, Ripley's K; KM, NA, log-rank, Cox, Aalen–Johansen; chained imputation with Rubin's rules | 39–41 |
| `empirical` | ECDF processes, bracketing/VC calculators, multiplier bootstrap | 48 |
| `semipar` | influence-function calculus, one-step, TMLE | 49 |
| `gsm` | the Gaussian sequence model: Pinsker, blockwise James–Stein, Lepski | 50 |
| `hdp` | random-matrix norms, matrix Bernstein checks, Gaussian widths | 51 |
| `bnp` | DP mixtures (CRP Gibbs), GP posteriors, spike-and-slab | 53 |
| `slt` | empirical Rademacher complexity, margin bounds | 54 |
| `selective` | polyhedral intervals, data fission/thinning | 56 |
| `sequential` | SPRT, spending functions, mixture and betting CSs, mSPRT, e-BH, CUSUM, off-policy IPW/DR | 58 |
| `amp` | AMP with state evolution | 59 |
| `shift` | filtering for robust means, label-shift estimation, DRO | 60 |
| `ot` | 1D OT, Sinkhorn, OT ranks, barycenters | 61 |
| `privacy` | Laplace/Gaussian mechanisms, accountants, private means and CIs | 63 |
| `evals` | clustered and paired eval errors, Bradley–Terry with sandwich SEs | 64 |

## 6. Part by part

Lengths are targets. Each part's chapter list is locked at its frontier sweep; content decides. Each heading gives
the stage and the prerequisites.

### Stage I · Bachelor's: Foundations (years 1–2)

The stage opens with data rather than axioms, and builds the language of chance at calculus level. It ends able to
estimate, test and simulate. The matrices of Part 4 and the simulation harness of Part 7 are tools for the rest of
the series.

#### Part 1 · The Shape of Data (~52 min; the pilot)
*Prerequisites:* none. *Question:* what can you know about what you cannot see?
*Story:* Graunt turns a list of deaths into knowledge of the living, and we build a world whose truth we know. Then
we find that every summary jiggles from sample to sample. A statistic is random, so we need the language of chance
(→ Part 2).

0. **Hook: the Bills of Mortality (1662).** Graunt's tables of christenings and burials, the plague years, the male
   surplus at birth (tested in Part 10); his estimate of London's size; Halley's life table (1693).
1. **Populations and samples.** Parameters vs statistics; the series' question; the "95% promise" and the empty
   Coverage Board; the Transcript and the degree ahead.
2. **Building the World.** Its design (§2), and why a known truth makes honest teaching possible; the `simulated`
   tag; a tour of the map, families, incomes, schools and clinics.
3. **Pictures first.** Dot plots and histograms; bin width as a choice (Sturges 1926, Scott 1979, Freedman–Diaconis
   1981; derived in Part 29).
4. **The centre as an optimization.**
   - The mean minimizes Σ(xᵢ − c)². The median minimizes Σ|xᵢ − c|: the subgradient as a tug-of-war. The mode is the
     limit of 0–1 loss, the midrange the L∞ centre; the Lᵖ centre sliding as p goes from 1 to ∞.
   - The Fréchet mean on a circle (clock times).
5. **Spread.** Σ(xᵢ − c)² = Σ(xᵢ − x̄)² + n(x̄ − c)² as Pythagoras in Rⁿ (`NSpace`); SD, MAD, IQR; Chebyshev's
   guarantee (Part 6).
6. **Quantiles and the ECDF.** The staircase and its generalized inverse; Tukey's five numbers and box plots;
   outliers.
7. **Shape.** Skewness; kurtosis as tails (Westfall 2014); Pareto's income law (1896) in the World; log scales; mean
   vs median income.
8. **The QQ plot** (Wilk & Gnanadesikan 1968). Why a straight line means the same family up to location and scale;
   reading the curvature; Quetelet's 5,738 Scottish chests (1846).
9. **Transformations.** Log, square root, Box–Cox (1964); variance stabilization (Part 6's delta method).
10. **Two variables.** Covariance; correlation as the cosine between centred vectors; |r| ≤ 1 by Cauchy–Schwarz;
    correlation is not slope; restriction of range.
11. **Same statistics, different pictures.** Anscombe (1973). *Built:* the Matejka–Fitzmaurice (2017) annealing morph,
    holding means, SDs and r to two decimals while a cloud becomes the word STATS.
12. **Traps of aggregation.** Simpson's paradox in the World (resolved in Part 36); the ecological fallacy (Robinson
    1950).
13. **Graphical integrity.** Playfair (1786), Nightingale (1858), Minard (1869); Cleveland & McGill (1984); misleading
    axes.
14. **The sample is random.** Twenty samples of 100; the `SamplingMachine`'s first run.
15. **Outro.** The five stages, problems, references.

*Built:* the World (v1); the morph engine. *Data:* Graunt; Quetelet; Anscombe.

#### Part 2 · Chance, Counted (~55)
*Prerequisites:* 1. *Question:* how do you reason exactly about what might happen?
*Story:* an interrupted dice game forces the invention of expected value. Paradoxes force the invention of sample
spaces. A courtroom shows what a transposed conditional costs. Random variables arrive with distributions whose
shapes need naming (→ Part 3).

0. **Hook: the problem of points (1654).** A game to three, interrupted at 2–1; Fermat's enumeration vs Pascal's
   recursion.
1. **Before axioms.** Cardano; Galileo's three dice (27 ways vs 25); Huygens (1657).
2. **Counting.** Permutations, combinations, multinomials, stars and bars.
3. **Bertrand's paradox (1889).** Three random chords: 1/3, 1/2, 1/4 (simulated). "Random" needs a measure.
4. **Kolmogorov's axioms (1933).**
   - Events as a σ-algebra, previewed (the full theory is Part 43; *Analysis, Built* Part 5).
   - Consequences: inclusion–exclusion; derangements → 1/e; continuity; the union bound.
5. **Conditioning.** Renormalizing a slice; the multiplication rule; total probability as a tree.
6. **Bayes' theorem.** The odds form; the World's screening test; natural frequencies.
7. **The prosecutor's fallacy.** The Sally Clark case (1999; RSS statement 2001; quashed 2003), told with care from
   the published record.
8. **Monty Hall** (Selvin 1975; vos Savant 1990). The host's protocol; variants enumerated exactly.
9. **Independence.** Pairwise but not mutual (Bernstein's tetrahedron); conditional independence.
10. **Random variables.** Functions on Ω; CDFs; discrete, continuous, mixed and singular (the Cantor distribution).
11. **Expectation.** The layer-cake formula; LOTUS; linearity; indicators (fixed points, birthdays, the coupon
    collector's nH_n).
12. **Variance and moments.** Var of sums; St. Petersburg (D. Bernoulli 1738) and log utility.
13. **Generating functions, first look.** pgfs of dice sums; convolution as polynomial multiplication.
14. **What probability means.** Frequency, logic and belief (von Mises, Keynes, Ramsey, de Finetti); the Dutch book
    (de Finetti 1937); Cox's theorem (1946).
15. **Outro.**

*Built:* an exact probability engine on finite spaces (Python fractions), checked against simulation.

#### Part 3 · The Family of Distributions (~55)
*Prerequisites:* 2. *Question:* why do the same few shapes keep appearing?
*Story:* deaths by horse kick follow a formula, and every distribution turns out to be a relative of a few others.
The family tree is assembled arrow by arrow. One variable at a time is not enough, and many variables need matrices
(→ Part 4).

0. **Hook: Bortkiewicz (1898).** 200 corps-years: 109, 65, 22, 3, 1 deaths against Poisson(0.61): 108.7, 66.3, 20.2,
   4.1, 0.6.
1. **Bernoulli → binomial.** Lattice paths; mean and variance by indicators.
2. **The law of rare events.** Binomial(n, λ/n) → Poisson, derived; Le Cam's inequality.
3. **Waiting.** Geometric and negative binomial; memorylessness; the negative binomial as gamma–Poisson.
4. **Without replacement.** The hypergeometric; capture–recapture on the World's lake.
5. **Continuous time.** The Poisson process; exponential and gamma waits; the inspection paradox (computed).
6. **The normal, three ways.** de Moivre (1733) via Stirling; Gauss (1809) from "the mean is best"; Herschel–Maxwell
   from rotation invariance; the Gaussian integral in polar coordinates.
7. **Transformations.** The CDF method; Jacobians in 1D and 2D; Box–Muller; the log-normal as a multiplicative CLT.
8. **The sampling family.** χ² (Helmert 1876), t, F; Cauchy as t₁ and as a lighthouse beam; Beta and gamma
   relations.
9. **Order statistics.** The k-th's density; uniform order statistics are Beta; the maximum (Part 9's tanks); Rényi's
   representation.
10. **Heavy tails.** Pareto and Zipf; log–log plots and their misuse (Clauset, Shalizi & Newman 2009).
11. **Generating functions.** MGFs and characteristic functions; moments from derivatives; uniqueness (proved in Part
    43); sums by products.
12. **Mixtures and hierarchies.** Beta-binomial, gamma–Poisson, scale mixtures → t.
13. **Exponential families, first look.** h(x) exp(ηT(x) − A(η)); A′(η) is the mean.
14. **The family tree** (Leemis & McQueston 2008), every arrow derived lit.
15. **Outro.**

*Built:* the family-tree explorer (each arrow a live transformation).

#### Part 4 · Matrices for Statistics (~52)
*Prerequisites:* a first course in linear algebra, or *AI, Built* Part 3. *Question:* what matrix facts does
statistics run on?
*Story:* a projection's eigenvalues can only be 0 and 1, and from that fact come degrees of freedom, χ², regression
and ANOVA. This part is the toolkit every later part reaches into. With it, many variables at once become a single
object (→ Part 5).

0. **Hook: the hat matrix.** H = X(XᵀX)⁻¹Xᵀ has eigenvalues 0 and 1 only, and that explains n − p.
1. **Vectors as data.** A sample of n as a point in Rⁿ; centring as projection away from 1 (`NSpace`).
2. **Projections.** Idempotent and symmetric; orthogonal complements; Gram–Schmidt and QR; P = A(AᵀA)⁻¹Aᵀ derived.
3. **Trace tricks.** tr(AB) = tr(BA); E[xᵀAx] = tr(AΣ) + μᵀAμ; rank = trace for projections.
4. **The spectral theorem** (sketched proof); quadratic forms as ellipsoids; the Rayleigh quotient.
5. **Positive semidefinite matrices.** The Loewner order; Cholesky; square roots; covariance matrices are PSD.
6. **The SVD.** From AᵀA; geometry (rotate, stretch, rotate); low-rank approximation (Eckart–Young).
7. **Generalized inverses.** The Moore–Penrose pseudoinverse; minimum-norm solutions.
8. **Block matrices.** The Schur complement; block inverses; determinants; Woodbury (Sherman–Morrison–Woodbury) and
   why it makes updating cheap.
9. **Kronecker products and vec.** vec(ABC) = (Cᵀ ⊗ A)vec(B); the structured covariances of Parts 25 and 39.
10. **Matrix calculus.** ∂(aᵀx), ∂(xᵀAx), ∂ log det Σ = Σ⁻¹, ∂ tr; the Gaussian MLE in one line.
11. **Quadratic forms in normal vectors.** xᵀAx ~ χ² iff A is a projection (for x ~ N(0, I)); Cochran's theorem
    previewed (Part 8).
12. **Conditioning and numerics.** Condition numbers; why never to invert XᵀX; floating point.
13. **Outro.**

*Built:* a projection lab (rotate Rⁿ for n = 3, watch idempotence, eigenvalues and residuals).
*Books:* Harville; Searle; Magnus & Neudecker; Seber *A Matrix Handbook for Statisticians*.

#### Part 5 · Many Variables at Once (~55)
*Prerequisites:* 3, 4. *Question:* what does knowing one thing tell you about another?
*Story:* Galton finds ellipses in a table of heights and discovers regression to the mean. Conditional expectation
is a projection, the Gaussian's conditionals are linear, and exchangeability prepares the ground for Bayes. Averages
of many variables come next (→ Part 6).

0. **Hook: Galton (1886).** 928 children of 205 families; the smoothed table's ellipses; "regression towards
   mediocrity".
1. **Joint, marginal, conditional.** Slicing a 3D density and renormalizing the slice.
2. **Dependence.** Uncorrelated is not independent; covariance matrices are PSD (Part 4).
3. **Conditional expectation as best predictor.** Minimizing mean squared error; the tower property; projection in L²
   (made rigorous in Part 44).
4. **Eve's law.** Var Y = E Var(Y | X) + Var E(Y | X) as Pythagoras; R².
5. **The multivariate normal.** An affine image of iid normals; ellipsoids from the spectral theorem; marginals;
   uncorrelated ⇒ independent only when jointly normal.
6. **Conditioning a Gaussian.** The Schur complement (Part 4); linear conditional means: regression is born.
7. **Regression to the mean.** The slope ρσ_y/σ_x; Galton recomputed; the sophomore slump; Kahneman's flight
   instructors.
8. **Three lines through one ellipse.** Y on X, X on Y, the major axis.
9. **Change of variables in many dimensions.** Jacobians; convolution; the Gaussian in polar coordinates.
10. **Latent variables.** Mixture surfaces; marginalizing a class.
11. **Copulas.** Sklar (1959); Gaussian vs Clayton vs Gumbel tails; the Gaussian copula and 2008 (Li 2000).
12. **Exchangeability.** Pólya's urn → Beta; de Finetti (1931) (proved in Part 44); the finite version.
13. **Measuring dependence.** Pearson, Spearman, Kendall, mutual information, distance correlation (Székely, Rizzo &
    Bakirov 2007), on a gallery of shapes.
14. **The simplex.** Multinomial and Dirichlet.
15. **Outro.**

*Built:* the Gaussian slicer; a Pólya urn machine. *Data:* Galton (Hanley 2004 transcription).

#### Part 6 · The Laws of Averages (~55)
*Prerequisites:* 5. *Question:* why does averaging work, how fast, and when does it fail?
*Story:* 787 guesses at an ox's weight land within 1% of the truth. We prove why at calculus level, test the folklore
"n ≥ 30", break the CLT with heavy tails and meet the law of maxima. The stronger forms wait for Part 43. To use
these laws we need randomness on demand (→ Part 7).

0. **Hook: Galton's ox (1907).** 787 tickets; median 1,207 lb against 1,198 lb.
1. **Inequalities.** Markov by area; Chebyshev; Jensen by chords.
2. **The weak law.** Chebyshev's proof; Bernoulli's golden theorem (1713) and his 25,550 trials vs modern bounds.
3. **Convergence, informally.** In probability vs in distribution; why "almost surely" needs Part 43.
4. **The CLT, seen.** Convolution powers of a lopsided law; *Built:* the Galton board.
5. **The CLT, proved by MGFs.** Taylor expansion of log M(t/√n); the limit e^{t²/2}; what the proof assumed (an MGF),
   flagged on the upgrade card for Part 43.
6. **Using it.** The normal approximation and continuity correction; the de Moivre–Laplace theorem.
7. **"n ≥ 30", tested.** The CLT's speed for skewed incomes, measured; Berry–Esseen, stated.
8. **The delta method.** Derived; variance-stabilizing transforms (Part 1) explained.
9. **Slutsky and continuous mapping**, stated and used.
10. **When averages fail.** Cauchy running means never settle (computed); stable laws, previewed.
11. **Concentration, first look.** Hoeffding's inequality, stated and checked against simulation.
12. **Maxima.** The three extreme-value families; return levels; the 1953 flood and the Delta Works (van Dantzig
    1956).
13. **Outro.** The upgrade cards Part 43 will answer.

#### Part 7 · Randomness on Demand: Simulation and Markov Chains (~55)
*Prerequisites:* 3, 6. *Question:* how does a deterministic machine make randomness, and how do you run an honest
simulation?
*Story:* von Neumann warned that arithmetic randomness is a "state of sin", and IBM's RANDU proved him right. We build
a generator, derive samplers, learn to run simulation studies (the method behind every Coverage Board row), and meet
Markov chains, the engine of MCMC. Simulation lets us watch statistics vary from sample to sample (→ Part 8).

0. **Hook: von Neumann (1951) and RANDU.** Points of RANDU falling on 15 planes in 3D (Marsaglia 1968).
1. **Pseudo-random generators.** LCGs (Lehmer 1949); periods; a PCG-style generator built; testing randomness
   (χ², runs, spectral tests).
2. **Inverse CDF.** The probability integral transform, proved; discrete inversion.
3. **Rejection sampling** (von Neumann 1951). Correctness and efficiency 1/M.
4. **Special methods.** Box–Muller; Marsaglia–Tsang gamma; Walker's alias method; the multivariate normal by
   Cholesky.
5. **Monte Carlo integration.** Error σ/√n in any dimension; Buffon's needle (1777).
6. **Simulation studies done right** (Morris, White & Crowther 2019).
   - Aims, data-generating mechanisms, estimands, methods, performance measures.
   - Seeds and independent streams; Monte Carlo standard errors; the Coverage Board protocol (§3) explained.
7. **Variance reduction.** Antithetic and control variates; importance sampling, first look.
8. **Markov chains.** Transition matrices; the chain as a flow of probability mass.
9. **Stationary distributions.** Left eigenvectors; detailed balance; random walks on graphs; PageRank.
10. **Mixing.** Shuffling a deck: the riffle-shuffle curve and its cutoff near seven shuffles (Bayer & Diaconis
    1992), computed.
11. **The Metropolis algorithm, first look.** Sampling a known shape by a walk that accepts or rejects (Part 27 does
    it in full).
12. **Outro.**

*Built:* statkit.random and the simulation-study harness used by every later part.

#### Part 8 · From Sample to Population (~55)
*Prerequisites:* 4, 6, 7. *Question:* how much does an estimate wobble, and how can one sample tell you?
*Story:* a brewer with four barley samples finds that the normal table lies. Fisher sees the answer as geometry in
n dimensions, and the first Coverage Board rows go up, one green and one red. Of the many estimators, which are
good, and how do we build them (→ Part 9)?

0. **Hook: Student (1908).** Gosset's card-deck simulation of 750 samples of 4, redone on 3,000 World residents.
1. **Sampling distributions.** The `SamplingMachine`; standard errors; σ/√n.
2. **The n − 1.** E s² = σ²; residuals live in an (n − 1)-dimensional subspace (Part 4).
3. **Fisher's geometry (1915, 1925).** Spherical symmetry; x̄ ⟂ s² by rotation.
4. **χ² and Cochran (1934).** Squared lengths of projections (Part 4).
5. **Student's t.** Its density derived; Gosset's cards vs the formula.
6. **F.** A ratio of χ²s; comparing variances.
7. **Bias, variance, MSE.** MSE = bias² + variance; the n + 1 divisor beats n − 1 for MSE.
8. **Consistency and plug-in.** T(F̂) for T(F): mean, variance, quantiles, correlation.
9. **Standard errors for nonlinear statistics.** The delta method for ratios; Laplace's estimate of France's
   population (1802).
10. **Finite populations.** The finite-population correction (Part 18).
11. **The Coverage Board opens.** The rows of §3.
12. **Robustness of normal theory.** The t-test is fairly robust; the F-test for variances is not (Box 1953).
13. **Outro.**

*Board rows:* Part 8 in §3. *Data:* Student (1908).

#### Part 9 · Estimation (~55)
*Prerequisites:* 8. *Question:* how do you build a good estimator, and how good can one be?
*Story:* serial numbers on captured tanks beat the spies. The method of moments and maximum likelihood give
estimators; sufficiency and Rao–Blackwell improve them; Cramér–Rao says how good any unbiased one can be, and the
tanks break even that. An estimate is not yet a decision: when is a difference real (→ Part 10)?

0. **Hook: the German tank problem.** Serial numbers vs intelligence estimates vs the post-war records (Ruggles &
   Brodie 1947).
1. **Estimators as recipes.** For the tanks: 2·mean − 1 and the maximum, with their sampling distributions.
2. **The method of moments** (Pearson 1894). Gamma and beta fits.
3. **Maximum likelihood** (Fisher 1912, 1922). Likelihood curves sharpening with n; score equations; invariance.
4. **Examples.** Normal, Poisson, exponential, uniform (the boundary MLE); Newton's method, first look.
5. **Properties.** Bias, MSE, consistency; the MLE's standard error from the curvature (asymptotic normality,
   stated).
6. **Sufficiency (Fisher 1922).** The idea; the factorization theorem in the discrete case.
7. **Rao–Blackwell.** Conditioning never hurts (Jensen); the tank estimator improved live.
8. **The best unbiased estimator.** Completeness, stated; the tank UMVUE m(k + 1)/k − 1 (Part 45 proves it in
   general).
9. **Fisher information.** The score's mean and variance; information as curvature.
10. **Cramér–Rao.** Proof by Cauchy–Schwarz; the tanks beat it (rate 1/n², since the support depends on N).
11. **Comparing estimators.** An MSE board for the tank estimators; robustness to model error, first look.
12. **Outro.**

*Built:* the tank factory game, grading the viewer's estimator.

#### Part 10 · Significance (~55)
*Prerequisites:* 8, 9. *Question:* when is a pattern too strong to be chance?
*Story:* eighty-two years of more boys than girls, and a lady who claims she can taste milk-first tea. Fisher's
p-values and Neyman–Pearson's error rates are two philosophies that became one procedure, and peeking quietly breaks
both. A test says yes or no, but how big is the effect, and how sure are we of its size (→ Part 11)?

0. **Hook: Arbuthnot (1710) and the lady tasting tea (Fisher 1935).** (1/2)⁸² ≈ 2.1 × 10⁻²⁵; 1/70.
1. **Fisher's logic.** Null, statistic, tail probability; Arbuthnot's sign test.
2. **Exact tests by design.** The tea's hypergeometric null; Fisher's exact test; randomization as the source of
   validity.
3. **p-values.** Uniform under H₀ (proved); their distribution under alternatives.
4. **Neyman–Pearson (1933).** Two errors, size and power.
5. **The Neyman–Pearson lemma** for simple hypotheses, proved as a knapsack (Part 46 generalizes).
6. **The likelihood ratio test.** Wilks' theorem, stated; one-sided vs two-sided.
7. **The everyday tests.** z, one- and two-sample t, paired t; Student vs Welch (1947).
8. **Pearson's χ² (1900).** Goodness of fit and independence; Mendel and Fisher's "too good to be true" (1936).
9. **Power and sample size.** n for 80% power; type M and S errors (Gelman & Carlin 2014).
10. **The peeking problem.** Checking after every observation: the false-positive rate climbs (computed). Sequential
    methods come in Parts 35 and 58.
11. **What p-values are not.** p ≠ P(H₀ | data); the dance of the p-values; the ASA statement (2016).
12. **Many tests, first look.** Bonferroni; the dead-salmon problem (Part 33).
13. **Outro.**

*Built:* the permutation machine; statkit.tests. *Data:* Arbuthnot; Mendel.

### Stage II · Bachelor's: Methods (years 3–4)

The workhorse methods of applied statistics: intervals, regression, design, categorical data, Bayes, resampling,
time series, surveys and prediction, each derived and then used on real and World data. The stage ends with a
complete analysis, the BSc capstone.

#### Part 11 · Honest Intervals (~55)
*Prerequisites:* 10. *Question:* what does "95% confident" promise, and which intervals keep it?
*Story:* the textbook interval for a proportion fails in a sawtooth. Neyman's construction repairs it, and the
Coverage Board becomes the series' judge. Next come intervals for relationships between variables (→ Part 12).

0. **Hook.** The Wald interval's exact coverage zigzagging below 95% as n changes (Brown, Cai & DasGupta 2001).
1. **Neyman (1937).** P_θ(θ ∈ C(X)) ≥ 1 − α for all θ; `IntervalRain`.
2. **Pivots.** Normal μ and σ², ratios of variances, exponential rates.
3. **Inverting tests.** Neyman's belt (`BeltConstruction`); the duality.
4. **The binomial family.** Wilson (1927) by inverting the score test; Agresti–Coull; Clopper–Pearson; Jeffreys; exact
   coverage curves.
5. **Likelihood intervals.** Wald vs profile; log-odds; the rule of three.
6. **Discreteness.** Exact coverage impossible; mid-p.
7. **Fieller (1954).** Ratios: bounded, the whole line, or two rays (Part 46 proves this is unavoidable).
8. **Simultaneous intervals.** Bonferroni; Scheffé (1953); the DKW band.
9. **Prediction and tolerance intervals.** Wilks' (1941) order-statistic limits, the ancestor of conformal (Part
   34).
10. **Credible vs confidence.** Where they agree and where they part (Welch 1939).
11. **The Coverage Board, formally.** The protocol of §3; rows from Parts 8–11.
12. **Outro.**

*Built:* statkit.intervals; `board.py` in full.

#### Part 12 · Least Squares (~58)
*Prerequisites:* 4, 11. *Question:* how do you fit a line through noise, and how sure are you of its slope?
*Story:* Gauss finds a lost asteroid and a priority war follows. Least squares is a projection, Gauss–Markov makes it
optimal, and the classical standard errors lie when the noise is uneven. A regression cannot tell cause, so we must
design the data (→ Part 13).

0. **Hook: Ceres (1801).** Piazzi loses it; Gauss predicts its return; Legendre (1805) vs Gauss (1809).
1. **The principle.** Normal equations; why squares (Gauss), and why absolute errors (Boscovich 1757, Laplace).
2. **Geometry.** The column space; H; orthogonal residuals (`NSpace`).
3. **Gauss–Markov.** BLUE, proved.
4. **Normal theory.** β̂'s distribution; t-tests; nested F-tests as Pythagoras; R².
5. **Frisch–Waugh–Lovell (1933).** "Controlling for", concretely; omitted-variable bias.
6. **Interpreting.** Units, dummies, interactions, polynomials and splines; extrapolation.
7. **Bands.** Confidence vs prediction.
8. **Collinearity.** VIFs; the elongated confidence ellipse.
9. **Diagnostics.** Leverage, studentized residuals, Cook's distance (1977); the `InfluenceProbe`.
10. **Heteroskedasticity.** The classical SE lies; White (1980) and HC3 (Board).
11. **Regression to the mean, revisited** (Part 5), and the regression fallacy.
12. **Outro.**

*Built:* statkit.ols (I), checked against statsmodels; the `InfluenceProbe`.

#### Part 13 · Experiments by Design (~58)
*Prerequisites:* 10, 12. *Question:* how should data be collected so that the answer is unambiguous?
*Story:* Fisher arrives at Rothamsted to sift seventy years of wheat records that cannot answer anything, and
invents randomization, blocking and factorial design. ANOVA becomes Pythagoras, and the same ideas run today's A/B
tests. Outcomes are not always normal (→ Part 14).

0. **Hook: Rothamsted (1919).** Broadbalk since 1843; Fisher's *Studies in Crop Variation* (1921).
1. **Three principles.** Replication, randomization, local control; Peirce & Jastrow (1884).
2. **Randomization as inference.** The randomization distribution; balance of hidden covariates (World).
3. **One-way ANOVA.** SST = SSB + SSW as Pythagoras; the F-test; ANOVA as regression.
4. **Contrasts.** Orthogonal contrasts; Tukey's HSD; Scheffé; Dunnett.
5. **Blocking.** Complete blocks; Darwin's *Zea mays* and Fisher's permutation test (1935).
6. **Latin squares** and crossover designs.
7. **Factorials.** 2^k effects as contrasts; Yates (1937); why one-factor-at-a-time misses a ridge.
8. **Fractional factorials.** Aliasing and resolution (half a cube's corners lit); Plackett–Burman.
9. **Response surfaces** (Box & Wilson 1951). *Built:* optimizing the World bakery's hidden recipe.
10. **Split plots.** Two error strata and the classic mistake (Board).
11. **Optimal design, first look.** D-optimality; quadratic regression on [−1, 1] puts 1/3 at −1, 0, 1.
12. **Power and sample size.** Cohen's d; the minimum detectable effect.
13. **Online experiments** (Kohavi, Tang & Xu 2020). CUPED (Deng et al. 2013) as regression adjustment; sample-ratio
    mismatch.
14. **Outro.**

*Built:* a field-trial simulator; statkit.design.

#### Part 14 · Counts and Categories (~55)
*Prerequisites:* 10, 12. *Question:* how do you regress a yes/no or a count, and read a table?
*Story:* the night before Challenger, a chart left out the flights with no damage. Logistic regression on all 23
flights sees the danger at 31°F, and contingency tables hide Simpson's paradox. Probabilities can also describe
beliefs (→ Part 15).

0. **Hook: 27 January 1986.** The teleconference chart; all 23 flights (Dalal, Fowlkes & Hoadley 1989; Tufte 1997).
1. **Why not least squares on 0/1.**
2. **Logistic regression.** Log-odds; odds ratios; latent variables (probit vs logit).
3. **Fitting by maximum likelihood.** Newton steps as weighted regressions (IRLS, intuition; theory in Part 24).
4. **The Challenger fit.** The profile-likelihood interval at 31°F, and the extrapolation caveat.
5. **Poisson regression.** Rates, offsets; Bortkiewicz by corps.
6. **Overdispersion, first look.** When Poisson SEs are too small (Board).
7. **Two-way tables.** χ² and Fisher's exact test; odds ratios and relative risks.
8. **Simpson's paradox.** The Berkeley admissions (Bickel, Hammel & O'Connell 1975), with mosaic plots flipping.
9. **Three-way tables.** Cochran–Mantel–Haenszel (1959).
10. **Case–control studies.** Why logistic slopes survive outcome-dependent sampling; Doll & Hill (1950).
11. **Scoring predictions.** ROC/AUC; calibration; the Brier score.
12. **Outro.**

*Built:* a Challenger dashboard; statkit.glm (I). *Data:* Challenger; Berkeley.

#### Part 15 · First Bayes (~55)
*Prerequisites:* 9, 11. *Question:* what should you believe after seeing the data?
*Story:* a ball rolled on a billiard table becomes the first posterior, and Laplace weighs the evidence that boys
outnumber girls. Conjugacy, priors and credible intervals follow, with a Metropolis walk by hand when the algebra
gives out. What if we assume nothing about the distribution at all (→ Part 16)?

0. **Hook: Bayes's billiard table (1763).** The Beta posterior; Laplace's rule of succession; Laplace's Paris births
   (figures *(verify)*).
1. **The machinery.** Prior × likelihood ∝ posterior (`BayesUpdate`); sequential = batch updating.
2. **Conjugacy.** Beta–binomial, gamma–Poisson, normal–normal (precision weighting derived).
3. **Summaries.** Posterior mean, median and mode; credible intervals; HPD.
4. **Prediction.** Posterior predictive distributions; the beta-binomial.
5. **Priors.** Informative and weakly informative; flat priors and their traps; sensitivity analysis.
6. **The normal model.** Unknown μ and σ² give a t posterior, matching Part 8's t-interval.
7. **Grids.** Computing any one- or two-parameter posterior on a grid.
8. **When grids fail.** A Metropolis walk by hand (Part 7), with trace plots.
9. **Bayes and frequency.** Credible intervals' coverage at fixed θ (Board); when they agree.
10. **Hypotheses, the Bayesian way.** Posterior odds and Bayes factors, first look (Part 26).
11. **Outro.**

*Built:* the billiard table; statkit.bayes (I).

#### Part 16 · Without Assumptions: Resampling and Ranks (~55)
*Prerequisites:* 8, 10, 11. *Question:* can the data stand in for the model?
*Story:* Efron asks for the standard error of a correlation from 15 law schools and answers by resampling. Ranks give
exact tests without distributions. Both have limits, and the German tank breaks the bootstrap. Data in time are not
independent (→ Part 17).

0. **Hook: Efron (1979).** The law-school sample, r = 0.776: what is its SE?
1. **Permutation tests.** Exchangeability under H₀; exact p-values; the permutation machine (Part 10) returns.
2. **The sign test and Wilcoxon's signed rank (1945).** The exact null by generating function.
3. **Mann–Whitney (1947).** U counts pairs; U/(mn) is the AUC.
4. **More rank methods.** Kruskal–Wallis, Spearman, Kendall.
5. **Efficiency, first look.** Wilcoxon loses only 4.5% at the normal and can win under heavy tails (computed; Part 30
   proves it).
6. **The jackknife** (Quenouille 1949; Tukey 1958).
7. **The bootstrap principle.** The real world mirrored by the bootstrap world (`BootstrapResampler`).
8. **Bootstrap intervals.** Percentile, basic, t; BCa, stated (Board).
9. **When it fails.** The uniform maximum: P(θ̂* = θ̂) → 1 − 1/e (the tanks again).
10. **Cross-validation.** Estimating prediction error by holding out (Part 19).
11. **Density estimates, first look.** Kernel smoothing as a sum of bumps (`KernelSum`; Part 29).
12. **Outro.**

*Built:* statkit.bootstrap and statkit.ranks. *Data:* the law-school sample.

#### Part 17 · Time Series (~55)
*Prerequisites:* 7, 12. *Question:* how do you do statistics when each observation remembers the last?
*Story:* Yule finds that marriages in the Church of England "predict" mortality, then invents autoregression to
explain sunspots. ARMA models, Box–Jenkins and forecasting follow. Not every sample is random, and who you ask
matters (→ Part 18).

0. **Hook: Yule (1926, 1927).** C of E marriages vs mortality, r ≈ 0.95; AR(2) for sunspots.
1. **Stationarity and the ACF.** White noise; the effective sample size of an autocorrelated mean (Board).
2. **AR, MA, ARMA.** Causality and invertibility from roots; the unit circle.
3. **Pseudo-cycles.** AR(2) complex roots; Slutsky (1927).
4. **Identification.** ACF/PACF signatures; Box & Jenkins (1970).
5. **Estimation.** Yule–Walker; least squares; Ljung–Box.
6. **Forecasting.** Best linear prediction; widening intervals; MASE.
7. **Trend and seasonality.** Decomposition; STL; Mauna Loa CO₂.
8. **Exponential smoothing.** Holt–Winters.
9. **Spurious regression, first look.** Two random walks "correlate" (Board).
10. **The M-competitions' lesson.** Simple methods and combinations are hard to beat.
11. **Outro.**

*Built:* statkit.ts (I). *Data:* Yule (1926); NOAA CO₂.

#### Part 18 · Who Did You Ask? Sampling and Surveys (~55)
*Prerequisites:* 8, 11. *Question:* how can 1,000 people speak for a nation, and how can 2.4 million fail to?
*Story:* the *Literary Digest*'s 2.4 million ballots lose to Gallup's far smaller sample. Neyman's design-based
inference makes sampling a science, and Meng's identity shows why size cannot buy back bias. Next, learning to
predict (→ Part 19).

0. **Hook: the *Literary Digest* (1936).** About 2.4 million returns predicted Landon; Roosevelt won about 61%.
1. **What went wrong.** Frame and nonresponse bias (Squire 1988), recreated on the World.
2. **Meng's identity (2018).** Error = data defect correlation × √((N − n)/n) × σ, derived; the effective size of a
   huge biased sample (Board).
3. **Design-based inference** (Neyman 1934). Kiær (1895); Bowley.
4. **Simple random sampling.** The finite-population correction derived.
5. **Stratification.** Neyman allocation n_h ∝ N_hS_h, derived; post-stratification.
6. **Clusters and stages.** Kish's design effect; PPS (Hansen & Hurwitz 1943).
7. **Horvitz–Thompson (1952).** Unbiasedness; Basu's elephants (1971).
8. **Ratio and regression estimators.** Laplace (1802) again; GREG.
9. **Weighting.** Raking (Deming & Stephan 1940) animated; nonresponse adjustment.
10. **Polls.** Quota sampling and 1948; the 2016 and 2020 polling errors (AAPOR reviews).
11. **Outro.**

*Built:* the World's polling firm; statkit.survey.

#### Part 19 · Learning from Data (~55)
*Prerequisites:* 12, 14, 16. *Question:* how do you predict well, and know how well you predict?
*Story:* Mosteller and Wallace decide who wrote twelve disputed *Federalist* papers from the rates of words like
"upon". Prediction error, cross-validation, the bias–variance trade-off and the first regularizers turn statistics
toward prediction. Now put it all together (→ Part 20).

0. **Hook: Mosteller & Wallace (1964).** Hamilton or Madison? Word rates as features (texts from Gutenberg).
1. **Prediction error.** Training vs test error; overfitting with polynomial degree.
2. **Bias and variance.** The decomposition, derived for k-NN and linear smoothers.
3. **Cross-validation.** k-fold and LOO; the one-SE rule.
4. **k-nearest neighbours.** The curse of dimensionality, first look.
5. **Naive Bayes vs logistic regression.** Generative vs discriminative (Ng & Jordan 2002).
6. **Trees.** Recursive partitioning (CART); pruning.
7. **Ridge and lasso, first look.** Shrinkage; the diamond (`L1Geometry`); Part 32 goes deep.
8. **Classification metrics.** Confusion matrices, ROC, precision–recall, calibration.
9. **The Federalist decided.** Our classifiers on the disputed papers, with CV error.
10. **Leakage and honest evaluation.**
11. **Outro.**

*Built:* statkit.learn. *Data:* the *Federalist* (Gutenberg).

#### Part 20 · The Analysis (~58; the BSc capstone)
*Prerequisites:* 1–19. *Question:* what does a complete, honest statistical analysis look like, start to finish?
*Story:* a public-health question is answered from a real public survey, every decision made on screen and checked
on the World. It ends with a report, a reproducible pipeline and the BSc on the Transcript. Next, the master's:
optimization first (→ Part 21).

0. **Hook: a question.** For example: how does blood pressure depend on salt and age? Answered from NHANES (CDC,
   public domain; availability *(verify)*, otherwise the World's health survey).
1. **From question to estimand.** What exactly is being estimated, for whom.
2. **The design and its weights** (Part 18). Why survey weights matter here.
3. **Cleaning.** Codes, missing values, implausible values: each decision logged.
4. **Exploration** (Part 1). Distributions, relationships, surprises.
5. **A first model** (Parts 12, 14). Specification choices, written down before looking at results.
6. **Checking it.** Residuals, influence, nonlinearity (splines), interactions.
7. **Uncertainty.** Design-based vs model-based SEs; the bootstrap (Part 16).
8. **Sensitivity.** What changes the answer: covariates, outliers, missing-data handling.
9. **Causal or not?** What this analysis can and cannot say (a preview of Parts 35–37).
10. **The same pipeline on the World**, where the truth is known: did we recover it?
11. **Communicating.** A one-page report and its graphics (Part 1's integrity rules).
12. **Reproducibility and ethics.** Seeds, scripts, data provenance, privacy.
13. **The BSc problem set.** Six problems spanning Stages I–II, solved.
14. **Outro.** The Transcript: the BSc. The master's begins.

*Built:* the capstone pipeline and report.

### Stage III · Master's

The modern toolkit, derived and justified. Each part revisits a BSc topic with an upgrade card where there is one,
then goes further. The stage ends with the comprehensive exam.

#### Part 21 · Optimization for Statistics (~55)
*Prerequisites:* 4, 9, 19. *Question:* how are estimators actually computed, and what does duality reveal about them?
*Story:* in 1939 George Dantzig arrived late to Neyman's class and solved two open problems he took for homework.
One became the generalized Neyman–Pearson lemma, which is linear-programming duality; Dantzig went on to invent the
simplex method. From there to Newton, EM, coordinate descent and proximal methods, the algorithms behind every later
estimator. First of all, likelihood (→ Part 22).

0. **Hook: Dantzig's "homework" (1939).** Dantzig & Wald (1951) on the Neyman–Pearson lemma; the simplex method
   (1947).
1. **Convex sets and functions.** Jensen; first- and second-order conditions; strong convexity.
2. **Lagrange and KKT.** Constrained MLEs; complementary slackness.
3. **Duality.** The dual of least squares and of the lasso; the Neyman–Pearson lemma as an LP.
4. **Linear programming.** Least absolute deviations (Boscovich, Laplace) and quantile regression as LPs; the simplex
   method, drawn.
5. **Newton and Fisher scoring.** Quadratic convergence and when it fails; line search; trust regions.
6. **MM algorithms** (Lange). Majorize–minimize; EM as MM (Part 22); IRLS as MM.
7. **Coordinate descent.** Convergence for separable penalties; the lasso's soft-threshold update.
8. **Proximal methods.** Proximal operators; ISTA and FISTA (Beck & Teboulle 2009), with rates.
9. **ADMM** (Boyd et al. 2011). Splitting; the fused lasso.
10. **Stochastic gradient.** Robbins–Monro (1951); Polyak–Ruppert averaging (asymptotically efficient!).
11. **Optimization and inference.** The curvature at the optimum is the observed information; optimization error vs
    statistical error.
12. **Outro.**

*Built:* statkit.optim.
*Books:* Boyd & Vandenberghe; Lange *Optimization*; Nocedal & Wright.

#### Part 22 · Likelihood in Depth (~58)
*Prerequisites:* 9, 10, 21. *Question:* why does maximum likelihood work, and what happens when the model is wrong?
*Story:* Pearson splits 1,000 crabs into two species by solving a ninth-degree polynomial. Likelihood and EM do it
better; the curvature becomes the standard error, and a misspecified model gets a sandwich. Next, the linear model in
full (→ Part 23).

0. **Hook: Weldon's crabs (1893); Pearson's nonic (1894).**
1. **Upgrade card** (Part 9). Consistency and asymptotic normality, now proved in the regular case.
2. **Consistency (Wald 1949).** KL ≥ 0; the argmax of a random curve.
3. **Asymptotic normality.** Expand the score; CLT plus LLN; √n(θ̂ − θ) → N(0, I⁻¹).
4. **Observed vs expected information** (Efron & Hinkley 1978).
5. **Many parameters.** The information matrix; profile likelihood along the ridge (`LikelihoodLandscape`).
6. **The trinity.** Wald, score and LR on one curve; Hauck–Donner (Board).
7. **Neyman–Scott (1948).** Incidental parameters: σ̂² → σ²/2.
8. **EM** (Dempster, Laird & Rubin 1977). Jensen's lower bound; monotonicity proved; Louis (1982) SEs; the crabs refit.
9. **When likelihood misbehaves.** Unbounded mixture likelihoods; boundary parameters; label switching.
10. **Misspecification** (Huber 1967; White 1982). The KL projection; the sandwich, derived (Board).
11. **Quasi-, composite and pseudo-likelihood** (Besag 1975).
12. **The likelihood principle** (Birnbaum 1962). Binomial vs negative-binomial stopping.
13. **Information geometry, a glimpse.** The Fisher metric; the natural gradient.
14. **Outro.**

*Built:* statkit.mle. *Data:* Weldon/Pearson.

#### Part 23 · The Linear Model in Depth (~58)
*Prerequisites:* 12, 21, 22. *Question:* what does the linear model really estimate, and how far can its standard
errors be trusted?
*Story:* in 1967 Longley showed that the era's regression programs gave wrong answers. The linear model in full
follows: the general linear hypothesis, GLS, standard errors that survive heteroskedasticity, clustering and
misspecification, and the bias of noisy regressors. Next, outcomes that are not normal (→ Part 24).

0. **Hook: Longley (1967).** Ill-conditioned data and wrong digits; QR vs normal equations (computed).
1. **Upgrade card** (Part 12).
2. **The general linear hypothesis.** Cβ = d; the F-test derived; Cochran's theorem (Part 4) in full.
3. **GLS and Aitken (1935).** Feasible GLS; the efficiency of OLS when GLS is right.
4. **Heteroskedasticity theory.** Eicker–Huber–White; HC0–HC3 (MacKinnon & White 1985); leverage and small samples.
5. **Clustering.** The Moulton factor; cluster-robust SEs (Liang & Zeger 1986; Arellano 1987); few clusters and the
   wild cluster bootstrap (Cameron, Gelbach & Miller 2008) (Board).
6. **Models as approximations** (Buja et al. 2019). The best linear predictor; the sandwich as its correct SE.
7. **Errors in variables.** Attenuation derived; Deming regression and total least squares; Hubble (1929).
8. **Quantile regression** (Koenker & Bassett 1978). Check loss, LP (Part 21); asymptotics.
9. **Splines and bases.** Regression splines; knot choice; the bridge to Part 29.
10. **Numerics.** Householder QR, Cholesky, SVD; condition numbers squared.
11. **Influence theory.** DFBETAS; the jackknife as influence (Part 16).
12. **Outro.**

*Built:* statkit.ols (II): wild bootstrap, quantile regression.

#### Part 24 · Generalized Linear Models (~55)
*Prerequisites:* 14, 21, 22. *Question:* how does one theory fit binary, count, positive and ordinal outcomes?
*Story:* Bliss's dying beetles (1935) give the probit and the dose–response curve. Nelder and Wedderburn unify
regression into one family fitted by one algorithm. Groups within groups come next (→ Part 25).

0. **Hook: Bliss (1935).** Beetle mortality at eight doses; probits and the LD50.
1. **Upgrade card** (Part 14).
2. **The exponential dispersion family.** Variance functions; canonical links; Nelder & Wedderburn (1972).
3. **IRLS derived.** Fisher scoring = weighted least squares on a working response.
4. **Deviance.** The saturated model; analysis of deviance; residuals (Dunn & Smyth 1996).
5. **Asymptotics for GLMs.** Wald, score, LR; the dispersion parameter.
6. **Separation** (Albert & Anderson 1984). The likelihood rising forever; Firth (1993).
7. **Quasi-likelihood** (Wedderburn 1974). Only a mean–variance relation; overdispersion (Board).
8. **Counts.** Negative binomial; zero inflation (Lambert 1992); hurdle models.
9. **Log-linear models.** Three-way tables as GLMs; conditional independence as zeros.
10. **Multinomial and ordinal.** Baseline-category logits; proportional odds (McCullagh 1980).
11. **GEE** (Liang & Zeger 1986). Working correlations; marginal vs conditional effects (Board).
12. **Proper scoring rules** (Gneiting & Raftery 2007).
13. **Outro.**

*Built:* statkit.glm (II). *Data:* Bliss (1935).

#### Part 25 · Borrowing Strength: Shrinkage and Mixed Models (~58)
*Prerequisites:* 15, 22, 23. *Question:* how do you estimate many related things at once?
*Story:* Efron and Morris predict eighteen batting averages, and shrinking them toward each other wins. James–Stein,
empirical Bayes, random effects and REML are one idea seen four ways. The prior is now explicit, so we turn fully
Bayesian (→ Part 26).

0. **Hook: Efron & Morris (1975).** 18 hitters after 45 at-bats; James–Stein wins (recomputed).
1. **James–Stein (1961).** The estimator; its risk via Stein's lemma and SURE, derived; positive part; Part 45 proves
   the admissibility theory.
2. **Empirical Bayes** (Robbins 1956; Efron & Morris 1973). James–Stein as estimated normal priors; Tweedie's formula
   and the winner's curse (Efron 2011).
3. **Random effects.** Variance components (Fisher 1918); ICC; design effects.
4. **The linear mixed model.** V = ZGZᵀ + R; GLS; BLUP via Henderson's equations (derived).
5. **ML vs REML** (Patterson & Thompson 1971).
6. **Inference.** Satterthwaite, Kenward–Roger; boundary tests ½χ²₀ + ½χ²₁ (Self & Liang 1987).
7. **Longitudinal data.** Random slopes (Laird & Ware 1982); growth curves; covariance structures.
8. **Crossed and nested effects.** The radon example (Gelman & Hill).
9. **Fixed vs random.** Hausman (1978); Mundlak (1978).
10. **GLMMs.** Laplace and Gauss–Hermite; PQL bias; conditional vs marginal odds ratios.
11. **Small areas.** Fay–Herriot (1979); EBLUP.
12. **Meta-analysis.** DerSimonian–Laird; τ² and I²; Hartung–Knapp (Board).
13. **Item response theory.** Rasch as a GLMM (Part 64).
14. **Outro.**

*Built:* statkit.mixed and statkit.shrink; the World's hospital league table. *Data:* Efron & Morris.

#### Part 26 · Bayesian Data Analysis (~58)
*Prerequisites:* 15, 25. *Question:* how do you build, fit and check a Bayesian model honestly?
*Story:* the eight schools pull Bayesian modelling into focus. Hierarchies, priors that encode real knowledge,
Bernstein–von Mises' truce and Lindley's lasting paradox, then checking and workflow. The integrals need computing
(→ Part 27).

0. **Hook: the eight schools** (Rubin 1981).
1. **Upgrade card** (Part 15).
2. **Hierarchical models.** Exchangeability and de Finetti (Part 5) as the justification; the eight schools' posterior
   over τ on a grid.
3. **Priors.** Jeffreys (1946) from invariance; reference priors (Bernardo 1979); weakly informative (Gelman 2006);
   improper posteriors.
4. **Conjugate families and exponential families** (Diaconis & Ylvisaker 1979).
5. **Bernstein–von Mises, stated and seen.** Posterior and sampling distributions overlap (Part 53 proves it).
6. **Bayes factors** (Jeffreys 1939; Kass & Raftery 1995).
7. **Lindley's paradox (1957).** Computed; the Sellke–Bayarri–Berger bound.
8. **Occam's razor, built in.** The evidence (MacKay 1992).
9. **Decisions.** Expected utility; value of information.
10. **Checking.** Posterior predictive checks (Rubin 1984; Gelman, Meng & Stern 1996); prior predictive checks.
11. **Workflow** (Gelman et al. 2020).
12. **The argument, honestly.** History from Laplace to MCMC (McGrayne 2011); Cox and coherence; where the schools
    differ.
13. **Bayesian nonparametrics, first look.** The Dirichlet process and the Chinese restaurant (Part 53).
14. **Outro.**

*Built:* statkit.bayes (II). *Data:* the eight schools.

#### Part 27 · Bayesian Computation (~60)
*Prerequisites:* 7, 26. *Question:* how do you compute an integral you cannot do, in a hundred dimensions?
*Story:* a random walk at Los Alamos computes the physics of hard disks. Metropolis, Gibbs and Hamiltonian dynamics
become Bayesian statistics' engines. We build a probabilistic programming language, watch NUTS fail in Neal's funnel
and fix it. Any model can now be fitted, so which one should we believe (→ Part 28)?

0. **Hook: Metropolis et al. (1953).**
1. **Importance sampling.** The optimal proposal; ESS; heavy-tailed weights; PSIS.
2. **Metropolis–Hastings.** Detailed balance (Part 7); random-walk proposals; the 0.234 rule.
3. **Gibbs** (Geman & Geman 1984; Gelfand & Smith 1990). Data augmentation; Albert–Chib probit.
4. **Diagnostics.** ESS; R̂ (rank-normalized, Vehtari et al. 2021).
5. **HMC** (Duane et al. 1987; Neal 2011). Leapfrog and symplecticity; the puck on the surface in 3D.
6. **NUTS** (Hoffman & Gelman 2014). U-turns; adaptation; divergences.
7. **Neal's funnel and the eight schools.** Centred vs non-centred.
8. **Built: a tiny probabilistic programming language.** *AI, Built*'s autodiff, NUTS, diagnostics, checked against
   closed-form posteriors.
9. **SMC.** Particle filters; tempering; the evidence.
10. **Variational inference.** The ELBO; CAVI; reverse KL underestimates variance (vs NUTS); ADVI; PSIS diagnostics.
11. **Laplace and INLA.**
12. **Likelihood-free.** ABC; neural posterior estimation; SBC (Talts et al. 2018) (Board).
13. **Exact sampling.** Coupling from the past (Propp & Wilson 1996).
14. **Outro.**

*Built:* statkit.ppl (the part's centrepiece).

#### Part 28 · Which Model? (~55)
*Prerequisites:* 19, 22, 26. *Question:* how do you choose a model without fooling yourself?
*Story:* fifty columns of noise produce a "significant" regression after screening. Optimism is quantified; AIC,
BIC, CV, LOO and WAIC are derived; singular models break BIC; averaging can beat choosing. Curves need more than
parameters (→ Part 29).

0. **Hook: Freedman's paradox (1983).**
1. **Optimism.** 2σ²·df/n (Efron 1986); degrees of freedom via Stein's lemma (Efron 2004).
2. **Cp and AIC** (Mallows 1973; Akaike 1973). AIC as expected KL, derived; TIC; AICc.
3. **BIC** (Schwarz 1978). The Laplace approximation, derived; consistency vs efficiency (Yang 2005).
4. **Cross-validation theory.** LOO and GCV for linear smoothers; what CV estimates (Bates, Hastie & Tibshirani 2024).
5. **Bayesian LOO.** PSIS-LOO and Pareto-k̂; WAIC (Watanabe 2010).
6. **Singular models.** Watanabe's RLCT replacing d/2 (computed on a mixture).
7. **MDL** (Rissanen 1978).
8. **Averaging.** BMA (Hoeting et al. 1999) vs stacking (Yao et al. 2018).
9. **Inference after selection, first look.** The naive CI after AIC (Board); splitting (Part 56).
10. **Subset selection.** Stepwise's sins; best subset by MIO vs the lasso (Hastie, Tibshirani & Tibshirani 2020).
11. **Calibrated forecasts.** PIT; log score and CRPS; Dawid (1984).
12. **Outro.**

*Built:* the model-selection bench; statkit.select.

#### Part 29 · Smoothing (~58)
*Prerequisites:* 16, 23, 25. *Question:* how do you estimate a whole curve, and how much data does it take?
*Story:* does Old Faithful have two humps or three? Kernels, splines and wavelets trade bias for variance at rates we
derive, until dimension defeats them. Part 50 proves the rates are optimal. When a few points are wrong, everything
can be wrong (→ Part 30).

0. **Hook: Old Faithful.** Silverman's (1981) mode test.
1. **Histograms as estimators.** h ∝ n^{−1/3}, derived (completing Part 1).
2. **KDE.** Bias and variance; h ∝ n^{−1/5}; the rate n^{−4/5}; Epanechnikov's kernel by the calculus of variations.
3. **Bandwidths.** Silverman; LSCV; Sheather–Jones.
4. **The curse of dimensionality.** n^{−4/(4+d)}; Silverman's table.
5. **Local polynomials** (Fan & Gijbels 1996). Boundary and design bias; LOESS.
6. **Smoothing splines.** The Reinsch–Schoenberg theorem, derived; the smoother matrix and its eigenbasis.
7. **Choosing λ.** GCV; REML (Part 25: splines as mixed models).
8. **RKHS and the representer theorem** (Kimeldorf & Wahba 1970); kernel ridge; GPs (Part 39).
9. **Wavelets.** Sparsity; VisuShrink's σ√(2 log n); SureShrink.
10. **GAMs** (Hastie & Tibshirani 1990; Wood 2017); backfitting.
11. **Inference for curves.** Bias in pointwise intervals; robust bias correction (Calonico, Cattaneo & Farrell 2018)
    (Board).
12. **Shape constraints.** Isotonic regression and PAVA; Grenander's cube-root rate.
13. **Outro.** Upgrade card for Part 50.

*Built:* statkit.smooth. *Data:* Old Faithful (license checked).

#### Part 30 · Robust Statistics (~55)
*Prerequisites:* 16, 22, 23. *Question:* what survives when the model is wrong?
*Story:* Tukey shows that a little contamination topples the standard deviation. Ranks lose at most 13.6%
efficiency; Huber solves a minimax problem; high-breakdown estimators refuse to be dragged. Next, the geometry of
many variables (→ Part 31).

0. **Hook: Tukey (1960); Newcomb (1882) via Stigler (1977).**
1. **Pitman efficiency.** Wilcoxon vs t: 3/π at the normal and ≥ 0.864 always (Hodges & Lehmann 1956), derived;
   normal scores (Chernoff & Savage 1958).
2. **Hodges–Lehmann** (1963).
3. **Gross-error models and influence functions** (Hampel 1974); the `InfluenceProbe`.
4. **Breakdown** (Hampel 1971; Donoho & Huber 1983).
5. **Huber (1964).** The minimax M-estimator, derived; ψ-functions; IRLS.
6. **Scale.** MAD, Qn, Sn.
7. **Robust regression.** LMS, LTS, S- and MM-estimators.
8. **Robust multivariate.** MCD; masking and swamping.
9. **Heavy-tailed means.** Median-of-means, derived; Catoni.
10. **Contamination on the World** (Board).
11. **Outro.** Upgrade card for Part 60.

*Built:* statkit.robust. *Data:* Newcomb.

#### Part 31 · Multivariate Analysis (~55)
*Prerequisites:* 4, 5, 22. *Question:* what structure hides in many correlated variables?
*Story:* a map of the World's towns is rebuilt from nothing but road distances. From there to the classical
multivariate toolkit, clustering, and graphs of conditional independence. When variables outnumber observations, we
need sparsity (→ Part 32).

0. **Hook: a map from distances** (classical MDS, Torgerson 1952).
1. **The data matrix.** Mahalanobis distance (1936).
2. **Wishart (1928).** Bartlett's decomposition.
3. **Hotelling's T² (1931).** Union–intersection (Roy 1953); MANOVA's four statistics.
4. **PCA** (Pearson 1901; Hotelling 1933). Variance and low rank; biplots; scree plots.
5. **Factor analysis** (Spearman 1904; Thurstone). Rotation and varimax; Heywood cases; FA vs PCA.
6. **CCA** (Hotelling 1936). Principal angles.
7. **Discriminant analysis** (Fisher 1936; Rao 1948). LDA and QDA; the history acknowledged.
8. **Clustering.** k-means as hard EM; Gaussian mixtures by EM (Part 22); choosing k.
9. **Graphical models.** Zeros of Σ⁻¹ as conditional independence; the graphical lasso (Friedman, Hastie & Tibshirani
   2008).
10. **High-dimensional warning.** T² as p/n grows (Board); Part 52.
11. **Outro.**

*Built:* the map from distances; statkit.multi.

#### Part 32 · Sparsity (~58)
*Prerequisites:* 19, 21, 23. *Question:* how can you solve for 1,000 unknowns from 100 equations?
*Story:* Candès recovers a phantom image from far too few measurements, and ℓ1 geometry explains how. The lasso and
its relatives are computed and tuned, and inference after them is repaired. Selecting variables means asking
thousands of questions (→ Part 33).

0. **Hook: Candès's phantom (2004; Candès, Romberg & Tao 2006).**
1. **Upgrade card** (Part 19).
2. **Ridge** (Hoerl & Kennard 1970). SVD shrinkage; ridge as a prior.
3. **From ℓ0 to ℓ1.** ℓq balls morphing in 3D.
4. **The lasso** (Tibshirani 1996). KKT; soft-thresholding; the octahedron (`L1Geometry`).
5. **Computing it.** Coordinate descent (Part 21); LARS and the path.
6. **The penalty zoo.** Elastic net, group, fused, adaptive, SCAD, MCP.
7. **Choosing λ.** CV; stability selection.
8. **Bayesian sparsity.** The Laplace prior's mean is not sparse; the horseshoe.
9. **Compressed sensing.** RIP and null-space properties (stated; proved in Part 51); the phantom (Built).
10. **Inference after the lasso.** Naive (Board); debiased lasso; double selection (Belloni, Chernozhukov & Hansen
    2014).
11. **Matrix completion.** The nuclear norm; SoftImpute.
12. **Outro.** Upgrade cards for Parts 52 and 59.

*Built:* statkit.sparse; the phantom.

#### Part 33 · Thousands of Questions (~58)
*Prerequisites:* 10, 25. *Question:* ask enough questions and chance will answer some. Which answers are real?
*Story:* a dead salmon "responds" to photographs. Benjamini and Hochberg change what error control means, knockoffs
catch false variables, and a simulator shows how forking paths manufacture discoveries. Then the replication
crisis, measured. Can a black box give honest uncertainty (→ Part 34)?

0. **Hook: the dead salmon** (Bennett et al. 2009/2010).
1. **The problem.** The World's 5,000-gene study; the `PValueSea`.
2. **FWER.** Bonferroni, Šidák, Holm via closed testing, Hochberg, Westfall–Young.
3. **FDR** (Benjamini & Hochberg 1995). BH proved under independence; BY under dependence.
4. **Adaptive FDR.** Storey's π₀ and q-values.
5. **Empirical Bayes** (Efron). Local fdr; the empirical null; the prostate data (Singh et al. 2002).
6. **FDR is an average.** The spread of the FDP; dependence (Board).
7. **Knockoffs** (Barber & Candès 2015; Candès et al. 2018). The filter and its coin-flip proof.
8. **The garden of forking paths.** *Built:* the p-hacking simulator (Simmons, Nelson & Simonsohn 2011).
9. **Replication.** Ioannidis (2005) derived; OSC (2015); Camerer et al. (2018).
10. **Publication bias.** Funnels, Egger, p-curve, selection models.
11. **Remedies argued.** Preregistration; α = 0.005; "abandon significance"; the ASA statements.
12. **The false coverage rate** (Benjamini & Yekutieli 2005) (Board).
13. **Outro.** Upgrade card for Part 56.

*Built:* statkit.multiple; the p-hacking simulator.

#### Part 34 · Prediction with Guarantees (~58)
*Prerequisites:* 16, 19, 33. *Question:* can any prediction come with an honest guarantee?
*Story:* Breiman tells statisticians that algorithms have won. Forests and boosting turn out to be estimators,
conformal prediction gives any model finite-sample coverage, and PPI turns ML guesses into valid estimates. But
prediction is not intervention (→ Part 35).

0. **Hook: Breiman (2001), "The Two Cultures"**, and the replies of Cox and Efron.
1. **Explain or predict?** The Rashomon effect; Shmueli (2010).
2. **Forests.** The variance ρσ² + (1 − ρ)σ²/B; consistency (Scornet, Biau & Vert 2015); permutation importance's bias;
   IJ intervals (Wager, Hastie & Efron 2014) (Board).
3. **Boosting as stagewise additive modelling** (Friedman, Hastie & Tibshirani 2000).
4. **What CV estimates**; nested CV.
5. **Calibration.** Reliability; Platt, isotonic, temperature scaling.
6. **Split conformal** (Papadopoulos et al. 2002; Lei et al. 2018). The quantile lemma; coverage in [1 − α, 1 − α + 1/(n
   + 1)] (Board).
7. **Jackknife+ and CV+** (Barber et al. 2021); CQR (Romano, Patterson & Candès 2019).
8. **Under shift.** Weighted conformal (Tibshirani et al. 2019) (Board); adaptive conformal online (Gibbs & Candès
   2021).
9. **Classification sets** (Romano, Sesia & Candès 2020).
10. **Prediction-powered inference** (Angelopoulos et al. 2023); PPI++ (Board).
11. **Interpretation as estimation.** Partial dependence, SHAP, LOCO.
12. **Outro.** Asthma and pneumonia (Caruana et al. 2015); upgrade card for Part 57.

*Built:* statkit.conformal and statkit.ppi.

#### Part 35 · What If? Experiments and Potential Outcomes (~58)
*Prerequisites:* 13, 23. *Question:* what does it mean for one thing to cause another, and why does randomization
let us find out?
*Story:* the 1954 polio trial ran two designs side by side, and only the randomized one told the truth. Potential
outcomes make causation precise, and the World shows both outcomes for every person. Randomization and Neyman
inference, noncompliance, interference, surrogates and sequential trials follow. When you cannot randomize
(→ Part 36)?

0. **Hook: the Salk trial (1954)** (Francis 1955; Meier 1972).
1. **Potential outcomes** (Neyman 1923; Rubin 1974); Holland's fundamental problem (`ScienceTable`, revealed in the
   World).
2. **Estimands and SUTVA.**
3. **Why randomization works.** Selection bias measured (Board).
4. **Fisher's sharp null.** Randomization inference.
5. **Neyman's variance.** The conservative estimator, derived (Board).
6. **Blocking and pairing.**
7. **Adjustment.** Freedman (2008) and Lin (2013) (Board).
8. **Cluster randomization** (Board).
9. **Noncompliance.** Principal strata; LATE (Imbens & Angrist 1994), derived.
10. **Interference.** Exposure mappings; two-stage designs.
11. **Subgroups.** ISIS-2 (1988).
12. **Sequential trials.** Group-sequential boundaries (Pocock 1977; O'Brien–Fleming 1979; Lan–DeMets 1983) as the
    cure for peeking (Board; Part 58 goes further).
13. **Surrogates.** CAST (1989); Prentice (1989).
14. **External validity.** Transporting a trial (Stuart et al. 2011; Dahabreh et al. 2019).
15. **Outro.**

*Built:* the World's clinic; statkit.causal (I).

#### Part 36 · Causes Without Experiments (~60)
*Prerequisites:* 35. *Question:* when you cannot randomize, what can still be learned, and at what cost in
assumptions?
*Story:* LaLonde throws away an experiment's controls and asks econometrics to recover the answer, and it fails.
Graphs say what to adjust for; propensity scores, double robustness and DML do the adjusting; sensitivity analysis
says how wrong we might be. Sometimes nature randomizes for us (→ Part 37).

0. **Hook: LaLonde (1986)**; Dehejia & Wahba (1999); Smith & Todd (2005).
1. **Unconfoundedness and overlap.**
2. **DAGs** (Wright 1921; Pearl 1995). d-separation (`CausalGraph`).
3. **Back door.** The adjustment formula; colliders (Berkson 1946), mediators, M-bias.
4. **Front door and do-calculus.** Pearl's rules; SWIGs.
5. **Simpson resolved** (Part 1).
6. **g-computation** (Robins 1986).
7. **Propensity scores** (Rosenbaum & Rubin 1983). Matching; subclassification (Cochran 1968); balance.
8. **IPW** (Board).
9. **AIPW and double robustness** (Robins, Rotnitzky & Zhao 1994); Kang–Schafer (Board).
10. **DML** (Chernozhukov et al. 2018). Orthogonality and cross-fitting (theory in Part 49) (Board).
11. **CATE.** Meta-learners; causal forests (Wager & Athey 2018), graded against the World's truth.
12. **Sensitivity.** Cornfield (1959); Rosenbaum's Γ; E-values; Cinelli & Hazlett (2020).
13. **Smoking and lung cancer.** Doll & Hill; Fisher (1958); Cornfield; Hill (1965).
14. **Time-varying treatments.** MSMs; target-trial emulation (Hernán & Robins 2016).
15. **LaLonde revisited**, with the role of overlap (recent re-analyses *(verify)*).
16. **Outro.**

*Built:* statkit.causal (II). *Data:* NSW (license checked).

#### Part 37 · Natural Experiments (~60)
*Prerequisites:* 35, 36. *Question:* when the world runs an experiment by accident, how do you read it?
*Story:* two water companies' pipes ran down the same streets, and Snow counted the dead. Instruments, cutoffs and
difference-in-differences each borrow a piece of randomization, and the standard panel regression can get the sign
wrong. Data in time again, in depth (→ Part 38).

0. **Hook: Snow (1855), Table IX.** 315 vs 37 deaths per 10,000 houses.
1. **The credibility revolution.** Leamer (1983); Angrist & Pischke (2010); the 2021 Nobel.
2. **IV.** Wright (1928); 2SLS as two projections; the draft lottery; quarter of birth.
3. **Weak instruments.** Staiger–Stock; Stock–Yogo; tF; Anderson–Rubin (Board).
4. **Many instruments; Mendelian randomization.**
5. **RD** (Thistlethwaite & Campbell 1960). Local linear at the cutoff; robust bias-corrected CIs (Board); *Built:* the
   World's scholarship.
6. **RD validity.** Manipulation tests; fuzzy RD; close elections.
7. **DiD.** The 2×2; Card & Krueger (1994); event studies.
8. **DiD inference.** Placebo laws (Bertrand, Duflo & Mullainathan 2004).
9. **Staggered adoption.** TWFE's negative weights (Goodman-Bacon 2021); TWFE gets the sign wrong on the World;
   Callaway–Sant'Anna, Sun–Abraham, Borusyak–Jaravel–Spiess (Board).
10. **Honest parallel trends** (Rambachan & Roth 2023).
11. **Synthetic control.** Prop 99 (Abadie, Diamond & Hainmueller 2010); placebo inference.
12. **SDID** (Arkhangelsky et al. 2021).
13. **Panel data.** Fixed effects as FWL; Nickell bias.
14. **Bounds** (Manski 1990; Lee 2009).
15. **Outro.**

*Built:* statkit.quasi. *Data:* Snow; Card–Krueger means; Prop 99 (license checked).

#### Part 38 · Time Series in Depth: Spectra, Unit Roots, Volatility and the Hidden State (~58)
*Prerequisites:* 17, 22. *Question:* what changes when memory is long, the variance moves, or the state is hidden?
*Story:* Hurst measures the Nile for a dam and finds memory that lasts centuries. Spectra, unit roots with Brownian
limits, volatility clustering, and Kalman's filter tracking what cannot be seen follow. Next, data in space
(→ Part 39).

0. **Hook: Hurst (1951).** The Nile, R/S, H well above ½; Toussoun's minima (622–1284).
1. **Upgrade card** (Part 17).
2. **Spectra.** Herglotz; the periodogram's inconsistency; Welch and multitaper; the sunspot cycle.
3. **Unit roots.** Dickey–Fuller (1979) and its Brownian limit (Part 44 proves Donsker); KPSS (Board).
4. **Spurious regression and cointegration.** Granger & Newbold (1974); Engle & Granger (1987); Johansen.
5. **Volatility.** ARCH (Engle 1982); GARCH (Bollerslev 1986).
6. **Long memory.** ARFIMA (Granger & Joyeux 1980; Hosking 1981).
7. **State space and Kalman (1960).** Gaussian conditioning (`KalmanEllipses`); the Nile's flow 1871–1970 and its drop
   around 1899.
8. **Smoothing and learning.** RTS; the prediction-error likelihood; EM (Shumway & Stoffer 1982); Apollo.
9. **Nonlinear filtering.** EKF, UKF; particle filters (Part 27); regime switching (Hamilton 1989).
10. **VARs and Granger causality** (Sims 1980; Granger 1969).
11. **Block bootstrap for series** (Künsch 1989).
12. **Forecasting frontier.** Pretrained forecasting models and honest evaluation *(verify current models)*.
13. **Outro.**

*Built:* statkit.ts (II). *Data:* the Nile; Toussoun; Yule's sunspots.

#### Part 39 · Space (~58)
*Prerequisites:* 25, 29. *Question:* how do you predict where nobody measured?
*Story:* a mining engineer estimates gold grades from boreholes. Kriging is the best linear predictor, Matérn says
how smooth the world is, and some parameters cannot be learned no matter how densely you sample. Sparse precision
matrices make it scale. Next, time measured to an event (→ Part 40).

0. **Hook: Krige (1951); Matheron (1963).**
1. **Spatial data.** Tobler (1970); the World's pollution field.
2. **Random fields.** Bochner's theorem.
3. **Variograms.** Nugget, sill, range; robust estimation.
4. **Kriging.** The BLUP derived; ordinary and universal; kriging = GP posterior mean (`FieldSurface`).
5. **Matérn (1960).** Smoothness; Stein (1999); only σ²/ρ^{2ν} is identifiable under infill (Zhang 2004).
6. **Likelihood estimation.** ML and REML; O(n³).
7. **Scaling.** Vecchia and NNGP; *Built:* 100,000 locations.
8. **GMRFs and SPDE** (Lindgren, Rue & Lindström 2011); INLA.
9. **Areal data.** Moran's I; CAR/SAR; BYM disease mapping.
10. **Point processes.** Ripley's K; Cox processes; Snow's map.
11. **Spatial confounding** (Hodges & Reich 2010).
12. **Space–time** (Gneiting 2002).
13. **GPs in ML.** Marginal likelihood; Bayesian optimization; emulators.
14. **Honest prediction** (Board).
15. **Outro.**

*Built:* statkit.spatial.

#### Part 40 · Time to Event (~58)
*Prerequisites:* 22, 24. *Question:* how do you average lifetimes you have not finished watching?
*Story:* a leukemia trial ends with patients still in remission. Kaplan–Meier, Aalen's martingales and Cox's partial
likelihood build the theory, and then come the traps: hazard ratios, immortal time, competing risks. Censoring is one
kind of missing data (→ Part 41).

0. **Hook: Freireich et al. (1963)**; Gehan (1965).
1. **Lifetimes.** S, h, H, S = e^{−H}; Graunt and Halley again; Gompertz.
2. **Censoring and truncation** (Board).
3. **Kaplan–Meier (1958).** Derived; the shrinking risk set (`KMStaircase`); redistribute-to-the-right.
4. **Greenwood (1926).** Log-log intervals (Board).
5. **Nelson–Aalen.**
6. **Counting processes.** The compensator and martingale (Aalen 1978); the full theory in Part 44.
7. **The log-rank test.** O − E over risk sets, derived.
8. **Cox (1972).** The partial likelihood, derived; ties.
9. **Checking Cox.** Schoenfeld residuals; time-varying coefficients.
10. **What hazard ratios mean** (Hernán 2010); RMST.
11. **Immortal time** (Suissa 2008); the Oscar winners.
12. **Parametric and AFT models.**
13. **Competing risks.** Fine–Gray; Aalen–Johansen.
14. **Frailty.** Vaupel, Manton & Stallard (1979); recurrent events.
15. **Prediction.** Concordance; IPCW Brier; survival forests; conformal survival.
16. **Outro.**

*Built:* statkit.survival. *Data:* Freireich/Gehan.

#### Part 41 · What You Didn't See: Missing Data and Measurement Error (~58)
*Prerequisites:* 18, 22, 36. *Question:* data are missing or mismeasured. When does it matter, and what can be done?
*Story:* Wald is shown where returning bombers were hit and says to armour where they were not. Rubin's mechanisms,
EM, multiple imputation, weighting (which is causal inference in disguise), Heckman's selection model and
measurement-error corrections follow. The master's is nearly done (→ Part 42).

0. **Hook: Wald's bombers (1943)** (Mangel & Samaniego 1984).
1. **Mechanisms** (Rubin 1976). MCAR, MAR, MNAR; ignorability, derived; graphical views (Mohan & Pearl 2021).
2. **The easy methods' sins.** Complete cases (Board); mean imputation; LOCF.
3. **Likelihood under MAR.** EM for a normal with holes; FIML.
4. **Multiple imputation** (Rubin 1987). Rubin's rules derived; chained equations; congeniality (Board).
5. **Weighting = causal inference.** IPW and AIPW for missing outcomes.
6. **MNAR.** Heckman (1979) and the inverse Mills ratio; pattern mixtures; tipping points.
7. **MRP** (Gelman & Little 1997). The Xbox poll (Wang et al. 2015); MRP on the World (Board).
8. **Measurement error.** Spearman (1904); regression calibration; SIMEX (Cook & Stefanski 1994).
9. **Misclassification.**
10. **Outro.** Upgrade card for Part 49.

*Built:* statkit.mi.

#### Part 42 · The Comprehensive Exam (~55; the MSc milestone)
*Prerequisites:* 21–41. *Question:* can you do the master's?
*Story:* a client walks in with messy data and a deadline; the comprehensive exam follows. Two consulting cases and
a dozen classic exam problems are solved on screen, and the MSc goes on the Transcript. Then the PhD core: the
rigorous foundations (→ Part 43).

0. **Hook: the client.** A consulting request from the World's ministry of health.
1. **Case 1: a design question.** Sample size, randomization unit, analysis plan, worked through (Parts 13, 35).
2. **Case 2: an observational question.** DAG, adjustment set, estimator, sensitivity, report (Parts 36, 41).
3. **Exam problems**, each posed, paused and solved:
   - an MLE with its asymptotic variance and a sandwich;
   - a GLM's IRLS step;
   - a REML derivation;
   - a posterior for a hierarchical model;
   - MCMC diagnostics;
   - AIC vs BIC;
   - a KDE bandwidth;
   - an influence function;
   - a lasso KKT check;
   - BH by hand;
   - a conformal interval;
   - a Kaplan–Meier curve with Greenwood bands.
4. **Outro.** The Transcript: the MSc. The PhD core begins.

*Built:* the MSc problem bank (every problem with a full solution in the README).

### Stage IV · PhD Core (the qualifying-exam year)

The rigorous foundations: measure-theoretic probability; the theory of estimation, testing and asymptotics;
empirical processes; semiparametric and minimax theory; high-dimensional probability and statistics; Bayesian
asymptotics; learning theory. Every part opens with upgrade cards from Stages I–III and proves what they only
stated. Every condition that matters gets a counterexample. The stage ends with the qualifying exam.

#### Part 43 · Measure-Theoretic Probability (~60)
*Prerequisites:* 6; *Analysis, Built* 1–5. *Question:* what exactly is a random variable, and what do the limit
theorems really say?
*Story:* in 1900 Hilbert asked for axioms of probability (his sixth problem), and Kolmogorov supplied them in 1933,
on top of Lebesgue's measure. The strong law, weak convergence and the CLT in its exact form follow, with Stein's
method showing how fast. Dependence comes next (→ Part 44).

0. **Hook: Hilbert's sixth problem (1900) and the *Grundbegriffe* (1933).** Upgrade cards from Parts 2 and 6.
1. **σ-algebras and measures.** π–λ (Dynkin); Carathéodory's extension (*Analysis, Built* Part 5); why not every set
   is measurable.
2. **Random variables as measurable maps.** Laws as push-forwards; generated σ-algebras as information.
3. **Integration.** Monotone and dominated convergence; Fatou; uniform integrability; the counterexamples.
4. **Independence and products.** Product measures; Kolmogorov's extension theorem; Fubini.
5. **Borel–Cantelli and the 0–1 laws.** Kolmogorov's 0–1 law; Hewitt–Savage.
6. **The strong law.** Kolmogorov's maximal inequality and three-series theorem; Etemadi's proof (1981).
7. **Weak convergence.** The portmanteau theorem; Skorokhod representation; tightness and Prokhorov; Helly.
8. **Characteristic functions.** Inversion; Lévy's continuity theorem, proved; Cramér–Wold.
9. **Lindeberg–Feller.** Proof; Feller's converse; what the MGF proof of Part 6 assumed.
10. **Stein's method** (Stein 1972). The Stein equation; a Berry–Esseen bound with explicit constants (Chen, Goldstein
    & Shao 2011).
11. **Infinitely divisible and stable laws.** Lévy–Khintchine; domains of attraction; the generalized CLT.
12. **Large deviations.** Cramér's theorem (1938); Sanov; the rate as a Legendre transform.
13. **Extremes.** The Fisher–Tippett–Gnedenko theorem, proved via max-stability.
14. **Outro.**

*Built:* a weak-convergence lab (laws converging in Lévy–Prokhorov and Kolmogorov distance, with the rates measured).
*Books:* Durrett; Billingsley; Kallenberg; Chen, Goldstein & Shao.

#### Part 44 · Martingales, Markov Chains and Brownian Motion (~60)
*Prerequisites:* 43. *Question:* what can be proved about randomness that unfolds in time?
*Story:* Markov counts vowels in Pushkin to refute Nekrasov's claim that the law of large numbers needs
independence. Conditional expectation in full, Doob's martingale theorems, Markov chains on general spaces and
Brownian motion as the limit of everything follow. Ville's inequality will rebuild testing in Part 58. Now the theory
of estimation (→ Part 45).

0. **Hook: Markov (1913).** *Eugene Onegin*'s 20,000 letters, recomputed on the original Russian.
1. **Conditional expectation.** Via Radon–Nikodym and as an L² projection; regular conditional distributions and
   disintegration.
2. **Martingales.** Doob decomposition; likelihood ratios under the null; Doob martingales.
3. **Optional stopping.** The theorem and its conditions; gambler's ruin; why doubling fails.
4. **Maximal inequalities.** Doob's Lᵖ; Ville's inequality (1939) (`BettingPaths`).
5. **Convergence.** Upcrossings; uniform integrability; reverse martingales; the SLLN and de Finetti (Part 5) by
   reverse martingales.
6. **Martingale concentration.** Azuma–Hoeffding; McDiarmid; Freedman.
7. **The martingale CLT** (Hall & Heyde 1980; McLeish 1974).
8. **Markov chains on general spaces.** Harris recurrence; drift and minorization (Meyn & Tweedie); geometric
   ergodicity; the MCMC CLT that justifies Part 27's standard errors.
9. **Coupling and mixing.** Doeblin; total variation; spectral gaps; Pólya's recurrence (1921).
10. **Brownian motion.** Lévy–Ciesielski construction; continuity and nowhere-differentiability; quadratic variation
    (cross-reference *Stochastic Calculus, Visualized*).
11. **Donsker's invariance principle**, via Skorokhod embedding; the Dickey–Fuller limit (Part 38) explained.
12. **The LIL** (Khinchin 1924; Hartman–Wintner 1941).
13. **Counting processes.** Compensators; Aalen's martingales; Rebolledo's CLT (the survival theory of Part 40).
14. **Outro.**

*Built:* a coupling and mixing lab.
*Books:* Williams; Durrett; Meyn & Tweedie; Levin, Peres & Wilmer; Hall & Heyde.

#### Part 45 · The Theory of Estimation (~60)
*Prerequisites:* 9, 25, 43. *Question:* what does "best" mean for an estimator, and why is the obvious estimator
inadmissible in three dimensions?
*Story:* in 1956 Charles Stein proved something few believed. Wald's decision theory gives the language;
sufficiency, completeness and equivariance give optimality; Stein's paradox, explained by Brown through the
recurrence of Brownian motion, gives the limits. Next, the same treatment for tests (→ Part 46).

0. **Hook: Stein (1956).** Upgrade cards from Parts 9 and 25.
1. **Decision theory** (Wald 1950). Risk; admissibility; minimax; Bayes rules.
2. **Risk sets.** Convex hulls; Bayes rules as supporting hyperplanes; minimax via least favourable priors.
3. **Complete class theorems.** Wald; the limits of Bayes rules.
4. **Exponential families as convex duality.** A(η) and its Legendre conjugate; mean-value parameters; Fisher
   information as A″; Pitman–Koopman–Darmois.
5. **Sufficiency in general.** Halmos–Savage (1949) factorization; minimal sufficiency; completeness and its
   counterexamples.
6. **Rao–Blackwell and Lehmann–Scheffé**, proved; the tanks' UMVUE; the absurd UMVUE (−1)^X.
7. **Ancillarity and Basu (1955).** Conditionality (Cox 1958).
8. **Information inequalities.** Multiparameter Cramér–Rao; Bhattacharyya bounds; the Chapman–Robbins bound for
   non-regular models.
9. **Equivariance.** Group families; the Pitman estimator as minimum-risk equivariant and as generalized Bayes.
10. **Stein's lemma, SURE, James–Stein**, proved with exact risks.
11. **Why three dimensions.** Brown (1971): admissibility ↔ recurrence (Part 44's Pólya).
12. **Minimaxity and admissibility in the normal-means problem.** Baranchik; proper Bayes minimax estimators
    (Strawderman 1971).
13. **Empirical Bayes theory.** Robbins; Tweedie; NPMLE (Kiefer–Wolfowitz 1956) and its regret (Jiang & Zhang 2009).
14. **Outro.**

*Built:* a risk-set explorer. *Books:* Lehmann & Casella; Berger; Ferguson; Keener; Brown (1986).

#### Part 46 · The Theory of Testing and Confidence (~58)
*Prerequisites:* 10, 11, 45. *Question:* when is a test optimal, and what can an interval honestly promise?
*Story:* Fisher and Neyman fought over comparing two means with unequal variances. Linnik later showed that no
"nice" exact test exists. The Neyman–Pearson theory in full (UMP, UMPU, invariance) follows, then confidence sets,
Fieller-type impossibility and closed testing. Next, large samples (→ Part 47).

0. **Hook: the Behrens–Fisher problem.** Fisher's fiducial answer, Neyman's objection, Welch; Linnik's theorem (1968).
1. **The Neyman–Pearson lemma in general.** Existence (weak-* compactness), necessity, the generalized lemma
   (Dantzig & Wald 1951; Part 21).
2. **MLR and Karlin–Rubin.**
3. **UMPU tests.** Similarity and Neyman structure; exponential families; the t-test's optimality proved.
4. **Invariance.** Maximal invariants; the Hunt–Stein theorem.
5. **The LRT.** Wilks proved under conditions; Chernoff (1954) on boundaries; Self & Liang.
6. **Confidence sets.** Uniformly most accurate sets by inverting UMP tests (`BeltConstruction`); unbiased sets.
7. **Impossibility.** Gleser & Hwang (1987): Fieller-type problems need infinite intervals.
8. **Bounded parameters.** Feldman & Cousins (1998) (Board).
9. **Simultaneous inference.** Scheffé's projections; closed testing (Marcus, Peritz & Gabriel 1976); partitioning.
10. **Conditional inference.** Recognizable subsets (Buehler 1959); Welch's example; ancillary conditioning.
11. **p-values and evidence.** Berger & Sellke (1987); calibration.
12. **Goodness of fit, rigorously.** Pearson's χ² limit; KS with estimated parameters (Part 48).
13. **Outro.**

*Built:* a Neyman-structure visualizer. *Books:* Lehmann & Romano; Shao; Schervish.

#### Part 47 · Asymptotic Statistics (~60)
*Prerequisites:* 22, 43, 45, 46. *Question:* what is the best possible estimator in large samples, and why is "best"
so hard to define?
*Story:* Hodges builds an estimator that beats the MLE at one point. Le Cam shows the price, a bump of risk just
beside it, and proves that every regular model looks locally like one Gaussian observation; Hájek's theorems make the
MLE optimal in a precise sense. The bootstrap's accuracy is explained too. Next, the processes behind it all
(→ Part 48).

0. **Hook: Hodges (1951).** The bump at θ = c/√n, computed.
1. **Stochastic orders and the toolkit.**
2. **M- and Z-estimators** (Huber 1964). Consistency via uniform laws and the argmax theorem; asymptotic normality and
   the sandwich.
3. **Quantiles.** The Bahadur representation (1966).
4. **Influence functions and the functional delta method** (Hampel 1974; Hadamard differentiability).
5. **U-statistics** (Hoeffding 1948). The Hájek projection; degenerate kernels.
6. **Rank statistics.** Hájek's projection; asymptotically efficient rank tests.
7. **LAN** (Le Cam 1960). Log-likelihood ratios converging to Gaussian shifts.
8. **Contiguity.** Le Cam's first and third lemmas; local power.
9. **Hájek's convolution theorem (1970) and the local asymptotic minimax theorem (1972)**; the Hodges bump explained.
10. **Efficiency of tests.** Pitman and Bahadur.
11. **The bootstrap, rigorously.** Consistency via Hadamard differentiability; Edgeworth expansions and second-order
    accuracy of bootstrap-t and BCa (Hall 1992) (Board).
12. **Saddlepoints** (Daniels 1954).
13. **Non-regular models.** The uniform maximum; boundaries; the m-out-of-n bootstrap.
14. **Outro.**

*Built:* the risk-bump explorer. *Books:* van der Vaart; Le Cam & Yang; Lehmann *Elements of Large-Sample Theory*;
Hall.

#### Part 48 · Empirical Processes (~60)
*Prerequisites:* 44, 47. *Question:* when does an average converge uniformly over a whole class of functions, and at
what rate?
*Story:* in 1949 Doob guessed the Kolmogorov–Smirnov limit from the Brownian bridge. Making the guess rigorous took
Donsker, Skorokhod and Dudley, and created a theory that now underlies all of modern statistics: VC classes,
entropy, chaining and Talagrand's inequality. Next, infinite-dimensional nuisance parameters (→ Part 49).

0. **Hook: Doob's heuristic (1949) and Donsker (1952).**
1. **Glivenko–Cantelli classes.** Symmetrization and Rademacher averages.
2. **VC classes** (Vapnik & Chervonenkis 1971). Sauer–Shelah; covering numbers of VC classes.
3. **Entropy and bracketing.** Covering vs bracketing numbers; examples (monotone, Lipschitz, Sobolev balls).
4. **Chaining.** Dudley's entropy integral (drawn as refining nets).
5. **Donsker classes.** The uniform CLT; uniform entropy and bracketing conditions.
6. **Maximal inequalities.** Bernstein-type; Talagrand's concentration (1996) and Bousquet's form.
7. **The functional delta method.** The quantile process; the Kaplan–Meier process (Part 40).
8. **Z-estimators with nuisance parameters.**
9. **Rates of convergence.** The rate theorem; cube-root asymptotics (Kim & Pollard 1990): Grenander and Chernoff's
   distribution (Part 29).
10. **The bootstrap empirical process** (Giné & Zinn 1990); the multiplier bootstrap.
11. **KS with estimated parameters**, done right (Board).
12. **Outro.**

*Built:* statkit.empirical. *Books:* van der Vaart & Wellner; Kosorok; Pollard; Giné & Nickl.

#### Part 49 · Semiparametric Efficiency (~58)
*Prerequisites:* 36, 47, 48. *Question:* how well can you estimate a number when the rest of the model is infinite
dimensional?
*Story:* Stein (1956) asked whether the centre of a symmetric distribution can be estimated as well without knowing
its shape. Bickel (1982) answered yes: knowing nothing can cost nothing. Tangent spaces, efficient influence
functions and their projections then explain double robustness and DML. Next, how well can anyone do at all
(→ Part 50)?

0. **Hook: adaptive estimation** (Stein 1956; Stone 1975; Bickel 1982).
1. **Models and tangent spaces.** Submodels and scores; the tangent space as a subspace of L² (`TangentSpace`).
2. **Pathwise differentiability.** Gradients and the efficient influence function as a projection.
3. **Efficiency bounds.** The convolution theorem in semiparametric models (Part 47).
4. **Worked influence functions.** The mean; the ATE (Hahn 1998); the partially linear model (Robinson 1988); Cox's
   partial likelihood is efficient.
5. **The nuisance tangent space and the efficient score.** Geometry of projections.
6. **Constructing efficient estimators.** One-step; estimating equations; TMLE (van der Laan & Rubin 2006).
7. **Double robustness** as a structural property of the influence function.
8. **DML theory.** Neyman orthogonality; cross-fitting; the product-rate condition n^{−1/4} × n^{−1/4}.
9. **Missing data, semiparametrically** (Robins, Rotnitzky & Zhao 1994; Tsiatis 2006).
10. **Higher-order influence functions** (Robins et al. 2008): beyond root-n.
11. **The World test.** Plug-in vs one-step vs TMLE (Board).
12. **Outro.**

*Built:* statkit.semipar. *Books:* Bickel, Klaassen, Ritov & Wellner; Tsiatis; van der Vaart ch. 25; Kennedy's
review (2022).

#### Part 50 · Minimax Theory: the Limits of Estimation (~58)
*Prerequisites:* 29, 45, 47. *Question:* how well can anyone estimate, with any method?
*Story:* Stone (1980) proved a speed limit for nonparametric estimation. The Gaussian sequence model turns out to
stand for almost every problem; Pinsker finds an exact constant; Le Cam, Fano and Assouad give lower bounds; Lepski
adapts. Some rates achievable in principle seem out of reach for any efficient algorithm. Next, the probability of
high dimensions (→ Part 51).

0. **Hook: Farrell (1972) and Stone (1980).** Upgrade card from Part 29.
1. **The Gaussian sequence model.** Le Cam equivalence with nonparametric regression and density estimation (Brown &
   Low 1996; Nussbaum 1996).
2. **Linear estimators and Pinsker's theorem (1980).** The exact minimax risk over ellipsoids.
3. **Le Cam's two-point method.** TV, Hellinger and KL; a density at a point.
4. **Fano's method.** Packings (`LowerBoundPacking`); Varshamov–Gilbert; sparse vectors and s log(p/s).
5. **Assouad's lemma.** Hypercubes of bumps; Hölder regression.
6. **Upper bounds that match.** Blockwise James–Stein; wavelet thresholding over Besov balls.
7. **Adaptation.** Lepski's method (1990); the price of adaptation for pointwise loss.
8. **Minimax testing** (Ingster). Separation rates; the sparse-mixture detection boundary and higher criticism
   (Donoho & Jin 2004).
9. **Statistical–computational gaps.** Planted clique and sparse PCA (Berthet & Rigollet 2013); low-degree evidence
   (Hopkins 2018).
10. **Outro.**

*Built:* statkit.gsm and a lower-bound workbench. *Books:* Tsybakov; Johnstone; Giné & Nickl; Polyanskiy & Wu.

#### Part 51 · High-Dimensional Probability (~58)
*Prerequisites:* 43, 48. *Question:* what does randomness look like in a thousand dimensions?
*Story:* almost all of a high-dimensional sphere lies near its equator, whichever equator you choose. From that
surprise come concentration of measure, non-asymptotic random matrix theory, chaining and Gordon's inequality,
which together explain why compressed sensing works. Next, statistics with p ≫ n (→ Part 52).

0. **Hook: the sphere's equator** (Lévy).
1. **Sub-Gaussian and sub-exponential variables.** Orlicz norms; Hoeffding and Bernstein, sharp.
2. **High-dimensional geometry.** Thin shells; near-orthogonality; Johnson–Lindenstrauss (cross-reference *AI,
   Built* Part 3).
3. **Concentration of Lipschitz functions.** Gaussian concentration (Tsirelson–Ibragimov–Sudakov); the sphere;
   Talagrand's convex-distance inequality.
4. **Random matrices, non-asymptotically.** ε-nets; the norm of a sub-Gaussian matrix; covariance estimation at rate
   √(p/n).
5. **Matrix concentration.** Matrix Bernstein (Tropp 2012).
6. **Chaining revisited.** Dudley; Sudakov minoration; generic chaining, a glimpse.
7. **Gaussian comparison.** Slepian, Sudakov–Fernique, Gordon.
8. **Gaussian widths and the escape through the mesh.** Exact recovery from random measurements.
9. **Statistical dimension** (Amelunxen, Lotz, McCoy & Tropp 2014): the Donoho–Tanner curve explained.
10. **Outro.**

*Built:* statkit.hdp. *Books:* Vershynin; Boucheron, Lugosi & Massart; Tropp; Wainwright ch. 2–6.

#### Part 52 · High-Dimensional Statistics (~60)
*Prerequisites:* 31, 32, 51. *Question:* what can be estimated, and how fast, when parameters outnumber observations?
*Story:* PCA on pure noise finds "large components". The lasso's oracle inequalities, the primal–dual witness,
low-rank recovery, perturbation theory and random matrix laws give exact answers, including a sharp threshold below
which a signal is invisible. Next, Bayesian theory (→ Part 53).

0. **Hook: noise with structure.** n = 1,000, p = 500: eigenvalues from ≈ 0.09 to ≈ 2.91.
1. **Upgrade card** (Part 32).
2. **The lasso's oracle inequality.** Restricted eigenvalues (Bickel, Ritov & Tsybakov 2009), proved.
3. **Support recovery.** Irrepresentability; the primal–dual witness (Wainwright 2009).
4. **Decomposable regularizers** (Negahban et al. 2012): one theorem for sparse, group and low-rank problems.
5. **Low-rank matrix recovery and completion** (Candès & Recht 2009; Koltchinskii, Lounici & Tsybakov 2011).
6. **Covariance estimation.** Banding and thresholding (Bickel & Levina 2008); Ledoit–Wolf.
7. **Perturbation theory.** Davis–Kahan and Wedin.
8. **Random matrix laws.** Marchenko–Pastur via the Stieltjes transform; Wigner (`SpectrumBulk`).
9. **Spiked models.** The BBP transition (Baik, Ben Arous & Péché 2005); eigenvector overlaps (Paul 2007) (Board).
10. **Tracy–Widom fluctuations**; Johnstone (2001).
11. **Sparse PCA and graphical models.** Consistency; the computational barrier (Part 50).
12. **Inference.** The debiased lasso's theory (Javanmard & Montanari 2014; van de Geer et al. 2014).
13. **Outro.**

*Built:* the random-matrix lab. *Books:* Wainwright; Bühlmann & van de Geer; Bai & Silverstein; Couillet & Liao.

#### Part 53 · Bayesian Asymptotics and Nonparametric Bayes (~58)
*Prerequisites:* 26, 47, 50. *Question:* when does the posterior find the truth, and are credible sets honest?
*Story:* Diaconis and Freedman showed that a reasonable Bayesian can be inconsistent forever. Schwartz's theorem,
contraction rates, Bernstein–von Mises in parametric and semiparametric models, and nonparametric priors follow,
ending with when credible bands cover and when they cannot. Next, learning theory (→ Part 54).

0. **Hook: Diaconis & Freedman (1986).** Upgrade card from Part 26.
1. **Doob's theorem (1949)**, proved (Part 44).
2. **Schwartz's theorem (1965).** KL support plus tests.
3. **Contraction rates** (Ghosal, Ghosh & van der Vaart 2000). Prior mass, entropy and tests.
4. **Bernstein–von Mises**, parametric, via LAN (Le Cam).
5. **Semiparametric BvM** (Castillo & Rousseau 2015) and its failures (Cox 1993; Freedman 1999).
6. **Dirichlet processes and Pólya trees.** Posterior consistency for densities.
7. **Gaussian process priors.** Rates via RKHS and small-ball probabilities (van der Vaart & van Zanten 2008).
8. **Adaptation.** Hierarchical and empirical Bayes priors.
9. **Credible bands.** When they cover; polished tails (Szabó, van der Vaart & van Zanten 2015) (Board).
10. **High-dimensional Bayes.** Spike-and-slab (Castillo, Schmidt-Hieber & van der Vaart 2015); the horseshoe (van der
    Pas, Kleijn & van der Vaart 2014).
11. **Misspecification and generalized posteriors.** Kleijn & van der Vaart (2012); Gibbs posteriors and SafeBayes
    (Grünwald).
12. **Outro.**

*Built:* statkit.bnp. *Books:* Ghosal & van der Vaart; Ghosh & Ramamoorthi; Giné & Nickl ch. 7.

#### Part 54 · Statistical Learning Theory (~56)
*Prerequisites:* 34, 48, 51. *Question:* why does fitting data generalize at all, and why does modern interpolation
seem to break the theory?
*Story:* in Moscow in 1971 Vapnik and Chervonenkis asked when empirical risk converges uniformly. VC and Rademacher
bounds, localization, margins, PAC-Bayes and stability answer them, and then models that interpolate and still
generalize demand new answers (cross-reference *AI, Built* Part 8, here proved). Then the qualifying exam
(→ Part 55).

0. **Hook: Vapnik & Chervonenkis (1971).**
1. **ERM and uniform convergence.**
2. **VC bounds**, from Part 48.
3. **Rademacher complexity.** The contraction lemma; linear and kernel classes.
4. **Localization and fast rates** (Bartlett, Bousquet & Mendelson 2005; Koltchinskii 2006).
5. **Margins** for boosting and SVMs.
6. **PAC-Bayes** (McAllester 1999; Catoni 2007).
7. **Stability** (Bousquet & Elisseeff 2002).
8. **Online learning.** Regret; online-to-batch conversion.
9. **Classification-calibrated surrogates** (Bartlett, Jordan & McAuliffe 2006).
10. **Interpolation.** Benign overfitting (Bartlett et al. 2020); why uniform convergence can fail to explain it
    (Nagarajan & Kolter 2019).
11. **Outro.**

*Built:* statkit.slt. *Books:* Shalev-Shwartz & Ben-David; Bach; Mohri et al.; Wainwright.

#### Part 55 · The Qualifying Exam (~55; the candidacy milestone)
*Prerequisites:* 43–54. *Question:* are you ready to do research?
*Story:* the night before the qualifying exam. Twelve classic problems, each posed, paused and proved on screen with
its picture, and candidacy goes on the Transcript. Then research (→ Part 56).

1. A Borel–Cantelli argument (43).
2. Optional stopping with an unbounded time (44).
3. A UMVUE via completeness, and a case where none exists (45).
4. Admissibility by Blyth's method (45).
5. A UMPU test via Neyman structure (46).
6. LAN and the local power of a test (47).
7. A bracketing bound for a Donsker class (48).
8. The efficient influence function of a functional (49).
9. A Fano lower bound for sparse estimation (50).
10. A matrix Bernstein bound for covariance estimation (51).
11. The lasso oracle inequality (52).
12. A posterior contraction rate (53).

*Outro:* the Transcript, candidacy. *Built:* the PhD problem bank, with full solutions in the README.

### Stage V · PhD Research

The research frontier, roughly the work of the last fifteen years. Each part centres on a few key papers, proves or
sketches their main theorems, reproduces their central experiment on the World, and ends with an **open problems**
card. Everything newer than mid-2026 is verified in its primary source before use. The stage ends with the
dissertation.

#### Part 56 · Inference After Selection (~56)
*Prerequisites:* 33, 46, 52. *Question:* how do you give honest uncertainty about a question chosen by looking at the
data?
*Story:* published effects shrink on replication, the winner's curse at scale (Ioannidis 2008). Simultaneous
coverage over all models (PoSI), conditional selective inference, randomized and fission-based alternatives, and the
theory of knockoffs each answer it, at different prices in power. Next, inference with no model at all (→ Part 57).

0. **Hook: inflated discoveries.** Upgrade card from Part 33.
1. **The selective-inference problem.** Selection events; why marginal intervals fail (Board).
2. **PoSI** (Berk et al. 2013). Simultaneous over all submodels; the √p cost.
3. **Conditional selective inference** (Fithian, Sun & Taylor 2014). The polyhedral lemma and truncated Gaussians (Lee
   et al. 2016), proved.
4. **Randomization and carving** (Tian & Taylor 2018). Trading a little data for a lot of power.
5. **Data fission and thinning** (Leiner et al.; Neufeld et al.). Splitting a single observation.
6. **Knockoff theory.** Fixed-X and model-X; the supermartingale proof; robustness to estimated distributions.
7. **Conformal selection** (Jin & Candès 2023).
8. **Inference on winners** (Andrews, Kitagawa & McCloskey *(verify)*).
9. **Selection in unsupervised problems.** Post-clustering inference (Gao, Bien & Witten 2022).
10. **Open problems.**

*Built:* statkit.selective.

#### Part 57 · Distribution-Free Inference (~56)
*Prerequisites:* 34, 46, 47. *Question:* what can be guaranteed with no assumptions, and what is impossible?
*Story:* Bahadur and Savage proved in 1956 that no honest confidence interval for a mean exists over all
distributions. Conformal inference finds what can be guaranteed, and the impossibility theorems mark the limits:
exchangeability, then beyond it, then conditional guarantees over function classes. Next, inference that lets you
look whenever you like (→ Part 58).

0. **Hook: Bahadur & Savage (1956).** The t-interval's coverage driven to near 0 over a heavy-tailed family (Board).
   Upgrade card from Part 34.
1. **Exchangeability and the quantile lemma**, proved.
2. **Full, split and jackknife+ conformal**; the jackknife+ proof (Barber et al. 2021).
3. **Impossibility.** Conditional coverage (Vovk 2012; Lei & Wasserman 2014; Foygel Barber et al. 2021);
   distribution-free regression functionals (Barber 2020).
4. **Conditional guarantees over function classes** (Gibbs, Cherian & Candès 2023).
5. **Beyond exchangeability.** Weighted conformal; nonexchangeable data (Barber et al. 2023).
6. **Online and adversarial.** Adaptive conformal inference and its guarantees (Gibbs & Candès 2021).
7. **Conformal p-values and outlier testing** (Bates et al. 2023).
8. **Risk control** (Angelopoulos et al.).
9. **Mondrian and group-conditional coverage** (Board).
10. **Open problems.**

*Built:* statkit.conformal (II). *Books:* Angelopoulos, Barber & Bates; Vovk, Gammerman & Shafer.

#### Part 58 · Anytime-Valid Inference and Adaptive Experiments (~60)
*Prerequisites:* 35, 44, 46. *Question:* what if you look at the data every day, and choose what to collect as you go?
*Story:* a Navy captain complains that tests run long after the answer is obvious, and Wald invents the sequential
probability ratio test. Ville's 1939 inequality, through betting, e-values and confidence sequences, rebuilds testing
so that you may look whenever you like. Adaptive experiments need their own inference. Next, high-dimensional
asymptotics (→ Part 59).

0. **Hook: the Statistical Research Group (1943).** Wald's SPRT; Wallis (1980). Upgrade cards from Parts 10 and 35.
1. **The SPRT.** Wald's approximations and identity; optimality (Wald & Wolfowitz 1948).
2. **Group sequential theory.** Spending functions in the Brownian picture; estimation after stopping.
3. **Test martingales and Ville** (Part 44) (`BettingPaths`).
4. **Testing by betting** (Shafer 2021; Shafer & Vovk). e-values; calibrators (Vovk & Wang 2021); merging.
5. **Composite nulls.** Universal inference (Wasserman, Ramdas & Balakrishnan 2020); GROW e-values and reverse
   information projections (Grünwald, de Heide & Koolen 2024).
6. **Confidence sequences.** Mixtures (Robbins 1970); LIL-rate boundaries (Howard et al. 2021); betting CSs
   (Waudby-Smith & Ramdas 2024) (Board).
7. **Game-theoretic probability.** Shafer & Vovk's framework; e-values as evidence.
8. **Multiple testing with e-values.** e-BH (Wang & Ramdas 2022); e-closure *(verify)*.
9. **Change detection.** CUSUM (Page 1954); Lorden's optimality; BOCPD.
10. **Bandits and adaptive designs.** Thompson (1933); Lai–Robbins; adaptive experiments for inference (Kasy &
    Sautmann 2021 *(verify)*).
11. **Inference after adaptivity.** Bias of sample means (Nie et al. 2018); adaptive weighting (Hadad et al. 2021);
    batched bandits (Zhang, Janson & Murphy 2020) (Board).
12. **Off-policy evaluation.** IPW and doubly robust policy values; their variance.
13. **Open problems.**

*Built:* statkit.sequential; the World's A/B platform. *Books:* Wald; Siegmund; Jennison & Turnbull; Ramdas & Wang;
Shafer & Vovk; Lattimore & Szepesvári.

#### Part 59 · High-Dimensional Asymptotics (~58)
*Prerequisites:* 32, 51, 52. *Question:* what happens to classical statistics when p and n grow together?
*Story:* at p/n = 0.2 the textbook likelihood-ratio test for logistic regression is badly miscalibrated (Sur & Candès
2019). The proportional regime replaces old answers with exact new ones, from free probability, AMP and state
evolution, Gordon's comparison and the physicists' replica method. Next, robustness and shift (→ Part 60).

0. **Hook: Sur & Candès (2019).** The inflated MLE and the χ² that is not (Board).
1. **The proportional regime.** Why classical asymptotics fail; what replaces them.
2. **Random matrix tools.** Stieltjes transforms; free convolution (Voiculescu).
3. **Exact ridge and ridgeless risk** (Dobriban & Wager 2018; Hastie, Montanari, Rosset & Tibshirani 2022); double
   descent derived.
4. **M-estimation in high dimensions** (El Karoui et al. 2013; Donoho & Montanari 2016).
5. **AMP and state evolution** (Donoho, Maleki & Montanari 2009; Bayati & Montanari 2011); the Donoho–Tanner curve
   from AMP.
6. **CGMT** (Thrampoulidis, Oymak & Hassibi 2015).
7. **The replica method's predictions** and their proofs for GLMs (Barbier et al. 2019).
8. **Random features and kernels** (Mei & Montanari 2022).
9. **Corrected inference.** Rescaled LRTs; debiased estimators in proportional regimes.
10. **Open problems.**

*Built:* an AMP solver with state evolution.

#### Part 60 · Robustness and Distribution Shift (~56)
*Prerequisites:* 30, 51, 57. *Question:* what can be guaranteed when the data are corrupted, or the future differs from
the past?
*Story:* a carefully rebuilt ImageNet test set cost every model accuracy (Recht et al. 2019, figures *(verify)*).
Tukey's depth, efficient robust estimation in high dimensions, the theory of covariate and label shift,
distributionally robust optimization and invariance make up today's answer. Next, the geometry of distributions
(→ Part 61).

0. **Hook: ImageNetV2.** Upgrade card from Part 30.
1. **Depth** (Tukey 1975). Minimax robust estimation via depth (Chen, Gao & Ren 2018).
2. **Efficient high-dimensional robust estimation.** Filtering (Diakonikolas et al. 2016; Lai, Rao & Vempala 2016);
   sum-of-squares.
3. **List-decodable learning** (Charikar, Steinhardt & Valiant 2017).
4. **Heavy tails in high dimensions.** Median-of-means tournaments (Lugosi & Mendelson 2019).
5. **Covariate shift.** Importance weighting and its variance (Board).
6. **Label shift** (Lipton, Wang & Smola 2018) (Board).
7. **DRO.** f-divergence and Wasserstein balls (Duchi & Namkoong 2021).
8. **Invariance.** ICP; anchor regression (Rothenhäusler et al. 2021).
9. **Transfer learning minimax** (Cai & Wei 2021).
10. **Detecting shift.**
11. **Open problems.**

*Built:* statkit.shift. *Books:* Diakonikolas & Kane.

#### Part 61 · Optimal Transport in Statistics (~58)
*Prerequisites:* 43, 48, 51. *Question:* how far apart are two distributions, when moving mass has a cost?
*Story:* Monge (1781) asked how to move earth at least cost, and Kantorovich (1942) made it linear programming (Part
21). Wasserstein geometry, its curse of dimensionality, entropic smoothing, transport maps, multivariate ranks, and
sampling recast as optimization follow. Next, the frontiers of causal inference (→ Part 62).

0. **Hook: Monge's earthworks (1781); Kantorovich (1942).**
1. **Kantorovich duality.** Couplings; the 1D quantile solution; c-concavity.
2. **Wasserstein distances.** Metrics on laws; geodesics and displacement interpolation (`TransportFlow`).
3. **Empirical rates.** n^{−1/d} (Dudley 1969; Fournier & Guillin 2015; Weed & Bach 2019).
4. **Entropic OT and Sinkhorn** (Cuturi 2013). Convergence; dimension-free sample complexity (Genevay et al. 2019;
   Mena & Niles-Weed 2019).
5. **Estimating transport maps.** Minimax rates (Hütter & Rigollet 2021).
6. **Barycenters and Fréchet means** (Agueh & Carlier 2011).
7. **Multivariate ranks and quantiles.** Center-outward ranks (Chernozhukov et al. 2017; Hallin et al. 2021); rank
   tests (Deb & Sen 2023).
8. **Gradient flows.** Langevin as the Wasserstein gradient flow of KL (Jordan, Kinderlehrer & Otto 1998); sampling as
   optimization (Part 27).
9. **Generative models and OT.** Wasserstein GANs; flow matching (cross-reference *AI, Built* Part 21).
10. **Open problems.**

*Built:* statkit.ot. *Books:* Villani; Peyré & Cuturi; Panaretos & Zemel; Chewi, Niles-Weed & Rigollet.

#### Part 62 · Frontiers of Causal Inference (~58)
*Prerequisites:* 36, 37, 49. *Question:* what can be identified, and estimated, when the textbook assumptions fail?
*Story:* when should HIV treatment start? Emulated trials comparing dynamic regimes (Cain et al. 2011) show that the
questions now go beyond a single treatment. Identification theory, sensitivity models, proximal inference,
interference, policy learning and causal discovery follow. Next, privacy and fairness (→ Part 63).

0. **Hook: when to start** (dynamic regimes; *(verify)* the cited analysis).
1. **Identification theory.** The ID algorithm and its completeness.
2. **Partial identification and sensitivity.** The marginal sensitivity model (Tan 2006; Zhao, Small & Bhattacharya
   2019).
3. **Proximal causal inference** (Miao, Geng & Tchetgen Tchetgen 2018; Tchetgen Tchetgen et al. 2020) (Board).
4. **Interference and networks** (Aronow & Samii 2017; Leung 2022).
5. **Policy learning** (Kitagawa & Tetenov 2018; Athey & Wager 2021) (Board).
6. **Dynamic treatment regimes** (Murphy 2003; Robins 2004); SMART designs.
7. **Causal discovery theory.** Faithfulness and its fragility; identifiability under restrictions; continuous
   optimization (Zheng et al. 2018) and its limits.
8. **Data fusion and transportability** (Bareinboim & Pearl 2016).
9. **Surrogates and long-term effects** (Athey et al. 2019).
10. **Open problems.**

*Built:* statkit.causal (III).

#### Part 63 · Privacy and Fairness (~58)
*Prerequisites:* 41, 46, 50. *Question:* how much does protecting individuals cost the statistics, and what does
fairness require?
*Story:* a governor's medical record re-identified from public data (Sweeney 1997), and most Americans unique by ZIP,
sex and birth date. Differential privacy as a hypothesis-testing guarantee, the minimax cost of privacy and the
2020 Census follow, then fairness criteria and the theorem that they cannot all hold. Last, statistics and AI
(→ Part 64).

0. **Hook: re-identification** (Sweeney 1997, 2000).
1. **Differential privacy** (Dwork, McSherry, Nissim & Smith 2006). Mechanisms; post-processing; composition.
2. **DP as hypothesis testing** (Wasserman & Zhou 2010; Kairouz et al. 2015); Gaussian DP (Dong, Roth & Su 2022).
3. **Accountants.** Rényi DP (Mironov 2017); zCDP (Bun & Steinke 2016).
4. **The cost of privacy.** Local DP minimax rates (Duchi, Jordan & Wainwright 2013); central DP (Cai, Wang & Zhang
   2021).
5. **Private inference.** CIs and tests on privatized data (Board).
6. **The 2020 Census** (Abowd et al. 2022). TopDown, post-processing bias, the redistricting debate.
7. **DP-SGD** and membership inference as a test.
8. **Fairness criteria.** Independence, separation, sufficiency.
9. **Impossibility** (Kleinberg, Mullainathan & Raghavan 2016; Chouldechova 2017); the COMPAS debate.
10. **Multicalibration** (Hébert-Johnson et al. 2018) and its link to conformal (Part 57).
11. **Causal fairness** (Kusner et al. 2017).
12. **Open problems.**

*Built:* statkit.privacy. *Books:* Dwork & Roth; Barocas, Hardt & Narayanan.

#### Part 64 · Statistics in the Age of AI (~58)
*Prerequisites:* 34, 57, 58. *Question:* when machines make the predictions, generate the data and grade each other,
what does honest uncertainty look like?
*Story:* a leaderboard reports 85.2% against 84.7%. Benchmarks are samples, arenas are logistic regressions, labels
come from models, data from generators, and every lesson of the degree applies. Then the dissertation (→ Part 65).

0. **Hook: the leaderboard.**
1. **Benchmarks are samples.** Clustered questions (Miller 2024) (Board).
2. **Paired comparisons.** McNemar; power; leaderboard multiplicity (Board).
3. **Arenas.** Bradley–Terry; sandwich and bootstrap intervals (Chiang et al. 2024); style control *(verify)*.
4. **IRT for benchmarks** (Part 25) *(verify recent work)*.
5. **Adaptive reuse of test sets.** The reusable holdout (Dwork et al. 2015); the Ladder (Blum & Hardt 2015).
6. **Labels from models.** PPI (Part 34); design-based supervised learning (Egami et al. 2023); LLM judges as
   measurement error (Part 41).
7. **Synthetic data and model collapse** (Shumailov et al. 2024). A Gaussian refit to its own samples, derived and
   computed.
8. **Uncertainty for language models.** Calibration (Kadavath et al. 2022); conformal methods for generation *(verify)*.
9. **Watermarks as hypothesis tests** *(verify)*.
10. **Simulation-based inference in science.** Calibration failures (Hermans et al. 2022).
11. **Generative models as density estimators.** Tweedie's formula inside diffusion (Part 25); statistical rates
    *(verify)*.
12. **Causal questions about AI deployments.** Interference; surrogate indices.
13. **Open problems.**

*Built:* statkit.evals.

#### Part 65 · The Dissertation (~60; the PhD milestone and the series finale)
*Prerequisites:* everything. *Question:* how is new statistical knowledge made, and what has the whole degree shown?
*Story:* a mini-dissertation is carried out on screen, from an open problem in Stage V to a conjecture, a theorem
for a special case, a preregistered simulation study and a real-data application. It is reported honestly whatever
the result. Then the full Coverage Board, and back to Graunt.

0. **Hook: back to Graunt.** A ledger became knowledge. Who makes knowledge now, and how?
1. **Choosing a question.** An open problem from Parts 56–64, chosen at writing time (for example, coverage of
   weighted conformal intervals when the weights are estimated).
2. **Reading the literature.** How to read a statistics paper: the theorem, its conditions, the simulation, the gap.
3. **A conjecture.** Stated precisely.
4. **A theorem for a special case.** Proved on screen.
5. **The simulation study.** Preregistered protocol (Part 7; Morris, White & Crowther 2019); run on the World; Monte
   Carlo errors; the result, reported whatever it is.
6. **Real data.** An application from the Museum.
7. **Writing and review.** Structure of a paper; what referees check; reproducibility.
8. **The full Coverage Board.** More than a hundred promises tested across the degree: which were kept, which broken, and the
   lessons in one table.
9. **The Transcript complete.** The degree in one picture; the timeline lit from 1662 to now.
10. **Where to go next.** The reading list beyond the series.

*Built:* the thesis: code, study and a short paper in the part's README.

## 7. Phases

0. **Infrastructure** (one session):
   - The toolchain in this container: Python 3.12 venv, manim, TeX Live with xelatex and CJK, ffmpeg. Manim and TeX
     are not installed here yet.
   - `explainer/stats/`: ACTS/PARTS, `series_map`, timeline, `chapter_card`, payoff, reference, upgrade and
     transcript cards; `style.py`, `viz.py`, `world.py`, `board.py`, `museum.py`, `kit/`.
   - `videos/stats/__init__.py`, `STATS_ZH_GUIDE.md`, `stats_text_zh.json`, `stats_upload.json`.
   - Tools: `stats` added to `BILINGUAL` in `tools/make.py`; `--series stats` for `qa_series.py`, `qa_report.py`,
     `qa_motion.py`, `qa_audio.py` and `package_uploads.py`.
   - `tests/test_stats_world.py` and `tests/test_stats_board.py`; a silent en + zh smoke render.
1. **Pilot: Part 1.** It introduces the World, the Board, the Transcript, the timeline, `SamplingMachine` and
   `NSpace`. Delivered in English and Chinese with previews and contact sheets. **Review with the user**, then lock
   the standard.
2. **Stage by stage**, reviewing with the user at each milestone:
   - Stages I–II (Parts 2–20): **the BSc**, about 18 hours, complete on its own at Part 20.
   - Stage III (Parts 21–42): the MSc.
   - Stage IV (Parts 43–55): the PhD core.
   - Stage V (Parts 56–65): research and the dissertation.

   Each part goes through:
   - the frontier sweep and the Museum's license checks;
   - locking the chapter list;
   - `compute.py` and its statkit module, with tests;
   - English scenes, then the QA gates;
   - Chinese narration and text, then the gates;
   - commit and push.

   Expect one part per one or two long sessions.

## 8. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| 0 | infrastructure: `explainer/stats` (series map, timeline, Transcript, upgrade cards, colours, the World, the Coverage Board, the Museum, the first instruments), tests | — |
| 1 | **written**, English (16 chapters); silent 480p QA renders and contact sheets reviewed; narration with the production voice and the Chinese edition still to do | ≈ 63 min (silent) |
| 2 | **written**, English (16 chapters); the build is `explainer/stats/prob.py` (exact Fractions, tested); `World.screening` added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 74 min (estimate, 144 wpm) |
| 3 | **written**, English (16 chapters); the build is the family-tree explorer (`FamilyTree`, 18 laws, 24 arrows); `World.lake` and the Museum's horse kicks added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 4 | **written**, English (14 chapters, each deepened with statistical applications: ANOVA as projections, leverage, Mahalanobis, FWL, LOO residuals, noncentral χ², numerics); the build is the projection lab (`ProjectionLab`); silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 5 | **written**, English (16 chapters, from Galton's 1886 table to the Dirichlet; deepened with the precision matrix, errors in variables, the conditional median, Bernstein's coins, copula sampling, finite exchangeability, η²); the build is the Gaussian slicer (`GaussianSlicer`) and the Pólya urn machine; the Museum's Galton table and 934 families added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 6 | **written**, English (15 chapters, from Galton's ox to the Delta Works: inequalities, the weak and strong laws, the CLT seen by exact convolution and proved by MGFs, de Moivre–Laplace, the CLT's speed for Pareto-tailed incomes, delta method, Slutsky, Cauchy and stable laws, Hoeffding and large deviations, extreme values and Port Pirie return levels); the build is the Galton board (`GaltonBoard`); the Museum's ox, Bernoulli's urn and Port Pirie added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 55 min narration (estimate) + animation |
| 7 | **written**, English (13 chapters: von Neumann and RANDU's planes, LCGs, PCG and the Mersenne Twister, testing, inversion and the bootstrap's ECDF, rejection and ARS, Box–Muller, Marsaglia–Tsang, the alias table, Monte Carlo and quasi-Monte Carlo, Buffon and Lazzarini, ADEMP simulation studies, variance reduction, Markov's Onegin, PageRank, seven shuffles, Metropolis and Gibbs); the build is `explainer/stats/kit/random.py` (tested against SciPy) and `NSpace.cloud`; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 8 | **written**, English (14 chapters: Student's cards on Macdonell's 3,000 heights, sampling distributions, n − 1 as a dimension, Fisher's rotation, χ² and Cochran, t derived and the sleep data, F, MSE and the n + 1 divisor, plug-in and Fisher's z, Laplace's ratio estimate of France, the FPC, the Coverage Board's first seven rows, Box on robustness); the Museum's crimtab, sleep and Laplace data added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 9 | **written**, English (13 chapters: the German tank problem from Ruggles & Brodie's table, estimators as recipes, Pearson's moments and the gamma fit, Fisher's likelihood with the horse kicks and the tank likelihood, the normal surface and Newton, consistency by KL and the SE from curvature, Neyman–Scott, sufficiency and factorization, Rao–Blackwell turning 2x̄ − 1 into the UMVUE, completeness and the average gap, Fisher information, Cramér–Rao by Cauchy–Schwarz and the tanks' 1/k rate, an MSE board under three worlds); the build is the tank factory game (`explainer/stats/kit/estimation.py`, tested) and `TankFactory`; the Museum's tank figures added; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 71 min narration (estimate) + animation |
| 10 | **written**, English (14 chapters: Arbuthnot's 82 years and the tea, Fisher's logic and which null Arbuthnot rejected, the tea's hypergeometric null and design power, Fisher's exact test, Darwin's 2¹⁵ sign flips, the permutation machine on the World, the uniform p-value, Neyman–Pearson errors, the lemma as a knapsack over 2,048 regions, LRT and Wilks, the Wald/score/LR trinity, Student vs Welch, Pearson's χ² with Mendel and a confounded clinic table, power and types S/M, peeking, what p-values are not, Bonferroni and the dead salmon); the build is the permutation machine (`PermutationMachine`) and `explainer/stats/kit/tests.py` (tested against SciPy); the Museum's Darwin and Mendel data added; five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 60 min narration (estimate) + animation |
| 11 | **written**, English (13 chapters: the Wald sawtooth and BCD's 591/592, Neyman's definition and the interval rain, one-sided bounds and poll planning, pivots and shortest intervals, Neyman's belt and Wald's pinched belt, the binomial family with exact coverage curves, likelihood intervals and the rule of three, discreteness with mid-p, Garwood and the median interval, Fieller and Gleser–Hwang, Bonferroni/Scheffé/DKW, prediction and tolerance with Wilks, credible vs confidence with HPD and Welch 1939, the Board's protocol); the build is `explainer/stats/kit/intervals.py` (tested) and `IntervalRain`; seven Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 12 | **written**, English (13 chapters: Ceres and the Legendre–Gauss dispute, the squares and the normal equations, why squares and Boscovich's LAD, the projection with QR and Pythagoras, Gauss–Markov proved and WLS, normal theory with the ANOVA table, FWL with omitted-variable bias and the clinic's Simpson, dummies/interactions/logs/splines, bands, collinearity, diagnostics with Anscombe and the influence probe, HC3, the regression fallacy with Galton 1886 and Secrist); the build is `explainer/stats/kit/ols.py` (checked against statsmodels) and `InfluenceProbe`; six Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 13 | **written**, English (15 chapters: Rothamsted, Broadbalk and the uniformity trial; the three principles on the field-trial simulator with Peirce & Jastrow; randomization inference over all 184,756 labellings and the World's hidden-covariate balance; one-way ANOVA as Pythagoras and as regression; orthogonal contrasts, the family-wise error, Tukey/Dunnett/Bonferroni/Scheffé; blocking with Darwin's *Zea mays*; Latin squares, Euler's officers and crossovers; factorials with OFAT on the bakery's ridge, the NPK cube, Yates's algorithm and Daniel's plot; fractional factorials and Plackett–Burman; response surfaces on the island bakery; split plots; optimal design with Kirstine Smith and Kiefer–Wolfowitz; power and the winner's curse; online experiments with CUPED and sample-ratio mismatch); the build is `explainer/stats/kit/design.py` (checked against SciPy/statsmodels) and `FieldPlot`; seven Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 79 min narration (estimate) + animation |
| 14 | **written**, English (13 chapters: the Challenger teleconference and the chart without the zeros; least squares on 0/1; logistic regression, odds ratios, logit vs probit and the canonical link; maximum likelihood by IRLS with the deviance; the Challenger fit with a dashboard, Wald vs profile intervals at 31°F and the extrapolation caveat; Poisson regression with offsets on the World; overdispersion in the World's towns; two-way and r × c tables at Berkeley; Simpson's paradox with mosaics; Mantel–Haenszel, CMH and Breslow–Day; case–control studies with Doll & Hill and a World check of Prentice–Pyke; ROC, calibration, the Brier score and thresholds); the build is `explainer/stats/kit/glm.py` (checked against statsmodels/SciPy) and `ChallengerDashboard`; eight Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 52 min narration (estimate) + animation |
| 15 | **written**, English (12 chapters: Bayes's billiard table, Laplace's Paris births and the sunrise; the machinery with sequential updating and a short history; conjugacy with the horse kicks and the World's heights; summaries, HPD and the Laplace approximation; prediction and predictive checks; priors, Jeffreys and prior predictive checks; the normal model's t posterior; grids on the Challenger posterior; Metropolis with step sizes, reparametrization and burn-in; credible-interval coverage and simulation-based calibration; Bayes factors, Lindley and the Sellke–Bayarri–Berger bound); the build is `explainer/stats/kit/bayes.py` and `BilliardTable`; six Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 16 | **written**, English (13 chapters: Efron's law schools; permutation tests from exchangeability with all 2,704,156 splits; the sign test, Fisher's sign flip of Darwin's maize, Wilcoxon's signed rank by generating function and Hodges–Lehmann; Mann–Whitney on the Challenger temperatures with U as the AUC; Kruskal–Wallis, Friedman, Spearman and Kendall; Pitman efficiency and the 0.864 bound; the jackknife's bias, SE, influence and failure for the median; the bootstrap principle and two worlds; percentile, basic, bootstrap-t and BCa intervals; the uniform maximum's 1 − 1/e spike; cross-validation and optimism; kernel densities and the bandwidth); the build is `explainer/stats/kit/ranks.py`, `explainer/stats/kit/bootstrap.py`, `BootstrapResampler` and `KernelSum`; eight Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 56 min narration (estimate) + animation |
| 17 | **written**, English (12 chapters: Yule's nonsense correlations, random walks and the pendulum; stationarity, the ACF and the autocorrelated mean with Newey–West and block bootstrap; AR, MA and ARMA with roots, the AR(2) triangle and Wold; pseudo-cycles, Slutsky and Yule's sunspot AR(2); identification by ACF/PACF and the Box–Jenkins cycle; Yule–Walker, least squares, AIC and Ljung–Box; forecasts with widening intervals on the sunspots of 1925–55; Keeling's CO₂ decomposed; exponential smoothing, Holt–Winters and the damped trend; spurious regression after Granger–Newbold; the M-competitions, a 63-series competition and rolling origins); the build is `explainer/stats/kit/ts.py`, `Correlogram`, `RootPlane` and `YulePendulum`; five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 18 | **written**, English (12 chapters: the *Literary Digest* recreated on the World; frame and nonresponse bias with Squire and Gallup's forecast; Meng's identity derived, with effective sizes of 6 and 50; design-based inference from Kiær, Bowley and Neyman; SRS, the fpc and systematic sampling; stratification and Neyman allocation; clusters, the design effect, PPS and multistage designs; Horvitz–Thompson and Basu's elephants; Laplace's ratio and the regression estimator; weighting, raking and MAR vs MNAR; polls from 1948 to 2020 and the Xbox poll); the build is the World's survey block, `explainer/stats/kit/survey.py` and `IslandMap`; five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 19 | **written**, English (12 chapters: the *Federalist* and Mosteller & Wallace's word rates from Gutenberg; training vs test error, Efron's optimism and Mallows' Cp; bias–variance derived and simulated for k-NN, df = tr S; cross-validation and the one-SE rule; k-NN, the curse of dimensionality and Cover & Hart; Poisson naive Bayes vs ridge logistic with learning curves; CART grown and pruned on the World's vote; ridge and the lasso with the ℓ₁ diamond; confusion matrices, ROC, precision–recall, calibration and cost-based thresholds; the disputed papers decided, with a robustness check on No. 55; leakage: selection inside the loop, six kinds of leak, holdout reuse and nested CV); the build is `explainer/stats/kit/learn.py` and `L1Geometry`; one Coverage Board row; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 20 | **written**, English (15 chapters: salt and blood pressure answered from NHANES 2017–2018, the public CDC survey; the estimand and a pre-specified plan; strata, masked PSUs and weights; a logged cleaning funnel; exploration; the planned weighted model; residual, spline, interaction and influence checks; four standard errors with t on 15 df; a 64-analysis specification curve and regression calibration from the second recall; a causal diagram against DASH-Sodium and the trial meta-analysis; the identical pipeline on the World and a randomized trial there; the one-page report; reproducibility, privacy and ethics; the BSc problem set); the build is the capstone pipeline, `explainer/stats/kit/capstone.py`, design-based regression and the Rao–Wu bootstrap in `statkit.survey`, the World's health block and the Museum's NHANES extract; three Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 55 min narration (estimate) + animation |
| 21 | **written**, English (13 chapters: Dantzig's homework, the World's bakery LP by simplex and Stigler's diet; convexity, Jensen, the log-partition function and condition numbers; Lagrange, KKT, the lasso's subgradients and PAVA; duality, the Neyman–Pearson lemma as an LP, ridge's dual and the lasso's duality gap; Boscovich's arcs, LAD and quantile regression on Engel; Newton and Fisher scoring on the likelihood's contours, Cauchy failure, Gauss–Newton; MM for the median, Engel and Bradley–Terry; coordinate descent; ISTA vs FISTA; ADMM and the fused lasso; Robbins–Monro, SGD and Polyak–Ruppert averaging; curvature, optimization vs statistical error, the sandwich); the build is `explainer/stats/kit/optim.py` and the `Landscape`; two Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 22 | **written**, English (14 chapters: Weldon's crabs and Pearson's nonic against maximum likelihood; the regularity conditions and the tanks; consistency by the KL inequality; asymptotic normality and the Cauchy; observed vs expected information after Efron–Hinkley; the gamma landscape, its ridge and the profile likelihood; Wald, score and LR, their intervals and Hauck–Donner; Neyman–Scott and why the profile fails; EM, Jensen's bound, its rate and Louis's SEs on the crabs; unbounded mixture likelihoods, label switching, boundary nulls and a parametric bootstrap; the KL projection, the sandwich and overdispersed counts; quasi-likelihood, the Ising model and Besag's pseudo-likelihood; the likelihood principle; Rao's metric, geodesics, the natural gradient and Jeffreys); the build is `explainer/stats/kit/mle.py` and the `LikelihoodLandscape`; Weldon's crabs in the Museum; five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 23 | **written**, English (12 chapters: Longley's test and the digits board; the sandwich and Gauss–Markov's fine print; the general linear hypothesis, its F three ways, the null F, the ellipse and Scheffé; GLS, WLS, AR(1) errors, Prais–Winsten and Durbin–Watson; HC0–HC3, Breusch–Pagan and the wild bootstrap; the World's schools, Moulton's factor, CR1, the wild cluster bootstrap, the level of clustering and random intercepts; the best linear predictor and the three regression bootstraps; attenuation, Hubble's three slopes, SIMEX; quantile regression, its sandwich, the fan and Engel's law; B-splines, knots by CV and tensor products; Householder, Givens and digits against κ; leverage, DFBETAS, the jackknife and masking); the build is `statkit.ols` II and the `DigitsBoard`; the World's `schools` block; Longley and Hubble in the Museum; eight Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 52 min narration (estimate) + animation |
| 24 | **written**, English (13 chapters: Bliss's beetles, probits and three links, the LD50 by Fieller; the three parts of a GLM and the linear probability model; the exponential dispersion family, gamma and Tweedie, links; IRLS derived on the beetles; deviance, analysis of deviance and randomized quantile residuals; asymptotics, the LD50, testing overdispersion, and the binary deviance's false alarms; separation, Firth and rare events; quasi-likelihood, the beta-binomial and a wrong mean posing as overdispersion; counts with offsets, NB, ZIP, hurdles and Poisson PML on the World's doctor visits; log-linear and graphical models; multinomial and proportional odds, checked; GEE on the World's schools, marginal vs conditional; proper scoring rules, calibration, CRPS and Murphy's decomposition); the build is `statkit.glm` II and the `DoseResponse` panel; the World's `visits` block; Bliss in the Museum; six Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 25 | **written**, English (14 chapters: Efron and Morris's eighteen hitters; James–Stein, Stein's lemma, SURE and the geometry of shrinkage; empirical Bayes, Robbins, the NPMLE and Tweedie's formula against the winner's curse; variance components, the ICC and design effects on the World's schools; the linear mixed model, Henderson's equations and BLUPs; ML vs REML; Satterthwaite, Kenward–Roger, boundary mixtures and profile intervals; growth curves with random slopes; nested towns, crossed essays and raters, lme4 notation; fixed vs random, Mundlak and Hausman; GLMMs by Laplace and AGQ, conditional vs marginal, and the World's hospital league table; Fay–Herriot small areas; meta-analysis, DL vs Hartung–Knapp; the Rasch model and test information); the build is `statkit.shrink`, `statkit.mixed` and the `ShrinkagePlot`; the World's `hospitals` block; Efron–Morris in the Museum; four Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 26 | **written**, English (14 chapters: Rubin's eight schools, no pooling, complete pooling and empirical Bayes's τ̂ = 0; the upgrade, exchangeability and de Finetti; the hierarchical model on an exact grid with the τ explorer; Jeffreys, reference, weakly informative and improper priors, with Gelman's sensitivity analysis; conjugate families, Diaconis–Ylvisaker and the doctor visits; Bernstein–von Mises seen, with coverage and failures; Bayes factors, Bartlett, BIC and model averaging; Lindley's paradox on the PEAR data and the Sellke–Bayarri–Berger bound; Occam's razor and the evidence; decisions, Wald, EVPI and EVSI; posterior and prior predictive checks; the workflow and simulation-based calibration; the argument, coherence and the likelihood principle; the Dirichlet process); the build is `statkit.bayes` II and the `TauExplorer`; the eight schools and PEAR in the Museum; three Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 27 | **written**, English (14 chapters: Metropolis's hard disks; importance sampling, the optimal proposal and PSIS; Metropolis–Hastings, detailed balance and the 0.234 rule; Gibbs, data augmentation and Albert–Chib on Bliss's beetles; R-hat, ESS and rank plots; Hamiltonian Monte Carlo, leapfrog vs Euler and the puck on the surface; NUTS and its warmup; Neal's funnel and the eight schools, centred vs non-centred against the exact grid; statkit's probabilistic programming language checked against closed forms; particle filters and tempered SMC; variational inference, CAVI and ADVI; Laplace and INLA; ABC and neural posterior estimation; coupling from the past); the build is `statkit.ppl` and the `PuckSurface`; four Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 28 | **written**, English (13 chapters: Freedman's paradox, noise screened into a significant regression; optimism, Efron's covariance penalty and the lasso's degrees of freedom; Cp, AIC derived, TIC on the World's visits and AICc; BIC by Laplace, the unit-information prior, consistency vs efficiency; PRESS, GCV and what CV estimates; PSIS-LOO, k̂ and WAIC on the eight schools; a singular mixture's RLCT by quadrature; MDL, NML and the prequential code; BMA vs stacking; the winner's curse and inference after selection; best subset vs the lasso and bootstrap stability on Stamey's prostate data; PIT, proper scores and CRPS); the build is `statkit.select` and the model-selection bench (`CriterionBench`); three Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50.5 min narration (estimate) + animation |
| 29 | **written**, English (14 chapters: Old Faithful's eruptions and Silverman's mode test, two humps not three; the histogram's exact MISE and cube-root bin; kernel estimates' bias, variance, Marron–Wand MISE and Epanechnikov's kernel; normal reference, Silverman, LSCV and Sheather–Jones; Silverman's table and the curse of dimensionality; Nadaraya–Watson vs local linear and LOESS on the motorcycle crash; the Reinsch–Schoenberg theorem and the spline spectrum; GCV vs REML; RKHS, the representer theorem and Gaussian processes; Haar/Daubechies wavelets, VisuShrink and SureShrink; an additive model for New York's ozone; robust bias-corrected intervals; isotonic regression and Grenander's cube-root rate); the build is `statkit.smooth` and the spline spectrum (`SplineSpectrum`); three Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50 min narration (estimate) + animation |
| 30 | **written**, English (12 chapters: Tukey's contaminated normal and Newcomb's 66 measurements of light; Pitman efficiency, the sign test's 2/π, Wilcoxon's 3/π and the 0.864 bound derived, normal scores; Hodges–Lehmann and its exact interval on Newcomb and Darwin; influence functions, sensitivity curves and the estimator rail; breakdown, maximal bias and implosion; Huber's minimax estimator derived, ψ functions, IRLS and a small Princeton Robustness Study; MAD, Qn, Sn and 1-D masking; LMS, LTS, GM, S and MM regression on the CYG OB1 stars; the MCD and Stahel–Donoho on Hawkins–Bradu–Kass; median of means and Catoni on Pareto data; contaminated samples from the World); the build is `statkit.robust` and the estimator rail (`EstimatorRail`); six Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50.7 min narration (estimate) + animation |
| 31 | **written**, English (12 chapters: the World's map rebuilt from road distances by classical scaling, and Hartigan's Europe with its Cologne–Geneva error; the data matrix, whitening and Mahalanobis distance on Fisher's irises; the Wishart, Bartlett's decomposition, the inverse-Wishart and Marchenko–Pastur; Hotelling's T² by union–intersection, the simultaneous ellipsoid and MANOVA's four statistics; principal components, Eckart–Young, classical scaling as PCA, the US-arrests biplot and parallel analysis; ML factor analysis of the 24 tests, Bartlett's test, varimax, factor scores and Heywood cases; canonical correlation on the savings data, principal angles and PLS; LDA, QDA and logistic regression; Lloyd's k-means, Gaussian mixtures, BIC and the adjusted Rand index; partial correlations, the graphical lasso and neighbourhood selection; T² as p/n grows, Bai–Saranadasa and Ledoit–Wolf); the build is `statkit.multi` and the map from distances (`DistanceMap`); five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51.9 min narration (estimate) + animation |
| 32 | **written**, English (13 chapters: Candès's phantom recovered exactly from 22 radial lines of k-space by total-variation minimization; the upgrade of Part 19 and the s log(p/s) count; ridge on the diabetes data through the SVD, its trace, its prior and Hoerl–Kennard's theorem; best subset, the ℓq balls, the octahedron and the convex envelope; the lasso's KKT conditions, soft thresholding and geometry; coordinate descent and the exact LARS-lasso path with HDL's drop; the elastic net, group, fused and adaptive lassos, SCAD and MCP with a support-recovery study; CV, the one-SE rule and stability selection on the 64-term quadratic model; Laplace versus horseshoe shrinkage and spike-and-slab; basis pursuit, the null space property, RIP, the Donoho–Tanner phase transition and the phantom against the number of lines; naive post-lasso inference, the debiased lasso, single versus double selection and PoSI; matrix completion by SoftImpute); the build is `statkit.sparse` and the phantom (`PhantomPanel`); five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 56.3 min narration (estimate) + animation |
| 33 | **written**, English (14 chapters: the dead salmon re-run on 9,141 voxels of smoothed noise; the World's 5,000-gene study and the p-value sea; Bonferroni, Šidák, Holm as closed testing, Hochberg and Westfall–Young; Benjamini–Hochberg with its proof, BH as a plug-in, PRDS and BY; Storey's π0, q-values and two-stage BH; Efron's local fdr and empirical null on the prostate data; the spread of the FDP under dependence and FDX; model-X and fixed-X knockoffs with the coin-flip proof; forking paths, optional stopping and the p-hacking simulator; Ioannidis's PPV, power, type M/S errors and the replication projects; funnels, Egger, PET, p-curves and selection models; preregistration, registered reports, α = 0.005, 'abandon significance' and the ASA; the false coverage rate); the build is `statkit.multiple`, the p-hacking simulator and the p-value sea (`PValueSea`); six Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 52.8 min narration (estimate) + animation |
| 34 | **written**, English (13 chapters: Breiman's two cultures with Cox's and Efron's replies; Shmueli's explain or predict and the Rashomon effect on the Wisconsin breast cancer data (50 bootstrap trees, 5 root features); forests' ρσ² + (1 − ρ)σ²/B measured on Friedman 1, OOB error, consistency, impurity vs permutation importance, the infinitesimal jackknife for bootstrap and subsampled forests; boosting as stagewise additive modelling, shrinkage and the lasso link; what cross-validation estimates (Bates, Hastie & Tibshirani); calibration with Platt, isotonic and temperature scaling; the quantile lemma and split conformal on the World's incomes; jackknife+, CV+ and CQR; weighted conformal under covariate shift and adaptive conformal online; APS, Mondrian sets and conformal p-values; prediction-powered inference and PPI++ with a smartwatch on the World's blood pressure; partial dependence, permutation, LOCO and Shapley values; the asthma and pneumonia model); the build is `statkit.conformal` and `statkit.ppi`, and the score ladder (`ScoreLadder`); fourteen Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 82 min narration (estimate) + animation |
| 35 | **written**, English (16 chapters: the Salk trial's two designs (43 vs 29 per 100,000); potential outcomes and the science table on the World's clinic trial, where both outcomes are known; estimands, SUTVA and hidden versions; selection bias measured when doctors choose; Fisher's sharp null, exact and by Monte Carlo, and its inversion; Neyman's variance and its conservative estimate; blocking, pairing and rerandomization; Freedman's critique of adjustment and Lin's interacted estimator; cluster randomization on the World's schools; noncompliance, principal strata and the LATE; interference and the two-stage design on an epidemic in the World's towns; ISIS-2 and subgroup fishing; peeking, Pocock, O'Brien–Fleming and Lan–DeMets boundaries; CAST and Prentice's surrogate criteria; transporting a trial to its target population); the build is the World's clinic trial and epidemic, `statkit.causal` (I) and the science table (`ScienceTable`); eleven Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 56 min narration (estimate) + animation |
| 36 | **written**, English (17 chapters: LaLonde's test on the NSW job-training data ($1,794 experimental vs −$635 against the PSID); unconfoundedness and overlap on an observational version of the World's clinic, where both outcomes are known; causal diagrams, chains, forks, colliders and d-separation; the back-door criterion, Berkson's bias, M-bias and mediators; the front door and the do-calculus; Simpson's paradox resolved by the graph; g-computation; propensity scores, matching and Cochran's five strata; IPW, balance and extreme weights; AIPW and Kang–Schafer's four scenarios; double machine learning with cross-fitting and the partially linear model; heterogeneous effects by T-, S-, X- and DR-learners and an honest causal forest; sensitivity analysis by Rosenbaum's Γ, E-values and Cinelli–Hazlett robustness values; smoking and lung cancer from Doll and Hill to Cornfield and Hill's viewpoints; time-varying treatments, marginal structural models, the g-formula and target trials; LaLonde revisited with overlap and placebo tests); the build is `statkit.causal` (II), the Museum's NSW data and the causal graph (`CausalGraph`); nine Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 56 min narration (estimate) + animation |
| 37 | **written**, English (16 chapters: Snow's Table IX (315 vs 37 per 10,000 houses); the credibility revolution and four designs; instruments, the Wald ratio and 2SLS on the World's schooling survey with quarter of birth; weak instruments, the t-test's size, tF and Anderson-Rubin sets; many instruments, LIML, Bound-Jaeger-Baker's fake quarters and Mendelian randomization with MR-Egger; regression discontinuity on the World's scholarship with local fits, the IK bandwidth and robust bias correction; McCrary's test after re-marking, covariate balance, fuzzy RD and close elections; Card and Krueger's difference-in-differences and an event study; placebo laws and clustered SEs; staggered adoption, where TWFE gets the sign wrong, the Goodman-Bacon decomposition, Callaway-Sant'Anna and imputation; honest parallel trends; Prop 99's synthetic control and placebo states; synthetic DiD reproducing Arkhangelsky et al.; fixed effects, Nickell's bias and Anderson-Hsiao; Manski and Lee bounds); the build is the World's schooling survey, scholarship and rollout, `statkit.quasi` and the cutoff lens (`CutoffLens`); eight Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 60 min narration (estimate) + animation |
| 38 | **written**, English (14 chapters: Hurst's R/S on Toussoun's Nile minima (H = 0.85); four departures from Part 17, Wold and ergodicity; spectra, the periodogram's inconsistency, Welch and multitaper, the 11-year sunspot cycle; Dickey-Fuller and its Brownian limit, KPSS, US macro series, Perron's breaks; spurious regression, Engle-Granger and Johansen on consumption and income, super-consistency; GARCH on the DAX, value-at-risk exceedances, volatility forecasts; ARFIMA, GPH and local Whittle, the long-memory mean; the Kalman filter as Gaussian conditioning with ellipses, the Nile's local level matching Durbin and Koopman, the steady-state gain as exponential smoothing, the 1899 drop; RTS, missing years, the prediction-error likelihood, EM, structural models, Apollo; EKF, UKF and particle filters, PMCMC, Hamilton's regimes in US growth; VARs, Granger causality, impulse responses and the price puzzle; block and stationary bootstraps; pretrained forecasters and honest evaluation); the build is `statkit.ts` (II), the Museum's Nile flow and minima, DAX and US macro data, and the Kalman ellipses (`KalmanEllipses`); seven Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51 min narration (estimate) + animation |
| 39 | **written**, English (15 chapters: Krige's boreholes and the World's hidden pollution field; Tobler's law, Cressie's three kinds of data, the effective sample size of 300 stations (5.7); random fields and Bochner's theorem; variograms on Meuse's log zinc, nugget, sill and range, Cressie-Hawkins, directional variograms; kriging derived, simple, ordinary and universal, the Meuse map and its cross-validation, the World against the truth, kriging as the GP posterior; Matern smoothness, Stein, Zhang's ridge measured, and kriging along and off it; ML and REML, choosing the smoothness, the cubic wall; Vecchia, its accuracy and profile, 100,000 locations, NNGP and the alternatives; GMRFs, the SPDE and INLA; Moran's I, SMRs, CAR, SAR and BYM on the World's towns; Snow's map, Ripley's K, the inhomogeneous null, Cox processes; spatial confounding simulated, Hodges and Reich, Paciorek, restricted spatial regression; separable and Gneiting covariances, the World's daily readings; GPs in machine learning, the Occam factor, emulators, expected improvement; honest prediction with block cross-validation and Meuse's z-scores); the build is `statkit.spatial`, the World's pollution block, the Museum's Meuse and Snow's map, and the field surface (`FieldSurface`); five Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50.6 min narration (estimate) + animation |
| 40 | **written**, English (16 chapters: the 6-MP trial with its twelve open rings; S, h and H, Graunt, Gompertz, Weibull and bathtub hazards; censoring and truncation on the World's cohort, naive treatments against the truth, delayed entry on the age scale; Kaplan-Meier derived and drawn as a staircase, redistribute-to-the-right, medians; Greenwood, plain, log and log-log bands, Hall-Wellner; Nelson-Aalen and the life table; counting processes, compensators and martingales checked on 4,000 paths; the log-rank test on Gehan's data, weighted versions; Cox's partial likelihood, ties, the Mayo PBC model and its null trial; Schoenfeld residuals, Grambsch-Therneau, the fading Karnofsky effect; what hazard ratios mean, frailty selection in a trial, RMST; immortal time, the Oscar winners, Stanford's transplants, the World's useless statin; AFT models and cure fractions; competing risks on MGUS, Aalen-Johansen and Fine-Gray; frailty, Vaupel's deceleration, the kidney infections; prediction with concordance, IPCW Brier, a survival forest and conformal lower bounds); the build is `statkit.survival`, the World's cohort block, the Museum's Gehan, PBC, Stanford, VA, MGUS and kidney data, and the KM staircase (`KMStaircase`); seven Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 50.4 min narration (estimate) + animation |
| 41 | **written**, English (10 chapters: Wald's bombers, the engines' missing holes; Rubin's mechanisms on the World's survey with three known masks, ignorability, patterns, missingness graphs, what can and cannot be tested; the easy methods' sins, complete cases right for some questions, the missing indicator, available cases, mean imputation, LOCF in a seeded trial; EM and FIML on New York's ozone, Buck, the missing information principle; multiple imputation, Rubin's rules derived, proper draws and PMM, chained equations, how many copies, congeniality; weighting as causal inference, IPW, AIPW and double robustness, calibration, balance; MNAR, Heckman on Mroz's women, exclusion restrictions, Manski bounds, pattern mixtures and a tipping point; MRP, the Xbox poll, the World's opt-in poll, YouGov, small areas; measurement error, Spearman, NHANES's sodium recalls, regression calibration, SIMEX, Deming, Berkson; misclassification, the matrix method, recall bias, validation substudies); the build is `statkit.mi`, the World's missing block, the Museum's Mroz data, and the mask grid (`MaskGrid`); nine Coverage Board rows; silent 480p QA renders and contact sheets reviewed; narration and Chinese edition to do | ≈ 51.2 min narration (estimate) + animation |
