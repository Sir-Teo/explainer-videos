"""Chinese narration for quant31: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 主动管理基本定律 (fundamental law of active management),
信息系数 (information coefficient, IC), 信息比率 (information ratio, IR), 广度 (breadth), 有效广度 (effective breadth),
转移系数 (transfer coefficient), 因子风险模型 (factor risk model), 风格暴露 (style exposure), 特质风险 (specific risk),
偏差统计量 (bias statistic), 调整贝塔 (adjusted beta), 非同步交易 (non-synchronous trading), 执行落差 (implementation
shortfall), 市场冲击 (market impact), 平方根法则 (square-root law), 元订单 (metaorder), 不交易区间 (no-trade region),
容量 (capacity), 目标组合 (aim portfolio), 短视交易者 (myopic trader), 交易速率 (trade rate), 多期优化 (multi-period
optimisation), 模型预测控制 (model predictive control), 滚动时域 (receding horizon), 阿尔法合成 (alpha combination),
拥挤 (crowding), 量化地震 (quant quake), 共动量 (comomentum), 业绩归因 (P&L attribution), 择时 (timing), 选股 (selection)."""

TITLE = '量化金融，从零搭建 · 第31部分：风险模型、成本与跨期交易'

CHAPTERS = {
    'Hook': '三点九，还是一点六',
    'Law': '1. 主动管理基本定律',
    'Model': '2. 因子风险模型',
    'Betas': '3. 特质风险与贝叶斯贝塔',
    'Costs': '4. 交易成本与平方根法则',
    'AimPortfolio': '5. 追逐移动的目标：Gârleanu与Pedersen',
    'MultiPeriod': '6. 多期优化',
    'Combine': '7. 阿尔法合成',
    'Capacity': '8. 衰减、容量与Berk–Green',
    'Quake': '9. 拥挤与2007年8月',
    'Attribution': '10. 业绩归因',
    'Envelope': '11. 币市上的目标组合，登记并打开',
    'House': '12. 第31条规则：风险模型',
    'Research': '写给研究者：IC变动时的信息比率',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-one. Risk models, costs":
        "第31部分。风险模型、成本与跨期交易：一个预测在必须被持有、用风险模型衡量、并以真实价格交易之后，还值多少。",

    'f"A forecast whose rank correlation':
        "一个预测，它与下个月收益的秩相关系数是百分之五：不算高的技能。五百只股票，每月调仓。"
        "<bookmark mark='a'/>主动管理中被引用最多的公式说，信息比率应该是每年{naive:.2f}，而Grinold和Kahn认为零点五就算好，一就算杰出。"
        "<bookmark mark='b'/>现在让这百分之五每个月都波动，标准差为百分之十，就像真实的预测那样。信息比率跌到{real:.2f}。平均技能相同，回报不到一半。",

    'f"This part follows the information ratio':
        "这一部分从预测一路追到账户，清点信息比率在途中丢掉了多少。<bookmark mark='a'/>首先丢给预测自身的不稳定。"
        "<bookmark mark='b'/>然后丢给成本：币市上的一个信号，成本前夏普比率为{c['gross_sharpe']:.2f}，用十万美元交易时为{cur[100000.0]:.2f}，用一百万美元时为{cur[1000000.0]:.2f}。"
        "<bookmark mark='c'/>最后丢给风险模型本身：这一部分登记的规则，在五年封存的数据上打开后失败了，失败的方式恰好说明风险模型该怎么用。",

    "Where this sits. Part thirty chose weights":
        "这一部分在系列中的位置。第30部分用估计的均值和协方差一次性地选出权重。这一部分让问题变得真实：协方差来自因子风险模型，权重必须交易，交易要花钱，"
        "而且在你向预测靠拢的时候，预测本身也在移动。这是整个系列中最接近系统化交易台每天早上工作的一部分：预测、度量风险、为交易定价、决定走多远。"
        "这些步骤每一步都在这里用真实数据计算并检验。",

    "Oldrich Vasicek showed in 1973":
        "Oldrich Vasicek在1973年说明了如何收缩估计出的贝塔；Barr Rosenberg大约在同一时期建立了第一批商业因子风险模型；1989年，Richard Grinold写下了基本定律。"
        "<bookmark mark='a'/>接着是交易的代价：市场冲击的平方根法则，Almgren和Chriss的最优执行，转移系数，Berk和Green解释为什么经理的技能到不了投资者手里的模型，"
        "IC变动时的信息比率，以及2007年8月的量化地震。<bookmark mark='b'/>还有现代的答案：Gârleanu和Pedersen的动态交易，扛不住成本的异象，凸的多期优化，以及AQR对自身交易成本的测量。",

    "The plan: the fundamental law and its corrections":
        "本部分的安排：基本定律及其修正；因子风险模型如何构建、如何检验；特质风险与收缩后的贝塔；成本的平方根法则与容量；"
        "向移动的目标交易，从Gârleanu和Pedersen到多期优化；信号合成；衰减、拥挤与量化地震；归因；一条在封存年份上打开的登记规则；"
        "以及IC变动时信息比率的精确公式。",

    "In the House, the portfolio and risk desk":
        "在本系列公司里，组合与风险部门得到了它的风险模型、成本模型和交易规则；从组合部门指向执行部门的那条箭头，第一次标上了价格。",

    # ------------------------------------------------------------------ Law
    "Chapter one. In 1989 Richard Grinold":
        "第一章。1989年，Richard Grinold写下了主动管理中被引用最多的公式。预测的技能能换来多少信息比率？又需要多少次下注？",

    "The derivation takes four lines.":
        "推导只要四行。<bookmark mark='a'/>对残差收益的预测，等于信息系数乘以资产的残差波动率，再乘以一个标准化得分：这就是Grinold法则。"
        "<bookmark mark='b'/>残差相互独立时，最优持仓是预测除以方差。<bookmark mark='c'/>这些持仓的信息比率的平方，是每次下注的预测平方除以方差之和："
        "IC的平方乘以得分平方之和。<bookmark mark='d'/>如果有BR次独立下注，信息比率就是IC乘以广度的平方根。",

    'f"Simulate it: an IC of five percent':
        "模拟一下：IC为百分之五，资产数分别为十、一百和五百。<bookmark mark='a'/>当IC每期都相同时，模拟出的信息比率与IC乘以根号N吻合。"
        "<bookmark mark='b'/>但如果让IC本身每期变动，五百个资产时信息比率就从{r500[0]['naive']:.2f}跌到{r500[-1]['sim']:.2f}。最后一列预测了这个结果：那是研究章节将要证明的公式。",

    'f"A second correction.':
        "第二个修正。<bookmark mark='a'/>Roger Clarke、Harindra de Silva和Steven Thorley在2002年加入了一个因子：约束让组合无法充分表达它的预测。"
        "<bookmark mark='b'/>转移系数是约束所允许的持仓与预测所想要的持仓之间的相关系数。"
        "<bookmark mark='c'/>一个五百只资产、只持有正得分的纯多头组合，转移系数约为{l['tc_long_only']:.2f}：其余的技能被约束吃掉了。",

    'f"What does breadth mean?':
        "广度到底是什么意思？<bookmark mark='a'/>它数的是独立的下注。如果下注的结果相互相关，有效数目就是N除以一加上N减一乘以平均相关系数：与第26部分计算有效试验次数的公式相同。"
        "<bookmark mark='b'/>一百只股票，如果它们的下注相关系数为百分之二十，只相当于{eff:.1f}次独立下注。"
        "<bookmark mark='c'/>时间上的广度也只计入新的信息。把月度信号每天调仓，并不能得到二十倍的下注；预测没变，变的只是交易，而交易要花钱。",

    "For scale: Grinold and Kahn call":
        "作为参照：Grinold和Kahn认为年化信息比率零点五算好，零点七五算很好，一算杰出。<bookmark mark='a'/>有用的股票信号，月度IC大约在百分之二到百分之十之间。"
        "所以，IC为百分之五、五百只股票时基本定律给出的三点九，远远超出了经理们实际做到的范围。要么预测比它的IC显示的更差，要么定律漏掉了什么。"
        "两者都对，这一部分要弄清楚各占多少。",

    "And three limits that make the law an upper bound.":
        "还有三个限制，使这条定律只是一个上界。<bookmark mark='a'/>广度数的是独立下注，不是资产：同一行业的一百只股票只是少数几次下注。"
        "<bookmark mark='b'/>IC不是常数，它的波动所付出的代价，比大多数使用这条定律的人预想的要大。<bookmark mark='c'/>而且定律是成本前的：靠频繁交易买来的广度，是要付钱的。",

    "Pause and predict. An IC of point zero five, five hundred stocks":
        "暂停一下，预测一下。IC为零点零五，五百只股票，每月调仓。基本定律承诺的年化信息比率是多少？",

    # ------------------------------------------------------------------ Model
    "Chapter two. Part thirty showed":
        "第二章。第30部分说明了，许多资产的样本协方差大部分是噪声。五十年来，业界的答案一直是因子风险模型。",

    'f"The idea in one line.':
        "一句话概括这个想法。<bookmark mark='a'/>每个收益都是对少数几个共同因子的暴露乘以因子收益，再加上资产自身的残差；残差在资产之间互不相关。"
        "所以协方差等于因子部分X F X转置，加上一个对角矩阵。<bookmark mark='b'/>三千只股票的完整协方差矩阵里有{full:,}个数。"
        "<bookmark mark='c'/>用六十个因子，因子模型只有{fac:,}个：因子协方差，加上每只股票一个特质方差。暴露根本不需要估计；它们是从股票自身的特征中测量出来的。",

    "The machine, in five parts.":
        "这台机器分五个部分。<bookmark mark='a'/>暴露：每个资产的特征，每天在整个股票池中标准化。"
        "<bookmark mark='b'/>因子收益：每天做一次横截面回归，把第二天的收益对今天的暴露回归；系数就是当天的因子收益。"
        "<bookmark mark='c'/>这些因子收益的协方差，对近期赋予更大权重。<bookmark mark='d'/>每个资产的残差方差，向同类收缩。"
        "<bookmark mark='e'/>对任意组合，给出一个可分解为因子部分和特质部分的风险预测。",

    "The House builds one, on the coins of Part twenty-nine.":
        "本系列公司用第29部分的币种建了一个。<bookmark mark='a'/>五个风格暴露，每个都在收盘时已知：规模，用成交额度量；对市场的贝塔；近期波动率；"
        "跳过最近一周的动量；以及用于反转的最近五天收益。另外还有一个市场因子，每个币种对它的暴露都是一。"
        "<bookmark mark='b'/>每个特征当天在所有币种之间标准化，并在三个标准差处截断，这样单个狂野的币种就无法主导回归。",

    "An equity model has more.":
        "股票模型的内容更多。<bookmark mark='a'/>几十个行业暴露，每只股票对应自己的行业；在全球模型中还有国家和货币。币市没有像样的行业，所以本系列公司的模型没有行业因子。"
        "<bookmark mark='b'/>行业带来一个技术问题：每只股票恰好属于一个行业，所以行业列加起来就等于市场列，回归无法把它们分开。"
        "<bookmark mark='c'/>商业模型加了一个约束：按市值加权的行业收益之和为零，这样市场因子就是市场，每个行业都相对于市场来度量。",

    'f"Factor returns come from one regression a day.':
        "因子收益来自每天一次的回归。<bookmark mark='a'/>每个币种明天的收益，等于它今天的暴露乘以因子收益，再加上残差。"
        "<bookmark mark='b'/>用跨币种的加权最小二乘来估计因子收益，权重随规模增大，因为大资产的残差噪声更小。"
        "<bookmark mark='c'/>每个系数都是一个组合的收益，这个组合对某个因子的暴露为一，对其他因子为零：这是Fama和MacBeth的洞见，见第23部分。"
        "<bookmark mark='d'/>平均每天，六个因子解释了币种收益离散度的{100 * m['r2_mean']:.0f}%。",

    'f"Here are the five style factor returns':
        "这是五个风格因子在研究年份内的累计收益。<bookmark mark='a'/>波动率因子每年亏损{abs(100 * v['mean']):.0f}%，t统计量为{v['t']:.1f}："
        "平静的币种跑赢狂野的币种，这是第24部分的低波动异象，出现在一个新的市场里。反转每年赚{100 * r['mean']:.0f}%，t为{r['t']:.1f}。"
        "<bookmark mark='b'/>但风险模型并不关心一个因子是否赚钱。它关心的是这个因子让许多资产一起波动，因此必须预测它的方差。",

    'f"How much of a coin\'s risk is common?':
        "一个币种的风险有多少是共同的？<bookmark mark='a'/>对中位数币种而言，预测方差的{100 * s:.0f}%是因子风险，主要来自市场。币种之间的联动远比股票强；"
        "对大盘股来说，特质部分的占比通常更大。<bookmark mark='b'/>这种拆分正是因子模型有用的原因：共同部分由少数几条历史很长的序列来预测，只有特质部分才留给每个资产自己那段又短又嘈杂的历史。",

    'f"Is the model right? Barra\'s test is simple.':
        "模型对吗？Barra的检验很简单。<bookmark mark='a'/>每天，用组合的实现收益除以模型前一天预测的波动率。"
        "<bookmark mark='b'/>如果预测正确，这些数的标准差应该是一：这就是偏差统计量。<bookmark mark='c'/>在六百五十天里，与一相差约百分之十一以内的都算通过。"
        "<bookmark mark='d'/>四个组合。等权币种：{ew:.2f}，轻微低估。随机多空组合和单个币种都通过了。而波动率因子本身得到{vf:.2f}：模型高估了它的风险。"
        "一个可能的原因是，这个因子在币市中自身的波动率变化得太快，六十天的半衰期跟不上。",

    "There are three kinds of factor model.":
        "因子模型有三类。<bookmark mark='a'/>基本面模型，就像我们刚刚建的这个，测量暴露、估计因子收益。"
        "<bookmark mark='b'/>统计模型仅从收益本身同时估计两者，用主成分，就像Connor和Korajczyk在1986年所做的：没有经济含义的标签，但适应得快。"
        "<bookmark mark='c'/>宏观经济模型观测因子收益，比如通胀和利率的意外变化，然后估计每个资产的暴露，就像Chen、Roll和Ross所做的。"
        "Gregory Connor在1995年的比较发现，基本面模型的解释力最强。",

    "The firm file. Barr Rosenberg founded Barra":
        "公司档案。Barr Rosenberg于1975年在伯克利创立了Barra，正是为了出售这样一台机器，它建立在他关于所谓“市场外协方差”的学术论文之上；MSCI在2004年收购了它。"
        "它的模型，以及其竞争对手的模型，成了经理、客户和监管者谈论风险的共同语言。这有一个代价，我们将在第九章看到：当每个人都用同样的方式度量风险，每个人都会看到同样的机会。",

    "Pause and predict. A portfolio's bias statistic is one point three":
        "暂停一下，预测一下。一个组合在两年日度数据上的偏差统计量是一点三。模型是高估还是低估了它的风险？差多少？",

    # ------------------------------------------------------------------ Betas
    "Chapter three. The factor model leaves":
        "第三章。因子模型留下两类需要逐个资产估计的数：特质方差，以及在最简单的模型里，一个贝塔。两者都有噪声，也都可以用同一个技巧改进。",

    "Specific risk first.":
        "先看特质风险。<bookmark mark='a'/>每个资产的残差方差，是它自身残差平方的指数加权平均。"
        "<bookmark mark='b'/>然后把它朝当天同类资产的平均值拉近一部分。商业模型朝规模相近的资产收缩，因为小资产的特质风险更大。"
        "<bookmark mark='c'/>本系列公司拉近百分之三十；对于两个月前才上市的资产，模型会拉得更多，因为它自身的历史说明不了什么。",

    "Betas. Marshall Blume noticed in 1971":
        "再看贝塔。Marshall Blume在1971年注意到，在一个时期估计出的贝塔，在下一个时期会向一回归。"
        "<bookmark mark='a'/>现在贝塔高的组合，之后很可能会低一些，贝塔低的则会高一些；把后期贝塔对前期贝塔回归，斜率约为三分之二。"
        "<bookmark mark='b'/>估计值的三分之二加上一的三分之一，就成了金融终端上显示的调整贝塔。Blume认为这部分是真实的漂移，部分是噪声估计的统计效应。",

    'f"Oldrich Vasicek made the statistical part exact':
        "Oldrich Vasicek在1973年把统计部分做得精确。<bookmark mark='a'/>每个估计出的贝塔，等于真实贝塔加上噪声，噪声的方差可以从回归中得知；而真实贝塔本身围绕一个均值分布。"
        "<bookmark mark='b'/>对真实贝塔的最佳猜测，是估计值与均值的加权平均，按各自的精度加权：估计越嘈杂，被拉回得越多。"
        "<bookmark mark='c'/>真实贝塔的离散程度从数据中估计：估计值的方差，减去平均噪声。这是经验贝叶斯，就像第30部分的Bayes–Stein均值。"
        "<bookmark mark='d'/>在币市上，用六十天的数据，币种自身估计值的平均权重为{v['weight']:.2f}。",

    "One quarter of the coins.":
        "一个季度的币种。<bookmark mark='a'/>横轴是每个币种用六十天估计的贝塔；纵轴是它在接下来六十天里的贝塔。完美的预测落在虚线上。"
        "点云比虚线更平：高的估计偏高，低的估计偏低。<bookmark mark='b'/>收缩把每个点水平地推向均值，点云于是更贴近对角线。",

    'f"Scored over all':
        "在全部{v['n_windows']}对季度上打分。<bookmark mark='a'/>原始估计对下一季度贝塔的均方误差是{mse['raw']:.3f}。把每个贝塔都设为一，稍差一点。"
        "Vasicek的收缩最好，把误差降低了{100 * gain:.0f}%。最好的估计既不是只用数据，也不是只用先验。",

    "Why it works.":
        "为什么有效？<bookmark mark='a'/>最大的估计值最有可能得到了运气的帮助；按估计值来挑选，就是按它的噪声来挑选。"
        "<bookmark mark='b'/>两部分里这已经是第四次出现同一个想法：Stein的均值，Ledoit和Wolf的协方差，Vasicek的贝塔，以及特质方差。接受一点偏差，换来大得多的方差下降。"
        "<bookmark mark='c'/>当先验错了，它就会失效：把一种新类型的资产，向一个它并不属于的群体的均值收缩。",

    "One more source of error in betas: time.":
        "贝塔还有一个误差来源：时间。<bookmark mark='a'/>交易稀少的资产对市场的反应会晚一天，所以用同日收益估计的贝塔偏低。小盘股和交易清淡的币种是最坏的情形。"
        "<bookmark mark='b'/>Myron Scholes和Joseph Williams，以及之后的Elroy Dimson，通过加上对前一天和后一天市场收益的斜率来修正它。"
        "<bookmark mark='c'/>或者用周收益来估计，让延迟的反应落在同一周内，代价是观测更少，而这恰恰是收缩最重要的时候。",

    "Pause and predict. A beta is estimated at one point eight":
        "暂停一下，预测一下。一个贝塔的估计值为一点八，标准误为零点三。在所有股票中，真实贝塔的均值为一，标准差为零点三。Vasicek的估计是多少？",

    # ------------------------------------------------------------------ Costs
    "Chapter four. The fundamental law is gross of costs.":
        "第四章。基本定律是成本前的。它计入的每一次下注都必须下单，而下单会让价格朝不利于你的方向移动。",

    "Andre Perold gave the right accounting in 1988":
        "Andre Perold在1988年给出了正确的记账方法：执行落差，即纸面组合的收益减去真实组合的收益，从做出决策时的价格开始计算。"
        "<bookmark mark='a'/>它有四个部分。费用，事先已知。买卖价差的一半，由想要立刻成交的一方支付。"
        "<bookmark mark='b'/>市场冲击：价格在你交易的时候、并且因为你的交易而移动。还有未完成交易的机会成本。对大型基金而言，冲击是账单的大头。",

    "The most robust regularity in market microstructure.":
        "市场微观结构中最稳健的规律。<bookmark mark='a'/>一笔大订单拆成一天内的许多小笔交易，它的价格冲击正比于日波动率乘以订单规模占日成交量比例的平方根。"
        "它在九十年代由Barra记录下来，2005年由Almgren及其合作者在股票上测量，2011年由Tóth及其合作者在期货上发现，之后又在期权和比特币上得到验证。"
        "第37部分解释为什么是平方根。<bookmark mark='b'/>以金额计，成本是规模乘以冲击，所以它按规模的一点五次方增长。"
        "<bookmark mark='c'/>基金规模翻倍，成本几乎变成三倍。这就是每个策略都有容量的原因。",

    'f"In the coins of Part twenty-nine.':
        "在第29部分的币种中。<bookmark mark='a'/>中位数合格币种每天成交约{adv / 1000000.0:.1f}百万美元，日波动率为{100 * sig:.1f}%。"
        "<bookmark mark='b'/>一笔一百万美元的订单相当于一天成交量的{100 * frac:.0f}%。<bookmark mark='c'/>平方根法则给它的定价约为{100 * c['cost_1m']:.1f}%，每次都要付。"
        "一个每天优势只有零点几个百分点的信号，付不起这个代价。",

    "How large are costs in practice?":
        "实际成本有多大？学术研究长期只能从公开成交数据中猜测哪些成交属于同一笔订单。2018年，当时在AQR的Andrea Frazzini、Ronen Israel和Tobias Moskowitz，"
        "公布了一家大型管理人自身的执行成本，据报道就是他们所在的公司：二十一个市场、十九年间、一点七万亿美元的交易。"
        "他们发现成本比早期学术估计小约一个数量级，以市场冲击为主，且随规模增长得比正比更慢，正如平方根法则所说。耐心而审慎的执行，会改变一个异象能否存活的答案。",

    "Robert Novy-Marx and Mihail Velikov":
        "Robert Novy-Marx和Mihail Velikov问：哪些异象能扛住成本？<bookmark mark='a'/>交易少的，比如价值、规模和盈利能力，能存活；高换手的，比如短期反转，大多不能。"
        "<bookmark mark='b'/>有帮助的是少交易：在目标周围设一个区间，区间内不交易；并且把成本放进优化之中，而不是事后扣除。"
        "<bookmark mark='c'/>纸面上的异象是成本前的；可投资的异象是扣除之后剩下的。",

    'f"A capacity curve.':
        "一条容量曲线。信号是第二章的低波动效应：做多平静的币种，做空狂野的币种，每天调仓，每天换手组合的{100 * c['turnover']:.0f}%。"
        "<bookmark mark='a'/>成本前，夏普比率为{c['gross_sharpe']:.2f}。<bookmark mark='b'/>用十万美元，{s5:.2f}。用一百万美元，{s6:.2f}。"
        "再往上，成本是优势的许多倍，曲线按规模的平方根下降。策略的容量就是这条曲线与你所需收益相交的地方，而对于薄市场中的日度信号，它很小。",

    "So costs belong inside the optimisation.":
        "所以成本应该放在优化之内。<bookmark mark='a'/>最大化预期收益，减去风险，减去从今天的持仓移动过去的成本，成本采用平方根法则的一点五次方。它仍然是凸问题。"
        "<bookmark mark='b'/>它的解让大多数仓位保持不动：在今天的持仓周围，有一个区域里任何交易都不值它的成本。"
        "<bookmark mark='c'/>而按风险缩放的二次成本，是让动态问题有闭式解的替代品，那是下一章的内容。",

    "A classical result about the no-trade region.":
        "关于不交易区间的一个经典结果。<bookmark mark='a'/>如果成本与交易金额成正比，最优策略就是在无摩擦目标周围设一个区间：区间内什么也不做，仓位漂出区间时只交易到区间边缘。"
        "<bookmark mark='b'/>成本很小时，区间的半宽按成本的立方根增长。George Constantinides在1986年描述了这个区间，Mark Davis和Andrew Norman精确刻画了它，"
        "Steven Shreve和Mete Soner推导出立方根法则。<bookmark mark='c'/>摩擦造成的效用损失按三分之二次方增长。"
        "<bookmark mark='d'/>所以即使成本很小，区间也很宽：成本降到八分之一，区间只缩小一半。小成本对行为影响很大，对福利影响很小。",

    "Pause and predict. A strategy nets six percent":
        "暂停一下，预测一下。一个策略在一亿美元规模时扣除百分之二的成本后，净赚百分之六。按平方根法则，在四亿美元时它净赚多少？",

    # ------------------------------------------------------------------ AimPortfolio
    "Chapter five. Nicolae Garleanu and Lasse Pedersen":
        "第五章。Nicolae Gârleanu和Lasse Pedersen在2013年解决了每个系统化交易者每天早上面对的问题：预测已经变了，交易要花钱，而明天它们还会再变。",

    "The problem. <bookmark mark='a'/> Expected returns come from a few signals":
        "问题是这样的。<bookmark mark='a'/>预期收益来自少数几个信号，每个信号以自己的速度衰减：动量信号以月计，反转信号以天计。"
        "<bookmark mark='b'/>选择一整条持仓路径，最大化预期收益的折现和，减去风险惩罚，再减去每笔交易的二次成本，成本按风险缩放，作为冲击的替代。"
        "<bookmark mark='c'/>Phi是每个信号每期衰减掉的比例。",

    "The solution uses Part eight's machinery.":
        "求解用的是第8部分的工具。<bookmark mark='a'/>线性动态加上二次目标，让价值函数是二次的，贝尔曼方程变成Riccati方程。"
        "<bookmark mark='b'/>最优策略：每一期，从昨天的持仓朝一个目标组合交易固定比例的距离。<bookmark mark='c'/>这个比例是a除以lambda，a是一个二次方程的根。"
        "<bookmark mark='d'/>成本很大时，它约等于风险厌恶除以成本的平方根：成本变成四倍，速度减半。",

    "And the aim portfolio is the insight.":
        "目标组合才是真正的洞见。<bookmark mark='a'/>它是今天的Markowitz组合与未来预期的Markowitz组合的加权平均。"
        "<bookmark mark='b'/>对于按几何速度衰减的信号，这个平均就是今天的Markowitz组合，只是每个信号都打了折扣。"
        "<bookmark mark='c'/>慢信号几乎保留全部权重。快信号被削减，因为在你交易完之前它就已经衰减了。瞄准目标的前方，每次只走一部分。",

    "Here is what it looks like, for one asset":
        "对于一个由一慢一快两个信号驱动的资产，它看起来是这样的。<bookmark mark='a'/>Markowitz目标随快信号跳来跳去；短视交易者去追它，每一跳都要付钱。"
        "<bookmark mark='b'/>目标组合给快信号打了折扣，所以动得更少。<bookmark mark='c'/>而最优持仓每天只朝目标走一部分：一条平滑的路径，跟随慢信号，忽略快信号的大部分噪声。",

    "Is the formula right? The House checks it the slow way.":
        "公式对吗？本系列公司用笨办法来检查。<bookmark mark='a'/>在二次价值函数上迭代贝尔曼方程，直到它不再变化，然后读出交易速率和目标权重。"
        "<bookmark mark='b'/>它们与闭式解在显示的每一位上都一致，无论交易便宜还是昂贵，信号快还是慢。",

    "With many assets, one modelling choice does the work.":
        "资产很多时，一个建模选择起了关键作用。<bookmark mark='a'/>Gârleanu和Pedersen让交易成本与其风险成正比，好像做市商为他们接手的库存风险收费。"
        "<bookmark mark='b'/>这样交易速率对整个组合就是一个数。<bookmark mark='c'/>如果成本矩阵是一般的，速率就变成一个矩阵，来自矩阵Riccati方程：在流动性好的资产上交易得快，在流动性差的资产上交易得慢。"
        "闭式解还在，简洁性没了。",

    'f"Now on the coins, with two signals from this part.':
        "现在用这一部分的两个信号在币市上做。<bookmark mark='a'/>一个慢信号：平静的币种，即近期波动率低的币种。它的得分每天衰减{100 * ph['slow']:.1f}%，半衰期约{hl['slow']:.0f}天。"
        "<bookmark mark='b'/>一个快信号：三天反转，每天衰减{100 * ph['fast']:.0f}%，半衰期一天半。"
        "<bookmark mark='c'/>每个信号的预期收益来自Grinold法则，IC在2018和2019年上拟合，风险模型是每个币种自身的近期方差。",

    'f"The result, net of costs, as trading gets more expensive.':
        "随着交易变贵，扣除成本后的结果。<bookmark mark='a'/>交易免费时，两个交易者完全一样：{rows[0]['gp']:.2f}。"
        "<bookmark mark='b'/>成本上升后，每天追逐Markowitz目标的短视交易者，在lambda为八时跌到{r8['myopic']:.2f}，为三十二时跌到{r32['myopic']:.2f}。"
        "Gârleanu和Pedersen的交易者保持在{r8['gp']:.2f}和{r32['gp']:.2f}，办法是每天先走{100 * r8['rate']:.0f}%、再走{100 * r32['rate']:.0f}%的距离，并把快信号的权重削减到{r32['w_fast']:.2f}。",

    "Three lessons. <bookmark mark='a'/> Trade partially":
        "三条教训。<bookmark mark='a'/>部分交易，永远不要一路走到今天的目标。<bookmark mark='b'/>瞄准它的前方：偏爱持久的信号，因为等你交易完成时它们的预测仍然成立。"
        "<bookmark mark='c'/>记住哪些是近似：真实的冲击不是二次的，风险模型也是估计出来的。下一章去掉第一个近似。",

    "Pause and predict. Trading costs quadruple.":
        "暂停一下，预测一下。交易成本变成四倍。最优交易速率大致如何变化？快信号在目标组合中的权重又会怎样？",

    # ------------------------------------------------------------------ MultiPeriod
    "Chapter six. Garleanu and Pedersen's closed form":
        "第六章。Gârleanu和Pedersen的闭式解需要二次成本且没有约束。真实的组合两者都不满足。现代的答案放弃闭式解，保留其思想。",

    "In 2017 Stephen Boyd and coauthors":
        "2017年，Stephen Boyd及其合作者给出了一般形式。<bookmark mark='a'/>规划未来H期的持仓路径，每期都用一个预测：最大化预期收益，减去任意凸的风险度量，"
        "再减去任意凸的交易成本，比如价差和冲击的一点五次方。<bookmark mark='b'/>在每个规划期上加入任意凸约束。"
        "<bookmark mark='c'/>然后只执行第一笔交易；明天有了新的预测，再重新规划。这是凸问题，标准求解器对数千个资产也能很快求解。",

    "The receding horizon.":
        "滚动时域。<bookmark mark='a'/>每天，优化器向前规划若干期，只执行第一步，然后窗口向前滑动。工程师称之为模型预测控制；它操控着化工厂和自动驾驶汽车。"
        "<bookmark mark='b'/>它不需要预测是对的；它需要的是今天能得到的最好预测，等明天的预测来了再用明天的。",

    "What the plan needs is a forecast for every period ahead.":
        "规划需要对未来每一期都有预测。<bookmark mark='a'/>对收益，需要一条期限结构：每个信号的预测按测得的速度衰减，就像第五章那样。"
        "<bookmark mark='b'/>对风险，通常就用今天的估计并保持不变，因为风险远比阿尔法持久；或者用第7部分的GARCH预测。"
        "<bookmark mark='c'/>对成本：成交量和价差随时段和日历变化，所以规划会把交易移到交易便宜的时段。",

    "What goes into the constraints.":
        "约束里放些什么。<bookmark mark='a'/>仓位上限。流动性上限，使任何仓位都不超过该资产几天的成交量。对风险模型各因子的中性。换手预算。"
        "<bookmark mark='b'/>还有每个资产预测风险的下限，这一部分登记的规则恰恰没有它，第十一章会说明后果。",

    'f"A small experiment.':
        "一个小实验。一个资产，一个每天衰减百分之十五的预测，冲击为一点五次方。<bookmark mark='a'/>如果交易免费，你会直接跳到Markowitz仓位，然后跟着它下降。"
        "<bookmark mark='b'/>单期优化器必须用一天的收益支付全部建仓成本，所以只买{p1[0]:.2f}。"
        "<bookmark mark='c'/>五期规划买{p5[0]:.2f}并且继续加仓，因为它看不到视野之外卖出的成本。"
        "<bookmark mark='d'/>长视野买{p40[0]:.2f}，稍微加一点，然后随着预测衰减规划一个有序的退出：动态的答案，不需要闭式解就找到了。",

    "Three lessons. <bookmark mark='a'/> A single-period optimizer":
        "三条教训。<bookmark mark='a'/>带成本的单期优化器对持久信号交易不足，因为它把一个仓位的全部成本都算到一期头上。"
        "<bookmark mark='b'/>短视野会过度交易，因为它从不为退出付费。"
        "<bookmark mark='c'/>而在二次成本、无约束、长视野的情形下，规划的第一步正是Gârleanu和Pedersen的交易：闭式解只是特例。",

    "Pause and predict. A forecast is expected to last only one day.":
        "暂停一下，预测一下。一个预测预计只持续一天。更长的规划视野会显著改变今天的交易吗？",

    # ------------------------------------------------------------------ Combine
    "Chapter seven. A desk never has one signal":
        "第七章。交易台从来不会只有一个信号；第29部分挖出了成千上万个。在优化器看到它们之前，它们必须变成每个资产的一个预测。",

    "The theory is Part thirty again.":
        "理论又回到了第30部分。<bookmark mark='a'/>预测是标准化得分的加权和。"
        "<bookmark mark='b'/>如果把各信号的IC放进一个向量，它们得分的相关矩阵为C，那么最佳组合的IC平方就是ic转置乘C的逆乘ic。"
        "<bookmark mark='c'/>最佳权重是C的逆乘以IC：把收益对得分回归，代数上与切点组合相同。"
        "<bookmark mark='d'/>互不相关的信号像独立下注一样相加。所以最佳权重继承了切点组合的所有问题：估计的IC，估计的相关，以及一个把它们的误差最大化的优化器。",

    'f"Six signals on the coins':
        "币市上的六个信号：第二章的五个风格暴露，以及第29部分挖出的阿尔法。<bookmark mark='a'/>蓝色是每个信号在2018和2019年的平均日度IC；青色是2020年的。"
        "<bookmark mark='b'/>挖出的阿尔法在两段时间里都是最强的，先是{tr['mined']:.3f}，然后是{va['mined']:.3f}。其次是低波动，符号为负。"
        "动量在两段时间之间改变了符号，反转的IC则增大了好几倍。",

    "Three combinations, from the most humble":
        "三种合成方式，从最谦逊到最雄心勃勃。<bookmark mark='a'/>等权，每个信号的符号来自训练期。<bookmark mark='b'/>按训练期IC成比例的权重，忽略信号之间的相关。"
        "<bookmark mark='c'/>以及回归本身，汇集训练期的每个币种和每一天，加上从零到很大的岭惩罚。",

    'f"The scores.':
        "得分如下。<bookmark mark='a'/>在训练年份，回归获胜，这是必然的：{r0['train']:.3f}。"
        "<bookmark mark='b'/>到了2020年，顺序反转。回归跌到{r0['valid']:.3f}。IC加权保持在{cb['IC-weighted']['valid']:.3f}，等权为{cb['equal']['valid']:.3f}。"
        "<bookmark mark='c'/>而挖出的阿尔法单独使用，{c['ic_valid']['mined']:.3f}，胜过所有合成。",

    "How to read it. <bookmark mark='a'/> The regression fitted":
        "怎么解读。<bookmark mark='a'/>回归拟合了训练期的IC和相关，然后信号变了：估计的权重带着估计的误差，与第30部分完全一样。"
        "<bookmark mark='b'/>当信号强度相近且相关较弱时，合成的帮助最大；这里一个信号承载了大部分信息。"
        "<bookmark mark='c'/>交易台会把合成向简单权重收缩，缓慢地重新拟合，并用实际交易的组合来评判它。",

    "One more ingredient: horizon.":
        "还有一个要素：期限。<bookmark mark='a'/>在交易缓慢的组合中，快信号的预测在交易完成前就已衰减，所以第五章的折扣应该放进合成之中。"
        "<bookmark mark='b'/>等价地，在你打算持有的期限上测量每个信号的IC：快信号的IC在一两天后达到峰值，慢信号的IC则会持续上升好几周。",

    "And where to combine.":
        "还有在哪里合成。<bookmark mark='a'/>合成预测，只做一次优化：来自不同信号的相反交易在进入市场前就相互抵消，风险模型也能看到整个组合。"
        "<bookmark mark='b'/>或者合成组合：每个信号单独一个组合，再加起来。运行和归因都更简单，但一个组合买入另一个组合卖出的东西，两边都要付价差。"
        "<bookmark mark='c'/>有成本时，分别最优的组合之和并不是最优组合。大公司通过内部撮合交易，挽回一部分差距。",

    "Pause and predict. Two signals each have an IC":
        "暂停一下，预测一下。两个信号的IC都是零点零四，它们的得分相关系数为零点五。最佳合成的IC是多少？",

    # ------------------------------------------------------------------ Capacity
    "Chapter eight. A signal's speed sets its turnover":
        "第八章。信号的速度决定换手，换手决定成本，成本决定它能管理多少钱。然后的问题是：利润归谁。",

    'f"Decay and turnover first.':
        "先看衰减和换手。<bookmark mark='a'/>按得分成比例持仓，得分的日间相关为一减phi。<bookmark mark='b'/>得分每天的变化方差为二phi。"
        "<bookmark mark='c'/>所以换手随衰减率的平方根增长。<bookmark mark='d'/>对第五章的两个信号，分别是{ts:.2f}和{tf:.2f}：每一美元上，反转组合的交易量约为平静组合的四倍，"
        "而按平方根法则，它付出的成本超过四倍。",

    "How large should a strategy be?":
        "一个策略应该做多大？<bookmark mark='a'/>每美元毛收益为g，规模为A，冲击服从平方根法则：每美元成本随规模的平方根增长，所以金额成本按A的一点五次方增长。"
        "<bookmark mark='b'/>净收益在盈亏平衡规模处降到零，即g除以c的平方。<bookmark mark='c'/>金额利润更早达到峰值：在盈亏平衡规模的九分之四处。"
        "<bookmark mark='d'/>在那里，每美元收益是毛收益的三分之一。容量不是策略失效的规模；它是一个选择：把多少优势让给市场。",

    "The picture. <bookmark mark='a'/> The net return per dollar falls from g":
        "图像如下。<bookmark mark='a'/>每美元净收益从g开始，按规模的平方根下降，在盈亏平衡处降到零。"
        "<bookmark mark='b'/>金额利润先上升，在九分之四处达到峰值，然后回落。按资产规模收费的经理希望待在峰值右侧；投资者希望在左侧。两者之间的张力就是下一个模型。",

    "Jonathan Berk and Richard Green wrote the model in 2004.":
        "Jonathan Berk和Richard Green在2004年写出了这个模型。<bookmark mark='a'/>经理有技能a；成本随基金规模上升；费率为f。投资者得到a减成本减费用。"
        "<bookmark mark='b'/>理性的投资者只要这个值为正就会继续投钱。<bookmark mark='c'/>所以在均衡中，他们得不到超过基准的收益，经理以更大基金上的费用形式拿走技能的全部价值。"
        "<bookmark mark='d'/>过去的收益推动资金流动，而不是未来的阿尔法。基金收益著名的缺乏持续性，正是一个有技能、有容量的世界所预测的。",

    "Put the square-root law into Berk and Green.":
        "把平方根法则放进Berk和Green的模型。<bookmark mark='a'/>投资者一直投钱，直到他们的阿尔法为零，这对任何费率都确定了基金的规模。"
        "<bookmark mark='b'/>以收入最大化来定费率的经理，收取技能的三分之一。<bookmark mark='c'/>基金随后恰好运行在盈亏平衡规模的九分之四，也就是之前的利润最大化规模。"
        "拥有策略的经理和出售策略的经理到达同一个规模；区别只在于谁拿走那三分之一。",

    "The evidence. <bookmark mark='a'/> Jonathan Berk and Jules van Binsbergen":
        "证据。<bookmark mark='a'/>Jonathan Berk和Jules van Binsbergen用美元增加值来度量技能，即阿尔法乘以规模，发现平均经理确实创造了价值，而且排名具有持续性，"
        "同时投资者的阿尔法接近零，正如模型所预测。<bookmark mark='b'/>这也解释了为什么一些最成功的基金对外部资金关闭：策略的拥有者想要利润最大化的规模，而不是最大的规模。"
        "<bookmark mark='c'/>本系列公司的规则：每个策略在获得资金之前，都要根据测得的换手和平方根法则报告它的容量。",

    "Pause and predict. A strategy breaks even at nine hundred million":
        "暂停一下，预测一下。一个策略在九亿美元时盈亏平衡。它在什么规模赚钱最多？在那里投资者保留毛收益的多少？",

    # ------------------------------------------------------------------ Quake
    "Chapter nine. A risk model that everyone uses":
        "第九章。一个人人都用的风险模型，会把每个人引向同样的交易。2007年8月的第二周，这笔账到期了。",

    "The crisis file. In the week of the sixth of August 2007":
        "危机档案。2007年8月6日那一周，许多量化多空股票基金在三天里损失惨重，而股市本身几乎没动。13日，高盛表示将与外部投资者一起向其全球股票机会基金注资三十亿美元，"
        "这是一只量化多空基金，据报道此前已亏损约百分之三十。它给出的解释提到了重叠的交易、上升的波动率和上升的相关性。",

    "Amir Khandani and Andrew Lo studied it":
        "Amir Khandani和Andrew Lo用最简单的市场中性组合研究了它。<bookmark mark='a'/>每天，买入昨天的输家，卖出昨天的赢家，按每只股票偏离市场的程度成比例。"
        "<bookmark mark='b'/>这个组合是美元中性的。<bookmark mark='c'/>它在价格反转时赚钱：它的报酬来自为昨天交易的人提供流动性。",

    'f"The House replays the rule':
        "本系列公司在美国四十九个行业组合上，按天回放了2007年7月和8月的这条规则。<bookmark mark='a'/>在6日那一周：8日，{100 * a8:.2f}%；9日，{100 * a9:.2f}%；"
        "而前一年典型的日波动为{100 * sd:.2f}%。<bookmark mark='b'/>10日，{100 * a10:+.2f}%，大部分收了回来。"
        "Khandani和Lo在个股上看到了同样的形状，幅度大得多：7日、8日、9日亏损，10日急剧反弹。",

    "Khandani and Lo's explanation, offered as a hypothesis.":
        "Khandani和Lo的解释，作为一个假说提出。<bookmark mark='a'/>一家持有类似组合的大型基金必须筹集现金，可能是因为信贷市场崩溃时在别处遭受了损失。"
        "<bookmark mark='b'/>它迅速卖出多头、买回空头，让所有持有同样仓位的人都承受不利的价格变动。"
        "<bookmark mark='c'/>其他人跟着亏损，触及风险限额，也开始平仓。<bookmark mark='d'/>抛售停止后，价格迅速反弹。",

    "Seen through the risk model of Chapter two.":
        "透过第二章的风险模型来看。<bookmark mark='a'/>这些组合对模型中的每个因子都是中性的。"
        "<bookmark mark='b'/>所以模型只看到分散在数百个名字上的特质风险，预测出一个小而分散的方差。"
        "<bookmark mark='c'/>但拥挤仓位的残差并不独立：各基金共同持有它们。缺失的因子就是人群本身，没有任何供应商的模型包含它。",

    "Can crowding be measured before it bites?":
        "能否在拥挤造成伤害之前度量它？<bookmark mark='a'/>Dong Lou和Christopher Polk为动量提出了一个指标，称为共动量：策略所持股票残差收益之间的超额相关。"
        "它高的时候，说明许多套利者已经入场，策略之后的收益更差。<bookmark mark='b'/>其他人关注空头腿的卖空量、策略在成交量中的占比，以及一只基金与同行的相关性。"
        "<bookmark mark='c'/>业界把这个教训保留为强制平仓的压力测试，以及按流动性加权的仓位限额。",

    'f"Two lessons.':
        "两条教训。<bookmark mark='a'/>风险模型只度量它包含的风险：对模型中性，并不是对一切中性。"
        "<bookmark mark='b'/>提供流动性等于做空崩盘：它靠吸收别人的交易赚钱，在所有人同时交易时亏钱。一个诚实的脚注：在行业组合上，这条逆向规则在之前十年里根本没有赚钱，"
        "夏普比率为{q['sharpe_1997_2007']:.2f}，因为行业是趋势性的而不是反转的。反转溢价存在于个股之中。",

    "Pause and predict. Your book's forecast volatility":
        "暂停一下，预测一下。你的组合预测波动率为每年百分之四，对模型中的每个因子都是中性的。说出它在一周内亏损百分之十的一种方式。",

    # ------------------------------------------------------------------ Attribution
    "Chapter ten. Every morning a risk desk":
        "第十章。每天早上，风险部门都要回答关于昨天的一个问题：钱从哪里来？因子模型可以精确地回答它。",

    "Multiply the factor model by the holdings.":
        "把因子模型乘以持仓。<bookmark mark='a'/>组合的收益是对各因子求和：暴露乘以因子收益，再加上特质部分。这个恒等式每天都精确成立。"
        "<bookmark mark='b'/>每个因子的贡献是暴露乘以收益。<bookmark mark='c'/>特质部分是在扣除所有因子之后选股带来的收益：因子ETF无法复制的那部分。",

    "Traditional managers know an older version.":
        "传统经理熟悉一个更老的版本。<bookmark mark='a'/>Gary Brinson及其合作者把基金相对基准的收益分成配置，即超配表现好的行业所得，"
        "<bookmark mark='b'/>以及选择，即在每个行业内挑出更好的股票所得。因子模型把两者都推广了：行业变成任意因子，选择变成特质收益。",

    'f"Now apply it to the best signal of Part twenty-nine':
        "现在把它用在第29部分最好的信号上，就是在第七章胜过所有合成的那个挖出的阿尔法。<bookmark mark='a'/>在研究年份，它成本前每年赚{100 * a['mean_total']:.0f}%。"
        "<bookmark mark='b'/>其中{100 * vol:.0f}%来自波动率因子：组合做空波动大的币种，而波动率因子亏损惨重。其他因子大致相互抵消。"
        "<bookmark mark='c'/>特质收益，也就是公式自己的那部分，每年为{100 * a['mean_specific']:.1f}%。",

    'f"Day by day.':
        "逐日来看。<bookmark mark='a'/>组合，以及它的因子部分，几乎完全重合。<bookmark mark='b'/>还有特质部分，它上涨了一段时间，然后几乎全部吐了回去。"
        "<bookmark mark='c'/>组合的夏普比率为{a['sharpe_total']:.2f}；特质部分的为{a['sharpe_specific']:.2f}。因子承载了它{100 * a['var_share_factor']:.0f}%的方差。",

    "What attribution teaches.":
        "归因教给我们什么。<bookmark mark='a'/>第29部分的搜索找到了一种做空高波动币种的新方式：低波动因子，被重新包装成一个公式。"
        "<bookmark mark='b'/>因子可以便宜地持有、有意识地确定规模；为它支付挖掘预算和试验次数，等于付了两次钱。"
        "<bookmark mark='c'/>补救办法是在残差上挖掘：在打分之前先让每个候选对风险模型的因子中性化，这样只有因子无法解释的技能才会得到奖励。",

    "One more split.":
        "再做一次拆分。<bookmark mark='a'/>一个因子的平均贡献，等于平均暴露乘以平均因子收益，再加上两者的协方差。"
        "<bookmark mark='b'/>第一部分是恒定暴露本来就能赚到的：一种溢价，可以便宜地复制。<bookmark mark='c'/>第二部分是择时：恰好在因子表现好的日子之前持有更多暴露。"
        "声称会择时因子的经理，应该在这一项里证明它。",

    "Return is attributed; so is risk.":
        "收益可以归因，风险也可以。<bookmark mark='a'/>波动率对持仓是一次齐次的，所以欧拉定理把它精确地拆分成可加的贡献：每个持仓乘以它的边际风险。第30部分的风险平价用的就是同样的拆分。"
        "<bookmark mark='b'/>按因子归组，每个因子的份额就是组合对它的暴露乘以它与整个组合的协方差。"
        "<bookmark mark='c'/>贡献可以为负：那个仓位对冲了其余部分。每天的风险报告就是这张表，放在收益归因旁边。",

    "Pause and predict. A fund returned twelve percent.":
        "暂停一下，预测一下。一只基金收益为百分之十二。它的平均市场贝塔为零点四，市场收益为百分之二十，择时项为百分之二。选股贡献了多少？",

    # ------------------------------------------------------------------ Envelope
    "Chapter eleven. Chapter five's trader":
        "第十一章。第五章的交易者，在信封打开之前登记，并在2021到2025年上一次性评判。",

    'f"The registration.':
        "登记内容。<bookmark mark='a'/>第五章的两个信号，用于每个合格币种，合成为目标组合，并以Gârleanu和Pedersen的速率向它交易，成本水平选在短视交易者已经失败的地方。"
        "每个参数都在研究年份固定，成本计入损益之内。<bookmark mark='b'/>它被计入{e['n_trials']}次试验，即为选出它而比较过的每个成本水平和交易者。计数器变为{n_now:,}。",

    'f"The envelope.':
        "打开信封。<bookmark mark='a'/>在研究年份，扣除成本后的夏普比率为{gp['sr_res']:.2f}。"
        "<bookmark mark='b'/>在封存年份，一场灾难：{gp['sr_hold']:.2f}，亏损是它所缩放到的波动率的许多倍。短视交易者在同样的年份上也一样糟糕，{my['sr_hold']:.2f}。坏掉的不是交易规则。",

    'f"Did the dynamic trader at least beat the myopic one?':
        "动态交易者至少胜过了短视交易者吗？<bookmark mark='a'/>在研究年份，遥遥领先：在相同成本下，{gp['sr_res']:.2f}对{my['sr_res']:.2f}。"
        "<bookmark mark='b'/>在封存年份，两者都崩溃了。不管坏掉的是什么，坏掉的是它们共用的信号和风险模型，而不是交易的方式。",

    'f"The Track Record\'s row, in months.':
        "业绩记录中按月计的这一行。<bookmark mark='a'/>研究期：夏普比率{r['sharpe']:.2f}，{r['n']}个月的标准误为{r['sharpe_se']:.2f}。"
        "封存年份：{h['sharpe']:.2f}，年化波动率{100 * h['vol']:.0f}%，而原本打算的是百分之十。这一行按原样记录。",

    'f"The diagnosis, run on the registered rule exactly as it was.':
        "诊断，在登记的规则上原样运行。<bookmark mark='a'/>把每天的损益按币种拆开。在{dg['n_days']:,}天中的{dg['days_affected']}天里，组合持有近期波动率几乎降到零的币种。"
        "其中几乎全部发生在2025年最后两个月：锚定美元的稳定币USDe成交量足以进入股票池；CVC和FTT各有一天几乎冻结。这些仓位承载了{100 * s:.0f}%的方差。"
        "<bookmark mark='b'/>组合的其余部分夏普比率为{dg['sr_rest']:.2f}。这个数字是诊断，不是结果：封存年份现在已经被看过，修复后的规则将是一次新的试验，而且是在不再封存的数据上。",

    "Why. <bookmark mark='a'/> The rule divides each forecast":
        "为什么。<bookmark mark='a'/>规则用每个资产的预测方差去除它的预测。"
        "<bookmark mark='b'/>稳定币，或者已经停止交易的币种，方差接近零，规则就会建立一个没有上限的仓位。在研究年份，没有一个合格币种有那么平静，所以这个缺陷无从显现。"
        "<bookmark mark='c'/>而方差接近零，只到它不再接近零为止。这是一场微缩的量化地震：风险模型说这个仓位没有风险。",

    "What the House changes, for every future rule":
        "本系列公司为今后的每条规则做出的改变，不计为试验，因为它不是策略。<bookmark mark='a'/>每个预测方差都设下限，下限按资产类别设定。"
        "<bookmark mark='b'/>仓位限额完全不依赖模型，按组合的份额和日成交量的份额来设。"
        "<bookmark mark='c'/>以及一个了解自己资产是什么的股票池：挂钩的和停牌的工具在任何信号看到它们之前就被剔除。",

    "Pause and predict. After seeing this result":
        "暂停一下，预测一下。看到这个结果后，一个交易台加上方差下限，重新运行2021到2025年。夏普比率是零点四。业绩记录可以怎样记录这个数字？",

    # ------------------------------------------------------------------ House
    "Chapter twelve. The House's thirty-first rule":
        "第十二章。本系列公司的第31条规则：一个策略在获得资金之前，必须展示哪些关于风险、成本和交易的东西。",

    "The first sheet. <bookmark mark='a'/> A moving IC":
        "第一张表。<bookmark mark='a'/>变动的IC让信息比率降低了一半以上。币种的大部分风险是共同的，模型的预测通过了偏差检验。收缩贝塔降低了误差。"
        "成本让一个好信号在一百万美元时夏普比率跌到零以下。Gârleanu和Pedersen的交易者扛住了短视交易者扛不住的成本。挖出的阿尔法大部分是一个因子。"
        "登记的规则在封存年份失败了，原因本系列公司现在说得出来。",

    "Chapter two's regression, as the House runs it.":
        "第二章的回归，按本系列公司的方式运行。每天，保留有收益且暴露齐全的资产；给它们加权；用一丝岭惩罚求解加权正规方程，这样共线的一天也不会出错；"
        "并保留残差，它们就成为特质收益。十四行代码承载了整个风险模型。",

    "And Chapter five's trade rate, three lines":
        "还有第五章的交易速率，三行，后面跟着测试套件用来检查它的笨办法：在二次价值函数上做值迭代，直到系数不再变化。本系列公司两者都保留，因为没有检验的闭式解只是一个断言。",

    "And the two guards the envelope asked for":
        "还有信封所要求的两道防护，在它打开之后加入库中，从现在起用于每条规则。每个预测方差的下限，按资产类别设定。"
        "以及根本不参考模型的仓位上限：组合的一个份额，和资产日成交量的一个份额。这六行代码本可以改变第十一章，而本系列公司不能把它们用在第十一章的封存年份上。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>风险模型；它的收缩与检验；基本定律及其修正；成本与动态交易；归因；以及两道防护。"
        "<bookmark mark='b'/>还有第31条规则。一个策略只有在满足以下条件时才能获得资金：它的风险由本系列公司的模型预测，并报告模型的偏差统计量；它的损益归因到因子和特质收益；"
        "它的成本按预定规模定价，并说明容量；它的交易规则知道明天会到来；每个预测方差都有下限，每个仓位都有上限，而这些限额不依赖模型。",

    "The rule against three cases.":
        "用这条规则检验三个案例。<bookmark mark='a'/>一个信息比率为三的推介：问IC随时间的标准差，正如研究章节所示，它为信息比率设了上限，无论资产有多少。"
        "<bookmark mark='b'/>一只波动率为百分之三的市场中性基金：问用的是谁的风险模型，以及强制平仓拥挤仓位会损失多少。"
        "<bookmark mark='c'/>一个夏普比率为二的日度策略：问它的换手，以及它是按什么规模计算成本的。",

    # ------------------------------------------------------------------ Research
    "For the researcher. The fundamental law treats":
        "写给研究者。基本定律把信息系数当作常数。它不是。下面给出它变动的精确代价：证明、模拟，并在币市上测量。",

    "The setup. <bookmark mark='a'/> In period t":
        "设定。<bookmark mark='a'/>在第t期，标准化收益等于该期的IC乘以得分，加上独立噪声。<bookmark mark='b'/>IC本身每期抽取，均值为mu，标准差为sigma。"
        "<bookmark mark='c'/>组合持有得分，所以它的收益是得分与收益乘积的平均。",

    "The proof is four lines.":
        "证明只有四行。<bookmark mark='a'/>把收益模型代入组合收益。"
        "<bookmark mark='b'/>得分是标准化的，所以第一个平均恰好为一；第二个是方差为N分之一的噪声，与IC独立。所以组合赚到该期的IC，加上随广度分散的噪声。"
        "<bookmark mark='c'/>它的均值是mu。<bookmark mark='d'/>根据全方差公式，它的方差是IC自身的方差，这部分不会被分散，加上噪声项，这部分会被分散。",

    'f"The theorem.':
        "定理。<bookmark mark='a'/>信息比率等于平均IC除以IC方差加上噪声方差除以N的平方根。"
        "<bookmark mark='b'/>IC从不变动时，它就是基本定律，IC乘以根号N。广度无限增大时，它趋于mu除以sigma：IC序列本身的信息比率，任何广度都无法超越。"
        "<bookmark mark='c'/>开头的数字：mu百分之五，sigma百分之十，五百只股票，每月{per:.2f}，每年{per * math.sqrt(12):.2f}，而不是三点九。",

    'f"Simulated. A mean IC of four percent':
        "模拟。平均IC为百分之四，广度从二十到一千。<bookmark mark='a'/>基本定律的承诺无限上升。"
        "<bookmark mark='b'/>IC波动百分之三时，信息比率弯向它的上限一点三三；波动百分之八时，它在零点五附近变平。"
        "<bookmark mark='c'/>模拟的策略落在公式上：一千个资产时，模拟值为{big[0]['sim']:.2f}和{big[1]['sim']:.2f}，预测值为{big[0]['formula']:.2f}和{big[1]['formula']:.2f}，而朴素定律说的是{big[0]['naive']:.2f}。",

    "A corollary every researcher should know.":
        "每个研究者都应该知道的一个推论。<bookmark mark='a'/>两个方差项在广度约为sigma平方分之一时相等。<bookmark mark='b'/>在那里，信息比率已经达到上限的百分之七十一。"
        "<bookmark mark='c'/>IC波动百分之十时，这个广度约为一百。超过它，提高信息比率的办法是更稳定的预测，而不是更多的资产。"
        "这就是为什么交易台逐月跟踪IC的标准差，以及为什么一个稳定有效的信号比一个时而惊艳的信号更值钱。",

    'f"Now the coins: the six signals of Chapter seven.':
        "现在看币市：第七章的六个信号。<bookmark mark='a'/>它们的日度IC很小，波动却极大：挖出的阿尔法平均为{m['ic']:.3f}，标准差为{m['ic_sd']:.2f}。"
        "<bookmark mark='b'/>朴素定律承诺它的日度信息比率为{m['naive']:.2f}；定理把它削减到{m['formula']:.2f}。"
        "<bookmark mark='c'/>组合实际每天赚到{m['realised']:.3f}。更接近了，但仍差两倍多。还缺了什么。",

    'f"The missing piece is the shape of the returns.':
        "缺的是收益分布的形状。<bookmark mark='a'/>组合的收益是其权重与收益之间的线性相关，乘以收益的离散度。"
        "<bookmark mark='b'/>我们测量的IC是秩相关，在厚尾下两者不同：少数极端波动主导了线性相关，并给它加上了噪声。"
        "<bookmark mark='c'/>币种日收益的超额峰度为{t['kurtosis']:.0f}；正态分布为零。",

    'f"The ladder of corrections, for the mined alpha.':
        "挖出的阿尔法的修正阶梯。<bookmark mark='a'/>基本定律：{m['naive']:.2f}。变动的IC：{m['formula']:.2f}。"
        "<bookmark mark='b'/>把秩IC换成组合实际权重与收益之间逐日的线性相关，取它的均值除以标准差，这已经包含了噪声项：{m['pearson_ir']:.3f}。"
        "<bookmark mark='c'/>组合赚到{m['realised']:.3f}，在一个标准误之内，约{se:.3f}。三个修正，每个都有理由，把承诺从每天半个夏普比率带到了实际赚到的数字。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>当IC有自相关时，年化信息比率不再是期数的平方根乘以日度信息比率；加上成本和动态交易，就没有闭式解。"
        "<bookmark mark='b'/>在资产相关、信号重叠时，广度是有效下注次数，如何估计它而不高估，一般情形下尚未解决。"
        "<bookmark mark='c'/>以及在收益厚尾时，使信息比率最大化的得分加权方式，没有已知的闭式解。",

    "Pause and predict. A signal's monthly IC":
        "暂停一下，预测一下。一个信号的月度IC均值为零点零三，标准差为零点零六。任何广度能给它的最大年化信息比率是多少？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-one in fourteen lines.":
        "用十四行回顾第31部分。基本定律把技能和广度变成信息比率，转移系数为约束收费。因子风险模型用少数几个因子加一个对角矩阵来预测许多资产的协方差；"
        "在币市上，大部分风险是共同的，偏差统计量检验了预测。Vasicek的收缩改进了贝塔。平方根法则为每笔交易定价，并给每个策略一个容量。"
        "Gârleanu和Pedersen的交易者瞄准目标前方、每次只走一部分，扛住了短视交易者扛不住的成本。",

    "Multi-period optimisation keeps the idea":
        "多期优化保留了这个思想，而不需要闭式解。用回归合成信号，在样本外输给了简单权重。容量是一个选择，Berk和Green解释了为什么投资者看不到技能。"
        "2007年8月展示了共享的风险模型看不到什么。归因表明挖出的阿尔法大部分是一个因子。登记的规则因接近零的方差而失败。研究章节精确地证明了变动的IC代价有多大。",

    "Six desk questions.":
        "六个交易台问题。IC为百分之五，五百只股票，每月调仓：定律说三点九，而波动的IC说约一点六。"
        "<bookmark mark='a'/>偏差统计量为一点三，意味着模型把那个组合的风险低估了百分之三十。<bookmark mark='b'/>一个因子中性的组合，可能通过模型不包含的风险在一周内亏损百分之十。",

    "At four times the size, costs per dollar double.":
        "规模变成四倍，每美元成本翻倍。<bookmark mark='a'/>成本变成四倍时，交易速度减半，并更偏向慢信号。"
        "<bookmark mark='b'/>看过封存年份之后修复的规则，是在不再封存的数据上的一次新试验。完整解答在讲义中。",

    "And twelve problems:":
        "还有十二道习题：开头的信息比率；偏差统计量的区间；一个Vasicek贝塔；四倍规模下的成本；利润最大化的规模；交易速率的极限；合成两个信号；由衰减得到换手；"
        "手算归因；以及信息比率的上限。然后是两道资格考试题：研究章节的定理，以及从Riccati方程推出Gârleanu和Pedersen的解。中英文解答都在讲义中。",

    "Where this comes back.":
        "这些内容在哪里再次出现。第32部分用这一部分的成本和风险模型，在各资产类别上交易趋势和套息。第33部分讲公司，在那里容量和费用决定谁拿走阿尔法。"
        "第37部分推导平方根法则并安排交易。第41部分回到拥挤和流动性螺旋。终章会对每一行做紧缩检验。",

    "The textbooks this part follows":
        "这一部分所依据的教科书，以及它引用的论文，从Blume和Vasicek的贝塔，到AQR对自身成本的测量。屏幕上的每个数字都由本系列公司的代码，"
        "从币安的公开市场数据和Kenneth French的行业组合计算得出，模拟和示意都有标注。",

    "The House's portfolio and risk desk now has":
        "本系列公司的组合与风险部门现在有了风险模型、成本模型和交易规则，以及两道吃过苦头才学会的防护。"
        "<bookmark mark='a'/>下一部分，第32部分：系统化宏观与另类溢价。跨越一个世纪的趋势跟踪，波动率目标，以及把套息、价值和防御溢价作为一个组合。",
}
