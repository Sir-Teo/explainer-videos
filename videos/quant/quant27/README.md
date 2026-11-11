# Part 27 — Machine Learning for Returns

This lecture studies weak return signals, model complexity, learned factor structures and prediction intervals. Published stock results, mathematical examples and the smaller original crypto calculations are distinct kinds of evidence. A model's training fit, a nominal interval or a high-dimensional architecture does not supply missing evaluation assumptions.

## Review status and data boundary

Scientific presentation, bilingual construction and actual rendered visual review are complete on the pinned source below. Full continuous production listening and pronunciation review remain separately pending.

The financial algorithms in `compute.py` and the House library are preserved byte for byte. The ordinary originals are `snr`, `kmz`, `nagel`, `zoo`, `descent`, `autoenc`, `attention`, `images`, `sdf`, `toolkit`, `conformal`, `pretrained` and `theory`. Their normal restoration attempts and frozen public-input checks are audited. Unavailable originals must remain withheld rather than replaced by a new historical strategy.

**Exclude `panel` and `envelope`.** The former invokes sealing; the latter registers and opens experiments. Neither may be computed or loaded for this presentation. Ordinary readers can read publicly available archives through 2025 before their research masks; this is different from accessing a sealed strategy payload. No claim is made that all post-2020 public bytes were unread. No new trials, force/refresh, registry writes, sealed-cache reads, opening or scoring are authorised by this review.

Existing read-only metadata records **10,457 cumulative trials through Part 27**, including an existing increment of 109, and 23,562 globally. These are registration counts, not proof that every informal research choice was counted.

The thirteen ordinary attempts are now complete: twelve succeeded; `pretrained` stopped at the first SPY reader because its frozen normalised input hash differed (observed prefix `d1d7c2e22207`, recorded `03d9199c9b96`). No result cache was produced, and the QQQ/EEM/GLD/XLE comparisons were not reached. Its numerical transfer results are withheld. The normal attempt was not retried and the source was not refreshed. The simulated explanatory window remains explicitly labelled and supplies no substitute historical score.

## Chapters and qualifications

| Scene | Subject and scope |
|---|---|
| Hook | GKX's author-reported stock results; an explicitly specified binary-signal breadth example |
| Signal | In-sample monthly volatility-normalised predictor fits; zero and historical-mean benchmarks differ |
| Zoo | Venue-specific USDT archive; later symbol coverage is not an investable point-in-time universe |
| Limits | Quote-volume splits and fixed turnover/fee scenarios; no causal or executable-capacity conclusion |
| Complexity | Positive ridge need not interpolate; capacity and feature scaling matter |
| Critics | Kernel diagnostics; artificial reversal baseline has different information |
| Theory | Gaussian proportional limits; excess risk excludes fresh noise, misspecified total MSE includes it |
| Autoencoder | Restricted managed-factor implementation; contemporaneous reconstruction differs from forecasting |
| DeepSDF | Finite pooled moments and L1-normalised weights; no positivity or general pricing certificate |
| Attention | Set interactions beyond already ranked inputs; one selected seed/week heatmap is descriptive |
| Images | Previous-close open proxy; selected images, overlapping training windows and gross comparisons |
| Foundation | Context-centred log absolute moves; retrospective transfer chronology and unequal adaptation |
| Toolkit | Activity bars, finite filters, daily-close barriers and concurrency weights |
| Conformal | Independent calibration and exchangeable scores; actual finite-boundary adaptive rule has limits |
| Firms | Dated public reports and the 16 January 2025 SEC firm settlement |
| Envelope | Registration and evaluation protocol; fixed paired-mean arithmetic, no sealed scores |
| House | Rule 27: evaluate the full information, selection, calibration and execution protocol |
| Outro | Fourteen qualified recap lines, six desk questions and twelve worked problems |

The frozen public symbol list contains 701 names. Original eligibility uses at least 30 recorded daily observations, weeks with at least ten eligible coins, 60 calendar days since the first observed close and a past-28-day median quote volume of at least 250,000 USDT. Missing-price and last-close fallbacks do not certify liquidation or delisting returns. Quote volume is not market capitalisation. Same-close forecasts and gross long-short returns do not establish attainable fills or short availability.

Subtracting seven from an integer YYYYMMDD date is not seven calendar days. The original zoo/conformal period cuts can retain late-December features whose seven-day labels end in January. Training and validation labels are winsorised separately using their own outcome quantiles; test labels stay raw. These original limitations are disclosed rather than repaired by a substitute market test.

## Mathematical scope

For a symmetric binary signal $S=\pm1$, $r=aS+\varepsilon$ with independent mean-zero noise variance $\sigma^2$, forecast $aS$ and sign position $S$, population $R^2=a^2/(a^2+\sigma^2)$ yields annual Sharpe $\sqrt{12R^2/(1-R^2)}$. Independent equal-risk bets multiply this by $\sqrt N$. **Arbitrary measured out-of-sample $R^2$ does not determine attainable Sharpe**, sign accuracy or a literal explained-variance fraction.

For IID normal weekly returns, annual Sharpe variance is approximately $(1+SR_{ann}^2/(2q))/T_{years}$, $q=52$. The approximation $SE\simeq1/\sqrt{T_{years}}$ and two-SE length $4/SR_{ann}^2$ are precision heuristics, not prospective power calculations. Paired strategy comparisons need their covariance, dependence and selection history.

The Gaussian ridge theorem assumes isotropic independent Gaussian features, independent noise, stated signal scaling and proportional dimension. Numerical limits use finite quadrature. Simulation medians and ranges are not exact finite-sample equality. Restricted managed-factor autoencoders are not identical to unrestricted ALS IPCA; their total fit uses contemporaneous test returns, while prediction uses mean factors from training plus validation.

Split conformal requires calibration labels independent of predictor fitting/selection and exchangeable calibration/new scores conditional on fitting. Rank $k=\lceil(n+1)(1-\alpha)\rceil$ uses infinite width when $k>n$; the unchanged helper caps $k$ at $n$. The crypto NN2 reuses validation labels for selection and calibration, so standard split-conformal coverage does not certify that example. Coverage is marginal, not per-regime.

The adaptive update always telescopes, but arbitrary-sequence counting bounds need appropriate boundary conventions or another bounded-state argument. The House uses finite past maxima and zero widths instead of infinite intervals and empty sets. Strictly increasing residual scores can therefore cause every interval to miss and drive the working level to negative infinity. An empirical Bitcoin coverage value is descriptive.

## References

Books: Kelly and Xiu, *Financial Machine Learning* (2023), chapters 1–9; Lopez de Prado, *Advances in Financial Machine Learning*, chapters 2–5 and 10; Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning*, chapters 3, 10 and 11; Goodfellow, Bengio and Courville, *Deep Learning*, chapters 6–9; Isichenko, *Quantitative Portfolio Management*, chapter 2.

Research includes Marchenko and Pastur (1967); Grinold (1989); Hansen and Jagannathan (1991); Vovk, Gammerman and Shafer (2005); Rahimi and Recht (2007); Welch and Goyal (2008); Zaheer et al. (2017); Dobriban and Wager (2018); Lei et al. (2018); Belkin et al. (2019); Kelly, Pruitt and Su (2019); Bartlett et al. (2020); Gu, Kelly and Xiu (2020, 2021); Israel, Kelly and Moskowitz (2020); Gibbs and Candès (2021); Giannone, Lenza and Primiceri (2021); Hastie et al. (2022); Mei and Montanari (2022); Leippold, Wang and Zhou (2022); Avramov, Cheng and Metzker (2023); Jiang, Kelly and Xiu (2023); Chen, Pelger and Zhu (2024); Kelly, Malamud and Zhou (2024); Ansari et al. (2024); Das et al. (2024); Nagel (2025); Kelly, Kuznetsov, Malamud and Xu (2025); Shi et al. (2025).

Verified primary references:

- [Gu, Kelly and Xiu, official paper](https://dachxiu.chicagobooth.edu/download/ML.pdf): author-reported monthly OOS $R^2$ around 0.33–0.40%; best NN gross long-short Sharpe 1.35 with market-cap weights, 2.45 with equal weights. These historical stock results are not this crypto illustration.
- [Kronos, arXiv:2508.02739](https://arxiv.org/abs/2508.02739), first posted August 2025: author-reported relative RankIC +93%/+87%, volatility MAE −9%, generative fidelity +22% on the paper's benchmarks. Not replicated here; corpus size alone proves no leakage.
- [SEC release 2025-15, 16 January 2025](https://www.sec.gov/newsroom/press-releases/2025-15): firm settlement, $90 million total penalties ($45 million per adviser) and $165 million voluntary repayments; the release also covers separate whistleblower-protection violations. Do not attribute all penalties solely to model changes or infer current individual-case status.
- Zuckerman (2019): reported Medallion arithmetic annual averages 66.1% gross and 39.1% net over 1988–2018. Public historical reporting is not an audited current offering or an investor-attainable forecast.

## Six desk questions, with solutions

1. **Half a percent population $R^2$, 500 independent binary-signal bets?** Under the explicitly stated model, $\sqrt{12(500)(0.005)/0.995}=5.49$ annual Sharpe. Measured OOS $R^2$ alone does not justify the model, independent bets, known parameters or trading assumptions.
2. **A million parameters and perfect training fit?** This alone decides little. Check rank, penalty, scaling, signal/noise assumptions, matched-information baselines and independent predictive risk. Positive ridge does not generally interpolate.
3. **Direction accuracy 55%?** Need move sizes, base rates, position sizes, covariance, turnover, execution and costs. Accuracy alone cannot determine net value.
4. **Annual Sharpe one over two years?** The IID-normal weekly approximation gives $SE=\sqrt{(1+1/104)/2}\simeq0.71$ and an illustrative normal 95% range near $[-0.39,2.39]$. This omits dependence, selection and small-sample uncertainty. A paired model comparison needs return covariance; power additionally needs an alternative and a rejection rule.
5. **Meta-model doubles precision but keeps one bet in ten?** Compare net profit and risk per unit time, accounting for move sizes, lost breadth and overlapping positions. In a simplified independent equal-scale setting, losing a factor ten in breadth requires a $\sqrt{10}$ increase in per-bet Sharpe to preserve total Sharpe. Precision does not determine that increase.
6. **A nominal 90% interval covers 70% in one regime?** A marginal theorem is not regime-conditional coverage. Check independent fitting, calibration/new-score exchangeability and implementation boundaries. Rolling or adaptive changes create a different protocol that needs its own evaluation; the original finite-max rule has no arbitrary-sequence certificate.

## Twelve problems with full solutions

Problems 1–6 develop the basic calculations; 7–10 extend the implementation analysis; 11–12 are qualifying problems. Numbering is continuous across the three screen pages.

1. **Binary signal and breadth.** Let $S=\pm1$ equiprobably, $r=aS+\varepsilon$, with independent mean-zero $\varepsilon$, variance $\sigma^2$, independent across months. Forecast $aS$. Its population squared-error reduction versus zero is $1-\sigma^2/(a^2+\sigma^2)=a^2/(a^2+\sigma^2)$. The sign-position payoff is $Sr=a+S\varepsilon$, with mean $a$ and variance $\sigma^2$. Its monthly Sharpe is $a/\sigma=\sqrt{R^2/(1-R^2)}$ for $a\ge0$. Independent months annualise by $\sqrt{12}$; $N$ independent equal-risk bets multiply the ratio by $\sqrt N$. Dependence, estimated forecasts and trading constraints invalidate a universal mapping from arbitrary empirical OOS $R^2$.

2. **Paired means.** For $D=A-B$, $\operatorname{Var}D=\sigma_A^2+\sigma_B^2-2\rho\sigma_A\sigma_B$. With unit standard deviations and $\rho=0.8$, variance is 0.4 and SD is $\sqrt{0.4}=0.63246$. For 100 independent pairs, $SE(\bar D)=\sqrt{0.4/100}=0.06325$. Correlated dates require a long-run variance estimator. This is a mean comparison in arbitrary units, not a Sharpe-difference formula.

3. **Zero-penalty ridge.** For a compact SVD $X=UDV^\top$, $\hat b_\lambda=V\operatorname{diag}(d_j/(d_j^2+N\lambda))U^\top y$. As $\lambda\downarrow0$, nonzero singular directions give $VD^{-1}U^\top y=X^+y$. This is the minimum-norm least-squares solution, since null-space additions increase norm. It interpolates iff $y$ lies in the column space of $X$, in particular for every $y$ when $X$ has full row rank. $P>N$ alone is insufficient without that rank condition. Positive ridge generally does not interpolate.

4. **Gaussian random Fourier features.** For $w\sim N(0,\eta^2I)$, $w^\top\Delta$ is normal with variance $\eta^2\|\Delta\|^2$. Its characteristic function gives $E\cos(w^\top\Delta)=\exp(-\eta^2\|\Delta\|^2/2)$. Paired sine/cosine maps with $M$ independent frequencies have inner product $M^{-1}\sum_j\cos(w_j^\top\Delta)$. Each summand is bounded, so its sample-mean variance is at most $1/M$ and pointwise error is $O_p(M^{-1/2})$. This is not a deterministic uniform guarantee over all possible inputs.

5. **Canonical projection and HJ bound.** Let $R$ be excess returns, $E R=\mu$, $\operatorname{Cov}R=\Sigma\succ0$, and $s^2=\mu^\top\Sigma^{-1}\mu$. For $M=1-w^\top R$, $E[MR]=0$ gives $(\Sigma+\mu\mu^\top)w=\mu$. Sherman–Morrison yields $w=\Sigma^{-1}\mu/(1+s^2)$. Hence $E M=1/(1+s^2)$ and $\operatorname{sd}M=s/(1+s^2)$. For any priced portfolio, $E M\,E R_p=-\operatorname{Cov}(M,R_p)$, so Cauchy–Schwarz gives $|SR_p|\le\operatorname{sd}M/E M$. The projection attains the unrestricted tangency ratio $s$, but may be negative in some states; it is not automatically a positive arbitrage-free SDF or the solution of a constrained conditional network problem.

6. **Brownian barriers.** Let $X_t=\mu t+\sigma W_t$, $\sigma>0$, start at zero, and stop on first hitting $\pm b$, $b>0$. The upper-hit probability solves $(\sigma^2/2)u''+\mu u'=0$ on $(-b,b)$, with $u(-b)=0$, $u(b)=1$. Solving gives $u(0)=(1-e^{-2\mu b/\sigma^2})/(1-e^{-4\mu b/\sigma^2})=1/(1+e^{-2\mu b/\sigma^2})$. Its continuous limit at $\mu=0$ is $1/2$. A finite horizon, discrete closes, overshoots and costs define a different problem.

7. **Fractional-filter decay.** With $w_0=1$ and $w_k=-w_{k-1}(d-k+1)/k$, repeated multiplication gives $w_k=(-1)^k{d\choose k}=\Gamma(k-d)/[\Gamma(-d)\Gamma(k+1)]$ for noninteger $0<d<1$. The gamma-ratio asymptotic gives $w_k\sim k^{-d-1}/\Gamma(-d)$; the prefactor is negative for this range of $d$. Polynomial decay is an infinite-filter property. Finite truncation, an ADF rejection or high correlation with the original price does not prove stationarity, preserved economic information or forecasting value. Fractionally differencing an $I(1)$ process by 0.3 need not make it stationary.

8. **Inclusive uniqueness.** With one label starting each integer day and fixed inclusive span $[i,i+h]$, an interior day is covered by starts $t-h,\ldots,t$, namely $h+1$ labels. Average inverse concurrency for an interior label is therefore $1/(h+1)$. A half-open span covering exactly $h$ dates instead gives $1/h$. Early barrier endings and sample edges change the weights. Summing uniqueness weights is a concurrency diagnostic, not a universal effective independent sample size or a replacement for covariance-based inference.

9. **Attention equivariance.** Shared rowwise projections under permutation $P$ give $Q'=PQ$, $K'=PK$, $V'=PV$. Therefore $Q'K'^\top=P(QK^\top)P^\top$. Rowwise softmax commutes with the simultaneous row/column permutation, so $A'=PAP^\top$ and $A'V'=PAV$. Shared output maps, residuals and rowwise feed-forward operations preserve this property. A fixed nonpermuted row-slot embedding can break it. An identity or alphabetical-rank feature that moves with its asset is part of the permuted row and need not break reindexing equivariance. Symmetry alone gives no predictive guarantee.

10. **Adaptive counting and a counterexample.** Sum $a_{t+1}=a_t+\gamma(\alpha-e_t)$ to get $T^{-1}\sum_te_t-\alpha=(a_1-a_{T+1})/(\gamma T)$. For finite scores, ideal conventions of an infinite interval when $a_t\le0$ and an empty set when $a_t\ge1$, with $a_1\in[0,1]$, keep the state in $[-\gamma,1+\gamma]$. Consequently the absolute discrepancy is at most $[\max(a_1,1-a_1)+\gamma]/(\gamma T)$. The House instead uses a finite past maximum and a zero-width interval at the boundaries. Strictly increasing residual scores exceed every finite past maximum, so $e_t=1$ forever and $a_t\to-\infty$ for $\alpha<1$. The identity still holds, but its remainder need not vanish. Zero residuals also distinguish width-zero from an empty set.

11. **(qual) Split conformal.** Conditional on an independently fitted predictor, suppose the $n$ calibration scores and the new score are exchangeable. With distinct scores, the new rank is uniform on $1,\ldots,n+1$. Let $k=\lceil(n+1)(1-\alpha)\rceil$, and choose the $k$th calibration order statistic, using infinity if $k>n$. Then coverage is $k/(n+1)\ge1-\alpha$, and it is at most $1-\alpha+1/(n+1)$. Random tie breaking recovers the uniform-rank argument; inclusive intervals without random tie breaking can only increase coverage, so the upper bound need not hold with ties. If $k=n+1$, infinite width covers surely. These are marginal statements; selection on calibration outcomes invalidates the standard conditional argument. The capped finite-order helper does not provide the all-alpha theorem.

12. **(qual) Gaussian finite-sample risk and limits.** Let $X$ have IID $N(0,1)$ entries, independent noise variance $\sigma^2$, fixed $\|b\|^2=r^2$ and independent isotropic test covariates. For $P<N-1$, OLS has conditional coefficient covariance $\sigma^2(X^\top X)^{-1}$; the Wishart inverse mean is $I/(N-P-1)$. Thus expected excess prediction risk is $\sigma^2P/(N-P-1)$, tending to $\sigma^2\gamma/(1-\gamma)$ when $P/N\to\gamma<1$. For $P>N+1$, minimum-norm error separates into lost signal $(I-X^+X)b$ and fitted noise $X^+\varepsilon$. Rotational invariance gives expected squared bias $r^2(1-N/P)$; $XX^\top$ is Wishart with $P$ degrees of freedom, yielding variance $\sigma^2N/(P-N-1)$. The limit is $r^2(1-1/\gamma)+\sigma^2/(\gamma-1)$. For $r^2=\sigma^2=1$ and $\gamma>1$, this equals $1+1/[\gamma(\gamma-1)]>1$, the zero-forecast excess risk; at $\gamma=1/2$, excess risk is one. Add fresh noise variance one for total MSE. For stronger signal $r^2>\sigma^2$, above-threshold ridgeless excess risk can beat zero when $\gamma>r^2/(r^2-\sigma^2)$; the unit-signal conclusion is not universal.

# 中文说明

本讲区分三类证据：文献作者报告的股票结果、明确给定假设的数学例子，以及较小规模的原始加密资产计算。训练拟合、名义覆盖率和复杂架构都不能补足评估中缺少的假设。科学表述修订、双语构造与实际渲染视觉审查已完成，证据见下文；完整生产成片连续听审和发音检查仍为独立待办。

十三项普通计算已尝试完成，十二项成功；预训练迁移在首个SPY冻结输入哈希不符时停止，未产生结果缓存，后续四只ETF未评估。数值结果保留缺失，不刷新、不重试，也不做替代历史策略。模拟窗口仅解释协议。

金融算法、House库和全局登记数据保持原字节。`panel`会调用封存，`envelope`会登记并打开实验，因此二者均不得计算、加载或评分。普通读取器可能先读取截至2025年的公开档案再应用研究期掩码；不能声称所有2020年后的公开数据从未读取。已有只读计数是第27讲累计10,457次、全系列23,562次；本次不新增试验，不强制刷新，不修改登记，不读取封存策略载荷。无法通过冻结输入校验的原始结果必须保留缺失状态。

701个名称是后来的公开档案覆盖，不能等同于逐时可投资样本池。60天按首次观测价格后的日历天数计算，成交额以USDT计价，不是市值。最后可用收盘价及缺失回退不保证完整退市清算收益。整数日期减7并非减7个日历日，部分年末标签可延伸至下一年。训练与验证目标分别按各自结果分位数缩尾；测试目标不缩尾。这些局限保持并披露，不另做替代历史策略测试。

理论岭回归风险是各向同性高斯、独立噪声与比例维数下的极限，超额风险不含新观测噪声；设定错误例子画的是包含噪声的总均方误差。自编码器总拟合用当期已实现收益提取因子，不能称为预测；预测版使用训练加验证期的因子均值。有限对抗矩不能认证正随机折现因子、每项条件矩或全局最优。

分裂共形要求预测器拟合和选择独立于校准标签，并要求给定拟合结果后，校准与新分数可交换。原始NN2重复使用验证标签进行选择和校准，不满足标准论证。边际覆盖也不是每个市场状态的覆盖。自适应更新的望远镜恒等式总成立，但任意序列计数界依赖边界约定和有界状态；House使用有限历史最大值及零宽区间，不自动继承无限区间与空集规则的保证。

## 六个交易台问题与解答

1. **二值信号、总体$R^2=0.5\%$、500个独立等风险下注？** 明确模型下年化夏普为$\sqrt{12\times500\times0.005/0.995}\approx5.49$。任意测得的样本外$R^2$不能单独确定可实现夏普；还需独立性、已知参数和交易假设。
2. **参数比样本多且训练完美拟合？** 单凭这一点无法判断。检查秩、惩罚、特征尺度、信噪比、同等信息基准与独立预测风险。正惩罚岭回归通常不插值。
3. **方向准确率55\%？** 还需涨跌幅、基准比例、仓位、协方差、换手、成交与成本。准确率不能决定净价值。
4. **两年年化夏普为1？** 独立正态周收益近似给出标准误$\sqrt{(1+1/104)/2}\approx0.71$，示意95\%区间约为$[-0.39,2.39]$。它未处理相依、选择或小样本误差。成对比较需要收益协方差；功效还需备择和拒绝规则。
5. **元模型精确率翻倍但只保留十分之一机会？** 比较单位时间扣费后的收益和风险，考虑涨跌幅、广度损失及重叠仓位。独立等尺度简化下，广度缩小十倍要求单笔夏普提高$\sqrt{10}$倍才能维持总体夏普；精确率本身不能确定这一点。
6. **名义90\%区间在一个状态只覆盖70\%？** 边际定理并不保证状态条件覆盖。先检查独立校准、可交换性和真实边界规则。滚动或自适应修改形成新协议，需要另行评估；原始有限最大值规则没有任意序列认证。

## 十二道习题与完整解答

1. **二值信号与广度。** 设$S=\pm1$等概率，$r=aS+\varepsilon$，噪声独立、均值零、方差$\sigma^2$，月份相互独立。预测$aS$相对零预测的总体平方误差改善为$a^2/(a^2+\sigma^2)$。按信号符号持仓得到$Sr=a+S\varepsilon$，均值$a$、方差$\sigma^2$，月夏普为$a/\sigma=\sqrt{R^2/(1-R^2)}$（$a\ge0$）。独立月份乘$\sqrt{12}$，$N$个独立等风险下注再乘$\sqrt N$。相依、预测估计和交易约束会改变映射，任意经验样本外$R^2$不能普遍推出可实现夏普。

2. **成对均值。** 令$D=A-B$，则$\operatorname{Var}D=\sigma_A^2+\sigma_B^2-2\rho\sigma_A\sigma_B$。两者标准差均为1、相关系数0.8时，方差0.4，标准差$\sqrt{0.4}=0.63246$。100组独立配对的均值差标准误为$\sqrt{0.4/100}=0.06325$。日期相依时应估计长期方差。这是任意单位的均值比较，不是夏普差公式。

3. **零惩罚岭极限。** 紧致奇异值分解$X=UDV^\top$给出$\hat b_\lambda=V\operatorname{diag}[d_j/(d_j^2+N\lambda)]U^\top y$。令$\lambda\downarrow0$得$VD^{-1}U^\top y=X^+y$。任何零空间附加项都增加范数，因此这是最小范数最小二乘解。当且仅当$y$在$X$的列空间中时插值；满行秩时对每个$y$都插值。只有$P>N$而无秩条件并不足够；正惩罚通常不插值。

4. **高斯随机傅里叶特征。** 若$w\sim N(0,\eta^2I)$，则$w^\top\Delta$为方差$\eta^2\|\Delta\|^2$的正态变量。特征函数实部给出$E\cos(w^\top\Delta)=e^{-\eta^2\|\Delta\|^2/2}$。配对正弦余弦、$M$个独立频率的内积是余弦样本均值；每项有界，均值方差不超过$1/M$，固定输入处误差为$O_p(M^{-1/2})$。这不是所有输入上一致成立的确定性保证。

5. **典范投影与HJ界。** 超额收益均值$\mu$、协方差$\Sigma\succ0$，设$s^2=\mu^\top\Sigma^{-1}\mu$。$M=1-w^\top R$和$E[MR]=0$给出$(\Sigma+\mu\mu^\top)w=\mu$。谢尔曼–莫里森公式得$w=\Sigma^{-1}\mu/(1+s^2)$，故$E M=1/(1+s^2)$，标准差$s/(1+s^2)$。任一定价组合满足$E M E R_p=-\operatorname{Cov}(M,R_p)$，柯西–施瓦茨给出$|SR_p|\le\operatorname{sd}M/E M$。无约束投影达到切点比率$s$，但可能在某些状态取负；不能自动视为正的无套利折现因子或受约束条件网络的解。

6. **布朗双障碍。** $X_t=\mu t+\sigma W_t$、$\sigma>0$，从零出发，首次到达$\pm b$时停止。上障碍先到概率满足$(\sigma^2/2)u''+\mu u'=0$，边界$u(-b)=0,u(b)=1$。解得$u(0)=(1-e^{-2\mu b/\sigma^2})/(1-e^{-4\mu b/\sigma^2})=1/(1+e^{-2\mu b/\sigma^2})$。$\mu\to0$时极限为二分之一。有限期限、离散收盘、跳越和成本是不同问题。

7. **分数阶权重衰减。** $w_0=1$，递推$w_k=-w_{k-1}(d-k+1)/k$给出$w_k=(-1)^k{d\choose k}=\Gamma(k-d)/[\Gamma(-d)\Gamma(k+1)]$，其中非整数$0<d<1$。伽马函数比值渐近得$w_k\sim k^{-d-1}/\Gamma(-d)$，该范围内前因子为负。这是无限滤波性质。有限截断、ADF拒绝或与原价格高相关都不能证明平稳、保留经济信息或具备预测价值；对$I(1)$过程做0.3阶差分不一定使其平稳。

8. **含端点唯一性。** 每日启动一个固定标签$[i,i+h]$且两端计入时，内部日期由$t-h,\ldots,t$启动的$h+1$个标签覆盖。因此内部平均逆并发度为$1/(h+1)$。若用恰含$h$个日期的半开区间，则为$1/h$。提前触及障碍和样本边缘会改变平均值。唯一性之和是并发诊断，不是普适独立样本量，也不能替代协方差推断。

9. **注意力等变性。** 行置换$P$使共享投影变为$Q'=PQ,K'=PK,V'=PV$，分数矩阵变为$P(QK^\top)P^\top$。逐行softmax与同时行列置换可交换，所以$A'=PAP^\top$且$A'V'=PAV$。共享输出映射、残差和逐行前馈保持性质。固定且不随行移动的位置嵌入可能破坏它；随资产同行置换的身份或字母排序特征则不一定破坏重新索引等变性。对称性不保证预测有效。

10. **自适应计数及反例。** 累加$a_{t+1}=a_t+\gamma(\alpha-e_t)$得$T^{-1}\sum e_t-\alpha=(a_1-a_{T+1})/(\gamma T)$。对有限分数，理想边界在$a_t\le0$时用无限区间、$a_t\ge1$时用空集，且$a_1\in[0,1]$，可将状态限制在$[-\gamma,1+\gamma]$。于是误差绝对值不超过$[\max(a_1,1-a_1)+\gamma]/(\gamma T)$。House却使用有限历史最大值和零宽区间。严格递增残差始终超过有限历史最大值，导致每次都漏盖，$\alpha<1$时$a_t\to-\infty$。恒等式仍正确，余项却不趋零。零残差也说明零宽区间不等于空集。

11. **（资格考试）分裂共形。** 给定独立拟合的预测器，假设$n$个校准分数和新分数可交换。无并列时，新秩在$1,\ldots,n+1$均匀分布。令$k=\lceil(n+1)(1-\alpha)\rceil$，采用第$k$个校准次序统计量；$k>n$时取无限宽。覆盖率为$k/(n+1)\ge1-\alpha$，且不超过$1-\alpha+1/(n+1)$。随机打破并列可恢复均匀秩；不随机且含边界的区间可能更保守，因此有并列时上界不必成立。$k=n+1$时无限宽必然覆盖。这是边际结论，校准标签参与选择会破坏标准条件论证；有限次序截顶的辅助函数不提供所有显著性水平的定理。

12. **（资格考试）高斯有限样本与极限风险。** $X$元素独立标准正态，独立噪声方差$\sigma^2$，固定$\|b\|^2=r^2$，测试协变量独立且各向同性。$P<N-1$时OLS条件协方差为$\sigma^2(X^\top X)^{-1}$；逆Wishart均值为$I/(N-P-1)$，故期望超额预测风险为$\sigma^2P/(N-P-1)$，比例极限为$\sigma^2\gamma/(1-\gamma)$。$P>N+1$时最小范数误差分成丢失信号$(I-X^+X)b$及拟合噪声$X^+\varepsilon$。旋转不变性给出期望偏差平方$r^2(1-N/P)$；$XX^\top$是自由度$P$的Wishart矩阵，噪声项为$\sigma^2N/(P-N-1)$。极限为$r^2(1-1/\gamma)+\sigma^2/(\gamma-1)$。信号和噪声均为1、$\gamma>1$时等于$1+1/[\gamma(\gamma-1)]>1$，高于零预测超额风险；$\gamma=1/2$时超额风险为1。总均方误差还需加新噪声方差1。较强信号$r^2>\sigma^2$下，$\gamma>r^2/(r^2-\sigma^2)$时可优于零预测，因此单位信号例子的结论并不普遍。

## Current visual review

Visual pass complete on `quantitative-finance`: 36 bilingual endpoint sheets, 18 English forty-frame motion sheets and 20 focused native frames actually inspected on source `bd34d3801908edd6d4501ce57cc8120cea063e27`. The chaptered silent timing preview runs 61:04, with 18 chapters and English subtitles. Eleven CPU speech reports cover 80 sampled lines; the actual narrated opening runs 197.933 seconds. Signal/image checks do not certify pronunciation or continuous production listening, which remain pending. [Artifact-bound evidence](../../../docs/qa/quant27-polish-evidence.json).

## 当前视觉审阅

本轮已实际检查36张双语旁白节点画面表、18张英文四十帧动画表和20张重点原尺寸画面。分章静音时序预览为61:04，含18章和英文字幕。十一份CPU语音报告覆盖80个抽样句段，并核验实际配音开场。预训练迁移在首个SPY公开输入冻结哈希不符时停止，数值结果保持缺失；固定模拟示意不是替代历史策略。信号与画面检查不替代完整成片连续听审或发音认证，后者仍单独待办。
