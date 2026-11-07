# Part 8 scientific source review

All 14 chapters, compute items, helpers and README were reviewed in manifest order. This checkpoint establishes the scientific correction pass; visual verification and narrated/bilingual production approval remain open.

Repairs include full-denominator histograms and faithful curve viewport clipping; a source-pool mean consistent with the sampling-machine draws; integer success counts rather than floating-point bin assignment; the population-variance convention in the exact finite-population correction; the design FPC in ratio standard errors; upward rounding of planned sample sizes; the untruncated t multiplier; and the height ranges needed to show histogram peaks honestly. The ratio example now reports design-linearized mean SE 21,402 and coverage 89.7%, rather than attributing its earlier result solely to first-order approximation.

Explanations now distinguish normal theory from finite-World comparisons, specify Cochran/ANOVA assumptions, distinguish independent fitted directions from arbitrary parameter counts, define Student's historical variance divisor, state the regularity needed for median/plug-in/bootstrap/CRLB results, qualify Fisher-z approximations, limit the optimal variance divisor to its estimator class, and state the independent-normal/known-variance/fixed-center James–Stein result. The sample-variance sensitivity at n=10 and excess kurtosis 6 is 3.7 times normal theory, not exactly four. Coverage Board verdicts are a prespecified Monte Carlo screening rule, with displayed two-SE bands distinguished from three-SE verdict thresholds.

Five reference tests pass: exact exhaustive SRS mean variance, preserved rounded/infinite Student tails, paired inference against SciPy, exhaustive ratio-design variance for a constant auxiliary variable, and success-count frequencies. All compute items complete and all 14 scene modules import. The first endpoint sweep is underway.

Chinese narration/caption tables and continuous narrated listening/playback remain open.
