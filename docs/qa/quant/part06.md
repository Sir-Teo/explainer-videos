# Quant, Built, Part 6: review log

Moved here from `videos/quant/quant6/README.md` on 12 November 2026, unchanged, so that the README holds
course material only. It records what earlier QA passes inspected and at which source revision; evidence
files it names were never committed (`docs/qa/evidence/` is git-ignored).

## Current polish and QA

The sequential review is tracked in [the finance QA log](../../../docs/qa/quantitative-finance-polish.md).
The MLE demonstration shows complete confidence regions and scales all three covariances by the same sample
multiplier. Its static SE labels refer to the original sample. Histograms retain the full sample as their density
denominator, leaving observations outside the window outside the plot. The bootstrap quiz specifies one fixed
circular block, not a geometric block whose mean length equals the sample size. The DiD derivation distinguishes
nonnegative two-by-two comparison weights from potentially negative treatment-effect weights. The DML remainder
includes both the cross-product of nuisance errors and the squared treatment-model error.
