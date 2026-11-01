# Quant, Built (量化金融，从零搭建)

*Plan of record, draft 1. No part is written yet; [`SYLLABUS.md`](SYLLABUS.md) has the chapter-by-chapter plan,
the standard every part meets, the data plan and the phases.*

A thirty-three-part course on quantitative finance in English and Chinese, from Bachelier's 1900 thesis to the
current research frontier and to how the industry works today. It covers the mathematics of chance and money,
derivatives pricing from no-arbitrage to rough volatility and deep hedging, rates, credit and XVA, empirical asset
pricing from CAPM through the factor zoo to machine-learning and LLM asset pricing, portfolio construction and
trading costs, market microstructure, execution and market making, crypto and DeFi, risk and systemic crises, and
what learning machines do to markets. Each part is a 30–60 minute lecture in the manner of *AI, Built*. Its
mathematics is derived on screen, its history is told, and its idea is tested against real market data and against
the crisis where it failed. Every number on screen comes from a real computation on public data, run on the computer
that renders the video, or from a cited source. Schematics are labeled `schematic`, made-up examples
`illustrative`, and synthetic markets `simulated`. Videos are `quant1` … `quant33`. These names are distinct from
the physics videos `quantum` and `quantum2`.

*An education in methods, not investment advice. Firms are described only from the public record.*

## The story

**Bachelier's fair game.** In March 1900 Louis Bachelier defended a thesis in Paris, *Théorie de la spéculation*,
supervised by Henri Poincaré. It modeled the Paris bond market as a fair game, "the mathematical expectation of the
speculator is zero," invented Brownian motion five years before Einstein to do so, and priced options with it. The
whole field is an argument with that sentence. **Pricing** (the measure Q) says the price *is* a fair game once you
discount and change measure, and builds everything on that: replication, hedging, the volatility surface, rates and
credit. **Investing and trading** (the measure P) says the price is *not quite* fair: there are risk premia,
anomalies, frictions and people on the other side who must be paid to trade. The question that grows through the
series is ***who is on the other side, and what are they paid for?*** The series closes on the day the field came
back to its origin. On 22 April 2020, two days after front-month WTI crude settled at −$37.63, CME switched its oil
options to Bachelier's normal model, because it allows a price below zero.

* **Act I, Foundations**: returns and the stylized facts, martingales and measure, stochastic calculus with
  jumps, time series and volatility, and decisions under uncertainty.
* **Act II, Pricing (Q)**: no-arbitrage, Black–Scholes–Merton and hedging, the volatility surface, stochastic and
  rough volatility, numerical and deep pricing, interest rates, credit and XVA, and FX, commodities and the basis.
* **Act III, Return Premia (P)**: risk and return in theory, factors, the factor zoo and its statistics,
  backtesting without fooling yourself, machine learning for returns, and text, LLMs and alternative data.
* **Act IV, Portfolios and Strategies**: portfolio construction, trading through time (costs, capacity, signal
  combination, how a quant firm is organized), and statistical arbitrage.
* **Act V, Market Microstructure**: who trades with whom, the limit order book, market impact and execution,
  market making and the speed race, and crypto and DeFi.
* **Act VI, The System**: measuring risk, leverage, liquidity and crises, and machines in the market.
* **Finale**: can you beat the market? The series' own track record, deflated by its own number of trials.

Five devices hold it together:

1. **The Surface** (`explainer.quant.surface`, the pricing scoreboard). One options surface frozen on one day.
   Every pricing model the series builds is calibrated to it: Black–Scholes, SVI, local volatility, Heston, SABR,
   jumps, rough Bergomi, path-dependent volatility, a neural SDE. Each model adds a row giving its in-sample
   implied-vol error, its next-day out-of-sample error, its arbitrage violations and its calibration time. Part 1
   freezes the surface; Part 7 adds the first row.
2. **The Track Record** (`explainer.quant.track`, the investing scoreboard), with a **sealed envelope**. All
   research in the series uses data up to 31 December 2020. Each strategy a part builds (momentum, value,
   betting-against-beta, a shrinkage SDF, the Welch–Goyal market timer, gradient boosting, a transformer across
   assets, an LLM sentiment signal, stat-arb residuals) is *registered*: its code hash and parameters are recorded
   before the hold-out window (1 January 2021 to the freeze date) is opened for it. The window is opened once,
   in that part's last chapter, and nothing is tuned afterwards.
3. **The trial counter** (`explainer.quant.trials`). Every backtest any part runs is counted, with its seed. The
   finale deflates the Track Record's Sharpe ratios by the series' true number of trials (Bailey and López de
   Prado's deflated Sharpe ratio). The series holds its own research to the standard it teaches in Part 19.
4. **The crisis file** (`explainer.quant.crisis_card`). Each part ends its main argument with the real event
   where its idea broke: 1987 for portfolio insurance, LTCM for convergence trades, August 2007 for crowded stat
   arb, 2008 for the Gaussian copula, Volmageddon for short volatility, the 2022 gilt crisis and SVB for duration,
   Terra for algorithmic stablecoins, August 2024 for the yen carry trade. The part measures what happened from
   data and does not just tell it.
5. **The timeline strip** (`explainer.quant.timeline`, 1900–2030) on every chapter card: ideas in gold, crises
   in red. The **payoff cards** ("where this comes back") are shared with *AI, Built*.

## Data

Everything rebuilds from public sources that cost nothing: Kenneth French's data library (daily factors since 1926),
Open Source Asset Pricing (Chen and Zimmermann: 200+ published predictors), the JKP global factor data, Amit
Goyal's predictor data, FRED, the US Treasury yield curve and the Fed's Gürkaynak–Sack–Wright curve, the New York
Fed's term premia and SOFR, the EIA, Deribit's public options API (a full BTC and ETH surface with implied
volatilities), Binance's public market-data archive (trades, order-book snapshots, perpetual funding), Nasdaq's
TotalView-ITCH sample day (already parsed by [`trading`](../markets/trading/README.md)), SEC EDGAR, and the Fed's
FOMC statements. Some data is proprietary or licensed: CRSP, OptionMetrics, TAQ, SPX options, metaorder records.
Where a part needs it, the part says so, uses published results with citations, and adds a calibrated `simulated`
market in which the true answer is known. [`SYLLABUS.md`](SYLLABUS.md#4-data) lists what each part uses and how
it is frozen.

## How it looks

The visual language is *AI, Built*'s (`explainer/ai/viz.py`): one idea per frame drawn big, continuity instead of
cuts, derivations in place, colour as meaning, a camera that narrates, and live quantities. The new instruments are
in `explainer/quant/`. They include a 3D implied-volatility surface with a camera tour (`VolSurface`), Monte Carlo
path fans with their density on the side (`PathFan`), a hedging ledger that splits P&L into gamma, theta and vega as
the path runs (`HedgeLedger`), an order-book ladder with queues (shared with `trading`), the yield curve morphing
through time, the efficient frontier, copula clouds, contagion networks and the constant-product curve. The full
list is in the syllabus.

## The parts

| # | Part | Mathematics and history | Data, models |
|---|---|---|---|
| **I** | **Foundations** | | |
| 1 | The Fair Game | returns and compounding, Bachelier and Regnault, the random walk and its tests, the stylized facts, efficient markets and Grossman–Stiglitz, P and Q | Ken French daily 1926–, BTC; the Surface frozen |
| 2 | Martingales and Measure | filtrations, conditional expectation as projection, martingales, optional stopping, the doubling strategy, change of measure, heavy tails and stable laws, testing by betting | |
| 3 | Stochastic Calculus | Brownian motion, Itô, SDEs, Girsanov, Feynman–Kac, local time, jumps and Lévy processes, fractional Brownian motion, signatures | |
| 4 | Time Series and Volatility | ARMA, unit roots and cointegration, regimes, Kalman, GARCH, realized volatility, HAR, microstructure noise, roughness | Binance 1-min, Ken French |
| 5 | Decisions Under Uncertainty | utility, Merton's problem by HJB, Kelly and growth, optimal stopping, ambiguity, BSDEs, mean-field games | |
| **II** | **Pricing (Q)** | | |
| 6 | No Arbitrage | the FTAP by separating hyperplanes, state prices, binomial trees, completeness, Breeden–Litzenberger, Ross recovery, martingale optimal transport | the Surface's implied density |
| 7 | Black–Scholes–Merton | three derivations, Greeks, the hedging P&L ½Γ(σ²−σ̂²), discrete and costly hedging, 1973 and 1987 | hedging replays; first row of the Surface |
| 8 | The Volatility Surface | smiles, no-arbitrage conditions, SVI/SSVI, Dupire local vol, variance swaps and the VIX, the variance risk premium, 0DTE | Deribit surface and DVOL, VIX |
| 9 | Stochastic Volatility and Jumps | Heston, SABR, Merton/Bates/Kou, Lévy models, stochastic local vol, the forward smile, the SPX/VIX puzzle | |
| 10 | Rough and Path-Dependent Volatility | fBM, rough Bergomi, rough Heston, the skew power law, Hawkes foundations, the roughness debate, path-dependent volatility, joint SPX/VIX | Hurst from data; rBergomi on the Surface |
| 11 | Computing Prices | Monte Carlo and variance reduction, QMC, MLMC, Longstaff–Schwartz, Greeks and AAD, finite differences, ADI, FFT and COS | the series' autodiff (AI Part 4) |
| 12 | Deep Pricing and Hedging | NN calibration, differential ML, deep BSDE, deep optimal stopping, deep hedging under costs, neural SDEs, market generators | our deep hedger |
| 13 | Interest Rates | curves and bootstrapping, NSS, PCA, short-rate and affine models, HJM, LMM, the term premium, SOFR, negative rates | Treasury, GSW, ACM, SOFR |
| 14 | Credit and XVA | Merton and KMV, intensities, CDS, Vasicek and Basel, copulas and CDOs, CVA/DVA/FVA/KVA/MVA, margin and CCPs | |
| 15 | FX, Commodities and the Basis | CIP and its violation, UIP and carry, storage and convenience yield, negative oil, the Treasury basis trade, inflation | FRED, EIA |
| **III** | **Return Premia (P)** | | |
| 16 | Risk and Return | Markowitz, CAPM, SDFs and Hansen–Jagannathan, APT, the equity premium puzzle, habit, long-run risk, disasters, intermediaries, demand systems | |
| 17 | Factors | Fama–MacBeth and GRS, size, value, momentum, profitability, low risk, carry, momentum crashes, factor timing | Ken French, JKP |
| 18 | The Factor Zoo | multiple testing and t > 3, replication, post-publication decay, shrinkage SDFs, double selection, weak factors, IPCA, RP-PCA | Open Source Asset Pricing |
| 19 | Backtesting Without Fooling Yourself | biases, the Sharpe ratio's error, deflated Sharpe, PBO by CSCV, purged CV, reality checks, e-values | the trial counter |
| 20 | Machine Learning for Returns | low signal-to-noise, Gu–Kelly–Xiu, the virtue of complexity and its critics, autoencoders, deep SDFs, transformers across assets, foundation models | Welch–Goyal, crypto cross-section |
| 21 | Text, LLMs and Alternative Data | dictionaries, embeddings, FinBERT, LLM sentiment, look-ahead bias and time-sliced models, LLM agents, alt data | FOMC, EDGAR |
| **IV** | **Portfolios and Strategies** | | |
| 22 | Portfolio Construction | error maximization, 1/N, Ledoit–Wolf and RMT cleaning, Black–Litterman, risk parity, HRP, robust optimization, Kelly | |
| 23 | Trading Through Time | the fundamental law, risk models, transaction costs, Gârleanu–Pedersen, multi-period optimization, alpha combination, capacity, the quant firm | |
| 24 | Statistical Arbitrage | pairs and cointegration, OU trading rules, PCA residuals, Kalman hedges, deep stat arb, the August 2007 quant quake | ETFs, crypto perps |
| **V** | **Market Microstructure** | | |
| 25 | Who Trades With Whom | Kyle, Glosten–Milgrom, Roll, PIN/VPIN, price discovery, market structure, PFOF, batch auctions | ITCH day |
| 26 | The Limit Order Book | queues, Hawkes processes, order-flow imbalance, the microprice, deep LOB models and their limits, generative order books | ITCH day, Binance depth |
| 27 | Market Impact and Execution | the square-root law, propagators, no dynamic arbitrage, Almgren–Chriss, Obizhaeva–Wang, execution with signals, RL execution | |
| 28 | Market Making and the Speed Race | Avellaneda–Stoikov, GLFT, adverse selection, latency arbitrage, HFT economics | builds on `trading` |
| 29 | Crypto and DeFi | AMMs, impermanent loss and LVR, concentrated liquidity, MEV, perpetual futures, stablecoins and runs, crypto factors | Binance, on-chain |
| **VI** | **The System** | | |
| 30 | Measuring Risk | VaR and ES, coherence, elicitability and backtests, EVT, copulas and tail dependence, stress tests, model uncertainty | Ken French daily 1926– |
| 31 | Leverage, Liquidity and Crises | margin spirals, fire sales, runs, networks and Eisenberg–Noe, CoVaR and SRISK, LTCM, 2008, March 2020, gilts, SVB | |
| 32 | Machines in the Market | RL and LLM agents as traders, simulators and agent-based models, algorithmic collusion, AI and financial stability | our simulated market |
| **Finale** | | | |
| 33 | Can You Beat the Market? | luck vs skill, the arithmetic of active management, adaptive markets, the Track Record deflated, open problems, back to Bachelier | the sealed envelope, opened |

## Related videos in this repo

[`stochastic`](../math/stochastic/README.md) (Brownian motion to Black–Scholes and Girsanov) is the preview of
Parts 3 and 7. [`trading`](../markets/trading/README.md) (a real-time market-making system on a full ITCH day) is
the engineering companion to Parts 25–28, and those parts read its data through its `compute`/`load`.
[`opposing_forces`](../markets/opposing_forces/README.md) is the discounting arithmetic behind Parts 13 and 16.
*AI, Built* supplies the machine learning: Part 5 (randomness, SDEs), Part 8 (generalization and double descent,
behind the virtue-of-complexity debate in Part 20), Part 21 (diffusion, behind market generators), Part 26 (RL,
behind Parts 27, 28 and 32) and the transformer of Part 13 (behind Parts 20 and 21).

## Shared code and the Chinese edition

`explainer/quant/` will hold the series' instruments and re-export *AI, Built*'s lecture cards and visual helpers.
The text helpers and derivation ladder are the analysis series' (`explainer.analysis`). Chinese narration goes in
`videos/quant/quantN/narration_zh.json`, on-screen text in `videos/quant/quant_text_zh.json`, and terms in
`QUANT_ZH_GUIDE.md` (to be written in Phase 0). The workflow is the one in
[`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md).
