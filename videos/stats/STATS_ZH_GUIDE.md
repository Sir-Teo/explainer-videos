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
