# Quant, Built: the syllabus (plan of record, draft 2)

Goal: a course in video that is **as complete as the standard textbooks taken together, as technical as a PhD
course, and as close to the academic and industry frontier as possible**, with the industry inside it: how Jane
Street, Citadel, Renaissance, Millennium, Two Sigma, D. E. Shaw, AQR, Optiver, SIG, Virtu, XTX, High-Flyer and the
bank desks actually make (and lose) money, from the public record. As in *AI, Built*, **the models are trained**,
on the CPU that renders the video, on real data, with training replayed on screen, and the parts are **one
connected story**. The series builds one quant firm, desk by desk, and runs it in the finale. It is in English and
Chinese and renders on macOS and Linux. Each part runs **30–60 minutes**; the plan is **43 parts, about 38 hours**.

How a part is made follows [`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md): the layout, chapters, the rule
that narration follows the data, compute, the QA loop and the Chinese edition. The textbooks (with the part each
chapter maps to), the industry library and **the full paper list, part by part** are in [`READING.md`](READING.md).
This file has the standard, the devices, the threads and the parts.

## 1. The standard every part meets

**A chapter is a lecture segment of 3–5 minutes**, in the AI series' order:

1. A motivating question, a market fact, or a failure.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("Itô", "no arbitrage", "tower property",
   "complete the square").
4. A computed experiment or a trained model that checks the result. It uses real data where possible, and
   otherwise a `simulated` market whose truth is known.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**
- An objectives card, and theorem and definition cards.
- **A textbook line.** Which chapters of which standard books the part covers ([`READING.md`](READING.md)). A part
  may not drop a topic those chapters treat as core without saying where in the series it is.
- **A paper list.** Every paper the part cites, in full, is in the part's README and in [`READING.md`](READING.md)
  (classic papers, the frontier, and industry sources).
- **A crisis file.** The real event where the part's idea broke, measured from data.
- **A firm file.** The firms whose business is the part's subject: what they do, how they earn it, what went
  wrong, and the numbers they have disclosed. Taken from the public record only: published research, filings,
  prospectuses, regulatory orders, court records, books. Allegations are labeled as allegations, with the firm's
  response.
- **Desk questions.** Two or three interview-style problems on the part's material, in the tradition of the
  trading-firm interview (Zhou's *Green Book*, Crack's *Heard on the Street*, Joshi's *Quant Job Interview*,
  market-making games, Jane Street's published puzzles). Full solutions are in the part's README.
- **A problem set.** 4–6 problems, about 90 s on screen, with full solutions in the README in English and Chinese.
- **The House.** The part adds a component to the series' own quant firm (Section 2), and the org-chart card
  lights it.
- **A reference card.** Textbooks, the classic papers, the frontier papers, and industry sources.

**Training standard (from *AI, Built*).** Every model a part trains is shown learning:
- `TrainingReplay` shows the loss curve and the model's outputs (the hedge ratio, the predicted surface, the
  quotes, the portfolio) scrubbed through checkpoints together.
- Several seeds with the spread shown; baselines at equal budgets; the classical method as the benchmark.
- **Narration branches on the result.** When a deep model loses to HAR or to Almgren–Chriss, the video says so and
  says why.
- The model zoo is listed in Section 4.

**The history thread.** Every part opens with its era ("how we got here", 2–3 min), lit on the timeline strip
(1900–2030; ideas in gold, crises in red, firms in blue). Every idea is credited with its people and year.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the writing
date: journals, SSRN and arXiv working papers, and regulator and exchange publications. Items marked *(verify)* are
2024–2026 work or events recalled from secondary sources. Each is checked against the paper or filing before it
goes on screen, and dropped if it does not hold up. The sweep may add newer work. Every citation in
[`READING.md`](READING.md) (authors, year, title, venue) is checked in the same pass.

**Numbers are real.**
- Computed numbers come from `compute.py`, cached under `.cache/quantN/`. Published numbers are cited. Labels:
  `schematic`, `illustrative`, `simulated` (with its generating model stated).
- Data is frozen and checksummed (Section 5).
- CPU budget: ≤ 2 h per part by default. Named exceptions (Section 4) get ≤ 12 h, resumable and seeded.
- Scene assertions use tolerances, so macOS and Linux builds agree.

**The P/Q discipline.** Every result says which measure it lives under. Q-results are scored on the Surface or
against replication; P-results are scored on the Track Record, net of a stated cost model, with the trial counter
running. Colours: `C.Q` for risk-neutral objects, `C.P` for real-world ones.

**Visual standard** (*AI, Built*'s `explainer/ai/viz.py`, plus `explainer/quant/viz.py`):

| Instrument | What it shows |
|---|---|
| `VolSurface` | the implied-volatility surface in 3D, with a camera tour and model surfaces morphing onto it |
| `PathFan` | Monte Carlo paths, with the terminal density growing on the side and the payoff under it |
| `HedgeLedger` | a hedged book's P&L split live into gamma, theta, vega, carry and costs as the path runs |
| `BinomialTree` | the replication tree, with values flowing back and the hedge at each node |
| `PayoffDiagram` | payoffs and prices, Greeks as slopes and curvatures |
| `CurveMorph` | the yield curve through time, with PCA modes as handles |
| `FrontierPlot` | the efficient frontier, with estimation error as a cloud |
| `OrderBookLadder` | bids and asks with queues, orders arriving and cancelling (shared with `trading`) |
| `ImpactTrace` | a metaorder's price path, with the square root and the propagator decay |
| `CopulaCloud` | joint draws in the unit square, with the tails lit |
| `ContagionNet` | a financial network, losses flowing along exposures |
| `AMMCurve` | the constant-product curve, with a trade and the arbitrageur's take |
| `DrawdownStrip` | an equity curve with drawdowns shaded and the sealed-envelope line |
| `TrialCounter` | the running count of backtests, and the hurdle it raises |
| `TrainingReplay` | a learning curve and the model's behaviour scrubbed together (from *AI, Built*) |
| `HouseChart` | the House's org chart, desks lit as they are built, money flowing between them |
| `crisis_card` / `firm_card` / `desk_question` | the set pieces |

**Bilingual standard (as *AI, Built*).**
- Every narration line has its `narration_zh.json` entry.
- Every on-screen string is in `quant_text_zh.json`, and `collect_text.py --check quantN` is clean.
- `QUANT_ZH_GUIDE.md` holds the glossary in mainland textbook and industry usage: 风险中性测度, 隐含波动率曲面,
  粗糙波动率, 雪球, 做市, 冲击成本, 因子动物园, 回测过拟合, 指数增强, 多策略平台, and so on.
- `zh_follow_numbers.py` and `check_narration.py` are run in both languages.
- The Chinese edition gets the A-share material its audience expects (Section 6): T+1, price limits, the 2015 crash
  and the 2016 circuit breaker, snowballs, index enhancement, the February 2024 quant drawdown, and High-Flyer and
  DeepSeek.

**Gates per part:**
- `lecture_length.py` (fails under 30 min).
- `contact_sheet.py`, `dead_air.py`, `collect_text.py --check` and `check_narration.py`.
- `qa_series.py` and `qa_audio.py` once those tools take `--series quant`.
- `pytest tests/test_quant_house.py` for the House library.

## 2. The devices

### The House: the series builds a quant firm

The connecting story. `explainer/quant/house/` is a small, tested, open quant stack written over the course of the
series. Each part adds one component, used by every later part, the way *AI, Built* grows its autodiff library and
its scoreboard. A `HouseChart` card opens each part with the desks built so far.

| Desk | Components | Built in |
|---|---|---|
| Data & technology | point-in-time data layer, calendars, corporate actions, the event-driven backtester | 1–3, 26 |
| Volatility desk | surface builder (SVI/SSVI), pricers, calibrators, the deep hedger, the options quoting engine | 10–17 |
| Rates desk | curve builder, term-structure models, swap and swaption pricers | 18, 19 |
| Credit & XVA | hazard curves, CDS pricer, exposure engine, CVA/FVA with AAD | 20, 21 |
| Macro desk | FX and commodity curves, carry and trend books | 22, 32 |
| Research | signals, factor library, ML models, LLM features, alpha miners, the trial counter | 23–29, 33 |
| Portfolio & risk | the risk model, the optimizer, alpha combination, VaR/ES and stress reports | 30, 31, 40 |
| Execution | impact model, scheduler, smart order router, TCA | 37 |
| Market making | quoting engine, inventory control, ETF creation and redemption arbitrage | 38 |
| Digital assets | AMM LP book, perp funding arbitrage | 39 |
| Treasury & funding | margin, repo and financing costs, liquidity stress | 2, 18, 41 |
| Compliance & surveillance | limits, pre-trade checks, spoofing and manipulation detection | 34, 35 |

**The finale runs the House** on the sealed window. Signals from Research are combined, sized by Portfolio &
risk, executed through the impact model, and attributed. The result is reported as a firm reports it: P&L by desk,
Sharpe, drawdowns, capacity, costs, and risk-limit breaches.

### The Surface (the pricing scoreboard)

`explainer.quant.surface`, frozen in Part 1 (`.cache/quant1/surface.json`). One full options surface on one fixed
day, plus the next trading day for out-of-sample checks. The primary candidate is Deribit BTC (public, free,
hundreds of quotes); an equity-index surface is added if a licensable free source is found in Phase 0.

| Part | Rows |
|---|---|
| 10 | Black–Scholes, one vol per maturity |
| 12 | SVI, SSVI, a VAE surface model; local vol (Dupire) by repricing |
| 13 | Heston, SABR, Bates, variance gamma |
| 14 | rough Bergomi, quadratic rough Heston, path-dependent volatility |
| 17 | the neural calibrator (speed), a neural SDE |

Columns: in-sample implied-vol RMSE (vega-weighted, vol points), next-day RMSE with parameters held, static-arbitrage
violations, parameter count, and calibration time on this CPU.

### The Track Record and the sealed envelope (the investing scoreboard)

`explainer.quant.track`.
- All research uses data up to 31 December 2020. The hold-out runs from 1 January 2021 to the freeze date set in
  Phase 0.
- A strategy is registered in its part with a code hash, parameters, universe, cost model and trial count. The
  hold-out is opened for it once, in that part's last chapter, and the result is shown whatever it is.
- Rows: classic factors (24); a shrinkage SDF (25); the ML models (27); the LLM signal (28); the mined alphas (29);
  minimum-variance and HRP (30); the Gârleanu–Pedersen trader (31); trend, carry, risk parity and short volatility
  (32); PCA-residual and deep stat arb (33); crypto carry and momentum (39); the House (43).
- Columns: return, volatility, Sharpe with standard error, maximum drawdown, turnover, and Sharpe net of costs. The
  finale adds the deflated Sharpe.

### The trial counter

`explainer.quant.trials`. Every compute item that backtests declares how many configurations it tried. The
declarations are code, so the count regenerates. Part 26 introduces it with the count so far. Part 29's alpha
miners run it up by orders of magnitude and are deflated accordingly. The finale uses the full count.

### Crisis files, firm files, payoff cards, the timeline

Indexed part by part in Section 6. Payoff cards ("where this comes back") and the timeline strip are *AI, Built*'s
instruments, here on a 1900–2030 strip.

## 3. The threads: how the parts connect

Each thread is a story that runs across parts. A payoff card plants it, and the later part opens by calling back to
it.

| Thread | Path through the series |
|---|---|
| **The fair game** (Bachelier, P vs Q) | 1 (the claim) → 4 (martingales) → 9 (Q exists) → 23 (the SDF links P and Q) → 43 (beat it?) |
| **Thorp** | 1 (blackjack) → 8 (Kelly) → 10 (his warrant formula before Black–Scholes) → 33 (Princeton/Newport, the first quant fund) → 43 |
| **LTCM** | 8 (leverage and Kelly) → 10 (Merton and Scholes) → 18 (Salomon's bond arbitrage) → 41 (1998) |
| **Crowding** | 24 (momentum crash 2009) → 33 (quant quake 2007) → 12 (Volmageddon 2018) → 22 (yen carry 2024) → 29 (A-share quant drawdown, Feb 2024) → 42 (machines sharing a model) |
| **Roughness and self-excitation** | 5 (fBM, Hawkes) → 7 (rough realized vol) → 14 (rough volatility) → 36 (Hawkes order flow) → 37 (metaorders cause roughness) |
| **Control** | 8 (HJB, Merton) → 10 (hedging as control) → 17 (deep hedging) → 37 (Almgren–Chriss) → 38 (Avellaneda–Stoikov) → 42 (RL and MFG agents) |
| **Liquidity is the hidden factor** | 2 (repo and margin) → 21 (margin and CCPs) → 22 (the basis trade) → 37 (impact) → 41 (spirals) |
| **The overfitting thread** | 6 (multiple testing) → 25 (factor zoo) → 26 (trial counter) → 27 (low SNR) → 29 (alpha miners) → 43 (deflation) |
| **Correlation** | 15 (worst-ofs, dispersion) → 20 (the Gaussian copula) → 40 (tail dependence) → 41 (contagion) |
| **AI, Built** | AI 4 (autodiff) → 16; AI 8 (double descent) → 27; AI 13–14 (transformers) → 27, 28, 36; AI 21 (diffusion) → 17; AI 26 (RL) → 8, 37, 38, 42; and High-Flyer → DeepSeek (AI 14, 16) in 29 and 34 |
| **The existing videos** | `stochastic` → 5, 10; `trading` → 35–38 (its ITCH pipeline is read through its compute); `opposing_forces` → 3, 18, 23 |

## 4. The model zoo (what the series trains)

Every entry is trained or fitted in its part's `compute.py`, seeded, cached, and replayed on screen. **Bold**
entries are named compute exceptions (≤ 12 h, resumable).

| Part | Models |
|---|---|
| 6 | double/debiased ML for a treatment effect in returns; lasso vs post-lasso inference |
| 7 | GARCH family by MLE; HAR-RV; an LSTM and a small transformer volatility forecaster vs HAR; a time-series foundation model zero-shot |
| 8 | PPO on Merton's problem vs the closed form (AI 26's code) |
| 11 | an RL options market maker that learns to scalp gamma under costs |
| 12 | an arbitrage-free neural SVI; a VAE over daily vol surfaces (Bergeron et al. 2022) |
| 14 | Hawkes fits; the PDV model's kernel regression |
| 15 | a neural surrogate pricer for snowballs and worst-of autocallables |
| 17 | **the neural calibrator** (rough Bergomi); differential ML; deep BSDE (100 assets); deep optimal stopping; **the deep hedger** (CVaR, costs); a neural SDE; **a market generator** (signature WGAN and a diffusion model) |
| 19 | ML bond risk premia (Bianchi–Büchner–Tamoni) vs Cochrane–Piazzesi |
| 20 | default prediction: logit vs gradient boosting on fundamentals |
| 21 | a deep xVA solver (Gnoatto–Picarelli–Reisinger) vs Monte Carlo |
| 24 | Bayesian factor timing |
| 25 | the KNS shrinkage SDF; IPCA; RP-PCA |
| 27 | **gradient boosting and network ensembles** (Gu–Kelly–Xiu); random-feature "complex" timers; an autoencoder factor model; a deep SDF (GAN); **a cross-asset transformer** (AI 13's code); a CNN on price images |
| 28 | **time-sliced pocket language models** (`explainer.lm`); a FinBERT-style fine-tune; an open-weight LLM scored locally |
| 29 | **a genetic-programming alpha miner; an RL alpha miner (AlphaGen-style); an LLM-agent alpha miner** |
| 30 | an end-to-end portfolio network |
| 33 | **deep statistical arbitrage** (CNN + transformer residual policy) |
| 36 | DeepLOB; **a generative order-book transformer** |
| 37 | an RL executor vs Almgren–Chriss |
| 38 | an RL market maker vs Avellaneda–Stoikov/GLFT |
| 39 | an RL liquidity provider for concentrated liquidity |
| 40 | CAViaR and a deep quantile network vs filtered historical simulation |
| 42 | **multi-agent RL market makers** (collusion test); LLM-agent traders in the simulator |
| 43 | the House, end to end |

## 5. Data

All sources are free. Licences and redistribution terms are checked in Phase 0. Small permitted files are
committed under `videos/quant/data/`; otherwise a fetch module downloads them and checks a committed SHA-256.

| Source | What | Parts |
|---|---|---|
| Kenneth French data library | factors (1926–), sorted portfolios, industries | 1, 7, 23–26, 30, 31, 40 |
| Open Source Asset Pricing (Chen–Zimmermann) | 200+ predictor portfolios | 25–27, 29–31 |
| JKP global factor data | 153 factors × 93 countries | 24, 25 |
| Amit Goyal's Welch–Goyal data | monthly predictors | 27 |
| Robert Shiller's data | prices, dividends, earnings, CAPE since 1871 | 3, 23 |
| SEC EDGAR, XBRL financial statement data sets | filings and fundamentals | 3, 20, 28 |
| Fed FOMC statements and minutes | text | 28 |
| FRED; US Treasury; Fed (GSW, H.10, H.15); NY Fed (ACM, SOFR) | rates, curves, FX, spreads, VIX | 12, 18, 19, 22, 41 |
| EIA | WTI spot and futures | 22 |
| Deribit public API | BTC/ETH options surfaces with IVs; DVOL | 1, 9–17 (the Surface) |
| Binance public data | trades, klines, book depth, perp funding | 1, 7, 10, 33, 35–39 |
| Nasdaq TotalView-ITCH sample day (via `trading`) | every message, one day | 35–38 |
| Qlib's public A-share data *(verify: licence and survivorship)* | a stock-level A-share cross-section | 27, 29, 33 |
| Public filings (call reports, prospectuses, S-1s, regulatory orders) | firm and crisis numbers | firm and crisis files |

**What cannot be had for free, and what the series does instead:**
- CRSP stock-level US returns: characteristic portfolios, plus crypto and A-share cross-sections.
- SPX options: the Deribit surface, with SPX facts cited.
- TAQ and metaorder records: the ITCH day, Binance, published estimates, and `simulated` markets.
- Survivorship bias in free equity data is shown, not hidden (Part 26).

## 6. Part by part

Length targets are estimates. Each part lists *Textbooks*, *Computed/Trained*, *Visuals*, *Crisis*, *Firms*,
*Desk*, and *House*. Textbook short names and the full paper list for each part are in [`READING.md`](READING.md).

### Act I · Markets and Money

### Part 1 · The Fair Game (~50 min)
1. Paris, 1900: Bachelier's thesis, Poincaré's report, the rente market; Regnault's square-root-of-time law (1863).
2. Prices and returns: simple vs log, compounding, arithmetic vs geometric means, volatility drag σ²/2.
3. The random walk: Kendall (1953), Osborne (1959), Samuelson (1965), proved in its one-line form; Cowles (1933)
   on forecasters.
4. Testing it: autocorrelations and variance ratios (Lo–MacKinlay 1988) on 94 years of daily US returns.
5. The stylized facts (Cont 2001), each measured: heavy tails with an inverse cubic law, volatility clustering,
   leverage, aggregational Gaussianity.
6. Mandelbrot's cotton (1963) and the possibility that variance does not exist.
7. Efficient markets (Fama 1970); the joint-hypothesis problem; Grossman–Stiglitz (1980); Black's "Noise" (1986).
8. Two worlds, P and Q: a risk-neutral density beside a real-world one, both from data.
9. Who is on the other side? Hedgers, speculators, market makers, arbitrageurs; zero-sum before costs.
10. Thorp: blackjack (1962), *Beat the Market* (1967), and the first idea that markets can be beaten by
    mathematics.
11. The devices: the House (empty), the Surface frozen, the sealed envelope, the trial counter at zero.

*Textbooks:* CLM ch. 1–2; Bodie–Kane–Marcus (returns); Cont–Tankov ch. 1 (stylized facts).
*Computed:* stylized facts on Ken French daily returns (1926–2020) and Binance BTC; variance ratios; the Surface
frozen and cleaned.
*Visuals:* Bachelier's walk as his figure, then as 4 million steps; tails on log axes against the Gaussian.
*Crisis:* 19 October 1987: the S&P 500 fell 20.5%; how many sigmas a Gaussian gives it and how often a cubic tail
expects one.
*Firms:* the industry map, introduced: banks and dealers, asset managers, multi-manager funds, systematic funds,
prop trading and market makers.
*Desk:* "I flip a fair coin until heads; I pay you 2ⁿ. What do you pay to play?"
*House:* the data layer; the point-in-time rule.

### Part 2 · The Machinery of Markets (~55)
1. The instruments: equities, bonds, futures and forwards, swaps, options, ETFs; how each is quoted.
2. Exchanges and OTC: order types, auctions (open, close), continuous trading, dealer markets, request for quote.
3. Clearing and settlement: CCPs, novation, T+1 (May 2024), the DTCC; why settlement risk mattered on 28 January
   2021 (Robinhood's collateral call).
4. Margin and leverage: initial and variation margin, portfolio margin, the futures account marked to market daily.
5. Short selling: locate, borrow, the fee, recalls, short squeezes, Volkswagen 2008.
6. Repo and securities lending: the plumbing that funds the market; haircuts as leverage limits.
7. Prime brokerage: financing, synthetic exposure via swaps, cross-margining (Archegos preview).
8. The players and their business models: sell-side desks (flow vs exotics, agency vs principal), buy-side funds
   (fees, high-water marks, 2-and-20 vs pass-through), proprietary trading, market makers, retail brokers and
   payment for order flow.
9. The quant industry map: systematic equity, CTAs, stat arb, HFT, options market making, multi-strategy
   platforms, and the roles (quant researcher, trader, developer, risk quant, strat, structurer).
10. Markets around the world: US, Europe, Japan, India's index options boom, China's A-shares (T+1 for stocks,
    ±10% limits, the STAR board's ±20%, northbound Stock Connect).
11. Benchmarks and indices: index construction, rebalancing, the index-inclusion effect.

*Textbooks:* Hull OFOD ch. 1–7; Harris *Trading and Exchanges* parts I–II; Tuckman–Serrat (repo chapter);
Pedersen *Efficiently Inefficient* ch. 1–5.
*Computed:* futures mark-to-market and margin calls on a real contract's history; the cost of borrow across a
squeeze (published borrow-fee data, cited); index-inclusion event study on Ken French/OSAP data where possible.
*Visuals:* a trade's life from order to settlement as a moving token through brokers, the exchange, the CCP and
the custodian; the money map of who pays whom.
*Crisis:* Volkswagen, October 2008: briefly the world's most valuable company on a short squeeze.
*Firms:* Citadel Securities and Virtu (wholesalers and PFOF); Robinhood (January 2021); the multi-manager platforms
(fees as pass-through).
*Desk:* "Make me a market on the number of trading days in a year." (the market-making game)
*House:* treasury and funding: margin and financing costs in every later backtest.

### Part 3 · Value, Accounting and the Firm (~50)
1. Time value: NPV, IRR, annuities and perpetuities; Gordon growth.
2. The three statements: balance sheet, income, cash flows; accruals; what an analyst reads.
3. XBRL: machine-readable fundamentals from EDGAR, built point-in-time into the House.
4. DCF valuation: free cash flow, WACC, terminal value; its sensitivity to the discount rate (callback to
   `opposing_forces`).
5. Multiples: P/E, EV/EBITDA, CAPE; Shiller's data.
6. Modigliani–Miller (1958) derived by arbitrage; taxes, distress, and the trade-off theory.
7. Payout: dividends, buybacks, and the dividend irrelevance proof.
8. Equity as a call on the firm (Merton preview, Part 20); real options.
9. Earnings: announcements, surprises and post-earnings-announcement drift (Ball–Brown 1968; Bernard–Thomas 1989).
10. Accounting signals that became factors: accruals (Sloan 1996), F-score (Piotroski 2000), gross profitability
    (Novy-Marx 2013), forward-linked to Part 24.
11. Mergers and corporate events: merger arbitrage's payoff as a short put (Mitchell–Pulvino 2001).

*Textbooks:* Berk–DeMarzo; Brealey–Myers–Allen; Damodaran *Investment Valuation*; Koller et al. (McKinsey) *Valuation*.
*Computed:* a point-in-time fundamentals panel from XBRL; a DCF's sensitivity surface; accrual and profitability
sorts; a merger-arbitrage payoff from public deal data where available.
*Visuals:* the three statements as linked ledgers with cash flowing between them; the DCF's value as a 3D surface
over growth and discount rate.
*Crisis:* Enron (2001) and Wirecard (2020): when the statements lie, and what the accruals said.
*Firms:* fundamental quant ("quantamental") desks; merger-arbitrage funds.
*Desk:* "A firm with no debt buys back 10% of its shares at market. What happens to the price, and to EPS?"
*House:* the fundamentals store.

### Act II · The Mathematical Toolkit

### Part 4 · Martingales and Measure (~50)
1. Probability spaces and filtrations as information.
2. Conditional expectation as orthogonal projection; the tower property.
3. Martingales: Ville (1939) named them after a betting system; Doob.
4. Optional stopping: you cannot beat a fair game, and its hypotheses are why.
5. The doubling strategy, admissibility, and Barings (1995): doubling down in Leeson's "88888" account.
6. Doob decomposition: drift plus martingale.
7. Change of measure on a coin; Radon–Nikodym; equivalent measures agree on what is impossible.
8. Heavy tails: stable laws (Lévy; Fama 1965; Mantegna–Stanley 1995).
9. Martingale convergence; the gambler's ruin.
10. Game-theoretic probability (Shafer–Vovk): testing by betting, e-values, anytime-valid inference (Ramdas et al.
    2023).

*Textbooks:* Shreve I ch. 2–3; Williams *Probability with Martingales*; Föllmer–Schied ch. 1.
*Computed:* doubling-strategy drawdowns; stable-law fits; e-process tests of the martingale hypothesis.
*Visuals:* projection onto coarser partitions; the doubling strategy's equity curves with the rare ruin lit.
*Crisis:* Barings 1995. *Firms:* casinos and blackjack teams (the MIT team) as risk management.
*Desk:* "A martingale starts at 1 and stops at 0 or 3. Probability it hits 3?" and "Expected flips to HH?"
*House:* the e-value monitor (used again in Part 26).

### Part 5 · Stochastic Calculus (~55)
1. Brownian motion as the scaling limit (Donsker); quadratic variation.
2. The Itô integral; the isometry; Stratonovich.
3. Itô's lemma; GBM; Euler–Maruyama and Milstein with orders computed.
4. Ornstein–Uhlenbeck, CIR; Feynman–Kac.
5. Girsanov and Cameron–Martin: drift is a change of measure.
6. Martingale representation: why a hedge exists.
7. Local time, Tanaka, and the stop-loss start-gain paradox (Carr–Jarrow 1990).
8. Jumps: Poisson, compound Poisson, Lévy–Itô, Itô for jumps.
9. Point processes with memory: Hawkes (1971), the branching ratio. Comes back in 14 and 36.
10. Fractional Brownian motion: Hurst H, not a semimartingale.
11. Rough paths and signatures (Lyons 1998; Chen 1957). Come back in 14, 17 and 42.

*Textbooks:* Shreve II ch. 3–11; Øksendal; Karatzas–Shreve *Brownian Motion and Stochastic Calculus*; Cont–Tankov
ch. 2–8; Björk ch. 4–5.
*Computed:* QV convergence; strong and weak orders; Girsanov reweighting; stop-loss start-gain hedging error;
Hawkes simulation by thinning.
*Visuals:* `PathFan` with the Fokker–Planck surface; fBM at H = 0.1, 0.5, 0.9.
*Note:* `stochastic` is the gentle version; this part assumes it.
*Desk:* "E[W_t⁴]?"; "Probability Brownian motion hits 1 before −2?"; "Price a digital by Girsanov."
*House:* the simulation library (used by every pricing part).

### Part 6 · Financial Econometrics (~50)
1. Regression in finance: OLS, overlapping observations, HAC errors (Newey–West 1987), clustered errors.
2. Predictive regressions and the Stambaugh bias (1999).
3. MLE and GMM (Hansen 1982): the Euler equation estimated.
4. Event studies: abnormal returns, CARs, inference (MacKinlay 1997).
5. Panel methods: Fama–MacBeth vs pooled vs fixed effects; Petersen (2009) on standard errors.
6. Bootstrap for dependent data: block and stationary bootstrap.
7. Bayesian inference: priors as shrinkage; hierarchical models for many assets.
8. Multiple testing, previewed (FWER, FDR; to Part 25).
9. Causal inference: instruments, differences-in-differences, regression discontinuity (Russell index cutoffs),
   double/debiased ML (Chernozhukov et al. 2018).
10. The signal-to-noise problem: how many years to tell a Sharpe of 0.5 from 0.

*Textbooks:* CLM ch. 3–4, 7; Cochrane *Asset Pricing* part II; Bali–Engle–Murray; Hayashi.
*Computed/Trained:* Stambaugh bias by simulation; HAC vs naive t-stats on overlapping returns; double ML on a
planted effect; the years-to-significance curve.
*Visuals:* the confidence ellipse of (α, β) shrinking with years of data; the Stambaugh bias as a shifted
histogram.
*Desk:* "A strategy has Sharpe 1 over 4 years. What is the standard error?"
*House:* the statistics module (HAC, bootstrap, FDR).

### Part 7 · Time Series and Volatility (~55)
1. Stationarity, ARMA, Box–Jenkins.
2. Unit roots; spurious regression (Granger–Newbold 1974).
3. Cointegration (Engle–Granger 1987; Johansen 1991).
4. Regimes (Hamilton 1989); the Kalman filter.
5. ARCH (Engle 1982) and GARCH (Bollerslev 1986) by MLE; EGARCH, GJR; DCC (Engle 2002).
6. "Does anything beat a GARCH(1,1)?" (Hansen–Lunde 2005); robust losses (Patton 2011).
7. Realized volatility (Andersen–Bollerslev–Diebold–Labys); the signature plot; two-scale and realized kernels.
8. HAR-RV (Corsi 2009), HARQ; jumps by bipower variation.
9. Roughness in the data: log realized vol at H ≈ 0.1 (Gatheral–Jaisson–Rosenbaum 2018), measured.
10. Deep volatility forecasting: an LSTM and a small transformer against HAR, trained here.
11. Time-series foundation models (Chronos, TimesFM, Moirai) zero-shot on volatility.

*Textbooks:* Tsay *Analysis of Financial Time Series*; Hamilton *Time Series Analysis*; Aït-Sahalia–Jacod
*High-Frequency Financial Econometrics*.
*Trained:* GARCH family; HAR; LSTM and transformer forecasters (5 seeds); a foundation model zero-shot.
*Visuals:* volatility as a slow hidden river under the noisy returns; the signature plot collapsing.
*Crisis:* March 2020: each model's forecast the day before.
*Desk:* "Daily vol is 1%. What is the vol over a year? Over a week? When is √T wrong?"
*House:* the volatility forecaster.

### Part 8 · Decisions and Control (~55)
1. Expected utility, risk aversion, certainty equivalents.
2. Dynamic programming; HJB derived.
3. Merton's problem (1969/71), the fraction (μ − r)/(γσ²), by HJB and simulation.
4. Kelly (1956), fractional Kelly, Thorp; Samuelson's objection (1979); ergodicity, and the controversy.
5. Optimal stopping: Snell envelope; American options preview.
6. Prospect theory; ambiguity (Ellsberg; Gilboa–Schmeidler; Hansen–Sargent).
7. Viscosity solutions, briefly: why HJB needs them (Crandall–Lions).
8. BSDEs (Pardoux–Peng 1990; El Karoui–Peng–Quenez 1997).
9. Mean-field games (Lasry–Lions; Huang–Malhamé–Caines 2006).
10. Reinforcement learning for the same problems: PPO on Merton vs the closed form.

*Textbooks:* Pham *Continuous-time Stochastic Control*; Back *Asset Pricing and Portfolio Choice Theory* ch. 1–2,
14; Carmona–Delarue; Touzi.
*Trained:* PPO on Merton's problem (AI 26's code), with the learned policy converging to the Merton line.
*Visuals:* the HJB value function as a surface with the control flowing; Kelly's growth parabola.
*Crisis:* leverage beyond Kelly, using LTCM's published leverage (full story in 41).
*Firms:* Thorp's Princeton/Newport and Kelly sizing.
*Desk:* "You have a 60% coin at even odds. What fraction do you bet?"
*House:* the sizing module.

### Act III · Derivatives (Q)

### Part 9 · No Arbitrage (~50)
1. Arbitrage, the law of one price, put–call parity and its practical failures.
2. One period: the FTAP by separating hyperplanes (Farkas), proved.
3. State prices and the SDF; Q as the SDF renormalized.
4. The binomial tree (Cox–Ross–Rubinstein 1979).
5. Completeness; super-replication as an LP.
6. Continuous time: Harrison–Kreps, Harrison–Pliska, Delbaen–Schachermayer.
7. Change of numeraire; forward and annuity measures.
8. Breeden–Litzenberger: the density from the Surface.
9. Ross recovery (2015) and its critique (Borovička–Hansen–Scheinkman 2016).
10. Robust bounds: martingale optimal transport (Hobson 1998; Beiglböck–Henry-Labordère–Penkner 2013), by LP.

*Textbooks:* Shreve I; Björk ch. 1–3, 10, 26; Duffie DAPT ch. 1–2, 6; Delbaen–Schachermayer; Henry-Labordère
*Model-Free Hedging*.
*Computed:* the FTAP LP; the implied density; MOT bounds.
*Visuals:* the separating hyperplane; the tree folding back; the density emerging from the smile.
*Crisis:* GameStop 2021: put–call parity and borrow.
*Desk:* "Call 10, put 7, strike 100, spot 103, no rates. Arbitrage?"; box spreads, and the 2019 Robinhood
"infinite leverage" box-spread episode.
*House:* the arbitrage checker (used on every surface).

### Part 10 · Black–Scholes–Merton (~55; the pilot)
1. 1973: Black, Scholes, Merton; the CBOE opens; Thorp's earlier formula; the TI calculator on the floor.
2. Three derivations: replication PDE, risk-neutral expectation, the binomial limit.
3. The Greeks as geometry; Θ = −½Γσ²S² (at r = 0).
4. The hedging P&L ½ΓS²(σ²_realized − σ²_implied)dt, derived and watched.
5. Hedging with the wrong volatility (El Karoui–Jeanblanc–Shreve 1998).
6. Discrete hedging error ∝ 1/√N (Boyle–Emanuel 1980); Leland (1985).
7. Implied volatility by inversion (Jäckel, "Let's be rational").
8. American options and the free boundary.
9. Dividends, borrow and the forward.
10. 1987: portfolio insurance and the birth of the skew; MacKenzie's performativity thesis (the model made the
    market that fitted it, until 1987).
11. 1997 to 1998: the Nobel, then LTCM.
12. The Surface's first row.

*Textbooks:* Hull OFOD ch. 13–15, 19; Shreve II ch. 4–5; Björk ch. 7–9; Wilmott PWOQF ch. 5–8; Joshi *Concepts*
ch. 5–6; Taleb *Dynamic Hedging*.
*Computed:* hedging replays on GBM, on Heston paths, and on real BTC against Deribit implied vols; error vs
rebalancing; Leland checked.
*Visuals:* `HedgeLedger`; the tree converging to the PDE in 3D.
*Crisis:* 19 October 1987. *Firms:* the CBOE floor; O'Connor & Associates and the first option market makers to use
the model.
*Desk:* "ATM call, 1 year, vol 20%, spot 100: price it in your head" (≈ 0.4·σ·S·√T); "What's the delta of a
digital as T → 0?"
*House:* the vol desk opens: the BSM pricer and hedger.

### Part 11 · Trading Options (~50; the practitioner's part)
1. How an options trader thinks: positions as Greeks, P&L as gamma vs theta.
2. Gamma scalping on a real path, and the variance it captures.
3. Vega, vanna, volga: the second-order Greeks and the risk reversal and butterfly.
4. Strategies: straddles, strangles, spreads, calendars, risk reversals; what each bets on.
5. Volatility trading: realized vs implied, the volatility risk premium, the edge in forecasting it (Sinclair).
6. Pin risk and expiry; early exercise and dividend plays.
7. The options market maker's book: quoting the surface, hedging the residual, inventory in Greeks.
8. Dispersion: index vs single-stock vol, implied correlation.
9. The India expiry-day boom: weekly index options, retail flow, and SEBI's 2024 tightening.
10. Case file: the SEBI interim order against Jane Street (July 2025), *alleged* index manipulation on expiry days,
    contested by the firm. The mechanics alleged, explained with an index-and-options toy model.

*Textbooks:* Natenberg *Option Volatility and Pricing*; Sinclair *Volatility Trading* and *Positional Option
Trading*; Taleb *Dynamic Hedging*; Bennett *Trading Volatility*.
*Trained:* an RL options market maker that learns to scalp gamma under costs, compared with delta-hedging rules.
*Computed:* gamma-scalping P&L on BTC paths; implied correlation from index and component vols (where data allows).
*Visuals:* a P&L surface over (spot move, vol move) for each strategy; the scalper's trades on the path.
*Firms:* SIG (game theory and poker in training, from public interviews), Optiver, IMC, Jane Street.
*Desk:* the market-making game ("make a market on a die roll; now I tell you it's even"); "Long a straddle, the
stock doesn't move. How do you lose money?"
*House:* the options quoting engine.

### Part 12 · The Volatility Surface (~55)
1. Smile, skew, term structure; delta quoting; sticky strike vs sticky delta.
2. Static no-arbitrage: butterfly and calendar; Roper's conditions; Lee's moment formula.
3. SVI (Gatheral 2004) and SSVI (Gatheral–Jacquier 2014), fitted to the Surface.
4. Dupire (1994) local volatility derived; Derman–Kani; Gyöngy's projection.
5. Local volatility's forward smile.
6. Variance swaps and the log contract (Carr–Madan; Demeterfi–Derman–Kamal–Zou 1999).
7. The VIX derived and computed: our BTC index vs Deribit's DVOL.
8. The variance risk premium (Carr–Wu 2009; Bollerslev–Tauchen–Zhou 2009), measured; the SVIX lower bound on the
   expected market return (Martin 2017), computed.
9. Dealer gamma, intraday momentum (Baltussen et al. 2021); 0DTE (Bandi–Fusari–Renò 2023; Dim–Eraker–Vilkov 2024).
10. VIX futures, the roll, short-vol ETPs.
11. Learning surfaces: an arbitrage-free neural SVI and a VAE over daily surfaces (Bergeron–Fung–Hull–Poulos 2022).

*Textbooks:* Gatheral *The Volatility Surface*; Bergomi ch. 1–2; Rebonato *Volatility and Correlation*; Hull
OFOD ch. 20, 27.
*Trained:* neural SVI; the surface VAE on Deribit history, with its latent space explored.
*Visuals:* `VolSurface` tour; butterfly violations glowing; the variance-swap strip of options weighted 1/K².
*Crisis:* Volmageddon, 5 February 2018: the VIX more than doubled and XIV lost over 90%.
*Firms:* volatility funds and dealers' vol desks; the ETP issuers.
*Desk:* "Why is the VIX above realized volatility on average?"; "Replicate a variance swap with options."
*House:* the surface builder.

### Part 13 · Stochastic Volatility and Jumps (~55)
1. Why volatility must move.
2. Heston (1993): the characteristic function by Riccati; Feller; Andersen's QE scheme.
3. SABR (Hagan et al. 2002): the expansion, the backbone, its arbitrage at low strikes and the fixes.
4. Jumps: Merton (1976), Kou (2002), Bates (1996).
5. Lévy models: VG, CGMY, NIG; time changes (Carr–Wu 2004).
6. Stochastic local volatility; the particle method (Guyon–Henry-Labordère).
7. Bergomi's variance curve models; forward variance as the state.
8. The forward smile, cliquets, and model disagreement.
9. The SPX/VIX puzzle (Gatheral 2008).
10. Calibration: loss landscapes, identifiability, parameter instability.

*Textbooks:* Bergomi *Stochastic Volatility Modeling*; Gatheral ch. 2–5; Cont–Tankov ch. 4, 11, 13; Lewis
*Option Valuation under Stochastic Volatility*.
*Computed:* Heston, Bates, VG, SABR on the Surface; the calibration landscape in 3D; exotic-price dispersion across
models fitted to the same vanillas.
*Visuals:* the variance process as a second river; the optimizer wandering in a flat valley.
*Crisis:* post-1987 skew; implied trees (Rubinstein 1994).
*Desk:* "In Heston, what sets the skew? The smile's curvature?"
*House:* the calibrator.

### Part 14 · Rough and Path-Dependent Volatility (~60; frontier)
1. The fact: the ATM skew explodes like T^{H−1/2}.
2. Volatility is rough (Gatheral–Jaisson–Rosenbaum 2018), re-measured.
3. Rough Bergomi (Bayer–Friz–Gatheral 2016); the hybrid scheme (Bennedsen–Lunde–Pakkanen 2017).
4. Rough Heston (El Euch–Rosenbaum 2019): fractional Riccati and Adams.
5. Where roughness comes from: nearly unstable Hawkes (Jaisson–Rosenbaum 2016; El Euch–Fukasawa–Rosenbaum 2018).
6. Markovian lifts (Abi Jaber–El Euch 2019).
7. The debate: estimator bias, Cont–Das (2024), Guyon–El Amrani (2023); both sides' evidence shown.
8. Path-dependent volatility (Guyon–Lekeufack 2023), the 4-factor PDV.
9. The quadratic rough Heston (Gatheral–Jusselin–Rosenbaum 2020) and joint SPX/VIX.
10. Guyon's (2020, 2022) dispersion-constrained martingale Schrödinger problem.
11. Signature volatility models (Cuchiero–Gazzetta–Svaluto-Ferro 2023).
12. What desks use and why: speed, and Part 17's neural calibrators.

*Textbooks:* Bayer–Friz–Fukasawa–Gatheral–Jacquier–Rosenbaum (eds.) *Rough Volatility* (SIAM 2023);
Guyon–Henry-Labordère *Nonlinear Option Pricing*.
*Computed/Trained:* rBergomi and rough Heston on the Surface; skew power-law fits vs two-factor Bergomi; the PDV
kernel regression of DVOL on past BTC returns; the Hurst estimator's bias on simulated paths.
*Visuals:* fBM sharpening as H → 0; the skew term structure on log–log axes.
*Crisis:* 5 August 2024: the VIX printed 65 on thin pre-market quotes.
*Desk:* "Why can't a one-factor Markov SV model fit a 1-week skew?"
*House:* rough and PDV pricers.

### Part 15 · Exotics and Structured Products (~55)
1. The structuring business: why banks sell structured notes and who buys them.
2. Barriers: reflection principle, closed forms, the discrete-monitoring correction (Broadie–Glasserman–Kou 1997).
3. Asians, lookbacks, digitals and their hedging problems (the digital's exploding gamma; call-spread hedging).
4. Autocallables and snowballs (雪球): the payoff, why the seller is long volatility then short, and the knock-in
   cliff.
5. Worst-of and correlation: the correlation skew; dispersion.
6. Cliquets and forward-starting options: forward-smile risk (Part 13).
7. Uncertain volatility (Avellaneda–Levy–Parás 1995; Lyons 1995): pricing under model uncertainty, the nonlinear
   PDE.
8. Model risk and reserves: how desks mark exotics and price model uncertainty.
9. Dealer hedging flows and their market footprint (the autocallable vega supply that depresses long-dated
   implied volatility).
10. A neural surrogate pricer for the snowball book.

*Textbooks:* Hull OFOD ch. 26; Bouzoubaa–Osseiran *Exotic Options and Hybrids*; Guyon–Henry-Labordère; Wilmott
PWOQF (exotics chapters).
*Computed/Trained:* snowball pricing and Greeks by MC across spot; a CSI 500 snowball book's knock-in exposure
simulated through January–February 2024 using public index data; the neural surrogate's speed and error.
*Visuals:* the snowball's value surface over (spot, time) with the knock-in cliff; the dealer's vega flipping sign.
*Crisis:* the January–February 2024 A-share snowball knock-ins; Korea's HSCEI-linked ELS (2016 and 2024).
*Firms:* Chinese brokers' OTC derivatives desks; European and Korean structured-product issuers.
*Desk:* "Price a digital with a call spread. What width, and what happens to the hedge near expiry?"
*House:* the exotics pricer.

### Part 16 · Computing Prices (~60)
1. Monte Carlo at 1/√n.
2. Variance reduction: antithetics, control variates, importance sampling.
3. Quasi-Monte Carlo: Sobol, the Brownian bridge, effective dimension.
4. Multilevel Monte Carlo (Giles 2008): ε⁻²(log ε)² vs ε⁻³ for Euler paths.
5. Longstaff–Schwartz; duality bounds (Andersen–Broadie).
6. Greeks: bumps, pathwise, likelihood ratio (Broadie–Glasserman 1996).
7. AAD (Giles–Glasserman 2006): all Greeks for a small constant multiple of one price, with the series' autodiff
   (AI Part 4).
8. Finite differences: explicit, implicit, Crank–Nicolson, Rannacher; American options as an LCP.
9. ADI for Heston (Craig–Sneyd; in 't Hout–Foulon).
10. Fourier: Carr–Madan, Lewis, COS (Fang–Oosterlee 2008).
11. Hardware: GPUs in bank risk; quantum amplitude estimation's real speedup.

*Textbooks:* Glasserman *Monte Carlo Methods in Financial Engineering*; Savine *Modern Computational Finance*;
Andersen–Piterbarg vol. I; Duffy *Finite Difference Methods*; Seydel.
*Computed:* convergence races; MLMC cost; LSM vs binomial; AAD cost ratio; COS vs FFT.
*Visuals:* error vs cost for every method on one log–log plot; Sobol vs random; the AAD tape running backwards.
*Firms:* bank quant libraries and overnight risk runs.
*Desk:* "How many paths for a price to 1 bp?"; "Why is AAD's cost independent of the number of Greeks?"
*House:* the pricing engine.

### Part 17 · Deep Pricing and Hedging (~60; frontier)
1. Hutchinson–Lo–Poggio (1994).
2. Neural calibration (Horvath–Muguruza–Tomas 2021).
3. Differential ML (Huge–Savine 2020).
4. Deep BSDE (Han–Jentzen–E 2018) in 100 dimensions.
5. Deep optimal stopping (Becker–Cheridito–Jentzen 2019).
6. Deep hedging (Buehler–Gonon–Teichmann–Wood 2019): CVaR, costs, indifference prices.
7. What the deep hedger learns: Leland and Whalley–Wilmott bands, rediscovered.
8. Neural SDEs with robust exotic bounds (Gierjatowicz et al. 2022).
9. Market generators: Quant GANs (Wiese et al. 2020), signature generators (Buehler et al. 2020), diffusion
   models (AI Part 21); judged by signature MMD and the stylized facts.
10. Production: model risk, validation (SR 11-7), what has reached desks *(verify: public deployments)*.

*Textbooks:* Dixon–Halperin–Bilokon *Machine Learning in Finance*; Kelly–Xiu *Financial Machine Learning*.
*Trained:* the neural calibrator; differential ML; deep BSDE; deep stopping; **the deep hedger** (replayed: the
hedge surface sharpening into a no-trade band); a neural SDE; **the market generator** (signature WGAN and a
diffusion model), scored on Part 1's stylized facts.
*Visuals:* the learned hedge as a surface in (time, spot); real vs generated paths in a lineup.
*Firms:* J.P. Morgan's published deep-hedging work.
*Desk:* "Your hedger has costs. Why does the optimal hedge have a band?"
*House:* the deep hedger and the market generator (the finale stress-tests the House with it).

### Part 18 · Money, Bonds and the Curve (~55)
1. Money and central banks: the policy rate, reserves, the Fed's floor system, QE and QT; the Taylor rule.
2. Bonds, yields, forwards, bootstrapping; day counts and conventions.
3. Duration, convexity, the Taylor ladder; DV01 and key-rate durations.
4. Curve fitting: Nelson–Siegel, Svensson, the Fed's GSW curve.
5. PCA: level, slope, curvature (Litterman–Scheinkman 1991).
6. Swaps: pricing, the swap spread, and its negative turn after 2015.
7. Treasury futures: the conversion factor and cheapest-to-deliver.
8. Repo and funding: special repo, the repo spike of September 2019.
9. LIBOR's end: the scandal, SOFR, compounded in arrears.
10. Expectations vs term premium (ACM; Kim–Wright); macro announcements as event studies (CPI, payrolls, FOMC).
11. Relative value: butterflies, curve trades, Salomon's arbitrage group and the birth of LTCM.

*Textbooks:* Tuckman–Serrat *Fixed Income Securities*; Fabozzi *Handbook of Fixed Income*; Veronesi *Fixed Income
Securities*; Hull OFOD ch. 4, 7, 9.
*Computed:* bootstrapped and NSS curves; PCA on GSW daily; swap and futures pricing; SOFR compounding; macro-day
event studies on 2-year yields.
*Visuals:* `CurveMorph` through three decades; PCA handles; duration as tangent, convexity as gap.
*Crisis:* September 2022 gilts and LDI; SVB, March 2023, its held-to-maturity loss from public filings.
*Firms:* Salomon Brothers (Meriwether's group); primary dealers; relative-value hedge funds.
*Desk:* "A 10-year zero yields 4%. Duration? Price change for +1 bp?"; "Why does convexity cost money?"
*House:* the curve builder and the rates desk.

### Part 19 · Term-Structure Models (~55)
1. Short-rate models: Vasicek, CIR, Hull–White, Black–Karasinski; trees.
2. Affine term structures (Duffie–Kan 1996); the Riccati system.
3. HJM (1992): the drift condition derived.
4. The LIBOR market model (BGM; Jamshidian 1997); the forward market model for SOFR (Lyashenko–Mercurio 2019).
5. Caps, floors, swaptions; Black vs Bachelier; SABR for rates; negative rates.
6. Bermudan swaptions: callable products, exercise boundaries, LSM.
7. Multi-curve and collateral discounting.
8. Bond risk premia: Cochrane–Piazzesi (2005) and machine learning (Bianchi–Büchner–Tamoni 2021).
9. Macro-finance term-structure models (Ang–Piazzesi 2003).
10. The convexity of mortgages: prepayment and negative convexity; MBS hedging flows.

*Textbooks:* Brigo–Mercurio *Interest Rate Models*; Andersen–Piterbarg vols. II–III; Rebonato; James–Webber.
*Computed/Trained:* Hull–White calibrated to caps; HJM drift check; a Bermudan by LSM; Cochrane–Piazzesi and
neural bond risk premia (seeds, honest comparison).
*Visuals:* the forward curve's evolution under HJM; the Bermudan exercise boundary.
*Crisis:* the 1994 bond massacre and Orange County; the 2020 negative-rate shift to Bachelier quotes.
*Firms:* agency MBS desks, mortgage REITs.
*Desk:* "Why is a Bermudan worth more than its most expensive European?"
*House:* term-structure models.

### Part 20 · Credit (~50)
1. Merton (1974); distance to default; KMV; Black–Cox.
2. Intensities (Jarrow–Turnbull; Duffie–Singleton); survival as discounting.
3. CDS: legs, bootstrapping, the 2009 Big Bang; the CDS–bond basis.
4. Default prediction: Altman's Z (1968), logit (Shumway 2001; Campbell–Hilscher–Szilagyi 2008), gradient
   boosting, trained on fundamentals.
5. Vasicek's large pool and the Basel IRB formula.
6. Gaussian copula (Li 2000), CDO tranches, base correlation, the t-copula.
7. 2008: structured finance (Coval–Jurek–Stafford 2009), ratings.
8. The distress puzzle: distressed stocks earn less (Campbell–Hilscher–Szilagyi 2008).
9. Credit factors and corporate bond markets: illiquidity, ETFs, and March 2020.
10. Private credit: the asset class's growth and its marks.

*Textbooks:* O'Kane *Modelling Single-name and Multi-name Credit Derivatives*; Schönbucher; Duffie–Singleton;
Lando.
*Computed/Trained:* distances to default from public balance sheets; logit vs gradient boosting default models;
tranche losses under copulas.
*Visuals:* `CopulaCloud`; the tranche waterfall.
*Crisis:* 2007–08 senior tranches; the London Whale (2012, J.P. Morgan's CIO, about $6.2 bn).
*Firms:* J.P. Morgan's invention of the CDS (1994); credit hedge funds.
*Desk:* "A 5-year CDS trades at 100 bp, recovery 40%. Annual default probability?" (≈ s/(1 − R))
*House:* credit desk.

### Part 21 · Counterparty Risk, XVA and Clearing (~50)
1. Exposure: EE, PFE, netting sets, collateral.
2. CVA and DVA derived; wrong-way risk.
3. FVA (Burgard–Kjaer 2011), the FVA debate (Hull–White 2012), KVA, MVA.
4. Exposure by Monte Carlo with AAD sensitivities (Part 16).
5. A deep xVA solver (Gnoatto–Picarelli–Reisinger) vs Monte Carlo.
6. Initial margin: ISDA SIMM; the cost of margin.
7. Central clearing: CCP waterfalls, default management, margin procyclicality.
8. Bank capital: SA-CCR, CVA capital, leverage ratio, and why balance sheets became expensive (Part 22).

*Textbooks:* Gregory *The xVA Challenge*; Green *XVA*; Brigo–Morini–Pallavicini.
*Trained:* the deep xVA solver.
*Computed:* a swap portfolio's exposure profile, CVA/FVA and AAD sensitivities; a CCP waterfall stress.
*Visuals:* exposure fans over the swap's life; the CCP waterfall filling.
*Crisis:* Archegos (March 2021); LME nickel (March 2022).
*Firms:* bank XVA desks; CCPs (LCH, CME, ICE).
*Desk:* "Why does a bank's DVA increase as its credit gets worse, and is that profit real?"
*House:* the XVA engine.

### Part 22 · FX, Commodities and the Basis (~55)
1. Covered interest parity and its violation (Du–Tepper–Verdelhan 2018).
2. UIP and the forward-premium puzzle (Fama 1984); carry and crash risk (Brunnermeier–Nagel–Pedersen 2008;
   Lustig–Roussanov–Verdelhan 2011).
3. FX options: Garman–Kohlhagen, delta conventions, risk reversals and butterflies, the vanna–volga method.
4. FX regimes and attacks: Soros and Black Wednesday (1992); the SNB (2015).
5. Commodities: storage, convenience yield, contango, the roll; Gorton–Rouwenhorst (2006).
6. Energy and power: seasonality, spikes, spread options; the 2021–22 European gas crisis.
7. Negative oil (20 April 2020) and CME's switch to Bachelier (22 April).
8. The Treasury basis trade: mechanics, leverage, March 2020, its size since *(verify: Fed and OFR)*.
9. Inflation: TIPS breakevens, inflation swaps, the risk premium.

*Textbooks:* Clark *Foreign Exchange Option Pricing*; Wystup; Geman *Commodities and Commodity Derivatives*;
Eydeland–Wolyniec.
*Computed:* CIP deviations; a carry book and its skew; WTI curves and roll; vanna–volga on an FX smile; breakevens.
*Visuals:* the CIP triangle with the leak widening; futures curves flipping.
*Crisis:* SNB 2015; yen carry, August 2024; Amaranth (2006, about $6 bn on natural gas).
*Firms:* global macro funds; commodity traders; Optiver's 2007 crude case (CFTC, settled).
*Desk:* "USD rates 5%, JPY 0%: is the yen forward at a premium or a discount? Why doesn't carry arbitrage it away?"
*House:* the macro desk.

### Act IV · Return Premia (P)

### Part 23 · Risk and Return (~55)
1. Markowitz (1952); the frontier by Lagrange; Tobin's separation.
2. CAPM derived; the SML; Roll's critique.
3. SDF: p = E[mx]; Hansen–Jagannathan bounds.
4. APT (Ross 1976); ICAPM (Merton 1973).
5. Consumption: Lucas, CCAPM, GMM.
6. The equity premium puzzle; habit, long-run risk, disasters.
7. Excess volatility (Shiller 1981); the Campbell–Shiller decomposition.
8. Intermediary asset pricing (He–Krishnamurthy; Adrian–Etula–Muir; He–Kelly–Manela).
9. Demand systems and inelastic markets (Koijen–Yogo 2019; Gabaix–Koijen 2021).
10. Behavioural finance and limits to arbitrage (Barberis–Thaler 2003; Shleifer–Vishny 1997).
11. Bubbles: theory and evidence (Greenwood–Shleifer–You 2019), the dot-com era.

*Textbooks:* Cochrane *Asset Pricing*; Campbell *Financial Decisions and Markets*; Back; Duffie DAPT; Shleifer
*Inefficient Markets*.
*Computed:* frontiers; HJ bounds; the puzzle's implied risk aversion; Campbell–Shiller on Shiller's data.
*Visuals:* the bullet frontier with a swinging tangency line; the HJ cone.
*Desk:* "Two assets, σ = 20% each, ρ = 0.5. Minimum-variance weights and volatility?"
*House:* the expected-return framework.

### Part 24 · Factors (~55)
1. GRS and Fama–MacBeth.
2. Size, value, the three-factor model.
3. Momentum, time-series momentum.
4. Momentum crashes (Daniel–Moskowitz 2016).
5. Profitability and investment; five factors; q-factors.
6. Low risk: BAB and low volatility.
7. Value and momentum everywhere; carry everywhere; quality.
8. Value's lost decade, measured.
9. ESG and climate: green returns (Pástor–Stambaugh–Taylor 2022).
10. Factor timing and factor momentum.
11. A-share factors: size, the shell premium, and reversal (Liu–Stambaugh–Yuan 2019).
12. The Track Record opens for the classic factors.

*Textbooks:* Ang *Asset Management*; Ilmanen *Expected Returns*; Bali–Engle–Murray; Pedersen ch. 9–12.
*Computed:* Fama–MacBeth and GRS; each factor's history and crashes; value's spread; an A-share factor check.
*Visuals:* the SML through the cloud of portfolios; momentum with 2009 lit.
*Crisis:* the momentum crash, March–May 2009.
*Firms:* AQR, DFA, and the factor-ETF industry.
*Desk:* "Momentum and value are negatively correlated. Why hold both?"
*House:* the factor library.

### Part 25 · The Factor Zoo (~55)
1. Hundreds of factors; t > 3 (Harvey–Liu–Zhu 2016).
2. Multiple testing: FWER, FDR.
3. Replication: Hou–Xue–Zhang (2020) vs Jensen–Kelly–Pedersen (2023).
4. Open Source Asset Pricing.
5. Post-publication decay (McLean–Pontiff 2016).
6. Data-mined vs peer-reviewed (Chen–Lopez-Lira–Zimmermann 2024).
7. Shrinking the cross-section (Kozak–Nagel–Santosh 2020).
8. Taming the factor zoo (Feng–Giglio–Xiu 2020).
9. Weak factors (Giglio–Xiu 2021; Giglio–Xiu–Zhang 2023).
10. PCA, RP-PCA, IPCA.
11. Bayesian comparison (Barillas–Shanken 2018).
12. The shrinkage SDF registered and opened.

*Textbooks:* Kelly–Xiu *Financial Machine Learning*; Bali–Engle–Murray.
*Trained:* KNS SDF, IPCA, RP-PCA.
*Computed:* t-statistic distribution; FDR discoveries; decay.
*Visuals:* the hurdle sliding from 2 to 3; the shrinkage path.
*Desk:* "200 strategies, all noise. Expected best t-stat?"
*House:* the SDF model.

### Part 26 · Backtesting Without Fooling Yourself (~55)
1. The biases, each with a planted error: look-ahead, survivorship, selection, point-in-time.
2. The event-driven backtester: fills, latency, costs, borrow, corporate actions; vectorized vs event-driven.
3. The Sharpe ratio's error (Lo 2002); minimum backtest length.
4. The trial counter so far; the expected maximum Sharpe of N trials, from EVT.
5. Deflated Sharpe (Bailey–López de Prado 2014); PBO by CSCV.
6. Purged and embargoed CV; walk-forward.
7. Reality checks: White (2000), Hansen SPA (2005), Romano–Wolf.
8. Technical rules that weren't (Sullivan–Timmermann–White 1999), re-run.
9. E-value monitoring of live strategies (Part 4).
10. Planted-alpha tests in a `simulated` market.
11. How firms decide to fund a strategy: research reviews, incubation, paper trading, capital ramps.

*Textbooks:* López de Prado *Advances in Financial Machine Learning* ch. 7–14; Isichenko *Quantitative Portfolio
Management* ch. 7.
*Computed:* 10,000 random rules, deflated; PBO; purged CV; survivorship demo.
*Visuals:* `TrialCounter` and the hurdle; the best-of-N distribution sliding right.
*Crisis:* published strategies that died out of sample.
*Desk:* "Your backtest has Sharpe 3. List what could be wrong."
*House:* the backtester and the trial counter.

### Part 27 · Machine Learning for Returns (~60; frontier)
1. Low signal-to-noise (Israel–Kelly–Moskowitz 2020).
2. Gu–Kelly–Xiu (2020).
3. Economic restrictions (Avramov–Cheng–Metzker 2023).
4. The virtue of complexity (Kelly–Malamud–Zhou 2024), replicated; double descent (AI Part 8).
5. The critics *(verify: Nagel 2025; Buncic 2025)*, re-run on the same data.
6. Autoencoder asset pricing (Gu–Kelly–Xiu 2021).
7. Deep SDFs with adversarial moments (Chen–Pelger–Zhu 2024).
8. Transformers across assets *(verify: Kelly–Kuznetsov–Malamud–Xu 2025)*.
9. Images of prices (Jiang–Kelly–Xiu 2023).
10. Foundation models *(verify: Kronos 2025)*, zero-shot, tested honestly.
11. The practitioner's toolkit (López de Prado 2018): information-driven bars, triple-barrier labels,
    meta-labeling, fractional differentiation, sample weights; each tested against its simple alternative.
12. Conformal prediction.
13. The ML strategies registered and opened.

*Textbooks:* Kelly–Xiu; López de Prado *ML for Asset Managers*; Dixon–Halperin–Bilokon; Jansen *ML for
Algorithmic Trading*.
*Trained:* boosting and network ensembles (seeds), the random-feature timers, an autoencoder, a deep SDF, a
cross-asset transformer, a chart CNN, a foundation model zero-shot; on characteristic portfolios, crypto and
A-shares.
*Visuals:* out-of-sample R² vs complexity; interaction maps; attention across assets; `TrainingReplay` on each.
*Firms:* Two Sigma and Renaissance (public record; the Medallion fund's reported returns via Zuckerman).
*Desk:* "Your model has monthly R² of 1%. Is that good? What Sharpe does it imply?"
*House:* ML signals.

### Part 28 · Text, LLMs and Alternative Data (~55; frontier)
1. Tetlock (2007); Loughran–McDonald (2011).
2. SESTM (Ke–Kelly–Xiu 2019); FinBERT.
3. Text as macro data (Bybee–Kelly–Manela–Xiu 2024); FOMC (Hansen–McMahon–Prat 2018).
4. LLMs read the news (Lopez-Lira–Tang 2023); LLM embeddings (Jiang–Kelly–Xiu 2022); LLM statement analysis
   (Kim–Muhn–Nikolaev 2024).
5. Look-ahead bias (Glasserman–Lin 2023; Sarkar–Vafa 2024); chronologically consistent models *(verify:
   He–Lv–Manela–Wu 2025)*.
6. The time-sliced experiment, trained here.
7. LLM trading agents *(verify: TradingAgents 2024 and successors)*.
8. Alternative data: satellites, card panels, web traffic, job postings; decay as it spreads.
9. BloombergGPT (2023) vs general models.
10. The LLM signal registered and opened.

*Textbooks:* Kelly–Xiu ch. on text; Gentzkow–Kelly–Taddy "Text as data" (2019).
*Trained:* time-sliced pocket LMs on FOMC and EDGAR text (`explainer.lm`); a FinBERT-style classifier; an
open-weight LLM run locally.
*Computed:* FOMC hawkishness vs 2-year moves; the look-ahead gap.
*Visuals:* FOMC sentences lighting up; the gap opening between models.
*Firms:* news-analytics vendors; Bloomberg.
*Desk:* "Your LLM signal backtests at Sharpe 4 on 2015–2020 news. What's the first thing you check?"
*House:* text features.

### Part 29 · Alpha Mining and Automated Research (~55; frontier)
1. The alpha factory: formulaic alphas (Kakushadze 2016), WorldQuant's model and its public BRAIN platform.
2. Genetic programming for alphas: the search space, fitness, bloat, overfitting.
3. RL alpha mining (AlphaGen, Yu et al. 2023): generating synergistic alpha sets.
4. LLMs as quant researchers: Alpha-GPT (2023), agentic research loops *(verify: R&D-Agent-Quant 2025;
   AlphaAgent 2025)*.
5. Combining thousands of weak alphas (Part 31 preview): correlation, decay, capacity.
6. The trial counter explodes: what a million searched formulas does to the hurdle.
7. China's quant industry: index enhancement (指数增强), the 2019–2023 boom, the February 2024 micro-cap drawdown,
   DMA products, regulators' response.
8. High-Flyer (幻方): from a quant fund to DeepSeek (AI Parts 14, 16).
9. What remains for humans: economic priors, data, and judgment.

*Textbooks:* Kakushadze–Serur *151 Trading Strategies*; Isichenko ch. 2–3.
*Trained:* a GP miner, an RL miner, and an LLM-agent miner on the A-share and crypto cross-sections, all on the
trial counter and deflated.
*Visuals:* the formula tree growing; the hurdle rising with the search.
*Crisis:* February 2024 A-share quant drawdown.
*Firms:* WorldQuant; High-Flyer; Ubiquant and the Chinese quant private funds (public record).
*Desk:* "You mined 10,000 alphas with average out-of-sample IC 0.01 and correlation 0.3. What's the combined IC?"
*House:* the alpha miners (the finale uses only what survives deflation).

### Act V · Portfolios, Strategies and the Firm

### Part 30 · Portfolio Construction (~55)
1. Error maximization (Michaud 1989); 1/N (DeMiguel–Garlappi–Uppal 2009).
2. Covariance in high dimension: Marchenko–Pastur; RMT cleaning (Laloux et al. 1999; Bun–Bouchaud–Potters 2017).
3. Ledoit–Wolf, linear and nonlinear.
4. Constraints as shrinkage (Jagannathan–Ma 2003).
5. Black–Litterman.
6. Risk parity and ERC; HRP (López de Prado 2016).
7. Robust optimization; CVaR as an LP (Rockafellar–Uryasev 2000).
8. Kelly portfolios; Cover's universal portfolio; stochastic portfolio theory (Fernholz).
9. Entropy pooling and views (Meucci).
10. End-to-end portfolios trained on the decision loss.
11. Minimum-variance and HRP registered and opened.

*Textbooks:* Meucci *Risk and Asset Allocation*; Grinold–Kahn ch. 14–15; Paleologo *Advanced Portfolio
Management*; Chincarini–Kim.
*Trained:* the end-to-end portfolio network.
*Computed:* frontiers with error clouds; MP vs empirical spectra; LW vs RMT vs sample.
*Visuals:* the true and estimated frontiers diverging; the spectrum against MP.
*Desk:* "Why does the optimizer love the asset with the most estimation error?"
*House:* the optimizer.

### Part 31 · Risk Models, Costs and Trading Through Time (~55)
1. The fundamental law (Grinold 1989), derived and its limits.
2. Factor risk models (Barra-style): industries and styles, specific risk, Bayesian shrinkage of betas; estimated.
3. Transaction costs (Frazzini–Israel–Moskowitz 2018; Novy-Marx–Velikov 2016).
4. Gârleanu–Pedersen (2013): the aim portfolio, derived.
5. Multi-period optimization (Boyd et al. 2017).
6. Alpha combination: shrinkage, the "mega-alpha"; forecast horizon blending.
7. Signal decay, turnover, capacity; Berk–Green (2004).
8. Crowding (Lou–Polk); factor-neutral books; hedging the residual.
9. P&L attribution: factor vs idiosyncratic, timing vs selection.

*Textbooks:* Grinold–Kahn *Active Portfolio Management*; Isichenko; Paleologo *The Elements of Quantitative
Investing*; Narang *Inside the Black Box*.
*Computed:* a Barra-style risk model on portfolios and A-shares; GP vs myopic trading net of costs; capacity curves;
ridge alpha combination.
*Visuals:* the aim portfolio as a moving target; the capacity curve bending.
*Crisis:* August 2007 (Khandani–Lo), seen through the risk model.
*Firms:* risk-model vendors; systematic equity funds.
*Desk:* "IC 0.05, 500 stocks, monthly rebalancing. Information ratio?"
*House:* the risk model, the alpha combiner, attribution.

### Part 32 · Systematic Macro and Alternative Premia (~55)
1. Trend following: a century of evidence (Hurst–Ooi–Pedersen 2017); the CTA business; why it pays in crises.
2. Volatility targeting and its effect (Moreira–Muir 2017) and the critique (Cederburg et al. 2020).
3. Carry across asset classes (Part 22, 24) as one book.
4. Risk parity: Bridgewater's All Weather (1996), the leverage it needs; 2022 when stocks and bonds fell together.
5. Selling volatility and insurance: the premium and the left tail (Part 12).
6. Event-driven: merger arbitrage, index rebalancing, earnings drift.
7. Seasonality and calendar effects; the turn of the month; overnight vs intraday returns.
8. Managed futures in 2008 and 2022.

*Textbooks:* Pedersen *Efficiently Inefficient* ch. 9–15; Ilmanen; Kakushadze–Serur; Clenow *Following the Trend*.
*Computed:* trend, carry, risk-parity, vol-targeting and short-vol books on public futures-like data (Ken French
and FRED proxies; crypto perps); their crisis behaviour.
*Visuals:* the trend book's "smile" against market returns; the risk-parity leverage dial.
*Crisis:* 2022: the stock–bond correlation flip.
*Firms:* Man AHL, Winton, AQR managed futures, Bridgewater.
*Desk:* "Why does trend following have positive skew?"
*House:* the macro books.

### Part 33 · Statistical Arbitrage (~50)
1. History: Morgan Stanley's APT group (Tartaglia), D. E. Shaw (1988), Princeton/Newport.
2. Pairs (Gatev–Goetzmann–Rouwenhorst 2006), re-run.
3. Cointegrated pairs; half-lives.
4. OU trading rules (Bertram 2010; Leung–Li 2015), derived.
5. PCA and ETF residuals (Avellaneda–Lee 2010).
6. Kalman hedge ratios.
7. Lead–lag and reversal (Lo–MacKinlay 1990).
8. Deep stat arb (Guijarro-Ordonez–Pelger–Zanotti 2022), trained.
9. Crowding and decay.
10. Registered and opened.

*Textbooks:* Chan *Algorithmic Trading*; Pole *Statistical Arbitrage*; Avellaneda–Lee.
*Trained:* deep stat arb on ETFs, crypto perps and A-shares (seeds).
*Visuals:* the spread in its OU band; eigenportfolios.
*Crisis:* the August 2007 quant quake (Khandani–Lo).
*Firms:* D. E. Shaw, Morgan Stanley's PDT, Renaissance.
*Desk:* "A spread is OU with half-life 5 days. When do you enter?"
*House:* the stat-arb book.

### Part 34 · Inside a Quant Firm (~55; industry)
1. Business models: proprietary trading (Jane Street, HRT, Jump, XTX), market making (Citadel Securities, Virtu,
   Optiver), multi-manager platforms (Millennium, Citadel, Balyasny, Point72), systematic funds (Renaissance, Two
   Sigma, D. E. Shaw, AQR, Man), bank desks, and Chinese quant private funds.
2. What has been disclosed: Virtu's S-1 (one losing day in 1,238); Jane Street's debt-offering disclosures
   *(verify: revenue figures)*; Renaissance's Medallion returns (Zuckerman); fund letters and SEC filings.
3. The pod model: capital allocation, drawdown stops, pass-through fees, and the talent market; the
   Millennium–Jane Street lawsuit over an India options strategy (2024, settled).
4. The research process: idea, data, backtest, review, incubation, capital.
5. Risk management at a firm: limits by desk, factor exposures, liquidity, stress, kill switches.
6. Technology: OCaml at Jane Street, kdb+/q, C++ and FPGAs, research clusters and GPUs.
7. Compliance and surveillance: spoofing, layering, marking the close; the CAT; the cases (Sarao, J.P. Morgan's
   $920 m spoofing settlement).
8. The interview: probability, expected value, market-making games, estimation, coding; how to prepare.
9. Culture and history: the firm-founding stories as told in public (Thorp, Simons, Shaw, Griffin, the Jane Street
   founders from SIG).

*Textbooks:* Narang *Inside the Black Box*; Isichenko; Paleologo; Zuckerman *The Man Who Solved the Market*;
Patterson *The Quants*; Derman *My Life as a Quant*.
*Computed:* the economics of a pod (Sharpe, capital, payout, stop-out probability) by simulation; the Virtu S-1
statistic tested against a Sharpe implied by daily P&L.
*Visuals:* `HouseChart` in full: desks, capital, risk and P&L flows.
*Firms:* all of the above, public record only.
*Desk:* a full mock interview segment.
*House:* compliance and limits.

### Act VI · Market Microstructure

### Part 35 · Who Trades With Whom (~55)
1. Garman (1976); Ho–Stoll (1981).
2. Glosten–Milgrom (1985).
3. Kyle (1985), λ derived.
4. Roll (1984), Amihud (2002).
5. PIN, VPIN and the critique.
6. Price discovery (Hasbrouck 1995).
7. Market structure: Reg NMS, maker–taker, dark pools, PFOF, the 2024 rules, T+1.
8. HFT as market maker (Menkveld 2013; Brogaard et al. 2014).
9. Manipulation: spoofing, layering, momentum ignition; detecting it in the ITCH day.
10. The flash crash (Kirilenko et al. 2017); the Treasury flash rally (2014).
11. Frequent batch auctions (Budish–Cramton–Shim 2015).

*Textbooks:* O'Hara *Market Microstructure Theory*; Hasbrouck *Empirical Market Microstructure*;
Foucault–Pagano–Röell *Market Liquidity*; Harris.
*Computed:* Kyle and Glosten–Milgrom simulated; Roll, Amihud, VPIN on ITCH and Binance; a spoofing-pattern detector.
*Visuals:* Kyle's price converging to value; the GM spread narrowing.
*Crisis:* 6 May 2010; Navinder Sarao. *Firms:* exchanges and wholesalers.
*Desk:* "Why does the bid-ask spread exist even with competitive, risk-neutral market makers?"
*House:* surveillance.

### Part 36 · The Limit Order Book (~55; frontier)
1. Queues (Cont–Stoikov–Talreja 2010); queue-reactive (Huang–Lehalle–Rosenbaum 2015).
2. Hawkes in finance (Bacry–Mastromatteo–Muzy 2015), estimated; near-criticality.
3. Order flow's long memory (Lillo–Farmer 2004).
4. OFI (Cont–Kukanov–Stoikov 2014); deep OFI (Kolm–Turiel–Westray 2023).
5. The microprice (Stoikov 2018).
6. DeepLOB; universal features (Sirignano–Cont 2019).
7. LOBCAST (Prata et al. 2024): fragile generalization.
8. Generative order books (Nagy et al. 2023) *(verify: LOB-Bench 2025)*.
9. Our generative book, trained here, and its stylized-fact scorecard.

*Textbooks:* Bouchaud–Bonart–Donier–Gould *Trades, Quotes and Prices*; Abergel et al. *Limit Order Books*;
Cartea–Jaimungal–Penalva ch. 1–4.
*Trained:* DeepLOB (honest out-of-sample); **the generative order-book transformer**.
*Visuals:* `OrderBookLadder` with Hawkes intensity glowing; the microprice moving.
*Firms:* HRT, Jump, Tower (public talks and papers).
*Desk:* "Bid 100 × 500, ask 100.01 × 100. Where is fair value?"
*House:* the order-book simulator (used by 37, 38, 42).

### Part 37 · Market Impact and Execution (~55)
1. Metaorders; what public data shows.
2. The square-root law (Tóth et al. 2011) and latent liquidity (Donier et al. 2015); universality *(verify:
   recent complete-market surveys)*.
3. Microstructure invariance (Kyle–Obizhaeva 2016).
4. The propagator (Bouchaud et al. 2004).
5. No dynamic arbitrage (Gatheral 2010).
6. Almgren–Chriss derived; the execution frontier.
7. Obizhaeva–Wang (2013).
8. Signals and many agents (Cartea–Jaimungal; MFG).
9. RL execution, trained here, vs Almgren–Chriss.
10. TCA, algos (VWAP, TWAP, POV, implementation shortfall), smart order routing.

*Textbooks:* Cartea–Jaimungal–Penalva; Guéant *The Financial Mathematics of Market Liquidity*; Lehalle–Laruelle
*Market Microstructure in Practice*; Bouchaud et al.
*Trained:* the RL executor in the Part 36 simulator.
*Computed:* propagator fits on ITCH; Almgren–Chriss frontiers; square-root emergence in a latent-book simulation.
*Visuals:* `ImpactTrace`; trajectories bending with risk aversion.
*Firms:* bank and broker algo desks.
*Desk:* "Trading 10% of daily volume costs 30 bp. What does 40% cost?" (√ law: 60 bp)
*House:* the execution desk.

### Part 38 · Market Making, ETFs and the Speed Race (~55)
1. Inventory and adverse selection.
2. Avellaneda–Stoikov (2008) by HJB; GLFT (2013).
3. Alpha in quotes, toxicity, mark-outs.
4. RL market making vs the analytic solution.
5. Tick size and queue position.
6. ETF market making: creation and redemption, the arbitrage band, authorized participants; bond ETFs in March
   2020 at discounts.
7. Latency arbitrage (Aquilina–Budish–O'Neill 2022).
8. HFT economics (Baron–Brogaard–Hagströmer–Kirilenko 2019).
9. Options market making at scale (Part 11) and the vol surface as the quote.

*Textbooks:* Guéant; Cartea–Jaimungal–Penalva ch. 10; Lehalle–Laruelle; Gastineau *The Exchange-Traded Funds
Manual*.
*Trained:* the RL market maker.
*Computed:* AS/GLFT vs simulation; mark-outs on ITCH; an ETF NAV-arbitrage simulation; latency-race statistics.
*Visuals:* the quotes skewing with inventory; the ETF premium band.
*Crisis:* Knight Capital (1 August 2012), fully in `trading`.
*Firms:* Jane Street and Flow Traders (ETFs), Virtu, Citadel Securities, XTX (FX), Optiver.
*Desk:* "You're long 1,000 shares in a falling market. How do you change your quotes?"
*House:* the market-making desk. *Note:* the engineering is in [`trading`](../markets/trading/README.md).

### Part 39 · Crypto and DeFi (~55)
1. Blockchains and exchanges, on and off chain; 24/7 markets.
2. CFMMs: x·y = k; the AMM as oracle (Angeris–Chitra 2020).
3. Impermanent loss and LVR (Milionis–Moallemi–Roughgarden–Zhang 2022).
4. Concentrated liquidity (Uniswap v3) and v4 hooks; an RL liquidity provider trained here.
5. MEV (Daian et al. 2020); block builders.
6. Perpetuals: funding and its no-arbitrage price (He–Manela–Ross–von Wachter 2022; Ackerer–Hugonnier–Jermann
   *(verify)*).
7. Cross-exchange arbitrage (Makarov–Schoar 2020).
8. Stablecoins and runs (Diamond–Dybvig on chain).
9. Crypto factors (Liu–Tsyvinski–Wu 2022).
10. Spot ETFs (January 2024).
11. Registered and opened.

*Textbooks:* Harvey–Ramachandran–Santoro *DeFi and the Future of Finance*; Narayanan et al. *Bitcoin and
Cryptocurrency Technologies*.
*Trained:* the RL LP.
*Computed:* LVR vs IL; funding and basis; cross-exchange gaps; Terra from public data.
*Visuals:* `AMMCurve` with LVR accumulating; funding pulling the perp to spot.
*Crisis:* Terra/LUNA (May 2022); FTX (November 2022).
*Firms:* Jump (Terra; the SEC's 2024 settlement with its affiliate), Alameda, Wintermute.
*Desk:* "An LP in an x·y = k pool; the price doubles. Loss vs holding?" (≈ 5.7%)
*House:* digital assets.

### Act VII · The System

### Part 40 · Measuring Risk (~55)
1. RiskMetrics; VaR three ways.
2. Coherence; VaR's failure of subadditivity; ES.
3. Elicitability (Gneiting 2011; Fissler–Ziegel 2016).
4. Backtests: Kupiec, Christoffersen, Acerbi–Székely.
5. FRTB.
6. EVT: POT, GPD, Hill; McNeil–Frey.
7. Copulas and tail dependence; correlation pitfalls.
8. FHS; stress and reverse stress tests.
9. Model uncertainty: the rearrangement algorithm.
10. Learned risk: CAViaR (Engle–Manganelli 2004) and a deep quantile network vs FHS, trained here.
11. Liquidity-adjusted risk.

*Textbooks:* McNeil–Frey–Embrechts *Quantitative Risk Management*; Jorion *Value at Risk*; Föllmer–Schied ch. 4;
Hull *Risk Management and Financial Institutions*.
*Trained:* CAViaR and a deep quantile network.
*Computed:* VaR/ES backtests on 1926–2020 daily returns; EVT fits; rearrangement bounds.
*Visuals:* VaR as a line, ES as the shaded mass; exceedance clusters.
*Crisis:* 2008 exceedance clustering.
*Firms:* bank market-risk functions; regulators.
*Desk:* "Your 99% one-day VaR is $10 m. Ten-day? What did you assume?"
*House:* risk reports.

### Part 41 · Leverage, Liquidity and Crises (~60)
1. Minsky and Kindleberger.
2. Diamond–Dybvig (1983).
3. Brunnermeier–Pedersen (2009) spirals.
4. Leverage cycles; fire sales (Shleifer–Vishny; Cont–Schaanning; Greenwood–Landier–Thesmar).
5. Eisenberg–Noe; contagion's phase transition (Acemoglu–Ozdaglar–Tahbaz-Salehi 2015).
6. CoVaR, SRISK.
7. LTCM, 1998.
8. 2007–08: repo runs, Lehman, AIG.
9. March 2020: the dash for cash.
10. China 2015: margin financing, the crash, the 2016 circuit breaker suspended after four days.
11. 2022–23: gilts, SVB, Credit Suisse; NBFI and policy.

*Textbooks:* Brunnermeier–Oehmke "Bubbles, Financial Crises, and Systemic Risk"; Gorton *Slapped by the Invisible
Hand*; Kindleberger–Aliber *Manias, Panics, and Crashes*; Lowenstein *When Genius Failed*.
*Computed:* the spiral; Eisenberg–Noe on EBA data; SRISK; March 2020 from FRED; China 2015 from public index data.
*Visuals:* `ContagionNet` cascading; the spiral tightening.
*Crisis:* all of them, in order.
*Firms:* LTCM, Bear Stearns, Lehman, AIG, Archegos (prime brokers' losses).
*Desk:* "A fund at 5× leverage loses 10%. Its lender raises haircuts from 20% to 30%. What must it sell?"
*House:* liquidity stress for the House.

### Part 42 · Machines in the Market (~55; frontier)
1. The Santa Fe market (Arthur et al. 1997); Lux–Marchesi (1999).
2. Simulators: ABIDES (Byrd–Hybinette–Balch 2020), the Part 36 generative book; the sim-to-real gap.
3. RL in markets: hedging, execution, market making, allocation; offline RL and why a backtest is not an
   environment.
4. LLM agents as traders, in the simulator.
5. Algorithmic collusion (Calvano et al. 2020; Colliard–Foucault–Lovo 2022; Dou–Goldstein–Ji *(verify)*),
   reproduced with multi-agent RL.
6. Herding when everyone shares a model (Gensler–Bailey 2020).
7. AI and stability: IMF (October 2024), FSB (2024); regulation *(verify: the current US rules)*.
8. Moore's law vs Murphy's law (Kirilenko–Lo 2013).

*Trained:* multi-agent RL market makers (collusion measured in spreads); LLM-agent traders.
*Visuals:* spreads converging above competition; shocks with diverse vs identical agents.
*Desk:* "Two algorithms that never communicate end up with wide spreads. Is that collusion?"
*House:* the House's agents placed in the simulated market.

### Finale

### Part 43 · Can You Beat the Market? (~60)
1. Sharpe's arithmetic (1991); Pedersen (2018).
2. Luck vs skill: Fama–French (2010), Barras–Scaillet–Wermers (2010), Berk–van Binsbergen (2015).
3. Adaptive markets (Lo 2004).
4. **The House runs**: signals, combination, sizing, execution, attribution, risk, on the sealed window, and
   stress-tested on the market generator's paths.
5. The Track Record, all rows; the trial counter, final; deflated Sharpes. Narration follows the numbers.
6. The Surface's final scoreboard.
7. Open problems: the equity premium; roughness; the zoo's dimension; low-SNR ML; LLM look-ahead; AI traders and
   stability; Treasury market plumbing; climate risk.
8. Back to Bachelier: 22 April 2020, and the fair game.

*Visuals:* `HouseChart` live with money flowing; the sealed envelope opened; the timeline 1900 to now.

## 7. Phases

0. **Infrastructure:**
   - `explainer/quant/`: `ACTS`, `PARTS`, the 1900–2030 timeline (ideas, crises, firms), `series_map`,
     `HouseChart`, the Surface, the Track Record, the trial counter, `crisis_card`, `firm_card`, `desk_question`,
     and the instruments in Section 1. *AI, Built*'s lecture cards and visual helpers are re-exported.
   - `explainer/quant/house/`: the House library's skeleton and `tests/test_quant_house.py`.
   - Data: licences, fetch modules, checksums, the freeze date. The Surface is frozen first.
   - Reading: [`READING.md`](READING.md)'s map checked against each book's actual table of contents (any chapter
     left unmapped either gets a home or is listed as out of scope, with the reason), and every paper citation
     checked against its source.
   - Colours in `explainer/style.py` (`C.P`, `C.Q`, hedge, impact, crisis red, firm blue, ...).
   - Tooling: `quant` in `make.py`'s bilingual series and in `qa_series.py`, `qa_report.py`, `qa_audio.py` and
     `package_uploads.py`; `quant_text_zh.json`, `QUANT_ZH_GUIDE.md`, `quant_upload.json`.
1. **Pilot: Part 10 (Black–Scholes–Merton).** It exercises the derivation ladder, `HedgeLedger`, `PathFan`, the
   first row of the Surface, the House's first desk, a crisis file, a firm file and desk questions, on real data.
   Delivered in English and Chinese. **Review with the user**, then lock the standard.
2. **Roll-out, Parts 1 → 43**, Act by Act. Each part goes through:
   - the frontier sweep (every *(verify)* resolved);
   - locking the chapter list;
   - the House component, with tests;
   - `compute.py` (training, registering Track Record rows, declaring trials);
   - English scenes, then QA gates;
   - Chinese, then QA gates;
   - commit and push.
3. **Finale** last, when every desk, row and trial is in.

Scale: about 38 hours of video, about 190–210k narration words per language, roughly 4–6k lines of scene code per
part, and the House library (target 10–15k lines, tested). Expect one part per one or two long sessions.

## 8. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| — | plan of record, draft 2 | — |
