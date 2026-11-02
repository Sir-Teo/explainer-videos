# Part 5 · Stochastic Calculus: expansion plan (21 → ~58 min)

Planning document only; nothing in the repo was changed. Sources read: `videos/quant/SYLLABUS.md` §1 (with the November 2026 revision and the "Hands-on" bullet) and §6 Part 5; `READING.md` §1–2 and §4 Part 5; every file in `videos/quant/quant5/`; `explainer/quant/{__init__,viz,data}.py`; `explainer/quant/house/sim.py`; `explainer/ai/viz.py`; `videos/ai/LECTURE_GUIDE.md`; `videos/ai/ai21/s12_reflow.py` (the replay bar) and `videos/ai/ai5/s15_mcmc.py` (the 3D bar); and the gentle prerequisite `videos/math/stochastic/` (49 min: QV, Itô integral, the lemma, GBM, SDEs, Fokker–Planck, Feynman–Kac, Black–Scholes, Girsanov). Part 5 must go **past** that video, not repeat it: proofs, constructions, the general theorems, and the experiments it lacks.

**Cadence.** The lead's addendum asks for 16–20 chapters at about 50–56 minutes, as in *AI, Built* (ai21 has 19 scenes,
54.1 min, about 140 spoken words a minute). So this plan has **20 scenes (hook, 18 chapters, outro), about 58 min**. A chapter runs 2.6–3.4 min (about 380–480 words of narration). Every syllabus item gets one or two chapters, so 5–7 minutes per item. The beats below are written so the 600–800-word drafts the lead asked for can be cut to length.

---

## 1. Current state (`python tools/lecture_length.py quant5`: 21.4 min)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 2.2 | Stop-loss start-gain hedge on 4,000 GBM paths loses 7.90–8.10 at 13…4,000 rebalances against a call worth 7.97. Strong hook, with a computed result and an animated path coloured by the holding. Objectives card, House card. No history-era segment, which the standard requires. |
| 1 | `s02_brownian` | 2.0 | Donsker (static overlay of 3 walks), the three variations (log–log plot), BTC volatility signature plot (80% → 71%). **No construction, no reflection principle, no proofs.** QV gets a plot, not a derivation. |
| 2 | `s03_ito` | 2.2 | Left against midpoint sums for ∫W dW (table), isometry and lemma as a 3-row ladder ("the gentle version derives it"), EM against Milstein orders (0.50/0.93 strong, 0.99/1.00 weak). **No construction of the integral, no isometry proof, no Stratonovich conversion or Wong–Zakai, no existence and uniqueness for SDEs.** |
| 3 | `s04_meanrev` | 2.3 | Vasicek and CIR fitted to DTB3 by regression (κ = 0.099, θ = 4.1%, Feller ratio 0.58), exact simulation, a Feynman–Kac theorem card, the Vasicek curve against the 0.93% 10-year of Dec 2020. **FK quoted, not proved; no Fokker–Planck surface (the syllabus asks for one); no generator or Dynkin.** |
| 4 | `s05_girsanov` | 2.2 | Girsanov card, IS digital (variance ÷52), MRT card. **No Cameron–Martin, no proof, no Novikov, no picture of paths being re-weighted; MRT and Clark–Ocone are named only.** |
| 5 | `s06_localtime` | 2.4 | Tanaka ladder, local time accumulating on one path, scatter (corr 0.97). Good; the derivation of Tanaka is asserted, not shown. |
| 6 | `s07_jumps` | 2.4 | Merton paths, Lévy–Itô and Itô-for-jumps as text, BTC bipower jumps (204 > 5 sd, 24% of variance), Hawkes fit (n = 0.36, half-life 7.6 h). **Poisson and compensators not derived; Hawkes stationarity and likelihood not derived; no thinning on screen; no time-change check.** |
| 7 | `s08_rough` | 2.6 | fBM at three H (static), BTC H ≈ 0.15, a two-path Lévy-area picture. **Not-a-semimartingale only asserted; no Lyons example of why area matters; no signature-learning experiment.** |
| 8 | `s09_house` | 0.6 | Table of tested routines; Rule 6; trial counter 12. |
| — | `s10_outro` | 2.5 | Recap in 8 lines, 3 desk questions, 5 problems, payoff, references. |

Overall: the experiments are real and good (keep them all), but every chapter is about 2 minutes and does three jobs. There are **no full derivations** beyond two ladders, **no 3D**, **no on-screen live simulation** apart from Create() of finished curves, **no lab (code) moments**, **no replays of fitting**, and **no industry or frontier chapter**. No crisis or firm file either.

---

## 2. Audit

### (a) Syllabus items

| Item | Now | Verdict |
|---|---|---|
| 1 BM as scaling limit (Donsker); QV | ch1, 2 min | **thin**: no construction, reflection or QV proof |
| 2 Itô integral; isometry; Stratonovich | ch2 part | **thin**: table only; no construction/proof/conversion |
| 3 Itô's lemma; GBM; EM and Milstein orders | ch2 part | **thin** for the lemma (deferred to gentle video); orders done well |
| 4 OU, CIR; Feynman–Kac | ch3 | **thin**: FK not proved; no FP surface; Feller via regression only |
| 5 Girsanov and Cameron–Martin | ch4 part | **thin**: no CM, no proof, no picture |
| 6 Martingale representation | ch4 part | **thin**: one card, no proof, no experiment |
| 7 Local time, Tanaka, Carr–Jarrow | ch5 | **covered**: needs the Tanaka derivation and occupation density |
| 8 Jumps: Poisson, compound, Lévy–Itô, Itô for jumps | ch6 part | **thin**: statements only |
| 9 Hawkes, branching ratio | ch6 part | **thin**: fit only |
| 10 fBM: Hurst, not a semimartingale | ch7 part | **thin**: assertion only |
| 11 Rough paths and signatures | ch7 part | **thin**: one picture |

### (b) Textbook sections → proposed chapter (new numbering of §3)

Chapter numbers are from my knowledge of the TOCs; those marked (?) should be checked against the book in Phase 0.

| Book · section | Proposed chapter / elsewhere |
|---|---|
| Shreve II 3.2 scaled random walks; 3.3 BM; 3.4 QV; 3.4.3 volatility of GBM | 1, 2 |
| Shreve II 3.5 Markov property; 3.6 first passage time; 3.7 reflection principle | 1 (reflection, first passage), 4 (Markov) |
| Shreve II 4.2–4.3 Itô integral (simple, general integrands) | 3 |
| Shreve II 4.4 Itô–Doeblin formula; 4.6 multivariable; Lévy's characterization | 4 |
| Shreve II 4.5 BSM | Part 10 (ch 4 only derives the GBM solution) |
| Shreve II 4.7 Brownian bridge | 1 (Lévy's midpoint construction is the bridge) |
| Shreve II 5.2 Girsanov; 5.3 martingale representation | 8, 9, 10 |
| Shreve II 5.4–5.6 fundamental theorems, dividends, forwards | Part 9 |
| Shreve II 6.2–6.3 SDEs, Markov property; 6.4 interest-rate models; 6.5 multidim FK; 6.6 (?) | 5 (SDEs), 6–7; 6.4 → Part 19 |
| Shreve II 7 exotics · 8 American · 9 numéraire · 10 term structure | Parts 15 · 8/10/16 · 9/19/22 · 19 |
| Shreve II 11.2 Poisson; 11.3 compound Poisson; 11.4 jump integrals; 11.5 Itô for jumps | 12 |
| Shreve II 11.6 change of measure for jumps; 11.7 call in a jump model | 13 (Esscher / incompleteness, brief); Part 13 |
| Øksendal 2 (BM construction, Kolmogorov extension and continuity) | 1 (Lévy construction; Kolmogorov–Chentsov named) |
| Øksendal 3 Itô integral, extensions, Stratonovich | 3 |
| Øksendal 4 Itô formula; martingale representation theorem (proof by exponentials) | 4, 10 |
| Øksendal 5 existence and uniqueness (Lipschitz, Picard), weak against strong | 5 |
| Øksendal 6 filtering (Kalman–Bucy) | **elsewhere**: Part 7 state-space models (check that Part 7 lists it; if not, add there) |
| Øksendal 7 diffusions: Markov, strong Markov, generator, Dynkin | 7 (generator, Dynkin, exit-time desk question) |
| Øksendal 8 Kolmogorov backward, Feynman–Kac, martingale problem, random time change, Girsanov | 7, 4 (Dambis–Dubins–Schwarz), 8 |
| Øksendal 9 boundary-value problems (Dirichlet) | gentle `stochastic` video (Laplace in a disk); named in 7 |
| Øksendal 10 optimal stopping; 11 control; 12 finance | Parts 8; 8; 9–10 |
| Karatzas–Shreve 1 martingales, Doob–Meyer | Part 4 |
| K–S 2 BM: construction, strong Markov, reflection, modulus, arcsine | 1, 2 (arcsine as pause question) |
| K–S 3.1–3.3 integration, change of variables | 3, 4 |
| K–S 3.4 representations of continuous martingales (DDS time change) | 4 (statement and picture), 14 (point-process analogue) |
| K–S 3.5 Girsanov (Novikov) | 8 |
| K–S 3.6–3.7 local time, Tanaka, Lévy's identity | 11 |
| K–S 4 BM and PDEs (heat equation, FK, arcsine law) | 7 |
| K–S 5 SDEs: strong and weak solutions, martingale problem, Feller's test, linear SDEs | 5, 6 (Feller boundary of CIR) |
| K–S 6 Lévy's theory of local time, excursions | 11 (Lévy's identity only); excursions **not core here: README note** |
| Cont–Tankov 2 Poisson, compound Poisson, Poisson random measures | 12 |
| C–T 3 Lévy processes: Lévy–Itô, Lévy–Khintchine | 12 |
| C–T 4 building Lévy processes (VG, NIG, CGMY, subordination) | Part 13 |
| C–T 5 multidimensional Lévy (copulas) | Part 13 (?) |
| C–T 6 simulation of Lévy processes | 12 (compound Poisson); rest → Part 16 |
| C–T 7 Lévy processes as models of returns (data) | 13 |
| C–T 8 stochastic calculus for jump processes (semimartingales, Itô, stochastic exponential, Esscher) | 12, 13 |
| C–T 9–10 (pricing, incompleteness, quadratic hedging) | 13 (incompleteness demo); Parts 11, 13 |
| Björk 4 stochastic integrals (Itô formula, correlated BMs) · Björk 5 SDEs, generator, Kolmogorov, FK (chapter numbers ? for 4th ed.) | 3, 4 · 5, 7 |
| Friz–Hairer 1–3 (rough paths, BM as a rough path); 4–5 integration, Itô | 16 (Lyons' example, the area); deeper → Part 14 |
| Friz–Hairer 8+ RDEs, regularity structures | beyond the series (README note) |

### (c) Papers on the Part 5 list in READING.md

| Paper | Now | Plan |
|---|---|---|
| Wiener 1923 | timeline only | on screen: hook history and ch1 construction card |
| Itô 1944; 1951 | on screen (narration; MRT card) | ch3 card (1944); ch5 card (1951 SDEs) |
| Cameron–Martin 1944 | card credit | ch8 theorem card, with the shift picture |
| Kac 1949 | card credit | ch7 proof card |
| Girsanov 1960 | card | ch8 |
| Stratonovich 1966 | named, no year | ch3 conversion card |
| Mandelbrot–Van Ness 1968 | on screen | ch15 representation formula |
| Hawkes 1971 | narration | ch14 card |
| Ogata 1981 | **absent** | ch14 lab: thinning code credited on screen |
| Carr–Jarrow 1990 | on screen | ch11 |
| Chen 1957 | on screen | ch16 (Chen's identity on screen) |
| Lyons 1998 | on screen | ch16 (the continuity theorem) |
| Chevyrev–Kormilitzin 2016 | **absent** | ch16 reference line and README reading guide |

Proposed additions to READING.md Part 5 (classic): Bachelier (1900) *Théorie de la spéculation*; Einstein (1905); Lévy (1948) *Processus stochastiques et mouvement brownien*; Donsker (1951) *Memoirs AMS*; Feller (1951) "Two singular diffusion problems" *Annals of Math.*; Tanaka (1963) *Z. Wahrsch.*; Wong–Zakai (1965) *Ann. Math. Stat.*; Dambis (1965), Dubins–Schwarz (1965); Clark (1970) *Ann. Math. Stat.*; Novikov (1972); Milstein (1974) *TPA*; Vasicek (1977) *JFE*; Cox–Ingersoll–Ross (1985) *Econometrica*; Merton (1976) *JFE*; Ocone (1984) *Stochastics*; Kloeden–Platen (1992); Broadie–Glasserman–Kou (1997) *Math. Finance* (discrete-monitoring correction); Rogers (1997)
*Math. Finance*; ABDL (2000); Barndorff-Nielsen–Shephard (2004); Zhang–Mykland–Aït-Sahalia (2005) *JASA*; Giles (2008) "Multilevel Monte Carlo path simulation" *Operations Research*; Filimonov–Sornette (2012) *PRE*; Hardiman–Bercot–Bouchaud (2013) arXiv 1302.1405 (*EPJ B*); Bacry–Mastromatteo–Muzy (2015) arXiv 1502.04592; Jaisson–Rosenbaum (2016) *AAP*; Gatheral–Jaisson–Rosenbaum (2018) *QF*. Industry and frontier: §4 below. Mark *(verify)* any of these the sweep has not yet opened; the ones I verified this session are listed in §4.

---

## 3. The chapter list (20 scenes, about 58 min)

Conventions: **Visual** is the signature picture, built before the formula. **Live** is a simulation drawn as it runs. **Lab** is a `code_block` (≤ 12 lines, from `explainer/ai/viz.py`) of the House function, then run with its output appearing. **Replay** is a `ValueTracker` scrub through fit checkpoints with the loss curve, seeds as `band`s and baselines at equal budget (the pattern of `ai21/s12_reflow.py`: `replay` and `measure`). **Compute** names the `compute.py` item with an estimated CPU time on 4 cores. Existing items keep their names and numbers.

### H · Hook: "A hedge that cannot lose, and does" (2.8 min) · `s01_hook` (deepened)
- Goal: the puzzle, the era, the map.
- Beats: (1) keep the stop-loss paradox as it is: the path coloured by holding, then the 7.90–8.10 table and the 7.97 call;
  (2) **new, "how we got here" (≈60 s)**: timeline strip lit 1900 Bachelier (Brownian prices, 5 years before Einstein), 1923 Wiener (the measure on paths), 1944 Itô, 1960 Girsanov, 1973 Black–Scholes–Merton, 1981 Harrison–Pliska, 1990 Carr–Jarrow, 1998 Lyons, 2018 "Volatility is rough", 2020 negative oil and the Bachelier switch
  (crisis red); (3) objectives card (11 items + industry + frontier); (4) House card: simulation library.
- Pause-and-predict: "Rebalance 4,000 times a year instead of 13. Does the loss shrink?" (No.)
- Compute: `stoploss` (exists, ~1.5 min).

### 1 · Building Brownian motion (2.8) · item 1 · `s02_construct` (new)
- Goal: BM as a limit and as a construction; the first fact it yields (reflection).
- Beats: definition card (W₀ = 0; independent, stationary N(0, t−s) increments; continuous paths). **Live Donsker**: a ±1 walk redrawn at n = 16, 128, 4,096 with the axes rescaling (t/n, x/√n) under a ValueTracker; then the same with uniform and with two-point skewed steps, all converging to one shape (universality). **Lévy's construction**: draw the chord W₀→W₁ ~ N(0,1); then each level k adds midpoints, each displaced by a Gaussian with variance 2^{-(k+1)}; the path "crystallises" level by level (the Brownian bridge on each interval). Name Kolmogorov–Chentsov (continuity).
  **Reflection principle**: one path crossing a = 1 at τ; after τ its mirror image is drawn in a second colour; both are equally likely, which gives the factor 2.
- Derivation (ladder):
  - $W_{\frac{s+t}{2}} \mid W_s, W_t \sim N\!\big(\tfrac{W_s+W_t}{2}, \tfrac{t-s}{4}\big)$, because Gaussian conditioning (the bridge).
  - $P(M_T \ge a) = P(M_T\ge a, W_T \ge a) + P(M_T \ge a, W_T < a)$, by splitting on the endpoint.
  - $P(M_T\ge a, W_T<a) = P(W_T > a)$, because of the strong Markov property and the symmetry after $\tau_a$ (the reflection).
  - $P(M_T \ge a) = 2P(W_T \ge a) = 2\big(1-\Phi(a/\sqrt T)\big)$, adding the two parts.
  - $f_{\tau_a}(t) = \frac{a}{\sqrt{2\pi t^3}}e^{-a^2/2t}$, $\mathbb E\,\tau_a = \infty$, by differentiating in $T$; the tail decays like $t^{-1/2}$.
- Experiment: 20,000 paths, 1,000 steps: simulated P(max ≥ 1) against 2(1 − Φ(1)) = 0.3173. The discrete monitor gives about 0.309 (expected), which is the Broadie–Glasserman–Kou shift of the barrier by 0.5826 σ√Δt:
  2(1 − Φ(1.0184)) ≈ 0.3085. A one-line link to discretely monitored barriers (Part 15).
- Pause-and-predict: "A fair game in continuous time: what fraction of the time is it most likely to have been ahead?"
  (Arcsine law: near 0 or near 1, not ½. Show the U-shaped histogram from the same paths.)
- Compute: `construct` (Lévy levels, 3 Donsker step laws; <0.1 min), `reflection` (0.5 min).

### 2 · Quadratic variation, accumulating (2.6) · item 1 · `s03_qv` (from s02)
- Goal: QV as the one non-vanishing variation; proved; measured on Bitcoin.
- Beats: **Live**: one path drawn left to right. Below it, three running sums Σ|ΔW|, Σ(ΔW)², Σ|ΔW|³ grow as the path is drawn. Then the grid is refined (n = 2⁴…2¹⁶) by a ValueTracker: the first sum's final value climbs off the chart, the third sinks to 0, and the middle one lands on the diagonal "t". The QV staircase hugs the line y = t. That is (dW)² = dt seen happening. Then the proof. Then the BTC signature plot (keep the existing 80% → 71% chart) with the noise explanation and subsampling.
- Derivation: $\mathbb E\sum(\Delta W_k)^2 = \sum \Delta t_k = T$ (variance of each increment); $\operatorname{Var}\sum(\Delta W_k)^2 = \sum 2\Delta t_k^2 \le 2T\max\Delta t_k \to 0$ (independence; Gaussian fourth moment 3Δt²); so $\sum(\Delta W)^2 \to T$ in $L^2$; hence $\sum|\Delta W| \ge \frac{\sum(\Delta W)^2}{\max|\Delta W|} \to \infty$ (the paths have infinite variation, so a Stieltjes integral is impossible, which is why chapter 3 exists). With microstructure noise $\varepsilon$: $\mathbb E\,RV_n = \sigma^2 T + 2n\,\mathbb E\varepsilon^2$ (noise adds n terms), which is why the BTC curve rises at 1 minute.
- Experiment: existing `variation` and `signature` (BTCUSDT 1m 2020): 80% at 1 min, 71% at 1 day. Add from the same data the implied noise variance from the 1-minute bias: $\hat{\mathbb E}\varepsilon^2 = (RV_{1m} - RV_{1d})/(2n)$ (computed).
- Pause-and-predict: "Sample twice as fast. By how much does the spread of the QV estimate shrink?" (by √2: sd √(2/n)).
- Compute: `variation`, `signature` (exist, ~1.5 min), `qv_live` (<0.1).

### 3 · Constructing the Itô integral, and Stratonovich's (3.2) · item 2 · `s04_integral` (from s03)
- Goal: define ∫H dW properly; prove the isometry and the martingale property; the other choice and why physics makes it.
- Beats: **Visual, a ledger of bets**: the integrand as a staircase of positions H_k held across each step (bars above the time axis), the increments ΔW_k as arrows, and the gains H_kΔW_k dropping into a running total. Refine the grid and the staircase approaches a continuous H. Then: simple processes → isometry → completion in L² (the "Cauchy sequence of staircases" picture: three refinements converging in mean square). Then **left against midpoint live**: both sums computed as the grid refines (existing `ito` table becomes two running dots converging to −0.330 and +0.170), and the gap of ½T drawn as the QV staircase again. Then Stratonovich conversion and **Wong–Zakai**: drive the ODE ẋ = x·Ẇ⁽ⁿ⁾ by the piecewise-linear interpolation W⁽ⁿ⁾ of a Brownian path. The ODE solution converges to the
  *Stratonovich* solution e^{W}, not to Itô's e^{W−t/2}. Smooth noise is Stratonovich noise.
- Derivation:
  - $I(H) = \sum_k H_{t_k}(W_{t_{k+1}}-W_{t_k})$, $H_{t_k}$ known at $t_k$ (definition, simple $H$).
  - $\mathbb E[I(H)^2] = \sum_k \mathbb E[H_{t_k}^2]\Delta t_k + 2\sum_{j<k}\mathbb E[H_jH_k\Delta W_j\,\mathbb E(\Delta W_k\mid\mathcal F_{t_k})]$ (expand the square; tower property).
  - $= \mathbb E\int_0^T H_t^2\,dt$ (the cross terms vanish: $\mathbb E(\Delta W_k\mid\mathcal F_{t_k}) = 0$).
  - $I$ is an isometry from simple processes into $L^2$; simple processes are dense in the predictable $L^2$, so $I$ extends uniquely (completion).
  - $\mathbb E[I_t(H)\mid\mathcal F_s] = I_s(H)$ (true for each simple sum, preserved in the $L^2$ limit).
  - $\int_0^T H\circ dW = \int_0^T H\,dW + \tfrac12\langle H, W\rangle_T$ (midpoint minus left point equals half the covariation).
  - $dX = b(X)\circ dW \iff dX = \tfrac12 b b'(X)\,dt + b(X)\,dW$ (apply the line above to $H = b(X)$, $d\langle b(X),W\rangle = b'b\,dt$).
- Experiment: `wong_zakai`: 20,000 paths. E[X₁] from the ODE driven by interpolated W (n = 4…1,024) against Itô E[e^{W−½}] = 1 and Stratonovich E[e^{W}] = e^{½} = 1.6487. Expected: the ODE mean goes to 1.649.
- Pause-and-predict: "A physicist simulates dX = X dW by smoothing the noise. Mean of X at t = 1?" (1.65, not 1.)
- Compute: `ito` (exists), `wong_zakai` (0.5 min).

### 4 · Itô's lemma in full (2.8) · item 3 · `s05_lemma` (new)
- Goal: the proof of the lemma (not the gentle sketch), the multivariate form, the product rule, GBM, and Lévy's characterization (used for Girsanov in ch8).
- Beats: **Visual (3D)**: `ThreeDScene` with the surface z = f(t, x) = x² e^{−t/4} (two inputs), a Brownian path lifted onto it. At each step a small tangent plane predicts the next height; the miss (above the plane, because of convexity) is drawn as a short red riser and stacked in a column beside the surface. The column grows like ½∫f_xx dt, not like 0. The camera orbits 40° while the column fills. Then the ladder. Then the 2D case on a surface z = f(x, y) for two correlated BMs (ρ = −0.7). The cross term appears as a twisting of the stacked risers.
- Derivation:
  - $f(t_{k+1},W_{k+1})-f(t_k,W_k) = f_t\Delta t + f_x\Delta W + \tfrac12 f_{xx}(\Delta W)^2 + R_k$ (Taylor to second order).
  - $\sum f_{xx}(t_k,W_k)\big[(\Delta W_k)^2-\Delta t_k\big]\to 0$ in $L^2$ (a martingale sum: the same variance computation as ch2).
  - $\sum R_k \to 0$ (the remainder is $o((\Delta W)^2)$ uniformly on compacts; $\sum|\Delta W|^3\to0$).
  - $df = f_t\,dt + f_x\,dW + \tfrac12 f_{xx}\,dt$ (limit of the three sums).
  - $df(X,Y) = f_x\,dX + f_y\,dY + \tfrac12 f_{xx}d\langle X\rangle + f_{xy}\,d\langle X,Y\rangle + \tfrac12 f_{yy}d\langle Y\rangle$, $d\langle W,B\rangle = \rho\,dt$ (the same proof in two variables).
  - $d(XY) = X\,dY + Y\,dX + d\langle X,Y\rangle$ (take $f = xy$).
  - $S_t = S_0\exp\big((\mu-\tfrac12\sigma^2)t + \sigma W_t\big)$ solves $dS = \mu S\,dt + \sigma S\,dW$ (apply the lemma to $\log S$).
  - Lévy: a continuous local martingale $M$ with $\langle M\rangle_t = t$ is a BM ($e^{iuM_t+u^2t/2}$ is a martingale by the lemma, so the increments are Gaussian). Dambis–Dubins–Schwarz: $M_t = B_{\langle M\rangle_t}$ (named, with a clock-warp picture reused in ch14).
- Experiment: the stacked "convexity column" against ½∫f_xx dt along the same path (computed: agreement to the discretisation error); for GBM, 20,000 paths: E[log S_T] = (μ − σ²/2)T measured against μT (the volatility drag, one line, since the gentle video covers it).
- Pause-and-predict: "E[W_t⁴]?" (3t², by the lemma: d W⁴ = 4W³dW + 6W²dt). This was a desk question; it moves here.
- Compute: `lemma_column` (<0.2).

### 5 · SDEs: existence, and how to simulate them (3.0) · item 3 · `s06_schemes` (from s03)
- Goal: when an SDE has a solution; the strong and weak orders, measured live; why orders cost money (MLMC).
- Beats: **Picard iteration live**: X⁽⁰⁾ ≡ x₀, X⁽¹⁾, X⁽²⁾ … drawn on one Brownian path for the Lipschitz example dX = sin(X) dt + 0.5 cos(X) dW, each iterate snapping closer, the sup-distance printed (factorial decay). Card: Itô (1951), Lipschitz plus linear growth gives a unique strong solution; strong against weak solutions (Tanaka's dX = sgn(X)dW, which has no strong solution, named). **Lab 1**: `sim.euler_maruyama` and `sim.milstein` (9 lines; the Milstein line highlighted). **Live**: run them on one GBM path at Δt = 1/4 … 1/256; the Euler path (red) and the Milstein path (gold) are redrawn at each Δt beside the exact path (white), the endpoint error dots falling onto two lines of slope ½ and 1 (existing `orders`: 0.50, 0.93; weak 0.99, 1.00). Then **MLMC** (Giles 2008): a telescoping stack of levels drawn as bars of cost. Strong order sets how fast the level variances fall.
- Derivation:
  - $\|X^{(k+1)}-X^{(k)}\|^2_{\mathcal S^2_t} \le C\int_0^t\|X^{(k)}-X^{(k-1)}\|^2_{\mathcal S^2_s}ds$ (Doob's inequality plus the isometry plus Lipschitz), so $\le (Ct)^k/k!$ and the iterates converge.
  - Milstein: $b(X_s) \approx b(X_t) + b'b(X_t)(W_s-W_t)$ (the lemma, to first order), so $\int_t^{t+h} b\,dW \approx b\Delta W + \tfrac12 b'b(\Delta W^2-h)$ (since $\int(W_s-W_t)dW_s = \tfrac12(\Delta W^2-h)$).
  - MLMC: $\mathbb E P_L = \mathbb E P_0 + \sum_{l=1}^L\mathbb E(P_l - P_{l-1})$ (telescoping); $V_l = O(h_l^{2\gamma})$ with strong order $\gamma$, so the cost to reach RMSE $\varepsilon$ is $O(\varepsilon^{-2}(\log\varepsilon)^2)$ for Euler, against $O(\varepsilon^{-3})$ for plain MC.
- Experiment: `orders` (exists); `mlmc`: a GBM call (S₀ = K = 100, σ = 20%), Euler, RMSE targets 10⁻², 3·10⁻³, 10⁻³: standard MC cost against MLMC cost, 4 seeds as a band. Expected: the ratio grows as ε shrinks, roughly an order of magnitude at 10⁻³ (computed; narration branches on the measured ratio).
- Pause-and-predict: "Halve the step. Euler's path error shrinks by …?" (1/√2.)
- Compute: `orders` (1 min), `picard` (<0.1), `mlmc` (5 min).

### 6 · Mean reversion: OU and CIR, solved and fitted (2.8) · item 4 · `s07_meanrev` (from s04)
- Goal: solve OU exactly; CIR's transition law and Feller's boundary; fit by exact MLE and watch it learn.
- Beats: DTB3 1954–2020 drawn (existing). **Lab 2**: `sim.ou_exact` (8 lines), run live: 200 paths fanning from the
  1954 rate, the side density converging to N(θ, σ²/2κ) (`side_density`). Derive the OU solution. CIR: the non-central χ² transition (card), the Feller condition with the boundary picture (paths that touch 0 and leave).
  **Replay**: exact-likelihood fit of CIR to DTB3 (Nelder–Mead on the non-central χ² log-density) scrubbed through iterates. Left: the log-likelihood curve. Right: the fitted stationary Gamma density morphing over the histogram of rates; 5 random starts as a band; the regression estimate as the equal-cost baseline (a dashed line).
- Derivation:
  - $d(e^{\kappa t}X_t) = e^{\kappa t}(\kappa X\,dt + dX) = \kappa\theta e^{\kappa t}dt + \sigma e^{\kappa t}dW$ (product rule; the integrating factor).
  - $X_t = \theta + (x_0-\theta)e^{-\kappa t} + \sigma\int_0^t e^{-\kappa(t-s)}dW_s$ (integrate).
  - $X_t \sim N\big(\theta+(x_0-\theta)e^{-\kappa t}, \tfrac{\sigma^2}{2\kappa}(1-e^{-2\kappa t})\big)$ (a Wiener integral of a deterministic integrand is Gaussian; isometry for the variance).
  - CIR: $X_{t+h} = c\,\chi'^2_d(\lambda)$, $c = \frac{\sigma^2(1-e^{-\kappa h})}{4\kappa}$, $d = \frac{4\kappa\theta}{\sigma^2}$, $\lambda = X_te^{-\kappa h}/c$ (a squared Bessel process, time-changed); the stationary law is Gamma(shape $2\kappa\theta/\sigma^2$, rate $2\kappa/\sigma^2$).
  - Feller: 0 is unattainable iff $2\kappa\theta \ge \sigma^2$, i.e. $d \ge 2$ (Feller's boundary test; a BES(d) hits 0 iff d < 2).
- Experiment: `rates` (exists: Vasicek κ = 0.099, half-life 7 y, θ = 4.1%, 12% negative; CIR Feller ratio 0.58); `cir_mle` (new): the exact MLE against the regression estimates, 5 starts. Expected: the Feller ratio stays below 1
  (computed; branch if it does not).
- Pause-and-predict: "OU from a rate far above θ. When is it halfway back?" (ln 2/κ ≈ 7 years.)
- Compute: `rates` (0.2), `cir_mle` (1 min).

### 7 · From paths to PDEs: Fokker–Planck and Feynman–Kac (3.2) · item 4 · `s08_pde` (new)
- Goal: the forward and backward equations as one object seen from two ends; a proof of Feynman–Kac; bonds.
- Beats: **Visual (3D, the syllabus's "PathFan with the Fokker–Planck surface")**: `ThreeDScene`, axes (t, x, p). A `PathFan` of CIR paths runs along the floor (t, x) while above it the density surface p(t, x) rises out of the point mass at x₀ and spreads. The camera starts at phi 70°, theta −60° and orbits to look down the t-axis, so the surface's slices become the side-histograms. Then **the Feller contrast**: two surfaces side by side, ν = 2κθ/σ² = 0.58 (fitted: the surface spikes into a wall at x = 0) and ν = 2 (the surface pinches to 0 at x = 0). The camera dollies to the x = 0 edge. *That* is the Feller condition. Then reverse the arrow of time: the same axes carry u(t, x) = bond price, solved backward from u(T, x) = 1, the surface sweeping from t = T to 0. Card: generator 𝓛 = a∂ₓ + ½b²∂ₓₓ; FP is 𝓛* forward and FK is 𝓛 backward. Dynkin's formula, with the exit-time desk question.
- Derivation:
  - $\frac{d}{dt}\mathbb E\varphi(X_t) = \mathbb E[\mathcal L\varphi(X_t)]$ (the lemma; the dW term has mean zero).
  - $\int\varphi\,\partial_tp = \int(\mathcal L\varphi)p = \int\varphi\,\mathcal L^*p$ (integrate by parts twice), so $\partial_tp = -\partial_x(ap)+\tfrac12\partial_{xx}(b^2p)$ (Fokker–Planck).
  - FK: let $M_s = e^{-\int_t^s r}u(s,X_s)$; then $dM = e^{-\int r}(u_t+\mathcal Lu-ru)\,ds + e^{-\int r}b\,u_x\,dW$ (the lemma plus the product rule).
  - If $u_t + \mathcal Lu - ru = 0$, $M$ is a martingale, so $u(t,x) = M_t = \mathbb E[M_T] = \mathbb E[e^{-\int_t^T r}g(X_T)\mid X_t=x]$ (optional sampling; integrability assumed).
  - Vasicek: $P = e^{A(\tau)-B(\tau)r}$ into $P_t + \kappa(\theta-r)P_r + \tfrac12\sigma^2P_{rr} - rP = 0$ gives $B' = 1-\kappa B$ and $A' = -\kappa\theta B + \tfrac12\sigma^2B^2$ (match the coefficients of $r$ and 1), so $B = (1-e^{-\kappa\tau})/\kappa$.
  - Dynkin: $\mathbb E f(X_\tau) = f(x) + \mathbb E\int_0^\tau\mathcal Lf$; with $f = x^2$ for BM on $(-a,b)$: $\mathbb E\tau = ab$.
- Experiment: `fp_surface` (densities on a 60 × 120 grid, OU closed form and CIR non-central χ²; checked against a histogram of 20,000 exact paths, L¹ < 0.02 expected); `fk_check`: the Vasicek 10-year bond by Monte Carlo (20,000 exact paths, trapezoid ∫r) against the closed form (expected agreement within 1 bp; computed); then keep the existing 1.38% model against 0.93% actual (Dec 2020) as the "P-parameters, Q-price" lesson (Part 19 calibrates).
- Pause-and-predict: "Brownian motion from 0 exits (−1, 2). Expected time?" (ab = 2.)
- Compute: `fp_surface` (0.5), `fk_check` (0.3).

### 8 · Girsanov: re-weighting paths (3.0) · item 5 · `s09_girsanov` (from s05)
- Goal: Cameron–Martin, then Girsanov proved via Lévy's characterization; when it fails.
- Beats: **Visual (the standard's own example)**: a fan of 300 driftless paths in one colour (`C.P`). A slider θ rises. The paths **do not move**; their opacity is re-weighted by Z_T(ω) = e^{θW_T − θ²T/2} (which gives them drift +θ under Q), and recoloured toward `C.Q` by weight. The terminal histogram on the side (weighted) slides from N(0, T) to N(θT, T). A second panel shows the *moved* fan (W + θt) with the same histogram: identical. Moving paths = re-weighting paths. Then Cameron–Martin (deterministic shift h ∈ H¹), the density, Girsanov for adapted θ, the proof, and Novikov. Failure: on [0, ∞) the measures are singular (W_t/t → 0 under P, → θ under Q), which the picture shows as weights collapsing to a few paths as T grows (effective sample size printed).
- Derivation:
  - Coin of Part 4: $\frac{dQ}{dP} = \prod_k\frac{q(\Delta W_k)}{p(\Delta W_k)} = \exp\big(\sum\theta\Delta W_k - \tfrac12\theta^2\Delta t_k\big)$ (ratio of Gaussian densities; complete the square).
  - $Z_t = \exp\big(\int_0^t\theta\,dW - \tfrac12\int_0^t\theta^2ds\big)$, $dZ = \theta Z\,dW$ (the lemma: Z is the stochastic exponential).
  - Under $dQ = Z_TdP$, $\widetilde W = W - \int\theta\,ds$: $d(Z\widetilde W) = Z\,d\widetilde W + \widetilde W\,dZ + d\langle Z,\widetilde W\rangle = Z(1+\theta\widetilde W)dW$ (product rule: the $-Z\theta\,dt$ and $+\theta Z\,dt$ cancel).
  - So $Z\widetilde W$ is a $P$-martingale, i.e. $\widetilde W$ is a $Q$-martingale (Bayes: $\mathbb E_Q[Y\mid\mathcal F_s] = \mathbb E_P[Z_TY\mid\mathcal F_s]/Z_s$); $\langle\widetilde W\rangle_t = t$; by Lévy, $\widetilde W$ is a $Q$-BM.
  - Novikov: $\mathbb E\exp(\tfrac12\int_0^T\theta^2) < \infty \Rightarrow \mathbb EZ_T = 1$ (otherwise $Z$ is only a supermartingale, and $Q$ loses mass).
- Experiment: `girsanov_paths`: 300 drawn paths plus 100,000 for the histogram; weighted mean of W_T against θT; effective sample size (Σw)²/Σw² at T = 1, 4, 16, 64 (expected: e^{−θ²T} decay, computed).
- Pause-and-predict: "Under P, what is E[Z_T]?" (1, if Novikov holds.)
- Compute: `girsanov_paths` (0.3).

### 9 · Girsanov at work: importance sampling, and why volatility can't be changed (2.6) · item 5 · `s10_is` (from s05)
- Goal: Girsanov as a computational tool; QV as the measure-invariant that makes σ observable and μ not.
- Beats: **Lab 3**: `sim.is_digital` (10 lines: shift Z by θ, weight by e^{−θZ−θ²/2}). **Live**: the two running MC estimates (plain and reweighted) drawn path by path with ±2 se bands on one axis, converging to 0.00714 (existing numbers: 0.0074 ± 0.0006 against 0.00707 ± 0.00008; variance ÷52). Then the asymmetry: **live** on one simulated year of
  1-minute GBM: σ̂ from QV settles to 20.0% within a hair, while μ̂ wanders ±20 points (both estimators drawn as the year unrolls). Two measures with σ = 20% and 21% disagree on an event of probability one ({QV = 0.04T}), so they are singular. That is why prices depend on σ and not on μ (Parts 9–10).
- Derivation: $\hat\sigma^2 = \frac1T\sum(\Delta\log S)^2$, $\operatorname{sd}(\hat\sigma)\approx\sigma/\sqrt{2n}$ (ch2's variance); $\hat\mu = \log(S_T/S_0)/T + \tfrac12\sigma^2$, $\operatorname{sd}(\hat\mu) = \sigma/\sqrt T$ (it depends on T only, not on n).
- Experiment: `girsanov` (exists); `observability`: n = 525,600 minutes, σ̂ sd ≈ 0.0002 against μ̂ sd = 0.20 (theory), measured on 200 years.
- Pause-and-predict: "Sample every second instead of every minute. Which estimate improves?" (σ̂ only.)
- Compute: `girsanov` (<0.1), `observability` (0.5).

### 10 · Martingale representation and Clark–Ocone: why a hedge exists (3.0) · item 6 · `s11_representation` (new)
- Goal: prove (in outline) that every Brownian martingale is a stochastic integral; compute the integrand; watch a hedge replicate; see the representation fail with a second noise.
- Beats: **Visual, live**: top, a Brownian path; middle, the martingale M_t = E[F | 𝓕_t] for F = W_T² (= W_t² + T − t), drawn as the path unrolls; bottom, the hedge's wealth V_t = E F + Σ H_k ΔW_k with H = 2W_t, drawn on the same axis. At n = 8 the two separate visibly; at n = 512 they overlap, and the gap |V_T − F| is shown as a red sliver whose sd falls like n^{−1/2}. Then the theorem with the proof idea: **exponentials are integrals** (the lemma), exponentials span L² (a card: a random variable orthogonal to all of them is 0), and the isometry closes the space. Clark–Ocone gives H = E[D_tF | 𝓕_t] (the Malliavin derivative as "the sensitivity of F to a bump in dW at t"). For a call it is the delta (Part 10). Finally **completeness breaks**: F depends on a second BM B (e.g. F = B_T²); the hedge in W alone leaves a residual that does not shrink with n.
- Derivation:
  - $\mathcal E^h_T = \exp(\int h\,dW - \tfrac12\int h^2)$, $d\mathcal E^h = h\mathcal E^h dW$, so $\mathcal E^h_T = 1 + \int_0^T h\mathcal E^h dW$ (the lemma: exponentials are integrals).
  - $\{\mathcal E^h_T\}$ is total in $L^2(\mathcal F_T^W)$ (if $Y\perp$ all of them, $\mathbb E[Y\,e^{\sum\lambda_iW_{t_i}}] = 0$ for all $\lambda$, so $Y = 0$: Fourier uniqueness).
  - So $F = \mathbb EF + \int_0^T H\,dW$ for every $F\in L^2$ (the isometry: limits of integrals are integrals), and $M_t = \mathbb E[F\mid\mathcal F_t] = M_0 + \int_0^t H\,dW$.
  - Clark–Ocone: $H_t = \mathbb E[D_tF\mid\mathcal F_t]$. Examples: $F = W_T^2$: $D_tF = 2W_T$, $H = 2W_t$; $F = W_T^3$: $H = 3(W_t^2 + T - t)$ (check by $\int_0^T(T-t)dW = \int_0^TW\,dt$, integration by parts).
  - Discrete hedge error for $F = W_T^2$: $F - V_T = \sum(\Delta W_k)^2 - T$, sd $= \sqrt{2/n}\,T$ (it is ch2's QV error).
- Experiment: `hedge_rates`: 20,000 paths, n = 8…2,048. The hedge error sd for W_T² (expected slope −½, value √(2/n)) and for a Black–Scholes ATM call (expected slope −½; Kamal–Derman 1999's approximation √(π/4)·vega·σ/√N as reference, marked *(verify)*); the two-factor residual (flat). Bands over 5 seeds.
- Pause-and-predict: "Hedge W_T² with 4× as many trades. The error sd?" (halves.)
- Compute: `hedge_rates` (3 min).

### 11 · Local time and Tanaka: the paradox resolved (3.2) · item 7 · `s12_localtime` (from s06)
- Goal: derive Tanaka; local time as occupation density; Lévy's identity; close the hook.
- Beats: **Visual, live**: a path runs; on the right a horizontal histogram of *time spent at each level* builds up as it runs (an occupation-density "sandpile" that grows sideways). A horizontal line at K picks the pile's height there: that is L_t^K. Tanaka by smoothing the kink: |x| replaced by f_ε (a parabola inside (−ε, ε)), f_ε'' = 1/ε on the band, and the lemma's second-order term becomes (1/2ε)·time in the band. Shrink ε (ValueTracker) and the band thins while its term converges. Then Lévy's identity (|W| − L is a BM; L = running max of −β), and the **HedgeLedger** of the stop-loss strategy on one path. Each crossing of K books a small loss, and the ledger total tracks ½L_t^K (existing `stoploss.one`). End with the existing scatter (corr 0.97) and table (7.84 against 7.97). Practice: pin risk (options at the strike close to expiry are the hardest to hedge); a link to Dupire's local volatility, whose derivation uses the same Tanaka–Meyer term (Part 12).
- Derivation:
  - $f_\varepsilon(x) = |x|$ for $|x|\ge\varepsilon$, $\frac{\varepsilon}{2}+\frac{x^2}{2\varepsilon}$ inside, so $f_\varepsilon'' = \frac1\varepsilon\mathbf 1_{(-\varepsilon,\varepsilon)}$ (definition).
  - $f_\varepsilon(W_t) = f_\varepsilon(0) + \int f_\varepsilon'(W)dW + \frac1{2\varepsilon}\int_0^t\mathbf 1_{\{|W_s|<\varepsilon\}}ds$ (the lemma; $f_\varepsilon\in C^1$, piecewise $C^2$ suffices).
  - $|W_t| = \int_0^t\operatorname{sgn}(W_s)dW_s + L^0_t$, $L^0_t = \lim\frac1{2\varepsilon}\int_0^t\mathbf 1_{\{|W_s|<\varepsilon\}}ds$ ($\varepsilon\to0$: $f_\varepsilon'\to\operatorname{sgn}$ in $L^2$).
  - Occupation: $\int_0^t g(W_s)ds = \int_{\mathbb R}g(a)L^a_t\,da$ (the same limit at every level $a$).
  - $(S_T-K)^+ = (S_0-K)^+ + \int\mathbf 1_{\{S>K\}}dS + \tfrac12L^K_T$, and $\mathbb E_Q[\tfrac12L^K_T] = C_0 - (S_0-K)^+$ (Tanaka for $S$; take expectations, r = 0) (Carr–Jarrow 1990).
- Experiment: `stoploss` (exists); `tanaka`: 20,000 BM paths, E[L₁⁰] against √(2/π) = 0.798, and Lévy's identity
  (the law of L₁ against that of max_{s≤1} W_s, a QQ line).
- Pause-and-predict: "Expected local time at 0 of BM by t = 1?" (E|W₁| = 0.80.)
- Compute: `stoploss` (shared), `tanaka` (0.5).

### 12 · Jumps: Poisson to Lévy–Itô, and Itô for jumps (3.2) · item 8 · `s13_levy` (from s07)
- Goal: build jump processes from the Poisson clock; compensate them; prove the jump Itô formula; Lévy–Khintchine.
- Beats: **Live**: a Poisson clock rings (tick marks on the time axis, exponential gaps drawn as springs), N_t climbs as a staircase, and the compensated Ñ_t = N_t − λt is drawn below, a martingale sawtooth. Marks attach random sizes Y_i: the compound Poisson. **Visual, the Lévy–Itô layer cake**: one Lévy path is decomposed into four stacked strips (drift line; Brownian part; big jumps |ΔX| ≥ 1; compensated small jumps). Sliding the cutoff ε → 0 makes the small-jump strip turn from sparse spikes into Brownian-looking fuzz (Asmussen–Rosiński intuition, named). Then the jump Itô formula with the jump term boxed, and the Merton paths (existing).
- Derivation:
  - $P(N_{t+h}-N_t = 1\mid\mathcal F_t) = \lambda h + o(h)$, gaps $\sim$ Exp(λ) (definition); $\mathbb E[N_t-\lambda t\mid\mathcal F_s] = N_s-\lambda s$ (independent increments).
  - $[\tilde N]_t = N_t$, $\mathbb E\tilde N_t^2 = \lambda t$ (each jump has size 1; $(\Delta N)^2 = \Delta N$).
  - $\mathbb E e^{iu\sum_{i\le N_t}Y_i} = \exp\big(\lambda t(\phi_Y(u)-1)\big)$ (condition on $N_t$).
  - $\mathbb Ee^{iuX_t} = e^{t\psi(u)}$, $\psi(u) = iub - \tfrac12\sigma^2u^2 + \int(e^{iux}-1-iux\mathbf 1_{|x|<1})\nu(dx)$ (Lévy–Khintchine: the four strips multiply because they are independent).
  - $f(X_t) = f(X_0) + \int f'(X_{s-})dX_s + \tfrac12\int f''d\langle X^c\rangle + \sum_{s\le t}\big[f(X_s)-f(X_{s-})-f'(X_{s-})\Delta X_s\big]$ (between jumps the continuous lemma; at each jump, replace the linear guess by the true change).
  - Merton: $S_t = S_0\exp\big((\mu-\tfrac12\sigma^2-\lambda\bar k)t + \sigma W_t + \sum Y_i\big)$, $\bar k = e^{m+s^2/2}-1$ (compensate so $\mathbb ES_t = S_0e^{\mu t}$).
- Experiment: `levy_layers` (one path, four strips, cutoffs ε = 1, 0.3, 0.1, 0.03; a variance-gamma example); a check that the compensated compound Poisson has mean 0 and variance λt E[Y²] on 50,000 paths.
- Pause-and-predict: "Poisson rate 6 a year. Probability of no jump in a month?" (e^{−0.5} = 0.61.)
- Compute: `levy_layers` (0.2), `merton` paths (exists inside `jumps`).

### 13 · Jumps in data, and the hedge they break (2.8) · item 8 · `s14_jumpdata` (from s07)
- Goal: detect jumps in real prices; show that jumps make the market incomplete (the representation of ch10 fails).
- Beats: the existing BTC bipower histogram (204 hours beyond 5 local sd, 62/78/64 by year, 0.015 expected for a Gaussian, 24% of variance), now with the bipower derivation and a running jump-share as the 2018–2020 path is drawn. Then **live hedging**: a short ATM call delta-hedged with the Black–Scholes delta at the diffusion vol on Merton paths, rebalanced n = 13 … 4,000 times. The no-jump error band shrinks to nothing; the jump-path error stalls at a floor, with one path's ledger showing the hedge losing in a single jump. Card: the Esscher transform, one of infinitely many risk-neutral measures (Part 13).
- Derivation: $BV = \frac\pi2\sum|r_k||r_{k-1}| \to \int\sigma^2dt$ while $RV \to \int\sigma^2dt + \sum J^2$ (E|Z| = √(2/π); one jump touches a product only with a neighbour that is O(√Δt)); so $RV - BV \to \sum J^2$ (Barndorff-Nielsen–Shephard 2004). Hedge P&L at a jump: $\Delta V - \Delta\cdot\Delta S = \tfrac12\Gamma J^2S^2 + O(J^3)$, which no choice of Δ removes for two different jump sizes (two unknowns per jump, one instrument).
- Experiment: `jumps` (exists); `jump_hedge`: 10,000 Merton paths (λ = 6, m = −5%, s = 8%, σ = 50% — the existing parameters), n ∈ {13, 52, 252, 1,000, 4,000}, error sd with and without jumps. Expected: the no-jump sd falls ∝ n^{−½}; the jump sd flattens (computed).
- Pause-and-predict: "Rebalance every second. Does the jump error vanish?" (No.)
- Compute: `jumps` (0.5), `jump_hedge` (2 min).

### 14 · Hawkes: jumps that cause jumps (3.2) · item 9 · `s15_hawkes` (from s07)
- Goal: self-exciting intensity, its branching structure and stationarity; simulate it (lab); fit it (replay); test the fit by time change.
- Beats: **Lab 4**: `sim.hawkes_thinning` (Ogata 1981, 12 lines) on screen, then run: the candidate points rain down under the dashed bound λ̄; accepted ones (gold) kick the intensity curve up by α, rejected ones (grey) fall through. The
  **branching picture**: the same events redrawn as a family tree (immigrants on the baseline, children hanging from parents), cluster sizes counted. **Replay**: the BTC fit (229 events 2018–2020): Nelder–Mead iterates scrubbed. Left, the log-likelihood climbing to −506 (Poisson baseline −588 as a dashed line); right, the fitted intensity curve morphing over the event ticks; 8 random starts as a band (they should coincide). **Visual, the time change**: warp the time axis by the fitted compensator Λ(t). The clustered ticks slide apart into an even rain, a unit Poisson process. A QQ-plot of the rescaled gaps against Exp(1) builds point by point, Hawkes on the line and Poisson off it. The same idea as Dambis–Dubins–Schwarz in ch4: a clock run by the intensity.
- Derivation:
  - $\lambda_t = \mu + \sum_{t_i<t}\alpha e^{-\beta(t-t_i)}$ (definition); each event's offspring count is Poisson with mean $n = \int_0^\infty\alpha e^{-\beta s}ds = \alpha/\beta$.
  - Stationary rate: $\bar\lambda = \mu + n\bar\lambda \Rightarrow \bar\lambda = \mu/(1-n)$, $n<1$ (take expectations); the cluster size is $1/(1-n)$ (a geometric series of generations).
  - $\ell = \sum_i\log\lambda(t_i) - \int_0^T\lambda\,dt$, $\int_0^T\lambda = \mu T + \frac\alpha\beta\sum_i(1-e^{-\beta(T-t_i)})$ (point-process likelihood).
  - $A_i = e^{-\beta(t_i-t_{i-1})}(1+A_{i-1})$, $\lambda(t_i) = \mu+\alpha A_i$ (the Ozaki recursion: O(N), not O(N²)).
  - Time-rescaling: $\tau_i = \Lambda(t_i)$ form a unit-rate Poisson process (Meyer/Papangelou), so $\tau_i-\tau_{i-1}\sim$ Exp(1) under a correct model.
- Experiment: `hawkes` (exists: n = 0.36, half-life 7.6 h); `hawkes_replay` (iterates + 8 starts); `hawkes_check`: 50 simulations at μ = 0.2, α = 1.4, β = 2 over T = 2,000 (mean count against μT/(1 − 0.7) = 1,333); `hawkes_rescale`: KS p-values for Hawkes against Poisson on BTC (expected: Poisson rejected; computed and branched). Industry note on screen: Hardiman, Bercot and Bouchaud (2013, CFM) estimated n near the critical value 1 for E-mini mid-price changes
  1998–2011; Filimonov–Sornette (2012) reported a rising n; the dispute is over kernels and windows (both verified via arXiv 1302.1405). Forward: Part 14 (nearly unstable Hawkes → rough volatility, Jaisson–Rosenbaum 2016), Part 36.
- Pause-and-predict: "Branching ratio 0.36. What fraction of large moves were triggered by earlier ones?" (36%.)
- Compute: `hawkes` (0.5), `hawkes_replay` (1), `hawkes_check` (1), `hawkes_rescale` (<0.1).

### 15 · Fractional Brownian motion: memory and roughness (3.0) · item 10 · `s16_fbm` (from s08)
- Goal: fBM's covariance and representation; the proof that it is not a semimartingale; simulate it (lab); measure roughness, and the caveat.
- Beats: **Visual, the H dial**: one fBM path built by Davies–Harte from a *fixed* complex Gaussian vector, redrawn as a ValueTracker sweeps H from 0.9 to 0.1. The same random seed turns from a smooth trend into a jagged scrawl, and passes through Brownian motion at 0.5 (the path highlighted). A readout shows the lag-1 increment correlation 2^{2H−1} − 1 changing sign at ½. **Lab 5**: `sim.fbm` (Davies–Harte, 12 lines). Then p-variation live: Σ|ΔB^H|² on refining grids for H = 0.3, 0.5, 0.7 (to ∞, to T, to 0) explains "not a semimartingale". Then Rogers' arbitrage idea (one line), and the existing BTC estimate H ≈ 0.15 (0.13–0.16; estimator recovers 0.10 and 0.48 on fBM). Then **the caveat, computed**: Cont and Das (2024) show that realized volatility can look rough when spot volatility is not. Simulate a smooth (H = 0.5, OU) log-volatility, measure it with 5-minute RV plus noise, estimate H, and get a low H. Narration branches on the number.
- Derivation:
  - $\mathbb E[B^H_tB^H_s] = \tfrac12(t^{2H}+s^{2H}-|t-s|^{2H})$ (definition); $\rho(k) = \tfrac12(|k+1|^{2H}-2|k|^{2H}+|k-1|^{2H})$ for unit increments (expand).
  - $B^H_t = \frac1{\Gamma(H+\frac12)}\int_{\mathbb R}\big[(t-s)_+^{H-\frac12}-(-s)_+^{H-\frac12}\big]dW_s$ (Mandelbrot–Van Ness: BM with a power-law memory kernel).
  - $\mathbb E\sum_{k<n}|B^H_{(k+1)/n}-B^H_{k/n}|^2 = n\cdot n^{-2H} = n^{1-2H}$ (self-similarity) → $\infty$ if $H<\frac12$, $0$ if $H>\frac12$.
  - A continuous semimartingale has finite, nonzero QV unless its martingale part vanishes; QV 0 means finite variation, which fails for $H>\frac12$ by the $p$-variation of order $1/H$; so for $H\neq\frac12$ it is not a semimartingale (outline; Rogers 1997).
- Experiment: `fbm_morph` (H grid 0.05…0.95, 1,000 points, fixed seed); `pvar`; `rough` (exists); `cont_das`: 500 days of a 1-second OU log-vol (H = ½, mean reversion 1/week) with an Euler price and i.i.d. noise; daily RV from 5-minute returns; `hurst_from_increments` on log RV. Expected: an estimate well below 0.5 (computed; if it is not, the narration says the artefact needs larger noise and reports what was found).
- Pause-and-predict: "H = 0.1. Is a rise more likely to be followed by a fall?" (Yes: ρ(1) = 2^{−0.8} − 1 = −0.43.)
- Compute: `fbm`/`fbm_morph` (0.3), `pvar` (0.3), `rough` (1), `cont_das` (3).

### 16 · Rough paths and signatures (3.2) · item 11 · `s17_signature` (from s08)
- Goal: why integration needs more than the path (Lyons' example); the signature; Chen; universality; learn with it.
- Beats: **Visual (3D), Lyons' helix**: X⁽ⁿ⁾(t) = n^{−1}(cos n²t, sin n²t) in the floor plane: tiny fast circles that shrink to a point as n grows (uniform distance → 0). Feed them to the ODE dY¹ = dX¹, dY² = dX², dY³ = Y¹dX² − Y²dX¹. The solution lifts into 3D as a helix whose **floor shadow shrinks while its height keeps rising to t**: the Lévy area n^{−2}·n²·t/2 does not vanish. The camera goes from top-down (paths converge) to side-on (solutions don't). So the solution map is discontinuous in the path alone, and continuous in (path, area): Lyons' theorem. Then the existing two-path area picture, Chen's identity (two segments concatenate by a tensor product), the factorial decay, and universality. **Lab 6**: `sim.signature(path, depth)` (new; 10 lines, Chen segment by segment).
  **Replay**: ridge regression of a path functional on truncated signatures, depth 1 → 5 scrubbed. Left, the hold-out R² climbing with depth (5 train/test splits as a band, increments-only and last-value baselines as dashed lines); right, predicted against true payoffs, the cloud tightening onto the diagonal.
- Derivation:
  - $S(X)^{i_1\dots i_k}_{s,t} = \int_{s<u_1<\dots<u_k<t}dX^{i_1}_{u_1}\cdots dX^{i_k}_{u_k}$ (definition); level 1 = increments; the antisymmetric part of level 2 is the Lévy area $A = \tfrac12\int(X^1dX^2 - X^2dX^1)$.
  - Lyons' example: $A^{(n)}_t = \tfrac12\int_0^t n^{-2}\cdot n^2\,du = t/2$ (on a circle of radius $r$ at angular speed $\omega$, area accrues at $\frac12r^2\omega$), while $\|X^{(n)}\|_\infty = 1/n$.
  - $Y^3_t = \int(Y^1dX^2 - Y^2dX^1) = 2A_t = t$ (the third ODE coordinate is twice the area).
  - Chen: $S(X*Y) = S(X)\otimes S(Y)$; a straight segment $\Delta$ has $S = \exp_\otimes(\Delta) = (1,\Delta,\Delta^{\otimes2}/2!,\dots)$ (the lab's loop).
  - $\|S^k\| \le L^k/k!$ for a path of length $L$ (the simplex has volume $1/k!$), so truncation error decays factorially.
  - Shuffle product: $\langle\ell_1,S\rangle\langle\ell_2,S\rangle = \langle\ell_1\sqcup\!\sqcup\,\ell_2,S\rangle$, so linear functionals form an algebra; with time added the signature separates paths; Stone–Weierstrass gives universal approximation on compacts.
- Experiment: `helix` (n = 1, 2, 4, 8; trivial); `sig_regression`: 20,000 time-augmented GBM paths (64 steps); targets:
  (a) the arithmetic average (exactly linear at depth 2: ∫X dt = TX_T − ∫t dX, so R² → 1.000 at depth 2: a built-in check), (b) an Asian call (A − K)⁺ (expected R² rising with depth, roughly 0.9+ by depth 4–5; computed), (c) the Lévy area of a 2D path (exactly level 2). Ridge λ chosen by CV; 5 splits; baselines: increments and last value.
- Pause-and-predict: "Two paths with the same increments: right-then-up and up-then-right. Which level of the signature first tells them apart?" (Level 2: areas +½ and −½.)
- Compute: `helix` (<0.1), `sig_regression` (3 min).

### 17 · Industry: how desks build, test and run SDE models (3.0) · `s18_industry` (new)
- Goal: what this calculus is used for inside banks, exchanges and market makers, from the public record; the crisis file and the firm file.
- Beats (each is a card or a live object, with its source on screen):
  1. **The model is a choice of SDE, and it can break: crisis file, 20 April 2020.** FRED `DCOILWTICO` (Cushing WTI spot) drawn through April 2020, falling to −36.98 on 20 April (fetched this session); the May NYMEX contract settled at −37.63 (CFTC release 8432-21). Under GBM log S is undefined below zero. CME Clearing advisory 20-152 (8 April) set triggers, and advisory 20-171 (21 April) switched WTI and related energy options to the **Bachelier** model for the margin cycle after trading on 22 April, to accommodate negative underlying prices and strikes. The visual: two path fans, GBM (bounded below by 0) and arithmetic BM (crossing 0), with the price line breaking through the GBM floor. Computed: Black-76 against Bachelier prices of a WTI put at matched ATM vol as F → 0 (illustrative).
  2. **Firm file: Interactive Brokers.** Its system did not display negative prices to customers; the CFTC
     (28 Sept 2021) found it "did not adequately prepare and configure its electronic trading system to recognize negative prices", fined it $1.75 million and ordered $82.57 million restitution (credited as already paid). The firm's provisional loss was about $88 million (April 2020), later ~$104 million (Q2 2020 results).
  3. **Simulation infrastructure.** Clearing houses: OCC's STANS margin system "utilizes large-scale Monte Carlo simulations to forecast price and volatility movements" (SEC filings). Libraries: QuantLib's path generators combine Sobol sequences with Brownian-bridge construction (ch1's Lévy construction is that bridge). Hardware: STAC-A2, the banks' benchmark for Monte Carlo Greeks of a multi-asset path-dependent option under **Heston**, with early exercise; an NVIDIA H100 report listed 8.9 ms warm time (*(verify against the STAC report)*).
  4. **Greeks at scale: adjoints.** Giles and Glasserman, "Smoking adjoints: fast Monte Carlo Greeks", *Risk* 2006: pathwise derivatives computed backward cost a small multiple of one price, whatever the number of inputs. Danske Bank won Risk's In-House System of the Year 2015 with AAD that let traders compute CVA "in 10 seconds, using standard hardware" (Risk.net teaser; Savine, *Modern Computational Finance*, 2018).
  5. **Itô on the trading floor: the VIX.** Lab-style derivation, and the hands-on experiment of the chapter: $d\log S = dS/S - \tfrac12\sigma^2dt \Rightarrow \int_0^T\sigma^2dt = 2\big(\int_0^T\frac{dS}{S} - \log\frac{S_T}{S_0}\big)$, and $-\log\frac{S_T}{F} = -\frac{S_T-F}{F} + \int_0^F\frac{(K-S_T)^+}{K^2}dK + \int_F^\infty\frac{(S_T-K)^+}{K^2}dK$ (Taylor with remainder). So realized variance = a delta hedge plus a static 1/K² strip of options (Demeterfi, Derman, Kamal, Zou 1999, Goldman Sachs QS note / *J. Derivatives*), the weighting Cboe's VIX methodology uses. **Live**: a Heston path with the replicating P&L and the realized variance drawn together; then with a Merton jump the two split by ≈ J³/3
     (ch12's jump term).
  6. **Model validation.** SR 11-7 (Fed/OCC, 4 April 2011) made "effective challenge", independent validation and outcomes analysis US supervisory practice. On 17 April 2026 SR 26-2 (Fed, OCC, FDIC) superseded it. The House's Rule 6
     (every simulator reproduces a known answer first) is that discipline in miniature; the chapter shows the House's test table (the old `s09_house` content) as the validation report.
- Experiment: `wti` (FRED DCOILWTICO 2020-03…2020-05; one new manifest entry); `bachelier_vs_black`; `varswap`:
  10,000 Heston paths (κ = 2, θ = 0.04, ξ = 0.5, ρ = −0.7, full-truncation Euler, 252 and 2,520 steps): replication error sd against realized variance. Expected: small and shrinking with n without jumps; a bias of order λE[J³]/3 with Merton jumps (computed).
- Pause-and-predict: "Why does the VIX weight strikes by 1/K²?" (It replicates −log S, the payoff whose Itô drift is exactly ½σ².)
- Compute: `wti` (<0.1), `bachelier_vs_black` (<0.1), `varswap` (5 min).

### 18 · Frontier: learning stochastic dynamics from data (2023–2026) (2.8) · `s19_frontier` (new)
- Goal: where this calculus meets machine learning now, with one model trained on screen.
- Beats: **Replay (the hands-on core)**: a neural SDE market generator (`explainer/quant/house/nsde.py`: 2-dimensional latent SDE, drift and diffusion MLPs of width 32, Euler with 32 steps, torch with 2 threads) trained on 32-day windows of BTC daily log prices from 2018–2019. The loss is the squared distance between expected depth-4 signatures (time-augmented, lead-lag) of real and generated windows: the expected-signature MMD. The ai21 `replay` layout: left, generated path fans at checkpoints morphing from noise-like to BTC-like; right, the loss; 3 seeds as a band. **Measure** on the 2020 hold-out
  (registered with the trial counter): signature-MMD, the kurtosis of daily returns, and the lag-1 autocorrelation of |r|, against GBM (MLE) and an i.i.d. bootstrap of 2018–2019 returns at equal data. Narration branches. If the bootstrap matches the neural SDE on kurtosis and beats it on MMD, say so. Then the cards:
  - Issa, Horvath, Lemercier, Salvi (2023), "Non-adversarial training of Neural SDEs with signature kernel scores", NeurIPS 2023, arXiv 2305.16274: signature-kernel scoring rules replace the GAN discriminator, with applications including rough volatility and limit order books. Our loss is the linear-kernel cousin.
  - Cuchiero, Gazzani, Möller, Svaluto-Ferro (2025), "Joint calibration to SPX and VIX options with signature-based models", *Mathematical Finance* 35(1):161–213, arXiv 2301.13235: the price as a linear function of the signature of a polynomial diffusion; joint calibration without jumps or rough volatility.
  - Walker, McLeod, Qin, Cheng, Li, Lyons (2024), "Log Neural Controlled Differential Equations: The Lie Brackets Make a Difference", ICML 2024 (PMLR 235), arXiv 2402.18512: log-signatures and Lie brackets for sequence models.
  - Cont, Das (2024), "Rough volatility: fact or artefact?", *Sankhyā B* 86(1):191–223, arXiv 2203.13820 (ch15's caveat); against it, the SIAM monograph *Rough Volatility* (Bayer, Friz, Fukasawa, Gatheral, Jacquier, Rosenbaum, 2023), and Guyon, Lekeufack (2023), "Volatility is (mostly) path-dependent", *Quantitative Finance* 23(9):1221–1258: past returns explain up to 90% of the variance of index implied volatility (SSRN 4174589).
  - Bayer, dos Reis, Horvath, Oberhauser (eds., 2025/26), *Signature Methods in Finance*, Springer Finance, open access
    (DOI 10.1007/978-3-031-97239-3); Cass, Salvi (2024), "Lecture notes on rough paths and applications to machine learning", arXiv 2404.06583.
  - Degenne, Ledvinka, Marion, Pfaffelhuber (2025), "Formalization of Brownian motion in Lean", arXiv 2511.20118: the construction of BM via Kolmogorov extension and Kolmogorov–Chentsov is machine-checked in Mathlib, and stochastic integrals are announced as the next step. Ch1's construction, proved by a computer.
  - Context (pre-2023, one line): Gierjatowicz, Sabate-Vidales, Šiška, Szpruch, Žurič, "Robust pricing and hedging via neural SDEs", *J. Computational Finance* (arXiv 2007.04154); Kidger et al. (2021) neural SDEs as GANs (ICML).
- Experiment: `nsde` (3 seeds × ~8 min, checkpoint every 100 steps, resumable via `CACHE.partial`); `nsde_eval` (1 min).
- Pause-and-predict: "A generator matches the expected signature up to depth 4. Does it match the distribution of 32-day maxima?" (Not necessarily: the expected signature determines the law only under growth conditions and at all depths
  (Chevyrev–Lyons 2016); truncation loses it.)
- Compute: `nsde` (25 min), `nsde_eval` (1).

### O · The House, recap, desk questions, problems (2.6) · `s20_outro` (from s09 + s10)
- The House card: the simulation library (the test table moves into ch17 as the validation report; here, the org chart lights and Rule 6 is stated); trial counter.
- Recap in 11 lines (one per item), payoff card (Parts 9, 10, 13, 14, 16, 17, 19, 36, 42), and the reference card.
- Desk questions (README has the solutions): keep E[W⁴] (now answered in ch4) → replace with **"Expected time for BM to leave (−a, b)?"** (ab, Dynkin); keep "hit +1 before −2" (2/3); keep "digital by Girsanov" (e^{−rT}N(d₂)).
- Problem set (≈90 s): the existing 5, plus (6) "show E[τ_a] = ∞ from the first-passage density" and (7) "compute the Clark–Ocone integrand of W_T³". README carries the solutions in English and Chinese.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.8 | 10 Representation | 3.0 |
| 1 Construction | 2.8 | 11 Local time | 3.2 |
| 2 QV | 2.6 | 12 Lévy–Itô | 3.2 |
| 3 Itô integral | 3.2 | 13 Jumps in data | 2.8 |
| 4 Lemma | 2.8 | 14 Hawkes | 3.2 |
| 5 SDEs/schemes | 3.0 | 15 fBM | 3.0 |
| 6 OU/CIR | 2.8 | 16 Signatures | 3.2 |
| 7 FP/FK | 3.2 | 17 Industry | 3.0 |
| 8 Girsanov | 3.0 | 18 Frontier | 2.8 |
| 9 IS / vol | 2.6 | Outro | 2.6 |
| | | **Total** | **≈ 58.0** |

(≈ 8,100 spoken words at the ai21 rate. The gate `lecture_length.py --floor 50` leaves 8 minutes of slack if any chapter runs short.)

---

## 3b. Hands-on summary (the addendum)

**Replays (fitted or trained models shown learning):** ch6 CIR exact MLE (5 starts, regression baseline); ch14 Hawkes MLE
(8 starts, Poisson baseline); ch16 signature ridge regression over depth (5 splits, increments and last-value baselines); ch18 neural SDE (3 seeds; GBM and bootstrap baselines at equal data). Implementation: store iterates
(`scipy.optimize.minimize(callback=...)` for Nelder–Mead; ridge fits per depth; torch checkpoints every 100 steps), then the ai21 pattern: `tk = ValueTracker(0)`, an `always_redraw` step counter and a loss dot, a `Create` of each loss segment, `Transform` of the model's output per checkpoint, and seeds as `band(ax, x, lo, hi, color)`.

**Labs (code_block, ≤ 12 lines, then run):** (1) ch5 `sim.euler_maruyama` and `sim.milstein`; (2) ch6 `sim.ou_exact`;
(3) ch9 `sim.is_digital` (new); (4) ch14 `sim.hawkes_thinning` (Ogata); (5) ch15 `sim.fbm` (Davies–Harte);
(6) ch16 `sim.signature` (new). Sketch of the new one:

```python
def signature(path, depth):                 # Chen, segment by segment
    X = np.asarray(path, float); d = X.shape[1]
    S = [np.ones(())] + [np.zeros((d,) * k) for k in range(1, depth + 1)]
    for dx in np.diff(X, axis=0):
        seg = [np.ones(())]                       # exp of a straight segment
        for k in range(1, depth + 1):
            seg.append(np.multiply.outer(seg[-1], dx) / k)
        S = [sum(np.multiply.outer(S[i], seg[k - i]) for i in range(k + 1))
             for k in range(depth + 1)]           # S <- S (x) seg
    return S
```
and `is_digital(S0, K, sigma, T, n, seed)`: draw Z; θ = (log(K/S0) + σ²T/2)/(σT); Z' = Z + θ√T; w = e^{−θ√T Z' + θ²T/2}; return the mean and se of 1{S_T > K}·w. The screen run prints the running mean.

**Live simulations (drawn as they run, not finished plots):** Donsker rescaling and Lévy's midpoint refinement (ch1); the three running variation sums (ch2); the bet-ledger integral and left/midpoint sums converging (ch3); the tangent-plane misses stacking on the 3D surface (ch4); Picard iterates and Euler/Milstein paths per Δt (ch5); the OU fan filling its stationary law (ch6); the path fan with the FP surface rising (ch7); paths re-weighted by Z (ch8); running MC estimates and the σ̂-against-μ̂ race (ch9); hedge wealth tracking M_t (ch10); the occupation sandpile and the stop-loss ledger (ch11); the Poisson clock (ch12); the delta hedge stalling at a jump (ch13); thinning (ch14); the H dial (ch15); the helix (ch16); the variance-swap replicator (ch17).

**Compute budget (seeded; ≈ 70 CPU-minutes of 120):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| stoploss* | 1.5 | girsanov_paths | 0.3 | hawkes_rescale | 0.1 |
| construct | 0.1 | girsanov* | 0.1 | fbm*, fbm_morph | 0.3 |
| reflection | 0.5 | observability | 0.5 | pvar | 0.3 |
| variation*, signature* | 1.5 | hedge_rates | 3 | rough* | 1 |
| qv_live | 0.1 | tanaka | 0.5 | cont_das | 3 |
| ito*, wong_zakai | 0.5 | levy_layers | 0.2 | helix, sig_regression | 3 |
| lemma_column | 0.2 | jumps* | 0.5 | wti, bachelier_vs_black | 0.1 |
| orders*, picard | 1 | jump_hedge | 2 | varswap | 5 |
| mlmc | 5 | hawkes* | 0.5 | nsde (3 seeds, resumable) | 25 |
| rates*, cir_mle | 1.2 | hawkes_replay | 1 | nsde_eval | 1 |
| fp_surface, fk_check | 0.8 | hawkes_check | 1 | envelope* | 0.1 |

(* exists.) `nsde` uses `CACHE.partial` per seed and torch checkpoints every 100 steps, and `torch.set_num_threads(2)`; everything else is numpy and seconds to minutes. One command rebuilds the part: `python -m videos.quant.quant5.compute`. Trial counter: register `cir_mle` (DTB3), `nsde_eval` (2020 hold-out); the hold-out is inside the existing research window (to December 2020), so nothing new needs sealing.

**House library additions** (`explainer/quant/house/sim.py`, tests in `tests/test_quant_house.py`): `levy_construction` (midpoint refinement; variance per level checked), `signature(path, depth)` (Chen; unit square area
1, and agreement with `signature2`), `local_time(path, level, eps)` (E L₁⁰ = √(2/π)), `hawkes_compensator` (rescaled gaps mean 1), `cir_mle` (recovers parameters from simulated CIR), `mlmc` (unbiased against Black–Scholes), `heston_euler`
(full truncation; E v_T against θ + (v₀ − θ)e^{−κT}), `is_digital`. New module `explainer/quant/house/nsde.py`
(neural SDE + expected-signature loss; test: it fits a GBM's drift and volatility to within 10%).

---

## 4. Verified sources for the industry and frontier chapters

Checked this session by web search or fetch (2 Nov 2026):

| Fact | Source |
|---|---|
| CME 20-152 (8 Apr 2020) triggers; 20-171 (21 Apr 2020): switch to Bachelier, effective the margin cycle after 22 Apr trading, "to accommodate negative prices… and negative strikes" | https://www.cmegroup.com/content/cmegroup/en/notices/clearing/2020/04/Chadv20-171.html ; reversal to Black-76/Whaley 31 Aug 2020 per CQG (secondary, *(verify)*) |
| WTI May contract settled −$37.63 on 20 Apr 2020; IB: $1.75M penalty, $82.57M restitution (credited), 28 Sep 2021; "did not adequately prepare and configure its electronic trading system to recognize negative prices" | https://www.cftc.gov/PressRoom/PressReleases/8432-21 |
| FRED DCOILWTICO 2020-04-20 = −36.98 (fetched; the test fetch's manifest line was reverted) | https://fred.stlouisfed.org/series/DCOILWTICO |
| IB provisional loss ≈ $88M (Apr 2020), ≈ $104M (Q2 2020 results) | https://www.businesswire.com/news/home/20200421005853/en ; https://www.businesswire.com/news/home/20200721005909/en |
| SR 11-7 (4 Apr 2011); SR 26-2 (17 Apr 2026, Fed/OCC/FDIC) supersedes SR 11-7 and SR 21-8 | https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm ; https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm |
| OCC STANS: "large-scale Monte Carlo simulations to forecast price and volatility movements" | https://www.theocc.com/Risk-Management/Margin-Methodology ; SEC filing https://www.sec.gov/files/rules/sro/occ/2020/34-90763.pdf |
| Giles & Glasserman (2006) "Smoking adjoints", *Risk* | https://www.risk.net/1500261 |
| Danske Bank, Risk In-House System of the Year 2015, AAD, CVA in ~10 s | https://www.risk.net/derivatives/2387869/house-system-year-danske-bank |
| STAC-A2: Heston MC Greeks, multi-asset path-dependent, early exercise; H100 8.9 ms *(verify in the report)* | https://docs.stacresearch.com/node/47892 ; https://stacresearch.com/system/files/resource/files/STAC_Intel_Webinar_27sep13-final_0.pdf |
| QuantLib Sobol + Brownian-bridge path generators | https://rkapl123.github.io/QLAnnotatedSource/d3/dd6/class_quant_lib_1_1_sobol_brownian_generator_base.html |
| Demeterfi, Derman, Kamal, Zou (1999), GS QS note / *J. Derivatives* 6(4):9–32; Cboe VIX methodology (variance-swap weighting) | https://emanuelderman.com/?p=5675 ; https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf |
| Hardiman, Bercot, Bouchaud (2013): n ≈ critical, E-mini 1998–2011 | https://arxiv.org/abs/1302.1405 |
| Issa, Horvath, Lemercier, Salvi, NeurIPS 2023 | https://arxiv.org/abs/2305.16274 |
| Cuchiero, Gazzani, Möller, Svaluto-Ferro, *Math. Finance* 35(1) 2025 | https://arxiv.org/abs/2301.13235 ; https://ideas.repec.org/a/bla/mathfi/v35y2025i1p161-213.html |
| Walker et al., ICML 2024 | https://arxiv.org/abs/2402.18512 ; https://proceedings.mlr.press/v235/walker24a.html |
| Cont, Das, *Sankhyā B* 86 (2024) | https://arxiv.org/abs/2203.13820 ; https://ideas.repec.org/a/spr/sankhb/v86y2024i1d10.1007_s13571-024-00322-2.html |
| Guyon, Lekeufack, *QF* 23(9) 2023 | https://papers.ssrn.com/abstract=4174589 |
| *Rough Volatility*, SIAM 2023, ISBN 978-1-61197-777-6 | https://doi.org/10.1137/1.9781611977783 |
| *Signature Methods in Finance* (Springer Finance, OA) | https://link.springer.com/book/9783031972386 |
| Cass, Salvi (2024) lecture notes | https://arxiv.org/abs/2404.06583 |
| Degenne, Ledvinka, Marion, Pfaffelhuber (2025) Lean BM | https://arxiv.org/abs/2511.20118 |
| Gierjatowicz et al., *J. Comput. Finance* | https://arxiv.org/abs/2007.04154 ; https://www.risk.net/journal-of-computational-finance/7956062 |

Unverified this session (keep the marks): Kamal–Derman (1999) "When you cannot hedge continuously" (*Risk*) and its √(π/4) constant; the CQG-reported 31 Aug 2020 reversal date; the STAC H100 figure; Laursen–Foster–Post (2024) Isabelle BM formalization (arXiv 2410.14718, seen in a search listing only).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 5 · Stochastic Calculus (~58)
1. Brownian motion as a limit (Donsker) and a construction (Lévy's midpoints, the Brownian bridge); the reflection
   principle and first passage; quadratic variation, proved and measured (the volatility signature plot).
2. The Itô integral built from simple integrands; the isometry and martingale property proved; Stratonovich and the
   Wong–Zakai theorem.
3. Itô's lemma proved, in several dimensions; Lévy's characterization and the Dambis–Dubins–Schwarz time change; SDEs:
   existence and uniqueness (Picard); Euler–Maruyama and Milstein with orders computed; multilevel Monte Carlo.
4. Ornstein–Uhlenbeck and CIR solved, fitted by exact likelihood (Feller's boundary); the generator, Dynkin,
   Fokker–Planck and Feynman–Kac (proved), with the density surface in 3D.
5. Girsanov and Cameron–Martin: drift is a change of measure (paths re-weighted, not moved); Novikov; importance
   sampling; volatility is observable, drift is not.
6. Martingale representation (proved through exponentials) and Clark–Ocone: why a hedge exists, and when it does not.
7. Local time, Tanaka (derived by smoothing the kink), occupation density, Lévy's identity; the stop-loss start-gain
   paradox (Carr–Jarrow 1990).
8. Jumps: Poisson, compensators, compound Poisson, Lévy–Khintchine and Lévy–Itô, Itô for jumps; jumps in Bitcoin
   (bipower variation) and the hedge they break.
9. Point processes with memory: Hawkes (1971), the branching ratio, Ogata's thinning, likelihood, and the
   time-rescaling test. Comes back in 14 and 36.
10. Fractional Brownian motion: Hurst H, Mandelbrot–Van Ness, not a semimartingale; volatility's roughness measured,
    and the Cont–Das caveat.
11. Rough paths and signatures (Chen 1957; Lyons 1998): Lyons' helix, Chen's identity, universality, regression on
    signatures. Come back in 14, 17 and 42.

*Textbooks:* Shreve II ch. 3–6, 11; Øksendal ch. 2–5, 7–8; Karatzas–Shreve ch. 2–3, 5; Cont–Tankov ch. 2–3, 6–8; Björk
ch. 4–5; Friz–Hairer ch. 1–3. Filtering (Øksendal 6) → Part 7; optimal stopping and control → Part 8.
*Computed:* reflection with the discrete-monitoring shift; QV and the BTC signature plot; Wong–Zakai; strong and weak
orders, MLMC cost; CIR exact MLE on DTB3; Fokker–Planck surfaces and a Feynman–Kac Monte Carlo check; Girsanov
re-weighting and effective sample size; hedge-error rates (W_T², a call, a second noise); stop-loss against local
time; BTC jumps and the jump hedge floor; Hawkes MLE and time-rescaling on BTC; the Cont–Das artefact; signature
regression; variance-swap replication with and without jumps; a neural SDE market generator.
*Visuals:* Lévy's midpoint construction; QV accumulating; the 3D tangent-plane misses; `PathFan` under the
Fokker–Planck surface (Feller's wall at 0); paths re-weighted by Z; the occupation sandpile; the Lévy–Itô layer cake;
thinning and the time-warp; the H dial; Lyons' helix in 3D.
*Labs:* `euler_maruyama`/`milstein`, `ou_exact`, `is_digital`, `hawkes_thinning`, `fbm`, `signature`.
*Industry:* CME's switch to Bachelier (April 2020); OCC's Monte Carlo margin; adjoint Greeks; STAC-A2; the VIX as
Itô's lemma; SR 11-7 → SR 26-2. *Frontier:* neural SDEs trained with signature scores (Issa et al. 2023);
signature-based SPX/VIX calibration (Cuchiero et al. 2025); Log-NCDEs (Walker et al. 2024); rough or not (Cont–Das
2024; Guyon–Lekeufack 2023); Brownian motion formalized in Lean (Degenne et al. 2025).
*Crisis:* 20 April 2020, WTI at −$37.63: a GBM cannot go there. *Firms:* CME Clearing; Interactive Brokers
(CFTC 2021); the banks' quant libraries (Danske's AAD).
*Note:* `stochastic` is the gentle version; this part assumes it.
*Desk:* "Expected time for Brownian motion to leave (−a, b)?"; "Probability Brownian motion hits 1 before −2?";
"Price a digital by Girsanov."
*House:* the simulation library (used by every pricing part), validated by Rule 6.
```

---

## 6. Implementation notes

- New scene files follow the numbering above (`s01_hook` … `s20_outro`). **Renaming modules invalidates the narration and manim caches** (CLAUDE.md), so the scenes that are only deepened can keep their module and class names, with new scenes inserted (e.g. keep `s02_brownian` as chapter 2, add `s02a_construct`); the manifest controls the order.
- 3D scenes (`VoiceoverScene, ThreeDScene`, as in `quant12/s01_hook.py` and `ai5/s15_mcmc.py`): ch4 lemma surface, ch7 FP surface and Feller wall, ch16 helix. Use `price_surface`/`loss_surface`, `add_fixed_in_frame_mobjects` for text, and reset the camera at the end of each block.
- Every narrated number is an f-string over the cache; the branches named above (MLMC ratio, CIR Feller ratio, KS verdicts, the Cont–Das H, signature R², the neural SDE against the bootstrap) must be computed verdicts.
- New on-screen strings go into `quant_text_zh.json`; new terms for `QUANT_ZH_GUIDE.md`: 局部时 (local time), 占位密度
  (occupation density), 反射原理 (reflection principle), 多层蒙特卡洛 (multilevel MC), 路径签名 (path signature), 列维面积
  (Lévy area), 时间变换 (time change), 补偿子 (compensator), 分支比 (branching ratio), 神经随机微分方程 (neural SDE).
- README: chapter list with minutes, the textbook audit table (§2b), the full paper list, 3 desk questions and 7 problems with solutions in English and Chinese.
