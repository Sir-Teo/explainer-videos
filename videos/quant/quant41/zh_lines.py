"""Chinese narration for quant41: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 杠杆 (leverage), 折扣率 (haircut), 去杠杆 (deleveraging), 损失螺旋
(loss spiral), 保证金螺旋 (margin spiral), 甩卖 (fire sale), 共同持仓 (common holdings), 清算向量 (clearing vector), 虚拟违约算法
(fictitious default algorithm), 相变 (phase transition), 系统性风险 (systemic risk), 条件在险价值 CoVaR, 边际预期亏损 (MES),
SRISK, 影子银行 (shadow banking), 回购 (repo), 商业票据 (commercial paper), 跌破面值 (breaking the buck), 最后贷款人 (lender of
last resort), 基差交易 (basis trade), 熔断 (circuit breaker), 磁吸效应 (magnet effect), 挤兑 (run), 全局博弈 (global games),
持有至到期 (held to maturity), 负债驱动投资 (LDI), 额外一级资本债 (AT1), 非银行金融中介 (NBFI), 逆周期 (anti-procyclical)."""

TITLE = '量化金融，从零搭建 · 第41部分：杠杆、流动性与危机'

CHAPTERS = {
    'Hook': '一只加杠杆的基金必须卖掉多少？',
    'Cycles': '1. 杠杆及其周期',
    'Spirals': '2. 螺旋',
    'FireSales': '3. 甩卖',
    'Networks': '4. 网络',
    'Systemic': '5. 度量系统性风险',
    'LTCM': '6. 1998年：长期资本管理公司',
    'GFC': '7. 2007—08年：影子银行的挤兑',
    'Dash': '8. 2020年3月：现金争夺战',
    'China': '9. 2015年：上海的杠杆牛市',
    'Y2023': '10. 2022—23年：加息、挤兑与救助',
    'House': '11. 第41条规则：挺过还没收到的追加保证金通知',
    'Research': '写给研究者：清算向量',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part forty-one. Leverage, liquidity and crises:":
        "第41部分。杠杆、流动性与危机：借来的钱和短期融资如何把小额亏损变成被迫抛售，把被迫抛售变成螺旋，把一家公司的麻烦变成所有人的麻烦。"
        "从长期资本管理公司到硅谷银行，每一个都配上它的数学。",

    'f"What this part finds. <bookmark mark=\'a\'/> Spirals amplify:':
        "这一部分的发现。<bookmark mark='a'/>螺旋会放大冲击：当价格下跌时贷款方提高保证金，百分之三的冲击最终变成{100 * k2['fall']:.0f}%的下跌，"
        "放大到{k2['amp']:.1f}倍。<bookmark mark='b'/>银行之间的联系先分担损失，然后传播损失：在一个十家银行的完全网络里，冲击不超过{rs['thr']:.0f}时"
        "只有受冲击的那一家倒下；超过它，十家全部倒下。<bookmark mark='c'/>有偿付能力的银行也会倒闭：如果资产提前卖出只能拿回百分之八十五，"
        "任何资产回报低于{dd['thr85']:.2f}的银行都会遭到挤兑。<bookmark mark='d'/>就连最安全的资产也会在恐慌中被抛售：二〇二〇年三月，股市下跌时，"
        "美国国债收益率从{ds['y10']['m9']:.2f}%升到了{ds['y10']['m18']:.2f}%。",

    "Why it matters. <bookmark mark='a'/> Crises end firms:":
        "为什么重要。<bookmark mark='a'/>危机会终结公司：长期资本管理公司、贝尔斯登、雷曼、AIG、Archegos、硅谷银行和瑞士信贷，都曾规模庞大、"
        "备受推崇，却在几周之内消失。<bookmark mark='b'/>危机也制定规则：资本和流动性比率、中央清算、压力测试和保证金规则，每一条都是在一场危机之后"
        "写下的。<bookmark mark='c'/>而本系列公司运行的每一个策略都由别人提供资金。第40部分度量了它可能亏多少；这一部分要问，它能不能挺过这样的亏损。",

    "And what this part is not.":
        "以及这一部分不是什么。<bookmark mark='a'/>它不是预测：这里没有一个模型能说出下一场危机何时到来，它们只说明冲击如何放大、什么让体系变得脆弱。"
        "<bookmark mark='b'/>它不是追责：公司只按公开记录的描述出现。<bookmark mark='c'/>它也不是投资建议。",

    "Where this sits. Act seven, the system.":
        "这一部分的位置。第七幕，体系。第40部分逐家公司地度量风险。这一部分沿着杠杆和流动性跨越公司，走进危机。接着第42部分让机器进入市场，"
        "第43部分追问这一切能否战胜市场。",

    "Forty years of crises, and of the theory":
        "四十年的危机，以及随之而来的理论。戴蒙德和迪布维格的银行挤兑；一九八七年的股灾；施莱弗和维什尼关于抛售的极限；长期资本管理公司。"
        "<bookmark mark='a'/>艾森伯格和诺伊的清算模型，雷曼和AIG，布伦纳迈尔和佩德森的螺旋，吉纳科普洛斯的杠杆周期。<bookmark mark='b'/>"
        "然后是上海股灾和传染阈值、SRISK、现金争夺战，以及二〇二三年的挤兑。",

    "The plan: leverage and its cycle;":
        "计划：杠杆及其周期；螺旋与甩卖；债务网络；度量系统性风险；用公开数据看五场危机；银行挤兑与本系列公司自己的流动性压力测试；"
        "以及网络清算背后的定理，给出证明。",

    "In the House, the treasury and funding desk":
        "在本系列公司里，资金与融资部门加入风险部门，提出一个任何单一风险数字都回答不了的问题：如果所有贷款方同时要求更多，本系列公司必须卖掉什么？",

    "A desk question to start.":
        "先来一个交易台问题。<bookmark mark='a'/>一只五倍杠杆的基金亏了百分之十。<bookmark mark='b'/>它的贷款方把抵押品的折扣率从百分之二十提高到"
        "百分之三十。<bookmark mark='c'/>暂停并预测：它必须卖掉多少？",

    # ------------------------------------------------------------------ Cycles
    "f'Chapter one, and the answer to the pause:":
        "第1章，以及暂停问题的答案：它持有的{b['assets']:.0f}中要卖掉{b['sale']:.1f}，几乎是全部持仓的三分之二。单是亏损就让它的权益从二十降到"
        "{b['equity']:.0f}；更高的折扣率让这些权益只能支撑{b['max_assets']:.1f}的资产。百分之十的亏损迫使它卖掉百分之六十。这个算术就是这一部分"
        "每一场危机的发动机。",

    "The arithmetic. <bookmark mark='a'/> Assets are funded":
        "算术。<bookmark mark='a'/>资产由权益和债务提供资金。<bookmark mark='b'/>杠杆是每单位权益对应的资产。<bookmark mark='c'/>所以权益回报等于"
        "杠杆乘以资产回报，再减去债务成本。<bookmark mark='d'/>资产下跌杠杆的倒数，权益就被清零：五倍时是百分之二十；三十倍时，据报道雷曼兄弟在"
        "二〇〇七年底正是这个杠杆，大约是百分之三。",

    "Where the leverage comes from.":
        "杠杆从哪里来。<bookmark mark='a'/>有担保的贷款方借出的钱少于抵押品的价值；差额就是折扣率。<bookmark mark='b'/>所以折扣率把杠杆上限定在"
        "它的倒数。<bookmark mark='c'/>当贷款方紧张时，他们提高折扣率，于是所有持有这种抵押品的加杠杆者必须在同一时刻收缩。",

    "The whole table, for a fund at five times.":
        "五倍杠杆基金的完整表格。<bookmark mark='a'/>没有亏损时，仅仅把折扣率从百分之二十提到百分之三十，就迫使它卖掉三分之一的持仓。"
        "<bookmark mark='b'/>有亏损时，两者相互叠加：下跌百分之十、折扣率百分之四十，基金只能持有现有资产的四分之一。危机中亏损和折扣率一起变动，"
        "所以必须把它们放在一起看。",

    "Hyman Minsky's three kinds of borrower.":
        "海曼·明斯基的三类借款人。<bookmark mark='a'/>对冲性融资：收入足以覆盖利息和本金。<bookmark mark='b'/>投机性融资：收入覆盖利息，本金必须"
        "滚动续借，所以借款人依赖贷款方。<bookmark mark='c'/>庞氏融资：收入两者都覆盖不了，借款人依赖价格上涨。他的观点是，平静的年份会让借款人"
        "沿着这张清单往下走：稳定孕育着不稳定。",

    "Charles Kindleberger's anatomy of a crisis.":
        "查尔斯·金德尔伯格对危机的解剖。<bookmark mark='a'/>一次外部冲击，一项新技术或新政策，打开了获利空间；信贷扩张成繁荣；在狂热中价格跑赢收入。"
        "<bookmark mark='b'/>内部人在困境中卖出，然后所有人在恐慌中抛售。他从南海泡沫开始就发现了同样的五个阶段；这一部分的危机也遵循它们。",

    "John Geanakoplos's leverage cycle.":
        "约翰·吉纳科普洛斯的杠杆周期。<bookmark mark='a'/>当买家看法不一时，价格由买下最后一单位的人决定。<bookmark mark='b'/>折扣率低时，最乐观的人"
        "能借到足够的钱买下全部供给，价格高于平均看法。<bookmark mark='c'/>当坏消息到来、折扣率同时上升，乐观者被清盘，资产转到悲观者手中：价格的"
        "跌幅远大于消息本身。",

    "Two kinds of liquidity.":
        "两种流动性。<bookmark mark='a'/>市场流动性：一笔卖单对价格的影响有多大，第36和第37部分。<bookmark mark='b'/>融资流动性：一个头寸多容易"
        "获得融资，第2和第21部分。<bookmark mark='c'/>它们相互喂养：价格下跌提高保证金，保证金提高迫使抛售，抛售压低价格。",

    "Pause and predict. A leveraged holder owns a large share":
        "暂停并预测。一个加杠杆的持有者占某项资产市场的很大份额。一条消息让价格下跌百分之三。如果它必须维持保证金，而保证金又随价格下跌而上升，"
        "价格最终会跌多少？",

    # ------------------------------------------------------------------ Spirals
    "f'Chapter two, and the answer to the pause:":
        "第2章，以及暂停问题的答案：在这个模型里大约是{100 * r2['fall']:.0f}%，是冲击的{r2['amp']:.0f}倍。单是被迫抛售就让价格下跌"
        "{100 * r0['fall']:.0f}%；随价格下跌而上升的保证金让它跌得更深。马库斯·布伦纳迈尔和拉瑟·佩德森把它们称为损失螺旋和保证金螺旋。",

    "A minimal version, in the House's spiral function.":
        "一个最简版本，就在本系列公司的spiral函数里。<bookmark mark='a'/>一个五倍杠杆的持有者。<bookmark mark='b'/>它的保证金随价格下跌而上升，"
        "上升幅度由kappa决定，kappa衡量贷款方变得多紧张。<bookmark mark='c'/>每一轮它都把头寸削减到权益能支撑的水平，<bookmark mark='d'/>"
        "而它的抛售压低价格，让它仍持有的一切都按更低的价格计值。",

    "Two spirals. <bookmark mark='a'/> The loss spiral:":
        "两种螺旋。<bookmark mark='a'/>损失螺旋：价格下跌缩小权益，持有者为维持杠杆而卖出，卖出再次压低价格。<bookmark mark='b'/>保证金螺旋："
        "面对更大不确定性的贷款方提高保证金，于是杠杆本身必须下降，卖出规模更大。两者在同一个市场、同一时间运转。",

    'f"The price, round by round, after a three percent shock.':
        "百分之三的冲击之后，价格一轮接一轮的变化。<bookmark mark='a'/>保证金不变时，每一轮的卖出都比上一轮少，价格最终停在下跌{fall0:.0f}%的位置。"
        "<bookmark mark='b'/>保证金随价格下跌而上升时，前几轮卖得更多，价格停在下跌{fall2:.0f}%的位置，而且轮数更少。",

    'f"By how nervous the lenders are.':
        "按贷款方的紧张程度来看。<bookmark mark='a'/>保证金固定时，百分之三的冲击变成{100 * r0['fall']:.0f}%，持有者卖掉一百单位中的"
        "{r0['sold']:.0f}。<bookmark mark='b'/>随着保证金越来越敏感，下跌达到{100 * r3['fall']:.0f}%，是消息本身的{r3['amp']:.1f}倍，持有者卖掉"
        "{r3['sold']:.0f}单位：几乎全部，卖进一个正被它自己压低的市场。",

    'f"By the size of the news.':
        "按消息的大小来看。<bookmark mark='a'/>百分之一的冲击：损失螺旋把它变成{100 * a['loss_only']:.0f}%，加上保证金螺旋则是"
        "{100 * a['both']:.0f}%。<bookmark mark='b'/>百分之八的冲击最终是{100 * b['both']:.0f}%。贷款方紧张时，结果几乎不取决于消息的大小："
        "螺旋一旦开始，就会一直转到杠杆耗尽。这是一个临界点，而不是成比例的反应。",

    'f"And by the depth of the market.':
        "以及按市场深度来看。<bookmark mark='a'/>市场相对于被迫卖家越深，螺旋越小：从持有者非常大时的{100 * s['deep'][0]['fall']:.0f}%，"
        "到市场深四倍时的{100 * s['deep'][-1]['fall']:.0f}%。拥挤的交易之所以危险，是因为身在其中的每个人都是那个大持有者。",

    "The evidence. <bookmark mark='a'/> Gary Gorton and Andrew Metrick":
        "证据。<bookmark mark='a'/>加里·戈顿和安德鲁·梅特里克测得，以证券化债券为抵押的回购折扣率从二〇〇七年初接近零，升到二〇〇八年底约百分之"
        "四十五：一场回购挤兑，也就是一个保证金螺旋。<bookmark mark='b'/>期货交易所在波动率跳升后提高保证金；据报道，二〇一一年的白银和二〇二〇年三月"
        "的各个市场里，提高都发生在下跌之中。<bookmark mark='c'/>最难卖出、最难融资的资产跌得最深：这就是安全投资转移。",

    "What stops it. <bookmark mark='a'/> A lender of last resort,":
        "什么能让它停下。<bookmark mark='a'/>最后贷款人，遵循沃尔特·白芝浩的规则：自由放贷，接受优质抵押品，收取惩罚性利率。一家以稳定折扣率接受"
        "这种资产的中央银行，就能打断保证金螺旋。<bookmark mark='b'/>跨周期设定的保证金，这样在萧条时就不必大幅上调。<bookmark mark='c'/>"
        "以及在二〇〇八年和二〇二〇年，中央银行作为最后买家，补上被迫卖家耗尽的市场深度。",

    "Pause and predict. Five banks hold mortgage securities,":
        "暂停并预测。五家银行持有抵押贷款证券、贷款和政府债券，杠杆在十五到三十倍之间。抵押贷款证券下跌百分之五，每家银行都卖出资产来恢复杠杆。"
        "随之而来的甩卖损失，比最初的损失大还是小？",

    # ------------------------------------------------------------------ FireSales
    "f'Chapter three, and the answer to the pause: comparable.":
        "第3章，以及暂停问题的答案：两者相当。最初的损失让五家银行损失了权益的{100 * first / E:.0f}%；它引发的甩卖又损失了"
        "{100 * second / E:.0f}%。对于持有抵押贷款证券很少的银行，甩卖造成的损失比消息本身造成的还大。损失是通过价格传播的，而不是通过它们之间的"
        "任何合约。",

    "Andrei Shleifer and Robert Vishny's insight.":
        "安德烈·施莱弗和罗伯特·维什尼的洞见。<bookmark mark='a'/>当一个行业的资产必须出售时，最看重这些资产的买家正是这个行业自己的公司，"
        "而它们受到了同样的冲击。<bookmark mark='b'/>所以外部人只肯折价买入：一个甩卖价，低于资产在正常时期的价值。<bookmark mark='c'/>"
        "又因为每个持有者都按这个价格给资产估值，一家公司的卖出就是每一家公司的损失。",

    "Robin Greenwood, Augustin Landier and David Thesmar":
        "罗宾·格林伍德、奥古斯丁·兰迪耶和大卫·泰斯马把它做成了模型。<bookmark mark='a'/>资产收益的冲击让每家银行按其持仓比例受损。"
        "<bookmark mark='b'/>以杠杆为目标的银行必须卖出杠杆乘以这笔损失。<bookmark mark='c'/>卖出推动价格，流动性差的资产受影响最大。"
        "<bookmark mark='d'/>于是每家持有这些资产的银行再亏一次，不管它有没有卖。",

    "Five stylised banks.":
        "五家典型化的银行。<bookmark mark='a'/>每家按不同比例持有抵押贷款证券、贷款和政府债券，杠杆在十五到三十倍之间。<bookmark mark='b'/>"
        "D银行杠杆最高，对抵押贷款的敞口最大；C银行主要持有政府债券。抵押贷款证券是流动性差的资产：卖出它们对价格的冲击是卖出债券的十倍。",

    'f"A five percent fall in mortgage securities.':
        "抵押贷款证券下跌百分之五。<bookmark mark='a'/>以十亿计的首轮损失与抵押贷款持仓成正比。<bookmark mark='b'/>为了恢复杠杆，银行卖出这些损失"
        "的十五到三十倍：总共{total:,.0f}十亿。<bookmark mark='c'/>卖出进一步压低价格，每家银行又亏一次。E银行因消息亏了{-f['first'][e_i]:.1f}十亿，"
        "又因别人的抛售亏了{-f['second'][e_i]:.1f}十亿。",

    'f"One number for the system.':
        "给整个体系的一个数字。<bookmark mark='a'/>总体脆弱度：甩卖损失占所有银行权益的比例。<bookmark mark='b'/>这里是{100 * f['AV']:.0f}%，"
        "来自一种资产百分之五的变动。<bookmark mark='c'/>如果这种资产难卖一倍，就是{100 * f['AV_double']:.0f}%。格林伍德、兰迪耶和泰斯马把它用在"
        "了二〇一一年欧洲银行持有的主权债上。",

    "In the data. <bookmark mark='a'/> Joshua Coval and Erik Stafford":
        "数据中的证据。<bookmark mark='a'/>约书亚·科瓦尔和埃里克·斯塔福德发现，遭遇资金流出的共同基金会卖出它们已经持有的股票，这些股票下跌，然后在"
        "随后几个月里回升。<bookmark mark='b'/>回升本身就是证据：能回来的价格不是信息，而是流动性，代价由被迫卖家支付。<bookmark mark='c'/>"
        "它一再重演：第38部分里二〇二〇年三月的债券基金，第21部分里Archegos的大宗抛售。",

    "The broader lesson. <bookmark mark='a'/> Common holdings are a network:":
        "更广的教训。<bookmark mark='a'/>共同持仓就是一张网络：两家从不互相借贷的银行，只要持有相同的资产就联系在一起，拉玛·孔特和埃里克·沙宁称之为"
        "价格传导的传染。<bookmark mark='b'/>所以分散化反而可能带来集中：如果每家银行都分散投资到同样的资产上，单独看每家都更安全，合起来却都暴露于"
        "同一场甩卖。<bookmark mark='c'/>一家银行自己的压力测试看不到别人的抛售；体系的压力测试必须把它们包括进来。",

    "Pause and predict. Ten banks each owe the others six dollars":
        "暂停并预测。十家银行各自总共欠其他银行六美元，各有半美元的缓冲。一号银行遭受损失。每家银行欠其他九家每家一点，还是只欠它的邻居，哪种体系"
        "更安全？",

    # ------------------------------------------------------------------ Networks
    "Chapter four, and the answer to the pause: it depends on the size of the loss.":
        "第4章，以及暂停问题的答案：取决于损失的大小。在某个阈值以下，完全连接的体系最安全：只有第一家银行倒下，因为它的缺口被薄薄地分摊了。"
        "超过这个阈值，同一个体系会一下子全部倒下，而环形体系是一家接一家地倒下。达龙·阿西莫格鲁、阿苏曼·奥兹达格拉尔和阿里礼萨·塔赫巴兹-萨利希"
        "称之为相变。",

    "How interbank payments clear, after Larry Eisenberg and Thomas Noe.":
        "银行间支付如何清算，依照拉里·艾森伯格和托马斯·诺伊的模型。<bookmark mark='a'/>每家银行对其他银行有一笔总欠款。<bookmark mark='b'/>"
        "违约者按所欠比例向债权人支付。<bookmark mark='c'/>每家银行要么全额支付，要么付出它拥有的全部：外部资产加上其他银行付给它的钱。清算向量同时"
        "满足每家银行的方程。",

    'f"Five banks. <bookmark mark=\'a\'/> Arrows are debts,':
        "五家银行。<bookmark mark='a'/>箭头是债务，越粗越大；每家银行还持有一些外部资产。<bookmark mark='b'/>虚拟违约算法先假设所有人都付款，"
        "找出付不了的，重新计算，然后停下：这里用了{n['rounds']}轮。外部资产很少的A银行在它欠的{pbar[0]:.0f}中支付了{p[0]:.1f}；缺口传给它的"
        "债权人，由他们吸收。",

    "A sharper version. <bookmark mark='a'/> Each bank holds a project worth a,":
        "一个更锐利的版本。<bookmark mark='a'/>每家银行持有一个价值为a的项目，先欠外部优先债权人v，再欠其他银行y；一家银行受到冲击epsilon。"
        "<bookmark mark='b'/>a减v是每家银行的缓冲。<bookmark mark='c'/>同样的银行间总债务可以排成环形，每家只欠邻居；排成完全网络，每家欠其他所有"
        "银行一点；或者排成几个簇。",

    'f"Ten banks, each owing six to the others':
        "十家银行，各自欠其他银行六，缓冲半美元。<bookmark mark='a'/>在环形网络里，违约随冲击一步步增加：每一次倒闭都把损失传给下一家。"
        "<bookmark mark='b'/>在完全网络里，什么都不扩散，直到冲击超过五，然后十家一起倒下。",

    "Why exactly five.":
        "为什么恰好是五。<bookmark mark='a'/>冲击超过一号银行自己的缓冲时，它就倒下。<bookmark mark='b'/>它付不出的部分由九个债权人平均分摊。"
        "<bookmark mark='c'/>每个债权人在分到的份额超过自己的缓冲时倒下，而这对所有人发生在同一个冲击上：n乘以缓冲，也就是五。分摊是安全的，"
        "直到分摊的损失同时超过每一个缓冲。",

    'f"And a third arrangement: two clusters of five,':
        "还有第三种排列：两个各五家的簇，每家只把百分之二的放款投向另一个簇。<bookmark mark='a'/>对于大冲击它表现最好：最多{d_max}家倒下，"
        "也就是一个簇，因为微弱的联系传过去的太少，推不倒另一个簇。阿西莫格鲁和合作者证明了：面对大冲击，弱连接的体系最稳定；面对小冲击，连接最紧密的"
        "体系最稳定。",

    "And real networks. <bookmark mark='a'/> They are core and periphery:":
        "以及真实的网络。<bookmark mark='a'/>它们是核心—边缘结构：少数大型交易商与所有人相连，对随机倒闭很稳健，对枢纽倒闭很脆弱。"
        "<bookmark mark='b'/>据综述报道，用监管机构的银行间数据所做的模拟发现，单靠直接传染很少造成大的损失：真正伤人的是它与甩卖和挤兑的组合。"
        "<bookmark mark='c'/>而中央清算，第21部分，把许多双边联系换成了每个市场一个枢纽。",

    "Pause and predict. Three financial industries:":
        "暂停并预测。三个金融行业：银行、保险公司和其他金融机构。在股灾中，对市场最重要的是哪一个：跌得最多的那个，还是陷入困境时最能拖动市场的"
        "那个？",

    # ------------------------------------------------------------------ Systemic
    'f"Chapter five, and the answer to the pause: they are different questions.':
        "第5章，以及暂停问题的答案：这是两个不同的问题。在市场最糟糕的日子里，其他金融机构跌得最多，平均{100 * abs(f['Fin']['mes']):.1f}%，"
        "保险公司跌得最少，{100 * abs(f['Insur']['mes']):.1f}%。但当保险公司自身陷入困境时，市场自己的最坏情形恶化得比银行陷入困境时更厉害。"
        "对危机的暴露和对危机的贡献，需要两种度量。",

    "Tobias Adrian and Markus Brunnermeier's CoVaR.":
        "托比亚斯·阿德里安和马库斯·布伦纳迈尔的CoVaR。<bookmark mark='a'/>在某个机构自身陷入困境的条件下，整个体系的在险价值。"
        "<bookmark mark='b'/>它来自体系收益对机构收益的分位数回归，用的是第40部分的弹球损失。<bookmark mark='c'/>而delta CoVaR是从机构的正常状态"
        "到困境状态的变化：这家机构出事时，体系的尾部会恶化多少。",

    'f"On thirty years of American data, with industries standing in for firms.':
        "用三十年的美国数据，以行业代替单个公司。<bookmark mark='a'/>delta CoVaR：银行陷入困境让市场的5%分位数移动"
        "{100 * s['full']['Banks']['dcovar']:.2f}%，保险公司{100 * s['full']['Insur']['dcovar']:.2f}%，其他金融机构"
        "{100 * s['full']['Fin']['dcovar']:.2f}%。<bookmark mark='b'/>而边际预期亏损，即每个行业在市场最糟糕的日子里跌多少，给出了不同的排序："
        "保险公司跌得最少，但它们的困境对市场尾部的拖动比银行的困境更大。",

    'f"Over time, in two-year windows.':
        "随时间变化，按两年窗口计算。<bookmark mark='a'/>三者在平静年份都很安静，在危机中一起骤降：最深的读数{100 * worst:.1f}%出现在二〇〇八年"
        "前后的窗口里。<bookmark mark='b'/>用市场价格构建的系统性度量是在危机到来时看见它，所以它更像一支温度计，而不是一个预测。",

    "The other side: exposure.":
        "另一面：暴露。<bookmark mark='a'/>边际预期亏损是一个机构在体系最糟糕的日子里的平均收益，也就是第40部分的欧拉贡献。<bookmark mark='b'/>"
        "它的长期版本近似六个月内、在一场百分之四十的崩盘中的损失：一减e的负十八倍MES次方。<bookmark mark='c'/>一家在市场坏日子里亏百分之三的公司，"
        "在危机中大约亏五分之二。",

    "Christian Brownlees and Robert Engle turned it into a capital number.":
        "克里斯蒂安·布朗利斯和罗伯特·恩格尔把它变成了一个资本数字。<bookmark mark='a'/>SRISK是一家公司在危机之后会短缺的资本：债务的百分之八，"
        "减去危机之后它的权益还值多少。<bookmark mark='b'/>审慎比率取百分之八。<bookmark mark='c'/>对所有公司加总，就是体系在最无法筹资的时刻所需要"
        "的资本。",

    'f"Lehman Brothers, at the end of twenty oh seven.':
        "雷曼兄弟，二〇〇七年底。<bookmark mark='a'/>据报道，六千九百一十亿美元的资产，对应二百二十五亿的权益：三十一倍。<bookmark mark='b'/>"
        "以那一年金融股的MES作为替代：{100 * r['mes']:.1f}%。<bookmark mark='c'/>隐含的危机损失是{100 * r['lrmes']:.0f}%。<bookmark mark='d'/>"
        "SRISK约为{r['srisk']:.0f}十亿美元：在它倒闭前十个月，资本缺口约为其权益的两倍。",

    "In policy. <bookmark mark='a'/> Since twenty eleven the Financial Stability Board":
        "在政策中。<bookmark mark='a'/>从二〇一一年起，金融稳定理事会每年依据五项指标点名全球系统重要性银行：规模、关联性、可替代性、复杂性和跨境活动。"
        "<bookmark mark='b'/>每一档都附加资本要求，从一个到三个半百分点。<bookmark mark='c'/>而SRISK这样的市场度量为上市公司公开发布，是对官方名单的"
        "一种公开检验。",

    "Their limits. <bookmark mark='a'/> Measures from market prices rise with the crisis,":
        "它们的局限。<bookmark mark='a'/>来自市场价格的度量随危机上升，而不是在危机之前：它们说明谁暴露其中，很少说明何时。<bookmark mark='b'/>"
        "高delta CoVaR可能意味着一家公司传播困境，也可能只是它与所有人共享相同的暴露。<bookmark mark='c'/>而且只有上市公司能被度量：基金、影子银行和"
        "私募信贷没有每日价格，而这正是二〇二〇年和二〇二三年的盲点。",

    "Pause and predict. In early nineteen ninety-eight a hedge fund":
        "暂停并预测。一九九八年初，一家对冲基金以四十七亿美元的资本持有约一千二百五十亿美元的资产，主要是押注利差会收窄的交易。多大的变动会让它清零，"
        "谁又不得不卖出？",

    # ------------------------------------------------------------------ LTCM
    "f'Chapter six, and the answer to the pause:":
        "第6章，以及暂停问题的答案：据报道，以{x['lev']:.0f}倍杠杆，资产损失约{100 * x['wipe']:.1f}%就够了。卖家将是所有持有相同交易的人，以及"
        "以这些交易为抵押放贷的银行：这就是为什么美联储把贷款方召集到一起，而不是任由他们挤兑。第10部分讲了这家基金的故事；这一章讲它的机制。",

    'f"The book, as reported in nineteen ninety-nine.':
        "账簿，依据一九九九年的报告。<bookmark mark='a'/>四十七亿美元的资本，对应一千二百五十亿美元的资产：<bookmark mark='b'/>大约{x['lev']:.0f}倍。"
        "<bookmark mark='c'/>外加约一万二千五百亿美元的衍生品，几乎没有初始保证金。<bookmark mark='d'/>而交易都是收敛押注：相似证券之间很小的利差，"
        "靠杠杆才值得去做。",

    "Why it failed together.":
        "为什么一起失败。<bookmark mark='a'/>交易商自己的交易台和其他基金持有类似的头寸，所以这些利差很拥挤。<bookmark mark='b'/>据报道，一九九八年八月"
        "俄罗斯违约，把投资者赶向流动性最好的证券，每一个收敛利差同时扩大。<bookmark mark='c'/>看起来分散在各国各市场的头寸，其实是同一个押注流动性"
        "的赌注：共同持仓，加上一个螺旋。",

    'f"One of the spreads, from public data.':
        "其中一个利差，来自公开数据。<bookmark mark='a'/>Baa级公司债相对十年期国债的收益率差，八月初在{x['baa']['pre']:.1f}个百分点附近。"
        "<bookmark mark='b'/>到十月，它达到{x['baa']['max']:.1f}，而国债收益率随着投资者涌入降到{x['y10']['min']:.2f}%：这就是每一笔收敛交易都在"
        "做空的安全投资转移。",

    "The resolution. <bookmark mark='a'/> On the twenty-third of September, fourteen banks,":
        "结局。<bookmark mark='a'/>九月二十三日，在纽约联储召集下，十四家银行投入三十六亿美元换取基金百分之九十的股份；据美联储的国会证词，没有借出"
        "任何公共资金。<bookmark mark='b'/>它们同意，是因为一次性清算整本账簿会迫使它们所有人把同样的头寸卖进同一个市场：一场协调起来避免了的甩卖。"
        "<bookmark mark='c'/>美联储在那个秋天三次降息，这个先例被争论了十年。",

    "Three lessons. <bookmark mark='a'/> Leverage turns small risks into large ones:":
        "三条教训。<bookmark mark='a'/>杠杆把小风险变成大风险：资产一个很少变动百分之四的百分之四变动，就终结了这家基金。<bookmark mark='b'/>"
        "每个贷款方只看得到账簿中属于自己的那一块，这正是第21部分主张保证金和清算的理由。<bookmark mark='c'/>流动性是一个共同因子：许多看似独立的押注"
        "是同一个融资押注，而用平静年份拟合的VaR看不见它。",

    "Pause and predict. The TED spread,":
        "暂停并预测。TED利差，即三个月期银行间拆借利率与国库券之间的差，在二〇〇七年之前平均不到半个百分点。它在二〇〇八年十月升到多高，它衡量的是"
        "什么？",

    # ------------------------------------------------------------------ GFC
    "f'Chapter seven, and the answer to the pause:":
        "第7章，以及暂停问题的答案：二〇〇八年十月十日，{t['max']:.2f}个百分点，而二〇〇六年的中位数是{t['pre']:.2f}。TED利差衡量银行之间相互借贷时"
        "比无风险利率多收多少：它们彼此有多信任。那个秋天，它们几乎不再信任。",

    "The structure. <bookmark mark='a'/> Mortgages pooled into securities":
        "结构。<bookmark mark='a'/>抵押贷款被打包成证券，再切成分级，即第20部分的信用模型。<bookmark mark='b'/>由交易商、表外通道和投资工具以及"
        "货币基金持有：银行之外的银行体系。<bookmark mark='c'/>用回购和商业票据做短期融资，没有存款保险，也没有最后贷款人。<bookmark mark='d'/>"
        "再用信用违约互换来保险，卖方包括AIG这样只有在被降级时才需要缴纳抵押品的公司。",

    'f"Two spreads from FRED.':
        "来自FRED的两个利差。<bookmark mark='a'/>TED利差：二〇〇七年八月第一次跳升，那时法国巴黎银行冻结了三只持有抵押贷款证券的基金；第二次在"
        "贝尔斯登前后；然后是雷曼之后的尖峰。<bookmark mark='b'/>以及Baa公司债利差，从约{g['baa']['pre']:.1f}到{g['baa']['max']:.1f}个百分点："
        "先是融资压力，然后是信用。",

    "The sequence, from the public record.":
        "依据公开记录的时间线。<bookmark mark='a'/>二〇〇七年八月：法国巴黎银行冻结三只基金，银行间利率跳升。<bookmark mark='b'/>二〇〇八年三月："
        "贝尔斯登无法续做回购，在美联储支持下被出售给摩根大通。<bookmark mark='c'/>九月：政府接管房利美和房地美，雷曼在十五日申请破产。"
        "<bookmark mark='d'/>第二天，AIG的追加抵押品要求换来美联储八百五十亿美元的贷款，一只货币市场基金跌破面值。<bookmark mark='e'/>十月，"
        "公共资本注入和担保。",

    "Two failures, two mechanisms.":
        "两次倒闭，两种机制。<bookmark mark='a'/>据报道，雷曼的杠杆约为三十一倍，大量融资是隔夜的，它在一个周末之内失去了贷款方，它的倒闭冻结了"
        "伦敦主经纪业务客户的资产。<bookmark mark='b'/>AIG为数千亿美元的优先级分级出售了保护；降级和价格下跌触发了它无法满足的追加抵押品要求。"
        "<bookmark mark='c'/>两者都是第1章的算术：单薄的权益，以及贷款方恰恰在权益最稀缺时要求更多。",

    "And the run spread to cash itself.":
        "挤兑还蔓延到了现金本身。<bookmark mark='a'/>货币市场基金承诺每份稳定在一美元，每天可赎回：这就是二〇〇八年版的第39部分稳定币。"
        "<bookmark mark='b'/>储备主要基金持有雷曼的商业票据，把它减记为零，跌破了面值。<bookmark mark='c'/>投资者在一周内从优质基金撤出数千亿美元，"
        "这些基金停止购买商业票据，企业失去了融资，直到财政部为货币基金提供担保。",

    "The response. <bookmark mark='a'/> The Fed lent to dealers,":
        "应对。<bookmark mark='a'/>美联储向交易商、货币基金和商业票据发行人放贷，然后直接买入抵押贷款证券：先是最后贷款人，然后是最后买家。"
        "<bookmark mark='b'/>各国政府向银行注资，从二〇〇九年起，压力测试告诉市场每家银行需要多少资本。<bookmark mark='c'/>以及随后的规则："
        "巴塞尔协议三的资本和流动性比率、中央清算、处置计划，以及对系统重要性银行的附加资本。",

    "Pause and predict. Between the ninth and the eighteenth of March twenty twenty,":
        "暂停并预测。二〇二〇年三月九日到十八日之间，美国股市大跌。世界上最安全的资产，十年期美国国债，它的收益率发生了什么，为什么？",

    # ------------------------------------------------------------------ Dash
    "f'Chapter eight, and the answer to the pause: it rose,":
        "第8章，以及暂停问题的答案：它上升了，从三月九日的{y['m9']:.2f}%升到十八日的{y['m18']:.2f}%，同时股市在下跌。在通常的恐慌中，国债是"
        "所有人都买的东西。而在这一次，有一个星期，所有人需要现金胜过需要安全，于是卖掉了手里流动性最好的东西。",

    'f"Two charts from public data.':
        "两张来自公开数据的图。<bookmark mark='a'/>右边是美国股市：在低点时比二月初下跌了约{drop:.0f}%。<bookmark mark='b'/>左边是十年期国债"
        "收益率。整个二月它在下降，这很正常：安全投资转移。<bookmark mark='c'/>然后，在三月九日到十八日这一周，股市继续下跌，它却上升了。安全资产"
        "正在被抛售。",

    "Who sold, as the official post-mortems describe it.":
        "谁在卖，依照官方事后报告的描述。<bookmark mark='a'/>外国中央银行，卖出国债换取捍卫本币所需的美元。<bookmark mark='b'/>面临赎回的债券基金，"
        "卖出它们能最快卖掉的资产。<bookmark mark='c'/>加杠杆的基金平掉国债基差交易。<bookmark mark='d'/>而本该买入的交易商受杠杆比率约束，"
        "这一比率把国债当作和其他资产一样的资产来计算：第1章的约束，落在了做市商身上。",

    "The basis trade, a descendant of LTCM's book.":
        "基差交易，长期资本管理公司那本账簿的后代。<bookmark mark='a'/>做多现券国债，用回购以很高的杠杆融资。<bookmark mark='b'/>做空它的期货合约；"
        "期货价格偏高，因为资产管理人想要敞口而不占用资产负债表。<bookmark mark='c'/>利差只有几个基点：第9部分的期现套利。<bookmark mark='d'/>"
        "风险不在债券本身，而在折扣率和保证金，它们一起上升，于是这笔交易不得不在最糟糕的时刻在现券市场上卖掉。",

    'f"Funding stress, again.':
        "又是融资压力。<bookmark mark='a'/>三个月期商业票据利率从二月中旬的{cp['pre']:.2f}%升到{cp['max']:.2f}%，而美联储正把利率降到零："
        "一个已经停止运转的市场。<bookmark mark='b'/>Baa信用利差大约翻倍，达到{baa['max']:.2f}个百分点。优质货币基金又在几天内流失了数十亿美元，"
        "就像二〇〇八年一样。",

    "The response came in days, not months.":
        "应对以天计，而不是以月计。<bookmark mark='a'/>十五日：利率降到零，七千亿美元的购买，更便宜的美元互换额度。<bookmark mark='b'/>然后，"
        "二〇〇八年的那些便利工具在两天内重新启用。<bookmark mark='c'/>二十三日，按所需的任何数量购买，并且第一次购买公司债。<bookmark mark='d'/>"
        "一个回购便利工具，让外国中央银行可以用国债抵押借款，而不必卖出。<bookmark mark='e'/>以及杠杆比率的豁免，让交易商能够持有国债。收益率回落，"
        "股市在二十三日见底。",

    "Set against twenty oh eight.":
        "与二〇〇八年对照。<bookmark mark='a'/>挤兑发生在不同的地方：二〇二〇年，在国债本身。<bookmark mark='b'/>没有人承担损失；这是一次纯粹的"
        "流动性冲击。<bookmark mark='c'/>起约束作用的是交易商的资产负债表，而不是银行资本。<bookmark mark='d'/>又因为应对是即时且无上限的，它只持续了"
        "大约两周，而不是十八个月。正如美联储官员所说，他们得出的教训是国债市场的结构本身需要改革，国债的中央清算正在推进。",

    "Pause and predict. From the middle of twenty fourteen, China's Shanghai Composite":
        "暂停并预测。从二〇一四年年中开始，中国的上证综合指数在一年内涨了一倍多，大量买入是用借来的钱完成的。它跌了多少，跌得多快？",

    # ------------------------------------------------------------------ China
    "f'Chapter nine, and the answer to the pause:":
        "第9章，以及暂停问题的答案：上证综指从二〇一五年六月十二日的高点{x['peak']:,.0f}，在十一周里下跌了{100 * -x['fall']:.0f}%，"
        "到八月二十六日的{x['low']:,.0f}。上涨的路上很大一部分是用融资买的；下跌的路上很大一部分是追加保证金。",

    'f"The index, from public data.':
        "指数，来自公开数据。<bookmark mark='a'/>从二〇一四年七月的约{x['start']:,.0f}，它在十一个月里上涨了{100 * x['rise']:.0f}%。"
        "<bookmark mark='b'/>然后在不到三个月里跌去四成以上，其中有单日百分之八的下跌。<bookmark mark='c'/>二〇一六年第一周又有两次："
        "{r1:.1f}%和{r2:.1f}%，那是熔断的日子。",

    "How the boom was financed.":
        "这轮牛市的资金从哪里来。<bookmark mark='a'/>券商的融资余额超过了两万亿元。<bookmark mark='b'/>在它周围还有一个灰色市场：伞形信托和配资平台"
        "给散户五到十倍的杠杆，并自动平仓。卞、何、薛和周后来逐个账户地追踪了它。<bookmark mark='c'/>六月，监管机构着手清理场外配资。"
        "<bookmark mark='d'/>剩下的就是第3章，只不过门上加了锁：被迫卖出撞上百分之十的跌停板，卖不掉一只股票的人就去卖另一只，抛售随之扩散。",

    "The response, as reported.":
        "据报道的应对。<bookmark mark='a'/>“国家队”：由国家支持的买家，通过证券金融公司获得中央银行资金。<bookmark mark='b'/>大股东被禁止减持，"
        "新股发行暂停。<bookmark mark='c'/>七月初，约一半上市公司停牌。如果你卖不掉你持有的东西，第3章说你就卖你能卖的：仍在交易的股票，以及海外市场。",

    "And the circuit breaker.":
        "还有熔断机制。<bookmark mark='a'/>从二〇一六年第一个交易日起：沪深三百指数下跌百分之五，暂停交易十五分钟；<bookmark mark='b'/>下跌百分之七，"
        "当天收市。<bookmark mark='c'/>一月四日，两个阈值在几分钟内先后触发。<bookmark mark='d'/>一月七日，开盘不到半小时就收市了，当晚这项规则被暂停。",

    "Why a breaker can pull prices toward itself.":
        "为什么熔断会把价格吸向自己。<bookmark mark='a'/>暂停之后你就卖不了。<bookmark mark='b'/>所以当价格接近阈值时，一个可能需要卖出的交易者应该"
        "现在就卖，趁门还没关上。<bookmark mark='c'/>而他们的卖出把价格推向阈值：这就是磁吸效应，萨布拉马尼亚姆在一九九四年建立了模型，陈、彼图霍夫和"
        "王也以中国的这段经历为背景建模。<bookmark mark='d'/>设计上的教训：阈值相距要远，而且是暂停而不是收市。美国的熔断设在百分之七、十三和二十。",

    "Pause and predict. In twenty twenty-two the Federal Reserve raised rates":
        "暂停并预测。二〇二二年，美联储以四十年来最快的速度加息。一家银行的长期债券账面价值一百，现在只值八十五，而它欠存款人九十。如果存款人离开，"
        "会发生什么？",

    # ------------------------------------------------------------------ Y2023
    "Chapter ten, and the answer to the pause. At fair value":
        "第10章，以及暂停问题的答案。按公允价值，这家银行有八十五对九十：权益是负五，尽管账面上是正十。只要存款人不走，它就能把债券持有到期，损失永远"
        "不会出现。如果他们离开，它就必须以八十五卖出，损失变成现实。这就是硅谷银行，也是最安全的资产能让一家银行沉没的原因。",

    "First, London, September twenty twenty-two.":
        "先看伦敦，二〇二二年九月。<bookmark mark='a'/>英国的养老金计划通过负债驱动投资基金对冲它们的长期负债：长期金边债券和互换，用回购加杠杆。"
        "<bookmark mark='b'/>一份含有无资金来源减税的“迷你预算”让三十年期收益率在几天内上升了一个多百分点。<bookmark mark='c'/>这些基金面临追加"
        "抵押品要求，卖出金边债券来满足，又把收益率推得更高：政府债券里的保证金螺旋。<bookmark mark='d'/>二十八日，英格兰银行买入长期金边债券，持续"
        "十三天，把它止住。",

    'f"Silicon Valley Bank, from its annual report':
        "硅谷银行，依据它的年报和美联储的审查报告。<bookmark mark='a'/>{s['deposits']:.0f}十亿美元的存款，大部分超过受保上限，来自科技公司和它们的"
        "投资人。<bookmark mark='b'/>{s['htm_book']:.1f}十亿美元持有至到期的债券，按成本入账，二〇二二年底价值{s['htm_fair']:.1f}十亿。"
        "<bookmark mark='c'/>损失{s['loss']:.1f}十亿，几乎等于它{s['equity']:.1f}十亿的全部权益。<bookmark mark='d'/>当它宣布卖债亏损和增发股票时，"
        "一天之内流出{s['out_9mar']:.0f}十亿，第二天早上还有更多的提款请求，它在十日被关闭。",

    'f"Diamond and Dybvig, nineteen eighty-three, with a fire sale.':
        "戴蒙德和迪布维格，一九八三年，加上甩卖。银行的资产如果持有，每单位值theta，如果提前卖出，只值r。每个存款人现在都可以取出一。"
        "<bookmark mark='a'/>如果有比例f的人提款，提前走的人拿到一，直到f等于r时银行耗尽。<bookmark mark='b'/>等待的人分剩下的：theta乘以一减f除以r，"
        "再除以一减f。随f下降，f达到r时为零。<bookmark mark='c'/>两个均衡。如果没人挤兑，等待得到{th:.1f}，没人应该挤兑。<bookmark mark='d'/>"
        "如果所有人都挤兑，等待什么也得不到，所有人都应该挤兑。同一家银行，同样的资产：结果只取决于存款人对彼此的预期。",

    'f"Which equilibrium? Carlsson and van Damme':
        "哪一个均衡？卡尔松和范达姆的全局博弈回答了它，莫里斯和申、戈尔茨坦和保兹纳把它用到了挤兑上。给每个存款人一个关于theta的、略带噪声的信号。"
        "<bookmark mark='a'/>于是只有一个均衡：低于阈值theta星就挤兑，高于它就留下。在阈值处，边际存款人对有多少人挤兑的不确定是均匀分布的，这使得"
        "theta星成为这个积分的根。<bookmark mark='b'/>r取{q['r']:.2f}，大致是硅谷银行债券的情况，theta星是{q['thr85']:.2f}：一家资产价值高达"
        "{q['thr85']:.2f}的有偿付能力的银行仍会遭到挤兑。<bookmark mark='c'/>为一半存款提供保险，它就降到{q['thr85_half']:.2f}。"
        "<bookmark mark='d'/>本系列公司也检验了这个极限：把噪声从零点三降到零点零一来求解博弈，阈值从{n[0]:.2f}上升到{n[3]:.2f}，收敛到公式。",

    'f"The system\'s view, from FRED.':
        "体系的视角，来自FRED。<bookmark mark='a'/>两年期国债收益率，从二〇二二年初的{x['y2']['start']:.2f}%升到{x['y2']['max']:.2f}%："
        "四十年来最快的上升，之前买入的每一张债券都被减值。<bookmark mark='b'/>美国商业银行的存款全年都在下降，在截至二〇二三年三月二十二日的三周里"
        "又减少了{drop:.0f}十亿美元，资金流向最大的银行和支付新利率的货币基金。",

    "The run spread, as reported.":
        "据报道，挤兑在扩散。<bookmark mark='a'/>签名银行在三月十二日被关闭；第一共和银行流失了超过一千亿美元的存款，在五月一日被出售给摩根大通。"
        "<bookmark mark='b'/>在苏黎世，经历多年亏损和丑闻的瑞士信贷也遭遇资金流出，十九日瑞士当局安排它以三十亿瑞郎出售给瑞银。<bookmark mark='c'/>"
        "它约一百六十亿瑞郎的额外一级资本债，本是用来吸收损失的或有资本，被减记为零，而股东却拿到了一些东西；这依据的是一项紧急法令，此后一直在法庭上"
        "受到挑战。",

    "And the policy answer was the model's.":
        "而政策的回答正是模型的回答。<bookmark mark='a'/>两家倒闭银行的每一笔存款都得到担保：受保比例在事后被设为一。<bookmark mark='b'/>美联储新的"
        "定期融资计划按面值而不是市值接受国债抵押：甩卖价值r被设为一。<bookmark mark='c'/>而悬而未决的问题在银行之外：养老金、货币基金和基差交易者，"
        "监管者称之为非银行金融中介，这一部分的许多压力正是从那里开始的。",

    "Pause and predict. The House runs its strategies at about two times leverage,":
        "暂停并预测。本系列公司以大约两倍的杠杆运行它的策略，由一家主经纪商提供融资。如果主经纪商在二〇〇八年最糟糕的那一天把保证金加倍，"
        "本系列公司必须卖掉什么，它能在一天之内卖掉那么多吗？",

    # ------------------------------------------------------------------ House
    'f"The answer to the pause. <bookmark mark=\'a\'/> The worst day of twenty oh eight':
        "暂停问题的答案。<bookmark mark='a'/>二〇〇八年美国市场最糟糕的一天是十二月一日：{100 * -h['worst']:.2f}%。假设整个账簿都像市场一样变动。"
        "<bookmark mark='b'/>在两倍杠杆下，权益从一降到{s2['equity']:.2f}。<bookmark mark='c'/>保证金从四分之一加倍到一半，主经纪商最多只为它的"
        "两倍提供融资。<bookmark mark='d'/>所以本系列公司必须卖掉账簿的{100 * s2['sale_frac']:.0f}%。如果每个头寸是半天的成交量，以成交量的十分之一"
        "来卖，大约需要{h['days2']:.1f}天。它能做到。",

    "Chapter eleven. The House's forty-first rule":
        "第11章。本系列公司的第41条规则属于它的资金与融资部门。这一部分追踪的公司，大多数在账面上看起来有偿付能力，却无法为自己融资一个星期。这条规则是一项"
        "每天都运行的流动性压力测试。",

    'f"The House\'s stress, by leverage.':
        "按杠杆看本系列公司的压力测试。<bookmark mark='a'/>保证金不变时，最糟糕的那一天在大约三倍以下不会迫使任何卖出。<bookmark mark='b'/>"
        "保证金加倍时，被迫卖出从略低于两倍处开始，并急剧上升。保证金翻三倍时，更加陡峭。<bookmark mark='c'/>虚线是本系列公司一天之内以成交量的十分之一"
        "能卖出的量，每个头寸为半天的成交量。<bookmark mark='d'/>加倍的那条曲线在刚过{h['lev_max']:.0f}倍处穿过它：这就是本系列公司的杠杆上限。",

    'f"Against a real case.':
        "对照一个真实案例。<bookmark mark='a'/>据报道，家族办公室Archegos通过几家主经纪商的总收益互换持有高度集中的头寸，每家都只看得到自己的那一块："
        "长期资本管理公司的教训，没有被吸取。<bookmark mark='b'/>以五倍杠杆、每个头寸五天成交量来运行本系列公司的压力测试：要卖掉账簿的"
        "{100 * s5['sale_frac']:.0f}%，需要{h['days5']:.0f}天。<bookmark mark='c'/>二〇二一年三月，当它的一只股票下跌时，银行们没有等待。它们争先"
        "大宗抛售；瑞士信贷报告了五十五亿美元的损失；创始人后来被判欺诈罪成立。",

    'f"Now through the whole of twenty oh eight and oh nine,':
        "现在用市场的真实收益，按天走完整个二〇〇八年和〇九年，杠杆两倍。主经纪商设定保证金有两种方式。<bookmark mark='a'/>与近期波动率挂钩：平静时"
        "{100 * h['h0']:.0f}%，随RiskMetrics波动率上升。本系列公司在两年里被迫卖出期初权益的{p2['pro_sold']:.2f}倍，其中{pct_fall:.0f}%发生在"
        "二〇〇九年三月低点之前。<bookmark mark='b'/>或者跨周期设定，从一开始就足以应对压力年份：{100 * h['h_ttc'][0]:.0f}%，在两倍杠杆下从不触发。"
        "完全没有被迫卖出。<bookmark mark='c'/>再注意一个转折。被迫卖出的一方最后的权益反而更多，{p2['pro_end']:.2f}对{p2['ttc_end']:.2f}："
        "在下跌中卖出保护了卖家。",

    "Which is the whole problem of this part, in one result.":
        "这一个结果就是这一部分的全部问题。<bookmark mark='a'/>对每家公司来说，在下跌中卖出是审慎的：与波动率挂钩的保证金保护了主经纪商，这里也保护了"
        "基金。<bookmark mark='b'/>但在这个草图里，本系列公司是价格接受者。当所有加杠杆的持有者一起卖出时，他们的卖出就是下跌本身。<bookmark mark='c'/>"
        "没有一个卖家会计算自己的卖出给别人的抵押品造成的损失，洛伦佐尼和斯坦因把这一点形式化了。这就是为什么欧洲的中央对手方现在必须限制保证金随"
        "波动率摆动的幅度。",

    'f"So the forty-first rule has four parts.':
        "所以第41条规则有四个部分。<bookmark mark='a'/>总杠杆至多{h['lev_max']:.0f}倍：在这个水平上，有记录以来最糟糕的一天加上保证金加倍，不会迫使"
        "本系列公司做出一天之内做不到的卖出。<bookmark mark='b'/>定期融资：保证金条款锁定至少三十天，分布在三家或更多主经纪商。<bookmark mark='c'/>"
        "现金缓冲至少等于保证金加倍时额外需要的部分。<bookmark mark='d'/>以及不只一扇门：没有一个头寸超过半天的成交量。",

    "The House's code. The forced sale is four lines:":
        "本系列公司的代码。被迫卖出只有四行：亏损、新的权益、贷款方最多愿意融资的量，以及两者之差。每日路径先加上收益，再把账簿设为目标和保证金允许量中"
        "较小的那个，并把差额记为被迫卖出。",

    "And Chapter ten's run. The payoffs:":
        "还有第10章的挤兑。收益：银行卖出f除以r个单位来支付离开的人，只要还能支付就全额支付，剩下的由等待的人分享。阈值是等待与挤兑之间平均差距的根，"
        "其中挤兑的比例取均匀分布：三行代码里的全局博弈结果。",

    "The tools this part adds to the House's crisis module.":
        "这一部分为本系列公司的危机模块增加的工具。<bookmark mark='a'/>杠杆与保证金；甩卖与网络；系统性风险与挤兑。<bookmark mark='b'/>以及第41条"
        "规则。本系列公司每天重演有记录以来最糟糕的一天，并把保证金加倍。它的杠杆、融资条款、现金和头寸规模必须挺过去，而不需要做出一天之内做不到的卖出。",

    "Three tests to carry away.":
        "三个随身带走的检验。<bookmark mark='a'/>当一只基金说它是市场中性的，问它如果明天保证金加倍必须卖掉什么，需要几天。<bookmark mark='b'/>"
        "当一家银行把债券持有到期，问它们今天值多少，以及它有多少资金能在一天之内流走。<bookmark mark='c'/>当一个网络看起来分散得很好，问它是针对多大的"
        "冲击分散的：超过阈值，联系就是在传播损失，而不是分担损失。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter four computed who pays what":
        "写给研究者。第4章计算了在违约网络中谁付多少，仿佛答案显而易见。这一章证明答案存在，找出它何时唯一，给出最多n轮就能找到它的算法，并以闭式推导出"
        "第4章的传染阈值。然后用模拟逐一检验。",

    "Eisenberg and Noe's model, two thousand and one.":
        "艾森伯格和诺伊的模型，二〇〇一年。<bookmark mark='a'/>银行i欠银行j L i j，总共欠p拔i。<bookmark mark='b'/>如果它付不了全额，债权人按比例"
        "分配：pi i j是j的份额。<bookmark mark='c'/>一家银行能付的是外部资产加上它收到的钱，但绝不超过它欠的：这就是映射phi。<bookmark mark='d'/>"
        "清算向量是phi的不动点。每家银行要么全额支付，要么付出它拥有的一切。",

    "Theorem one, existence.":
        "定理一，存在性。<bookmark mark='a'/>phi把从零到p拔的盒子映射到它自身，而且是单调的：别人付得越多，你就能付得越多。所以由塔斯基不动点定理，"
        "最大和最小的清算向量存在，其他所有清算向量都在两者之间。<bookmark mark='b'/>迭代就能找到它们：从全额支付往下，或者从零往上。",

    "The proof, for this map.":
        "针对这个映射的证明。<bookmark mark='a'/>从全额支付开始。<bookmark mark='b'/>第一步只会降低支付，而对一个不等式施加单调映射会保持它，所以这个序列"
        "下降。<bookmark mark='c'/>它以零为下界，所以收敛；由于phi连续，极限是一个不动点。<bookmark mark='d'/>任何其他不动点都在每一次迭代之下，所以"
        "这个是最大的。从零往上，同样的论证给出最小的。",

    "Theorem two, uniqueness.":
        "定理二，唯一性。<bookmark mark='a'/>假设从每家银行出发，都有一条债务链通向一家外部资产为正的银行。<bookmark mark='b'/>那么最大和最小的清算向量"
        "重合：答案只有一个。只有当一组银行只欠自己人、又别无他物时，这个条件才会失效。",

    "The proof. <bookmark mark='a'/> Let d be the difference":
        "证明。<bookmark mark='a'/>令d为最大向量与最小向量之差，S为d为正的银行集合。<bookmark mark='b'/>S中的银行在最小向量下付的少于它欠的，所以在那里"
        "它付出全部所有；在最大向量下它至多付出那么多。<bookmark mark='c'/>相减并对S求和。S之外的银行不贡献任何东西，而pi的每一行之和至多为一。"
        "<bookmark mark='d'/>所以这串不等式是紧的：S中的每家银行只向S中的银行付款。",

    "And the end. <bookmark mark='a'/> Under the greatest vector,":
        "最后一步。<bookmark mark='a'/>在最大向量下，S中的银行也付出它们拥有的全部。<bookmark mark='b'/>把它们收到的钱分成来自S内部的支付，其总和等于"
        "S自己的支付，以及来自外部的支付。<bookmark mark='c'/>相消之后，剩下的是非负的，且总和为零：S里没有外部资产，也没有钱流入。<bookmark mark='d'/>"
        "这是一个外面什么也没有的封闭群体，而正则性禁止这种情况。所以S是空集，清算向量是唯一的。",

    "And the algorithm that finds it, fictitious default.":
        "以及找到它的算法，虚拟违约。<bookmark mark='a'/>假设所有人都全额支付。<bookmark mark='b'/>找出付不了的银行。<bookmark mark='c'/>解一个线性方程组："
        "违约者付出全部所有，其余全额支付。<bookmark mark='d'/>支付只会下降，所以违约集合只会扩大，算法在n轮之内停止。一家银行在第几轮违约，说明它在级联中"
        "处于多深的位置：艾森伯格和诺伊把它提议为系统性暴露的一种度量。",

    'f"The check. <bookmark mark=\'a\'/> {r[\'trials\']} random networks':
        "检验。<bookmark mark='a'/>{r['trials']}个随机网络，每个十二家银行，债务随机，外部资产为正，因而是正则的。<bookmark mark='b'/>在"
        "{r['trials']}个中的{r['agree']}个里，算法的答案与从全额支付迭代、从零迭代的结果在小数点后八位上相同：最大和最小向量重合，正如定理二所说。"
        "<bookmark mark='c'/>它需要的轮数从未超过{r['rounds_max']}，平均{r['rounds_mean']:.2f}，而上界是十二。",

    "And the counterexample when regularity fails.":
        "以及正则性失效时的反例。<bookmark mark='a'/>两家银行互相欠一，别无他物。<bookmark mark='b'/>全额支付是一个清算向量：每家收到一，再把它付出去。"
        "什么都不付也是。从上往下迭代找到前者，从下往上找到后者。定理的条件不是一个技术细节。",

    "Theorem three, Chapter four's phase transition.":
        "定理三，第4章的相变。<bookmark mark='a'/>在n家银行的完全网络里，每家资产为a、优先债务为v，对一家银行的冲击epsilon恰好在epsilon超过n乘以"
        "a减v时让所有银行倒下。<bookmark mark='b'/>在它以下，网络分担损失，只有一家倒下。在它以上，所有银行同时倒下。",

    "The derivation, for the symmetric case.":
        "对称情形下的推导。<bookmark mark='a'/>如果其他银行全额支付，零号银行拥有资产减去冲击，加上收到的钱，再减去优先债务。<bookmark mark='b'/>"
        "它所欠款项的缺口，是冲击超出自身缓冲a减v的部分。<bookmark mark='c'/>这个缺口由其他n减一家平均分摊。<bookmark mark='d'/>每家在分到的份额超过"
        "自身缓冲a减v时倒下：也就是epsilon超过n乘以a减v时。由对称性，一个债权人倒下意味着所有债权人都倒下。",

    'f"The check, on a grid of shocks a twentieth apart.':
        "检验，在间隔二十分之一的冲击网格上。<bookmark mark='a'/>随着冲击增大，环形网络一次失去一家银行。<bookmark mark='b'/>完全网络先失去一家，"
        "然后在{r['jump']:.2f}处失去全部十家：这是公式给出的{r['thr']:.0f}之上的第一个网格点。<bookmark mark='c'/>两个弱连接的簇停在五家：损失在簇内"
        "扩散，而簇之间细弱的联系是一道防火墙。",

    'f"Add Chapter three to Chapter four.':
        "把第3章加到第4章上。<bookmark mark='a'/>每家银行还持有一单位共同资产，违约者卖出它，为所有人压低价格：西富恩特斯、费鲁奇和申的模型。"
        "<bookmark mark='b'/>现在，曾经以一家违约就分担了大小为四的冲击的完全网络，失去了全部{f4['complete_fs']}家：甩卖降低了每家银行的缓冲，阈值落到"
        "冲击之下。原本只失去几家的环形网络，失去了全部。在交易对手之间分散，分散不了一种共同资产。",

    "Where the literature goes.":
        "文献走向何方。<bookmark mark='a'/>罗杰斯和维拉特加入违约成本：唯一性可能失效，健康的银行可以通过救助一家濒危银行而获利，就像长期资本管理公司的"
        "债权人那样。<bookmark mark='b'/>格拉瑟曼和杨给网络的贡献设了上界：没有违约成本或甩卖时，通过支付的传染只比直接损失多出一点点。这就是为什么这一章的"
        "最后一张表很重要。<bookmark mark='c'/>埃利奥特、戈卢布和杰克逊表明，级联在一体化和分散化处于中等水平时最严重。",

    "Three open problems. <bookmark mark='a'/> The data:":
        "三个开放问题。<bookmark mark='a'/>数据：双边敞口大多观察不到，通常的重构方法，最大熵，把它们摊得很均匀，从而低估了传染。<bookmark mark='b'/>"
        "带价格的网络：同时包含甩卖和挤兑的清算，它何时唯一，以及如何为真实体系计算它。<bookmark mark='c'/>以及银行之外：基金、交易商、清算所和加密借贷机构"
        "之间的联系，正是这一部分的危机开始的地方，却是度量得最少的。",

    "Pause and predict. Three banks in a ring":
        "暂停并预测。三家银行排成环形，每家欠下一家一，各自持有一半的外部资产。清算向量唯一吗，它是什么？",

    # ------------------------------------------------------------------ Outro
    "Part forty-one in thirteen lines.":
        "用十三行概括第41部分。繁荣积累杠杆，萧条解除杠杆。一只五倍杠杆、亏了百分之十又面对更高折扣率的基金，必须卖掉大部分持仓。损失螺旋和保证金螺旋"
        "一起把小冲击变成大下跌。甩卖通过共同持仓传播损失。银行之间的联系分担小损失、传播大损失。系统性风险可以度量，雷曼的很大。长期资本管理公司展示了"
        "一个拥挤的流动性押注能造成什么。",

    "In twenty oh eight the run was on the shadow banks.":
        "二〇〇八年，挤兑发生在影子银行。二〇二〇年三月，它发生在最安全的资产上。二〇一五年的中国，是融资债务，以及一个把价格吸向自己的熔断机制。"
        "二〇二三年，是一家损失藏在脚注里的银行。本系列公司的规则限制它的杠杆并确保它的融资。研究者章节证明了清算向量存在、唯一，并且阈值有闭式解。",

    "Three lessons. <bookmark mark='a'/> Solvency is not enough:":
        "三条教训。<bookmark mark='a'/>有偿付能力还不够：这一部分里大多数公司在账面上看起来有偿付能力，却因为无法为自己融资一个星期而倒下。"
        "<bookmark mark='b'/>人群就是风险：一个持有者能卖的，所有持有者卖不了。<bookmark mark='c'/>后盾有效，也有代价：每一次救助结束了一场恐慌，"
        "也改变了下一轮繁荣的预期。",

    "The part on one card.":
        "一张卡片上的这一部分。被迫卖出，以及螺旋的乘数。清算向量，以及传染阈值。CoVaR和SRISK。还有挤兑：等待的收益，以及确定阈值的那个积分。",

    "How this part connects.":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>向后：保证金、长期资本管理公司、信用、清算、冲击成本、稳定币挤兑和风险数字，都在一场危机中相遇。"
        "<bookmark mark='b'/>横向：甩卖是所有人同时支付的市场冲击成本，银行挤兑是以存款代替代币的脱锚。<bookmark mark='c'/>向前：第42部分追问当人群"
        "是共享同一个模型的机器时会发生什么，第43部分追问是否有人因承担这种风险而获得回报。",

    "Six desk questions.":
        "六个交易台问题。开场的那个：五倍杠杆、下跌百分之十、折扣率百分之三十，九十中要卖掉五十六点七。<bookmark mark='a'/>有偿付能力的银行怎么会倒闭？"
        "挤兑，当提前卖出的资产拿不回它们的价值时。<bookmark mark='b'/>损失螺旋维持杠杆不变；保证金螺旋降低允许的杠杆。",

    "Is a connected system safer?":
        "连接紧密的体系更安全吗？对小冲击是，超过阈值就不是。<bookmark mark='a'/>一家银行对系统性风险的贡献？CoVaR，或者SRISK。<bookmark mark='b'/>"
        "二〇二〇年三月国债收益率为什么上升？一场交易商吸收不了的现金争夺战。完整解答在讲义里。",

    "The research chapter's pause, answered.":
        "研究者章节的暂停问题，答案来了。<bookmark mark='a'/>每家银行都持有一半的外部资产，所以体系是正则的，清算向量唯一。<bookmark mark='b'/>"
        "它就是全额支付：每家银行收到一，持有一半，付出它的一，留下一半。代入验证，确实是不动点。",

    "And twelve problems:":
        "以及十二道习题：亏损之后的杠杆；一次被迫卖出；螺旋的乘数；杠杆目标；手算一个清算向量；一个传染阈值；CoVaR；SRISK；挤兑的收益；以及一家银行的"
        "利率损失。然后是两道资格考试题：完整的清算定理，以及全局博弈的挤兑阈值。中英文解答都在讲义里。",

    "Where this comes back.":
        "这些内容会在哪里再次出现。第42部分把机器放进市场，追问共享同一个模型的人群是否会一起冲进同样的螺旋。第43部分追问是否有人因承担崩盘和流动性"
        "风险而获得回报。",

    "The textbooks this part follows,":
        "这一部分依循的教科书，以及它引用的论文，从戴蒙德和迪布维格到SRISK。屏幕上的每个数字都由本系列公司的代码计算得出，数据来自FRED、肯尼斯·弗伦奇"
        "截至二〇二〇年的日收益、公开的指数数据和公开文件，或者来自模拟。",

    "The House now knows how much leverage":
        "本系列公司现在知道它在危机中能承受多少杠杆，也知道为什么不能指望别人。<bookmark mark='a'/>下一部分，第42部分：市场中的机器。模拟市场、"
        "学习型交易者、不用交流就能合谋的算法，以及当所有人共享一个模型时会发生什么。",

}
