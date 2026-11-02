# Part 17 · Deep Pricing and Hedging: expansion plan (27.1 → ~57.5 min)

Planning document only; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 (the
November 2026 standard, "Hands-on", training standard) and §6 Parts 16–17; `READING.md` §1 (numerical-methods and ML
spines) and §4 Part 17; `videos/ai/LECTURE_GUIDE.md`; every file in `videos/quant/quant17/` (manifest, common, compute,
the 14 scenes, README) and every cached result in `.cache/quant17/`; `explainer/quant/house/deep.py` (all 1,113
lines) and `quoting.ww_band`; `explainer/quant/viz.py` (`lab_card`/`lab_run`, `TrainingReplay`, `seed_band`,
`price_surface`, `smile_points3d`); the timeline in `explainer/quant/__init__.py`; the plans `quant5.md` (format),
`quant16.md` (Part 16 owns AAD, MLMC, LSM and duality, the industry of computing; its ch9 sets LSM against this part's
network on the five-asset max-call), `quant11.md` (Part 17 owns deep hedging and learned bands; Part 11 keeps a short
replay and a forward link) and `quant14.md` (Part 14's ch17 tells the neural-surrogate lineage Bayer–Stemper → HMT →
Rosenbaum–Zhang and races calibration speeds; this part trains the surrogate and does not retell the lineage).
Probe scripts (not in the repo): `/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/q17probe/pa.py … pd.py`
(about 12 CPU-minutes in all, one thread, `nice 10`, on a machine at load 18–25).

**Cadence.** Hook + 19 chapters + outro = 21 scenes, **about 57.5 minutes** (≈ 8,000 spoken words at 139 wpm; now
3,800). Chapters run 2.4–3.1 min. Each of the ten syllabus items gets at least one full chapter; items 2 (calibration),
3 (differential ML), 4 (deep BSDE), 6 (the deep hedger), 7 (the band) and 9 (generators: chapter 16 plus the House's
cross-generator test in 19) get two.

**What this part already has, and what it lacks.** Compute is rich and real (§1): eight networks trained, every
number cached. What it lacks is the *watching*: no `TrainingReplay` anywhere (one five-snapshot trade-map sequence in
`s09_band` comes closest), one seed per network, no `lab_card`, no 3D (the syllabus asks for "the learned hedge as a
surface in (time, spot)"), no history segment, derivations quoted in three-row ladders rather than proved, no frontier
chapter, and an industry chapter of three cards. So the expansion is mostly **re-running what exists with checkpoints
and seeds** (cheap: the expensive item, `calib_data`, is reused untouched) plus five small new experiments that close
syllabus gaps: CVaR and the drift trap (item 6), Leland (item 7), a network's Greeks (item 1), GP-with-gradients
(item 3, Dixon–Halperin–Bilokon ch. 3), and hedgers tested across generators (item 9, Rule 17).

---

## 1. Current state (`python tools/lecture_length.py quant17`: 27.1 min, 14 scenes)

| # | Scene | Min | What it covers, how deep, what is computed |
|---|---|---|---|
| — | `s01_hook` Hook | 1.6 | Band network's no-trade corridor at 15 days (static plot) vs WW; price 3.02 vs 3.55 daily delta at 0.5%; J.P. Morgan firm card (70% Euro Stoxx flow, "as reported by Risk.net"); objectives; House card. **No history segment.** |
| 1 | `s02_hlp` | 1.8 | HLP redone: 3×64 SiLU on 66,150 simulated prices; price curve within 0.02% of strike; tracking RMSE 0.214 (net) vs 0.209 (BS delta) on 200 fresh options. **Training not shown; one seed; no universal-approximation statement; nothing on a network's Greeks.** |
| 2 | `s03_calib` | 2.0 | Pointwise rBergomi calibrator: 894,903 MC labels (12,000 sets), held-out 1.90 vol pts vs "label noise" 2.86 (see §6 risk 1: this comparison needs fixing), the Surface in 27 s (H = 0.074, η = 1.89, ρ = −0.40), 0.97 net / 1.08 MC; 6 ms vs 2.35 s. Static training curve; **no replay of the calibration itself, no 3D surface.** |
| 3 | `s04_roughhist` | 1.7 | 100 weekly surfaces (2024–25): H at the floor 0.02 in most weeks (10th–75th pct all 0.02; 97% below 0.15); median RMSE 1.19 vs Heston 1.22; ten MC spot checks agree. Good; the "wall" is narrated, not explained. |
| 4 | `s05_dml` | 1.8 | 7-asset Bachelier basket; n = 256: price RMSE 5.03 → 0.43, delta 31×; n-sweep table. One seed; the unbiasedness of pathwise labels asserted. |
| 5 | `s06_bsde` | 2.1 | HJE's 100-d default-risk PDE: ladder of 3 rows; u₀ = 57.37 vs 57.300 (0.12%) in 16 min; no-default 59.57 vs paper's 60.781 (undiscounted). **BSDE asserted, not derived; u₀'s convergence not shown though the curve is cached (81 points).** |
| 6 | `s07_stopping` | 2.0 | BCJ max-call: two-lobe region (d = 2), 13.886 vs binomial 13.902; d = 5: 26.107 ± 0.020 vs paper 26.156. Date-by-date curves cached, not shown. |
| 7 | `s08_hedger` | 2.2 | Objective ladder (entropic, indifference); no-cost net = BS delta within 0.06 shares, price 2.36 = 2.36; band net beats delta and WW at every cost (3.52 vs 4.86 and 3.69 at 1%). **CVaR named, never trained.** |
| 8 | `s09_band` | 2.1 | Five trade-map snapshots (0…3,000 steps) of the plain net at 0.5%; Imaki's band: 0.7× WW width at the money, flat across prices. **Closest thing to a replay in the part; no Leland; WW stated, not derived.** |
| 9 | `s10_nsde` | 1.8 | Neural SV fitted to 36 Heston calls (0.12 vol pts); down-and-out call range [0.0671, 0.0703] vs Heston 0.0685. No replay; no surfaces. |
| 10 | `s11_generator` | 2.6 | BTC 32-day windows: iid, GJR-GARCH, signature LSTM, DDPM; stylized-fact scores and signature distance; lineup. Curves cached, not replayed; diffusion's reverse process never shown. |
| 11 | `s12_production` | 2.2 | J.P. Morgan and Danske firm cards; SR 26-2 history card; a five-row validation table. |
| 12 | `s13_house` | 0.8 | Rule 17 card; trial counter 73. |
| — | `s14_outro` | 2.4 | Recap, 3 desk questions, 5 problems, payoffs, references, House. |

Cached compute (single seeds; wall-clock from the cache): `calib_data` (12,000 rBergomi sets, ~1 h on 2 processes),
`calib` 739 s, `calib_hist`, `hlp`, `dml` (8 runs, 25–148 s each), `bsde` 970 s, `stopping` 758 + 673 s, `hedge`
(no-cost, cost with 5 snapshots, band at 5 costs, band surface), `nsde`, `generator` (sig LSTM 1,372 s, DDPM 37 s).
Nothing stores model weights except `calib_net.pt`, so every replay needs a re-run with checkpoints (§3b).

---

## 2. Audit

### (a) Syllabus items → chapters

| Item | Now | Plan |
|---|---|---|
| 1 Hutchinson–Lo–Poggio | ch1, 1.8 min, result only | ch1 (replay, 3D price surface, lab) + ch2 (a network's Greeks, shape constraints) |
| 2 Neural calibration (HMT) | ch2–3 | ch3 (learning the map, label noise done right, replay) + ch4 (calibrating through it, 3D, lab) + ch5 (weekly) |
| 3 Differential ML | ch4, 1.8 | ch6 (unbiased pathwise labels proved, replay, lab) + ch7 (3D tangent planes; GP with gradients) |
| 4 Deep BSDE in 100 d | ch5, 2.1 | ch8 (BSDE derived from Itô; nonlinear Feynman–Kac; shooting picture) + ch9 (u₀ replay with seeds, linear check, lab) |
| 5 Deep optimal stopping | ch6, 2.0 | ch10 (Snell recursion, bang-bang proof, 3D exercise tunnel, date-by-date replay, lab; LSM verdict) |
| 6 Deep hedging: CVaR, costs, indifference | ch7, 2.2 | ch11 (objective proved; no-cost replay onto delta; lab) + ch12 (CVaR trained; the drift trap: Merton's term rediscovered) |
| 7 Leland and WW bands rediscovered | ch8, 2.1 | ch13 (WW and Leland derived; band emerging, replayed with seeds; Leland vs WW vs net) + ch14 (band surface in 3D; Imaki lab; WW prior) |
| 8 Neural SDE robust bounds | ch9, 1.8 | ch15 (replay of calibrate-then-push; low/high surfaces in 3D; duality link to Part 9) |
| 9 Market generators | ch10, 2.6 | ch16 (DDPM reverse process live, signature MMD derived, scoreboard, lineup) + ch19 (hedgers trained on one generator, tested on others and on BTC) |
| 10 Production: model risk, SR 26-2, deployments | ch11, 2.2 | ch17 (industry) + ch18 (frontier 2023–2026) + ch19 (the House's Rule 17, tested) |

### (b) Textbook sections → chapter

Dixon–Halperin–Bilokon (2020): the chapter list is confirmed from bookseller listings (Springer's page confirms 12
chapters in three parts); section numbers inside chapters are *(verify)* against the book.

| Book · chapter | Proposed chapter / elsewhere |
|---|---|
| DHB 1 Introduction (statistical learning, supervised vs RL, ML in finance) | ch1 card |
| DHB 2 Probabilistic modeling (Bayesian inference, model selection) | Part 6, Part 27 |
| DHB 3 Bayesian regression and Gaussian processes, incl. GP surrogates for derivative prices and Greeks (*verify* section) | **ch7**: a GP with gradient observations as the classical twin of differential ML (computed) |
| DHB 4 Feedforward networks: architecture, universal approximation, back-propagation, regularization, convexity of payoff-like functions (*verify*) | ch1 (UAT card, training replay), ch2 (activations and Greeks) |
| DHB 5 Interpretability (sensitivities, Jacobians of a network) | ch2: a network's Greeks *are* its Jacobian and Hessian |
| DHB 6 Sequence modeling (AR, ARMA, GARCH) | Part 7; ch16 uses GJR-GARCH as a baseline |
| DHB 7 Probabilistic sequence modeling (HMM, particle filters) | Part 7 |
| DHB 8 Advanced networks: RNN, LSTM, GRU, CNN, autoencoders | ch16 (the LSTM generator; Quant GANs' TCN as a card); rest → Part 27 |
| DHB 9 Introduction to RL (MDPs, Bellman, Q-learning) | Part 8 |
| DHB 10 Applications of RL: QLBS option pricing and hedging (Halperin), G-learning | **ch12** card: QLBS and RL hedging (Kolm–Ritter 2019; Cao–Chen–Hull–Poulos 2021) as the RL view of the same objective; G-learning → Part 30 |
| DHB 11 Inverse RL and imitation learning | Part 29 (README note) |
| DHB 12 Frontiers | ch18 card |
| Kelly–Xiu (FnT 2023, 13(3–4):205–363; NBER w31502): §2 the virtue of complexity *(verify section numbering)* | ch1 (over-parameterized nets fit 66,150 prices without overfitting the formula); return prediction → Part 27; factor models → Part 25; portfolios → Part 30; text → Part 28. Derivatives are not a core topic of the survey *(verify)*: README says so |
| Glasserman ch. 8 (American options, stochastic mesh, LSM, duality) | Part 16 owns; ch10 is the learned stopping rule, with Part 16's LSM number as the baseline |
| Savine (AAD) ch. 8–15 | Part 16 owns the tape; ch6 uses its output as training labels (one line + forward/backward link) |
| Glasserman ch. 7 (pathwise and likelihood-ratio Greeks) | Part 16; ch6–7 prove the pathwise label is unbiased, and ch7's pause question (a digital) points back to the LR method |
| Shreve II 6.4/6.6 (FK) and Øksendal 8 | Part 5; ch8 derives the *nonlinear* Feynman–Kac (Pardoux–Peng) on top |
| Gatheral ch. 2–3 (local/stochastic vol) | Parts 12–13; ch15 calibrates a neural SV model to Heston prices |
| Proposed new reading (deep PDE theory): Jentzen, Kuckuck, von Wurstemberger, *Mathematical Introduction to Deep Learning* (arXiv 2310.20360, 2023) *(verify)* | ch9 card (why the cost is polynomial in d); README reading guide |

### (c) Papers on the Part 17 list (READING.md) → where they appear

| Paper | Now | Plan |
|---|---|---|
| Hodges–Neuberger 1989 | ladder credit | ch11 (indifference price derived); ch13 (bands exist in their numerics) |
| Hutchinson–Lo–Poggio 1994 | ch1 | ch1 (their RBF/MLP/PPR on S&P 500 futures options 1987–91, card) |
| Whalley–Wilmott 1997 | ch8 | ch13 derivation, ch14 3D |
| SR 11-7 (2011); SR 26-2 (17 Apr 2026) | ch11 | ch17 (SR 26-2: Fed/OCC/FDIC; supersedes SR 11-7 and SR 21-8; generative and agentic AI outside its scope) |
| Hernandez 2016 (*Risk*) | **absent** | ch3 card: the first "calibrate by a network" (it learned the map from quotes to parameters; HMT learn the forward map) |
| E–Han–Jentzen 2017 | **absent** | ch8 card (the method's first paper; HJE 2018 is the PNAS showcase) |
| Han–Jentzen–E 2018 | ch5 | ch8–9 |
| Sirignano–Spiliopoulos 2018 (DGM) | **absent** | ch9 card: the residual-loss alternative, and why the BSDE form needs no second derivatives |
| Becker–Cheridito–Jentzen 2019 | ch6 | ch10, with Table 1 verified (below) |
| Buehler–Gonon–Teichmann–Wood 2019 | ch7 | ch11–12 |
| Huge–Savine 2020 | ch4 | ch6–7 |
| Ruf–Wang 2020 (review) | **absent** | ch1 card ("hundreds of papers; most test against Black–Scholes on simulated data, many leak future information": phrase to be checked against their abstract before quoting *(verify)*); README |
| Wiese–Knobloch–Korn–Kretschmer 2020 (Quant GANs) | ref card only | ch16 card (TCN generator; volatility clustering and leverage; *QF* 2020) |
| Buehler–Horvath–Lyons–Perez Arribas–Wood 2020 | ref card | ch16 (signature VAE "for small data environments", the origin of signature-based generator scores) |
| Cuchiero–Khosrawi–Teichmann 2020 | **absent** | ch15 card (GAN calibration of LSV: the generator is the leverage function) |
| Horvath–Muguruza–Tomas 2021 | ch2 | ch3–4 |
| Kidger–Foster–Li–Lyons 2021 | **absent** | ch16 card. **Fix the author list in READING.md: Kidger, Foster, Li, Oberhauser, Lyons** (arXiv 2102.03657, ICML 2021) |
| Ni–Szpruch–Wiese–Liao–Xiao 2021 | ref card | ch16. **READING.md conflates two papers**: "Conditional Sig-Wasserstein GANs" is Liao, Ni, Szpruch, Wiese, Sabate-Vidales, Xiao (arXiv 2006.05421, 2020); "Sig-Wasserstein GANs for time series generation" is Ni, Szpruch, Sabate-Vidales, Xiao, Wiese, Liao (arXiv 2111.01207, 2021). List both; venue of the second *(verify: ICAIF 2021)* |
| Chevyrev–Oberhauser 2022 (*JMLR*) | **absent** | ch16 derivation row (the expected signature characterizes the law, under a normalization) |
| Gierjatowicz et al. 2022 (*J. Comput. Finance*) | ch9 | ch15 |
| "Buehler et al. 2022–2023 follow-ups *(verify: titles)*" | — | **Resolved** (arXiv listing fetched): Buehler, Murray, Pakkanen, Wood, "Learning risk-neutral implied volatility dynamics" (2103.11948, 2021); "…Remove the drift under trading frictions with minimal equivalent near-martingale measures" (2111.07844, 2021); Buehler, Murray, Wood, "Deep Bellman hedging" (2207.00932, 2022); Murray, Wood, Buehler, Wiese, Pakkanen, "…Continuous RL… across multiple risk aversions" (2207.07467, 2022); Wiese, Bai, Wood, Buehler, "Learning to simulate equity option markets" (1911.01700, NeurIPS 2019 workshop); Wiese et al., "Multi-asset spot and option market simulation" (2112.06823, 2021). Venues of the 2021–22 ones not shown in the arXiv feed *(verify)*. Used in ch12 (drift), ch17 (Bellman hedging: "optimal hedge for arbitrary initial portfolios without the need for re-training") |

**Proposed additions to READING.md Part 17.** Classic: Cybenko (1989) *Math. Control Signals Systems*; Hornik (1991)
*Neural Networks* (universal approximation, ch1); Leland (1985) *J. Finance* (ch13; shared with Part 10);
Davis–Panas–Zariphopoulou (1993) *SIAM J. Control Optim.* (optimal band under exponential utility, ch14 *(verify)*);
Pardoux–Peng (1990) *Systems & Control Letters* (BSDEs, ch8); Rockafellar–Uryasev (2000) *J. Risk* (CVaR as a
minimum, ch12); Longstaff–Schwartz (2001) (baseline, Part 16's); Merton (1969) (the drift term, ch12); Ho–Jain–Abbeel
(2020) *NeurIPS* (DDPM, ch16); Bayer–Stemper (2018) arXiv 1810.03399 (pointwise calibration, ch3, shared with Part 14);
Liu–Oosterlee–Bohte (2019) *Risks* 7(1) (networks for prices and implied vols, ch3); Ferguson–Green (2018) "Deeply
learning derivatives" arXiv 1809.02233 ("a million times faster", ch17); Imaki, Imajo, Ito, Minami, Nakagawa (2021/2023)
"No-transaction band network", *J. Financial Data Science* (DOI 10.3905/jfds.2023.1.125; ch13–14, on screen now but
missing from READING); Hutzenthaler, Jentzen, Kruse, Nguyen (2020) "A proof that rectified deep neural networks
overcome the curse of dimensionality…", *SN PDE* *(verify)* (ch9); Halperin (2020) "QLBS" *J. Derivatives* *(verify
venue)*; Kolm–Ritter (2019) *J. Financial Data Science* *(verify)*; Cao–Chen–Hull–Poulos (2021) *J. Financial Data
Science* 3(1):10–27 (verified in the arXiv feed). Frontier (2023–2026): §4 below.

---

## 3. The chapter list (21 scenes, about 57.5 min)

Conventions as in quant5.md. **Visual**: the signature picture, built before the formula. **Live**: a simulation drawn
as it runs. **Lab**: `lab_card` (≤ 12 lines of the House's code, exact lines named) then `lab_run` with the cached
output. **Replay**: `TrainingReplay(steps, loss, frame, checkpoints)` with seeds as `seed_band`, baselines at equal
budget. **Compute**: the `compute.py` item and CPU-minutes (one core, unloaded; ×2 on a loaded machine). Numbers
marked *planning run* came from my probes and must be recomputed by `compute.py`; numbers marked *cache* are already
in `.cache/quant17/`.

### H · Hook: "A machine that hedges" (2.8 min) · `s01_hook` (deepened)
- Goal: the puzzle, the era, the map.
- Beats: (1) **keep** the band teaser, but make it **live**: one simulated path runs (ValueTracker over 30 days); the
  band's two edges ride with the price; the holding (a dot) sits still inside the band and is pushed to the nearest
  edge when it exits; a running cost counter ticks only on those pushes, while a second dot (daily delta) trades every
  day and its counter climbs faster. End on the cached prices 3.02 vs 3.55. (2) **new, "how we got here" (≈ 60 s)**:
  timeline lit at 1985 (Leland), 1989 (Hodges–Neuberger; Cybenko), 1994 (HLP), 1997 (WW), 2011 (SR 11-7, new year),
  2016 (Hernandez), 2018/2019 (deep BSDE, deep hedging, deep stopping), 2020 (DML; Quant GANs), 2021 (HMT, band
  network), 2022 (neural SDE bounds), 2026 (SR 26-2, new year; SANOS/GROMM). (3) Objectives (10 items + industry +
  frontier). (4) House card. The J.P. Morgan "70%" line moves to ch17 and is checked there.
- Pause-and-predict: "Costs double. Does the corridor double in width?" (No: about 2^{1/3} = 1.26× in WW's
  asymptotics; ch13 measures it.)
- Compute: none new (`hedge` cache); the live path uses `hedge_live` (0.2 min: one path, both policies, from the
  band policy saved by `hedge_seeds`).

### 1 · Learning a pricing formula (2.9) · item 1 · `s02_hlp` (deepened)
- Goal: HLP's question; a network as a function approximator; what it gets right and what the hedge reveals.
- Beats: HLP card (1994, *J. Finance*: RBF, MLP and projection pursuit fitted to simulated BS prices and to S&P 500
  futures options 1987–1991). **Replay**: 3 seeds training on the 66,150 prices; left panel: the learned
  C/K(S/K) at T = 0.125 against the BS curve, and below it the error curve shrinking; right: training MSE, seeds as a
  band. **3D**: the learned price surface over (S/K, T) rotating, with the BS surface as a wireframe and the error
  painted on it (red where |error| > 0.1% of K: at the shortest expiries near the money). Then the hedge test as
  before (200 fresh options), but **live**: one option's hedge ledger filling day by day for both deltas.
- Derivation:
  - $C(\lambda S, \lambda K, T) = \lambda C(S, K, T)$, because GBM scales: so $C = K\,c(S/K, T)$, two inputs, not three (HLP's trick).
  - $\sup_{x\in[a,b]^2}|c(x) - \hat c_\theta(x)| < \varepsilon$ for some width, by the universal approximation theorem
    (Cybenko 1989; Hornik 1991: continuous functions on a compact set, any non-polynomial activation).
  - $\hat\Delta = \partial_S C = \partial_x \hat c(S/K, T)$, by the chain rule; computed by autograd, not by a formula.
  - $e = \hat C_0 + \sum_k \hat\Delta_k (S_{k+1} - S_k) - (S_T - K)^+$; with daily rebalancing $\operatorname{sd}(e) \propto N^{-1/2}$ (Part 10): the net's tracking error can only match BS's, not beat it.
- Experiment: `hlp` (cache: tracking RMSE 0.214 net vs 0.209 BS); `hlp_replay` (new: 3 seeds, MSE every 5 epochs,
  the slice every 20 epochs, the (S/K, T) grid 31×21 at the end). The narration states the 3-seed spread of the
  tracking RMSE and branches on whether the net's interval contains BS's.
- Lab 1: `deep.train_mlp_regressor`, lines 397–404 (the mini-batch loop: 8 lines) → prints `n_train 66150`, final
  MSE per seed, the slice error at the money.
- Pause-and-predict: "The network never saw a delta. Will its derivative hedge as well as Black–Scholes?" (Yes within
  noise; both are limited by daily rebalancing.)
- Compute: `hlp_replay` (6 min).

### 2 · A network's Greeks (2.5) · item 1 · `s02a_greeks` (new)
- Goal: a pricing network is judged by its derivatives; activation and architecture decide them; no-arbitrage shapes.
- Beats: **Visual**: the same HLP data fitted by three networks (ReLU, SiLU, softplus); three panels drawn in turn:
  price (all three indistinguishable), delta (ReLU's a staircase), gamma (ReLU's a row of spikes, the others smooth),
  BS as white. Then the **butterfly test**: the learned call price across strikes at fixed S, its second difference
  drawn as bars; negative bars (an arbitrage: a butterfly with negative price) lit red, counted per network.
- Derivation:
  - $\hat c(x) = W_2\,\phi(W_1 x + b_1) + b_2 \Rightarrow \partial_x^2 \hat c = W_2\,\phi''(\cdot)\,(W_1)^2$, by the chain rule twice.
  - ReLU: $\phi'' = 0$ except at kinks, so $\hat\Gamma = 0$ almost everywhere: a ReLU net cannot represent gamma.
  - $\partial_K C = -e^{-rT}\mathbb Q(S_T > K) \in [-e^{-rT}, 0]$ and $\partial_K^2 C = e^{-rT} q(K) \ge 0$ (Breeden–Litzenberger, Part 12): monotone and convex in $K$.
  - Shape by construction (convex-in-input networks, Dugas et al. 2009 *(verify)*) or by penalty (Ackerer–Tagasovska–Vatter 2020, *NeurIPS* *(verify)*); Part 12 owns arbitrage-free surfaces.
- Experiment: `greeks_act` (new): ReLU/SiLU/softplus × 3 seeds on the HLP set (same epochs); outputs Δ, Γ on a grid
  at T = 0.125, RMSE against BS for each, and the share of negative butterflies on a 41-strike grid. Expected:
  equal price errors, ReLU's gamma RMSE an order larger; the narration reports the computed ratio.
- Pause-and-predict: "Which network hedges a short straddle's gamma risk worst?" (ReLU.)
- Compute: `greeks_act` (8 min).

### 3 · The neural calibrator I: learning the pricing map (2.9) · item 2 · `s03_calib` (deepened)
- Goal: HMT's two-step idea; what the network learns; how good it can be when its labels are noisy.
- Beats: the two-step diagram animated: offline (12,000 parameter sets → Monte Carlo → 894,903 labels, a progress
  bar filling with a cloud of (θ, T, k) points); online (quotes in, parameters out). Cards: Hernandez (2016, inverse
  map), Bayer–Stemper (2018, pointwise), HMT (2021, grid of 8×11; this part uses the pointwise form), Liu–Oosterlee–Bohte
  (2019). **Replay**: train/val RMSE over 40 epochs (2 seeds: cached seed 0 + `calib_ckpt` seed 1) with the left panel
  showing the three smiles of the Surface at the true calibrated parameters as the network sees them at epochs 1, 5,
  10, 20, 40 (they sharpen from flat to skewed). Then the **noise floor** done right (risk 1 in §6).
- Derivation:
  - Offline: $\hat F_\theta(\vartheta, T, k) \approx \sigma^{\text{rB}}_{\text{impl}}(\vartheta, T, k)$ by least squares on MC labels $y = F + \varepsilon$.
  - $\mathbb E(\hat F - y)^2 = \mathbb E(\hat F - F)^2 + \mathbb E\varepsilon^2$, because the held-out label's noise is independent of the network: the held-out error cannot fall below the label noise.
  - Two independent labels: $\mathbb E(y_1 - y_2)^2 = s_1^2 + s_2^2$, and with $n$ paths $s^2 \propto 1/n$: so 10k- and 20k-path labels give $1.5\,s_{10k}^2$ (the current 2.86 is this, not $s$).
  - So $\mathbb E(\hat F - F)^2 = \text{held-out}^2 - s_{10k}^2$: the network's own error, separated from its labels'.
- Experiment: `calib` (cache) + `calib_noise` (new: 300 held-out sets re-simulated with 20k paths; the three-way
  decomposition, RMSE and median absolute). Planning run on 40 sets: see §6 risk 1. The narration branches: "the
  network is closer to the truth than its labels are" only if the computed decomposition says so.
- Pause-and-predict: "Train on labels with twice the noise. Does the held-out error double?" (No: averaging over
  nearby θ smooths noise; the floor rises, the network's own error barely moves.)
- Compute: `calib_ckpt` (12 min: one more training run with 5 checkpoints), `calib_noise` (4 min).

### 4 · The neural calibrator II: calibrating through the network (2.8) · item 2 · `s03a_calibrate` (new)
- Goal: calibration as gradient descent through a network; why it is fast; where it is blind.
- Beats: **3D (VolSurface)**: the Surface's 148 quotes as dots over (k, T); the network's implied-vol surface at the
  first iterate (flat, wrong), then morphing iterate by iterate (Adam, then L-BFGS) onto the dots, the camera
  circling; a side panel shows the five parameters as sliders moving, and the loss falling. **12 starts** as a band of
  loss curves; the best start replayed. Then the fresh-MC check: the MC smile dots drawn over the network's smile
  (0.97 vs 1.08 vol points, cache). Speed race (cache: 6 ms vs 2.35 s per surface).
- Derivation:
  - $\vartheta(u) = \ell + (h - \ell)\tfrac{1 + \tanh u}{2}$, so every iterate stays inside the training box.
  - $\nabla_u L = \nabla_\vartheta L \odot (h - \ell)\tfrac{1 - \tanh^2 u}{2}$, by the chain rule: the gradient **vanishes at the walls**, which is why chapter 5's H sits at 0.02 and stays there.
  - $\nabla_\vartheta L = 2\sum_i w_i(\hat F_i - \sigma_i)\nabla_\vartheta \hat F_i$, exact by autograd: with MC each gradient would cost 5 extra simulations, with noise.
  - Cost: (starts × iterations) × 6 ms ≈ 27 s here vs the same count × 2.35 s ≈ hours by MC (computed from the cache).
- Experiment: `calib_trace` (new: `calibrate_neural` with the iterates recorded every 5 steps for all 12 starts and the
  network's surface on a 30×20 (k, T) grid at 10 checkpoints of the best start).
- Lab 2: `deep.calibrate_neural`, lines 166–170 (the model: tanh map into the box) and 177–182 (the Adam loop),
  11 lines → prints the fitted (H, η, ρ), the RMSE 0.97 and the 27 s.
- Pause-and-predict: "Today's market wants H = 0.01, below the box. What does the calibrator report?" (0.02, with no
  warning: the wall.)
- Compute: `calib_trace` (1.5 min).

### 5 · Rough volatility, week by week (2.4) · item 2 · `s04_roughhist` (kept, tightened)
- Goal: a year-scale use of the calibrator, and an extrapolation lesson.
- Beats: keep the H, η, ρ time series and the Heston comparison. **New visual**: the training box drawn as a 2D slab
  in (H, η); 100 weekly fits drop in one by one (ValueTracker over weeks) and pile up against the H = 0.02 wall; the
  ten MC spot checks light green where MC agrees. Link back to ch4's vanishing gradient.
- Derivation (two rows): rBergomi's ATM skew $\psi(T) \sim T^{H - 1/2}$ (Part 14), so a steep short-dated BTC skew
  pushes $H \to 0$; at the wall, the fit is the best *inside* the box, and the MC checks confirm it is a fit, not the
  market's H.
- Experiment: `calib_hist` (cache: share at the floor, median RMSE 1.19 vs 1.22, rBergomi ahead in 56% of weeks).
- Pause-and-predict: "Retrain with H down to 0.005. Do the weekly H's move?" (Unknown here; README problem. Not
  computed: `calib_data` would need a new hour.)
- Compute: none.

### 6 · Differential machine learning (3.0) · item 3 · `s05_dml` (deepened)
- Goal: train on payoffs and their pathwise derivatives; prove why the derivative labels are honest.
- Beats: **Visual**: 300 noisy (basket, payoff) samples (cache scatter) and the exact Bachelier price curve; then each
  sample sprouts a short arrow, its pathwise slope; the arrows line up along the price's slope far better than the
  dots do along the price. **Replay**: the 1-D slice of the fit at n = 1,024, plain vs differential side by side,
  at 6 checkpoints; loss panel with 3 seeds as bands. Then the error-vs-n log–log plot, both methods, 3 seeds as bands.
- Derivation:
  - $Y = (w\cdot X_T - K)^+$, $X_T = X + \sqrt T\,L Z$; $\partial_X Y = \mathbf 1\{w\cdot X_T > K\}\,w$, by the chain rule (pathwise).
  - $\mathbb E[\partial_X Y \mid X] = \partial_X \mathbb E[Y\mid X] = \partial_X V(X)$, by dominated convergence ($Y$ is Lipschitz in $X$, so differentiation and expectation commute).
  - Loss: $\frac{1}{1+\lambda}\big[(f(x) - y)^2 + \lambda\sum_j \omega_j(\partial_j f(x) - \partial_j y)^2\big]$, $\omega_j$ normalizing each input's scale (the "twin network": the backward pass is part of the forward model).
  - Labels per sample: $1 + d = 8$ here; AAD makes the extra $d$ cost a small constant multiple of one pricing (Part 16's theorem).
- Experiment: `dml` (cache: n = 256: price RMSE 5.03 → 0.43; delta 0.398 → 0.0127) + `dml_seeds` (new: seeds 2–3 at
  n = 256, 1,024, 4,096) + `dml_replay` (new). The narration quotes the seed spread at n = 256, where the plain net's
  5.03 looks like a failed fit: if seeds 2–3 give ~1, say the 5.03 was one bad seed, and plot all three.
- Lab 3: `deep.train_differential`, lines 473–481 (the twin loss, 9 lines) → prints price and delta RMSE, plain vs
  differential at n = 1,024.
- Pause-and-predict: "Which needs more samples to get delta right: price labels alone, or price plus slopes?"
- Compute: `dml_seeds` (10 min), `dml_replay` (1.5 min).

### 7 · Differential labels in three dimensions (2.5) · item 3 · `s05a_dml3d` (new)
- Goal: the geometry of derivative labels; the Gaussian-process twin (DHB ch. 3); where pathwise labels fail.
- Beats: **3D**: a two-asset Bachelier basket; 64 training samples as dots above the (X₁, X₂) plane, each with a small
  tangent plane (its pathwise gradient). Two fitted surfaces grow in turn: plain (wobbly between dots) and
  differential (hugging the true surface, drawn as a wireframe); camera walk; the error surface painted in colour.
  Then the classical twin: a **GP with gradient observations** fitted to the same 64 (price, gradient) pairs:
  its surface and its uncertainty band (a translucent shell) shrinking where the gradients are.
- Derivation:
  - GP prior $f \sim \mathcal{GP}(0, k)$; then $\operatorname{Cov}(f(x), \partial_j f(x')) = \partial_{x'_j}k(x, x')$ and $\operatorname{Cov}(\partial_i f(x), \partial_j f(x')) = \partial_{x_i}\partial_{x'_j}k(x, x')$, because differentiation is linear.
  - Posterior mean $\bar f(x_*) = k_*^\top (K + \sigma^2 I)^{-1}[y; \partial y]$ over the stacked $n(1+d)$ observations: the same information as differential ML, solved exactly, at $O((n(1+d))^3)$ cost.
  - So DML is the scalable version: cost linear in $n$.
- Experiment: `dml2d` (new: d = 2, n = 64, 3 seeds: plain net, differential net, GP with gradients (RBF kernel,
  numpy), errors on a 41×41 grid).
- Pause-and-predict: "Price a digital this way. What is the pathwise derivative of a digital?" (Zero almost surely:
  the labels say nothing; smooth the payoff or use likelihood-ratio labels, Part 16.)
- Compute: `dml2d` (2 min).

### 8 · The deep BSDE I: from a PDE to a learning problem (3.0) · item 4 · `s06_bsde` (deepened)
- Goal: derive the BSDE from Itô, state the nonlinear Feynman–Kac theorem, and see the method as aiming.
- Beats: keep the curse card (10¹⁰⁰ nodes). **Visual ("shooting")**: 64 paths of the hundred-asset worst-of drawn as
  thin ribbons; from today's guess u₀ (a dot on the left) each path's Y is stepped forward with that path's noise;
  at expiry each Y lands near or far from its target min_i X_T (white ticks); the misses drawn as red segments. The
  guess is nudged and the paths re-fired: misses shrink. Cards: E–Han–Jentzen (2017), HJE (2018, *PNAS*), Pardoux–Peng
  (1990).
- Derivation:
  - $Y_t = u(t, X_t) \Rightarrow dY_t = (\partial_t u + \mathcal L u)\,dt + \nabla u^\top \sigma(X_t)\,dW_t$, by Itô.
  - The PDE says $\partial_t u + \mathcal L u = (1-\delta)Q(u)u + Ru =: f(Y)$, so $dY_t = f(Y_t)\,dt + Z_t\cdot dW_t$ with $Z_t = \sigma(X_t)^\top\nabla u$.
  - $Y_T = g(X_T) = \min_i X^i_T$: a *backward* SDE, terminal condition known, start unknown.
  - Pardoux–Peng (1990): for Lipschitz $f$ the pair $(Y, Z)$ is unique, and $Y_0 = u(0, x_0)$: nonlinear Feynman–Kac.
  - Euler: $Y_{n+1} = Y_n + f(Y_n)\Delta t + Z_n\cdot\Delta W_n$, $Z_n = \text{net}_n(X_{t_n})$; minimize $\mathbb E|Y_N - g(X_N)|^2$ over $(u_0, Z_0, \theta)$: zero loss ⇔ the guess was the price.
  - Linear check: no default ($\delta = 1$) gives $f = RY$, so $Y_0 = e^{-RT}\mathbb E\,g(X_T)$: plain Monte Carlo, 59.57 (cache).
- Experiment: `bsde` (cache) + `bsde_seeds` (below) for the shooting snapshots.
- Pause-and-predict: "Double the dimension to 200. Does the cost per step double, or square?" (Double: linear in d.)
- Compute: shared with ch9.

### 9 · The deep BSDE II: watching u₀ converge (2.5) · item 4 · `s06a_bsde_train` (new)
- Goal: the training replayed, with seeds and the honest error bar; why it beats the curse; the alternatives.
- Beats: **Replay**: u₀ by iteration (cache seed 0, 81 points) + seed 1 (`bsde_seeds`) as a band, the reference
  57.300 as a white line; left panel: the scatter of $Y_N$ against $g(X_N)$ for 256 paths at iterations 0, 100, 300,
  1,000, 2,000, collapsing onto the diagonal. The final number reported as the mean ± sd of the last 1,000 iterations
  (*planning run* on the cache: 57.354 ± 0.043 over the last 20 logged values, so 0.09% above 57.300, not the
  single-iterate 57.37). **Linear check run** (δ = 1) converging to the MC 59.57. Cards: DGM (Sirignano–Spiliopoulos
  2018: PDE residual at random points, needs second derivatives), Hutzenthaler–Jentzen–Kruse–Nguyen (2020; cost
  polynomial in d and 1/ε for semilinear heat equations *(verify)*), multilevel Picard (the source of 57.300).
- Derivation: cost per iteration $O(N\,d\,(d+10)\,B)$ (batch $B$, $N - 1$ subnetworks of width $d + 10$), so linear in
  steps and quadratic in d at fixed width, against $10^d$ for a grid.
- Lab 4: `deep.deep_bsde`, lines 524–534 (`run`: the forward Euler for X and Y, 11 lines) → prints u₀ at iterations
  0, 1,000, 4,000 and the reference.
- Pause-and-predict: "The loss stalls at 27, not 0. Is the network failing?" (No: the Euler error and the batch
  noise; u₀ is what matters, and it has converged.)
- Compute: `bsde_seeds` (1 seed × 2,000 iterations with scatter snapshots + the δ = 1 run × 2,000: 16 min).

### 10 · Deep optimal stopping (3.0) · item 5 · `s07_stopping` (deepened)
- Goal: learn the exercise rule date by date, prove the lower bound, and compare honestly with Longstaff–Schwartz.
- Beats: **3D exercise tunnel**: for d = 2, the stop region in (S₁, S₂) at each of the 8 dates stacked along a time
  axis: two lobes that widen toward expiry, the camera flying down the tunnel; the diagonal "continue" valley (where
  max(S₁, S₂) is uncertain) narrowing. **Replay**: the backward training, date 8 → date 1: each date's objective curve
  (cache: 10 points per date, d = 5) drawn in turn, and for d = 2 the date-4 region forming at steps 0, 50, 100, 200,
  300. **Verdict bar chart** (d = 5): network 26.107 ± 0.020 (500 steps per date, CPU, cache); LSM (Part 16's
  `maxcall`, loaded through its `load`); BCJ's own [26.156, 26.162] (3,000 + d steps per date, batch 8,192, GTX 1080,
  28 s; Table 1, verified). Narration branches: if Part 16's LSM sits above our network (the planning run of quant16
  says 26.146 ± 0.031), say so plainly: at a CPU budget, a good regression basis wins here; the network's advantage is
  that it needs no hand-made basis and scales to d = 500 (BCJ Table 1 runs to 500 assets).
- Derivation:
  - Snell envelope: $V_n = \max\big(g_n, \mathbb E[V_{n+1}\mid X_n]\big)$, $V_N = g_N$ (Part 8/16).
  - Stopping times by recursion: $\tau_n = n F_n + \tau_{n+1}(1 - F_n)$, $F_n \in \{0, 1\}$ a function of $X_n$.
  - Given $X_n$: $\mathbb E[g_n F + G_{n+1}(1-F)\mid X_n] = G^* + F\,(g_n - \mathbb E[G_{n+1}\mid X_n])$ is linear in $F$, so $F^* = \mathbf 1\{g_n \ge \mathbb E[G_{n+1}\mid X_n]\}$: bang-bang.
  - Train a sigmoid $F_\theta$ (gradients), evaluate the hard rule $\mathbf 1\{F_\theta > \tfrac12\}$ on fresh paths: $\mathbb E\,g_{\tau_\theta} \le V_0$, a lower bound; the upper bound is Part 16's dual.
- Experiment: `stopping` (cache) + `stopping_region` (new: d = 2, 300 steps per date, the region at all 8 dates on a
  61×61 grid and date 4's at 5 checkpoints) + Part 16's `maxcall` (read only). Optional `stopping_budget` (d = 5 at
  1,500 steps per date, ~35 min): **decision for the lead** (§6).
- Lab 5: `deep.deep_stopping`, lines 620–628 (one date's training loop, 9 lines) → prints the lower bounds 13.886
  (d = 2, binomial 13.902) and 26.107 (d = 5).
- Pause-and-predict: "At S₁ = S₂ = 130 near expiry, stop or wait?" (Wait: on the diagonal the max has the most
  optionality.)
- Compute: `stopping_region` (6 min).

### 11 · The deep hedger I: the objective (3.0) · item 6 · `s08_hedger` (deepened)
- Goal: deep hedging's objective derived; the indifference price; the no-cost sanity check watched.
- Beats: keep the framework ladder, now in full (below). **Replay**: no-cost training, 3 seeds: left panel the
  network's holding against S at 15 days (from a delta-hedged previous holding), converging onto the BS delta curve;
  right the entropic risk falling from 15.7 to 2.36, seeds as a band, and the BS benchmark as a line. Then a **live
  hedge**: one path, 30 rebalances, the network's and BS's holdings as two step lines that coincide.
- Derivation:
  - $\rho(X) = \frac1\gamma\log\mathbb E\,e^{-\gamma X}$: monotone, convex, and $\rho(X + c) = \rho(X) - c$ (cash invariance), by pulling $e^{-\gamma c}$ out of the expectation.
  - $p = \inf_\delta \rho\big(-Z + (\delta\cdot S)_T - C_T(\delta)\big) - \inf_\delta \rho\big((\delta\cdot S)_T - C_T(\delta)\big)$, the seller's indifference price (Hodges–Neuberger 1989); the second term is 0 when $S$ is a martingale (do nothing).
  - Small $\gamma$: $\rho(X) \approx -\mathbb E X + \frac\gamma2\operatorname{Var}X$, by expanding log and exp to second order.
  - Check (no costs, $\mu = 0$): $p \approx C_{BS} + \frac\gamma2\operatorname{Var}(e_{\text{discrete}}) = 2.287 + 0.5\times0.357^2 = 2.351$ against the trained 2.355–2.360 (cache): the price of rebalancing only daily.
- Experiment: `hedge` (cache) + `hedge_replay` (new: no-cost, 3 seeds, 800 iterations, the holding curve at 16
  checkpoints; cost 0.5%, 3 seeds, 1,500 iterations, trade map every 100).
- Lab 6: `deep.hedge_pnl`, lines 272–280 (the P&L of a short call hedged by any policy, 9 lines) → prints price,
  CVaR 50%, sd for network and delta (cache).
- Pause-and-predict: "Set γ ten times larger. Does the no-cost hedge change?" (No: with no costs the replicating
  hedge is optimal for every γ; only the price's risk premium changes.)
- Compute: `hedge_replay` (part 1: 6 min).

### 12 · The deep hedger II: risk measures, and the drift trap (2.6) · item 6 · `s08a_drift` (new)
- Goal: CVaR trained; what a hedger does under a real-world drift; the P/Q discipline in deep hedging.
- Beats: (1) **CVaR**: the loss histogram of the entropic hedger and the CVaR(50%) hedger overlaid, the worst half
  shaded; the Rockafellar–Uryasev minimization drawn as the threshold $w$ sliding to the 50% quantile.
  (2) **The drift trap**: train the same no-cost hedger on paths with μ = 30% a year. Replay: the holding curve
  lifts *above* BS delta by a near-constant amount; the Merton line $\Delta + \mu/(\gamma\sigma^2 S)$ drawn dashed
  and the network sits on it. (3) Then the twist: evaluate both hedgers on driftless paths: the drifted hedger's
  price is worse; it was partly speculating. Cards: François–Gauthier–Godin–Pérez-Mendoza (2024: the gap between
  deep and delta hedging "can act as a speculative overlay"; a suitable risk measure prevents it), Buehler–Murray–
  Pakkanen–Wood (2021: train under a minimal equivalent near-martingale measure to "remove the drift"), QLBS and RL
  hedging (DHB ch. 10; Kolm–Ritter 2019; Cao–Chen–Hull–Poulos 2021) as the RL view of the same objective.
- Derivation:
  - $\mathrm{CVaR}_\alpha(L) = \min_w\big\{w + \tfrac1\alpha\mathbb E(L - w)^+\big\}$ (Rockafellar–Uryasev 2000), minimized at $w = \mathrm{VaR}_\alpha$: so $w$ is one more trainable number.
  - Complete market, CARA utility, $r = 0$: the optimal terminal wealth splits into replication of $Z$ plus Merton's portfolio, so $\delta^*_t = \Delta_t + \frac{\mu}{\gamma\sigma^2 S_t}$, by the martingale method (the claim is hedged away; the rest is the no-claim problem, whose CARA solution invests a fixed $\mu/(\gamma\sigma^2)$ dollars).
  - At $S = 100$, $\mu = 0.3$, $\gamma = 1$, $\sigma = 0.2$: $0.3/(0.04\times100) = 0.075$ shares.
- Experiment: `risk_measures` (new: entropic vs CVaR(50%), band network at 0.5% costs, 3 seeds, full size) and `drift` (new: μ ∈ {0, 0.3},
  3 seeds; holding curve at 15 days; prices under P and under Q). **Planning run** (1 seed, 600 iterations, batch
  2,048): mean deviation from delta across S ∈ [90, 110] = **0.073 shares against Merton's 0.075**; priced on drifted
  paths 2.324 (below the driftless 2.355: it counts on the drift), on driftless paths 2.517 (worse: the overlay is
  risk). **CVaR planning run** (no costs, 1 seed, 400 iterations, batch 2,048): the CVaR-trained hedger reached
  CVaR₅₀ 2.594 (sd 0.403, still up to 0.20 shares off delta), the entropic one at the same budget CVaR₅₀ 2.748 (sd 0.583,
  up to 0.37 off), against fully trained delta's 2.557 (cache): at this budget neither has converged, so the full-size
  `risk_measures` item is needed. With no costs every risk measure should end at delta (replication is optimal), so
  `risk_measures` runs **at 0.5% costs**, where the two objectives give different bands and different tails; the
  narration reports which tail each one thins.
- Pause-and-predict: "Your deep hedger makes money on average with no costs. Is it hedging?" (Partly speculating:
  check its holdings against delta on driftless paths.) This becomes desk question 4.
- Compute: `risk_measures` (6 min), `drift` (6 min).

### 13 · Where not to trade I: the band emerges (2.9) · item 7 · `s09_band` (deepened)
- Goal: Leland and Whalley–Wilmott derived; the plain network discovering a band with nobody telling it.
- Beats: **Replay** (densified): the plain network's trade map (trade size over price × current holding) at every
  100 steps of 1,500, 3 seeds (`hedge_replay`): a diagonal stripe of "do nothing" opens and widens; the WW corridor
  drawn as two dashed lines; right panel: the risk falling, seeds as a band. Cached: at the money the do-nothing
  holdings widen from 0.50–0.52 (no costs) to 0.46–0.56 (0.5%). **Bar chart by cost** (0.1–1%): daily delta,
  Leland (delta at an inflated volatility), WW band, band network; indifference price and turnover.
- Derivation (Leland, 4 rows):
  - Over $\Delta t$ the delta moves by $\Delta\Delta \approx \Gamma\,\Delta S$, so $\mathbb E|\Delta\Delta|\,S = \Gamma S^2\sigma\sqrt{\Delta t}\sqrt{2/\pi}$ (mean of $|N(0,1)|$).
  - Cost per unit time $\frac{k}{2}\Gamma S^2\sigma\sqrt{2/\pi}/\sqrt{\Delta t}$ with round-trip cost $k = 2c$; add it to the BS PDE's $\frac12\sigma^2S^2\Gamma$ term.
  - So $\hat\sigma^2 = \sigma^2\big(1 + \sqrt{2/\pi}\,\tfrac{k}{\sigma\sqrt{\Delta t}}\big)$ for a short call (Leland 1985).
  - Here $\sigma\sqrt{\Delta t} = 0.0105$; at $c = 0.5\%$ the Leland number is 0.76 and $\hat\sigma = 26.6\%$.
- Derivation (Whalley–Wilmott, 4 rows): a gap $\epsilon = \delta - \Delta$ costs $\frac\gamma2\epsilon^2\sigma^2S^2\,dt$ of certainty equivalent; keeping $|\epsilon| \le h$ needs turnover $\approx \sigma^2S^2\Gamma^2/h$ per unit time (reflected diffusion of $\epsilon$ with variance rate $\sigma^2S^2\Gamma^2$), costing $cS$ per share; uniform $\epsilon$ on $[-h, h]$ has $\mathbb E\epsilon^2 = h^2/3$; minimize $\frac{\gamma}{6}h^2\sigma^2S^2 + c\,S\,\sigma^2S^2\Gamma^2/h$ ⇒ $h = \big(\tfrac{3cS\Gamma^2}{2\gamma}\big)^{1/3}$ (the House's `quoting.ww_band`, the same formula). Hence the cube root: doubling $c$ widens the band by $2^{1/3}$.
- Experiment: `leland` (new). **Planning run** (100,000 paths, same seed as the cache): indifference price at
  0.1 / 0.25 / 0.5 / 1%: daily delta 2.59 / 2.94 / 3.55 / 4.86; Leland 2.58 / 2.89 / 3.37 / 4.26; WW 2.56 / 2.77 /
  3.08 / 3.69; band network (cache) 2.53 / 2.73 / 3.02 / 3.52. Leland lowers turnover only a little (cost 1.00 vs 1.11
  at 0.5%), WW halves it (0.47). The narration's ordering is computed, not typed.
- Pause-and-predict: "Leland's price at 0.5% is BS at 26.6% vol, 3.04. Why is the hedger's indifference price higher
  (3.37)?" (Leland covers the expected cost; the entropic price also charges for the variance.)
- Compute: `hedge_replay` (part 2: 12 min), `leland` (1 min).

### 14 · Where not to trade II: the band as a surface (2.9) · item 7 · `s09a_band3d` (new)
- Goal: the syllabus visual: the learned hedge as a surface in (time, spot); the band network's architecture; what
  theory guarantees.
- Beats: **3D**: over (days to expiry, price): the BS delta surface (white wireframe), the learned band's lower and
  upper surfaces (translucent sheets, cache `band.surface`: 20 × 61), and WW's (dashed mesh). The camera walks along
  the strike: WW's band bulges at the strike near expiry (gamma), the learned band is nearly flat across prices and
  widens toward expiry (cache: width at the money 0.22 → 0.28 shares from 30 to ~5 days, against WW's 0.31 → 0.58).
  One simulated path then runs *on* the surface, its holding a bead that stays between the sheets. **Seeds**: band
  network's price at three costs, 3 seeds as error bars (planning run at reduced size: 3.031 at all three seeds; the
  band network is very stable). **WW prior** (Arzel–Lehdili 2026): a band network initialized at WW's band vs the
  default narrow start, 2 seeds each: the replayed loss curves, WW-start ahead early.
- Derivation:
  - Band network (Imaki et al. 2021): $[\ell, u] = [\Delta - \mathrm{softplus}(a_\theta), \Delta + \mathrm{softplus}(b_\theta)]$, $\delta_k = \min(\max(\delta_{k-1}, \ell), u)$: the hedge moves only to the nearest edge.
  - Theorem (Davis–Panas–Zariphopoulou 1993 *(verify)*; Imaki et al. prove optimality of a band for a wider class): under exponential utility and proportional costs the optimal strategy is a no-trade region, so the architecture loses nothing.
  - Why the learned band is narrower than WW's: WW is the $c \to 0$, continuous-trading limit; at daily rebalancing the hedge already drifts between dates, so less band is needed.
- Experiment: `hedge` (cache surface), `hedge_seeds` (new: band network, costs {0.1, 0.5, 1}%, seeds 3 and 4, full
  size, policies saved as `.pt`), `band_prior` (new).
- Lab 7: `Hedger.band`, lines 252–256 (delta from erf, the two softplus offsets: 5 lines) plus `quoting.ww_band`
  lines 99–101 (3 lines) → prints at the money, 15 days: learned [lo, hi] and WW's [0.31, 0.70] (cache `ww_slices`).
- Pause-and-predict: "Near expiry, far out of the money: where is the band?" (Both edges pinned at 0: delta is 0 and
  the band hardly binds.)
- Compute: `hedge_seeds` (18 min), `band_prior` (8 min).

### 15 · Neural SDEs and robust bounds (3.0) · item 8 · `s10_nsde` (deepened)
- Goal: a model rich enough to measure model risk; calibrate, then push; the range and what it is not.
- Beats: keep the model ladder. **Replay** in two acts: (1) calibration: the 36 model implied vols (4 expiries × 9
  strikes) rising onto the Heston targets as the loss falls; (2) the push: two copies start from the calibrated model,
  the down-and-out price drifting down for one and up for the other, while a vanilla-error gauge must stay under its
  ceiling (states that break it are drawn grey and rejected). **3D**: the low and high models' implied-vol surfaces
  over (K, T) superimposed on Heston's: visually identical (within 0.19 vol points, cache), yet the barrier option's
  price differs (0.0671 vs 0.0703; Heston 0.0685, inside). One sample path from each model at the barrier: the high
  model's volatility is lower near 0.8.
- Derivation:
  - Calibrate: $\min_\theta \sum_{ij}(P^\theta_{ij} - P^{\text{mkt}}_{ij})^2$ with $P^\theta_{ij} = \mathbb E^\theta(S_{T_i} - K_j)^+$, differentiated through the Euler scheme.
  - Push: $\min_\theta\ \pm\,\mathbb E^\theta[\Phi] + \lambda\sum_{ij}(P^\theta_{ij} - P^{\text{mkt}}_{ij})^2$ (a penalty for the constraint "every vanilla repriced").
  - The range found is a **lower estimate** of the true model range (a local search inside one model class), which sits inside the model-free MOT bounds of Part 9 for the same constraints.
  - Martingale correction $S \leftarrow S/\bar S$ (control variate): $\mathbb E S_T = 1$ exactly on each batch.
- Experiment: `nsde` (cache) + `nsde_trace` (new: same run with traces: calibration loss and 36 IVs every 20
  iterations; push trajectories of (vanilla error, barrier price) every 10; seed 1 added for the range's spread).
  Narration branches on whether seed 1's range overlaps seed 0's.
- Cards: Cuchiero–Khosrawi–Teichmann (2020) LSV by GAN; Guyon–Mustapha (2022/2024) neural joint SPX/VIX calibration:
  a one-factor neural SLV "fits both smiles and VIX futures within bid-ask spreads" (SSRN 4309576; *Risk*).
- Pause-and-predict: "Add the 0.8-strike one-touch to the calibration set. What happens to the range?" (It shrinks:
  the barrier's information is in the touch.)
- Compute: `nsde_trace` (2 seeds: 20 min).

### 16 · Market generators (3.1) · item 9 · `s11_generator` (deepened)
- Goal: four ways to invent markets; how to judge them; a diffusion model watched as it generates.
- Beats: (1) **Live**: the DDPM's reverse process: 24 windows of pure noise de-noised step by step (t = 200 → 0),
  turning into return paths; side by side, the forward process adding noise to a real BTC window. (2) Generator
  cards: GJR-GARCH (the econometric baseline), Quant GANs (TCN), signature LSTM (vol × noise, trained by expected
  signatures), DDPM. (3) **Replay**: the sig-LSTM's signature loss (cache curve, 150 points) with its windows' kurtosis
  and |r| autocorrelation as live readouts (from `gen_snaps`); the DDPM's loss with 3 seeds. (4) The **scoreboard**
  (cache): kurtosis, |r| ACF, leverage, signature distance to train and to held-out. (5) **Lineup** (cache): four
  windows, one real; pause.
- Derivation:
  - Forward: $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon$, $\bar\alpha_t = \prod_{s\le t}(1-\beta_s)$, by composing Gaussian steps.
  - Loss $\mathbb E\|\varepsilon - \varepsilon_\theta(x_t, t)\|^2$; reverse mean $\frac{1}{\sqrt{\alpha_t}}\big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\varepsilon_\theta\big)$ (Ho–Jain–Abbeel 2020; AI Part 21 builds it).
  - Signature $S(X)_{[0,T]} = (1, \int dX, \iint dX\otimes dX, \dots)$; the expected signature determines the law under a normalization (Chevyrev–Oberhauser 2022), so $\|\mathbb E S(X) - \mathbb E S(Y)\|$ is a distance between generators (a linear-kernel MMD; Part 5 builds signatures).
  - Lead–lag: the level-2 area of (lead, lag) is the quadratic variation, so volatility clustering shows up in the signature.
- Experiment: `generator` (cache: e.g. held-out kurtosis 2.4 vs training 14.7; diffusion nearest the held-out years by
  signature distance, 0.93, because its tails are thin, 1.43), `ddpm_reverse` (new), `gen_snaps` (new, optional: the
  sig-LSTM re-run with snapshots, 23 min; **decision for the lead**, otherwise the replay uses the cached loss alone).
- Lab 8: `deep.sig_mmd`, lines 775–780, with `deep.signature`'s Chen step (lines 740–747) → prints the signature
  distances of each generator to the held-out windows (cache).
- Pause-and-predict: the lineup: "Which of the four is real?"
- Compute: `ddpm_reverse` (3 min).

### 17 · Industry: what has reached desks (2.8) · item 10 · `s12_production` (deepened)
- Goal: deployments on the public record, and the supervisors' rules.
- Beats: **firm cards**, each with what was reported and by whom: J.P. Morgan (Risk.net's 2022 Quant of the Year
  profile of Hans Buehler: deep hedging "learns hedging strategies… through hundreds of thousands of simulations";
  a data-driven "Flow Trader" hedging vanilla index option books on the S&P 500 and Euro Stoxx since 2018, as
  reported by Risk.net; the "about 70% of Euro Stoxx flow options" figure **(verify against the Risk.net article
  before it stays on screen)**; Buehler later joined XTX Markets as deputy CEO, as reported by Risk.net *(verify
  year)*; J.P. Morgan researchers co-authored "Quantum deep hedging" (*Quantum* 7, 1191, 2023; trapped-ion circuits of
  up to 16 qubits; "comparable performance" with fewer parameters). Danske Bank (Huge–Savine; AAD in production;
  existing card). Scotiabank (Ferguson–Green 2018 "Deeply learning derivatives": basket call valuations "a million
  times faster", as the authors claim; affiliation *(verify)*). **Regulators**: SR 26-2 (17 April 2026; Fed, OCC,
  FDIC; supersedes SR 11-7 and SR 21-8; effective challenge, conceptual soundness, outcomes analysis, inventory,
  materiality; generative and agentic AI outside its scope: so a deep hedger is in, an LLM assistant is not); PRA
  SS1/23 (published 17 May 2023, effective 17 May 2024, revised 23 April 2026; applies to UK banks with internal-model
  approval; covers "the use of artificial intelligence in modelling techniques such as machine learning"). Then the
  existing validation table, rebuilt as **SR 26-2's checklist applied to this part's networks**, each row lighting
  the chapter that did it (held-out error ch3; input ranges ch4–5; known answers ch9, ch11; the simulator as the
  model ch19; nightly checks against Part 16's engine).
- Derivation: none (an industry chapter); one computed panel: the "known answers" scoreboard of the part (u₀ vs
  57.300; stopping vs binomial; no-cost hedger vs BS; drift hedger vs Merton), all from the caches.
- Pause-and-predict: "Under SR 26-2, is the market generator a model?" (Yes: it produces the scenarios the hedger is
  validated on.)
- Compute: none.

### 18 · Frontier: 2023–2026 (2.8) · `s12a_frontier` (new)
- Goal: where the field is now, with one result recomputed on screen.
- Beats (cards, each with the finding quoted from the abstract; all fetched from arXiv this session):
  - **Arbitrage-free generative option markets** (Buehler, Horvath, Kratsios, Limmer, Saqur, Wiese): SANOS (2026:
    smooth, strictly arbitrage-free surfaces; calibration "formulated as a linear program", S&P 500 options); DYSANOS
    (2026: a generative model of SANOS surfaces, 891 OptionMetrics S&P surfaces Jan 2022–Aug 2025, AR(1) baseline,
    "free of dynamic arbitrage" numerically on 100,000 paths); GROMM (Oct 2026: statically and dynamically
    arbitrage-free, initial state "within bid/ask for more than 95%" of relevant prices); PIVOT (2026: a differentiable
    implied-vol layer through Jäckel's solver). This is the deep hedger's missing piece: a simulator of *option* markets.
  - **Is the deep hedger hedging?** François et al. (2024, speculation); Zernikov (2026: TD3 agents on S&P 500 options
    2015–2023 "usually learn a systematic delta haircut"); Maggiolo–Nuti–Štrupl–Szehr (2025: local optima under
    non-convex costs; AlphaZero "more sample-efficient"); Godin (2026, "Is deep hedging reinforcement learning?").
  - **Making it train**: Mueller–Akkari–Gonon–Wood (2024: second-order optimizer "in 1/4 of the number of steps" on a
    cliquet); Arzel–Lehdili (2026: a WW prior for band networks "converges faster": **recomputed in ch14**);
    Neagu–Godin–Simard–Kosseim (2024: market impact); He–Sutter–Gonon (2025: adversarial training).
  - **Stopping and BSDEs**: Reppen–Soner–Tissot-Daguette (2022, neural boundary); Bayer–Pelizzari–Schoenmakers (2023,
    primal and dual with signatures); Ye–Wong (2025, DeepMartingale: the dual learned); Huang–Oosterlee (2026, the
    compound BSDE: fully forward).
  - **Generators and calibration**: Issa–Horvath–Lemercier–Salvi (2023, signature-kernel scores; Part 5 trains it);
    Guyon–Mustapha (joint SPX/VIX, ch15).
- Visual: a frontier map (the part's chapters as nodes, each paper attached where it extends one), lit card by card.
- Experiment: the WW-prior result from `band_prior` (ch14) restated with the paper's claim beside it; the narration
  says whether our small run agrees.
- Pause-and-predict: "Which is harder to build: a hedger, or the simulator it trains on?"
- Compute: none new.

### 19 · The House: Rule 17, tested (2.0) · items 9–10 · `s13_house` (deepened)
- Goal: the House's rule, and the experiment that justifies it: a hedger is only as good as its simulator.
- Beats: Rule 17 card (kept). **The cross-generator matrix**: band hedgers (0.5% costs) trained on GBM (from
  `hedge_seeds`) and on GJR-GARCH paths fitted to BTC (rescaled to 20% annual vol), each tested on GBM, GJR-GARCH and
  real BTC 30-day windows (2017–2025, rescaled likewise), plus daily delta and WW on the same paths: a 3 × 4 heat map
  of indifference prices filling cell by cell. Narration branches on whether the GBM-trained hedger degrades most on
  real windows. Trial counter stays at 73 (nothing is a strategy).
- Experiment: `crossgen` (new).
- Compute: `crossgen` (8 min).

### Outro (2.4) · `s14_outro` (deepened)
- Recap (one line per chapter, numbers from the caches); **desk questions** (keep 3; add "Your deep hedger makes money
  on average with no costs. Is it hedging?"); **problems** (keep 5; add 6: "Derive Leland's volatility" and 7: "Show
  the CARA hedge under drift is Δ + μ/(γσ²S)"); payoffs; references (add the frontier and the new classics); House;
  next part.

---

## 3b. Hands-on summary

**Labs (≥ 3 required; 8 planned; all ≤ 12 lines of `explainer/quant/house/deep.py` unless stated):**

| # | Ch | Function | Lines | Output on screen (cache) |
|---|---|---|---|---|
| 1 | 1 | `train_mlp_regressor` | 397–404 | n_train 66,150; final MSE per seed; slice error |
| 2 | 4 | `calibrate_neural` | 166–170, 177–182 | (H, η, ρ) = (0.074, 1.89, −0.40); RMSE 0.97; 27 s |
| 3 | 6 | `train_differential` | 473–481 | price/delta RMSE plain vs differential, n = 1,024 |
| 4 | 9 | `deep_bsde` (`run`) | 524–534 | u₀ at 0 / 1,000 / 4,000 iterations; 57.300 |
| 5 | 10 | `deep_stopping` | 620–628 | 13.886 (13.902); 26.107 ± 0.020 |
| 6 | 11 | `hedge_pnl` | 272–280 | price, CVaR, sd: network vs delta |
| 7 | 14 | `Hedger.band` + `quoting.ww_band` | 252–256 + 99–101 | learned and WW bands at the money |
| 8 | 16 | `sig_mmd` + `signature` | 775–780 (+ 740–747) | signature distances by generator |

**Replays (every network shown learning; seeds as bands; baselines at equal budget):** ch1 HLP (3 seeds; BS curve as
the target); ch3 calibrator (2 seeds; label-noise floor as a line); ch4 calibration through the net (12 starts as a
band); ch6 DML (3 seeds each, plain vs differential at equal n); ch9 deep BSDE (2 seeds; reference line; linear run);
ch10 stopping (date by date; region forming); ch11 no-cost hedger (3 seeds; BS delta as target); ch12 drift hedger
(Merton line as target); ch13 band emerging (3 seeds; WW corridor); ch14 WW-prior vs default (2 seeds each); ch15 neural
SDE calibrate-then-push (2 seeds); ch16 DDPM (3 seeds) and the sig-LSTM's cached curve. Implementation: the
`TrainingReplay` instrument with a `frame(i)` per checkpoint; 3D frames (ch4, ch14) rebuild a `price_surface` per
checkpoint inside a `ThreeDScene` with `add_fixed_in_frame_mobjects` for the loss panel.

**Live simulations:** the hook's path riding the band; ch1's hedge ledger; ch8's BSDE shooting; ch11's coinciding
holdings; ch12's sliding CVaR threshold; ch14's bead on the band surface; ch16's reverse diffusion; ch19's heat map
filling.

**3D (`ThreeDScene`):** ch1 price surface and its error; ch4 the network's IV surface morphing onto the Surface's
quotes; ch7 tangent planes, the two fits and the GP shell; ch10 the exercise tunnel; ch14 the band sheets over (τ, S);
ch15 low/high/Heston IV surfaces.

**Compute budget (new items only; one core, unloaded; seeded; resumable per seed with `CACHE.partial`):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| hlp_replay (3 seeds) | 6 | bsde_seeds (seed 1 + linear) | 16 | hedge_seeds (2 seeds × 3 costs, `.pt` saved) | 18 |
| greeks_act (3 acts × 3 seeds) | 8 | stopping_region (d = 2) | 6 | band_prior (2 × 2) | 8 |
| calib_ckpt (1 seed, 5 ckpts) | 12 | hedge_replay (no-cost + cost, 3 seeds) | 18 | nsde_trace (2 seeds) | 20 |
| calib_noise (300 sets) | 4 | risk_measures (3 seeds × 2) | 6 | ddpm_reverse (3 seeds) | 3 |
| calib_trace | 1.5 | drift (2 μ × 3 seeds) | 6 | crossgen (1 training + evals) | 8 |
| dml_seeds | 10 | leland | 1 | hedge_live | 0.2 |
| dml_replay | 1.5 | dml2d | 2 | | |

Total ≈ **155 CPU-minutes** on one core unloaded, of which about 40 can be cut by running `nsde_trace` with one seed and
`hedge_replay` at batch 2,048 (≈ 115 min, inside the 2 h budget). Optional, lead's call: `stopping_budget` (35) and
`gen_snaps` (23). `calib_data` (the existing 1-hour item) is **not** re-run. Every training item uses
`torch.set_num_threads(1)` (2 under no contention), `CACHE.partial` per seed, and saves the policy or network
(`.pt`) so later items (hook's live path, `crossgen`) evaluate rather than retrain. One command rebuilds the part:
`python -m videos.quant.quant17.compute`.

**House library additions** (append to `explainer/quant/house/deep.py`; tests appended to `tests/test_quant_house.py`):
- `gbm_torch_mu(n, steps, T, sigma, mu, S0, gen)`; `train_hedger_p(..., mu=0.0)` (thin wrapper using it). Test: mu = 0
  reproduces `gbm_torch` draws for the same generator.
- `merton_hedge(S, sigma, mu, gamma)` = μ/(γσ²S). Test: the drift-trained hedger's mean deviation from delta is within
  0.02 of it (small run, 300 iterations).
- `leland_sigma(sigma, cost, dt)`. Test: cost 0 returns sigma; matches the closed form at c = 0.5%.
- `cvar_ru(X, w, alpha)` (Rockafellar–Uryasev form with a trainable threshold) and `risk="cvar_ru"` via a new
  `train_hedger_risk`. Test: minimizing over w on a fixed sample returns the empirical CVaR within 1e-3.
- `WWBandHedger(Hedger)` (band network whose softplus offsets start at WW's half-width). Test: at initialization its
  band equals `quoting.ww_band` within 1e-3 at the money.
- `calibrate_neural_trace(...)` (as `calibrate_neural`, also returning iterates). Test: final parameters equal
  `calibrate_neural`'s for the same seed.
- `gp_with_gradients(X, y, dY, Xq, ls, noise)` (numpy RBF GP on stacked value and gradient observations). Test: on a
  quadratic in 2-D, interpolates values and gradients at the data within 1e-4.
- `ddpm_reverse_snapshots(sample_fn, ...)`: exposes intermediate x_t (a variant of `train_ddpm`'s sampler; append a
  new `train_ddpm_snap` rather than editing `train_ddpm`). Test: the final snapshot equals `sample(n, seed)`.
- `deep_bsde(..., snap_at=())` cannot be edited (append-only): append `deep_bsde_snap` returning (Y_N, g) scatters.
  Test: with δ = 1 and 300 iterations, u₀ is within 1.5 of the MC no-default price.
- `deep_stopping_regions(...)` (d = 2 regions per date). Test: the region at the last exercise date contains
  (150, 60) and not (100, 100).
- `garch_paths_torch(params, residuals, n, steps)` for `crossgen`. Test: unconditional variance matches ω/(1 − α − γ/2 − β) within 10%.

---

## 4. Verified sources for the industry and frontier chapters

Checked this session (2 November 2026) by fetch or search:

| Fact | Source |
|---|---|
| BCJ Table 1: d = 5, s₀ = 100: L̂ 26.156, Û 26.162, point 26.159, 95% CI [26.138, 26.174], Broadie–Cao CI [26.115, 26.164]; d = 2: 13.895/13.903, binomial 13.902; 3,000 + d training steps, batch 8,192, two hidden layers of d + 40, float32 on a GTX 1080; tL = 28.1 s (d = 5); *JMLR* 20 (2019) paper 74 | https://arxiv.org/abs/1804.05394 (PDF read) |
| Buehler's arXiv record: deep hedging (2018), risk-neutral IV dynamics (2021), near-martingale measures (2021), Deep Bellman hedging (2022), continuous RL across risk aversions (2022), SANOS (Jan 2026), PIVOT (Jun 2026), DYSANOS (Aug 2026), GROMM (Oct 2026), uncertainty-aware strategies (2025) | https://export.arxiv.org/api/query?search_query=au:Buehler_Hans ; abstracts: 2601.11209, 2608.12587, 2610.16732, 2606.17065, 2207.00932, 2111.07844 |
| Deep-hedging literature 2023–2026 (titles, authors, dates; quoted findings) | arXiv: 2407.14736, 2504.06208, 2410.22568, 2603.29994, 2605.21696, 2303.16585 (*Quantum* 7, 1191), 2510.01874, 2402.13326, 2508.14757, 2607.13353 |
| Optimal stopping 2022–2026 | arXiv: 2205.04595, 2312.03444, 2510.13868, 2601.18634, 2210.10443 (Gonon, expressivity) |
| Imaki et al., *J. Financial Data Science* DOI 10.3905/jfds.2023.1.125 | https://arxiv.org/abs/2103.01775 |
| Ferguson–Green (2018): "a million times faster" | https://arxiv.org/abs/1809.02233 |
| Huge–Savine (2020) abstract; Bayer–Stemper (2018); Liu–Oosterlee–Bohte (*Risks* 7(1), 2019); Gierjatowicz et al.; Buehler–Horvath–Lyons–Perez Arribas–Wood (2020) | arXiv 2005.02347, 1810.03399, 1901.08943, 2007.04154, 2006.14498 |
| Kidger–Foster–Li–Oberhauser–Lyons (ICML 2021); Liao et al. (2020) conditional SigWGAN; Ni et al. (2021) SigWGAN; Quant GANs (*QF* 2020); Issa et al. (2023) | arXiv 2102.03657, 2006.05421, 2111.01207, 1907.06673, 2305.16274 |
| PRA SS1/23: published 17 May 2023, effective 17 May 2024; current version 23 April 2026; scope: banks with IRB/IMA/IMM approval; covers "the use of artificial intelligence in modelling techniques such as machine learning" | https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss |
| SR 26-2 (17 April 2026; Fed/OCC/FDIC; supersedes SR 11-7 and SR 21-8; generative and agentic AI outside scope) | verified by the lead; https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm |
| Risk.net: Hans Buehler, Quant of the Year 2022; Flow Trader since 2018 on S&P 500 and Euro Stoxx vanilla index books; later to XTX Markets as deputy CEO | https://www.risk.net/awards/7926411/quant-of-the-year-hans-buehler ; https://www.risk.net/people/7946131/people-moves-exit-buehler-for-xtx-spitz-quits-ca-and-more (search snippets; pages paywalled) |
| Guyon–Mustapha, "Neural joint S&P 500/VIX smile calibration": SSRN 4309576 (Dec 2022, rev. Jan 2024): "fit both smiles and VIX futures within bid-ask spreads"; *Risk* cutting edge | https://papers.ssrn.com/abstract=4309576 ; https://www.risk.net/cutting-edge/7958175/neural-joint-sp-500vix-smile-calibration |
| Kelly–Xiu, NBER w31502 (July 2023); *FnT Finance* 13(3–4):205–363 | https://www.nber.org/papers/w31502 |
| DHB chapter list (12 chapters, three parts) | bookseller listing (Eyrolles) via search; Springer confirms 12 chapters |

**Unverified (keep the marks or drop):** the "about 70% of J.P. Morgan's Euro Stoxx flow options" figure (on screen now
in `s01_hook` and `s12_production`; the search did not surface it; check the Risk.net article or drop to "a large
chunk of its Euro Stoxx vanilla book", which the search did surface); the year of Buehler's move to XTX; Guyon's Risk
Quant of the Year (2025 per the search summary; page did not load) and the *Risk* issue date of the Guyon–Mustapha
article; Scotiabank as Ferguson and Green's affiliation; Davis–Panas–Zariphopoulou (1993) citation details; Dugas et
al. (2009) and Ackerer–Tagasovska–Vatter (2020) venues; Hutzenthaler–Jentzen–Kruse–Nguyen (2020) venue; Halperin's
QLBS venue; Kolm–Ritter venue; DHB and Kelly–Xiu section numbers; the Jentzen–Kuckuck–von Wurstemberger book; venues
of Buehler's 2021–2022 follow-ups; the Ruf–Wang phrase to be quoted.

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 17 · Deep Pricing and Hedging (~58; frontier)
1. Learning a pricing formula: Hutchinson–Lo–Poggio (1994) redone and replayed; universal approximation; a network's
   Greeks (activation decides gamma) and no-arbitrage shapes.
2. Neural calibration (Horvath–Muguruza–Tomas 2021): learning rough Bergomi's pricing map from Monte Carlo, the label
   noise floor, calibration as gradient descent through the network (the 3D surface converging), the training box's
   wall; two years of weekly surfaces.
3. Differential ML (Huge–Savine 2020): pathwise labels proved unbiased; the twin network; tangent planes in 3D; the
   Gaussian process with gradients as its exact, unscalable twin.
4. Deep BSDE (E–Han–Jentzen 2017; Han–Jentzen–E 2018) in 100 dimensions: the BSDE derived from Itô, nonlinear
   Feynman–Kac (Pardoux–Peng), u₀ replayed with seeds, the linear check; DGM and multilevel Picard.
5. Deep optimal stopping (Becker–Cheridito–Jentzen 2019): the bang-bang proof, the exercise tunnel in 3D, the lower
   bound, against Longstaff–Schwartz at equal budget (Part 16).
6. Deep hedging (Buehler–Gonon–Teichmann–Wood 2019): entropic risk and CVaR, indifference prices (Hodges–Neuberger),
   the no-cost check; the drift trap (Merton's term rediscovered; near-martingale measures).
7. What the deep hedger learns: Leland and Whalley–Wilmott derived, the band emerging in training, the band network
   (Imaki et al. 2021) and the learned hedge as a surface in (time, spot).
8. Neural SDEs with robust exotic bounds (Gierjatowicz et al. 2022): calibrate, then push; joint SPX/VIX (Guyon–Mustapha).
9. Market generators: GARCH, Quant GANs, signature generators (Buehler et al. 2020; Ni et al. 2021), diffusion models
   (AI Part 21); judged by signature MMD and Part 1's stylized facts; hedgers tested across generators.
10. Production: SR 26-2 (April 2026, replacing SR 11-7) and PRA SS1/23; what has reached desks (J.P. Morgan, Danske);
    the frontier 2023–2026 (arbitrage-free generative option markets; is deep hedging speculation?).

*Textbooks:* Dixon–Halperin–Bilokon ch. 1, 3–5, 8, 10, 12; Kelly–Xiu §2. Glasserman 7–8 and Savine → Part 16.
*Trained (all replayed, seeds as bands):* HLP networks (three activations); the calibrator and the calibration; DML
and a GP with gradients; deep BSDE (with the linear check); deep stopping; the deep hedger (entropic, CVaR, under
drift, with costs); the band network (with a WW prior); a neural SDE; DDPM and a signature LSTM.
*Visuals:* the band riding a live path; the price surface and its error in 3D; the IV surface converging onto the
quotes; tangent planes; BSDE shooting; the exercise tunnel; the band sheets over (time, spot); low/high model surfaces;
reverse diffusion; the cross-generator heat map.
*Labs:* `train_mlp_regressor`, `calibrate_neural`, `train_differential`, `deep_bsde`, `deep_stopping`, `hedge_pnl`,
`Hedger.band`/`ww_band`, `sig_mmd`.
*Firms:* J.P. Morgan (deep hedging in production, as reported by Risk.net); Danske Bank (DML, AAD).
*Industry:* SR 26-2; PRA SS1/23; quantum deep hedging (2023). *Frontier:* SANOS/DYSANOS/GROMM (2026); François et al.
(2024); Mueller et al. (2024); Arzel–Lehdili (2026); Reppen–Soner–Tissot-Daguette; Bayer–Pelizzari–Schoenmakers.
*Desk:* "Your hedger has costs. Why does the optimal hedge have a band?"; "A neural calibrator fits beautifully. How
do you know it is right?"; "Why record the payoffs' derivatives?"; "Your deep hedger makes money on average with no
costs. Is it hedging?"
*House:* the deep hedger and the market generator; Rule 17 (no network without a slower, independent engine; tested on
two generators and on history) (the finale stress-tests the House with it).
```

---

## 6. Minutes, new modules, data, risks

**Minutes per scene** (target 57.5; `lecture_length.py --floor 50`):

| Scene | Min | Scene | Min | Scene | Min |
|---|---|---|---|---|---|
| `s01_hook` H | 2.8 | `s05_dml` 6 | 3.0 | `s09_band` 13 | 2.9 |
| `s02_hlp` 1 | 2.9 | `s05a_dml3d` 7 | 2.5 | `s09a_band3d` 14 | 2.9 |
| `s02a_greeks` 2 | 2.5 | `s06_bsde` 8 | 3.0 | `s10_nsde` 15 | 3.0 |
| `s03_calib` 3 | 2.9 | `s06a_bsde_train` 9 | 2.5 | `s11_generator` 16 | 3.1 |
| `s03a_calibrate` 4 | 2.8 | `s07_stopping` 10 | 3.0 | `s12_production` 17 | 2.8 |
| `s04_roughhist` 5 | 2.4 | `s08_hedger` 11 | 3.0 | `s12a_frontier` 18 | 2.8 |
| | | `s08a_drift` 12 | 2.6 | `s13_house` 19 | 2.0 |
| | | | | `s14_outro` | 2.4 |

Total 57.8. Kept modules and class names: all 14 (narration and manim caches are keyed by them); new modules
`s02a_greeks` (Greeks), `s03a_calibrate` (Calibrate), `s05a_dml3d` (DML3D), `s06a_bsde_train` (BSDETrain),
`s08a_drift` (Drift), `s09a_band3d` (Band3D), `s12a_frontier` (Frontier). The chapter numbers on every
`chapter_card` change (2 → 3, …): edit all `chapter_card(n, …)` calls and the "Chapter n" narration lines with the
manifest. Timeline: append (2011, "SR 11-7: model risk") and (2026, "SR 26-2; generative option markets") if the lead
agrees (append-only rule).

**Data:** nothing new to fetch. Part 13's Deribit surfaces (via `Q13._quotes`), Binance BTCUSDT daily closes (via
`data.binance_klines`), Part 14's `rbergomi` and Part 16's `maxcall` read through their `load`. `crossgen` reuses
the generator item's BTC windows.

**Risks and decisions for the lead:**
1. **The calibrator's "label noise" comparison is wrong as stated.** `compute_calib` measures noise as the RMSE of
   (label with 10k paths) − (fresh MC with 20k paths), whose variance is 1.5 s²_{10k}, not s². "Held-out 1.90 below
   the 2.86 noise" therefore compares unlike things. `calib_noise` (ch3) decomposes it properly; the narration must
   follow the result. **Planning run** (40 held-out sets, 2,940 points; network vs its 10k-path label, vs a fresh
   20k-path MC, and label vs fresh): RMSE 1.54, 0.95 and 1.82 vol points (medians 0.69, 0.47, 0.76). So the 10k-path
   label noise is about 1.49 (= 1.82/√1.5), and the network is **closer to the fresh, less noisy simulation than its
   own training labels are** (0.95 against 1.82): it has averaged the noise away. The variance split is not exact
   (heavy-tailed implied-vol noise; the two estimates of the network's own error disagree, 0.40 and below 0), so
   the screen should show the three RMSEs and medians, not a derived "true error". The cached 2.86 came from 12 sets
   and is outlier-driven.
2. **Deep BSDE's 0.12%** quotes a single iterate; the last 1,000 iterations average 57.354 ± 0.043 (planning run on
   the cache), 0.09% high. Report the average with its spread.
3. **Deep stopping loses to LSM at our budget** (26.107 vs Part 16's planning 26.146 ± 0.031; BCJ 26.156 at 6× the
   steps on a GPU). Decide: (a) say so (recommended; it is the honest result and Part 16 already plans to say it), or
   (b) spend ~35 CPU-min on `stopping_budget` (1,500 steps per date) and branch on it.
4. **DML's n = 256 plain error 5.03** may be one bad seed; `dml_seeds` settles it before the narration repeats "cuts
   the error from 5.03 to 0.43".
5. **The 70% J.P. Morgan figure** is on screen in two scenes and unverified this session (§4).
6. **READING.md fixes**: Kidger et al. author list (add Oberhauser); split the two Sig-Wasserstein GAN papers; add
   Imaki et al., Leland, Pardoux–Peng, Rockafellar–Uryasev, Ferguson–Green, the 2023–2026 list.
7. `deep.sig_mmd`'s docstring says each level is "scaled by k!", the code does not scale (the tensor exponential
   already carries 1/k!): fix the docstring (one-line House edit; not append-only, so the lead decides).
8. Ownership: Part 16 keeps AAD, LSM, duality and the computing industry (STAC, GPUs); Part 14 keeps the
   neural-surrogate lineage and the speed race; Part 11 keeps a short learned-hedger replay that links here; Part 5
   trains the neural SDE generator (`deep.train_nsde`); this part references each in one line.
9. Load: on the shared machine (load 18–25 during planning) every training item ran 2–3× slower than its unloaded
   estimate; run `compute` under `nice -n 10`, one thread per item, two items at a time at most.

**Chinese:** new terms for `QUANT_ZH_GUIDE.md`: 无交易区间 (no-trade band), 无差异价格 (indifference price), 熵风险度量
(entropic risk measure), 条件风险价值 (CVaR), 差分机器学习 (differential ML), 路径导数 (pathwise derivative), 倒向随机微分方程
(BSDE), 非线性费曼–卡茨 (nonlinear Feynman–Kac), 斯内尔包络 (Snell envelope), 神经网络校准器 (neural calibrator), 标签噪声
(label noise), 扩散模型 (diffusion model), 期望签名 (expected signature), 市场生成器 (market generator), 默顿项 (Merton term).

**README:** chapter list with minutes; the textbook audit table of §2b; the paper list of §2c plus §4; desk questions 1–4
and problems 1–7 with solutions in English and Chinese; the build command.

## 7. Lead's decisions (2 Nov 2026)

1. Yes: add `calib_noise` and reword chapter 3 to what it measures (network vs fresh Monte Carlo against label vs fresh), dropping "below the noise of its labels" unless the new item supports it, in EN, ZH, README and the recap.
2. Corrected: Part 16 computed LSM at 26.103 ± 0.014 (2M evaluation paths) vs deep stopping 26.107 ± 0.020 — a tie; both below BCJ. Say they tie at our budget; no `stopping_budget` item. Cite BCJ Table 1's bounds [26.156, 26.162] as theirs.
3. Yes: the deep BSDE as a tail average with spread.
4. Yes: `dml_seeds`; the headline follows the seeds.
5. The "about 70%" J.P. Morgan figure: verify from Risk.net's own article, or replace it in both scenes (and zh lines, on-screen text, README) with the wording that is confirmed.
6. Yes: READING.md fixes (Kidger et al. with Oberhauser; split the two sig-Wasserstein papers; add Imaki, Leland, Pardoux–Peng, Rockafellar–Uryasev, Ferguson–Green and 2023–2026 papers).
7. Yes: fix `deep.sig_mmd`'s docstring to match the code (small exact edit); append 2011 and 2026 to the timeline if used.
8. No `gen_snaps`: the machine is loaded; the signature-LSTM replay uses the cached loss curve.
Keep the existing compute items and their cached results (the Chinese dry run of the current version passed); `calib_data` is not re-run.
