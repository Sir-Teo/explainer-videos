# Quant, Built — Part 1: The Fair Game

Part 1 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the first part of Act I, Markets and Money. It asks how well a game of pure chance
describes prices, and measures the answer on ninety-four years of the US stock market, on Bitcoin, and on one morning
of Bitcoin options. Every number is computed by the series' own code ([`compute.py`](compute.py), the House library in
[`explainer/quant/house`](../../../explainer/quant/house)) from public data: Kenneth French's daily market and
size-decile returns, Binance's Bitcoin prices, and Deribit's option trades (the Surface). Statistics of stocks and
Bitcoin use data up to 31 December 2020 only: the later years are sealed (chapter 14). Schematics and simulations
are labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 53 minutes)

* **Which one is real?** Four one-year charts: three Gaussian random walks with the market's mean and volatility, and
  the US market in 1997. The charts look alike; the daily returns don't: 27 October 1997, −6.6%, a 6.8σ day that a
  bell curve expects once in 5×10⁸ years. Objectives; the House opens its data desk.
* **1. Paris, 1863 and 1900.** Regnault's square-root-of-time law (1863); Bachelier's thesis (1900, graded
  *honorable*); Savage's postcards and Samuelson (1950s). Regnault's law on 98 one-year stretches since 1926, and on
  log scales: slope 0.52 for the US market (1 day to 2 years), 0.50 for Bitcoin; a year's spread 13% above the daily
  extrapolation.
* **2. Prices, returns and the drag.** Simple and log returns; +50% then −50%; 94 calendar years: arithmetic mean
  11.95%, geometric 10.02%, gap 1.93% against ½σ² = 1.97%; the lognormal derivation; daily-rebalanced leverage since
  1926: $1 became $8,642 (1×), $209,604 (2×), $255,193 (3×, after losing 98.7% by July 1932); growth is a parabola in
  leverage with its peak at (μ − r)/σ² ≈ 2.6 (Kelly, Part 8).
* **3. The random walk.** Cowles (1933), Kendall (1953), Osborne (1959); Samuelson's proof (1965) by the tower
  property; a fair price at work (twenty coin tosses); martingale against random walk.
* **4. Testing the walk.** Autocorrelation and the variance ratio, VR(q) = 1 + 2Σ(1 − k/q)ρₖ; Lo and MacKinlay
  (1988) replicated on French's size deciles over their exact sample (6 Sept 1962 – 26 Dec 1985, 1,215 weeks): the
  smallest decile's weekly autocorrelation +0.35, VR(16) = 2.57, z* ≈ 9–11; the largest decile a random walk;
  1986–2020: +0.16 for small stocks, about zero or negative elsewhere; in rolling five-year windows the small-stock
  echo survives publication and collapses in the mid-2000s (decimal prices, Reg NMS, electronic trading).
* **5. Heavy tails.** 24,896 days on a log-density scale; excess kurtosis 17.7; days beyond 5σ: 101 seen against
  0.014 expected (beyond 10σ: 5 against 4×10⁻¹⁹); the tail on log-log axes, slope about −3 (Gopikrishnan, Meyer,
  Amaral and Stanley 1998); Hill estimates: α = 2.89 (both tails), 2.84 (losses), Bitcoin 3.7, and 3.96 after scaling
  by recent volatility.
* **6. Volatility clusters.** 94 years of daily returns and monthly volatility; autocorrelations to a year: returns
  ≈ 0 (ρ₁ = +0.05), absolute returns 0.31 at a day and 0.12 at a year, decaying like k^−0.23, gone when the days are
  shuffled; Bitcoin's shorter memory; the leverage effect (corr(rₜ, |rₜ₊ₖ|) ≈ −0.10 for k = 1…5, ≈ 0 backwards;
  Black 1976).
* **7. Slower clocks, thinner tails.** Daily, monthly and yearly return shapes; kurtosis 17.7 → 6.7 → 2.8 (half a
  year), slower than independence would allow; without 19 October 1987 the daily kurtosis is 14.1.
* **8. Does the variance exist?** Mandelbrot (1963) and stable laws; running standard deviations (US market, bell
  curve, Student t(3), Cauchy); running kurtosis jumps in 1987; one day carries 19% of 94 years' fourth-power mass.
* **9. Efficient markets.** Fama (1970), the three forms and the joint-hypothesis problem; Grossman and Stiglitz
  (1980); Black's "Noise" (1986); Martin and Nagel (2022) as a simulation: 500 stocks, 200 characteristics, Bayesian
  investors, prices efficient by construction; an in-sample test rejects in 64% of 300 markets (nominal 5%); the
  out-of-sample R² is negative in all of them (median −7.3%).
* **10. Two worlds, P and Q.** P and Q defined; the Surface's 51-day BTC smile and an SVI curve through it;
  Breeden–Litzenberger (1978); the Q density against 51-day returns of the four years before (Q: mean 0, spread
  17.6%, P(−20% or worse) 10.1%; P: +5.1%, 21.3%, 7.9%); Martin's (2017) bound: var^Q(S_T/F) = 3.11% over 51 days, at
  least 22% a year of expected excess return if his condition holds.
* **11. Who is on the other side?** Hedgers, speculators, market makers, arbitrageurs; Sharpe's arithmetic of
  active management (1991); the industry firm file (market makers and proprietary traders, systematic funds,
  multi-manager platforms, banks and asset managers), from the public record.
* **12. Beating the dealer.** The doubling system (3,000 sessions; ruin 0.10%, mean −0.02 ± 0.07 over 200,000);
  the optional stopping theorem and three stopping rules; Thorp's card counting (six-deck shoes, Hi-Lo true
  counts: 27% of hands favour the player; flat bets −0.50%, bets of 1–8 by count +0.08% of the money bet); Princeton
  Newport Partners (19.1% before fees, 15.1% after, against 10.2% for the S&P 500, 1969–1988, as Thorp reports).
* **13. March 2020.** The crisis file: the US market on 16 March 2020 (−12.0%, 8.7σ against its own past year;
  3×10¹⁵ years under a bell curve, about 23 under the fitted tail) and Bitcoin on 12 March (−39.5%, 13.9σ; about 12
  years under its own tail).
* **14. The House opens.** The data layer; rule 1, point in time; rule 2, the sealed envelope (research to 2020,
  2021–2025 sealed with recorded SHA-256 digests in [`../data/envelope.json`](../data/envelope.json)); the trial
  counter at 0.
* **Recap, desk questions, problems.** Ten lines; three desk questions; five problems; where this comes back;
  references; the House and the series map.

## Build it

```bash
python -m videos.quant.quant1.compute                     # every number, cached in .cache/quant1/ (~6 min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant1 Tails   # one chapter, silent, with a contact sheet
python tools/make.py quant1 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
python tools/make.py quant1                               # the production voice (README, "Narration")
```

The Martin–Nagel item (`nagel`) is the slow one: 300 simulated markets, about five minutes.

## Desk questions, with solutions

1. **The St Petersburg game.** The payout 2ⁿ comes with probability 2⁻ⁿ, so the expectation is Σₙ 2⁻ⁿ2ⁿ = Σ 1 = ∞.
   Nobody pays more than a few dollars: payouts beyond what any counterparty could pay are not real, and people value
   wealth by its logarithm. With log utility (Daniel Bernoulli, 1738) and nothing else at stake, the game's
   certainty equivalent solves ln c = Σₙ 2⁻ⁿ ln 2ⁿ = ln 2 · Σₙ n2⁻ⁿ = 2 ln 2, so c = $4.
2. **Up or down 50%, forever.** Each year multiplies wealth by 1.5 or 0.5: the mean factor is 1, so expected wealth
   stays at its start forever. But log wealth is a random walk with drift ½ ln 1.5 + ½ ln 0.5 = ½ ln 0.75 ≈ −0.144 a
   year, so the median path falls by about 13% a year and goes to zero; the expectation is carried by vanishingly rare
   paths. A good investment for nobody who lives on one path: chapter 2's drag, ½σ² with σ = 50%.
3. **Two heads in a row.** Let E be the expected number of tosses. The first toss is a tail (prob ½): start again,
   E + 1. Heads then tails (prob ¼): start again, E + 2. Heads, heads (prob ¼): done in 2. So E = ½(E + 1) + ¼(E + 2)
   + ¼ · 2, giving E = 6. (For a head then a tail, HT, the answer is 4: patterns that overlap themselves take longer.)

## Problems, with solutions

1. **Fair prices are martingales.** Eₜ[Pₜ₊₁] = Eₜ[Eₜ₊₁[X]] = Eₜ[X] = Pₜ by the tower property. For s < t, the
   increments satisfy E[(Pₜ₊₁ − Pₜ)(Pₛ₊₁ − Pₛ)] = E[(Pₛ₊₁ − Pₛ) Eₜ[Pₜ₊₁ − Pₜ]] = 0, so they are uncorrelated. They need
   not be independent: let εₜ be fair coin flips (±1) and Pₜ₊₁ = Pₜ + σₜ εₜ₊₁ with σₜ = 1 + |Pₜ − P₀|/10: every increment
   has mean zero given the past, but its size depends on the path so far (volatility clustering, chapter 6).
2. **The lognormal means.** If r = ln(1 + R) ~ N(m, s²), then E[1 + R] = E[eʳ] = e^{m + s²/2}, the lognormal mean,
   so the arithmetic mean simple return is e^{m+s²/2} − 1; a dollar invested for T periods grows like e^{Σr}, whose
   per-period growth is e^m − 1, the geometric mean. With chapter 2's numbers, e^m − 1 = 10.02% gives m = 9.55%, and
   e^{m+s²/2} − 1 = 11.95% gives s = 18.6%, close to the 19.9% standard deviation of the simple annual returns (the
   two measure slightly different things: log against simple returns, and real years aren't exactly lognormal).
3. **The variance ratio.** For a stationary series with variance σ² and autocorrelations ρₖ,
   Var(r₁ + … + r_q) = qσ² + 2σ² Σ_{k=1}^{q−1} (q − k)ρₖ (each lag k appears q − k times). Divide by qσ²:
   VR(q) = 1 + 2Σ_{k<q}(1 − k/q)ρₖ; for q = 2, VR(2) = 1 + ρ₁.
4. **Hill's estimator.** With P(X > x) = (x/x_m)^−α, Y = ln(X/x_m) has P(Y > y) = e^{−αy}: exponential with mean
   1/α. Hill's estimator is this, with x_m the (k+1)-th largest value and the k largest as the sample: α̂ = (mean of
   ln(X₍ᵢ₎/X₍ₖ₊₁₎))⁻¹. With α = 3, E|X|ᵖ is finite only for p < 3: the mean and variance exist, the third moment
   barely does not, and the fourth (kurtosis) is infinite, which is why chapter 8's running kurtosis never settles.
5. **The best leverage.** A fund holding L times the market, rebalanced continuously and borrowing at r, has
   instantaneous return r + L(μ − r) and variance L²σ², so its growth rate is g(L) = r + L(μ − r) − ½L²σ². Then
   g′(L) = 0 gives L* = (μ − r)/σ², the Kelly leverage, and g(L*) = r + (μ − r)²/(2σ²). From the daily data of
   1926–2020: μ = 10.6%, r = 3.0%, σ = 17.1% a year, so L* = 2.62 and g(L*) = 13.0% a year, against 9.2% at L = 1;
   growth falls back to the unlevered level at L = 2L* − 1 ≈ 4.2 and is negative beyond (μ − r + √((μ − r)² + 2rσ²))/σ²
   ≈ 5.6. Real funds pay fees and borrow above the bill rate, which moves the peak down.

## Data and reproducibility

* Kenneth French's data library: the daily Fama–French factors (the market is Mkt−RF + RF) and the daily
  value-weighted size-decile portfolios (NYSE breakpoints), frozen through 31 December 2025, checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Binance's public archive: BTC/USDT daily candles from 17 August 2017.
* Deribit's public history: every BTC option trade of 10 December 2025, 00:00–12:00 UTC (the Surface).
* The research window ends on 31 December 2020; the digests of 2021–2025 are in
  [`../data/envelope.json`](../data/envelope.json).
* Simulations are seeded; every render on any machine shows the same numbers.

---

# 量化金融，从零搭建 — 第1部分：公平的赌局

本系列量化金融课程共43部分，这是第一幕“市场与货币”的第一部分。它问的是：一场纯粹的机会游戏，能在多大程度上描述价格？
答案在94年的美国股市、比特币以及一天上午的比特币期权上测量出来。所有数字都由本系列自己的代码根据公开数据算出。股票和比特币的
统计只使用2020年12月31日之前的数据，之后的年份被封存（第14章）。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **圣彼得堡游戏。** 收益2ⁿ出现的概率是2⁻ⁿ，期望是Σₙ 2⁻ⁿ2ⁿ = ∞。可是没有人愿意付超过几美元：超出任何对手方支付能力的收益并不
   真实，而且人们按对数来衡量财富。用对数效用（丹尼尔·伯努利，1738），且没有其他财富时，确定性等价满足
   ln c = Σₙ 2⁻ⁿ ln 2ⁿ = 2 ln 2，所以c = 4美元。
2. **永远上涨或下跌50%。** 每年财富乘以1.5或0.5，平均乘数是1，所以期望财富永远不变。但对数财富是一个漂移为
   ½ ln 1.5 + ½ ln 0.5 = ½ ln 0.75 ≈ −0.144的随机游走：中位数路径每年下跌约13%，最终归零，期望全靠极其罕见的路径撑着。
   这就是第2章的拖累，½σ²，σ = 50%。
3. **连续两次正面。** 设期望投掷次数为E。第一次是反面（概率½）：重新开始，E + 1。正面后反面（概率¼）：重新开始，E + 2。
   两次正面（概率¼）：2次结束。E = ½(E + 1) + ¼(E + 2) + ¼ · 2，解得E = 6。（“正反”的答案是4：会和自身重叠的模式要等更久。）

## 习题与解答

1. **公平价格是鞅。** 由塔性质，Eₜ[Pₜ₊₁] = Eₜ[Eₜ₊₁[X]] = Eₜ[X] = Pₜ。对s < t，
   E[(Pₜ₊₁ − Pₜ)(Pₛ₊₁ − Pₛ)] = E[(Pₛ₊₁ − Pₛ) Eₜ[Pₜ₊₁ − Pₜ]] = 0，所以增量不相关。但不必独立：令εₜ为公平硬币（±1），
   Pₜ₊₁ = Pₜ + σₜ εₜ₊₁，σₜ = 1 + |Pₜ − P₀|/10：每个增量在给定过去时均值为零，但大小取决于此前的路径（第6章的波动率聚集）。
2. **对数正态的两种平均。** 若r = ln(1 + R) ~ N(m, s²)，则E[1 + R] = e^{m + s²/2}，算术平均简单收益为e^{m+s²/2} − 1；
   一美元按e^{Σr}增长，每期增长率为e^m − 1，即几何平均。用第2章的数字：e^m − 1 = 10.02%得m = 9.55%，
   e^{m+s²/2} − 1 = 11.95%得s = 18.6%，与年度简单收益的标准差19.9%接近。
3. **方差比。** 对方差为σ²、自相关为ρₖ的平稳序列，Var(r₁ + … + r_q) = qσ² + 2σ² Σ_{k=1}^{q−1} (q − k)ρₖ。
   除以qσ²得VR(q) = 1 + 2Σ_{k<q}(1 − k/q)ρₖ；q = 2时VR(2) = 1 + ρ₁。
4. **希尔估计量。** 若P(X > x) = (x/x_m)^−α，则Y = ln(X/x_m)服从均值为1/α的指数分布。希尔估计量就是以第k+1大的值为x_m、
   以最大的k个值为样本的这个估计。α = 3时，只有p < 3阶的矩有限：均值和方差存在，四阶矩（峰度）无穷大，
   所以第8章的滚动峰度永远不会稳定。
5. **最优杠杆。** 持有L倍市场、连续再平衡、按r借款的基金，增长率为g(L) = r + L(μ − r) − ½L²σ²。令g′(L) = 0得
   L* = (μ − r)/σ²，即凯利杠杆，g(L*) = r + (μ − r)²/(2σ²)。用1926–2020年的日数据：μ = 10.6%，r = 3.0%，σ = 17.1%，
   L* = 2.62，g(L*) = 13.0%，而L = 1时为9.2%；L ≈ 4.2时增长率回落到不加杠杆的水平，约5.6倍以上为负。
   真实基金要付费用，借款利率高于国库券利率，会把峰值往下推。
