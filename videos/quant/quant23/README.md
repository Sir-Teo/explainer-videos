# Quant, Built — Part 23: Risk and Return

The opening of Act IV covers portfolio choice, equilibrium pricing, consumption, intermediaries, demand and speculative resale. Sixteen scenes include an opening, thirteen chapters, a research chapter and an outro. The English narration estimate is about 60 minutes; final media duration is measured separately. See the [syllabus](../SYLLABUS.md).

Original public-data calculations, fixed numerical illustrations and quoted published estimates have different scopes. Simplified reconstructions are not exact paper replications. Education in methods; not investment advice.

## Scientific and data scope

* **Portfolio choice:** the unrestricted frontier assumes positive-definite covariance and D>0. Tangency separation also requires a normalisable positive-premium portfolio, mean–variance preferences and common unconstrained financing. The correlation endpoints ±1 in the two-asset picture are singular algebraic illustrations, not separately established arbitrage-free equilibria; inverse-covariance formulas use the stated positive-definite case. The full saved empirical frontier is visible. Actual telecom, shops and other weights are −28.8%, +44.0% and −55.7%. The original 1990–2007 fit is rebalanced monthly to fixed weights during 2008–2020, with shorts and zero costs; it does not hold fixed share counts.
* **CAPM:** portfolio grouping reduces idiosyncratic beta noise but does not eliminate common errors or time variation. Low beta is not a total-safety ranking. The mechanical 5.2% BAB illustration uses whole-sample betas, including future information; it is retrospective, not implementable or published BAB performance. Its naive t-statistic is not robust certification. Stock-index tests jointly test the model and market proxy.
* **SDF:** E[Rᵉ] = −cov(m,Rᵉ)/E[m]. A linear factor projection may change sign. Only a positive factor, correctly normalised with a known one-period gross cash return (conditionally when needed), defines a probability density. Option prices constrain traded payoffs; limited quotes do not identify every state.
* **HJ:** bars show monthly Sharpe ratios multiplied by √12. Divide by √12 for the monthly SDF coefficient-of-variation bound; they are not annual SDF bounds. The named [`review_audits.py`](review_audits.py) display audit reproduces the original gross-return bound at all original grid points, then evaluates the same saved sample moments on a declared 301-point grid [0.5,1.02]. It introduces no fitting, strategy trial or performance series. The 1948–2024 sample has 77 observations. The full bound reaches 20.515. All seven original CRRA points fail the necessary bound at their own means: the earlier claim that gamma 20 reaches it is false. At gamma 20, sd(m)=0.275 versus bound 12.460; at 50, 0.618 versus 18.688. The bill is nominal cash deflated ex post and has inflation risk. This L2 bound omits positivity; satisfying it would not establish a positive factor pricing all assets.
* **APT/PCA:** the 2A−B example is exact arbitrage only if residual risks cancel and cash/shorting assumptions hold. B adjusts to 13% only if A and cash are fixed. PCA components, betas and mean returns use the same 1970–2025 sample and assets: descriptive in-sample fit, not structural or out-of-sample pricing evidence. PC signs are arbitrary; the reported market correlation is absolute. The full cumulative first-ten share (80.69%) is retained.
* **Consumption/GMM:** current-vintage broad real per-capita PCE includes durables; Q4 is a quarter average timestamped October, not a December instant. Annual consumption and returns run through 2024. The first-order premium formula and log-rate benchmark need their payoff/distribution assumptions. The saved unconstrained two-step fit uses 76 observations, lag-0 covariance, beta 1.507 and gamma 27.28 (SE 21.69), J=5.415, p=0.247. Weak identification, no stored optimiser-success diagnostic and no HAC check limit interpretation; non-rejection is not validation.
* **Premium/disasters:** the 8.781% arithmetic real excess mean differs from the opening's compound-growth gap. Implied gamma uses the saved ddof-1 covariance 0.001297214 (not an exact product of differently normalised standard deviations), giving 67.69 in a mixed simple/log approximation. Mapping its wealth gamble to consumption needs extra assumptions. Fixed-loss disaster curves retain their full tails: the 40% loss curve reaches 112.86% at gamma 10. They are not a full Barro calibration; Jensen comparisons require the same law and mean with a convex loss term. Historical premia alone do not prove a risk explanation or guarantee recovery after a crash.
* **Shiller:** the variance argument needs constant discounting, no-bubble transversality and suitable stationary finite second moments. The empirical picture fits a full-history trend and uses a last-ten-price terminal convention; it is illustrative rather than a formal rationality rejection. January prices are monthly averages, with a rolling dividend proxy. **The saved legacy CS routine skips the next return:** its 136 anchors (1871–2006) use years **2–16**, ending 2022. We preserve the protected algorithm and do not introduce a corrected market regression. This is not a correctly aligned next-15-year decomposition. Bars normalise b_r=0.50185 and −b_d=0.09157 by their sum; about 84.6%/15.4%, not all yield variance. The dividend contribution is positive. Finite-horizon terminal terms and linearisation error remain; no next-return guarantee or identified news split follows.
* **Intermediaries:** all seven saved capital-risk point estimates are positive; four approximate Shanken t-values exceed 1.96. Commodities are positive too (t≈1.57). Class windows differ, betas use each full sample, and iid-style statistics are not HAC, joint, causal or exact-paper certification. Book dealer leverage and parents' market capital are different measures. The balance-sheet example sells 45 and repays debt, assuming no additional impact/costs; raising equity is another choice. Scarcity alone does not prove mispricing.
* **Demand:** the logit derivative holds wealth, shares outstanding, characteristics and other prices fixed. Its beta-zero=1 example is not a literal self-financing index-fund elasticity. Aggregate equilibrium needs wealth, supply and cross-price feedback. The cited Gabaix–Koijen multiplier near five is a local allocation-shock hypothesis subject to identification; every share purchase has a seller. Buybacks also change corporate cash/financing.
* **Behaviour:** prospect decision weights are not perceived probabilities. A static loss kink alone does not generally derive a dynamic disposition policy. Odean's estimates and the Palm stub value are quoted, not recomputed; the latter is not an unconditional riskless arbitrage given borrow/recall, costs and distribution timing. Shleifer–Vishny inputs form a toy, not a calibrated history of LTCM or crisis bases.
* **Run-ups:** the implemented relative threshold is (1+R_industry)/(1+R_market)−1>1, not R_industry−R_market>1. The source has 2,868 missing industry cells, filled with zero by the original code. It keeps the first trigger, at least 25 months apart within each industry; cross-industry events overlap. All 60 saved events have complete 24-month follow-up (latest July 2022), though the algorithm permits censoring. 53.3% crash and +19.9% mean subsequent return are conditional descriptive summaries. No matched unconditional baseline, trading costs or executable short performance is computed. Chart colours use hindsight; full multiples up to 6.228 are shown. Cited predictor and hedge-fund studies do not prove universal pre-peak exit.
* **Bubbles/research:** general pricing is B_t=E_t[m B_next]; physical expected-growth examples need risk-neutral/constant-required-return assumptions. No-bubble transversality excludes bubbles. Nonnegative/positive-kernel and finite-payoff restrictions are conditional; fixed supply alone is insufficient. Harrison–Kreps uses next-period dividends. Strict premiums need changing strict optimists and reachability, not ties. The sweep holds a chosen average transition matrix fixed, not a measured true law or average valuation. Unlimited risk-neutral shorting can prevent equilibrium. Common beliefs give P=V_Q; only type 2 gives state-zero price exactly 16/11≈1.455. A worked answer is shown. Turnover and warrant evidence do not uniquely identify the mechanism.

## Chapters and practice

Opening; 1 Markowitz; 2 Tobin and estimation; 3 CAPM; 4 SDF and HJ; 5 APT/ICAPM; 6 consumption/GMM; 7 premium puzzle; 8 Shiller; 9 intermediaries; 10 demand; 11 behaviour; 12 bubbles; 13 House research; researcher: disagreement; outro. Twelve problems appear on three numbered pages (1–6, 7–10, 11–12). The lab displays the unchanged House functions `tangency`, `hj_excess` and `shleifer_vishny`.

## Desk questions, with solutions

1. Equal 20% volatilities, correlation 0.5: weights 1/2 each; variance 0.03, volatility 17.32%.
2. A flat beta line can reflect financing constraints, proxy/model failure and estimation issues. The saved mechanical BAB result is retrospective, using whole-sample betas; it does not establish an implementable strategy.
3. Raw same-period Sharpe 2 gives σ(m)/E[m]≥2 in that period. If 2 annualises monthly returns, the monthly bound is 2/√12≈0.577. Verify frequency, selection and tail exposure.
4. Saved simple premium / sample log covariance gives 0.087813/0.001297214≈67.69, an approximation. Smooth consumption makes the covariance small; it does not directly measure wealth preferences.
5. A low yield permits different long-horizon returns, dividend growth and terminal yields, plus approximation error. It does not fix the next return; the saved shifted diagnostic is not a correctly timed decomposition.
6. Under the cited local allocation-shock assumptions, 1%/0.2≈5%. Sellers accommodate the shift; wealth, supply and news can alter this relation.

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


## Problems, with solutions

1. **The frontier.** Minimise ½ w'Σw subject to w'μ = m and w'1 = 1. The first-order condition Σw = λμ + γ1 gives
   w = λΣ⁻¹μ + γΣ⁻¹1. The constraints become λB + γA = m and λA + γC = 1, so λ = (Cm − A)/D and γ = (B − Am)/D. Then
   σ² = w'Σw = λm + γ = (Cm² − 2Am + B)/D.
2. **Two assets.** w₁ = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂) = (0.01 − 0.006)/(0.04 + 0.01 − 0.012) = 0.105, w₂ = 0.895.
   The variance is 0.105² × 0.04 + 0.895² × 0.01 + 2 × 0.105 × 0.895 × 0.006 = 0.00958, a volatility of 9.79%: a
   little below the safer asset's 10%.
3. **Tangency and HJ.** The tangency weights are proportional to z = Σ⁻¹(μ − r_f1); its excess mean is
   z'(μ − r_f1)/z'1 and its variance z'Σz/(z'1)² = z'(μ − r_f1)/(z'1)², so its Sharpe ratio squared is
   (μ − r_f1)'Σ⁻¹(μ − r_f1). This is the **square** of the necessary same-period HJ coefficient-of-variation lower bound. The bound itself is its square root. A positive-definite covariance and a normalisable positive-premium tangency are assumed; positivity of the pricing projection is not imposed.
4. **How many years?** The standard error of a mean is σ/√T = 18%/√30 = 3.3% a year. Halving it needs four times as
   much data: 120 years. A premium of about 6% is barely two standard errors from zero after thirty years.
5. **The CAPM.** The tangency condition is Σw_M = κ(μ − r_f1) for some κ > 0; the i-th row says cov(R_i, R_M) =
   κ(E[R_i] − r_f). For the market itself, var(R_M) = κ(E[R_M] − r_f). Dividing, E[R_i] − r_f =
   β_i(E[R_M] − r_f) with β_i = cov(R_i, R_M)/var(R_M).
6. **The CAPM's discount factor.** For an excess return, 0 = E[mR^e] = E[m]E[R^e] + cov(m, R^e). With m = a − bR_M,
   cov(m, R^e) = −b cov(R_M, R^e), so E[R^e] = (b/E[m]) cov(R^e, R_M), which is the CAPM when b/E[m] =
   (E[R_M] − r_f)/var(R_M). Using gross market return R_M and known gross cash R_f consistently, cash pricing gives E[m] = 1/R_f, b = (E[R_M] − R_f)/(R_f var(R_M)) and a = 1/R_f + b E[R_M]. This linear pricing projection can be negative; CAPM pricing alone does not certify an equivalent probability density.
7. **The riskless rate.** With m = e^{−δ}(C₁/C₀)^{−γ} and ln growth ~ N(g, σ²): 1/R_f = E[m] = e^{−δ − γg + γ²σ²/2},
   so r_f = δ + γg − γ²σ²/2. With δ = 1%, g = σ = 2% and γ = 10: r_f = 0.01 + 0.20 − 0.02 = 19%, The 19% is a **log** rate in the iid Gaussian log-growth benchmark, not a simple rate. The saved bill proxy is nominal cash deflated ex post and has inflation risk; its mean cannot be called a known real risk-free rate.
8. **A disaster.** Marginal utility scales as C^{−γ}, so a 29% fall raises it by 0.71^{−4} ≈ 3.9 times. An asset that
   loses heavily in that state is paid for the loss weighted by nearly four, and with γ larger the weight explodes:
   a small probability times a large weight is a large premium.
9. **The Campbell–Shiller constant.** R_{t+1} = (P_{t+1} + D_{t+1})/P_t; in logs r = pd_{t+1} − pd_t + Δd + ln(1 +
   e^{−pd_{t+1}}). A first-order expansion of the last term around the mean gives κ + ρ pd_{t+1} with
   ρ = 1/(1 + e^{dp̄}) (dp̄ the mean log dividend yield). With dp̄ = −3.25, ρ = 1/(1 + e^{−3.25}) = 0.963.
10. **Shleifer–Vishny.** p₁ = V − S₁ + F₁ = 1 − 0.3 + 0.2 = 0.90. p₂ = (V − S₂ + F₁(1 − a))/(1 − aF₁/p₁) =
    (1 − 0.4 − 0.1)/(1 − 0.3/0.9) = 0.5/0.667 = 0.75 (against 0.80 with a=0, no return-sensitive fund reduction). F₂ = F₁ + aF₁(p₂/p₁ − 1) =
    0.2 + 0.3 × (−0.167) = 0.15: the fund loses a quarter of its capital just as the price is furthest from value.
11. **(qual) The fixed point.** The map TP = β max_i Q_i(d + P) is monotone and satisfies |TP − TP′|_∞ ≤ β|P − P′|_∞
   (each Q_i is a stochastic matrix and max is 1-Lipschitz), so it is a contraction with a unique fixed point. Since
   P = TP ≥ βQ_i(d + P) and V_i = βQ_i(d + V_i), P − V_i ≥ βQ_i(P − V_i); iterating, P − V_i ≥ (βQ_i)ⁿ(P − V_i) → 0.
   For the example, guess the holders (type 1 in state 0, type 2 in state 1) and solve the linear system
   P₀ = ¾[½(0 + P₀) + ½(1 + P₁)], P₁ = ¾[¼(0 + P₀) + ¾(1 + P₁)]: P₀ = 24/13, P₁ = 27/13; check that the guessed type is
   indeed the higher bidder in each state.
12. **(qual) When the premium vanishes.** If type j has the highest Q_j(d + P) in every state, P = βQ_j(d + P), the
   same equation as V_j, whose solution is unique: P = V_j = max_i V_i. Strict premiums require changing **strict** optimists and suitable reachability, rather than an arbitrary change of tie-break. The positive transition matrices in the fixed example satisfy the relevant conditions.


## Data, reproducibility and QA scope

The 13 original computations restored through their normal recorded hash checks: 13 successes, zero blocked. No force/refresh, protected algorithm edit, new market trial, registry mutation or sealed experiment opening. The cumulative counter remains **317 through Part 23**, global **23,562**. All 98 protected files retain baseline hashes.

Public French bytes through December 2025 are read, including by `_ff()` before tests restrict their dates. This is distinct from sealed experiment payloads; do not claim no public 2021–2025 observations were read. Original fitted-window illustrations stop at December 2020; public descriptive series can extend later. FRED provides broad PCE, CPI and Nasdaq; Shiller and HKM provide their published data. Consumption actually ends in 2024. Published Palm, disaster, elasticity, prospect and account estimates remain cited estimates.

The display audit is a separately named fixed numerical illustration (`hj_display_audit`), with its original-cache hash, sample moments and grid saved. It leaves legacy caches untouched. Three existing pure numerical regressions pass; they do not validate empirical timing.

```bash
python -m videos.quant.quant23.compute  # normal original checks; never add --force/refresh
python -m videos.quant.quant23.review_audits
EXPLAINER_TTS=silent python tools/qa_scene.py quant23 SDF
```

Current final render evidence is reported separately in [the QA ledger](../../../docs/qa/quantitative-finance-polish.md). Source preflight, sampled generated speech and silent-preview timing are distinct from continuous production narration listening and pronunciation certification, which remain a separate scope.

# 第23部分：风险与收益

第四幕从组合选择、均衡定价和消费模型，走向中介资本、需求、行为和转售泡沫。十六个场景，英文讲稿估计约六十分钟；实际媒体时长另行测量。公开数据原始计算、固定数值示例和引用论文数字应分别解释，简化重构不是精确论文复现。

## 科学口径与限制

* 前沿假定协方差正定和D>0；Tobin分离还需共同输入、均值方差偏好和相同无限制融资条件。两资产图的相关系数±1端点是奇异的代数示例，并未单独建立无套利均衡；逆协方差公式使用正定条件。原拟合切点在2008–2020年月度再平衡到固定权重，允许卖空、忽略成本，不是固定股数。BAB使用全样本未来贝塔，属于回顾示例；贝塔低不等于总风险安全。
* 超额收益为−cov(m,Rᵉ)/E[m]，分母不可省略。线性定价投影可为负，不能自动当作正贴现因子或概率密度。风险中性变换需正性和已知一期现金总收益，必要时使用条件期望。
* HJ柱是月度夏普乘√12，除以√12才是月度变异系数下界，不能解释为年度贴现因子波动。命名的固定显示审计保持原样本矩和公式，在预定301点网格完整显示曲线，不新增拟合、策略试验或业绩序列。1948–2024年77个观测中，七个CRRA点全部低于各自均值下的必要界；伽马二十并未碰到曲线。国库券事后平减仍有通胀风险，下界未施加正性。
* APT零因子贝塔并不保证零残差风险；严格套利还需卖空与融资条件。PCA因子、暴露、均值使用同一资产与全样本，只是样本内描述；主成分符号任意，市场相关用绝对值。
* 消费采用当前版本、含耐用品的广义PCE；第四季度是季度平均，时间戳十月，并非十二月瞬时值。实际年度数据到2024年。无约束两步GMM用76观测、零滞后协方差；贝塔1.507，伽马27.28，标准误21.69。弱识别、无优化器成功记录、无HAC稳健检验限制解释，J不拒绝不等于认证。
* 百分之8.781的实际算术超额收益与开场复合增长差不同；用保存的样本协方差0.001297214得近似伽马67.69。财富赌局到消费偏好需额外映射。固定损失灾难曲线完整保留百分之112.86的尾部，并非完整Barro校准；Jensen比较需同一分布与均值。持有穿越崩盘不保证恢复。
* Shiller图依赖常数贴现、横截、平稳和二阶矩假设，重构还采用全历史趋势与最后十个价格终值，不是理性定价的正式拒绝。**旧版CS索引跳过第一期收益**：1871–2006年136个锚点使用第二至第十六年结果，直到2022年。保留受保护算法，不新增修正市场回归，不能称为正确对齐的未来十五年分解。柱以两个协方差项之和归一化，收益约84.6%、股利约15.4%，后者为正，并非全部方差或识别出的消息。终端项与线性化误差仍在。
* 七个中介资本风险点估计全部为正，四个近似Shanken t值超过1.96；商品也为正。各类窗口不同、贝塔用各自全样本，不是HAC、联合或因果认证。交易商账面杠杆与母公司市场资本不是同一变量。资产负债表示例卖出45并偿债，假定无新增冲击或成本；增资也是选择。
* logit偏导固定财富、股数、特征与其他价格，贝塔零为一的例子不是字面的自融资指数基金。总量均衡需要财富、供给与交叉价格反馈。约五倍的引用乘数是有条件的局部配置冲击假说，每笔购买都有卖方，回购还改变现金和融资。
* 前景决策权重不是主观概率，静态损失拐点不一般性推出动态卖出政策。Odean和Palm数字为引用，负的隐含剩余价值不是无条件套利，仍有借券、召回、费用与时点风险。Shleifer–Vishny是玩具机制，不是危机历史校准。
* 大涨相对门槛是财富比率(1+R行业)/(1+R市场)−1>1。原代码将2868个行业缺失值填零，同一行业触发至少间隔25个月，跨行业可重叠。保存的60事件全部有完整24月随访，最新2022年7月，但算法允许截尾。53.3%崩盘和随后平均+19.9%仅是条件描述，无匹配无条件基准或可执行做空认证。颜色是事后标签，倍数尾部完整保留。
* 一般泡沫条件为B_t=E_t[mB下一期]，屏幕物理增长例子需风险中性或常数要求收益率假设。固定供给本身不排除泡沫。HK使用下一期股利，严格溢价需严格乐观者变化和可达性；平均转移矩阵是选定参考链，不是真实概率估计或平均估值。无限制风险中性卖空甚至可导致无均衡。共同信念时P=V_Q；只有第二类时状态零恰为16/11≈1.455，答案为相等。换手和权证证据不唯一识别机制。

## 六个交易台解答

1. 各半，方差0.03，波动率17.32%。
2. 平贝塔线可能涉及融资约束、代理与估计问题；全样本贝塔BAB不是可执行策略复现。
3. 原始同频率夏普二给同频率HJ变异系数下界二；若二是月度夏普年化值，月度下界2/√12≈0.577。
4. 0.087813/0.001297214≈67.69是混合简单和对数收益的近似，不是直接财富偏好估计。
5. 低股利收益率允许多种长期收益、股利、终端项与近似误差组合，不决定下一期收益；所存诊断有移位。
6. 在引用的局部配置冲击假设下，1%/0.2≈5%；所有购买有卖方，还需考虑财富、供给和信息。

## 习题与解答

1. **前沿。** 在w'μ = m、w'1 = 1的约束下最小化½ w'Σw。一阶条件Σw = λμ + γ1给出w = λΣ⁻¹μ + γΣ⁻¹1。约束变为λB + γA = m和λA + γC = 1，所以λ = (Cm − A)/D，γ = (B − Am)/D。于是σ² = w'Σw = λm + γ = (Cm² − 2Am + B)/D。
2. **两个资产。** w₁ = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂) = (0.01 − 0.006)/(0.04 + 0.01 − 0.012) = 0.105，w₂ = 0.895。方差为0.105² × 0.04 + 0.895² × 0.01 + 2 × 0.105 × 0.895 × 0.006 = 0.00958，波动率9.79%：略低于较安全资产的10%。
3. **切点组合与HJ界。** 切点组合的权重与z = Σ⁻¹(μ − r_f1)成正比；它的超额均值为z'(μ − r_f1)/z'1，方差为z'Σz/(z'1)² = z'(μ − r_f1)/(z'1)²，所以夏普比率的平方为(μ − r_f1)'Σ⁻¹(μ − r_f1)。该表达式是同频率HJ变异系数必要下界的**平方**，下界本身需要开平方。假定协方差正定、正溢价切点可以归一化，并未施加定价投影的正性。
4. **需要多少年？** 均值的标准误为σ/√T = 18%/√30 = 每年3.3%。减半需要四倍的数据：120年。约6%的溢价在三十年后只比零大两个标准误左右。
5. **CAPM。** 切点条件为Σw_M = κ(μ − r_f1)，κ > 0；第i行给出cov(R_i, R_M) = κ(E[R_i] − r_f)。对市场本身，var(R_M) = κ(E[R_M] − r_f)。相除得E[R_i] − r_f = β_i(E[R_M] − r_f)，β_i = cov(R_i, R_M)/var(R_M)。
6. **CAPM的贴现因子。** 对超额收益，0 = E[mR^e] = E[m]E[R^e] + cov(m, R^e)。取m = a − bR_M，cov(m, R^e) = −b cov(R_M, R^e)，所以E[R^e] = (b/E[m]) cov(R^e, R_M)；当b/E[m] = (E[R_M] − r_f)/var(R_M)时这就是CAPM。为现金定价确定E[m] = 1/R_f，所以b = (E[R_M] − R_f)/(R_f var(R_M))，a = 1/R_f + b E[R_M]。这些系数统一使用市场和现金总收益；线性定价投影可能为负，不能自动当作概率密度。
7. **无风险利率。** 取m = e^{−δ}(C₁/C₀)^{−γ}，对数增长 ~ N(g, σ²)：1/R_f = E[m] = e^{−δ − γg + γ²σ²/2}，所以r_f = δ + γg − γ²σ²/2。δ = 1%、g = σ = 2%、γ = 10时：r_f = 0.01 + 0.20 − 0.02 = 19%，这里百分之十九是独立同分布正态对数增长基准中的**对数**利率。所存国库券代理用事后通胀平减，仍有通胀风险，均值不是已知实际无风险利率。
8. **一次灾难。** 边际效用与C^{−γ}成比例，所以下跌29%使它上升0.71^{−4} ≈ 3.9倍。在这种状态下大幅亏损的资产，其损失以接近四的权重计价；γ更大时权重会爆炸：很小的概率乘以很大的权重，就是很大的溢价。
9. **Campbell–Shiller常数。** R_{t+1} = (P_{t+1} + D_{t+1})/P_t；取对数r = pd_{t+1} − pd_t + Δd + ln(1 + e^{−pd_{t+1}})。在均值附近对最后一项做一阶展开得到κ + ρ pd_{t+1}，其中ρ = 1/(1 + e^{dp̄})（dp̄为平均对数股息率）。dp̄ = −3.25时，ρ = 1/(1 + e^{−3.25}) = 0.963。
10. **Shleifer–Vishny。** p₁ = V − S₁ + F₁ = 1 − 0.3 + 0.2 = 0.90。p₂ = (V − S₂ + F₁(1 − a))/(1 − aF₁/p₁) = (1 − 0.4 − 0.1)/(1 − 0.3/0.9) = 0.5/0.667 = 0.75（a为零、无收益敏感资金下降时为0.80）。F₂ = F₁ + aF₁(p₂/p₁ − 1) = 0.2 + 0.3 × (−0.167) = 0.15：恰在价格离价值最远时，基金损失了四分之一的资本。
11. **（资格考试）不动点。** 映射TP = β max_i Q_i(d + P)单调且满足|TP − TP′|_∞ ≤ β|P − P′|_∞，是压缩映射，有唯一不动点。由P = TP ≥ βQ_i(d + P)与V_i = βQ_i(d + V_i)得P − V_i ≥ βQ_i(P − V_i)，迭代得P − V_i ≥ 0。对例子，猜测持有者（状态0为第1类，状态1为第2类）并解线性方程组P₀ = ¾[½P₀ + ½(1 + P₁)]、P₁ = ¾[¼P₀ + ¾(1 + P₁)]：P₀ = 24/13，P₁ = 27/13；再验证所猜的类型在每个状态下确实出价更高。
12. **（资格考试）溢价何时消失。** 若第j类在每个状态下都有最高的Q_j(d + P)，则P = βQ_j(d + P)，与V_j的方程相同，而其解唯一：P = V_j = max_i V_i。严格溢价需要严格乐观者改变和适当可达性，仅改变平手时的持有人不够。本例的正转移矩阵满足相关条件。


## 数据与审阅

十三项原始计算均通过正常哈希检查恢复，没有force/refresh、受保护算法改动、新市场试验、注册表修改或封存实验读取。累计次数保持本部分317、全局23562，98个受保护文件不变。公开French字节确实读到2025年，包括先读取再限制日期的辅助函数；它们与封存实验载荷不同，不能说2021–2025年公开数据从未读取。原拟合窗口示例止于2020年12月，描述历史可以更晚。三个原有纯数值回归测试通过，不认证经验时间对齐。命名显示审计保留原缓存哈希和样本矩，不替代旧缓存。连续生产配音试听与发音认证是独立的待完成范围，不能用静音预览、信号或文字时序检查替代。

## Current visual review

Visual pass complete on `quantitative-finance`: 32 bilingual endpoint sheets, 16 English forty-frame motion sheets and 29 focused native frames actually inspected on source `27549ce7b136a78142e5678a3da34cb64fcb103b`. The chaptered silent timing preview runs 70:54 with 16 chapters and English subtitles. Eleven CPU speech reports cover 82 sampled lines; the actual narrated opening runs 157.067 seconds. These signal/visual checks do not certify pronunciation or continuous production listening, which remain pending. [Artifact-bound evidence](../../../docs/qa/quant23-polish-evidence.json).

## 当前视觉审阅

本轮已实际检查32张双语旁白节点画面表、16张英文四十帧动画表及29张重点原尺寸画面。分章静音时序预览为70:54，含16章与英文字幕。十一份CPU语音报告覆盖82个抽样句段，并核验实际配音开场。信号和画面检查不替代发音或完整生产成片连续听审，后者仍是独立待办。
