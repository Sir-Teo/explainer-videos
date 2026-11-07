# Part 12 scientific source review

Read all 13 chapters, all 15 compute items, helpers, OLS toolkit, its regression tests and README in manifest order.

- Joint two-coefficient confidence ellipses now use the exact 2 F(2, n−p) cutoff with estimated residual variance, rather than a chi-squared large-sample approximation. Reference checks evaluate the boundary in every direction.
- The selected-student example measures a 1.297 raw-unit gain, equal to 0.917 test SD because each test has variance 2. The plot, narration and README distinguish these units; a truncated-normal reference verifies the expected selection effect.
- Cropped simulation histograms keep the full denominator; curves and fitted lines use geometric viewport clipping. Scatterplots omit off-panel observations instead of moving them to boundaries. Galton bubble area is proportional to count.
- Gauss–Markov, exact normal inference, weighted/GLS estimation, pivots, working bands and high-dimensional interpolation have explicit exogeneity, rank, covariance and independence conditions. Householder/QR is distinguished from other valid numerical solvers. World-family coverage is an empirical check, not exact normal theory for a finite population.
- FWL removes linear projections. The omitted-variable formula is stated for population projection slopes; a separate test checks the exact sample identity against statsmodels. Adjustment is distinguished from causal identification, with overlap, consistency and functional-form requirements.
- Robust HC3 covariance is asymptotic under independent sampling and a regular design, not a universal small-sample or dependent-data fix. The stronger funnel shows its known-model oracle SE (0.299), distinguished from the HC3 estimate (0.267). An independent fixed-design simulation verifies the oracle variance.
- Log-income predictions use a geometric scale, interaction plus/minus values are labelled as one SE, QQ diagnostics indicate compatibility rather than proof, and regression toward the mean in both directions does not rule out causal relationships.
- The orbit is labelled a constructed schematic and does not claim to fit historical observations; the disputed role of least squares in the 1801 recovery is distinguished from the 1809 publication. Boscovich's constrained absolute-error precursor and nearly collinear rounded Anscombe data are described precisely. An independent linear program checks the LAD objective.
- Added context headings for narration lead-ins and repaired toolkit documentation links.

Validation: all 15 compute items refreshed; all 13 modules imported; 14 focused tests passed, including six new independent numerical references. Existing Coverage Board figures are unchanged. The English endpoint sweep is starting; visual, motion, narrated playback and translation gates remain open.
