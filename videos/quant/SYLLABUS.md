# Quant, Built: the syllabus (plan of record, draft 1)

Goal: a university- and desk-level course in video, **as complete and as close to the academic and industry
frontier as possible**. It tells **how quantitative finance became what it is today** alongside the mathematics,
and it tests every idea on real data. It is in English and Chinese to the standard of *AI, Built* and *Analysis,
Built*, and renders on macOS and Linux. Each part runs **30–60 minutes**, as its content needs. The plan totals
about 28 hours across 33 parts.

The series is built the way *AI, Built* was built. [`videos/ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md) is the
working guide for a part: layout, chapters, the narration-follows-data rule, compute, the QA loop and Chinese.
This file states only what differs or is new.

## 1. The standard every part meets

**A chapter is a lecture segment of 3–5 minutes**, in the AI series' order:

1. A motivating question, a market fact, or a failure.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("Itô", "no arbitrage", "tower property",
   "complete the square").
4. A computed experiment that checks the result, on real data where possible and on a `simulated` market whose
   truth is known otherwise.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**
- An objectives card.
- Theorem and definition cards.
- **A crisis file.** The real event where the part's idea broke or was tested, measured from data.
- A problem set: 4–6 problems, about 90 s on screen, with full solutions in the part's README in English and
  Chinese.
- A reference card listing textbooks, the classic papers, the frontier papers and, where public, the industry
  sources (practitioner papers, exchange and regulator documents).

**The history thread.**
- Every part opens with its era ("how we got here", 2–3 min), lit on the timeline strip.
- Every idea is credited with its people and year.
- The arc runs through:
  - Bachelier and the random walk (1900–1965);
  - portfolio theory and CAPM (1952–1964);
  - the option-pricing revolution and the Chicago Board Options Exchange (1973);
  - the rise of the quants on Wall Street: the Morgan Stanley APT group, Salomon's bond arbitrage, D. E. Shaw,
    Renaissance, and the derivatives desks of the 1980s–90s;
  - the crises that reshaped the models (1987, 1998, 2007–08);
  - electronic markets and high-frequency trading (Reg NMS, 2005–07; the 2010 flash crash);
  - post-crisis plumbing: XVA, central clearing, the end of LIBOR;
  - the factor zoo and the replication debate (2014–2023);
  - machine learning and AI asset pricing (2018–).
- The timeline strip (`explainer.quant.timeline`, 1900–2030) gains each part's milestones: ideas in gold, crises
  in red.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the writing
date. Primary sources here are journals, SSRN and arXiv working papers, and regulator and exchange publications.
The frontier items marked *(verify)* below are 2024–2026 working papers or events recalled from secondary sources.
Each is checked against the paper or filing before it goes on screen, and dropped if it does not hold up. A part
may find newer work in its sweep and add it.

**Industry, honestly.** Desk practice is taught as practice: how a volatility desk marks a surface, how an
execution desk measures slippage, how a multi-manager platform sets risk limits. It is taught only from the public
record (practitioner papers in *Risk* and the *Journal of Portfolio Management*, firm research that has been
published, regulatory filings, court records, exchange specifications). Firms are named only for what they have
published or what is documented about them. Every part carries the line *not investment advice*.

**Numbers are real.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/quantN/`. Published numbers are cited.
  Schematics are labeled `schematic`, made-up examples `illustrative`, and synthetic markets `simulated`, with
  their generating model stated.
- Market data is frozen (Section 4): each part reads its data through a fetch module that verifies a SHA-256
  checksum, so every render sees the same numbers.
- CPU budget: ≤ 2 h per part by default. Named exceptions (the deep hedger in Part 12, the return-prediction
  models in Part 20, the LLM experiments in Part 21, the generative order book in Part 26, the agents in Part 32)
  get ≤ 12 h, are resumable, and are seeded.
- Scene assertions use tolerances, not exact equality, so macOS (Accelerate) and Linux (OpenBLAS) builds agree.

**The P/Q discipline.** Every result says which measure it lives under. Q-results (prices, hedges, calibrations)
are scored on the Surface or against a replication argument. P-results (forecasts, premia, strategies) are scored
on the Track Record, net of a stated cost model, with the trial counter running. A colour carries the distinction
on every screen: `C.Q` for risk-neutral objects and `C.P` for real-world ones.

**Visual standard** (3Blue1Brown manner; *AI, Built*'s `explainer/ai/viz.py`, plus `explainer/quant/viz.py`):

| Instrument | What it shows |
|---|---|
| `VolSurface` | the implied-volatility surface in 3D, with a camera tour and model surfaces morphing onto it |
| `PathFan` | thousands of Monte Carlo paths, with the terminal density growing on the side and the payoff under it |
| `HedgeLedger` | a hedged position's P&L split live into gamma, theta, vega and costs as the path runs |
| `BinomialTree` | the replication tree, with values flowing back and the hedge at each node |
| `PayoffDiagram` | payoffs and prices, Greeks as slopes and curvatures |
| `CurveMorph` | the yield curve through time (Treasury daily), with PCA modes as handles |
| `FrontierPlot` | the efficient frontier, with portfolios as glowing points and estimation error as a cloud |
| `OrderBookLadder` | bids and asks with queues, orders arriving and cancelling (shared with `trading`) |
| `ImpactTrace` | a metaorder's price path, with the square root and the propagator decay |
| `CopulaCloud` | joint draws in the unit square, with the tails lit |
| `ContagionNet` | a banking network, losses flowing along exposures (Eisenberg–Noe) |
| `AMMCurve` | the constant-product curve, with a trade moving along it and the arbitrageur's take |
| `DrawdownStrip` | a strategy's equity curve with its drawdowns shaded and the sealed-envelope line |
| `TrialCounter` | the running count of backtests, and the hurdle it raises |
| `crisis_card` | the date, the event, and the measured damage |
| 3D camera tours | the surface, densities in time, loss landscapes of calibration, the HJB value function |

**Bilingual standard (as *AI, Built*).**
- Every narration line has its `narration_zh.json` entry.
- Every on-screen string is in `quant_text_zh.json`, and `tools/collect_text.py --check quantN` is clean.
- The glossary in `QUANT_ZH_GUIDE.md` is extended for every new term, following mainland usage in textbooks and
  practice: 风险中性测度, 隐含波动率曲面, 粗糙波动率, 做市, 冲击成本, 因子动物园, 回测过拟合, and so on.
- `zh_follow_numbers.py` and `check_narration.py` (listen test) are run in both languages.

**Gates per part:**
- `tools/lecture_length.py`: an estimate before render, the measured length after; fails under 30 min.
- `contact_sheet.py`, `dead_air.py`, `collect_text.py --check` and `check_narration.py`.
- `qa_series.py` and `qa_audio.py`, as for *AI, Built*, once those tools take `--series quant`.

## 2. The devices

**The Surface** (`explainer.quant.surface`; computed in Part 1, `.cache/quant1/surface.json`). One full options
surface, all listed strikes and maturities, on one fixed day, plus the following trading day for out-of-sample
checks. The primary candidate is a Deribit BTC surface: it has hundreds of quotes and is public and free. The
choice is made in Phase 0, and an equity-index surface is added if a licensable free source is found. Rows:

| Part | Model |
|---|---|
| 7 | Black–Scholes, one volatility per maturity |
| 8 | SVI and SSVI; local volatility (Dupire), checked by repricing |
| 9 | Heston; SABR; Bates (stochastic volatility with jumps) |
| 10 | rough Bergomi; quadratic rough Heston; a path-dependent volatility model |
| 12 | a neural-network calibrator for rough Bergomi (its speed); a neural SDE |

The columns are: in-sample implied-volatility RMSE (vol points, vega-weighted), next-day RMSE with parameters held,
static-arbitrage violations, parameter count, and calibration time on this CPU.

**The Track Record** (`explainer.quant.track`) and **the sealed envelope**.
- The research window ends 31 December 2020; the hold-out runs from 1 January 2021 to the freeze date set in
  Phase 0.
- A strategy is registered in its part with a code hash, its parameters, its universe, its cost model and its
  number of trials. The hold-out is then opened for it once, in that part's last chapter, and the result is shown
  whatever it is. Narration branches on the result (*AI, Built*'s rule: never hide a disappointing number,
  explain it).
- Rows: market timing on the Welch–Goyal predictors (Part 20); size, value, momentum, profitability,
  betting-against-beta and time-series momentum (Part 17); a shrinkage SDF (Part 18); gradient boosting and a
  network on characteristic portfolios, the random-features "complex" timer, and a transformer across assets
  (Part 20); an LLM sentiment signal on FOMC text (Part 21); a minimum-variance and an HRP portfolio (Part 22);
  PCA-residual stat arb (Part 24); a crypto carry and momentum book (Part 29).
- Columns: annualized return, volatility, Sharpe (with a standard error), maximum drawdown, turnover, and Sharpe
  net of costs. The finale adds the deflated Sharpe.

**The trial counter** (`explainer.quant.trials`). Each compute item that backtests declares how many
configurations it evaluated. The counter sums these across parts, and the declarations are code, so the count
regenerates with everything else. Part 19 introduces it with the count so far. The finale uses the full count.

**The crisis file** (`explainer.quant.crisis_card`). Its index is in Section 3, part by part. Each crisis is shown
with data (prices, spreads, volumes on the day), and the narration measures what happened and does not just tell
the story.

**Payoff cards and the timeline** come from *AI, Built* (`explainer.ai.payoff_card`), on a 1900–2030 strip.

## 3. Part by part

Length targets are estimates; content decides. *Computed* lists the part's own experiments. *Crisis* is the
crisis file.

### Act I · Foundations

### Part 1 · The Fair Game (~50 min)
1. Paris, 1900: Bachelier's thesis, Poincaré's report, the rente market; Regnault's square-root-of-time law
   (1863).
2. Prices and returns: simple vs log returns, compounding, the arithmetic vs geometric mean, volatility drag
   σ²/2.
3. The random walk: Kendall (1953), Osborne (1959), Samuelson (1965), "properly anticipated prices fluctuate
   randomly", proved in its one-line form.
4. Testing it: autocorrelations, the variance ratio (Lo–MacKinlay 1988), computed on 94 years of daily US market
   returns (1926–2020).
5. The stylized facts (Cont 2001): heavy tails with an inverse cubic law, volatility clustering, the leverage
   effect, aggregational Gaussianity, and no linear autocorrelation with strong autocorrelation of |r|. Each is
   measured.
6. Mandelbrot's cotton (1963) and why variance might not exist; the tail index from a Hill plot (preview of
   Part 30).
7. Efficient markets (Fama 1970) in three forms; the joint-hypothesis problem.
8. Grossman–Stiglitz (1980): why perfectly efficient markets are impossible; Black's "Noise" (1986).
9. Two worlds, P and Q: the first look at a risk-neutral density beside a real-world one, both from data.
10. Who is on the other side? Hedgers, speculators, market makers, liquidity providers; zero-sum before costs,
    negative-sum after (Sharpe 1991, preview).
11. The devices: the Surface frozen, the sealed envelope, the trial counter at zero, the timeline.

*Computed:* stylized facts on Ken French daily market returns (1926–2020) and on BTC (Binance, 1-minute and
daily); variance ratios with standard errors; the Surface frozen and checked for staleness and crossed quotes.
*Visuals:* Bachelier's random walk drawn as his figure, then as 4 million steps; the return histogram's tails on
log axes unfolding against the Gaussian; |r| autocorrelation decaying like a power law.
*Crisis:* 19 October 1987, a −20.5% day: how many standard deviations a Gaussian gives it, and how often a cubic
tail says it should happen.

### Part 2 · Martingales and Measure (~50)
1. Probability spaces and filtrations as information: what you know at time t.
2. Conditional expectation as orthogonal projection; the tower property.
3. Martingales: Ville (1939) named them after a betting system; Doob.
4. You cannot beat a fair game: the optional stopping theorem, and its hypotheses are why it is true.
5. The doubling strategy wins almost surely and has a ruinous expected drawdown; admissibility; Barings (1995):
   doubling down in Nick Leeson's "88888" error account.
6. The Doob decomposition: drift plus martingale (signal plus noise).
7. Change of measure on a coin: likelihood ratios and the Radon–Nikodym derivative; equivalent measures agree
   on what is impossible.
8. The law of large numbers and the CLT, and their failure under heavy tails: stable laws (Lévy; Fama 1965;
   Mantegna–Stanley 1995, the truncated Lévy flight).
9. Martingale convergence; the gambler's ruin.
10. Game-theoretic probability (Shafer–Vovk): testing by betting, e-values and anytime-valid inference (Ramdas
    et al. 2023). It comes back in Part 19 as a strategy monitor.

*Computed:* doubling-strategy drawdown distributions; stable-law fits; e-process tests of "returns are a
martingale" on daily data.
*Visuals:* conditional expectation as projection onto coarser and coarser partitions; the doubling strategy's
equity curves with the rare catastrophic path lit.
*Crisis:* Barings 1995.

### Part 3 · Stochastic Calculus (~55)
1. Brownian motion as the scaling limit (Donsker); Wiener (1923).
2. Quadratic variation and (dW)² = dt.
3. The Itô integral: left endpoints as no-peeking; the isometry; Stratonovich and when it is right.
4. Itô's lemma; geometric Brownian motion and the lognormal.
5. SDEs: existence and uniqueness, Euler–Maruyama and Milstein, with strong and weak orders computed.
6. Ornstein–Uhlenbeck and CIR (mean reversion; rates and volatility come back).
7. Feynman–Kac: expectations solve PDEs (Kolmogorov backward).
8. Girsanov and Cameron–Martin: drift is a change of measure. The bridge from P to Q.
9. Martingale representation: why a hedge exists.
10. Local time and Tanaka's formula; the stop-loss start-gain paradox (Carr–Jarrow 1990).
11. Jumps: Poisson and compound Poisson, the Lévy–Itô decomposition, Itô for jumps.
12. Fractional Brownian motion (Mandelbrot–Van Ness 1968): Hurst H, and why it is not a semimartingale.
13. Rough paths and signatures (Lyons 1998; Chen 1957): a path described by its iterated integrals. They come
    back in Parts 10, 12 and 32.

*Computed:* QV convergence; Euler vs Milstein orders; Girsanov reweighting checked against a shifted simulation;
the stop-loss start-gain hedging error measured.
*Visuals:* `PathFan` with densities in 3D, the Fokker–Planck surface under it; fBM paths at H = 0.1, 0.5, 0.9 side
by side.
*Note:* the `stochastic` video is the gentle version; this part assumes it and goes further (jumps, local time,
fBM, signatures).

### Part 4 · Time Series and Volatility (~55)
1. Stationarity, ARMA, the Box–Jenkins programme (1970).
2. Unit roots: Dickey–Fuller, spurious regression (Granger–Newbold 1974), computed.
3. Cointegration (Engle–Granger 1987, Johansen): the setup of Part 24.
4. Regimes: Hamilton (1989) Markov switching; the Kalman filter (1960) for latent states.
5. Volatility clusters: ARCH (Engle 1982) and GARCH(1,1) (Bollerslev 1986), likelihood on screen.
6. Asymmetry: EGARCH, GJR; the leverage effect; DCC (Engle 2002).
7. "Does anything beat a GARCH(1,1)?" (Hansen–Lunde 2005); robust losses for volatility forecasts (Patton
   2011).
8. Realized volatility (Andersen–Bollerslev–Diebold–Labys): sum of squared intraday returns, converging to
   integrated variance.
9. Microstructure noise: the signature plot, two-scale (Zhang–Mykland–Aït-Sahalia 2005), realized kernels.
10. HAR-RV (Corsi 2009): a cascade of horizons; HARQ.
11. Jumps vs diffusion: bipower variation (Barndorff-Nielsen–Shephard).
12. Roughness in the data: log realized vol scaling at H ≈ 0.1 (Gatheral–Jaisson–Rosenbaum 2018), measured.
    The debate is left open for Part 10.

*Computed:* GARCH and HAR on the market index and BTC; the signature plot from 1-minute BTC; the Hurst estimate
of log realized volatility with its estimator bias checked on simulated paths.
*Visuals:* volatility as a slow hidden river under the noisy returns; the signature plot collapsing as sampling
slows.
*Crisis:* the March 2020 volatility spike, and what each model forecast the day before.

### Part 5 · Decisions Under Uncertainty (~50)
1. Expected utility (von Neumann–Morgenstern); risk aversion (Arrow–Pratt); certainty equivalents.
2. Dynamic programming (Bellman 1957); the Hamilton–Jacobi–Bellman equation derived from a one-step argument.
3. Merton's problem (1969/71): the optimal fraction (μ − r)/(γσ²), derived by HJB and checked by simulation.
4. Kelly (1956) and growth-optimal betting; Thorp's blackjack and the market; fractional Kelly; Samuelson's
   objection (1979).
5. Ergodicity and time averages vs ensemble averages, and the controversy around them.
6. Optimal stopping: the Snell envelope; the secretary problem; American options preview.
7. Prospect theory (Kahneman–Tversky 1979): loss aversion and probability weighting, measured preferences.
8. Ambiguity: Ellsberg, maxmin (Gilboa–Schmeidler), robust control (Hansen–Sargent).
9. BSDEs (Pardoux–Peng 1990; El Karoui–Peng–Quenez 1997): pricing and hedging as backward equations. They come
   back in Parts 12 and 14.
10. Many agents: mean-field games (Lasry–Lions; Huang–Malhamé–Caines 2006). They come back in Parts 27 and 32.

*Computed:* Merton by HJB finite differences vs Monte Carlo; Kelly growth curves and drawdown risk at full vs half
Kelly.
*Visuals:* the HJB value function as a 3D surface with the optimal control flowing over it; Kelly's growth parabola
with ruin on the far side.
*Crisis:* a Kelly bettor with the wrong edge, using Long-Term Capital's published leverage as the setting (full
story in Part 31).

### Act II · Pricing (Q)

### Part 6 · No Arbitrage (~50)
1. Arbitrage defined; the law of one price; put–call parity, and where it fails in practice (hard-to-borrow
   stocks, dividends, early exercise).
2. One period: payoff matrices; the FTAP by a separating hyperplane (Farkas), proved.
3. State prices (Arrow–Debreu) and the stochastic discount factor; why Q is the SDF renormalized.
4. The binomial tree (Cox–Ross–Rubinstein 1979): replication backwards, the hedge at each node.
5. Completeness and the second FTAP; incomplete markets and super-replication bounds as linear programs.
6. Continuous time: Harrison–Kreps (1979), Harrison–Pliska (1981), Delbaen–Schachermayer (NFLVR, 1994), told
   as history with the key idea.
7. Change of numeraire: forward measures and annuity measures. Rates and FX use them.
8. Breeden–Litzenberger (1978): the second derivative in strike is the density. Extracted from the Surface.
9. Ross recovery (2015): can we get P from Q? And the critique (Borovička–Hansen–Scheinkman 2016).
10. Robust bounds: model-free super-replication given the smile; martingale optimal transport (Hobson 1998;
    Beiglböck–Henry-Labordère–Penkner 2013); the bounds for a forward-start option, computed by LP.

*Computed:* the FTAP LP on a three-state market; the implied density from the Surface (smoothed, with its
arbitrage checks); MOT price bounds.
*Visuals:* the separating hyperplane between payoffs and the positive orthant; the tree folding back; the density
emerging as the smile is differentiated twice.
*Crisis:* the 2021 GameStop options and borrow market: put–call parity violations, measured where public data
allows.

### Part 7 · Black–Scholes–Merton (~55; the pilot)
1. 1973: Black, Scholes, Merton; the CBOE opens; Thorp's earlier formula; the TI calculator on the floor.
2. Derivation 1: replicate with stock and bond, the PDE.
3. Derivation 2: the risk-neutral expectation by Girsanov.
4. Derivation 3: the binomial tree's limit.
5. The Greeks as geometry: delta, gamma, theta, vega; the Θ = −½Γσ²S² identity (at r = 0).
6. The fundamental hedging P&L: ½ΓS²(σ²_realized − σ²_implied)dt, derived and watched on a path.
7. Hedging with the wrong volatility (El Karoui–Jeanblanc–Shreve 1998): robustness, path-dependence of the P&L.
8. Discrete hedging error ∝ 1/√N (Boyle–Emanuel 1980), measured; transaction costs and Leland (1985).
9. Implied volatility: inverting the formula (Newton, Jäckel's "Let's be rational"); the first look at the smile.
10. American options: early exercise, the free boundary, the binomial put.
11. Dividends, borrow, and the forward: what traders actually price.
12. 1987: portfolio insurance (Leland O'Brien Rubinstein), the crash, and the birth of the skew.
13. 1997 to 1998: the Nobel, and then LTCM (preview of Part 31).
14. The Surface's first row: flat volatility per maturity.

*Computed:* delta-hedging replays on simulated GBM, on Heston paths (wrong model), and on real BTC hourly paths
against Deribit implied vols; hedging error vs rebalancing frequency; Leland's adjusted volatility checked.
*Visuals:* `HedgeLedger`, with gamma gains and theta bleed ticking against each other; the tree converging to the
PDE solution in 3D.
*Crisis:* 19 October 1987.

### Part 8 · The Volatility Surface (~55)
1. Smile, skew, term structure; quoting in delta; sticky strike vs sticky delta; the surface over time.
2. Static no-arbitrage: butterfly (convexity in strike) and calendar (total variance increasing), and Roper's
   conditions.
3. Wing behaviour: Lee's moment formula (2004).
4. Parameterizations: SVI (Gatheral 2004), its arbitrage-free SSVI (Gatheral–Jacquier 2014), fitted to the
   Surface.
5. Local volatility: Dupire (1994) derived; Derman–Kani trees; Gyöngy's projection theorem.
6. Why local volatility misprices the forward smile.
7. Variance swaps: the log-contract replication (Carr–Madan; Demeterfi–Derman–Kamal–Zou 1999).
8. The VIX formula derived from the replication and computed: our own BTC index vs Deribit's published DVOL.
9. The variance risk premium (Carr–Wu 2009; Bollerslev–Tauchen–Zhou 2009): implied above realized, measured;
   who earns it and why.
10. Dealer gamma and intraday dynamics (Ni–Pearson–Poteshman 2005; Baltussen et al. 2021); the 0DTE era
    (Bandi–Fusari–Renò 2023; Dim–Eraker–Vilkov 2024).
11. Volatility products: VIX futures, the term-structure roll, short-vol ETPs.

*Computed:* SVI/SSVI fits with arbitrage checks; Dupire local vol from the fit and Monte Carlo repricing; our VIX
on Deribit vs DVOL; the VRP from DVOL and realized BTC volatility, and from VIX vs realized S&P (FRED, Ken French).
*Visuals:* `VolSurface` camera tour; butterfly violations glowing red where a raw fit breaks; the variance-swap
replication as a strip of options weighted 1/K².
*Crisis:* Volmageddon, 5 February 2018: the VIX doubled in a day and XIV lost more than 90%.

### Part 9 · Stochastic Volatility and Jumps (~55)
1. Why volatility must move: the smile's dynamics.
2. Heston (1993): the model, the characteristic function by an affine ansatz (Riccati equations), the Feller
   condition.
3. Simulating Heston: why Euler fails; Andersen's QE scheme.
4. SABR (Hagan et al. 2002): the expansion, its backbone, negative densities at low strikes, and arbitrage-free
   fixes.
5. Jumps: Merton (1976), Kou (2002), Bates (1996); the short-maturity skew that only jumps can produce.
6. Lévy models: variance gamma, CGMY; time changes.
7. Stochastic local volatility: the leverage function by the particle method (Guyon–Henry-Labordère).
8. The forward smile and cliquets: where models disagree with the same vanilla prices.
9. The SPX/VIX joint puzzle: why classical models fail both at once (Gatheral 2008), set up for Part 10.
10. Calibration as optimization: loss landscapes, identifiability, parameter instability day to day.

*Computed:* Heston and Bates calibrated to the Surface by Fourier pricing; SABR per maturity; the calibration loss
landscape in 3D; exotic-price dispersion across models fitted to the same vanillas.
*Visuals:* the Heston variance process as a second, slower river; the calibration loss surface with the optimizer
wandering in its flat valley.
*Crisis:* the post-1987 smile, and implied binomial trees (Rubinstein 1994).

### Part 10 · Rough and Path-Dependent Volatility (~60; a frontier part)
1. The fact: the at-the-money skew explodes like T^{H−1/2} at short maturities; no Markov model with few factors
   does that.
2. Volatility is rough (Gatheral–Jaisson–Rosenbaum 2018): the scaling of log realized volatility, re-measured
   (Part 4).
3. Rough Bergomi (Bayer–Friz–Gatheral 2016): the Volterra kernel, simulation by the hybrid scheme
   (Bennedsen–Lunde–Pakkanen 2017).
4. Rough Heston (El Euch–Rosenbaum 2019): the fractional Riccati equation and its Adams scheme.
5. Where roughness comes from: nearly unstable Hawkes processes and metaorder splitting (Jaisson–Rosenbaum 2016;
   El Euch–Fukasawa–Rosenbaum 2018).
6. Markovian lifts: multi-factor approximations (Abi Jaber–El Euch 2019; the lifted Heston).
7. The debate: estimator bias (Fukasawa et al.), "rough volatility: fact or artefact?" (Cont–Das 2024), "does
   the ATM skew really follow a power law?" (Guyon–El Amrani 2023). The evidence for each side is shown.
8. Path-dependent volatility (Guyon–Lekeufack 2023): volatility is mostly a function of past returns, and the
   4-factor PDV model.
9. The quadratic rough Heston (Gatheral–Jusselin–Rosenbaum 2020) and the joint SPX/VIX calibration.
10. Solving the puzzle without parametric models: Guyon's (2020, 2022) Schrödinger-bridge / dispersion-constrained
    martingale transport.
11. Signature volatility models (Cuchiero–Gazzetta–Svaluto-Ferro 2023).
12. What desks use and why: the rough models' speed problem (solved by Part 12's neural calibrators).

*Computed:* rBergomi and rough Heston on the Surface (new rows); the skew term structure fitted by power law vs a
two-factor Bergomi; a PDV regression of DVOL on past BTC returns; the Hurst estimator on simulated rough and
non-rough paths, showing its bias.
*Visuals:* fBM paths sharpening as H → 0; the skew term structure on log–log axes with each model's line; the PDV
kernel decaying.
*Crisis:* 5 August 2024: the VIX printed 65 intraday on thin pre-market quotes. What an index of illiquid wings
measures, and what path-dependent models predicted.

### Part 11 · Computing Prices (~60)
1. Monte Carlo at 1/√n; the price of a basket and an Asian option.
2. Variance reduction: antithetics, control variates (the geometric Asian), importance sampling for deep
   out-of-the-money options.
3. Quasi-Monte Carlo: Sobol sequences, the Brownian bridge construction, effective dimension.
4. Multilevel Monte Carlo (Giles 2008): cost ε⁻²(log ε)² instead of ε⁻³ for Euler paths, derived and measured.
5. Longstaff–Schwartz (2001): regression for early exercise; low and high bounds (Andersen–Broadie duality).
6. Greeks: bump-and-revalue, pathwise, likelihood ratio (Broadie–Glasserman 1996).
7. Adjoint algorithmic differentiation (Giles–Glasserman 2006, "Smoking adjoints"): all Greeks for a small constant
   multiple of the cost of one price, with the series' own autodiff (AI Part 4).
8. Finite differences: explicit stability, implicit, Crank–Nicolson and Rannacher smoothing; American options as
   a linear complementarity problem.
9. Two dimensions: ADI for Heston (Craig–Sneyd; in 't Hout–Foulon).
10. Fourier pricing: Carr–Madan FFT, the Lewis formula, the COS method (Fang–Oosterlee 2008).
11. Hardware: why banks moved risk to GPUs; a note on quantum amplitude estimation and its real speedup.

*Computed:* convergence plots for every method; MLMC cost vs ε; LSM vs the binomial American put; AAD cost ratio
across 10–1000 Greeks; COS vs FFT vs quadrature accuracy for Heston.
*Visuals:* the error vs cost race between methods on one log–log plot; Sobol points filling the square beside
random ones; the AAD tape running backwards.

### Part 12 · Deep Pricing and Hedging (~60; a frontier part)
1. History: Hutchinson–Lo–Poggio (1994) learn Black–Scholes from data.
2. Neural calibration: learn the parameters-to-surface map, then calibrate rough Bergomi in milliseconds
   (Horvath–Muguruza–Tomas 2021).
3. Differential machine learning (Huge–Savine 2020): train on pathwise derivatives and learn the pricer from one
   simulation.
4. High-dimensional PDEs: the deep BSDE method (Han–Jentzen–E 2018), a 100-asset basket.
5. Deep optimal stopping (Becker–Cheridito–Jentzen 2019): Bermudan max-calls with bounds.
6. Deep hedging (Buehler–Gonon–Teichmann–Wood 2019): hedging with costs under a convex risk measure (CVaR);
   indifference prices; the learned hedge ratio's no-trade band.
7. What the deep hedger learns: it rediscovers Leland and Whalley–Wilmott bands, compared.
8. Neural SDEs calibrated to vanillas with robust exotic bounds (Gierjatowicz–Sabate-Vidales–Šiška–Szpruch–Žurič
   2022).
9. Market generators: Quant GANs (Wiese et al. 2020), signature-based simulators (Buehler et al. 2020),
   diffusion models for paths (AI Part 21); how to tell whether generated paths are any good (signature MMD,
   stylized-fact checks).
10. Production realities: model risk, explainability, validation (SR 11-7), and what has and has not reached the
    desks *(verify: public deployments)*.

*Computed:* the NN calibrator (rows on the Surface); differential ML vs plain regression; deep BSDE in 100
dimensions vs MC; **our deep hedger**, trained on CPU under proportional costs, replayed through training with its
hedge ratio and P&L histogram scrubbed together (`TrainingReplay`); a market generator scored on the stylized facts
of Part 1.
*Visuals:* the learned hedge as a surface in (time, spot) that sharpens into a band; real vs generated paths
indistinguishable in a lineup.

### Part 13 · Interest Rates (~60)
1. Bonds and discounting; yields, forwards and the par curve; bootstrapping from Treasuries.
2. Duration and convexity derived; the Taylor ladder of a bond price.
3. Curve fitting: Nelson–Siegel (1987), Svensson (1994); the Fed's GSW curve.
4. PCA: level, slope, curvature (Litterman–Scheinkman 1991), computed on 30+ years of curves.
5. Short-rate models: Vasicek, CIR, Hull–White fitted to today's curve; affine term structures (Duffie–Kan 1996).
6. HJM (1992): the drift condition derived; why the forward curve's drift is fixed by its volatility.
7. LIBOR market model (BGM, Jamshidian 1997); caps, floors and swaptions; Black vs Bachelier quotes.
8. The term premium: expectations vs risk; ACM and Kim–Wright estimates; the rate hikes of 2022.
9. LIBOR's end: the 2012 scandal, SOFR, compounded-in-arrears rates and the forward market model
   (Lyashenko–Mercurio 2019).
10. Negative rates in Europe and Japan: why the normal model returned (callback to Bachelier).
11. Multi-curve and collateral discounting (OIS) after 2008.

*Computed:* bootstrapped and NSS curves; PCA on GSW daily; Hull–White calibration; the HJM drift checked by
simulation; SOFR compounding from New York Fed data; the ACM term premium plotted with events.
*Visuals:* `CurveMorph` playing three decades of curves; PCA modes as handles that bend the curve; duration as the
tangent and convexity as the gap.
*Crisis:* the September 2022 gilt crisis (liability-driven investment, collateral calls, the Bank of England's
intervention); SVB, 10 March 2023, its held-to-maturity loss computed from public filings by the duration formula.

### Part 14 · Credit and XVA (~55)
1. Merton (1974): equity as a call on the firm; distance to default; KMV.
2. First passage (Black–Cox 1976); why structural spreads are too low at short maturities.
3. Reduced form: default intensities (Jarrow–Turnbull, Duffie–Singleton); survival as discounting.
4. CDS: the premium and protection legs; bootstrapping hazard rates; the 2009 Big Bang standardization.
5. Portfolio credit: Vasicek's large homogeneous pool (the Basel IRB formula, derived).
6. The Gaussian copula (Li 2000) and CDO tranches; base correlation; the t-copula and tail dependence.
7. 2008: the economics of structured finance (Coval–Jurek–Stafford 2009); ratings; correlation risk.
8. Counterparty risk: exposure profiles (EE, PFE) by Monte Carlo; CVA and DVA.
9. The XVA family: FVA (Burgard–Kjaer 2011), KVA, MVA; wrong-way risk.
10. Margin and central clearing: initial margin, ISDA SIMM, CCP default waterfalls.

*Computed:* Merton distances to default from public balance sheets; tranche loss distributions under Gaussian vs t
copulas; an interest-rate swap's exposure profile and CVA by MC, with AAD sensitivities from Part 11.
*Visuals:* `CopulaCloud` with tails lit, Gaussian vs t; the tranche "waterfall" filling with losses; exposure fans
over the swap's life.
*Crisis:* 2007–08 senior tranches; Archegos (March 2021): total return swaps, hidden concentration, and what
margin models missed.

### Part 15 · FX, Commodities and the Basis (~50)
1. Covered interest parity as an arbitrage, and its post-2008 violation (Du–Tepper–Verdelhan 2018): why balance
   sheets became costly.
2. Uncovered interest parity and the forward-premium puzzle (Fama 1984).
3. The carry trade and crash risk (Brunnermeier–Nagel–Pedersen 2008; Lustig–Roussanov–Verdelhan 2011).
4. FX options: Garman–Kohlhagen, the smile in delta, risk reversals and butterflies.
5. Commodities: storage theory (Kaldor, Working), convenience yield, contango and backwardation, the roll.
6. Commodity futures as an asset class (Gorton–Rouwenhorst 2006); the financialization debate.
7. Negative oil, 20 April 2020: storage at Cushing, the expiry, and CME's switch to Bachelier on 22 April.
8. The Treasury cash–futures basis trade: the mechanics, its leverage, its role in March 2020, and its size since
   *(verify: latest Fed and OFR estimates)*.
9. Inflation: TIPS breakevens, the inflation risk premium.

*Computed:* CIP deviations from public rates and FX (FRED, Fed H.10); a carry portfolio and its skew; WTI futures
curves and roll yield from EIA data; TIPS breakevens.
*Visuals:* the CIP triangle (borrow, convert, lend, convert back) with the leak widening after 2008; the futures
curve flipping from backwardation to contango.
*Crisis:* the Swiss franc, 15 January 2015; the yen carry unwind, August 2024; LME nickel, March 2022 (trades
cancelled).

### Act III · Return Premia (P)

### Part 16 · Risk and Return (~55)
1. Markowitz (1952): mean–variance, the frontier derived by Lagrange; two-fund separation (Tobin 1958).
2. CAPM (Sharpe 1964, Lintner, Mossin): derived; the security market line; Roll's critique (1977).
3. The SDF view: p = E[mx]; Hansen–Jagannathan bounds (1991) computed from the market's Sharpe ratio.
4. APT (Ross 1976): factors from no-arbitrage.
5. ICAPM (Merton 1973): hedging demands and state variables.
6. Consumption: Lucas (1978), CCAPM; GMM (Hansen 1982).
7. The equity premium puzzle (Mehra–Prescott 1985), with US numbers computed; the risk-free rate puzzle.
8. Answers: habit (Campbell–Cochrane 1999), long-run risk (Bansal–Yaron 2004), rare disasters (Rietz 1988; Barro
   2006).
9. Excess volatility (Shiller 1981) and the Campbell–Shiller decomposition: is it cash flows or discount rates?
10. Intermediary asset pricing (He–Krishnamurthy 2013; Adrian–Etula–Muir 2014; He–Kelly–Manela 2017): the
    marginal investor is a dealer.
11. Demand systems and inelastic markets (Koijen–Yogo 2019; Gabaix–Koijen 2021): a dollar of flow moves prices
    by about five dollars. A current frontier of asset pricing.

*Computed:* frontiers from factor data; HJ bounds; the equity premium puzzle's implied risk aversion; the
Campbell–Shiller decomposition on Shiller's data.
*Visuals:* the frontier as a bullet with the tangency line swinging as the risk-free rate moves; the HJ cone with
models as points outside and inside.

### Part 17 · Factors (~55)
1. Testing: time-series regressions and GRS (1989); cross-sectional Fama–MacBeth (1973); errors-in-variables.
2. Size (Banz 1981) and value (Basu 1977; Fama–French 1992); the three-factor model (1993).
3. Momentum (Jegadeesh–Titman 1993; Carhart 1997); time-series momentum (Moskowitz–Ooi–Pedersen 2012).
4. Momentum crashes (Daniel–Moskowitz 2016): the 2009 rebound, computed.
5. Profitability and investment: Novy-Marx (2013), the five-factor model (2015), the q-factor model (Hou–Xue–Zhang
   2015).
6. Low risk: betting against beta (Frazzini–Pedersen 2014), low volatility; leverage constraints as the reason.
7. Value and momentum everywhere (Asness–Moskowitz–Pedersen 2013): across asset classes, and their negative
   correlation.
8. Carry everywhere (Koijen–Moskowitz–Pedersen–Vrugt 2018); quality (Asness–Frazzini–Pedersen 2019).
9. Value's lost decade (2010–2020): intangibles, rates, and spreads, measured.
10. Risk or mispricing? Behavioural accounts, limits to arbitrage (Shleifer–Vishny 1997).
11. Factor timing and factor momentum.
12. The Track Record opens for the classic factors.

*Computed:* Fama–MacBeth and GRS on Ken French portfolios; each factor's history and drawdowns; momentum's crash
anatomy; value's spread; the classic factors registered and opened.
*Visuals:* the cross-section as a cloud of portfolios with the SML fitted through it; momentum's equity curve with
2009 lit.
*Crisis:* the momentum crash of March–May 2009.

### Part 18 · The Factor Zoo (~55)
1. Hundreds of factors: the zoo (Cochrane 2011; Harvey–Liu–Zhu 2016), and why t > 3.
2. Multiple testing: Bonferroni, Holm, Benjamini–Hochberg; FDR in finance.
3. Replication: "Replicating anomalies" (Hou–Xue–Zhang 2020) vs "Is there a replication crisis in finance?"
   (Jensen–Kelly–Pedersen 2023), and why they disagree.
4. Open Source Asset Pricing (Chen–Zimmermann 2022): the data the series uses.
5. Post-publication decay (McLean–Pontiff 2016), measured on the Chen–Zimmermann portfolios.
6. Data-mined vs peer-reviewed (Chen–Lopez-Lira–Zimmermann 2024): does theory help?
7. Shrinking the cross-section (Kozak–Nagel–Santosh 2020): the SDF by ridge and elastic net in PC space.
8. Taming the factor zoo (Feng–Giglio–Xiu 2020): double-selection lasso.
9. Weak factors and test assets (Giglio–Xiu 2021; Giglio–Xiu–Zhang 2023); three-pass regression.
10. Latent factors: PCA, RP-PCA (Lettau–Pelger 2020), IPCA (Kelly–Pruitt–Su 2019).
11. Bayesian model comparison of factor models (Barillas–Shanken 2018).
12. The shrinkage SDF registered and opened.

*Computed:* the t-statistic distribution of 200+ predictors against the null; FDR-controlled discoveries;
pre- vs post-publication returns; the KNS SDF's out-of-sample R² vs shrinkage; IPCA on characteristic portfolios.
*Visuals:* a histogram of t-statistics with the hurdle sliding from 2 to 3; the shrinkage path of SDF weights.

### Part 19 · Backtesting Without Fooling Yourself (~50)
1. The biases: look-ahead, survivorship, selection, point-in-time data; each demonstrated with a planted error.
2. The Sharpe ratio's standard error (Lo 2002), with autocorrelation and non-normality corrections.
3. Minimum backtest length (Bailey–López de Prado).
4. The trial counter so far, and the expected maximum Sharpe of N trials of noise, derived from extreme-value
   theory.
5. The deflated Sharpe ratio (Bailey–López de Prado 2014).
6. Probability of backtest overfitting by combinatorially symmetric CV (Bailey–Borwein–López de Prado–Zhu).
7. Purged and embargoed cross-validation; walk-forward.
8. Data-snooping tests: White's reality check (2000), Hansen's SPA (2005), Romano–Wolf stepdown.
9. "The technical rules that weren't" (Sullivan–Timmermann–White 1999), re-run.
10. Monitoring live strategies with e-values: when to stop believing (callback to Part 2).
11. Synthetic-data tests: planting alpha in a `simulated` market and counting how often each method finds it.

*Computed:* a grid of 10,000 random technical rules on pre-2021 data, their best Sharpe, and its deflation; PBO on
that grid; purged vs naive CV on a planted-leak example; the series' trial counter so far.
*Visuals:* `TrialCounter` with the hurdle rising as trials accumulate; the best-of-N Sharpe distribution sliding
right.
*Crisis:* not a market event but a research one: published strategies that died out of sample (cited).

### Part 20 · Machine Learning for Returns (~60; a frontier part)
1. Why finance is different: low signal-to-noise (monthly R² ≈ 0.4%), non-stationarity, competition; "Can
   machines learn finance?" (Israel–Kelly–Moskowitz 2020).
2. Gu–Kelly–Xiu (2020): penalized regression, trees, boosting and networks on stock characteristics, and the
   finding that nonlinear interactions matter.
3. Economic restrictions (Avramov–Cheng–Metzker 2023): where ML gains come from (microcaps, distress) and whether
   they survive costs.
4. The virtue of complexity (Kelly–Malamud–Zhou 2024): random-feature market timing on Welch–Goyal predictors;
   double descent in return prediction (callback to AI Part 8), replicated.
5. The critics: what the complex timer actually learns *(verify: Nagel 2025, "Seemingly virtuous complexity";
   Buncic 2025)*, re-run on the same data.
6. Autoencoder asset pricing (Gu–Kelly–Xiu 2021); conditional factor models.
7. Deep SDFs with adversarial moments (Chen–Pelger–Zhu 2024).
8. Transformers across assets: AI asset pricing models *(verify: Kelly–Kuznetsov–Malamud–Xu 2025)*; attention
   as cross-sectional information sharing.
9. Images of prices: CNNs on charts (Jiang–Kelly–Xiu 2023).
10. Time-series foundation models (Chronos, TimesFM, Moirai) and finance-specific ones *(verify: Kronos 2025)*:
    zero-shot forecasts tested honestly.
11. Uncertainty: conformal prediction for returns and risk.
12. The ML strategies registered and opened.

*Computed:* the Welch–Goyal random-features experiment (the complexity curve and its critique); gradient boosting
and a network on Chen–Zimmermann characteristic portfolios and on a crypto cross-section; a small cross-asset
transformer (reusing AI Part 13's code); a foundation-model zero-shot test; each registered on the Track Record.
*Visuals:* the out-of-sample R² vs complexity curve with its interpolation peak; SHAP-style interaction maps; the
attention matrix across assets.

### Part 21 · Text, LLMs and Alternative Data (~55; a frontier part)
1. History: Tetlock (2007), Antweiler–Frank; the Loughran–McDonald dictionary (2011) and why general sentiment
   words fail in 10-Ks.
2. Supervised text models: SESTM (Ke–Kelly–Xiu 2019); embeddings and FinBERT.
3. Text as macro data: business news and the business cycle (Bybee–Kelly–Manela–Xiu 2024); FOMC communication
   (Hansen–McMahon–Prat 2018).
4. LLMs read the news: "Can ChatGPT forecast stock price movements?" (Lopez-Lira–Tang 2023); LLM embeddings and
   expected returns (Jiang–Kelly–Xiu 2022); financial statement analysis by LLM (Kim–Muhn–Nikolaev 2024).
5. Look-ahead bias: a model trained on the future knows the future (Glasserman–Lin 2023; Sarkar–Vafa 2024);
   chronologically consistent models *(verify: He–Lv–Manela–Wu 2025)*.
6. A time-sliced experiment: small models trained on text up to year t only, against a model that has seen
   later text, compared on the same task.
7. LLM agents that trade (TradingAgents 2024 and successors *(verify)*): what their backtests do and do not show.
8. Alternative data: satellites, card panels, web traffic, job postings; how its value decays as it spreads.
9. Domain models: BloombergGPT (2023) vs general models; what scale bought.
10. The LLM signal registered and opened.

*Computed:* hawkishness scores of every FOMC statement (dictionary, small supervised model, an open-weight LLM run
locally) against 2-year Treasury moves on announcement days (FRED); the time-sliced look-ahead experiment on FOMC
and EDGAR text with the series' pocket language models (`explainer.lm`); 8-K event study where free data allows.
*Visuals:* FOMC sentences lighting up word by word; the look-ahead gap opening between the time-sliced and the
"future-aware" model.

### Act IV · Portfolios and Strategies

### Part 22 · Portfolio Construction (~55)
1. Mean–variance as an error maximizer (Michaud 1989); the sensitivity of weights to means.
2. 1/N beats them all? (DeMiguel–Garlappi–Uppal 2009), re-run.
3. Covariance estimation: sample covariance in high dimension; Marchenko–Pastur; RMT cleaning (Laloux et al.
   1999; Bun–Bouchaud–Potters 2017).
4. Shrinkage: Ledoit–Wolf linear (2004) and nonlinear (2017, 2020).
5. Constraints as shrinkage (Jagannathan–Ma 2003).
6. Black–Litterman (1992): views as Bayesian updates of equilibrium.
7. Risk parity and equal risk contribution (Maillard–Roncalli–Teïletche 2010); leverage.
8. Hierarchical risk parity (López de Prado 2016), and what it trades away.
9. Robust optimization; CVaR optimization (Rockafellar–Uryasev 2000) as a linear program.
10. Growth: Kelly portfolios, Cover's universal portfolio (1991), stochastic portfolio theory (Fernholz 2002).
11. End-to-end: learning portfolios directly from the decision loss.
12. Minimum-variance and HRP registered and opened.

*Computed:* frontiers with estimation-error clouds; MP vs empirical eigenvalues of 100 portfolios; LW vs sample vs
RMT out-of-sample variance; risk parity and HRP backtests.
*Visuals:* `FrontierPlot` with the "true" and estimated frontiers diverging; the eigenvalue histogram against the
MP law with the market mode far outside.

### Part 23 · Trading Through Time (~55)
1. The fundamental law of active management (Grinold 1989): IR = IC·√breadth, derived and its limits.
2. Risk models: industry and style factors (Barra-style), estimated and tested.
3. Transaction costs: spread, impact, fees; real-trade estimates (Frazzini–Israel–Moskowitz 2018); anomalies net
   of costs (Novy-Marx–Velikov 2016).
4. Dynamic trading with predictable returns and costs (Gârleanu–Pedersen 2013): trade partially toward an aim
   portfolio, derived.
5. Multi-period optimization by convex programming (Boyd et al. 2017).
6. Alpha combination: from many weak signals to one forecast; shrinkage and the "mega-alpha"; formulaic alphas
   (Kakushadze 2016).
7. Signal decay, turnover and capacity; fund size and performance (Berk–Green 2004).
8. Crowding: comomentum (Lou–Polk), common holdings, and the quant quake.
9. How a quant firm is organized (public record): research platforms, data, the pod model of multi-manager funds,
   risk limits and stop-outs, compute.
10. Attribution: what made the money, after the fact.

*Computed:* a Barra-style risk model on characteristic portfolios; the Gârleanu–Pedersen trader vs a myopic
trader net of costs; capacity curves; alpha combination by ridge vs equal weights.
*Visuals:* the aim portfolio as a moving target with the trader's path chasing it; the capacity curve bending
down.
*Crisis:* August 2007, the quant quake (Khandani–Lo 2007/2011), reconstructed with their contrarian strategy.

### Part 24 · Statistical Arbitrage (~50)
1. History: the Morgan Stanley group in the 1980s, pairs trading, D. E. Shaw.
2. Pairs trading (Gatev–Goetzmann–Rouwenhorst 2006), re-run.
3. Cointegration-based pairs (Part 4); the half-life of mean reversion.
4. Trading an OU process: optimal entry and exit thresholds (Bertram 2010; Leung–Li 2015), derived.
5. Factor-residual stat arb: PCA and ETF residuals (Avellaneda–Lee 2010); the s-score.
6. Kalman-filter hedge ratios.
7. Reversal and lead–lag (Lo–MacKinlay 1990).
8. Deep statistical arbitrage (Guijarro-Ordonez–Pelger–Zanotti 2022): learned residual portfolios and
   trading policies.
9. Crowding and the decline of simple stat arb; costs at high turnover.
10. The PCA-residual book registered and opened.

*Computed:* pairs and PCA-residual strategies on sector ETFs and on crypto perpetuals (Binance); OU threshold
optimization vs simulation; a small CNN-plus-transformer residual policy (Guijarro-Ordonez et al.'s architecture,
scaled down).
*Visuals:* a spread oscillating in its OU band with entries and exits lit; residual portfolios as eigen-portfolios
draining away.
*Crisis:* August 2007, seen from the stat-arb book: crowding and deleveraging.

### Act V · Market Microstructure

### Part 25 · Who Trades With Whom (~55)
1. Why markets need intermediaries: Garman (1976), inventory models (Ho–Stoll 1981).
2. Adverse selection: Glosten–Milgrom (1985), the spread derived from Bayes.
3. Kyle (1985): the informed trader, noise traders and the market maker; λ derived; information enters prices
   gradually.
4. Roll's spread estimator (1984) and Amihud's illiquidity (2002), computed.
5. Toxicity: PIN (Easley et al. 1996), VPIN (2012) and its critique (Andersen–Bondarenko 2014).
6. Price discovery and information shares (Hasbrouck 1995).
7. Market structure: exchanges, Reg NMS (2005), the NBBO, maker–taker fees, dark pools, payment for order flow,
   the US equity market rules of 2024 (tick sizes and access fees), T+1 (May 2024).
8. HFT as market maker (Menkveld 2013; Brogaard–Hendershott–Riordan 2014).
9. The flash crash, 6 May 2010 (Kirilenko et al. 2017); the Treasury flash rally, 15 October 2014.
10. Frequent batch auctions (Budish–Cramton–Shim 2015): a proposal and its debate.

*Computed:* Kyle and Glosten–Milgrom simulated and matched to theory; Roll and Amihud measures on the ITCH day
(through `trading`'s compute) and on Binance; VPIN on the same data.
*Visuals:* the Kyle equilibrium as price converging to value over the trading day; the Glosten–Milgrom spread
narrowing as the market maker learns.
*Crisis:* 6 May 2010.

### Part 26 · The Limit Order Book (~55; a frontier part)
1. The book as a queueing system (Cont–Stoikov–Talreja 2010): probabilities of a price move from queue sizes.
2. The queue-reactive model (Huang–Lehalle–Rosenbaum 2015).
3. Hawkes processes (Hawkes 1971; Bacry–Mastromatteo–Muzy 2015): self-excitation, the branching ratio, estimated
   on real trades; near-criticality (callback to Part 10).
4. Order flow's long memory (Lillo–Farmer 2004) and how prices stay unpredictable anyway.
5. Order-flow imbalance (Cont–Kukanov–Stoikov 2014), measured; multi-level and deep OFI (Kolm–Turiel–Westray 2023).
6. The microprice (Stoikov 2018), derived and tested.
7. Deep LOB models: DeepLOB (Zhang–Zohren–Roberts 2019), universal features of price formation (Sirignano–Cont
   2019).
8. The reality check: benchmarks show fragile generalization (LOBCAST, Prata et al. 2024).
9. Generative order books: token-level generative models of message streams (Nagy et al. 2023), benchmarks
   *(verify: LOB-Bench 2025)*.
10. A small generative order book trained here, and how its simulated book compares to the real one.

*Computed:* queue-depletion probabilities vs Cont–Stoikov–Talreja; Hawkes fits on ITCH and Binance trades; OFI and
microprice regressions; a DeepLOB-style model with honest out-of-sample tests; a small generative LOB model
(resumable) and its stylized-fact scorecard.
*Visuals:* `OrderBookLadder` live with Hawkes intensity glowing as events cluster; the microprice between bid and
ask as the queues change.

### Part 27 · Market Impact and Execution (~55)
1. Why large orders move prices; metaorders; what the public can and cannot measure.
2. The square-root law (Tóth et al. 2011; Almgren et al. 2005), its universality across assets *(verify: recent
   complete-market surveys)*, and the latent-order-book explanation (Donier et al. 2015).
3. Market microstructure invariance (Kyle–Obizhaeva 2016).
4. The propagator model (Bouchaud et al. 2004): transient impact and the efficiency of prices despite long-memory
   order flow.
5. No dynamic arbitrage (Gatheral 2010): which impact models are consistent.
6. Optimal execution: Bertsimas–Lo (1998), Almgren–Chriss (2000) derived, and the efficient frontier of execution.
7. Transient impact and the order-book shape (Obizhaeva–Wang 2013).
8. Execution with signals and many agents (Cartea–Jaimungal; mean-field games, callback to Part 5).
9. RL for execution (Nevmyvaka–Feng–Kearns 2006 and successors), with a fair benchmark.
10. Transaction cost analysis: implementation shortfall, VWAP, arrival price, and how desks measure slippage.

*Computed:* propagator fits on ITCH trade signs; Almgren–Chriss frontiers; an execution simulation in a
`simulated` latent-order-book market where the square-root law emerges, compared with published estimates; an RL
executor vs Almgren–Chriss.
*Visuals:* `ImpactTrace` with the square root rising and the propagator decaying after the metaorder ends; the
Almgren–Chriss trajectories bending as risk aversion grows.

### Part 28 · Market Making and the Speed Race (~50)
1. The market maker's problem: inventory and adverse selection.
2. Avellaneda–Stoikov (2008) derived by HJB: the reservation price and the optimal spread.
3. Guéant–Lehalle–Fernandez-Tapia (2013): the closed form with inventory limits.
4. Adverse selection in quotes: alpha signals, fill toxicity, mark-outs.
5. RL market making (callback to AI Part 26) vs the analytic solution.
6. Tick size, queue position, and the value of being first.
7. The speed race: latency arbitrage measured in exchange messages (Aquilina–Budish–O'Neill 2022), about 0.5 bp
   of volume.
8. The economics of HFT (Baron–Brogaard–Hagströmer–Kirilenko 2019): concentration and returns.
9. Options market making: delta, vega and the volatility surface as the quote.

*Computed:* Avellaneda–Stoikov and GLFT vs simulation; mark-out curves on the ITCH day; an RL market maker in the
Part 26 simulator; latency-race statistics where the ITCH day allows.
*Visuals:* the quote pair skewing as inventory builds; mark-out curves fanning by fill type.
*Note:* the engineering (feeds, FPGAs, kernel bypass) is in [`trading`](../../markets/trading/README.md). This
part is its mathematics.
*Crisis:* Knight Capital, 1 August 2012 (briefly; told fully in `trading`).

### Part 29 · Crypto and DeFi (~55)
1. Markets without intermediaries: blockchains, exchanges on and off chain, the 24/7 market.
2. Constant-function market makers: x·y = k derived; price impact on the curve; the AMM as an oracle
   (Angeris–Chitra 2020).
3. Impermanent loss and loss-versus-rebalancing (Milionis–Moallemi–Roughgarden–Zhang 2022): the LP is short
   gamma to arbitrageurs, derived.
4. Concentrated liquidity (Uniswap v3, 2021) as a range order; v4 hooks.
5. MEV: front-running, sandwiches and the block builder market (Daian et al. 2020, "Flash Boys 2.0").
6. Perpetual futures: the funding mechanism and its no-arbitrage price (He–Manela–Ross–von Wachter 2022;
   Ackerer–Hugonnier–Jermann *(verify: publication)*); basis and funding measured.
7. Cross-exchange arbitrage and its limits (Makarov–Schoar 2020; the kimchi premium).
8. Stablecoins: collateralized, fiat-backed, algorithmic; runs (Diamond–Dybvig 1983) on chain.
9. Crypto factor models (Liu–Tsyvinski–Wu 2022): market, size, momentum.
10. Spot ETFs (January 2024) and the institutional market.
11. The crypto carry-and-momentum book registered and opened.

*Computed:* LVR vs impermanent loss for a simulated LP against Binance prices; funding and basis histories;
cross-exchange price gaps; a crypto factor model; the Terra collapse from public on-chain and exchange data.
*Visuals:* `AMMCurve` with the arbitrageur moving the pool and LVR accumulating; the funding rate pulling the
perpetual towards spot.
*Crisis:* Terra/LUNA, May 2022; FTX, November 2022.

### Act VI · The System

### Part 30 · Measuring Risk (~55)
1. RiskMetrics (1994) and VaR; historical, parametric and Monte Carlo VaR.
2. Coherence (Artzner–Delbaen–Eber–Heath 1999): why VaR is not subadditive (a counterexample) and expected
   shortfall is.
3. Elicitability: VaR is, ES alone is not (Gneiting 2011), but jointly they are (Fissler–Ziegel 2016); what that
   means for backtesting.
4. Backtests: Kupiec (1995), Christoffersen (1998), Acerbi–Székely (2014) for ES.
5. Basel's FRTB: 97.5% ES, liquidity horizons.
6. Extreme value theory: block maxima, peaks over threshold, GPD (Balkema–de Haan–Pickands); the Hill estimator;
   conditional EVT (McNeil–Frey 2000).
7. Copulas (Sklar 1959) and tail dependence; correlation's pitfalls (Embrechts–McNeil–Straumann 2002).
8. Filtered historical simulation; stress testing and reverse stress tests.
9. Model uncertainty: VaR bounds with unknown dependence, the rearrangement algorithm (Embrechts–Puccetti–
   Rüschendorf 2013).
10. Liquidity risk: time to liquidate and liquidity-adjusted VaR.

*Computed:* VaR/ES models on 1926–2020 daily returns, backtested with exceedances shown; EVT tail fits; t vs
Gaussian copula on factor pairs; rearrangement bounds.
*Visuals:* the loss distribution with VaR as a line and ES as the shaded mass beyond it; exceedance clusters lit on
the timeline.
*Crisis:* 2008 VaR exceedances clustered, as the backtest predicts they will when volatility is ignored.

### Part 31 · Leverage, Liquidity and Crises (~60)
1. History: Minsky and Kindleberger; manias, panics, crashes.
2. Bank runs (Diamond–Dybvig 1983): the two equilibria, derived.
3. Market and funding liquidity (Brunnermeier–Pedersen 2009): margin spirals, derived and simulated.
4. Leverage cycles (Geanakoplos 2010); fire sales (Shleifer–Vishny 1992; Cont–Schaanning 2017; Greenwood–Landier–
   Thesmar 2015).
5. Networks: Eisenberg–Noe (2001) clearing vectors, computed; contagion and its phase transition
   (Acemoglu–Ozdaglar–Tahbaz-Salehi 2015).
6. Systemic risk measures: CoVaR (Adrian–Brunnermeier 2016), SRISK (Brownlees–Engle 2017).
7. LTCM, 1998: convergence trades, leverage, crowding, and the Fed-brokered rescue.
8. 2007–08: the run on repo (Gorton–Metrick 2012), Lehman, AIG's CDS.
9. March 2020: the dash for cash and Treasury market dysfunction (Duffie 2020; He–Nagel–Song 2022).
10. 2022–23: gilts and LDI; SVB and uninsured deposits (Jiang–Matvos–Piskorski–Seru 2024); Credit Suisse.
11. Non-bank financial intermediation and the policy response.

*Computed:* the Brunnermeier–Pedersen spiral simulated; Eisenberg–Noe on a network calibrated to public
stress-test data (EBA); SRISK from public market data; the March 2020 Treasury and dollar funding moves from FRED.
*Visuals:* `ContagionNet` with losses cascading; the margin spiral as a loop tightening.
*Crisis:* all of them, in order.

### Part 32 · Machines in the Market (~55; a frontier part)
1. History: the Santa Fe artificial stock market (Arthur et al. 1997); Lux–Marchesi (1999); agent-based models.
2. Market simulators: ABIDES (Byrd–Hybinette–Balch 2020), the generative book of Part 26; the simulation-to-real
   gap.
3. Reinforcement learning in markets: what has been tried (hedging, execution, market making, allocation) and the
   offline-RL problem: a backtest is not an environment.
4. LLM agents as traders and analysts, in simulated markets.
5. Algorithmic collusion: Q-learning pricing agents learn to collude (Calvano et al. 2020); AI traders in
   securities markets (Colliard–Foucault–Lovo 2022; Dou–Goldstein–Ji *(verify: latest version)*), reproduced in
   our simulator.
6. Herding and homogeneity: when everyone uses the same model (Gensler–Bailey 2020).
7. AI and financial stability: IMF GFSR (October 2024), FSB (2024); regulation's path *(verify: current status
   of US rules on predictive analytics)*.
8. Moore's law vs Murphy's law (Kirilenko–Lo 2013): automation, speed and fragility.

*Computed:* a multi-agent simulated market with Q-learning market makers, where we measure collusion in spreads;
LLM-agent episodes in the simulator; herding when agents share a model.
*Visuals:* agents' spreads converging above the competitive level as they learn; the market's response to a shock
with diverse vs identical agents.

### Finale

### Part 33 · Can You Beat the Market? (~55)
1. The arithmetic of active management (Sharpe 1991; Pedersen 2018).
2. Luck vs skill: Fama–French (2010), false discoveries among funds (Barras–Scaillet–Wermers 2010), skill measured
   in dollars (Berk–van Binsbergen 2015).
3. Adaptive markets (Lo 2004): efficiency as an ecology.
4. The Track Record, all rows, on the sealed window.
5. The trial counter, final, and the deflated Sharpe ratios. Narration follows the numbers: what survived,
   what did not, and why.
6. What the series built: Q (the Surface's final scoreboard) and P (the Track Record).
7. Open problems: the equity premium; roughness; the factor zoo's true dimension; ML at low signal-to-noise; LLM
   look-ahead; AI traders and stability; climate risk pricing; the plumbing of the Treasury market.
8. Back to Bachelier: 22 April 2020, and the fair game.

*Computed:* the Track Record compiled and deflated; the final Surface scoreboard.
*Visuals:* the series map lit end to end; the sealed envelope opened; the timeline from 1900 to now.

## 4. Data

All sources below are free. Licences and redistribution terms are checked in Phase 0. Where redistribution is
allowed, a frozen snapshot is committed under `videos/quant/data/` (small files) or downloaded by a fetch module
and checked against a committed SHA-256. Where it is not allowed, only the fetch module and the checksum are
committed. The freeze date is set once in Phase 0.

| Source | What | Parts |
|---|---|---|
| Kenneth French data library | daily and monthly factors (1926–), sorted portfolios, industries | 1, 4, 16–19, 22, 23, 30 |
| Open Source Asset Pricing (Chen–Zimmermann) | 200+ predictor portfolio returns, signal documentation | 18–20, 22, 23 |
| JKP global factor data (Jensen–Kelly–Pedersen) | 153 factors × 93 countries | 17, 18 |
| Amit Goyal's data (Welch–Goyal) | the monthly equity-premium predictors | 20 |
| Robert Shiller's data | prices, dividends, earnings, CAPE since 1871 | 16 |
| FRED | Treasury yields, VIX, FX, spreads, SOFR, breakevens | 8, 13, 15, 21, 31 |
| US Treasury; Fed (GSW curve, H.10, H.15); NY Fed (ACM term premia, SOFR) | curves, rates, FX | 13, 15 |
| EIA | WTI spot and futures | 15 |
| Deribit public API | BTC/ETH options surface with IVs, DVOL history | 1, 6–10, 12 (the Surface) |
| Binance public data (data.binance.vision) | trades, klines, book depth, perpetual funding | 1, 4, 7, 10, 24–26, 29 |
| Nasdaq TotalView-ITCH sample day | every message, one day (via `trading`) | 25–28 |
| SEC EDGAR; Fed FOMC statements and minutes | text | 21 |
| Public filings (call reports, 10-Ks, EBA stress-test data) | balance sheets | 13, 14, 31 |

**What the series cannot get for free, and what it does instead:**
- CRSP stock-level returns: characteristic-sorted portfolios (Chen–Zimmermann, JKP) instead, and the crypto
  cross-section where stock-level data is needed.
- SPX options (OptionMetrics, Cboe): the Deribit surface, with SPX facts cited from papers.
- TAQ and metaorder data: the ITCH day, Binance, published estimates, and `simulated` markets.
- Survivorship bias in free equity prices is shown and not hidden (Part 19).

## 5. Phases

0. **Infrastructure:**
   - `explainer/quant/`: `ACTS`, `PARTS`, the 1900–2030 timeline with idea and crisis entries, `series_map`, the
     Surface, the Track Record, the trial counter, `crisis_card`, and the instruments in Section 1. *AI, Built*'s
     lecture cards and visual helpers are re-exported.
   - Data: the licence check, fetch modules, checksums, and the freeze date. The Surface is frozen first.
   - Colours in `explainer/style.py` (`C.P`, `C.Q`, payoff, hedge, impact, crisis red, ...).
   - Tooling: `quant` added to `make.py`'s bilingual series and to `qa_series.py`, `qa_report.py`, `qa_audio.py`
     and `package_uploads.py`, which currently assume `ai`; `quant_text_zh.json` and `QUANT_ZH_GUIDE.md`;
     `quant_upload.json`.
   - README, CLAUDE.md and the series map.
1. **Pilot: Part 7 (Black–Scholes–Merton).** It exercises the derivation ladder, `HedgeLedger`, `PathFan`, the
   first row of the Surface, a crisis file (1987) and real data (Deribit and Binance). Classic treatments exist to
   measure it against. Delivered in English and Chinese, with previews and contact sheets. **Review with the
   user**, then lock the standard.
2. **Roll-out, Parts 1 → 33**, Act by Act. Part 1 comes first after the pilot, because it freezes the data and
   introduces the devices. Each part goes through:
   - the frontier sweep (resolving every *(verify)*);
   - locking the chapter list;
   - `compute.py` (registering Track Record rows and declaring trials);
   - English scenes, then QA gates;
   - Chinese narration and text, then QA gates;
   - commit and push.
3. **Finale.** Part 33 is written last, when every row and every trial is in.

Scale: about 28 hours of video, about 140–160k narration words per language, and roughly 4–6k lines of scene code
per part. Expect one part per one or two long sessions.

## 6. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| — | plan of record, draft 1 | — |
