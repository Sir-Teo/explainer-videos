# Part 28 scientific source review

Read the README, solutions/glossary, manifest, all sixteen compute items, model-selection kit and all thirteen chapters in order. Recomputed all sixteen inputs and repeated the final school LOO calculation with paired refit contributions. All thirteen scenes import. Nineteen numerical/reference checks pass, including an independent scikit-learn pipeline; the statistics-qa extra declares the testing dependencies.

Corrections include:
- A proper independent-effect prior and an analytic held-out predictive reference. The former flat independent priors made whole-school LOO undefined. With N(0,100²) priors, exact LOO is −44.3261 while PSIS is −36.4602 and WAIC −33.9138: neither approximation is a trustworthy ranking without the check. The hierarchy uses Part 26's wider continuous-CDF grid and agrees with independent Gaussian-contrast integration.
- Paired LOO model differences from refit contributions, and paired held-out case-loss errors for prostate predictors. Overlapping LOO PITs retain a descriptive KS distance without invalid iid p-values or claims that flat histograms prove calibration.
- Fold-specific centering/scaling for penalized regression, validated with an independent scikit-learn pipeline; safeguarded Poisson likelihood updates; covariance degrees-of-freedom estimates with Monte Carlo error.
- Singular evidence with nonuniform grids resolving both crossing axes and explicit refinement bounds below 0.0011 log-evidence units. The regular comparator integrates its full declared prior, checked against independent double quadrature.
- Fixed N(-2,1)/N(2,1) candidates matching the stated M-open example and selection of a single candidate on training data, rather than held-out scores. Normalized criterion weights over searched candidates are not model-size posterior probabilities.
- Correct scopes for fixed-design optimism, lasso active-count degrees of freedom, Cp/AICc/TIC, BIC consistency and unit-information approximations, CV conditional-error results, singular-model RLCTs, coding/NML existence, BMA optimality, splitting and polyhedral/fission guarantees.
- A coherent known-SE normal cutoff for the selection example (conditional coverage 0.75973), excess-risk rather than noisy total-risk labels and Monte Carlo error bars in the subset race. Squared error of the predictive mean is proper but not strictly proper over full distributions; PIT flatness and climatology claims are qualified.
- Geometric curve clipping, full-range CV displays, source-specific narration context headings and corrected historical/computational qualifiers.

All 97 ESL prostate rows, eight predictors and response match at the Museum's stated precision, and the 67/30 split matches exactly. Historical Freedman and subset-race calculations are explicitly teaching simulations, not archival reproductions. The eight-school source was independently reconciled in Part 26.

English render inspection is the next gate. Chinese narration/caption tables, continuous listening and final narrated masters remain open.
