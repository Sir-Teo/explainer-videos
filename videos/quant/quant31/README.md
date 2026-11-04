# Quant, Built — Part 31: Risk Models, Costs and Trading Through Time

Part 31 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act V, Portfolios, Strategies and the Firm (30–38), built to the
series' PhD layer. Part 30 chose weights once from estimated means and covariances. This part makes that real:

* the covariance comes from a factor risk model;
* the weights must be traded, and trading costs money;
* the forecasts move while you trade toward them.

Its universe is Part 29's: every Binance USDT coin with 60 days of history and enough volume. Research uses
2018–2020; 2021–2025 is sealed. August 2007 is replayed on Kenneth French's daily industry portfolios. It covers:

* **The fundamental law** (Grinold): IR = IC√BR derived; the transfer coefficient (Clarke, de Silva and Thorley); and
  effective and time breadth.
* **A Barra-style factor risk model of the coins:**
  * standardised style exposures and daily weighted cross-sectional regressions;
  * an EWMA factor covariance and specific variances shrunk toward their peers;
  * Barra's bias statistic, industries and their constraint, and the three kinds of factor model.
* **Betas:** Blume's regression toward one, Vasicek's Bayesian betas scored on the next quarter, and Dimson's
  non-synchronous correction.
* **Transaction costs:**
  * implementation shortfall (Perold) and the square-root law of impact;
  * AQR's measured costs (Frazzini, Israel and Moskowitz) and anomalies after costs (Novy-Marx and Velikov);
  * a capacity curve, and the cube-root no-trade band.
* **Trading through time:**
  * Garleanu and Pedersen's aim portfolio and trade rate, derived and checked against value iteration, then traded on
    the coins against a myopic trader;
  * multi-period convex optimisation (Boyd et al.), with a horizon experiment.
* **Alpha combination:** equal, IC-weighted and ridge weights, horizons, and forecast against portfolio blending.
* **Capacity:** decay → turnover → capacity; the profit-maximising size (4/9 of break-even); and Berk and Green, with
  the square-root law (fee = a/3).
* **Crowding:** August 2007 (Khandani and Lo's contrarian strategy replayed), the unwind hypothesis, the risk model's
  blind spot, and comomentum.
* **P&L attribution:** factor against specific, Brinson, timing against static, and the Euler risk decomposition;
  Part 29's mined alpha is 86% factor.
* **For the researcher:** the information ratio when the IC moves. The theorem is proved, simulated and measured; the
  breadth at which more assets stop helping; and the ladder of corrections (moving IC, fat tails) that takes the law's
  promise to what the coins paid. Open problems close the chapter.
* **The registered rule:** the aim-portfolio trader registered and opened on 2021–2025. It failed, through forecast
  variances near zero; the diagnosis follows, and the House adds two guards.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`riskmodel`](../../../explainer/quant/house/riskmodel.py) module). Data: Binance's public daily klines, via Part 29's
eligible universe, and Kenneth French's data library (49 daily industry portfolios).

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: three point nine, or one point six** (3.1).
  * IC 0.05, 500 stocks, monthly: the law promises 3.87; with an IC standard deviation of 0.10, 1.58.
  * Where the information ratio goes: the moving IC, costs (calm-coin Sharpe 1.27 gross, 0.68 at $100k, −0.31 at $1m),
    and the risk model.
  * Act V; fifty years of holding a forecast; the plan.
* **1. The fundamental law** (3.1).
  * Grinold's rule α = IC·ω·z and the four-line derivation.
  * Simulated with N = 10–500: a constant IC matches IC√N; with an IC standard deviation of 0.10 at N = 500, 1.12 →
    0.46.
  * The transfer coefficient: long only on 500 assets, 0.86.
  * Effective breadth: 100 bets correlated 0.2 are worth 4.8; time breadth.
  * Grinold and Kahn's scale (0.5 good, 1.0 exceptional); three limits.
* **2. Factor risk models** (5.6).
  * Σ = XFX' + Δ: 4.5 million numbers against 4,830 for N = 3,000 and K = 60.
  * The five-part machine; five styles and a market; industries and the sum-to-zero constraint.
  * Daily WLS (R² 0.19 on average).
  * Factor returns 2018–20: volatility −48%/yr (t −2.4), reversal +33% (t 2.1). The median coin's risk is 72% factor.
  * Bias statistics:

    | Portfolio | Bias statistic |
    |---|---|
    | equal-weighted | 1.08 |
    | random long-short | 0.91 |
    | volatility factor | 0.84 (over-forecast) |
    | single coins | 1.07 |

  * Fundamental, statistical and macroeconomic models (Connor 1995); Barra.
* **3. Specific risk and Bayesian betas** (3.8).
  * Shrunk specific variances.
  * Blume (β_next ≈ 0.34 + 0.68β) and the adjusted beta.
  * Vasicek's posterior (weight 0.73 on the coin's own estimate).
  * One quarter's scatter, raw against shrunk. Over 12 pairs of quarters, the mean squared error of next quarter's beta:

    | Estimate | MSE |
    |---|---|
    | raw | 0.050 |
    | Vasicek | 0.041 |
    | β = 1 for all | 0.052 |

  * Why shrinkage works; Scholes–Williams and Dimson.
* **4. Transaction costs and the square-root law** (4.7).
  * Implementation shortfall.
  * The square-root law and the 3/2 power: $1m in the median coin ($3.3m a day, σ 5.2%) costs 2.9%.
  * Frazzini–Israel–Moskowitz ($1.7 tn, 21 markets, 19 years); Novy-Marx–Velikov.
  * The capacity curve, $100k to $1bn (0.68, −0.31, −3.3, …).
  * Costs inside the optimisation; the κ^{1/3} no-trade band and κ^{2/3} welfare loss.
* **5. Trading toward a moving target: Garleanu and Pedersen** (4.5).
  * The problem; the Riccati solution and trade rate a/λ ≈ √(γ/λ); the aim portfolio and the weight 1/(1 + φa/γ).
  * An illustration; the closed form against value iteration (equal to 1e-15).
  * Many assets and the Λ ∝ Σ assumption.
  * On the coins: calm (φ 0.023, half-life 30 days) and 3-day reversal (φ 0.37, 1.5 days). Myopic against GP Sharpe:

    | λ | Myopic | GP |
    |---|---|---|
    | 8 | 0.04 | 0.66 |
    | 32 | −2.13 | 0.53 |

  * Lessons.
* **6. Multi-period optimization** (2.9).
  * Boyd et al. (2017); the receding horizon; forecasts for every period; constraints.
  * One asset with 3/2-power impact: the first trade is 0.09 for a one-period plan, 0.26 for five periods and 0.24 for
    forty, the last with an orderly exit.
  * The link to GP.
* **7. Alpha combination** (3.3).
  * IC² = ic'C⁻¹ic.
  * Six signals' ICs in 2018–19 and 2020: the mined alpha 0.080 → 0.072.
  * The 2020 ICs:

    | Combination | IC, 2020 |
    |---|---|
    | equal weights | 0.068 |
    | IC weights | 0.070 |
    | ridge | 0.054–0.059 |
    | the mined alpha alone | 0.072 |

  * Horizons; combining forecasts or portfolios.
* **8. Decay, capacity and Berk–Green** (3.4).
  * Turnover ∝ √(2φ): 0.21 against 0.86.
  * Π(A) = gA − cA^{3/2}: break-even (g/c)²; A* = 4/9 of it; net g/3.
  * Berk and Green; with square-root costs, f* = a/3 and the same 4/9.
  * Berk and van Binsbergen; the House's capacity rule.
* **9. Crowding and August 2007** (3.4).
  * The quant quake: Goldman's $3bn GEO recapitalisation, as announced on 13 August 2007, after a reported loss of about
    30%.
  * Khandani and Lo's contrarian rule on the 49 industries: 8 Aug −1.04%, 9 Aug −0.82%, 10 Aug +1.21%, against a
    typical ±0.36%.
  * The unwind hypothesis; the risk model's view; comomentum.
  * Lessons: the contrarian rule's 1997–2007 Sharpe on industries was −0.41.
* **10. P&L attribution** (3.2).
  * The identity; Brinson.
  * The mined alpha: 90%/yr gross, of which 98% points came from the volatility factor. Its factor share of variance was
    86%; its specific Sharpe was 0.21, against 1.80 for the book.
  * Mine on residuals; static against timing; Euler risk contributions.
* **11. The aim portfolio on the coins, registered and opened** (3.5).
  * 10 trials; the counter goes 23,523 → 23,533.
  * Research Sharpe 0.66 (myopic 0.05). On 2021–25: −0.96 (myopic −0.83).
  * Monthly: −0.43 ± 0.25 at 413% volatility.
  * The diagnosis. On 55 of 1,825 days, positions in coins with near-zero forecast variance carried 93% of the variance.
    These were mostly USDe, a stablecoin, in November and December 2025. The rest of the book had a Sharpe of 0.35; this
    is a diagnosis only.
  * Why 1/σ² rules need floors; the House's guards.
* **12. Rule 31: the risk model** (2.8). The first sheet; `factor_returns`, the trade rate and its check, and the
  guards, from the House's source; the module; Rule 31; three cases.
* **For the researcher: the information ratio when the IC moves** (4.8).
  * The setup; the four-line proof; the theorem with its limits.
  * Simulations at N = 20–1000: at N = 1000, 0.93 and 0.47 simulated against 0.92 and 0.47 predicted, and a naive 1.26.
  * The corollary: N* ≈ 1/σ², where IR is 71% of its ceiling.
  * The coins: the mined alpha's daily IC is 0.076 ± 0.30; the naive law gives 0.52 and the theorem 0.23.
  * Fat tails (excess kurtosis 18); the Pearson IC's IR is 0.117, against a realised 0.087, within one standard error.
  * Open problems.
* **Recap, desk questions, problems** (3.0). Fourteen lines; six desk questions; twelve problems, two of qualifying-exam
  level, solved below.

## Hands-on

* **Built and run here:**
  * a fundamental factor risk model of the coins: exposures, daily WLS, EWMA factor covariance, shrunk specific
    variance, bias tests;
  * Vasicek's betas, scored out of sample;
  * square-root costs and a capacity curve;
  * Garleanu–Pedersen and myopic traders, net of costs;
  * a multi-period plan with 3/2-power impact;
  * ridge alpha combination;
  * daily factor attribution;
  * Khandani–Lo's contrarian rule in August 2007.
* **Labs, from the House's source:** `factor_returns`, `gp_trade_rate` with its `riccati_scalar` check, and the guards
  `floor_variance` and `cap_positions`.
* **Simulations against theory:** the moving-IC theorem at six breadths and two IC volatilities.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Grinold and Kahn, *Active Portfolio Management* (2nd ed., 2000) | the fundamental law, risk models, forecasting, transaction costs, attribution | 1–4, 7, 10 |
| Isichenko, *Quantitative Portfolio Management* (2021) | forecast combination, costs, optimisation with impact | 4–7 |
| Paleologo, *The Elements of Quantitative Investing* | factor models, specific risk, the bias statistic, attribution | 2, 3, 10 |
| Narang, *Inside the Black Box* | risk models, transaction-cost models, execution | 2, 4 |
| Boyd et al., *Multi-Period Trading via Convex Optimization* (2017) | single- and multi-period optimisation | 6 |

## Papers, chapter by chapter

* ch. 1: Grinold (1989), *JPM*; Clarke, de Silva and Thorley (2002), *FAJ*.
* ch. 2: Rosenberg (1974), *JFQA*; Fama and MacBeth (1973); Connor and Korajczyk (1986), *JFE*; Chen, Roll and Ross
  (1986), *JB*; Connor (1995), *FAJ*.
* ch. 3: Blume (1971, 1975), *JF*; Vasicek (1973), *JF*; Scholes and Williams (1977), *JFE*; Dimson (1979), *JFE*.
* ch. 4: Perold (1988), *JPM*; Torre (1997); Almgren, Thum, Hauptmann and Li (2005); Tóth et al. (2011), *PRX*;
  Frazzini, Israel and Moskowitz (2018); Novy-Marx and Velikov (2016), *RFS*; Constantinides (1986), *JPE*; Davis and
  Norman (1990); Shreve and Soner (1994).
* ch. 5: Garleanu and Pedersen (2013), *JF* 68.
* ch. 6: Boyd, Busseti, Diamond, Kahn, Koh, Nystrup and Speth (2017), *Foundations and Trends in Optimization*.
* ch. 7: Grinold and Kahn, ch. on forecasting.
* ch. 8: Berk and Green (2004), *JPE*; Berk and van Binsbergen (2015), *JFE*.
* ch. 9: Khandani and Lo (2007; 2011, *JFM*); Lou and Polk, "Comomentum"; Goldman Sachs press release, 13 August 2007.
* ch. 10: Brinson, Hood and Beebower (1986), *FAJ*.
* Research: Qian and Hua (2004), *JIM*; Ding (2010); Buckle (2004); Ding and Martin (2017).

## For the researcher

* **The theorem.**
  * The model: in period t, standardised returns are r = IC_t z + √(1 − IC_t²)ε. The scores z are standardised, the
    noise ε is i.i.d., and IC_t is i.i.d. with mean μ and variance σ².
  * The book with holdings ∝ z has IR = μ/√(σ²(1 − 1/N) + (1 − μ²)/N).
  * With σ = 0 this is the fundamental law, up to √(1 − μ²). As N → ∞ it tends to μ/σ.
  * At N* = (1 − μ²)/σ², IR ≈ μ/(σ√2), which is 71% of the ceiling.
* **Measured.** Rank weights earn the Pearson correlation of weights with returns, not the rank IC. With the coins'
  fat tails (excess kurtosis 18), that correlation's IR (0.117 a day for the mined alpha) is what the book delivered
  (0.087, standard error ≈ 0.03).
* **Simplifications.**
  * The cost model is quadratic for the trading rule (λ = 8), the square-root law for the capacity curve.
  * The coins' risk model has no industries, and its specific variances are shrunk 30% toward the cross-sectional
    mean.
  * The GP trader uses a diagonal risk model of 60-day variances. That is the flaw the envelope exposed.
* **Open problems.**
  * The multi-period IR with an autocorrelated IC and costs.
  * Estimating effective breadth without overstating it.
  * The IR-optimal weighting under heavy tails.

## Build it

```bash
python -m videos.quant.quant31.compute                            # every item; a few minutes on 2 cores
python -m pytest -q tests/test_quant_house.py -k riskmodel
EXPLAINER_TTS=silent python tools/qa_scene.py quant31 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant31                                      # the narrated part
```

## Desk questions, with solutions

1. **IC 0.05, 500 stocks, monthly. IR?** The fundamental law gives 0.05√6000 ≈ 3.87. If the monthly IC has a standard
   deviation of 0.10, the per-month IR is 0.05/√(0.01·0.998 + 0.9975/500) ≈ 0.457, so about 1.58 a year.
2. **Bias statistic 1.30 over two years of daily data.** Realised volatility is 30% above forecast. The 95% band is
   1 ± 2√(2/504) ≈ 1 ± 0.13, so this is a clear under-forecast.
3. **A factor-neutral book with 4% forecast volatility loses 10% in a week.** It can happen through a common risk the
   model does not contain:
   * crowded positions unwound by others (August 2007);
   * a forecast variance near zero (Chapter 11);
   * a factor moving far beyond its history.
4. **6% net at $100m after 2% costs; at $400m?** Costs per dollar grow like √A, so they double to 4%. The gross 8% nets
   4%.
5. **Costs quadruple.** The trade rate a/λ ≈ √(γ/λ) halves. The fast signal's aim weight 1/(1 + φa/γ) falls, since
   a ≈ √(γλ) doubles.
6. **A variance floor added after the envelope, Sharpe 0.4 on 2021–25.** This says nothing new about the hold-out. The
   years have been seen, so the repaired rule is a new trial on research data, and it waits for data that did not exist
   when it was written.

## Problems, with solutions

1. **The hook.** 0.05·√(500·12) = 3.87; 0.457·√12 = 1.58.
2. **The band.** T = 504: 1 ± 2√(2/504) = 1 ± 0.126. 1.30 lies outside it: an under-forecast.
3. **Vasicek.** Precisions are 1/0.09 for both, so β* = (1.8 + 1.0)/2 = 1.4.
4. **Four times the size.** Costs 2% → 2·√4 = 4%; net 8% − 4% = 4%.
5. **Break-even $900m.** A* = (4/9)·900 = $400m; the investors' net is g/3, a third of the gross.
6. **The trade-rate limit.** As ρ → 0, a = (−γ + √(γ² + 4γλ))/2 ≈ √(γλ) when λ ≫ γ, so a/λ ≈ √(γ/λ). Quadrupling λ
   halves it.
7. **Two signals.** IC² = ic'C⁻¹ic = 2·0.04²/(1 + 0.5) = 0.00213, so IC ≈ 0.046.
8. **Turnover.** The ratio is √(0.32/0.02) = 4.
9. **Attribution.** 12% = 0.4·20% (8%) + 2% timing + selection, so selection is 2%.
10. **The ceiling.** μ/σ = 0.5 a month; √12·0.5 ≈ 1.73 a year. N* = (1 − 0.0009)/0.0036 ≈ 278.
11. **(qual) The moving-IC theorem.**
    * Decomposition: π_t = IC_t·(1/N)Σz_i² + √(1 − IC_t²)·(1/N)Σz_iε_i. The first average is 1. Given IC_t, the second
      term has mean 0 and variance (1 − IC_t²)/N.
    * Mean and variance: E π = μ. By total variance, Var π = σ² + E(1 − IC_t²)/N = σ² + (1 − μ² − σ²)/N
      = σ²(1 − 1/N) + (1 − μ²)/N.
    * Monotonicity and limit: IR = μ/√Var π increases in N whenever 1 − μ² > σ², and tends to μ/σ.
    * At N*: here σ²(1 − 1/N*) ≈ σ² and (1 − μ²)/N* = σ², so Var ≈ 2σ² and IR ≈ μ/(σ√2).
12. **(qual) Garleanu–Pedersen, scalar.** Let d = 1 − ρ and take the next period's signal to be f' = (1 − φ)f.
    * **Bellman equation.** V(x₋, f) = max_x { d[x β f' − (γ/2)σ²x²] − (λ/2)σ²(x − x₋)² + d E V(x, f') }.
    * **Quadratic guess.** Substitute the guess. The first-order condition is linear: x = k_x x₋ + k_f f, with
      k_x = λσ²/(dγσ² + λσ² + dA_xx).
    * **Riccati equation.** Matching the x₋² terms gives A_xx = λσ² − (λσ²)²/(dγσ² + λσ² + dA_xx).
    * **Trade rate.** Write A_xx = λσ²(1 − k_x). The trade rate 1 − k_x = a/λ then solves
      d(a/λ)²λ + (dγ + λρ)(a/λ) − dγ = 0, so a = (−(γd + λρ) + √((γd + λρ)² + 4γλd²))/(2d).
    * **Aim.** The f-coefficients give the aim x̄ = k_f f/(a/λ). Relative to Markowitz's β(1 − φ)f/(γσ²), the ratio is
      1/(1 + φa/γ). The House checks both against value iteration, to 1e-12.

## Data and reproducibility

* **Binance daily klines.**
  * The source is Part 29's frozen grid of every USDT pair.
  * A coin is eligible on a day with 60 days of history and a median quote volume of at least 250,000 USDT.
  * The hold-out dataset `binance/usdt_daily_returns` is sealed and was opened once, by `gp_calm_reversal_part31`.
* **Kenneth French's 49 daily industry portfolios** (to 2020) for August 2007.
* **Registered:** `gp_calm_reversal_part31`, charged 10 trials (every cost level and trader compared in Chapter 5).
  * The counter goes from 23,523 to 23,533.
  * The Track Record row: research 0.53 ± 0.54 (33 months), hold-out −0.43 ± 0.25 (60 months).
  * The row is recorded as it is. The diagnosis (Sharpe 0.35 without the near-zero-variance coins) is not a result.
* **Quoted, not computed:**
  * Frazzini–Israel–Moskowitz's, Novy-Marx–Velikov's, Blume's, Connor's and Berk–van Binsbergen's results;
  * Khandani–Lo's stock-level losses;
  * Goldman's announcement and the reported GEO loss.
* **Simulated or illustrative:** the fundamental-law and theorem simulations; the aim-portfolio picture; the
  multi-period experiment.

---

# 量化金融，从零搭建 — 第31部分：风险模型、成本与跨期交易

本系列共四十三部分，这是第五幕"组合、策略与公司"（第30–38部分）的第二部分，按本系列的博士层次标准构建。第30部分用估计的均值和协方差一次性地选出权重；本部分让它变得真实：协方差来自因子风险模型，权重必须交易，交易要花钱，而在你向预测靠拢时预测本身也在移动。资产范围沿用第29部分：所有具备60天历史且成交量足够的币安USDT币种，2018–2020年用于研究，2021–2025年封存；2007年8月在Kenneth French的日度行业组合上回放。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：三点九，还是一点六。**
  * IC为0.05、500只股票、每月调仓：定律承诺3.87；若IC的标准差为0.10，则为1.58。
  * 信息比率的去向：变动的IC、成本（平静币种信号成本前夏普1.27，十万美元时0.68，一百万美元时−0.31）、风险模型。
  * 第五幕；五十年持有预测的历史；本部分计划。
* **1. 主动管理基本定律。**
  * Grinold法则α = IC·ω·z与四行推导。
  * N = 10–500的模拟：IC恒定时与IC√N吻合；IC标准差为0.10、N = 500时为1.12 → 0.46。
  * 转移系数：500个资产只做多为0.86。
  * 有效广度：相关0.2的100次下注相当于4.8次；时间广度。
  * Grinold与Kahn的标尺（0.5为好，1.0为杰出）；三个限制。
* **2. 因子风险模型。**
  * Σ = XFX' + Δ：N = 3,000、K = 60时为450万个数对4,830个数。
  * 五部分的机器；五个风格因子加一个市场因子；行业与和为零约束。
  * 日度加权最小二乘（平均R² 0.19）。
  * 2018–20年因子收益：波动率每年−48%（t −2.4），反转+33%（t 2.1）。中位数币种风险的72%来自因子。
  * 偏差统计量：

    | 组合 | 偏差统计量 |
    |---|---|
    | 等权 | 1.08 |
    | 随机多空 | 0.91 |
    | 波动率因子 | 0.84（高估） |
    | 单个币种 | 1.07 |

  * 基本面、统计与宏观三类模型（Connor 1995）；Barra。
* **3. 特质风险与贝叶斯贝塔。**
  * 收缩的特质方差。
  * Blume（β_next ≈ 0.34 + 0.68β）与调整贝塔。
  * Vasicek后验（币种自身估计权重0.73）。
  * 一个季度的散点图，原始对比收缩。12对季度上，下一季度贝塔的均方误差：

    | 估计 | 均方误差 |
    |---|---|
    | 原始 | 0.050 |
    | Vasicek | 0.041 |
    | 全部β = 1 | 0.052 |

  * 收缩为何有效；Scholes–Williams与Dimson。
* **4. 交易成本与平方根法则。**
  * 执行落差。
  * 平方根法则与3/2次方：在中位数币种（日成交330万美元，σ 5.2%）上交易一百万美元成本为2.9%。
  * Frazzini–Israel–Moskowitz（1.7万亿美元，21个市场，19年）；Novy-Marx–Velikov。
  * 从十万到十亿美元的容量曲线。
  * 把成本放进优化；κ^{1/3}的不交易区间与κ^{2/3}的福利损失。
* **5. 追逐移动的目标：Gârleanu与Pedersen。**
  * 问题；Riccati解与交易速率a/λ ≈ √(γ/λ)；目标组合与权重1/(1 + φa/γ)。
  * 示意图；闭式解对值迭代（一致到1e-15）。
  * 多资产与Λ ∝ Σ假设。
  * 币市上：平静信号（φ 0.023，半衰期30天）与三天反转（φ 0.37，1.5天）。短视与GP的夏普比率：

    | λ | 短视 | GP |
    |---|---|---|
    | 8 | 0.04 | 0.66 |
    | 32 | −2.13 | 0.53 |

  * 教训。
* **6. 多期优化。**
  * Boyd等（2017）；滚动时域；每期的预测；约束。
  * 单资产、3/2次方冲击：第一笔交易，单期规划为0.09，五期为0.26，四十期为0.24，最后一种带有序退出。
  * 与GP的联系。
* **7. 阿尔法合成。**
  * IC² = ic'C⁻¹ic。
  * 六个信号在2018–19与2020年的IC：挖出的阿尔法0.080 → 0.072。
  * 2020年的IC：

    | 合成方式 | 2020年IC |
    |---|---|
    | 等权 | 0.068 |
    | IC加权 | 0.070 |
    | 岭回归 | 0.054–0.059 |
    | 挖出的阿尔法单独使用 | 0.072 |

  * 期限；合成预测还是合成组合。
* **8. 衰减、容量与Berk–Green。**
  * 换手 ∝ √(2φ)：0.21对0.86。
  * Π(A) = gA − cA^{3/2}：盈亏平衡(g/c)²；A*为其4/9；净收益g/3。
  * Berk–Green；在平方根成本下f* = a/3，规模同为4/9。
  * Berk与van Binsbergen；本系列公司的容量规则。
* **9. 拥挤与2007年8月。**
  * 量化地震：高盛于2007年8月13日宣布向GEO注资30亿美元，此前据报道亏损约30%。
  * Khandani–Lo逆向规则在49个行业上：8月8日−1.04%，9日−0.82%，10日+1.21%，典型波动±0.36%。
  * 平仓假说；风险模型的视角；共动量。
  * 教训：逆向规则在行业上1997–2007年的夏普为−0.41。
* **10. 业绩归因。**
  * 恒等式；Brinson。
  * 挖出的阿尔法：成本前每年90%，其中98个百分点来自波动率因子。因子占方差的86%；特质部分夏普0.21，组合整体为1.80。
  * 在残差上挖掘；静态与择时；欧拉风险贡献。
* **11. 币市上的目标组合，登记并打开。**
  * 10次试验；计数器23,523 → 23,533。
  * 研究期夏普0.66（短视0.05）。2021–25年：−0.96（短视−0.83）。
  * 月度：−0.43 ± 0.25，波动率413%。
  * 诊断：1,825天中有55天，预测方差接近零的币种仓位承载了93%的方差，主要是2025年11–12月的稳定币USDe。组合其余部分夏普0.35，这只是诊断。
  * 为什么1/σ²规则需要下限；本系列公司的两道防护。
* **12. 第31条规则：风险模型。** 第一张表；本系列公司源码中的`factor_returns`、交易速率及其检验、两道防护；模块；第31条规则；三个案例。
* **写给研究者：IC变动时的信息比率。**
  * 设定；四行证明；定理及其极限。
  * N = 20–1000的模拟：N = 1000时模拟值0.93与0.47，预测值0.92与0.47，朴素定律1.26。
  * 推论：N* ≈ 1/σ²，此时信息比率达到上限的71%。
  * 币市：挖出的阿尔法日度IC为0.076 ± 0.30；朴素定律给出0.52，定理给出0.23。
  * 厚尾（超额峰度18）；皮尔逊IC的信息比率0.117，实现值0.087，在一个标准误之内。
  * 开放问题。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 写给研究者

* **定理。**
  * 模型：第t期标准化收益r = IC_t z + √(1 − IC_t²)ε。得分z已标准化，噪声ε独立同分布，IC_t独立同分布，均值μ、方差σ²。
  * 持仓 ∝ z的组合，信息比率IR = μ/√(σ²(1 − 1/N) + (1 − μ²)/N)。
  * σ = 0时即为基本定律（相差√(1 − μ²)）；N → ∞时趋于μ/σ。
  * 在N* = (1 − μ²)/σ²处，IR ≈ μ/(σ√2)，即上限的71%。
* **测量。** 秩权重赚到的是权重与收益的皮尔逊相关，而不是秩IC。在币市的厚尾下（超额峰度18），这一相关的信息比率（挖出的阿尔法每天0.117）就是组合实际交付的水平（0.087，标准误约0.03）。
* **简化。**
  * 交易规则用二次成本（λ = 8），容量曲线用平方根法则。
  * 币市风险模型没有行业，特质方差向横截面均值收缩30%。
  * GP交易者使用60天方差的对角风险模型。这正是信封所暴露的缺陷。
* **开放问题。**
  * 带自相关IC与成本的多期信息比率。
  * 不高估地估计有效广度。
  * 厚尾下信息比率最优的加权方式。

## 交易台问题与解答

1. **IC 0.05、500只股票、每月调仓，信息比率？** 基本定律给出0.05√6000 ≈ 3.87。若月度IC标准差为0.10，每月信息比率为0.05/√(0.01·0.998 + 0.9975/500) ≈ 0.457，每年约1.58。
2. **两年日度数据上的偏差统计量为1.30。** 实现波动率比预测高30%。95%区间为1 ± 2√(2/504) ≈ 1 ± 0.13，所以这是明显的低估。
3. **预测波动率4%的因子中性组合一周亏损10%。** 它可能通过模型不包含的共同风险发生：
   * 他人平仓拥挤仓位（2007年8月）；
   * 接近零的预测方差（第11章）；
   * 某个因子远超其历史的变动。
4. **一亿美元时扣除2%成本后净赚6%；四亿美元时？** 每美元成本随√A增长，翻倍到4%；毛收益8%，净收益4%。
5. **成本变成四倍。** 交易速率a/λ ≈ √(γ/λ)减半。快信号的目标权重1/(1 + φa/γ)下降，因为a ≈ √(γλ)翻倍。
6. **信封打开后加上方差下限，2021–25年夏普0.4。** 这对样本外没有任何新的说明。那些年份已被看过，所以修复后的规则是研究数据上的一次新试验，要等它写成之后才出现的数据来检验。

## 习题与解答

1. **开篇。** 0.05·√(500·12) = 3.87；0.457·√12 = 1.58。
2. **区间。** T = 504：1 ± 2√(2/504) = 1 ± 0.126。1.30在区间外：低估。
3. **Vasicek。** 两者精度都是1/0.09，所以β* = (1.8 + 1.0)/2 = 1.4。
4. **四倍规模。** 成本2% → 2·√4 = 4%；净收益8% − 4% = 4%。
5. **盈亏平衡九亿美元。** A* = (4/9)·900 = 四亿美元；投资者净收益为g/3，即毛收益的三分之一。
6. **交易速率的极限。** ρ → 0时，a = (−γ + √(γ² + 4γλ))/2，在λ ≫ γ时a ≈ √(γλ)，所以a/λ ≈ √(γ/λ)。λ变成四倍，速率减半。
7. **两个信号。** IC² = ic'C⁻¹ic = 2·0.04²/(1 + 0.5) = 0.00213，所以IC ≈ 0.046。
8. **换手。** 比值为√(0.32/0.02) = 4。
9. **归因。** 12% = 0.4·20%（8%）+ 2%择时 + 选股，所以选股为2%。
10. **上限。** μ/σ = 每月0.5；每年√12·0.5 ≈ 1.73。N* = (1 − 0.0009)/0.0036 ≈ 278。
11. **（资格考试）变动IC定理。**
    * 分解：π_t = IC_t·(1/N)Σz_i² + √(1 − IC_t²)·(1/N)Σz_iε_i。第一个平均为1；给定IC_t时，第二项均值为0、方差为(1 − IC_t²)/N。
    * 均值与方差：E π = μ。由全方差公式，Var π = σ² + E(1 − IC_t²)/N = σ² + (1 − μ² − σ²)/N = σ²(1 − 1/N) + (1 − μ²)/N。
    * 单调性与极限：当1 − μ² > σ²时，IR = μ/√Var π随N递增，趋于μ/σ。
    * 在N*处：σ²(1 − 1/N*) ≈ σ²，且(1 − μ²)/N* = σ²，所以Var ≈ 2σ²，IR ≈ μ/(σ√2)。
12. **（资格考试）标量Gârleanu–Pedersen。** 令d = 1 − ρ，并取下一期信号为f' = (1 − φ)f。
    * **贝尔曼方程。** V(x₋, f) = max_x { d[xβf' − (γ/2)σ²x²] − (λ/2)σ²(x − x₋)² + d E V(x, f') }。
    * **二次猜测。** 代入猜测，一阶条件是线性的：x = k_x x₋ + k_f f，其中k_x = λσ²/(dγσ² + λσ² + dA_xx)。
    * **Riccati方程。** 比较x₋²项得A_xx = λσ² − (λσ²)²/(dγσ² + λσ² + dA_xx)。
    * **交易速率。** 记A_xx = λσ²(1 − k_x)，交易速率1 − k_x = a/λ满足d(a/λ)²λ + (dγ + λρ)(a/λ) − dγ = 0，所以a = (−(γd + λρ) + √((γd + λρ)² + 4γλd²))/(2d)。
    * **目标。** f的系数给出目标x̄ = k_f f/(a/λ)，与Markowitz的β(1 − φ)f/(γσ²)之比为1/(1 + φa/γ)。本系列公司用值迭代检验两者，一致到1e-12。

## 数据与复现

* **币安日K线。**
  * 数据来自第29部分冻结的全部USDT交易对网格。
  * 币种在具备60天历史且成交额中位数不低于25万USDT的日子才合格。
  * 样本外数据集`binance/usdt_daily_returns`已封存，并由`gp_calm_reversal_part31`打开一次。
* **Kenneth French的49个日度行业组合**（至2020年），用于2007年8月。
* **本部分登记：** `gp_calm_reversal_part31`，计10次试验（第5章比较过的每个成本水平与交易者）。
  * 计数器从23,523升到23,533。
  * 业绩记录：研究期0.53 ± 0.54（33个月），样本外−0.43 ± 0.25（60个月）。
  * 这一行按原样记录；诊断（去掉接近零方差币种后夏普0.35）不是结果。
* **引用而非计算：**
  * Frazzini–Israel–Moskowitz、Novy-Marx–Velikov、Blume、Connor与Berk–van Binsbergen的结果；
  * Khandani–Lo在个股上的亏损；
  * 高盛的公告与据报道的GEO亏损。
* **模拟或示意：** 基本定律与定理的模拟；目标组合示意图；多期实验。
