# Quant, Built — Part 10: Black–Scholes–Merton

Part 10 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the second part of Act III, Derivatives, and the series' pilot. It shows how an option
can be manufactured from the stock and cash, derives the Black–Scholes–Merton price three ways, takes the hedger's
profit and loss apart term by term, and tests all of it on real markets. Every number is computed by the series' own
code ([`compute.py`](compute.py), the House library in [`explainer/quant/house`](../../../explainer/quant/house))
from public data: Deribit's option trades and DVOL index, Binance's Bitcoin prices, and Kenneth French's US market
returns. Schematics and made-up examples are labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Manufacturing an option.** A real month, October 2021: a 30-day Bitcoin call sold at Deribit's DVOL (89%);
  Bitcoin rises 37%; unhedged the seller loses 27 per 100, hedged every hour the seller makes 1.15 (the median of the
  1,706 months of chapter 11). Implied 89% against realized 61%. Objectives; the House opens its volatility desk.
* **1. Before the formula.** Bachelier (1900); Sprenkle (1961), Boness (1964), Samuelson (1965) and their two
  unknown rates; Thorp and Kassouf (1967) and the warrant hedge; Black and Scholes (1969–73) and Merton (1970–73); the
  CBOE opens (26 April 1973); traders quote volatility; the Nobel (1997).
* **2. The riskless portfolio.** The stock, the bond, the option; Itô's lemma; the delta hedge; μ drops out; no
  arbitrage; the Black–Scholes PDE; the heat-equation picture, run backwards from the payoff.
* **3. The price as an expectation.** Feynman–Kac; the risk-neutral measure (Harrison–Kreps 1979, Harrison–Pliska
  1981); 400,000 outcomes under P (19.74) and Q (12.36 ± 0.03, against the formula's 12.34); Girsanov reweighting;
  the expectation done by hand (the stock as numeraire); N(d₂) as a Q-probability, N(d₁) as delta.
* **4. The tree and its limit.** One period: replication and the risk-neutral probability; a four-step CRR tree
  (prices, values, hedges); convergence for N = 1…400, zigzagging like 1/N.
* **5. The Greeks as geometry.** The value surface in 3D; delta and gamma as time runs out; Θ = −½σ²S²Γ, computed;
  vega = σ(T − t)S²Γ: one bump seen three ways.
* **6. Where the hedger's money comes from.** d(book) = ½ΓS²(σᵢ² − σᵣ²)dt derived; the breakeven move ±σᵢ√dt on a
  real path; the hedging ledger live on three paths (12%, 28%, 20% realized against 20% implied); 20,000-path
  distributions (+1.59, −1.60, +0.00).
* **7. Hedging with the wrong volatility.** P&L = ½∫Γ S²(σᵢ² − σᵣ²)dt (El Karoui, Jeanblanc & Shreve 1998); dollar
  gamma as a heat map; two paths with the same realized volatility and 8× different profits; 4,000 Heston paths:
  P&L against realized vol (ρ = −0.87) and against the gamma-weighted formula (ρ = 0.99).
* **8. Hedging in steps, and paying for it.** The discrete hedging error derived, sd ∝ √Δt, and measured on 20,000
  paths per frequency (slope −0.49); the cost/error trade-off; Leland's volatility, verified: it covers the rebalancing
  costs, and the first hedge and the unwind (0.26) are outside the formula.
* **9. Implied volatility and the first smile.** The solver on a real Deribit quote; the smiles of 10 December 2025;
  the Surface in 3D (254 quotes); the Surface's first row: Black–Scholes with one vol per expiry, 4.36 vol points in
  sample, 4.74 the next day.
* **10. Early exercise.** Calls are never exercised early (no dividends); the American put on a 2,000-step tree
  (6.0900 against the European 5.5735); the free boundary.
* **11. Selling volatility on real Bitcoin.** 1,706 thirty-day calls sold at DVOL from April 2021 and hedged every hour:
  mean +1.35 per 100, 81% winning months, ρ = 0.86 with the volatility gap; the ledger explains every month; costs and
  the DVOL–at-the-money gap; the worst month, July–August 2024 (sold at 47%, realized 64%).
* **12. October 1987.** Portfolio insurance as replicated puts; the crash in Kenneth French's daily data (−17.4%);
  −20.7σ, a Gaussian waiting time of 10⁹² years against 60 years under the fitted power tail (α = 2.71); the skew.
* **13. The Nobel, and then LTCM.** The 1997 prize; Long-Term Capital Management's trades, leverage and 1998; the
  rescue; what every hedge assumes.
* **Recap, desk questions, problems.**

## Build it

The finished video is not stored in the repository. From the repo root, after the setup in the
[top-level README](../../../README.md#setup) (or `bash tools/setup_linux.sh`):

```bash
python -m explainer.quant.data                    # the market data, fetched once and checksummed (~2 min)
python -m videos.quant.quant10.compute            # every computed item (~8 min; cached in .cache/quant10)
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
   gamma is smaller (chapter 7).
4. **Leland.** σ_L² = σ²(1 + √(2/π) k / (σ√Δt)) with round-trip cost k = 0.2%. Daily (Δt = 1/252): σ_L = 21.2%;
   weekly (Δt = 1/52): σ_L = 20.6%. Weekly hedging is cheaper to sell, because it trades less, but its hedging error
   is about √5 ≈ 2.2 times larger (chapter 8).
5. **Early exercise.** A call is worth at least S − K e^{−rT} ≥ S − K, so it is always worth at least as much alive as
   exercised, and strictly more when r > 0: never exercise early without dividends. A put is worth at least
   K e^{−rT} − S, which is less than K − S when r > 0: exercising a deep put can win, because the strike received now
   earns interest. At r = 0 that bound is K − S itself, so the put is never exercised early either: early exercise
   of a put requires a positive interest rate.

## Data and reproducibility

* Deribit option trades of 10 and 11 December 2025, 00:00–12:00 UTC (6,060 and 7,843 trades) from
  `history.deribit.com`; DVOL hourly, April 2021 – December 2025; Binance BTCUSDT hourly candles; Kenneth French's
  daily factors through 2025. Each raw piece's SHA-256 is in [`../data/manifest.json`](../data/manifest.json).
* Seeds are fixed in every compute item. The BTC experiment's months overlap; chapter 11 also reports the statistic on
  57 non-overlapping months.

---

# 量化金融，从零搭建 — 第10部分：Black–Scholes–Merton

本系列共四十三部分（见[系列计划](../README.md)与[教学大纲](../SYLLABUS.md)），这是第三幕“衍生品”的第二部分，也是系列的试点。
本部分说明期权如何用股票和现金“制造”出来，用三种方法推导 Black–Scholes–Merton 价格，逐项拆解对冲者的损益，并全部在真实市场数据上检验。
所有数字均由本系列自己的代码（[`compute.py`](compute.py) 与 House 库 `explainer/quant/house`）根据公开数据计算：Deribit 的期权成交与 DVOL 指数、Binance 的比特币价格、Kenneth French 的美国市场收益。示意图和虚构例子在画面上均有标注。

*本视频讲授方法，不构成投资建议。*

## 交易台问题与解答

1. **一年期平值看涨期权，波动率 20%，现价 100，利率为零：心算价格。** 平值时 d₁ = σ√T/2 很小，C ≈ Sφ(0)σ√T ≈ 0.4 × 0.2 × 100 = 8；公式给出 7.97。
2. **你持有平值跨式组合，股价一周不动，赚了还是亏了？** 亏了：多头跨式是多 gamma、空 theta；价格不动时 gamma 一分不赚，theta 却照付。一个月期、20% 波动率、标的 100 的跨式，一周约亏 0.53（两倍看涨期权的 theta）。
3. **临近到期时平值数字期权的 delta。** 数字期权的 delta 是风险中性密度在行权价处的值 φ(d₂)/(Sσ√τ)，按 1/√τ 增长；微小的价格变动就会让对冲在“零”和“大量持仓”之间翻转。实务中交易台用很窄的看涨价差来超额对冲，并为此收费。

## 习题与解答

1. **平价关系与 delta。** 利用 N(x) + N(−x) = 1，C − P = S − Ke^{−rT}。对 S 求导，括号项 Sφ(d₁) − Ke^{−rT}φ(d₂) 因 φ(d₂) = φ(d₁)Se^{rT}/K 而为零，故 Δ = N(d₁)。
2. **二叉树的概率。** quS + (1 − q)dS = Se^{rΔt}，股票平均以 r 增长，贴现后的价格是鞅。r = 0 时 q = ½ − σ√Δt/4 + O(Δt) → ½。
3. **波动率交易员的估算。** r = 0 且无漂移时，以 σᵢ 卖出并对冲、股票实际波动率为 σᵣ，期望对冲损益恰为 C(σᵢ) − C(σᵣ)。三个月平值、25% 对 20%：4.98 − 3.99 = 1.00（每 100 名义），约等于 vega × (σᵢ − σᵣ) = 19.9 × 0.05。若把 gamma 固定在平值处，½(σᵢ² − σᵣ²)∫ΓS²dt 给出 1.79，偏高：真实路径会离开行权价，那里的 gamma 更小（第7章）。
4. **Leland。** σ_L² = σ²(1 + √(2/π)·k/(σ√Δt))，双边成本 k = 0.2%。每日对冲 σ_L = 21.2%，每周对冲 σ_L = 20.6%。每周对冲成本低、卖价也低，但对冲误差约大 √5 ≈ 2.2 倍（第8章）。
5. **提前行权。** 看涨期权至少值 S − Ke^{−rT} ≥ S − K，不付股息时永远不应提前行权。看跌期权的下界是 Ke^{−rT} − S，在 r > 0 时小于 K − S：深度实值时提前行权、现在收到行权价并赚取利息，可能更优。r = 0 时看跌期权也不会提前行权：看跌期权提前行权需要正利率。
