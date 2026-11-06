# Statistics, Built — Part 58: Anytime-Valid Inference and Adaptive Experiments

Part 58 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the third part of Stage V, the research frontier.

It opens with the Statistical Research Group at Columbia in 1943 (Wallis 1980). A Navy officer complained that a test
of two alternative methods ran its full length long after the answer was clear, and Abraham Wald answered with the
sequential probability ratio test. On Wald's kind of example (a defective rate of 10% against 20%, α = 5%, β = 10%), the
exact SPRT needs 56.9 shells on average when the rate is 10% and 59.3 when it is 20%. The best fixed-sample test needs 109.
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
- CAST (Echt et al. 1991) as a betting test on the order of its deaths;
- game-theoretic probability (Shafer & Vovk): the protocol, upper probability, the law of large numbers by betting,
  testing a forecaster;
- e-BH (Wang & Ramdas 2022), its proof, against BH, and closed e-BH (Xu, Fischer & Ramdas 2025, preprint);
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
| betting confidence sequence | conversion 12%, visitors 20 to 2,000 | 95% | 96.3% | kept |
| naive interval after Thompson sampling | two equal arms, 1,000 visitors | 95% | 90.6% | broken |
| adaptively weighted AIPW interval | two equal arms, 1,000 visitors | 95% | 93.9% | kept |

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
| 2 | Group-sequential | K = 5: Pocock 2.415; O'Brien–Fleming 4.56, 3.23, 2.63, 2.28, 2.04; bias of the mean at stopping ≤ 0.023 SD, but 0.14 given an early stop at θ = 0.1 (16% stop early) |
| 3 | Ville | 20,000 null streams: Ville's test (M ≥ 20, 1,000 looks) 4.1%; peeking 53% by 1,000 looks |
| 4 | Betting | p = 0.05 → e = 2.24 (κ = ½), p = 0.001 → 15.8; five studies: P(E ≥ 20) 26% (one), 46% (average), 82% (product) |
| 5 | Composite nulls | n = 40, σ unknown: t-test 4.7% under H₀, universal inference 0.1%; at μ = 0.5, 87% vs 18% |
| 6 | Confidence sequences | 300 streams, t ∈ [20, 2,000]: CLT 46.3% uniform (94% at the end), mixture 100%, betting 96.3%; widths at 5,000: CLT ±0.91, betting ±1.85, mixture ±2.38, stitched ±2.96, union Hoeffding ±4.61 points |
| 7 | CAST | 63 of 89 deaths on the drugs: mixture wealth 333 (anytime p ≤ 0.003; fixed z = 3.92, p ≈ 9 × 10⁻⁵); over random orders wealth reaches 20 after a median of 45 deaths (10%–90%: 16–71) |
| 8 | Game-theoretic probability | a forecaster saying 30% when it rains 40%: growth 0.0225 a day at λ = ½, discredited at 1% in about 205 days |
| 9 | e-BH | 50 metrics, 10 effects of 3 SD, equicorrelation 0.6, q = 0.1: BH FDR 6.7%, power 77%; e-BH 1.0%, 47% |
| 10 | Change detection | ARL₀ / delay for a 1-SD shift: h = 2: 36 / 4.5; 3: 117 / 6.6; 4: 345 / 8.2; 5: 871 / 10.3; the Nile: mean 1,098 → 850, CUSUM alarm 1901, last change 1899 by BOCPD |
| 11 | Bandits | 10% vs 12%, 4,000 visitors, 60 runs: balanced loses 40 conversions, Thompson 16 (88% to the better design by the end); Lai–Robbins constant 10, so 10 log T ≈ 83 at T = 4,000 |
| 12 | Adaptivity | two equal arms, 1,000 visitors, 1,000 experiments: arm A got 124–893 visitors (10%–90%); sample-mean bias −1.6 points, coverage 90.6%; weighted AIPW bias −0.9, coverage 93.9% |
| 13 | Off-policy | "always A" (true 0.10), 200 runs: IPW 0.1005 (SD 0.0163, coverage 93%), DR 0.1004 (0.0156, 95%) |
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
- **Multiple testing.** R. Wang & A. Ramdas, *JRSS B* 84 (2022); Z. Xu, L. Fischer & A. Ramdas, arXiv:2504.11759
  (2025, preprint); Z. Ren & R. Foygel Barber, *JRSS B* 86 (2024).
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
2. **Wald's identity.** S_N = Σ_i Z_i 1{N ≥ i}, and {N ≥ i} is determined by Z_1, …, Z_{i−1}, so it is independent of
   Z_i. Hence E S_N = Σ_i E Z_i P(N ≥ i) = E Z₁ Σ_i P(N ≥ i) = E Z₁ E N, the exchange justified by Σ E|Z_i| 1{N ≥ i} =
   E|Z₁| E N < ∞.
3. **Ville.** Let τ = inf{t: M_t ≥ 1/α} ∧ T. By optional stopping at the bounded time τ, 1 = E M_τ ≥ (1/α) P(max_{t≤T}
   M_t ≥ 1/α). Let T → ∞ (monotone convergence).
4. **Calibrators and merging.** f_κ is decreasing, and ∫₀¹ κp^{κ−1} dp = 1, so E f_κ(P) ≤ 1 whenever P is
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
