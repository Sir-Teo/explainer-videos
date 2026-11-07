# Part 23 scientific source review

All 13 scenes, README and solutions, 14 compute items and the local/shared OLS code were read in chapter order. All compute items were refreshed and all 13 scenes imported. The focused checks pass 17 tests plus five subtests (seven new independent checks and ten OLS-kit tests).

- Separated the shared World school and health programme effects in the earlier shared correction; school truth is now +20 points. NIST's 16 Longley rows, six predictors and seven certified coefficients match exactly; see `longley-source.json`.
- Corrected numerical sensitivity claims: mathematical squared condition number versus rounded Gram estimate, independent 90-digit reference for the supplied rounded inputs, failed-solve accounting, and the pessimistic squared-condition residual term. QR updates carry transformed responses.
- Replaced the finite-World histogram's exact-null claim with fresh conditional Gaussian responses. Qualified rank, covariance, common-intercept, affine-restriction and simultaneous-contrast assumptions.
- Distinguished original OLS residual autocorrelation (0.815), actual DW (0.380) and iterated PW rho (0.820); constrained stationary PW is explicit and was inactive throughout the seeded simulation.
- Implemented cluster-sufficient-statistic restricted wild bootstrap, checked against full observation-level refits. Monte Carlo p-values use the +1 correction and count numerical ties consistently. Eight-school fits redraw one-arm designs before fitting, recording two redraws and conditional sampling. Formula and wild-bootstrap studies retain their separate denominators.
- Corrected quantile sparsity to inverse density, empirical score meat for misspecified lines, density-bread scaling, transformation and causal qualifications, positive-intercept Engel food shares, and approximate bootstrap comparisons.
- Learned distinct spline knots within each CV training fold and computed the one-SE heuristic (minimum 8 requested knots; one-SE 0); clarified natural cubic dimensions. Geometric viewport clipping preserves crossings and missing gaps without flattening curves.
- Corrected outcome-error mean versus variance, instrument exclusion requirements, actual intercepts on plotted father fits, illustrative Hubble error calibration, leverage versus residual robustness and deleted-scale DFBETAS.

English visual rendering is the next gate. This source review does not approve playback or bilingual production. Chinese tables, continuous listening and final narrated masters remain open.
