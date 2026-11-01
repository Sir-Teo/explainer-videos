# Quant, Built (量化金融，从零搭建)

*Plan of record, draft 2. No part is written yet.*
- [`SYLLABUS.md`](SYLLABUS.md): the standard, the devices, the threads, the model zoo, the data, all 43 parts
  chapter by chapter, and the phases.
- [`READING.md`](READING.md): every textbook the series covers and the parts each maps to, coverage maps for the
  core books, the industry and history library, and the full paper list for every part.

A forty-three-part course on quantitative finance in English and Chinese. It aims to be as complete as the standard
textbooks taken together, as technical as a PhD course, and as close to the academic and industry frontier as
possible: Hull, Shreve, Björk, Gatheral, Bergomi, Glasserman, Brigo–Mercurio, Tuckman, Cochrane, Campbell–Lo–MacKinlay,
Grinold–Kahn, López de Prado, McNeil–Frey–Embrechts, Cartea–Jaimungal–Penalva, Bouchaud et al., O'Hara and more,
mapped topic by topic, plus the papers that came after them. The industry runs through it: how Jane Street,
Citadel, Renaissance, Millennium, Two Sigma, D. E. Shaw, AQR, Optiver, SIG, Virtu, XTX, High-Flyer and the bank desks
make and lose money, told from the public record. As in *AI, Built*, **the models are trained** on the computer
that renders the video and replayed on screen. Every number comes from a computation on public data or a cited
source. Schematics are labeled `schematic`, made-up examples `illustrative`, and synthetic markets `simulated`.
Each part is a 30–60 minute lecture (about 38 hours in all). Videos are `quant1` … `quant43`, distinct from the
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

* **Act I, Markets and Money** (1–3): the fair game; the machinery of markets (instruments, clearing, margin,
  shorting, repo, prime brokerage, the players and the quant industry map); value, accounting and the firm.
* **Act II, The Mathematical Toolkit** (4–8): martingales and measure; stochastic calculus with jumps, Hawkes, fBM
  and signatures; financial econometrics; time series and volatility; decisions and control.
* **Act III, Derivatives (Q)** (9–22): no-arbitrage; Black–Scholes–Merton (the pilot); trading options; the
  volatility surface; stochastic volatility and jumps; rough and path-dependent volatility; exotics and structured
  products (snowballs, autocallables); computing prices; deep pricing and hedging; money, bonds and the curve;
  term-structure models; credit; XVA and clearing; FX, commodities and the basis.
* **Act IV, Return Premia (P)** (23–29): risk and return; factors; the factor zoo; backtesting without fooling
  yourself; machine learning for returns; text, LLMs and alternative data; alpha mining and automated research.
* **Act V, Portfolios, Strategies and the Firm** (30–34): portfolio construction; risk models, costs and trading
  through time; systematic macro and alternative premia; statistical arbitrage; inside a quant firm.
* **Act VI, Market Microstructure** (35–39): who trades with whom; the limit order book; impact and execution;
  market making, ETFs and the speed race; crypto and DeFi.
* **Act VII, The System** (40–42): measuring risk; leverage, liquidity and crises; machines in the market.
* **Finale** (43): can you beat the market?

## The devices

1. **The House** (above): one firm, built desk by desk, run in the finale.
2. **The Surface** (the pricing scoreboard): one options surface frozen on one day (candidate: Deribit BTC, public
   and free). Every pricing model is calibrated to it and scored on implied-vol error, next-day error, arbitrage
   violations and speed: Black–Scholes, SVI/SSVI, a VAE, local vol, Heston, SABR, Bates, rough Bergomi, quadratic
   rough Heston, path-dependent vol, the neural calibrator, a neural SDE.
3. **The Track Record and the sealed envelope** (the investing scoreboard). All research uses data to 31 December
   2020. Every strategy is registered (code hash, parameters, costs, trial count) before its 2021-onward hold-out
   is opened, once, in its part. The result is shown whatever it is.
4. **The trial counter**. Every backtest the series runs is counted. The finale deflates the Track Record by the
   true number of trials, including the millions of formulas Part 29's alpha miners search.
5. **Crisis files, firm files and desk questions** in every part:
   - the event where the idea broke, measured from data;
   - the firms whose business it is, from the public record;
   - interview-style problems in the trading-firm tradition, with solutions.
6. **Threads, payoff cards and the timeline** (1900–2030; ideas, crises, firms). Threads run across parts: the
   fair game, Thorp, LTCM, crowding, roughness and Hawkes, control from HJB to RL, liquidity, overfitting,
   correlation, and the links to *AI, Built* (autodiff, double descent, transformers, diffusion, RL, High-Flyer
   and DeepSeek).

## What gets trained

Every part trains or fits its models on the CPU, seeded and replayed on screen (`TrainingReplay`), against the
classical benchmark at equal budget. Narration branches on the result. The list:
- volatility forecasters (GARCH, HAR, LSTM, transformer, a foundation model zero-shot);
- PPO on Merton's problem;
- an RL options market maker;
- a neural SVI and a surface VAE;
- a snowball surrogate pricer;
- the neural calibrator, differential ML, deep BSDE, deep optimal stopping, **the deep hedger**, a neural SDE and
  **a market generator**;
- ML bond risk premia; default models; a deep xVA solver;
- the shrinkage SDF and IPCA;
- **gradient-boosting and network ensembles, random-feature timers, an autoencoder, a deep SDF and a cross-asset
  transformer**;
- **time-sliced language models** and an LLM signal;
- **genetic-programming, RL and LLM-agent alpha miners**;
- an end-to-end portfolio network;
- **deep statistical arbitrage**;
- DeepLOB and **a generative order-book transformer**;
- RL executors, market makers and liquidity providers;
- CAViaR and a deep quantile network;
- **multi-agent RL market makers** tested for collusion.

The full table is in [`SYLLABUS.md`](SYLLABUS.md#4-the-model-zoo-what-the-series-trains).

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

- [`stochastic`](../math/stochastic/README.md) is the gentle version of Parts 5 and 10.
- [`trading`](../markets/trading/README.md) is the engineering companion to Parts 35–38. Those parts read its data
  through its compute.
- [`opposing_forces`](../markets/opposing_forces/README.md) is the discounting arithmetic behind Parts 3, 18 and 23.
- *AI, Built* supplies the machine learning: autodiff (AI 4 → Part 16), double descent (AI 8 → 27), transformers
  (AI 13 → 27, 28, 36), diffusion (AI 21 → 17) and RL (AI 26 → 8, 11, 37, 38, 42).

## Shared code and the Chinese edition

- `explainer/quant/` will hold the instruments and re-export *AI, Built*'s lecture cards and visual helpers.
- `explainer/quant/house/` will hold the House library, tested by `tests/test_quant_house.py`.
- Text helpers and the derivation ladder are the analysis series' (`explainer.analysis`).
- Chinese narration goes in `videos/quant/quantN/narration_zh.json`, on-screen text in
  `videos/quant/quant_text_zh.json`, and terms in `QUANT_ZH_GUIDE.md` (Phase 0). The Chinese edition carries the
  A-share material its audience expects (snowballs, index enhancement, the 2015 crash, the February 2024 quant
  drawdown, High-Flyer).
- The workflow is [`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md).
