# Statistics, Built — Part 60: Robustness and Distribution Shift

Part 60 of [the 65-part course](../README.md). The central question is which assumptions let a statistical procedure survive contamination or deployment shift.

The ImageNetV2 hook concerns the **MatchedFrequency** collection: evaluated models lost 11–14 percentage points of top-one accuracy. Benchmark gains generally transferred, but preserved rankings do not establish absence of adaptive overfitting. Collection variants have different gaps.

The chapters cover halfspace depth, efficient robust means, list decoding, heavy tails, covariate and label shift, DRO, causal invariance, transfer and shift detection. Their numerical examples have narrower scopes than the referenced theorems:

- Angular sweeps calculate planar closed-halfplane depth at each query. The 50-by-50 grid search approximates the depth median; it is not an exact global maximizer or the high-dimensional minimax algorithm.
- Deterministic spectral trimming removes five percent of extreme projections per iteration. It illustrates one planted-cluster attack and is not a certified adversarial filter. Four replicates and empirical Monte Carlo errors are saved.
- K-means supplies four candidates in a separated-cluster illustration. General bounded-covariance list decoding has an order-one-over-root-alpha accuracy scale; that is not the Gaussian minimax lower bound.
- The heavy-tail experiment uses a geometric median of 30 block means, not the covariance-optimal tournament estimator. Its empirical 99th percentiles from 400 runs have order-statistic uncertainty.
- Huber mixtures and strong sample corruption have different computational guarantees. The strong/TV statistical-query barrier must not be applied to Huber mixtures, which admit order-epsilon algorithms.

## Empirical examples and calibration

NHANES is a **fixed, unweighted complete-case empirical extract** of 5,176 adults, with age top-coded at 80. Pressure averages available SBP readings. It is not a survey-weighted national estimand. Source and unlabelled reference draws are independent, with replacement. Selection probability is proportional to exp(-(age-18)/20); the correctly specified log ratio is linear in age.

| Procedure | Repetitions | Result | Nominal 95% interval coverage (Monte Carlo SE) |
|---|---:|---|---|
| Unweighted source mean, n=600 | 400 | 118.450, SD 0.677; empirical target 126.187 | 0.00% (0.00 percentage points) |
| Logistic-ratio weighted mean | 400 | 126.242, SD 1.242; mean Kish ESS 267.6 | 95.25% (1.06 points) |
| Classify-and-count prevalence | 300 | 0.6424; target .70 | 72.00% (2.59 points) |
| Projected BBSE prevalence | 300 | 0.6993, SD 0.0699 | 92.33% (1.54 points) |

The weighted interval uses a **joint logistic-ratio/Hajek sandwich**, centered separately within fixed source and target strata. It includes ratio fitting and the 2,000-point reference sample. Its normal approximation requires correct specification, overlap and regularity. Kish ESS diagnoses concentration; it is not an exact information count for heterogeneous outcomes and estimated weights. Plotted sampling curves are Gaussian fits.

The biopsy experiment is semi-synthetic. Each classifier trains on 250 biopsies; independent 150-point source calibration and 100-point target samples are drawn from a shared remaining class-conditional reservoir, with replacement. Labels have source prevalence 0.3726 and target probability .70, with fluctuating realized counts. This makes label shift exact conditional on the empirical reservoir. BBSE enforces the simplex and checks identifiability. The 100-resample percentile bootstrap is approximate: its observed undercoverage is retained. EM averages 0.6871; narrower spread does not establish posterior calibration. These are not clinical validation results.

For DRO, young-only training-loss balls cannot certify older-group membership just because a risk curve crosses a group's observed loss. The displayed curves are comparisons. Separate **all-adult empirical** calculations verify membership: for a group of base mass p, D_chi2(P(.|G)||P)=(1/p-1)/2 and D_KL=-log p. Both robust risks are checked against the group's empirical risk. Scalar KKT solves record feasible primal weights, divergences and dual gaps; no future-population guarantee is implied.

ICP uses Gaussian linear coefficient-invariance and residual-variance F tests with multiplicity corrections. Its no-false-parent probability requires valid testing of the true-parent model and an unchanged outcome mechanism. Anchor regression agrees with unique 2SLS in the infinite-penalty limit only when the projected design identifies the coefficients; the plotted example is underidentified for IV. The zero label represents gamma=1e-9.

Transfer shows a simplified one-source pooled-lasso/residual-correction core over 40 repetitions, with paired draws and Monte Carlo errors. Five coordinate shifts of .15 or 1 have total l-one contrast .75 or 5. It does not implement adaptive multi-source aggregation.

Detection uses a pooled label-invariant Gaussian-kernel bandwidth and plus-one permutation p-values. The statistic can be negative. The shifted example has MMD squared 0.1192, p=0.00332; the null comparison p=0.950. Held-out classifier accuracy 0.670, p=9.19e-10, uses the exact conditional **hypergeometric**, rather than binomial, law for balanced labels. Risk monitoring needs labels or additional assumptions.

## Build and verification

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m videos.stats.stats60.compute --force
pytest -q tests/test_stats60_checked.py tests/test_stats_kit_shift.py
python tools/build.py stats60 -q l
python tools/lecture_length.py stats60 --floor 50
```

All 11 computed inputs regenerated; **24 tests pass** (17 audited local checks, seven legacy checks). Estimated English narration: 51.7 minutes. [Audited kernels](checked.py) are used by this part; the shared statkit contains the earlier educational implementations. The instrument is DepthMap.

[Scientific QA and data/proof receipts](../../../docs/qa/evidence/stats60-polish-20261107/README.md). English sampled visual verification is pending. Chinese narration/caption tables, continuous listening/playback and final masters remain open; this checkpoint is not bilingual production approval.

## Sources

- **The hook.** B. Recht, R. Roelofs, L. Schmidt & V. Shankar, ICML (2019).
- **Depth.** J. Tukey, *Proc. ICM* (1975); D. Donoho & M. Gasko, *Ann. Stat.* 20 (1992); M. Chen, C. Gao & Z. Ren,
  *Ann. Stat.* 46 (2018).
- **Efficient robustness.**
  - I. Diakonikolas, G. Kamath, D. Kane, J. Li, A. Moitra & A. Stewart, FOCS (2016);
  - K. Lai, A. Rao & S. Vempala, FOCS (2016);
  - I. Diakonikolas, D. Kane & A. Stewart, FOCS (2017);
  - I. Diakonikolas & D. Kane, *Algorithmic High-Dimensional Robust Statistics* (2023).
- **List decoding.** M. Charikar, J. Steinhardt & G. Valiant, STOC (2017).
- **Heavy tails.**
  - A. Nemirovski & D. Yudin (1983); N. Alon, Y. Matias & M. Szegedy, STOC (1996);
  - S. Minsker, *Bernoulli* 21 (2015);
  - L. Devroye, M. Lerasle, G. Lugosi & R. Oliveira, *Ann. Stat.* 44 (2016);
  - G. Lugosi & S. Mendelson, *Ann. Stat.* 47 (2019) and *Found. Comput. Math.* 19 (2019);
  - S. Hopkins, *Ann. Stat.* 48 (2020); O. Catoni, *Ann. IHP* 48 (2012).
- **Covariate shift.**
  - H. Shimodaira, *J. Stat. Plan. Inference* 90 (2000); L. Kish, *Survey Sampling* (1965);
  - J. Huang, A. Smola, A. Gretton, K. Borgwardt & B. Schölkopf, NeurIPS (2006);
  - M. Sugiyama et al., *Ann. Inst. Stat. Math.* 60 (2008).
- **Label shift.**
  - G. Forman, ECML (2005);
  - M. Saerens, P. Latinne & C. Decaestecker, *Neural Computation* 14 (2002);
  - Z. Lipton, Y.-X. Wang & A. Smola, ICML (2018);
  - B. Schölkopf et al., ICML (2012).
- **DRO.**
  - A. Ben-Tal, D. den Hertog, A. De Waegenaere, B. Melenberg & G. Rennen, *Management Science* 59 (2013);
  - J. Duchi & H. Namkoong, *JMLR* 20 (2019) and *Ann. Stat.* 49 (2021);
  - P. Mohajerin Esfahani & D. Kuhn, *Math. Programming* 171 (2018);
  - J. Blanchet & K. Murthy, *Math. Oper. Res.* 44 (2019); J. Blanchet, Y. Kang & K. Murthy, *J. Appl. Prob.* 56 (2019);
  - S. Sagawa, P. W. Koh, T. Hashimoto & P. Liang, ICLR (2020);
  - T. Hashimoto, M. Srivastava, H. Namkoong & P. Liang, ICML (2018);
  - W. Hu, G. Niu, I. Sato & M. Sugiyama, ICML (2018).
- **Invariance.**
  - J. Peters, P. Bühlmann & N. Meinshausen, *JRSS B* 78 (2016);
  - D. Rothenhäusler, N. Meinshausen, P. Bühlmann & J. Peters, *JRSS B* 83 (2021);
  - M. Arjovsky, L. Bottou, I. Gulrajani & D. Lopez-Paz, arXiv:1907.02893 (2019);
  - E. Rosenfeld, P. Ravikumar & A. Risteski, ICLR (2021);
  - I. Gulrajani & D. Lopez-Paz, ICLR (2021).
- **Transfer.**
  - S. Ben-David, J. Blitzer, K. Crammer, A. Kulesza, F. Pereira & J. Vaughan, *Machine Learning* 79 (2010);
  - S. Kpotufe & G. Martinet, *Ann. Stat.* 49 (2021); T. Cai & H. Wei, *Ann. Stat.* 49 (2021);
  - S. Li, T. Cai & H. Li, *JRSS B* 84 (2022);
  - Y. Ganin et al., *JMLR* 17 (2016); H. Zhao, R. Tachet des Combes, K. Zhang & G. Gordon, ICML (2019).
- **Detection.**
  - A. Gretton, K. Borgwardt, M. Rasch, B. Schölkopf & A. Smola, *JMLR* 13 (2012);
  - D. Lopez-Paz & M. Oquab, ICLR (2017);
  - S. Rabanser, S. Günnemann & Z. Lipton, NeurIPS (2019);
  - A. Podkopaev & A. Ramdas, ICLR (2022);
  - F. Liu et al., ICML (2020).
- **Open problems.** P. W. Koh et al. (WILDS), ICML (2021); J. Miller et al., ICML (2021).
- **Data.** A. Azzalini & A. Bowman, *Appl. Stat.* 39 (1990); NHANES (CDC); W. Wolberg, W. Street & O. Mangasarian
  (1995).


- **Contamination-model distinction.** Diakonikolas, Kane, Pensia & Pittas, NeurIPS (2023), [arXiv:2312.01547](https://arxiv.org/abs/2312.01547), especially Theorem 1.3 and section 1.3.
## Problems and solutions

1. **Contaminated scalar median.** For epsilon<1/2 and added mass at positive infinity, (1-epsilon)Phi(m)=1/2. Hence m=Phi^-1(1/[2(1-epsilon)])=sqrt(pi/2) epsilon+O(epsilon^2). Coordinate biases can accumulate in Euclidean norm under a common-coordinate attack.
2. **Importance weights and ESS.** If Q_X is absolutely continuous with respect to P_X and the conditional outcome law is unchanged, integration gives E_P[w f]=E_Q[f]. Conditional on fixed covariates, independent outcomes with a constant conditional mean and variance sigma squared give Var(sum(wY)/sum w)=sigma squared sum(w squared)/(sum w) squared. Without constant mean/variance, or with estimated weights, this is not the full Hajek variance.
3. **Adjusted counts.** E[q_CC]=q TPR+(1-q)FPR. If TPR differs from FPR, q=(E[q_CC]-FPR)/(TPR-FPR). Binary BBSE gives the same moment equation. Estimated rates and projection produce sampling uncertainty and possible finite-sample bias; singular confusion matrices do not identify prevalence.
4. **Chi-square DRO.** Under (n/2)sum(q_i-1/n)^2<=rho, Cauchy-Schwarz bounds risk by mean(loss)+sqrt(2 rho Var_n(loss)). Equality holds for weights proportional to the centered loss perturbation while all weights remain nonnegative. At larger radii positivity binds; the checked KKT solver handles that regime.
5. **Anchor limits.** Since P_A is an orthogonal projection, W=I-(1-sqrt(gamma))P_A gives the criterion ||W(y-Xb)|| squared. At gamma=1 this is OLS. As gamma grows, minimization first prioritizes ||P_A(y-Xb)|| squared. A unique limit equals 2SLS if X'P_A X is invertible; otherwise a further criterion can select among projected-loss minimizers and there is no unique IV coefficient vector.
6. **Classifier odds.** In a pool of n0 source and n1 target draws, Bayes membership c=n1 q/(n0 p+n1 q). Therefore (n0/n1)c/(1-c)=q/p, with the orientation and class proportions specified. Fitted classifier probabilities need to approximate this posterior for the equality to be useful.

## Where it comes back

Part 61 studies optimal transport; Part 62 transports causal effects; Part 63 relates robustness and privacy; Part 64 examines large-model behavior; Part 65 revisits robustness in research.
