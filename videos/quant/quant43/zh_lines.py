"""Chinese narration for quant43."""

TITLE = '量化金融，从零搭建 · 第43部分：你能战胜市场吗？'

CHAPTERS = {
    'Hook': '技能还是运气？',
    'Arithmetic': '1. 夏普的算术',
    'Luck': '2. 运气还是技能？',
    'Scale': '3. 技能、规模与资金',
    'Adaptive': '4. 适应性市场',
    'Record': '5. 完整打开的业绩记录',
    'Surface': '6. 曲面的记分板',
    'Open': '7. 我们仍然不知道的',
    'Bachelier': '8. 回到巴舍利耶',
    'Journey': '9. 本系列公司的历程',
    'House': '10. 第43条规则：市场是默认选项',
    'Research': '写给研究者：有多少没有技能，技能流向何处？',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part forty-three, the last. Can you beat the market?":
        "第43部分，最后一部分。你能战胜市场吗？这是本系列每一部分都在绕着走的问题，这次直接提出：用算术，用统计，用技能的经济学，并用完全打开的本系列公司"
        "自己的记录。",

    'f"What this part finds. <bookmark mark=\'a\'/> Luck is generous:':
        "这一部分的发现。<bookmark mark='a'/>运气很慷慨：一个毫无技能、成本百分之一的基金经理，十五年后仍有{100 * p15:.0f}%的概率跑赢指数。"
        "<bookmark mark='b'/>研究会缩水：在本系列公司登记的二十五个策略中，研究期夏普比率每高出一点，在封存的样本外只多换来{sl:.2f}。<bookmark mark='c'/>"
        "平淡者胜：本系列公司自己的已发表溢价组合，在样本外赚得{hs:.2f}，扣除成本后{hn:.2f}。<bookmark mark='d'/>市场会学习：一九七〇年代的规律已经消失。",

    "The desk question, answered in Chapter two.":
        "交易台问题，在第2章回答。<bookmark mark='a'/>你的基金连续五年跑赢市场。<bookmark mark='b'/>另有两千只基金也在尝试。<bookmark mark='c'/>是技能，还是"
        "运气？你又怎么才能分辨？",

    "Why it matters. <bookmark mark='a'/> Most savings are managed by someone paid to beat the market,":
        "为什么重要。<bookmark mark='a'/>大部分储蓄由被付钱去战胜市场的人管理，他们能否做到关系到巨额费用。<bookmark mark='b'/>本系列中的每个策略都是一次"
        "尝试；这一部分追问这些尝试合起来带来了什么。<bookmark mark='c'/>本系列公司从第一部分起就保存记录，正是为了在最后能诚实地回答这个问题。",

    "The question is older than the field.":
        "这个问题比这个领域还古老。<bookmark mark='a'/>一九三三年，阿尔弗雷德·考尔斯对四十五家预测机构四年的预测打分，没有发现它们能预测的证据。"
        "<bookmark mark='b'/>一九六八年，迈克尔·詹森用市场的风险调整收益衡量共同基金，发现它们落后的幅度大约等于成本：这是第一个阿尔法。"
        "<bookmark mark='c'/>一九七六年，约翰·博格的第一只零售指数基金，在夏普写下算术之前，就把它变成了一种产品。",

    "And what this part is not. <bookmark mark='a'/> It is not advice.":
        "以及这一部分不是什么。<bookmark mark='a'/>它不是投资建议。<bookmark mark='b'/>它不使用真实基金的数据，那些数据需要授权；基金群体是模拟的，并按已发表的"
        "估计校准。<bookmark mark='c'/>它也不是最终结论：五年的样本外只是第一次诚实的测量，而不是永久的判决。",

    "Where this sits: the last part of Act seven, and of the series.":
        "这一部分的位置：第七幕的最后一部分，也是整个系列的最后一部分。度量了风险，追踪了危机，放出了机器；现在是此前四十二部分都在为之准备的问题。",

    "The plan: Sharpe's arithmetic; luck against skill;":
        "计划：夏普的算术；运气对技能；技能的回报去了哪里；会适应的市场；完全打开的业绩记录；定价记分板；开放问题；回到本系列的起点；以及计数技能背后的"
        "定理。",

    "In the House, every desk is built.":
        "在本系列公司里，每个部门都已建成。它们最后一次一起汇报，问题不再是每个部门能做什么，而是它们合在一起赚到了什么。",

    "Pause and predict. Before costs, what is the average return of all actively managed money,":
        "暂停并预测。扣除成本之前，所有主动管理资金的平均收益相对于市场是多少？",

    # ------------------------------------------------------------------ Arithmetic
    "Chapter one, and the answer to the pause: exactly the market's return, before costs.":
        "第1章，以及暂停问题的答案：扣除成本前恰好等于市场收益。不是大约，而是恰好。威廉·夏普称之为主动管理的算术，它不需要价格模型，不需要有效性理论，"
        "也不需要数据。它是会计。",

    "The argument. <bookmark mark='a'/> Every dollar invested in a market is held by someone,":
        "论证。<bookmark mark='a'/>投入市场的每一美元都由某人持有，要么被动，要么主动。<bookmark mark='b'/>被动投资者按市场权重持有每一只证券。"
        "<bookmark mark='c'/>所以被动资金恰好赚取市场收益。<bookmark mark='d'/>又因为市场是两者的平均，主动资金合在一起，扣除成本前也恰好赚取市场收益。每一个"
        "主动的赢家，都按美元对美元地对应着一个主动的输家。",

    "In three lines. <bookmark mark='a'/> The market's return is the weighted average":
        "三行。<bookmark mark='a'/>市场收益是被动收益与主动收益的加权平均。<bookmark mark='b'/>代入被动收益，它就是市场收益。<bookmark mark='c'/>所以主动"
        "收益等于市场收益，扣除成本后，平均的主动美元落后平均的被动美元，差额恰好是两者支付成本之差。",

    "So what does a manager with no skill look like?":
        "那么，一个毫无技能的基金经理是什么样子？<bookmark mark='a'/>它每年平均落后指数一个成本的幅度，并围绕这个值按跟踪误差波动。<bookmark mark='b'/>"
        "T年后它领先的概率就是这个。<bookmark mark='c'/>成本随时间线性累加，而运气只按平方根增长：期限越长，算术越占上风。",

    'f"With a one percent cost and five percent tracking error.':
        "成本百分之一、跟踪误差百分之五。<bookmark mark='a'/>一年后，{100 * p1:.0f}%的零技能基金经理领先指数：几乎是抛硬币。<bookmark mark='b'/>十五年后，"
        "{100 * p15:.0f}%；三十年后，{100 * p30:.0f}%。<bookmark mark='c'/>两万个模拟的基金经理落在公式曲线上。所以少数人在十五年里跑赢指数，正是单凭运气"
        "就会出现的情况：它本身并不是技能的证据。",

    "How long would it take to tell?":
        "要多久才能分辨？<bookmark mark='a'/>基金经理主动收益的t统计量，随信息比率乘以年数的平方根而增长。<bookmark mark='b'/>要达到两个标准误，需要二除以"
        "信息比率，再平方。<bookmark mark='c'/>出色的信息比率一半需要十六年；不错的零点二需要一百年。大多数职业生涯在证明完成之前就结束了。",

    'f"And by cost.':
        "再按成本来看。<bookmark mark='a'/>每年四分之一个百分点的成本下，{100 * g[0]['p15']:.0f}%的零技能基金经理十五年后仍然领先。<bookmark mark='b'/>"
        "百分之二时，只有{100 * g[-1]['p15']:.0f}%。费用是基金经理收益中唯一确定的部分。",

    'f"And costs compound.':
        "而且成本会复利。<bookmark mark='a'/>一单位资金以百分之七的毛收益增长三十年，按指数基金的成本，变成{e0:.1f}。<bookmark mark='b'/>每年百分之一的"
        "成本，{e1:.1f}；百分之二，{e2:.1f}：同样的市场，财富少了{lost:.0f}%。基金经理收益中确定的那部分，正是会复利增长的那部分。",

    "What the arithmetic makes of the game.":
        "算术对这场游戏意味着什么。<bookmark mark='a'/>扣除成本前，相对于市场，主动管理是零和的：每一份收益都是另一个主动管理者的损失。<bookmark mark='b'/>"
        "扣除成本后，它是负和的。<bookmark mark='c'/>所以赢家是那些比平均主动美元更有信息的人，而这个平均是由其他专业人士决定的，他们还在不断进步。查尔斯·"
        "埃利斯称之为输家的游戏。",

    "What the data on real funds show.":
        "真实基金的数据显示了什么。<bookmark mark='a'/>二十年来，标普的记分卡一直报告，大多数主动管理的美国股票基金在长期内扣除费用后落后于基准，正如算术所"
        "预言的。<bookmark mark='b'/>它们无法说明领先的少数是否有技能。<bookmark mark='c'/>而关闭的基金，大多是表现差的，除非数据保留它们，否则会从平均值中"
        "消失：这就是第26部分的幸存者偏差，在基金业中。",

    "Lasse Pedersen found the crack in the arithmetic.":
        "拉瑟·佩德森找到了算术中的裂缝。<bookmark mark='a'/>它假设被动投资者从不交易。但市场在变化：新股发行，公司进出指数。<bookmark mark='b'/>为了保持"
        "市场权重，被动投资者必须买入新纳入的、卖出被剔除的，而价格可以由主动交易者设定。<bookmark mark='c'/>所以主动管理在总体上可以创造价值：提供这种流动性，"
        "并让价格包含信息。算术约束的是平均，而不是每一个基金经理。",

    "And the oldest answer to why anyone tries, from Part one.":
        "以及为什么还有人尝试的最古老答案，来自第1部分。<bookmark mark='a'/>桑福德·格罗斯曼和约瑟夫·斯蒂格利茨：如果价格反映了所有信息，就没有人会花钱"
        "收集信息，那价格也就无法反映信息。<bookmark mark='b'/>均衡时，知情交易者赚得刚好够支付获取信息的成本：用佩德森的话说，有效地无效。<bookmark mark='c'/>"
        "所以技能应该存在，赚得大约等于它的成本，并且在最容易被复制的地方最难找到。",

    "Pause and predict. Two thousand funds, none with any skill at all,":
        "暂停并预测。两千只基金，没有一只有任何技能，每只都观察二十年。它们中最高的阿尔法t统计量会有多大？",

    # ------------------------------------------------------------------ Luck
    'f"Chapter two, and the answer to the pause: about {bn:.1f}.':
        "第2章，以及暂停问题的答案：大约{bn:.1f}。在本系列公司的模拟中，两千只无技能基金里最幸运的一只，t统计量为{bn:.2f}，其中有{ns}只通过了通常的两个"
        "标准误检验。基金足够多时，总有人看起来很出色。问题从来不是最好的基金是否显著，而是好基金是否比运气所能产生的更多。",

    "Back to the desk question.":
        "回到交易台问题。<bookmark mark='a'/>不考虑成本，一只无技能的基金在任意一年跑赢市场的概率约为一半，所以连续五年的概率是三十二分之一。"
        "<bookmark mark='b'/>两千只基金中，大约六十只会凭运气做到。<bookmark mark='c'/>至少有一只做到的概率基本上是一。所以五年连胜只有在拥有它的基金远多于六十只"
        "时才算证据：这正是巴拉斯、斯卡耶和沃默斯的计数方法。",

    "A world where the truth is known.":
        "一个真相已知的世界。<bookmark mark='a'/>大多数基金完全没有阿尔法。<bookmark mark='b'/>大约四分之一的阿尔法为负：它们覆盖不了成本。"
        "<bookmark mark='c'/>大约百分之一有真正的技能。这些比例依照洛朗·巴拉斯、奥利维耶·斯卡耶和拉斯·沃默斯对美国股票基金的估计。<bookmark mark='d'/>"
        "每只基金观察二十年，跟踪误差百分之五。",

    "The t-statistics of all two thousand.":
        "全部两千只基金的t统计量。<bookmark mark='a'/>轮廓线显示如果没有基金有技能会是什么样：一个以零为中心的钟形。<bookmark mark='b'/>真实群体向左移动，"
        "这是不擅长的那四分之一造成的，右侧还有一条细细的额外尾巴。<bookmark mark='c'/>超过通常的临界值二，右尾里混着少数有技能的基金和许多幸运的基金。逐只"
        "区分是不可能的；数出它们却可以。",

    'f"Fama and French\'s comparison, done the same way:':
        "法玛和弗伦奇的比较，用同样的方法：把基金的t统计量逐个百分位，与一个所有阿尔法都设为零的群体比较。<bookmark mark='a'/>在左尾，基金远比运气差："
        "第一个百分位上是{a1:.2f}对{n1:.2f}。<bookmark mark='b'/>在右尾，它们只好一点点：第九十九个百分位上是{a99:.2f}对{n99:.2f}。<bookmark mark='c'/>"
        "单凭运气，就有大约{t2:.0f}只基金超过通常的临界值，{t3:.1f}只超过三。",

    "How the literature does it on real funds.":
        "文献如何在真实基金上做到这一点。<bookmark mark='a'/>尤金·法玛和肯尼斯·弗伦奇把每只基金的收益去掉阿尔法后自助重抽样，看单凭运气会产生什么。"
        "<bookmark mark='b'/>据他们报告，扣除成本后，真实分布位于运气分布的左边：很少有基金赚回自己的费用。<bookmark mark='c'/>罗伯特·科索夫斯基和合作者用类似"
        "的自助法发现，最好的那些基金扣除成本前的阿尔法比运气所能给出的更大。",

    "Barras, Scaillet and Wermers count, rather than pick.":
        "巴拉斯、斯卡耶和沃默斯是计数，而不是挑选。<bookmark mark='a'/>首先是约翰·斯托里对没有阿尔法的基金数量的估计：大的p值主要来自它们，并且均匀分布，"
        "所以把它们的数量放大，就估计出了这个比例。<bookmark mark='b'/>其中有已知的一部分会凭运气落入每一个显著的尾部。<bookmark mark='c'/>所以右尾中显著的比例"
        "减去幸运的部分，估计出有技能的比例；左尾则是不擅长的比例。研究者章节会证明第一步为什么有效。",

    'f"And it works. <bookmark mark=\'a\'/> The share with no alpha:':
        "而且它有效。<bookmark mark='a'/>没有阿尔法的比例：真实为{pi0t:.1f}%，估计为{pi0e:.1f}%。<bookmark mark='b'/>不擅长的：{mt:.1f}%对{me:.1f}%。"
        "<bookmark mark='c'/>有技能的：{pt:.1f}%对{pe:.1f}%。没有识别出任何一只基金；识别出的是比例。",

    'f"So what does a significant fund mean?':
        "那么，一只显著的基金意味着什么？<bookmark mark='a'/>两千只中有{ns}只越过了通常的门槛。<bookmark mark='b'/>其中只有{sh:.0f}%真正有技能。"
        "<bookmark mark='c'/>其余是幸运的零阿尔法基金。这就是错误发现率，也是为什么明星基金经理的业绩本身说明的比看起来要少。",

    'f"Persistence, in the simulated population.':
        "模拟群体中的持续性。按前十年给基金排名，然后观察后十年。<bookmark mark='a'/>最差的十分位继续亏损：每年{bn:+.1f}%，因为其中主要是不擅长的基金，它们的"
        "成本是永久的。<bookmark mark='b'/>最好的十分位几乎不持续：{tn:+.1f}%。其中只有{ts:.0f}%真正有技能；其余是幸运的，而运气不会重复。卡哈特的发现，在真相"
        "已知的情况下得到复现。",

    "And over time. <bookmark mark='a'/> Mark Carhart found":
        "以及随时间的变化。<bookmark mark='a'/>马克·卡哈特发现，赢家的持续性主要来自其持仓的动量和成本差异；只有最差的基金会可靠地一直差下去。"
        "<bookmark mark='b'/>高成本是永久的；幸运的连胜不是。<bookmark mark='c'/>这留下一个谜题：如果确实存在一点技能，为什么它没有表现为持久的超额收益？",

    "Pause and predict. A manager is truly skilled, and investors can see it.":
        "暂停并预测。一位基金经理真正有技能，而且投资者看得出来。基金的投资者会赚得比市场多吗？基金经理呢？",

    # ------------------------------------------------------------------ Scale
    "Chapter three, and the answer to the pause: the investors earn about the market,":
        "第3章，以及暂停问题的答案：投资者赚得大约等于市场，而基金经理因技能获得报酬。乔纳森·伯克和理查德·格林的论证：资金流向显示出技能的基金经理，又因为技能"
        "不能规模化，资金会一直流入，直到基金给投资者的阿尔法为零。技能是真实的；它体现在基金的规模和基金经理的费用上，而不是投资者的收益上。",

    "The model, in the House's skill module.":
        "模型，在本系列公司的skill模块里。<bookmark mark='a'/>基金经理在第一美元上赚取毛阿尔法a，每多一美元都会降低它。<bookmark mark='b'/>投资者移动资金，"
        "直到扣除费用后的预期净阿尔法为零。<bookmark mark='c'/>他们不知道a，所以用贝叶斯法则从收益中学习它。<bookmark mark='d'/>所以基金规模跟随估计出的技能，"
        "而其投资者的预期阿尔法在每个时点都是零。",

    'f"Four hundred managers, twenty years, in simulation.':
        "四百位基金经理，二十年，模拟。<bookmark mark='a'/>最有技能的四十位随着业绩积累吸引资金；<bookmark mark='b'/>大多数基金经理几乎吸引不到资金：最后只有"
        "{sa:.0f}%还在管理资金。在这些人中，基金经理的最终规模与真实技能的相关系数为{ca:.2f}。资金市场找到了技能。",

    'f"And what investors earned.':
        "以及投资者赚到了什么。<bookmark mark='a'/>按实际投入的资金加权，净阿尔法围绕零散布：平均每年{an:+.1f}%。<bookmark mark='b'/>它与真实技能的相关系数"
        "为{cn:.2f}：毫无关系。<bookmark mark='c'/>最有技能的基金经理在第一美元上能赚{st:.1f}%；在它们达到的规模上，毛阿尔法为{gt:.1f}%，刚好约等于它们的"
        "费用。它们的技能变成了它们的规模。",

    'f"So who gets what.':
        "那么谁得到了什么。<bookmark mark='a'/>基金经理的收入是费率乘以资产：在模拟中，整个行业每年约{rv:.0f}个单位。<bookmark mark='b'/>增加的价值，即毛"
        "阿尔法乘以资产，约{va:.1f}。<bookmark mark='c'/>而提供资金的投资者赚得大约等于市场。技能是稀缺的投入，所以它的拥有者保留了租金。",

    "In real data. <bookmark mark='a'/> Jonathan Berk and Jules van Binsbergen":
        "在真实数据中。<bookmark mark='a'/>乔纳森·伯克和朱尔斯·范宾斯伯根用增加的价值来衡量技能：费前阿尔法乘以管理的资产。据他们报告，平均每只基金每年增加约"
        "三百万美元。<bookmark mark='b'/>增加过价值的基金会继续增加价值，而它们投资者的净阿尔法并不突出。<bookmark mark='c'/>技能和投资者的收益是两个不同的问题，"
        "而第二个问题由夏普的算术回答。",

    "Scale at the level of the industry.":
        "行业层面的规模。<bookmark mark='a'/>据卢博什·帕斯托、罗伯特·斯坦博和卢西安·泰勒报告，主动管理行业越大，每只基金表现越差。<bookmark mark='b'/>而且"
        "基金经理随时间变得更有技能，业绩却没有改善：更多的技能在争夺同样的错误定价。<bookmark mark='c'/>这就是格罗斯曼和斯蒂格利茨：知情的回报随知情者增多而"
        "下降。",

    "And why some managers refuse money.":
        "以及为什么有些基金经理拒绝资金。<bookmark mark='a'/>每个策略都有容量，超过某个规模，冲击成本就会吃掉阿尔法：用伯克和格林的语言说，就是第37部分的平方"
        "根律。<bookmark mark='b'/>据报道，一些最著名的量化基金曾退还外部资金，只管理自己的钱。<bookmark mark='c'/>而本系列公司从第34部分起，就按容量而不是需求"
        "来确定每个团队的规模。",

    "What follows for each of the three parties.":
        "这对三方各意味着什么。<bookmark mark='a'/>对选择基金的投资者：过去的收益对未来的净收益说明得很少，而费用说明得很多，并且事先就知道。"
        "<bookmark mark='b'/>对基金经理：容量是策略的一部分，超出容量的每一美元都由已有的投资者买单。<bookmark mark='c'/>对经济学家：投资者收益没有持续性，并不"
        "是没有技能的证据。这个市场恰好把技能藏在了第2章去找它的地方。",

    "Pause and predict. Has the American stock market become harder to predict":
        "暂停并预测。美国股市是不是变得更难根据自己的过去来预测了？猜一猜一九七〇年代和二〇一〇年代日收益的自相关。",

    # ------------------------------------------------------------------ Adaptive
    'f"Chapter four, and the answer to the pause: in the nineteen seventies,':
        "第4章，以及暂停问题的答案：一九七〇年代是{a70:.2f}；二〇一〇年代是{a10:.2f}。一天的收益曾经能预测第二天方向的相当一部分。现在它什么也预测不了，或者"
        "只预示轻微的反转。市场学会了，或者说交易者学会了。",

    "Andrew Lo's view.":
        "罗闻全的观点。<bookmark mark='a'/>有效市场假说说价格已经反映了所有信息。<bookmark mark='b'/>罗闻全的适应性市场说，有效性是会学习的交易者相互竞争的"
        "结果，而且它会变化。<bookmark mark='c'/>所以机会应当出现、被发现、被竞争掉，一个市场有多有效应当随交易它的人而改变。",

    "Ninety years of Kenneth French's daily market returns.":
        "肯尼斯·弗伦奇九十年的市场日收益。<bookmark mark='a'/>在每个滚动的五年窗口里，一天的收益与下一天的相关性。<bookmark mark='b'/>在这个世纪的大部分时间里"
        "它是正的，在一九七〇年代达到峰值，那时小盘股价格变动迟缓，使指数变得可预测。<bookmark mark='c'/>然后它下降，经历了股指期货的出现、电子交易，以及两千"
        "年之后的高频做市，降到零以下。",

    'f"By decade, with a second measure.':
        "按十年来看，用第二个指标。<bookmark mark='a'/>罗闻全和麦金雷的方差比：五日收益的方差除以日方差的五倍，随机游走为一。<bookmark mark='b'/>一九七〇年代是"
        "{v70:.2f}：周变动比日变动所暗示的更大，这是趋势的特征。二〇一〇年代是{v10:.2f}：轻微的均值回归。同一个市场，不同的生态。",

    'f"The variance ratio across horizons, two decades compared.':
        "跨期限的方差比，比较两个十年。<bookmark mark='a'/>在一九七〇年代，它随期限上升，二十天时达到{e70:.2f}：趋势。<bookmark mark='b'/>在二〇一〇年代它下降，"
        "到{e10:.2f}：反转。随机游走是两者之间的那条水平线。",

    "Why it fell. <bookmark mark='a'/> Not all of the old pattern was opportunity:":
        "为什么下降。<bookmark mark='a'/>过去的规律并不都是机会：一部分是很少交易的股票的陈旧价格，是测量效应。<bookmark mark='b'/>但随着交易变得便宜，微小的"
        "可预测性变得值得利用，而利用它们就消除了它们。<bookmark mark='c'/>一个会衰减的规律，正是在整个世纪上做回测时会被高估的东西。",

    "What the adaptive view implies.":
        "适应性观点意味着什么。<bookmark mark='a'/>风险溢价随投资者群体而变化，策略有生命周期，创新是公司生存的方式。<bookmark mark='b'/>它预言了拥挤，正如第33"
        "部分的量化地震所显示的，预言了策略收益的繁荣与萧条，以及一个平均有效、局部无效的市场。<bookmark mark='c'/>它做不到的，是说出下一个有效的策略是什么。",

    "The debate's most famous moment.":
        "这场争论最著名的时刻。<bookmark mark='a'/>二〇一三年，诺贝尔奖授予了尤金·法玛，他认为价格在短期内难以预测；罗伯特·席勒，他表明价格在长期内可以由估值"
        "预测；以及拉斯·彼得·汉森，他构建了检验两者的工具。<bookmark mark='b'/>这并不矛盾：缓慢变化的预期收益允许两者同时成立。<bookmark mark='c'/>这也是本系列"
        "自己在第6和第23部分的结论：缓慢变化的预期收益，测量误差很大。",

    "And the evidence that strategies decay.":
        "以及策略会衰减的证据。<bookmark mark='a'/>据大卫·麦克莱恩和杰弗里·庞蒂夫报告，他们跟踪了九十七个已发表的异象：原样本期之后收益约低四分之一，发表之后"
        "低一半以上。<bookmark mark='b'/>第一次下降是统计：样本中有一部分是运气。第二次是适应：投资者读了论文。<bookmark mark='c'/>而本系列公司对自己做了同样的"
        "检验。",

    'f"Adaptation, in the House\'s own record.':
        "本系列公司自己记录中的适应。<bookmark mark='a'/>加密货币套息，即第39部分的期现套利，二〇二〇年的研究夏普比率为{rs:.2f}，样本外为{hs:.2f}。"
        "<bookmark mark='b'/>随着机构进入，以及二〇二四年一月起美国现货交易所交易基金的推出，更多资本追逐同样的基差。<bookmark mark='c'/>它减半了，但没有消失，"
        "因为它仍在为其承担的融资和交易所风险提供回报。",

    "Pause and predict. Over this series the House registered twenty-five strategies,":
        "暂停并预测。在这个系列中，本系列公司登记了二十五个策略，并为每一个打开一次封存的样本外数据。你预计它们的夏普比率从研究期到样本外会下降多少？",

    # ------------------------------------------------------------------ Record
    'f"Chapter five, and the answer to the pause: the average Sharpe ratio went from':
        "第5章，以及暂停问题的答案：平均夏普比率从研究期的{mr:.2f}变为样本外的{mh:.2f}，两者的回归斜率为{sl:.2f}：每个策略高于平均的研究夏普中，大约一半"
        "保留了下来。在{r['n_long']}个研究窗口较长的策略上，斜率为{sll:.2f}。与麦克莱恩和庞蒂夫相近，而这一次完全没有选择展示哪些结果的余地。",

    "First, what the record is.":
        "首先，这份记录是什么。<bookmark mark='a'/>每个策略都登记了代码的哈希值、参数、成本模型和尝试过的配置数量。<bookmark mark='b'/>每一个选择都基于截至二〇"
        "二〇年底的数据。<bookmark mark='c'/>封存的样本外，二〇二一到二〇二五年，每个策略只打开一次，结果无论如何都展示出来；本系列公司的代码拒绝第二次查看。"
        "<bookmark mark='d'/>试验计数器累计了每一个尝试过的配置。",

    "The rows, in the order they were opened.":
        "这些行，按打开的顺序。<bookmark mark='a'/>第24部分的十个经典因子，在样本外开始之前很久就已发表：市场、价值和盈利能力表现很好；规模亏损；动量扣除成本后"
        "大致持平。<bookmark mark='b'/>然后是因子动物园的收缩组合，表现很好，以及第27部分的模型。",

    "<bookmark mark='a'/> The rest: text, mined alphas,":
        "<bookmark mark='a'/>其余的：文本、挖掘的阿尔法、组合构建、风险模型交易者、趋势与风险平价、统计套利、加密货币套息，以及本系列公司自己的组合。"
        "<bookmark mark='b'/>绿色表示按本系列公司的成本模型扣除成本后为正，红色为负。大多数是绿色；很少有远离其标准误的。",

    'f"All twenty-five at once.':
        "把二十五个放在一起。<bookmark mark='a'/>如果没有任何衰减，每个点都会落在虚线上。<bookmark mark='b'/>它们落在虚线下方，沿着一条斜率{sl:.2f}、截距{ic:.2f}"
        "的直线：研究夏普比率每高一点，样本外大约多换来半点。<bookmark mark='c'/>远在直线上方的点，一个币种网络和挖掘的阿尔法，研究窗口只有两年和三年，所以它们"
        "的研究夏普本身几乎没有被测准。",

    'f"By family.':
        "按类别来看。<bookmark mark='a'/>经典因子最可信，因为是别人几十年前选定的，从{cl['res']:.2f}变为{cl['hold']:.2f}，扣除成本后{cl['net']:.2f}。"
        "<bookmark mark='b'/>因子动物园的收缩组合和加密货币套息保持了很高的夏普比率。机器学习和文本在样本外比样本内更好，但研究窗口很短。组合构建和系统性宏观保持了"
        "适度的正值。",

    "Before the hold-out, what did the counter say about the searched strategies?":
        "在样本外之前，计数器对那些经过搜索的策略说了什么？<bookmark mark='a'/>紧缩夏普比率：研究夏普超过同样多次噪声试验中最好者的概率。加密货币套息和组合方法"
        "通过了。<bookmark mark='b'/>市场择时、文本信号、币种网络和挖掘的阿尔法没有通过：它们的研究无法把它们与运气分开。然后这四个中两个照样表现很好，两个没有。"
        "计数器衡量的是研究能声称什么，而不是未来会怎样。",

    'f"The trial counter, final:':
        "试验计数器，最终：<bookmark mark='a'/>整个系列共{tr:,.0f}个配置。<bookmark mark='b'/>搜索最多的策略，第29部分挖掘的阿尔法，尝试了一万三千零一十个"
        "配置；按这个数量紧缩后，它的研究记录与噪声中最好者无法区分。然后它在样本外表现很好。<bookmark mark='c'/>经典因子是别人几十年前选定的，不带有本系列公司"
        "自己的选择。<bookmark mark='d'/>教训：紧缩夏普比率低，意味着研究无法判断。它并不意味着策略会失败。",

    'f"And the hold-out has its own multiple-testing problem:':
        "样本外也有自己的多重检验问题：打开了二十五行。<bookmark mark='a'/>五年的夏普比率标准误约为{se:.2f}。<bookmark mark='b'/>所以二十五个毫无优势的策略中"
        "最好的一个也会显示约{bn:.2f}。<bookmark mark='c'/>有{na}行越过了这个门槛：动物园的两个组合、价值与动量、加密货币套息、挖掘的阿尔法和币种网络。",

    "What held, and what did not.":
        "什么站住了，什么没有。<bookmark mark='a'/>因子动物园的收缩组合、价值与动量组合、加密货币套息，以及市场本身，都表现很好。<bookmark mark='b'/>规模亏损，"
        "市场择时亏损，风险模型交易者被其范围内的稳定币拖垮。<bookmark mark='c'/>诚实的警告：五年很短。样本外夏普比率的标准误接近零点四五，所以大多数行既无法与"
        "其研究值区分，也无法与零区分。",

    "A word on the brightest rows.":
        "关于最亮眼的几行，说一句。<bookmark mark='a'/>因子动物园的组合是在二〇二一到二〇二三年上评分的，这是其开源数据库覆盖的年份，而且它们分散在数百个已发表"
        "的异象上。<bookmark mark='b'/>它们是纸面组合，交易其中小而缺乏流动性的部分的成本只能估计。<bookmark mark='c'/>但组合并收缩之后，已发表的异象在它们从未"
        "见过的三年里保留了大部分溢价。",

    'f"And the House\'s own row, registered in this part with one trial.':
        "以及本系列公司自己的那一行，在这一部分登记，只尝试一次。<bookmark mark='a'/>在十个经典因子之间等风险配置，权重由截至二〇二〇年的十年波动率固定。"
        "<bookmark mark='b'/>研究期夏普比率{rs:.2f}，扣除成本后{rn:.2f}。<bookmark mark='c'/>样本外{hs:.2f}，扣除成本后{hn:.2f}。在已发表溢价之间分散，这个系列"
        "里最平淡的策略，兑现了它大部分的承诺。",

    'f"The House\'s ensemble through the hold-out, month by month.':
        "本系列公司的组合在样本外逐月的表现。<bookmark mark='a'/>在二〇二二年股票和债券一起下跌的通胀冲击中，分散的溢价站住了。<bookmark mark='b'/>二〇二一年初"
        "的一个单位，到二〇二五年底变成{end:.2f}，未扣除成本：稳定，不惊艳，而且正如登记时所写。",

    'f"The verdict on the record.':
        "对这份记录的结论。<bookmark mark='a'/>{sp:.0f}%的行样本外夏普比率为正。<bookmark mark='b'/>但在五年里，只有{ss:.0f}%单独显著。<bookmark mark='c'/>"
        "第2章的斯托里估计量给出没有优势的比例约为{pi0:.2f}，这是一个来自二十五行的估计，研究者章节会说明它的分量。本系列公司找到的大部分东西是真实的，比看起来"
        "小，而且大多是已发表的溢价。",

    "Pause and predict. Nine pricing models were fitted to the same options surface":
        "暂停并预测。在第10到14部分，九个定价模型被拟合到同一个期权曲面上。哪一个拟合得最好，它是最复杂的吗？",

    # ------------------------------------------------------------------ Surface
    "f'Chapter six, and the answer to the pause: SSVI,":
        "第6章，以及暂停问题的答案：SSVI，{best['rmse']:.2f}个波动率点，它是对曲面本身的参数化，而不是关于价格如何变动的模型。在动态模型中，是粗糙Bergomi，"
        "{rb['rmse']:.2f}，只有少数几个参数。两者都不是最复杂的；各自都有正确的形状。",

    'f"The pricing scoreboard, every model on the same Bitcoin options surface,':
        "定价记分板，每个模型都在同一个比特币期权曲面上，用同一个指标。<bookmark mark='a'/>单一波动率的布莱克—斯科尔斯偏差{bs:.1f}个波动率点：第10部分的"
        "微笑。<bookmark mark='b'/>第13部分的跳跃把它减半，但没有更进一步。<bookmark mark='c'/>随机波动率，Heston，达到{hs:.2f}，粗糙Heston稍好一些。"
        "<bookmark mark='d'/>粗糙Bergomi和SSVI参数化拟合得最好：短期偏斜需要粗糙性，这是第14部分的论点，或者需要一个专门为拟合它而选的形状。",

    'f"Where the parts also tested tomorrow.':
        "那些也检验了第二天的部分。<bookmark mark='a'/>每个到期日一个波动率的布莱克—斯科尔斯：今天{b_in:.2f}，明天{b_out:.2f}。<bookmark mark='b'/>"
        "粗糙Bergomi，重放：{r_in:.2f}和{r_out:.2f}，站住了。<bookmark mark='c'/>一个路径依赖的波动率模型今天拟合得和粗糙Bergomi一样好，{p_in:.2f}，第二天"
        "却跌到{p_out:.2f}：第14部分的过拟合，也是记分板保留第二栏的原因。",

    "How the House's options desk uses the scoreboard.":
        "本系列公司的期权交易台如何使用这个记分板。<bookmark mark='a'/>报价时，用一个无套利的参数化曲面，它的任务是拟合今天。<bookmark mark='b'/>对冲和为奇异期权"
        "定价时，用一个对冲在明天依然有效的动态模型，重新校准，并记录它的误差。<bookmark mark='c'/>采用新模型时，按第14条规则：它必须在样本外、在交易台真正需要的"
        "东西上，胜过更简单的模型。",

    "Three lessons from the scoreboard.":
        "记分板的三个教训。<bookmark mark='a'/>拟合不是唯一的分数：参数化拟合今天的曲面，而动态模型还必须为明天的曲面定价并在其间对冲，前面各部分在样本外检验过这一点。"
        "<bookmark mark='b'/>正确的形状胜过更多的参数：参数同样多的跳跃模型比Heston拟合得更差，而参数很少的粗糙Bergomi比它们都拟合得好。<bookmark mark='c'/>一天的"
        "一个曲面是方法上的一课，而不是适用于所有市场的排名。",

    "And why this surface.":
        "以及为什么是这个曲面。<bookmark mark='a'/>比特币期权曲面公开、免费而且完整，所以本系列公司在第1部分冻结了一个，并保留第二天的数据用于检验。<bookmark mark='b'/>"
        "它的波动率很大，微笑比股指的更接近对称，所以换成股票曲面，一些模型的排名会不同。<bookmark mark='c'/>重要的是，记分板在任何模型建立之前就已固定：它是业绩记录"
        "在定价上的孪生兄弟。",

    "Pause and predict. After forty-three parts,":
        "暂停并预测。经过四十三个部分，你认为量化金融仍然无法回答的最大问题是什么？",

    # ------------------------------------------------------------------ Open
    "Chapter seven, and the answer to the pause, or eight of them.":
        "第7章，以及暂停问题的答案，或者说八个答案。每一部分都以开放问题结尾；这些是在整个系列中反复出现的问题，在市场中，在模型中，也在研究它们的工具中。",

    "In markets. <bookmark mark='a'/> The equity premium:":
        "在市场中。<bookmark mark='a'/>股权溢价：为什么股票长期以来比债券多支付了这么多，而消费却如此平稳，没有一个模型能在不作强假设的情况下解开这个谜题。"
        "<bookmark mark='b'/>粗糙波动率：波动率是真的粗糙，还是只在我们能测量的尺度上看起来如此，这对对冲又意味着什么。<bookmark mark='c'/>以及因子动物园的维数："
        "预期收益真正独立的来源有多少个，五个、二十个，还是数百个微弱的来源。",

    "In models. <bookmark mark='a'/> Learning when the signal is tiny:":
        "在模型中。<bookmark mark='a'/>信号极小时的学习：当收益的可预测部分只占其方差的百分之一时，灵活的模型何时胜过线性模型，以及如何在样本外之前就知道。"
        "<bookmark mark='b'/>对已经读过未来的语言模型进行诚实的检验，以及大规模地、只用每个日期当时已知的信息训练的模型。<bookmark mark='c'/>以及共用模型的机器对它们"
        "所交易的市场的稳定性有何影响，又该如何测量。",

    "In the system, and in the method.":
        "在系统中，也在方法中。<bookmark mark='a'/>如何让最安全的资产在恐慌中保持流动性：交易商的资产负债表、中央清算和基差交易。<bookmark mark='b'/>气候风险，在很短的"
        "数据上为很长的期限定价，本系列没有涵盖它，这本身就是一个开放问题。<bookmark mark='c'/>以及研究本身：每一次检验都会消耗一点数据的诚实，本系列公司的封存信封"
        "和计数器是一个答案，但不是最后的答案。",

    "And three things the series did settle,":
        "以及本系列确实解决了的三件事，至少就它自己的数据而言。<bookmark mark='a'/>正态风险价值会失败：在美国市场九十年的数据上，它被突破的次数远超承诺，而且成簇"
        "出现。<bookmark mark='b'/>学习算法可以不经沟通就合谋。<bookmark mark='c'/>回测不是预测：信封打开时，研究夏普比率会缩水。",

    "And the method the series used on all of them.":
        "以及本系列在所有问题上使用的方法。<bookmark mark='a'/>一个问题，一个模型，一个被证明的定理，然后用模拟或数据检验。<bookmark mark='b'/>数据按其已知的日期"
        "使用，有研究窗口和封存的样本外。<bookmark mark='c'/>每一次试验都被计数，结果无论如何都展示出来。",

    "Pause and predict. In nineteen hundred Louis Bachelier":
        "暂停并预测。一九〇〇年，路易·巴舍利耶把价格建模为可以跌到零以下的随机游走。一家大型交易所在什么时候改用了他的模型，为什么？",

    # ------------------------------------------------------------------ Bachelier
    "Chapter eight, and the answer to the pause: the twenty-second of April":
        "第8章，以及暂停问题的答案：二〇二〇年四月二十二日。两天前，西德克萨斯原油五月合约以每桶负三十七点六三美元结算。布莱克—斯科尔斯无法为负价格上的期权定价；"
        "巴舍利耶在一九〇〇年就可以。世界上最大的期货交易所把它的原油期权改用了他的模型。",

    "The episode, from the public record.":
        "这段经过，来自公开记录。<bookmark mark='a'/>二〇二〇年四月二十日，储油设施几乎已满，即将到期的五月合约持有人付钱让别人接手：结算价负三十七点六三。"
        "<bookmark mark='b'/>交易所的清算所宣布，从二十二日起，若干能源合约的期权将用巴舍利耶模型估值。<bookmark mark='c'/>第10部分的警告在实践中应验：模型的假设"
        "是产品的一部分，对数正态价格不可能为负。市场并不在乎。",

    "And oil was not the first time.":
        "原油也不是第一次。<bookmark mark='a'/>二〇一〇年代，欧元和日元利率跌到零以下，对数正态报价失效，互换期权市场转而用巴舍利耶的正态波动率报价：第19部分。"
        "<bookmark mark='b'/>价差，以及任何可能为负的东西，天然属于他的模型。<bookmark mark='c'/>存活下来的模型不是最优雅的，而是市场没有打破其假设的那一个。",

    "The two models. <bookmark mark='a'/> Bachelier's:":
        "两个模型。<bookmark mark='a'/>巴舍利耶的：价格按固定大小的正态增量变动，所以可以穿过零。<bookmark mark='b'/>他的看涨期权价格，一行就能写出。"
        "<bookmark mark='c'/>布莱克、斯科尔斯和默顿的：增量与价格成比例，所以价格保持为正。对股票更好；对原油，有几天是错的。",

    'f"The two models side by side, for a one-month call':
        "两个模型并排比较，标的是十美元原油期货的一个月看涨期权，两者在平值处的波动率相互匹配。<bookmark mark='a'/>在平值处它们一致，相差几美分。"
        "<bookmark mark='b'/>在远高于平值处，布莱克—斯科尔斯要价{khi_bs:.2f}，巴舍利耶为{khi_b:.2f}：对数正态价格有更长的右尾。<bookmark mark='c'/>而在零或"
        "更低的行权价上，布莱克—斯科尔斯没有答案，巴舍利耶给出零行权价看涨期权的价格{k0:.2f}。在二〇二〇年四月，重要的正是这一行。",

    "And Bachelier's deeper idea, where Part one began.":
        "以及巴舍利耶更深的思想，也是第1部分的起点。<bookmark mark='a'/>公平博弈：给定今天，明天价格的期望就是今天的价格。<bookmark mark='b'/>第4部分的定理："
        "那么用你所知道的信息构建的任何策略都不可能有正的期望收益。<bookmark mark='c'/>这一部分的算术，是同一思想的会计形式。比公平博弈赚得更多的，是风险或技能，"
        "而技能赚到的大约正是它的成本。",

    "And the man. <bookmark mark='a'/>":
        "以及这个人。<bookmark mark='a'/>一九〇〇年三月二十九日，路易·巴舍利耶在巴黎为他的投机理论论文答辩，亨利·庞加莱是答辩委员之一。<bookmark mark='b'/>"
        "论文包含了随机游走、比爱因斯坦关于布朗运动的论文早五年的扩散方程，以及在法国国债上检验的期权价格。<bookmark mark='c'/>它被遗忘了半个世纪，直到伦纳德·"
        "萨维奇和保罗·萨缪尔森发现了它。本系列就从那里开始。",

    "The whole arc. Bachelier's thesis;":
        "完整的弧线。巴舍利耶的论文；马科维茨的投资组合；萨缪尔森和法玛的有效价格；布莱克、斯科尔斯和默顿。<bookmark mark='a'/>哈里森和克雷普斯的测度；一九八七年的"
        "股灾；法玛和弗伦奇的因子；长期资本管理公司。<bookmark mark='b'/>金融危机；粗糙波动率；负油价与现金争夺；以及二〇二五年底本系列公司样本外的关闭。",

    "Pause and predict. The House began as an empty building":
        "暂停并预测。本系列公司起初是一栋空楼和一个封存的信封。说出本系列七幕中每一幕为它增加的一样东西。",

    # ------------------------------------------------------------------ Journey
    "Chapter nine, and the answer to the pause, act by act.":
        "第9章，以及暂停问题的答案，一幕一幕来。每一幕都为本系列公司建立了交易台，每一部分至少证明一个定理，然后用模拟或数据检验。下面简要列出，作为本系列公司现在"
        "所知道的东西的地图。",

    "Act one, foundations.":
        "第一幕，基础。<bookmark mark='a'/>它建立了公平博弈和时点数据的纪律，会计、鞅、随机微积分、计量经济学、波动率和控制。<bookmark mark='b'/>它证明了，"
        "除其他之外，方差比的规律，第2部分保证金背后的检验，公平游走能偏离多远，已实现方差的误差，以及估计给默顿投资者带来多少成本。它给本系列公司的教训：在知道"
        "之前，什么都不算知道；一个预测在被检验之前毫无价值。",

    "Act two, derivatives.":
        "第二幕，衍生品。<bookmark mark='a'/>套利检查器，布莱克—斯科尔斯和一个期权交易台，曲面以及拟合到它上面的每个模型，奇异期权，一个定价引擎和深度对冲。"
        "<bookmark mark='b'/>以及关于带摩擦的套利、对冲再平衡的最优区间、由需求驱动的期权价格、翼部的矩爆炸、粗糙模拟的收敛性，以及深度求解器误差界的定理。它的教训："
        "价格只与它的对冲一样好，每个模型的误差都必须在同一个记分板上衡量。",

    "Act three, rates, credit and macro.":
        "第三幕，利率、信用和宏观。<bookmark mark='a'/>一个曲线构建器和一个利率交易台，期限结构模型，一个信用交易台，XVA和清算，以及外汇和大宗商品。"
        "<bookmark mark='b'/>以及关于为什么曲线的因子看起来像水平、斜率和曲率，下限处的影子利率，信用组合中的集中度，错向风险的界，以及仓储经济学的定理。它的教训："
        "最安全的资产结构最多，信用交易台最严重的损失来自其交易对手共同的行为。",

    "Act four, asset pricing.":
        "第四幕，资产定价。<bookmark mark='a'/>风险与收益，因子库，业绩记录在这里打开了它的第一批行，以及因子动物园。<bookmark mark='b'/>以及关于分歧产生"
        "泡沫、动量利润的分解，以及已发表异象有多少是真实的定理。它的教训：能预测收益的东西大多是风险的补偿，其余的大多是运气。",

    "Act five, the quant's craft.":
        "第五幕，量化的手艺。<bookmark mark='a'/>回测协议和试验计数器，机器学习，文本和语言模型，一个阿尔法工厂，投资组合，一个风险模型和一个交易者，宏观账簿，"
        "统计套利，以及公司本身。<bookmark mark='b'/>以及关于众多回测中胜出者的推断、插值模型的风险、一个信号需要多少文本、挖掘的阿尔法、最优交易速率、趋势的恒等式、"
        "成本的区间规律，以及回撤止损的定理。它的教训：计数每一次试验，为每一笔交易收费。",

    "Act six, the market's machinery.":
        "第六幕，市场的机制。<bookmark mark='a'/>谁与谁交易，订单簿，执行，做市和速度竞赛，以及加密货币和去中心化金融。<bookmark mark='b'/>以及关于凯尔的"
        "连续拍卖、微观价格、瞬时冲击下的最优执行计划、狙击均衡，以及流动性提供者因套利而损失多少的定理。它的教训：每一笔交易的另一边都有人，而且他们通常知道些什么。",

    "And Act seven, the system.":
        "以及第七幕，系统。<bookmark mark='a'/>一个风险函数，流动性压力和危机档案，智能体、模拟器和合谋审计，以及这一部分的记录。<bookmark mark='b'/>以及关于什么"
        "能被回测、清算向量、羊群效应和合谋，以及在这一部分的研究章节中，如何计数技能以及技能流向何处的定理。它的教训：系统比它的任何部分都更脆弱，市场是默认选项。",

    'f"And the count.':
        "以及计数。<bookmark mark='a'/>七幕四十三个部分，每一部分都有一个研究章节。<bookmark mark='b'/>登记了{nr}个策略和预测，其中{nt}个是业绩记录的行。"
        "<bookmark mark='c'/>计数了{tr:,.0f}个配置。<bookmark mark='d'/>以及一个封存的样本外，为每一行打开一次，再也不会打开。",

    "Pause and predict. Forty-two rules later,":
        "暂停并预测。四十二条规则之后，本系列公司的最后一条规则应该是什么？",

    # ------------------------------------------------------------------ House
    "The answer to the pause, the forty-third rule.":
        "暂停问题的答案，第43条规则。<bookmark mark='a'/>假定本系列公司无法战胜市场。<bookmark mark='b'/>直到一份先登记、只打开一次、扣除成本、计数了每一次"
        "试验的记录说明并非如此。<bookmark mark='c'/>然后，按那份记录所能承受的程度确定下注规模；在五年之后，那是一个分仓，而不是整个基金。",

    'f"The House\'s last evening report, desk by desk.':
        "本系列公司最后一份晚间报告，逐个交易台。<bookmark mark='a'/>风险：每个数字都是预测，并附上它的回测。<bookmark mark='b'/>资金：杠杆有上限，保证金锁定，"
        "持有现金以防翻倍。<bookmark mark='c'/>智能体：每一个都与它自己的副本对抗检验。<bookmark mark='d'/>研究：业绩记录上{nr}行，计数了{tr:,.0f}次试验。"
        "<bookmark mark='e'/>以及投资组合：市场，一个有上限的溢价分仓，别无其他，直到记录给出理由。",

    "Chapter ten. The forty-third rule belongs to the whole House,":
        "第10章。第43条规则属于整个本系列公司，它是其他每一条规则都在为之铺路的那一条：举证责任在策略一方，而不在市场一方。",

    "Some of the rules that got the House here.":
        "把本系列公司带到这里的一些规则。<bookmark mark='a'/>第一条：时点。<bookmark mark='b'/>新模型必须在样本外胜过更简单的模型。<bookmark mark='c'/>回测"
        "协议：登记、计数、紧缩。<bookmark mark='d'/>风险数字是预测；在你还没收到的追加保证金通知中存活；在智能体自己创造的市场里检验它。<bookmark mark='e'/>以及"
        "最后一条：市场是默认选项。",

    "So what the House does with its money,":
        "那么本系列公司如何处置它的资金，作为教学示例，而非投资建议。<bookmark mark='a'/>核心持有市场本身，按指数成本。<bookmark mark='b'/>一个分仓投向本系列公司"
        "用已发表溢价构建并只打开过一次的那个策略，规模设定为风险有上限。<bookmark mark='c'/>研究继续：新的行现在登记，只在它们自己的窗口结束时打开。"
        "<bookmark mark='d'/>以及第40到42条规则的限制，在任何模型之外。",

    "The House, complete.":
        "本系列公司，完整了。数据和技术在最上面；交易台，从波动率和利率到信用、宏观和数字资产；研究、投资组合和风险，执行和做市；资金和合规在底层。四十三个部分"
        "之前，它还是一栋空楼和一个封存的信封。",

    "What the House would tell the people who join it.":
        "本系列公司会对加入它的人说什么。<bookmark mark='a'/>对新分析师：在运行检验之前把它写下来，计数你尝试的东西，把最后几年封存起来，并报告成本。"
        "<bookmark mark='b'/>对投资组合经理：低成本地持有市场，按样本外记录确定策略规模，并知道对面是谁。<bookmark mark='c'/>对研究者：证明你所声称的，在证明"
        "从未见过的数据上检验它，并发表零结果。",

    "The House's code for Chapter two.":
        "本系列公司第2章的代码。斯托里的估计只有两行：p值大于lambda的比例，再放大。巴拉斯、斯凯莱和韦尔默斯的比例，从每个显著的尾部减去该估计所隐含的幸运零假设。",

    "The tools this part adds, in the House's skill module.":
        "这一部分在本系列公司技能模块中新增的工具。<bookmark mark='a'/>夏普的算术与运气；技能的计数与定价；以及适应性有效性。<bookmark mark='b'/>以及完整的"
        "第43条规则。",

    "Three last tests to carry away.":
        "最后带走的三个检验。<bookmark mark='a'/>当一只基金五年跑赢市场时，问有多少人尝试过，仅凭运气会有什么结果，以及它的记录是否在运行之前登记。"
        "<bookmark mark='b'/>当一位经理有真正的技能时，问谁得到了它。<bookmark mark='c'/>当一个策略有效了几十年时，问支付它的那个市场是否仍然存在，以及它的样本外"
        "说了什么。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Two theorems.":
        "写给研究者。两个定理。第2章用没有技能的基金数量的估计来计数有技能的基金；第25部分说过它偏高，这一章证明为什么，以及相关性对它有什么影响。第3章说有技能"
        "经理的投资者得不到阿尔法；这一章也证明这一点，并用模拟检验两者。",

    "The setting. <bookmark mark='a'/> m tests,":
        "设定。<bookmark mark='a'/>m个检验，其中m₀个是真零假设：没有技能的基金或策略。<bookmark mark='b'/>每个零假设的p值是均匀分布的。这是唯一的假设。"
        "<bookmark mark='c'/>计数大于阈值lambda的p值。<bookmark mark='d'/>然后放大：如果每个大的p值都来自零假设，计数的平均值将是m₀乘以一减lambda。",

    "The theorem. <bookmark mark='a'/> The estimator's expectation":
        "定理。<bookmark mark='a'/>估计量的期望等于真实比例，加上一个来自p值落在lambda之上的备择假设的项。<bookmark mark='b'/>所以平均而言，它从不低估没有"
        "技能的基金比例；它向上的偏差恰好来自弱的备择假设。而且，证明清楚地表明，这不需要检验之间相互独立。",

    "The proof is linearity.":
        "证明就是线性。<bookmark mark='a'/>计数是示性函数之和，它的期望是它们的概率之和。完全没有用到独立性。<bookmark mark='b'/>每个零假设贡献一减lambda，"
        "因为它是均匀的；每个备择假设贡献它自己的概率。<bookmark mark='c'/>相除。<bookmark mark='d'/>多出来的项是一个概率除以一个正数，所以偏差向上，只有当没有"
        "任何备择假设的p值超过lambda时才消失。",

    "Which threshold?":
        "用哪个阈值？<bookmark mark='a'/>偏差随lambda上升而下降，因为强的备择假设很少有大的p值。<bookmark mark='b'/>但方差上升，因为被计数的p值更少了。"
        "<bookmark mark='c'/>一个偏差与方差的权衡，斯托里用自助法估计误差来解决。",

    'f"The check. A thousand tests, eighty percent nulls,':
        "检验。一千个检验，百分之八十是零假设，每种设定四百个样本。<bookmark mark='a'/>备择假设较弱时，估计量明显高于真值：在lambda为二分之一时，{wm:.3f}"
        "对零点八。<bookmark mark='b'/>备择假设较强时，{sm:.3f}，几乎无偏。<bookmark mark='c'/>而且在每个阈值上，每个模拟的平均值都落在定理的直线上。",

    "A corollary for Chapter two.":
        "第2章的一个推论。<bookmark mark='a'/>有技能的比例减去了预期的幸运零假设。<bookmark mark='b'/>根据定理，这个数平均而言被高估了。<bookmark mark='c'/>"
        "所以估计的技能比例偏低：在期望上，它是技能的一个下界。当巴拉斯、斯凯莱和韦尔默斯几乎没有发现技能时，偏差是站在技能一边的。",

    'f"What dependence does.':
        "相关性有什么影响。定理中的均值不需要独立性，但方差需要。<bookmark mark='a'/>检验相互独立时，估计在不同样本间的离散程度为{s0:.3f}。<bookmark mark='b'/>"
        "给每一对检验零点六的相关性，就像同一市场中的基金那样，均值几乎不变，而离散程度上升到{s6:.3f}。相关的检验让估计量平均而言保持诚实，但在任何一个样本中都"
        "不可靠。",

    'f"And how the estimate is used: controlling false discoveries,':
        "以及这个估计如何使用：在第2章的基金总体上控制错误发现。<bookmark mark='a'/>把基金的p值排序。<bookmark mark='b'/>本雅米尼和霍赫贝格的规则宣布最小的k个，"
        "k是p值低于q乘以k除以m的最大序号；错误发现的期望比例至多为q。<bookmark mark='c'/>对每只基金在百分之五水平上检验，宣布{nn}只基金有技能，其中{nf:.0f}%"
        "是错误的。<bookmark mark='d'/>在百分之十水平上用这个规则，宣布{nb}只，{fb:.0f}%是错误的：更少的宣称，而且是真的。",

    'f"Storey\'s q-values, on the same population:':
        "斯托里的q值，在同一个总体上：对每只基金，它会被宣布为有技能的最小错误发现率。<bookmark mark='a'/>最好的基金q值接近{q1:.3f}。<bookmark mark='b'/>"
        "到第十二只，{q12:.3f}。这里十二只都是真正有技能的，因为这个总体有二十二只阿尔法很大的有技能基金；技能更弱时，幸运的基金会在更靠后的位置混进来，而q值告诉你"
        "在哪里停下。",

    'f"And on the House\'s own record.':
        "以及在本系列公司自己的记录上。<bookmark mark='a'/>二十五行，针对样本外夏普为正的单侧p值：估计没有优势的比例为{p0:.2f}。<bookmark mark='b'/>自助法"
        "给出的百分之九十区间从{lo:.2f}到{hi:.2f}。<bookmark mark='c'/>而且因为许多行是相关的因子组合，真正的不确定性还要更大。定理说这个估计平均而言不会太低；"
        "二十五个相关的行能说的也就仅此而已。",

    "The second theorem, for Chapter three.":
        "第二个定理，对应第3章。<bookmark mark='a'/>在伯克和格林的市场中，给定今天所有公开信息，投资者明年净阿尔法的期望为零，所以它与任何公开信息都不相关，包括"
        "过去的收益。<bookmark mark='b'/>技能是真实的，它体现为规模，而不是投资者所得的持续性。",

    "The proof, in four lines.":
        "证明，四行。<bookmark mark='a'/>竞争性的资金流动设定基金规模，使期望净阿尔法为零。<bookmark mark='b'/>代入：明年净阿尔法剩下的，是投资者对技能估计的误差，"
        "加上噪声。<bookmark mark='c'/>后验均值是投资者的最佳猜测，所以给定他们所知，它的误差均值为零。<bookmark mark='d'/>由塔性质，他们所知道的任何东西，包括"
        "去年的收益，都与它不相关。第1部分的公平博弈，作为一个均衡重新出现。",

    'f"The check, in Chapter three\'s simulation.':
        "检验，在第3章的模拟中。<bookmark mark='a'/>把每只基金明年的净阿尔法对今年的回归：斜率{s1:+.3f}，标准误{e1:.3f}。没有持续性，正如定理所说。"
        "<bookmark mark='b'/>现在去掉资金流动：每只基金保持同样的规模。斜率变为{s2:.3f}。<bookmark mark='c'/>而那个世界的理论值，即基金收益方差中技能所占的比例，"
        "给出{th:.3f}。同样的经理，同样的技能：持续性随资金流动出现或消失。",

    "How the two theorems fit together.":
        "两个定理如何相互配合。<bookmark mark='a'/>第25部分给出了斯托里的估计；这一章证明了它的偏差、它在相关性下的表现，以及它对计数技能意味着什么。"
        "<bookmark mark='b'/>在实践中，它为每只基金给出一个q值，即它会被称为有技能的最小错误发现率。<bookmark mark='c'/>结合伯克和格林：技能可以被计数，但很少能"
        "被识别；而在技能存在的地方，竞争把它的回报从投资者转移给经理。",

    "Where this connects.":
        "与哪些研究相连。<bookmark mark='a'/>约阿夫·本雅米尼和约瑟夫·霍赫贝格的错误发现率，斯托里的估计使它更精确。<bookmark mark='b'/>在金融中：坎贝尔·哈维、"
        "刘岩和朱合庆为新因子设定的更高门槛，巴拉斯、斯凯莱和韦尔默斯关于基金的研究，以及关于已发表异象有多少能被复现的研究。<bookmark mark='c'/>以及布拉德利·埃夫"
        "隆的局部错误发现率：这只特定基金是零假设的概率，是第25部分收缩方法的近亲。",

    "Three open problems. <bookmark mark='a'/> Estimators whose variance":
        "三个开放问题。<bookmark mark='a'/>在所有检验共享同一个市场时，方差依然受控的估计量。<bookmark mark='b'/>时有时无的技能，正如适应性市场所预言的。"
        "<bookmark mark='c'/>以及把计数用在研究本身：一个领域已发表的结果中有多少是零假设。",

    "Pause and predict. The House's twenty-five rows are correlated.":
        "暂停并预测。本系列公司的二十五行是相关的。这会让斯托里对它们零假设比例的估计偏高、偏低，还是都不？",

    # ------------------------------------------------------------------ Outro
    "Part forty-three in thirteen lines.":
        "用十三句话概括第43部分。扣除成本之前，主动管理的资金恰好赚到市场收益；扣除成本之后，更少。运气很慷慨，基金足够多时，总有人看起来很出色。技能可以被计数，"
        "却无法被找到。在技能存在的地方，它变成了规模和费用。而且市场会适应：七十年代的规律已经消失。",

    "The House's record kept about half of its research Sharpe,":
        "本系列公司的记录在样本外保留了大约一半的研究夏普比率。大多数行为正；单独显著的很少。它自己的已发表溢价组合站住了。定价记分板奖励正确的形状而不是更多的参数。"
        "开放问题依然开放，这是诚实的。巴舍利耶的模型为负油价定了价。以及最后一条规则：市场是默认选项。",

    "And the series, in one picture.":
        "以及整个系列，一张图。七幕四十三个部分：基础，从公平博弈到随机微积分；衍生品，从无套利到深度对冲；固定收益与信用；资产定价与因子；量化的手艺，从回测到"
        "投资组合；市场的机制，从订单簿到执行、做市和加密货币；以及系统，从风险到危机、机器，以及这个问题。",

    "Three lessons from all forty-three parts.":
        "全部四十三个部分的三个教训。<bookmark mark='a'/>市场大体上是一个公平博弈：能被预测的通常是风险溢价，而不是免费午餐。<bookmark mark='b'/>诚实是一种"
        "方法：时点数据、封存的样本外，以及计数每一次试验，没有这些，每一次回测都只是广告。<bookmark mark='c'/>系统大于它的各个部分：杠杆、流动性和共用的模型可以把"
        "许多明智的决定变成一个脆弱的市场。",

    "The part on one card.":
        "这一部分浓缩在一张卡片上。夏普的算术。运气战胜指数的概率。斯托里的估计量。伯克和格林的均衡。以及巴舍利耶的看涨期权，一切开始的地方。",

    "Six last desk questions.":
        "最后六个交易台问题。开头的问题：技能还是运气？单凭一份记录说明不了多少；把跑赢市场的数量与运气会给出的数量相比。<bookmark mark='a'/>为什么主动管理"
        "必然落后于被动？算术。<bookmark mark='b'/>谁从技能中获益？经理，通过规模。",

    "A strategy worked for fifty years?":
        "一个策略有效了五十年？检查它的市场是否仍然存在。<bookmark mark='a'/>研究夏普比率为二？预期样本外只保留大约一半的超额部分。<bookmark mark='b'/>为什么"
        "斯托里的估计是保守的？线性。完整的解答在笔记中。",

    'f"The research chapter\'s pause, answered.':
        "研究章节的暂停问题，答案。<bookmark mark='a'/>平均而言都不：计数的期望是概率之和，无论相关性如何，证明从未用到独立性。<bookmark mark='b'/>但可靠性"
        "差得多：相关性为零点六时，均值保持在{m6:.2f}，而离散程度从{s0:.3f}上升到{s6:.3f}。",

    "And twelve problems:":
        "以及十二道习题：算术；十年里的运气；有多少基金会因偶然而显得显著；斯托里的估计；有技能的比例；伯克和格林的基金规模；方差比；样本外的标准误；样本外预测；"
        "以及巴舍利耶的平值看涨期权。然后是两道资格考试题：完整的斯托里估计量，以及夏普的算术与佩德森的例外。中英文解答都在笔记中。",

    "The books this part follows,":
        "这一部分依据的书籍，以及它引用的论文，从巴舍利耶到佩德森。屏幕上的每个数字都来自肯尼斯·弗伦奇的收益数据、本系列公司自己的业绩记录和信封、曲面的缓存拟合，"
        "或使用固定种子的模拟。",

    "And how to check all of it.":
        "以及如何检验这一切。<bookmark mark='a'/>每一部分的计算脚本都用公开数据和固定种子重新生成每一个数字，本系列公司的代码库经过测试。<bookmark mark='b'/>"
        "信封的登记表和业绩记录是提交到仓库的文件，所以任何人都可以检查没有一行被打开两次。<bookmark mark='c'/>以及下一步去哪里：每张参考卡片上的教科书，以及第7章"
        "的开放问题，每一个都是一篇论文。",

    "And what it was built on.":
        "以及它建立在什么之上。<bookmark mark='a'/>公开数据：肯尼斯·弗伦奇的数据库、FRED、AQR的数据集、开源资产定价数据库、美国证券交易委员会的文件、美国财政部，"
        "以及两家加密货币交易所的公开档案。<bookmark mark='b'/>论文，每一篇都注明作者，公司只按公开记录描述。<bookmark mark='c'/>以及一种先证明、后宣称的讲课习惯。",

    "The House began as an empty building, a sealed envelope and a counter at zero.":
        "本系列公司起初是一栋空楼、一个封存的信封和一个归零的计数器。它结束时，每个交易台都已建成，每一次试验都已计数，对它被建来提出的那个问题也有了诚实的回答："
        "你可以战胜市场，一点点，有时候，靠承担风险或真正的技能，而你只有在看之前就记分，才会知道是哪一种。<bookmark mark='a'/>《量化金融，从零搭建》到此结束。感谢你"
        "和我们一起搭建它。",

    "And, just as honestly, what the series could not test.":
        "同样诚实地说，本系列无法检验的东西。<bookmark mark='a'/>真实的基金记录：基金收益数据库需要授权，所以技能的计数是在一个已知真相的模拟总体上检验的，"
        "而不是在真实基金上。<bookmark mark='b'/>其他曲面：一天的一个比特币期权曲面为那个市场的模型排名，而不是为每个市场。<bookmark mark='c'/>更长的样本外："
        "封存的五年无法把大多数策略与其研究值区分开，也无法与零区分开。<bookmark mark='d'/>以及作为交易者的语言模型，本系列讨论过，但没有运行。每一项都是这门"
        "课程下一个版本应该开始的地方。",
}
