

# Quant, Built — Part 40: Measuring Risk

Thirteen scenes examine risk quantiles, integrated-tail expected shortfall, forecasting diagnostics, extreme values, dependence, stress, uncertainty, learned quantiles and historical Basel methodology. The risk dashboard is a proposed research design, not one reconciled live capital report or deployment approval. Current bilingual construction and artifact-bound visual review are complete; the evidence and remaining production-listening scope are recorded below.

## Evidence and data scope

Thirteen audited unchanged ordinary originals were each invoked once. Twelve succeeded: `var3`, `sqrt`, `coherent`, `backtest`, `evt`, `depend`, `stress`, `ra`, `learned`, `liq`, `research`, `options`. Their hashes are pinned in `common.py`. `extra` was blocked before the unchanged original checker because the initial public-key map omitted Binance's assembled daily-file key. This was an audit gap, not a demonstrated frozen-hash mismatch. The attempt and rejection remain recorded; no retry, audit-widening rerun, partial-output reuse or substitute historical fit follows. Its threshold sweep, cross-market tail fits, copula portfolio simulation, Euler table and worst-window ranking are omitted. Clearly chosen formulas/examples replace those sections without recreating failed empirical output.

The initial map listed 43 possible public keys, not every key actually reachable: the blocked assembled key exposed the missing 44th dependency. Possible keys do not claim every key was read. Ten inherited rejected keys plus this newly blocked key remain barred before original checking. French daily factors and 49 daily industries are frozen subsets through 2020-12-31. Industry comparisons use complete eligible rows. No strategy hold-out or strategy payload was opened, read or scored. Every `compute.py`, the financial algorithms and all 98 protected files remain unchanged. Existing registrations are 23,561 through Part 40 and 23,562 globally; none are new work from this pass.

Do not run the default all-item computation. Missing or changed pinned outputs fail before implicit computation. `extra` and sensitive prefixes are rejected before name-to-path conversion, counted loading or cache access. No force/refresh, new market trial, rejected-key retry or registry mutation is part of this review.

## Scientific conventions

For integrable positive-convention losses L, VaR is the generalized alpha quantile. Strict exceedance has probability at most 1-alpha; equality needs appropriate continuity. ES is `(1-alpha)^-1 integral_alpha^1 VaR_u du`. A conditional mean above the quantile agrees for continuous losses, but atoms need boundary mass splitting. The unchanged historical helper uses a NumPy interpolated quantile and mean of observations at/above that cutoff; it is not an exact integrated empirical ES for arbitrary atoms. The discrete bond/mixture examples explicitly split atoms.

Root-time scaling is exact for zero-mean iid Gaussian additive losses with fixed variance. For returns with daily mean mu and scale sigma, horizon loss VaR is `-h mu + sqrt(h) sigma z_alpha`. The approved historical exercise sums overlapping simple daily returns, not compounded buy-and-hold returns. Overlap affects sampling dependence. A gap from scaling does not identify clustering, autocorrelation or rebounds as its unique cause. A chosen +10%/-10% path sums to zero but compounds to -1%.

The options example shorts 1,000 straddles and hedges initial delta. Delta-gamma retains the quadratic spot term but omits theta; full Black–Scholes revaluation advances maturity by one day and keeps the hedge static. Their difference does not isolate gamma approximation error. The five-point implied-volatility stress is applied to every simulated path, not only the worst spot moves, and is not a fitted joint spot/volatility model.

Coherence and duality require a specified integrable domain; the ES dual uses probability densities between zero and `1/(1-alpha)` integrating to one. Elliptical VaR subadditivity requires jointly elliptical linear losses with a nonnegative confidence coefficient, not merely separately fitted elliptical marginals. Euler allocation additionally needs differentiability, with subgradients/boundary weights when absent. Convex dual representations require the relevant function-space lower-semicontinuity/Fatou assumptions. Normal ES at 97.5% has coefficient 2.3378, close to but not equal to the 99% VaR coefficient 2.3263; a universal cross-confidence inequality does not follow just from calling tails fat.

The rolling GJR implementation has a material timing limitation. At each refit, `garch_filter` initializes variance from a segment including some evaluation observations, so the forecast series is not strictly past-measurable. Parameters are otherwise periodically estimated on preceding data; residual centering and approximation choices also remain as coded. Reported tests compare this unchanged implementation descriptively. Non-rejection is not proof of calibration, independence, suitability or equality between models. Calendar-year traffic-light counts differ from the historical regulatory 250-day windows. Kupiec and Christoffersen use chi-square asymptotics; sparse counts and dependence affect finite-sample calibration. Z2's iid normal/t4 critical values are two null examples, not a distribution-free theorem.

The marginal peaks-over-threshold limit requires a maximum domain of attraction. Dependence affects estimation/inference and may need mixing or declustering conditions; filtering does not guarantee iid shocks. Positive fitted GPD shape motivates regular variation without proving a universal population tail law. Under an assumed power tail with exponent zeta, moments strictly below zeta can exist and those strictly above diverge; equality is a separate boundary question. The cached xi=0.1967 implies a fitted exponent about 5.08, so claiming that the fifth moment must be infinite would be wrong. Finite ES requires xi<1. Hill uses the k largest positive observations divided by the next, `(k+1)`st order-statistic cutoff. Its reference line is shown on an expanded axis. No confidence interval is calculated for remote-tail quantiles.

Industry one-percent co-exceedance frequencies are finite-threshold conditional statistics. Gaussian zero asymptotic tail dependence does not imply impossible joint crashes or riskless senior tranches. A copula's latent correlation parameter need not equal Pearson correlation after nonlinear marginal transforms. Selected-crash correlation estimates a different conditional population; the observed gap does not identify a causal selection decomposition. The fixed covariance for retrospective factor stress uses 1990–2020, including dates after some replayed crises. Mahalanobis distance is not a one-dimensional Gaussian tail probability. A minimum-distance loss route is maximum-density only for suitable elliptically decreasing distributions, with a zero-centered linear loss and positive-definite covariance in this illustration.

The rearrangement output is a finite-grid alternating heuristic with an iteration cap and a capped last upper quantile. Agreement of two grids does not certify global optimality or continuum lower/upper bounds. The analytic sum-of-ES bound is separate and valid for integrable marginals. The network is one seeded run trained through 1990 against adaptive comparators, not an architecture-wide or causal test. A trading decade has about 25 nominal 1% tail observations; 65 years have about 164, not 650. DM inference uses a five-lag HAC estimate and its asymptotic dependence/moment assumptions; non-rejection is not equivalence. Proposed better inputs or residual models were not newly trained.

## Scoring, calibration and the proof

Elicitability specifies a distribution class, action domain and finite expected scores. Pinball loss has derivative F(q)-tau at continuity points and subgradient `[F(q-)-tau,F(q)-tau]` at atoms. Its minimizing set is the quantile set; strict consistency for a point requires uniqueness. If a strictly consistent score elicits T and `T(F0)=T(F1)=t`, then the mixture's expected score is a mixture of uniquely minimized scores, so `T(lambda F1+(1-lambda)F0)=t`. Thus convex level sets are necessary.

At 90%, `F0=delta_1` and `F1=.95 delta_0+.05 delta_2` have integrated ES 1, but their half mixture has ES 1.25. On a convex class containing them, ES alone therefore has no strictly consistent scalar score. **This does not make ES impossible to backtest.** Calibration/model-verification tests and strict score-based comparison are different tasks. Joint VaR–ES scores exist with suitable domains and assumptions.

For returns use `e<v<0`, a unique continuous tau quantile, finite first moment, negative true ES and finite expected score. FZ0 is

`S(v,e;r)=-1{r<=v}(v-r)/(tau e)+v/e+log(-e)-1`.

For fixed e<0, `partial_v E S=(F(v)-tau)/(-tau e)`, which changes sign at the unique quantile q. Put `A(v)=v-E(v-R)^+/tau`. At q, `A(q)=e_true`. The other derivative is `(e-A(v))/e^2`; at q it changes from negative to positive at true ES. Minimize v first, then e, to obtain the global pair minimum on the stated action domain. Atoms/nonunique quantiles require the general theorem. Scaling returns and forecasts by c>0 adds log(c); score differences are invariant, but absolute FZ0 score levels are not literally unit free.

The finite 400,000-draw heatmap samples every second full-grid point, whereas the reported minimum uses the full grid. A grid/sampling match is numerical evidence, not proof of exact population equality. The power experiment changes the full t3/normal distributions while matching one VaR; it does not change only the tail. Its 2,000 replications of length 1,000 and 4,000 simulated normal-null critical-value replications have Monte Carlo error and model-specific calibration.

QLIKE can target a correctly specified conditional second moment or suitable unbiased proxy under its assumptions. It does not elicit unconditional variance with unknown mean from a single raw observation. Squared error elicits a mean; fixed-benchmark out-of-sample R-squared is a normalized loss comparison. The expectile risk convention is minus a lower return expectile, tau<=1/2, or an upper loss expectile. Classification among law-invariant coherent elicitable risks needs an atomless rich space and its regularity assumptions.

## Historical Basel and liquidity scope

[Basel 2019, MAR33](https://www.bis.org/publications/201901-standards-minimum-capital-requirements-market-risk.pdf) specifies a ten-day base from ten-day factor changes **without shorter-horizon scaling**, then nested factor subsets at longer liquidity horizons. The displayed cascade includes all-factor base ES squared plus successive nested-subset ES squared times horizon increments/10. The cached table instead scales one-day historical ES by root ten; it is explicitly a synthetic single-horizon illustration, not a compliant base or full bank capital. Corrected visible examples: large-cap equity price 10; IG sovereign spread and large-cap equity volatility 20; HY sovereign/IG corporate spread 40; HY corporate spread and small-cap equity volatility 60; credit-spread volatility 120 days. The original cache's overbroad category strings remain unaltered, and presentation corrects their interpretation.

P&L attribution compares risk-theoretical with hypothetical P&L on a specified static portfolio, not simply realized front-office P&L. Stress calibration, constrained aggregation, default and non-modellable risks add requirements. [The 1996 backtesting framework](https://www.bis.org/publications/199601-standards-supervisory-framework-use-backtesting-conjunction-internal-models-approach-market-risk-capital.pdf) is historical; local implementation and current requirements are not certified here. Root participation is a chosen terminal-impact scale; under a cumulative square-root trajectory its average over quantity is two thirds of terminal impact before fees, spread and other effects. It is not automatically average execution cost or a universal VaR add-on.

## Primary sources checked

- [Gneiting, Making and Evaluating Point Forecasts](https://arxiv.org/abs/0912.0902): task-matched scoring and non-elicitability.
- [Fissler and Ziegel, Higher order elicitability and Osband's principle](https://arxiv.org/abs/1503.08123): joint elicitation and conditions.
- [Fissler, Ziegel and Gneiting, ES jointly elicitable with VaR](https://arxiv.org/abs/1507.00244): explicitly distinguishes model-verification backtests from elicitability.
- [RiskMetrics Technical Document, 1996](https://www.msci.com/documents/10199/5915b101-4206-4ba0-aee2-3449d5c7e95a): EWMA and historical context.
- Basel sources above, read from their actual landing-page PDF links. The guessed JPMorgan task-force URL returned 404, so the unsupported operational anecdote is removed; that failure is retained, not cited as evidence.

## Twelve worked problems — six foundations

1. **Normal, zero mean, sigma=1%.** `VaR_alpha=sigma Phi^-1(alpha)`; `ES_alpha=sigma phi(Phi^-1(alpha))/(1-alpha)`. At 99% they are 2.32635% and 2.66521%; at 97.5%, 1.95996% and 2.33780%. These are additive daily loss units, not capital approval.
2. **Stationary Gaussian AR(1), phi=.1.** With marginal variance sigma², lag-k covariance is sigma² phi^k. Summing all diagonal and off-diagonal terms gives `Var(sum_1^10 r)=sigma²[10+2 sum_1^9(10-k).1^k]=11.975308642 sigma²`. Its SD factor is 3.460535889, versus root ten 3.162277660. Zero-mean Gaussianity transfers that SD factor to the selected quantile; it is not a compounding formula.
3. **Independent 3% defaults of 100.** Each zero-loss mass .97 exceeds .95, hence VaR95=0. Joint zero-loss mass is `.97²=.9409<.95`; cumulative mass through loss100 is `1-.03²=.9991>=.95`, hence joint VaR95=100. This is a non-subadditivity example, not a claim that diversification increases every risk functional.
4. **Eight hits, T=250, p=.01.** With phat=.032, `LR=2[x log(phat/p)+(T-x) log((1-phat)/(1-p))]=7.733550724`. A chi-square1 asymptotic p-value is .0054204. Historical Basel yellow covers 5–9 exceptions; at eight the base-plus-add-on multiplier is 3.75 in that historical framework. Sparse-count asymptotics and current local requirements are separate questions.
5. **Ten hits, first/last zero, four adjacent hit pairs.** Among 999 transitions, `n11=4`, `n10=10-4=6`, `n01=6`, `n00=999-16=983`. Thus `p11=4/(4+6)=.4` and `p01=6/(983+6)=.006066734`. The large difference indicates first-order clustering in this sequence. It does not identify volatility as its cause; without endpoint information the exact denominators would be underspecified.
6. **GPD extrapolation.** `u=.02,xi=.2,beta=.008,N_u/n=.04,alpha=.999`. The exceedance multiplier is `(25*.001)^(-.2)`. Hence `VaR=.02+.008/.2[(.025)^(-.2)-1]=.0636511642` and `ES=(VaR+.008-.2*.02)/(.8)=.0845639553`. Require alpha above the threshold's percentile, support positivity and xi<1 for finite ES. These are chosen parameters, not another fitted historical tail.

## Four advanced solutions

7. **t copula, rho=.5, nu=4.** The lower-tail limit is `2 t_5(-sqrt(5*(1-.5)/(1+.5)))=2 t_5(-sqrt(5/3))=.2531699951`. It is a limit of a conditional probability, not the joint probability at a finite 1% threshold; rho is a latent copula parameter.
8. **Reverse stress, dollar SD=2m, target16m.** With zero center, positive-definite covariance Sigma and a linear loss `-w'x=L`, minimize `x'Sigma^-1 x`. Lagrange differentiation gives `2 Sigma^-1 x+lambda w=0`, so `x*=-L Sigma w/(w'Sigma w)`. Substitution satisfies the constraint and gives distance `L/sqrt(w'Sigma w)=8`. Positive definiteness gives uniqueness; maximum-density interpretation additionally requires a suitable elliptical model.
9. **Three Lomax/Pareto-II losses, exponent2.** Their quantile is `q_u=(1-u)^(-1/2)-1`; VaR99=9. Integrating the upper tail gives `ES99=2/sqrt(.01)-1=19`. For any dependence, `VaR99(sum)<=ES99(sum)<=sum ES99=57`, using integrability and ES subadditivity. The cached grid estimate about45.9 is separate numerical evidence, not a certified optimum or proof that57 is sharp.
10. **Chosen single-horizon ES, 5m base at10days and60day horizon.** The illustration gives `5 sqrt(60/10)=12.247448714m`. This is one-horizon scaling, not complete FRTB capital. A compliant ten-day base must itself use ten-day risk-factor changes, with nested subset aggregation and other regulatory charges handled separately.

## Two qualifying solutions

11. **Pinball, level sets, ES obstruction and variational formula.** For finite E|Y|, expected check loss is convex. At a continuity point differentiation yields `(1-tau)F(q)-tau[1-F(q)]=F(q)-tau`. At atoms use left/right derivatives `F(q-)-tau` and `F(q)-tau`; minimizers satisfy `F(q-)<=tau<=F(q)`. Uniqueness gives strict consistency. If T is elicited by S and equal to t at F0 and F1, every alternative x has strictly higher expected score in each distribution. Linearity of expectation preserves that strict inequality in nontrivial mixtures, forcing the mixture's T to be t. Now F0=delta1 and F1=.95delta0+.05delta2 both have ES90=1: the latter tail splits 5% twos and5% zeros. In the half mixture, the worst10% contains2.5% twos plus7.5% ones, giving `(2*.025+1*.075)/.1=1.25`. The level set fails convexity, ruling out a strictly consistent scalar ES score on this class, without ruling out calibration tests. Finally `g(v)=v+E(L-v)^+/(1-alpha)` is convex, with subgradient containing zero exactly when `F(v-)<=alpha<=F(v)`. At such v, `g(v)=[E L1{L>v}+v(F(v)-alpha)]/(1-alpha)`, which splits the cutoff atom and equals integrated-tail ES. This proves the formula for integrable losses, including atoms.
12. **Z2 and the global joint-score minimum.** Let forecasts be measurable with respect to information H_(t-1), with a continuous conditional alpha quantile v_t, nonzero positive ES e_t and the relevant ratios integrable. Then `E[L_t 1{L_t>v_t}|H]=(1-alpha)e_t`, so `E[L_t I_t/e_t|H]=1-alpha`. Iterated expectation gives E Z2=0 even for random forecasts; no exchange of a random denominator with expectation is assumed. If VaR stays correct but the forecast ES is lower, expected Z2 is `T^-1 sum E[e_true,t/e_forecast,t]-1`, positive under pointwise underestimation, not generally a ratio of unconditional means. For the lower-return FZ0 convention assume e<v<0, a unique continuous tau quantile and finite first/score moments. At fixed e, `partial_v E S=(F(v)-tau)/(-tau e)` changes from negative to positive at q. At q set `e_true=q-E(q-R)^+/tau`. Then `partial_e E S=(e-e_true)/e²`, negative below e_true and positive above. Thus v=q is globally optimal for each fixed e and e=e_true is globally optimal there: the pair is the global minimum in the stated domain. At the root the second derivative in e is `1/e_true²>0`, but the sign argument supplies the global result. General atoms/nonunique actions require the broader theorem.

# 第40部分：度量风险

十三个场景讨论分位数、积分尾部预期亏损、回测、极值、相依性、压力、学习模型与历史巴塞尔方法。风险汇总表是研究设计，不是同一实盘组合的完整资本报告，也不构成上线或资本批准。

## 数据与结论边界

十三个经审计的常规原始计算各调用一次，十二个成功。`extra`因访问图漏列Binance组装日线键，在原校验器调用前被屏障阻止；这属于审计缺口，不是已证明的冻结哈希不符。不重试、不扩大授权后重跑、不读取或复用部分输出、不换一个历史拟合。其阈值扫描、比特币尾部、Copula组合模拟、历史欧拉表与最差窗口表均删除，以明确标记的公式或选定例子说明概念。

初始图列出43个可能公共键，遗漏的组装键使完整依赖至少多一项；不能称原图穷尽，也不能把可能依赖说成实际全部读取。十个既有拒绝键与本次阻止键持续拦截。只使用截至2020年末的French研究数据和获准模拟结果，不打开、读取或评分封存策略。所有原始金融算法、每个`compute.py`与98个受保护文件不变。本轮没有刷新、新市场试验或登记变化；累计计数截至第40部分为23,561、全局23,562。

## 科学解释

VaR为广义分位数，严格突破概率至多1-alpha；连续正确校准时才等于它。ES定义为上尾分位数的积分，遇到分位点原子须拆分边界质量，不能一概写作含全部边界原子的条件均值。原历史助手使用插值分位数及阈值以上样本均值，对任意离散样本不等于精确积分ES；债券与混合反例单独拆分原子。

平方根时间法则假设零均值、独立同分布正态的可加日损失；非零收益均值按天数线性累加。历史十日量是重叠简单日收益之和，不是复利财富变化；差距不能唯一归因于自相关或波动聚集。期权二阶近似省略theta，完全估值减少一天期限，故两者差异不只代表gamma近似误差；五点波动冲击施于全部路径。

GJR每次重估段的初始方差使用含部分评估期收益的片段，因此结果并非严格只依赖过去信息的预测验证。未拒绝选定检验不等于模型正确、适用或彼此等价。日历年度红黄次数不等于监管滚动250日窗口。Z2的两种iid临界值不是分布无关定理。

超阈值极限定理需要适当最大吸引域；边际极限与相关样本推断不同，过滤不保证残差独立。拟合正形状并不证明真实总体幂律。xi约0.1967给出拟合指数约5.08，不能据此声称五阶矩必定无限；严格低于、严格高于指数及等于指数的边界问题应分开。有限ES需xi<1。Hill使用前k大值相对于第k+1大值的比率。

行业1%共突破是有限阈值统计，不是渐近尾部相依系数；高斯系数为零不表示联合危机不可能或高级分层无风险。Copula潜在相关参数不必等于边际非线性变换后的Pearson相关。条件崩盘相关度对应另一个条件总体，不能把差距全部识别为偏差。压力距离用1990–2020协方差，早期危机属于回顾对比；Mahalanobis距离不是一维正态尾概率。重排数值是有限网格、有上端截断与迭代上限的启发式，不是全局最优或连续界的认证。

网络只运行一个种子，参数冻结，而比较模型自适应；65个交易年约有164个名义1%尾部观测，不是650个。DM采用五阶HAC近似，其非拒绝不是等价证明，也不识别模型结构的因果优劣。未来输入或残差模型只是研究方向，没有新增训练。

ES不可单独严格评分引出，不等于不能回测。校准检验、模型验证与一致评分比较是不同任务。Pinball在原子处使用次梯度；唯一分位数才给出唯一严格最优。FZ0在负尾域及唯一连续分位数、有限矩等条件下可共同引出VaR和ES。单位乘c会使绝对分数加log(c)，差分保持不变；绝对水平不是字面上的无单位。QLIKE针对适当条件二阶矩，不是未知均值的无条件方差。Expectile分类须说明符号、无原子丰富空间与正则性。

巴塞尔2019要求十日风险因子变化形成基础ES，不能由一天ES简单开方缩放。原缓存表正是后者，故只作为单期限缩放示例，不是合规十日基数或完整资本。显示类别按2019表修正：大盘股价10日；投资级主权利差及大盘股波动20日；高收益主权、投资级公司利差40日；高收益公司利差及小盘股波动60日；信用利差波动120日。P&L归因比较风险理论与假设静态组合P&L，不是简单比较实际前台交易损益。本段不认证当前本地法规。平方根冲击若表示终点价格冲击，平均执行成本需沿数量积分；选定轨迹下为终点的三分之二。

## 十二道完整解答：六道基础

1. **正态。** 零均值、sigma=1%，VaR=sigma乘正态分位数，ES=sigma乘该点密度再除尾概率。99%分别为2.32635%、2.66521%；97.5%分别为1.95996%、2.33780%。它们是可加损失单位，不是资本批准。
2. **AR(1)。** 平稳零均值高斯、phi=.1、边际方差sigma²时，k阶协方差为sigma² phi^k。十日和的方差为`[10+2 sum_(k=1)^9(10-k).1^k]sigma²=11.975308642sigma²`，标准差因子3.460535889。高斯零均值才能把该因子直接用于分位数；不是复利公式。
3. **3%独立违约。** 单只零损失概率.97≥.95，故VaR95=0。两只零损失概率.9409<.95，而损失不超过100的概率.9991≥.95，故联合VaR95=100。这说明VaR不次可加，不表示所有风险函数都惩罚分散。
4. **8次突破。** T=250，目标p=.01，经验比例.032。似然比`2[8 log(.032/.01)+242 log(.968/.99)]=7.733550724`，卡方1自由度近似p=.0054204。历史1996黄区为5–9次；8次对应乘数3.75。稀疏样本近似与现行本地规则另论。
5. **成簇。** 1000天、首尾指标均为0、10个1、4个相邻11对：共有999个转移，n11=4、n10=6、n01=6、n00=983。因此p11=.4，p01=6/989=.006066734。差距提示一阶聚集，但不识别波动率为原因；缺少首尾条件时精确分母不充分。
6. **GPD。** u=.02、xi=.2、beta=.008、超额比例.04、alpha=.999，则`VaR=.02+.04[(.025)^(-.2)-1]=.0636511642`；`ES=(VaR+.008-.004)/.8=.0845639553`。须目标超过阈值百分位、满足支撑条件，且xi<1保证有限ES。参数是选定例子，不是新历史拟合。

## 四道进阶

7. **t Copula。** rho=.5、nu=4时，系数`2 t5(-sqrt(5/3))=.2531699951`。这是条件概率的极限，不是1%阈值的联合概率；rho为潜在相关参数。
8. **反向压力。** 零中心、正定Sigma、线性损失约束`-w'x=L`。拉格朗日一阶条件`2 Sigma^-1 x+lambda w=0`，代入约束得`x*=-L Sigma w/(w'Sigma w)`。最小距离`L/sqrt(w'Sigma w)=16/2=8`；正定性保证唯一。最大密度解释还需适当椭圆递减分布。
9. **相依界。** 三个指数2的Lomax损失，`q_u=(1-u)^(-1/2)-1`，故VaR99=9；积分上尾得到ES99=`2/sqrt(.01)-1=19`。对任何相依，`VaR(sum)≤ES(sum)≤3*19=57`。约45.9的缓存网格量只是数值估计，不认证最优，也不证明57为锐界。
10. **单期限示例。** 十日ES=500万、期限60日，选定开方规则给`5 sqrt(6)=12.247448714`百万。并非完整FRTB资本；十日基数、嵌套因子集合、压力及其他资本项须另满足规定。

## 两道资格题

11. **引出与ES反例。** E|Y|有限时，期望pinball损失为凸函数。连续点导数为F(q)-tau；原子处左右导数为F(q-)-tau、F(q)-tau，因此最小化条件为F(q-)≤tau≤F(q)。唯一分位数给严格一致性。若严格评分S使F0和F1的函数值同为t，则任何x≠t在两者下期望损失均更大；期望对分布混合线性，非平凡混合也唯一由t最小化，故水平集必须凸。现取F0=delta1、F1=.95delta0+.05delta2；两者ES90=1，后者尾部取5%的2及5%的0。半混合的最差10%为2.5%的2和7.5%的1，均值`(.025*2+.075*1)/.1=1.25`，故ES水平集不凸。在包含这些分布的凸类上，无严格一致标量ES评分，但仍可做校准回测。最后`g(v)=v+E(L-v)^+/(1-alpha)`为凸函数；0属于其次梯度当且仅当F(v-)≤alpha≤F(v)。在此v处，`g=[E L1{L>v}+v(F(v)-alpha)]/(1-alpha)`恰好拆分分位点原子，等于积分ES。这证明可积损失（含原子）的变分公式。
12. **Z2与联合评分。** 预测v_t、e_t对前一期信息H可测，条件损失连续，v为正确alpha分位数、e为非零正ES，并假设相关比率可积。则`E[L_t I_t|H]=(1-alpha)e_t`，所以`E[L_t I_t/e_t|H]=1-alpha`；迭代期望给E Z2=0，未把随机分母移到期望外。若VaR正确但ES逐点低估，则期望Z2为`T^-1 sum E[e_true/e_forecast]-1>0`，通常不是无条件均值的比。FZ0改用负收益尾：e<v<0、唯一连续tau分位数、有限一阶与评分矩。固定e，v导数`(F(v)-tau)/(-tau e)`在q由负转正。定义`e_true=q-E(q-R)^+/tau`，在q处e导数`(e-e_true)/e²`也由负转正。先对v再对e全局最小化，证明该域的联合唯一最优；根处e二阶导数为1/e_true²>0，但全局性来自符号论证。原子与非唯一动作须用一般定理。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part40.md`](../../../docs/qa/quant/part40.md).*
