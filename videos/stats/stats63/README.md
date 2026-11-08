# Statistics, Built — Part 63: Privacy and Fairness

Part 63 of [the 65-part course](../README.md), on differential privacy, statistical inference after privacy noise, census post-processing, private learning and competing fairness criteria.

The historical Weld linkage illustrates how removing names can fail. NHANES uniqueness is **within the unweighted 5,176-adult complete-case extract**, not a demonstrated linkage or population re-identification rate. Age is top-coded at 80 and pressure averages available readings. Successful external linkage additionally requires comparable measurements, inclusion knowledge and an identified source.

## Audited examples

[Local checked kernels](checked.py) preserve the shared educational kit while repairing this part's computations.

- **Definition and accounting:** state add/remove versus fixed-size replace-one adjacency and match sensitivity to it. Delta is additive event slack, not generally a probability of an unprotected operating mode. The pure-DP posterior-odds reading concerns fixed neighboring alternatives, not all correlated secrets under arbitrary whole-database priors. Gaussian GDP curves and independent Gaussian-shift composition can be exact; generic GDP and zCDP guarantees need not attain equality. Privacy CLTs and subsampling amplification have conditions and finite-step errors. For Gaussian RDP, continuous optimization gives exactly the usual zCDP-to-DP expression; a grid artifact no longer separates them.
- **Cost:** vectorize sufficient-statistic simulations without changing marginal binomial/randomized-response experiments and save Monte Carlo errors. The local effective-size heuristic is scoped to small-epsilon proportion estimation, not every high-dimensional problem. Equating the displayed risks d/n and d² log(1/delta)/(n² epsilon²) gives **n=d log(1/delta)/epsilon²**, about **11,513** at d=1,000, epsilon=1, delta=1e-5. The old 3,400 crossover was algebraically wrong. Tail classes and logarithmic factors matter for minimax claims.
- **Intervals:** retain the *raw* noisy proportion as center; clip only the plug-in sampling variance. The exact variance decomposition applies before output clipping. The variance-corrected Wald interval remains approximate, particularly when Laplace noise dominates. The Board's 2,000 trials give 85.4% naive versus 95.2% noise-aware coverage; this does not certify every parameter or budget. Publish mechanism and parameters, not the realized noise alongside the answer.
- **Census:** distinguish rounded continuous Gaussian noise in this toy from the actual discrete Gaussian mechanism. Replace independent rounding with largest-remainder rounding of the nonnegative projection, so all 200 integer releases preserve the exact total (**maximum total error 0**). Tiny-block bias is +0.638 people (MC SE 0.023); total-weighted biases sum to zero. This is a fixed-public-total illustration, not calibrated TopDown. Real invariants are outside ordinary neighboring-record protection and are not free post-processing of confidential totals. Rho=2.63 converts to epsilon≈18.2 at delta=1e-10; a continuous-Gaussian comparison's mu≈2.29 is **not** an exact census GDP guarantee or demonstrated attack power.
- **Private logistic learning:** remove data-fitted full-sample centering/scaling. Use fixed feature units and pointwise clipping; under fixed-size replace-one adjacency the clipped-gradient sum has sensitivity **2C**. Correct Gaussian noise to 2C sqrt(60/(2rho)). All budgets use the same ten random train/test splits. Each model has its own budget; repeated models and public-data accuracy diagnostics are not one jointly private release. Accuracy at epsilon 0.37 is 0.789, at 1.21 is 0.912; clipped nonprivate baseline 0.944. Descriptive split SDs do not establish performance equivalence. Audit lower bounds account for delta and rate uncertainty; unsuccessful attacks do not prove privacy.
- **COMPAS:** independently reproduce all **6,172** filtered primary rows, including 5,278 Black/white defendants, exactly for six retained columns. Descriptive error-rate and approximate predictive-parity patterns coexist; neither group PPVs nor every score-cell outcome rate are exactly equal. Distinguish full-score independence/separation/sufficiency from one-threshold versions, and sufficiency from numerical calibration. Decile labels are not probabilities. Algebraic identities are subject to nonzero denominators; PPV=1 with false negatives need not be perfect classification. Unequal base rates alone do not force every chosen threshold to violate equalized odds.
- **Multicalibration:** empirical stopping concerns eligible cells in a specified class, not all computable subgroups. Patches replay exactly. The reported test gap is a weighted **average** absolute residual, not the worst violation; it falls 0.03843→0.03062, while the white-group gap rises 0.02855→0.03432. Twenty overlapping random halves describe split variability, not independent-population uncertainty. Unsigned gaps cannot establish over- or underprediction. Generalization requires complexity, confidence and cell-mass control; omniprediction is relative to specified losses and comparator classes.
- **Causal fairness:** ordinary group residuals need not be counterfactually invariant. Replace the rounded/clipped prior count with an explicit continuous additive measurement index and known structural group effect 1.2. Train on 10,000 people; evaluate on **20,000 independent people**, using paired interventions with shared background factors. Subtracting the known structural effect gives maximum paired score change 2.2e-16; the raw index's mean paired change is 0.09307. A small group-average gap alone is not a counterfactual-fairness proof. Held-out AUCs are 0.6424 and 0.6557, conditional on the specified toy.

## Build and evidence

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m videos.stats.stats63.compute --force
pytest -q tests/test_stats63_checked.py tests/test_stats_kit_privacy.py
python tools/build.py stats63 -q l
python tools/lecture_length.py stats63 --floor 50
```

All 14 chapters reviewed, all 12 inputs regenerated and **20 checks pass** (14 local, six legacy). Estimated English narration: **69.9 minutes**. [Evidence](../../../docs/qa/evidence/stats63-polish-20261107/README.md). The recorded English sampled visual checkpoint is complete; Chinese narration/captions, continuous listening/playback and final masters remain open.

## Sources

- **The hook.**
  - L. Sweeney, *J. Law Med. Ethics* 25 (1997); Sweeney, "Simple demographics often identify people uniquely",
    Carnegie Mellon Data Privacy Working Paper 3 (2000); Sweeney, *Int. J. Uncertainty, Fuzziness and Knowledge-Based
    Systems* 10 (2002); P. Golle, WPES (2006).
  - A. Narayanan & V. Shmatikov, IEEE S&P (2008); N. Homer et al., *PLoS Genetics* 4 (2008); I. Dinur & K. Nissim,
    PODS (2003).
  - J. Angwin, J. Larson, S. Mattu & L. Kirchner, "Machine Bias", ProPublica (2016); W. Dieterich, C. Mendoza &
    T. Brennan, Northpointe (2016).
- **Differential privacy.**
  - C. Dwork, F. McSherry, K. Nissim & A. Smith, TCC (2006); S. Warner, *JASA* 60 (1965);
  - C. Dwork & A. Roth, *Found. Trends Theor. Comput. Sci.* 9 (2014); B. Balle & Y.-X. Wang, ICML (2018);
  - F. McSherry & K. Talwar, FOCS (2007).
- **Testing and accounting.**
  - L. Wasserman & S. Zhou, *JASA* 105 (2010); P. Kairouz, S. Oh & P. Viswanath, ICML (2015);
  - J. Dong, A. Roth & W. Su, *JRSS B* 84 (2022);
  - C. Dwork, G. Rothblum & S. Vadhan, FOCS (2010); I. Mironov, CSF (2017); M. Bun & T. Steinke, TCC (2016).
- **The cost of privacy.** J. Duchi, M. Jordan & M. Wainwright, FOCS (2013) and *JASA* 113 (2018); T. Cai, Y. Wang &
  L. Zhang, *Ann. Statist.* 49 (2021).
- **Private inference.**
  - V. Karwa & S. Vadhan, ITCS (2018); C. Ferrando, S. Wang & D. Sheldon, AISTATS (2022);
  - M. Gaboardi, H. W. Lim, R. Rogers & S. Vadhan, ICML (2016); J. Awan & A. Slavković, NeurIPS (2018).
- **The census.**
  - J. Abowd et al., *Harvard Data Science Review*, Special Issue 2 (2022); the 2020 redistricting data's ρ = 2.63
    (2.56 persons, 0.07 housing units);
  - U.S. Census Bureau, release of the 2020 redistricting noisy measurement file (15 June 2023);
  - C. Kenny et al., *Science Advances* 7 (2021); *Alabama v. U.S. Department of Commerce* (M.D. Ala., three-judge
    court, June 2021);
  - J. Abowd & I. Schmutte, *American Economic Review* 109 (2019).
- **Private learning.**
  - M. Abadi et al., CCS (2016); N. Carlini et al., USENIX Security (2021); R. Shokri et al., IEEE S&P (2017);
  - N. Carlini et al., IEEE S&P (2022); M. Jagielski, J. Ullman & A. Oprea, NeurIPS (2020); M. Nasr et al., IEEE S&P
    (2021); T. Steinke, M. Nasr & M. Jagielski, NeurIPS (2023);
  - E. Bagdasaryan, O. Poursaeed & V. Shmatikov, NeurIPS (2019).
- **Fairness.**
  - S. Barocas, M. Hardt & A. Narayanan, *Fairness and Machine Learning* (MIT Press, 2023);
  - M. Hardt, E. Price & N. Srebro, NeurIPS (2016); A. Flores, K. Bechtel & C. Lowenkamp, *Federal Probation* 80
    (2016);
  - A. Chouldechova, *Big Data* 5 (2017); J. Kleinberg, S. Mullainathan & M. Raghavan, ITCS (2017; arXiv 2016);
  - S. Corbett-Davies, E. Pierson, A. Feller, S. Goel & A. Huq, KDD (2017).
- **Multicalibration.**
  - U. Hébert-Johnson, M. Kim, O. Reingold & G. Rothblum, ICML (2018); M. Kim, A. Ghorbani & J. Zou, AIES (2019);
  - C. Dwork et al., STOC (2021); P. Gopalan et al., ITCS (2022); I. Gibbs, J. Cherian & E. Candès, arXiv:2305.12616.
- **Causal fairness.**
  - M. Kusner, J. Loftus, C. Russell & R. Silva, NeurIPS (2017); N. Kilbertus et al., NeurIPS (2017);
  - R. Nabi & I. Shpitser, AAAI (2018); I. Kohler-Hausmann, *Northwestern Univ. Law Rev.* 113 (2019);
  - L. Liu, S. Dean, E. Rolf, M. Simchowitz & M. Hardt, ICML (2018).
- **Open problems.** T. Raghunathan, J. Reiter & D. Rubin, *J. Official Statistics* 19 (2003); D. Ensign et al.,
  FAT* (2018).

## Problems and solutions

1. **Randomized response.**
   - For a report r, P(r | x = 1)/P(r | x = 0) is π/(1 − π) or (1 − π)/π. With π = e^ε/(1 + e^ε), both lie in
     [e^{−ε}, e^ε], so the mechanism is ε-DP.
   - The report is 1 with probability q = πp + (1 − π)(1 − p) = (2π − 1)p + (1 − π). So
     p̂ = (q̂ − (1 − π))/(2π − 1) is unbiased.
   - Var(p̂) = q(1 − q)/(n(2π − 1)²).
2. **The Laplace mechanism.**
   - The output densities are (ε/2Δ)exp(−ε|z − f(D)|/Δ) and the same with f(D′).
   - Their ratio is exp(ε(|z − f(D′)| − |z − f(D)|)/Δ) ≤ exp(ε|f(D) − f(D′)|/Δ) ≤ e^ε, by the triangle inequality and
     the definition of Δ.
   - Integrating over any set S gives the definition.
3. **Gaussian trade-off curves.**
   - The outputs are N(f(D), σ²) and N(f(D′), σ²). Standardizing gives N(0, 1) against N(s/σ, 1), with
     |s| = |f(D) − f(D′)| ≤ Δ.
   - Testing a larger shift is easier, so the worst case is s = Δ and the curve is G_{Δ/σ}.
   - For two independent mechanisms the pair is N(0, I) against N((μ₁, μ₂), I). The likelihood ratio depends only on
     the projection onto (μ₁, μ₂)/‖μ‖, which is N(0, 1) against N(‖μ‖, 1). Thus the independent Gaussian-shift experiment has this exact composed curve. For arbitrary mechanisms merely satisfying the GDP bounds, it is a sharp composition guarantee, not mandatory equality.
4. **When central privacy becomes cheap.**
   - The privacy term is 2/(nε)² and the sampling term is p(1 − p)/n. The privacy share is a tenth when
     2/(nε)² = p(1 − p)/(9n), that is, n = 18/(ε²p(1 − p)).
   - At p = 0.3 and ε = 0.1 this is n ≈ 8,571.
5. **Chouldechova's identity.**
   - The true positives number PPV · H = (1 − FNR)pn, and the false positives (1 − PPV)H = FPR(1 − p)n, where H is the
     number labelled high.
   - Dividing, (1 − PPV)/PPV = FPR(1 − p)/((1 − FNR)p). Solving for FPR gives the identity.
6. **The impossibility.**
   - If both groups have the same PPV and FNR, then FPR_a/FPR_b = [p_a/(1 − p_a)]/[p_b/(1 − p_b)], provided the
     common factor (1 − PPV)(1 − FNR)/PPV is not zero.
   - The odds differ when the base rates differ, so the FPRs differ.
   - The factor vanishes only if PPV = 1, when both FPRs are zero, or FNR = 1, when the classifier catches no one and
     the identity degenerates. PPV=1 does not require perfect prediction: some positives may still be missed. At FNR=1 with no true positives, positive PPV can be undefined or zero, and the displayed division requires separate treatment.


## Next

Part 64 examines statistics for AI-generated predictions, labels, benchmarks and data.
