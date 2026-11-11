"""Chinese narration for quant7; literal prefixes and computed-line templates."""

TITLE = '量化金融，从零搭建 · 第7部分：时间序列与波动率'

CHAPTERS = {
    'Research':
        '写给研究者：比较嵌套的预测',
    'Hook':
        '噪声之下的河流',
    'Arma':
        '1. 平稳性、ARMA与博克斯–詹金斯方法',
    'Series':
        '2. 单位根与伪回归',
    'Coint':
        '3. 协整',
    'Regimes':
        '4. 隐藏机制',
    'Kalman':
        '5. 卡尔曼滤波与随机波动率',
    'Garch':
        '6. 用最大似然估计ARCH与GARCH',
    'Zoo':
        '7. 平稳性、厚尾与不对称：GARCH家族',
    'Dcc':
        '8. 会变的相关性',
    'Realized':
        '9. 已实现波动率',
    'Har':
        '10. 跳跃与HAR',
    'Rough':
        '11. 波动率是粗糙的吗？',
    'Scoring':
        '12. 诚实地给预测评分',
    'Training':
        '13. 训练神经网络',
    'Race':
        '14. 竞赛',
    'Frontier':
        '15. 基础模型与前沿',
    'March':
        '16. 2020年3月',
    'Industry':
        '17. 业界：为钱而做的波动率预测',
    'House':
        '18. 波动率预测器',
    'Outro':
        '回顾、交易台问题与习题',
}

ZH = {
    'Part seven. Time series and volatility.':
        '第7部分。时间序列与波动率。第1部分发现收益的线性依赖较弱，幅度的持续性更强。本部分建立风险预测模型并作比较。',
    'Almost a century of the American market':
        "这是美国市场近一个世纪的走势，每柱是每五个交易日采一次、共四个日波动的均方根，约一柱一个交易月。<bookmark mark='a'/>大的波动不会单独到来。它们成簇出现：三十年代初、1987、2008、2020年3月。贝努瓦·曼德布罗特在1963年从棉花价格中看到了这一点：大的变化之后往往跟着大的变化，涨跌皆有。<bookmark mark='b'/>那么，暂停一下，预测看看。你能预测明天的方向吗？你能预测明天的幅度吗？<bookmark mark='c'/>这条亮线就是这些成簇现象所暗示的那个缓慢、隐藏的量：波动率。",
    'f"The data answer. Correlate each day':
        "数据给出的答案：把收益与滞后收益求相关。<bookmark mark='a'/>这个美国样本中的线性相关较小，一阶为{r_[0]:.2f}。这不证明方向不可预测，也不排除交易信号。<bookmark mark='b'/>绝对收益的一阶相关为{ab[0]:.2f}，一百个交易日后仍为{ab[-1]:.2f}。幅度的持续性更强，但样本中衰减慢不能单独证明数学上的长记忆。",
    'The same holds in a market that never closes.':
        "在一个从不休市的市场中也能看到聚集。这是三年半的比特币。<bookmark mark='a'/>五分钟收益给出每日波动率测量，每天一个带噪声的点。<bookmark mark='b'/>卡尔曼滤波追踪较慢的水平；参数使用全样本，所以这是回顾性演示。预测条件风险并不要求预测每天的方向，期权定价、风险限额和仓位都依赖风险预测。",
    'How we got here. In 1927 Udny Yule':
        "我们是怎么走到这里的。1927年，乌德尼·尤尔把太阳黑子数建模为一个记得自己过去的序列：第一个自回归。1960年，鲁道夫·卡尔曼发表了针对隐藏状态的滤波器。1970年博克斯和詹金斯把建模变成一门手艺，1979年迪基和富勒给出了随机游走的检验。<bookmark mark='a'/>然后是波动率：1982年恩格尔的ARCH，1986年博勒斯列夫的GARCH，1987年恩格尔和格兰杰的协整，1989年汉密尔顿的机制转换。<bookmark mark='b'/>1994年，摩根大通免费发布了RiskMetrics。日内数据让波动率变得可以测量，2003年恩格尔和格兰杰分享了诺贝尔奖。<bookmark mark='c'/>2009年的HAR，2018年的粗糙波动率，以及2024年以来的基础模型。每一个都有自己的一章。",
    'The plan. Time-series foundations':
        '本部分的安排。时间序列基础：ARMA、单位根与协整。隐藏状态。GARCH家族，推导并拟合。已实现波动率、HAR与粗糙性。然后是评分、在这里训练的神经网络、竞赛和基础模型。还有2020年3月，以及业界的做法。',
    'In the House, this part builds the volatility forecaster':
        "在我们的公司里，本部分搭建波动率预测器：测量方法、模型和评分规则。<bookmark mark='a'/>第10部分波动率交易台开张时，用的就是这台引擎。",
    'Chapter one. Stationarity, ARMA models':
        '第1章。平稳性、ARMA模型与博克斯–詹金斯方法。',
    'The simplest series that remembers':
        "最简单的有记忆的序列：保留昨天值的比例phi，加一个新冲击。phi为零时是纯噪声。<bookmark mark='a'/>调到一半，自相关按phi的滞后次幂衰减。<bookmark mark='b'/>调到0.9，摆动变长，方差约增至五倍。<bookmark mark='c'/>到0.99，冲击约需七十步减半。它像被冲击推动的弹簧球。在独立单位方差冲击、平稳初始分布和phi绝对值小于1的条件下，均值、方差不随时间改变，协方差只依赖滞后。",
    'Why those numbers. Substitute the recursion':
        "这些数从哪里来？反复代入，序列成为过去冲击的加权和。<bookmark mark='a'/>独立冲击的方差相加，得到几何级数。<bookmark mark='b'/>乘以滞后值取期望，自相关就是phi的滞后次幂。<bookmark mark='c'/>向前迭代得到预测；此半衰期公式用于phi在0与1之间。<bookmark mark='d'/>Ljung与Box把残差自相关平方相加：在适当白噪声假设下渐近服从卡方分布，拟合ARMA后须调整自由度。<bookmark mark='e'/>Wold证明，纯非确定性的协方差平稳序列可写成过去新息的移动平均；ARMA把权重写得紧凑。",
    'How do you tell which model you have?':
        "如何识别模型？看指纹。AR模型的自相关衰减，控制较短滞后后的偏自相关在p阶后截尾；MA模型则是自相关在q阶后截尾。<bookmark mark='a'/>Box和Jenkins把它变成循环：识别候选、估计、用Ljung--Box检查残差。单个检验不拒绝并不证明独立。频谱在频域携带相同的二阶信息，这里留在时域。",
    'f"Lab. The House\'s autoregression':
        "实验。我们公司的自回归：滞后值加最小二乘。把它用在VIX的对数上，1990到2020年共{a['n_vix']:,}个交易日。<bookmark mark='a'/>phi是{a['ar1_phi']:.3f}：恐惧以约{a['ar1_half_life']:.0f}个交易日的半衰期消退。",
    'f"Let the Akaike criterion choose':
        "让AIC在这组候选模型中选择。ARMA({best['p']},{best['q']})胜出，但残差仍未通过Ljung--Box检验：这说明有限候选集合尚未解释所有序列相关，不能据此证明长记忆。<bookmark mark='a'/>九十四年日收益的Q为{lb['r']['Q']:.0f}，平方收益为{lb['sq']['Q']:,.0f}，约大{ratio:.0f}倍。幅度的依赖明显更强。<bookmark mark='b'/>暂停预测：phi从下方接近1时，方差和半衰期怎样？都趋于无穷，这就是下一章。",
    'Chapter two. Unit roots, and the regression that lies.':
        '第2章。单位根，以及会说谎的回归。',
    'Let phi reach one, and the spring snaps.':
        "让phi达到1，弹簧断了。左边是六十条平稳路径，包络为逐时点正负两个标准差，不是整条路径的边界。<bookmark mark='a'/>右边是相同冲击产生的随机游走，每次冲击永久留下，包络按时间平方根扩张。这是单位根，可作为对数价格的基准模型，而不是每种价格都已被证明的事实。",
    'f"To test for a unit root':
        "检验单位根：把变化量对常数项和昨天的水平回归，看系数的t统计量。单位根下它不是正态。两万条模拟随机游走的统计量堆积起来；两端受截断归箱影响的柱省略，密度仍按全部抽样次数归一。<bookmark mark='a'/>均值约{u['mean']:.1f}，用正态的负1.645临界值会拒绝{100 * u['share_below_1645']:.0f}%。<bookmark mark='b'/>本设定的5%分位点约{q05:.2f}；带常数、无趋势使用对应的迪基--富勒表。",
    'Why it is not normal.':
        "为什么不服从正态？与模拟一样拟合常数项。平方随机游走并求和，再减去滞后水平的均值乘最终水平。<bookmark mark='a'/>按样本量平方根缩放，唐斯克定理给出布朗运动；对回归变量去均值得到W mu。<bookmark mark='b'/>系数乘T的极限是布朗路径函数的比值。<bookmark mark='c'/>t统计量也有非正态极限。<bookmark mark='d'/>分子还要减去最终布朗值乘路径平均值。这才是带常数项、无趋势的迪基--富勒极限，与模拟一致；加入趋势又会改变分布。",
    'f"Lab. The House\'s test':
        "实验。我们公司的检验：把变化量对常数、昨天的水平和五个滞后变化量回归，再把t统计量与负二点八六比较。在四个序列上运行。<bookmark mark='a'/>先暂停预测一下：十年期国债收益率不可能涨到无穷。它有单位根吗？<bookmark mark='b'/>比特币的对数价格和股市的对数指数：未拒绝单位根原假设。{y10_line}至于VIX：{vix_line}",
    'The ten-year yield: over sixty years the test cannot tell':
        '十年期收益率：六十年的数据里，检验无法把它和随机游走区分开。未拒绝不等于证明单位根：当phi接近一时，检验的功效很低。',
    'f"Unit roots matter because':
        "单位根之所以重要，是因为把一个游走的序列对另一个回归是个陷阱。克莱夫·格兰杰和保罗·纽博尔德在1974年证明了这一点。取两千对彼此毫无关系的随机游走，把一个对另一个回归。其中{100 * s['rej_levels']:.0f}%的t统计量超过二。用变化量回归，是百分之五，本该如此。<bookmark mark='a'/>彼得·菲利普斯在1986年证明了原因：在水平上，斜率并不收敛到零，而是收敛到一个随机数，所以随着样本增大，t统计量按T的平方根增长。从五十天到两千天，它增长了{grow:.1f}倍。<bookmark mark='b'/>数据越多，谎言越自信。<bookmark mark='c'/>比特币对美国股市，用对数水平：t统计量二十四。用日变化量，联系是真实的但很弱：只解释百分之五的方差，大部分来自2020年。",
    'Chapter three. Cointegration.':
        '第3章。协整。',
    'f"In 1994 Michael Murray':
        "Murray在1994年用醉汉与狗解释协整：醉汉是随机游走，狗跟随她，追踪误差平稳。<bookmark mark='a'/>两者的位置都能漂移。<bookmark mark='b'/>检验使用东西向坐标之差，其ADF为{j['adf_gap']:.1f}，醉汉位置为{j['adf_drunk']:.1f}。不拒绝本身不能证明单位根，但模拟构造已知。协整指I一序列存在平稳线性组合；欧氏距离的牵绳只是相关的非线性图像。",
    'f"A real leash.':
        "真实的牵绳。现货和永续价格的ADF未拒绝单位根，I一是工作假设。<bookmark mark='a'/>2020年的基差更稳定，包括三月危机。使用对应临界值的Engle--Granger残差检验拒绝单位根。<bookmark mark='b'/>按拟合AR系数{rho:.2f}，今天偏离拟合均值20基点，明天的条件期望约偏离{20 * rho:.0f}基点。这不是保证盈利的交易；资金费率和套利把价格联系起来。",
    'The algebra. Two series are cointegrated':
        "代数上，I一序列的某个线性组合平稳就是协整。<bookmark mark='a'/>在表示定理的常规条件下，对应一个误差修正模型。<bookmark mark='b'/>两变量、常数项、无趋势的残差检验，其渐近5%临界值约为负3.34，不能套普通ADF表。<bookmark mark='c'/>多变量用VECM的降秩矩阵表示。<bookmark mark='d'/>先剔除滞后差分和确定性项，再由变化量与滞后水平的典型相关计算迹检验。",
    'f"Johansen\'s test, made visible.':
        "把约翰森检验画出来：1990至2020年的三个月、五年和十年国债收益率，每天一个三维点。<bookmark mark='a'/>主要方向描述利率水平。<bookmark mark='b'/>侧看云团很薄，但PCA薄度不是协整证明，也不必等于估计的协整向量。<bookmark mark='c'/>在常数、无趋势、两阶VAR的设定下，迹检验给出条件性的秩结论。{hag}Hall、Anderson和Granger在1992年研究过国库券期限之间的协整。第19部分讲收益率曲线，第33部分讲配对交易；下一章是隐藏机制。",
    'Here the test finds a different structure':
        '这里检验找到的结构与经典结果不同。',
    'Chapter four. Hidden regimes.':
        '第4章。隐藏机制。',
    'Volatility is hidden; we only see its effects.':
        "波动率是隐藏的，我们只看得到它的效果。建模的一种方法是少数几个隐藏状态。1989年，詹姆斯·汉密尔顿让经济按马尔可夫链在机制之间切换，每个机制有自己的均值和波动率。想象两个装着信念的罐子：平静和风暴。<bookmark mark='a'/>每个月发生两件事。第一，预测：一点液体在两个罐子之间渗漏，因为机制可能改变。<bookmark mark='b'/>然后这个月的收益落下，每个罐子按这个收益在其机制下的可能性被重新缩放，也就是这两条钟形曲线，总量再倒回到一升。<bookmark mark='c'/>看它走过1929年。每一次大的月度波动都把信念推向风暴，而且停在那里。<bookmark mark='d'/>参数使用全样本拟合，因此这是回顾性滤波；让它跑完整个世纪，它画出的红色区域照亮了大萧条、1974、1987、2008和2020年。",
    'f"In symbols. The update is Bayes':
        "用符号写出来。更新就是贝叶斯法则：把预测概率乘以每个机制下收益的密度，再归一化。<bookmark mark='a'/>预测是乘以转移矩阵。<bookmark mark='b'/>一个每月以概率p持续的机制，持续的月数服从几何分布，均值为一除以一减p。<bookmark mark='c'/>处于风暴中的长期比例，使流入和流出相互平衡。<bookmark mark='d'/>用拟合出的概率，平静期平均持续约{1 / (1 - P[0, 0]):.0f}个月，风暴约{1 / (1 - P[1, 1]):.0f}个月，市场约有{100 * r['pi_storm']:.0f}%的时间处于风暴中。",
    'f"How are the regimes found?':
        "这些机制是怎么找到的？用期望最大化：猜两个机制，运行滤波器和平滑器得到每个月的概率，用这些概率加权的月份重新估计每个机制的均值和波动率，然后重复。精确EM步骤不降低似然，但可能收敛到局部最优。<bookmark mark='a'/>在九十四年的月度收益上，前几轮取得大部分似然增益，此后仍继续收敛：一个平静机制，年均值{100 * mu[0]:+.0f}%，波动率{100 * sd[0]:.0f}%；一个风暴机制，均值{100 * mu[1]:.0f}%，波动率{100 * sd[1]:.0f}%。<bookmark mark='b'/>暂停预测一下。模型确信现在很平静时，来了一个负百分之八的月份。风暴罐子会被装满吗？<bookmark mark='c'/>{answer}",
    'f"No. It rises from':
        "不会。它从{100 * r['prior_storm']:.0f}%升到{100 * r['post_storm_m8']:.0f}%：一个坏月份还不是风暴，证据需要积累。",
    'Chapter five. The Kalman filter, and stochastic volatility.':
        '第5章。卡尔曼滤波与随机波动率。',
    "Kalman's filter of 1960 does for a continuous hidden state":
        "卡尔曼滤波器用一个钟形分布描述隐藏的连续状态：中心是估计，宽度是不确定性。<bookmark mark='a'/>预测：隐藏水平可能漂移，分布变宽。<bookmark mark='b'/>观测到已实现波动率，它带有测量噪声。<bookmark mark='c'/>在独立高斯状态与测量噪声假设下，将两钟形曲线相乘并归一化，得到更窄的后验，中心向测量移动K比例。<bookmark mark='d'/>每天重复：预测、观测、更新。",
    'f"The derivation. The hidden level drifts':
        "推导。隐藏水平以方差q漂移，测量加入方差为r的噪声，预测就是加上q。<bookmark mark='a'/>贝叶斯把先验乘以测量的似然，<bookmark mark='b'/>配方给出规则：精度相加，均值按增益K移动，K等于先验方差除以先验方差加噪声。<bookmark mark='c'/>在稳态下，每晚的变宽和每天的变窄相互平衡，增益只取决于信噪比。比特币对数波动率的信噪比约为{k['snr']:.2f}，所以每天信念向新测量值移动{100 * k['K_ss']:.0f}%。<bookmark mark='d'/>暂停预测一下：如果测量更嘈杂，信念会移动得更多还是更少？更少：r上升，信噪比下降，K沿曲线滑下去。",
    "Lab. Here is the House's filter":
        "实验。四行循环：扩散、增益、拉近、收窄。q、r以及初始不确定性使用整个研究样本估计，因此这是回顾性的滤波演示，不是实时回测。<bookmark mark='a'/>在比特币日对数波动率上运行，画出河流和模型内的不确定性带。",
    'f"The same filter gives a model of volatility.':
        "同一个滤波器还给出一个波动率模型。让对数方差成为一个隐藏的自回归：随机波动率。<bookmark mark='a'/>平方收益是它一个非常嘈杂的测量。取对数后，在标准正态收益冲击假设下，对数平方噪声有这些已知矩。安德鲁·哈维、埃丝特·鲁伊斯和尼尔·谢泼德在1994年把它当作高斯噪声，卡尔曼滤波器对非高斯的对数卡方噪声给出高斯准似然。<bookmark mark='b'/>在九十四年的日收益上，phi是{sv['phi']:.3f}：半衰期约{sv['half_life']:.0f}个交易日。平滑后的波动率跟随下一章的GARCH模型，{track}两个截然不同的模型，同一条隐藏的河。",
    "f'closely, with a correlation of":
        "相当接近，相关系数为{k['corr_sv_garch']:.2f}。",
    'Chapter six. ARCH and GARCH, by maximum likelihood.':
        '第6章。用最大似然估计ARCH与GARCH。',
    'Robert Engle, on a sabbatical at the London School of Economics':
        "恩格尔想描述英国通胀的不确定性，1982年提出ARCH：今天冲击的方差取决于昨天的冲击。<bookmark mark='a'/>把方差想成桶里的水：omega持续注水，每晚保留beta比例。<bookmark mark='b'/>每天按水位平方根的尺度抽取收益，再把alpha乘收益平方溅回桶里。<bookmark mark='c'/>运行后，聚集自然出现。在omega为正、系数非负且alpha加beta小于1、冲击条件方差为1时，条件期望回归有限长期方差；单条路径仍不断受到冲击。",
    'The equations behind the bucket.':
        "桶背后的方程。收益等于波动率乘单位条件方差冲击，博勒斯列夫让方差也记住自身。<bookmark mark='a'/>在正参数和alpha加beta小于1等条件下，长期方差是omega除以1减alpha减beta。<bookmark mark='b'/>展开得过去平方收益的指数加权和。<bookmark mark='c'/>高斯冲击下得到似然，非正态时作为准似然。<bookmark mark='d'/>方差的条件期望按alpha加beta回归。<bookmark mark='e'/>平方收益有ARMA代数恒等式；要作协方差ARMA解释还需四阶矩有限。这也解释了平方收益强烈的序列依赖。",
    'f"Lab. The House\'s GARCH':
        "实验。我们公司的GARCH是五行递推加一行似然，其余交给优化器。<bookmark mark='a'/>在美国市场的{g['n']:,}个交易日上，alpha约为十分之一，beta约为十分之九。<bookmark mark='b'/>暂停预测一下：alpha加beta是{us['garch']['persistence']:.3f}。一个冲击之后，要多少天才会消退一半？<bookmark mark='c'/>{us['garch']['half_life']:.0f}个交易日，大约三个月。这是拟合出的波动率，一天一天地画过整个世纪。",
    'f"What did the optimiser do?':
        "优化器做了什么？用方差目标确定omega，画出alpha与持续性alpha加beta上的似然面。<bookmark mark='a'/>单纯形搜索经过{gl['n_iter']}次迭代，到达alpha为{P[-1][0]:.3f}、beta为{P[-1][1]:.3f}附近；轨迹投影到有限网格，读数保留实际点。<bookmark mark='b'/>不同方向的坡度不同，但精度比必须另算曲率或稳健协方差，不能只看图。<bookmark mark='c'/>RiskMetrics的EWMA在alpha加beta等于1、omega为0的边界，没有有限长期回归水平。下一章是GARCH家族。",
    'Chapter seven. Stationarity, fat tails and asymmetry':
        '第7章。平稳性、厚尾与不对称：GARCH家族。',
    'f"Every GARCH is a point on this plane.':
        "每个GARCH都是这个平面上的一个点。在alpha加beta等于一的线以下，方差是有限的。<bookmark mark='a'/>美国市场就在这条线下方，比特币更靠里一些。<bookmark mark='b'/>线的上方会怎样？丹尼尔·纳尔逊在1990年证明，即使无条件方差无限，也可能存在严平稳分布。只要alpha乘z平方加beta的对数的平均为负，过程就会稳定下来，而这条红色的边界位于那条线之外。<bookmark mark='c'/>暂停预测一下。alpha零点三加beta零点七五等于一点零五；零点二五加零点八也一样。在高斯冲击假设下，哪一个存在平稳分布？<bookmark mark='d'/>{verdict}",
    'The first is negative: the process is strictly stationary':
        '第一个为负：过程是严平稳的，它会稳定到一个分布，只是方差无穷。第二个为正：它会爆炸。同样的和，相反的命运。',
    'Both come out on the same side of zero here.':
        '这里两者落在零的同一侧。',
    'Why. Unrolled, the variance':
        "为什么？假定omega为正、系数非负，冲击独立同分布、非退化并满足对数可积性。展开方差是随机乘积之和。<bookmark mark='a'/>平均对数因子为负，乘积衰减并给出平稳解。<bookmark mark='b'/>alpha为正且平方冲击非恒定时，严格詹森不等式说明IGARCH也可严平稳，但无有限无条件方差。<bookmark mark='c'/>条件单位方差使高斯准似然得分均值为零。一致性还需识别与遍历等条件；正态三明治标准误还要求得分方差有限，极厚尾可能破坏它。<bookmark mark='d'/>GJR对下跌另加权重，其常用持续性公式假定冲击对称。<bookmark mark='e'/>EGARCH保证方差为正，但仍需平稳性约束。",
    'f"Draw tomorrow\'s variance against today\'s return':
        "把明天的方差画成今天收益的函数：新闻冲击曲线。对GARCH，它是一条对称的抛物线：同样大小的下跌和上涨算作一样。<bookmark mark='a'/>市场不这么看。费希尔·布莱克在1976年注意到，下跌之后波动率上升得更多。用GJR拟合美国市场，抛物线就倾斜了：下跌使明天方差上升的幅度，是同样大小上涨的{(a + gam) / a:.0f}倍。<bookmark mark='b'/>EGARCH在对数上工作，弯曲的方式不同，两者都比对称模型拟合得好得多。<bookmark mark='c'/>比特币背后没有公司杠杆，却显示出同样的倾斜：企业杠杆不能是唯一可能解释，但这个拟合不能单独识别原因。",
    'f"Last, the tails.':
        "最后，尾部。把每天的收益除以GARCH的波动率。如果冲击是正态的，这些标准化残差对着正态分位数应当落在对角线上。<bookmark mark='a'/>它们没有：两端翘开，峰度是{gl['kurt_z']:.1f}，不是三。GARCH解释了收益厚尾的一部分，不是全部。<bookmark mark='b'/>给冲击一个学生t分布并估计它的自由度：约{tg['nu']:.0f}。现在点变直了，对数似然上升了{tg['loglik'] - gl['g_loglik']:,.0f}。波动率路径几乎不变；变的是尾部，而尾部正是风险经理拿薪水要算对的东西。单一资产的波动率只是故事的一半。下一章：会变动的相关性。",
    'Chapter eight. Correlations that move.':
        '第8章。会变的相关性。',
    'Volatilities move, and so do correlations.':
        "波动率会变，相关性也会变。这里每年一个椭圆：美国股票的日收益横着画，十年期国债竖着画，从1962年开始。<bookmark mark='a'/>看它随波动率起落而呼吸，看它倾斜。在通胀的七十和八十年代，它向上倾：股票和债券一起下跌。<bookmark mark='b'/>2000年前后它先趋于竖直，然后向另一边倾斜：股票下跌时债券上涨。指针跟踪着相关性。符号翻转改善了分散化，但不是六四组合表现的唯一原因。",
    'f"How to model it.':
        "怎么建模。一百个资产的完整多元GARCH有五千多万个参数；即使受限的BEKK形式也有两万五千个。罗伯特·恩格尔2002年的动态条件相关只需要三百零二个动态系数，此外还有相关性目标矩阵的元素。<bookmark mark='a'/>把协方差拆成波动率和相关性。<bookmark mark='b'/>给每个资产拟合一个GARCH，然后对它们标准化冲击的乘积运行一个类似GARCH的递推，<bookmark mark='c'/>每天再重新缩放成一个真正的相关矩阵。<bookmark mark='d'/>似然一分为二，所以分两个简单的步骤估计。对股票和债券，b是{d['b']:.3f}：相关性冲击非常持久。",
    'f"Here is the fitted correlation day by day':
        "这是逐日拟合的相关性，灰色是一个普通的指数平均作对比：DCC的路径更平滑，因为它的记忆更长。较早时期大部分时间相关性为正：通胀同时伤害两者。然后它翻转了。<bookmark mark='a'/>暂停预测一下。2010年，你给六四组合的风险模型仍假设相关性为正零点三。固定已实现的边际波动率，只改变相关性假设，风险更高还是更低？这是回顾性的相关性比较。<bookmark mark='b'/>{verdict}2022年，在我们的时间窗之外，符号又翻转了。",
    'f"Safer. With the correlation at':
        "更小。相关性为{e['rho_2010']:+.2f}时，组合的波动率是{100 * e['real_6040']:.0f}%，而不是模型说的{100 * e['model_6040']:.0f}%。",
    'Chapter nine. Realized volatility.':
        '第9章。已实现波动率。',
    'Can volatility be measured after the fact?':
        "波动率能事后测量吗？这是比特币狂野的一天，逐分钟：2019年6月26日。<bookmark mark='a'/>把这一天切成半小时。每个半小时的收益得到一个正方形，边长是波动的大小，面积是它的平方。把面积加起来：这就是已实现方差。<bookmark mark='b'/>切得更细，十分钟，五分钟：正方形增加到六倍并且变小，而它们的总和变化小得多。<bookmark mark='c'/>在极限上，它就是第5部分的二次变差，即一天内瞬时方差的积分。安德森、博勒斯列夫、迪博尔德和拉比斯在2000年前后以此为基础：波动率变得可以观测。<bookmark mark='d'/>然而到了每分钟，总和又往上爬了。为什么？",
    'f"Build the answer point by point.':
        "一个点一个点地搭出答案。对2019年的每一天，分别以一小时、三十分钟，一直到一分钟的采样间隔计算已实现波动率，再取平均。<bookmark mark='a'/>间隔越小，线越高：2019年，一分钟采样比五分钟采样高{100 * rise:.1f}%。<bookmark mark='b'/>在整个样本上，算上2017和2018年较薄的市场，差距是{100 * rise_all:.0f}%。罪魁祸首是微观结构噪声：成交在买价和卖价之间来回弹跳，每一次弹跳都加上一个与波动率无关的小正方形。<bookmark mark='c'/>暂停预测一下：每秒采样会更好吗？不会：采样越频繁，加进来的弹跳越多。",
    'f"On three and a half years of Bitcoin':
        "在三年半的比特币数据中，一分钟测量的平均年化波动率为{100 * z['vol_rv1']:.0f}%，五分钟为{100 * z['vol_rv5']:.0f}%。<bookmark mark='a'/>两种噪声修正测量约为{100 * z['vol_tsrv']:.0f}%，双幂变差稍低。<bookmark mark='b'/>这里的区间使用连续、无噪声中心极限定理，不处理噪声和跳跃；负方差下界截为零。典型半宽约为方差的{100 * rel:.0f}%。已实现方差仍是带误差的测量。下一章用它建立HAR。",
    'Chapter ten. Jumps, and the HAR model.':
        '第10章。跳跃与HAR模型。',
    'f"Realized variance counts jumps too':
        "已实现方差也会把跳跃算进去：一次突然的波动，一个巨大的正方形。奥勒·巴恩多夫–尼尔森和尼尔·谢泼德找到了一个忽略它的测度。<bookmark mark='a'/>不是把每个收益平方，而是把它的大小乘以相邻收益的大小。跳跃和一个普通的邻居配对，所以它的长方形依然很细：双幂次变差只收敛到连续部分，它与已实现方差的差就是跳跃。<bookmark mark='b'/>他们2006年的检验把这个差变成一个z分数。<bookmark mark='c'/>在比特币的五分钟收益上，按百分之一的水平，{100 * s['jump_share_1pct']:.0f}%的日子出现跳跃。那么2020年3月12日呢？z是{s['z_0312']:.2f}。{verdict}",
    'With a measured variance every day':
        "每天有了方差测量，预测成为回归。Corsi的HAR使用昨天以及过去5、22个观测的平均。这是股票市场的交易周、月惯例；比特币每天交易，不能按日历周月理解。<bookmark mark='a'/>不同平均的变化速度不同。<bookmark mark='b'/>展开后是权重受约束的22阶自回归阶梯。<bookmark mark='c'/>拟合的log-HAR能在这些尺度模仿缓慢衰减，不能据此证明真正的幂律长记忆。",
    'f"Lab. The House\'s HAR':
        "实验。HAR把昨天、5期和22期平均放进回归。<bookmark mark='a'/>比特币截至2019年的拟合中，日和22期系数为{b[1]:.2f}、{b[3]:.2f}，5期接近零，R平方为{h['HAR']['r2']:.2f}。<bookmark mark='b'/>改用滚动252个比特币日，约八个月。日系数较稳定，但5期与22期互换权重：平均值相关，短窗口难区分它们。",
    'f"Pause and predict: if yesterday\'s realized variance':
        "暂停预测：昨天的方差测量很嘈杂，应多信还是少信？<bookmark mark='a'/>少信。已实现四次变差能帮助估计测量不确定性。<bookmark mark='b'/>标量、独立经典测量误差例子会使系数向零衰减；这不是多变量HAR的精确公式。<bookmark mark='c'/>HARQ让日系数随四次变差调整。这里估计为负，但不精确，{verdict}<bookmark mark='d'/>HAR-CJ另给跳跃一个系数，log-HAR拟合对数。下一章研究粗糙性。",
    'the sign is right, but on three years of Bitcoin':
        '符号是对的，但在三年的比特币数据上并不显著。',
    'Chapter eleven. Is volatility rough?':
        '第11章。波动率是粗糙的吗？',
    'How rough is the river?':
        "河流有多粗糙？这里是模拟路径，下方普通布朗运动的H为一半。<bookmark mark='a'/>放大并归一化，比较外形。<bookmark mark='b'/>上方H为0.1，更曲折；自相似指分布意义，不是每段完全相同。<bookmark mark='c'/>绝对增量的q阶矩随滞后按qH次幂缩放。Gatheral、Jaisson和Rosenbaum在已实现波动率代理中估计出约0.1；这支持代理的粗糙缩放，不能排除测量噪声、平滑和有限尺度解释。",
    'Rough, as Gatheral, Jaisson and Rosenbaum found':
        '粗糙的，正如盖瑟尔、雅伊松和罗森鲍姆在股指上发现的那样。',
    'Chapter twelve. Scoring forecasts honestly.':
        '第12章。诚实地给预测评分。',
    'f"In 2005 Peter Hansen and Asger Lunde raced':
        "Hansen和Lunde在2005年比较330个模型。真实方差不可见，只能用带噪声代理评分。<bookmark mark='a'/>真实方差设为1，移动预测画期望损失。<bookmark mark='b'/>代理变得更嘈杂时，波动率平方误差对应的最优方差预测移到{am:.2f}，波动率约为它的平方根。<bookmark mark='c'/>在正、条件无偏及可积等条件下，QLIKE的最小点不变；这是Patton排名稳健性的图示。",
    'Why QLIKE is robust.':
        "QLIKE为何稳健？比较同一信息集下的正预测，代理须为正、条件无偏且期望损失有限。<bookmark mark='a'/>对期望损失求导，目标是条件均值方差。<bookmark mark='b'/>代理噪声只增加与预测无关的项，因此保留排名。<bookmark mark='c'/>取平方根会经由詹森不等式改变目标。<bookmark mark='d'/>DM用长期方差比较平均损失差；正态参照需要合适的中心极限定理与正且有限的长期方差。复用测试集及模型选择还需额外处理。",
    'f"A simulation with a known answer':
        "一个已知答案的模拟：GARCH波动率，每天的真值都知道，重复{sc['R']}次。提供四个预测：真值、真值的百分之八十、百分之一百二十，以及六十天移动平均。用四种损失、对着三种代理变量来评判。<bookmark mark='a'/>暂停预测一下：对着平方收益，用波动率上的绝对误差，谁赢，真值还是它的百分之八十？<bookmark mark='b'/>{verdict}QLIKE和方差上的平方误差，在每一种代理变量下都选出了真值。",
    '80 percent of it. The absolute error on volatility':
        '百分之八十。波动率上的绝对误差奖励偏低的预测，波动率上的平方误差也一样。',
    'f"Lab. The House\'s scoring tools':
        "实验。QLIKE与使用Newey--West方差的DM统计量。这里复用了2020年数据，比较属于探索性。<bookmark mark='a'/>Mincer--Zarnowitz校准要求截距为0、斜率为1。log-HAR的拟合斜率约{mz['log-HAR']['b']:.1f}，不能单凭相关关系确定原因。重新校准应在训练或验证数据拟合，再用新结果检验。",
    'f"Last, many models at once.':
        "最后同时比较多个模型。Hansen--Lunde--Nason模型置信集反复检验预测精度相等并剔除较差模型。名义覆盖针对固定候选集中的最优模型，需要有效的依赖和自助法条件；自适应选模后不是保证。<bookmark mark='a'/>这里，{verdict}<bookmark mark='b'/>在75%水平，{out_txt}被剔除。下一章训练网络。",
    'All of them survive.':
        '全部存活。只有一年、其中还有一个三月，无法以百分之九十的置信度把这些模型区分开。',
    'The set shrinks to the models listed in yellow.':
        '集合收缩到黄色列出的模型。',
    'Chapter thirteen. Training the networks.':
        '第13章。训练神经网络。',
    'Three networks, each reading':
        "三个网络读取过去22天的对数已实现方差。LSTM有门控记忆。<bookmark mark='a'/>小型transformer用注意力加权。<bookmark mark='b'/>输出映回方差使用验证残差校准的工作性对数正态修正；缺乏分布假设时不是精确条件均值。<bookmark mark='c'/>Reisenhofer、Xandro Bayer与Hautsch提出的HARNet，把初始函数设为训练窗口的log-HAR，和竞赛中截至12月重拟合的基线不同。<bookmark mark='d'/>三个网络使用相同划分、早停与五个种子。",
    'f"Watch the {name} learn.':
        "看{name}学习。右边是五个种子的验证损失，左边是各检查点对2019年下半年的预测。<bookmark mark='a'/>随机初始化的预测近乎平坦，随后找到水平和慢变化。第一个种子的最佳轮数为{be}。这次小样本实验主要学到水平与持续性，不能据此限制更大数据和模型的能力。",
    'f"Pause and predict: five seeds':
        "暂停预测：五个种子、相同数据与架构，2020年分数会一致吗？<bookmark mark='a'/>LSTM从{sp['LSTM'][0]:.3f}到{sp['LSTM'][1]:.3f}，transformer的跨度是{wide:.1f}倍。挑选最优种子会增加选择自由度。这里的登记方案固定五个种子并平均，不把挑出的种子当作新发现。<bookmark mark='b'/>HARNet从log-HAR结构出发，种子结果更接近。",
    'f"HARNet\'s replay looks different.':
        "HARNet的回放看起来不一样。它的第一帧就已经是对数HAR的预测，验证损失从{v0:.3f}起步，而其他网络要二十轮才到这里。<bookmark mark='a'/>训练只把它降到{vb:.3f}，最佳轮数较早，此后继续运行直到耐心规则停止；左侧最终面板用保留的最佳权重，右侧显示完整停止路径。学到的滤波器离起点很近：昨天仍然占主导，正如赖森霍费尔和合作者在股指上发现的那样。这个网络是HAR的一台显微镜：它确认了结构，而不是取代它。",
    'Chapter fourteen. The race.':
        '第14章。竞赛。',
    "Hansen and Lunde's question, asked of Bitcoin":
        "用比特币重问Hansen与Lunde的问题：什么能胜过GARCH？他们的货币和股票结论并不相同。<bookmark mark='a'/>网络训练至2019年6月、下半年验证；传统模型拟合至12月。2020年是回顾性评估，部分模型看过结果后加入并计数。<bookmark mark='b'/>EWMA、GARCH、GJR看日收益，HAR与HARQ看已实现方差，网络平均五个种子。都预测次日方差，以QLIKE评分。",
    'f"Now run the test year, day by day.':
        "现在把测试年一天一天地跑一遍。每根柱是一个模型到目前为止的平均QLIKE，柱子随日子推移重新排序。<bookmark mark='a'/>整个一月和二月，领先的是{lead0}：在平静的市场里，最简单的平均很难被打败。<bookmark mark='b'/>然后是3月12日。每根柱都猛然一跳，顺序在一天之内被打乱。<bookmark mark='c'/>到十二月，读取已实现方差对数的模型排在前面，{lead1}以毫厘之差夺得第一。",
    'f"The results, over the':
        "结果，覆盖2020年的{r['test_days']}天。越低越好。<bookmark mark='a'/>只看日收盘价的模型，指数平均、GARCH和GJR，排在最后。<bookmark mark='b'/>读取已实现方差的模型更好，两个神经网络还要更好。LSTM以迪博尔德–马里亚诺t为负三胜过HAR。它发现了什么吗？<bookmark mark='c'/>看它预测的是什么：已实现方差的对数，而不是方差本身。取对数驯服了主导最小二乘拟合的那些尖峰。所以，在看到这些结果之后，我们加了一个参赛者，试验计数器也把它算进去：还是HAR，四个系数，只是拟合在对数上。<bookmark mark='d'/>它排在第一。对比对数HAR，LSTM的t统计量为{dml['LSTM']['t']:.1f}，有利于对数HAR：没有证据表明网络在对数之外增加了任何东西。<bookmark mark='e'/>白点：单个种子。<bookmark mark='f'/>而用平方误差给同样的预测评分，顺序就变了：{mse_order[0]}排第一。一场竞赛的诚实程度，取决于它的损失函数。",
    'f"And the late entrant, HARNet':
        "还有后来加入的HARNet，它生来就是对数HAR。<bookmark mark='a'/>它能胜过自己的起点吗？{verdict}那置信集呢？{mcs_line}",
    'As the last chapter warned, it keeps every model':
        '正如上一章警告的，它保留了每一个模型：一年的数据无法加冕赢家。',
    'It narrows the field, but keeps several models.':
        '它缩小了范围，但保留了好几个模型。',
    'Here is the whole test year.':
        "这是整个评估年，每点为每日已实现波动率。GARCH只看收盘收益，反应较慢。<bookmark mark='a'/>log-HAR利用日内路径信息追踪水平。这些拟合漏掉最大尖峰，但不能证明其他模型或信息无法改善。条件风险预测描述分布或水平，不是逐个实现的意外。",
    'Chapter fifteen. Foundation models, and the frontier.':
        '第15章。基础模型与前沿。',
    'Since 2024, foundation models promise':
        "2024年以来，基础模型尝试无需针对目标序列训练就预测。Chronos把数值变成词元。<bookmark mark='a'/>窗口使用比特币截至3月12日的日波动率，已包含危机，再按平均尺度归一。<bookmark mark='b'/>分箱把每天变成固定词表中的一个词元。<bookmark mark='c'/>真正Chronos用大规模语料训练transformer预测下个词元，输出各箱概率。接下来本地玩具只借鉴分词，不复制架构。",
    'The published models are not installed here':
        "这里没有安装论文模型，因此搭建了受分词启发的玩具：词元嵌入加单隐藏层numpy MLP，不是transformer，也不是Chronos复现。训练语料是四类合成波动率。<bookmark mark='a'/>看三个种子学习。3月13日的预测读取截至12日的64天，包括危机当天，不能说提前预见危机。词元概率从合成数据学习持续性。",
    'f"Pause and predict: a model trained only on synthetic':
        "暂停预测：只用合成序列训练的玩具，对比在比特币拟合的四个系数，会怎样？<bookmark mark='a'/>冻结模型逐日评估2020年，扇形是名义10至90分位区间。<bookmark mark='b'/>QLIKE为{f['qlike']:.3f}，log-HAR为{f['qlike_loghar']:.3f}。{verdict}区间覆盖{100 * f['cover80']:.0f}%的日子，名义80%不是保证。未拒绝差异也不等于模型等效。",
    'It wins, by more than luck.':
        '它赢了，超出了运气的范围。从合成序列学到的结构可以迁移。',
    'Worse, by more than luck.':
        '更差，超出了运气的范围。用比特币自身拟合的四个系数仍然获胜。',
    'f"Slightly better, but within noise':
        '略好一点，但在噪声之内：迪博尔德–马里亚诺统计量是{tt:.1f}。',
    'f"Worse, though one year cannot make the gap significant':
        '更差，不过一年的数据无法让这个差距显著：统计量是{tt:.1f}。它落在HAR和Transformer之间：一个从未见过比特币的模型，和水平上的HAR一样好，但不如对数HAR。',
    'What do the real models do?':
        "真实模型如何？Brini在2026年7月比较50种资产上的9个基础模型和8个计量模型。这里是论文的一日QLIKE：逐资产先取比值，再跨资产平均。<bookmark mark='a'/>TTM在图中最好。Sundial与HAR的一日比值也略低于log-HAR；TTM是三个报告期限都领先的唯一基础模型。<bookmark mark='b'/>论文用重新校准诊断尺度影响，TTM与log-HAR组合在该基准上表现良好。这不是普遍排名；预训练数据也可能覆盖评估期。",
    'The frontier in one screen':
        "一屏看完前沿：2024和2025年的基础模型，以及波动率方面的论文。机器学习在道指成分股上一日预测帮到了HAR；跨股票汇总训练的网络可以泛化。<bookmark mark='a'/>在金融上，TimesFM需要微调，在金融数据上预训练有帮助，Kronos在它自己的基准上报告了提升。诚实的总结：在波动率上，对数HAR仍然是要跨过的门槛。这里的每个模型都在平静和动荡的日子里一起打分。下一章：最动荡的时刻，2020年3月。",
    'Chapter sixteen. March 2020.':
        '第16章。2020年3月。',
    'In March 2020, as Covid-19 closed one economy after another':
        '2020年3月，新冠疫情让一个又一个经济体停摆，所有东西同时被抛售换取现金。3月12日，美国股市下跌百分之九点六。比特币一天下跌百分之三十九点五。在以太坊上，据事后的一份报告，约八百万美元的MakerDAO抵押品以零出价被拍卖。3月16日，股市下跌百分之十二，是1987年以来最糟的一天；VIX，也就是市场自己对波动率的预测，收于八十二点六九，创下纪录。',
    'Here are the weeks around it.':
        "这是前后几周。点是每天的已实现波动率，线是前一天做出的预测。<bookmark mark='a'/>三条线都在12日之后跳起。然后在市场平静下来的几周里，三条线都居高不下：冲击之后，波动率衰减得比用平静年份拟合的模型所预期的更快。",
    'A desk question. Daily volatility is one percent.':
        '一个交易台问题。日波动率是百分之一。一周的波动率是多少？一年呢？这个答案什么时候是错的？',
    'Chapter seventeen. How the industry forecasts volatility.':
        '第17章。业界如何预测波动率。',
    'f"In October 1994 J.P. Morgan published RiskMetrics':
        "1994年10月，摩根发布RiskMetrics，日方差衰减系数0.94，月度预测使用0.97；MSCI于2010年收购。<bookmark mark='a'/>统一衰减保持半正定，适当初始条件下保持正定。任意逐元素衰减可能破坏它，但结构化异质模型仍可有效。<bookmark mark='b'/>美国市场网格结果：{rmse_line}。周QLIKE：{qlike_line}。这里损失与预测期限都不同，不能把差异只归因于损失函数。",
    "f'the squared error picks":
        "平方误差选的是{ind['lam_rmse']:.2f}",
    'f"It picks {ind':
        "它选的是{ind['lam_qlike']:.2f}，正是摩根大通的那个数字。",
    'f"Factor risk models face this at scale.':
        "因子风险模型在更大规模上面对同样的问题。按MSCI自己的说法，MSCI Barra 2011年的美国股票模型用比波动率更长的半衰期估计相关性，以保持矩阵良态，并加入一个波动率机制调整，用横截面偏差统计量的时间序列来缩放每个因子的波动率。<bookmark mark='a'/>我们拿不到确切的公式，所以这里是一个同样思路的复现：把每天收益与预测波动率之比的平方在各组合间平均，再平滑。预测偏低时，乘数升到一以上。<bookmark mark='b'/>在十个规模组合上，它在大萧条时冲到{pk['1929']:.1f}，1987年到{pk['1987']:.1f}，2020年到{pk['2020']:.1f}。{vra_line}",
    'f"Trend followers lean heavily on volatility forecasts.':
        "趋势策略依赖波动率预测。Harvey等研究波动率缩放；Moskowitz、Ooi与Pedersen使用60日重心估计仓位。<bookmark mark='a'/>我们的美国市场描述性示例使用两日滞后、10倍杠杆上限、10%波动率目标，未扣交易和融资成本。普通基准事后按整个时期波动率匹配。{vt_line}回撤基于累计简单超额收益，不是复利或对数财富。",
    "f'The Sharpe ratio rises from":
        "夏普比率从{b['sharpe']:.2f}升到{a['sharpe']:.2f}，最糟的日子更温和，最深的回撤浅得多。预测不需要预测方向就能赚钱；它只需要知道什么时候该小。",
    'Here the Sharpe ratio does not improve.':
        '这里夏普比率没有改善。',
    'Chapter eighteen. The volatility forecaster.':
        '第18章。波动率预测器。',
    'f"The House\'s data desk now carries a volatility forecaster':
        "公司的数据台已有波动率预测器。<bookmark mark='a'/>包含日内测量、GARCH、动态相关、随机波动率、HAR、机制、卡尔曼滤波与评分工具。<bookmark mark='b'/>第八条规则是前瞻标准；这次2020年比较曾复用，并在结果后加入模型，不能称完全事前。登记记录本部分{env2['part7_trials']}次模型试验，系列截至本部分为{env2['trials']}次；2021年起的保留集仍封存。",
    'f"Lab. This is how a desk calls it':
        "实验。递归插件log-HAR使用固定残差方差修正，并非精确多步对数正态矩。研究窗口最后一天2020年12月31日，比特币次日年化波动率约{100 * h['btc_next']:.0f}%，未来22个日历日的年化均方根约{100 * h['btc_month']:.0f}%。<bookmark mark='a'/>美国市场GARCH期限结构{shape}",
    'rises with the horizon':
        '随期限上升：市场比它的长期水平更平静，GARCH预期它向上回归。',
    'falls with the horizon':
        '随期限下降：预期波动率向下回归。',
    'f"Part seven in ten lines.':
        '第7部分回顾。幅度持续性强，但收益低自相关不证明不可预测。单位根推断取决于确定性项。协整研究平稳组合。隐藏状态与GARCH以不同方式描述波动率。相关性会变。已实现测量含噪声和跳跃，代理粗糙性需解释。复用2020年比较中{best}的QLIKE领先，但相对log-HAR没有清晰改善证据。论文基础模型结论依赖架构与期限，方差聚合需自协方差和期限条件。',
    'Four desk questions.':
        "四个交易台问题。恒定方差、零自协方差下，每日1%在5个交易日约2.2%、252日约16%。<bookmark mark='a'/>价格回归的t值：检查单整并用正确残差检验临界值。<bookmark mark='b'/>危机日可能主导平方误差排名；使用合理基线、损失和推断。<bookmark mark='c'/>alpha加beta等于1、omega为正时没有有限无条件方差；严平稳要满足Nelson对数条件。严格詹森不等式还需alpha为正、平方冲击非恒定。解答见笔记。",
    'And eight problems':
        '还有八道习题：GARCH的期限结构与半衰期，GARCH作为平方收益的ARMA模型，噪声给已实现方差带来的偏差与最优采样频率，QLIKE为什么能正确排名，卡尔曼增益，迪基–富勒极限，以及两道资格考试水平的题：为什么迪博尔德–马里亚诺检验偏向较小的嵌套模型，以及偏多少。中英文解答见笔记。',
    'Where this comes back:':
        '这些内容会在哪里再出现：第10部分起的波动率交易台和波动率曲面，第13和14部分的随机波动率与粗糙波动率，配对交易与收益率因子，系统化宏观，以及第31和40部分的风险模型与风险价值。',
    'The textbook chapters this part covers':
        '本部分覆盖的教材章节与论文。实证示例用本系列代码与公开数据：French市场收益、FRED收益率和VIX，以及Binance价格。模拟固定种子，基础模型的论文比较明确标为引用结果。',
    'The House can now forecast how much the market will move.':
        "我们的公司现在能预测市场会动多大。<bookmark mark='a'/>下一部分，第8部分：决策与控制。有了预测，该下多大的注？效用、动态规划、默顿的投资组合问题，以及凯利准则和至今仍围绕着它的争论。",
    'Two practical details. The critical value depends':
        "两个实用细节。临界值取决于回归里还有什么。没有常数项时，百分之五分位点是负一点九四。<bookmark mark='a'/>加上常数项，允许序列有非零均值，是负二点八六，正是我们模拟出的数字。<bookmark mark='b'/>再加上时间趋势，是负三点四一：回归每多估计一个确定性项，分布就再往左移一些。如果变化量本身是自相关的，普通检验会失真，所以增广检验加入滞后变化量，直到残差变成白噪声。把这些项选错，是单位根检验出错最常见的方式。但两个有单位根的序列仍可能被绑在一起。下一章：协整。",
    'f"One more check on the race: calibration.':
        "再检查校准：Mincer--Zarnowitz要求截距为0、斜率为1。<bookmark mark='a'/>这里斜率最接近1的是{best_cal}，为{mz[best_cal]['b']:.2f}；这不代表所有校准标准都最好。log-HAR斜率为{mz['log-HAR']['b']:.1f}。修正应在更早的训练或验证数据拟合，并用新结果检验。同样本重新校准只能诊断，不能证明预测改善。下一章是基础模型。",
    'Rule eight, unpacked':
        "规则八是前瞻标准：选模时不触碰评估集，与简单基线比较，依据代理与嵌套结构选择损失和推断。<bookmark mark='a'/>本章2020年比较后来复用并加入新模型，均已计数，因此排名为探索性。QLIKE稳健要求正的条件无偏方差代理。DM和置信集有适用条件，嵌套平方误差可能需Clark--West。登记揭示搜索历史，另一个2021年起的保留集仍封存。",
    'How the parameters are found.':
        "参数是怎么找到的。滤波器只向后看；估计时我们可以利用事后信息。金氏平滑器从最后一个月倒推回第一个月，用之后的一切信息修正每个月的概率。<bookmark mark='a'/>然后，最大化步骤就是加权最小二乘：每个机制的均值和方差，是各月按属于该机制的概率加权后的平均。<bookmark mark='b'/>每个转移概率，是从一个机制转到另一个机制的期望次数，除以在第一个机制中的期望时间。期望，然后最大化，反复进行：阿瑟·登普斯特、南·莱尔德和唐纳德·鲁宾1977年的算法，它永远不会降低似然。状态切换是一个会跳的隐藏变量。下一章：一个缓慢漂移的隐藏变量，以及追踪它的滤波器。",
    'f"Why the recursion is safe.':
        "递推为何有效？展开后，Q是目标矩阵与过去冲击外积的加权和。<bookmark mark='a'/>目标和初始矩阵正定，a、b非负且和小于1，Q就保持正定，可以归一化为相关矩阵。<bookmark mark='b'/>多步预测却是非线性的：冲击外积的条件期望是R而非Q，精确递推必须保留期望R；用Q代替只是线性化。<bookmark mark='c'/>这里a加b为{a + b:.3f}，对应的持续性摘要半衰期约{hl:.0f}个交易日，并不是归一化相关性预测的精确半衰期。相关性会随时期改变，平衡组合必须关注它。下一章用日内数据测量波动率。",
    'f"What does H measure?':
        "H衡量什么？分数布朗运动的协方差使缩放后的过程同分布；这些最小最大归一化面板只演示形状，不是估计器。<bookmark mark='a'/>模型中相邻增量的相关为2的2H减1次幂再减1。<bookmark mark='b'/>H小于一半时为负。<bookmark mark='c'/>代入比特币代理估计H为{H:.2f}，模型隐含相关约{rho:.2f}；这不是直接测得的增量相关。<bookmark mark='d'/>适当的粗糙波动率、杠杆和正则条件下，短期限ATM偏斜可按期限的H减一半次幂变化。第14部分展开，下一章先讲评分。",
    'f"Why stop early?':
        "为什么早停？训练损失持续下降，可能最终过拟合。<bookmark mark='a'/>这个种子的验证损失在第{be}轮最低，之后上升{gap:.3f}，支持在这里停止，但不能证明记住了具体噪声。<bookmark mark='b'/>保留最佳验证权重，约三十轮无改善后停。网络训练至2019年6月、下半年验证；传统基线拟合至12月。2020年不参与梯度或早停，但后来用于比较和新增模型。另一个2021年起的信封仍封存。",
    'Recall the test.':
        "回顾这个检验。<bookmark mark='a'/>取每天小模型的平方误差，减去大模型的。<bookmark mark='b'/>迪博尔德和马里亚诺把平均值除以它的长期标准误，与正态比较。<bookmark mark='c'/>但假设小模型嵌套在大模型里，额外的系数真的为零。那么在总体中两个模型给出同样的预测，差值恒等于零，正态近似没有方差可用。",
    'The fix, from Todd Clark and Kenneth West in 2007, is one line.':
        "托德·克拉克和肯尼斯·韦斯特在2007年给出的修正只有一行。<bookmark mark='a'/>把大模型的额外参数在原假设下的代价加回去：两个预测之差的平方。<bookmark mark='b'/>然后对调整后的差值做单侧检验，与正态比较。它不是精确的，但很接近，在我们的公司里只需一行代码。",
    'Simulate it.':
        "做模拟。<bookmark mark='a'/>目标是纯噪声，大模型增加了一个什么也预测不了的持久回归变量。迪博尔德-马里亚诺统计量的中心明显低于零：大模型因它的估计噪声而受罚。<bookmark mark='b'/>克拉克-韦斯特统计量的中心接近零，接近正态曲线。",
    "On real data, Bitcoin's realized variance in 2019 and 2020.":
        "比特币2019至2020年的已实现方差。<bookmark mark='a'/>HAR相对单滞后的样本MSE高约1%，DM没有清晰证据，CW略偏向HAR但不显著。HARQ相对HAR的样本MSE高约65%，两个统计量均未支持HARQ。调整改变检验统计量，不会降低已经发生的预测损失；样本更差也不证明总体永远更差。",
    'Pause and predict. Over two hundred forecasts':
        '暂停思考。在两百个预测上，平均损失差为负零点零二，标准误零点零三，两个预测之差的平方的平均值为零点零五。粗略比较时，假定调整后统计量的标准误也为0.03，再计算两个统计量。它们偏向哪个模型？',
    'The ten-year yield: the unit-root null is rejected':
        '十年期收益率：在此检验设定下拒绝单位根原假设。',
    'this specification rejects the unit-root null decisively.':
        '此设定明确拒绝单位根原假设。',
    'The nominal test does not detect a jump.':
        '名义检验未检出跳跃；这不证明没有跳跃，有限采样与噪声会影响检验。',
    'The nominal test rejects the continuous-path null, subject to its assumptions.':
        '名义检验拒绝连续路径原假设，结论依赖检验条件。',
    'f"Conditional on fitted parameters, the filter uses':
        "给定拟合参数，滤波器只使用截至当天的观测；刚才的平滑路径则用了事后信息。Rauch、Tung和Striebel的平滑器从后向前运行：<bookmark mark='a'/>用下一天平滑值的新信息修正今天的估计。<bookmark mark='b'/>隐藏对数方差的平稳均值为{sv['mu']:.2f}，对应年化波动率中位数约{100 * lr:.0f}%，不是无条件均值；均值还需要对数正态方差修正。预测用滤波，历史描述可用平滑。下一章用过去收益直接构造GARCH方差。",
    'f"The theory. Under continuous':
        "理论：连续无噪声半鞅下，平方和收敛到积分方差；跳跃会另加跳跃平方。<bookmark mark='a'/>在常规条件下，BNS误差按n的平方根倒数缩小，由四次幂估计。<bookmark mark='b'/>独立外生价格噪声产生2n乘噪声方差的偏差。<bookmark mark='c'/>两项MSE近似平衡偏差与采样误差。一分钟的噪声代理还含有效价格变动，所以约{s['nstar_min_median']:.0f}分钟的插件结果只是演示，不是验证过的最优频率。<bookmark mark='d'/>TSRV结合疏密网格，图中的有限样本分母与代码一致。<bookmark mark='e'/>已实现核利用自协方差消除噪声，需要相应假设。预平均和不规则采样进一步扩展工具。",
    'f"Lab. The House\'s estimator fits':
        "实验。对每个q估计对数矩与对数滞后的斜率，再由斜率对q估计H。<bookmark mark='a'/>模拟H为0.1和0.5时，返回约{s1.mean():.2f}、{s5.mean():.2f}。<bookmark mark='b'/>比特币{len(ro['lv']):,}天的对数已实现波动率给出H为{b['H']:.2f}。{verdict}这仍是带噪声代理的尺度估计，不能证明潜在波动率粗糙。<bookmark mark='c'/>H为一半时，q等于2的斜率为1。<bookmark mark='d'/>理想高斯粗糙模型的预测器使用幂律核，HAR可作有限尺度近似。",
    'f"Here is what each model said on March':
        "各模型在3月11日对12日如何预测？最高的{best}给出年化{100 * m[best]:.0f}%。<bookmark mark='a'/>实际测量为{100 * real:.0f}%。<bookmark mark='b'/>这些拟合漏掉了幅度，但不能证明所有模型或信息集都不可能预测。已实现测量帮助事后反应。<bookmark mark='c'/>极大日会主导方差平方误差；QLIKE改变尺度和不对称性，仍受极端值影响，排名稳健还需要评分章的代理条件。",
    'f"If daily returns have constant variance':
        "若日收益方差恒定且自协方差为零，方差可相加：每日1%，5个交易日约2.2%，252日约16%。<bookmark mark='a'/>图把每个期限都年化：累计标准差是预期方差之和的平方根，再乘252除以T的平方根，得到均方根年化尺度，因此恒方差线是水平的。<bookmark mark='b'/>GARCH起点为{100 * s['spot_vol']:.0f}%，未来一年的期限平均年化波动率为{100 * gv[-1]:.0f}%，向长期{100 * un:.0f}%靠近。<bookmark mark='c'/>自协方差影响方差聚合，分位数还需分布假设。物理测度GARCH期限结构不同于含风险溢价的风险中性期权隐含波动率。",
    'f"Options desks have a forecast in prices':
        "期权价格包含预测。VIX是标普500的30个日历日隐含指数，我们的代理是French较宽泛美国市场未来21个交易日的实现值。<bookmark mark='a'/>VIX有{100 * ind['share_vix_above']:.0f}%的观测高于代理，平均高{ind['vrp_mean']:.0f}个波动率点。这并不直接识别方差风险溢价，还需匹配期望、平方、期限和指数。<bookmark mark='b'/>回顾性回归R平方分别为{100 * mzv['r2']:.0f}%与{100 * mzg['r2']:.0f}%。{both_line}GARCH参数在1990年前拟合，但去均值使用研究样本；重叠结果使用HAC标准误。这是描述性关联，不是新的时点验证。",
    'For the researcher: Chapter twelve':
        '写给研究者：第12章比较了DM检验。在嵌套模型的平方误差总体原假设下，预测差可能退化，普通正态推断可能失效。这里研究一种递归估计设定及Clark--West调整。',
    'And in a finite sample, estimation matters.':
        "有限样本中估计误差很重要。<bookmark mark='a'/>定义delta为两个拟合预测的差，包括共同系数重新估计的影响。<bookmark mark='b'/>精确恒等式是大模型减小模型的平方误差等于delta平方减两倍小模型误差乘delta。只与未来新息独立，不足以消掉整个交叉项。适当估计与正交条件下，主导近似留下额外均方惩罚。<bookmark mark='c'/>下面的实验中损失差偏负，递归嵌套极限非标准，并依赖预测期与估计期之比。",
    'Three practical research questions.':
        "三个实际研究问题。<bookmark mark='a'/>候选模型混合嵌套与非嵌套时，联合推断必须覆盖退化与估计误差，普通置信集输出不自动有效。<bookmark mark='b'/>Giacomini--White研究固定长度滚动估计的预测方法，需要非退化和正则条件，不是让所有嵌套都无害。<bookmark mark='c'/>分位数、预期损失等目标需要对应损失的理论，不能直接套平方预测差调整；这不意味着不存在相关方法。",
    'daily-variance RMSE is smallest at the left edge':
        '日方差RMSE在网格左端最小，但这不能确定网格之外的最优值',
    'It lowers this historical QLIKE':
        '历史QLIKE降低；初始化之后，乘数只使用前一天及更早的标准化收益。',
    'Both coefficients are significant in this in-sample HAC regression':
        '两个系数在此样本内HAC回归中均显著，这不是独立预测验证。',
    'At least one coefficient is not significant here':
        '至少一个系数在这里不显著；不拒绝不能证明没有增量信息。',
    'f"By the smallest of margins, and well within noise:':
        '只领先极小幅度，DM统计量为{t:.1f}。没有清晰改善证据；不拒绝不能证明等效。',
    'The nominal test favors HARNet here':
        '这里名义检验偏向HARNet，但须考虑依赖假设和评估样本复用。',
    'Size and power in this simulated DGP.':
        "此模拟数据生成过程中的检验水平与功效。<bookmark mark='a'/>原假设为真时，迪博尔德和马里亚诺每两百五十次才拒绝一次，远低于百分之五：这个检验几乎从不偏向大模型。克拉克和韦斯特约百分之三拒绝，略为保守，正如他们所报告的。<bookmark mark='b'/>真实斜率为零点零五时，迪博尔德和马里亚诺一百次中发现一次，克拉克和韦斯特发现八次；零点一时，前者仍不到百分之四，后者是四次中一次。这里未调整检验功效很低，这些拒绝率不是普遍结果。",
    'In this specification, the rank-one verdict implies':
        '在此设定下，秩一结论意味着两个共同随机趋势和一个协整关系。',
    'Using that rough common standard error,':
        '使用这个粗略的共同标准误，DM约为负0.67，偏向小模型。调整后的均值是0.03，所以CW约为1，略偏向大模型但不显著。真正的CW标准误必须从调整后的序列计算。',
}

PHRASES = {
}
