# Preregistered protocol: weighted conformal prediction with estimated weights

Written before the full study was run. Only a 50-replicate pilot of one cell (μ = 1, γ = 0.5) had been seen, to check
the code and the Monte Carlo error. The study's results are reported in the README, whatever they show. This file is
not edited after the run.

The design follows Morris, White & Crowther (2019), ADEMP.

## Aims

1. Measure how much coverage weighted split conformal prediction loses under covariate shift when the weights are
   estimated, or deliberately wrong.
2. Check the theorem's lower bound, 1 − α − TV(P_ŵ, Q), in every cell, and see how tight it is.

## Data-generating mechanisms

- Source P: X ~ N(0, 1). Target Q: X ~ N(μ, 1).
- In both: Y = sin X + X/2 + exp(γX) ε, with ε ~ N(0, 1).
- Factors, fully crossed: μ ∈ {0.5, 1, 1.5} (the size of the shift), and γ ∈ {0, 0.5, 1} (how strongly the noise
  depends on x).
- Each replicate draws:
  - 500 calibration pairs from P;
  - 200 test pairs from Q;
  - independently, 500 unlabelled draws from each of P and Q, for estimating the weights.

## Estimand

Coverage of the target at nominal 1 − α = 0.90: P_Q(Y ∈ C(X)).

## Methods

The score is |Y − m(X)| with the true mean m, so the study isolates the conformal step. The methods are:
1. **none**: ordinary split conformal.
2. **oracle**: weighted conformal with the true ratio w(x) = exp(μx − μ²/2).
3. **estimated**: weights from a logistic classifier of target against source on (1, x), fitted on the unlabelled
   draws. This is correctly specified for this shift.
4. **tempered**: w(x)^0.5, the kind of shrunken ratio an over-regularized classifier gives.
5. **misspecified**: a logistic classifier that sees only |x|, so it cannot represent a shift in the mean.

## Performance measures

Over 1,000 replicates per cell, where a replicate's coverage is averaged over its 200 test points:
- mean coverage with its Monte Carlo standard error;
- median interval width;
- the fraction of infinite intervals;
- the theorem's bound, computed exactly for each replicate's weight function and averaged.

The pilot's Monte Carlo SE was about 0.005 with 50 replicates, so 1,000 gives about 0.0012.

## Predictions, written in advance

- **P1.** *none* under-covers, more so as μ and γ grow. At γ = 0 it covers 0.90 in every μ, because the scores do
  not depend on x.
- **P2.** *oracle* is within three Monte Carlo SEs of 0.90, or above it, in every cell.
- **P3.** *estimated* is within one point of 0.90 in every cell.
- **P4.** *tempered* and *misspecified* under-cover when γ > 0, but stay above the theorem's bound in every cell.
- **P5.** The bound is loosest at γ = 0 and tightest at γ = 1.

A prediction that fails is reported as failed.
