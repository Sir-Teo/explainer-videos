"""Chinese narration for quant38: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 做市商 (market maker), 即时性 (immediacy), 返佣 (rebate), 事后损益
(markout), 存货 (inventory), 保留价格 (reservation price), 成交强度 (fill intensity), 狙击 (sniping), 延迟套利 (latency
arbitrage), 频繁批量拍卖 (frequent batch auctions), 减速带 (speed bump), 交易所交易基金 (ETF), 授权参与者 (authorised
participant), 申购/赎回 (creation/redemption), 基金净值 (NAV), 溢价/折价 (premium/discount), 杠杆基金 (leveraged ETF),
按比例分配 (pro rata), 囚徒困境 (prisoner's dilemma)."""

TITLE = '量化金融，从零搭建 · 第38部分：做市、交易所交易基金与速度竞赛'

CHAPTERS = {
    'Hook': '做市商靠什么谋生？',
    'Business': '1. 做市商的生意',
    'Tape': '2. 在成交记录上做市',
    'Fills': '3. 成交率与最优报价',
    'Tick': '4. 跳价大小与队列位置',
    'ETF': '5. 为交易所交易基金做市',
    'Speed': '6. 速度竞赛',
    'Industry': '7. 快速做市的经济学',
    'House': '8. 第38条规则：只报你能测量的价',
    'Research': '写给研究者：狙击均衡',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-eight. Market making, exchange-traded funds":
        "第38部分。做市、交易所交易基金与速度竞赛：前三部分里每一笔订单另一边的生意，以及它为什么变成了一场以微秒计的较量。",

    "A simple description of market making.":
        "对做市的一个简单描述。<bookmark mark='a'/>在买价买入，在卖价卖出，赚取价差。<bookmark mark='b'/>在比特币永续合约上，价差是一跳："
        "约万分之零点零四。<bookmark mark='c'/>那么，到底有谁能靠这个赚钱？这一部分在真实的成交记录上测量答案。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>在最优价位报价会亏钱：在成交记录上回放的做市商，每笔成交约亏{abs(d['slow']['pnl_per_fill']):.0f}跳；"
        "即使是能在每次扫单之前撤单的做市商，也亏{abs(d['fast']['pnl_per_fill']):.0f}跳。<bookmark mark='b'/>在同一份记录上拟合的最优报价模型说，"
        "应在约三十跳之外报价，而那么远的报价在不计排队和手续费时确实赚钱。<bookmark mark='c'/>速度竞赛是一个均衡，研究者章节会证明："
        "它的价差不取决于有多少家公司参赛，而批量拍卖会拿走这份奖金。",

    "Why it matters. <bookmark mark='a'/> Electronic market makers":
        "为什么这很重要。<bookmark mark='a'/>如今，股票、期货、期权、外汇和加密市场里大部分可见的流动性都由电子做市商提供，这份工作过去由银行"
        "用资产负债表来做。<bookmark mark='b'/>他们出售的是即时性：现在就能以已知价格成交的权利，对手方会承担风险，直到另一边到来。"
        "<bookmark mark='c'/>第37部分的每一笔订单都与他们成交，而同样的生意以ETF套利的形式，让基金价格贴近其持仓的价值。",

    "Three things market making is not.":
        "做市不是什么。<bookmark mark='a'/>它不是赌方向：做市商希望一天结束时仓位为零，存货只是为吃单者服务的副产品。"
        "<bookmark mark='b'/>它不是从价差里白拿钱：价差只是毛利，在最活跃的市场上，成本比它更大。<bookmark mark='c'/>它也不是一个市场："
        "做市商真正的账本是一个跨越数千种工具和交易场所、互相轧差并对冲的组合。",

    "Where this sits. Part thirty-five met the dealer in theory":
        "这一部分的位置。第35部分在理论中认识了交易商；第36部分测量了队列，第37部分测量了执行者的成本。这一部分经营交易商的生意，"
        "结束第六幕对微观结构的考察，之后第39部分转向加密货币与去中心化金融。",

    "Fifty years of the dealer's problem.":
        "交易商问题的五十年。先是Mark Garman的存货模型，接着是Thomas Ho和Hans Stoll；Glosten和Milgrom的逆向选择；1993年美国第一只ETF。"
        "<bookmark mark='a'/>然后是Avellaneda和Stoikov的最优报价、闪电崩盘、Guéant、Lehalle和Fernandez-Tapia的闭式解，以及Albert Menkveld"
        "对一家高频做市商的研究。<bookmark mark='b'/>再到速度竞赛：批量拍卖被提出、减速带获批、高频交易的经济学、2020年3月的债券ETF，"
        "以及在伦敦证券交易所测得的竞赛。",

    "The plan: the maker's profit and loss":
        "计划如下：做市商的损益；在比特币成交记录上回放的做市商；成交率以及它所蕴含的最优报价；跳价大小与被钉住的价差中的租金；"
        "ETF做市与2020年3月；速度竞赛与高频交易的经济学；最后证明狙击均衡。",

    "In the House, the market-making desk opens":
        "在本系列公司里，做市台在执行台旁边开张：一个出售即时性，一个购买即时性，每一方都必须知道另一方在付多少钱。",

    # ------------------------------------------------------------------ Business
    "Chapter one. A market maker posts prices":
        "第1章。做市商挂出愿意买入和卖出的价格，让别人来选择。它的利润，是付给每一个因为知道得更多或者更快而选择与它交易的人之后剩下的部分。",

    "The profit and loss. <bookmark mark='a'/> Half the spread on every fill":
        "损益。<bookmark mark='a'/>每笔成交赚一半价差，加上交易场所对挂单流动性的返佣，减去逆向选择，再加上存货随价格变动带来的盈亏。"
        "<bookmark mark='b'/>逆向选择用事后损益来衡量：成交之后中间价朝吃单者方向移动了多远。<bookmark mark='c'/>所以每笔成交的优势等于半价差加返佣，"
        "减去预期的事后损失。只有当吃单者所知道的东西不如他们付出的多时，它才是正的。",

    "Three risks. <bookmark mark='a'/> Adverse selection":
        "三种风险。<bookmark mark='a'/>逆向选择：吃单者知道些什么，要么是私人信息，要么只是对公开消息读得更快。<bookmark mark='b'/>存货："
        "每笔成交都留下一个仓位，在另一边到来之前，做市商承担它的价格风险。<bookmark mark='c'/>还有运营：一个出故障几分钟的报价引擎，"
        "可能亏掉超过一年的价差收入。据报道，Knight Capital在2012年8月不到一小时内亏损约4.4亿美元。",

    "What a spread pays for.":
        "价差为什么付费。<bookmark mark='a'/>Hans Stoll以及后来Roger Huang和Stoll的经典分解有三部分。<bookmark mark='b'/>订单处理："
        "手续费、技术、资本。<bookmark mark='c'/>存货：在另一边到来之前持有仓位的风险。<bookmark mark='d'/>以及逆向选择：信息更多或速度更快的"
        "对手方赢走的部分。在比特币永续合约上，第三部分大到价差无法覆盖，下一章会说明。",

    "Part eleven derived the classic model.":
        "第11部分推导过经典模型。<bookmark mark='a'/>在Avellaneda和Stoikov的做市商中，保留价格随存货下降，降幅等于风险厌恶乘以仍需承担的方差。"
        "<bookmark mark='b'/>总价差有一个风险项，以及一个来自报价成交频率与每笔成交收益之间权衡的项。<bookmark mark='c'/>它依赖一个假设："
        "距离为delta的报价按泊松速率A乘e的负k乘delta次方被打到，与价格接下来去哪里无关。第3章会在成交记录上检验这个假设。",

    "The core trade-off in one line.":
        "一句话说清核心权衡。<bookmark mark='a'/>距离为delta的报价每笔成交赚delta，成交速率随delta下降。<bookmark mark='b'/>最大化单位时间收入，"
        "答案是delta等于k分之一：每个公式里的基础项。<bookmark mark='c'/>其余的一切都关于存货：报价要倾斜多少，才能把买进来的东西甩掉。",

    'f"In numbers.':
        "用数字来看。<bookmark mark='a'/>一个示例做市商：风险厌恶十分之一，仍需承担的方差为4，成交衰减为1.5。<bookmark mark='b'/>总价差是"
        "{total:.2f}，大部分是成交率项，接近k分之二；风险项只加了0.4。<bookmark mark='c'/>持有两个单位时，它把报价中心放在中间价下方0.8，"
        "以便多卖少买。",

    "And its practical form.":
        "以及它的实用形式。<bookmark mark='a'/>Guéant、Lehalle和Fernandez-Tapia证明，在有存货上限的长时间范围里，最优距离会变得平稳："
        "一个基础距离，风险厌恶小时接近k分之一，再加上一个与存货成正比的倾斜。<bookmark mark='b'/>卖价是买价的镜像：多头做市商卖得更便宜、"
        "买得更少。<bookmark mark='c'/>每单位的倾斜随波动率和风险厌恶增加，随成交率下降。其中的一切都可以从成交记录中估计。",

    "How we got here.":
        "我们是怎么走到今天的。<bookmark mark='a'/>纽约证券交易所曾经给每只股票指定一位专家，他能看到订单簿，并有义务维持市场有序。"
        "<bookmark mark='b'/>1994年，William Christie和Paul Schultz发现纳斯达克的交易商几乎从不报奇数个八分之一美元，使价差保持在四分之一美元；"
        "随后是调查和一笔巨额和解。<bookmark mark='c'/>2001年的十进制报价和电子订单簿终结了这两种模式：价差大幅收窄，做市变成了技术的较量。",

    "Who does it today.":
        "今天由谁来做。<bookmark mark='a'/>在美国股票市场，批发商在交易所之外内部化大部分零售订单，并为订单流向券商付费。<bookmark mark='b'/>"
        "电子做市商同时在交易所为数千种工具报价；正如第34部分所讨论的，Virtu披露在约一千二百个交易日中只有一天亏损。<bookmark mark='c'/>"
        "有些交易场所与指定做市商签约，要求他们在一天中的最低比例时间内、以不超过某个上限的价差报价，作为交换获得返佣或优先权。",

    "Not all flow is equal.":
        "订单流并不平等。<bookmark mark='a'/>做市商的事后损益取决于它和谁交易：零售订单小，很少有信息；而快速套利者的订单从定义上就有信息。"
        "<bookmark mark='b'/>这就是批发商为零售订单向券商付费的原因，也是交易所上剩下的订单流迫使公开价差更宽的原因。<bookmark mark='c'/>"
        "按对手方、规模和时段划分的事后损益，是做市商最保密的统计数字。",

    "Real makers run many books at once.":
        "真正的做市商同时经营许多账本。<bookmark mark='a'/>一家为一千只股票做市的公司用股指期货对冲共同因子，把个股存货保持得很小："
        "高频版的第31部分风险模型。<bookmark mark='b'/>期权做市商为整个波动率曲面报价，并对冲它的希腊字母，就像第11部分那样。"
        "<bookmark mark='c'/>在加密市场，同一个比特币在许多交易场所以现货和永续合约的形式交易：做市商在几个场所报价，在最便宜的地方对冲。",

    "Pause and predict. A maker joins the best bid and offer":
        "暂停并预测。一个做市商加入比特币永续合约的最优买价和卖价，并在价格移动时重新加入。在赚到半跳价差之后，一分钟后它每笔成交的平均利润是多少？",

    # ------------------------------------------------------------------ Tape
    "f'Chapter two, and the answer to the pause":
        "第2章，以及暂停问题的答案：每笔成交约亏{abs(d['pnl_per_fill']):.0f}跳。半跳的价差是真实的，但每笔成交之后都有一个四十倍大的不利变动。"
        "本章展示钱去了哪里。",

    "The maker. <bookmark mark='a'/> It joins the best bid":
        "这个做市商。<bookmark mark='a'/>它以极小的数量排到最优买价和最优卖价各自队列的末尾。<bookmark mark='b'/>每十分之一秒检查一次订单簿，"
        "如果最优价格离开了，就撤单并重新加入。<bookmark mark='c'/>它在任一方向最多持有五个单位。<bookmark mark='d'/>它的成交来自第36部分"
        "用真实成交对真实队列的回放。",

    'f"The result for a whole day':
        "整整一天的结果，5月17日。<bookmark mark='a'/>慢速做市商成交{s['n']:,}次。每次赚半跳，然后在同一个十分之一秒内亏约"
        "{abs(s['step']):.0f}跳，每笔成交总计亏{abs(s['pnl_per_fill']):.0f}跳。<bookmark mark='b'/>一个理想化的快速做市商，在任何扫单打到之前"
        "就撤单，成交次数减半，亏{abs(f['pnl_per_fill']):.0f}跳。<bookmark mark='c'/>再加上第36部分的不平衡警告，撤掉受威胁的一侧，亏损降到每笔"
        "{abs(ff['pnl_per_fill']):.1f}跳。仍然是亏损。",

    "Where the money goes, per fill.":
        "每笔成交，钱去了哪里。<bookmark mark='a'/>赚到半跳。然后在成交的那个十分之一秒里，中间价朝不利于做市商的方向移动，这是迄今最大的一块；"
        "接着在下一秒、下十秒、之后一分钟又亏一些。<bookmark mark='b'/>大部分亏损在一个每十分之一秒才看一次的做市商能够反应之前就已注定。",

    "The markout over time, for the three makers.":
        "三个做市商的事后损益随时间的变化。<bookmark mark='a'/>都从正半跳开始。慢速做市商在成交的十分之一秒内立刻下跌；快速的跌得慢一些，"
        "在随后几秒里下跌。<bookmark mark='b'/>一分钟后，三者都低于零，过滤的那个最少。速度决定了在你能反应之前有多少变动已经发生；"
        "预测决定了你究竟接受多少订单流。",

    "What the filter does.":
        "过滤器起什么作用。<bookmark mark='a'/>撤掉不平衡所威胁的一侧，去掉了快速做市商近三分之二的成交。<bookmark mark='b'/>留下的成交在第一秒内"
        "亏得更少。<bookmark mark='c'/>一天的总亏损缩小，主要是因为交易得少了。过滤器是一种拒绝最差订单流的方法，而不是赚取价差的方法。",

    "Who is on the other side of those fills?":
        "这些成交的另一边是谁？<bookmark mark='a'/>对其他交易场所作出反应的交易者：比特币的价格在许多交易所和现货市场上被发现，"
        "另一个场所一动，这里的报价就过时了。<bookmark mark='b'/>被迫的订单流：杠杆仓位的强平以一阵阵同方向的市价单到来。"
        "<bookmark mark='c'/>还有更快的做市商先撤单，所以扫单到来时留在最优价位上的，正是慢的那些报价。",

    'f"The price of slowness.':
        "慢的代价。<bookmark mark='a'/>慢速做市商会被每一次穿过它价格的扫单成交。<bookmark mark='b'/>理想化的快速做市商躲开了它们，只会被停在它价格上的"
        "成交打到。<bookmark mark='c'/>两者之差，每笔约{gap:.0f}跳，正是速度竞赛所争夺的：在价格穿过你之前撤出的能力。第6章会把它写进模型。",

    'f"And its inventory.':
        "再看它的存货。<bookmark mark='a'/>唯一的控制是每个方向五个单位的上限。<bookmark mark='b'/>存货的标准差是{d['slow']['inv_sd']:.1f}个单位，"
        "接近上限本身：扫单一次又一次地打同一侧。<bookmark mark='c'/>所以做市商一天中大部分时间被钉在某个上限上，只报一边，恰恰是订单流一边倒的时候。"
        "GLFT的倾斜会更早、更强地偏转。",

    'f"On three days, two weekdays and a Saturday.':
        "在三天里，两个工作日和一个星期六。<bookmark mark='a'/>排序从未改变：慢的最差，快的较好，快而过滤的最好，但从不为正；最好的一天是每笔"
        "{best:.1f}跳。一个没有自身预测、在最优价位、在这个市场上的报价规则，是在给它的对手方付钱。",

    'f"In basis points.':
        "换算成基点。<bookmark mark='a'/>一跳是{tb:.3f}个基点。<bookmark mark='b'/>所以最好规则的亏损约为每笔{need:.2f}个基点。<bookmark mark='c'/>"
        "每笔成交有这么大的返佣才刚好打平。标准的挂单手续费是反方向的，所以这门生意只属于手续费等级最低、真正够快、预测比我们更好的公司。",

    "What the replay leaves out":
        "回放遗漏了什么，免得结论被夸大。<bookmark mark='a'/>真正的做市商以微秒反应；我们的快速做市商是理想化的，回放也看不到十分之一秒以内的事。"
        "<bookmark mark='b'/>真正的做市商占据队列前端的位置，第36部分发现那里的成交毒性小得多。<bookmark mark='c'/>它们还在其他场所对冲。"
        "教训依然成立：价差本身几乎什么都付不起。",

    "Pause and predict. Avellaneda and Stoikov's model assumes":
        "暂停并预测。Avellaneda和Stoikov的模型假设报价的成交速率随它离中间价的距离指数衰减。用比特币的成交记录拟合，它的最优报价会离中间价多远："
        "一跳、五跳，还是三十跳？",

    # ------------------------------------------------------------------ Fills
    'f"Chapter three, and the answer to the pause: about':
        "第3章，以及暂停问题的答案：约{half:.0f}跳，离中间价三美元，而不是一跳。用比特币成交记录拟合的模型说，要远离中间价报价。"
        "本章说明原因，并检验它是否正确。",

    "How to measure fill rates.":
        "如何测量成交率。<bookmark mark='a'/>在每一秒开始时，想象在离中间价各个距离上都有报价。<bookmark mark='b'/>数一数有多少比例的秒里，"
        "有吃单成交达到了那个价格。<bookmark mark='c'/>把它换算成泊松强度。<bookmark mark='d'/>再拟合指数函数：在对数坐标上是一条直线，斜率就是k。",

    'f"On Bitcoin\'s perpetual. <bookmark mark=\'a\'/> A quote half a tick':
        "在比特币永续合约上。<bookmark mark='a'/>离中间价半跳的报价，在约三分之一的秒里会被达到；四十五跳之外的，约二十分之一。"
        "<bookmark mark='b'/>拟合得到k为每跳{f['k']:.3f}：强度每过{half_d:.0f}跳才减半。在第一跳之后衰减很慢，因为比特币一动就动很多跳，"
        "即第36部分的扫单。最前面的那个点高于直线：最优价位是特殊的。",

    'f"Is the fit stable?':
        "拟合稳定吗？<bookmark mark='a'/>逐日来看，k分别是{k0:.3f}和{k1:.3f}：更繁忙的工作日衰减更慢，因为更大的扫单走得更远。"
        "参数随市场状态变化，所以真正的交易台会在一天中不断重新估计，报价也随之变宽变窄。",

    'f"Feed Bitcoin\'s fill rates and volatility':
        "把比特币的成交率和波动率代入Guéant、Lehalle和Fernandez-Tapia的公式。<bookmark mark='a'/>风险厌恶很小时，最优半价差约为"
        "{r0['half_spread']:.0f}跳，几乎全部是基础项k分之一。更大的风险厌恶会让报价更宽、随存货倾斜得更厉害：gamma为百分之一时是"
        "{r2['half_spread']:.0f}跳，每多持有一个单位再加{r2['skew']:.0f}跳。离最优价位远得很。",

    'f"Is the model right?':
        "模型对吗？在成交记录上检验。在每一秒开始时，在离中间价delta跳处挂单；任何达到它们的成交都让它们成交；用一分钟后的中间价给每笔成交标价。"
        "<bookmark mark='a'/>靠近最优价位，成交是毒药：五跳处，每笔{r5['pnl60']:.0f}跳。<bookmark mark='b'/>亏损随距离缩小，在三十跳附近穿过零，"
        "那里是{r30['pnl60']:+.0f}，四十五跳处是{r45['pnl60']:+.0f}。模型给出的距离，大约就是开始赚钱的地方。",

    'f"Per hour, for one unit at each distance.':
        "按小时计，每个距离一个单位。<bookmark mark='a'/>两跳之外，成交很多，每笔都亏：每小时约亏{abs(r2['per_hour60']):,.0f}跳。"
        "<bookmark mark='b'/>三十跳之外，大约打平。<bookmark mark='c'/>四十五跳之外，每小时约赚{r45['per_hour60']:,.0f}跳，在这个乐观的检验里，"
        "每个比特币的报价约七百美元。真实的深档位是共享的，要付手续费，还要承担存货。",

    'f"Why far quotes earn.':
        "为什么远处的报价能赚钱。<bookmark mark='a'/>扫单的吃单者付出的价格超过中间价最终停下的地方；远处的报价被这段超调成交，然后中间价会朝它回来。"
        "<bookmark mark='b'/>这样的成交很少，在四十五跳处每小时约{r45['fills_per_hour']:.0f}次，而在最优价位是数千次。<bookmark mark='c'/>"
        "而且这是一个上界：它假设我们的报价在该价位排第一，而真实的深档位也有自己的队列。",

    "What the model gets wrong.":
        "模型错在哪里。<bookmark mark='a'/>它假设成交与未来的价格变动无关：它说的是报价多久成交一次，而不是成交意味着什么。<bookmark mark='b'/>"
        "在成交记录上，最优价位的成交是消息，价格会朝不利于做市商的方向移动。公式落在大致正确的距离上，部分是出于错误的原因。<bookmark mark='c'/>"
        "修正方法是让成交率依赖于状态，并加入短期阿尔法，就像Cartea、Jaimungal和Jason Ricci所做的：第36部分依赖状态的预测是现成的输入。",

    "How alpha enters the quotes.":
        "阿尔法如何进入报价。<bookmark mark='a'/>在Cartea、Jaimungal和Ricci的模型中，报价以中间价加预期变动为中心，然后像之前一样加宽和倾斜。"
        "<bookmark mark='b'/>重要的预测，是报价可能停留的那段时间内的预测。<bookmark mark='c'/>在比特币上，第36部分按时间跨度的平均变动表是自然的输入，"
        "而不是在这里会过头的微观价格。",

    "Pause and predict. Bitcoin's perpetual sits at a one-tick spread":
        "暂停并预测。比特币永续合约几乎一直停在一跳的价差。如果跳价缩小十倍，价差会缩小十倍吗？谁会得益，谁会受损？",

    # ------------------------------------------------------------------ Tick
    "Chapter four, and the answer to the pause: no.":
        "第4章，以及暂停问题的答案：不会。在钉在一跳的订单簿上，更小的跳价只让价差收窄到竞争会把它推到的地方，并把竞争从队列位置转到价格上。"
        "吃单者从更窄的价差中得益；占据长队列前端的做市商失去他们的租金。",

    "A pinned spread.":
        "被钉住的价差。<bookmark mark='a'/>当做市商愿意接受的价差小于一跳时，<bookmark mark='b'/>价差停在一跳，队列变长：本来会互相压价的做市商"
        "无法压价。<bookmark mark='c'/>于是他们争夺优先权而不是价格，而优先权属于先到的人：一场速度竞赛。",

    'f"A rough calibration of the rent.':
        "对租金的粗略校准。<bookmark mark='a'/>吃单者每秒成交约{bt['lam_i']:.0f}次。<bookmark mark='b'/>五跳以上的跳动每秒约出现"
        "{bt['lam_j']:.2f}次，平均{bt['J']:.0f}跳。<bookmark mark='c'/>第6章的狙击模型把这些换算成约{bt['half']:.2f}跳的半价差。"
        "<bookmark mark='d'/>跳价强制为半跳。如果这个校准哪怕大致正确，被钉住的价差就比单靠竞争会定出的更宽，多出的部分是做市商通过提早排队来争夺的租金。"
        "这只是一个粗略估计，带有模型的全部简化。",

    "The race for the queue.":
        "争夺队列。<bookmark mark='a'/>第36部分给比特币队列前端的定价约为每笔订单十一跳：在末尾，成交是有毒的那些。<bookmark mark='b'/>做市商靠这些方法"
        "排到前面：在某个价格成为最优之前就挂单，在小幅波动中保留订单，在价位被清空后最快重新加入。<bookmark mark='c'/>有些交易场所用别的方式分配成交："
        "某些期货市场按数量比例分配，或者通过别人无法使用的挂单方式。",

    "Another way to share a pinned spread.":
        "分享被钉住的价差的另一种方式。<bookmark mark='a'/>时间优先，大多数股票和加密订单簿的规则，让速度买到位置。<bookmark mark='b'/>按比例撮合，"
        "用于某些利率期货，把每笔进来的订单按挂单数量的比例分给各个挂单。<bookmark mark='c'/>于是做市商挂出远多于自己想要的数量，因为成交随数量增长："
        "竞赛从速度转向数量，显示的深度夸大了人们真正想交易的量。",

    "Recall what the queue position is worth.":
        "回想一下队列位置值多少。<bookmark mark='a'/>在第36部分的回放中，排在比特币队列末尾的订单中位等待三秒，五分之四在一分钟内成交。"
        "<bookmark mark='b'/>排在前面，五分之一秒。<bookmark mark='c'/>前面的成交更早，而且对手是更小、信息更少的交易：被钉住的价差的租金就在那里收取。",

    "So what is the right tick?":
        "那么合适的跳价是多少？<bookmark mark='a'/>太大，价差由规则决定，队列很长，做市商在速度上花钱。<bookmark mark='b'/>太小，任何人都能以微不足道的"
        "金额插到队列前面，报价闪烁，最优档位变薄。<bookmark mark='c'/>Khalil Dayri和Mathieu Rosenbaum建议选择跳价，使平均价差略高于一跳，"
        "在那里价格竞争起作用，挂单也仍然值得。",

    "Fees move the economic spread off the grid.":
        "手续费让经济意义上的价差离开价格网格。<bookmark mark='a'/>报价价差停在一跳。<bookmark mark='b'/>双向跨越的吃单者付出一跳和两次吃单手续费。"
        "<bookmark mark='c'/>做市商赚一跳和两次返佣。所以手续费让即时性的真实价格可以不同于跳价，这就是挂单-吃单收费如何绕过被钉住的价差，"
        "正如第35部分所述。",

    "So who gains when the tick shrinks?":
        "那么跳价缩小时谁得益？<bookmark mark='a'/>一旦它不再约束，竞争决定价差。<bookmark mark='b'/>吃单者每笔交易付得更少。<bookmark mark='c'/>"
        "赢得队列竞赛的做市商失去他们的租金。最优档位显示的深度也会变薄，这可能让大订单更贵，即使小订单变便宜。",

    "Rules in practice.":
        "实践中的规则。<bookmark mark='a'/>2016年至2018年，美国的跳价试点把一组小盘股的跳价扩大到五美分：价差变宽，深度增加，对投资者的结果好坏参半。"
        "<bookmark mark='b'/>2024年的修订对流动性好的股票反其道而行，采用半美分跳价。<bookmark mark='c'/>加密交易所自行设定并更改跳价："
        "每一次更改都在吃单者和做市商之间转移租金。",

    "Pause and predict. An ETF holding corporate bonds":
        "暂停并预测。一只持有公司债的ETF价格为八十美元，而它所持债券的公布价值是八十四美元。谁可能获利，怎么做，又为什么可能做不到？",

    # ------------------------------------------------------------------ ETF
    "Chapter five, and the answer to the pause: an authorised participant":
        "第5章，以及暂停问题的答案：授权参与者可以买入便宜的ETF，赎回换成债券，再卖出债券，前提是债券真的能按公布价值卖出去。"
        "在2020年3月，往往卖不出去。交易所交易基金是有第二个出口的做市。",

    "How an ETF works.":
        "ETF如何运作。<bookmark mark='a'/>授权参与者，通常是大型交易商，把一篮子证券交给基金，换取大批新份额。<bookmark mark='b'/>或者反过来："
        "交回份额，换回证券，以实物形式进行，所以基金永远不必卖出。<bookmark mark='c'/>基金净值每天根据持仓价格计算。<bookmark mark='d'/>"
        "几乎所有交易都在交易所进行，发生在投资者和做市商之间，完全不触及基金本身。",

    "The arbitrage band.":
        "套利区间。<bookmark mark='a'/>如果价格高于净值的幅度超过申购成本，参与者就买入一篮子证券，申购份额并卖出。<bookmark mark='b'/>如果低于净值的幅度"
        "超过赎回成本，它就买入份额，赎回并卖出一篮子证券。<bookmark mark='c'/>所以价格停留在净值周围的一个区间里，区间宽度等于交易底层证券和"
        "使用交易商资产负债表的成本：大盘股很窄，债券很宽。",

    'f"The pause\'s arbitrage, worked through.':
        "把暂停问题里的套利算一遍。<bookmark mark='a'/>以八十美元买入份额。<bookmark mark='b'/>赎回换成债券，再按公布价值减去百分之二的成本卖出债券。"
        "<bookmark mark='c'/>纸面上每份额赚{gain:.2f}美元。<bookmark mark='d'/>但如果公布价值过时，债券实际只能卖七十九美元，这笔交易就会亏损。"
        "折价是市场给这些债券的价格。",

    "Two layers of makers.":
        "两层做市商。<bookmark mark='a'/>交易所做市商全天为份额报价，并用期货、一篮子证券或相关基金对冲；参与者在一天结束时申购和赎回。"
        "<bookmark mark='b'/>他们定价的是一篮子证券的实时公允价值，往往比公布的值新得多。<bookmark mark='c'/>而参与者没有义务行动。Kevin Pan和Yao Zeng"
        "证明，当他们的资产负债表稀缺时，区间会变宽。",

    "Three details that matter.":
        "三个重要的细节。<bookmark mark='a'/>实物赎回让美国基金可以交出成本基础低的证券而不是卖掉它们，所以分配给股东的资本利得更少。"
        "<bookmark mark='b'/>自美国证券交易委员会2019年的ETF规则以来，基金可以接受与其持仓不同的定制篮子，这对债券基金有帮助。<bookmark mark='c'/>"
        "有些基金以现金申购，由基金自己交易证券；2024年1月获批的首批美国现货比特币基金就是这样设立的。",

    "How the price is watched.":
        "价格是如何被盯着的。<bookmark mark='a'/>许多交易所每十五秒公布一次篮子的参考价值，来自持仓的最新价格。<bookmark mark='b'/>溢价是价格除以官方净值"
        "再减一。<bookmark mark='c'/>但做市商并不按公布的值报价。他们用最具流动性的相关价格，期货和其他基金，构建自己的公允价值，"
        "这就是为什么即使债券本身没有交易，他们也能为债券基金报价。",

    'f"March twenty twenty, in the largest high-yield bond fund':
        "2020年3月，最大的高收益债券基金HYG。<bookmark mark='a'/>从1月的高点到3月23日，价格下跌了{100 * abs(h['drawdown']):.0f}%，"
        "<bookmark mark='b'/>日成交量达到2019年中位数的{h['max_vol_x']:.0f}倍。正如国际清算银行的经济学家和其他人所报告的，最大的债券基金相对其"
        "公布价值出现了几个百分点的折价，是它们历史上最大的。",

    "Was the fund wrong, or the value?":
        "错的是基金，还是净值？<bookmark mark='a'/>大多数公司债很少交易，所以公布价值是由滞后于市场的估值价格构建的。<bookmark mark='b'/>"
        "基金份额连续交易，先反映消息。<bookmark mark='c'/>所以折价一部分是基金发现了债券尚未显示的价格，一部分是交易商的资产负债表再也装不下更多债券："
        "让区间闭合的套利，需要有人买下这篮子债券。",

    "The turn. <bookmark mark='a'/> On the twenty-third of March":
        "转折。<bookmark mark='a'/>3月23日，美联储宣布将通过一个新工具购买公司债，包括公司债ETF；那天是该基金的低点。<bookmark mark='b'/>"
        "折价收窄、价格上涨，远在该工具大量购买之前：这个宣布恢复了交易商持有存货的意愿。<bookmark mark='c'/>央行购买ETF，实际上是在私人资产负债表"
        "满了的时候为套利提供资产负债表，第41部分会回到这个主题。",

    "A special case: leveraged and inverse funds.":
        "一个特例：杠杆和反向基金。<bookmark mark='a'/>它们承诺每天收益的某个倍数，所以每天都必须重设敞口。<bookmark mark='b'/>Minder Cheng和"
        "Ananth Madhavan证明，收盘时需要的交易是L乘以L减一、乘以当天收益、乘以资产，方向总是与价格变动相同。<bookmark mark='c'/>三倍杠杆基金"
        "在下跌百分之五之后，必须卖出相当于其资产百分之三十的敞口：可预测的顺周期订单流，做市商看得到它的到来。",

    "Three lessons. <bookmark mark='a'/> The band is a cost, not a law":
        "三条教训。<bookmark mark='a'/>区间是成本，而不是定律：在压力下，资产负债表的成本占主导。<bookmark mark='b'/>对流动性差的持仓，基金的价格可能"
        "是更好的价格，折价可能是信息。<bookmark mark='c'/>ETF在流动性很少的资产之上提供流动性。它之所以有效，是因为做市商为这段差距提供仓储，"
        "而当他们做不到时，它就承受压力。",

    "Pause and predict. Public news moves Bitcoin's value by ten ticks.":
        "暂停并预测。公开消息让比特币的价值移动十跳。做市商过时的报价可以被撤销，也可能被四个与它一样快的对手中的任何一个狙击。"
        "在五家同样快的公司中，它被狙击的频率是多少？",

    # ------------------------------------------------------------------ Speed
    "Chapter six, and the answer to the pause: four times in five.":
        "第6章，以及暂停问题的答案：五次中有四次。当消息公开时，报价的做市商是一个对多个的赛跑者，它赢得撤单比赛的频率，"
        "只和任何其他人赢得成交比赛的频率一样。Eric Budish、Peter Cramton和John Shim把这变成了一个均衡。",

    "The race. <bookmark mark='a'/> News arrives":
        "赛跑。<bookmark mark='a'/>消息到来：期货价格变动，或者相关资产跳动，每家快速公司都在几微秒内看到的公开信息。<bookmark mark='b'/>"
        "做市商发出撤单；它的对手发出订单去打那个过时的报价；交易所按到达顺序逐条处理消息。<bookmark mark='c'/>在N家同样快的公司中，"
        "做市商的撤单先到的概率是N分之一。",

    "The model, simplified to its core.":
        "模型，简化到核心。<bookmark mark='a'/>做市商从投资者那里赚一半价差；每当消息让它的报价过时而它又输掉比赛，它就亏掉跳动减去半价差。"
        "<bookmark mark='b'/>每个狙击者赢N次比赛中的一次。<bookmark mark='c'/>在均衡中，没有公司想换角色，所以两种利润相等，N被消去："
        "半价差等于lambda J乘J除以lambda I加lambda J，无论多少公司竞争。研究者章节会证明。",

    'f"Simulate it: investors at rate one':
        "模拟一下：投资者速率为1，大小为4的跳动速率为十分之一，五家公司，长时间运行。<bookmark mark='a'/>随着半价差加宽，做市商的利润上升，"
        "每个狙击者的利润下降。<bookmark mark='b'/>它们恰好在公式所说的{b['s_star']:.2f}处相交。更窄的价差会让做市商变成狙击者；"
        "更宽的价差会把狙击者吸引来做市。",

    "And the spread does not depend on how many race.":
        "价差不取决于有多少人参赛。<bookmark mark='a'/>在同样的价差下，无论两家还是三十家公司，做市商和每个狙击者的利润都保持相等。"
        "随着公司增加两者都缩小，因为同一份奖金被分成更多份；但由投资者通过价差支付的奖金本身并不缩小。快速公司之间的竞争不会让价差变窄。",

    'f"The same prize on Bitcoin, in dollars.':
        "比特币上的同一份奖金，用美元计。<bookmark mark='a'/>第2章的慢速做市商，每边报一个比特币，在5月17日会亏约{slow_k:.0f}千美元。"
        "<bookmark mark='b'/>理想化的快速做市商约亏{fast_k:.0f}千美元。<bookmark mark='c'/>单靠速度就让亏损减少一半以上，但仍是亏损：其余部分需要预测和"
        "手续费等级。",

    "The arms race. <bookmark mark='a'/> The prize":
        "军备竞赛。<bookmark mark='a'/>奖金是狙击比赛的价值，由投资者通过价差支付。<bookmark mark='b'/>在连续市场里，快任何一点点，都能赢下每一场比赛。"
        "<bookmark mark='c'/>所以每家公司都购买速度；最终它们又一样快，奖金照旧分配，而花掉的钱是纯粹的社会成本。一个囚徒困境，"
        "体现在光纤和微波塔上。",

    "Is it real? <bookmark mark='a'/> On the London Stock Exchange":
        "这是真的吗？<bookmark mark='a'/>在伦敦证券交易所，Matteo Aquilina、Budish和Peter O'Neill测得持续几微秒、只有少数几家公司参与的比赛，"
        "约占成交量的五分之一，对所有交易征收约半个基点的税。<bookmark mark='b'/>在比特币上，第2章慢速与快速做市商之间每笔约十跳的差距，"
        "是从做市商的椅子上看到的同一份奖金。<bookmark mark='c'/>Matthew Baron、Jonathan Brogaard、Björn Hagströmer和Andrei Kirilenko发现，"
        "在高频公司中，最快的赚得最多，利润集中在少数几家。",

    'f"The physics of the race.':
        "比赛的物理学。<bookmark mark='a'/>芝加哥附近的期货交易所和纽约附近的股票交易所相距约一千一百五十公里。<bookmark mark='b'/>光在空气中走完这段"
        "约需{t_air:.1f}毫秒。<bookmark mark='c'/>在被折射率减慢的玻璃光纤中，约需{t_fibre:.1f}毫秒。<bookmark mark='d'/>两者之差不到两毫秒，"
        "正是这一差距支付了两座城市之间的微波塔链：这是根据物理学的计算，而不是任何公司测得的线路。",

    "The remedies proposed.":
        "提出的补救方法。<bookmark mark='a'/>频繁批量拍卖：在几分之一秒内收集订单，然后以一个价格清算，这样微小的速度优势不再能赢，公司在价格上竞争。"
        "<bookmark mark='b'/>减速带：IEX让每笔进来的订单延迟三百五十微秒，并在延迟结束之前更新自己的挂钩订单。<bookmark mark='c'/>以及不对称的延迟或"
        "手续费，在做市商和狙击者之间转移租金。",

    "How a batch auction clears.":
        "批量拍卖如何清算。<bookmark mark='a'/>这个批次中到达的所有买单，按价格排序；它们在批次内何时到达并不重要。<bookmark mark='b'/>卖单同样处理。"
        "<bookmark mark='c'/>在需求与供给相遇的地方确定一个统一价格，这里是100.01美元：成交六个单位，所有人以同一价格成交，该价格上的超额需求按比例分配。"
        "早一微秒什么也买不到。",

    "Why it has not happened.":
        "为什么还没有实现。<bookmark mark='a'/>Budish、Robin Lee和Shim认为，交易所靠出售速度，即托管和数据，赚钱，几乎没有自己切换的动机。"
        "<bookmark mark='b'/>批量拍卖也有成本：如果只有一个场所批量化，流动性会分散；批次间隔必须选择；批次边界上会出现新的博弈。"
        "<bookmark mark='c'/>批量拍卖其实早已存在，就是开盘和收盘集合竞价：每秒做十次才是新东西。",

    "Pause and predict. If a market switched to batch auctions":
        "暂停并预测。如果一个市场改为每十分之一秒进行一次批量拍卖，狙击奖金、价差以及快一微秒的价值会发生什么？",

    # ------------------------------------------------------------------ Industry
    "The answer to the pause. <bookmark mark='a'/> In a batch auction":
        "暂停问题的答案。<bookmark mark='a'/>在批量拍卖中，批次内到达的公开消息会在拍卖清算之前传到每个出价者，所以狙击奖金几乎消失。"
        "<bookmark mark='b'/>价差降到存货风险和真正私人信息的成本。<bookmark mark='c'/>而一微秒几乎一文不值，因为它只在批次边缘才起作用。",

    "Chapter seven. A handful of studies":
        "第7章。少数几项研究通过监管者的数据看到了高频公司的交易内部。它们讲述了一个一致的故事：钱从哪里来，谁留住了它。",

    "Inside one maker.":
        "一家做市商的内部。<bookmark mark='a'/>Albert Menkveld研究了Chi-X和Euronext上的一家大型高频做市商。它赚到了价差和返佣。"
        "<bookmark mark='b'/>它在仓位上亏钱：第1章的逆向选择和存货。<bookmark mark='c'/>净额为正，但每笔很小，靠巨大的成交量积累，存货在几分钟内均值回复，"
        "并在各场所之间对冲。这是我们回放的算术，只是由更快的人来做。",

    "Across firms. <bookmark mark='a'/> High-frequency firms":
        "跨公司来看。<bookmark mark='a'/>高频公司既挂单也吃单，Baron和同事发现，激进的、吃单的那些是最赚钱的之一。<bookmark mark='b'/>利润集中在最快的少数几家；"
        "新进入者赚得更少，退出得更频繁。<bookmark mark='c'/>预测利润的是速度排名，而不是速度本身：资产在于比所有人都快，也就是第6章的军备竞赛。",

    "What speed costs.":
        "速度的代价。<bookmark mark='a'/>放在交易所数据中心里的服务器、每条消息的直连数据，以及两者的费用：一种有利于规模的固定成本。"
        "<bookmark mark='b'/>金融中心之间的微波和激光链路，因为光在空气中比在玻璃光纤中传得快。<bookmark mark='c'/>以及写进可编程芯片的订单逻辑。"
        "所有这些都是第6章的社会成本，一场为瓜分同一份奖金而进行的竞赛。",

    "How inventory is really managed.":
        "存货实际上如何管理。<bookmark mark='a'/>为许多标的做市的公司会在各处积累小仓位。<bookmark mark='b'/>共同因子立即在流动性最好的工具，即股指期货上对冲："
        "实时版的第31部分风险模型。<bookmark mark='c'/>剩下的部分很小，属于各个标的，通过倾斜报价来甩掉，就像Menkveld那家做市商在几分钟内平仓一样。",

    "In stress. <bookmark mark='a'/> In normal times":
        "在压力之下。<bookmark mark='a'/>平常时期，快速做市商之间的竞争让大多数市场的价差变窄。<bookmark mark='b'/>当波动率跳升，逆向选择和存货风险也跳升，"
        "做市商加宽报价或撤离，就像2010年5月6日和2014年10月15日那样。<bookmark mark='c'/>大多数电子做市商没有报价义务。"
        "出于选择提供的流动性，也可以出于选择撤走。",

    "Obligations, where they exist.":
        "存在义务的地方。<bookmark mark='a'/>在欧洲，MiFID II要求运行算法做市策略的公司签订协议，并在规定比例的交易时间内连续报价。"
        "<bookmark mark='b'/>在美国，指定做市商必须把报价保持在规定的价差之内，但大多数电子做市商只有很轻的义务。<bookmark mark='c'/>"
        "义务能在压力下保住流动性，但让这个角色成本更高；返佣和优先权就是报酬。",

    "How large the prize is.":
        "奖金有多大。<bookmark mark='a'/>Aquilina、Budish和O'Neill把他们在伦敦的估计推广到全球股票市场，约为每年五十亿美元。"
        "<bookmark mark='b'/>少数最快的公司赢得大部分比赛；输家是较慢的做市商，最终是投资者。<bookmark mark='c'/>而它没给投资者带来任何东西："
        "比赛只是重新分配了批量设计本会留给他们的钱。",

    "Options at scale.":
        "大规模的期权做市。<bookmark mark='a'/>期权做市商用一个波动率曲面为每个行权价和到期日报价，所以曲面一动，所有报价同时重新定价。"
        "<bookmark mark='b'/>它的存货就是它的希腊字母：持续对冲delta，通过倾斜报价管理vega和gamma。<bookmark mark='c'/>它也参加同样的比赛："
        "过时的曲面像过时的报价一样被狙击，一次成千上万个价格。",

    "And in crypto. <bookmark mark='a'/> Exchanges charge by volume tier":
        "再看加密市场。<bookmark mark='a'/>交易所按成交量等级收费，最大的做市商付得很少或者拿到返佣：正如第2章所示，这就是亏损和生意之间的区别。"
        "<bookmark mark='b'/>做市商在许多场所报价，在最深的地方对冲，永续合约的资金费率是存货成本的一部分。<bookmark mark='c'/>新代币常常以合同雇用"
        "做市商；据报道，一些执法案件显示了这类条款如何造成公众看不到的利益冲突。",

    "Pause and predict. The House wants to make markets":
        "暂停并预测。本系列公司想为比特币永续合约做市。根据第2章到第6章，它的交易台在挂出第一笔订单之前必须具备哪三样东西？",

    # ------------------------------------------------------------------ House
    "The answer to the pause. <bookmark mark='a'/> First, a measured edge":
        "暂停问题的答案。<bookmark mark='a'/>第一，测量过的优势：在本系列公司自己的速度和队列位置下，预期的事后损失必须小于半价差加返佣。"
        "第2章那种朴素报价差了十跳。<bookmark mark='b'/>第二，对照对手测量过的速度，因为奖金归最快的人。<bookmark mark='c'/>第三，"
        "对存货和亏损的硬性上限，以及一个能一次停止所有报价的开关。",

    "Chapter eight. The House's thirty-eighth rule":
        "第8章。本系列公司的第38条规则属于它新开的做市台。报价是本系列公司里唯一能在一小时内亏掉一年利润的业务，所以规则很严格。",

    "The first sheet. <bookmark mark='a'/> A quote at the touch":
        "第一张汇总表。<bookmark mark='a'/>在最优价位亏钱的报价，无论慢还是快，听从队列时亏得少一些。随距离缓慢衰减的成交率，以及离中间价很远、"
        "在不计排队和手续费时赚钱的最优报价。不到一跳的狙击价差。还有一只两个月内下跌超过五分之一的债券基金。",

    "Controls, before any edge.":
        "先有控制，再谈优势。<bookmark mark='a'/>每个工具和总体的仓位上限，各自配有对冲。<bookmark mark='b'/>亏损上限，以及在亏损、消息或成交比预期更快时"
        "自动停止报价的开关。<bookmark mark='c'/>还有对每笔订单的交易前检查，价格区间和数量上限，在美国，市场准入规则要求经纪自营商这样做。",

    "How the desk would go live.":
        "交易台会怎样上线。<bookmark mark='a'/>先回放，在真实的成交记录上，以本系列公司自己测得的延迟和队列位置计算成交。<bookmark mark='b'/>然后小规模实盘，"
        "严格限额，把实盘的事后损益与回放的比较：差距就是回放的误差。<bookmark mark='c'/>然后慢慢扩大规模，而且只在实盘的事后损益停留在回放的"
        "置信区间之内时才扩大。",

    "And capital.":
        "还有资本。<bookmark mark='a'/>每个仓位都需要在交易场所或清算所缴纳保证金，在许多场所做市的公司要在每个场所都存放抵押品。<bookmark mark='b'/>"
        "资本由最坏的一分钟而不是平均的一天决定：一侧成串的成交，以及打滑的对冲。<bookmark mark='c'/>所以交易台的规模受到它的事后损益、限额和资本的限制。",

    "Chapter three's measurement.":
        "第3章的测量。对每一秒，记录任何买单超过起始中间价的最远距离，以及任何卖单低于它的最远距离，以跳为单位；然后对每个距离，计算达到它的秒的比例。",

    "Chapter one's closed form, in four lines:":
        "第1章的闭式解，四行：由波动率、风险厌恶和成交参数算出的倾斜常数，以及等于基础项加半个倾斜的半价差。",

    "Chapter two's replay at its core.":
        "第2章回放的核心。快速做市商躲开任何穿过其价格的扫单；否则，穿过价格的成交，或在该价格上超过前方队列的成交，会让它成交，存货随之变化。",

    "And Chapter six. The equilibrium half-spread in one line":
        "还有第6章。一行的均衡半价差；以及模拟中的比赛：除非提供者的撤单先到，否则它会被狙击，概率是N分之一的反面，而在批量拍卖中永远不会。",

    "Two desks under one roof.":
        "同一屋檐下的两个交易台。<bookmark mark='a'/>当组合台的订单可以与做市台的存货成交时，在本系列公司内部撮合能为双方省下价差。"
        "<bookmark mark='b'/>但做市商会看到执行者的订单流，抢在它之前交易就是抢跑自己的客户。<bookmark mark='c'/>所以两个台是分开的，"
        "内部撮合只能以公开市场确定的价格进行，合规部门审查每一个案例。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>成交率与报价；在成交记录上的做市商；以及速度竞赛。<bookmark mark='b'/>还有第38条规则。"
        "本系列公司只在这样的地方报价：在自己的速度和队列位置下测得的事后损失，低于它赚到的价差加返佣。每个报价引擎都在仓位和亏损上限下运行，"
        "并配有一键停止开关。任何基金套利的规模，都要按它在2020年3月那样的压力下所需的资产负债表来确定。",

    "The rule against three cases.":
        "用三个案例检验这条规则。<bookmark mark='a'/>一份报价策略的回测：问成交是怎样模拟的，排在队列末尾还是前面，扫单有没有计入。"
        "<bookmark mark='b'/>供应商的最优报价模型：要它的事后损益，而不是成交率。<bookmark mark='c'/>一个总能成功的ETF套利：问当债券无法按公布价值卖出时"
        "会发生什么，以及由谁的资产负债表来持有它们。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter six stated":
        "写给研究者。第6章陈述了Budish、Cramton和Shim的结果：狙击价差不取决于有多少公司参赛。本章把它作为均衡来证明，推广到任意跳动分布，"
        "证明批量拍卖会消除奖金，并用模拟和比特币数据检验两者。",

    "The model. <bookmark mark='a'/> A public value":
        "模型。<bookmark mark='a'/>一个公开的价值，以速率lambda J向上或向下跳动J。<bookmark mark='b'/>以速率lambda I到达、支付半价差的无信息投资者。"
        "<bookmark mark='c'/>N家同样快的公司，它们同时发出的消息被交易所按随机顺序逐条处理。<bookmark mark='d'/>一家公司在价值附近提供流动性；"
        "当跳动让它的报价过时，它试图撤单，其他公司试图与之成交。",

    "Lemma one, the payoffs.":
        "引理一，收益。<bookmark mark='a'/>提供者从每个投资者那里赚钱，每当其他N减一条消息中有一条先于它的撤单，它就亏钱。<bookmark mark='b'/>"
        "其他每家公司赢得某场比赛的概率是N分之一。<bookmark mark='c'/>两种角色之间的差完全不含N：提供者的损失和一个狙击者的收益加起来，"
        "正好是每次跳动一整场比赛。",

    "Lemma two, indifference.":
        "引理二，无差异。<bookmark mark='a'/>如果提供流动性比狙击赚得多，对手就会挂出稍窄一点的价差，拿走投资者，赚得更多：价格竞争。"
        "<bookmark mark='b'/>如果赚得少，提供者宁愿去狙击，在那个价差上就没有人提供流动性。<bookmark mark='c'/>所以在任何均衡中，两种角色同样有吸引力。",

    "Lemma three, existence and uniqueness.":
        "引理三，存在性与唯一性。<bookmark mark='a'/>把这个差写成半价差h的函数。<bookmark mark='b'/>它在零处为负，在跳动大小处为正，并且严格递增。"
        "<bookmark mark='c'/>所以它恰有一个根，而在零到J之间它是线性的：半价差等于lambda J乘J除以lambda I加lambda J。",

    "The theorem. <bookmark mark='a'/> The equilibrium half-spread":
        "定理。<bookmark mark='a'/>均衡半价差等于lambda J乘J除以lambda I加lambda J，与公司数量无关。<bookmark mark='b'/>单位时间的狙击租金等于"
        "投资者在价差中付出的：投资者承担了比赛的全部成本。更多的公司把奖金分成更多份，但不改变奖金本身；而由于稍快一点的公司就能赢下每一场比赛，"
        "所有公司都投资于速度，这笔投资被浪费了。",

    "What moves the spread.":
        "什么在推动价差。<bookmark mark='a'/>公开消息越频繁，比赛越多，价差越宽：与许多相关工具挂钩的市场被狙击得最多。<bookmark mark='b'/>"
        "无信息投资者越多，成本就分摊到越多的交易上，所以越繁忙的市场越便宜。<bookmark mark='c'/>以及最惊人的一条：增加快速公司对投资者毫无改变。",

    "The general case.":
        "一般情形。<bookmark mark='a'/>当跳动大小随机时，提供者只在大于其半价差的跳动上亏钱，而且只亏超出的部分。<bookmark mark='b'/>左边随h上升，"
        "右边随h下降，所以同样恰有一个均衡。<bookmark mark='c'/>由于超出部分是跳动的凸函数，均值相同但更分散的跳动会让价差变宽或保持不变："
        "决定被狙击成本的是尾部，而不是平均值。",

    'f"Check one: simulation.':
        "检验一：模拟。<bookmark mark='a'/>公式给出{b['s_star']:.3f}。<bookmark mark='b'/>模拟的利润曲线在{cross:.3f}处相交。<bookmark mark='c'/>"
        "在那个价差上，无论两家还是三十家公司，两种角色赚得一样，正如定理所说。",

    'f"Check two: batch auctions, in the simulation.':
        "检验二：模拟中的批量拍卖。<bookmark mark='a'/>在连续交易中，五家公司中的每一家通过狙击每单位时间赚{b['byN'][2]['sniper']:.3f}。"
        "<bookmark mark='b'/>在批量拍卖中，什么也赚不到：报价在每次清算前都按当前价值重设，所以过时的报价从不被成交。<bookmark mark='c'/>"
        "在同样的价差下，提供者保留了全部，而提供者之间的竞争会把价差推向零。",

    "The logic of the batch result.":
        "批量结果的逻辑。<bookmark mark='a'/>在一个批次之内，消息的顺序不重要：看到消息的提供者会在拍卖使用其报价之前更新报价。<bookmark mark='b'/>"
        "所以提供者通过互相压价来竞争，而不是赛跑。<bookmark mark='c'/>狙击项消失了，只剩下在批次最后一瞬间到来的消息，剩下的是一个没有比赛的世界会有的价差。",

    "Why, in a formula.":
        "用公式说明原因。<bookmark mark='a'/>在延迟为delta、批次间隔为tau时，只有落在批次最后delta时间内的跳动才会抓住过时的报价。<bookmark mark='b'/>"
        "同样的无差异论证于是给出一个与delta除以tau成正比的价差。<bookmark mark='c'/>一微秒对十分之一秒是十的负五次方：狙击部分缩小五个数量级，"
        "比批次间隔更短的速度几乎一文不值。",

    'f"The welfare arithmetic.':
        "福利的算术。<bookmark mark='a'/>投资者付出lambda I乘以半价差，恰好等于狙击租金。<bookmark mark='b'/>在模拟的参数下，每单位时间"
        "{b['lam_i'] * h:.3f}。<bookmark mark='c'/>批量市场通过更窄的价差把它还给投资者，同时消除了在速度上花钱的理由。收益是两者之和。",

    "The arms race, formally.":
        "正式地看军备竞赛。<bookmark mark='a'/>一家公司单独每单位时间付出c，换取微小的速度优势，就能赢下每一场比赛。<bookmark mark='b'/>如果每家公司都付钱，"
        "比赛又变得均等，每家赢N分之一，而所有人都付出了c。<bookmark mark='c'/>只要投资成本低于它本会输掉的那些比赛，投资就是占优选择："
        "一个囚徒困境，总成本N乘c由市场承担。",

    'f"Check three: the general condition':
        "检验三：一般条件，使用比特币自己的跳动大小。用从每一次真实中间价变化中抽取的跳动和吃单者的真实速率来模拟市场。<bookmark mark='a'/>"
        "两种角色之差在{cross:.2f}跳处穿过零，<bookmark mark='b'/>恰是直接求解该条件所得的位置：{b['btc']['general_half']:.2f}。",

    'f"Check four: Bitcoin.':
        "检验四：比特币。<bookmark mark='a'/>把快照之间中间价的每一次变化当作一次公开跳动，用它的真实大小：每秒{bt['lam_all']:.2f}次，"
        "平均{bt['mean_move']:.0f}跳。<bookmark mark='b'/>对照吃单者的速率求解，一般条件给出约{bt['general_half']:.2f}跳的半价差。"
        "<bookmark mark='c'/>低于跳价强制的半跳。这是一个粗略的校准，因为吃单者并非都没有信息，也不是每次变动都是公开消息，但它说明在这个市场上"
        "约束价差的是跳价而不是狙击，第2章的亏损来自别处：来自订单流中的信息。",

    "Where this sits. <bookmark mark='a'/> Budish, Cramton and Shim's paper":
        "这项工作的位置。<bookmark mark='a'/>Budish、Cramton和Shim的论文包含一般跳动、军备竞赛和批量拍卖，并以相关期货和基金为证据。"
        "<bookmark mark='b'/>Aquilina、Budish和O'Neill在伦敦证券交易所测量了比赛。<bookmark mark='c'/>Markus Baldauf和Joshua Mollner，以及Menkveld"
        "和Marius Zoican证明，一旦获取信息成为一种选择，更快的市场可能让价差变宽，也可能让它变窄。",

    "Three open questions. <bookmark mark='a'/> An equilibrium spread":
        "三个开放问题。<bookmark mark='a'/>同时包含私人信息、公开跳动和存货的均衡价差，并用消息数据估计。<bookmark mark='b'/>当连续市场和批量市场并存时，"
        "流动性去哪里，结果是否有效率？<bookmark mark='c'/>以及在加密市场的众多场所之间，延迟各不相同、没有合并报价时的狙击：谁赢，吃单者付出什么？",

    "Pause and predict. Investors arrive at rate ten":
        "暂停并预测。投资者以速率10到达，三跳的跳动以速率2到达。狙击半价差是多少？如果跳动以相同概率是一跳或五跳，均值相同呢？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-eight in thirteen lines.":
        "用十三行回顾第38部分。做市商的利润是半价差和返佣，减去事后损失，再加减存货。在比特币上，在最优价位报价会亏钱，无论慢还是快，"
        "大部分亏损在成交自己的十分之一秒内到来。成交率随距离缓慢衰减，所以最优报价远在外面，在那里扫单的超调会付钱。"
        "而被钉在一跳的价差把价格竞争变成了队列竞赛。",

    "ETF arbitrage keeps a fund's price within a cost band":
        "ETF套利把基金价格保持在一个成本区间内，直到像2020年3月那样，区间变成了一张没人拥有的资产负债表的成本。狙击价差不取决于有多少公司参赛，"
        "所以速度是一个囚徒困境，而批量拍卖会消除它的奖金。高频利润是价差和返佣减去仓位损失，集中在最快的公司。研究者章节证明了狙击均衡。",

    "Three lessons. <bookmark mark='a'/> The spread pays for almost nothing":
        "三条教训。<bookmark mark='a'/>价差几乎什么都付不起：做市商的命运取决于成交之后的事后损益，而它取决于速度、队列位置和预测。<bookmark mark='b'/>"
        "模型必须在正确的东西上检验：事后损益，而不是成交率。<bookmark mark='c'/>市场设计决定奖金：跳价大小、撮合规则和批次间隔，决定公司是在价格上"
        "还是在速度上竞争，以及由谁付钱。",

    "The part on one card.":
        "一张卡片上的这一部分。做市商的优势。成交率与基础距离k分之一。GLFT的报价及其存货倾斜。ETF的套利区间。与公司数量无关的狙击价差。"
        "以及它的批量拍卖版本，按延迟除以批次间隔缩小。",

    "How this part connects.":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>往回看：第35部分的交易商模型变成了有成本的生意；第36部分的事后损益变成了它的损益；"
        "第37部分的执行者是它的客户。<bookmark mark='b'/>横向看：第11部分的期权做市商是另一种产品中的同一门生意。<bookmark mark='c'/>往前看："
        "第39部分的自动做市商按公式报价，第41部分的危机是做市商退出的时候，第42部分的学习型主体坐上做市商的椅子。",

    "Six desk questions. Where does a market maker's profit come from?":
        "六个交易台问题。做市商的利润从哪里来？价差和返佣，减去事后损失。<bookmark mark='a'/>为什么按存货倾斜报价？让接下来的成交减少它。"
        "<bookmark mark='b'/>比特币的报价应该放在哪里？约三十跳之外。",

    "Why does a pinned spread create a speed race?":
        "为什么被钉住的价差会造成速度竞赛？做市商只能争夺位置。<bookmark mark='a'/>是什么让ETF贴近其价值，它何时失效？套利，直到资产负债表装满。"
        "<bookmark mark='b'/>为什么速度竞争不能让价差变窄？因为狙击价差不取决于公司数量。完整解答见讲义。",

    "The research chapter's pause, answered.":
        "研究者章节暂停问题的答案。<bookmark mark='a'/>二乘三除以十二：半跳。<bookmark mark='b'/>跳动为一跳或五跳时答案相同，都是半跳，因为两种大小都超过"
        "半价差，所以超出部分是线性的。只有当某些跳动小于半价差时，分散度才起作用，那正是尾部登场的地方。",

    "And twelve problems: a maker's edge":
        "还有十二道习题：做市商的优势；Avellaneda和Stoikov的价差；由成交概率求k；速度的价值；被钉住的价差中的租金；ETF套利；狙击概率；狙击价差；"
        "批量拍卖；以及速度投资。然后是两道资格考试题：完整的狙击均衡，以及由HJB方程推导GLFT报价。中英文解答见讲义。",

    "Where this comes back. Part thirty-nine replaces quotes":
        "这些内容会在哪里再出现。第39部分用一条定价曲线取代报价：自动做市商。第41部分问流动性消失时由谁提供。第42部分让学习型主体坐上做市商的椅子。"
        "第43部分问，在付钱给做市商之后，是否有人能战胜市场。",

    "The textbooks this part follows, and the papers it draws on, from Garman":
        "这一部分所依据的教科书和论文，从Garman的存货模型到在伦敦测得的比赛。屏幕上的每个数字，都是本系列公司的代码根据币安公开的最优报价和成交记录、"
        "雅虎财经的K线或模拟算出来的。",

    "The House now knows what market making costs":
        "本系列公司现在知道做市的成本、需要的速度，以及它的规则必须在哪里叫停。<bookmark mark='a'/>下一部分，第39部分：加密货币与去中心化金融。"
        "永续合约及其资金费率、没有订单簿的交易所，以及一个交易场所倒闭时会发生什么。",

    # ------------------------------------------------------------------ added sections
    "Where adverse selection comes from, recalled from Part thirty-five.":
        "逆向选择从何而来，回顾第35部分。<bookmark mark='a'/>在Glosten和Milgrom的模型中，价值以相同概率为高或低，比例为mu的吃单者知道是哪一个。"
        "<bookmark mark='b'/>于是一笔买单是价值为高的证据，竞争性的做市商把卖价定在给定买单时的期望价值：平均值加上mu乘以半个区间。"
        "<bookmark mark='c'/>价差等于mu乘以区间，全部是逆向选择。<bookmark mark='d'/>五分之一的吃单者有信息、区间为十时，价差为二。"
        "<bookmark mark='e'/>做市商平均什么也赚不到：每笔成交的半价差恰好支付随后的事后损失。在比特币永续合约上，这个平衡是为队列前端最快的做市商"
        "而达成的，而不是为排在末尾的慢速做市商，这就是下一章的回放会亏钱的原因。",

    'f"How good is the exponential?':
        "指数形式有多好？<bookmark mark='a'/>在每个距离上比较测得的强度和拟合曲线。在半跳处，也就是最优价位，测得的速率比拟合高{touch:.0f}%。"
        "<bookmark mark='b'/>从一跳到三十跳，拟合平均偏差约{mid_err:.0f}%：对数刻度上的一条直线，正如模型假设的那样。<bookmark mark='c'/>"
        "在四十五跳处又高出{tail:.0f}%：最大的扫单比指数形式允许的走得更远。<bookmark mark='d'/>所以存在两种状态。该侧的任何成交都能到达"
        "最优价位上的报价；一跳之外的报价需要一次扫单。最优距离k分之一来自第二种状态，指数形式在那里拟合得很好；第一种状态，即最优价位，"
        "是大部分成交发生的地方。",
}
