

# Quant, Built · Part 30: Portfolio Construction

Scientific presentation revision, bilingual construction and actual rendered visual review are complete. Fourteen audited ordinary originals restored without retries; the strategy experiment remains excluded before counted/cache access. Full production listening remains separately pending.

This part opens Act V and asks how estimates become holdings. Sixteen chapters cover error maximisation, equal weights, random-matrix benchmarks, covariance shrinkage, constraints, Black–Litterman, ERC and HRP, robust optimisation, CVaR, growth, entropy pooling, end-to-end learning, evaluation protocol, the House, a research proof and worked problems. This is educational material, not an investment recommendation.

## Data, computations and interpretation

The unchanged originals use Kenneth French's 49 value-weighted industry portfolios and monthly risk-free rates through December 2020, daily industry returns through 2020 for spectra, and firm-count/mean-size blocks for industry-cap proxies. The archived files are parsed before their through-date masks. Frozen subset hashes verify those subsets; they do not establish historical publication timing, complete point-in-time membership or attainable execution. Simulations stipulate the full 1970–2020 research sample moments as a fixed Gaussian population; they do not measure historical future delivery.

All `compute.py` files, House routines and three registries remain unchanged. Permitted ordinary items are `universe`, `michaud`, `rolling`, `spectrum`, `shrink`, `constraints`, `bl`, `riskparity`, `cvar`, `growth`, `views`, `e2e`, `theory`, `factor`. The `envelope` original and its cache/payload are excluded. No force, refresh, new market trial, registration, opening or strategy scoring is performed. Existing metadata is **23,480 through Part 29, 23,525 through Part 30, 23,562 globally**; the increment 45 is bookkeeping, not independent tests.

The presentation distinguishes these details of the saved algorithms:

- Rolling returns are monthly excess returns. All Chapter 2 `pred_vol` values evaluate weights using the trailing **sample covariance**, including weights selected with shrinkage. They are not each estimator's own covariance forecast. The research chapter's shrinkage comparison instead uses its own fitted covariance.
- The rolling rule keyed “inverse volatility” actually uses inverse **variance**. The standalone risk-parity snapshot uses inverse standard deviation. Cache identifiers are retained; these are distinct rules.
- Tangency weights are the inverse-covariance mean direction normalised by its weight sum. A negative denominator reverses its positive-Sharpe orientation; near-zero denominators can produce extreme gross exposures. This saved rule is not a universally well-behaved maximum-positive-Sharpe allocation.
- Turnover is half the absolute change in target weights, excluding drifted holdings. Costs subtract average chosen charges from mean returns and retain gross volatility. This is a sensitivity proxy, with financing, borrow, slippage and impact omitted. Maintaining a fixed 1/N target can require trades despite zero target-weight changes.
- Sample covariance and nonlinear shrinkage use divisor T−1; the local linear shrinkage routines use demeaned divisor T moments. Fixed-target unbiased-S intensity algebra does not transfer unchanged to a target estimated from S. The spectral oracle minimises Frobenius loss within sample eigenvectors, not portfolio loss. Sorted population eigenvalues are not the same directional objects.
- MP support is an asymptotic null benchmark. In-bulk eigenvalues can contain weak structure; outliers need economic interpretation. The daily original zero-fills missing returns. Clipping preserves trace before diagonal renormalisation, which can alter eigenvalues. Correlation heatmaps retain negative entries.
- Jagannathan–Ma is an exact adjusted quadratic identity on the unit-budget affine set. Full-space positive definiteness of the adjusted matrix is unnecessary, and future performance improvement is not guaranteed. Binding multipliers do not simply identify every asset that the original unconstrained optimum shorted.
- Black–Litterman estimates delta from sample moments and uses a specified Gaussian prior/view model. Its view-error multiplier is not a confidence probability. The numerical example uses unchanged covariance; predictive covariance adds posterior mean uncertainty and can change weights even when a view agrees with the prior mean. Unconstrained risky demands need not sum to one.
- ERC equalises fitted variance-contribution shares. HRP uses a sample-dependent single-linkage order and inverse-variance cluster proxies; it is not generally ERC or GMV and does not isolate estimation errors across clusters.
- Expected shortfall averages the worst probability mass, taking a fraction of quantile atoms when needed. The LP uses the exact scenario objective. The score helper uses an interpolated quantile and positive-part formula; finite discrete conventions can differ.
- Kelly's quadratic log-growth expression is exact in the specified diffusion and approximate for discrete returns. Historical fitted leverage and the scalar fractional-Kelly calculation do not identify future optimal exposure or a universal half-Kelly prescription. Discrete solvency and financing need separate modelling.
- Cover's continuous-uniform theorem differs from the saved uniform mixture of 201 grid portfolios. The grid best/mixture wealth ratio is at most 201, while the two-asset continuous bound is n+1. A fixed grid does not certify its continuous hindsight optimum. The monthly industry-cap diversity illustration is not a verification of continuous-time relative arbitrage after costs.
- Entropy effective scenarios measure probability concentration, not independent observations. The market stress fixes a second moment about the **prior** mean; its displayed root is not generally posterior standard deviation, since the posterior mean is not constrained to stay fixed. Arbitrary correlations and ranks need a suitable feasible formulation.
- The original end-to-end demonstration scales features using **both training and validation** before its 1975–2005/2006–2020 split, leaking validation moments. Validation is repeatedly inspected. Logged training scores are pre-update and validation scores post-update; final tables use final weights. Only one seed and score histories are saved, without intermediate weight checkpoints. The two-step comparator clips an inverse-covariance direction positive and renormalises; it is not the exact long-only MV solver. These are retrospective diagnostics, with no new fit to seek a better result.

All optimizer-cloud coordinates, including negative model means and high volatility, remain visible. Spectrum and return histograms do not fold out-of-range values into boundary bins. Research histogram heights are counts/1000. The displayed T=120 histograms retain all 1,000 counts each. The saved T=60 out-risk bins 0–6 contain 664 counts, and T=80 contain 999; those other cached histograms lose tail locations. Their omitted counts are disclosed without inventing values or rerunning the simulation.

## Evaluation protocol and fixed arithmetic

Freeze the entire information and trading procedure: data vintage, availability, preprocessing, windows, hyperparameters, solver, constraints, stopping, benchmarks and reporting. Specify drifted holdings, cash, fills, financing, borrow and costs. Use paired comparisons and inference appropriate to dependence and selection. A wide interval does not establish equivalence; one fresh period alone does not cure leakage or low power. No sealed strategy verdict is supplied.

Two chosen uncorrelated annual volatilities 10% and 20% give GMV weights(.8,.2) and volatility 8.944%; ERC weights(2/3,1/3) give 9.428%; equal money gives 11.180%. These are fixed covariance calculations, with no historical assets or return comparison.

A separate fixed one-period toy starts with half a dollar in each asset and simple returns(10%,0). Pretrade values become(.55,.50), wealth 1.05 and weights(11/21,10/21). Returning to equal weights **before fees** sells .025 and buys .025. The target has not changed, but gross trading is .05 initial dollars. At a chosen 5 bp per dollar traded, the fee is.05×.0005=.000025 initial dollars, or**0.25 bp of initial wealth**. Fees are paid separately; this is not a self-financing post-fee rebalance or a complete net-return model.

## Research: exact Gaussian sampling laws

Fix IID Gaussian returns with positive-definite covarianceΣ. There are K assets and T observations, n=T−1, and S is the demeaned divisor-n sample covariance. Require n ≥ K for full rank. Unit-budget GMV is unrestricted apart from its budget. Write v*=1/(1'Σ⁻¹1), v_in=1/(1'S⁻¹1) and v_out=w_hat'Σ w_hat. For fixed nonzeroa and W~W ishart_K(n,Σ),

$$\frac{a'\Sigma^{-1}a}{a'W^{-1}a}\sim\chi^2_{n-K+1},\qquad \frac{v_{in}}{v_*}\sim\frac{\chi^2_{n-K+1}}n.$$

For K ≥ 2,

$$\frac{v_{out}}{v_*}\sim1+\frac{K-1}{n-K+2}F_{K-1,n-K+2},\qquad E\frac{v_{out}}{v_*}=\frac{n-1}{n-K}\quad(n>K).$$

When K = 1, the out-risk ratio is identically one. Downward bias of the report is an **ensemble expectation**, not a statement that every draw understates risk. The chi-square upper tail is unbounded. Under K,T→∞ and K/T→γ<1, the in/out ratios concentrate at 1−γ and 1/(1−γ); their random ratio tends to 1/(1−γ)². Extensions require explicit moment, dependence and spectral conditions.

Multiplyingv_in by n(n−1)/[(n−K+1)(n−K)] is ensemble-unbiased for E[v_out] under this fixed Gaussian model. It is not a conditional forecast guarantee for the fitted portfolio, nor E[v_out/v_in]. Research-period next-year variance ratios are descriptive ratios of averages under changing conditions, not direct measurements of the fixed population law.

## Six desk checks

1. **Flattering estimates:** an objective can select input errors. Specify objective, normalisation, loss, constraints and evaluation rather than infer one universal source of failure.
2. **49 assets,60 months,3%reported volatility:** no true volatility follows from those facts alone. Gaussian ratios are benchmarks; audit assumptions, timing and independent risk measurement.
3. **Long-only improves:** the adjusted quadratic identity explains a possible regularizer, not a guaranteed future benefit or causal attribution.
4. **No-view BL:** posterior mean staysΠ; unchangedΣ recovers benchmark risky demand, while predictive(1+τ)Σ scales it by 1/(1+τ), absent other constraints.
5. **Estimated Kelly:** full or half Kelly is not a universal recommendation. The fraction needs true strength, known variance and specified estimation/solvency assumptions.
6. **Fixed 1/N:** relative returns drift holdings. Actual rebalance trades depend on pretrade weights and fee/cash conventions even when targets do not change.

## Problems 1–6: complete solutions

**1. GMV.** For uncorrelated variances.01 and.04, minimise.01 w²+.04(1−w)². Its derivative.02 w−.08(1−w)=0 givesw₁=.8,w₂=.2. Variance=.0064+.0016=.008, volatility√.008=.0894427. These are known covariance unit-budget weights.

**2. ERC.** Equal variance contributions require(w₁σ₁)²=(w₂σ₂)². Positive weights givew₁/w₂=σ₂/σ₁=2, hence(2/3,1/3). Variance=2(.1×2/3)²=.00888889 and volatility.0942809. Equal weights have variance(.01+.04)/4=.0125 and volatility.111803. Different objectives produce different weights.

**3. MP support.** q=49/60=.816667,√q=.903696; edges(1±√q)²=.00927444 and 3.62405889. The reference assumes the specified independent unit-variance high-dimensional null. These finite substituted edges are not confidence limits or proof that modes in the band lack economic signal.

**4. Intensity.** Let A=E||S−Σ||²_Fand B=||F−Σ||²_F, with fixed F and E[S]=Σ. The cross term vanishes, so risk(δ)=δ²B+(1−δ)²A. Differentiation givesδ*=A/(A+B)=E||S−Σ||²/E||S−F||²; restrict it to[0,1], with allδ equivalent if A+B=0. If F is estimated from S, cross-covariance terms need not vanish, so this fixed-target derivation does not supply the fitted-target optimum.

**5. BL.** With no informative views, mean posterior isΠ=δΣ w_m and mean-uncertainty covariance M=τΣ. Using unchangedΣ gives risky demandΣ⁻¹Π/δ=w_m. Using predictiveΣ+M givesw_m/(1+τ). Other budgets, long-only constraints or rescaling define different allocation problems. Setting P=0 with positive-definiteΩhas this no-information limit; a singular defaultΩmust not be blindly inverted.

**6. Kelly.** In the known-parameter diffusion, f*=.06/.16²=2.34375. Excess growth is fμ−f²σ²/2. Atf=2 f*, it is 2μ²/σ²−2μ²/σ²=0, so total growth equals the risk-free rate in this model. This is not a discrete-path or solvency guarantee.

## Problems 7–10: complete solutions

**7. Two mixture bounds.** For positive gross returns, a frictionless continuous-uniform two-asset mixture satisfiesbest_continuous/mixture≤n+1, hence the log growth gap≤log(n+1)/n→0. For M fixed portfolios with equal initial capital, mixture wealth=(Σ_j S_j)/M≥max_j S_j/M, givingbest_grid/mixture≤M and log gap≤log M/n. The second competes only with its grid. A fixed grid does not approximate every continuous optimum with a certified error; neither theorem competes with arbitrary dynamic foresight strategies or includes costs.

**8. Tail mass.** At 80%, worst 20%is exactly the loss 10, giving ES=10. At 60%, worst 40%is losses 5 and 10, giving ES=7.5. Equivalently minimiseα+E[(L−α)⁺]/(1−β); quantile atoms are included only as much as necessary. Simply averaging every observation at or above a chosen quantile can use too much mass.

**9. Entropy.** q₁+q₂=1 and−.1 q₁+.1 q₂=.05 giveq₁=.25,q₂=.75. This is the only feasible probability vector, so it also minimises relative entropy to the positive prior. No Gaussian assumption is needed; support is fixed to the two supplied scenarios.

**10. Ratios.** K = 100,T=250,n=249 give E[v_in/v*]=150/249=.6024096 and E[v_out/v*]=248/149=1.6644295. Their ratio is(248/149)/(150/249), about 2.7630. The high-dimensional reference atγ=.4 is 1/.6²=2.77778. Neither is a known ratio for one fit. In the Gaussian model the report's Schur residual is independent of the regression coefficients determining out-risk, so when n > K+1 the expected random ratio is[(n−1)/(n−K)]×[n/(n−K−1)], a different quantity.

## Problems 11–12: qualifying solutions

**11. Sampling laws and correction.** Rotate a fixed nonzeroa into the first coordinate, transformingΣ and Wtogether. Partition W. Block inversion gives(W⁻¹)₁₁=1/s, where s=W₁₁−W₁₂W₂₂⁻¹W₂₁. View W as the cross-product ofn Gaussian observations. Regressing the first column on the other K−1 leavesn−K+1 residual degrees of freedom, so s/σ₁₁·₂~χ²_{n−K+1}. Since(Σ⁻¹)₁₁=1/σ₁₁·₂, this proves the inverse-quadratic lemma. Takinga=1 and W=n S gives the reported-risk law and expectation(n−K+1)/n.

For out-risk, whiten and rotate the transformed budget to the first coordinate, scaling so population minimum variance is one. Write W=[[a,b'];[b,C]], C~W ishart_{K−1}(n,I). The fitted unit-budget weights are(1,−β)withβ=C⁻¹b. Conditional on C, β~N(0,C⁻¹); integrating over Cgives√νβ a spherical multivariate t_νwithν=n−K+2. Therefore||β||²=(K−1)F_{K−1,ν}/νand true-risk ratio 1+||β||²has the stated law. Its mean needsν>2, i.e.n > K, and equals 1+(K−1)/(n−K)=(n−1)/(n−K). K = 1 is degenerate. The Gaussian regression residual producing the in-law is independent ofβ.

For K,T→∞withγ<1, the appropriate chi-square degrees of freedom diverge and chi-square/df→1 in probability. The F component likewise concentrates when its dimensions grow; fixed K withγ=0 also gives the unit limits. Slutsky then gives the in/out limits and their random ratio. Dividing E[v_out/v*]by E[v_in/v*]gives the bias factor n(n−1)/[(n−K)(n−K+1)]. Multiplying the report by it estimates the ensemble mean E[v_out]without bias; it does not condition on the fitted sample. Shrinkage, dependence, tails and changingΣ require separate laws.

**12. Adjusted quadratic.** Let S≻0 andwsolve minw'Swsubject to 1'w=1,w≥0. KKT gives 2 Sw−γ1−λ=0, λ≥0 andλ_iw_i=0. Define S~=S−(λ1'+1λ')/2. Then S~w=Sw−λ/2=γ1/2. For any other unit-budgetu=w+v,1'v=0. The objective difference isu'S~u−w'S~w=2 v'S~w+v'S~v=v'Sv>0 forv≠0, because the rank correction vanishes on zero-budget directions. Thuswuniquely minimises the adjusted quadratic on that affine set even if S~is not positive definite on the whole space. This proves an algebraic equivalence, not future dominance or an identification of every unconstrained short.

## Papers, chapter by chapter

* ch. 1: Markowitz (1952); Merton (1972); Michaud (1989); Best and Grauer (1991); Chopra and Ziemba (1993); Scherer (2002).
* ch. 2: DeMiguel, Garlappi and Uppal (2009), *RFS* 22; Kan and Zhou (2007), *JFQA* 42; Tu and Zhou (2011), *JFE* 99.
* ch. 3: Marchenko and Pastur (1967); Laloux, Cizeau, Bouchaud and Potters (1999); Bun, Bouchaud and Potters (2017).
* ch. 4: Ledoit and Wolf (2003, 2004a, 2004b, 2020).
* ch. 5: Jagannathan and Ma (2003), *JF* 58; DeMiguel, Garlappi, Nogales and Uppal (2009), *Management Science* 55.
* ch. 6: Black and Litterman (1992), *FAJ*; He and Litterman (1999); Jorion (1986), *JFQA* 21.
* ch. 7: Maillard, Roncalli and Teïletche (2010); Spinu (2013); López de Prado (2016), *JPM*.
* ch. 8: Goldfarb and Iyengar (2003); Ceria and Stubbs (2006); Artzner, Delbaen, Eber and Heath (1999); Rockafellar and
  Uryasev (2000).
* ch. 9: Kelly (1956); Breiman (1961); Cover (1991); Fernholz (2002).
* ch. 10: Meucci (2008), "Fully flexible views".
* ch. 11: Zhang, Zohren and Roberts (2020), *JFDS*; Elmachtoub and Grigas (2022), *Management Science*.
* ch. 12: Jobson and Korkie (1981); Memmel (2003).
* Research: Muirhead (1982); Kempf and Memmel (2006); Bai, Liu and Wong (2009); El Karoui (2010); Ledoit and Wolf (2017);
  Bodnar, Parolya and Schmid (2018).

## Verification and rebuilding

Bilingual source and numerical checks pass. Existing pure portfolio/theory checks run with:

```bash
source /workspace/environment/activate.sh
python -m pytest -q tests/test_quant_house.py -k 'portfolio_estimators_and_allocations or gmv_theory_matches_simulation'
```

Original ordinary computation must specify only the fourteen allowed item names above. The default original CLI includes the excluded experiment and is outside this pass. Construction diagnostics do not supply final render approval. Final bilingual endpoint sheets, English motion, exact flagged intervals, sampled speech signals and a narrated opening must be checked on the final frozen source. Continuous production listening remains a separate step.

---

# 第30部分：组合构建

科学表述、双语构建与实际画面审阅已完成。十四个获准的常规原始计算已恢复，没有重试。完整成片连续听审与发音审查仍单独待办；封存策略在计数/缓存入口之前即被排除。

十六个场景讨论估计误差、等权、随机矩阵参考、协方差收缩、约束、Black–Litterman、ERC与HRP、鲁棒优化、CVaR、增长、熵池化、端到端学习、评估协议、研究证明和完整习题。材料用于方法教育。

## 数据及边界

原始代码使用French的49个市值加权行业组合、截至2020年的月度/日度收益与无风险利率，以及行业公司数量和平均规模。读取归档后才按截止日期筛选。冻结子集的哈希不证明历史发布时点、完整的时点成员或可成交性。模拟把1970–2020年的研究矩指定为固定高斯总体，不能称为历史未来交付。

计算代码、House算法和三份登记文件不变。只恢复前文列出的十四个常规项目，不访问envelope策略缓存或载荷，不强制重算、刷新、新增市场试验、登记、开启或评分。既有累计登记为第29部分23,480、第30部分23,525、全系列23,562；增加45是记账，不是独立检验数。

第二章所有规则的预测风险都用尾随**样本协方差**评价权重，不是各收缩估计器自报的风险。研究章另用收缩规则自己的拟合协方差，两个口径不同。滚动键名inverse volatility实际是逆方差，独立风险平价快照才用逆标准差。切点方向按权重和归一化，负分母可反转正夏普方向，接近零可产生极大总敞口。

换手仅取目标权重变化的一半，漏掉持仓漂移。成本表从均值中扣平均费用，保留毛波动率，故是敏感性近似。固定等权目标不等于零交易。样本和非线性收缩用T−1分母，局部线性收缩用去均值后的T分母。固定目标的强度公式不直接适用于同数据估出的目标；样本特征向量下的Frobenius先知值也不是组合损失先知值。

MP区间是渐近零假设参考，不是噪声分类器。原日度代码把缺失收益填零；特征值平均步骤保迹，随后的对角归一化仍可改变谱。负相关保留符号。Jagannathan–Ma只需预算为一的仿射空间上有相同曲率，不要求修改矩阵在全空间正定，更不保证未来改善。

BL中的delta也来自样本估计；观点误差方差倍数不是置信概率。不变协方差和含均值不确定性的预测协方差给不同需求；后者在观点均值等于先验时仍可能改权重。ERC等化拟合方差贡献，HRP用聚类和逆方差簇代理，两者不是同一个优化器，也不隔离估计误差。

离散ES按最坏概率质量计，必要时只取分位点原子的一部分。历史情景LP与插值分位点评分约定可能略有不同。Kelly二次增长属于所述扩散模型；拟合杠杆和分数Kelly不构成未来最优或普遍半Kelly规则。Cover连续均匀混合定理与201点网格混合不同；网格最优/混合财富比上界201，连续两资产上界n+1。行业市值的月度多样性例子不验证连续时间、扣费后相对套利。

熵有效情景数衡量概率集中度，不是独立样本数。市场压力约束是围绕**先验均值**的二阶矩，后验均值未固定，其平方根不一定是后验标准差。端到端原始示范在划分训练与验证前，用两个时期共同标准化特征，泄漏验证矩；验证还被反复观察。日志训练分数在更新前、验证在更新后，最终表用最终权重。只有一个种子和分数轨迹，无中间权重检查点；两步对照是逆矩阵方向截负并归一化，不是精确只做多MV解。这些是保留缺陷并披露的回顾诊断，不重新训练寻求更好成绩。

优化云图保留负模型均值和高波动尾部。直方图不把区间外数值折到边界。研究T=120的两组直方图各保留1000计数，柱高为计数/1000。缓存T=60的0–6真风险区间仅664计数，T=80有999；其他尾部的位置未存，不虚构、不重跑。

## 协议与固定算术

冻结数据时点、预处理、窗口、调参、求解器、约束、停止和报告政策；明确漂移持仓、现金、成交、融资、借券与成本。配对比较需考虑相依和选择。宽区间不证明等价，一个新时期也不自动解决泄漏或低检验力。不提供封存策略结论。

固定不相关年波动10%、20%：GMV权重(.8,.2)，波动8.944%；ERC权重(2/3,1/3)，波动9.428%；等权波动11.180%。另一个单期玩具从各半美元开始，指定收益(10%,0)，成交前价值(.55,.50)，总值1.05，权重(11/21,10/21)。费用前恢复等权需卖.025、买.025，毛交易.05初始美元。每成交美元5基点则费用.000025初始美元，即初始财富.25基点。费用另付，未求扣费后自融资再平衡。

## 六个交易台检查

1. 乐观误差为何被选择：看目标、归一化、约束、损失和评估，不能归因于一个普遍机制。
2. 49资产60个月、报告3%波动：不能据此知道真实风险；高斯倍数只是条件模型参考。
3. 只做多改善：调整二次型恒等式不是未来优势保证。
4. 无观点BL：均值保持Π，不变Σ恢复基准风险需求；预测(1+τ)Σ给基准/(1+τ)，另加约束会变。
5. 估计Kelly：分数需要真实强度、已知方差和明确误差及偿付假设，不能普遍选一半。
6. 固定等权仍需交易：收益使持仓漂移，交易来自成交前权重，费用分母另需说明。

## 习题1–6：完整解答

**1. GMV。** 最小化.01w²+.04(1−w)²，一阶条件.02w−.08(1−w)=0，得(.8,.2)。方差.008，波动.0894427。已知协方差、预算为一，不含收益预测。

**2. ERC。** 正权重下(w₁σ₁)²=(w₂σ₂)²给权重比2，得(2/3,1/3)。方差.00888889、波动.0942809。等权方差.0125、波动.111803。等钱、等风险和最小方差目标不同。

**3. MP。** q=49/60=.816667，平方根.903696，边界(1±√q)²约.00927444、3.62405889。独立单位方差、高维渐近零假设下成立；代入有限维度不是置信界，更不识别经济信号。

**4. 强度。** 令A=E||S−Σ||²、B=||F−Σ||²。F固定且S无偏使交叉项为零，风险δ²B+(1−δ)²A，导数为零得δ=A/(A+B)，等于噪声/样本到目标的期望平方距离；限制到[0,1]，若分母零则所有δ相同。F也由S估计时交叉协方差不能忽略，原推导不直接适用。

**5. BL。** 无信息观点下均值Π=δΣw_m，均值不确定性M=τΣ。用Σ优化得w_m；用Σ+M得w_m/(1+τ)，这里没有额外预算约束。若P=0，取正定Ω才可直接用精度公式；不能盲目反演默认的奇异零矩阵。

**6. Kelly。** 已知参数扩散模型f*=.06/.16²=2.34375。二次超额增长fμ−f²σ²/2，在2f*处为零，总增长等于无风险率。这不是离散路径或不破产保证。

## 习题7–10：完整解答

**7. 混合界。** 正价格比、无摩擦再平衡时，两资产连续均匀混合满足连续事后最优/混合≤n+1，故每期对数增长差≤log(n+1)/n→0。M个固定组合等初始资本的混合财富为ΣS_j/M≥maxS_j/M，故网格最优/混合≤M，每期差≤logM/n。后者只竞争网格，不能认证连续最优近似误差，也不竞争任意动态先知策略、不含成本。

**8. ES。** 80%时最坏20%正好是10，ES=10；60%时最坏40%是5和10，ES=7.5。按概率质量计，分位点原子只取所需部分；无条件把所有“大于等于分位点”的观测平均，可能取多了质量。也可直接最小化α+E[(L−α)⁺]/(1−β)。

**9. 熵。** q₁+q₂=1、−.1q₁+.1q₂=.05给(.25,.75)。这是唯一可行概率向量，所以也是相对正先验的熵最优；不需高斯，仅使用所给两情景。

**10. 倍数。** K=100、T=250、n=249：报告风险相对总体最小值的期望150/249=.6024096，真风险期望248/149=1.6644295。期望之比约2.7630，γ=.4的极限参考2.77778。都不是某次拟合的已知倍数。高斯下报告的舒尔残差与决定真风险的回归系数独立，n>K+1时随机比的期望为[(n−1)/(n−K)]×[n/(n−K−1)]，与期望之比不同。

## 习题11–12：资格题完整证明

**11. 分布及修正。** 固定非零a可通过同时变换a、W、Σ转到第一坐标。分块逆矩阵给(W⁻¹)₁₁=1/s，s=W₁₁−W₁₂W₂₂⁻¹W₂₁。把W写作n个高斯向量的交叉积，将第一列对其他K−1列回归，残差自由度n−K+1，因此s/σ₁₁·₂为该自由度χ²；而(Σ⁻¹)₁₁=1/σ₁₁·₂，得到逆二次型引理。取a=1、W=nS，报告风险比为χ²_{n−K+1}/n，期望(n−K+1)/n。

真风险方面，先白化并旋转变换后的预算向量到第一坐标，缩放至总体最小方差为一。写W=[[a,b'];[b,C]]，C为K−1维、n自由度单位尺度Wishart。拟合单位预算权重为(1,−β)，β=C⁻¹b。给定C，β为N(0,C⁻¹)；积分C得到√νβ服从球面对称多元t，ν=n−K+2。故||β||²=(K−1)F_{K−1,ν}/ν，真风险比为1+||β||²。有限均值需ν>2即n>K，得(n−1)/(n−K)。K=1时真风险比恒一。报告风险所用回归残差与β独立。

K、T共同趋大且K/T→γ<1时，相应χ²/自由度依概率趋一，F部分也集中；固定K且γ=0亦得一。由Slutsky，报告、真风险和随机比的极限依次为1−γ、1/(1−γ)、1/(1−γ)²。两个期望相除得修正n(n−1)/[(n−K)(n−K+1)]；乘报告风险无偏估计的是重复训练总体中E[v_out]，不是给定拟合的条件风险，更不是随机比的期望。正态性、独立性、固定正定Σ及秩条件不能省略，收缩有不同分布。

**12. 调整二次型。** S正定，预算一且w≥0。KKT为2Sw−γ1−λ=0、λ≥0、λ_iw_i=0。定义S~=S−(λ1'+1λ')/2，则S~w=γ1/2。任意其他单位预算u=w+v有1'v=0。二次型差2v'S~w+v'S~v=v'Sv，非零v时严格正，因为调整项在零预算方向消失。故w在预算仿射空间上唯一最优，毋须S~在全空间正定。恒等式不保证未来改善，也不识别所有原无约束空头。

参考文献对应上方逐章列表。最终冻结源上的双语节点、英文动画及精确标记区间现均已实际审阅；诊断与最终批准分开保存。完整成片连续听审与发音认证仍单独待办。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part30.md`](../../../docs/qa/quant/part30.md).*
