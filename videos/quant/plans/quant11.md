# Part 11 · Trading Options: expansion plan (19.4 → ~57 min)

Planning document only; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 and
§6 Parts 10–13; `READING.md` §1 (volatility and practice books), §3, §4 Parts 10–12; every file in
`videos/quant/quant11/` (`manifest.py`, `common.py`, `compute.py`, all ten scenes, `README.md`); the House modules
`quoting.py`, `hedge.py`, `bs.py`, `surface.py`, `volsurface.py`; `explainer/quant/{__init__,viz,data}.py`
(`lab_card`/`lab_run`, `TrainingReplay`, `seed_band`, `HedgeLedger`, `price_surface`, the timeline);
`videos/ai/LECTURE_GUIDE.md`; the plans for Parts 2–9 and the chapter lists of the built Parts 8, 10, 12, 13 and 17,
so this part does not repeat them. Probe runs (scratchpad, seeded, < 4 CPU-min each) gave the numbers marked
**(probe)**; the implementer recomputes them in `compute.py` and the narration follows what comes back.

**Boundaries with the neighbours (decided here, so the parts do not overlap).**
- Part 10 owns the derivation of the hedger's P&L (½ΓS²(σᵣ² − σᵢ²)), hedging with the wrong vol, discrete-hedging
  error and Leland, and the 1,706-month BTC "sell a hedged call" study. Part 11 *uses* those results and shows them
  as a trader runs them: the P&L explain, the scalper's trades, the choice of hedge frequency.
- Part 12 owns the smile's shape and dynamics, SSVI, Dupire, variance swaps, the VIX, the VRP measured as variance-swap
  minus realized (Carr–Wu), Volmageddon, dealer gamma and 0DTE. Part 11 measures the premium in *option returns*
  (Coval–Shumway, Bakshi–Kapadia) and only points to 0DTE.
- Part 17 owns deep hedging and the learned no-trade band (its chapters 7–8). Part 11 keeps its existing learned
  hedger as one point on the cost–risk chart, with a forward link, and trains a different model: the market maker.
- Parts 36/38 own the limit order book and equity/ETF market making; Part 11 is the options desk's version, in
  volatility units. Part 9 owns parity, conversions and the box spread (mentioned here in one line).

---

## 1. Current state (`python tools/lecture_length.py quant11`: 19.4 min)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 2.8 | Desk question (hedged straddle in a quiet week) with a one-row ladder; the May 2021 BTC straddle at DVOL 74% vs realized 127%, P&L +1.7 on 16.9 (computed `scalp`); objectives; House card. Good hook. **No history segment.** |
| 1 | `s02_greeks` | 1.5 | Two-row ladder (the Taylor series, vanna/volga definitions); six static P&L heat-tiles (spot × vol move). **No derivation of any Greek, no 3D, no real book, no P&L explain.** |
| 2 | `s03_scalp` | 1.5 | Hedge trades dotted on the real path; the gamma/theta/net ledger (+6.4 / −4.6 / +1.7). Static `Create` of finished curves; `HedgeLedger` not used. **No counterfactual (path order), no frequency question.** |
| 3 | `s04_vrp` | 1.4 | DVOL vs HAR forecast vs realized; the registered forecast-edge test (1.75 vs 0.57, t ≈ 2.4; counter 73). Real and good, but thin: **no option-return evidence (Coval–Shumway, Bakshi–Kapadia), no sizing, no tail.** |
| 4 | `s05_mm` | 2.4 | Die game + Glosten–Milgrom (stated); toy vol-quoting book with/without inventory skew (64 → 9 max inventory); three firm cards. **No derivation of the spread or the optimal skew; no real flow data; the "Trained: RL market maker" of the syllabus is absent.** |
| 5 | `s06_expiry` | 2.0 | ATM gamma at a day/an hour/a minute (0.15 → 5.8); pin risk in words; one sentence on early exercise; dispersion identity + 90 years of realized industry correlation. **Three syllabus items (6, 8 and half of 6) squeezed into one chapter; no pinning mechanism, no data test, no dividend play, no implied correlation data.** |
| 6 | `s07_india` | 2.6 | SEBI study stats (91%, ₹1.8 lakh crore, ₹1.06 lakh crore), the Oct 2024 circular, the interim-order crisis card, the impact toy. Careful and well labelled. **Two items in one chapter; no data on what short-dated option buyers earn; no appeal status.** |
| 7 | `s08_hedging` | 1.7 | Whalley–Wilmott band picture; cost/risk frontier of every-step, fixed bands, WW and a deep hedger (κ = 1, 4, 16). Good computed chart, but the learner is not shown learning, and Part 17 now owns this. **No hedging with options (gamma/vega with a second option).** |
| 8 | `s09_house` | 0.8 | Table of House functions; Rule 11; trial counter 73. |
| — | `s10_outro` | 2.6 | Recap (8 lines), 3 desk questions, 5 problems, payoffs, references, next part. |

Overall: the experiments are real (keep all seven compute items), but there are **no full derivations** (two short
ladders), **no 3D**, **no live simulation** (finished curves are `Create`d), **no lab moments**, **no training
replay** (the deep hedger and the toy book are reported, not watched), **no industry or frontier chapter**, no crisis
file of the part's own (the hook month is a case, not a blow-up), and the books' core practice material (synthetics
and early exercise, hedging with options, position analysis, sizing) is missing.

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item (SYLLABUS §6 Part 11) | Now | Plan |
|---|---|---|
| 1 Positions as Greeks; P&L as gamma vs theta | ch1 (1.5 min) | ch1 (Greeks derived, real P&L explain) + ch2 |
| 2 Gamma scalping on a real path; the variance it captures | ch2 (1.5) | ch2 (live ledger, path-order counterfactual) + ch3 (hedge frequency on 244 real 30-day windows) |
| 3 Vega, vanna, volga; RR and BF | two ladder rows | ch4 (derived; vanna–volga smile rebuilt on the Surface; 100 weeks of RR/BF) |
| 4 Strategies and what each bets on | six heat-tiles | ch5 (3D P&L surfaces morphing; 96 real four-week trades on real smiles) |
| 5 Realized vs implied; VRP; the forecaster's edge (Sinclair) | ch3 (1.4) | ch6 (the premium in option returns) + ch7 (the edge test, sizing, the tail) |
| 6 Pin risk and expiry; early exercise and dividend plays | half of ch5 | ch11 (expiry, gamma, pinning: mechanism and a BTC test) + ch12 (early exercise, the dividend play) |
| 7 Market maker's book: quoting, hedging the residual, inventory in Greeks | ch4 (2.4), ch7 | ch8 (spread and adverse selection, measured on Deribit) + ch9 (optimal skew; the trained market maker) + ch10 (hedging the book with options and under costs) |
| 8 Dispersion, implied correlation | half of ch5 | ch13 (Cboe implied correlation 2006–2025 against realized; the trade's P&L) |
| 9 India's expiry-day boom | half of ch6 | ch14 (+ what short-dated option buyers earned on Deribit) |
| 10 Case file: SEBI v. Jane Street (alleged) | half of ch6 | ch15 (order, appeal, the 2024 Millennium suit; the toy as a 3D region) |
| *Trained:* RL options market maker | absent | ch9 (Q-learning against the exact dynamic program and the GLFT formula; 5 seeds) |
| *Computed:* scalping on BTC; implied correlation | partly | ch2–3; ch13 (Cboe COR3M) |
| *Visuals:* P&L surface over (spot, vol); scalper's trades | 2D tiles; dots | ch5 3D; ch2 live |
| *Firms:* SIG, Optiver, IMC, Jane Street | cards | ch17 (+ Citadel Securities, Wolverine via PFOF; Optiver's CFTC case) |
| *Desk:* die game; long straddle, no move | kept | kept, + one new (ch12) |
| *House:* the options quoting engine | ch8 | outro (as in Part 5's plan) + labs in ch1, 2, 9, 10, 13 |
| (standard) crisis file | none | ch16: short-volatility blow-ups (LJM 2018; Structured Alpha 2020) |
| (standard) industry and frontier chapters | none | ch17, ch18 |

### (b) Textbook sections → chapter

The four books' tables of contents could not be fetched from the publishers this session (McGraw-Hill's page lists
topics only; O'Reilly and retailer pages refused). Chapter numbers below are from memory and marked *(verify)*;
the topic mapping holds whatever the numbering.

| Book · section | Chapter here / elsewhere |
|---|---|
| Natenberg 2nd ed. (2015) ch. 1–4 contracts, forward pricing, settlement, expiration P&L *(verify)* | Part 2; ch5 (expiration P&L diagrams as the surfaces' t = T slice) |
| Natenberg ch. 5–6 theoretical pricing, volatility *(verify)* | Part 10; ch6 (realized/implied/forecast, "a trader's four volatilities") |
| Natenberg ch. 7, 9 risk measurement I–II (the Greeks, second-order) *(verify)* | ch1, ch4 |
| Natenberg ch. 8 dynamic hedging *(verify)* | ch2, ch3 |
| Natenberg ch. 10–11 introduction to spreading; volatility spreads *(verify)* | ch5 |
| Natenberg ch. 12 risk considerations (choosing among spreads) *(verify)* | ch5 (bets table), ch7 (sizing) |
| Natenberg ch. 13 bull and bear spreads *(verify)* | ch5 |
| Natenberg ch. 14–15 synthetics; option arbitrage (conversions, reversals, boxes) *(verify)* | ch12 (one card); Part 9 owns parity and boxes |
| Natenberg ch. 16 early exercise of American options *(verify)* | ch12 |
| Natenberg ch. 17 hedging strategies *(verify)* | ch10 |
| Natenberg ch. 18 models and the real world *(verify)* | ch11 (expiry, discontinuities), ch16 (tails) |
| Natenberg ch. 19 volatility revisited *(verify)* | ch6–7 |
| Natenberg ch. 20 position analysis *(verify)* | ch1 (the risk report and P&L explain), ch10 |
| Natenberg ch. 21 stock index futures and options *(verify)* | ch13 (index vs components), ch14 |
| Natenberg ch. 22 intermarket spreading *(verify)* | ch13 (dispersion as an intermarket spread) |
| Natenberg ch. 23–24 volatility contracts; skews *(verify)* | Part 12 (variance swaps, VIX, skew); ch4 here (RR/BF) |
| Sinclair *Volatility Trading* 2nd ed. (2013): option pricing; volatility measurement and forecasting *(verify)* | Part 7 (HAR) and ch6–7 |
| Sinclair VT: implied volatility dynamics and the premium *(verify)* | ch6; Part 12 |
| Sinclair VT: hedging (frequency, bands, the hedging-volatility choice) *(verify)* | ch3, ch10 |
| Sinclair VT: trade sizing (Kelly) and money management *(verify)* | ch7 (Kelly for a short-vol bet); Part 8 owns Kelly |
| Sinclair VT: trading psychology, event volatility *(verify)* | ch7 (one line on events); README note |
| Sinclair *Positional Option Trading* (2020): the premium, finding edges, choosing structures, sizing *(verify)* | ch5–7 |
| Taleb *Dynamic Hedging* (1997) Part I: instruments, market making, liquidity holes *(verify)* | ch8–9, ch16 |
| Taleb Part II: delta, gamma and "shadow gamma", vega and its buckets, theta and the minor Greeks, correlation *(verify)* | ch1, ch2, ch4, ch10 (vega buckets), ch13 |
| Taleb: pin risk, the binary at expiry, bleed *(verify)* | ch11 |
| Taleb Part III exotics (barriers, binaries, multi-asset) | Part 15 |
| Bennett *Trading Volatility* (2014) ch. 1 options; ch. 2 volatility trading (variance swaps) | ch2–3; Part 12 |
| Bennett ch. 3 (Black–Scholes assumptions stretched), ch. 4 forward-starting products and volatility indices | Part 12–13 |
| Bennett ch. 5 exotics (quanto, composite) | Part 15, Part 22 |
| Bennett ch. 6 relative value and correlation trading (dispersion) | ch13 |
| Bennett: skew and term-structure trading *(chapter number unconfirmed)* | ch4 (RR/BF), ch5 (calendar); Part 12 |
| Hull OFOD "Trading strategies involving options"; "The Greek letters" (READING §2) | ch5; ch1, ch10 |

### (c) Papers on the Part 11 list in READING.md

| Paper | Now | Plan |
|---|---|---|
| Carr–Madan (1998) "Towards a theory of volatility trading" | absent | ch3: the gamma-weighted vs variance-weighted payoff (why a straddle is a dirty variance bet); one card |
| Coval–Shumway (2001) | absent | ch6: card + the BTC replication on real smiles |
| Bakshi–Kapadia (2003) | absent | ch6: card + delta-hedged gains on 96 BTC weeks |
| Avellaneda–Lipkin (2003) | absent | ch11: the pinning mechanism, simulated |
| Ni–Pearson–Poteshman (2005) | absent | ch11: card + the BTC clustering test |
| Gârleanu–Pedersen–Poteshman (2009) | absent | ch9: demand pressure prices options because market makers cannot hedge perfectly; the skew of the inventory-averse quote |
| Driessen–Maenhout–Vilkov (2009) | named on card | ch13: the correlation risk premium |
| Goyal–Saretto (2009) | absent | ch7: the cross-sectional version of the edge test (HV − IV sorts) |
| Stoikov–Sağlam (2009) | absent | ch9: the option market maker's HJB in vega units |
| Baldacci–Bergault–Guéant (2021) | absent | ch9: many options, inventory in vega, dimensionality reduction; ch18 |
| SEBI interim order (3 Jul 2025) | on screen | ch15 |
| Millennium v. Jane Street *(verify)* | not on screen | ch15. **Correct the READING entry:** the suit was *Jane Street v. Millennium Management* and two former Jane Street traders (S.D.N.Y., filed April 2024), dismissed after a settlement filed 6 December 2024, terms undisclosed (Bloomberg Law; Hedgeweek) — verify on the court docket (PACER/CourtListener) before it goes on screen. |

Proposed additions to READING.md Part 11 (classic and industry): Glosten–Milgrom (1985) *JFE*; Hodges–Neuberger
(1989) *Rev. Futures Markets*; Whalley–Wilmott (1997) *Math. Finance*; Leland (1985) (shared with Part 10);
Castagna–Mercurio (2007) "The vanna-volga method for implied volatilities", *Risk*; Avellaneda–Stoikov (2008) *QF*;
Guéant–Lehalle–Fernandez-Tapia (2013) "Dealing with the inventory risk", *Math. Financial Economics*; Pool–Stoll–Whaley
(2008) "Failure to exercise call options: an anomaly and a trading game", *J. Futures Markets* *(verify volume)*;
Hao–Kalay–Mayhew (2010) "Ex-dividend arbitrage in option markets", *RFS* *(verify)*; Golez–Jackwerth (2012)
"Pinning in the S&P 500 futures", *JFE* *(verify)*; Muravyev (2016) "Order flow and expected option returns", *JF*;
Muravyev–Pearson (2020) "Options trading costs are lower than you think", *RFS*; Hull–White (2017) "Optimal delta
hedging for options", *J. Banking & Finance*; Buehler–Gonon–Teichmann–Wood (2019) (on screen already; Part 17's).
Frontier (verified this session): Bali, Beckmeyer, Mörke, Weigert (2023) *RFS* 36(9):3548–3602; Bryzgalova,
Pavlova, Sikorskaya (2023) *JF* 78(6):3465–3514; Cao, Chen, Farghadani, Hull, Poulos, Wang, Yuan (2023) "Gamma and
vega hedging using deep distributional reinforcement learning", *Frontiers in AI* 6:1129370 (arXiv 2205.05614);
"Market making of options via reinforcement learning" (arXiv 2307.01814, 2023; authors *(verify)*); SEBI F&O study
update (7 July 2025). Industry: CFTC v. Optiver (2008 complaint, 2012 order); SEC v. LJM (2021); U.S. v. AGI US
(2022). Remove nothing.

---

## 3. The chapter list (hook + 18 chapters + outro, about 57 min)

Conventions as in Part 5's plan: **Visual** is the signature picture, built before the formula; **Live** a
simulation drawn as it runs; **Lab** a `lab_card` (≤ 12 lines of real House code) then `lab_run` with the cached
output; **Replay** a `TrainingReplay`/ValueTracker scrub with seeds as `seed_band`; **Compute** the `compute.py`
item and CPU minutes (one core). Existing modules and Scene classes are kept for kept chapters; new chapters get new
modules (`s03a_…` sorts beside its neighbour; the manifest sets the order). All money is "per 100 of underlying"
unless said.

### H · Hook: "Gamma against theta" (3.0) · `s01_hook` (deepened)
- Goal: the puzzle, the era, the map.
- Beats: (1) keep the desk question and its ladder; (2) keep May 2021 (DVOL 74%, realized 127%, P&L +1.7 on a
  premium of 16.9) but draw it **live**: a `ValueTracker` walks the hour index; the BTC path, the hedge position and
  a `HedgeLedger` (gamma green, theta red, net) fill together, so the viewer sees the crash pay little because the
  ledger's gamma bar stops growing once spot leaves the strike; (3) **new, "how we got here" (≈ 60 s)**: the timeline
  strip lit at 1973 (CBOE opens; floor traders quote volatility), 1985 (Glosten–Milgrom; Leland), 1987 (Black
  Monday; SIG founded months before), 2000 (Jane Street), 2018 (Volmageddon), 2020 (negative oil; Structured Alpha
  inside the same March), 2021 (GameStop: retail options), 2024 (India's F&O curbs); (4) objectives card (10 items +
  industry + frontier); (5) House card.
- Pause-and-predict: "Realized volatility was nearly twice what you paid. Did the straddle double its money?"
  (No: +1.7 on 16.9.)
- Compute: `scalp` (exists, < 0.1).

### 1 · Positions as Greeks, and the P&L explain (3.2) · item 1 · `s02_greeks` (kept module, rebuilt)
- Goal: a book is one Taylor series; derive each Greek's sign and size; a real next-day P&L explained to within 2%.
- Beats: **Visual (3D)**: `ThreeDAxes` (spot S, days to expiry τ, value V); the straddle's value surface. A plane
  tangent at today's point is drawn; the gap between surface and plane along S is the gamma "bowl"; sliding the
  point one day toward expiry (`ValueTracker` on τ) sinks the bowl by θ. The camera orbits so the viewer sees the
  bowl's depth (½Γ dS²) and the drop (θ dt) as two lengths that cancel at the breakeven move. Then desk conventions
  card: cash delta (Δ·S), gamma per 1% move (½ΓS²·0.01²), vega per vol point, theta per day. Then the **P&L explain**
  on the real Surface: a five-leg book (long ATM straddle, short two 90% puts, long a 110% call; 30 days) on
  10 December 2025, revalued on 11 December's smile; a waterfall builds bar by bar: delta, gamma, theta, vega,
  vanna, volga, unexplained.
- Derivation (ladder):
  - $\Pi(S+dS,\sigma+d\sigma,t+dt) - \Pi = \Delta dS + \tfrac12\Gamma dS^2 + \Theta dt + \mathcal V d\sigma +
    \text{vanna}\,dS\,d\sigma + \tfrac12\text{volga}\,d\sigma^2 + \dots$ (Taylor in three variables).
  - $\Delta = N(d_1)$, $\Gamma = \frac{\varphi(d_1)}{S\sigma\sqrt\tau}$, $\mathcal V = S\varphi(d_1)\sqrt\tau$
    (differentiate the formula; $S\varphi(d_1) = Ke^{-r\tau}\varphi(d_2)$ cancels the cross terms).
  - $\Theta = -\tfrac12\sigma^2S^2\Gamma$ at $r = 0$ (the Black–Scholes PDE; Part 10).
  - $\tfrac12\Gamma dS^2 + \Theta dt = \tfrac12\Gamma S^2\big[(dS/S)^2 - \sigma^2dt\big]$ (substitute), so the
    breakeven daily move is $\sigma\sqrt{dt}$: 50% vol ⇒ 2.6% a day (worked example).
  - $\mathcal V = \sigma\tau S^2\Gamma$ (one bump seen as vega and gamma; Part 10's identity used to read a risk
    report: long gamma and long vega go together for vanillas).
- Experiment (`explain`, real data): **(probe)** spot −2.40% overnight, ATM 30-day vol 43.7% → 41.1%; book P&L
  −1,521 (USD per unit notional of the legs), explained −1,548: delta −1,570, gamma +130, theta −86, vega −74,
  vanna +61, volga −8; unexplained +28 (1.8%). The narration names vanna as the surprise (spot and vol fell
  together) and branches on |unexplained|/|actual|.
- Lab 1: `quoting.book_greeks` (quoting.py lines 43–49, 7 lines), run on the five-leg book, printing the cash Greeks.
- Pause-and-predict: "50% vol. How far must the stock move today for a long-gamma hedged book to break even?"
  (σ√(1/365) ≈ 2.6%.)
- Compute: `explain` (surface fits of two days, 0.5 min; the trades are cached).

### 2 · Gamma scalping on a real path (3.0) · item 1–2 · `s03_scalp` (kept, deepened)
- Goal: watch the scalper trade; see that the path's *order* sets the P&L, not just its variance.
- Beats: **Live**: the existing trades chart becomes a running scene: one `ValueTracker` over 720 hours drives the
  path, the hedge (units of BTC held), buy/sell dots appearing as they happen, and the `HedgeLedger` bars. **Visual
  (3D, where gamma lives)**: the dollar-gamma landscape ½ΓS²(S, t) for the straddle drawn as a ridge along the
  strike that sharpens toward expiry; the May 2021 path is lifted onto it as a glowing curve. The viewer sees the
  path climb the ridge in the first fortnight and slide off it on the 19th: the crash happened on the lowland. Then
  the counterfactual: the same 720 hourly returns **reshuffled** 2,000 times (identical realized variance, different
  order); the histogram of P&L builds up with the real month marked.
- Derivation:
  - $P\&L = \sum_k \tfrac12\Gamma_k S_k^2\big(r_k^2 - \sigma_i^2\Delta t\big) + \text{residual}$ (sum the ch1
    identity over the hedging steps).
  - $\mathbb E[P\&L \mid \text{path}] \neq f(\sum r_k^2)$: the weight $\Gamma_kS_k^2$ depends on where spot is when
    the move happens (Part 10's El Karoui–Jeanblanc–Shreve weight, now on one real month).
  - Carr–Madan (1998): a payoff weighting every move by $1/S^2$ instead (the log contract) collects $\sum r_k^2$
    exactly; that is the variance swap (Part 12).
- Experiment: `scalp` (exists); `scalp_shuffle` (new): 2,000 permutations of the hourly returns, P&L for each (same
  RV by construction); expected: the real +1.7 sits in the lower part of a wide distribution whose mean is far
  higher (computed; branch on the percentile).
- Lab 2: `hedge.delta_hedge`, the accounting lines (hedge.py lines 74–79: the step's mark-to-market, the gamma term,
  the theta term), run on the May path with `record=[0]`, printing the three totals.
- Pause-and-predict: "Same returns, crash on day 2 instead of day 19. More or less?" (Computed from a single reorder.)
- Compute: `scalp_shuffle` (2,000 × 2 legs × 720 steps vectorized: 1 min).

### 3 · How often to hedge, and the variance you capture (2.8) · item 2 · `s03a_frequency` (new)
- Goal: hourly vs daily vs move-triggered hedging, measured on every 30-day window of 2021–2025; what intraday mean
  reversion does to the scalper.
- Beats: **Live**: one month, three hedgers running side by side (hourly in gold, daily in blue, "rehedge on a 2%
  move" in green), their hedge positions stepping as the path unrolls; their ledgers race. Then the 244 windows as a
  scatter (P&L against realized minus implied vol) with one colour per rule, filling week by week, and the
  regression lines. Then the variance ratio: daily variance against 24× hourly variance as a single number with its
  meaning (mean reversion inside the day means the hourly scalper is paid more than the daily one).
- Derivation:
  - Hedging error per step $\approx \tfrac12\Gamma S^2(r^2 - \sigma^2\Delta t)$, variance $\tfrac12\Gamma^2S^4\sigma^4\Delta t^2$
    per step, so the total sd $\propto \sqrt{\Delta t}$ (Part 10's result, recalled in one line).
  - With returns that are negatively autocorrelated within the day, $\operatorname{Var}(\sum_{24} r) = 24\sigma_h^2
    (1 + 2\sum_j(1-\tfrac j{24})\rho_j) < 24\sigma_h^2$ (variance ratio < 1), so the gamma collected at hourly
    steps exceeds the daily one by $\tfrac12\Gamma S^2(24\sigma_h^2 - \sigma_d^2)$ per day.
  - Move-triggered hedging (Zakamouline's "hedge on a band in spot") trades only when $|S/S_{\text{last}} - 1| > h$;
    each trade locks $\approx \tfrac12\Gamma S^2h^2$.
- Experiment: `frequency` (new): long 30-day ATM straddles at DVOL every 7 days, April 2021–November 2025, hedged
  hourly, 4-hourly, daily and on 2% moves; mean, sd, correlation with RV − IV; the BTC variance ratio. Numbers:
  **(probe, 244 windows, no costs)** mean P&L per 100: hourly −2.86 (sd 3.51), 4-hourly −2.69 (3.81), daily −2.59
  (4.27), on 2% moves −2.88 (3.75); correlation with RV − IV 0.88, 0.86, 0.82, 0.86; BTC variance ratio daily /
  (24 × hourly) = 0.978 (a trace of intraday mean reversion, too small to matter). The lesson the data gives:
  frequency buys *precision* (sd falls from 4.27 to 3.51, and the P&L tracks the volatility gap more tightly), not
  *mean*; and the mean is negative because DVOL was above realized (ch6). Narration branches on whether the mean
  differences exceed their paired standard error (here they should not). Add a second panel with 10 bp costs
  (`hedge.delta_hedge(cost=…)`), where the hourly hedger's precision is paid for (computed).
- Pause-and-predict: "If BTC trends within the day, does hedging more often help the long-gamma trader?" (No: with
  positive autocorrelation the daily hedger collects more.)
- Compute: `frequency` (≈ 4 min).

### 4 · Vega, vanna, volga: the risk reversal and the butterfly (3.0) · item 3 · `s03b_secondorder` (new)
- Goal: the second-order Greeks derived and seen; the 25-delta RR and BF as the market's prices of vanna and volga;
  rebuild a real smile from three quotes.
- Beats: **Visual (3D)**: the vega surface $\mathcal V(K, \sigma)$ of a 30-day option; vanna drawn as the surface's
  slope along spot/strike, volga as its curvature along σ; a 25-delta put and call marked as two flags, ATM as a
  third. The camera shows that ATM sits on the ridge (volga ≈ 0) and the wings on the flanks (volga > 0). Then the
  vanna–volga construction: three instruments (ATM straddle, 25Δ RR, 25Δ BF) whose weights solve a 3×3 system to
  hedge vega, vanna and volga; the smile is rebuilt from those three numbers and laid over the real SSVI smile of
  10 December 2025. Then 100 weekly 30-day RR and BF (2024–2025) as two time series under the BTC price.
- Derivation:
  - $\text{vanna} = \partial_\sigma\Delta = -\varphi(d_1)\,d_2/\sigma$, $\text{volga} = \partial_\sigma\mathcal V =
    \mathcal V\,d_1d_2/\sigma$ (differentiate $d_1$ in σ: $\partial_\sigma d_1 = -d_2/\sigma$).
  - ATM-forward: $d_1 d_2 = -\sigma^2\tau/4 \approx 0$ ⇒ volga ≈ 0; at 25Δ, $d_1 = \pm0.674$ ⇒ volga > 0, vanna of
    opposite signs on the two wings (so $RR = \sigma_{25C} - \sigma_{25P}$ loads on vanna, $BF = \tfrac12(\sigma_{25C}
    + \sigma_{25P}) - \sigma_{ATM}$ on volga).
  - Vanna–volga: $C^{VV}(K) = C^{BS}(K) + \sum_{i=1}^3 x_i(K)\,[C^{mkt}_i - C^{BS}_i]$, with $x(K)$ solving
    $\sum_i x_i\,(\mathcal V_i, \text{vanna}_i, \text{volga}_i) = (\mathcal V, \text{vanna}, \text{volga})(K)$
    (match the three sensitivities; Castagna–Mercurio 2007). The implied vol of $C^{VV}$ is the rebuilt smile.
- Experiment: `secondorder` (new): on the Surface day, 25Δ strikes from the SSVI smile (solve $\Delta(K, \sigma(K)) =
  0.25$), RR and BF, the VV smile vs SSVI (RMSE in vol points over |k| < 0.3); 100 weekly RR/BF from Part 12's
  `history` grid (read through `videos.quant.quant12.compute.load`). Expected: VV within about a vol point inside
  the 10–90 delta range and worse in the far wings (computed; branch); RR negative (put skew) in most weeks, with
  call-skew spells in rallies (computed share).
- Pause-and-predict: "Which has more volga, an ATM straddle or a 25-delta strangle of the same vega?" (The strangle.)
- Compute: `secondorder` (< 1 min).

### 5 · Strategies: what each structure bets on, and what it paid (3.2) · item 4 · `s03c_strategies` (new; tiles move here from `s02_greeks`)
- Goal: every standard structure as a shape over (spot move, vol move) and over time; then a real record.
- Beats: **Visual (3D, the syllabus's "P&L surface over (spot move, vol move)")**: one `ThreeDAxes` surface that
  **morphs** straddle → strangle → risk reversal → butterfly → call spread → calendar (`Transform` between
  `price_surface`s of `quoting.pnl_surface`), the camera holding a 3/4 view; a second ValueTracker advances the
  holding period from 0 to 21 days so each surface sinks (theta) or rises; the expiration P&L (Natenberg's
  diagram) is the surface's last slice, drawn as a line on the floor. A "bets" card per structure (gamma, vega,
  direction, skew, term). Then the **record**: 96 four-week trades of each structure, priced each Wednesday on
  that day's real Deribit smile (Part 12's `history` SSVI grid) and settled on Binance's price 28 days later; six
  violin/strip plots fill week by week.
- Derivation: structure Greeks as sums of legs (one line each), e.g. straddle $\Gamma = 2\Gamma_{ATM}$, $\Delta \approx
  0$; RR $\mathcal V \approx 0$, $\Delta \approx 0.5$; BF $\Gamma < 0$ near the body and $> 0$ in the wings; calendar
  $\mathcal V_{far} - \mathcal V_{near} > 0$ and $\Gamma_{far} - \Gamma_{near} < 0$ (the $\sqrt\tau$ and $1/\sqrt\tau$
  scalings).
- Experiment: `strategies` (new). **(probe)** 96 trades each, 2024-01 to 2025-11, per 100 of BTC: straddle mean
  −0.65, median −3.18, wins 34%; strangle (±10%) −0.50 / −2.83 / 23%; risk reversal +2.37 / −0.37 / 27% (BTC rose
  in the sample); butterfly +0.15 / −1.42 / 44%; call spread +0.87 / −1.79 / 46%; calendar +0.09 / −0.17 / 44%;
  none with a Newey–West t above 1.6. The narration says what the record can and cannot show: two years of one
  asset, an up-market; the medians tell the theta story, the means the tails.
- Pause-and-predict: "Which structure loses money in the most weeks?" (The strangle: 77% of weeks.)
- Compute: `strategies` (< 1 min).

### 6 · The volatility risk premium in option returns (2.8) · item 5 · `s04a_premium` (new)
- Goal: what buying options earns, unhedged (Coval–Shumway) and hedged (Bakshi–Kapadia); why it is a premium.
- Beats: **Live**: 96 weekly hedged straddles run as a stack of tiny ledgers (one row per week, each filling in
  green or red as its four weeks pass); the running mean with ±2 NW-se band converges below zero. Cards: Coval and
  Shumway (2001): ATM S&P straddles lost about 3% a *week* *(verify the figure in the paper)*; Bakshi and Kapadia
  (2003): delta-hedged gains negative, more so at the money, so the market prices volatility risk. Then the
  insurance picture: the left tail of the short side's distribution (from ch5's record) shaded.
- Derivation:
  - $\Pi_T = \int_0^T\tfrac12\Gamma S^2(\sigma_r^2 - \sigma_i^2)dt + \varepsilon$ (Part 10), so
    $\mathbb E^P[\Pi_T] < 0 \iff \sigma_i^2 > \mathbb E^P_\Gamma[\sigma_r^2]$ (the gamma-weighted expected variance).
  - Under Q, $\mathbb E^Q[\Pi_T] = 0$ (a self-financing hedged position is a Q-martingale); so a negative P-mean is a
    *risk premium* $\mathbb E^P - \mathbb E^Q$, paid for bearing variance risk that rises in crashes (a negative
    market price of volatility risk, Bakshi–Kapadia).
- Experiment: `premium` (new): the hedged straddle of ch5's record, hourly hedges. **(probe)** mean −1.22 per 100,
  median −1.37, positive in 26% of weeks, NW t = −3.65 (n = 96, overlapping four-week windows, 4 lags). This is
  measured at the market's own ATM implied, not at DVOL, so it complements Part 12's variance-swap VRP. Narration
  branches on t.
- Pause-and-predict: "If the premium is so reliable, why doesn't everyone sell straddles?" (ch16's answer.)
- Compute: `premium` (shares `strategies`' loop, 1.5 min).

### 7 · A forecaster's edge, tested, and how much to bet (3.0) · item 5 · `s04_vrp` (kept, deepened)
- Goal: Sinclair's rule tested out of sample (kept); the cross-sectional version; sizing a short-vol bet; the tail.
- Beats: keep `series` (DVOL vs HAR vs realized) and `result` (1.75 vs 0.57, t ≈ 2.4; counter 73), now with the
  monthly bars **filling live** month by month in two colours. Add: Goyal–Saretto (2009) card — sorting stocks on
  HV − IV earned large straddle spreads (the cross-section of the same idea; Part 25 tests such sorts). Then
  **sizing**: the Kelly fraction for a bet with the measured mean and variance and its fat left tail: a slider over
  the fraction f drawing the expected log-growth curve computed on the empirical monthly P&L distribution, with the
  worst month marked; the maximum sits far below the Gaussian Kelly f = μ/σ² (Sinclair's sizing chapter; Part 8).
- Derivation:
  - $g(f) = \mathbb E\log(1 + fX)$, $g'(0) = \mathbb EX$, $f^*_{Gauss} = \mu/\sigma^2$ (second-order expansion).
  - With a left tail: $g(f) \to -\infty$ as $f \to 1/|x_{\min}|$, so $f^* < 1/|x_{\min}|$ (log of a loss of
    everything), which binds before $\mu/\sigma^2$ for short-vol P&L.
- Experiment: `edge` (exists), `envelope` (exists), `kelly` (new; the empirical g(f) on Part 10's 1,706 monthly
  P&Ls, read via `load10("btc")`): f*_empirical against f*_Gauss (computed; branch).
- Pause-and-predict: "Your edge has t = 2.4 on 43 months. Lever it 5×?" (No: the trial counter and the tail.)
- Compute: `kelly` (< 0.1).

### 8 · Making a market: the spread, and who you trade with (3.0) · item 7 · `s05_mm` (kept: `game`; `book` moves to ch9; `firms` to ch17)
- Goal: derive the spread from adverse selection; measure it on real Deribit trades.
- Beats: keep the die game ladder. **Visual (Glosten–Milgrom, live)**: a fair-value distribution (a bar over two
  values, high and low) that re-weights after each simulated trade: buys push it up, sells down; bid and ask lines
  close in as the market maker learns, and the spread shrinks to zero once the value is known. Then **real flow**:
  524,741 Deribit BTC option trades (100 Wednesdays, 00–12 UTC) as a rain of dots (taker buys gold, sells blue) on
  a moneyness × tenor plane; then the maker's markout curve: the edge at the trade versus mark, and what is left
  5 minutes, 30 minutes and 1 hour later after delta-hedging, in vol points.
- Derivation:
  - $ask = \mathbb E[V\mid \text{buy}] = \frac{\pi\,(\mu + (1-\mu)/2)\,V_H + (1-\pi)(1-\mu)/2\,V_L}{\Pr(\text{buy})}$
    with informed share μ (Bayes).
  - $ask - bid = \mu(V_H - V_L)$ at π = ½ (substitute; the spread is the informed share times the uncertainty).
  - Effective spread vs realized spread: edge at trade $= s\,(p - m_t)$; markout $= s\,(p - m_{t+h}) + \Delta\,(I_{t+h} -
    I_t)$ (delta-hedged); adverse selection $=$ edge − markout (Huang–Stoll style decomposition).
- Experiment: `flow` (new). **(probe)** maker edge against Deribit's mark at the trade: mean 0.36 vol points
  (median 0.17); delta-hedged markout +0.26 after 5 min, +0.22 after 30 min, +0.21 after 1 h (coverage 88/83/78% of
  trades with a later print on the same instrument): about 40% of the edge goes back to informed flow within the
  hour. Taker buys and sells are balanced by vega (OTM calls 29% bought vs 27% sold; OTM puts 15% vs 16%). Large
  trades (top 5% by size) pay a wider edge (median 0.33 vs 0.16). Mark price is Deribit's, an exchange model price,
  so the edge is "against the exchange's fair value" (said on screen).
- Lab 3 (new function): `quoting.markouts(...)` (≤ 12 lines: sign, edge, the delta-hedged markout), run on one day
  with its three-line output.
- Pause-and-predict: "Your quote is hit and the market moves against you. Was your spread too narrow or too wide?"
- Compute: `flow` (≈ 3 min over 100 days; cached per day with `CACHE.partial`).

### 9 · Inventory: the optimal quote, and a market maker that learns (3.4) · item 7 · `s05a_inventory` (new)
- Goal: Avellaneda–Stoikov/GLFT in vega units, derived; the exact dynamic program; the syllabus's **trained RL market
  maker**, watched learning against it.
- Beats: keep the existing toy book (`mm`: max inventory 64 vs 9) as the motivation. **Derivation** of the reservation
  price and spread. **Visual**: the policy map (rows: inventory −10…+10 vega units; colour: quote skew) as a heat
  strip beside the inventory axis. **Replay**: tabular Q-learning (5 seeds) scrubbed through checkpoints 0, 10k,
  50k, 200k, 800k steps: the learned skew strip morphing from noise to the staircase of the exact DP optimum (drawn
  as a white outline), the loss panel replaced by "greedy value as % of the DP optimum" with a seed band; baselines
  as dashed lines at equal budget: symmetric fixed quotes and the GLFT closed form. **Live**: the trained agent and
  the symmetric quoter run on the same 2,000 clients, inventories drawn as they happen.
- Derivation:
  - Fills: $\lambda^\pm(\delta) = Ae^{-k\delta}$; objective $\mathbb E[X_T + q_TS_T] - \tfrac\gamma2\sigma^2\int q_t^2dt$
    (Cartea–Jaimungal's running penalty form).
  - HJB: $\partial_t\theta + \max_{\delta^\pm}\sum_\pm\lambda^\pm(\delta^\pm)[\delta^\pm + \theta(q\mp1) - \theta(q)] -
    \tfrac\gamma2\sigma^2q^2 = 0$ (ansatz $u = x + qs + \theta(t,q)$).
  - First-order condition: $\delta^{\pm*} = \tfrac1k + \theta(q) - \theta(q\mp1)$ (differentiate $Ae^{-k\delta}(\delta +
    \cdot)$).
  - Reservation price $r = s - q\gamma\sigma^2(T-t)$ and spread $\delta^a + \delta^b = \gamma\sigma^2(T-t) +
    \tfrac2\gamma\ln(1+\tfrac\gamma k)$ (Avellaneda–Stoikov's expansion); GLFT's stationary limit
    $\delta^{\pm} \approx \tfrac1\gamma\ln(1+\tfrac\gamma k) \pm \tfrac{2q\pm1}{2}\sqrt{\tfrac{\sigma^2\gamma}{2kA}
    (1+\tfrac\gamma k)^{1+k/\gamma}}$.
  - In an options book, $q$ is vega inventory and $\sigma$ the vol of implied vol (Stoikov–Sağlam 2009); many options
    reduce to a few risk factors (Baldacci–Bergault–Guéant 2021).
- Experiment: `mm` (exists); `mm_learn` (new). **(probe)** inventory ±10, A = 0.45, k = 1.5, seven offsets per side,
  φ = 0.02, discount 0.995: value iteration gives the optimum (value 15.5 at q = 0); best symmetric fixed quote −1.0
  (the penalty eats it); Q-learning with exploring starts reaches 13.1–13.6 (84–88% of the optimum) after 800k steps,
  35 s per seed; its skew matches the DP staircase near q = 0 and is noisier at rarely visited inventories. The
  implementer should parametrize actions as (half-spread, skew) to reduce noise and use 5 seeds.
- Lab 4: `quoting.quote` (quoting.py lines 84–93, 10 lines), run at inventories −20, 0, +20.
- Pause-and-predict: "You are long 20 vega. Do you raise or lower both quotes?" (Lower.)
- Compute: `mm_learn` (5 seeds × ~1 min, plus DP < 0.1).

### 10 · Hedging the book: Greeks with options, and under costs (3.0) · item 7 · `s08_hedging` (kept, refocused)
- Goal: hedge what the underlying cannot (gamma, vega) with other options; vega by bucket; then costs (kept chart).
- Beats: **Visual**: a two-dimensional "Greek space" (gamma on x, vega on y); the book is an arrow; each available
  option is a basis arrow (short-dated: gamma-heavy; long-dated: vega-heavy); the hedge solves for the combination
  that brings the arrow to the origin, drawn as vectors adding tip to tail; then delta is zeroed with the
  underlying (a third axis collapsing). Then vega buckets (Taleb): a term-structure bar chart of the book's vega by
  expiry; a parallel hedge zeroes the total but not the buckets; a steepening move shows the leftover P&L. Then
  keep `band` (Whalley–Wilmott) and `frontier` (cost–risk chart), with the deep hedger now a **replay**: its
  training curve (variance + κ·cost) for three κ with 3 seeds as bands, then the dot landing on the chart; forward
  link to Part 17.
- Derivation:
  - $\begin{pmatrix}\Gamma_1&\Gamma_2\\ \mathcal V_1&\mathcal V_2\end{pmatrix}\begin{pmatrix}n_1\\n_2\end{pmatrix} =
    -\begin{pmatrix}\Gamma_B\\ \mathcal V_B\end{pmatrix}$, then $n_0 = -(\Delta_B + n_1\Delta_1 + n_2\Delta_2)$ (solve
    the 2×2, then delta with the stock).
  - Gamma/vega ratio: $\mathcal V/\Gamma = \sigma\tau S^2$ (ch1), so options of different τ are independent hedges.
  - Whalley–Wilmott band $\pm(\tfrac{3\lambda S\Gamma^2}{2\gamma})^{1/3}$ (kept; the problem set derives its scaling).
- Experiment: `hedging` (exists; add `loss` histories and 3 seeds → `hedging_replay`); `greekhedge` (new): a short
  30-day ATM straddle on 10,000 Heston paths (the House's `stochvol`), hedged (a) delta only, (b) delta + gamma
  with a 7-day option, (c) delta + gamma + vega with 7- and 60-day options; P&L sd with and without vol-of-vol.
  Expected: (b) removes most of the GBM error, (c) most of the Heston vega error (computed; branch).
- Lab 5: `quoting.ww_band` (quoting.py lines 96–101, 6 lines), run for 15 days at S = 90, 100, 110.
- Pause-and-predict: "You must kill your gamma but keep your vega. Buy short-dated or long-dated options?"
  (Short-dated buys gamma cheaply per unit of vega; sell long-dated to offset vega.)
- Compute: `hedging_replay` (3 κ × 3 seeds × ~1 min = 9 min), `greekhedge` (2 min).

### 11 · Expiry and pin risk (2.8) · item 6 · `s06_expiry` (kept: `pin`; `dispersion` moves to ch13)
- Goal: what gamma does in the last hours; the pinning mechanism; does BTC pin?
- Beats: **Visual (3D)**: the gamma surface Γ(S, τ) over the last day, a ridge at the strike that becomes a spike as
  τ → 0 (the existing day/hour/minute numbers, 0.15 → 5.8, read off it); delta as a step (kept curves). **Live
  (Avellaneda–Lipkin)**: a simulated stock with hedgers net long gamma at K; each step the hedgers sell above K and buy
  below K (their delta trades), the price impact nudging it back; 200 paths fan out and the terminal histogram grows
  a spike at K; flip the sign (net short gamma) and the histogram develops a hole at K. Then Ni–Pearson–Poteshman's
  finding (card) and the **BTC test**: Deribit settles at 08:00 UTC on the 30-minute TWAP of its index (Deribit
  support, verified); the distance of BTC from the nearest $1,000 strike at Friday 08:00 against all other hours,
  as two histograms filling.
- Derivation:
  - $\Gamma_{ATM} \approx \frac{1}{S\sigma\sqrt{2\pi\tau}}$ (ch1's formula at $d_1 \to 0$; the problem set).
  - Hedgers' net flow $= -\Gamma_{net}\,dS$ per unit move (re-hedging a long-gamma book sells into rises), so with
    linear impact $dS = \ldots - \kappa\,\Gamma_{net}\,dS$, i.e. the effective volatility near K is
    $\sigma/(1 + \kappa\Gamma_{net}(S,\tau))$ (Avellaneda–Lipkin's damped volatility), which → 0 at K as τ → 0.
  - Pin risk for a seller: assignment is a coin flip at $S_T \approx K$; the overnight exposure is a full unit of
    delta of unknown sign (Taleb).
- Experiment: `pin_sim` (new; 2,000 paths, two signs of Γ_net); `pin_btc` (new). **(probe)** 2021–2025 hourly closes:
  share within ±$100 of a $1,000 multiple 24.5% at Friday 08:00 (n = 261) vs 19.9% at all hours (z ≈ 1.9); mean
  distance 0.231 vs 0.246 of the spacing; monthly expiries (n = 60) 26.7%; Friday 07:00 control 19.2%. Suggestive,
  not conclusive: the narration says so (and that Binance's 08:00 close is a proxy for Deribit's TWAP; 1-minute data
  around 07:30–08:00 would be the right test, where cached).
- Pause-and-predict: "Market makers are net *short* gamma at a strike into expiry. Pin, or repel?" (Repel.)
- Compute: `pin_sim` (0.5), `pin_btc` (< 0.1).

### 12 · Early exercise, synthetics, and the dividend play (2.6) · item 6 · `s06b_early` (new)
- Goal: when an American option is worth more alive than dead; the one reason to exercise a call; the "trading
  game" around it.
- Beats: **Visual**: a binomial tree (`binomial_tree`) for a call on a stock paying a discrete dividend D at t_D:
  nodes light gold where exercise beats holding; all gold nodes sit on the layer just before t_D, deep in the money.
  Then the condition as two bars racing at each ITM node: the dividend D against the time value lost
  $K(1 - e^{-r(T-t_D)}) + P$. Card on synthetics (call − put = forward; conversions, reversals; Part 9 owns the box).
  Then **the dividend play** (Pool–Stoll–Whaley 2008; Hao–Kalay–Mayhew 2010): on the day before ex-date, holders
  who forget to exercise ITM calls leave value to the short side; traders who are short and long equal amounts of
  the same call (a wash) collect from the unexercised holders through random assignment. An animated assignment
  lottery: each short position drawn against the pool of exercises.
- Derivation:
  - $C^{Am} \ge S - K$ and, without dividends, $C^{Eu} \ge S - Ke^{-r\tau} > S - K$ ⇒ never exercise (Merton 1973).
  - Just before ex-date: exercise gives $S - K$; holding gives $\ge S - D - Ke^{-r(T-t)}$ ⇒ exercise only if
    $D > K(1 - e^{-r(T-t)}) + P(S-D, K, T-t)$ (put–call parity on the continuation value).
  - Dividend play: with exercised fraction $e$ of open interest $OI$ and the player's wash position $w$ (long $w$, short
    $w$), the player exercises its longs, and its shorts are assigned with probability $\approx (e\,OI + w)/(OI + w)$;
    its expected gain is $wD\,(1 - e)\,OI/(OI + w)$ (assignment is pro rata).
- Experiment: `early` (new): the tree (S = K = 100, D = 2 at 3 weeks before a 2-month expiry, r = 4%) with the
  exercise region; the condition swept over D and r; the dividend-play payoff over e and w. All illustrative, labelled.
- Pause-and-predict: "No dividends, deep in the money call. Exercise to lock in the gain?" (No: sell it, or sell
  stock against it.)
- Compute: `early` (< 0.1).

### 13 · Dispersion and implied correlation (3.0) · item 8 · `s06a_dispersion` (new; content from `s06_expiry.dispersion`)
- Goal: index variance from its parts; implied correlation measured from Cboe's index; the dispersion trade's P&L;
  why it is short a crash; the crowding of 2024–2025.
- Beats: **Visual (3D)**: the index-vol surface $\sigma_I(\rho, \bar\sigma)$ for an equal-weight 50-name index: a
  plane rising in ρ; a horizontal slice at the observed index vol cuts a curve, and the implied ρ is read off.
  **Live**: a correlation matrix heat map whose off-diagonal glows hotter as ρ rises, with the index vol bar rising
  beside it. Then the data: Cboe's 3-month implied correlation index (COR3M) daily 2006–2025 drawn against the
  realized industry correlation (kept series), the gap shaded as the correlation risk premium. Then the trade's P&L
  as two ledgers (short index vega, long member vega).
- Derivation:
  - $\sigma_I^2 = \sum_iw_i^2\sigma_i^2 + \sum_{i\neq j}w_iw_j\rho_{ij}\sigma_i\sigma_j$ (variance of a sum).
  - $\rho_{impl} = \frac{\sigma_I^2 - \sum w_i^2\sigma_i^2}{(\sum w_i\sigma_i)^2 - \sum w_i^2\sigma_i^2}$ (solve for a
    single ρ) (Lab 6).
  - Large N: $\rho_{impl} \approx \sigma_I^2/(\sum w_i\sigma_i)^2$ (the own-variance term vanishes as $1/N$).
  - Dispersion P&L (delta-hedged straddles, vega-weighted): $\approx \sum_i w_i\,\tfrac12\Gamma_iS_i^2(\sigma_{r,i}^2 -
    \sigma_{i,i}^2) - \tfrac12\Gamma_IS_I^2(\sigma_{r,I}^2 - \sigma_{i,I}^2)$, whose sign is driven by
    $\rho_{impl} - \rho_{real}$ (substitute the first line for both index variances).
- Experiment: `dispersion` (exists); `cor3m` (new, data: Cboe COR3M CSV, a new fetcher, frozen through 2025-12-31).
  **(probe of the raw file)** 5,225 days since January 2006, mean 40.9; peaks 90.8 (8 Dec 2011) and 90.3 (16 Mar
  2020); 2024's low 7.6 and 2025's 11.1 (record lows: dispersion's crowding years). Plus the premium: COR3M against
  the realized correlation of the 49 industries over the next 63 days *(requires daily industry returns: new
  `ken_french_industries_daily` fetcher; if not added, use the monthly 36-month realized series and say that the two
  are not like for like)*. Caveat on screen: Cboe recalculated the COR indices with a new method in 2022 and
  back-filled history *(verify on Cboe's methodology page)*; industries correlate more than single stocks.
- Lab 6: `quoting.implied_correlation` (quoting.py lines 76–81, 6 lines), run on a 3-name toy and on COR3M's peak day.
- Pause-and-predict: "Index implied vol 20%, every member 30%, many members. Implied correlation?" (≈ 0.44.)
- Compute: `cor3m` (< 0.1), `dispersion` (exists, 0.3).

### 14 · India's expiry-day boom, and what lottery tickets pay (3.0) · item 9 · `s07_india` (kept: `boom`; `case`, `toy` move to ch15)
- Goal: the facts of India's boom; what short-dated options return to their buyers, measured on another market.
- Beats: keep the three SEBI stats and the rules card (with figures checked: FY25 net losses ₹1,05,603 crore, 91% of
  individual traders lost — SEBI study of 7 July 2025; *the later revision to ≈ ₹1.12 lakh crore and FY26's ₹91,685
  crore were reported in 2026 — (verify) against SEBI before use*). **Visual (live)**: a day of short-dated OTM option
  tickets on Deribit: each ticket a small card that flips at expiry, 84% turning grey (worthless), a few paying many
  times their price, a running "premium paid vs paid back" bar. Then the theory: an OTM option's expected return
  under P when implied exceeds expected realized, and the skewness preference (lottery demand) that keeps buyers
  coming. Then SEBI's three measures as dials (fewer weeklies, bigger lots, extra margin) and what they are meant
  to do.
- Derivation:
  - $\mathbb E^P[\text{payoff}]/\text{price}$ for a short-dated OTM call (zero drift): the price is $C(\sigma_i)$, the
    expected payoff $C(\sigma_r)$ (the same formula at the realized vol).
  - For $k = \ln(K/S) > 0$ fixed and $\tau \to 0$: $C(\sigma) \approx \frac{S(\sigma\sqrt\tau)^3}{k^2\sqrt{2\pi}}
    e^{-k^2/(2\sigma^2\tau)}$ (Mills' ratio on $N(-d)$, twice), so the ratio is
    $\approx (\sigma_r/\sigma_i)^3\exp\!\big(-\tfrac{k^2}{2\tau}(\tfrac1{\sigma_r^2} - \tfrac1{\sigma_i^2})\big)$, which
    collapses as τ → 0 whenever $\sigma_i > \sigma_r$: short-dated OTM options magnify the premium (checked
    numerically against the exact ratio on screen).
- Experiment: `shortdated` (new, real Deribit trades). **(probe)** 242,517 trades in options expiring within 2 days
  (100 Wednesdays, 2024–2025; settlement proxied by Binance's 08:00 hourly close): taker-bought OTM options returned
  −18.8% of premium (premium-weighted), 84% expired worthless, 12% were profitable; under 24 hours: −18.5%, 85%,
  11%. Taker-*sold* OTM options would have returned −23.7% to a buyer (so takers who sell are not on the losing side
  either; the narration notes that Deribit's takers are not India's retail and the comparison is of mechanisms, not
  people).
- Pause-and-predict: "Nine in ten lose. Does that prove the options were overpriced?" (No: a lottery can be fair and
  still lose most of the time; the premium-weighted return answers that.)
- Compute: `shortdated` (1.5 min).

### 15 · Case file: SEBI's interim order against Jane Street (alleged) (2.8) · item 10 · `s07a_case` (new; `case` and `toy` from `s07_india`)
- Goal: what was alleged, the procedure since, and the mechanics, with every claim labelled.
- Beats: keep the crisis card (amount corrected to ₹4,843.57 crore, the figure in SEBI's order and its 14 July 2025
  press release) and the source line. Add the timeline of the record: April 2024 Jane Street sues Millennium and two
  former traders over an India options strategy (a hearing revealed the India link; the case settled, filed
  6 December 2024, terms undisclosed — Bloomberg Law; *verify on the docket*); 3 July 2025 interim order (four
  entities named: JSI Investments, JSI2 Investments, Jane Street Singapore, Jane Street Asia Trading); 14 July 2025
  SEBI confirms the escrow deposit and the firm resumes trading; the firm's appeal before the Securities Appellate
  Tribunal (reported September 2025); *(unverified: a single report that SAT reserved an order on a document
  request on 21 October 2026 — use only if confirmed on SAT's site)*. "No final finding at the time of writing." **Visual
  (3D)**: the toy model generalized: net P&L over (morning purchase Q, options position D) as a surface, the
  cash leg's loss a trough along Q and the options' gain a ramp along D; the region where the whole profits although
  the cash leg loses is lit. Then the regulator's lens: the ratio of options exposure to cash-market volume on
  expiry days, which SEBI's later surveillance measures target (intraday position limits; verify the circular).
- Derivation: the toy's three legs (kept), generalized: cash $= -\lambda Q^2$ (round trip with linear impact), options
  $= D\cdot 2\lambda Q$ (the index move the afternoon selling causes, times the options' delta exposure), so net $>0
  \iff D > Q/2$ (set the sum to zero) — "the options must be large relative to the trading".
- Experiment: `alleged` (exists) + `alleged_surface` (new; trivial). Labelled "illustration: invented numbers".
- Pause-and-predict: none (a case file); instead "What would you need to see to tell manipulation from hedging?"
  (Intent and pattern: the order's evidence; the course does not judge it.)
- Compute: < 0.1.

### 16 · Crisis file: when short volatility blows up (3.0) · `s07b_shortvol` (new)
- Goal: the part's own crisis: the premium of ch6 is a payment for exactly these days.
- Beats: **Live**: S&P 500 (French daily market index, cumulated) and the VIX (FRED `VIXCLS`) through February 2018
  and February–March 2020, drawn day by day; beside them two illustrative books ledgering live: (a) a short
  near-the-money put-spread book "hedged" with puts 10–25% out of the money, (b) the same with the hedges moved to
  30–50% out of the money. (b) earns more every quiet month and loses many times more in March 2020. Then the
  record, card by card: **LJM** (SEC complaint, 27 May 2021: a short-volatility strategy lost more than $1 billion, over
  80% of the funds, in two trading days in February 2018; the SEC alleged misleading statements about risk; the
  defendants contested — SEC press release 2021-89); **Allianz Global Investors U.S. (Structured Alpha)** (DOJ,
  May 2022: the unit pleaded guilty to securities fraud; with its parent agreed to pay more than $6 billion, including
  $3.2 billion restitution, a $2.3 billion penalty and $463 million forfeiture; the statement of facts says hedges
  promised at 10–25% out of the money were bought far deeper, averaging 30–50% from February 2018; the funds lost
  more than $7 billion in March 2020; the CIO later pleaded guilty); *Malachite Capital (March 2020 closure, as
  reported by Bloomberg) — (unverified), use only if a primary filing is found*.
- Derivation: a short put's loss in a gap $\approx -\Delta\,dS - \tfrac12\Gamma dS^2 - \mathcal V\,d\sigma$, with all
  three terms of the same sign in a crash (dS < 0, dσ > 0, Γ > 0 for the put held short); a put spread caps it at
  $K_1 - K_2$ only if the long strike is near enough (the hedge's moneyness is the whole risk).
- Experiment: `shortvol` (new): the two books priced with Black–Scholes at the VIX (labelled "illustrative: VIX used
  as every strike's vol; skew ignored, which flatters the deep hedge"), monthly rolls 2017–2020; cumulative P&L and
  the March 2020 drawdown of each (computed).
- Pause-and-predict: "Moving your tail hedge from 20% to 40% out of the money cuts its cost by how much, and its payoff
  in a 35% crash by how much?" (Computed on the chart.)
- Compute: `shortvol` (< 0.5).

### 17 · Industry: who makes options markets, and how (3.0) · `s05b_industry` (new; firm cards from `s05_mm`)
- Goal: the business from the public record: firms, flow, exchanges, rules.
- Beats (cards and live objects, sources on screen):
  1. Scale: OCC cleared 15.3 billion contracts in 2025 (including futures) against 4.8 billion in 2019 (OCC 2025
     annual report; 2024 performance highlights): a bar chart growing year by year.
  2. Who is on the other side of retail: Bryzgalova, Pavlova and Sikorskaya (2023): retail options trading has reached
     over 60% of US option volume by their measure; nearly 90% of options payment for order flow comes from three
     wholesalers, mostly Citadel Securities, Susquehanna and Wolverine; retail favours cheap short-dated options and
     loses on average at wide spreads. Muravyev–Pearson (2020): measured relative to fair value, trading costs are
     lower than quoted spreads suggest for sophisticated timers.
  3. The firms (kept and extended): SIG (1987; game theory and poker in training, from its job postings); Optiver and
     IMC (1986, 1989, Amsterdam floor); Jane Street (2000). **Optiver's CFTC case**: a 2008 complaint that its traders
     attempted to manipulate NYMEX crude, heating oil and gasoline settlement prices 19 times on 11 days in March 2007
     ("bully the market"); a 2012 court order of $14 million in penalties and disgorgement, the firm neither admitting
     nor denying (CFTC releases 5521-08 and 6239-12).
  4. How a desk actually quotes: a surface fitted every few milliseconds, quotes in vol shifted by inventory (ch9),
     Greek limits, auto-hedgers on futures (ch10), from firms' public descriptions and the market-making game used
     in interviews *(the implementer cites only what a firm has published; no internal claims)*.
  5. Exchange design that matters to traders: Deribit's TWAP settlement (ch11), NSE's expiry-day rules (ch14),
     Cboe's implied correlation index (ch13).
- Experiment: `industry_bars` (OCC annual volumes typed from the cited reports, labelled as published numbers).
- Pause-and-predict: "Why would a wholesaler pay a broker for your option orders?" (Your flow is uninformed on average:
  ch8's adverse selection runs the other way.)
- Compute: none.

### 18 · Frontier: learning to trade options (2023–2026) (2.8) · `s08a_frontier` (new)
- Goal: what machine learning now does on option desks and in the literature; one model fitted on screen, honestly.
- Beats: **Replay (hands-on core)**: a walk-forward predictor of BTC's four-week delta-hedged straddle P&L (ch6) from
  four features known at the trade: IV − HAR forecast, IV − trailing 30-day RV, the 25Δ RR and the 7d–60d term slope
  (all from Part 12's weekly grid and Binance): ridge and a depth-2 gradient-boosted tree (scikit-learn), refitted
  each week on the past only; the out-of-sample prediction line drawn week by week over the realized P&L, 5
  bootstrap resamplings of the training set as a band; the single-signal rule of ch7 as the baseline. Registered
  with the trial counter (+1). Narration branches: with 96 overlapping weeks, the honest expectation is "nothing
  survives"; say so if so, and say what Bali et al. had (12 million observations).
- Cards (verified this session):
  - Bali, Beckmeyer, Mörke, Weigert (2023), *RFS* 36(9): nonlinear ML on 265 option- and stock-based characteristics,
    12 million observations 1996–2020, profitable long–short delta-hedged equity option portfolios after costs;
    option-based characteristics strongest, stock-based ones add.
  - Cao, Chen, Farghadani, Hull, Poulos, Wang, Yuan (2023), *Frontiers in AI*: distributional RL for gamma and vega
    hedging with a second option under costs (ch10's problem, learned).
  - Baldacci, Bergault, Guéant (2021), *QF*: optimal market making in many options via a reduction to a few risk
    factors (ch9 at scale); arXiv 2307.01814 (2023): RL quotes across strikes and maturities *(authors verify)*.
  - Bryzgalova, Pavlova, Sikorskaya (2023), *JF*: retail options and the wholesalers (ch17).
  - Pointers, not repeated: 0DTE and dealer gamma (Part 12); deep hedging and learned bands (Part 17); option-implied
    machine-learned surfaces (Part 12).
- Pause-and-predict: "A model finds t = 3 after 40 tries. What is its deflated t?" (Part 26's lesson.)
- Compute: `frontier_ml` (≈ 3 min; scikit-learn; seeds for the bootstrap).

### O · The quoting engine, recap, desk questions, problems (3.0) · `s10_outro` (absorbs `s09_house`)
- The House card and the module table (kept from `s09_house`, extended with the new functions), Rule 11, the trial
  counter (73 + this part's registrations).
- Recap in 10 lines (one per item), payoff card (Parts 12, 13, 15, 17, 26, 36–38, 42), reference card (books; papers;
  frontier; industry and regulatory sources).
- Desk questions (README solutions): keep the straddle and the die; replace the third with **"Deep ITM American call,
  dividend tomorrow of 2, rates 4%, two months left, put worth 0.3. Exercise?"** (D = 2 > K(1 − e^{−rτ}) + P at
  K = 100: 0.66 + 0.3, so yes); keep the short-ATM-before-expiry question as a problem.
- Problem set (≈ 90 s): the existing 5, plus (6) "derive vanna and volga", (7) "show the dispersion P&L's sign is
  set by ρ_impl − ρ_real", (8) "derive the GLFT skew's sign from the HJB". README carries English and Chinese solutions.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 3.0 | 10 Hedging the book | 3.0 |
| 1 Greeks / P&L explain | 3.2 | 11 Expiry and pin | 2.8 |
| 2 Scalping | 3.0 | 12 Early exercise | 2.6 |
| 3 Hedge frequency | 2.8 | 13 Dispersion | 3.0 |
| 4 Second-order | 3.0 | 14 India | 3.0 |
| 5 Strategies | 3.2 | 15 Case file | 2.8 |
| 6 Premium | 2.8 | 16 Short-vol crises | 3.0 |
| 7 Edge and sizing | 3.0 | 17 Industry | 3.0 |
| 8 Spread / adverse selection | 3.0 | 18 Frontier | 2.8 |
| 9 Inventory / RL | 3.4 | Outro | 3.0 |
| | | **Total** | **≈ 59.2** |

(≈ 8,200 spoken words at 139 wpm. If the gate measures above 60, trim ch15 and ch17 first; the floor of 50 leaves
9 minutes of slack.)

---

## 3b. Hands-on summary

**Labs (`lab_card` ≤ 12 lines of real House code, then `lab_run` with cached output):**
1. ch1 `quoting.book_greeks` — `explainer/quant/house/quoting.py` lines 43–49 (7 lines); output: the five-leg book's
   cash delta, gamma per 1%, vega per point, theta per day.
2. ch2 `hedge.delta_hedge` accounting — `hedge.py` lines 74–79 (6 lines); output: gamma +6.4, theta −4.6, net +1.7.
3. ch8 `quoting.markouts` (new, ≤ 12 lines); output: edge 0.36, markouts 0.26 / 0.22 / 0.21 vol points.
4. ch9 `quoting.quote` — `quoting.py` lines 84–93 (10 lines); output: bid/ask at inventory −20, 0, +20.
5. ch10 `quoting.ww_band` — `quoting.py` lines 96–101 (6 lines); output: half-widths at 90/100/110.
6. ch13 `quoting.implied_correlation` — `quoting.py` lines 76–81 (6 lines); output: the toy and COR3M's peak.
(Line numbers as of 2 Nov 2026; re-read before excerpting, since other parts append to `quoting.py`.)

**Replays (every fit or training watched, seeds as bands, baselines at equal budget):** ch9 Q-learning market maker
(5 seeds; DP optimum, symmetric quotes and GLFT as baselines); ch10 deep hedger (3 κ × 3 seeds; Whalley–Wilmott band
as the classical benchmark; store the loss each 25 steps); ch18 walk-forward ridge/GBM (5 bootstrap resamplings;
single-signal rule baseline). Also ValueTracker-driven "fits": ch4 vanna–volga weights solved strike by strike as a
sweep; ch7 the Kelly curve as the fraction slides.

**Live simulations:** the May 2021 hedge with its ledger (hook, ch2); 2,000 path reorderings (ch2); three hedgers
racing (ch3); the value surface sinking with time (ch1); structures morphing and decaying (ch5); 96 weekly ledgers
(ch6); monthly edge bars (ch7); Glosten–Milgrom belief updating (ch8); the trained agent vs symmetric quotes (ch9);
the Greek-space hedge (ch10); Avellaneda–Lipkin pinning paths (ch11); the tree's exercise region and the
assignment lottery (ch12); the correlation matrix heating (ch13); lottery tickets flipping (ch14); the two short-vol
books through 2018 and 2020 (ch16).

**3D scenes** (`ThreeDScene`, `price_surface`, `add_fixed_in_frame_mobjects` for text): ch1 value surface (S, τ);
ch2 dollar-gamma landscape (S, t); ch4 vega surface (K, σ); ch5 P&L surface (spot move, vol move) morphing; ch11 gamma
spike (S, τ); ch13 σ_I(ρ, σ̄); ch15 toy net P&L (Q, D).

**Compute budget (seeded, one command `python -m videos.quant.quant11.compute`; ≈ 40 CPU-minutes of 120):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| scalp* | 0.1 | premium | 1.5 | pin_sim | 0.5 |
| edge*, envelope* | 1 | kelly | 0.1 | pin_btc | 0.1 |
| explain | 0.5 | flow (partial per day) | 3 | early | 0.1 |
| scalp_shuffle | 1 | mm* | 0.1 | dispersion*, cor3m | 0.4 |
| frequency | 4 | mm_learn (5 seeds) | 5 | shortdated | 1.5 |
| secondorder | 1 | hedging* | 3 | alleged*, alleged_surface | 0.1 |
| strategies | 1 | hedging_replay (9 runs) | 9 | shortvol | 0.5 |
| | | greekhedge | 2 | frontier_ml | 3 |

(* exists.) Long items use `CACHE.partial` (per day for `flow` and `shortdated`, per seed for `mm_learn` and
`hedging_replay`); torch with `set_num_threads(1)`. Register with the trial counter: `frontier_ml` (1); `mm_learn`
and `strategies` are descriptive (no registration); the counter goes 73 → 74 (+1 if the implementer adds a premium
test variant).

---

## 4. Industry and frontier: facts and sources

Checked this session (2 Nov 2026) by search or fetch:

| Fact | Source |
|---|---|
| SEBI interim order 3 Jul 2025; ₹4,843.57 crore; entities JSI Investments, JSI2 Investments, Jane Street Singapore, Jane Street Asia Trading; 14 Jul 2025 SEBI confirms the escrow deposit; firm allowed to resume | https://www.barandbench.com/news/sebi-bars-jane-street-group-from-indian-securities-markets ; https://moneylife.in/article/jane-street-deposits-rs4843-crore-in-escrow-not-allowed-to-trade-contrary-to-media-reports/77664.html (primary: SEBI order and press release on sebi.gov.in — fetch before screen) |
| Jane Street's SAT appeal (document request), Sept 2025 | https://moneylife.in/article/jane-street-questions-sebis-findings-demands-nsesebi-documents-in-sat-appeal-reports/78222.html ; SAT reserving an order 21 Oct 2026: *(unverified, single source)* https://lapaasvoice.com/sat-reserves-order-in-jane-street-case-as-firm-seeks-more-sebi-documents/ |
| Jane Street v. Millennium (S.D.N.Y., filed Apr 2024; India options strategy revealed at a hearing; settlement filed 6 Dec 2024; terms undisclosed) | https://news.bloomberglaw.com/ip-law/jane-street-millennium-settle-india-options-trade-secrets-case ; https://www.bloomberg.com/news/articles/2024-04-19/jane-street-s-secret-strategy-concerns-india-hearing-reveals *(docket to confirm)* |
| SEBI F&O study (7 Jul 2025): FY25 individual net losses ₹1,05,603 crore (+41%); 91% lost | https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html ; Lok Sabha answer https://eparlib.sansad.in/bitstream/123456789/3018034/1/AU2473_JmzTiN.pdf ; later figures (≈ ₹1.12 lakh crore revised; FY26 ₹91,685 crore) *(verify)* https://www.moneylife.in/article/retail-fo-traders-lose-91685-crore-in-fy2526-despite-sebi-curbs-average-loss-hits-117-lakh-govt/81318.html |
| AGI US guilty plea (May 2022): >$6 bn total incl. $3.2 bn restitution, $2.3 bn penalty, $463 m forfeiture; hedges promised 10–25% OTM bought 30–50% OTM from Feb 2018; >$7 bn loss in March 2020 | https://www.justice.gov/usao-sdny/press-release/file/1506871/download (statement of facts) ; https://www.justice.gov/usao-sdny/pr/allianz-global-investors-us-sentenced-connection-multibillion-dollar-fraud-scheme ; https://www.claimsjournal.com/news/national/2022/05/17/310504.htm |
| SEC v. LJM (27 May 2021): short-vol strategy, >$1 bn and >80% lost in two trading days, Feb 2018; allegations of misleading risk statements; parallel CFTC action | https://www.sec.gov/news/press-release/2021-89 ; https://www.sec.gov/litigation/litreleases/2021/lr25101.htm |
| CFTC v. Optiver: 2008 complaint (19 attempts, 11 days, March 2007, NYMEX energy settlements); 2012 order $14 m | https://www.cftc.gov/PressRoom/PressReleases/5521-08 ; https://www.cftc.gov/PressRoom/PressReleases/6239-12 |
| Deribit: 08:00 UTC expiry settles on a 30-minute TWAP of the index (07:30–08:00, 4-second snapshots) | https://support.deribit.com/hc/en-us/articles/29734325712413-Settlement |
| OCC: 15.3 bn contracts cleared in 2025 (incl. futures); 12.3 bn in 2024; 4.8 bn in 2019 | https://annualreport.theocc.com/ ; https://prd-web.theocc.com/getmedia/ef5ba92e-ea33-4d52-831a-dfed00b86199/OCC-ToolKit-PerfHighlights-2024-v2.pdf |
| Cboe COR3M/COR1M daily history 2006– (CSV) | https://cdn.cboe.com/api/global/us_indices/daily_prices/COR3M_History.csv (redirects to cdn-api.cboe.com; fetched; methodology *(verify)*) |
| Bali, Beckmeyer, Mörke, Weigert (2023) *RFS* 36(9):3548–3602 | https://www.wiwi.uni-muenster.de/fcm/en/publication/98329575 (doi 10.1093/rfs/hhad017) |
| Bryzgalova, Pavlova, Sikorskaya (2023) *JF* 78(6):3465–3514 | https://lbsresearch.london.edu/id/eprint/2827 |
| Cao et al. (2023) gamma and vega hedging with distributional RL, *Frontiers in AI* | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9992725/ ; arXiv 2205.05614 |
| RL option market making (2023) | https://arxiv.org/abs/2307.01814 *(authors and venue: verify)* |

Unverified (keep the marks or drop): Natenberg/Sinclair/Taleb/Bennett chapter numbers; Coval–Shumway's "about 3% a
week"; Pool–Stoll–Whaley, Hao–Kalay–Mayhew and Golez–Jackwerth venue details; Cboe's 2022 COR methodology change;
Malachite Capital; SAT's 21 Oct 2026 step; SEBI's post-2025 surveillance measures named in ch15; SIG/Optiver/IMC
founding years (on screen already; re-check against the firms' own pages).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 11 · Trading Options (~57; the practitioner's part)
1. How an options trader thinks: the book as one Taylor series, each Greek derived; P&L as gamma against theta; a
   real next-day P&L explain on the Surface.
2. Gamma scalping on a real path, its order effect (the same returns reshuffled), and how often to hedge (hourly,
   daily, on moves) across every month of 2021–2025.
3. Vega, vanna, volga derived; the risk reversal and butterfly as their prices; the vanna–volga smile rebuilt from
   three quotes.
4. Strategies: straddles, strangles, spreads, calendars, risk reversals, butterflies; what each bets on, and what each
   paid on two years of real smiles.
5. Volatility trading: the premium in option returns (Coval–Shumway; Bakshi–Kapadia), a forecaster's edge tested out
   of sample (Sinclair; Goyal–Saretto), and how much to bet when the tail is fat.
6. Expiry: gamma at the strike, pin risk, the pinning mechanism (Avellaneda–Lipkin) and a test on Bitcoin; early
   exercise, synthetics and the dividend play.
7. The options market maker: the spread from adverse selection (Glosten–Milgrom) measured on Deribit's trades;
   inventory and the optimal quote (Avellaneda–Stoikov, GLFT, Stoikov–Sağlam); hedging the book's gamma and vega with
   other options, and under costs.
8. Dispersion: index against component volatility, implied correlation (Cboe COR3M) against realized, the
   correlation risk premium.
9. The India expiry-day boom: weekly index options, retail losses, SEBI's 2024 measures; what short-dated options
   return to their buyers.
10. Case file: SEBI's interim order against Jane Street (July 2025), *alleged* expiry-day index manipulation,
    contested by the firm; the mechanics alleged, as a toy model.

*Textbooks:* Natenberg *Option Volatility and Pricing*; Sinclair *Volatility Trading* and *Positional Option
Trading*; Taleb *Dynamic Hedging*; Bennett *Trading Volatility*; Hull OFOD (strategies, Greeks).
*Trained:* a reinforcement-learning options market maker (Q-learning, 5 seeds) against the exact dynamic program and
the GLFT formula; the learned hedger (replayed; Part 17 goes further); a walk-forward predictor of hedged option P&L.
*Computed:* P&L explain on the Surface; scalping and its reshuffles; hedge frequency on 244 BTC windows; vanna–volga
on the Surface; 96 weeks of structures on real smiles; delta-hedged gains; Deribit maker edge and markouts; pinning
on BTC; COR3M against realized correlation; short-dated option returns on Deribit; short-vol books through 2018 and
2020.
*Visuals:* the value surface sinking by theta; the dollar-gamma landscape with the crash on it; P&L surfaces morphing
across structures; the vega surface with vanna and volga; Glosten–Milgrom beliefs; the policy map learning; Greek
space; the gamma spike and pinning paths; the index-vol surface over correlation.
*Labs:* `book_greeks`, `delta_hedge`, `markouts`, `quote`, `ww_band`, `implied_correlation`.
*Crisis:* short volatility blown up: LJM (February 2018) and Allianz Structured Alpha (March 2020), from the SEC's and
DOJ's records.
*Firms:* SIG, Optiver (and its CFTC case), IMC, Jane Street, Citadel Securities and the PFOF wholesalers.
*Industry:* OCC volumes; retail flow and PFOF (Bryzgalova–Pavlova–Sikorskaya 2023); Deribit's settlement design.
*Frontier:* machine-learned option returns (Bali et al. 2023); RL for gamma–vega hedging (Cao et al. 2023) and for
option market making (Baldacci–Bergault–Guéant 2021 and successors).
*Desk:* the market-making game ("make a market on a die roll; now I tell you it's even"); "Long a straddle, the
stock doesn't move. How do you lose money?"; "Deep ITM American call, dividend tomorrow: exercise?"
*House:* the options quoting engine.
```

---

## 6. Implementation notes

**Minutes** — §3 table, ≈ 59 min; floor 50, ceiling 60.

**Probe result for ch3 (hedge frequency):** written into ch3 (means −2.86/−2.69/−2.59/−2.88, sds 3.51/3.81/4.27/3.75,
variance ratio 0.978). The probe took ≈ 6 CPU-min single-threaded (bs.greeks per step on one path at a time);
vectorize across windows in `compute.py` (all 244 paths as one array) to bring it under 1 min.

**New House functions** (append to `explainer/quant/house/quoting.py` unless noted; one test each in
`tests/test_quant_house.py`):
- `pnl_explain(legs, S0, S1, sig0, sig1, dt)` → dict of Greek terms + actual + unexplained. Test: for a tiny move the
  unexplained term is O(move³).
- `delta_strike(F, T, iv_fn, delta, cp)` → strike with Black delta = target on a smile (bisection). Test: flat smile
  matches the closed form $K = F e^{-\sigma\sqrt T N^{-1}(\Delta) + \sigma^2T/2}$.
- `vanna_volga(K, F, T, strikes3, vols3, atm_vol)` → VV implied vol. Test: returns the market vols at the three pillar
  strikes exactly.
- `markouts(ts, sign, price, mark, index, delta, vega, horizons)` → edge and delta-hedged markouts in vol points.
  Test: a synthetic tape with a known permanent impact recovers it.
- `mm_value_iteration(...)`, `mm_q_learning(..., seed, checkpoints)` and `glft_quotes(q, A, k, sigma, gamma)`. Tests:
  DP skew antisymmetric in q; Q-learning on a 3-state toy converges to DP; GLFT skew sign.
- `greek_hedge(book_greeks, instruments_greeks)` → quantities zeroing (Γ, V) then Δ. Test: residual Greeks ≈ 0.
- `hedge.delta_hedge_on_moves(t, S, K, T, sigma, band, ...)` (append to `hedge.py`). Test: band → 0 equals hourly.
- `pin_simulation(n_paths, gamma_net, impact, seed)` (append to `sim.py`). Test: Γ_net = 0 reproduces GBM's
  terminal variance.
- `american_call_dividend(S, K, T, r, sigma, D, tD, n)` (append to `trees.py`) → price and exercise mask. Test: D = 0
  equals the European price.
- `implied_correlation` exists; `dispersion_pnl(...)` optional.

**Data (through `explainer/quant/data.py`):** all cached already except (1) Cboe `COR3M` daily — add
`cboe_index(symbol, through="2025-12-31")` (CSV via cdn.cboe.com, follows a 307 redirect to cdn-api.cboe.com; frozen
and checksummed like `fred`); (2) optional `ken_french_industries_daily(49)` for the next-63-day realized correlation.
Reused: Deribit trades of 100 Wednesdays (2024-01-03 … 2025-11-26, 00–12 UTC) and the two Surface days; DVOL and
Binance 1h; Part 12's `history` grid via `videos.quant.quant12.compute.load("history")` (declare the dependency, as
`edge` does with Part 10); FRED `VIXCLS`; French daily market; Part 10's `btc` via its `load`.

**Modules:** keep `s01_hook`, `s02_greeks`, `s03_scalp`, `s04_vrp`, `s05_mm`, `s06_expiry`, `s07_india`,
`s08_hedging`, `s10_outro` (classes `Hook`, `Greeks`, `Scalp`, `VRP`, `MarketMaker`, `Expiry`, `India`, `Hedging`,
`Outro`). New: `s03a_frequency`, `s03b_secondorder`, `s03c_strategies`, `s04a_premium`, `s05a_inventory`,
`s05b_industry`, `s06a_dispersion`, `s06b_early`, `s07a_case`, `s07b_shortvol`, `s08a_frontier`. `s09_house` leaves
the manifest (its content goes to the outro). Manifest order is §3's order; chapter-card numbers must match it
(note the module names do not: `s04a_premium` is chapter 6 and `s04_vrp` chapter 7; `s08_hedging` is chapter 10).
Recompute `mm`, `hedging`, `dispersion` only if their parameters change (their keys stay).

**Narration branches** (compute verdicts, never typed): the explain residual share (ch1); the reshuffle percentile
(ch2); the frequency ranking and the variance ratio (ch3); VV RMSE (ch4); every structure's t (ch5); the hedged
straddle t (ch6); f*_empirical vs f*_Gauss (ch7); markout share retained (ch8); Q-learning % of optimum (ch9); the
Heston vega-hedge gain (ch10); the BTC pinning z (ch11); COR3M vs realized gap sign (ch13); the frontier model vs the
single-signal rule (ch18).

**Chinese:** new terms for `QUANT_ZH_GUIDE.md`: 损益归因 (P&L explain), 方差比 (variance ratio), 瓦纳/沃尔加 → use
vanna/volga as 凡纳 (vanna)、沃尔加 (volga) *(check the guide's existing choice)*, 风险逆转 (risk reversal), 蝶式价差
(butterfly), 逆向选择 (adverse selection), 盯市结果/事后收益 (markout), 库存风险 (inventory risk), 钉住风险 (pin risk),
股息套利/股息博弈 (dividend play), 离散度交易 (dispersion), 隐含相关性 (implied correlation), 订单流付费 (PFOF).

**Risks.**
- Part 12's `history` cache must exist (it does); if Part 12's expansion renames that item, `strategies`,
  `premium`, `secondorder` and `frontier_ml` break: coordinate (the lead should freeze the item name).
- Part 10 and Part 12 are being expanded in parallel; if their plans add a P&L explain, hedge-frequency or
  Coval–Shumway chapter, the lead decides which part keeps it (this plan's boundaries are in the header).
- `flow` uses Deribit's mark price as fair value; markouts need a later print on the same instrument (78–88%
  coverage); say both on screen.
- The BTC pinning result is marginal (z ≈ 1.9); it must be narrated as suggestive, and may flip with the TWAP-based
  test.
- Short-dated "buyer returns" use Binance's 08:00 hourly close as the settlement proxy; a 1-minute TWAP is better
  where Binance 1m data is cached (it is only partly).
- Case-file facts change: re-check SEBI and SAT before rendering; never state an outcome that has not happened.
- `shortvol` prices every strike at the VIX (no skew): label it illustrative; it understates the cost of near hedges.
- The Q-learning agent is tabular on a small MDP: call it what it is ("the simplest learner that can find the
  answer"), with the DP as ground truth; Part 17 has the deep version of hedging.

## 7. Lead's decisions (2 Nov 2026)

1. Boundaries accepted: Part 10 keeps the P&L derivation, discrete hedging and Leland; Part 12 keeps the variance-swap premium, 0DTE, dealer gamma and Volmageddon (XIV/SVXY/VIX futures); Part 17 keeps deep hedging and learned bands. Part 11's learned hedger stays only as a short replay with a forward link.
2. Part 12's compute item `history` keeps its name and structure (the Part 12 implementer has been told). Read it with Part 12's cache; if a Part 12 item is missing when you run, wait or compute on what exists and note it.
3. Yes: `cboe_index(...)` in `explainer/quant/data.py` (append-only), frozen through 2025-12-31, with a manifest entry and checksum. The 49-industry daily fetcher only if a chapter really needs it.
4. Accepted: keep module names for cache validity; the manifest sets the order.
5. Yes: LJM (2018) and Allianz Structured Alpha (2020) are Part 11's crisis file; Part 12 points here.
Also: correct READING.md to "Jane Street v. Millennium" (settled December 2024) after checking the docket; verify or drop Coval–Shumway's figure, venues, COR3M methodology change, Malachite, the tribunal report, and the arXiv authors.
