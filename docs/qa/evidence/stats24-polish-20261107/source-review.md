# Part 24 scientific source review

Every scene in the 14-chapter manifest, README and solutions, all 12 compute items, common helpers, the GLM kit and its existing reference tests were read. All computations were refreshed, all scenes imported and 19 numerical/reference checks passed.

- Checked local weighted-QR IRLS with explicit candidate recomputation, line-search failure and convergence handling against statsmodels for all three Bliss links and an overshooting Poisson start.
- Replaced dense exchangeable inversions with their analytic rank-one form and recorded any positive-definiteness constraints. Independence and exchangeable estimates and robust covariances match statsmodels.
- Corrected the finite-World GEE targets: 0.391567 for independence and 0.378283 for exchangeable under the approximate logistic mean. Coverage uses the corresponding target; exchangeable coverage is 95.8%. Mean, sampling and asymptotic requirements are explicit.
- Corrected prior-weight variance, information and sufficiency formulas; inverse-link signs/scales, unscaled deviance versus LR scaling, the NB2 score and a computed 1924.0 overdispersion LR.
- Distinguished fitted randomized quantile diagnostics from exact known-CDF transforms, marginal count variance from conditional overdispersion, and approximate quasi F inference from the exact Gaussian case.
- Corrected the false equivalence of hierarchical and graphical log-linear models, common-OR versus Mantel–Haenszel estimation, latent-model and causal interpretations, and small-sample/separation qualifications.
- Qualified the fitted logistic forecast rather than assuming exact calibration; retained bin counts and Wilson uncertainty bars, checked equal AUC under monotone probability rescaling, and separated Murphy resolution from AUC and excess log loss from total loss.
- Added local viewport clipping, contextual equation headings, more precise historical claims and corrected README paths.

This is a scientific source checkpoint. Visual rendering is next. Chinese narration/caption tables, continuous listening/playback and final narrated masters remain open; no bilingual production approval is claimed.
