# Quant, Built — Part 6: Financial Econometrics

Part 6 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. It is about learning from the one history we
have without fooling ourselves:

* overlapping observations and HAC standard errors;
* predictive regressions and Stambaugh's bias;
* GMM and the consumption Euler equation;
* event studies;
* panel standard errors;
* the bootstrap for dependent data and the signal-to-noise problem;
* shrinkage and multiple testing;
* causal designs and double machine learning.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`econ`](../../../explainer/quant/house/econ.py) module, tested) from public data: Robert Shiller's monthly market
data, Kenneth French's factors and 49 industries, and FRED's consumption and prices. Simulations are seeded and
labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 40 minutes)

* **One regression, five verdicts.** Does an industry's past year (months t−12 to t−2) predict its next month?
  The test uses French's 49 industries, 1928–2020, 51,858 industry-months. The t-statistics are:
  * pooled OLS: 1.86;
  * clustered by industry: 1.21;
  * clustered by month: 0.27;
  * two-way clustered: 0.27;
  * Fama–MacBeth: 5.08, with a slope eight times larger (0.0170 against 0.0022).

  Then the objectives, and the House's statistics module.
* **1. Overlapping data and predictive regressions.** Five-year real returns on the log dividend yield (Shiller,
  1871–2020, 1,739 overlapping windows) give a naive t of 15.0, Newey–West 2.8 and Hansen–Hodrick 2.5. In 400
  simulated null worlds, with a predictor as persistent as the yield (monthly ρ = 0.99), the false-rejection rates
  are 77%, 17% and 14%. Stambaugh's bias, simulated at ρ = 0.92 and corr(u, v) = −0.75, averages +0.056 at 50 years
  and +0.018 at 150. The annual dividend-yield regression, 1871–2020, has ρ = 0.91, corr = −0.83 and
  β = 0.034 (t = 1.1), which is 0.016 after the bias correction.
* **2. GMM and the consumption Euler equation.** Hansen's GMM and J test, applied to real PCE per capita (FRED), the
  market and the T-bill (French), quarterly 1947–2020, with instruments a constant, lagged consumption growth and the
  lagged market return:
  * β = 1.002 (0.009) and γ = 1.1 (1.5);
  * J = 20.0 on 4 df, p = 0.0005: the model is rejected;
  * a quarterly equity premium of 2.1% against consumption growth with sd 1.1% and correlation 0.06 with stocks,
    which would need γ ≈ 421 (Mehra and Prescott 1985).
* **3. Event studies and panels.** The turn of the month, days −1 to +3 (about 18% of trading days), carried 74% of
  the market's return in 1926–1986 (t = 7.4) and 45% in 1987–2020 (t = 2.6). Then the panel puzzle resolved: the
  common monthly shock (Petersen 2009), and why pooled OLS and Fama–MacBeth estimate different weighted slopes.
* **4. The bootstrap and the signal-to-noise problem.** The US market's annual Sharpe ratio, 1926–2020, is 0.44.
  Its standard error is 0.103 by the iid formula (Lo), 0.104 with fat tails (Mertens), 0.119 by block bootstrap and
  0.122 by stationary bootstrap. Years for an expected t of 2: 16 at a Sharpe of 0.5, and 4 at 1. The chance a
  strategy looks worse than zero after five years is 13% at a Sharpe of 0.5 and 29% at 0.25. Tobacco against the
  market: 95% (α, β) regions over 5, 20 and 60 years.
* **5. Many assets, many tests.** 40 industries with full histories: means estimated on 1927–1973 and scored on
  1974–2020. Empirical-Bayes shrinkage estimates the between-industry spread at zero, and the grand mean halves the
  error (8.0 → 3.8, in squared percent a year). Then the CAPM alphas of the 49 industries: 5 have p < 0.05 (food,
  tobacco, medical equipment and drugs positive; steel negative), and none survives Bonferroni, Holm or
  Benjamini–Hochberg. Of 1,000 pure-noise strategies, 50 pass at 5% and none after BH.
* **6. Causal inference.** Instruments, difference in differences, and regression discontinuity (the Russell
  1000/2000 boundary), shown as schematics. Double ML on a planted effect of 0.3, over 60 samples of 4,000: it
  recovers 0.300 ± 0.018, where OLS with linear controls gives 1.15.
* **7. The statistics module.** Rule 7: no number leaves the House without a standard error that respects how the data
  were sampled, and the count of everything tried. The trial counter reads 63.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant6.compute                    # every number, cached in .cache/quant6/ (about a minute)
EXPLAINER_TTS=silent python tools/qa_scene.py quant6 Many     # one chapter, silent, with a contact sheet
python tools/make.py quant6 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Sharpe 1 over 4 years.** For iid normal returns, se(SR) ≈ √((1 + SR²/2)/T) = √(1.5/4) ≈ 0.61 in annual units.
   The 95% interval is about 1 ± 1.2: the data cannot tell this strategy from one with no edge.
2. **The best of 20 has p = 0.03.** If all 20 are worthless and independent, the chance that at least one has
   p ≤ 0.03 is 1 − 0.97²⁰ ≈ 46%. Bonferroni requires p < 0.05/20 = 0.0025. Correlated strategies reduce the effective
   number of tests, but the count of tries must be reported either way.
3. **Annual returns sampled monthly over 40 years.** There are 480 regression rows, but each annual return shares 11
   months with its neighbour, so there are about 40 independent observations. Use Newey–West (12+ lags) or
   Hansen–Hodrick (11 lags) errors. Chapter 1's simulation shows they still over-reject with a persistent predictor.

## Problems, with solutions

1. **The cost of overlap.** With y_t = Σ_{j=1}^{h} ε_{t+j} and a predictor that barely changes, the regression
   residuals are close to y_t itself. Neighbouring y_t share h − k shocks at lag k, so their autocorrelation is
   (h − k)/h. The variance of the slope's sampling error is inflated by Σ_{|k|<h}(1 − |k|/h) = h relative to the
   naive formula, so the naive standard error is too small by about √h: √60 ≈ 7.7 for five-year returns sampled
   monthly. Compare 15.0 against 2.8 in chapter 1.
2. **Stambaugh's bias.** With r_{t+1} = a + βx_t + u and x_{t+1} = c + ρx_t + v, write u = (σ_uv/σ_v²)v + e, with e
   independent of v. OLS gives β̂ − β = (σ_uv/σ_v²)(ρ̂ − ρ) + noise with mean zero, and Kendall's
   E[ρ̂ − ρ] ≈ −(1 + 3ρ)/T. So E[β̂ − β] ≈ −(σ_uv/σ_v²)(1 + 3ρ)/T. For annual dividend yields, ρ = 0.91, T = 149,
   σ_u = 0.167, σ_v = 0.192 and corr = −0.83 give σ_uv/σ_v² = −0.72 and a bias of +0.72 × 3.72/149 = +0.018.
3. **The Sharpe ratio's standard error.** SR̂ = μ̂/σ̂. With iid normal returns, Var(μ̂) = σ²/T, Var(σ̂) ≈ σ²/(2T),
   and the two are independent. The delta method gives Var(SR̂) ≈ (1/σ²)(σ²/T) + (μ²/σ⁴)(σ²/(2T)) = (1 + SR²/2)/T.
   Fat tails add (κ − 3)SR²/4 and skewness −γ SR (Mertens 2002).
4. **Holm.** Order the p-values p₍₁₎ ≤ … ≤ p₍ₘ₎ and reject while p₍ᵢ₎ ≤ α/(m − i + 1). Suppose there are m₀ true nulls
   and Holm makes a false rejection. At the first one, at least m₀ hypotheses are not yet rejected, so its threshold
   is at most α/m₀. Therefore P(any false rejection) ≤ P(min over true nulls of p ≤ α/m₀) ≤ α, by Bonferroni over
   the m₀ nulls. Every threshold α/(m − i + 1) is at least α/m, so Holm rejects at least what Bonferroni rejects.
5. **James–Stein.** For x ~ N(μ, I_k), Stein's lemma gives the risk of (1 − (k − 2)/‖x‖²)x as
   k − (k − 2)² E[1/‖x‖²] < k, which is the risk of x itself. Shrinking toward the grand mean x̄ spends one degree of
   freedom on estimating the target, so the factor becomes (k − 3)/‖x − x̄‖², which needs k ≥ 4. With 40 industries
   and an estimated spread of zero, the empirical-Bayes version shrinks all the way.

## Data and reproducibility

* Robert Shiller's `ie_data.xls`, monthly 1871–2020 (real total returns, dividend yields).
* Kenneth French's monthly factors (`F-F_Research_Data_Factors`) and `49_Industry_Portfolios`, value-weighted,
  through December 2020. The hold-out from 2021 is sealed.
* FRED: real PCE per capita (A794RX0Q048SBEA, hold-out sealed) and CPIAUCSL.
* Registered with the trial counter: the industry-momentum panel (1), the turn-of-the-month event study (1) and the
  49 industry alphas (49).

---

# 量化金融，从零搭建 — 第6部分：金融计量经济学

本部分讲如何从我们仅有的一段历史中学习而不自欺：重叠观测与HAC标准误、预测回归与Stambaugh偏差、GMM与消费欧拉方程、事件研究、面板标准误、
相依数据的自助法与信噪比问题、收缩与多重检验，以及因果设计与双重机器学习。所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **四年夏普比率为1。** 对独立正态收益，se(SR) ≈ √((1 + SR²/2)/T) = √(1.5/4) ≈ 0.61（年化）。95%区间约为1 ± 1.2：数据无法把这个策略
   与毫无优势的策略区分开。
2. **20个策略中最好的p = 0.03。** 如果20个都毫无价值且相互独立，至少一个的p ≤ 0.03的概率是1 − 0.97²⁰ ≈ 46%。邦费罗尼要求
   p < 0.05/20 = 0.0025。策略之间的相关性会减少有效检验次数，但无论如何都必须报告尝试了多少次。
3. **40年按月采样的年度收益。** 回归有480行，但每个年度收益与相邻的共享11个月：大约只有40个独立观测值。使用Newey–West（12个以上的滞后）
   或Hansen–Hodrick（11个滞后）标准误；第1章的模拟表明，面对持续性预测变量它们仍会过度拒绝。

## 习题与解答

1. **重叠的代价。** y_t = Σ_{j=1}^{h} ε_{t+j}，预测变量几乎不变时残差接近y_t本身；相邻的y_t在滞后k处共享h − k个冲击，自相关为(h − k)/h。
   斜率抽样误差的方差相对朴素公式被放大Σ_{|k|<h}(1 − |k|/h) = h倍，所以朴素标准误小了约√h倍：按月采样的五年期收益为√60 ≈ 7.7
   （对比第1章的15.0与2.8）。
2. **Stambaugh偏差。** 设r_{t+1} = a + βx_t + u，x_{t+1} = c + ρx_t + v，写u = (σ_uv/σ_v²)v + e，e与v独立。OLS给出
   β̂ − β = (σ_uv/σ_v²)(ρ̂ − ρ) + 均值为零的噪声，而Kendall的E[ρ̂ − ρ] ≈ −(1 + 3ρ)/T。所以E[β̂ − β] ≈ −(σ_uv/σ_v²)(1 + 3ρ)/T。
   年度股息率：ρ = 0.91，T = 149，σ_u = 0.167，σ_v = 0.192，相关系数−0.83，得σ_uv/σ_v² = −0.72，偏差+0.72 × 3.72/149 = +0.018。
3. **夏普比率的标准误。** SR̂ = μ̂/σ̂。独立正态收益下Var(μ̂) = σ²/T，Var(σ̂) ≈ σ²/(2T)，且两者独立；由delta方法，
   Var(SR̂) ≈ (1 + SR²/2)/T。厚尾加上(κ − 3)SR²/4，偏度加上−γ SR（Mertens 2002）。
4. **Holm方法。** 把p值排序，只要p₍ᵢ₎ ≤ α/(m − i + 1)就继续拒绝。设有m₀个真实原假设；如果Holm出现错误拒绝，在第一次错误拒绝时至少还有m₀个
   未被拒绝，所以阈值至多为α/m₀；因此P(任何错误拒绝) ≤ P(真实原假设中最小的p ≤ α/m₀) ≤ α。每个阈值都不小于α/m，所以Holm拒绝的至少与
   邦费罗尼一样多。
5. **James–Stein。** 对x ~ N(μ, I_k)，由Stein引理，(1 − (k − 2)/‖x‖²)x的风险为k − (k − 2)² E[1/‖x‖²] < k，即x本身的风险。
   向总均值x̄收缩要用掉一个自由度去估计目标：系数变为(k − 3)/‖x − x̄‖²，需要k ≥ 4。对40个行业、估计的差异为零时，经验贝叶斯版本会完全收缩。
