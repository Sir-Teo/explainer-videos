# Part 2 · The Machinery of Markets: expansion plan (24.6 → ~60 min)

Research and planning only; nothing in the repo was edited. Facts marked *(unverified)* were not confirmed against a
primary source and stay off screen until checked. "Checked" numbers were computed in this session from the repo's
cached data (`.cache/quant_data/`) or Binance's public archive.

**Target.** 20 chapters, about 60 min. AI parts run 17–19 chapters in 50–56 min, so chapters here are 2.5–3.5 min
(420–600 words at the measured ~170 wpm). An item with a derivation, an experiment and a case gets two chapters,
which together reach the standard's 4–6 min. The part has 6 labs, 4 fits shown learning, 10 live simulations, 2 3D
scenes, and ~95–115 CPU-min of compute (seeded, resumable).

## 1. Current state (`python tools/lecture_length.py quant2` = 24.6 min)

| # | Chapter (module) | Min | Coverage and depth |
|---|---|---|---|
| H | Press buy? (`s01_hook`) | 2.3 | Token through 6 boxes; Robinhood card (numbers differ from SEC report, §7); objectives; House. No derivation or experiment. |
| 1 | Instruments (`s02`) | 1.4 | Static 6-row table, illustrative quotes; notional/leverage card. |
| 2 | Orders, books, auctions (`s03`) | 2.4 | Order cards; **static** 10-level book; computed 300-order auction (100.07, 14,535 sh) as finished curves; dealer/RFQ cards. |
| 3 | Clearing and settlement (`s04`) | 1.8 | Novation diagram; computed netting bars ($11.0→3.1→1.0 bn); T+5→T+1. No proof, no waterfall. |
| 4 | Margin and leverage (`s05`) | 2.8 | Best chapter: 3-step liquidation ladder; real BTC March 2020, 10×/3×/2× liquidated; funding 2020 (17.2%/yr). Finished plots. |
| 5 | Short selling (`s06`) | 1.9 | 5-step list; payoff mirror; VW 4-point schematic. No data, no model. |
| 6 | Repo, lending, PBs (`s07`) | 2.2 | Repo arrows; haircut 1/h as text; TRS; Archegos narrated. |
| 7 | Day repo broke (`s08`) | 2.0 | FRED SOFR/DFF/IOER Aug–Oct 2019, reserves. Real data, finished plot. |
| 8 | Who earns what (`s09`) | 2.3 | Sell/buy-side cards; computed 2-and-20 with HWM 1927–2020 ($7,893 → $360); roles narrated. |
| 9 | World (`s10`) | 1.8 | Text table; price limits asserted, not simulated. |
| 10 | Funding desk (`s11`) | 0.8 | House chart, list of functions. |
| R | Outro (`s12`) | 2.8 | Recap, 3 desk questions, 5 problems, payoffs. |

There are 6 compute items (seconds each). There are no labs, no fits shown learning, no 3D scenes and no live
simulations. The House has `funding.py` (`margin_account`, `liquidation_price`, `netting`, `call_auction`,
`fund_fees`, `max_leverage`).

## 2. Audit

### (a) Syllabus items

| Item | Status | Gap |
|---|---|---|
| 1 Instruments, quotes | **thin** | No forward price, basis, contract specs, clean/dirty bond price or ETF NAV; no hedging with futures (READING §2 gives Hull's hedging chapter to Part 2). |
| 2 Exchanges/OTC, auctions, RFQ | **thin** | Static book; no validity or hidden orders, visibility precedence, RFQ economics or tick rule. |
| 3 Clearing, settlement, Jan 2021 | **covered, shallow** | No netting proof, waterfall, NSCC model or ECP; Robinhood numbers need correcting. |
| 4 Margin, leverage, portfolio margin | **full (liquidation); missing (IM models)** | No SPAN/VaR margin, procyclicality or portfolio margin. |
| 5 Short selling, squeeze, VW | **thin** | No fee/rebate arithmetic, SI above 100% or squeeze dynamics. |
| 6 Repo and securities lending | **medium** | The 2019 crisis is good; specials, tri-party and the lending market missing. |
| 7 Prime brokerage, TRS | **thin** | Narration only. |
| 8 Players, business models, PFOF | **medium / thin** | Fees computed; PFOF and agency/principal one line each. |
| 9 Quant industry map, roles | **thin** | One narration block. |
| 10 World markets | **thin** | Limits asserted. |
| 11 Benchmarks and indices | **missing** | Nothing. |

### (b) Textbook core sections → chapter (chapter numbers as recalled for the editions named; verify against the TOCs)

| Book · section | Chapter / part |
|---|---|
| Hull OFOD 1 Introduction (forwards, futures, options; traders) | 2, 3; traders 18 |
| Hull 2 Futures markets and CCPs (specs, convergence, daily settlement, margin, OTC, CCPs, delivery, forwards vs futures) | 2, 3, 7, 9 |
| Hull 3 Hedging with futures (basis risk, cross hedge, min-var ratio, tailing, beta hedge, stack and roll) | 3 |
| Hull 5 Forward/futures prices (carry, known yield, valuing forwards, futures vs forwards) | 3; FX/commodities, futures vs expected spot → Part 22 |
| Hull 5 §short selling | 11 |
| Hull 4, 6, 7 (rates, IR futures, swaps) | quoting in 2 → Part 18 |
| Hull 10 Mechanics of options markets (specs, OCC, margin on written options) | 2, 7; strategies → Part 11 |
| Harris 1–2 Introduction; the trading industry | 1, 18 |
| Harris 3 Orders (market, limit, stop, MIT; DAY/GTC/IOC/FOK; hidden/iceberg) | 4 |
| Harris 4 Market structures (quote-/order-driven, brokered; continuous vs call; transparency) | 4, 5, 6 |
| Harris 5 Order-driven markets (precedence: price, visibility, time; uniform vs discriminatory pricing) | 4, 5 |
| Harris 6 Brokers (principal–agent, best execution) | 6 |
| Harris 7–8 Why people trade; good markets | Part 1 ch 9; 18 (one beat); Part 35 |
| Tuckman–Serrat, repo (GC/special, specialness and on-the-run, fails charge, tri-party, leverage) | 12, 13 |
| Pedersen 1 (hedge funds, fees, HWM); 2 (SR, IR, HWM, drawdown) | 15; rest of 2 → Part 26 |
| Pedersen 3–4 (backtesting, portfolio construction) | Parts 26, 30 |
| Pedersen 5 (trading and financing: margin, funding liquidity, spirals) | 9, 10, 12, 14; Part 41 |
| Mishkin, financial system and money markets | 1, 12 (light) |

### (c) Part 2 papers (READING §4)

| Paper | Now | Plan |
|---|---|---|
| Shleifer (1986) *JF* | absent | screen, ch 16 |
| Chang–Hong–Liskovich (2015) *RFS* 28(1):212–246 | absent | screen, ch 16 (simulated RD) |
| D'Avolio (2002) *JFE* 66:271–306 | absent | screen, ch 11 |
| Duffie (1996) *JF* 51(2):493–526 | absent | screen, ch 12 |
| Duffie (2010) *JEP* 24(1) | absent | screen, ch 14 |
| Copeland–Martin–Walker (2014) *JF* 69(6):2343–2380 | absent | screen, ch 12 |
| Battalio–Corwin–Jennings (2016) *JF* | absent | screen, ch 6 |
| Ernst–Spatt (2022) NBER WP 29883 (verified; drop *(verify)*) | absent | screen, ch 6 |
| Fung–Hsieh (1997) *RFS* | absent | mentioned, ch 15 |
| Getmansky–Lo–Makarov (2004) *JFE* 74:529–609 | absent | screen, ch 15 (computed) |
| SEC Staff (2021) report | source note | screen, ch 1, 6, 8, 11 |
| SEC (2024) Rule 612 amendments | absent | screen, ch 4, 19 |
| SEBI (2023, 2024) F&O studies | screen | kept; FY25 update added (ch 17) |

To add to READING Part 2: • Smith–Farmer–Gillemot–Krishnamurthy (2003) *QF*; • Duffie–Zhu (2011) *RAPS*; •
Brunnermeier–Pedersen (2009) *RFS*; • Afonso et al. (2021) NY Fed *EPR* 27(2); • the six ch 19 papers.

## 3. Chapters (20, ~60 min)

Terms used below: • **Lab**: a `code_block` (≤12 lines, `explainer/ai/viz.py`) shown, then run, with output appearing
live. • **Live**: a simulation drawn as it runs (`ValueTracker`/`always_redraw`). • **Replay**: a fit scrubbed through
checkpoints with its loss curve and seed bands (as in `ai21/s12_reflow.py`).

Each chapter gives the goal, beats in order, derivation steps with *(reasons)*, the signature visual, the experiment,
the hands-on elements and a pause-and-predict question.

### Ch 1 · What happens when you press buy? (`s01_hook`, deepened, 3.0)
**Goal.** One trade end to end; on 28 Jan 2021 the plumbing, not the price, decided who could trade; the era.  
**Beats.** (1) Title. (2) The 6-node token journey (keep), with a clock that splits into "seconds" and "T+1" lanes;
collateral coins drop into the CCP box while the token waits. (3) Robinhood, corrected to the SEC staff report: · 27
Jan: NSCC intraday calls of **$6.9 bn on 36 members** ($2.1 bn mark-to-market, $4.8 bn special), $25.5 bn total
required. · 28 Jan: ECP charges waived for all members. Absent the waiver, one retail broker-dealer would have owed an
ECP charge "more than double its margin requirement of $1.4 billion". · GME short interest **122.97% of float**. (4)
History strip: 1602 VOC shares; 1730 Dojima rice futures recognized; 1792 Buttonwood; 1848 CBOT; 1925 Board of Trade
Clearing Corp. (the first independent US futures clearing house); 1973 DTC and CBOE; 1986 Big Bang; 2001
decimalization; 2005 Reg NMS; 2024 T+1. (5) Objectives; House (treasury lit).  
**Visual.** CCP coins accumulate with open exposure; on replaying 27 Jan they pour in and a bar rises to $25.5 bn.  
**Sources.** • SEC report:
https://www.sec.gov/files/staff-report-equity-options-market-struction-conditions-early-2021.pdf • Dojima:
https://www.odex.co.jp/en/about/derivative • BOTCC: https://www.marketswiki.com/wiki/Clearing_Corporation  
**Predict.** "Why would a CCP want more collateral from a broker whose customers are only buying?" (Answered in ch 8.)

### Ch 2 · Instruments and how they are quoted (`s02_instruments`, deepened, 2.5)
**Goal.** What is quoted, in what unit; what a contract is.  
**Beats.** Each table row animates its quote: • Bond: a flat clean price, accrued interest growing, the dirty price
saw-toothing at coupons. • Futures card: underlying, size, tick value, expiry, settlement (E-mini multiplier *(verify
with CME)*). • Option card: 100-share multiplier, strike, expiry, exercise style; OCC as clearer. • ETF: price against
intraday NAV, with the creation/redemption arrow (→ Part 38). • Notional against value; leverage = notional/equity.  
**Derivations.** • $P_{\text{dirty}}=P_{\text{clean}}+c\cdot\tfrac{\text{days since coupon}}{\text{days in period}}$
*(quoted clean so it doesn't jump at coupons)*. • Swap value $\approx\text{DV01}\cdot\Delta y$ *(notional sets size;
value is sensitivity times move)*.  
**Visual.** The dirty saw-tooth drawn live over the flat clean line, the AI wedge shaded.  
**Predict.** "Clean price unchanged for a month: did the holder earn anything?"

### Ch 3 · Futures: carry, basis and the hedge (`s03_futures`, new, 3.5)
**Goal.** $F=Se^{(r-q)T}$ by replication; the basis converging on real data; the minimum-variance hedge.  
**Beats.** (1) Fact: on 10 Feb 2021 the March BTC future traded ~5% over spot, ~40% a year. (2) Cash-and-carry. (3)
Reverse carry. (4) Convergence on data. (5) Implied carry. (6) Futures vs forwards: daily settlement; equal prices
when rates are deterministic (proof → Part 18). (7) Basis risk and $h^*$. (8) Beta hedge $N^*=\beta V_A/V_F$. (9)
Stack and roll, in one line.  
**Derivations.** (1) Borrow $S_0$, buy, short the forward; at T deliver for $F_0$, repay $S_0e^{rT}$
*(cash-and-carry)*. (2) Zero outlay plus a riskless $F_0-S_0e^{rT}$ gives $F_0\le S_0e^{rT}$ *(no arbitrage)*. (3)
Short, lend, long forward: $F_0\ge S_0e^{rT}$ *(reverse carry)*. (4) Yield q: $F_0=S_0e^{(r-q)T}$ *(hold $e^{-qT}$
units, reinvest)*. (5) $b_t=S_t(e^{(r-q)(T-t)}-1)\to0$ *(convergence)*; $\hat r=\ln(F_t/S_t)/(T-t)$. (6)
$\operatorname{Var}(\Delta S-h\Delta F)=\sigma_S^2-2h\rho\sigma_S\sigma_F+h^2\sigma_F^2$ *(variance of a difference)*.
(7) $h^*=\rho\sigma_S/\sigma_F$ *(FOC; second derivative $2\sigma_F^2>0$)*. (8)
$\operatorname{Var}^*=\sigma_S^2(1-\rho^2)$, effectiveness $\rho^2$ *(substitute)*; $N^*=h^*Q_A/Q_F$.  
**Signature visual.** • (a) Spot and the March-2021 future drawn live hour by hour, two ribbons zipping shut; the gap
re-plotted below as an annual rate; a days-to-expiry counter. • (b) **3D**: $\operatorname{Var}(h,\rho)/\sigma_S^2$
over $h\in[0,1.6]$, $\rho\in[0,1]$ ($\sigma_S/\sigma_F=1.2$). A ball rolls into the valley $h^*=1.2\rho$ as the camera
orbits; a ρ-slice parabola deepens as $\rho\to1$. *The valley's depth $1-\rho^2$ IS effectiveness.*  
**Experiment (checked).** `binance_klines("BTCUSD_210326","1h",...,market="futures/cm")` against spot BTCUSDT:

| Date | Basis | Annualized |
|---|---|---|
| 1 Dec 2020 (115 d) | 4.67% | 14.5% |
| 10 Jan 2021 | 5.07% | 24.0% |
| 19 Feb 2021 | 4.59% | 46.6% |
| 21 Mar 2021 (5 d) | 0.35% | 25.4% |

Mean annualized 24.7%, max 57% (more than 10 days left). The final bar is off by 0.7% (USD vs USDT, index vs Binance
spot): say so. Cross hedge: ETH with BTC, h* fitted 2021–22, tested 2023, ρ² in vs out of sample. Compute 2 min.  
**Lab 1.** New `funding.min_var_hedge(dS, dF)` (5 lines): `c=np.cov(dS,dF); h=c[0,1]/c[1,1]; resid=dS-h*dF`; return
h and `1-resid.var()/dS.var()`. Run on ETH/BTC.  
**Predict.** "F = 102, S = 100, 6 months, r = 3%: trade?" ($F^*=101.51$: sell F, buy S, lock 0.49.)

### Ch 4 · The order book (`s04_book`, new, 3.0)
**Goal.** The book as queues; price, visibility and time precedence; the cost of a market order; the tick.  
**Beats.** (1) Order types plus DAY/GTC/IOC/FOK, and hidden/iceberg orders (behind displayed orders at the same
price). (2) **Live** zero-intelligence book (Smith et al. 2003), 60 s simulated. (3) One level as a queue: joins at
the back, cancels from the middle. (4) A size-Q market order walks the book; effective spread. (5) Tick: SEC Rule 612
amendments (Sept 2024). · Half-penny tick where the time-weighted quoted spread is ≤$0.015. · Access-fee cap cut from
30 to 10 mils. · Compliance moved from Nov 2025 to **2 Nov 2026** by exemptive relief; further delay requested. Check
status.  
**Derivations.** Depth d per tick δ, best ask a: (1) Fills levels $k=1..Q/d$ at $a+(k-1)\delta$ *(price priority)*.
(2) $\bar p=a+\tfrac\delta2(\tfrac Qd-1)$ *(arithmetic series)*. (3) $\bar p-m=\tfrac s2+\tfrac\delta2(\tfrac Qd-1)$
*(half-spread plus the walk; linear here, concave in real books → Part 37)*. (4) Effective spread $2|p-m|$.  
**Signature visual.** `OrderBookLadder` (new in `explainer/quant/viz.py`, reused by Parts 35–38): mirrored bars per
level made of order blocks. Arrivals stack at the back, cancels fade from the middle, and a market order is a red bite
eating blocks front-first. A moving spread bracket, with a spread histogram building beside it.  
**Experiment (simulated).** ZI model (rates α limit/level, μ market, δ cancel/share), 200k events × 8 seeds,
snapshots every 50 events. Spread against μ/α; depth profile; impact against the uniform formula. Expected: concave
impact; spread rising with μ/α. Compute 10 min.  
**Predict.** "Halve the tick on a one-tick-spread stock with long queues: spread? queue?"

### Ch 5 · Auctions: one price for everyone (`s05_auction`, deepened, 3.0)
**Goal.** Prove the auction picks the volume-maximizing crossing; watch the indicative price form; why the close
matters.  
**Beats.** (1) Uniform vs discriminatory pricing. (2) **Live**: 300 orders arrive one at a time, each adding a step to
a staircase; indicative price and imbalance readouts update (as in published imbalance feeds, e.g. Nasdaq's NOII). (3)
Proof. (4) A 2,000-share market-on-close buy shifts the crossing. (5) Why the close matters (index funds, NAVs).
Auction share ~7.5% of US volume (Bogousslavsky–Muravyev draft) *(verify)*.  
**Derivations.** (1) $D(p)=\sum_{b_i\ge p}q_i$ is non-increasing; $S(p)=\sum_{a_j\le p}q_j$ is non-decreasing. (2)
$V=\min(D,S)$ *(both sides needed)*. (3) Where $S<D$, V = S rises; where $S>D$, V = D falls *(monotone)*, so V peaks
at the crossing. (4) Ties: least $|D-S|$, then a reference price *(exchange rule)*.  
**Visual.** The staircases build, the crossing slides, and the MOC order shifts demand right.  
**Experiment.** `auction` (existing), plus `auction_live` (state after each order), plus the MOC shock. 1 min.  
**Lab 2.** `funding.call_auction` (existing, 12 lines): run, the price prints.  
**Predict.** "A 2,000 buy at any price: moves the price more or less than in the continuous book?"

### Ch 6 · Dealers, RFQ and wholesalers (`s06_dealers`, new, 3.0)
**Goal.** Quote-driven markets; asking n dealers; why wholesalers pay for retail flow.  
**Beats.** (1) Dealer markets (bonds, FX, swaps); RFQ. (2) RFQ: a better best quote against leakage. (3) Wholesalers:
retail flow carries less adverse selection; the gain is shared as price improvement plus PFOF. (4) Evidence: ·
Ernst–Spatt: PFOF small in stocks, large in options. · Battalio–Corwin–Jennings: rebate-maximizing routing lowers
limit-order execution quality. · SEC 2021: ~80% of off-exchange GME volume internalized; 88% of internalized dollars
by three wholesalers (Citadel ~50%, Virtu ~26%); Citadel internalized ~$4.2 bn of GME on 27 Jan. (5) Best execution.  
**Derivations.** (1) Dealer cost $c_i\sim N(0,\sigma^2)$ iid *(private inventory)*. (2) $\mathbb E\max_{i\le
n}Z_i=n\int z\phi\Phi^{n-1}dz\approx\sqrt{2\ln n}$ *(order statistics)*. (3) $C(n)=m-\sigma\mathbb
E\max_nZ+\lambda(n-1)$ *(leakage per dealer)*; $n^*$ where $\sigma(\mathbb E\max_{n+1}-\mathbb E\max_n)=\lambda$. (4)
Wholesaler profit per share is $s/2-\alpha_R-\text{PI}-\pi\ge0$ *(markouts)*; competition drives $\text{PI}+\pi\to
s/2-\alpha_R$.  
**Visual.** n dealer dots flash quotes and the best glows. Repeated 200×, the best-quote histogram slides left as n
grows while a leak meter rises; their sum is a U-curve with the minimum marked. Markout curves for simulated retail
against institutional flow.  
**Experiment (simulated).** RFQ Monte Carlo n = 1..20 ($10^5$ draws), $n^*$ over λ/σ; a flow simulation in which a
fraction φ knows the price 60 s ahead. Expected: $n^*\approx3$–6; retail markout ≈ 0, institutional negative. 2 min.  
**Predict.** "Why would anyone pay to trade against you?"

### Ch 7 · Clearing: novation, netting, waterfall (`s07_clearing`, deepened, 3.5)
**Goal.** Netting only shrinks obligations; a CCP's response to default; when a CCP raises risk.  
**Beats.** (1) Novation (keep). (2) **Live** netting graph. (3) Proof. (4) Duffie–Zhu (2011): clearing one class
breaks cross-class netting and can raise exposure. (5) Waterfall: defaulter's IM → defaulter's default fund → CCP skin
in the game → survivors' default fund → assessments → VM haircutting. Cover-2 per CPMI–IOSCO PFMI *(verify wording)*.
(6) Scale: NSCC netted ~$2.2 tn/day to $33.5 bn (98%) in 2024 (https://www.dtcc.com/annuals/2024/; fetch failed,
*verify*).  
**Derivations.** With $x_{ij}\ge0$ owed by i to j: (1) $G=\sum x_{ij}$; $y_{ij}=x_{ij}-x_{ji}$;
$B=\sum_{i<j}|y_{ij}|$. (2) $|x_{ij}-x_{ji}|\le x_{ij}+x_{ji}$, so $B\le G$ *(triangle inequality)*. (3)
$n_i=\sum_jy_{ij}$, $M=\sum n_i^+$ *(a CCP collects net debts only)*. (4) $n_i^+\le\sum_jy_{ij}^+$, so $M\le B$
*(positive part subadditive)*. (5) $\sum n_i=0$ *(the CCP is flat)*.  
**Signature visual.** `NettingGraph` (new): 25 nodes on a circle with 5,395 arcs. Bilateral step: opposite arcs
annihilate. Multilateral step: arcs are pulled into a central CCP node and collapse to one arrow each; counters tick
11.0 → 3.1 → 1.0 bn. Waterfall: a stacked column drained layer by layer by a loss liquid over 5 stress scenarios; only
the worst reaches survivors.  
**Experiment.** • `netting` (existing). • `duffie_zhu`: N 5–50 × K 1–10, $10^4$ draws. Expected: a CCP helps only when
N is large relative to K. • `waterfall`: 25 members, IM at 99% 2-day VaR, t(3) stress, $10^5$ scenarios, the share of
losses reaching each layer.

20 min.  
**Lab 3.** `funding.netting` (existing) run on the 5,395 trades.  
**Predict.** "A→B 10, B→C 10, C→A 10: what moves through a CCP?" (0.)

### Ch 8 · Settlement and the deposit (`s08_settlement`, new, 2.5)
**Goal.** Why unsettled trades need collateral, how NSCC sizes it, what T+1 changed; the answer to ch 1.  
**Beats.** (1) DVP, CNS; T+5 → T+3 (1995) → T+2 (2017) → T+1 (28 May 2024). (2) NSCC clearing fund: a parametric-VaR
volatility component at 99%, plus mark-to-market, special charges and ECP (SEC report §2). (3) Buying customers still
leave the broker owing cash at settlement on shares that may collapse first. (4) After T+1
(https://www.dtcc.com/news/2024/september/12/sifma-ici-and-dtcc-release-t1-after-action-report): · clearing fund  
**−$2.4 bn (20%), $12.2 bn → $9.8 bn**; · affirmation 73% → ~95%; · CNS fails 2.12% (July 2024), in line with T+2.  
**Derivations.** (1) $E_h=hf$ *(h days of unsettled net buying)*. (2) $D=z_{0.99}\sigma\sqrt\tau E_h$ *(parametric
VaR, close-out τ)*. (3) Halving h halves one-way $E_h$; netted two-way flow shrinks less *(why 20%, not 50%)*.  
**Visual.** A conveyor: each day drops a crate that rides h days; a VaR shadow beneath scales with σ. T+2 → T+1
shortens the belt; a σ spike balloons the shadow (27 Jan).  
**Experiment (simulated).** Net buying while vol goes 60% → 400% (stated); deposit at T+2/T+1/T+0, one-way vs two-way
flow, 8 seeds. Optional GME path via `yahoo_daily` (rate-limited this session). 2 min.  
**Predict.** "At T+0, does the deposit vanish?" (Not the intraday exposure.)

### Ch 9 · Margin and liquidation (`s09_margin`, deepened, 3.0)
**Goal.** The real crash run live, and the liquidation probability as a 3D object.  
**Beats.** (1) IM/VM/MM and the ladder (keep). (2) **Live**: `margin_account` steps hourly from 1 Mar 2020; equity
bars fill and drain `HedgeLedger`-style; accounts are crossed out (10× 9 Mar; 3× 12 Mar; 2× 13 Mar at $4,063, $271
below zero). (3) Funding (compressed). (4) The 3D surface. (5) Portfolio margin: offsets for hedged books (→ ch 10).  
**Derivations.** (1) Keep the 3-step $P_{\text{liq}}$. (2) $d=-\ln(P_{\text{liq}}/P_0)$. (3) $\mathbb P(\min_{t\le
H}X_t\le-d)=2\Phi(-d/\sigma\sqrt H)$ *(reflection principle, driftless log-price)*.  
**Signature visual.** **3D**: empirical P(liquidated within H days) over leverage 1–50 × H 1–90, from daily entries
in BTC hourly 2020–25, with the translucent Brownian surface over it. The camera orbits to the cliff where fat tails
beat the formula; a slice at L = 10, H = 19 lands on the March 2020 traders.  
**Experiment.** `margin` (existing) plus `liq_surface` (`binance_klines(...,"1h","2020-01","2025-12",
market="futures/um")`, window minimum lows, a vectorized 50×90 grid; numbers from the run). 8 min.  
**Lab 4.** `funding.margin_account`'s 8-line loop, stepped with the live ledger.  
**Predict.** "5× → 10×: does the distance halve, or worse?" (d 0.22 → 0.10; probability more than doubles.)

### Ch 10 · How much margin? Models and procyclicality (`s10_imodel`, new, 3.0)
**Goal.** Derive and fit a margin model, and see it demand most when members can least pay.  
**Beats.** (1) SPAN-style scenario grid (CME's 16 scenarios *(verify)*). (2) EWMA VaR margin. (3) Fit λ (shown
learning). (4) Kupiec backtest. (5) Procyclicality and anti-procyclicality tools (EMIR buffer or stressed look-back
*(verify)*). (6) Inserts: · **LME nickel, 8 Mar 2022**: the three-month contract more than doubled; trading suspended;
the day's trades cancelled. FCA Final Notice 20 Mar 2025, £9.2 m (https://www.cityam.com/?p=2316359; cite the notice
itself). · **UK LDI, Sept 2022**: gilts +100 bp in 4 days; collateral calls; BoE purchases
(https://bankunderground.co.uk/2024/07/26/what-caused-the-ldi-crisis/).  
**Derivations.** (1) $\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)r_{t-1}^2$ *(EWMA)*. (2)
$\text{IM}_t=z_{0.99}\sigma_t\sqrt h\cdot N$ *(Gaussian VaR over close-out h)*. (3)
$\ell(\lambda)=-\tfrac12\sum(\ln\sigma_t^2+r_t^2/\sigma_t^2)$, $\hat\lambda=\arg\max\ell$ *(likelihood)*. (4)
$LR=-2\ln\frac{0.99^{T-x}0.01^x}{(1-\hat p)^{T-x}\hat p^x}\sim\chi^2_1$ *(Kupiec coverage)*.  
**Signature visual.** The price with margin as a **breathing band**, drawn daily through 1987. On 19 Oct the −17.4%
bar pierces it and the band balloons 3.5% → 12%: "margin arrives after the loss". **Replay**: λ sweeps 0.90 → 0.995,
ℓ(λ) traces and the band redraws, gradient iterates walk to $\hat\lambda$. Bands from 1926–2020, BTC and 5 bootstrap
blocks; baseline constant-σ.  
**Experiment (checked; λ = 0.97, 2-day 99%, `ken_french_daily` 1926–2020).** • 1-day breach rate **2.0%** against 1%
nominal. • Margin 2.47% (1 Sep 87) → 3.46% (16 Oct) → 10.82% (20 Oct) → 12.03% (30 Oct). • Within-year peak/trough:
1987 ×5.5; 2008 ×4.0; 2020 **×7.5** (2.31% on 14 Feb → 12.85% on 23 Mar).

Same on BTC. 5 min.  
**Lab 5.** New `funding.ewma_margin(r, lam=.97, z=2.326, h=2)` (6 lines: the recursion, `return z*np.sqrt(h*v)`), run
on 1987.  
**Predict.** "Faster-reacting margin: is the market safer?" (The CCP is; members get bigger calls on the worst day.)

### Ch 11 · Short selling and the squeeze (`s11_short`, deepened, 3.0; crisis file: Volkswagen)
**Goal.** Fee, rebate, dividends, recall; short interest above 100%; why squeezes cascade.  
**Beats.** (1) Locate, borrow, 102% collateral (keep). (2) P&L with rebate. (3) D'Avolio: mostly general collateral;
≤~9% of stocks with fees above 1%, specials averaging 4.3% (as quoted by Daniel et al. 2025; check
https://www.johnhcochrane.com/s/davolio_borrowing_stock_JF.pdf). (4) Relending: the SEC footnote example (1 share
shorted twice gives 2%); GME 122.97%. (5) **Live** squeeze. (6) VW: · 26 Oct 2008: Porsche 42.6% of ordinary shares
plus cash-settled options on 31.5% (74.1%); Lower Saxony ~20%; so ~6% free float (computed). · **€210.52 → €1,005.01**
intraday 28 Oct; €512 on 29 Oct after Porsche said it would release up to 5% (https://risk.net/node/1518068;
cross-check with exchange data). · Funds sued *alleging* Porsche misled the market; Porsche denied it
(https://hflawreport.com/2539726/).  
**Derivations.** (1) Collateral $C\approx1.02S_0$ earns rebate $r_b=r-f$ *(lender keeps the fee)*. (2)
$\Pi_T=(S_0-S_T)+Cr_bT-\sum\text{div}$ *(price, rebate, manufactured dividends)*. (3) $f>r\Rightarrow r_b<0$
*(specials: the short pays on its own collateral)*. (4) $\Delta\ln P=\kappa\,\text{net buys}/F$ *(impact per free
float)*; shorts cover once $P\ge\theta_kP_0$, and a cascade runs while each cover crosses the next threshold *(forced
buying)*.  
**Signature visual.** The float as a **water tank**: locked-up stakes fill it from below, leaving a thin free layer.
Shorts queue at the tap with buckets while a price thermometer rises; above thresholds buckets are forced; when the
queue outruns the layer, the thermometer explodes. Then the relending loop: one share passes A → B → C while the
short-interest counter reads 2 and the share count stays 1.  
**Experiment (simulated).** `squeeze`: 1,000 shorts with lognormal thresholds; float 2–50%; SI 20–140%; κ so 1% of
float moves the price 0.5% (stated); 8 seeds; peak multiple against SI/float. Expected: a sharp transition near SI ≈
free float. 15 min.  
**Predict.** "SI 120% of float: how, and who is short what?"

### Ch 12 · Repo, lending and specials (`s12_repo`, deepened, 3.0)
**Goal.** Secured funding; haircuts as leverage limits and the spiral; specialness as the price of scarce collateral.  
**Beats.** (1) Repo legs; interest = cash·r·d/360. (2) Tri-party vs bilateral. Copeland–Martin–Walker: tri-party
margins and funding fairly stable for most borrowers; Lehman's fell sharply; no system-wide run there
(https://www.newyorkfed.org/research/staff_reports/sr506.pdf). (3) Tower and spiral (Brunnermeier–Pedersen 2009). (4)
Specials (Duffie 1996): specialness raises price by the PV of borrowing savings
(https://ideas.repec.org/a/bla/jfinan/v51y1996i2p493-526.html); the on-the-run premium. (5) Securities lending as the
same market from the stock side (ch 11's fee).  
**Derivations.** (1) $\sum_k(1-h)^k=1/h$ *(each \$1 of collateral borrows 1−h, which buys more collateral)*. (2) $h\to
h'$ at the limit forces sales $A(1-h/h')$ *(new limit E/h′)*. (3) Impact cuts E and forces more sales; amplification
$1/(1-g)$ *(fixed point of the loop)*. (4) $P_{\text{sp}}-P_{\text{GC}}=\sum_t(r_{GC}-r_s)P\Delta t/(1+r)^t$ *(the
bond lends cheap cash)*.  
**Signature visual.** `CollateralTower`: blocks each (1−h)× the one below, reaching 1/h (50× at 2%). Slide h to 4%:
the top half crumbles into a market bin, the price ticks down, all blocks shrink, the next layer crumbles, until a
fixed point; a loop-gain counter.  
**Experiment (simulated).** `spiral`: 10 funds at max leverage, linear impact, haircut 2% → 3/4/6%, haircut rising with
realized vol; amplification; 8 seeds. 5 min.  
**Lab 6.** New `funding.deleverage(E, A, h_new, impact)` (≤10 lines) runs the tower live.  
**Predict.** "A Treasury is special at −1% for three months: its price?"

### Ch 13 · The day repo broke (`s13_repo_crisis`, deepened crisis, 3.0)
**Goal.** Measure Sept 2019 and recover the reserve demand curve from data.  
**Beats.** (1) Timeline (keep: SOFR 2.20% on 13 Sep → 5.25% on 17 Sep). (2) **SOFR percentile fan** (FRED
`SOFR1/25/75/99`). The 99th percentile (checked): 2.40% (13 Sep), 4.60% (16), **9.00% (17)**, 5.00% (18), 2.50% (19).
(3) NY Fed offered up to $75 bn; dealers bid $53 bn
(https://www.chicagofed.org/publications/chicago-fed-letter/2019/423). (4) **Fit** the demand curve. (5) Afonso et al.
(2021). (6) March 2020 in one line (→ Part 41).  
**Derivations.** (1) Banks hold reserves until their marginal value equals $s=r_{\text{repo}}-r_{\text{IOR}}$
*(opportunity cost)*. (2) $s(R)=a+be^{-cR}$ *(flat when abundant, steep when scarce)*, by least squares.  
**Signature visual.** Weekly (reserves, SOFR−IOR) dots for 2018–21 appear in time order: the dot crawls left under QT
and leaps on 17 Sep 2019. **Replay**: Gauss–Newton iterates bend the curve in beside the loss curve; bootstrap band;
linear baseline.  
**Experiment (checked; cached FRED SOFR, IOER, IORB, WRESBAL).** Mean weekly SOFR−IOR by reserves:

| Reserves | $1.3–1.5 tn | $1.5–1.7 tn | $1.7–2.0 tn | $2.5–3.5 tn | $3.5–5 tn |
|---|---|---|---|---|---|
| SOFR−IOR | **+15.0 bp** (max +82.6) | +4.0 bp | −0.7 bp | −2.7 bp | −9.6 bp |

3 min.  
**Predict.** "Where on this curve was the system in September 2019?"

### Ch 14 · Prime brokers and the race to sell (`s14_prime`, new, 3.0)
**Goal.** PB and TRS economics; why an unwinding client starts a race.  
**Beats.** (1) PB services: financing, custody, clearing, cross-margining. (2) TRS flows; swaps don't appear as
ownership in 13F filings. (3) Archegos: · The SEC *alleges* ~$1.5 bn / $10 bn exposure (Mar 2020) → >$36 bn / $160 bn
(Mar 2021) (https://www.sec.gov/news/press-release/2022-70). · Credit Suisse lost ~$5.5 bn; Nomura ~$2–2.85 bn
(sources differ; use its filing). · Hwang convicted July 2024; 18 years on 20 Nov 2024
(https://www.nbcnews.com/news/us-news/archegos-bill-hwang-sentenced-18-years-prison-massive-us-fraud-rcna181134). (4)
The race. (5) Duffie (2010): PB clients run from a weak dealer (Bear, Lehman).  
**Derivations.** (1) The fund receives $\Delta S+\text{div}$ and pays $(r+s_f)S\Delta t$ *(synthetic long with
financing)*. (2) K banks sell q each with linear impact λ; the j-th gets $P_0-\lambda((j-1)q+q/2)$ *(earlier sales
moved it)*. (3) $L_j=\lambda q^2(j-\tfrac12)$: the last loses $(2K-1)\times$ the first *(race)*. (4) A standstill
splits losses evenly, but selling first is each bank's best response *(prisoner's dilemma)*.  
**Visual.** Four bank towers beside a shared price axis. Blocks drop bank by bank, the price ratchets down and loss bars
fill. Replay with another order, then a standstill. A 2×2 payoff matrix lights the Nash cell.  
**Experiment (simulated).** `fire_sale`: K = 2–8, square-root impact, random orders, loss by rank, 8 seeds. 3 min.  
**Predict.** "You hear first: what do you do, and to whom?"

### Ch 15 · Who earns what: fees and smoothed returns (`s15_business`, deepened, 3.5)
**Goal.** Business models; fees compounded; too-smooth reported returns, measured.  
**Beats.** (1) Sell side (flow/exotics, agency/principal), buy side, prop, market makers (compressed). (2) Fees
(existing: $7,893 → $360; investor keeps 4.5% of profit; $3,288 after 1%). (3) Performance fee as a **call** struck at
the HWM. (4) Multi-manager pass-through, qualitative only *(no number unless sourced)*. (5) GLM smoothing. (6)
Fung–Hsieh: option-like hedge-fund returns.  
**Derivations.** (1) Fee $=\phi(V_T-\text{HWM})^+$ *(a call; out of the money after losses, hence closures and
relaunches)*. (2) $R^o_t=\sum_{k=0}^2\theta_kR_{t-k}$, $\sum\theta=1$ *(GLM)*. (3)
$\operatorname{Var}R^o=\sigma^2\sum\theta_k^2\le\sigma^2$ *(iid true returns)*. (4)
$\rho_1=(\theta_0\theta_1+\theta_1\theta_2)/\sum\theta_k^2$ *(MA(2) autocovariance)*. (5) Reported SR
$=\text{SR}/\sqrt{\sum\theta_k^2}$ *(same mean, less vol)*; θ by MA(2) MLE.  
**Signature visual.** A true return path and its reported *shadow* drawn live as a lagged average; the shadow's vol
ribbon thins and a Sharpe gauge rises; θ moves on a simplex triangle and the gauge follows. **Replay**: MLE iterations
converge to the true θ (5 seeds banded; moment-estimator baseline).  
**Experiment.** • Checked: smallest size decile (`ken_french_size_daily`) daily AC1 **0.40 (1963–89) against 0.04
(1990–2020)**; big decile 0.11 vs −0.09. Stale prices are smoothing in the wild. • Simulated: θ = (0.5, 0.3, 0.2)
inflates SR ×1.62. • `fees` (existing).

5 min.  
**Predict.** "AC1 = 0.4: true vol higher or lower than reported, by how much?"

### Ch 16 · Benchmarks and indices (`s16_index`, new, 3.0)
**Goal.** How indices are built and rebalanced; do demand curves for stocks slope down?  
**Beats.** (1) Cap, float and price weights (the Dow divisor). (2) Rebalancing demand. (3) Shleifer (1986): S&P
additions since 1976 earned announcement returns tied to index-fund buying, +2.79% for 1976–83 (as quoted in
https://www.nber.org/papers/w8654.pdf); the Harris–Gurel reversal in one line. (4) Russell RD (Chang–Hong–Liskovich
2015): the top of the R2000 gets far more index weight than the bottom of the R1000. (5) Benchmarking intensity
(Pavlova–Sikorskaya 2023). (6) Greenwood–Sammon (2025): ~7.4% (1990s) → <1% (last decade)
(https://papers.ssrn.com/abstract=4294297).  
**Derivations.** (1) $w_i=f_iN_iP_i/\sum_j f_jN_jP_j$ *(float factor)*; price-weighted $I=\sum P_i/\text{divisor}$,
with the divisor reset at splits. (2) $Q_i=Aw_i/P_i$, so inclusion demand $\Delta Q_i/N_i=Af_i/\text{cap}$ *(passive
assets A)*. (3) $\Delta P/P\approx(\Delta Q/N)/\varepsilon$ *(downward-sloping demand)*. (4) $\tau=\lim_{x\downarrow
c}\mathbb E[y|x]-\lim_{x\uparrow c}\mathbb E[y|x]$ by local-linear fits with bandwidth b *(continuity at the cutoff)*.  
**Visual.** 3,000 cap-sorted bars with a gate at rank 1000. Passive money pours in by within-index weight: thin at the
R1000 tail, thick at the R2000 head, a visible jump. Then a returns-vs-rank scatter with local-linear fits sliding in
from each side, and a bandwidth slider showing bias against noise.  
**Experiment (simulated).** `index_rd`: 30 reconstitutions × 3,000 stocks; true jump 1.5% (stated); size-decile vol
noise; bandwidths 50–500; 8 seeds. Expected: truth recovered, variance rising as bandwidth shrinks. Optional TSLA 2020
check via `yahoo_daily` *(availability unverified)*. 8 min.  
**Predict.** "Why does joining the R2000 bring more buying than staying in the R1000?"

### Ch 17 · Markets around the world (`s17_world`, deepened, 2.5)
**Goal.** Rules differ and change the statistics; price limits measured.  
**Beats.** (1) US (fragmented, wholesalers, T+1). (2) EU and UK T+1 on **11 Oct 2027**: EU regulation published 14 Oct
2025; UK accepted on 19 Feb 2025 (https://fca.org.uk/markets/about-t1-settlement). (3) Japan (the funding yen → Part
22). (4) India: · NSE the largest derivatives exchange by contracts since 2019
(https://www.fia.org/fia/articles/global-futures-and-options-volume-hits-record-137-billion-contracts-2023). · SEBI:
93% of individual F&O traders lost money FY22–24, over ₹1.8 lakh crore
(https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html).
· FY25: 91%, ₹1,05,603 crore (July 2025 study, via moneylife; link SEBI's release). · From 20 Nov 2024: contracts of
at least ₹15 lakh; one weekly expiry per exchange. (5) China: · T+1 shares; ±10% (±20% STAR/ChiNext); Stock Connect. ·
Short-selling refinancing suspended 11 Jul 2024
(https://www.securitiesfinancetimes.com/securitieslendingnews/regulationarticle.php?article_id=227170). ·
Program-trading rules flag 300 orders/s or 20,000/day
(https://www.simmons-simmons.com/en/publications/clypwunlq0046txdsscgltqm8/new-regulations-on-programme-trading-in-the-chinese-securities-market).
(6) **Live** price-limit simulation.  
**Derivation.** (1) $r^o_t=\operatorname{clip}(r_t+c_{t-1},\pm L)$, $c_t=r_t+c_{t-1}-r^o_t$ *(the unexecuted move
rolls over)*. (2) So $\operatorname{Cov}(r^o_t,r^o_{t+1})>0$ near limits.  
**Visual.** The true price is a free particle on a spring tied to the observed price, which bumps a ceiling; the spring
drags it up the next day; an AC1 readout climbs with jump intensity.  
**Experiment (simulated).** `limits`: a jump-diffusion with 2–4% daily vol; limits ±10% and ±20%; 8 seeds; AC1 and
tail truncation. 3 min.  
**Predict.** "Limit-up close, buyers queued: tomorrow's expected return, and can you trade it?"

### Ch 18 · INDUSTRY: who runs the machine, and how they earn (`s18_industry`, new, 3.0)
**Goal.** The firms that live on plumbing, with disclosed numbers, and the quant industry map and roles (item 9).  
**Visual.** The **money map**: boxes for retail, broker, wholesaler, exchange, CCP, custodian, fund, PB and repo
lender, with particles for PFOF, spreads, fees, interest and margin. Each `firm_card` zooms out of its box.  
**Firm cards.** • **Exchanges.** CME 2024: record revenue **$6.1 bn**; ADV **26.9 m** contracts (February results; the
January release said 26.5 m)
(https://www.cmegroup.com/media-room/press-releases/2025/2/12/cme_group_inc_reportsall-timerecordannualrevenueadjustedoperatin.html).
• **Clearing.** NSCC 98% netting; clearing fund −20% after T+1; $6.9 bn of intraday calls on 27 Jan 2021 (ch 7–8).
• **Wholesalers.** · Citadel Securities says it executes **>35%** of US retail volume (company claim,
https://www.citadelsecurities.com/?p=38878). · Virtu 2024 10-K: revenue **$2,876.9 m** (+25.4%), Market Making
$2,374.1 m, net income $534.5 m
(https://www.sec.gov/Archives/edgar/data/1592386/000159238625000055/virt-20241231.htm). • **Retail brokers.** ·
Robinhood Q4 2024 transaction revenue **$672 m**: crypto $358 m, options $222 m, equities $61 m
(https://investors.robinhood.com/static-files/039b9f51-74df-4ca8-9a2a-78e128bea7af). · The 10-K's PFOF terms:
per-contract for options, spread-linked for equities
(https://www.sec.gov/Archives/edgar/data/1783879/000178387925000049/hood-20241231.htm). • **Banks, PBs, the basis
trade.** · Archegos (ch 14). · Hedge funds' cash–futures basis trade **~$830 bn** in Sept 2025, about double its
early-2020 peak; hedge-fund repo borrowing $3.0 tn (Monin, FEDS Note, 22 Jun 2026,
https://www.federalreserve.gov/econres/notes/feds-notes/decomposing-hedge-funds-u-s-treasury-exposures-20260622.html).
• **Regulators.** · SEC (Rule 612, Treasury clearing); FCA (LME). · SEBI's 3 Jul 2025 interim order *alleging*
manipulation of Bank Nifty (and Nifty on fewer days) around expiries: **₹4,843.57 crore** impounded into escrow. Jane
Street disputes the findings and resumed trading after the deposit
(https://www.moneylife.in/article/jane-street-resumes-derivatives-trading-in-india-after-sebis-rs4843-crore-escrow-compliance/77732.html).
Allegations only; read the order and any later order first. • **The quant map** (horizon µs → years against
instrument): · HFT and market making: Citadel Securities, Virtu, Jane Street, Optiver, XTX; · options market making:
SIG; · stat arb; · CTAs: Man AHL; · systematic equity: AQR, Two Sigma; · multi-managers: Millennium, Citadel; · bank
desks.

  Roles light up: researcher, trader, developer, risk quant, strat, structurer.  
**Experiment.** `industry` stores only the cited numbers (revenue-mix bars). <1 min.  
**Desk.** The market-making game (keep).

### Ch 19 · FRONTIER, 2023–2026 (`s19_frontier`, new, 3.0)
**Visual.** One card per item; the timeline zooms to 2023–27, and pending rules land hollow on their future dates.  
**Research.** (1) Greenwood, Sammon (2025), "The Disappearing Index Effect," *JF* 80(2):657–698
(https://ideas.repec.org/a/bla/jfinan/v80y2025i2p657-698.html). Ties back to ch 16. (2) Pavlova, Sikorskaya (2023),
"Benchmarking Intensity," *RFS* 36(3):859–903 (https://ideas.repec.org/a/oup/rfinst/v36y2023i3p859-903..html): low
elasticities; higher intensity followed by lower returns. (3) Bryzgalova, Pavlova, Sikorskaya (2023), "Retail Trading
in Options and the Rise of the Big Three Wholesalers," *JF* 78(6):3465–3514
(https://lbsresearch.london.edu/id/eprint/2827): Citadel, Susquehanna, Wolverine; 12.6% average spread; retail loses
on average. (4) Schwarz, Barber, Huang, Jorion, Odean (2025), "The 'Actual Retail Price' of Equity Trades," *JF*
80(5):2507–2541 (https://ideas.repec.org/a/bla/jfinan/v80y2025i5p2507-2541.html): 85,000 simultaneous orders; the
dispersion comes from wholesaler pricing across brokers, not from PFOF. (5) Glicoes, Iorio, Monin, Petrasek (2024),
"Quantifying Treasury Cash-Futures Basis Trades," FEDS Notes, 8 Mar
(https://www.federalreserve.gov/econres/notes/feds-notes/quantifying-treasury-cash-futures-basis-trades-20240308.html);
Monin (2026), ~$830 bn. (6) Pinter (2023), "An anatomy of the 2022 gilt market crisis," BoE SWP 1019
(https://www.bankofengland.co.uk/working-paper/2023/an-anatomy-of-the-2022-gilt-market-crisis).  
**Structure.** (7) T+1 and its after-action numbers. (8) Rule 612 (adopted Sept 2024; compliance 2 Nov 2026 by
exemptive relief; further delay requested; check) (https://sec.gov/files/34-101070-fact-sheet.pdf). (9) Treasury
clearing mandate: cash **31 Dec 2026**, repo **30 Jun 2027**
(https://www.sewkis.com/insights/sec-extends-compliance-dates-for-ust-repo-and-cash-transaction-clearing-rule/).
Duffie (2023, Jackson Hole), "Resilience redux," argues for central clearing and all-to-all trading *(secondary
summary; read the paper)*. (10) Rules 13f-2 and 10c-1a: remanded, not vacated, on 25 Aug 2025; compliance moved to
2028 (https://www.ca5.uscourts.gov/opinions/pub/23/23-60626-CV0.pdf). (11) EU/UK T+1 2027; SEBI 2024; China 2024.

*(Bogousslavsky–Muravyev, "Who Trades at the Close?": venue and year unverified; reading guide only until checked.)*

### Ch 20 · Funding desk; recap, desk, problems (`s20_outro`, merged, 3.0)
**House.** `funding.py` gains: • `min_var_hedge`, `implied_carry`; • `ewma_margin`, `fit_ewma_lambda`; •
`liquidation_probability`; • `ccp_waterfall`; • `short_pnl`; • `deleverage`, `fire_sale`; • `glm_smooth`, `glm_fit`.

Rule 3 stands. New rule: margin follows `ewma_margin`, not a constant. Tests in `tests/test_quant_house.py`: • h* on
correlated normals; • EWMA closed form at constant r; • $M\le B\le G$ on random graphs; • waterfall sums; • fire-sale
losses against the formula; • GLM variance against the formula.  
**Desk.** Keep the market-making game; add "F 102, S 100, 6 m, 3%: trade?" and "SI 120% of float: how, and your
risk?"  
**Problems.** (1) Liquidation plus the reflection probability. (2) $M\le B\le G$ on 3 members. (3) The spiral's fixed
point. (4) h* with ρ = 0.8, σS/σF = 1.25 (h* = 1.0, effectiveness 0.64). (5) GLM θ = (0.6, 0.3, 0.1) and reported SR
1.5, giving true SR 1.02.

Then recap, payoff card, references.

## 4. Hands-on summary and compute budget

**Labs (6).** (1) `min_var_hedge` (3). (2) `call_auction` (5). (3) `netting` (7). (4) `margin_account` (9). (5)
`ewma_margin` (10). (6) `deleverage` (12).

**Fits shown learning (replays with seed bands and equal-budget baselines).** • λ̂ (10; constant-σ baseline). •
Reserve curve (13; linear baseline). • GLM θ (15; moment baseline). • RD over bandwidth (16).

**Live simulations.** Book (4), auction (5), RFQ (6), netting and waterfall (7), settlement belt (8), margin ledger
(9), squeeze (11), tower (12), fire sale (14), limits (17).

**3D.** Var(h, ρ) (3); P(liquidation | L, H) (9).

**New instruments** in `explainer/quant/viz.py`: `OrderBookLadder`, `NettingGraph`, `CollateralTower`, `MoneyMap`.

| Item | Min | Item | Min |
|---|---|---|---|
| `basis` (cm quarterly vs spot) | 1 | `liq_surface` (BTC 2020–25, 50×90) | 8 |
| `hedge` (ETH/BTC, bootstrap) | 2 | `imodel` (EWMA, λ fit, Kupiec; KF and BTC) | 5 |
| `book` (ZI, 200k × 8 seeds) | 10 | `squeeze` (grid × 8 seeds) | 15 |
| `auction`, `auction_live`, MOC | 1 | `repo`, `sofr_fan`, `reserve_curve` | 3 |
| `rfq` | 2 | `spiral` | 5 |
| `netting`, `duffie_zhu` | 10 | `fire_sale` | 3 |
| `waterfall` (10⁵ scenarios) | 10 | `fees`, `glm` | 5 |
| `settlement` | 2 | `index_rd` | 8 |
| `margin`, `funding` (existing) | 1 | `limits` | 3 |
| `industry` | <1 | **Total (4-core CPU)** | **≈ 95–115** |

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 2 · The Machinery of Markets (~60)
1. The instruments and how each is quoted: shares, bonds (clean and dirty), futures and forwards (contract specs,
   cost of carry F = Se^{(r−q)T} by replication, the basis converging at expiry), swaps, options (contract specs, the
   OCC), ETFs (price against NAV); hedging with futures (basis risk, the minimum-variance ratio h* = ρσ_S/σ_F,
   effectiveness ρ², beta hedging).
2. Exchanges and OTC: order types and validity, hidden orders; the order book as queues (price, visibility and time
   precedence; the cost of walking the book; the tick and the 2024 Rule 612 amendments); call auctions (the crossing
   maximizes volume, proved; the closing auction); dealer markets and RFQ (best of n against information leakage);
   wholesalers and payment for order flow.
3. Clearing and settlement: novation; netting (M ≤ B ≤ G, proved) and Duffie–Zhu on when a CCP raises exposure; the
   default waterfall and cover-2; DVP, CNS and T+1 (28 May 2024); NSCC's VaR deposit and ECP, and 27–28 January 2021.
4. Margin and leverage: initial, variation and maintenance margin; liquidation prices and the probability of
   liquidation (reflection principle against BTC data); portfolio margin; margin models (SPAN, EWMA VaR with λ fitted
   by likelihood, the Kupiec backtest) and procyclicality (1987, 2020; LME nickel 2022; UK LDI 2022).
5. Short selling: locate, borrow, the fee and the rebate, recalls, dividends; short interest above 100% by relending;
   squeeze dynamics; Volkswagen 2008.
6. Repo and securities lending: repo legs and rates, tri-party and bilateral; haircuts as leverage limits (1/h) and
   the deleveraging spiral; specials and the on-the-run premium (Duffie 1996); September 2019 and the reserve demand
   curve.
7. Prime brokerage: financing, custody, cross-margining; total return swaps; the race to sell (Archegos, 2021); the
   prime-brokerage run (Duffie 2010).
8. The players and their business models: sell side (flow and exotics, agency and principal), buy side (fees,
   high-water marks as options, pass-through), proprietary trading, market makers, retail brokers and PFOF; smoothed
   returns (Getmansky–Lo–Makarov) and option-like returns (Fung–Hsieh).
9. The quant industry map and the roles, placed by horizon and instrument (the industry chapter).
10. Markets around the world: the US, the EU and UK (T+1 on 11 October 2027), Japan, India (index options, SEBI's
    studies and 2024 measures), China (T+1, ±10% and ±20% limits, Stock Connect, the 2024 short-selling and
    program-trading rules); what price limits do to measured returns.
11. Benchmarks and indices: cap, float and price weighting; rebalancing demand; the inclusion effect (Shleifer 1986;
    the Russell regression discontinuity; benchmarking intensity) and its disappearance.

*Textbooks:* Hull OFOD ch. 1–3, 5, 10 (ch. 4, 6, 7 → Part 18); Harris *Trading and Exchanges* ch. 1–6 (ch. 7–8 → 35);
Tuckman–Serrat (repo chapter); Pedersen *Efficiently Inefficient* ch. 1, 5 (ch. 2–4 → 26, 30); Mishkin (financial
system overview).
*Computed:* the BTC quarterly basis converging (Binance, 2020–21); the ETH/BTC minimum-variance hedge in and out of
sample; a zero-intelligence order book; the closing auction built order by order; best-of-n RFQ; netting
(gross/bilateral/CCP) and Duffie–Zhu; a CCP default waterfall under stress; the settlement deposit under T+2/T+1/T+0;
10×/3×/2× BTC longs liquidated in March 2020 and the liquidation-probability surface 2020–25; EWMA margin fitted by
likelihood on 1926–2020 and BTC, with breach rates and procyclicality; a short squeeze against free float; the haircut
spiral; the reserve demand curve from FRED (2018–21) and the SOFR percentile fan of September 2019; a fire-sale race;
fees with a high-water mark on 1927–2020; return smoothing in the smallest size decile and by MLE; a Russell-style
regression discontinuity (simulated, truth known); price limits.
*Visuals:* a trade's life with a collateral clock; the order book as queues filling and emptying; auction staircases
crossing; the netting graph collapsing into the CCP; the waterfall draining; the settlement conveyor; margin as a
breathing band; 3D: hedge variance over (h, ρ) and liquidation probability over (leverage, horizon); the float tank
and the squeeze; the collateral tower crumbling; banks racing to sell; the smoothed shadow of a return path; index
money pouring at the Russell cutoff; the price-limit spring; the money map.
*Crisis:* Volkswagen, October 2008 (a squeeze on a ~6% free float); September 2019 repo; 28 January 2021, LME nickel
2022 and the UK LDI episode as inserts.
*Firms:* CME, DTCC/NSCC, Citadel Securities and Virtu (wholesaling and PFOF), Robinhood (January 2021), the prime
brokers in Archegos, the basis-trading hedge funds; regulators: the SEC (Rule 612, Treasury clearing), SEBI (F&O
studies; the Jane Street interim order, allegations), the FCA (LME).
*Desk:* "Make me a market on the number of trading days in a year." "Futures 102, spot 100, six months, 3%: trade?"
"Short interest is 120% of float: how?"
*House:* treasury and funding: margin (EWMA, liquidation), financing, borrow fees, haircuts and deleveraging, hedge
ratios, clearing and auctions, fees with a high-water mark; every later backtest pays them.
```

## 6. Minutes per chapter

| Ch | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Min | 3.0 | 2.5 | 3.5 | 3.0 | 3.0 | 3.0 | 3.5 | 2.5 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.5 | 3.0 | 2.5 | 3.0 | 3.0 | 3.0 | **≈ 60** |

At ~170 wpm (measured: 485 words → 2.8 min), 2.5 min ≈ 420 words and 3.5 min ≈ 600 words. The 50-min floor holds
even if every chapter runs 15% short.

## 7. Corrections and open checks

**Robinhood (current hook).** Replace "asked for about $3 billion … reduced to about $1.4 billion" with the SEC
wording: a $1.4 bn margin requirement, and a waived ECP charge that would have been more than double it. A court order
mentions a deposit deficit "of over $3 billion"
(https://www.docketalarm.com/cases/Florida_Southern_District_Court/1--21-md-02989/IN_RE--_January_2021_Short_Squeeze_Trading_Litigation/453/).
The "$3.4 bn raised" stat was not verified.

**Unverified; keep off screen until checked.** • SPAN's 16 scenarios. • EMIR anti-procyclicality parameters. • The
E-mini multiplier. • Metallgesellschaft figures. • Nomura's exact Archegos loss. • The LME's cancelled-trade value. •
Closing-auction volume shares, and Bogousslavsky–Muravyev's venue. • Pass-through fee levels. • D'Avolio's 9% and 4.3%
against the original. • DTCC's 98% netting. • Rule 612's status after 2 Nov 2026 (today).

**Data.** • New FRED series: `SOFR1`, `SOFR25`, `SOFR75`, `SOFR99`. • `binance_klines(..., market="futures/cm")` for
`BTCUSD_210326`.

Both were confirmed reachable (Binance publishes SHA-256 files), and running them adds entries to
`videos/quant/data/manifest.json`. Yahoo returned "Too Many Requests" here, so the GME, TSLA and VOW checks are
optional.

