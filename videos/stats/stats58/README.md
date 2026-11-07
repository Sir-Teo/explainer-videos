# Statistics, Built — Part 58: Anytime-Valid Inference and Adaptive Experiments

Part 58 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the third part of Stage V, the research frontier.

It opens with the Statistical Research Group at Columbia in 1943 (Wallis 1980). A Navy officer complained that a test
of two alternative methods ran its full length long after the answer was clear, and Abraham Wald answered with the
sequential probability ratio test. On Wald's kind of example (a defective rate of 10% against 20%, α = 5%, β = 10%), the
exact SPRT needs 56.9 shells on average when the rate is 10% and 59.3 when it is 20%. The smallest nonrandomized one-sided count test meeting those targets needs 109.
The unplanned way to look early, checking a 5% z-test after every observation, rejects a true null 38% of the time
within 100 looks and 62% within 5,000. The part asks how to test and estimate when you look whenever you like, and when
you choose what to collect as you go:
- the SPRT, computed exactly on the lattice: thresholds, paths, Wald's error bounds and identity, the OC and ASN curves
  against Wald's approximations, the long tail of N, Wald–Wolfowitz optimality, overshoot;
- group-sequential theory in the Brownian picture: Pocock and O'Brien–Fleming, Lan–DeMets spending, the bias of the mean
  at stopping, stagewise ordering;
- test martingales and Ville's inequality, proved by optional stopping; peeking against Ville; null and alternative
  wealth paths; tests of power one; anytime-valid p-values;
- testing by betting (Shafer 2021): e-values, calibrators (Vovk & Wang 2021), merging, Kelly growth;
- composite nulls: universal inference (Wasserman, Ramdas & Balakrishnan 2020) against the t-test; GROW e-values and the
  reverse information projection (Grünwald, de Heide & Koolen 2024); invariance (Pérez-Ortiz et al. 2024);
- confidence sequences: Robbins's normal mixture, the LIL limit and stitching (Howard et al. 2021), betting confidence
  sequences (Waudby-Smith & Ramdas 2024), on the World's A/B platform;
- CAST (Echt et al. 1991) as a working death-label betting illustration, with simulated orders;
- game-theoretic probability (Shafer & Vovk): the protocol, upper probability, the law of large numbers by betting,
  testing a forecaster;
- e-BH (Wang & Ramdas 2022), its proof, against BH, and closed e-BH (Xu et al., arXiv:2509.02517v3, 2026);
- change detection: CUSUM (Page 1954), Lorden's criterion, ARLs, the Nile, Bayesian online changepoint detection
  (Adams & MacKay 2007);
- bandits: Thompson sampling (1933), Lai–Robbins, exploration sampling for policy choice (Kasy & Sautmann 2021);
- inference after adaptivity: negative bias (Nie et al. 2018), batched bandits (Zhang, Janson & Murphy 2020), adaptively
  weighted AIPW (Hadad et al. 2021);
- off-policy evaluation by IPW and doubly robust estimators;
- five open problems.

It keeps two promises:
- **Part 10** computed a p-value once, at a planned n. Chapters 3–7 give e-values and test martingales, valid at every
  look.
- **Part 35** gave group-sequential boundaries for planned looks. Chapter 2 gives them the Brownian picture, and chapter
  6 lets you look at any time.

**Built in this part:**
- **`statkit.sequential`** ([`explainer/stats/kit/sequential.py`](../../../explainer/stats/kit/sequential.py)), tested
  in `tests/test_stats_kit_sequential.py`:
  - the Bernoulli SPRT, exact on the lattice (OC, ASN, the stopping-time law) and by Wald's approximations, the fixed-n
    binomial comparison, single paths;
  - the bias of the mean after a group-sequential stop;
  - likelihood-ratio test martingales, Ville's check, the peeking curve;
  - calibrators, e-to-p, merging, e-BH, and the split-LRT e-value for a normal mean with unknown variance;
  - normal-mixture, stitched (LIL) and Hoeffding (fixed and union-bound) sequences, and the hedged betting confidence
    sequence for bounded data, with a time-uniform coverage harness;
  - CUSUM with average run lengths, and Bayesian online changepoint detection for a normal mean;
  - Thompson sampling with recorded propensities, AIPW scores, adaptively weighted estimates and intervals, and IPW and
    doubly robust policy values.
- **The confidence funnel** (`ConfidenceFunnel` in `explainer/stats/viz.py`), the part's instrument: a stream's running
  estimate on a log-time axis, with bands for any method (a fixed-n interval, a confidence sequence), the truth, and dots
  at the times a band excluded it.

**Data.**
- From the Museum: CAST's deaths (Echt et al. 1991) and the Nile's annual flow (Cobb 1978).
- From the World: the A/B platform's conversion streams (seeded).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| fixed-n CLT interval, checked every visit | conversion 12%, visitors 20 to 2,000 | 95% | 46.3% | broken |
| betting confidence sequence | conversion 12%, visitors 20 to 2,000 | 95% | 97.0% | kept |
| naive interval after Thompson sampling | two equal arms, 1,000 visitors | 95% | 90.0% | broken |
| adaptively weighted AIPW interval | two equal arms, 1,000 visitors | 95% | 93.7% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats58.compute   # once (about three minutes)
python tools/build.py stats58 -q l                         # fast 480p preview
python tools/build.py stats58                              # 1080p30 -> renders/stats58.mp4
python tools/qa_scene.py stats58 ConfidenceSequences
python tools/lecture_length.py stats58 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The Statistical Research Group | p₀ = 0.1, p₁ = 0.2, α = 5%, β = 10%: fixed test n = 109 (reject at ≥ 17); SPRT E N = 56.9 and 59.3, errors 3.9% and 9.7%; peeking: 38% by 100 looks, 62% by 5,000 |
| 1 | The SPRT | steps +0.693 per defective, −0.118 per good; band (−2.25, 2.89); 12 lots each: mean 43 and 60 shells; ASN peaks at 88.6 near p = 0.15 (Wald 79.4); P(N > 109) = 9.3% and 11.7% |
| 2 | Group-sequential | K = 5: Pocock 2.413; O'Brien–Fleming 4.56, 3.23, 2.63, 2.28, 2.04; maximum observed overall bias on five effects ≈ 0.023 SD, but about 0.14 given a positive early stop at θ = 0.1 (16% stop early) |
| 3 | Ville | 20,000 null streams: Ville's test (M ≥ 20, 1,000 looks) 4.1%; peeking 53% by 1,000 looks |
| 4 | Betting | p = 0.05 → e = 2.24 (κ = ½), p = 0.001 → 15.8; five studies: P(E ≥ 20) 26% (one), 46% (average), 82% (product) |
| 5 | Composite nulls | n = 40, σ unknown: t-test 4.7% under H₀, universal inference 0.1%; at μ = 0.5, 87% vs 18% |
| 6 | Confidence sequences | 300 streams, t ∈ [20, 2,000]: CLT 46.3% uniform (94% at the end), mixture 100%, betting 97.0%; widths at 5,000: CLT ±0.91, betting ±1.85, mixture ±2.38, stitched ±2.96, union Hoeffding ±4.61 points |
| 7 | CAST | 63 of 89 deaths on the drugs: mixture wealth 333 (anytime p ≤ 0.003; fixed z = 3.92, p ≈ 9 × 10⁻⁵); over random orders wealth reaches 20 after a median of 45 deaths (10%–90%: 16–71) |
| 8 | Game-theoretic probability | a forecaster saying 30% when it rains 40%: growth 0.0225 a day at λ = ½, log-drift crossing approximation about 204 days under IID .4 rain; random waiting time |
| 9 | e-BH | 50 metrics, 10 effects of 3 SD, equicorrelation 0.6, q = 0.1: BH FDR 6.7%, power 77%; e-BH 1.0%, 47% |
| 10 | Change detection | ARL₀ / delay for a 1-SD shift: h = 2: 36 / 4.5; 3: 117 / 6.6; 4: 345 / 8.2; 5: 871 / 10.3; the Nile: mean 1,098 → 850, CUSUM alarm 1901, posterior-favoured change 1899 under the chosen BOCPD model |
| 11 | Bandits | 10% vs 12%, 4,000 visitors, 60 runs: balanced loses 40 conversions, Thompson 16 (88% to the better design by the end); Lai–Robbins constant 10, so 10 log T ≈ 83 at T = 4,000 |
| 12 | Adaptivity | finite-MC matching with true 1% floor, two equal arms, 1000 runs: arm A allocation 10%–90% 115–863; naive bias -1.71 points, coverage 90.0%; weighted bias -0.98, coverage 93.7% |
| 13 | Off-policy | fixed always-A target .10, 200 runs: IPW 0.0991 (SD 0.0156, coverage 92.5%); DR 0.0990 (SD 0.0149, coverage 92.0%); asymptotic normal intervals |
| 14 | Open problems | — |
| 15 | Outro | — |

## Sources

- **History.** W. A. Wallis, *JASA* 75 (1980); A. Wald, *Ann. Math. Stat.* 16 (1945) and *Sequential Analysis*
  (1947); A. Wald & J. Wolfowitz, *Ann. Math. Stat.* 19 (1948); D. Siegmund, *Sequential Analysis* (1985).
- **Group sequential.** P. Armitage, C. McPherson & B. Rowe, *JRSS A* 132 (1969); S. Pocock, *Biometrika* 64 (1977);
  P. O'Brien & T. Fleming, *Biometrics* 35 (1979); K. K. G. Lan & D. DeMets, *Biometrika* 70 (1983); C. Jennison &
  B. Turnbull, *Group Sequential Methods with Applications to Clinical Trials* (2000).
- **Martingales and e-values.** J. Ville, *Étude critique de la notion de collectif* (1939); G. Shafer, *JRSS A* 184
  (2021); V. Vovk & R. Wang, *Ann. Stat.* 49 (2021); J. Kelly, *Bell System Technical Journal* 35 (1956); G. Shafer &
  V. Vovk, *Probability and Finance* (2001) and *Game-Theoretic Foundations for Probability and Finance* (2019);
  A. Ramdas & R. Wang, *Hypothesis Testing with E-values* (2024).
- **Composite nulls.** L. Wasserman, A. Ramdas & S. Balakrishnan, *PNAS* 117 (2020); P. Grünwald, R. de Heide &
  W. Koolen, *JRSS B* 86 (2024); M. F. Pérez-Ortiz, T. Lardy, R. de Heide & P. Grünwald, *Ann. Stat.* (2024).
- **Confidence sequences.** D. Darling & H. Robbins, *PNAS* 58 (1967); H. Robbins, *Ann. Math. Stat.* 41 (1970);
  S. Howard, A. Ramdas, J. McAuliffe & J. Sekhon, *Ann. Stat.* 49 (2021); I. Waudby-Smith & A. Ramdas, *JRSS B* 86
  (2024); R. Johari, P. Koomen, L. Pekelis & D. Walsh, *Operations Research* 70 (2022).
- **Multiple testing.** R. Wang & A. Ramdas, *JRSS B* 84 (2022); Z. Xu, A. Solari, L. Fischer, R. de Heide, A. Ramdas & J. Goeman, arXiv:2509.02517v3 (2026); Z. Ren & R. Foygel Barber, *JRSS B* 86 (2024).
- **Change detection.** E. Page, *Biometrika* 41 (1954); G. Lorden, *Ann. Math. Stat.* 42 (1971); G. Moustakides,
  *Ann. Stat.* 14 (1986); R. Adams & D. MacKay, arXiv:0710.3742 (2007).
- **Bandits and adaptivity.** W. Thompson, *Biometrika* 25 (1933); T. L. Lai & H. Robbins, *Adv. Appl. Math.* 6
  (1985); E. Kaufmann, N. Korda & R. Munos, ALT (2012); M. Kasy & A. Sautmann, *Econometrica* 89 (2021); X. Nie,
  X. Tian, J. Taylor & J. Zou, AISTATS (2018); K. Zhang, L. Janson & S. Murphy, NeurIPS (2020); V. Hadad,
  D. Hirshberg, R. Zhan, S. Wager & S. Athey, *PNAS* 118 (2021); M. Dudík, J. Langford & L. Li, ICML (2011);
  T. Lattimore & C. Szepesvári, *Bandit Algorithms* (2020).
- **Data.** D. Echt et al., *NEJM* 324 (1991); G. Cobb, *Biometrika* 65 (1978); J. Durbin & S. J. Koopman, *Time Series
  Analysis by State Space Methods* (2012).

## Problems and solutions

1. **Wald's bound.** On {reject}, Λ_N ≥ A. Then P₁(reject) = E₀[Λ_N; reject] ≥ A P₀(reject), so P₀(reject) ≤
   P₁(reject)/A ≤ 1/A = α/(1 − β).
2. **Wald's identity.** For IID integrable increments and finite EN, S_N = Σ_i Z_i 1{N ≥ i}, and {N ≥ i} is determined by Z_1, …, Z_{i−1}, so it is independent of
   Z_i. Hence E S_N = Σ_i E Z_i P(N ≥ i) = E Z₁ Σ_i P(N ≥ i) = E Z₁ E N, the exchange justified by Σ E|Z_i| 1{N ≥ i} =
   E|Z₁| E N < ∞.
3. **Ville.** Let τ = inf{t: M_t ≥ 1/α} ∧ T. By optional stopping at the bounded time τ, 1 = E M_τ ≥ (1/α) P(max_{t≤T}
   M_t ≥ 1/α). Let T → ∞ (monotone convergence).
4. **Calibrators and merging.** For 0<κ<1, f_κ is decreasing, and ∫₀¹ κp^{κ−1} dp = 1, so E f_κ(P) ≤ 1 whenever P is
   super-uniform (integrate f_κ against the distribution of P, using that f_κ is decreasing). For e-values E_1, …, E_K,
   E[(1/K) Σ E_k] = (1/K) Σ E E_k ≤ 1, with no assumption on dependence.
5. **Robbins's mixture.** ∫ exp(λS − λ²t/2) φ_τ(λ) dλ = (1 + tτ²)^{−1/2} exp(τ²S²/(2(1 + tτ²))). Setting it < 1/α and
   solving gives S² < ((1 + tτ²)/τ²)(log(1 + tτ²) + 2 log(1/α)); divide by t² for the mean. Ville makes it hold at all
   t at once.
6. **e-BH.** If H_i is rejected, e_i ≥ m/(αR), so 1{i rejected}/(R ∨ 1) ≤ α e_i/m. Summing over nulls and taking
   expectations, FDR ≤ (α/m) Σ_{i null} E e_i ≤ α m₀/m.

## Glossary

- **Sequential tests.** SPRT; likelihood-ratio walk; Wald's thresholds; operating characteristic; average sample
  number; Wald's identity; overshoot; truncation; Wald–Wolfowitz optimality.
- **Group sequential.** Information fraction; Brownian picture; Pocock and O'Brien–Fleming boundaries; spending
  function; stagewise ordering; median-unbiased estimate.
- **Anytime-valid.** Test martingale; Ville's inequality; optional stopping; e-value; e-process; calibrator; Kelly
  criterion; growth rate; universal inference; split LRT; GROW; reverse information projection; confidence sequence;
  stitching; betting confidence sequence; anytime-valid p-value; power-one test; Forecaster, Skeptic and Reality; upper
  probability; e-BH.
- **Change.** CUSUM; average run length; Lorden's criterion; run length; hazard; BOCPD; e-detector.
- **Adaptive experiments.** Thompson sampling; regret; Lai–Robbins bound; exploration sampling; propensity floor;
  AIPW score; adaptive weighting; batched bandits; off-policy evaluation; IPW; doubly robust estimator.

## Where it comes back

- **Part 59**: classical statistics when p and n grow together.
- **Part 60**: robustness when the future shifts.
- **Part 62**: adaptive and sequential causal designs, and dynamic treatment regimes.
- **Part 63**: privacy budgets spent over time.
- **Part 64**: evaluating AI systems as they are deployed.
- **Part 65**: the dissertation's monitoring plan.

## QA reconciliation

Detailed [scientific source review](../../../docs/qa/evidence/stats58-polish-20261107/source-review.md), including corrected methods, Monte Carlo errors and remaining production gates:

All sixteen English scenes and the shared sequential helpers were reviewed. Twenty-three checks pass (18 local parameterized cases, five legacy tests). All sixteen inputs were regenerated. The scientific-source and recorded sampled visual checkpoints are complete; continuous playback/listening, Chinese production and final narrated masters remain open.

The old betting CS used the first/last surviving point of a .001--.999 grid, which could exclude off-grid means or endpoints. It now uses cells covering [0,1]. K+(m) decreases and K-(m) increases in m; on [a,b], (K+(b)+K-(a))/2 is a LOWER capital bound. Only cells whose bound has crossed 1/alpha are excluded. The hull of surviving cells is consequently a conservative continuum confidence set. Log capital avoids exponential clipping. Independent direct wealth calculations on 801 off-grid candidates verify containment; endpoint constant streams and off-grid truths are tested. The grid spacing is at most .001, potentially widening the interval. Empty sets remain explicit. The common conditional mean and nonnegative predictable stakes are essential beyond boundedness. This plug-in rule is not claimed LIL optimal.

SPRT propagation records unfinished mass and EN bounds. If mass r remains at time n, stopped EN plus nr is a lower bound. From any continuing state, k consecutive successes or l failures force exit; geometric blocks bound the remaining mean by min(k/p^k,l/(1-p)^l). Multiply by r to bound the EN remainder. Across the displayed rates its interval is under 2e-7 wide. Probability arithmetic is evaluated in floating point, not a literal exact-real computation. Enumeration of all nine-step paths and independent 1000-path simulations at seven rates validate the results, including p=0,1. The old n_max*r term used the wrong time after early numerical truncation and supplied no infinite-tail certificate. Wald's approximate thresholds guarantee relaxed bounds alpha/(1-beta), beta/(1-alpha); actual errors meet nominal targets in this example, not universally. Optimality compares actual errors at two simple IID hypotheses with finite EN. Fixed n=109 is minimal for the nonrandomized one-sided count test. Truncated terminal rules require recalibration.

Smooth Gauss-Legendre continuation quadrature replaces moving-boundary grid rounding. Doubling 160 to 320 nodes preserves total null crossing .05 within 2e-10. Pocock's five-look value is 2.41317622. Exactness concerns known-variance Gaussian scores and deterministic/noninformative timing; data-chosen z-dependent looks need joint calibration. Gold stopping bias now conditions specifically on positive early crossings, with both signs retained in numerical summaries. The maximum on five simulated effect values is not a uniform bound. Median-unbiased estimates solve a stagewise p=.5 equation rather than taking a CI midpoint.

Peeking simulations batch rows to avoid multi-gigabyte arrays; a full-array seeded check verifies identical results. Probability summaries retain Monte Carlo errors. Ville uses expected stopped wealth <=1 for nonnegative supermartingales, equality only for martingales at bounded stops. Stopping information must belong to the valid filtration. Power-one tests use threshold 1/alpha and positive finite IID alternative log drift. A forty-path empirical false-alarm share is not deterministically bounded by .05. Reciprocal e-values are clipped at one; the running reciprocal includes starting wealth. A fixed-time family of e-values is not automatically an e-process.

There is no universal strict fixed-time power penalty for e-values or anytime-valid testing: E=1{a level-alpha fixed test rejects}/alpha is an e-value with the identical rejection region; a sequential test can wait for that sample size. The chosen half-power calibrator maps p=.05 to 2.24, not an intrinsic posterior-odds conversion. 1/P has infinite mean for uniform P, not every valid P. Products need independence or conditional fairness; marginal validity and predictability alone do not suffice. Gaussian log growth b mu-b^2/2 loses (b-mu)^2/2, symmetrically for equal over/under errors.

Universal inference requires independent evaluation data, normalized candidate densities, a correct likelihood model, and the true null likelihood supremum or a certified upper bound. The normal null variance MLE no longer has epsilon added: changing the parameter can lower the supposedly maximizing denominator and invalidate the proof. A degenerate all-zero evaluation sample gives e=0. Independent likelihood optimization checks the result. A likelihood ratio has mean at most one, with equality under candidate absolute continuity. Averaging finitely many splits reduces but need not remove random split dependence. Fixed-sample UI is not automatically sequential under reuse.

Growth optimality is for fixed Q; composite alternatives require their own worst-case optimization. Reverse information projection needs domination, attainment/closed-convex-family and integrability conditions. The projection can be a mixture outside the original null family. In the invariance paper, Proposition 6 restricts stopping to the maximal-invariant filtration. Appendix C.1 explicitly shows raw-data stopping can destroy stopped e-value validity. The source and display now state that restriction.

LIL width limits are scoped to ordinary sample-mean-centered intervals in nondegenerate models, not every imaginable CS at each parameter. The factor-of-two comparison is sample-size/path-specific: the LIL factor relative to fixed-n width can grow slowly without bound. For Bernoulli observations the normal mixture uses Hoeffding's .5 sub-Gaussian scale and is a supermartingale, not an exact Gaussian martingale. The Wald interval is only approximately nominal even at fixed n. Betting simultaneous coverage is .970 (empirical MCSE .00985); observed 100% over 300 streams is not population certainty. Board rows now use empirical Monte Carlo errors.

CAST counts match the primary abstract, including treatment totals and all cause-specific deaths. Nearly equal arms do not justify IID fair death labels with changing risk sets/exposure. Terminal wealth about 333 is explicitly a working-model illustration. Two thousand simulated permutations conditional on totals produce crossing summaries; thirty are plotted. They do not date the real warning or establish the actual trial could have stopped after half the deaths. Order is unavailable in this extract, rather than asserted absent from all publications. Reciprocal terminal wealth only bounds the running anytime p under that working model. The count z test is not the trial's original clinical analysis.

The strong-law outline mixes fixed small positive and negative rational stakes, then uses savings. The displayed bound log K^lambda >= lambda t(ybar-.5)-lambda^2 t/4 holds for |lambda|<=1. Recurring nonzero excess makes some account unbounded along a subsequence, and savings locks in gains. Betting on the previously winning side was not a proof. Upper probability equals ordinary probability for complete finite-horizon binary protocols; wider settings need assumptions. Forecaster testing uses full conditional probabilities, not empirical calibration. The rain example's log-drift crossing approximation is about 204 days; it is not a guaranteed hitting time. Bounded overshoot gives expected length approximately 204--218 days under the stated IID .4 alternative.

E-BH allows arbitrary dependence of VALID null e-values for a specified family, with the zero-discovery convention. It does not justify selecting only positive completed experiments, redefining m, substituting running maxima, or arbitrary global repeated stopping. Stops influenced by other streams need appropriate joint-filtration validity. One-sided Gaussian p-values in the comparison satisfy PRDS. The closure citation is now the six-author merged arXiv:2509.02517v3 (July 2026), with its specific e-BH/BY improvements; no unsupported claim that the old preprint remains under review.

CUSUM resets on negative cumulative log increments, not an ordinary SPRT's negative lower boundary. Mean time to false alarm is not an ever-false-alarm probability. Simulated alternative delay starts with a change at time one and zero initial capital, rather than all worst-case histories. Requested caps are respected; censoring, restricted means, run lengths and Monte Carlo errors are saved. No observed censoring does not prove the tail is absent. Lorden/Moustakides optimality assumes calibrated known IID laws and its specified criterion. E-detectors aggregate staggered processes for run-length guarantees. An unadjusted maximum over infinitely many start-time martingales is not Ville-valid.

All 100 Nile years/flows exactly match R's independent export. The first 28 years estimate the baseline retrospectively; this is not an exact known-law prospective calibration. The plot establishes no climate/dam cause or permanent regime. BOCPD now retains all 101 run-length columns; truncating at 60 hid the late diagonal. Two-year-bin opacity equals posterior bin mass, bins below .03 are explicitly omitted without renormalization. Posterior-favoured change years remain model dependent. The after-observation hazard reset convention matches the recurrence.

Our finite-MC policy computes winning frequencies from auxiliary posterior draws, then actually randomizes actions with those frequencies. They are exact propensities conditional on the auxiliary draws before action, approximations to exact Thompson sampling. A true minimum is f+(1-Kf)*frequency: max(f,frequency) followed by renormalization weakened the old advertised floor. Extreme-arm tests and independent enumeration verify floor and score conditional expectations. Exact-TS theorems do not automatically cover this fixed-MC policy. Lai-Robbins concerns expected regret of uniformly efficient policies; the sharp comparison is KL-UCB. It is neither a finite-horizon bound nor a demonstrated numerical crossover. Balanced pseudo-regret is .02 per worse-arm visitor, .01 per visitor overall; the old narration was off by two. Sixty simulated final regrets average 16.12, MCSE 1.81. A constant floor incurs asymptotically linear regret.

Downward mean bias is scoped to optimistic designs and the example, not all adaptive rules. Equal-arm nonnormality is a batched-model counterexample, distinct from the one-at-a-time simulation. Predictable AIPW scores are unbiased; the self-normalized ratio need not be unbiased or a martingale. Square-root propensity weights need variance convergence, effective sample growth and moment/Lindeberg conditions for normal CIs. Regenerated naive/weighted coverage is .900/.937 over 1000 experiments (empirical MCSE .00949/.00769); weighted bias remains about -.00985. The method is not exact finite sample.

Off-policy evaluation fixes the target policy, uses positive known auxiliary-conditional probabilities and a fixed misspecified prediction model. Unbiasedness is across repetitions, not conditional on all realized logs. Same-future-response fitting needs additional justification; a model need not always reduce variance. Empirical SD uses ddof=1 and per-run estimates/coverage errors are saved. IPW/DR coverage is .925/.920 over 200 runs (MCSE about .019 each), not an exact nominal guarantee. The .05 floor genuinely caps weights at 20. Open-problem claims acknowledge existing formal asymptotic definitions, efficiency results and methods for delays; each project needs a specific remaining question.

Persistent headings identify theorem scopes. Part-local polygon/segment viewport intersections preserve crossings and missing breaks in wealth paths and confidence bands; curves outside the frame are not flattened at its boundary. The recorded English sampled visual checkpoint is complete. Chinese narration/captions, continuous listening, full narrated playback and final bilingual masters remain open.
