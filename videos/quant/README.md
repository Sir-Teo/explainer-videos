# Quant, Built (量化金融，从零搭建)

*Plan of record, draft 3 (30 parts). No part is written yet.*
- [`SYLLABUS.md`](SYLLABUS.md): the standard, the devices, the threads, the model zoo, the data, all 30 parts
  chapter by chapter, and the phases.
- [`READING.md`](READING.md): every textbook the series covers and the parts each maps to, coverage maps for the
  core books, the industry and history library, and the full paper list for every part.

A thirty-part course on quantitative finance in English and Chinese. It aims to be as complete as the standard
textbooks taken together, as technical as a PhD course, and as close to the academic and industry frontier as
possible: Hull, Shreve, Björk, Gatheral, Bergomi, Glasserman, Brigo–Mercurio, Tuckman, Cochrane, Campbell–Lo–MacKinlay,
Grinold–Kahn, López de Prado, McNeil–Frey–Embrechts, Cartea–Jaimungal–Penalva, Bouchaud et al., O'Hara and more,
mapped topic by topic, plus the papers that came after them. The industry runs through it: how Jane Street,
Citadel, Renaissance, Millennium, Two Sigma, D. E. Shaw, AQR, Optiver, SIG, Virtu, XTX, High-Flyer and the bank desks
make and lose money, told from the public record. As in *AI, Built*, **the models are trained** on the computer
that renders the video and replayed on screen. Every number comes from a computation on public data or a cited
source. Schematics are labeled `schematic`, made-up examples `illustrative`, and synthetic markets `simulated`.
Each part is a 45–65 minute lecture (about 29 hours in all). Videos are `quant1` … `quant30`, distinct from the
physics videos `quantum` and `quantum2`.

*An education in methods, not investment advice. Firms are described only from the public record; allegations are
labeled as allegations.*

## The story

**Bachelier's fair game.** In March 1900 Louis Bachelier defended *Théorie de la spéculation* in Paris. It modeled
the bond market as a fair game ("the mathematical expectation of the speculator is zero"), invented Brownian motion
five years before Einstein to do it, and priced options with it. The field is an argument with that sentence.
- **Pricing** (Q) says the price *is* a fair game once you discount and change measure.
- **Investing and trading** (P) say it is *not quite* fair: there are premia, anomalies, frictions, and people who
  must be paid to take the other side.

The question that grows through the series is ***who is on the other side, and what are they paid for?*** It ends
on 22 April 2020, two days after WTI crude settled at −$37.63, when CME switched its oil options to Bachelier's
model because it allows a price below zero.

**The House.** Alongside the story, the series builds its own quant firm, `explainer/quant/house/`, a tested open
quant stack. Each part adds a desk or a component: the data layer, the vol desk's surface and hedger, the rates
curve, the XVA engine, the factor library, the ML and LLM signals, the alpha miners, the risk model and optimizer,
the execution desk, the market maker, the crypto book, compliance and risk reports. A `HouseChart` card opens each
part with what is built so far. **The finale runs the whole House** on data no part has touched and reports it as a
firm would.

## The parts

| # | Part | What it covers | Trained here |
|---|---|---|---|
| **I** | **Markets and Money** | | |
| 1 | The Fair Game | Bachelier, returns, the random walk and its tests, the stylized facts, efficient markets, P and Q, Thorp | |
| 2 | The Machinery of Markets | instruments, exchanges and market structure, clearing, margin, shorting, repo, prime brokerage, the firm (DCF, Modigliani–Miller), the players and the quant industry map, A-shares and India | |
| **II** | **The Mathematical Toolkit** | | |
| 3 | Martingales and Stochastic Calculus | filtrations, optional stopping, change of measure, testing by betting, Itô, Girsanov, Feynman–Kac, local time, jumps, Hawkes, fBM, signatures | |
| 4 | Financial Econometrics and Volatility | HAC, GMM, event studies, causal ML, unit roots and cointegration, GARCH, realized volatility, HAR, roughness | GARCH/HAR vs LSTM, transformer, foundation models |
| 5 | Decisions and Control | utility, HJB, Merton, Kelly, stopping, no-trade regions, BSDEs, mean-field games | PPO on Merton |
| **III** | **Derivatives (Q)** | | |
| 6 | No Arbitrage | FTAP by hyperplanes, state prices, trees, completeness, Breeden–Litzenberger, Ross recovery, martingale optimal transport | |
| 7 | Black–Scholes–Merton (pilot) | three derivations, Greeks, the hedging P&L, discrete and costly hedging, implied vol, 1973 and 1987 | |
| 8 | The Volatility Surface and How It Trades | no-arbitrage, SVI/SSVI, Dupire, gamma scalping, vol strategies, variance swaps and the VIX, the VRP, dispersion, 0DTE, the options market maker's book, the SEBI case | RL gamma scalper, neural SVI, surface VAE |
| 9 | Stochastic, Rough and Path-Dependent Volatility | Heston, SABR, jumps, Lévy, SLV, rough Bergomi, rough Heston, Hawkes foundations, the roughness debate, PDV, joint SPX/VIX, signature models | |
| 10 | Exotics and Structured Products | barriers, Asians, digitals, snowballs and autocallables, worst-ofs, cliquets, uncertain volatility, model reserves | snowball surrogate |
| 11 | Computing Prices | Monte Carlo, QMC, MLMC, Longstaff–Schwartz, Greeks and AAD, finite differences, ADI, Fourier/COS | |
| 12 | Deep Pricing and Hedging | neural calibration, differential ML, deep BSDE, deep stopping, deep hedging, neural SDEs, market generators | **deep hedger**, **market generator**, calibrator |
| 13 | Money, Bonds and the Curve | central banks, curves, duration, PCA, swaps, futures and CTD, repo, SOFR, term premium, relative value | |
| 14 | Term-Structure Models | short-rate, affine, HJM, LMM/FMM, swaptions, Bermudans, multi-curve, bond risk premia, MBS | ML bond risk premia |
| 15 | Credit, Counterparty and XVA | Merton, intensities, CDS, default prediction, copulas and CDOs, private credit, CVA/DVA/FVA/KVA/MVA, margin, CCPs, capital | default models, deep xVA |
| 16 | FX, Commodities and the Basis | CIP and its violation, carry, FX options, storage, negative oil, the Treasury basis trade, inflation | |
| **IV** | **Return Premia (P)** | | |
| 17 | Risk and Return | CAPM, SDFs, HJ bounds, APT, the equity premium, intermediaries, demand systems, behavioural finance, bubbles | |
| 18 | Factors and Fundamentals | GRS, Fama–MacBeth, XBRL fundamentals, value, momentum, quality, low risk, carry, crashes, ESG, A-share factors | factor timing |
| 19 | The Factor Zoo and Backtesting | t > 3, replication, decay, shrinkage SDFs, IPCA, biases, deflated Sharpe, PBO, purged CV, reality checks | KNS SDF, IPCA |
| 20 | Machine Learning for Returns | low SNR, Gu–Kelly–Xiu, the virtue of complexity and its critics, deep SDFs, transformers, foundation models, López de Prado's toolkit | **ensembles**, **cross-asset transformer** |
| 21 | LLMs, Text and Automated Research | dictionaries to LLMs, look-ahead bias, alternative data, formulaic alphas, GP/RL/LLM alpha miners, China's quant industry, High-Flyer | **time-sliced LMs**, **alpha miners** |
| **V** | **Portfolios, Strategies and the Firm** | | |
| 22 | Portfolio Construction, Risk Models and Costs | estimation error, RMT and shrinkage, Black–Litterman, risk parity, HRP, the fundamental law, Barra-style risk models, costs, Gârleanu–Pedersen, alpha combination, capacity | end-to-end portfolio |
| 23 | Systematic Strategies | trend, vol targeting, carry, risk parity, short vol, event-driven, pairs, OU rules, PCA residuals, deep stat arb | **deep stat arb** |
| 24 | Inside a Quant Firm | business models, disclosures, the pod model, research process, risk limits, technology, compliance, the interview | |
| **VI** | **Market Microstructure** | | |
| 25 | Microstructure and the Order Book | Glosten–Milgrom, Kyle, liquidity measures, the flash crash, batch auctions, queues, Hawkes, OFI, the microprice, deep and generative LOB models, spoofing | DeepLOB, **generative order book** |
| 26 | Impact and Execution | the square-root law, propagators, no dynamic arbitrage, Almgren–Chriss, Obizhaeva–Wang, execution with signals, TCA | RL executor |
| 27 | Market Making, ETFs and Machines | Avellaneda–Stoikov, GLFT, mark-outs, ETFs, latency arbitrage, artificial markets, algorithmic collusion | RL and **multi-agent** market makers, LLM traders |
| 28 | Crypto and DeFi | AMMs, LVR, concentrated liquidity, MEV, perps, stablecoins and runs, crypto factors | RL liquidity provider |
| **VII** | **The System** | | |
| 29 | Risk, Leverage and Crises | VaR/ES, elicitability, EVT, copulas, stress tests, runs, spirals, fire sales, networks, CoVaR/SRISK, LTCM to SVB, AI and stability | CAViaR, deep quantile |
| **Finale** | | | |
| 30 | Can You Beat the Market? | luck vs skill, adaptive markets, **the House runs**, the Track Record deflated, open problems, back to Bachelier | the House |

Every part also has a textbook line, a crisis file, a firm file, desk questions (interview-style) and a problem
set.

## The devices

1. **The House** (above): one firm, built desk by desk, run in the finale.
2. **The Surface** (the pricing scoreboard): one options surface frozen on one day (candidate: Deribit BTC, public
   and free). Every pricing model is calibrated to it and scored on implied-vol error, next-day error, arbitrage
   violations and speed.
3. **The Track Record and the sealed envelope** (the investing scoreboard). All research uses data to 31 December
   2020. Every strategy is registered (code hash, parameters, costs, trial count) before its 2021-onward hold-out
   is opened, once, in its part. The result is shown whatever it is.
4. **The trial counter**. Every backtest the series runs is counted. The finale deflates the Track Record by the
   true number of trials, including the millions of formulas Part 21's alpha miners search.
5. **Crisis files, firm files and desk questions** in every part.
6. **Threads, payoff cards and the timeline** (1900–2030; ideas, crises, firms). Threads run across parts: the
   fair game, Thorp, LTCM, crowding, roughness and Hawkes, control from HJB to RL, liquidity, overfitting,
   correlation, and the links to *AI, Built* (autodiff, double descent, transformers, diffusion, RL, High-Flyer and
   DeepSeek).

## Data

Everything rebuilds from free public sources:
- Ken French's library (1926–), Open Source Asset Pricing, the JKP factors, the Welch–Goyal predictors, Shiller's
  data, and SEC EDGAR/XBRL;
- FOMC texts, FRED, the Treasury, the Fed and NY Fed curves, and the EIA;
- Deribit's options API, Binance's market-data archive, and Nasdaq's ITCH sample day (via
  [`trading`](../markets/trading/README.md));
- a public A-share cross-section *(licence to verify)*.

CRSP, OptionMetrics, TAQ and metaorder records are not free. Where a part needs them it uses cited results and a
`simulated` market with known truth instead.

## Related videos in this repo

- [`stochastic`](../math/stochastic/README.md) is the gentle version of Parts 3 and 7.
- [`trading`](../markets/trading/README.md) is the engineering companion to Parts 25–27, which read its data
  through its compute.
- [`opposing_forces`](../markets/opposing_forces/README.md) is the discounting arithmetic behind Parts 2, 13 and 17.
- *AI, Built* supplies the machine learning: autodiff (AI 4 → Part 11), double descent (AI 8 → 20), transformers
  (AI 13 → 20, 21, 25), diffusion (AI 21 → 12) and RL (AI 26 → 5, 8, 26, 27).

## Shared code and the Chinese edition

- `explainer/quant/` will hold the instruments and re-export *AI, Built*'s lecture cards and visual helpers.
- `explainer/quant/house/` will hold the House library, tested by `tests/test_quant_house.py`.
- Text helpers and the derivation ladder are the analysis series' (`explainer.analysis`).
- Chinese narration goes in `videos/quant/quantN/narration_zh.json`, on-screen text in
  `videos/quant/quant_text_zh.json`, and terms in `QUANT_ZH_GUIDE.md` (Phase 0). The Chinese edition carries the
  A-share material its audience expects (snowballs, index enhancement, the 2015 crash, the February 2024 quant
  drawdown, High-Flyer).
- The workflow is [`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md).
