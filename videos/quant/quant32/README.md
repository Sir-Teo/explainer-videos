# Quant, Built — Part 32: Systematic Macro and Alternative Premia

Part 32 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act V, Portfolios, Strategies and the Firm (30–38), built to the
series' PhD layer. Parts 30 and 31 worked on single securities; this part moves up to whole asset classes, the books
that trade them by rule, and the premia paid for holding risks others want to shed.

The universe is the House's macro panel of 23 US-listed ETFs across five classes: equities, Treasuries, credit,
commodities and currencies. The data are dividend-adjusted daily closes, as excess returns over 3-month T-bills, with
2006–2020 for research and 2021–2025 sealed. Long histories come from:

* Kenneth French (the US market, daily from 1926);
* FRED (10-year yields from 1962; spot oil, gas and exchange rates);
* Cboe's PUT index;
* AQR's published Century of Factor Premia and time-series momentum series;
* Part 28's FOMC archive.

The part covers:

* **Trend following** (Moskowitz, Ooi and Pedersen 2012):
  * time-series momentum built on the panel, with lookbacks, sizing and asset classes;
  * a century of evidence (Hurst, Ooi and Pedersen 2017; Lempérière et al. 2014);
  * how a CTA runs, with firm files on AHL/Man and Winton.
* **The smile and the crisis:**
  * 2008, 2009 and the first quarter of 2020;
  * slow crises, fast crashes and reversals;
  * the straddle identity, and trend as a diversifier for 60/40.
* **Volatility targeting**, asset by asset:
  * the evidence (Moreira and Muir; Cederburg et al.; Harvey et al.);
  * the leverage effect, and crowding in vol-control rules.
* **Risk parity:**
  * 60/40's risk concentration, and leverage aversion (Asness, Frazzini and Pedersen);
  * All Weather and the four environments;
  * the House's book, its leverage dial and financing cost;
  * the stock–bond correlation 1962–2020, and why it changes sign (Campbell, Sunderam and Viceira).
* **Value, momentum, carry and defensive across asset classes**, 1926–2020:
  * their Sharpe ratios and correlations, and the multi-style combination;
  * value and momentum everywhere, and betting against beta;
  * crisis years and cautions.
* **Carry, made visible:**
  * fund returns minus spot returns, for oil, natural gas and six currencies;
  * contango and backwardation, and bond carry;
  * negative oil in April 2020;
  * a currency carry book and its 2008 crash.
* **Selling insurance:** Cboe's PUT index against the market, Israelov and Nielsen's decomposition, Volmageddon, who
  buys insurance, and the mirror of trend.
* **Calendars, nights and events:**
  * the turn of the month and sell-in-May, by era;
  * FOMC announcement days, and overnight against intraday returns;
  * merger arbitrage, index changes and earnings drift;
  * data mining (Sullivan, Timmermann and White).
* **For the researcher:** why trend following is long a straddle.
  * The identity P = ½(S² − Q).
  * The mean is the lag-weighted autocovariance.
  * The third moment counts triangles, so the skewness is 2^{3/2}(n − 2)/√(n(n − 1)) → 2√2.
  * The limit law is ½(Z² − 1), so P(P > 0) → 31.7%.
  * Checked by simulation and on the 23 funds; diversification, the sign rule, and filters; open problems.
* **The registered books:** the trend book and the risk-parity book, registered and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`systematic`](../../../explainer/quant/house/systematic.py) module).

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: crisis alpha** (3.2).
  * 2008: SPY −37.7%, 60/40 −17.9%, the trend book +7.3%, AQR's trend series +24.6%.
  * Three questions; three kinds of premium; Act V; seventy years of trading whole markets; the plan.
* **1. Trend following** (4.6).
  * The panel; the rule (sign of the 252-day return, 40% per position, the book at 10%).
  * 2007–2020: Sharpe 0.51 against SPY 0.49 and 60/40 0.70, with correlation −0.01 to stocks and worst fall −18%.
  * Six configurations (1-month 0.10, 3-month 0.43, 12-month 0.51); by class, from currencies 0.00 to credit 0.50.
  * A century of evidence; AQR's series 1.06; AHL and Winton; how a CTA runs and what it charges; horizons.
* **2. The smile and the crisis** (4.2).
  * The quarterly scatter: a faint, slightly negative curvature on 23 funds; +2.0% in 2008Q4 and +9.7% in 2020Q1.
  * The mechanism; years 2008–2020 (2009 −3.9%).
  * Slow crises, fast crashes and reversals; 2020Q1 explained.
  * The straddle identity; the price of the straddle.
  * 60/40 with 20% in trend: Sharpe 0.87 → 0.96, worst fall −30% → −23%.
* **3. Volatility targeting** (3.7).
  * The rule; SPY's exposure path.
  * Sharpe raised for 9 of 23 funds, drawdown cut for 14; SPY 0.49 → 0.57 with a drawdown of −56% → −25%.
  * The leverage effect; the literature; risk budgeting; crowding.
* **4. Risk parity and the stock–bond correlation** (4.8).
  * 60/40 is 94% stocks in risk; leverage aversion; All Weather and its four environments.
  * The House's book: 2.0 gross on average, credit 33% of the risk, leverage 0.78–2.96.
  * Sharpe 0.48 against 60/40's 0.70; financing.
  * The correlation by decade: +0.17, +0.33, +0.26, +0.30, then −0.24 and −0.49.
* **5. Value, momentum, carry and defensive, everywhere** (4.4).
  * Definitions; carry (Koijen, Moskowitz, Pedersen and Vrugt).
  * Sharpe ratios 0.53, 0.64, 0.55 and 0.68, combined 1.45 (1926–2020).
  * Their paths; correlations (value–momentum −0.53); defensive and betting against beta.
  * The six worst equity years; value and momentum everywhere; cautions.
* **6. Carry, made visible** (4.5).
  * Oil: spot −2.8% a year, USO −18.9% a year; gas: spot −7.3%, UNG −37.3%.
  * Contango and backwardation; bond carry.
  * Negative oil: −$37.63, and USO's fall of 77% from 1 March 2020.
  * Currency carry: only AUD positive (+1.5% a year).
  * A carry book: Sharpe 0.07, −18% in 2008Q4, skewness −1.13.
* **7. Selling insurance** (3.3).
  * PUT against the market, 2007–2020: Sharpe 0.45 against 0.62, volatility 11.8% against 16.2%, skewness −1.63.
  * Beta 0.64, alpha −1.1% a year; Israelov–Nielsen; Volmageddon; who buys; the mirror of trend.
* **8. Calendars, nights and events** (4.8).
  * The turn of the month, as a share of the market's excess return: 93%, 147% and 38% by era.
  * The flow story; the night: SPY 1993–2020 earned 10.5% a year overnight against 0.8% intraday.
  * Sell in May: t = 2.2 for 1963–1990 and 1.6 since.
  * FOMC days: 31 bp against 3 bp, 24% of the return on 191 days.
  * Events; data mining.
* **9. The trend and risk-parity books, registered and opened** (4.3).
  * 6 and 2 trials; the counter goes 23,533 → 23,541.
  * 2021–25 Sharpe ratios: trend 0.27 ± 0.45, risk parity 0.15 ± 0.46, 60/40 0.48, SPY 0.69.
  * 2022: trend +15%, SPY −20%, 60/40 −18%, risk parity −23%.
  * The trend book's 2022 by class (bonds +20%).
  * The stock–bond correlation turned positive: −0.44 in research, then +0.08, +0.13, +0.06 and +0.09.
  * 60/40 with 20% trend: 2022 −18% → −12%.
  * Reading; next steps.
* **10. Rule 32: the macro books** (3.2).
  * The first sheet; the books together (risk parity–60/40 +0.67, trend–60/40 +0.06).
  * Labs: TSMOM, the identity, risk parity.
  * The module; Rule 32; three cases.
* **For the researcher: why trend following is long a straddle** (7.0).
  * The setup; four lemmas (identity, mean, moments, limit); the theorem.
  * Simulations at n = 2–252 (n = 63: skew 2.72 against 2.76; 32.2% of blocks won).
  * The limit law; SPY's exact parabolas.
  * The 23 funds: skew 1.52 and 3.77 against 2.62 and 2.76; won 34% and 35%; mean against autocovariance, correlation
    0.93 and 0.85.
  * Diversification (0.55 theory, 0.33 measured); the sign rule; filters; open problems.
* **Recap, desk questions, problems** (3.0). Fourteen lines; six desk questions; twelve problems, two of qualifying-exam
  level, solved below.

## Hands-on

* **Built and run here:**
  * time-series momentum, volatility targeting and risk parity on 23 ETFs;
  * a 10-year Treasury built from yields, giving the stock–bond correlation since 1962;
  * carry measured as fund minus spot;
  * a currency carry book;
  * the turn of the month, sell-in-May and FOMC days on 95 years of daily data;
  * overnight and intraday SPY;
  * the trend identity, simulated and measured.
* **Labs, from the House's source:** `tsmom_positions`, `linear_trend_blocks` with `trend_skew_theory`, and
  `risk_parity`.
* **Simulations against theory:** the skewness theorem at eight block lengths; the limit law.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Pedersen, *Efficiently Inefficient* (2015) | global macro, managed futures, risk parity, carry | 1–5 |
| Ilmanen, *Expected Returns* (2011) | carry, value, momentum, volatility selling, seasonality | 5–8 |
| Kakushadze and Serur, *151 Trading Strategies* (2018) | trend, carry, calendar and event strategies | 1, 6, 8 |
| Clenow, *Following the Trend* (2013) | how a futures trend fund is built and run | 1, 2 |

## Papers, chapter by chapter

* ch. 1: Moskowitz, Ooi and Pedersen (2012), *JFE*; Hurst, Ooi and Pedersen (2017), *JPM*; Lempérière et al. (2014),
  *J. Investment Strategies*.
* ch. 2: Fung and Hsieh (2001), *RFS*; Daniel and Moskowitz (2016), *JFE*.
* ch. 3: Moreira and Muir (2017), *JF*; Cederburg, O'Doherty, Wang and Yan (2020), *JFE*; Harvey et al. (2018), *JPM*.
* ch. 4: Asness, Frazzini and Pedersen (2012), *FAJ*; Campbell, Sunderam and Viceira (2017), *Critical Finance Review*;
  Bridgewater, "The All Weather Story".
* ch. 5: Koijen, Moskowitz, Pedersen and Vrugt (2018), *JFE*; Asness, Moskowitz and Pedersen (2013), *JF*; Frazzini and
  Pedersen (2014), *JFE*; Brunnermeier, Nagel and Pedersen (2008), *NBER Macro Annual*.
* ch. 6: Keynes (1930) and Hicks (1939) on normal backwardation.
* ch. 7: Israelov and Nielsen (2015), *FAJ*; Ilmanen (2012), *FAJ*; Garleanu, Pedersen and Poteshman (2009), *RFS*.
* ch. 8: Ariel (1987), *JFE*; Lakonishok and Smidt (1988), *RFS*; Ogden (1990), *JF*; Bouman and Jacobsen (2002), *AER*;
  Lucca and Moench (2015), *JF*; Lou, Polk and Skouras (2019), *JFE*; Mitchell and Pulvino (2001), *JF*; Bernard and
  Thomas (1989); Sullivan, Timmermann and White (2001), *J. Econometrics*.
* Research: Potters and Bouchaud (2005), *Wilmott*; Fung and Hsieh (2001).

## For the researcher

* **The theorem.**
  * The rule: within a block of n returns, the linear trend rule holds x_t = Σ_{s<t} r_s.
  * Its profit is exactly P = ½(S² − Q) for every path, with E P = Σ_k (n − k)γ_k + C(n, 2)μ².
  * For i.i.d. normal returns: E Y² = C(n, 2), E Y³ = n(n − 1)(n − 2), and skew = 2^{3/2}(n − 2)/√(n(n − 1)).
  * For any i.i.d. returns with finite variance, P/(nσ²) ⇒ ½(Z² − 1).
* **Measured.**
  * Simulated skewness matches the theorem.
  * On the 23 funds (standardised returns), the skewness is large and positive, though noisy under fat tails.
  * The share of blocks won is near 32%.
  * Each fund's mean profit tracks its own autocovariances.
* **Simplifications.**
  * ETFs stand in for futures.
  * Returns are before costs and fees.
  * The bond is a constant-maturity proxy built from yields.
  * The styles are AQR's published series, not rebuilt.
  * The PUT index is daily only from 2007.
* **Open problems.**
  * Adaptive filters under non-stationary autocovariances.
  * The optimal no-trade band for a long-straddle strategy.
  * Who supplies the autocorrelation.

## Build it

```bash
python -m videos.quant.quant32.compute                            # every item; a few minutes on 2 cores
python -m pytest -q tests/test_quant_house.py -k systematic
EXPLAINER_TTS=silent python tools/qa_scene.py quant32 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant32                                      # the narrated part
```

## Desk questions, with solutions

1. **Why does trend following have positive skew?** The linear rule's profit is ½(S² − Q): a straddle on the block's
   move, financed by realised variance. Under i.i.d. returns its skewness is 2^{3/2}(n − 2)/√(n(n − 1)) → 2√2, with no
   autocorrelation needed.
2. **Where does its expected return come from?** Only from autocorrelation, E P = Σ_k (n − k)γ_k, plus a negligible drift
   term.
3. **60/40: the stocks' share of risk?** 0.36·0.0256 / (0.36·0.0256 + 0.16·0.0036) = 0.0092/0.0098 ≈ 94%.
4. **Why did risk parity lose more than 60/40 in 2022?** It was levered on bonds. The stock–bond correlation turned
   positive with inflation, so its diversification and its leverage failed together.
5. **Does volatility targeting raise the Sharpe ratio?** For 9 of 23 funds here. It reduced the worst drawdown for 14,
   mostly risky assets, through the leverage effect.
6. **An income fund sells index puts.** Ask for:
   * its skewness and worst month;
   * its beta (0.64 for the PUT index, 2007–2020);
   * its 2008, February 2018 and March 2020.

## Problems, with solutions

1. **60/40's risk.** About 94% stocks (desk question 3).
2. **Equal risk.** w_S/w_B = σ_B/σ_S = 6/16, so w_S = 0.27 and w_B = 0.73. The unlevered volatility is
   √(0.27²·0.16² + 0.73²·0.06²) ≈ 6.2%, so L ≈ 10/6.2 ≈ 1.6.
3. **Styles.** With ρ = 0: 0.6·√4 = 1.2. With ρ = 0.3: 0.6·√(4/(1 + 3·0.3)) = 0.6·1.45 ≈ 0.87.
4. **A levered loss.** The exposure is 2.5, of which 1.75 is bonds and 0.75 stocks: 1.75·(−10%) + 0.75·(−20%) =
   −32.5%, before financing.
5. **A put seller.** The mean is (50·1% − 30%)/51 ≈ 0.39% a month. The skewness is negative, since one large loss sits
   below many small gains.
6. **Overnight break-even.** 10%/504 ≈ 2 bp per trade.
7. **Random walk.** With γ_k = 0 for k ≥ 1, E P = Σ_{s<t} E[r_s]E[r_t] = C(n, 2)μ².
8. **Skewness.** For n = 63: 2^{1.5}·61/√(63·62) = 2.83·61/62.5 ≈ 2.76. Over 23 independent markets: 2.76/√23 ≈ 0.58.
9. **Years to two standard errors.** The Sharpe ratio's standard error is ≈ 1/√T, so 0.3 > 2/√T requires T > 44 years.
10. **Variance-proportional returns.** If μ_t = kσ_t², the Merton exposure μ_t/σ_t² is constant. Targeting then shrinks
    exposure exactly when the expected return is highest, which hurts the Sharpe ratio.
11. **(qual) Moments and limit law.**
    * **Second moment.** E Y² = Σ over pairs of pairs of E[z_a z_b z_c z_d], which is non-zero (and equal to 1) only
      when {a, b} = {c, d}, so E Y² = C(n, 2).
    * **Third moment.** For three pairs, the expectation is non-zero only when each index appears exactly twice, that
      is, when the pairs are the sides of a triangle. There are C(n, 3) triangles and 3! orderings, so
      E Y³ = n(n − 1)(n − 2).
    * **Skewness.** n(n − 1)(n − 2)/(n(n − 1)/2)^{3/2} = 2^{3/2}(n − 2)/√(n(n − 1)).
    * **Limit law.** Y = ½(S² − Q) with S/√n ⇒ Z and Q/n → 1, so Y/n ⇒ ½(Z² − 1), and P(Y > 0) → P(Z² > 1) = 31.7%.
12. **(qual) Filters.**
    * **Mean.** E P_w = Σ_k w_k (n − k)γ_k.
    * **Variance.** For i.i.d. returns with unit variance, the terms r_s r_t are uncorrelated across distinct pairs, so
      Var P_w = Σ_k w_k² (n − k).
    * **Optimum.** Maximising E/√Var is a Cauchy–Schwarz problem, giving w_k ∝ γ_k(n − k)/(n − k) = γ_k: the filter
      matched to the autocovariances.

## Data and reproducibility

* **Funds.** Yahoo Finance's dividend-adjusted daily closes for 23 ETFs (2006-01 to 2025-11), each checked by SHA-256.
* **FRED.** DTB3, DGS10, DCOILWTICO, DHHNGSP and six exchange rates.
* **Other sources.** Kenneth French's daily file; Cboe's PUT index; AQR's Century of Factor Premia and TSMOM data
  sets (as published, through 2020 here); Part 28's FOMC archive.
* **Registered:** `trend_part32` (6 trials) and `riskparity_part32` (2).
  * The counter goes from 23,533 to 23,541.
  * The hold-out `yahoo/etf_panel_excess` is sealed and was opened once.
  * Track Record rows: trend research 0.49 ± 0.27 (165 months), hold-out 0.27 ± 0.45 (59); risk parity 0.49 ± 0.29
    and 0.15 ± 0.46.
* **Studied, not registered:** the currency carry book; the 60/40-plus-trend blend; volatility targeting.
* **Quoted, not computed:** Hurst–Ooi–Pedersen's century; Lempérière et al.; Moreira–Muir, Cederburg et al. and Harvey
  et al.; Lucca–Moench's intraday timing; Bouman–Jacobsen; Mitchell–Pulvino; Goldman, Bridgewater and Credit Suisse
  events as announced or reported.

---

# 量化金融，从零搭建 — 第32部分：系统化宏观与另类溢价

本系列共四十三部分，这是第五幕"组合、策略与公司"（第30–38部分）的第三部分，按本系列的博士层次标准构建。第30和31部分处理单个证券；本部分上升到整个资产类别，研究按规则交易它们的组合，以及因承担他人想甩掉的风险而获得的溢价。

资产范围是本系列公司的宏观面板：23只美国上市ETF，覆盖股票、国债、信用、商品和货币五类。数据是股息调整后的日度收盘价，取相对3个月国库券的超额收益，2006–2020年用于研究，2021–2025年封存。长期历史来自：

* Kenneth French（美国市场，自1926年起的日度数据）；
* FRED（自1962年起的10年期收益率；原油、天然气现货与汇率）；
* Cboe的PUT指数；
* AQR公布的"一个世纪的因子溢价"与时间序列动量序列；
* 第28部分的FOMC档案。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：危机阿尔法。**
  * 2008年：SPY −37.7%，六四组合 −17.9%，趋势组合 +7.3%，AQR趋势序列 +24.6%。
  * 三个问题；三种溢价；第五幕；七十年交易整个市场的历史；本部分计划。
* **1. 趋势跟踪。**
  * 资产面板；规则（252天收益的符号，每个仓位40%，组合10%）。
  * 2007–2020年：夏普0.51，SPY为0.49，六四组合为0.70；与股票相关性−0.01，最大跌幅−18%。
  * 六种配置（1个月0.10，3个月0.43，12个月0.51）；按类别，从货币0.00到信用0.50。
  * 一个世纪的证据；AQR序列1.06；AHL与Winton；CTA如何运作与收费；期限。
* **2. 微笑曲线与危机。**
  * 季度散点：23只基金上的曲率微弱、略为负；2008年第四季度+2.0%，2020年第一季度+9.7%。
  * 机制；2008–2020逐年（2009年−3.9%）。
  * 慢危机、快速崩盘与反转；2020年第一季度的解释。
  * 跨式恒等式；跨式的代价。
  * 六四组合配置20%趋势：夏普0.87 → 0.96，最大跌幅−30% → −23%。
* **3. 波动率目标。**
  * 规则；SPY的敞口路径。
  * 23只中9只夏普提高、14只回撤降低；SPY夏普0.49 → 0.57，回撤−56% → −25%。
  * 杠杆效应；文献；风险预算；拥挤。
* **4. 风险平价与股债相关性。**
  * 按风险算，六四组合有94%是股票；杠杆厌恶；全天候与四种环境。
  * 本系列公司的组合：平均总敞口2.0，信用占风险33%，杠杆0.78–2.96。
  * 夏普0.48，六四组合为0.70；融资成本。
  * 各年代相关性：+0.17、+0.33、+0.26、+0.30，然后是−0.24、−0.49。
* **5. 价值、动量、套息与防御，无处不在。**
  * 定义；套息（Koijen、Moskowitz、Pedersen与Vrugt）。
  * 夏普比率0.53、0.64、0.55、0.68，合成后1.45（1926–2020）。
  * 路径；相关性（价值–动量−0.53）；防御与押注低贝塔。
  * 股票最差的六年；价值与动量无处不在；警示。
* **6. 看得见的套息。**
  * 原油：现货每年−2.8%，USO每年−18.9%；天然气：现货−7.3%，UNG −37.3%。
  * 期货溢价与现货溢价；债券套息。
  * 负油价：−37.63美元；USO自2020年3月1日起下跌77%。
  * 货币套息：只有澳元为正（每年+1.5%）。
  * 套息组合：夏普0.07，2008年第四季度−18%，偏度−1.13。
* **7. 卖出保险。**
  * PUT对比市场，2007–2020：夏普0.45对0.62，波动率11.8%对16.2%，偏度−1.63。
  * 贝塔0.64，阿尔法每年−1.1%；Israelov–Nielsen；Volmageddon；谁在购买；趋势的镜像。
* **8. 日历、夜晚与事件。**
  * 月末效应占市场超额收益的份额，按时期分别为93%、147%、38%。
  * 资金流解释；夜晚：1993–2020年SPY隔夜每年赚10.5%，日内0.8%。
  * 五月卖出：1963–1990年t = 2.2，此后1.6。
  * FOMC日：31个基点对3个基点，191天贡献了24%的收益。
  * 事件；数据挖掘。
* **9. 趋势组合与风险平价组合，登记并打开。**
  * 6次与2次试验；计数器23,533 → 23,541。
  * 2021–25年夏普比率：趋势0.27 ± 0.45，风险平价0.15 ± 0.46，六四组合0.48，SPY 0.69。
  * 2022年：趋势+15%，SPY −20%，六四组合−18%，风险平价−23%。
  * 趋势组合2022年按类别（债券+20%）。
  * 股债相关性转正：研究期−0.44，之后为+0.08、+0.13、+0.06、+0.09。
  * 六四组合配置20%趋势：2022年−18% → −12%。
  * 解读；下一步。
* **10. 第32条规则：宏观组合。**
  * 第一张表；组合之间的关系（风险平价–六四组合+0.67，趋势–六四组合+0.06）。
  * 源码实验：TSMOM、恒等式、风险平价。
  * 模块；第32条规则；三个案例。
* **写给研究者：为什么趋势跟踪是做多跨式组合。**
  * 设定；四个引理（恒等式、均值、矩、极限）；定理。
  * n = 2–252的模拟（n = 63：偏度2.72对2.76；32.2%的段盈利）。
  * 极限分布；SPY的精确抛物线。
  * 23只基金：偏度1.52与3.77，对比2.62与2.76；盈利段34%与35%；均值与自协方差的相关性0.93与0.85。
  * 分散化（理论0.55，实测0.33）；符号规则；滤波器；开放问题。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 写给研究者

* **定理。**
  * 规则：在n个收益的一段中，线性趋势规则持有x_t = Σ_{s<t} r_s。
  * 对每条路径，利润恰好为P = ½(S² − Q)，且E P = Σ_k (n − k)γ_k + C(n, 2)μ²。
  * 对独立同分布正态收益：E Y² = C(n, 2)，E Y³ = n(n − 1)(n − 2)，偏度 = 2^{3/2}(n − 2)/√(n(n − 1))。
  * 对任何方差有限的独立同分布收益，P/(nσ²) ⇒ ½(Z² − 1)。
* **测量。**
  * 模拟的偏度与定理吻合。
  * 在23只基金（标准化收益）上，偏度大且为正，但在厚尾下带有噪声。
  * 盈利段占比接近32%。
  * 每只基金的平均利润跟随其自身的自协方差。
* **简化。**
  * 用ETF代替期货。
  * 收益为成本与费用前。
  * 债券是由收益率构建的固定期限代理。
  * 风格采用AQR公布的序列，未重建。
  * PUT指数仅自2007年起有日度数据。
* **开放问题。**
  * 非平稳自协方差下的自适应滤波器。
  * 做多跨式策略的最优不交易区间。
  * 谁在提供自相关。

## 交易台问题与解答

1. **趋势跟踪为什么有正偏度？** 线性规则的利润为½(S² − Q)：这一段波动上的跨式组合，以已实现方差融资。在独立同分布收益下，其偏度为2^{3/2}(n − 2)/√(n(n − 1)) → 2√2，不需要任何自相关。
2. **它的期望收益来自哪里？** 只来自自相关，E P = Σ_k (n − k)γ_k，另加一个可忽略的漂移项。
3. **六四组合中股票的风险份额？** 0.36·0.0256 / (0.36·0.0256 + 0.16·0.0036) ≈ 94%。
4. **为什么风险平价在2022年比六四组合亏得多？** 它加了债券杠杆。股债相关性随通胀转正，所以它的分散化与杠杆同时失效。
5. **波动率目标会提高夏普比率吗？** 这里23只中有9只。它降低了14只的最大回撤，大多是高风险资产，原因是杠杆效应。
6. **一只收益型基金卖出指数看跌期权。** 要问：
   * 它的偏度和最差月份；
   * 它的贝塔（2007–2020年PUT指数为0.64）；
   * 它的2008年、2018年2月和2020年3月。

## 习题与解答

1. **六四组合的风险。** 约94%是股票（交易台问题3）。
2. **等风险。** w_S/w_B = σ_B/σ_S = 6/16，所以w_S = 0.27，w_B = 0.73。未加杠杆的波动率为√(0.27²·0.16² + 0.73²·0.06²) ≈ 6.2%，所以L ≈ 10/6.2 ≈ 1.6。
3. **风格。** ρ = 0时：0.6·√4 = 1.2。ρ = 0.3时：0.6·√(4/(1 + 3·0.3)) = 0.6·1.45 ≈ 0.87。
4. **杠杆亏损。** 敞口2.5，其中债券1.75、股票0.75：1.75·(−10%) + 0.75·(−20%) = −32.5%，未计融资成本。
5. **看跌期权卖方。** 均值为(50·1% − 30%)/51 ≈ 每月0.39%。偏度为负，因为一次大亏落在许多小赚之下。
6. **隔夜盈亏平衡。** 10%/504 ≈ 每笔2个基点。
7. **随机游走。** 当k ≥ 1时γ_k = 0，所以E P = Σ_{s<t} E[r_s]E[r_t] = C(n, 2)μ²。
8. **偏度。** n = 63时：2^{1.5}·61/√(63·62) ≈ 2.76。23个独立市场：2.76/√23 ≈ 0.58。
9. **达到两个标准误所需年数。** 夏普比率的标准误约为1/√T，0.3 > 2/√T要求T > 44年。
10. **与方差成比例的收益。** 若μ_t = kσ_t²，则Merton敞口μ_t/σ_t²为常数。此时目标化恰在预期收益最高时缩小敞口，会降低夏普比率。
11. **（资格考试）矩与极限分布。**
    * **二阶矩。** E Y²是对成对的两两乘积求E[z_a z_b z_c z_d]之和，只有当{a, b} = {c, d}时非零（且等于1），所以E Y² = C(n, 2)。
    * **三阶矩。** 对三对乘积，只有当每个下标恰好出现两次时期望才非零，即三对是一个三角形的三条边。三角形有C(n, 3)个，排列方式有3!种，所以E Y³ = n(n − 1)(n − 2)。
    * **偏度。** n(n − 1)(n − 2)/(n(n − 1)/2)^{3/2} = 2^{3/2}(n − 2)/√(n(n − 1))。
    * **极限分布。** Y = ½(S² − Q)，其中S/√n ⇒ Z、Q/n → 1，所以Y/n ⇒ ½(Z² − 1)，且P(Y > 0) → P(Z² > 1) = 31.7%。
12. **（资格考试）滤波器。**
    * **均值。** E P_w = Σ_k w_k (n − k)γ_k。
    * **方差。** 对单位方差的独立同分布收益，不同对的r_s r_t互不相关，所以Var P_w = Σ_k w_k² (n − k)。
    * **最优。** 最大化E/√Var是一个柯西–施瓦茨问题，给出w_k ∝ γ_k：与自协方差相匹配的滤波器。

## 数据与复现

* **基金。** Yahoo Finance上23只ETF股息调整后的日度收盘价（2006-01至2025-11），每个都用SHA-256校验。
* **FRED。** DTB3、DGS10、DCOILWTICO、DHHNGSP及六个汇率。
* **其他来源。** Kenneth French日度文件；Cboe的PUT指数；AQR的"一个世纪的因子溢价"与TSMOM数据集（按公布版本，这里截至2020年）；第28部分的FOMC档案。
* **本部分登记：** `trend_part32`（6次试验）与`riskparity_part32`（2次）。
  * 计数器从23,533升到23,541。
  * 样本外数据集`yahoo/etf_panel_excess`已封存，并只打开一次。
  * 业绩记录：趋势组合研究期0.49 ± 0.27（165个月），样本外0.27 ± 0.45（59个月）；风险平价0.49 ± 0.29与0.15 ± 0.46。
* **研究但未登记：** 货币套息组合；六四组合加趋势的混合；波动率目标。
* **引用而非计算：** Hurst–Ooi–Pedersen的一个世纪；Lempérière等；Moreira–Muir、Cederburg等与Harvey等；Lucca–Moench的日内时间；Bouman–Jacobsen；Mitchell–Pulvino；高盛、桥水与瑞信的事件，以公告或报道为准。
