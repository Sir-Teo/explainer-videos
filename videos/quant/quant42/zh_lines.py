"""Chinese narration for quant42: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 人工市场 (artificial market), 基本面交易者 (fundamentalist),
图表交易者 (chartist), 典型事实 (stylised facts), 羊群效应 (herding), 生灭链 (birth-death chain), 贝塔二项分布
(beta-binomial), 信息瀑布 (information cascade), 模拟器 (simulator), 模拟矩方法 (method of simulated moments), 反事实
(counterfactual), 强化学习 (reinforcement learning), Q学习 (Q-learning), 离线强化学习 (offline RL), 回放 (replay),
算法合谋 (algorithmic collusion), 合谋指数 (collusion index), 冷酷触发 (grim trigger), 单次偏离原则 (one-shot deviation
principle), 冲击响应 (impulse response), 模型单一化 (monoculture), 共同份额 (common share), 熔断开关 (kill switch)."""

TITLE = '量化金融，从零搭建 · 第42部分：市场中的机器'

CHAPTERS = {
    'Hook': '这算合谋吗？',
    'Artificial': '1. 人工市场',
    'Herding': '2. 羊群效应',
    'Sims': '3. 模拟器',
    'Learning': '4. 学习交易',
    'LLM': '5. 作为交易者的语言模型',
    'Collusion': '6. 算法合谋',
    'Crowd': '7. 当所有人共用一个模型',
    'Stability': '8. 人工智能与金融稳定',
    'House': '9. 第42条规则：在智能体自己创造的市场里检验它',
    'Research': '写给研究者：合谋何时能够持续？',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part forty-two. Machines in the market:":
        "第42部分。市场中的机器：当交易者是会学习的程序、市场本身由它们组成时，会发生什么。人工市场、羊群效应、模拟器、会学习的做市商、"
        "不用交流就能合谋的算法，以及共用一个模型的人群。",

    'f"What this part finds. <bookmark mark=\'a\'/> Two learning pricing algorithms':
        "这一部分的发现。<bookmark mark='a'/>两个从不交流、会学习的定价算法，最终停在从竞争利润到垄断利润之间{100 * d95['delta']:.0f}%的位置，"
        "并且会惩罚降价的对手。<bookmark mark='b'/>回测不是环境：放在另一条规则的成交记录上回放，更宽的报价看起来值{rp['naive4']:.0f}；"
        "真实交易时，它只赚{rp['live4']:.0f}。<bookmark mark='c'/>一个为每位交易者提供五分之一订单的模型，提供了市场{100 * w2['common']:.0f}%的"
        "订单流。<bookmark mark='d'/>羊群效应有一条精确的定律，在第2章证明。",

    "The desk question for this part, answered in Chapter six.":
        "这一部分的交易台问题，在第6章回答。<bookmark mark='a'/>两个从不交流的算法，<bookmark mark='b'/>最终都报出很宽的价差。"
        "<bookmark mark='c'/>这算合谋吗？先记下你的答案；经济学家和律师的回答不同。",

    "Why it matters. <bookmark mark='a'/> Most trading volume in American equities":
        "为什么重要。<bookmark mark='a'/>据监管机构报告，美国股票和期货的大部分成交量已经由算法发出，其中会学习的算法占比越来越大。"
        "<bookmark mark='b'/>单个算法可以检验；由算法组成的市场却可能做出任何一个算法都没有被设计去做的事。<bookmark mark='c'/>而本系列公司自己的"
        "智能体正在与同类交易，有一天也可能被复制。",

    "And what this part is not. <bookmark mark='a'/> No agent here is a recommendation,":
        "以及这一部分不是什么。<bookmark mark='a'/>这里没有一个智能体是投资建议，也没有一个用真钱交易过。<bookmark mark='b'/>本系列公司在这一部分"
        "没有运行任何作为交易者的语言模型；第5章解释原因，以及公平的检验需要什么。<bookmark mark='c'/>每个学习得到的结果都来自本系列公司自己的模拟器，"
        "随机种子固定。",

    "Where this sits. Act seven, the system. Part forty measured risk":
        "这一部分的位置。第七幕，体系。第40部分度量风险，第41部分把它带进危机。这一部分把机器放进市场，观察它们对市场、对彼此做了什么。"
        "最后的第43部分追问：到底有没有人能战胜市场。",

    "Thirty years. Alan Kirman's ants;":
        "三十年。艾伦·柯曼的蚂蚁；零智能交易者；圣塔菲人工市场；卢克斯和马尔凯西。<bookmark mark='a'/>用于执行的强化学习；闪电崩盘；"
        "骑士资本；摩尔定律对墨菲定律。<bookmark mark='b'/>然后是卡尔瓦诺会合谋的学习者和ABIDES模拟器，最早关于人工智能与系统性风险的论文，以及"
        "二〇二四年监管机构的报告。",

    "The plan: artificial markets and herding;":
        "计划：人工市场与羊群效应；模拟器；会学习的做市商；作为交易者的语言模型；复现算法合谋；共用一个模型的人群；监管机构担心什么；以及说明"
        "合谋何时能够持续的定理。",

    "In the House, the research desk and the market makers":
        "在本系列公司里，研究部门和做市商把它们的学习型智能体带到合规部门面前，合规部门提出一个它们都没被训练来回答的问题：当它们成功时，市场会"
        "怎样？",

    "Pause and predict. A market of traders following simple rules:":
        "暂停并预测。一个由遵循简单规则的交易者组成的市场：有人认为价格会回归价值，有人追逐趋势。它能产生真实市场的肥尾和波动率聚集吗？如果能，"
        "它需要什么成分？",

    # ------------------------------------------------------------------ Artificial
    "Chapter one, and the answer to the pause: yes, if the agents switch":
        "第1章，以及暂停问题的答案：能，只要智能体在规则之间切换并相互模仿。交易者只遵循一种规则、或随机交易的市场，尾部很薄，波动率没有记忆。"
        "交易者在规则之间跟风切换的市场，两者都有。需要的成分不是智能，而是模仿。",

    "The first artificial stock market.":
        "第一个人工股票市场。<bookmark mark='a'/>一九九〇年代在圣塔菲研究所，布莱恩·阿瑟、约翰·霍兰、布莱克·勒巴伦、理查德·帕尔默和保罗·泰勒给每个"
        "智能体一组预测规则；智能体保留有效的规则，并用遗传算法繁殖新规则。<bookmark mark='b'/>学得慢时，市场稳定在理性预期价格上。学得快时，"
        "技术交易自发出现，伴随泡沫、崩盘和波动率聚集。<bookmark mark='c'/>教训是：市场的统计指纹需要许多规则相互依赖的适应性智能体，而不需要"
        "非理性的智能体。",

    "A smaller model with the same mechanism, after Reiner Franke and Frank Westerhoff,":
        "一个机制相同的更小模型，依照赖纳·弗兰克和弗兰克·韦斯特霍夫，放在本系列公司的agents模块里。<bookmark mark='a'/>基本面交易者预期价格回归"
        "价值。<bookmark mark='b'/>图表交易者外推上一次的变动，他们的订单噪声更大。<bookmark mark='c'/>做市商按两类人的合计需求移动价格。"
        "<bookmark mark='d'/>智能体会换组：持基本面观点的人越多，基本面就越有吸引力，这就是羊群效应；定价偏离越大，吸引力也越大。",

    "Two thousand simulated days.":
        "两千个模拟交易日。<bookmark mark='a'/>收益成串出现：平静的时段，然后是剧烈的时段。<bookmark mark='b'/>在它下面是图表交易者的份额。当羊群效应"
        "把人群推向图表交易，他们噪声更大、追逐趋势的订单占据主导，波动率上升；当巨大的定价偏离把他们拉回基本面，波动率下降。这里的波动率有一个"
        "看得见的原因：谁在交易。",

    "Side by side, on the same scale.":
        "并排放在同一刻度上。<bookmark mark='a'/>截至二〇二〇年美国市场的最后两千个交易日，右端是二〇二〇年三月。<bookmark mark='b'/>以及智能体市场的"
        "两千天。两者都有被风暴打断的平静时段。真实市场最猛烈的风暴更猛：第1章的智能体尾部更薄，下表会显示这一点。",

    'f"The stylised facts, side by side.':
        "典型事实，并排比较。<bookmark mark='a'/>超额峰度：美国市场九十五年为{f['real']['kurt']:.1f}，智能体市场为{f['sim']['kurt']:.1f}，"
        "高斯分布为零。<bookmark mark='b'/>尾部指数：智能体市场的尾部是厚的，虽然不如真实市场厚。<bookmark mark='c'/>收益本身在三者中都几乎不可预测。"
        "<bookmark mark='d'/>但收益的大小可以预测：相隔二十天，绝对收益的自相关在数据中是{f['real']['acf_abs'][4]:.2f}，在智能体市场中是"
        "{f['sim']['acf_abs'][4]:.2f}，而高斯分布什么都没有。",

    "Volatility clustering across horizons.":
        "跨越各个期限的波动率聚集。<bookmark mark='a'/>在真实市场里，波动率的记忆衰减得很慢，一百天后仍明显大于零。<bookmark mark='b'/>智能体市场的"
        "衰减方式相同，因为图表交易者的份额本身就变化缓慢：羊群效应让人群在一个状态里停留几周。<bookmark mark='c'/>高斯分布完全没有记忆。第7部分"
        "用GARCH拟合了这一点；这里是一个机制产生了它。",

    'f"Can the agent market be fitted to the real one?':
        "智能体市场能拟合到真实市场上吗？用模拟矩方法，在两个参数的网格上：图表交易者外推得有多猛，以及他们的订单噪声有多大。<bookmark mark='a'/>"
        "每一格是一次模拟，按其峰度和波动率记忆与美国市场的距离着色。<bookmark mark='b'/>最好的一格给出峰度{kurt_b:.1f}，目标是{kt:.1f}；"
        "二十天滞后的记忆为{acf_b:.2f}，目标是{at:.2f}；它位于网格边缘：没有一格达到真实市场的尾部。<bookmark mark='c'/>再看另一个轴：每一行都一样。"
        "改变噪声，损失变化{ratio:.1f}倍；改变图表交易者外推的力度，损失最多只变{spread:.0f}%。这两个矩只识别了一种行为，而不是两种：这是第3章的"
        "第一个警告。",

    "Why it works. <bookmark mark='a'/> Given who is trading,":
        "为什么有效。<bookmark mark='a'/>给定谁在交易，下一期收益的方差由两组人的份额和他们订单的噪声决定。<bookmark mark='b'/>份额变化缓慢，因为每个"
        "智能体是否换组取决于其他所有人。<bookmark mark='c'/>所以波动率是随机的，而且持续，有其原因：弗兰克和韦斯特霍夫称之为结构性随机波动率。",

    "The deterministic cousin, from William Brock and Cars Hommes.":
        "它的确定性表亲，来自威廉·布洛克和卡斯·霍姆斯。<bookmark mark='a'/>交易者以logit概率在预测规则之间选择，<bookmark mark='b'/>权重是每条规则"
        "最近的利润，所以潮流追随业绩。<bookmark mark='c'/>随着选择强度上升，位于基本面价值的稳态失去稳定，先变成周期，再变成混沌。他们称之为通往"
        "随机性的理性之路：不需要噪声，只需要向有效的规则切换。",

    "And the opposite extreme.":
        "以及相反的极端。<bookmark mark='a'/>达南杰·戈德和夏姆·孙德表明，在预算范围内随机出价的交易者，在双向拍卖中几乎达到完全的配置效率。"
        "<bookmark mark='b'/>多因·法默和合作者发现，随机的订单流能预测价差的大部分行为，即第36部分的模型。<bookmark mark='c'/>所以智能体模型把市场"
        "规则白送的东西，也就是效率，与需要行为才能产生的东西分开：肥尾和聚集来自模仿。",

    "Pause and predict. A hundred agents each sometimes switch view on their own,":
        "暂停并预测。一百个智能体，每个有时自己改变看法，有时模仿碰巧遇到的人。如果模仿远比独自改变常见，人群会把时间花在哪里：平分两边，还是"
        "别处？",

    # ------------------------------------------------------------------ Herding
    "f'Chapter two, and the answer to the pause: at the extremes.":
        "第2章，以及暂停问题的答案：在两端。当模仿占主导时，人群大部分时间几乎一致，偏向这一边或那一边，并不时在两者之间摇摆。它很少平分。"
        "像这里一样有一百个智能体时，它有{100 * k['bi']['p_edges']:.0f}%的时间完全一致。",

    "Alan Kirman's model, from a puzzle about ants.":
        "艾伦·柯曼的模型，来自一个关于蚂蚁的谜题。给蚂蚁两个完全相同的食物源，它们会挤到其中一个上，然后不时整体转移到另一个。"
        "<bookmark mark='a'/>每一步选出一个智能体。<bookmark mark='b'/>它以概率epsilon自己改变主意。<bookmark mark='c'/>否则它随机遇到另一个，并以"
        "一减delta的概率采纳对方的看法。<bookmark mark='d'/>持有看法A的人数上升或下降一：这是一条生灭链。",

    "A hundred agents. <bookmark mark='a'/> With copying far more common":
        "一百个智能体。<bookmark mark='a'/>当模仿远比独立切换常见时，份额停留在零或一附近，并突然跳到另一端。<bookmark mark='b'/>独立切换多十倍，"
        "同一群人就在一半附近徘徊。智能体完全相同；变化的只是独立思考与模仿之间的平衡。",

    "The theorem. <bookmark mark='a'/> The chain's stationary law is exactly beta-binomial,":
        "定理。<bookmark mark='a'/>这条链的平稳分布恰好是贝塔二项分布，参数alpha等于epsilon乘以N减一，再除以一减delta。<bookmark mark='b'/>"
        "所以随着人群扩大，份额收敛到两个参数都为alpha的贝塔分布。alpha大于一：中间一个峰。alpha小于一：U形，人群在两端。当独立切换比每N减一次"
        "转化中的一次还少时，羊群效应获胜。",

    "The proof is four lines.":
        "证明只有四行。<bookmark mark='a'/>生灭链是可逆的，所以细致平衡一步一步确定它的平稳分布。<bookmark mark='b'/>上升的概率：选中一个持B观点的"
        "智能体，然后它自己转变，或者遇到k个持A观点者之一。提出一减delta除以N减一这个因子，epsilon就变成alpha。<bookmark mark='c'/>下降的概率，同理。"
        "<bookmark mark='d'/>因子相消，剩下的恰好是贝塔二项分布相邻概率之比。",

    'f"The check. Forty million steps of each chain,':
        "检验。每条链四千万步，与定理给出的分布（白色）对比。<bookmark mark='a'/>羊群效应：U形，两端质量很大。<bookmark mark='b'/>独立：中间一个峰。"
        "<bookmark mark='c'/>模拟频率与精确分布的总变差距离分别为{k['bi']['tv_exact_sim']:.3f}和{k['uni']['tv_exact_sim']:.3f}，而链的分布与贝塔二项"
        "公式精确到最后一位。",

    'f"And a second exact result: how long the crowd stays.':
        "以及第二个精确结果：人群停留多久。<bookmark mark='a'/>对生灭链，从k下降一步的平均时间是一步，加上如果它先上升、再回到这里所需的时间：一个从"
        "顶端开始的递推。<bookmark mark='b'/>从百分之九十持A摆到百分之十，就是这些项的和。<bookmark mark='c'/>羊群人群需要{bt:,.0f}步，模拟为"
        "{bs:,.0f}步。<bookmark mark='d'/>独立人群需要{ut:,.0f}步，模拟为{us:,.0f}步：更短，因为独立人群本来就很少停在百分之九十。",

    'f"And how the crowd\'s size matters.':
        "以及人群规模的影响。<bookmark mark='a'/>保持alpha为零点二。一百个智能体时，人群有{100 * e[0]['p']:.0f}%的时间完全一致；一千个时是"
        "{100 * e[1]['p']:.0f}%；一万个时仍有{100 * e[2]['p']:.0f}%。<bookmark mark='b'/>这个概率按N的负alpha次方下降，慢到大群体仍会长时间接近一致。",

    'f"Put the herd in a market:':
        "把羊群放进市场：让价格等于基本面价值加上一个与人群情绪成正比的溢价，就像阿尔法拉诺、卢克斯和瓦格纳所做的那样。<bookmark mark='a'/>有羊群"
        "效应时，每当人群摇摆，收益就成串出现。<bookmark mark='b'/>独立智能体则不会。<bookmark mark='c'/>波动率的记忆是{a5h:.2f}对{a5u:.2f}，但超额"
        "峰度只有{kh:.1f}对{ku:.1f}。单靠羊群效应，解释聚集比解释市场的尾部更好；尾部需要第1章在规则之间的切换。",

    "Herding in a market. <bookmark mark='a'/> Thomas Lux and Michele Marchesi":
        "市场中的羊群效应。<bookmark mark='a'/>托马斯·卢克斯和米凯莱·马尔凯西构建了分成乐观者和悲观者、彼此跟风的图表交易者，以及基本面交易者，"
        "所有人通过传染和利润来切换。<bookmark mark='b'/>它产生了肥尾和波动率聚集，表现为图表交易者阶段性主导，而价格平均仍跟随基本面。"
        "<bookmark mark='c'/>西蒙娜·阿尔法拉诺、卢克斯和弗里德里希·瓦格纳把柯曼过程放进一个简单到可以估计的市场模型里，情绪服从本章的贝塔分布。",

    "In real markets. <bookmark mark='a'/> Josef Lakonishok, Andrei Shleifer and Robert Vishny":
        "在真实市场中。<bookmark mark='a'/>约瑟夫·拉孔尼肖克、安德烈·施莱弗和罗伯特·维什尼测量了同向交易一只股票的养老基金是否比偶然情况下更多："
        "多一点，主要在小盘股。<bookmark mark='b'/>羊群效应也可以是理性的：当别人的行动包含信息时，模仿是明智的，而信息瀑布仍可能是错的。"
        "<bookmark mark='c'/>用相同数据训练、或调用同一个模型的机器，不用见面就彼此模仿。那是第7章。",

    'f"How rational copying goes wrong, exactly.':
        "理性的模仿如何出错，精确地说。<bookmark mark='a'/>每个智能体得到一个私人信号，十次中对七次，依次行动，看得到之前的行动，看不到之前的信号。"
        "<bookmark mark='b'/>一旦某一方向的选择比另一方向多出两个，公开证据就压过任何单个信号，所有人都开始模仿：这就是瀑布。<bookmark mark='c'/>"
        "两两来看。意见一致的一对启动瀑布；意见不一致的一对相互抵消。所以第一对一致的人决定结果，胜负比为p平方比q平方。<bookmark mark='d'/>信号准确率"
        "为百分之七十时，人群有{pw:.1f}%的时间锁定在错误答案上；本系列公司的模拟给出{ps:.1f}%。四十个智能体的信息，汇总起来几乎可以确定答案，却"
        "被丢掉了。",

    "Pause and predict. A simulated market matches the real one on every stylised fact.":
        "暂停并预测。一个模拟市场在每一个典型事实上都与真实市场吻合。在它里面有效的策略，在真实市场里可能有效吗？",

    # ------------------------------------------------------------------ Sims
    "Chapter three, and the answer to the pause: not necessarily, and often not.":
        "第3章，以及暂停问题的答案：不一定，而且常常不会。吻合典型事实只说明模拟器重现了没有新人加入时价格如何变动。策略需要的是别的东西：市场如何"
        "对它自己的订单作出反应，以及其他交易者如何适应它。这两者都不在拟合模拟器所用的历史数据里。",

    "What a modern market simulator is, taking ABIDES as the example.":
        "以ABIDES为例，现代市场模拟器是什么。<bookmark mark='a'/>一个有限价订单簿的交易所。<bookmark mark='b'/>一群背景交易者，每个是一条简单规则，"
        "再加上被检验的策略。<bookmark mark='c'/>订单和成交作为带延迟的消息传递。<bookmark mark='d'/>输出一份成交记录，就像真实交易所打印的那样，"
        "外加任何历史记录都给不了的东西：因为这个策略在场而发生了什么。",

    "How to judge a simulator.":
        "如何评判一个模拟器。<bookmark mark='a'/>第一，典型事实：尾部、聚集、价差和深度。<bookmark mark='b'/>第二，响应：一笔大单的冲击，即第37部分的"
        "平方根律，以及它如何衰减。这才是策略真正感受到的。<bookmark mark='c'/>斯维特兰娜·维耶特伦科和合作者把两者都提议为真实性指标，并发现一个"
        "模拟器可以吻合前者却错过后者。",

    "Fitting one to data.":
        "把它拟合到数据上。<bookmark mark='a'/>模拟矩方法：选择参数，使模拟器的统计量与市场的吻合。<bookmark mark='b'/>每个典型事实是一个带权重的矩。"
        "<bookmark mark='c'/>或者直接从订单簿事件中学习模拟器，比如第36部分的队列模型或生成网络。它能很逼真地重现订单簿，但其中没有原因，所以无法说明"
        "任何人会如何对新事物作出反应。",

    "So the gap between simulation and reality has three sources.":
        "所以模拟与现实之间的差距有三个来源。<bookmark mark='a'/>人为痕迹：学习者会找到模拟器里一切能赚钱的东西，包括它的简化。一个过于耐心的噪声"
        "交易者就是白送的钱。<bookmark mark='b'/>反事实：历史显示的是没有你时市场如何变动，而有你时它会如何变动是假设出来的，不是测量出来的。"
        "<bookmark mark='c'/>以及适应：真实的竞争者会反过来学习，所以一个赚钱的策略会改变让它赚钱的那群人。",

    "This is an old problem in economics.":
        "这是经济学里的一个老问题。<bookmark mark='a'/>罗伯特·卢卡斯在一九七六年指出，在一种政策下估计出的关系在政策改变时会失效，因为人们会作出反应。"
        "拟合于过去的模拟器就是这样一种关系。<bookmark mark='b'/>答案是具有明确目标的智能体，它们的行为可以在新规则下重新计算；第1章的智能体只有"
        "规则，没有目标。<bookmark mark='c'/>监管者也在构建这样的模型：英格兰银行关于债券基金和交易商的智能体模型，用来研究压力下的甩卖。",

    "The House's own simulator for this part, small enough to understand completely.":
        "本系列公司为这一部分构建的模拟器，小到可以完全理解。<bookmark mark='a'/>一个每次变动一个最小报价单位的价值，只有知情交易者看得到。"
        "<bookmark mark='b'/>知情交易者只在报价错误时交易：第35部分的格洛斯滕和米尔格罗姆。<bookmark mark='c'/>报价离中间价越远，噪声交易者交易得越少："
        "第38部分的成交规律。<bookmark mark='d'/>以及一个做市商，它选择半价差，以及按库存把报价偏移多少；它赚取价差，扣除被知情者造成的损失和持有"
        "库存的费用。",

    "And what this simulator leaves out, honestly.":
        "以及这个模拟器坦白地省略了什么。<bookmark mark='a'/>没有订单簿：一个做市商，每边一个报价，没有队列，没有速度竞赛。<bookmark mark='b'/>其他交易者"
        "从不学习，而真实的知情交易者会像做市商研究它一样研究做市商。<bookmark mark='c'/>它故意做得很小：每个结果都能手算检验，所以其中出的任何问题"
        "都是学习者的错，而不是模拟器的错。真实的模拟器只会增加失败的方式。",

    "Pause and predict. A market maker learns its quotes by trial and error":
        "暂停并预测。一个做市商在百分之五的交易者知情的市场里通过试错学习报价。然后它被部署到百分之三十的交易者知情的市场。它会亏钱吗？它会比在更难"
        "的市场里训练的做市商做得更差吗？",

    # ------------------------------------------------------------------ Learning
    "f'Chapter four, and the answer to the pause: it still makes money,":
        "第4章，以及暂停问题的答案：它仍然赚钱，而且在这个市场里，它在哪个世界训练几乎无关紧要。在百分之五知情的市场训练，在百分之三十知情的市场里"
        "每场赚{e30:.0f}；在那里训练的做市商赚{h30:.0f}。两者缺的是经验：八条固定规则中最好的一条赚{b30:.0f}。",

    "Reinforcement learning in finance, so far in this series.":
        "本系列到目前为止的金融强化学习。<bookmark mark='a'/>对冲：第17部分的深度对冲，在模拟路径上学习。<bookmark mark='b'/>执行：第37部分的队列执行器。"
        "<bookmark mark='c'/>以及做市和配置：以报价或权重为行动，以库存或持仓为状态。本·汉布利、徐任远和杨慧宁综述了这四类。每一类都需要一个学习的"
        "环境，而每个环境都是一个模拟器。",

    "The market maker as a learning problem,":
        "把做市商看作一个学习问题，放在第3章的交易商市场里。<bookmark mark='a'/>它看到自己的库存和上一笔交易的方向。<bookmark mark='b'/>它选择半价差，"
        "以及是否按库存偏移报价。<bookmark mark='c'/>它的报酬是相对真实价值赚到的价差，加上库存价值的变化，减去风险费用。<bookmark mark='d'/>它用"
        "Q学习训练两万四千场，然后在新的场次上评分。",

    'f"One session, under the best fixed rule.':
        "最好的固定规则下的一场交易。<bookmark mark='a'/>价值每次漂移一个单位；做市商从来看不到它，只看到成交。<bookmark mark='b'/>它的中间价跟随订单流，"
        "落后于价值，两者之间的每一个缺口都是知情者的机会。<bookmark mark='c'/>它的库存来回摆动，偏移把它拉回零附近。四百步中有{n_tr}笔交易。",

    'f"First, every fixed rule, where fifteen percent of traders are informed.':
        "首先看每一条固定规则，百分之十五的交易者知情。<bookmark mark='a'/>一个单位的半价差几乎不赚钱：知情者把它吃掉了。四个单位又把噪声交易者赶走。"
        "<bookmark mark='b'/>最好的是{best['half']}个单位并偏移，每场{best['mean']:.0f}。按库存偏移让每种宽度的利润大约翻倍：卸掉风险和价差一样重要。",

    'f"Now the learners.':
        "现在看学习者。<bookmark mark='a'/>最好的固定规则，在每个市场里把八条都试一遍找到。<bookmark mark='b'/>在百分之五知情的市场训练的学习者：在它自己的"
        "市场里赚{g5:.0f}，约为最好规则{b05:.0f}的{share:.0f}%。九百五十万步的试错接近、但没有超过对八条简单规则的搜索。<bookmark mark='c'/>以及在"
        "困难市场里训练的学习者。比较最后一列：{h30:.0f}对{e30:.0f}，在噪声范围内相同。在正确的世界里训练没有帮助，而且下一张图会显示，单纯训练得更久"
        "也没有帮助。",

    'f"How the learning goes,':
        "学习过程如何，在训练进行时用新场次给贪婪策略评分。<bookmark mark='a'/>仅仅五百场之后，它就已经赚到{first:.0f}：价差和偏移很早就学会了。"
        "<bookmark mark='b'/>然后它并不稳定下来。随着很少访问的状态被修改，它的收益来回摆动，在{ep_low:,.0f}场后降到{low:.0f}，<bookmark mark='c'/>"
        "最后又回到{last:.0f}，始终没有达到最好固定规则的{best:.0f}。在这么嘈杂的市场里，步长固定的表格学习是在游荡，而不是收敛：这又是一个理由，"
        "本系列公司要在学习者即将部署的那一刻，用新数据给它评分。",

    "Why a fixed rule can beat a learner.":
        "为什么一条固定规则能战胜学习者。<bookmark mark='a'/>第38部分推导了最优报价：在指数成交规律下，使收入最大的价差是k分之一，再因逆向选择和库存而"
        "加宽。<bookmark mark='b'/>在这里，未考虑知情者时是两个单位，知情者的存在把最好的规则推到三个单位。<bookmark mark='c'/>一个什么都没被告知的学习者，"
        "必须从数百万笔交易中发现这一切。模型正确时，基于模型的方法获胜；只有模型错误时，学习才值得。",

    "What the learner trained in the easy market chose,":
        "在容易市场里训练的学习者，在平静的一步之后，按库存作出的选择。<bookmark mark='a'/>接近零库存时，它报两到四个单位。<bookmark mark='b'/>无论多头"
        "还是空头库存，它大多偏移并收窄，在能卸掉风险的一侧报得很紧。但相邻的格子意见不一：这些状态访问得太少，学不好，这是在嘈杂市场里靠经验学习的"
        "代价，也是它落后于最好固定规则的原因。",

    "The regime change, in detail.":
        "仔细看市场状态的变化。<bookmark mark='a'/>容易市场的学习者平均报大约三个单位。<bookmark mark='b'/>困难市场的学习者报得更紧，而不是更宽，任何关于"
        "市场的理论都不会这样建议：那是学习中的噪声。<bookmark mark='c'/>所以诚实的结论比通常的故事更窄。状态变化确实是一个新环境，但一个没有收敛的"
        "学习者，无法与一个学错了世界的学习者区分开。",

    'f"And why a backtest is not an environment.':
        "以及为什么回测不是环境。记录两单位规则的一场交易：谁交易了，什么时候。<bookmark mark='a'/>实盘中它赚{rp['live2']:.0f}。<bookmark mark='b'/>"
        "现在用通常的方法在这份记录上评估四单位规则：同样的交易，每笔好两个单位。它看起来值{rp['naive4']:.0f}。<bookmark mark='c'/>实盘运行，它只赚"
        "{rp['live4']:.0f}，比两单位规则还少，因为更宽的报价把噪声交易者赶走了。成交记录记下的是谁和旧报价交易，而不是谁会和新报价交易。",

    "The general problem has a name: offline reinforcement learning.":
        "这个一般问题有一个名字：离线强化学习。<bookmark mark='a'/>数据是旧策略采取的行动以及随后发生的事。<bookmark mark='b'/>问题是一个新策略本来能赚"
        "多少。<bookmark mark='c'/>重要性加权回答了它：按新策略以这种方式行动的可能性高多少或低多少，给每一步重新加权。<bookmark mark='d'/>但前提是旧策略"
        "曾经采取过新的行动。一个总是报两个单位的做市商，对四个单位一无所知；回放只是编造了答案。",

    "Why a table, when the field uses deep networks?":
        "这个领域都用深度网络，为什么这里用表格？<bookmark mark='a'/>深度强化学习用网络代替表格，或者直接学习策略，从而能处理多到无法列举的状态，比如整个"
        "订单簿。<bookmark mark='b'/>它解决不了样本效率、模拟器的假设或缺失的反事实，网络还可能更彻底地过拟合模拟器的怪癖。<bookmark mark='c'/>"
        "三十九个状态可以打印出来阅读，所以本系列公司能看到学到了什么，而不只是赚了多少。",

    "Pause and predict. Language models read the news and write trading plans.":
        "暂停并预测。语言模型阅读新闻、撰写交易计划。在历史数据上检验它，最难的问题是什么？",

    # ------------------------------------------------------------------ LLM
    "Chapter five, and the answer to the pause: knowing what happened.":
        "第5章，以及暂停问题的答案：知道发生了什么。一个用某日期之前的文本训练的语言模型，已经读过此前每个事件之后的新闻，所以在那段历史上的回测"
        "测量的可能是它的记忆，而不是它的判断。第28部分测量了这种前视偏差，并构建了只用某日期之前文本训练的小模型。这一章追问，当这样的模型变成交易者"
        "时，会有什么不同。",

    "Three ways they are used, as the research describes them.":
        "按研究文献的描述，它们有三种用法。<bookmark mark='a'/>作为阅读者：模型给新闻打分，供另一条交易规则使用，即第28部分的语气。<bookmark mark='b'/>"
        "作为规划者：一个智能体阅读、用文字推理并输出订单，有时是分析师、交易员和风险经理组成的流水线。<bookmark mark='c'/>以及作为群体：许多智能体在"
        "同一个模拟市场里，看它们一起形成什么价格。",

    "Why simulators matter for language models in particular.":
        "为什么模拟器对语言模型尤其重要。<bookmark mark='a'/>在真实历史上，模型可能记得随后发生的事。<bookmark mark='b'/>在模拟器里，新闻和结果都是合成的，"
        "没有什么可记的：这是对推理以及智能体之间互动的干净检验。<bookmark mark='c'/>但它是关于模拟器的证据。第3章的差距对它们和对其他任何东西一样适用。",

    "What an honest test would need.":
        "一个诚实的检验需要什么。<bookmark mark='a'/>在检验窗口开始之前就结束的训练数据。<bookmark mark='b'/>提示词、版本和每一次运行的登记记录，因为每次"
        "改写措辞都是计数器上的又一次试验。<bookmark mark='c'/>成本，以及第26部分针对尝试次数的折减。<bookmark mark='d'/>以及一个基准：使用同样文本的"
        "最简单规则。语言模型增加的就是两者之差。",

    "There are two clean ways out.":
        "有两条干净的出路。<bookmark mark='a'/>时间一致的模型，只用每个日期之前发表的文本训练，所以在那个日期的回测无法记得之后的事。第28部分构建了"
        "小型的这类模型。<bookmark mark='b'/>代价是每个日期一个模型，每个都落后于前沿，所以检验测量的是一个较旧模型的能力。<bookmark mark='c'/>或者等待："
        "只在模型发布之后的事件上检验。诚实，而且慢。",

    "And a risk that is new in scale.":
        "还有一个规模上全新的风险。<bookmark mark='a'/>许多公司调用同样少数几个基础模型，这是金融稳定理事会在二〇二四年指出的集中度：一个供应商，一个"
        "故障点。<bookmark mark='b'/>同一个模型被问到关于同一条新闻的相似问题，会给出相似的答案：不需要任何交流的相关交易。<bookmark mark='c'/>共用一个"
        "模型的人群就是跟风的人群，而第2章说明了这样的人群把时间花在哪里。",

    "What language-model traders could do to a market, in principle.":
        "语言模型交易者原则上可能对市场做什么。<bookmark mark='a'/>价格应当更快地吸收新闻，因为机器同时阅读每一条标题。<bookmark mark='b'/>但同样少数几个"
        "模型读同一条标题，会在同一时刻作出同样的反应：新闻时刻的第7章共同份额。<bookmark mark='c'/>而为机器读者写的文本，无论真假，都成了推动价格的"
        "手段。那里的防线是知道文本从哪里来，而不是更好的模型。",

    "Where the House stands.":
        "本系列公司的立场。<bookmark mark='a'/>它在这一部分没有运行任何作为交易者的语言模型。运行下载的模型代码超出了这次构建被允许的范围，而且没有干净"
        "截止日期的检验无论如何都只会测量记忆。<bookmark mark='b'/>它转而搭建了检验台：一个模拟器、一个登记簿、一个成本模型和基准，任何智能体都可以"
        "放进去。<bookmark mark='c'/>以及已知的情况：就本系列所能核实的而言，还没有一项公开发表、事先登记、样本外、扣除成本的大规模语言模型交易者检验。",

    "Pause and predict. Two pricing algorithms learn by trial and error.":
        "暂停并预测。两个定价算法通过试错学习。它们从不交流，一次又一次地相互定价。它们最终会停在竞争性价格上吗？",

    # ------------------------------------------------------------------ Collusion
    'f"Chapter six, and the answer to the pause: no,':
        "第6章，以及暂停问题的答案：不会，它们不会停在竞争性价格上。在本系列公司对一个著名实验的复现中，两个学习算法停在平均价格{d95['price']:.2f}，"
        "而竞争会给出{c['p_nash']:.2f}，垄断会给出{c['p_mon']:.2f}：从前者到后者走了{100 * d95['delta']:.0f}%。它们从未交换过一条消息。",

    'f"The experiment, from Emilio Calvano,':
        "这个实验来自埃米利奥·卡尔瓦诺、贾科莫·卡尔佐拉里、温琴佐·德尼科洛和塞尔吉奥·帕斯托雷洛。<bookmark mark='a'/>两家公司在logit需求下出售"
        "相似的商品。<bookmark mark='b'/>每家赚取它的利润率乘以需求。<bookmark mark='c'/>如果只相遇一次，各自作出最优反应，价格是{c['p_nash']:.2f}；"
        "拥有两家的垄断者会定价{c['p_mon']:.2f}。<bookmark mark='d'/>算法从跨越两者的十五个价格中选择。",

    "The learners. <bookmark mark='a'/> Each remembers only last period's two prices.":
        "学习者。<bookmark mark='a'/>每个只记得上一期的两个价格。<bookmark mark='b'/>它保存一张表，记录每个状态下每个价格有多好，并把表中的条目向所得"
        "利润加上下一步的折现价值推进一点：第8部分的Q学习。<bookmark mark='c'/>它随机探索，并越来越少。<bookmark mark='d'/>九十六个独立场次，每场"
        "一百五十万期。度量：利润位于竞争（零）和垄断（一）之间的什么位置。",

    'f"The result, by how much the learners value the future.':
        "结果，按学习者多看重未来来看。<bookmark mark='a'/>短视的学习者，折现因子为零，最终指数为{r0['delta']:.2f}：接近竞争，高出一点只是因为学习不完美。"
        "<bookmark mark='b'/>随着未来变得更重要，价格上升。<bookmark mark='c'/>在零点九五时，指数是{r95['delta']:.2f}。耐心使合谋成为可能，正如重复博弈"
        "理论所说：研究者章节会证明它。",

    'f"Session by session,':
        "逐场来看，折现因子为零点九五。<bookmark mark='a'/>每个点是一对学习者最终停下的地方。几乎所有点都位于竞争点（绿色）和垄断点（红色）之间，"
        "并远高于前者。<bookmark mark='b'/>只有{sym:.0f}%以相等价格结束：学习者常常不均等地分享收益，或在几对价格之间循环。<bookmark mark='c'/>"
        "在停在一对价格上的{n_fixed}场中，有{pun:.0f}%会对被迫的降价作出惩罚。平均的冲击响应并不是平均出来的假象。",

    'f"Is it collusion, or just slow learning?':
        "这是合谋，还是只是学得慢？卡尔瓦诺和合作者提出的检验。取学到的策略，在停在一对价格上的{c['n_ir']}场中取平均。<bookmark mark='a'/>强迫一号公司"
        "降价一期，降到它的最优反应。<bookmark mark='b'/>下一期，二号公司大幅降低自己的价格：一次惩罚。<bookmark mark='c'/>然后两者在大约{r['back']}期"
        "之内回到原来的位置。对维持高价的奖励和对降价的惩罚，在没有任何一方被告知的情况下学会了：这就是经济学家所说的合谋。",

    "In financial markets. <bookmark mark='a'/> Jean-Edouard Colliard,":
        "在金融市场中。<bookmark mark='a'/>让-爱德华·科利亚尔、蒂埃里·富科和斯特凡诺·洛沃让Q学习交易商相互竞争：据他们报告，价差高于竞争水平，但当"
        "逆向选择让利润风险更大时，高得少一些。<bookmark mark='b'/>窦文斯、伊塔伊·戈德斯坦和季妍把学习算法交给知情投机者：它们交易得没有竞争所要求的"
        "那么激进，价格包含的信息也更少。<bookmark mark='c'/>对交易商来说价格就是价差，而惩罚就是在对手降价之后报得更紧。",

    'f"The House\'s version of the market makers\' finding.':
        "本系列公司版本的做市商发现。给每一期的利润加上一个随机冲击，就像逆向选择对交易商所做的那样。<bookmark mark='a'/>小的噪声改变不大。"
        "<bookmark mark='b'/>与利润本身一样大的噪声把指数降到{hi['delta']:.2f}。合谋需要学习者能把对手的降价和坏运气区分开，而嘈杂的利润让这变得困难。",

    "Why this matters more for algorithms than for people.":
        "为什么这对算法比对人更重要。<bookmark mark='a'/>产业经济学家列出了让默契合谋更容易的因素：卖家少且相似、互动频繁、价格即时可见、需求稳定。"
        "<bookmark mark='b'/>算法把每一项都调高了：它们互动数百万次，即时看到对手的价格，而且永不遗忘。<bookmark mark='c'/>电子市场是极端情形：报价在"
        "微秒内对所有人可见，同样的少数几家公司每天在每只股票上相遇。",

    "And why the number of sellers matters, in one line of algebra.":
        "以及卖家数量为什么重要，用一行代数说明。<bookmark mark='a'/>商品完全相同时，合谋的公司平分垄断利润，稍微降价的公司拿走全部，而竞争什么也不留。"
        "<bookmark mark='b'/>研究者章节的阈值变成一减n分之一。<bookmark mark='c'/>两个卖家需要折现因子一半；十个需要十分之九。卡尔瓦诺和合作者报告，"
        "三个和四个学习者时合谋更少，正如公式所示。",

    "So, is it collusion?":
        "那么，这是合谋吗？<bookmark mark='a'/>对经济学家来说，是：价格靠奖励和惩罚维持在竞争水平之上。<bookmark mark='b'/>对法律来说，不清楚。竞争法"
        "主要禁止协议，没有交流的协调通常是合法的；学来的协调算不算，是一个悬而未决的问题，约瑟夫·哈林顿对此有过论述。<bookmark mark='c'/>证据也开始"
        "出现：据斯蒂芬妮·阿萨德和合作者报告，德国加油站采用定价算法后，在本地双寡头中两家都采用的地方，利润率上升了。",

    "And the cases regulators have brought so far are of a different kind.":
        "而监管者迄今提起的案件属于另一类。<bookmark mark='a'/>二〇二四年，美国司法部起诉RealPage，指控其租金定价软件让相互竞争的房东通过共享数据"
        "协调租金。这些指控存在争议，这里只作为指控报道。<bookmark mark='b'/>其理论不是两个学习者自己发现了合谋，而是一个算法为许多竞争者定价：一个"
        "枢纽，就像第7章的共享模型。<bookmark mark='c'/>授权给许多交易商的报价模型具有同样的结构，这就是为什么本系列公司的审计也针对供应商的模型。",

    "Pause and predict. A hundred traders each take a fifth of every trade":
        "暂停并预测。一百个交易者，每笔交易都有五分之一来自同一个共享模型的信号，其余来自各自独立的判断。市场订单流的方差中，有多大份额是所有人共同的？",

    # ------------------------------------------------------------------ Crowd
    'f"Chapter seven, and the answer to the pause:':
        "第7章，以及暂停问题的答案：{100 * r['common']:.0f}%。每笔交易的五分之一来自共享模型，但这些五分之一都指向同一个方向，而其余五分之四在一百个"
        "交易者之间相互抵消。所以共同部分主导了市场的订单流。一点点共享的输入，乘以一个人群，就是市场看到的大部分东西。",

    "The concern, stated before the language-model boom.":
        "这个担忧在语言模型热潮之前就已提出。<bookmark mark='a'/>加里·根斯勒和莉莉·贝利在二〇二〇年指出，深度学习可能通过单一化提高系统性风险：相似"
        "的模型，用相似的数据训练，从少数供应商处购买。<bookmark mark='b'/>乔恩·丹尼尔松、罗伯特·麦克雷和安德烈亚斯·乌特曼指出，学到同样教训的风险引擎"
        "会让风险管理更加顺周期。<bookmark mark='c'/>机制不是一个坏模型，而是同一个模型无处不在，于是一个错误同时成了所有人的错误。",

    "The arithmetic. <bookmark mark='a'/> Each trader's order puts a weight w":
        "算术。<bookmark mark='a'/>每个交易者的订单在共享信号上放权重w，其余放在自己的判断上。<bookmark mark='b'/>把它们加起来。共享部分相干地叠加，"
        "N平方乘w平方；私人部分像随机游走一样叠加，N乘以一减w的平方。<bookmark mark='c'/>所以对任何正的w，共同份额都随人群规模增长。"
        "<bookmark mark='d'/>权重五分之一、一百个交易者时，是百分之八十六。",

    'f"In simulation, with a hundred traders whose orders move the price.':
        "在模拟中，一百个交易者的订单推动价格。<bookmark mark='a'/>波动率对共享模型权重的关系。权重五分之一时，它已经是多样化市场的{r2['vol_ratio']:.1f}倍；"
        "所有人都跟随模型时，是十倍。<bookmark mark='b'/>这些点落在公式的曲线上。<bookmark mark='c'/>标签显示共同份额：权重超过十分之一后，市场看到的一切中"
        "有一半以上是同一个信号。",

    'f"Now let the shared model make one mistake:':
        "现在让共享模型犯一个错：某一天它的信号错了四个标准差。<bookmark mark='a'/>在多样化市场里，什么都不会发生：没人听它的。<bookmark mark='b'/>"
        "权重五分之一时，那天的变动是多样化市场日波动率的{r2['shock_sd']:.0f}倍。所有人都用这个模型时，超过五十倍。对一家公司只是噪声的模型错误，"
        "对共享它的市场就是一场崩盘。",

    "How would anyone see it coming?":
        "怎样才能提前看到它？<bookmark mark='a'/>用少数几个共同因子为许多交易者的订单流建模：把第31部分的风险模型用在订单流而不是收益上。"
        "<bookmark mark='b'/>因子解释的订单流方差份额，就是这一章测量出来的共同份额。<bookmark mark='c'/>份额上升说明人群正在趋同。拥有逐笔交易数据的"
        "监管者可以追踪它；一家公司至少可以追踪自己的订单流与其他所有人的相关性变得多高。",

    "Three conclusions. <bookmark mark='a'/> Diversity is a public good.":
        "三个结论。<bookmark mark='a'/>多样性是一种公共品。每家公司都因使用能找到的最好模型而获益；所有公司都这样做时市场受损，却没有一家公司承担这个"
        "成本。这又是第41部分的甩卖外部性。<bookmark mark='b'/>能减少它的：不同的数据、期限和目标，以及对整个人群起约束作用的限制。<bookmark mark='c'/>"
        "以及要检验什么：一个策略对抗它自己的副本时表现如何，也就是它成功并被模仿后会面对的市场。",

    "Pause and predict. The International Monetary Fund and the Financial Stability Board":
        "暂停并预测。国际货币基金组织和金融稳定理事会都在二〇二四年发布了关于金融业人工智能的报告。你认为最让它们担心的是什么？",

    # ------------------------------------------------------------------ Stability
    "Chapter eight, and the answer to the pause: the last two chapters.":
        "第8章，以及暂停问题的答案：就是前两章。两份报告都把相关性和集中度放在前列：许多公司依赖同样少数几个模型和供应商，以机器速度朝同一方向交易，"
        "使市场在压力下变动得更快、更远。两者都没有说这已经大规模发生；两者都说条件正在形成。",

    "What the reports said, in their own framing.":
        "两份报告按它们自己的框架说了什么。<bookmark mark='a'/>国际货币基金组织二〇二四年十月的稳定报告：人工智能可能提高交易速度、成交量和策略之间的"
        "相关性，并在压力下放大波动；它建议审视熔断机制和保证金规则。<bookmark mark='b'/>一个月后的金融稳定理事会：对集中的模型和云服务供应商的依赖、"
        "市场相关性、网络风险和模型风险。<bookmark mark='c'/>两者的共同点：尚无证据表明人工智能已经大规模引发不稳定，而且用来寻找证据的数据很少。",

    "The rules that exist, as of this part.":
        "截至这一部分已有的规则。<bookmark mark='a'/>在欧洲，自二〇一八年起，算法交易者必须在使用前检验每个算法，能够立即停止它，并限制它能发送的量。"
        "<bookmark mark='b'/>在美国，自二〇一〇年起，经纪商必须在订单到达市场之前拦截超出风险限额的订单。<bookmark mark='c'/>欧洲的《人工智能法》按用途"
        "监管，在金融领域把信用评分和部分保险定价列为高风险，交易仍由原有规则管辖。<bookmark mark='d'/>以及据报道，美国二〇二三年关于经纪商预测性数据"
        "分析的一项提案，在二〇二五年被撤回。",

    "Andrei Kirilenko and Andrew Lo put the problem in two laws.":
        "安德烈·基里连科和罗闻全用两条定律概括这个问题。<bookmark mark='a'/>摩尔定律：计算越来越快、越来越便宜，所以更多交易被自动化。<bookmark mark='b'/>"
        "墨菲定律：凡是可能出错的都会出错，而在机器速度下，它会在任何人能干预之前就出错。<bookmark mark='c'/>风险就在两者之间的差距：技术跑在了为更慢的"
        "市场设计的控制之前。",

    "What machine-speed failures have looked like so far, from the public record.":
        "依据公开记录，迄今为止机器速度的失败是什么样子。<bookmark mark='a'/>二〇一〇年的闪电崩盘，第35部分。<bookmark mark='b'/>据报道，二〇一二年的骑士资本"
        "在旧代码被重新启用后的四十五分钟内亏损约四亿四千万美元。<bookmark mark='c'/>二〇一四年十月的美国国债市场，十年期收益率在没有新闻的情况下十二分钟内"
        "下跌十六个基点又恢复。<bookmark mark='d'/>二〇一六年英镑两分钟内下跌约百分之六。<bookmark mark='e'/>这些都不是学习型机器造成的。它们都是自动化的"
        "流动性一起撤出，快过控制措施的反应。",

    "And inside the firm, an older discipline.":
        "在公司内部，还有一门更老的纪律。<bookmark mark='a'/>美国银行监管机构二〇一一年的模型风险指引要求每个模型都经过独立验证，写明其局限，并监控其"
        "使用。<bookmark mark='b'/>学习打破了这个计量单位：一个会自我重训的模型每次都是一个新模型，所以验证必须覆盖产生模型的程序。<bookmark mark='c'/>"
        "而为每个智能体的交易负责的是一个人，而不是一个算法。这是上面所有制度的共同之处。",

    "So the controls come in three layers.":
        "所以控制分三层。<bookmark mark='a'/>公司内部：模型之外的限额和熔断开关，模型无法通过学习绕过。<bookmark mark='b'/>交易所：价格带、暂停和批量拍卖，"
        "让人群慢下来。<bookmark mark='c'/>以及体系层面：模型、数据和供应商的多样性，以及度量它的手段，而这还没有人拥有。",

    "Pause and predict. Before the House lets a learned agent trade,":
        "暂停并预测。在本系列公司让一个学习型智能体交易之前，除了它受训的市场，还应该用什么来检验它？",

    # ------------------------------------------------------------------ House
    "The answer to the pause: four tests.":
        "暂停问题的答案：四项检验。<bookmark mark='a'/>在与它受训市场不同的市场里。<bookmark mark='b'/>对抗它自己的副本：如果它有效并被模仿，它会面对的市场。"
        "<bookmark mark='c'/>面对一次被迫的偏离：它会学着惩罚降价的对手吗？如果会，它就是在合谋。<bookmark mark='d'/>以及在模拟器里实盘运行，绝不在另一个"
        "策略的成交记录上回放。",

    "Chapter nine. The House's forty-second rule":
        "第9章。本系列公司的第42条规则属于它的研究部门和做市商，由合规部门监督。一个学习型智能体不仅要在它受训的市场里评估，还要在它自己的成功会创造的"
        "市场里评估。",

    'f"The scorecard for this part\'s own agents.':
        "这一部分自己的智能体的记分卡。<bookmark mark='a'/>无论在哪里训练，做市商在困难市场里都赚大约{h30:.0f}，而最好的固定规则赚{best30:.0f}。"
        "<bookmark mark='b'/>每笔交易有五分之一来自共享模型，使{100 * w2['common']:.0f}%的订单流成为共同的。<bookmark mark='c'/>定价学习者会合谋并惩罚。"
        "<bookmark mark='d'/>而回放会让一条报价规则的表面利润多出两倍以上。<bookmark mark='e'/>没有一个通过。",

    "The collusion audit, which compliance now runs":
        "合规部门现在对每个定价或报价智能体运行的合谋审计。<bookmark mark='a'/>让智能体与它自己的副本对抗，直到两者稳定。<bookmark mark='b'/>强迫一个副本降价"
        "一次。<bookmark mark='c'/>观察另一个接下来做什么。<bookmark mark='d'/>先降价、再回到原来的水平，是奖惩机制的特征，这个智能体在交易之前就要被退回。",

    "And the governance around it.":
        "以及围绕它的治理。<bookmark mark='a'/>模型之外的限额，由智能体看不到的代码执行，并有一个由人控制的熔断开关。<bookmark mark='b'/>刻意的多样性："
        "本系列公司的任何两个智能体都不会同时共享数据和目标。<bookmark mark='c'/>每一种配置、随机种子和重训都算作一次试验，在评分之前登记。",

    "And the agent registry.":
        "以及智能体登记簿。<bookmark mark='a'/>一个智能体就是它的代码、数据、随机种子，以及它学习时所用模拟器的版本：足以精确重建它。<bookmark mark='b'/>"
        "每次重训产生一个新的智能体，也是本系列公司计数器上的一次新试验。<bookmark mark='c'/>批准意味着对每个新智能体重新运行四项检验。上个月通过、之后"
        "又重训过的智能体，不算通过。",

    "The House's code for Chapter six.":
        "本系列公司第6章的代码。两家公司都选择之后，新状态就是这对价格。每家公司拿到自己的利润，加上新状态下最好价格的折现价值，并把表中的条目向这个目标"
        "移动一步。其中没有任何地方提到对手的意图，也没有提到合谋。",

    "And the audit. Force firm one":
        "以及审计。强迫一号公司在一期内对二号公司的价格作出最优反应，然后让两者按学到的策略行动，并记录随后的价格。",

    "The tools this part adds, in the House's agents module.":
        "这一部分在本系列公司agents模块中增加的工具。<bookmark mark='a'/>人工市场与羊群效应；交易商市场及其学习者；合谋与单一化。<bookmark mark='b'/>"
        "以及第42条规则。一个学习型智能体只有在以下检验之后才能交易：在它从未受训的市场里，对抗它自己的副本，面对一次被迫的偏离，并且是实盘而不是"
        "回放。它的限额放在它之外。",

    "Three tests to carry away. <bookmark mark='a'/> When an agent did well in a simulator,":
        "三个随身带走的检验。<bookmark mark='a'/>当一个智能体在模拟器里表现很好，问模拟器对别人如何响应作了什么假设，以及这个智能体在它从未见过的状态里"
        "表现如何。<bookmark mark='b'/>当价格在没有协议的情况下居高不下，问一个卖家降价之后会发生什么。<bookmark mark='c'/>当许多公司使用同一个模型，问它"
        "驱动了多大份额的订单流，以及它的一个错误会造成什么。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter six watched learning algorithms":
        "写给研究者。第6章观察到学习算法维持高价并惩罚降价的对手。这一章证明这种行为在什么情况下能够成为均衡，为第6章的博弈计算阈值，并与学习者实际"
        "做的事情比较，而两者并不相同。",

    "Three numbers from the one-period game.":
        "单期博弈中的三个数。<bookmark mark='a'/>pi c，两家都收取合谋价格时每家的利润。<bookmark mark='b'/>pi d，对手维持该价格时，一家通过降价在一期内"
        "能赚到的最多利润。<bookmark mark='c'/>以及pi n，一次性纳什利润。<bookmark mark='d'/>降价今天有利，合谋比竞争有利，而博弈无限重复，收益按delta"
        "折现。",

    "The tool. <bookmark mark='a'/> A strategy profile is subgame perfect":
        "工具。<bookmark mark='a'/>一个策略组合是子博弈完美的，当且仅当没有参与者能通过在单个历史处偏离、然后回到原策略而获益。<bookmark mark='b'/>"
        "在收益有界的折现博弈中，任何有利的偏离都可以截短成一个有利的单次偏离，因为遥远的未来几乎不算数。所以一次检查一期就够了。",

    "For the researcher who wants the lemma proved too, the sketch.":
        "给也想看到引理证明的研究者，一个概要。<bookmark mark='a'/>假设某个偏离在某个历史处获益epsilon。<bookmark mark='b'/>截断它：照它走T期，然后回到"
        "原策略。收益有界，所以T之后发生的事至多值二M乘delta的T次方，再除以一减delta。<bookmark mark='c'/>T足够大时，截断后的偏离仍然获益。"
        "<bookmark mark='d'/>取最短的有利偏离。在它最后一个偏离的历史处，偏离一次然后回去必然已经有利，否则就会有更短的偏离。所以存在一个有利的单次偏离。",

    "The theorem. <bookmark mark='a'/> The grim-trigger strategy,":
        "定理。<bookmark mark='a'/>冷酷触发策略，即只要双方一直收取合谋价格就继续收取，一旦有任何偏离就永远收取纳什价格，是子博弈完美均衡，当且仅当"
        "delta至少为pi d减pi c，除以pi d减pi n。<bookmark mark='b'/>耐心必须超过偏离的诱惑，以惩罚的代价来衡量。",

    "The proof, by the lemma.":
        "证明，借助引理。<bookmark mark='a'/>在路径之外，偏离之后双方永远收取纳什价格。这是子博弈完美的：面对一个无论你做什么都收取纳什价格的对手，任何单次"
        "偏离都无利可图。<bookmark mark='b'/>在路径上，比较永远合谋，与偏离一次赚取pi d、然后永远纳什。<bookmark mark='c'/>两边乘以一减delta。"
        "<bookmark mark='d'/>移项整理。因为pi d大于pi c，pi c又大于pi n，阈值严格位于零和一之间。",

    "A corollary, for forgiving punishments like the learners'.":
        "一个推论，针对学习者那样会宽恕的惩罚。<bookmark mark='a'/>用纳什价格惩罚T期，然后回到合谋。<bookmark mark='b'/>由同一个引理，当今天的收益不超过"
        "惩罚期间损失的利润时，它能阻止偏离。<bookmark mark='c'/>惩罚越短需要越多耐心，而随着T增大，阈值下降到冷酷触发的阈值。",

    'f"For Chapter six\'s logit game.':
        "对第6章的logit博弈。<bookmark mark='a'/>在垄断价格处，三种利润如图。<bookmark mark='b'/>只要delta高于{m['grim']:.2f}，冷酷触发就能维持垄断定价。"
        "<bookmark mark='c'/>一期惩罚需要{T['1']:.2f}；五期惩罚需要{T['5']:.2f}，几乎就是冷酷触发的阈值。<bookmark mark='d'/>不那么雄心勃勃的合谋需要的耐心"
        "更少：合谋价格越低，降价的诱惑越小。",

    'f"How low can the threshold go?':
        "阈值能低到什么程度？<bookmark mark='a'/>任何惩罚都不能把一家公司压到它的最小最大利润以下：即对手能强加给它的最低利润。<bookmark mark='b'/>所以没有"
        "任何机制能在这个阈值以下维持合谋，而迪利普·阿布鲁的最优惩罚规则，先给一根短促的大棒再给胡萝卜，可以逼近它。<bookmark mark='c'/>在第6章的网格上，"
        "最小最大利润是{mm:.3f}，界是{ab:.2f}，而冷酷触发是{gr:.2f}。处在零点九五的学习者远高于两者。",

    'f"The check, against the learners.':
        "检验，对照学习者。<bookmark mark='a'/>在阈值右边，垄断定价可以被维持。<bookmark mark='b'/>学习者一开始并没有在那里找到它：折现因子为一半时，已经"
        "高于阈值，它们的指数只有{d5['delta']:.2f}。只有在delta达到零点九及以上时，它们才走完大部分路程。<bookmark mark='c'/>所以定理是正确的必要条件，"
        "而学习需要的耐心远多于均衡所需。一个可能的原因：学习者在探索时，对手的惩罚很难与噪声区分，所以它必须值得很多，才能被学会。",

    'f"And the learned punishments.':
        "以及学到的惩罚。<bookmark mark='a'/>第6章的冲击响应：一次深度降价，然后在大约{r['back']}期内回归。<bookmark mark='b'/>由推论，对任何高于"
        "{T['5']:.2f}的delta，五期惩罚都能阻止偏离，远低于学习者的零点九五。<bookmark mark='c'/>所以它们不必发现冷酷触发。任何足够长的惩罚都行，而会宽恕"
        "的惩罚可以避免永无休止的价格战。",

    "Why learners find collusion at all.":
        "学习者为什么会找到合谋。<bookmark mark='a'/>不是通过对均衡进行推理。Q学习者对一个价格价值的估计取决于对手在做什么，所以两个学习者的误差一起变动。"
        "<bookmark mark='b'/>马蒂诺·班基奥和贾科莫·曼特加扎称之为自发耦合，并证明它即使没有记忆或耐心也能维持高价。<bookmark mark='c'/>萨拉·菲什、"
        "亚奈·贡恰罗夫斯基和兰·肖雷尔报告，基于语言模型的定价智能体在这类博弈中也会达到高价。",

    "Where the theory goes.":
        "理论走向何方。<bookmark mark='a'/>德鲁·富登伯格和埃里克·马斯金的无名氏定理：只要足够有耐心，几乎任何好于惩罚的结果都可以是均衡，这就是为什么"
        "定理是必要条件，却很少说明学习者会到达哪一个。<bookmark mark='b'/>爱德华·格林和罗伯特·波特：当对手的价格只能透过噪声看到时，合谋需要偶尔的价格"
        "战，正如第6章的嘈杂利润所暗示的。<bookmark mark='c'/>以及扎克·布朗和亚历山大·麦凯：比对手更新更快的算法，即使没有合谋也会抬高价格，因为它起到"
        "了承诺的作用。",

    "Three open problems. <bookmark mark='a'/> A theory of learning:":
        "三个开放问题。<bookmark mark='a'/>一个学习理论：学习者会到达哪些均衡，多快，以及这如何取决于探索和记忆。<bookmark mark='b'/>检测：不看算法，"
        "就能在市场数据中区分学来的合谋与竞争的检验。<bookmark mark='c'/>以及设计：让学来的合谋无利可图的市场规则。",

    "Pause and predict. With a discount factor of zero,":
        "暂停并预测。折现因子为零时，定理不允许任何合谋，然而短视的学习者最终却高于纳什利润。给出两个原因。",

    # ------------------------------------------------------------------ Outro
    "Part forty-two in thirteen lines.":
        "用十三行概括第42部分。圣塔菲市场显示适应性智能体会自发产生泡沫和波动率聚集。在规则之间跟风切换产生肥尾和缓慢的波动率记忆。柯曼的人群有一条精确"
        "的定律。模拟器吻合事实比吻合响应容易。会学习的做市商无论在哪里训练，都不如最好的简单规则。回放的回测不是实盘的市场。",

    "Language models need a clean test":
        "在任何人能说语言模型交易得好不好之前，它们需要一个干净的检验。学习算法不用交流就会合谋，越有耐心越多，噪声越大越少。共享模型主导了使用它的人群"
        "的订单流。监管者担心相关性和集中度。研究者章节证明了合谋何时能够持续。以及本系列公司的规则：在智能体会创造的市场里检验每一个智能体。",

    "Three lessons. <bookmark mark='a'/> The market is its agents:":
        "三条教训。<bookmark mark='a'/>市场就是它的智能体：它的统计规律、流动性和崩盘，是交易者们共同所为。<bookmark mark='b'/>学习会找到一切能赚钱的"
        "东西，包括合谋和模拟器的缺陷。<bookmark mark='c'/>多样性就是稳定：不同的智能体吸收冲击，而副本放大冲击。",

    "The part on one card. The fundamentalist and chartist market.":
        "一张卡片上的这一部分。基本面交易者与图表交易者的市场。柯曼的精确定律。Q学习的更新。合谋的阈值，冷酷的和有限的。以及人群订单流的共同份额。",

    "How this part connects. <bookmark mark='a'/> Backwards: volatility models,":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>向后：波动率模型、Q学习、试验计数器、前视偏差、第35到38部分的做市商，以及第41部分的羊群效应。"
        "<bookmark mark='b'/>横向：合谋是带记忆的价差竞争，单一化是由模型构成的共同持仓。<bookmark mark='c'/>向前：第43部分追问，在由这样的智能体组成的"
        "市场里，是否有人能战胜市场。",

    "Six desk questions. The hook's: is it collusion?":
        "六个交易台问题。开场的那个：这算合谋吗？在经济学上，如果被迫的降价受到惩罚、然后被宽恕，就算；在法律上，是一个悬而未决的问题。"
        "<bookmark mark='a'/>为什么回测不是环境？因为你的报价改变了谁和你交易。<bookmark mark='b'/>在模拟器里训练的智能体要检查什么？响应，以及它从未见过"
        "的状态。",

    "How does herding cluster volatility?":
        "羊群效应如何让波动率聚集？通过一个缓慢变化的趋势追随者份额。<bookmark mark='a'/>共享模型为什么重要？它的部分相干地叠加。<bookmark mark='b'/>"
        "冷酷触发何时能维持垄断价格？高于研究者章节证明的阈值时。完整解答在讲义里。",

    'f"The research chapter\'s pause, answered.':
        "研究者章节的暂停问题，答案来了。<bookmark mark='a'/>第一，网格。在十五个价格上，一次性博弈有它自己的均衡，合谋指数分别为{ne[0]['delta']:.2f}和"
        "{hi_ne:.2f}，所以短视的学习者可以停在连续纳什价格之上。<bookmark mark='b'/>第二，学习本身：{100 * my['above_grid_ne']:.0f}%的短视场次最终甚至"
        "高于较高的那个网格均衡，因为探索把两个学习者的估计耦合在一起，正如班基奥和曼特加扎所证明的。",

    "And twelve problems: why size is predictable":
        "以及十二道习题：为什么收益不可预测而其大小可预测；柯曼的alpha；它的细致平衡；面对有弹性的噪声交易者时的最优价差；回放偏差；logit纳什价格；合谋"
        "阈值；共同份额；共享模型的错误；以及网格上的合谋。然后是两道资格考试题：单次偏离原则及其推论，以及完整的柯曼定律。中英文解答都在讲义里。",

    "Where this comes back. Part forty-three, the last,":
        "这些内容会在哪里再次出现。最后的第43部分追问，在由这样的智能体组成的市场里，是否有人能战胜市场，以及罗闻全为什么称市场是适应性的。",

    "The textbooks this part follows, and the papers it draws on, from Friedman's":
        "这一部分依循的教科书，以及它引用的论文，从弗里德曼的超博弈到监管机构的报告。屏幕上的每个数字都来自本系列公司随机种子固定的模拟器，或来自肯尼斯·"
        "弗伦奇截至二〇二〇年的日收益。",

    "The House now tests its agents against the market they would create.":
        "本系列公司现在在智能体会创造的市场里检验它们。<bookmark mark='a'/>下一部分，也是最后一部分，第43部分：你能战胜市场吗？夏普的算术，运气对技能，"
        "以及完全打开的本系列公司业绩记录。",

}
