# Quant, Built — Part 40: Measuring Risk

Part 40 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VII, The System, built to the series' PhD layer. It asks how a
firm says how much it could lose: how risk numbers are made, how they are checked, what can and cannot be checked,
and what they cannot see.

Measurement uses Kenneth French's daily US market return from July 1926 to December 2020, with its size and value
factors, and his 49 value-weighted industries, daily, to 2020. All of it lies in the series' research window; the
sealed hold-out is not opened. Bitcoin's daily closes (2017–2020) give one comparison.

The models:
* Gaussian, Student-t, historical simulation and RiskMetrics;
* filtered historical simulation on EWMA and GJR-GARCH residuals, and McNeil and Frey's GARCH with a generalised
  Pareto tail;
* CAViaR and a quantile network;
* Gaussian and t copulas, the reverse stress test and the rearrangement algorithm.

The part covers:

* **Value at risk, three ways:**
  * definitions; RiskMetrics (λ = 0.94);
  * **$100m in the US market at end-2007:**

    | Method | VaR, $m | ES, $m |
    |---|---|---|
    | normal | 1.9 | 2.2 |
    | historical simulation | 2.5 | 2.8 |
    | Student-t (ν ≈ 3.2) and its Monte Carlo | 2.4 | 3.6 |
    | RiskMetrics (EWMA) | 2.8 | 3.2 |

  * **On 15 October 2008** the 500-day methods said 3.4–4.2 and RiskMetrics 10.0, against a loss of 8.8.
  * **The square-root-of-time rule:** 9.7% against 10.5% directly. By decade the ratio runs from 0.89 (1990s) to
    1.34 (1970s).
  * **A delta-hedged short straddle book:** delta-normal VaR 0; delta-gamma $729; full revaluation $615; with a
    5-point vol rise, $1,601.
* **Coherence:**
  * two independent bonds: VaR 0 + 0 against 100 together, ES 80 + 80 against 103.2;
  * the axioms (Artzner, Delbaen, Eber and Heath 1999); ES as a supremum over scenarios; normal ES (2.67σ at 99%,
    2.34σ at 97.5%); spectral and convex measures;
  * Euler allocation: on a market + SMB + HML book, HML carries 9.2% of ES against 6.5% of variance.
* **Backtesting, 1928–2020, 24,396 forecasts each:**

  | Forecaster | Exceeded (target 1%) | Kupiec, independence | Z2 | Red years |
  |---|---|---|---|---|
  | normal on 500 days | 2.24% | both fail; π11 = 12% | +1.92 | 22 |
  | historical simulation | 1.52% | both fail | +0.62 | 11 |
  | RiskMetrics | 2.16% | both fail | +1.60 | 12 |
  | filtered HS on EWMA | 1.19% | both fail | +0.21 | 0 |
  | **filtered HS on GJR-GARCH** | **0.88%** | **pass (p = 0.057, 0.94)** | **−0.09** | **1** |
  | GJR with an EVT tail | 0.69% | Kupiec fails: too cautious | −0.25 | 3 |

  * Z2's simulated 5% critical value is 0.11 for normal and 0.12 for t(4) losses.
* **Extreme-value theory:**
  * the 1987 crash was 16σ, a normal probability of about 10⁻⁵⁹; excess kurtosis 16.7;
  * Pickands–Balkema–de Haan;
  * POT above the 95th percentile (1,244 days): ξ = 0.197, a tail exponent of about 5, stable across thresholds
    (ξ between 0.19 and 0.23);
  * at 99.99%, EVT gives VaR 11.7% and ES 15.2%, against the normal's 4.0%;
  * Hill from 4.3 to 2.2 across k; the US right tail ξ = 0.29; Bitcoin's losses ξ = 0.26;
  * McNeil–Frey.
* **Dependence and copulas:**
  * correlation's pitfalls; Sklar; Gaussian against t copulas;
  * **joint worst-1% days:** Banks–Insurance 0.67 in the data against 0.40 under a Gaussian copula; Oil–Mines 0.52
    against 0.23;
  * the t copula leaves the 99% VaR nearly unchanged but raises the 99.9% ES from 15.4% to 18.5%;
  * conditional correlation's bias: 0.51 on crash days against 0.56 overall;
  * Li's copula and 2007–08.
* **Stress tests:**
  * historical days on the factor book: 1987 $13.8m (18.8σ), 2008 $8.3m, 2020 $12.5m;
  * the worst ten-day windows: −35.4% (Oct 1929) to −25.5% (Mar 2020);
  * supervisory stress tests;
  * **the reverse stress test** x* = −LΣw/(wᵀΣw): a $10m loss at 8.2σ; Studer's maximum loss.
* **Model uncertainty (the rearrangement algorithm):**
  * for three Pareto losses at 99%, the worst-case VaR is 1.48×, 1.70× and 1.98× the sum of the VaRs at tail
    exponents 3, 2 and 1.5;
  * the ES bound; aggregation;
  * the estimation error of a 500-day quantile (about 7%);
  * JPMorgan's 2012 VaR model change, as reported.
* **Learned risk, trained to 1990 and tested on 1991–2020:**

  | Forecaster | Pinball (bp) | Exceeded | Kupiec p |
  |---|---|---|---|
  | GJR-filtered HS | **3.41** | 0.99% | 0.95 |
  | CAViaR (β₁ = 0.86) | 3.48 | 1.05% | 0.70 |
  | quantile network | 3.59 | 1.31% | 0.010 |
  | historical simulation | 4.43 | 1.61% | 0.000 |

  * **Diebold–Mariano, against GJR-filtered HS:** t = 1.83 for the network and 1.92 for CAViaR. Neither is
    significant.
* **Regulation and liquidity:**
  * Basel 1996, Basel 2.5, FRTB (97.5% ES, liquidity horizons, stressed calibration, desk approval, P&L attribution);
  * the √(LH/10) scaling, illustrated;
  * Bangia et al.'s liquidity-adjusted VaR, and impact (Part 37);
  * CCP margin and procyclicality.
* **Rule 40: a risk number is a forecast.** The answer; the sheet; the evening report; governance; the desks; four
  labs; three cases.
* **For the researcher: what can be backtested?**
  * The pinball lemma; Osband's convex level sets; ES not elicitable (constructed); Rockafellar–Uryasev;
    Fissler–Ziegel; the FZ0 derivative.
  * **Checks:**
    * level sets;
    * the FZ0 grid minimum at the truth on a t₄ sample;
    * forecasters ranked by FZ0 with DM t-statistics from 6.7 to 11.1;
    * power with only the tail wrong: Kupiec 5.9%, Z2 32%.
  * Comparative backtests; expectiles.

No strategy is registered in this part; the trial counter stays at 23,559.

*An education in methods, not investment advice.*

## Chapters (about 53 minutes)

* **Hook: ten-day VaR from one-day.** The question; three findings; why it matters; three things a risk number is
  not; where this sits; seventy years; the plan.
* **1. Value at risk, three ways.** Definitions; a picture; RiskMetrics; three methods; end-2007; October 2008; the
  square root; by decade; options; what the number says.
* **2. Coherent risk measures.** Two bonds; the axioms; VaR's record; ES; its normal form; spectral; convex; Euler
  allocation; which.
* **3. Backtesting.** Kupiec; the traffic light; Christoffersen; six forecasters; 2008; year by year; red years; Z2;
  lessons.
* **4. Extreme value theory.** Fat tails; the theorem; POT; the fit; thresholds; beyond the data; Hill; other tails;
  McNeil–Frey; cautions.
* **5. Dependence and copulas.** Pitfalls; Sklar; points; tail dependence; industries; a portfolio under two copulas;
  conditional correlation; Li; lessons.
* **6. Stress tests.** Why; historical days; ten-day windows; supervisory tests; reverse stress; its table; maximum
  loss; limits.
* **7. Model uncertainty.** The problem; the algorithm; animated; results; the ES bound; aggregation; estimation
  error; JPMorgan 2012.
* **8. Learned risk.** The pinball loss; CAViaR; the network; results; 2008; Diebold–Mariano; why not; what would do
  better.
* **9. Regulation and liquidity.** Three generations; FRTB; horizons; stressed calibration; desks; LVaR; impact; CCP
  margin.
* **10. Rule 40.** The answer; the sheet; the report; governance; the desks; four labs; the module; three cases.
* **For the researcher: what can be backtested?**
  * Scores; two lemmas; the theorem; check one.
  * Rockafellar–Uryasev; Fissler–Ziegel; half a proof; checks two to four.
  * Comparative backtests; expectiles; related work; open problems.
* **Outro.** Thirteen lines; three lessons; the part on one card; connections; six desk questions; the pause answer;
  twelve problems (two of qualifying-exam level, solved below); payoffs; references.

## Hands-on

* **Built and run here:**
  * six one-day forecasters over 93 years, with Kupiec, Christoffersen, the traffic light and Z2, and Z2's
    simulated null;
  * GPD fits across thresholds and Hill plots;
  * empirical tail dependence of 49 industries, and portfolios under Gaussian and t copulas;
  * historical and reverse stress tests;
  * the rearrangement algorithm;
  * a delta-hedged option book by delta-normal, delta-gamma and full revaluation;
  * CAViaR and a quantile network with Diebold–Mariano tests;
  * the FZ0 score's grid;
  * a Monte Carlo of the power of Kupiec against Z2.
* **Labs, from the House's source:** `christoffersen`, `evt_var_es`, `reverse_stress`, `rearrangement`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| McNeil, Frey and Embrechts, *Quantitative Risk Management* (2015) | VaR, ES, EVT, copulas, aggregation, backtesting | 1–7 |
| Jorion, *Value at Risk* (2006) | methods, backtesting, Basel | 1, 3, 9 |
| Föllmer and Schied, *Stochastic Finance* (2016), ch. 4 | coherent and convex risk measures | 2 |
| Hull, *Risk Management and Financial Institutions* (2018) | regulation, FRTB, liquidity | 9 |

## Papers, chapter by chapter

* ch. 1: J.P. Morgan/Reuters (1996), *RiskMetrics*; Roy (1952), *Econometrica*.
* ch. 2: Artzner, Delbaen, Eber and Heath (1999), *Mathematical Finance*; Acerbi and Tasche (2002), *JBF*; Acerbi
  (2002), *JBF*; Föllmer and Schied (2002), *Finance and Stochastics*; Tasche (1999).
* ch. 3: Kupiec (1995), *J. Derivatives*; Christoffersen (1998), *IER*; Acerbi and Székely (2014), *Risk*.
* ch. 4: Balkema and de Haan (1974); Pickands (1975); Hill (1975); McNeil and Frey (2000), *J. Empirical Finance*.
* ch. 5: Sklar (1959); Embrechts, McNeil and Straumann (2002); Boyer, Gibson and Loretan (1997); Forbes and Rigobon
  (2002), *JF*; Li (2000), *J. Fixed Income*.
* ch. 6: Breuer, Jandačka, Rheinberger and Summer (2009), *IJCB*; Studer (1999).
* ch. 7: Embrechts, Puccetti and Rüschendorf (2013), *JBF*; JPMorgan Chase Management Task Force (2013) and the US
  Senate Permanent Subcommittee on Investigations (2013), on the CIO losses.
* ch. 8: Engle and Manganelli (2004), *JBES*; Koenker and Bassett (1978), *Econometrica*.
* ch. 9: Bangia, Diebold, Schuermann and Stroughair (1999); Basel Committee (1996, 2009, 2019).
* Research: Osband (1985); Gneiting (2011), *JASA*; Fissler and Ziegel (2016), *Annals of Statistics*; Ziegel
  (2016), *Mathematical Finance*; Bellini and Bignozzi (2015), *Quantitative Finance*; Nolde and Ziegel (2017),
  *Annals of Applied Statistics*; Patton, Ziegel and Chen (2019), *J. Econometrics*; Rockafellar and Uryasev (2000),
  *J. Risk*.

## For the researcher

* **Elicitability.** T is elicitable if some scoring function S makes T(F) the unique minimiser of E_F S(x, Y).
* **Lemma 1 (quantiles).** d/dq E ℓ_τ(q, Y) = F(q) − τ, so the pinball loss elicits the τ-quantile; VaR is elicitable.
* **Lemma 2 (Osband).** Elicitable functionals have convex level sets. If T(F₀) = T(F₁) = t, the mixture's expected
  score is the mixture of expected scores, each minimised at t.
* **Theorem (ES is not elicitable).** F₀ = δ₁ and F₁ = 0.95δ₀ + 0.05δ₂ both have ES₉₀% = 1, but their half-half
  mixture has ES = 1.25.
* **Rockafellar–Uryasev.** ES_α = min_v{v + E(L − v)⁺/(1 − α)}, minimised at VaR_α.
* **Fissler–Ziegel (stated).** (VaR, ES) is jointly elicitable. In the FZ0 form,
  S(v, e; r) = −1{r ≤ v}(v − r)/(τe) + v/e + log(−e) − 1, for e < v < 0.
  * **Half of the proof.** For the true v, ∂_e E S = 0 iff e = E[R | R ≤ v].
* **Measured.**
  * **Level sets.** VaR is unchanged by mixing; ES goes from 1, 1 to 1.25.
  * **The FZ0 grid.** On 400,000 t₄ draws at τ = 2.5% the minimum is exactly at (VaR, ES) = (−1.96%, −2.82%).
  * **Ranking, 1928–2020 at 97.5%.** The GJR-filtered HS is best, ahead of EVT, EWMA-FHS, RiskMetrics, HS and the
    normal, with DM t = 6.7–11.1.
  * **Power over 1,000 days** (true t₃, a normal forecast with the right 99% VaR, ES 3.00 against 4.04). Kupiec
    rejects 5.9%, its size; Z2 rejects 32% at its simulated 5% critical value of 0.53.
* **Simplifications.**
  * One market index; daily data.
  * Univariate forecasters.
  * Fixed refit schedules (GJR every 1,250 days).
  * The network's features are daily.
* **Open problems.**
  * Powerful ES tests in one or two years of data.
  * Elicitability of systemic measures (CoVaR).
  * Scores aligned with the losses that matter to a bank.

## Build it

```bash
python -m videos.quant.quant40.compute                            # every item; a few minutes
python -m pytest -q tests/test_quant_house.py -k risk_var
EXPLAINER_TTS=silent python tools/qa_scene.py quant40 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant40                                      # the narrated part
```

## Desk questions, with solutions

1. **VaR $10m one-day; ten-day?**
   * √10 × 10 = $31.6m, assuming iid normal days.
   * On the US market since 1926 the ratio of ten-day to one-day 99% VaR is 3.4, and 4.2 in the 1970s.
2. **Why is VaR not coherent?**
   * It is not subadditive: two independent 4% defaults have 95% VaRs of 0 each and 100 together.
   * ES is coherent.
3. **How do you backtest VaR?**
   * Count exceptions (Kupiec) and test their independence (Christoffersen); apply the traffic light.
   * Use decades: one year has little power.
4. **Beyond the data?**
   * EVT: fit a generalised Pareto to exceedances, after filtering volatility (McNeil–Frey).
   * The US tail exponent is about 5.
5. **What does correlation miss?**
   * Tail dependence. The Gaussian copula has none.
   * Banks and insurers crash together 0.67 of the time, against the Gaussian's 0.40.
6. **Can ES be backtested?**
   * Not alone: it is not elicitable. Jointly with VaR it is (FZ0).
   * Acerbi–Székely's Z2 uses VaR's exceptions.

## Problems, with solutions

1. **Normal.** With σ = 1%, VaR₉₉ = 2.33% and ES₉₉ = 2.67%; VaR₉₇.₅ = 1.96% and ES₉₇.₅ = 2.34%.
2. **Autocorrelation.**
   * Var(Σ₁₀ r) = σ²[10 + 2Σ_{k=1}^{9}(10 − k)0.1^k] = 11.98σ².
   * The factor is √11.98 = 3.46, against √10 = 3.16.
3. **Bonds at 3%.**
   * Each VaR₉₅ is 0, because 3% < 5%.
   * P(one or more) = 1 − 0.97² = 5.91% > 5%, so the joint VaR₉₅ is 100.
4. **Kupiec.** With x = 8 and T = 250, LR = 7.73 and p = 0.005. The zone is yellow (multiplier 3.75).
5. **Clustering.**
   * π₁₁ = 4/10 = 0.40 and π₀₁ ≈ 6/989 = 0.006.
   * An exception makes another 65 times as likely: the model ignores volatility.
6. **EVT.**
   * VaR = 0.02 + (0.008/0.2)[(10,000/400 × 0.001)^−0.2 − 1] = 6.37%.
   * ES = (0.0637 + 0.008 − 0.004)/0.8 = 8.46%.
7. **t copula.** λ = 2t₅(−√(5 × 0.5/1.5)) = 2t₅(−1.29) = 0.253.
8. **Reverse stress.** The distance is 16/2 = 8σ, along −Σw: each factor moves in proportion to its covariance with
   the portfolio.
9. **Dependence bound.** Worst VaR ≤ ΣES = 3 × 19 = 57. The rearrangement algorithm gives 46.
10. **FRTB.** 5 × √(60/10) = $12.2m.
11. **(qual) Elicitability.**
    * **Lemma 1.** E ℓ_τ(q, Y) = ∫_{y<q}(1 − τ)(q − y)dF + ∫_{y≥q}τ(y − q)dF. Its derivative is
      (1 − τ)F(q) − τ(1 − F(q)) = F(q) − τ, and the function is convex in q, so the minimiser is F⁻¹(τ).
    * **Lemma 2.** If S is strictly consistent and T(F₀) = T(F₁) = t, then for every x,
      E_{F_λ}S(x, Y) = λE_{F₁}S(x, Y) + (1 − λ)E_{F₀}S(x, Y) ≥ E_{F_λ}S(t, Y), with equality only at x = t.
      So T(F_λ) = t.
    * **ES fails.** The pair F₀ and F₁ above violates Lemma 2.
    * **Rockafellar–Uryasev.** g(v) = v + E(L − v)⁺/(1 − α) is convex with g′(v) = 1 − P(L > v)/(1 − α), which is zero
      at VaR_α. At v = VaR, g = VaR + E[(L − VaR)1{L > VaR}]/(1 − α) = E[L | L ≥ VaR] = ES (for continuous L).
12. **(qual) Foundations of ES tests.**
    * **E[Z₂] = 0.** E[L_t I_t] = (1 − α)ES_t for correct forecasts of a continuous loss. Hence
      E[Σ L_t I_t/ES_t] = T(1 − α), and E[Z₂] = 0.
    * **Z₂ detects an ES that is too low.** If VaR is right and ES_f < ES, then E[Z₂] = ES/ES_f − 1 > 0.
    * **FZ0 in e.** With v fixed at the true quantile,
      ∂_e E S = e⁻²(E[(v − R)1{R ≤ v}]/τ − v) + e⁻¹.
      This is zero at e = v − E[(v − R)1{R ≤ v}]/τ = E[R | R ≤ v], because P(R ≤ v) = τ. The second derivative is
      positive there, so the expected score is minimised at the true ES.

## Data and reproducibility

* **Kenneth French's library.**
  * Daily factors (Mkt-RF + RF, SMB, HML) and 49 industries, through 2020-12-31, frozen subsets checked against the
    manifest.
  * The hold-out is not used.
* **Binance.** BTCUSDT daily closes, 2017-08 to 2020-12.
* **Simulation.**
  * Copulas, the FZ0 grid, the power study and Z2's null, with seeds fixed in `compute.py`.
  * The option book under Black–Scholes.
* **No registration.** The counter stays at 23,559.
* **Quoted, not computed.**
  * The JPMorgan CIO episode (task force and Senate reports).
  * Basel and FRTB rules.
  * CCP margin in March 2020, as reported.

---

# 量化金融，从零搭建 — 第40部分：度量风险

四十三部分量化金融系列的第40部分，第七幕“体系”的第一部分，按本系列的博士层次构建。它追问一家公司如何说明自己可能亏多少：风险数字如何得出、如何检验、什么能检验什么不能，以及它们看不见什么。

测量使用Kenneth French的美国市场日收益（1926年7月至2020年12月）与四十九个行业的日收益，全部在研究窗口之内，不打开留出期。

本部分涵盖：
* **VaR的三种算法**：
  * 2007年底与2008年10月的对比；
  * 时间平方根法则低估（9.7%对10.5%）；
  * delta对冲的跨式空头组合：delta-正态VaR为零，完全重新估值为615美元。
* **一致性**：
  * 两只债券的反例；
  * 预期亏损的上确界表示与谱、凸风险度量；
  * 欧拉分配。
* **回测（1928–2020）**：
  * 正态法被突破2.24%、成簇出现，Z2 = +1.92；
  * GJR过滤的历史模拟法0.88%，通过全部检验。
* **极值理论**：1987年崩盘是16个标准差；ξ = 0.197，尾部指数约为五，在不同阈值下稳定。
* **相依性**：银行与保险的共同最糟日子为0.67，高斯为0.40；t Copula使99.9%的预期亏损从15.4%升到18.5%。
* **压力测试**：历史情景、十日窗口、反向压力（一千万美元亏损在8.2个标准差处）。
* **模型不确定性**：重排算法给出最坏VaR为VaR之和的1.5到2倍；摩根大通2012年的模型变更。
* **学习出来的风险**：CAViaR和网络都没有胜过GJR过滤法。
* **监管与流动性**：FRTB、流动性期限、流动性调整VaR、清算所保证金。
* **第40条规则**：风险数字是一种预测。
* **写给研究者**：
  * VaR可引出，预期亏损不可，两者合在一起可以；
  * FZ0评分；
  * 只有尾部出错时，Kupiec的拒绝率为5.9%，Z2为32%。

本部分不登记策略，计数器仍为23,559。

*这是方法教育，不是投资建议。*

## 章节（约53分钟）

* **开场**：交易台问题、三个发现、为什么重要、风险数字不是什么、七十年的历史、计划。
* **1. VaR的三种算法**：定义、RiskMetrics、三种方法、2007与2008、平方根法则、期权。
* **2. 一致性风险度量**：两只债券、公理、预期亏损、谱与凸度量、欧拉分配。
* **3. 回测**：Kupiec、红绿灯、Christoffersen、六个预测者、2008年、逐年、Z2。
* **4. 极值理论**：定理、超阈值峰值、阈值稳定性、超出数据、Hill、其他尾部、McNeil–Frey。
* **5. 相依性与Copula**：陷阱、Sklar、尾部相依、行业数据、两种Copula下的组合、条件相关、Li。
* **6. 压力测试**：历史情景、十日窗口、监管压力测试、反向压力、最大损失。
* **7. 模型不确定性**：重排算法、结果、预期亏损界、加总、估计误差、摩根大通2012。
* **8. 学习出来的风险**：弹球损失、CAViaR、网络、结果、Diebold–Mariano、原因。
* **9. 监管与流动性**：三代规则、FRTB、期限、压力校准、流动性调整VaR、冲击、清算所保证金。
* **10. 第40条规则**：汇总表、晚间报告、治理、各交易台、四个实验、三个案例。
* **写给研究者**：
  * 评分、两个引理、定理；
  * Rockafellar–Uryasev、Fissler–Ziegel、一半的证明；
  * 四项检验、比较式回测、期望分位数、开放问题。
* **结尾**：回顾、教训、公式卡、联系、交易台问题、习题（两道资格考试题，解答见下文）。

## 写给研究者

* **引理一**：弹球损失引出分位数，VaR可引出。
* **引理二（Osband）**：可引出的泛函水平集是凸的。
* **定理**：δ₁与0.95δ₀ + 0.05δ₂的预期亏损都为一，等权混合为1.25，所以预期亏损不可引出。
* **Fissler–Ziegel**：(VaR, ES)可联合引出（FZ0）；固定真实VaR时，FZ0对e的期望在真实ES处最小。
* **检验**：
  * 水平集；
  * t₄样本上FZ0网格的最小值恰在真实值；
  * 1928–2020年按FZ0排名，GJR过滤法最好，DM t为6.7到11.1；
  * 检验力：Kupiec 5.9%，Z2 32%。
* **开放问题**：
  * 短样本下有检验力的预期亏损检验；
  * 系统性风险度量的可引出性；
  * 与银行真实损失一致的评分。

## 交易台问题与解答

1. √10 × 1000万 = 3160万美元，假设独立同分布正态；美国市场实际比值为3.4，七十年代为4.2。
2. VaR不满足次可加性（两只债券）；预期亏损是一致的。
3. 数例外（Kupiec）、检验独立性（Christoffersen）、红绿灯；要看几十年。
4. 极值理论：对超阈值部分拟合广义帕累托，先过滤波动率；美国的尾部指数约为五。
5. 尾部相依：高斯Copula为零；银行与保险一起崩盘的比例为0.67，高斯为0.40。
6. 预期亏损单独不能回测；和VaR一起可以（FZ0）；Z2使用VaR的例外。

## 习题与解答

1. σ = 1%：VaR₉₉ = 2.33%，ES₉₉ = 2.67%；VaR₉₇.₅ = 1.96%，ES₉₇.₅ = 2.34%。
2. 因子为√11.98 = 3.46，而非3.16。
3. 每只VaR₉₅为0；同时持有时为100（任一违约概率5.91%）。
4. LR = 7.73，p = 0.005，黄灯（乘数3.75）。
5. π₁₁ = 0.40，π₀₁ ≈ 0.006：例外之后再出现例外的可能性是65倍，模型忽视了波动率。
6. VaR = 6.37%，ES = 8.46%。
7. λ = 0.253。
8. 距离为8个标准差，方向沿−Σw。
9. 最坏VaR ≤ 三个ES之和 = 57；重排算法给出46。
10. 5 × √6 = 1220万美元。
11. **（资格考试）可引出性**：
    * 弹球损失的导数为F(q) − τ；
    * Osband引理；
    * 预期亏损的反例；
    * Rockafellar–Uryasev表示。
12. **（资格考试）预期亏损检验的基础**：
    * 正确预测下E[Z₂] = 0；
    * ES低估时E[Z₂] > 0；
    * 固定真实VaR，FZ0对e的导数在e = E[R | R ≤ v]处为零。

## 数据与复现

* **Kenneth French数据库**：截至2020年底的日因子与四十九个行业，冻结子集与清单核对；不使用留出期。
* **模拟**：随机种子固定在compute.py中。
* **不登记策略**：计数器仍为23,559。
* **引用而非计算**：摩根大通首席投资办公室事件、巴塞尔与FRTB规则、2020年3月的清算所保证金，均按报道表述。
