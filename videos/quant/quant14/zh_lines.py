"""Chinese narration for quant14: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第14部分：粗糙与路径依赖波动率'

CHAPTERS = {
    'Hook': '粗糙',
    'Fact': '1. 有限期限的偏斜绝对值',
    'SkewMath': '2. 为什么是幂律：由核得到偏斜',
    'Rough': '3. 测量已实现方差的粗糙度',
    'Forecast': '4. 用粗糙的记忆做预测',
    'RBergomi': '5. 粗糙贝尔戈米模型',
    'Hybrid': '6. 模拟粗糙路径：混合格式',
    'RHeston': '7. 粗糙赫斯顿：沃尔泰拉方程与它的里卡蒂方程',
    'Adams': '8. 求解：分数阶亚当斯格式',
    'Hawkes': '9. 粗糙从何而来',
    'Lift': '10. 马尔可夫提升',
    'Debate': '11. 争论之一：时间序列在愚弄我们吗？',
    'Options': '12. 争论之二：期权怎么说',
    'PDV': '13. 路径依赖波动率',
    'SPX': '14. 标普500上的路径依赖波动率，以及2024年8月5日',
    'Joint': '15. 标普与VIX联合校准：二次粗糙赫斯顿与居永的难题',
    'Signature': '16. 签名波动率模型',
    'House': '17. 交易台用什么，以及粗糙实验室',
    'Frontier': '18. 研究选读，2023至2025年',
    'Research': '写给研究者：粗糙模拟收敛得多快',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part fourteen. Rough and path-dependent volatility.":
        "第14部分。粗糙与路径依赖波动率。这是波动率建模最新的一章，也是争论最多的一章。",

    'Two random paths. Zoom into the Brownian path two hundred and fifty-six times, r':
        "两条随机路径。把布朗路径放大256倍，每段都重新填满方框。布朗运动会变成直线吗？<bookmark mark='a'/>不会。布朗运动和分数布朗运动都具有自相似性；按各自的理论时间与振幅比例缩放，都不会变得可微。这里采用的却是每个有限片段的实测极差归一化。<bookmark mark='b'/>下方路径的H为十分之一：时间间隔缩小时，它的增量比布朗增量缩小得慢。最后只剩几十个模拟步，折线反映的是绘图分辨率，不能证明平滑。<bookmark mark='c'/>盖瑟尔、贾森与罗森鲍姆2014年的预印本、2018年发表的论文，在已实现波动率代理中发现了较低的尺度指数。本部分重新测量这一现象，用粗糙模型定价，并检验其他解释。",

    'How we got here. In 1968 Benoit Mandelbrot and John Van Ness defined fractional ':
        "我们是怎么走到这里的。1968年，伯努瓦·曼德尔布罗和约翰·范内斯定义了分数布朗运动，也就是带赫斯特指数的过程。<bookmark mark='a'/>1987年崩盘之后出现了偏斜，九十年代的模型，首先是赫斯顿模型，让方差具有布朗运动的局部正则性，在非退化处仍不可微。1998年，法比安娜·孔特和埃里克·勒诺给了波动率长记忆：H大于二分之一。<bookmark mark='b'/>洛伦佐·贝尔戈米为远期方差曲线建模；2007年，埃莉莎·阿洛斯、豪尔赫·莱昂和约瑟普·比韦斯证明，粗糙的核会让偏斜成为幂律。<bookmark mark='c'/>2014年，那篇为这个领域命名的论文问世：波动率是粗糙的。随后是粗糙贝尔戈米、粗糙赫斯顿、二次粗糙赫斯顿，以及Risk杂志2021年度量化人物。<bookmark mark='d'/>2023年，一种对立的观点：路径依赖波动率。而在2024年8月5日，VIX在开盘前打出了六十五以上。",

    "The plan. The fact that started it, measured week by week":
        "本部分的安排。引出这一切的事实，逐周测量，以及粗糙的核为什么会造成它。为粗糙命名的那次测量，以及它给预测者带来了什么。"
        "交易台熟悉的两个粗糙模型，连同打开来看的数值方法。粗糙可能从何而来，以及如何把它变成马尔可夫的。反对粗糙的论据。"
        "对立的观点：波动率大体上是过去的函数，并在2024年8月5日上检验。最后是前沿，以及交易台实际在跑什么。",

    "In the House, the volatility desk opens a rough lab.":
        "在我们的公司里，波动率交易台开设了一个粗糙实验室。<bookmark mark='a'/>它增加了模型、让模型能用的数值方法，"
        "以及一条规则：新模型何时才算站稳了脚跟。",

    # ------------------------------------------------------------------ Fact
    'Chapter one. Finite-maturity skew magnitudes.': '第1章。有限期限的偏斜绝对值。',

    'f"Here are the original one hundred and two dates in the frozen 2024 to 2025 dat':
        "这里保留冻结数据清单中2024至2025年的全部102个原始日期。每根线表示各期限SVI曲线在平值附近用有限差分得到的偏斜绝对值，两个轴取对数。来源是汇总的期权标记价格，并非同时可执行报价，也不是到期趋零的连续极限。<bookmark mark='a'/>许多日期的短期限绝对值更陡，但八个拟合指数为负。带符号偏斜也会改变方向，取绝对值会隐藏这一信息。白线是描述性的幂律拟合。<bookmark mark='b'/>直方图保留全部指数，包括负值。中位数为{w['a_median']:.2f}，四分位数为{w['a_q'][0]:.2f}和{w['a_q'][1]:.2f}。它们概括的是有限窗口，不能证明偏斜发散。红线为2024年8月7日，即后面危机发生两天之后。",

    'f"One date up close: the tenth of December 2025 Surface. <bookmark mark=\'a\'/> Th':
        "近看一个日期：2025年12月10日的曲面。<bookmark mark='a'/>幂律拟合指数为{p['a']:.2f}。<bookmark mark='b'/>平移幂律对这些点拟合略好，平移量为{365 * q['eps']:.0f}天。正平移使这个函数在零期限处有界，但并没有观测到该极限。<bookmark mark='c'/>在全部原始日期中，{100 * w['bounded_share']:.0f}%的平移拟合将报告的对数均方根误差降低超过零点零一。逐周优化使用报价记录数加权，报告的误差却不加权，两种拟合的指数约束也不同。这个门槛只是样本内的描述规则，不是显著性检验，也不能认证模型选择。",

    "in most weeks the straight line is as good as anything": "在大多数周里，直线和任何别的形式一样好",
    "in most weeks the bending form fits better": "在大多数周里，弯曲的形式拟合得更好",

    'f"Define psi as the magnitude of the implied-volatility slope in log-moneyness a':
        "定义psi为平值处隐含波动率对数价值度斜率的绝对值。观测采用有限差分，是导数的近似。<bookmark mark='a'/>幂律写成c乘T的负a次方。只有在适当粗糙模型的短期限展开下，a才等于二分之一减H。把有限窗口中位数{w['a_median']:.2f}代入，会得到{w['H_median']:.2f}，这并不识别赫斯特指数。通常的布朗沃尔泰拉平方可积核要求H为正；更广的超粗糙构造属于另一类。<bookmark mark='b'/>平移模型在拟合平移量为正时有界。<bookmark mark='c'/>假设H为十分之一，且幂律近似适用于一天到一个月，偏斜绝对值之比是多少？<bookmark mark='d'/>三十的十分之四次方，约3.9。单凭这个比值，无法判断头寸总波动率风险。",

    "A rough reading, as the time series of chapter three will find.": '这是一个粗糙的读数，第3章的时间序列也会得到这样的结果。',
    "That is below zero, which no rough model allows:":
        "这低于零，没有任何粗糙模型允许这样：除了粗糙之外，还有别的东西让比特币的短端变陡，下一章计算出的跳跃偏斜给出了一个候选。",

    # ------------------------------------------------------------------ SkewMath
    "Chapter two. Why a power law: the skew from the kernel.": "第2章。为什么是幂律：由核得到偏斜。",

    'Why can a rough kernel produce a power-law skew? The floor contains all pairs t ':
        "为什么粗糙核能产生幂律偏斜？底面包含所有t早于u、u早于到期T的时间对，高度示意一次冲击对远期方差的影响。<bookmark mark='a'/>初始远期方差平坦、波动率的波动率较小时，带符号偏斜的首项正比于三角形上的核积分，再除以T平方。指数核在零附近有界；期限远小于其衰减时间时，该比值趋于常数。<bookmark mark='b'/>理想幂核在对角线有可积奇点，未截断积分按T的H加二分之三次方缩放。为便于观察，图中屋顶除以二点五并截顶，右侧曲线并非用这个显示体积计算。<bookmark mark='c'/>解析积分除以T平方，得到T的H减二分之一次方。这些是模型的首阶结论，振幅与适用范围取决于具体模型。",

    "Now the algebra behind the picture.":
        "现在是图像背后的代数。在远期方差模型里，更晚的u时刻的期望方差随现货一起移动：它们的协方差是rho乘以波动率、乘以远期方差、"
        "再乘以滞后u减t处的核。<bookmark mark='a'/>洛伦佐·贝尔戈米和朱利安·居永证明，在波动率的波动率的一阶近似下，平值偏斜就是这个协方差在三角形上的积分，"
        "除以二倍的sigma立方乘T平方。<bookmark mark='b'/>对指数核，二重积分是T除以kappa减去一个修正项：在短期约为T平方的一半，所以偏斜是平的；"
        "在长期约为T除以kappa，所以偏斜像T分之一那样下降。<bookmark mark='c'/>对幂律核，积分两次：T的H加二分之三次方。除以T平方：T的H减二分之一次方。"
        "<bookmark mark='d'/>用粗糙贝尔戈米自己的核，前面的常数也可以明确写出。",

    "Fukasawa's 2021 theorem concerns a precise limiting market. Prices are positive ":
        "深泽2021年的定理讨论一个明确的极限市场：价格为正的连续伊藤过程，瞬时方差为正且局部赫尔德正则，固定到期日前附近有无摩擦期权交易。平值附近持续同号、H小于二分之一的幂律，与严格高于H的方差正则性冲突。<bookmark mark='a'/>我们的有限期限绝对值拟合包含符号变化，不能验证这些假设。正则化核和多个指数核都能在有限区间近似幂律。定理区分的是极限行为，不能决定这场有限数据比较的胜者。",

    'f"Now finite-grid numerical prices. First consider the illustrative exponential ':
        "现在看有限网格数值定价。先考虑每年二的示意指数衰减率：只有期限远小于半年、并考虑模型其他时间尺度时，首阶偏斜才近似平坦。<bookmark mark='a'/>图中的赫斯顿曲线却使用第十三部分拟合的衰减率，约14.8，其短窗口拟合指数为{hs['short']:.2f}。<bookmark mark='b'/>红线把常数扩散与贝茨拟合的跳跃参数组合，有限差分指数为{js['short']:.2f}；它不是所有跳跃模型的普遍渐近规律。贝茨同时包含随机方差与跳跃。<bookmark mark='c'/>在这些网格上，粗糙模型曲线也与首阶虚线公式不同。小波动率的波动率理论不是有限网格的精确预测。<bookmark mark='d'/>市场短窗口指数为{m['market']['short']:.2f}。模型主要采用2至14天和60至365天窗口，但市场与粗糙贝尔戈米窗口不同，偏斜差分方法也不同。这些分数描述已记录的计算，不能证明必须采用某一类核。下面测量粗糙度。",

    # ------------------------------------------------------------------ Rough
    'Chapter three. Measuring roughness in realized variance.': '第3章。测量已实现方差的粗糙度。',

    'f"Gatheral, Jaisson and Rosenbaum studied realized-volatility proxies computed f':
        "盖瑟尔、贾森与罗森鲍姆研究由高频收益构造的已实现波动率代理。这里是用五分钟收益测得的比特币每日已实现方差对数。<bookmark mark='a'/>下方是H为{float(keys[0]):.2f}的分数布朗模拟路径和布朗路径，缩放到近似相同的每日变动幅度。<bookmark mark='b'/>低H基准的增量负相关，但它不是平稳的均值回复过程。视觉相似不能识别潜在方差的概率规律；时间聚合与测量误差将在后面的争论中起作用。",

    "Their measurement rests on one property.":
        "他们的测量建立在一个性质上。如果对数方差的行为像分数布朗运动，那么它在滞后delta上的变化，与一个常数乘以delta的H次方再乘以标准正态变量同分布。"
        "<bookmark mark='a'/>取q阶绝对矩，尺度就提了出来：delta的qH次方。<bookmark mark='b'/>在对数刻度上，每个q都对应滞后的一条直线，"
        "而斜率zeta(q)与q成正比。比例就是H。<bookmark mark='c'/>一个提醒：我们观测到的是已实现方差，即一天的积分方差加上误差。"
        "第十一章会说明这有多大影响。",

    'f"The estimator fits a log-moment slope for each q, then regresses those slopes ':
        "估计量先对每个q拟合对数矩斜率，再把这些斜率对q做带自由截距的回归，回归斜率就是报告的H。<bookmark mark='a'/>每个选定H只使用一条固定模拟路径：H为十分之一、十分之三和二分之一时，读数为{chk[1]['est']:.2f}、{chk[2]['est']:.2f}和{chk[3]['est']:.2f}；H为零点零五时读作{chk[0]['est']:.2f}。每个值一条路径只能提示问题，不能证明统计偏差。比特币两个时期的读数为{r['H']:.2f}和{r18['H']:.2f}。它们概括有限滞后下的已实现方差代理，既非瞬时方差的直接观测，也不等于期权定价测度下的H。",

    'f"For each lag from one to fifty days and each q, plot an empirical moment. <boo':
        "对一至50天的各滞后和每个q，画出经验矩。<bookmark mark='a'/>对每种颜色拟合双对数直线；偏离直线的部分也属于证据。<bookmark mark='b'/>再把斜率对q回归，图中保留真实的自由截距直线，斜率为{r['H']:.2f}。理想分数布朗基准才满足zeta q严格等于qH。<bookmark mark='c'/>在这一基准下，若q等于二时的斜率为一，H是多少？<bookmark mark='d'/>二分之一。但单凭一个矩指数，不能确定过程就是布朗运动。",

    'f"Two era estimates: {r18[\'H\']:.2f} and {r[\'H\']:.2f}; after removing each full s':
        "两个时期估计为{r18['H']:.2f}和{r['H']:.2f}；去掉各完整样本的星期均值后，为{r18['H_deseasonalized']:.2f}和{a['btc_deseasonalized']:.2f}。<bookmark mark='a'/>所引股指研究也出现较低有限滞后指数。代理之间的相似不能识别瞬时方差正则性。后面比较采样、噪声与均值回复的解释。下面介绍粗糙预测器。",

    # ------------------------------------------------------------------ Forecast
    "Chapter four. Forecasting with a rough memory.": "第4章。用粗糙的记忆做预测。",

    'The fractional Brownian benchmark also gives a conditional-mean predictor from i':
        "分数布朗基准还给出利用整个过去的条件均值预测器。这里把其权重离散化，并在250天有限窗口内重新归一化。权重集中于近期观测，后面带有衰减尾部。<bookmark mark='a'/>预测期限增长时，最新观测的权重会增加还是减少？<bookmark mark='b'/>减少，权重向更远的过去分散。<bookmark mark='c'/>示意HAR阶梯结合当天值、五天均值与22天均值，可以近似分布滞后结构。这提供一种解释思路，不能证明HAR在所有市场表现良好的原因。",

    "The formula. In the rough fractional stochastic volatility model":
        "公式。在粗糙分数随机波动率模型里，对数方差等于nu乘以一个分数布朗运动，再加一个常数。<bookmark mark='a'/>给定全部过去，"
        "分数布朗运动在delta之后的期望值，是过去对这个核的积分，前面有一个常数：cos(H pi)除以pi。这是卡尔·纽兹曼和文森特·普尔的一个定理，"
        "也是粗糙性论文的公式5.1。<bookmark mark='b'/>这个常数从哪里来？代入t减s等于delta乘u：核的积分是pi除以cos(H pi)，"
        "所以这个常数只是让权重加起来等于一。预测就是过去的加权平均。<bookmark mark='c'/>在日度数据上，积分变成用这些权重的求和，"
        "并做归一化：这就是我们公司的函数，也就是你刚才看到的柱子。",

    'f"A retrospective comparison across two Bitcoin eras, at one, five and twenty da':
        "回顾性比较两个比特币时期，预测期限为一、五、20天。回归系数每20天重估，只使用当时已经观测到的目标。但粗糙预测器的H使用整个时期、包括测试日期的数据估计，因此不是完整的实时预测检验。<bookmark mark='a'/>图中显示较早时期的五天比较，保留全部观测值与预测值。<bookmark mark='b'/>六个期限与时期组合中，粗糙版本胜HAR {f['rough_wins']}次，HAR胜{6 - f['rough_wins']}次。评分分母使用测试期自身均值附近的变动，而预测时无法知道这个未来基准。20天时四种分数均为负。<bookmark mark='c'/>四个按时间划分的区段显示排名不稳定。这些数据可比较拟合预测器的形状，但没有证明可部署优势，也没有做统计优胜检验。",

    'A distinction about memory. Comte and Renault used fractional volatility with H ':
        "区分几种记忆。孔特与勒诺采用H大于二分之一的分数波动率表示长程依赖，这类分数布朗路径仍然不可微。<bookmark mark='a'/>H小于二分之一则表示更粗糙的路径和负相关的分数布朗增量。预测器依然对过去水平使用尾部权重，但这不等于H大于二分之一、增量正相关时通常所说的长程依赖。局部粗糙度、平稳长记忆和预测持续性是不同性质。下面介绍用于期权定价的粗糙贝尔戈米。",

    # ------------------------------------------------------------------ RBergomi
    "Chapter five. Rough Bergomi.": "第5章。粗糙贝尔戈米模型。",

    'Bayer, Friz and Gatheral introduced rough Bergomi in 2016. Its instantaneous var':
        "拜尔、弗里茨与盖瑟尔2016年提出粗糙贝尔戈米。瞬时方差等于初始远期方差曲线乘补偿后的高斯指数。这里的驱动是黎曼—刘维尔沃尔泰拉过程，并非具有平稳增量的完整分数布朗运动。输入曲线来自第十三部分有限执行价市场构造，并保持固定。<bookmark mark='a'/>再拟合三个参数H、eta和rho。期望方差等于输入曲线是模型恒等式，不代表每个期权标记价格都被精确匹配。",

    "The Itô isometry gives the driver's variance as t to two H. <bookmark mark='a'/>":
        "伊藤等距给出驱动方差为t的二H次方。<bookmark mark='a'/>中心高斯指数配上图中的补偿项，均值为一，因此瞬时方差期望等于输入xi零的t。eta加倍会改变该期望吗？<bookmark mark='b'/>不会。固定未来日期t，在s时刻条件化，得到图中关于s的指数鞅。这证明远期方差恒等式，不代表瞬时方差是鞅，也不能单独证明股票是真鞅。在通常条件下，标准粗糙贝尔戈米结果对非正rho保证股票的该性质。<bookmark mark='c'/>自然状态仍是一条曲线，现价和当前方差本身不能构成有限维马尔可夫状态。",

    'The kernel is singular, so a finite-grid simulator needs care. The hybrid scheme':
        "核具有奇点，有限网格模拟需要谨慎。混合格式解析处理最近的格子，近似其余部分。<bookmark mark='a'/>这四条路径使用拟合参数，但方差曲线为示意平坦曲线。负rho耦合驱动，使价格下跌通常与波动率上升相联系，却不保证每次波动率尖峰都伴随下跌。图中每条样本都是有限网格实现。",

    'f"Now watch it calibrate. On the right, the fit error after every evaluation of ':
        "现在看它校准。右边是每次模型求值之后的拟合误差，取迄今为止最好的；色带是三组随机数之间的离散。左边是模型在三个到期日上的微笑，对照以点表示的基准曲面报价。<bookmark mark='a'/>它从一个猜测出发：H为十分之一，波动率的波动率不大。优化器把H往下推，把eta往上推：短期微笑变陡，去贴合报价。<bookmark mark='b'/>在三组随机种子上，拟合出的H落在{min(Hs):.2f}和{max(Hs):.2f}之间，在新的路径上重新定价后误差在{min(oos):.2f}和{max(oos):.2f}个波动率点之间。期权所要求的粗糙度是极端的。这里是在同一批市场标记价格上更换模拟种子，不是未见过的市场日期。H范围还受到优化器、网格与固定方差曲线选择的影响。",

    'f"The headline fit, on twenty thousand paths: roughness {p[\'H\']:.2f}, vol of vol':
        "主拟合，在两万条路径上：粗糙度{p['H']:.2f}，波动率的波动率{p['eta']:.1f}，相关系数{p['rho']:.2f}，在新路径上的误差为{rb['rmse']:.2f}个波动率点。<bookmark mark='a'/>在同样的报价上，第13部分的赫斯顿误差为{rs['heston_rmse_same']:.2f}，用了五个自由数字和一个荒谬的波动率的波动率。三个数加上市场的方差曲线胜过了五个数。第17部分每周校准这个模型，用一个神经网络代替蒙特卡洛。这个模型的每个数都来自模拟粗糙路径。下一章：怎样做对。方差曲线是额外的市场输入。模型结构与有限数值预算不同，使这个单日比较有局限。",

    # ------------------------------------------------------------------ Hybrid
    "Chapter six. Simulating a rough path: the hybrid scheme.": "第6章。模拟粗糙路径：混合格式。",

    "Rough Bergomi's driver is an integral of past shocks":
        "粗糙贝尔戈米的驱动是过去冲击对核“t减s的H减二分之一次方”的积分。这里是t之前最后六个时间步上的它。在s等于t处它冲向无穷：正是这个尖峰让路径变得粗糙。"
        "<bookmark mark='a'/>朴素格式，即黎曼和，在每个格子的左端对核采样一次，在它下面堆柱子。远离t时柱子没问题。在最后一个格子里，它们几乎什么都没抓住："
        "红色的面积。<bookmark mark='b'/>停下来预测一下：H减小时，谁的误差会变大？<bookmark mark='c'/>朴素格式的：H越小，方差越多地集中在尖峰里。"
        "<bookmark mark='d'/>米克尔·本内德森、阿斯格·伦德和米科·帕卡宁的混合格式做两件事。它精确地积分第一个格子，连同尖峰一起，"
        "用一对相关的正态抽样。对其他格子，它不在边缘处计算核，而是在点b_k处，使单根柱子恰好拥有这个格子的面积。",

    "The algebra. On the first cell, the Brownian increment":
        "代数。在第一个格子上，布朗增量和奇异核的积分是一对相关的高斯变量，协方差就是这个，直接来自伊藤等距。把它们一起抽样，尖峰就被精确处理了。"
        "<bookmark mark='a'/>对往回k步的格子，取核等于它在该格子上自身平均值的那个点b_k。<bookmark mark='b'/>于是粗糙驱动就是精确的第一个格子，"
        "加上固定权重乘以过去增量之和：一个因果卷积。<bookmark mark='c'/>而卷积用快速傅里叶变换计算，每条路径n log n次运算，"
        "精确模拟则要分解一个n乘n的协方差矩阵。",

    'Here is that convolution, done slowly. The grey bars are the shocks. The rough k':
        '这就是那个卷积，慢速演示。灰色的柱子是冲击。粗糙核的权重，在最新的冲击上最高，沿着它们滑动；在每个位置，加权和就是粗糙驱动的一个值，画在下面。快速傅里叶变换一次算出所有位置。本动画使用24个截断的远端取值权重，并将输出标准化。前面的公式和实验展示的才是实际混合格式。',

    'f"The House\'s version, abridged to its essentials: the covariance of the first c':
        "这是我们公司的版本，删减到要点：第一个格子的协方差和它的乔列斯基因子，最优点，用FFT做的卷积，以及方差。<bookmark mark='a'/>运行真正重要的检验：粗糙驱动在时刻一的方差恰好是一。H为0.05时，混合格式给出{r05['hybrid']:.2f}；朴素求和给出{r05['riemann']:.2f}，有一半以上的方差丢在了尖峰里。当H升到十分之三，朴素格式的误差缩小，正如图像所说。<bookmark mark='b'/>在价格上，损害是巨大的：粗糙贝尔戈米30天平值波动率用混合格式是{100 * at['hybrid']:.0f}%，用朴素格式是{100 * at['riemann']:.0f}%。<bookmark mark='c'/>在速度上，混合格式按n log n增长，{verdict}。模拟很慢。下一章：一个有近似闭式解的粗糙模型——粗糙赫斯顿模型。这些是带模拟误差的有限网格估计。乔列斯基计时采用分数布朗协方差，混合计时采用沃尔泰拉驱动；它说明计算成本，并非同一概率规律下的精度比较。",

    "and by four thousand steps the exact Cholesky factorisation": "到四千步时，精确的乔列斯基分解是两者中较慢的那个",
    "though at these sizes an exact Cholesky factorisation is still competitive":
        "不过在这些规模上，精确的乔列斯基分解在这台机器上仍有竞争力：混合格式真正的优势是在任何网格上都准确，而代价增长平缓",

    # ------------------------------------------------------------------ RHeston
    "Chapter seven. Rough Heston:": "第7章。粗糙赫斯顿：沃尔泰拉方程与它的里卡蒂方程。",

    "Rough Bergomi has no closed form. Omar El Euch and Mathieu Rosenbaum":
        "粗糙贝尔戈米没有闭式解。奥马尔·埃勒尤赫和马蒂厄·罗森鲍姆找到了一个保留赫斯顿优点的粗糙模型，入口是换一种方式写赫斯顿的方差："
        "今天的值等于初始值，加上对每一次过去推动的记忆，即均值回复的漂移和随机冲击，每一次都由一个核加权。<bookmark mark='a'/>"
        "对赫斯顿来说核是常数：每一次推动都被完整记住。这是由一组冲击驱动的一条方差路径。<bookmark mark='b'/>现在只改变核，"
        "换成H为十分之三、然后十分之一的幂律：最近的推动分量极重，久远的逐渐淡去。同样的冲击，路径变得参差不齐。这就是粗糙赫斯顿。",

    "Now the derivation. Rough Heston's variance is Heston's":
        "现在推导。粗糙赫斯顿的方差就是赫斯顿的方差，只是把常数核换成分数阶核：t的alpha减一次方除以gamma(alpha)，其中alpha等于H加二分之一。"
        "<bookmark mark='a'/>它是一个仿射沃尔泰拉过程，对这类过程，爱德华多·阿比·贾贝尔、马丁·拉尔松和塞尔吉奥·普利多证明，"
        "对数特征函数是函数F(h)对初始曲线g_0的积分。<bookmark mark='b'/>h本身满足一个卷积方程，而与分数阶核的卷积就是分数阶积分。"
        "把它反过来：h的分数阶导数等于赫斯顿自己的里卡蒂方程右端。<bookmark mark='c'/>代入g_0，特征函数就是h的两个分数阶积分的指数："
        "埃勒尤赫和罗森鲍姆的公式。h没有闭式解，但只有一个方程，对每个频率解一次。<bookmark mark='d'/>停下来预测一下：令H等于二分之一，"
        "会得到什么？<bookmark mark='e'/>alpha等于一，分数阶导数就是普通导数，这就是赫斯顿的里卡蒂方程。我们公司的测试正是在检查这一点。",

    'f"With all six parameters free, the original local numerical fit gives H of {p[\'':
        "六参数自由时，原始局部数值拟合给出H为{p['H']:.2f}、波动率的波动率{p['nu']:.1f}、均值回复{p['lambda']:.0f}，误差{rh['rmse']:.2f}个波动率点。<bookmark mark='a'/>固定H为十分之一再拟合，误差为{r1['rmse']:.2f}，波动率的波动率为{x1[3]:.1f}，均值回复为{x1[1]:.0f}。<bookmark mark='b'/>不同参数组合对本日期拟合较接近。这不是统计等价检验，也不能要求实际测度与风险中性测度的H相同。八十步分数亚当斯、COS误差、局部优化、边界与报价权重都会影响比较。下一章显示更完整的数值剖面。",

    'Compare finite-maturity skew magnitudes on this one date. Dots come from market ':
        "比较同一日期的有限期限偏斜绝对值。白点来自市场SVI有限差分。<bookmark mark='a'/>粗糙贝尔戈米使用输入的市场远期方差曲线，图中偏斜也包含蒙特卡洛和网格误差。<bookmark mark='b'/>两条粗糙赫斯顿曲线使用不同拟合参数与分数亚当斯求解器。短端水平与局部凸起，是这些数值实现的结果。没有曲线匹配每个期限；本比较不能把核的作用与方差曲线输入、校准选择和数值误差分离，也没有检验精确零期限渐近规律。下面介绍分数求解器。",

    # ------------------------------------------------------------------ Adams
    "Chapter eight. Solving it:": "第8章。求解：分数阶亚当斯格式，以及H的剖面。",

    "How do you solve an equation with a fractional derivative?":
        "怎样求解一个带分数阶导数的方程？把它写成积分方程：h在时刻t等于F(h)的分数阶积分。<bookmark mark='a'/>然后沿网格推进，"
        "就像常微分方程求解器那样，但对核做精确积分。预测步在每个过去的格子上把F当作常数。<bookmark mark='b'/>校正步把F当作网格点之间的线性函数，"
        "并在新点上使用预测值：乘积梯形法则。这就是凯·迪特尔姆、内维尔·福特和艾伦·弗里德的分数阶亚当斯格式。<bookmark mark='c'/>"
        "与普通求解器的区别：每个新点都需要整个过去。这个记忆求和让n步的代价变成n的平方。",

    "Watch it run, for ten frequencies u at once":
        "看它运行，同时对十个频率u，跨越30天。在每一步，黄色的线就是记忆：每一个更早的点都被拉进下一个点。灰色的点是预测步的猜测，黄色的点是校正后的值。<bookmark mark='a'/>常微分方程只需要上一个点。这里每一步都有整把历史的扇子到达，这就是为什么粗糙模型曾被认为很慢，也是为什么几毫秒仍然是一项成就。",

    'f"The House\'s code: the predictor weights, the corrector weights, and the update':
        "我们公司的代码：预测权重、校正权重和更新，几行代码同时处理所有频率。<bookmark mark='a'/>停下来预测一下：把步数加倍，误差缩小多少？<bookmark mark='b'/>对照一个1600步的解来运行。步数每加倍一次，误差大约下降到三分之一：观测到的阶数为{a['order']:.1f}。而把H设为二分之一时，这个格式与赫斯顿的闭式特征函数吻合，{match}。这个拟合阶数仅对应本参数、频率网格与1600步参考解，不是普遍的亚当斯收敛定理。",


    'Here is the modulus of the computed characteristic function over frequency and m':
        "这里是数值特征函数的模随频率和期限的变化，先看赫斯顿极限。归一化特征函数在零频率处等于一。<bookmark mark='a'/>保持其他参数不变，把H改为十分之一，数值函数的模发生变化。它描述傅里叶空间的衰减，却不能识别偏度的符号，因为把分布左右反射不会改变这个模。较低的脊线也不能单独证明所有意义上的分布都更宽。复特征函数及进一步计算的期权价格才包含微笑信息。",

    'f"Fix H at nine values and refit the other five parameters. <bookmark mark=\'a\'/>':
        "将H固定在九个值，并重估其余五个参数。<bookmark mark='a'/>H为零点零五时误差{e05['rmse']:.2f}，十分之一时{e01['rmse']:.2f}；自由拟合H为{free['H']:.2f}，误差{free['rmse']:.2f}。绿色区域描述时间序列代理估计，不是风险中性H的置信区间。<bookmark mark='b'/>期限柱形保留全部误差，包括最大的短端偏差。此目标与预算下的单日局部数值拟合偏好更大H，不能识别普遍市场H。下面介绍一种订单流机制。",

    # ------------------------------------------------------------------ Hawkes
    "Chapter nine. Where roughness comes from:": "第9章。粗糙从何而来：近乎不稳定的订单流。",

    'Hawkes models illustrate reactive order arrivals. Each event temporarily raises ':
        "霍克斯模型示意反应性订单到达：每次事件暂时抬高条件到达强度。三个指数核例子的基准强度对应相同平稳均值，再各自除以有限样本均值。<bookmark mark='a'/>这里分枝比十分之九比二分之一聚集更强。<bookmark mark='b'/>接近一时，事件家族可能很大。这是合成活动示意，不是经验分枝比拟合，也不能证明粗糙波动率。下面引入重尾核与协调的近临界极限。",

    'Now a branching representation with a heavy-tailed Lomax delay kernel, rather th':
        "现在采用重尾Lomax延迟核的分枝表示，不同于前面的指数核。移民事件触发子代，子代再触发后续世代。<bookmark mark='a'/>分枝比十分之九时，在有限时域截断之前，平稳移民家族平均十个成员。<bookmark mark='b'/>分枝比0.99时，平稳事件中后代而非移民占多少？<bookmark mark='c'/>99%，每个家族平均100个成员。图中有限树只保留所示世代与时域；这些平稳期望不是图中的精确事件数。",

    'Start with Hawkes intensity: a baseline plus past events weighted by a kernel. <':
        "从霍克斯强度出发：基准加上按核加权的过去事件。<bookmark mark='a'/>取期望得到更新方程。<bookmark mark='b'/>预解核是各卷积幂的和，每一项对应一个世代。<bookmark mark='c'/>贾森与罗森鲍姆令重尾参数alpha介于二分之一与一之间，采用近临界分枝序列，并协调缩放时间、基准强度与振幅。缩放后的预解核趋于Mittag--Leffler密度，在零附近正比于t的alpha减一次方。<bookmark mark='d'/>2016年定理得到H等于alpha减二分之一的积分分数CIR极限。价格过程与杠杆需要额外建模假设。前面的有限模拟没有实现完整极限序列。",

    'A finite-scale illustration, not a limit theorem in motion. We show log binned c':
        '这是一段有限尺度示意，并非极限定理的动态证明。图中为分枝比0.9999的一次霍克斯模拟的分箱计数对数，零计数先抬至一再取对数。显示窗口从200扩至二万箱时，每段独立按极差归一化并下采样。留下的不规则性只是这一条样本的视觉特征。定理需要过程、基准强度与时间范围共同缩放的一系列模型；本动画没有实现这一序列。',

    'f"Apply the same finite-lag estimator to log binned activity, with three fixed s':
        "把同一个有限滞后估计量用于分箱活动对数，每个分枝比取三个固定种子。<bookmark mark='a'/>分枝比二分之一时，估计均值为{lo:.2f}，接近滞后无关的计数噪声。本扫描最大的均值为{hi:.2f}。这里H增大表示有限滞后矩斜率更陡，不表示局部更粗糙。<bookmark mark='b'/>改变尾部参数没有跟随极限公式，三种尾部的读数都接近十分之一。贾森与罗森鲍姆定理要求alpha在二分之一与一之间、分枝比趋近临界，并对时间、基准强度与振幅协调缩放，得到H等于alpha减二分之一的积分分数CIR极限。这些固定有限模拟没有检验全部假设。<bookmark mark='c'/>多变量推广把特定买卖不对称及无套利假设与杠杆联系起来，另一些市场冲击模型把反应性订单流与粗糙极限联系起来。它们是基于模型的机制，不能从聚集现象普遍推断。下面介绍马尔可夫提升。",

    # ------------------------------------------------------------------ Lift
    "Chapter ten. Markovian lifts.": "第10章。马尔可夫提升。",

    'The fractional kernel admits an exact continuum mixture of exponentials. A finit':
        "分数核可以精确表示为指数函数的连续混合。有限和可在选定滞后区间近似它，并恢复有限马尔可夫状态。这里程序使用正权重的几何量化，增加因子数会同时改变速率与权重。<bookmark mark='a'/>仅作规划启发，假设一个因子覆盖一个数量级，从一分钟到一年跨多少个数量级？<bookmark mark='b'/>约五点七，可先猜六个，但这不保证精度。所需数量还取决于H、滞后区间、求积方法和误差容限。有限指数和在零处有界，无法精确再现奇点。",

    "Why is a power law a mixture of exponentials?":
        "为什么幂律是指数的混合？把e的负xt次方对x的负alpha次方积分：代入y等于xt，得到gamma(1减alpha)乘t的alpha减一次方。<bookmark mark='a'/>所以分数阶核恰好是指数对一个混合测度的积分：一个完全单调函数。<bookmark mark='b'/>把积分换成N个带权重的节点，核就变成一个有限和。<bookmark mark='c'/>每个指数成为一个因子U_i，有自己的均值回复速度x_i，全部由同一个布朗运动驱动。方差等于初始曲线加上因子的加权和：一个N加一维的马尔可夫模型，也就是爱德华多·阿比·贾贝尔的提升赫斯顿模型，用20个因子就很实用。",

    'The white curve is a numerical Volterra Euler reference with cell-averaged fract':
        "白线是采用格点平均分数核、五百时间步的沃尔泰拉欧拉数值参考解，不是连续粗糙赫斯顿的精确路径。图中保留数值方差的负值，尽管模拟在平方根内对方差取非负下限。再比较由相同布朗增量驱动的提升模型。<bookmark mark='a'/>一个、五个、二十、五十、200因子以不同速度接近该参考解。参考解与提升解都有离散误差；这种耦合路径比较不能单独分离纯核误差，也不能确定连续时间收敛阶。",

    'f"Compare the thirty-day smile to the fractional-Adams numerical reference at H ':
        "把30天微笑与H为十分之一的分数亚当斯数值参考解比较。<bookmark mark='a'/>一个因子误差为{rows[0]['iv_err']:.1f}个波动率点，十个为{rows[3]['iv_err']:.1f}，20个为{rows[4]['iv_err']:.1f}，50个为{rows[5]['iv_err']:.2f}。这些是十三个执行价上的有限网格价格差，不是误差定理。路径实验使用200条耦合路径；五十因子相对欧拉参考解的均方根距离为参考标准差的{lp['rows'][3]['dist']:.2f}倍。边际期权价格可以相近，而耦合路径仍明显不同。路径依赖产品与对冲需要重视这种区别。",

    # ------------------------------------------------------------------ Debate
    "Chapter eleven. The debate, part one:": "第11章。争论之一：时间序列在愚弄我们吗？",

    'f"Not everyone accepts that volatility is rough.':
        "并不是每个人都接受波动率是粗糙的。先看我们自己数据里的一个陷阱：比特币的周末很平静，周六的已实现波动率大约是工作日的一半。"
        "<bookmark mark='a'/>这个每周的节奏每天上下跳动，估计量把它读成了粗糙性。去掉它，H从{a['btc']:.2f}升到"
        "{a['btc_deseasonalized']:.2f}。仍然粗糙，但这个数字的变化是因为日历，而不是自然规律。",

    'Cont and Das study how measurement can affect apparent roughness. These three si':
        "孔特与达斯研究测量如何影响表观粗糙度。这三个模拟方差过程具有布朗局部正则性，均值回复速度不同。<bookmark mark='a'/>较慢的例子经每日已实现方差测量读作约十分之四。<bookmark mark='b'/>较快的例子接近零：每日滞后斜率小，不一定表示局部H小。这些是固定合成示例，不是普遍的估计偏差定理。<bookmark mark='c'/>下面看四种子参数图。",

    'f"Here is the estimator\'s bias map, the centrepiece of the debate. On the floor,':
        "这是估计量的偏差图，这场争论的核心。地面上是一个模拟对数波动率的两个旋钮：它的真实H，从非常粗糙到布朗运动；以及它均值回复的快慢，从完全不回复到半衰期五小时，每个都模拟七百天，并按比特币的方式测量。高度是估计量报告的H。<bookmark mark='a'/>停下来预测一下：一个布朗正则的波动率，H为二分之一，半衰期一天。估计量会报告什么？<bookmark mark='b'/>大约十分之一：{M[i05, j1]:.2f}。比特币的数字。<bookmark mark='c'/>现在在比特币的读数{lvl:.2f}处把这张图切开。金色曲线是所有读起来恰好像比特币的真实粗糙度与均值回复的组合：从非常粗糙、均值回复缓慢，到布朗正则、半衰期大约一天。一个数字无法在它们之间做出选择。<bookmark mark='d'/>还要注意，在左后方，没有均值回复时，真实H为0.05读出来是{M[i005, 0]:.2f}：一天内的平均让路径变平滑，把估计值往上推，而均值回复和噪声把它往下拉。曲面是每格四个固定种子的平均，并在六十四个参数格间插值。等高线只是平均读数相同的描述，不是置信集合，也不能证明生成数据的规律相同。",

    'Why can a low fitted exponent be ambiguous? First, daily realized variance integ':
        "为什么低拟合指数有歧义？第一，每日已实现方差聚合了潜在方差并包含测量误差。<bookmark mark='a'/>在简化的独立加性对数代理噪声模型中，二阶增量矩增加一个与滞后无关的底部，使拟合斜率降低；这不是对所有q与噪声模型都成立的加性公式。<bookmark mark='b'/>第二，平稳均值回复使增量方差在特征时间之外饱和。每日滞后因此可能读到近零斜率，却不能识别局部路径正则性。<bookmark mark='c'/>第三，Chong等人2024年的极小极大理论针对通过高频价格观测的指定粗糙波动率参数模型，H的估计速率为n的负一除以四H加二次方。该结果中H越小，指数对应的速度越快，接近平方根n速率。它不能认证这里简单的每日估计量，也不给这些拟合曲面提供置信区间。",

    "The statistics literature took this seriously.":
        "统计学文献认真对待了这一点。深泽正彰、高畠哲也和丽贝卡·韦斯特法尔对测量误差建模，仍然发现波动率是粗糙的。<bookmark mark='a'/>"
        "安妮·博尔科及其合作者用广义矩方法修正了它：H仍约为0.05。<bookmark mark='b'/>拉玛·孔特和普尔巴·达斯展示了我们刚才模拟的那种假象。"
        "<bookmark mark='c'/>而极小极大理论说明，一个数字能确定的东西有多少。什么能把它们区分开？短于一天的滞后，以及期权。这是下一章。"
        "下一章：期权怎么说。",

    # ------------------------------------------------------------------ Options
    "Chapter twelve. The debate, part two:": "第12章。争论之二：期权怎么说。",

    'f"Return to the original weekly fits. Gold indicates that the shifted power law ':
        "回到原始逐周拟合。金色表示平移幂律把报告的未加权对数均方根误差降低超过零点零一，否则橙色显示普通幂律。<bookmark mark='a'/>共{len(weeks)}个日期，其中{int(sum(better))}个为金色。这是人为选定的样本内门槛，没有复杂度惩罚，也没有显著性检验。指数约束不同，因此两族拟合并非完全嵌套。<bookmark mark='b'/>金色日期的拟合平移量中位数为{w['eps_median_days']:.0f}天。平移量概括观测期限上的曲率，不是测得的真实市场偏斜停止增长边界。两种颜色都不能确定零期限行为。",

    "so for most weeks the power law is as good a description as its rival": "所以对大多数周来说，幂律和它的对手是一样好的描述",
    "so for most weeks the skew does stop growing at the shortest expiries": "所以对大多数周来说，偏斜确实在最短的到期日上停止增长",

    'Selected published comparisons. Livieri and co-authors study temporal scaling in':
        "选读已发表比较。Livieri等人研究隐含波动率代理的时间尺度规律，并非直接测量到期微笑导数。<bookmark mark='a'/>Rømer用SPX及SPX与VIX联合数据比较单因子粗糙模型与经典选择。<bookmark mark='b'/>Guyon与El Amrani质疑未平移幂律在最短观测期限的拟合。<bookmark mark='c'/>Abi Jaber与Li的2025年研究中，特定非粗糙路径依赖和两因子马尔可夫模型在其SPX样本上拟合更好。结论针对所测模型族、校准目标与数据集，不排除所有粗糙构造。",

    "Why can a classical two-factor model compete? Give Bergomi's kernel two exponent":
        "为什么一个经典的两因子模型能与之竞争？给贝尔戈米的核两个指数，一快一慢。<bookmark mark='a'/>把第二章的公式逐项应用，得到两个偏斜之和，每个在自己的时间尺度以下是平的，以上则像T分之一那样下降。<bookmark mark='b'/>停下来预测一下：半衰期为五天和一年时，这一对能否在一周到六个月上假冒一条幂律？<bookmark mark='c'/>近似地，可以：在两个时间尺度之间，和从一种状态平滑地弯向另一种，在双对数图上看起来是直的。它就是第十章中两个因子的提升，并不声称有任何粗糙性。该首阶示意还需要适当的相对振幅与杠杆载荷；两个衰减率不能确定唯一的幂律指数。",

    'f"Now our own race, on the Surface\'s quotes.':
        "现在是我们自己的比赛，在基准曲面的报价上。一个带第13部分方差曲线的两因子贝尔戈米模型，五个数在两万条路径上用最小二乘拟合，拟合过程回放。"
        "<bookmark mark='a'/>拟合出的半衰期是{hl[0]:.1f}天和{hl[1]:.0f}天：一个快因子和一个慢因子，正如代数所提示的。<bookmark mark='b'/>"
        "在新路径上重新定价，它的误差是{b2['rmse']:.2f}个波动率点，粗糙贝尔戈米是{rbm:.2f}。所以{verdict}。一个市场的一天什么也定不下来；"
        "诚实的解读是，粗糙模型和多因子模型在价格上是势均力敌的对手，选择取决于动态、速度和对冲。"
        "第三种观点认为，波动率由价格路径本身驱动。下一章。",

    "the two-factor model beats rough Bergomi on our Surface": "两因子模型在我们的基准曲面上胜过了粗糙贝尔戈米，正如阿比·贾贝尔和李在标普上发现的那样",
    "rough Bergomi still wins on our Surface, with fewer numbers": "粗糙贝尔戈米在我们的基准曲面上仍然获胜，而且用的数字更少",

    # ------------------------------------------------------------------ PDV
    'Chapter thirteen. Path-dependent volatility and implied-index tracking.': '第13章。路径依赖波动率与隐含指数跟踪。',

    "Guyon and Lekeufack's 2023 work studies volatility as a function of price histor":
        "Guyon与Lekeufack在2023年研究以价格历史决定波动率。先看一个经验隐含指数代理：常数加趋势特征，再加活动特征平方根。它与指定连续时间瞬时波动率定价模型不同。<bookmark mark='a'/>趋势对过去收益加权，活动对过去平方收益加权。这里最新纳入的收益，与目标指数收盘值属于同一天。<bookmark mark='b'/>平移幂律权重在零处有界，可在有限窗口缓慢衰减。重构R平方较高，不能证明不存在其他波动率创新，也不能证明当天收益尚未观测时即可预测该指数。",

    "Here is the model running.":
        "这是模型在运行。上面是比特币价格，逐日。在移动的日期后面，黄色的尾迹是活跃度核对每个过去日子的权重。右边是两个记忆：可以为负的趋势，"
        "和始终为正的活跃度。<bookmark mark='a'/>下面是仅由两个记忆重建的隐含波动率，对照DVOL：价格一抽动，两者一起跳。",

    'f"How is it fitted?':
        "它是怎么拟合的？四个形状参数，两个指数和两个平移，用非线性最小二乘搜索，而对每个候选，三个贝塔由普通回归得出：变量投影。"
        "右边是搜索过程中的误差；左边是每次改进时的两个核。<bookmark mark='a'/>趋势核收缩为短记忆；活跃度核稳定为一条平移了大约"
        "{365 * p['delta2']:.0f}天的幂律。在样本内，拟合解释了DVOL变化的{100 * p['r2_train']:.0f}%。",

    'f"Bitcoin\'s target is DVOL, a thirty-day implied-volatility index. Fit the kerne':
        "比特币目标为DVOL，即30天隐含波动率指数。用2021至2023年拟合核与回归，再固定用于2024及2025年。特征包含目标当天收益，因此是留出日期的跟踪，不是提前预测。<bookmark mark='a'/>训练R平方为{p['r2_train']:.2f}。<bookmark mark='b'/>后续日期为{p['r2_test']:.2f}；拟合的30天已实现波动率基准，相对测试期自身均值计算时R平方为负。<bookmark mark='c'/>在合并样本中，活动项标准差为{100 * p['contrib']['activity']:.0f}个指数点，趋势项为{100 * p['contrib']['trend']:.1f}。这些相关分量的尺度不是因果或增量方差分解。趋势指数还达到了搜索边界。结论仅描述这一拟合代理与样本，不能普遍声称比特币不在意收益方向。",

    'f"There is a Markovian version. Make each kernel a convex mix of two exponential':
        "它有一个马尔可夫版本。让每个核成为两个指数的凸组合。<bookmark mark='a'/>于是每个记忆是两个指数移动平均的混合，模型有四个因子，每个用一行更新：我们公司的代码正是这样。<bookmark mark='b'/>以同样方式拟合到比特币上：活跃度记忆分裂为一个{hl[2]:.0f}天的快因子和一个{hl[3]:.0f}天的慢因子。在样本外它解释了DVOL的{100 * q['r2_test']:.0f}%，幂律版本是{100 * q['tspl_test']:.0f}%：{verdict}。<bookmark mark='c'/>它是一个定义良好的随机微分方程吗？马塞尔·努茨和安德烈斯·里韦罗斯·巴尔德韦尼托证明了它是，埃尔韦·安德烈和本雅明·茹尔丹把这一点推广到一般的核。图中的指数移动平均是每日数据滤波器。连续反馈随机微分方程的定理有特定符号与参数域、正初始活动，并需分别讨论波动率正性和股票鞅性。这里无符号约束的经验回归没有验证这些条件。",

    "the Markovian version does better out of sample": "马尔可夫版本在样本外比它所替代的幂律核做得更好",
    "the Markovian version gives up a little out of sample": "马尔可夫版本在样本外略有损失，换来的是马尔可夫性",

    # ------------------------------------------------------------------ SPX
    "Chapter fourteen. Path-dependent volatility on the S&P 500": "第14章。标普500上的路径依赖波动率，以及2024年8月5日。",

    'f"Guyon and Lekeufack\'s home ground was the S&P 500 and the VIX. Replicate it. T':
        "居永和勒克富克的主场是标普500和VIX。复现它。输入只有美国市场自己从1986年起的日收益，用肯·弗伦奇的市值加权市场代替标普；目标是VIX。在2000到2018年上拟合，然后冻结。<bookmark mark='a'/>看三十年描画出来：互联网泡沫破裂、2008年、波动率末日、2020年3月。<bookmark mark='b'/>在样本内，它解释了VIX变化的{100 * s['r2_train']:.0f}%；在样本外，从2019到2025年，是{100 * s['r2_test']:.0f}%，而对过去一个月已实现波动率的线性关系只有{100 * s['r2_base_test']:.0f}%。VIX的大部分是市场所走路径的函数。这里用同日收益重构同日VIX收盘值，并采用不同的股票收益序列，因此是代理复现，不是事前预测，也不能证明VIX没有独立创新。",

    'f"Here, unlike Bitcoin, the trend matters. The fitted trend coefficient is negat':
        "在这里，与比特币不同，趋势很重要。拟合出的趋势系数为负：市场一直在下跌时，VIX更高。这就是杠杆效应，也是下一章宗巴赫效应的原材料。<bookmark mark='a'/>停下来预测一下：标普一天下跌百分之三。哪一项对预测的影响更大？<bookmark mark='b'/>两项都会推动它，而趋势带着符号：下跌让两者都升高，同样幅度的上涨提高活跃度，却降低趋势项。在样本期内，趋势项的一个标准差相当于{100 * s['contrib']['trend']:.1f}个VIX点，活跃度是{100 * s['contrib']['activity']:.1f}。<bookmark mark='c'/>一个提醒：趋势核的指数跑到了它取值范围的边缘，所以它的记忆比我们的窗口能确定的更长。<bookmark mark='d'/>而残差就是路径无法解释的一切。回归残差是这组拟合特征没有解释的部分，不等于所有可能价格路径模型都无法解释的部分。",

    'f"The fifth of August 2024. The yen carry trade was unwinding; Japan\'s Nikkei fe':
        "2024年8月5日。日元套息交易正在平仓；日本日经指数当天下跌{-100 * c['nikkei_0805']:.1f}%。在美国开盘前，VIX打出了六十五以上，据一份美国证券交易委员会的工作人员论文，而VIX期货保持在三十五以下。它收于{100 * a5['vix']:.2f}，上周五是{100 * a2['vix']:.2f}。<bookmark mark='a'/>只给路径依赖模型输入当天为止的收益：它给出{100 * a5['pdv']:.1f}。差距{gap:.0f}个点，就是路径无法解释的部分。<bookmark mark='b'/>那是什么？国际清算银行由卡拉姆菲尔·托多罗夫和格里戈里·维尔科夫所做的这次飙升的剖析，指向了报价：VIX是用报价而不是成交计算的，而看跌期权的买卖价差急剧扩大。证券交易委员会的工作人员论文与之一致。一次报价中的流动性事件，叠加在真实的去杠杆之上。<bookmark mark='c'/>作为对比，在波动率末日，2018年2月5日，VIX收于{100 * vm['vix']:.1f}，模型给出{100 * vm['pdv']:.1f}。PDV数值包含八月五日当天收益，对应收盘。开盘前VIX高点属于不同时间。所引报价机制有助于解释日内指数尖峰，但收盘回归残差不能识别其因果贡献。",

    'f"Bitcoin during the same episode. DVOL\'s hourly high on August fifth reaches {m':
        "同一事件中的比特币。八月五日DVOL小时最高达到{mx:.0f}。<bookmark mark='a'/>五分钟收益计算的当日已实现波动率年化为{rv5:.0f}%，它与30天隐含指数的期限和含义不同。<bookmark mark='b'/>纳入当天收益后，固定代理重构DVOL收盘为{100 * bp['pdv']:.0f}，观测为{100 * bp['dvol']:.0f}。这个接近结果不能证明比特币价格与股票期权报价之间的因果对比。<bookmark mark='c'/>右侧为原始七月三十一日和八月七日偏斜绝对值曲线，保留可用期限；它们既不测量开盘前VIX事件，也不能确定零期限极限。下面讨论SPX与VIX联合建模。",

    # ------------------------------------------------------------------ Joint
    "Chapter fifteen. Joint S&P and VIX:": "第15章。标普与VIX联合：二次粗糙赫斯顿，以及居永的难题。",

    'Joint SPX and VIX calibration asks one risk-neutral model to fit both markets. S':
        "SPX与VIX联合校准要求一个风险中性模型同时拟合两个市场。有些连续单因子模型在加陡SPX短端微笑后，会产生过高的VIX期权波动率。这是模型相关的矛盾，不是关于所有连续模型的定理。<bookmark mark='a'/>第十三部分用比特币示意相关机制，并没有联合校准SPX与VIX。<bookmark mark='b'/>这里介绍二次粗糙赫斯顿与Guyon的约束熵构造，再运行一个更简单的双边际数值运输示例。",

    "In 2020 Jim Gatheral, Paul Jusselin and Mathieu Rosenbaum":
        "2020年，吉姆·盖瑟尔、保罗·朱瑟兰和马蒂厄·罗森鲍姆提出了二次粗糙赫斯顿模型。Z是过去收益的粗糙加权平均，由与价格相同的布朗运动驱动。"
        "方差是Z的一条抛物线：a乘以Z减b的平方，再加c。<bookmark mark='a'/>停下来预测一下：一次急涨，波动率上升还是下降？<bookmark mark='b'/>"
        "看黄色的点随路径展开沿抛物线移动。下跌把Z往下推，波动率沿左臂上升。足够大的上涨把Z推过b，波动率沿右臂上升。这种凸性让波动率的波动率依赖于状态，"
        "并让VIX微笑向上倾斜。他们用这六个数，在2017年5月19日同时拟合了标普和VIX的微笑。",

    'f"That feedback has a signature in the time series, the Zumbach effect: markets ':
        "这种反馈在时间序列里留下了印记，即宗巴赫效应：市场不是时间可逆的。过去一个月的大幅变动对下一个月高已实现波动率的预测，好于过去的高波动率对大幅变动的预测。<bookmark mark='a'/>用20天的窗口来测量。在二次粗糙赫斯顿路径中，正向相关是{z['qRH'][0]:.2f}，反向是{z['qRH'][1]:.2f}。在1990年以来的美国市场中，是{z['market'][0]:.2f}对{z['market'][1]:.2f}：{verdict}。<bookmark mark='b'/>粗糙贝尔戈米没有从价格到波动率的反馈，接近对称：{z['rBergomi'][0]:.2f}对{z['rBergomi'][1]:.2f}。模拟相关采用示意风险中性动态，历史相关采用实际市场数据，窗口相互重叠。这个定性比较不是统计检验。没有显式收益反馈的杠杆模型也可能产生弱Zumbach不对称。",

    "the asymmetry is there in both the model and the market": "模型和市场里都有这种不对称",
    "the asymmetry does not show in both the model and the market": "这种不对称并没有同时出现在模型和市场里",

    "The mathematics, in four lines.":
        "数学，分四行。二次粗糙赫斯顿的动态，用论文自己的参数形式。<bookmark mark='a'/>VIX的平方是未来30天对数合约的市场价格，条件意义下：第12部分的公式。<bookmark mark='b'/>由詹森不等式，VIX期货至多是一个远期方差互换的平方根，而后者由标普微笑确定：两个市场通过凸序绑在一起。<bookmark mark='c'/>居永的精确回答发表于2024年，是一个受离散度约束的鞅薛定谔问题：在所有匹配两个日期的标普微笑和VIX微笑的鞅模型中，取相对熵意义下最接近参考模型的那一个，用类似辛克霍恩的迭代求出，就像第9部分那样。",

    'f"An illustration using Bitcoin smiles near {jb[\'T1\'] * 365:.0f} and {jb[\'T2\'] *':
        "用比特币约{jb['T1'] * 365:.0f}天和{jb['T2'] * 365:.0f}天的微笑作示意。由SVI得到的密度经过截断与离散，第二个支撑又被调整以满足凸序。在该有限鞅网格上，优化两日期间对数收益绝对值。<bookmark mark='a'/>约束残差下降，上界方向最终约为十亿分之一。熵正则给出内部目标值{lo['value']:.3f}和{up['value']:.3f}；无正则线性规划给出图中更宽的网格区间。<bookmark mark='b'/>独立蒙特卡洛得到粗糙贝尔戈米数值{jb['rbergomi']:.3f}，位置仅作比较，不认证其边际等于修正后的网格边际。它们不是完整原始市场微笑的严格界。Guyon三边际构造还施加VIX分布及条件对数合约一致性，而这个双边际求解器没有这两项。下面介绍签名波动率。",

    "inside the interval, as any model that fits both smiles must be": "落在区间之内，任何拟合两个微笑的模型都必须如此",
    "outside the interval: a sign of Monte Carlo error": "落在区间之外：这是蒙特卡洛误差的迹象",

    # ------------------------------------------------------------------ Signature
    "Chapter sixteen. Signature volatility models.": "第16章。签名波动率模型。",

    "Christa Cuchiero, Guido Gazzani and Sara Svaluto-Ferro asked:":
        "克里斯塔·库切罗、圭多·加扎尼和萨拉·斯瓦卢托-费罗问：如果波动率是路径签名的线性函数会怎样？第5部分构造了签名，即路径的迭代积分。"
        "这是驱动路径，时间和一个布朗运动在一起。随着它展开，它到第三层的签名，十五个数，在右边生长：增量、面积、更高阶的迭代积分。"
        "<bookmark mark='a'/>波动率是这十五根柱子的加权和，画在下面：一个由路径自身几何构建的路径依赖波动率。<bookmark mark='b'/>"
        "停下来预测一下：只保留第一层，一个常数、时间和W。那是什么模型？<bookmark mark='c'/>波动率是一个高斯驱动的线性函数：斯坦-斯坦型模型。"
        "更高的层次增加路径依赖。",

    'Here is why this is clever. Volatility is the inner product of a parameter vecto':
        "这就是它的巧妙之处。波动率是参数向量ell与签名的内积。<bookmark mark='a'/>对数价格是sigma的随机积分减去它二次变差的一半。因为sigma对ell是线性的，第一项对ell是线性的，第二项是二次的：ell转置A减二分之一ell转置B ell。<bookmark mark='b'/>A和B只依赖于模拟的路径。把它们存一次，对布朗运动和它的独立伙伴都存，相关系数rho也就可以自由选取。<bookmark mark='c'/>而签名的线性泛函可以逼近路径的任何连续函数，所以这个模型族想多丰富就有多丰富。普适逼近讨论适当紧集上时间增广几何路径的签名深度不断增加；固定三阶模型只是很小的子类。期权校准对参数仍是非线性的。",

    'f"In the House, pricing a new parameter vector is three lines of linear algebra ':
        "在我们公司，给一个新的参数向量定价，只是对存好的数组做三行线性代数：不需要新的模拟。每次调用同时给每条路径、每个到期日定价。<bookmark mark='a'/>在一组一万条路径上拟合基准曲面，误差为{s['rmse_in']:.2f}个波动率点；在一组新路径上是{s['rmse_out']:.2f}。代码将各到期日模拟终值除以其样本均值。这个数值修正不能证明存在动态一致的单一真鞅模型。线性签名载荷可以有正有负，更换路径仍使用同一批市场标记价格。",

    'f"Watch the sixteen numbers calibrate:':
        "看这十六个数校准：右边是误差，左边是三个到期日上的微笑。因为每次求值只是线性代数，搜索很便宜。<bookmark mark='a'/>"
        "在新路径上重新定价，我们基准曲面上的得分：粗糙贝尔戈米、两因子贝尔戈米模型和签名模型。最低的是：{best_name}。<bookmark mark='b'/>"
        "与扬卡·默勒一起，同一个团队在2025年证明，签名模型能联合拟合标普和VIX期权，既不需要跳跃也不需要粗糙性：又一次，是路径依赖在起作用。"
        "下一章：交易台实际在用什么，以及我们公司的粗糙实验室。",

    # ------------------------------------------------------------------ House
    "Chapter seventeen. What desks use, and the rough lab.": "第17章。交易台用什么，以及粗糙实验室。",

    'f"These timings compare single pricing-map evaluations, not completed calibratio':
        "这些计时比较单次定价映射求值，不是完整校准。蒙特卡洛、分数亚当斯与提升赫斯顿计算的输出、离散方法和精度也不同。单凭它们能判断五秒校准时限吗？<bookmark mark='a'/>不能。第十七部分原始基准比较神经映射与它模仿的蒙特卡洛映射，测得单次求值比约{ratio:,.0f}倍。训练属于离线成本，替代器受到训练域与近似误差限制。第十四部分其他柱形记录的是这些实现于共享机器上的速度。<bookmark mark='b'/>总校准时间还取决于优化求值次数、导数、数据处理与精度要求。这说明加快映射的动机，不能确定普遍的交易台时限或行业采用程度。",

    'Published work on faster calibration. Bayer and Stemper train a pricing map offl':
        "加快校准的文献。拜尔与Stemper离线训练定价映射；Horvath、Muguruza与Tomas发展深度校准；罗森鲍姆与Zhang将神经方法用于二次粗糙赫斯顿及SPX与VIX联合拟合。<bookmark mark='a'/>替代器在训练域内代替重复数值定价。<bookmark mark='b'/>第十七部分实现一个原始基准，表现针对该设置。<bookmark mark='c'/>远期方差对冲理论使用覆盖相关曲线风险的工具。有限数量可交易方差互换，并不自动对冲每个曲线方向或使市场完备。",

    "Recognition, from both sides.":
        "来自双方的认可。Risk杂志把吉姆·盖瑟尔和马蒂厄·罗森鲍姆评为2021年度量化人物，以表彰二次粗糙赫斯顿模型。盖瑟尔的话，据巴鲁克学院报道："
        "粗糙波动率终于被接受了，人们确实在实践中使用它。<bookmark mark='a'/>两年后，Risk杂志的新星奖授予了西居尔·罗默，他对十五年标普数据的校准，"
        "是单因子粗糙模型不够用的最有力证据之一。这个领域既奖励想法，也奖励对它最尖锐的检验。",

    'Cboe launched VIX1D on April twenty-fourth 2023, using short-expiry SPX option m':
        "芝加哥期权交易所2023年4月24日推出VIX1D，使用短到期期限SPX期权中间报价，测量一天隐含期限，并非零期限微笑的局部导数。<bookmark mark='a'/>这些市场使短时段建模成为实际工作。这里比特币数据约从两天开始，不能确定零日期权行为。日内采样、价差、指数构造与有限差分分辨率都很重要。",

    'f"The lab contains simulators, Riccati solvers, lifts, roughness estimators, ret':
        "实验室包含模拟器、里卡蒂求解器、提升、粗糙度估计、收益历史滤波、运输与签名模型。<bookmark mark='a'/>各自有不同目标与数值预算。<bookmark mark='b'/>第十四条规则要求针对实际用途，与更简单模型比较验证。同日价格最低误差属于{surf}；回顾性粗糙对HAR胜者为{fc}；留出日期隐含指数跟踪为{trk}。信息集不同，不能合成采用排名。新种子是数值验证，不是未见市场数据。没有增加策略试验，本部分计数仍为{env['trials']}。下面介绍研究选读。",

    # ------------------------------------------------------------------ Frontier
    'Chapter eighteen. Selected research, 2023 to 2025.': '第18章。2023至2025年研究选读。',

    'Selected results published from 2023 through 2025. Bayer and Breneis obtain supe':
        "选读2023至2025年发表的结果。拜尔与布雷奈斯在系数满足Lipschitz条件时，证明高斯求积近似具有超多项式强收敛；这不是关于本几何提升或所有非线性波动率方程的定理。Bolko等人研究修正测量误差的粗糙度估计。<bookmark mark='a'/>2024年工作包括极小极大估计、估计量假象、Guyon约束联合校准，以及Nutz与Riveros Valdevenito的四因子解存在性。Andrès与Jourdain研究一般核条件，含2025年版本。<bookmark mark='b'/>2025年的SPX模型比较和联合签名模型进一步扩展选择。这些研究针对特定模型、数据和假设，不能证明所有粗糙模型都不可或缺或已经过时。",

    'f"Two mathematical directions. Friz and Gatheral organize forward-variance expan':
        "两个数学方向。弗里茨与盖瑟尔把远期方差展开组织为森林，首阶偏斜是应用之一。收敛与截断精度需要条件，不能把展开自动当作每个模型都可用的精确公式。<bookmark mark='a'/>正则结构提供处理奇异粗糙波动率展开的工具。股票的适应伊藤积分仍然存在；困难在于处理普通有限状态微积分之外的奇异乘积与展开。<bookmark mark='b'/>波动率依赖路径，就必须粗糙吗？<bookmark mark='c'/>不。正则性取决于核和动态。零处有界的平移核，在最短滞后可以产生布朗尺度的随机波动率；有界不等于可微。拟合的离散收益代理本身不能唯一识别连续时间的局部正则性。",

    'f"On the same-date Bitcoin marks, the lowest recorded numerical error belongs to':
        "在同日比特币标记价格上，记录的最低数值误差属于{best[1]}，为{best[2]:.2f}个波动率点。这是校准证据，没有未来日期定价或对冲验证。<bookmark mark='a'/>粗糙预测比较用全时期数据固定H；隐含指数模型则固定拟合系数，用同日收益跟踪留出日期。VIX代理的留出R平方为{100 * ps['r2_test']:.0f}%。这些问题的信息集不同。较低的有限滞后尺度指数、期权拟合与指数重构，分别提供针对自身目标的证据；任何一个都不能独自识别真实波动率规律或认证模型采用。",

    # ------------------------------------------------------------------ Outro
    'Part fourteen: finite-maturity skew magnitudes and finite-lag variance exponents':
        '第十四部分：有限期限偏斜绝对值与有限滞后方差指数是描述性证据，需要保留符号、采样与估计量影响。粗糙核渐近结论依赖模型假设。回顾性预测比较没有证明优于HAR的实时优势。粗糙贝尔戈米匹配输入的期望方差曲线，并给出同日的一次期权拟合；粗糙赫斯顿保留分数里卡蒂表示。混合格式和提升在特定近似情形下改善计算。近临界霍克斯极限需要协调缩放。收益历史代理利用同日收益跟踪留出日期的隐含指数；残差不能识别所有未观测原因。运输与签名扩展模型选择，也各有数值与鞅性问题。采用模型仍需针对目标任务验证。',

    'Four desk questions. Under an assumed H of one tenth and applicable power-law sc':
        "四个交易台问题。假设H为十分之一且幂律缩放适用，一天对一个月的偏斜比约3.9；头寸风险仍取决于敞口与希腊字母。<bookmark mark='a'/>比较粗糙度和快速均值回复时，应使用多个考虑噪声的测量，并进行真正前瞻的目标任务验证。<bookmark mark='b'/>比较替代器、提升或傅里叶方法的速度时需要匹配精度；单次求值不等于完整校准。<bookmark mark='c'/>通常条件下正则单因子模型的局部短期限偏斜有界，但仍可能拟合有限的一周观测。单指数从平坦过渡到逆期限，不能排除所有有限窗口拟合。完整解答与假设见讲义。",

    "And ten problems:":
        "还有十道习题：粗糙过程的方差、估计量背后的标度律、粗糙贝尔戈米的鞅性质、提升背后的恒等式、霍克斯过程的平均速率、粗糙偏斜背后的二重积分、"
        "混合格式的最优点，以及马尔可夫路径依赖因子。另外两道是资格考试题：精确的强误差，以及朴素格式的偏差。中英文解答都在讲义里。",

    "Where this comes back.":
        "这些内容会在哪里再出现。第15部分在粗糙和经典模型下给奇异期权定价。第16部分加速蒙特卡洛，第17部分训练让粗糙模型变快的网络。"
        "霍克斯的订单流图景会随限价订单簿和市场冲击回来，路径依赖特征会在预测中回来。",

    'The book and chapters this part covers, and the papers it draws on. The data are':
        '本部分涵盖的书和章节，以及它引用的论文。数据是基准曲面和两年的每周Deribit期权成交，币安的比特币一分钟、五分钟和日度价格，Deribit的DVOL，来自FRED的VIX和日经指数，以及肯·弗伦奇的日度市场收益。讲义记录了期权标记价格汇总、有限差分方法、日期安排与数值局限。',

    "The volatility desk now has models for every scale of volatility":
        "波动率交易台现在有了适用于每个尺度波动率的模型，以及在它们之间做选择的规则。<bookmark mark='a'/>下一部分，第15部分：奇异期权与结构化产品。"
        "障碍期权、自动赎回、棘轮期权，以及卖给储户的票据，在过去三个部分的模型下定价，以及它们之间的差距让买方付出了什么。",

    # ------------------------------------------------------------------ Research (the PhD layer)
    'For the researcher: uniform-grid rough-driver error. For the power kernel with H':
        '写给研究者：均匀网格上的粗糙驱动误差。对于H介于零与二分之一的幂核，适当的固定格内取值规则，其均方根误差为n的负H次方阶。固定数量精确格子的混合格式可以显著降低常数，但不改变该阶。这不是对所有网格、近似类型或不断增加精确格子数量的下界。下面比较精确的确定性误差积分与原始模拟。',

    'Take the Riemann--Liouville driver at time one with H strictly between zero and ':
        "取时刻一的黎曼—刘维尔驱动，H严格介于零与二分之一。<bookmark mark='a'/>幂核平方可积，但在端点无界。<bookmark mark='b'/>均匀网格阶梯近似使用固定的各滞后格内取值规则，取值点必须位于该格。<bookmark mark='c'/>伊藤等距给出图中的精确误差积分。缩放后，这些适当规则的尾部格误差可求和，而首格误差为正。<bookmark mark='d'/>因此均方根误差为n的负H次方阶。H为十分之一时，渐近误差减半需把网格数乘二的十次方。本结论不覆盖任意非均匀网格或改变近似类型的情况。",

    "The hybrid scheme attacks the constant. <bookmark mark='a'/> Simulate the first ":
        "混合格式攻击的是常数。<bookmark mark='a'/>把前kappa个格子的积分精确地模拟出来，作为与增量联合抽取的高斯变量，其余的用阶梯。<bookmark mark='b'/>用第6章的最优求值点。<bookmark mark='c'/>误差是同一个和，但它现在从奇点之后才开始。速率仍是n的负H次方。常数崩塌了，因为几乎全部误差都在第一个格子里。<bookmark mark='d'/>米克尔·本内德森、阿斯格·伦德和米科·帕卡宁在2017年给出了精确的渐近常数。这里加密网格时kappa保持固定；增加kappa或改变近似类型可能改变阶数。",

    "f'The errors, computed exactly.":
        "精确计算的误差。<bookmark mark='a'/>黎曼和：从八步到一千多步，误差从{r8:.2f}降到{r1024:.2f}，而这个变量自身的标准差是一。斜率是十分之一。"
        "<bookmark mark='b'/>只有一个精确格子的混合格式：斜率相同，低二十倍。<bookmark mark='c'/>两个精确格子，又低一些。速率由H决定；格式只选择常数。",

    "Check the formula by simulation.":
        "用模拟检验公式。从增量、精确的格子积分和网格上真实粗糙路径的精确联合高斯分布中抽样，使真实值和两个格式都来自同一条布朗路径。"
        "<bookmark mark='a'/>模拟的误差与公式在三位数字上一致，两个格式、每个网格都是如此。",

    'f"Now the original finite-grid price experiment: one-year at-the-money rough-Ber':
        "现在看原始有限网格价格实验：一年平值粗糙贝尔戈米看涨期权，所有格式使用相同股票欧拉步。<bookmark mark='a'/>白线使用网格上的精确联合高斯驱动，协方差数值求积，仍有股票时间离散与蒙特卡洛误差。<bookmark mark='b'/>八步时，朴素格式配理论补偿项比参考低{100 * (p8['exact_iv'] - p8['riemann_iv']):.0f}个波动率点。驱动方差过小，与该补偿项不匹配；驱动方差缺口为n的负二H次方阶，但不能自动证明价格偏差也有相同阶数。<bookmark mark='c'/>改用格式自身方差后，八步和六十四步的差分别为{100 * (p8['riemann_wick_iv'] - p8['exact_iv']):.1f}和{100 * (p64['riemann_wick_iv'] - p64['exact_iv']):.1f}点。四个耦合网格不能确定渐近弱收敛率。拜尔、霍尔与坦蓬内的H加二分之一定理针对带收益条件的线性粗糙Stein--Stein模型，而非本指数非线性模型。<bookmark mark='d'/>此实验中混合曲线接近网格参考；接近共用网格的参考解，不认证连续时间定价精度。",

    "Three questions for implementation. <bookmark mark='a'/> Which weak-error theore":
        "实现中的三个问题。<bookmark mark='a'/>哪个弱误差定理真正匹配系数、收益与离散格式？线性粗糙模型的结果不能直接转给粗糙贝尔戈米。<bookmark mark='b'/>拟议多层耦合在实测计算成本下能减少多少方差？H很小时朴素耦合可能低效，但一个阶数不能决定所有构造。<bookmark mark='c'/>最后，目标是否有可支持网格外推的误差展开？这里四网格普通期权实验，没有回答路径依赖产品或SPX与VIX联合模型的问题。这些是本部分尚未验证的问题，不是对当前文献的穷尽判断。",

    'Assume the asymptotic root mean squared error is C times n to minus H. What grid':
        '假设渐近均方根误差为C乘n的负H次方。把误差减半需要网格数乘多少？二的一除以H次方：H为十分之一时1024倍，H为十分之四时约五点七倍。从六十四步开始，分别约为65536步和362步。这是渐近规划计算，不是精确有限网格预测。',
}

PHRASES = {
    "rough Bergomi": "粗糙贝尔戈米",
    "two-factor Bergomi": "两因子贝尔戈米",
    "signature": "签名模型",
    "rough": "粗糙预测",
    "HAR": "HAR",
    "a tie": "平局",
    "4-factor PDV": "四因子路径依赖波动率",
    "power-law PDV": "幂律路径依赖波动率",
    "Heston": "赫斯顿",
    "rough Heston (free)": "粗糙赫斯顿（自由拟合）",
    "signature model": "签名模型",
    "the two-factor Bergomi model": "两因子贝尔戈米模型",
    "the signature model": "签名模型",
    "to better than one part in a million": "误差小于百万分之一",
    "to within a few parts in a million": "误差在百万分之几以内",
    "closely, though not exactly": "很接近，但不是精确相等",
}
