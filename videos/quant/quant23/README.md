# Quant, Built — Part 23: Risk and Return

Part 23 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act IV, Return Premia (23–29). Act III asked what things must cost;
this part asks what they pay, and why. It builds the theory of expected returns from Markowitz to the inelastic markets
hypothesis, tests each piece on a century of public data, and opens the House's research desk. It covers:

* mean–variance: the two-asset frontier, the frontier by Lagrange, the global minimum-variance and tangency portfolios,
  Tobin's separation, and estimation error (the tangency's Sharpe ratio halves out of sample; 1/N wins);
* the CAPM derived; the security market line on sixty-two years of beta-sorted deciles, flat; noisy betas, portfolios
  and shrinkage; betting against beta; Roll's critique;
* the stochastic discount factor: p = E[mx], its special cases, its identity with the risk-neutral measure, and the
  Hansen–Jagannathan bound on the market, industries and 25 size and value portfolios;
* the APT (an arbitrage worked by hand, principal components of 49 industries) and Merton's ICAPM;
* consumption: Lucas, the Euler equation, Hansen and Singleton's GMM on US data since 1948; the equity premium and
  risk-free rate puzzles; habit, long-run risk and disasters;
* Shiller's excess volatility on Shiller's own data since 1871, and the Campbell–Shiller decomposition;
* intermediary asset pricing (He–Krishnamurthy; Adrian–Etula–Muir; He–Kelly–Manela on seven asset classes);
* demand systems and inelastic markets (Koijen–Yogo; Gabaix–Koijen);
* behavioural finance and the limits of arbitrage: 3Com and Palm, Shleifer–Vishny, prospect theory, the disposition
  effect; bubbles (Greenwood–Shleifer–You on 49 industries; the Nasdaq; rational bubbles).

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`premia`](../../../explainer/quant/house/premia.py) module). Data: Kenneth French's data library (the market, bills,
industries, beta deciles, size and value portfolios), Robert Shiller's online data, FRED (real consumption per person,
CPI, the Nasdaq Composite) and He, Kelly and Manela's published factors and test assets.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 50 minutes)

* **What risk is worth** (2.4 min). A dollar in US stocks in July 1926 → $17,488 at the end of 2025, against $24.9 in
  bills (10.3% against 3.3% a year); every theory as E[R] − R_f = β λ, and all of them as p = E[mx]; the history
  strip (1952–2021); the plan; the research desk opens.
* **1. Markowitz: the frontier** (2.5). Two assets of 20% volatility as the correlation runs from −1 to 1; the frontier
  by Lagrange (two-fund separation); the global minimum-variance portfolio, which needs no means; ten US industries,
  1990–2025 (GMV volatility 11%, below every industry); the optimiser's extreme weights.
* **2. Cash, the tangency, and estimation error** (2.4). The capital market line and Tobin's separation; the tangency
  on the industries (Sharpe 0.85 against the market's 0.58); fitted on 1990–2007 and held to 2025: 0.89 in sample,
  0.45 out, against 1/N 0.64, GMV 0.67 and the market 0.66; shrinkage, constraints (Jagannathan–Ma) and
  Black–Litterman.
* **3. The CAPM and the flat line** (3.7). The CAPM derived from market clearing; the SML and Black–Jensen–Scholes;
  noisy betas (a standard error of 0.26 on five years of monthly data), errors in variables, portfolios, Blume's and
  Vasicek's shrinkage; beta deciles 1963–2025 (betas 0.60–1.60; fitted slope 3.3% against a premium of 7.1%,
  intercept 4.5%); betting against beta (5.6% a year, Sharpe 0.30, t = 2.35; Frazzini–Pedersen); Roll's critique.
* **4. One price equation: the discount factor** (3.9). p = E[mx], 1 = E[mR], E[R^e] = −cov(m, R^e)/E[m]; the CAPM,
  consumption, factor and intermediary models as choices of m; m and the risk-neutral measure, dQ/dP = m R_f; the
  Hansen–Jagannathan bound derived; the market 0.46, ten industries 0.63, 25 size–value portfolios 1.39 (0.86 out of
  sample); the gross-return cup and the CRRA discount factor climbing into it only at very high γ.
* **5. Many factors: APT and ICAPM** (3.0). Ross's argument; an arbitrage by hand (A: β 1, 8%; B: β 2, 12%; 2A − B is
  riskless at 4% against cash at 3%); principal components of 49 industries (the first 56% of variance, correlation
  0.96 with the market; five components 73%); pricing by components (R² ≈ 0 with one, 0.22 with ten); Merton's ICAPM.
* **6. Consumption and GMM** (2.7). Lucas's tree and the Euler equation; lognormal predictions for the premium and the
  riskless rate; US real consumption per person, 1948–2025 (volatility 1.9%, the market's 17%, correlation 0.39);
  Hansen–Singleton GMM with instruments (γ = 27, standard error 22; β = 1.51; J = 5.4, p = 0.25); the risk-free rate
  puzzle (Weil).
* **7. The equity premium puzzle** (3.4). The premium 8.8% a year; γ ≈ 68 to explain it, and what that means for a
  gamble; Mehra and Prescott (1985); habit (Campbell–Cochrane), long-run risk (Bansal–Yaron) and disasters (Rietz;
  Barro: p = 1.7%, b = 0.29; γ = 4 gives 2.1%, 5.4% at b = 0.40); what is agreed and what is not.
* **8. Prices move too much** (2.9). The ex post rational price and the variance bound; Shiller's data, 1871–2022,
  detrended (σ(p) = 0.44 against σ(p*) = 0.29); the Campbell–Shiller identity derived; the split on fifteen-year
  horizons (b_r = 0.50, b_d = −0.09, ρ = 0.962: of what is explained, about 85% is returns); two readings; the Nobel of
  2013.
* **9. Intermediaries price assets** (3.4). He–Krishnamurthy's discount factor; a dealer's balance sheet worked (a 5%
  fall halves equity; restoring a 10% ratio means selling $45 of $95; loss and margin spirals); He–Kelly–Manela's
  capital ratio, 1970–2018 (2.2% in early 2009); two-pass tests on seven asset classes (capital-risk price positive in
  six; stocks R² 0.53 against the CAPM's 0.08); Adrian–Etula–Muir's leverage factor and the tension between them.
* **10. Demand systems and inelastic markets** (3.4). Koijen and Yogo's logit demand from 13F holdings; each investor's
  elasticity 1 − β₀(1 − w) (an index fund ≈ 0.01, fixed dollars 1, a value investor ≈ 5; a 70/30 market ≈ 0.3); the
  picture; Gabaix and Koijen's aggregate elasticity of about 0.2 and multiplier of 5; passive investing, buybacks and
  the debate.
* **11. Behaviour and the limits of arbitrage** (4.3). Barberis and Thaler's two pillars; 3Com and Palm (2 March 2000;
  the rest of 3Com at about −$22 billion; Lamont–Thaler); Shleifer–Vishny's performance-based arbitrage derived and
  charted (0.90 after the first shock; 0.80 without withdrawals; 0.60 at a = 3); prospect theory's two curves
  (Tversky–Kahneman 1992: losses 2.25 times gains; a 1% chance felt as 5.5%; Barberis–Huang); the disposition effect
  (Odean 1998: PGR 0.148 against PLR 0.098); noise-trader risk and extrapolation.
* **12. Bubbles** (3.7). Fama's and Shiller's definitions; the Nasdaq (5,048.62 on 10 March 2000, 1,114.11 on 9 October
  2002, −78%); Greenwood–Shleifer–You's run-ups on 49 industries, 1926–2025 (60 run-ups, 53% crashed, average return
  over the next two years +20%); when they happened; rational bubbles (Blanchard–Watson: 16.7% a year at r = 5% and a
  10% annual chance of bursting; why theory rules most out); riding the bubble (Brunnermeier–Nagel).
* **13. Rule 23: the research desk** (4.4). The desk's first sheet; **lab**: `tangency`, `hj_excess`,
  `shleifer_vishny`; risk, constraint or error: three reasons for a premium; the research pipeline (claim, reason,
  estimate, hold-out, stress, ledger); the `premia` module; Rule 23; the rule against the optimiser, a new anomaly,
  the arbitrage fund and the industry that doubled.
* **Recap, desk questions, problems** (3.6). Fourteen lines; six desk questions; ten problems, solutions below.

## Hands-on

* **Lab** (the House's own code on screen): `tangency`, `hj_excess`, `shleifer_vishny` (ch. 13).
* **Computed:** the industry frontier and its out-of-sample record against 1/N; the SML on beta deciles and betting
  against beta; Hansen–Jagannathan bounds for three sets of assets and the CRRA discount factor; principal components
  of 49 industries; GMM on the Euler equations; the disaster premium; Shiller's p* and the Campbell–Shiller split;
  two-pass tests of the capital factor; Shleifer–Vishny prices; Greenwood–Shleifer–You run-ups.
* **Live constructions:** the two-asset curve bending as the correlation falls; the capital market line swinging up to
  the tangency; the HJ cup with the consumption SDF climbing toward it; an arbitrage portfolio landing on the beta
  axis; elastic and inelastic demand shifting; prospect theory's kink and weighting curve; a research pipeline.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Cochrane, *Asset Pricing* | 1 (p = E[mx]), 4–6 (the SDF, mean–variance, factor models), 9 (CAPM, APT, ICAPM), 10–11 (GMM), 20–21 (the equity premium, predictability, volatility) | ch. 1–9 |
| Campbell, *Financial Decisions and Markets* | 2–3 (mean–variance), 4 (the SDF), 5 (the CAPM and its tests), 6 (consumption, the puzzle, habit, long-run risk, disasters), 9 (behavioural finance) | ch. 1–8, 11 |
| Back, *Asset Pricing and Portfolio Choice Theory* | 5 (mean–variance), 6 (factor pricing), 7 (consumption) | ch. 1–6 |
| Duffie, *Dynamic Asset Pricing Theory* | 1–2 (state prices, the SDF), 10 (Lucas) | ch. 4, 6 |
| Shleifer, *Inefficient Markets* | 1–4 (noise traders, limits of arbitrage, the 3Com case's kind) | ch. 11–12 |

## Papers, chapter by chapter

* Hook: Kenneth French's data library; the history strip's papers below.
* ch. 1–2: Markowitz (1952); Tobin (1958); Merton (1972) on the frontier's algebra; Black and Litterman (1992);
  Jagannathan and Ma (2003); Ledoit and Wolf (2004); DeMiguel, Garlappi and Uppal (2009).
* ch. 3: Sharpe (1964); Lintner (1965); Black (1972); Black, Jensen and Scholes (1972); Fama and MacBeth (1973); Blume
  (1971, 1975); Vasicek (1973); Roll (1977); Frazzini and Pedersen (2014).
* ch. 4: Harrison and Kreps (1979); Hansen and Jagannathan (1991); Cochrane, *Asset Pricing*, ch. 1 and 5.
* ch. 5: Ross (1976); Merton (1973); Connor and Korajczyk (1986).
* ch. 6–7: Lucas (1978); Breeden (1979); Hansen (1982); Hansen and Singleton (1982); Mehra and Prescott (1985); Rietz
  (1988); Weil (1989); Epstein and Zin (1989); Campbell and Cochrane (1999); Bansal and Yaron (2004); Barro (2006).
* ch. 8: Shiller (1981); LeRoy and Porter (1981); Campbell and Shiller (1988); Cochrane (2011).
* ch. 9: Brunnermeier and Pedersen (2009); He and Krishnamurthy (2013); Adrian, Etula and Muir (2014); He, Kelly and
  Manela (2017).
* ch. 10: Koijen and Yogo (2019); Gabaix and Koijen (2021).
* ch. 11: De Long, Shleifer, Summers and Waldmann (1990); Tversky and Kahneman (1992); Shleifer and Vishny (1997); Odean
  (1998); Barberis and Thaler (2003); Lamont and Thaler (2003); Barberis and Huang (2008); Greenwood and Shleifer
  (2014).
* ch. 12: Blanchard and Watson (1982); Diba and Grossman (1988); Abreu and Brunnermeier (2003); Brunnermeier and Nagel
  (2004); Greenwood, Shleifer and You (2019).

## Build it

```bash
python -m videos.quant.quant23.compute                        # every item (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant23 SDF      # one chapter, silent, with a contact sheet
python tools/make.py quant23 --cpu-voice -q m                 # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Two assets, 20% volatility each, correlation 0.5: minimum-variance weights and volatility?** Half each, by
   symmetry. The variance is 0.25 × 0.04 + 0.25 × 0.04 + 2 × 0.25 × 0.5 × 0.04 = 0.03, so the volatility is 17.3%:
   with a correlation of a half, diversification takes off less than three points (ch. 1).
2. **Why is the security market line flatter than the CAPM says?** One reading (Black, 1972; Frazzini and Pedersen,
   2014): investors who cannot or will not borrow buy high-beta stocks to get more risk, bidding them up and lowering
   their returns. Betting against beta, low-beta levered up long and high-beta levered down short, earned 5.6% a year
   on the deciles (ch. 3).
3. **An asset has a Sharpe ratio of 2. What does that say about any model that prices it?** By Hansen–Jagannathan,
   σ(m)/E(m) ≥ 2: a discount factor with a volatility of 200% a year, far beyond any consumption model. Suspect the
   data first: selection among many tries, stale or smoothed prices, or a tail risk that has not yet happened (ch. 4).
4. **Why does the equity premium need a risk aversion near 70?** Because the covariance of stocks with consumption is
   tiny: consumption's volatility is 1.9%, the market's 17%, and their correlation 0.39, so the covariance is about
   0.0013, and 8.8% / 0.0013 ≈ 68. The same γ then predicts a riskless rate far above the one observed (ch. 6–7).
5. **The dividend yield is at a record low. What must happen next?** By the Campbell–Shiller identity, low future
   returns, or high future dividend growth, or a yield that stays low indefinitely. In the data the movements of the
   yield have forecast returns, not dividends (ch. 8).
6. **The market's demand elasticity is 0.2. A fund moves 1% of the market from bonds to stocks. Effect?** Prices rise by
   about 1% / 0.2 = 5%, until the other holders, the few whose demand responds to price, sell enough to absorb the
   flow. With elasticity that low there are few such sellers, so the price must move a long way (ch. 10).

## Problems, with solutions

1. **The frontier.** Minimise ½ w'Σw subject to w'μ = m and w'1 = 1. The first-order condition Σw = λμ + γ1 gives
   w = λΣ⁻¹μ + γΣ⁻¹1. The constraints become λB + γA = m and λA + γC = 1, so λ = (Cm − A)/D and γ = (B − Am)/D. Then
   σ² = w'Σw = λm + γ = (Cm² − 2Am + B)/D.
2. **Two assets.** w₁ = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂) = (0.01 − 0.006)/(0.04 + 0.01 − 0.012) = 0.105, w₂ = 0.895.
   The variance is 0.105² × 0.04 + 0.895² × 0.01 + 2 × 0.105 × 0.895 × 0.006 = 0.00958, a volatility of 9.79%: a
   little below the safer asset's 10%.
3. **Tangency and HJ.** The tangency weights are proportional to z = Σ⁻¹(μ − r_f1); its excess mean is
   z'(μ − r_f1)/z'1 and its variance z'Σz/(z'1)² = z'(μ − r_f1)/(z'1)², so its Sharpe ratio squared is
   (μ − r_f1)'Σ⁻¹(μ − r_f1). The Hansen–Jagannathan bound for these excess returns is the same expression, since the
   minimum-variance discount factor is linear in them with the same weights.
4. **How many years?** The standard error of a mean is σ/√T = 18%/√30 = 3.3% a year. Halving it needs four times as
   much data: 120 years. A premium of about 6% is barely two standard errors from zero after thirty years.
5. **The CAPM.** The tangency condition is Σw_M = κ(μ − r_f1) for some κ > 0; the i-th row says cov(R_i, R_M) =
   κ(E[R_i] − r_f). For the market itself, var(R_M) = κ(E[R_M] − r_f). Dividing, E[R_i] − r_f =
   β_i(E[R_M] − r_f) with β_i = cov(R_i, R_M)/var(R_M).
6. **The CAPM's discount factor.** For an excess return, 0 = E[mR^e] = E[m]E[R^e] + cov(m, R^e). With m = a − bR_M,
   cov(m, R^e) = −b cov(R_M, R^e), so E[R^e] = (b/E[m]) cov(R^e, R_M), which is the CAPM when b/E[m] =
   (E[R_M] − r_f)/var(R_M). Pricing cash fixes E[m] = 1/R_f, so b = (E[R_M] − R_f)/(R_f var(R_M)) and
   a = 1/R_f + b E[R_M].
7. **The riskless rate.** With m = e^{−δ}(C₁/C₀)^{−γ} and ln growth ~ N(g, σ²): 1/R_f = E[m] = e^{−δ − γg + γ²σ²/2},
   so r_f = δ + γg − γ²σ²/2. With δ = 1%, g = σ = 2% and γ = 10: r_f = 0.01 + 0.20 − 0.02 = 19%, against about 1% in
   the data: the risk-free rate puzzle.
8. **A disaster.** Marginal utility scales as C^{−γ}, so a 29% fall raises it by 0.71^{−4} ≈ 3.9 times. An asset that
   loses heavily in that state is paid for the loss weighted by nearly four, and with γ larger the weight explodes:
   a small probability times a large weight is a large premium.
9. **The Campbell–Shiller constant.** R_{t+1} = (P_{t+1} + D_{t+1})/P_t; in logs r = pd_{t+1} − pd_t + Δd + ln(1 +
   e^{−pd_{t+1}}). A first-order expansion of the last term around the mean gives κ + ρ pd_{t+1} with
   ρ = 1/(1 + e^{dp̄}) (dp̄ the mean log dividend yield). With dp̄ = −3.25, ρ = 1/(1 + e^{−3.25}) = 0.963.
10. **Shleifer–Vishny.** p₁ = V − S₁ + F₁ = 1 − 0.3 + 0.2 = 0.90. p₂ = (V − S₂ + F₁(1 − a))/(1 − aF₁/p₁) =
    (1 − 0.4 − 0.1)/(1 − 0.3/0.9) = 0.5/0.667 = 0.75 (against 0.80 without withdrawals). F₂ = F₁ + aF₁(p₂/p₁ − 1) =
    0.2 + 0.3 × (−0.167) = 0.15: the fund loses a quarter of its capital just as the price is furthest from value.

## Data and reproducibility

* Kenneth French's data library: the market, the one-month bill, 10 and 49 industries, beta-sorted deciles, 25 size
  and value portfolios, monthly; through December 2025.
* Robert Shiller's online data (ie_data): the S&P composite, dividends and CPI, monthly from 1871.
* FRED: A794RX0Q048SBEA (real personal consumption expenditures per capita), CPIAUCSL, NASDAQCOM. Frozen through 2025
  and checksummed.
* He, Kelly and Manela: the capital ratio and factor, and their test portfolios, as the authors publish them.
* Published figures quoted, not computed: the 3Com and Palm prices (Lamont and Thaler); Barro's disaster calibration;
  Gabaix and Koijen's elasticity; Tversky and Kahneman's parameters; Odean's PGR and PLR.
* Illustrative inputs, labelled on screen: the two-asset examples, the APT arbitrage, the beta-noise example, the
  dealer's balance sheet, the logit investors, the Shleifer–Vishny parameters, the rational bubble.
* No hold-out is opened in this part; the trial counter stays at 315.

---

# 量化金融，从零搭建 — 第23部分：风险与收益

本部分是第四幕“收益溢价”（第23–29部分）的第一部分。第三幕问的是东西必须值多少钱；本部分问的是它们支付多少、为什么。它从Markowitz一直讲到无弹性市场假说，用一个世纪的公开数据检验每一块理论，并开设House的研究交易台。本部分讲：

* 均值–方差：两资产前沿、用拉格朗日乘数求前沿、全局最小方差组合与切点组合、Tobin分离定理，以及估计误差（切点组合的夏普比率在样本外减半；1/N获胜）；
* 推导CAPM；用六十二年按贝塔排序的十分位组合画出证券市场线——它是平的；含噪声的贝塔、组合与收缩；押注低贝塔；Roll的批评；
* 随机贴现因子：p = E[mx]、它的特例、它与风险中性测度的等价，以及市场、行业和25个规模–价值组合上的Hansen–Jagannathan界；
* APT（手算一次套利；49个行业的主成分）与Merton的ICAPM；
* 消费：Lucas、欧拉方程、1948年以来美国数据上的Hansen–Singleton GMM；股权溢价之谜与无风险利率之谜；习惯、长期风险与灾难；
* 用Shiller自己1871年以来的数据检验过度波动，以及Campbell–Shiller分解；
* 中介资产定价（He–Krishnamurthy；Adrian–Etula–Muir；He–Kelly–Manela的七个资产类别）；
* 需求系统与无弹性市场（Koijen–Yogo；Gabaix–Koijen）；
* 行为金融与套利的限制：3Com与Palm、Shleifer–Vishny、前景理论、处置效应；泡沫（Greenwood–Shleifer–You在49个行业上的研究；纳斯达克；理性泡沫）。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约50分钟）

* **风险值多少。** 1926年7月投入美国股市的一美元，到2025年底变成17,488美元，投入国库券只有24.9美元（每年10.3%对3.3%）；每个理论都写成E[R] − R_f = βλ，而它们全都是p = E[mx]；历史条（1952–2021）；本部分安排；研究交易台开张。
* **1. Markowitz：前沿。** 两个波动率20%的资产，相关系数从−1变到1；用拉格朗日乘数求前沿（两基金分离）；不需要任何均值的全局最小方差组合；1990–2025年的十个美国行业（最小方差组合波动率11%，低于每个行业）；优化器给出的极端权重。
* **2. 现金、切点组合与估计误差。** 资本市场线与Tobin分离定理；行业上的切点组合（夏普比率0.85，市场0.58）；用1990–2007年拟合并持有到2025年：样本内0.89，样本外0.45，对比1/N的0.64、最小方差组合的0.67和市场的0.66；收缩、约束（Jagannathan–Ma）与Black–Litterman。
* **3. CAPM与那条平的线。** 由市场出清推导CAPM；证券市场线与Black–Jensen–Scholes；含噪声的贝塔（五年月度数据的标准误为0.26）、变量误差、组合、Blume与Vasicek的收缩；1963–2025年的贝塔十分位组合（贝塔0.60–1.60；拟合斜率3.3%，而溢价为7.1%，截距4.5%）；押注低贝塔（每年5.6%，夏普比率0.30，t = 2.35；Frazzini–Pedersen）；Roll的批评。
* **4. 一个定价方程：贴现因子。** p = E[mx]，1 = E[mR]，E[R^e] = −cov(m, R^e)/E[m]；CAPM、消费模型、因子模型和中介模型都是对m的选择；m与风险中性测度，dQ/dP = m R_f；推导Hansen–Jagannathan界；市场0.46、十个行业0.63、25个规模–价值组合1.39（样本外0.86）；总收益的“杯形”下界，CRRA贴现因子只有在γ很高时才爬进去。
* **5. 多个因子：APT与ICAPM。** Ross的论证；手算一次套利（A：β为1，8%；B：β为2，12%；2A − B无风险地赚4%，而现金是3%）；49个行业的主成分（第一个解释56%的方差，与市场的相关系数0.96；前五个73%）；用主成分定价（一个时R²约为0，十个时0.22）；Merton的ICAPM。
* **6. 消费与GMM。** Lucas的果树与欧拉方程；对数正态下对溢价和无风险利率的预测；1948–2025年美国人均实际消费（波动率1.9%，市场17%，相关系数0.39）；带工具变量的Hansen–Singleton GMM（γ = 27，标准误22；β = 1.51；J = 5.4，p = 0.25）；无风险利率之谜（Weil）。
* **7. 股权溢价之谜。** 溢价每年8.8%；要解释它γ约为68，以及这对一次赌博意味着什么；Mehra与Prescott（1985）；习惯（Campbell–Cochrane）、长期风险（Bansal–Yaron）与灾难（Rietz；Barro：p = 1.7%，b = 0.29；γ = 4时为2.1%，b = 0.40时为5.4%）；哪些已有共识，哪些没有。
* **8. 价格波动太大。** 事后理性价格与方差界；Shiller的数据，1871–2022，去趋势后（σ(p) = 0.44，σ(p*) = 0.29）；推导Campbell–Shiller恒等式；十五年期限上的分解（b_r = 0.50，b_d = −0.09，ρ = 0.962：被解释部分中约85%来自收益）；两种解读；2013年的诺贝尔奖。
* **9. 中介机构为资产定价。** He–Krishnamurthy的贴现因子；算一个交易商的资产负债表（资产下跌5%使权益减半；恢复10%的资本比率要卖掉95美元中的45美元；损失与保证金螺旋）；He–Kelly–Manela的资本比率，1970–2018（2009年初为2.2%）；七个资产类别上的两步回归检验（资本风险价格在六个类别为正；股票的R²为0.53，CAPM为0.08）；Adrian–Etula–Muir的杠杆因子以及二者之间的矛盾。
* **10. 需求系统与无弹性市场。** Koijen与Yogo基于13F持仓的logit需求；每个投资者的弹性为1 − β₀(1 − w)（指数基金约0.01，固定金额为1，价值投资者约5；70/30的市场约0.3）；示意图；Gabaix与Koijen估计的总弹性约0.2、乘数为5；被动投资、回购与争论。
* **11. 行为与套利的限制。** Barberis与Thaler的两大支柱；3Com与Palm（2000年3月2日；3Com的其余业务估值约−220亿美元；Lamont–Thaler）；推导并画出Shleifer–Vishny的基于业绩的套利（第一次冲击后0.90；无赎回时0.80；a = 3时0.60）；前景理论的两条曲线（Tversky–Kahneman 1992：损失的权重是收益的2.25倍；1%的机会感觉像5.5%；Barberis–Huang）；处置效应（Odean 1998：PGR为0.148，PLR为0.098）；噪声交易者风险与外推。
* **12. 泡沫。** Fama与Shiller的定义；纳斯达克（2000年3月10日5,048.62，2002年10月9日1,114.11，−78%）；Greenwood–Shleifer–You在49个行业上的暴涨，1926–2025（60次暴涨，53%崩盘，随后两年的平均收益+20%）；它们发生在何时；理性泡沫（Blanchard–Watson：r = 5%、每年10%的破裂概率时，每年上涨16.7%；为什么理论排除了大多数泡沫）；骑在泡沫上（Brunnermeier–Nagel）。
* **13. 第23条规则：研究交易台。** 交易台的第一张表；**实验**：`tangency`、`hj_excess`、`shleifer_vishny`；风险、约束或错误：溢价的三种理由；研究流程（主张、理由、估计、样本外、压力、台账）；`premia`模块；第23条规则；用优化器、一个新异象、套利基金和翻倍的行业检验这条规则。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十道习题，解答见下文。

## 交易台问题与解答

1. **两个资产，波动率都是20%，相关系数0.5：最小方差权重和波动率？** 由对称性各一半。方差为0.25 × 0.04 + 0.25 × 0.04 + 2 × 0.25 × 0.5 × 0.04 = 0.03，所以波动率为17.3%：相关系数为一半时，分散化只降低不到三个百分点（第1章）。
2. **为什么证券市场线比CAPM说的平？** 一种解读（Black，1972；Frazzini与Pedersen，2014）：不能或不愿借钱的投资者买高贝塔股票来获得更多风险，把它们的价格抬高、收益压低。押注低贝塔——把低贝塔加杠杆做多、高贝塔去杠杆做空——在十分位组合上每年赚5.6%（第3章）。
3. **一个资产的夏普比率是2。这对任何能为它定价的模型意味着什么？** 由Hansen–Jagannathan界，σ(m)/E(m) ≥ 2：贴现因子每年的波动率达200%，远超任何消费模型。先怀疑数据：在多次尝试中挑选、陈旧或平滑的价格，或尚未发生的尾部风险（第4章）。
4. **为什么股权溢价需要接近70的风险厌恶？** 因为股票与消费的协方差极小：消费的波动率为1.9%，市场为17%，相关系数0.39，协方差约0.0013，8.8% / 0.0013 ≈ 68。同样的γ又预测出远高于实际的无风险利率（第6–7章）。
5. **股息率处于历史最低。接下来必须发生什么？** 由Campbell–Shiller恒等式：要么未来收益低，要么未来股息增长高，要么股息率无限期地保持低位。数据中股息率的变动预测的是收益，而不是股息（第8章）。
6. **市场的需求弹性是0.2。一只基金把市场的1%从债券转到股票。效果？** 价格上涨约1% / 0.2 = 5%，直到其他持有者——少数需求对价格有反应的人——卖出足够多来吸收这笔资金。弹性这么低时这样的卖家很少，所以价格必须走很远（第10章）。

## 习题与解答

1. **前沿。** 在w'μ = m、w'1 = 1的约束下最小化½ w'Σw。一阶条件Σw = λμ + γ1给出w = λΣ⁻¹μ + γΣ⁻¹1。约束变为λB + γA = m和λA + γC = 1，所以λ = (Cm − A)/D，γ = (B − Am)/D。于是σ² = w'Σw = λm + γ = (Cm² − 2Am + B)/D。
2. **两个资产。** w₁ = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂) = (0.01 − 0.006)/(0.04 + 0.01 − 0.012) = 0.105，w₂ = 0.895。方差为0.105² × 0.04 + 0.895² × 0.01 + 2 × 0.105 × 0.895 × 0.006 = 0.00958，波动率9.79%：略低于较安全资产的10%。
3. **切点组合与HJ界。** 切点组合的权重与z = Σ⁻¹(μ − r_f1)成正比；它的超额均值为z'(μ − r_f1)/z'1，方差为z'Σz/(z'1)² = z'(μ − r_f1)/(z'1)²，所以夏普比率的平方为(μ − r_f1)'Σ⁻¹(μ − r_f1)。这些超额收益的Hansen–Jagannathan界是同一个表达式，因为最小方差贴现因子对它们是线性的，权重相同。
4. **需要多少年？** 均值的标准误为σ/√T = 18%/√30 = 每年3.3%。减半需要四倍的数据：120年。约6%的溢价在三十年后只比零大两个标准误左右。
5. **CAPM。** 切点条件为Σw_M = κ(μ − r_f1)，κ > 0；第i行给出cov(R_i, R_M) = κ(E[R_i] − r_f)。对市场本身，var(R_M) = κ(E[R_M] − r_f)。相除得E[R_i] − r_f = β_i(E[R_M] − r_f)，β_i = cov(R_i, R_M)/var(R_M)。
6. **CAPM的贴现因子。** 对超额收益，0 = E[mR^e] = E[m]E[R^e] + cov(m, R^e)。取m = a − bR_M，cov(m, R^e) = −b cov(R_M, R^e)，所以E[R^e] = (b/E[m]) cov(R^e, R_M)；当b/E[m] = (E[R_M] − r_f)/var(R_M)时这就是CAPM。为现金定价确定E[m] = 1/R_f，所以b = (E[R_M] − R_f)/(R_f var(R_M))，a = 1/R_f + b E[R_M]。
7. **无风险利率。** 取m = e^{−δ}(C₁/C₀)^{−γ}，对数增长 ~ N(g, σ²)：1/R_f = E[m] = e^{−δ − γg + γ²σ²/2}，所以r_f = δ + γg − γ²σ²/2。δ = 1%、g = σ = 2%、γ = 10时：r_f = 0.01 + 0.20 − 0.02 = 19%，而数据中约为1%：无风险利率之谜。
8. **一次灾难。** 边际效用与C^{−γ}成比例，所以下跌29%使它上升0.71^{−4} ≈ 3.9倍。在这种状态下大幅亏损的资产，其损失以接近四的权重计价；γ更大时权重会爆炸：很小的概率乘以很大的权重，就是很大的溢价。
9. **Campbell–Shiller常数。** R_{t+1} = (P_{t+1} + D_{t+1})/P_t；取对数r = pd_{t+1} − pd_t + Δd + ln(1 + e^{−pd_{t+1}})。在均值附近对最后一项做一阶展开得到κ + ρ pd_{t+1}，其中ρ = 1/(1 + e^{dp̄})（dp̄为平均对数股息率）。dp̄ = −3.25时，ρ = 1/(1 + e^{−3.25}) = 0.963。
10. **Shleifer–Vishny。** p₁ = V − S₁ + F₁ = 1 − 0.3 + 0.2 = 0.90。p₂ = (V − S₂ + F₁(1 − a))/(1 − aF₁/p₁) = (1 − 0.4 − 0.1)/(1 − 0.3/0.9) = 0.5/0.667 = 0.75（无赎回时为0.80）。F₂ = F₁ + aF₁(p₂/p₁ − 1) = 0.2 + 0.3 × (−0.167) = 0.15：恰在价格离价值最远时，基金损失了四分之一的资本。

## 数据与复现

* Kenneth French数据库：市场、一个月国库券、10个和49个行业、按贝塔排序的十分位组合、25个规模–价值组合，月度，至2025年12月。
* Robert Shiller的在线数据（ie_data）：标普综合指数、股息与CPI，1871年起的月度数据。
* FRED：A794RX0Q048SBEA（人均实际个人消费支出）、CPIAUCSL、NASDAQCOM。冻结到2025年并校验哈希。
* He、Kelly与Manela：资本比率与因子，以及作者公布的检验组合。
* 引用而非计算的公开数字：3Com与Palm的价格（Lamont与Thaler）；Barro的灾难校准；Gabaix与Koijen的弹性；Tversky与Kahneman的参数；Odean的PGR与PLR。
* 屏幕上标注为示意的输入：两资产的例子、APT套利、贝塔噪声的例子、交易商的资产负债表、logit投资者、Shleifer–Vishny的参数、理性泡沫。
* 本部分不打开任何样本外数据；试验计数器保持在315。
