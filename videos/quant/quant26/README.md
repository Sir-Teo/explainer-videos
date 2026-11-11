# Quant, Built — Part 26: Backtesting Without Fooling Yourself

Part 26 of [Quant, Built](../README.md), following [the syllabus](../SYLLABUS.md). A selected historical return is not a promise of executable future returns. This lecture separates data availability, selection, execution assumptions, uncertainty, validation and monitoring. Educational methods, not investment advice.

## Evidence and data boundary

The presentation uses fourteen restored original calculations from unchanged `compute.py` and unchanged House algorithms. Sixteen normal original invocations produced fourteen successes and two source-verification failures, with no retries, force, refresh, registry changes or additional market trials. The existing cumulative registered count through Part 26 is **10,348**; the global count is **23,562**. The pre-Part-26 snapshot is **348**. All 98 protected files retain their baseline hashes.

The original `survivor` calculation stops at the SEC ticker-file hash check. The original `engine` calculation stops at the Yahoo EEM extract hash check, before the later AAPL and SPY readers. Neither original empirical result is available for this review. The current workspace files fail the frozen manifest hashes; recovery found no matching workspace copy or git version. Their original code, failure logs and mismatching public inputs are preserved in the local QA archive. We do not refresh the manifest, bypass verification, fabricate caches or substitute a historical strategy. The Survivorship and Engine chapters instead use explicitly fabricated, fixed arithmetic examples. Current CIK membership would not, by itself, measure literal corporate survival.

`common.load` rejects `envelope`, `survivor` and `engine` prefixes before the cache/counting loader. The Envelope class is a conceptual registration and evaluation-accounting chapter; it does not read the sealed experiment cache, register anything, or open its market payload. Build commands below render the presentation; do not run all compute items, use force/refresh or open the envelope.

The access audit lists **32 possible pre-existing public manifest keys**, not 32 confirmed reads: public OSAP panels, French data through 2020, Philadelphia monthly vintages, Cboe PUT, and the SEC/Yahoo readers reachable from the original code. Failed early readers prevent some downstream accesses. The public OSAP archive contains later-published/backfilled vintages before the research-date cuts. Reading that public archive is distinct from a sealed strategy opening, and does not make its older observations a timestamp-complete point-in-time panel.

## Nineteen chapters

1. **Hook.** The earlier winner among 10,000 configurations has Sharpe 1.67 through 1986 and 0.02 in 1987–2020. Gross excess-cash compounding and a later decline do not prove clean data, tradeability or a unique cause.
2. **Look-ahead.** A deliberate same-day index error changes the 200-day rule's Sharpe from 0.22 to 1.31; the five-day version reaches 8.75. GDP revisions compare 216 quarters, 1966–2019, with December 2020 vintages: mean absolute revision 1.54 points, 7.4% sign changes. Monthly vintage availability is not a complete release-timestamp replay.
3. **Survivorship.** The blocked SEC original is withheld. Four invented returns −20%, −10%, +10%, +20% average zero; retaining only the positive pair gives +15%. A fixed +10%, then −50% sequence compounds to −45%. Selection need not always bias upward; missing and delisting returns require provider-specific definitions.
4. **Selection.** Saved Student-t noise simulations give mean best annual Sharpe 0.69, 1.12, 1.46, 1.73 for 10, 100, 1,000, 10,000 estimates over five years. The independent-normal maximum law is exact for that stated model; the Gumbel mean formula is an approximation.
5. **Engine.** The blocked Yahoo original is withheld. Invented quotes 100 at decision close, 102 next open, 101 next close separate decision, assumed fill and mark. One share loses 1 before costs; with 1,000 capital and a 0.20 fee, ending wealth is 998.80. Fixed split and dividend examples show accounting identities. A protected loop excerpt explains event ordering without certifying external data or realistic fills.
6. **Sharpe error.** IID delta-method and moment formulas; stationary arithmetic aggregation under autocorrelation. Market ratio 0.44, estimated standard error 0.10; PUT ratio 0.45, error 0.27 or 0.30 with moments. These errors omit serial dependence. Fixed two-standard-error planning approximations are not power guarantees.
7. **Counter.** Existing registrations, the 348 pre-part snapshot, and 10,348 through this part. Approximate mean maxima are not significance cutoffs. Registered counts omit informal choices; correlations do not identify a universal independent-search count.
8. **Technical rules.** A seeded sample of configurations from four families, inspired by the literature rather than an exact replication. Gross excess-cash returns, two research eras and selected-family comparisons. Stale prices are a plausible concern, not an identified causal decomposition.
9. **Deflated Sharpe.** PSR/DSR normal-reference confidence scores, not posterior probabilities or exact selection-adjusted tests. A participation ratio estimated from 1,500 sampled return correlations and scaled to 10,000 gives heuristic effective counts around 176 and 155. Later-era selection is distinct from testing the earlier winner.
10. **PBO.** 12,870 overlapping half-sample splits, a precise half-tie rank convention and PBO 0.00/0.43. Zero does not mean rank one in every split or no overfitting. The saved logit histogram has a finite window; omitted tails are counted explicitly. All 800 saved scatter pairs are shown without clipping.
11. **Cross-validation.** Full-sample feature scaling leaks into every original score. Blocked/purged folds can use future training; walk-forward training labels cross the boundary before maturity. A 20-day embargo does not remove every 60-day feature overlap. Hit rate uses the training-label median. These are leakage diagnostics, not clean live forecast estimates.
12. **Reality checks.** Cash-relative differential means; 500 stationary-bootstrap draws with mean block length 10; simplified RC, SPA and step-down implementations. Zero means 0/500 exceedances. Sample-SD studentisers do not estimate serial long-run variance; approximate inference needs bootstrap assumptions. Nonrejection is not equivalence.
13. **Monitoring.** Retrospective clipped-increment diagnostics on published-selected predictors. A valid nonnegative betting supermartingale requires a precommitted/predictable process with conditional clipped mean at most zero. A raw-return mean claim does not imply that null after clipping. e-BH requires valid unit-expectation-bounded e-values under true nulls; the saved counts alone do not establish those conditions.
14. **Planted alpha.** Forty simulated markets per edge, 1,000 strategies, ten nonzero means. Saved discovery and DSR-score frequencies illustrate power/error tradeoffs under this simulation; they prove no universal impossibility or zero error.
15. **Funding.** Fixed Gaussian simulated careers and an assumed arithmetic capital ramp. True Sharpe 1 is below the tested full target 1.5: its 3.8% stopping frequency is not a full-null false-alarm rate. True-zero stopping is 61.7%, median month 43 among stopped careers; half-target stopping is 9.6%. No calibrated execution costs or live capacity are modelled.
16. **Registration and evaluation accounting.** Conceptual protocol, an existing metadata count, and fixed precision arithmetic. No sealed experiment opening or replacement historical performance test.
17. **House protocol.** Available-time inputs, known exclusions, trial accounting, training-only transformations, mature labels, costs and a fresh evaluation design. Protected algorithms remain unchanged.
18. **Research: inference on a winner.** Known-Gaussian selection bounds versus estimated historical Sharpe proxies. Exact ideal inversion is separate from finite ±60-standard-error brackets, an 801-point hybrid grid, simulated critical values and a 400-draw IID Gaussian multiplier calculation. The later conditional lower endpoint is beyond its stored −13.47 solver floor; that floor is not the exact endpoint. Historical differences do not isolate regime change from selection.
19. **Outro.** Qualified recap, six desk questions, twelve problems in continuous 6/4/2 pages, references and next-part link.

## Six desk questions and answers

1. **Sharpe 3: what could be wrong?** Trace available-time inputs, missing firms, every search choice, signal/fill timing, costs, borrow and corporate actions. Inspect dependence, precision, validation and structural change. An event loop alone cannot validate external inputs or executable prices.
2. **400 settings, ten years, best Sharpe 1.2?** The independent-normal approximate mean maximum is about 0.94. Exceeding a mean is not rejection at a stated level. Dependence, trial spread and the omitted research path matter; DSR is a sensitivity diagnostic.
3. **Three years, annualised Sharpe 2, lag-one correlation 0.4?** If every higher autocorrelation is zero, stationary arithmetic aggregation maps 2 to about 1.52. Those summaries do not identify a valid confidence interval; additional moments and dependence estimation are needed.
4. **200 trades, 4 bp gross, 3 bp costs?** The margin is 1 bp per trade. A 2% annual arithmetic margin additionally assumes 200 full-capital turnovers and no other costs. A 1 bp cost error erases it; trade size and cost calibration matter.
5. **Three-year default labels, five random folds of firm-years?** Respect label maturity and overlap, fit transformations only within available training data, and evaluate chronologically for future prediction. Group separation is needed when the target is new-firm generalisation. Choose gaps from actual label/feature spans.
6. **E-process at 12, move threshold 20 to 10?** The 5% bound at 20 is not retained. For a valid e-process starting at one, Ville gives a 10% crossing bound at ten. New monitors and restarts need valid conditional nulls, predictable choices and an overall error budget.

## Twelve worked problems: 6 foundations, 4 graduate, 2 qualifying

These are explicitly fixed mathematical examples, not new market trials.

1. **IID normal Sharpe variance.** For g(μ,σ)=μ/σ, gradient (1/σ,−SR/σ). Under normal IID observations, asymptotic Var(μ̂)=σ²/T, Var(σ̂)=σ²/(2T), Cov=0. The delta method gives Var(SR̂)≈(1+SR²/2)/T. This is an asymptotic per-period result, not an exact small-sample or serially dependent variance.
2. **Normal maximum.** Independence gives P(max Zᵢ≤c)=∏P(Zᵢ≤c)=Φ(c)^N. At N=100 the median is Φ⁻¹(2^(−1/100))≈2.46204.
3. **100 noise estimates, five years.** Let A_N=(1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne)). The normal/Gumbel mean approximation gives A_100/√5≈1.13172 annual Sharpe. This is not an exact Student-t simulation mean or significance threshold.
4. **N=1,000, target Sharpe 1.** Equate the approximate null mean maximum to one: Y≈A_1000²≈10.5958 years. This mean-hurdle length does not specify confidence or detection power.
5. **PSR score.** With monthly SR̂=0.1,T=60,skew=−1,kurtosis=6, z=0.1√59/√(1−(−1)0.1+(6−1)0.1²/4)≈0.72824. Φ(z)≈0.76677. This normal-reference confidence score is not a Bayesian posterior or an exact selection test.
6. **Lo aggregation.** With ρ₁=0.3 and all other lags zero, η(12)=12/√(12+2·11·0.3)≈2.78243. Naive √12 scaling is about 24.50% larger. The assumptions concern stationary arithmetic-sum moments, not a universal compounded-return identity.
7. **CSCV counts.** Choose 8 of 16 blocks: C(16,8)=12,870. A specified block is selected in C(15,7)=6,435 splits. The splits share observations and are not independent experiments.
8. **Inclusive purging convention.** There are 5,000 observations, five contiguous folds, training label spans [i,i+20], and 20 additional embargo indices after the test label span. For an interior test fold [a,b] of 1,000 indices, its union of labels is [a,b+20]. Twenty earlier training spans intersect at the left; twenty later indices overlap the right; another twenty are embargoed. Thus 60 training observations are removed and 3,940 of the initial 4,000 remain. End folds have different counts. A different interval convention changes the answer.
9. **Stationary bootstrap.** With restart probability p=0.1, geometric block length on {1,2,…} has E[L]=1/p=10 and P(L≥20)=(1−p)^19≈0.135085.
10. **Repeated looks.** A nonnegative supermartingale E₀=1 under the actual conditional null satisfies P(sup_t E_t≥20)≤0.05, including 120 looks. For 120 independent 5% tests, P(any rejection)=1−0.95^120≈0.997878. Nested monthly tests are dependent, so that independent-test benchmark is not their universal error rate. Clipped raw-return monitors first need a justified clipped-increment null.
11. **General Gaussian winner bounds.** X∼N(μ,Σ), Σ_jj>0, and known covariance. Set ρ_k=Σ_kj/Σ_jj and Z_k=X_k−ρ_kX_j; Gaussian projection makes Z independent of X_j. The event X_j≥X_k is Z_k≤a_kX_j with a_k=1−ρ_k. For a_k>0 it gives X_j≥Z_k/a_k; for a_k<0 it gives X_j≤Z_k/a_k; for a_k=0 it requires Z_k≤0. Combine all lower/upper bounds with feasibility. For equal variances and nondegenerate correlations below one, the upper bound is infinite. Conditional on feasible Z and winner j, the known-model distribution is the corresponding truncated normal. Exact inversion gives conditional coverage; finite solver caps, grids and estimated covariances do not inherit exact numerical guarantees.
12. **Naive interval for an independent null winner.** For N independent standard normals, a symmetric interval max Zᵢ±1.96 covers the selected true mean zero iff max Zᵢ∈[−1.96,1.96]. Coverage is Φ(1.96)^N−Φ(−1.96)^N. It is approximately 95.00% for N=2 and 28.20% for N=50. Positive winner bias does not imply strict undercoverage for every N or covariance structure; the two-estimate case is a useful counterexample.

## References and textbook map

- Brown, Goetzmann, Ibbotson and Ross (1992), *Survivorship bias in performance studies*; Shumway (1997), *The delisting bias in CRSP data*; Shumway and Warther (1999), Nasdaq delisting returns. Missingness and population definitions, not a substitute for blocked SEC outputs.
- Brock, Lakonishok and LeBaron (1992); Sullivan, Timmermann and White (1999); White (2000); Politis and Romano (1994); Hansen (2005); Romano and Wolf (2005). Trading-rule selection and bootstrap inference under stated assumptions.
- Lo (2002), *The statistics of Sharpe ratios*; Mertens (2002), *Variance of the IID estimator in Lo (2002)*; Getmansky, Lo and Makarov (2004). Estimation, finite moments and serial correlation.
- Bailey and López de Prado (2014), deflated Sharpe ratio; Bailey, Borwein, López de Prado and Zhu (2014; 2017), backtest length and PBO. Separate heuristic mean hurdles from exact inference.
- López de Prado (2018), *Advances in Financial Machine Learning*, chapters 1 and 7; Arnott, Harvey and Markowitz (2019), *A backtesting protocol in the era of machine learning*. Evaluation design and implementation.
- Ville (1939); Shafer and Vovk (2019); Wang and Ramdas (2022), e-BH. Betting evidence needs its actual conditional null; valid e-values precede multiplicity control.
- Andrews, Kitagawa and McCloskey (2024), *Inference on winners*, QJE 139. Known-model theorem versus the finite numerical and historical plug-in examples here.
- Leinweber (2007), *Stupid data miner tricks*. Historical illustration of search, not an empirical result generated by this review.

## Build and QA

Activate the repository environment first. Cached presentation loads are guarded; the two unavailable originals and sealed envelope are not presentation dependencies. For example:

```bash
source /workspace/environment/activate.sh
EXPLAINER_TTS=silent EXPLAINER_LANG=en manim -ql videos/quant/quant26/s03_survivor.py Survivor
EXPLAINER_TTS=silent EXPLAINER_LANG=zh manim -ql videos/quant/quant26/s05_engine.py Engine
python tools/zh_lines.py quant26 --todo
```

The scientific, bilingual construction and rendered visual review is complete on the source pinned below. Full continuous production-voice listening and pronunciation review remain separately pending.

# 中文：第26讲，不自欺的回测

本讲保留19章，区分数据可用时间、研究选择、执行假设、估计误差、验证与监控。教育材料，不构成投资建议。

原始计算共正常调用16次，14项成功；SEC股票代码表和Yahoo EEM数据未通过冻结哈希校验，相关历史结果不展示。两章改用明确虚构的固定算术，不伪造缓存、不刷新清单、不绕过校验、不另做历史策略测试。原始代码、失败日志和不匹配的公开输入均已保存。`common.load`在缓存及计数加载器之前拒绝这两项及封存实验。封存章只讲登记、精度和评估记账，不打开市场载荷。原有累计计数为本讲之前348、截至本讲10,348、全局23,562；98个保护文件保持原哈希。

访问审计列出32个原代码可能访问的既有公开数据键，并非声称全部实际读取。公开OSAP档案含事后发表和回填版本，按研究日期切片不等于完整时点数据库，也不等于打开封存策略实验。GDP月度版本不能代替精确发布日期和日内执行回放。

章节顺序：开场；前视；生存者选择的固定算术；多次选择；执行时钟的固定算术；夏普估计误差；试验计数；技术规则；DSR；PBO；交叉验证；现实检验；监控；植入信号；资金爬坡；登记与评估记账；House协议；胜者推断；总结。十四项成功缓存的结果及模型限制见上文英文逐章说明。

核心限制：所有原交叉验证分数都用了全样本标准化；分块与清除设计仍可能用未来训练数据，前向设计的训练标签也未完全成熟。PSR和DSR是近似置信分数，不是后验概率或精确选择校正检验。PBO拆分高度重叠，零值不证明没有过拟合；有限直方图区间外的数量明确列出。500次自助抽样中的零超越不等于真实概率为零，原样本标准差不估计序列长期方差。

监控的有效条件是实际截断增量在给定过去下的条件均值不大于零；原始收益均值限制不能自动推出此条件。e-BH先要求真零假设下有效的e值。资金模拟中真实夏普1低于完整目标1.5，所以3.8%的停止率不能称为该零假设下的误报率。胜者推断的已知高斯定理与历史插件近似必须分开：原算法根搜索限制为观测值上下60个标准误，混合区间用801点网格。后来胜者的−13.47是搜索下限，不是精确区间端点。

## 六道面试题与答案

1. **回测夏普3，哪里可能出错？** 查数据可用时点、消失公司、研究选择、信号与成交时间、成本、融券、公司行动、相关性、估计误差、验证和结构变化。事件循环本身不能证明外部数据无泄漏或成交价可得。
2. **400组参数、十年、最好夏普1.2？** 独立正态模型的近似零技能最大值均值约0.94。超过均值不是给定水平的拒绝；相关性、试验间离散度和未记录的研究路径都重要。DSR是近似敏感性诊断。
3. **三年、年化夏普2、一阶自相关0.4？** 若其他自相关全为零，平稳算术聚合的缩放修正约为1.52。仅这些统计量不能确定有效置信区间，还需更高阶矩和依赖估计。
4. **每年200笔、毛利4基点、成本3基点？** 每笔净余1基点。年化算术2%还假定每笔用满本金、全年200次完整周转且无其他成本。成本误差1基点就能抹平优势。
5. **三年违约标签，企业年度记录随机五折？** 标签须成熟，清除实际重叠区间，预处理只能用当时可得训练数据。预测未来用时间设计，推广到新企业还需按企业隔离；间隔由实际特征和标签窗口确定。
6. **e过程到12，把阈值20改成10？** 不能保留5%界限。有效非负超鞅从1开始时，Ville在阈值10给10%的穿越概率上界。重启还需有效条件零假设、可预测选择和总体错误预算。

## 十二道完整解答：6道基础、4道研究生、2道资格题

均为固定数学例题，不产生市场试验。

1. **夏普方差。** g(μ,σ)=μ/σ，梯度为(1/σ,−SR/σ)。独立正态下，均值估计方差σ²/T、标准差估计渐近方差σ²/(2T)，两者协方差为零。Delta法得Var(SR̂)≈(1+SR²/2)/T。这是每期渐近式，不是小样本或序列相关下的精确方差。
2. **正态最大值。** 独立性给P(max Zᵢ≤c)=Φ(c)^N。N=100时中位数Φ⁻¹(2^(−1/100))≈2.46204。
3. **100个噪声估计、五年。** 令A_N=(1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne))。正态极值均值近似为A_100/√5≈1.13172。这不是Student-t模拟的精确均值或显著性阈值。
4. **1,000次、目标夏普1。** 把近似零技能最大值均值设为1，得Y≈A_1000²≈10.5958年。这个均值门槛不指定置信水平或检验功效。
5. **PSR。** 月夏普0.1、T=60、偏度−1、峰度6，z=0.1√59/√(1+0.1+5·0.1²/4)≈0.72824，Φ(z)≈0.76677。这是正态参考置信分数，不是贝叶斯后验或精确选择检验。
6. **Lo缩放。** ρ₁=0.3，其他滞后为零，η(12)=12/√(12+2·11·0.3)≈2.78243。朴素√12缩放高估约24.50%。条件是平稳算术和的矩，不是普遍的复利恒等式。
7. **CSCV计数。** C(16,8)=12,870；指定块入选的拆分有C(15,7)=6,435。拆分共享观测，不是独立实验。
8. **含端点清除。** 5,000个观测分五个连续折，标签[i,i+20]含端点，测试标签范围之后再禁运20个索引。内部测试折[a,b]含1,000个观测，标签并集为[a,b+20]。左侧20个训练标签相交，右侧20个索引相交，另禁运20个，共删除60个，原4,000个训练观测剩3,940。边缘折及其他区间约定答案不同。
9. **平稳自助抽样。** 重启概率p=0.1时，块长在正整数上服从几何分布，E[L]=10，P(L≥20)=0.9^19≈0.135085。
10. **反复查看。** 在实际条件零假设下，E₀=1的非负超鞅满足P(sup E_t≥20)≤0.05，120次查看也适用。120个独立5%检验至少拒绝一次的概率为1−0.95^120≈0.997878。嵌套月度检验相关，不能直接套独立结果。截断收益监控必须先证明截断增量的条件均值限制。
11. **一般高斯胜者。** 已知Σ且Σ_jj>0，令ρ_k=Σ_kj/Σ_jj、Z_k=X_k−ρ_kX_j；高斯投影使Z与X_j独立。X_j≥X_k等价于Z_k≤a_kX_j，其中a_k=1−ρ_k。a_k正时给下界，负时给上界，零时要求Z_k≤0。合并全部界限与可行性；等方差且非退化相关小于1时上界无穷。给定可行残差和胜者，X_j服从对应截断正态。精确反演的定理不能直接赋予有限搜索、网格或估计协方差同样的精确数值保证。
12. **独立零均值胜者的朴素区间。** max Zᵢ±1.96覆盖零，当且仅当最大值位于[−1.96,1.96]。覆盖率Φ(1.96)^N−Φ(−1.96)^N；N=2约95.00%，N=50约28.20%。胜者向上偏不意味着所有N和协方差结构下都严格欠覆盖。

参考文献和教材对应关系见英文列表。科学源稿、双语构造和实际渲染视觉审查已完成，证据索引见下文；完整生产语音听审和发音检查仍另行待办。

## Current visual review

Visual pass complete on `quantitative-finance`: 38 bilingual endpoint sheets, 19 English forty-frame motion sheets and 20 focused native frames actually inspected on source `e2f29a766e3c5ca3a67667aff286f5f8834db679`. The chaptered silent timing preview runs 70:23, with 19 chapters and English subtitles. Eleven CPU speech reports cover 84 sampled lines; the actual narrated opening runs 223.600 seconds. Signal and image checks do not certify pronunciation or continuous production listening, which remain pending. [Artifact-bound evidence](../../../docs/qa/quant26-polish-evidence.json).

## 当前视觉审阅

本轮已实际检查38张双语旁白节点画面表、19张英文四十帧动画表及20张重点原尺寸画面。分章静音时序预览为70:23，含19章和英文字幕。十一份CPU语音报告覆盖84个抽样句段，并核验实际配音开场。信号与画面检查不替代发音或完整生产成片连续听审，后者仍为独立待办。两项原历史计算未通过冻结数据校验，不展示不可用输出；固定算术例子与原历史结果明确区分。
