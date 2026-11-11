# Part 14 · Rough and Path-Dependent Volatility: expansion plan (19.9 → ~57 min)

This is a planning document; nothing in the repo was changed. Sources read:
* `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 (the standard) and §6 Part 14 (12 items) with its neighbours, Parts 13 and 15.
* `READING.md`: the textbook table and the §4 Part 14 paper list (22 papers). `videos/ai/LECTURE_GUIDE.md`;
  `videos/quant/plans/{IMPLEMENT,quant5,quant7}.md`.
* Every file in `videos/quant/quant14/` and the cached results in `.cache/quant14/`.
* The House: `explainer/quant/house/{rough,sim,stochvol,surface,arbitrage}.py`, plus `explainer/quant/viz.py` (`lab_card`,
  `lab_run`, `TrainingReplay`, `seed_band`).
* Neighbours, to avoid duplication: Part 5's plan already does fBM, the H dial, Mandelbrot–Van Ness and the Cont–Das artefact on
  simulated data, as well as Hawkes thinning and signatures. Part 7's plan measures H on its own RV and shows the RFSV kernel next
  to HAR. Part 13 has Bergomi's forward variance and the SPX/VIX puzzle (Gatheral 2008). Part 17 (`s04_roughhist`)
  calibrates rough Bergomi weekly with a neural calibrator.

Part 14 therefore assumes fBM and Hawkes basics. It goes **past** them into the models, the numerics, the
estimation debate and the 2020–2025 frontier.

Probe runs this session used `.venv/bin/python` with `OMP_NUM_THREADS=1`, about 12 CPU-minutes in total. Scripts
are in `scratchpad/q14/`. The numbers marked *(probe)* are real but must be recomputed by `compute.py`.

---

## 1. Current state (`python tools/lecture_length.py quant14`: **19.9 min**, 12 scenes)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 1.4 | A Brownian path and an H = 0.1 path, zoomed ×16 and ×256 (strong idea, but static panels). Objectives, House card. **No history segment.** |
| 1 | `s02_fact` | 1.8 | The Surface's ATM skew on log–log axes: power law T^−0.49 (H ≈ 0.01) against the bounded (T + 21 d)^−0.88 (log RMSE 0.19 against 0.23). A Volterra ladder (2 rows). **No derivation of why a kernel gives T^{H−½}; one day only; no comparison with model skews.** |
| 2 | `s03_rough` | 1.8 | BTC log RV (5-minute returns, 700 days) against fBM; m(q, Δ) lines; H = 0.08 (0.12 with weekdays evened out); estimator on fBM: 0.05 → 0.01, 0.1 → 0.09, 0.3 → 0.31, 0.5 → 0.50. Good data, but **no lab, no forecasting (GJR's second half), no long-memory/Comte–Renault contrast.** |
| 3 | `s04_rbergomi` | 1.9 | Model ladder, 4 paths, fit H = 0.03, η = 2.05, ρ = −0.56, error 0.83 vol pts against Heston's 1.37 on the same 175 quotes. **No martingale derivation, the hybrid scheme is named but not shown, the fit is not replayed, no seeds.** |
| 4 | `s05_rheston` | 2.5 | Characteristic function and fractional Riccati (3 rows, quoted). Free fit: H = 0.45, ν = 4.5, λ = 16, error 1.28. With H held at 0.1: 1.49; at 0.2: 1.41; at 0.05: 2.25. Skew term structures. **No derivation from the Volterra equation, no Adams scheme on screen, no convergence check.** |
| 5 | `s06_hawkes` | 1.5 | Activity panels at n = 0.5/0.9/0.99, and the Jaisson–Rosenbaum and El Euch–Fukasawa–Rosenbaum statement. **Asserted, not derived or measured.** |
| 6 | `s07_lift` | 1.5 | Kernel against a sum of exponentials; the 30-day smile error falls from 4.70 vol pts (N = 1) to 1.11 (10), 0.57 (20) and 0.26 (50). Good. **Identity not derived; Abi Jaber (2019) lifted Heston named only.** |
| 7 | `s08_debate` | 1.7 | Weekend trap (H 0.08 → 0.12). Three smooth models read 0.38 / 0.42 / 0.02. **Only the time-series side; the options-side debate (Guyon–El Amrani, Abi Jaber–Li, Rømer) is missing; no estimator theory.** |
| 8 | `s09_pdv` | 1.8 | Guyon–Lekeufack on DVOL: R² 0.88 in sample, 0.42 out of sample, against the baseline's 0.68 and −0.27. The activity term does the work. Good. **No 4-factor PDV, no S&P 500 replication, no replay of the fit.** |
| 9 | `s10_frontier` | 1.0 | Four history cards: qRH 2020, Guyon 2022, signatures 2023, HMT 2021. **Items 9, 10, 11 and 12 are a sentence each.** |
| 10 | `s11_house` | 0.8 | Library table, Rule 14, trial counter 73. |
| — | `s12_outro` | 2.4 | Recap, 3 desk questions, 5 problems, payoff, references. |

Overall: the computed results are good and real, and all are kept. But every chapter is about 1.5–2.5 minutes, and items 9–12 are
history cards. The part has **no lab moments, no replays, no 3D, no live simulation**: the panels appear finished. There is **no
industry chapter, no crisis file** (the syllabus names 5 August 2024) and no 2023–2026 frontier beyond Cont–Das.

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item | Now | Plan |
|---|---|---|
| 1 ATM skew ∝ T^{H−½} | ch1, 1.8 min, one day | ch1 (102 weekly surfaces, 3D) + ch2 (derivation, model skews, Fukasawa 2021) |
| 2 Volatility is rough, re-measured | ch2 | ch3 (estimator lab, two BTC eras) + ch4 (RFSV forecasting against HAR) |
| 3 rBergomi; hybrid scheme | ch3 | ch5 (model, martingale proof, calibration replay) + ch6 (hybrid scheme lab, exactness check) |
| 4 Rough Heston: fractional Riccati, Adams | ch4 | ch7 (derivation from the Volterra Heston equation, fit) + ch8 (Adams lab, convergence, 3D characteristic function, H profile) |
| 5 Nearly unstable Hawkes | ch5 (asserted) | ch9 (branching sweep computed; Jaisson–Rosenbaum argument; leverage) |
| 6 Markovian lifts | ch6 | ch10 (identity derived, lifted Heston, Bayer–Breneis) |
| 7 The debate | ch7 | ch11 (time series: weekend, bias map in 3D, estimator theory) + ch12 (options: power law or not, weekly; model horse races) |
| 8 PDV, 4-factor | ch8 | ch13 (BTC/DVOL, replay, Markovian 4FMPDV) + ch14 (S&P 500/VIX replication and the 5 Aug 2024 crisis) |
| 9 Quadratic rough Heston, joint SPX/VIX | 1 card | ch15, first half (simulated; Zumbach effect measured) |
| 10 Guyon's DMSP | 1 card | ch15, second half (puzzle explained; martingale-transport lab with bounds) |
| 11 Signature volatility models | 1 card | ch16 (calibrated to the Surface by a quadratic-in-parameters trick: lab and replay) |
| 12 What desks use and why | 1 card | ch17 (industry: speed, surrogates, lifts, Risk awards, VIX1D/0DTE; the House) |
| frontier | — | ch18 (2023–2026) |

### (b) Textbook sections → chapter

**Bayer, Friz, Fukasawa, Gatheral, Jacquier and Rosenbaum (eds.), *Rough Volatility* (SIAM 2023).** The table of contents was
verified via Crossref, DOI prefix 10.1137/1.9781611977783:

| Book chapter | Plan |
|---|---|
| 1 Volatility is rough (Gatheral–Jaisson–Rosenbaum), pp. 1–29 | ch3, ch4 |
| 2 Pricing under rough volatility (Bayer–Friz–Gatheral), pp. 31–58 | ch5 |
| 3 No-arbitrage implies power-law market impact and rough volatility (Jusselin–Rosenbaum), pp. 59–82 | ch9 (statement and card); impact → Part 37 |
| 4 Rough Heston (Gerhold–Jacquier–Rosenbaum), pp. 83–101 | ch7, ch8 |
| 5 Rough affine models (Keller-Ressel–Larsson–Pulido), pp. 103–113 | ch7 (affine Volterra card), ch10 |
| 6 Hedging under rough volatility (Fukasawa–Horvath–Tankov), pp. 115–125 | ch17 (hedging with forward variance; card) |
| 7 Hybrid scheme (Bennedsen–Lunde–Pakkanen), pp. 127–155 | ch6 |
| 8 Asymptotics (Bayer–Friz–Fukasawa–Jacquier), pp. 157–182 | ch2 (short-time skew) |
| 9 Forest expansion of forward variance models (Friz–Gatheral), pp. 183–198 | ch2 (named as the exact series behind the first-order skew formula) |
| 10 Regularity structure for rough volatility (Bayer–Friz–Gassiat–Martin–Stemper), pp. 199–244 | ch18 (one card); README note: the full theory is beyond the series |

**Guyon–Henry-Labordère, *Nonlinear Option Pricing* (CRC 2013/14).** Chapter list from Crossref (DOI 10.1201/b16332-6…-18):

| Book chapter | Plan |
|---|---|
| 1 Option pricing in a nutshell; 2 Monte Carlo; 3 Some excursions | Parts 9, 16 |
| 4–5 Nonlinear PDEs, examples; 6 early exercise; 7 BSDEs | Parts 8, 16, 17 |
| 8 Uncertain lapse and mortality | README note (insurance; not core to the series) |
| 9 Uncertain volatility model | Part 15 (`s09_uvm`) |
| 10 McKean nonlinear SDEs; 11 Calibration of LSV models (particle method) | Part 13 (SLV). Here: ch13, a card on calibrating PDV to smiles as a McKean problem *(verify that ch. 11 treats path-dependent volatility)* |
| 12 Local correlation models | Part 15 (worst-of) |
| 13 Marked branching diffusions | Part 17 (README pointer) |

**Secondary sources used for derivations.** Bergomi, *Stochastic Volatility Modeling* (2016): ch. 7–8, forward variance
models and the expansion of the smile at first order in vol of vol → ch2 *(verify chapter numbers)*. Gatheral, *The
Volatility Surface*, ch. 3–5 (ATM skew of stochastic volatility and jump models) → ch2; the computed model skews replace
any claim about jumps. Friz–Hairer (2nd ed. 2020): rough paths for rough volatility → ch16 and ch18 (the regularity
structure card) *(verify which chapter of the 2nd edition treats rough volatility)*.

### (c) Papers on the Part 14 list in READING.md, and where they appear

| Paper | Now | Plan |
|---|---|---|
| Comte–Renault 1998 | absent | ch4: long memory (H > ½) against roughness (H < ½), one card |
| Alòs–León–Vives 2007 | on screen | ch2 derivation credit |
| Fukasawa 2011 | on screen | ch2 |
| Bayer–Friz–Gatheral 2016 | on screen | ch5 |
| Jaisson–Rosenbaum 2016 | on screen | ch9 |
| Bennedsen–Lunde–Pakkanen 2017 | on screen | ch6 lab credit |
| Gatheral–Jaisson–Rosenbaum 2018 | on screen | ch3, ch4 (forecast formula) |
| El Euch–Fukasawa–Rosenbaum 2018 | on screen | ch9 (leverage from no-arbitrage) |
| Livieri–Mouti–Pallavicini–Rosenbaum 2018 | **absent** | ch12 (H implied from options; *(verify their reported H)*) |
| Bayer–Stemper 2018 | **absent** | ch17 (neural calibration lineage) |
| El Euch–Rosenbaum 2019 | on screen | ch7, ch8 |
| Abi Jaber–El Euch 2019 | on screen | ch10 |
| Abi Jaber 2019 (lifted Heston) | **absent** | ch10 (the lifted Heston, *QF* 19(12)) |
| Gatheral–Jusselin–Rosenbaum 2020 | card | ch15 |
| Guyon 2020 (puzzle solved, *Risk*) | **absent** | ch15 |
| Fukasawa–Takabatake–Westphal 2022 | **absent** | ch11 (consistent estimation under measurement error) |
| Rømer 2022 | **absent** | ch12 (*QF* 22(10):1805–1838: rough models miss the SPX term structure; a two-factor OU model fits) |
| Guyon–El Amrani 2023 | on screen | ch1, ch12. **Venue: Risk.net "Cutting Edge" (risk.net/7957304), not *QF* as READING.md says: fix** |
| Guyon–Lekeufack 2023 | on screen | ch13, ch14 |
| Cuchiero–**Gazzani**–Svaluto-Ferro 2023 | card | ch16. **READING.md and `s10_frontier` misspell the second author as "Gazzetta": fix.** *SIFIN* 2023, arXiv 2207.13136 (volume *(verify)*) |
| Guyon 2024 DMSP | card ("2022") | ch15. **Verified: *Finance and Stochastics* 28(1):27–79 (2024): drop the *(verify)* in READING.md; the card's year becomes 2024 (working paper 2022)** |
| Cont–Das 2024 | on screen | ch11 |

**Proposed additions to READING.md Part 14** (each verified this session unless marked):
* Fukasawa (2021), "Volatility has to be rough", *QF* 21(1):1–8, arXiv 2002.09215 (ch2).
* Horvath, Muguruza, Tomas (2021), "Deep learning volatility", *QF* 21(1):11–27 (ch17).
* Bolko, Christensen, Pakkanen, Veliyev (2023), "A GMM approach to estimate the roughness of stochastic volatility", *J.
  Econometrics* 235(2):745–778 (H ≈ 0.05 after correcting the measurement error; ch11).
* Chong, Hoffmann, Liu, Rosenbaum, Szymanski (2024), "Statistical inference for rough volatility: minimax theory", *Ann.
  Statist.* 52(4):1277–1306, and "… central limit theorems", *AAP* 34(3) (ch11).
* Bayer, Breneis (2023), "Markovian approximations of stochastic Volterra equations with the fractional kernel", *QF*
  23(1):53–70 (ch10).
* Rosenbaum, Zhang (2022), "Deep calibration of the quadratic rough Heston model", *Risk* (arXiv 2107.01611) (ch15, ch17).
* Abi Jaber, Li (2025), "Volatility models in practice: rough, path-dependent or Markovian?", *Math. Finance* 35(4):796–817,
  arXiv 2401.03345 (ch12, ch18).
* Nutz, Riveros Valdevenito (2024), "On the Guyon–Lekeufack volatility model", *Finance Stoch.* 28(4):1203–1223 *(volume and
  pages from a citing paper: verify)*, arXiv 2307.01319; Andrès, Jourdain (2024), arXiv 2408.02477 (ch13).
* Mandelbrot–Van Ness (1968), already listed under Part 5 (cross-reference only).
* Industry: BIS Bulletin 90 (Aquilina, Lombardi, Schrimpf, Sushko, 27 Aug 2024); BIS Bulletin 95 (Todorov, Vilkov, 29 Oct
  2024); the SEC DERA working paper on the August 2024 VIX spike (sec.gov/files/dera-vix-working-paper-2504.pdf; *authors and
  title (verify)*); Cboe VIX1D launch (24 Apr 2023).

---

## 3. The chapter list (20 scenes: hook, 18 chapters, outro; about 57 min)

**Conventions.**
* **Visual**: the signature picture, built before the formula.
* **Live**: a simulation drawn as it runs.
* **Lab**: `lab_card` with ≤ 12 lines of real House code, then `lab_run` printing cached outputs.
* **Replay**: `TrainingReplay`, or a ValueTracker scrub, through the stored iterates of a fit, with seeds as `seed_band`.
* **Compute**: the item in `compute.py` and its CPU-minutes.

Keep every existing module and class name. The new modules are lettered (`s02a_…`), and `manifest.py` sets the order (CLAUDE.md:
renaming invalidates caches). Narration targets about 139 words a minute.

### H · Hook: "Rough" (2.8 min) · `s01_hook` (deepened)
- **Goal.** The puzzle, the era, the map.
- **Beats.**
  1. **Make the zoom live.** Keep the two paths, but drive the zoom by a ValueTracker: a window shrinks continuously from the whole path to 1/256, and the
     axes rescale as it goes. The Brownian path visibly straightens and the H = 0.1 path does not. A readout shows "zoom ×k".
  2. **New, "how we got here" (about 50 s).** The timeline strip lights:
     * 1968 Mandelbrot–Van Ness;
     * 1987 crash (red: the skew is born; Part 13);
     * 1993 Heston;
     * 1998 Comte–Renault (long memory);
     * 2004 Bergomi;
     * 2007 Alòs–León–Vives;
     * 2014 "Volatility is rough" (arXiv 1410.3394);
     * 2016 rough Bergomi and Jaisson–Rosenbaum;
     * 2019 rough Heston;
     * 2020 quadratic rough Heston and Guyon's puzzle solution;
     * 2021 Risk's Quants of the Year: Gatheral and Rosenbaum (blue);
     * 2023 path-dependent volatility;
     * 2024 Cont–Das;
     * **5 Aug 2024** (red: VIX about 66 before the open).
  3. Objectives card: 12 items plus industry and frontier.
  4. House card: the rough lab.
- **Pause-and-predict.** "Zoom into a Brownian path 256 times. Does it look smoother or rougher?" (Smoother: the increments
  scale as Δ^½, so slopes blow up while the rescaled picture straightens. A rough path scales as Δ^0.1 and keeps its look.)
- **Compute.** None new (fBM drawn in-scene by `sim.fbm`).

### 1 · The fact: an exploding skew (3.0) · item 1 · `s02_fact` (deepened)
- **Goal.** The ATM skew term structure as a measured object, across two years and not one day; the power law and its
  bounded rival.
- **Beats.**
  1. **Visual (3D).** A `ThreeDScene` with x = log₁₀ T (2 days to 1 year), y = calendar week (102 Deribit weekly surfaces,
     January 2024 to December 2025) and z = log₁₀ |skew|. Each week's points appear as a ribbon, row by row, like a loom. Each
     row's fitted power-law line is drawn across it. Then the camera orbits to look down the y-axis, so all 102 lines stack
     into one fan, and a histogram of slopes rises on the side.
  2. Then the existing Dec-2025 plot (power law against bounded) as the "one day" close-up.
  3. Week of 7 Aug 2024 highlighted in red (the crisis week; ch14).
- **Derivation.** None here (ch2). One card with the definitions:
  $\psi(T) = |\partial_k\sigma_{\rm imp}(k,T)|_{k=0}$; power law $\psi = cT^{-a}$, with $a = \tfrac12 - H$ read as roughness;
  bounded $\psi = c(T+\varepsilon)^{-a}$ (Guyon–El Amrani).
- **Experiment.** `skew_weekly`, run *(probe)* on all 102 days:
  * the median exponent is **a = 0.45** (implied H ≈ 0.05); the interquartile range is 0.25–0.58, and 56% of weeks have a in
    [0.3, 0.7];
  * the bounded form improves the log fit by more than 0.01 on **25% of weeks**, with a median shift of **24 days**;
  * per-week log RMSE is about 0.6. That is noisier than the Dec-2025 build's 0.23: weekly days have fewer trades.

  **Implementation:** require ≥ 8 quotes per expiry and |k| < 0.3, and weight expiries by the number of trades.
  **Narration branches** on the final median and on the bounded-better share.
- **Pause-and-predict.** "If H = 0.1, by what factor is a 1-day skew steeper than a 1-month one?" (30^{0.4} ≈ 3.9.)
- **Compute.** `skew` (exists), `skew_weekly` (new; 8 CPU-min *(probe: 485 s for 102 days)*).

### 2 · Why a power law: the skew from the kernel (3.0) · item 1 · `s02a_skewmath` (new)
- **Goal.** Derive why a kernel K produces a skew ψ(T) ∝ (double integral of K)/T². Then:
  * exponential kernels give a flat skew at short T and 1/T at long T;
  * power-law kernels give T^{H−½};
  * Fukasawa's theorem: a power-law skew forces roughness.
- **Beats.**
  1. **Visual.** The triangle {0 < t < s < T} in the (t, s) plane, drawn as a 3D surface z = K(s − t) above it. A slider shrinks T.
     For an exponential kernel the surface over the triangle is nearly flat, so the volume ∝ T² and the skew is
     constant. For the power kernel it is a ridge that spikes along the diagonal, so the volume ∝ T^{H+3/2}. The camera looks along the
     diagonal. The volume is "poured" (fill opacity rising) and divided by T², drawn as a live point on a log–log skew plot.
  2. Then the computed skews of Part 13's Heston, a Merton jump model, rBergomi (fitted) and rough Heston (H = 0.1) on the same log–log
     axes against the market points.
- **Derivation** (ladder):
  - $\sigma^2_t = \xi_0(t)\,\mathcal E\big(\int_0^t K(t-s)\,dW_s\big)$, $d\langle \ln S, \xi^u\rangle_t = \rho\,\sigma_t\,\xi_t(u)\,K(u-t)\,dt$
    (a forward variance model; Itô).
  - $\psi(T) \approx \dfrac{\rho}{2\sigma_0^{3}T^{2}}\displaystyle\int_0^T\!\!\int_t^T \sigma_0\,\xi_0(u)\,K(u-t)\,du\,dt$
    (first order in vol of vol: the skew is the integrated spot–variance covariance; Bergomi–Guyon 2012). *Verify the
    normalisation against Bergomi ch. 8 or Friz–Gatheral (*Rough Volatility* ch. 9) before it goes on screen.*
  - $K(\tau) = \eta e^{-\kappa\tau}$: $\int_0^T\!\int_t^T e^{-\kappa(u-t)} = \frac{T}{\kappa}-\frac{1-e^{-\kappa T}}{\kappa^2}$, which is
    $\approx T^2/2$ for $T\ll 1/\kappa$ (flat skew) and $\approx T/\kappa$ for $T \gg 1/\kappa$ (skew $\propto 1/T$). Integrate.
  - $K(\tau) = \eta\tau^{H-\frac12}$: $\int_0^T\!\int_t^T (u-t)^{H-\frac12} = \frac{T^{H+3/2}}{(H+\frac12)(H+\frac32)}$, so
    $\psi \propto T^{H-\frac12}$ (integrate twice; Alòs–León–Vives 2007, Fukasawa 2011).
  - Fukasawa (2021): if $\psi(T)\sim cT^{H-\frac12}$ with $H<\frac12$ in a continuous model, volatility cannot have
    finite-variation or Brownian-smooth paths without admitting an arbitrage. "Volatility has to be rough" (theorem card;
    quoted, not proved).
  - Several exponentials at different κ give a power law over the range their time scales span (forward to ch10 and ch11).
- **Experiment.** `skew_models` (new): ATM skew against T from 2 days to 1 year for:
  * Heston (Part 13's fit);
  * Merton jumps (Part 13 parameters, COS);
  * rBergomi (from `rbskew`);
  * rough Heston at H = 0.1 (from `rprofile`);
  * a 2-factor exponential (κ = 50 and 2).

  Each has a fitted local slope on 2–14 days and on 60–365 days. **Narration states what the computed jump skew
  does** (no assertion about jump models without the number).
- **Pause-and-predict.** "Mean reversion κ = 2 a year. Over what range of expiries does Heston's skew look flat?" (T ≪ 1/κ:
  well under six months.)
- **Compute.** `skew_models` (< 1 min), `skew_kernel` (analytic, trivial).

### 3 · Volatility is rough, re-measured (3.0) · item 2 · `s03_rough` (deepened)
- **Goal.** The Gatheral–Jaisson–Rosenbaum estimator: why it works, what it reads, and its check on synthetic data.
- **Beats.**
  1. Keep the BTC/fBM/BM panels, but draw them **live** (`tracing`).
  2. **Lab 1**: `rough.log_rv_scaling` (rough.py lines 166–182, cut to 12 lines: the double loop over q and lags, the polyfit,
     and H from the regression of ζ on q). `lab_run` prints:
     * fBM checks 0.05 → 0.01, 0.1 → 0.09, 0.3 → 0.31, 0.5 → 0.50;
     * BTC 2024–25 H = 0.08 (de-seasonalized 0.12);
     * BTC 2018–2020 (1-minute data resampled to 5 minutes) H = 0.13 *(probe)*.
  3. **Live**: the m(q, Δ) dots appear lag by lag and the five fitted lines rotate into place. Then the ζ_q-against-q panel
     builds point by point.
  4. A two-era comparison bar: 2018–20 against 2024–25.
- **Derivation.**
  - $\log\sigma^2_{t+\Delta}-\log\sigma^2_t \overset{d}{=} \nu\,\Delta^{H} Z$ for fBM with Hurst $H$ (stationary self-similar
    increments).
  - $m(q,\Delta) = \mathbb E|\cdot|^q = \nu^q\Delta^{qH}\,\mathbb E|Z|^q$ (take the q-th moment), so $\log m = qH\log\Delta + c_q$:
    slopes $\zeta_q = qH$, linear in q (monofractal).
  - $\widehat{\sigma^2_t} = \sum_{i}r_{t,i}^2 = \int_t^{t+1}\sigma^2_s ds + \text{noise}$ (realized variance estimates the
    *integrated*, not the spot, variance; ch11 returns to this).
- **Pause-and-predict.** "If the q = 2 line had slope 1, what is H?" (½.)
- **Compute.** `roughness` (exists), `roughness_2018` (new; BTC 1m 2018–2020, < 1 min).

### 4 · Forecasting with a rough memory (2.6) · item 2 · `s03a_forecast` (new)
- **Goal.** GJR's practical payoff, the rough forecast formula, against HAR; and the distinction between rough (H < ½) and long
  memory (H > ½, Comte–Renault 1998).
- **Beats.**
  1. **Visual.** Today's log-variance forecast as a weighted sum of the past. A bar chart of weights over past days is drawn
     beneath the BTC log-RV series. A slider moves the forecast horizon Δ from 1 to 20 days, and the weights reshape (the
     power-law kernel 1/((j + Δ) j^{H+½}) flattening). Beside it, HAR's three-step staircase (1/5/22 days) for comparison.
     The forecast line is then drawn live across the test period.
  2. Card: Comte–Renault's long-memory SV (fractional integration, H > ½) explained long-range autocorrelation. GJR's
     point is the opposite end: rough short-scale behaviour with a slowly decaying kernel.
- **Derivation.**
  - $\log\sigma^2_t = \nu W^H_t + c$, with $W^H$ Mandelbrot–Van Ness (Part 5) (the RFSV model).
  - $\mathbb E[W^H_{t+\Delta}\mid\mathcal F_t] = \frac{\cos(H\pi)}{\pi}\Delta^{H+\frac12}\int_{-\infty}^t \frac{W^H_s}{(t-s+\Delta)(t-s)^{H+\frac12}}ds$
    (the conditional expectation of fBM given its past; Nuzman–Poor 2000, as used by GJR). *Check the constant against GJR
    (2018) §5 before it goes on screen.*
  - Discretised: weights $w_j\propto[(j+\Delta)j^{H+\frac12}]^{-1}$ normalised to one (the forecast is a weighted average).
- **Experiment.** `rfsv_forecast` (new): log-RV on BTC 2018–2020 (1,074 days *(probe)*) and 2024–25. RFSV (with the measured H)
  against HAR, AR(1) and last value, at Δ = 1, 5, 20, with a rolling origin and a 250-day kernel window.

  *Probe (single split, 500-day kernel window, too little training data):* Δ = 1 out-of-sample R² was **HAR 0.51, RFSV
  0.44, last value 0.38**. At 5 and 20 days the split was too short to be meaningful.

  **The narration must branch:** if HAR wins, say so. HAR is a three-step approximation of the same slowly decaying kernel
  (Corsi 2009; Part 7). Roughness explains why HAR works, not necessarily that RFSV beats it. Seeds are not applicable;
  show rolling-origin windows as a band.
- **Pause-and-predict.** "H = 0.1. Does the forecast weight on yesterday rise or fall as the horizon grows?" (It falls; the
  weights spread to the more distant past.)
- **Compute.** `rfsv_forecast` (1 min).

### 5 · Rough Bergomi (3.0) · item 3 · `s04_rbergomi` (deepened)
- **Goal.** The model, why it is a martingale with the market's variance curve built in, and its calibration *watched*.
- **Beats.**
  1. Keep the model ladder; add the proof.
  2. **Replay**: the least-squares calibration on the Surface, iterate by iterate. Right: the cost, from the stored `fun` at each
     evaluation. Left: the model smile at three expiries (7, 30 and 120 days) morphing onto the quotes, with the (H, η, ρ)
     readout ticking. 3 random-number seeds are drawn as a band.
  3. The out-of-sample re-price on fresh paths: 0.83 vol points, against Heston's 1.37.
  4. The skew term structure (existing `rbskew`).
  5. One line forward to Part 17, which calibrates this weekly with a network.
- **Derivation.**
  - $W^H_t = \sqrt{2H}\int_0^t(t-s)^{H-\frac12}dW_s$, so $\mathrm{Var}\,W^H_t = 2H\int_0^t (t-s)^{2H-1}ds = t^{2H}$ (the Itô
    isometry).
  - $\mathbb E\,e^{\eta W^H_t - \frac12\eta^2t^{2H}} = 1$, so $\mathbb E v_t = \xi_0(t)$ (Gaussian moment generating function): the
    variance curve is matched.
  - $\xi_s(t) = \mathbb E_s v_t = \xi_0(t)\exp\big(\eta\sqrt{2H}\int_0^s (t-u)^{H-\frac12}dW_u - \frac{\eta^2}{2}\int_0^s 2H(t-u)^{2H-1}du\big)$,
    an exponential martingale in s (condition on $\mathcal F_s$; the remaining part is independent and Gaussian).
  - Not Markov in $(S, v)$: the state is the whole curve $\xi_s(\cdot)$ (Bergomi's forward variance, Part 13).
- **Experiment.** `rbergomi` (exists), plus `rb_replay` (new): the same calibration with the trace recorded (wrap `resid`), at
  seeds 3, 4 and 5; the spread of fitted H across seeds is reported.
- **Pause-and-predict.** "Double η. What happens to E[v_t]?" (Nothing: the compensator −½η²t^{2H} keeps it at ξ₀(t).)
- **Compute.** `rbergomi` (exists), `rbskew` (exists), `rb_replay` (3 seeds × ~5 min = **15 min**, resumable per seed via
  `CACHE.partial`).

### 6 · Simulating a rough path: the hybrid scheme (2.6) · item 3 · `s04a_hybrid` (new)
- **Goal.** Why naive discretisation fails near the singular kernel, and how the hybrid scheme fixes it at O(n log n).
- **Beats.**
  1. **Visual.** The kernel (t − s)^{H−½} drawn over the last few cells before t: a spike to infinity at s = t. A naive
     left-point Riemann sum stacks bars under it and visibly misses the spike, shaded red. The hybrid scheme fills the first cell
     **exactly**, with a Gaussian pair, and replaces the far cells with bars at optimal points b_k (green).
  2. **Live**: the FFT convolution as the kernel sliding along the dW sequence, then 4 paths growing step by step.
  3. **Lab 2**: `rough.rbergomi_paths`, lines 29–44, cut to 12 lines (the 2×2 covariance and Cholesky, the `_b` weights, and
     the FFT convolution). `lab_run` prints the variance check.
- **Derivation.**
  - Cell 1: $\big(\Delta W_i,\ \int_{t_i}^{t_{i+1}}(t_{i+1}-s)^{H-\frac12}dW_s\big)$ is Gaussian with covariance
    $\begin{psmallmatrix}\Delta & \frac{\Delta^{H+1/2}}{H+1/2}\\ \cdot & \frac{\Delta^{2H}}{2H}\end{psmallmatrix}$ (Itô isometry
    on one cell).
  - Cells k ≥ 2: $(t-s)^{H-\frac12}\approx (b_k\Delta)^{H-\frac12}$ with
    $b_k = \big(\frac{k^{H+1/2}-(k-1)^{H+1/2}}{H+1/2}\big)^{1/(H-1/2)}$ (choose the point that matches the cell's integral of the
    kernel: mean-square optimal).
  - The sum over k is a causal convolution, computed by FFT in O(n log n), against O(n³) for an exact Cholesky of the
    n × n covariance.
- **Experiment.** `hybrid_check` (new): Var W^H_1 by hybrid, left-point Riemann and exact Cholesky; 20,000 paths, n = 100,
  for H ∈ {0.05, 0.1, 0.3}. *Probe:*

  | H | hybrid | left-point Riemann | exact |
  |---|---|---|---|
  | 0.05 | **1.03** | **0.40** | 1.00 |
  | 0.1 | 1.03 | 0.64 | 1.00 |
  | 0.3 | 1.01 | 0.95 | 1.00 |

  Also the timing of hybrid against Cholesky for n = 250, 500, 1,000, and the rBergomi ATM 30-day implied vol under both schemes
  (the bias in price).
- **Pause-and-predict.** "Which scheme's error grows as H falls?" (Riemann: the spike carries more of the variance.)
- **Compute.** `hybrid_check` (1 min).

### 7 · Rough Heston: the Volterra equation and its Riccati (3.0) · item 4 · `s05_rheston` (deepened)
- **Goal.** Derive the characteristic function from the affine Volterra structure, not quote it; the fit, with its
  surprise.
- **Beats.**
  1. **Visual.** Heston's variance written as "today's value plus memory of all past pushes". The memory kernel morphs from a
     constant (Heston, H = ½) into the power law (H = 0.1), and a simulated variance path re-drawn with each kernel
     (lifted simulation, N = 20, live) turns jagged.
  2. Then the ladder.
  3. Then the existing free fit against held-H table, and the skew term structure.
- **Derivation.**
  - $V_t = V_0 + \frac{1}{\Gamma(\alpha)}\int_0^t(t-s)^{\alpha-1}\big[\lambda(\theta-V_s)ds + \nu\sqrt{V_s}\,dW_s\big]$, with $\alpha = H+\frac12$
    (Heston, with the kernel 1 replaced by the fractional kernel).
  - Affine Volterra: $\log\mathbb E e^{iuX_T} = \int_0^T F(u,h(T-s))\,g_0(s)\,ds$, where $g_0(t) = V_0 + \lambda\theta\int_0^t K$ (the
    Abi Jaber–Larsson–Pulido affine transform; *Rough Volatility* ch. 5).
  - $h = K * F(u,h)$, i.e. $D^\alpha h = F(u,h) = -\frac12(u^2+iu) + (i\rho\nu u-\lambda)h + \frac12\nu^2h^2$ (convolution with the
    fractional kernel is the fractional integral, whose inverse is $D^\alpha$).
  - $\phi(u) = \exp\big(\theta\lambda\,I^1h(T) + V_0\,I^{1-\alpha}h(T)\big)$ (substitute $g_0$; El Euch–Rosenbaum 2019).
  - At α = 1, $D^1h = h'$: Heston's Riccati equation (the consistency check the House tests).
- **Experiment.** `rheston`, `rprofile` (exist). The free fit drifts back to H = 0.45 with ν = 4.5 (error 1.28); held at 0.1 the
  error is 1.49, with ν = 1.0. The narration keeps its existing honest reading.
- **Pause-and-predict.** "Set H = ½ in the fractional Riccati equation. What do you get?" (Heston's Riccati ODE.)
- **Compute.** exists.

### 8 · Solving it: the fractional Adams scheme, and the H profile (3.0) · item 4 · `s05a_adams` (new)
- **Goal.** How a fractional ODE is solved, its convergence measured, and how much the Surface cares about H.
- **Beats.**
  1. **Lab 3**: `rough.frac_riccati`, lines 68–82 (the predictor weights `bw`, corrector weights `aw`, the update). `lab_run`
     prints the convergence table.
  2. **Live**: the solution h(t) for u = 1…10 grows along t, with the predictor (dashed) and corrector (solid) at each step. The
     memory sum is drawn as a fan of arrows from all past grid points into the new point (every point is pulled by the whole
     past, unlike an ODE).
  3. **Visual (3D)**: |φ(u, T)| as a surface over (u, T), for H = 0.5 morphing into H = 0.1. The camera orbits, and the short-T
     ridge decays faster in u for the rough model (fatter short-dated tails, a steeper short skew).
  4. **Replay of the H profile**: refit the other five parameters at H on a grid of 9 values from 0.05 to 0.5. The vega-weighted error
     curve is drawn point by point, with the free optimum (0.45) and the time-series H (0.08–0.12) marked. A side panel shows the
     error by expiry (short against long) at each H: where roughness is paid for or rewarded.
- **Derivation.**
  - $h(t_{k+1}) = \frac{\Delta^\alpha}{\Gamma(\alpha+2)}\big[F(h^P_{k+1}) + \sum_{j\le k}a_{j,k+1}F(h_j)\big]$, with predictor
    $h^P_{k+1} = \frac{\Delta^\alpha}{\Gamma(\alpha+1)}\sum_j\big((k+1-j)^\alpha-(k-j)^\alpha\big)F(h_j)$ (product-trapezoid and
    product-rectangle rules on the Volterra form; Diethelm et al.).
  - Cost O(n²) for n steps, against O(n) for an ODE (the memory sum).
- **Experiment.** `adams_conv` (new). *Probe* at u ∈ [0.5, 15], T = 30 days, H = 0.1:

  | n | 25 | 50 | 100 | 200 | 400 | 800 |
  |---|---|---|---|---|---|---|
  | max error | 1.8e-3 | 5.4e-4 | 1.7e-4 | 5.2e-5 | 1.5e-5 | 3.8e-6 |
  | seconds | 0.02 | — | 0.03 | 0.04 | 0.08 | 0.19 |

  So the observed order is ≈ 1.7. At H = ½ the scheme agrees with Heston's closed form to **7e-7** (n = 200).

  `rh_profile9` (new): 9 values of H × 25 function evaluations. Reuse `rprofile` for 0.05, 0.1 and 0.2.
- **Pause-and-predict.** "Double the Adams steps. Error shrinks by?" (About 3.2×: order 1.7.)
- **Compute.** `adams_conv` (0.2 min), `rh_profile9` (~15 min).

### 9 · Where roughness comes from: nearly unstable order flow (3.0) · item 5 · `s06_hawkes` (deepened)
- **Goal.** From reactive order flow to rough Heston: the argument, the branching structure, and what simulation can and
  cannot show.
- **Beats.**
  1. Keep the three activity panels (n = 0.5/0.9/0.99), now **live**: the bins fill as events arrive.
  2. **Visual**: the family tree. Immigrants on the axis, children hanging below on power-law delays; at n → 1 the trees become
     enormous and span all scales. A zoom-out (ValueTracker on the time window) shows the counting process of a near-critical
     Hawkes turning into a jagged rough curve.
  3. **Computed**: the GJR estimator applied to the log activity as n sweeps 0.5 → 0.9999.
  4. Card: El Euch–Fukasawa–Rosenbaum. At high frequency, no-arbitrage plus buy/sell asymmetry of the kernels forces the
     leverage effect (ρ < 0) in the limit. Jusselin–Rosenbaum (*Rough Volatility* ch. 3): no-arbitrage implies power-law
     impact and rough volatility (forward to Part 37).
- **Derivation.**
  - $\lambda_t = \mu + \int_0^t\phi(t-s)dN_s$, so $\mathbb E\lambda_t = \mu + \int_0^t\phi(t-s)\mathbb E\lambda_s ds$ (take
    expectations; $dN - \lambda dt$ is a martingale).
  - $\mathbb E\lambda_t = \mu\big(1 + \int_0^t\psi\big)$, with $\psi = \sum_{k\ge1}\phi^{*k}$ (the renewal equation solved by its
    resolvent; generations of the family tree).
  - With $\|\phi\|_1 = n_T\to1$ and $\phi(t)\sim t^{-(1+\alpha)}$, the rescaled resolvent converges to the Mittag-Leffler density
    $t^{\alpha-1}E_{\alpha,\alpha}(-\lambda t^\alpha)$, and its small-t behaviour $t^{\alpha-1}$ is the rough Heston kernel (Laplace
    transforms; heavy tail ⇒ $1-\hat\phi(z)\approx c z^\alpha$).
  - Limit: the rescaled intensity solves rough Heston's Volterra equation with $H = \alpha - \frac12$ (Jaisson–Rosenbaum 2016;
    theorem card).
- **Experiment.** `hawkes_sweep` (new): power-law (Lomax) kernel, simulated by **branching** (generation by generation,
  vectorised; 3–4 million events in about 1 s). GJR H on log activity in fixed bins, 3 seeds. *Probe:*

  | branching ratio n | 0.5 | 0.9 | 0.999 | 0.9999 |
  |---|---|---|---|---|
  | estimated H (α = 0.6) | −0.005 | 0.016 | 0.135 | 0.108 |

  Across α ∈ {0.6, 0.75, 0.9} at n = 0.9999 the estimates are 0.09–0.11. **The finite sample shows roughness emerging near criticality,
  but does not recover H = α − ½.** The narration says exactly that: the limit theorem needs n → 1 and T → ∞
  together. A Fano-factor variant did not separate α either *(probe)*.
- **Pause-and-predict.** "Branching ratio 0.99. What share of trades are reactions to earlier trades?" (99%; the mean
  cluster holds 100 events.)
- **Compute.** `hawkes` (exists), `hawkes_sweep` (1 min). The new House function `sim.hawkes_branching_powerlaw` gets a test:
  mean count = μT/(1 − n).

### 10 · Markovian lifts (2.6) · item 6 · `s07_lift` (deepened)
- **Goal.** Derive the exponential-mixture identity; build the lifted Heston; see convergence in N.
- **Beats.**
  1. Keep the kernel/exponentials figure, but animate N growing 1 → 50 under a ValueTracker. Each new exponential appears
     as a thin coloured curve that adds into the sum, and the sum crawls up the power law decade by decade.
  2. Then **live**: one variance path driven by the same Brownian increments under N = 1, 5, 20 and the exact hybrid
     simulation, converging.
  3. Keep the 30-day smile error table (4.70 → 0.26).
  4. Card: Bayer–Breneis (2023), Gaussian-quadrature nodes, superpolynomial convergence in N. Abi Jaber (2019), the lifted
     Heston as a practical model with N = 20 and a single parameter r_N.
- **Derivation.**
  - $\int_0^\infty e^{-xt}x^{-\alpha}dx = \Gamma(1-\alpha)\,t^{\alpha-1}$ (substitute $y = xt$).
  - So $\frac{t^{\alpha-1}}{\Gamma(\alpha)} = \int_0^\infty e^{-xt}\mu(dx)$, with $\mu(dx) = \frac{x^{-\alpha}dx}{\Gamma(\alpha)\Gamma(1-\alpha)}$
    (divide by $\Gamma(\alpha)\Gamma(1-\alpha)$; Bernstein: completely monotone).
  - Quantise μ on geometric nodes $x_i$ with weights $c_i$: $K\approx\sum c_ie^{-x_it}$, so $V_t = g_0(t) + \sum_i c_iU^i_t$ with
    $dU^i = -x_iU^i dt + \lambda(\theta - V)dt + \nu\sqrt V dW$ (each exponential is one OU-like factor; Markov in N + 1
    dimensions).
- **Experiment.** `lift` (exists). `lift_paths` (new): pathwise L² distance from lifted to hybrid V for N = 1, 5, 20, 50.
- **Pause-and-predict.** "How many exponentials to cover lags from one minute to one year at one per decade?" (About 6:
  scale invariance needs one per decade, ~log₁₀ 525,600.)
- **Compute.** `lift` (exists), `lift_paths` (0.5 min).

### 11 · The debate I: is the time series fooling us? (3.0) · item 7 · `s08_debate` (deepened)
- **Goal.** The estimator's identification problem made visible, and what the statistics literature says.
- **Beats.**
  1. Keep the weekend trap (0.08 → 0.12) and the three smooth models (0.38, 0.42, 0.02).
  2. **Visual (3D), the new centrepiece**: the **bias map**. On the floor:
     * x = the true H, from 0.05 to 0.5;
     * y = the mean-reversion half-life of a fractional OU, from none down to 5 hours (log scale).

     The surface z = the GJR estimate from simulated 5-minute RV over 700 days. The camera orbits; then a horizontal plane at
     BTC's measured 0.08–0.12 slices the surface. The intersection curve (gold) is every (H, half-life) pair that would show
     Bitcoin's number. It runs from (H = 0.1, no mean reversion) to (H = 0.5, half-life ≈ 1 day). One number cannot choose.
  3. Then what can:
     * curvature of log m(q, Δ) in log Δ (straight for rough, bending for fast mean reversion);
     * sub-daily lags;
     * the options (ch12).
  4. Statistical cards:
     * Fukasawa–Takabatake–Westphal (2022): a consistent Whittle-type estimator under measurement error;
     * Bolko–Christensen–Pakkanen–Veliyev (2023): GMM, correcting the "illusive roughness" from RV error, still H ≈ 0.05;
     * Chong–Hoffmann–Liu–Rosenbaum–Szymanski (2024): the best possible rate for H from n prices is $n^{-1/(4H+2)}$, slow;
     * Cont–Das (2024).
- **Derivation.**
  - $\widehat{RV}_t = \int_t^{t+1}\sigma^2_sds + \varepsilon_t$ (integrated plus measurement error).
  - The error is i.i.d., so $\mathbb E|\Delta\log\widehat{RV}|^q$ gains a lag-independent floor; the fitted slope falls, and so does
    $\hat H$ (a flat additive term at all lags lowers the slope).
  - fOU with rate κ: $\mathrm{Var}(X_{t+\Delta}-X_t)\approx\nu^2\Delta^{2H}$ for $\Delta\ll1/\kappa$, but $\to 2\mathrm{Var}X$ (flat) for
    $\Delta\gg1/\kappa$. If 1/κ is below one day, every daily lag sits on the flat part, so $\hat H\approx0$ (stationarity).
  - Minimax: $\inf_{\hat H}\sup\mathbb E|\hat H-H|\asymp n^{-1/(4H+2)}$ (Chong et al. 2024; quoted).
- **Experiment.** `bias_map` (new): fOU by Davies–Harte fBM increments and an AR(1) filter (`scipy.signal.lfilter`), 5-minute
  grid, 700 days. Scale the log-vol so the sd of daily changes = 0.3; vol = 0.5·e^x; returns, RV, and both the integrated and
  measured estimates. An 8 × 8 grid × 4 seeds. *Probe (5 × 5 × 2 seeds, 7 s), estimated H from RV:*

  | true H | no mean reversion | half-life 30 d | 5 d | 1 d | 5 h |
  |---|---|---|---|---|---|
  | 0.05 | 0.16 | 0.16 | 0.09 | 0.007 | −0.007 |
  | 0.1 | 0.20 | 0.19 | 0.11 | 0.014 | −0.017 |
  | 0.3 | 0.34 | 0.32 | 0.19 | 0.05 | −0.007 |
  | 0.5 | 0.50 | 0.45 | 0.29 | **0.095** | 0.015 |

  Note the **upward** bias at very small H, from daily integration smoothing the spot path (0.05 reads 0.16). This is the
  opposite sign to the fBM-direct check of ch3 (0.05 → 0.01). The narration must explain both:
  * integration smooths, which pushes the estimate up;
  * mean reversion and noise flatten, which push it down.

  Add a `straightness` statistic: the residual of the log–log fit, per cell.
- **Pause-and-predict.** "A perfectly smooth volatility with a one-day half-life: what H does the estimator report?" (About
  0.1, Bitcoin's number *(probe 0.095)*.)
- **Compute.** `artefact` (exists), `bias_map` (2 min).

### 12 · The debate II: what the options say (2.6) · item 7 · `s08a_options` (new)
- **Goal.** The options-side evidence for and against rough models, measured on our two years of weekly surfaces and taken from the published horse races.
- **Beats.**
  1. **Visual**: the 102 weekly skew fans from ch1 reappear. Each week's power-law and bounded fits are drawn, and the weeks where
     the bounded form wins by > 0.01 flash gold (25% *(probe)*). A dial shows the distribution of the bounded fit's shift ε
     (median 24 days *(probe)*).
  2. Then the horse-race board, cards with results as reported:
     * Livieri–Mouti–Pallavicini–Rosenbaum (2018): H from options;
     * Rømer (2022): one-factor rBergomi and rough Heston miss the SPX term-structure effect over 2004–2019, and a two-factor OU
       model fits SPX almost perfectly and SPX–VIX decently;
     * Guyon–El Amrani (2023): 2020–21 SPX, SX5E and DAX, where a two-parameter power law fails once short maturities are
       included;
     * Abi Jaber–Li (2025): rough models underperform one-factor Markovian ones from 1 week to 3 months, and a path-dependent and
       a two-factor Markovian model with 3–4 parameters win from 1 week to 3 years.
  3. Our own board: the Surface errors from ch5 and ch7 (rBergomi 0.83, Heston 1.37, rough Heston free 1.28, at 0.1 1.49), plus a
     **two-factor Bergomi** fit to the same 175 quotes (new; the Abi Jaber–Li-style comparison on our data). Narration
     branches on whether 2-factor beats rBergomi.
- **Derivation.** A two-factor Bergomi kernel $K(\tau) = \eta_1e^{-\kappa_1\tau}+\eta_2e^{-\kappa_2\tau}$ gives
  $\psi\propto\sum_i\eta_i\big(\frac{1}{\kappa_iT}-\frac{1-e^{-\kappa_iT}}{\kappa_i^2T^2}\big)$ (ch2's formula, term by term), which on
  [1 week, 1 year] can mimic $T^{-0.4}$ with κ₁ ≈ 50 and κ₂ ≈ 1 (the same "several time scales" as ch10).
- **Experiment.** `skew_weekly` (shared). `bergomi2f` (new): 2-factor Bergomi Monte Carlo with Part 13's ξ₀, common random
  numbers, 20,000 paths. Calibrate (κ₁, κ₂, η₁, η₂, ρ), with the stored trace replayed briefly. Re-price on fresh paths.
- **Pause-and-predict.** "A two-factor model with half-lives of 5 days and 1 year. Can it fake a power-law skew from 1 week to 6
  months?" (Yes, approximately; ch2's sum.)
- **Compute.** `bergomi2f` (~10 min).

### 13 · Volatility is (mostly) path-dependent (3.0) · item 8 · `s09_pdv` (deepened)
- **Goal.** Guyon–Lekeufack's model, fitted and watched learning; the 4-factor Markovian form.
- **Beats.**
  1. Keep the ladder.
  2. **Visual, live**: two weighted "memories" of the BTC return path fill as the path is drawn: a trend bar R₁ (signed) and an
     activity bar √R₂ (always up). The kernel weights appear as a glowing trail behind the moving date. Implied vol is
     rebuilt from them in real time against DVOL.
  3. **Replay**: the least-squares fit of the kernel shapes (α₁, δ₁, α₂, δ₂). Right: the cost. Left: the two kernels morphing
     from the start values to the fit, with R² in sample as a readout. Then the out-of-sample split (0.42 against −0.27).
  4. **The 4-factor Markovian PDV (4FMPDV)**: each kernel as a convex combination of two exponentials, so R₁ and R₂ each have
     two Markov factors updated by one line each. **Lab 4**: the new `rough.pdv4_step` (8 lines). Fit; compare R² with the
     TSPL form.
  5. Card: Nutz–Riveros Valdevenito (2024), the 4-PDV SDE is well posed; Andrès–Jourdain (2024).
- **Derivation.**
  - $\sigma_t = \beta_0+\beta_1R_{1,t}+\beta_2\sqrt{R_{2,t}}$, $R_{n,t} = \int_{-\infty}^tK_n(t-u)\,(dS_u/S_u)^n$ (definition).
  - $K(\tau) = (1-\theta)\lambda_0e^{-\lambda_0\tau}+\theta\lambda_1e^{-\lambda_1\tau}$ ⇒ $R = (1-\theta)R^{(0)}+\theta R^{(1)}$, with
    $dR^{(j)} = \lambda_j(r_t^n - R^{(j)})dt$ (a convex mixture of exponentials, each an exponential moving average: Markov).
  - The fit: $\beta$ by OLS inside, the kernel shapes by nonlinear least squares (variable projection; why the replay has only
    4 dimensions).
- **Experiment.** `pdv` (exists), `pdv_replay` (new: stored iterates, < 1 min), `pdv4` (new: 4FMPDV on BTC/DVOL, < 2 min).
- **Pause-and-predict.** "For bitcoin, does it matter which way the price moved?" (Hardly: the trend term moves DVOL by 0.9
  points (one sd), the activity term by 19.)
- **Compute.** ~3 min.

### 14 · PDV on the S&P 500, and 5 August 2024 (3.0) · item 8 · crisis · `s09a_spx` (new)
- **Goal.** Replicate Guyon–Lekeufack where they did it, on the VIX; then the crisis day where path-dependence explains
  bitcoin's volatility and not the VIX.
- **Beats.**
  1. **Live**: the VIX 2000–2025 drawn, with the PDV prediction from market returns only tracing it, and the train/test split
     at 2019.
  2. The trend term matters here: β₁ ≈ −2.1 *(probe)*. Falls raise volatility, which is the leverage effect and the Zumbach effect's
     raw material (ch15).
  3. **Crisis file: 5 August 2024**, `crisis_card`:
     * the VIX closed at 38.57 (FRED VIXCLS), from 23.39 on 2 August;
     * the PDV, fed only past returns, says **25.4** *(probe)*; the gap is about 13 points;
     * before the open the index printed about 66 (BIS Bulletin 95: "around 66"; SEC DERA staff paper: "over 65"), with the
       widening of OTM put bid–ask spreads lifting the mid-quotes the VIX is computed from (BIS 95, Todorov and Vilkov, 29 Oct 2024);
     * BIS Bulletin 90 (27 Aug 2024): the VIX rise "far exceeded" what its historical relation with S&P 500 returns implied;
       our PDV gap is that statement, computed;
     * the same hours on Deribit: DVOL's hourly high was **92.7** on 5 Aug (from 51 on 2 Aug), but its daily close of 63 was
       predicted by the BTC PDV at 61 *(probe)*. Bitcoin really moved: 5-minute RV annualised **219%** that day. The VIX's
       spike was a quote phenomenon, bitcoin's a price phenomenon.
  4. Context, in one line: Volmageddon (5 Feb 2018) as a second check, VIX 37.3 against PDV 24.2 *(probe)*. Link to Part 12.
- **Derivation.** Residual decomposition $\sigma^{\rm imp}_t - \hat\sigma^{\rm PDV}_t$ = everything not explained by the path:
  risk-premium shocks, liquidity, quotes. A one-line card, since PDV is a regression on the path.
- **Experiment.** `pdv_spx` (new): Ken French daily market return (Mkt−RF + RF; CRSP value-weighted as an S&P proxy, labelled)
  1986–2025 and FRED VIXCLS 1990–2025, train 2000–2018, test 2019–2025, dt = 1/252, lookback 1,000. *Probe:*
  * **R² 0.94 in sample, 0.85 out of sample**, against a 21-day-RV baseline's 0.81 and 0.56;
  * kernels: α₁ = 1.01 (at the lower bound), δ₁ = 0.021; α₂ = 1.55, δ₂ = 0.049;
  * β = (0.055, −2.11, 0.87); the trend term's one-sd contribution is 2.4 points and activity's 6.4.

  The implementation must check α₁ at the bound (widen it, or report). `crisis_aug2024` (new):
  * VIXCLS around 5 Aug;
  * DVOL hourly 1–9 Aug 2024 (cached);
  * BTC 5-minute RV by day (cached);
  * both PDV predictions;
  * the Deribit surface of 7 Aug 2024 against 31 Jul 2024 (ATM skew term structures).
- **Pause-and-predict.** "The S&P falls 3% in a day. Which term moves the PDV forecast more, trend or activity?" (Both; trend
  carries the sign.)
- **Compute.** `pdv_spx` (1 min), `crisis_aug2024` (0.5 min). **Data:** `data.fred("VIXCLS", "1990-01-01", "2025-12-31")`
  adds one manifest entry through the data layer (the CSV is already cached to 2025-12-31). Ken French daily through
  2025-12-31 is already in the manifest.

### 15 · Joint SPX/VIX: quadratic rough Heston and Guyon's puzzle (3.0) · items 9–10 · `s09b_joint` (new)
- **Goal.** Why fitting the S&P and VIX smiles together is hard; two answers: a rough model with feedback, and an exact
  non-parametric construction.
- **Beats.**
  1. Recap of Part 13's puzzle in one picture. The VIX smile is upward sloping; continuous models that fit the SPX skew make
     VIX vol of vol too low.
  2. **Quadratic rough Heston**: variance as a parabola of a rough weighted return. **Live**: a simulated path where a
     sharp fall *or* rally sends Z away from b and V up the parabola (the parabola drawn at the side, with a dot riding it).
  3. **Computed Zumbach effect**: past squared trends predict future vol better than the reverse (time-reversal
     asymmetry), measured on qRH paths and on the S&P (French market). Bars: forward against backward correlation.
  4. **Guyon's DMSP**: the convex-ordering picture. The SPX smiles at T₁ and T₂ bound what the VIX at T₁ can be; Guyon (2020)
     showed the joint calibration is possible, and his DMSP (2024) builds the exact joint fit, the entropy-closest martingale to a
     reference model satisfying all three smiles. **Lab 5**: `arbitrage.entropic_mot` (Part 9's House code, 12 lines of the
     Sinkhorn-with-martingale step) run on BTC 30- and 60-day marginals from the Surface. Cost: |log(S₂/S₁)| (a forward-start
     absolute return, ≈ √(2/π)·forward vol). sign = ±1 gives the lowest and highest values any martingale coupling of the two
     smiles allows. **Replay**: the Sinkhorn trace (marginal and martingale errors falling to 1e-6), and the bounds closing.
     rBergomi's value is drawn inside the interval. Label: illustration of the principle, not Guyon's full three-marginal
     algorithm.
- **Derivation.**
  - qRH: $Z_t = \int_0^tK(t-s)\lambda(\theta_0(s)-Z_s)ds + \int_0^tK(t-s)\eta\sqrt{V_s}dW_s$, $V_t = a(Z_t-b)^2+c$, $dS/S = \sqrt{V}dW$
    (Gatheral–Jusselin–Rosenbaum 2020).
  - $Z$ is a rough weighted average of past returns, so $V$ is high after a big move either way (the parabola), and the convexity
    makes vol of vol state-dependent (the VIX smile slopes up).
  - $\mathrm{VIX}^2_T = \mathbb E_T\big[\frac{1}{\tau}\int_T^{T+\tau}V_sds\big] = \mathbb E_T\big[-\frac2\tau\log\frac{S_{T+\tau}}{S_T}\big]$ (Part 12's
    log-contract, conditionally).
  - Jensen: $\mathbb E[\mathrm{VIX}_T]\le\sqrt{\mathbb E\,\mathrm{VIX}^2_T}$, and the right side is fixed by the SPX smiles (the forward
    variance swap). So the VIX future is bounded by the SPX smiles. The puzzle is that models that fit SPX produce VIX
    distributions too narrow to match VIX options (Guyon 2020).
  - DMSP: $\min_{\mathbb Q}H(\mathbb Q\mid\mathbb P)$ subject to $S_{T_1}\sim\mu_1$, $S_{T_2}\sim\mu_2$, $\mathrm{VIX}_{T_1}\sim\nu$,
    the martingale condition and the VIX constraint. The dual is a Sinkhorn-like iteration with potentials for each marginal and
    for each conditional constraint (Lagrange; Guyon 2024).
- **Experiment.** `qrh_sim` (new): the lifted kernel (N = 10), Euler, 10,000 paths, 1 year of daily steps; GJR-style
  parameters *(take a, b, c, λ, η, H from Gatheral–Jusselin–Rosenbaum 2020's reported fit: verify)*. Measure the Zumbach
  asymmetry. Stretch: the 1-month VIX smile by nested MC (2,000 × 500; ~5 min).

  `zumbach_spx` (new): the same statistic on French daily returns (< 0.1 min).

  `joint_bounds` (new): entropic MOT on a 60 × 80 grid, ε = 0.01, 500 iterations, both signs. The rBergomi value of the same
  claim comes from `rbergomi` paths.

  **Narration branches**: if the qRH asymmetry or the S&P asymmetry is not positive, it says so.
- **Pause-and-predict.** "In qRH, does a sharp rally raise or lower volatility?" (Raise: the parabola.)
- **Compute.** `qrh_sim` (2–7 min), `zumbach_spx` (< 0.1), `joint_bounds` (2 min).

### 16 · Signature volatility models (2.6) · item 11 · `s09c_signature` (new)
- **Goal.** Volatility as a linear function of the signature of a driving path; calibration that becomes almost a
  regression; fitted to the Surface.
- **Beats.**
  1. **Visual**: the time-augmented driving path (t, W_t) drawn in the plane. Its signature terms up to depth 3 (15 of them)
     light up as small growing bars as the path unrolls (Part 5's Chen loop). Then σ_t = Σ ℓ_i Ŝ_i(t) is drawn as the
     weighted sum of those bar heights, a volatility path built from the signature.
  2. **Lab 6**: `rough.sigvol_logS` (new, 10 lines), the trick: given precomputed per-path vectors A and matrices B, any ℓ
     prices in microseconds.
  3. **Replay**: least-squares calibration of (ℓ, ρ) to the 175 quotes. The cost falls, and the model smiles at three expiries
     morph onto the quotes; 3 path seeds as a band.
  4. Compare with rBergomi (0.83) and the two-factor Bergomi (ch12); the narration branches.
  5. Card: Cuchiero–Gazzani–Svaluto-Ferro (2023) do this with a polynomial-process driver and jointly fit SPX/VIX
     (Cuchiero–Gazzani–Möller–Svaluto-Ferro 2025, *Math. Finance*: in Part 5's plan).
- **Derivation.**
  - $\sigma_t = \langle\ell,\widehat{\mathbb X}_{0,t}\rangle$, with $\widehat{\mathbb X}$ the signature of $(t,W_t)$ truncated at depth 3
    (definition: linear in ℓ).
  - $\log S_T = \int_0^T\sigma_tdZ_t - \frac12\int_0^T\sigma_t^2dt = \ell^\top A - \frac12\ell^\top B\ell$, with
    $A = \int\widehat{\mathbb X}dZ$ and $B = \int\widehat{\mathbb X}\widehat{\mathbb X}^\top dt$ (σ is linear in ℓ: the stochastic
    integral is linear, the quadratic variation quadratic).
  - $Z = \rho W+\sqrt{1-\rho^2}B^\perp$ ⇒ $A = \rho A^W+\sqrt{1-\rho^2}A^\perp$ (store both, so ρ is free too).
  - Universality: linear functionals of signatures approximate continuous path functionals on compacts (Stone–Weierstrass;
    Part 5), so any (reasonable) path-dependent volatility is reachable as depth grows.
- **Experiment.** `sigvol` (new): 20,000 paths × 2 seeds, 200 daily steps (to 200 days), A and B stored at the quoted expiries
  (~10 expiries × 20,000 × (15 + 225) floats ≈ 400 MB, so **store in float32 per expiry, or reduce to 10,000 paths**). The
  signature is built by incremental Chen updates vectorised over paths. Least squares on (ℓ, ρ) with the trace stored;
  re-price on the fresh seed.
- **Pause-and-predict.** "Depth 1 only: what kind of volatility model is σ = ℓ₀ + ℓ₁t + ℓ₂W_t?" (A Bachelier-type vol linear in
  the driver, i.e. Stein–Stein-like.)
- **Compute.** `sigvol` (~10 min).

### 17 · What desks use, and why: industry, and the rough lab (2.8) · item 12 · `s11_house` (deepened)
- **Goal.** The production constraint (speed), how rough models reach desks, and the House's adoption rule.
- **Beats.** Cards with sources; one live object:
  1. **Speed is the gate.** A race bar chart of calibration time on this machine, all computed:
     * rBergomi by MC least squares (minutes);
     * rough Heston by Adams+COS (seconds);
     * lifted Heston N = 20 (sub-second);
     * Part 17's neural calibrator (milliseconds).
  2. **The neural surrogate lineage.** Bayer–Stemper (2018, arXiv 1810.03399), then Horvath–Muguruza–Tomas (*QF* 21(1):11–27,
     2021: "calibration within a few milliseconds for the full implied volatility surface"; Risk's Rising Star award, Feb
     2020), then Rosenbaum–Zhang (Risk 2022: deep calibration of qRH, SPX and VIX jointly in real time, as reported by
     Risk.net). Forward link to Part 17 (`s03_calib`, `s04_roughhist`).
  3. **The recognition.** Risk Awards 2021: Jim Gatheral and Mathieu Rosenbaum, Quants of the Year, citing the qRH joint
     calibration paper. Gatheral is quoted: rough volatility "has finally found acceptance" and "people are actually using it
     in practice" (as reported by Risk.net). The sceptic's award: Sigurd Emil Rømer, Risk's Rising Star (2022 *(verify
     year)*), whose work finds two-factor Markov models fit SPX better.
  4. **Why the short end became a business.** Cboe launched VIX1D (1-day volatility index) on 24 Apr 2023, computed from SPXW
     quotes, as zero-days-to-expiry options reached nearly half of S&P 500 option volume (as reported by Reuters). At those
     expiries ch1's power law is the whole question.
  5. **Hedging under rough volatility**: hedge with the forward variance curve (variance swaps) as instruments, not a spot vol
     state (Fukasawa–Horvath–Tankov, *Rough Volatility* ch. 6; card).
  6. **The rough lab** (existing content, expanded):
     * the House's new functions (`hybrid`, `frac_riccati`, `lifted_heston_cf`, `log_rv_scaling`, `fit_pdv`, `pdv4_step`,
       `sigvol_logS`, `qrh_paths`, `hawkes_branching_powerlaw`);
     * **Rule 14** (adopt only if it beats the simpler model out of sample on its quantity, with the estimator checked on
       synthetic data), now applied to the part's scoreboard:
       * the Surface: rBergomi, 2-factor Bergomi, sigvol;
       * forecasting: RFSV against HAR;
       * implied-vol tracking: PDV against the baseline.

     The board marks the winner of each row from the computed numbers.
  7. Trial counter (unchanged: no strategy tested).
- **Experiment.** `calib_speed` (new: wall time of one calibration evaluation per method; < 2 min). The numbers are
  machine-dependent, so they are shown with "this machine" and as ratios.
- **Pause-and-predict.** "A desk recalibrates every 5 seconds. Which of these four can it run?" (Lift or surrogate.)
- **Compute.** `calib_speed` (2), `envelope` (exists).

### 18 · Frontier, 2023–2026 (3.0) · `s10_frontier` (rewritten)
- **Goal.** Where the field is now, with one result from each line computed or shown.
- **Beats**: a timeline ribbon 2023 → 2026, each card dropping onto it:
  - Abi Jaber–Li (2025, *Math. Finance* 35(4)): rough models lose to Markovian/PDV ones on SPX 2011–2022 smiles (our
    ch12 board echoes it).
  - Chong et al. (2024, *AoS*; *AAP*): estimation theory for H; minimax rate (ch11).
  - Bolko et al. (2023, *J. Econometrics*): H ≈ 0.05 after correcting the RV error.
  - Cont–Das (2024): the artefact (ch11).
  - Guyon (2024, *Finance Stoch.* 28(1)): DMSP exact joint fit (ch15).
  - Nutz–Riveros Valdevenito (2024), Andrès–Jourdain (2024): PDV well-posedness.
  - Bayer–Breneis (2023): Markovian approximations with superpolynomial convergence (ch10).
  - Regularity structures for rough volatility (*Rough Volatility* ch. 10): a renormalised Taylor expansion for
    pricing; and Friz–Gatheral's forest expansion (ch. 9).
  - Signature models (Cuchiero et al.), and the open-access *Signature Methods in Finance* (Springer, 2025/26; already in
    Part 5's plan).
  - **Computed close**: a summary board of every model's out-of-sample score in this part (the same as ch17's board but sorted
    by date of the idea). The narration ends on the verdict the numbers give.
- **Pause-and-predict.** "If volatility is a function of the path, is it still rough?" (It can look rough if the kernel is
  singular; GL's fitted kernels are shifted power laws, bounded at zero: smooth. The two views differ exactly at the shortest
  scales.)
- **Compute.** None new.

### O · Recap, desk questions, problems (2.6) · `s12_outro` (deepened)
- Recap in 12 lines (one per item), payoff card (Parts 15, 16, 17, 27, 32, 36, 37, 38), and a reference card updated with every
  paper above.
- **Desk questions** (README has solutions):
  * keep "H ≈ 0.1: one-day against one-month skew" (≈ 3.9×);
  * keep "rough or fast mean reversion: how to test" (now answered by ch11's map and ch12);
  * keep "calibrate in milliseconds" (ch17);
  * add the syllabus's own: **"Why can't a one-factor Markov SV model fit a 1-week skew?"** Its skew is flat below 1/κ (ch2); to
    be steep at 1 week, κ must be ≈ 50 a year, and then the long end collapses like 1/(κT).
- **Problems** (90 s): keep the existing 5, plus:
  6. derive ∫₀ᵀ∫ₜᵀ(u − t)^{H−½}du dt;
  7. show $b_k$ is the cell-mean point of the kernel (ch6);
  8. show the 4FMPDV factor obeys dR = λ(r² − R)dt.

  README solutions in English and Chinese.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.8 | 10 Lifts | 2.6 |
| 1 Fact | 3.0 | 11 Debate I | 3.0 |
| 2 Skew math | 3.0 | 12 Debate II | 2.6 |
| 3 Rough | 3.0 | 13 PDV | 3.0 |
| 4 Forecast | 2.6 | 14 PDV/SPX + crisis | 3.0 |
| 5 rBergomi | 3.0 | 15 Joint SPX/VIX | 3.0 |
| 6 Hybrid | 2.6 | 16 Signatures | 2.6 |
| 7 Rough Heston | 3.0 | 17 Industry + House | 2.8 |
| 8 Adams | 3.0 | 18 Frontier | 3.0 |
| 9 Hawkes | 3.0 | Outro | 2.6 |
| | | **Total** | **≈ 57.2** |

This is about 7,950 spoken words at 139 words a minute. It sits 7 minutes above the floor and 3 below the cap: keep chapters at their
targets.

---

## 3b. Hands-on summary

**Labs** (`lab_card` ≤ 12 lines, then `lab_run` with cached outputs):

| # | Ch | Function (file, lines) | Output printed |
|---|---|---|---|
| 1 | 3 | `rough.log_rv_scaling` (rough.py 166–182, cut to 12) | fBM checks; H for BTC 2018–20 and 2024–25 |
| 2 | 6 | `rough.rbergomi_paths` (rough.py 29–44, cut to 12: covariance, Cholesky, `_b`, FFT) | Var W^H_1: hybrid 1.03, Riemann 0.40, exact 1.00 (H = 0.05) |
| 3 | 8 | `rough.frac_riccati` (rough.py 68–82) | the convergence table; Heston check 7e-7 |
| 4 | 13 | `rough.pdv4_step` (new, 8 lines) | R² of 4FMPDV against TSPL |
| 5 | 15 | `arbitrage.entropic_mot` (arbitrage.py 331–346, 12 lines) | lower and upper bound; final constraint errors |
| 6 | 16 | `rough.sigvol_logS` (new, 10 lines) | calibration error against rBergomi |

**Replays** (TrainingReplay or ValueTracker scrubs, seeds as `seed_band`):
* ch5: the rBergomi calibration (3 seeds; Heston 1.37 as the baseline line);
* ch8: the H profile of rough Heston (9 fits);
* ch12: the 2-factor Bergomi fit;
* ch13: the PDV kernel fit (and the 4FMPDV fit);
* ch15: the Sinkhorn trace;
* ch16: the sigvol calibration (2 seeds).

Store the iterates by wrapping the residual function. Record (params, ½‖r‖²) per evaluation and thin the record to the
accepted steps by a running minimum.

**Live simulations**:
* the continuous zoom (hook);
* the loom of weekly skews (ch1);
* the kernel triangle pouring (ch2);
* m(q, Δ) building (ch3);
* forecast weights reshaping (ch4);
* paths growing in the hybrid scheme (ch6);
* Adams predictor/corrector with memory arrows (ch8);
* Hawkes bins filling and the family tree (ch9);
* exponentials adding into the kernel; lifted paths converging (ch10);
* PDV memories filling (ch13);
* VIX and PDV tracing; the crisis week's hours (ch14);
* qRH riding the parabola (ch15);
* signature bars growing (ch16).

**3D**:
* ch1: the skew loom, (log T, week) → log skew;
* ch2: the kernel over the triangle;
* ch8: |φ(u, T)|;
* ch11: the bias map, (H, half-life) → Ĥ.

**Compute budget** (seeded, resumable; about 95 CPU-minutes of 120, existing items included):

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| skew* | <0.1 | rh_profile9 | 15 | bergomi2f | 10 |
| skew_weekly | 8 | hawkes* | 0.5 | pdv*, pdv_replay, pdv4 | 3 |
| skew_models, skew_kernel | 1 | hawkes_sweep | 1 | pdv_spx, crisis_aug2024 | 1.5 |
| roughness*, roughness_2018 | 2 | lift*, lift_paths | 2 | qrh_sim (+ VIX stretch), zumbach_spx | 2–7 |
| rfsv_forecast | 1 | artefact* | 2 | joint_bounds | 2 |
| rbergomi*, rbskew* | 12 | bias_map | 2 | sigvol | 10 |
| rb_replay (3 seeds, `CACHE.partial`) | 15 | adams_conv | 0.2 | calib_speed | 2 |
| hybrid_check | 1 | rheston*, rprofile* | 10 | envelope* | 0 |

(* exists; the existing items' times are estimates, so measure on rebuild.) `python -m videos.quant.quant14.compute` rebuilds
the part. No torch is needed. All items are numpy/scipy with `OMP_NUM_THREADS=1`. Run the long ones (`rb_replay`,
`rh_profile9`, `bergomi2f`, `sigvol`) under `nice -n 10 nohup` with logs in the scratchpad.

---

## 4. Industry and frontier: verified sources (2 Nov 2026)

| Fact | Source |
|---|---|
| *Rough Volatility* (SIAM 2023): 10 chapters, titles, authors and pages as in §2b | Crossref, prefix 10.1137/1.9781611977783 (e.g. https://doi.org/10.1137/1.9781611977783.ch4) |
| *Nonlinear Option Pricing* chapter list | Crossref, DOIs 10.1201/b16332-6 … -18 |
| Risk Awards 2021: Gatheral and Rosenbaum, Quants of the Year; the qRH joint-calibration paper cited; Gatheral: people "actually using it in practice" | https://www.risk.net/awards/7736196/quants-of-the-year-jim-gatheral-and-mathieu-rosenbaum ; https://newscenter.baruch.cuny.edu/news/baruch-professor-jim-gatheral-named-quant-of-the-year/ |
| Horvath–Muguruza–Tomas, *QF* 21(1):11–27 (2021); "a few milliseconds"; Risk Rising Star | https://ideas.repec.org/a/taf/quantf/v21y2021i1p11-27.html ; https://www.risk.net/awards/7216346/rising-star-in-quant-finance-blanka-horvath-aitor-muguruza-and-mehdi-tomas |
| Rømer, *QF* 22(10):1805–1838 (2022); Risk Rising Star | https://ideas.repec.org/a/taf/quantf/v22y2022i10p1805-1838.html ; https://www.risk.net/awards/7955764/rising-star-in-quantitative-finance-sigurd-emil-romer (year of award *(verify)*) |
| Rosenbaum–Zhang, deep calibration of qRH (Risk; arXiv 2107.01611) | https://www.risk.net/cutting-edge/7954656/deep-calibration-of-the-quadratic-rough-heston-model ; https://arxiv.org/abs/2107.01611 |
| Guyon (2024) DMSP, *Finance Stoch.* 28(1):27–79 | https://ideas.repec.org/a/spr/finsto/v28y2024i1d10.1007_s00780-023-00524-y.html |
| Guyon–El Amrani: Risk.net Cutting Edge; 2020–21 SPX/SX5E/DAX; a power law fails with short maturities | https://www.risk.net/cutting-edge/7957304/does-the-term-structure-of-the-at-the-money-skew-really-follow-a-power-law |
| Fukasawa (2021), "Volatility has to be rough", *QF* 21(1):1–8 | https://arxiv.org/abs/2002.09215 |
| Fukasawa–Takabatake–Westphal, "Is volatility rough?" (arXiv 1905.04852; *Math. Finance* 2022 per READING.md, *(verify issue)*) | https://arxiv.org/abs/1905.04852 |
| Bolko et al., *J. Econometrics* 235(2):745–778 (2023); H ≈ 0.05 | https://arxiv.org/abs/2010.04610 |
| Chong et al., *Ann. Statist.* 52(4):1277–1306 (2024); rate n^{−1/(4H+2)}; CLT companion *AAP* 34(3) | https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-4/10.1214/23-AOS2343.full ; https://arxiv.org/abs/2210.01216 |
| Abi Jaber–Li, *Math. Finance* 35(4):796–817 (2025); the findings as in ch12 | https://arxiv.org/abs/2401.03345 ; https://ideas.repec.org/a/bla/mathfi/v35y2025i4p796-817.html |
| Bayer–Breneis, *QF* 23(1):53–70 (2023) | https://ideas.repec.org/a/taf/quantf/v23y2023i1p53-70.html |
| Nutz–Riveros Valdevenito: 4-PDV well posed (*Finance Stoch.* 28(4) per a citing paper, *(verify)*); Andrès–Jourdain | https://arxiv.org/abs/2307.01319 ; https://arxiv.org/abs/2408.02477 |
| Cuchiero, **Gazzani**, Svaluto-Ferro, *SIFIN* 2023 (volume *(verify)*) | https://arxiv.org/abs/2207.13136 |
| BIS Bulletin 90 (27 Aug 2024): the VIX rise far exceeded its historical relation with S&P 500 returns; deleveraging | https://www.bis.org/publ/bisbull90.htm (the exact wording is from a search summary; quote only after reading the PDF *(verify)*) |
| BIS Bulletin 95 (Todorov, Vilkov, 29 Oct 2024): biggest one-day VIX spike; widening put bid–ask spreads; VIX ETFs and dispersion unlikely drivers; pre-market peak "around 66" | https://www.bis.org/publ/bisbull95.htm (the 66 figure is from a search summary of the PDF *(verify in the PDF)*) |
| SEC DERA staff working paper on the VIX spike ("over 65" pre-market) | https://www.sec.gov/files/dera-vix-working-paper-2504.pdf *(title and authors to verify)* |
| VIX closes 23.39 (2 Aug 2024), 38.57 (5 Aug), 27.71 (6 Aug) | FRED VIXCLS (local cache `.cache/quant_data/fred/VIXCLS.csv`) |
| Cboe VIX1D launched 24 Apr 2023, from SPXW quotes; 0DTE "nearly half" of S&P option volume (Reuters) | https://ir.cboe.com/news/news-details/2023/Cboe-Global-Markets-Launches-1-Day-Volatility-Index-Designed-to-Measure-Volatility-Over-Current-Trading-Day-04-24-2023/default.aspx |

**Unverified** (keep the marks or drop):
* the Bergomi–Guyon first-order skew formula's normalisation;
* the GJR forecast constant cos(Hπ)/π;
* Livieri et al.'s reported H from options;
* the qRH parameter values;
* Guyon–Henry-Labordère ch. 11 treating PDV;
* the Friz–Hairer chapter on rough volatility;
* Bergomi's chapter numbers;
* the year of Rømer's Rising Star award;
* the SEC paper's authors;
* the exact BIS quotations (from search summaries, not the PDFs);
* Cboe's response to BIS (seen only in a trade-press headline; do not use).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 14 · Rough and Path-Dependent Volatility (~57; frontier)
1. The fact: the at-the-money skew grows like T^{H−1/2}, measured on 102 weekly Deribit surfaces; why a kernel makes
   it (the skew as integrated spot–variance covariance), why one-factor Markov models cannot, and why a power law forces
   roughness (Fukasawa 2021).
2. Volatility is rough (Gatheral–Jaisson–Rosenbaum 2018), re-measured on bitcoin in two eras; the rough forecast
   formula against HAR; long memory (Comte–Renault 1998) is not roughness.
3. Rough Bergomi (Bayer–Friz–Gatheral 2016): the martingale property and the variance curve; calibrated and replayed;
   the hybrid scheme (Bennedsen–Lunde–Pakkanen 2017) against naive discretisation.
4. Rough Heston (El Euch–Rosenbaum 2019): the affine Volterra derivation, the fractional Riccati equation, Adams with
   its convergence measured; how much the Surface cares about H.
5. Where roughness comes from: nearly unstable Hawkes order flow (Jaisson–Rosenbaum 2016; El Euch–Fukasawa–Rosenbaum
   2018), simulated by branching.
6. Markovian lifts (Abi Jaber–El Euch 2019; Abi Jaber 2019; Bayer–Breneis 2023).
7. The debate: the estimator's bias map (rough against fast mean reversion), estimation theory (Fukasawa et al. 2022;
   Bolko et al. 2023; Chong et al. 2024; Cont–Das 2024); the options side (Guyon–El Amrani; Rømer 2022; Abi Jaber–Li
   2025) and a two-factor Bergomi on the Surface.
8. Path-dependent volatility (Guyon–Lekeufack 2023) on DVOL and on the VIX; the 4-factor Markovian PDV.
9. Quadratic rough Heston (Gatheral–Jusselin–Rosenbaum 2020): the Zumbach effect; joint SPX/VIX.
10. Guyon's (2020, 2024) puzzle and dispersion-constrained martingale Schrödinger problem; martingale-transport bounds.
11. Signature volatility models (Cuchiero–Gazzani–Svaluto-Ferro 2023), calibrated to the Surface.
12. What desks use and why: speed, surrogates (Horvath–Muguruza–Tomas 2021) and lifts; Rule 14.

*Textbooks:* Bayer–Friz–Fukasawa–Gatheral–Jacquier–Rosenbaum (eds.) *Rough Volatility* (SIAM 2023), ch. 1–10;
Guyon–Henry-Labordère *Nonlinear Option Pricing* ch. 10–11 (UVM → 15, BSDEs → 17); Bergomi ch. 7–8; Gatheral ch. 3–5.
*Computed/Trained:* weekly skew power laws; model skews; GJR on BTC 2018–20 and 2024–25; RFSV against HAR; rBergomi
calibration replayed (3 seeds); hybrid against Riemann; Adams convergence and the H profile; branching Hawkes sweep;
lifts; the estimator bias map; a two-factor Bergomi; PDV on DVOL and VIX, 4FMPDV; qRH and the Zumbach effect;
martingale-transport bounds; a signature volatility model on the Surface.
*Visuals:* the skew loom (3D); the kernel over the triangle (3D); |φ(u, T)| (3D); the bias map (3D); the hybrid scheme
filling the singular cell; Adams with memory arrows; Hawkes family trees; exponentials summing into a power law.
*Labs:* `log_rv_scaling`, `rbergomi_paths`, `frac_riccati`, `pdv4_step`, `entropic_mot`, `sigvol_logS`.
*Crisis:* 5 August 2024: the VIX at about 66 before the open, on wide put quotes; path-dependence explains bitcoin's
DVOL that day and not the VIX. *Firms:* Cboe (VIX, VIX1D), Deribit (DVOL); Risk's 2021 Quants of the Year.
*Desk:* "Why can't a one-factor Markov SV model fit a 1-week skew?"; "Rough or fast mean reversion: how would you
test it?"; "Calibrate a rough model in milliseconds."
*House:* rough and PDV pricers; Rule 14.
```

---

## 6. Implementation notes

**Manifest order** (keep every existing module and class):
1. `s01_hook`
2. `s02_fact`
3. `s02a_skewmath`
4. `s03_rough`
5. `s03a_forecast`
6. `s04_rbergomi`
7. `s04a_hybrid`
8. `s05_rheston`
9. `s05a_adams`
10. `s06_hawkes`
11. `s07_lift`
12. `s08_debate`
13. `s08a_options`
14. `s09_pdv`
15. `s09a_spx`
16. `s09b_joint`
17. `s09c_signature`
18. `s11_house` (ch17)
19. `s10_frontier` (ch18)
20. `s12_outro`

Chapter numbers on `chapter_card`s must be renumbered to match. `zh_lines.py` `CHAPTERS` gets the new class names.

**New House functions** (append to `explainer/quant/house/rough.py` unless noted; one test each in
`tests/test_quant_house.py`):

| Function | Test |
|---|---|
| `volterra_riemann(H, T, n, n_paths, seed)` (the naive scheme, for ch6) | its variance at H = 0.3 is within 10% of t^{2H}, and below the hybrid's at H = 0.05 |
| `skew_term_fit(T, skew)` (power and shifted fits, as in `compute_skew`) | recovers a = 0.4 on synthetic c·T^{−0.4} |
| `fou_paths(H, half_life, n, dt, seed)` (fBM increments + AR(1) filter) | with half_life=None it equals cumulative fBM; stationary variance finite with mean reversion |
| `rfsv_predict(log_v, H, horizon, window)` | on simulated fBM, beats last-value at horizon 5 |
| `pdv4_step` / `pdv4_features(r, dt, lam0, lam1, theta)` | the EMA recursion equals the convolution with the 2-exponential kernel |
| `qrh_paths(a, b, c, lam, eta, H, N, T, n, n_paths, seed)` (lifted) | V ≥ c everywhere; at η = 0, deterministic Z |
| `sigvol_features(T_idx, n, n_paths, depth, seed)` and `sigvol_logS(ell, rho, A_W, A_perp, B)` | with ℓ = (σ, 0, …) it reproduces Black–Scholes prices within MC error |
| `sim.hawkes_branching_powerlaw(mu, n, alpha, c, T, seed)` | mean count ≈ μT/(1 − n) within 5% |
| `lift_weights(H, N, rN)` (expose `c`, `x` from `lifted_heston_cf`) | Σ c_i e^{−x_i t} within 5% of the kernel on [1e-2, 1] for N = 20 |

**Data.** Every input is already in the manifest except one: `data.fred("VIXCLS", "1990-01-01", "2025-12-31")`, which adds a
manifest entry via the data layer (the CSV is cached). The existing inputs are:
* Deribit weekly option trades (102 days, 2024-01-03 … 2025-12-11);
* Binance BTCUSDT 1m (2018–2020) and 5m (2024–25);
* DVOL hourly and daily;
* Ken French daily factors through 2025-12-31;
* Part 13's cached `bergomi`/`calibrate`/`skew` via `Cache("quant13")`.

**Narration branches** (computed verdicts, never typed):
* the weekly median exponent and the bounded-better share;
* RFSV against HAR at each horizon;
* the seed spread of rBergomi's H;
* Hawkes H against n (and the failure to recover α − ½);
* 2-factor Bergomi against rBergomi;
* sigvol against rBergomi;
* the qRH and S&P Zumbach signs;
* the PDV gap on 5 Aug 2024;
* α₁ at its bound in `pdv_spx`.

**Corrections to existing text:**
* "Gazzetta" → "Gazzani" in `s10_frontier`, the reference card and READING.md.
* Guyon's DMSP card year 2022 → 2024 (*Finance Stoch.*), with the 2020 Risk paper as the puzzle's solution.
* Guyon–El Amrani's venue → Risk (Cutting Edge), unless the implementer finds a *QF* version.
* `s02_fact`'s line "jumps explode like one over maturity" must be replaced by ch2's computed result, or dropped.

**Risks.**
1. `skew_weekly` is noisy (per-week log RMSE ≈ 0.6). Filter and weight it, show the IQR, and do not over-read a single week.
2. RFSV may lose to HAR. That is fine and is said; it is the honest result.
3. `rb_replay` and `bergomi2f` MC-calibration noise: use common random numbers, re-price on a fresh seed, and show seeds as bands.
4. `sigvol` memory: use float32, or 10,000 paths.
5. The qRH parameters are unverified. If the paper's values cannot be confirmed, label them "illustrative parameters" and keep
   only the qualitative Zumbach check.
6. The `joint_bounds` toy is not Guyon's algorithm. Label it so.
7. The total is 57 min against a 60 cap. Watch the long chapters (2, 11, 14, 15) for overrun.

**New terms for QUANT_ZH_GUIDE.md:**

| English | Chinese |
|---|---|
| hybrid scheme | 混合格式 |
| fractional Riccati equation | 分数阶里卡蒂方程 |
| Adams scheme | 亚当斯格式 |
| Markovian lift | 马尔可夫提升 |
| nearly unstable | 近乎不稳定 |
| branching ratio | 分支比 |
| bias map | 偏差图 |
| path-dependent volatility | 路径依赖波动率 |
| Zumbach effect | 宗巴赫效应 |
| martingale Schrödinger problem | 鞅薛定谔问题 |
| signature volatility model | 签名波动率模型 |
| forward variance curve | 远期方差曲线 |
| 0DTE | 零日到期期权 |

**README:**
* the chapter list with minutes;
* the textbook audit tables (§2b);
* the full paper list (§2c plus additions);
* 4 desk questions and 8 problems with solutions, in English and Chinese;
* "rebuild with one command".

## 7. Lead's decisions (2 Nov 2026)

1. Yes, fix: "Gazzetta" → "Gazzani"; Guyon–El Amrani is Risk (Cutting Edge); Guyon's DMSP is Finance Stoch. 28(1), 2024 — in READING.md, the README and the scenes. Replace `s02_fact`'s "jump skews explode like 1/T" with a computed result.
2. Yes: VIXCLS 1990–2025 through the data layer. Part 12 is adding the same series in parallel: check `videos/quant/data/manifest.json` first and reuse an existing entry rather than adding a duplicate.
3. Accepted: `s11_house` as chapter 17, `s10_frontier` as chapter 18; the manifest sets the order.
4. Keep the joint SPX/VIX illustration, labelled plainly as a martingale-transport bounds illustration in the spirit of Guyon, not his algorithm.
5. Yes: results that go against rough models are shown as they come; the forecast comparison uses a rolling (expanding-window) out-of-sample design with enough training data.
Mind the 60-minute cap: measure as you go.
