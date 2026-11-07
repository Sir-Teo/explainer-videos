# Statistics, Built — Part 62: Frontiers of Causal Inference

Part 62 of [the 65-part course](../README.md). It studies identification, sensitivity, proximal methods, interference, policies and regimes, discovery, transport and surrogates. Each replaces an assumption with other explicit assumptions.

The HIV-CAUSAL hook distinguishes **20,971 eligible adults from 8,392 analyzed after CD4 declined into the 200–499 range**. Its four reported hazard ratios and intervals agree with Cain et al. (2011). Follow-up began below 500, and initiation strategies included a six-month grace period. Death-only intervals containing one do not demonstrate equivalent safety of waiting. START randomized 4,685 adults with CD4>500; its composite of serious AIDS, serious non-AIDS events or all-cause death had HR .43 (.30–.62). Its interim treatment recommendation in 2015 broadly supported earlier therapy, while its population, regimes and endpoints differed from the emulation. Agreement does not validate every observational assumption.

## Audited examples

[Local checked kernels](checked.py) drive this part. The [shared educational statkit](../../../explainer/stats/kit/frontier.py) remains available; its earlier approximations are not silently presented as the audited implementation. ExposureMap is the visual instrument.

- **Front door:** verify all four treatment–mediator cells before evaluating the binary formula. Causal interpretation requires the specified graph, positivity and consistency. Completeness of do-calculus and ID is scoped to the relevant acyclic nonparametric latent-variable model, not every causal question. Hedges need not be literal bow graphs.
- **Sensitivity:** sorting computes exact extrema of the *finite Hajek weight box*. These relaxed bounds omit conditional compatibility constraints and are not the population-sharp Tan identified set. The propensity fit is checked, 8.14% of probabilities are clipped to [.01,.99], and 200 treatment-stratified bootstrap resamples refit scaling and the propensity model. Endpoint intervals are illustrative bootstrap approximations, not a universal causal ATE certificate. Experimental earnings differences are estimated benchmarks, not known truths. No uncomputed strongest-confounder or motivation benchmark is claimed.
- **Proximal 2SLS:** apply the instrument projection without an n-by-n matrix, check identification and use HC1 sandwich errors. Save first-stage robust F, partial R-squared and projected-design condition numbers. Proxy exclusions, bridge existence/completeness, latent exchangeability and overlap are essential; two correlated proxies alone do not identify an effect.
- **Interference:** use exact Bernoulli probabilities by degree. Isolated units retain zero probability for neighbor-treated exposures. The spillover contrast uses the 390 nonisolates; direct-alone comparisons use common support among all 400 units. Under the stated any-treated-neighbor model, a unit-specific Horvitz–Thompson estimator **can** estimate global all-treated versus none. Its true mean is 3 minus the isolated fraction, 2.975. Repeated-assignment SDs also include fresh outcome noise and are not IID standard errors.
- **Policy evaluation:** remove leakage from two-fold nuisance fitting into the learned policy. Each run now has **400 policy observations plus 400 independent nuisance-training outcomes**, with known randomization probability .5. Learn on 200 policy units and evaluate on the other 200 conditional on the independent nuisance fit. Optimize whole tied groups and include constant rules. Coverage includes equality at zero-width intervals for an exactly zero policy gain. The target is the randomly learned rule's population gain, not the oracle's gain. The representative chart optimizes its displayed upper-threshold subfamily; the coverage experiment uses both directions.
- **Dynamic regimes:** retain full stage-two history, including the first-treatment-by-initial-state reward. A linear first-stage Q remains a working approximation. Evaluate all five policies on 200,000 common fresh simulation states with final outcome noise integrated out; save value and paired-difference Monte Carlo errors conditional on one fitted regime. Randomization supplies sequential exchangeability, while consistency, positivity, model correctness and follow-up still matter.
- **Discovery:** compute a PC-stable skeleton with frozen adjacency at each depth, neighbor sets from both endpoints and no three-variable cutoff. This does not implement CPDAG orientation. Match the cited varsortability implementation's Boolean reachability-by-path-length aggregation and half-credit ties; standardization gives **0.50**, rather than floating-point artifacts. NOTEARS is not run in this demonstration, and standardization need not remove every covariance shortcut. Interventions can show ancestral influence without proving a direct edge.
- **Transport:** use known simulated selection odds as an oracle example. The target is each repetition's nonparticipant population; its true average effect is stored per repetition. The previous comparison used a different whole-pool target. A sufficient conditional-effect-invariance set is needed, rather than every conceivable modifier. Selection diagrams and sample-membership indicators play different roles; outcome-level invariance and contrast invariance can differ.
- **Surrogates:** include index-fit variance from the independent observational sample in a two-sample delta SE. The bypass example violates both surrogacy and cross-sample conditional-mean comparability, rather than isolating one failure. Statistical Prentice conditions are not equivalent to a simplistic all-paths-through-S graph. Principal-stratum average criteria do not assert individual-level causal implications.

## Numerical checkpoint

| Example | Revised result |
|---|---|
| Relaxed earnings sensitivity | IPW -341.55; exact envelope reaches zero at Lambda 1.08105, experimental benchmark at 1.60662 |
| Proximal, 600 samples of 1,000 | mean 1.0245, coverage 95.33% (MC SE 0.86 percentage points) |
| Network, 300 assignment/noise repetitions | direct 2.003, spillover 0.987, global total HT 2.958 versus truth 2.975 |
| Learned policy, 800 repetitions | in-sample coverage 79.12%; independent split 93.62%; biases +0.07468 and +0.00066 |
| One learned two-stage regime | value 0.86494 (MC SE 0.00449); oracle 0.88311 |
| PC-stable skeleton, 30 graphs | recall 0.7613, precision 0.9352; raw path-based variance-order score 0.9762 |
| Oracle-odds transport, 200 trials | estimate 1.4901; mean nonparticipant truth 1.5239; error -0.0338 (MC SE 0.0147) |
| Surrogate index | valid 1.6439 (SE 0.1193), truth 1.55; bypass 1.5799 (SE 0.1200), truth .55 |

The transport error is retained rather than described as exact recovery; normalized weights can have finite-sample bias. Policy Wald coverage is a finite Monte Carlo finding and an asymptotic approximation, not distribution-free finite-sample coverage. All four Board rows record empirical Monte Carlo standard errors.

NSW data were independently compared again to the Matching and MatchIt distributions: all covariates agree exactly, stored earnings within half a cent. The comparison group follows MatchIt's documented PSID label; the original historical panel records and full LaLonde specification were not independently reconstructed. CAST counts are quoted from the primary report verified in Part 58, not from patient-level records.

## Build and verification

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m videos.stats.stats62.compute --force
pytest -q tests/test_stats62_checked.py tests/test_stats_kit_frontier.py
python tools/build.py stats62 -q l
python tools/lecture_length.py stats62 --floor 50
```

All 10 inputs regenerated; **20 checks pass** (14 audited local and six legacy). All narration/list bookmarks match their rows. Estimated English narration is 51.3 minutes. [QA evidence](../../../docs/qa/evidence/stats62-polish-20261107/README.md). The recorded English sampled visual checkpoint is complete. Chinese narration/caption tables, continuous listening/playback and final narrated masters remain open; this checkpoint is not bilingual production approval.

## Sources

- **The hook.** HIV-CAUSAL Collaboration (L. Cain et al.), *Ann. Intern. Med.* 154 (2011); INSIGHT START Study Group,
  *NEJM* 373 (2015).
- **Identification.**
  - J. Pearl, *Biometrika* 82 (1995); J. Tian & J. Pearl, AAAI (2002);
  - Y. Huang & M. Valtorta, AAAI (2006); I. Shpitser & J. Pearl, AAAI (2006);
  - A. Balke & J. Pearl, *JASA* 92 (1997);
  - I. Fulcher, I. Shpitser, S. Marealle & E. Tchetgen Tchetgen, *JRSS B* 82 (2020);
  - J. Pearl & D. Mackenzie, *The Book of Why* (2018).
- **Sensitivity.**
  - C. Manski (1990); Z. Tan, *JASA* 101 (2006); Q. Zhao, D. Small & B. Bhattacharya, *JRSS B* 81 (2019);
  - J. Dorn & K. Guo, *JASA* 118 (2023); C. Cinelli & C. Hazlett, *JRSS B* 82 (2020);
  - T. VanderWeele & P. Ding, *Ann. Intern. Med.* 167 (2017);
  - R. LaLonde, *AER* 76 (1986); R. Dehejia & S. Wahba, *JASA* 94 (1999).
- **Proximal.**
  - W. Miao, Z. Geng & E. Tchetgen Tchetgen, *Biometrika* 105 (2018);
  - E. Tchetgen Tchetgen, A. Ying, Y. Cui, X. Shi & W. Miao, arXiv:2009.10982 (2020);
  - Y. Cui, H. Pu, X. Shi, W. Miao & E. Tchetgen Tchetgen, *JASA* (2023);
  - M. Lipsitch, E. Tchetgen Tchetgen & T. Cohen, *Epidemiology* 21 (2010).
- **Interference.**
  - P. Aronow & C. Samii, *Ann. Appl. Stat.* 11 (2017); M. Leung, *Econometrica* 90 (2022);
  - M. E. Halloran & C. Struchiner, *Epidemiology* (1991, 1995); M. Hudgens & M. E. Halloran, *JASA* 103 (2008);
  - J. Ugander et al., KDD (2013); S. Baird et al., *REStat* 100 (2018); M. Ali et al., *Lancet* 366 (2005).
- **Policy learning.**
  - T. Kitagawa & A. Tetenov, *Econometrica* 86 (2018); S. Athey & S. Wager, *Econometrica* 89 (2021);
  - I. Andrews, T. Kitagawa & A. McCloskey, *QJE* 139 (2024); M. Dudík, J. Langford & L. Li, ICML (2011).
- **Regimes.**
  - J. Robins, *Math. Modelling* 7 (1986) and (2004); S. Murphy, *JRSS B* 65 (2003) and *Stat. Med.* 24 (2005);
  - M. Hernán & J. Robins, *Am. J. Epidemiol.* 183 (2016).
- **Discovery.**
  - P. Spirtes & C. Glymour, *Soc. Sci. Comput. Rev.* 9 (1991); T. Verma & J. Pearl (1990);
  - C. Uhler, G. Raskutti, P. Bühlmann & B. Yu, *Ann. Stat.* 41 (2013);
  - S. Shimizu et al., *JMLR* 7 (2006); P. Hoyer et al., NeurIPS (2009); J. Peters & P. Bühlmann, *Biometrika* 101 (2014);
  - A. Hauser & P. Bühlmann, *JMLR* 13 (2012); X. Zheng et al., NeurIPS (2018);
  - A. Reisach, C. Seiler & S. Weichwald, NeurIPS (2021); J. Robins et al., *Biometrika* 90 (2003).
- **Transport.**
  - J. Pearl & E. Bareinboim, AAAI (2011); E. Bareinboim & J. Pearl, *PNAS* 113 (2016);
  - I. Dahabreh et al., *Biometrics* 75 (2019) and *Stat. Med.* (2020); D. Westreich et al., *Am. J. Epidemiol.* (2017);
  - N. Kallus, A. Puli & U. Shalit, NeurIPS (2018); R. Meager, *AEJ: Applied* 11 (2019).
- **Surrogates.**
  - R. Prentice, *Stat. Med.* 8 (1989); T. VanderWeele, *Biometrics* 69 (2013);
  - C. Frangakis & D. Rubin, *Biometrics* 58 (2002);
  - S. Athey, R. Chetty, G. Imbens & H. Kang, NBER Working Paper 26463 (2019);
  - D. Echt et al., *NEJM* 324 (1991).
- **Open problems.** V. Veitch, D. Sridhar & D. Blei, UAI (2020); B. Schölkopf et al., *Proc. IEEE* 109 (2021).

## Problems and solutions

1. **Front door.** Under the specified graph and positivity, identify P(m|do(a))=P(m|a); identify P(y|do(m)) by averaging P(y|m,a') over P(a'); combine through the mediator, which intercepts every directed treatment–outcome path. The formula does not follow from mediation alone without the back-door conditions.
2. **Weight box.** Inverse propensity is one plus the odds against the observed arm. Bounding the full-versus-measured propensity odds ratio in [1/Lambda,Lambda] yields [1+(1/e-1)/Lambda,1+(1/e-1)Lambda]. These necessary bounds alone omit conditional compatibility constraints; optimizing the box is a relaxation of the population model.
3. **Linear proximal moments.** If Y=b0+bA A+gamma U+epsilon and W=U+eta, then Y=b0+bA A+gamma W+(epsilon-gamma eta). Under valid proxy noise/exclusion assumptions the instruments (1,A,Z) are orthogonal to that error. A full-rank projected design then yields consistent 2SLS coefficients; the equation and rank condition need to hold, not merely marginal proxy correlation.
4. **Bernoulli direct effect.** Under the stated exposure model and independent assignments, a unit's neighbors' treatment is independent of its own treatment. Therefore E[Y_i|Z_i=1]-E[Y_i|Z_i=0]=2. Finite arm means have random denominators and possible ratio bias; this identity is not a claim of exact finite-sample Hajek unbiasedness. A spillover contrast requires common positive exposure support.
5. **Winner's curse.** For a fixed class with unbiased fixed-policy value estimates, Jensen's inequality gives E sup_pi Vhat(pi)>=sup_pi V(pi). Also E V(pihat)<=sup_pi V(pi), so expected selected in-sample optimism is nonnegative. Truly independent evaluation, conditional on independent nuisance training, removes this selection reuse; normal intervals still need distributional/regularity conditions.
6. **Inverse odds.** Let p(x) be membership in a trial rather than its nonparticipant target in a common population. The two covariate laws are proportional to p(x)f(x) and (1-p(x))f(x); their density ratio is proportional to (1-p)/p. Normalized weighting cancels the constant. Targeting the entire baseline population instead would use inverse selection probabilities, not the same inverse odds. Causal transport additionally needs treatment randomization/exchangeability, consistency, conditional effect invariance and overlap.

## Where it comes back

Part 63 considers fair decisions and privacy; Part 64 studies causal questions about AI systems; Part 65 revisits research design and causal claims.
