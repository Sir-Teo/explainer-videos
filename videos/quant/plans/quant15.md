# Part 15 · Exotics and Structured Products: expansion plan (22.3 → ~58 min)

This is a planning document; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 and the
§6 Part 15 entry; `READING.md` §1–2 and §4 Part 15; every file in `videos/quant/quant15/` (manifest, common,
compute, the twelve scenes, README) and its cache `.cache/quant15/`; `explainer/quant/house/exotics.py` with its
three tests in `tests/test_quant_house.py`; `explainer/quant/viz.py` (`lab_card`/`lab_run`, `TrainingReplay`,
`seed_band`); `explainer/quant/__init__.py` (timeline years); `videos/ai/LECTURE_GUIDE.md`; `videos/quant/plans/quant5.md`
(the format) and `IMPLEMENT.md`. Neighbours checked so material is not repeated:
- `quant5` plan: reflection principle, first passage, and BGK named as a link to Part 15.
- `quant10`: discrete hedging.
- `quant11` s06: dispersion and implied correlation.
- `quant12` s04: variance swaps.
- `quant13` s08: forward smile, a cliquet and a forward-start under five models, and the SPX/VIX puzzle. Its
  `exotics` and `calibrate` items are reused here.
- `quant16`: MC, QMC, MLMC, LSM, Greeks, AAD, FD, Fourier.
- `quant17`: differential ML, deep hedging, neural SDEs.

Part 15 must go **past** those parts on what is specific to exotics: path dependence, barriers and static
replication, discontinuous payoffs, autocallables, correlation, model uncertainty, and the business and its crises.

**Planning runs.** Every number below marked "(planning run)" was computed this session from cached data or
simulation, with scripts in `scratchpad/q15/` (`p_static.py`, `p_modelrisk.py`, `p_cliq.py`, `p_snow.py`,
`p_surr.py`, `p_uvm.py`, `p_dig.py`, `p_corr.py`, `p_buyers.py`). Each must be recomputed by `compute.py`. Narration
branches on what comes back.

---

## 1. Current state (`python tools/lecture_length.py quant15`: 22.3 min)

| # | Scene | Min | What it covers, and how deep |
|---|---|---|---|
| — | `s01_hook` Hook | 1.5 | CSI 500 ETF 2021–2024 drawn, knock-in levels of the 2022–23 notes, the January 2024 low; objectives (7 rows); House card. Strong picture, but no history segment ("how we got here"), which the standard requires. |
| 1 | `s02_business` | 1.9 | Note = ZCB + options (3-row ladder of statements, not a derivation); Henderson–Pearson 8%; Célérier–Vallée; two firm cards. **No decomposition computed, no funding spread, no buyer outcomes.** |
| 2 | `s03_barriers` | 2.2 | Reflection on one static path; DOC formula quoted; BGK table (monthly 7.44, continuous 7.28, BGK within 0.01); delta near the barrier (0.43). **No derivation of the formula, no PDE view, no 3D, no static hedging (Derman–Ergener–Kani and Carr–Ellis–Gupta are on the paper list but absent).** |
| 3 | `s04_digitals` | 2.4 | Digital delta spike (0.06/0.25/0.67), call-spread table, Asian CV (6.20 against 10.87; noise ÷21), lookback 19.3/18.5. Three topics in one chapter; **no hedging simulation, no one-touch, no skew effect on digitals, no Asian PDE.** |
| 4 | `s05_snowball` | 3.2 | Terms, fair coupon by vol (3.9% → 26.6%; 13.4% at 20%), value surface (2D), dealer delta 1.7 → 1.15 and vega sign. Good, the richest chapter. **No outcome distribution, no carry/basis, Greeks not in 3D, no lab.** |
| 5 | `s06_crash` | 2.3 | Jan–Feb 2024: −18%, Bloomberg $13 bn, UBS $50 bn, April curbs; stylized 36-note book, 11 knock-ins, dealer delta 15 → 25 → 15 from the surrogate; the debate. Good crisis file. |
| 6 | `s07_korea` | 1.8 | Stylized HSCEI step-down ELS 2021 (6 of 12 lost 38–54%); 19.3 tn won, 1.2 tn lost, FSS scheme. **No 2015–16 episode, no firm file (Natixis 2018).** |
| 7 | `s08_correlation` | 1.0 | Worst-of put 0.169 → 0.115 over ρ; ρ = 0.46. **No derivation (Margrabe, Stulz), no 3D, no correlation regimes, no correlation skew model.** |
| 8 | `s09_uvm` | 1.9 | BSB in words, call-spread bounds [0.31, 0.62] against BS 0.45–0.48; reserves in one line. **No derivation, no non-additivity number, no hedged (Lagrangian) UVM.** |
| 9 | `s10_surrogate` | 1.0 | MLP on 3,000 MC prices, RMSE 0.017, 0.4 µs against 3 s. **No replay, one seed, no baseline.** |
| 10 | `s11_house` | 0.9 | Rule 15, counter 73. |
| — | `s12_outro` | 2.3 | Recap, 3 desk questions, 5 problems, payoff, references. |

Overall the experiments are real and worth keeping, but the part is less than half as long as it should be:
- Syllabus item 6 (cliquets and forward-starts) is **missing entirely**, and item 9 (dealer flows) is two sentences
  inside chapter 4.
- There is **no 3D** (the syllabus asks for the snowball's value surface with the cliff; it is drawn in 2D), **no
  lab**, **no replay**, **no live simulation** except `Create` of finished curves, **no frontier chapter** and **no
  industry chapter** apart from the business cards.
- Static replication (2 papers on the list), model risk (Cont 2006; Glasserman–Xu 2014) and the textbooks' Asian
  and lookback PDE material are absent.
- Two factual items need repair: Korea's outstanding notional (19.3 tn won here, 18.8 tn in the March 2024 press,
  see §4) and the README's claim of "about 55 minutes".

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item | Now | Plan |
|---|---|---|
| 1 Structuring business; who buys | ch1, 1.9 min, thin | ch1 anatomy and margin (computed decomposition); ch2 buyers and their outcomes on the real path |
| 2 Barriers: reflection, closed forms, BGK | ch2, partial | ch3 reflection → closed form → PDE, 3D surface; ch4 discrete monitoring and static hedging |
| 3 Asians, lookbacks, digitals; hedging problems | ch3 squeezed | ch5 digitals, one-touch, call-spread hedge simulated; ch6 Asians and lookbacks |
| 4 Autocallables and snowballs | ch4–6 | ch7 pricing and outcomes; ch8 Greeks in 3D; ch9 January 2024; ch10 Korea and Natixis |
| 5 Worst-of, correlation skew, dispersion | ch7, 1.0 min | ch11 (Margrabe, Stulz, 3D, regimes, worst-of snowball) |
| 6 Cliquets and forward-starts | **absent** | ch12 (homogeneity, the vega ridge, reverse cliquets) |
| 7 Uncertain volatility | ch8 partial | ch13 (BSB derived, live PDE, non-additivity, Lagrangian hedge) |
| 8 Model risk and reserves | one sentence | ch14 (same vanillas, different exotics; Cont; Glasserman–Xu) + ch17 (how desks reserve) |
| 9 Dealer hedging flows | two sentences | ch15 (book vega and gamma on the real path; peak vega) |
| 10 Neural surrogate | ch9, 1.0 min | ch16 (replay, seeds, polynomial baseline, an honest verdict) + ch18 frontier |

### (b) Textbook sections → chapter

Chapter numbers checked against the publisher where noted. Others are marked *(verify)*.

| Book · section | Chapter / elsewhere |
|---|---|
| **Hull OFOD (11th) ch. 26 "Exotic options"** *(verify the chapter number in the 11th ed.)*: packages | 1 |
| — nonstandard American; perpetual American; gap options | 5 (gap as a digital plus a call, one line); American → Part 16 |
| — forward start; cliquets | 12 |
| — compound; chooser | README reading note (Geske 1979 in Part 20, compound as equity on assets); chooser = call + put by parity, problem 7 |
| — barrier; binary; lookback; shout; Asian | 3, 4, 5, 6; shout as a lookback variant, one line in 6 |
| — exchange options; options involving several assets (basket, rainbow) | 11 |
| — volatility and variance swaps | Part 12 (forward link) |
| — static options replication (Derman–Ergener–Kani) | 4 |
| Hull ch. 27 "More on models and numerical procedures" (path-dependent numerics, barrier trees) | 6 (Asian state augmentation), Part 16 |
| **Shreve II ch. 7**: 7.2 maximum of BM with drift; 7.3 knock-out barriers (up-and-out call, BSM PDE, computation); 7.4 lookbacks (floating strike, PDE, reduction of dimension); 7.5 Asians (fixed strike, augmentation of state, change of numéraire) | 3 (7.2–7.3), 6 (7.4–7.5) |
| **Bouzoubaa–Osseiran** (TOC verified, Wiley-VCH): 2 the world of structured products (sell side, buy side, the market, an ELN) | 1, 2 |
| — 3.9 Asians; 3.10 an example of the structuring process | 6, 1 |
| — 5.7–5.8 vanna, volga, multi-asset sensitivities | 8, 11 |
| — 7 correlation (multi-asset options, measurement, baskets, quantos, trading correlation) | 11; quantos → Part 22 |
| — 8 dispersion (worst-of, best-of); 9 dispersion options (rainbow, ICBC, outperformance) | 11 (worst-of, best-of, rainbow); dispersion trading → Part 11 |
| — 10 barriers (BS valuation; hedging down-and-in puts; barriers in structured products) | 3, 4, 8 |
| — 11 digitals (European, American, risk analysis, in structured products) | 5 |
| — 12 autocallables (single-asset; participating; with down-and-in puts; multi-asset) | 7, 8, 11 (worst-of snowball) |
| — 13 the cliquet family (forward starts; local caps and floors; reverse cliquets) | 12 |
| — 14 more cliquets (multi-asset; Napoleons; lookbacks) | 12 (Napoleon), 6 |
| — 15 mountain range (Altiplano, Himalaya, Everest, Atlas) | 11 (named on a card: what each pays, one line each) |
| — 16 volatility derivatives | Part 12 |
| — 17–21 hybrids; dynamic strategies and thematic indices | Parts 19, 21, 22 (hybrids); thematic/risk-control indices → README reading note (Part 32) |
| — App. A models; B approximations (basket, ICBC inequality, digital vega) | 13–14; 5 (digital vega sign) |
| **Guyon–Henry-Labordère** (*Nonlinear Option Pricing*): ch. 9 the uncertain volatility model (parametric approach, UVM by BSDEs) *(chapter number from the publisher listing; verify)* | 13 |
| — ch. 10 McKean SDEs, particle method; calibration of LSV and local correlation | Part 13 (SLV, done); 11 (local correlation, named) |
| — BSDEs, American options, branching diffusions | Part 17 (deep BSDE), Part 16; branching → README note |
| **Wilmott PWOQF** (2nd ed.), exotics chapters *(titles from memory; verify numbers)*: introduction to exotic and path-dependent options; barrier options; strongly path-dependent options; Asian options; lookback options; miscellaneous exotics; equity and FX term sheets; uncertain parameters; static hedging | 3–6, 12, 13, 4, 1 (term sheets) |
| Gatheral *The Volatility Surface* ch. 9 barrier options (put-call symmetry, static hedge, lookbacks, discrete monitoring); ch. 10 exotic cliquets (locally capped globally floored, reverse, Napoleon) *(verify chapter numbers)* | 4, 6; 12 |
| Taleb *Dynamic Hedging*: binary options; barrier options; multi-asset options *(verify parts and chapters)* | 5, 3–4, 11 |
| Rebonato *Volatility and Correlation*: correlation chapters *(verify)* | 11 |

### (c) Papers on the Part 15 list in READING.md

| Paper | Now | Plan |
|---|---|---|
| Goldman, Sosin, Gatto (1979) | on screen | ch6 lookback card and hedge-by-reflection |
| Kemna, Vorst (1990) | on screen | ch6 lab (geometric Asian, the control variate) |
| Reiner, Rubinstein (1991) | on screen | ch3 card |
| Avellaneda, Levy, Parás (1995) | on screen | ch13 derivation |
| Lyons (1995) | on screen | ch13 |
| Derman, Ergener, Kani (1995) | **absent** | ch4: the calendar-spread construction on the barrier line |
| Broadie, Glasserman, Kou (1997) | on screen | ch4 (table + overshoot derivation) |
| Carr, Ellis, Gupta (1998) | **absent** | ch4: put-call symmetry static hedge, computed failure under skew |
| Cont (2006) | **absent** | ch14: the model-uncertainty measure on the BTC Surface |
| Henderson, Pearson (2011) | on screen | ch2 |
| Glasserman, Xu (2014) | **absent** | ch14: KL-ball worst case, computed by exponential tilting |
| Célérier, Vallée (2017) | on screen | ch2 |
| Public sources on 2024 snowballs, Korean ELS | partly | ch9, ch10 with the URLs of §4 |

**Proposed additions to READING.md Part 15.** Each is to be checked against its source; the ones not opened this
session are marked.

Classics:
- Merton (1973), *Bell J.*: the down-and-out formula.
- Margrabe (1978), *JF*.
- Stulz (1982), "Options on the minimum or the maximum of two risky assets", *JFE*.
- Johnson (1987), *JFQA*: several assets.
- Conze, Viswanathan (1991), *JF*: lookbacks.
- Rubinstein, Reiner (1991), "Unscrambling the binary code", *Risk* *(verify)*.
- Rubinstein (1991), "Somewhere over the rainbow", *Risk* *(verify)*.
- Kunitomo, Ikeda (1992), *Math. Finance*: double barriers.
- Geman, Yor (1993), *Math. Finance*: Asians by Bessel processes.
- Bowie, Carr (1994), "Static simplicity", *Risk* *(verify)*.
- Rogers, Shi (1995), *J. Appl. Prob.*: Asians.
- Avellaneda, Parás (1996), "Managing the volatility risk of portfolios of derivative securities: the Lagrangian
  uncertain volatility model", *Applied Mathematical Finance*.
- Boyer, Gibson, Loretan (1999), the bias of conditional correlations *(verify venue)*.
- Vecer (2001), "A new PDE approach for pricing arithmetic average Asian options", *J. Computational Finance*.
- Forbes, Rigobon (2002), *JF*: contagion and the conditioning bias.
- Wilmott (2002), "Cliquet options and volatility models", *Wilmott Magazine* *(verify)*.
- Hirsa, Courtadon, Madan (2003), "The effect of model risk on the valuation of barrier options", *J. Risk
  Finance* *(verify)*.
- Schoutens, Simons, Tistaert (2004), "A perfect calibration! Now what?", *Wilmott Magazine* *(verify)*.
- Carr, Lee (2009), "Put-call symmetry: extensions and applications", *Math. Finance*.
- Langnau (2010), "A dynamic model for correlation", *Risk* *(verify)*.
- Kerkhof, Melenberg, Schumacher (2010), "Model risk and capital reserves", *JBF*.
- Huge, Savine (2020), "Differential machine learning", *Risk* / arXiv 2005.02347 (shared with Part 17).

Investor side:
- Egan (2019), "Brokers versus retail investors: conflicting interests and dominated products", *JF*.
- Vokata, "Engineering lemons", working paper (Dice Center WP 2020-21; **not** confirmed as published; cite as a
  working paper).
- Calvet, Célérier, Sodini, Vallée (2023), "Can security design foster household risk-taking?", *JF* *(verify)*.

Frontier, 2023–2026, all verified on arXiv this session: see §4.

---

## 3. The chapter list (20 scenes: hook, 18 chapters, outro; about 58 min)

Conventions:
- **Visual** is the signature picture, built before the formula.
- **Live** is a simulation drawn as it runs.
- **Lab** is `lab_card` + `lab_run` with a real excerpt of the House (≤12 lines, line numbers as in
  `explainer/quant/house/exotics.py` today).
- **Replay** is a `TrainingReplay` or `ValueTracker` scrub with seeds as `seed_band`.
- **Compute** names the `compute.py` item with an estimated single-core CPU time.

Kept modules keep their names and classes. New modules are inserted with letter suffixes, so the caches of kept
scenes survive and `manifest.py` sets the order. All `chapter_card` numbers change to the new numbering.

### H · Hook: "Fifteen percent, unless" (2.8 min) · `s01_hook` (deepened)
- Goal: the puzzle, the era, the map.
- Beats:
  1. Keep the CSI 500 cliff, with the knock-in lines and the January 2024 low.
  2. **New, "how we got here" (≈60 s)**, lit on the timeline strip:
     - 1973 Merton's barrier formula;
     - 1979 Goldman–Sosin–Gatto, lookbacks;
     - 1987 the first "Asian" options, traded in Tokyo *(verify the Bankers Trust story or drop it)*;
     - 1990 Kemna–Vorst;
     - 1991 Reiner–Rubinstein. **1991 is not a timeline year: append it**, as the IMPLEMENT rules allow;
     - 1995 uncertain volatility;
     - 1997 BGK;
     - 1998 Carr–Ellis–Gupta;
     - 2016 the first HSCEI ELS scare (crisis red);
     - 2018 Natixis's Korean autocallables;
     - 2024 snowballs and the HSCEI ELS. 2024 already reads "snowballs; the yen carry unwind".
  3. The objectives card, 12 rows (the 10 items, industry, frontier).
  4. The House card: the exotics pricer.
- Pause-and-predict: "A note pays 15% a year unless the index falls a quarter. Is 15% a gift?" (No. Chapter 7 shows
  it is the price of a crash put; at 20% vol the fair coupon is ≈13%.)
- Compute: `market`, `book2024` (exist).

### 1 · Anatomy of a note, and the margin (3.0) · item 1 · `s02_business` (deepened)
- Goal: take a note apart into priced pieces; show where the coupon comes from (options, the issuer's funding) and
  where the margin sits.
- Beats:
  - **Visual, the decomposition engine.** A bar of height 100 (the issue price) splits live into stacked blocks:
    - the zero-coupon bond, discounted at the issuer's funding rate;
    - the coupon strip (a ladder of knock-out digitals, one block per month);
    - minus the down-and-in put (a block hanging *below* the axis);
    - the issuer's margin, the gap left at the top.

    Each block is computed by its own Monte Carlo on the same paths (CRN), and the blocks snap together to exactly
    the note's price.
  - Then the reverse convertible as the simplest case, with its payoff diagram: a bond line and a short put kink.
  - A funding-spread slider: widening the issuer's credit spread shrinks the bond block and frees room for the
    coupon. The buyer is paid to bear the issuer's default risk (Part 20).
  - Firm cards (kept): the buyers, the issuers.
- Derivation (ladder):
  - $\text{RC payoff} = (1+c) - (1-S_T/S_0)^+ \cdot \mathbf 1_{\{\text{put}\}}$, so $V = e^{-(r+s)T}(1+c) -
    P_{\text{fund}}(S_0;T)/S_0$. Reason: payoff algebra; the issuer discounts its own promise at its funding spread $s$.
  - Fair coupon $c^* = e^{(r+s)T}\big(1 + P/S_0\big) - 1$. Reason: set $V = 1$; the put premium and the funding
    spread both feed the coupon.
  - Snowball: $V = \underbrace{\textstyle\sum_m \mathbb E[e^{-rt_m}\mathbf 1_{\tau=m}](1+\tfrac{cm}{12})}_{\text{autocall strip}}
    + e^{-rT}\mathbb E[(1+2c)\mathbf 1_{\text{no KO, no KI}}] + e^{-rT}\mathbb E[\min(S_T,1)\mathbf 1_{\text{no KO, KI}}]$.
    Reason: the payoff splits on three disjoint events.
  - $\text{margin} = \text{issue price} - V$. Reason: the issuer's P&L at inception, before hedging costs.
    Accounting may defer it (ch17).
- Experiment: `decompose`, new.
  - The 2-year CSI 500 snowball at its fair coupon (σ = 19.98%, the 2021–23 realized vol), on 40,000 CRN paths.
  - Blocks: the bond, the KO digital strip, the full-coupon claim, the DIP. Their sum must be within MC error of 1
    (an assert of an invariant, not of a hoped-for result).
  - Fair coupon for funding spreads s = 0, 50, 100, 200 bp.
- Pause-and-predict: "The issuer's credit spread widens by 100 bp. Does the coupon it can offer rise or fall?" (Rise.
  The buyer is paid for the issuer's credit, which Lehman's note buyers learned in 2008.)
- Compute: `decompose` (2 min).

### 2 · Who buys, and what they earned (2.6) · item 1 · `s02a_buyers` (new)
- Goal: the empirical record on structured-product investors, plus our own outcome tally on the real path.
- Beats:
  - **Live, the vintage wall.** One stylized snowball (15% headline, KO 103% monthly after 3 months, KI 75% daily,
    24 months) is issued on the first trading day of every month 2017–2023 on the CSI 500 ETF.
  - Each note is a dot that rides along the real index path from its start. It turns gold when it knocks out, red
    when it ends knocked in below its strike, white if it pays the full coupon.
  - A running tally prints by vintage. Then the papers as cards with their findings:
    - Henderson–Pearson (2011, SPARQS, about 8% above fair value);
    - Egan (2019, reverse convertibles: brokers steered clients to dominated products);
    - Vokata (working paper: about 28,000 US yield-enhancement products 2006–2015; attractive yields, negative
      risk-adjusted returns; fees of about 6–7% a year, as summarised; often dominated by listed-option
      combinations) *(verify the exact figures against the working paper)*;
    - Célérier–Vallée (2017: headline rates rose with complexity);
    - Calvet, Célérier, Sodini, Vallée (2023, Swedish capital-protected products drew households into risk)
      *(verify)*.
- Derivation: $\mathbb E[R_{\text{buyer}}] = \mathbb E^{\mathbb P}[\text{payoff}]/\text{price} - 1$. Under
  $\mathbb Q$ that ratio is $1 - \text{margin}$. Under $\mathbb P$ the buyer adds the premium for selling a crash put
  (the variance risk premium of Part 12), so selling such puts **can** pay on average: the record says fees and
  complexity ate it. One honest line: one market path is not a sample of outcomes.
- Experiment: `buyers`, new. Planning run, 82 notes 2017–2023 that have matured by Nov 2025:
  - **26 ended in a loss** (worst −31.9%);
  - **mean annualised return 7.7%** (a naive average of annualised returns: show the per-vintage table, not only
    the mean);
  - every 2019 and 2020 vintage knocked out at 15%;
  - 2017: 7 of 12 lost.

  Show each vintage against holding the index over the same window, and against a 2% deposit.
- Pause-and-predict: "Notes sold near the index's top or its bottom: which did better?" (Bottom: the 2019–20
  vintages all knocked out.)
- Compute: `buyers` (<0.1 min).

### 3 · Barriers: reflection, the closed form, the PDE (3.0) · item 2 · `s03_barriers` (deepened)
- Goal: derive the barrier formula two ways (paths and PDE), see the value surface, and see why the hedge is ugly.
- Beats:
  - **Live reflection.** 60 paths are drawn one by one. Each that touches H flashes, and its post-touch mirror is
    drawn in `OPT`.
  - A side histogram of terminal values builds: the touched-and-above mass equals the mirrored-below mass.
  - **3D (ThreeDScene).** The DOC value $V(S,\tau)$ over spot 80–130 and time to expiry 0–0.5 rises from the
    payoff. The barrier is a wall at S = H where the surface is pinned to zero. The camera orbits from the front
    (vanilla-like) to the barrier edge, where the slope (delta) stays steep right up to the wall.
  - Then the delta surface in the same frame, its ridge along S = H⁺.
  - Keep the existing delta slice, 0.43 just above the barrier.
- Derivation:
  - $P(M_T \ge b,\ W_T \le x) = P(W_T \ge 2b - x)$ for $x \le b$. Reason: reflection after $\tau_b$ (strong Markov,
    symmetry).
  - With drift $\nu$: $f_{M,W}$ by Girsanov on the driftless joint density. Reason: Part 5's change of measure
    multiplies by $e^{\nu W_T - \nu^2T/2}$.
  - $DOC = C(S,K) - (H/S)^{2\lambda - 2}\, C(H^2/S, K)$ for $H \le K$, $\lambda = \frac{r-q}{\sigma^2} + \frac12$.
    Reason: integrate the payoff against the killed density.
  - PDE: $\partial_t V + \tfrac12\sigma^2S^2V_{SS} + (r-q)SV_S - rV = 0$ on $S>H$, with $V(H,t)=0$. Method of
    images: if $V$ solves BS, so does $(S/H)^{2-2\lambda}V(H^2/S, t)$. Subtract the image and the boundary condition
    holds. Reason: the image term is the same formula, seen from the PDE side.
  - In–out parity: $DIC + DOC = C$. Reason: exactly one of the two is alive at expiry.
- Lab 1: `exotics.down_out_call`, lines 19–28 (10 lines; `lam`, `y`, `din`, `out`); run it to print
  `DOC(100,100,85,0.5,0.25,0.02) = 7.28`, and the MC 7.29 ± 0.07 (from the existing `barrier` item).
- Experiment: `barrier` (exists); `barrier_surface`, new: the closed form on a 60 × 40 (S, τ) grid plus finite-
  difference delta.
- Pause-and-predict: "A down-and-in call plus a down-and-out call with the same terms is worth …?" (The vanilla.)
- Compute: `barrier` (1.5 min), `barrier_surface` (<0.1).

### 4 · Watched at the close, and hedged without trading (3.0) · item 2 · `s03a_static` (new; BGK table moves here from `s03_barriers`)
- Goal: discrete monitoring (BGK, with the reason for β), and static replication: Derman–Ergener–Kani and
  Carr–Ellis–Gupta, then where it breaks.
- Beats:
  - **Live**: a fine path with monthly monitoring ticks. Excursions below H *between* ticks are drawn in red and go
    unseen. The table builds (existing numbers: monthly 7.44, weekly 7.38, daily 7.33, continuous 7.28; BGK within
    0.01).
  - **Static hedge, visual**: the barrier line in the (t, S) plane. Derman–Ergener–Kani fill it backward with
    vanillas of decreasing maturity, each chosen to zero the portfolio on the barrier at one date. The portfolio's
    value along S = H flattens to zero, one date at a time.
  - Then Carr–Ellis–Gupta, one line: under symmetry, a down-and-in call is $K/H$ puts at $H^2/K$, held until the
    touch, then swapped.
  - **Live**: paths hit the barrier. At the touch the puts are sold and the call bought, and the ledger shows zero
    net cost under Black–Scholes. Rerun on Heston paths with ρ = −0.7: the swap at the touch leaves cash on the
    table every time.
- Derivation:
  - The overshoot of the discretely monitored walk past $H$ has limiting mean $\beta\sigma\sqrt{\Delta t}$,
    $\beta = -\zeta(\tfrac12)/\sqrt{2\pi} \approx 0.5826$. Reason: Siegmund's corrected diffusion approximation;
    the ladder-height of a Gaussian walk.
  - So $V_{\text{disc}}(H) \approx V_{\text{cont}}(He^{\mp\beta\sigma\sqrt{\Delta t}})$. Reason: shift the barrier
    away by the mean overshoot.
  - Put-call symmetry ($r = q = 0$, smile symmetric in $\log K/F$): $C(K) = \frac{K}{F}P(F^2/K)$. Reason: under
    BS, $\mathbb E[(S_T-K)^+] = \frac KF\mathbb E[(F^2/K - S_T)^+]$ by the measure change with density $S_T/F$
    (Carr–Lee).
  - At the touch $F = H$: $C(K) = \frac KH P(H^2/K)$. So holding $\frac KH$ puts struck at $H^2/K$ replicates the
    DIC. Reason: the two have equal value on the barrier and the put expires worthless if no touch
    ($H^2/K < H$).
  - Under skew ($\rho<0$), puts at $H^2/K$ trade at higher implied vol than calls at $K$, so the hedge costs more
    than the barrier is worth. Reason: symmetry fails; Carr–Lee's extension needs symmetric dynamics.
- Experiment: `static`, new. DIC, S = K = 100, H = 90, T = ½, r = q = 0, 100,000 paths, 500 steps. Planning run:
  - BS: true minus static −0.106, which is the monitoring bias alone (−0.06 at 2,000 steps).
  - Heston with ρ = 0 (v₀ = θ = 0.0625, κ = 2, ξ = 0.8): −0.118, about the same, so symmetry holds.
  - Heston with ρ = −0.7: −0.753. The skew breaks the static hedge by an order of magnitude more than the
    monitoring.

  Narration branches on the computed numbers.
- Lab: new `exotics.static_dic_hedge(K, H, F)` (returns weight and strike; 5 lines) beside the run.
- Pause-and-predict: "With a negative skew, is the put-symmetry hedge too dear or too cheap?" (Too dear.)
- Compute: `static` (2 min).

### 5 · Digitals, one-touches, and the call-spread hedge (3.0) · item 3 · `s04_digitals` (deepened; Asians move out)
- Goal: the digital's gamma explosion measured as hedging error; why desks book call spreads; the one-touch by
  reflection; the skew in a digital's price.
- Beats:
  - Keep the delta spike (0.06/0.25/0.67).
  - **Live HedgeLedger**: one path, two books side by side, both delta-hedged: a short digital and a short ε = 2
    call spread, rebalanced daily for a month. Then the P&L histograms of 40,000 paths at 21, 84 and 336 rebalances.
    Planning run:
    - P&L sd: digital 0.179 / 0.129 / 0.093; spread 0.133 / 0.077 / 0.042;
    - 1% tail: digital −0.52 / −0.45 / −0.35; spread −0.35 / −0.23 / −0.13;
    - prices: 0.486 against 0.541.

    The spread's error falls about twice as fast. The extra 0.055 is the price of a hedgeable book.
  - Then the **one-touch**: a path touching H pays at once. Reflection gives the closed form, and with zero drift it
    is exactly twice the digital. Planning run (S = 100, H = 90, ½ year, σ = 25%, r = 0): closed form 0.580, MC
    (2,000 steps) 0.571, 2 × digital 0.612.
  - Finally the **skew**: a digital is minus the slope of the call price in strike, so it carries the smile's slope.
- Derivation:
  - $D(K) = -\frac{d}{dK}C(K, \sigma(K)) = e^{-rT}N(d_2) - \mathcal V(K)\,\sigma'(K)$. Reason: the chain rule; the
    call price depends on K directly and through the smile.
  - With $\sigma'(K)<0$ (equity skew), the digital call is **dearer** than $N(d_2)$. Reason: the vega term is
    positive.
  - $\Delta_D = \frac{e^{-rT}\phi(d_2)}{S\sigma\sqrt\tau} \to \infty$ at $S=K$ as $\tau\to0$. Reason:
    differentiate $N(d_2)$.
  - Call spread $\frac{1}{\varepsilon}[C(K-\varepsilon) - C(K)] \ge D(K)$ and $|\Delta| \le 1/\varepsilon$.
    Reason: payoff dominance; the delta is bounded by the payoff's slope.
  - One-touch (down, $b = \ln(H/S)$, drift $\mu$):
    $OT = N\!\big(\frac{b - \mu T}{\sigma\sqrt T}\big) + e^{2\mu b/\sigma^2}N\!\big(\frac{b+\mu T}{\sigma\sqrt T}\big)$.
    Reason: the first-passage law of BM with drift (Part 5, reflection plus Girsanov). With $\mu = 0$ this is
    $2N(b/\sigma\sqrt T)$.
- Experiment: `digital` (exists); `digital_hedge` (new, 1.5 min); `onetouch` (new, closed form plus MC, <0.2);
  `digital_skew` (new: digital on the BTC Surface's SSVI slice at 30 days, flat-vol $N(d_2)$ against the
  skew-adjusted price, from Part 12's `surface` cache, <0.1).
- Pause-and-predict: "Equity skew. Is a digital call dearer or cheaper than Black–Scholes at the ATM vol?" (Dearer.)

### 6 · Averages and extremes: Asians and lookbacks (2.8) · item 3 · `s04a_asian` (new; content from `s04_digitals`)
- Goal: why averaging tames a payoff; Kemna–Vorst as a control variate; Shreve's change of numéraire (Vecer's
  one-dimensional PDE); lookbacks by reflection.
- Beats:
  - **Live**: a path draws with a running average (gold) and a running minimum (blue) trailing it, and the Asian and
    lookback payoffs read off at the end.
  - **The control-variate scatter**: 4,000 paths' arithmetic and geometric payoffs plotted against each other fall
    on a tight line, the regression line draws, and the residual cloud is what is left to estimate.
  - Keep the noise bar chart (÷21) and the lookback numbers (19.3 continuous, 18.5 daily: the BGK effect again).
  - Shout options as a lookback cousin, one line.
- Derivation:
  - $\log G = \frac1n\sum\log S_{t_i} \sim N\big(\log S_0 + (r-q-\tfrac{\sigma^2}{2})\bar t,\ \sigma^2\sum_{i,j}\min(t_i,t_j)/n^2\big)$.
    Reason: a linear map of a Gaussian vector.
  - In continuous time $\operatorname{Var}\log G = \sigma^2T/3$, so the effective vol is $\sigma/\sqrt3$. Reason:
    $\int\!\!\int\min(s,t) = T^3/3$. That is why Asians are cheap.
  - $\hat\theta_{cv} = \bar Y_A - b(\bar Y_G - \mu_G)$, with $\operatorname{Var} = \operatorname{Var}\bar Y_A(1-\rho^2)$.
    Reason: optimal $b = \operatorname{Cov}/\operatorname{Var}$. The measured noise ratio 21 means $\rho \approx 0.9989$.
  - Vecer / Shreve 7.5.3: with $X_t = \big(\frac1T\int_0^t S\,du - K\big)/S_t$ plus the remaining-average term,
    under the numéraire $S$ the price is $S_0\,u(0, X_0)$ with $u_t + \tfrac12\sigma^2(q(t) - x)^2u_{xx} = 0$.
    Reason: dividing by the numéraire kills one dimension (state augmentation, then reduction).
  - Lookback: $\mathbb E[S_T - \min_{t\le T}S_t]$ in closed form from the joint law of $(W_T, \min W)$. Reason:
    reflection again (Goldman–Sosin–Gatto; Conze–Viswanathan).
- Lab 2: `exotics.geometric_asian_call`, lines 69–78 (10 lines), run to print `geo 5.91 · arith(CV) 6.20 ·
  vanilla 10.87`.
- Experiment: `asian` (exists); `asian_scatter` (new, <0.1). Optional: a Vecer PDE price by `engine`'s FD
  machinery against the CV price (a new House function `asian_vecer`, ≈0.3 min) if the implementer has time;
  otherwise a card.
- Pause-and-predict: "Why is an Asian call worth about half a vanilla?" (Averaging divides the variance by about 3.)

### 7 · The snowball, priced (3.0) · item 4 · `s05_snowball` (deepened)
- Goal: price the snowball properly and see its outcome distribution; show that the fair coupon is a linear solve;
  carry and the futures basis.
- Beats:
  - The terms card (kept). **Lab 3**: `exotics.snowball_payoff`, lines 121–126 (the knock-out loop) and 127, 130–133
    (knock-in and the two maturity cases): 12 lines.
  - **Live**: 300 paths run with daily ticks. Each path freezes and turns gold at its knock-out month, turns red
    and keeps going once knocked in, and lands in one of three bins on the right.
  - A histogram of knock-out months fills beside it. Planning run (40,000 paths, σ = 19.98%, coupon 13.36%):
    - **78.4% knock out**: mean month 6.0; 38.5% at the first observation, month 3;
    - **17.6% end knocked in**: mean value 0.70 per unit;
    - 3.9% pay the full coupon;
    - expected life 9.9 months; 5% quantile of value 0.63.
  - **The fair coupon as a line**: the note's value is linear in the coupon, so draw $V(c)$ for c from 0 to 30%; it
    crosses 1 at $c^*$. Then the curve by volatility (kept: 3.9% → 26.6%).
  - **Carry**: the issuer hedges in index futures, which traded at a large discount to spot. That discount enters
    the price like a dividend yield q, and the coupon slider moves. Planning run (10,000 paths), fair coupon:
    - q = 0, 4%, 8%: **13.2%, 19.5%, 29.2%**;
    - knock-in 70/75/80%: 10.0/13.2/15.8%.

    Risk.net reported issuers blaming a narrowing CSI 500 basis (13.16% to 8.72% annualised, September to November)
    for shrinking coupons *(verify the year)*.
- Derivation:
  - $V(c) = A + cB$, with $A = \sum_m\mathbb E[e^{-rt_m}\mathbf 1_{\tau=m}] + e^{-rT}\mathbb E[\mathbf 1_{\text{alive, no KI}} + \min(S_T,1)\mathbf 1_{\text{alive, KI}}]$
    and $B = \sum_m\tfrac m{12}\mathbb E[e^{-rt_m}\mathbf 1_{\tau=m}] + 2e^{-rT}P(\text{alive, no KI})$. Reason: the
    payoff is affine in c on each event.
  - $c^* = (1 - A)/B$. Reason: one MC run gives A and B, so no bisection is needed. Replace `fair_coupon`'s
    bisection with this in a new House function `snowball_AB` (the old one stays for the test).
  - Under futures hedging, $F_t = S_te^{(r-q_{\text{eff}})(T-t)}$ with $q_{\text{eff}}$ = dividend + basis. Reason:
    the hedge earns the roll, and risk-neutral pricing with the futures forward is pricing with $q_{\text{eff}}$.
  - The coupon rises with q: a lower forward means a likelier knock-in, so the put the buyer sells is dearer.
- Experiment: `snowball` (exists); `outcomes` (new, 3 min); `coupon_q` (new: q and KI grids by the linear solve,
  2 min).
- Pause-and-predict: "What fraction of these snowballs end before maturity?" (About four in five.)

### 8 · The issuer's Greeks, in three dimensions (3.0) · item 4 · `s05a_greeks` (new; Greeks content from `s05_snowball`)
- Goal: delta, gamma and vega over (spot, time), not knocked in and knocked in; peak vega; how the Greeks are
  computed for a product with discontinuities.
- Beats:
  - **3D**, three surfaces in turn on `ThreeDAxes` (spot 0.70–1.10 × months 0–22).
    - The issuer's **delta**: a ridge that climbs toward the knock-in line and then falls off a cliff onto the
      knocked-in sheet, a second surface drawn beneath in `BAD`.
    - **Gamma**: a spike along the knock-in line and ripples at each knock-out date.
    - **Vega**: a positive hill above the barrier that shrinks with time, sliding under zero just below.

    The camera orbits each one and dollies along the knock-in line.
  - Then the existing 1D slices six months in (delta 1.7 just above KI, 1.15 below), with "peak vega" marked: spot
    slightly above the barrier at mid-life.
  - Then how the numbers are made: common random numbers and finite-difference bumps. Bump size trades bias against
    noise (a live plot of delta against h).
- Derivation:
  - $\Delta \approx \frac{V(S+h) - V(S-h)}{2h}$, error $= O(h^2) + O\big(\frac{\sigma_{MC}}{h\sqrt N}\big)$ with
    independent draws, and $O(h^2) + O\big(\frac{1}{\sqrt N}\big)$ with CRN on smooth payoffs. Reason: the Taylor
    remainder against the variance of a difference.
  - For barrier payoffs a path switches state as h crosses it, so the CRN difference has variance
    $O(1/(h N))$. Reason: an indicator jumps on a set of paths of measure $O(h)$. Hence the noisy delta near the
    knock-in, and pathwise derivatives are biased (the frontier fixes this, ch18).
  - The issuer's vega sign: $\mathcal V_{\text{issuer}} = -\mathcal V_{\text{note}} = \mathcal V_{DIP} - \mathcal V_{\text{coupon strip}}$.
    Reason: decomposition (ch1). The DIP's vega is positive and largest near the barrier; after knock-in the DIP is
    a vanilla put, deep in the money, with small vega.
- Experiment: `greeks3d` (new). Grid 15 spots × 12 months × {not KI, KI}, CRN, 10,000 paths, bumps h = 0.01 in spot
  and 1 vol point; about 1,100 MC prices. Also `bump_curve`: delta at S = 0.77 for h ∈ {0.0025 … 0.04}, 3 seeds as a
  band.
- Pause-and-predict: "Where is the issuer's vega largest: at the start, just above the knock-in, or after it?" (Just
  above it, mid-life.)
- Compute: `greeks3d` (12 min), `bump_curve` (1 min).

### 9 · January 2024: the snowballs melt (3.0) · item 4 · `s06_crash` (deepened; crisis file)
- Goal: the episode from the public record and rebuilt on the real path; what the hedgers had to trade.
- Beats:
  - The record cards:
    - Bloomberg (11 Jan 2024): about **$13 bn** of snowballs near their loss triggers;
    - Caixin, citing Bloomberg and Securities Association of China data: about **$27 bn** outstanding onshore at
      the end of July 2023;
    - Risk.net: on 22 January the CSI 500 fell **4.7%** to a four-year low, with up to a third of products at
      knock-in;
    - Asia Financial: the UBS estimate of about $50 bn *(verify the UBS attribution)*;
    - Bloomberg (24 April 2024): China told brokers to limit exposure to snowballs *(headline verified; body to
      verify)*.
  - **Live** (kept, made live): the 36-note book on the real path. Notes knock in one by one from 22 January (11
    by 5 February). The dealers' delta (surrogate) climbs from 15 to 25 notes' worth of futures, then is cut to 15
    at the low.
  - **New**: the book's gamma as a bar under each day, i.e. what the hedgers had to buy on the way down and sell at
    the knock-ins, per 1% move.
  - Keep the debate (Risk.net against the sceptics), labelled as reports.
- Derivation: hedge trade on day $t$: $\Delta N_t \approx \Gamma^{\text{book}}_t\,\Delta S_t + \sum_{i\in KI_t}
  (\Delta_i^{-} - \Delta_i^{+})$. Reason: Taylor for the continuous part, plus a jump in each note's delta at its
  knock-in.
- Experiment: `book2024` (exists; add the per-day gamma from the surrogate by second differences).
- Pause-and-predict: "As the index fell toward the barriers, did the hedgers buy or sell?" (Buy, then sell at the
  knock-ins.)
- Compute: `book2024` (+0.5 min).

### 10 · Korea's ELS, twice, and a dealer's loss (3.0) · item 4 · `s07_korea` (deepened; firm file)
- Goal: the same product on the HSCEI in two episodes; the buyer's and the dealer's sides.
- Beats:
  - **Live**: the HSCEI 2015–2025. 2015 vintages are issued monthly and run into February 2016 (new, computed).
    Then the 2021 vintages (kept: 6 of 12 knocked in, losses 38–54% at maturity in 2024).
  - Record cards:
    - about **18.8 tn won** outstanding in Dec 2023 per the March 2024 press. The scene's "19.3 tn" is to be
      checked against the FSS release and corrected;
    - **1.2 tn won** lost in Jan–Feb 2024 and a projected 4.6 tn for the year (FSS plan, 11 March 2024, as
      reported by JoongAng Daily);
    - the compensation scheme; banks repaid part of losses, around 40% by industry estimate;
    - in November 2025 the FSS sent preliminary penalty notices of about **2 tn won** to five banks (KB Kookmin,
      Shinhan, Hana, NH NongHyup, SC; 15.9 tn won sold). The final amount was reported differently later, so it
      is **unverified; say "proposed"**.
  - **Firm file: Natixis.** On 18 Dec 2018 Natixis disclosed a **€259–260 m** hit (a €100 m revenue reduction plus
    a €160 m provision) on Asian equity derivatives, i.e. autocallables sold to Korean investors. It said its
    hedging model had proved "deficient" in the market conditions, and it stopped creating the notes.
- Derivation: the step-down schedule as a sequence of digitals at the 6-month dates; the KI put at 50%. In
  $\mathbb P$ terms: a step-down sold near a peak inherits the index's drawdown distribution (one line), so vintage
  matters more than terms.
- Experiment: `korea` (exists); `korea2015` (new, the same function with 2015 issuance, <0.1).
- Pause-and-predict: "Two notes with identical terms, issued four months apart. Why opposite outcomes?" (Their
  barriers sit at different index levels.)

### 11 · Worst-of, correlation, and the correlation skew (3.0) · item 5 · `s08_correlation` (deepened)
- Goal: price several-asset payoffs by numéraire change; see the dealer's correlation exposure; see correlation move
  when it matters.
- Beats:
  - **3D**: the worst-of put payoff $(K - \min(S_1,S_2))^+$ as a folded surface over $(S_1,S_2)$, the crease along
    the diagonal.
  - A cloud of 2,000 terminal points is scattered on the floor. As ρ slides from −0.2 to 1 the cloud collapses onto
    the diagonal, and the price bar beside it falls (kept: 0.169 → 0.115; measured ρ = 0.46).
  - Then **correlation regimes**, computed from the cached ETFs. Planning run:
    - CSI 500 vs CSI 1000: 0.76 in 2021–23, **0.91 in Jan–Feb 2024**, 0.985 in Feb–Mar 2020;
    - CSI 500 vs HSCEI: 0.46 in 2021–23, 0.60 in Jan–Feb 2024, 0.71 in Feb–Mar 2020.

    Caution card: correlations conditioned on big moves are biased upward even with constant ρ (Boyer–Gibson–
    Loretan; Forbes–Rigobon). The planning run's "big-down-day" correlation (0.30 against 0.23 on up days) is shown
    only with that caveat.
  - Then the **worst-of snowball** on CSI 500 and CSI 1000: the fair coupon rises as ρ falls.
  - Correlation skew and local correlation as a card: Langnau (2010), Guyon's local correlation (GHL).
  - The mountain-range family as a one-line card each (Altiplano, Himalaya, Everest; Bouzoubaa–Osseiran ch. 15).
  - Dispersion → Part 11.
- Derivation:
  - Margrabe: $\mathbb E^{\mathbb Q}[e^{-rT}(S_1 - S_2)^+] = S_2(0)\,\mathbb E^{\mathbb Q^{(2)}}[(S_1/S_2 - 1)^+]$.
    Reason: change to the numéraire $S_2$ (Part 9).
  - $S_1/S_2$ is a $\mathbb Q^{(2)}$-martingale with vol $\sigma^2 = \sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2$.
    Reason: Itô for a ratio (Part 5).
  - $\min(S_1,S_2) = S_1 - (S_1 - S_2)^+$. Reason: algebra. So the "minimum asset" is priced by Margrabe; the
    worst-of put needs the bivariate normal (Stulz 1982), shown as a card.
  - $\frac{\partial V}{\partial\rho} = \mathbb E\big[\int_0^T \sigma_1\sigma_2 S_1S_2\,\partial_{12}V\,dt\big]$.
    Reason: the cross-gamma is what correlation buys, as vega is what volatility buys.
- Experiment: `worstof` (exists); `corr_regimes` (new, <0.1); `worstof_ac` (new: worst-of snowball on CSI 500 and
  CSI 1000 at their 2021–23 vols, fair coupon by linear solve for ρ ∈ {0.3, …, 1.0}, 2 min).
- Pause-and-predict: "Correlation jumps to one in a crash. Does the issuer, long the worst-of put, gain or lose?"
  (Loses: the put cheapens; the issuer is short correlation.)

### 12 · Cliquets and forward-starts: the risk vega cannot see (3.0) · item 6 · `s08a_cliquet` (new)
- Goal: price forward-starts by homogeneity; cliquets as strips of them; why a cliquet's vega can be zero while its
  volatility risk is not.
- Beats:
  - **Live**: a 12-month path. At each monthly reset a new mini-axis is struck at the current level. That month's
    return is clipped between the floor and cap (drawn as a band) and drops into a running sum, with the global
    floor shown at the end.
  - **3D**: the price surface over (σ from 5% to 50%, local cap from 1% to 6%) for the locally capped and floored
    cliquet. A **ridge** runs through it where $\partial V/\partial\sigma = 0$, and the camera rides along the ridge.
    Planning run (12 monthly periods, cap 3%, floor −3%, global floor 0, 200,000 paths): price 0.0192, 0.0283,
    0.0311, 0.0321, **0.0323**, 0.0321, 0.0311, 0.0298 at σ = 5, 10, 15, 20, 25, 30, 40, 50%. It is flat from 20 to
    30%, so vega ≈ 0 there.
  - With no local floor and cap 2% the price only falls with vol (0.0152 → 0.0007). The **reverse cliquet**
    $(C + \sum\min(r_i,0))^+$ is short vol steeply (C = 30%: 0.231 → 0.005).
  - Then Part 13's computed fact (re-quoted from its cache, not recomputed): the same cliquet under five models
    fitted to one Surface differs by 7.8%. Model risk where Black–Scholes vega says there is none.
  - Napoleons, one line.
- Derivation:
  - $\text{FS}_0 = \mathbb E[e^{-rt_2}(S_{t_2} - \alpha S_{t_1})^+] = S_0e^{-qt_1}\,C^{BS}(1,\alpha,t_2-t_1)$.
    Reason: homogeneity of degree 1 and independent increments. The price depends only on the forward vol between
    $t_1$ and $t_2$.
  - Cliquet $= \mathbb E[\max(\sum_i \min(\max(r_i, f), c), F)]$. Reason: a strip of capped and floored forward
    returns with a global floor; not a sum of forward-starts because of the global floor.
  - $\frac{\partial V}{\partial\sigma} = 0$ at the ridge, but $\frac{\partial^2V}{\partial\sigma^2} < 0$ (volga).
    So a model with random vol prices it lower: $\mathbb E[V(\sigma)] \le V(\mathbb E\sigma)$ by Jensen. Reason:
    concavity in σ (Wilmott 2002 *(verify)*; Bergomi's smile dynamics, Part 13).
- Experiment: `cliquet` (new: σ × cap grid, 3 product variants, 200,000 paths, ≈1 min); reuse `quant13` `exotics`
  (cache read only).
- Pause-and-predict: "A cliquet's Black–Scholes vega is zero. Is it immune to volatility?" (No: it is concave in
  σ, so random vol lowers its price.)

### 13 · Uncertain volatility: the price of not knowing (3.0) · item 7 · `s09_uvm` (deepened)
- Goal: derive the Black–Scholes–Barenblatt equation; watch it solve; show non-linearity and hedging with vanillas.
- Beats:
  - **Live 3D**: the PDE marches backward from expiry on (S, t). The surface $V(S,t)$ grows out of the call-spread
    payoff while the floor beneath is painted by the volatility the worst case chooses: `BAD` where Γ > 0 (σ_max),
    `GOOD` where Γ < 0 (σ_min). The boundary between the colours (Γ = 0) drifts as time runs back.
  - Then the bounds (kept: [0.31, 0.62] against BS 0.45–0.48).
  - **Non-additivity**, computed (planning run): the upper prices of the two legs separately sum to **1.0005**,
    against **0.623** for the spread as one book. Netting gamma is worth 0.38 per unit.
  - **Lagrangian UVM** (Avellaneda–Parás 1996): buy or sell 90 and 110 calls at their market (BS 25%) prices to
    minimise the worst case. The bounds tighten to **[0.412, 0.520]** with weights ≈ (+0.06, −0.06) (planning run,
    Nelder–Mead, 80 PDE solves). A small replay of the optimiser: the upper bound falling as the weights move.
- Derivation:
  - Seller's worst case: $\sup_{\sigma_t\in[\underline\sigma,\bar\sigma]}\mathbb E[e^{-rT}g(S_T)]$. Reason: the
    seller must hedge against the adversarial volatility path.
  - Dynamic programming: $\partial_tV + \sup_{\sigma}\{\tfrac12\sigma^2S^2V_{SS}\} + rSV_S - rV = 0$. Reason: the
    HJB of a control problem with σ as the control (Part 8).
  - $\sup$ is attained at $\sigma = \bar\sigma$ if $V_{SS}>0$, $\underline\sigma$ if $V_{SS}<0$. Reason: linear in
    $\sigma^2$, maximised at an endpoint (BSB).
  - $U(g_1+g_2) \le U(g_1) + U(g_2)$. Reason: the sup of a sum is at most the sum of the sups; equality only if both
    legs pick the same σ everywhere.
  - Lagrangian: $U^\lambda(g) = \min_\lambda\big\{U(g - \sum\lambda_iC_i) + \sum\lambda_i C_i^{\text{mkt}}\big\}$.
    Reason: the static vanillas are hedged at known prices, so only the residual bears the worst case.
- Lab 4: `exotics.uvm_price`, lines 211–215 (the Γ estimate and the σ switch, 5 lines) plus 207–210 (setup), run
  to print `upper 0.62 · lower 0.31`.
- Experiment: `uvm` (exists); `uvm_book` (new: legs, joint, Lagrangian with iterates stored, ≈2 min); `uvm_film`
  (new: V and the σ map stored every 10 of 400 steps, <0.2).
- Pause-and-predict: "Is the worst-case price of a book the sum of its parts?" (No. Netting gammas makes it
  cheaper.)

### 14 · Same vanillas, different exotics: measuring model risk (3.0) · item 8 · `s09a_modelrisk` (new)
- Goal: quantify model uncertainty on the Surface; Cont's measure; Glasserman–Xu's worst case.
- Beats:
  - **Visual**: four path fans (LV, Heston, Bates, VG), all fitted to the BTC Surface of 10 Dec 2025 (Part 13's
    calibrations). Each fan is in its own colour.
  - Left panel: their 90-day smiles land on the same market dots. Right panel: bars of four exotics split apart as
    each fan's paths are scored live. Planning run (20,000 paths, 120 days, zero rates, per unit spot):

    | | LV | Heston | Bates | VG |
    |---|---|---|---|---|
    | 90-day ATM call | 0.0881 | 0.0883 | 0.0888 | 0.0940 |
    | down-and-out call (H = 0.8) | 0.0856 | 0.0831 | 0.0843 | 0.0927 |
    | one-touch 0.8 | 0.323 | 0.320 | 0.312 | 0.329 |
    | double-no-touch (0.8, 1.25) | **0.448** | 0.492 | **0.500** | 0.420 |
    | 4-month BTC autocall, fair coupon | **45.2%** | 39.9% | **38.7%** | 40.6% |

    The vanillas agree within 1% except VG (6% off at 90 days: say so). The double-no-touch spreads 19% and the
    autocall coupon 6.5 points.
  - Then **Glasserman–Xu**: the snowball's paths re-weighted by exponential tilting toward its losses. Opacity
    tracks the weight, as in Part 5's Girsanov picture. The worst-case price falls as the relative-entropy budget η
    grows, drawn as a curve.
- Derivation:
  - Cont (2006): $\mu(X) = \sup_{Q\in\mathcal Q}\mathbb E^Q[X] - \inf_{Q\in\mathcal Q}\mathbb E^Q[X]$ over models
    consistent with the calibration instruments. Reason: a coherent measure of model uncertainty; it is 0 for
    traded vanillas.
  - $\sup\{\mathbb E^Q[V] : D(Q\|P)\le\eta\}$. Lagrangian: $\frac{dQ_\theta}{dP} = \frac{e^{\theta V}}{\mathbb E
    e^{\theta V}}$. Reason: entropy duality (Donsker–Varadhan), the optimum is an exponential tilt.
  - $\eta(\theta) = \theta\,\mathbb E_{Q_\theta}[V] - \log\mathbb E e^{\theta V}$. Reason: plug the tilt into
    $D(Q\|P)$; solve for θ, then the worst price is $\mathbb E_{Q_\theta}V$.
  - Reserve $= \text{model price} - \text{worst plausible price}$ (seller). Reason: what the desk holds back (ch17).
- Experiment: `modelrisk` (new; reads `quant13` `calibrate` and calls its path simulators with 20,000 paths, ≈1.5
  min; must not modify Part 13's cache); `robust` (new: KL tilt for the CSI 500 snowball on the `outcomes` paths,
  η grid, <0.2).
- Pause-and-predict: "Which is most model-dependent: the one-touch, the double-no-touch or the autocall?" (The
  autocall's coupon and the DNT; the one-touch is pinned by the skew.)

### 15 · Dealer flows: when the hedges move the market (2.8) · item 9 · `s09b_flows` (new)
- Goal: aggregate the issuers' Greeks of a stylized book on the real path; show the vega supply and peak vega;
  separate mechanism (arithmetic) from contested magnitudes.
- Beats:
  - **Live**: the CSI 500 path 2021–2024 runs left to right. Under it, a strip shows the stylized book's aggregate
    vega and gamma per 1% (notes issued monthly, 2021–23, standard terms), computed day by day from a (spot,
    months, KI) table.
  - As spot rallies notes knock out and vega vanishes; as spot sinks toward the barriers vega peaks, then collapses
    at the knock-ins.
  - **The vega-supply picture**, labelled *schematic*: an implied-vol term structure whose long end is pushed down
    by arrows labelled "issuers sell vega".
  - The practitioner record, labelled as reports: Risk.net on autocallable issuance weighing on Euro Stoxx long-
    dated vol and on "peak vega"; SRP on long-dated vol in Japan *(verify the dates of each)*.
  - The Korea and Natixis link (ch10): a hedging model's vega and correlation assumptions failing together.
- Derivation:
  - Book vega $\mathcal V_t = \sum_i N_i\,\mathcal V(S_t/S_{0,i},\ t - t_{0,i},\ KI_{i,t})$. Reason: linearity over
    notes, each priced from the table.
  - The vega issuers must sell to stay flat, $\approx \mathcal V_t$ at the maturities of the notes' expected lives
    (≈10 months to 2 years: ch7). Reason: matching vega by bucket.
  - The daily futures trade $\approx \Gamma_t S_t\,\Delta S_t$. Its price impact is $\propto
    \sigma\sqrt{Q/V}$ (Part 37's square root, named). Reason: whether hedging moves the market depends on Q/V, which
    the record disputes.
- Experiment: `book_vega` (new: vega and gamma tables on a 19 × 12 × 2 grid by CRN finite differences, 6,000 paths;
  then the daily aggregation over 2021–2024; ≈10 min).
- Pause-and-predict: "When is the dealers' aggregate vega largest: after a rally, or just before the barriers
  break?" (Just before.)

### 16 · A neural pricer for the book, trained on screen (3.0) · item 10 · `s10_surrogate` (deepened)
- Goal: train the surrogate as a replay with seeds, compare it fairly, and say honestly when a network is not
  needed.
- Beats:
  - **Replay** (`TrainingReplay`). The right panel shows test RMSE against 40,000-path MC on 150 fresh notes, three
    seeds as a band. The left panel shows the network's price curve over spot at month 6 (not KI and KI), morphing
    from noise onto the MC dots.
  - Planning run, test RMSE at steps 0, 100, 300, 1,000, 2,000 and 4,000 (three seeds):

    | seed | 0 | 100 | 300 | 1,000 | 2,000 | 4,000 |
    |---|---|---|---|---|---|---|
    | 0 | 0.89 | 0.064 | 0.050 | 0.044 | 0.027 | **0.016** |
    | 1 | 0.98 | 0.061 | 0.051 | 0.040 | 0.027 | **0.025** |
    | 2 | 0.96 | 0.056 | 0.049 | 0.042 | 0.027 | **0.025** |

  - Then the **equal-data baseline**: a degree-4 polynomial in (log S, months), separate by KI flag, gets **0.011**,
    and the labels' own MC noise is ≈0.010.
  - **Narration branches.** At three inputs the polynomial wins. The network's case is many inputs: a worst-of on
    three assets with the vol surface as input (Sharma et al. 2024 report 250× faster than MC for three underlyings;
    Hull and co-authors' exotic-valuation network), where polynomials explode combinatorially.
  - Keep the speed (≈0.4 µs against ≈3 s).
  - **Lab 5**: the training loop (`compute.py` `compute_surrogate`, the 8 lines from `opt = …` to `opt.step()`).
- Derivation:
  - $\mathbb E\|f_\theta - y\|^2 = \mathbb E\|f_\theta - V\|^2 + \mathbb E\|V - y\|^2$. Reason: the MC label noise
    is independent with mean zero, so the network can beat the label noise against the **true** price (it averages
    neighbours). The test target (40,000 paths) has noise ≈0.003.
  - Polynomial count: $\binom{d+p}{p}$ terms at degree p in d inputs. Reason: why a fixed basis stops scaling past a
    few inputs, and a network does not.
  - The hedge from the surrogate: $\Delta = \partial_Sf_\theta$ by autograd. Reason: ch9 used it. A smooth network
    has a smooth delta even where MC bumps are noisy (ch8).
- Experiment: `surrogate` (exists; **change it to save Xtr, ytr, Xte, yte** to the cache so the replay reuses
  them; the data generation took 938 s on a loaded machine); `surrogate_replay` (new: 3 seeds, test RMSE every 100
  steps, price curves at 6 checkpoints, poly-4 baseline; ≈3 min once the data are cached).
- Pause-and-predict: "Labels carry MC noise of 0.01. Can test error against the true price fall below 0.01?" (Yes.)

### 17 · Industry: how desks mark, reserve and report exotics (2.8) · `s11a_industry` (new)
- Goal: what banks and regulators actually require, from the public record; the House's Rule 15.
- Beats (cards and live objects, each with its source on screen):
  1. **Prudent valuation.** EU Commission Delegated Regulation 2016/101 requires additional valuation adjustments
     for, among others, model risk and close-out costs. It is the regulatory twin of ch14's reserve. Visual: the
     model price, the range of plausible models, the AVA as the bar's top.
  2. **Day-one profit.** Under IFRS 9 (B5.1.2A), a gain at inception is recognised only if the fair value is
     evidenced by a quoted price or observable inputs. Otherwise it is deferred, which is why the margin of ch1 is
     not booked on day one for a Level 3 note *(verify the paragraph reference)*.
  3. **Capital.** FRTB's residual risk add-on for exotic and path-dependent payoffs (Basel MAR23 *(verify)*). Zeron,
     Wu and Ruiz (2023) cut the cost of FRTB-IMA expected shortfall for equity autocallables by about 90% with
     Chebyshev "sliding" proxies, passing the P&L attribution tests.
  4. **Conduct.** EU PRIIPs (Regulation 1286/2014) key information documents for packaged products; FINRA's notices
     on complex products *(verify numbers and dates)*; Korea's FSS penalties (ch10).
  5. **Model validation.** SR 11-7 superseded by SR 26-2 (17 April 2026; verified in the Part 5 plan). Natixis 2018
     as the case of a hedging model that failed (ch10).
  6. **The House**: Rule 15 (kept from `s11_house`). Price every note under at least two models and hold a reserve
     for the gap; simulate the hedge through the worst path on record, including the barrier day. The House's test
     table is shown as the validation report.
- Experiment: none new; reuse ch14's spread as the AVA illustration.
- Pause-and-predict: "Why can a bank not book the margin on day one?" (The fair value rests on unobservable inputs.)

### 18 · Frontier, 2023–2026 (2.6) · `s11b_frontier` (new)
- Goal: where exotics computation is going, with one hands-on check.
- Beats:
  - **Hands-on**: the pathwise delta of a digital is zero on every path, which biases differential ML and AAD.
  - **Live**, three estimators of a 1-month digital's delta converge as paths are added:
    - pathwise: stuck at 0;
    - likelihood ratio: noisy, unbiased;
    - pathwise plus Lakshtanov's boundary correction: unbiased, low noise.

    All three are against the exact $\phi(d_2)/(S\sigma\sqrt T)$, with 5 seeds as bands.
  - Then cards, every one verified on arXiv this session:
    - Glasserman, Karmarkar (2025), "Differential ML with a Difference" (arXiv 2512.05301): pathwise labels are
      biased for digitals and barriers; likelihood-ratio labels, and a hybrid with gamma, cut test errors.
    - Lakshtanov (2026), "Unbiased Monte Carlo Greeks for Discontinuous Payoffs" (arXiv 2609.06137): pathwise AAD
      plus boundary corrections for barriers, autocallables and digitals.
    - Lopez-Piqueres, Acharya, Sun, Kumar (2026), "Functional Tensor Trains for High-Order Greeks and Exposure Tails
      of Multi-Asset Structured Products" (arXiv 2610.42119): worst-of autocallables, third-order Greeks without
      sampling noise.
    - Zeron, Wu, Ruiz (2023), FRTB-IMA for equity autocallables (arXiv 2305.06215).
    - Sharma, Chen, Noh, DeJesus, Schlener (2024), distributional RL for hedging portfolios of autocallables (arXiv
      2407.10903) and ML pricing of 3-asset autocallables (arXiv 2411.01121; ACM ICAIF 2024).
    - Cibrario et al. (2025), quantum pricing of autocallables, ≈50× lower T-depth for the payoff (arXiv
      2507.19039). Say plainly: no advantage on today's hardware (Part 16).
    - Higgins (2026), stochastic spot/vol correlation (double Heston) and FX barrier pricing (arXiv 2602.01376).
    - Fukasawa (2026), short-term barrier price expansion (arXiv 2610.00340).
    - Goudenège, Molent, Zanette (2025), uncertain volatility for cliquet-style equity-indexed annuities (arXiv
      2502.10300).
    - Che, Lim, Sun (2026), multi-period multi-asset martingale optimal transport (arXiv 2602.02996): model-free
      bounds for multi-asset exotics (Part 9's MOT).
- Derivation: for $F = \mathbf 1_{\{S_T>K\}}$, $S_T = S_0e^{\cdots+\sigma\sqrt TZ}$:
  - pathwise $\partial_{S_0}F = 0$ a.s. Reason: an indicator is flat almost everywhere;
  - LR: $\partial_{S_0}\mathbb E F = \mathbb E[F\cdot\frac{Z}{S_0\sigma\sqrt T}]$. Reason: differentiate the density,
    not the payoff;
  - the boundary term is $[F]\,\phi(z^*)\,\partial_{S_0}z^*$. Reason: the jump times the density at the boundary
    times the boundary's speed. It is the missing term.
- Experiment: `pathwise_digital` (new, <0.2).
- Pause-and-predict: "AAD gives a digital's delta as zero. Bug or feature?" (A known bias of pathwise derivatives.)

### O · The House, recap, desk questions, problems (2.6) · `s12_outro` (deepened; absorbs `s11_house`)
- House card: the exotics pricer lit, with Rule 15 and the trial counter (unchanged: no strategy is tested; read
  `envelope`).
- Recap in 12 lines; payoff card (Parts 16, 17, 20, 21, 37, 41); reference card.
- Desk questions (README has the solutions):
  - keep "a digital as a call spread";
  - keep "the snowball issuer's vega";
  - replace the worst-of question with **"Price a one-touch with zero drift, given the digital."** (Twice the
    digital, by reflection.) The worst-of question moves into the README as a fourth.
- Problems: the existing 5, plus:
  - (6) "show the snowball's value is affine in the coupon and solve for c*";
  - (7) "price a chooser with parity";
  - (8) "derive Margrabe by the numéraire $S_2$".

  On screen, ≈90 s; English and Chinese solutions in the README.

### Minutes

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.8 | 10 Korea, Natixis | 3.0 |
| 1 Anatomy | 3.0 | 11 Correlation | 3.0 |
| 2 Buyers | 2.6 | 12 Cliquets | 3.0 |
| 3 Barriers | 3.0 | 13 UVM | 3.0 |
| 4 Static/BGK | 3.0 | 14 Model risk | 3.0 |
| 5 Digitals | 3.0 | 15 Flows | 2.8 |
| 6 Asians | 2.8 | 16 Surrogate | 3.0 |
| 7 Snowball | 3.0 | 17 Industry | 2.8 |
| 8 Greeks 3D | 3.0 | 18 Frontier | 2.6 |
| 9 January 2024 | 3.0 | Outro | 2.6 |
| | | **Total** | **≈ 58.0** |

That is about 8,060 spoken words at 139 words a minute. The 50-minute floor leaves 8 minutes of slack.

---

## 3b. Hands-on summary

**Labs (`lab_card` + `lab_run`, ≤12 lines, real House code):**

| # | Chapter | Excerpt | Run output (from cache) |
|---|---|---|---|
| 1 | 3 | `exotics.down_out_call`, lines 19–28 | `DOC 7.28 · MC 7.29 ± 0.07` (`barrier`) |
| 2 | 6 | `exotics.geometric_asian_call`, lines 69–78 | `geo 5.91 · arith(CV) 6.20 · vanilla 10.87` (`asian`) |
| 3 | 7 | `exotics.snowball_payoff`, lines 121–127 and 130–133 | `P(KO) 0.78 · P(loss) 0.18 · c* 13.4%` (`outcomes`) |
| 4 | 13 | `exotics.uvm_price`, lines 207–215 | `upper 0.62 · lower 0.31 · hedged [0.41, 0.52]` (`uvm`, `uvm_book`) |
| 5 | 16 | `compute_surrogate` training loop (8 lines) | the RMSE per seed (`surrogate_replay`) |
| (6) | 4 | new `exotics.static_dic_hedge` (5 lines) | `K/H = 1.11 puts at 81 · BS gap −0.11 · skew gap −0.75` (`static`) |

Line numbers refer to `exotics.py` today. If functions are appended above them, re-read the ranges.

**Replays (fits and training shown learning):**
- ch16 surrogate: 3 seeds as `seed_band`, poly-4 baseline dashed, MC-noise floor dotted.
- ch13 Lagrangian UVM: the Nelder–Mead iterates of the vanilla weights with the upper bound falling, stored with a
  callback.
- ch8 bump-size curve: delta against h, 3 seeds.
- ch7 the coupon line $V(c)$ drawn from the A, B of one run (not a fit, a solve; say so).
- ch14 tilt: the worst-case price as η grows (a ValueTracker on η re-weighting path opacities).

**Live simulations:**
- ch2 the vintage wall;
- ch3 reflection;
- ch4 unseen excursions and the static swap at the touch;
- ch5 the digital and call-spread ledgers;
- ch6 running average and minimum;
- ch7 snowball paths freezing at knock-out and reddening at knock-in;
- ch9 the 2024 book knocking in;
- ch10 HSCEI vintages;
- ch11 the correlated cloud collapsing;
- ch12 cliquet resets;
- ch13 the BSB PDE marching back;
- ch15 book vega along the real path;
- ch18 three delta estimators converging.

**3D:**
- ch3 DOC value and delta surfaces with the barrier wall;
- ch8 the issuer's delta, gamma and vega surfaces over (spot, months), not KI and KI;
- ch11 the worst-of payoff over $(S_1,S_2)$ with the correlated cloud;
- ch12 the cliquet price over (σ, cap) with the zero-vega ridge;
- ch13 $V(S,t)$ with the σ-choice map painted on the floor.

**Compute (seeded, cached per item, ≈ 80 CPU-min of 120 on an idle core; the machine was loaded during planning):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| market* | 0.1 | snowball* | 8 | worstof_ac | 2 |
| decompose | 2 | outcomes | 3 | cliquet | 1 |
| buyers | 0.1 | coupon_q | 2 | uvm*, uvm_film | 0.7 |
| barrier*, barrier_surface | 1.6 | greeks3d | 12 | uvm_book | 2 |
| static | 2 | bump_curve | 1 | modelrisk | 1.5 |
| digital*, digital_hedge | 1.6 | book2024* (+gamma) | 1.5 | robust | 0.2 |
| onetouch, digital_skew | 0.3 | korea*, korea2015 | 0.1 | book_vega | 10 |
| asian*, asian_scatter | 2 | worstof*, corr_regimes | 0.6 | surrogate* (re-run to save data) | 8–16 |
| pathwise_digital | 0.2 | surrogate_replay | 3 | envelope* | 0 |

(* exists.)
- `greeks3d`, `book_vega` and `surrogate` are the long ones: run them under `nice -n 10` with `nohup` and a log, and
  cache them per item. `greeks3d` should cache per month row (`CACHE.partial`) so it resumes.
- `modelrisk` imports `videos.quant.quant13.compute` and reads its cache. It needs `.cache/quant13/calibrate.json`
  present; it must never write to it.
- One command rebuilds the part: `python -m videos.quant.quant15.compute`.
- The trial counter: nothing is registered (no strategy is backtested); `buyers` is descriptive, one path, and says so.

---

## 4. Industry and frontier: sources (checked 2 Nov 2026)

| Fact | Source | Status |
|---|---|---|
| Bloomberg, 11 Jan 2024: "China 'Snowball' Derivatives Worth $13 Billion Near Loss Levels"; CICC said spillover could be limited | https://www.bloomberg.com/news/articles/2024-01-11/china-snowballs-worth-13-billion-seen-nearing-loss-triggers | headline and lede verified |
| Onshore snowballs ≈ $27 bn at end-July 2023 (SAC data, via Bloomberg); CICC average CSI 500 knock-in ≈ 4,865 | https://www.caixinglobal.com/2023-10-27/china-selloff-threatens-27-billion-of-snowball-derivatives-102121130.html | verified (secondary, citing SAC) |
| CSI 500 −4.7% on 22 Jan 2024, up to a third of products at knock-in; issuers' re-hedging said to add to the futures sell-off | https://www.risk.net/derivatives/7958855/china-snowball-knock-ins-fuel-futures-sell-off | summary verified (paywall) |
| UBS estimate ≈ $50 bn market | https://www.asiafinancial.com/losses-on-50bn-leveraged-products-behind-china-stocks-plunge | *(verify UBS attribution in body)* |
| CSI 500 basis narrowed 13.16% → 8.72% annualised (6 Sep → 4 Nov), issuers blaming it for smaller coupons | https://www.risk.net/derivatives/7894576/sales-of-chinas-snowball-notes-fall | *(verify year: 2023 expected)* |
| China tells brokers to limit exposure to snowballs (24 Apr 2024) | https://www.bnnbloomberg.ca/china-tells-brokers-to-limit-exposure-to-snowball-derivatives-1.2063133 | headline only *(verify body)* |
| Snowball issuers hit by the slump | https://risk.net/derivatives/7939391/china-stock-slump-hits-snowball-issuers | *(verify contents)* |
| FSS compensation plan, 11 Mar 2024; 1.2 tn won lost Jan–Feb 2024; 4.6 tn projected; ≈18.8 tn won outstanding Dec 2023 | https://www.koreajoongangdaily.com/business/hk-tied-els-sellers-could-face-full-compensation-for-investor-losses/11969702 | verified (press); FSS release to cite directly *(verify)* |
| FSS preliminary penalties ≈2 tn won to KB, Shinhan, Hana, NH, SC (28 Nov 2025); 15.9 tn won sold | https://www.koreajoongangdaily.com/business/koreas-financial-regulator-issues-2-trillion-won-in-penalties-to-five-banks-for-els-mis-selling/12248418 | verified as *preliminary*; final amount conflicting in 2026 reports (*unverified*) |
| Natixis: €259 m (≈€260 m) Asian equity derivatives hit, 18 Dec 2018: €100 m revenue reduction plus €160 m provision; Korean autocallables; hedging model "deficient"; stopped creating them | https://newsroom-en.groupebpce.fr/news/natixis-confirms-its-strategic-ambitions-and-the-payment-of-a-eur1-5bn-special-dividend-despite-negative-non-recurring-items-in-4q18-d78f-53927.html ; https://natixis.groupebpce.com/wp-content/uploads/2022/08/natixis_4q18.pdf ; https://www.structuredretailproducts.com/news/details/74627 | verified (company release; press) |
| Autocallable issuance and long-dated vol; peak vega | https://risk.net/node/2421792 ; https://risk.net/derivatives/7505201/autocalls-hit-peak-vega-where-hedging-costs-mount ; https://structuredretailproducts.com/news/77045/socit-gnrale-long-dated-implied-vol-in-japan-under-pressure | practitioner reports; *(verify dates)*; present as reports |
| Vokata, "Engineering lemons", Dice Center WP 2020-21: 28,000+ YEPs 2006–2015, attractive yields, negative returns; fees ≈6–7%/yr (as summarised) | https://ideas.repec.org/p/ecl/ohidic/2020-21.html | working paper; figures *(verify in the paper)* |
| Bouzoubaa–Osseiran TOC (chapters 2, 7–15 as in §2b) | https://wiley-vch.de/en/areas-interest/finance-economics-law/exotic-options-and-hybrids-978-0-470-68803-8 | verified |
| Guyon–Henry-Labordère: UVM chapter (parametric approach, UVM by BSDEs); McKean SDEs; LSV and local correlation calibration | https://www.routledge.com/Nonlinear-Option-Pricing/Guyon-Henry-Labordere/p/book/9781466570337 | verified from a listing; chapter numbers *(verify)* |
| SR 26-2 supersedes SR 11-7 (17 Apr 2026) | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm | verified in the Part 5 plan |
| EU prudent valuation RTS, Delegated Reg. 2016/101 (model-risk AVA) | https://eur-lex.europa.eu/eli/reg_del/2016/101/oj | *(verify article numbers)* |
| PRIIPs Regulation (EU) 1286/2014 | https://eur-lex.europa.eu/eli/reg/2014/1286/oj | known; *(verify link)* |
| IFRS 9 B5.1.2A day-one gains; FRTB MAR23 residual risk add-on; FINRA complex-product notices | IFRS Foundation; https://www.bis.org/basel_framework/chapter/MAR/23.htm ; FINRA | *(verify all three)* |
| Glasserman, Karmarkar (2025) | https://arxiv.org/abs/2512.05301 | verified |
| Lakshtanov (2026) | https://arxiv.org/abs/2609.06137 | verified |
| Lopez-Piqueres, Acharya, Sun, Kumar (2026) | https://arxiv.org/abs/2610.42119 | verified |
| Zeron, Wu, Ruiz (2023) | https://arxiv.org/abs/2305.06215 | verified |
| Sharma, Chen, Noh, DeJesus, Schlener (2024 ×2) | https://arxiv.org/abs/2407.10903 ; https://arxiv.org/abs/2411.01121 (ACM ICAIF 2024) | verified |
| Cibrario et al. (2025) quantum autocallables | https://arxiv.org/abs/2507.19039 | verified |
| Higgins (2026) | https://arxiv.org/abs/2602.01376 | verified |
| Fukasawa (2026) | https://arxiv.org/abs/2610.00340 | verified (title only) |
| Goudenège, Molent, Zanette (2025) | https://arxiv.org/abs/2502.10300 | verified |
| Che, Lim, Sun (2026) MOT | https://arxiv.org/abs/2602.02996 | verified (title only) |

**Unverified (keep the marks or drop):**
- the 1987 Tokyo origin of "Asian" options;
- the UBS $50 bn attribution;
- the year of the 13.16% → 8.72% basis report;
- the body of the April 2024 Bloomberg report;
- the final Korean penalty amounts (2026);
- "19.3 tn" in the current scene, against 18.8 tn in the press;
- the FINRA notice numbers, MAR23, IFRS 9 B5.1.2A;
- page and issue numbers of the classic papers;
- Calvet et al. (2023), Wilmott (2002), Schoutens–Simons–Tistaert (2004), Hirsa–Courtadon–Madan (2003), Langnau
  (2010), Rubinstein (1991, ×2), Bowie–Carr (1994) venues;
- Hull 11th-ed. chapter number, and the Wilmott, Gatheral and Taleb chapter numbers;
- a 2016 HSCEI ELS knock-in episode and any Korean issuance curbs that followed. Only the *computed* 2015 vintages
  are certain; narrate the record only if verified.

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 15 · Exotics and Structured Products (~58)
1. The structuring business: a note taken apart into a bond, a coupon strip and a short put, priced piece by piece;
   the issuer's funding and margin; who buys, and what the record says they earned (Henderson–Pearson 2011;
   Célérier–Vallée 2017; Egan 2019); stylized notes followed on the real CSI 500 path.
2. Barriers: the reflection principle, the closed form and the PDE with its image; the value surface and the
   hedge at the wall; discrete monitoring (Broadie–Glasserman–Kou 1997); static replication (Derman–Ergener–Kani
   1995; Carr–Ellis–Gupta 1998) and how the skew breaks it.
3. Digitals and one-touches (the exploding gamma, the call-spread hedge simulated, the skew in a digital's price);
   Asians (Kemna–Vorst control variate; the change-of-numéraire PDE) and lookbacks (Goldman–Sosin–Gatto 1979).
4. Autocallables and snowballs (雪球): the price as a linear function of the coupon, the outcome distribution, carry
   and the futures basis; the issuer's delta, gamma and vega in 3D (long vol above the barrier, then short); the
   knock-in cliff.
5. Worst-of and correlation: Margrabe and Stulz; cross-gamma; correlation in calm and in crashes; the worst-of
   snowball; correlation skew and local correlation; mountain-range products.
6. Cliquets and forward-starting options: homogeneity, forward-volatility risk, the zero-vega ridge and volga;
   reverse cliquets and Napoleons (Part 13 for the forward smile).
7. Uncertain volatility (Avellaneda–Levy–Parás 1995; Lyons 1995): the Black–Scholes–Barenblatt equation solved
   live; non-additivity; the Lagrangian hedge with vanillas (Avellaneda–Parás 1996).
8. Model risk and reserves: exotics under models fitted to the same vanillas; Cont's (2006) measure; Glasserman–Xu
   (2014) worst case by exponential tilting; prudent valuation, day-one P&L and validation.
9. Dealer hedging flows: a book's aggregate vega and gamma on the real path, peak vega, the vega supply that
   depresses long-dated implied volatility; what is arithmetic and what is disputed.
10. A neural surrogate pricer for the snowball book, trained on screen with seeds and an equal-data baseline;
    discontinuous payoffs and their Greeks (frontier).

*Textbooks:* Hull OFOD ch. 26; Shreve II ch. 7; Bouzoubaa–Osseiran ch. 2, 7–15; Guyon–Henry-Labordère (UVM; local
correlation); Wilmott PWOQF (exotics chapters); Gatheral (barriers; exotic cliquets); Taleb (binaries and barriers).
Volatility derivatives → Part 12; numerics → Part 16; deep pricing → Part 17; hybrids → Parts 19, 21, 22.
*Computed/Trained:* note decomposition; buyer outcomes on the CSI 500 path; barrier closed form against MC by
monitoring frequency; static-hedge error under BS and Heston (ρ = 0, −0.7); digital against call-spread hedging error;
the snowball's outcome distribution, coupon by carry and barrier; Greeks surfaces; the 2024 book and its gamma; Korean
vintages 2015 and 2021; correlation regimes and the worst-of snowball; cliquet price over (σ, cap); UVM bounds,
non-additivity and the Lagrangian hedge; exotics under LV/Heston/Bates/VG fitted to the BTC Surface; the KL worst
case; book vega 2021–2024; the neural surrogate (3 seeds) against a polynomial; unbiased digital Greeks.
*Visuals:* the snowball's value and Greeks surfaces with the knock-in cliff (3D); the barrier wall; the static hedge
on the barrier line; the BSB PDE marching back with its σ map; the worst-of cloud collapsing; the cliquet ridge; path
fans diverging on exotics while agreeing on vanillas.
*Labs:* `down_out_call`, `geometric_asian_call`, `snowball_payoff`, `uvm_price`, the surrogate's training loop,
`static_dic_hedge`.
*Industry:* prudent valuation and model reserves, day-one P&L, FRTB for autocallables, PRIIPs; Natixis 2018.
*Frontier:* differential ML for discontinuous payoffs (Glasserman–Karmarkar 2025); unbiased MC Greeks (Lakshtanov
2026); tensor trains for worst-of autocallables (2026); RL hedging of autocallable books (2024); quantum autocallable
pricing (2025).
*Crisis:* the January–February 2024 A-share snowball knock-ins; Korea's HSCEI-linked ELS (2016 and 2024).
*Firms:* Chinese brokers' OTC derivatives desks; Korean banks and securities firms (FSS 2024–25); Natixis (2018).
*Desk:* "Price a digital with a call spread. What width, and what happens to the hedge near expiry?"; "The snowball
issuer's vega: sign, and where it peaks?"; "Price a one-touch with zero drift, given the digital."
*House:* the exotics pricer; Rule 15 (two models, a reserve, the worst path on record).
```

---

## 6. Implementation notes

**Manifest order (20 scenes):**
- `s01_hook`, `s02_business`, `s02a_buyers`, `s03_barriers`, `s03a_static`, `s04_digitals`, `s04a_asian`,
  `s05_snowball`, `s05a_greeks`;
- `s06_crash`, `s07_korea`, `s08_correlation`, `s08a_cliquet`, `s09_uvm`, `s09a_modelrisk`, `s09b_flows`;
- `s10_surrogate`, `s11a_industry`, `s11b_frontier`, `s12_outro`.

**Decision for the lead:** `s11_house` (0.9 min) is folded into ch17 (Rule 15) and the outro, and dropped from the
manifest. Its narration cache is lost, which is negligible. Content moves between kept modules:
- BGK → `s03a`;
- Asians and lookbacks → `s04a`;
- the 1D Greeks → `s05a`.

Kept modules re-narrate, so their caches will regenerate.

**House additions** (append to `explainer/quant/house/exotics.py`; tests appended to `tests/test_quant_house.py`):

| Function | Test |
|---|---|
| `one_touch(S, H, T, sigma, r=0, q=0)` (down or up, paid at expiry) | equals 2 × digital at zero drift; MC within 0.01 at 2,000 steps (BGK-shifted) |
| `static_dic_hedge(K, H, F)` → (weight, strike) | under BS with r = q = 0, weight × put(strike) = `bs.price(...) − down_out_call(...)` to 1e-10 |
| `snowball_AB(sigma, …)` → (A, B), so c* = (1 − A)/B | A + c·B equals `snowball_price` at c within 1e-12 (same seed); c* matches `fair_coupon` within 2e-3 |
| `autocall_on_paths(S, obs, ko, ki, coupon_per_obs)` → pv (for any model's paths) | reduces to `snowball_payoff` on GBM paths |
| `worst_of_autocall(S1, S2, …, rho)` | ρ = 1 and equal vols give the single-asset coupon |
| `margrabe(S1, S2, T, s1, s2, rho)` | MC within 3 se |
| `cliquet_bs(sigma, n, cap, floor, gfloor, n_paths)` | cap → ∞, floor → −∞, gfloor → −∞ gives E Σ r_i = 0 |
| `uvm_lagrangian(payoff, hedges, mkt_prices, …)` | the bound with hedges ≤ the bound without; equal when the hedge weights are 0 |
| `kl_worst_case(values, eta)` | η = 0 gives the mean; monotone in η |
| `digital_delta_estimators(S0, K, T, sigma, n, seed)` → (pathwise, LR, corrected) | corrected and LR within 3 se of exact; pathwise = 0 |

Optional: `asian_vecer(S, K, T, sigma, r, n_x, n_t)`; test against the CV price within 0.02.

**Data:**
- Everything is already in `videos/quant/data/manifest.json`: 510500.SS, 512100.SS, ^HSCE to 2025-11-30; the BTC
  Surface through Part 13's cache. **No new downloads.**
- Check before use: 512100.SS's full-sample correlation with 510500 (0.52) is much lower than its 2021–23 value
  (0.76). Inspect for split or rebasing artefacts in Yahoo's unadjusted closes (use log returns and drop |r| > 15%
  days if a corporate action is found, and say so).

**Narration branches (computed verdicts):**
- the static-hedge gaps (skew against monitoring);
- whether the spread's hedging error falls faster than the digital's;
- the snowball outcome shares;
- the q and KI coupons;
- which model gives the extreme autocall coupon and DNT;
- the polynomial against the network (the planning run says the polynomial wins: the narration must say so if the
  recomputation agrees);
- the KL curve;
- whether the Lagrangian hedge tightens the bounds.

**Risks:**
- `greeks3d` and `book_vega` are the heaviest items; cache per row.
- The surrogate's data generation took 938 s on the loaded machine.
- 3D scenes (ch3, 8, 11, 12, 13) need `add_fixed_in_frame_mobjects` for text, as in `quant12/s01_hook.py`.
- `modelrisk` depends on Part 13's cache, so the build order is quant13 before quant15.

**Chinese:**
- New terms for `QUANT_ZH_GUIDE.md`: 一触即付 (one-touch), 双不触碰 (double-no-touch), 静态对冲 (static hedge),
  看跌-看涨对称 (put-call symmetry), 离散观察修正 (discrete-monitoring correction), 棘轮期权 (cliquet), 远期生效期权
  (forward-start), 最差表现 (worst-of), 相关性偏斜 (correlation skew), 不确定波动率模型 (UVM), 审慎估值调整 (prudent
  valuation adjustment), 首日损益 (day-one P&L), 峰值vega (peak vega), 基差/贴水 (basis/discount), 替代定价模型
  (surrogate pricer).
- The Chinese edition's audience knows 雪球 well. Keep the CSI 500 basis (贴水) beat and the April 2024 curbs
  prominent.

**README:**
- the chapter list with minutes;
- the textbook audit table (§2b);
- the full paper list (including the additions above);
- 3 desk questions + 1 extra and 8 problems with solutions in English and Chinese;
- correct "about 55 minutes" to the measured length.

## 7. Lead's decisions (2 Nov 2026)

1. Accepted: `s11_house` leaves the manifest; Rule 15 moves to the industry chapter and the outro; new modules lettered so kept scenes keep their caches.
2. Part 13's calibrations are already cached (Part 13 was built); read them read-only. Part 13 is being re-planned in parallel: if its item names change later, the lead reconciles.
3. Accepted: rerun `surrogate` so it saves train/test data for the replay (run it niced, single thread).
4. Yes: check 512100.SS closes for split/adjustment artefacts before using the correlation; use adjusted closes or drop the full-sample figure.
5. Accepted: append 1991 to the shared timeline (append-only).
The narration says the polynomial beats the network at three inputs, as computed. Korean penalties, notional, UBS attribution, Risk.net year, Bloomberg body, FINRA/FRTB/IFRS references, chapter numbers and Vokata's venue: verify or drop.
