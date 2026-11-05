"""Chinese narration for quant35: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 市场微观结构 (market microstructure), 交易商/做市商 (dealer),
存货 (inventory), 报价偏移 (quote shading), 逆向选择 (adverse selection), 知情交易者 (informed trader), 噪声交易者 (noise
trader), 价格冲击 (price impact), 订单流 (order flow), 主动买入 (taker buy), 有效价差 (effective spread), 已实现价差
(realised spread), 知情交易概率 (PIN), 成交量同步知情交易概率 (VPIN), 批量成交量分类 (bulk volume classification),
价格发现 (price discovery), 信息份额 (information share), 永续合约 (perpetual future), 资金费率 (funding rate), 全国最佳
买卖报价 (NBBO), 做市-吃单收费 (maker-taker), 暗池 (dark pool), 批发商 (wholesaler), 频繁批量拍卖 (frequent batch
auctions), 狙击 (sniping), 布朗桥 (Brownian bridge)."""

TITLE = '量化金融，从零搭建 · 第35部分：谁与谁交易'

CHAPTERS = {
    'Hook': '内幕交易者的订单透露了什么',
    'Dealer': '1. 交易商的问题',
    'GM': '2. Glosten与Milgrom：价差是一份保险',
    'Kyle': '3. Kyle：内幕交易者如何交易，代价是什么',
    'Measures': '4. 只用价格衡量价差',
    'Flow': '5. 测量Kyle的lambda',
    'VPIN': '6. 有毒订单流：PIN与VPIN',
    'Discovery': '7. 跨市场的价格发现',
    'Structure': '8. 市场结构：管道系统',
    'HFT': '9. 作为做市商的高频交易者',
    'Crashes': '10. 当流动性消失时',
    'House': '11. 第35条规则：知道对手是谁',
    'Research': '写给研究者：连续时间的Kyle模型',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-five. Who trades with whom":
        "第35部分。谁与谁交易：交易商、知情者和其他人，以及他们的订单透露了什么。第六幕开始：市场微观结构。",

    "One trader knows what the asset is worth.":
        "有一位交易者知道这项资产值多少。<bookmark mark='a'/>其他所有人只看得到价格和订单。"
        "<bookmark mark='b'/>内幕交易者缓慢地买入，藏身于一无所知的交易者之中，价格在噪声中漂移，到收盘时恰好到达内幕交易者所知道的价值。"
        "这一部分讲的是信息如何进入价格，谁为把它放进去付钱，以及其他所有人为交易付出什么代价。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>在比特币上，每一百万美元的净主动买入在一分钟内使价格移动{lam:.1f}个基点，而且反应是凹的。"
        "<bookmark mark='b'/>基于日度价格的经典流动性指标，在今天流动性很好的市场上严重失效：Roll价差给出SPY为{spy:.0f}个基点，而真实值只有三分之一个基点；"
        "一个著名的毒性指标追踪的是波动率，而不是订单真实的不平衡。<bookmark mark='c'/>还有一个精确的定理：连续交易的内幕交易者赚的是只交易一次者的两倍，而价格最终恰好停在价值上。",

    "Where this sits. Act five built strategies":
        "这一部分在系列中的位置。第五幕构建了策略和公司。第六幕深入交易本身：这一部分讲谁与谁交易；然后是限价订单簿、执行、做市和数字资产市场。"
        "它用到第4部分的鞅、第7部分的滤波、第8部分的控制，以及第31部分的冲击。",

    "Fifty years of the field.":
        "这个领域的五十年。Mark Garman在1976年为它命名；然后是Ho和Stoll、Roll，1985年的Kyle以及Glosten和Milgrom，1992年Back的连续时间证明。"
        "<bookmark mark='a'/>然后是测量：Hasbrouck的价格发现、PIN、Amihud的非流动性，以及构建了今天碎片化美国市场的那些规则。"
        "<bookmark mark='b'/>还有电子化时代：闪电崩盘、VPIN、批量拍卖，以及T+1结算。",

    "The plan: the dealer's inventory problem":
        "本部分的安排：交易商的存货问题；Glosten和Milgrom的价差；Kyle的内幕交易者；从价格衡量流动性；在比特币上测量Kyle的lambda；有毒订单流；"
        "现货与期货之间的价格发现；美国市场的管道系统；高频做市商；闪电崩盘与批量拍卖；以及连续时间的Kyle模型，给出证明。",

    "In the House, this part gives the compliance desk":
        "在本系列公司里，这一部分为合规部门提供监控工具，为数据部门提供带方向的订单流：这是之后执行部门和做市部门的原材料。",

    # ------------------------------------------------------------------ Dealer
    "Chapter one. Every trade has two sides":
        "第一章。每笔交易都有两方，在大多数市场上其中一方是交易商：整天向任何人报出买价和卖价的人。1976年，Mark Garman提出交易商要生存必须做什么，并由此给这个领域起了名字：市场微观结构。",

    "Garman's model.":
        "Garman的模型。<bookmark mark='a'/>买单随机到达，卖价越高到得越少。<bookmark mark='b'/>卖单在买价越低时到得越少。"
        "<bookmark mark='c'/>即使两个速率平均来看相等，交易商的存货，即卖出者减去买入者，也是一个随机游走：它会无限漂移，资本固定的交易商终将破产。"
        "报价不能只赚取价差，还必须引导存货。",

    "Thomas Ho and Hans Stoll's answer.":
        "Thomas Ho和Hans Stoll的答案。<bookmark mark='a'/>让两个报价都随存货反向偏移：报价的中点等于公允价值减去一个常数乘以交易商的持仓。"
        "<bookmark mark='b'/>围绕中点的价差是服务的报酬。<bookmark mark='c'/>持有多头的交易商把两个报价都调低：它的卖价更吸引人，买价则更不吸引人，所以接下来的交易会把存货卖回去。"
        "第11部分的Avellaneda和Stoikov模型是同一个思想，经过了优化。",

    "Simulated, twenty thousand arrivals.":
        "模拟，两万次到达。<bookmark mark='a'/>不做偏移时，存货漂移到数百个单位。<bookmark mark='b'/>做偏移时，它保持在零附近几个单位以内，因为每一笔增加存货的交易都让下一笔不太可能发生。",

    "Part eleven made this optimal.":
        "第11部分把它做到了最优。<bookmark mark='a'/>在Marco Avellaneda和Sasha Stoikov的模型里，交易商的保留价格等于价值减去存货乘以风险厌恶再乘以它还需承担的方差。"
        "<bookmark mark='b'/>最优总价差有两部分：存货风险，以及由报价远离时客户停止交易的速度决定的部分。"
        "<bookmark mark='c'/>更高的波动率、更长的剩余时间或更强的风险厌恶：更多的偏移和更宽的报价。Ho和Stoll的两个效应，被精确化了。",

    'f"The trade-off, measured.':
        "权衡，测出来看。<bookmark mark='a'/>偏移会放弃一些价差，因为交易商有时为了出货而报出对自己不利的价格：平均利润下降。"
        "<bookmark mark='b'/>但风险下降得多得多：利润均值与各次运行间离散度之比从{ra:.1f}升到{rb:.0f}。交易商靠价差赚钱，靠偏移生存。",

    "Who the dealers are today.":
        "今天的交易商是谁。<bookmark mark='a'/>纽约证券交易所曾经给每只股票指定一位专营商，负有维持市场有序的义务；今天的指定做市商有报价义务，也在拍卖中享有特权。"
        "<bookmark mark='b'/>大多数债券和外汇仍然通过询价与交易商交易，交易商的资产负债表就是市场的存货。"
        "<bookmark mark='c'/>其余地方，算法为数以千计的品种报价，用存货限额代替了专营商的资本：第九章的主题。",

    "So a spread has three parts.":
        "所以价差有三个部分。<bookmark mark='a'/>订单处理：在场的成本。<bookmark mark='b'/>存货：持有客户卖出之物的风险，由随波动率和头寸扩大的价差来支付。"
        "<bookmark mark='c'/>以及逆向选择：有些客户比交易商知道得多。这一部分即使在竞争性的、风险中性的交易商之间也会保留下来，它是接下来两章的主题。",

    "Pause and predict. A dealer holding forty units":
        "暂停并预测。一位持有四十个单位的交易商，每单位把中点偏移百分之五。价差为一时，它的报价相对于公允价值在哪里？",

    # ------------------------------------------------------------------ GM
    "Chapter two. Suppose dealers are competitive":
        "第二章。假设交易商是竞争性的，平均什么也赚不到，并且不在乎风险，所以存货没有成本。还会有价差吗？1985年，Lawrence Glosten和Paul Milgrom表明一定会有，第11部分运行过他们的市场。这里给出推导。",

    "The model. <bookmark mark='a'/> An asset is worth one or nothing":
        "模型。<bookmark mark='a'/>一项资产值一或零；市场认为它值一的概率是p。<bookmark mark='b'/>比例为mu的交易者知道价值并据此交易。"
        "<bookmark mark='c'/>其余的人出于自己的原因随机买卖。<bookmark mark='d'/>交易商是竞争性的、风险中性的：它预期每笔交易都赚不到钱。",

    "The quotes. <bookmark mark='a'/> To make nothing on a buy":
        "报价。<bookmark mark='a'/>要在一笔买入上不赚不亏，卖价必须等于在有人选择买入这一条件下的期望价值。交易本身就是信息。"
        "<bookmark mark='b'/>由贝叶斯法则，价值高时买入更可能发生，因为那时知情者会买。"
        "<bookmark mark='c'/>从对半的先验出发，卖价是一加mu再除以二，买价是一减mu再除以二，价差恰好是mu：知情交易者的比例。不知情者支付价差；交易商把它转交给知情者。",

    'f"With numbers.':
        "用数字。<bookmark mark='a'/>十个交易者里有三个知情，先验对半：买价零点三五，卖价零点六五。"
        "<bookmark mark='b'/>一旦信念移到零点八，报价上升，价差收窄到{a2 - b2:.2f}。<bookmark mark='c'/>当市场变得确定时，价差消失：知情者再也没有可知道的东西了。",

    'f"Four hundred runs of the market':
        "这个市场运行四百次，每次价值都是一。<bookmark mark='a'/>价差从mu开始，随着交易揭示价值而收窄。知情交易者越多，价差开始越宽、收得越快："
        "十个里有三个知情时，在中位数那次运行中，大约{t3:.0f}笔交易后信念超过百分之九十九。知情交易让市场变贵，也让价格变准。",

    "The price itself.":
        "价格本身。<bookmark mark='a'/>一次运行：每笔买入把它推高，每笔卖出把它拉低，幅度随市场越来越确定而缩小。"
        "<bookmark mark='b'/>平均而言它爬升到价值。价格在交易商的信息下是一个鞅，即第4部分的公平游戏，而它之所以收敛到真值，是因为有些交易者知道真值。",

    'f"How fast does the market learn?':
        "市场学得多快？<bookmark mark='a'/>用赔率来写，贝叶斯法则是乘法：每一笔买入把价值高的赔率乘以一加mu除以一减mu，每一笔卖出则除以它。"
        "<bookmark mark='b'/>所以信念只取决于买入减卖出的次数，达到百分之九十九需要固定数量的净买入。"
        "<bookmark mark='c'/>十个里有三个知情时，约需{n_net:.0f}次净买入；而净买入以每笔交易mu的速度累积，所以约{n_net / mu:.0f}笔交易，接近模拟的中位数{t3:.0f}。",

    "The model's predictions, as studies have found them.":
        "模型的预测，以及研究如何发现它们。<bookmark mark='a'/>在预定消息发布之前，价差变宽、深度变薄，因为此时可能知道更多的交易者比例最高。"
        "<bookmark mark='b'/>消息一旦公开，即使波动率很高，价差也会收窄，这个检验能把信息和存货区分开。"
        "<bookmark mark='c'/>而小而冷门的股票，分析师更少、私人信息的空间更大，在同样的成交量下价差更宽。",

    "The lessons. <bookmark mark='a'/> The spread is not the dealer's profit":
        "教训。<bookmark mark='a'/>价差不是交易商的利润：竞争性的交易商从不知情者那里收取价差，又把它输给知情者。"
        "<bookmark mark='b'/>不知情者为价格发现付钱。<bookmark mark='c'/>如果知情者足够多，价差就会超过任何其他人愿意支付的水平，交易就会停止：George Akerlof的柠檬市场，体现在一个报价上。",

    "Pause and predict. With four in ten traders informed":
        "暂停并预测。十个交易者里有四个知情，先验对半，第一笔交易是买入。下一组买价和卖价是多少？",

    # ------------------------------------------------------------------ Kyle
    "Chapter three. Glosten and Milgrom fixed the trade size":
        "第三章。Glosten和Milgrom把交易规模固定为一。1985年，Albert Kyle让知情交易者自己选择交易多少，并且知道更大的订单会把价格推得更远。"
        "答案给出了这个领域最常用的数字：lambda，订单流的价格冲击。",

    "The model. <bookmark mark='a'/> An asset worth v":
        "模型。<bookmark mark='a'/>一项价值为v的资产，服从正态分布；只有内幕交易者知道v。<bookmark mark='b'/>内幕交易者提交订单x；噪声交易者提交u，与一切独立。"
        "<bookmark mark='c'/>竞争性的做市商只看得到总量y，并把价格定在它能盈亏平衡的水平：给定订单流的期望价值。内幕交易者藏身于噪声之中。",

    "Guess that both sides are linear.":
        "猜测双方都是线性的。<bookmark mark='a'/>内幕交易者按错误定价的比例交易，强度为beta。<bookmark mark='b'/>做市商按订单流的比例移动价格，冲击为lambda。"
        "<bookmark mark='c'/>给定beta，盈亏平衡的lambda是一个回归系数：价值与订单流的协方差除以订单流的方差。",

    "The insider's side.":
        "内幕交易者这一边。<bookmark mark='a'/>给定lambda，它的期望利润是错误定价乘以订单，减去lambda乘以订单的平方：一条向下开口的抛物线。"
        "<bookmark mark='b'/>它的顶点是错误定价除以二倍lambda。<bookmark mark='c'/>内幕交易者只以它能交易的一半力度交易，因为每多一个单位都会把价格推向对自己不利的方向。",

    "Put the two together.":
        "把两者放在一起。<bookmark mark='a'/>beta等于sigma u除以sigma v，lambda等于sigma v除以二倍sigma u。内幕交易者按噪声来调整订单：它总是恰好交易伪装所允许的那么多。"
        "价格冲击随着有待知道的东西增加，随着掩护它的噪声增加而减小。<bookmark mark='b'/>内幕交易者期望赚到sigma u乘sigma v的一半，而价格揭示了价值方差的一半。",

    "Checked by simulation. <bookmark mark='a'/> The insider's profit":
        "用模拟检验。<bookmark mark='a'/>内幕交易者的利润、噪声交易者的损失以及剩余的不确定性，都与定理吻合。而前两个是同一个数："
        "做市商盈亏平衡，所以内幕交易者赚到的，就是噪声交易者亏掉的。这就是为内幕交易者买单的人。",

    "And the insider cannot do better.":
        "而内幕交易者无法做得更好。<bookmark mark='a'/>面对同样的价格冲击，交易一半或一点五倍都赚得更少，正落在定理预测的那条抛物线上。均衡意味着双方都不想改变，这里双方确实都不想。",

    'f"Kyle also let the insider trade over many auctions.':
        "Kyle还让内幕交易者在多次拍卖中交易。<bookmark mark='a'/>算出递推：只有一次拍卖时，结束时还剩一半不确定性。"
        "有四次、十六次、二百五十六次时，内幕交易者把交易分散开，剩余的不确定性沿一条直线下降，在结束时降到零。"
        "<bookmark mark='b'/>价格冲击从一次拍卖时的{l1:.2f}升到二百五十六次时的{l256:.2f}：趋向sigma v除以sigma u。研究章节证明这个极限。",

    "Kyle also named the three dimensions of liquidity":
        "Kyle还命名了流动性的三个维度，这一幕其余部分都在测量它们。<bookmark mark='a'/>紧度：快速转手一个头寸的成本，即价差。"
        "<bookmark mark='b'/>深度：使价格移动一个单位所需的订单流，即lambda的倒数。<bookmark mark='c'/>还有弹性：价格从一次不带信息的冲击中恢复得多快。"
        "真实市场三者兼有；第36部分的订单簿分别测量它们。",

    "The two models side by side.":
        "两个模型并排比较。<bookmark mark='a'/>Glosten和Milgrom固定交易规模，让做市商看到每笔交易的方向；流动性的代价是价差；知情者很多、机械地交易。"
        "Kyle让一个有策略的内幕交易者选择规模，只让做市商看到净订单流，用冲击给流动性定价。在两者中，价格都是一个从交易中学习价值的鞅。研究章节表明它们在极限下相遇。",

    "Who are Kyle's insiders?":
        "Kyle的内幕交易者是谁？<bookmark mark='a'/>利用重大非公开信息交易是违法的；Kyle的内幕交易者是任何合法地拥有更好信息的人：更好的模型或更快的分析。"
        "<bookmark mark='b'/>Pierre Collin-Dufresne和Vyacheslav Fos研究了之后必须披露持股的维权投资者，发现他们在噪声多时交易最多，而标准流动性指标几乎察觉不到他们。"
        "<bookmark mark='c'/>有策略的内幕交易者会刻意隐藏，所以一个安静的市场并不能证明没人知道什么。",

    "What Kyle gives a practitioner.":
        "Kyle给从业者的东西。<bookmark mark='a'/>lambda是可测量的：把价格变化对带方向的订单流做回归，就像第五章在比特币上做的那样。"
        "<bookmark mark='b'/>深度就是噪声：当有大量不知情的订单流可以藏身时，市场就深。"
        "<bookmark mark='c'/>知情交易是渐进的：能够跨时间交易的内幕交易者会缓慢而稳定地交易，这也正是第37部分最优执行的形状。",

    "Pause and predict. Noise trading doubles.":
        "暂停并预测。噪声交易翻倍。lambda、内幕交易者的订单及其期望利润会怎样？",

    # ------------------------------------------------------------------ Measures
    "Chapter four. Most historical data has no quotes":
        "第四章。大多数历史数据没有报价，只有价格和成交量。微观结构从这些数据中构建流动性估计量。这里有三个，在真值已知的地方检验它们。",

    "Richard Roll's estimator":
        "Richard Roll的估计量，第33部分把它当作一个警告。<bookmark mark='a'/>成交落在有效价格附近的买价或卖价上。"
        "<bookmark mark='b'/>这种反弹使相邻的价格变化负相关，幅度是价差平方的四分之一。"
        "<bookmark mark='c'/>所以价差等于两倍的负自协方差的平方根：只用价格得到的价差。",

    "What the estimator sees.":
        "估计量看到的是什么。<bookmark mark='a'/>有效价格在游走。<bookmark mark='b'/>成交随机地落在它上方或下方半个价差处，所以打印出来的价格呈锯齿状：上去又下来，比随机游走更频繁。这种锯齿就是价差。",

    "How hopeless is it?":
        "这有多绝望？<bookmark mark='a'/>信号是价差平方的四分之一。样本自协方差的噪声约为日方差除以样本长度的平方根。"
        "<bookmark mark='b'/>所以要在两个标准误上看到价差，需要这么长的样本。"
        "<bookmark mark='c'/>对SPY，日波动率百分之一点二、价差三分之一个基点：大约一万亿天，数十亿年。当价差占日变动相当比例时Roll估计量才有效，就像1980年代的许多股票，以及今天小而缺乏流动性的证券。",

    "Two more. <bookmark mark='a'/> Shane Corwin and Paul Schultz":
        "另外两个。<bookmark mark='a'/>Shane Corwin和Paul Schultz从每日最高价和最低价读出价差：最高价通常是在卖价上的买入，最低价通常是在买价上的卖出，"
        "而区间有一个随时间增长的波动率部分和一个不随时间增长的价差部分。<bookmark mark='b'/>Yakov Amihud的非流动性：每交易一美元的价格变动，Kyle的lambda的日度版本。"
        "<bookmark mark='c'/>以及用来检验它们的真值：美国交易最活跃的基金报价宽度是一美分，只是一个基点的一小部分。",

    'f"Ten American funds':
        "十只美国基金，从交易最多的到最少的，2015年到2020年。<bookmark mark='a'/>Roll估计量给出世界上流动性最好的基金SPY的价差为{spy['roll_bp']:.0f}个基点；"
        "它的报价价差约为三分之一个基点。对其中两只基金它根本给不出答案。<bookmark mark='b'/>Corwin和Schultz好一些，但仍然给出{spy['cs_bp']:.0f}。"
        "<bookmark mark='c'/>相比之下，Amihud的指标几乎恰好按交易量对这些基金排序。",

    "Why they fail here.":
        "它们在这里为什么失效。<bookmark mark='a'/>对一只每天波动百分之一的基金，一美分的反弹淹没在噪声里；Roll公式实际测到的是任何日度均值回归。"
        "<bookmark mark='b'/>最高-最低区间主要是波动率，所以它的模型中的小误差就会淹没价差。"
        "<bookmark mark='c'/>而在比特币的分钟数据上，最小价位只有千分之几个基点，自协方差为正，Roll根本给不出答案。这些估计量是为1980年代的宽价差设计的，对流动性较差的资产仍然有效；对今天流动性最好的市场，请用报价。",

    'f"Amihud\'s measure against volume':
        "Amihud的指标对成交量，取对数刻度。<bookmark mark='a'/>一条紧密的直线，相关系数{rho:.2f}，斜率接近负一：每美元的价格变动几乎与成交额一比一地下降。"
        "它之所以有效，是因为它测量的是随规模变化的冲击，而不是一个小到看不见的价差。这就是它成为资产定价研究中标准流动性指标的原因。",

    "With quotes, the spread can be taken apart.":
        "有了报价，价差就可以拆开。<bookmark mark='a'/>有效价差：一笔交易相对于当时中点所支付的。<bookmark mark='b'/>已实现价差：流动性提供者相对于稍后的中点所保留的。"
        "<bookmark mark='c'/>两者之差，即价格冲击：输给信息的那部分价差。它就是Glosten和Milgrom的逆向选择，逐笔测量，也是监管机构和券商报告执行质量的标准方法。",

    "Pause and predict. A stock's daily price changes":
        "暂停并预测。一只股票日价格变化的自协方差是负万分之四美元平方。Roll估计量给出多大的价差？你什么时候会相信它？",

    # ------------------------------------------------------------------ Flow
    "Chapter five. Kyle's lambda is the price of order flow.":
        "第五章。Kyle的lambda是订单流的价格。要测量它，你需要知道哪些交易是买入。比特币的公开数据直接告诉了我们：每一分钟，有多少是由越过价差的交易者买入的。",

    "The data. <bookmark mark='a'/> Binance's one-minute bars":
        "数据。<bookmark mark='a'/>Binance的一分钟K线记录了有多少成交量是由越过价差的一方，即主动方，买入的。"
        "<bookmark mark='b'/>所以以美元计的带方向订单流就是主动买入减去主动卖出。"
        "<bookmark mark='c'/>Kyle的方程变成一个回归：每分钟的收益对其带方向的订单流，覆盖2021年到2024年比特币的两百多万分钟。",

    'f"The answer. <bookmark mark=\'a\'/> Lambda is':
        "答案。<bookmark mark='a'/>lambda是每一百万美元净主动买入{fu['lambda']:.1f}个基点。"
        "<bookmark mark='b'/>它的t统计量达到数百，订单流解释了分钟收益方差的{100 * fu['r2']:.0f}%：推动价格的东西中很大一部分就是订单流本身。"
        "<bookmark mark='c'/>典型一分钟的净订单流约为{f['flow_sd']:.1f}百万美元，所以它使价格移动约{move:.0f}个基点。",

    'f"But the response is not a straight line.':
        "但反应不是一条直线。<bookmark mark='a'/>按订单流把各分钟分组，平均收益在订单流小时上升得很陡，在订单流大时变平。"
        "<bookmark mark='b'/>买入最多的那些分钟，每百万美元使价格移动{r_big:.0f}个基点；最小的那些，每美元移动得多得多。"
        "平方根比直线拟合得更好：第31部分的凹性冲击，在一个根本没有交易商的市场里再次出现。",

    "Linear in Kyle, concave in data.":
        "在Kyle那里是线性的，在数据里是凹的。为什么？<bookmark mark='a'/>Kyle的直线来自正态分布：价值和噪声都是正态时，给定订单流对价值的最优估计是线性的。"
        "<bookmark mark='b'/>在数小时内执行的大订单则服从第31部分的平方根定律。"
        "<bookmark mark='c'/>大的订单流部分可以从之前的订单流预测，所以每多一美元给市场带来的意外更少；而且在大订单执行期间，流动性提供者会补充订单簿。厚尾而非正态的订单流把Kyle的直线弯成了曲线。",

    'f"A puzzle hidden in the same data.':
        "同一份数据里藏着一个谜题。<bookmark mark='a'/>带方向的订单流是持续的：这一分钟的净买入以{f1:.2f}的相关系数预测下一分钟的净买入，四小时后相关系数仍为正，{f240:.3f}。"
        "大订单被切片，所以买入接着买入。<bookmark mark='b'/>然而收益几乎不可预测。如果订单流可以预测，而订单流推动价格，为什么价格不可预测？"
        "因为市场预期到了订单流：每分钟买入中可预测的部分比意外部分的冲击更小，这正是前面测到的凹性。价格对订单流中的新信息作出反应，而不是对订单流本身。",

    'f"Lambda month by month.':
        "逐月来看lambda。<bookmark mark='a'/>它在每百万美元{lo:.1f}到{hi:.1f}个基点之间变化。它与当月波动率的相关系数是{rho:+.2f}："
        "在波动大的月份，同样的订单流把价格推得更远，正如Kyle的公式所说，因为lambda随有待了解的东西而增长。",

    'f"And through the day.':
        "以及一天之中。<bookmark mark='a'/>比特币全天候交易，但并不均匀。lambda随小时变化，它与该小时成交量的相关系数是{rho:+.2f}。"
        "Kyle的深度是可以藏身的噪声，最繁忙的时段并不自动就是最深的：当繁忙时段也是新闻时段时，噪声和信息同时到达。",

    'f"Across coins, in 2024.':
        "跨币种，2024年。<bookmark mark='a'/>五种币，从比特币到狗狗币。推动比特币每百万美元要{btc:.1f}个基点；推动XRP要{xrp:.0f}。"
        "<bookmark mark='b'/>Kyle的公式说lambda应当与有待了解的东西除以可藏身的噪声成正比：收益波动率除以订单流波动率。在对数刻度上斜率是{b1:.2f}，接近一。"
        "前面的常数是订单流与收益的相关系数，对每种币都约为二分之一：同一个市场，五种深度。",

    'f"Over longer horizons.':
        "在更长的期限上。<bookmark mark='a'/>把订单流和收益在五分钟、十五分钟、一小时上加总。lambda下降，从{l1:.1f}降到{l60:.1f}：每分钟冲击的一部分会反转，所以订单流的永久价格小于它的第一次触碰。"
        "R平方上升，从{r1:.2f}升到{r60:.2f}：在一小时的尺度上，比特币变动的三分之一可以用谁在买入来解释。",

    "What it means. <bookmark mark='a'/> Impact has a temporary part":
        "这意味着什么。<bookmark mark='a'/>冲击有一个会反转的暂时部分，和一个作为信息的永久部分。"
        "<bookmark mark='b'/>主动订单流之所以推动价格，是因为对手方分不清知情订单和噪声订单，正是Kyle的做市商。"
        "<bookmark mark='c'/>对交易者来说，凹性反应是把大订单分散到不同时间执行的理由，第37部分的主题。",

    "Pause and predict. With a lambda of four point six":
        "暂停并预测。按线性模型，lambda为每百万美元四点六个基点，在一分钟内买入一千万美元要花多少？为什么真实成本更低，而一百万美元订单每美元的真实成本更高？",

    # ------------------------------------------------------------------ VPIN
    "Chapter six. Glosten and Milgrom's mu":
        "第六章。Glosten和Milgrom的mu，知情交易者的比例，决定价差。如果能测量它，做市商就知道何时该拉宽报价。两个著名的尝试，以及对第二个的检验。",

    "PIN. <bookmark mark='a'/> David Easley":
        "PIN。<bookmark mark='a'/>David Easley、Nicholas Kiefer、Maureen O'Hara和Joseph Paperman：每天要么有私人消息，要么没有。"
        "<bookmark mark='b'/>买单和卖单随机到达，在有消息的日子里，知情交易者会加到一侧。"
        "<bookmark mark='c'/>一笔交易是知情交易的概率，用极大似然从每日的买卖笔数中估计。它成为资产定价中的一个标准变量，也是一个缓慢的变量：它需要很多天的数据。",

    "VPIN, its fast successor.":
        "VPIN，它的快速继任者。<bookmark mark='a'/>批量成交量分类：根据每根K线价格变动了多少，把它的成交量拆成买入和卖出，不需要给任何一笔交易定方向。"
        "<bookmark mark='b'/>David Easley、Marcos Lopez de Prado和Maureen O'Hara对最近五十个成交量桶的订单不平衡取平均。"
        "<bookmark mark='c'/>每个桶是一天成交量的五十分之一，所以时钟按成交量走，而不是按时间。他们认为它在2010年闪电崩盘之前就升高了。",

    "PIN has its own troubles.":
        "PIN有它自己的问题。<bookmark mark='a'/>它的似然函数有许多局部极大值，估计值取决于优化器从哪里开始。"
        "<bookmark mark='b'/>Jefferson Duarte和Lance Young发现，PIN中能预测股票收益的部分是与非流动性相关的部分，而不是与私人信息相关的部分。"
        "<bookmark mark='c'/>而两个指标都需要知道哪些交易是买入：PIN靠交易分类器，VPIN靠价格变动。分类器是薄弱环节，这正是接下来的检验。",

    'f"VPIN on four years of Bitcoin':
        "比特币四年的VPIN，一分钟K线。<bookmark mark='a'/>它平均约为{v['mean']:.2f}，有尖峰。问题是这些尖峰意味着什么。",

    "Two crashes.":
        "两次崩盘。<bookmark mark='a'/>2021年5月19日，比特币在一天之内下跌了约三分之一。<bookmark mark='b'/>以及2022年11月8日，交易所FTX崩溃之时。"
        "在两次中，VPIN都是随着崩盘本身跳升，而不是明显在崩盘之前。与损失同时到来的警告不是警告。",

    'f"Bitcoin allows a test that equities did not.':
        "比特币允许做一个股票做不到的检验。<bookmark mark='a'/>在相同的窗口上，VPIN与已实现波动率的相关系数是{v['corr_rv']:.2f}。"
        "<bookmark mark='b'/>它与真实的主动买卖不平衡的相关系数，Binance直接记录了这个不平衡，是{v['corr_true']:.2f}。"
        "<bookmark mark='c'/>批量分类在构造上就把一次大的价格变动分给一侧，所以VPIN在很大程度上是一个波动率仪表。Torben Andersen和Oleg Bondarenko在2014年正是这样批评的；这里真实的订单流证实了它。",

    "What market makers use instead.":
        "做市商实际用的是什么。<bookmark mark='a'/>事后损益：在自己的每笔成交之后，中点向对自己不利的方向移动了多远。"
        "<bookmark mark='b'/>在一秒、十秒、一分钟、五分钟上测量，并按对手方、交易场所和小时区分。"
        "<bookmark mark='c'/>不知情订单流的事后损益会恢复；知情订单流的则持续向不利于交易商的方向移动。这是直接从自己的交易中读出的Glosten和Milgrom，完全不需要分类器。",

    "The lessons. <bookmark mark='a'/> A measure inherits its classifier":
        "教训。<bookmark mark='a'/>一个指标继承了它的分类器：基于价格变动构建的指标会在价格变动时上升。<bookmark mark='b'/>在有带方向订单流的地方，就用它。"
        "<bookmark mark='c'/>而一个在波动率上升时拉宽报价的交易商仍然是对的，出于第一章的存货原因，即使那个仪表测的不是信息。",

    "Pause and predict. A bar's price rises by two standard deviations":
        "暂停并预测。一根K线的价格上涨了两个标准差，成交量一千个比特币。批量分类如何把它拆成买入和卖出？如果真实的拆分是对半呢？",

    # ------------------------------------------------------------------ Discovery
    "Chapter seven. Bitcoin trades on a spot market":
        "第七章。比特币在现货市场交易，也以五倍的成交量作为永续合约交易。套利把两个价格绑在一起。但消息总得先到达某个地方。Joel Hasbrouck的问题：哪个市场发现了价格？",

    "The model. <bookmark mark='a'/> Both prices are one efficient price":
        "模型。<bookmark mark='a'/>两个价格都是同一个有效价格加上各市场特有的噪声。<bookmark mark='b'/>有效价格是随机游走；它的新息就是消息。"
        "<bookmark mark='c'/>两者之差，即基差，是平稳的：两者协整，第33部分的词，由套利维系在一起。",

    "The tool. <bookmark mark='a'/> Part thirty-three's error-correction model":
        "工具。<bookmark mark='a'/>第33部分的误差修正模型，用于两个价格。<bookmark mark='b'/>载荷alpha说明每个市场向收窄基差的方向移动得多强。"
        "<bookmark mark='c'/>不调整的那个市场就是另一个市场所追随的，所以每个市场在共同趋势中的权重，等于另一个市场的调整速度。",

    "Hasbrouck's information share.":
        "Hasbrouck的信息份额。<bookmark mark='a'/>有效价格新息的方差来自残差协方差。<bookmark mark='b'/>每个市场在其中所占的份额就是它的信息份额。"
        "<bookmark mark='c'/>但当两个市场的冲击在一个采样间隔内相关时，拆分取决于哪个排在前面，答案是一个区间。",

    'f"The answer, month by month, from one-minute bars.':
        "答案，逐月，来自一分钟K线。<bookmark mark='a'/>每根柱子是永续合约信息份额的区间。平均而言它从接近零到接近一：宽度为{d['width']:.2f}。在一分钟采样下，这个方法无法说明哪个市场领先。",

    'f"Why. <bookmark mark=\'a\'/> Within a minute':
        "为什么。<bookmark mark='a'/>在一分钟之内，两个收益几乎是同一个数：相关系数{d['corr0']:.3f}。"
        "<bookmark mark='b'/>套利者在几毫秒内对齐两个订单簿，一分钟里包含数千轮价格发现。"
        "<bookmark mark='c'/>所以这个方法需要更细的数据，用逐笔数据的研究通常发现期货市场领先。一个如实报告的零结果：本系列公司的数据太粗，回答不了这个问题。",

    "What the method found when it was new.":
        "这个方法刚出现时的发现。<bookmark mark='a'/>Joel Hasbrouck研究了在纽约证券交易所和地区交易所交易的三十只道琼斯股票，发现纽交所的信息份额超过十分之九。"
        "<bookmark mark='b'/>它之所以奏效，是因为那时报价以秒为单位变动；以今天的速度，同样的问题需要纳秒级时间戳。"
        "<bookmark mark='c'/>在许多研究中，股指期货都领先于股票：知情交易者先去更便宜、杠杆更高的市场。",

    'f"What one-minute data can still say.':
        "一分钟数据仍然能说明什么。<bookmark mark='a'/>永续合约上一分钟的收益以{d['lead_perp']:+.3f}的相关系数预测现货下一分钟的收益；反过来是{d['lead_spot']:+.3f}。很小，但不对称。"
        "<bookmark mark='b'/>而永续合约的美元成交量是现货的{ratio:.1f}倍。持续几秒的领先留下的残迹指向同一个方向：杠杆便宜、成交量集中的衍生品先动。",

    'f"What holds the two prices together.':
        "是什么把两个价格绑在一起。<bookmark mark='a'/>永续合约永不到期；取而代之的是，每八小时，当永续合约价格高于现货时多头向空头支付资金费率，低于现货时空头向多头支付。"
        "月平均基差保持在几个基点之内：最大是在{hi_m}，牛市之中，最负是在{lo_m}。资金费率就是按时间表支付的套利；第39部分会构建它。",

    "Pause and predict. Two markets: when the basis widens":
        "暂停并预测。两个市场：当基差扩大时，市场A收窄其中的百分之九十，市场B收窄百分之十。哪个的信息份额更大，大约是多少？",

    # ------------------------------------------------------------------ Structure
    "Chapter eight. The models so far had one dealer":
        "第八章。到目前为止的模型都只有一个交易商和一个市场。一只美国股票在十多家交易所和数十个场外场所交易，由规则连接起来。规则决定谁与谁相遇，以什么价格。",

    "The rules, in the United States.":
        "美国的规则。<bookmark mark='a'/>2005年通过的全国市场系统规则：任何场所都不得穿越另一个场所显示的更优价格成交。"
        "<bookmark mark='b'/>每个场所都必须让其他场所以有上限的费用访问它的报价。<bookmark mark='c'/>对一美元以上的股票，报价不得精细于一美分。"
        "<bookmark mark='d'/>它们共同定义了全国最佳买卖报价，每个券商的执行质量都以它为基准来评判。一个市场，由许多市场拼成。",

    "How venues compete.":
        "交易场所如何竞争。<bookmark mark='a'/>大多数交易所向挂出限价单的交易者，即挂单方，按每股几分之一美分支付返佣。"
        "<bookmark mark='b'/>向越过价差的交易者，即吃单方，收取费用。<bookmark mark='c'/>所以一笔交易的真实成本是扣除费用和返佣后的价差。"
        "有些场所把方案倒过来，向吃单方付钱，从而吸引不同的订单：场所的价目表决定了谁在那里交易。",

    "Where orders go.":
        "订单去向哪里。<bookmark mark='a'/>交易所：显示的订单簿，它们设定全国最佳报价并主持开盘和收盘拍卖。"
        "<bookmark mark='b'/>暗池：没有显示报价的场所，通常按中点撮合，大订单可以藏在其中，这正是Kyle的内幕交易者的愿望。"
        "<bookmark mark='c'/>还有批发商，它们从券商那里购买散户订单并自己成交，常常比最佳报价略好。据报道，场外交易合计约占美国股票成交量的一半。",

    "Who chooses the dark?":
        "谁选择暗处？<bookmark mark='a'/>暗池按中点撮合买卖双方，省下价差，但前提是对手方出现。"
        "<bookmark mark='b'/>Haoxiang Zhu表明，知情交易者都想站在同一侧，所以他们在暗池的订单常常无法撮合，他们更偏好明盘市场确定的成交。"
        "<bookmark mark='c'/>所以暗池吸引不知情者，这使信息集中到交易所：即使公开价差变宽，价格发现也可能改善。",

    "Chapter two explains the consequences.":
        "第二章解释了后果。<bookmark mark='a'/>散户订单不太可能带有信息，所以批发商可以在价差之内成交它们并且仍然盈利。"
        "<bookmark mark='b'/>留在交易所的订单信息含量更高。<bookmark mark='c'/>而根据Glosten和Milgrom，知情交易者比例更大意味着留下来的每个人面对更宽的公开价差。"
        "分流帮助了离开的那部分，却可能损害每个人看到的价格：订单流付费争论的核心。",

    "The rules keep changing.":
        "规则在不断变化。<bookmark mark='a'/>2024年9月，美国证券交易委员会为价差通常被卡在一个最小价位的股票采用了半美分最小价位，并降低了访问费上限。"
        "<bookmark mark='b'/>被卡在一美分的价差比它的自然水平更宽；多出的部分由吃单方支付，挂单方则靠排队位置而不是价格来竞争它，第36部分的主题。"
        "<bookmark mark='c'/>而IEX，2016年起成为交易所，把每一笔进入的订单延迟三百五十微秒，使过时的报价无法被狙击。",

    "Two more pieces of the plumbing.":
        "管道系统的另外两部分。<bookmark mark='a'/>收盘拍卖：指数基金和以基准考核的管理人需要官方收盘价，所以每天成交量中越来越大的一部分在最后的拍卖中成交。"
        "<bookmark mark='b'/>拍卖以单一价格撮合所有订单，一天一次的批量拍卖，正是第十章为每一时刻提出的设计。"
        "<bookmark mark='c'/>还有订单类型，从市价单到挂钩单再到隐藏单，每一种都表明交易者想买入或卖出多少即时性。",

    "And after the trade.":
        "还有交易之后。<bookmark mark='a'/>从2024年5月起，美国股票在交易后一个工作日结算，而不是两个。"
        "<bookmark mark='b'/>等待更短意味着对会员违约的暴露更少，所以清算所要求的抵押品更少；第21部分讲到的2021年1月迷因股逼空就是理由。"
        "<bookmark mark='c'/>在加密货币交易所，交易在交易所自己的账本上即时结算，根本没有清算所，交易所本身就是对手方，正如FTX所显示的。",

    "One retail order's journey.":
        "一笔散户订单的旅程。<bookmark mark='a'/>券商，它对客户负有最佳执行义务，并可能为这笔订单收到付款。"
        "<bookmark mark='b'/>路由器，它按价格、费用和成交概率把订单拆分到各个场所。<bookmark mark='c'/>批发商或暗池，能在最佳报价之内成交的就成交。"
        "<bookmark mark='d'/>明盘交易所，处理剩下的部分，按受保护的报价成交。<bookmark mark='e'/>一天之后，通过清算所结算。每一个箭头都是关于对手方是谁的一个选择。",

    "Pause and predict. A twenty-dollar stock":
        "暂停并预测。一只二十美元的股票报价宽一美分，但它的自然价差只有三分之一美分，挂单方获得五分之一美分的返佣。吃单方真正支付多少？半美分最小价位使谁获益？",

    # ------------------------------------------------------------------ HFT
    "Chapter nine. The dealers of Chapter one are now algorithms":
        "第九章。第一章的交易商现在是算法，为数以千计的品种报价，以微秒更新。它们是今天的做市商，还是别的什么？证据说两者都是，取决于时刻。",

    "The new market makers.":
        "新的做市商。<bookmark mark='a'/>Albert Menkveld研究了欧洲股票上的一家高频做市商：它的大多数交易是被动的，在它自己的报价上成交。"
        "<bookmark mark='b'/>它的存货迅速回到零，每天收盘时接近持平：第一章的偏移，被自动化了。"
        "<bookmark mark='c'/>它赚取价差，减去信息更多的交易者拿走的部分，而它的速度让这些损失保持很小：在消息到来之前就更新的报价，就是不会被狙击的报价。",

    "The evidence. <bookmark mark='a'/> Terrence Hendershott":
        "证据。<bookmark mark='a'/>Terrence Hendershott、Charles Jones和Albert Menkveld：2003年纽约证券交易所自动化其报价时，算法交易增加，大盘股的价差收窄。"
        "<bookmark mark='b'/>Jonathan Brogaard、Hendershott和Ryan Riordan：高频交易者的主动订单沿着永久性价格变化的方向移动，加快了价格发现。"
        "<bookmark mark='c'/>而同样的订单在消息到来时从较慢的报价那里吃走流动性：它们的部分利润就是其他做市商的逆向选择。",

    "Eric Budish, Peter Cramton and John Shim found":
        "Eric Budish、Peter Cramton和John Shim发现了一种完全没有私人信息的逆向选择。<bookmark mark='a'/>当公开消息改变价值时，一场竞赛开始：报价的主人试图撤单，其他所有人试图成交。"
        "<bookmark mark='b'/>在连续时间里总有人先到，而主人是一对多。<bookmark mark='c'/>所以价差必须覆盖一笔任何速度都无法消除的狙击损失，因为每个人都一起变快。第十章给出他们的补救办法。",

    "And a subtler kind of speed.":
        "还有一种更微妙的速度。<bookmark mark='a'/>一家养老基金切分一笔大订单，会在订单流中留下一个模式。"
        "<bookmark mark='b'/>Liyan Yang和Haoxiang Zhu建模了反向跟单者：察觉这个模式并朝同一方向交易的快速交易者，他们提高了机构的成本，同时让价格更早地接近其信息。"
        "<bookmark mark='c'/>所以执行算法加入随机性，并把规模藏在暗池里：Kyle的内幕交易者，对阵一个会读订单流的对手。",

    "Is the sniping cost large?":
        "狙击成本大吗？<bookmark mark='a'/>Matteo Aquilina、Eric Budish和Peter O'Neill利用伦敦证券交易所的消息数据，包括撤单失败的尝试，找到了快速交易者争抢同一个过时报价、在微秒内决出胜负的竞赛。"
        "<bookmark mark='b'/>他们报告这类竞赛约占富时一百成交量的五分之一，对全部交易形成约半个基点的流动性税。<bookmark mark='c'/>由投资者通过价差支付，被少数最快的公司赢走。",

    "And the abuses speed allows.":
        "还有速度带来的违规。<bookmark mark='a'/>动量点火：意在引发其他算法跟随的激进订单，然后反向交易。<bookmark mark='b'/>幌骗和分层挂单，第34部分的案件。"
        "<bookmark mark='c'/>以及拖慢他人数据的大量下单和撤单。每一种都利用了其他算法在读订单簿这一点，这就是监控也要读它的原因。",

    "Pause and predict. A quote is hit by a sniper":
        "暂停并预测。当公开消息到来时一个报价会被狙击，这发生在它百分之二的成交上，每次损失三个最小价位。覆盖它的最小价差是多少？",

    # ------------------------------------------------------------------ Crashes
    "Chapter ten. Every model in this part assumed someone is quoting.":
        "第十章。这一部分的每个模型都假设有人在报价。过去十五年里，世界上最深的市场有两次在几分钟内失去了报价，价格去了谁也没想到的地方。",

    "The sixth of May, 2010.":
        "2010年5月6日。<bookmark mark='a'/>在一个本已紧张的下午，一家大型基金集团开始卖出七万五千份E-mini期货合约，约四十亿美元，所用算法被设定为无论价格如何都交易成交量的百分之九，正如监管机构联合报告所描述的。"
        "E-mini在几分钟内下跌约百分之五；股票随之下跌，有些以一美分成交；大部分跌幅在约二十分钟内收复。",

    "What happened inside.":
        "内部发生了什么。<bookmark mark='a'/>一个按固定成交量比例交易的算法，在成交量上升时会加速，而它自己的卖出又推高了成交量。"
        "<bookmark mark='b'/>Andrei Kirilenko、Albert Kyle、Mehrdad Samadi和Tugkan Tuzun发现，高频交易者没有引发下跌，但他们在彼此之间来回传递存货，像传烫手山芋，进一步推高了成交量，然后退了出去。"
        "<bookmark mark='c'/>由于没有人愿意持有存货，第一章的交易商消失了，订单打在了远离任何价值的占位报价上。",

    "What changed after.":
        "之后发生了什么变化。<bookmark mark='a'/>单只股票的价格区间，当价格过快变动过远时暂停交易。<bookmark mark='b'/>取消远离市场成交的规则。"
        "<bookmark mark='c'/>还有给依赖流动性的人的教训：它是交易商每一微秒都在做的选择，在最不需要时充裕，在存货风险飙升时撤走。",

    'f"Liquidity that comes and goes':
        "来来去去的流动性，在比特币上逐日测量。<bookmark mark='a'/>2021年到2024年每一天的Kyle lambda：中位数为每百万美元{d['median']:.1f}个基点。"
        "<bookmark mark='b'/>在最糟糕的日子里它是中位数的{ratio:.1f}倍，而最糟糕的日子集中在2022年：6月和7月加密货币借贷机构的倒闭，以及11月FTX崩溃的那一周。"
        "它与当日波动率的相关系数是{d['corr_vol']:.2f}，与当日美元成交量基本为零：在压力之日，无论交易是否活跃，深度都消失了。",

    "In crypto, liquidity can vanish by design.":
        "在加密货币中，流动性可能按设计消失。<bookmark mark='a'/>永续合约让交易者持有大额杠杆头寸，当价格跌破保证金时自动按市价平仓。"
        "<bookmark mark='b'/>每一笔强制卖出都是主动订单流，按lambda推动价格。<bookmark mark='c'/>如果一个基点的下跌所触发的卖出使价格下跌超过一个基点，下跌就会自我强化，直到杠杆耗尽。"
        "刚才测到的压力日更高的lambda，恰恰在连锁平仓开始时让它更有可能发生。",

    "And bonds.":
        "还有债券。<bookmark mark='a'/>2014年10月15日，在世界上流动性最好的债券市场，十年期美国国债收益率在大约十二分钟内下跌约十六个基点又回升，没有任何消息可以解释。"
        "官方报告发现，高频公司主导了交易，而且订单簿在这次变动之前已经变薄。一个市场可以在成交量上很深，在承诺上却很浅。",

    "Chapter nine's remedy.":
        "第九章的补救办法。<bookmark mark='a'/>今天，订单一到达就撮合，所以微小的速度优势赢得每一场竞赛。"
        "<bookmark mark='b'/>Budish、Cramton和Shim提出频繁批量拍卖：把订单收集一小段时间，然后以单一价格全部撮合。"
        "<bookmark mark='c'/>在一个批次内，先到毫无价值，所以想狙击的人必须在价格上竞争，公开消息带来的租金流回报价的主人，并通过更窄的价差流向投资者。",

    "The arithmetic, in Chapter nine's example.":
        "算术，用第九章的例子。<bookmark mark='a'/>当每笔交易赚到的半个价差覆盖对狙击者的期望损失时，做市商盈亏平衡。"
        "<bookmark mark='b'/>百分之二的交易伴随消息，每次使价值移动三个最小价位：价差必须比原本至少宽零点一二个最小价位。"
        "<bookmark mark='c'/>在批量拍卖中，做市商可以在消息所在的同一批次中修改订单，价差中的这一部分就消失了。",

    "Pause and predict. A seller must sell five percent":
        "暂停并预测。一个卖家必须卖出一个市场日成交量的百分之五，使用一个按成交量百分之九交易的算法。它自己的卖出使成交量翻倍。所需时间会怎样？",

    # ------------------------------------------------------------------ House
    "Chapter eleven. The House's thirty-fifth rule":
        "第十一章。本系列公司的第35条规则是关于对手方的。任何交易台在一个市场交易之前，必须知道它可能在和谁交易，以及它自己的订单会告诉他们什么。",

    "The first sheet. <bookmark mark='a'/> Shading keeps":
        "第一张汇总表。<bookmark mark='a'/>偏移让交易商的存货保持很小。知情交易让价差变宽、价格变快。连续交易的内幕交易者赚到定理所说的数。"
        "比特币的订单流有一个可测量的、凹的价格，解释了它五分之一到三分之一的变动。经典的日度价差估计量在流动性好的基金上失效。VPIN测量的更多是波动率而不是毒性。"
        "而一分钟数据无法分辨哪个比特币市场在发现价格。",

    'f"And the House\'s own footprint.':
        "还有本系列公司自己的足迹。<bookmark mark='a'/>如果本系列公司的币种组合在一分钟内调仓一千万美元比特币，Kyle的直线给出{lin:.0f}个基点。"
        "<bookmark mark='b'/>第五章测到的凹性反应给出接近{cost_sq:.0f}。<bookmark mark='c'/>分散到一小时内，每分钟的那一份使价格移动{lam * per_min:.2f}个基点，而每次触碰的大部分都会反转。如何最优地切分是第37部分的内容。",

    "Chapter two's quotes in four lines.":
        "第二章的报价，四行代码。价值高时买入的概率，价值低时买入的概率；给定买入和给定卖出时价值的贝叶斯法则；报价就是期望值。其中没有任何关于利润的东西：零利润已经内置于定义之中。",

    "Chapter five's regression:":
        "第五章的回归：去掉缺失的分钟，把收益对带方向的订单流加常数项做回归，报告lambda及其t统计量和解释的方差比例。研究章节对Kyle模型的检验就是最后这个数。",

    "And Chapter seven's shares.":
        "还有第七章的份额。共同趋势的权重是调整速度的正交补；然后，对两个市场的每一种排序，分解残差协方差，取每个市场在有效价格方差中的那一部分。两种排序，两个答案，真值在两者之间。",

    "And the research chapter's market.":
        "还有研究章节的市场。每一步，内幕交易者把剩余的差距除以剩余的时间来交易，噪声加入它的随机订单，价格移动lambda乘以总量。七行代码，每条路径都终止于价值。",

    "The tools this part adds. <bookmark mark='a'/> Dealers;":
        "这一部分新增的工具。<bookmark mark='a'/>交易商；三种形式的Kyle模型；流动性指标；毒性与价格发现；以及一个带方向订单流的数据源。"
        "<bookmark mark='b'/>还有第35条规则。交易台在一个市场交易之前，要说明对手方可能是谁，并测量该市场订单流的价格。"
        "在有带方向订单流的地方，用它而不是日度价差代理变量来估计自己的冲击。合规部门要像对手那样阅读交易台自己的订单。",

    "The rule against three cases.":
        "用这条规则检验三个案例。<bookmark mark='a'/>一篇用Roll估计量测量价差的论文：问资产的真实价差是不是一美分。"
        "<bookmark mark='b'/>一家出售毒性信号的供应商：问它与波动率以及与带方向订单流的相关性。"
        "<bookmark mark='c'/>一个今天必须买入五千万美元的交易台：问lambda、它的凹性，以及谁会看到这些订单，然后切分它们。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter three's recursion":
        "写给研究者。第三章的递推暗示了一个极限：随着拍卖次数增多，价格冲击趋于稳定，剩余的不确定性沿直线下降。"
        "本章按照Kyle 1985年的论文和Kerry Back 1992年的证明，在连续时间中证明这个极限，并加以检验。",

    "The setup. <bookmark mark='a'/> A value v, known to the insider":
        "设定。<bookmark mark='a'/>一个价值v，内幕交易者知道，在时刻一向所有人揭示。<bookmark mark='b'/>总订单流：内幕交易者以速率theta交易，噪声交易者是布朗运动。"
        "<bookmark mark='c'/>做市商把价格定为给定迄今订单流的期望价值。<bookmark mark='d'/>内幕交易者的利润累积它买入的每一单位上价值与价格之差。",

    "Lemma one, the market maker.":
        "引理一，做市商。<bookmark mark='a'/>假设内幕交易者按剩余错误定价的比例交易。"
        "<bookmark mark='b'/>那么做市商的问题是一个Kalman-Bucy滤波器，即连续时间中第7部分的滤波器：价格按订单流的比例移动，增益为lambda。"
        "<bookmark mark='c'/>剩余的不确定性以lambda平方乘以噪声方差的速率下降。",

    "Lemma two, the insider.":
        "引理二，内幕交易者。<bookmark mark='a'/>Kerry Back对内幕交易者价值函数的猜测，lambda为常数：错误定价的平方，加上lambda平方乘sigma u平方乘剩余时间，再除以二倍lambda。"
        "<bookmark mark='b'/>它的导数很简单。<bookmark mark='c'/>在结束时，剩下的是从未被交易掉的错误定价的平方：留在桌上的钱。",

    "Check it in Part eight's Hamilton-Jacobi-Bellman equation.":
        "在第8部分的汉密尔顿-雅可比-贝尔曼方程中检验它。<bookmark mark='a'/>在最优交易速率下，利润率加上价值函数的漂移必须为零。"
        "<bookmark mark='b'/>含theta的项恰好抵消：内幕交易者对交易快慢无所谓。<bookmark mark='c'/>其余项也抵消。所以每种策略赚得一样多，只要它不在桌上留钱：价格必须在时刻一之前到达价值。",

    "Lemma three closes the loop.":
        "引理三闭合了循环。<bookmark mark='a'/>lambda为常数时，引理一的方差沿直线下降，它必须在结束时降到零。"
        "<bookmark mark='b'/>这就确定了lambda：初始方差的平方根除以sigma u。<bookmark mark='c'/>而让价格恰好到达价值的策略，是把剩余的差距除以剩余的时间来交易，它对差距是线性的，正如引理一所假设的。",

    "The theorem. <bookmark mark='a'/> Lambda is sigma v over sigma u":
        "定理。<bookmark mark='a'/>lambda等于sigma v除以sigma u；内幕交易者把剩余差距除以剩余时间来交易；剩余的不确定性线性下降到零。"
        "<bookmark mark='b'/>期望利润，即在v上取平均的初始价值函数，是sigma v乘以sigma u：单次拍卖利润的两倍。对市场而言，价格是一个波动率恒定的鞅；对内幕交易者而言，它是一座终止于价值的布朗桥。",

    "One path, two views.":
        "一条路径，两种视角。<bookmark mark='a'/>对做市商而言，总订单流看起来与噪声完全一样：价格是一个鞅，第4部分的公平游戏。"
        "<bookmark mark='b'/>对知道v的内幕交易者而言，同一个价格有一个把它拉向价值的漂移：一座布朗桥。"
        "<bookmark mark='c'/>内幕交易者完美地隐藏了自己。它的交易没有改变订单流的分布，这正是lambda可以保持不变的原因。",

    "Four simulated markets.":
        "四个模拟市场。<bookmark mark='a'/>每个价格都像随机游走一样被噪声推动着游走。<bookmark mark='b'/>每个都恰好终止于它的价值，即那个点，因为随着时间耗尽，内幕交易者的交易越来越用力地把它拉过去。",

    'f"Across six hundred markets.':
        "跨六百个市场。<bookmark mark='a'/>价值与价格之差的均方沿着定理的直线，一减t，下降。"
        "<bookmark mark='b'/>内幕交易者的平均利润是{pr:.3f}，定理给出{prt:.0f}。信息以恒定速率泄漏出来，恰好与噪声允许的一样快。",

    "And Kyle's discrete recursion approaches it.":
        "而Kyle的离散递推逼近它。<bookmark mark='a'/>拍卖越多，第一次的价格冲击越趋近于一，中途的不确定性越趋近于二分之一，结束时的不确定性越趋近于零。"
        "连续定理是离散博弈的极限，正如Kyle所猜想、Back所证明的。",

    "Two refinements.":
        "两个细化。<bookmark mark='a'/>随着结束临近，内幕交易者的强度无界地上升。<bookmark mark='b'/>但它交易所依据的差距同时在缩小，所以它的期望交易量只按剩余时间的倒数增长。"
        "<bookmark mark='c'/>在更长的期限上，噪声有更多时间掩护内幕交易者：lambda随期限的平方根下降，利润随之上升。",

    "Compared. <bookmark mark='a'/> One auction reveals half":
        "比较。<bookmark mark='a'/>一次拍卖揭示一半的信息。<bookmark mark='b'/>跨时间交易，内幕交易者揭示了全部信息，却仍然赚两倍，因为它从不比噪声能掩护的更快地交易。"
        "<bookmark mark='c'/>而噪声交易者亏掉的恰好是内幕交易者赚到的：他们为价格的信息含量付钱。",

    'f"A test against data.':
        "用数据检验。<bookmark mark='a'/>在Kyle的模型中，每一次价格变化都通过订单流发生，所以收益对订单流的回归会完美拟合。"
        "<bookmark mark='b'/>在比特币上，第五章在一分钟上得到R平方{r1:.2f}，在一小时上得到{r60:.2f}。"
        "<bookmark mark='c'/>其余部分是在任何人交易之前就推动报价的公开信息：第九章的狙击竞赛，Kyle只有私人信息的模型没有包括它。这个模型解释的是价格中从交易里学到的那部分，而数据说那是五分之一到三分之一。",

    "Where this sits. <bookmark mark='a'/> Kerry Back proved":
        "这个结果的位置。<bookmark mark='a'/>Kerry Back用这里所用的价值函数，对一般的价值分布证明了连续均衡。"
        "<bookmark mark='b'/>Craig Holden和Avanidhar Subrahmanyam表明，几个相互竞争的内幕交易者会彼此抢跑，信息几乎立即释放。"
        "<bookmark mark='c'/>而Back和Shmuel Baruch把这一部分的两个模型联系起来：交易频繁而规模很小的Glosten-Milgrom市场会变成Kyle的市场。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>一个同时包含公开消息与渐进私人信息、并且与第五章的R平方相符的可处理均衡，目前还不知道。"
        "<bookmark mark='b'/>会择时交易的噪声交易者，就像最优执行者那样，会改变订单流所揭示的东西。"
        "<bookmark mark='c'/>以及一个在明盘、暗池和衍生品市场之间选择的内幕交易者：它的信息首先出现在哪里，没有闭式解。",

    "Pause and predict. In continuous Kyle":
        "暂停并预测。在连续Kyle模型中，sigma v为二，sigma u为一。lambda、价格的波动率和内幕交易者的期望利润各是多少？如果期限是四年而不是一年，它们如何变化？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-five in fourteen lines.":
        "第35部分，十四行。交易商必须偏移报价，否则会被自己的存货拖垮。价差是对知情交易者的保险。Kyle的内幕交易者以它能交易的一半力度交易，lambda是订单流的价格。"
        "日度价差估计量在流动性好的基金上失效，而Amihud比率有效。在比特币上订单流的价格是可测量的，而且是凹的。一个著名的毒性指标主要是波动率。而一分钟K线太粗，找不到比特币的价格在哪里被发现。",

    "American markets are one market":
        "美国市场是由规则拼成的一个市场，而规则在不断变化。高频交易者是今天的交易商，也是今天的狙击手。流动性曾两次在几分钟内消失。"
        "批量拍卖会让交易者在价格而不是速度上竞争。研究章节证明了，连续交易的内幕交易者会揭示一切，并赚两倍。",

    "Six desk questions.":
        "六个交易台问题。为什么交易商是竞争性的、风险中性的，却仍然有价差？逆向选择。<bookmark mark='a'/>什么是Kyle的lambda？一单位订单流的价格。"
        "<bookmark mark='b'/>交易商为什么要偏移报价？为了消化存货。",

    "When does Roll's estimator fail?":
        "Roll估计量何时失效？当反弹很小时。<bookmark mark='a'/>VPIN测量的是什么？主要是波动率。<bookmark mark='b'/>是什么使闪电崩盘成为可能？撤走的流动性。完整解答在讲义里。",

    'f"The pause questions, answered.':
        "暂停题的答案。持有四十个单位的交易商把中点报在价值下方二：它为了出货而低价卖出。"
        "<bookmark mark='a'/>十个里有四个知情、一笔买入之后，买价是{b1:.2f}，卖价是{a1:.2f}。<bookmark mark='b'/>当噪声翻倍时，lambda下降，内幕交易者的订单和利润上升，各为原来的根号二倍。",

    'f"Roll\'s spread is':
        "Roll价差是{roll:.2f}美元，只有在反弹占主导时才可信。<bookmark mark='a'/>一分钟内一千万美元，按直线是四十六个基点，实际更少。"
        "<bookmark mark='b'/>一根两倍标准差的K线被拆成约{buy:.0f}对{1000 - buy:.0f}，无论真实的拆分是什么。",

    "The market that hardly adjusts leads.":
        "几乎不调整的市场领先。<bookmark mark='a'/>半美分最小价位有利于吃单方，狙击价差是零点一二个最小价位。"
        "<bookmark mark='b'/>成交量翻倍使时间减半。在sigma v为二的连续Kyle模型中，lambda、价格的波动率和利润都是二；在四年期限上，lambda减半，利润翻倍。",

    "And twelve problems: a shaded dealer":
        "还有十二道习题：偏移报价的交易商；一笔买入之后的Glosten和Milgrom；噪声更多时的Kyle；Roll；lambda的成本；批量分类；信息份额；做市-吃单收费下的真实成本；狙击价差；按成交量比例卖出的卖家。"
        "然后是两道资格考试题：用价值函数推导连续Kyle模型，以及单次拍卖均衡及其期限缩放。中英文解答都在讲义里。",

    "Where this comes back. Part thirty-six opens":
        "这些内容会在哪里再次出现。第36部分打开限价订单簿。第37部分像Kyle的内幕交易者那样，最优地切分订单。第38部分又是交易商，存货与逆向选择同时出现。第39部分是比特币交易的那个市场。",

    "The textbooks this part follows, and the papers it draws on, from Garman":
        "这一部分所依据的教科书，以及它引用的论文，从1976年的Garman到闪电崩盘的研究。屏幕上的每个数字都由本系列公司的代码，用Binance的公开数据档案、Yahoo Finance的K线和模拟算出，示意图都已标明。",

    "The House now knows who is on the other side":
        "本系列公司现在知道它交易的另一方是谁：保护存货的交易商、藏身于噪声中的知情交易者，以及阅读它订单的其他算法。"
        "<bookmark mark='a'/>下一部分，第36部分：限价订单簿。排队、最小价位，以及一张挂单在价格离开之前被成交的概率。",

}
