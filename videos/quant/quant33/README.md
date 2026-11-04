# Quant, Built — Part 33: Statistical Arbitrage

Part 33 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act V, Portfolios, Strategies and the Firm (30–38), built to the
series' PhD layer. Part 32 followed trends across asset classes; this part bets against them, at the scale of days and
single securities: pairs, cointegrated spreads, residuals of a factor model, and the mathematics of trading mean
reversion.

The universe is Kenneth French's 49 daily US industry portfolios, with research through 2020 and 2021–2025 sealed.
Supporting data:

* French's daily size deciles (weekly lead-lag from 1963);
* Binance's daily BTC and ETH bars (the Kalman chapter, 2018–2020);
* Cboe's VIX (the liquidity test, 1990–2020).

The part covers:

* **History:** Thorp and Princeton/Newport; Bamberger and Tartaglia at Morgan Stanley; D. E. Shaw, Renaissance and PDT,
  as reported; what decimalisation and competition changed.
* **Pairs by distance** (Gatev, Goetzmann and Rouwenhorst 2006), re-run on the industries; Do and Faff; the short leg
  (borrow fees, recalls, the 2008 short-sale ban).
* **Cointegration and the screening problem:**
  * Engle–Granger, year-by-year pass rates against the test's own false-positive rate, and persistence;
  * the selection bias of measured half-lives;
  * Johansen's baskets, and Royal Dutch/Shell as the purest pair.
* **The Ornstein–Uhlenbeck spread:** the AR(1) map, the s-score, Kendall's bias in short windows, and the confidence
  interval of a half-life.
* **Eigenportfolios and residuals** (Avellaneda and Lee 2010):
  * the residual book on the industries, gross and net;
  * eight variants and a ninth rule with the research chapter's band;
  * Sharpe against turnover, by era, and why costs bite twice.
* **Hedge ratios that move:** the Kalman filter on BTC/ETH, its effective window, and the trap of the forecast-error
  spread.
* **Reversal and lead-lag:**
  * Lo and MacKinlay's decomposition, computed and checked to the last digit;
  * size-decile lead-lag and its disappearance after 1990;
  * Roll's bounce, nonsynchronous trading, and horizon-dependence (reversal, industry momentum, long-run reversal).
* **Learning the residual:** a small network on 30-day residual paths against the s-score, with the deep-learning
  stat-arb literature.
* **Liquidity, crowding and decay:**
  * Grossman–Miller; Nagel's VIX test on industries;
  * Shleifer–Vishny's limits of arbitrage, and who demands immediacy;
  * August 2007, and decay.
* **For the researcher:** the optimal band for a mean-reverting spread.
  * The renewal-reward profit rate, and the first-passage times from Dynkin's formula.
  * The universal curve, and the frictionless limit σ√(κ/π).
  * The small-cost law m*/s_eq ≈ (3c/s_eq)^{1/3}.
  * Checked by simulation and on the industries.
* **The registered book:** the residual book with the research band, registered and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`statarb`](../../../explainer/quant/house/statarb.py) module).

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: two prices on an elastic band** (2.4). The promise; what this part finds; where it sits; four decades of
  stat arb; the plan.
* **1. From Morgan Stanley's back office to the quant firms** (2.8). Thorp; the APT group; D. E. Shaw; Renaissance;
  PDT; what changed.
* **2. Pairs by distance** (3.6).
  * The GGR rule on the 43 industries with complete histories since 1964.
  * One pair, Telecom/Business services in 2008H2.
  * By decade: −1.45 and −1.50 in the 1960s and 70s, 0.25 in the 1990s and 0.22 in the 2010s; overall Sharpe −0.25
    before costs.
  * Industry momentum; the literature; the short leg.
* **3. Cointegration and the screening problem** (3.9).
  * Engle–Granger at −3.34.
  * On average 7.3% of industry pairs pass a year, against a 3.7% false-positive rate; 8.1% of passes pass again.
  * Median half-life 7.6 days, biased short by selection.
  * Johansen; Royal Dutch/Shell; three answers to screening.
* **4. The Ornstein–Uhlenbeck spread** (3.4).
  * The model, its AR(1) form and the s-score.
  * Kendall's bias on 30, 60 and 250 days.
  * The half-life's interval: with b = 0.9, 6.6 days, but 2.9 days to no reversion at two standard errors.
  * Bertram and Leung–Li.
* **5. Eigenportfolios and residuals** (5.1).
  * Avellaneda and Lee's bands: gross Sharpe 0.88, net −0.39.
  * Eight variants all lose after costs (best gross 1.36, net −0.41); the research band: 1.13 gross, +0.21 net, at
    11% daily turnover.
  * Ten points of turnover cost about 0.39 of Sharpe.
  * By era, gross 1.46, 0.74, 1.11; net 0.59, −0.22, 0.15. Refinements; netting.
* **6. Hedge ratios that move** (2.9).
  * BTC/ETH: static β 0.96, ADF −1.40, half-life 279 days.
  * Kalman spread: ADF −14.8, half-life 1.3 days.
  * The effective window 1/√(q/r); the trap; lessons.
* **7. Reversal and lead-lag** (3.8).
  * The decomposition: size deciles, own −0.35 bp and cross +0.32 bp a week; industries, −0.12 and +0.15.
  * Large → small 0.15, small → itself 0.21.
  * The eras flip after 1990; Roll's bounce; horizons.
* **8. Learning the residual** (3.6).
  * The claim and the literature.
  * The House's network, 2017–2020: IC 0.0034; gross Sharpe 0.24 against the s-score's 1.26; after costs −7.2, at 95%
    daily turnover.
* **9. Liquidity, crowding and decay** (3.5).
  * The industry contrarian on the VIX: t = −0.26; Sharpe −0.66.
  * Limits of arbitrage; demanders of immediacy; August 2007; decay.
* **10. The residual book, registered and opened** (3.5).
  * 9 trials; the counter goes 23,541 → 23,550.
  * 2021–25: gross Sharpe 1.13, unchanged from research; net 0.30 (0.36 ± 0.44 on monthly returns), 1.1% a year at
    3.5% volatility.
  * Years −0.8%, +1.2%, +4.8%, −2.1%, +2.3%; break-even cost 6.2 and 6.9 bp a side.
  * The deflation bar for 9 trials, 0.29, above the research years' 0.21.
* **11. Rule 33: the stat-arb book** (4.3). The first sheet; labs (`ou_fit`, `s_score`, `band_rate`, `lo_mackinlay`);
  the module; Rule 33; capacity and monitoring; three cases.
* **For the researcher: the optimal band for a mean-reverting spread** (8.0).
  * The setup; two lemmas; the theorem.
  * The two times; rates for three costs; the universal curve.
  * The frictionless limit; the cube-root law and its check; a worked example.
  * Simulations; data; related results; open problems.
* **Recap, desk questions, problems** (3.9). Fourteen lines; six desk questions; the pause questions answered; twelve
  problems, two of qualifying-exam level, solved below.

## Hands-on

* **Built and run here:**
  * the distance rule;
  * year-by-year Engle–Granger screens with a random-walk control;
  * the Avellaneda–Lee residual book with nine configurations, gross and net;
  * a Kalman hedge ratio;
  * Lo–MacKinlay's decomposition;
  * a network on residual paths;
  * Nagel's VIX regression;
  * the optimal band, exactly and by simulation.
* **Labs, from the House's source:** `ou_fit`, `s_score`, `band_rate` with the two passage times, and `lo_mackinlay`.
* **Simulations against theory:** the band rate at nine (c, m) points, extrapolated to continuous monitoring; the
  small-cost law at six costs.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Vidyamurthy, *Pairs Trading* (2004) | distance and cointegration methods, the tradable spread | 2, 3 |
| Pole, *Statistical Arbitrage* (2007) | reversion, structural breaks, the 2000s decline | 1, 2, 9 |
| Chan, *Algorithmic Trading* (2013) | mean reversion, Johansen, the Kalman hedge ratio | 3, 4, 6 |
| Pedersen, *Efficiently Inefficient* (2015) | statistical arbitrage, liquidity provision, 2007 | 1, 9 |
| Leung and Li, *Optimal Mean Reversion Trading* (2016) | OU trading as optimal stopping | 4, research |

## Papers, chapter by chapter

* ch. 1: Thorp's own account (*A Man for All Markets*, 2017); Khandani and Lo (2007, 2011).
* ch. 2: Gatev, Goetzmann and Rouwenhorst (2006), *RFS*; Do and Faff (2010), *FAJ*; Moskowitz and Grinblatt (1999),
  *JF*; Engelberg, Reed and Ringgenberg (2018), *JF*.
* ch. 3: Engle and Granger (1987), *Econometrica*; Johansen (1991), *Econometrica*; Froot and Dabora (1999), *JFE*.
* ch. 4: Kendall (1954); Bertram (2010), *Physica A*; Leung and Li (2015), *IJTAF*.
* ch. 5: Avellaneda and Lee (2010), *Quantitative Finance*.
* ch. 7: Lo and MacKinlay (1990), *RFS*; Lehmann (1990), *QJE*; Jegadeesh (1990), *JF*; Roll (1984), *JF*; De Bondt and
  Thaler (1985), *JF*.
* ch. 8: Krauss, Do and Huck (2017), *EJOR*; Guijarro-Ordonez, Pelger and Zanotti (2021), arXiv:2106.04028.
* ch. 9: Grossman and Miller (1988), *JF*; Nagel (2012), *RFS*; Shleifer and Vishny (1997), *JF*; Shleifer (1986), *JF*;
  Coval and Stafford (2007), *JFE*.
* Research: Bertram (2010); Leung and Li (2015); Krauss (2017), *J. Economic Surveys*.

## For the researcher

* **The theorem.**
  * For dX = −κX dt + σ dW, the rule waits at 0, enters one unit against the deviation at |X| = m and exits at 0. It
    earns m − c per cycle.
  * By renewal-reward its long-run profit rate is R(m) = (m − c)/(E_0[τ_m] + E_{−m}[T_0]).
  * Dynkin's formula gives E_{−m}[T_0] = (2/σ²)∫_{−m}^0 e^{κy²/σ²}∫_{−∞}^y e^{−κz²/σ²} dz dy and
    E_0[τ_m] = (2/σ²)∫_0^m e^{κy²/σ²}∫_0^y e^{−κz²/σ²} dz dy.
  * Scaling gives R = s_eq κ g(m/s_eq, c/s_eq), so m*/s_eq = h(c/s_eq) is universal.
  * The frictionless limit is R(0⁺) = σ√(κ/π).
* **The small-cost law (new in this part).** In units m̃ = m/s_eq, with a = √(π/2):
  * κE_{−m}[T_0] = a m̃ − m̃²/2 + a m̃³/6 − m̃⁴/12 + O(m̃⁵);
  * κE_0[τ_m] = m̃²/2 + m̃⁴/12 + O(m̃⁶).
  * The quadratic and quartic terms cancel in the cycle length, so R ≈ (κ s_eq/a)(m̃ − c̃)/(m̃ + m̃³/6).
  * The optimum satisfies m̃*³ = 3c̃ + o(c̃), and R(m*)/R(0⁺) = 1 − ½(3c̃)^{2/3} + o(c̃^{2/3}).
  * Exact optimum against the law: c̃ = 0.0005, 0.002, 0.01, 0.05, 0.1, 0.3 give ratios 1.006, 0.999, 1.007, 1.020,
    1.032 and 1.070.
* **Measured.**
  * Simulations at dt = 0.002 and 0.0005, Richardson-extrapolated, match the theorem within a few percent at nine
    points, and the optimum wins in every case.
  * On the industries, the theory band (each residual's own c from its hedge) turned a −0.39 net Sharpe into +0.21 in
    research. On the sealed years it gave 0.30 net (1.13 gross).
* **Simplifications.**
  * Industry portfolios stand in for stocks.
  * A flat 5 bp a side on both legs, with each position's hedge charged separately.
  * A one-unit position, no stop-loss, and parameters estimated without correcting Kendall's bias.
* **Open problems.**
  * The band under parameter uncertainty and learning.
  * Breaks and stop-losses together.
  * The multi-spread free-boundary problem with a risk budget and square-root impact.

## Build it

```bash
python -m videos.quant.quant33.compute                            # every item; about ten minutes on 2 cores
python -m pytest -q tests/test_quant_house.py -k statarb
EXPLAINER_TTS=silent python tools/qa_scene.py quant33 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant33                                      # the narrated part
```

## Desk questions, with solutions

1. **Two prices are cointegrated: what do you trade, and what can go wrong?** The spread y − βx against its mean. What
   can go wrong:
   * the tie can break;
   * β is estimated on the same days;
   * a screen of 1,176 pairs at 5% passes about 59 by chance.
2. **What is an s-score?** (X_t − θ̂)/ŝ_eq for the OU fitted to a residual's cumulative sum over 60 days. Avellaneda and
   Lee enter beyond ±1.25 and exit near the mean.
3. **A Kalman spread with a one-day half-life: a pair?** Not on that evidence. It is the filter's one-step forecast
   error, close to white noise by construction. Test the profit out of sample.
4. **Where does a contrarian's profit come from?** E π = −(N − 1)/N²·tr Γ_1 + (ι'Γ_1ι − tr Γ_1)/N² − σ²(μ): own
   reversal, lead-lag, minus the dispersion of means.
5. **Why did the residual book lose with the standard bands?** About 20% daily turnover × 2 legs × 5 bp × 252 ≈ 5.2% a
   year, against 3.6% gross.
6. **How should the band depend on costs?** Through m*/s_eq = h(c/s_eq), with h(x) ≈ (3x)^{1/3} near zero. The speed
   scales the profit, not the band.

## Problems, with solutions

1. **Speed.** κ = −ln 0.9 = 0.105 a day; the half-life is ln 2/κ = 6.6 days.
2. **False passes.** 1,176 × 0.05 ≈ 59. Bonferroni at a 5% family-wise level tests each pair at 0.05/1,176 ≈
   4.3·10⁻⁵.
3. **A band from the curve.** c/s_eq = 0.6/2 = 0.3, so m* ≈ 1.03 s_eq ≈ 2.07% (the law gives 0.97 s_eq).
4. **A residual book after costs.** Gross 0.8 × 4% = 3.2%. Costs are 2 × 0.2 × 5 bp × 252 = 5.04%, so net ≈ −1.8% a
   year, a Sharpe of about −0.46.
5. **The cross term.** Γ_1 has one non-zero entry γ off the diagonal, so E π = (γ − 0)/N² with N = 2: γ/4.
6. **A filter's errors.** Nothing about cointegration. A slope of 0.3 says the filter is a little slow. Cointegration
   is a property of the prices, tested on a fixed combination out of sample.
7. **A reversal after costs.** 0.4 × 5 bp = 2 bp a day of costs: nothing is left.
8. **An IC's years.** se(IC) ≈ 1/√(N T), so 0.01 > 2/√(49 T) requires T > 816 days, about 3.2 years.
9. **A Sharpe ratio's years.** se ≈ 1/√T in years, so T > (2/0.3)² ≈ 44 years.
10. **The small-cost law.** m* ≈ (0.03)^{1/3} = 0.31 s_eq (exact 0.313). R/R(0⁺) ≈ 1 − ½·0.03^{2/3} = 1 − 0.048 =
    95.2% (exact 0.7598/0.7979 = 95.2%).
11. **(qual) The theorem.**
    * **Renewal.** By the strong Markov property the process restarts at 0 after each exit, so cycles are i.i.d. With
      finite expected length, the renewal-reward theorem gives R = E[reward]/E[length] = (m − c)/(E_0[τ_m] + E_{−m}[T_0]).
    * **Passage times.** f(x) = E_x[T] solves (σ²/2) f'' − κx f' = −1 with f = 0 on the boundary. Multiplying by
      e^{−κx²/σ²} gives (e^{−κx²/σ²} f')' = −(2/σ²) e^{−κx²/σ²}.
      * For T_0 from below, f' bounded at −∞ gives f'(y) = −(2/σ²) e^{κy²/σ²} ∫_{−∞}^y e^{−κz²/σ²} dz.
      * For τ_m from 0, symmetry gives f'(0) = 0.
      * Integrating once more gives the two formulas.
    * **Scaling.** Put X = s_eq X̃ and t = t̃/κ, with s_eq = σ/√(2κ). The generator becomes κ(½ f̃'' − x̃ f̃'), so the
      passage times are (1/κ)·T̃(m̃) and R = s_eq κ (m̃ − c̃)/T̃(m̃). Its maximiser depends on c̃ alone.
12. **(qual) The limits.**
    * **Expansions** (κ = 1, s_eq = 1, so σ² = 2 and a = √(π/2)).
      * I(y) = ∫_{−∞}^y e^{−z²/2} dz = a + y − y³/6 + …, and e^{y²/2} I(y) = a + y + a y²/2 + y³/3 + …. Integrating
        over [−m, 0] gives E_{−m}[T_0] = a m − m²/2 + a m³/6 − m⁴/12 + ….
      * Similarly e^{y²/2} ∫_0^y e^{−z²/2} dz = y + y³/3 + …, so E_0[τ_m] = m²/2 + m⁴/12 + ….
    * **Frictionless limit.** With c = 0, R = m/(a m + O(m³)) → 1/a = √(2/π). In general units this is σ√(κ/π).
    * **Cube-root law.** For c > 0, maximise (m − c)/(m + m³/6). The first-order condition is −m³/3 + c + c m²/2 = 0,
      so m*³ = 3c + O(c^{5/3}).
    * **Rate.** R(m*)/R(0⁺) = (1 − c/m)/(1 + m²/6) ≈ 1 − (3c)^{2/3}/3 − (3c)^{2/3}/6 = 1 − ½(3c)^{2/3}.

## Data and reproducibility

* **Kenneth French.** The 49 industry portfolios, daily, value-weighted (1926-07 to 2025-12, with research through
  2020); the daily size deciles. Each file is checked by SHA-256.
* **Binance.** Daily BTCUSDT and ETHUSDT bars (2018–2020).
* **Cboe.** The daily VIX close (1990–2020).
* **Registered:** `residual_sscore_part33`, charged with 9 trials (the eight Avellaneda–Lee variants and the research
  band, which was added after they failed).
  * The counter goes from 23,541 to 23,550.
  * The hold-out `kenfrench/industries49_daily` is sealed and was opened once.
  * Track Record row: research 0.22 ± 0.19 (324 months), hold-out 0.36 ± 0.44 (60 months), net of 5 bp a side.
* **Studied, not registered:**
  * distance pairs;
  * cointegration screens;
  * the Kalman spread;
  * the network (IC 0.0034, net Sharpe −7.2 on 2017–2020);
  * the industry contrarian.
* **Quoted, not computed:**
  * GGR's stock results;
  * Avellaneda and Lee's stock results;
  * Krauss–Do–Huck and Guijarro-Ordonez–Pelger–Zanotti;
  * Froot–Dabora;
  * Shleifer's index effect and Coval–Stafford.
  Firm histories (Princeton/Newport, Morgan Stanley's group, D. E. Shaw, Renaissance, PDT) are as reported.

---

# 量化金融，从零搭建 — 第33部分：统计套利

这是一套共四十三部分的量化金融系列的第33部分（见[系列计划](../README.md)与[教学大纲](../SYLLABUS.md)），也是第五幕"组合、策略与公司"（第30–38部分）的第四部分，按系列的博士层次构建。第32部分在各资产类别上跟随趋势；这一部分则逆着趋势下注，尺度是几天和单个证券：配对、协整价差、因子模型的残差，以及交易均值回归的数学。

资产范围是Kenneth French的49个美国行业日度组合，研究期到2020年，2021–2025年封存。辅助数据：

* French的日度规模十分位组合（从1963年起的周度领先-滞后）；
* Binance的BTC与ETH日K线（卡尔曼一章，2018–2020年）；
* Cboe的VIX（流动性检验，1990–2020年）。

每个数字都由本系列自己的代码算出（[`compute.py`](compute.py)和本系列公司的[`statarb`](../../../explainer/quant/house/statarb.py)模块）。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：橡皮筋上的两个价格**（2.4）。教科书的承诺、本部分的发现、在系列中的位置、四十年的统计套利、本部分的安排。
* **1. 从摩根士丹利的后台到量化公司**（2.8）。Thorp；APT小组；D. E. Shaw；文艺复兴；PDT；什么改变了。
* **2. 距离法配对**（3.6）。
  * 在1964年以来历史完整的43个行业上运行GGR规则。
  * 一对：2008年下半年的电信/商业服务。
  * 按十年：1960和70年代为−1.45和−1.50，1990年代0.25，2010年代0.22；全期扣除成本前夏普比率−0.25。
  * 行业动量；文献；空头那条腿。
* **3. 协整与筛选问题**（3.9）。
  * 恩格尔-格兰杰临界值−3.34。
  * 每年平均7.3%的行业配对通过，而假阳性率为3.7%；通过者中8.1%再次通过。
  * 半衰期中位数7.6天，因选择而偏短。
  * Johansen；荷兰皇家/壳牌；筛选问题的三种答案。
* **4. 奥恩斯坦-乌伦贝克价差**（3.4）。
  * 模型、其AR(1)形式与s分数。
  * 30、60、250天上的肯德尔偏差。
  * 半衰期的区间：b = 0.9时为6.6天，但两个标准误覆盖从2.9天到不回归。
  * Bertram与Leung–Li。
* **5. 特征组合与残差**（5.1）。
  * Avellaneda和Lee的区间：毛夏普0.88，净−0.39。
  * 八个变体扣除成本后全部亏损（毛夏普最高1.36，净−0.41）；研究区间：毛1.13，净+0.21，日换手11%。
  * 每十个百分点的换手约损失0.39的夏普比率。
  * 分时代：毛1.46、0.74、1.11；净0.59、−0.22、0.15。改进；轧差。
* **6. 会变的对冲比率**（2.9）。
  * BTC/ETH：静态β 0.96，ADF −1.40，半衰期279天。
  * 卡尔曼价差：ADF −14.8，半衰期1.3天。
  * 有效窗口1/√(q/r)；陷阱；教训。
* **7. 反转与领先-滞后**（3.8）。
  * 分解：规模十分位组合自身项每周−0.35个基点，交叉项+0.32；行业为−0.12和+0.15。
  * 大盘→小盘0.15，小盘→自身0.21。
  * 1990年后时代翻转；Roll的反弹；期限。
* **8. 学习残差**（3.6）。
  * 论断与文献。
  * 本系列公司的网络，2017–2020年：IC 0.0034；毛夏普0.24，s分数为1.26；扣除成本后−7.2，日换手95%。
* **9. 流动性、拥挤与衰减**（3.5）。
  * 行业逆向策略对VIX：t = −0.26；夏普−0.66。
  * 套利的极限；即时性的需求者；2007年8月；衰减。
* **10. 残差组合，登记并打开**（3.5）。
  * 9次试验；计数器从23,541变为23,550。
  * 2021–25年：毛夏普1.13，与研究期相同；净0.30（月度收益计0.36 ± 0.44），每年1.1%，波动率3.5%。
  * 各年−0.8%、+1.2%、+4.8%、−2.1%、+2.3%；盈亏平衡成本每边6.2和6.9个基点。
  * 9次试验的紧缩门槛0.29，高于研究期的0.21。
* **11. 第33条规则：统计套利组合**（4.3）。第一张汇总表；代码实验（`ou_fit`、`s_score`、`band_rate`、`lo_mackinlay`）；模块；第33条规则；容量与监控；三个案例。
* **写给研究者：均值回归价差的最优交易区间**（8.0）。
  * 设定；两个引理；定理。
  * 两个时间；三种成本下的速率；普适曲线。
  * 无摩擦极限；立方根定律及其检验；算例。
  * 模拟；数据；相关结果；开放问题。
* **回顾、交易台问题与习题**（3.9）。十四行回顾；六个交易台问题；暂停题的答案；十二道习题，其中两道是资格考试水平，解答见下。

## 写给研究者

* **定理。**
  * 对dX = −κX dt + σ dW，规则在0处等待，在|X| = m时逆着偏离进场一个单位，在0处出场，每个周期赚m − c。
  * 由更新-报酬定理，长期利润率为R(m) = (m − c)/(E_0[τ_m] + E_{−m}[T_0])，两个首达时间由迪金公式给出。
  * 尺度变换给出R = s_eq κ g(m/s_eq, c/s_eq)，所以m*/s_eq = h(c/s_eq)是普适的。
  * 无摩擦极限为R(0⁺) = σ√(κ/π)。
* **小成本定律（本部分新增）。**
  * 以m̃ = m/s_eq为单位，κE_{−m}[T_0] = a m̃ − m̃²/2 + a m̃³/6 − …，κE_0[τ_m] = m̃²/2 + m̃⁴/12 + …，其中a = √(π/2)。
  * 二次项和四次项在周期长度中抵消，所以m̃*³ = 3c̃ + o(c̃)，且R(m*)/R(0⁺) = 1 − ½(3c̃)^{2/3} + o(c̃^{2/3})。
  * 与精确最优值之比在c̃ = 0.0005到0.3之间为0.999至1.070。
* **测量。**
  * 在dt = 0.002和0.0005上模拟并做理查森外推，九个点上都与定理相差几个百分点以内。
  * 在行业上，理论区间把净夏普从−0.39变为研究期的+0.21，封存年份上净0.30。
* **简化。**
  * 用行业组合代替股票。
  * 两条腿每边统一5个基点，每个头寸的对冲分别收费。
  * 一个单位的头寸，没有止损，参数估计未校正肯德尔偏差。
* **开放问题。**
  * 参数不确定与学习下的区间。
  * 断裂与止损并存。
  * 带风险预算和平方根冲击的多价差自由边界问题。

## 交易台问题与解答

1. **两个价格协整：交易什么，可能出什么错？** 交易价差y − βx相对其均值的偏离。可能出错的地方：
   * 联系可能断裂；
   * β是在同样的日子上估计的；
   * 在5%水平上筛选1,176对，约59对会偶然通过。
2. **什么是s分数？** 对残差累计和最近60天拟合OU过程后的(X_t − θ̂)/ŝ_eq；Avellaneda和Lee在±1.25之外进场，在均值附近出场。
3. **半衰期一天的卡尔曼价差是配对吗？** 凭这个证据不是：它是滤波器的一步预测误差，按构造接近白噪声。应在样本外检验利润。
4. **逆向策略的利润从哪里来？** E π = −(N − 1)/N²·tr Γ_1 + (ι'Γ_1ι − tr Γ_1)/N² − σ²(μ)：自身反转、领先-滞后，减去均值的离散度。
5. **为什么用标准区间的残差组合会亏钱？** 约20%日换手 × 2条腿 × 5个基点 × 252 ≈ 每年5.2%，而毛收益是3.6%。
6. **区间应如何依赖成本？** 通过m*/s_eq = h(c/s_eq)，在零附近h(x) ≈ (3x)^{1/3}。速度缩放利润，而不移动区间。

## 习题与解答

1. **速度。** κ = −ln 0.9 = 每天0.105；半衰期ln 2/κ = 6.6天。
2. **假通过。** 1,176 × 0.05 ≈ 59；邦费罗尼校正下，每对的检验水平为0.05/1,176 ≈ 4.3·10⁻⁵。
3. **从曲线读出区间。** c/s_eq = 0.6/2 = 0.3，所以m* ≈ 1.03 s_eq ≈ 2.07%（定律给出0.97 s_eq）。
4. **扣除成本后的残差组合。** 毛收益0.8 × 4% = 3.2%；成本2 × 0.2 × 5个基点 × 252 = 5.04%；净约每年−1.8%，夏普约−0.46。
5. **交叉项。** Γ_1只有一个非对角元素γ，所以N = 2时E π = γ/N² = γ/4。
6. **滤波器的误差。** 与协整无关：斜率0.3说明滤波器稍慢。协整是价格的性质，要在样本外对一个固定组合检验。
7. **扣除成本后的反转。** 0.4 × 5个基点 = 每天2个基点的成本：什么也不剩。
8. **信息系数需要的年数。** se(IC) ≈ 1/√(N T)，0.01 > 2/√(49 T)要求T > 816天，约3.2年。
9. **夏普比率需要的年数。** 以年计se ≈ 1/√T，所以T > (2/0.3)² ≈ 44年。
10. **小成本定律。** m* ≈ (0.03)^{1/3} = 0.31 s_eq（精确值0.313）；R/R(0⁺) ≈ 1 − ½·0.03^{2/3} = 95.2%（精确值95.2%）。
11. **（资格考试）定理。**
    * **更新。** 由强马尔可夫性，每次出场后过程在0处重新开始，各周期独立同分布；周期期望长度有限时，更新-报酬定理给出R = E[报酬]/E[长度]。
    * **首达时间。** f(x) = E_x[T]满足(σ²/2) f'' − κx f' = −1，边界上f = 0。乘以e^{−κx²/σ²}得(e^{−κx²/σ²} f')' = −(2/σ²) e^{−κx²/σ²}。
      * 对从下方到达的T_0，f'在−∞处有界。
      * 对从0出发的τ_m，由对称性f'(0) = 0。
      * 再积分一次即得两个公式。
    * **尺度。** 令X = s_eq X̃、t = t̃/κ，生成元变为κ(½ f̃'' − x̃ f̃')，所以R = s_eq κ (m̃ − c̃)/T̃(m̃)，其最大值点只依赖于c̃。
12. **（资格考试）极限。**
    * **展开**（κ = 1，s_eq = 1，σ² = 2，a = √(π/2)）。
      * I(y) = a + y − y³/6 + …，e^{y²/2} I(y) = a + y + a y²/2 + y³/3 + …，在[−m, 0]上积分得E_{−m}[T_0] = a m − m²/2 + a m³/6 − m⁴/12 + …。
      * 同理E_0[τ_m] = m²/2 + m⁴/12 + …。
    * **无摩擦极限。** c = 0时R → 1/a = √(2/π)，一般单位下即σ√(κ/π)。
    * **立方根定律。** c > 0时最大化(m − c)/(m + m³/6)，一阶条件为−m³/3 + c + c m²/2 = 0，故m*³ = 3c + O(c^{5/3})。
    * **速率。** R(m*)/R(0⁺) ≈ 1 − (3c)^{2/3}/3 − (3c)^{2/3}/6 = 1 − ½(3c)^{2/3}。

## 数据与复现

* **Kenneth French。** 49个行业日度市值加权组合（1926-07至2025-12，研究期到2020年），以及日度规模十分位组合，均以SHA-256校验。
* **Binance。** BTCUSDT和ETHUSDT日K线（2018–2020年）。
* **Cboe。** VIX日收盘（1990–2020年）。
* **已登记：** `residual_sscore_part33`，按9次试验计（八个Avellaneda–Lee变体，以及在它们失败之后加入的研究区间）。
  * 计数器从23,541变为23,550。
  * 封存数据`kenfrench/industries49_daily`只打开一次。
  * 业绩记录：研究期0.22 ± 0.19（324个月），封存期0.36 ± 0.44（60个月），已扣除每边5个基点。
* **研究过、未登记：**
  * 距离法配对；
  * 协整筛选；
  * 卡尔曼价差；
  * 网络（IC 0.0034，2017–2020年净夏普−7.2）；
  * 行业逆向策略。
* **引用、未计算：**
  * GGR与Avellaneda–Lee在股票上的结果；
  * Krauss–Do–Huck与Guijarro-Ordonez–Pelger–Zanotti；
  * Froot–Dabora；
  * Shleifer的指数效应与Coval–Stafford。
  公司历史（Princeton/Newport、摩根士丹利的小组、D. E. Shaw、文艺复兴、PDT）均为公开报道。
