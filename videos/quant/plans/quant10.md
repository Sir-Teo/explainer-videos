# Part 10 · Black–Scholes–Merton: expansion plan (45.6 → ~57 min, rendered)

Planning document only; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 (the
November 2026 standard) and §6 Parts 1, 8–17; `READING.md` §1–3 and §4 Parts 9–12; `videos/ai/LECTURE_GUIDE.md`;
`videos/quant/plans/IMPLEMENT.md`, `RESEARCH.md`, `quant5.md` (format) and the neighbours' plans `quant8.md`, `quant9.md`,
`quant11.md` (with its lead's decisions), `quant12.md`, `quant16.md`; every file in `videos/quant/quant10/` (manifest,
common, compute, the 15 scenes, README; narration extracted with an AST script); the cached results in `.cache/quant10/`;
the House modules `bs.py`, `hedge.py`, `paths.py`, `trees.py`, `surface.py`, `sim.py` (`merton_jumps`), `control.py`
(`perpetual_put`); `explainer/quant/{__init__,viz,data}.py` (`lab_card`, `lab_run`, `TrainingReplay`, `seed_band`,
`HedgeLedger`, `binomial_tree`, `price_surface`, the timeline). Probe scripts (not in the repo):
`/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/q10/probe/p1.py … p3.py`
(about 3 CPU-minutes in all, one thread, `nice 10`). Numbers marked **(probe)** were computed this session on the
cached data or seeded simulations; `compute.py` must recompute them and the narration follows what comes back.

**Part 10 is already long; the job is the standard, not minutes.** It is the series' pilot: 15 scenes, 45.6 min,
every chapter about 3 minutes, real experiments throughout. What it lacks is what the November 2026 standard added:
**no lab** (no House code on screen), **no replay** with seeds as bands, only two 3D scenes, **no industry and no
frontier chapter**, syllabus item 9 (dividends, borrow, the forward) **absent**, item 7 (inversion) and item 12 (the
first row) squeezed into one chapter, derivations that stop at the PDE (the PDE is never solved; the tree's limit, the
American free boundary, Leland and EKJS are stated, not derived), and several listed papers never on screen
(Brennan–Schwartz, Rubinstein–Leland, Barone-Adesi–Whaley, Kim, Carr–Jarrow–Myneni, Derman–Taleb, Haug–Taleb, MacKenzie–Millo).

**Boundaries (decided with the neighbours' plans; do not repeat them).**
- Part 10 keeps the P&L derivation, wrong-vol hedging, discrete hedging and Leland (Part 11 plan, lead's decision 1).
  Part 11 owns the *trade*: P&L explain, gamma scalping, hedge frequency **on BTC** (its ch3, including move-triggered
  hedging), the dividend play and synthetics (its ch12). Part 10 does the theory of hedge frequency on GBM and with
  jumps, and points to Part 11 for the data.
- Part 9 owns parity, the one-step tree as geometry, CRR with its convergence sawtooth (its ch6), Girsanov re-weighting
  with effective sample size (its ch9), and change of numeraire with N(d₁)/N(d₂) as two probabilities (its ch11), and
  computed Deribit's implied basis (its hook). Part 10 keeps short versions where BSM needs them and **adds what Part 9
  does not: the tree→PDE limit in 3D, the PDE solved by the heat kernel, the carry as an input to the formula.**
- Part 8 owns optimal stopping, the perpetual put and smooth fit (its ch12, `control.perpetual_put`). Part 10's American
  chapter is the *finite-maturity* put: the free boundary from the tree, the early-exercise premium (Kim; Carr–Jarrow–
  Myneni), Barone-Adesi–Whaley, the dividend call; one line recalls smooth fit.
- Part 16 owns numerical methods (FD/PSOR/LCP with the American value surface in 3D, LSM, Leisen–Reimer, MLMC). Part 10's
  3D American object is the **premium** surface P_A − P_E from the tree, not the value surface by PSOR.
- Part 12 owns the surface (smile shape and dynamics, sticky rules, SVI, Dupire, variance swaps, VIX). Part 10 inverts
  implied volatility, shows the first smile and fills the Surface's first row.
- Part 1 already measures 19 October 1987 in sigmas and with a cubic tail (its crisis file). Part 10's 1987 chapter
  shortens the tails block to one line and adds what is Part 10's own: **portfolio insurance replayed on the 1987 data**.
- LTCM thread (SYLLABUS §3): 8 leverage → **10 Merton and Scholes** → 18 Salomon → 41 the 1998 story. Part 10 tells the
  option-theoretic side (selling volatility, what every hedge assumes) and leaves the margin spiral to 41.
- Part 17 owns Hutchinson–Lo–Poggio, neural pricers, deep hedging and learned bands; Part 5 owns CME's switch to
  Bachelier and the stop-loss start-gain paradox (one-line pointers here).

---

## 0. The length arithmetic (read first; decision 1 for the lead)

`tools/lecture_length.py` estimates unrendered scenes at **140 words a minute**, but Part 10's *rendered* chapters run at
**169 counted words a minute** (7,712 counted words in 45.6 rendered minutes; per chapter 146–182). A plan written at 140
wpm (≈ 8,000 words) would render at about 47 minutes and fail the floor. So:

- **Target about 9,600 counted words** (21 scenes, 380–560 words each) → about **57 rendered minutes**.
- Before rendering, the tool will *estimate* about 68 minutes for this text. The implementer must not cut to bring the
  estimate under 60; the rendered figure is what counts. (Alternatively the lead lets the implementer pass
  `--wpm 169` if the tool grows that option; nothing in this plan depends on it.)
- `measured()` takes the latest `.narration.json` for a module, so after edits a kept scene still reports its **old**
  rendered length until the lead re-renders it. The implementer should read the word counts, not the minutes, for kept
  scenes.

---

## 1. Current state (`python tools/lecture_length.py quant10`: 45.6 min rendered, 7,712 counted words)

| # | Scene | Min · words | What it covers, and how deep | Missing against the standard |
|---|---|---|---|---|
| — | `s01_hook` Hook | 3.2 · 582 | Oct 2021 BTC call sold at DVOL 88.5%, BTC +37%, unhedged −27, hedged +1.15 (the median of 1,706 months); objectives; House opens the vol desk | pause-and-predict; fine otherwise |
| 1 | `s02_history` History | 3.8 · 613 | Bachelier; Sprenkle, Boness, Samuelson with μ and ρ unknown; Thorp–Kassouf's hedge picture; Black–Scholes via CAPM; Merton; CBOE 26 Apr 1973; MacKenzie; Nobel | the TI calculator and Black's sheets (syllabus item 1); 911 contracts; facts unverified (Thorp 1969, journal rejections) |
| 2 | `s03_replication` Replication | 3.3 · 562 | Itô, Π = V − ΔS, μ drops out, no-arbitrage, the PDE; heat picture in 2D | self-financing done properly (Shreve 4.5); the PDE never solved; no lab |
| 3 | `s04_riskneutral` RiskNeutral | 3.6 · 616 | FK; P vs Q fans (19.74 vs 12.36 ± 0.03 vs formula 12.34); Girsanov weights (12.36); the integral split; N(d₂) as Q-probability (0.530 vs simulated 53.1%, P 68.3%) | MC convergence as a replay with seeds; overlaps Part 9's Girsanov and numeraire chapters |
| 4 | `s05_tree` Tree | 2.8 · 511 | one step 120/90; 4-step tree; N = 1…400 sawtooth (10.4456 vs 10.4506) | **the syllabus visual "the tree converging to the PDE in 3D"**; the limit derived; overlaps Part 9 ch6 |
| 5 | `s06_greeks` Greeks (3D) | 3.1 · 552 | value surface V(S, τ); Δ, Γ live as τ shrinks; Θ = −½σ²S²Γ computed; vega = στS²Γ | Greeks derived (the Sφ(d₁) = Ke^{−rT}φ(d₂) identity); r ≠ 0 form |
| 6 | `s07_ledger` Ledger | 3.4 · 596 | d(book) = ½ΓS²(σᵢ² − σᵣ²)dt ladder; breakeven band ±σᵢ√dt; HedgeLedger on three paths; 20,000-path distributions | **lab** (the House's hedger); the best scene of the part, keep |
| 7 | `s08_wrongvol` WrongVol | 2.6 · 439 | EKJS integral stated; two paths same RV, 2.12 vs 0.25; Heston 4,000 paths: P&L against RV corr −0.87, against the gamma-weighted formula 0.99 | EKJS **proved**; hedge at implied vs at actual (Ahmad–Wilmott); 3D dollar-gamma |
| 8 | `s09_discrete` Discrete | 2.7 · 485 | error ∝ √Δt derived and measured (slope −0.486), Derman–Kamal rule; Leland weekly: −0.53 → −0.25 → +0.01 without end costs | split: jumps floor (Derman–Taleb), seeds; Leland derived; Kabanov–Safarian; cost–risk surface |
| 9 | `s10_implied` Implied (3D) | 3.4 · 548 | one quote inverted (43.66%); smiles of 10 Dec 2025; 3D Surface; first row: 4.36 in, 4.74 out, 0 calendar violations; DVOL 45.9 vs ATM30 44.1 | items 7 and 12 in one chapter; Jäckel only named; no lab, no replay over the whole Surface |
| 10 | `s11_american` American | 2.6 · 437 | Merton's no-early-exercise; American put 6.0900 vs 5.5735 on a 2,000-step tree; the boundary | free boundary conditions; Kim / CJM premium; BAW; Brennan–Schwartz; dividends |
| 11 | `s12_btc` BTC | 3.3 · 585 | 1,706 thirty-day calls sold at DVOL Apr 2021–Dec 2025, hourly hedge: mean +1.35, 81% win, ρ with IV−RV; costs 1.20; 57 non-overlapping months 1.42 ± 0.22; worst month Jul–Aug 2024 −3.34 | replay through time with a bootstrap band; inverse-option note |
| 12 | `s13_crash` Crash | 3.0 · 472 | portfolio insurance; −17.4% in French's data, −20.7σ, 10⁹² years vs 60 years (α = 2.71); the skew; MacKenzie | **the sigma count duplicates Part 1's crisis file**; insurance never simulated; Brady figures |
| 13 | `s14_ltcm` LTCM | 1.8 · 263 | Nobel; LTCM trades, leverage, Russia, $4.5bn loss, 14 banks, $3.6bn | short (1.8 min); no computed piece |
| — | `s15_outro` Outro | 3.0 · 451 | recap 8 lines; 3 desk questions; 5 problems; payoffs; references; House | recap for 19 chapters; 2 more problems |

What is computed now (`compute.py`, about 8 CPU-min): `tree`, `riskneutral`, `ledger`, `wrong_vol`, `discrete`,
`implied`, `btc`, `crash87`. All stay, with their names.

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item | Now | Plan |
|---|---|---|
| 1 History (1973; CBOE; Thorp; the TI calculator) | ch1 | ch1 (deepened: Black's sheets, the calculator, first-day volume) and ch18 (industry) |
| 2 Three derivations | ch2–4 | ch2 replication (self-financing), **ch3 the PDE solved (heat kernel, 3D)**, ch4 expectation, ch5 tree→PDE in 3D |
| 3 Greeks as geometry; Θ = −½Γσ²S² | ch5 | ch6 (derived, r ≠ 0 identity) |
| 4 Hedging P&L derived and watched | ch6 | ch7 (+ lab 2) |
| 5 Wrong volatility (EKJS 1998) | ch7 | ch8 (proved; Ahmad–Wilmott; 3D dollar gamma) |
| 6 Discrete hedging; Leland | ch8 | **two chapters**: ch9 discrete error (with jumps: Derman–Taleb), ch10 Leland (derived, Kabanov–Safarian, 3D cost–risk surface) |
| 7 Implied vol by inversion (Jäckel) | ch9 part | **ch11 of its own** (lab 3, replay over 254 quotes, the normalized price surface in 3D) |
| 8 American; free boundary | ch10 | ch14 (premium surface, Kim/CJM, BAW, the dividend call) |
| 9 Dividends, borrow and the forward | **absent** | **ch13 (new)**: Merton's yield, Black-76, Garman–Kohlhagen, inverse options, the forgotten forward on the Surface |
| 10 1987, portfolio insurance, the skew, performativity | ch12 | ch16 (insurance replayed on the 1987 data; Brady's numbers; the skew; MacKenzie) |
| 11 Nobel, then LTCM | ch13 | ch17 (option-theoretic side; VIX 1998 computed) |
| 12 The Surface's first row | ch9 part | ch12 (with the first smile) |
| — Industry chapter | absent | **ch18** |
| — Frontier chapter | absent | **ch19** (with the minimum-variance delta replay) |

### (b) Textbook sections → chapter

Chapter and section numbers from memory of the editions named in READING.md; *(verify)* marks need a check against the
publisher's table of contents in Phase 0.

| Book · section | Chapter / elsewhere |
|---|---|
| Hull OFOD 13 binomial trees (one step, risk-neutral valuation, two steps, American, delta, u and d from σ) | ch5 (limit); one step and CRR → Part 9; numerics → Part 16 *(verify 11th-ed. numbering)* |
| Hull 14 Wiener processes and Itô's lemma | Part 5 (ch2 recalls Itô in one line) |
| Hull 15 BSM: lognormal property, expected return, volatility estimate, idea of the derivation, the PDE, risk-neutral valuation, the formulas, warrants, implied volatility, dividends | ch2–4; implied → ch11–12; dividends → ch13; warrants/ESOs → Part 3 *(verify)* |
| Hull 17 options on indices and currencies; 18 futures options and Black's model | ch13 (Merton's q, Garman–Kohlhagen, Black-76); FX detail → Part 22 *(verify)* |
| Hull 19 the Greek letters: naked/covered, stop-loss, delta, theta, gamma, the Δ–Θ–Γ relation, vega, rho, realities of hedging, portfolio insurance | ch6, ch7; stop-loss → Part 5 (its hook); portfolio insurance → ch16; hedging in practice → ch18 and Part 11 *(verify)* |
| Hull 20 volatility smiles (put–call parity argument, the post-1987 skew) | ch12 (first look), ch16 (birth of the skew); the rest → Part 12 |
| Shreve II 4.5 the BSM equation (portfolio value, option value, equating, solution, Greeks, parity) | ch2, ch3, ch6 |
| Shreve II 5.2 risk-neutral measure and the BSM formula by Girsanov; 5.3 martingale representation | ch4; representation → Part 5; Girsanov in full → Parts 5, 9 |
| Shreve II 5.5 dividend-paying stocks (continuous, lump); 5.6 forwards and futures | ch13 |
| Shreve II 8.3 perpetual put; 8.4 finite-expiration put (analytic and probabilistic characterization); 8.5 American calls | ch14 (8.4, 8.5); 8.3 → Part 8 |
| Shreve I.4 American derivative securities | Part 8 (Snell), ch14 recalls |
| Björk 7 arbitrage pricing (the BS model, the PDE, risk-neutral valuation, the formula) | ch2–4 *(verify 4th-ed. numbering)* |
| Björk 8 completeness and hedging | ch7 (the replicating portfolio is the hedge) |
| Björk 9/10 parity relations and delta hedging (the "Greeks" chapter) | ch6, ch7 *(verify)* |
| Björk dividends; forwards and futures; currency derivatives chapters | ch13 *(verify numbering)* |
| Wilmott PWOQF 5 the BS model; 6 PDEs (the heat-equation transformation); 7 formulae and Greeks; 8 simple generalizations (dividends, time-dependent σ, r) | ch2, **ch3**, ch6, ch13 *(verify)* |
| Wilmott PWOQF 9 early exercise and American options | ch14 |
| Wilmott PWOQF "How to delta hedge" (hedging with implied vs actual vol; Ahmad–Wilmott) | ch8 *(verify chapter)* |
| Wilmott PWOQF "Discrete hedging"; "Transaction costs" (Leland, Hoggard–Whalley–Wilmott, Whalley–Wilmott) | ch9, ch10; bands → Parts 11, 17 *(verify chapters)* |
| Joshi *Concepts* 5 Itô calculus; 6 risk neutrality and martingale measures | ch2–4 *(verify)* |
| Joshi *Concepts* 7 the practical pricing of a European option (Greeks, implied vol, hedging error) | ch6–9, ch11 *(verify)* |
| Joshi *Concepts* 12 options with discretionary choice (American) | ch14; numerics → Part 16 *(verify)* |
| Taleb *Dynamic Hedging*: delta, gamma and shadow gamma, theta and carry, vega and the surface, the hedging error | ch6–10, ch18; the surface → Part 12 *(verify chapter layout)* |
| Baxter–Rennie 3 continuous processes, the BS model by martingales; 4 dividends, FX, quantos | ch4, ch13; quantos → Part 22 |

Nothing core is dropped: everything not in Part 10 is in Parts 3, 5, 8, 9, 11, 12, 16, 17 or 22, as marked.

### (c) Papers on the Part 10 list in READING.md → where they appear

| Paper | Now | Plan |
|---|---|---|
| Sprenkle 1961; Boness 1964 | on screen (ch1) | ch1 (kept) |
| Black–Scholes 1973 (*JPE*); Merton 1973 (*Bell J*) | on screen | ch1–4; Merton's dividend yield ch13; Merton's no-early-exercise ch14 |
| Black 1976 (*JFE*) | **absent** | ch13 card (Black-76 is the market's formula for futures options and Deribit) |
| Brennan–Schwartz 1977 (*JF*) | **absent** | ch14 card (the first finite-difference American put; solved in Part 16) |
| Boyle–Emanuel 1980 (*JFE*) | narration | ch9 card |
| Rubinstein–Leland 1981 (*FAJ*) | **absent** | ch16 lab (replicating a put with stock and cash) |
| Leland 1985 (*JF*) | on screen | ch10 derived |
| Barone-Adesi–Whaley 1987 (*JF*) | **absent** | ch14 computed against the tree |
| Brady Commission 1988 | narration ($60–90bn) | ch16 card with verified quotes (p. 29 of the report) |
| Kim 1990 (*RFS*); Carr–Jarrow–Myneni 1992 (*Math. Finance*) | **absent** | ch14: the early-exercise premium integral, computed from the tree's boundary |
| El Karoui–Jeanblanc–Shreve 1998 (*Math. Finance*) | on screen | ch8 proved |
| MacKenzie–Millo 2003 (*AJS* 109(1):107–145) | named | ch1, ch16, ch18 |
| Derman–Taleb 2005 (*QF*) | **absent** | ch9: the jump floor under the hedging error, computed |
| Haug–Taleb 2011 (*JEBO* 77(2):97–106) | **absent** | ch18 card, with the counter-view |
| Jäckel 2015 (*Wilmott* 2015(75):40–53) | named | ch11 card and the solver race |

**Proposed additions to READING.md Part 10** (classic): Bachelier (1900); Samuelson (1965) "Rational theory of warrant
pricing" *IMR*; Thorp–Kassouf (1967) *Beat the Market*; McKean (1965) *IMR* (pointer to Part 8); Garman–Kohlhagen (1983)
*JIMF*; Roll (1977), Geske (1979), Whaley (1981) (the American call with a dividend, *JFE*; the dividend play itself is
Part 11's); Jacka (1991) *Math. Finance*; Brenner–Subrahmanyam (1988) *FAJ*; Corrado–Miller (1996) *JBF*; Soner–Shreve–
Cvitanić (1995) "There is no nontrivial hedging portfolio for option pricing with transaction costs" *AAP*; Kabanov–
Safarian (1997) *Finance and Stochastics* 1(3):239–250; Derman–Kamal (1998/99) "When you cannot hedge continuously: the
corrections to Black–Scholes", Goldman Sachs QS note (verified, √(π/4) prefactor); Diener–Diener (2004) *Math. Finance*
(the tree's oscillation) *(verify)*; Rubinstein (1994) "Implied binomial trees" *JF* (the post-1987 skew);
Jackwerth–Rubinstein (1996) *JF* (10⁻¹⁶⁰ for the 1987 futures fall, as quoted by MacKenzie 2003); MacKenzie (2003) "An
equation and its worlds" *Social Studies of Science* (Black's sheets); Ahmad–Wilmott (2005) "Which free lunch would you
like today, Sir?" *Wilmott* (Nov.); Hull–White (2017) "Optimal delta hedging for options" *JBF* 82:180–190; Ruf–Wang
(2022) "Hedging with linear regressions and neural networks" *JBES* 40(4):1442–1454. Industry and official: President's
Working Group (April 1999); Greenspan and McDonough testimony (1 Oct 1998); Jorion (2000) *EFM* 6(3):277–300. Frontier:
§4.

---

## 3. The chapter list (21 scenes: hook, 19 chapters, outro; about 9,600 words, about 57 rendered minutes)

Conventions as in `quant5.md`. **Visual**: the signature picture, built before the formula. **Live**: a simulation drawn
as it runs. **Lab**: `lab_card` + `lab_run` with real House lines (≤ 12). **Replay**: `TrainingReplay` or a
ValueTracker scrub through checkpoints, seeds as `seed_band`. **Compute**: the `compute.py` item, CPU-minutes on one
core. Words are counted words (placeholders count 3); minutes are rendered-equivalent at 169 wpm. Every chapter card's
number changes (the manifest and the cards must agree; the one-line "Chapter N." narration lines are re-voiced).

### H · Hook: "Manufacturing an option" (520 w, 3.1 min) · `s01_hook` (kept)
- Keep as it is (the October 2021 month, the white hedged line, the gap 88.5% vs 61.2%, objectives, the House).
- Objectives card gains: "the PDE solved", "the carry", "industry and frontier".
- Pause-and-predict (new, before the reveal): "Bitcoin rose 37% in the month you sold the call. Did the *hedged*
  seller lose?" (No: +1.15; the hedge cancels direction.)
- Compute: `btc` (exists).

### 1 · Before the formula (520 w, 3.1) · item 1 · `s02_history` (kept, trimmed by ~90 words)
- Goal: the era, and the one thing the earlier formulas lacked.
- Beats: keep Bachelier → Sprenkle/Boness/Samuelson (μ and ρ glowing as unknowns, then replaced by r) → Thorp–Kassouf's
  hedge picture (the flat-at-today curve) → Black–Scholes via CAPM → Merton's continuous hedge → JPE and the Bell
  Journal. Add: **the floor** (moved from the old `exchange` block and tightened): 26 April 1973, 16 stocks, calls only,
  911 contracts on the first day (Cboe's 2012 annual report, quoting Joseph Sullivan); puts came in 1977. Black sold
  sheets of theoretical prices to market makers (MacKenzie 2003, with his Figure 2, "one of Black's sheets"), and
  calculators appeared on the floor (*(verify the TI SR-52 / 1975 advertisement against MacKenzie 2006 before saying
  "TI"; MacKenzie 2003 says calculators were rarely used on the CBOE floor because entering inputs was slow: say so)*).
- Derivation (one ladder, the "two unknowns" made exact): $C_{\rm Sprenkle} = e^{-\rho T}\big[Se^{\mu T}N(d_1^\mu) -
  KN(d_2^\mu)\big]$, $d^\mu_{1,2} = \frac{\ln(S/K)+(\mu\pm\frac12\sigma^2)T}{\sigma\sqrt T}$ (expected payoff under a lognormal
  with drift μ, discounted at ρ); set $\mu = \rho = r$ (why that is allowed is chapters 2–4) → Black–Scholes.
- Visual: a timeline strip lit 1900, 1961, 1965, 1967, 1969, 1973, 1977, 1997; the Sprenkle formula with μ and ρ in amber
  sliding out and r in teal sliding in.
- Pause-and-predict: "Two investors expect +30% and −10% a year from the stock. Do they agree on the call's price?" (Yes.)
- Facts to verify before rendering: Thorp's 1969 claim (Thorp, *A Man for All Markets*, 2017; his 2002–03 *Wilmott*
  column "What I knew and when I knew it" *(verify)*); "turned down by the first journals" (Black's own account, 1989
  *J. Portfolio Management* "How we came up with the option formula" *(verify)*).
- Compute: none.

### 2 · The riskless portfolio, done properly (470 w, 2.8) · item 2 · `s03_replication` (kept; heat block moves to ch3)
- Goal: the PDE from a self-financing replication, not from "Π is riskless" (the textbook gap the original argument
  glosses: Π = V − ΔS is not self-financing when Δ changes).
- Beats: keep `setup_` and `why_mu`. Rewrite `derive` as Shreve's version: the replicating portfolio X (Δ shares, the
  rest in the bank), its self-financing change, Itô on V, match the dW terms then the dt terms. A one-line note: the
  1973 "riskless hedge" argument reaches the same PDE; Merton's version is the one that survives scrutiny.
- Derivation (ladder):
  - $dX_t = \Delta_t\,dS_t + r(X_t - \Delta_tS_t)\,dt$ (self-financing: gains only from the shares and the bank).
  - $dV = \big(V_t + \mu SV_S + \tfrac12\sigma^2S^2V_{SS}\big)dt + \sigma SV_S\,dW$ (Itô).
  - $dX = \big(rX + (\mu - r)\Delta S\big)dt + \sigma\Delta S\,dW$ (substitute $dS = \mu S\,dt + \sigma S\,dW$).
  - $\Delta_t = V_S$ (match the $dW$ terms: the only way $X$ can track $V$ path by path).
  - $V_t + rSV_S + \tfrac12\sigma^2S^2V_{SS} - rV = 0$ (match the $dt$ terms; the $\mu SV_S$ terms cancel: μ drops out).
  - $V(T,S) = (S-K)^+$ (terminal condition), so $X_0 = V(0,S_0)$ replicates (uniqueness: Part 16 / Feynman–Kac).
- Visual: the old Π-portfolio panel kept; a two-column "match the coefficients" animation (dW column lights, then dt
  column; μ's two terms fly together and vanish).
- Pause-and-predict: "Why can the hedger ignore μ but not σ?" (σ multiplies the curvature term that cannot be hedged away.)
- Compute: none (no numbers).

### 3 · Solving the equation: heat, run backwards (430 w, 2.5) · item 2 · `s03a_heat` (new; `ThreeDScene`)
- Goal: solve the PDE (Black and Scholes did it this way, through the heat equation *(verify the 1973 paper's
  Churchill citation)*); see the payoff's kink melt.
- Beats: **Visual (3D)**: axes (x = log S, τ = time left, u). At τ = 0 the payoff ridge (a hockey stick in x); as a
  ValueTracker raises τ, the surface u(x, τ) rises out of it, the kink rounding off; a translucent Gaussian kernel slides
  along the x-axis and, at one point, the area under kernel × payoff is shaded: that area *is* the height of the surface
  there. Camera: phi 70° → 60°, theta −55° → −20°. Then the change of variables as a ladder, the convolution, and the
  formula falling out. **Lab 1**: `bs.price` (lines 40–49, 10 lines) next to a 6-line Gauss–Hermite convolution
  (`bs.heat_price`, new): both run, same digits.
- Derivation (ladder):
  - $\tau = T - t$, $x = \ln S$: $V_\tau = \tfrac12\sigma^2V_{xx} + (r - \tfrac12\sigma^2)V_x - rV$ (chain rule).
  - $u = e^{r\tau}V$, $y = x + (r - \tfrac12\sigma^2)\tau$: $u_\tau = \tfrac12\sigma^2u_{yy}$ (the discount and the drift removed:
    the heat equation with diffusivity σ²/2).
  - $u(y,\tau) = \int \frac{1}{\sqrt{2\pi\sigma^2\tau}}e^{-(y-z)^2/2\sigma^2\tau}\,(e^z - K)^+\,dz$ (the heat kernel convolved
    with the payoff: the fundamental solution).
  - Split at $z = \ln K$; complete the square in the $e^z$ term → $e^{y + \sigma^2\tau/2}N(d_1) - KN(d_2)$ (Gaussian integrals).
  - $V = SN(d_1) - Ke^{-r\tau}N(d_2)$ (undo the substitutions; $e^{y+\sigma^2\tau/2} = Se^{r\tau}$).
- Experiment: `heat` (new): the 3D grid u(x, τ) for 60 × 40 nodes (closed form), the kernel at three τ, and the
  convolution by 64-point Gauss–Hermite against `bs.price` for 9 (S, τ) pairs. Expected: agreement to 1e−10.
- Pause-and-predict: "Double the volatility. What happens to the *time* it takes the kink to melt?" (It is quartered:
  the equation only knows σ²τ.)
- Compute: `heat` (< 0.1).

### 4 · The price as an expectation (480 w, 2.8) · item 2 · `s04_riskneutral` (kept, trimmed; replay added)
- Goal: Feynman–Kac read for BSM; Q as the measure that makes the formula an average; the same price by simulation.
- Beats: keep `feynman_kac`, `two_worlds` (P 19.74 vs Q 12.36 vs formula 12.34), `meaning` (N(d₂) = 0.530 vs simulated
  53.1% under Q, 68.3% under P). Shorten `integral` to the risk-neutral Gaussian integral only and point to Part 9 (its
  ch11) for N(d₁) as the stock-measure probability. **Replay (new)**: the Monte Carlo estimate under Q drawn as n grows
  from 10² to 4·10⁵ (log x), 8 seeds as a `seed_band` narrowing like 1/√n onto the formula line; the Girsanov-weighted
  estimator from P-paths as a second band (the baseline at equal budget): wider, because the weights spread
  (Part 9 owns the ESS argument; here one sentence).
- Derivation (ladder): $V_0 = e^{-rT}\mathbb E^{\mathbb Q}[(S_T-K)^+]$ (FK, Part 5); $\ln S_T \sim N(\ln S_0 + (r-\tfrac12\sigma^2)T,\ \sigma^2T)$
  under Q (GBM with drift r); $\mathbb Q(S_T > K) = N(d_2)$ (standardize); $e^{-rT}\mathbb E^{\mathbb Q}[S_T1_{S_T>K}] = S_0N(d_1)$
  (complete the square: the exponential tilts the Gaussian by σ√T).
- Experiment: `riskneutral` (exists); `mc_seeds` (new): 8 seeds × n ∈ {10², …, 4·10⁵}, plain Q and P-weighted.
  Expected: the Q band contains 12.336 from n ≈ 10⁴; the weighted band is wider by about e^{θ²T/2} in sd (θ = 0.4).
- Pause-and-predict: "Under P, 68% of calls finish in the money. Is the call worth 68% of anything?" (No: prices are Q.)
- Compute: `riskneutral` (exists), `mc_seeds` (0.5).

### 5 · The tree and its limit, in 3D (470 w, 2.8) · item 2 · `s05_tree` (kept, rebuilt around the syllabus visual)
- Goal: the third derivation as a limit: the tree's recursion *is* a discretized PDE.
- Beats: shorten `one_step` to 20 s (Part 9 builds it; here: q = 1/3 from the numbers, one line). **Visual (3D, the
  syllabus's "tree converging to the PDE")**: `ThreeDScene` with axes (t, S, V). The CRR lattice for N = 4 is drawn
  as nodes at height V (gold balls, hedge ratio as a small arrow on each); the BS value surface V(t, S) is drawn
  translucent. A ValueTracker steps N = 4 → 16 → 64 → 256: the nodes multiply and settle onto the surface; the camera
  orbits 60°. **Live**: the existing N = 1…400 sawtooth redrawn as it computes beside it. **Lab 4**: `trees.crr`'s
  backward loop (lines 37–49, 12 lines), run for N = 4, 64, 400 (prints 10.2…, 10.4…, 10.4456 vs 10.4506; computed).
- Derivation (ladder): $V(t,S) = e^{-r\Delta t}[qV(t+\Delta t, uS) + (1-q)V(t+\Delta t, dS)]$ (backward induction);
  $u = e^{\sigma\sqrt{\Delta t}}$, $q = \frac{e^{r\Delta t}-d}{u-d} = \tfrac12 + \frac{r - \sigma^2/2}{2\sigma}\sqrt{\Delta t} + O(\Delta t)$ (expand);
  Taylor $V(t+\Delta t, uS)$ and $V(t+\Delta t, dS)$ to $O(\Delta t)$: the $\sqrt{\Delta t}$ terms give $rSV_S\Delta t$, the
  quadratic terms $\tfrac12\sigma^2S^2V_{SS}\Delta t$ (collect powers of $\sqrt{\Delta t}$); divide by Δt → the BS PDE.
  Error: $O(1/N)$ with an oscillating constant from the strike's position between nodes (Diener–Diener 2004 *(verify)*;
  smoothing it is Leisen–Reimer, Part 16).
- Experiment: `tree` (exists); `tree3d` (new): lattices for N = 4, 16, 64, 256 (nodes and values; `crr(..., keep=N+1)`),
  the BS surface on a 40 × 40 grid.
- Pause-and-predict: "Even N gives a node exactly at the strike. Above or below the formula?" (Read off the sawtooth.)
- Compute: `tree` (1, exists), `tree3d` (< 0.2).

### 6 · The Greeks as geometry (480 w, 2.8) · item 3 · `s06_greeks` (kept, 3D kept; a derivation added)
- Goal: every Greek as a slope of one surface, and derived in two lines each.
- Beats: keep `surface`, `delta_gamma`, `theta_identity`, `vega_one_bump`; trim `surface` by 40 words; add one ladder.
- Derivation (ladder):
  - $S\varphi(d_1) = Ke^{-rT}\varphi(d_2)$ (because $d_1^2 - d_2^2 = 2\ln(S/K) + 2rT$; the identity that makes Greeks short).
  - $\Delta = N(d_1)$ (differentiate the formula; the two $\varphi$ terms cancel by the identity).
  - $\Gamma = \frac{\varphi(d_1)}{S\sigma\sqrt T}$; $\mathcal V = S\varphi(d_1)\sqrt T = \sigma TS^2\Gamma$ (differentiate again; vega in gamma units).
  - $\Theta + rS\Delta + \tfrac12\sigma^2S^2\Gamma = rV$ (the PDE read as a ledger; at r = 0, Θ = −½σ²S²Γ).
- Pause-and-predict: "At-the-money, r = 0, T → ∞: the call's delta?" (→ 1, since d₁ = σ√T/2 → ∞.)
- Compute: none new (closed forms, drawn).

### 7 · Where the hedger's money comes from (500 w, 3.0) · item 4 · `s07_ledger` (kept; lab added)
- Goal: unchanged (the best chapter of the pilot).
- Beats: keep all four blocks; trim `three_paths` by 60 words. **Lab 2** (new, before `three_paths`): the House's
  hedging loop `hedge.delta_hedge`, lines 79–92 (≤ 12 lines: the step P&L, `g_term`, `the_acc`, the rebalance), then run
  on the three ledger paths; output: one line per path "gamma −x.xx theta +x.xx residual ±0.0x pnl ±x.xx" (computed from
  the existing `ledger` cache). The residual line is the honest one: what the second-order expansion misses.
- Derivation: the existing ladder (book = −(dV − ΔdS) → Taylor → Itô → Θ identity).
- Pause-and-predict: "Realized equals implied. Does every path end at zero?" (No: the spread from hedging four times a
  day, chapter 9.)
- Compute: `ledger` (exists).

### 8 · Hedging with the wrong volatility (470 w, 2.8) · item 5 · `s08_wrongvol` (kept, deepened)
- Goal: prove EKJS; see the gamma weighting as a landscape; the choice of hedge volatility (Ahmad–Wilmott).
- Beats: **Visual (3D, replaces the heat map)**: the dollar-gamma "mountain" ½Γ(t, S)S² over (t, S) (ridge along the
  strike, rising toward expiry). The two existing paths (2.12 vs 0.25) walk on the floor; a column under each path's
  track fills as it goes (∫½ΓS² dt), the near path's column visibly taller. Then the proof. Then **hedge at implied or
  at actual?**: two histograms grow from 10,000 paths (long a call bought at 20% when the world realizes 30%): hedged at
  actual, the profit is nearly the same on every path (a spike at V(σᵣ) − V(σᵢ)); hedged at implied, the same mean, a
  wide spread. Keep the Heston scatter (corr 0.99 with the gamma-weighted formula).
- Derivation (ladder):
  - $V^h = V(t,S;\sigma_h)$ solves $V^h_t + \tfrac12\sigma_h^2S^2V^h_{SS} = 0$ (r = 0; BS at the hedge vol).
  - $dV^h = V^h_t\,dt + V^h_S\,dS + \tfrac12V^h_{SS}\,d\langle S\rangle_t$, $d\langle S\rangle_t = \sigma_t^2S^2dt$ (Itô under the true dynamics).
  - $d(V^h - \text{hedge}) = \tfrac12\Gamma^hS^2(\sigma_t^2 - \sigma_h^2)\,dt$ (substitute the PDE; the hedge cancels $V^h_S\,dS$).
  - Short the option at $\sigma_h$: $\text{P\&L}_T = \tfrac12\int_0^T\Gamma^hS^2(\sigma_h^2 - \sigma_t^2)\,dt$ (integrate; $V^h_T$ = payoff).
  - If $\sigma_t \le \sigma_h$ always and $\Gamma^h \ge 0$ (convex payoff), P&L ≥ 0 on every path (EKJS 1998: robustness).
  - Hedging at actual σᵣ instead: P&L $= V(\sigma_r) - V(\sigma_i)$, path-independent in the continuous limit (apply the
    line above with $\sigma_h = \sigma_t$, mark-to-model).
- Experiment: `wrong_vol` (exists); `hedge_choice` (new): 20,000 GBM paths, μ = 10%, σᵣ = 30%, a call bought at σᵢ = 20%,
  hedged at 20% vs 30%, 252 steps; also σᵣ = 25% to make losses possible; `dgamma3d` (the surface on 50 × 40).
  **Probe (10,000 paths, σᵣ 30%)**: hedged at implied mean 1.986, sd 0.965; hedged at actual mean 1.992, sd 0.328
  (the 0.33 is the discrete-hedging noise of 252 steps); V(30%) − V(20%) = 1.991.
- Pause-and-predict: "You are sure realized will be 30%. Which hedge gives a smoother P&L day to day?" (Implied: the
  actual-vol hedge locks in the total but swings mark-to-market; Ahmad–Wilmott.)
- Compute: `wrong_vol` (1, exists), `hedge_choice` (1.5), `dgamma3d` (< 0.1).

### 9 · Hedging in steps (450 w, 2.7) · item 6 · `s09_discrete` (kept: `derive`, `measure`; `costs` moves to ch10)
- Goal: the √Δt law derived and measured with seeds; its distribution; where it stops (jumps).
- Beats: keep `derive` and `measure` (slope −0.486; formula with the exact integral; Derman–Kamal's
  $\sqrt{\pi/4}\,\mathcal V\sigma/\sqrt N$, now credited properly: Goldman Sachs Quantitative Strategies note, 1998/99, with
  its prefactor 0.886 on screen). **Replay**: the sd-vs-N chart rebuilt with 5 seeds as a `seed_band` (thin: the law is
  sharp). **Live**: the distribution at N = 13 vs 252 (Z² − 1 is skewed: the short-gamma P&L has a fat left tail; show
  skewness, computed). Then **Derman–Taleb**: the same hedge on Merton jump paths; the jump band refuses to narrow (a
  floor), while GBM's keeps halving every ×4.
- Derivation (ladder): the existing three rows; plus with jumps: per jump the hedge error is
  $V(S e^J) - V(S) - \Delta S(e^J - 1) \approx \tfrac12\Gamma S^2J^2$, not $O(\Delta t)$ (a jump is not made smaller by
  hedging more often), so $\operatorname{Var} \to \lambda\int\mathbb E[(\ldots)^2]dt > 0$ as $\Delta t \to 0$.
- Experiment: `discrete` (exists); `discrete_seeds` (5 seeds, 9 frequencies, 20,000 paths); `jump_floor` (Merton λ = 2/yr,
  J ~ N(−5%, 8%), hedged at the total-variance vol; N = 16…1,024). **Probe (4,000 paths)**: jump-diffusion sd 1.82,
  1.68, 1.63, 1.67 at N = 16, 64, 256, 1,024; GBM at the same total vol 1.01, 0.52, 0.26, 0.13.
- Pause-and-predict: "Hedge 16 times more often. How much smaller is the error?" (4×, unless the stock jumps.)
- Compute: `discrete` (2, exists), `discrete_seeds` (8), `jump_floor` (3).

### 10 · Paying for it: Leland's volatility (420 w, 2.5) · item 6 · `s09a_leland` (new; the `costs` block moves here)
- Goal: derive Leland; check it; see the trade-off surface; know where it fails.
- Beats: **Visual (3D)**: the total-risk surface over (hedges per quarter N, one-way cost k): height = expected cost +
  one sd of hedging error for the short ATM call; a ridge of optimal N for each k traced in gold; at k = 0 the optimum
  runs off to N = ∞ (continuous hedging), at 25 bp it sits near weekly. Then the derivation; then the existing weekly
  check (−0.53 → −0.25 → +0.01 without the end trades; the 0.26 of first hedge and unwind). **Lab 5**: `bs.leland_vol`
  (new, 3 lines) and the `hedge.delta_hedge(..., cost=k, cost_ends=False)` call; run → σ_L for daily and weekly hedging
  (problem 4's 21.2% and 20.6% at k = 0.2% round trip). Then **the limit**: with k fixed and N → ∞, σ_L → ∞ (σ_L² ∝ 1/√Δt):
  the price of perfect hedging with costs is unbounded, and the cheapest super-replication of a call is to buy the
  share (Soner–Shreve–Cvitanić 1995); Kabanov–Safarian (1997) showed Leland's error does not vanish for constant k
  (narrate only what the computed `kabanov` table shows; the paper's exact limit *(verify in the paper)*). Forward link:
  bands (Whalley–Wilmott; Part 11 on BTC; Part 17 learned).
- Derivation (ladder):
  - Per step the hedge trades $|\delta\Delta| \approx \Gamma|\delta S| = \Gamma S\sigma\sqrt{\Delta t}\,|Z|$ shares (Δ moves with Γ).
  - Expected cost per step $= \tfrac{k}{2}S\,\mathbb E|\delta\Delta| = \tfrac{k}{2}\Gamma S^2\sigma\sqrt{\Delta t}\sqrt{2/\pi}$ (k round trip; $\mathbb E|Z| = \sqrt{2/\pi}$).
  - Cost rate $= \tfrac12\Gamma S^2\cdot\sigma k\sqrt{2/\pi}/\sqrt{\Delta t}$ (divide by Δt): it looks like extra variance.
  - Absorb it: $\tfrac12\sigma_L^2 = \tfrac12\sigma^2 + \tfrac12\sigma k\sqrt{2/\pi}/\sqrt{\Delta t}$, i.e. $\sigma_L^2 = \sigma^2\big(1 + \sqrt{2/\pi}\,\tfrac{k}{\sigma\sqrt{\Delta t}}\big)$ (Leland 1985).
  - Error sd $\propto\sqrt{\Delta t}$ (ch9) while cost $\propto 1/\sqrt{\Delta t}$: the optimum balances the two.
- Experiment: `discrete` (exists, the weekly check); `leland_grid` (new): N ∈ {4, 8, 13, 26, 52, 126, 252} × k ∈ {0, 2, 5,
  10, 25, 50} bp, 10,000 paths each; `kabanov` (new): Leland-priced and hedged, k = 0.25%, N = 13 … 4,032.
  **Probe (4,000 paths)**: at k = 25 bp the mean cost grows from 0.38 (N = 4) to 1.51 (N = 252) while sd falls 1.64 →
  0.56; Leland's σ_L = 21.4%, 22.7%, 25.6%, 30.1% at N = 13, 52, 252, 1,008 and the premium 4.27 → 6.00, with the
  Leland-hedged book's mean near zero and sd 0.98 → 0.15 (rebalancing costs only).
- Pause-and-predict: "Costs double. Should you hedge more or less often?" (Less: the ridge moves left.)
- Compute: `leland_grid` (4), `kabanov` (4).

### 11 · Turning the formula inside out: implied volatility (430 w, 2.5) · item 7 · `s10a_solver` (new; the `invert` block moves here)
- Goal: why the inversion is well posed; how it is done to machine precision; how the House's solver does on 254 real
  quotes.
- Beats: **Visual (3D)**: Jäckel's normalized Black price $b(x, s)$ over log-moneyness x and total vol s = σ√T: a smooth
  sheet rising in s, flat for small s far from the money. A real quote is a horizontal plane; its intersection with the
  sheet is a curve; the quote's x picks one point on it: the implied s. The camera dives to the flat corner (deep OTM,
  short-dated) where the sheet's slope (vega) is nearly zero: there Newton overshoots. Then the existing single-quote
  block (43.66%, the Corrado–Miller start). **Lab 3**: `bs.implied_vol`'s loop (lines 121–135, 12 lines: Newton step,
  bracket update, bisection fallback). **Replay**: all 254 Surface quotes inverted at once. Left: the smile, dots
  starting at their guesses and snapping onto it iteration by iteration; right: max and median |error| per iteration on
  a log axis. Two runs at equal iterations: plain Newton from σ = 50%, and the House's (Corrado–Miller + bracket).
- Derivation (ladder):
  - $\max(F - K, 0) \le C/D < F$ (no arbitrage), and $\partial C/\partial\sigma = DF\varphi(d_1)\sqrt T > 0$ (vega) ⇒ exactly one σ
    (continuous, strictly increasing, onto the interval).
  - Normalized: $b(x,s) = e^{x/2}N(\tfrac xs + \tfrac s2) - e^{-x/2}N(\tfrac xs - \tfrac s2)$, $x = \ln(F/K)$ (divide by $\sqrt{FK}$:
    two inputs instead of five).
  - At the money: $b(0,s) = 2N(s/2) - 1 \approx s\varphi(0) = 0.3989\,s$ (Taylor) ⇒ $C \approx 0.4\,F\sigma\sqrt T$
    (Brenner–Subrahmanyam 1988; the desk question).
  - Newton: $s_{n+1} = s_n - (b(s_n) - \beta)/b_s(s_n)$; where $b_s \to 0$ the step explodes, so bracket it (bisection keeps
    a shrinking interval) or start close (Corrado–Miller 1996; Jäckel's rational guess + two Householder steps, 2015).
- Experiment: `implied` (exists); `solver_race` (new, from the cached Surface). **Probe**: the House solver needs a median
  of 3 iterations to 1e−10, p90 6, worst 11 (16-day calls 66–82% OTM, vega ~3e−4 in normalized units); plain Newton from
  a naive start produces inf or negative σ on 9 (s₀ = 0.5√T) to 33 (s₀ = 1) of the 254 quotes before recovering or not.
  The narration branches on these counts.
- **Bug found while probing** (decision 3): in `bs.implied_vol` a quote that has already converged can be knocked out by
  the bisection fallback while others are still iterating (quote 131 of the Surface: error 2e−15 at iteration 8, 0.37 at
  iteration 9, then ~30 halvings; the final answer is still right). A drawn replay would show the jump.
- Pause-and-predict: "A deep out-of-the-money option is quoted at a price one tick too high. How wrong can its implied
  vol be?" (Very: where vega is near zero, a tick is many vol points.)
- Compute: `solver_race` (< 0.2).

### 12 · The first smile, and the Surface's first row (420 w, 2.5) · items 7, 12 · `s10_implied` (kept: `smiles`, `surface3d`, `scoreboard`)
- Goal: unchanged: implied vols of every trade of 10 Dec 2025 smile and lean; Black–Scholes' best effort gets the
  Surface's first row (4.36 vol points in sample, 4.74 the next morning; 0 calendar violations; 11 parameters; DVOL 45.9
  vs ATM30 44.1).
- Beats: the three kept blocks, trimmed by 40 words. One new sentence and a dashed overlay: the smile is *not* a
  carry artefact (chapter 13 shows what a forgotten forward would have drawn).
- Pause-and-predict: "Out-of-the-money puts are dearer than equidistant calls. What is the market pricing that the
  formula is not?" (Big down moves.)
- Compute: `implied` (exists).

### 13 · Dividends, borrow and the forward (430 w, 2.5) · item 9 · `s10b_carry` (new)
- Goal: every listed variant of Black–Scholes is one formula on the forward; on the Surface, forgetting the forward
  draws a fake skew.
- Beats: **Visual**: a `PathFan` under Q with its mean line; a carry slider b = r − q moves; the fan's centre (the
  forward F = Se^{bT}) tilts, the call's value and delta bars respond, the put's move the other way. Then the
  reduction card: stock with dividend yield q (Merton 1973), stock index, borrow fee as negative carry (a hard-to-borrow
  stock, GameStop in Part 9), FX with q = r_f (Garman–Kohlhagen 1983), a futures contract with b = 0 (Black 1976), a
  Deribit inverse option = Black-76 ÷ F (BTC-settled; Alexander–Chen–Imeraj 2023). Discrete dividends: the escrowed
  model (`trees.american_call_dividend` uses it) in one line; early exercise before a dividend → ch14, and the trade
  around it → Part 11. **Live (real)**: the Surface's carry term structure ln(F/S)/T per expiry (computed: 2.6% at 2 days
  rising to 4.8% at 198 days (probe); Part 9 measured the same basis from parity), then the implied vols recomputed with
  spot in place of the forward: calls shift up, puts down, by more the longer the expiry: a skew that is pure
  bookkeeping.
- Derivation (ladder):
  - $dX = \Delta(dS + qS\,dt) + r(X - \Delta S)\,dt$ (the shares pay a yield q to the holder: self-financing with dividends).
  - $V_t + (r - q)SV_S + \tfrac12\sigma^2S^2V_{SS} - rV = 0$ (match terms as in ch2).
  - $V = e^{-rT}[FN(d_1) - KN(d_2)]$, $F = Se^{(r-q)T}$, $d_{1,2} = \frac{\ln(F/K) \pm \frac12\sigma^2T}{\sigma\sqrt T}$ (solve as in ch3 with drift r − q).
  - $\Delta = e^{-qT}N(d_1)$; the futures delta $= e^{-rT}N(d_1)$ (differentiate in S, or in F with $\partial F/\partial S = e^{(r-q)T}$).
  - Inverse (BTC-settled) price $= V/F$, so parity reads $C - P = D(1 - K/F)$ in coin (Part 9).
- Experiment: `carry` (new, cached Surface): carry per expiry; implied vols with spot vs forward. **Probe**: mean
  error +1.2 vol points for calls and −1.2 for puts at 51 days; +3.0 / −2.5 at 198 days; ±0.1 at one day.
- Pause-and-predict: "The dividend yield rises. Does a call's delta rise or fall?" (Falls: both e^{−qT} and N(d₁) fall.)
- Compute: `carry` (< 0.2).

### 14 · Early exercise and the free boundary (470 w, 2.8) · item 8 · `s11_american` (kept, deepened)
- Goal: when stopping beats waiting; the boundary as part of the solution; the early-exercise premium as an integral;
  what desks used before fast trees.
- Beats: keep `calls` (Merton's argument) and `puts` (6.0900 vs 5.5735). **Visual (3D, new)**: the early-exercise
  *premium* P_A − P_E over (S, τ): a ridge that is zero far above the strike, grows toward the boundary, and below the
  boundary becomes the exact gap (K − S) − P_E; the gold boundary curve S*(τ) runs along the ridge's crest, rising to
  K as τ → 0. Then the free-boundary problem (value matching; smooth pasting recalled from Part 8 in one line). Then the
  **premium integral** (Kim 1990; Jacka 1991; Carr–Jarrow–Myneni 1992): the boundary from the tree plugged into the
  integral reproduces the tree's price. Then **Barone-Adesi–Whaley (1987)**: the quadratic approximation, computed;
  Brennan–Schwartz (1977) named as the first FD solution (Part 16 solves the LCP). Last: the call with one discrete
  dividend (`trees.american_call_dividend`): the exercise nodes all sit just before the ex-date.
- Derivation (ladder):
  - $P(t,S) = \sup_{\tau}\mathbb E^{\mathbb Q}[e^{-r(\tau-t)}(K - S_\tau)^+]$ (optimal stopping; Part 8).
  - Continuation: $P_t + rSP_S + \tfrac12\sigma^2S^2P_{SS} - rP = 0$ for $S > S^*(t)$; stopping: $P = K - S$ for $S \le S^*(t)$.
  - Value matching $P(t, S^*) = K - S^*$; smooth pasting $P_S(t, S^*) = -1$ (Part 8's smooth fit).
  - In the stopping region the PDE operator gives $-rK$: $(\partial_t + \mathcal L - r)(K - S) = -rK$ (interest lost on the strike).
  - Itô on $e^{-rt}P$ and take expectations: $P_A = P_E + \int_0^T rKe^{-rs}\,\mathbb Q(S_s < S^*(s))\,ds$, with
    $\mathbb Q(S_s < S^*(s)) = N(-d_2(S_0, S^*(s), s))$ (the premium is the interest earned on K while exercised).
  - BAW: write $P_A = P_E + \varepsilon$; ε solves the PDE with $\varepsilon_t$ dropped (quadratic in the exponent), so
    $\varepsilon = A(S/S^*)^{q_1}$; fit $A, S^*$ by value matching and smooth pasting (one nonlinear equation).
- Experiment: `tree` (exists); `american_more` (new): premium surface (41 spots × 30 maturities, 600-step trees), Kim's
  integral from the 2,000-step boundary, BAW, the dividend call. **Probe**: tree 6.0900; European 5.5735; Kim integral
  with the raw tree boundary 6.0788 (the 0.011 gap is the boundary's node-grid staircase: smooth the boundary, or use
  the boundary from a finer tree, and the narration branches on the remaining gap); BAW 6.0976 (+0.008), its critical
  price 81.7 vs the tree's 80.7 at one year.
- Pause-and-predict: "Rates go to zero. Where does the American put's boundary go?" (To zero: with r = 0 the premium
  vanishes, problem 5.)
- Compute: `tree` (exists), `american_more` (1.5).

### 15 · Selling volatility on real Bitcoin (500 w, 3.0) · hedging replays on real data · `s12_btc` (kept; replay added)
- Goal: unchanged (the 1,706-month study), with the experiment *seen running* and its uncertainty drawn.
- Beats: keep `series`, `scatter`, `distribution`, `crisis` (trimmed by 80 words). **Replay (new)**: a date cursor
  sweeps April 2021 → December 2025: each month's trade drops as a dot into the scatter while the cumulative P&L line
  grows below, with a block-bootstrap band (200 resamples of the 57 non-overlapping months, 5 bootstrap seeds as a
  `seed_band` of the running mean); the ledger's gamma and theta totals for the month under the cursor flash beside it.
  One added sentence: Deribit's options are inverse (BTC-settled); the House hedges a dollar-linear call and the
  difference is second order here (Alexander–Chen–Imeraj 2023 work it out).
- Experiment: `btc` (exists); `btc_replay` (new: running mean, bootstrap bands, per-month ledger totals; from the cache).
- Pause-and-predict: "81% of months won. Is the strategy safe?" (The worst month lost 2.5 average months; the left tail.)
- Compute: `btc` (3, exists), `btc_replay` (0.2).

### 16 · October 1987 (500 w, 3.0) · item 10 · `s13_crash` (kept; tails shortened; insurance replayed)
- Goal: portfolio insurance as the delta hedge of this part, replayed on the real October; the skew's birth;
  performativity.
- Beats: keep `insurance` (now with **Lab 6**: `hedge.replicate_put` (new, 9 lines; Rubinstein–Leland 1981 on screen),
  run on 1987's daily returns). **Live (new)**: from 1 July 1987, an insured portfolio (one-year floor at 95, σ 15%,
  T-bill rate) rebalanced daily on Kenneth French's market returns: the stock weight bar falls as the market falls; the
  portfolio line tracks above the floor until Friday 16 October; on Monday the gap jumps straight through it, and the
  next day the model demands selling most of what is left. Brady's numbers on a card (verified: "$60 to $90 billion of
  equity assets"; "the typical portfolio insurance model calls for stock sales in excess of 20 percent of a portfolio in
  response to a 10 percent decline"; "$12 billion … should already have been sold. Less than $4 billion had in fact been
  sold"). Keep `day`. Replace `tails` by one sentence pointing to Part 1's crisis file (−20.7σ) and MacKenzie's quotation
  of Jackwerth–Rubinstein (1996): the futures fall had probability 10⁻¹⁶⁰ under lognormality. Keep `after` (the skew,
  Rubinstein 1994; MacKenzie's performativity and "the options market's collective defence mechanism").
- Derivation (ladder): insured value = portfolio + put ⇒ stock weight $w = \frac{S(1 + \Delta_P)}{S + P}$ (hold the
  replicating portfolio of S + P); $\partial w/\partial S > 0$ (the put's delta falls as S falls: sell into declines);
  a gap of size J between rebalances loses $\approx \tfrac12\Gamma S^2J^2$ (chapter 9's jump term, now for the insurer).
- Experiment: `crash87` (exists, now mostly unused on screen; keep the item); `insurance87` (new). **Probe**: with
  these parameters the model sells 37% of the equity on a 10% fall (Brady: "in excess of 20 percent"); the stock weight
  goes 0.93 (5 Oct) → 0.78 (16 Oct) → 0.64 (19 Oct, before the day's move) → 0.11 on the 20th; the insured portfolio
  ends October at 83.8 against a floor of 95. Narration branches on the computed breach.
- Pause-and-predict: "The insurer's rule says sell after a fall. What does that do when everyone follows it?"
- Compute: `crash87` (exists), `insurance87` (< 0.1).

### 17 · The Nobel, and then LTCM (400 w, 2.4) · item 11 · `s14_ltcm` (kept; one computed panel)
- Goal: the option theorists' fund as a short-volatility, short-liquidity book; what every hedge in this part assumes.
- Beats: keep `story` and `lesson`. **Visual (new)**: FRED VIXCLS for 1998 drawn day by day: 18.0 on 1 July, 45.7 on
  8 October (computed); below it the mark-to-market of a unit short-vega book (−1 per vol point), labelled
  illustrative ("VIX is a 30-day index; LTCM's options were long-dated, whose vols moved less"). Numbers on cards only
  from the record: losses "52 percent … through August 31" and "14 banks and securities firms" (McDonough, 1 Oct 1998);
  "a capital infusion of about $3-1/2 billion" (Greenspan, 1 Oct 1998); leverage and notional from the President's
  Working Group (April 1999) — **use the same figures as Part 8's crisis card (28:1, $1.3tn) after checking them in the
  PWG text** *(the CFTC copy was behind a challenge page this session)*. "Central bank of volatility" and the size of
  the equity-vol position: *as reported by Lowenstein (2000) (unverified)*. Full story → Part 41.
- Pause-and-predict: "A hedge is riskless if you can trade continuously. What three things must also be true?"
  (You can trade, you can fund, and others are not all doing the same trade.)
- Compute: `ltcm98` (< 0.1).

### 18 · Industry: how the formula is used for a living (460 w, 2.7) · `s14a_industry` (new)
- Goal: from the public record, how exchanges, market makers and desks use (and do not use) BSM.
- Beats (each a card or live object, its source on screen):
  1. **The floor, 1973–1987**: Black's sheets (MacKenzie 2003, figure 2), arbitrage by market makers pushing prices
     toward the model (MacKenzie–Millo 2003); calculators. **Firm file: O'Connor & Associates** (Chicago options
     trading firm founded 1977; described in 1989 as "the largest market maker in the financial options exchanges in
     the United States" (*New York Times*, as quoted); with Swiss Bank Corporation from 1988, acquired 1992, later UBS
     O'Connor) *(verify each against a primary source: SBC/UBS releases or the NYT archive)*.
  2. **Quoting in volatility**: desks quote, hedge and limit risk in vol and vega, not dollars; the model as a
     "translation device". The counter-view, labelled as an argument: Haug–Taleb (2011): traders priced with
     heuristics and put–call parity before and after 1973, and the formula is "never" used as such. Rebonato's "wrong
     number in the wrong formula" *(verify the quotation's source, *Volatility and Correlation* 1999)*.
  3. **Where the formula sits inside the plumbing** (one line each, pointers): Black-76 for options on futures; CME's
     switch to Bachelier in April 2020 (Part 5); OCC's margin (Part 5); the VIX (Part 12); grant-date fair value of
     employee options (Part 3).
  4. **Crypto adopts the formula**: Deribit lists only inverse options (Alexander–Chen–Imeraj 2023); Coinbase completed
     its $2.9bn acquisition of Deribit on 14 August 2025 (about $59–60bn open interest at closing, per the companies'
     announcement); IBIT options began trading on Nasdaq on 19 November 2024, 353,716 contracts on the first day
     (Nasdaq). The listed BTC options market and the Surface's venue now run the formula of 1973 every second.
- **Computed (the floor trader's mental arithmetic, on the Surface)**: the ATM-forward rule C ≈ 0.4Fσ√T against the exact
  price for each of the 11 expiries (using `implied.atm_iv`): the error is −(σ√T)²/24 plus 0.27% from 0.4 vs 0.3989;
  at most about 1% on 10 December 2025 (computed). And the vega of the 10 December tape by expiry ("where the market's
  vega sits").
- Pause-and-predict: "Why would a floor trader buy a sheet of theoretical prices rather than compute them?" (Speed:
  the sheet was faster than the calculator.)
- Compute: `industry` (< 0.1).

### 19 · Frontier: 2023–2026, and the delta desks actually use (450 w, 2.7) · `s14b_frontier` (new)
- Goal: what is new at the edge of BSM, with one model fitted on screen, honestly.
- Beats: **Replay (hands-on core): the minimum-variance delta on Bitcoin.** Black–Scholes' delta assumes volatility
  does not move with the price. Hull and White (2017) fit, by regression, how implied vol moves with spot and correct
  delta: $\Delta_{MV} = \Delta_{BS} + \frac{\mathcal V}{S}\,\frac{\mathbb E[d\sigma\mid dS]}{dS/S}$. The House fits the spot–vol beta
  of DVOL on BTC walk-forward, month by month (trailing 12 months), and hedges a 30-day ATM call priced at DVOL with
  both deltas out of sample. Left: the beta scrubbed through time (the line crosses zero: negative in 2021–22,
  positive in 2023), with 5 bootstrap seeds as a band; right: cumulative hedge-error variance of BS-delta vs MV-delta.
  **Probe (calendar-year betas, daily data)**: corr(Δln S, ΔDVOL) −0.42, −0.57, +0.33, +0.08, −0.39 for 2021–2025; a
  30-day ATM call at 55% has BS delta 0.531 and MV delta 0.480, 0.436, 0.574, 0.539, 0.497. Narration branches on the
  out-of-sample variance reduction (it may be small or negative when the beta flips: say so). Ruf–Wang (2022): on
  S&P 500 and Euro Stoxx options, a linear regression with the leverage effect does about as well as a neural hedger,
  and careless train/test splits overstate the network.
- Cards (verified this session; arXiv items are preprints and must be called that):
  - Alexander, Chen, Imeraj (2023), "Crypto quanto and inverse options", *Mathematical Finance* 33(4):1005–1043:
    pricing and hedging inverse and quanto-inverse options in a Black–Scholes world; Deribit lists only inverse products.
  - Matic, Packham, Härdle (2023), "Hedging cryptocurrency options", *Review of Derivatives Research* 26(1):91–133:
    calibrations point to stochastic vol, rare jumps and infinite activity; short-dated BTC options respond less to
    vol or gamma hedges; multi-instrument hedges cut tail risk on longer-dated ones.
  - The implied-vol race of 2026: Schadner, "An explicit solution to Black–Scholes implied volatility" (arXiv
    2604.24480: implied vol as an inverse-Gaussian quantile, exact, reported faster than a state-of-the-art solver on one
    benchmark); Le Floc'h and Healy, "Implying volatility: how fast can we go?" (arXiv 2605.29102, FlashIV); Amiriyan and
    Boutaib (arXiv 2609.05491, gated neural initial guesses + two Householder steps); Saqur, Limmer, Kratsios, Horvath,
    Buehler, "PIVOT" (arXiv 2606.17065: a differentiable layer around Jäckel's solver; 1.79·10⁹ inversions a second on
    one H100, authors' figure). Chapter 11's problem, fifty years on, still being sped up.
  - Ushakov and Berdinsky (arXiv 2608.19223, 2026): the Black–Scholes call price derived from the Gaussian kernel
    (chapter 3's route) and machine-checked in Lean 4 / Mathlib, "sorry-free".
  - Pointers, not repeated: deep hedging and learned bands (Part 17); rough volatility (Part 14); 0DTE (Part 12).
- Pause-and-predict: "When Bitcoin's vol rises with its price, should a call seller hold more or fewer coins than
  Black–Scholes says?" (More: MV delta > BS delta.)
- Compute: `mv_delta` (1; bootstrap seeds 5).

### O · The vol desk, recap, desk questions, problems (420 w, 2.5) · `s15_outro` (kept, extended)
- House card: the vol desk (pricer, hedger, solver, the first Surface row) gains `leland_vol`, `heat_price`, `baw`,
  `replicate_put`, `mv_delta`.
- Recap in 12 lines (one per syllabus item, plus industry and frontier). Payoff card unchanged (11, 12, 13, 14, 15, 16,
  17, 32, 37–38, 41) plus 22 (FX carry).
- Desk questions (README has solutions): keep the three (ATM mental price; the still straddle; the ATM digital's delta).
- Problems: the existing five plus (6) "Derive Leland's σ_L from the expected |δΔ| per step" and (7) "With carry b,
  show that using S instead of F raises call implied vols and lowers put implied vols; estimate the error for b = 4%,
  T = 0.5, σ = 45%" (solutions EN + ZH; the numbers from `carry`).
- Compute: none.

### Minutes (counted words; rendered-equivalent minutes at 169 wpm; the tool's pre-render estimate at 140 wpm)

| Scene | Words | Rendered min | Scene | Words | Rendered min |
|---|---|---|---|---|---|
| Hook | 520 | 3.1 | 11 Solver | 430 | 2.5 |
| 1 History | 520 | 3.1 | 12 Smile, first row | 420 | 2.5 |
| 2 Replication | 470 | 2.8 | 13 Carry | 430 | 2.5 |
| 3 Heat | 430 | 2.5 | 14 American | 470 | 2.8 |
| 4 Expectation | 480 | 2.8 | 15 BTC | 500 | 3.0 |
| 5 Tree 3D | 470 | 2.8 | 16 1987 | 500 | 3.0 |
| 6 Greeks | 480 | 2.8 | 17 LTCM | 400 | 2.4 |
| 7 Ledger | 500 | 3.0 | 18 Industry | 460 | 2.7 |
| 8 Wrong vol | 470 | 2.8 | 19 Frontier | 450 | 2.7 |
| 9 Discrete | 450 | 2.7 | Outro | 420 | 2.5 |
| 10 Leland | 420 | 2.5 | **Total** | **9,640** | **≈ 57.0** (estimate 68.9 before rendering) |

New 3D chapters and replays add animation time outside narration; if the first render runs long, trim chapters 1, 7,
15 (the longest kept ones), not the new material.

---

## 3b. Hands-on summary

**Labs (`lab_card` + `lab_run`, real House lines, ≤ 12):**
1. ch3 `bs.price` (`explainer/quant/house/bs.py` lines 40–49) beside the new `bs.heat_price` (6 lines): both print 10.4506
   for (100, 100, 1, 20%, 5%).
2. ch7 `hedge.delta_hedge` loop (`hedge.py` lines 79–92, the step, `g_term`, `the_acc`, the rebalance; trim to 12): run on
   the three ledger paths, prints gamma / theta / residual / P&L per path.
3. ch11 `bs.implied_vol` iteration (`bs.py` lines 121–135): run on the Surface, prints iterations median / p90 / max
   and the worst quote.
4. ch5 `trees.crr` backward loop (`trees.py` lines 37–49): run for N = 4, 64, 400.
5. ch10 `bs.leland_vol` (new, 3 lines) + the cost-aware `delta_hedge` call: run → σ_L daily / weekly and the grid's optimum.
6. ch16 `hedge.replicate_put` (new, ≤ 9 lines): run on 1987 → the weight and value table, floor breach.

**Replays and seeds:** ch4 MC under Q vs P-weighted, 8 seeds; ch5 tree N scrub with the 3D lattice; ch9 sd vs N, 5
seeds, and the jump floor; ch11 254 quotes converging, two solvers at equal iterations; ch15 the BTC study swept
month by month with bootstrap bands; ch19 the walk-forward MV-delta fit, 5 bootstrap seeds, BS delta as the baseline.

**Live simulations:** the kernel sliding over the payoff (ch3); lattice nodes settling onto the surface (ch5); the
hedging ledger (ch7, kept); paths walking on the dollar-gamma mountain and their columns filling (ch8); two hedges'
histograms growing (ch8); jump vs GBM error bands (ch9); the cost–risk surface with its ridge (ch10); the carry slider
tilting the fan (ch13); the insurer's weight bar falling through October 1987 (ch16); VIX 1998 day by day (ch17).

**3D (`ThreeDScene`):** ch3 heat surface u(x, τ); ch5 tree lattice → V(t, S); ch6 value surface (kept); ch8 dollar-gamma
½ΓS²(t, S); ch10 total-risk surface over (N, k); ch11 normalized Black price b(x, s); ch12 the Surface (kept); ch14
early-exercise premium over (S, τ).

**Compute budget (seeded; one core; ≈ 45 CPU-minutes of 120):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| tree* | 1 | discrete* | 2 | carry | 0.2 |
| riskneutral* | 0.1 | discrete_seeds | 8 | american_more | 1.5 |
| ledger* | 1 | jump_floor | 3 | btc*, btc_replay | 3.2 |
| wrong_vol* | 1 | leland_grid | 4 | crash87*, insurance87 | 0.2 |
| implied* | 0.5 | kabanov | 4 | ltcm98 | < 0.1 |
| heat, tree3d | 0.3 | solver_race | 0.2 | industry | < 0.1 |
| mc_seeds | 0.5 | hedge_choice, dgamma3d | 1.6 | mv_delta | 1 |

(* exists; names kept.) Everything is numpy; nothing needs torch. `discrete_seeds` and `leland_grid` use
`CACHE.partial` per (seed, N) so a killed run resumes. One command rebuilds the part:
`python -m videos.quant.quant10.compute`. Trial counter: `mv_delta` is a hedging comparison on data, registered (+1); the
rest are Q-side checks against closed forms.

---

## 4. Industry and frontier: sources

Checked this session (2 Nov 2026) by search and fetch:

| Fact | Source |
|---|---|
| Brady Report: "$60 to $90 billion of equity assets were under portfolio insurance administration"; "stock sales in excess of 20 percent of a portfolio in response to a 10 percent decline"; "$12 billion (20 percent of $60 billion) … should already have been sold. Less than $4 billion had in fact been sold" (report p. 29 in the scanned copy) | https://pages.nes.ru/aobizhaeva/BradyReport_1988_on_market_crash.pdf (full text, downloaded and searched) |
| Derman–Kamal, "When you cannot hedge continuously: the corrections to Black–Scholes", Goldman Sachs QS note (© 1998): σ_P&L ≈ √(π/4)·κσ/√N, prefactor 0.886 | https://emanuelderman.com/wp-content/uploads/1998/12/risk-non_continuous_hedge.pdf |
| MacKenzie (2003) "An equation and its worlds" *SSoS*: Black's service selling sheets of theoretical prices (fig. 2); post-1987 deterioration of fit (Rubinstein 1994); Jackwerth–Rubinstein (1996) 10⁻¹⁶⁰; the skew as "collective defence mechanism" | https://www.pure.ed.ac.uk/ws/files/43520366/MacKenzie_SSoS_2003_AnEquationAndItsWorlds.pdf |
| MacKenzie–Millo (2003) *AJS* 109(1):107–145 | https://wrap.warwick.ac.uk/88987 |
| CBOE opened 26 Apr 1973, 911 contracts on 16 stocks, calls only (Sullivan, quoted in Cboe's 2012 annual report); puts from 1977 (secondary) | https://cdn.cboe.com/resources/annual_reports/annualreport2012.pdf ; https://www.cboe.com/insights/posts/the-creation-of-listed-options-at-cboe |
| McDonough testimony, 1 Oct 1998: "52 percent losses on the year through August 31"; "14 banks and securities firms agreed to participate" | https://www.newyorkfed.org/newsevents/speeches/1998/mcd981001 |
| Greenspan testimony, 1 Oct 1998: "lost half its capital base" by end-August; "a capital infusion of about $3-1/2 billion"; "$2-3/4 billion of capital" returned end-1997 | https://www.federalreserve.gov/boarddocs/testimony/1998/19981001.htm |
| Jorion (2000) *EFM* 6(3):277–300 (LTCM's risk underestimated: short history, concentration) | https://ideas.repec.org/a/bla/eufman/v6y2000i3p277-300.html |
| Haug–Taleb (2011) *JEBO* 77(2):97–106 | https://ideas.repec.org/a/eee/jeborg/v77y2011i2p97-106.html |
| Ahmad–Wilmott (2005) *Wilmott* (Nov.): hedging at actual vol gives path-independent profit with wild mark-to-market swings; at implied, path-dependent | https://wilmott.com/?p=1358 |
| Kabanov–Safarian (1997) *Finance Stoch.* 1(3):239–250, DOI 10.1007/s007800050023 (limiting hedging error of Leland's strategy) | https://ideas.repec.org/a/spr/finsto/v1y1997i3p239-250.html |
| Hull–White (2017) *JBF* 82:180–190 (minimum-variance delta, empirical, no SV model needed) | secondary listings; *(verify against SSRN/Elsevier)* |
| Ruf–Wang (2022) *JBES* 40(4):1442–1454, DOI 10.1080/07350015.2021.1931241 | https://researchonline.lse.ac.uk/id/eprint/107811 ; https://arxiv.org/abs/2004.08891 |
| Alexander–Chen–Imeraj (2023) *Math. Finance* 33(4):1005–1043, DOI 10.1111/mafi.12410 | https://ideas.repec.org/a/bla/mathfi/v33y2023i4p1005-1043.html ; arXiv 2107.12041 |
| Matic–Packham–Härdle (2023) *Rev. Derivatives Research* 26(1):91–133, DOI 10.1007/s11147-023-09194-6 | https://edoc.hu-berlin.de/18452/29120 ; arXiv 2112.06807 |
| Jäckel (2015) "Let's be rational" *Wilmott* 2015(75):40–53 (two Householder steps to machine precision; C code) | secondary (PyPI `lets_be_rational`, NAG s30acc); jaeckel.org *(fetch the paper)* |
| Schadner (2026) arXiv 2604.24480 (v4 18 May 2026) | https://arxiv.org/abs/2604.24480 |
| Le Floc'h–Healy (2026) arXiv 2605.29102 (FlashIV) | https://arxiv.org/abs/2605.29102 |
| Saqur, Limmer, Kratsios, Horvath, Buehler (2026) arXiv 2606.17065 (PIVOT; 1.79e9 IV/s on one H100, max rel. error 9.3e−14, authors' figures) | https://arxiv.org/abs/2606.17065 |
| Amiriyan–Boutaib (2026) arXiv 2609.05491 | https://arxiv.org/abs/2609.05491 |
| Ushakov–Berdinsky (2026) arXiv 2608.19223 (BS call price from the Gaussian kernel, Lean 4/Mathlib, "sorry"-free) | https://arxiv.org/abs/2608.19223 |
| Coinbase closed the Deribit acquisition 14 Aug 2025: $2.9bn ($700M cash + 11M shares), ~$59bn open interest | https://www.businesswire.com/news/home/20250814749927/en ; https://www.theblock.co/post/366957 |
| IBIT options' first day 19 Nov 2024: 353,716 contracts (Nasdaq) | https://www.nasdaq.com/newsroom/nasdaq-listed-ibit-options-end-first-day-top-1-all-options-products-traded |
| O'Connor & Associates founded 1977 (Chicago); SBC relationship from 1988, acquired 1992; "largest market maker in the financial options exchanges in the United States" (NYT 1989, as quoted) | secondary only: https://en.wikipedia.org/wiki/O%27Connor_%26_Associates ; *(verify in UBS/SBC releases or the NYT archive)* |

**Unverified (keep the marks; verify or drop before rendering):** Thorp's "1969" formula (his own account); the 1973
paper's rejections; the TI calculator advertisement; the 1973 paper's heat-equation/Churchill route; "1.1 million
contracts by end-1973"; Deribit's ~90% share of BTC options OI (ForkLog, secondary); PWG 1999's leverage and notional
figures (Part 8 quotes 28:1 and $1.3tn; the existing Part 10 narration says "some twenty-five times": make the two
parts agree after reading the PWG report); LTCM's equity-vol position size and "central bank of volatility" (Lowenstein);
Rebonato's "wrong number" quotation; Diener–Diener (2004); textbook chapter numbers marked *(verify)*; the Kabanov–
Safarian limit's exact form; Jäckel's 2024 implementation update (cited by Schadner).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 10 · Black–Scholes–Merton (~57; the pilot)
1. 1973: Black, Scholes, Merton; Sprenkle, Boness and Samuelson's two unknowns; Thorp and Kassouf's hedge; the CBOE
   opens (911 contracts, 16 stocks); Black's sheets of theoretical prices on the floor.
2. Three derivations: the self-financing replication PDE; the PDE solved through the heat equation; the risk-neutral
   expectation; the binomial tree's limit, derived (the recursion is a discretized PDE) and seen in 3D.
3. The Greeks as geometry, derived (Sφ(d₁) = Ke^{−rT}φ(d₂)); Θ + rSΔ + ½σ²S²Γ = rV.
4. The hedging P&L ½ΓS²(σ²_implied − σ²_realized)dt, derived and watched in the ledger.
5. Hedging with the wrong volatility, proved (El Karoui–Jeanblanc–Shreve 1998); hedge at implied or at actual
   (Ahmad–Wilmott 2005); dollar gamma as a landscape.
6. Discrete hedging: error ∝ √Δt (Boyle–Emanuel 1980; Derman–Kamal's √(π/4)); the floor jumps put under it
   (Derman–Taleb 2005). Transaction costs: Leland (1985) derived and checked; the cost–risk trade-off; why constant
   costs make perfect hedging unbounded (Soner–Shreve–Cvitanić 1995; Kabanov–Safarian 1997).
7. Implied volatility by inversion: existence and uniqueness, the normalized price, Brenner–Subrahmanyam,
   Corrado–Miller, Jäckel's "Let's be rational"; the House's solver on all 254 quotes.
8. American options: the free boundary, the early-exercise premium (Kim 1990; Carr–Jarrow–Myneni 1992),
   Barone-Adesi–Whaley (1987), the call before a dividend.
9. Dividends, borrow and the forward: Merton's yield, Black-76, Garman–Kohlhagen, inverse (coin-settled) options; the
   fake skew drawn by a forgotten forward.
10. 1987: portfolio insurance (Rubinstein–Leland 1981) replayed on the October data; the Brady Commission's numbers;
    the birth of the skew; MacKenzie's performativity thesis.
11. 1997 to 1998: the Nobel, then LTCM as a short-volatility, short-liquidity book.
12. The Surface's first row.

*Textbooks:* Hull OFOD ch. 13, 15, 17–19; Shreve II §4.5, ch. 5, ch. 8; Björk ch. 7–10 and the dividends/futures/FX
chapters; Wilmott PWOQF ch. 5–9 and the hedging and transaction-cost chapters; Joshi *Concepts* ch. 5–7, 12; Taleb
*Dynamic Hedging*; Baxter–Rennie ch. 3–4. Perpetual put and smooth fit → Part 8; trees, PDE and LSM numerics → Part
16; the smile → Part 12; the trade (scalping, frequency on data, dividend play) → Part 11.
*Computed:* the heat-kernel solution; MC under Q with seeds; the tree lattice converging; hedging replays on GBM,
Heston and jump paths, and on real BTC against DVOL (1,706 months); hedge at implied vs actual; error vs rebalancing
with seeds and the jump floor; Leland checked, the cost–risk surface; the solver race on the Surface; the carry term
structure and the forgotten-forward skew; the American premium (tree, Kim's integral, BAW); portfolio insurance on
October 1987; VIX through 1998; the minimum-variance delta on BTC.
*Visuals:* `HedgeLedger`; the tree converging to the PDE in 3D; the heat surface; the dollar-gamma mountain; the
normalized price surface; the early-exercise premium surface; the insurer's weight through October 1987.
*Labs:* `bs.price`/`heat_price`, `hedge.delta_hedge`, `bs.implied_vol`, `trees.crr`, `leland_vol`, `replicate_put`.
*Industry:* Black's sheets and the CBOE floor; quoting in volatility (and Haug–Taleb's dissent); Black-76 at the
exchanges; Deribit (Coinbase, 2025) and IBIT options (2024). *Frontier:* inverse options (Alexander–Chen–Imeraj
2023); hedging crypto options (Matic–Packham–Härdle 2023); the 2026 implied-volatility solvers (Schadner; Le
Floc'h–Healy; PIVOT); Black–Scholes machine-checked in Lean (2026); the minimum-variance delta (Hull–White 2017;
Ruf–Wang 2022).
*Crisis:* 19 October 1987. *Firms:* the CBOE floor; O'Connor & Associates; Leland O'Brien Rubinstein; LTCM.
*Desk:* "ATM call, 1 year, vol 20%, spot 100: price it in your head" (≈ 0.4·σ·S·√T); "Long a straddle, the stock
sits still for a week"; "What's the delta of a digital as T → 0?"
*House:* the vol desk opens: the BSM pricer, the hedger, the implied-vol solver and the Surface's first row.
```

---

## 6. Implementation notes

**Manifest (21 scenes, in order).** `s01_hook` Hook · `s02_history` History · `s03_replication` Replication ·
`s03a_heat` Heat (new) · `s04_riskneutral` RiskNeutral · `s05_tree` Tree · `s06_greeks` Greeks · `s07_ledger` Ledger ·
`s08_wrongvol` WrongVol · `s09_discrete` Discrete · `s09a_leland` Leland (new) · `s10a_solver` Solver (new) ·
`s10_implied` Implied · `s10b_carry` Carry (new) · `s11_american` American · `s12_btc` BTC · `s13_crash` Crash ·
`s14_ltcm` LTCM · `s14a_industry` Industry (new) · `s14b_frontier` Frontier (new) · `s15_outro` Outro. All kept module and
class names are unchanged; blocks that move (`s03_replication.heat` → `s03a_heat`; `s09_discrete.costs` →
`s09a_leland`; `s10_implied.invert` → `s10a_solver`) are re-voiced in their new modules. Every chapter card's number
changes; `s05_tree` (3D lattice) and the new 3D scenes are `VoiceoverScene, ThreeDScene` (as `s06_greeks` is). Scene method names
must not shadow `setup`/`render`/`play`/`wait`/`add`/`remove`/`clear` (`s03_replication.setup_` already avoids it).

**New House functions** (append-only; tests appended to `tests/test_quant_house.py`):
- `bs.heat_price(payoff, S, T, sigma, r=0.0, n=64)`: Gauss–Hermite convolution of any payoff with the lognormal
  kernel. Test: equals `bs.price` for a call and a put to 1e−9; a digital equals e^{−rT}N(d₂).
- `bs.leland_vol(sigma, k_round_trip, dt)`. Test: problem 4's 21.2% (daily) and 20.6% (weekly) at k = 0.2%.
- `bs.baw(S, K, T, sigma, r, q=0.0, cp=-1)` (Barone-Adesi–Whaley 1987) returning price and critical price. Test: within
  0.02 of a 2,000-step CRR tree for the ATM 1-year put (r = 5%, σ = 20%: 6.0976 vs 6.0900, probe); equals the European
  call when q = 0 and cp = +1.
- `trees.early_exercise_premium(S, K, r, sigma, times, boundary)`: the Kim/CJM integral. Test: with the 2,000-step tree's
  boundary, within 0.015 of the tree's premium (probe gap 0.011 with the raw boundary; tighten after smoothing).
- `hedge.replicate_put(returns, rf, floor, T, sigma, start=100.0)`: daily synthetic-put insurance (Rubinstein–Leland),
  returns weights and values. Test: on 2,000 seeded GBM paths with daily steps at the model's σ, the terminal value is
  ≥ 0.98 × floor on ≥ 99% of paths; with one −20% gap it breaches.
- `hedge.spot_vol_beta(logret, dvol_change)` and `hedge.mv_delta(S, K, T, sigma, beta, r=0, q=0, cp=1)` (Hull–White
  style, beta form). Test: recovers a planted beta from simulated data within 0.05; with beta = 0 equals the BS delta.
- (no new path generator: `sim.merton_jumps` exists; `control.perpetual_put` exists for the one-line recall.)

**`compute.py`.** Keep the eight items and their keys. Add: `heat`, `tree3d`, `mc_seeds`, `hedge_choice`, `dgamma3d`,
`discrete_seeds`, `jump_floor`, `leland_grid`, `kabanov`, `solver_race`, `carry`, `american_more`, `btc_replay`,
`insurance87`, `ltcm98`, `industry`, `mv_delta`. Data: all already cached and in the manifest (Deribit trades of 10–11
Dec 2025 via `surface.build`, DVOL, Binance BTCUSDT 1h, Kenneth French daily, FRED `VIXCLS`). **No new data.**
`btc_replay` and `mv_delta` read `btc`'s inputs the way `compute_btc` does (one helper, no duplicated alignment code).

**Decisions for the lead.**
1. **Length arithmetic**: the rendered narrator runs at 169 counted words/min on this part, not 139–140. This plan targets
   ~9,600 words (≈ 57 rendered min; the tool will estimate ≈ 69 min before rendering). Tell the implementer to work to
   the word table, not to the pre-render estimate (§0).
2. **Overlaps accepted here**: Part 9 keeps one-step trees, the CRR sawtooth, Girsanov ESS and numeraire probabilities
   (Part 10 shortens them); Part 1 keeps the 1987 sigma count (Part 10 drops its `tails` block to one line); Part 8 keeps
   the perpetual put/smooth fit; Part 16 keeps the American value surface (Part 10 draws the premium surface); Part 11
   keeps move-triggered and BTC hedge-frequency work. Confirm, or reassign.
3. **`bs.implied_vol` bug** (found in the probe): converged quotes are bumped by the bisection fallback while others
   iterate (Surface quote 131: 2e−15 → 0.37 at iteration 9, ~30 extra iterations; final values correct). The fix is a
   per-element `done` mask (freeze converged entries) or accepting a Newton step equal to a bracket end. It is a bug
   fix inside an existing House function, which the append-only rule does not cover: allow the Part 10 implementer to
   fix it (with a test), or assign it separately. Lab 3 and the replay should run on the fixed solver.
4. **The minimum-variance delta** sits in Part 10's frontier chapter (BSM's delta corrected by data). Part 12 owns smile
   dynamics (sticky strike/delta); confirm that Part 12 does not also plan an MV-delta experiment.
5. **LTCM figures**: Parts 8 and 10 must quote the same PWG numbers; read the PWG report (the CFTC copy was blocked
   here) and fix one wording for both.
6. Inverse options: Part 9 explains BTC-settled parity; Part 10 uses the inverse form only in ch13 and ch15 (one line
   each) and the Alexander–Chen–Imeraj card. Confirm no third part plans an inverse-option chapter.

**Risks.**
- Rendering time: three new 3D scenes plus the rebuilt tree chapter; keep surfaces at ≤ 40 × 40 and reuse
  `price_surface`.
- The `kabanov` table may show the Leland-hedged error still shrinking at N = 4,032 (the probe: sd 0.15 at N = 1,008);
  the narration must say what it shows (the *price* diverging is the robust lesson) and must not assert a nonzero limit
  without the paper.
- `mv_delta` may show little or negative out-of-sample gain when the beta flips; that is the result, not a failure.
- `insurance87`'s numbers depend on the chosen floor, horizon and σ; say "an illustrative insured portfolio" on screen
  and put the parameters in the corner; Brady's figures are the evidence, the replay is the mechanism.
- The pre-render estimate (≈ 69 min) will alarm a reader of `lecture_length.py`; see decision 1.
- Facts in §4's unverified list must be verified or dropped; O'Connor's details rest on secondary sources.

**Chinese.** New terms for `QUANT_ZH_GUIDE.md`: 自融资组合 (self-financing portfolio), 热方程 (heat equation), 热核
(heat kernel), 美元伽马 (dollar gamma), 离散对冲误差 (discrete hedging error), 交易成本 (transaction costs), Leland
波动率, 隐含波动率反解 (implied-vol inversion), 归一化 Black 价格 (normalized Black price), 持有成本 (carry), 币本位/反向期权
(inverse option), 提前行权溢价 (early-exercise premium), 自由边界 (free boundary), 光滑粘贴 (smooth pasting), 投资组合保险
(portfolio insurance), 最小方差 delta (minimum-variance delta), 现货-波动率贝塔 (spot–vol beta). The README gets the
textbook-audit table (§2b), the full paper list (§2c and §4), 3 desk questions and 7 problems with solutions in English
and Chinese.

## 7. Lead's decisions (2 Nov 2026)

1. Yes: write to the plan's word table (~9,640 words). The length tool now uses the quant narrator's measured 168 wpm and re-estimates any rewritten chapter, so `lecture_length.py quant10 --floor 50` is reliable again.
2. Overlaps confirmed as assumed (Part 9: one-step trees, CRR sawtooth, Girsanov, numeraire probabilities; Part 1: the 1987 sigma count; Part 8: perpetual put, smooth fit; Part 16: the American value surface; Part 11: hedge frequency on BTC and move-triggered hedging).
3. Yes: fix `bs.implied_vol` so converged quotes are frozen (masked) while others iterate, with a test; final values unchanged (other parts use it).
4. The minimum-variance delta on BTC belongs to Part 13 (being expanded; a `stochvol.py` function). Part 10's frontier chapter cites it in one line with a forward link and uses another replay (e.g. the solver race or an operator-learning / neural-BS item from the plan).
5. LTCM wording: the Part 8 implementer is verifying from the President's Working Group report and writes it to `scratchpad/plans/ltcm_wording.md`; use that wording (if absent when you need it, verify yourself from the PWG report or Federal Reserve History).
6. Confirmed: Part 9 owns coin-settled (inverse) parity; no other part plans an inverse-option chapter.
Unverified items: verify or drop (Thorp 1969, the journal rejections, the TI advertisement, Churchill, PWG figures, Lowenstein, O'Connor, Rebonato's quote, Diener–Diener, Kabanov–Safarian, chapter numbers).
