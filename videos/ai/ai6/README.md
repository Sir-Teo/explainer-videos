# AI, Built — Part 6: Classical ML

Part 6 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)),
and the start of Act II, *Learning from Data*. One task runs through it: who wrote this page, Jane Austen or Charles
Dickens? Pages are 1,000-word chunks of five of Part 1's novels (639 pages: *Pride and Prejudice* and *Emma*;
*A Tale of Two Cities*, *Great Expectations* and *A Christmas Carol*), each described, as Mosteller and Wallace
described the Federalist papers, by how often it uses the 70 commonest words; 30% of the pages (191) are held out.
The 70-word lexicon is fixed from the complete five-novel corpus without author labels before splitting; this is
an unsupervised benchmark definition shared with Parts 7, 8 and 11. Classifier parameters and learned scalers use
training pages only. The holdout evaluates new chunks from these same five novels, not previously unseen novels.
The pictures use two of the numbers: how often a page says "the", and how often it says "not". Every method is
written out in numpy in `compute.py` (no machine-learning library), every random choice is seeded, and every number
on screen or in the narration is computed there. The numbers below are from the reference run (Linux, numpy 2.5);
another machine can move the last digits, and the narration follows its own run.

About 51 minutes; a hook, seventeen chapters and an outro.

The evaluation is conditional on that fixed dictionary and five-novel corpus. Training/test curves over penalties,
depths or rounds are descriptive diagnostics; they are not independent test sets at every point. Training-only
cross-validation chooses the stated settings. The final contest compares twelve named, fixed procedures on the
same folds; it is not a comparison at equal computational budgets, and tied mean scores are reported as ties.

The LDA inset whitens the actual pooled within-author covariance with its inverse square root. It connects the
means in whitened coordinates, then pulls that normal back with the transpose of the whitening map, giving the
full inverse-covariance mean direction. Agreement with least squares means coefficient direction, not necessarily
the same intercept or decision threshold. The positive maximizing eigenpair is distinct from zero-eigenvalue
stationary directions. The Gaussian-kernel truncation check is one-dimensional, with gamma 1 and both inputs on
a 61-point grid in [-1.5, 1.5]; its error is not a dimension-independent/global approximation guarantee.

ROC area credits a tied positive/negative score pair by one half. Log loss is computed stably from out-of-fold
logits in nats per page without a probability-clipping cap; probabilities are still used for reliability diagrams
and Brier scores. The large-sample qualifier on the nearest-neighbor error bound also applies to the recap.

## Outline

* **Hook: who wrote this page?** A page; its fingerprint of small words (Mosteller & Wallace, 1963–64); the 639
  pages as points; how we got here, from Legendre (1805) to TabPFN (2025); the plan.
* **1. Least squares.** Three points and the squares on their misses (Legendre 1805; Gauss and Ceres, 1801); the fit
  as Gauss's maximum likelihood under bell-shaped noise (1809), derived; as a perpendicular projection onto the
  plane of every line's predictions (3D), and the normal equations (Part 3 owns the projection mechanics); Zipf's law on Part 1's 4.33 million words: slope −1.08, R² = 0.996.
* **2. The best linear unbiased line.** The Gauss–Markov theorem (Gauss 1821, Markov 1900) derived:
  Var β̃ = σ²(AᵀA)⁻¹ + σ²DDᵀ. Checked by 40,000 simulated data sets: least squares' slope variance 0.0103 (theory
  0.0104), the end-point slope's 0.0244 (theory 0.0247), both unbiased. Outside the theorem: Theil–Sen (median of
  pairwise slopes, not linear) loses with Gaussian noise (0.0115) and wins with heavy-tailed noise of the same
  variance (0.0067 against 0.0101). Solving it: κ(A) = 9.7 on the pages squares to 93 in AᵀA; normal equations and
  QR agree to 2 × 10⁻¹⁵; with "not" duplicated (rank 71 of 72), the normal equations return weights of size 10¹⁵,
  while the pseudoinverse splits the weight exactly in half. Least squares as a classifier: 191 of 191 held-out pages.
* **3. Ridge.** Hoerl & Kennard (1970). Derived through the SVD: the fit along direction j is scaled by
  d_j²/(d_j² + λ). The 70 singular values of the standardized pages (63.4 down to 6.6), with 91% of the authorship
  signal along the first two directions; the shrinkage factors as λ grows; effective weights Σ d²/(d² + λ); the 70
  coefficient paths (smooth, but not necessarily monotone in each coordinate); ridge as the MAP estimate under a
  Gaussian prior, and weight decay. The near-zero count refers to sampled coefficient/penalty pairs below a
  numerical tolerance, not mathematically exact zeros.
  Ten-fold cross-validation (mean ± 1 s.e.) picks λ ≈ 75 (54 effective weights), 99.5% on the held-out pages.
* **4. The lasso.** Tibshirani (1996): the diamond's corner; the soft threshold derived from subgradients;
  coordinate descent (Friedman, Hastie & Tibshirani, glmnet 2010) along 61 penalties, KKT conditions checked at every
  one (worst violation 1.6 × 10⁻⁹); the first eight words (not, she, very, be, out, such, to, mrs) give 90%; the
  ten-fold cross-validated error curve (± 1 s.e.) is lowest at 57 words and nearly flat there, and the
  one-standard-error rule keeps 46 words (99.5%). Zou & Hastie's elastic net (2005) on a near-copy of "not": the lasso
  picks one twin, the elastic net shares.
* **5. Logistic regression.** Score, line and sigmoid; the probability sheet with the pages lifted to 0 and 1 (3D);
  cross-entropy 0.51 bits per page; convexity derived (gradient Xᵀ(p − y), Hessian XᵀSX/n ⪰ 0; eigenvalues at the
  answer 0.043, 0.050, 0.119); gradient descent replayed, the line swinging into place; 82% with two rates, 190 of 191
  with seventy.
* **6. Newton's method.** Newton = iteratively reweighted least squares (Nelder & Wedderburn 1972), derived; Newton
  against gradient descent on the plane, step by step; on all 70 rates Newton reaches the minimum to machine precision
  in 8 steps, gradient descent needs 1,000 steps to get within 10⁻⁶; the correct digits per Newton step
  (… 4.3, 7.1, 12.6: roughly doubling, quadratic convergence). With 70 rates the training pages are separable:
  as the penalty weakens 10⁶-fold the weights grow from 1.2 to 12.0 without end (Soudry et al. 2018: gradient descent
  then turns toward the max-margin direction).
* **7. Naive Bayes.** Multinomial naive Bayes derived: its log-odds are linear in the word counts; generative against
  discriminative; what it learned by counting (Austen: mrs, she, very; Dickens: out, up, me). Ng & Jordan (2002)
  reproduced: over many random training sets, naive Bayes has the lower error up to
  8 pages, logistic regression from 12 pages on, ending at 0.5% against 5.8%. Calibration (ten-fold cross-validated
  probabilities): logistic regression's expected calibration error 0.039; naive Bayes gives 90% of pages odds beyond
  a million to one (ECE 0.042), and Platt scaling (1999) brings it to 0.011.
* **8. Fisher's direction.** Fisher (1936): the separation along every direction, the best one; S_W⁻¹ pictured as
  rounding the clouds; why the cut is Bayes-optimal for two equal-shaped Gaussians (log-odds linear: logistic
  regression's form with Fisher's direction); the generalized eigenproblem S_B w = J S_W w derived; on 70 rates one nonzero eigenvalue
  (S_B has rank 1), its eigenvector equal to the formula and to least squares on a 0/1 target (cosines 1.000000);
  82% with two rates, 100% with seventy.
* **9. Neighbours, and the curse of dimensionality.** Fix & Hodges (1951); a 15-neighbour vote; regions as k grows
  (k = 1: 93% of training pages, 68% of new ones; best on held-out pages at k = 15, 84%; cross-validation picks
  k = 125, 82%). Cover & Hart (1967) sketched: R* ≤ E 2η(1 − η) ≤ 2R*(1 − R*), checked on two Gaussians
  (R* = 21.2%, limit 29.2%, bound 33.4%; 1-NN at n = 10,000: 29.5%; √n neighbours: 21.5%). The curse (Bellman 1957):
  the nearest of 2,000 points in a cube is 0.1% of the average distance in 1D and 94% in 1,000D; a cube holding 10% of
  the data has side 0.79 in 10D; adding 1,000 noise columns drops 15-NN from 98% to 88%, logistic regression only from
  99.5% to 97%.
* **10. Kernels.** Rosenblatt's perceptron (1958) and Novikoff's bound (1 mistake on the toy, bound 15); XOR: 400
  mistakes in 100 passes; Minsky & Papert (1969); add x₁x₂ and it separates after 4. Circles lifted onto a
  paraboloid (3D), the separating plane found by a hard-margin SVM. The trick: (x·z + 1)² = φ(x)·φ(z), checked to
  10⁻¹⁴; the Gaussian kernel's infinite Taylor features (20 kept: 7 × 10⁻⁸). Mercer (1909): the Gaussian Gram matrix
  on the 448 training pages has no negative eigenvalues (smallest −2 × 10⁻¹⁴, rounding); tanh(x·z − 1) has 138. The
  representer theorem (Kimeldorf & Wahba 1971; Schölkopf, Herbrich & Smola 2001) derived, and checked: ridge in
  2,000 random Gaussian features lies in the span of the pages' features to 2 × 10⁻¹⁴.
* **11. The widest street.** The margin derived (min ½‖w‖²); the toy's 3 support vectors; hinge, logistic,
  exponential and 0–1 losses; the dual derived with Lagrange multipliers and KKT (Part 4 owns them); complementary
  slackness; SMO (Platt 1998; Fan, Chen & Lin's working-set rule) written out and run on the pages with a Gaussian
  kernel: C from 0.01 to 100, support vectors 407 → 169, relative primal-dual gaps up to 3.8 × 10⁻⁶. At C = 1,
  outside/bound margin checks have zero violations at tolerance 10⁻³; the maximum free-margin residual is 5.6 × 10⁻⁵.
  the ten-fold cross-validated grid over C and γ (best 83.9%, 12 of the 25 settings within a point of it, worst
  54.9% at tiny C); cross-validation picks C = 0.1, γ = 0.1 (81% held out); 99.5% with all 70 rates. Cortes & Vapnik (1995).
* **12. Trees.** The learned depth-3 tree and its boxes; Gini, entropy and error rate; why a strictly concave
  impurity always rewards a useful split (Jensen), and the scan of every threshold on "not" (all three pick 8.5);
  accuracy against depth (best held out at depth 4, 83%; cross-validation picks 3; grown fully: 94% train, 74% new).
  CART (Breiman, Friedman, Olshen & Stone 1984). Fragility: depth-3 trees on 20 bootstrap resamples (70 rates) start
  with 3 different words (not 10, mrs 7, she 3) and score 80–93% held out.
* **13. Bagging and random forests.** Var = ρσ² + (1 − ρ)σ²/B derived and checked by simulation (ρ = ½, B = 100:
  0.512 against 0.505); measured on the pages over 30 training sets of 150 pages: bagging ρ = 0.109, σ² = 0.118;
  eight random words ρ = 0.013, σ² = 0.146; two words ρ = 0.007. A forest of 300 (Breiman 2001, after Ho 1995): one
  tree 93.7%, bagging 99.5%, forest 100% (191 of 191); out-of-bag estimate 98%.
* **14. AdaBoost.** Freund & Schapire (1997); the weights piling onto hard pages (2 rates); the exponential-loss
  derivation of α = ½ log((1 − ε)/ε) (Friedman, Hastie & Tibshirani 2000), checked against a numerical search
  (3 × 10⁻⁶); on 70 rates the training error reaches 0 at round 19, with held-out error 3.7%. The observed held-out
  minimum is 0.5% at round 45; the final value at round 400 is 1.6%, so the improvement is not monotone
  (margins: Schapire et al. 1998). Viola & Jones (2001): rectangle features, a boosted cascade, 384 × 288 at 15 frames a
  second on a 700 MHz Pentium III (schematic).
* **15. Gradient boosting, second order.** Friedman (2001); XGBoost's second-order objective, leaf weight
  −G/(H + λ) and split gain derived (Chen & Guestrin 2016), checked on the first split ("mrs" ≤ 0.5: formula 92.797,
  direct evaluation 92.797, true drop 100.55); boosting on the two rates as it learns (best after 4 rounds, 83.2%,
  slipping to 77.5% by 200); on 70 rates Newton leaves reach 0.0066 bits against 0.042 for first-order leaves, 99.0%
  against 95.8% held out.
* **16. Keeping score.** The ROC curve traced by sweeping the threshold (cross-validated logistic regression on two
  rates): AUC 0.9095, equal to the share of correctly ranked (Dickens, Austen) pairs (Mann–Whitney); with Dickens
  made rare (15 pages against 288), "always Austen" is 95% accurate, the ROC area stays 0.91, average precision falls
  from 0.93 to 0.57; accuracy against log loss (ten-fold cross-validated probabilities): Platt scaling leaves naive
  Bayes' 95.6% accuracy unchanged but cuts its log loss from 0.478 to 0.088 nats per page (logistic regression on 70
  rates: 0.034); one 70/30 split's accuracy ranges 77.5–88.5% over 100 splits, ten-fold cross-validation over 20
  shuffles 82.9–83.7%.
* **17. The contest, and two cultures.** Every method on the same ten folds of all 639 pages (mean ± s.d.): with 2
  rates, the tested procedures score 76–83% on these folds, an empirical comparison rather than an information ceiling;
  with 70, logistic regression and the Gaussian SVM 99.5%, the lasso 99.4%, LDA and least squares 99.2%,
  AdaBoost 99.1%, the forest 98.4%, gradient boosting 98.3%, k-NN 98.3%, naive Bayes 95.8%, one tree 93.0%. Breiman's
  two cultures (2001); the Netflix Prize (2006–09), Kaggle (2010), XGBoost in 17 of 29 Kaggle-blog winners of 2015;
  why trees still win on tables (Grinsztajn, Oyallon & Varoquaux 2022); foundation models for tables: TabPFN
  (Hollmann et al., *Nature*, Jan 2025; the reported $2.8$-second comparison is its classification benchmark
  configuration, against an ensemble tuned for four hours), TabPFN-2.5 (Nov 2025), and TabPFN-3 (May 2026;
  its million-row capacity claim is at 200 features, and its TabArena lead is the authors' report). These dates
  identify the cited publications or preprint submissions. The broader June 2026
  [*Beyond IID* benchmark](https://arxiv.org/html/2606.30410v1) tests TabPFN-2.6, not TabPFN-3, and includes model
  authors among its coauthors (see its Competing Interests disclosure). Foundation models are strong on small and
  medium IID tables; traditional tree and deep baselines expose boundary cases on non-IID, large or high-dimensional
  data. These findings are version- and task-specific. The chapter then shows how the classics live on inside today's models (the softmax, linear
  probes and weight decay, sparse autoencoders' L1, the neural tangent kernel and attention as a kernel smoother,
  retrieval, calibration).
* **Outro.** Twelve pictures from the part's results; where it comes back (Parts 7, 8, 9, 11, 13, 31); eight
  problems; Part 7's teaser; references.

## Run

From the repo root:

```
python tools/make.py ai6                 # everything: Part 1's books if missing, the numbers, both languages
python -m videos.ai.ai6.compute          # only the numbers (about 15 CPU-minutes, one core; resumable)
python tools/build.py ai6                # English
python tools/build.py ai6 --lang zh      # Chinese
EXPLAINER_TTS=silent python tools/build.py ai6 -q l --fps 15   # a quick silent preview
```

`compute.py` items are cached in `.cache/ai6/`; the two longest (`bagging`, `board`) save each piece as it finishes
and resume. Other parts read `load("pages")`, `split()` and `standardize()` from here (Parts 7, 8 and 11).

## References

Books: T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning*, 2nd ed. (2009); C. M. Bishop,
*Pattern Recognition and Machine Learning* (2006); K. P. Murphy, *Probabilistic Machine Learning: An Introduction*
(2022); B. Schölkopf & A. Smola, *Learning with Kernels* (2002).

Papers, by chapter: Mosteller & Wallace, *JASA* (1963) and *Inference and Disputed Authorship* (1964); Legendre (1805);
Gauss, *Theoria Motus* (1809) and *Theoria Combinationis* (1821–23); Markov (1900); Moore (1920); Penrose (1955);
Theil (1950); Sen (1968); Hoerl & Kennard (1970); Tibshirani (1996); Zou & Hastie (2005); Friedman, Hastie &
Tibshirani, *Regularization Paths for GLMs via Coordinate Descent* (2010); Berkson (1944); Nelder & Wedderburn (1972);
Soudry et al., *The Implicit Bias of Gradient Descent on Separable Data* (2018); Platt, *Probabilistic Outputs for
SVMs* (1999); Ng & Jordan, *On Discriminative vs. Generative Classifiers* (2002); Fisher, *The Use of Multiple
Measurements in Taxonomic Problems* (1936); Fix & Hodges (1951); Cover & Hart, *Nearest Neighbor Pattern
Classification* (1967); Bellman, *Dynamic Programming* (1957); Rosenblatt (1958); Novikoff (1962); Minsky & Papert,
*Perceptrons* (1969); Mercer (1909); Aizerman, Braverman & Rozonoer (1964); Kimeldorf & Wahba (1971); Schölkopf,
Herbrich & Smola, *A Generalized Representer Theorem* (2001); Boser, Guyon & Vapnik (1992); Cortes & Vapnik,
*Support-Vector Networks* (1995); Platt, *Sequential Minimal Optimization* (1998); Fan, Chen & Lin (2005); Breiman,
Friedman, Olshen & Stone, *CART* (1984); Quinlan (1986); Breiman, *Bagging Predictors* (1996); Ho (1995); Breiman,
*Random Forests* (2001); Freund & Schapire (1997); Schapire, Freund, Bartlett & Lee, *Boosting the Margin* (1998);
Friedman, Hastie & Tibshirani, *Additive Logistic Regression* (2000); Viola & Jones, *Rapid Object Detection using a
Boosted Cascade of Simple Features* (CVPR 2001); Friedman, *Greedy Function Approximation* (2001); Chen & Guestrin,
*XGBoost* (KDD 2016); Breiman, *Statistical Modeling: The Two Cultures* (2001); Grinsztajn, Oyallon & Varoquaux, *Why
do tree-based models still outperform deep learning on typical tabular data?* (NeurIPS 2022); Hollmann et al.,
[*Accurate predictions on small data with a tabular foundation model*](https://www.nature.com/articles/s41586-024-08328-6) (*Nature* 637, Jan 2025); Prior Labs, *TabPFN-2.5*
(arXiv 2511.08667, Nov 2025) and *TabPFN-3* (arXiv 2605.13986, May 2026); Purucker et al., *Beyond IID: How General Are
Tabular Foundation Models, Really?* (arXiv 2606.30410, June 2026).

## Problems

1. For y_i = β₀ + β₁x_i + ε_i, show that the slope through the two end points is unbiased with variance
   2σ²/(x_n − x₁)², and that least squares' is σ²/Σ(x_i − x̄)². Which is smaller?
2. Show that ridge's fit is Σ_j u_j d_j²/(d_j² + λ) u_jᵀy, and that tr Z(ZᵀZ + λI)⁻¹Zᵀ = Σ_j d_j²/(d_j² + λ).
3. Derive the soft threshold from subgradients, and show that the lasso's weights are all zero exactly when
   λ ≥ max_j |z_jᵀy|/n.
4. Show that the logistic loss's Hessian XᵀSX/n is positive semidefinite, and that if a line separates the training
   data, no finite weights minimize the loss.
5. Show that the Gram matrix of K(x, z) = (x·z + 1)² is positive semidefinite, and find a Gram matrix of
   tanh(x·z − 1) with a negative eigenvalue.
6. Derive the dual of the soft-margin SVM, and use complementary slackness to show that α_i = C for every training
   point strictly inside the street.
7. Derive Var((1/B)Σ_b T_b) = ρσ² + (1 − ρ)σ²/B, and AdaBoost's α = ½ log((1 − ε)/ε) from the exponential loss.
8. For the logistic loss, derive XGBoost's leaf weight −G/(H + λ) and split gain, and show that a single leaf at
   p = ½ moves the log-odds by −4G/(n + 4λ).

### Solutions

1. Both are linear in y. The end-point slope is (y_n − y₁)/(x_n − x₁); its mean is (β₁x_n − β₁x₁)/(x_n − x₁) = β₁,
   and since y_n and y₁ are independent with variance σ², its variance is 2σ²/(x_n − x₁)². Least squares' slope is
   Σ(x_i − x̄)y_i / Σ(x_i − x̄)², with mean β₁ (because Σ(x_i − x̄) = 0) and variance σ²/Σ(x_i − x̄)². Since
   Σ(x_i − x̄)² ≥ (x₁ − x̄)² + (x_n − x̄)² ≥ (x_n − x₁)²/2, least squares' variance is never larger — Gauss–Markov in
   miniature. For the chapter's twelve points from 1 to 10: 0.0104σ² against 0.0247σ².
2. With Z = UDVᵀ, ZᵀZ + λI = V(D² + λI)Vᵀ, so w = V(D² + λI)⁻¹DUᵀy and Zw = UD(D² + λI)⁻¹DUᵀy =
   Σ_j u_j d_j²/(d_j² + λ) u_jᵀy. The hat matrix is H = U diag(d_j²/(d_j² + λ)) Uᵀ, whose trace is the sum of the
   factors; at λ = 0 it is the rank, the number of weights.
3. One coordinate minimizes ½(z − w)² + λ|w|. At a minimum, 0 ∈ w − z + λ∂|w|, where ∂|w| = {sign w} for w ≠ 0 and
   [−1, 1] at 0. If w > 0, w = z − λ, needing z > λ; if w < 0, w = z + λ, needing z < −λ; w = 0 works exactly when
   |z| ≤ λ. Together w = sign(z) max(|z| − λ, 0). For the whole lasso (1/2n)‖y − Zw‖² + λ‖w‖₁, w = 0 is optimal iff
   0 ∈ −Zᵀy/n + λ∂‖0‖₁, i.e. |z_jᵀy|/n ≤ λ for every j.
4. With p_i = σ(x_iᵀw), the Hessian is (1/n)Σ p_i(1 − p_i) x_i x_iᵀ, so vᵀHv = (1/n)Σ p_i(1 − p_i)(x_iᵀv)² ≥ 0. If
   y_i(wᵀx_i) > 0 for all i (labels ±1), then along tw the loss Σ log(1 + e^{−t y_i wᵀx_i}) decreases strictly to 0 as
   t → ∞ but is positive for every finite t, so no finite minimizer exists — Chapter 6's runaway weights.
5. (x·z + 1)² = φ(x)·φ(z) with φ = (x₁², x₂², √2x₁x₂, √2x₁, √2x₂, 1) in two dimensions (and similarly in any), so
   aᵀKa = ‖Σ_i a_iφ(x_i)‖² ≥ 0. For tanh: one point x = 0 gives K = tanh(−1) < 0, a 1×1 Gram matrix with a negative
   eigenvalue; the chapter found 138 on the training pages.
6. Lagrangian L = ½‖w‖² + CΣξ_i − Σα_i[y_i(w·x_i + b) − 1 + ξ_i] − Σμ_iξ_i with α, μ ≥ 0. ∂L/∂w = 0 gives
   w = Σα_iy_ix_i; ∂L/∂b = 0 gives Σα_iy_i = 0; ∂L/∂ξ_i = 0 gives α_i + μ_i = C, so 0 ≤ α_i ≤ C. Substituting:
   maximize Σα_i − ½ΣΣα_iα_jy_iy_j x_i·x_j subject to those constraints. Complementary slackness: μ_iξ_i = 0 and
   α_i[y_if(x_i) − 1 + ξ_i] = 0. A point strictly inside the street has y_if(x_i) < 1, so ξ_i > 0, so μ_i = 0 and
   α_i = C.
7. Var((1/B)ΣT_b) = (1/B²)Σ_{b,c}Cov(T_b, T_c) = (1/B²)(Bσ² + B(B − 1)ρσ²) = ρσ² + (1 − ρ)σ²/B. For AdaBoost, with
   weights w_i ∝ e^{−y_iF(x_i)} normalized and weighted error ε, L(α) ∝ (1 − ε)e^{−α} + εe^{α}; L′(α) = 0 gives
   e^{2α} = (1 − ε)/ε.
8. With g_i = p_i − y_i and h_i = p_i(1 − p_i), a leaf of weight w contributes Gw + ½(H + λ)w², minimized at
   w* = −G/(H + λ) with value −½G²/(H + λ). A split replaces one leaf by two, so the gain is
   ½[G_L²/(H_L + λ) + G_R²/(H_R + λ) − (G_L + G_R)²/(H_L + H_R + λ)] − γ. At p = ½ every h_i = ¼, so H = n/4 and
   w* = −G/(n/4 + λ) = −4G/(n + 4λ).

### 习题（中文）

1. 对y_i = β₀ + β₁x_i + ε_i，证明穿过两个端点的斜率是无偏的，方差为2σ²/(x_n − x₁)²，而最小二乘斜率的方差为
   σ²/Σ(x_i − x̄)²。哪个更小？
2. 证明岭回归的拟合是Σ_j u_j d_j²/(d_j² + λ) u_jᵀy，并且tr Z(ZᵀZ + λI)⁻¹Zᵀ = Σ_j d_j²/(d_j² + λ)。
3. 用次梯度推导软阈值，并证明套索回归的权重全为零，当且仅当λ ≥ max_j |z_jᵀy|/n。
4. 证明逻辑回归损失的黑塞矩阵XᵀSX/n是半正定的；并证明若有一条直线能分开训练数据，则不存在有限的最优权重。
5. 证明K(x, z) = (x·z + 1)²的格拉姆矩阵半正定，并找出tanh(x·z − 1)的一个有负特征值的格拉姆矩阵。
6. 推导软间隔支持向量机的对偶问题，并用互补松弛证明：严格位于街道内部的每个训练点都有α_i = C。
7. 推导Var((1/B)Σ_b T_b) = ρσ² + (1 − ρ)σ²/B，并由指数损失推导AdaBoost的α = ½ log((1 − ε)/ε)。
8. 对逻辑损失，推导XGBoost的叶子权重−G/(H + λ)和分割增益，并证明在p = ½时，单片叶子让对数几率移动−4G/(n + 4λ)。

### 解答（中文）

1. 两者都对y是线性的。端点斜率是(y_n − y₁)/(x_n − x₁)，均值为β₁；y_n与y₁独立、方差均为σ²，所以方差是
   2σ²/(x_n − x₁)²。最小二乘斜率是Σ(x_i − x̄)y_i / Σ(x_i − x̄)²，因为Σ(x_i − x̄) = 0，其均值为β₁，方差为
   σ²/Σ(x_i − x̄)²。由于Σ(x_i − x̄)² ≥ (x₁ − x̄)² + (x_n − x̄)² ≥ (x_n − x₁)²/2，最小二乘的方差从不更大：这是
   高斯–马尔可夫定理的缩影。本章1到10上的12个点：0.0104σ²对0.0247σ²。
2. 设Z = UDVᵀ，则ZᵀZ + λI = V(D² + λI)Vᵀ，所以w = V(D² + λI)⁻¹DUᵀy，Zw = Σ_j u_j d_j²/(d_j² + λ) u_jᵀy。
   帽子矩阵H = U diag(d_j²/(d_j² + λ)) Uᵀ，它的迹就是这些因子之和；λ = 0时等于秩，即权重的个数。
3. 单个坐标最小化½(z − w)² + λ|w|。最优处0 ∈ w − z + λ∂|w|，其中w ≠ 0时∂|w| = {sign w}，在0处为[−1, 1]。
   若w > 0，则w = z − λ，要求z > λ；若w < 0，则w = z + λ，要求z < −λ；w = 0恰在|z| ≤ λ时成立。合起来就是
   w = sign(z) max(|z| − λ, 0)。对整个套索回归(1/2n)‖y − Zw‖² + λ‖w‖₁，w = 0最优当且仅当对每个j都有
   |z_jᵀy|/n ≤ λ。
4. 记p_i = σ(x_iᵀw)，黑塞矩阵为(1/n)Σ p_i(1 − p_i) x_i x_iᵀ，所以vᵀHv = (1/n)Σ p_i(1 − p_i)(x_iᵀv)² ≥ 0。若对所有i
   有y_i(wᵀx_i) > 0（标签取±1），则沿tw方向，损失Σ log(1 + e^{−t y_i wᵀx_i})随t → ∞严格减小并趋于0，但对每个有限的
   t都为正，所以不存在有限的最小值点：这就是第6章里跑掉的权重。
5. 在二维中(x·z + 1)² = φ(x)·φ(z)，φ = (x₁², x₂², √2x₁x₂, √2x₁, √2x₂, 1)（任意维同理），所以
   aᵀKa = ‖Σ_i a_iφ(x_i)‖² ≥ 0。对tanh：取单个点x = 0，K = tanh(−1) < 0，就是一个有负特征值的1×1格拉姆矩阵；
   本章在训练页上找到了138个负特征值。
6. 拉格朗日函数L = ½‖w‖² + CΣξ_i − Σα_i[y_i(w·x_i + b) − 1 + ξ_i] − Σμ_iξ_i，α, μ ≥ 0。∂L/∂w = 0得
   w = Σα_iy_ix_i；∂L/∂b = 0得Σα_iy_i = 0；∂L/∂ξ_i = 0得α_i + μ_i = C，所以0 ≤ α_i ≤ C。代回：在这些约束下最大化
   Σα_i − ½ΣΣα_iα_jy_iy_j x_i·x_j。互补松弛：μ_iξ_i = 0，且α_i[y_if(x_i) − 1 + ξ_i] = 0。严格位于街道内部的点有
   y_if(x_i) < 1，所以ξ_i > 0，于是μ_i = 0，α_i = C。
7. Var((1/B)ΣT_b) = (1/B²)Σ_{b,c}Cov(T_b, T_c) = (1/B²)(Bσ² + B(B − 1)ρσ²) = ρσ² + (1 − ρ)σ²/B。对AdaBoost，
   权重w_i ∝ e^{−y_iF(x_i)}归一化后，加权错误率为ε，L(α) ∝ (1 − ε)e^{−α} + εe^{α}；令L′(α) = 0得
   e^{2α} = (1 − ε)/ε。
8. 记g_i = p_i − y_i，h_i = p_i(1 − p_i)，权重为w的一片叶子贡献Gw + ½(H + λ)w²，在w* = −G/(H + λ)处取最小值
   −½G²/(H + λ)。一次分割把一片叶子换成两片，所以增益是
   ½[G_L²/(H_L + λ) + G_R²/(H_R + λ) − (G_L + G_R)²/(H_L + H_R + λ)] − γ。在p = ½时每个h_i = ¼，H = n/4，
   w* = −G/(n/4 + λ) = −4G/(n + 4λ)。

## Glossary

| English | 中文 |
|---|---|
| least squares, normal equations | 最小二乘，正规方程 |
| Gauss–Markov theorem, best linear unbiased estimator (BLUE) | 高斯–马尔可夫定理，最佳线性无偏估计 |
| Theil–Sen estimator | 泰尔–森估计 |
| pseudoinverse (Moore–Penrose) | 伪逆（摩尔–彭罗斯） |
| ridge regression, shrinkage factor, effective number of weights | 岭回归，收缩因子，有效权重数 |
| lasso, soft threshold, coordinate descent, regularization path | 套索回归（Lasso），软阈值，坐标下降，正则化路径 |
| subgradient | 次梯度 |
| one-standard-error rule | 一个标准误规则 |
| elastic net | 弹性网络 |
| logistic regression, sigmoid, convex | 逻辑回归，S形函数（sigmoid），凸的 |
| Hessian | 黑塞矩阵 |
| Newton's method, iteratively reweighted least squares (IRLS), working response | 牛顿法，迭代重加权最小二乘（IRLS），工作响应 |
| generalized linear model | 广义线性模型 |
| separable data | 可分数据 |
| naive Bayes, Laplace smoothing | 朴素贝叶斯，拉普拉斯平滑 |
| generative, discriminative | 生成式，判别式 |
| calibration, reliability diagram, expected calibration error, Platt scaling | 校准，可靠性图，期望校准误差，普拉特缩放 |
| Fisher's linear discriminant (LDA), within-class / between-class scatter | 费希尔线性判别（LDA），类内散度、类间散度 |
| generalized eigenproblem, Rayleigh quotient | 广义特征值问题，瑞利商 |
| k nearest neighbours, Bayes error, Cover–Hart bound | k近邻，贝叶斯错误率，科弗–哈特界 |
| curse of dimensionality | 维数灾难 |
| perceptron, Novikoff's bound, XOR | 感知机，诺维科夫界，异或 |
| kernel, kernel trick, feature map, Gram matrix | 核函数，核技巧，特征映射，格拉姆矩阵 |
| Mercer's theorem, positive semidefinite | 默瑟定理，半正定 |
| Gaussian (RBF) kernel, random Fourier features | 高斯（RBF）核，随机傅里叶特征 |
| representer theorem, kernel ridge regression | 表示定理，核岭回归 |
| support vector machine, margin, support vector | 支持向量机，间隔，支持向量 |
| hinge loss, soft margin | 铰链损失，软间隔 |
| dual problem, KKT conditions, complementary slackness, duality gap | 对偶问题，KKT条件，互补松弛，对偶间隙 |
| sequential minimal optimization (SMO) | 序列最小优化（SMO） |
| decision tree, Gini impurity, split gain | 决策树，基尼不纯度，分割增益 |
| bagging, bootstrap resample, out-of-bag estimate | 装袋法（bagging），自助重抽样，袋外估计 |
| random forest | 随机森林 |
| boosting, AdaBoost, decision stump, exponential loss | 提升法，AdaBoost，决策树桩，指数损失 |
| cascade (Viola–Jones), rectangle (Haar-like) feature | 级联（维奥拉–琼斯），矩形（类哈尔）特征 |
| gradient boosting, second-order (Newton) boosting, leaf weight | 梯度提升，二阶（牛顿）提升，叶子权重 |
| ROC curve, AUC, hit rate, false-alarm rate | ROC曲线，曲线下面积（AUC），命中率，误报率 |
| precision, recall, average precision | 精确率，召回率，平均精确率 |
| cross-validation, held-out set | 交叉验证，留出集 |
| the two cultures (data modeling, algorithmic modeling) | 两种文化（数据建模，算法建模） |
| tabular foundation model | 表格基础模型 |
