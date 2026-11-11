# Part 12 · The Volatility Surface: expansion plan (15.5 → ~58 min)

Planning document only; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 (the
November 2026 standard), §2 (the Surface, the trial counter), §6 Parts 9–17; `READING.md` §1, the Gatheral coverage map
and §4 Part 12; `videos/ai/LECTURE_GUIDE.md`; every file in `videos/quant/quant12/` (manifest, common, compute, nine
scenes, README, zh_lines); `explainer/quant/viz.py` (`lab_card`/`lab_run`, `TrainingReplay`, `seed_band`,
`price_surface`, `smile_points3d`, `readout`); the House modules `volsurface.py`, `smile.py`, `surface.py`, `bs.py`,
`stochvol.py`, `arbitrage.py`, `deep.py`, `rough.py` (signatures); the manifests of Parts 9, 10, 11, 13, 14, 17 and the plans
`videos/quant/plans/quant5.md` (format) and `quant9.md` (overlap). Probe scripts and downloads are in
`scratchpad/q12/` (`p1.py` … `p5.py`, `dl/`); every number below marked **(probe)** was computed this session on the
cached data and must be recomputed by `compute.py`.

**What the neighbours already own (do not repeat).** Part 9 derives Breeden–Litzenberger, butterflies as state prices,
a first SVI fit with its density, and names Lee's bound. Part 10 inverts implied volatility and shows the first smile.
Part 11 owns Sinclair's forecast edge and gamma scalping. Part 13 owns Heston/SABR/SLV, the cross-model forward smile
and the SPX/VIX puzzle. Part 14 owns the skew's power law, rough volatility, 5 August 2024. Part 17 owns neural
calibrators and market generators. Part 12 is therefore the home of: the surface as an object (shape, quoting,
dynamics), static arbitrage in total-variance form, SVI/SSVI fitted properly, Dupire/Gyöngy/local-vol dynamics,
variance and volatility swaps, the VIX and DVOL, the variance risk premium and SVIX, VIX futures and ETPs, dealer gamma
and 0DTE, and learning surfaces.

**Cadence.** 21 scenes (hook, 19 chapters, outro), about **58 min** (≈ 8,050 words at 139 wpm). A chapter runs 2.5–3.0
min (350–420 words).

---

## 1. Current state (`python tools/lecture_length.py quant12`: 15.5 min)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 1.6 | Good 3D tour of the Surface (254 quotes, SSVI at 0.74 vol pts vega-weighted), objectives, House. **No history segment** (the standard requires "how we got here"). |
| 1–2 | `s02_smile` Smile | 2.5 | Three SVI slices; RR/BF ladder; sticky test (moneyness 2.6 vs strike 3.0 vol pts); then g, calendar, Lee, SSVI as a 3-row ladder. **Two syllabus items squeezed into one scene; g, Lee and SSVI's theorems quoted, not derived; no arbitrage ever shown happening; SVI never fitted on screen.** |
| 3 | `s03_localvol` LocalVol | 1.5 | Dupire/Gyöngy as a 3-row ladder; LV curves; forward skew 3.4 vs 6.5. **Dupire not derived; Derman–Kani a name; Gyöngy not checked; no 3D.** |
| 4 | `s04_varswap` VarSwap | 1.6 | Itô + Carr–Madan ladder; 1/K² strip bars; √K_var 48.8% vs ATM 43.7%; our VIX 48.8% vs DVOL 45.9%. **VIX recipe not shown; no replication run; no vol swap; jumps not mentioned.** |
| 5 | `s05_vrp` VRP | 1.7 | 100 weekly surfaces: 54% implied vs 47.6% realized, positive 76% of weeks, NW t = 3.6; SVIX bound 31%. **Static plots; no SPX benchmark; BTZ predictability not tested; SVIX not derived (README only).** |
| 6 | `s06_volmageddon` Volmageddon | 2.2 | Crisis card (VIX 17.31 → 37.32, +116%), roll text, GEX ladder, Baltussen and 0DTE in text. **No futures data, no rebuild of the note, no simulation of gamma feedback; item 10 (VIX futures, roll, ETPs) has no chapter.** |
| 7 | `s07_learning` Learning | 1.5 | VAE: 1.9 vol pts, corr(z₁, ATM) 0.96, latent walks. **Training not replayed; one seed; the "arbitrage-free neural SVI" of the syllabus is absent.** |
| 8 | `s08_house` House | 0.8 | Function table, Rule 12, counter 73. |
| — | `s09_outro` Outro | 2.0 | Recap 8 lines, 3 desk questions, 5 problems, payoffs, references. |

Overall: real and good numbers (keep all), but every idea gets one ladder and one static plot. **No lab, no replay, no
live simulation, only one 3D moment, no industry or frontier chapter, no history thread.** Syllabus items 1, 2, 3, 4
each need a full chapter or two; items 5, 7, 10 are missing as chapters.

---

## 2. Audit

### (a) Syllabus items (current §6 entry) → chapters of §3

| Item | Now | Plan |
|---|---|---|
| 1 Smile, skew, term structure; delta quoting; sticky strike vs sticky delta | ch1–2, 1.3 min | ch1 (shape, term structure), ch2 (quoting, stickiness, SSR, PCA dynamics) |
| 2 Static no-arbitrage: butterfly, calendar, Roper, Lee | half of ch2 | ch3 (derived; Vogt's arbitrage glowing; Lee's moments on the Surface) |
| 3 SVI and SSVI fitted | one ladder row | ch4 (SVI, JW, fit replay, lab), ch5 (SSVI theorems, 3D replay, lab) |
| 4 Dupire derived; Derman–Kani; Gyöngy | ladder | ch6 (derivation, 3D LV surface, implied tree), ch7 (Gyöngy checked by Monte Carlo) |
| 5 Local volatility's forward smile | half of ch3 | ch8 (forward smile, LV dynamics: smile moves the wrong way, SSR = 2) |
| 6 Variance swaps and the log contract | ch4 | ch9 (derivation, strip, truncation, jumps), ch10 (replication on real BTC; vol swaps) |
| 7 The VIX; our index vs DVOL | half of ch4 | ch11 (Cboe recipe lab; 100-week DVOL comparison; VIX history) |
| 8 VRP (Carr–Wu; BTZ); SVIX | ch5 | ch12 (BTC + SPX 1990–2025; P&L skew; BTZ test), ch13 (SVIX derived; risk-neutral moments) |
| 9 Dealer gamma, intraday momentum, 0DTE | text | ch16 (GEX derived; feedback simulated live; 0DTE record) |
| 10 VIX futures, the roll, short-vol ETPs | **missing** | ch14 (VX futures from Cboe; rebuild the index and the inverse note), ch15 (Volmageddon) |
| 11 Learning surfaces | ch7 | ch17 (VAE replay with seeds; arbitrage-penalised neural surface vs SSVI, replayed) |
| Industry / frontier | — | ch18, ch19 |

### (b) Textbook sections → chapter (or another part)

Gatheral's TOC was checked against the Wiley/Eyrolles listings and a scanned contents page (11 chapters, below). The
other books' chapter numbers are from memory and marked *(verify)*.

| Book · section | Here / elsewhere |
|---|---|
| **Gatheral** 1 Stochastic and local volatility (Dupire derivation, local variance as conditional expectation of instantaneous variance, BBF "local ≈ average", implied as average of local along the most likely path) | ch6, ch7, ch8 |
| Gatheral 2 The Heston model | Part 13 (ch7 uses Heston only as the Gyöngy test-bed) |
| Gatheral 3 The implied volatility surface (SVI, the Heston fit, the "skew = ½ local skew" rule, the term structure of ATM skew) | ch4, ch6; skew term structure → Part 14 |
| Gatheral 4 The Heston–Nandi model (local variance in Heston–Nandi; numerical LV) | ch7 (LV of a stochastic-vol model, computed); details → Part 13 |
| Gatheral 5 Adding jumps · 6 Modeling default | Part 13 (ch9 shows the jump term of a variance swap) |
| Gatheral 7 Volatility surface asymptotics (Lee's extreme-strike formula; short and long expiry) | ch3 (Lee), ch4 (SVI's long-maturity Heston limit); short-expiry → Part 14 |
| Gatheral 8 Dynamics of the volatility surface (skew dynamics under SV and LV) | ch2, ch8 |
| Gatheral 9 Barrier options · 10 Exotic cliquets | Part 15; Part 13 (cliquets) |
| Gatheral 11 Volatility derivatives (variance and volatility swaps, VIX, options on variance) | ch9, ch10, ch11, ch14; options on VIX → Part 13 |
| **Bergomi** 1 Introduction (Black–Scholes P&L, carry) | Parts 10–11 *(verify chapter)* |
| Bergomi 2 Local volatility (market model, vega hedge, SSR = 2 in LV, forward smile of LV) | ch6, ch8 |
| Bergomi 3 Forward-start options | ch8 (LV); Part 13 (SV) |
| Bergomi 4 Stochastic volatility, introduction · 6–7 forward variance and two-factor models | Part 13 |
| Bergomi 5 Variance swaps (forward variances, log contracts, large returns, strike discreteness, weighted variance swaps) | ch9, ch10 (both effects computed) |
| Bergomi 8 LSV · 9 The smile of SV models · 10 What causes the ATMF skew | Parts 13, 14 *(Routledge listing confirms these chapter titles; order verify)* |
| **Rebonato** *Vol & Corr* — implied vs instantaneous volatility; local volatility and its dynamics; smile dynamics "sticky" regimes | ch2, ch6, ch8 *(verify chapter numbers)* |
| Rebonato — correlation chapters | Parts 15, 20, 40 |
| **Hull** OFOD "Volatility smiles and volatility surfaces" (put–call parity argument, FX vs equity smiles, the implied distribution, determining the surface, Greeks with a smile) | ch1, ch2 (Greeks under stickiness) |
| Hull "More on models and numerical procedures" (CEV, the implied volatility function model, mixed jump–diffusion) | ch6 (IVF = local vol); CEV and jumps → Part 13 *(verify ch. 20 / 27 numbering for the 11th edition)* |
| **Sinclair** *Volatility Trading* — variance swaps, VRP, the VIX | ch9–ch12; forecasting edge → Part 11 |
| **Bennett** *Trading Volatility* — skew and term-structure trading, variance and volatility swaps, VIX futures, dispersion | ch2, ch9–ch11, ch14; dispersion → Part 11 *(verify chapter list)* |
| Cont–Tankov / Lewis | Part 13 |

### (c) Papers on the Part 12 list (READING.md) → where they appear

| Paper | Now | Plan |
|---|---|---|
| Derman–Kani 1994 "Riding on a smile" | named | ch6: the implied tree drawn, nodes bent by the skew |
| Dupire 1994 "Pricing with a smile" | ladder | ch6: derivation in full |
| Rubinstein 1994 "Implied binomial trees" (JF) | absent | ch6 card (and Part 13's post-1987 crisis) |
| Gyöngy 1986 | ladder | ch7: proved in outline and checked by Monte Carlo |
| Demeterfi–Derman–Kamal–Zou 1999 | credit | ch9 (strip), ch10 (vol-swap convexity) |
| Derman 1999 "Regimes of volatility" | absent | ch2: the three regimes as a dial |
| Britten-Jones–Neuberger 2000 (JF) | absent | ch9: model-free implied variance |
| Cont–da Fonseca 2002 (QF) | absent | ch2: PCA of surface moves, computed |
| Lee 2004 (MF) | named | ch3: derived; wings on the Surface |
| Gatheral 2004 SVI | named | ch4 |
| Carr–Wu 2009; BTZ 2009 | text | ch12 (BTZ predictability tested) |
| Roper 2010 | name | ch3: the conditions card |
| Gatheral–Jacquier 2014 | ladder | ch5: both theorems; Vogt's example in ch3 |
| Martin 2017 (QJE) | ch5 | ch13: derived on screen |
| Ackerer–Tagasovska–Vatter 2020 (NeurIPS) | absent | ch17: the penalised network is its recipe |
| Baltussen–Da–Lammers–Martens 2021 (JFE 142(1):377–403, verified) | text | ch16 |
| Bergeron–Fung–Hull–Poulos 2022 | credit | ch17 |
| Bandi–Fusari–Renò 2023 "0DTE option pricing" (SSRN 4503344, verified) | text | ch16 card |
| Beckmeyer–Branger–Gayda 2023 | absent | ch16 one line *(verify title/venue)* |
| Dim–Eraker–Vilkov 2024 (SSRN 4692190; title verified, findings not read) | text | ch16 card, findings to be read before stated |
| Cboe VIX White Paper; Deribit DVOL methodology | partial | ch11 |

**Proposed additions (classic):** Neuberger (1994) "The log contract", *JPM*; Carr–Madan (1998) "Towards a theory of
volatility trading"; Hagan–Kumar–Lesniewski–Woodward (2002) "Managing smile risk", *Wilmott* (LV's smile moves the wrong
way, ch8); Berestycki–Busca–Florent (2002) *QF* (ch6); Bakshi–Kapadia–Madan (2003) *RFS* (risk-neutral moments, ch13);
Backus–Foresi–Wu (2004) Gram–Charlier smile (ch1); Fengler (2009) "Arbitrage-free smoothing of the implied volatility
surface", *QF* (ch17 baseline); Zeliade (2009) "Quasi-explicit calibration of Gatheral's SVI model" (ch4); Carr–Lee
(2009) "Volatility derivatives", *Annu. Rev. Fin. Econ.* (ch10); Cheng–Madhavan (2009) "The dynamics of leveraged and
inverse ETFs" (ch14); Gatheral–Jacquier (2011) "Convergence of Heston to SVI", *QF* (ch4); Andreasen–Huge (2011)
"Volatility interpolation", *Risk* (ch18); Andersen–Fusari–Todorov (2017) "Short-term market risks implied by weekly
options", *JF* (ch16); Dew-Becker–Giglio–Le–Rodriguez (2017) "The price of variance risk", *JFE* (ch12); Johnson (2017)
"Risk premia and the VIX term structure", *JFQA* (ch14); Griffin–Shams (2018) "Manipulation in the VIX?", *RFS* 31(4)
(verified: doi 10.1093/rfs/hhx085; ch15); Martin–Wagner (2019) "What is the expected return on a stock?", *JF* (ch13);
Hendriks–Martini (2019) "The extended SSVI volatility surface", *J. Comput. Finance* (ch5). Volumes/pages *(verify)*
except where stated.

**Proposed additions (2023–2026 frontier, verified this session):** Vuletić–Cont, "VolGAN: a generative model for
arbitrage-free implied volatility surfaces", *Applied Mathematical Finance* 31(4):203–238 (2024; online 2025);
Wiedemann–Jacquier–Gonon, "Operator deep smoothing for implied volatility", ICLR 2025, arXiv 2406.11520;
Kelly–Kuznetsov–Malamud–Xu, "Deep learning from implied volatility surfaces", SFI RP 23-60, SSRN 4531181 (2023);
Martini–Mingone, "No arbitrage SVI", *SIAM J. Financial Math.* (2022), arXiv 2005.03340, and "No arbitrage global
parametrization for the eSSVI volatility surface", *QF* 22(12):2205–2217 (2022), arXiv 2204.00312;
Bandi–Fusari–Renò (2023) as above.

---

## 3. The chapter list (21 scenes, about 58 min)

Conventions as in quant5.md. **Visual** = the signature picture, built before the formula. **Live** = drawn as it is
simulated. **Lab** = `lab_card` + `lab_run` with House code (≤ 12 lines) and its cached output. **Replay** =
`TrainingReplay` or ValueTracker scrub, seeds as `seed_band`. **Compute** = `compute.py` item, CPU minutes on one core
under contention. Every narrated number is an f-string over the cache; branches are computed verdicts.

Module plan: existing modules and classes are kept for chapters they still carry (`s01_hook.Hook`, `s02_smile.Smile`,
`s03_localvol.LocalVol`, `s04_varswap.VarSwap`, `s05_vrp.VRP`, `s06_volmageddon.Volmageddon`, `s07_learning.Learning`,
`s09_outro.Outro`); new chapters get inserted modules (`s02a_…`); `manifest.py` sets the order. `s08_house` leaves the
manifest (its table moves into ch18, its Rule 12 into the outro); delete the module or keep it unlisted (lead's choice).
Chapter numbers on `chapter_card`s change (LocalVol becomes 6, etc.); narration is rewritten anyway.

### H · Hook: "The shape of fear" (2.8 min) · `s01_hook` (deepened)
- Goal: the object, the era, the map.
- Beats: (1) keep the 3D tour of the Surface (dots, then SSVI surface, camera orbit). (2) **New, "how we got here" (≈70 s):**
  timeline strip lit 1973 (flat: one σ), 1987 (crisis red: the skew is born), 1993 (VIX on S&P 100, Whaley), 1994
  (Dupire, Derman–Kani, Rubinstein), 1999 (DDKZ at Goldman), 2003 (VIX moves to SPX strips), 2004 (VIX futures; SVI),
  2009 (VRP papers), 2014 (SSVI), 2018 (Volmageddon, red), 2021 (DVOL), 2023 (VIX1D; 0DTE boom), 2024 (IBIT options).
  While the strip lights, a flat plane in the same 3D axes **bends into the 1987 skew** (a ValueTracker morphs
  σ(k,T) = σ₀ → the fitted SSVI). (3) Objectives (12 rows). (4) House card.
- Pause-and-predict: "Black–Scholes says this surface is flat. Which corner is highest, and why?" (Short-dated
  downside: crash insurance.)
- Compute: `surface` (exists).

### 1 · The smile, read (2.8) · item 1 · `s02_smile` (rewritten: shapes only)
- Goal: what the shape means: skewness and kurtosis of the risk-neutral law; term structure; Bitcoin vs SPX.
- Beats: **Visual (2D→3D)**: the three slices drawn as dots, the SVI curves grow through them; then each slice is lifted
  back into the 3D surface (camera rotates from front view into the tour pose), so "smile" and "surface" are one object.
  Then a **live density morph**: a slider adds negative skewness / excess kurtosis to a lognormal; the right panel
  shows the implied smile it produces (BS inversion of the Gram–Charlier prices) tilting and curling in step.
  Then the term structure over two years: the 7/30/90/180-day ATM vols of the 100 weekly surfaces as four traces, the
  inverted weeks shaded. Then the skew's sign through time (BTC call-skew weeks lit gold).
- Derivation:
  - $w(k,T) = \sigma_{\rm imp}^2(k,T)\,T$, $k = \ln K/F$ (total implied variance; the natural coordinate).
  - $q(x) \approx \phi(x)\big[1 + \tfrac{\gamma_1}{6}He_3(x) + \tfrac{\gamma_2}{24}He_4(x)\big]$ (Gram–Charlier: skewness γ₁ and excess kurtosis γ₂ as corrections).
  - $\sigma_{\rm imp}(d) \approx \sigma\big[1 - \tfrac{\gamma_1}{6}d + \tfrac{\gamma_2}{24}(d^2-1)\big]$, $d = -k/(\sigma\sqrt T)$ (Backus–Foresi–Wu: price the corrected density, invert to first order).
  - So γ₁ < 0 ⇒ puts (d > 0) dearer: skew; γ₂ > 0 ⇒ both wings up: smile (read off the formula).
  - $\sigma^2_{\rm fwd}(T_1,T_2) = \frac{w(0,T_2)-w(0,T_1)}{T_2-T_1}$ (forward variance from the term structure; must be ≥ 0, ch3).
- Experiment: `termskew` (new, from `history`): **(probe)** mean ATM 49.2% (7d), 50.8% (30d), 53.8% (90d), 56.3% (180d):
  upward on average; 7d above 180d in 15% of weeks, 30d above 90d in 13%; 30-day skew σ(−0.1) − σ(+0.1) averaged
  −0.35 vol pts and was a **call skew in 64% of weeks** (corr with the week's return 0.18). Narration branches on the
  share: BTC 2024–25 was mostly call-skewed, unlike the SPX since 1987, while the Surface day itself is put-skewed.
- Pause-and-predict: "A market whose risk-neutral returns have positive skewness: which way does its smile tilt?" (Toward calls.)
- Compute: `termskew` (<0.1).

### 2 · How the surface moves: quoting, stickiness, factors (3.0) · item 1 · `s02a_dynamics` (new)
- Goal: delta quoting; the three "regimes" of Derman (1999); the skew-stickiness ratio; the principal components of moves.
- Beats: (1) **Visual**: the 30-day smile on a strike axis and, beneath it, the same smile on a delta axis; a ValueTracker
  moves spot ±8%; in "sticky strike" the curve stays put on the strike axis, in "sticky moneyness/delta" it slides with
  spot; a third mode ("local vol", ch8) slides it the *other* way. A readout shows ATM vol under each. (2) The day test
  (exists) and the **weekly test** over 99 pairs, drawn as two error bars per week. (3) **SSR dial**: the measured ratio on a
  0–2 dial with markers 0 (sticky moneyness), 1 (sticky strike), 2 (local vol). (4) **PCA live**: the 99 weekly changes of
  the 17 × 6 log-vol grid; the three eigen-surfaces appear in 3D one by one, each animated by ±2 sd of its score (level
  breathing, term twist, skew tilt); explained-variance bars fill.
- Derivation:
  - $\Delta_C = N(d_1)$, $d_1 = \frac{-k + w/2}{\sqrt w}$, so $k_{25C} = 0.674\,\sigma\sqrt T + \tfrac12\sigma^2 T$ (invert $N(d_1) = 0.25$).
  - $\mathrm{RR}_{25} = \sigma_{25C}-\sigma_{25P}\approx \partial_k\sigma\cdot(k_{25C}-k_{25P})$ (first order: RR measures the slope; BF the curvature).
  - Skew-stickiness ratio $R = \dfrac{d\sigma_{\rm ATM}/d\ln S}{\partial_k\sigma|_{k=0}}$ (Bergomi's definition).
  - Sticky strike: $\sigma_{\rm ATM}(S) = \sigma(K{=}S)$ ⇒ $R = 1$; sticky moneyness: $\sigma(\ln K/S)$ fixed ⇒ $R = 0$ (differentiate).
  - $\partial_{\ln S}\sigma(K) = (R-1)\,\partial_k\sigma$, hence $\Delta = \Delta_{BS} + \mathcal V\,\frac{(R-1)\,\partial_k\sigma}{S}$ (chain rule: the smile's dynamics change the hedge).
  - PCA: $\Delta X_t = \sum_i s_{i,t} f_i$, $f_i$ eigenvectors of $\operatorname{cov}(\Delta X)$ (Cont–da Fonseca 2002).
- Experiment: `dynamics` (new): **(probe)** weekly sticky-moneyness RMSE 3.57 vol pts vs sticky strike 4.09 (strike better in
  only 25% of weeks); PCA explained variance 68.5%, 16.4%, 8.2%, 4.3% (PC1 loads 0.17 at 7 days falling to 0.03 at 180:
  short end moves most; PC2 a term twist; PC3 tilts the skew, −0.155 → +0.137 across k at 30d). SSR by regression
  2.4 but corr(Δln S, ΔATM) = 0.05 and mean skew ≈ 0: **not identified in BTC** (the narration must say so, not quote
  2.4 as a fact; branch on the regression's t-stat). Cont–da Fonseca found three factors explain most SPX/FTSE moves; ours: the computed sum.
- Pause-and-predict: "Spot falls 5%, skew is −0.4 vol pt per 1% moneyness, sticky strike. ATM vol?" (+2 points.)
- Compute: `dynamics` (<0.1).

### 3 · Static arbitrage: what shapes are impossible (3.0) · item 2 · `s02b_arbitrage` (new)
- Goal: derive the butterfly condition in total variance, the calendar condition, Lee's wing bound; watch an arbitrage.
- Beats: **Visual**: Vogt's SVI smile (from Gatheral–Jacquier 2014) looks harmless; beneath it Gatheral's g(k) is drawn
  left to right and **dips below zero, glowing red, on k ∈ [0.64, 1.26]**; the implied density goes negative there;
  then three call prices at strikes around k = 0.88 assemble a butterfly whose price is printed negative ("you are paid
  to own a non-negative payoff"). Calendar: two total-variance curves crossing, the crossing region glowing. Lee: the
  wings of w(k) against the lines w = 2|k|; each Surface expiry's wing slopes appear as rays, with the implied moment
  number beside them. Roper's conditions as a checklist card that ticks for the Surface.
- Derivation:
  - $C(K)$ convex and decreasing, $\partial_{KK}C = q(K) \ge 0$ (Part 9's density; recalled in one line).
  - $C = F\big[N(d_+) - e^kN(d_-)\big]$, $d_\pm = -k/\sqrt w \pm \sqrt w/2$ (Black in total variance).
  - $q(K) = \frac{g(k)}{K\sqrt{2\pi w}}\,e^{-d_-^2/2}$, $g = \big(1-\frac{k w'}{2w}\big)^2 - \frac{w'^2}{4}\big(\frac1w+\frac14\big) + \frac{w''}{2}$ (differentiate twice in $k$, using $e^kN'(d_-) = N'(d_+)$).
  - No butterfly arbitrage ⇔ $g \ge 0$ (the prefactor is positive).
  - No calendar arbitrage ⇔ $\partial_T w(k,T) \ge 0$ at fixed $k$ (at fixed moneyness the call is the price of a convex payoff of a martingale, increasing in $T$; Gatheral–Jacquier Lemma 2.1).
  - Lee: if $w(k) \sim \beta k$ then $d_+ \sim \sqrt k\,(\sqrt\beta/2 - 1/\sqrt\beta)$, and $C/F \to 0$ needs $d_+\to-\infty$ ⇒ $\beta \le 2$.
  - $\beta_R = 2 - 4\big(\sqrt{\tilde p^2+\tilde p}-\tilde p\big)$, $\tilde p = \sup\{p: \mathbb E S_T^{1+p}<\infty\}$, i.e. $\tilde p = \frac{(2-\beta_R)^2}{8\beta_R}$ (Lee 2004; invert).
- Experiment: `arbitrage` (new): **(probe)** Vogt's smile: g_min = −0.033 at k = 0.88, negative on [0.64, 1.26]; negative
  density mass −4.3·10⁻⁵ (tiny, far wing: hard to see in prices, easy to see in g). Butterfly price at k = 0.88 to be
  computed (negative). Lee on the Surface's SVI fits: wing slopes β_L/β_R grow from 0.03/0.01 (1 day) to 0.35/0.20
  (289 days): implied right-moment p̃ = 2.1 and left q̃ = 1.0 at 289 days, all β well under 2 (no wing arbitrage).
  `arbitrage.static_checks` (Part 9's checker) run on every expiry: violations 0 (computed).
- Pause-and-predict: "A smile's right wing has slope 2.5 in total variance. What can you do?" (Sell the far call for
  more than its maximum value relation allows: arbitrage; β must be ≤ 2.)
- Compute: `arbitrage` (<0.1).

### 4 · SVI: a smile in five numbers, fitted (2.8) · item 3 · `s02c_svi` (new)
- Goal: where SVI comes from, what its parameters mean, how it is fitted, how fits go wrong.
- Beats: **Visual**: the raw-SVI hyperbola with five sliders, each moving one feature (a lifts, b opens the wings, ρ
  tilts, m shifts, σ rounds the vertex), with its asymptotes drawn. Then the **JW view**: the same smile labelled by the
  trader's five numbers (ATM variance, ATM skew, put wing, call wing, minimum variance). **Lab 1** `smile.fit_svi`.
  **Replay**: the 51-day expiry (35 quotes): six random starts, each a curve morphing through its least-squares
  iterates onto the dots; RMSE per evaluation as a loss curve, the six as a band.
- Derivation:
  - $w(k) = a + b\big(\rho(k-m)+\sqrt{(k-m)^2+\sigma^2}\big)$ (Gatheral 2004).
  - Wings: $w'(\pm\infty) = b(\rho\pm1)$; vertex $\min w = a + b\sigma\sqrt{1-\rho^2}$ (differentiate; set $w'=0$).
  - Lee ⇒ $b(1+|\rho|)\le 2$ (ch3 applied to the asymptotes).
  - Origin: Heston's implied variance as $T\to\infty$ is exactly of SVI form (Gatheral–Jacquier 2011; stated with a card).
  - JW: $v = w(0)/T$, $\psi = \frac{b}{2\sqrt{w(0)}}\Big(\rho - \frac{m}{\sqrt{m^2+\sigma^2}}\Big)$, $p = \frac{b(1-\rho)}{\sqrt{w(0)}}$, $c = \frac{b(1+\rho)}{\sqrt{w(0)}}$, $\tilde v = \frac{a+b\sigma\sqrt{1-\rho^2}}{T}$ (reparametrize: these are what desks quote and move).
  - Fit: $\min\sum_i \nu_i\big(w(k_i)-w_i\big)^2$; for fixed $(m,\sigma)$ the model is linear in $(a, b\rho, b)$ (Zeliade's quasi-explicit reduction to two dimensions).
- Experiment: `svi_replay` (new): **(probe)** six starts from 12.6–58.7 vol pts RMSE all converge in 28–43 evaluations to
  0.254 vol pts and the same point (a = −0.041, b = 0.129, ρ = −0.096, m = 0.082, σ = 0.513). Then all 11 expiries' fits
  with their JW numbers in a table; g_min per expiry (exists: smallest 0.075). Card: Martini–Mingone (2022) give the
  full characterization of butterfly-free raw SVI.
- Pause-and-predict: "b(1 − ρ) = 0.14 at 51 days. What does it say about Bitcoin's downside?" (Left-tail moment finite up to q̃ ≈ 3.)
- Compute: `svi_replay` (0.5).

### 5 · SSVI: the whole surface in one formula (2.8) · item 3 · `s02d_ssvi` (new; content from `s02_smile.arbitrage`)
- Goal: a surface-wide parametrization with arbitrage-freedom proved; fitted in 3D; its limits.
- Beats: **Visual (3D)**: θ_T (ATM total variance) as a rising curve on the floor; for each θ the SSVI smile is hung
  above it, and the slices sweep together into the surface. **Lab 2** `volsurface.fit_ssvi` (unpack + residual: the
  monotone θ by cumulative exps, the clip η ≤ 2/(1+|ρ|)). **Replay (3D)**: the SSVI surface morphing through the
  optimizer's iterates onto the 254 white dots, the camera orbiting; vega-weighted RMSE curve right; 5 random starts as
  a band. Then the theorem card, and the per-expiry SVI vs SSVI RMSE as paired bars (the price of global consistency).
- Derivation:
  - $w(k,\theta_T) = \frac{\theta_T}{2}\big(1+\rho\varphi k + \sqrt{(\varphi k+\rho)^2+1-\rho^2}\big)$, $\varphi = \frac{\eta}{\theta^\gamma(1+\theta)^{1-\gamma}}$ (definition).
  - Calendar-free ⇔ $\partial_T\theta_T \ge 0$ and $0 \le \partial_\theta(\theta\varphi) \le \frac{1+\sqrt{1-\rho^2}}{\rho^2}\varphi$ (GJ Thm 4.1; README problem 3 checks the power law).
  - Butterfly-free if $\theta\varphi(1+|\rho|) < 4$ and $\theta\varphi^2(1+|\rho|)\le 4$ (GJ Thm 4.2, sufficient).
  - For the power law: $\theta\varphi^2(1+|\rho|) = \eta^2(1+|\rho|)\,\theta^{1-2\gamma}(1+\theta)^{2\gamma-2}$ ≤ 4 for all θ iff γ ≤ ½ given η(1+|ρ|) ≤ 2 (the bound at θ → 0).
- Experiment: `ssvi_replay` (new; wrap the residual to record every parameter vector): **finding to show honestly:** the
  fitted γ = 0.557 > ½, so GJ's sufficient condition holds only for θ > ≈1.5·10⁻⁷ (computed:
  $\theta^{1-2\gamma} \le 4/(\eta^2(1+|\rho|))$), i.e. at every quoted maturity, not provably at all; g_min on the fitted
  slices 0.26 (exists). Narration branches on γ ≤ ½. RMSE 0.74 vol pts (exists) vs per-expiry SVI (computed). Card:
  eSSVI (Hendriks–Martini 2019; Mingone 2022 global no-arbitrage) lets ρ vary with maturity.
- Pause-and-predict: "SSVI has 3 + (number of expiries) parameters; SVI per expiry has 5 each. Which fits better in sample? Which do you quote from?"
- Compute: `ssvi_replay` (1.0).

### 6 · Dupire's local volatility, derived (3.0) · item 4 · `s03_localvol` (deepened; `forward` moves to ch8)
- Goal: the unique diffusion that reprices every vanilla; derived twice; its shape; its tree.
- Beats: **Visual (3D)**: the implied surface (translucent) and the local-vol surface computed from it rise together on
  the same axes; the camera drops to look along k: local is steeper, about twice the slope (BBF), and blows up at the
  short end. Then **Derman–Kani's implied tree**: a binomial tree whose node spacing is warped level by level so that
  each strike is repriced (nodes crowd on the downside); the tree's local vols read off as node colours equal the
  surface's. **Lab 3** `volsurface.g_function` + `dupire_local_var` (the denominator is ch3's g).
- Derivation:
  - $dS = \sigma(S,t)S\,dW$ ⇒ $\partial_T p = \tfrac12\partial_{KK}(\sigma^2K^2p)$ (Fokker–Planck, Part 5).
  - $\partial_TC = \int(x-K)^+\partial_Tp\,dx = \tfrac12\int(x-K)^+\partial_{xx}(\sigma^2x^2p)\,dx = \tfrac12\sigma^2(K,T)K^2p(K,T)$ (integrate by parts twice; $\partial_{xx}(x-K)^+ = \delta_K$).
  - $\sigma^2_{\rm loc}(K,T) = \frac{\partial_TC}{\frac12K^2\partial_{KK}C}$ (since $p = \partial_{KK}C$).
  - In total variance: $\sigma^2_{\rm loc} = \frac{\partial_Tw}{g(k)}$ (change variables $K\to k$, $C\to w$; Gatheral eq. 1.10). So calendar ≥ 0 and g ≥ 0 are exactly "local variance is real".
  - BBF: $\sigma_{\rm imp}(k) \approx \Big(\frac1k\int_0^k\frac{du}{\sigma_{\rm loc}(u)}\Big)^{-1}$ as $T\to0$ ⇒ $\partial_k\sigma_{\rm imp}(0) = \tfrac12\partial_k\sigma_{\rm loc}(0)$ (harmonic mean along the straight line; differentiate).
- Experiment: `localvol` (exists) + `bbf` (new): **(probe)** local/implied ATM slope ratio 1.81 (7d), 1.70 (14d), 1.78 (30d),
  1.81 (60d), 1.82 (90d), 1.79 (180d): "about twice"; the narration says 1.7–1.8, and why not exactly 2 (BBF is a
  short-maturity statement; the first-order average ignores curvature). `dk_tree`: a 40-step implied tree on the SSVI
  surface (new House function), repricing error per strike printed.
- Pause-and-predict: "Implied skew is −0.375 per unit k at 30 days. Local skew?" (≈ −0.75.)
- Compute: `localvol` (exists, ~3), `bbf` (<0.1), `dk_tree` (0.2).

### 7 · Gyöngy: every model has a local-volatility twin (2.5) · item 4 · `s03a_gyongy` (new)
- Goal: why Dupire's function is the conditional expectation of variance; check it numerically; check LV reprices the Surface.
- Beats: **Live**: a Heston path fan (the House's QE scheme) runs to T = 0.25 on the floor of a 3D plot; at the end the
  cloud of (log S_T, v_T) points appears; a vertical slab slides along k, and at each k the slab's average √v_T is
  drawn as a gold dot. Over it, Dupire's curve from Heston's own option prices (COS) draws itself: the dots land on it.
  Then **live repricing**: 40,000 paths under the Surface's LV; for each expiry the Monte-Carlo smile appears over the
  SSVI smile (two curves converging as paths accumulate, ValueTracker over path count).
- Derivation:
  - Under $dS = \sigma_tS\,dW$ with random $\sigma_t$: $\partial_TC = \tfrac12K^2\,\mathbb E\big[\sigma_T^2\,\delta(S_T-K)\big]$ (Tanaka–Meyer for $(S_T-K)^+$, Part 5; take expectations).
  - $= \tfrac12K^2\,p(K,T)\,\mathbb E[\sigma_T^2\mid S_T=K]$ (condition on $S_T$).
  - ⇒ $\sigma^2_{\rm loc}(K,T) = \mathbb E^Q[\sigma_T^2\mid S_T=K]$ (compare with ch6; Gyöngy 1986: the one-dimensional marginals match).
  - The twin matches every $p(\cdot,T)$, not the joint law across dates: the warning of ch8.
- Experiment: `gyongy` (new): **(probe)** Heston v₀ = 0.25, κ = 3, θ = 0.30, ξ = 1.2, ρ = −0.3, T = 0.25, 100,000 QE paths:
  Dupire from COS prices vs √E[v_T | log S_T = k] agree within 1 vol pt across k ∈ [−0.5, 0.5] (e.g. 68.2/67.6 at −0.5,
  45.8/45.7 at 0.15, 51.9/51.2 at 0.5); the fan is 90 steps (computed, 5 s). `lv_reprice` (new): LV Monte Carlo prices of
  the Surface's quotes at 7, 30, 90 days, vega-weighted RMSE vs SSVI (expected ≲ 1 vol pt; the existing 4-substep scheme;
  narration branches if the short end misses).
- Pause-and-predict: "Two models with the same local vol: do they give the same price for a 30-day option starting in 60 days?" (No: ch8.)
- Compute: `gyongy` (1.5 incl. COS bumps), `lv_reprice` (6).

### 8 · Local volatility's future: the forward smile and the backbone (2.8) · item 5 · `s03b_forward` (new; from `s03_localvol.forward`)
- Goal: what LV predicts about tomorrow's smile, and why it is wrong.
- Beats: **Visual (live)**: spot slides right under a ValueTracker; under LV the implied smile slides **left** (the
  smile moves against the spot: Hagan et al. 2002's complaint), under sticky moneyness it rides along; the readout shows
  R ≈ 2 for LV. Then the **forward smile** fan: the 30-day smile starting today, in 30, 60, 90 days under LV, flattening
  step by step (each drawn as its MC paths accumulate), against today's 30-day smile (fixed). Card: forward-start
  options and cliquets depend on exactly this; Part 13 prices them across models.
- Derivation:
  - $\sigma_{\rm imp}(K;S) \approx \sigma_{\rm loc}\big(\tfrac{S+K}{2}\big)$ (BBF to first order: the average along the line).
  - $\Rightarrow \partial_S\sigma_{\rm ATM} = \partial_K\sigma_{\rm loc} \approx 2\,\partial_K\sigma_{\rm imp}$, i.e. $R_{LV} \approx 2$ (ch6's factor two).
  - For a fixed strike: $\partial_S\sigma_{\rm imp}(K;S) = \tfrac12\partial\sigma_{\rm loc} = \partial_K\sigma_{\rm imp}$: with a put skew, a rise in S lowers every implied vol: the smile shifts opposite to spot.
  - Forward-start payoff $(S_{T_2}/S_{T_1} - e^k)^+$; its smile is the law of $S_{T_2}/S_{T_1}$ (no closed form under LV: simulate).
  - LV's local vol flattens with time at fixed moneyness (the surface's $\partial_k\sigma_{\rm loc}$ decays like the implied skew's term structure), so forward skews fade.
- Experiment: `localvol` (exists: forward 30-day skew 60 days out 3.4 vs today 6.5 vol pts) extended as `fwd_curve` (new):
  forward skews for start dates 0, 15, 30, 60, 90 days (the same 40,000 paths, reused; computed). Expected monotone decay;
  narration reports the measured curve.
- Pause-and-predict: "Under local vol, spot drops 5% with a put skew. ATM vol?" (Rises by about 2 × skew × 5%.)
- Compute: `fwd_curve` (5; shares paths with `lv_reprice` if run together).

### 9 · Variance swaps: buying volatility itself (2.8) · item 6 · `s04_varswap` (deepened)
- Goal: replicate realized variance with a static strip and a dynamic hedge; what breaks it.
- Beats: **Visual**: the payoff −2 ln(S_T/F) drawn; then option payoffs (hockey sticks), each scaled by 2ΔK/K², drop in
  one by one from the forward outward, and their sum **converges onto the log curve** (residual shaded and shrinking).
  Then the existing strip bars with a **truncation slider**: strikes kept within ±x of the forward; √K_var climbs with x.
  Then the jump term: one jump J on a path; the log contract pays 2(e^J − 1 − J), realized variance J²; the gap J³/3 is
  drawn as a sliver.
- Derivation:
  - $d\ln S = \frac{dS}{S} - \tfrac12\sigma^2dt$ ⇒ $\int_0^T\sigma^2dt = 2\int_0^T\frac{dS}{S} - 2\ln\frac{S_T}{S_0}$ (Itô).
  - $f(S) = f(F) + f'(F)(S-F) + \int_0^Ff''(K)(K-S)^+dK + \int_F^\infty f''(K)(S-K)^+dK$ (Taylor with integral remainder; Carr–Madan).
  - $f = -\ln$: $f'' = 1/K^2$ ⇒ $K_{\rm var} = \frac2T\int_0^\infty\frac{\mathrm{OTM}(K)}{K^2}dK$ (take Q-expectations; the hedge has mean 0).
  - Model-free: $\mathbb E^Q\int(dS/S)^2 = $ the same integral for any continuous price (Britten-Jones–Neuberger 2000).
  - With a jump: $2(e^J-1-J) - J^2 = \tfrac{J^3}{3} + O(J^4)$ (expand), so down-jumps make the log contract under-pay realized variance.
- Experiment: `varswap` (exists: √K_var 48.8% vs ATM 43.7%; DVOL 45.9%) + `trunc` (new): **(probe)** √K_var with strikes
  within ±10%: 38.8%; ±20%: 45.0%; ±30%: 47.2%; ±50%: 48.5%; ±80%: 48.7%; ±120%: 48.8%. A fifth of the variance lives
  beyond ±20%.
- Pause-and-predict: "Why is √K_var above ATM vol?" (The strip owns the dear downside wing; convexity of the 1/K² weights.)
- Compute: `varswap` (exists), `trunc` (<0.1).

### 10 · Replicating on real Bitcoin; volatility swaps (2.8) · item 6 · `s04a_replicate` (new)
- Goal: run the replication on 100 real 30-day windows; see what monitoring and jumps cost; price a vol swap.
- Beats: **Live (HedgeLedger)**: one week's strip is bought at its surface price (Deribit-like strikes, static), then the
  hourly BTC path from Binance runs for 30 days while the delta hedge (2/(T·S) per unit) rebalances daily; the ledger
  splits P&L into strip payoff, hedge gains, and realized variance; at the end the two totals sit side by side. Then the
  100 windows as a scatter (replicated vs realized variance) on a 45° line. **Lab 4** `volsurface.var_swap_strike` and
  the new `strip_replication`. Then the **vol swap**: √ is concave, so E√V < √EV; the 100 realized vols drawn as dots on
  the √ curve, the chord and the gap labelled.
- Derivation:
  - Daily-monitored contract: $RV = \frac{365}{n}\sum_i\ln^2\frac{S_{i+1}}{S_i}$; replication error $= \frac{365}{n}\sum_i\big[2(r_i - \ln(1+r_i)) - \ln^2(1+r_i)\big] \approx \frac{365}{n}\sum_i \tfrac{2}{3}r_i^3$ (Taylor; the cubic term from ch9).
  - $\sqrt V \approx \sqrt K + \frac{V-K}{2\sqrt K} - \frac{(V-K)^2}{8K^{3/2}}$ ⇒ $K_{\rm vol} \approx \sqrt{K_{\rm var}} - \frac{\operatorname{Var}(V)}{8K_{\rm var}^{3/2}}$ (second-order Taylor; DDKZ 1999; Carr–Lee 2009).
- Experiment: `replication` (new; Binance BTCUSDT 1h, the 100 weekly fits): **(probe)** with an hourly hedge the log
  contract matches hourly realized variance almost exactly (corr 0.99999; mean error −0.00007 in variance; worst week
  starting 2025-02-19); a daily-hedged replication against hourly-measured variance differs by sd 0.057 in variance
  (on a mean of 0.239): the monitoring frequency in the contract is not a detail. The full computation adds the finite
  strike grid and truncation at inception (computed; narration reports both error components). Vol-swap convexity:
  E√RV = 47.6% vs √E[RV] = 48.9%, DDKZ approximation 1.2 vol pts (probe).
- Pause-and-predict: "A vol swap and a variance swap on the same month: which strike is higher, as a volatility?" (The variance swap's.)
- Compute: `replication` (0.5).

### 11 · The VIX, and our own (2.8) · item 7 · `s04b_vix` (new)
- Goal: the Cboe recipe line by line; our index against DVOL for two years; the VIX's history.
- Beats: **Lab 5** `volsurface.vix` (K₀, Q(K), ΔK/K², the forward correction) run on the Surface's two straddling
  expiries; each strike's contribution builds as a bar chart in the order the code loops. Then the 30-day interpolation
  as two dots on the variance-time line with the chord read at 30 days. Then **two lines over 100 weeks**: our √K_var
  (from each Wednesday's surface) and DVOL at the same hour, drawn together, the gap shaded. Then the VIX from 1990 to
  2025 (FRED VIXCLS) drawn with crisis peaks lit (2008, 16 Mar 2020 at 82.69, 5 Feb 2018 +116%); the term-structure line
  VIX/VIX3M since 2007 under it.
- Derivation:
  - $\sigma^2 = \frac2T\sum_i\frac{\Delta K_i}{K_i^2}e^{rT}Q(K_i) - \frac1T\Big(\frac{F}{K_0}-1\Big)^2$ (Cboe; the discretized strip).
  - The correction: centring the strip at $K_0\le F$ instead of $F$ adds $\frac2T\int_{K_0}^F\frac{(K-S)^+-(S-K)^+}{K^2}dK$ ≈ $\frac1T(F/K_0-1)^2$ (parity on $[K_0,F]$; Taylor).
  - $\sigma^2_{30} = \Big[T_1\sigma_1^2\frac{N_2-N_{30}}{N_2-N_1} + T_2\sigma_2^2\frac{N_{30}-N_1}{N_2-N_1}\Big]\frac{N_{365}}{N_{30}}$ (linear in total variance).
- Experiment: `vixcomp` (new): **(probe)** over 100 weeks our index averaged 54.0% vs DVOL 52.3%, corr 0.994, gap
  +1.6 ± 1.2 vol pts (narration: same recipe, different wings and quotes). VIX history (VIXCLS 1990–2025, cached):
  largest one-day rises 5 Feb 2018 (+116%), 18 Dec 2024 (+74%), 5 Aug 2024 (+65%); peak close 82.69 on 16 Mar 2020;
  VIX below VIX3M on **90% of days** since Dec 2007 (FRED VXVCLS, probe).
- Pause-and-predict: "Remove every option beyond ±20% from the strip. Does the index go up or down?" (Down: ch9's truncation.)
- Compute: `vixcomp` (<0.2). Data: FRED `VXVCLS` (new manifest entry), `VIXCLS` 1990–2025 window (new entry).

### 12 · The variance risk premium, measured (2.8) · item 8 · `s05_vrp` (deepened)
- Goal: why implied exceeds realized; measure it on BTC and on the S&P 500; what selling it feels like; does it predict returns?
- Beats: **Live**: the 100 weekly pairs drawn week by week (implied above, realized after), a running mean and a running
  NW t-stat as readouts. Then the **insurance ledger**: a short variance swap's weekly P&L as bars, mostly small green, a
  few deep red; cumulative line with its drawdown shaded; the worst window (starting 31 Jul 2024, which contains 5 Aug)
  flagged. Then the S&P 500 1990–2025: VIX² vs the next 21 days' realized, drawn as a 35-year river.
- Derivation:
  - $\mathbb E^Q[X] = \frac{\mathbb E^P[mX]}{\mathbb E^P[m]}$ (Part 9) ⇒ $\mathbb E^Q[RV] - \mathbb E^P[RV] = \frac{\operatorname{cov}^P(m,RV)}{\mathbb E^P[m]}$ (expand).
  - Variance is high when marginal utility m is high ⇒ cov > 0 ⇒ VRP > 0 (insurance).
  - NW: $\hat V = \hat\gamma_0 + 2\sum_{L=1}^4(1-\frac L5)\hat\gamma_L$ (weekly 30-day windows overlap ~4).
  - BTZ test: $r_{t\to t+30} = \alpha + \beta\,(K_{{\rm var},t} - RV_{t-30\to t}) + \varepsilon$ (ex-ante VRP; NW t).
- Experiment: `history` (exists: 54% vs 47.6%, 76% of weeks, t = 3.6); `vrp_pnl` (new): **(probe)** short-var weekly P&L skewness
  −0.55, worst −0.208 in variance (window from 2024-07-31), best +0.271; BTZ slope −0.09, NW t −0.5, R² 0.004: **no
  predictability in BTC 2024–25** (branch: say so; BTZ found it for the S&P at quarterly horizons). `spx_vrp` (new, Yahoo
  ^GSPC + VIXCLS): **(probe)** 1990–2025, VIX averaged 19.5 vs 15.4 realized over the next 21 trading days, positive
  86% of days, worst 26 Feb 2020. Card: Dew-Becker et al. (2017): the premium is concentrated at the short end.
- Pause-and-predict: "A strategy wins 76% of weeks. Is it a good one?" (Look at the 24%: skew −0.55.)
- Compute: `vrp_pnl` (<0.1), `spx_vrp` (<0.1). Trial counter: the BTZ regression is a predictive test → register 1 trial (lead's decision; see §6).

### 13 · What option prices say about the future: SVIX and risk-neutral moments (2.6) · item 8 · `s05a_moments` (new; from `s05_vrp.svix`)
- Goal: Martin's bound derived; risk-neutral variance, skewness, kurtosis from strips; their history in BTC.
- Beats: **Visual**: three option strips with different weightings (1/K² for log variance, constant for SVIX, the BKM
  cubic/quartic weights) drawn as three bar sets over the same smile, each integral filling a gauge. Then the weekly
  series of Q-variance, Q-skewness and Q-kurtosis over 2024–25, Q-skewness crossing zero (the call-skew weeks of ch1).
- Derivation:
  - $\operatorname{var}^Q(R) = \frac{2}{F^2}\int_0^\infty \mathrm{OTM}(K)\,dK$ (Carr–Madan with $f(S) = S^2$, $f'' = 2$).
  - $\mathbb E[R]-R_f = \frac{\operatorname{var}^Q(R)}{R_f} - \operatorname{cov}(mR,R)$ (from $\mathbb E^Q X = R_f\mathbb E[mX]$, $\mathbb E[mR]=1$).
  - If $\operatorname{cov}(mR,R)\le0$: $\mathbb E[R]-R_f \ge R_f\,\mathrm{SVIX}^2$ (Martin's negative-correlation condition).
  - BKM: $V = \mathbb E^Q[r^2]$, $W = \mathbb E^Q[r^3]$, $X = \mathbb E^Q[r^4]$ with $r=\ln S_T/F$, each a strip with weights $\frac{2(1-\ln(K/F))}{K^2}$, $\frac{6\ln(K/F) - 3\ln^2(K/F)}{K^2}$, … (Carr–Madan with $f = r^n$); skew $= (W-3\mu V+2\mu^3)/(V-\mu^2)^{3/2}$.
- Experiment: `history` (SVIX bound 31%/yr, exists); `rn_moments` (new; refits from the cached weekly trades): Q-skewness
  and Q-kurtosis series; share of weeks with positive Q-skew (expected ≈ ch1's 64%, computed); correlation with the
  week's realized return. Card: Martin (2017) S&P bound ≈ 5%/yr (from the paper) and Martin–Wagner (2019) for stocks.
- Pause-and-predict: "Bitcoin's SVIX bound says ≥ 31% a year. Why not buy?" (The condition may fail; it is a bound under an assumption, not a forecast.)
- Compute: `rn_moments` (2; 100 SSVI refits).

### 14 · VIX futures, the roll, and short-volatility notes (2.8) · item 10 · `s06a_etp` (new)
- Goal: what a VIX future is (not a var swap); the roll yield; how an inverse note is built and why it must buy into spikes.
- Beats: **Visual (3D)**: the VIX futures curve through time, June 2017–March 2018, as a ribbon surface (date × days to
  expiry × price), upward-sloping almost every day, then on 5 Feb 2018 folding into backwardation. **Live**: rebuild the
  short-term futures index (front/second roll, as S&P's methodology) day by day from Cboe settlements, and beside it the
  −1× daily note; the note's line climbs through 2017 then falls off the chart. **Lab 6** new `vx_index` + `inverse_note`.
  Then the rebalancing flow: for each day the futures the issuer must buy, as bars, tallest on 5 Feb.
- Derivation:
  - $F^{VX}_t(T) = \mathbb E^Q_t[\mathrm{VIX}_T] \le \sqrt{\mathbb E^Q_t[\mathrm{VIX}_T^2]}$ (a future on volatility, Jensen: below the forward variance swap rate).
  - Index weights $w_1 = \frac{d_r}{d_t}$, $w_2 = 1-w_1$ (days remaining in the roll over days in the roll period); daily return of the index $= \frac{w_1F_1' + w_2F_2'}{w_1F_1+w_2F_2}-1$.
  - In contango, rolling down the curve earns $\approx \frac{F_2-F_1}{F_1}$ per month for the short.
  - A note with daily leverage $L$: $N_{t+1} = N_t(1+Lr)$; to restore exposure $LN_{t+1}$ the hedger trades $(L^2-L)\,r\,N_t$ (both $L=-1$ and $L=2$ give $2rN_t$: **buy after a rise**, Cheng–Madhavan 2009).
- Experiment: `vx_etp` (new; Cboe VX settlement CSVs, 10 expiries): **(probe)** front-month settle 15.625 → 33.225 on 5 Feb
  (+113%), second month 14.975 → 27.975 (+87%); rebuilt index **+96.1%** that day, so the −1× note fell **96.1%**, which
  matches XIV's indicative value falling from 108.37 to about 4.22 (as reported; verify the second figure); the note had
  gained about 64% from June to December 2017; the curve was in contango (front < second) on 86% of days (median slope
  +7.9%). TVIX 2012 (Credit Suisse halted creations 21 Feb 2012; premium to indicative value reached about 89%,
  as reported by Bloomberg) as the second card. SVXY's leverage moved from −1× to −0.5× at the close on 27 Feb 2018
  (ProShares fact sheet).
- Pause-and-predict: "An inverse note is worth $1bn, and its index rises 10%. How many dollars of futures must the hedge buy?" ($200m.)
- Compute: `vx_etp` (<0.1). Data: new loader `data.cboe_vx(expiry)` (CSV per expiry, checksummed).

### 15 · Volmageddon, 5 February 2018 (2.6) · crisis · `s06_volmageddon` (deepened; `dealers` moves to ch16)
- Goal: the day, the mechanism measured, the funds, and the allegations.
- Beats: keep the crisis card (17.31 → 37.32); then the **term-structure snap**: VIX/VIX3M ratio 1.016 on 2 Feb → 1.327
  on 5 Feb (FRED, probe); the 3D futures ribbon from ch14 at that date; the 4:00–4:15 pm rebalancing window explained with
  ch14's flow bars. Firm files (each a `firm_card`, public record only):
  - Credit Suisse, XIV: the press release of 6 Feb 2018 announced an acceleration event (intraday indicative value ≤ 20%
    of the prior day's close). Investors later *alleged* manipulation; the Second Circuit revived the claims
    *(verify citation: Set Capital LLC v. Credit Suisse, 2d Cir. 2021)*; the bank denies wrongdoing.
  - LJM: the SEC *alleged* (complaint of 27 May 2021) that LJM and two portfolio managers misled investors about risk;
    losses exceeded $1bn over two trading days, >80% of the funds' value; the defendants contested the charges
    *(outcome: verify)*.
  - Griffin–Shams (2018, *RFS*): volume spikes in SPX options at VIX settlement, consistent with manipulation; Cboe
    disputed the paper. Labelled as research and allegation.
- Derivation: one line: the 5 Feb loss of a −1× note is −(index return), unbounded relative to its 2017 gains (ch14).
- Experiment: `volmageddon` (exists) + `vx_etp` (shared) + VXVCLS.
- Pause-and-predict: "Why did the note's issuer have to buy at the close, not earlier?" (The promise is on the daily close-to-close return.)
- Compute: shared.

### 16 · Dealer gamma, intraday momentum, and same-day options (3.0) · item 9 · `s06b_gamma` (new; from `s06_volmageddon.dealers`)
- Goal: who is short gamma, what their hedging does to prices, and the 0DTE debate.
- Beats: **Live simulation**: two price paths driven by the same shocks; in one the dealer is long gamma (hedges sell
  rallies), in the other short (hedges buy them); the hedge trades appear as arrows on each path and the short-gamma
  path visibly swings wider; a running realized-vol readout for each. Then an end-of-day panel: the last 30 minutes'
  return against the rest of the day's, for the short-gamma simulation (positive slope: intraday momentum) and the
  long-gamma one (flat/negative). Then the GEX card and the 0DTE growth line (Cboe-reported shares).
- Derivation:
  - Hedge position $h = -\Gamma_d\,S\,\Delta S$ per unit move; with linear impact $\Delta S = \Delta S_0 + \lambda h$:
    $\Delta S = \frac{\Delta S_0}{1+\lambda\Gamma_dS}$ (solve the fixed point).
  - $\Gamma_d > 0$ (dealers long) damps; $\Gamma_d < 0$ amplifies, diverging as $\lambda|\Gamma_d|S\to1$.
  - $\mathrm{GEX} = \sum_i\Gamma_i\,S^2\,\mathrm{OI}_i\,s_i$, $s_i = \pm1$ the dealers' assumed side (the assumption is the weak point).
- Experiment: `gamma_toy` (new, simulated; label `simulated`): realized-vol ratio short/long against λΓ; intraday-momentum
  slope by regime (computed, 5 seeds as a band). Public record: Baltussen et al. (2021): over 60 futures, 1974–2020,
  the last 30 minutes are predicted by the rest of the day, and SPX option and leveraged-ETF hedging demand drives
  the strength (verified from the abstract). 0DTE: >43% of SPX option volume in 2023 (Bandi, as quoted by JHU Carey);
  Cboe-reported record monthly shares of 62% (August 2025) and 66.2% (July 2026; secondary source, *verify on
  Cboe*); Cboe launched VIX1D on 24 April 2023 (verified). Papers: Andersen–Fusari–Todorov (2017) weeklies;
  Bandi–Fusari–Renò (2023) 0DTE pricing (jumps for OTM, continuous for ATM; data 2014–May 2023); Dim–Eraker–Vilkov (2024)
  *(findings to be read before stating)*; Beckmeyer et al. (2023) *(verify)*. The narration states that the evidence
  on whether 0DTE moves the index is mixed, not a verdict.
- Pause-and-predict: "Dealers are short a lot of gamma at the 6,000 strike, spot 6,010, one hour to expiry. What does spot do?" (Their hedging pushes it away from the strike; long gamma would pin it.)
- Compute: `gamma_toy` (1).

### 17 · Learning surfaces (3.0) · item 11 · `s07_learning` (deepened)
- Goal: train two learners on screen: a VAE that compresses surfaces, and a network that smooths one surface without arbitrage.
- Beats: **Replay 1 (VAE)**: `TrainingReplay` left panel = a 3D reconstructed surface of one chosen week morphing from
  noise to its true shape; right = loss with 5 seeds as a band; then the latent scatter (existing) builds week by week
  coloured by ATM vol, and a **3D latent walk**: moving z₁ lifts the whole surface, z₂ tilts it (existing walks, now as
  surfaces). **Replay 2 (neural surface)**: an MLP w(k,T) trained on 80% of the Surface's quotes with the ch3 penalties
  (relu(−g) and relu(−∂_T w) on a collocation grid); left = the surface in 3D, collocation points flashing red where g < 0
  and going dark as the penalty bites; right = train/held-out RMSE and the penalty; 3 seeds band; SSVI on the same split
  as a dashed baseline. Then the same network **without** the penalty: violations counted.
- Derivation: ELBO $= \mathbb E_q[\ln p(x|z)] - \mathrm{KL}(q(z|x)\|N(0,I))$ (one line, AI series reference);
  penalised loss $\sum_i(\hat\sigma_i-\sigma_i)^2 + \lambda\big[\overline{(-g)^+} + \overline{(-\partial_Tw)^+}\big]$ (Ackerer et al. 2020; derivatives by autodiff).
- Experiment: `vae` (exists; add 5 seeds and checkpoints every 100 steps: recon 1.9 vol pts, corr 0.96); `neural_surface` (new):
  **(probe)** held-out RMSE 1.32 / 0.99 / 0.81 vol pts (3 seeds) vs SSVI on the same splits 2.01 / 2.22 / 2.26 (unweighted);
  zero butterfly or calendar violations on a 201 × 60 grid; 75 s per seed under load. The unpenalised run and the
  vega-weighted comparison are to be computed; narration branches on whether the network beats SSVI out of sample
  (probe says yes, by ~1 vol pt) and states the cost (no closed form, no extrapolation guarantee).
- Pause-and-predict: "The network fits better. Why might a desk still quote SSVI?" (Extrapolation, stability day to day, provable no-arbitrage, speed.)
- Compute: `vae` (2; 5 seeds), `neural_surface` (10; 3 seeds × 2 variants).

### 18 · Industry: who builds surfaces, and who sells them (2.8) · `s07a_industry` (new)
- Goal: exchanges, dealers, asset managers and regulators, from the public record.
- Beats (cards and live objects, sources on screen):
  1. **Exchanges compute surfaces as indices.** Cboe: VIX introduced 1993 on S&P 100 options (Whaley), moved to S&P 500
     strips with Goldman Sachs in 2003, futures in March 2004, options in February 2006, VIX1D in April 2023. Deribit:
     DVOL launched 31 March 2021 (30-day, two straddling expiries), DVOL futures 27 March 2023; Deribit acquired by Coinbase
     (closed 14 August 2025, about $2.9bn, as reported). IBIT options listed on Nasdaq 19 November 2024 ($1.9bn
     notional on day one, as reported by Bloomberg's analysts).
  2. **Dealers' quants wrote the field.** Derman–Kani (Goldman, 1994), DDKZ (Goldman QS, 1999), Gatheral's SVI (a
     Merrill Lynch presentation, 2004 *(verify affiliation)*), Andreasen–Huge's "Volatility interpolation" (Danske, 2011
     *(verify)*). The House's builder (old `s08_house` table) shown against this list: what a bank's builder does that ours
     does not (dividends, rates, intraday marking).
  3. **Firm file: Allianz Global Investors U.S., "Structured Alpha".** SEC (17 May 2022): about 114 institutional investors
     put about $11bn into an options strategy whose downside risks the SEC found were concealed; losses exceeded $5bn in
     March 2020; AGI US pleaded guilty to securities fraud, paid a $675m civil penalty (plus disgorgement deemed
     satisfied) and is barred from advising US registered funds for 10 years; total payments over $6bn as reported.
     Lesson on screen: a short-volatility book whose hedges were removed (as found by the SEC) is ch12's left tail.
  4. **Regulators and short-vol products.** The XIV acceleration (ch15), SVXY to −0.5× (ch14), LJM (ch15). 
- Experiment: none new (reuses ch12's P&L skew); `industry_facts` is a static table.
- Pause-and-predict: "Why can an exchange compute a VIX for BTC but not a 'true' variance swap rate?" (Finite strikes; ch9.)
- Compute: none.

### 19 · Frontier, 2023–2026 (2.6) · `s07b_frontier` (new)
- Goal: what is new in surfaces, with one small replication on screen.
- Beats (cards, each with a 1-line finding and one visual):
  - Wiedemann–Jacquier–Gonon (ICLR 2025): a graph neural operator maps raw quotes to a smoothed surface in one pass;
    trained on ten years of intraday SPX (60m+ points), ~100k parameters, adheres to no-arbitrage constraints. Visual:
    our Surface's 254 quotes → our ch17 net (per-surface) vs "one net for all days" diagram.
  - Vuletić–Cont, VolGAN (*Appl. Math. Finance* 2024): a GAN with scenario re-weighting that generates arbitrage-free
    SPX surfaces and time-varying correlations, used for hedging. Visual: ch17's VAE scenarios side by side.
  - Kelly–Kuznetsov–Malamud–Xu (2023): implied-vol surfaces as images; an ensemble of ML models predicts the
    cross-section of stock returns out of sample (from the abstract). Link Part 27.
  - Martini–Mingone (2022): exact butterfly-free region of SVI; eSSVI's global no-arbitrage parametrization. Visual:
    ch4's parameter space with the forbidden region shaded.
  - Bandi–Fusari–Renò (2023): 0DTE surfaces (ch16).
  - Signature SPX/VIX joint calibration (Cuchiero et al. 2025) and PDV (Guyon–Lekeufack 2023) → Part 14.
  - **Small replication on screen**: "one net for all weeks": the ch17 network conditioned on the VAE latent (z₁, z₂) as
    extra inputs, trained on all 100 weeks' grids; held-out weeks RMSE vs per-week SSVI (computed; narration branches).
- Pause-and-predict: "A generator of surfaces passes the arbitrage checker every day. Is it a good risk model?" (Not necessarily: dynamics and tails matter, Part 40.)
- Compute: `operator_net` (8; 3 seeds).

### O · The House, recap, desk questions, problems (2.4) · `s09_outro` (+ old `s08_house` rule)
- House card: the surface builder lit; Rule 12 stated; trial counter (73, or 74 if the BTZ test is registered).
- Recap in 12 lines (one per item + industry + frontier), payoff card (Parts 13, 14, 15, 17, 27, 40, 41), reference card.
- Desk questions: keep "Why is the VIX above realized on average?" and "Replicate a variance swap"; replace the third
  with **"Spot falls 5%; under local vol, sticky strike and sticky delta, where does ATM vol go?"** (ch2/ch8). Keep the
  dealer-gamma question as the pause-and-predict of ch16.
- Problems (≈90 s): keep the 5; add (6) "derive g(k) from Black's formula in total variance" and (7) "show
  K_vol ≈ √K_var − Var(V)/(8K_var^{3/2})". README carries solutions in English and Chinese.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.8 | 10 Replication | 2.8 |
| 1 Smile | 2.8 | 11 VIX | 2.8 |
| 2 Dynamics | 3.0 | 12 VRP | 2.8 |
| 3 Arbitrage | 3.0 | 13 SVIX/moments | 2.6 |
| 4 SVI | 2.8 | 14 VIX futures/ETPs | 2.8 |
| 5 SSVI | 2.8 | 15 Volmageddon | 2.6 |
| 6 Dupire | 3.0 | 16 Gamma/0DTE | 3.0 |
| 7 Gyöngy | 2.5 | 17 Learning | 3.0 |
| 8 Forward smile | 2.8 | 18 Industry | 2.8 |
| 9 Var swaps | 2.8 | 19 Frontier | 2.6 |
| | | Outro | 2.4 |
| | | **Total** | **≈ 58.0** |

(≈ 8,050 words. The `--floor 50` gate leaves 8 minutes of slack.)

---

## 3b. Hands-on summary

**Labs (`lab_card` + `lab_run`, ≤ 12 lines each, outputs from the cache):**
1. ch4 `explainer/quant/house/smile.py` lines 32–35 and 37–44 (`fit_svi`: residual, the six starts, bounds with Lee's
   b(1+|ρ|) ≤ 2) → prints the best start's (a, b, ρ, m, σ) and RMSE for the 51-day expiry.
2. ch5 `volsurface.py` lines 45–54 and 57 (`fit_ssvi`: tanh/exp/sigmoid unpacking, cumulative θ, η clip, residual,
   `least_squares`) → prints ρ, η, γ, the θ's and the RMSE.
3. ch6 `volsurface.py` lines 108–117 (`g_function`, `dupire_local_var`) → prints g_min and σ_loc at k = 0 for 7/30/90 days.
4. ch10 `volsurface.py` lines 130–134 (`var_swap_strike`) + new `strip_replication` (≈8 lines) → prints K_var, the
   realized variance and the replication error for the replayed week.
5. ch11 `volsurface.py` lines 141–152 (`vix`: K₀, Q, ΔK, the sum and the correction) → prints both expiries' σ, the 30-day
   interpolation, and DVOL.
6. ch14 new `vx_index` + `inverse_note` (≈11 lines) → prints the 5 Feb index return and the note's value path.

**Replays (seeds as bands, baselines at equal budget):** ch4 SVI (6 starts; nothing to compare: all converge, which is
the point); ch5 SSVI in 3D (5 starts; per-expiry SVI as baseline); ch17 VAE (5 seeds; PCA reconstruction with 2
components as the equal-size baseline, computed from ch2's eigenvectors); ch17 neural surface (3 seeds; SSVI on the same
split); ch19 operator-style net (3 seeds; per-week SSVI). Implementation: record iterates in a wrapped residual (SVI/SSVI)
or torch checkpoints every 100 steps; `TrainingReplay(steps, loss[seeds], frame, checkpoints)`; 3D frames via
`price_surface` inside a `ThreeDScene` with labels `add_fixed_in_frame_mobjects`.

**Live simulations:** the flat-to-skew morph (hook); the Gram–Charlier smile slider (ch1); the three stickiness regimes
under a spot slider (ch2); g crossing zero (ch3); SVI sliders (ch4); Heston fan → conditional-variance dots (ch7); LV MC
smiles converging (ch7); smile sliding against spot and forward smiles fading (ch8); option payoffs summing to the log
contract (ch9); the hedge ledger on a real BTC month (ch10); strike contributions accumulating (ch11); weekly VRP pairs
and the insurance ledger (ch12); the VX index and the inverse note day by day (ch14); long/short-gamma paths (ch16).

**3D (ThreeDScene):** hook (Surface + morph), ch2 (PCA eigen-surfaces), ch5 (SSVI replay), ch6 (implied vs local
surfaces), ch7 (Heston cloud), ch14 (VX futures ribbon), ch17 (VAE surfaces, neural surface).

**Compute budget (seeded; ≈ 52 CPU-minutes measured or estimated on one core under a load of ~20; ≈ 45 min idle):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| surface* | 1 | gyongy | 1.5 | vrp_pnl, spx_vrp | 0.2 |
| localvol* | 3 | lv_reprice | 6 | rn_moments | 2 |
| varswap*, trunc | 0.2 | fwd_curve | 5 | vx_etp | 0.1 |
| history* (fetch ~10 once) | 3 | replication | 0.5 | gamma_toy | 1 |
| volmageddon* | <0.1 | vixcomp | 0.2 | vae* (5 seeds) | 2 |
| termskew, dynamics | 0.1 | arbitrage | 0.1 | neural_surface | 10 |
| svi_replay | 0.5 | ssvi_replay | 1 | operator_net | 8 |
| bbf, dk_tree | 0.3 | envelope* | <0.1 | | |

(* exists.) The budget leaves ~65 CPU-minutes unused. **Optional (lead's decision):** extend the weekly history back to
April 2021 (`history_ext`, ~140 more Wednesdays of Deribit trades: ~15 min of fetching, ~5 CPU-min of fits), which adds
the 2022 bear market (LUNA, FTX) to ch1, ch2, ch12, ch13 and gives the VAE/operator nets 2.4× the data. It grows the data
cache by roughly 25 MB and the manifest by ~140 trade-day entries. `neural_surface`, `operator_net` and `vae` use
`CACHE.partial` per seed and `torch.set_num_threads(1)`. One command rebuilds: `python -m videos.quant.quant12.compute`.

---

## 4. Industry and frontier: sources checked this session (2 Nov 2026)

| Fact | Source |
|---|---|
| Credit Suisse XIV acceleration event announced 6 Feb 2018; trigger: intraday indicative value ≤ 20% of prior close; prior reference value $108.3681 (2 Feb) | https://credit-suisse.com/articles/media-releases/2018/02/en/credit-suisse-announces-event-acceleration-xiv-etn.html (release; text seen via excerpts) |
| XIV litigation: claims revived by the Second Circuit (allegations; bank denies) | https://www.cohenmilstein.com/credit-suisse-faces-revived-claims-over-inverse-vix-crash-law360/ (plaintiffs' counsel, secondary) — *verify the opinion itself* |
| XIV final indicative ≈ $4.22 (5 Feb); redemption ≈ $5.99 | secondary reports only — *(unverified)*; use our computed −96.1% and say "as reported" for the prices |
| SVXY changed from −1× to −0.5× effective close 27 Feb 2018 (UVXY 2× → 1.5×) | https://www.proshares.com/our-etfs/strategic/svxy (fund page / fact sheet) |
| SEC v. LJM (27 May 2021): alleged misleading statements on risk; >$1bn losses over two trading days, >80% of funds' value; CRO settled; defendants contested | https://www.sec.gov/news/press-release/2021-89 ; https://www.sec.gov/enforcement-litigation/litigation-releases/lr-25101 — outcome *(verify)* |
| SEC, Allianz Global Investors U.S. Structured Alpha (17 May 2022): ~114 investors, ~$11bn, >$5bn lost March 2020, $675m penalty, $315.2m disgorgement + $34m interest deemed satisfied, 10-year bar; guilty plea; total >$6bn (reported) | https://www.sec.gov/news/press-release/2022-84 (fetched) |
| Griffin–Shams (2018) "Manipulation in the VIX?" *RFS*, doi 10.1093/rfs/hhx085; Cboe disputed | https://doi.org/10.1093/rfs/hhx085 ; press coverage (hedgefundalpha.com) |
| Baltussen, Da, Lammers, Martens (2021) *JFE* 142(1):377–403: >60 futures 1974–2020; last 30 min predicted; SPX options and leveraged ETFs drive it | https://www3.nd.edu/~zda/intramom.pdf ; https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/ |
| Cboe VIX1D launched 24 Apr 2023 (SPXW quotes; current day) | https://ir.cboe.com/news/news-details/2023/Cboe-Global-Markets-Launches-1-Day-Volatility-Index-Designed-to-Measure-Volatility-Over-Current-Trading-Day-04-24-2023/default.aspx |
| SPX 0DTE share: record 62% (August, Cboe insights post); 66.2% July 2026 (secondary) *(verify year on Cboe pages)*; ~43–45% in 2023 (Bandi; seminar abstract) | https://www.cboe.com/insights/posts/spx-0-dte-options-jump-to-record-62-share-in-august ; https://carey.jhu.edu/articles/risk-reward-insights-0dte-option-trading |
| Bandi, Fusari, Renò (2023) "0DTE option pricing", SSRN 4503344 | https://papers.ssrn.com/abstract=4503344 |
| Dim, Eraker, Vilkov (2024), SSRN 4692190 (title only verified) | https://papers.ssrn.com/abstract=4692190 |
| VIX: 1993 (S&P 100, Whaley), 2003 SPX methodology with Goldman, futures March 2004 (24 vs 26 March differs across sources), options Feb 2006 | https://www.cboe.com/tradable-products/vix/vix-historical-data/ ; https://www.indexologyblog.com/2022/05/31/29-years-of-vix/ ; Cboe VIX white paper https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf |
| Cboe VX futures daily settlements are public CSVs (used in ch14; fetched to scratchpad) | https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/VX_2018-02-14.csv |
| FRED VIX3M (VXVCLS) from Dec 2007 (fetched to scratchpad) | https://fred.stlouisfed.org/series/VXVCLS |
| Deribit DVOL launched 31 Mar 2021 (two expiries around 30 days); DVOL futures 27 Mar 2023 | https://coindesk.com/markets/2021/03/31/crypto-options-giant-deribit-launches-bitcoin-volatility-index ; https://insights.deribit.com/?p=1813 |
| Coinbase closed Deribit acquisition 14 Aug 2025, ~$2.9bn (reported) | https://www.theblock.co/post/366957/coinbase-completes-2-9-billion-cash-and-stock-acquisition-of-deribit |
| IBIT options began on Nasdaq 19 Nov 2024; ~354k contracts, $1.9bn notional day one (as reported) | https://www.nasdaq.com/newsroom/nasdaq-listed-ibit-options-end-first-day-top-1-all-options-products-traded |
| TVIX: creations halted 21 Feb 2012; premium peaked ~89% in March (as reported) | https://www.bloomberg.com/news/articles/2012-03-24/credit-suisse-tames-rogue-vix-note-premium-with-share-issuance ; https://www.etftrends.com/2012/03/tvix-falls-more-after-credit-suisse-restarts-issuance/amp/ |
| VolGAN (Vuletić–Cont), *Appl. Math. Finance* 31(4):203–238 | https://papers.ssrn.com/abstract=4617536 ; https://ideas.repec.org/a/taf/apmtfi/v31y2024i4p203-238.html |
| Operator deep smoothing (Wiedemann–Jacquier–Gonon), ICLR 2025 | https://arxiv.org/abs/2406.11520 ; https://iclr.cc/virtual/2025/poster/32104 |
| Kelly–Kuznetsov–Malamud–Xu (2023), SSRN 4531181 | https://papers.ssrn.com/abstract=4531181 |
| Martini–Mingone, "No arbitrage SVI" (SIFIN 2022); eSSVI global (*QF* 22(12) 2022) | https://arxiv.org/abs/2005.03340 ; https://arxiv.org/abs/2204.00312 |
| Ackerer–Tagasovska–Vatter (2020) NeurIPS | https://arxiv.org/abs/1906.05065 |
| Gatheral TOC (11 chapters incl. Heston–Nandi, asymptotics, dynamics, volatility derivatives) | https://gov.wiley.com/WileyCDA/WileyTitle/productCd-0471792519,descCd-tableOfContents.html ; https://www.eyrolles.com/Entreprise/Livre/the-volatility-surface-9780471792512 |
| Bergomi chapter titles (local volatility, forward-start options, variance swaps incl. large returns and strike discreteness, smile of SV models) | https://www.routledge.com/Stochastic-Volatility-Modeling/Bergomi/p/book/9781482244069 |

**Unverified (keep the marks or drop):** XIV's $4.22/$5.99 figures; the Set Capital v. Credit Suisse citation; LJM's outcome;
the 66.2% July 2026 0DTE share (secondary); Dim–Eraker–Vilkov and Beckmeyer et al. findings; Gatheral's 2004 affiliation;
Andreasen–Huge (2011) details; Hull and Rebonato chapter numbers; Bennett's chapter list; volume/page numbers of the
classic additions; Martin's "≈ 5% a year" S&P figure (re-read the paper).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 12 · The Volatility Surface (~58)
1. Smile, skew, term structure, read as the risk-neutral law's skewness and kurtosis (Backus–Foresi–Wu); delta quoting;
   how the surface moves: sticky strike, sticky delta, Derman's regimes (1999), the skew-stickiness ratio, and the
   principal components of daily moves (Cont–da Fonseca 2002).
2. Static no-arbitrage in total variance: Gatheral's g derived, calendar monotonicity, Roper's conditions, Lee's moment
   formula (2004); an arbitrage shown happening (Vogt's SVI).
3. SVI (Gatheral 2004; its Heston origin; the JW parameters; fitted and replayed) and SSVI (Gatheral–Jacquier 2014;
   both theorems; fitted to the Surface in 3D); eSSVI and the exact no-arbitrage SVI region (Martini–Mingone 2022).
4. Dupire (1994) derived from Fokker–Planck; Derman–Kani and Rubinstein's implied trees; BBF's factor of two;
   Gyöngy's projection checked by Monte Carlo on Heston.
5. Local volatility's dynamics: the smile moves against the spot (Hagan et al. 2002), the forward smile fades.
6. Variance swaps and the log contract (Neuberger; Carr–Madan; DDKZ 1999; Britten-Jones–Neuberger 2000): strike
   truncation, jumps, monitoring; replicated on 100 real Bitcoin months; volatility swaps and convexity.
7. The VIX derived and run line by line; our BTC index against Deribit's DVOL for two years; the VIX since 1990.
8. The variance risk premium (Carr–Wu 2009; Bollerslev–Tauchen–Zhou 2009) on BTC and the S&P 500, its P&L skew, and a
   predictability test; Martin's (2017) SVIX bound derived; risk-neutral moments (Bakshi–Kapadia–Madan 2003).
9. Dealer gamma and its feedback, simulated; intraday momentum (Baltussen et al. 2021); 0DTE (Andersen–Fusari–Todorov
   2017; Bandi–Fusari–Renò 2023; Dim–Eraker–Vilkov 2024); VIX1D.
10. VIX futures, the roll, short-volatility notes: the short-term futures index and a −1× note rebuilt from Cboe
    settlements; leveraged-product rebalancing (Cheng–Madhavan 2009).
11. Learning surfaces: a VAE over two years of weekly surfaces (Bergeron et al. 2022) and an arbitrage-penalised network
    (Ackerer et al. 2020), both trained and replayed against SSVI.

*Textbooks:* Gatheral ch. 1, 3, 7, 8, 11 (2, 4–6 → Part 13; 9–10 → Parts 15, 13); Bergomi ch. 2, 3, 5 (rest → 13, 14);
Rebonato *Vol & Corr* (implied vs local, smile dynamics); Hull OFOD "Volatility smiles and surfaces" and the
implied-volatility-function model; Sinclair; Bennett.
*Computed/Trained:* term structure and skew sign over 100 weeks; stickiness tests and surface PCA; Vogt's arbitrage and
Lee's moments on the Surface; SVI and SSVI fit replays; Dupire, BBF ratio, an implied tree; Gyöngy on Heston; LV
repricing and forward skews; strike truncation; variance-swap replication on BTC; vol-swap convexity; our VIX vs DVOL;
VRP on BTC and the S&P 500 with P&L skew and a BTZ test; SVIX and risk-neutral moments; the VX index and inverse note;
gamma feedback; the surface VAE (5 seeds); the penalised neural surface (3 seeds); one net for all weeks.
*Visuals:* the flat plane bending into the skew; stickiness under a spot slider; eigen-surfaces breathing; g glowing
red; the SSVI surface fitting itself in 3D; implied vs local surfaces; the Heston cloud and its conditional variance;
payoffs summing to the log contract; the VX futures ribbon folding on 5 February 2018; long- vs short-gamma paths.
*Labs:* `fit_svi`, `fit_ssvi`, `g_function`/`dupire_local_var`, `var_swap_strike`/`strip_replication`, `vix`,
`vx_index`/`inverse_note`.
*Crisis:* Volmageddon, 5 February 2018: the front VIX future +113%, the rebuilt −1× note −96%.
*Firms:* Cboe and Deribit (index makers); Credit Suisse (XIV, TVIX); ProShares (SVXY); LJM (SEC allegations);
Allianz Global Investors U.S. (Structured Alpha, SEC 2022); dealers' quants (Goldman's DDKZ and Derman–Kani).
*Frontier:* operator deep smoothing (ICLR 2025); VolGAN (2024); deep learning from IV surfaces (Kelly et al.);
no-arbitrage SVI/eSSVI (Martini–Mingone 2022); 0DTE pricing.
*Desk:* "Why is the VIX above realized volatility on average?"; "Replicate a variance swap with options."; "Spot falls
5%: where does ATM vol go under sticky strike, sticky delta and local vol?"
*House:* the surface builder (Rule 12: quote only from a fitted, checked surface; state the dynamics).
```

---

## 6. Implementation notes

**Minutes:** §3 table (≈ 58.0). If short, lengthen ch2, ch6, ch12 (derivation-rich) first.

**New House functions** (append to `explainer/quant/house/volsurface.py` unless noted; tests appended to
`tests/test_quant_house.py`):

| Function | Test |
|---|---|
| `svi_jw(p, T)` / `svi_from_jw(jw, T)` | round trip raw → JW → raw to 1e-10 |
| `lee_moment(beta)` | β = 2 → 0; β → 0 → ∞; inverse of Lee's formula to 1e-12 |
| `ssvi_butterfly_bound(fit)` | returns the smallest θ at which GJ's sufficient conditions hold (0 when γ ≤ ½ and η(1+|ρ|) ≤ 2); matches a brute-force θ scan |
| `skew_stickiness(dlnS, datm, skew)` | simulated sticky-strike data → R ≈ 1; sticky-moneyness → R ≈ 0 |
| `surface_pca(grids)` | explained variance sums to 1; recovers a planted level factor |
| `implied_tree(fit, S0, T, n)` (Derman–Kani, `trees.py` if more natural) | reprices flat-vol surface = CRR to 1e-6; skewed SSVI strikes within 0.2 vol pt |
| `conditional_variance(x, v, k, width)` (Gyöngy) | on a BS simulation returns σ² everywhere |
| `strip_replication(K, otm, F, T, path)` | on a GBM path with dense strikes: error ~ cubic term; on a constant path: 0 |
| `vol_swap_convexity(rv)` | equals √mean − mean√ on a known sample; DDKZ approximation within 10% for small variance |
| `vix_30d(T1, s1, T2, s2)` | reproduces the Cboe white paper's worked example *(if numbers available)* or equals constant input |
| `rn_moments(K, otm, F, T)` (BKM) | lognormal: skew ≈ 3·s·… known closed form; variance = σ²T to 1e-3 |
| `vx_index(settles, expiries, days)`, `inverse_note(r, L)`, `rebalance_flow(L, r, N)` | constant curve → zero return; L = −1, r = 0.1 → flow 0.2N; note path equals cumprod(1 + L r) |
| `gamma_feedback(shocks, lam, gamma_d)` | λΓ = 0 → identity; vol ratio = 1/(1+λΓS) for small shocks |
| `deep.train_surface_net(k, T, iv, penalty, seed, every)` | on SSVI-generated quotes reaches < 0.3 vol pt with zero g violations |

**Compute items** (new names; existing kept): `termskew`, `dynamics`, `arbitrage`, `svi_replay`, `ssvi_replay`, `bbf`,
`dk_tree`, `gyongy`, `lv_reprice`, `fwd_curve`, `trunc`, `replication`, `vixcomp`, `vrp_pnl`, `spx_vrp`, `rn_moments`,
`vx_etp`, `gamma_toy`, `neural_surface`, `operator_net`; `vae` gains seeds and checkpoints (keep its existing keys so
`s07_learning` loads unchanged numbers).

**Data (through `explainer.quant.data`):** FRED `VXVCLS` 2007-12-04…2025-12-31 and `VIXCLS` 1990-01-02…2025-12-31
(new windows: two manifest entries); Yahoo `^GSPC` 1990-01-01…2025-11-30 (one entry); a new loader
`cboe_vx(expiry)` for `https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/VX_<expiry>.csv`
(expiries 2017-05-17 … 2018-04-18, ten files, each checksummed after parsing); Binance 1h and DVOL 2024–25 and the 100
Deribit days already cached. Optional `history_ext` (decision below).

**Risks.**
1. **SSR is not identified** in BTC 2024–25 (corr 0.05, mean skew ≈ 0); never narrate "SSR = 2.4" as a finding.
2. **SSVI's γ > ½**: the "provably arbitrage-free" claim in the current ch2 narration and README is too strong; reword
   to "sufficient condition holds at every quoted maturity" (computed threshold).
3. **Research window:** the trial counter treats tests on 2021+ data carefully; the BTZ regression on 2024–25 is a
   predictive test; register it (counter 73 → 74) or present it as descriptive. Decision for the lead.
4. **Allegations** (XIV, LJM, VIX manipulation) must be labelled as allegations with the firms' responses; outcomes
   to be checked before broadcast.
5. **3D render cost:** five ThreeDScenes with surfaces; keep `resolution` ≤ (32, 24) and Dot3D at (4, 4) as the hook does.
6. **Neural runs under load** took 75 s/seed at load 20; resumable per seed; `torch.set_num_threads(1)`.
7. **0DTE shares** change monthly; quote only Cboe-published figures with their month and year.
8. Moving `s08_house` out of the manifest changes chapter numbering; update `zh_lines.py` CHAPTERS by class.

**Chinese:** new terms for `QUANT_ZH_GUIDE.md`: 总隐含方差 (total implied variance), 偏斜粘性比 (skew-stickiness ratio),
粘性执行价/粘性delta, 蝶式套利/日历套利, 矩公式 (moment formula), 隐含二叉树 (implied tree), 远期微笑 (forward smile),
对数合约 (log contract), 波动率互换的凸性调整, 展期收益 (roll yield), 反向VIX票据, 交易商伽马敞口 (GEX), 当日到期期权 (0DTE),
风险中性矩 (risk-neutral moments).

**Decisions for the lead:** (a) extend the weekly history to April 2021 (`history_ext`, +~25 MB data)? (b) register the BTZ
test with the trial counter? (c) delete `s08_house` or keep it unlisted? (d) accept three new data sources (FRED VXVCLS,
Yahoo ^GSPC, Cboe VX CSVs) into the manifest.

## 7. Lead's decisions (2 Nov 2026)

1. Yes: extend the weekly surface history back to April 2021 through the data layer (resumable, checksummed).
2. The 2024–25 predictability regression is presented as descriptive evidence, not a strategy trial: the trial counter stays at 73 (later parts already show 73).
3. `s08_house` leaves the manifest and the module is deleted; its content moves to the industry chapter and the outro.
4. Yes: FRED VXVCLS and the 1990–2025 VIXCLS window, Yahoo ^GSPC, and Cboe VX settlement CSVs through a new `cboe_vx` loader, all as proper manifest entries with checksums.
Also: reword "provably arbitrage-free" for the fitted SSVI (γ = 0.557 > ½: the Gatheral–Jacquier sufficient condition holds for every quoted maturity, θ above about 1.5·10⁻⁷, not for all θ), in the narration, zh lines and README problem 3. XIV prices, the Second Circuit citation, the LJM outcome, the 0DTE share, chapter numbers and Martin's figure: verify or drop.
