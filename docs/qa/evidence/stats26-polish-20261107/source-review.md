# Part 26 scientific source review

Read the README, solutions/glossary, manifest, all fourteen compute items, Bayesian kit and all fifteen chapters in order. All fourteen items were recomputed; the final prior plot and coverage items were recomputed after refinements. All fifteen scenes import. Twenty-four focused checks pass, including Bayesian kit and shared Monte Carlo Board tests.

Corrections include:
- Replace the truncated tau posterior with a checked wide grid and independent infinite-range integration. For three schools, the flat-tau median is 23.0486, the 95th percentile 285.2375 and 32.86% of the posterior lies above 40. The former median 13.7 was a truncation artifact. Conditional Gaussian draws are exact; the tau inverse CDF is a finite numerical approximation. Prior comparisons use density per log10 tau on a logarithmic plot.
- Integrate Bernstein-von Mises total-variation distance over the full positive support and include the approximating normal's negative mass. Separate regular fixed-dimensional results from increasing-dimensional settings and avoid universal higher-order rate claims.
- Restrict Bartlett's minimum to the specified normal prior family, use integer sample sizes in Lindley's curve, qualify the Sellke–Bayarri–Berger alternative class and prior odds, retain prior constants in Bayes factors/BIC discussions, and qualify the iid PEAR likelihood.
- Compute decision information values by normal-mixture integration and a pilot decision boundary, replacing in-sample binned optimization. EVPI 2.20472 and EVSI 1.23280 satisfy independent single-normal and limiting-information references.
- Replace a bootstrap/moment negative-binomial check with a proper joint posterior for log mean and log shape, check grid refinement and boundary mass, distinguish zero simulation exceedances from zero probability, and separate conditional risk priors from marginal binary prediction.
- Calculate interval-coverage Monte Carlo error across 1,000 independent datasets rather than treating eight correlated intervals within each dataset as independent. Coverage is 94.7375%, 31.9250% and 93.7625%; hierarchical fixed-World coverage is not guaranteed by prior-averaged Bayesian calibration. The optional shared Board field preserves these errors through save/load and future cumulative boards.
- Qualify finite exchangeability, conjugacy parameterizations, inverse-gamma concentration, discrete MAP under zero-one loss, Savage/Wald/Cox assumptions, stopping rules, SBC and diagnostic limitations. DP conjugacy is conditional on the direct latent draws in mixture models; stick plots preserve remaining mass.
- Clip curve segments geometrically, preserve gaps, keep dashed curves as VMobjects, and add context headings at narration transitions.

Eight-school observations and standard errors independently match the Stan example-models source (receipt attached). PEAR figures were reconciled with the repository Museum only. Numerical references include direct integration over the population mean, infinite-range tau integration, normal-mixture information, high-precision beta-binomial evidence, exact-support TV integrals and independent-dataset coverage error.

English render inspection is the next gate. Chinese narration/caption tables, continuous listening and final narrated masters remain open.
