# Chinese edition of *Statistics, Built* (统计学，从零搭建)

Translations will live in `videos/stats/statsN/narration_zh.json`, keyed by the English line, and each part's
`zh_lines.py` translates the lines computed from data as templates. On-screen text lives in
`videos/stats/stats_text_zh.json` (`python tools/collect_text.py --check statsN`). The conventions are *AI, Built*'s
([`../ai/AI_ZH_GUIDE.md`](../ai/AI_ZH_GUIDE.md)):

- Spoken Mandarin, short sentences; same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; numbers as digits (169.50 厘米, 38,910); Latin symbols stay Latin (θ, x̄, n, r).
- Spoken math: θ帽 (theta hat), x拔 (x-bar), 对i求和, 至多, 当且仅当, n分之1.
- People's names in the standard Chinese form on first mention, with the original in brackets where it helps
  (格朗特 Graunt, 凯特勒 Quetelet, 高尔顿 Galton, 皮尔逊 Pearson, 费希尔 Fisher, 奈曼 Neyman).
- Book and paper titles in 《》.

## Glossary (Part 1; extended part by part)

| English | 中文 |
|---|---|
| statistics | 统计学 |
| population / sample | 总体 / 样本 |
| parameter / statistic | 参数 / 统计量 |
| estimate, estimator | 估计值，估计量 |
| the World (the simulated population) | 模拟世界（“世界”） |
| the Coverage Board | 覆盖率记分板 |
| the Museum (historical data) | 数据博物馆 |
| the Transcript | 成绩单 |
| Bills of Mortality | 死亡统计表 |
| life table | 生命表 |
| dot plot | 点图 |
| histogram | 直方图 |
| bin, bin width | 组，组距 |
| density | 密度 |
| mean / median / mode | 均值 / 中位数 / 众数 |
| midrange | 中程数 |
| loss function | 损失函数 |
| Fréchet mean | 弗雷歇均值 |
| deviation | 离差 |
| variance / standard deviation | 方差 / 标准差 |
| median absolute deviation (MAD) | 中位数绝对偏差 |
| interquartile range (IQR) | 四分位距 |
| Chebyshev's inequality | 切比雪夫不等式 |
| empirical distribution function (ECDF) | 经验分布函数 |
| quantile, percentile, quartile | 分位数，百分位数，四分位数 |
| five-number summary | 五数概括 |
| box plot | 箱线图 |
| outlier | 离群值 |
| skewness / kurtosis | 偏度 / 峰度 |
| heavy tail | 重尾 |
| power law, Pareto tail | 幂律，帕累托尾 |
| Hill estimator | 希尔估计量 |
| QQ plot | QQ图（分位数–分位数图） |
| location–scale family | 位置–尺度族 |
| transformation | 变换 |
| Box–Cox transformation | Box–Cox变换 |
| log-likelihood | 对数似然 |
| Jacobian | 雅可比因子 |
| variance stabilization | 方差稳定化 |
| delta method | delta方法 |
| scatter plot | 散点图 |
| covariance / correlation | 协方差 / 相关系数 |
| Cauchy–Schwarz inequality | 柯西–施瓦茨不等式 |
| restriction of range | 全距限制 |
| Anscombe's quartet | 安斯库姆四重奏 |
| simulated annealing | 模拟退火 |
| Simpson's paradox | 辛普森悖论 |
| confounder | 混杂因素 |
| ecological fallacy | 生态谬误 |
| lie factor | 谎言因子 |
| sampling distribution | 抽样分布 |
| standard error | 标准误 |
| confidence interval | 置信区间 |
| coverage | 覆盖率 |

## Glossary (Part 2)

| English | 中文 |
|---|---|
| the problem of points | 点数问题（赌金分配问题） |
| expected value, expectation | 期望值，期望 |
| classical probability | 古典概率 |
| equally likely | 等可能 |
| sample space, outcome, event | 样本空间，结果，事件 |
| permutation / combination | 排列 / 组合 |
| stars and bars | 隔板法（星与杠） |
| Pascal's triangle | 帕斯卡三角形（杨辉三角） |
| Bertrand's paradox | 贝特朗悖论 |
| Kolmogorov's axioms | 柯尔莫哥洛夫公理 |
| σ-algebra | σ-代数 |
| countable additivity | 可数可加性 |
| inclusion–exclusion | 容斥原理 |
| union bound | 并集上界（布尔不等式） |
| Bonferroni inequalities | 邦费罗尼不等式 |
| derangement, the hat-check problem | 错排，帽子问题 |
| conditional probability | 条件概率 |
| multiplication rule | 乘法法则 |
| law of total probability | 全概率公式 |
| Bayes' theorem | 贝叶斯定理 |
| prior / posterior odds | 先验 / 后验几率 |
| likelihood ratio | 似然比 |
| sensitivity / specificity / prevalence | 灵敏度 / 特异度 / 患病率 |
| natural frequencies | 自然频数 |
| prosecutor's fallacy | 检察官谬误 |
| Monty Hall problem | 蒙提霍尔问题（三门问题） |
| independent, pairwise / mutually | 独立，两两独立 / 相互独立 |
| conditional independence | 条件独立 |
| random variable | 随机变量 |
| distribution, push-forward | 分布，推前测度 |
| cumulative distribution function (CDF) | 累积分布函数 |
| discrete / continuous / mixed / singular | 离散 / 连续 / 混合 / 奇异 |
| the Cantor distribution, devil's staircase | 康托尔分布，魔鬼阶梯 |
| law of the unconscious statistician (LOTUS) | 无意识统计学家定律 |
| linearity of expectation | 期望的线性性 |
| indicator | 示性变量 |
| coupon collector | 赠券收集问题 |
| covariance | 协方差 |
| St. Petersburg paradox | 圣彼得堡悖论 |
| utility | 效用 |
| probability generating function | 概率母函数 |
| Sicherman dice | 西克曼骰子 |
| frequentist / Bayesian | 频率学派 / 贝叶斯学派 |
| Dutch book, coherence | 荷兰赌，融贯性 |
| Cox's theorem | 考克斯定理 |

## Glossary (Part 3)

| English | 中文 |
|---|---|
| Bernoulli / binomial | 伯努利 / 二项分布 |
| law of rare events (law of small numbers) | 稀有事件定律（小数定律） |
| Poisson distribution, Poisson process | 泊松分布，泊松过程 |
| total variation distance | 全变差距离 |
| Le Cam's inequality | 勒卡姆不等式 |
| geometric / negative binomial | 几何分布 / 负二项分布 |
| memorylessness | 无记忆性 |
| first-step analysis | 首步分析 |
| hypergeometric | 超几何分布 |
| capture–recapture | 捕获–再捕获法（标记重捕法） |
| exponential / gamma | 指数分布 / 伽马分布 |
| superposition / thinning | 叠加 / 稀疏化 |
| inspection paradox, length-biased sampling | 检查悖论，长度偏倚抽样 |
| normal distribution, Stirling's formula | 正态分布，斯特林公式 |
| change of variables, Jacobian | 变量替换，雅可比行列式 |
| Box–Muller transform | Box–Muller变换 |
| log-normal | 对数正态分布 |
| chi-squared / Student's t / F | 卡方分布 / 学生t分布 / F分布 |
| Cauchy distribution | 柯西分布 |
| order statistics, beta distribution | 次序统计量，贝塔分布 |
| the German tank problem | 德国坦克问题 |
| Pareto / Zipf's law | 帕累托分布 / 齐普夫定律 |
| moment generating function / characteristic function | 矩母函数 / 特征函数 |
| mixture, overdispersion | 混合分布，过度离散 |
| beta-binomial | 贝塔二项分布 |
| law of total variance | 全方差公式 |
| exponential family, natural parameter, sufficient statistic, log-normalizer | 指数族，自然参数，充分统计量，对数配分函数 |

## Glossary (Part 4)

| English | 中文 |
|---|---|
| hat matrix | 帽子矩阵 |
| projection (orthogonal), idempotent | （正交）投影，幂等 |
| column space, orthogonal complement | 列空间，正交补 |
| degrees of freedom | 自由度 |
| Gram–Schmidt, QR decomposition | 格拉姆–施密特正交化，QR分解 |
| trace, cyclic property | 迹，循环性 |
| leverage | 杠杆值 |
| spectral theorem, eigenvalue, eigenvector | 谱定理，特征值，特征向量 |
| quadratic form, Rayleigh quotient | 二次型，瑞利商 |
| Mahalanobis distance, whitening | 马氏距离，白化 |
| power iteration | 幂迭代法 |
| positive (semi)definite | 正定（半正定） |
| Cholesky decomposition | 楚列斯基分解 |
| Loewner order | 勒夫纳序 |
| generalized variance | 广义方差 |
| singular value decomposition (SVD), low-rank approximation | 奇异值分解，低秩逼近 |
| Moore–Penrose pseudoinverse, minimum-norm solution | 摩尔–彭罗斯伪逆，最小范数解 |
| dummy-variable trap, estimable function | 虚拟变量陷阱，可估函数 |
| ridge regression | 岭回归 |
| Schur complement, block matrix | 舒尔补，分块矩阵 |
| Woodbury identity, Sherman–Morrison formula | 伍德伯里恒等式，谢尔曼–莫里森公式 |
| Frisch–Waugh–Lovell theorem | 弗里施–沃–洛弗尔定理 |
| leave-one-out residual, PRESS | 留一残差，预测残差平方和 |
| Kronecker product, vec operator | 克罗内克积，向量化算子 |
| matrix calculus, gradient, Hessian | 矩阵微积分，梯度，黑塞矩阵 |
| score, Fisher information | 得分函数，费希尔信息 |
| Cochran's theorem | 科克伦定理 |
| noncentral chi-squared, power | 非中心卡方分布，检验功效 |
| condition number, floating point | 条件数，浮点数 |
| catastrophic cancellation | 灾难性抵消 |

## Glossary (Part 5)

| English | 中文 |
|---|---|
| joint, marginal, conditional distribution | 联合分布，边缘分布，条件分布 |
| mid-parent | 双亲平均身高 |
| regression towards mediocrity, regression to the mean | 向平庸回归，均值回归 |
| uncorrelated, independent; pairwise, mutually independent | 不相关，独立；两两独立，相互独立 |
| covariance matrix, inner product | 协方差矩阵，内积 |
| diversification | 分散化 |
| conditional expectation, best predictor | 条件期望，最优预测 |
| tower property (law of total expectation) | 塔性质（全期望公式） |
| Eve's law (law of total variance) | 夏娃定律（全方差公式） |
| correlation ratio η² | 相关比 η² |
| conditional median, conditional quantile, quantile regression | 条件中位数，条件分位数，分位数回归 |
| multivariate normal, jointly normal | 多元正态分布，联合正态 |
| Cramér–Wold device | 克拉默–沃尔德方法 |
| precision matrix, partial correlation, conditional independence | 精度矩阵，偏相关，条件独立 |
| covariance selection, graphical model | 协方差选择，图模型 |
| major axis, errors in variables, regression dilution | 主轴，变量含误差模型，回归稀释 |
| reliability ratio, correction for attenuation | 信度比，衰减校正 |
| change of variables, Jacobian, convolution | 变量替换，雅可比行列式，卷积 |
| Rayleigh distribution | 瑞利分布 |
| latent variable, mixture model, latent class | 潜变量，混合模型，潜在类别 |
| Simpson's paradox | 辛普森悖论 |
| copula, Sklar's theorem, tail dependence | 联结函数（copula），斯克拉定理，尾部相依 |
| Gaussian, Clayton, Gumbel copula | 高斯、克莱顿、冈贝尔 copula |
| exchangeability, de Finetti's theorem | 可交换性，德菲内蒂定理 |
| Pólya's urn | 波利亚罐子模型 |
| Spearman's rho, Kendall's tau | 斯皮尔曼秩相关系数，肯德尔 τ |
| distance correlation, mutual information | 距离相关，互信息 |
| simplex, multinomial, Dirichlet distribution | 单纯形，多项分布，狄利克雷分布 |
| conjugacy | 共轭性 |
| spurious correlation, compositional data, log-ratio | 伪相关，成分数据，对数比 |

## Glossary (Part 6)

| English | 中文 |
|---|---|
| the wisdom of crowds, vox populi | 群体智慧，民意 |
| Markov's inequality, Chebyshev's inequality, Jensen's inequality | 马尔可夫不等式，切比雪夫不等式，詹森不等式 |
| convex function | 凸函数 |
| law of large numbers (weak, strong) | （弱、强）大数定律 |
| the gambler's fallacy | 赌徒谬误 |
| convergence in probability, in distribution, almost surely, in mean square | 依概率收敛，依分布收敛，几乎必然收敛，均方收敛 |
| central limit theorem | 中心极限定理 |
| Galton board (quincunx) | 高尔顿板（梅花机） |
| convolution power | 卷积幂 |
| de Moivre–Laplace theorem, continuity correction | 棣莫弗–拉普拉斯定理，连续性校正 |
| Lindeberg condition | 林德伯格条件 |
| Berry–Esseen theorem | 贝里–埃森定理 |
| delta method, variance-stabilizing transformation | Delta 方法，方差稳定变换 |
| Slutsky's theorem, continuous mapping theorem | 斯卢茨基定理，连续映射定理 |
| consistent estimator | 相合估计量 |
| heavy tail, stable law, generalized CLT | 重尾，稳定分布，广义中心极限定理 |
| concentration inequality, Hoeffding's inequality, Chernoff bound | 集中不等式，霍夫丁不等式，切尔诺夫界 |
| union bound | 联合界（布尔不等式） |
| large deviations, rate function | 大偏差，速率函数 |
| extreme value theory, GEV distribution | 极值理论，广义极值分布 |
| Gumbel, Fréchet, Weibull distributions | 冈贝尔分布，弗雷歇分布，韦布尔分布 |
| return level, return period | 重现水平，重现期 |
| profile likelihood | 剖面似然 |

## Glossary (Part 7)

| English | 中文 |
|---|---|
| pseudo-random number generator, seed, period | 伪随机数生成器，种子，周期 |
| linear congruential generator, lattice, spectral test | 线性同余生成器，格结构，谱检验 |
| middle-square method | 平方取中法 |
| Mersenne Twister, PCG | 梅森旋转算法，PCG 生成器 |
| independent streams | 独立随机数流 |
| inverse-CDF (inversion) method | 逆变换法 |
| rejection sampling, envelope, acceptance rate | 拒绝抽样，包络函数，接受率 |
| adaptive rejection sampling, log-concave | 自适应拒绝抽样，对数凹 |
| Box–Muller transform | Box–Muller 变换 |
| alias method | 别名法 |
| Monte Carlo integration, Monte Carlo standard error | 蒙特卡洛积分，蒙特卡洛标准误 |
| quasi-Monte Carlo, low-discrepancy sequence | 拟蒙特卡洛，低差异序列 |
| Buffon's needle | 布丰投针 |
| simulation study (ADEMP) | 模拟研究（ADEMP） |
| antithetic variates, control variates, stratified sampling, importance sampling | 对偶变量，控制变量，分层抽样，重要性抽样 |
| Markov chain, transition matrix | 马尔可夫链，转移矩阵 |
| stationary distribution, detailed balance, reversible | 平稳分布，细致平衡，可逆 |
| irreducible, aperiodic, ergodic theorem | 不可约，非周期，遍历定理 |
| random walk on a graph, PageRank | 图上的随机游走，PageRank |
| riffle shuffle, total variation distance, cutoff phenomenon | 鸽尾洗牌，全变差距离，截断现象 |
| mixing time | 混合时间 |
| Metropolis algorithm, Gibbs sampling, MCMC | Metropolis 算法，吉布斯抽样，马尔可夫链蒙特卡洛 |
