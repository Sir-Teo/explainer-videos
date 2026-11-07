# Part 9 scientific source review

Reviewed the README, all ten compute items, the local helpers, all 13 scene modules in manifest order, and the estimation toolkit examples.

- Histograms retain the full simulation denominator when tails leave the viewport. Likelihood curves are normalized at the exact MLE, including the uniform boundary. Clipped curves preserve separate paths across off-panel excursions.
- The two-parameter normal likelihood uses a chi-squared cutoff with two degrees of freedom for its approximate 95% joint contour. One-parameter intervals remain explicitly approximate.
- Tank maxima may equal the population count. The displayed inverse-square-root and inverse-capture rates are approximations in the stated small-sampling-fraction regime; finite-population factors remain visible.
- Moment matching requires finite identifying moments and a continuous/differentiable inverse. Gamma variance uses divisor n explicitly. The finite-simulation variance ratio is qualified before the approximate sample-size interpretation.
- Consistency requires uniform convergence and a separated maximum; the KL proof handles candidate mass outside the true support. Regularity, positive finite information, boundary likelihood-ratio mixtures, and first-order nuisance information are scoped explicitly.
- Completeness/Rao–Blackwell equality is almost sure. Cauchy information specifies unit scale. The geometric information bound uses an absolute derivative. Irregular models have other bounds even though the usual differentiable Cramér–Rao proof fails.
- Biased shrinkage does not universally improve risk, an oracle multiplier is distinguished from its usable approximation, capture weights are distinguished from inclusion probabilities, and toolkit Monte Carlo-error claims match the actual return fields.
- Added context headings for narration lead-ins and corrected the historical tank table comparison and toolkit documentation link.

Validation: all compute items regenerated; all 13 scene modules imported; 15 focused numerical/toolkit tests passed. Five new reference checks cover exhaustive tank unbiasedness and conditional improvement, SciPy gamma fits, exact relative likelihoods, retained histogram tail mass, and geometric clipping.

Visual, motion, speech and translation gates remain open at this source checkpoint. The English endpoint sweep is running. No bilingual or continuous-playback approval is implied.
