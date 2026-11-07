# Statistics, Built — Part 19: Learning from Data

Part 19 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Until now the goal was a parameter: a mean, a
slope, an effect. This part turns to prediction: how to predict well, and how to know how well you predict.

It opens with the *Federalist* papers of 1787–88. Hamilton, Madison and Jay all signed them "Publius", and twelve
were claimed by both Hamilton and Madison. Mosteller and Wallace (1964) settled the question with the rates of dull
words. *upon* appears in every one of Hamilton's 51 papers, at 1.0–7.5 per 1,000 words. It is absent from 11 of
Madison's 14 and from 10 of the 12 disputed papers. The texts come from Project Gutenberg, counted by
[`tools/federalist_counts.py`](../../../../tools/federalist_counts.py).

From there the part covers:
- **Prediction error.** Training and test error; polynomials of degree 1–14 fitted to 30 points.
  - Test error is smallest at degree 3 (0.100), against a noise variance of 0.09.
  - At degree 14, the training error is 0.04 and the test error 346.
  - Efron's covariance penalty and the optimism 2σ²p/n, derived.
  - Mallows' Cp also picks degree 3, but misses the explosion at high degree.
- **Bias and variance.** Test error = noise + bias² + variance, derived and simulated for k-NN at a point.
  - 3,000 training sets; best k = 12.
  - Variance σ²/k; df = tr S for linear smoothers.
- **Cross-validation.**
  - 10-fold CV of k picks k = 8 (test error 0.119); the true optimum is k = 7.
  - The one-SE rule picks k = 17 (test error 0.141).
  - What CV estimates (Bates, Hastie & Tibshirani, online 2023 / volume 2024), with a Board row; leave-one-out.
- **k-nearest neighbours.**
  - Regions for the World's vote with k = 1 and k = 51.
  - The curse of dimensionality: a cube holding 10% of the data has edge 0.79 in 10 dimensions. The ratio of
    nearest to average distance rises from 0.003 to 0.81.
  - With irrelevant dimensions, 10-NN error rises from 0.086 to 0.43, against 0.45 for predicting the mean.
  - Cover & Hart (1967): 1-NN settles at 31.0%, below the bound of 35.1%. √n-NN falls to 22.6%, close to the Bayes
    error of 22.7%.
- **Naive Bayes vs logistic regression.**
  - Generative vs discriminative; the Poisson log odds as a weighted word count.
  - Leave-one-out: 0 errors in 65 for each.
  - Learning curves: with 6 training papers, 6.1% vs 10.7% (Ng & Jordan 2002).
  - Naive Bayes is overconfident.
- **Trees.** CART on the World's vote from income and age.
  - Splits at incomes of 31.4k and 76.4k.
  - Cost-complexity pruning; CV selects a leaf budget of 4; weakest-link pruning gives 3 actual leaves.
  - Test error 35.9% pruned vs 38.5% for the full 35-leaf tree; always guessing Red scores 37.6%.
- **Ridge and the lasso.**
  - The ℓ₁ diamond against the ℓ₂ disc (`L1Geometry`).
  - Soft thresholding and proportional shrinkage.
  - Paths for 20 predictors, 3 of them real. CV keeps 8 variables; the one-SE rule keeps exactly the 3 real ones.
- **Classification metrics.**
  - Confusion matrices at thresholds 0.5 and 0.35: recall 23.7% → 63.8%, precision 57.5% → 47.7%.
  - ROC (AUC 0.663), precision–recall, calibration (Brier 0.215).
  - Choosing a threshold from costs: t* = 1/(1 + c), found empirically at 0.43, 0.34 and 0.17.
- **The *Federalist* decided.**
  - Naive Bayes favours Madison on all 12; No. 55 is the weakest, at log₁₀ odds 0.6.
  - Ridge logistic gives P(Madison) = 0.30 for No. 55 and 0.74–0.99 for the other eleven.
  - The joint papers come out Madison's.
  - Robustness: dropping *upon* flips No. 55 (log₁₀ odds −2.2) and leaves the other eleven for Madison.
- **Leakage and honest evaluation.**
  - Selecting 20 of 2,000 noise features before CV gives 11.3% error; selecting inside the loop gives 50.1%.
  - A catalogue of six leaks.
  - A reused holdout: the vote of 513 random guesses scores 72.4% on the leaderboard and 50.4% on fresh labels.
  - The optimism of the CV minimum, against nested CV.
  - The train / validate / test discipline.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- word counts are the Museum's *Federalist*;
- the vote, incomes and ages are the World's survey block;
- everything else is a seeded simulation with a known truth (y = sin 2πx + x/2 + N(0, 0.3²) for the regression
  examples).

**Built in this part:**
- **`statkit.learn`** ([`explainer/stats/kit/learn.py`](../../../../explainer/stats/kit/learn.py)), checked in
  `tests/test_stats_kit_learn.py`:
  - K-fold splits, CV scores with fold SEs, and the one-SE rule;
  - k-NN regression and classification;
  - Poisson naive Bayes with per-word contributions;
  - ridge logistic regression;
  - CART growing, cost-complexity pruning paths and pruning;
  - standardization, ridge, soft thresholding, and the lasso by coordinate descent with its path;
  - confusion matrices, precision–recall curves and AUC.
- **The ℓ₁ geometry** (`L1Geometry` in `explainer/stats/viz.py`): least-squares contours with the lasso's diamond
  and ridge's disc, and the point where they first touch.

The Coverage Board gains one row: a 95% interval for test error.

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| 10-fold CV ± 1.96 SE | k-NN test error, n = 100 | 2,000 | 90.15% | broken |

## Build it

```bash
python -m videos.stats.stats19.compute         # once (a few minutes; cached in .cache/stats19)
python tools/build.py stats19 -q l             # fast 480p preview
python tools/build.py stats19                  # 1080p30 -> renders/stats19.mp4
python tools/qa_scene.py stats19 Leakage
python tools/lecture_length.py stats19 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Hamilton or Madison? 1964 | 51 Hamilton, 14 Madison, 5 Jay, 3 joint, 12 disputed; *upon* in 51/51 Hamilton papers, absent in 11/14 Madison and 10/12 disputed |
| 1 | Prediction error | best degree 3 (test 0.100); degree 14: train 0.04, test 346; noise 0.09; cubic train 0.071; Cp picks degree 3 |
| 2 | Bias and variance | 3,000 training sets of 100 at x₀ = 0.25; best k = 12 (total 0.098) |
| 3 | Cross-validation | CV picks k = 8 (test 0.119); one-SE k = 17 (test 0.141); true optimum k = 7 (0.117); Board 90.15% |
| 4 | k-nearest neighbours | cube edge 0.79 at p = 10; distance ratio 0.003 → 0.81; 10-NN error 0.086 → 0.43; 1-NN 30.5% (limit 31.0%, bound 35.1%), √n-NN 22.6%, Bayes 22.7% |
| 5 | Naive Bayes vs logistic | 91 words; LOO 0/65 errors each; 6 training papers: 6.1% vs 10.7%; *upon* odds factor about 17 |
| 6 | Trees | splits at 31.4k (Blue 25.1%) and 76.4k (42.7% / 63.1%); CV selects a leaf budget of 4; weakest-link pruning gives 3 actual leaves; test 35.9% vs 38.5% (35 leaves); always Red 37.6% |
| 7 | Ridge and the lasso | lasso (1.20, 0.00) vs ridge (1.05, 0.58) in the picture; CV keeps 8, one-SE keeps 3; true (3.81, −1.94, 1.61), fitted (3.15, −1.48, 1.48) |
| 8 | Classification metrics | accuracy 65.2% (always Red 62.9%); recall 23.7% → 63.8%, precision 57.5% → 47.7% at t = 0.35; AUC 0.663; Brier 0.215; best t 0.43 / 0.34 / 0.17 for c = 1 / 2 / 5 |
| 9 | The *Federalist* decided | log₁₀ odds 0.6 (No. 55) to 19.7; logistic P(Madison) 0.30 for No. 55, 0.74–0.99 otherwise; joint papers 28, 17, 9; without *upon*: 11 of 12, No. 55 at −2.2 |
| 10 | Leakage and honest evaluation | 11.3% vs 50.1% (n = 60, p = 2,000, 100 data sets); best random guess 54.9%, vote 72.4% vs 50.4% fresh; min CV 0.1075, true 0.1094, nested 0.1153 |
| 11 | Outro | — |

## Sources

- **The *Federalist*.**
  - F. Mosteller & D. Wallace, *JASA* 58 (1963); *Inference and Disputed Authorship: The Federalist* (1964).
  - D. Adair, "The authorship of the disputed Federalist papers", *William and Mary Quarterly* 1 (1944).
  - The texts: Project Gutenberg, eBook 18.
- **Prediction error and model choice.**
  - C. Mallows, *Technometrics* 15 (1973); H. Akaike (1973).
  - B. Efron, *JASA* 81 (1986) and *JASA* 99 (2004).
  - M. Stone, *JRSS B* 36 (1974); S. Geisser, *JASA* 70 (1975).
  - S. Bates, T. Hastie & R. Tibshirani, *JASA* 119 (2024; arXiv 2021).
  - S. Geman, E. Bienenstock & R. Doursat, *Neural Computation* 4 (1992).
- **Methods.**
  - T. Cover & P. Hart, *IEEE Trans. Inf. Theory* 13 (1967); C. Stone, *Ann. Stat.* 5 (1977); R. Bellman,
    *Adaptive Control Processes* (1961).
  - A. Ng & M. Jordan, *NIPS* 14 (2002).
  - L. Breiman, J. Friedman, R. Olshen & C. Stone, *Classification and Regression Trees* (1984).
  - A. Hoerl & R. Kennard, *Technometrics* 12 (1970); R. Tibshirani, *JRSS B* 58 (1996).
  - L. Breiman, "Statistical modeling: the two cultures", *Statistical Science* 16 (2001).
- **Leakage.**
  - C. Ambroise & G. McLachlan, *PNAS* 99 (2002).
  - S. Kaufman, S. Rosset, C. Perlich & O. Stitelman, *ACM TKDD* 6 (2012).
  - A. Blum & M. Hardt, *ICML* (2015); C. Dwork et al., *Science* 349 (2015).
- **Books.**
  - G. James, D. Witten, T. Hastie & R. Tibshirani, *An Introduction to Statistical Learning* (2nd ed., 2021).
  - T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning* (2nd ed., 2009), §7.10.2 for the
    wrong and right way to cross-validate.

## Problems and solutions

**1. The optimism of least squares.**

*Solution.* Assume the model is right, so Xβ = f and the hat matrix H projects onto a p-dimensional space.
- **Training error.** The residual vector is (I − H)y = (I − H)ε, so E[RSS] = σ² tr(I − H) = σ²(n − p). Dividing by n
  gives E[train] = σ²(1 − p/n).
- **Test error at the same x's.** For new responses y* = f + ε*, E‖y* − Hy‖² = nσ² + E‖Hε‖² = nσ² + σ² tr H =
  σ²(n + p). So E[test] = σ²(1 + p/n).

The gap is 2σ²p/n, Mallows' penalty.

**2. k-NN for a parabola.**

*Solution.* The prediction at x₀ is the average of f(x₀ + jh) = x₀² + 2x₀jh + j²h² over j = −m, …, m. The middle
term averages to zero.
- **Bias.** Since Σj² = m(m + 1)(2m + 1)/3, dividing by k = 2m + 1 gives bias = h²m(m + 1)/3, whatever x₀.
- **Variance.** σ²/k.
- **MSE.** h⁴m²(m + 1)²/9 + σ²/(2m + 1). The squared bias grows like k⁴ and the variance falls like 1/k.

**3. Neighbourhoods in high dimensions.**

*Solution.* The edge is e = 0.01^{1/p}. For p = 10, e = 0.01^{0.1} ≈ 0.63; for p = 100, e ≈ 0.955. To hold 1% of
the data, the "neighbourhood" must span 63%, and then 95.5%, of every axis.

**4. A paper without *upon*.**

*Solution.* For a count x in t thousand words, the Poisson log likelihood ratio is
log[P_M(x)/P_H(x)] = x log(r_M/r_H) − t(r_M − r_H). With x = 0 and t = 2, it is −2(0.18 − 3.3) = 6.24 nats, or
6.24/ln 10 ≈ 2.71 in base 10: about 500 to 1 for Madison from the absence of a single word. Hamilton would expect
6.6 uses in such a paper, and e^{−6.6} is tiny.

**5. Ridge and the lasso for a standardized orthogonal design.**

*Solution.* Centre the predictors and response and let XᵀX = nI. Then β̂ = Xᵀy/n and SSE/(2n) = constant + ½||β − β̂||².
- **Ridge.** Adding (λ/2)||β||² and setting the gradient to zero gives β = β̂/(1 + λ).
- **Lasso.** Adding λ||β||₁ separates into ½(βⱼ − β̂ⱼ)² + λ|βⱼ|. The minimizer is sign(β̂ⱼ)(|β̂ⱼ| − λ)₊.

These use the same per-observation conventions as the scenes. The intercept is not penalized. With XᵀX = I and unnormalized loss, the effective penalty must be rescaled accordingly.

**6. A good test for a rare condition.**

*Solution.* Per 10,000 people: 100 have the condition, of whom 90 test positive; 9,900 don't, of whom 495 test
positive.
- **Precision.** 90/(90 + 495) ≈ 15.4%.
- **Accuracy.** (90 + 9,405)/10,000 = 94.95%, below the 99% of declaring everyone negative.

## Glossary

- **Training error, test error**: average loss on the data a rule learned from, and on new data from the same source.
- **Overfitting, underfitting**: a rule that follows the noise; a rule too stiff to follow the signal.
- **Optimism; covariance penalty; Cp; AIC**: the expected gap between test and training error, and estimates of
  test error that add it back.
- **Bias–variance decomposition**: expected test error = noise + bias² + variance, at each x.
- **Linear smoother; effective degrees of freedom**: a fit ŷ = Sy; df = tr S.
- **Tuning parameter**: a setting chosen from the data (k, a degree, λ).
- **K-fold and leave-one-out cross-validation**: estimating test error by fitting without each fold in turn.
- **One-standard-error rule**: choose the simplest model within one SE of the best CV error.
- **Nested cross-validation**: tuning inside an inner loop, scoring in an outer one.
- **k-nearest neighbours**: predict by averaging (or voting among) the k closest training cases.
- **Curse of dimensionality**: in many dimensions, neighbourhoods are no longer local and distances concentrate.
- **Bayes rule, Bayes error**: the best possible classifier when the distributions are known, and its error.
- **Generative vs discriminative**: modelling p(x | y) and p(y), or P(y | x) directly.
- **Naive Bayes**: a generative classifier that treats features as independent within each class.
- **Classification tree (CART); impurity; cost-complexity pruning**: recursive axis-parallel splits, scored by Gini or
  squared error, cut back by a penalty α per leaf.
- **Ridge regression; the lasso; soft thresholding**: ℓ₂ and ℓ₁ penalties on coefficients; the lasso's coordinate
  update.
- **Confusion matrix; recall (sensitivity); precision; specificity**: the four outcomes of a classifier and the rates
  built from them.
- **ROC curve; AUC**: recall against false-positive rate across thresholds, and the area under it.
- **Precision–recall curve**: precision against recall across thresholds, for rare positives.
- **Calibration; Brier score**: predicted probabilities that match observed frequencies; their mean squared error.
- **Leakage**: information from the evaluation data reaching the fitted rule (preprocessing, selection, tuning,
  duplicates, time, target).
- **Holdout reuse; adaptive overfitting**: a test set that degrades as its scores guide choices.

## Where it comes back

| Idea | Returns in |
|---|---|
| a full analysis with an honest held-out check | 20 |
| AIC, BIC and CV compared | 28 |
| smoothers and their degrees of freedom | 29 |
| the lasso in depth | 32 |
| prediction intervals with guarantees (conformal) | 34 |
| the curse of dimensionality, in theory | 51, 52 |
| why test error can be bounded: learning theory | 54 |
| inference after the data chose the model | 56 |
| the Coverage Board | every part; 65 |


## Review clarifications

The stored word-count asset was regenerated from the current Gutenberg eBook 18 and matched all 85 records exactly. The historical feature list is a reproduction aid: literature-based selection using this same corpus means that zero leave-one-out errors are not an independent external validation of feature discovery. Naive Bayes uses equal author priors here; ridge logistic has its fitted intercept. Their probabilities have not been shown to be calibrated by classification accuracy alone.

The covariance penalty uses fresh responses at the same fixed training inputs. The polynomial test curve instead uses new random inputs; high-degree instability between training points is a different risk target. The added same-input expected-risk curve includes approximation bias even when the signal is not in the polynomial space. A training error below the noise variance is possible under a well-specified model and is not proof of harmful overfitting.

Ridge and lasso now use consistent per-observation objectives: ridge minimizes SSE/(2n) + λ||β||²/2, and lasso minimizes SSE/(2n) + λ||β||₁. With XᵀX = nI, their coefficients are β̂/(1+λ) and soft(β̂, λ), respectively. The ridge code multiplies λ by n before calling the toolkit's unnormalized solver. The path axes show −log₁₀λ, so weaker penalties lie to the right. Refitting after lasso removes the explicit penalty, not selection bias.

The tree's CV parameter is a maximum leaf budget. Weakest-link pruning can skip sizes: the selected budget of four yields three actual leaves. Classification impurity in this implementation is Gini; held-out evaluation uses misclassification.

K-neighbour noise variance σ²/k is conditional on training locations. The displayed random-design variance also includes variation in neighbour signal values. Classical U-shaped risk and monotone bias/variance tradeoffs are illustrative patterns rather than universal laws. Universal k-NN consistency assumes IID observations, fixed finite dimension, k→∞ and k/n→0.

The Board and nested-CV comparison now use exact one-dimensional population risk. For the known sinusoid-plus-linear signal and uniform future inputs, k-neighbour predictions are constant between (xᵢ+xᵢ₊ₖ)/2 boundaries; integrating their squared errors avoids noise from a shared finite reference test set. Board coverage is 90.15%; the nested example has mean CV minimum 0.1075, exact selected-fit risk 0.1094, and outer-CV loss 0.1153. Outer fits use 80 observations rather than 100. Bates et al.'s specialized nested variance interval is distinct from ordinary nested tuning/evaluation.

Precision–recall curves evaluate complete tied-score groups and retain full recall. Binned calibration is a limited diagnostic. The cost curves are retrospective empirical averages, with minima near but not equal to calibrated-risk thresholds; choose costs and thresholds before a final independent test. Evaluation splits must follow the intended target: new patients require patient grouping, whereas closed-set authorship necessarily includes known authors on both sides.
