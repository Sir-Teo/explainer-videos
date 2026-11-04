# Quant, Built — Part 10: Black–Scholes–Merton

Part 10 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the second part of Act III, Derivatives, and the series' pilot. It shows how an option
can be manufactured from the stock and cash, derives the Black–Scholes–Merton price three ways, takes the hedger's
profit and loss apart term by term, and tests all of it on real markets. Every number is computed by the series' own
code ([`compute.py`](compute.py), the House library in [`explainer/quant/house`](../../../explainer/quant/house))
from public data: Deribit's option trades and DVOL index, Binance's Bitcoin prices, and Kenneth French's US market
returns. Schematics and made-up examples are labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 63 minutes)

* **Manufacturing an option.** A real month, October 2021: a 30-day Bitcoin call sold at Deribit's DVOL (89%);
  Bitcoin rises 37%; unhedged the seller loses 27 per 100, hedged every hour the seller makes 1.15 (the median of the
  1,706 months of chapter 15). Pause and predict; implied 89% against realized 61%; objectives; the House's vol desk.
* **1. Before the formula.** Bachelier (1900); Sprenkle (1961), Boness (1964), Samuelson (1965) and their two
  unknown rates μ and ρ; Thorp and Kassouf (1967) and the warrant hedge (Thorp's discount-free formula, as MacKenzie
  2003 reports); Black–Scholes and Merton; the JPE's and REStat's first rejections; the CBOE opens (26 April 1973:
  calls only, 16 stocks, 911 contracts; puts from 1977); Black's sheets; the Nobel (1997).
* **2. The riskless portfolio.** The stock, the bond, the option; the self-financing replicating portfolio
  (Shreve II §4.5): match the dW terms (Δ = ∂V/∂S), then the dt terms (μ cancels): the Black–Scholes PDE.
* **3. Solving the equation: heat, run backwards.** (3D) The value over log-spot and time left rising out of the
  payoff; the heat kernel sliding along it; the change of variables to u_τ = ½σ²u_yy, the convolution, the formula.
  **Lab:** `bs.price` and the new `bs.heat_price` agree to 12 decimals.
* **4. The price as an expectation.** Feynman–Kac; P (19.74) and Q (12.36 ± 0.03 against 12.34); Girsanov; the
  Gaussian integral by hand. **Replay:** Monte Carlo under Q with 8 seeds closing on the formula, and the
  Girsanov-reweighted estimator as the baseline (here narrower: sd ratio 0.62, importance sampling by accident).
* **5. The tree and its limit.** One step (Part 9 builds it); **3D:** whole CRR lattices (N = 4, 16, 64, 256)
  settling onto the Black–Scholes surface (worst node gap 0.99 → 0.11); the recursion expanded into the PDE; the
  N = 1…400 sawtooth (Diener–Diener 2004). **Lab:** `trees.crr`'s backward loop: 9.9705, 10.4194, 10.4456 vs 10.4506.
* **6. The Greeks as geometry.** The value surface in 3D; delta and gamma as time runs out; the identity
  Sφ(d₁) = Ke^{−rT}φ(d₂) and two-line derivations; Θ = −½σ²S²Γ computed; vega = σ(T − t)S²Γ.
* **7. Where the hedger's money comes from.** d(book) = ½ΓS²(σᵢ² − σᵣ²)dt; the breakeven band; **Lab:** the House's
  hedging ledger (`hedge.delta_hedge`) with its gamma, theta and residual columns; three live paths; 20,000-path
  distributions.
* **8. Hedging with the wrong volatility.** El Karoui–Jeanblanc–Shreve (1998) proved; **3D:** the dollar-gamma
  mountain with two paths and their filling columns (≈7× apart); hedge at implied or at actual (Ahmad–Wilmott 2005):
  20,000 paths, sd 0.96 vs 0.33 around the same mean 1.99; 4,000 Heston paths (ρ = −0.87 vs 0.99).
* **9. Hedging in steps.** sd ∝ √Δt derived (Boyle–Emanuel 1980; Derman–Kamal's √(π/4)) and measured with 5 seeds
  as a band; the distribution's skew; jumps put a floor under the error (Derman–Taleb 2005), with the jump term
  computed.
* **10. Paying for it: Leland's volatility.** **3D:** the cost–risk landscape over hedges and costs, with the ridge of
  optimal frequency (252 at zero cost; 26 at 25 bp; 13 at 50 bp); Leland derived; **Lab:** `bs.leland_vol` (21.2%
  daily, 20.6% weekly at 0.2% round trip) and the weekly check (−0.53 → −0.25 → +0.01 without the end trades);
  the limit: σ_L 21% → 38% and the premium 4.26 → 7.49 as hedging speeds up (Soner–Shreve–Cvitanić 1995;
  Kabanov–Safarian 1997).
* **11. Turning the formula inside out.** One real quote inverted; **3D:** Jäckel's normalized price b(x, s) and a
  quote's plane; existence, Brenner–Subrahmanyam, Newton and its flat corner; **Lab:** `bs.implied_vol` (now freezing
  converged quotes); **Replay:** all 254 Surface quotes solving at once (median 3 iterations, worst 11), against plain
  Newton from 50% (10 quotes thrown off, 9 never return); one tick on the flattest quote moves its vol by 19 points.
* **12. The first smile, and the Surface's first row.** The smiles of 10 December 2025; the Surface in 3D; the first
  row: 4.36 vol points in sample, 4.74 the next day, no calendar arbitrage, 11 parameters; DVOL 45.9% vs ATM30 44.1%.
* **13. Dividends, borrow and the forward.** The carry slider moving the risk-neutral fan; the PDE with a yield; one
  formula on the forward (Merton 1973, Garman–Kohlhagen 1983, Black 1976, inverse options); the Surface's basis
  (2.6% to 4.8% a year) and the fake skew from forgetting the forward (+1.2/−1.2 points at 51 days, +3.3/−2.7 at 289).
* **14. Early exercise and the free boundary.** Merton's no-early-exercise; the American put (6.0900 vs 5.5735);
  **3D:** the early-exercise premium over (S, τ) with the free boundary; value matching, smooth pasting; Kim's
  integral from the tree's boundary (6.0947); Brennan–Schwartz (1977); Barone-Adesi–Whaley (6.0976, critical 81.7);
  the call exercised only just before a dividend.
* **15. Selling volatility on real Bitcoin.** 1,706 thirty-day calls sold at DVOL and hedged hourly: mean +1.35 per
  100, 81% winning months; **Replay:** the 57 independent months swept with a block-bootstrap band (5 seeds × 200),
  ending between 1.05 and 1.86; costs; inverse settlement; the worst month (August 2024).
* **16. October 1987.** Portfolio insurance (Rubinstein–Leland 1981); **Lab:** `hedge.replicate_put`; the insured
  portfolio replayed on French's daily data from 1 July 1987: 93% in stocks on 5 October, 64% going into Black
  Monday, 11% the day after; it ends October at 83.8 against a floor of 93.0; the Brady Commission's numbers; −20.7σ
  and Jackwerth–Rubinstein's 10⁻¹⁶⁰; the skew; MacKenzie's performativity.
* **17. The Nobel, and then LTCM.** The 1997 prize; LTCM's book (28:1 balance-sheet leverage and over $1 trillion
  notional at end-1997, GAO 1999); the VIX through 1998 (18.0 on 1 July, 45.7 on 8 October) and an illustrative
  short-vega book; the rescue; what every hedge assumes.
* **18. Industry: the formula at work.** Black's sheets and the CBOE floor (MacKenzie–Millo 2003); O'Connor &
  Associates; quoting in volatility (Rebonato's "wrong number") and Haug–Taleb's dissent; the 0.4·Fσ√T rule on the
  Surface (within 1.0%); Black-76 in the plumbing; Deribit (Coinbase, 2025) and IBIT options (2024).
* **19. Frontier: 2023 to 2026.** The 2026 implied-volatility race (Schadner; Le Floc'h–Healy; PIVOT; Amiriyan–Boutaib;
  preprints); Black–Scholes machine-checked in Lean (Ushakov–Berdinsky); **Replay:** a small network learns a first
  guess for implied vol (5 seeds), finished by Newton steps; inverse options (Alexander–Chen–Imeraj 2023); hedging
  crypto options (Matic–Packham–Härdle 2023); the minimum-variance delta (Hull–White 2017; Ruf–Wang 2022; on BTC in
  Part 13).
* **For the researcher: when to rebalance a hedge.** Equal times: N·Var of the error → (T/2)E∫Γ²σ⁴S⁴dt (11.9
  per 100 of stock, squared, for a three-month at-the-money call at 20%). Rebalancing when the price has moved by a:
  the squared move is exactly a², the error is ½Γσ²S²(Eτ − τ), and with Eτ = a²/(σ²S²), Var τ = (2/3)a⁴/(σS)⁴ the
  per-interval variance is Γ²a⁴/6 against Γ²a⁴/2 at equal times: a factor of three. Optimizing the width, a ∝ |Γ|^{−1/2}
  (in delta terms |Δ_t − Δ_τ|² = hΓ_τ) gives N·Var → (1/6)(E∫|Γ|σ²S²dt)² = 2.64, at most a third of the equal-time
  constant by Cauchy–Schwarz (Fukasawa 2011's lower bound over stopping-time rules; Rosenbaum and Tankov 2014 with
  jumps); fixed price or delta bands give 3.98. Simulation (3,000 paths, 2^14 steps) at N ≈ 16/64/256: equal times
  10.3/12.2/12.8, price band 4.5/4.3/4.6, delta band 5.1/4.1/4.1, optimal band 3.2/3.0/2.8. Bitcoin: 47 thirty-day calls
  written every 15 days on 2019–2020 one-minute closes, hedged at their own realized (hindsight) volatility: error
  standard deviation 25.6% of the premium at equal times vs 10.1% with the band (16 trades), 19.0% vs 8.6% (64); mean
  errors +4.5/+11.9% and +8.4/+10.8%, sources not separated. Three open problems; pause: 256 × 2.64/11.9 ≈ 57 trades.
* **Recap, desk questions, nine problems (two at qualifying-exam level).**

## Hands-on

* **Labs** (the House's code on screen, then run): `bs.price` / `bs.heat_price` (ch. 3); `trees.crr` (ch. 5);
  `hedge.delta_hedge` (ch. 7); `bs.leland_vol` with the cost-aware hedger (ch. 10); `bs.implied_vol` (ch. 11);
  `hedge.replicate_put` (ch. 16).
* **Replays with seeds as bands:** Monte Carlo under Q vs Girsanov (ch. 4); the lattice scrub (ch. 5); sd vs N and the
  jump floor (ch. 9); the solver race (ch. 11); the BTC study month by month (ch. 15); the learned first guess (ch. 19).
* **3D:** the heat surface (3), the lattice (5), the value surface (6), dollar gamma (8), the cost–risk landscape (10),
  the normalized price (11), the Surface (12), the early-exercise premium (14).

## Textbook audit

| Book · section | Where |
|---|---|
| Hull, *OFOD* (11th ed.) ch. 13 binomial trees | ch. 5 (limit); one step and CRR → Part 9; numerics → Part 16 |
| Hull ch. 14 Wiener processes and Itô's lemma | Part 5 (ch. 2 recalls Itô) |
| Hull ch. 15 the BSM model (lognormality, the PDE, risk-neutral valuation, implied volatility, dividends) | ch. 2–4, 11–13 |
| Hull ch. 17 options on indices and currencies; ch. 18 futures options and Black's model | ch. 13 (FX detail → Part 22) |
| Hull ch. 19 the Greek letters (delta, theta, gamma, vega, the Δ–Θ–Γ relation, portfolio insurance) | ch. 6, 7, 16 |
| Hull ch. 20 volatility smiles | ch. 12, 16; the rest → Part 12 |
| Shreve II §4.5 the BSM equation | ch. 2, 3, 6 |
| Shreve II §5.2 risk-neutral pricing; §5.5 dividends; §5.6 forwards and futures | ch. 4, 13 |
| Shreve II §8.4 finite-expiration American put; §8.5 American calls (§8.3 perpetual put → Part 8) | ch. 14 |
| Björk, *Arbitrage Theory* ch. 7 arbitrage pricing; ch. 8 completeness and hedging; ch. 10 parity and delta hedging | ch. 2–4, 7 |
| Björk, the dividends, forwards/futures and currency chapters (by title) | ch. 13 |
| Wilmott, *PWOQF* ch. 5 the BS model; ch. 6 PDEs (the heat equation); ch. 7 formulae and Greeks; ch. 8 generalizations; ch. 9 early exercise | ch. 2, 3, 6, 13, 14 |
| Wilmott, "how to delta hedge" (Ahmad–Wilmott), discrete hedging, transaction costs (by title) | ch. 8, 9, 10 |
| Joshi, *Concepts and Practice* ch. 5–7 (Itô, risk neutrality, practical pricing); ch. 12 discretionary choice | ch. 2–9, 11, 14 |
| Taleb, *Dynamic Hedging* (delta, gamma, theta, vega, the hedging error) | ch. 6–10, 18 |
| Baxter–Rennie ch. 3 the BS model by martingales; ch. 4 dividends, FX | ch. 4, 13 (quantos → Part 22) |

## Papers on screen

Sprenkle (1961); Boness (1964); Samuelson (1965); Thorp–Kassouf (1967); Black–Scholes (1973); Merton (1973);
Black (1976); Brennan–Schwartz (1977); Cox–Ross–Rubinstein (1979); Boyle–Emanuel (1980); Rubinstein–Leland (1981);
Garman–Kohlhagen (1983); Leland (1985); Barone-Adesi–Whaley (1987); Brady Commission (1988); Brenner–Subrahmanyam
(1988); Kim (1990); Carr–Jarrow–Myneni (1992); Rubinstein (1994); Soner–Shreve–Cvitanić (1995); Corrado–Miller (1996);
Jackwerth–Rubinstein (1996); Kabanov–Safarian (1997); El Karoui–Jeanblanc–Shreve (1998); Derman–Kamal (Goldman Sachs,
1998); GAO (1999); MacKenzie (2003); MacKenzie–Millo (2003); Diener–Diener (2004); Ahmad–Wilmott (2005);
Derman–Taleb (2005); Haug–Taleb (2011); Jäckel (2015); Hull–White (2017); Ruf–Wang (2022); Alexander–Chen–Imeraj
(2023); Matic–Packham–Härdle (2023); Schadner (2026); Le Floc'h–Healy (2026); Saqur et al. (PIVOT, 2026);
Ushakov–Berdinsky (2026); Amiriyan–Boutaib (2026). arXiv items are preprints.

## Build it

The finished video is not stored in the repository. From the repo root, after the setup in the
[top-level README](../../../README.md#setup) (or `bash tools/setup_linux.sh`):

```bash
python -m explainer.quant.data                    # the market data, fetched once and checksummed (~2 min)
python -m videos.quant.quant10.compute            # every computed item (~40 CPU-min; cached in .cache/quant10)
python tools/build.py quant10 -q l                # 480p preview (EXPLAINER_TTS=silent for no narration)
python tools/build.py quant10 -q k --fps 60       # 2160p60
python tools/qa_scene.py quant10 Ledger           # one chapter, silent, with a contact sheet
```

## Desk questions, with solutions

1. **An at-the-money call, one year, volatility 20%, spot 100, no rates: price it in your head.** At the money,
   d₁ = σ√T/2 is small, so C = S[N(d₁) − N(d₂)] ≈ S φ(0) σ√T = 0.3989 σS√T ≈ 0.4 × 0.2 × 100 = 8. The formula gives
   7.97.
2. **You are long an at-the-money straddle and the stock does not move for a week. Did you make or lose money?** You
   lost: a long straddle is long gamma and short theta, and with no move the gamma earns nothing while theta is paid
   in full. For a one-month 20% straddle on 100 that is about 0.53 for the week (twice a call's theta).
3. **The delta of an at-the-money digital call near expiry.** The digital pays 1 above the strike; its delta is the
   risk-neutral density at the strike, φ(d₂)/(Sσ√τ), which grows like 1/√τ. A tiny move flips the hedge between none
   and a large position: unhedgeable in practice, so desks over-hedge digitals as a tight call spread (long a call at
   K − ε, short one at K, scaled by 1/ε) and charge for the spread.

## Problems, with solutions

1. **Parity and delta.** C − P = [S N(d₁) − K e^{−rT} N(d₂)] − [K e^{−rT} N(−d₂) − S N(−d₁)] = S − K e^{−rT}, using
   N(x) + N(−x) = 1. For delta, differentiate: ∂C/∂S = N(d₁) + [S φ(d₁) − K e^{−rT} φ(d₂)] ∂d₁/∂S (the two d's have
   the same derivative). Since d₂ = d₁ − σ√T, φ(d₂) = φ(d₁) e^{d₁σ√T − σ²T/2} = φ(d₁) S e^{rT}/K, so the bracket is
   zero and Δ = N(d₁).
2. **The tree's probability.** q u S + (1 − q) d S = S[d + q(u − d)] = S e^{rΔt}, so the stock grows at r on average
   and its discounted value is a martingale. At r = 0, q = (1 − d)/(u − d); with u = e^{σ√Δt}, d = 1/u, expanding
   gives q = ½ − σ√Δt/4 + O(Δt) → ½.
3. **The volatility trader's estimate.** With r = 0 and no drift, the expected hedged P&L of a short option sold at σᵢ
   and hedged at σᵢ when the stock realizes σᵣ is exactly C(σᵢ) − C(σᵣ) = 4.98 − 3.99 = 1.00 per 100 for a three-month
   at-the-money call at 25% and 20%: vega × (σᵢ − σᵣ) = 19.9 × 0.05. The frozen-spot shortcut ½(σᵢ² − σᵣ²)∫ΓS²dt with
   Γ kept at the money gives vega × (σᵢ² − σᵣ²)/σᵢ = 1.79: too high, because real paths leave the strike, where
   gamma is smaller (chapter 8).
4. **Leland.** σ_L² = σ²(1 + √(2/π) k / (σ√Δt)) with round-trip cost k = 0.2%. Daily (Δt = 1/252): σ_L = 21.2%;
   weekly (Δt = 1/52): σ_L = 20.6%. Weekly hedging is cheaper to sell, because it trades less, but its hedging error
   is about √5 ≈ 2.2 times larger (chapter 9).
5. **Early exercise.** A call is worth at least S − K e^{−rT} ≥ S − K, so it is always worth at least as much alive as
   exercised, and strictly more when r > 0: never exercise early without dividends. A put is worth at least
   K e^{−rT} − S, which is less than K − S when r > 0: exercising a deep put can win, because the strike received now
   earns interest. At r = 0 that bound is K − S itself, so the put is never exercised early either: early exercise
   of a put requires a positive interest rate.
6. **Leland derived.** Over a step, delta changes by δΔ ≈ Γ δS = ΓSσ√Δt Z, so the shares traded are |δΔ| and the
   expected cost of the step is (k/2)·S·E|δΔ| = (k/2)ΓS²σ√Δt·√(2/π) for a round-trip cost k (half on each trade).
   Per unit of time that is ½ΓS²·σk√(2/π)/√Δt: the same form as the variance term ½ΓS²σ² of the hedging P&L. Adding
   it to the variance, σ_L² = σ² + σk√(2/π)/√Δt = σ²(1 + √(2/π) k/(σ√Δt)).
7. **The forgotten forward.** Price an at-the-money-forward call with F = Se^{bT} and invert it with S and no carry:
   the formula thinks the call is in the money by ln(F/S) = bT, so it explains the price with a higher volatility.
   To first order δσ ≈ (∂C/∂F)(F − S)/vega ≈ N(d₁)·bT/(φ(d₁)√T) ≈ 0.5 × 0.02/(0.399 × 0.707) ≈ 3.5 points for
   b = 4%, T = 0.5, σ = 45%; the put, out of the money by the same amount, comes out about as much too low. The exact
   inversion (`carry` item): call 49.0% (+4.0), put 41.8% (−3.2); the asymmetry is second order.
8. **(qual) Exit-time moments.** Let X = σS·W locally, with variance rate v = σ²S², and τ = inf{t: |X_t| = a}.
   X² − vt is a martingale, so a² = vEτ: Eτ = a²/v. X⁴ − 6vtX² + 3v²t² is a martingale (Itô), so
   a⁴ − 6va²Eτ + 3v²Eτ² = 0, Eτ² = 5a⁴/(3v²) and Var τ = 2a⁴/(3v²). Over the interval the hedge error is
   ½Γ[(ΔX)² − vτ] = ½Γv(Eτ − τ), with variance ¼Γ²v²·2a⁴/(3v²) = Γ²a⁴/6. An equal-time step of the same mean length
   Δt = a²/v has error ½Γv Δt(Z² − 1), variance ½Γ²v²Δt² = Γ²a⁴/2.
9. **(qual) The optimal band.** Per unit time the error variance accrues at (1/6)Γ²a²v (intervals of variance Γ²a⁴/6
   at rate v/a²) and trades at v/a². The Lagrangian (1/6)Γ²a²v + λv/a² is minimized pointwise at a⁴ = 6λ/Γ², so
   a ∝ |Γ|^{−1/2}. Then Var = (c²/6)∫|Γ|v and N = (1/c²)∫|Γ|v with a = c|Γ|^{−1/2}, so N·Var = (1/6)(∫|Γ|v dt)². By
   Cauchy–Schwarz (∫|Γ|v dt)² ≤ T∫Γ²v²dt, so N·Var ≤ (1/6)T∫Γ²v² = (1/3)·(T/2)∫Γ²v², the equal-time constant.

## Data and reproducibility

* Deribit option trades of 10 and 11 December 2025, 00:00–12:00 UTC (6,060 and 7,843 trades) from
  `history.deribit.com`; DVOL hourly, April 2021 – December 2025; Binance BTCUSDT hourly candles; Kenneth French's
  daily factors through 2025. Each raw piece's SHA-256 is in [`../data/manifest.json`](../data/manifest.json).
* Seeds are fixed in every compute item. The BTC experiment's months overlap; chapter 11 also reports the statistic on
  57 non-overlapping months.

## For the researcher

* **The theorems.** Fukasawa (2011), "Asymptotically efficient discrete hedging," in *Stochastic Analysis with
  Financial Applications* (Birkhäuser): lim E[N]·E⟨error⟩ ≥ (1/6)(E∫|Γ|σ²S²dt)² over stopping-time rules, attained by
  the band |Δ_t − Δ_τ|² = hΓ_τ; Rosenbaum and Tankov (2014), "Asymptotically optimal discretization of hedging
  strategies with jumps," *Ann. Appl. Probab.* 24 (arXiv:1108.5940).
* **Simplifications.** One option, zero rates, the leading-order (small band) approximation; E[N]·Var rather than
  Fukasawa's E[N]·E⟨error⟩; the bands are checked on a grid of 2^14 steps, so overshoot widens them slightly.
* **Open problems.** Costs and a trade budget together for a book of options; corrections at a few dozen trades; jumps,
  rough volatility and many assets.

---

# 量化金融，从零搭建 — 第10部分：Black–Scholes–Merton

本系列共四十三部分（见[系列计划](../README.md)与[教学大纲](../SYLLABUS.md)），这是第三幕“衍生品”的第二部分，也是系列的试点。
本部分说明期权如何用股票和现金“制造”出来，推导并求解 Black–Scholes–Merton 方程（复制、热方程、风险中性期望、二叉树极限），逐项拆解对冲者的损益，并全部在真实市场数据上检验。
所有数字均由本系列自己的代码（[`compute.py`](compute.py) 与本系列公司的代码库 `explainer/quant/house`）根据公开数据计算：Deribit 的期权成交与 DVOL 指数、Binance 的比特币价格、Kenneth French 的美国市场收益、FRED 的 VIX。示意图和虚构例子在画面上均有标注。

*本视频讲授方法，不构成投资建议。*

## 章节（约63分钟）

* **用股票和现金造出一份期权。** 2021年10月：按DVOL（89%）卖出30天比特币看涨期权，比特币上涨37%；不对冲亏27（每100），每小时对冲赚1.15。
* **1. 公式之前。** 巴舍利耶；斯普伦克尔、博内斯、萨缪尔森的两个未知数μ和ρ；索普与卡苏夫的对冲；论文最初被拒；芝加哥期权交易所开业（911张合约）；布莱克的理论价格表。
* **2. 无风险组合。** 自融资复制组合：dW项相等得Δ = ∂V/∂S，dt项相等时μ抵消，得到Black–Scholes偏微分方程。
* **3. 解方程：倒着运行的热传导。** （三维）价值曲面从收益中升起、热核滑过；变量代换得热方程、卷积、公式。**实验：** `bs.price` 与新的 `bs.heat_price` 一致到12位小数。
* **4. 价格是一个期望。** 费曼–卡茨；P与Q；吉尔萨诺夫；手算高斯积分。**回放：** Q下的蒙特卡洛，8个种子收拢到公式；吉尔萨诺夫重新加权的估计量作基线（这里反而更窄）。
* **5. 二叉树及其极限。** （三维）N = 4、16、64、256 的完整格点落到曲面上；递推展开成偏微分方程；锯齿收敛。**实验：** `trees.crr`。
* **6. 希腊字母的几何。** 价值曲面；恒等式 Sφ(d₁) = Ke^{−rT}φ(d₂)；Θ = −½σ²S²Γ；Vega = σ(T − t)S²Γ。
* **7. 对冲者的钱从哪里来。** ½ΓS²(σᵢ² − σᵣ²)dt；盈亏平衡带；**实验：** 对冲账本 `hedge.delta_hedge`；三条路径；两万条路径的分布。
* **8. 用错误的波动率对冲。** 证明 El Karoui–Jeanblanc–Shreve；（三维）美元Gamma地形；按隐含还是按实际波动率对冲（Ahmad–Wilmott）；赫斯顿路径。
* **9. 分步对冲。** 误差 ∝ √Δt，五个种子的带；偏度；跳跃给误差垫了一个底（Derman–Taleb）。
* **10. 为对冲付费：利兰波动率。** （三维）成本–风险地形与最优频率山脊；推导利兰公式；**实验：** `bs.leland_vol`；对冲越频繁，σ_L 和期权费无上界（Soner–Shreve–Cvitanić；Kabanov–Safarian）。
* **11. 把公式反过来用。** （三维）归一化价格 b(x, s)；存在唯一性、Brenner–Subrahmanyam、牛顿法；**实验：** `bs.implied_vol`；**回放：** 254个报价同时求解。
* **12. 第一条微笑曲线与基准曲面的第一行。** 2025年12月10日的微笑；三维曲面；第一行：样本内4.36，次日4.74个波动率点。
* **13. 股息、借券与远期。** 持有成本滑块；写在远期上的同一个公式（Merton、Garman–Kohlhagen、Black-76、反向期权）；基准曲面的基差与忘掉远期造成的假偏斜。
* **14. 提前行权与自由边界。** （三维）提前行权溢价曲面与自由边界；Kim积分；Brennan–Schwartz；Barone-Adesi–Whaley；除息前的看涨期权。
* **15. 在真实的比特币上卖出波动率。** 1706笔交易；**回放：** 57个独立月份逐月展开，块自助法置信带；最差的月份。
* **16. 1987年10月。** 投资组合保险；**实验：** `hedge.replicate_put`，在1987年真实数据上重放；布雷迪委员会的数字；偏斜的诞生。
* **17. 诺贝尔奖，然后是LTCM。** 杠杆约28倍、表外名义金额超过一万亿美元（GAO 1999）；1998年的VIX；救助；每个对冲的前提。
* **18. 业界：公式如何谋生。** 布莱克的价格表与交易池；奥康纳联合公司；用波动率报价；0.4·Fσ√T 法则在基准曲面上的误差；Deribit 与 IBIT 期权。
* **19. 前沿：2023至2026年。** 2026年的隐含波动率求解竞赛（预印本）；Lean 中机器验证的 Black–Scholes；**回放：** 小网络学习初始猜测（5个种子）；反向期权、比特币期权对冲、最小方差Delta（第13部分）。
* **写给研究者：何时再平衡对冲。** 等时间：误差的N·Var → (T/2)E∫Γ²σ⁴S⁴dt（三个月期平值看涨、σ = 20%时，每100股为11.9）。价格移动a时再平衡：平方变动恰为a²，误差为½Γσ²S²(Eτ − τ)，由Eτ = a²/(σ²S²)、Var τ = (2/3)a⁴/(σS)⁴，每个区间方差为Γ²a⁴/6，等时间为Γ²a⁴/2：三倍。优化宽度a ∝ |Γ|^{−1/2}（用Delta表示为|Δ_t − Δ_τ|² = hΓ_τ）得N·Var → (1/6)(E∫|Γ|σ²S²dt)² = 2.64，由柯西–施瓦茨至多为等时间常数的三分之一（深泽2011在停时规则上的下界；有跳跃时罗森鲍姆与坦科夫2014）；固定价格带或Delta带为3.98。模拟（3,000条路径、2^14步），N ≈ 16/64/256时：等时间10.3/12.2/12.8，价格带4.5/4.3/4.6，Delta带5.1/4.1/4.1，最优带3.2/3.0/2.8。比特币：2019–2020年每15天写一份30天期看涨，共47份，用一分钟收盘价、以各自实现的（事后）波动率对冲：误差标准差在等时间下为期权费的25.6%，用带为10.1%（16次交易）；64次时为19.0%对8.6%；平均误差+4.5/+11.9%与+8.4/+10.8%，来源未分离。三个开放问题；暂停题：256 × 2.64/11.9 ≈ 57次。
* **回顾、交易台问题、九道习题（两道为资格考试水平）。**

教科书对照表与论文列表见英文部分。

## 交易台问题与解答

1. **一年期平值看涨期权，波动率 20%，现价 100，利率为零：心算价格。** 平值时 d₁ = σ√T/2 很小，C ≈ Sφ(0)σ√T ≈ 0.4 × 0.2 × 100 = 8；公式给出 7.97。
2. **你持有平值跨式组合，股价一周不动，赚了还是亏了？** 亏了：多头跨式是多 gamma、空 theta；价格不动时 gamma 一分不赚，theta 却照付。一个月期、20% 波动率、标的 100 的跨式，一周约亏 0.53（两倍看涨期权的 theta）。
3. **临近到期时平值数字期权的 delta。** 数字期权的 delta 是风险中性密度在行权价处的值 φ(d₂)/(Sσ√τ)，按 1/√τ 增长；微小的价格变动就会让对冲在“零”和“大量持仓”之间翻转。实务中交易台用很窄的看涨价差来超额对冲，并为此收费。

## 习题与解答

1. **平价关系与 delta。** 利用 N(x) + N(−x) = 1，C − P = S − Ke^{−rT}。对 S 求导，括号项 Sφ(d₁) − Ke^{−rT}φ(d₂) 因 φ(d₂) = φ(d₁)Se^{rT}/K 而为零，故 Δ = N(d₁)。
2. **二叉树的概率。** quS + (1 − q)dS = Se^{rΔt}，股票平均以 r 增长，贴现后的价格是鞅。r = 0 时 q = ½ − σ√Δt/4 + O(Δt) → ½。
3. **波动率交易员的估算。** r = 0 且无漂移时，以 σᵢ 卖出并对冲、股票实际波动率为 σᵣ，期望对冲损益恰为 C(σᵢ) − C(σᵣ)。三个月平值、25% 对 20%：4.98 − 3.99 = 1.00（每 100 名义），约等于 vega × (σᵢ − σᵣ) = 19.9 × 0.05。若把 gamma 固定在平值处，½(σᵢ² − σᵣ²)∫ΓS²dt 给出 1.79，偏高：真实路径会离开行权价，那里的 gamma 更小（第8章）。
4. **Leland。** σ_L² = σ²(1 + √(2/π)·k/(σ√Δt))，双边成本 k = 0.2%。每日对冲 σ_L = 21.2%，每周对冲 σ_L = 20.6%。每周对冲成本低、卖价也低，但对冲误差约大 √5 ≈ 2.2 倍（第9章）。
5. **提前行权。** 看涨期权至少值 S − Ke^{−rT} ≥ S − K，不付股息时永远不应提前行权。看跌期权的下界是 Ke^{−rT} − S，在 r > 0 时小于 K − S：深度实值时提前行权、现在收到行权价并赚取利息，可能更优。r = 0 时看跌期权也不会提前行权：看跌期权提前行权需要正利率。
6. **推导利兰波动率。** 一步内 δΔ ≈ ΓδS = ΓSσ√Δt·Z，期望成本 (k/2)·S·E|δΔ| = (k/2)ΓS²σ√Δt·√(2/π)（k 为双边成本）。除以 Δt 得 ½ΓS²·σk√(2/π)/√Δt，与损益中的方差项 ½ΓS²σ² 同形，并入方差即 σ_L² = σ²(1 + √(2/π)k/(σ√Δt))。
7. **忘掉远期。** 用 F = Se^{bT} 定价的平值远期看涨期权，若用 S 且不计持有成本反解，公式会以为它实值 ln(F/S) = bT，于是用更高的波动率解释价格。一阶近似 δσ ≈ N(d₁)·bT/(φ(d₁)√T) ≈ 0.5 × 0.02/(0.399 × 0.707) ≈ 3.5 个点（b = 4%，T = 0.5，σ = 45%）；看跌期权大致低同样多。精确反解（`carry` 计算项）：看涨 49.0%（+4.0），看跌 41.8%（−3.2），不对称来自二阶项。
8. **（资格考试）退出时间的矩。** 局部地X = σS·W，方差速率v = σ²S²，τ = inf{t: |X_t| = a}。X² − vt是鞅，所以a² = vEτ，Eτ = a²/v。X⁴ − 6vtX² + 3v²t²是鞅（伊藤），所以a⁴ − 6va²Eτ + 3v²Eτ² = 0，Eτ² = 5a⁴/(3v²)，Var τ = 2a⁴/(3v²)。区间内对冲误差为½Γ[(ΔX)² − vτ] = ½Γv(Eτ − τ)，方差Γ²a⁴/6。相同平均长度Δt = a²/v的等时间步误差为½ΓvΔt(Z² − 1)，方差Γ²a⁴/2。
9. **（资格考试）最优带。** 单位时间内误差方差以(1/6)Γ²a²v累积，交易速率为v/a²。拉格朗日函数(1/6)Γ²a²v + λv/a²逐点在a⁴ = 6λ/Γ²处最小，所以a ∝ |Γ|^{−1/2}。取a = c|Γ|^{−1/2}，Var = (c²/6)∫|Γ|v，N = (1/c²)∫|Γ|v，所以N·Var = (1/6)(∫|Γ|v dt)²。由柯西–施瓦茨(∫|Γ|v dt)² ≤ T∫Γ²v²dt，所以N·Var ≤ (1/3)·(T/2)∫Γ²v²，即等时间常数的三分之一。

## 写给研究者

* **定理。** 深泽正彰（2011），《渐近有效的离散对冲》，收于*Stochastic Analysis with Financial Applications*（Birkhäuser）：在停时规则上lim E[N]·E⟨误差⟩ ≥ (1/6)(E∫|Γ|σ²S²dt)²，由带|Δ_t − Δ_τ|² = hΓ_τ达到；罗森鲍姆与坦科夫（2014），*Ann. Appl. Probab.* 24（arXiv:1108.5940），含跳跃。
* **简化。** 单一期权、零利率、首阶（窄带）近似；用E[N]·Var而非深泽的E[N]·E⟨误差⟩；带在2^14步的网格上检验，越界使带略宽。
* **开放问题。** 一整本期权在成本与交易预算下的联合问题；几十次交易时的修正；跳跃、粗糙波动率与多资产。
