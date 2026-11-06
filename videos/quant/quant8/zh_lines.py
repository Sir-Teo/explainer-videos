"""Chinese narration for quant8: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第8部分：决策与控制'

CHAPTERS = {
    'Hook': '该下多大的注，以及我们如何走到这里',
    'Utility': '1. 效用与风险厌恶',
    'Bellman': '2. 贝尔曼原理：倒着求解',
    'HJB': '3. HJB方程与验证定理',
    'Viscosity': '4. 价值函数有折点时：黏性解',
    'Merton': '5. 默顿问题',
    'Consumption': '6. 消费与鞅方法',
    'Costs': '7. 交易成本：不交易楔形',
    'Kelly': '8. 凯利与布雷曼',
    'LTCM': '9. 分数凯利、估计风险与LTCM',
    'Samuelson': '10. 萨缪尔森的反驳与遍历性',
    'Stopping': '11. 最优停止：斯内尔包络',
    'SmoothFit': '12. 自由边界：光滑粘合与美式看跌期权',
    'Behaviour': '13. 人们如何决策：前景理论与模糊性',
    'BSDE': '14. 倒向随机微分方程',
    'MFG': '15. 平均场博弈：一起卖出的人群',
    'RL': '16. 默顿问题上的强化学习',
    'Industry': '17. 谁以定仓位为生',
    'Frontier': '18. 前沿，2023到2026年',
    'Research': '写给研究者：默顿规则中的估计风险',
    'House': '19. 仓位模块',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    'Part eight. Decisions and control.':
        '第8部分。决策与控制。第7部分预测了市场会动多大。本部分问每个交易员接下来都要面对的问题：根据你的判断，该下多大的注？',
    'Here is a game. You get twenty-five dollars and a coin that lands heads sixty pe':
        "你得到二十五美元，一枚正面概率六成的硬币。半小时里可以任意金额押任意一面，赔率一赔一，次数不限，最终可领取的现金最多二百五十美元。每次押多少？<bookmark mark='a'/>2016年哈加尼与杜威把这个游戏交给六十一位受过金融和经济学训练的人，大约三成输光全部本金。",
    'Let the game play itself first. Each column has a hundred and sixty players. Ind':
        "先看模拟。每列一百六十名玩家，独立的硬币序列在四种比例之间配对：百分之十、二十、四十或一百。模拟三百次，财富上限二百五十美元，低于一美分便吸收停止。<bookmark mark='a'/>暂停预测：四十和一百，哪列最常触及破产阈值？去掉上限，四十还会增长吗？<bookmark mark='b'/>三百次，用对数刻度。",
    'f"All in: {100 * b[\'1.0\'][\'p_bust\']:.0f} percent went bust, because one tail tak':
        "全押时{100 * b['1.0']['p_bust']:.0f}%破产，一次反面就拿走全部。押四成时，无上限的期望对数增长略为负；但{100 * b['0.4']['p_cap']:.0f}%达到吸收上限，{100 * b['0.4']['p_bust']:.0f}%触及下限。押两成时{100 * b['0.2']['p_cap']:.0f}%达到上限，本次样本无人触及下限。比例小于一时，有限次抛掷不会让正财富恰好变成零。",
    'f"The log-growth answer is older than the game. At a fixed fraction f, uncapped ':
        "对数增长的答案比游戏古老。固定比例f，无上限每次增长是p乘log一加f，加q乘log一减f。<bookmark mark='a'/>峰值在p减q，也就是百分之二十：1956年的凯利准则。四成时，精确期望对数增长已是每次负百分之零点二四五。第二个零点接近但低于两倍凯利。有上限、有限期限的目标则不同。<bookmark mark='b'/>每种比例模拟两万人，押两成时{100 * k20['p_cap']:.0f}%达到上限，无人触及一美分阈值；全押时{100 * k100['p_bust']:.0f}%破产。这些是样本频率。",
    'How we got here. Daniel Bernoulli':
        "我们是怎么走到这里的。1738年，丹尼尔·伯努利提出对数效用；1944年，冯·诺伊曼和摩根斯坦用公理建立期望效用；1956年，约翰·凯利找到增长准则；1957年，理查德·贝尔曼给出每个多阶段决策背后的递推。<bookmark mark='a'/>1969年，罗伯特·默顿解决了投资者的问题；1979年，保罗·萨缪尔森抨击凯利，卡尼曼和特沃斯基展示人们真实的选择方式。1983年，克兰德尔和利翁斯让贝尔曼方程变得严格；1990年，戴维斯和诺曼解决了交易成本问题，帕尔杜和彭实戈提出倒向随机方程。<bookmark mark='b'/>然后是2006年有连续统参与者的博弈，以及2017年我们要检验的学习算法。<bookmark mark='c'/>这是一棵树，根是期望效用：押多少、如何随时间决策、如何面对人群、人们实际怎样决策，以及机器如何学会答案。",
    'The plan. Utility and the price of risk.':
        '本部分的安排。效用与风险的价格。贝尔曼递推、HJB方程及其背后的理论。带消费和交易成本的默顿问题。凯利，证明与批评。何时停止，以及人们实际如何决策。倒向方程、人群和一台学习机器。以及基金在实践中如何给赌注定大小。',
    'In the House, this part builds the sizing module':
        "在我们的公司里，本部分搭建仓位模块：效用、默顿和凯利比例，以及背后的求解器。<bookmark mark='a'/>从第10部分的期权到第30部分的组合，公司的每一个头寸都将由它来定大小。",
    'Chapter one. Utility, and risk aversion.':
        '第1章。效用与风险厌恶。',
    'In 1738 Daniel Bernoulli looked at a game':
        "1738年，丹尼尔·伯努利研究了一个期望收益无穷大的游戏：奖池一直翻倍，直到硬币正面朝上；可没有人愿意花很多钱去玩。他的回答是：用效用来衡量金钱，也就是财富的对数。<bookmark mark='a'/>1944年，冯·诺伊曼和摩根斯坦把它变成定理。如果你对赌博的偏好满足完备性、传递性、连续性和独立性，也就是把两个赌博和同一个第三者混合，永远不会颠倒它们的顺序，<bookmark mark='b'/>那么你偏好A胜过B，恰好当A的期望效用更大。这里是有限彩票的标准表示；无界结果还需要额外正则性和可积条件。",
    'f"Take a coin flip that leaves you':
        "考虑一次抛硬币，让你从一百变成五十或一百五十，效用取对数。<bookmark mark='a'/>把两个结果当作等重的砝码挂在曲线上。它们的平衡点在弦的中点，高度就是期望效用；因为曲线是弯的，弦落在曲线下方。<bookmark mark='b'/>向左滑动直到碰到曲线：那份确定的财富与这场赌博价值相同，这就是确定性等价，{ce:.1f}。差额{100 - ce:.1f}就是风险溢价，曲线的弯曲就是风险厌恶。",
    'f"Economists usually give the curve one dial:':
        "经济学家用幂效用调节曲率：财富的一减伽马次方除以一减伽马；伽马等于一取对数极限。同一比例赌博的偏好不随财富改变。把两个结果归一化为零和一，弦不动，曲线弯曲。<bookmark mark='a'/>伽马增加，确定性等价左移：三时{ces[i3]:.1f}，三十时{ces[-1]:.1f}，接近最坏结果。<bookmark mark='b'/>风险厌恶对应正伽马；经验估计强烈依赖场景和模型。",
    'What is the bend worth in money?':
        "这种弯曲值多少钱？普拉特在1964年、阿罗在1965年给出答案：定义溢价pi，使一场公平赌博与确定损失pi一样糟。<bookmark mark='a'/>把左边展开到二阶；均值为零，剩下二分之一方差乘以u的二阶导数。<bookmark mark='b'/>把右边展开到一阶。<bookmark mark='c'/>令两者相等：溢价等于二分之一方差乘以绝对风险厌恶。<bookmark mark='d'/>除以财富，相对风险厌恶出现了：对幂效用，它恰好就是伽马。这是小额零均值赌博、效用足够光滑且余项受控时的局部近似。金额方差得到金额溢价；收益率方差得到相对财富的溢价。",
    'f"Check it. For a ten-dollar gamble':
        "检验一下。对十美元的赌博，近似几乎精确；对五十美元的赌博，它开始偏离：伽马为一时，{g1['exact']:.1f}对{g1['approx']:.1f}。<bookmark mark='a'/>暂停预测：伽马为三，为了避开五十或一百五十的抛硬币，你愿意付多于还是少于二十？<bookmark mark='b'/>多于：{100 - u['ce_g3']:.1f}。<bookmark mark='c'/>一个警告，来自马修·拉宾2000年的研究：财富效用无法解释拒绝小额有利赌博，除非同时荒谬地拒绝大额赌博。第13章会讨论这个问题。效用为一次决策排序。大多数决策会重复。下一章：怎样随时间做决策——倒着来。",
    "Chapter two. Bellman's principle":
        '第2章。贝尔曼原理：倒着求解问题。',
    "Richard Bellman's principle of optimality says that an optimal plan remains opti":
        "贝尔曼最优性原理说，在模型的信息和可容许性规则下，最优计划在它到达的状态仍最优。从终端效用倒推。<bookmark mark='a'/>每个节点选择可行股票比例，最大化下一期期望价值。<bookmark mark='b'/>这里各期收益独立、机会集相同，效用为CRRA，总财富为正，比例约束不依赖财富。猜测价值为财富的幂乘时间系数。<bookmark mark='c'/>财富从一期最大化中分离。<bookmark mark='d'/>这些条件下最优比例不依赖财富和期限。随机投资机会可能引入对冲需求，单靠CRRA不能证明短视性。",
    'f"Lab one: the House\'s solver. It takes':
        "实验一：我们公司的求解器。它用默顿的市场：股票期望收益百分之八、波动率百分之十八，债券百分之二，投资者伽马为三，期限十年。期望用十五个高斯-埃尔米特节点计算。它每次倒退一个月；在网格上每个财富水平尝试一百五十一个比例，通过确定性等价插值下个月的价值，保留最好的。<bookmark mark='a'/>运行。没有下限时，它在整个网格上选择{100 * p0.min():.0f}%到{100 * p0.max():.0f}%：默顿的{100 * sw['pi_merton']:.1f}%，误差在网格步长之内，处处如此。一个笨拙的搜索找到了公式。",
    'f"Now add a floor:':
        "现在加上下限：投资者十年后必须至少保住每一美元起始财富中的六十美分。曲面是求解器在每个财富和日期的决策，按计算的方式搭建：从第十年倒着，一片一片。<bookmark mark='a'/>小图是这一片在财富为一时的选择：下一期的期望价值对比例，一个驼峰，峰顶就是决策。它从临近截止时的{100 * f['best_at_1'][last]:.0f}%走到今天的{100 * f['best_at_1'][0]:.0f}%。<bookmark mark='b'/>淡色平面是没有下限的默顿；有了下限，决策在靠近下限时降向零，越接近截止日降得越陡。",
    'f"Slice it at three dates.':
        "在三个日期切开它。<bookmark mark='a'/>求解器把默顿比例投在缓冲上，也就是超出下限今天成本的那部分财富。暂停预测：临近截止日、刚好在下限之上，比例上升还是下降？<bookmark mark='b'/>下降：缓冲在缩小，赌注也随之缩小。<bookmark mark='c'/>线是闭式解，即投资组合保险；点是从未见过它的求解器。两者最多相差{np.nanmax(np.abs(P - Q)):.3f}。让时间步长缩到零，贝尔曼递推就变成一个方程。下一章：HJB方程。",
    "Chapter five. Merton's problem.":
        '第5章。默顿问题。',
    'f"The last two chapters found Merton\'s answer two ways:':
        "前两章用两种方法找到了默顿的答案：持有固定比例，即超额收益除以伽马乘以方差，在我们的市场里是{100 * pi:.1f}%。固定在实践中意味着什么？<bookmark mark='a'/>暂停预测：股票刚跌了百分之二十。默顿买还是卖？<bookmark mark='b'/>看一个模拟市场五年里的两个杯子，上层是股票，下层是债券。股票上涨时，股票层膨胀，默顿卖出把它倒回线上。下跌时，他买入。他在下跌后买入：算术上的逆向投资者，而不是观点上的。第二个杯子买入持有，组合随市场漂移到任何地方，它的风险是运气造成的。",
    "f'Over {rb['n']:,} simulated thirty-year markets":
        "在{rb['n']:,}个模拟的三十年市场中，对伽马为三的投资者，再平衡胜出，以确定性等价计每年高出{100 * (rb['ce_mix'] - rb['ce_bh']):.2f}%，而买入持有最终的股票比例取决于运气。",
    "f'Buy-and-hold comes out ahead over":
        "在{rb['n']:,}条模拟路径的蒙特卡洛估计中，买入持有较高。与连续时间定理比较前，需要评估抽样误差和月度再平衡近似。",
    'With many stocks the derivation is the same':
        "有多只股票时，推导相同，只是比例变成向量，还有协方差矩阵。抛物线变成二次型，顶点是协方差矩阵的逆乘以超额收益，再除以伽马。<bookmark mark='a'/>把它分解。这个向量的方向与伽马完全无关：每个投资者，无论谨慎还是大胆，持有同样的风险资产组合，风险厌恶只决定相对债券持有多少。这就是默顿的共同基金定理，托宾分离定理的连续时间版本；第30部分用数据搭建这只基金。此分离结果使用常系数、正定协方差和无摩擦无约束交易；若归一化为权重和为一，还要求逆协方差乘超额收益向量的分量之和非零。",
    'f"Now put in the American market\'s history:':
        "现在代入美国市场的历史：每年相对国库券的超额收益{100 * m['excess']:.1f}%，波动率{100 * m['sigma']:.1f}%。<bookmark mark='b'/>对数效用的投资者应把{100 * f[0]:.0f}%的财富放在股票上，需要借钱。伽马为三时，{100 * f[2]:.0f}%；伽马为十时，{100 * f[-1]:.0f}%。<bookmark mark='c'/>但超额收益是金融中最不确定的数字。九十四年之后，它的标准误仍有每年{100 * m['se_excess']:.1f}%，正如默顿本人1980年指出的，误差条显示了这对答案的影响：对伽马为三，从{100 * lo[2]:.0f}%到{100 * hi[2]:.0f}%都有可能。方差估得准，均值估不准。公式是精确的，输入却不是。第13章会遇到认真对待这种怀疑的投资者。默顿还问了该花得多快。下一章：消费，以及这个问题的第二种解法。这些比例事后使用全样本历史矩。误差条是独立收益假设下的名义标准误近似，并非前瞻建议，也没有涵盖全部模型风险。",
    "Chapter eight. Kelly, and Breiman's theorem.":
        '第8章。凯利与布雷曼定理。',
    'In 1956 John Kelly of Bell Labs':
        "1956年，贝尔实验室的约翰·凯利问：一个拥有带噪声私人电报线的赌徒该怎样下注？他的回答：最大化财富对数的期望。<bookmark mark='a'/>1960年，克劳德·香农在麻省理工把这篇论文给了爱德华·索普，索普把它用于二十一点，并从1969年11月起用于给一个投资合伙企业定仓位。据索普2006年本人的叙述，到1998年5月，它以每年约百分之二十的速度复利增长，标准差约百分之六，与市场几乎不相关。",
    'For the coin, set the growth derivative to zero: the Kelly fraction is p minus q':
        "硬币上，令增长率导数为零，凯利比例是p减q。<bookmark mark='a'/>常系数扩散中连续再平衡，伊藤公式让对数财富漂移成为抛物线。<bookmark mark='b'/>顶点是超额收益除以方差，即伽马为一的默顿；超额增长是夏普平方的一半。<bookmark mark='c'/>固定硬币比例、对数收益独立同分布且可积时，强大数律使对数财富除以n趋于g。<bookmark mark='d'/>对不同且增长严格较低的固定比例，财富比指数发散。相同策略立刻反驳对所有策略的笼统说法。布雷曼更一般的结果另有策略和市场条件。",
    'f"Watch it: half Kelly, Kelly and twice Kelly':
        "看吧：半凯利、凯利和两倍凯利，在同样的模拟市场中运行四十年，用对数刻度。<bookmark mark='a'/>暂停预测：两倍凯利的增长率中位数是多少？<bookmark mark='b'/>两倍凯利最好的路径冲到所有人之上，这正是诱惑所在，但它的中位数几乎没有离开地面。<bookmark mark='c'/>把时间平均线叠在扇形上：每条中位数都沿着自己的线走，两倍凯利的增长率就是现金利率，{100 * L['r']:.0f}%：承担全部风险，什么也没得到。",
    'f"How long is eventually? Run Kelly':
        "“最终”有多长？在一万个市场里让凯利与半凯利和两倍凯利比一百年，数一数凯利领先的市场。<bookmark mark='a'/>对两倍凯利，十年后它在{100 * vd[9]:.0f}%的市场领先，一百年后{100 * vd[99]:.0f}%。对半凯利，十年后只有{100 * vh[9]:.0f}%，一百年后{100 * vh[99]:.0f}%。白线是闭式解，来自对数财富的正态分布。布雷曼定理是对的，也是慢的：半凯利让出的增长太少，要一辈子才会落后。",
    'f"And Kelly\'s parabola from history:':
        "再看历史中的凯利抛物线：从1926到2020年，每月再平衡到美国市场的固定比例，以国库券利率借钱。<bookmark mark='a'/>全仓每年增长{100 * k['growth_at_1']:.1f}%；峰值在{100 * k['best']:.0f}%，增长{100 * k['growth_at_best']:.1f}%。<bookmark mark='b'/>在{100 * k['ruin_leverage']:.0f}%时，仅1931年9月一个月就会让你归零。峰值是事后找到的；接下来看看必须猜测它时会发生什么。",
    "Chapter ten. Samuelson's objection, and ergodicity.":
        '第10章。萨缪尔森的反驳与遍历性。',
    'f"Kelly\'s admirers argued that every long-horizon investor should maximize growt':
        "有人主张长期投资者都该最大化增长，萨缪尔森在1979年反驳。<bookmark mark='a'/>本扩散模型中比较固定比例：凯利{100 * s['f_kelly']:.0f}%，伽马三的默顿{100 * s['f_merton']:.0f}%。十年后凯利在{100 * p[list(T).index(10)]:.0f}%的市场更富，一百年后{100 * p[list(T).index(100)]:.0f}%。<bookmark mark='b'/>但对该投资者，凯利的年度确定性等价对数率为{100 * s['ce_rate_kelly']:.1f}%，默顿则是正的{100 * s['ce_rate_merton']:.1f}%。这是对数率，不是财富的算术百分比变化。更常领先不等于最大化该投资者的期望效用。",
    'The algebra behind the objection takes four lines.':
        "这个反驳背后的代数只需四行。固定比例时，对数财富服从正态分布，均值和方差都与时间成正比。<bookmark mark='a'/>幂效用的确定性等价是财富的一减伽马次幂的期望再还原回去；正态矩母函数精确地算出它。<bookmark mark='b'/>它的增长率完全与期限无关：现金利率，加上f乘以超额收益，减去伽马的一半乘以f平方乘以sigma平方。<bookmark mark='c'/>这条抛物线在每个期限都在该伽马的默顿比例处达到峰值。长期限不会把任何人变成凯利投资者，除非伽马等于一；凯利几乎确定的领先，是用少见的亏损换来的，而谨慎的投资者对这些亏损的看重超过所有的小额收益。",
    'f"A modern form: heads, wealth rises':
        "现代例子：正面财富增五成，反面减四成，平均收益每次百分之五。十万玩家模拟。<bookmark mark='a'/>少数幸运者推高平均，典型路径却因一正一反乘零点九而缩小；六十次后{100 * e['share_below_1']:.0f}%亏钱。<bookmark mark='b'/>Peters讨论总体平均财富与长期平均对数收益的差异；后者才是增长率，并非财富的时间平均。Meder等2021年研究乘法赌博中的风险选择，Toda在2023年批评其解释。<bookmark mark='c'/>暂停预测：若目标为对数增长，应押多少？<bookmark mark='d'/>凯利取{100 * L['kelly_stake']:.0f}%，每次增长约{100 * L['kelly_growth']:.1f}%。原来典型路径亏损的全押游戏，部分押注可有正对数增长。下一章讨论何时停止。",
    'Chapter nine. Fractional Kelly, estimation risk':
        '第9章。分数凯利、估计风险与长期资本管理公司。',
    'f"Practitioners rarely bet full Kelly.':
        "实务中常用分数凯利。常系数、连续再平衡GBM中，把比例取为c倍凯利。<bookmark mark='a'/>超额对数增长是最优增长的二c减c平方倍；半凯利保留四分之三增长和一半波动，两倍凯利的超额增长为零。这不是任意资产的精确规律。<bookmark mark='b'/>若只把均值优势高估k倍、方差已知正确，实际押注为真实凯利的ck倍；全凯利在k等于二时超额对数增长归零，半凯利在四时归零。<bookmark mark='c'/>本特1994年讨论了高估优势的危险，其赛马团队采用保守的分数凯利。",
    'f"On real data: resample US history':
        "用真实数据：把美国历史按一年为块重抽样四百次，找出每次的最优比例。百分之九十落在{100 * k['bs_p05']:.0f}%到{100 * k['bs_p95']:.0f}%之间。<bookmark mark='a'/>按每个估计押全凯利，再用真实历史打分：很多落在陡峭的一侧，标为红色。每个估计的一半则留在平坦的顶部。<bookmark mark='b'/>一般地，全凯利的超额增长在k等于二时归零，半凯利在四时归零，模拟路径与此一致。暂停预测：你估计夏普比率为一，真实值是一半。哪个增长更快？<bookmark mark='c'/>半凯利，它恰好是真实值上的凯利。<bookmark mark='d'/>历史也可以很仁慈：我们公司登记过的检验在1926到1972年选出{100 * k['split_f1']:.0f}%，之后它每年增长{100 * k['split_g2_at_f1']:.1f}%。",
    'The crisis file. Long-Term Capital Management was founded':
        '危机档案。长期资本管理公司由债券交易员约翰·梅里韦瑟于1994年2月创立；1997年共同获得诺贝尔奖的罗伯特·默顿和迈伦·斯科尔斯都是合伙人。它买入便宜的债券、卖出相近的昂贵债券，赌它们之间的利差会收窄：小而稳定的利润，加了很多倍杠杆。1997年底，它以四十七亿美元资本持有一千二百九十亿美元的资产负债表资产，二十八比一，衍生品名义价值一万三千亿美元。1998年8月俄罗斯违约，投资者涌向安全资产，利差扩大而不是收窄：仅那一个月基金就损失了百分之四十四的价值。9月23日，纽约联邦储备银行召集的十四家银行和券商注资三十六亿美元，拿走了基金百分之九十的份额。',
    'f"Why so dangerous?':
        "为什么这么危险？这是一个示例，不是该基金的账目：一笔年收益百分之一、波动率百分之一的交易，凯利杠杆是{l_['kelly_before']:.0f}，所以二十八比一看起来很谨慎。<bookmark mark='a'/>但凯利杠杆随波动率的平方下降。波动率达到平静时的{cross:.1f}倍时，二十八就是全凯利；达到三倍时，它是凯利的{28 / l_['kelly_after']:.1f}倍，越过了增长为零的那条线。<bookmark mark='b'/>仓位大小只和波动率预测一样好。凯利有一位著名的批评者。下一章：萨缪尔森的反对意见。LTCM的资产权益杠杆与单笔交易凯利比例不是同一风险指标。这里假定超额漂移固定；流动性和尾部依赖不能简化为波动旋钮。",
    'Chapter eleven. Optimal stopping, and the Snell envelope.':
        '第11章。最优停止与斯内尔包络。',
    'For the finite-horizon stopping theorem, take an integrable adapted reward, a fi':
        "有限期限停止定理假设奖励适应且可积，截止日期N有限，初始信息平凡。到N强制停止；此前比较立即收益与条件期望继续价值。<bookmark mark='a'/>倒推可证斯内尔的U是支配奖励的最小超鞅。<bookmark mark='b'/>首次U等于g时停，在此前停止后的U为鞅。停止时刻不超过N，可选抽样给出最优期望收益。<bookmark mark='c'/>图中的随机游走则没有固定日期，但状态限于零到二十，吸收端点强制停止。在这些边界和可积条件下，价值是该有限网格上奖励的最小凹优函数。",
    'f"A payoff for every position, a skyline of pegs.':
        "每个位置一个收益，一排高低不一的木桩。暂停预测：价值会碰到哪些木桩？<bookmark mark='a'/>价值迭代：从收益开始，把每个值换成它的木桩和两个邻居平均中较大的那个。曲线升起，像一根被拉紧搭在最高木桩上的绳子，{s['sweeps']}次扫描之后停下。<bookmark mark='b'/>绳子落在木桩上的地方，停止；悬在上方的地方，等待。在位置十，选择时机的权利值{s['U0_mid']:.2f}，而立即停止只得{g[10]:.0f}。",
    'f"Lab three. Two completely different routines':
        "实验三。我们公司里两段完全不同的程序。一段是你刚看到的价值迭代：几行最大值和平均。另一段对随机游走一无所知：它计算木桩的上凸包，也就是绳子真正的形状，然后插值。<bookmark mark='a'/>两段都运行。价值迭代在{s['sweeps']}次扫描后收敛，两个答案相差不到十的负{-int(np.floor(np.log10(s['max_gap'])))}次方。概率和几何给出同一个对象。",
    'f"The secretary problem: a known hundred candidates arrive in uniformly random o':
        "秘书问题：已知有一百名候选人，排名互不相同，以均匀随机顺序到达。每人可与已见者比较，但须当场接受或拒绝，不能召回；选到最好者才成功。<bookmark mark='a'/>最优规则先拒绝固定人数，再选首次创纪录者。一百人时最佳截点为{q['best_k']}，成功率{100 * q['best_p']:.1f}%。人数增大时，最优拒绝比例与成功率都趋于e分之一。这是渐近极限，不是每个有限人数的精确概率。下一章看连续时间行权边界。",
    'Chapter thirteen. How people really decide':
        '第13章。人们如何真正决策：前景理论与模糊性。',
    'Does anyone actually choose by expected utility?':
        "1953年阿莱给出两组选择：确定一百万，或一成概率五百万、八成九一百万、一分为零；常见选择是确定的一百万。另一组是一成一概率一百万，或一成概率五百万；常见选择是后者。<bookmark mark='a'/>C和D来自A和B：把共同的八成九概率一百万都替换为零。期望效用独立性要求两组排序一致，这种选择模式却反转。",
    "Kahneman and Tversky's prospect theory, 1979":
        "1979年的前景理论和1992年的累积版本改变三件事。<bookmark mark='a'/>从参照点衡量价值，收益凹、损失凸；示例损失系数为二点二五，是特定拟合参数，并非普适常数。<bookmark mark='b'/>权重作用于从尾部排序的累积概率。<bookmark mark='c'/>相关模型研究持有亏损、卖出盈利和彩票型收益需求，但这本身不证明市场因果。",
    'f"Benartzi and Thaler proposed in 1995':
        "贝纳茨和塞勒在1995年提出，股票被冷落是因为人们查看得太频繁。暂停预测：如果每五年而不是每个月看一次，损失厌恶的投资者会持有更多股票，还是更少？<bookmark mark='a'/>我们公司登记过的检验，用九十四年的美国收益。一个月的尺度上，一半的收益落在曲线陡峭的损失一侧；两年的尺度上，分布滑向收益一侧。<bookmark mark='b'/>每h个月给股票和国库券打分：短期内国库券胜出，两条曲线在{cross}个月处相交。贝纳茨和塞勒发现大约一年，对比的是债券。<bookmark mark='c'/>所以答案是更多。你多久看一次，本身就是一个决策。这里仅比较纯股票与国库券，不是最优混合配置，也没有计算五年期限。",
    'Second, people dislike unknown odds':
        "第二，人们讨厌未知的赔率，这与风险无关：埃尔斯伯格1961年的坛子，以及吉尔博阿和施迈德勒1989年的理论：选择最坏可信模型下最好的行动。<bookmark mark='a'/>帕斯卡尔·梅恩豪特在2004年把它用于默顿问题，承接汉森和萨金特：自然可以压低股票的漂移，但要付出熵的代价。<bookmark mark='b'/>内层最小化是一条抛物线。<bookmark mark='c'/>在Maenhout的缩放下，你押得越多，最坏情形越悲观。<bookmark mark='d'/>结果是伽马换成伽马加theta的默顿：怀疑的作用就像额外的风险厌恶。伽马加theta的结果使用这里特定的齐次熵惩罚。此处theta是模糊厌恶，不是其他章节的夏普符号。",
    'f"The game on US numbers, gamma three:':
        "用美国的数据玩这场博弈，伽马为三：红色是自然对每个仓位的最坏漂移；蓝色是投资者对每个漂移的默顿回应。<bookmark mark='a'/>它们交于{100 * row['pi']:.0f}%，没有怀疑时是{100 * rf['pi_plain']:.0f}%。<bookmark mark='b'/>该有多少怀疑？只有数据无法排除的那么多：选择theta，使得用九十四年的数据，最坏模型有百分之二十的时间会被误认为估计值。此时theta是{th:.1f}。下一章：鲁棒偏好和美式看跌期权共同背后的方程——倒向随机微分方程。识别误差取已知波动率、常数漂移、等先验正态似然检验：Phi负的漂移差绝对值乘年数平方根，再除以两倍sigma。百分之二十是选定校准值，不是数据确立的可信边界。",
    'Chapter eighteen. The frontier, 2023 to 2026.':
        '第18章。前沿，2023到2026年。',
    'The chapters of this part form a graph,':
        "本部分的各章构成一张图，当前的研究就在它的边上。<bookmark mark='a'/>在学习和HJB方程之间：Yanwei Jia和周迅宇2023年发表在《机器学习研究杂志》上的论文，弄清了时间连续时Q学习意味着什么。",
    'Min Dai, Yuchao Dong, Jia and Zhou showed':
        '戴民、董宇超、Yanwei Jia和周迅宇证明，默顿问题最优随机化策略的均值就是默顿比例，所以行动者-评论家学习者可以直接从数据中找到它，而无需估计期望收益，也就是第5章所说的金融中最不确定的数字。不显式估计漂移不等于没有统计不确定性；结论依赖该随机化控制模型与目标。',
    'In a 2026 paper the same group finds':
        '在2026年的一篇论文中，同一团队针对递归版本的问题，找到了一个不依赖财富的闭式高斯策略，它的分散程度随风险厌恶和波动率上升而缩小：探索被计入了目标函数。',
    'Between dynamic programming and deep learning:':
        '在动态规划与深度学习之间：Jeonggyu Huh、Jaegi Jeon、Hyeng Keun Koo和Byung Hwa Lim用庞特里亚金极大值原理引导神经网络，求出一百个资产的约束组合最优解，远超网格所能处理的范围。',
    "Huh and Koo's 2026 follow-up studies parameter uncertainty and reports that its ":
        'Huh与Koo在2026年研究参数不确定性，报告其模型和训练协议下，无模型PPO基线仍远离目标。这是特定基准结果，不是强化学习的普适极限。',
    'For crowds, a survey by Mathieu':
        '关于人群，Mathieu Laurière等人的综述梳理了智能体如何在没有模型的情况下学习平均场均衡，就像我们的阻尼最佳响应迭代在有模型时所做的那样。',
    'Daniel Chee, Noufel Frikha and Libo Li':
        'Daniel Chee、Noufel Frikha和Libo Li在2026年一篇关于美式期权的论文中，把停止、探索和反射倒向方程结合在一起，并给出收敛速度。',
    'And on the Kelly branch, Alexis':
        '凯利分支上，Toda在2023年批评遍历性经济学。图中许多连接把学习方法与HJB、边界或固定点结合。这些论文的模型假设和数值设定不同，来源列在笔记。接下来把公司的仓位模块组合起来。',
    'Chapter nineteen. The sizing module.':
        '第19章。仓位模块。',
    "The House's sizing module collects this part's tools, every one tested against a closed form or a second method, because":
        "我们公司的仓位模块汇集了本部分的工具，每一个都用闭式解或第二种方法检验过，因为一条错误的定仓位规则会同时错在每一个头寸上。<bookmark mark='a'/>效用与确定性等价。用动态规划和HJB方程的有限差分求默顿。黏性解那一章的格式比较。消费与不交易区间。凯利与实现增长。三种方式求停止：价值迭代、凸包和光滑粘合。前景理论与稳健比例。倒向方程与人群。还有学习者，它们必须先与答案一致，才会被托付更难的事情。一切都能用一条命令重建，观众可以改动任何输入再运行一遍。",
    'f"Here is how the House sizes a position,':
        "这是公司的示例治理流程，组合分别推导的规则，并非联合最优控制解。美国历史估计的凯利比例为{100 * kel:.0f}%。<bookmark mark='a'/>默认先取一半，{50 * kel:.0f}%；按百分之二十识别误差约定校准的稳健比例为{100 * rob_kelly:.0f}%，取两者较小值。<bookmark mark='b'/>区间外才调仓，使用名义回撤缓冲，并随波动预测更新。预测更新不能阻止突然跳跃，这些步骤不保证回撤下限。<bookmark mark='c'/>这是示例规则九。本部分原有三项登记：样本分割凯利、短视损失厌恶和波动目标，累计{env['trials']}次。",
    'f"Part eight in ten lines. Twenty percent maximizes uncapped log growth for the ':
        "第8部分十句话。六成硬币无上限对数增长在两成比例最大，四成已略负。小额公平金额赌博的风险溢价近似伽马乘金额方差除以两倍财富。贝尔曼和光滑验证需要可容许性，不光滑HJB用黏性比较与满足条件的收敛格式。美国全样本、伽马三的默顿代入比例为{100 * m['fraction'][2]:.0f}%，误差条为名义近似。小成本区间半宽的一阶量级是成本立方根。模型条件下，固定比例凯利最终胜过增长严格较低的比例；期望效用在任何期限都可能偏好较少风险。停止、稳健控制、倒向方程与人群博弈各有条件。PPO检查是带模拟器下限的数值比较。实际仓位结合预测和风险约束，不保证免受跳跃。",
    'Four desk questions.':
        "四道交易台问题。六成的硬币：押百分之二十，每次让财富增长约百分之二；押百分之四十就不再增长。<bookmark mark='a'/>波动率百分之十、夏普比率为一的策略：凯利说十倍杠杆。别这样：四年夏普为一几乎算不上证据，波动率还可能翻三倍。<bookmark mark='b'/>为什么有耐心的投资者会拒绝凯利？因为最大化增长就是最大化期望对数，而这只对一种特定的风险厌恶才是对的。<bookmark mark='c'/>成本为百分之一时，你的股票权重从百分之六十二漂到六十六：什么都不做，你仍在区间之内。完整解答在讲义里。",
    'And nine problems:':
        '还有九道习题：任意赔率下的凯利公式、默顿的价值函数、分数凯利、秘书问题的e分之一、彼得斯硬币该押多少、永续看跌期权的光滑粘合，以及卖出的人群。其中两道是资格考试题：估计出来的优势的确切代价，以及方差也要估计时的修正。中英文解答都在讲义里。',
    'Where this comes back. Optimal stopping prices the American option':
        '这些内容会在哪里再出现。最优停止在第10和16部分为美式期权定价。倒向方程在深度对冲中回归，也在第21部分回归，那里不同利率下的融资正是我们定价过的非线性。凯利和默顿为第30和31部分的组合定仓位。平均场博弈为订单簿和执行建模。强化学习在后面的部分里对冲、执行和交易。第41部分完整讲述LTCM的故事。',
    'The textbook chapters and papers are listed in the notes. Numerical illustration':
        '教材章节和论文列在笔记里。数值示例使用本系列代码、公开French市场收益和固定种子模拟。历史故事和论文结果是带来源的引用，不是从这些数据计算出的结论。',
    'The House can now forecast risk and size its bets.':
        "我们的公司现在能预测风险，也能给赌注定大小了。工具箱就此完成。<bookmark mark='a'/>下一部分，第9部分，衍生品篇的开始：无套利。为什么可复制的收益只有一个价格，资产定价基本定理，以及由第4部分的鞅构建的风险中性测度。",
    'Chapter three. The Hamilton-Jacobi-Bellman':
        '第3章。哈密顿-雅可比-贝尔曼方程与验证定理。',
    "Shrink Bellman's period to an instant. Over":
        "把贝尔曼的一期缩短为瞬间。在长度为h的短区间上，现在的价值等于区间末尾的最佳期望价值：同一个原理。<bookmark mark='a'/>用第5部分的伊藤公式展开未来的价值。它等于今天的价值，加上一个漂移积分，即时间导数加上所选比例下财富的生成元，再加上一个对布朗运动的随机积分。<bookmark mark='b'/>随机积分的均值为零。两边减去今天的价值，再除以h。<bookmark mark='c'/>令h趋于零，被积函数的平均变成它现在的值：零等于时间导数，加上对比例取上确界的项，即财富漂移乘以V x，加上二分之一方差乘以V x x。这就是哈密顿-雅可比-贝尔曼方程，终端条件是效用。<bookmark mark='d'/>上确界里面是关于pi的抛物线。V是凹的时候，顶点就是最大值，一阶条件给出比例。<bookmark mark='e'/>现在猜测解是财富的幂乘以时间的函数。对x的导数变成V的倍数，上确界变成一个数，方程化为f的常微分方程，终点时f等于一。比例正是默顿的：超额收益除以伽马乘以方差。这段形式推导假设价值光滑、动态规划成立，区间内控制为可容许过程。随机积分须局部化并满足可积条件，才能取零期望。",
    'f"Here is the maximum as a picture:':
        "这是最大化的图像：在每个财富水平，括号除以正数一减伽马乘以V，是比例的抛物线，决策就是它的顶点。<bookmark mark='a'/>移动财富。没有下限时，顶点从不移动：处处都是{100 * h['pi_merton']:.0f}%。<bookmark mark='b'/>打开第2章的下限：财富接近它时，抛物线变窄，顶点滑向零。<bookmark mark='c'/>暂停预测：波动率加倍，比例会怎样？<bookmark mark='d'/>降为四分之一，大约{100 * h['pi_merton'] / 4:.0f}%。",
    'We guessed a smooth solution. Verification turns it into a value function under ':
        "猜到光滑解后，需要增长和可积条件才能验证它等于价值。沿任意可容许财富过程应用伊藤公式。<bookmark mark='a'/>HJB使漂移非正。局部化和一致可积性若允许取终端期望，期望效用不超过候选价值。达到上确界且适定、可容许的反馈使漂移为零并达到价值，所以最优。<bookmark mark='b'/>光滑性、随机积分条件、终端极限和可容许性都重要；单独的鞅条件并非排除翻倍策略的通用定理。下一章处理不光滑价值。",
    'f"The equation can also be solved without guessing.':
        "这个方程也可以不靠猜测来解。我们公司的有限差分求解器，{h['n_t']}个时间步乘以{h['n_y']}个财富节点，在每一步交替进行：给定比例解出价值，把比例移到每个顶点，重复。<bookmark mark='a'/>大多数步用了{int(np.argmax(h['pass_counts']))}轮。<bookmark mark='b'/>它的比例与默顿相差{100 * h['pi_err']:.3f}个百分点，价值与闭式解相差{100 * h['rel_err']:.2f}%以内，<bookmark mark='c'/>而且网格加密时误差不断下降。但价值函数并不总是光滑的。下一章：有折角时怎么办。",
    'Chapter four. When the value function has kinks':
        '第4章。价值函数有折点时：黏性解。',
    'The verification theorem needed a smooth value function.':
        "验证定理要求光滑价值。财富下限、停止与等待之间的选择、交叉分支的最大值，都可能造成折点，并非每个最大值都必然不光滑。<bookmark mark='a'/>看最简单例子：区间两端为零，斜率绝对值为一。没有处处光滑解；帐篷除了顶点都满足，带凹口的折线也几乎处处满足，还有无穷多种折线。<bookmark mark='b'/>只要求几乎处处成立无法选出唯一答案，数值格式也可能收敛到错误解。暂停预测，计算机会选哪一个？<bookmark mark='c'/>我们要的是帐篷，即到边界的距离、最快退出问题的价值，需要更合适的解定义。",
    'Crandall and Lions found it in 1983:':
        "克兰德尔和利翁斯在1983年找到了：永远不对u求导。改用光滑的检验函数去接触它，把检验函数的导数代入方程。<bookmark mark='a'/>在峰顶，光滑函数可以从上方以负一到一之间的任何斜率接触，每一个都通过下解检验；从下方没有函数能接触。峰顶通过。<bookmark mark='b'/>在谷底，一条平的抛物线从下方接触，上解检验要求斜率大小减一至少为零。结果是负一：谷底不通过。<bookmark mark='c'/>每个向下的折点都不通过，只有帐篷留下。",
    'The comparison principle, when it holds for the PDE and its boundary conditions,':
        "比较原理在方程及其边界条件满足相应假设时，使下解不超过上解，并给唯一性。连续性、动态规划和边界条件适当时，控制价值是HJB黏性解。<bookmark mark='a'/>Barles与Souganidis证明：极限方程有比较原理、边界处理适当时，单调、稳定、一致的近似格式收敛。单调表示邻点值的更新保序。每个条件都重要；只有一致性并不保证收敛。",
    'f"Test it. March the equation, u t plus':
        "检验一下。把方程u t加上u x的大小等于一，从零开始向前推进，直到稳定。左边是迎风格式，从信息来的那一侧看每个邻点：单调的。右边是教科书上的中心差分：相容，但不单调。<bookmark mark='a'/>迎风格式的剖面像水灌满帐篷一样上升，恰好停在距离函数上。中心差分的剖面在相邻节点之间长出锯齿，锯齿越长越大。<bookmark mark='b'/>在每个网格上，迎风格式的误差都在舍入误差水平。中心差分的误差在最细的网格上达到十的{int(np.log10(grid['321']['central']))}次方：加密反而更糟。<bookmark mark='c'/>相容性不够。单调性才让网格收敛到正确的折点，这也是第2章的求解器，一个正权平均的最大值，找到投资组合保险的原因。工具齐备，来看经典问题。下一章：默顿问题。中心差分图使用固定显示窗口，超出部分省略；误差读数保留完整量级。",
    'Chapter six. Consumption, and the martingale method.':
        '第6章。消费与鞅方法。',
    'f"In 1971 Merton added the other half of a life:':
        "1971年，默顿加入了人生的另一半：消费。投资者以速率c消费，从中获得效用，并以rho贴现未来。在无限期限下，方程不再依赖时间，消费表现为对财富的消耗。<bookmark mark='a'/>c的一阶条件是一条可以说出口的规则：一直消费，直到消费的边际效用等于多存一美元的边际价值。<bookmark mark='b'/>再次猜测幂函数形式。消费与财富成正比，股票比例与之前完全相同：消费和投资分离。<bookmark mark='c'/>代入并匹配财富的幂次，消费率是常数nu。rho为百分之三时，对数效用恰好消费rho；伽马为三时每年消费财富的{100 * nu[2]:.2f}%。<bookmark mark='d'/>有限寿命且不留遗产时，用时间函数做同样的步骤，得到一个在接近终点时上升的消费率。无限期限解要求消费系数为正，并满足横截条件和可容许性；伽马一取对数极限。",
    'f"Over a forty-year life with gamma three':
        "四十年人生、伽马三，初始消费财富率为每年{100 * c['life_t0']:.1f}%。之后先缓慢再陡峭上升；瞬时消费财富率像剩余时间的倒数一样发散。图省略临终前高于每年百分之三十的部分。<bookmark mark='a'/>不同伽马的无限期消费率差异不大：更好市场增加财富，也奖励储蓄，两者相抵。<bookmark mark='b'/>暂停预测：更有耐心、rho百分之一，消费更多还是更少？<bookmark mark='c'/>更少：{100 * c['nu_patient']:.2f}%。",
    "Return to chapter five's terminal-wealth problem. Cox and Huang, and independent":
        "回到第5章的终端财富问题。Cox与Huang，以及独立的Karatzas、Lehoczky和Shreve给出第二种方法。完全市场中的状态价格密度xi结合贴现和测度变换密度。<bookmark mark='a'/>选择可负担、可积并能由可容许策略复制的终端收益，满足状态价格预算，就成为静态优化。若要处理消费，还须把消费流加入预算。<bookmark mark='b'/>拉格朗日乘子让边际效用正比于xi。CRRA终端财富是xi的负伽马分之一次方乘预算常数。<bookmark mark='c'/>在本常系数市场中，它是股票的幂索取权，连续固定比例再平衡能复制这个终端收益。",
    'f"Check it: two thousand investors rebalance daily':
        "检验两千条十年、每日再平衡路径。散点图选取窗口内最多一千二百个点。<bookmark mark='a'/>它们与静态曲线的最大偏差为{100 * m['max_rel']:.2f}%，这是本次每日离散近似的误差。<bookmark mark='b'/>较低伽马使曲线更倾斜：投资者在便宜状态买更多财富。以上均假设交易免费。下一章讨论成本。",
    'Chapter seven. Transaction costs, and the no-trade wedge.':
        '第7章。交易成本与不交易楔形。',
    'f"Merton\'s investor trades every instant':
        "默顿的投资者每时每刻交易以保持固定比例。如果每笔交易要付交易金额的百分之一，那就是灾难：连续再平衡的换手率是无穷大。她该怎么办？<bookmark mark='a'/>把她的财富画成平面上的一个点：横轴是债券的美元数，纵轴是股票的美元数。默顿的规则是一条从原点出发的射线：上面每一点的股票比例都相同。<bookmark mark='b'/>有了成本，射线张开成楔形。楔形内什么都不做。市场把点推到边缘时，只交易刚好够留在边缘上的量，从不回到中间。<bookmark mark='c'/>看一个市场的十五年。点在楔形内自由游走，边缘上的每次闪光是一笔微小的交易。与每周回到射线的投资者比较交易次数。<bookmark mark='d'/>楔形每年交易财富的{100 * w['turn_band']:.1f}%；保持在射线上，{100 * w['turn_ray']:.0f}%。在数学上，这个点是一个在锥面边缘被反射的扩散。路径使用每周交易，带宽来自月度有限期限近似。这是楔形区间示例，不是连续奇异控制最优解的精确模拟。",
    'The mathematics. The controls are no longer rates':
        "数学上，控制变量不再是速率，而是累计买入和卖出，每一美元要付epsilon：一个奇异控制问题。<bookmark mark='a'/>HJB方程变成变分不等式：三项中最大的为零。第一项起作用的地方，价值满足不交易方程；第二项起作用的地方，买入恰好值它的成本；第三项起作用的地方，卖出恰好值它的成本。三个区域：买入、卖出，以及中间的楔形。<bookmark mark='b'/>幂效用再次让财富分离，只剩股票比例。<bookmark mark='c'/>成本很小时，区间半宽按成本的立方根增长：很小的成本就能换来很宽的区间。迈克尔·马吉尔和乔治·康斯坦丁尼德斯在1976年看到了这个区间；马克·戴维斯和安德鲁·诺曼在1990年构造了解；史蒂文·施里夫和梅特·索纳在1994年用第4章的工具，以黏性解证明了它。",
    'f"Lab two: the band by dynamic programming.':
        "实验二，用动态规划求区间。每月从各股票比例选择目标，再按交易比例支付近似成本；最优动作是不动的区域就是区间。<bookmark mark='a'/>百分之一成本下，区间为{100 * rows[2]['lo']:.1f}%至{100 * rows[2]['hi']:.1f}%，半宽{100 * rows[2]['half']:.1f}点；小成本渐近值为{100 * rows[2]['asym']:.1f}点。网格、时间和成本近似都可能影响差异。",
    'f"Pause and predict: if costs double':
        "暂停预测：成本翻倍，区间宽度也翻倍吗？<bookmark mark='a'/>小成本的一阶渐近半宽增加为二的立方根，约四分之一；不是有限成本的精确规律。<bookmark mark='b'/>本次对数效用、成本百分之一、季度模拟中，区间{100 * g1['lo']:.0f}%至{100 * g1['hi']:.0f}%，净增长比每季回到默顿高每年{100 * g1['gain']:.2f}%，换手为{100 * g1['band']['turnover']:.0f}%，对照{100 * g1['merton']['turnover']:.0f}%。下一章讨论凯利增长目标。",
    'Chapter twelve. Free boundaries:':
        '第12章。自由边界：光滑粘合与美式看跌期权。',
    'f"In continuous time the stopping rule becomes a boundary':
        "在连续时间里，停止规则变成空间中的一条边界，没人告诉你它在哪里。看最简单的情形：一个永不到期的美式看跌期权，随时以K卖出股票的权利。持有期间，在某个行权水平b之上，它的价值满足没有时间导数的Black-Scholes方程。<bookmark mark='a'/>试一个S的幂。指数满足一个根为一和负beta的二次方程，只有负根能让股票极高时看跌期权一文不值。<bookmark mark='b'/>价值匹配：在水平b行权，得到K减b，这确定了常数。亨利·麦基恩在1965年解出了它。<bookmark mark='c'/>选哪个水平？让价值最大的那个。对b求导，条件等价于要求价值以收益自身的斜率负一离开收益，没有折角：光滑粘合。利率百分之五、波动率百分之三十时，边界是{p['b_star']:.1f}。",
    'f"Watch the choice. The grey line is the payoff;':
        "看这个选择。灰线是收益，蓝线是股价首次跌到b便行权的价值。<bookmark mark='a'/>b很低时，曲线接触收益的斜率比负一更陡，读数是两条斜率之差。提高b，股价一百时的价值先上升；b太高时斜率过平，价值又下降。<bookmark mark='b'/>最佳边界{bs:.1f}恰好使斜率差为零，价值{p['v100']:.2f}。四十年二叉树的边界为{p['tree_boundary0']:.1f}，价格{p['tree_price']:.2f}。<bookmark mark='c'/>暂停预测：利率上升，边界上升还是下降？<bookmark mark='d'/>上升：beta增大，百分之七利率下边界为{p['b_star_r7']:.1f}。等待收到执行价的利息代价更高，因此更早行权。",
    'f"With an expiry, the boundary rises':
        "有到期日时，边界随时间流逝升向行权价。<bookmark mark='a'/>对一年期看跌期权，选择时机的权利值{a['american'] - a['european']:.2f}。<bookmark mark='b'/>一般地，价值满足变分不等式，是黏性解，也是一个反射倒向方程的值：这是第14章的主题。在那之前，先看一个求解器回答不了的问题：人实际上是怎样做决定的。",
    'Chapter fourteen. Backward stochastic differential equations.':
        '第14章。倒向随机微分方程。',
    'The control problems so far ran forward in time':
        "倒向随机微分方程寻找适应信息的过程Y和Z，并在终点等于给定收益。在具有鞅表示性质的布朗过滤下，终值平方可积，驱动在零处满足时间上的平方可积条件，且驱动对Y、Z一致利普希茨时，帕尔杜与彭实戈1990年的定理给出平方可积适应解的存在唯一性。<bookmark mark='a'/>线性驱动对应Black--Scholes；光滑马尔可夫情形中，Z等于sigma乘S乘delta，并非直接等于股票份数。<bookmark mark='b'/>非线性例子中，借款利率百分之六、存款百分之一，现金账户为负时触发额外融资项。相同终值且满足标量比较定理条件时，更大的驱动给更大的价值。<bookmark mark='c'/>数值上先向前模拟股票，再倒推，用跨路径回归近似条件期望。",
    'f"Here is the scheme running, on a ratio call spread: long one call at ninety-fi':
        "看涨比例价差：买一份执行价九十五的看涨，卖两份一百零五的看涨，期限半年；高股价时收益为负且无下界。先模拟两万条股票路径。<bookmark mark='a'/>再倒推：灰点是下一期价值对本期股价的散点，回归估计条件期望，再作驱动修正。面板只显示股价75到125、价值负12到12；超出部分省略，不压在边缘。<bookmark mark='b'/>暂停预测：价格会落在百分之一与百分之六的Black--Scholes价格之间吗？<bookmark mark='c'/>不会，本次数值为{rp['Y0']:.3f}，高于{rp['bs_r']:.3f}与{rp['bs_R']:.3f}。现金符号决定借存利率，这不是统一利率的线性定价算子。",
    'f"As path counts increase, these estimates approach the PDE reference {b[\'pde\']:':
        "本次固定离散化中，路径数增加后估计接近PDE参照{b['pde']:.3f}。每个规模运行三次，图示正负二倍运行标准差，仅概括离散程度，不是置信区间或收敛证明。<bookmark mark='a'/>六次多项式估计为{b['poly']:.3f}，局部帽函数在这里更接近参照。这个比较不能单独识别误差来源。Han、Jentzen和E在2018年展示高维神经BSDE方法；第17部分会训练一个。下一章看投资者与人群互动。",
    'Chapter fifteen. Mean-field games:':
        '第15章。平均场博弈：一起卖出的人群。',
    'Now many traders face each other.':
        "现在许多交易者彼此相对。在平均场博弈中，每个参与者把人群当作给定，倒着求解一个控制问题，而人群则在所有人的选择推动下向前演化。拉斯里和利翁斯，以及Minyi Huang、Malhamé和Caines，在2006年提出了它。<bookmark mark='a'/>一个有闭式解的例子：N家基金都要在时间T前卖出一大笔股票；卖得快要付溢价，所有人的卖出都会压低价格。<bookmark mark='b'/>一个计划的成本取决于其他人的平均卖出速度。<bookmark mark='c'/>最优回应满足欧拉-拉格朗日方程。<bookmark mark='d'/>一致性，即其他人也这样做，给出一个线性方程。<bookmark mark='e'/>单独一家时，直线卖出；在人群中，抢着卖，赶在别人的卖出压到价格之前。本例为确定性开环、对称清仓博弈，初始库存一、期末强制为零；单独交易为直线还要求库存惩罚为零。本例为确定性对称开环计划，初始库存一、期末为零；单独交易直线清仓要求库存惩罚为零。",
    'How does a crowd find that equilibrium?':
        "这里用阻尼最佳响应迭代。左边是从终点倒推的计划，右边是它产生的人群卖出速度。起初假定人群不动。<bookmark mark='a'/>先求对这个人群的最佳响应，再把新响应与旧计划各混合一半，重复直到计划与人群一致。本例的曲线先超调再靠近灰色均衡。这是阻尼固定点迭代，并非经典的历史平均虚拟博弈算法；展示的是本参数实例的收敛。",
    'f"Lab four: given the crowd\'s rate,':
        "实验四：给定人群的速度，最优回应是一次三对角求解；人群的新速度是它的斜率；混合，重复。<bookmark mark='a'/>残差按几何级数下降，{len(res)}轮后低于十的负{-int(np.floor(np.log10(res[-1])))}次方，与闭式解的差在网格误差之内。在前五分之一的时间里：单独一家卖出{100 * R['1']['share_fifth']:.0f}%，两家{100 * R['2']['share_fifth']:.1f}%，十家{100 * R['10']['share_fifth']:.1f}%，极限下{100 * R['inf']['share_fifth']:.1f}%。",
    'Pause and predict: you know nine other funds':
        "暂停预测：你知道另外九家基金这周在卖同一只股票。你会比单独时卖得更快还是更慢？<bookmark mark='a'/>更快。单独一家，直线；两家，曲线弯曲；十家，更弯；在平均场极限下，这一大笔股票被抢着卖掉。<bookmark mark='b'/>右边是五百家仓位不同的基金，各自回应同一个人群：整个库存分布很早就冲向零，每家基金都在为别人的匆忙买单。<bookmark mark='c'/>这就是拥挤交易的数学。皮埃尔·卡尔达利亚盖和夏尔-阿尔贝·勒阿勒在2018年这样为拥挤交易建模；卡林、洛博和维斯瓦纳坦研究了少数人之间的掠夺性交易；拉克和扎里福普卢证明，相互比较考核的基金会承担更多风险。第36和37部分会回到这里。下一章：机器能只靠经验学会这些规则吗？",
    'Chapter sixteen. Reinforcement learning':
        '第16章。默顿问题上的强化学习。',
    "The learner receives the simulated market and reward, without Merton's analytic ":
        "学习器获得模拟市场与奖励，但没有默顿解析最优值。状态为时间和对数财富，动作为比例，奖励为总财富因子的对数；取对数前先设置百万分之一的下限。<bookmark mark='a'/>可交换微分与期望且可积时，真实的有限期限策略梯度，是每一期动作得分乘真实优势的总和。<bookmark mark='b'/>我们用学习评价器的一步TD误差估计优势，可能有偏。<bookmark mark='c'/>PPO截断代理目标，并不硬性限制每次策略更新或KL散度。",
    'f"Lab five: a thousand and twenty-four ten-year episodes per iteration, three hu':
        "实验五：每轮一千零二十四条十年路径，共三百轮。动作是无界高斯比例，总财富下限为百万分之一。这是数值模拟器，不是杠杆几何布朗运动的可容许性定理。<bookmark mark='a'/>五个种子的最终平均比例为{100 * min(fin):.0f}%至{100 * max(fin):.0f}%，有限求积基准为{100 * ps['discrete']:.0f}%。所示差距最多每年{100 * max(ps['shortfall']):.2f}%，比较的是平均比例处的连续增长公式，不是完整学习策略的季度绩效。",
    'Here is the training, scrubbed checkpoint':
        "逐检查点看训练。右侧是五个种子的平均股票比例及其离散程度，与有限求积基准比较；左侧是同一检查点的时间和财富策略图。<bookmark mark='a'/>它从约百分之五十开始，上升，有些种子超调，最后在基准附近游走。这是本次固定训练协议的结果。策略图趋平，最终比例对时间和财富依赖很弱，符合常系数默顿模型的形状；学习器没有得到解析最优值。",
    'f"Now add trading costs: a one percent cost on every trade. The dynamic program ':
        "现在加入每笔百分之一的交易成本。此数值动态规划的区间为{100 * lo:.0f}%到{100 * hi:.0f}%，区间内不动，外面交易到边缘。暂停预测，学习器会找到它吗？<bookmark mark='a'/>对照区间，看五个学习策略。",
    "f'They do: each seed leaves":
        "找到了：每个种子都在接近该区间的范围内保持不动，其净增长中位数为每年{100 * np.median(pg):.2f}%，胜过再平衡到默顿的{100 * pc['merton']['growth']:.2f}%。下一章：以确定下注规模为业的人。",
    'f"Not quite: the learners trade':
        "本协议下还没有完全找到：学习器往中间交易一部分，只留下很窄的不动区域。五个种子的净增长中位数为每年{100 * np.median(pg):.2f}%，对照每季回到默顿的{100 * pc['merton']['growth']:.2f}%以及区间策略的{100 * pc['band']['growth']:.2f}%。区间比学习器中位数高{100 * (pc['band']['growth'] - np.median(pg)):.2f}个百分点。这五个种子、这个训练预算没有恢复动态规划策略，不是所有强化学习方法的结论。下一章看实务。",
    'Chapter seventeen. Who sizes bets for a living.':
        '第17章。谁以定仓位为生。',
    'First the bettors, from their own accounts.':
        "先看下注者，依据他们自己的叙述。索普1994年的体育投注测试：五万美元，按凯利定仓位，优势估计刻意保守，一百零一天里赚了十二万三千美元。<bookmark mark='a'/>威廉·本特的团队每年在香港投注约四百七十场赛马，面对约百分之十九的抽成，五个赛季中四个盈利，始终押凯利的保守分数，因为按全凯利，用他的话说，损失一半资金是常有的事。<bookmark mark='b'/>埃尔温·伯利坎普学生时代在贝尔实验室凯利手下工作，1989年取得Axcom的控制权，这家公司为吉姆·西蒙斯的大奖章基金做交易。大奖章如何定仓位并未公开，我们也不猜测。",
    'Most institutions work inside risk budgets':
        "大多数机构在风险预算之内运作，而风险预算就是控制约束。挪威石油基金把相对基准的预期波动率上限定在一点二五个百分点；桥水的全天候组合始于1996年，在四种经济环境上放置相等的风险。<bookmark mark='a'/>据《华尔街日报》2024年报道，千禧年的基金经理亏损百分之五，资金会被减半，亏到百分之七点五很可能被解雇；该公司未予置评。<bookmark mark='b'/>格罗斯曼和周在1993年解决了回撤问题：通过持有高出下限的缓冲的默顿比例，永远不跌破峰值的alpha倍：这就是第2章的下限，只是会随峰值上调。对数效用Grossman-Zhou结果约束连续扩散中的贴现财富。下面每周模拟使用它启发的名义财富缓冲；离散交易和跳跃未必守住下限。",
    'f"One path each: Kelly in red':
        "红色是凯利，蓝色是GZ启发的名义财富缓冲，底线为峰值的八成；本条示例路径在下跌时减仓，并保持在底线之上。<bookmark mark='a'/>两千条路径中，凯利最坏回撤{100 * d['worst_dd_kelly']:.0f}%，缓冲策略{100 * d['worst_dd_gz']:.0f}%；中位对数增长分别为{100 * d['median_growth_kelly']:.1f}%和{100 * d['median_growth_gz']:.1f}%。<bookmark mark='b'/>距百分之五限额只差零点一个百分点时，缓冲很小，仓位也很小。这是每周名义财富示例，原理论约束连续时间贴现财富；样本未穿越底线不代表离散交易或跳跃下的保证。",
    'Volatility targeting here scales exposure by inverse lagged realized variance. M':
        '这里按滞后实现方差的倒数调整仓位。Moreira和Muir在2017年研究相关规则。本次既有登记历史计算使用九十四年French数据。方差信号虽滞后，但仓位用全样本均值归一化为一，整个流程仍有事后信息。毛收益未计交易和融资成本。',
    "f'It helped: a Sharpe ratio of":
        "本次事后毛收益计算的夏普为{v['sr_scaled']:.2f}，对照{v['sr_mkt']:.2f}；年化alpha为{100 * v['alpha']:.1f}%，所示t值{v['alpha_t']:.1f}来自同方差OLS参考，不是HAC统计量。这些样本关联不识别因果机制；仓位变化很大，实际基金通常限制杠杆。",
    "f'It did not help here:":
        "在这里它没有用：夏普比率{v['sr_scaled']:.2f}，对比{v['sr_mkt']:.2f}。",
    'Execution desks solve a control problem daily:':
        "执行交易台每天都在解控制问题：阿尔姆格伦和克里斯，2001年；Almgren、Thum、Hauptmann和Li用花旗集团的交易拟合了冲击，它随规模的五分之三次方增长。<bookmark mark='a'/>还有维克多·哈加尼，就是那个硬币实验的作者，如今用默顿规则给客户的组合定仓位；他与詹姆斯·怀特2023年合著的《消失的亿万富翁》把财富的流失归咎于糟糕的仓位与消费。最后，前沿。",
    'For the researcher: Chapter 9 asked':
        '写给研究者：第9章问的是，如果你把优势高估了固定的倍数会怎样。但估计出来的优势，误差是随机的，而且有它的分布规律。这里给出按估计值下注的确切代价，以及让代价最小的比例。',
    "Start with one risky asset and known volatility. <bookmark mark='a'/> Replace th":
        "从单一风险资产、已知波动率开始。<bookmark mark='a'/>将默顿比例中的平均超额收益换成T年高斯估计。<bookmark mark='b'/>CE是GBM固定比例的精确年度CRRA确定性等价对数率，扣除现金。对估计均值平均这个分数，不等于最大化无条件期望效用。<bookmark mark='c'/>估计均值的二阶矩为真均值平方加sigma平方除以T。固定T时，跨估计取平均仍保留方差惩罚：平均CE为西塔平方减T分之一，再除以二伽马。<bookmark mark='d'/>真值最优分数为西塔平方除以二伽马，估计代价是二伽马T分之一。西塔零点四时，历史短于六又四分之一年，代入规则平均CE为负；这不表示期望算术利润为负。",
    "So consider a fixed scaling. <bookmark mark='a'/> Expected CE across estimated m":
        "考虑固定倍数。<bookmark mark='a'/>对均值估计取平均后的CE是c的抛物线。<bookmark mark='b'/>波动率已知时，顶点为T乘夏普平方，除以它再加一。夏普零点四时，二十年取百分之七十六，五年取四十四。这个真值规则需要真实夏普。目标是对估计样本平均的CE，不同于无条件期望效用。<bookmark mark='c'/>其平均CE非负，夏普非零时为正；任意收缩并无保证。<bookmark mark='d'/>Kan与Zhou在2007年研究了多资产参数不确定性下的相关组合；估计协方差的公式另需条件。",
    "These curves use known volatility. <bookmark mark='a'/> The plug-in crosses zero":
        "曲线先假设波动率已知。<bookmark mark='a'/>代入规则在六又四分之一年穿过零，再从下方靠近真值最优分数。<bookmark mark='b'/>大约十九年以前，一半优于全量；之后估计改善，一半放弃了太多增长。<bookmark mark='c'/>金色真值规则使用真实夏普，在同一平均CE目标下不低于这两种固定选择。<bookmark mark='d'/>白点连波动率也估计，长历史时接近已知波动率公式，五年时额外估计惩罚明显。独立同分布正态收益且样本数足够时，可用卡方逆矩求修正公式，见第九题。",
    'f"The table mixes two explicitly labelled calculations: estimated-variance simul':
        "表里明确区分两种计算：估计方差的模拟，以及已知波动率的解析真值列。<bookmark mark='a'/>五年时，代入平均CE为{100 * t['sims']['5']['plug']:.1f}%，一半为{100 * t['sims']['5']['half']:.1f}%，{100 * t['sims']['5']['p_negative_ce']:.0f}%的代入估计对应负的真实CE。这是CE分数，不是算术利润。<bookmark mark='b'/>五十年时，代入接近真值列，一半已落后。<bookmark mark='c'/>紫色倍数来自同一数据，随估计夏普的平方增加，本身也有噪声。在这些模拟中，二十年以内所展示的期限都不如简单的一半。已知真值缩放与从数据估计它不同。",
    'f"Now a retrospective, frictionless US illustration at gamma two, scored from Ju':
        "看伽马为二的美国市场事后无摩擦示例，从1936年7月评分。每月只用此前数据，初始窗口为1926年7月至1936年6月。<bookmark mark='a'/>实现均值减一半伽马乘方差的分数，代入规则{100 * u['plug']['ce']:.1f}%，一半{100 * u['half']['ce']:.1f}%，估计倍数{100 * u['chat']['ce']:.1f}%。这是实现代理值，不是有限样本精确效用。<bookmark mark='b'/>本路径上代入规则在三者中胜出。窗口由十年增加到约九十五年，之后夏普{t['us_theta']:.2f}，全样本{t['us_theta_all']:.2f}。单一路径不能独自检验期望。<bookmark mark='c'/>直接持有市场在这里超过三条估计规则。全样本默顿使用事后信息。这些比较既不识别单一原因，也未计交易成本。",
    "Three open questions. <bookmark mark='a'/> The optimal multiple needs":
        "三个研究方向。<bookmark mark='a'/>真值最优倍数需要真实夏普。估计它有噪声；比较可行规则须指定损失、策略类和参数范围，不能声称普适支配。<bookmark mark='b'/>贝叶斯投资者边投资边学习；Barberis在2000年说明参数不确定性可让期限重要。优势若漂移，历史长度与收缩应一起选择。<bookmark mark='c'/>肥尾和波动聚集下，估计对凯利增长的代价依赖具体模型和估计器，不能直接沿用高斯公式。",
    'Pause and predict. A Sharpe ratio of point three, estimated':
        '暂停预测。夏普零点三由二十五年数据估计。假设它恰是真值，已知波动率下哪个固定倍数最大化平均CE？二点二五除以三点二五，约零点六九。这是假设真值的计算，不是估计值带来的保证。',
}
