# Part 11 scientific source review

Read all 13 chapters, the compute module, local helpers, interval toolkit, tests and README in manifest order.

- Replaced coverage-curve flattening with geometric viewport clipping and kept breaks between disjoint visible segments. The likelihood is normalized at the exact MLE, included in its grid.
- Whole-CDF DKW coverage uses the exact supremum, including both limits at ties. Checking only the plotting grid had overstated coverage as 96.8%; the whole-line check is 95.85%. The 0.8% joint Wald comparison explicitly includes marginal tail failures and only checks its 200 grid points. The displayed band now includes the upper bound before the first observation.
- The credible-interval comparison uses unmodified equal-tailed Jeffreys posterior intervals, including boundary counts. The chapter distinguishes these from the boundary-modified frequentist recommendation. Coverage averages/minima are labelled by their grid.
- Exact continuous pivots, discrete conservative quantiles, normal/independence assumptions, known-covariance Fieller sets, regular asymptotics, test ordering and confidence sets versus intervals have explicit scopes. Welch is an approximation under unequal variances. Simulation screening is not proof or guaranteed detection power.
- Poll planning rounds 1067.11 up to 1068 and distinguishes uncertainty in one share from a difference. The tank interval is a continuous IID approximation. The shortest variance interval is scoped to fixed pivotal cutpoints.
- One-sided 95% zero-event bounds are distinguished from two-sided Poisson bounds (3 versus 3.69). One-to-one likelihood invariance, log-odds boundary issues, rank-based shift intervals, unconditional exchangeability, prediction-width ratios and tolerance levels are clarified.
- Removed absolute historical claims about fiducial inference and randomized intervals; added context headings to narration lead-ins and repaired documentation paths.

Validation: all 13 compute items regenerated and 13 scene modules imported. Twelve focused/reference toolkit tests passed, including five new independent checks. The board numbers are unchanged. English visual, motion, narrated playback and translation checks remain open.
