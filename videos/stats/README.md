# Statistics, Built (统计学，从零搭建)

**Status: in production.** Parts 1–47 are written in English (12–16 chapters each):
- *The Shape of Data*, about an hour;
- *Chance, Counted*, about 74 minutes, with the exact probability engine `explainer/stats/prob.py`;
- *The Family of Distributions*, about 55 minutes, with the family-tree instrument `FamilyTree`;
- *Matrices for Statistics*, about 55 minutes, with the projection lab;
- *Many Variables at Once*, about 50 minutes, with the Gaussian slicer (`GaussianSlicer`) and a Pólya urn machine;
- *The Laws of Averages*, about 55 minutes, with the Galton board (`GaltonBoard`);
- *Randomness on Demand*, about 50 minutes, with `statkit.random` (generators, samplers and the simulation-study harness);
- *From Sample to Population*, about 50 minutes, which opens the Coverage Board with its first seven rows;
- *Estimation*, about 70 minutes, with the tank factory game (`statkit.estimation`) and the `TankFactory`;
- *Significance*, about 60 minutes, with the permutation machine (`PermutationMachine`) and `statkit.tests`;
- *Honest Intervals*, about 50 minutes, with `statkit.intervals` and the interval rain (`IntervalRain`);
- *Least Squares*, about 50 minutes, with `statkit.ols` and the influence probe (`InfluenceProbe`);
- *Experiments by Design*, about 79 minutes, with `statkit.design` (the field-trial simulator and the island bakery) and the field plot (`FieldPlot`);
- *Counts and Categories*, about 52 minutes, with `statkit.glm` and the Challenger dashboard (`ChallengerDashboard`);
- *First Bayes*, about 50 minutes, with `statkit.bayes` and Bayes's billiard table (`BilliardTable`);
- *Without Assumptions*, about 56 minutes, with `statkit.ranks`, `statkit.bootstrap`, the bootstrap resampler (`BootstrapResampler`) and the kernel sum (`KernelSum`);
- *Time Series*, about 51 minutes, with `statkit.ts`, the correlogram (`Correlogram`), the root plane (`RootPlane`) and Yule's pendulum (`YulePendulum`);
- *Who Did You Ask?*, about 51 minutes, with the World's survey block, `statkit.survey` and the island map (`IslandMap`);
- *Learning from Data*, about 50 minutes, with `statkit.learn` and the ℓ₁ geometry (`L1Geometry`);
- *The Analysis*, the BSc capstone, about 55 minutes, on NHANES 2017–2018, with the capstone pipeline, `statkit.capstone`, design-based regression, and the World's health block;
- *Optimization for Statistics*, about 51 minutes, with `statkit.optim` and the landscape (`Landscape`);
- *Likelihood in Depth*, about 51 minutes, with `statkit.mle`, the likelihood landscape (`LikelihoodLandscape`) and Weldon's crabs;
- *The Linear Model in Depth*, about 52 minutes, with `statkit.ols` II, the digits board (`DigitsBoard`), the World's schools, Longley and Hubble;
- *Generalized Linear Models*, about 51 minutes, with `statkit.glm` II, the dose–response panel (`DoseResponse`), the World's doctor visits and Bliss's beetles;
- *Borrowing Strength: Shrinkage and Mixed Models*, about 51 minutes, with `statkit.shrink`, `statkit.mixed`, the shrinkage plot (`ShrinkagePlot`), the World's hospitals and Efron and Morris's hitters;
- *Bayesian Data Analysis*, about 51 minutes, with `statkit.bayes` II, the τ explorer (`TauExplorer`), Rubin's eight schools and the PEAR data;
- *Bayesian Computation*, about 51 minutes, with `statkit.ppl` (a probabilistic programming language with NUTS), the puck on the surface (`PuckSurface`) and the eight schools' funnel;
- *Which Model?*, about 50 minutes, with `statkit.select`, the model-selection bench (`CriterionBench`) and Stamey's prostate data;
- *Smoothing*, about 50 minutes, with `statkit.smooth`, the spline spectrum (`SplineSpectrum`), Old Faithful, the motorcycle crash and New York's ozone;
- *Robust Statistics*, about 51 minutes, with `statkit.robust`, the estimator rail (`EstimatorRail`), Newcomb's light, the CYG OB1 stars and Hawkins–Bradu–Kass;
- *Multivariate Analysis*, about 52 minutes, with `statkit.multi`, the map from distances (`DistanceMap`), Hartigan's European road distances, Fisher's irises, the 24 tests, the savings data and US arrests;
- *Sparsity*, about 56 minutes, with `statkit.sparse`, the phantom (`PhantomPanel`), the diabetes data of the LARS paper and the Shepp–Logan phantom;
- *Thousands of Questions*, about 53 minutes, with `statkit.multiple`, the p-hacking simulator, the p-value sea (`PValueSea`), the World's gene study and the prostate microarray;
- *Prediction with Guarantees*, about 82 minutes, with `statkit.conformal`, `statkit.ppi`, the score ladder (`ScoreLadder`) and the Wisconsin breast cancer data;
- *What If? Experiments and Potential Outcomes*, about 56 minutes, with the World's clinic trial and epidemic, `statkit.causal` (I), the science table (`ScienceTable`), and the Salk, ISIS-2 and CAST trials;
- *Causes Without Experiments*, about 56 minutes, with `statkit.causal` (II), the causal graph (`CausalGraph`), and the NSW job-training data;
- *Natural Experiments*, about 60 minutes, with the World's schooling survey, scholarship and rollout, `statkit.quasi`, the cutoff lens (`CutoffLens`), Snow's Table IX, Card and Krueger's means and the Prop 99 panel;
- *Time Series in Depth*, about 51 minutes, with `statkit.ts` (II), the Kalman ellipses (`KalmanEllipses`), Toussoun's Nile minima, the Nile's flow, the DAX and US macro data;
- *Space*, about 50.6 minutes, with `statkit.spatial`, the field surface (`FieldSurface`), the World's pollution field, Meuse's heavy metals and Snow's map;
- *Time to Event*, about 50.4 minutes, with `statkit.survival`, the KM staircase (`KMStaircase`), the World's cohort, Gehan's 6-MP trial, Mayo's PBC trial, the Stanford heart transplants and MGUS;
- *What You Didn't See*, about 51.2 minutes, with `statkit.mi`, the mask grid (`MaskGrid`), the World's survey masks and opt-in poll, New York's ozone, NHANES's sodium recalls and Mroz's women;
- *The Comprehensive Exam*, about 59.1 minutes, with the MSc problem bank, the exam card (`ExamCard`), the World's ministry block (a cluster trial to design and a salt-substitute survey to analyse), and twelve exam problems on Bliss, Longley, the eight schools, ozone, Old Faithful, Newcomb, Stamey, the prostate microarray and the 6-MP trial;
- *Measure-Theoretic Probability*, about 60.7 minutes, with `statkit.limits` (the weak-convergence lab), the convergence lab (`ConvergenceLab`), Bortkiewicz's horse kicks, Bernoulli's urn, the DAX and Port Pirie's sea levels;
- *Martingales, Markov Chains and Brownian Motion*, about 51.4 minutes, with `statkit.chains`, the betting paths (`BettingPaths`), Markov's *Onegin* and the 6-MP trial;
- *The Theory of Estimation*, about 65.7 minutes, with `statkit.decision`, the risk-set explorer (`RiskSet`), Ruggles and Brodie's tanks, Efron and Morris's hitters and Efron and Hastie's insurance claims;
- *The Theory of Testing and Confidence*, about 51.9 minutes, with `statkit.testing`, the Neyman-structure visualizer (`NeymanSlices`), Old Faithful, ISIS-2, the lady tasting tea and Bliss's beetles;
- *Asymptotic Statistics*, about 50.5 minutes, with `statkit.asymptotics`, the risk-bump explorer (`RiskBump`) and Newcomb's light.

Their instruments are in `explainer/stats/`; narration and the Chinese edition follow. The chapter-by-chapter plan and the production standard are in [`SYLLABUS.md`](SYLLABUS.md).

This series is a whole education in statistics on video: **a bachelor's degree, a master's, and a PhD**. It runs to
sixty-five parts in five stages, in English and Chinese, and assumes calculus at the start. By the end it reaches the
research frontier: selective and anytime-valid inference, high-dimensional asymptotics, optimal transport, causal
machine learning, privacy, and the statistics of AI.

Each part is a **50–60 minute lecture**, about 60 hours in all. Each one derives its mathematics on screen, every step
with its reason. It tells the history of the ideas, builds a working tool or toy, and checks every claim with a real
computation. The rigour rises with the stage: calculus-level proofs in the bachelor's stages, measure-theoretic
theorem–proof in the PhD core, research papers in the last stage. The videos are named `stats1` … `stats65`, in
`videos/stats/statsN/`.

## The story

**Graunt's question.** In 1662 John Graunt, a London haberdasher, read half a century of weekly *Bills of
Mortality*. From them he worked out things about the living city that nobody had counted: how many people lived
there, how many boys were born for every girl, how long a Londoner could expect to live. Statistics is his question
made precise: *what can we know about what we cannot see, from what we can, and how often will we be wrong?*

The series tells three stories at once:

1. **A student's journey.** The first stage asks what a histogram is. The last stage writes a dissertation. Every
   stage ends at a milestone of a real degree: the capstone analysis (BSc), the comprehensive exam (MSc), the
   qualifying exam (PhD candidacy) and the dissertation (PhD).
2. **The history of the field, moving forward as the level rises.** The bachelor's stages cover the classical era,
   from Graunt to Fisher and Neyman. The master's covers the methods of 1950–2000: the bootstrap, GLMs, MCMC, the
   lasso and causal inference. The PhD core covers the theory that justified them, from Le Cam and empirical
   processes to minimax theory. The research stage covers the work of the last fifteen years.
3. **One promise, tested.** Every method promises something: an unbiased estimate, a 5% false-alarm rate, a 95%
   interval, a controlled false discovery rate. The series asks which promises are kept, under what assumptions, and
   what breaks them. It answers by measuring, on the Coverage Board.

## The five stages

| Stage | Parts | Level | Rigour | After it you can |
|---|---|---|---|---|
| **I. Bachelor's: Foundations** (years 1–2) | 1–10 | calculus and a first look at matrices | every result derived; proofs at the level of Rice or Casella & Berger | reason with probability, estimate, test and simulate |
| **II. Bachelor's: Methods** (years 3–4) | 11–20 | Stage I | full derivations; practice on real data | analyse a dataset start to finish: regression, design, categorical data, Bayes, resampling, time series, surveys, prediction |
| **III. Master's** | 21–42 | a BSc in statistics, or Stages I–II | matrix calculus, optimization, asymptotics stated precisely | use and justify the modern toolkit: likelihood, linear and generalized models, mixed models, Bayesian computation, model choice, smoothing, robustness, multivariate and sparse methods, multiple testing, conformal prediction, causal inference, time series, spatial, survival and missing data |
| **IV. PhD core** (qualifying-exam year) | 43–55 | an MSc, plus the real analysis of *Analysis, Built* Parts 1–6 | measure-theoretic; exact conditions, with counterexamples showing why each is needed | prove: probability, estimation and testing theory, asymptotics, empirical processes, semiparametric efficiency, minimax lower bounds, high-dimensional probability and statistics, Bayesian asymptotics, learning theory |
| **V. PhD research** | 56–65 | Stage IV | research papers, with open problems | read and extend the frontier: selective, distribution-free and anytime-valid inference, high-dimensional asymptotics, robustness and shift, optimal transport, causal frontiers, privacy and fairness, statistics for AI; then write a dissertation |

**Entry points.** Each stage opens with a placement chapter: what the stage assumes, with links back to the parts
that taught it. A viewer with a statistics degree can start at Part 21, and a PhD student at Part 43.

## The devices that hold it together

1. **The World** (`explainer.stats.world`). A seeded, simulated population of one million residents in households,
   towns and regions. It holds heights inherited through families, skewed incomes, schools, a disease with a
   screening test, a treatment taken for confounded reasons with *both* potential outcomes recorded for everyone,
   an instrument, a staggered policy, a scholarship cutoff, survival times, a spatial pollution field, daily time
   series with change points, survey response propensities, missingness mechanisms, data-entry errors, and 10,000
   genetic markers with 20 real effects. In real life the truth is never visible. In the World it is, so every
   estimator, test and interval in the series can be graded against it. It is always labelled `simulated` on screen.
2. **The Coverage Board** (`explainer.stats.board`). This is the series' scoreboard. Each interval or test is run
   thousands of times on the World. The board records its actual coverage (or false-alarm rate) against the nominal
   95% (or 5%), with Monte Carlo error bands. Green means the promise is kept, red means it is broken, blue means it
   is conservative. There are more than a hundred rows by the end. Some are classic failures: the Wald binomial interval,
   peeking, heteroskedasticity, selection, weak instruments, staggered adoption, high-dimensional logistic
   regression, nonparametric credible bands. Others show honest methods keeping the promise: conformal prediction,
   confidence sequences, debiased and orthogonalized estimators.
3. **The Spiral.** The central results are met three times, each time sharper. The CLT, for example: by moment
   generating functions in Part 6, as the delta method and the bootstrap in Parts 16 and 22, and then as
   Lindeberg–Feller, Stein's method and Donsker in Parts 43 and 48. Each return opens with an **upgrade card**: the
   earlier statement, what it quietly assumed, and what will now be proved.
4. **The Transcript.** Each part is a "course" on an on-screen transcript. Stage milestones show what has been
   earned: the BSc (Part 20), the MSc (Part 42), candidacy (Part 55) and the PhD (Part 65).
5. **The Museum** (`explainer.stats.museum`). Real historical data, transcribed from the original publication with
   its source on screen. Examples: Graunt (1662), Arbuthnot (1710), Snow (1855), Galton (1886), Weldon's crabs
   (1893), Bortkiewicz (1898), Student (1908), Bliss's beetles (1935), the Salk trial (1954), Freireich (1963),
   Efron–Morris (1975), the eight schools (1981), Challenger (1986).
6. **statkit, built** (`explainer/stats/kit/`). The series writes its own small, readable statistics library, one
   piece per part, from the first random number generator to NUTS, double machine learning, Sinkhorn and confidence
   sequences. Each module is checked against SciPy and statsmodels in `tests/`.
7. **The timeline strip, 1650–2030**, lit on every chapter card; **payoff cards** ("where this comes back");
   **cross-series links** to *Analysis, Built* (measure, Hilbert space, Fourier) and *AI, Built* (information,
   learning theory, diffusion).

## How it looks

The series draws in the manner of 3Blue1Brown, with *AI, Built*'s instruments and *Analysis, Built*'s derivation
ladder. New statistics instruments go in `explainer/stats/viz.py` (list in the syllabus, §1).

* **Colour is meaning, everywhere.** The true parameter θ is always gold and the estimate θ̂ always blue. Data are
  white, the null distribution grey, the alternative teal. The prior is purple, the likelihood green, the posterior
  orange. Residuals are red, treated units coral and controls sky blue, and missing values are hollow.
* **Sampling is shown, not stated.** The `SamplingMachine` builds sampling distributions live. `IntervalRain` drops
  intervals against the truth line, with the misses turning red.
* **Statistics as geometry.** Samples as vectors in Rⁿ with the camera orbiting: the mean as a projection, χ² as a
  squared length, regression as projection, ANOVA as Pythagoras. Conditional expectation as projection in L²,
  efficient influence functions as projections onto tangent spaces, and the lasso's diamond meeting the contours.
* **Landscapes and flows.** Likelihood surfaces with the test trinity drawn on them; HMC's puck; Marchenko–Pastur's
  bulk and the BBP spike; Wasserstein geodesics moving mass; Langevin dynamics as a gradient flow.
* **Live quantities.** Bandwidth, prior strength, shrinkage, contamination, privacy budget and selection threshold
  are value trackers, so the viewer sees each estimate respond.
* **Real numbers.** Everything plotted comes from the part's `compute.py`. Tags say which kind it is: `computed`,
  `simulated`, `historical data` (with source), `illustrative` or `schematic`.

## The parts

| # | Part | Hook | Mathematics | Built |
|---|---|---|---|---|
| **I** | **Bachelor's: Foundations** | | | |
| 1 | The Shape of Data | Graunt's bills, 1662 | summaries as loss minimizers, ECDF, QQ, transformations, correlation as a cosine, Anscombe, Simpson | the World; a same-statistics morph |
| 2 | Chance, Counted | the problem of points, 1654 | axioms, conditioning, Bayes, independence, random variables, expectation, Dutch books | an exact probability engine |
| 3 | The Family of Distributions | Bortkiewicz's horse kicks | binomial→Poisson, three derivations of the normal, χ²/t/F, order statistics, generating functions, the family tree | the family-tree explorer |
| 4 | Matrices for Statistics | the hat matrix's two eigenvalues | projections, idempotents, trace tricks, PSD order, spectral and SVD, Schur, Woodbury, Kronecker, matrix calculus, quadratic forms | a projection lab |
| 5 | Many Variables at Once | Galton's ellipses, 1886 | conditional expectation as projection, Eve's law, the multivariate normal, conditioning, regression to the mean, copulas, exchangeability | a Gaussian slicer; Pólya's urn |
| 6 | The Laws of Averages | Galton's ox, 1907 | Markov and Chebyshev, the weak law, the CLT by MGFs, the delta method, "n ≥ 30" tested, heavy tails, extremes | a Galton board |
| 7 | Randomness on Demand | von Neumann's "state of sin", 1951 | PRNGs and RANDU, samplers, Monte Carlo error, simulation-study design, Markov chains, Metropolis | statkit.random; the simulation-study harness |
| 8 | From Sample to Population | Student at Guinness, 1908 | sampling distributions, n − 1 as dimension, Fisher's geometry, χ², t, F, MSE, plug-in | Student's card deck; the Board's first rows |
| 9 | Estimation | the German tank problem | method of moments, maximum likelihood, bias and MSE, sufficiency, Rao–Blackwell, Fisher information, Cramér–Rao | the tank factory game |
| 10 | Significance | Arbuthnot 1710; the lady tasting tea | p-values, Neyman–Pearson, the likelihood ratio, z/t/χ²/exact tests, power, Welch, the peeking problem | a permutation machine |
| **II** | **Bachelor's: Methods** | | | |
| 11 | Honest Intervals | the broken Wald interval | Neyman's construction, pivots, inversion, the binomial family, Fieller, prediction and tolerance intervals | the Coverage Board, formally |
| 12 | Least Squares | Gauss finds Ceres, 1801 | projection, Gauss–Markov, t and F, FWL, diagnostics, robust standard errors | statkit.ols; an influence probe |
| 13 | Experiments by Design | Fisher at Rothamsted, 1919 | randomization, ANOVA geometry, blocking, factorials, fractional factorials, response surfaces, A/B tests | a field-trial simulator |
| 14 | Counts and Categories | the Challenger O-rings, 1986 | logistic and Poisson regression, odds ratios, tables, Simpson's paradox, case–control | a Challenger dashboard |
| 15 | First Bayes | Bayes's billiard table, 1763 | conjugacy, priors, posteriors, credible and predictive intervals, grids, Metropolis by hand | the billiard table |
| 16 | Without Assumptions | Efron's law schools, 1979 | permutation and rank tests, Wilcoxon and Mann–Whitney, the jackknife, the bootstrap, cross-validation | statkit.bootstrap, statkit.ranks |
| 17 | Time Series | Yule's nonsense correlation, 1926 | stationarity, ARMA, ACF/PACF, Box–Jenkins, forecasting, smoothing, seasonality | statkit.ts (I) |
| 18 | Who Did You Ask? | the *Literary Digest*, 1936 | SRS and the FPC, stratification, clusters, PPS, Horvitz–Thompson, raking, Meng's identity | the World's polling firm |
| 19 | Learning from Data | who wrote the disputed *Federalist* papers? | prediction error, CV, k-NN, naive Bayes vs logistic, trees, ridge and lasso, ROC | statkit.learn |
| 20 | **The Analysis** (BSc capstone) | a public health survey | a complete, reproducible analysis: question, design, cleaning, EDA, model, checks, inference, report, ethics | the capstone report; the BSc problem set |
| **III** | **Master's** | | | |
| 21 | Optimization for Statistics | Dantzig's "homework", 1939 | convexity, duality and KKT, Newton and scoring, MM and EM, coordinate descent, proximal methods, LP, ADMM, SGD | statkit.optim |
| 22 | Likelihood in Depth | Pearson's crabs, 1894 | MLE asymptotics, profile likelihood, Neyman–Scott, EM, misspecification and the sandwich, the likelihood principle | statkit.mle |
| 23 | The Linear Model in Depth | Longley's benchmark, 1967 | the general linear hypothesis, Cochran, GLS, heteroskedasticity and cluster theory, errors in variables, quantile regression, numerics | statkit.ols (II) |
| 24 | Generalized Linear Models | Bliss's beetles, 1935 | exponential dispersion families, IRLS, deviance, quasi-likelihood, separation and Firth, GEE, ordinal models | statkit.glm |
| 25 | Borrowing Strength | Efron–Morris baseball, 1975 | James–Stein via SURE, empirical Bayes, random effects, BLUP, REML, GLMMs, small areas, meta-analysis | statkit.mixed; a league table |
| 26 | Bayesian Data Analysis | the eight schools, 1981 | hierarchical Bayes, priors, Bernstein–von Mises, Bayes factors, Lindley's paradox, checking, workflow | statkit.bayes |
| 27 | Bayesian Computation | Los Alamos, 1953 | importance sampling, MH, Gibbs, HMC, NUTS, diagnostics, SMC, VI, ABC, SBC | a tiny probabilistic programming language |
| 28 | Which Model? | Freedman's paradox, 1983 | optimism, AIC and BIC derived, CV and GCV, PSIS-LOO, WAIC, MDL, stacking | a model-selection bench |
| 29 | Smoothing | Old Faithful's two humps | KDE and spline theory, local polynomials, RKHS, wavelets, GAMs, shape constraints | statkit.smooth |
| 30 | Robust Statistics | Tukey's contaminated normal, 1960 | Pitman efficiency and the 0.864 bound, influence, breakdown, Huber's minimax, LTS, MM, MCD, median-of-means | statkit.robust |
| 31 | Multivariate Analysis | a map from a table of distances | Wishart, Hotelling, PCA, factor analysis, CCA, LDA, MDS, clustering and mixtures, graphical models | statkit.multi |
| 32 | Sparsity | Candès's phantom, 2004 | ridge, ℓ1 geometry, coordinate descent and LARS, the penalty zoo, compressed sensing, debiased lasso, matrix completion | statkit.sparse |
| 33 | Thousands of Questions | the dead salmon in the scanner | FWER, BH proved, q-values, local fdr, knockoffs, forking paths, replication, publication bias | a p-hacking simulator |
| 34 | Prediction with Guarantees | Breiman's two cultures, 2001 | forests and boosting as estimators, what CV estimates, calibration, split and jackknife+ conformal, PPI | statkit.conformal |
| 35 | What If? | the Salk polio trial, 1954 | potential outcomes, randomization and Neyman inference, Lin's adjustment, noncompliance and LATE, interference, sequential trials | a trial with both outcomes visible |
| 36 | Causes Without Experiments | LaLonde's job training, 1986 | DAGs, back-door and front-door, propensity scores, IPW, AIPW, DML, CATE, sensitivity, smoking | statkit.causal |
| 37 | Natural Experiments | Snow's Grand Experiment, 1854 | IV, weak instruments, RD, DiD, staggered adoption, synthetic control, SDID, bounds | statkit.quasi |
| 38 | Time Series in Depth | Hurst's Nile, 1951 | spectra, unit roots and Dickey–Fuller, cointegration, GARCH, long memory, Kalman, VARs, particle filters | statkit.ts (II) |
| 39 | Space | Krige's gold, 1951 | variograms, kriging, Matérn, Vecchia, GMRF and SPDE, areal models, point processes, GPs | statkit.spatial |
| 40 | Time to Event | Freireich's 6-MP trial, 1963 | censoring, Kaplan–Meier, Greenwood, log-rank, Cox, counting processes, competing risks, frailty | statkit.survival |
| 41 | What You Didn't See | Wald's bombers, 1943 | Rubin's mechanisms, EM and FIML, multiple imputation, IPW/AIPW, Heckman, MNAR sensitivity, measurement error, MRP | statkit.mi |
| 42 | **The Comprehensive Exam** | the consulting client | worked comprehensive-exam problems; two consulting cases from design to report | the MSc problem bank |
| **IV** | **PhD Core** | | | |
| 43 | Measure-Theoretic Probability | Hilbert's sixth problem, 1900 | π–λ and extension, integration theorems, independence and 0–1 laws, Kolmogorov's SLLN, weak convergence, characteristic functions, Lindeberg–Feller, Stein's method, infinitely divisible laws, large deviations | a weak-convergence lab |
| 44 | Martingales, Markov Chains and Brownian Motion | Markov vs Nekrasov, 1913 | conditional expectation (Radon–Nikodym), Doob's theorems, uniform integrability, reverse martingales, martingale CLT, Harris chains and drift conditions, coupling, Brownian motion, Donsker, LIL, counting processes | a coupling and mixing lab |
| 45 | The Theory of Estimation | Stein's 1956 shock | decision theory, complete classes, exponential families as convex duality, sufficiency and completeness, Basu, equivariance, Stein, Brown's recurrence theorem, empirical Bayes theory | a risk-set explorer |
| 46 | The Theory of Testing and Confidence | the Behrens–Fisher problem | Neyman–Pearson in general, MLR, UMPU via Neyman structure, invariance and Hunt–Stein, Wilks and Chernoff's boundary, optimal confidence sets, Gleser–Hwang, closed testing, conditional inference | a Neyman-structure visualizer |
| 47 | Asymptotic Statistics | Hodges' superefficiency, 1951 | M/Z-estimators, influence functions, U-statistics, LAN, contiguity, Le Cam's lemmas, Hájek's theorems, efficiency of tests, bootstrap theory, Edgeworth, saddlepoints | a risk-bump explorer |
| 48 | Empirical Processes | Doob's heuristic, 1949 | Glivenko–Cantelli and Donsker classes, symmetrization, VC, entropy and bracketing, chaining, Talagrand, the functional delta method, rates and cube-root asymptotics | statkit.empirical |
| 49 | Semiparametric Efficiency | adaptive estimation (Stein 1956; Bickel 1982) | tangent spaces, pathwise derivatives, efficient influence functions, bounds, one-step and TMLE, double robustness, DML theory, higher-order influence functions | statkit.semipar |
| 50 | Minimax Theory | the speed limit of nonparametrics (Stone 1980) | the Gaussian sequence model and Le Cam equivalence, Pinsker's theorem, Le Cam/Fano/Assouad, adaptation (Lepski), minimax testing and higher criticism, statistical–computational gaps | a lower-bound workbench |
| 51 | High-Dimensional Probability | the sphere's equator | sub-Gaussian and sub-exponential tools, Gaussian and Talagrand concentration, ε-nets, matrix Bernstein, chaining, Slepian and Gordon, Gaussian widths, statistical dimension | statkit.hdp |
| 52 | High-Dimensional Statistics | PCA finds structure in noise | oracle inequalities, the primal–dual witness, decomposable regularizers, low-rank recovery, covariance and Davis–Kahan, random matrices (MP, BBP, TW), sparse PCA | the random-matrix lab |
| 53 | Bayesian Asymptotics and Nonparametric Bayes | Diaconis & Freedman's inconsistency, 1986 | Doob and Schwartz, contraction rates, parametric and semiparametric BvM, DP and GP priors, credible-band coverage, spike-and-slab and horseshoe theory, Gibbs posteriors | statkit.bnp |
| 54 | Statistical Learning Theory | Vapnik & Chervonenkis, 1971 | uniform convergence, VC and Rademacher, localization, margins, PAC-Bayes, stability, online learning, calibrated surrogates, benign overfitting | statkit.slt |
| 55 | **The Qualifying Exam** | the night before | twelve classic qualifying-exam problems, solved on screen | the PhD problem bank |
| **V** | **PhD Research** | | | |
| 56 | Inference After Selection | the winner's curse | PoSI, conditional selective inference, randomization and carving, data fission and thinning, knockoff theory, conformal selection, inference on winners | statkit.selective |
| 57 | Distribution-Free Inference | Bahadur & Savage's impossibility, 1956 | exchangeability, full/split/jackknife+ conformal proofs, impossibility theorems, conditional guarantees, beyond exchangeability, conformal p-values | statkit.conformal (II) |
| 58 | Anytime-Valid Inference and Adaptive Experiments | Wald's SPRT, 1943 | the SPRT, alpha spending, test martingales, e-values, composite nulls, confidence sequences, game-theoretic probability, e-BH, change points, bandits and off-policy inference | statkit.sequential |
| 59 | High-Dimensional Asymptotics | a χ² that is not (Sur & Candès 2019) | the proportional regime, free probability, exact ridge risk, AMP and state evolution, CGMT, replica predictions, random features | an AMP solver |
| 60 | Robustness and Distribution Shift | ImageNet's new test set (Recht et al. 2019) | depth, filtering and SoS, list decoding, covariate and label shift, DRO, invariance and anchor regression, transfer minimax | statkit.shift |
| 61 | Optimal Transport in Statistics | Monge's earthworks, 1781 | Kantorovich duality, Wasserstein geometry, empirical rates, entropic OT and Sinkhorn, map estimation, barycenters, multivariate ranks, Langevin as a gradient flow | statkit.ot |
| 62 | Frontiers of Causal Inference | when to start HIV treatment | ID theory, sensitivity models, proximal inference, interference, policy learning, dynamic regimes, causal discovery theory, data fusion | statkit.causal (II) |
| 63 | Privacy and Fairness | re-identification from ZIP, sex and birth date | DP and its accountants, DP as hypothesis testing, the cost of privacy, private inference, the 2020 Census, fairness criteria, impossibility, multicalibration | statkit.privacy |
| 64 | Statistics in the Age of AI | a leaderboard: 85.2% vs 84.7% | evaluation error bars, arenas and IRT, the reusable holdout, PPI with model labels, model collapse, conformal for LLMs, watermark tests, SBI | statkit.evals |
| 65 | **The Dissertation** | back to Graunt | how statistical research is done, a mini-dissertation carried out on screen, the full Coverage Board, the reading list onward | the thesis |

## The Spiral: results met three times

| Result | First pass (BSc) | Second pass (MSc) | Third pass (PhD) |
|---|---|---|---|
| Laws of large numbers and the CLT | 6 (Chebyshev, MGFs) | 16, 22 (bootstrap, delta method in many dimensions) | 43, 44, 48 (Kolmogorov, Lindeberg–Feller, Stein's method, martingale CLT, Donsker) |
| Estimation and optimality | 9 (MLE, Cramér–Rao, Rao–Blackwell) | 22, 25 (asymptotics, James–Stein) | 45, 47, 49, 50 (complete classes, Le Cam–Hájek, semiparametric and minimax bounds) |
| Testing and intervals | 10, 11 | 22, 33 | 46, 56, 57, 58 |
| Regression | 12, 14 | 23, 24, 32 | 52, 59 |
| Bayes | 15 | 26, 27 | 53 |
| Resampling and ranks | 16 | 30 | 47, 48 |
| Prediction | 19 | 34 | 54, 57 |
| Causation | 1, 14 (Simpson), 13 (randomization) | 35–37 | 49, 62 |
| Dependence in time | 7, 17 | 38 | 44, 58 |
| Missing and selected data | 18 | 41 | 49, 56, 63 |

## Course map, for orientation

The stages cover what these programmes teach; course numbers and contents vary by year.

| Stage | Comparable courses |
|---|---|
| I | undergraduate probability (e.g. Harvard Stat 110, Berkeley Stat 134) and mathematical statistics (Harvard Stat 111, Berkeley Stat 135); linear algebra for statistics |
| II | regression, experimental design, categorical data, Bayesian statistics, nonparametrics, time series, sampling, statistical learning, a capstone |
| III | first-year MS and applied PhD sequences (e.g. Stanford STATS 305A–C, CMU 36-705) and electives (Bayesian, causal, survival, spatial, computing) |
| IV | PhD probability and theory (e.g. Stanford STATS 310A–C and 300A–C, Berkeley STAT 205A–B and 210A–B, CMU 36-709/710) |
| V | topics courses and reading groups |

## The bookshelf

| Stage | Main texts |
|---|---|
| I | Blitzstein & Hwang; Ross; Feller vol. 1; Rice; Casella & Berger; Wasserman *All of Statistics*; Freedman, Pisani & Purves; Tukey *EDA*; Harville *Matrix Algebra from a Statistician's Perspective* |
| II | Seber & Lee; Weisberg; Box, Hunter & Hunter; Montgomery; Agresti *Categorical Data Analysis*; Hoff; Efron & Tibshirani; Hollander, Wolfe & Chicken; Shumway & Stoffer; Brockwell & Davis; Hyndman & Athanasopoulos; Lohr; Cochran; James, Witten, Hastie & Tibshirani (ISLR); Gelman, Hill & Vehtari |
| III | Boyd & Vandenberghe; Lange *Optimization*; Pawitan; Christensen; Agresti *Foundations*; McCullagh & Nelder; Gelman & Hill; Gelman et al. *BDA3*; McElreath; Robert & Casella; Burnham & Anderson; Wand & Jones; Wood; Huber & Ronchetti; Maronna et al.; Anderson; Mardia, Kent & Bibby; Hastie, Tibshirani & Friedman (ESL); Hastie, Tibshirani & Wainwright; Efron *Large-Scale Inference*; Angelopoulos & Bates; Imbens & Rubin; Hernán & Robins; Pearl; Angrist & Pischke; Cunningham; Hamilton; Durbin & Koopman; Cressie; Rasmussen & Williams; Kalbfleisch & Prentice; Klein & Moeschberger; Little & Rubin; van Buuren |
| IV | Durrett; Billingsley *Probability and Measure* and *Convergence of Probability Measures*; Williams; Kallenberg; Meyn & Tweedie; Levin, Peres & Wilmer; Lehmann & Casella; Lehmann & Romano; Keener; Schervish; Berger; Ferguson; van der Vaart *Asymptotic Statistics*; Le Cam & Yang; van der Vaart & Wellner; Kosorok; Giné & Nickl; Bickel, Klaassen, Ritov & Wellner; Tsiatis; Tsybakov; Johnstone *Gaussian Estimation*; Polyanskiy & Wu; Vershynin; Boucheron, Lugosi & Massart; Wainwright *High-Dimensional Statistics*; Bühlmann & van de Geer; Bai & Silverstein; Ghosal & van der Vaart; Ghosh & Ramamoorthi; Shalev-Shwartz & Ben-David; Bach *Learning Theory from First Principles*; Mohri, Rostamizadeh & Talwalkar |
| V | Angelopoulos, Barber & Bates *Theoretical Foundations of Conformal Prediction*; Vovk, Gammerman & Shafer; Ramdas & Wang *Hypothesis Testing with E-values*; Shafer & Vovk; Jennison & Turnbull; Diakonikolas & Kane; Villani; Peyré & Cuturi; Panaretos & Zemel; Chewi, Niles-Weed & Rigollet *Statistical Optimal Transport*; Couillet & Liao; Pearl & Bareinboim's papers; Wager *Causal Inference*; Chernozhukov et al. *Applied Causal Inference Powered by ML and AI*; Dwork & Roth; Barocas, Hardt & Narayanan *Fairness and Machine Learning*; the primary papers on each part's reference card |
| History, throughout | Stigler (*The History of Statistics*, *Statistics on the Table*, *The Seven Pillars*); Hald; Hacking; Porter; Salsburg; McGrayne |

## Shared code and the Chinese edition (planned)

`explainer/stats/` will hold the series' instruments: the World, the Coverage Board, the Museum, the Transcript and
upgrade cards, statkit, chapter cards with the timeline, the series map, and payoff and reference cards. The text
helpers and lecture set pieces are shared with the other two series. Chinese narration will live in
`videos/stats/statsN/narration_zh.json`, on-screen text in `videos/stats/stats_text_zh.json`, and terms in
`STATS_ZH_GUIDE.md`, the same way as *AI, Built*.
