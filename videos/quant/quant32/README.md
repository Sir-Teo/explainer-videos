# Quant, Built · Part 32: Systematic Macro and Alternative Premia

Trend, volatility targeting, risk budgeting, carry, put writing and calendar rules,
with explicit assumptions and worked exercises. English source estimate: 62.7 minutes.
Actual bilingual construction, sampled speech and final visual review are complete. Full continuous production listening remains separately pending.

## Reproduction scope

Two unchanged ordinary calculations reproduced: AQR's published styles and Cboe
PUT against Kenneth French's market. Seven other originals failed frozen
adjusted-price checksum checks. Their historical strategy results are not used.
Affected lessons use explicitly chosen mathematics in [illustrations.py](illustrations.py),
without a substitute historical backtest. The research chapter evaluates exact
analytic reference laws, without a new simulation.

Nine distinct originals were each invoked once. A runner error rechecked the same
rejected source in five other originals. The accurate count is **five repeated
failed-source checks, zero function reruns**. Original logs and the corrective audit
are preserved. No refresh, additional market trial, sealed strategy payload access,
registry mutation or financial-algorithm change occurred. All 98 protected files
retain their recorded bytes. Existing public trial counts are 23,543 through Part 32
and 23,562 globally; these are metadata, not new performance results.

The scene loader rejects seven unavailable originals and envelope-prefixed names
before delegation. Only styles and shortvol remain as scene data loads. Missing
or invalid cached inputs are a stop condition; do not force, refresh or retry them.

## Chapters

| Chapter | Result and scope |
|---|---|
| Hook | Chosen persistent, reversing and final-jump paths; premium stories as hypotheses. |
| 1. Trend | Lagged timing, summed excess returns, sizing, six designs, breadth and chosen fees. |
| 2. Smile | P=(S²−Q)/2 for the reset linear rule. Path-dependent Q is neither fixed option premium nor wealth. Chosen turnover and blend covariance. |
| 3. Volatility targeting | Forecast error, caps, EWMA timing, inverse SD versus inverse variance, leverage and funding. |
| 4. Risk parity | Two-asset special case; three-group Euler counterexample; old-position risk under correlation change. |
| 5. Styles | Published AQR portfolios, reconstructed history, log wealth, changing coverage and ex-post crisis selection. |
| 6. Carry | Foreign-deposit cross product, covered interest parity, forward settlement units, bond approximation and quoted negative WTI futures. |
| 7. Insurance | PUT construction, total versus excess returns, drawdown convention, legacy beta proxy, dated windows and XIV's different exposure. |
| 8. Calendar | Overnight product identity, linear cost budget, event clocks, merger risk and multiple tests. |
| 9. Evaluation | Protocol, public counts and chosen covariance-stress rebalancing. No held-out verdict. |
| 10. House | Exact source excerpts for lagged trend, risk budgeting and block identity. |
| Research | Stationary mean, Gaussian moments and exact law, weaker iid limit, aggregation and matched filter. |
| Recap | Six desk questions; six basic, four advanced and two qualifying exercises. |

Existing House source is displayed unchanged. A source excerpt does not establish
attainable performance. All chosen inputs are stipulated, not fitted. Actual
constructions, plotted ranges, bilingual captions, motion, sampled speech and the
narrated opening have been checked in the artifact-bound review below.

Cached-data build after review:

    source /workspace/environment/activate.sh
    python tools/lecture_length.py quant32 --floor 50
    python tools/zh_lines.py quant32 --verify
    EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/build.py quant32 --lang en
    EXPLAINER_TTS=kokoro EXPLAINER_VOICE=zf_001 python tools/build.py quant32 --lang zh

## Measurement conventions

AQR's style Sharpes are .53, .64, .55 and .68; its provider multi-style series is
1.45, not demonstrated to be an equal average of the four displayed series.
The 1,134 monthly observations end December 2020. SD uses the population divisor,
annual scaling sqrt(12). Paths are cumulative log wealth, with missing returns
filled by zero. Underlying start dates differ; currency carry begins February 1974.
Six worst equity years are selected ex post. Multi-style is slightly negative in 2008.

PUT has 167 months February 2007–December 2020: Sharpe .45 versus .62 for French's
market, annual SD 11.8% versus 16.2%, monthly excess-return skew −1.63 versus −.57.
Wealth compounds total returns. Drawdown starts at the first observed NAV, omitting
a possible fall from initial NAV one. The beta proxy .640 divides covariance by N−1
and variance by N; annual intercept proxy −1.07% is not exact OLS or causal alpha,
and has no supplied standard error. Event windows are **September–November 2008**
and **February–March 2020**, with PUT returns −27.6% and −19.8%; neither is a full year.

XIV's February 2018 termination involved daily inverse short-term VIX futures,
not PUT. The quoted −37.63 dollars is the May WTI futures settlement on 20 April
2020, not cash spot or a fund return.

## Textbook audit and papers

| Textbook | Core coverage and continuation |
|---|---|
| Pedersen, Efficiently Inefficient (2015) | Macro signals, carry, constraints and implementation: chapters 1, 3–7, House. Statistical arbitrage in Part 33; firm organisation in Part 34. |
| Ilmanen, Expected Returns (2011) | Value, momentum, carry, defensive, insurance and seasonality: chapters 5–8. Risk stories distinguished from identified causes. |
| Kakushadze–Serur, 151 Trading Strategies (2018) | Trend, carry, calendar and event definitions: chapters 1, 6, 8. No claim of exhaustive empirical replication. |
| Clenow, Following the Trend (2013) | Signals, sizing, horizons and implementation: chapters 1–4 and House; futures/basis mechanics also in Part 22. |

- Moskowitz–Ooi–Pedersen (2012), Time Series Momentum, JFE; Hurst–Ooi–Pedersen
  (2017), A Century of Evidence on Trend-Following Investing, JPM; Lempérière et al.
  (2014), Two Centuries of Trend Following, Journal of Investment Strategies:
  published evidence and reconstruction assumptions, not a fresh House backtest.
- Babu–Levine–Ooi–Pedersen–Stamelos (2020), Trends Everywhere, Journal of Investment
  Management: broader applications of trend signals motivate careful distinctions
  among markets, predictors and implementable instruments. Kelly–Moskowitz–Pruitt
  (2021), Understanding Momentum and Reversal, JFE: a framework for momentum and
  reversal across horizons; it does not make every fitted rule's profit an identity.
- Fung–Hsieh (2001), The Risk in Hedge Fund Strategies: Theory and Evidence from
  Trend Followers, RFS: lookback-option factors differ from the reset linear rule.
  Potters–Bouchaud (2005), Trend Followers Lose More Often Than They Gain, Wilmott:
  payoff-shape motivation. Daniel–Moskowitz (2016), Momentum Crashes, JFE:
  cross-sectional momentum evidence cannot be transferred to every trend rule.
- Moreira–Muir (2017), Volatility-Managed Portfolios, JF: inverse-variance management.
  Cederburg–O'Doherty–Wang–Yan (2020), On the Performance of Volatility-Managed
  Portfolios, JFE: real-time robustness. Harvey et al. (2018), The Impact of
  Volatility Targeting, JPM: heterogeneous asset effects.
- Asness–Frazzini–Pedersen (2012), Leverage Aversion and Risk Parity, FAJ:
  constraints hypothesis. Campbell–Sunderam–Viceira (2017), Inflation Bets or
  Deflation Hedges? The Changing Risks of Nominal Bonds, Critical Finance Review:
  changing bond exposure. Bridgewater, The All Weather Story: attributed firm history.
- Asness–Moskowitz–Pedersen (2013), Value and Momentum Everywhere, JF:
  cross-asset comovement and liquidity associations. Frazzini–Pedersen (2014),
  Betting Against Beta, JFE: defensive evidence and funding constraints.
- Koijen–Moskowitz–Pedersen–Vrugt (2018), Carry, JFE: asset-specific carry
  measurement. Brunnermeier–Nagel–Pedersen (2008), Carry Trades and Currency Crashes,
  NBER Macroeconomics Annual: downside exposure. Keynes (1930) and Hicks (1939):
  historical normal-backwardation theories, not modern causal estimates.
- Israelov–Nielsen (2015), Covered Calls Uncovered, FAJ: exposure decomposition
  for a different strategy. Ilmanen (2012), Do Financial Markets Reward Buying or
  Selling Insurance and Lottery Tickets?, FAJ: insurance and lottery preferences.
  Gârleanu–Pedersen–Poteshman (2009), Demand-Based Option Pricing, RFS:
  imperfect hedging and dealer capacity.
- Ariel (1987), A Monthly Effect in Stock Returns, JFE; Lakonishok–Smidt (1988),
  Are Seasonal Anomalies Real?, RFS; Ogden (1990), Turn-of-Month Evaluations of
  Liquid Profits and Stock Returns, JF: calendar evidence and flow hypotheses.
  Bouman–Jacobsen (2002), The Halloween Indicator, “Sell in May and Go Away”, AER:
  seasonality and selection concerns.
- Lucca–Moench (2015), The Pre-FOMC Announcement Drift, JF: pre-announcement
  windows differ from statement-day close-to-close returns. Lou–Polk–Skouras
  (2019), A Tug of War: Overnight Versus Intraday Expected Returns, JFE:
  distinct clocks and exposures.
- Mitchell–Pulvino (2001), Characteristics of Risk and Return in Risk Arbitrage, JF:
  merger completion risk. Bernard–Thomas (1989), Post-Earnings-Announcement Drift:
  Delayed Price Response or Risk Premium?: event-response hypotheses.
  Sullivan–Timmermann–White (2001), Dangers of Data Mining: The Case of Calendar
  Effects in Stock Returns, Journal of Econometrics: selection-aware inference.

## For the researcher

P=½(S²−Q) holds for every finite path of the specified reset linear rule.
For stationary finite-second-moment increments,
E[P]=C(n,2)μ²+Σ_(k=1)^(n−1)(n−k)γ_k. Drift is not silently dropped.

For iid N(0,σ²), P/σ² has distribution ½[(n−1)U−V], with independent
U~χ²_1, V~χ²_(n−1). Variance is σ⁴n(n−1)/2, skew is
2^(3/2)(n−2)/sqrt(n(n−1)), and win probability Pr(F_(1,n−1)>1).
These are exact analytic evaluations, not simulated or fitted results.

For iid zero-mean increments with finite nonzero variance, CLT and LLN give
P/(nσ²) ⇒ ½(Z²−1); continuity at zero gives win probability tending to
2Pr(Z>1)=.3173105. Weak convergence alone does not imply convergence of skewness.
Heavy tails, estimated filters, costs, clipping, overlap and missing-data clocks
need separate analysis.

Open questions: convexity after realistic constraints (Potters–Bouchaud; Fung–Hsieh);
stable lag dependence after costs and selection (Moskowitz–Ooi–Pedersen; Lempérière);
protection at a portfolio's actual crisis horizon (Hurst–Ooi–Pedersen).
Answers need specified filters, executable exposure and appropriate uncertainty.

## Twelve worked problems: six basic, four advanced, two qualifying

All numerical inputs are chosen.

1. **Basic: stock risk fraction.** Weights (.6,.4), SDs (.2,.1), correlation zero.
   Variance=(.6×.2)²+(.4×.1)²=.016. Stock Euler fraction=.0144/.016=**90%**.
   Euler SD fractions are also w_i(Σw)_i/σ²; they are not capital weights.

2. **Basic: inverse volatility.** Same SDs, correlation −.2. Normalising inverse
   SDs gives (1/3,2/3). Weighted standalone SDs both equal 1/15.
   Variance=2(1/15)²(1−.2)=.00711111; base SD=**8.43274%**.
   L=.1/.0843274=**1.185854**, below chosen cap 4; positions
   (.395285,.790569). Equal Euler fractions are a two-asset special case.

3. **Basic: four styles.** Equal-volatility, equal-Sharpe .6 and equal weights:
   SR=.6 sqrt(4/[1+3ρ̄]). At average correlation zero, **1.20**;
   at .3, 1.2/sqrt(1.9)=**.87057**. This does not reconstruct AQR multi-style.

4. **Basic: forecast error.** Target .1, forecast .1, cap 3 gives
   x=min(.1/.1,3)=**1**. True conditional SD .2 gives |x|.2=**20%**.
   Forecast-based exposure does not guarantee true risk.

5. **Basic: income and tail.** Fifty months at .01, then one at −.30:
   mean=(50×.01−.30)/51=**.00392157**, or .392157% monthly.
   Deviations are .31/51 fifty times and −50×.31/51 once; cube sum
   (.31/51)³(50−50³)<0, hence negative skew. Compound total return
   1.01^50×.70−1=**15.12423%**, a different quantity from the arithmetic mean.

6. **Basic: cost budget.** Additive annual gross budget .10, 504 equally charged
   trade legs: .10−504c=0 gives c=.000198413=**1.98413 bp per leg**.
   If the count denotes round trips, the unit changes. Actual compounding,
   variable notional and impact need different accounting.

7. **Advanced: independent drift.** Independent increments with mean μ and finite
   second moment give E[r_s r_t]=μ² for s<t. Counting C(n,2) pairs yields
   **E[P]=C(n,2)μ²**. Zero mean is an additional assumption. Under stationarity
   with dependence add Σ_k(n−k)γ_k. Costs and capital scaling are separate.

8. **Advanced: Gaussian aggregation.** At n=63, skew
   2^(3/2)61/sqrt(63×62)=**2.760633**.
   K=23 independent identical profits with finite third moment have total
   variance Kv and centred third moment Km_3, because centred cross terms vanish.
   Skew therefore divides by sqrt(K), giving **.575632**.
   Zero pair correlation alone does not eliminate mixed third moments.

9. **Advanced: detection horizon.** Given SE(SR)≈1/sqrt(T), true annual SR=.3:
   .3 sqrt(T)=2 implies **T=(2/.3)²=44.444 years**.
   This is a planning signal/SE ratio, not a guarantee of rejection or specified
   power. Dependence, nonnormality and selection alter uncertainty.

10. **Advanced: targeting counterexample.** Known σ is .1 or .2 with equal
    probability, μ=σ², r=μ+σε, independent standard-normal ε.
    E[r]=.025; Var(r)=Eσ²+Var(σ²)=.025+.000225=.025225;
    unconditional one-period SR=**.157407**.
    With x=.1/σ (1 or .5), mean=.1Eσ=.015 and
    variance=.01+Var(.1σ)=.010025, giving SR=**.149813**.
    Targeting can lower Sharpe even with perfect conditional forecasts.
    The conditional objective xμ−γx²σ²/2, γ>0, gives
    x*=μ/(γσ²)=**1/γ**, constant, whereas inverse-SD targeting varies.
    This fixed two-state example is not empirically calibrated.

11. **Qualifying: Gaussian quadratic form.** For iid standard normals, let
    Y=Σ_(s<t)z_s z_t. E[Y]=0. In Y², different edges leave at least one
    independent zero-mean vertex, so only identical edges survive. Each
    contributes one, giving E[Y²]=C(n,2).
    In Y³, Gaussian odd moments kill all graphs except three distinct edges
    forming a triangle. Each chosen triangle has six edge orders and contributes
    E[z_i²z_j²z_k²]=1. Thus E[Y³]=6C(n,3)=n(n−1)(n−2).
    Divide by C(n,2)^(3/2) to obtain the skewness.

    Y=z'Az, A=(11'−I)/2. Eigenvalues are (n−1)/2 along 1 and −1/2
    in its n−1 orthogonal directions. Gaussian orthogonal invariance gives
    Y~½[(n−1)χ²_1−χ²_(n−1)], independent terms, and
    Pr(Y>0)=Pr(F_(1,n−1)>1).
    Finally Y/n=½[((Σz)/sqrt(n))²−Σz²/n].
    CLT and LLN, followed by Slutsky, yield ½(Z²−1).
    Continuity at zero implies Pr(Y>0)→2Pr(Z>1)=.3173105.
    Positive skew does not imply a positive expected edge.

12. **Qualifying: matched filter.** Fixed deterministic weights give
    P_w=Σ_(s<t)w_(t−s)r_s r_t.
    Stationarity gives E[P_w]=Σ_k(n−k)w_k(γ_k+μ²), by pair counting.
    Under the separate iid zero-mean variance reference,
    Var_0(P_w)=σ⁴Σ_k(n−k)w_k² because different edges have zero covariance.

    Against a specified zero-mean alternative with autocovariances γ_k,
    write a_k=n−k. The mean/reference-SD ratio is
    [Σa_k w_kγ_k]/[σ² sqrt(Σa_k w_k²)].
    Weighted Cauchy–Schwarz bounds it by sqrt(Σa_kγ_k²)/σ²,
    attained at **w_k=cγ_k, c>0**. If all γ_k=0 every admissible
    filter has zero numerator. This optimises a reference-variance criterion;
    the full correlated alternative variance adds covariance terms.
    Costs, estimated weights and selection change the optimisation.

## 中文

本部分讲授趋势、波动率目标、风险预算、套息、卖出看跌期权与日历规则。
英文源稿估计62.7分钟；双语实际构建、抽样语音与最终画面审阅已完成，完整成片连续听审仍单独待办。

仅两个原始普通计算通过冻结数据校验：AQR风格与Cboe PUT/French市场。
其余七项因复权价格校验和改变而停止；本修订不使用其历史策略结果，
不构造替代回测。相关章节使用明确指定的数学输入，研究章计算解析分布，
没有新增模拟或市场试验。九个不同函数各调用一次，但运行器错误地又检查
同一失败来源五次。因此准确记录为**五次失败来源重复检查、零次函数重跑**。
日志和纠正说明保留。未刷新、访问封存策略载荷或修改登记表与算法；
98个受保护文件字节不变。

章节涵盖信息时点、逐路径恒等式、预测与杠杆上限、风险贡献、风格样本、
跨币种与期货单位、PUT与尾部、事件时钟、评估协议、原代码实验和研究证明。
教材对应和逐篇文献用途见上表。AQR路径为累计对数财富，缺失收益以零填充，
底层起点不同，多风格不能直接当作四条展示序列的等权平均。危机年份事后选择。
PUT财富使用总收益，风险摘要使用超额收益；回撤从首个观测净值开始。
贝塔代理的协方差分母N−1、方差分母N，不是精确OLS；截距代理不是因果阿尔法。
2008事件仅9至11月，2020事件仅2至3月。XIV的每日反向VIX期货不同于PUT；
负37.63美元为WTI期货结算价，不是现货或基金收益。

研究章区分逐路径代数、平稳均值与高斯分布三个层次。
Q随路径改变，不是固定期权费或去均值方差。独立同分布、零均值、
有限非零方差足以给出弱极限，但不保证三阶矩收敛。
约束后的凸性、扣成本后稳定相关性及不同期限危机保护仍需独立证据。

### 十二题完整解答：六基础、四进阶、两资格

1. **基础：股票风险。** 权重(.6,.4)、波动率(.2,.1)、相关零，
   方差(.6×.2)²+(.4×.1)²=.016。股票Euler份额
   .0144/.016=**90%**。标准差贡献占比同为w_i(Σw)_i/σ²，
   不等于资本权重，且依赖给定协方差。

2. **基础：逆波动率。** 相关−.2时，逆标准差归一化权重(1/3,2/3)，
   加权独立风险均1/15。方差2(1/15)²(1−.2)=.00711111，
   标准差**8.43274%**。目标10%需L=**1.185854**，低于上限4；
   仓位(.395285,.790569)。等Euler贡献是此两资产特例。

3. **基础：四风格。** 等波动、等夏普、等权时，
   SR=.6 sqrt(4/[1+3ρ̄])。平均相关零得**1.20**，
   .3得**.87057**。此矩关系不是AQR多风格构造的复现。

4. **基础：预测误差。** x=min(.1/.1,3)=**1**；
   真实条件标准差.2，组合条件标准差为**20%**。
   基于预测控制仓位并不保证真实风险等于目标。

5. **基础：收入与尾部。** 均值(50×.01−.30)/51
   =**.00392157**，即月均.392157%。五十个偏差.31/51，
   一个偏差−50×.31/51，立方和(.31/51)³(50−50³)<0，偏度负。
   复利总收益1.01^50×.70−1=**15.12423%**，不同于算术均值。

6. **基础：成本预算。** 可加年度毛收益预算.10，504条等额计费交易腿，
   .10−504c=0，故c=.000198413=**每腿1.98413基点**。
   若计数为往返，单位随之改变；真实复利、名义金额和冲击需另算。

7. **进阶：独立漂移。** 独立且二阶矩有限时，
   E[r_s r_t]=μ²。共C(n,2)对，故**E[P]=C(n,2)μ²**。
   零均值是额外条件，不能自动忽略漂移；平稳相关时再加
   Σ(n−k)γ_k。此式不包括成本和资本归一化。

8. **进阶：偏度合成。** n=63时偏度
   2^(3/2)61/sqrt(63×62)=**2.760633**。
   K=23个独立同分布、三阶矩有限的利润，中心化交叉项为零，
   总方差Kv、三阶中心矩Km_3，故偏度除sqrt(K)得**.575632**。
   两两不相关不足以消除混合三阶矩。

9. **进阶：识别期限。** 题设SE(SR)≈1/sqrt(T)，
   .3 sqrt(T)=2得**T=44.444年**。这是规划信号/标准误比值，
   不保证拒绝，也未指定检验功效；相关、非正态与筛选改变不确定性。

10. **进阶：目标反例。** 事先可知σ各半概率取.1、.2，
    μ=σ²，ε独立标准正态。原收益均值.025，
    方差Eσ²+Var(σ²)=.025225，无条件单期夏普**.157407**。
    x=.1/σ取1或.5时，均值.015，方差
    .01+Var(.1σ)=.010025，夏普**.149813**。
    完美风险预测也不保证提高夏普。条件目标
    xμ−γx²σ²/2的一阶条件给x*=μ/(γσ²)=**1/γ**，
    是常数，逆标准差目标仓位则变化。此模型无经验拟合。

11. **资格：高斯二次型。** Y=Σ_(s<t)z_s z_t，z独立标准正态。
    E[Y]=0。Y²中不同边留下至少一个一次出现的独立零均值顶点；
    同边自乘贡献1，共C(n,2)项，因此E[Y²]=C(n,2)。
    Y³中高斯奇数矩消去非三角图，选三顶点并排序三边有
    6C(n,3)项，每项E[z_i²z_j²z_k²]=1，
    所以E[Y³]=n(n−1)(n−2)。除方差3/2次方得偏度。

    写Y=z'Az，A=(11'−I)/2；全一方向特征值(n−1)/2，
    其余n−1方向为−1/2。正交变换保持标准高斯坐标独立，
    故Y分布为[(n−1)χ²_1−χ²_(n−1)]/2，两卡方独立，
    胜率Pr(F_(1,n−1)>1)。
    Y/n=½[((Σz)/sqrt(n))²−Σz²/n]，
    中心极限定理、大数律及Slutsky给极限(Z²−1)/2。
    极限在零点无原子，胜率趋于2Pr(Z>1)=.3173105。
    正偏度不意味着正期望收益。

12. **资格：匹配滤波器。** 固定确定性权重给
    P_w=Σ_(s<t)w_(t−s)r_s r_t，平稳模型逐滞后数配对得
    E[P_w]=Σ(n−k)w_k(γ_k+μ²)。
    另在独立零均值、方差σ²的参考模型下，
    不同边协方差零，故Var_0(P_w)=σ⁴Σ(n−k)w_k²。

    对指定零均值备择自协方差γ_k，令a_k=n−k，
    均值/参考标准差为[Σa_k w_kγ_k]/[σ²sqrt(Σa_k w_k²)]。
    加权Cauchy–Schwarz给上界sqrt(Σa_kγ_k²)/σ²，
    **w_k=cγ_k，c>0**时取等。若所有γ_k为零，
    每个可行滤波器分子都零。此为参考方差优化；
    相关备择的完整方差还有协方差项。成本、估计和筛选改变最优解。

## Current visual review

Scientific presentation revision, bilingual construction and actual rendered visual review are complete on `quantitative-finance`, source `eebbe2b4523a2fc6247c7bff2ea78a5a1ebf8432`, fingerprint `0afeae3ee802a466a2e679afddb9f38f6d13296b4388def41c9465ee9da86e9b`. All 26 bilingual endpoint sheets, 13 English forty-frame motion sheets and 20 focused native frames were actually inspected across all thirteen scenes. Every exact flagged interval has an artifact-bound decision. Earlier diagnostic and unsuccessful final attempts retain their own execution fingerprints and exact bytes; no approval transfers to the fresh final renders.

All 126 narration contexts translate at runtime, and raw narration agrees across bilingual endpoints, English motion and current construction captures. The 37 actual computed fields and 32 captured curve ranges pass. One existing pure numerical test passes. The 359 additive captions preserve all 34,295 prior strings, yielding 34,654. All 98 protected files remain unchanged.

Nine distinct audited ordinary originals were invoked: two succeeded and seven failed frozen-source validation. Five repeated checks of a rejected shared source across distinct functions are explicitly corrected in the preserved audit; no function was rerun. Failed empirical lessons use expressly stipulated mathematical examples, without a substitute historical strategy or new market trial. No refresh, registry mutation or sealed experiment access occurred.

The chaptered silent timing preview runs 74:49, with thirteen chapters and English subtitles. Eleven CPU speech reports cover 109 sampled lines; the actual narrated opening lasts 259.400 seconds. Full continuous production listening and pronunciation review remain separately pending. [Artifact-bound evidence](../../../docs/qa/quant32-polish-evidence.json).

## 当前视觉审阅

科学表述、双语构建及实际画面审阅已完成。实际检查全部 26 张双语旁白节点画面表、13 张英文四十帧动画表及 20 张重点原尺寸画面，覆盖十三个场景。每个标记区间均有绑定实际文件的审阅决定；此前诊断与未获批准的最终尝试保留原始字节及执行指纹，不转移批准。

全部 126 处旁白经运行时翻译与实际文本核对，37 个实际格式化字段及 32 处曲线范围检查通过。新增 359 条字幕保留此前全部 34,295 条，共 34,654 条；98 个受保护文件未改变。

九个不同常规原始计算各调用一次：两个成功，七个因冻结来源校验失败。不同函数曾对同一已拒绝来源重复检查五次，计数错误已明确更正并保留证据；没有重新调用原函数。失败的实证章节改用明确指定的数学例子，没有替代历史策略回测、新增市场试验、刷新数据、修改登记或访问封存实验。

分章静音预览为 74:49，含十三章及英文字幕。十一份 CPU 语音报告覆盖 109 个抽样句段，并检查实际配音开场。画面与信号检查不替代完整成片连续听审或发音认证，后两项仍单独待办。
