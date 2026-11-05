"""Chinese narration for quant36: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 限价订单簿 (limit order book), 最优买价/最优卖价 (best bid/offer),
中间价 (mid), 队列 (queue), 跳 (tick, as a unit), 价格-时间优先 (price-time priority), 挂单/吃单 (make/take), 撤单
(cancel), 订单流不平衡 (order-flow imbalance, OFI), 队列不平衡 (queue imbalance), 加权中间价 (weighted mid), 微观价格
(microprice), 霍克斯过程 (Hawkes process), 分支比 (branching ratio), 签名图 (signature plot), 队列反应模型
(queue-reactive model), 程式化事实 (stylised facts), 零智能模型 (zero intelligence), 成交后损益 (markout), 冰山订单
(iceberg), 只挂单 (post-only), 立即成交或撤销 (IOC), 马尔可夫可加过程 (Markov additive process), 基本矩阵
(fundamental matrix), 调和函数 (harmonic function)."""

TITLE = '量化金融，从零搭建 · 第36部分：限价订单簿'

CHAPTERS = {
    'Hook': '公允价值在哪里？',
    'Book': '1. 订单簿',
    'Queues': '2. 队列与下一跳',
    'Events': '3. 引发事件的事件',
    'OFI': '4. 订单流不平衡',
    'Micro': '5. 微观价格',
    'Deep': '6. 深度学习看订单簿',
    'Gen': '7. 我们自己的订单簿',
    'Trading': '8. 在队列中交易',
    'House': '9. 第36条规则：用价差衡量订单簿',
    'Research': '写给研究者：微观价格定理',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-six. The limit order book":
        "第36部分。限价订单簿：每个电子市场都由挂单排成的队列构成，这些队列又透露了下一个价格的什么信息。",

    "A question asked in trading interviews.":
        "一道交易面试题。<bookmark mark='a'/>最优买价是100美元，有500股；最优卖价是100.01美元，只有100股。公允价值在哪里？"
        "<bookmark mark='b'/>中间价说是100.005美元。但卖方那一小队很可能先被吃光，然后价格上跳一格。"
        "<bookmark mark='c'/>按挂单量加权的中间价和一个队列模型，都把公允价值放在靠近卖价的地方。这一部分在比特币的订单簿上检验谁对。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>队列能预测下一跳：随着买方在两个最优队列中所占份额上升，下一步上涨的概率从"
        "{100 * m['p_up'][0]:.0f}%升到{100 * m['p_up'][-1]:.0f}%。但为大跳价资产设计的Stoikov微观价格，在比特币上偏离中间价"
        "{lean:.0f}跳，而且过了头；一张朴素的平均变动表，却在从未见过的日子上把10秒预测误差降低了{gain:.0f}%。"
        "<bookmark mark='b'/>订单流不平衡推动价格：在10秒尺度上，它解释了中间价变化的{100 * r2:.0f}%。"
        "<bookmark mark='c'/>再看诚实测量下的深度学习：在没见过的日子上，一个神经网络猜对下一秒方向的比例是{100 * net:.0f}%，"
        "一条线性规则是{100 * lin:.0f}%。",

    "Why it matters, even to a slow investor.":
        "为什么这很重要，即便对慢节奏的投资者也是如此。<bookmark mark='a'/>本系列的每一个策略都要通过订单簿交易："
        "按月调仓的因子组合照样在卖价买入、在买价卖出，第31部分算的交易成本，就是订单簿上的价格。"
        "<bookmark mark='b'/>最快的交易台就生活在订单簿里，每天数百万次地赚取或亏掉零点几跳。"
        "<bookmark mark='c'/>它也是模型最快碰到现实的地方：公允价格、预测或模拟器，几天之内就能在数百万个观测上检验。"
        "这让订单簿成为诚实研究的实验室，这一部分就把它当实验室用。",

    "Where this sits. Part thirty-five asked who trades with whom.":
        "这一部分的位置。第35部分问的是谁与谁交易。这一部分打开他们交易所经由的机制：订单簿，以及它的队列、跳价和撤单。"
        "它为本系列公司建立一个订单簿模拟器，第37部分的执行和第38部分的做市都会用到它。",

    "Twenty years of the field.":
        "这个领域的二十年。2004年，Fabrizio Lillo和Doyne Farmer发现订单方向有长记忆；2010年，Rama Cont与合作者为队列建模；"
        "人们还发现，订单的自激到达接近临界。<bookmark mark='a'/>接着是订单流不平衡、队列反应模型，以及Sasha Stoikov的微观价格。"
        "<bookmark mark='b'/>然后是深度学习：DeepLOB、普适特征、订单簿生成模型，以及一个检验这些方法能否推广的基准。",

    "The plan: the book itself":
        "计划如下：订单簿本身，用比特币永续合约来测量；队列与下一跳，先看模型，再看数据；事件的聚集与订单方向的记忆；"
        "订单流不平衡；微观价格的拟合与检验；订单簿的深度模型，以及本系列公司自己的生成式订单簿和它的评分卡；在队列中交易；"
        "最后证明微观价格定理。",

    "In the House, the data desk gains":
        "在本系列公司里，数据台获得了一张100毫秒网格上的最优报价，研究台获得了一个订单簿模拟器：接下来两部分将在这个实验室里交易。",

    # ------------------------------------------------------------------ Book
    "Chapter one. A limit order book is a list":
        "第1章。限价订单簿是一张清单，列出所有人现有的买入和卖出报价，按价格排序。这一幕里的每个交易所都是这样一张清单。"
        "下面是它的规则，以及加密货币中交易最活跃的订单簿的一天。",

    "The rules. <bookmark mark='a'/> A limit order rests":
        "规则。<bookmark mark='a'/>限价单停在某个价格上，直到成交或撤单：挂单者提供流动性。"
        "<bookmark mark='b'/>市价单立即与最优的挂单成交，并支付价差。"
        "<bookmark mark='c'/>优先级：价格最优者先成交；同一价格上，先到先得。所以队列中的位置是一种资产。"
        "<bookmark mark='d'/>还有跳价，即最小的价格步长：在比特币永续合约上是10美分，约为万分之零点零四。",

    "The picture. <bookmark mark='a'/> Offers above":
        "图像。<bookmark mark='a'/>卖单在上，买单在下，每个价格旁边是在那里等待的数量。"
        "<bookmark mark='b'/>最优买价与最优卖价之间的差距就是价差；在流动性好的市场上，它通常是一跳，价格不能再靠近，"
        "所有动作都发生在两个最优队列的大小上。",

    "Four events change the book.":
        "有四种事件改变订单簿。<bookmark mark='a'/>新的限价单排到某个队列的末尾。"
        "<bookmark mark='b'/>挂单被撤销：这是做市商防御过时报价的手段。<bookmark mark='c'/>市价单吃掉最优队列的前端。"
        "<bookmark mark='d'/>当某个最优队列被清空，价格就移动。价格是两个队列赛跑的结果。",

    'f"The data: Binance\'s public stream':
        "数据：币安公开的比特币永续合约最优买卖报价流，2023年5月的四天。<bookmark mark='a'/>超过99%的时间里，价差是一跳。"
        "最优队列里有几个比特币，价值十几万到三十万美元。在工作日，最优报价每秒变化约{d0['updates_per_s']:.0f}次，周末更少。"
        "前两天用来拟合模型，周末用来检验。",

    "One minute of it. <bookmark mark='a'/> The best bid and offer":
        "其中的一分钟。<bookmark mark='a'/>最优买价和卖价相隔10美分，一起移动。"
        "<bookmark mark='b'/>下方是两个最优队列，买方向上画，卖方向下画。注意看：价格穿过某一价位之前，那个队列先被耗向零。"
        "这场赛跑就是这一部分的全部游戏。",

    'f"Activity through a day.':
        "一天中的活跃程度。<bookmark mark='a'/>即使在星期六，订单簿每个小时每秒都更新几十次，在世界协调时{hi_h}点左右达到高峰。"
        "加密市场从不收盘，但它也会稍微睡一会儿。",

    "The vocabulary of orders.":
        "订单的词汇。<bookmark mark='a'/>限价单在自己的价格上等待，提供流动性；市价单立即吃掉最优价格，索取流动性。"
        "<bookmark mark='b'/>只挂单宁可被拒绝也不允许吃单，做市商用它来保护自己的费率；立即成交或撤销的订单能成交多少就成交多少，"
        "不留挂单。<bookmark mark='c'/>冰山订单只显示一部分数量，从隐藏的储备中补充，每补一次就失去一次位置。"
        "止损单在价格穿过某个水平时变成市价单：这是下跌会自我强化的原因之一。",

    'f"Why the tick matters.':
        "为什么跳价重要。<bookmark mark='a'/>当跳价相对于交易者愿意接受的价差、相对于价格的波动都很宽时，价差停在一跳，队列很长，"
        "价格很少移动，每次只动一跳：优先级就是一切。<bookmark mark='b'/>当跳价很小时，价格一次移动许多跳，交易者靠价格竞争。"
        "第35部分讲到的美国半美分跳价，针对的正是第一类市场。<bookmark mark='c'/>比特币永续合约两者兼具：价差是一跳，像第一类；"
        "但在相隔十分之一秒的两个快照之间，中间价一旦变化，跳动的中位数是{mv:.0f}跳，像第二类。Mathieu Rosenbaum和Khalil Dayri"
        "正是用价格的这种行为来衡量跳价大小的，按这个标准，这里的跳价是小的。第5章会说明这为什么重要。",

    "Pause and predict. Five bitcoin are queued ahead":
        "暂停并预测。你新挂了1个比特币的订单，前面排着5个比特币。成交每秒吃掉0.2个比特币，撤单每秒从你前面移走0.1个。"
        "你要多久才能成交？",

    # ------------------------------------------------------------------ Queues
    "Chapter two. With a one-tick spread":
        "第2章。价差为一跳时，两个最优队列中有一个被耗尽，价格就会移动。所以下一步是两个队列之间的赛跑。"
        "Rama Cont和Adrien de Larrard把这场赛跑变成了一个公式。",

    "The race. <bookmark mark='a'/> Two best queues":
        "赛跑。<bookmark mark='a'/>两个最优队列，买方和卖方。<bookmark mark='b'/>每个队列随新订单增长，随撤单和成交缩短；"
        "在Rama Cont、Sasha Stoikov和Rishi Talreja的模型中，这是一个生灭过程；速率平衡时是随机游走，在极限下是布朗运动。"
        "<bookmark mark='c'/>如果卖方先耗尽，价格就上跳一格。",

    "A picture makes it solvable.":
        "一张图让它可解。<bookmark mark='a'/>把两个队列画成象限中的一个点：买方沿着地面，卖方沿着墙壁。"
        "<bookmark mark='b'/>这个点像二维布朗运动一样游走。如果先碰到地面，卖方已耗尽，价格上跳；如果先碰到墙，价格下跳。"
        "<bookmark mark='c'/>每种结果的概率，是这个点能看到的象限边界所占的份额，它只取决于点的角度。",

    "The formula. <bookmark mark='a'/> A Brownian motion in a quadrant":
        "公式。<bookmark mark='a'/>从角度theta出发的象限内布朗运动，从地面离开的概率随角度线性下降："
        "把复平面平方，象限就展开成半平面，那里的答案是经典的。<bookmark mark='b'/>角度由两个队列之比决定。"
        "<bookmark mark='c'/>所以上跳的概率是：1减去π分之2乘以卖方与买方之比的反正切。两者相等时是一半，卖方很短时接近1。",

    "What the model assumes.":
        "这个模型假设了什么。<bookmark mark='a'/>每个最优队列以某个速率获得限价单，又以其他速率因市价单和撤单而失去订单，"
        "全都随机且相互独立。<bookmark mark='b'/>当一个队列被清空，价格移动一跳，两个新队列重新抽取：模型在每次移动时忘掉一切。"
        "<bookmark mark='c'/>由此，Cont和de Larrard推出了两次移动之间的等待时间、方向，以及极限下价格的波动率，所用的只是订单速率"
        "和新队列的大小。请记住这种遗忘：第5章里比特币打破的正是这条假设。",

    'f"Against the data, on the two test days.':
        "用两个检验日的数据来对照。<bookmark mark='a'/>按不平衡程度分组，下一步上涨的概率：从买方极小时的{100 * p[0]:.0f}%，"
        "到卖方极小时的{100 * p[-1]:.0f}%。<bookmark mark='b'/>模型的形状和中心都对，但两端太陡：真实市场比随机游走的赛跑更不确定。"
        "概率等于不平衡这条直线，位于两者之间。",

    "Why the data are flatter.":
        "为什么数据更平缓。<bookmark mark='a'/>队列不是随机游走：一个队列变薄时，做市商会赶来补充，另一些人则从中撤出。"
        "<bookmark mark='b'/>真实队列的一部分是看不见的，即隐藏订单和冰山订单。<bookmark mark='c'/>而卖方之所以短，"
        "可能是因为知道些什么的卖家即将到来：队列并不独立于信息。",

    "The fix. <bookmark mark='a'/> Weibing Huang":
        "修正。<bookmark mark='a'/>黄伟兵（Weibing Huang）、Charles-Albert Lehalle和Mathieu Rosenbaum的队列反应模型，"
        "让每种事件的速率取决于队列当前的大小。<bookmark mark='b'/>这些速率直接从数据中读出：数一数在每个大小上停留单位时间内"
        "发生了多少事件。<bookmark mark='c'/>结果是一个可以模拟的队列马尔可夫链：由数据生成的订单簿，第7章将构建它并为它打分。",

    "Pause and predict. The bid queue holds nine lots":
        "暂停并预测。买方队列有9手，卖方3手。按Cont和de Larrard的公式，上跳的概率是多少？按“概率等于不平衡”的规则呢？",

    # ------------------------------------------------------------------ Events
    "Chapter three. Orders do not arrive like raindrops.":
        "第3章。订单不像雨滴那样到来。它们成串出现，而且买单之后跟着买单，一连几分钟。这里测量两个事实，并看看它们意味着什么。",

    "Part five's Hawkes process, applied to trades.":
        "把第5部分的霍克斯过程用到成交上。<bookmark mark='a'/>每笔成交都提高后续成交的速率，这部分超额随后衰减。"
        "<bookmark mark='b'/>分支比n是每笔成交直接引发的成交笔数。<bookmark mark='c'/>所以平均速率等于外部速率除以1减n，"
        "而所有成交中有n这么大的比例是对先前成交的反应。",

    'f"One hour of Bitcoin\'s trades':
        "比特币一小时的成交，共{h['n']:,}笔。<bookmark mark='a'/>拟合出的分支比是{h['branching']:.2f}：大约三分之二的成交"
        "是对先前成交的反应。<bookmark mark='b'/>似然函数比泊松过程更偏好自激，差距是{dll:,.0f}个对数点。"
        "<bookmark mark='c'/>但第5部分的检验，即用拟合出的强度重新标度时间，仍然不通过：单一的衰减速率无法同时描述毫秒级和分钟级的聚集。",

    "The deeper result. <bookmark mark='a'/> With a kernel":
        "更深的结果。<bookmark mark='a'/>Stephen Hardiman、Nicolas Bercot和Jean-Philippe Bouchaud用一个从微秒跨到小时的核，"
        "在股指期货上估计出接近1的分支比。<bookmark mark='b'/>一个接近临界的市场：几乎每个订单都是对另一个订单的反应，"
        "小冲击可能层层放大。<bookmark mark='c'/>第14部分已经说明，恰恰是这类接近不稳定的霍克斯过程，在极限下产生日度价格的粗糙波动率。"
        "微观结构解释了宏观。",

    "How to read a Hawkes process.":
        "如何读懂霍克斯过程。<bookmark mark='a'/>每个事件都会提高未来事件的速率，这个提升随后衰减。"
        "<bookmark mark='b'/>分支比是一个事件直接触发的事件数的期望。<bookmark mark='c'/>Alan Hawkes和David Oakes把这个过程看成家族树："
        "每个背景事件都有子女、孙辈，依此类推；只有当分支比小于1时，一个家族的平均规模才是有限的。"
        "<bookmark mark='d'/>所以平均速率等于背景速率除以1减分支比。接近1时，几乎每笔成交都是对另一笔成交的反应。",

    'f"The second fact: signs repeat.':
        "第二个事实：方向会重复。<bookmark mark='a'/>成交方向（买或卖）的自相关，对成交笔数的滞后，画在对数坐标上。"
        "<bookmark mark='b'/>一条直线：指数约为{gm:.2f}的幂律。Fabrizio Lillo和Doyne Farmer在2004年于伦敦证券交易所发现了同样的现象："
        "一笔买入会让数百笔之后的另一笔买入更有可能。衰减这么慢，意味着长记忆。",

    "Why signs repeat.":
        "为什么方向会重复。<bookmark mark='a'/>机构把大订单拆成许多小订单，这些子订单方向相同。"
        "<bookmark mark='b'/>如果这些大订单的规模有幂律尾部，方向的自相关就按幂律衰减，指数由尾部决定：这是Lillo、Szabolcs Mike"
        "和Farmer的论证。<bookmark mark='c'/>又是第35部分的谜题：方向可以预测，价格却不能，因为方向在预期之中的成交对价格的冲击更小。"
        "冲击必然依赖于历史。",

    'f"And a third, which surprises.':
        "还有第三个事实，令人意外。<bookmark mark='a'/>签名图：在不同采样间隔下测量的单位时间中间价变化的方差。"
        "对随机游走来说它是平的。对股票价格来说，它通常在短间隔处下降，因为买卖价反弹增加了噪声。"
        "<bookmark mark='b'/>这里它却上升了，从十分之一秒到10秒，升了约{rise:.0f}%。在最短的尺度上，中间价的变化是正相关的。",

    "Why. <bookmark mark='a'/> With a one-tick spread":
        "原因。<bookmark mark='a'/>价差为一跳时，最优卖单被耗尽，价差张开到两跳，中间价上升半跳。"
        "<bookmark mark='b'/>接着一位做市商在缺口内挂出新的买单，中间价再升半跳。<bookmark mark='c'/>所以价格上移一跳，"
        "是中间价同方向的两次半跳。在比特币上还有第二个原因：吃掉多档的扫单成串到来，即本章的自激，所以接连的跳动往往延续。"
        "中间价在最细的尺度上有趋势，成交价却在反弹：你采样哪一个，决定了你看到什么。",

    "Pause and predict. A Hawkes process has a background rate":
        "暂停并预测。一个霍克斯过程的背景速率是每秒2笔成交，分支比是0.68。它的平均速率是多少？如果分支比升到0.95呢？",

    # ------------------------------------------------------------------ OFI
    "Chapter four. Part thirty-five measured the price of trades.":
        "第4章。第35部分测量了成交的价格。但在订单簿事件中，成交只占少数：挂单和撤单同样改变队列。"
        "Rama Cont、Arseniy Kukanov和Sasha Stoikov问：关于队列的哪一个数字最能解释价格变化？",

    "The definition. <bookmark mark='a'/> At the best bid":
        "定义。<bookmark mark='a'/>在最优买价上，计入新增的数量（如果买价上升，则计入整个新队列），减去移走的数量"
        "（如果买价下降，则减去整个旧队列）。<bookmark mark='b'/>最优卖价上同样处理。<bookmark mark='c'/>两者之差在一个区间内求和，"
        "就是订单流不平衡：订单簿顶端的净买入压力，挂单、撤单和成交都计算在内。",

    "Two minutes of it, second by second.":
        "其中的两分钟，逐秒来看。<bookmark mark='a'/>上方是订单流不平衡：绿色是净买入压力，红色是净卖出压力。"
        "<bookmark mark='b'/>下方是中间价的变化。两者一秒接一秒地同步变动，比只看成交要紧密得多。",

    "By hand, three snapshots.":
        "手算三个快照。<bookmark mark='a'/>100美元处买5个比特币，100.10美元处卖4个。<bookmark mark='b'/>然后买方新增2个，"
        "卖方撤掉1个：3个比特币的买入压力，却没有一笔成交。<bookmark mark='c'/>接着卖单被吃掉，价格上升一跳，旧卖价处出现一笔2个的新买单："
        "消失的卖单在卖方一侧计为负3，新买单全额计入，又是5个。<bookmark mark='d'/>8个比特币的净压力，中间价上升10美分。"
        "只看成交会漏掉那次撤单。",

    'f"Regress the mid change on the imbalance':
        "把同一区间内的中间价变化对不平衡做回归。<bookmark mark='a'/>在1秒尺度上，不平衡解释了四分之一到三分之一的方差；"
        "10秒尺度上约{100 * r10:.0f}%；一分钟尺度上约{100 * r60:.0f}%。每一天都是如此，无论工作日还是周末。"
        "第35部分里带方向的成交解释了约五分之一的分钟收益；把挂单和撤单也算进来，大约翻了一倍。",

    'f"And the coefficient\'s size.':
        "再看系数的大小。<bookmark mark='a'/>在每个半小时内做同样的回归，把每个比特币不平衡的冲击，对当时最优队列的深度作图。"
        "<bookmark mark='b'/>在对数坐标上，斜率是{sl:.2f}。Cont、Kukanov和Stoikov的程式化模型恰好预测负1："
        "要让价格移动一跳，不平衡必须清空一个队列，所以冲击等于一跳除以深度。同样的压力下，薄的订单簿走得更远。",

    "Compare Part thirty-five. <bookmark mark='a'/> In the stylised model":
        "和第35部分比较。<bookmark mark='a'/>在程式化模型中，每一个队列量的不平衡大约让中间价移动半跳。"
        "<bookmark mark='b'/>Kyle的lambda只用了成交，响应是凹的。<bookmark mark='c'/>把限价单也算进来，响应接近线性："
        "成交冲击的凹性，很大程度上是成交之后订单簿的回补，而不平衡把这部分也计入了。",

    "Where it goes next. <bookmark mark='a'/> Ke Xu":
        "接下来的方向。<bookmark mark='a'/>Ke Xu、Martin Gould和Sam Howison证明，订单簿更深档位上的同一种不平衡也带有信息，"
        "最优队列薄的时候尤其如此。<bookmark mark='b'/>Petter Kolm、Jeremy Turiel和Nicholas Westray把订单流不平衡而不是原始价格和数量"
        "喂给深度网络，报告了更好的短期预测：输入比架构更重要。<bookmark mark='c'/>还有一个提醒：本章的一切解释的是同一区间内的价格变化。"
        "预测下一个区间，是第6章那个难得多的问题。",

    "Two refinements. <bookmark mark='a'/> Rama Cont, Mihai Cucuringu":
        "两个改进。<bookmark mark='a'/>Rama Cont、Mihai Cucuringu和Chao Zhang用前十档不平衡的第一主成分把它们合并："
        "一个综合数字，比只用最优档解释得更多。<bookmark mark='b'/>跨股票来看：一旦知道某只股票自己的综合不平衡，"
        "其他股票的不平衡对它同一区间的价格变化几乎没有补充，但确实有助于预测接下来的变化。"
        "<bookmark mark='c'/>我们的数据只有最优报价，所以这一部分测量的是最优档版本；更深的版本需要完整的深度数据流。",

    "Pause and predict. The best queues average eight bitcoin":
        "暂停并预测。最优队列平均有8个比特币，跳价是10美分。在10秒内，订单流不平衡是正12个比特币。中间价大约移动多少？",

    # ------------------------------------------------------------------ Micro
    'f"The answer to the pause. <bookmark mark=\'a\'/> Ten cents over twice eight':
        "暂停问题的答案。<bookmark mark='a'/>10美分除以8的两倍，再乘以12：<bookmark mark='b'/>约{100 * move:.1f}美分，"
        "<bookmark mark='c'/>四分之三跳。12个比特币的净买入相当于一个半队列，而程式化模型让中间价每个队列移动半跳。",

    "Chapter five. Back to the interview question":
        "第5章。回到那道面试题：给定两个最优队列，公允价值是多少。2018年，Sasha Stoikov用一个定义、一个定理和一个估计量给出了答案。"
        "我们在比特币订单簿的两天上拟合它，在另外两天上检验它。",

    "Three candidates. <bookmark mark='a'/> The mid ignores":
        "三个候选。<bookmark mark='a'/>中间价完全不看队列。<bookmark mark='b'/>加权中间价偏向队列较小的一侧，也就是可能先被吃掉的一侧："
        "卖单几乎没有时，它几乎就落在卖价上。<bookmark mark='c'/>Stoikov的微观价格是中间价的期望值，不是下一次移动后的，"
        "而是给定当前不平衡和价差、在未来许多次中间价变化之后的期望值。",

    "Why the weighted mid is not the answer.":
        "为什么加权中间价不是答案。<bookmark mark='a'/>卖单几乎没有时，它几乎就落在卖价上。<bookmark mark='b'/>卖单被吃掉，"
        "价格上跳，新的卖价处来了一个新队列，于是不平衡复位，加权中间价又回落到新中间价之下。"
        "<bookmark mark='c'/>它先跳上去，又部分跳回来：它的变化是可预测的，所以它不是鞅。而公允价格必须是鞅，否则就可以对着它交易获利。",

    "The estimator is a Markov chain.":
        "估计量是一个马尔可夫链。<bookmark mark='a'/>状态是不平衡（分成十组）和价差（一跳或两跳）。"
        "<bookmark mark='b'/>在100毫秒网格上，数一数每个状态转到每个其他状态的次数，分为中间价不动和中间价移动两种，并记下移动多少。"
        "<bookmark mark='c'/>对中间价移动之前的各步求和，就得到第一次变化的期望值，以及变化之后的状态。"
        "<bookmark mark='d'/>微观价格的调整项再加上之后每一次移动的期望变化。数据做了镜像处理，即交换买卖双方，所以没有漂移，求和收敛。"
        "研究者章节会证明它确实收敛。",

    'f"The fit, on the two training days':
        "在两个训练日上、价差为一跳时的拟合结果。<bookmark mark='a'/>加权中间价最多偏离半跳：在这个尺度上是一条平线。"
        "<bookmark mark='b'/>Stoikov的微观价格在最极端的组里偏离{abs(g1[-1]):.0f}跳，即两美元半。"
        "<bookmark mark='c'/>同样那几天中间价实际的后续变化：下一秒，极端组里是{abs(e1[-1]):.0f}跳；"
        "<bookmark mark='d'/>下一分钟是{abs(e60[-1]):.0f}跳，在中间各组里远小于微观价格。理论给出的答案，比市场实际兑现的任何东西都大。",

    'f"The test, on two days the fits never saw.':
        "在拟合从未见过的两天上检验。<bookmark mark='a'/>预测1秒、10秒和一分钟之后的中间价，把平方误差和直接用中间价的误差比较。"
        "加权中间价略有帮助，最多百分之一。Stoikov的微观价格在1秒尺度上是一场灾难，比什么都不做最多差{worst:.0f}%，"
        "到一分钟时仍然更差。<bookmark mark='b'/>一张朴素的表，记录训练日上每个状态在每个时间跨度内的平均变动，做到了微观价格承诺的事："
        "在两个检验日上都把10秒误差降低了{e_lo:.0f}%到{e_hi:.0f}%，尽管在1秒尺度上，它在其中一天也略有失手。",

    'f"The same failure, seen as a martingale test':
        "同样的失败，换成检验日上的鞅检验来看。<bookmark mark='a'/>中间价不是鞅：从最极端的组出发，它在下一秒朝不平衡指向的方向漂移"
        "{md:.0f}跳。<bookmark mark='b'/>公允价格根本不该漂移。微观价格却向相反方向漂移：它已经偏得比市场愿意跟随的更远，于是又回来。"
        "过头和不足一样可以预测。",

    'f"Why the theory fails here.':
        "理论为什么在这里失败。<bookmark mark='a'/>比特币永续合约是小跳价市场：2.7万美元上的10美分，约为万分之零点零四。"
        "<bookmark mark='b'/>在相隔十分之一秒的两个快照之间，中间价一旦移动，通常一下跳{mv:.0f}跳：最优队列只是深厚订单簿的薄薄一层。"
        "<bookmark mark='c'/>而且这个状态不是马尔可夫的。一次移动之后，最优档以外的深度、最近的订单流和第3章的记忆都起作用，"
        "所以一个只看不平衡和价差的链，把偏离向前传递得太远。Stoikov是为大跳价股票设计微观价格的，在那里最优队列就是订单簿。"
        "研究者章节会精确检验这条边界。",

    'f"So, the interview, which is about a large-tick stock':
        "那么回到面试题，它说的是一只大跳价股票：100美元的价格，1美分的跳价。<bookmark mark='a'/>买方占了六分之五的股数。"
        "<bookmark mark='b'/>在一个大跳价的订单簿上，也就是第7章本系列公司的模拟器上拟合，这一组的微观价格是{adj:.2f}跳。"
        "<bookmark mark='c'/>公允价值约为100.008美元：高于中间价，略低于加权中间价。偏向卖方，但不要偏到底，因为卖单被吃掉之后，"
        "会来一个新的卖单。对那一类订单簿，这就是答案；比特币的订单簿告诉我们何时该怀疑它。",

    "What it is for. <bookmark mark='a'/> A market maker":
        "它有什么用。<bookmark mark='a'/>以微观价格而不是中间价为中心报价的做市商，被狙击的次数更少：第38部分。"
        "<bookmark mark='b'/>执行者在微观价格快要甩开自己时跨过价差，在它偏向自己时挂限价单：第37部分。"
        "<bookmark mark='c'/>以微观价格为基准来衡量，短期收益和滑点里的买卖价反弹会更少。",

    "Pause and predict. A deep network sees the last ten seconds":
        "暂停并预测。一个深度网络看到订单簿最近10秒的30个数字，一条线性规则也看到同样的30个数字。"
        "在两者都没见过的日子上，谁对下一秒方向的预测更好？",

    # ------------------------------------------------------------------ Deep
    "Chapter six. The order book is a large":
        "第6章。订单簿是一条庞大、有结构、快速到达的数字流：正是深度学习据说擅长的东西。自2017年以来，几十篇论文把它喂给神经网络。"
        "他们发现了什么？我们又发现了什么？",

    "Three results the field builds on.":
        "这个领域赖以建立的三个结果。<bookmark mark='a'/>Zihao Zhang、Stefan Zohren和Stephen Roberts的DeepLOB："
        "在十档价格和数量上做卷积，再接一个循环网络，预测平滑后的中间价是涨、跌还是不变。"
        "<bookmark mark='b'/>Justin Sirignano和Rama Cont用数百只美国股票一起训练一个网络。它胜过逐只股票拟合的模型，"
        "即使在它从没见过的股票上也是如此：价格形成的机制看起来是普适的。<bookmark mark='c'/>输入也很重要："
        "同样的网络，喂订单流不平衡比喂原始档位数据效果更好。",

    "What DeepLOB sees, and how.":
        "DeepLOB看到了什么，又是怎么看的。<bookmark mark='a'/>最近100个订单簿事件，每个事件有买卖双方十档的价格和数量：共四千个数字。"
        "<bookmark mark='b'/>第一层卷积把每一档的价格和数量配对，再把每个买档和卖档配对，然后汇总各档：订单簿的结构被写进了滤波器。"
        "<bookmark mark='c'/>接着是不同宽度的并行滤波器，对应不同的时间尺度，再接一个在窗口内传递记忆的循环层。"
        "<bookmark mark='d'/>输出是跌、平或涨。",

    "What Sirignano and Cont found, in more detail":
        "更详细地看Sirignano和Cont的发现，因为这是最有力的正面结果。<bookmark mark='a'/>普适性：一个适用于所有股票的模型胜过逐只股票的模型，"
        "即使在它从未见过的股票上也是如此。<bookmark mark='b'/>平稳性：用较早年份训练，不重新拟合，在之后几个月里仍保持准确率。"
        "<bookmark mark='c'/>路径依赖：更长的订单簿历史改进了预测。价格形成有记忆，只看当前状态的模型抓不住这一点。"
        "研究者章节会从另一侧碰到同一个事实。",

    "Then the benchmark. <bookmark mark='a'/> Most papers report":
        "然后是基准。<bookmark mark='a'/>大多数论文报告的是同一个公开数据集：2010年五只芬兰股票的十天数据。"
        "<bookmark mark='b'/>Matteo Prata和同事在一个开放框架里重跑了十五个已发表的模型。<bookmark mark='c'/>在模型没有针对其调参的数据上，"
        "每一个都明显变差；大多数都对基准过拟合了。这是第26部分的教训，只不过发生在毫秒尺度上。",

    "The labels matter as much as the network.":
        "标签和网络一样重要。<bookmark mark='a'/>基准的标签把接下来k个中间价的平均值和当前中间价比较：一个平滑过的未来。"
        "<bookmark mark='b'/>一个阈值决定哪些变动算作不变，从而决定了常数猜测能得到多高的准确率。"
        "<bookmark mark='c'/>平滑后的标签比收益更容易预测：接下来几个中间价的平均值有一部分已由最初几个决定，相邻的标签又互相重叠。"
        "更容易不等于可交易。下面我们的检验预测的是朴素的下一次中间价变化。",

    "Our own test, small but honest.":
        "我们自己的检验，规模小，但诚实。<bookmark mark='a'/>每一秒30个数字：10秒的按深度标准化的订单流不平衡、中间价变化和队列不平衡。"
        "<bookmark mark='b'/>目标是接下来1秒或10秒的中间价变化，以跳为单位。两天训练，两天检验。"
        "<bookmark mark='c'/>三个模型：只用当前不平衡；用全部30个数字的线性规则；以及一个两层网络，取三个随机种子的平均，"
        "在训练日的末段上提前停止。",

    'f"The answer to the pause. <bookmark mark=\'a\'/> Over the next second':
        "暂停问题的答案。<bookmark mark='a'/>对下一秒，只用不平衡猜对方向的比例是{100 * i1:.0f}%，线性规则{100 * l1:.0f}%，"
        "网络{100 * n1:.0f}%。<bookmark mark='b'/>对10秒，线性规则{100 * l10:.0f}%，网络{100 * n10:.0f}%。在样本外，"
        "网络在方向上从没赢过。而解释的方差很小：在10秒尺度上最多{100 * r10:.1f}%。",

    'f"How to read that.':
        "如何解读。<bookmark mark='a'/>在{100 * e['zero']:.0f}%的秒里，中间价根本不动。动的时候，线性规则对方向判断得相当好，"
        "即便是五跳以上的跳动，也有{100 * big['acc']:.0f}%的时候猜对；它猜不到的是幅度，所以解释的方差一直很小。"
        "<bookmark mark='b'/>这不是钱。只要预测超过一跳就按其方向交易，每笔交易捕捉到约{t1['gain']:.1f}跳的中间价变化。"
        "价差要花一跳，而几个基点的吃单手续费花得更多：在这里一个基点约等于{per_bp:.0f}跳。况且中间价不是任何人能成交的价格。"
        "<bookmark mark='c'/>最后，检验分数比训练分数还高，{100 * te:.0f}%对{100 * tr:.0f}%，原因是周末更安静，而不是模型变好了。"
        "永远要问两个样本之间什么变了。",

    "Three lessons. <bookmark mark='a'/> Features beat architecture":
        "三条教训。<bookmark mark='a'/>特征胜过架构：不平衡已经包含了网络能找到的大部分东西，在两天的数据上，多出来的容量只是在拟合噪声。"
        "<bookmark mark='b'/>深度模型靠规模取胜：Sirignano和Cont用了数百只股票、许多个月。<bookmark mark='c'/>为交易打分，而不是为标签打分："
        "基准上平滑过的涨、跌、平标签，在按成本、按有人能交易的时间跨度衡量之前，还不是一个策略。",

    "Pause and predict. A simulator reproduces the rates":
        "暂停并预测。一个模拟器准确再现了每种队列大小下挂单、撤单和成交的速率。它的价格会像真实订单簿那样出现波动率聚集吗？",

    # ------------------------------------------------------------------ Gen
    "Chapter seven. The answer to the pause is no":
        "第7章。暂停问题的答案是不会，本章说明原因。预测说的是接下来发生什么；模拟器却必须生成一整天都像真实市场一样运转的数据。"
        "这是难得多的检验，而接下来的两部分需要一个这样的模拟器。",

    "Why build one. <bookmark mark='a'/> Replaying history":
        "为什么要建一个。<bookmark mark='a'/>回放历史是不够的：加入回放的订单永远不会推动价格，永远不排队，也永远不会被狙击。"
        "<bookmark mark='b'/>模拟器让交易台可以检验执行和做市，运行从未发生过的压力情景，并且不冒资金风险地训练第8部分的强化学习者。"
        "<bookmark mark='c'/>危险恰好是它的镜像：在模拟器上调好的算法学到的是模拟器，模拟器每搞错一个事实，就变成一笔并不存在的利润。",

    "Four families. <bookmark mark='a'/> Statistical models":
        "四大类。<bookmark mark='a'/>统计模型，即队列反应模型和霍克斯驱动的订单簿：速率从数据中读出，可解释，速度快。"
        "<bookmark mark='b'/>基于主体的市场，例如ABIDES，其中带有策略的模拟交易者在撮合引擎中相遇。"
        "<bookmark mark='c'/>深度生成订单簿：订单流的条件对抗网络，以及Peer Nagy和同事的生成器，它像语言模型写文字那样逐个词元地写出消息流。"
        "<bookmark mark='d'/>以及如何评判它们：Svitlana Vyetrenko和同事提出，用真实订单簿的一张程式化事实清单为模拟器打分。我们接下来就这样做。",

    "The simplest simulator of all has no traders in it.":
        "最简单的模拟器里根本没有交易者。<bookmark mark='a'/>Eric Smith、Doyne Farmer和同事让订单随机到达、价格随机、撤单也随机。"
        "<bookmark mark='b'/>量纲分析于是由四个速率确定价差，只差一个关于单一数字的函数。<bookmark mark='c'/>在伦敦的股票上，"
        "这个零智能模型预测出了平均价差在不同股票之间差异的大部分。订单簿的机制解释了很多；它们漏掉的，正是策略和信息所在之处。",

    'f"The House\'s simulator is the queue-reactive model':
        "本系列公司的模拟器就是队列反应模型，用5月17日的数据拟合。单位是一个典型订单，{q['unit']:.1f}个比特币。"
        "<bookmark mark='a'/>对最优队列的每一种大小，它每秒增长和缩短的频率。<bookmark mark='b'/>小队列增长得比缩短得快，"
        "大队列缩短得比增长得快：队列被拉向一个典型大小，这正是第2章的随机游走所缺少的反应。队列被清空时，价格移动，"
        "新队列从数据显示的分布中抽取：{100 * p1:.0f}%的时候只有一个单位，中位数是{k_med}。",

    'f"An hour of the simulated mid':
        "模拟中间价的一小时，只来自拟合出的速率。<bookmark mark='a'/>它像价格一样游走，每次半跳，最后离起点{abs(m[-1]):.2f}美元。"
        "看起来挺像。问题是它在要紧的方面像不像。",

    'f"The scorecard.':
        "评分卡。<bookmark mark='a'/>模拟器把队列的大小做对了，约{mo['queue_med']:.0f}个单位。<bookmark mark='b'/>它动得太慢："
        "每分钟{mo['moves_per_min']:.1f}次中间价移动，而在拟合所用的那一天是{tr['moves_per_min']:.0f}次。它的移动只有泊松时钟的"
        "{mo['gap_cv']:.1f}倍那么成串，数据里是{tr['gap_cv']:.1f}倍。它没有同方向的成对移动，自相关是{abs(mo['move_ac1']):.2f}，"
        "数据是{tr['move_ac1']:.2f}。它的10秒变化峰度是{mo['kurt_10s']:.1f}，数据是{tr['kurt_10s']:.0f}：尾部太薄。一个事实对，四个错。",

    "The diagnosis. <bookmark mark='a'/> The rates depend only":
        "诊断。<bookmark mark='a'/>速率只取决于当前队列，所以模型没有记忆：没有第3章的自激和订单方向记忆，于是没有聚集，尾部也薄。"
        "<bookmark mark='b'/>队列每一步只变化一个单位，而在数据里，一笔市价单可以一次吃掉整个队列：所以价格动得太少。"
        "<bookmark mark='c'/>每个修正都对应评分卡上的一行：依赖近期事件的速率、能一次移走许多单位的事件，以及把价差纳入状态。"
        "研究台保留这个模拟器和它的评分卡，作为任何更好的模拟器都必须超越的基线。",

    "Three rules for anyone who builds a market simulator.":
        "给任何构建市场模拟器的人的三条规则。<bookmark mark='a'/>匹配事实，而不只是似然：一个模型可以拟合好每一步，却仍然错过一整天的形状。"
        "<bookmark mark='b'/>检查它会不会反应：算法在其中交易时，模拟价格必须像真实价格那样响应，这是第37部分的主题。"
        "<bookmark mark='c'/>还要做样本外检验，换一天、换一个市场状态。",

    "Pause and predict. You join the back of a five-bitcoin queue":
        "暂停并预测。你排到买方一个5比特币队列的末尾。后来，你的订单成交了。这是好消息吗？",

    # ------------------------------------------------------------------ Trading
    'f"Chapter eight, and the answer to the pause':
        "第8章，以及暂停问题的答案：通常不是。排在队列末尾的挂单，要等它前面的整个队列被吃光才成交，而这往往恰好发生在价格穿过之前。"
        "在比特币订单簿上，这样一次成交之后一秒，中间价平均对订单不利{abs(mk):.0f}跳。",

    "Price-time priority. <bookmark mark='a'/> At one price":
        "价格-时间优先。<bookmark mark='a'/>在同一价格上，订单按到达顺序成交：队列是一条排队的线，线上的位置是一种资产。"
        "<bookmark mark='b'/>Ciamac Moallemi和Kai Yuan为它估值：排在前面的成交更早，成交对象是更小、信息更少的交易，"
        "所以它的价值可以占价差的很大一部分。<bookmark mark='c'/>而成交本身就是消息。这是从另一把椅子上看第35部分的Glosten和Milgrom："
        "打到你订单上的交易者，可能知道些什么。",

    "The experiment. <bookmark mark='a'/> Every thirty seconds":
        "实验。<bookmark mark='a'/>每隔30秒，只要价差是一跳，就让一笔极小的订单加入最优买价或卖价，排在队列末尾，"
        "或者作为思想实验，排在最前面。<bookmark mark='b'/>真实的成交记录从前端吃掉队列，撤单按比例从我们前面的部分扣除。"
        "<bookmark mark='c'/>成交后，我们在1秒、10秒和一分钟之后用中间价给这笔订单标价，以跳为单位，对我们有利为正。"
        "在成交那一刻，它赚到一半的价差：半跳。",

    'f"The result. <bookmark mark=\'a\'/> At the back of the queue':
        "结果。<bookmark mark='a'/>排在队列末尾时，{100 * bk['fill']:.0f}%的订单在一分钟内成交，中位等待{bk['median_s']:.1f}秒。"
        "成交一秒之后，中间价平均对订单不利{abs(bk['markout']['1 s']):.1f}跳，误差约{se:.1f}，并且一直停在那里。"
        "那半跳价差被完全淹没了。<bookmark mark='b'/>排在最前面时，几乎立刻成交，成交后损益只差{abs(fr['markout']['1 s']):.1f}跳。"
        "同样的价格，同样的日子：差别大部分来自在队列中的位置。",

    'f"By the size of the queue, in five groups.':
        "按队列大小分成五组。<bookmark mark='a'/>排在末尾时，队列越长，成交越糟：从短队列的不利{abs(yb[0]):.0f}跳，"
        "到长队列的不利{abs(yb[-1]):.0f}跳，因为只有一次大规模、知情的扫单才能清空长队列。<bookmark mark='b'/>排在最前面时恰好相反。"
        "队列短时成交仍然不好，不利{abs(yf[0]):.0f}跳。但排在长队列最前面时，成交后损益转为正，约{yf[-1]:.0f}跳："
        "身后的队列保护了你，因为小额成交让你成交，大额成交则必须先吃掉队列的其余部分，价格才会移动。",

    'f"Put a price on the place in line.':
        "给队列中的位置定个价。<bookmark mark='a'/>排在末尾，每挂一笔订单，成交概率乘以成交后损益：约亏{abs(vb):.0f}跳。"
        "<bookmark mark='b'/>排在最前面，约{abs(vf):.1f}跳。<bookmark mark='c'/>两者之差约{gap:.0f}跳，就是排在第一的价值："
        "是这笔订单名义上赚到的半跳价差的许多倍。这就是做市商争相排到最前面的原因。",

    'f"Both ways at once.':
        "两头同时吃亏。<bookmark mark='a'/>订单成交了，说明价格从它身上穿过。<bookmark mark='b'/>没有成交，说明价格跑掉了："
        "在那一分钟里，未成交的订单看着中间价朝远离它们的方向移动了{bk['missed']:.0f}跳。你得到的成交，正是你宁愿没有的；"
        "你错过的，正是你想要的。<bookmark mark='c'/>这是Thomas Copeland和Dan Galai的图景：一笔挂着的限价单，是免费写给市场的一份期权。"
        "价差是它的权利金，谁写了它，谁就必须以消息到达的速度为它重新定价。",

    "The race behind the markouts.":
        "成交后损益背后的赛跑。<bookmark mark='a'/>价值一动，站错一边的每一笔挂单都突然被错误定价。"
        "<bookmark mark='b'/>挂单者试图撤单，撤单所需的时间，就是这份免费期权保持敞开的时间。<bookmark mark='c'/>另一个人在同样的几微秒内"
        "试图抢先吃掉它。在连续订单簿里，这场赛跑由速度决定胜负，而正如第35部分所示，预期损失被算进了每一个价差。",

    "So how does any market maker survive?":
        "那么做市商怎么活下来？<bookmark mark='a'/>他们早撤单：微观价格或不平衡一旦转为不利，报价就撤回。我们那笔极小的订单从不撤单，所以被狙击。"
        "<bookmark mark='b'/>他们早排队：在一个价位成为最优之前就加入，以便占住靠前的位置；争夺这个位置，就是第35部分的延迟军备竞赛。"
        "<bookmark mark='c'/>他们还拿报酬：为挂单流动性支付的返佣。做市商的利润是价差加返佣减逆向选择，逐笔成交地衡量。第38部分会建一个。",

    "Pause and predict. A resting bid is filled just as":
        "暂停并预测。一笔挂着的买单成交时，卖方队列刚刚补满，买方队列几乎空了。微观价格会预先警告你吗？它当时偏向哪一边？",

    # ------------------------------------------------------------------ House
    "The answer to the pause. <bookmark mark='a'/> An almost empty bid":
        "暂停问题的答案。<bookmark mark='a'/>几乎空的买方对着满满的卖方，不平衡接近零。<bookmark mark='b'/>微观价格向下偏，偏向买价："
        "在大跳价订单簿上约三分之一跳，在比特币订单簿上更多。<bookmark mark='c'/>它警告过你。以它为中心报价的做市商，"
        "会在成交之前调低或撤掉买单：这是抵御逆向选择的第一道防线。",

    "Chapter nine. The House's thirty-sixth rule":
        "第9章。本系列公司的第36条规则关于订单簿。来自订单簿的每一个信号都小、快而且脆弱，而它的模拟器可能以看起来像利润的方式出错。"
        "所以这条规则规定了每样东西必须证明什么。",

    "The first sheet. <bookmark mark='a'/> A book that sits":
        "第一张汇总表。<bookmark mark='a'/>一个几乎一直停在一跳价差、每秒更新上百次的订单簿。能预测下一跳的队列。互相激发的成交到达，"
        "以及有长记忆的方向。解释了大部分价格变化的订单流不平衡，冲击接近深度的倒数。在小跳价订单簿上过头的微观价格，"
        "以及一张称职的朴素表格。没能胜过线性规则的网络。尾部太薄的模拟器。还有亏钱的挂单成交，排在队列末尾时亏得很厉害。",

    "What this part did not measure":
        "这一部分没有测量什么，免得有人把它引用得超出它的分量。<bookmark mark='a'/>只有最优报价，只有一个交易所，只有一周中的四天："
        "每个数字都是对那个市场的一次测量，而不是自然常数。<bookmark mark='b'/>相隔十分之一秒的快照，而不是每一个事件："
        "一步之内发生的事是近似的。<bookmark mark='c'/>没有手续费，没有延迟，没有隐藏数量。本系列公司每次都把这些局限写在数字旁边。",

    "Chapter four's definition in one expression.":
        "第4章的定义，写成一个表达式。对买方，如果买价上升或不变，计入新数量，如果下降或不变，减去旧数量；卖方是镜像，再相减。"
        "每一项要么是一个完整的队列，要么是零，这就是为什么它不用看见任何一笔订单，就能捕捉到挂单和撤单。",

    "Chapter five's estimator. Invert one minus":
        "第5章的估计量。求1减去无移动矩阵的逆，它对中间价移动之前的各步求和。这给出第一次变化的期望和变化之后的状态。"
        "然后加上之后每一次移动的期望变化，共四百项，并记录最后两百项让答案改变了多少：在我们的拟合上，完全没有改变。",

    "Chapter seven's simulator.":
        "第7章的模拟器。每一步，每个队列按照与其当前大小相应的拟合概率增长或缩短一个单位。一个队列清空时，中间价朝那个方向移动半跳，"
        "两个队列都从数据中重新抽取。评分卡上的失败在代码里一目了然：速率只看当前队列，而且没有任何东西一次移动超过一个单位。",

    "And Chapter eight's replay.":
        "还有第8章的回放。在我们价格上的一笔成交，如果大于我们前面的队列，就让我们成交；任何穿过我们价格的成交也一样。"
        "否则，成交吃掉我们前面的队列，净撤单按比例扣除；如果这个价位从最优档消失，我们就独自排在最前面。",

    "And Chapter five's humble winner.":
        "还有第5章那个不起眼的赢家。对每个价差可用的快照，取它的状态和中间价在该时间跨度内的变化；把数据做镜像，让表格反对称；"
        "再按状态求平均。没有链，没有极限，没有定理：一个诚实的条件均值，按它将被使用的时间跨度来拟合。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>最优报价流和成交记录的两个加载器；各种特征；微观价格；记忆；以及模拟器和成交回放。"
        "<bookmark mark='b'/>还有第36条规则。订单簿信号要在从未见过的日子上打分，对照中间价和线性规则，并以跳为单位对照它必须支付的价差。"
        "模拟器要附带评分卡，只在它通过的地方使用。每一笔挂单成交都要在1秒、10秒和60秒时标记损益。",

    "The rule against three cases.":
        "用三个案例检验这条规则。<bookmark mark='a'/>一篇在基准上准确率85%的论文：要它换一个市场、换一年，要线性基线，要扣除价差后的利润。"
        "<bookmark mark='b'/>一个在模拟器里调好的执行算法：要评分卡，并问价格是否会对算法自己的订单作出反应。"
        "<bookmark mark='c'/>一位为高成交率自豪的做市商：要成交后损益。排在队列末尾时，高成交率衡量的是你被狙击了多少次。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter five used Stoikov's microprice":
        "写给研究者。第5章用了Stoikov的微观价格，看到级数收敛，也看到它在比特币上失败。本章证明它背后的定理：极限何时存在，"
        "等于什么，为什么是鞅。然后在假设成立和不成立的地方分别检验这些假设。",

    "The setting. <bookmark mark='a'/> The state of the top of the book":
        "设定。<bookmark mark='a'/>订单簿顶端的状态只取有限多个值。<bookmark mark='b'/>假设一：状态是马尔可夫链，"
        "中间价的每次变化只取决于它所伴随的那次转移，而与中间价的水平无关。这是一个马尔可夫可加过程。"
        "<bookmark mark='c'/>假设二，对称性：交换买卖双方，动力学映射到自身，每次移动都反向。"
        "<bookmark mark='d'/>假设三：没有状态会永远等待，而且在中间价变化时刻看到的状态是混合的。",

    "Lemma one, the first move.":
        "引理一，第一次移动。<bookmark mark='a'/>令g1(x)为从状态x出发中间价第一次变化的期望。<bookmark mark='b'/>对第一步取条件："
        "要么中间价现在就动，期望变化为R；要么链以概率Q转到另一个状态而中间价不变，然后重新开始。"
        "<bookmark mark='c'/>由假设三，Q的谱半径小于1，所以1减Q可逆：它的逆就是对所有等待步数的求和。",

    "Lemma two, the later moves.":
        "引理二，之后的移动。<bookmark mark='a'/>同样的求和给出第一次变化刚结束时状态的分布：B，等于1减Q的逆乘以T。"
        "它的每一行和为1，所以B是随机矩阵。<bookmark mark='b'/>在每次变化时刻用强马尔可夫性，下一次变化只通过那时的状态依赖于过去。"
        "<bookmark mark='c'/>所以n次变化之后中间价的期望，等于中间价加上级数的前n项。",

    "Lemma three, convergence.":
        "引理三，收敛。<bookmark mark='a'/>由Perron-Frobenius定理，B的幂在每一行都收敛到平稳分布。"
        "<bookmark mark='b'/>由对称性，平稳分布是镜像对称的，第一次移动是反对称的，所以两者正交。没有对称性，每次移动都会加上一个漂移，"
        "级数就会发散。<bookmark mark='c'/>所以各项是B的幂减去它的极限，其谱半径是第二特征值：它们按几何速度衰减。"
        "<bookmark mark='d'/>求和是一个诺伊曼级数，有闭式解：链的基本矩阵作用在第一次移动上。",

    "The theorem. <bookmark mark='a'/> Under the three hypotheses":
        "定理。<bookmark mark='a'/>在三个假设下，无穷多次变化之后中间价的期望存在，等于中间价加上状态的g，即基本矩阵作用在第一次移动上。"
        "<bookmark mark='b'/>而且它在中间价变化的时刻是鞅：它在下一次变化时的期望值，是中间价加上第一次移动再加上B乘g，"
        "而这又等于g，因为g正是第一次移动加上B乘g。最后这个恒等式就是整个证明。",

    "A corollary: uniqueness.":
        "一个推论：唯一性。<bookmark mark='a'/>任何关于状态的调整f，使中间价加f成为鞅，当且仅当f等于第一次移动加上B乘f。"
        "<bookmark mark='b'/>两个解之差是不可约链的调和函数，也就是常数。<bookmark mark='c'/>对称性把这个常数定为零。"
        "所以微观价格是这种形式中唯一的公允价格，加权中间价只是碰巧才可能是。",

    'f"Why symmetry is not a technicality.':
        "为什么对称性不是技术细节。<bookmark mark='a'/>不做镜像来拟合这个链，两个训练日就带有每次中间价移动{a['pi_g1_ticks']:.2f}跳的漂移。"
        "<bookmark mark='b'/>引理三的正交性不再成立，这个漂移每移动一次就加一次，永无止境。<bookmark mark='c'/>10次移动之后，"
        "和是{a['partial'][0]:.1f}跳，100次之后是{a['partial'][1]:.1f}跳，400次之后是{a['partial'][2]:.1f}跳。"
        "没有对称性就没有微观价格，只有一个外推的趋势。",

    'f"Check one: the algebra':
        "检验一：代数，用第5章在比特币上的拟合。<bookmark mark='a'/>B的最大特征值是1，第二特征值是{lam2:.2f}。"
        "对称性让平稳分布与第一次移动正交，精确到机器精度。<bookmark mark='b'/>各项落在斜率为第二特征值对数的直线上，"
        "级数与闭式解吻合到十三位。定理的结论对拟合出的链成立，这是必然的。它们对市场是否成立，是另一个问题。",

    'f"What the second eigenvalue means.':
        "第二特征值意味着什么。<bookmark mark='a'/>它是一次偏离在一次中间价变化之后保留下来的比例。<bookmark mark='b'/>比特币拟合出的链"
        "每次移动保留{l_b:.2f}，半衰期是{h_b:.1f}次移动，所以它把第一次移动的偏离大约加了三遍。<bookmark mark='c'/>在模拟器里，"
        "每次移动后两个队列都重新抽取，偏离立刻被遗忘，微观价格基本上就是第一次移动。<bookmark mark='d'/>所以放大倍数大约是1除以"
        "1减特征值：链所相信的持续性，恰恰是把比特币的微观价格放大的东西。",

    'f"Check two: where the hypotheses hold.':
        "检验二：在假设成立的地方。第7章本系列公司的队列模拟器，是大跳价世界中的一个队列马尔可夫链。在一次长模拟上拟合微观价格，"
        "在另一次上检验。<bookmark mark='a'/>中间价的漂移是可预测的，在极端处一秒内最多{md:.2f}跳。<bookmark mark='b'/>微观价格不漂移："
        "最多{mc:.3f}跳。在这个订单簿里，加权中间价恰好接近微观价格，也几乎是平的。",

    'f"Check three, the theorem\'s limit itself.':
        "检验三，定理的极限本身。时间跨度越来越长，每个状态出发的平均变动应当趋近微观价格。把实现的漂移画成它的一个比例。"
        "<bookmark mark='a'/>在模拟器里，它在10秒左右升到约1，然后稳定在{settle:.2f}附近：略高一点，因为十个不平衡分组只是对两个队列的"
        "粗略概括，所以这个链只是近似马尔可夫。<bookmark mark='b'/>在比特币上，它在{peak:.2f}处达到峰值，然后回落："
        "市场兑现的不到预测偏离的一半，随后又收回一部分。假设一不成立，定理的结论也随之不成立。",

    'f"And a direct test of hypothesis one.':
        "再直接检验假设一。<bookmark mark='a'/>如果状态是马尔可夫的，那么给定中间价变化刚结束时的状态，下一次变化的方向就不能依赖上一次的方向。"
        "<bookmark mark='b'/>所以在每个状态内部，比较上涨之后和下跌之后下一次的方向，再取平均。<bookmark mark='c'/>在模拟器里，差距是"
        "{mk['sim']:.2f}，接近零。在比特币上是{mk['btc']:.2f}：上一次移动的方向带有状态所没有的信息。假设直接被否定，"
        "这正是上一个检验中定理的极限失败的原因。",

    "Where this sits. <bookmark mark='a'/> Marco Avellaneda":
        "这项工作的位置。<bookmark mark='a'/>Marco Avellaneda、Josh Reed和Sasha Stoikov在存在隐藏流动性的情况下，"
        "从两个最优队列推出了上涨的概率：单步版本。<bookmark mark='b'/>Martin Gould和Julius Bonart在纳斯达克股票上检验了队列不平衡，"
        "发现它对大跳价股票很强，对小跳价股票很弱：同一条边界。<bookmark mark='c'/>Stoikov的论文给出了这里证明的定义、估计量和收敛条件。",

    "Three open questions. <bookmark mark='a'/> What is the smallest summary":
        "三个开放问题。<bookmark mark='a'/>小跳价订单簿的最小概括是什么，能让它足够马尔可夫，使微观价格的极限与市场的极限一致？"
        "<bookmark mark='b'/>在自激的订单流下，状态是无穷维的：一个可计算、带误差界的公允价格还不为人知。"
        "<bookmark mark='c'/>一项资产在许多交易场所交易，每个场所都有自己的队列：合并订单簿的公允价格还没有一般理论。",

    "Pause and predict. Two states, bid-heavy and offer-heavy.":
        "暂停并预测。两个状态：买方偏重和卖方偏重。从买方偏重出发，下一次中间价变化以四分之三的概率上涨一跳，否则下跌一跳。"
        "每次变化之后，状态以概率p保持不变。当p是四分之三时，微观价格偏离多少？p趋于1时又会怎样？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-six in thirteen lines.":
        "用十三行回顾第36部分。订单簿是价格上的队列，先到先得。两个最优队列的平衡能预测下一跳，但没有随机游走赛跑说的那么准。"
        "成交激发成交，订单方向有记忆。订单流不平衡解释了每次价格变化的大部分。加权中间价不是公允价格；Stoikov的微观价格在理论上是，"
        "但在比特币的小跳价订单簿上它过了头，而一张朴素的平均变动表做好了它的工作。",

    "Deep models of the book lose much of their benchmark edge":
        "订单簿的深度模型在新数据上失去了大部分基准优势，我们的网络也没胜过线性规则。我们的模拟器匹配了队列，却错过了聚集。"
        "排在队列末尾的挂单成交会被狙击，因为限价单是一份免费的期权。研究者章节证明了微观价格定理，然后找到了它的假设成立的地方。",

    "Three lessons to take from this part.":
        "这一部分的三条教训。<bookmark mark='a'/>检验假设，而不只是证明。微观价格定理是对的，但比特币的订单簿不是它所假设的那种订单簿，"
        "在做出任何预测之前，对马尔可夫性的直接检验就已经说明了这一点。<bookmark mark='b'/>先建基线：只用不平衡、线性规则和朴素表格，"
        "做得和网络与理论一样好。<bookmark mark='c'/>用你付出的单位来衡量：对照价差的跳数，逐笔成交的损益。高准确率、高成交率和收敛的级数，"
        "每一样都可能一文不值。",

    "Six desk questions. What is order-flow imbalance?":
        "六个交易台问题。什么是订单流不平衡？最优队列在各种事件下的净变化。<bookmark mark='a'/>为什么队列不平衡能预测下一跳？"
        "短的队列先被清空。<bookmark mark='b'/>什么是微观价格，什么时候可以信任它？在大跳价订单簿上，并且要先检验。",

    "Why is the weighted mid not a fair price?":
        "为什么加权中间价不是公允价格？它的变化可以预测。<bookmark mark='a'/>为什么排在队列末尾的成交是坏消息？它恰好在价格穿过之前到来。"
        "<bookmark mark='b'/>你会怎样为一个模拟器打分？用程式化事实，在样本外，并看它对你自己的订单如何反应。完整解答见讲义。",

    'f"The remaining pause questions, answered.':
        "其余暂停问题的答案。前面的5个比特币以每秒0.3个的速度减少：{t_front:.1f}秒到最前面，{t_fill:.1f}秒后成交。"
        "<bookmark mark='a'/>队列为9和3时，Cont和de Larrard给出{p_cdl:.2f}，不平衡规则给出四分之三，数据更接近后者。"
        "<bookmark mark='b'/>这个霍克斯过程平均每秒{mean1:.2f}笔成交；分支比为0.95时是{mean2:.0f}笔，几乎全部由其他成交触发。"
        "<bookmark mark='c'/>两状态的微观价格在p为四分之三时偏离{lean:.0f}跳，p趋于1时没有上界：移动之后的持续性正是放大偏离的东西，"
        "也正是比特币的链高估的东西。",

    "And twelve problems: time in the queue":
        "还有十二道习题：在队列中的时间；上跳概率；霍克斯速率；方向记忆；订单流不平衡的冲击；面试题里的订单簿；如何诚实地报告一个网络；"
        "没有记忆的模拟器；排在队列末尾的订单的盈亏；以及按微观价格撤单的做市商。然后是两道资格考试题：完整的微观价格定理，"
        "以及两状态订单簿。中英文解答见讲义。",

    "Where this comes back. Part thirty-seven measures":
        "这些内容会在哪里再出现。第37部分测量大订单的冲击并为它们安排时间表。第38部分用微观价格、存货和队列位置来做市。"
        "第39部分会遇到一个根本没有队列的订单簿：自动做市商。第42部分则把学习型主体放进像这样的模拟市场。",

    "The textbooks this part follows":
        "这一部分所依据的教科书，首先是Bouchaud和合著者的《Trades, Quotes and Prices》，以及它引用的论文，从Lillo和Farmer"
        "到重新检验深度模型的基准。屏幕上的每个数字，都是本系列公司的代码根据币安公开的最优报价流和成交记录，或者本系列公司自己的模拟器算出来的。",

    "The House can now read the book":
        "本系列公司现在能读懂订单簿了：它的队列、它的订单流、在存在时的公允价格，以及排队等待的代价。"
        "<bookmark mark='a'/>下一部分，第37部分：市场冲击与执行。一笔大订单会让价格移动多少，为什么成本按平方根增长，"
        "以及如何安排一笔交易使它的成本最低。",
}
