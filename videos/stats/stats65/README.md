# Statistics, Built — Part 65: The Dissertation

The final part illustrates a research workflow: question, literature, conjecture, proof, numerical study,
application, writing, and review. The course transcript is a teaching metaphor; watching it does not award a
university qualification. The result is a teaching derivation of established weighted-conformal robustness
ideas, without an established novelty or exhaustive literature-priority claim.

The closing chapters collect the current Coverage Board, revisit the course, and suggest further study.
See the [series plan](../README.md), [syllabus](../SYLLABUS.md), and [QA evidence](../../../docs/qa/evidence/stats65-polish-20261107/README.md).

The historical [protocol](PROTOCOL.md) is preserved verbatim. Its original commit also contained results;
that commit alone cannot independently establish the timing of the historical execution. The
[QA amendment](QA-AMENDMENT.md) was committed before the corrected computation, after the original results
had been seen. The revised evidence is a **post hoc corrected rerun**, not a new preregistered confirmation.

## The teaching theorem

Let calibration pairs be IID from P, and let an independent test pair have law Q, with a common conditional
law Y|X. Use a fixed score or prediction model trained independently of calibration and test data.
For a positive measurable weight ŵ, fixed independently of those observations, assume
0 < E_P ŵ(X) < ∞ and define P_ŵ(dx) = ŵ(x)P_X(dx)/E_P ŵ(X).
The weighted split-conformal construction, including its test atom at infinity, satisfies

**Q{Y ∈ Ĉ_ŵ(X)} ≥ 1 − α − TV(P_ŵ, Q_X).**

The inequality is marginal over calibration and test draws. It is an at-least-nominal guarantee, not an
assertion of equality or conditional coverage for every x. For an independently learned weight/model,
condition on their training samples first; averaging over weight training gives an expected-TV penalty.

1. For the artificial target Q̃ = P_ŵ ⊗ P_{Y|X}, ŵ is proportional to its exact covariate likelihood ratio.
   The weighted-exchangeability result of Tibshirani et al. (2019) gives marginal coverage at least 1 − α.
2. Conditional on the calibration data, the coverage event is a fixed measurable set A.
   Its probabilities under Q and Q̃ differ by at most TV(Q, Q̃).
3. Their common conditional outcome kernel implies TV(Q, Q̃) = TV(Q_X, P_ŵ). Average over calibration data.

This reformulates known weighted-conformal and TV-robustness arguments for the lesson. Barber et al. (2023)
and Lei & Candès (2021) contain related robustness analyses; neither the theorem nor the simulation design
establishes a new research contribution.

Under P_X = N(0,1), Q_X = N(μ,1), weights exp(λμx) produce N(λμ,1), so TV is
2Φ(|1−λ||μ|/2) − 1. A logistic classifier with slope b̂ similarly gives TV = 2Φ(|b̂−μ|/2) − 1.
Consistency of b̂ makes the penalty vanish. A root auxiliary-sample-size penalty requires regular,
correctly specified fixed-dimensional logistic estimation and proportional growth of source/target samples;
it is not a root-n theorem for absolute coverage error. Pinsker gives TV ≤ √(KL/2); in the tempered-normal
case KL = (1−λ)²μ²/2. Estimating TV or KL from practical data can itself be difficult.

## Corrected numerical study

There are 3 shifts × 3 noise settings × 5 methods, with 1,000 independent replicates per cell:
500 calibration observations, 200 target test observations, and 500 independent unlabelled observations
per side for weight fitting. Method cells are unpaired. The known mean isolates the conformal step.
The original seeds and protocol predictions are retained.

The local [checked kernels](checked.py) validate logistic convergence, use closed-form normal TV and a
piecewise analytic absolute-tilt TV, and batch weighted quantiles without discarding the atom at infinity.
Independent quadrature and scalar-quantile references check these calculations. Shared historical kernels
remain available for comparison; the computation now uses the local checked implementation.

Coverage at γ = 1 (mean theoretical lower bound in parentheses):

| μ | None | Oracle | Estimated | Tempered λ=.5 | Misspecified, abs(x) only |
|---|---|---|---|---|---|
| .5 | .809 (.703) | .902 (.900) | .901 (.878) | .861 (.801) | .837 (.706) |
| 1 | .688 (.517) | .905 (.900) | .906 (.874) | .815 (.703) | .798 (.555) |
| 1.5 | .544 (.353) | .924 (.900) | .925 (.868) | .763 (.608) | .790 (.464) |

Monte Carlo SEs are empirical across independent replicate coverage means. The saved gap SE also accounts
for the random fitted-weight TV. All 45 cells are compatible with their lower bounds within simulation
uncertainty; these simulations cannot prove the theorem. At γ=0, coverage ranges .899–.910.

The original estimated-weight prediction P3 fails: coverage exceeds the stipulated one-point tolerance
at the largest shifts. Oracle/estimated infinite fractions are about 2.8% at μ=1.5, γ=1. Infinite intervals
contribute to coverage, but this observation alone does not attribute all excess coverage to them.
The saved finite-covered mass plus infinite fraction equals total coverage. The other predictions are
qualitatively compatible with these simulations, subject to MC uncertainty rather than deterministic guarantees.

Study widths are medians of replicate medians among **finite** intervals, reported separately from infinite
fractions. At μ=1.5, γ=1, these are 6.3 unweighted and 25.7 oracle. An infinite interval occurs when the test
point's normalized weight exceeds α; its weight need not exceed the entire calibration sum. These residual
intervals illustrate a width trade-off, not an optimal-width theorem.

## NHANES empirical-distribution demonstration

The Museum extract contains 5,176 complete age/BMI records with at least one finite systolic blood-pressure
reading. The outcome averages the available readings. Age is top-coded at 80. Survey weights and the survey
sampling design are not used, so the experiment does not establish national population coverage.

On this fixed table, define source row mass proportional to π(age)=expit(−(age−45)/8) and target mass
proportional to 1−π(age). Because selection depends only on covariates, these laws share Y|X. All five samples
are independent IID draws **with replacement**: model training 1,093, calibration 1,094, auxiliary source 1,000,
auxiliary target 1,000, target test 3,000. Repeated rows are expected under this empirical experiment.
A fitted mean uses age, squared age, BMI and their interaction. A separate regularized logistic classifier
estimates the target/source density ratio using age, squared age and BMI.

Across 200 independent replicates:

| Weights | Coverage ± MC SE | Age ≥65 | Age <65 | Mean of replicate median finite widths, mmHg |
|---|---|---|---|---|
| None | .73430 ± .00160 | .64619 | .79700 | 41.07 |
| Oracle | .90504 ± .00267 | .87844 | .92397 | 63.34 |
| Estimated | .90536 ± .00262 | .88003 | .92339 | 63.07 |

The source has 2.04% older adults versus 41.54% in the target (24.85% in the original table).
Mean calibration weight ESS is 82.04 oracle / 81.68 estimated, out of 1,094; mean largest shares are 5.13% / 5.51%.
These concentration diagnostics are not exact information counts or coverage certificates. Estimated/true
log-weight correlation is .99862, which alone does not establish weight accuracy. The estimated-weight mean
finite-table TV is .05626, giving the conservative mean lower bound .84374. The estimated infinite fraction is .00279.

## Coverage Board

The part adds four rows: shifted unweighted conformal 68.8%, estimated-weight conformal 90.6%,
unweighted NHANES 73.4%, and estimated-weight NHANES 90.5%, each against 90% nominal coverage.
All four save empirical dataset-level MC SEs. The full mosaic is rebuilt only when every Board-contributing
part has an input; totals, stage counts, and historical examples come from current inputs with saved hashes.
Its labels use descriptive three-MC-SE screening. Legacy rows use a nominal Bernoulli reference; the mosaic
is not a simultaneous test or an estimate of failure rates in statistical practice. Deliberately selected
counterexamples are overrepresented. Passing a row does not validate new-data assumptions or guarantee useful width/power.

## Build and verify

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats65.compute
python -m pytest tests/test_stats65_checked.py tests/test_stats_kit_thesis.py
python tools/build.py stats65 -q l
python tools/qa_scene.py stats65 Study
python tools/lecture_length.py stats65 --floor 50
```

All previous Board inputs must be generated before `fullboard`; missing contributors fail explicitly.
English source/numerical review and sampled rendering evidence are distinct from continuous narrated
playback/listening, Chinese narration/captions and final masters.

## Problems and solutions

1. **Scale invariance.** Multiplying calibration and test weights by the same positive constant leaves
   normalized masses, the weighted quantile and the prediction set unchanged.
2. **Normal TV.** Densities N(a,1), N(b,1) cross at (a+b)/2. Their mass difference on either half-line is
   2Φ(|a−b|/2)−1.
3. **Normal tilt.** Completing the square in exp(λμx−x²/2) gives N(λμ,1) after normalization.
4. **Scores independent of covariates.** Conditional on independently trained score/model parameters,
   suppose the law of S|X=x is constant across x. A covariate shift then preserves the score law;
   ordinary unweighted split-conformal scores are exchangeable and coverage is at least 1−α.
   Merely omitting x as an explicit score argument does not ensure this condition.
5. **Common outcome kernel.** For any event A, integrate its indicator against P(dy|x) to obtain g(x)∈[0,1].
   The supremum of its integrals against Q_X−P_ŵ is TV. Taking events depending only on x proves equality
   for the joint laws sharing that kernel.
6. **Dependent-weight stress test.** Compare independently fitted weights with weights overfitted on the
   calibration observations under strong shift. Use bounded/clipped positive weights or verify integrability;
   arbitrary high-degree exponential-polynomial weights need not normalize. Record coverage and each replicate's
   bound with empirical gap MC SE; write the prediction before execution. A failure would challenge an extension
   to dependent fitting, not the stated independent-training theorem.

Limitations include one covariate and calibration size in the simulation, the known mean, deliberately designed
empirical selection, weak overlap and loose covariate-only bounds. Cross-fitting and sharper score-aware bounds
require separate arguments and checking existing literature before asserting novelty.

## Sources and further study

- Graunt, *Natural and Political Observations Made upon the Bills of Mortality* (1662).
- Tibshirani, Barber, Candès & Ramdas, *Conformal prediction under covariate shift*, NeurIPS (2019).
- Barber, Candès, Ramdas & Tibshirani, *Conformal prediction beyond exchangeability*, Annals of Statistics 51 (2023).
- Lei & Candès, *Conformal inference of counterfactuals and individual treatment effects*, JRSS B 83 (2021).
- Morris, White & Crowther, *Using simulation studies to evaluate statistical methods*, Statistics in Medicine 38 (2019).
- Angelopoulos, Barber & Bates, *Theoretical Foundations of Conformal Prediction* (2024); Kish, *Survey Sampling* (1965).
- van der Vaart, *Asymptotic Statistics*; Wainwright, *High-Dimensional Statistics*; Gelman et al., *Bayesian Data Analysis*;
  Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*; Hernán & Robins, *Causal Inference: What If*;
  Imbens & Rubin, *Causal Inference for Statistics, Social, and Biomedical Sciences*.
