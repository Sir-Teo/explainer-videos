# Statistics, Built — Part 54: Statistical Learning Theory

Part 54 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the twelfth part of Stage IV, the PhD core: the last course before the qualifying exam.

It opens in Moscow in 1971, where Vladimir Vapnik and Alexey Chervonenkis asked when the empirical risk converges to
the true risk uniformly over a class of rules, and answered with shattering. The part asks why fitting data generalizes
at all, and why modern interpolating models seem to break the answer:
- empirical risk minimization, uniform convergence, realizable and agnostic PAC learning (Valiant 1984), structural risk
  minimization and the no-free-lunch theorem;
- VC bounds by symmetrization and Sauer–Shelah (proved), matching lower bounds, pseudo- and fat-shattering dimensions,
  and selection on the Board;
- Rademacher complexity: symmetrization, the contraction lemma, Massart's lemma, linear and kernel classes, deep
  networks' norm-based bounds;
- localization and fast rates: Massart and Tsybakov noise, the Bernstein condition, the fixed point, nonparametric
  regression's critical radius;
- margins: AdaBoost on the breast cancer data, the margin bound, boosting as a statistician reads it, SVMs and sample
  compression;
- PAC-Bayes: McAllester's and Maurer's bounds for a Gibbs posterior, the Gibbs variational identity and its distinction from a bounded-loss guarantee,
  non-vacuous bounds for deep networks;
- stability: ridge regression, SGD (Hardt, Recht & Singer 2016), differential privacy and the reusable holdout;
- online learning: Hedge, online-to-batch, bandits (UCB1, EXP3, Lai–Robbins), online convex optimization and mirror
  descent;
- classification-calibrated surrogates, ψ-transforms, noise conditions and proper losses;
- interpolation: double descent, benign overfitting, and why uniform convergence cannot explain it (Nagarajan & Kolter
  2019).

It keeps three promises:
- **Part 48**'s uniform laws, VC classes and chaining were studied for their own sake. Chapters 1–4 turn them into the
  risk of the rule you chose.
- **Part 34** calibrated and conformalized predictions by experiment, for a fixed model. Chapters 5–9 say why the
  learning algorithm itself generalizes.
- **Part 53**'s Gibbs posteriors for misspecified models get PAC-Bayes bounds in chapter 6.

**Built in this part:**
- **`statkit.slt`** ([`explainer/stats/kit/slt.py`](../../../explainer/stats/kit/slt.py)), tested in
  `tests/test_stats_kit_slt.py`:
  - thresholds: data and exact risk; local checked ERM and exact deviation at all grouped jump limits; VC, Rademacher and finite-class bounds;
  - Rademacher complexity of linear and kernel classes by Monte Carlo against their trace bounds;
  - AdaBoost with decision stumps, recording training and test error and normalized margins;
  - PAC-Bayes: binary KL and its inverse, McAllester's and the kl bound, Gibbs posteriors over a finite class;
  - stability: bounded ridge sampled replacement-loss diagnostics; coupled SGD mean divergence with Monte Carlo errors;
  - online learning: Hedge and its bound; Bernoulli bandits with UCB1, EXP3 and ε-greedy; Lai–Robbins's bound;
  - ψ-transforms of the hinge, logistic, exponential and squared losses;
  - interpolation: latent excess prediction risk of min-norm fits, finite simulated averages and exact expected risks away from the singular range; verified interpolation in the benign design.
- **The shatterer** (`Shatterer` in `explainer/stats/viz.py`), the part's instrument: a panel of labelled points with a
  separating half-plane clipped to the frame, or a cross where no half-plane realizes the labelling, so that a whole
  set of dichotomies can be laid out and counted.

**Data.**
- From the Museum: the Wisconsin breast cancer data (569 tumours, 30 features).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains three rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Wald interval on the training error | best of 1,000 classifiers, n = 200 | 95% | 0% | broken |
| Hoeffding + union bound over the class | best of 1,000 classifiers, n = 200 | 95% | 99.8% | conservative |
| Wald interval on a fresh holdout | best of 1,000 classifiers, n = 200 | 95% | 94.0% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats54.compute   # once (a few minutes)
python tools/build.py stats54 -q l                         # fast 480p preview
python tools/build.py stats54                              # 1080p30 -> renders/stats54.mp4
python tools/qa_scene.py stats54 Online
python tools/lecture_length.py stats54 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Vapnik and Chervonenkis | half-planes on n random points: 2, 4, 8, 14, 22, 32, 44, 58, 74 labellings (2ⁿ = 512 at n = 9; Sauer's bound 130); four points in a square: 14 of 16 |
| 1 | ERM | thresholds, n = 25 → 1,600: excess risk 0.039 → 0.0006 (realizable), 0.050 → 0.0026 (η = 0.4); uniform deviation 0.17 → 0.021 |
| 2 | VC bounds | VC bound 1.72 → 0.26, Rademacher bound 1.16 → 0.20 for d = 1; union half-width 0.163 for K = 1,000, n = 200; Board as above |
| 3 | Rademacher | linear class 0.221 → 0.034 (bound 0.225 → 0.036); Gaussian kernel 0.200 → 0.035 (bound 0.200 → 0.035) for n = 25 → 800 |
| 4 | Localization | excess risk slopes ≈ −1 against the deviation's −½, for noise 0, 0.1 and 0.4 |
| 5 | Margins | breast cancer, 340 train / 229 test: tie-safe stumps: zero training error at round 9; test error 0.0742 at round 9 → 0.0437 at round 400; minimum margin −0.178 (5), 0.178 (50), 0.215 (400) |
| 6 | PAC-Bayes | 101 thresholds, n = 500, noise 0.15: best kl bound 0.211 (λ = 200, true risk 0.155) vs union bound 0.221; McAllester 0.234 |
| 7 | Stability | bounded ridge, n = 200, p = 50: sampled loss changes 0.1316 → 0.000492 and signed gap 0.04695 → −0.002540 over λ = 10⁻³ → 3 (10 datasets); SGD divergence after 10 epochs 0.16 (η = 0.2; bound 4) and 0.27 (η = 1; bound 20) |
| 8 | Online learning | Hedge, K = 50, T = 5,000: regret 51.7 vs bound 98.9; bandits, T = 50,000: ε-greedy 1,193, EXP3 962, UCB1 269, Lai–Robbins 75 |
| 9 | Surrogates | ψ(θ) = \|θ\| (hinge), θ² (squared), 1 − √(1 − θ²) (exponential) |
| 10 | Interpolation | min-norm least squares, n = 100: 12-dataset mean latent excess risk 1.14 (p = 10), 1,392 (p = n), 0.925 (p = 1,000); population mean is infinite at p = n−1, n, n+1; benign excess 0.191 → 0.013 for n = 50 → 400; short tail 0.246 |
| 11 | Outro | — |

## Sources

- **Foundations.** V. Vapnik & A. Chervonenkis, *Theory Probab. Appl.* 16 (1971); N. Sauer, *J. Comb. Theory A* 13
  (1972); S. Shelah, *Pacific J. Math.* 41 (1972); L. Valiant, *CACM* 27 (1984); A. Blumer, A. Ehrenfeucht,
  D. Haussler & M. Warmuth, *JACM* 36 (1989); A. Ehrenfeucht, D. Haussler, M. Kearns & L. Valiant, *Inf. Comput.* 82
  (1989); D. Wolpert, *Neural Comput.* 8 (1996).
- **Capacity.** P. Bartlett & S. Mendelson, *JMLR* 3 (2002); V. Koltchinskii, *IEEE Trans. Inf. Theory* 47 (2001);
  M. Ledoux & M. Talagrand, *Probability in Banach Spaces* (1991); P. Massart, *Ann. Fac. Sci. Toulouse* 9 (2000);
  D. Haussler, *J. Comb. Theory A* 69 (1995); N. Alon, S. Ben-David, N. Cesa-Bianchi & D. Haussler, *JACM* 44 (1997);
  P. Bartlett, D. Foster & M. Telgarsky, *NeurIPS* (2017); N. Golowich, A. Rakhlin & O. Shamir, *COLT* (2018).
- **Fast rates.** P. Massart & É. Nédélec, *Ann. Stat.* 34 (2006); A. Tsybakov, *Ann. Stat.* 32 (2004); P. Bartlett,
  O. Bousquet & S. Mendelson, *Ann. Stat.* 33 (2005); V. Koltchinskii, *Ann. Stat.* 34 (2006); P. Bartlett &
  S. Mendelson, *PTRF* 135 (2006).
- **Margins.** Y. Freund & R. Schapire, *JCSS* 55 (1997); R. Schapire, Y. Freund, P. Bartlett & W. S. Lee, *Ann. Stat.*
  26 (1998); J. Friedman, T. Hastie & R. Tibshirani, *Ann. Stat.* 28 (2000); J. Friedman, *Ann. Stat.* 29 (2001);
  C. Cortes & V. Vapnik, *Mach. Learn.* 20 (1995); N. Littlestone & M. Warmuth (1986).
- **PAC-Bayes.** D. McAllester, *Mach. Learn.* 37 (1999); A. Maurer (2004); O. Catoni, *PAC-Bayesian Supervised
  Classification* (2007); P. Germain, F. Bach, A. Lacoste & S. Lacoste-Julien, *NeurIPS* (2016); G. K. Dziugaite &
  D. Roy, *UAI* (2017).
- **Stability.** O. Bousquet & A. Elisseeff, *JMLR* 2 (2002); M. Hardt, B. Recht & Y. Singer, *ICML* (2016);
  C. Dwork, V. Feldman, M. Hardt, T. Pitassi, O. Reingold & A. Roth, *Science* 349 (2015).
- **Online learning.** N. Cesa-Bianchi, A. Conconi & C. Gentile, *IEEE Trans. Inf. Theory* 50 (2004); M. Zinkevich,
  *ICML* (2003); E. Hazan, A. Agarwal & S. Kale, *Mach. Learn.* 69 (2007); A. Nemirovski & D. Yudin (1983); P. Auer,
  N. Cesa-Bianchi & P. Fischer, *Mach. Learn.* 47 (2002); P. Auer, N. Cesa-Bianchi, Y. Freund & R. Schapire, *SIAM J.
  Comput.* 32 (2002); T. L. Lai & H. Robbins, *Adv. Appl. Math.* 6 (1985).
- **Surrogates.** T. Zhang, *Ann. Stat.* 32 (2004); P. Bartlett, M. Jordan & J. McAuliffe, *JASA* 101 (2006);
  A. Tewari & P. Bartlett, *JMLR* 8 (2007); J. Platt (1999).
- **Interpolation.** C. Zhang, S. Bengio, M. Hardt, B. Recht & O. Vinyals, *ICLR* (2017); M. Belkin, D. Hsu, S. Ma &
  S. Mandal, *PNAS* 116 (2019); M. Belkin, D. Hsu & J. Xu, *SIAM J. Math. Data Sci.* 2 (2020); T. Hastie, A. Montanari,
  S. Rosset & R. Tibshirani, *Ann. Stat.* 50 (2022); P. Bartlett, P. Long, G. Lugosi & A. Tsigler, *PNAS* 117 (2020);
  T. Liang & A. Rakhlin, *Ann. Stat.* 48 (2020); M. Belkin, A. Rakhlin & A. Tsybakov, *AISTATS* (2019); V. Nagarajan &
  J. Kolter, *NeurIPS* (2019).
- **Data.** W. Wolberg, W. Street & O. Mangasarian, Wisconsin Diagnostic Breast Cancer (1995).
- **Books.** S. Shalev-Shwartz & S. Ben-David, *Understanding Machine Learning* (2014); F. Bach, *Learning Theory from
  First Principles* (2024); M. Mohri, A. Rostamizadeh & A. Talwalkar, *Foundations of Machine Learning* (2018);
  M. Wainwright, *High-Dimensional Statistics* (2019), ch. 4, 13, 14; V. Vapnik, *Statistical Learning Theory* (1998);
  N. Cesa-Bianchi & G. Lugosi, *Prediction, Learning, and Games* (2006).

## Problems and solutions

1. **Two VC dimensions.**
   - Intervals shatter two points a < b: ∅, {a}, {b} and {a, b} are each cut out by an interval. For three points
     a < b < c, the labelling (+, −, +) needs an interval containing a and c but not b, which is impossible. So the VC
     dimension is 2.
   - Half-planes shatter any three points not on a line: every subset of a triangle's vertices is separated from the
     rest by a line. For four points, either one lies inside the triangle of the others (it cannot be labelled
     differently from all three) or they form a convex quadrilateral (the two diagonals' labelling, + − + − around the
     hull, cannot be separated: Radon's theorem). So the VC dimension is 3.
2. **The finite-class bound.**
   - For each h, Hoeffding gives P(|R_n(h) − R(h)| > t) ≤ 2e^{−2nt²}.
   - A union bound over K rules gives P(sup_h |R_n − R| > t) ≤ 2Ke^{−2nt²}.
   - Set this to δ and solve: t = √(log(2K/δ)/(2n)).
3. **Linear classes.**
   - sup_{‖w‖≤B} ⟨w, Σσᵢxᵢ⟩/n = B‖Σσᵢxᵢ‖/n by Cauchy–Schwarz.
   - By Jensen, E‖Σσᵢxᵢ‖ ≤ (E‖Σσᵢxᵢ‖²)^{1/2} = (Σ‖xᵢ‖²)^{1/2}, since the cross terms have mean zero.
4. **The realizable threshold.**
   - Let the truth be t₀ and let A₊ = [t₀, t₀ + ε′] carry probability ε (similarly A₋ below t₀).
   - ERM's threshold lies within the sample points nearest t₀, so if the risk exceeds ε then no sample point fell in A₊ or
     none fell in A₋.
   - Each has probability (1 − ε)ⁿ; a union bound gives 2(1 − ε)ⁿ ≤ 2e^{−nε}, so the risk is O(log(1/δ)/n).
5. **Hedge's regret.**
   - Let W_t = Σₖ e^{−ηL_{t,k}}. Then log(W_{t+1}/W_t) = log E_{w_t} e^{−ηℓ_t(k)} ≤ −η w_t·ℓ_t + η²/8 by Hoeffding's lemma.
   - Summing: log W_{T+1} − log K ≤ −η·(your loss) + η²T/8.
   - And log W_{T+1} ≥ −η min_k L_{T,k}. Rearranging: regret ≤ log K/η + ηT/8.
6. **The hinge's ψ.**
   - At a point with η = η(x), the conditional hinge risk of a prediction f is η(1 − f)₊ + (1 − η)(1 + f)₊, which is
     minimized over f ∈ [−1, 1] at sign(2η − 1), with value 1 − |2η − 1|.
   - A prediction with the wrong sign has hinge risk at least 1 (at f = 0), an excess of at least |2η − 1|, which is
     exactly the excess 0–1 risk at that point. So ψ(θ) = |θ|.

## Glossary

- **Capacity.**
  - Shattering; growth function; VC dimension; Sauer–Shelah; pseudo-dimension; fat-shattering; covering number:
    counting.
  - Rademacher complexity; symmetrization; contraction; Massart's lemma; Gaussian complexity: fitting noise.
- **Learning.**
  - ERM; realizable; agnostic; PAC; structural risk minimization; oracle inequality; no free lunch.
  - Excess risk; slow and fast rates; Massart noise; Tsybakov noise; Bernstein condition; local Rademacher complexity;
    critical radius.
- **Algorithms.**
  - Margin; AdaBoost; gradient boosting; SVM; support vector; sample compression.
  - Gibbs posterior; PAC-Bayes; kl inverse; uniform stability; differential privacy; reusable holdout.
  - Regret; Hedge; online-to-batch; bandit; UCB; EXP3; online gradient descent; mirror descent.
- **Losses and interpolation.**
  - Surrogate; classification-calibrated; ψ-transform; proper loss.
  - Interpolation; double descent; min-norm interpolator; benign overfitting; effective rank; implicit bias.

## Where it comes back

- **Part 55**: the qualifying exam's learning-theory problem.
- **Part 57**: conformal guarantees, distribution-free.
- **Part 58**: online learning becomes betting: e-values.
- **Part 59**: exact risks of interpolators in proportional asymptotics.
- **Part 64**: the generalization of foundation models.

## QA reconciliation

The scenes use [checked.py](checked.py) for the corrected local algorithms. The shared historical `slt` kit retains its original outputs; its threshold deviation uses a grid and its ridge diagnostic measures prediction changes. The local code uses actual loss changes and exact threshold jumps instead. Twenty-three checks pass (17 local cases and six legacy checks), including independent brute-force tied-stump optimization, narrow-angle LP separability, threshold jump limits, endpoint KL inversion, a counterexample to a pathwise SGD interpretation, inverse-Wishart risk versus independent least-squares simulations, and verified interpolation residuals. All twelve numerical inputs were regenerated. All 17,070 breast-cancer feature values and 569 diagnoses match the primary UCI data in row order.

AdaBoost no longer considers cuts inside an equal-feature block. Such a cut cannot be realized by its saved threshold and previously supplied the wrong weighted error to the coefficient update. Every selected stump's error is now checked directly against its predictions. Zero ensemble scores predict +1. This repair changes the first zero-error round from 12 to 9 and final holdout error from 0.0480 to 0.0437. More rounds need not monotonically improve normalized margins or prevent overfitting; this is one fixed split, not a statistical comparison across training samples.

The ridge example now has feature radius at most one and responses bounded by one. It measures the maximum squared-loss change over twenty sampled replacements and 2,000 validation points, then averages over ten datasets. This is a diagnostic and does not estimate the supremum over all datasets, neighbours and test points. Stored empirical Monte Carlo errors describe the diagnostic and the signed test-minus-training gap separately. A conservative uniform loss bound, 4(1+1/√λ)²/(λn), follows by bounding each half-loss gradient and strong convexity; it can be very loose. The signed asinh chart retains negative gaps instead of dropping them. The high-probability stability formula uses the replacement bounded-difference coefficient 2nβ+M.

Coupled logistic SGD uses the same iid index stream for both datasets, bounded feature norms and step size at most eight. The HRS divergence bound is in expectation over this randomness. It is not pathwise: selecting the changed record on the first step can exceed 2η/n. Every retained path is independently checked against 2η times its actual number of visits to the changed record. Forty paths, sampled index-visit counts and pointwise Monte Carlo errors are retained. Zero mean divergence is a missing log-scale point rather than log(0) or an invented positive value.

The interpolation curve measures latent excess prediction risk, excluding irreducible new-response noise 0.25. The 1,392 peak is a twelve-draw average, not an estimate of a finite population mean. Gaussian inverse-Wishart theory gives infinite mean excess risk at p = n−1, n and n+1. Away from this range the exact mean is retained and drawn as a broken dashed reference, with model-omission variance included. Individual draws and medians are saved; no finite-variance Monte Carlo claim is made at the singularity. The benign experiment verifies every numerical training residual, retains all four per-cell risks and MCSEs, and holds the total tail variance at ten when comparing the long and short tails. Large effective rank alone is not sufficient: small bias and both rank conditions, as well as the design/noise assumptions, matter.

Bounds now state their independent-data, fixed-class, bounded-loss and relevant model conditions. Optimism is in expectation. Probability bounds and expectation bounds are distinguished in the threshold chart. One-sided Rademacher symmetrization is distinguished from absolute deviation, and selecting a margin level requires a simultaneous margin argument. Network bounds depend on depth, activation, input radius and controlled norms. Massart/Tsybakov fast-rate statements require the Bayes rule in the class or an appropriate excess-loss Bernstein condition; regression's squared-distance identity is restricted to the well-specified case. Localization uses the excess-loss star hull and a sub-root upper bound, not an arbitrary function class fixed point.

PAC-Bayes controls Gibbs risk for independent priors and bounded losses, not automatically a deterministic majority vote. Binary KL preserves endpoint support exactly. The Gibbs variational objective and nonlinear bound optimization are distinct. The chart's coefficient of empirical risk differs by n from the later learning-rate convention. Unbounded likelihood loss and model evidence need a separate exponential-moment theorem. Flatness alone does not imply small prior-relative KL. Privacy-based holdout reuse requires a mechanism and a query/privacy budget; one-nearest-neighbour is not generically uniformly stable.

Hedge uses mixture loss; randomized action statements require a non-anticipating adversary. The clipped-uniform simulated expert's expected advantage is 0.095, not 0.1. Bandit paths are mean pseudo-regrets with stored ten-run errors. Lai–Robbins is an asymptotic instance-dependent reference, not a finite-time lower envelope. Online-to-batch uses convex averaging or a randomized mixture. Convex regret rates also need bounded domains/gradients and suitable schedules.

Logistic loss and its calibration transform both use bits. The ψ chart now uses nonnegative excess risks. Calibration includes differentiability at zero for the convex derivative criterion and compares against unrestricted score optima; restricted-model approximation error remains relevant. The noise-assisted exponent is scoped to the displayed quadratic-calibration losses. Proper composite loss identifies a linked population probability, not automatic finite-sample calibration. The final hinge exercise asks for the correct domination inequality, removing an erroneous extra factor of |2η−1|. The Board is a constructed fixed class with independent Bernoulli error coordinates, reports empirical dataset-level MCSE, and distinguishes independent holdout selection from the Wald interval's approximate coverage.

Forty-two persistent theorem headings and local segment clipping prepare the visual pass. The recorded English sampled visual checkpoint is complete. Chinese narration/captions, continuous listening and final masters remain open.
