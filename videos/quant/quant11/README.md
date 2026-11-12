

# Quant, Built — Part 11: Trading Options

Part 11 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the practitioner's part of Act III: a hook, eighteen chapters and an outro, about 65
minutes. Every number is computed by the series' own code ([`compute.py`](compute.py); the House's
[`quoting`](../../../explainer/quant/house/quoting.py), [`hedge`](../../../explainer/quant/house/hedge.py),
[`sim`](../../../explainer/quant/house/sim.py) and [`trees`](../../../explainer/quant/house/trees.py), tested in
`tests/test_quant_house.py`) from Deribit's trades and DVOL, Binance's hourly BTCUSDT, Part 12's weekly Deribit smiles,
Cboe's COR3M, FRED's VIX, Kenneth French's market and industries, and published regulatory and court records. Toy
models are labelled as illustrations on screen.

*An education in methods, not investment advice. The option-strategy results are historical and on one market. The
SEBI matter is described as alleged, from the regulator's interim order and statements and the firm's public
statements; the reviewed record through 7 November 2026 contains no final merits finding.*

## Chapters (about 65 minutes)

* **Gamma against theta (hook).** The desk question (a hedged straddle in a quiet week). May 2021 run live: a 30-day ATM
  BTC straddle bought at DVOL's 74%, hedged hourly, realized 127%, earned +1.7 on a premium of 16.9, the ledger's gamma
  bar stalling once the crash carried spot away. How we got here: 1973, 1985, 1987, 2018–2020, 2021, 2024.
* **1. Positions as Greeks, and the P&L explain.** The straddle's value surface in 3D: the gamma bowl against ten days of
  theta, balancing at σ√dt. Derivation: Taylor in (S, t, σ); Δ, Γ, 𝒱 in closed form; Θ = −½σ²S²Γ; the breakeven move
  (2.6% a day at 50% vol); 𝒱 = στS²Γ. Lab: `book_greeks` on a five-contract, four-position book (cash delta 61,224; gamma 21.5 per 1%; vega
  154 per point; theta −112 a day). The real explain from 10 to 11 December 2025: forward input −2.8%, ATM vol 43.7 → 41.7%;
  delta −1,839, gamma +178, theta −86, vega −27, vanna +74, volga −10; actual −1,679, unexplained +30 (1.8%).
* **2. Gamma scalping on a real path.** The hedge trading live on the May 2021 path; the dollar-gamma landscape in 3D
  with the path on it; 2,000 reshuffles of the same 720 hourly returns (identical realized variance): mean +7.8, 90%
  range [3.0, 14.2]; the real +1.7 beat only 0.4% of them; the crash moved to day 2 earns +2.1. Derivation: the summed
  identity, the path-dependent weight (El Karoui–Jeanblanc–Shreve), Carr–Madan's log contract. Lab: `delta_hedge`.
* **3. How often to hedge.** Three hedgers raced on one month; 244 thirty-day straddles at DVOL, 2021–2025: mean
  P&L hourly −2.86 (sd 3.51), 4-hourly −2.69 (3.81), daily −2.59 (4.27), on 2% moves −2.88 (3.75); hourly minus daily
  −0.27, t = −1.6 (mean difference unresolved; sample correlation with RV − IV 0.82 → 0.88). With
  10 bp costs: hourly −4.30, daily −3.07. BTC variance ratio 0.978. Derivation: √Δt error, the variance ratio,
  move-triggered hedging (Zakamouline).
* **4. Vega, vanna, volga.** The vega surface 𝒱(K, σ) in 3D with the 25Δ flags. Derivation of vanna and volga; d₁d₂ at
  the money and at 25Δ; RR and BF as mixed-exposure quote coordinates. Vanna–volga (Castagna–Mercurio) on the Surface: RR −5.6,
  BF +1.75 vol points; the rebuilt smile with RMSE 0.19 points against SSVI between the 10Δ strikes, off by up to 12 in the far
  wings. 100 weekly 30-day RR/BF, 2024–2025: RR negative in only 28% of weeks (BTC's call skew in rallies); BF averaged
  +1.6.
* **5. Strategies.** One 3D P&L surface over (spot move, vol move) morphing through straddle, strangle, risk reversal,
  butterfly, call spread and calendar, sinking with time. The bets table. 96 four-week trades of each on real smiles
  (2024–2025): straddle mean −0.65 / median −3.18 / wins 34%; strangle −0.50 / −2.83 / 23%; risk reversal +2.37 /
  −0.37 / 27%; butterfly +0.15 / −1.42 / 44%; call spread +0.87 / −1.79 / 46%; calendar +0.09 / −0.17 / 44%; no NW t
  above 1.6.
* **6. The volatility premium in option returns.** 96 hedged straddles at the market's own 28-day ATM implied as
  ledgers filling: mean −1.22 per 100, positive in 26% of weeks, NW t = −3.6. Coval–Shumway (2001: about −3% a week)
  and Bakshi–Kapadia (2003). Unhedged on BTC: −4% of premium on average (t −0.2), median −29%. Derivation: P-mean
  versus the Q-martingale; the premium as the gap.
* **7. Forecast diagnostics, and how much to bet.** DVOL vs HAR vs realized, traced; the cached retrospective diagnostic (1.75 vs 0.57,
  ordinary t ≈ 2.4; entry-day variance includes later hours). Goyal–Saretto (2009). Kelly on Part 10's 1,706 monthly P&Ls: mean/variance heuristic = 46, the sample ruin wall 1/|x_min| = 30,
  the empirical optimum against the wall at 29.8; half of it keeps most of the growth.
* **8. Making a market: the spread.** The die game; Glosten–Milgrom running (the fixed 24-trade sample ends with belief 0.5, bid 0.35 and ask 0.65);
  derivation of ask − bid = μ(V_H − V_L) and the edge/markout split. 524,281 Deribit BTC option trades on 100
  Wednesdays: maker edge against the mark +0.36 vol points (median 0.17); delta-hedged markouts +0.26 / +0.22 / +0.21
  after 5 / 30 / 60 minutes (59% kept after an hour); the largest 5% pay 0.46 and keep 0.17. Lab: `markouts`.
* **9. Inventory, and a market maker that learns.** The toy book (max inventory 64 → 9). Derivation: fills Ae^{−kδ},
  the HJB, the first-order condition, GLFT; Stoikov–Sağlam, Baldacci–Bergault–Guéant, Gârleanu–Pedersen–Poteshman. Lab:
  `quote`. Replay: tabular Q-learning, 5 seeds × 800,000 clients, against the exact DP (value 15.5): 79–92% of the
  optimum; GLFT snapped to the grid 99%; the best symmetric quote −1.0. Live: learned +151 against symmetric −62 on
  the same 2,000 clients.
* **10. Hedging the book.** Greek space: a short straddle carried back to the origin by 0.55 of a 7-day and 1.23 of a
  60-day option, then shares. Derivation: the 2×2 system, 𝒱/Γ = στS². Simulated (10,000 paths): GBM sd 0.91 → 0.13 with
  the gamma hedge; Heston 2.14 → 1.39 → 0.54 with gamma and then vega. Vega buckets under a steepening (Taleb). The
  Whalley–Wilmott band (lab `ww_band`); the deep hedger replayed (3 cost weights, with 3 replay seeds only at κ = 1) on the cost–risk chart
  (Part 17 goes further).
* **11. Expiry and pin risk.** The gamma spike in 3D (0.15 a day and 5.8 a minute before expiry); delta as a
  step; pin risk. Avellaneda–Lipkin derived and simulated: ending within 0.5 of the strike 10% with no hedgers, 33%
  net long, 0.35% net short. Ni–Pearson–Poteshman; Golez–Jackwerth. BTC at Deribit's Friday 08:00 expiries,
  2021–2025: within $100 of a $1,000 strike 24.5% (n = 261, z = 1.9) against 19.9% at all hours; Friday 07:00 control
  19.2%: suggestive, not conclusive.
* **12. Early exercise, synthetics and the dividend play.** Merton's no-early-exercise; the dividend condition derived;
  the House's tree with the exercise region (only the step before the dividend): American 4.55 against European 4.19.
  Conversions and reversals. The dividend play as an assignment lottery (Pool–Stoll–Whaley 2008; Hao–Kalay–Mayhew 2010).
* **13. Dispersion and implied correlation.** A correlation matrix heating; σ_I(ρ, σ̄) in 3D sliced at the index vol;
  derivation (large-N ρ ≈ σ_I²/σ̄²); lab `implied_correlation` (50-member value 0.43, large-N approximation 0.44 for 20% against 30%). Cboe COR3M 2006–2025: mean
  42.0, peak 90.8 (8 December 2011), 90.3 in March 2020, record lows 7.6 (July 2024) and 11.1 (January 2025);
  Driessen–Maenhout–Vilkov. The trade simulated: P&L against ρ_impl − ρ_real, correlation 0.92, right sign in 95%.
* **14. India's expiry-day boom, and what lottery tickets pay.** SEBI's studies (91% lost; ₹1.8 lakh crore over three
  years; ₹1.06 lakh crore in FY25) and the October 2024 measures. Deribit tickets: 85,103 eligible taker-buy OTM trade records
  expiring within two days returned −19% premium-weighted; 84% expired worthless, 12% paid more than they cost. The
  short-dated ratio C(σ_r)/C(σ_i) derived (Mills' ratio), exact against approximate.
* **15. Case file: SEBI and Jane Street (alleged).** The interim order (3 July 2025; ₹4,843.57 crore impounded as alleged
  unlawful gains; four entities); the record: Jane Street v. Millennium (S.D.N.Y., April 2024, settled December
  2024), the escrow deposit and SEBI's 21 July statement, the SAT appeal (September 2025), the tribunal reserving its
  order on the document dispute (October 2026, as reported by LiveLaw). The toy and its 3D generalization (net > 0 iff
  D > Q/2), and SEBI's intraday position limits (circular of 1 September 2025).
* **16. Crisis file: when short volatility blows up.** Two illustrative short-put books with near (17.5% OTM) and deep
  (40% OTM) hedges, 2017–2020, VIX plus a fixed skew: before 2020 +10.1 and +10.6 per 100; March 2020 drawdowns −26.6
  and −36.3. LJM (SEC 2021-89) and Allianz Global Investors U.S. Structured Alpha (guilty plea, May 2022; SEC 2022-84).
* **17. Industry.** OCC options-and-futures clearing volumes (4.98 bn contracts in 2019 to 15.3 bn in 2025); retail options and the wholesalers
  (Bryzgalova–Pavlova–Sikorskaya 2023), Muravyev–Pearson (2020); SIG, Optiver, IMC, Jane Street; CFTC v. Optiver
  (2008/2012); the desk's loop; venue rules.
* **18. Frontier.** A logged historical walk-forward ridge and boosted-tree predictor of the hedged straddle's P&L from four
  features (66 out-of-sample weeks): correlations with the outcome about zero; both learn only "sell", earning what
  always selling earns (+0.86 a week, t 2.6) against +0.32 for chapter 7's single signal. Bali–Beckmeyer–Mörke–Weigert
  (2023), Cao et al. (2023), Baldacci–Bergault–Guéant (2021), Fang–Xu (2023).
* **For the researcher: demand-based option pricing.** A competitive mean-variance dealer who must hold −d options,
  with hedged residuals ε (payoff less discrete delta-hedge gains), prices p = E[x] + γΣ_ε d (the first-order form of
  Gârleanu, Pedersen and Poteshman 2009): own impact γVar ε_i, cross-impact γCov(ε_i, ε_j), none when Σ_ε = 0.
  Simulation: a Merton jump-diffusion (σ 45%, 4 jumps a year with log-jump mean −8% and standard deviation 10%), 30-day OTM options at strikes
  80–120, hedged daily at the total volatility 52%, 40,000 jump paths and 8,000 paths per 52% diffusion comparison: residual sd 1.1–2.0 per 100 (no jumps 0.4–0.9,
  hourly 0.08–0.19). With γ set so that one unit of 85-put demand targets one point locally (about 0.99 on repricing), it moves the
  80 put 1.1 points and the 120 call 0.19 (no jumps, daily: 0.13; hourly: 0.006); demand for every put adds 4.0 points
  at 80 and 1.0 at 120, demand for calls tilts the smile the other way (1.4 at 80, 2.4 at 120). Finite empirical exponential tilt with a fixed hedge against the first-order line, the short put's residual skewness 4.6: the marginal premium is
  9% higher at the displayed position near 0.96 units and 51% at four. Deribit taker flow on the Surface's two days, net share of traded vega: OTM
  puts within 30 days −21%, beyond +14%; OTM calls −2% and −23%; near the money about 0. Three open problems; pause:
  in dollars the 90 put rises more (1.08 of the 85's own impact, against 0.72 for the 80 put), in volatility the 80 put
  (1.1 points against 0.8), because the 80 put has less vega.
* **The quoting engine, recap, desk questions, ten problems (two at qualifying-exam level) (outro).** The House's new functions; Rule 11; the as-of-Part-11 trial
  counter (312; the chapter-7 count is 311).

## Interpretation and validation limits

The Bitcoin examples are historical model diagnostics. DVOL is an index proxy for
hypothetical dollar options, not an executable straddle or call quote. The weekly
smiles reconstruct IV from mark prices and pool records from 00:00 to 12:00 UTC,
including observations after the nominal 08:00 entry. Their reference index also
uses a window around that hour. Availability of the reconstructed inputs at entry
is not established. Pricing with a spot input, interpolated smiles and hourly
Binance hedges does not reproduce inverse-contract cash flows, executable spreads,
fees, liquidity or funding.

The chapter-7 HAR coefficients use earlier days, but its next-day input includes
the full entry calendar day's realized variance, including hours after entry; that
next-day prediction is reused as a monthly proxy. The 1.75 versus 0.57 split cannot
establish a tradable forecasting edge. Disjoint windows need not be independent.
The existing registry preserves code specifications and counts; it has no timestamp
that establishes registration before calculation. The chapter-18 four-week label
gap does not resolve quote-input timing. Its five ordinary bootstrap refits form
a descriptive range, not a confidence or prediction interval. R-squared uses the
fixed initial-sample mean; the running-error panel also shows an expanding-mean
benchmark. None of these replays is newly evaluated in this polish pass.

The gamma landscape displays ΓS²/100 with a view cap of 12; this is a scaled
illustration, distinct from the recorded path’s cumulative gamma P&L.

Greek P&L explains are finite-step approximations. The log-contract variance
replication is exact for continuous quadratic variation under its stated
continuous-hedging assumptions, with corrections for jumps and discrete sampling.
The displayed straddle shading inflates ordinary standard errors heuristically;
the reported Newey-West statistic separately uses four lags. An insignificant
frequency difference is not evidence of equivalent means. The Kelly curve is an
in-sample average over overlapping windows: its bankruptcy wall uses the worst
observed loss, not a bound on future losses. The second-order log expansion uses
E[X²]; mean/variance is only a heuristic.

The demand calculation fixes a martingale measure, zero rates and yield, and
preselected delta hedges. The dealer variable denotes shorts. Covariance impact is
a mean-variance illustration of the richer Gârleanu–Pedersen–Poteshman theory.
The exponential-tilt comparison is a finite empirical calculation on fixed hedge
residuals; it neither optimizes all hedge strategies nor certifies existence of a
population exponential moment. The displayed jump parameters are log-jump
parameters. Forty thousand jump paths are compared with eight thousand paths in
each diffusion case. Two days of filtered taker flow do not identify customer
identity, a common collar or a causal pricing effect.

The American cash-dividend tree uses an escrowed-dividend model. Exercise and
continuation tie at equality in the dividend criterion. A same-expiry put spread
bounds expiry payoff liability by its strike gap at any hedge distance; net loss
also subtracts the initial credit. That bound does not remove interim margin or
liquidity risk. Synthetic rolling hedge options marked at current Black–Scholes
volatility, even on Heston paths, are not Heston option prices or executed hedges.

The short-dated ticket calculation treats each trade record as one unit, ignoring
reported amount. Its return is weighted by quoted unit premiums, not actual traded
cash or contract volume. The return on instruments takers sold is the hypothetical
buyer's return, not the sellers' own profit; neither identifies investor performance.

The COR3M series before its July 2021 launch is backcast history. The Bitcoin
pinning check uses a thousand-dollar grid and Binance hourly closes, not the actual
listed strike set or Deribit settlement averages; its binomial z omits dependence
and baseline uncertainty. OCC contract totals include futures. Case records were
reviewed as of 7 November 2026: the Jane Street matter is described as alleged,
with the latest verified October 2026 document-dispute report attributed to the
legal press. The LJM record includes subsequent final judgments and a September
2026 Fair Fund; the Allianz seven-billion figure is lost market value, distinct
from principal losses.

## Textbook audit

| Book and section | Where |
|---|---|
| Natenberg, *Option Volatility and Pricing* (2nd ed.): contracts, forward pricing, expiration P&L | Part 2; chapter 5 (the surfaces' expiry slice) |
| Natenberg: theoretical pricing; volatility (realized, implied, forecast) | Part 10; chapters 6–7 |
| Natenberg: risk measurement (the Greeks, second order) | chapters 1, 4 |
| Natenberg: dynamic hedging | chapters 2, 3 |
| Natenberg: spreading; volatility spreads; risk considerations; bull and bear spreads | chapter 5 (and 7, sizing) |
| Natenberg: synthetics; option arbitrage (conversions, reversals, boxes) | chapter 12; Part 9 (parity, boxes) |
| Natenberg: early exercise of American options | chapter 12 |
| Natenberg: hedging strategies; position analysis | chapters 1 (explain), 10 |
| Natenberg: models and the real world; volatility revisited | chapters 6, 11, 16 |
| Natenberg: index futures and options; intermarket spreading | chapters 13, 14 |
| Natenberg: volatility contracts; skews | Part 12; chapter 4 |
| Sinclair, *Volatility Trading*: measurement and forecasting; implied dynamics and the premium | Part 7; chapters 6–7; Part 12 |
| Sinclair, *Volatility Trading*: hedging (frequency, bands); trade sizing (Kelly) | chapters 3, 10; chapter 7 (Part 8 owns Kelly) |
| Sinclair, *Positional Option Trading*: the premium, edges, structures, sizing | chapters 5–7 |
| Taleb, *Dynamic Hedging*: market making, liquidity holes | chapters 8–9, 16 |
| Taleb: delta, gamma, vega and its buckets, theta, correlation | chapters 1, 2, 4, 10, 13 |
| Taleb: pin risk, the binary at expiry | chapter 11 |
| Taleb: exotics | Part 15 |
| Bennett, *Trading Volatility*: options and volatility trading; variance swaps | chapters 2–3; Part 12 |
| Bennett: relative value and correlation (dispersion) | chapter 13 |
| Bennett: skew and term structure; volatility indices; exotics | chapter 4; Parts 12, 13, 15 |
| Hull, *Options, Futures, and Other Derivatives*: trading strategies; the Greek letters | chapters 5; 1, 10 |

## Reading (papers on screen)

Glosten–Milgrom (1985); Leland (1985); Huang–Stoll (1997); Whalley–Wilmott (1997); Carr–Madan (1998); Coval–Shumway
(2001); Bakshi–Kapadia (2003); Avellaneda–Lipkin (2003); Ni–Pearson–Poteshman (2005); Zakamouline (2006);
Castagna–Mercurio (2007); Avellaneda–Stoikov (2008); Pool–Stoll–Whaley (2008, *J. Financial Markets*);
Gârleanu–Pedersen–Poteshman (2009); Driessen–Maenhout–Vilkov (2009); Goyal–Saretto (2009); Stoikov–Sağlam (2009);
Hao–Kalay–Mayhew (2010); Golez–Jackwerth (2012); Guéant–Lehalle–Fernandez-Tapia (2013); Guéant (2017); Muravyev–Pearson
(2020); Baldacci–Bergault–Guéant (2021); Bali–Beckmeyer–Mörke–Weigert (2023); Bryzgalova–Pavlova–Sikorskaya (2023); Cao
et al. (2023); Fang–Xu (2023); Buehler et al. (2019, Part 17's). Records: SEBI studies (2024, 2025), circulars (1
October 2024, 1 September 2025), interim order (3 July 2025); SEC 2021-89, 2022-84; U.S. v. AGI US (2022); CFTC
5521-08, 6239-12; Jane Street v. Millennium (S.D.N.Y. 24-cv-2783). Full list: [READING.md](../READING.md).

## Build it

```bash
python -m videos.quant.quant11.compute                   # every number, cached in .cache/quant11/ (about 40 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant11 Hedging # one chapter, silent, with a contact sheet
python tools/make.py quant11 --cpu-voice -q m            # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Long a hedged straddle in a quiet week.** The daily P&L is ½ΓS²[(dS/S)² − σ²_imp dt] + vega·dσ_imp. With no
   moves, the first term is the full theta charge, ½ΓS²σ²_imp dt per day. If implied volatility also falls, vega
   loses too. You make money when realized variance, weighted by gamma, exceeds implied.
2. **The die.** E[X] = 3.5, so quote symmetrically around it, for example 3.3 / 3.7. Given "even", E[X | even] = 4 and
   the quote moves to about 3.8 / 4.2. The question to ask is why you are being told: information that reaches you
   through a trade moves fair value against you (adverse selection).
3. **Deep ITM American call, dividend of 2 tomorrow, rates 4%, two months left, put worth 0.3.** Exercising captures
   the dividend D = 2. Holding keeps the interest on the strike, K(1 − e^{−rτ}) = 100(1 − e^{−0.04/6}) ≈ 0.66, and the
   insurance the put provides, 0.3. Since 2 > 0.96, exercise today, before the ex-date (chapter 12). Without the
   dividend you would never exercise: sell the call, or short the stock against it (Merton 1973). A large short ATM
   option an hour before expiry is now problem 2's territory: gamma near its peak, and pin risk.

## Problems, with solutions

1. **The gamma–theta integral.** Mark the option at σ_imp and hedge its delta. By Itô,
   dV = Θdt + ΔdS + ½ΓS²σ²_r dt. By the Black–Scholes PDE at σ_imp (r = 0), Θ = −½ΓS²σ²_imp. So the hedged book earns
   ½ΓS²(σ²_r − σ²_imp)dt, and over the life ∫½ΓS²(σ²_r,t − σ²_imp)dt. The weight ΓS² is large near the strike and
   near expiry. The same realized variance therefore pays a lot if it happens there, and little far from the strike
   (May 2021).
2. **Gamma at expiry.** Γ = φ(d₁)/(Sσ√τ). At the money with τ → 0, d₁ → 0 and φ(0) = 1/√(2π), so
   Γ ≈ 1/(Sσ√(2πτ)). At S = 100 and σ = 0.5: a day (τ = 1/365) gives 0.152, and a minute (τ = 1/525,600) gives 5.78,
   √1440 ≈ 38 times larger.
3. **Implied correlation for two assets.** σ_I² = ¼σ² + ¼σ² + 2·¼ρσ² = σ²(1 + ρ)/2, so ρ = 2σ_I²/σ² − 1.
4. **The die with an informed counterparty.** Suppose the counterparty knows the roll with probability p and otherwise
   trades at random. Quote 3.5 ± s with s ≤ 0.5. Uninformed trades earn s. Informed trades lose E|X − 3.5| − s =
   1.5 − s, since |X − 3.5| takes the values 0.5, 1.5 and 2.5 equally often, and all of them trade. Breaking even
   requires (1 − p)s = p(1.5 − s), so s = 1.5p, valid while p ≤ 1/3.
5. **The band's scaling.** With a band of half-width h around delta, the mis-hedge variance per unit time scales as
   h²σ²S². The rate of trading needed to stay inside it scales as (Γσ S)²·S/h in shares times price. A hedger with
   risk aversion γ therefore minimizes γσ²S²h² + λσ²S³Γ²/h. Setting the derivative to zero gives
   h³ = λSΓ²/(2γ), so h ∝ (λSΓ²/γ)^{1/3}. Whalley and Wilmott's asymptotics give the constant 3/2 in place of 1/2.
6. **Vanna and volga.** d₁ = (ln F/K + ½σ²τ)/(σ√τ), so ∂d₁/∂σ = √τ − d₁/σ = −d₂/σ (using d₂ = d₁ − σ√τ). Then
   vanna = ∂Δ/∂σ = φ(d₁)∂d₁/∂σ = −φ(d₁)d₂/σ, and since 𝒱 = Sφ(d₁)√τ and φ′(x) = −xφ(x),
   volga = ∂𝒱/∂σ = −Sd₁φ(d₁)√τ·∂d₁/∂σ = 𝒱d₁d₂/σ. At the forward, d₁ = ½σ√τ and d₂ = −½σ√τ, so d₁d₂ = −σ²τ/4,
   small and negative for short-dated options at the forward; volga is positive where d₁ and d₂ share a sign.
   At unadjusted 25-delta the call wing is positive, while the put wing needs σ√τ < 0.674.
7. **The dispersion trade's sign.** Each locally frozen, delta-hedged leg earns
   ½ΓS²(σ²_r − σ²_i) integrated over time, with its position quantity included in Γ.
   Vega matching alone does not equate these variance weights when leg volatilities differ.
   If member and index quantities instead give local variance weights cwᵢ and c, the P&L is
   c[Σwᵢ(σ²_{r,i} − σ²_{i,i}) − (σ²_{r,I} − σ²_{i,I})]. With members' realized vols equal to their
   implied ones, substitute σ_I² = Σwᵢ²σᵢ² + ρΣ_{i≠j}wᵢwⱼσᵢσⱼ to get
   c(ρ_impl − ρ_real)Σ_{i≠j}wᵢwⱼσᵢσⱼ. Its sign follows the correlation gap under those local
   matching assumptions. The simulation uses an approximate ATM vega scale and evolving Greeks;
   its 0.92 correlation and 95% sign agreement are numerical diagnostics, not an exact payoff identity.
8. **The direction of the optimal quotes.** From the first-order condition δ^{b*} = 1/k + θ(q) − θ(q+1) and
   δ^{a*} = 1/k + θ(q) − θ(q−1). The value θ is concave in q (the penalty −φq² makes extra inventory costlier the
   larger it is), so θ(q) − θ(q+1) increases in q and θ(q) − θ(q−1) decreases in q: when q grows the bid moves away
   from fair value and the ask moves toward it. Both quotes shift down, by about (q ± ½)√(φe/(Ak)) in the GLFT
   approximation.
9. **(qual) Demand pressure.** A dealer who sells q options to end users at prices p and hedges them has wealth
   W = q^⊤(p − E x) − q^⊤ε, with E W = q^⊤(p − E x) and Var W = q^⊤Σ_ε q. Maximizing
   E W − (γ/2)Var W gives p − E x = γΣ_ε q, and market clearing q = d gives p = E x + γΣ_ε d. Then ∂p_i/∂d_j = γΣ_ij =
   γΣ_ji = ∂p_j/∂d_i (symmetric, as Σ is), and with Σ_ε = 0 (perfect replication) p = E x whatever d is.
10. **(qual) Exact exponential utility.** Short q units at price p with residual ε, the dealer's terminal wealth is
   q(p − E x − ε). Indifference: E[−e^{−γq(p − Ex − ε)}] = −1, so p − E x = (1/(γq))log E e^{γqε}. With the cumulant
   expansion log E e^{tε} = κ₂t²/2 + κ₃t³/6 + …, t = γq: p − E x = γqκ₂/2 + γ²q²κ₃/6 + … The first term is the
   mean-variance (average) premium; a positive third cumulant, a residual that loses big in crashes, adds a term
   growing like q² per unit within the local cumulant expansion. This correction increases total compensation
   faster than linearly, but a moment finite only near zero does not establish finite prices for arbitrary q.

## For the researcher

* **The theorems.** Gârleanu, Pedersen and Poteshman (2009), "Demand-Based Option Pricing," *RFS* 22(10); Bollen and
  Whaley (2004) on net buying pressure; Stoikov and Sağlam (2009) on option market making under inventory risk.
* **Simplifications.** One period, a single competitive dealer with mean-variance preferences, delta hedges at a fixed
  volatility rather than optimal hedges, γ chosen for scale; the Deribit flow is two days and the taker side is only a
  proxy for end users.
* **Open problems.** Identifying dealers' risk aversion; demand against risk in the volatility premium; dynamic
  equilibrium with many dealers and inventories.

## Data and reproducibility

* Deribit BTC option trades (100 Wednesdays 2024-01-03 … 2025-11-26, 00–12 UTC; the two Surface days), DVOL; Binance
  BTCUSDT hourly 2021–2025; Part 12's weekly SSVI grid (`history`); Part 10's `btc` months; Cboe COR3M (new fetcher
  `data.cboe_index`, frozen through 2025-12-31); FRED VIXCLS; Kenneth French daily market and 49 industries.
* Registered with the trial counter: the forecast-edge test (chapter 7) and the walk-forward predictor (chapter 18).
* Long items resume: `mm_learn` per seed, `hedging_replay` per run with checkpoints every 50 steps.
* Settlement at Binance's 08:00 hourly close stands in for Deribit's 30-minute TWAP (chapters 11, 14); Deribit's mark
  price is the exchange's own model value (chapter 8).

---

# 量化金融，从零搭建 — 第11部分：交易期权

第三幕中属于从业者的一部分：开场、十八章、写给研究者的一章和结尾，约64分钟。每个数字都由本系列自己的代码计算（`compute.py`；公司库的`quoting`、`hedge`、
`sim`和`trees`，在`tests/test_quant_house.py`中测试），数据来自Deribit的成交和DVOL、币安的BTCUSDT小时数据、第12部分的每周Deribit微笑、
芝加哥期权交易所的COR3M、FRED的VIX、肯尼斯·弗伦奇的市场与行业数据，以及公开的监管与法院记录。玩具模型在画面上标明为示意。

*讲的是方法，不构成投资建议。期权策略的结果是历史的、只针对一个市场。SEBI一案根据监管机构的临时命令和声明以及该公司的公开声明描述为指控；
截至撰写时尚无最终认定。*

## 各章（约64分钟）

* **伽马对时间损耗（开场）。** 交易台问题；实时重放2021年5月：按DVOL的74%买入、每小时对冲的三十天平值比特币跨式组合，已实现127%，
  在16.9的权利金上只赚+1.7。历史：1973、1985、1987、2018–2020、2021、2024。
* **1. 头寸即希腊字母，以及损益归因。** 跨式组合价值曲面的三维图：伽马之碗对十天的时间损耗，在σ√dt处平衡。推导Δ、Γ、𝒱、Θ = −½σ²S²Γ、
  盈亏平衡变动（50%波动率时每天2.6%）、𝒱 = στS²Γ。实验：`book_greeks`；2025年12月10日到11日的真实归因：delta −1,839、伽马+178、
  theta −86、vega −27、vanna +74、volga −10；实际−1,679，未解释+30（1.8%）。
* **2. 真实路径上的伽马剥头皮。** 实时对冲；美元伽马地形的三维图；同样720个小时收益率打乱2,000次：均值+7.8，真实的+1.7只胜过0.4%；
  崩盘挪到第2天得+2.1。卡尔–马丹的对数合约。实验：`delta_hedge`。
* **3. 多久对冲一次。** 三个对冲者赛跑；244个三十天跨式组合：每小时−2.86（标准差3.51），每天−2.59（4.27），按2%变动−2.88（3.75）；
  均值无显著差别（t = −1.6），频率买到的是精度；10个基点成本下每小时−4.30、每天−3.07；方差比0.978。
* **4. vega、vanna、volga。** vega曲面三维图；推导；风险逆转与蝶式价差作为vanna与volga的价格；vanna–volga在Surface上：RR −5.6、BF +1.75，
  十delta之间误差0.19个点；两年每周RR只有28%为负。
* **5. 策略。** 一张三维损益曲面在六种结构间变形；96周真实微笑上的记录：宽跨式77%的星期亏钱；没有一个t超过1.6。
* **6. 期权收益中的波动率溢价。** 96个对冲跨式组合：均值每100亏1.22，t = −3.6；科瓦尔–舒姆韦、巴克希–卡帕迪亚；P与Q的差即溢价。
* **7. 预测者的优势与下注大小。** 登记过的检验（1.75对0.57，t ≈ 2.4）；戈亚尔–萨雷托；凯利：高斯答案46倍，破产墙30倍，经验最优贴着墙。
* **8. 做市：价差。** 骰子游戏；格洛斯滕–米尔格罗姆模型实时运行；524,281笔Deribit成交：做市优势+0.36个波动率点，一小时后保留59%。
  实验：`markouts`。
* **9. 库存与会学习的做市商。** HJB与GLFT推导；实验`quote`；表格型Q学习5个种子达到精确最优的79–92%，GLFT 99%，对称报价为负。
* **10. 对冲整本账。** 希腊字母空间；赫斯顿模拟中伽马与vega对冲把标准差从2.14降到0.54；按桶的vega；惠利–威尔莫特带（实验`ww_band`）；
  深度对冲重放。
* **11. 到期与钉住风险。** 伽马尖峰三维图；阿韦拉内达–利普金推导与模拟（净多头33%收在执行价附近，净空头0.35%）；比特币星期五到期24.5%
  对所有小时19.9%（z = 1.9）：只是提示。
* **12. 提前行权、合成头寸与股息博弈。** 默顿的结论；股息条件；树上的行权区域（美式4.55对欧式4.19）；转换与反转；指派抽签。
* **13. 离散度与隐含相关性。** 相关矩阵与σ_I(ρ, σ̄)曲面；实验`implied_correlation`；COR3M 2006–2025：峰值90.8，2024年低点7.6；
  模拟交易：损益与ρ_impl − ρ_real的相关系数0.92。
* **14. 印度的到期日热潮与彩票的回报。** SEBI的研究与2024年措施；Deribit上两天内到期的虚值期权：按权利金加权回报−19%，84%作废。
* **15. 案卷：SEBI与简街（指控）。** 临时命令、托管存款、证券上诉法庭的上诉、简街诉千禧（2024年和解）；玩具模型及其三维推广；
  2025年9月的日内持仓限额。
* **16. 危机档案。** 两本示意性的做空看跌账（近对冲与深对冲），2020年3月回撤−26.6与−36.3；LJM与安联Structured Alpha。
* **17. 业界。** OCC成交量；散户期权与批发商；SIG、Optiver、IMC、简街；CFTC诉Optiver；交易台的循环。
* **18. 前沿。** 登记过的样本外预测器：与结果的相关性约为零，只学会了"卖"；巴利等人、曹等人、巴尔达奇等人、方与许。
* **写给研究者：基于需求的期权定价。** 必须持有−d份期权、对冲后残差为ε（收益减去离散Delta对冲收益）的竞争性均值–方差交易商定价为p = E[x] + γΣ_ε d（格尔莱亚努、佩德森与波特什曼2009的一阶形式）：自身冲击γVar ε_i，交叉冲击γCov(ε_i, ε_j)，Σ_ε = 0时为零。模拟：默顿跳跃扩散（σ 45%，每年4次、均值−8%、离散度10%的跳跃），执行价80–120的30天虚值期权，按总波动率52%每日对冲，40,000条路径：残差标准差每100为1.1–2.0（无跳跃0.4–0.9，每小时0.08–0.19）。取γ使一单位85看跌需求将其自身波动率抬高一点，则80看跌抬高1.1点、120看涨0.19点（无跳跃每日0.13，每小时0.006）；对每个看跌的需求在80处加4.0点、120处1.0点，对看涨的需求让微笑反向倾斜（80处1.4、120处2.4）。精确指数效用无差异价与一阶线对照，卖出看跌残差偏度4.6：边际溢价在一单位时高9%，四单位时高51%。曲面两天的Deribit吃单流量，占成交vega的净份额：30天内虚值看跌−21%，以上+14%；虚值看涨−2%与−23%；平值附近约为0。三个开放问题；暂停题：以美元计90看跌涨得更多（为85自身冲击的1.08，80看跌为0.72），以波动率计80看跌更多（1.1点对0.8点），因为80看跌的vega更小。
* **结尾：报价引擎、回顾、交易台问题、十道习题（两道为资格考试水平）。**

## 教材对照

| 教材章节 | 位置 |
|---|---|
| Natenberg：合约、远期定价、到期损益 | 第2部分；第5章 |
| Natenberg：理论定价；波动率 | 第10部分；第6–7章 |
| Natenberg：风险度量（希腊字母、二阶） | 第1、4章 |
| Natenberg：动态对冲 | 第2、3章 |
| Natenberg：价差、波动率价差、风险考量、牛熊价差 | 第5章（第7章：仓位） |
| Natenberg：合成头寸、期权套利 | 第12章；第9部分 |
| Natenberg：美式期权提前行权 | 第12章 |
| Natenberg：对冲策略、头寸分析 | 第1、10章 |
| Natenberg：模型与现实、再论波动率 | 第6、11、16章 |
| Natenberg：指数期货与期权、跨市场价差 | 第13、14章 |
| Natenberg：波动率合约、偏斜 | 第12部分；第4章 |
| Sinclair《波动率交易》：测量与预测、溢价、对冲、凯利 | 第7部分；第3、6、7、10章；第8部分 |
| Sinclair《头寸期权交易》 | 第5–7章 |
| Taleb《动态对冲》：做市、流动性空洞、希腊字母、vega分桶、钉住风险 | 第1、2、4、8–11、13、16章；奇异期权在第15部分 |
| Bennett《交易波动率》：波动率交易、方差互换、离散度、偏斜与期限结构 | 第2–4、13章；第12、13、15部分 |
| Hull《期权、期货及其他衍生产品》：交易策略、希腊字母 | 第5章；第1、10章 |

## 交易台问题与解答

1. **安静一周里持有对冲后的跨式组合多头。** 每日损益为½ΓS²[(dS/S)² − σ²_imp dt] + vega·dσ_imp。没有波动时，第一项就是全额的时间损耗，
   每天½ΓS²σ²_imp dt；若隐含波动率也下降，vega也亏钱。只有当按伽马加权的已实现方差超过隐含方差时才赚钱。
2. **骰子。** E[X] = 3.5，围绕它对称报价，例如3.3 / 3.7。得知"偶数"后，E[X | 偶数] = 4，报价移到约3.8 / 4.2。要问的是为什么告诉你：
   通过交易传到你这里的信息，会让公允价值朝不利于你的方向移动（逆向选择）。
3. **深度实值美式看涨，明天派息2，利率4%，还剩两个月，看跌值0.3。** 行权获得股息D = 2。继续持有保留执行价的利息
   K(1 − e^{−rτ}) = 100(1 − e^{−0.04/6}) ≈ 0.66，以及看跌期权提供的保险0.3。因为2 > 0.96，今天、在除息日之前行权（第12章）。
   没有股息时永远不该提前行权：卖掉看涨，或做空股票对冲（默顿1973）。到期前一小时卖出大量平值期权的问题，见习题2：伽马接近峰值，还有钉住风险。

## 习题与解答

1. **伽马–时间损耗积分。** 按σ_imp给期权定价并对冲delta。由伊藤公式，dV = Θdt + ΔdS + ½ΓS²σ²_r dt。由σ_imp下的布莱克–斯科尔斯方程（r = 0），
   Θ = −½ΓS²σ²_imp。所以对冲后的账本赚取½ΓS²(σ²_r − σ²_imp)dt，整个期限内为∫½ΓS²(σ²_r,t − σ²_imp)dt。权重ΓS²在执行价附近和临近到期时很大，
   所以同样的已实现方差发生在那里就赚得多，远离执行价就赚得少（2021年5月）。
2. **到期时的伽马。** Γ = φ(d₁)/(Sσ√τ)。平值且τ → 0时，d₁ → 0，φ(0) = 1/√(2π)，所以Γ ≈ 1/(Sσ√(2πτ))。S = 100、σ = 0.5时：
   一天（τ = 1/365）为0.152，一分钟（τ = 1/525,600）为5.78，大了√1440 ≈ 38倍。
3. **两资产的隐含相关性。** σ_I² = ¼σ² + ¼σ² + 2·¼ρσ² = σ²(1 + ρ)/2，所以ρ = 2σ_I²/σ² − 1。
4. **有知情对手的骰子。** 设对手以概率p知道点数，否则随机交易。报价3.5 ± s，s ≤ 0.5。与不知情者的交易赚s；与知情者的交易亏
   E|X − 3.5| − s = 1.5 − s，因为|X − 3.5|等可能地取0.5、1.5、2.5，而且都会成交。盈亏平衡要求(1 − p)s = p(1.5 − s)，即s = 1.5p，
   在p ≤ 1/3时成立。
5. **对冲带宽度的标度。** 在delta周围半宽为h的带内，错配对冲每单位时间的方差按h²σ²S²增长；为留在带内所需的交易速率，按股数乘价格计约为(ΓσS)²·S/h。
   风险厌恶为γ的对冲者因此最小化γσ²S²h² + λσ²S³Γ²/h。令导数为零得h³ = λSΓ²/(2γ)，即h ∝ (λSΓ²/γ)^{1/3}。
   Whalley与Wilmott的渐近分析给出的常数是3/2而不是1/2。
6. **vanna与volga。** d₁ = (ln F/K + ½σ²τ)/(σ√τ)，所以∂d₁/∂σ = √τ − d₁/σ = −d₂/σ（用到d₂ = d₁ − σ√τ）。于是
   vanna = ∂Δ/∂σ = φ(d₁)∂d₁/∂σ = −φ(d₁)d₂/σ；又因𝒱 = Sφ(d₁)√τ且φ′(x) = −xφ(x)，volga = ∂𝒱/∂σ = 𝒱d₁d₂/σ。在远期处
   d₁ = ½σ√τ、d₂ = −½σ√τ，d₁d₂ = −σ²τ/4，对短期期权很小：平值处volga ≈ 0，两翼d₁与d₂同号，volga为正。
7. **离散度交易的符号。** vega匹配、delta对冲的跨式组合，每条腿赚取½ΓS²(σ²_r − σ²_i)对时间的积分，平值时½ΓS²对每条腿是方差的同一倍数c。
   损益为c[Σwᵢ(σ²_{r,i} − σ²_{i,i}) − (σ²_{r,I} − σ²_{i,I})]。把σ_I² = Σwᵢ²σᵢ² + ρΣ_{i≠j}wᵢwⱼσᵢσⱼ代入已实现和隐含的指数方差。
   若成分股的已实现波动率等于隐含，除c(ρ_impl − ρ_real)Σ_{i≠j}wᵢwⱼσᵢσⱼ外全部抵消，符号即ρ_impl − ρ_real的符号
   （第13章的模拟：差值与损益的相关系数0.92，95%的情景符号正确）。
8. **最优报价的方向。** 由一阶条件δ^{b*} = 1/k + θ(q) − θ(q+1)，δ^{a*} = 1/k + θ(q) − θ(q−1)。价值θ对q是凹的（惩罚−φq²使库存越大，
   多一单位越贵），所以θ(q) − θ(q+1)随q增大、θ(q) − θ(q−1)随q减小：q增大时买价远离公允价值、卖价靠近它。两个报价都下移，
   在GLFT近似下约为(q ± ½)√(φe/(Ak))。
9. **（资格考试）需求压力。** 持有q份期权、残差为ε的交易商财富为W = q^⊤(p − E x) − q^⊤ε，E W = q^⊤(p − E x)，Var W = q^⊤Σ_ε q。最大化E W − (γ/2)Var W得p − E x = γΣ_ε q，市场出清q = d给出p = E x + γΣ_ε d。于是∂p_i/∂d_j = γΣ_ij = ∂p_j/∂d_i（对称），Σ_ε = 0（完美复制）时无论d为何p = E x。
10. **（资格考试）精确的指数效用。** 以价格p卖出q单位、残差为ε时，期末财富为q(p − E x − ε)。无差异条件E[−e^{−γq(p − Ex − ε)}] = −1给出p − E x = (1/(γq))log E e^{γqε}。由累积量展开log E e^{tε} = κ₂t²/2 + κ₃t³/6 + …，t = γq：p − E x = γqκ₂/2 + γ²q²κ₃/6 + …。第一项是均值–方差（平均）溢价；正的三阶累积量，即在崩盘中大亏的残差，增加一个按q²增长的项，所以对崩盘保护的大仓位被定价得超过比例。

## 写给研究者

* **定理。** 格尔莱亚努、佩德森与波特什曼（2009），《基于需求的期权定价》，*RFS* 22(10)；Bollen与Whaley（2004）论净买入压力；Stoikov与Sağlam（2009）论库存风险下的期权做市。
* **简化。** 单期、单一竞争性的均值–方差交易商、按固定波动率做Delta对冲而非最优对冲、γ只为确定尺度；Deribit的流量只有两天，吃单方只是终端用户的代理。
* **开放问题。** 识别交易商的风险厌恶；波动率溢价中需求与风险之分；多交易商、跨期库存下的动态均衡。

## 数据与可复现性

* Deribit比特币期权成交（2024-01-03至2025-11-26的100个星期三，世界协调时0–12点；Surface两天）、DVOL；币安BTCUSDT小时数据2021–2025；
  第12部分的每周SSVI网格；第10部分的月度损益；芝加哥期权交易所COR3M（新的`data.cboe_index`，冻结到2025-12-31）；FRED的VIX；弗伦奇的数据。
* 在试验计数器上登记：预测者优势检验（第7章）和样本外预测器（第18章）。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part11.md`](../../../docs/qa/quant/part11.md).*
