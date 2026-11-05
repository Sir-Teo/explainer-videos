"""Chinese narration for quant37: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 市场冲击 (market impact), 执行 (execution), 母订单/元订单
(metaorder), 子订单 (child order), 参与率 (participation rate), 执行差额 (implementation shortfall), 平方根法则
(square-root law), 潜在流动性 (latent liquidity), 传播子 (propagator), 响应函数 (response function), 无动态套利
(no dynamic arbitrage), 衰减核 (decay kernel), 正定 (positive definite), 韧性 (resilience), 时间加权平均价格 (TWAP),
成交量加权平均价格 (VWAP), 成交量占比 (POV), 交易成本分析 (TCA), 智能订单路由 (smart order routing), 到达价格
(arrival price), 弗雷德霍姆方程 (Fredholm equation)."""

TITLE = '量化金融，从零搭建 · 第37部分：市场冲击与执行'

CHAPTERS = {
    'Hook': '百分之十花三十个基点；百分之四十花多少？',
    'Meta': '1. 元订单',
    'Sqrt': '2. 平方根法则',
    'Prop': '3. 传播子',
    'NoArb': '4. 无动态套利',
    'AC': '5. Almgren与Chriss',
    'OW': '6. 会恢复的订单簿',
    'RL': '7. 学出来的执行者',
    'Algos': '8. 算法与账单',
    'House': '9. 第37条规则：交易之前先定价',
    'Research': '写给研究者：暂时性冲击下的最优执行时间表',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-seven. Market impact and execution":
        "第37部分。市场冲击与执行：一笔大订单会让价格朝不利于下单者的方向移动多少，以及怎样下单才能让成本最低。",

    'f"A question asked of execution traders.':
        "一道问执行交易员的题。<bookmark mark='a'/>买入一只股票一天成交量的十分之一，冲击成本是30个基点。买入十分之四要多少？"
        "<bookmark mark='b'/>直线说是120个基点。<bookmark mark='c'/>几乎所有大型真实订单数据都说是{a:.0f}：冲击随规模的平方根增长。"
        "为什么会这样，以及这对如何交易意味着什么，就是这一部分的内容。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>冲击是凹的：在比特币上，一分钟的价格变动按带方向成交量的{ag['slope']:.2f}次方增长；"
        "在潜在流动性模型中，随着订单变大，指数从1降到约{lt['slope_large']:.2f}。<bookmark mark='b'/>最优时间表是一个定理："
        "对害怕风险的交易者是Almgren和Chriss的答案，对会恢复的订单簿是Obizhaeva和Wang的答案，这里给出证明。"
        "<bookmark mark='c'/>而一个诚实衡量的学习型执行者，没有胜过最朴素的时间表：{r['Q-learning']['mean']:.1f}个半跳，"
        "TWAP是{r['TWAP']['mean']:.1f}个。",

    "Why it matters. <bookmark mark='a'/> A strategy's capacity":
        "为什么这很重要。<bookmark mark='a'/>一个策略的容量，就是它的冲击吃掉它的阿尔法时的规模：第31部分的平方根已经决定了"
        "本系列公司的规模。<bookmark mark='b'/>对大额交易的基金来说，冲击是它付出的最大成本，远高于手续费和价差。"
        "<bookmark mark='c'/>一整个行业，券商的算法、交易成本分析和订单路由，都因为这一条曲线而存在。",

    "Three beliefs this part corrects.":
        "这一部分纠正的三个看法。<bookmark mark='a'/>认为冲击就是价差：对小订单成立，但对占一天成交量相当份额的订单，价差只是零头。"
        "<bookmark mark='b'/>认为拆单总有帮助：拆单能隐藏订单、分散风险，但在平方根法则下，它几乎不降低预期冲击。"
        "<bookmark mark='c'/>认为成本低的执行就是好执行：单笔订单的成本大部分是运气，执行只能在许多订单上评判。",

    "Where this sits. Part thirty-five asked who trades with whom; Part thirty-six":
        "这一部分的位置。第35部分问的是谁与谁交易；第36部分打开了订单簿。这一部分把一笔大订单送进订单簿，"
        "而第38部分坐在另一边，作为吸收它的做市商。",

    "Fifty years of the subject.":
        "这个领域的五十年。1972年，Alan Kraus和Hans Stoll测量了大宗交易的冲击；André Perold定义了执行差额；Dimitris Bertsimas"
        "和Andrew Lo，以及后来的Robert Almgren和Neil Chriss，把执行表述为最优控制问题。<bookmark mark='a'/>接着是传播子、"
        "Jim Gatheral的无动态套利条件、在各个市场上测得的平方根法则，以及Obizhaeva和Wang的有韧性的订单簿。"
        "<bookmark mark='b'/>再后来是潜在流动性、微观结构不变性和强化学习。",

    "The plan: metaorders and what public data shows":
        "计划如下：元订单以及公开数据能显示什么；平方根法则与潜在流动性；传播子；哪些冲击模型是被允许的；Almgren和Chriss，"
        "然后是Obizhaeva和Wang；一个学习型执行者、券商出售的算法和交易成本分析；最后证明暂时性冲击下的最优时间表。",

    "In the House, the execution desk opens":
        "在本系列公司里，执行台开张了：它接收组合台发来的每一笔订单，为它安排时间表，并报告它花了多少成本。",

    # ------------------------------------------------------------------ Meta
    "Chapter one. No institution buys a large position in one order.":
        "第1章。没有哪家机构会用一笔订单建立大头寸。它把一个决定拆成成百上千个子订单，分布在数小时或数天里。"
        "这整体叫作元订单，它的成本就是这一部分的主题。",

    "The vocabulary. <bookmark mark='a'/> A parent order of total size Q":
        "术语。<bookmark mark='a'/>一个总规模为Q的母订单，以许多子订单的形式发出。<bookmark mark='b'/>它的参与率："
        "它在执行期间占市场成交量的份额，是执行者能控制的主要旋钮。<bookmark mark='c'/>以及它的冲击：在它整个执行期间，"
        "价格朝交易方向的移动。",

    "How the cost is measured.":
        "成本如何衡量。<bookmark mark='a'/>André Perold的执行差额：把真实组合与一个按决策时价格成交的纸面组合比较，"
        "再加上从未成交的部分。<bookmark mark='b'/>它分成延迟成本、跨越价差并推动价格的成本、价格路径的运气，以及错失的机会。"
        "<bookmark mark='c'/>对任何占一天成交量相当份额的订单，佣金只是几分钱，冲击才是那张账单。",

    "The shape every large study reports.":
        "每一项大型研究都报告的形状。<bookmark mark='a'/>元订单执行期间，价格朝它的方向移动，而且是凹的：先快后慢。"
        "<bookmark mark='b'/>停止之后，价格回撤一部分。Esteban Moro和同事，以及Nataliya Bershova和Dmitry Rakhlin发现，"
        "大约三分之二的峰值保留下来。付出了峰值、保留三分之二的交易者，就有三分之一是纯粹的成本。",

    "Who receives the cost.":
        "谁收到了这笔成本。<bookmark mark='a'/>冲击是某个人的收入：价格朝买方不利的方向移动，被卖给它的人赚走了，"
        "也就是做市商和另一边有耐心的交易者。<bookmark mark='b'/>回撤的部分是流动性的价格。保留下来的部分，是市场得知有人想买。"
        "<bookmark mark='c'/>第35部分的Kyle市场让冲击全部是永久的、线性的。真实的元订单是凹的、部分暂时的，这需要比Kyle更多的东西。",

    'f"What we can measure.':
        "我们能测量什么。<bookmark mark='a'/>元订单是私有的：大型研究使用的是券商和基金自己的记录。公开的成交记录只显示成交，"
        "不显示是谁发出的。<bookmark mark='b'/>它确实能显示总体冲击：一个时间窗口内的价格变化，对所有人加在一起的带方向成交量。"
        "<bookmark mark='c'/>我们的数据：2023年5月比特币永续合约的十天成交记录，每天约{ag['v_day'] / 1000:.0f}千个比特币成交。",

    "How researchers see metaorders at all.":
        "研究者到底怎么看到元订单。<bookmark mark='a'/>专有记录，即券商或基金自己与母订单关联的子订单：这是黄金标准。"
        "<bookmark mark='b'/>泄露的账户数据，比如来自Mt. Gox交易所的数据。<bookmark mark='c'/>或者从成交记录中找代理变量，"
        "比如同方向成交的连串或券商代码：噪声大，而且偏向那些容易被发现的订单。",

    'f"Aggregate impact on Bitcoin.':
        "比特币上的总体冲击。<bookmark mark='a'/>在10秒、1分钟和5分钟的窗口里，平均价格变化对不平衡作图：买入减卖出，"
        "再除以两者之和。<bookmark mark='b'/>在零附近是线性的，然后变平：不平衡超过约一半之后，更加一边倒也换不来更多的价格变动。"
        "Felix Patzelt和Jean-Philippe Bouchaud在期货和股票上发现了同样的S形。在一分钟尺度上，最强的不平衡让价格移动约{mx:.0f}跳。",

    'f"And against size.':
        "再对规模作图。<bookmark mark='a'/>把每一分钟按带方向成交量的大小排序，在对数坐标上画出朝该方向的价格变动。"
        "<bookmark mark='b'/>斜率是{sl:.2f}：凹的，介于直线和平方根之间。这还不是平方根法则，那条法则说的是单个交易者的元订单"
        "在整个执行期间的冲击。但这是同样的凹性，只是在所有人的订单流里同时看到的。",

    "Pause and predict. An order buying one percent":
        "暂停并预测。一笔买入一天成交量百分之一的订单让价格移动10个基点。按平方根法则，百分之四的订单会怎样？按线性法则呢？",

    # ------------------------------------------------------------------ Sqrt
    "The answer to the pause. <bookmark mark='a'/> Under the square-root law, four times":
        "暂停问题的答案。<bookmark mark='a'/>按平方根法则，规模变为四倍，价格移动变为两倍：20个基点。<bookmark mark='b'/>按直线，"
        "是40个基点。<bookmark mark='c'/>这个差别不是细节：在平方根下，每买一个单位的冲击随规模下降。",

    "Chapter two. The most robust empirical regularity":
        "第2章。市场微观结构中最稳健的经验规律，以及一个关于它为什么成立的谜。然后是一个解释它的隐藏流动性模型。",

    "The law. <bookmark mark='a'/> The impact of a metaorder":
        "法则。<bookmark mark='a'/>以日波动率为单位，元订单的冲击约等于它占日成交量份额的平方根。Thomas Loeb和Nicolò Torre"
        "在股票上测量过，Almgren和同事在花旗集团的订单上测量过，Bence Tóth和同事在期货上测量过。<bookmark mark='b'/>在非常不同的市场上，"
        "前因子都是1的量级。<bookmark mark='c'/>而且在一阶近似下，它取决于买了多少，而不是买得多快。",

    "How universal. <bookmark mark='a'/> Across thousands of stocks":
        "有多普适。<bookmark mark='a'/>在数千只股票和数十种期货上，在跨越好几个数量级的规模上，指数都接近二分之一。"
        "<bookmark mark='b'/>在比特币上，Jonathan Donier和Julius Bonart从Mt. Gox交易所泄露的账户级记录中重建了约一百万个元订单，"
        "也发现了平方根。<bookmark mark='c'/>也有局限：非常小的订单表现出线性冲击，有些数据用对数拟合更好，前因子也会变化。",

    'f"What the law says for Bitcoin\'s perpetual':
        "这条法则对比特币永续合约意味着什么，取前因子为1。<bookmark mark='a'/>一天成交量的千分之一，约{m01:.0f}百万美元，"
        "成本约{costs[0]:.0f}个基点。<bookmark mark='b'/>百分之一，约{costs[1]:.0f}个基点：规模十倍，成本三倍。"
        "<bookmark mark='c'/>一天的十分之一，约{costs[2]:.0f}个基点，相当于一天波动率的三分之一。",

    "Why is it a puzzle?":
        "为什么这是个谜？<bookmark mark='a'/>Kyle的模型给出直线。平方根意味着市场吸收大订单比任何固定深度都更便宜。"
        "<bookmark mark='b'/>可见的订单簿帮不上忙：它只容纳一天成交量的很小一部分，一笔百分之一的元订单会把它清空很多次。"
        "<bookmark mark='c'/>所以流动性必然是潜在的：那些愿意在某个价格买或卖、但只在价格靠近时才显露出来的交易者。",

    "A second route, by dimensions.":
        "第二条路，量纲分析。<bookmark mark='a'/>以波动率为单位的冲击，只能取决于订单占成交量的份额和它的持续时间。"
        "<bookmark mark='b'/>数据说持续时间几乎无关紧要。<bookmark mark='c'/>一个启发式论证补上最后一步：在时间T内吸收这笔订单的"
        "流动性提供者，要求补偿sigma乘根号T的风险，而他们提供的成交量随T增长；消去时间，就剩下平方根。"
        "这是启发式，不是定理，但它解释了这条法则为什么如此普适。",

    'f"How small the visible book is.':
        "可见的订单簿有多小。<bookmark mark='a'/>第36部分测得两个最优报价处约有10个比特币。<bookmark mark='b'/>这个合约每天成交约"
        "{ac['v_day'] / 1000:.0f}千个比特币。<bookmark mark='c'/>显示出来的最优报价只占一天成交量的{share:.3f}%。"
        "吸收大订单的东西，都是随着价格移动才到来的：这就是潜在的含义。",

    "The picture of latent liquidity.":
        "潜在流动性的图像。<bookmark mark='a'/>价格之下隐藏的买入意愿和价格之上隐藏的卖出意愿。Jonathan Donier、Julius Bonart、"
        "Iacopo Mastromatteo和Bouchaud证明，如果这些潜在订单不断到达、被撤销并随机修改价格，那么价格附近的密度呈V形："
        "随着离价格的距离线性增长。<bookmark mark='b'/>买方必须吃掉旧价格和新价格之间的所有卖单：一个三角形。",

    "The derivation in three lines.":
        "三行推导。<bookmark mark='a'/>在价格附近，潜在密度是线性的，斜率为花体L。<bookmark mark='b'/>要把价格从0推到delta，"
        "买方必须吸收其间的每一个卖单：三角形的面积，二分之一L乘delta的平方。<bookmark mark='c'/>反解，价格按2Q除以L的平方根移动。"
        "<bookmark mark='d'/>而由量纲，斜率按成交量除以方差标度，这就变成了法则里的sigma乘以Q除以V的平方根。",

    'f"Now simulate it:':
        "现在来模拟：潜在密度在扩散，买方在一个单位时间内于价格处移除卖单，规模跨越五个数量级。<bookmark mark='a'/>小订单让价格按比例移动，"
        "斜率{lt['slope_small']:.2f}：订单簿有时间在它们周围回补。<bookmark mark='b'/>大订单弯向平方根，斜率{lt['slope_large']:.2f}，"
        "逼近静态订单簿的公式。小订单线性，大订单平方根：这正是Federico Bucci和同事在真实数据中发现的转变。",

    'f"And after the order stops.':
        "订单停止之后。<bookmark mark='a'/>价格在买入结束时达到峰值{peak:.1f}，<bookmark mark='b'/>然后随着潜在订单簿愈合而衰减，"
        "再过九个单位时间降到{end:.1f}，并继续缓慢地按时间平方根的倒数衰减。在这个纯粹的模型里没有什么是永久的；"
        "在真实市场里，信息让其中一部分留下来。",

    "And a striking consequence.":
        "一个惊人的推论。<bookmark mark='a'/>假设冲击随已买入数量的平方根增长。<bookmark mark='b'/>那么平均成交价位于通往峰值的"
        "三分之二处。<bookmark mark='c'/>Doyne Farmer、Austin Gerig、Fabrizio Lillo和Henri Waelbroeck提出了公平定价论证："
        "在竞争性市场中，价格应当停在平均成交价上，这样买方和流动性提供者平均都不赚钱。于是峰值的三分之二留了下来："
        "第1章报告的回撤，由平方根推导出来了。",

    "A different route to universality.":
        "通往普适性的另一条路。<bookmark mark='a'/>Albert Kyle和Anna Obizhaeva把交易活跃度定义为波动率乘以美元成交量。"
        "<bookmark mark='b'/>他们的不变性假设说，赌注在业务时间中到达，并在每个市场转移相同的美元风险；"
        "这确定了赌注数量如何随活跃度标度，即它的三分之二次方。<bookmark mark='c'/>所以以波动率为单位的冲击，对每种资产来说，"
        "都是以赌注为单位的规模的同一个函数。平方根与它相容，而它还预测了前因子应如何随市场变化。",

    "Pause and predict. The signs of trades are predictable":
        "暂停并预测。正如第36部分所示，成交方向在数百笔之后仍可预测，价格却不可预测。每笔成交的冲击随时间必须怎样变化？",

    # ------------------------------------------------------------------ Prop
    "Chapter three, and the answer to the pause: the impact of each trade must decay.":
        "第3章，以及暂停问题的答案：每笔成交的冲击必须衰减。买单之后跟着买单，持续数百笔。如果每一笔都永久地推动价格，"
        "价格就会可预测地形成趋势。事实并非如此，所以每笔成交的冲击必须消退，而且恰好快到能抵消方向的可预测性。",

    "The model. <bookmark mark='a'/> Jean-Philippe Bouchaud, Yuval Gefen":
        "模型。<bookmark mark='a'/>Jean-Philippe Bouchaud、Yuval Gefen、Marc Potters和Matthieu Wyart把价格写成过去每一笔成交"
        "现存冲击的总和。G，即传播子，表示一笔成交的冲击在若干笔成交之后还剩多少。<bookmark mark='b'/>响应函数，即买入后l笔成交时"
        "价格移动了多少，它把G和之后的成交混在一起。<bookmark mark='c'/>而方向自相关就是第36部分的幂律。",

    'f"Measured on Bitcoin\'s tape':
        "在比特币的成交记录上测量，四天共{n_tr}笔成交，取每笔成交之前的中间价。<bookmark mark='a'/>一笔买入之后，价格在数百笔成交中"
        "持续上升，因为后面还有更多买入，并在约{lag_max}笔之后达到约{r_max:.0f}跳的峰值。<bookmark mark='b'/>然后它变平，并略微下弯。"
        "尽管买入还在继续，它也没有一直增长。",

    'f"Now separate the two.':
        "现在把两者分开。<bookmark mark='a'/>把每次价格变化对过去一千笔成交的方向做回归，这消除了方向之间的相关，再把系数累加。"
        "这就是传播子：一笔成交的冲击，随着订单簿吸收它，在约{p['G_peak_lag']}笔之后升到{p['G_peak']:.2f}跳，"
        "<bookmark mark='b'/>然后缓慢衰减，像滞后的幂函数，指数为{p['beta']:.2f}。",

    'f"A metaorder through Bitcoin\'s fitted propagator.':
        "让一笔元订单通过比特币拟合出的传播子。市场上每五笔成交中有一笔是我们的，全是买入，持续六百笔，然后停止。"
        "<bookmark mark='a'/>我们买入时冲击凹形上升，停止后衰减，四百笔之后降到峰值的约{100 * end:.0f}%："
        "第1章的形状，来自在成交记录上测得的单一核。",

    "What to distrust in this fit.":
        "这个拟合中不可轻信的地方。<bookmark mark='a'/>什么算一笔成交：归集成交记录把同一吃单者在同一价格的多次成交合并，"
        "所以一次扫单变成几条记录。<bookmark mark='b'/>时钟：中间价来自十分之一秒的网格，几笔成交共用一个快照，所以最初几个滞后不可靠。"
        "<bookmark mark='c'/>还有平稳性：四天，其中两天是周末。一条曲线是不同市场状态的平均。",

    'f"The balance.':
        "平衡。<bookmark mark='a'/>如果传播子按滞后的幂律衰减，<bookmark mark='b'/>那么把相关的方向通过它累加起来，价格的方差就按时间的"
        "某个幂增长。<bookmark mark='c'/>要让价格扩散，既不形成趋势也不回复，衰减指数必须等于1减gamma再除以2：市场对方向的记忆"
        "与冲击的消退恰好抵消。<bookmark mark='d'/>在比特币上，拟合给出{p['beta']:.2f}，预测值是{p['beta_theory']:.2f}："
        "量级相同，衰减稍快，数据只有四天，网格也粗。",

    "What the propagator says.":
        "传播子说了什么。<bookmark mark='a'/>一笔预期之中的成交比一笔出人意料的成交对价格的影响更小：传播子是用线性方式说出这一点。"
        "<bookmark mark='b'/>让一笔元订单通过它，一连串各自衰减的子订单，冲击在执行期间凹形增长，停止后衰减：第1章的形状。"
        "<bookmark mark='c'/>但线性的传播子无法让冲击成为规模的平方根。那需要潜在订单簿的非线性。",

    "Two ways to say it.":
        "两种说法。<bookmark mark='a'/>本章的暂时性冲击模型：每笔成交的冲击按一个固定的核衰减。<bookmark mark='b'/>或者历史依赖冲击："
        "只有每个方向中的意外成分推动价格，所以预期之中的成交几乎没有成本。Lillo和Farmer称之为不对称流动性：预期会被打的一侧会被填满。"
        "<bookmark mark='c'/>两者都调和了可预测的订单流与不可预测的价格；它们的区别在于对单个交易者的元订单作何预测。",

    "Pause and predict. Suppose each trade's impact lasted":
        "暂停并预测。假设每笔成交的冲击持续一段时间，然后完全消失。一个交易者能否先买入再卖回，仅靠自己的冲击赚钱？",

    # ------------------------------------------------------------------ NoArb
    "Chapter four, and the answer to the pause: yes.":
        "第4章，以及暂停问题的答案：能。如果冲击持续固定时间后消失，交易者可以先买入，等待，再卖给仍被买入推高的价格。"
        "一个冲击模型不能送出赚钱机器。Jim Gatheral把这一点变成了条件。",

    "The setting. <bookmark mark='a'/> Linear transient impact":
        "设定。<bookmark mark='a'/>线性暂时性冲击：每交易一个单位，就按一个衰减的核G推动价格。<bookmark mark='b'/>一个交易计划的期望成本"
        "是一个二重积分：每笔交易都要付出之前交易留下的冲击，以及它自身冲击的一半。<bookmark mark='c'/>往返交易先买后卖回到零。"
        "没有信息的交易者永远不应期望从中获利。",

    "First, permanent impact.":
        "首先，永久冲击。<bookmark mark='a'/>假设以速率v交易会让价格永久移动f(v)。<bookmark mark='b'/>Gur Huberman和Werner Stanzl证明，"
        "除非f是线性的，否则快买慢卖，或者反过来，就能赚钱。<bookmark mark='c'/>而在线性永久冲击下，无论时间表如何，成本都是二分之一"
        "kappa乘X的平方：它无法被优化掉。只有暂时性的部分取决于怎样交易。",

    "Why it must be linear, in numbers.":
        "为什么必须是线性的，用数字来看。<bookmark mark='a'/>假设永久冲击随交易速率的平方增长。<bookmark mark='b'/>在一个单位时间内快速买入"
        "一个单位：价格上升1。<bookmark mark='c'/>在十个单位时间内慢慢卖回：价格只下降十分之一。<bookmark mark='d'/>仓位归零，价格却更高了："
        "卖出时的价格高于买入。重复下去，就是一台赚钱机器。只有线性函数才能让两次移动恰好抵消。",

    'f"The kernel of the pause:':
        "暂停问题里的那个核：冲击持续十分之三的时间范围，然后消失。<bookmark mark='a'/>搜索最便宜的往返交易，答案是一组针对核的边缘"
        "安排好时机的买卖。<bookmark mark='b'/>它的期望成本是负的：每单位交易{b['rt_cost']:.2f}。一台赚钱机器，完全不需要信息。"
        "所以这个核不可能是冲击的模型。",

    "The condition. <bookmark mark='a'/> Gatheral showed":
        "条件。<bookmark mark='a'/>Gatheral证明，当且仅当核是正定的，才没有任何往返交易的期望成本为负。<bookmark mark='b'/>由Bochner定理，"
        "这意味着它的傅里叶变换永不为负。<bookmark mark='c'/>方框核的变换是sinc函数，有些地方为负：所以才有那台机器。"
        "衰减的指数函数和幂律都能通过。",

    "A stronger condition.":
        "更强的条件。<bookmark mark='a'/>Aurélien Alfonsi、Alexander Schied和Alla Slynko证明，在凸且递减的核下，最优的买入方式从不卖出。"
        "<bookmark mark='b'/>仅有正定性还不够：有些禁止赚钱机器的核，仍然会让最好的买入方式包含卖出。<bookmark mark='c'/>高斯核就是一个："
        "正定，但在零附近是凹的。",

    'f"The Gaussian kernel, on eleven trading dates.':
        "高斯核，在十一个交易时点上。<bookmark mark='a'/>买入一个单位的最优方式是交替的：它总共买入{1 + gg['sell']:.2f}，"
        "再卖回{gg['sell']:.2f}。<bookmark mark='b'/>而且它比稳定买入更便宜，{gg['cost']:.3f}对{gg['twap']:.3f}。"
        "一个建议为了买入而卖出的模型，是在告诉你它的核错了。",

    'f"Refine the grid and it gets worse.':
        "把网格加细，情况更糟。<bookmark mark='a'/>六个时点时，最优方案几乎不卖出。到二十一个时点，为了买入一个单位，最大的单笔交易约为"
        "{last['max']:,.0f}个单位。成本持续下降，交易却在爆炸：极限下不存在最优策略，只有越来越剧烈地操纵自己的冲击。",

    'f"Does Bitcoin\'s fitted kernel pass?':
        "比特币拟合出的核能通过吗？<bookmark mark='a'/>越过峰值之后，第3章的传播子是指数为{p['beta']:.2f}的幂律。"
        "<bookmark mark='b'/>它是递减的、凸的。<bookmark mark='c'/>由Pólya判据，一个凸的、递减到零的偶函数是正定的。所以测得的核既不允许"
        "往返获利，也不允许靠卖出来买入：按拟合结果，这个市场没有动态套利。",

    "The lessons for a desk.":
        "给交易台的教训。<bookmark mark='a'/>在冲击模型驱动算法之前，先检验模型本身：正定，最好还凸且递减。"
        "<bookmark mark='b'/>Obizhaeva和Wang的指数核以及Bouchaud的幂律传播子都能通过。<bookmark mark='c'/>而一旦冲击对交易速率是非线性的，"
        "Gatheral证明指数衰减就不可能，幂律衰减则必须满足一个把它的指数与冲击指数联系起来的不等式：自由选择很少。",

    "Pause and predict. You must sell five thousand bitcoin":
        "暂停并预测。你必须在一小时内卖出五千个比特币。卖得快冲击更大；卖得慢则在价格风险中暴露更久。一个非常厌恶风险的卖方应该怎样交易？",

    # ------------------------------------------------------------------ AC
    "Chapter five, and the answer to the pause: fast at first":
        "第5章，以及暂停问题的答案：先快后慢。害怕价格波动的卖方会把卖出前置，付出更多冲击来承担更少风险。"
        "Robert Almgren和Neil Chriss在2000年把这个权衡精确化。",

    "The model. <bookmark mark='a'/> The price diffuses":
        "模型。<bookmark mark='a'/>价格在扩散，每次卖出按比例永久压低价格。<bookmark mark='b'/>实际得到的价格还要更低，"
        "低出一个与交易速率成正比的暂时性冲击。<bookmark mark='c'/>持仓在N个区间内从X降到零。",

    "The objective. <bookmark mark='a'/> The expected shortfall":
        "目标。<bookmark mark='a'/>期望差额：永久部分，任何时间表都改变不了；暂时部分，惩罚快速交易。<bookmark mark='b'/>它的方差："
        "每一个仍持有的单位都暴露在价格风险中，惩罚慢速交易。<bookmark mark='c'/>最小化均值加上lambda乘以方差。",

    "The solution. <bookmark mark='a'/> The first-order condition":
        "解。<bookmark mark='a'/>对每个持仓的一阶条件是一个线性二阶差分方程。<bookmark mark='b'/>持仓在开始时固定为X、结束时为零，"
        "解是双曲正弦。<bookmark mark='c'/>常数kappa，即lambda乘sigma平方除以eta的平方根，就是紧迫度：kappa的倒数是订单的半衰期。"
        "没有风险厌恶时是一条直线，即TWAP；风险厌恶很强时，几乎立刻卖完。",

    "The same answer in continuous time":
        "用第8部分的变分法，在连续时间里得到同样的答案。<bookmark mark='a'/>最小化速度成本（eta乘速率的平方）与风险成本"
        "（lambda乘sigma平方乘持仓的平方）之和的积分。<bookmark mark='b'/>欧拉-拉格朗日方程描述一个被弹簧拉向零的粒子。"
        "<bookmark mark='c'/>开始时满仓、结束时清空，解就是双曲正弦。",

    "A Bitcoin-sized example":
        "一个比特币规模的例子：在一小时内逐分钟卖出五千个比特币，约1.35亿美元，波动率和暂时性冲击用第1章的分钟数据估计。"
        "<bookmark mark='a'/>没有风险厌恶时，是一条直线。<bookmark mark='b'/>随着lambda增大，曲线向开头弯曲：更多在早期卖出，最后几分钟剩得很少。",

    "The efficient frontier.":
        "有效前沿。<bookmark mark='a'/>每个时间表是一个点：期望差额对它的标准差。TWAP平均最便宜，风险也最大。"
        "<bookmark mark='b'/>沿着曲线移动，就是用冲击换确定性，而且最初几步很便宜：在TWAP附近前沿是平的，所以任何厌恶风险的交易者"
        "都应该至少稍微前置一些。",

    'f"The numbers.':
        "数字。<bookmark mark='a'/>均匀卖出的暂时性冲击约为{tw['cost'] / 1000:.0f}千美元，{bp_tw:.1f}个基点，而标准差是"
        "{tw['sd'] / 1000:.0f}千美元：风险远远超过成本。<bookmark mark='b'/>中等的风险厌恶付出{mid['cost'] / 1000:.0f}千美元，"
        "把不确定性降到{mid['sd'] / 1000:.0f}千美元。<bookmark mark='c'/>它的半衰期约为{hl:.0f}分钟：订单的三分之二在前二十分钟完成。",

    'f"What lambda means.':
        "lambda意味着什么。<bookmark mark='a'/>它有单位：每平方美元不确定性对应的期望成本美元数。<bookmark mark='b'/>在10的负6次方时，"
        "这个时间表的风险项约值{pen / 1000:.0f}千美元。<bookmark mark='c'/>把它理解为确定性等价：交易台愿意以期望冲击的形式付出多少，"
        "来消除不确定性。选择lambda就是选择这个价格。",

    'f"But compare the square-root law.':
        "但与平方根法则比较一下。<bookmark mark='a'/>用按单个分钟拟合的线性暂时成本，Almgren和Chriss说是{bp_tw:.1f}个基点。"
        "<bookmark mark='b'/>对一笔占一天成交量{100 * frac:.1f}%的订单，平方根法则说约为{bp_sq:.0f}个基点。"
        "<bookmark mark='c'/>差距在于累积的冲击。线性模型立刻忘掉每一分钟的冲击；真实的冲击会持续并在订单执行期间累积。"
        "时间表的形状仍然有用，但它的成本必须来自平方根，或者来自传播子。",

    "What desks actually use.":
        "交易台实际用什么。<bookmark mark='a'/>交易前估计：每股付一半价差，订单整体用平方根，再加手续费。<bookmark mark='b'/>Almgren和同事"
        "在花旗集团自己的订单上，把暂时性冲击拟合为交易速率的五分之三次方，永久冲击为线性。<bookmark mark='c'/>所以实践是一种混合："
        "用最优控制的答案确定时间表的形状，用经验法则为它定价。",

    "Three extensions. <bookmark mark='a'/> With impact a power of the rate":
        "三个推广。<bookmark mark='a'/>当冲击是速率的幂时，Almgren证明曲线形状会改变，但仍会因风险而前置。<bookmark mark='b'/>更早的"
        "Bertsimas和Lo在有可预测漂移的情况下只最小化期望成本：没有漂移时，答案就是TWAP。<bookmark mark='c'/>而均值-方差时间表是静态的。"
        "Almgren和Julian Lorenz证明，随着价格变动重新优化，在盈利之后卖得更快，效果更好，代价是失去时间一致性。",

    "Beyond variance.":
        "超越方差。<bookmark mark='a'/>Alexander Schied和Torsten Schöneborn证明，在指数效用下静态时间表是最优的，在其他效用下时间表"
        "会随财富调整。<bookmark mark='b'/>当价格可能跳跃时，最小化差额的尾部度量会更多地前置。<bookmark mark='c'/>而在实践中，"
        "交易台并不选lambda：他们根据信号的衰减和订单的规模，设定一个紧迫度、半衰期或参与率。",

    "Pause and predict. Now impact decays":
        "暂停并预测。现在冲击会衰减：订单簿在两次交易之间恢复。一个风险中性的买方有一小时。稳定交易仍是最优的吗，"
        "还是应该把一部分订单整块成交？",

    # ------------------------------------------------------------------ OW
    "Chapter six. Almgren and Chriss's temporary impact vanishes":
        "第6章。Almgren和Chriss的暂时性冲击在每笔交易后的瞬间就消失了。真实的订单簿随时间恢复：被吃掉的流动性以某个速率被补充。"
        "Anna Obizhaeva和王江为这样的世界构建了时间表，它的答案令人惊讶。",

    "The model. <bookmark mark='a'/> A book with depth q":
        "模型。<bookmark mark='a'/>一个深度为q的订单簿：规模为x的买单吃掉卖单，把卖价抬高x除以q。<bookmark mark='b'/>这个偏移随后愈合："
        "新的卖单到来，以速率rho填补缺口，这就是韧性。<bookmark mark='c'/>这就是第4章带指数核的暂时性冲击：凸的、递减的、被允许的。",

    'f"The answer to the pause: blocks.':
        "暂停问题的答案：整块。<bookmark mark='a'/>趁订单簿未受扰动，先整块买入。<bookmark mark='b'/>然后恰好以订单簿恢复的速率交易，"
        "让偏移保持不变。<bookmark mark='c'/>最后再整块买入同样大小：最后一笔交易之后，没有未来让它的冲击再让你付钱。"
        "<bookmark mark='d'/>成本是X的平方除以深度乘以2加rho T。当rho T为10时，每一整块是订单的{100 * cf['block']:.1f}%。",

    'f"On a grid of two hundred dates':
        "在两百个时点的网格上，数值最优解。<bookmark mark='a'/>两端各有一个尖峰，中间是平坦的速率，低于稳定的TWAP速率。"
        "<bookmark mark='b'/>随着网格加细，整块和成本都收敛到公式：在一千个时点上，成本与公式相差{100 * err:.3f}%。",

    "By resilience. <bookmark mark='a'/> With none":
        "按韧性来看。<bookmark mark='a'/>没有韧性时，冲击是永久的：每一整块是订单的一半，而且任何时间表的成本都一样，"
        "这是Huberman和Stanzl的线性永久冲击。随着订单簿恢复得更快，整块缩小，成本按rho T的倒数下降：极限下就是Almgren和Chriss的"
        "暂时性冲击。两个模型，同一个家族。",

    'f"Put Bitcoin\'s displayed resilience into the theorem.':
        "把比特币可见订单簿的韧性代入定理。<bookmark mark='a'/>最优队列以至少每秒{rho:.0f}的速率恢复。<bookmark mark='b'/>在一小时里，"
        "rho T达到数万。<bookmark mark='c'/>整块消失了：只看可见订单簿，就应稳定交易。让整块值得的那种缓慢韧性，存在于潜在订单簿"
        "和传播子的缓慢衰减中。",

    'f"And with Bouchaud\'s power-law propagator':
        "再用Bouchaud的幂律传播子代替指数核。<bookmark mark='a'/>指数核在整块之间保持平坦的速率。<bookmark mark='b'/>幂律则按U形交易："
        "两端有整块，中间速率下凹，因为旧的冲击停留得更久。与TWAP相比，最优时间表在指数核下节省{gain_e:.0f}%的成本，"
        "在幂律下节省{gain_p:.0f}%。",

    'f"How resilient is Bitcoin\'s book?':
        "比特币的订单簿有多大韧性？取两天里的{rs['n']:,}次扫单，即十分之一秒内移动十跳以上的情形。<bookmark mark='a'/>最优队列几乎立刻"
        "被补满：深度降到正常的约{100 * dep[0]:.0f}%，在几百毫秒内恢复。<bookmark mark='b'/>但价格没有回来。扫单之后它继续朝同一方向"
        "漂移，两分钟后达到约{path[-2]:.0f}跳。这里的扫单是消息，而不是订单簿上的凹痕：对大订单重要的韧性在潜在流动性里，"
        "而不在可见的队列里。",

    "Signals. <bookmark mark='a'/> Give the executor":
        "信号。<bookmark mark='a'/>给执行者一个价格漂移的短期预测。<bookmark mark='b'/>Álvaro Cartea和Sebastian Jaimungal，"
        "以及Charles-Albert Lehalle和Eyal Neuman证明，最优速率是经风险调整的时间表再加一个倾斜：在预测的上涨之前交易，"
        "在预测的回撤中等待。<bookmark mark='c'/>而第36部分的不平衡和微观价格正是这样的短期预测。",

    "And other executors.":
        "还有其他执行者。<bookmark mark='a'/>当许多基金朝同一方向交易时，每一家的冲击都是所有人的成本：Pierre Cardaliaguet和Lehalle"
        "用第8部分的工具平均场博弈求解了均衡。<bookmark mark='b'/>Markus Brunnermeier和Lasse Pedersen展示了得知有被迫卖方的交易者"
        "如何先卖后买回：保密是执行的一部分。<bookmark mark='c'/>而公开的、拥挤的订单流，比如指数调整，要为与人群同向交易反复缴税。",

    "Pause and predict. A reinforcement learner trains":
        "暂停并预测。一个强化学习者在本系列公司的订单簿模拟器中训练六万回合，在二十步内卖出二十个单位。它能胜过稳定、朴素的TWAP吗？",

    # ------------------------------------------------------------------ RL
    'f"Chapter seven, and the answer to the pause: no, not here.':
        "第7章，以及暂停问题的答案：在这里不能。六万回合之后，学习者的平均成本是{q:.1f}个半跳，TWAP是{tw:.1f}个。"
        "为什么，以及要怎样才能做得更好，就是本章的内容。",

    "The literature. <bookmark mark='a'/> Yuriy Nevmyvaka":
        "文献。<bookmark mark='a'/>2006年，Yuriy Nevmyvaka、Yi Feng和Michael Kearns把表格型强化学习用在纳斯达克订单簿上，"
        "改进了简单策略。<bookmark mark='b'/>随后出现了深度版本，例如Brian Ning、Franco Lin和Jaimungal的双重深度Q学习，"
        "报告了相对TWAP和Almgren-Chriss的收益。<bookmark mark='c'/>问题在于：学习者只能和它练习的市场一样好。",

    'f"The environment.':
        "环境。<bookmark mark='a'/>市场是第36部分的队列反应订单簿，用5月17日的数据拟合。<bookmark mark='b'/>任务：在{r['steps']}步内"
        "卖出{r['inv']}个单位，剩下的在最后一次性卖出。<bookmark mark='c'/>一次卖出吃掉买方队列；每当一个队列被清空，价格下跌半跳，"
        "订单继续往下吃。这就是冲击。<bookmark mark='d'/>成本是执行差额，以半跳为单位。",

    "The learner. <bookmark mark='a'/> It sees the step":
        "学习者。<bookmark mark='a'/>它看到当前步数、剩余库存，以及分成三组的队列不平衡。<bookmark mark='b'/>每一步它卖出零、一、二或"
        "四个单位。<bookmark mark='c'/>它用第8部分的Q学习来学习，在六万回合中探索越来越少。",

    "Learning. <bookmark mark='a'/> The cost per episode":
        "学习过程。<bookmark mark='a'/>每回合的成本，按每五百回合取平均，从探索到利用。<bookmark mark='b'/>它带着噪声朝TWAP的线下降，"
        "并停在线的上方。奖励的噪声很大：单个回合成本的标准差是三十个半跳，所以学习者是在大量噪声中拟合一个很小的信号。",

    'f"On five thousand fresh episodes.':
        "在五千个新回合上。<bookmark mark='a'/>TWAP的成本是{res['TWAP']['mean']:.1f}个半跳。学习者是{res['Q-learning']['mean']:.1f}，"
        "胜过除TWAP之外的所有手工规则：前置卖出{res['front-loaded']['mean']:.1f}，在买方薄时卖出"
        "{res['sell when the bid is thin']['mean']:.1f}，一次性全部卖出{res['dump at once']['mean']:.1f}。"
        "标准误约为半个半跳，所以与TWAP的差距是真实的。",

    "What it learned.":
        "它学到了什么。<bookmark mark='a'/>它在每一步的平均卖出量，对比TWAP每步稳定的一个单位。它一开始等待，中间卖得不均匀，"
        "把更多留到最后：在一个价格是无漂移随机游走的订单簿里，等待平均来说没有成本，而它对何时卖出的估计仍然有噪声。",

    "Why not. <bookmark mark='a'/> There is little to find":
        "为什么不行。<bookmark mark='a'/>没什么可发现的：在这个订单簿里价格没有漂移，队列在每次移动后都会遗忘，所以最优时间表接近稳定，"
        "TWAP已经接近最优。<bookmark mark='b'/>奖励的噪声很大：单个回合的成本变化远大于好策略之间的差别。<bookmark mark='c'/>在有记忆、"
        "有信号、有韧性的订单簿里，最优解不是简单公式，学习才可能有帮助；但前提是模拟器通过评分卡。评判学习型执行者，首先要对比TWAP。",

    "What would do better.":
        "什么能做得更好。<bookmark mark='a'/>公共随机数：在相同的模拟路径上比较策略，让噪声在差值中抵消。<bookmark mark='b'/>先有结构："
        "学习相对TWAP或Almgren-Chriss的偏离，而不是整个时间表。<bookmark mark='c'/>还要一个会反应的市场，有记忆、扫单和韧性，"
        "对照数据打分，最终检验放在样本外。",

    "Designing a better experiment.":
        "设计一个更好的实验。<bookmark mark='a'/>更丰富的状态：价差、近期不平衡、微观价格的偏离和短期波动率。<bookmark mark='b'/>带风险惩罚的"
        "奖励，让学习者面对Almgren和Chriss的权衡。<bookmark mark='c'/>以及在相同随机路径上与TWAP、同等风险下的Almgren-Chriss，"
        "和一条简单的不平衡规则作比较。",

    'f"Pause and predict. Bitcoin\'s perpetual trades {hi:.1f}':
        "暂停并预测。比特币永续合约在世界协调时下午两点到三点成交一天成交量的{hi:.1f}%，在早上四点到五点成交{lo:.1f}%。"
        "一个VWAP订单要在一天内交易一千个比特币。这两个小时各交易多少？",

    # ------------------------------------------------------------------ Algos
    'f"The answer to the pause. <bookmark mark=\'a\'/> In the busy hour':
        "暂停问题的答案。<bookmark mark='a'/>在繁忙的那个小时，约{a:.0f}个比特币。<bookmark mark='b'/>在安静的那个小时，约{b:.0f}个。"
        "<bookmark mark='c'/>VWAP时间表按市场预期成交量的比例交易，所以订单全天在市场中所占份额相同：这正是决定冲击的量。",

    "Chapter eight. The theory becomes products":
        "第8章。理论变成了产品：每家券商都出售的几种执行算法，它们之下的路由器，以及告诉客户这一切花了多少钱的交易成本分析。",

    "The menu. <bookmark mark='a'/> TWAP":
        "菜单。<bookmark mark='a'/>TWAP：按时间等分，是Bertsimas和Lo给风险中性交易者的答案。<bookmark mark='b'/>VWAP：按一天中各时刻"
        "预期成交量的比例分配，所以它跟踪成交量加权平均价格。<bookmark mark='c'/>POV：按实际成交量的固定份额交易，所以结束时间不确定。"
        "<bookmark mark='d'/>以及IS，执行差额算法：Almgren和Chriss的前置时间表，由紧迫度决定。",

    'f"Bitcoin\'s volume curve':
        "比特币的成交量曲线，来自2023年永续合约的每一分钟。<bookmark mark='a'/>加密市场从不收盘，但它也有一天的节奏：从{j}点开始的"
        "那个小时是低谷，占成交量的{sh[j]:.1f}%；从{k}点开始的那个小时是高峰，占{sh[k]:.1f}%，那时纽约开盘、美国数据公布。"
        "<bookmark mark='b'/>TWAP是那条虚线，每个小时都一样。VWAP跟随柱状图。",

    'f"Two more calendars.':
        "另外两个日历。<bookmark mark='a'/>一周：周末每分钟的成交量约为工作日的{100 * we / wk:.0f}%。<bookmark mark='b'/>所以VWAP算法"
        "的好坏取决于它的成交量预测。<bookmark mark='c'/>还有事件，指数调整、到期日和数据公布，会扭曲曲线；在美国股票中，"
        "仅收盘集合竞价就可能占一天成交量的十分之一。",

    "The square-root law has a striking consequence for participation.":
        "平方根法则对参与率有一个惊人的推论。<bookmark mark='a'/>冲击取决于规模，而不是持续时间。<bookmark mark='b'/>参与率为pi的POV订单，"
        "所需时间由它的规模决定。<bookmark mark='c'/>所以交易得更慢几乎不降低预期冲击；更细致的研究发现它对速率只有微弱的依赖。"
        "<bookmark mark='d'/>但它会增加风险。在平方根下，耐心买到的主要是风险，而不是节省，这就是为什么紧迫度是一个真正的选择。",

    "The close. <bookmark mark='a'/> Stock exchanges":
        "收盘。<bookmark mark='a'/>股票交易所以一场集合竞价结束一天，所有市价收盘单和限价收盘单按同一个价格成交；指数基金在那里调仓。"
        "<bookmark mark='b'/>交易所事先公布竞价的不平衡，流动性提供者针对它交易。<bookmark mark='c'/>加密市场没有收盘：它的基准是"
        "在一个时间窗口内从多个交易场所计算的参考价格，执行者像跟踪短时VWAP一样跟踪它。",

    "Beneath the schedule.":
        "时间表之下。<bookmark mark='a'/>智能订单路由器按显示的数量、手续费、成交概率和被狙击的风险，把每笔子订单分配到各个交易场所。"
        "<bookmark mark='b'/>每笔子订单要么挂单，更便宜但更慢，并且会遭遇第36部分测得的逆向选择；要么跨越价差直接成交。"
        "<bookmark mark='c'/>暗池能隐藏订单，但只有当池中其他用户没在读它时才有帮助。",

    "And in crypto. <bookmark mark='a'/> There is no consolidated quote":
        "再看加密市场。<bookmark mark='a'/>没有合并报价，也没有订单保护规则：比特币在几十个交易所交易，在它们之间路由是交易者自己的问题。"
        "<bookmark mark='b'/>同样的敞口以现货和永续合约两种形式交易，执行者可以在两者之间分配，付出基差和资金费率。"
        "<bookmark mark='c'/>每个交易场所都持有抵押品，这是第39部分要定价的对手方风险。",

    'f"A pre-trade estimate, as an illustration.':
        "一个交易前估计，作为示例。<bookmark mark='a'/>买入1.5亿美元的一只宽基股票基金，它每天成交300亿美元：占一天的千分之五。"
        "<bookmark mark='b'/>日波动率为1.2%，平方根法则给出约{imp:.1f}个基点。<bookmark mark='c'/>加上一半价差和手续费，"
        "总计约{tot:.1f}个基点：几乎全部是冲击。",

    "Transaction-cost analysis.":
        "交易成本分析。<bookmark mark='a'/>从到达价格出发，这是执行者无法操纵的基准。<bookmark mark='b'/>像第1章那样分解每个母订单的差额。"
        "<bookmark mark='c'/>像第36部分那样对成交做事后损益标记。<bookmark mark='d'/>再把实现的成本与交易前估计比较，并对照噪声来评判。"
        "对单笔订单来说，这个噪声巨大，正如Almgren和Chriss的标准差所示：交易成本分析是一个跨许多订单的统计问题。",

    'f"A worked example.':
        "一个完整的例子。在100美元时决定买入十万股。<bookmark mark='a'/>算法在高出五美分的价格开始：延迟成本。<bookmark mark='b'/>九万股"
        "以平均100.30美元成交：执行成本，包括价差、冲击和时机。<bookmark mark='c'/>一万股始终没有成交，价格最终停在100.60美元："
        "机会成本。<bookmark mark='d'/>合计为订单的{bp:.0f}个基点。注意，未成交的那十分之一比延迟花得还多。",

    "And a warning about benchmarks.":
        "关于基准的一个警告。<bookmark mark='a'/>VWAP可以被操纵：大订单本身会推动VWAP，所以跑赢它可能只说明订单很大。"
        "<bookmark mark='b'/>收盘价基准会诱使人在收盘时交易，而订单本身参与决定那个价格。<bookmark mark='c'/>以VWAP考核的券商，"
        "即使客户的阿尔法衰减很快，也会按VWAP交易。基准应当与紧迫度相匹配。",

    "Pause and predict. The House's portfolio desk sends an order":
        "暂停并预测。本系列公司的组合台发来一笔占一天成交量百分之二的订单，其信号的阿尔法在一天内衰减。券商提供VWAP。"
        "执行台应该改要什么？",

    # ------------------------------------------------------------------ House
    "The answer to the pause. <bookmark mark='a'/> An alpha that decays":
        "暂停问题的答案。<bookmark mark='a'/>一天内衰减的阿尔法让等待变得昂贵：延迟是一种机会成本，扮演着Almgren-Chriss中风险的角色。"
        "<bookmark mark='b'/>所以要一个前置的执行差额算法，或者更高的参与率。平方根法则说，额外的冲击不大。<bookmark mark='c'/>"
        "并且对照到达价格来评判，而不是对照VWAP。",

    "Chapter nine. The House's thirty-seventh rule":
        "第9章。本系列公司的第37条规则属于它新开的执行台。每笔订单到达时都带着成本估计和时间表，离开时带着实测成本，与两者对照。",

    "The first sheet. <bookmark mark='a'/> Impact on Bitcoin":
        "第一张汇总表。<bookmark mark='a'/>比特币上随规模呈凹形的冲击。冲击从线性转为平方根的潜在订单簿。以大约保持价格扩散的速率衰减的"
        "传播子。风险远超成本的Almgren-Chriss时间表。Obizhaeva和Wang的整块。还有一个尚未胜过TWAP的学习型执行者。",

    'f"How the desk sizes a trade.':
        "交易台如何确定交易规模。<bookmark mark='a'/>一个预期赚十个基点的信号。<bookmark mark='b'/>只有当平方根冲击更小时，才值得交易。"
        "<bookmark mark='c'/>在比特币永续合约上，按它的日波动率和成交量，这把订单上限定在约{cap_m:.0f}百万美元。再大，信号就是在给市场付钱。",

    "What the desk records, for every order.":
        "交易台为每笔订单记录什么。<bookmark mark='a'/>之前：它占预期成交量的份额、带不确定性的平方根估计、信号的半衰期，以及时间表。"
        "<bookmark mark='b'/>之中：参与率、相对时间表的路径，以及每笔子订单之前的微观价格。<bookmark mark='c'/>之后：相对到达价格的差额及其"
        "分解、事后损益标记，以及实现成本与估计的对比，在许多订单上汇总，直到噪声被平均掉。后面的部分正是用这份记录来衡量容量。",

    'f"The same sizing as a picture.':
        "同样的规模确定，画成图。<bookmark mark='a'/>比特币永续合约上订单的平方根成本对订单规模，从十万美元到十亿美元。"
        "<bookmark mark='b'/>信号的十个基点在约{cap_m:.0f}百万美元处与它相交。点的左边，交易赚钱；右边，是给市场付钱。"
        "本系列公司运行的每个策略都有这样一张图，它的规模远在左边。",

    "Chapter two's latent book.":
        "第2章的潜在订单簿。每一步，密度按离散拉普拉斯算子扩散；订单执行期间，价格处的一个源移除卖单；价格就是密度穿过零的地方。"
        "十行代码，平方根就出来了。",

    "Chapter five's schedule:":
        "第5章的时间表：由双曲余弦得到紧迫度kappa，持仓是双曲正弦，以及差额的期望成本和方差。",

    "Chapters four and six.":
        "第4章和第6章。构造核在每一对时点上的矩阵，对全1向量求解，再按订单规模缩放：离散的弗雷德霍姆条件。"
        "以及对指数核它所收敛到的闭式解，两行。",

    "And Chapter three's fit:":
        "还有第3章的拟合：方向自相关，以及价格变化与过去方向的互相关，解一个托普利茨方程组，再累加。传播子就是一笔成交的冲击还剩下的部分。",

    "And Chapter seven's market order.":
        "还有第7章的市价单。只要还有剩余单位，就吃掉最优买价处的数量，价格比中间价低半跳；队列被清空时，中间价下跌半跳，并重新抽取队列。"
        "冲击，九行代码。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>测量；潜在订单簿；时间表；以及学习环境。<bookmark mark='b'/>还有第37条规则。每笔订单进入市场时，"
        "都要带着来自平方根的交易前成本、与其信号紧迫度相匹配的时间表，以及以到达价格为基准。交易台使用的每个冲击模型都要检验无动态套利。"
        "每个学习型执行者首先要对比TWAP来评判。",

    "The rule against three cases.":
        "用三个案例检验这条规则。<bookmark mark='a'/>一份不计成本的回测：要它在其规模下的平方根成本，以及它吃掉阿尔法时的规模。"
        "<bookmark mark='b'/>一个有免费午餐的冲击模型：问它的核是否正定、凸且递减。如果优化器为了买入而卖出，模型就是错的。"
        "<bookmark mark='c'/>一个跑赢VWAP的券商：要相对到达价格的差额、订单占成交量的份额，以及事后损益标记。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter six stated":
        "写给研究者。第6章陈述了Obizhaeva和Wang的答案：一整块、一个稳定速率、再一整块。本章用变分论证对任意正定核证明它，"
        "精确求解指数情形，并在网格上、跨韧性以及用比特币拟合的传播子来检验它。",

    "The setting. <bookmark mark='a'/> A strategy is any signed measure":
        "设定。<bookmark mark='a'/>策略是交易区间上任何总和等于订单的带符号测度：整块、连续交易、买入和卖出。<bookmark mark='b'/>它的期望成本"
        "是第4章的二重积分。<bookmark mark='c'/>核是连续且严格正定的：每一个非零的交易计划，包括往返交易，都要花钱。",

    "Lemma one, uniqueness.":
        "引理一，唯一性。<bookmark mark='a'/>成本是一个二次型：沿任意方向mu移动，它改变一个线性项和一个二次项。<bookmark mark='b'/>严格正定性"
        "让二次项为正。<bookmark mark='c'/>所以成本在一个凸集上严格凸，两个最小点的中点会更便宜：最多只有一个。",

    "Lemma two, the first-order condition.":
        "引理二，一阶条件。<bookmark mark='a'/>在时刻a多买一个单位，在时刻b少买一个单位：总量不变。<bookmark mark='b'/>在最小点，一阶变化必须"
        "为零，所以函数f，即策略在每个时刻所累积的冲击，在a和b处取相同的值。<bookmark mark='c'/>对每一对a和b都成立：f在整个区间上是"
        "一个常数lambda。反过来，由凸性，任何使f为常数的策略都是最小点。<bookmark mark='d'/>它的成本是二分之一lambda乘X。",

    "Lemma three, the exponential kernel.":
        "引理三，指数核。<bookmark mark='a'/>猜测形状：两端各一整块，中间一个常数速率。<bookmark mark='b'/>把核对它积分：每一整块贡献一个"
        "从其端点衰减的指数，稳定的流量贡献它们的补。<bookmark mark='c'/>当每一整块恰好等于速率乘以恢复时间时，指数项相消，f为常数。",

    "Solve. <bookmark mark='a'/> The order must be filled":
        "求解。<bookmark mark='a'/>订单必须完成：两整块加上速率乘T等于X。<bookmark mark='b'/>整块等于速率除以rho，所以每一整块是X除以"
        "2加rho T。<bookmark mark='c'/>常数冲击是整块的两倍。<bookmark mark='d'/>而成本，即lambda乘X的一半，是X的平方除以2加rho T。",

    "Why the theorem needs measures.":
        "为什么定理需要测度。<bookmark mark='a'/>把策略限制为交易速率，不允许整块。<bookmark mark='b'/>那么成本可以任意接近最优值，"
        "却永远达不到。<bookmark mark='c'/>越来越窄、越来越高的脉冲逼近整块，它们的成本逼近最小值。所以自然的空间是测度，"
        "在那里最小值存在：Almgren和Chriss之所以能只用速率，是因为他们的暂时性冲击对脉冲施加了无穷大的惩罚。",

    "The theorem. <bookmark mark='a'/> For any strictly positive-definite kernel":
        "定理。<bookmark mark='a'/>对任何严格正定核，最优时间表唯一，并由区间上恒定的累积冲击刻画。<bookmark mark='b'/>对指数核，"
        "它就是两整块加稳定速率，成本为X的平方除以深度乘2加rho T。它从不卖出。没有韧性时，成本就是永久成本，对每个时间表都一样；"
        "韧性很快时，成本就是Almgren和Chriss的暂时成本。一个定理把第4、5、6章连在一起。",

    "Why the shape, in words.":
        "用文字解释这个形状。<bookmark mark='a'/>开头一整块，因为订单簿未受扰动：这些单位是订单能买到的最便宜的，它们的冲击有整个时间范围"
        "来愈合。<bookmark mark='b'/>结尾一整块，因为最后一笔交易的冲击不会伤害任何后续交易。<bookmark mark='c'/>中间是常数速率，"
        "因为保持累积冲击不变，让每个时刻同样昂贵。如果某个时刻更便宜，在那时多买就能降低成本：这就是弗雷德霍姆条件。",

    "The two limits connect the models.":
        "两个极限把模型连起来。<bookmark mark='a'/>没有韧性时，冲击是永久的、线性的，时间表无关紧要。<bookmark mark='b'/>韧性很快时，整块消失，"
        "成本就是对Almgren-Chriss暂时性冲击稳定交易的成本。<bookmark mark='c'/>所以他们的eta等于1除以深度乘韧性：暂时性冲击就是一个"
        "愈合很快的薄订单簿。",

    'f"Check one: the grid.':
        "检验一：网格。在rho T为10时，在越来越细的网格上精确求解离散问题。<bookmark mark='a'/>成本收敛到公式的"
        "{o['closed']['cost']:.4f}，第一整块收敛到{o['closed']['block']:.4f}，而且每笔交易都是买入。整块从上方缩向极限，"
        "因为在粗网格上，第一个时点还承担了一部分流量。",

    'f"Check two: what the optimum is worth.':
        "检验二：最优解值多少。指数核下TWAP的成本也有闭式解。<bookmark mark='a'/>当订单簿几乎不恢复时，最优时间表相对TWAP的节省很小，"
        "因为那时冲击几乎是永久的；当它几乎立刻恢复时，节省又很小。在两者之间它达到峰值，当rho T接近{rows[k]['rhoT']:g}时约为{y[k]:.0f}%："
        "时间范围是几个恢复时间那么长。",

    "Beyond the exponential.":
        "超越指数核。<bookmark mark='a'/>取第3章的幂律传播子。<bookmark mark='b'/>定理仍然刻画了最优解，但积分方程没有闭式解，"
        "所以像本系列公司的代码那样在网格上求解。<bookmark mark='c'/>答案保留了整块，并把速率弯成U形，在两端附近最大：Gatheral、Schied"
        "和Slynko发现，对纯幂律，密度甚至会在两端发散。在凸核下它从不卖出。",

    'f"Check three: Bitcoin\'s own kernel.':
        "检验三：比特币自己的核。取第3章的传播子，即在约{b['l0']}笔成交之后指数为{b['beta']:.2f}的幂律，在{b['trades']:,}笔成交内"
        "安排一次买入。<bookmark mark='a'/>最优解以各占{100 * b['block0']:.1f}%的整块开头和结尾，中间按浅U形交易，从不卖出，正如Alfonsi、"
        "Schied和Slynko的定理对凸递减核所保证的。<bookmark mark='b'/>它比TWAP节省{save:.1f}%：冲击如此持久时，时间表的形状关系不大，"
        "订单的规模关系很大。",

    "Where this sits. <bookmark mark='a'/> Gatheral, Schied and Slynko":
        "这项工作的位置。<bookmark mark='a'/>Gatheral、Schied和Slynko给出了一般核的弗雷德霍姆刻画，以及若干核的显式解。"
        "<bookmark mark='b'/>Alfonsi、Antje Fruth和Schied让订单簿可以是任意形状，这使冲击变成非线性，结果两端仍有整块。"
        "<bookmark mark='c'/>而Obizhaeva和Wang的原始论文把韧性解读为新流动性到来的速度。",

    "Three open questions. <bookmark mark='a'/> A model with square-root impact":
        "三个开放问题。<bookmark mark='a'/>一个规模上有平方根冲击、带衰减核、没有动态套利、且最优时间表可计算的模型。"
        "<bookmark mark='b'/>从公开数据中区分冲击里属于信息的部分和属于机制的部分。<bookmark mark='c'/>许多带暂时性冲击和私有信号的基金的均衡，"
        "以及它是否稳定。",

    "Pause and predict. With an exponential kernel":
        "暂停并预测。指数核，rho T为2，订单为1：整块多大，中间速率多少，成本多少？TWAP的成本又是多少？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-seven in thirteen lines.":
        "用十三行回顾第37部分。元订单在执行期间凹形地推动价格，其中约三分之一会回撤。在比特币上，一分钟的价格变动随带方向成交量的增长"
        "慢于比例。平方根法则在各个市场成立，潜在流动性解释了它。传播子的衰减恰好快到能抵消订单方向的记忆。冲击模型必须禁止赚钱机器。",

    "Almgren and Chriss front-load by urgency":
        "Almgren和Chriss按紧迫度前置，他们的风险远超成本，尽管线性冲击低估了成本。Obizhaeva和Wang在两端整块交易。学习型执行者没有胜过TWAP。"
        "券商的算法就是这些时间表，以到达价格来评判。研究者章节证明了暂时性冲击下的最优时间表。",

    "Three lessons. <bookmark mark='a'/> Size first, schedule second":
        "三条教训。<bookmark mark='a'/>先规模，后时间表：在平方根下，交易多少决定了大部分成本，最好的时间表只能节省其中几个百分点。"
        "<bookmark mark='b'/>冲击模型是关于免费午餐的断言；在对它做优化之前先检验它。<bookmark mark='c'/>拿朴素答案来评判学习："
        "在模拟器里胜不过TWAP的学习者，在市场里也胜不过。",

    "The part on one card.":
        "一张卡片上的这一部分。平方根法则。潜在订单簿的三角形。传播子与方向记忆的平衡。暂时性冲击下时间表的成本，对允许的核永不为负。"
        "Almgren和Chriss的双曲正弦。以及Obizhaeva和Wang的整块及其成本。",

    "How this part connects.":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>往回看：第31部分的成本现在有了微观结构，第35部分的Kyle模型是线性、永久的特例。"
        "<bookmark mark='b'/>横向看：第36部分提供了模拟器和信号，第8部分提供了数学。<bookmark mark='c'/>往前看：第38部分的做市商赚的"
        "正是执行者付出的，第41部分的抛售潮是所有人同时发出的元订单。",

    "Six desk questions. Ten percent of volume":
        "六个交易台问题。成交量的百分之十花三十个基点；百分之四十呢？按平方根，是六十个基点。<bookmark mark='a'/>为什么冲击是凹的？"
        "V形的潜在流动性。<bookmark mark='b'/>方向可预测时，为什么价格不可预测？冲击会衰减。",

    "What must an impact model satisfy?":
        "冲击模型必须满足什么？一个正定的核。<bookmark mark='a'/>厌恶风险的卖方怎样交易？前置。<bookmark mark='b'/>订单簿会恢复时呢？"
        "两端整块。完整解答见讲义。",

    'f"The research chapter\'s pause, answered.':
        "研究者章节暂停问题的答案。两端各四分之一整块，中间速率{rate:.1f}，成本{cost:.2f}。TWAP的成本是{twap:.3f}：最优解节省{save:.0f}%。",

    "And twelve problems: the square root":
        "还有十二道习题：平方根；潜在订单簿；传播子的指数；赚钱机器；Almgren和Chriss的紧迫度；TWAP的风险；Obizhaeva和Wang；"
        "一个VWAP小时；参与率；以及对照阿尔法确定规模。然后是两道资格考试题：暂时性冲击下的最优时间表，以及从第一性原理推导Almgren-Chriss。"
        "中英文解答见讲义。",

    "Where this comes back. Part thirty-eight sits":
        "这些内容会在哪里再出现。第38部分坐在另一边，作为执行者与之交易的做市商。第39部分会遇到由一条曲线定价的流动性。"
        "第41部分问当所有人都必须同时卖出时冲击会怎样。第42部分则把执行者放到其他机器之中。",

    "The textbooks this part follows, and the papers it draws on, from Kraus":
        "这一部分所依据的教科书和论文，从Kraus和Stoll的大宗交易到深度强化学习。屏幕上的每个数字，都是本系列公司的代码根据币安公开的"
        "成交记录、最优报价和K线，或者根据模拟算出来的。",

    "The House can now price a trade before making it":
        "本系列公司现在能在交易之前为它定价，安排时间表，并测量它花了多少。<bookmark mark='a'/>下一部分，第38部分：做市、交易所交易基金"
        "与速度竞赛。这一部分每笔订单的另一边，以及它如何谋生。",
}
