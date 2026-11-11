# Part 13 · Stochastic Volatility and Jumps: expansion plan (26.0 → ~58 min)

This is a planning document. Nothing in the repo was changed.

**Sources read.**
* `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 (the November 2026 standard) and §6 Parts 12–16.
* `READING.md`: the spine tables, the Gatheral coverage map, the Hull/Shreve rows that name Part 13, and §4 Part 13 (22 papers).
* `videos/ai/LECTURE_GUIDE.md`; `videos/quant/plans/{RESEARCH,IMPLEMENT,quant5}.md` (format).
* Every file in `videos/quant/quant13/` (manifest, common, compute, the eleven scenes, README) and the cached results in
  `.cache/quant13/` (all eleven items exist).
* The House: `explainer/quant/house/stochvol.py` (all of it), `volsurface.py`, `rough.py` (signatures), and
  `tests/test_quant_house.py` §stochvol. The instruments in `explainer/quant/viz.py` (`lab_card`, `lab_run`,
  `TrainingReplay`, `seed_band`, `price_surface`, `smile_points3d`, `readout`, `HedgeLedger`).

**Probe scripts.** They are not in the repo: `scratchpad/q13/p1.py` … `p4.py`. They ran at `nice 10` with one thread, about
6 CPU-minutes in all, on a machine with a load average near 20. Every number marked **(probe)** is real and computed on the
cached Surface, Binance and DVOL data, but `compute.py` must recompute it.

**What the neighbours own (do not repeat).**
* **Part 5** (plan): Brownian motion, CIR's transition law and Feller's boundary test, Poisson processes, Lévy–Itô,
  Lévy–Khintchine and Itô for jumps.
* **Part 11**: P&L explain, vanna–volga, and a Heston straddle hedged with delta, gamma and vega (ch10).
* **Part 12**:
  * Dupire and Gyöngy, proved and checked on Heston (ch7);
  * the forward smile of local volatility and SSR = 2 (ch8);
  * the empirical SSR and stickiness (ch2);
  * variance swaps, the VIX/DVOL and the VRP;
  * the jump term of a variance swap.
* **Part 14**:
  * the skew's power law and its kernel derivation (Bergomi–Guyon; ch2);
  * calibrating two-factor Bergomi (`bergomi2f`, ch12);
  * the solutions to joint SPX/VIX (quadratic rough Heston, Guyon's DMSP; ch15);
  * rough models.
* **Part 15**: exotic reserves and uncertain volatility.
* **Part 16**: the derivations of COS, Carr–Madan and Lewis, ADI for Heston, MLMC and AAD.
* **Part 17**: neural calibrators.

So Part 13 is the home of:
* the stochastic-volatility models themselves, their characteristic functions derived, their simulation, and SABR;
* jump and Lévy models fitted to the Surface;
* SLV and the particle method;
* Bergomi's variance curves (the framework, not the fit);
* the forward smile and cliquets across models;
* the SPX/VIX puzzle stated and measured;
* calibration as an inverse problem;
* how desks judge a model by its hedge.

**Cadence.** 20 scenes (hook, 18 chapters, outro) of about **58 min**, which is about 8,050 words at 139 wpm. A chapter
runs 2.6–3.2 min (360–450 words).

---

## 1. Current state (`python tools/lecture_length.py quant13`: 26.0 min, 11 scenes)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 1.9 | DVOL 2021–2025 with three floods (Terra–Luna, FTX, August 2024). The cliquet across 5 models (spread 8%). Objectives and the House card. **No history segment.** |
| 1 | `s02_moves` | 2.5 | RV30 from 17% to 122%; DVOL's vol of vol 89%; on −5% days DVOL +6.4%, on +5% days +0.5%; correlation by year (−0.58 in 2022, +0.30 in 2023). A 1987 history card. Hull–White in two ladder rows. Good facts, **but the mixing argument is asserted, not derived**. |
| 2 | `s03_heston` | 3.1 | The model in 4 ladder rows (the Riccati equation *stated*). Six QE paths. The fit: Heston 1.33 against BS 3.89 vol points, κ = 14.8, ξ = 4.6, ρ = −0.31, Feller 0.37, 3-day expiry missed by 5.3. Euler against QE bias. **No derivation of the CF, no little-trap, no parameter intuition, QE not explained beyond one sentence, no lab.** |
| 3 | `s04_sabr` | 2.8 | Model; slice fits (0.38 points, 27 params, ν ∝ T^−0.49); backbone for β ∈ {0, ½, 1}; Hagan's 10-year density is negative below 0.7% and has mass 0.63. **Hagan's formula is quoted, not explained; the fixes are named only.** |
| 4 | `s05_jumps` | 3.9 | Merton, Kou and Bates in 3 rows; VG, Lévy and Carr–Wu in 3 rows; scores (VG 2.89, NIG 2.70, Bates 1.31, λ at its bound of 20); three slices; the skew term structure. **Two syllabus items share one chapter. No Merton series, no VG derivation, no CGMY, Kou or Merton fit, no simulation on screen.** |
| 5 | `s06_slv` | 1.9 | Model, Gyöngy condition, kernel particle estimator (3 rows); leverage function and repricing error (0.44–0.69 points). **No particles on screen, no convergence study, and the mixing fraction is fixed at ½ without discussion.** |
| 6 | `s07_bergomi` | 2.0 | The forward variance curve from the Surface (the weekend dip: Saturday RV 29% against 50–59% on weekdays); the 2-factor model in 3 rows. **No simulation, no vol-of-vol term structure, no SSR.** |
| 7 | `s08_forward` | 2.5 | Forward smiles across 5 models (LV flattens to 3.4 points of skew against 6.5 today); cliquet and forward-start bars; the SPX/VIX puzzle as two history cards. **The puzzle has no computation.** |
| 8 | `s09_calibration` | 2.3 | A 3D landscape over (κ, ξ) with 225 fits and a valley; all 12 starts at one minimum; 100 weekly Heston fits (median weekly |Δlog κ| 25%, κ at its bound in some weeks). Good. **No replay, no regularisation, no identifiability measure.** |
| 9 | `s10_house` | 1.0 | The calibrator module card and Rule 13. |
| — | `s11_outro` | 2.2 | Recap in 8 lines, 3 desk questions, problems, payoffs, references. |

**Overall.** The data work is excellent and real (keep every number). But:
* every model is *stated*: there is not one derivation carried through;
* there are **no labs, no replays, no live simulations** (apart from `Create()` of finished paths);
* there is one 3D scene (the landscape);
* there is **no industry or frontier chapter**;
* the cliquet's 8% disagreement, the part's own hook, is never explained mechanically.

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item | Now | Verdict → plan |
|---|---|---|
| 1 Why volatility must move | ch1 (2.5 min) | covered as facts; mixing not derived → **ch1 (facts, 1987 crisis), ch2 (Hull–White/Romano–Touzi mixing derived)** |
| 2 Heston: Riccati CF; Feller; QE | ch2 (3.1) | thin → **ch3 (CF derived + little trap), ch4 (parameters, short-T skew, fit replay), ch5 (Feller, QE derived, lab)** |
| 3 SABR: expansion, backbone, low-strike arbitrage, fixes | ch3 (2.8) | thin on the fixes → **ch6 (Hagan's formula, the backbone, slice replay), ch7 (density, arbitrage-free PDE computed, Bartlett delta)** |
| 4 Jumps: Merton, Kou, Bates | ch4 half | thin → **ch8 (Merton series derived; Merton, Kou and Bates fitted; Bates replay)** |
| 5 Lévy: VG, CGMY, NIG; Carr–Wu | ch4 half | thin → **ch9 (VG CF derived, CGMY fine structure, gamma clock live, lab)**; **ch10** (term structure of skew across all models) |
| 6 SLV; particle method | ch5 (1.9) | thin → **ch11 (particles live, convergence, lab), ch12 (mixing fraction swept)** |
| 7 Bergomi; forward variance as state | ch6 (2.0) | thin → **ch13 (variance curve simulated, vol-of-vol term structure, SSR of SV computed)** |
| 8 Forward smile, cliquets, model disagreement | ch7 half | covered → **ch14 (forward-start derived, Heston semi-analytic check, cliquet mechanics)**; disagreement → ch12, ch17 |
| 9 SPX/VIX puzzle | ch7 cards | asserted → **ch15 (stated, Jensen bound, measured on BTC: the model's vol of vol against DVOL's)** |
| 10 Calibration: landscape, identifiability, instability | ch8 (2.3) | good start → **ch16 (Hessian, regularised recalibration, 100-week replay, lab)** |
| Industry, frontier | absent | **ch17, ch18** |

### (b) Textbook sections → chapter (or another part)

Gatheral's and Bergomi's chapter titles were checked against the publishers' listings. Bergomi's titles come from the
Routledge page, fetched this session; the numbering follows its order. Cont–Tankov's titles and order come from the
Routledge/Eyrolles listings, chapter numbers *(verify)*. Lewis's titles come from the Wolfram library listing, numbering
*(verify)*.

| Book · chapter | Where |
|---|---|
| Gatheral 1 SV and LV (the SV PDE, Heston derivation set-up) | ch3 (PDE and affine ansatz); LV → Part 12 |
| Gatheral 2 The Heston model (CF, Riccati, the branch cut, simulation, the fit) | ch3, ch4, ch5 |
| Gatheral 3 The implied volatility surface (BBF, the Heston skew, term structure of ATM skew) | ch4 (ρξ/4√v₀ derived), ch10; the power law → Part 14 |
| Gatheral 4 Heston–Nandi (local variance of an SV model) | Part 12 ch7; here a ch11 line (E[v \| S] is what SLV divides by) |
| Gatheral 5 Adding jumps (SVJ, SVJJ, short-dated skew) | ch8, ch10; jumps in variance swaps → Part 12 ch9 |
| Gatheral 6 Modeling default (jump to ruin) | ch8 card (λ with a jump to zero); credit → Part 20 |
| Gatheral 7 Asymptotics | ch4 (short-T skew), ch10 (long-T 1/T); Lee → Part 12; the power law → Part 14 |
| Gatheral 8 Dynamics of the volatility surface (skew stickiness) | ch13 (the SSR of SV, computed); empirical → Part 12 ch2 |
| Gatheral 10 Exotic cliquets | ch14; structuring → Part 15 |
| Gatheral 11 Volatility derivatives (options on VIX) | ch15 (the Heston vol-index option smile, computed); swaps and the VIX → Part 12 |
| Bergomi 3 Forward-start options (SV part) | ch14 |
| Bergomi 4 Stochastic volatility, introduction (the vega-hedged P&L, realized against implied vol of vol and covariance) | ch2, ch17 (hedging) |
| Bergomi 6 The Heston model (its limits: one κ ties the curve's shape to the vol-of-vol term structure) | ch4, ch13 |
| Bergomi 7 Forward variance models (the N-factor model, simulation) | ch13 (simulated); calibrated 2-factor → Part 14 ch12 |
| Bergomi 8 The smile of SV models (expansion in vol of vol) | ch2 (second order in vol of vol), ch10; the full Bergomi–Guyon expansion → Part 14 ch2 |
| Bergomi 9 Linking static and dynamic properties (SSR) | ch13 |
| Bergomi 10 What causes equity smiles? | ch1, ch2, ch10 |
| Bergomi 11 Multi-asset SV | Part 15 (worst-of, correlation skew); a README note |
| Bergomi 12 Local-stochastic volatility | ch11, ch12 |
| Cont–Tankov 4 Building Lévy processes (subordination, VG, NIG, CGMY, tempered stable) | ch9 |
| C–T 6 Simulating Lévy processes | ch9 (gamma clock), lab |
| C–T 11 Risk-neutral modelling with exponential Lévy (smile shapes, term structure) | ch9, ch10 |
| C–T 13 Inverse problems and model calibration (ill-posedness, regularisation, relative entropy) | ch16 |
| C–T 14 Time-inhomogeneous jump processes (additive/Sato processes fix the term structure) | ch10 card |
| C–T 15 Stochastic volatility models with jumps (Bates, BNS-OU, time-changed Lévy) | ch8, ch9 |
| C–T 1–3, 5, 7–10, 12 | Part 5 (2–3, 6, 8), Part 11 and Part 5 (9–10 hedging, incompleteness), Part 16 (12 PIDE), README note (5 multivariate) |
| Lewis 1 Introduction · 2 The fundamental transform | ch3 (the CF as a transform); Lewis's pricing formula → Part 16 |
| Lewis 3 The vol-of-vol series expansion · 4 Mixing solutions · 5 The smile | ch2 |
| Lewis 6 The term structure of implied volatility | ch10 |
| Lewis 7 Utility-based equilibrium (the price of vol risk) | ch15 (P against Q for ξ), Part 12 (VRP) |
| Lewis 8 Duality and changes of numéraire | ch14 card (put–call symmetry for forward starts) |
| Lewis 9 Volatility explosions and the failure of the martingale pricing formula | ch5 card (moment explosions; Andersen–Piterbarg 2007); Lee → Part 12 |
| Lewis 10 Option prices at large volatility · 11 Solutions to models | README note · ch3 |
| Guyon–Henry-Labordère, *Nonlinear Option Pricing*: McKean SDEs; calibration of LSV by particles *(verify numbering; Part 14's plan gives 10–11)* | ch11; PDV as McKean → Part 14 |
| Oosterlee–Grzelak: Heston and the QE scheme; Lévy/jump chapter; COS | ch5, ch9; COS → Part 16 *(verify chapter numbers)* |
| Shreve II 11.7 A call in a jump model | ch8 (Merton series) |
| Hull: "More on models" (mixed jump–diffusion, SV, CEV) | ch8, ch2, ch6 (CEV as SABR's β backbone) |

### (c) Papers on the Part 13 list → where they appear

| Paper | Now | Plan |
|---|---|---|
| Merton 1976 | ch4 narration | ch8: the series derivation card and the fit |
| Hull–White 1987 | ch1 row | ch2: the mixing theorem, derived |
| Madan–Seneta 1990 | absent | ch9 card (VG for returns) |
| Stein–Stein 1991 | absent | ch2 (the OU-vol model, history strip) |
| Heston 1993 | on screen | ch3 (the CF derived) |
| Bates 1996 | on screen | ch8 (fit, replay) |
| Bakshi–Cao–Chen 1997 | absent | ch17 (horse race: SV+jumps for pricing, SV for hedging) |
| Barndorff-Nielsen 1997 | NIG fitted, uncited | ch9 card (NIG via inverse-Gaussian clock) |
| Madan–Carr–Chang 1998 | on screen | ch9 (CF derived) |
| Bates 2000 | ch1 card | ch1 crisis file (post-1987 fears) |
| Duffie–Pan–Singleton 2000 | absent | ch3 (affine transform analysis: why the ansatz works), ch8 (SVCJ) |
| Carr–Geman–Madan–Yor 2002 | named | ch9 (CGMY fitted, Y on screen) |
| Hagan et al. 2002 | on screen | ch6 |
| Kou 2002 | narration | ch8 (fitted; memoryless overshoot card) |
| Bergomi 2004/2005 | ch6 | ch13 |
| Carr–Wu 2004 | ch4 row | ch9 (time change derived) |
| Albrecher et al. 2007 | references only | ch3 (little trap, computed failure of the original form) |
| Broadie–Chernov–Johannes 2007 | absent | ch8 card (jumps in volatility needed; risk premia) |
| Andersen 2008 | on screen | ch5 (derived, lab) |
| Gatheral 2008 | ch7 card | ch15 |
| Guyon–Henry-Labordère 2012 | ch5 | ch11 |
| Hagan et al. 2014 (arbitrage-free SABR) | named | ch7 (PDE solved) |

**Proposed additions to READING.md, Part 13.** Unless marked, these are standard references and the implementing agent
re-checks the venue.

*Classic.*
* Scott (1987), *JFQA*; Wiggins (1987), *JFE*.
* Renault–Touzi (1996), *Math. Finance* (symmetric smile when ρ = 0); Romano–Touzi (1997), *Math. Finance* (mixing with
  correlation).
* Lipton (2002), "The vol smile problem", *Risk*.
* Eraker–Johannes–Polson (2003), *JF*.
* Cont–Tankov (2004), "Nonparametric calibration of jump-diffusion option pricing models", *J. Comput. Finance*.
* Kou–Wang (2004), *Management Science*.
* Kahl–Jäckel (2005), "Not-so-complex logarithms in the Heston model", *Wilmott*.
* Broadie–Kaya (2006), *Operations Research*.
* Bartlett (2006), "Hedging under SABR", *Wilmott*.
* Andersen–Piterbarg (2007), "Moment explosions in stochastic volatility models", *Finance Stoch.*
* Carr–Geman–Madan–Yor (2007), "Self-decomposability and option pricing", *Math. Finance*.
* Ren–Madan–Qian (2007), *Risk*.
* Obłój (2008), "Fine-tune your smile" (arXiv 0708.0998, seen this session).
* Henry-Labordère (2009), *Risk*.
* Lord–Koekkoek–van Dijk (2010), *QF*.
* Cont–Kokholm (2013), *Math. Finance*.
* Antonov–Konikov–Spector (2015), "The free boundary SABR", *Wilmott*.
* Hull–White (2017), "Optimal delta hedging for options", *JBF* *(verify volume and pages)*.

*Bitcoin.*
* Hou–Wang–Chen–Härdle (2020), *J. Financial Econometrics* 18(2):250–279 (verified).
* Matic–Packham–Härdle (2023), *Rev. Derivatives Research* 26(1):91–133 (verified).

*Frontier.* See §4.

---

## 3. The chapter list (20 scenes, about 58 min)

**Conventions.**
* **Visual**: the signature picture, built before the formula.
* **Live**: a simulation drawn as it runs.
* **Lab**: `lab_card` with ≤ 12 lines of House code, then `lab_run` typing out the cached result.
* **Replay**: `TrainingReplay` or a ValueTracker scrub through stored iterates, with starts or seeds as `seed_band`.
* **Compute**: the `compute.py` item, with CPU minutes on one core.

Existing items keep their names. Kept modules keep their names and classes; new modules are inserted, and
`manifest.py` sets the order.

**Recording iterates.** `sv.calibrate` uses `least_squares`, which has no callback. Add `trace=True` to the House
function: it wraps the residual function and stores (evaluation number, RMSE, parameters). **(probe)** One Heston fit on
the Surface takes 90–120 evaluations, about 4–5 s.

### H · Hook: "The second river" (2.8 min) · `s01_hook` (deepened)
- **Goal.** The puzzle, the era, the map.
- **Beats.**
  1. Keep the DVOL river with its three floods, and keep the cliquet table (5 models, the same vanillas, 7.8% apart).
  2. **New, "how we got here" (≈ 60 s).** The timeline strip lights:
     * 1973 Black–Scholes;
     * 1976 Merton's jumps;
     * **1987 crash** (red);
     * 1987 Hull–White;
     * 1991 Stein–Stein;
     * 1993 Heston;
     * 1994 Dupire and Rubinstein's implied trees;
     * 1996 Bates;
     * 1998 variance gamma for options;
     * 2002 SABR, Kou and CGMY;
     * 2004 Carr–Wu, and VIX futures (26 March);
     * 2005 Bergomi;
     * 2006 VIX options (24 February);
     * 2008 Andersen's QE, and Gatheral's SPX/VIX talk;
     * 2012 the particle method;
     * 2020 Guyon's puzzle solved;
     * 2022 Terra–Luna and FTX (red).
  3. The objectives card (10 items + industry + frontier).
  4. The House card: the calibrator.
- **Pause-and-predict.** "Five models agree on every vanilla option. Can they disagree on anything?" (Yes: on the
  future smile, by 8% here.)
- **Compute.** `facts`, `exotics` (exist).

### 1 · Why volatility must move (3.0) · item 1 · `s02_moves` (kept: `series`, `leverage`; `mixing` moves to ch2)
- **Goal.** The stylised facts of volatility, measured. The crisis that taught the market the skew.
- **Beats.**
  1. **Live, the two rivers.** BTC's price on top and RV30/DVOL below, drawn together by a ValueTracker. A scatter of
     (daily return, Δlog DVOL) builds point by point at the side, with the regression line rotating as points arrive.
     Colour by year, so 2023's flip shows as a cloud tilting the other way.
  2. Four facts, each a number:
     * the range of RV30 (17–122%);
     * the vol of vol (89%);
     * clustering: the autocorrelation of |r| decays slowly (new, computed);
     * mean reversion: the half-life of log DVOL from an AR(1) (new, computed).
  3. **Crisis file: 19 October 1987.** S&P 500 daily data, if `yahoo_daily("^GSPC")` reaches 1987 *(verify; else FRED
     SP500 does not go back that far, so cite)*. The day's log return was −22.9% against the prior year's daily σ. Its
     z-score and the GBM probability are printed (computed). Then Rubinstein (1994): flat index-option vols before,
     dear puts ever since. Bates (2000): post-'87 crash fears priced in S&P futures options.
- **Derivation.** Short ladder, the measurement definitions:
  - RV and vol of vol, $\widehat{\text{volvol}} = \operatorname{sd}(\Delta\log\text{DVOL})\sqrt{365}$, defined;
  - AR(1) on $\log\text{DVOL}$ gives a half-life $=\ln 2/\hat\kappa$, the discretised OU of Part 5.
- **Experiment.** `facts` (exists). `facts` gains `acf_abs` (lags 1–60), `dvol_halflife` and `crash1987` (needs one new
  data-layer entry, ^GSPC 1986–1987; <0.1 min).
- **Pause-and-predict.** "Bitcoin rose 10% today. Does implied volatility rise or fall?" (Both have happened: −0.58
  correlation in 2022, +0.30 in 2023.)

### 2 · Random volatility makes a smile (2.8) · item 1 · `s02a_mixing` (new; from `s02_moves.mixing`)
- **Goal.** Prove that stochastic volatility makes a smile (ρ = 0), and that correlation tilts it. Hull–White,
  Renault–Touzi and Romano–Touzi.
- **Beats.**
  1. **Visual, mixing.** A slider raises the vol of vol. The density of ln S_T is drawn as a crowd of thin Gaussians
     (one per simulated variance path, opacity ∝ weight) summing to a fat-tailed envelope (gold). Under it, the
     implied-vol curve lifts at both wings while the centre dips.
  2. Turn on ρ < 0: each Gaussian is shifted left in proportion to its variance (Romano–Touzi's $\xi_T$), and the smile
     tilts into a skew.
  3. History strip: Hull–White, Scott and Wiggins (1987); Stein–Stein (1991, OU volatility).
- **Derivation.**
  - With ρ = 0, $\ln S_T \mid \{v_s\} \sim N\big(-\tfrac12 \int_0^T v\,ds,\ \int_0^T v\,ds\big)$ (W¹ is independent of the variance path).
  - $C = \mathbb E\big[C_{BS}(S_0,K,T,\bar\sigma^2_T)\big]$, $\bar\sigma^2_T = \tfrac1T\int_0^T v\,ds$ (tower property: Hull–White 1987).
  - $C \approx C_{BS}(\mathbb E\bar\sigma^2) + \tfrac12\,\partial^2_{\sigma^2}C_{BS}\,\operatorname{Var}(\bar\sigma^2)$ (Taylor to second order in vol of vol).
  - $\partial^2_{\sigma}C_{BS} = \text{vega}\cdot d_1d_2/\sigma$, positive for $|k|$ large and negative at the money (differentiate vega $= S\sqrt T\varphi(d_1)$). So the wings rise and the centre falls: a smile, symmetric in $k$ (Renault–Touzi 1996).
  - With ρ ≠ 0, write $W^1 = \rho W^2 + \sqrt{1-\rho^2}W^\perp$: $C = \mathbb E\big[C_{BS}\big(S_0\xi_T, K, T, (1-\rho^2)\bar\sigma^2_T\big)\big]$, $\xi_T = e^{\rho\int\sqrt v\,dW^2 - \frac12\rho^2\int v\,ds}$ (condition on $W^2$; Romano–Touzi 1997). High-variance paths come with low $\xi_T$ when ρ < 0, which gives the skew.
- **Experiment.** `mixing` (new): on the fitted Heston, the Romano–Touzi conditional estimator (20,000 variance paths by
  QE, with the conditional BS formula) against the COS price across 13 strikes. Expected: agreement within 2 standard
  errors, and a standard error 5–20× below plain MC (computed). Then ρ forced to 0 to show the symmetric smile.
- **Pause-and-predict.** "Double the vol of vol, ρ = 0. Which moves more: the ATM vol or the 25-delta wings?" (The wings
  rise, ATM falls slightly.)
- **Compute.** `mixing` (1 min).

### 3 · Heston I: the characteristic function, derived (3.2) · item 2 · `s03_heston` (kept: `model`, `rivers`; `fit`, `qe` move)
- **Goal.** Derive Heston's CF in full. See why affine models are solvable. Meet the branch-cut trap.
- **Beats.**
  1. Keep the two-rivers QE paths.
  2. **Visual (3D), the CF as an object.** φ(u) for the fitted model, drawn as a curve in (u, Re φ, Im φ) space: a helix
     spiralling into the axis. The camera orbits. Slower decay means fatter tails; the twist is the skew (ρ).
  3. Then the derivation ladder.
  4. **Visual, the little trap.** Down to the complex plane. The point $z(u) = (1-g e^{dT})/(1-g)$ of Heston's original
     form is traced as u sweeps 0 → 20 at T = 1. It winds around the origin and crosses the negative real axis (lit red),
     so the principal log jumps by 2πi and φ is discontinuous. Albrecher et al.'s form $(1-g' e^{-dT})/(1-g')$ stays in
     the right half-plane.
  5. **Lab 1** `stochvol.heston_cf` (12 lines; the `d`, `g`, `C`, `D` lines highlighted). Run: the Fang–Oosterlee
     benchmark to 10⁻⁸ (existing test), and the original form's failure on our own fit.
- **Derivation.**
  - $x = \ln S$, $\tau = T - t$, $f = \mathbb E[e^{iux_T}\mid x, v]$ solves $f_\tau = \tfrac12 v(f_{xx}-f_x) + \rho\xi v f_{xv} + \tfrac12\xi^2 v f_{vv} + \kappa(\theta - v)f_v$ (Feynman–Kac, Part 5).
  - Ansatz $f = \exp(C(\tau) + D(\tau)v + iux)$ (the coefficients are affine in $v$: Duffie–Pan–Singleton 2000).
  - Collect the terms in $v$: $D' = \tfrac12\xi^2D^2 - (\kappa - \rho\xi iu)D - \tfrac12(u^2+iu)$, $D(0)=0$ (a Riccati equation).
  - Collect the constant terms: $C' = \kappa\theta D$, $C(0) = 0$.
  - The roots of the quadratic are $D_\pm = (b\pm d)/\xi^2$, with $b = \kappa - \rho\xi iu$ and $d = \sqrt{b^2 + \xi^2(u^2+iu)}$, so $D = \frac{b-d}{\xi^2}\frac{1-e^{-d\tau}}{1-g e^{-d\tau}}$, $g = \frac{b-d}{b+d}$ (separate variables, partial fractions).
  - $C = \frac{\kappa\theta}{\xi^2}\big[(b-d)\tau - 2\ln\frac{1-ge^{-d\tau}}{1-g}\big]$ (integrate $D$).
  - With this choice $|ge^{-d\tau}| < 1$, so the log never crosses its branch cut (Kahl–Jäckel 2005; Albrecher et al. 2007). Prices then follow from one Fourier integral (COS; derived in Part 16).
- **Experiment.** `trap` (new). **(probe)** On the fitted Heston, the original form disagrees with the little-trap form:
  * at T = 1 from u ≈ 1.69, where |φ| = 0.68 is far from negligible (1,824 of 6,000 grid points wrong on u ∈ (0, 60]);
  * at T = 3 from u ≈ 0.51;
  * at T = 0.25 nowhere.

  For textbook parameters (κ = 1.5, ξ = 1, ρ = −0.7) it holds to T = 1 and fails at T = 3. Compute the resulting
  price error (naive CF with non-finite values zeroed) against COS.
- **Pause-and-predict.** "Is Heston's ln S_T normal given the variance path?" (Only if ρ = 0: ch2.)
- **Compute.** `trap` (<0.1), `calibrate` (exists).

### 4 · Heston II: what each parameter does, and the fit (3.0) · item 2 · `s03a_hestonfit` (new; from `s03_heston.fit`)
- **Goal.** Read each parameter off the surface. Derive the short-maturity skew. Watch the fit converge.
- **Beats.**
  1. **Visual (3D), sliders.** The model surface σ(k, T) is drawn with `price_surface`, the Surface's 193 quotes are
     dots (`smile_points3d`), and five sliders are moved one at a time (morphs):
     * v₀ lifts the short end;
     * θ lifts the long end;
     * κ sets how fast one becomes the other;
     * ρ rotates every smile;
     * ξ bends every smile and tilts the short end more.
  2. **Replay**: the Heston calibration scrubbed through its evaluations. Left, the model surface morphs onto the dots.
     Right, the RMSE curve. Three starts as a band.
  3. The fitted table (keep). The 3-day slice is still missed by 5.3 points.
- **Derivation** (the short-T skew; README problem 2 brought on screen):
  - As $T\to0$, $\sigma^2_{\text{imp}}(k)\approx$ the average of local variance along the straight line from 0 to $k$ (Berestycki–Busca–Florent).
  - Local variance $=\mathbb E[v\mid x]$, with $v - v_0 \approx \xi\sqrt{v_0}W^2$ and $x \approx \sqrt{v_0}W^1$, so $\mathbb E[v\mid x] \approx v_0 + \rho\xi x$ (Gaussian regression).
  - $\sigma^2_{\text{imp}}(k) \approx v_0 + \tfrac12\rho\xi k$ (average a line), so $\partial_k\sigma_{\text{imp}}\big|_0 = \rho\xi/(4\sqrt{v_0})$ (differentiate $\sqrt{\cdot}$).
  - The curvature is $\propto \xi^2(1 - \tfrac{7}{4}\rho^2)/v_0^{3/2}$ to leading order *(verify the constant against Gatheral ch. 3 before it goes on screen; otherwise say "∝ ξ²")*. For large $T$ mean reversion damps both by $(1 - e^{-\kappa T})/\kappa T$.
- **Experiment.**
  * `heston_replay` (new): `calibrate(trace=True)` from the default start and two random starts. **(probe)** Their
    calibrator RMSE goes 3.24 / 25.4 / 22.7 → 1.296 for all three, in 120 / 108 / 90 evaluations (4–5 s each).
  * `skew` (exists): the formula gives ρξ/(4√v₀) = −0.731 and the model at 2 days −0.737 (cached).
- **Hands-on.** The replay, and the sliders run live through `surface_iv`. Precompute the grids in `heston_sliders`
  (5 parameters × 9 values × 9 expiries).
- **Pause-and-predict.** "Make ρ positive. What happens to the 3-day skew?" (It flips to a call skew; for BTC in 2023 that
  was not absurd.)
- **Compute.** `heston_replay` (0.5), `heston_sliders` (0.5).

### 5 · Heston III: Feller, and simulating it honestly (2.8) · item 2 · `s03b_simulate` (new; `qe` from `s03_heston`)
- **Goal.** Why naive schemes fail when Feller fails. Andersen's QE derived by moment matching. The exact and
  2024 alternatives.
- **Beats.**
  1. **Live.** One step of the variance from v = 0.05 (near zero), with Δ = 1/52. 100,000 draws fill three
     histograms side by side, against the exact non-central χ² density (white curve):
     * Euler (with a red mass below zero, then truncated);
     * QE (the spike at zero plus the exponential tail);
     * QE on the quadratic branch at v = 0.5.
  2. Feller's condition (0.37 on our fit): Part 5's boundary test in one line, with the variance paths touching zero.
  3. **Lab 2** `stochvol.heston_qe`: the 12 lines of the ψ switch and both branches. Run: the existing bias table, with
     Euler at 2 steps 20% too high and QE −1%.
  4. Card: Broadie–Kaya (2006) exact simulation; Choi–Kwok (2024), Poisson conditioning (frontier). Moment explosions
     (Andersen–Piterbarg 2007): for large strikes E[S^p] blows up in finite time. That is the link to Lee's formula
     (Part 12).
- **Derivation.**
  - $m = \theta + (v-\theta)e^{-\kappa\Delta}$ and $s^2 = \frac{v\xi^2e^{-\kappa\Delta}}{\kappa}(1-e^{-\kappa\Delta}) + \frac{\theta\xi^2}{2\kappa}(1-e^{-\kappa\Delta})^2$ (the exact conditional moments of CIR).
  - $\psi = s^2/m^2$. If $\psi\le\psi_c$: $v' = a(b+Z)^2$, $b^2 = \frac2\psi - 1 + \sqrt{\frac2\psi}\sqrt{\frac2\psi-1}$, $a = \frac{m}{1+b^2}$ (match the mean and variance of a scaled non-central χ² with one degree of freedom).
  - Else $v' = 0$ with probability $p = \frac{\psi-1}{\psi+1}$, otherwise Exp with rate $\beta = \frac{1-p}{m}$ (match two moments with a mass at zero).
  - $\ln S' = \ln S + \frac\rho\xi(v'-v-\kappa\theta\Delta) + (\frac{\kappa\rho}{\xi}-\frac12)\int v + \sqrt{1-\rho^2}\int\sqrt v\,dW^\perp$ (solve the $v$ equation for $\int\sqrt v\,dW^2$), with the trapezoid for $\int v$. That gives $K_0\ldots K_4$, and $K_0^*$ makes $S$ a martingale exactly.
- **Experiment.**
  * `qe` (exists).
  * `qe_density` (new): KS distance to the exact one-step law for Euler-truncated and QE at Δ ∈ {1/365, 1/52, 1/12},
    started at v ∈ {0.05, θ, 0.5}. Expected: QE's distance is small everywhere and Euler's large near zero (computed).
- **Pause-and-predict.** "Feller holds. Is Euler then fine?" (Better, but still biased; QE's advantage is largest when
  Feller fails.)
- **Compute.** `qe` (exists, ~3), `qe_density` (0.5).

### 6 · SABR I: Hagan's formula and the backbone (3.0) · item 3 · `s04_sabr` (kept: `model`, `slices`, `backbone`)
- **Goal.** The model of the rates desks. What the expansion says, term by term. How the smile moves with the forward.
- **Beats.**
  1. **Replay**: the nine slice fits sweep across expiries in turn. Each slice's least-squares iterates morph the
     curve onto its quotes, its (α, ρ, ν) dot lands on three small parameter panels, and the ν dots line up on a
     log–log line of slope −0.49.
  2. **Visual (3D)**: the nine fitted smiles assembled into a ribbon surface over (k, T).
  3. Backbone: the forward slides left and right. The ATM point rides along F^{β−1}, while the smile slides with F
     (β = 1, sticky delta) or drags against it (β = 0). Contrast with LV's wrong-way backbone (Part 12 ch8; Hagan et
     al.'s motivation).
- **Derivation.**
  - $dF = \alpha F^\beta dW$, $d\alpha = \nu\alpha\,dZ$, $dW\,dZ = \rho\,dt$ (definition; CEV with stochastic scale).
  - For $\beta = 1$: $\sigma_B(K) \approx \alpha\,\frac{z}{x(z)}\big[1 + (\tfrac14\rho\nu\alpha + \tfrac{2-3\rho^2}{24}\nu^2)T\big]$, $z = \frac\nu\alpha\ln\frac FK$, $x(z) = \ln\frac{\sqrt{1-2\rho z+z^2}+z-\rho}{1-\rho}$ (singular perturbation, Hagan et al. 2002; quoted, with the one-line idea: an effective local volatility along the most likely path).
  - $\frac{z}{x(z)} = 1 - \frac\rho2 z + \frac{2-3\rho^2}{12}z^2 + O(z^3)$ (expand $x$ at 0).
  - So with $k = \ln(K/F)$: $\partial_k\sigma|_0 \approx \rho\nu/2$ (the skew is ρ times vol of vol) and $\partial^2_k\sigma|_0 \approx \frac{(2-3\rho^2)\nu^2}{6\alpha}$ (curvature from ν²).
  - Backbone: $\sigma_{ATM}(F) \approx \alpha F^{\beta-1}$ (leading order).
- **Experiment.** `calibrate` (exists: 0.38 points, 27 parameters, ν ∝ T^−0.49); `sabr` (exists); `sabr_replay` (new:
  stored iterates per slice).
- **Pause-and-predict.** "Each slice's ν falls like T^−½. What does one global SABR do at 3 days?" (It underfits the short
  skew: the same diagnosis as Heston, and Part 14's doorway.)
- **Compute.** `sabr_replay` (0.2).

### 7 · SABR II: negative densities and the fixes (2.6) · item 3 · `s04a_sabrfix` (new; `density` from `s04_sabr`)
- **Goal.** Where the expansion breaks, how desks repaired it, and how to hedge with it.
- **Beats.**
  1. Keep the 10-year density (minimum −130, mass 0.63, negative below a 0.7% strike).
  2. **Live**: the **arbitrage-free SABR** density solved forward in T by the effective PDE. The density surface grows
     in 3D over (F, T), stays non-negative and keeps mass 1, with the absorbed mass accumulating as a bar at F = 0. It
     is drawn against Hagan's density sheet going negative.
  3. Cards:
     * Obłój (2008), the corrected leading term;
     * Antonov–Konikov–Spector (2015), free-boundary SABR for negative rates;
     * shifted and normal SABR (rates below zero, 2015–2021).
  4. **Bartlett's delta**: the SABR delta includes the α move correlated with F.
     $\Delta_{\text{B}} = \partial_F V + \partial_\sigma V\big(\partial_F\sigma_B + \partial_\alpha\sigma_B\,\frac{\rho\nu}{F^\beta}\big)$, which leads into ch17's real-data minimum-variance delta.
- **Derivation.**
  - Arbitrage-free SABR: $\partial_T Q = \tfrac12\partial_F^2\big(D^2(F)E(T,F)Q\big)$, with absorbing boundary at $F = 0$ (Hagan et al. 2014; the effective forward equation integrated over α).
  - $D(F) = \sqrt{\alpha^2 + 2\alpha\rho\nu y + \nu^2y^2}\,F^\beta$, $y = \frac{F^{1-\beta}-f^{1-\beta}}{1-\beta}$ *(verify the exact form and E(T, F) against the 2014 paper before coding)*.
  - Mass conservation: $\frac{d}{dT}\big(\int_0^\infty Q\,dF + Q_L + Q_R\big) = 0$ (flux into the boundary bars).
- **Experiment.** `sabr_pde` (new): a finite-volume Crank–Nicolson scheme, 400 nodes, for the rates-like example (F = 3%,
  β = ½, ρ = −0.3, ν = 0.4, α = 0.035, T = 10). Expected: the density is ≥ 0, mass 1 to 10⁻⁸, and the ATM vol matches
  Hagan to a few bp (computed).
- **Pause-and-predict.** "Hagan's 10-year density integrates to 0.63. Where did the rest go?" (Into negative densities
  and missing tail: the formula is not a distribution.)
- **Compute.** `sabr_pde` (1).

### 8 · Jumps: Merton, Kou and Bates (3.0) · item 4 · `s05_jumps` (kept: `models`, `scores` reduced to jump models)
- **Goal.** Price with jumps exactly (the Merton series). Fit three jump models. Learn what the Surface's verdict means.
- **Beats.**
  1. **Visual, the Merton layer cake.** The terminal density is built as a Poisson-weighted sum of normals: layer n = 0
     (no jump, weight e^{−λT}), n = 1, 2, … appear with weight bars. The call price stacks the matching BS prices. A λ
     slider moves mass between the layers.
  2. Kou: double-exponential jumps; the memoryless overshoot gives barrier closed forms (Kou–Wang 2004, card).
  3. Bates CF = Heston × the jump factor (independence).
  4. The fits table. **Replay**: the Bates calibration, with λ climbing to its bound of 20 and σ_J falling to its
     floor while the RMSE barely moves. The jumps became "a second diffusion".
  5. Cards:
     * jump to default (Gatheral 6) → Part 20;
     * SVCJ, with jumps in volatility (Duffie–Pan–Singleton 2000; Eraker–Johannes–Polson 2003; Broadie–Chernov–Johannes
       2007);
     * Hou et al. (2020): on BTC, an SVCJ fit finds anti-correlated jumps in returns and variance.
- **Derivation.**
  - $\frac{dS}{S_-} = (r - \lambda\bar k)dt + \sigma dW + (e^J - 1)dN$, $\bar k = e^{\mu_J+\sigma_J^2/2}-1$ (compensate so that $e^{-rt}S$ is a martingale).
  - Given $N_T = n$: $\ln S_T \sim N\big(\ln S_0 + (r - \lambda\bar k - \tfrac12\sigma^2)T + n\mu_J,\ \sigma^2T + n\sigma_J^2\big)$ (a sum of independent normals).
  - $C = \sum_{n\ge0} e^{-\lambda'T}\frac{(\lambda'T)^n}{n!}\,C_{BS}(S_0,K,T,\sigma_n,r_n)$, $\lambda' = \lambda(1+\bar k)$, $\sigma_n^2 = \sigma^2 + n\sigma_J^2/T$, $r_n = r - \lambda\bar k + n\ln(1+\bar k)/T$ (condition on $n$, then Poisson-weight; Merton 1976).
  - $\varphi_{\text{Bates}} = \varphi_{\text{Heston}}\cdot\exp\big(\lambda T(e^{iu\mu_J - \frac12\sigma_J^2u^2} - 1 - iu\bar k)\big)$ (independent factors multiply).
- **Experiment.** `levy_fits` (new; shared with ch9), with Merton, Kou and CGMY added to the calibrator. **(probe)**
  * **Merton** (σ, λ, μ_J, σ_J): 2.16 vol points. Its jumps are rare and huge: λ = 0.25 a year, mean −49%, σ_J = 45%. The
    3-day expiry is missed by 9.2.
  * **Kou**: 2.41 points (λ = 1.7, p = 0.56, η₁ = 25.6, η₂ = 3.8).
  * **Bates** (exists): 1.31, λ = 20 (the bound), μ_J = −3.8%, σ_J = 1% (its floor).

  Narration: *with stochastic volatility present, the optimizer spends the jumps on the body of the smile; without it,
  they become a crash insurance tail.* This is computed and branches on the fitted values. `bates_replay` (new): Bates
  `calibrate(trace=True)`, 3 starts.
- **Pause-and-predict.** "Merton with λ = 0.25 a year. Probability of no jump before a 3-day option expires?"
  (e^{−0.25·3/365} ≈ 99.8%.)
- **Compute.** `levy_fits` (1.5), `bates_replay` (0.5).

### 9 · Lévy models and time changes (3.0) · item 5 · `s05a_levy` (new; `levy` from `s05_jumps`)
- **Goal.** Build pure-jump models by changing the clock. Derive VG's CF. Read CGMY's fine structure. Unify with SV
  (Carr–Wu).
- **Beats.**
  1. **Live, the gamma clock.** A Brownian path is drawn in business time. Then the calendar axis is warped by gamma
     increments: stretches where the clock ran fast collapse into jumps, and quiet stretches flatten. The VG path
     appears from the same Brownian path.
  2. **Visual, the fine structure.** The CGMY Lévy density $C e^{-G|x|}/|x|^{1+Y}$ is drawn with a Y slider from −0.5 to
     1.8, and a matching simulated path redraws:
     * a few big jumps (Y < 0, finite activity);
     * a swarm of small ones (0 < Y < 1);
     * diffusive fuzz (1 < Y < 2).
  3. **Lab 3** `stochvol.vg_cf` + `vg_paths` (10 lines). Run: the COS price of a 30-day ATM call against 200,000 VG
     paths (agreement within 2 se, computed).
  4. Fits board: VG 2.89, NIG 2.70, CGMY 2.50 (probe). Carr–Wu card: a Lévy process on a CIR clock is stochastic
     volatility with jumps.
- **Derivation.**
  - $X_t = \theta G_t + \sigma W_{G_t}$, $G_t\sim\Gamma(t/\nu,\ \nu)$ (Brownian motion on a gamma clock; Madan–Seneta 1990).
  - $\mathbb E[e^{iuX_t}\mid G_t] = e^{G_t(iu\theta - \frac12\sigma^2u^2)}$ (Gaussian given the clock).
  - $\mathbb E[e^{sG_t}] = (1-\nu s)^{-t/\nu}$ (the gamma mgf), so $\varphi(u) = (1 - iu\theta\nu + \tfrac12\sigma^2\nu u^2)^{-t/\nu}$.
  - $\omega = \frac1\nu\ln(1-\theta\nu - \tfrac12\sigma^2\nu)$, added to the drift so $\varphi(-i) = 1$ (martingale correction).
  - CGMY: $\psi(u) = C\Gamma(-Y)\big[(M-iu)^Y - M^Y + (G+iu)^Y - G^Y\big]$ (integrate $e^{iux}-1$ against the density); VG is $Y = 0$, $C = 1/\nu$.
  - Time change: $\mathbb E[e^{iuL_{T_t}}] = \mathbb E[e^{T_t\psi_L(u)}]$, which is the Laplace transform of the clock $T_t = \int_0^t v_s\,ds$. For a CIR clock that is Heston's affine formula again (Carr–Wu 2004; a measure change handles the correlation).
- **Experiment.** `levy_fits` (above). **(probe)** CGMY with Y ∈ [0.1, 0.95] hits the bound Y = 0.95 (2.65 points). With
  Y ∈ [1.05, 1.95] it settles at Y = 1.64 (2.50 points; C = 0.071, G = 0.69, M = 11.4). The Surface asks for
  *infinite variation*, which is diffusion-like (computed; branch). `lab_vg` (new, 0.3).
- **Pause-and-predict.** "VG has no Brownian part. Can its paths look continuous?" (On a chart, yes: infinitely many
  small jumps.)
- **Compute.** `lab_vg` (0.3).

### 10 · The skew across maturities: what each model can do (2.8) · items 2, 4, 5 · `s05b_skew` (new; `slices`, `skew` from `s05_jumps`)
- **Goal.** One picture that sorts every model by its skew term structure. It ends at Part 14's door.
- **Beats.**
  1. **Visual, live.** A maturity slider sweeps T from 1 year down to 2 days. Small multiples of each model's smile
     morph at once (Heston, Bates, Merton, VG, NIG, CGMY, SABR slices). On a log–log panel each model's ATM skew dot
     traces its curve, with the market's nine points fixed:
     * Heston flattens to ρξ/(4√v₀);
     * the Lévy models steepen like 1/T over two weeks to a year (cached local slopes: VG −1.0, NIG −0.56 → −0.99);
     * the market sits at T^−0.49.
  2. Card: additive/Sato processes (Carr–Geman–Madan–Yor 2007; Cont–Tankov ch. 14) repair the Lévy term structure.
  3. Abi Jaber–De Carvalho (2023): fast mean reversion and huge vol of vol make Heston imitate jumps. Our fit (κ = 14.8,
     ξ = 4.6) sits in that regime (→ ch18).
- **Derivation.**
  - For an exponential Lévy model the cumulants scale with T: $c_n(T) = c_nT$. So the skewness is $\gamma_1(T) = \gamma_1(1)/\sqrt T$ (cumulant scaling).
  - $\sigma(k)\approx\sigma_T\big(1 + \frac{\gamma_1(T)}{6\sigma_T\sqrt T}k\big)$ (Gram–Charlier to first order; *verify the normalisation*), so skew ∝ $\gamma_1(T)/\sqrt T \propto 1/T$.
  - Diffusive SV: the skew → $\rho\xi/(4\sqrt{v_0})$, a constant (ch4), and is damped by $(1-e^{-\kappa T})/\kappa T$ beyond $1/\kappa$.
  - Neither gives $T^{-1/2}$ over a decade: Part 14 explains why with the kernel derivation, so say it there.
- **Experiment.** `skew` (exists), extended with Merton, Kou, CGMY and the SABR slices (0.5). The local slopes on
  2–14 days and 60–365 days are printed per model. **The narration states the computed slopes**, not "1/T" as a slogan
  (cf. Part 14's lead decision).
- **Pause-and-predict.** "A model's skew is constant as T → 0. Can it fit a 3-day expiry?" (Only with an enormous ξ:
  ch4's κ = 14.8, ξ = 4.6.)
- **Compute.** `skew` (+0.5).

### 11 · Stochastic local volatility: the particle method (3.0) · item 6 · `s06_slv` (kept, deepened)
- **Goal.** A model that fits today exactly and moves plausibly. The McKean–Vlasov loop, and how particles cut it.
- **Beats.**
  1. **Live (the signature).** 4,000 particles in the (x = ln S, v) plane advance step by step. At each step a kernel
     window slides along x and the conditional mean E[v | x] is drawn as a gold curve through the cloud. The leverage
     L(x, t) = σ_loc/√E[v | x] is then computed. It is deposited as one slice of a 3D leverage surface over (x, t) that
     grows behind the cloud, and the camera turns to show it. Each particle's next step uses that slice.
  2. **Lab 4** `stochvol.slv_paths` (new House function, moved out of `compute._simulate`): the 12-line step (kernel,
     L, update). Run: the repricing table (0.44–0.69 points, cached).
  3. **Replay**: repricing error against the number of particles N ∈ {2k, 8k, 40k} and bandwidths, with 3 seeds as
     bands.
  4. Cards:
     * Gyöngy (Part 12 ch7, recalled in one line);
     * the PDE route (Ren–Madan–Qian 2007; Lipton 2002);
     * Reisinger–Tsianni (2025): propagation of chaos for this exact particle system, strong rate ½ (frontier).
- **Derivation.**
  - $\frac{dS}{S} = L(S,t)\sqrt{v_t}\,dW^1$, $\sigma^2_{\text{loc}} = L^2\,\mathbb E[v_t\mid S_t = S]$ (Gyöngy: matching marginals).
  - $L$ depends on the law of $(S_t, v_t)$, which depends on $L$: a McKean–Vlasov SDE (nonlinear in the sense of McKean).
  - $\mathbb E[v\mid S]\approx\frac{\sum_i v^i K_h(S^i - S)}{\sum_i K_h(S^i - S)}$ (Nadaraya–Watson over the particles themselves), $h = 1.06\,\hat\sigma N^{-1/5}$ (Silverman).
  - The error has a bias of $O(h^2)$ and a variance of $O(1/(Nh))$, so $h\propto N^{-1/5}$ balances them (kernel regression), and the error falls like $N^{-2/5}$ *(state as the heuristic it is)*.
- **Experiment.** `slv` (exists). `slv_particles` (new): N ∈ {2,000; 8,000; 40,000} × 3 seeds, 120 days, repricing RMSE
  at 30/60/90/120 days. Expected: falling with N, with a floor from the time step (computed). This is the part's
  largest numpy job.
- **Pause-and-predict.** "Set the vol of vol to zero. What is L?" (σ_loc/√v: SLV collapses to LV.)
- **Compute.** `slv` (exists, ~3), `slv_particles` (12).

### 12 · The mixing fraction: between two worlds (2.6) · items 6, 8 · `s06a_mixfrac` (new)
- **Goal.** One dial, η (the share of the vol of vol kept from Heston), moves every exotic while every vanilla stays
  fixed.
- **Beats.**
  1. **Visual, the dial.** η slides 0 → 1. Three panels morph together:
     * the leverage surface (steep at η = 1, flat at η = 0, where L = σ_loc/√v₀ is all LV);
     * the 30-day forward smile in 60 days (flat for LV, skewed for SV);
     * the cliquet price bar.
     The repricing-error readout stays under one vol point throughout. That is the point: vanillas cannot see η.
  2. Industry: FX desks pick η from barrier and no-touch prices, which *do* see it. Sources: Clark, *Foreign Exchange
     Option Pricing* (2011); the Bloomberg SLV note (Tataru–Fisher 2010, cited by later papers; *(unverified: not
     fetched)*).
- **Derivation.** $\xi_\eta = \eta\,\xi$, $L_\eta^2\,\mathbb E_\eta[v\mid S] = \sigma^2_{\text{loc}}$ for every η (Gyöngy holds for each). The forward smile's skew is roughly $\propto$ the spot–vol covariance at the forward date, which scales with $\eta\xi$ (ch2's tilt). So the cliquet is monotone in η, to first order (computed check).
- **Experiment.** `mixing_sweep` (new): η ∈ {0, 0.25, 0.5, 0.75, 1}, 40,000 particles each, one seed (3 seeds at η = ½).
  For each: the repricing error, the forward ATM vol and skew, the cliquet and the forward-start price. Expected:
  monotone from LV toward Heston (computed; branch if not).
- **Pause-and-predict.** "Which exotic is most sensitive to η: a 1-year European, a forward-start, or a cliquet?" (The
  cliquet; the European not at all.)
- **Compute.** `mixing_sweep` (15).

### 13 · Bergomi: forward variance as the state (3.0) · item 7 · `s07_bergomi` (kept: `curve_`, `model`; deepened)
- **Goal.** Make the whole variance curve the state. See its vol-of-vol term structure. Link the static smile to its
  dynamics (SSR).
- **Beats.**
  1. Keep the market curve (the weekend dip).
  2. **Visual (3D), the curve in motion.** The forward variance curve ξ_t(T) is simulated by the 2-factor model from the
     Surface's ξ₀ and drawn as a ribbon over (t, T) as t advances day by day. The front end whips, the long end barely
     moves, and each slice stays a martingale (its average over 2,000 paths is drawn as a still line). Then the same
     with Heston: the whole curve moves as one exponential, because one κ does two jobs.
  3. **SSR**: a dial reads $R = \frac{d\sigma_{ATM}/d\ln S}{\text{skew}}$ for Heston by maturity. **(probe)** 1.93 at 2
     days, 1.87 at 30 days, 1.58 at 90, 1.20 at 1 year. Against it, LV's ≈ 2 (Part 12 ch8) and Part 12's measured BTC
     SSR (forward reference).
- **Derivation.**
  - $\xi_t(T) = \mathbb E_t^Q[v_T]$ is a $Q$-martingale in $t$ (tower property); it is the rate of a forward-starting variance swap.
  - $\xi_t(T) = \xi_0(T)\exp\big(\omega x^T_t - \tfrac{\omega^2}2\operatorname{Var}x^T_t\big)$, $x^T_t = \alpha_\theta\big[(1-\theta)e^{-k_1(T-t)}X^1_t + \theta e^{-k_2(T-t)}X^2_t\big]$, $dX^i = -k_iX^i\,dt + dW^i$ (Bergomi 2005; a lognormal martingale; *verify the α_θ normalisation against Bergomi ch. 7*).
  - The instantaneous vol of $\xi_t(T)$ is $\omega\alpha_\theta\sqrt{(1-\theta)^2e^{-2k_1\tau} + \theta^2e^{-2k_2\tau} + 2\rho_{12}\theta(1-\theta)e^{-(k_1+k_2)\tau}}$ (Itô; τ = T − t): the vol-of-vol term structure, set independently of today's curve.
  - Heston: $d\xi_t(T) = e^{-\kappa\tau}\,\xi\sqrt{v_t}\,dW^2$ (differentiate $\theta + (v-\theta)e^{-\kappa\tau}$), so a single exponential, with the same κ that shapes $\xi_0(\cdot)$.
  - SSR at short $T$: $\mathbb E[dv\mid d\ln S] = \rho\xi\,d\ln S$ (regression of the two Brownian increments) and $\sigma_{ATM}\approx\sqrt v$, so $d\sigma_{ATM} = \frac{\rho\xi}{2\sqrt v}d\ln S$. With ch4's skew $\frac{\rho\xi}{4\sqrt v}$, $R\to 2$.
- **Experiment.** `bergomi` (exists). `bergomi_sim` (new): 2,000 curves × 120 days with Bergomi's typical parameters,
  labelled illustrative (k₁ = 8, k₂ = 0.35, θ = 0.25, ρ₁₂ = 0, ω = 2.8 *(take from Bergomi ch. 7's example: verify)*).
  Part 14 calibrates the 2-factor model, so it is not calibrated here. `ssr` (new; COS finite differences).
- **Pause-and-predict.** "A one-year variance swap and a one-week one: whose rate is more volatile?" (The one-week:
  vol of vol decays with τ.)
- **Compute.** `bergomi_sim` (0.5), `ssr` (<0.1).

### 14 · Forward smiles and cliquets (2.8) · item 8 · `s08_forward` (kept: `smiles`, `exotics`; `puzzle` moves to ch15)
- **Goal.** Price claims on the future smile. Show why the models disagree, mechanically.
- **Beats.**
  1. **Live**: the forward smile (30 days, starting in 60) under each model, built from its MC paths. The smile's points
     settle as paths accumulate (`seed_band` across 3 seeds). Today's smile is drawn fixed for comparison: LV flattens to
     3.4 points of skew against 6.5 today; VG keeps today's shape.
  2. **Visual, the cliquet.** Four monthly coupons. Each period's return is drawn as a bar clipped by the cap line (10%)
     and the floor (0). The coupons stack into the payoff, and the price per model is shown as a bar. Then the
     mechanism: a cliquet is a strip of forward-start call spreads, so it is priced off forward smiles, which no vanilla
     pins down.
- **Derivation.**
  - $(S_{T_2}/S_{T_1} - e^k)^+$ is homogeneous of degree 0 in $S_{T_1}$, so its time-$T_1$ value is $C(1, e^k, \tau; \text{state}_{T_1})$ (scaling).
  - Lévy: the state is irrelevant, so the forward smile equals today's τ-smile (independent stationary increments; README problem 3).
  - Heston: $\text{price} = \mathbb E\big[C_H(1, e^k, \tau; v_{T_1})\big]$ with $v_{T_1}\sim c\,\chi'^2_d(\lambda)$, a one-dimensional integral against the CIR law (tower + ch5's transition).
  - Cliquet: $\sum_i\min(\max(r_i, f), c) = \sum_i\big[f + (r_i - f)^+ - (r_i - c)^+\big]$ (each coupon is a forward-start call spread).
- **Experiment.** `exotics` (exists: the cliquet at 13.73% LV, 13.12% Heston, 13.32% Bates, 14.17% VG, 13.67% SLV; spread
  7.8%). `fwd_semi` (new): the Heston forward smile by the 1D integral (COS inside) against the MC forward smile.
  Expected: within MC error (a Rule 6 check, computed).
- **Pause-and-predict.** "In which model is a forward-start option worth exactly today's option?" (Any exponential
  Lévy model.)
- **Compute.** `fwd_semi` (0.5), `exotics` (exists, ~6).

### 15 · The SPX/VIX puzzle, measured on Bitcoin (2.8) · item 9 · `s08a_puzzle` (new; cards from `s08_forward.puzzle`)
- **Goal.** State the puzzle precisely. Measure its Bitcoin version: the smile asks for a vol of vol that DVOL does not
  have.
- **Beats.**
  1. The history cards (keep): Cboe VIX futures 26 March 2004, VIX options 24 February 2006; Gatheral (2008); Cont and
     Kokholm (2013), whose jumps decouple the two; Guyon (2020) → Part 14.
  2. **Visual, two rivers again.** The fitted Heston's own 30-day vol index, simulated (gold), runs beside the real DVOL
     (orange), with the histograms of daily log changes filling at the side. The model's histogram is about twice as
     wide.
  3. The Jensen gap drawn as the concave √ under a spread of VIX² values.
  4. Then the Heston vol-index option smile (computed).
- **Derivation.**
  - $\text{VIX}^2_T = \mathbb E_T\big[\tfrac1\tau\int_T^{T+\tau}v_s\,ds\big] = \theta + (v_T-\theta)\frac{1-e^{-\kappa\tau}}{\kappa\tau}$ (Heston is affine: integrate ξ_T(·)).
  - $\mathbb E[\text{VIX}_T] \le \sqrt{\mathbb E[\text{VIX}^2_T]}$ = the forward variance-swap rate, which the spot smile fixes (Jensen). The gap is the variance of VIX, so the vol of vol is priced by VIX futures and options.
  - A change to an equivalent measure alters drifts, never diffusion coefficients (Girsanov, Part 5). So ξ fitted under $Q$ is the vol of vol under $P$ too. That makes the model's implied volatility of its own vol index testable against history.
  - The puzzle (Guyon's statement, verified from his 2020 slides): for continuous models, fitting the short SPX skew needs a large vol of vol, which then makes the model's ATM VIX implied vol too high. Fitting VIX breaks SPX.
- **Experiment.** `vol_puzzle` (new). **(probe)** Under the fitted Heston:
  * the model's 30-day vol index has a realized vol of vol of **193% a year**, against DVOL's **89%**;
  * options on that index would trade at an ATM implied vol of 125% (30 days; 74% at 90 days), with a hard floor of 33.6%
    (the √(θ(1−b)) floor);
  * the model's return/vol-index correlation is −0.25, against DVOL's −0.23. The tilt is right; the size of the vol of
    vol is twice too big.

  Same direction as the SPX/VIX puzzle. Repeat for Bates (computed). Narration branches on the ratio. Caveat on screen:
  the BTC version compares Q-dynamics with P-history; the measure-invariance of ξ is what makes this legitimate within
  the model.
- **Pause-and-predict.** "Can the VIX future trade above the 30-day variance-swap vol?" (No: Jensen.)
- **Compute.** `vol_puzzle` (1).

### 16 · Calibration: landscapes, identifiability, instability (3.2) · item 10 · `s09_calibration` (kept: `landscape`, `history`; deepened)
- **Goal.** Calibration as an ill-posed inverse problem. Measure identifiability. Regularise. Watch two years of
  refits.
- **Beats.**
  1. Keep the 3D landscape and valley.
  2. Add the Hessian at the optimum: its eigenvectors are drawn as two arrows on the floor, the long one along the
     valley, and its condition number is printed.
  3. **Replay, 100 weeks.** The weekly recalibration scrubbed week by week: the (κ, ξ) dot wanders along the valley, and
     the five parameter series draw themselves with RMSE beneath.
  4. Then **regularised**, the same 100 weeks with a Tikhonov pull toward last week. Dots for λ ∈ {0, λ₁, λ₂} trace a
     frontier of "median weekly parameter change" against "median fit error". Cont–Tankov (2004): relative-entropy
     regularisation for jump models.
  5. **Lab 5** `stochvol.calibrate_reg` (new, 10 lines: the residual vector stacked with $\sqrt\lambda\,W(x - x_{\text{prev}})$).
- **Derivation.**
  - $\hat x = \arg\min\tfrac12\|r(x)\|^2$, $H \approx J^\top J$ (Gauss–Newton).
  - Near the optimum, $\delta L \approx \tfrac12\delta x^\top H\delta x$, so a small eigenvalue means a flat direction: the data pin $v_{\text{top}}^\top\delta x$, not each coordinate (the valley).
  - $\operatorname{Cov}(\hat x) \approx \hat\sigma^2 H^{-1}$ (local linearisation), so the parameter standard errors are printed.
  - Regularised: $\min\tfrac12\|r(x)\|^2 + \tfrac\lambda2\|W(x - x_{\text{prev}})\|^2$, which shifts each eigenvalue by λ (ridge) and stabilises the flat direction at little cost in fit.
- **Experiment.**
  * `landscape`, `history` (exist: median weekly |Δlog κ| 25%, ξ ranging 1.1–6, κ 0.08–20).
  * `hessian` (new; finite-difference J at the optimum, <0.2).
  * `history_reg` (new): 2 λ values × 100 weeks. Expected: parameter changes fall by a large factor for an RMSE increase
    of a few hundredths of a point (computed; branch).
- **Pause-and-predict.** "Overnight κ jumped from 3 to 20 and the fit barely moved. Which prices changed?" (Vanillas
  hardly; forward-starts and hedges a lot.) This was a desk question; it moves here.
- **Compute.** `hessian` (0.2), `history_reg` (20).

### 17 · Industry: who builds these models, and how desks judge them (3.0) · `s09a_industry` (new; module card from `s10_house`)
- **Goal.** From the public record: who invented and runs these models, how a model is judged by its hedge, and what
  a desk does with disagreement.
- **Beats.** Cards and one live experiment:
  1. **Firm file: Société Générale's quant research.** Bergomi, then head of equity derivatives quantitative research,
     was Risk's Quant of the Year 2009 for the Smile Dynamics papers. Guyon (at SocGen 2006–2012) and Henry-Labordère
     developed the particle method there (2012). Henry-Labordère won Quant of the Year 2013 (publisher's bio; Risk page
     *(verify year on risk.net)*). Guyon was Quant of the Year at the Risk Awards 2025 (announced November 2024), cited
     for the neural joint SPX/VIX work with Mustapha.
  2. **Exchanges**: Cboe listed VIX futures (26 March 2004) and VIX options (24 February 2006). Deribit's DVOL is the
     crypto counterpart (Part 12). Volatility became an asset with its own smile: ch15's puzzle.
  3. **How a desk judges a model: its hedge.** **Live** `HedgeLedger`: a 30-day ATM BTC option, marked at DVOL every day
     2021–2025, is hedged with (a) the Black–Scholes delta and (b) the **minimum-variance delta** (Hull–White 2017):
     $\Delta_{MV} = \Delta_{BS} + \text{vega}\cdot\partial\mathbb E[\sigma]/\partial S$, with the slope from ch1's leverage
     regression. The two cumulative squared-error curves race. **(probe)**:
     * β fixed from 2021–22 (−0.67 vol points per 1% move ÷ 100) cut the hedge-error variance by **23% in-sample** but
       **raised it by 55% in 2023–25**, when the leverage effect flipped;
     * a rolling 60-day β cut it by **9%** (90-day 5%, 180-day 7%, 365-day 4%).

     Branch: *the model's dynamics matter for hedging, and they are not stable.*
  4. **The horse races**:
     * Bakshi–Cao–Chen (1997), on S&P 500 options: SV with jumps priced best, while for hedging SV alone was enough;
     * Matic–Packham–Härdle (2023), on BTC options: calibration points to SV with low jump frequency; for longer-dated
       options, multi-instrument hedges and SV models reduce tail risk, while short-dated options respond less to
       vol or gamma hedges.
  5. **Model risk → reserves.** ch14's 8% cliquet spread is what a desk must report. Part 15 turns it into a reserve (EU
     prudent valuation's model-risk AVA, *(verify: Commission Delegated Regulation (EU) 2016/101)*). Model validation
     (SR 11-7 → SR 26-2) is in Part 5's industry chapter: one line.
  6. **The House**: the calibrator's validation table (the old `s10_house` content), its Rule 13, and its log of the
     weekly refits.
- **Derivation.** $\Delta_{MV} = \frac{\operatorname{Cov}(dC, dS)}{\operatorname{Var}(dS)} = C_S + C_\sigma\,\frac{\mathbb E[d\sigma\mid dS]}{dS}$ (regress the option's change on the spot's). In Heston: $= C_S + C_v\,\rho\xi/S$ (ch13's regression).
- **Experiment.**
  * `mv_delta` (new, real data; <0.1): fixed and rolling β, variance reductions per year.
  * `heston_hedge` (new, simulated): in the fitted Heston world, BS delta against Heston delta against MV delta for a
    30-day ATM call, 2,000 paths, daily. Expected: MV best (computed; 3 min).
- **Pause-and-predict.** "Volatility rises when prices fall. Should you hold more or less underlying than Black–Scholes
  says when long a call?" (Less. When spot falls, volatility tends to rise, so the call's vega gain offsets part of its
  delta loss. The option behaves like a smaller delta.) *(Probe: mean Δ_BS 0.536 against Δ_MV 0.460.)*
- **Compute.** `mv_delta` (<0.1), `heston_hedge` (3).

### 18 · Frontier, 2023–2026 (2.8) · `s09b_frontier` (new)
- **Goal.** Where SV-and-jumps research is now, with one computed tie-in.
- **Beats.**
  1. **Replay, the reversionary limit.** Refit Heston on the Surface with κ fixed at 15, 30, 60 and 120 (the other four
     free). The slice smiles morph and the fitted ξ grows roughly like √κ. The fit error barely changes and the short
     skew sharpens toward a jump-like shape. This is Abi Jaber–De Carvalho's (2023) "reversionary Heston": as the
     time-scale → 0 it converges to NIG-type jumps (H ≤ −½) or rough-like limits. Narration branches on the computed ξ/√κ
     and errors.
  2. Cards (all checked this session):
     * Abi Jaber, Illand, Li (2023), *the quintic OU model*: volatility a degree-5 polynomial of one fast OU factor, and
       a joint SPX–VIX fit with 6 effective parameters. A Markovian, non-rough answer to ch15 (arXiv 2212.10917; venue
       *(verify: Risk 2023)*).
     * Guyon, Mustapha (2023), "Neural joint S&P 500/VIX smile calibration", *Risk*. A one-factor SLV with neural drift
       and diffusion, fitting SPX smiles, VIX futures and VIX smiles within bid–ask (SSRN 4309576).
     * Choi, Kwok (2024), "Simulation schemes for the Heston model with Poisson conditioning", *EJOR* 314(1):363–376:
       exact-type simulation without Bessel draws (ch5).
     * Reisinger, Tsianni (2025), arXiv 2504.14343: the particle system's well-posedness, propagation of chaos, strong
       rate ½ (ch11).
     * Wang, Després, Dureau, Buet-Golfouse (2026), arXiv 2608.01217: a neural operator returns the surface, Dupire LV,
       the leverage and the conditional moment at once. Calibration goes from 98.5 to 0.6 ms, with forward-start and
       cliquet prices within 0.1 and 0.2 points of the particle method (synthetic tests, as reported).
     * Forward: Part 14 (rough, PDV, DMSP); Part 17 (neural calibrators, deep hedging).
- **Experiment.** `reversionary` (new): 4 κ values × `calibrate(trace=True)` (κ fixed via the bounds) (0.5).
- **Pause-and-predict.** "Speed up mean reversion 8× and keep the short skew. What must ξ do?" (Grow ≈ √8×: the
  skew is ρξ/(4√v₀) only after averaging over 1/κ.)
- **Compute.** `reversionary` (0.5).

### O · The calibrator, recap, desk questions, problems (2.6) · `s11_outro` (absorbs `s10_house`)
- The House card: the vol desk's calibrator lit; Rule 13; the trial counter, unchanged at 73.
- Recap in 10 lines (one per item), the payoff card (Parts 12, 14, 15, 16, 17, 19, 22), and the reference card
  (expanded).
- **Desk questions** (README has the solutions):
  1. Keep "In Heston, what sets the skew? the curvature?"
  2. Keep "LV and SV both fit; price a cliquet".
  3. Replace the κ question (now answered in ch16) with **"Why can't a variance future trade above the variance-swap
     vol?"** (Jensen; ch15).
- **Problems** (90 s): the existing 5, plus (6) "derive the Merton series" and (7) "derive the VG characteristic function
  and its martingale correction". The README has solutions in English and Chinese.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.8 | 10 Skew across T | 2.8 |
| 1 Why vol moves | 3.0 | 11 SLV particles | 3.0 |
| 2 Mixing | 2.8 | 12 Mixing fraction | 2.6 |
| 3 Heston CF | 3.2 | 13 Bergomi | 3.0 |
| 4 Heston fit | 3.0 | 14 Forward smile | 2.8 |
| 5 Heston simulation | 2.8 | 15 SPX/VIX puzzle | 2.8 |
| 6 SABR I | 3.0 | 16 Calibration | 3.2 |
| 7 SABR II | 2.6 | 17 Industry | 3.0 |
| 8 Jumps | 3.0 | 18 Frontier | 2.8 |
| 9 Lévy | 3.0 | Outro | 2.6 |
| | | **Total** | **≈ 57.8** |

That is about 8,050 spoken words. The gate (`--floor 50`) leaves about 8 minutes of slack, and the 60-minute cap leaves
2.2: measure as chapters land.

---

## 3b. Hands-on summary

**Labs** (`lab_card` + `lab_run`, ≤ 12 lines of the real House code, printed outputs from the cache):

1. **ch3 `stochvol.heston_cf`.** `stochvol.py` lines 17–28 (all 12, as they stand). Output: the COS benchmark error
   and "original form wrong from u = 1.69 at T = 1".
2. **ch5 `stochvol.heston_qe`.** The loop body, lines 177–193 (the ψ switch, the quadratic and exponential branches),
   trimmed to 12. Output: the Euler/QE bias rows.
3. **ch9 `stochvol.vg_cf` + `vg_paths`.** Lines 56–62 and 212–218. Output: COS against MC.
4. **ch11 `stochvol.slv_paths`** (new; the step from `compute._simulate`, about 12 lines). Output: the repricing table.
5. **ch16 `stochvol.calibrate_reg`** (new, 10 lines). Output: the λ frontier rows.

**Replays** (the fit shown learning; starts or seeds as bands; baselines at equal budget):
* **ch4**: Heston on the Surface, 3 starts. **(probe)** About 100 evaluations each, 4–5 s. Baseline: the single BS vol
  as a dashed line.
* **ch6**: SABR slice by slice, 9 slices, with the iterates of each.
* **ch8**: Bates, 3 starts, with λ → bound.
* **ch9**: VG, NIG and CGMY fits as a three-curve race on one RMSE axis.
* **ch11**: SLV repricing error against particle count, 3 seeds.
* **ch16**: 100 weekly refits, raw against regularised.
* **ch18**: κ-fixed refits.

`calibrate(..., trace=True)` stores (nfev, rmse, x) per residual evaluation. The replay shows the best-so-far curve, and
the model surface is rebuilt at about 8 checkpoints (`surface_iv` per checkpoint, cached).

**Live simulations**:
* ch1: the two rivers and the scatter;
* ch2: the mixing crowd of Gaussians;
* ch3: the CF helix and the branch-cut winding;
* ch5: one-step variance histograms;
* ch8: the Merton layer cake;
* ch9: the gamma clock and the CGMY Y dial;
* ch11: particles with the kernel window and the leverage surface growing;
* ch12: the η dial;
* ch13: the variance curve ribbon;
* ch14: forward smiles accumulating, and cliquet coupons;
* ch15: the model vol index against DVOL;
* ch17: the hedge ledger race.

**3D scenes:**
* ch3: the CF helix;
* ch4: the Heston surface with sliders, and the Surface dots;
* ch6: the SABR ribbon;
* ch7: the SABR PDE density sheet;
* ch11: the leverage surface;
* ch13: the curve over (t, T);
* ch16: the landscape (exists).

**Compute budget** (seeded; ≈ 75 CPU-minutes of 120; * = exists):

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| facts* (+acf, half-life, crash1987) | 0.3 | sabr_pde | 1 | mixing_sweep | 15 |
| calibrate* | 2 | levy_fits | 1.5 | bergomi*, bergomi_sim, ssr | 0.7 |
| mixing | 1 | bates_replay | 0.5 | exotics*, fwd_semi | 6.5 |
| trap | 0.1 | lab_vg | 0.3 | vol_puzzle | 1 |
| heston_replay, heston_sliders | 1 | skew* (+models) | 0.7 | landscape*, hessian | 4 |
| qe*, qe_density | 3.5 | slv* | 3 | history*, history_reg | 25 |
| sabr*, sabr_replay | 0.4 | slv_particles | 12 | mv_delta, heston_hedge | 3.1 |
| | | | | reversionary, envelope* | 0.5 |

`slv_particles`, `mixing_sweep` and `history_reg` use `CACHE.partial` per (N, seed), per η and per week, so a killed run
resumes. Everything else is seconds to a few minutes. One command rebuilds the part:
`python -m videos.quant.quant13.compute`. No strategy is tested, so the trial counter stays at 73; `mv_delta` is
descriptive hedging, not a trial.

---

## 4. Industry and frontier: sources checked this session (2 Nov 2026)

| Fact | Source |
|---|---|
| Abi Jaber, Illand, Li, "The quintic Ornstein–Uhlenbeck volatility model that jointly calibrates SPX & VIX smiles" (v1 Dec 2022, v2 May 2023); degree-5 polynomial of one OU, 6 effective parameters | https://arxiv.org/abs/2212.10917 (venue *(verify)*) |
| Guyon's puzzle: for continuous models, a good SPX fit leaves the model's ATM VIX implied vol too large; solved non-parametrically by dispersion-constrained martingale transport (Risk, April 2020) | https://cermics.enpc.fr/~guyon/documents/TheJointSPXVIXSmileCalibrationPuzzleSolved_Slides_BBQ_19feb2020.pdf ; https://www.risk.net/7518926 |
| Guyon, Mustapha, "Neural joint S&P 500/VIX smile calibration": one-factor SLV with neural SDEs, fit within bid–ask (SSRN Dec 2022; Risk 2023) | https://papers.ssrn.com/abstract=4309576 ; https://www.risk.net/cutting-edge/7958175/neural-joint-sp-500vix-smile-calibration |
| Guyon: Risk Quant of the Year (Risk Awards 2025, announced 26 Nov 2024); at Société Générale 2006–2012 | https://www.risk.net/awards/7960375/quant-of-the-year-julien-guyon ; https://engineering.nyu.edu/news/fre-visiting-associate-professor-julien-guyon-named-quant-year ; https://cermics.enpc.fr/~guyon/documents/cv_guyon_feb2025.pdf |
| Bergomi, head of equity derivatives quant research at Société Générale, Risk Quant of the Year (2009) for Smile Dynamics | https://www.risk.net/awards/1496978/quant-of-the-year-lorenzo-bergomi ; https://www.crcpress.com/authors/i12741-lorenzo-bergomi |
| Henry-Labordère, Quant of the Year 2013 (publisher's bio); a later Risk page lists him at Natixis | https://www.crcpress.com/authors/i1031-pierre-henry-labordere ; https://www.risk.net/awards/7955845/quant-of-the-year-pierre-henry-labordere *(year verify on risk.net)* |
| Abi Jaber, De Carvalho, "Reconciling rough volatility with jumps" (2023, rev. 2024): reversionary Heston → NIG-type limits for H ≤ −½ | https://arxiv.org/abs/2303.07222 |
| Choi, Kwok (2024) *EJOR* 314(1):363–376, Heston with Poisson conditioning | https://ideas.repec.org/a/eee/ejores/v314y2024i1p363-376.html ; https://arxiv.org/abs/2301.02800 |
| Reisinger, Tsianni (2025), particle system for calibrated Heston-type LSV: well-posedness, propagation of chaos, rate ½ | https://arxiv.org/abs/2504.14343 |
| Wang, Després, Dureau, Buet-Golfouse (Aug 2026), neural operator for LSV: 98.5 → 0.6 ms; forward-start/cliquet within 0.1/0.2 pp of particles (synthetic) | https://arxiv.org/abs/2608.01217 |
| Hou, Wang, Chen, Härdle (2020) "Pricing cryptocurrency options", *J. Fin. Econometrics* 18(2):250–279: SVCJ on BTC; anti-correlated jumps in returns and variance | https://ideas.repec.org/a/oup/jfinec/v18y2020i2p250-279..html |
| Matic, Packham, Härdle (2023) "Hedging cryptocurrency options", *Rev. Derivatives Research* 26(1):91–133 | https://edoc.hu-berlin.de/18452/29120 (DOI 10.1007/s11147-023-09194-6) |
| VIX options first traded 24 Feb 2006 (9,423 contracts); VIX futures 26 Mar 2004 on CFE | https://mondovisione.com/media-and-resources/news/cboe-to-list-options-on-the-cboe-volatility-index-vix-friday-february-24-2006-2011124/ ; https://ir.cboe.com/news/news-details/2024/Cboe-Global-Markets-Commemorates-20-Years-of-Cboe-Futures-Exchange-and-VIX-Futures-Trading/default.aspx |
| Bergomi, *Stochastic Volatility Modeling*, chapter titles (12 chapters) | https://www.routledge.com/Stochastic-Volatility-Modeling/Bergomi/p/book/9781482244069 |
| Lewis (2000) chapter titles | https://library.wolfram.com/infocenter/Books/3512/ |
| Cont–Tankov structure (calibration, time-inhomogeneous, SV with jumps chapters) | https://www.routledge.com/Financial-Modelling-with-Jump-Processes/Cont-Tankov/p/book/9781584884132 |
| Hagan et al. (2002) *Wilmott* pp. 84–108; Obłój (2008) correction | https://arxiv.org/abs/0708.0998 |

**Unverified (keep the marks).**
* Tataru–Fisher (2010), the Bloomberg SLV note (only cited by others; titles and years differ between citations).
* The Henry-Labordère award year on risk.net.
* The venue of the quintic OU paper.
* The EU model-risk AVA article.
* Hull–White (2017) volume and pages.
* Whether Yahoo's ^GSPC covers October 1987 through the data layer.
* The Bergomi 2-factor normalisation and the example parameters.
* The Gram–Charlier skew constant.
* Heston's curvature constant.
* The exact arbitrage-free SABR PDE coefficients.
* "Particle method = industry standard": a phrase in a secondary summary only; say "widely used (as described by …)" or
  drop it.

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 13 · Stochastic Volatility and Jumps (~58)
1. Why volatility must move: Bitcoin's vol of vol, clustering and leverage, measured; 1987 and the skew; random
   volatility makes a smile (Hull–White 1987, Renault–Touzi, Romano–Touzi), derived.
2. Heston (1993): the characteristic function derived (affine ansatz, Riccati), the little trap, what each parameter
   does, the short-maturity skew ρξ/(4√v₀); Feller; Andersen's QE scheme derived; exact and Poisson-conditioned
   simulation.
3. SABR (Hagan et al. 2002): the expansion and the backbone; the negative density; arbitrage-free SABR solved as a PDE;
   Bartlett's delta.
4. Jumps: Merton's series, Kou, Bates; what the Surface does with jump parameters.
5. Lévy models: variance gamma derived as a time change, NIG, CGMY's fine structure; Carr–Wu; the term structure of
   skew across every model.
6. Stochastic local volatility: the McKean–Vlasov loop and the particle method (Guyon–Henry-Labordère 2012), its
   convergence; the mixing fraction.
7. Bergomi's forward variance curves: the curve as the state, the vol-of-vol term structure, the SSR of SV models.
8. The forward smile and cliquets across models fitted to the same vanillas: model disagreement.
9. The SPX/VIX puzzle (Gatheral 2008; Guyon 2020), measured in its Bitcoin form: the smile's vol of vol against DVOL's.
10. Calibration: landscapes, identifiability (the Hessian), parameter instability over 100 weeks, regularisation.

*Textbooks:* Gatheral ch. 2–6, 8, 10–11 (parts); Bergomi ch. 3–4, 6–10, 12; Cont–Tankov ch. 4, 6, 11, 13–15; Lewis
ch. 1–6, 8–9; Guyon–Henry-Labordère (LSV calibration); Oosterlee–Grzelak (Heston, QE, Lévy).
*Computed:* Heston, Bates, Merton, Kou, VG, NIG, CGMY and SABR on the Surface, with replays; the original Heston form's
branch-cut failure; QE against Euler and the exact law; arbitrage-free SABR; SLV convergence and the mixing-fraction
sweep; forward smiles and cliquets across models; the Heston vol index against DVOL; 100 weekly refits, raw and
regularised; the minimum-variance delta on BTC.
*Visuals:* the variance process as a second river; the mixing crowd; the CF helix and the branch cut; the gamma clock;
particles with the leverage surface growing; the variance curve in motion; the optimizer wandering in a flat valley.
*Labs:* `heston_cf`, `heston_qe`, `vg_cf`/`vg_paths`, `slv_paths`, `calibrate_reg`.
*Industry:* Société Générale's quant research (Bergomi, Guyon, Henry-Labordère); Cboe's VIX futures and options;
hedging by the minimum-variance delta; the horse races (Bakshi–Cao–Chen 1997; Matic–Packham–Härdle 2023).
*Frontier:* reversionary Heston and jumps (Abi Jaber–De Carvalho); the quintic OU model; neural joint SPX/VIX
(Guyon–Mustapha 2023); Poisson-conditioned Heston simulation (Choi–Kwok 2024); particle-method analysis (2025);
neural operators for LSV (2026).
*Crisis:* 19 October 1987 and the skew ever since (Rubinstein 1994; Bates 2000).
*Desk:* "In Heston, what sets the skew? The smile's curvature?"; "LV and SV both fit; price a cliquet"; "Why can't
a variance future trade above the variance-swap vol?"
*House:* the calibrator (with traces and regularisation) and the SLV particle simulator.
```

---

## 6. Implementation notes

**Modules.** Kept, with the same names and classes: `s01_hook`, `s02_moves`, `s03_heston`, `s04_sabr`, `s05_jumps`,
`s06_slv`, `s07_bergomi`, `s08_forward`, `s09_calibration`, `s11_outro`. New:
* `s02a_mixing`;
* `s03a_hestonfit`, `s03b_simulate`;
* `s04a_sabrfix`;
* `s05a_levy`, `s05b_skew`;
* `s06a_mixfrac`;
* `s08a_puzzle`;
* `s09a_industry`, `s09b_frontier`.

`s10_house` leaves the manifest (its card goes to ch17 and its rule to the outro; delete the module, as Parts 12 and 16
did). The chapter numbers on the cards follow the manifest.

**Methods that move.**
* `Heston.fit` → `HestonFit`; `Heston.qe` → `Simulate`;
* `SABR.density` → `SABRFix`;
* `Jumps.levy` → `Levy`; `Jumps.slices` and `Jumps.skew` → `Skew`;
* `Moves.mixing` → `Mixing` (the 1987 card stays in ch1);
* `Forward.puzzle` → `Puzzle`.

**House additions.** `explainer/quant/house/stochvol.py`, append-only, each with a test in `tests/test_quant_house.py`:

| Function | Test |
|---|---|
| `cgmy_cf(u, T, C, G, M, Y)` | φ(−i) = 1; Y → 0 matches VG with C = 1/ν |
| `MODELS["Merton"]`, `["Kou"]`, `["CGMY"]` | calibrate round-trip on synthetic quotes |
| `merton_series(S, K, T, sigma, lam, mj, sj, r=0, n_max=60)` | equals COS to 1e-8 |
| `calibrate(..., trace=False)` returning `trace` | the trace's last x equals the result |
| `calibrate_reg(name, quotes, x_prev, lam, W=None)` | lam = 0 equals `calibrate`; large lam returns x_prev |
| `slv_paths(lv_fn, heston_x, days, n_paths, mix=0.5, substeps=4, n_sub=8000, seed=0, return_L=False)` (moved from `compute._simulate`, which then calls it; the cache is unchanged for mix = 0.5) | the repricing error is below 1 vol point on the test SSVI |
| `heston_vix2(v, kappa, theta, tau)` and `heston_vix_options(v0, kappa, theta, xi, T, tau, K)` (non-central χ² quadrature) | the future ≤ √(forward var-swap rate) |
| `heston_forward_start(x, T1, tau, k)` (1D integral) | against MC |
| `sabr_pde_density(F, alpha, beta, rho, nu, T, n=400)` | mass 1, density ≥ 0, ATM vol near Hagan |
| `mv_delta(delta, vega, beta, S)` | the hedge-variance identity on synthetic data |

**Narration branches.** The branches must be computed verdicts:
* the Merton/Bates jump shapes;
* the CGMY Y region;
* whether the SLV error falls with N;
* the η monotonicity;
* the model-to-DVOL vol-of-vol ratio;
* the regularisation frontier;
* the MV-delta sign by period;
* the reversionary ξ/√κ.

Every number is an f-string over the cache. The README's "1.33 vol points" is the vega-weighted implied-vol RMSE, while
`calibrate`'s internal `rmse` (1.296) is a price-over-vega metric. Label the replays' y-axis as the latter, or recompute
the IV RMSE at checkpoints, so the two never appear as one number.

**Data.** Everything is cached:
* the Surface and 100 weekly surfaces (Part 12's builder);
* Binance daily and hourly;
* Deribit DVOL;
* Part 12's SSVI (`Cache("quant12").load("surface")`), read only through its `load`.

Optional: one new data-layer entry, ^GSPC daily 1986–1987, for `crash1987`. If Part 12 has already extended the weekly
surfaces back to April 2021 (its lead decision 1), `history_reg` can cover 2021–2025 and include Terra–Luna and FTX.
Keep 2024–2025 as the default so the part does not depend on that.

**Chinese terms** for `QUANT_ZH_GUIDE.md`:
* 混合定理 (mixing theorem);
* 小陷阱 (little trap);
* 分支切割 (branch cut);
* 二次指数格式 (QE scheme);
* 骨架 (backbone);
* 无套利SABR;
* 跳跃扩散 (jump-diffusion);
* 方差伽马 (variance gamma);
* 时间变换 (time change);
* 精细结构 (fine structure);
* 杠杆函数 (leverage function);
* 粒子方法 (particle method);
* 混合比例 (mixing fraction);
* 远期方差曲线 (forward variance curve);
* 偏斜粘性比 (SSR);
* 远期微笑 (forward smile);
* 棘轮期权 (cliquet);
* 最小方差Delta (minimum-variance delta);
* 正则化 (regularisation).

**Risks.**
1. **CPU on a loaded machine.** `mixing_sweep`, `slv_particles` and `history_reg` total about 50 min. They are resumable
   and should run under `nice`.
2. **The sizes of the derivations.** Ch3, ch5 and ch13 are dense: keep each ladder to 6–7 rows and cut words, not steps.
3. **The 60-minute cap**: 2 minutes of headroom.
4. **The arbitrage-free SABR PDE** is the one genuinely new numerical method here. If its verification slips, ch7 falls
   back to Obłój's correction plus the AKS card, with the PDE named.
5. **Merton's fit** (λ = 0.25, −49% jumps) may move between runs. The narration must follow whatever is cached.
6. **Heston curvature and Gram–Charlier constants**: verify, or say "∝".

---

## 7. Decisions for the lead

1. **`s10_house` leaves the manifest.** Its card goes to the industry chapter and its rule to the outro, as decided for
   Parts 12 and 16.
2. **The split with Part 14.**
   * Part 13 owns the Bergomi framework, its simulation and the SSR, but does **not** calibrate 2-factor Bergomi (Part
     14's `bergomi2f`).
   * Part 13 states and measures the SPX/VIX puzzle; Part 14 solves it.
   * Part 13's skew chapter states the computed slopes and leaves the kernel derivation to Part 14.
3. **A possible error in Part 14's plan.** Its ch15 says continuous models that fit the SPX skew make the "VIX vol of vol
   too low" and "VIX distributions too narrow". Guyon's own 2020 slides say the opposite: a good SPX fit leaves the
   model's **ATM VIX implied vol too large**. Our BTC measurement agrees: the fitted Heston's vol index has a vol of vol
   of 193%, against DVOL's 89%. Please have Part 14's implementer reword that beat.
4. **New House functions.** Accept the ten new `stochvol` functions, with tests. `slv_paths` is moved out of `compute.py`
   with defaults that reproduce the cached `slv` and `exotics` exactly.
5. **The real-data minimum-variance delta** (ch17) is descriptive hedging on DVOL-marked options, not a strategy trial,
   so the counter stays at 73. Its headline is honest: +23% in-sample, −55% out-of-sample with a fixed β, and 4–9% better
   with rolling β.
6. **^GSPC for October 1987.** Optional: one manifest entry. Otherwise the crisis card cites the −20.5% S&P day without a
   computed z-score.

## 7. Lead's decisions (2 Nov 2026)

1. Yes: `s10_house` leaves the manifest; its card goes to the industry chapter, its rule to the outro.
2. Split confirmed: Part 13 owns the Bergomi framework, its simulation and the SSR, and states and measures the SPX/VIX puzzle; Part 14 calibrates two-factor Bergomi, derives the kernel skew and presents attempted solutions (Part 14's implementer has been told, and to fix the direction of the puzzle: a good SPX fit makes the model's VIX implied vols too high).
3. Yes: the ten new `stochvol.py` functions with tests; moved code keeps defaults so cached results are unchanged.
4. The real-data hedging experiment is descriptive: the trial counter stays at 73.
5. Yes, S&P 500 daily 1986–87 for the 1987 z-score, through the data layer; Part 12 adds Yahoo ^GSPC in parallel — reuse its loader/entry if present.
6. KEEP all existing compute item names and output structures: Part 15 (expanding in parallel) reads Part 13's calibrations read-only.
Watch the 60-minute cap (the plan leaves ~2 min). Unverified items: verify or drop.
