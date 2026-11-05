"""Chinese narration for quant39: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 区块链 (blockchain), 智能合约 (smart contract), 中心化/去中心化交易所
(CEX/DEX), 托管 (custody), 自动做市商 (AMM), 恒定乘积 (constant product), 流动性提供者 (LP), 无常损失 (impermanent loss),
相对再平衡损失 (loss-versus-rebalancing, LVR), 集中流动性 (concentrated liquidity), 资本效率 (capital efficiency), 最大可提取价值
(MEV), 三明治攻击 (sandwich), 滑点容忍度 (slippage tolerance), 永续合约 (perpetual), 资金费率 (funding rate), 期现套利
(cash-and-carry), 稳定币 (stablecoin), 挤兑 (run), 脱锚 (depeg), 预言机 (oracle), 闪电贷 (flash loan)."""

TITLE = '量化金融，从零搭建 · 第39部分：加密货币与去中心化金融'

CHAPTERS = {
    'Hook': '价格翻倍时，流动性提供者亏多少',
    'Chains': '1. 区块链与交易所',
    'AMM': '2. 自动做市商',
    'LVR': '3. 流动性提供者亏掉了什么',
    'Concentrated': '4. 集中流动性',
    'MEV': '5. 顺序就是钱',
    'Perps': '6. 永续合约',
    'Carry': '7. 期现套利，登记在案',
    'Stable': '8. 稳定币与挤兑',
    'Market': '9. 交易场所、基金与横截面',
    'House': '10. 第39条规则：清点收益里看不到的风险',
    'Research': '写给研究者：相对再平衡损失',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-nine. Crypto and decentralised finance":
        "第39部分。加密货币与去中心化金融：永不收盘的市场、本身就是程序的交易所、永不到期的期货，以及以代币形式存在的美元。这是第六幕的最后一部分。",

    'f"A desk question.':
        "一个交易台问题。<bookmark mark='a'/>你把以太币和美元存入一个恒定乘积池。<bookmark mark='b'/>以太币的价格翻倍。<bookmark mark='c'/>"
        "和单纯持有相比，你亏了多少？教科书的答案是{100 * abs(a['il2']):.1f}%。这一部分说明，为什么这个数字问错了问题。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>一个池子会把它方差的八分之一输给套利者：在以太币2023年的分钟数据上，是其价值的{lv['lvr_pct']:.2f}%，"
        "公式给出{lv['rv8_pct']:.2f}%。<bookmark mark='b'/>肥尾有利于套利者：在真实价格上，他们拿走的那部分损失约为这里证明的布朗运动定理所预测的"
        "{f3['arb_lvr'] / f3['theory']:.1f}倍。<bookmark mark='c'/>期现套利是真实的，但它的风险在别处：一个登记在案的期现套利组合在密封留出期里"
        "每年赚{ca['hold']['ann_pct']:.0f}%，而一次交易所倒闭就会抹掉好几年的收益。",

    "Why it matters. <bookmark mark='a'/> It is a market the size":
        "为什么重要。<bookmark mark='a'/>这是一个堪比主要资产类别的市场，代币总值以万亿美元计，按某些统计口径还拥有全球交易最活跃的期货合约。"
        "<bookmark mark='b'/>它是一座实验室：每一笔成交、报价和每一个池子都是公开的，第35到38部分建模的微观结构就在数据里。"
        "<bookmark mark='c'/>本系列公司的世界也已经和它相连：基金持有比特币ETF，交易对手持有稳定币，各个交易台与同一批套利者交易。",

    "Where this sits. Parts thirty-five to thirty-eight built":
        "这一部分的位置。第35到38部分搭建了交易商、订单簿、执行者和做市商。这一部分在加密市场里把它们一一重新找出来，并为第六幕收尾，"
        "随后第七幕转向整个体系：风险、杠杆与危机。",

    "Seventeen years. Satoshi Nakamoto's paper":
        "十七年。中本聪2008年的论文；2014年Mt. Gox交易所的崩溃；2015年的以太坊；以及2016年BitMEX的永续合约。<bookmark mark='a'/>"
        "然后是Uniswap最早的池子、2020年的“去中心化金融之夏”，MEV在那时被命名，以及集中流动性。<bookmark mark='b'/>还有危机与制度："
        "2022年的Terra、FTX和以太坊转向权益证明；USD币的脱锚；现货ETF；以及美国的稳定币法。",

    "The plan: blockchains, venues and custody":
        "计划：区块链、交易场所与托管；池子以及它们亏掉了什么；集中流动性与一个学习型提供者；交易顺序与MEV；永续合约、资金费率与一个登记在案的"
        "期现套利组合；稳定币与挤兑；以及相对再平衡损失的理论，加以证明并在真实价格上检验。",

    "In the House, a digital-assets desk opens":
        "在本系列公司里，数字资产交易台开张了，这是最后一个交易台。它的第一项任务是弄清楚，它的哪些风险永远不会出现在它的收益里。",

    # ------------------------------------------------------------------ Chains
    "Chapter one. Crypto markets trade on two kinds of venue":
        "第1章。加密市场同时在两类场所交易：一类交易所看起来和第35到38部分的一样，另一类是公共账本上的程序，根本不需要交易所。两者都全天候运行。",

    "A blockchain is a public ledger.":
        "区块链是一个公共账本。<bookmark mark='a'/>任何人都可以读取它，任何人都可以提交交易，交易被打包成区块。<bookmark mark='b'/>每个区块都承诺了"
        "它之前的那个区块，所以改写过去意味着重做此后的一切。<bookmark mark='c'/>程序也存在于它之上。一个交易池就是一份智能合约，持有代币、"
        "按它的公式运行，中间没有任何人。",

    "Who writes the ledger.":
        "谁来写账本。<bookmark mark='a'/>比特币，中本聪2008年的设计：矿工竞相求解一道难题，大约每十分钟一个区块。<bookmark mark='b'/>以太坊，"
        "自2022年起：质押以太币的验证者轮流出块，每十二秒一个时隙。<bookmark mark='c'/>每笔交易都为它占用的空间支付费用，称为gas：一场争夺"
        "被打包的拍卖。<bookmark mark='d'/>而谁来构建区块，谁就决定其中交易的顺序，这件事原来非常值钱。",

    "Two kinds of venue. <bookmark mark='a'/> Centralised exchanges":
        "两类场所。<bookmark mark='a'/>中心化交易所托管客户资产，在链下撮合订单，并提供带杠杆的永续合约；大部分价格发现发生在那里。"
        "<bookmark mark='b'/>去中心化交易所是链上的合约，没有托管，也没有订单簿：公式决定价格，套利者推动价格。<bookmark mark='c'/>两者之间，"
        "流动着稳定币、跨链桥，以及昼夜同时交易两边的套利者。",

    "A market that never closes.":
        "一个永不收盘的市场。<bookmark mark='a'/>每年八千七百六十个小时，而证券交易所大约只有一千六百个小时。<bookmark mark='b'/>周末更清淡，"
        "成交量约为工作日的一半，正如第37部分所测，因为银行和它们的转账停了。<bookmark mark='c'/>所以风险按三百六十五天年化，而最剧烈的波动"
        "可能恰好发生在盯盘的人最少的时候。",

    "And the plumbing. <bookmark mark='a'/> A centralised crypto exchange":
        "还有底层管道。<bookmark mark='a'/>中心化加密交易所同时是经纪商、交易场所和清算所，这些角色在第21和35部分是分开的。<bookmark mark='b'/>"
        "保证金被持续盯市，仓位由机器强制平仓，也就是第2部分的保证金账户。<bookmark mark='c'/>如果一笔强平无法成交，由交易所的保险基金赔付；"
        "保险基金用完后，另一边盈利的仓位会被削减，这叫自动减仓。",

    'f"The failure that defined the risk:':
        "定义了这种风险的那次倒闭：2022年11月的FTX，据报道，并经后来的庭审确认。<bookmark mark='a'/>FTX自己的代币FTT，月初在币安上约为"
        "{f['first']:.0f}美元。一篇新闻报道质疑其关联交易公司Alameda的资产负债表，其中大量资产就是FTT；币安表示将卖出自己持有的FTT。"
        "<bookmark mark='b'/>8日提现停止，该代币跌到约{f['low']:.2f}美元。客户资产曾被关联公司动用；其创始人于2023年11月被判欺诈罪成立。",

    "Three lessons. <bookmark mark='a'/> Venue risk is not in the returns":
        "三条教训。<bookmark mark='a'/>交易场所风险不在收益里：一个在FTX上运行的策略，直到资产消失的那一天之前看起来都很正常，而没有任何回测"
        "包含那一天。<bookmark mark='b'/>抵押品就是敞口：存放在交易场所的保证金和现货会随它一起损失，所以本系列公司按场所设定上限，就像第21部分"
        "为交易对手敞口定价那样。<bookmark mark='c'/>而建立在发行方自家代币上的资产负债表，只值那个代币在甩卖中能卖出的价钱。",

    "The cash leg. <bookmark mark='a'/> Stablecoins such as tether":
        "现金腿。<bookmark mark='a'/>泰达币和USD币这样的稳定币，是发行方承诺按一美元赎回的代币。<bookmark mark='b'/>它们由银行存款、国库券和"
        "回购支持：一家没有存款保险的狭义银行，这是第8章的主题。<bookmark mark='c'/>这一部分几乎每一个价格都以稳定币计价：比特币对泰达币，"
        "而不是对美元。",

    "Pause and predict. A pool holds five thousand ether":
        "暂停并预测。一个池子持有五千个以太币和一千万美元，所以价格是两千美元。一位交易者从中买入五百个以太币，支付千分之三的手续费。"
        "平均成交价是多少？",

    # ------------------------------------------------------------------ AMM
    'f"Chapter two, and the answer to the pause:':
        "第2章，以及暂停问题的答案：平均每个以太币约{t['avg']:,.0f}美元，比池子的起始价格高{100 * t['slip']:.0f}%。池子没有订单簿，只有一个公式，"
        "而公式对每多买一单位都要价更高。这一章把这个公式拆开来看。",

    "The constant-product market maker.":
        "恒定乘积做市商。<bookmark mark='a'/>一个池子持有数量为x的代币和y的计价资产，接受任何保持两者乘积不变的交易。<bookmark mark='b'/>"
        "它的价格是两种储备之比，也就是曲线的斜率。<bookmark mark='c'/>交易者放入delta x的代币，必须使乘积保持不变，<bookmark mark='d'/>"
        "这就决定了它能拿到多少；对投入部分收取的手续费，在经典池子里是千分之三，归提供储备的人所有。",

    'f"A pool of {a[\'x\']:,.0f} ether':
        "一个持有{a['x']:,.0f}个以太币和{y_m:.0f}百万美元稳定币的池子，所以价格是两千。<bookmark mark='a'/>以太币的买家把这个点沿曲线向上推："
        "以太币流出，美元流入，斜率也就是价格随之上升。<bookmark mark='b'/>卖家把它推回去。这条曲线永远不会耗尽：它只是对每多一单位要价更高，没有上限。",

    'f"What the curve charges.':
        "曲线收多少钱。<bookmark mark='a'/>十个以太币比起始价格贵{100 * t0['slip']:.1f}%，主要是手续费。<bookmark mark='b'/>一百个，"
        "{100 * a['trades'][1]['slip']:.1f}%；五百个，即池子的十分之一，{100 * a['trades'][2]['slip']:.0f}%；<bookmark mark='c'/>一千个，"
        "即池子的五分之一，{100 * t3['slip']:.0f}%。滑点比规模增长得更快，因为交易沿着一条越来越陡的曲线前进。这就是第36部分的订单簿，"
        "只是深度由公式而不是由做市商决定。",

    "The general form. <bookmark mark='a'/> A constant-function market maker":
        "一般形式。<bookmark mark='a'/>恒定函数做市商接受任何保持某个不变量固定的交易，其等值线是凸的。<bookmark mark='b'/>它的价格是等值线的斜率。"
        "<bookmark mark='c'/>Balancer的加权池在每种代币上保持固定的价值份额。<bookmark mark='d'/>Curve的stableswap用于本应平价交易的资产，"
        "在锚定点附近几乎是一条直线，所以稳定币兑换几乎不改变价格，而一旦脱锚就急剧弯曲。",

    "How the pool's price stays right.":
        "池子的价格如何保持正确。<bookmark mark='a'/>池子不知道市场价格，它只知道自己的储备。当以太币在中心化交易所上涨时，池子仍然报旧价。"
        "<bookmark mark='b'/>套利者从池子买入便宜的以太币，再到别处卖出，直到池子扣除手续费后的价格与市场一致。<bookmark mark='c'/>每一笔这样的"
        "交易都是对着过时的价格做的，就像第38部分被狙击的报价：套利者的利润就是流动性提供者的损失。",

    "The pool as an oracle.":
        "作为预言机的池子。<bookmark mark='a'/>Guillermo Angeris和Tarun Chitra证明，池子的价格携带信息：把它推离市场要让操纵者付出真金白银，"
        "这笔钱被套利者收走。<bookmark mark='b'/>所以借贷协议读取时间加权平均价，操纵者必须让价格偏离市场许多个区块。<bookmark mark='c'/>但是闪电贷"
        "在同一笔交易内借入并归还，让资金在一瞬间变得免费，据报道，只读取单个区块价格的协议就这样被掏空过。",

    'f"What a liquidity provider gives up.':
        "流动性提供者放弃了什么。<bookmark mark='a'/>价格为P时，恒定乘积池持有根号k除以P的代币，价值为二倍根号kP。<bookmark mark='b'/>单纯持有起始"
        "资产的价值是起点乘以r加一，其中r是价格之比。<bookmark mark='c'/>两者之比减一就是无常损失：二倍根号r除以一加r，再减一。<bookmark mark='d'/>"
        "如果以太币翻倍，池子比持有少值{100 * abs(a['il2']):.1f}%：这就是交易台问题的答案。价格减半的代价完全一样。",

    'f"The whole curve.':
        "整条曲线。<bookmark mark='a'/>小幅变动时很小，对价格的对数对称，价格四倍变动时为{100 * abs(a['il4']):.0f}%，无论涨跌。<bookmark mark='b'/>"
        "它被称为“无常”，是因为价格回到起点时它就消失了。这个名字恰恰是问题所在：它只取决于价格最终停在哪里，而不取决于路径，所以它完全不告诉你"
        "池子一路上付给了套利者多少钱，也不告诉你手续费是否弥补了这些。",

    "Pause and predict. In twenty twenty-three ether rose":
        "暂停并预测。2023年，以太币从约一千二百美元涨到二千三百美元。一个恒定乘积池每分钟都被套利到币安的价格。和一个持有相同数量以太币、"
        "但按市场价格交易的组合相比，它把自身价值的多大比例输给了套利者？",

    # ------------------------------------------------------------------ LVR
    "f'Chapter three, and the answer to the pause:":
        "第3章，以及暂停问题的答案：全年约为其价值的{lv['lvr_pct']:.1f}%。这不是无常损失，后者只取决于价格最终停在哪里；这是一笔输给套利者、"
        "一分钟一分钟累积起来的损失。这一章说明如何测量它，以及为什么它才是正确的度量。",

    "Three portfolios. <bookmark mark='a'/> Hold:":
        "三个组合。<bookmark mark='a'/>持有：保留起始资产。<bookmark mark='b'/>池子：价格上涨时卖出代币、下跌时买入，用的都是它自己过时的价格。"
        "<bookmark mark='c'/>以及Jason Milionis、Ciamac Moallemi、Tim Roughgarden和Anthony Lee Zhang的再平衡组合：每一时刻的持仓都与池子相同，"
        "但每一次调整都按市场价格进行。",

    'f"Ether in twenty twenty-three, a constant-product pool with no fee':
        "2023年的以太币，一个不收手续费的恒定乘积池，每十分钟被套利到币安的价格。<bookmark mark='a'/>持有起始资产最终为起点的{pth['hold'][-1]:.3f}。"
        "<bookmark mark='b'/>再平衡组合为{pth['rebal'][-1]:.3f}。<bookmark mark='c'/>池子为{pth['lp'][-1]:.3f}：低于两者，而且与再平衡组合的差距"
        "稳步扩大，无论市场平静还是上涨。",

    'f"Take the differences.':
        "看差值。<bookmark mark='a'/>池子减持有，{il:+.3f}，是无常损失；它混合了两件事。<bookmark mark='b'/>池子减再平衡，{-lvr:+.3f}，"
        "是相对再平衡损失：两者在每一时刻的敞口相同，所以差距纯粹是按过时价格交易的成本。<bookmark mark='c'/>再平衡减持有，{mk:+.3f}，是市场部分："
        "在以太币上涨时持有的以太币变少了。那是一种敞口选择，可以用对冲抵消，而不是成本。",

    "Why the rebalancing benchmark is the right one.":
        "为什么再平衡基准才是正确的。<bookmark mark='a'/>它可以被对冲：用永续合约做空池子的代币持仓的提供者，剩下的恰好就是这个差距加上手续费。"
        "<bookmark mark='b'/>它是可预测的：以由波动率决定的速率累积，与价格最终停在哪里无关。<bookmark mark='c'/>它是某个人的收入：套利者的利润、"
        "一笔手续费，或付给构建区块的人的钱。",

    'f"The rate has a formula, proved in the research chapter.':
        "这个速率有公式，在研究者章节中证明。<bookmark mark='a'/>对恒定乘积池，是方差的八分之一乘以池子的价值，按单位时间计。<bookmark mark='b'/>"
        "以太币2023年的波动率为{100 * lv['vol']:.0f}%，所以方差的八分之一是{lv['rv8_pct']:.2f}%。<bookmark mark='c'/>每分钟套利一次的池子实测损失："
        "{lv['lvr_pct']:.2f}%。",

    'f"Does it depend on how often the pool is arbitraged?':
        "它取决于池子被套利的频率吗？<bookmark mark='a'/>每分钟、每五分钟、每小时、每天：损失都在{lo:.2f}%到{hi:.2f}%之间，因为以太币的已实现方差"
        "几乎不随采样频率变化。无论套利者切得多细，池子损失的都是它方差的八分之一。",

    'f"When providing pays.':
        "什么时候提供流动性才划算。<bookmark mark='a'/>一个做了对冲的提供者赚取手续费、支付LVR。<bookmark mark='b'/>手续费收入等于费率乘以周转。"
        "<bookmark mark='c'/>按千分之三的费率，在以太币的2023年里，一个池子全年需要约为其价值{need:.0f}倍的成交量，<bookmark mark='d'/>"
        "也就是每天约为池子的{per_day:.1f}%，而且必须来自非套利者。套利交易也付手续费，但恰恰是在那些构成损失本身的交易上。",

    "The same thing in Part eleven's language.":
        "用第11部分的语言再说一遍。<bookmark mark='a'/>池子的价值是价格的凹函数：它是负伽马，就像卖出的跨式期权。<bookmark mark='b'/>做了对冲的期权卖方"
        "支付伽马的一半乘以方差，而做了对冲的流动性提供者支付的正是这个。<bookmark mark='c'/>它的手续费扮演期权时间衰减的角色。为池子提供流动性就是在卖波动率。",

    "Pause and predict. A concentrated position supplies liquidity":
        "暂停并预测。一个集中流动性头寸只在价格上下百分之五之内提供流动性。它每一美元提供的流动性是恒定乘积头寸的多少倍？它每一美元的损失又会怎样？",

    # ------------------------------------------------------------------ Concentrated
    "f'Chapter four, and the answer to the pause:":
        "第4章，以及暂停问题的答案：每一美元的流动性约为{e5:.0f}倍，因此只要价格停留在区间内，每一美元输给套利的损失也约为{e5:.0f}倍。"
        "集中，就是在同一个卖波动率的头寸上加杠杆。",

    "Uniswap's third version, in twenty twenty-one.":
        "2021年，Uniswap的第三版。<bookmark mark='a'/>提供者选择一个价格区间，只在其中提供流动性。在区间内，它的行为像一个带有更大虚拟储备的恒定乘积池，"
        "持有x的代币，<bookmark mark='b'/>以及y的美元。<bookmark mark='c'/>在区间之外它停止交易、什么也赚不到：低于区间时全部是代币，高于区间时全部是美元。",

    'f"A position on ether between':
        "一个以太币价格在{v['pa']:,.0f}到{v['pb']:,.0f}美元之间的头寸。<bookmark mark='a'/>低于区间时，它只持有以太币，所以价值随以太币一比一下跌。"
        "<bookmark mark='b'/>在区间内，价值弯曲：凹的、负伽马，这是池子的标志。<bookmark mark='c'/>高于区间时，它已经卖光以太币，只持有美元：上涨收益被封顶。"
        "这是一份被持续卖出的备兑看涨期权。",

    'f"How much liquidity a dollar buys.':
        "一美元能买到多少流动性。<bookmark mark='a'/>对从P除以w到P乘以w的区间，相对恒定乘积头寸的倍数是一除以一减去w的负二分之一次方。"
        "<bookmark mark='b'/>正负百分之一：约{e1:.0f}倍。正负百分之十：约{rows_[3]['eff']:.0f}倍。上下各翻一倍：{rows_[-1]['eff']:.1f}倍。"
        "一个区间很窄的提供者赚到的手续费，相当于一个拥有这么多倍资本的全区间提供者。",

    'f"The price of concentration: leaving the range.':
        "集中的代价：离开区间。2023年的以太币，区间以每天的开盘价为中心。<bookmark mark='a'/>正负百分之一：价格在{100 * r1['days_left']:.0f}%的日子里"
        "离开过区间，有{100 * r1['out_share']:.0f}%的时间在区间之外，什么也赚不到。<bookmark mark='b'/>正负百分之五：{100 * r5['days_left']:.0f}%的日子，"
        "{100 * r5['out_share']:.1f}%的时间。窄区间需要不断重新居中，而每一次重新居中都是一笔有成本的交易。",

    "And the loss scales the same way.":
        "损失也按同样的方式放大。<bookmark mark='a'/>按单位流动性，速率是sigma平方的四分之一乘以L根号P，和全区间池一样。<bookmark mark='b'/>"
        "所以按每一美元计，在区间中心附近，损失是全区间速率乘以资本效率。<bookmark mark='c'/>手续费也一样。集中放大了这个赌注，但不改变它的符号。"
        "如果手续费胜过方差，越窄越好；如果不是，越窄亏得越快。",

    'f"Can a provider learn when to concentrate?':
        "提供者能学会什么时候集中吗？计划里承诺了一个学习型提供者，这就是它，在一个模拟世界里。<bookmark mark='a'/>波动率是{100 * sig[0]:.0f}%或"
        "{100 * sig[1]:.0f}%，不时切换，而提供者看不到当前是哪一种。<bookmark mark='b'/>每天它要么撤出，要么重新居中一个宽、中或窄的区间。"
        "<bookmark mark='c'/>它只能看到昨天的已实现波动率。<bookmark mark='d'/>它的回报是来自无信息交易者的手续费，按区间的资本效率放大，减去当天"
        "输给套利的精确损失，再减去重新居中的成本。它对冲了代币敞口，所以价格方向不起作用。",

    'f"After four thousand simulated days,':
        "四千个模拟交易日之后，它学到了什么，以每天资本的基点计。<bookmark mark='a'/>平静的一天之后，窄区间的价值约为{q_calm:+.0f}；更宽的区间少得多。"
        "<bookmark mark='b'/>动荡的一天之后，每个区间都亏钱，窄区间亏得最多，而价值为零的撤出最好。中间状态几乎从未出现，因为两种状态相距很远。",

    'f"Tested on two thousand fresh days.':
        "在两千个全新的交易日上检验。<bookmark mark='a'/>每一个固定区间平均都亏钱，窄区间亏得最多，每天{narrow:+.0f}个基点，因为动荡日的损失超过"
        "平静日的收益。<bookmark mark='b'/>学到的策略，平静时用窄区间、动荡时撤出，每天赚{ev['learned']['mean_bp']:+.0f}，接近能看到状态的提供者的"
        "{ev['oracle']['mean_bp']:+.0f}。它全部的本领就是一条规则：波动率高的时候不要卖波动率。",

    "What not to conclude.":
        "不能得出什么结论。<bookmark mark='a'/>手续费水平是假设的：真实的手续费收入取决于无信息成交量，而且要和区间内所有其他提供者分享。"
        "<bookmark mark='b'/>这个世界很简单：两种相距很远的状态，加上一个能揭示它们的信号。<bookmark mark='c'/>但教训成立：提供流动性就是卖波动率，"
        "学习型策略的价值在于把握卖出的时机，这正是第11部分波动率交易台的教训。",

    "Pause and predict. A trader buys a hundred thousand dollars":
        "暂停并预测。一位交易者从第2章的池子买入十万美元的以太币，接受最多百分之一的滑点。一个能够安排区块内交易顺序的人先看到了这笔订单。他能拿走多少？",

    # ------------------------------------------------------------------ MEV
    "f'Chapter five, and the answer to the pause:":
        "第5章，以及暂停问题的答案：攻击者约赚{r['profit']:,.0f}美元，而交易者收到的以太币比报价少约{r['victim_loss']:,.0f}美元；差额作为手续费归池子。"
        "在公共账本上，谁安排交易的顺序，谁就能围绕它们交易。",

    "How a trade reaches the ledger.":
        "一笔交易如何到达账本。<bookmark mark='a'/>用户签署一笔兑换；它在待处理交易的公共池里等待；搜索者围绕它编写交易捆绑包；构建者组装整个区块，"
        "并为让区块被打包而出价；提议者接受最高出价。<bookmark mark='b'/>据报道，自2022年起，大多数以太坊区块都是这样构建的。<bookmark mark='c'/>"
        "选择区块里放什么、按什么顺序放，这件事的价值被称为最大可提取价值。",

    'f"A sandwich, step by step,':
        "三明治攻击，一步一步来，针对一笔允许百分之一滑点的一百万美元买单。<bookmark mark='a'/>攻击者先买入以太币，把池子沿曲线向上推。"
        "<bookmark mark='b'/>受害者的买单接着执行，价格更差，但恰好在其限度之内，所以不会失败。<bookmark mark='c'/>然后攻击者按受害者推高的价格，"
        "把以太币卖回池子。利润：约{r['profit']:,.0f}美元，而受害者比报价少收到约{r['victim_loss']:,.0f}美元。",

    "What limits it. <bookmark mark='a'/> Every swap names":
        "是什么限制了它。<bookmark mark='a'/>每一笔兑换都写明它最少接受多少：滑点容忍度。<bookmark mark='b'/>攻击者抢先交易的规模恰好让受害者停在限度之内。"
        "<bookmark mark='c'/>所以攻击者拿走的大致是容忍度乘以交易额，减去池子对攻击者两条腿收取的手续费。受害者自己的设置决定了奖金的大小。",

    'f"The prize, in Chapter two\'s pool.':
        "在第2章的池子里，奖金有多大。<bookmark mark='a'/>在这里，一笔一万美元的交易在任何容忍度下都是安全的：攻击者两条腿的手续费超过了它能拿走的。"
        "<bookmark mark='b'/>十万美元、百分之一，约{r1['profit']:,.0f}；<bookmark mark='c'/>一百万美元、百分之三，约{r3['profit']:,.0f}。利润几乎与"
        "容忍度乘以规模成正比，而手续费设定了一个门槛，低于它就没人费心。",

    "Three kinds of extractable value,":
        "三类可提取价值，最早由Philip Daian和合作者在2020年的《Flash Boys 2.0》中归纳。<bookmark mark='a'/>套利，在池子之间以及池子与中心化交易所之间，"
        "据链上数据研究报道，这是最大的一类。<bookmark mark='b'/>清算：借贷协议向最先偿还抵押不足贷款的人支付奖励，争夺它就是争夺区块内的位置。"
        "<bookmark mark='c'/>以及三明治攻击和即时流动性：围绕另一位用户的兑换交易，纯粹是从该用户那里的转移。",

    "Chapter three's loss, seen from the block.":
        "从区块的角度看第3章的损失。<bookmark mark='a'/>LVR等于套利利润加上套利交易的手续费：最大的可提取价值来源。<bookmark mark='b'/>搜索者竞相捕获它，"
        "构建者竞相争取搜索者，提议者出售区块。<bookmark mark='c'/>只要竞争足够，大部分会被竞价让渡给控制区块的人，就像第38部分的狙击租金流向了出售速度的交易场所。",

    "Defences. <bookmark mark='a'/> Tight slippage limits":
        "防御。<bookmark mark='a'/>严格的滑点限制会缩小奖金，而直接发给构建者的私有通道让兑换不进入公共交易池。<bookmark mark='b'/>批量拍卖，"
        "例如CoW Swap，以统一价格清算订单，所以批次内的顺序无关紧要：第38部分的补救办法，搬到了链上。<bookmark mark='c'/>而出售每个区块第一笔交易权利的池子，"
        "或随波动率提高手续费的池子，可以把一部分损失还给它们的提供者。",

    "Pause and predict. A perpetual future never expires":
        "暂停并预测。永续合约永不到期，所以没有什么在某个日期迫使它的价格与现货相等。是什么让比特币永续合约保持在现货的几个基点之内？谁为此付钱？",

    # ------------------------------------------------------------------ Perps
    'f"Chapter six, and the answer to the pause: funding.':
        "第6章，以及暂停问题的答案：资金费率。每八小时，一方持有者向另一方付款，金额随永续合约相对现货的溢价增加。合约高于现货时由多头付款，"
        "而在比特币上大部分时间都是如此：自2020年以来平均每年约{b['annual_pct']:.0f}%。",

    "How it works. <bookmark mark='a'/> Every eight hours on Binance":
        "它如何运作。<bookmark mark='a'/>在币安上，每八小时，多头持有者按资金费率乘以仓位价值向空头持有者付款。<bookmark mark='b'/>当永续合约高于现货指数时，"
        "费率为正，做多变得有成本，从而把价格往下拉。<bookmark mark='c'/>当它低于现货时，费率转负，由空头付款。<bookmark mark='d'/>没有到期、无需展期，"
        "再加上高杠杆，使它成为加密市场交易最活跃的合约。",

    "Binance's rule. <bookmark mark='a'/> A premium index":
        "币安的规则。<bookmark mark='a'/>溢价指数对八小时内永续合约偏离现货指数的程度取平均。<bookmark mark='b'/>费率等于这个溢价加上万分之一的利息项，"
        "并被限制在一个区间内。<bookmark mark='c'/>所以只要溢价很小，资金费率就恰好等于利息项：每八小时万分之一，每年约百分之十一，由多头支付。",

    "Its no-arbitrage price.":
        "它的无套利价格。<bookmark mark='a'/>永续合约多头获得价格变动，并按强度kappa就与现货的差额支付资金费。<bookmark mark='b'/>建立头寸不花钱，"
        "所以在第9部分的定价测度下，它的收益是一个鞅。<bookmark mark='c'/>试一个与现货成比例的价格，现货以利率减去该币出借所得的速度漂移。"
        "<bookmark mark='d'/>答案是：kappa除以kappa减去r减q，再乘以现货，来自Songrun He、Asaf Manela、Omri Ross和Victor von Wachter。"
        "当美元的收益高于币的收益时，永续合约高于现货，幅度约为r减q除以kappa。",

    "That interest term matters.":
        "这个利息项很重要。<bookmark mark='a'/>每天三次万分之一，每年约百分之十一。<bookmark mark='b'/>所以即使永续合约按现货价格交易，多头也要支付它。"
        "<bookmark mark='c'/>而持有现货并做空永续合约的人就能收取它，且不承担价格敞口：下一章的交易。",

    "Six years of Bitcoin's funding,":
        "比特币六年的资金费率，每九次结算取一次，年化。<bookmark mark='a'/>一条位于约百分之十一处的密集横线：溢价很小时的利息项。<bookmark mark='b'/>"
        "2021年牛市中远高于它的尖峰，当时加杠杆的多头为其敞口支付了每年超过百分之一百的费用。<bookmark mark='c'/>以及2021年和2022年崩盘中低于零的时段，"
        "那时由空头付款。",

    'f"Year by year. <bookmark mark=\'a\'/> On Bitcoin, funding averaged':
        "逐年来看。<bookmark mark='a'/>比特币的资金费率在2021年平均每年{y21['annual_pct']:.0f}%，在Terra和FTX的2022年为{y22['annual_pct']:.0f}%，"
        "那一年{100 * y22['neg']:.0f}%的结算为负。<bookmark mark='b'/>六年合计，{100 * b['at_base']:.0f}%的结算恰好等于利息项，平均为"
        "{b['annual_pct']:.0f}%；以太币为{e['annual_pct']:.0f}%。<bookmark mark='c'/>2025年，等于利息项的比例降到{100 * b['by_year'][5]['at_base']:.0f}%，"
        "费率一次也没有超过它，套利收益缩小到{b['by_year'][5]['annual_pct']:.0f}%：很可能是更多资本前来收取它了。",

    'f"Does the rule explain the data?':
        "这条规则能解释数据吗？<bookmark mark='a'/>每个点是一次结算：此前八小时永续合约相对现货的溢价，取自小时收盘价，对应当次设定的费率。"
        "相关系数{b['corr_prem']:.2f}。<bookmark mark='b'/>把币安的规则作用于溢价，相关系数升至{b['corr_rule']:.2f}：位于万分之一处的平坦段就是那个限制区间，"
        "在数据中清晰可见。",

    "Who pays, and why.":
        "谁付钱，为什么。<bookmark mark='a'/>正的资金费率是杠杆的价格：加杠杆的多头为他们无法在现货中融资获得的敞口所支付的费用，一个由加密市场自身杠杆需求"
        "决定的利率。<bookmark mark='b'/>它也是情绪的晴雨表，上涨时高、崩盘时为负，强制平仓集中出现在它的极端值附近。<bookmark mark='c'/>它也是第2部分的"
        "保证金账户在2020年3月崩盘中一路支付的持续成本。",

    'f"Pause and predict. Funding on ether\'s perpetual':
        "暂停并预测。以太币永续合约的资金费率平均每年约{f['ETHUSDT']['annual_pct']:.0f}%。一个交易台买入以太币并做空永续合约来收取它，"
        "不承担以太币的价格敞口。可能出什么问题？",

    # ------------------------------------------------------------------ Carry
    "Chapter seven, and the answer to the pause: three things.":
        "第7章，以及暂停问题的答案：三件事。资金费率可能转负，于是交易台要付钱。上涨行情会让做空的永续合约在保证金上先出现亏损，而现货的收益还来不及调用，"
        "所以需要备用资本。交易所还可能倒闭，带走存放在那里的一切。这一章登记这笔交易，打开密封的留出期，然后追问它的收益没有显示什么。",

    "The book. <bookmark mark='a'/> Long one unit of spot,":
        "这个组合。<bookmark mark='a'/>做多一单位现货，做空一单位永续合约：对币价没有敞口。<bookmark mark='b'/>它在每次结算时收取资金费，再加减溢价的变化。"
        "<bookmark mark='c'/>现货全额买入，空头按其价值的三分之一缴纳保证金，所以每一美元现货需要一点三三美元资本。<bookmark mark='d'/>进出一次的成本是"
        "十五个基点。",

    "What can go wrong, before any data.":
        "在看任何数据之前，先想想会出什么错。<bookmark mark='a'/>资金费率在崩盘中转负，一直持仓的组合要一路付钱。<bookmark mark='b'/>空头腿有保证金要求："
        "上涨百分之五十会让它在现货收益转移过来之前亏掉一半名义金额，没有备用资本就会被强平，对冲也就没了。<bookmark mark='c'/>交易场所可能倒闭，"
        "所有东西计价所用的稳定币也可能脱锚。",

    'f"Nine variants, on the research window.':
        "研究窗口上的九个变体。<bookmark mark='a'/>比特币、以太币或两者；一直持仓、过去一周资金费率为正时持仓、或超过每年百分之五时持仓。窗口很短："
        "币安公开的资金费率文件从2020年1月开始，所以研究只有那一年。<bookmark mark='b'/>最好的是：{c['best']['asset']}，{rule_name}，每年"
        "{c['best']['ann_pct']:.0f}%，夏普比率{c['best']['sharpe']:.1f}。过滤条件几乎不起作用，因为2020年的资金费率几乎总是正的。",

    'f"So the House registers it.':
        "于是本系列公司登记它。<bookmark mark='a'/>以太币组合，一直持仓，连同成本、保证金和代码的哈希值。<bookmark mark='b'/>九次试验。"
        "<bookmark mark='c'/>本系列已尝试配置的计数器升至{c['trials']:,}。然后打开信封，只此一次。",

    'f"The envelope.':
        "信封。<bookmark mark='a'/>承诺的是：每年{r['ann_pct']:.0f}%，夏普比率{r['sharpe']:.1f}。<bookmark mark='b'/>在五个未见过的年份里实际交付："
        "每年{h['ann_pct']:.1f}%，夏普{h['sharpe']:.1f}。收益不到一半，但仍是业绩记录中最高的夏普比率之一。<bookmark mark='c'/>它最大的回撤是"
        "{abs(h['maxdd_pct']):.1f}%。按这些数字，它看起来像白送的钱。先记住这个想法。",

    'f"Year by year. <bookmark mark=\'a\'/> Twenty twenty-one, the leverage boom':
        "逐年来看。<bookmark mark='a'/>2021年，杠杆繁荣：{ys['2021']['ret_pct']:.0f}%。<bookmark mark='b'/>2022年，Terra和FTX："
        "{ys['2022']['ret_pct']:.1f}%，因为以太币的资金费率在三分之一的结算中为负。<bookmark mark='c'/>然后是{ys['2023']['ret_pct']:.0f}%、"
        "{ys['2024']['ret_pct']:.0f}%和{ys['2025']['ret_pct']:.0f}%。这份收益由加杠杆的多头支付，所以他们最热切时它最大，他们被强平时它几乎为零。",

    'f"The hold-out as a curve.':
        "把留出期画成曲线。<bookmark mark='a'/>2021年陡峭上升，一个平坦的年份，之后是较缓的斜率：一美元变成了{v[-1]:.2f}美元。一路上几乎没有起伏。"
        "正是这样的曲线，应当让风险经理追问它没有显示什么。",

    'f"Why it decayed.':
        "它为什么衰减。<bookmark mark='a'/>这笔交易变得拥挤：据报道，从2024年起它被大规模打包进Ethena的美元代币，由用永续合约空头对冲的现货支持，"
        "也就是第31部分的搜索反复找到的那个近乎无风险的币。<bookmark mark='b'/>2025年，比特币和以太币的资金费率一次也没有超过利息项。<bookmark mark='c'/>"
        "而承诺建立在一年牛市之上：在十二个月上，夏普比率的标准误是{se:.2f}，是五年留出期的三倍。",

    'f"What the returns do not show.':
        "收益没有显示什么。<bookmark mark='a'/>即使现货托管在别处，空头的保证金，也就是四分之一的资本，仍然放在交易所。<bookmark mark='b'/>大多数这类组合"
        "把两条腿都放在同一家交易所以轧差保证金，那样一次倒闭就会带走一切。<bookmark mark='c'/>仅仅损失保证金，就会抹掉留出期里约{yrs:.1f}年的收益。"
        "回测中{abs(h['maxdd_pct']):.1f}%的回撤，实际上只是在说币安活了下来。在FTX上运行同样组合的交易者失去了他们的抵押品。",

    "So what is it? <bookmark mark='a'/> A premium, not an arbitrage":
        "那么它到底是什么？<bookmark mark='a'/>是一种溢价，而不是套利：为多头提供杠杆、承担交易场所和稳定币风险所得的报酬，是第22部分的套息交易在新市场里的样子。"
        "<bookmark mark='b'/>它与它的市场一起崩溃：在加密借贷机构纷纷倒闭的2022年，它几乎什么也没赚。<bookmark mark='c'/>所以本系列公司按它的尾部，"
        "即失去一个交易场所的抵押品，来确定规模，而不是按它的夏普比率。",

    "Pause and predict. On the tenth of March twenty twenty-three":
        "暂停并预测。2023年3月10日，存放USD币部分储备的银行倒闭了，这枚币跌到约八十八美分。那是一场挤兑吗？一个只是等了三天的持有者拿到了什么？",

    # ------------------------------------------------------------------ Stable
    "Chapter eight, and the answer to the pause: yes, a run":
        "第8章，以及暂停问题的答案：是的，一场挤兑，针对一个储备一度令人怀疑的发行方。而等了三天的持有者重新拿到了一美元，因为美国当局为倒闭银行的存款"
        "提供了全额担保。稳定币是一家银行，也会像银行一样被挤兑。",

    "Three kinds. <bookmark mark='a'/> Backed by dollars,":
        "三种类型。<bookmark mark='a'/>由美元支持，比如泰达币和USD币：发行方持有存款、国库券和回购，为经过审核的客户赎回代币。<bookmark mark='b'/>"
        "由加密资产支持，比如DAI：以价值更高的其他代币作抵押的贷款，抵押品下跌时自动清算。<bookmark mark='c'/>以及由孪生代币支持：Terra的UST，"
        "可以兑换价值一美元的第二种代币，而那是协议自己印出来的。",

    "Douglas Diamond and Philip Dybvig's bank, on chain.":
        "Douglas Diamond和Philip Dybvig的银行，搬到链上。<bookmark mark='a'/>负债可以随时按一美元赎回。<bookmark mark='b'/>资产中有一部分是流动的，"
        "其余部分仓促出售时只能折价。<bookmark mark='c'/>如果所有人同时赎回，资产就不够。<bookmark mark='d'/>而在先到先得的赎回规则下，如果别人在挤兑，"
        "先跑就是划算的，所以即使是一个从容处置时有偿付能力的发行方，挤兑也是一个均衡。",

    "In numbers. <bookmark mark='a'/> With all reserves liquid":
        "用数字说明。<bookmark mark='a'/>如果所有储备都是流动的，就没有理由挤兑：一美元对一美元。<bookmark mark='b'/>如果五分之一不流动、甩卖折价百分之二十，"
        "一次全面挤兑后每一美元只剩九十六美分，足以让挤兑成为安全的选择。只要有任何不流动性，挤兑就有可能；它的代价取决于折价幅度。",

    'f"USD coin in March twenty twenty-three, minute by minute.':
        "2023年3月的USD币，逐分钟。<bookmark mark='a'/>硅谷银行在10日星期五倒闭；发行方Circle披露其储备中有三十三亿美元在那里。币安上该币对泰达币的序列"
        "在星期六下午开盘，价格为{u['low']:.3f}。<bookmark mark='b'/>它有{u['min_below98'] / 60:.0f}个小时低于九十八美分。<bookmark mark='c'/>"
        "星期日晚上，美国当局为该银行的全部存款提供担保，到最低点后{u['hours_to_995']:.0f}小时，这枚币回到了九十九点五美分以上。",

    'f"Read the price.':
        "读懂价格。<bookmark mark='a'/>约百分之八的储备在倒闭的银行。<bookmark mark='b'/>即使一分钱也收不回，其余储备也能覆盖约九十二美分。"
        "<bookmark mark='c'/>但它的成交价是{u['low']:.2f}：甚至低于最坏情形，因为赎回要通过周末关门的银行，急需美元的持有者只能求助于市场。"
        "决定价格的是流动性，而不是偿付能力。",

    "What normally holds the peg is Part thirty-eight's ETF arbitrage.":
        "平时维持锚定的是第38部分的ETF套利。<bookmark mark='a'/>低于一美元时，买入代币，向发行方赎回。<bookmark mark='b'/>高于一美元时，存入美元，铸造并卖出。"
        "<bookmark mark='c'/>但只有经过审核的客户才能这样做，而且只能在银行营业时间；正如Richard Lyons和Ganesh Viswanath-Natraj所示，锚定的紧密程度"
        "取决于进入这个窗口的通道。",

    "Terra, in May twenty twenty-two.":
        "2022年5月的Terra。<bookmark mark='a'/>协议把一个UST兑换成价值一美元的新铸LUNA，它的孪生代币。<bookmark mark='b'/>低于一美元时，套利者销毁UST、"
        "收到LUNA并卖出。<bookmark mark='c'/>这让LUNA涌入市场并压低它的价格，<bookmark mark='d'/>于是每一次新的赎回都会铸造出更多LUNA。防御在自我吞噬。"
        "据报道，对UST的需求主要依赖一个借贷协议Anchor，它为存款支付接近百分之二十的利息。",

    'f"On Binance, hour by hour.':
        "币安上，逐小时。<bookmark mark='a'/>UST月初为一美元，9日脱锚；到交易停止时，它接近{ut['last']:.2f}。<bookmark mark='b'/>LUNA在1日约为"
        "{lu['first']:.0f}美元，一周内下跌了六个数量级以上，因为赎回以万亿为单位印出了它。据报道，数百亿美元的市值灰飞烟灭。",

    "Three lessons. <bookmark mark='a'/> A coin backed by a token":
        "三条教训。<bookmark mark='a'/>由自身系统印出的代币支持的币，靠的是信心，而信心一旦消失，两者一起崩塌。<bookmark mark='b'/>传染：据报道，暴露于"
        "Terra且彼此关联的借贷机构在整个夏天相继倒闭，FTX在11月跟上，这是第41部分螺旋的微缩版。<bookmark mark='c'/>以及法律：据报道，Terraform Labs"
        "及其创始人在2024年被美国陪审团认定承担欺诈责任，创始人后来在一起刑事案件中认罪。",

    "And the rules that followed.":
        "以及随后的规则。<bookmark mark='a'/>在欧洲，MiCA法规的稳定币规则自2024年年中起适用。<bookmark mark='b'/>在美国，2025年7月的GENIUS法案要求以"
        "现金和短期国库券按一比一持有储备，并定期披露。<bookmark mark='c'/>但国库券储备是安全的，却不是即时的现金，周末的挤兑仍然会遇到关门的银行。",

    "Pause and predict. In early twenty eighteen,":
        "暂停并预测。2018年初，比特币在韩国比在美国贵出百分之几十，持续了好几周。为什么套利者没有消除这个差距？",

    # ------------------------------------------------------------------ Market
    "Chapter nine, and the answer to the pause: capital controls.":
        "第9章，以及暂停问题的答案：资本管制。套利者必须在一个国家买入、在另一个国家卖出，然后把钱转回来；韩国对韩元汇出和外国人在其交易所开户的限制，"
        "让第二条腿既慢又贵。一个没有收盘铃的市场，仍然可以有国界。",

    "Igor Makarov and Antoinette Schoar's study":
        "Igor Makarov和Antoinette Schoar对加密套利的研究。<bookmark mark='a'/>在同一个国家内，以同一种货币交易的交易所价格很接近，因为币和现金在它们之间"
        "很容易转移。<bookmark mark='b'/>跨越国界，差距大而持久：韩国的溢价在2018年初一度超过百分之四十。<bookmark mark='c'/>而且买入压力上升时，这些差距"
        "一起扩大。稀缺的是能够跨越国界的套利资本，而不是信息。",

    "Where the price is made.":
        "价格在哪里形成。<bookmark mark='a'/>第35部分的信息份额发现，比特币的价格主要在永续合约上被发现，那里的杠杆最便宜。<bookmark mark='b'/>链上的池子"
        "很少领先；第3章的套利者把价格带给它们。<bookmark mark='c'/>周末加密市场照常交易，而芝加哥的期货和基金都休市，所以挂牌产品在星期一开盘时，"
        "会跳到加密市场已经去到的地方。",

    "Before the funds, a trust.":
        "在基金之前，是一只信托。<bookmark mark='a'/>灰度的比特币信托只创设份额，从不赎回。<bookmark mark='b'/>没有第38部分的申购和赎回，就没有什么把它的价格"
        "与它持有的比特币绑在一起：据报道，它多年溢价交易，在2022年则以接近一半的价值折价交易。<bookmark mark='c'/>与此同时，持有人一直按全部价值每年"
        "支付百分之二的费用。",

    'f"The discount closes.':
        "折价收窄。灰度比特币信托的价格除以比特币价格，以2022年底为一。<bookmark mark='a'/>它在2023年一路上升，8月美国上诉法院裁定监管机构拒绝该信托"
        "转为ETF的理由不成立之后，上升尤其陡峭。<bookmark mark='b'/>到2024年1月获批时，它高出了{100 * gb['rise']:.0f}%：折价几乎消失，因为赎回即将到来。"
        "每份额的比特币没有变；变的只是赎回它的权利。",

    'f"And the funds.':
        "还有基金。<bookmark mark='a'/>2024年1月11日，十一只现货比特币ETF开始交易。<bookmark mark='b'/>贝莱德的那只首日成交约{ib['first_day_bn']:.1f}"
        "十亿美元，<bookmark mark='c'/>全年平均每天约{ib['mean_bn']:.1f}十亿美元。<bookmark mark='d'/>它们的申购和赎回就是第38部分的套利，起初以现金进行；"
        "据报道，2025年起允许实物申赎。",

    "And the cross-section of coins.":
        "还有币的横截面。<bookmark mark='a'/>Yukun Liu、Aleh Tsyvinski和Xi Wu发现，三个因子，即加密市场、规模和动量，可以为币的横截面定价。"
        "<bookmark mark='b'/>Liu和Tsyvinski发现，加密收益几乎不暴露于股票、货币或商品的因子，而可以被动量和投资者关注度预测。<bookmark mark='c'/>"
        "第27部分的网络在七百零一个币上取得了一点二九的留出期夏普比率，扣除成本后为一点一三，但仍低于本系列到那时一万次试验所设定的门槛。",

    "Firms, from the public record.":
        "来自公开记录的公司。<bookmark mark='a'/>在2024年12月的一项和解令中，美国证交会认定，Jump Trading的关联公司Tai Mo Shan在2021年5月买入UST的方式"
        "误导了投资者对锚定机制的认识；它支付了一亿二千三百万美元，既不承认也不否认这些认定。<bookmark mark='b'/>新代币通过合同雇用做市商，报酬常常是"
        "该代币的期权；据报道，2024年的执法案件把其中一些安排描述为对倒交易的幌子。<bookmark mark='c'/>币安及其创始人在2023年就违反美国反洗钱和制裁规定"
        "认罪，支付了约四十三亿美元。",

    "Pause and predict. The House opens a digital-assets desk":
        "暂停并预测。本系列公司开设一个数字资产交易台，运行第7章的期现套利组合，并在池子里提供流动性。在第一笔交易之前，它的规则应设定哪三个限额？",

    # ------------------------------------------------------------------ House
    "The answer to the pause. <bookmark mark='a'/> First, venues":
        "暂停问题的答案。<bookmark mark='a'/>第一，交易场所：对任何一家交易所持有的抵押品设上限，因为期现套利组合真正的尾部是交易场所。<bookmark mark='b'/>"
        "第二，美元：对任何一种稳定币设上限，因为每一种都是没有保险的银行。<bookmark mark='c'/>第三，池子：只在手续费胜过实测的套利损失时提供流动性，"
        "并对冲代币敞口。",

    "Chapter ten. The House's thirty-ninth rule":
        "第10章。本系列公司的第39条规则属于它新开的数字资产交易台。它的策略拥有业绩记录中最平滑的收益，也有从不出现在收益中的最大风险。",

    "The first sheet. <bookmark mark='a'/> A pool that lost":
        "第一张汇总表。<bookmark mark='a'/>一个把方差的八分之一输给套利、精确到小数点后第二位的池子，以及比布朗运动理论所允许的拿走多得多的套利者。"
        "一个同时放大手续费和损失的集中区间。大部分时间被钉在利息项上的资金费率。一个夏普比率在样本外减半、却仍像白送钱一样的期现套利组合。还有一枚"
        "成交价到过八十八美分的美元代币。",

    "Venues. <bookmark mark='a'/> Spot sits with a regulated custodian":
        "交易场所。<bookmark mark='a'/>现货放在受监管的托管机构，只作为可召回的抵押品交给交易所；空头的保证金保持在最低水平附近。<bookmark mark='b'/>"
        "任何一家交易所持有的资本都不超过设定的比例，并定期测试提现。<bookmark mark='c'/>每家交易所都有一份第21部分式的信用档案：谁拥有它、谁审计它、"
        "它的负债和储备，以及客户资产在法律上存放在哪里。",

    "Contracts. <bookmark mark='a'/> On chain, the code is the counterparty":
        "合约。<bookmark mark='a'/>在链上，代码就是交易对手；据报道，跨链桥和协议的漏洞攻击一次就能卷走数亿美元。<bookmark mark='b'/>本系列公司只使用"
        "经过审计、记录很长、利害攸关的合约，并对每一个设敞口上限。<bookmark mark='c'/>它还检查每个协议读取的是什么价格，因为可被操纵的预言机可以用闪电贷掏空。",

    "Operations. <bookmark mark='a'/> No single person can move funds":
        "运营。<bookmark mark='a'/>任何单个人都不能转移资金：多个签名人，或用多方计算拆分的密钥，并有单笔交易限额。<bookmark mark='b'/>市场永不收盘，"
        "所以限额也永不休息：自动检查，以及一周每个小时都有值班交易员。<bookmark mark='c'/>第34部分的合规同样适用于链上：对地址进行制裁筛查，并记录每一笔交易。",

    "Chapter three's simulator at its core.":
        "第3章模拟器的核心。在每个区块里，如果池子扣除手续费后的价格高于市场，套利者就把代币卖给它，直到区间边缘；如果低于市场，就买入；在区间之内，什么也不发生。",

    "The research chapter in three lines:":
        "三行代码概括研究者章节：精确的单步损失、连续速率sigma平方的八分之一，以及一个区块包含套利的概率。",

    "Chapter five's attack:":
        "第5章的攻击：攻击者的买入、受害者的买入、攻击者的卖出；抢先交易的规模是让受害者仍在限度之内的最大值。",

    "And Chapter six: Binance's funding rule,":
        "还有第6章：币安的资金费率规则，即溢价加上一个被限制的利息项，以及永续合约相对现货的无套利倍数。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>池子、池子亏掉了什么，以及交易顺序和永续合约。<bookmark mark='b'/>还有第39条规则。本系列公司以再平衡为基准"
        "评估每一个池子头寸，按套利的频率、并考虑肥尾。它对任何一家交易场所的抵押品和任何一种稳定币的敞口设上限。它按失去一个交易场所的损失来确定"
        "期现套利的规模，而不是按它的夏普比率。",

    "The rule against three cases.":
        "用三个案例检验这条规则。<bookmark mark='a'/>一个以手续费收益率做广告的池子：问它输给套利的损失，因为只有手续费没有损失，账只算了一半。"
        "<bookmark mark='b'/>一只夏普比率为四的基差基金：问抵押品放在哪里、用的是哪种稳定币，以及一家交易场所倒闭会损失多少。<bookmark mark='c'/>"
        "一枚支付百分之二十的稳定币：问它由什么支持，以及谁在支付这份收益。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter three measured":
        "写给研究者。第3章测量了池子输给套利者的损失。本章证明它背后的公式，来自Jason Milionis、Ciamac Moallemi、Tim Roughgarden和Anthony Lee Zhang；"
        "推导精确的离散版本；证明手续费和区块时间如何决定套利者留下多少；并用模拟和以太币的真实价格检验每一个结果。",

    "The model. <bookmark mark='a'/> The market price follows":
        "模型。<bookmark mark='a'/>市场价格服从波动率为sigma的鞅。<bookmark mark='b'/>一个被连续套利的池子，位于其曲线上按市场价格计最便宜的那一点："
        "否则套利者会对任何其他点交易。这就定义了它的持仓x星和y星，都是P的函数。<bookmark mark='c'/>池子的价值是P乘x星加y星。<bookmark mark='d'/>"
        "基准是：一个在每一时刻都持有同样数量代币、但按市场价格交易的组合。它的收益是x星乘以dP。",

    "Lemma one. <bookmark mark='a'/> The pool's value is a minimum":
        "引理一。<bookmark mark='a'/>池子的价值是在其曲线上、对价格为线性的函数的最小值。<bookmark mark='b'/>所以它是凹的。<bookmark mark='c'/>由包络定理，"
        "它的导数就是持仓本身：V对P的导数等于x星。一阶近似下，池子价值的变动和它的持仓完全一样。",

    "Lemma two. <bookmark mark='a'/> The second derivative":
        "引理二。<bookmark mark='a'/>二阶导数就是持仓的斜率，凹性使它小于或等于零。<bookmark mark='b'/>价格上涨时池子卖出代币，下跌时买入：它总是逆着走势交易。"
        "这就是损失的全部来源。",

    "The theorem. <bookmark mark='a'/> The rebalancing portfolio minus the pool":
        "定理。<bookmark mark='a'/>再平衡组合减去池子，称为相对再平衡损失，是一个持续速率的积分：sigma平方P平方除以二，乘以持仓斜率的绝对值。"
        "<bookmark mark='b'/>它从不为负，以可预测的速率累积，而且与无常损失不同，它不在乎路径终点在哪里。",

    "The proof is three lines.":
        "证明只有三行。<bookmark mark='a'/>对池子的价值用伊藤公式。<bookmark mark='b'/>引理一把一阶导数变成持仓，引理二给出二阶导数的符号。<bookmark mark='c'/>"
        "减去再平衡组合的收益：随机部分恰好抵消，剩下的是纯粹的漂移，即二分之一sigma平方P平方乘以斜率。积分，就是定理。",

    "Two corollaries.":
        "两个推论。<bookmark mark='a'/>对恒定乘积池，速率是sigma平方的八分之一乘以池子的价值：第3章的公式。<bookmark mark='b'/>对集中头寸，在区间内是"
        "sigma平方的四分之一乘以流动性乘以根号P，区间外为零。<bookmark mark='c'/>用数字说，在百分之五十的波动率下，恒定乘积池每年损失约其价值的百分之三。"
        "它的手续费必须超过这个数。",

    "This part adds an exact discrete version.":
        "这一部分补充一个精确的离散版本。<bookmark mark='a'/>在一步之内，池子只在末尾被套利一次，损失等于再平衡收益减去池子价值的变化。<bookmark mark='b'/>"
        "对恒定乘积池，它是一个完全平方：价值的一半乘以价格比的平方根减一的平方。对任意大小的步长都精确成立。<bookmark mark='c'/>对一个对数正态的步长，"
        "它的期望是V乘以一减去e的负sigma平方delta t除以八次方，<bookmark mark='d'/>步长缩小时趋于连续速率。",

    'f"Check one: simulation.':
        "检验一：模拟。<bookmark mark='a'/>四十万步对数正态价格，池子每一步都被交易到市场价格。<bookmark mark='b'/>逐步累加的精确恒等式与模拟的损失"
        "在舍入误差内相等。<bookmark mark='c'/>连续公式的误差在{100 * abs(r['ratio'] - 1):.2f}%以内。",

    'f"Check two: a concentrated position.':
        "检验二：集中头寸。<bookmark mark='a'/>沿着同类路径的一个从六十到一百六十的区间，{100 * v['in_range']:.0f}%的时间在区间内。<bookmark mark='b'/>"
        "模拟的损失与定理在区间外关闭的速率相差不到{100 * abs(v['sim'] / v['theory'] - 1):.1f}%。",

    'f"Check three: ether in twenty twenty-three':
        "检验三：2023年的以太币，也就是暂停问题里的池子。<bookmark mark='a'/>逐分钟计，这个池子全年把其价值的{lv['lvr_pct']:.2f}%输给了套利，"
        "而已实现方差的八分之一给出{lv['rv8_pct']:.2f}%：逐月相等，从平静月份的{lo:.2f}%到3月的{hi:.2f}%。<bookmark mark='b'/>"
        "这个公式完全不需要价格模型：只需要池子被套利那个频率上的已实现方差。",

    "Now fees and blocks, after Milionis, Moallemi and Roughgarden.":
        "现在加入手续费和区块，依照Milionis、Moallemi和Roughgarden。<bookmark mark='a'/>设z为错价，即市场价格与池子价格之比的对数。<bookmark mark='b'/>"
        "在宽度为gamma，也就是手续费的区间之内，任何套利都不划算。<bookmark mark='c'/>池子只能在区块到来时被交易，区块以泊松速率lambda到达。"
        "<bookmark mark='d'/>如果区块到来时z在区间之外，套利者就把池子交易回区间边缘。在区块之间，z像布朗运动一样游走。",

    "Lemma three: the mispricing's stationary law.":
        "引理三：错价的平稳分布。<bookmark mark='a'/>在区间之内没有什么移走概率，所以密度是平的。<bookmark mark='b'/>在区间之外，每个区块以速率lambda"
        "移走概率质量并把它送回边缘，所以密度以根号二lambda除以sigma的速率指数衰减。<bookmark mark='c'/>归一化。<bookmark mark='d'/>泊松到达看到的是"
        "时间平均，所以一个区块发现套利机会的概率就是区间外的质量：一除以一加gamma乘根号二lambda除以sigma。",

    "The theorem. <bookmark mark='a'/> The trade probability":
        "定理。<bookmark mark='a'/>交易概率是一除以一加eta，其中eta等于gamma乘根号二lambda除以sigma。套利者的利润在一阶近似下等于这个概率乘以LVR。"
        "<bookmark mark='b'/>所以手续费并不缩小相对再平衡组合的损失：它们把损失分给套利者和池子自己的手续费收入。区块越快、手续费越低，套利者拿走的越多。",

    'f"Check four: Poisson blocks in simulation,':
        "检验四：模拟中的泊松区块，波动率百分之八十，平均十二秒一个区块。<bookmark mark='a'/>每个区块之前测得的错价：区间内是平的，区间外指数衰减，"
        "正是引理三的密度。<bookmark mark='b'/>在从万分之一到百分之一的各种手续费下，有交易的区块比例都与公式吻合；在千分之三时，研究运行中为"
        "{t['p_trade']:.3f}，理论为{t['theory']:.3f}。套利利润与LVR之比也几乎完全跟随它。",

    'f"But Ethereum\'s blocks are not Poisson:':
        "但以太坊的区块不是泊松的：自2022年起，它们像时钟一样每十二秒一个。<bookmark mark='a'/>在固定区块下，交易比泊松公式略多，而套利者留下的更少："
        "在千分之三时，是LVR的{f3['arb_lvr']:.3f}，公式为{f3['theory']:.3f}。规则的时钟让错价跑到区间外很远的时间更少。",

    'f"Check five: ether\'s real minutes':
        "检验五：以太币2023年的真实分钟数据，池子每分钟被套利一次。<bookmark mark='a'/>交易比布朗公式预测的少，但套利者留下的多得多：在千分之三时，"
        "是LVR的{f3['arb_lvr']:.2f}，约为公式的{ratio:.1f}倍。<bookmark mark='b'/>真实价格大多数分钟都很平静，只在少数分钟跳动，而一次跳动会把错价带到"
        "区间外很远的地方，那里的每一点都是利润。布朗定理对布朗价格是精确的；对真实价格，它低估了套利者拿走的，也高估了手续费还回来的。",

    "What it means. <bookmark mark='a'/> For liquidity providers":
        "这意味着什么。<bookmark mark='a'/>对流动性提供者，基准是LVR而不是无常损失：手续费收入要和价值的sigma平方的八分之一比较，按套利的频率测量，"
        "并考虑肥尾。<bookmark mark='b'/>对池子设计者，手续费只是重新分配损失；要减少它，就要拍卖套利的权利，或让手续费随波动率上升。<bookmark mark='c'/>"
        "对本系列公司：用永续合约对冲的池子赚的是手续费减去LVR，是一个方差空头。它就是第11部分的负伽马，写在了区块链上。",

    "Where this sits. <bookmark mark='a'/> Milionis, Moallemi, Roughgarden and Zhang":
        "这项工作的位置。<bookmark mark='a'/>Milionis、Moallemi、Roughgarden和Zhang定义了LVR并证明了它的速率；Milionis、Moallemi和Roughgarden加入了"
        "手续费和区块。<bookmark mark='b'/>Agostino Capponi和Ruizhe Jia研究了手续费在提供者与套利者之间的权衡，Andreas Lehar和Christine Parlour研究了"
        "谁在Uniswap上提供流动性。<bookmark mark='c'/>Angeris、Chitra及合作者发展了这些市场的凸几何、它们的预言机和路由。",

    "Three open questions. <bookmark mark='a'/> Fat tails:":
        "三个开放问题。<bookmark mark='a'/>肥尾：当价格跳动时，正如检验五所示，什么取代一除以一加eta，手续费又该如何应对？<bookmark mark='b'/>最佳机制："
        "一个每个区块拍卖套利权利、或动态设定手续费的池子。池子最多能挽回多少？<bookmark mark='c'/>以及同时存在许多池子：同一交易对分布在手续费和区间各不相同的"
        "池子里，而套利者在所有池子之间路由。",

    "Pause and predict. A constant-product pool's volatility doubles":
        "暂停并预测。一个恒定乘积池的波动率翻倍，手续费和区块速率不变。如果原来eta等于一，它的相对再平衡损失会怎样？套利者拿走的份额又会怎样？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-nine in thirteen lines.":
        "用十三行回顾第39部分。加密资产在托管型交易所和链上合约中交易，FTX说明了托管意味着什么。池子的价格是其储备之比，由套利者保持诚实。无常损失只取决于"
        "价格最终停在哪里；输给套利的损失取决于路径，等于池子价值的方差八分之一，以太币的2023年把它确认到小数点后第二位。集中同时放大手续费和损失，"
        "而学习型提供者唯一的本领是在波动率高时停止卖出波动率。",

    "The order of transactions is worth money.":
        "交易的顺序就是钱。资金费率把永续合约拴在现货附近，在比特币上，超过三分之一的结算恰好等于利息项。登记在案的期现套利组合兑现了约一半的承诺，"
        "夏普比率仍然很高，而它真正的尾部是交易场所。稳定币是没有保险的银行。研究者章节证明了输给套利的损失，以及手续费和区块如何分配它。还有本系列公司的规则："
        "清点收益里看不到的风险。",

    "Three lessons. <bookmark mark='a'/> The old models, in new clothes":
        "三条教训。<bookmark mark='a'/>旧模型，新外衣：池子是一个永远被狙击的做市商，永续合约是带资金费时钟的期货，稳定币是一家狭义银行。<bookmark mark='b'/>"
        "用正确的基准衡量：再平衡组合去掉市场敞口，留下成本。<bookmark mark='c'/>回测显示的是市场，而不是管道：交易场所、合约、密钥和锚定会以任何收益序列"
        "都不包含的方式失败。",

    "The part on one card.":
        "一张卡片上的这一部分。无常损失。LVR速率及其恒定乘积形式。精确的单步损失。区间的资本效率。带手续费和区块的交易概率，以及套利利润。还有永续合约的无套利价格。",

    "How this part connects.":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>往回看：第38部分的过时报价就是池子的过时价格，第11部分的负伽马就是提供者的负伽马，第22部分的套息"
        "就是资金费率，第2部分的保证金账户就是永续合约的保证金账户。<bookmark mark='b'/>横向看：第21部分的交易对手风险就是交易场所风险，第9部分的期货是永续合约"
        "有到期日的亲戚。<bookmark mark='c'/>往前看：第40部分在一个有肥尾、不收盘的市场里测量风险，第41部分的螺旋在2022年贯穿了加密市场，第42部分的机器"
        "包括它的机器人。",

    "Six desk questions. A provider's loss against holding":
        "六个交易台问题。价格翻倍时提供者相对持有的损失？百分之五点七，但正确的度量是相对再平衡的损失。<bookmark mark='a'/>池子输给套利的是什么？"
        "其价值方差的八分之一。<bookmark mark='b'/>为什么要集中流动性？为了放大一个“手续费胜过方差”的赌注，所以在波动率高时不要这样做。",

    "What keeps a perpetual near spot? Funding.":
        "是什么让永续合约贴近现货？资金费率。<bookmark mark='a'/>期现套利是白送的钱吗？不是：它是一种溢价，带着一条任何回测都装不下的尾巴。"
        "<bookmark mark='b'/>稳定币什么时候会崩？当它的储备在赎回的那一刻缺乏流动性，或者储备就是它自己的代币时。完整解答见讲义。",

    "The research chapter's pause, answered.":
        "研究者章节暂停问题的答案。<bookmark mark='a'/>相对再平衡损失与方差成正比，所以变为四倍。<bookmark mark='b'/>而eta与波动率成反比，从一减半到二分之一，"
        "所以交易概率从二分之一升到三分之二：套利者拿走一个大了四倍的损失的三分之二，手续费挽回的份额更小。",

    "And twelve problems: impermanent loss;":
        "还有十二道习题：无常损失；曲线上一笔交易的成本；以美元计的LVR；精确的单区块损失；区间的效率；交易概率；期现套利组合的收益；永续合约的溢价；"
        "抵消套利收益的交易场所风险；以及一场挤兑。然后是两道资格考试题：完整的LVR定理，以及带手续费和泊松区块的套利。中英文解答见讲义。",

    "Where this comes back. Part forty measures risk":
        "这些内容会在哪里再出现。第40部分在有肥尾、不收盘的市场里测量风险。第41部分追踪杠杆和流动性螺旋，加密市场的2022年就是一条连锁反应。第42部分构建"
        "交易、报价和安排区块的机器。第43部分追问是否有人能战胜市场。",

    "The textbooks this part follows, and the papers it draws on, from Diamond":
        "这一部分所依据的教科书和论文，从Diamond和Dybvig的银行挤兑到相对再平衡损失的理论。屏幕上的每个数字，都是本系列公司的代码根据币安的公开数据档案、"
        "雅虎财经的K线或模拟算出来的。",

    "Act six is complete:":
        "第六幕完成了：本系列公司现在能看清谁和谁交易、读懂订单簿、执行、做市，并在链上交易，它的交易台全部开张。<bookmark mark='a'/>接下来是第七幕，体系。"
        "第40部分：测量风险。在险价值、预期亏损，以及如何判断一个风险模型是否有效。",
}
