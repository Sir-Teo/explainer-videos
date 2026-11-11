# Quant, Built — Part 24: Factors

Seventeen chapters connect factor definitions, model tests, crashes, international evidence and implementation limits. Research return calculations end in December 2020. Chapter 13 is a conceptual registration and holdout-accounting lesson: this review neither opens nor scores the sealed experiment. The endpoint and motion visual review is complete; production listening remains separately pending.

## Evidence and reproducibility

The review restored all thirteen permitted original items using normal frozen checks. Seventeen actual invocations comprise thirteen initial attempts and four ordinary dependency retries: the initial four failures were missing `openpyxl`, not data-hash failures. Installing the already-declared locked dependency allowed all four retries to pass. The initial failures and invocation records remain preserved. No force, refresh, registry rewrite or substitute historical strategy was used.

The dependency closure uses eighteen preexisting public manifest entries. Some French, AQR and q-factor readers consume named public observations through 2025 before the December 2020 calculation cutoff; the public CH4 source also contains 2021. Updated/backfilled public files are not contemporaneous vintages. Source metadata in the public BE/ME archive identifies June formation and prior-December market equity, but the annual spread block's exact release/snapshot clock is not reconstructed. Its year labels must not be described as verified December snapshots.

`common.load` rejects envelope-prefixed items before the original cache or counted loader can run. House and Outro load only permitted originals. The review adds no registration, opening, score or market trial. All 98 protected compute, House and registry files remain byte-identical to the baseline; the baseline counters are Part 24 cumulative 327 and global 23562. Local evidence is under `renders/qa/quant24/`; tracked review records are under `docs/qa/`.

## Scientific interpretation

- Capitalised excess/long-short research indices omit cash yield, funding, borrow and transaction costs. Zero net initial outlay is not zero margin or capital. Annual means are arithmetic. The original drawdown starts its peak at the first observed compounded value, omitting the initial-one anchor; statistics drop missing rows while cumulative indices zero-fill them.
- The preserved `econ.grs` uses residual covariance `U'U/(T-K-1)` and factor covariance with denominator `T-1`, but the GRS prefactor assumes ML moments. Saved F/p entries are legacy proxies, not exact standard-GRS calibration. Standard theory instead uses ML residual and factor covariances, iid Gaussian homoskedastic errors, full rank and `T>N+K`. No corrected market regression or p-value is substituted.
- The two-pass calculation uses fixed full-sample betas. Its saved covariance inflation multiplies slope covariance by `1+c` and adds factor covariance divided by T, re-adding variance already present under the usual traded-factor setup. Saved adjusted t values are legacy proxies, not formal Shanken, HAC or multiple-testing certification. Separate alpha regressions use lag-6 Newey–West; mean t and moment Sharpe errors are iid-style benchmarks. Nonrejection does not prove zero expected alpha, payoff spanning, efficiency or absence of residual risk.
- The forty-stock sort is one illustrative cross-section, not a June-vintage production replication. Balancing 2×3 cells does not remove all characteristic exposures. The pre/post-1981 split is descriptive; it does not identify publication effects, especially for value's different discovery history.
- The TSMOM smile uses the published aggregate column, nonoverlapping three-month groups aligned to calendar quarters from January 1985, and compounded market excess returns. Its same-sample quadratic is not a straddle payoff or guaranteed crisis hedge. The crash table shows six entries from the original eight-entry worst-month inventory. Conditional crash subgroups use the current excess-market sign ex post, after a prior-24-month total-market bear indicator; the first 24 warmup months are classified normal.
- The unchanged scaling rule uses six **monthly** observations, annualises sample volatility by √12, targets 12% and caps exposure at 3. It is not the cited original daily-realised-volatility implementation. Raw/scaled statistics use the same finite mask. The sample Sharpe improves from 0.46 to 0.75, but the worst scaled month still loses 38%; funding, costs, margin and historical vintages are untested.
- The dividend-discount table is a finite 200-year payout toy without terminal book value. Infinite-horizon Gordon comparative statics require constant ROE/growth, `r>g` and a suitable terminal condition. A small conditional HML alpha is not exact spanning. Public q-factor releases do not reconstruct recursive forecasts or historical parameter availability here.
- BAB is neutral to estimated betas, not guaranteed realised-beta neutral or safe. Futures require mandate permission, collateral and effective-leverage limits. International value/momentum mixes beat both components in all eight original samples; negative correlation alone does not guarantee this or protect every bad year. Futures carry `S/F-1` refers to profit to expiry normalised by initial futures price, with unchanged spot; margin return, contract units and collateral yield are separate.
- HML's September 2020 trough index is about 0.422, ending December near 0.442; the preserved first-observation-peak drawdown is −57.49%. The four-standard-error comparison is conditional on iid stationary returns and a fixed historical mean/volatility, not a selection-adjusted probability. Relative valuation identities need cash-flow, terminal and stationarity assumptions before they motivate positive future premia.
- Green expected-return statements are conditional equilibrium claims. News adjustments are observational, not unique causal identification. The fixed-seed chart adds shocks to simple returns; Problem 10 explicitly uses multiplicative price shocks. A popularity episode can bias a historical mean without necessarily reversing its sign.
- The annual timing regression pairs published spread row `y-1` with calendar-year `y` HML (93 pairs, 1928–2020). Its full-sample fit and lag-2 Newey–West t are descriptive, not a reconstructed real-time forecast. TSFM contains UMD, so regressing UMD on TSFM has mechanical self-exposure, not independent explanation or incremental signal evidence. The rule uses six equal signed exposures, not covariance-aware risk parity. Likewise `equal_risk` is inverse-volatility allocation, not equal total risk contribution.
- Chinese and US factors share dates, not universes, definitions, implementation costs or a controlled experiment. Historical shell/IPO mechanisms refer to 2000–2020; registration-based IPO reform expanded in 2023. Returns alone do not establish retail causality.
- The research panel retains 40 complete-history industries from 49 using the entire 1926–2020 window. Formation signals sum log returns; holding returns are simple. The second rule uses twelve formation months and skips one, unlike classic eleven-month 12–2 momentum. A single scale makes **average** long exposure one, not every month's gross exposure. Covariance denominator T makes the decomposition exact. The original 400 resamples use 24-month nonwrapping blocks and exclude the last possible start. This finite bootstrap and exact accounting do not identify a causal information network.

## Chapters and builds

The manifest orders the opening, model tests, size/value, momentum, crashes, profitability/investment, low risk, international styles, value drawdown, green returns, timing, China, industry, conceptual accounting, House, research and recap. Problems are paginated 6/4/2. English and Chinese narration carry the same qualifications.

Activate the workspace environment before Manim commands. Use audited, explicit permitted cache items only. Do not run the default all-items compute command: it includes the excluded experiment. A silent scene preview is `EXPLAINER_TTS=silent python tools/qa_scene.py quant24 Crash`. Complete production narration/listening is distinct from sampled CPU speech checks and timing previews.

## Six desk answers

1. Value/momentum covariance improves this historical mix, but future premia, costs and simultaneous losses can overturn it.
2. A practically useful model may have small errors despite rejection. Check inference calibration, error locations, residual risks, costs and genuinely new validation; rejection is not inevitable merely because T is large.
3. A post-1981 size t near 0.6 cannot distinguish disappearance from imprecision or composition changes. The split alone does not identify publication causality.
4. Reassess momentum within a predeclared risk budget. The ex-post rebound beta is not advance knowledge; hedging/scaling changes costs and foregone upside and does not guarantee protection.
5. Compare effective leverage, collateral, margin and mandate permission before considering futures. A borrowing prohibition may also restrict derivatives; an anomaly is not a suitable-trade certificate.
6. The annual spread's high historical rank and weak full-sample fit do not establish a December real-time forecast or guarantee the next return. No sealed outcome is used to answer this question.

Research pause: for N=2, if the only nonzero cross covariance is `Cov(x_1,r_2)=c>0`, its profit contribution is `−c/4`. This describes that cross term only; different means can add another component. No autocorrelation alone does not force the total profit to equal `−c/4`.

## Twelve problems, with worked solutions

1. **Squared-Sharpe gain.** Write `R=α+Bf+ε`, with mean-zero ε orthogonal to f. Transform the joint portfolio space to `(f,R-Bf)=(f,α+ε)`. The second block has **mean α**, not mean-zero ε, and covariance Σ. With matching moments, cash convention and unrestricted weights, block orthogonality gives `SR²(f,R)=μ_f'Ω⁻¹μ_f+α'Σ⁻¹α`. The gain is `α'Σ⁻¹α`; there is no additional `1+SR_f²` divisor in this identity. That divisor belongs in the GRS statistic.
2. **One asset and covariance conventions.** Let `ν=T-K-1`, `s_e²=U'U/ν`, `Ω_ML=F_c'F_c/T` and `q=f̄'Ω_ML⁻¹f̄`. Then `Var_OLS(α̂)=s_e²(1+q)/T`, so `t_OLS²=Tα̂²/[s_e²(1+q)]`. Standard GRS uses `Σ_ML=(ν/T)s_e²`; for N=1, `F=να̂²/[Σ_ML(1+q)]=t_OLS²` exactly. The preserved mixed-convention proxy instead satisfies `J/t_OLS²=(ν/T)(1+q)/[1+(T-1)q/T]`, not merely `ν/T`. This is a theoretical algebra exercise, not a corrected historical regression.
3. **2×3 arithmetic.** `SMB=(1.2+1.0+1.5)/3-(0.6+0.8+1.1)/3=0.40%`. `HML=(1.5+1.1)/2-(1.2+0.6)/2=0.40%`. This is one cross-section's cell arithmetic, not a production-factor replication.
4. **Gordon comparison.** With constant ROE/growth, `r>g`, clean-surplus payout assumptions and an appropriate terminal condition, `M/B=Σ(ROE-g)(1+g)^(τ-1)/(1+r)^τ=(ROE-g)/(r-g)`. With ROE 12%, g 5%, B/M 0.8: `1.25=0.07/(r-0.05)`, hence **r=10.6%**. The finite 200-year scene toy is only an approximation to this infinite sum.
5. **Mix.** Mean 4.5%; variance `¼(0.01+0.01-1.2×0.01)=0.002`; volatility 4.472%; Sharpe **1.006**, versus 0.4 and 0.5. Assumed fixed moments and costless rebalancing; no general dominance guarantee.
6. **Rebound beta.** `β_UMD=0.8-1.8=-1`. A 15% market return contributes **−15%** under the stated fixed-beta linear relation, before alpha, residual news and costs; it is not a realised-return guarantee.
7. **Monthly scaling.** Exposure `min(3,0.12/0.40)=0.30`; a −34% factor month contributes **−10.2%**, excluding cash/funding/costs. The volatility estimate must precede the return; target volatility is not guaranteed realised volatility.
8. **BAB.** `0.6%/0.7-0.8%/1.5=0.32381%` monthly. Multiplying by 12 gives **3.886% arithmetic annualisation**, not a compounded annual return. Estimated beta is `0.7/0.7-1.5/1.5=0`; realised beta, leverage and funding risk can differ.
9. **Years.** Under iid returns and a stable known premium/volatility, `t≈SR√Y`. Thus `Y=(2/0.45)²=19.75` years and `SR=2/√5=0.8944` for five years. These are precision approximations, not power guarantees or selection-adjusted significance thresholds.
10. **Green/brown multiplicative surprise.** With a surprise multiplier applied after baseline return, green `(1.05)(1.10)-1=15.5%`; brown `(1.07)(0.95)-1=1.65%`. The price shock alone **does not determine next-year expected returns**. They remain 5%/7% only under an additional fixed-conditional-return law after the level shift; other cash-flow or discount-rate changes can produce different expectations. The chart's additive shock toy uses another explicitly stated convention.
11. **Exact sample decomposition.** Use covariance denominator T. `π̄=(1/N)Σ_i overline(x_i r_i)-overline(x̄_t r̄_t)`. Expand each product into covariance plus means, and use `Cov(x̄_t,r̄_t)=(1/N²)Σ_ij Cov(x_j,r_i)`. The diagonal coefficient is `(N-1)/N²`, off-diagonal coefficient `-1/N²`, and means contribute `(1/N)Σ_i(μ_xi-μ_x)(μ_ri-μ_r)`. This holds for the specified log-formation/simple-holding data without a causal interpretation.
12. **Known population.** Let `r_it=μ_i+f_t+e_it`, equal unit factor loadings, iid f independent of all idiosyncratic innovations, and independent stationary `e_it=φe_i,t-1+z_it`. For one-period simple-return formation, own covariance is `φσ_z²/(1-φ²)`; cross covariance is zero in the population. The own contribution is `(N-1)φσ_z²/[N(1-φ²)]`; the mean contribution is the cross-sectional variance of μ. The equal-loading common factor cancels from demeaned zero-sum weights **path by path**. Finite estimates of the individual components need not equal their population values. Unequal loadings or serial dependence change the result.

## Papers, chapter by chapter

* Hook: Black, Jensen and Scholes (1972); Fama and French (1993).
* ch. 1: Fama and MacBeth (1973); Gibbons, Ross and Shanken (1989); Shanken (1992); Lewellen, Nagel and Shanken
  (2010); Barillas and Shanken (2018).
* ch. 2: Basu (1977); Banz (1981); Rosenberg, Reid and Lanstein (1985); Fama and French (1992, 1993, 1996);
  Lakonishok, Shleifer and Vishny (1994); McLean and Pontiff (2016); Asness, Frazzini, Israel, Moskowitz and Pedersen
  (2018).
* ch. 3: De Bondt and Thaler (1985); Jegadeesh (1990); Lehmann (1990); Jegadeesh and Titman (1993); Carhart (1997);
  Barberis, Shleifer and Vishny (1998); Hong and Stein (1999); Grinblatt and Han (2005); Moskowitz, Ooi and Pedersen
  (2012).
* ch. 4: Daniel and Moskowitz (2016); Barroso and Santa-Clara (2015); Cederburg, O'Doherty, Wang and Yan (2020).
* ch. 5: Fama and French (2006, 2015); Novy-Marx (2013); Hou, Xue and Zhang (2015, 2021); Stambaugh and Yuan (2017).
* ch. 6: Black (1972); Ang, Hodrick, Xing and Zhang (2006); Baker, Bradley and Wurgler (2011); Bali, Cakici and
  Whitelaw (2011); Frazzini and Pedersen (2014); Novy-Marx and Velikov (2022).
* ch. 7: Asness, Moskowitz and Pedersen (2013); Koijen, Moskowitz, Pedersen and Vrugt (2018); Asness, Frazzini and
  Pedersen (2019).
* ch. 8: Cohen, Polk and Vuolteenaho (2003); Asness and Frazzini (2013); Arnott, Harvey, Kalesnik and Linnainmaa
  (2021); Israel, Laursen and Richardson (2021); Eisfeldt, Kim and Papanikolaou (2022).
* ch. 9: Pástor, Stambaugh and Taylor (2021, 2022); Bolton and Kacperczyk (2021); Berg, Kölbel and Rigobon (2022).
* ch. 10: Asness (2016); Haddad, Kozak and Santosh (2020); Ehsani and Linnainmaa (2022).
* ch. 11: Liu, Stambaugh and Yuan (2019).
* ch. 12: Frazzini, Israel and Moskowitz (2018); Novy-Marx and Velikov (2016); press reports on AQR's assets.


# 第二十四部分：因子

十七个章节讨论因子定义、模型检验、崩盘、国际证据与实施边界。收益计算截至二〇二〇年十二月。第十三章仅作登记与留出记账的概念讨论；本次审查没有打开、评分或检查封存实验，也没有新增市场试验。本轮视觉审查已完成；完整成片听审仍另行待办。

十三个允许的原始项目均通过普通冻结检查恢复，共十七次实际调用：最初十三次中四次因缺少已声明的openpyxl失败，安装锁定依赖后普通重试全部成功。原失败记录保留；没有强制刷新、改写登记或用另一历史策略替代。十八个公开清单键均已存在。部分公开文件先读取截至二〇二五年的公开观测，再截至二〇二〇年；CH4公开源还包含二〇二一年。这些回填版本不等于当时实时数据。九十八个受保护文件不变，基线计数为本部分327、全局23562。

旧GRS混合了残差与因子的协方差分母，保存的F与p只能作为代理值；标准精确GRS需要极大似然矩、独立正态同方差误差、满秩及足够观测。固定全样本贝塔的两阶段协方差还重复添加因子方差，调整t值不是正式Shanken校正。另行使用的阿尔法回归为六阶滞后Newey–West，均值t和夏普误差则是独立同分布型基准。不拒绝不证明支付张成、效率或零剩余风险。

因子累计曲线是不计现金利息、融资、借券和交易成本的研究指数，不是实际财富。回撤从首个观测值建立峰值，统计量删除缺失行而指数填零。四十只股票只是单期排序示例；一九八一年前后分段不能识别发表的因果作用。月度缩放使用此前六个月度收益、年波动目标百分之十二、上限三倍，不是原论文的日度已实现波动规则；最差缩放月仍亏损约百分之三十八。条件熊市反弹分组用了当月市场方向，是事后关联。

国际八市场五五组合在各自样本中均超过单独策略夏普，但负相关不保证未来优势。BAB只对估计贝塔中性；低贝塔不等于安全，期货需考虑授权、保证金与有效杠杆。绿色预期溢价是条件均衡说法，新闻调整不是唯一因果识别。因子动量自身含UMD，因此UMD回归存在机械重叠，不能独立解释股票动量。年度价差回归按年份标签配对，不重建十二月快照或实时发布日期。中国的历史制度讨论限定于二〇〇〇至二〇二〇年；全面注册制改革及市场结构变化限制外推。

研究专题从四十九行业中按全区间完整历史选出四十列，形成信号为对数收益之和，持有期为简单收益；十二个形成月再跳一月，不同于经典十一月信号。缩放只让平均多头敞口为一。分母T使记账精确，四百次二十四月非循环自助抽样且漏掉最后可行起点，其推断和因果解释有限。反波动权重不等于考虑协方差的等风险贡献。

## 六个交易台答案

1. 历史协方差改善价值动量组合，但溢价变化、成本和共同下跌都可能使它失效。
2. 实际误差小的模型仍可能有用；检查推断校准、误差分布、剩余风险、成本与真正新样本验证。长样本不必然拒绝模型。
3. 发表后规模t约零点六，无法区分溢价消失、估计噪声和构成变化；分段不识别发表因果效应。
4. 按预先制定的预算调整动量风险，不能把事后反弹贝塔当作事前预警；缩放和对冲仍有成本和失效可能。
5. 先比较有效杠杆、抵押品、保证金与授权，借款限制也可能涵盖期货。异常收益不是适当投资的证明。
6. 年度价差排名极高和弱全样本拟合，不建立十二月实时预测，也不保证下一年收益；不使用任何封存结果。

## 十二道习题与解答

1. 写成`R=α+Bf+ε`，ε均值零且与f正交。组合变换为`(f,R-Bf)=(f,α+ε)`，第二块均值是α。矩约定一致且权重不受限时，最大夏普平方增量为`α'Σ⁻¹α`，不再除以一加因子夏普平方；该分母属于GRS检验统计量。
2. 令`ν=T-K-1`、`s_e²=U'U/ν`、`Ω_ML=F_c'F_c/T`、`q=f̄'Ω_ML⁻¹f̄`。则截距方差为`s_e²(1+q)/T`。标准GRS使用`Σ_ML=(ν/T)s_e²`，单资产时恰有`F=t_OLS²`。保留的混合约定代理则满足`J/t_OLS²=(ν/T)(1+q)/[1+(T-1)q/T]`，不是简单ν/T。这是理论代数练习，不是修正市场回归。
3. `SMB=(1.2+1.0+1.5)/3-(0.6+0.8+1.1)/3=0.40%`；`HML=(1.5+1.1)/2-(1.2+0.6)/2=0.40%`。仅表示单期单元算术。
4. 净资产收益与增长恒定、`r>g`且终值条件适当时，无限几何和给出`M/B=(ROE-g)/(r-g)`。`1.25=0.07/(r-0.05)`，故折现率**10.6%**。成片二百年无终值示例是有限近似。
5. 均值4.5%，方差0.002，波动4.472%，夏普**1.006**。依赖固定矩和无成本再平衡，不是一般优越性定理。
6. 动量贝塔`0.8-1.8=-1`。固定贝塔线性关系下，市场上涨15%贡献**−15%**，尚未计阿尔法、特有新闻及成本，并非实际损失保证。
7. 事前估计波动40%、目标12%时敞口`min(3,0.12/0.40)=0.3`；−34%月份贡献**−10.2%**，未计现金、融资和成本。目标不保证实际波动。
8. `0.6%/0.7-0.8%/1.5=0.32381%`月收益；乘十二得**3.886%算术年化**，不是复利。估计贝塔为零，实际贝塔和融资风险可能不同。
9. 独立同分布、溢价波动稳定且已知时，`t≈SR√Y`，故`Y=(2/0.45)²=19.75`年，五年需`SR=2/√5=0.8944`。这是精度近似，不保证检验功效，也未调整多重选择。
10. 乘法意外价格冲击下，绿色`1.05×1.10-1=15.5%`，棕色`1.07×0.95-1=1.65%`。单次价格冲击**不能确定下一年预期收益**；只有额外假定水平变化后条件收益规律仍固定，才仍为5%和7%。图中的加法简单收益冲击采用另一明确约定。
11. 协方差分母为T。展开`π̄=(1/N)Σ_i overline(x_i r_i)-overline(x̄_t r̄_t)`，再用`Cov(x̄_t,r̄_t)=(1/N²)Σ_ij Cov(x_j,r_i)`。自身项系数`(N-1)/N²`、非对角项系数`−1/N²`，均值项为`(1/N)Σ_i(μ_xi-μ_x)(μ_ri-μ_r)`。这是精确样本记账，不识别原因。
12. `r_it=μ_i+f_t+e_it`，公共因子独立同分布、等单位载荷，特有项独立平稳一阶自回归。单期简单收益形成下，自身总体协方差`φσ_z²/(1-φ²)`、交叉总体协方差零，自身贡献`(N-1)φσ_z²/[N(1-φ²)]`，均值贡献为μ的横截面方差。公共等载荷因子在零和去均值权重中**逐路径抵消**；有限样本各项不必恰等于总体值。非等载荷或因子序列相关会改变结论。

研究专题暂停题：N=2且唯一非零交叉协方差为`Cov(x_1,r_2)=c>0`时，该联系的利润贡献为`−c/4`。这仅指交叉项；均值差异可另有贡献，仅无自相关不意味着总利润必等于`−c/4`。

## Current visual review

Visual pass complete on `quantitative-finance`: 34 bilingual endpoint sheets, 17 English forty-frame motion sheets and 24 focused native frames actually inspected on source `9baf04efcaccf7c7e27dc4a95a29ebb716a97cb2`. The chaptered silent timing preview runs 64:07, with 17 chapters and English subtitles. Eleven CPU speech reports cover 90 sampled lines; the actual narrated opening runs 201.625 seconds. These signal and visual checks do not certify pronunciation or continuous production listening, which remain pending. [Artifact-bound evidence](../../../docs/qa/quant24-polish-evidence.json).

## 当前视觉审阅

本轮已实际检查34张双语旁白节点画面表、17张英文四十帧动画表及24张重点原尺寸画面。分章静音时序预览为64:07，含17章和英文字幕。十一份CPU语音报告覆盖90个抽样句段，并核验实际配音开场。信号与画面检查不替代发音或完整生产成片连续听审，后者仍是独立待办。
