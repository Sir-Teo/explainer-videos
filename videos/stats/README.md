# Statistics, Built (统计学，从零搭建)

**Status: master plan (draft 1), not yet in production.** No part has sources, data or renders yet. The
chapter-by-chapter plan and the production standard are in [`SYLLABUS.md`](SYLLABUS.md).

This is a thirty-six-part course on mathematical statistics, in English and Chinese. It starts with a 1662 table of
London deaths and ends with the statistics of evaluating AI models. On the way it covers what a graduate statistics
curriculum covers: probability and its limit theorems; the classical theory of estimation, testing and intervals;
large-sample optimality; linear, generalized and hierarchical models; Bayesian inference and its computation;
resampling, rank, robust and smoothing methods; multivariate and high-dimensional statistics; multiple testing and
the replication crisis; prediction and conformal inference; causal inference from experiments, observational data
and natural experiments; time series, spatial data, survival data, surveys and missing data; and sequential,
anytime-valid inference.

Each part is a **50–60 minute lecture**. It derives its mathematics on screen, every step with its reason. It tells
the history of the ideas, including who argued with whom. It builds a working tool or toy, and it checks every
claim with a real computation. The videos are named `stats1` … `stats36`, in `videos/stats/statsN/`.

## The story

**Graunt's question.** In 1662 John Graunt, a London haberdasher, read half a century of weekly *Bills of
Mortality*. From them he worked out things about the living city that nobody had counted: how many people lived
there, how many boys were born for every girl, how long a Londoner could expect to live. Statistics is his question
made precise: *what can we know about what we cannot see, from what we can, and how often will we be wrong?*

The second half of that question drives the series. Every statistical method promises something: an unbiased
estimate, a 5% false-alarm rate, a 95% interval, a controlled false discovery rate. The series asks which promises
are kept, under what assumptions, and what breaks them. It answers by measuring.

* **Act I, Data and Chance (Parts 1–6).** The data first, then the language of chance: axioms and conditioning,
  the family of distributions, many variables at once, the laws of averages, and randomness unfolding in time
  (Markov chains and martingales).
* **Act II, Inference (7–13).** The problem turned around, from data back to the world: sampling distributions,
  sufficiency, likelihood, significance tests, confidence intervals, decision theory and the shock of Stein's
  shrinkage, and Le Cam's large-sample theory of what "best" means.
* **Act III, Models (14–17).** Least squares and its geometry, the design of experiments, generalized linear models
  and hierarchical models.
* **Act IV, Bayes (18–20).** Inverse probability from Bayes's billiard table to Bernstein–von Mises; computing
  posteriors (Monte Carlo, MCMC, HMC and our own probabilistic programming language); checking, comparing and
  averaging models.
* **Act V, Fewer Assumptions (21–23).** The bootstrap, ranks and robustness, and smoothing.
* **Act VI, Many Variables, Many Questions (24–27).** Multivariate analysis and random matrices, sparsity,
  multiple testing and replication, and prediction with honest uncertainty (conformal inference).
* **Act VII, Causes (28–30).** Potential outcomes and randomized experiments, causal inference from observational
  data, and natural experiments.
* **Act VIII, Data with Structure (31–34).** Time series and the Kalman filter, spatial statistics and Gaussian
  processes, survival analysis, and surveys, missing data and selection.
* **Finale (35–36).** Inference that watches the data arrive (sequential tests, e-values, confidence sequences),
  then statistics in the age of AI and the complete Coverage Board.

Each part is a story with a historical hook, a central question, a climax that is usually something we build or
compute, and a hand-off that poses the next part's question. Part 1 hands off with "a statistic is itself random,
so we need the language of chance". Part 14 hands off with "a regression cannot tell cause; design the data", and
Part 27 with "a model that predicts well can still be useless for deciding what to do".

## The devices that hold it together

1. **The World** (`explainer.stats.world`). A seeded, simulated population of one million residents in households,
   towns and regions. It holds heights inherited through families, skewed incomes, schools, a disease with a
   screening test, a treatment taken for confounded reasons with *both* potential outcomes recorded for everyone,
   an instrument, a staggered policy, a scholarship cutoff, survival times, a spatial pollution field, daily time
   series with a change point, survey response propensities, missingness mechanisms, data-entry errors, and 10,000
   genetic markers with 20 real effects. In real life the truth is never visible. In the World it is, so every
   estimator, test and interval in the series can be graded against it. It is always labelled `simulated` on screen.
2. **The Coverage Board** (`explainer.stats.board`). This is the series' scoreboard. Each interval or test a part
   introduces is run thousands of times on the World. The board records its actual coverage (or false-alarm rate)
   against the nominal 95% (or 5%), with Monte Carlo error bands. Green means the promise is kept, red means it is
   broken, blue means it is conservative. The first rows appear in Part 7: the t-interval kept, the z-interval
   with an estimated σ at n = 5 broken. The last rows come in Part 36: cluster-robust error bars for AI evaluations.
   In between, about a hundred rows record where each assumption fails, including the Wald binomial interval,
   classical errors under heteroskedasticity, intervals after model selection, two-way fixed effects under
   staggered adoption, peeking at a running t-test, and, kept, conformal intervals and confidence sequences.
3. **The Museum** (`explainer.stats.museum`). This is real historical data, transcribed from the original
   publication with its source on screen. Examples: Graunt's bills (1662), Arbuthnot's christenings (1710),
   Quetelet's chests (1846), Snow's water companies (1855), Galton's families (1886), Weldon's crabs (1893),
   Bortkiewicz's horse kicks (1898), Student's sleep data (1908), Yule's nonsense correlation (1926), the Salk trial
   (1954), Freireich's leukemia trial (1963), the Efron–Morris batting averages (1975), the eight schools (1981),
   the Berkeley admissions (1973) and the Challenger O-rings (1986). The World is where the truth is known; the
   Museum is where the methods were born.
4. **statkit, built** (`explainer/stats/kit/`). The series writes its own small, readable statistics library, one
   piece per part: samplers from a single uniform, an MLE/EM engine, least squares by QR with sandwich errors, IRLS
   for GLMs, REML, a tiny probabilistic programming language with NUTS, the bootstrap with BCa, rank tests, robust
   regression, smoothing splines, a coordinate-descent lasso, Benjamini–Hochberg and knockoffs, conformal
   prediction, double machine learning, the Kalman filter, kriging, Kaplan–Meier and Cox, survey weighting,
   multiple imputation, and confidence sequences. Each tool is checked against SciPy and statsmodels in `tests/`.
   By the finale, viewers have watched a statistics package being built and verified.
5. **The timeline strip, 1650–2030**, from Graunt to e-values, lit on every chapter card; **payoff cards** ("where
   this comes back"); and **cross-series links** to *Analysis, Built* (measure, Hilbert space, Fourier) and *AI,
   Built* (information, learning theory, diffusion), where those parts are the deeper treatment.

## How it looks

The series draws in the manner of 3Blue1Brown, with *AI, Built*'s instruments (`explainer.ai.viz`,
`explainer.ai.lecture`) and *Analysis, Built*'s derivation ladder (`explainer.analysis.ladder`, `why`). New
statistics instruments go in `explainer/stats/viz.py`.

* **Colour is meaning, everywhere.** The true parameter θ is always gold and the estimate θ̂ always blue. Data are
  white, the null distribution grey, the alternative teal. The prior is purple, the likelihood green, the posterior
  orange. Residuals are red, treated units coral and controls sky blue, and missing values are hollow.
* **Sampling is shown, not stated.** `SamplingMachine` draws samples from the World, computes the statistic, and
  drops each value into a growing histogram, so the sampling distribution builds itself. `IntervalRain` shows a
  hundred intervals falling against the truth line, with the misses turning red and a live coverage counter.
* **Statistics as geometry.** `NSpace` puts a sample of three in 3D with the camera orbiting. The mean is a
  projection onto the 1-vector; χ² is a squared length; regression is a projection onto the column space; ANOVA is
  Pythagoras; Cochran's theorem is a set of orthogonal projections.
* **Landscapes.** Log-likelihood surfaces in 3D: the score as slope, Fisher information as curvature, the profile
  likelihood as a ridge walk, and the Wald, score and likelihood-ratio tests drawn on one curve. HMC's puck slides
  over the negative log-posterior, and the lasso's diamond meets the elliptical contours.
* **Live quantities.** Bandwidth, prior strength, shrinkage factor and contamination fraction are value trackers,
  so the viewer sees each estimate respond.
* **Signature sequences.** The Galton board falling into a bell; the Neyman belt read sideways; Stein shrinkage
  pulling points in 3D; Marchenko–Pastur's bulk forming and the BBP spike popping out of it; Benjamini–Hochberg's
  line sweeping a sea of 5,000 p-values; flows of association through a causal graph, blocked and unblocked; the
  potential-outcomes table with half its cells hidden; Kalman ellipses predicting and updating; a Kaplan–Meier
  staircase with its risk set leaving; a kriging surface with its uncertainty; betting martingales hitting Ville's
  ceiling.
* **Real numbers.** Everything plotted comes from the part's `compute.py` and is asserted in the scene. Tags say
  which kind it is: `computed`, `simulated` (the World), `historical data` (the Museum, with source),
  `illustrative` or `schematic`.

## The parts

| # | Part | Hook | Mathematics | Built |
|---|---|---|---|---|
| **I** | **Data and Chance** | | | |
| 1 | The Shape of Data | Graunt's bills, 1662 | summaries as loss minimizers, ECDF, QQ, Box–Cox, correlation as a cosine, Anscombe, Simpson | the World; a same-statistics morph |
| 2 | Chance, Counted | the problem of points, 1654 | axioms, σ-algebras, conditioning, Bayes, independence, random variables, expectation, Dutch books | an exact probability engine |
| 3 | The Family of Distributions | Bortkiewicz's horse kicks | binomial→Poisson, normal (de Moivre, Gauss, Herschel–Maxwell), χ²/t/F, order statistics, generating functions, the family tree | a sampler library from one uniform; RANDU's planes |
| 4 | Many Variables at Once | Galton's ellipses, 1886 | conditional expectation as projection, Eve's law, multivariate normal, Schur complements, copulas, exchangeability, de Finetti | a Gaussian slicer; Pólya's urn |
| 5 | The Laws of Averages | Galton's ox, 1907 | modes of convergence, LLN, Glivenko–Cantelli, DKW, concentration, CLT proved, Berry–Esseen, delta method, stable laws, extreme values, large deviations | a Galton board |
| 6 | Fair Games | Markov's *Onegin*, 1913 | Markov chains, mixing, shuffles, Pólya recurrence, martingales, optional stopping, Ville, Azuma, Donsker, the Brownian bridge | a KS test from scratch |
| **II** | **Inference** | | | |
| 7 | From Sample to Population | Student at Guinness, 1908 | sampling distributions, n−1 as dimension, Fisher's geometry of the normal sample, χ², t, F, Cochran, MSE, plug-in | Student's card-deck experiment; the Board's first rows |
| 8 | Data Reduction | the German tank problem | sufficiency, factorization, exponential families, Rao–Blackwell, Lehmann–Scheffé, Basu, Fisher information, Cramér–Rao | the tank factory game |
| 9 | Likelihood | Pearson's crabs, 1894 | MLE consistency and normality, profile likelihood, Neyman–Scott, EM, misspecification and the sandwich, the likelihood principle | an MLE/EM engine |
| 10 | Significance | Arbuthnot 1710; the lady tasting tea | p-values, Neyman–Pearson, UMP and MLR, Wilks, the trinity, Pearson's χ², Mendel, Welch, power, equivalence | a permutation machine |
| 11 | Honest Intervals | the broken Wald interval | Neyman's construction, pivots, test inversion, Wilson and Clopper–Pearson, Fieller and Gleser–Hwang, Feldman–Cousins, Scheffé, tolerance intervals, fiducial | the Coverage Board, formally |
| 12 | The Shock of Shrinkage | Efron–Morris baseball, 1975 | decision theory, risk sets, minimax, complete classes, Stein's lemma, James–Stein, Brown's recurrence link, empirical Bayes, Tweedie | a hospital league table |
| 13 | Asymptopia | Hodges' superefficient estimator | M/Z-estimators, influence functions, U-statistics, LAN, contiguity, Le Cam's third lemma, Hájek's convolution theorem, semiparametric efficiency, Edgeworth, saddlepoints | a risk-bump explorer |
| **III** | **Models** | | | |
| 14 | Least Squares | Gauss finds Ceres, 1801 | projection, Gauss–Markov, F as Pythagoras, Frisch–Waugh–Lovell, leverage and Cook's D, sandwich and cluster SEs, errors in variables, quantile regression, QR | statkit.ols; an influence probe |
| 15 | Experiments by Design | Fisher at Rothamsted, 1919 | randomization inference, ANOVA geometry, blocking, Latin squares, factorials, aliasing, response surfaces, D-optimality, split plots, CUPED | a field-trial simulator |
| 16 | Beyond the Normal | the Challenger O-rings, 1986 | exponential dispersion families, IRLS, deviance, separation and Firth, overdispersion, quasi-likelihood, log-linear models, case–control, GEE, proper scores | statkit.glm |
| 17 | Borrowing Strength | the eight schools | random effects, BLUP, REML, boundary tests, longitudinal data, GLMMs and Laplace, splines as mixed models, Fay–Herriot, meta-analysis, Rasch | statkit.mixed |
| **IV** | **Bayes** | | | |
| 18 | Inverse Probability | Bayes's billiard table, 1763 | conjugacy, priors (Jeffreys, reference), Bernstein–von Mises, Doob consistency, Bayes factors, Lindley's paradox, matching priors, Dirichlet processes | the billiard table |
| 19 | Sampling the Posterior | Los Alamos, 1953 | Monte Carlo, importance sampling, MH, Gibbs, HMC, NUTS, R̂ and ESS, Neal's funnel, SMC, VI, ABC, neural posterior estimation, SBC, coupling from the past | a tiny probabilistic programming language |
| 20 | Which Model? | Freedman's paradox, 1983 | optimism and degrees of freedom, AIC and BIC derived, CV and GCV, posterior predictive checks, PSIS-LOO, WAIC, singular learning theory, MDL, stacking | a model-selection bench |
| **V** | **Fewer Assumptions** | | | |
| 21 | Pulling Yourself Up | Efron's law-school data, 1979 | jackknife, bootstrap, percentile/t/BCa, Edgeworth explanation, failures and m-out-of-n, wild and block bootstraps, .632+, Bayesian bootstrap | statkit.bootstrap |
| 22 | When the Model Is Wrong | Tukey's contaminated normal, 1960 | rank tests, Pitman efficiency and the 0.864 bound, Hodges–Lehmann, influence and breakdown, Huber's minimax, LTS, MM, MCD, median-of-means, robust high-dimensional estimation | statkit.robust |
| 23 | Smoothing | Old Faithful's two humps | histograms and KDE (rates derived), Epanechnikov, bandwidths, local polynomials, the smoothing-spline theorem, RKHS, wavelet thresholding, minimax lower bounds, isotonic and Grenander | statkit.smooth |
| **VI** | **Many Variables, Many Questions** | | | |
| 24 | Many Variables | PCA finds structure in noise | Wishart, Hotelling T², PCA, factor analysis, CCA, LDA, MDS, Marchenko–Pastur, BBP, Tracy–Widom, Ledoit–Wolf, graphical lasso | a random-matrix lab; a map from distances |
| 25 | More Variables Than Data | Candès's phantom, 2004 | ridge, ℓ1 geometry, soft-thresholding, LARS, compressed sensing, Donoho–Tanner, oracle inequalities, debiased lasso, post-selection inference, ridgeless double descent | statkit.lasso; phantom recovery |
| 26 | Thousands of Questions | the dead salmon in the scanner | FWER, closed testing, BH proved, q-values, local fdr, knockoffs, selective inference, forking paths, Ioannidis, publication bias | a p-hacking simulator |
| 27 | The Two Cultures | Breiman, 2001 | forests and boosting as estimators, what CV estimates, calibration, conformal prediction (split, jackknife+, CQR, weighted, adaptive), conformal risk control, prediction-powered inference | statkit.conformal |
| **VII** | **Causes** | | | |
| 28 | What If? | the Salk polio trial, 1954 | potential outcomes, randomization and Neyman inference, Lin's adjustment, clusters, noncompliance and LATE, interference, surrogates, transportability | a trial where both outcomes are visible |
| 29 | Causes Without Experiments | LaLonde's job training, 1986 | DAGs and d-separation, back-door and front-door, do-calculus, propensity scores, IPW, AIPW, DML, causal forests, sensitivity and E-values, causal discovery | statkit.causal |
| 30 | Natural Experiments | Snow's Grand Experiment, 1854 | IV and 2SLS, weak instruments and Anderson–Rubin, RD, DiD, staggered adoption, synthetic control, SDID, Manski bounds | the World's natural experiments |
| **VIII** | **Data with Structure** | | | |
| 31 | Time Series | Yule's nonsense correlation, 1926 | ARMA, Wold, spectra, unit roots and Dickey–Fuller, spurious regression, cointegration, GARCH, long memory, the Kalman filter, VARs | statkit.ts |
| 32 | Space | Krige's gold, 1951 | random fields, variograms, kriging, Matérn, Vecchia, GMRFs and SPDE, CAR/BYM, point processes and Ripley's K, Gaussian processes | statkit.spatial |
| 33 | Time to Event | Freireich's 6-MP trial, 1963 | censoring, Kaplan–Meier, Greenwood, counting-process martingales, log-rank, Cox's partial likelihood, hazard-ratio pitfalls, competing risks, frailty | statkit.survival |
| 34 | Who's Missing? | the *Literary Digest*, 1936 | Meng's identity, Horvitz–Thompson, stratification and Neyman allocation, design effects, raking, MRP, Rubin's mechanisms, multiple imputation, Heckman, SIMEX, differential privacy | statkit.survey, statkit.mi |
| **Finale** | | | | |
| 35 | Watching as You Go | Wald's SPRT, 1943 | peeking, the SPRT, alpha spending, test martingales, e-values, universal inference, confidence sequences, e-BH, CUSUM, inference after bandits | statkit.sequential |
| 36 | What Can We Honestly Claim? | back to Graunt | error bars for AI evaluations, arenas and IRT, the reusable holdout, PPI with LLM labels, model collapse, conformal for LLMs, watermark tests, simulation-based inference; the full Coverage Board | an eval-statistics kit |

## The bookshelf

The parts follow the standard graduate texts, with the classic and frontier papers on each part's reference card.
The main books, by part:

| Area | Books | Parts |
|---|---|---|
| Probability | Feller; Billingsley *Probability and Measure*; Durrett; Grimmett & Stirzaker; Blitzstein & Hwang; Williams *Probability with Martingales*; Norris; Levin, Peres & Wilmer; Vershynin *High-Dimensional Probability*; Boucheron, Lugosi & Massart | 2–6 |
| Mathematical statistics | Casella & Berger; Wasserman *All of Statistics*; Rice; Hogg, McKean & Craig; DeGroot & Schervish; Bickel & Doksum; Keener; Shao; Schervish; Cox & Hinkley; Young & Smith | 7–12 |
| Estimation and testing | Lehmann & Casella *Theory of Point Estimation*; Lehmann & Romano *Testing Statistical Hypotheses*; Pawitan *In All Likelihood*; Schweder & Hjort *Confidence, Likelihood, Probability* | 8–11 |
| Decision theory | Berger *Statistical Decision Theory and Bayesian Analysis*; Ferguson; Efron *Large-Scale Inference* | 12, 26 |
| Asymptotics | van der Vaart *Asymptotic Statistics*; Ferguson *A Course in Large Sample Theory*; Le Cam & Yang; Lehmann *Elements of Large-Sample Theory*; Serfling; Bickel, Klaassen, Ritov & Wellner; Tsiatis *Semiparametric Theory and Missing Data* | 13, 29 |
| Linear and generalized models | Seber & Lee; Rao *Linear Statistical Inference*; Christensen *Plane Answers*; Weisberg; Freedman *Statistical Models*; Agresti *Foundations* and *Categorical Data Analysis*; McCullagh & Nelder; Koenker *Quantile Regression* | 14, 16 |
| Design | Fisher *The Design of Experiments*; Box, Hunter & Hunter; Montgomery; Cox & Reid; Wu & Hamada; Atkinson, Donev & Tobias; Kohavi, Tang & Xu | 15 |
| Multilevel models | Gelman & Hill; Gelman, Hill & Vehtari; Pinheiro & Bates; Searle, Casella & McCulloch; Wood *Generalized Additive Models*; Rao & Molina | 17 |
| Bayesian | Gelman et al. *Bayesian Data Analysis*; McElreath *Statistical Rethinking*; Robert *The Bayesian Choice*; Bernardo & Smith; Jaynes; Hoff; Ghosal & van der Vaart | 18–20 |
| Computation | Robert & Casella *Monte Carlo Statistical Methods*; Liu; Brooks et al. *Handbook of MCMC*; Owen; Chopin & Papaspiliopoulos; Efron & Hastie *Computer Age Statistical Inference* | 19, 21 |
| Model selection | Burnham & Anderson; Claeskens & Hjort; Konishi & Kitagawa; Watanabe; Grünwald *The MDL Principle* | 20 |
| Resampling | Efron & Tibshirani; Davison & Hinkley; Hall *The Bootstrap and Edgeworth Expansion*; Shao & Tu; Politis, Romano & Wolf | 21 |
| Nonparametric and robust | Lehmann *Nonparametrics*; Hollander, Wolfe & Chicken; Huber & Ronchetti; Hampel et al.; Maronna et al.; Diakonikolas & Kane; Silverman; Wand & Jones; Fan & Gijbels; Tsybakov; Wasserman *All of Nonparametric Statistics*; Wahba | 22, 23 |
| Multivariate and random matrices | Anderson; Mardia, Kent & Bibby; Johnson & Wichern; Muirhead; Jolliffe; Bai & Silverstein; Couillet & Liao; Lauritzen | 24 |
| High-dimensional | Hastie, Tibshirani & Friedman *ESL*; Hastie, Tibshirani & Wainwright; Bühlmann & van de Geer; Wainwright *High-Dimensional Statistics*; Giraud; Foucart & Rauhut | 25, 27 |
| Prediction and conformal | Breiman et al. *CART*; Vovk, Gammerman & Shafer; Angelopoulos, Barber & Bates *Theoretical Foundations of Conformal Prediction* | 27 |
| Causal inference | Imbens & Rubin; Hernán & Robins *What If*; Pearl *Causality*; Pearl, Glymour & Jewell; Rosenbaum; Morgan & Winship; Peters, Janzing & Schölkopf; Ding; Wager; Chernozhukov et al.; Angrist & Pischke; Cunningham; Cattaneo, Idrobo & Titiunik; Manski | 28–30 |
| Time series | Brockwell & Davis; Hamilton; Shumway & Stoffer; Box, Jenkins, Reinsel & Ljung; Durbin & Koopman; Harvey; Hyndman & Athanasopoulos; Tsay; Percival & Walden | 31 |
| Spatial | Cressie; Cressie & Wikle; Stein; Banerjee, Carlin & Gelfand; Diggle; Rue & Held; Rasmussen & Williams | 32 |
| Survival | Kalbfleisch & Prentice; Klein & Moeschberger; Andersen, Borgan, Gill & Keiding; Fleming & Harrington; Aalen, Borgan & Gjessing; Therneau & Grambsch | 33 |
| Surveys and missing data | Cochran; Lohr; Särndal, Swensson & Wretman; Kish; Little & Rubin; van Buuren; Carroll et al. *Measurement Error*; Dwork & Roth | 34 |
| Sequential | Wald; Siegmund; Jennison & Turnbull; Tartakovsky et al.; Shafer & Vovk; Ramdas & Wang *Hypothesis Testing with E-values* | 35 |
| Data analysis and history | Tukey *EDA*; Cleveland; Tufte; Freedman, Pisani & Purves; Stigler (*History of Statistics*, *Seven Pillars*); Hald; Hacking; Salsburg; McGrayne | 1, throughout |

## Shared code and the Chinese edition (planned)

`explainer/stats/` will hold the series' instruments: the World, the Coverage Board, the Museum, statkit, chapter
cards with the timeline, the series map, and payoff and reference cards. The text helpers and the lecture set pieces
are shared with the other two series. Chinese narration will live in `videos/stats/statsN/narration_zh.json`,
on-screen text in `videos/stats/stats_text_zh.json`, and terms in `STATS_ZH_GUIDE.md`, the same way as *AI, Built*.
