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

**Revision of November 2026: a part replaces a course.** The series is meant to be watched *instead of* the
lectures it covers, so a part has the depth of the corresponding chapters of a graduate course and the visual
intuition of 3Blue1Brown. Concretely:

- **Length: 50–60 minutes, hard floor 50** (`tools/lecture_length.py quantN --floor 50`). A part that runs short
  is missing material, not padding: find what its textbooks and papers cover that it does not.
- **One syllabus item, one or two chapters.** Each numbered item of Section 6 gets at least one full chapter of
  about 3 minutes, 2.5–4 (never several items squeezed into one chapter). An item with a derivation, an experiment and a
  case gets two.
- **A signature visual in every chapter**, built before the formula is written: the idea as a moving picture the
  viewer could redraw from memory (the measure change as paths being re-weighted and recoloured; Itô's correction
  as the quadratic variation piling up; the hedge as a ledger filling; the surface as a 3D object the camera walks
  around; the order book as queues that fill and empty). Static plots are the supporting cast, not the lead.
  3D (`ThreeDScene`) wherever the object has two inputs.
- **Derivations in full.** Every step on screen with its reason; the key result proved, not quoted, at the level
  of the textbooks in [`READING.md`](READING.md). Worked numerical examples after each result, and a
  pause-and-predict question per chapter.
- **A textbook audit** in each part's README: a table from every core section of the part's textbooks to the
  chapter that covers it, or to the part of the series that does. Nothing core is silently dropped.
- **Every paper on the part's list in [`READING.md`](READING.md) appears**: on screen with what it found, or in
  the README's reading guide with one line on why it matters.
- **Hands-on, as in *AI, Built*.** 16–20 chapters per part. The viewer watches things being built and trained,
  not results being reported: (a) every model the part fits or trains is shown learning, scrubbed through its
  checkpoints with the loss curve (`ValueTracker`-driven replays, as in AI Part 21's reflow chapter), with several
  seeds drawn as spread bands and baselines at equal budgets; (b) at least three "lab" moments per part show the
  House's actual implementation of the key algorithm on screen (`code_block`, at most a dozen lines) and then run
  it, the output appearing live; (c) simulations run on screen rather than as finished plots (paths drawn as they
  are simulated, a hedge rebalancing step by step, an order book filling); (d) a computing budget of about two
  CPU-hours per part, like the AI series', resumable and seeded, so every part has real experiments to show; and
  (e) every part rebuilds from one command, which the README gives, so a viewer can rerun and change it.
- **An industry chapter and a frontier chapter** in every part. Industry: how the firms that do this for a
  living actually do it (hedge funds, trading firms, banks, exchanges, regulators), from the public record:
  research papers by their staff, filings, books, court and regulatory documents, interviews on the record.
  Frontier: the 2023–2026 research, checked against the papers.

**Revision of November 2026 (2): the PhD layer.** A part also replaces the *doctoral* course on its subject, not
only the master's one. On top of the above, every part has:

- **A research chapter (4–6 minutes)**: the part's central result in the generality of the research literature,
  with its assumptions stated and the proof's key steps on screen, using the literature's own tools (asymptotics,
  random-matrix and empirical-process arguments, measure theory, martingale methods, convex duality) where the
  papers use them; then **checked by simulation against the theorem's prediction**, the formula and the experiment
  drawn on the same axes. Where the simple version shown earlier in the part is a special case, the chapter says
  of what.
- **Open problems**: two or three questions the literature has not settled, each with the papers that frame it and
  what an answer would change, on a card in the frontier chapter and in the README.
- **Qualifying-exam problems**: the problem set gains two proof problems at the level of a PhD qualifying exam
  (derive the theorem's special case, prove a bound, construct a counterexample), solved in full in the README in
  both languages.
- **"For the researcher"** in the README: the theory papers, the theorem each proves and under what assumptions,
  and every place the video simplifies.
- **Length**: the PhD layer raises a part to **55–65 minutes** (floor 50 still holds). Cut repetition before
  material.

Parts 1–26 were made before this revision; each gets its research chapter, exam problems and README section in a
retrofit pass (tracked in [`PROGRESS.md`](PROGRESS.md)).

**A chapter is a lecture segment of about 3 minutes (2.5–4; 16–20 per part, as in the AI series)**, in the AI series' order:

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
- `lecture_length.py --floor 50` (fails under 50 min).
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
| 38 | (moved to 42) GLFT tested on markouts instead |
| 39 | a learned (tabular) liquidity provider for concentrated liquidity, in simulation |
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

### Part 2 · The Machinery of Markets (~58)
1. The instruments and how each is quoted: shares, bonds (clean and dirty), futures and forwards (contract specs,
   cost of carry F = Se^{(r−q)T} by replication, the basis converging at expiry), swaps, options (contract specs, the
   OCC), ETFs (price against NAV); hedging with futures (basis risk, the minimum-variance ratio h* = ρσ_S/σ_F,
   effectiveness ρ², beta hedging).
2. Exchanges and OTC: order types and validity, hidden orders; the order book as queues (price, visibility and time
   precedence; the cost of walking the book; the tick and the 2024 Rule 612 amendments, compliance moved to November
   2027); call auctions (the crossing maximizes volume, proved; the closing auction); dealer markets and RFQ (best of
   n against information leakage); wholesalers and payment for order flow.
3. Clearing and settlement: novation; netting (M ≤ B ≤ G, proved) and Duffie–Zhu on when a CCP raises exposure; the
   default waterfall and cover-2; DVP, CNS and T+1 (28 May 2024); NSCC's VaR deposit and ECP, and 27–28 January 2021.
4. Margin and leverage: initial, variation and maintenance margin; liquidation prices and the probability of
   liquidation (reflection principle against BTC data); portfolio margin; margin models (SPAN's 16 scenarios, EWMA VaR
   with λ fitted by likelihood, the Kupiec backtest) and procyclicality (1987, 2008, 2020; EMIR's anti-procyclicality
   tools; LME nickel 2022; UK LDI 2022).
5. Short selling: locate, borrow, the fee and the rebate, recalls, dividends; short interest above 100% by relending;
   squeeze dynamics against free float; Volkswagen 2008.
6. Repo and securities lending: repo legs and rates, tri-party and bilateral; haircuts as leverage limits (1/h) and
   the deleveraging spiral; specials and the on-the-run premium (Duffie 1996); September 2019 and the reserve demand
   curve.
7. Prime brokerage: financing, custody, cross-margining; total return swaps; the race to sell (Archegos, 2021); the
   prime-brokerage run (Duffie 2010).
8. The players and their business models: sell side (agency and principal), buy side (fees, high-water marks as
   options, pass-through), proprietary trading, market makers, retail brokers and PFOF; smoothed returns
   (Getmansky–Lo–Makarov) and option-like returns (Fung–Hsieh).
9. The quant industry map and the roles, placed by horizon and instrument (the industry chapter).
10. Markets around the world: the US, the EU and UK (T+1 on 11 October 2027), Japan, India (index options, SEBI's
    studies and 2024 measures), China (T+1, ±10% and ±20% limits, Stock Connect, the 2024 short-selling and
    program-trading rules); what price limits do to measured returns.
11. Benchmarks and indices: cap, float and price weighting; rebalancing demand; the inclusion effect (Shleifer 1986;
    the Russell regression discontinuity; benchmarking intensity) and its disappearance.

*Textbooks:* Hull OFOD ch. 1–3, 5, 10 (ch. 4, 6, 7 → Part 18); Harris *Trading and Exchanges* ch. 1–6 (ch. 7–8 → 35);
Tuckman–Serrat (repo chapter); Pedersen *Efficiently Inefficient* ch. 1, 5 (ch. 2–4 → 26, 30); Mishkin (financial
system overview).
*Computed:* the BTC quarterly basis converging (Binance coin-margined BTCUSD_210326, 2020–21); the ETH/BTC
minimum-variance hedge in and out of sample; a zero-intelligence order book; the closing auction built order by order;
best-of-n RFQ and markouts; netting (gross/bilateral/CCP) and Duffie–Zhu; a CCP default waterfall under stress; the
settlement deposit under T+2/T+1; 10×/3×/2× BTC longs liquidated in March 2020 and the liquidation-probability surface
2020–25; EWMA margin fitted by likelihood on 1926–2020 and BTC, with breach rates and procyclicality; a short squeeze
against free float; the haircut spiral; the reserve demand curve from FRED (2018–21) and the SOFR percentile fan of
September 2019; a fire-sale race; fees with a high-water mark on 1927–2020; return smoothing in the smallest size decile
and by MLE; a Russell-style regression discontinuity (simulated, truth known); price limits.
*Data added:* FRED SOFR1, SOFR25, SOFR75, SOFR99; Binance futures/cm BTCUSD_210326 hourly; Binance spot ETHUSDT daily
(all through `explainer/quant/data.py`, checksummed in `videos/quant/data/manifest.json`).
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
*House:* treasury and funding: margin (EWMA, liquidation odds), financing, borrow fees, haircuts and deleveraging,
hedge ratios, clearing and auctions, fees with a high-water mark, return smoothing; every later backtest pays them.

### Part 3 · Value, Accounting and the Firm (~55)
1. Time value: NPV, IRR (bisection, and a project with two roots), annuities and perpetuities; Gordon growth.
2. The duration of equity, (1 + r)/(r − g), against the measured rate sensitivity of growth and value stocks.
3. The three statements as one double-entry machine, run on screen (the House's accounting simulator); the indirect
   cash flow statement and DuPont derived.
4. Accruals: Sloan's persistence test, as a mechanism (a simulated panel), on EDGAR filings, and as a portfolio.
5. XBRL and the point-in-time fundamentals store on real filings: the bitemporal plane (GE's recasts), Kraft Heinz's
   restatement queried as of two dates, filing lags against the 60/75/90-day rules.
6. DCF: free cash flow from the statements, the value-driver formula (growth adds value only when RONIC > WACC), the
   enterprise-to-equity bridge, the (r, g) and (g, RONIC) surfaces, and a Monte Carlo of the value.
7. The cost of capital: WACC, levered betas, APV, and the market's implied return (Damodaran's ERP rebuilt, 1960–2020).
8. Residual income (Ohlson 1995) derived from clean surplus; P/B = 1 + (ROE − r)/(r − g) as a surface.
9. Multiples (P/E, PVGO, EV/EBITDA) and the CAPE; the Campbell–Shiller identity and Cochrane's decomposition on 150
   years of Shiller's data, with the Stambaugh bootstrap.
10. Modigliani–Miller (1958) by arbitrage; the tax shield, Miller (1977), distress and the trade-off; what CFOs say
    (Graham–Harvey).
11. Payout: the dividend-irrelevance proof; buybacks, Rule 10b-18, the EPS illusion; issuers against repurchasers.
12. Equity as a call (Merton 1974): risk-shifting (Jensen–Meckling 1976), debt overhang (Myers 1977), real options.
13. Earnings announcements: SUE, an event study from 8-K dates (the House's `car`), the drift (Ball–Brown 1968;
    Bernard–Thomas 1989), then and now (Martineau 2022).
14. Accounting signals that became factors (accruals, F-score, gross profitability) and their decay after
    publication, across 208 predictors (McLean–Pontiff; Chen–Zimmermann).
15. Merger arbitrage: the spread as a risk-neutral probability, Capri–Tapestry (2023–24), and the short put
    (Mitchell–Pulvino) re-estimated on The Merger Fund.
16. Forensic accounting: Enron, Wirecard, Luckin, Kraft Heinz; the Beneish M-score and its base-rate problem;
    Dechow et al.'s F-score.

*Textbooks:* Berk–DeMarzo ch. 2–4, 7–9, 14–19, 22, 28; Brealey–Myers–Allen ch. 2–6, 16–19, 22, 28, 31; Damodaran ch.
2–3, 7, 9–20, 28–32; Koller et al. ch. 2–16, 20, 32; Bodie–Kane–Marcus ch. 18–19; CLM ch. 7; Luenberger ch. 2–3;
Penman (residual income) as a reference.
*Computed/Trained:* p* recursion; rate betas of B/M deciles; IRR bisection; the accounting simulator; Sloan's
regression on a simulated panel and on EDGAR; the restatement and filing-lag audit of the cached filings; DCF Monte
Carlo; implied ERP; Campbell–Shiller with a Stambaugh bootstrap; NI sorts; Merton surfaces; an Apple event study;
208 OSAP predictors before and after publication; Capri's implied probability; the MERFX kink regression with a
bootstrap; M-scores; an earnings forecaster (random walk, OLS, ridge, MLP; 5 seeds) on a simulated panel, replayed.
*Visuals:* the receding cash-flow conveyor; the duration fulcrum; three ledgers running with the identity lit; the 3D
accrual-persistence plane; the bitemporal plane with the as-of line sweeping; the (r, g) and (g, RONIC) surfaces; the
balance beam of the implied return; the P/B surface crossing 1 along ROE = r; the return/dividend tug-of-war; the
fixed pie with the government wedge; the equity and debt surfaces over (A, σ); event-time paths in SUE lanes; 208
predictors falling to their post-publication returns.
*Crisis:* Enron (2001), Wirecard (2020), Luckin Coffee (2020) and Kraft Heinz (restated 2019).
*Firms:* corporate finance practice (Graham–Harvey); valuation in court (Dell, Rural/Metro); rating agencies;
activists (13D); quant equity on fundamentals (AQR, OSAP); merger-arbitrage funds; the SEC and the FASB (leases).
*Desk:* the buyback question; Gordon's implied return; the merger-arb probability; "ROE 12%, r 8%, g 4%: P/B?"
*House:* the fundamentals store on real EDGAR filings (`fundamentals`: as-of queries, filing lags, the accounting
simulator, SUE and event studies); `valuation` (IRR by bisection, duration, value driver, residual income, implied
rate, APV and Miller, Campbell–Shiller, Beneish).

### Act II · The Mathematical Toolkit

### Part 4 · Martingales and Measure (~57)
1. Probability spaces and filtrations as information: σ-algebras as the questions you can answer, measurability,
   Kolmogorov (1933); coin space as the unit interval.
2. Conditional expectation as orthogonal projection: Kolmogorov's definition, the properties, the tower; regression
   is the same projection with data.
3. Martingales: Ville (1939) named them after a betting system; Doob; sub- and supermartingales; Jensen.
4. You can't beat the system: the martingale transform, and the same tax per unit staked for every roulette system.
5. Stopping times and optional stopping, proved: the walk that always wins, with E[τ] = ∞; Wald; uniform
   integrability; pattern waiting times (Li 1980).
6. The doubling strategy, admissibility (Harrison–Pliska 1981; Dybvig–Huang 1988), and Barings (1995): doubling
   down in Leeson's "88888" account.
7. Gambler's ruin and bold play (de Moivre; Dubins–Savage 1965); expected duration.
8. Martingale convergence: upcrossings, Pólya's urn, Lévy's upward theorem as learning.
9. Doob decomposition: drift plus martingale, ⟨M⟩; the drift depends on the filtration (Ivey v Genting, 2017).
10. Change of measure on a coin: density process, Bayes, discrete Girsanov, the Esscher transform on real returns.
11. Radon–Nikodym by martingales; equivalent measures agree on what is impossible; Kakutani's dichotomy.
12. Heavy tails: stable laws (Lévy; Fama 1965; Mantegna–Stanley 1995), the characteristic function and the
    generalized CLT.
13. Game-theoretic probability (Shafer–Vovk): Ville's inequality, testing by betting, e-values, anytime-valid
    inference (Ramdas et al. 2023); learning the bet (ONS, aGRAPA); confidence sequences; e-BH.

*Textbooks:* Williams *Probability with Martingales* ch. 9–14 (and 0, 4, 16–18); Shreve I ch. 2, 3, 5; Shreve II
ch. 1–2; Föllmer–Schied §1.2 (preview) and App. A.2.
*Computed:* conditional means of the market by era; six betting systems; first passage and Wald; pattern waits;
doubling and a schematic doubling rule on the 1995 Nikkei; Pólya's urn and upcrossings; a Bayesian drift learner;
Doob's decomposition of the market; the Esscher measure of US returns; dyadic Radon–Nikodym and Kakutani; stable
fits (McCulloch, ECF, MLE replayed); peeking; online bettors trained and compared; e-BH on 200 strategies;
casino hold and Azuma.
*Visuals:* the coin-space zoom; projection in 3D; the curtain desk; the bell and the curtain; the leaking balance;
the staircase and the cliff; the upcrossing trader; one P&L with two drifts; paths recoloured, not moved; the 3D
density emerging from dyadic bars; the bettor's needle learning Kelly.
*Crisis:* Barings 1995. *Firms:* casinos (Nevada hold vs edge), advantage players (Thorp, Uston, Ivey), bookmakers
(Kaunitz et al. 2017, Benter, Flutter), prediction markets (Kalshi, Polymarket, Betfair), sequential testing
(Optimizely, Netflix).
*Desk:* "A martingale starts at 1 and stops at 0 or 3. Probability it hits 3?"; "Expected flips to HH?";
"Penney's game: you pick HHT, I pick THH. Who wins?"; "A fair walk is stopped the first time it is up 1. E[τ]?"
*House:* the e-value monitor with learned bets (`ONSBettor`), confidence sequences and e-BH (used again in Part 26).

### Part 5 · Stochastic Calculus (~57)
1. Brownian motion as a limit (Donsker) and a construction (Lévy's midpoints, the Brownian bridge); the reflection
   principle and first passage; quadratic variation, proved and measured (the volatility signature plot).
2. The Itô integral built from simple integrands; the isometry and martingale property proved; Stratonovich and the
   Wong–Zakai theorem.
3. Itô's lemma proved, in several dimensions; Lévy's characterization and the Dambis–Dubins–Schwarz time change; SDEs:
   existence and uniqueness (Picard); Euler–Maruyama and Milstein with orders computed (MLMC in one line → Part 16).
4. Ornstein–Uhlenbeck and CIR solved, fitted by exact likelihood (Feller's boundary); the generator, Dynkin,
   Fokker–Planck and Feynman–Kac (proved), with the density surface in 3D.
5. Girsanov and Cameron–Martin: drift is a change of measure (paths re-weighted, not moved); Novikov; importance
   sampling as a short application (the theory → Part 16); volatility is observable, drift is not.
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
*Computed:* reflection with the discrete-monitoring shift and the arcsine law; QV and the BTC signature plot (noise
backed out); Wong–Zakai; Picard iterates; strong and weak orders; CIR exact MLE on DTB3; Fokker–Planck surfaces and a
Feynman–Kac Monte Carlo check; Dynkin's exit time; Girsanov re-weighting and effective sample size; volatility against
drift observability; hedge-error rates (W_T², a call, a second noise); local time two ways and the stop-loss
shortfall; Lévy–Khintchine checked on a tempered stable process; BTC jumps and the jump hedge floor; Hawkes MLE and
time-rescaling on BTC; fBM p-variation; the Cont–Das artefact; signature regression; variance-swap replication with
and without jumps; a neural SDE market generator scored on a 2020 hold-out.
*Visuals:* Donsker with three step laws; Lévy's midpoint construction; QV accumulating; the bet ledger; the 3D
tangent-plane misses; `PathFan` under the Fokker–Planck surface (Feller's wall at 0); paths re-weighted by Z; the
occupation sandpile; the Lévy–Itô layer cake; thinning, the Hawkes family tree and the time-warp; the H dial; Lyons'
helix in 3D.
*Labs:* `euler_maruyama`/`milstein`, `ou_exact`, `is_digital`, `hawkes_thinning`, `fbm`, `signature`.
*Replays:* CIR exact MLE (5 starts); Hawkes MLE (8 starts); signature regression over depth (5 splits); the neural SDE
(3 seeds).
*Industry:* CME's switch to Bachelier (April 2020); Interactive Brokers (CFTC 2021); OCC's STANS Monte Carlo margin;
the variance swap and the VIX as Itô's lemma; SR 11-7 → SR 26-2. *Frontier:* neural SDEs trained with signature
scores (Issa et al. 2023); signature-based SPX/VIX calibration (Cuchiero et al. 2025); Log-NCDEs (Walker et al.
2024); rough or not (Cont–Das 2024; Guyon–Lekeufack 2023); Brownian motion formalized in Lean (Degenne et al. 2025).
*Crisis:* 20 April 2020, WTI at −$37.63: a GBM cannot go there. *Firms:* CME Clearing; Interactive Brokers; OCC.
*Note:* `stochastic` is the gentle version; this part assumes it. MLMC complexity, the optimal importance-sampling
shift, adjoint Greeks and Monte Carlo hardware belong to Part 16.
*Desk:* "Expected time for Brownian motion to leave (−a, b)?"; "Probability Brownian motion hits 1 before −2?";
"Price a digital by Girsanov."
*House:* the simulation library (used by every pricing part), validated by Rule 6.

### Part 6 · Financial Econometrics (~55; 20 chapters)
1. Regression in finance: OLS as projection, Frisch–Waugh–Lovell, the sandwich; overlapping observations and HAC
   errors (Newey–West 1987, Hansen–Hodrick 1980, Hodrick 1992); fixed-b and EWC (Kiefer–Vogelsang 2005; Lazarus,
   Lewis, Stock and Watson 2018); clustered errors.
2. Predictive regressions: the Stambaugh bias (1999) derived; Amihud–Hurvich and IVX (Kostakis–Magdalinos–
   Stamatogiannis 2015); out of sample (Welch–Goyal 2008; Campbell–Thompson 2008; Goyal–Welch–Zafirov 2024).
3. MLE (information, QMLE, a dependence-robust sandwich) and GMM (Hansen 1982): the geometry, efficiency, the J test;
   the Euler equation estimated (Hansen–Singleton 1982), weakly identified and rejected.
4. Event studies: market model, CARs and their variance, event clustering (FFJR 1969; MacKinlay 1997); the turn of
   the month and FOMC decision days (Lucca–Moench 2015), measured, with placebos.
5. Panel methods: clustering (Petersen 2009); Fama–MacBeth vs pooled vs fixed effects, within and between; the
   two-pass CAPM test, Shanken's correction, GRS.
6. Bootstrap for dependent data: block (Künsch 1989) and stationary (Politis–Romano 1994); coverage measured.
7. Bayesian inference: priors as shrinkage; James–Stein; a hierarchical model for many assets, sampled by Gibbs.
8. Multiple testing, previewed: FWER, Holm, FDR (Benjamini–Hochberg 1995), proved; to Parts 25–26.
9. Causal inference: instruments, differences-in-differences (and the staggered-adoption trap), regression
   discontinuity (Russell cutoffs); double/debiased ML (Chernozhukov et al. 2018), orthogonality derived.
10. The signal-to-noise problem: how many years to tell a Sharpe of 0.5 from 0.

*Textbooks:* CLM ch. 2, 4, 8 and App. A; Cochrane *Asset Pricing* (rev. ed.) ch. 10–16, 20–21; Hayashi ch. 1–8;
Greene (8th ed.) ch. 2–6, 8, 11, 13–16, 20; Bali–Engle–Murray ch. 1–6; Tsay ch. 12 (MCMC).
*Computed/Trained:* HAC, fixed-b (critical values simulated) and EWC sizes in null worlds; Petersen's simulation;
Fama–MacBeth on 49 industries, the within/between split and the flat two-pass SML; Stambaugh's bias as a tilted
cloud; Goyal–Welch out of sample on Shiller (five predictors); Student-t MLE replayed, naive vs sandwich vs HAC
sandwich; GMM objective surface and a 400-economy Monte Carlo for the Euler equation; FOMC and turn-of-month event
studies with placebos; bootstrap coverage in 1,000 simulated markets; Gibbs-sampled industry means; BH on a planted
world; IV/DiD/staggered DiD/RD with planted effects; double ML across seeds and penalties; the years-to-significance
curve and the (α, β) ellipse refitted quarterly.
*Visuals:* the projection in 3D; the HAC window sliding over autocovariances; Ω masks for clustering;
cross-sections stacking into a time series of slopes and clouds sliding to the origin; the Stambaugh cloud tilting;
the likelihood hill climbed by Newton; the GMM ellipse touching the moment line; the J surface's ridge in 3D; event
paths sliding into event time; blocks cut and reshuffled; alphas on springs; the BH line rotating; residual clouds
for DML; the (α, β) ellipse shrinking as months arrive.
*Labs:* `econ._hac_meat` + `ols`; `econ.fama_macbeth`; `econ.gmm` (condensed); `econ.stationary_bootstrap`;
`econ.benjamini_hochberg`; `econ.dml_plr` (condensed).
*Crisis:* F-Squared (SEC 2014): signals applied a week early, marketed as a track record.
*Firms:* Man Group (Harvey–Liu haircuts), AQR (replication; a century of factor evidence), Research Affiliates (the
backtest protocol); the SEC Marketing Rule (nine advisers, 2023); nonstandard errors and reproducibility (Menkveld et
al. 2024; Pérignon et al. 2024).
*Frontier:* Goyal–Welch–Zafirov 2024; Kelly–Malamud–Zhou 2024 vs Nagel 2025; Lazarus–Lewis–Stock 2021; inference on
winners (Andrews–Kitagawa–McCloskey 2024); DiD (Roth et al. 2023); causal ML (Chernozhukov et al. 2024; Maasoumi et
al. 2024); LLM look-ahead (Glasserman–Lin 2023).
*Desk:* "A strategy has Sharpe 1 over 4 years. What is the standard error?"; "Pooled slope 0.002, Fama–MacBeth
0.017: which is wrong?"; "Twenty strategies, the best p = 0.03: significant?"; "t = 2.5 on five-year returns and a
persistent yield: trade it?"
*House:* the statistics module (HAC/EWC/fixed-b, Hodrick, clustering, Fama–MacBeth, within/between, two-pass and
GRS, MLE/GMM, out of sample, Amihud–Hurvich and IVX, event studies and placebos, bootstraps, Gibbs, FDR, causal
designs, double ML).

### Part 7 · Time Series and Volatility (~59; 20 chapters)
1. Stationarity, ACF, ARMA, Box–Jenkins (Yule 1927; Box–Jenkins 1970; Ljung–Box 1978); log VIX identified.
2. Unit roots: the Dickey–Fuller distribution derived and simulated (1979); spurious regression (Granger–Newbold
   1974; Phillips 1986).
3. Cointegration: Engle–Granger (1987) and the error-correction model; Murray's drunk and her dog (1994); Johansen
   (1991) on Treasury yields, in 3D.
4. Hidden states: Hamilton's regime filter (1989) by EM; the Kalman filter (1960) and stochastic volatility by QML
   (Harvey–Ruiz–Shephard 1994).
5. ARCH (Engle 1982) and GARCH (Bollerslev 1986) by MLE, with the likelihood surface in 3D; Nelson's stationarity
   (1990), QMLE (Bollerslev–Wooldridge 1992), Student-t; EGARCH, GJR; DCC (Engle 2002).
6. Scoring forecasts: "does anything beat a GARCH(1,1)?" (Hansen–Lunde 2005); robust losses proved (Patton 2011);
   Mincer–Zarnowitz, Diebold–Mariano, the model confidence set (Hansen–Lunde–Nason 2011).
7. Realized volatility (ABDL 2003; BNS 2002): the CLT, noise and the signature plot built, optimal sampling
   (Bandi–Russell 2008), two-scale and realized kernels.
8. HAR-RV (Corsi 2009) derived as a restricted AR(22); HARQ; jumps by bipower variation and the BNS test; HAR-CJ.
9. Roughness in the data: log realized vol at H ≈ 0.1 (Gatheral–Jaisson–Rosenbaum 2018), measured.
10. Deep volatility forecasting: an LSTM, a small transformer and HARNet against HAR, trained here and replayed.
11. Time-series foundation models: Chronos's tokenisation, a toy Chronos-style model trained here on synthetic
    series and run zero-shot; the published comparison (Brini 2026) and the 2022–2026 papers.
12. Industry: RiskMetrics' EWMA, Barra's volatility regime adjustment, volatility targeting (Man AHL; Moskowitz–Ooi–
    Pedersen), implied against realized on the options desk.

*Textbooks:* Tsay *Analysis of Financial Time Series* ch. 1–5, 8, 10–11; Hamilton *Time Series Analysis* ch. 3–5,
13, 15–22; Brockwell–Davis *Introduction to Time Series and Forecasting*; Francq–Zakoian *GARCH Models*;
Aït-Sahalia–Jacod *High-Frequency Financial Econometrics*; Andersen et al., "Volatility and correlation forecasting"
(*Handbook of Economic Forecasting*, 2006); CLM ch. 12; QRM (financial time series).
*Trained:* GARCH family (likelihood replay); HAR (rolling replay); LSTM, transformer and HARNet forecasters (5 seeds
each, replayed); a toy foundation model (3 seeds, replayed).
*Visuals:* clusters lighting up a century of returns; the AR(1) slider; the Dickey–Fuller histogram streaming; the
GARCH leaky bucket; the Kalman belief as a moving Gaussian; regime jars; the drunk and her dog; the yield cloud seen
edge-on; QV as squares; the signature plot built; the live 2020 leaderboard.
*Labs:* `ar_fit`, `adf`, `kalman_states`, `garch_filter`, `har_fit`, `log_rv_scaling`, `qlike`/`diebold_mariano`,
`forecast`.
*Crisis:* March 2020: each model's forecast the day before.
*Industry:* RiskMetrics (1994–96 Technical Document); MSCI Barra USE4; Harvey et al. (2018); the VIX.
*Desk:* "Daily vol is 1%. What is the vol over a year? Over a week? When is √T wrong?"; "α + β = 1: stationary?"
*House:* the volatility forecaster.

### Part 8 · Decisions and Control (~55)
1. Expected utility: the vNM axioms, Arrow–Pratt derived, certainty equivalents; Allais and Rabin as warnings.
2. Dynamic programming (Bellman 1957), backward induction on a grid; the HJB equation derived from the DPP and
   Itô; the verification theorem.
3. Viscosity solutions in outline (Crandall–Lions 1983): kinks, touching test functions, comparison; monotone
   schemes converge (Barles–Souganidis 1991).
4. Merton's problem (1969/71) by HJB and by finite differences: the fraction (μ − r)/(γσ²), rebalancing, two-fund
   separation; on 94 years of US data with its error bars.
5. Consumption (Merton 1971) and the martingale method (Cox–Huang 1989; Karatzas–Lehoczky–Shreve 1987): the
   investor buys a power claim.
6. Transaction costs: the Davis–Norman (1990) no-trade wedge, Shreve–Soner (1994), the ε^{1/3} band, by
   dynamic programming here.
7. Kelly (1956) and Breiman (1961), proved; fractional Kelly and estimation risk (Thorp, Benter); Samuelson's
   objection (1979); ergodicity and the controversy (Peters 2019; Doctor–Wakker–Wang 2020; Toda 2023).
8. Optimal stopping: the Snell envelope as the least concave majorant; smooth fit (McKean 1965); the American
   put preview.
9. Prospect theory (KT 1979/1992; Benartzi–Thaler 1995 redone on data); ambiguity (Ellsberg; Gilboa–Schmeidler;
   Hansen–Sargent; Maenhout's robust Merton derived).
10. BSDEs (Pardoux–Peng 1990; El Karoui–Peng–Quenez 1997): two-rate pricing by regression.
11. Mean-field games (Lasry–Lions; Huang–Malhamé–Caines 2006): a liquidating crowd, closed form and fictitious play.
12. Reinforcement learning on the same problems: PPO on Merton (5 seeds) and on the transaction-cost problem,
    against the DP band.

*Textbooks:* Pham ch 1–7; Touzi ch 2–6, 9; Karatzas–Shreve *Methods* ch 3, 6; Björk (stochastic control, the
martingale approach, optimal stopping); Merton *Continuous-Time Finance* ch 4–5; Øksendal ch 10–11; Back ch 1–2,
14; Bertsekas vol. I; Sutton–Barto ch 3–6, 13; Carmona–Delarue vol. I.
*Trained:* PPO on Merton (5 seeds, AI 26's code) converging to the Merton line; PPO on the transaction-cost
problem against the DP band; replayed with checkpoints.
*Labs:* the Bellman grid solver; the no-trade band; the Snell envelope; MFG fictitious play; PPO's core.
*Visuals:* the value surface built backward slab by slab; the HJB sup as a moving parabola; test functions
touching a kink; the Davis–Norman wedge with a reflected wealth dot; Kelly fans growing live; the Snell envelope as
a rope over pegs; the smooth-fit slider; the crowd's two arrows of time.
*Crisis:* leverage beyond Kelly, using LTCM's published leverage (full story in 41).
*Firms:* Thorp's partnership and Kelly sizing (Thorp 2006); Benter's syndicate; risk budgets (NBIM's 1.25 pp
limit; multi-manager drawdown rules, as reported); execution desks.
*Desk:* "You have a 60% coin at even odds. What fraction do you bet?" "With 1% costs your weight drifted from 62%
to 66%. Trade?"
*House:* the sizing module (Merton, Kelly, no-trade band, drawdown floor).

### Act III · Derivatives (Q)

### Part 9 · No Arbitrage (~56)
1. Arbitrage, the law of one price and put–call parity, proved by replication and checked on the Surface against
   Deribit futures; where parity breaks: borrow (Ofek–Richardson–Whitelaw 2004), Palm/3Com (Lamont–Thaler 2003),
   American boxes.
2. One period: the FTAP by separating hyperplanes (Farkas, Stiemke), proved, seen in 3D, and decided by a simplex run
   on screen.
3. State prices and the SDF; Q as the SDF renormalized; the risk-neutral simplex; Bitcoin's empirical pricing kernel.
4. The binomial tree (Cox–Ross–Rubinstein 1979): replication derived, the hedge run along a path, convergence to
   Black–Scholes, one American beat.
5. Completeness; super-replication as an LP and its dual (Harrison–Pliska 1981); options complete the market (Ross
   1976); dynamic super-replication and uncertain volatility (Avellaneda–Levy–Parás 1995; Lyons 1995).
6. Continuous time: Harrison–Kreps, Harrison–Pliska, Girsanov as reweighting; doubling, admissibility, NFLVR
   (Delbaen–Schachermayer 1994, 1998; Dalang–Morton–Willinger 1990), strict local martingales and bubbles
   (Cox–Hobson 2005).
7. Change of numeraire (Geman–El Karoui–Rochet 1995; Jamshidian 1989): N(d1) as a probability, Margrabe, forward and
   annuity measures, Bitcoin as numeraire.
8. Breeden–Litzenberger: butterflies become the density; static and calendar no-arbitrage; the SVI fit replayed; the
   density on every expiry in 3D and its dependence on the specification (Shikhman et al. 2026).
9. Ross recovery (2015), its critique (Borovička–Hansen–Scheinkman 2016; Martin–Ross 2019; Qin–Linetsky 2016) and the
   evidence (Jackwerth–Menner 2020; Jensen–Lando–Pedersen 2019; Horvath 2025).
10. Robust bounds: martingale optimal transport (Hobson 1998; Beiglböck–Henry-Labordère–Penkner 2013;
    Galichon–Henry-Labordère–Touzi 2014), its dual as a model-free hedge in 3D, solved by LP on refining grids and by
    entropic iteration.
11. Industry: authorized participants and ETF discounts (March 2020; Haddad–Moreira–Muir 2021), box-spread financing
    (van Binsbergen–Diamond–Grotteria 2022; BOXX), Royal Dutch/Shell, negative stubs, limits of arbitrage
    (Shleifer–Vishny 1997, simulated), LTCM.
12. Frontier: neural and Sinkhorn MOT (Neufeld–Sester 2023; Hasenbichler et al.), multi-marginal MOT, joint SPX/VIX
    no-arbitrage (Guyon 2024), multi-asset bounds (Neufeld–Papapantoleon–Xiang 2023), adapted Wasserstein
    (Bartl–Beiglböck–Pammer 2026), the pricing-kernel and recovery debate (Heston–Jacobs–Kim 2023).

*Textbooks:* Shreve I ch. 1, 3, 4; Shreve II ch. 5, 9; Björk (4th ed., 2020) ch. 2–3, 9–12, 15 (ch. 29 and 34 named);
Duffie DAPT ch. 1–2, 6; Delbaen–Schachermayer Part I; Föllmer–Schied ch. 1, 5, 7; Henry-Labordère *Model-Free
Hedging*.
*Computed:* parity forwards vs Deribit futures; the FTAP and super-replication LPs (simplex replay); CRR convergence
and exact replication; dynamic super-replication; Girsanov reweighting; doubling and bubble simulations; Margrabe
under two numeraires; BL densities on all expiries with specification bands; Bitcoin's pricing kernel; Ross recovery
sweep; MOT bounds, duals, grid and entropic convergence; Shleifer–Vishny liquidations.
*Trained:* a neural MOT dual (3 seeds) against the LP.
*Visuals:* the separating plane in 3D; P→Q bars and the risk-neutral simplex; the tree folding back with its hedge;
paths reweighted by Girsanov's density; the density re-weighted by a numeraire; butterflies becoming the density;
the density ridge in 3D; the dual hedge surface lowered onto the payoff in 3D.
*Crisis:* GameStop 2021: put–call parity and borrow; LTCM 1998. *Firms:* ETF authorized participants, box-spread
lenders (BOXX), LTCM (full story in 41).
*Desk:* "Call 10, put 7, strike 100, spot 103, no rates. Arbitrage?"; box spreads, and the 2019 Robinhood
"infinite leverage" box-spread episode; "Price a digital from two calls"; "A negative stub: arbitrage?".
*House:* the arbitrage checker (used on every surface): parity and forwards, FTAP/simplex, super-replication,
static and calendar checks, MOT bounds with duals and entropic solver, Ross recovery.

### Part 10 · Black–Scholes–Merton (~58; the pilot)
1. 1973: Black, Scholes, Merton; Sprenkle, Boness and Samuelson's two unknowns; Thorp and Kassouf's hedge (and
   Thorp's undiscounted formula, as MacKenzie reports); the first rejections; the CBOE opens (calls only, 16 stocks,
   911 contracts); Black's sheets of theoretical prices on the floor.
2. Three derivations: the self-financing replication PDE; the PDE solved through the heat equation (the kernel seen in
   3D); the risk-neutral expectation (Monte Carlo with seeds, Girsanov as the baseline); the binomial tree's limit,
   derived (the recursion is a discretized PDE) and seen in 3D.
3. The Greeks as geometry, derived (Sφ(d₁) = Ke^{−rT}φ(d₂)); Θ + rSΔ + ½σ²S²Γ = rV.
4. The hedging P&L ½ΓS²(σ²_implied − σ²_realized)dt, derived and watched in the ledger.
5. Hedging with the wrong volatility, proved (El Karoui–Jeanblanc–Shreve 1998); hedge at implied or at actual
   (Ahmad–Wilmott 2005); dollar gamma as a landscape.
6. Discrete hedging: error ∝ √Δt (Boyle–Emanuel 1980; Derman–Kamal's √(π/4)); the floor jumps put under it
   (Derman–Taleb 2005). Transaction costs: Leland (1985) derived and checked; the cost–risk landscape; why constant
   costs make perfect hedging unbounded (Soner–Shreve–Cvitanić 1995; Kabanov–Safarian 1997).
7. Implied volatility by inversion: existence and uniqueness, the normalized price, Brenner–Subrahmanyam,
   Corrado–Miller, Jäckel's "Let's be rational"; the House's solver on all 254 quotes, against plain Newton.
8. American options: the free boundary, the early-exercise premium (Kim 1990; Carr–Jarrow–Myneni 1992),
   Brennan–Schwartz (1977), Barone-Adesi–Whaley (1987), the call before a dividend.
9. Dividends, borrow and the forward: Merton's yield, Black-76, Garman–Kohlhagen, inverse (coin-settled) options; the
   fake skew drawn by a forgotten forward.
10. 1987: portfolio insurance (Rubinstein–Leland 1981) replayed on the October data; the Brady Commission's numbers;
    the birth of the skew; MacKenzie's performativity thesis.
11. 1997 to 1998: the Nobel, then LTCM as a short-volatility, short-liquidity book (GAO 1999; VIX through 1998).
12. The Surface's first row.

*Textbooks:* Hull OFOD ch. 13, 15, 17–20; Shreve II §4.5, ch. 5, §8.4–8.5; Björk ch. 7, 8, 10 and the
dividends/futures/FX chapters; Wilmott PWOQF ch. 5–9 and the hedging and transaction-cost chapters; Joshi *Concepts*
ch. 5–7, 12; Taleb *Dynamic Hedging*; Baxter–Rennie ch. 3–4. Perpetual put and smooth fit → Part 8; trees, PDE and
LSM numerics → Part 16; the smile → Part 12; the trade (scalping, frequency on data, dividend play) → Part 11.
*Computed:* the heat-kernel solution; MC under Q with seeds; the tree lattice converging; hedging replays on GBM,
Heston and jump paths, and on real BTC against DVOL (1,706 months, swept with bootstrap bands); hedge at implied vs
actual; error vs rebalancing with seeds and the jump floor; Leland checked, the cost–risk landscape, Leland's limit;
the solver race on the Surface; the carry term structure and the forgotten-forward skew; the American premium (tree,
Kim's integral, BAW); portfolio insurance on October 1987; VIX through 1998; the floor's 0.4 rule on the Surface; a
learned first guess for implied volatility (5 seeds).
*Visuals:* `HedgeLedger`; the tree converging to the PDE in 3D; the heat surface and kernel; the dollar-gamma
mountain; the cost–risk landscape; the normalized price surface; the early-exercise premium surface; the insurer's
weight through October 1987.
*Labs:* `bs.price`/`heat_price`, `trees.crr`, `hedge.delta_hedge`, `leland_vol`, `bs.implied_vol`, `replicate_put`.
*Industry:* Black's sheets and the CBOE floor; O'Connor & Associates; quoting in volatility (and Haug–Taleb's
dissent); Black-76 in the plumbing; Deribit (Coinbase, 2025) and IBIT options (2024). *Frontier:* inverse options
(Alexander–Chen–Imeraj 2023); hedging crypto options (Matic–Packham–Härdle 2023); the 2026 implied-volatility
solvers (Schadner; Le Floc'h–Healy; PIVOT; Amiriyan–Boutaib); Black–Scholes machine-checked in Lean (2026); the
minimum-variance delta (Hull–White 2017; Ruf–Wang 2022), fitted on BTC in Part 13.
*Crisis:* 19 October 1987. *Firms:* the CBOE floor; O'Connor & Associates; Leland O'Brien Rubinstein; LTCM.
*Desk:* "ATM call, 1 year, vol 20%, spot 100: price it in your head" (≈ 0.4·σ·S·√T); "Long a straddle, the stock
sits still for a week"; "What's the delta of a digital as T → 0?"
*House:* the vol desk opens: the BSM pricer and heat solver, the hedger (with costs), the implied-vol solver,
Barone-Adesi–Whaley and Kim's premium, portfolio insurance, and the Surface's first row.

### Part 11 · Trading Options (~58; the practitioner's part)
1. How an options trader thinks: the book as one Taylor series, each Greek derived; P&L as gamma against theta; a
   real next-day P&L explain on the Surface.
2. Gamma scalping on a real path, its order effect (the same returns reshuffled 2,000 times), and how often to hedge
   (hourly, daily, on 2% moves) across 244 BTC windows of 2021–2025.
3. Vega, vanna, volga derived; the risk reversal and butterfly as their prices; the vanna–volga smile rebuilt from
   three quotes; 100 weeks of BTC RR and BF.
4. Strategies: straddles, strangles, spreads, calendars, risk reversals, butterflies; what each bets on (3D P&L
   surfaces morphing), and what each paid on two years of real smiles.
5. Volatility trading: the premium in option returns (Coval–Shumway; Bakshi–Kapadia), a forecaster's edge tested out
   of sample (Sinclair; Goyal–Saretto), and how much to bet when the tail is fat (Kelly with a ruin wall).
6. Expiry: gamma at the strike, pin risk, the pinning mechanism (Avellaneda–Lipkin) simulated and tested on Bitcoin
   (Ni–Pearson–Poteshman); early exercise, synthetics and the dividend play (Pool–Stoll–Whaley; Hao–Kalay–Mayhew).
7. The options market maker: the spread from adverse selection (Glosten–Milgrom) measured on 524,000 Deribit trades
   (edge and markouts); inventory and the optimal quote (Avellaneda–Stoikov, GLFT, Stoikov–Sağlam); hedging the book's
   gamma and vega with other options, vega by bucket, and under costs.
8. Dispersion: index against component volatility, implied correlation (Cboe COR3M 2006–2025), the correlation risk
   premium, and the trade's P&L simulated.
9. The India expiry-day boom: weekly index options, retail losses, SEBI's 2024 measures; what short-dated options
   return to their buyers (Deribit).
10. Case file: SEBI's interim order against Jane Street (July 2025), *alleged* expiry-day index manipulation,
    contested by the firm; the record since (escrow, the SAT appeal; Jane Street v. Millennium, settled 2024); the
    mechanics alleged, as a toy model and its 3D generalization.

*Textbooks:* Natenberg *Option Volatility and Pricing*; Sinclair *Volatility Trading* and *Positional Option
Trading*; Taleb *Dynamic Hedging*; Bennett *Trading Volatility*; Hull OFOD (strategies, Greeks).
*Trained:* a tabular Q-learning options market maker (5 seeds) against the exact dynamic program and the GLFT
formula; the deep hedger (3 cost weights × 3 seeds, replayed; Part 17 goes further); a walk-forward ridge/boosted-tree
predictor of hedged straddle P&L (registered).
*Computed:* P&L explain on the Surface; scalping and its reshuffles; hedge frequency on 244 BTC windows; vanna–volga
on the Surface; 96 weeks of structures on real smiles; delta-hedged gains; Kelly on Part 10's 1,706 months; Deribit
maker edge and markouts; Greek hedges under Heston; pinning simulated and on BTC; early exercise on a tree; COR3M;
dispersion simulated; short-dated option returns on Deribit; short-vol books through 2018 and 2020.
*Visuals:* the value surface sinking by theta; the dollar-gamma landscape with the crash on it; P&L surfaces morphing
across structures; the vega surface with vanna and volga; Glosten–Milgrom beliefs; the policy map learning; Greek
space; the gamma spike and pinning paths; the index-vol surface over correlation; the alleged mechanics as a surface.
*Labs:* `book_greeks`, `delta_hedge`, `markouts`, `quote`, `ww_band`, `implied_correlation`.
*Crisis:* short volatility blown up: LJM (February 2018) and Allianz Structured Alpha (March 2020), from the SEC's and
DOJ's records.
*Firms:* SIG, Optiver (and its CFTC case), IMC, Jane Street, Citadel Securities and the PFOF wholesalers.
*Industry:* OCC volumes; retail flow and PFOF (Bryzgalova–Pavlova–Sikorskaya 2023; Muravyev–Pearson 2020); the desk's
loop; Deribit's settlement design; SEBI's intraday position limits.
*Frontier:* machine-learned option returns (Bali et al. 2023); RL for gamma–vega hedging (Cao et al. 2023) and for
option market making (Baldacci–Bergault–Guéant 2021; Fang–Xu 2023).
*Desk:* the market-making game ("make a market on a die roll; now I tell you it's even"); "Long a straddle, the
stock doesn't move. How do you lose money?"; "Deep ITM American call, dividend tomorrow: exercise?"
*House:* the options quoting engine.

### Part 12 · The Volatility Surface (~58)
1. Smile, skew, term structure, read as the risk-neutral law's skewness and kurtosis (Backus–Foresi–Wu); delta quoting;
   how the surface moves: sticky strike, sticky delta, Derman's regimes (1999), the skew-stickiness ratio, and the
   principal components of weekly moves (Cont–da Fonseca 2002).
2. Static no-arbitrage in total variance: Gatheral's g derived, calendar monotonicity, Roper's conditions, Lee's moment
   formula (2004); an arbitrage shown happening (Vogt's SVI).
3. SVI (Gatheral 2004; its Heston origin; the JW parameters; fitted and replayed) and SSVI (Gatheral–Jacquier 2014;
   both theorems, and where the butterfly condition stops holding when γ > ½; fitted to the Surface in 3D); eSSVI and
   the exact no-arbitrage SVI region (Martini–Mingone 2022).
4. Dupire (1994) derived from Fokker–Planck; Derman–Kani and Rubinstein's implied trees; BBF's factor of two;
   Gyöngy's projection checked by Monte Carlo on Heston; local vol repricing the Surface.
5. Local volatility's dynamics: the smile moves against the spot (Hagan et al. 2002), the forward smile fades.
6. Variance swaps and the log contract (Neuberger; Carr–Madan; DDKZ 1999; Britten-Jones–Neuberger 2000): strike
   truncation, jumps, monitoring; replicated on 243 real Bitcoin months; volatility swaps and convexity.
7. The VIX derived and run line by line; our BTC index against Deribit's DVOL since 2021; the VIX since 1990.
8. The variance risk premium (Carr–Wu 2009; Bollerslev–Tauchen–Zhou 2009) on BTC and the S&P 500, its P&L skew, and a
   descriptive predictability regression; Martin's (2017) SVIX bound derived; risk-neutral moments (Bakshi–Kapadia–Madan
   2003).
9. Dealer gamma and its feedback, simulated; intraday momentum (Baltussen et al. 2021); 0DTE (Andersen–Fusari–Todorov
   2017; Bandi–Fusari–Renò 2023; Dim–Eraker–Vilkov 2024); VIX1D.
10. VIX futures, the roll, short-volatility notes: the short-term futures index and a −1× note rebuilt from Cboe
    settlements; leveraged-product rebalancing (Cheng–Madhavan 2009).
11. Learning surfaces: a VAE over weekly surfaces (Bergeron et al. 2022) and an arbitrage-penalised network
    (Ackerer et al. 2020), both trained and replayed against SSVI.

*Textbooks:* Gatheral ch. 1, 3, 7, 8, 11 (2, 4–6 → Part 13; 9–10 → Parts 15, 13); Bergomi (local volatility,
forward-start options, variance swaps; the rest → 13, 14); Rebonato *Vol & Corr* (implied vs local, smile dynamics);
Hull OFOD "Volatility smiles and surfaces" and the implied-volatility-function model; Sinclair; Bennett.
*Computed/Trained:* term structure and skew sign over 243 weeks (2021–2025); stickiness tests and surface PCA; Vogt's
arbitrage and Lee's moments on the Surface; SVI and SSVI fit replays; Dupire, BBF ratio, an implied tree; Gyöngy on
Heston; LV repricing and forward skews; strike truncation; variance-swap replication on BTC; vol-swap convexity; our
VIX vs DVOL; VRP on BTC and the S&P 500 with P&L skew and a BTZ regression; SVIX and risk-neutral moments; the VX
index and inverse note; gamma feedback; the surface VAE (5 seeds); the penalised neural surface (3 seeds); one net
for all weeks.
*Visuals:* the flat plane bending into the skew; stickiness under a spot slider; eigen-surfaces breathing; g glowing
red; the SSVI surface fitting itself in 3D; implied vs local surfaces; the Heston cloud and its conditional variance;
payoffs summing to the log contract; the VX futures ribbon folding on 5 February 2018; long- vs short-gamma paths.
*Labs:* `fit_svi`, `fit_ssvi`, `g_function`/`dupire_local_var`, `strip_replication`, `vix`, `vx_index`/`inverse_note`.
*Crisis:* Volmageddon, 5 February 2018: the front VIX future +113%, the rebuilt −1× note −96%.
*Firms:* Cboe and Deribit (index makers); Credit Suisse (XIV, TVIX); ProShares (SVXY); Griffin–Shams (VIX settlement);
dealers' quants (Goldman's DDKZ and Derman–Kani, Dupire at Paribas, SVI at Merrill Lynch, Andreasen–Huge at Danske).
LJM and Allianz Structured Alpha are Part 11's crisis file.
*Frontier:* operator deep smoothing (ICLR 2025); VolGAN (2024); deep learning from IV surfaces (Kelly et al.);
no-arbitrage SVI/eSSVI (Martini–Mingone 2022); 0DTE pricing.
*Desk:* "Why is the VIX above realized volatility on average?"; "Replicate a variance swap with options."; "Spot falls
5%: where does ATM vol go under sticky strike, sticky delta and local vol?"
*House:* the surface builder (Rule 12: quote only from a fitted, checked surface; state the dynamics).

### Part 13 · Stochastic Volatility and Jumps (~56)
1. Why volatility must move: bitcoin's vol of vol, clustering and leverage, measured; 1987 and the skew; random
   volatility makes a smile (Hull–White 1987, Renault–Touzi, Romano–Touzi), derived.
2. Heston (1993): the characteristic function derived (affine ansatz, Riccati), the little trap, what each parameter
   does, the short-maturity skew ρξ/(4√v₀); Feller; Andersen's QE scheme derived; exact and Poisson-conditioned
   simulation.
3. SABR (Hagan et al. 2002): the expansion and the backbone; the negative density; arbitrage-free SABR solved as a PDE;
   Bartlett's delta.
4. Jumps: Merton's series, Kou, Bates; what the Surface does with jump parameters.
5. Lévy models: variance gamma derived as a time change, NIG, CGMY's fine structure; Carr–Wu; the term structure of
   skew across every model.
6. Stochastic local volatility: the McKean–Vlasov loop and the particle method (Guyon–Henry-Labordère 2012), its
   convergence; the mixing fraction.
7. Bergomi's forward variance curves: the curve as the state, the vol-of-vol term structure, the SSR of SV models.
8. The forward smile and cliquets across models fitted to the same vanillas: model disagreement.
9. The SPX/VIX puzzle (Gatheral 2008; Guyon 2020), measured in its bitcoin form: the smile's vol of vol against DVOL's.
10. Calibration: landscapes, identifiability (the Hessian), parameter instability over 100 weeks, regularisation.

*Textbooks:* Gatheral ch. 2–8, 10–11 (parts); Bergomi ch. 3–4, 6–10, 12; Cont–Tankov ch. 4, 6, 11, 13–15; Lewis
ch. 1–6, 8–9; Guyon–Henry-Labordère (LSV calibration); Oosterlee–Grzelak (Heston, QE, Lévy).
*Computed:* Heston, Bates, Merton, Kou, VG, NIG, CGMY and SABR on the Surface, with replays; the original Heston form's
branch-cut failure; QE against Euler and the exact law; arbitrage-free SABR; SLV convergence and the mixing-fraction
sweep; forward smiles and cliquets across models; the Heston vol index against DVOL; 100 weekly refits, raw and
regularised; the minimum-variance delta on BTC.
*Visuals:* the variance process as a second river; the mixing crowd; the CF helix and the branch cut; the gamma clock;
particles with the leverage surface growing; the variance curve in motion; the optimizer wandering in a flat valley.
*Labs:* `heston_cf`, `heston_qe`, `vg_cf`/`vg_paths`, `slv_paths`, `calibrate_reg`.
*Industry:* Société Générale's quant research (Bergomi, Guyon, Henry-Labordère); Cboe's VIX futures and options;
hedging by the minimum-variance delta; the horse races (Bakshi–Cao–Chen 1997; Matic–Packham–Härdle 2023); the EU
model-risk valuation adjustment.
*Frontier:* reversionary Heston and jumps (Abi Jaber–De Carvalho); the quintic OU model; neural joint SPX/VIX
(Guyon–Mustapha 2023); Poisson-conditioned Heston simulation (Choi–Kwok 2024); particle-method analysis (2025);
neural operators for LSV (2026).
*Crisis:* 19 October 1987 and the skew ever since (Rubinstein 1994; Bates 2000).
*Desk:* "In Heston, what sets the skew? The smile's curvature?"; "LV and SV both fit; price a cliquet"; "Why can't
a VIX future trade above the variance-swap vol?"
*House:* the calibrator (with traces, fixed parameters and regularisation) and the SLV particle simulator.

### Part 14 · Rough and Path-Dependent Volatility (~58; frontier)
1. The fact: the at-the-money skew grows like T^{H−1/2}, measured on 102 weekly Deribit surfaces (2024–2025); why a
   kernel makes it (the skew as integrated spot–variance covariance, Bergomi–Guyon 2012), why one-factor Markov models
   cannot, and why a power law forces roughness (Fukasawa 2021).
2. Volatility is rough (Gatheral–Jaisson–Rosenbaum 2018), re-measured on bitcoin in two eras; the rough forecast
   formula against HAR (expanding-window, out of sample); long memory (Comte–Renault 1998) is not roughness.
3. Rough Bergomi (Bayer–Friz–Gatheral 2016): the martingale property and the variance curve; calibrated and replayed
   (3 seeds); the hybrid scheme (Bennedsen–Lunde–Pakkanen 2017) against naive discretisation.
4. Rough Heston (El Euch–Rosenbaum 2019): the affine Volterra derivation, the fractional Riccati equation, Adams with
   its convergence measured; how much the Surface cares about H (a nine-point profile).
5. Where roughness comes from: nearly unstable Hawkes order flow (Jaisson–Rosenbaum 2016; El Euch–Fukasawa–Rosenbaum
   2018), simulated by branching; what a finite sample can and cannot show.
6. Markovian lifts (Abi Jaber–El Euch 2019; Abi Jaber 2019; Bayer–Breneis 2023): convergence in law and path by path.
7. The debate: the estimator's bias map (rough against fast mean reversion), estimation theory (Fukasawa–Takabatake–
   Westphal 2022; Bolko et al. 2023; Chong et al. 2024; Cont–Das 2024); the options side (Livieri et al. 2018; Rømer
   2022; Guyon–El Amrani 2023; Abi Jaber–Li 2025) and a two-factor Bergomi calibrated to the Surface.
8. Path-dependent volatility (Guyon–Lekeufack 2023) on DVOL and on the VIX, fits replayed; the 4-factor Markovian PDV
   (well posed: Nutz–Riveros Valdevenito 2024).
9. Quadratic rough Heston (Gatheral–Jusselin–Rosenbaum 2020, with their calibrated parameters): the Zumbach effect
   measured on the model, on rough Bergomi and on the US market; joint SPX/VIX.
10. Guyon's puzzle (2020: models fitted to the SPX skew give VIX implied vols too high; Part 13 measures it) and his
    dispersion-constrained martingale Schrödinger problem (*Finance Stoch.* 2024); martingale-transport bounds on the
    Surface as an illustration.
11. Signature volatility models (Cuchiero–Gazzani–Svaluto-Ferro 2023), calibrated to the Surface (in and out of
    sample); joint SPX/VIX with signatures (Cuchiero–Gazzani–Möller–Svaluto-Ferro 2025).
12. What desks use and why: speed (timed), neural surrogates (Bayer–Stemper 2018; Horvath–Muguruza–Tomas 2021;
    Rosenbaum–Zhang 2022) and lifts; hedging with the forward variance curve; Rule 14 applied to the part's scoreboard.

*Textbooks:* Bayer–Friz–Fukasawa–Gatheral–Jacquier–Rosenbaum (eds.) *Rough Volatility* (SIAM 2023), ch. 1–10;
Guyon–Henry-Labordère *Nonlinear Option Pricing* ch. 10–11 (McKean SDEs and the particle method; UVM → 15, BSDEs → 17);
Bergomi *Stochastic Volatility Modeling*, the forward variance and smile-expansion chapters; Gatheral *The Volatility
Surface* (stochastic-volatility and jump skews); Friz–Hairer (2nd ed. 2020) §14.5.
*Computed/Trained:* weekly skew power laws (102 weeks); model skews (Heston, Bates, jumps, rough); GJR on BTC 2018–20 and
2024–25; RFSV against HAR; rBergomi calibration replayed (3 seeds); hybrid against Riemann; Adams convergence and the H
profile; branching Hawkes sweep; lifts in law and pathwise; the estimator bias map (64 cells × 4 seeds); a two-factor
Bergomi; PDV on DVOL and VIX, 4FMPDV; qRH and the Zumbach effect; entropic martingale-transport bounds; a signature
volatility model on the Surface; calibration speed.
*Visuals:* the skew loom (3D); the kernel over the triangle (3D); |φ(u, T)| (3D); the bias map (3D); the hybrid scheme
filling the singular cell; Adams with memory arrows; Hawkes family trees and zoom-out; exponentials summing into a
power law; PDV memories filling; qRH riding its parabola; signature bars growing.
*Labs:* `log_rv_scaling`, `rbergomi_paths`, `frac_riccati`, `pdv4_step`, `entropic_mot`, `sigvol_logS`.
*Crisis:* 5 August 2024: the VIX above 65 before the open on wide put quotes (SEC DERA working paper; BIS Bulletin 95);
path-dependence explains bitcoin's DVOL that day and not the VIX. *Firms:* Cboe (VIX, VIX1D), Deribit (DVOL); Risk's
2021 Quants of the Year and 2023 Rising Star.
*Desk:* "Why can't a one-factor Markov SV model fit a 1-week skew?"; "Rough or fast mean reversion: how would you
test it?"; "Calibrate a rough model in milliseconds."
*House:* rough and PDV pricers, lifts, qRH, signature volatility, branching Hawkes; Rule 14.

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

*Textbooks:* Hull OFOD, "Exotic options" (ch. 27 of the 11th ed.; ch. 26 of the Global Edition); Shreve II ch. 7; Bouzoubaa–Osseiran ch. 2, 7–15; Guyon–Henry-Labordère (UVM; local
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
*Labs:* `down_out_call`, `static_dic_hedge`, `geometric_asian_call`, `snowball_payoff`, `uvm_price`, the surrogate's
training loop. *Replays:* the surrogate (3 seeds) against a polynomial; the Lagrangian UVM optimiser; the bump-size
curve (3 seeds); the entropic tilt; three digital-delta estimators (5 seeds).
*Industry:* prudent valuation and model reserves, day-one P&L, FRTB for autocallables, PRIIPs; Natixis 2018.
*Frontier:* differential ML for discontinuous payoffs (Glasserman–Karmarkar 2025); unbiased MC Greeks (Lakshtanov
2026); tensor trains for worst-of autocallables (2026); RL hedging of autocallable books (2024); quantum autocallable
pricing (2025).
*Crisis:* the January–February 2024 A-share snowball knock-ins; Korea's HSCEI-linked ELS (the 2015 vintages near
their barriers and the FSC's 37 tn won count of January 2016; the 2021 vintages' losses and the FSS scheme of 2024).
*Firms:* Chinese brokers' OTC derivatives desks; Korean banks and securities firms (FSS 2024–25); Natixis (2018).
*Desk:* "Price a digital with a call spread. What width, and what happens to the hedge near expiry?"; "The snowball
issuer's vega: sign, and where it peaks?"; "Price a one-touch with zero drift, given the digital."
*House:* the exotics pricer; Rule 15 (two models, a reserve, the worst path on record).

### Part 16 · Computing Prices (~59)
1. Monte Carlo: the estimator, the CLT error bar, efficiency (variance × work); random numbers (inverse transform,
   Box–Muller, Cholesky) and reproducible parallel streams (counter-based generators).
2. Variance reduction: antithetics, control variates (the optimal coefficient; Kemna–Vorst's geometric control),
   stratification and Latin hypercubes; importance sampling (the zero-variance measure, the optimal shift learned by
   cross-entropy, weight degeneracy).
3. Quasi-Monte Carlo: discrepancy and Koksma–Hlawka, Sobol nets (Joe–Kuo), scrambling for error bars; the Brownian
   bridge and PCA; effective dimension (Caflisch–Morokoff–Owen 1997; Paskov–Traub 1995).
4. Multilevel Monte Carlo (Giles 2008): the complexity theorem proved; Euler (β = 1) against Milstein (β = 2);
   randomised MLMC (Rhee–Glynn 2015).
5. American options by simulation: Longstaff–Schwartz run backward on real paths; the duality bound derived
   (Rogers; Haugh–Kogan) and computed (Andersen–Broadie); the five-asset max-call, against Part 17's network.
6. Greeks: bumps (bias–variance, common random numbers), pathwise, likelihood ratio, Malliavin weights
   (Broadie–Glasserman 1996; Fournié et al. 1999).
7. AAD (Giles–Glasserman 2006): reverse mode, the cheap-gradient principle, cost against the number of inputs,
   check-pointing.
8. Finite differences: θ-schemes, von Neumann stability and Lax's theorem; Crank–Nicolson's ringing and Rannacher; the
   American put as a complementarity problem (PSOR; the penalty method).
9. ADI for Heston (Douglas; Craig–Sneyd; in 't Hout–Foulon), on non-uniform grids.
10. Fourier: Carr–Madan and Lewis derived; COS (Fang–Oosterlee 2008) and its truncation; the race between every method.
11. Hardware: the overnight run, GPUs and FPGAs, sensitivities for SIMM and FRTB; quantum amplitude estimation built,
    simulated and costed.

*Textbooks:* Glasserman ch. 1–5, 7–8 (6 → Part 5, 9 → Part 40); Savine Parts I–III; Andersen–Piterbarg vol. I (FD and
MC chapters); Duffy; Seydel (finite elements: README note); Oosterlee–Grzelak (COS chapter).
*Computed:* the CI funnel and its coverage; Kemna–Vorst control (variance ÷ ~1,300); the IS variance curve and
cross-entropy; star discrepancy; dropping Sobol's first point; effective dimension (step/bridge/PCA); MLMC Euler vs
Milstein; LSM boundary, basis sweep, duality gap, Bermudan reference, five-asset max-call (a tie with Part 17's
network); bump RMSE surface; AAD cost against inputs (wall clock and operation counts); explicit blow-up; PSOR vs
penalty; uniform vs non-uniform ADI; Lewis vs COS; the race with a control variate; QAE vs MC at equal oracle calls; a
Chebyshev pricer; RQMC median-of-means.
*Visuals:* the race drawn as the clock runs; the net's boxes lighting; the bridge's coordinates (3D); the MLMC
telescope and replay; LSM run backward; the bump-error valley (3D); the AAD tape running both ways; the explicit march
exploding (3D); the American surface with its free boundary (3D); ADI sweeps on the Heston surface (3D); a density
rebuilt by cosines; the Grover rotation; the Chebyshev error surface collapsing (3D).
*Labs:* `brownian_bridge`, `mc_call`, `_mlmc_level`, `andersen_broadie_put`, `aad_greeks`, `fd_american_put`,
`cos_price`.
*Industry:* the overnight run; SIMM and FRTB sensitivities; Danske Bank's AAD; JPMorgan's FPGAs (2011); STAC-A2;
the OCC's Monte Carlo margin; QuantLib and ORE. *Frontier:* QSP derivative pricing (2024); median-of-means RQMC (2023);
COS term bounds (2024); signature stopping (2023); Chebyshev and tensor pricers.
*Firms:* Danske Bank; JPMorgan and Maxeler; bank quant libraries and overnight risk runs. (The London Whale's VaR
spreadsheet stays in Part 20: the Task Force report could not be fetched to quote here.)
*Desk:* "How many paths for a price to 1 bp?"; "Why is AAD's cost independent of the number of Greeks?";
"Crank–Nicolson's gamma oscillates: why, and the fix?"; "LSM 6.06, dual 6.41: what next?"
*House:* the pricing engine; Rule 16 (every price with its error, every method checked against another).

### Part 17 · Deep Pricing and Hedging (~58; frontier)
1. Learning a pricing formula: Hutchinson–Lo–Poggio (1994) redone and replayed (three seeds); universal
   approximation; a network's Greeks (the activation decides gamma: SiLU, ReLU, softplus) and no-arbitrage shapes
   (the butterfly test).
2. Neural calibration (Horvath–Muguruza–Tomas 2021; Hernandez 2016; Bayer–Stemper 2018): learning rough Bergomi's
   pricing map from Monte Carlo, label noise measured against fresh simulation, calibration as gradient descent
   through the network (the 3D surface converging onto the quotes, twelve starts), the training box's wall; two years
   of weekly surfaces.
3. Differential ML (Huge–Savine 2020): pathwise labels proved unbiased; the twin network replayed with seeds; tangent
   planes in 3D; the Gaussian process with gradients (Dixon–Halperin–Bilokon ch. 3) as its exact, unscalable twin.
4. Deep BSDE (E–Han–Jentzen 2017; Han–Jentzen–E 2018) in 100 dimensions: the BSDE derived from Itô, nonlinear
   Feynman–Kac (Pardoux–Peng 1990), the shooting picture, u₀ as a tail average with seeds, the linear (no-default)
   check; DGM and multilevel Picard.
5. Deep optimal stopping (Becker–Cheridito–Jentzen 2019): the bang-bang proof, the exercise tunnel in 3D, the lower
   bound, level with Longstaff–Schwartz at our budget (Part 16) and below BCJ's published bounds.
6. Deep hedging (Buehler–Gonon–Teichmann–Wood 2019): entropic risk and CVaR (Rockafellar–Uryasev), indifference prices
   (Hodges–Neuberger), the no-cost check replayed; the drift trap (Merton's term rediscovered; François et al. 2024;
   near-martingale measures); QLBS and RL hedging.
7. What the deep hedger learns: Leland and Whalley–Wilmott derived, the band emerging in training (three seeds), the
   band network (Imaki et al. 2021; Davis–Panas–Zariphopoulou 1993) and the learned hedge as a surface in (time,
   spot); a Whalley–Wilmott prior (Arzel–Lehdili 2026) re-run.
8. Neural SDEs with robust exotic bounds (Gierjatowicz et al. 2022): calibrate, then push, both replayed; generative
   LSV calibration (Cuchiero–Khosrawi–Teichmann 2020); joint SPX/VIX (Guyon–Mustapha).
9. Market generators: GJR-GARCH, Quant GANs, signature generators (Buehler et al. 2020; Ni et al. 2021; Kidger et al.
   2021), diffusion models (AI Part 21, reverse process shown live); judged by signature MMD and Part 1's stylized
   facts; hedgers tested across generators and on history.
10. Production: SR 26-2 (17 April 2026, Fed/OCC/FDIC, replacing SR 11-7 and SR 21-8) and PRA SS1/23; what has reached
    desks (J.P. Morgan, Danske, as reported); the frontier 2023–2026 (SANOS/DYSANOS/GROMM; is deep hedging
    speculation?).

*Textbooks:* Dixon–Halperin–Bilokon ch. 1, 3–5, 8, 10, 12; Kelly–Xiu (the virtue of complexity); Jentzen–Kuckuck–von
Wurstemberger (deep PDE theory). Glasserman 7–8 and Savine → Part 16.
*Trained (all replayed, seeds as bands):* HLP networks (three activations); the calibrator and the calibration; DML
and a GP with gradients; deep BSDE (with the linear check); deep stopping; the deep hedger (entropic, CVaR, under
drift, with costs); the band network (with a WW prior; on GBM and on GARCH paths); a neural SDE; DDPM and a signature
LSTM.
*Visuals:* the band riding a live path; the price surface and its error in 3D; the IV surface converging onto the
quotes; tangent planes and the GP shell; BSDE shooting; the exercise tunnel; the band sheets over (time, spot);
low/high model surfaces; reverse diffusion; the cross-generator heat map.
*Labs:* `train_mlp_regressor`, `calibrate_neural`, `train_differential`, `deep_bsde`, `deep_stopping`, `hedge_pnl`,
`Hedger.band`/`ww_band`.
*Firms:* J.P. Morgan (data-driven hedging of vanilla index books since 2018, deep hedging extended to cliquets, as
reported by Risk.net); Danske Bank (DML, AAD).
*Industry:* SR 26-2; PRA SS1/23; quantum deep hedging (2023). *Frontier:* SANOS/DYSANOS/GROMM (2026); François et al.
(2024); Zernikov (2026); Godin (2026); Mueller et al. (2024); Arzel–Lehdili (2026); Reppen–Soner–Tissot-Daguette;
Bayer–Pelizzari–Schoenmakers; Ye–Wong; Issa et al.
*Desk:* "Your hedger has costs. Why does the optimal hedge have a band?"; "A neural calibrator fits beautifully. How
do you know it is right?"; "Why record the payoffs' derivatives?"; "Your deep hedger makes money on average with no
costs. Is it hedging?"
*House:* the deep hedger and the market generator; Rule 17 (no network without a slower, independent engine; tested on
two generators and on history), tested in chapter 19 (the finale stress-tests the House with it).

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

### Part 28 · Text, LLMs and Alternative Data (~57; frontier; built)
0. Hook: the 22 January 2008 statement, word by word; the two-year's 28 bp fall.
1. Words as numbers: bag of words, document-term matrix, Zipf and Heaps, tf-idf (Gentzkow–Kelly–Taddy 2019).
2. Dictionaries: Tetlock (2007); Antweiler–Frank (2004); Tetlock–Saar-Tsechansky–Macskassy (2008); Loughran–McDonald
   (2011); the central-bank misfit (*unemployment*, *stability*).
3. Tone and the two-year yield; Kuttner (2001); Gürkaynak–Sack–Swanson (2005), the path factor.
4. Length, readability (Loughran–McDonald 2014), how much a statement changes; Cohen–Malloy–Nguyen's lazy prices;
   forward-guidance phrases.
5. SESTM (Ke–Kelly–Xiu 2019), fitted on statements.
6. Topics (NMF; LDA) as eras; Bybee–Kelly–Manela–Xiu (2024).
7. Inside the FOMC: Hansen–McMahon–Prat (2018); Meade–Stasavage (2008); Shapiro–Wilson (2022);
   Gorodnichenko–Pham–Talavera (2023).
8. Embeddings: PPMI–SVD, Levy–Goldberg (2014), word2vec (Mikolov et al. 2013).
9. Transformers; FinBERT (Huang–Wang–Yang 2023); a pocket LM trained on the minutes.
10. LLMs read the news: Lopez-Lira–Tang (2023); Chen–Kelly–Xiu (2022); Kim–Muhn–Nikolaev (2024); Araci (2019);
    Hansen–Kazinnik (2023); Cao–Jiang–Wang–Yang (2024).
11. Look-ahead bias: Glasserman–Lin (2023); Sarkar–Vafa (2024); He–Lv–Manela–Wu (2025).
12. The time-sliced experiment: three pocket LMs (to 2007; to 2020; to 2007 and 2013–2020), bits per character,
    probes, samples.
13. LLM agents: ReAct; TradingAgents (Xiao–Sun–Luo–Wang 2024).
14. Alternative data: Katona–Painter–Patatoukas–Zeng (2025); Zhu (2019); Kyle with N insiders.
15. Domain models: BloombergGPT (Wu et al. 2023); Li et al. (2023); the text desk.
16. The statement score registered (13 trials) and opened on 2021–25.
17. Rule 28: text features.
Research: why screening finds the words (Chebyshev's association lemma; sure screening; recovery by n; permutation
test on the statements).

*Textbooks:* Gentzkow–Kelly–Taddy "Text as data" (2019); Kelly–Xiu, the text chapter; Jurafsky–Martin.
*Trained:* three time-sliced pocket LMs on FOMC minutes (`explainer.lm.pocket`), point-in-time BPE tokenizers.
*Computed:* FOMC tone vs 2-year moves; SESTM; NMF topics; PPMI–SVD embeddings; the look-ahead gap.
*Firms:* Bloomberg; news-analytics vendors (RavenPack), from the public record.
*Desk:* "Your LLM signal backtests at Sharpe 4 on 2015–2020 news. What's the first thing you check?"
*House:* `explainer/quant/house/text.py`.

### Part 29 · Alpha Mining and Automated Research (~56; frontier; built)
0. Hook: ten thousand random formulas; the best of N climbing; where Act IV ends.
1. Formulaic alphas: Kakushadze (2016), 101 alphas as trees; delay, neutralisation, rank weights, decay; three of the
   101 on coins.
2. The search space: the count by depth (doubly exponential); Koza's grow method; distinct formulas against distinct
   scores.
3. Random search against a pure-noise baseline; the winner's curse and shrinkage; on coins, a few real patterns
   restated (low volatility above all).
4. Genetic programming (Koza 1992): crossover, tournaments, bloat and parsimony; equal-budget comparison with random
   search; Allen–Karjalainen (1999).
5. RL alpha mining: AlphaGen (Yu, Xue, Ao, Pan, He, Tu and He, KDD 2023), the synergy reward; a REINFORCE generator
   trained here; the policy gradient derived.
6. LLM research agents: Alpha-GPT (Wang et al. 2023), AlphaAgent (Tang et al. 2025), R&D-Agent-Quant (Li et al.,
   NeurIPS 2025), as reported; an honest protocol. No agent run here.
7. Combining weak alphas: the IC ceiling c/√ρ; the participation ratio; equal against estimated weights;
   residualising against the library (Frisch–Waugh).
8. The trial counter explodes (10,468 → 23,478): the independent-trials bar; a daily-shuffle null that keeps the
   trials' correlation (500 formulas ≈ 32 effective).
9. Decay with the horizon and through time (McLean–Pontiff 2016); signal speed and turnover; WorldQuant and BRAIN
   (public record); crowding.
10. China's quant industry: index enhancement (指数增强), February 2024 (micro-caps, DMA, Ningbo Lingjun's one-minute
    sale and three-day ban), the hedge's arithmetic.
11. High-Flyer (幻方) to DeepSeek; Fire-Flyer 2 (arXiv 2408.14158).
12. What remains for humans: priors (the economics of low volatility: Frazzini–Pedersen; Bali–Cakici–Whitelaw), data,
    judgement, when to stop.
13. The mined combination registered (13,010 trials) and opened on 2021–25: 2.78 ± 0.71 gross, 1.64 net.
14. Rule 29: the alpha factory.
Research: the out-of-sample Sharpe ratio of an estimated combination, SR*/√(1 + K/(T SR*²)) (Brown 1976; Kan–Zhou
2007): derivation, the in-sample mirror, the limit, simulations, the Wishart bias, the bar for one more alpha, the
mined alphas.

*Textbooks:* Kakushadze–Serur *151 Trading Strategies*; Isichenko ch. 2–3; Koza; Sutton–Barto ch. 13.
*Trained:* a random miner, a GP miner (three runs) and a REINFORCE token generator on the crypto cross-section, all on
the trial counter; the LLM-agent miner is described, not run.
*Visuals:* the formula tree growing and splicing; the hurdle against the search; the correlation matrix of mined
alphas; equal against estimated weights by K.
*Crisis:* February 2024 A-share quant drawdown.
*Firms:* WorldQuant; High-Flyer; Ningbo Lingjun (public record).
*Desk:* "You mined 10,000 alphas with average out-of-sample IC 0.01 and correlation 0.3. What's the combined IC?"
*House:* `explainer/quant/house/alphas.py` (the finale uses only what survives deflation).

### Act V · Portfolios, Strategies and the Firm

### Part 30 · Portfolio Construction (~55; built)
0. Hook: the optimizer's promise against its delivery; Act V begins.
1. Error maximisation (Michaud 1989): a known-truth experiment on the 49 industries; Best–Grauer sensitivity;
   Chopra–Ziemba; 5 against 20 years; resampled efficiency (no better).
2. 1/N (DeMiguel–Garlappi–Uppal 2009): the rolling contest 1980–2020 with costs and windows; predicted against
   realised risk; Kan–Zhou (2007) and Tu–Zhou (2011) combinations.
3. Covariance in high dimension: Marchenko–Pastur against the daily spectrum; market and sector modes; crises;
   RMT clipping (Laloux et al. 1999; Bun–Bouchaud–Potters 2017).
4. Ledoit–Wolf, linear (identity, constant correlation) and analytical nonlinear (2020) against the oracle; factor-model
   covariances; the window.
5. Constraints as shrinkage (Jagannathan–Ma 2003), proved and checked; norm constraints (DeMiguel et al. 2009).
6. Black–Litterman: reverse optimisation, a view relative to equilibrium, He–Litterman's view portfolios, confidence;
   Bayes–Stein means (Jorion 1986).
7. Risk parity (Spinu's convex ERC) and HRP (López de Prado 2016).
8. Robust optimisation; VaR's non-subadditivity; CVaR as an LP (Rockafellar–Uryasev 2000).
9. Kelly and fractional Kelly under estimation error; Cover's universal portfolio; Fernholz's diversity weights and the
   excess growth rate.
10. Entropy pooling (Meucci 2008): a stress view on returns and one on volatility.
11. End-to-end portfolios trained on the Sharpe ratio (Zhang–Zohren–Roberts 2020); smart predict-then-optimize
    (Elmachtoub–Grigas 2022).
12. Shrunk minimum variance, HRP and 1/N registered and opened on 2021–25 (0.35, 0.50, 0.58; differences inside one
    standard error).
13. Rule 30: the optimizer.
Research: why the optimizer underestimates its own risk: the exact laws of the sample GMV's reported and true variance
(a Wishart χ² lemma via a Schur complement; Kempf–Memmel's F law), the limits 1 − γ and 1/(1 − γ), simulations,
shrinkage, and the industries.

*Textbooks:* Meucci *Risk and Asset Allocation*; Grinold–Kahn ch. 14–15; Paleologo *Advanced Portfolio
Management*; Chincarini–Kim; Muirhead (Wishart).
*Trained:* the end-to-end portfolio network.
*Computed:* frontiers with error clouds; MP vs empirical spectra; LW vs RMT vs nonlinear vs sample; every rule rolled
1980–2020.
*Visuals:* the true and estimated frontiers diverging; the spectrum against MP; the eigenvalues against the oracle.
*Desk:* "Why does the optimizer love the asset with the most estimation error?"
*House:* `explainer/quant/house/portfolio.py` (the optimizer).

### Part 31 · Risk Models, Costs and Trading Through Time (~55; built)
0. Hook: IC 0.05 on 500 stocks monthly promises 3.87; a moving IC gives 1.58; where the information ratio goes.
1. The fundamental law (Grinold 1989), derived and simulated; the transfer coefficient (Clarke–de Silva–Thorley 2002);
   effective and time breadth; Grinold–Kahn's scale; limits.
2. A Barra-style factor risk model of the coins: standardised styles, daily WLS factor returns, EWMA factor
   covariance, specific variances; industries and the sum-to-zero constraint; the bias statistic; fundamental,
   statistical and macro models (Connor 1995); Barra.
3. Specific risk and Bayesian betas: Blume's regression to one; Vasicek (1973) scored on the next quarter;
   Scholes–Williams and Dimson.
4. Transaction costs: implementation shortfall (Perold 1988); the square-root law; Frazzini–Israel–Moskowitz (2018);
   Novy-Marx–Velikov (2016); a capacity curve; costs inside the optimisation; the κ^{1/3} no-trade band.
5. Gârleanu–Pedersen (2013): the aim portfolio and trade rate, derived and checked by value iteration; Λ ∝ Σ; GP
   against myopic on the coins net of costs.
6. Multi-period optimization (Boyd et al. 2017): receding horizon, per-period forecasts, constraints, a horizon
   experiment with 3/2-power impact.
7. Alpha combination: ic'C⁻¹ic; equal, IC and ridge weights trained 2018–19, judged 2020; horizons; forecast against
   portfolio blending.
8. Decay → turnover → capacity; the 4/9 rule; Berk–Green (2004) with square-root costs (fee a/3); Berk–van Binsbergen.
9. Crowding: August 2007 (Khandani–Lo replayed on the daily industries), the unwind hypothesis, the risk model's blind
   spot, comomentum (Lou–Polk).
10. P&L attribution: factor against specific, Brinson, static against timing, Euler risk contributions; Part 29's mined
    alpha is 86% factor.
11. The aim-portfolio trader registered and opened on 2021–25: −0.96 (research 0.66), through forecast variances near
    zero; the diagnosis; the House's guards.
12. Rule 31: the risk model.
Research: the information ratio when the IC moves: IR = μ/√(σ²(1 − 1/N) + (1 − μ²)/N) proved, simulated, the breadth
N* ≈ 1/σ², and the coins' ladder of corrections (naive 0.52 → moving IC 0.23 → Pearson 0.117 → realised 0.087).

*Textbooks:* Grinold–Kahn *Active Portfolio Management*; Isichenko; Paleologo *The Elements of Quantitative
Investing*; Narang *Inside the Black Box*; Boyd et al. (2017).
*Computed:* a Barra-style risk model of the coins with bias tests; Vasicek betas out of sample; a capacity curve; GP
vs myopic trading net of costs; ridge alpha combination; attribution; August 2007 on the daily industries; the
moving-IC theorem against simulation and the coins.
*Visuals:* the aim portfolio as a moving target; the capacity curve bending; the planned paths by horizon; the ladder
of corrections.
*Crisis:* August 2007 (Khandani–Lo), seen through the risk model.
*Firms:* Barra; AQR's measured trading costs; Goldman's GEO (as announced and reported).
*Desk:* "IC 0.05, 500 stocks, monthly rebalancing. Information ratio?"
*House:* `explainer/quant/house/riskmodel.py` (the risk model, the law, costs and trading, attribution, guards).

### Part 32 · Systematic Macro and Alternative Premia (~55; built)
0. Hook: 2008 (stocks −38%, 60/40 −18%, trend +7%); three kinds of premium: risk, behavioural, structural.
1. Trend following: time-series momentum (Moskowitz–Ooi–Pedersen 2012) on a 23-ETF macro panel; lookbacks and
   sizing; by class; a century of evidence (Hurst–Ooi–Pedersen 2017; Lempérière et al. 2014); AHL/Man, Winton; fees.
2. The smile and the crisis: slow crises, fast crashes, reversals (2009); 2020Q1; the straddle identity; trend as a
   diversifier of 60/40.
3. Volatility targeting asset by asset (Moreira–Muir 2017; Cederburg et al. 2020; Harvey et al. 2018); the leverage
   effect; crowding in vol-control rules.
4. Risk parity: 60/40's risk concentration; leverage aversion (Asness–Frazzini–Pedersen 2012); All Weather (1996) and
   its four environments; leverage dial and financing; the stock–bond correlation 1962–2020 (Campbell–Sunderam–Viceira).
5. Value, momentum, carry and defensive across asset classes, 1926–2020 (AQR, as published); correlations; everywhere
   (Asness–Moskowitz–Pedersen 2013); betting against beta; crisis years.
6. Carry made visible: fund minus spot for oil, gas and six currencies; contango and backwardation; bond carry;
   negative oil (April 2020); a currency carry book and its 2008 crash (Koijen et al. 2018).
7. Selling insurance: Cboe PUT 2007–2020; Israelov–Nielsen; Volmageddon (February 2018); demand-based option pricing.
8. Calendars, nights and events: turn of the month and sell-in-May by era; FOMC days (Lucca–Moench); overnight vs
   intraday (Lou–Polk–Skouras); merger arbitrage, index changes, drift; data mining (Sullivan–Timmermann–White).
9. The trend and risk-parity books registered and opened on 2021–25 (0.27 and 0.15; 2022 +15% and −23%; the
   stock–bond correlation turned positive).
10. Rule 32: the macro books.
Research: why trend following is long a straddle: P = ½(S² − Q) exactly; E P = Σ(n − k)γ_k; skewness
2^{3/2}(n − 2)/√(n(n − 1)) → 2√2 by counting triangles; the limit ½(Z² − 1) and P(P > 0) → 31.7%; simulations and
the 23 funds; diversification, the sign rule, matched filters.

*Textbooks:* Pedersen *Efficiently Inefficient*; Ilmanen *Expected Returns*; Kakushadze–Serur; Clenow *Following the
Trend*.
*Computed:* trend, vol-targeting and risk-parity books on 23 ETFs; the stock–bond correlation since 1962; carry as fund
minus spot; the PUT index; calendar, FOMC and overnight effects; the trend identity simulated and measured.
*Visuals:* the smile and the exact parabolas; the risk-parity leverage dial; the stock–bond correlation; the oil fund
against spot.
*Crisis:* 2022: the stock–bond correlation flip; negative oil (April 2020); Volmageddon (February 2018).
*Firms:* AHL/Man, Winton, Bridgewater (All Weather), AQR's published series.
*Desk:* "Why does trend following have positive skew?"
*House:* `explainer/quant/house/systematic.py` (the macro books).

### Part 33 · Statistical Arbitrage (~55; built)
0. Hook: two prices on an elastic band; what survives on the industries.
1. History: Princeton/Newport (1969), Morgan Stanley's APT group (Bamberger, Tartaglia), D. E. Shaw (1988),
   Renaissance, PDT (1993), as reported; what decimalisation and competition changed.
2. Pairs by distance (Gatev–Goetzmann–Rouwenhorst 2006) re-run on the industries (Sharpe −0.25); Do–Faff 2010; the
   short leg (borrow fees, recalls, the 2008 ban; Engelberg–Reed–Ringgenberg 2018).
3. Cointegration and the screening problem: Engle–Granger year by year (7.3% pass against a 3.7% false-positive rate;
   8.1% pass again); selection-biased half-lives; Johansen baskets; Royal Dutch/Shell (Froot–Dabora 1999).
4. The OU spread: AR(1) map, s-score, Kendall's bias, the half-life's interval; Bertram 2010, Leung–Li 2015.
5. Eigenportfolios and residuals (Avellaneda–Lee 2010): gross 0.88, net −0.39; eight variants against turnover; the
   research band +0.21 net; by era; refinements; hedge netting.
6. Kalman hedge ratios on BTC/ETH: the forecast-error trap (ADF −14.8, half-life 1.3 days); the effective window.
7. Reversal and lead-lag (Lo–MacKinlay 1990; Lehmann 1990): the decomposition computed exactly; the post-1990 flip;
   Roll's bounce; horizons (Jegadeesh; Moskowitz–Grinblatt; De Bondt–Thaler).
8. Learning the residual (Krauss–Do–Huck 2017; Guijarro-Ordonez–Pelger–Zanotti 2021): a network on residual paths,
   IC 0.003, net −7.2.
9. Liquidity, crowding and decay: Grossman–Miller; Nagel 2012 on industries (t −0.26); Shleifer–Vishny 1997; index
   changes and fire sales; August 2007.
10. The residual book registered (9 trials) and opened on 2021–25: gross 1.13, net 0.30; break-even 6–7 bp a side.
11. Rule 33: the stat-arb book.
Research: the optimal band for an OU spread: renewal-reward rate (m − c)/(E_0[τ_m] + E_{−m}[T_0]) from Dynkin; the
universal curve m*/s_eq = h(c/s_eq); frictionless limit σ√(κ/π); the small-cost law m*/s_eq ≈ (3c/s_eq)^{1/3};
simulations and the industries.

*Textbooks:* Vidyamurthy *Pairs Trading*; Pole *Statistical Arbitrage*; Chan *Algorithmic Trading*; Pedersen
*Efficiently Inefficient*; Leung–Li *Optimal Mean Reversion Trading*.
*Computed:* distance pairs, cointegration screens with a random-walk control, the residual book in nine
configurations, a Kalman hedge ratio, Lo–MacKinlay's decomposition, a residual-path network, Nagel's regression, the
optimal band exactly and by simulation.
*Crisis:* August 2007; the 2008 short-sale ban; LTCM's twin-share trade (1998).

### Part 34 · Inside a Quant Firm (~55; industry; built)
0. Hook: a Sharpe-1 manager under a 5% stop at 10% volatility lasts about four months on average.
1. Six business models (prop trading, market making and payment for order flow, platforms, systematic funds, bank
   desks after Volcker, China's quant private funds), public record only.
2. What has been disclosed: Virtu's S-1 (1 losing day in 1,238 = daily Sharpe 3.15 under normality; t tails; the law
   of large numbers); Jane Street's revenue and Medallion's returns as reported, fees checked.
3. The pod model: sizing by volatility budget; the reported 5%/7.5% rules; pass-through fees; a simulated platform
   (investors' Sharpe 1.90 with stops vs 1.19 without when skill varies; ~equal when it does not); selection; netting
   risk; the Jane Street–Millennium case (2024, settled), as reported.
4. From idea to capital: review; the House's Track Record haircut (slope 0.75); incubation; a posterior-sized ramp.
5. Firm-level risk: layers, limits, liquidity in days, stress, crisis correlations; Knight Capital (2012); Rule
   15c3-5; Archegos (2021).
6. Technology: OCaml (Minsky 2011), C++/FPGAs, point-in-time data and kdb+, the light-speed floor Aurora–Carteret;
   colocation; Budish–Cramton–Shim; reproducibility.
7. Compliance: spoofing, layering, marking the close, wash trades; Sarao; J.P. Morgan's $920m; the CAT; detection;
   SEBI's 2025 interim order on Jane Street (allegations, contested).
8. The interview: computed puzzles, a market game with an informed counterparty, Kelly, a Fermi estimate, code.
9. Founding stories as told in public (Thorp, Simons, Shaw, Griffin, Jane Street, Englander, AQR, Two Sigma);
   survivorship.
10. Do drawdown stops help? Six factors, six rules, against i.i.d. shuffle nulls (36 trials, not registered).
11. Rule 34: the firm; the compliance desk.
Research: how long a seat lasts: E[τ] = (e^{2Sδ} − 1 − 2Sδ)/(2S²) and the exponential peak (Taylor 1975; Lehoczky
1977), proved from the reflected drawdown's Dynkin equation and the scale function; regimes; simulations; the stop's
power as a sequential test.

*Textbooks:* Narang *Inside the Black Box*; Isichenko; Paleologo; Zuckerman *The Man Who Solved the Market*;
Patterson *The Quants*; Derman *My Life as a Quant*; Thorp *A Man for All Markets*.
*Computed:* the disclosed-statistic map; the stop-time theorem by simulation; a platform of pods; the Track Record
haircut; factor stops against shuffles.
*Firms:* public record only; allegations labelled.
*House:* the compliance desk and Rule 34.

### Act VI · Market Microstructure

### Part 35 · Who Trades With Whom (~55; built)
1. The dealer: Garman (1976) inventory; Ho–Stoll (1981) shading; Avellaneda–Stoikov; the three components of a spread.
2. Glosten–Milgrom (1985) derived: spread = μ at an even prior; learning in odds; lemons.
3. Kyle (1985): λ = σ_v/(2σ_u) derived and simulated; the N-auction recursion; tightness, depth, resiliency.
4. Roll, Corwin–Schultz and Amihud on ten ETFs: daily spread estimators fail on liquid funds; Amihud ranks liquidity
   (slope −0.94 on dollar volume); effective, realised and impact spreads.
5. Kyle's λ on Binance taker flow: 4.6 bp per $1m (R² 0.21), concave; persistent flow against unpredictable returns;
   by month, hour, coin and horizon.
6. PIN and VPIN: on Bitcoin VPIN tracks volatility (0.67) more than the true imbalance (0.09); markouts.
7. Price discovery: Hasbrouck IS between spot and perpetual (one-minute bars too coarse; bounds 0.95 wide); the
   funding basis.
8. Market structure: Reg NMS, maker–taker, dark pools (Zhu 2014), segmentation, PFOF, the 2024 rules, the closing
   auction, T+1.
9. HFT as market maker (Menkveld 2013; Brogaard et al. 2014); sniping and its tax (Aquilina–Budish–O'Neill 2022);
   back-running.
10. The flash crash (Kirilenko et al. 2017); Bitcoin's daily λ; liquidation cascades; the Treasury flash rally (2014);
    frequent batch auctions (Budish–Cramton–Shim 2015).
11. Rule 35: know who is on the other side.
Research: Kyle in continuous time (Kyle 1985; Back 1992): λ = σ_v/σ_u, profit σ_vσ_u, the Brownian bridge, proved by
Kalman–Bucy and Back's value function; simulated; the discrete limit; Kyle's R² = 1 against Bitcoin's 0.21–0.32.

*Textbooks:* O'Hara *Market Microstructure Theory*; Hasbrouck *Empirical Market Microstructure*;
Foucault–Pagano–Röell *Market Liquidity*; Harris.
*Computed:* the dealer, Glosten–Milgrom and Kyle simulated; Roll, Amihud, Kyle's λ and VPIN on Binance and ETFs;
Hasbrouck IS; daily λ.
*Crisis:* 6 May 2010; 15 October 2014; May 2021 and November 2022 on Bitcoin.
*House:* surveillance; a signed-flow feed.

### Part 36 · The Limit Order Book (~55; built)
1. The book on Binance's BTCUSDT perpetual (best quotes on a 100-ms grid, May 2023): one-tick spread over 99% of the
   time, a median 8-tick jump when the mid moves, so small-tick by Dayri–Rosenbaum; order types.
2. Queues: Cont–Stoikov–Talreja (2010); Cont–de Larrard (2013) P(up) derived from the quadrant's harmonic measure, too
   steep against the data (16% to 86%); queue-reactive (Huang–Lehalle–Rosenbaum 2015).
3. Hawkes on trades (branching 0.68; cluster representation; near-criticality, Hardiman–Bercot–Bouchaud 2013);
   sign memory ℓ^−0.85 (Lillo–Farmer 2004; Lillo–Mike–Farmer 2005); a rising signature plot; same-direction pairs.
4. OFI (Cont–Kukanov–Stoikov 2014): R² 0.37–0.45 at 10 s on every day; impact ∝ depth^−1.17; multi-level, integrated
   and deep OFI (Xu–Gould–Howison; Cont–Cucuringu–Zhang 2023; Kolm–Turiel–Westray 2023).
5. The microprice (Stoikov 2018) with every move counted: ±25 ticks on Bitcoin, worse than the mid out of sample; a
   per-horizon table of mean moves cuts 10-s error 3–5%; the interview answer from a large-tick book.
6. DeepLOB, universal features (Sirignano–Cont 2019), LOBCAST (Prata et al. 2024); our 30-input test: linear 87.2%
   against network 84.0% on direction; the edge per trade (~1.5 ticks) against spread and fees (1 bp ≈ 27 ticks).
7. Simulators: zero intelligence (Smith et al. 2003; Farmer–Patelli–Zovko 2005), ABIDES, generative books (Coletta et
   al. 2021; Nagy et al. 2023); the House's queue-reactive simulator and its five-fact scorecard (one right).
8. Trading in the queue: a passive-order replay on the tape (back: 82% filled, −14.7 ticks at 1 s; front: −1.6); the
   value of queue position (Moallemi–Yuan); the free option (Copeland–Galai 1983); the cancel race.
9. Rule 36: score the book against the spread.
Research: the microprice theorem (H1–H3; first-step, strong-Markov and Perron–Frobenius lemmas; martingale and
uniqueness; why symmetry), checked in the simulator (drift flat, realised drift → g) and on Bitcoin (peaks at 0.46 g;
a direct Markov test rejects H1).

*Textbooks:* Bouchaud–Bonart–Donier–Gould *Trades, Quotes and Prices*; Abergel et al. *Limit Order Books*;
Cartea–Jaimungal–Penalva ch. 1–4.
*Computed:* every number from Binance's `bookTicker` and `aggTrades` and the House simulator. Not built: a generative
transformer; the House's simulator is the queue-reactive model, scored, as the baseline a learned generator must beat.
*Desk:* "Bid 100 × 500, ask 100.01 × 100. Where is fair value?"
*House:* the order-book simulator and the fill replay (used by 37, 38, 42).

### Part 37 · Market Impact and Execution (~55; built)
1. Metaorders, implementation shortfall (Perold 1988), the impact path (two-thirds remains); aggregate impact on ten
   days of Binance trades: sigmoid in imbalance, a minute's move ∝ signed volume^0.81.
2. The square-root law (Loeb; Torre; Almgren et al. 2005; Tóth et al. 2011; Donier–Bonart on Mt. Gox); latent
   liquidity (Donier et al. 2015) derived and simulated (exponent 1.02 → 0.42, Bucci et al. 2019); fair pricing
   (Farmer et al. 2013); invariance (Kyle–Obizhaeva 2016).
3. The propagator (Bouchaud et al. 2004) fitted on 3.4m trades: peak 0.72 tick at 77 trades, decay ℓ^−0.17 against
   (1 − γ)/2 = 0.10; history-dependent impact.
4. No dynamic arbitrage: Huberman–Stanzl; Gatheral (2010) positive definiteness (a box kernel's money machine);
   Alfonsi–Schied–Slynko convexity (a Gaussian kernel buys by selling); Bitcoin's kernel passes (Pólya).
5. Almgren–Chriss derived (discrete and variational); 5,000 BTC in an hour: TWAP 1.6 bp, sd $267k; the frontier; the
   linear model against the square root's 20 bp.
6. Obizhaeva–Wang (2013): blocks and the recovery rate; Bitcoin's sweeps refill in 100–200 ms but the price keeps
   drifting; signals (Cartea–Jaimungal; Lehalle–Neuman); crowding (Cardaliaguet–Lehalle).
7. A Q-learning executor in the Part 36 simulator: 52.7 against TWAP's 50.7 half-ticks; why, and what would do better.
8. TWAP, VWAP, POV, IS; Bitcoin's volume curve; the close; routing; TCA and benchmarks.
9. Rule 37: price the trade before you make it.
Research: the optimal schedule under transient impact (uniqueness, the Fredholm condition, the Obizhaeva–Wang
solution; why measures), checked on a grid, across resilience (saving peaks at 12%) and with Bitcoin's kernel.

*Textbooks:* Bouchaud et al.; Cartea–Jaimungal–Penalva; Guéant; Lehalle–Laruelle.
*Computed:* everything from Binance's trades, best quotes and bars, the latent book and the House simulator; ITCH data
were not used (not public), so the propagator is fitted on Bitcoin.
*Desk:* "Trading 10% of daily volume costs 30 bp. What does 40% cost?" (√ law: 60 bp)
*House:* the execution desk and Rule 37.

### Part 38 · Market Making, ETFs and the Speed Race (~55; built)
1. The maker's P&L (half-spread + rebate − markout ± inventory); spread components (Stoll; Huang–Stoll);
   Avellaneda–Stoikov recalled from Part 11; δ* = 1/k; GLFT (2013); specialists, odd-eighths, wholesalers.
2. A maker replayed on Bitcoin's tape (Part 36's queue model): on 17 May the slow maker loses 19.8 ticks a fill, an
   idealised fast one 8.7, fast and filtered 4.6; never positive on three days; a tick is 0.037 bp.
3. Fill intensities fitted to the tape (A = 0.23/s, k = 0.035/tick); GLFT's quotes about 30 ticks out; tested on
   markouts: break-even near 30 ticks, +19.7 at 45 (an upper bound, from sweeps' overshoot); alpha in quotes
   (Cartea–Jaimungal–Ricci 2014).
4. Tick size and queue position: pinned spreads, the queue race, pro rata, the optimal tick (Dayri–Rosenbaum 2015),
   the tick-size pilot and the 2024 half-cent tick.
5. ETF market making: creation and redemption, the band, a worked arbitrage; HYG −22% to 23 March 2020 with 5.4×
   volume; stale NAVs and full dealers; the Fed's facility; leveraged funds' rebalancing (Cheng–Madhavan).
6. The speed race: Budish–Cramton–Shim (2015), simulated (crossing at 0.364, equal for N = 2–30); Aquilina–Budish–
   O'Neill (2022); the physics of microwave links; batch auctions and speed bumps.
7. HFT economics: Menkveld (2013); Baron–Brogaard–Hagströmer–Kirilenko (2019); costs, hedging, stress, obligations,
   options makers, crypto.
8. Rule 38: quote only what you can measure.
Research: the sniping equilibrium (three lemmas; the theorem for any jump distribution; batch auctions scale it by
δ/τ; welfare; the arms race as a prisoner's dilemma), checked by simulation, in batch auctions and with Bitcoin's own
jumps (h* ≈ 0.33 tick, below the half-tick floor).

*Textbooks:* Guéant; Cartea–Jaimungal–Penalva ch. 10; Lehalle–Laruelle; Gastineau *The Exchange-Traded Funds
Manual*.
*Computed:* everything from Binance's best quotes and trades, Yahoo bars for HYG and TLT, and the sniping simulation.
ITCH markouts were replaced by Bitcoin's (ITCH is not public). The planned RL market maker moved to Part 42, which
trains learning makers against each other; this part tests the analytic quotes on markouts instead.
*Crisis:* Knight Capital (1 August 2012), as reported, as the operational risk that sets Rule 38's kill switch.
*Desk:* "How does a market maker earn a living?" (spread and rebate minus markout; at the touch on Bitcoin it does not)
*House:* the market-making desk and Rule 38. *Note:* the engineering is in [`trading`](../markets/trading/README.md).

### Part 39 · Crypto and DeFi (~57; built)
1. Blockchains and exchanges, custody, 24/7 markets, the exchange as clearing house; FTX from the public record (FTT
   $26 to $1.23 on Binance).
2. CFMMs: x·y = k, slippage on a 5,000 ETH pool, stableswap and weighted pools, the AMM as oracle (Angeris–Chitra
   2020), impermanent loss.
3. LVR (Milionis–Moallemi–Roughgarden–Zhang 2022) on ETH's 2023 minutes: 2.659% measured against σ²/8 = 2.659%;
   break-even volume; the hedged LP as short gamma.
4. Concentrated liquidity (Uniswap v3): efficiency, leaving the range; a learned LP (tabular, simulated) that is narrow
   when calm and out when stormy.
5. MEV (Daian et al. 2020), proposer-builder separation; a sandwich solved and tabulated; defences.
6. Perpetuals: funding, Binance's rule, the no-arbitrage price (He–Manela–Ross–von Wachter 2022); six years of BTC and
   ETH funding (37% of settlements at exactly 0.01%).
7. The cash-and-carry book registered (9 trials) and opened: Sharpe 4.6 on 2020, 2.16 on 2021–25; the venue tail.
8. Stablecoins and runs (Diamond–Dybvig on chain): USDC in March 2023 minute by minute; Terra's spiral; MiCA and the
   GENIUS Act.
9. Cross-border premiums (Makarov–Schoar 2020); GBTC's discount and the spot ETFs (January 2024); the crypto
   cross-section (Liu–Tsyvinski–Wu 2022).
10. Rule 39: count the risks the returns do not show.
Research: LVR proved (envelope and Itô), an exact discrete identity, fees and Poisson blocks (the stationary
mispricing law and P_trade, after Milionis–Moallemi–Roughgarden 2023), checked by simulation, fixed blocks and real
ETH prices (arbitrageurs keep 2.3× the Brownian share at 0.3%).

*Textbooks:* Harvey–Ramachandran–Santoro *DeFi and the Future of Finance*; Narayanan et al. *Bitcoin and
Cryptocurrency Technologies*.
*Trained:* the learned LP (tabular, in simulation).
*Computed:* LVR against IL on real prices; fees and blocks; funding and the premium; the carry book; USDC, UST, LUNA and
FTT from Binance; GBTC and IBIT from Yahoo. Terra's on-chain supply was not computed (no node access); it is quoted.
*Crisis:* Terra/LUNA (May 2022); FTX (November 2022); USDC and SVB (March 2023).
*Firms:* Jump's affiliate Tai Mo Shan (the SEC's settled order, December 2024); Binance (2023 plea); Grayscale and
BlackRock (the ETFs).
*Desk:* "An LP in an x·y = k pool; the price doubles. Loss vs holding?" (≈ 5.7%; the right measure is LVR)
*House:* the digital-assets desk and Rule 39.

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
