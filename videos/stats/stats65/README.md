# Statistics, Built — Part 65: The Dissertation

Part 65 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). It is the last part of Stage V and the PhD milestone.

It returns to the series' first page: John Graunt's *Natural and Political Observations Made upon the Bills of
Mortality* (1662), where a ledger became knowledge. The part asks how new statistical knowledge is made, and answers
by carrying out a small dissertation on screen. It then shows the whole degree:
- the full Coverage Board, 318 promises from 57 parts;
- the completed transcript;
- where to go next.

The dissertation's question comes from Parts 57 and 60. Weighted conformal prediction keeps its coverage under
covariate shift when the likelihood ratio is known. In practice the ratio is estimated. How much coverage does the
estimation cost?

The part's chapters:
- choosing a question:
  - importance, novelty, feasibility and falsifiability, and where questions come from;
  - candidates from Parts 56–64, and cutting the chosen one to size;
  - what would count as an answer;
- reading the literature:
  - how to read a paper, and the founding proof's weighted exchangeability (Tibshirani, Barber, Candès & Ramdas 2019);
  - Barber, Candès, Ramdas & Tibshirani (2023), and Lei & Candès (2021);
  - reading a simulation table, checking formulas numerically, and the gap;
- a conjecture: wrong weights make a right method for the wrong target, and coverage is at least
  1 − α − TV(P_ŵ, Q). It comes with its Gaussian special case and its doubts;
- a theorem, proved on screen in three steps:
  - corollaries for tempered and logistic weights, with consistency at rate n^{−1/2};
  - a worked number, the missing upper bound, and a KL version via Pinsker;
  - the relation to prior work;
- a preregistered simulation study (Morris, White & Crowther 2019):
  - the protocol and its five predictions, in [`PROTOCOL.md`](PROTOCOL.md), written before the main run;
  - Monte Carlo error, then coverage, bounds, slack and widths;
  - the scorecard, the failed prediction and its mechanism, and limitations;
- an application to NHANES with a designed selection that under-samples the old:
  - unweighted, true and estimated weights;
  - weight diagnostics (effective sample size, the largest weight), and a practical workflow;
- writing and review: structure, a four-sentence abstract, figures, a mock referee report, reproducibility and
  honesty;
- the full Coverage Board, shown in the new board mosaic:
  - what breaks a promise and what keeps one, by stage;
  - rows to remember, and what the Board cannot show;
- the transcript complete: the timeline lit from 1662, the stages, the instruments, and the series by numbers;
- where to go next: books, open problems from Parts 56–65, journals, replication, habits;
- the thesis in five lines, a reflection, three questions, and farewell.

It keeps the last two promises:
- **Part 57** assumed the likelihood ratio was known. Chapters 3–6 estimate it and count the cost.
- **Part 7** taught simulation without saying when to decide what to simulate. Chapter 5 writes the protocol down
  first.

**Built in this part:**
- **The thesis.** This README is its short paper; [`PROTOCOL.md`](PROTOCOL.md) is its preregistration.
- **`statkit.thesis`** ([`explainer/stats/kit/thesis.py`](../../../explainer/stats/kit/thesis.py)), tested in
  `tests/test_stats_kit_thesis.py`:
  - the Gaussian TV formula and the exact grid TV of any reweighted source;
  - the bound;
  - the data-generating mechanism;
  - logistic (and misspecified) density-ratio weights;
  - weighted split-conformal half-widths;
  - one replicate and the full study;
  - the application's selection probabilities.
- **The board mosaic** (`BoardMosaic` in `explainer/stats/viz.py`), the part's instrument. It draws every Coverage
  Board row of the degree as a tile, stacked above its part and coloured by verdict, with the five stages marked.

**Data.**
- The Museum's NHANES extract, with a selection designed in advance so the true weights are known.
- Everything else is seeded simulation or exact arithmetic.

The Coverage Board gains four rows, and the full Board now holds 318: 139 kept, 25 conservative, 154 broken.

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| split conformal, no weights, under shift | μ = 1, γ = 1, n = 500 | 90% | 68.8% | broken |
| weighted conformal, estimated weights | μ = 1, γ = 1, n = 500 | 90% | 90.6% | kept |
| NHANES blood pressure, no weights | a sample short of the old | 90% | 73.4% | broken |
| NHANES blood pressure, estimated weights | a sample short of the old | 90% | 91.2% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats65.compute   # once (several minutes; the study is 45,000 replicates)
python tools/build.py stats65 -q l                         # fast 480p preview
python tools/build.py stats65                              # 1080p30 -> renders/stats65.mp4
python tools/qa_scene.py stats65 Study
python tools/lecture_length.py stats65 --floor 50
```

## The thesis

**Weighted conformal prediction with estimated weights: a total-variation bound, and how loose it is.**

*Abstract.*
- Weighted conformal prediction guarantees coverage under covariate shift when the likelihood ratio is known, but in
  practice the ratio is estimated.
- We show that with weights fixed in advance, coverage falls by at most the total variation distance between the
  reweighted source and the target.
- In a preregistered simulation the bound held in all 45 cells, but left wide slack, most when the scores depended
  weakly on the covariates. Estimated weights over-covered at large shifts, through infinite intervals.
- On NHANES data with a designed selection, estimated weights restored 91% coverage where unweighted intervals gave
  73%.

**Theorem.**
- Let (Xᵢ, Yᵢ), i ≤ n, be iid from P and (X, Y) from Q, independent, with P_{Y|X} = Q_{Y|X}.
- Let ŵ > 0 be fixed (independent of the calibration data) with E_P ŵ < ∞, and let P_ŵ(dx) = ŵ(x)P(dx)/E_P ŵ.
- Then the weighted split-conformal set Ĉ_ŵ satisfies Q(Y ∈ Ĉ_ŵ(X)) ≥ 1 − α − TV(P_ŵ, Q_X).

*Proof.*
1. ŵ is proportional to dP_ŵ/dP, and the weighted quantile ignores constants. By Tibshirani et al. (2019), a test pair
   from Q̃ = P_ŵ ⊗ P_{Y|X} is covered with probability at least 1 − α.
2. Given the calibration data, coverage is the probability of a fixed set A. Then |Q(A) − Q̃(A)| ≤ TV(Q, Q̃), and
   TV(Q, Q̃) = TV(Q_X, P_ŵ) because the two share the conditional law.
3. The distance does not depend on the calibration data, so averaging gives the claim. ∎

**Corollaries.**
- Tempered Gaussian-tilt weights w^λ under P = N(0, 1), Q = N(μ, 1) give the bound
  1 − α − (2Φ(|1 − λ||μ|/2) − 1).
- A logistic classifier with slope b̂ gives 1 − α − (2Φ(|b̂ − μ|/2) − 1).
- By Pinsker, the loss is at most √(KL/2); for the tempered weights that is |1 − λ||μ|/2.

**Relation to prior work.** Barber, Candès, Ramdas & Tibshirani (2023) bound the coverage gap of weighted methods
under arbitrary departures from exchangeability by total variation terms, and the theorem here is of the same kind. Its
contribution is a single computable distance for estimated covariate-shift weights, with the study's measurement of
how tight it is.

**Study** ([`PROTOCOL.md`](PROTOCOL.md), ADEMP).
- Design: 3 shifts μ × 3 noise dependences γ × 5 methods, 1,000 replicates per cell. Each replicate has 500
  calibration points, 200 test points, and 500 unlabelled points per side for the weights.
- Monte Carlo SEs: at most 0.0027.

Coverage at γ = 1, with each method's bound in brackets:

| μ | none | oracle | estimated | tempered (λ = 0.5) | misspecified (\|x\| only) |
|---|---|---|---|---|---|
| 0.5 | 0.809 (0.703) | 0.902 (0.900) | 0.901 (0.878) | 0.861 (0.801) | 0.837 (0.706) |
| 1.0 | 0.688 (0.517) | 0.905 (0.900) | 0.906 (0.874) | 0.815 (0.703) | 0.798 (0.555) |
| 1.5 | 0.544 (0.353) | 0.924 (0.900) | 0.925 (0.868) | 0.763 (0.608) | 0.790 (0.464) |

Further results:
- **γ = 0.** Every method covers 0.899–0.910, because the scores are exchangeable under any shift.
- **Slack.** At μ = 1, coverage minus the bound, for no weights, is 0.38 at γ = 0, 0.23 at γ = 0.5 and 0.17 at γ = 1.
- **Infinite intervals.** At μ = 1.5, about 2.8% of the oracle and estimated intervals are infinite.

**The predictions, scored.**
- **P1** held: no weights under-cover, more with μ and γ, and cover 0.90 at γ = 0.
- **P2** held: the true weights are at or above 0.90 in every cell.
- **P3** failed: the estimated weights were not within a point of 0.90 everywhere. At μ = 1.5 they cover 0.907
  (γ = 0), 0.920 (γ = 0.5) and 0.925 (γ = 1), because extreme weights make intervals infinite.
- **P4** held: the tempered and misspecified weights under-cover but stay above their bounds.
- **P5** held: the bound is loosest at γ = 0 and tightest at γ = 1.

**Application.** NHANES, 5,176 adults. Each enters the study with probability 1/(1 + e^{(age − 45)/8}), so about 2,187
enter; 25% of adults are 65 or over, but only 2% of the study. The target is the adults the study missed. Over 200
draws:

| Weights | Coverage | 65 and over | Under 65 | Median width (mmHg) |
|---|---|---|---|---|
| none | 73.4% | 64.4% | 79.9% | 41 |
| true | 91.2% | 88.9% | 92.8% | 65 |
| estimated (logistic on age, BMI) | 91.2% | 89.1% | 92.8% | 65 |

Weight diagnostics:
- The estimated and true log weights correlate 0.999.
- The weighted calibration set's effective sample size is about 79 of 1,094, and the largest weight carries 6% of
  the total.

**Limitations and open questions.**
- Weights estimated on the calibration data itself (cross-fitting) are not covered.
- The bound ignores the scores, so it is loose when they depend weakly on x. A score-aware distance is the natural
  sharpening.
- An upper bound needs control of the largest weight.
- The study used one covariate, one calibration size and the true mean function.

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Back to Graunt | 1662; 64 parts done |
| 1 | The question | five candidates from Parts 56–64 |
| 2 | The literature | Tibshirani et al. (2019); Barber et al. (2023); Lei & Candès (2021); TV formula checked to 10⁻⁸ |
| 3 | The conjecture | μ = 1: bound 51.7% with no weights, 70.3% with half-strength weights |
| 4 | The theorem | worked case μ = 1, λ = 0.5: TV 0.197, bound 70.3%, observed 81.5% (γ = 1) |
| 5 | The study | 45 cells × 1,000; bound held in 45/45; P3 failed; slack 0.17–0.38 at μ = 1; widths at μ = 1.5, γ = 1: none 6.3, oracle 25.7 |
| 6 | NHANES | coverage 73.4% / 91.2% / 91.2%; 65+: 64% / 89% / 89%; ESS ≈ 79 of 1,094 |
| 7 | Writing | abstract, four figures, three referee points |
| 8 | The full Board | 318 rows, 57 parts: 139 kept, 25 conservative, 154 broken |
| 9 | The transcript | 65 of 65 |
| 10 | Where next | — |
| 11 | Outro | — |

## Sources

- J. Graunt, *Natural and Political Observations Made upon the Bills of Mortality* (1662).
- R. Tibshirani, R. Barber, E. Candès & A. Ramdas, "Conformal prediction under covariate shift", NeurIPS (2019).
- R. Barber, E. Candès, A. Ramdas & R. Tibshirani, "Conformal prediction beyond exchangeability", *Ann. Statist.* 51
  (2023).
- L. Lei & E. Candès, "Conformal inference of counterfactuals and individual treatment effects", *JRSS B* 83 (2021).
- T. Morris, I. White & M. Crowther, "Using simulation studies to evaluate statistical methods", *Statistics in
  Medicine* 38 (2019).
- A. Angelopoulos, R. Barber & S. Bates, *Theoretical Foundations of Conformal Prediction* (2024).
- L. Kish, *Survey Sampling* (1965).
- **Further reading.**
  - A. van der Vaart, *Asymptotic Statistics* (1998); M. Wainwright, *High-Dimensional Statistics* (2019);
  - A. Gelman et al., *Bayesian Data Analysis* (3rd ed., 2013); T. Hastie, R. Tibshirani & J. Friedman, *The
    Elements of Statistical Learning* (2nd ed., 2009);
  - M. Hernán & J. Robins, *Causal Inference: What If* (2020); G. Imbens & D. Rubin, *Causal Inference for
    Statistics, Social, and Biomedical Sciences* (2015).

## Problems and solutions

1. **Scale invariance.** The weighted quantile uses the normalized weights wᵢ/(Σⱼwⱼ + w_test). Multiplying every
   weight by c > 0 leaves them unchanged, so the set is unchanged.
2. **TV between unit-variance normals.**
   - The densities of N(a, 1) and N(b, 1) cross only at m = (a + b)/2, so the TV is
     P_b(X > m) − P_a(X > m) for a < b.
   - That is Φ(d/2) − Φ(−d/2) = 2Φ(d/2) − 1, with d = |a − b|.
3. **The tilted normal.** e^{λμx}e^{−x²/2} = e^{−(x − λμ)²/2}e^{λ²μ²/2}. Normalizing gives N(λμ, 1).
4. **Scores that ignore x.** If S = s(X, Y) has the same law whatever X is, then the calibration scores and the test
   score are iid under any covariate shift. So they are exchangeable, and Part 57's quantile lemma gives coverage
   ≥ 1 − α.
5. **Dropping the conditional law.**
   - Q(A) − Q̃(A) = ∫ g(x)(q(x) − p̃(x))dx, with g(x) = ∫ 1_A(x, y)p(y | x)dy ∈ [0, 1].
   - The supremum of such integrals over g in [0, 1] is TV(Q_X, Q̃_X).
6. **A refutation design.**
   - Aims: test whether coverage stays above the bound when ŵ is fitted on the calibration data itself.
   - Data: a flexible classifier, such as a high-degree polynomial logistic regression, overfitted to the same n
     source points plus a target sample, under a strong shift with γ = 1.
   - Estimand: target coverage.
   - Methods: split-sample ŵ against same-sample ŵ.
   - Performance: coverage ± MC SE against each replicate's bound.
   - Prediction, written first: same-sample weights correlate with the calibration scores, and coverage can fall
     below the bound.

## Glossary

- **The process.** Research question; literature gap; conjecture; theorem; corollary; preregistration; ADEMP;
  Monte Carlo standard error; falsified prediction; referee report; reproducibility.
- **The thesis.**
  - Covariate shift; likelihood ratio; weighted conformal prediction; weighted exchangeability; reweighted source P_ŵ;
    total variation; Pinsker's inequality.
  - Tempered weights; density-ratio classifier; effective sample size; infinite intervals; overlap.
- **The degree.** Coverage Board; kept, conservative, broken; transcript; the World; the Museum; statkit.

## Where it comes back

This is the last part. Everything comes back here: every Board row of Parts 1–65 is in chapter 8's mosaic, and every
part's cell is filled in chapter 9's transcript.
