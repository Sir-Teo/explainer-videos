

# Quant, Built — Part 25: The Factor Zoo

Part 25 of [Quant, Built](../README.md), following the [syllabus](../SYLLABUS.md). The lecture preserves the original numerical methods while distinguishing selected published evidence, illustrative inference and a genuinely fresh test. The endpoint and motion visual review is complete; production listening remains separately pending.

The original [compute.py](compute.py), House algorithms and global trial/track/manifest registries are unchanged. Ten permitted original items are restored normally. The envelope item is excluded before either the cache or counted loader; Track is a conceptual accounting chapter, with no experiment result or substitute historical strategy. Educational material, not investment advice.

## Chapters and scientific scope

1. **Two hundred coins.** A fixed 240-month, 200-strategy independent normal-return example and a selected published-predictor census. The best observed mean t is not a prespecified single test. The normal maximum formula assumes independent standard normals; the separate saved maximum simulations draw independent Student-t variables with 239 degrees of freedom. Positive and absolute maxima differ. The square-root-log formula is asymptotic, particularly inaccurate at one try.
2. **Hundreds of factors.** The search count raises a normal Bonferroni threshold. Valid marginal p-values give Bonferroni control under arbitrary dependence; Harvey–Liu–Zhu's t > 3 is a model-dependent research conclusion, not a universal critical value. Fixed base-rate/power arithmetic does not estimate the true share of published factors.
3. **Multiple testing.** Bonferroni and Holm address familywise error in a fixed family. BH bounds expected false-rejection proportion under valid null calibration and independence or suitable PRDS, not arbitrary positive correlation. FDR does not bound realised errors, portfolio losses or funding risk. Saved return p-values use naive iid mean t statistics and normal tails, so formal calibration is conditional. Bootstrap/reality-check methods are conceptual references, not newly executed market inference.
4. **Replication.** Construction, weights, breakpoints, microcaps, sample and data vintage change the estimand. OSAP's documented reconstructions are not identical historical data vintages. The original-paper mask follows SampleStart/End years without an extra 2020 cap; post-publication starts in the next calendar year, ends by December 2020 and needs 24 finite months. Publication and direction selection remain.
5. **Decay and empirical Bayes.** The normal-normal illustration assumes independent unit-noise observations and a normal prior. The posterior-mean slope 0.831 acts on deviations from the fitted prior mean; it is not a premium-retention forecast. The observed post/original mean-return ratio 0.379 and scatter slope 0.426 are different estimands. Their difference is not a causal bias decomposition. Publication-truncation and learning interpretations require assumptions; a one-third to one-half retention scenario is not a universal forecast.
6. **Mined against peer-reviewed.** Published studies and their construction choices are attributed. Expected noise counts use marginal normal probabilities; independence affects joint uncertainty rather than the sum's expectation. Retention in a published study does not calibrate a new strategy's costs or future return.
7. **Shrinking the cross-section.** A centered linear kernel m = 1 − b′(F − μ) has mean one and may be negative. F b is a factor-portfolio return, not m. The House implements isotropic ridge (S + γI)⁻¹μ in the chosen factor units; rescaling changes its prior. The 154-column universe is selected for complete observations from 1973 through 2023 before returns are restricted to 1973–2020. Three contiguous CV folds fit on the other folds, including future observations; the penalty grid uses full-window covariance. The chosen κ uses all observations through 2020, including the later 2001–2020 evaluation window. The split is retrospective, with hyperparameter leakage, not independent chronological validation. Full-window portfolio scaling is also retrospective; split scaling uses the fitting window. Twenty κ settings are in the existing ledger; this review adds none.
8. **Taming the zoo.** The simplified FGX-style code selects two lasso sets and takes their union. Its no-intercept lassos standardise columns without demeaning; the final cross-asset regression adds an intercept and reports HC0. It omits dependent portfolio errors, estimated-covariance uncertainty and the full paper's inference correction. Of 25 recent predictors against 53 older controls, nominal mean/no-control/DS crossings are 21/14/5. These are heuristic, non-nested diagnostics, not certified discoveries. SDF covariance loadings are not automatically mean premia; nonrejection does not establish exact return spanning or no investor benefit.
9. **Weak factors.** The original fixed 400-replication illustration uses N = 50, T = 480 and monthly λ = 0.005 (6% arithmetic annual), with beta scales 1 and 0.05. Classical independent errors-in-variables attenuation is a qualified example, not a general identity for generated betas. Three-pass methods need pervasive factors, rank, normalization and identification assumptions; PCA does not recover every factor by construction.
10. **PCA, RP-PCA, IPCA.** RP-PCA diagonalises F′F/T + γμμ′ with γ = 10 fixed in the original code. γ = −1 gives ML-centered covariance, with the same eigenvectors but rescaled eigenvalues relative to divisor T − 1. The retrospective 1973–2000/2001–2020 split inherits complete-history and publication selection; ten component counts are displayed, and selecting the best adds selection. Later-window RMS intercepts are fitted on that later window, not frozen alpha forecasts. IPCA is conceptual here; characteristic-dependent betas do not make characteristics literally equal to covariances, and alpha nonrejection is not exact pricing.
11. **Comparing models.** On a common union with matching moments and unrestricted traded-factor weights, higher attainable SR² leaves a smaller mean-variance gap. This is not universal model truth, exact payoff spanning or constrained-investor dominance. Finite GRS has model-specific scaling; saved legacy GRS outputs remain proxies. The actual family is ten columns (including EG), market mandatory and at most six total: Σ(j=0..5) C(9,j) = 382 models. Training is 1967–1993; later fixed-weight evaluation is 1994–2020. The top-out list selects on that very window. Maximum SR² uses covariance divisor T − 1, whereas later fixed-portfolio SR uses standard-deviation divisor T. Modern expected-growth histories are not reconstructed recursive-vintage forecasts.
12. **Registration and holdout accounting.** Freeze code, universe, information clocks, missing-data rules, costs, benchmark and decision rule before a genuinely separated test. Hashing does not make examined data unseen. Under the stable modest-Sharpe iid approximation, t ≈ SR_annual √Y and se(SR_annual) ≈ 1/√Y. At Y = 3, se ≈ 0.58 and t = 2 needs SR ≈ 1.15; SR = 0.4 gives t ≈ 0.69. These are fixed arithmetic examples, not sealed results.
13. **The House.** Existing registered count through Part 25 is 348, globally 23,562. The count omits inherited publication searches and does not prove selection-free inference. The 98 protected files remain fixed. Research factor combinations omit realistic trading, funding, collateral, borrow and capital constraints; compounded long-short research indices are not automatically dollar wealth.
14. **For the researcher.** Exact BH FDR = π₀q needs independent p-values with uniform true-null marginals. Storey's untruncated fixed-λ estimator has E π̂₀ ≥ π₀ under uniform nulls; this is not a realised bound, and capping at one can change it. The 400-replication toy uses independent normal nulls and gamma non-null effects; simulation averages have Monte Carlo error. Empirical p-values inherit selected predictors and approximate calibration. Capped π̂₀, adaptive q/π̂₀ BH, kernel density and clipped local ratios are sensitivity diagnostics without automatic finite-sample FDR or posterior certification. The fitted sum Σ(1 − lfdr) is not an identified count of real economic effects.
15. **Recap and exercises.** Fourteen qualified lessons, six desk questions, and all twelve worked problems below. On-screen problems use continuously numbered 6/4/2 pages. Every observed plotted value is retained; axes include original extrema rather than clipping tails to the plotting window.

## Desk questions, with solutions

1. **Best of 200 noise strategies.** Under the saved independent Student-t illustration, the expected positive maximum is about 2.8, or about 3.0 for the absolute maximum. A normal asymptotic formula is only an approximation; dependence and the actual search family matter.
2. **Best t = 2.9 among 200.** For independent standard normals the selected one-sided tail is 1 − Φ(2.9)^200 ≈ 0.31, versus 1 − Φ(2.9) ≈ 0.0019 for a prespecified test. This calibration is conditional on the declared search and null model.
3. **Ten of 100 signals.** Choose and report a discovery-error objective with valid null calibration and dependence assumptions. FDR controls an expectation, not the realised dud count or loss of the selected portfolio; FWER is also meaningful for a family of claims.
4. **Microcap significance.** Equal-weight and value-weight results estimate different portfolios. Neither a t = 4 nor a changed t = 1.2 by itself identifies a persistent premium. Assess sample uncertainty, liquidity, costs and scale.
5. **Published 0.8% monthly.** 0.3–0.4% can be an explicitly labelled sensitivity scenario. The selected historical mean-retention ratio is not a calibrated universal forecast, and net implementation requires separate costs and uncertainty.
6. **Insignificant simplified DS loading.** Nonrejection does not prove spanning or zero incremental utility. Check power, weak identification, covariance and selection uncertainty, factor dependence and implementation. Exact spanning is a stronger payoff statement.

## Problems, with solutions

1. **Normal maximum.** Independence gives Pr(max Zᵢ ≤ c) = ∏Pr(Zᵢ ≤ c) = Φ(c)^n. The median solves Φ(c) = 2^(−1/n); for n = 200 it is about 2.70. This is the median of standard-normal maxima, not the Student-t simulation's mean.
2. **Normal Bonferroni.** For 212 two-sided tests at 5%, p ≤ 0.05/212 = 0.00023585 and |z| ≥ Φ⁻¹(1 − 0.05/(2·212)) ≈ 3.68. The union bound uses valid marginal p-values and permits arbitrary dependence; exact finite-sample Student-t thresholds differ.
3. **Five p-values.** Bonferroni's 0.01 threshold rejects 0.001 and 0.008: two. Holm thresholds 0.01, 0.0125, 0.01667, 0.025, 0.05 yield three before the 0.03 failure. BH thresholds 0.01k have last crossing at k = 4 (0.03 ≤ 0.04), so four.
4. **Conditional empirical Bayes.** Under t = θ + ε with independent ε ~ N(0,1), θ ~ N(4,5), the observed variance is 6. Posterior mean at t = 7 is 4 + (5/6)(7 − 4) = 6.5. A fitted selected-universe model need not be calibrated for future returns.
5. **Ridge in components.** For symmetric positive-definite Σ = Σ_k λ_k q_kq_k′ and γ ≥ 0, (Σ + γI)⁻¹μ = Σ_k (q_k′μ)/(λ_k + γ) q_k = Σ_k [λ_k/(λ_k + γ)] [(q_k′μ)/λ_k] q_k. Positive λ_k permits the unshrunk expression. The isotropic penalty is unit dependent.
6. **Two directions.** Unshrunk loadings are 0.002/0.01 = 0.2 and 0.002/0.0001 = 20. At γ = 0.001 they are 0.1818 and 1.8182. The smaller-eigenvalue direction retains 1/11 of its loading, versus 10/11 for the larger. Under this prior it is shrunk more, without proving its mean is false.
7. **RP-PCA at −1.** F′F/T − μμ′ = Σ_t(F_t − μ)(F_t − μ)′/T. This ML-centered covariance equals (T − 1)/T times the usual sample covariance, so eigenvectors agree but eigenvalues are rescaled.
8. **Classical attenuation.** If β̂ = β + u, u is independent additive error, residuals are orthogonal to β and u, and an intercept is fitted, plim λ̂ = λ Var(β)/(Var(β)+Var(u)) = 0.2λ. These assumptions are not automatic for generated factor betas or weak-factor two-pass inference.
9. **Conditional model comparison.** B has higher attainable SR² (0.8 versus 0.5). For a common union of traded returns and matching moments, the unexplained mean-variance gap is SR²(union) − SR²(model); B leaves a gap 0.3 smaller. Factors themselves can form that common union. Raw finite GRS values have additional model-specific scaling. This does not establish a unique risk story, exact spanning, investor dominance under constraints, or a future winner.
10. **Expected noise counts.** With standard-normal null marginals, 29,000·2Φ̄(2) ≈ 1,320 and 29,000·2Φ̄(3) ≈ 78.3. Linearity of expectation needs no cross-test independence. Dependence does change dispersion and the chance of any exceedance.
11. **Exact BH theorem.** Assume independent p-values and uniform true-null marginals. Let R⁽ⁱ⁾ be BH's rejection count with p_i set to zero, a function only of p₋ᵢ. For k ≥ 1, {p_i ≤ qk/m, R = k} = {p_i ≤ qk/m, R⁽ⁱ⁾ = k}. Lowering a rejected p does not change the final count; conversely a p at most qk/m preserves the kth crossing and cannot create a later one. Independence and uniformity give probability (qk/m)Pr(R⁽ⁱ⁾ = k). Therefore E[V/max(R,1)] = Σ_i∈H₀ Σ_k (1/k)(qk/m)Pr(R⁽ⁱ⁾ = k) = m₀q/m. Valid super-uniform nulls give ≤ rather than exact equality. Independence of the family is an explicit sufficient condition here.
12. **Storey and local/tail rates.** For fixed λ and uniform true-null marginals, E#{p > λ} = m₀(1 − λ) + Σ_i∈H₁ Pr(p_i > λ) ≥ m₀(1 − λ). Dividing proves the untruncated expectation bound; a realised estimate need not be above π₀, and capping at one may break the expectation inequality. For m = m₀ = 1 and λ = 1/2, the capped estimator is 1{p > 1/2}, with expectation 1/2 < π₀ = 1. For a correctly specified two-group density f = π₀φ + (1 − π₀)f₁, and a positive upper-tail probability, Pr(H₀|Z ≥ z) = π₀Φ̄(z)/F̄(z) = ∫_z^∞ [π₀φ(u)/f(u)]f(u)du/F̄(z) = E[lfdr(Z)|Z ≥ z]. This uses a standard-normal null and one consistent positive tail. If lfdr decreases on that tail, the average is at most its threshold value. Arbitrary clipped fitted ratios do not inherit that posterior identity.

## Data access and reproducibility

OSAP release 2024.10 uses the original public `PredictorLSretWide.parquet` and `SignalDoc.csv` readers from Part 3. Their fully read public release includes observations through 2023. Complete-history universe selection therefore uses later missingness, even though return calculations generally end in 2020. Named French and q public archives include observations through 2025 before cuts. Public archive reads are distinct from opening or scoring the excluded sealed experiment; no claim is made that all post-2020 public bytes remain unread.

No force/refresh, new registration, market strategy trial, sealed payload access or replacement historical test is authorised or performed in this review. One initial zoo restore hit a concurrent public-cache temporary-file rename race; its exact failure is retained and one ordinary retry succeeded after the other reader finished. The ten permitted originals all restored, with 11 total invocations. No computation or registry was edited to bypass a check.

The range audit includes original histogram tails, the full −1.005 CV score, all scatter points, full weak-simulation estimates and all post-publication rug observations. The saved density curve remains on its actual computed grid [−4,7]; expanding the rug axis does not extrapolate it. The nested text table is extended additively; earlier strings remain byte-for-byte in value. Source translation, actual renders, sampled signal/timing checks and continuous listening are separate evidence categories.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Kelly and Xiu, *Financial Machine Learning* | 3 (regularisation, the lasso), 4 (PCA, RP-PCA, IPCA), 5 (SDF estimation, KNS) | ch. 6–9 |
| Bali, Engle and Murray, *Empirical Asset Pricing* | 5 (the cross-section, multiple tests), 6 (factor models) | ch. 1–4, 10 |
| Efron, *Large-Scale Inference* | 1–4 (empirical Bayes, false discovery rates) | ch. 2, 4 |
| Cochrane, *Asset Pricing* | 12–13 (regression tests, the SDF with many factors) | ch. 6, 10 |

## Papers, chapter by chapter

* Hook: Cochrane (2011); Chen and Zimmermann (2022).
* ch. 1: Ioannidis (2005); Harvey, Liu and Zhu (2016); Harvey (2017).
* ch. 2: Holm (1979); Benjamini and Hochberg (1995); White (2000); Romano and Wolf (2005); Harvey and Liu (2020).
* ch. 3: Fama and French (2008); Hou, Xue and Zhang (2020); Chen and Zimmermann (2022); Jensen, Kelly and Pedersen
  (2023).
* ch. 4: McLean and Pontiff (2016); Chen and Zimmermann (2020); Chordia, Goyal and Saretto (2020).
* ch. 5: Yan and Zheng (2017); Chen, Lopez-Lira and Zimmermann (working paper, arXiv 2212.10317).
* ch. 6: Kozak, Nagel and Santosh (2018, 2020).
* ch. 7: Tibshirani (1996); Belloni, Chernozhukov and Hansen (2014); Feng, Giglio and Xiu (2020).
* ch. 8: Kan and Zhang (1999); Kleibergen (2009); Giglio and Xiu (2021); Giglio, Xiu and Zhang (test assets and weak
  factors).
* ch. 9: Connor and Korajczyk (1986); Kelly, Pruitt and Su (2019); Lettau and Pelger (2020).
* ch. 10: Lewellen, Nagel and Shanken (2010); Barillas and Shanken (2017, 2018); Fama and French (2018); Bryzgalova,
  Huang and Julliard (2023).
* ch. 11: Novy-Marx and Velikov (2016) on costs.

## Build it

```bash
python -m videos.quant.quant25.compute                        # every item (OSAP data cached by Part 3)
EXPLAINER_TTS=silent python tools/qa_scene.py quant25 KNS      # one chapter, silent, with a contact sheet
python tools/make.py quant25 --cpu-voice -q m                 # English and Chinese, narrated by Kokoro on the CPU
```


---

# 量化金融，从零搭建 — 第25部分：因子动物园

本讲遵循[系列计划](../README.md)与[教学标准](../SYLLABUS.md)，保留原数值方法，同时区分已发表筛选证据、示意推断与真正全新的检验。本轮视觉审查已完成；完整成片听审仍另行待办。计算模块、House算法和全局登记均不改动。十项允许的原计算正常恢复；封存实验在缓存或计数加载器之前即被排除，不使用替代历史策略。本内容用于教育，不构成投资建议。

## 章节与科学限定

1. **两百枚硬币。** 固定模拟展示搜索改变最大值分布。独立标准正态最大值公式与239自由度学生t最大值模拟不同，正向最大值与绝对最大值也不同；平方根对数公式是渐近近似。
2. **数量与门槛。** 邦费罗尼在有效边际p值下允许任意依赖；t > 3是特定模型与研究背景下的结论，不是普遍临界值。固定真实比例与功效算例没有估计发表集合中的真实比例。
3. **多重检验。** 邦费罗尼、霍尔姆控制固定族错误率；BH需要有效零假设标定及独立或适用的正回归依赖，任意正相关并不足够。错误发现率控制期望比例，不控制实现错误数量、组合亏损或融资风险。收益p值使用朴素独立同分布均值t与正态尾概率，其有效性有条件。
4. **重现。** 权重、断点、微盘股、样本和数据版本会改变估计对象。原样本掩码直接使用论文元数据年份，不另加二〇二〇年上限；发表后从下一历年开始，最迟到二〇二〇年十二月，至少二十四个月。发表与方向筛选仍存在，现代重建不是当时版本。
5. **衰减与贝叶斯。** 正态共轭示例假设独立单位噪声及正态先验。零点八三一是相对先验均值偏离的后验斜率，不是保留每项溢价的比例。观测均值比零点三七九与散点斜率零点四二六是不同对象，两者与贝叶斯斜率之差不是因果分解。保留三分之一至二分之一只能作为敏感性情景。
6. **挖掘与同行评审。** 公开研究结果均注明出处与构造。固定边际概率下的期望噪声计数不需要独立；独立影响联合不确定性。历史研究的保留率不能标定新策略未来净收益。
7. **收缩横截面。** 中心化线性核m = 1 − b′(F − μ)均值为一但未必为正；Fb是因子组合收益，不是m。各向同性岭依赖因子单位。154列资产集合按一九七三至二〇二三年的完整观测筛选，再使用截至二〇二〇年的收益。三折连续区块交叉验证用其他折训练，其中包括未来折；惩罚网格使用全窗口协方差，最佳卡帕也用到后段二〇〇一至二〇二〇年。因此后段评价存在超参数信息泄漏，并非独立顺序验证。全窗口规模归一化具有回顾性，分段规模则按训练段确定。
8. **驯服动物园。** 简化双重选择取两个套索集合并集；无截距套索缩放但不去均值，最终横截面回归含截距并报告HC0。它忽略组合误差依赖、协方差估计不确定性与完整论文推断。25个新预测变量对53个旧控制的21/14/5个名义门槛超越是启发式、非嵌套诊断。载荷不显著不能证明精确张成或没有增量价值。
9. **弱因子。** 固定400次模拟含50个资产、480个月，月度价格零点零零五。经典独立测量误差衰减是有条件算例，并非生成贝塔的一般恒等式。三步方法需要广泛性、秩、归一化与识别条件，主成分不会自动恢复所有因子。
10. **主成分。** 风险溢价主成分矩阵为F′F/T + γμμ′，原计算固定γ = 10。负一时为分母T的中心化协方差，特征向量与分母T减一相同而特征值不同。分段继承完整历史与发表筛选；显示十种K，挑选最优点再增加筛选。后段阿尔法在后段本身拟合，并非完全冻结预测。工具主成分仅概念介绍，特征不字面等于协方差。
11. **模型比较。** 共同可交易收益并集、相同矩约定与无约束权重下，较高可达夏普平方留下较小均值方差缺口。这不是普遍模型真理、精确张成或约束投资者支配。十列含预期增长，市场必须纳入且总数最多六个，共382个子集。训练一九六七至一九九三年，后段评价一九九四至二〇二〇年；后段最优名单直接在该段选择。最大夏普平方使用T减一协方差，后段固定组合标准差使用T，有限样本约定不同。回填预期增长不是递归历史版本。
12. **登记与精度。** 真正分离的检验前，冻结代码、资产集合、时钟、缺失值、成本、基准与决策规则。哈希不能让已观察样本变新。稳定低夏普独立同分布近似下，t约等于年化夏普乘年数平方根；三年标准误约零点五八，t等于二需要夏普约一点一五，夏普零点四对应t约零点六九。均为固定算术例，不是封存结果。
13. **House。** 截至本部分既有登记348次，全局23562次；本轮新增均为零，98个受保护文件不变。局部台账不枚举继承的发表搜索，因子组合还缺乏真实交易、融资、抵押、借券与资本约束。多空研究指数不自动等于美元财富。
14. **研究者专题。** BH精确等式要求独立检验和严格均匀的真零假设p值。固定兰布达、未截断斯托里估计量的期望不低于派零，但不是每次实现的上界；截于一可改变期望界。模拟有蒙特卡洛误差。实证设上限派零、自适应BH、核密度与截断局部比值都是有条件诊断，不自动获得有限样本错误率或后验认证，补数求和不是已识别的真实效应数量。
15. **回顾与习题。** 十四点回顾、六道研究台题、十二道完整习题。画面按6/4/2分页连续编号，保留全部观测极值，不把尾部裁到绘图区边界。

## 交易台问题与解答

1. **两百个噪声策略的最佳值。** 保存的独立学生t示例正向最大值均值约二点八，绝对最大值约三；正态渐近式只是近似，依赖与搜索族都重要。
2. **最佳t为二点九。** 独立标准正态假设下，选择后尾概率1 − Φ(2.9)^200约零点三一；事前指定单项则约零点零零一九。必须说明搜索数量与零假设模型。
3. **一百个中选十个。** 声明错误控制目标及有效标定、依赖假设。错误发现率控制期望，不保证已实现错误数量或组合安全；族错误率也适用于一族主张。
4. **微盘股显著性。** 等权与市值权估计不同组合；单个t值不能识别持续溢价。应评估不确定性、流动性、成本与规模。
5. **发表月收益百分之零点八。** 零点三至零点四可作为明确标注的敏感性情景，并非通用标定预测。净实施还要单独评估成本与不确定性。
6. **简化载荷不显著。** 不拒绝不能证明精确张成或没有增量效用；需要功效、弱识别、协方差与选择不确定性、因子依赖及实施分析。

## 习题与解答

1. **正态最大值。** 独立性给出Pr(max Zᵢ ≤ c) = Φ(c)^n；中位数满足Φ(c) = 2^(−1/n)，n = 200时约2.70。这是标准正态最大值中位数，不是学生t模拟均值。
2. **邦费罗尼。** 0.05/212 = 0.00023585，双侧正态临界值Φ⁻¹(1 − 0.05/(2·212))约3.68。有效边际p值及并集界允许任意依赖；有限样本学生t临界值不同。
3. **五个p值。** 邦费罗尼0.01拒绝0.001和0.008，共二个。霍尔姆门槛0.01、0.0125、0.01667、0.025、0.05，在0.03失败前拒绝三个。BH最后交点k = 4，0.03 ≤ 0.04，拒绝四个。
4. **条件贝叶斯。** t = θ + ε，独立单位正态噪声，θ ~ N(4,5)，观测方差6；t = 7的后验均值4 + (5/6)(7 − 4) = 6.5。已筛选集合的拟合模型未必标定未来收益。
5. **岭分解。** 正定对称Σ = Σ_k λ_k q_kq_k′，γ ≥ 0时，(Σ + γI)⁻¹μ = Σ_k(q_k′μ)/(λ_k + γ)q_k = Σ_k[λ_k/(λ_k + γ)][(q_k′μ)/λ_k]q_k。未收缩形式需要正特征值；各向同性惩罚依赖单位。
6. **两个方向。** 原载荷0.002/0.01 = 0.2，0.002/0.0001 = 20；γ = 0.001时为0.1818和1.8182。小特征值方向保留十一分之一，大方向保留十一分之十。这是该先验的收缩结果，不证明其均值虚假。
7. **负一特例。** F′F/T − μμ′ = Σ_t(F_t − μ)(F_t − μ)′/T，等于常用样本协方差的(T − 1)/T倍。特征向量相同，特征值缩放。
8. **经典衰减。** 若β̂ = β + u且u独立加性，结构误差与β、u正交，回归含截距，则plim λ̂ = λ·0.01/(0.01 + 0.04) = 0.2λ。生成因子贝塔和弱因子两步推断不自动符合这些假设。
9. **条件比较。** B的可达夏普平方0.8高于A的0.5。在相同矩、共同可交易收益并集和无约束权重下，缺口SR²(并集) − SR²(模型)小0.3。因子自身可组成共同并集。有限GRS还有模型相关缩放；结论不证明风险解释、精确张成、约束支配或未来赢家。
10. **期望噪声数量。** 标准正态边际下，29000·2Φ̄(2)约1320，29000·2Φ̄(3)约78.3。期望线性不要求各检验独立；依赖改变离散程度和至少一次超越的概率。
11. **BH精确证明。** 假设p值独立且真零假设均匀。R⁽ⁱ⁾为把p_i设零后的拒绝数，仅依赖其余p值。k ≥ 1时，{p_i ≤ qk/m, R = k}等于{p_i ≤ qk/m, R⁽ⁱ⁾ = k}：降低已拒绝p值不改变最终数量；反向把p恢复到不超过第k门槛仍保留该交点且不产生更后交点。独立均匀性给出概率(qk/m)Pr(R⁽ⁱ⁾ = k)。对真零假设及k求和，E[V/max(R,1)] = Σ_i∈H₀Σ_k(1/k)(qk/m)Pr(R⁽ⁱ⁾ = k) = m₀q/m。超均匀有效零假设只给上界，不保证等式。
12. **斯托里及局部尾部。** 固定λ与均匀真零假设下，E#{p > λ} = m₀(1 − λ) + Σ_i∈H₁Pr(p_i > λ) ≥ m₀(1 − λ)，除以m(1 − λ)即得未截断期望界。实现值未必大于派零，截于一可破坏期望不等式。例如m = m₀ = 1、λ = 1/2时，截断估计为1{p > 1/2}，期望1/2小于派零1。正确两组模型f = π₀φ + (1 − π₀)f₁、正尾概率下，Pr(H₀|Z ≥ z) = π₀Φ̄(z)/F̄(z) = ∫_z^∞[π₀φ(u)/f(u)]f(u)du/F̄(z) = E[lfdr(Z)|Z ≥ z]。须使用标准正态零分布与一致正尾；局部率递减时，尾部平均不大于门槛处局部率。任意截断拟合比值不自动继承后验恒等式。

## 数据与复现边界

公开OSAP2024.10的两个原始读取器会完整读取包含截至二〇二三年观测的公开版本；完整历史资产筛选因此使用后续缺失信息。指定法国因子与q公开档案包含截至二〇二五年的数据，随后截取。读取公开档案不同于打开或评分被排除的封存实验；不声称所有二〇二〇年后的公开字节均未读取。

本轮不强制刷新、不新增登记或市场策略试验、不访问封存载荷、不创建替代历史检验。初次动物园恢复遇到并发公开缓存临时文件改名冲突，完整失败保留；另一个读取器完成后，单次正常重试成功。十项原计算共十一轮调用均恢复，算法和登记未为绕过检查而修改。

范围审查包括全部直方图尾部、最低约负一点零零五的交叉验证分数、全部散点、完整弱因子模拟和全部发表后地毯观测。密度曲线仍限于实际计算网格负四至七，不外推。字幕表仅追加；原有字符串值不变。源码翻译、实际渲染、抽样信号与对齐检查，以及完整连续听审分别记录。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part25.md`](../../../docs/qa/quant/part25.md).*
