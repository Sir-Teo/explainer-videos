"""Chinese narration for quant40: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 在险价值 (VaR), 预期亏损 (expected shortfall), 一致性风险度量
(coherent risk measure), 次可加性 (subadditivity), 谱风险度量 (spectral), 凸风险度量 (convex), 回测 (backtest), 例外
(exception), 红绿灯 (traffic light), 条件覆盖 (conditional coverage), 极值理论 (EVT), 广义帕累托 (GPD), 超阈值峰值 (POT),
尾部指数 (tail exponent), 尾部相依 (tail dependence), Copula (copula), 压力测试 (stress test), 反向压力测试 (reverse stress),
重排算法 (rearrangement algorithm), 弹球损失 (pinball loss), 可引出性 (elicitability), 评分函数 (scoring function),
流动性期限 (liquidity horizon)."""

TITLE = '量化金融，从零搭建 · 第40部分：度量风险'

CHAPTERS = {
    'Hook': '由一日VaR到十日VaR',
    'VaR': '1. 在险价值的三种算法',
    'Coherent': '2. 一致性风险度量',
    'Backtest': '3. 回测',
    'EVT': '4. 极值理论',
    'Depend': '5. 相依性与Copula',
    'Stress': '6. 压力测试',
    'Uncertainty': '7. 模型不确定性',
    'Learned': '8. 学习出来的风险',
    'FRTB': '9. 监管与流动性',
    'House': '10. 第40条规则：风险数字是一种预测',
    'Research': '写给研究者：什么可以被回测？',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part forty. Measuring risk:":
        "第40部分。度量风险：一家公司用来说明自己可能亏多少的数字，如何得出它们、如何检验它们，以及它们看不见什么。这是第七幕“体系”的第一部分。",

    'f"A desk question. <bookmark mark=\'a\'/> Your ninety-nine percent':
        "一个交易台问题。<bookmark mark='a'/>你的99%单日在险价值是一千万美元。<bookmark mark='b'/>监管机构要十天的。<bookmark mark='c'/>教科书的答案是"
        "根号十乘以一千万，约三千二百万，这假设每天独立同分布且服从正态。在美国市场九十年的数据上，实际的十日损失给出的比值是{ratio:.1f}，而不是3.16，"
        "在某些十年里还要大得多。",

    'f"What this part finds.':
        "这一部分的发现。<bookmark mark='a'/>在九十三年里，正态VaR在{100 * n['rate']:.2f}%的日子里被突破，是承诺的两倍多，而且成簇出现；而一个经GARCH过滤的"
        "VaR通过了所有检验。<bookmark mark='b'/>预期亏损无法单独回测，研究者章节会证明这一点，但它可以和VaR一起回测。<bookmark mark='c'/>相依性是最大的未知数："
        "在厚尾下，一个总和的VaR的最坏情形是各部分之和的{r2['worst_lo'] / r2['comonotonic']:.1f}倍。",

    "Why it matters. <bookmark mark='a'/> Risk numbers set capital:":
        "为什么重要。<bookmark mark='a'/>风险数字决定资本：银行交易账户的资本、清算所的保证金、基金的限额。错向一边，公司就脆弱；错向另一边，资本就闲置。"
        "<bookmark mark='b'/>据报道，它们在2007年和2008年当众失灵，例外成簇出现，损失是所报VaR的许多倍。<bookmark mark='c'/>本系列公司建立的每一个交易台"
        "现在都需要一个限额，而限额就是一个必须有人为之辩护的风险数字。",

    "Three things a risk number is not.":
        "风险数字不是什么。<bookmark mark='a'/>它不是最坏情形：按定义，每一百天里就有一天更糟，糟多少它没有说。<bookmark mark='b'/>它不是头寸本身的属性："
        "它是一个模型和一个窗口给出的预测，换一个模型就会得到另一个数字。<bookmark mark='c'/>它也不是全部风险：流动性、尾部的相依性，以及数据中从未出现过的事件，"
        "都在它之外。",

    "Where this sits. Act six built every trading desk.":
        "这一部分的位置。第六幕建起了每一个交易台。第七幕退后一步看整个体系：这一部分度量风险，第41部分追踪杠杆和流动性如何走向危机，第42部分让机器进入市场，"
        "第43部分追问这一切是否能战胜市场。",

    "Seventy years. Andrew Roy's safety-first rule":
        "七十年。Andrew Roy在1952年的安全第一准则；七十年代的极值定理；Kent Osband关于引出的论文；以及摩根大通的RiskMetrics。<bookmark mark='a'/>"
        "然后是巴塞尔的VaR、一致性风险度量、McNeil和Frey带极值尾部的GARCH，以及CAViaR。<bookmark mark='b'/>再然后是危机、Gneiting的可引出性、FRTB转向"
        "预期亏损以及Fissler和Ziegel的联合评分，还有它的实用形式。",

    "The plan: value at risk three ways;":
        "计划：在险价值的三种算法；一致性与预期亏损；回测；尾部与相依性；压力测试与模型不确定性；学习出来的风险模型；监管与流动性；以及对“什么可以被回测”"
        "这一理论的证明。",

    "In the House, the risk function takes over":
        "在本系列公司里，风险部门接手了每个交易台的晚间报告，它首先追问：如果自己的数字错了，它要怎么知道。",

    # ------------------------------------------------------------------ VaR
    "Chapter one. Since the nineteen nineties,":
        "第1章。自九十年代以来，银行用一个数字概括市场风险：在给定的一天、给定的置信水平下，它们预计不会超过的损失。这一章定义它，用三种方法估计它，"
        "并说明这些估计在哪里出现分歧。",

    "The definitions. <bookmark mark='a'/> Work in losses:":
        "定义。<bookmark mark='a'/>以损失计：损失是负的收益。<bookmark mark='b'/>置信水平为alpha的在险价值，是损失的alpha分位数，即以一减alpha的概率被超过的门槛。"
        "<bookmark mark='c'/>预期亏损是超过它的那些日子里的平均损失。<bookmark mark='d'/>在99%下，VaR应该每一百天被突破一次。那是关于频率的承诺，完全不涉及幅度；"
        "预期亏损才说明幅度。",

    'f"In a picture, for a Student t':
        "画成图，用一个四个自由度的学生t分布。<bookmark mark='a'/>VaR是一条线：百分之一的概率质量位于{v:.2f}之外。<bookmark mark='b'/>预期亏损是阴影部分的"
        "重心，在{es:.2f}处：尾部变厚时它会移动，即使那条线不动。",

    "Where the number came from.":
        "这个数字从何而来。<bookmark mark='a'/>摩根大通的RiskMetrics，1996年公开：一个lambda为0.94的指数加权方差，即第7部分的EWMA。<bookmark mark='b'/>"
        "在正态收益下，99%的VaR是2.33个标准差乘以头寸。<bookmark mark='c'/>据报道，它每天下午四点十五分被送到董事长手中，而巴塞尔1996年的修订允许银行"
        "依据这类模型计算资本。",

    "Three ways to estimate it.":
        "估计它的三种方法。<bookmark mark='a'/>参数法：假设一个分布，估计参数，读出分位数。<bookmark mark='b'/>历史模拟法：把过去五百天的收益作用在今天的头寸上，"
        "取第五差的那一天，除了窗口什么也不假设。<bookmark mark='c'/>以及蒙特卡洛法：在拟合的模型下模拟头寸，当期权让损失变得非线性时必须用它。",

    'f"A hundred million dollars in the American stock market':
        "2007年底投在美国股市的一亿美元，用此前五百天的数据。<bookmark mark='a'/>正态法给出的VaR是{100 * x['normal'][0]:.1f}百万；历史模拟法是"
        "{100 * x['hs'][0]:.1f}。<bookmark mark='b'/>拟合的学生t分布，自由度约为{x['nu']:.0f}，它和它的蒙特卡洛在VaR上与历史法一致，却把预期亏损定得高得多，"
        "{100 * x['t'][1]:.1f}百万。<bookmark mark='c'/>而对那年秋天的波动作出反应的RiskMetrics给出{100 * x['ewma'][0]:.1f}。五种诚实的方法，差异几乎达到"
        "这个数字的一半。",

    'f"The same position on the fifteenth of October':
        "同一个头寸，2008年10月15日。<bookmark mark='a'/>用五百天数据的方法仍然看到的大多是平静：正态VaR为{100 * x['normal'][0]:.1f}百万，历史法"
        "{100 * x['hs'][0]:.1f}。<bookmark mark='b'/>RiskMetrics在年化波动率{100 * x['sig_ann']:.0f}%下给出{100 * x['ewma'][0]:.1f}。<bookmark mark='c'/>"
        "那天市场下跌了{loss:.1f}%：这个头寸亏了{loss:.1f}百万。只有很快忘记过去的方法接近了它。",

    'f"The desk question\'s rule.':
        "交易台问题里的规则。<bookmark mark='a'/>十日VaR等于根号十乘以一日VaR：只对独立的正态收益精确成立。<bookmark mark='b'/>在1926年到2020年的美国市场上，"
        "一日99%的历史VaR为{100 * s['one_day']:.2f}%，按规则放大为{100 * s['scaled']:.2f}%。<bookmark mark='c'/>实际发生的十日损失给出"
        "{100 * s['direct']:.2f}%：大跌的日子成簇出现，这条规则低估了风险。",

    'f"Decade by decade, the rule is neither safe nor conservative.':
        "逐个十年来看，这条规则既不安全也不保守。<bookmark mark='a'/>在七十年代，实际的十日VaR是放大值的{hi70:.2f}倍：日收益正自相关，坏日子后面跟着坏日子。"
        "<bookmark mark='b'/>在九十年代是{lo90:.2f}倍：坏日子后面跟着反弹。误差取决于日与日之间的相依性，而这条规则恰恰把它假设掉了。",

    'f"Why Monte Carlo is needed for options.':
        "为什么期权需要蒙特卡洛。<bookmark mark='a'/>一个做空一千份平值跨式期权并做了delta对冲的组合。它的delta为零，所以线性的delta-正态VaR为零。"
        "<bookmark mark='b'/>加上伽马，损失变成二次的，VaR为{o['delta_gamma'][0]:,.0f}美元。<bookmark mark='c'/>在每一个模拟价格上对每一份期权完全重新定价，"
        "得到{o['full'][0]:,.0f}。<bookmark mark='d'/>如果隐含波动率同时上升五个点，则是{o['vol_shock'][0]:,.0f}：一个只看现货的模型永远不会去动的风险因子。",

    "What the number is.":
        "这个数字是什么。<bookmark mark='a'/>它说，在模型之下，每一百天里有九十九天损失会更小。<bookmark mark='b'/>它没有说第一百天的损失有多大，没有说模型是否正确，"
        "也没有说如果头寸无法在一天内卖出会怎样。<bookmark mark='c'/>它之所以长盛不衰，是因为它是一个董事会读得懂、又能用随后的日子来检验的数字。接下来两章追问"
        "它是否应该相加，以及如何检验它。",

    "Pause and predict. Two bonds each lose a hundred dollars":
        "暂停并预测。两只债券各自以百分之四的概率独立地亏损一百美元，否则不亏。每只的95% VaR都是零。同时持有两只时，95% VaR是多少？",

    # ------------------------------------------------------------------ Coherent
    'f"Chapter two, and the answer to the pause:':
        "第2章，以及暂停问题的答案：{b['var']:.0f}美元。至少一只债券违约的概率是{100 * b['p_any']:.2f}%，超过百分之五，所以组合的VaR是一次完整的违约，"
        "而每只债券单独看都是零。分散化让报告出来的风险凭空出现。",

    'f"The numbers. <bookmark mark=\'a\'/> Each bond alone:':
        "数字。<bookmark mark='a'/>每只债券单独看：VaR为零，因为违约比二十天里的一天还罕见；预期亏损为{s['es']:.0f}。<bookmark mark='b'/>两者相加，VaR为零。"
        "<bookmark mark='c'/>一起持有，VaR为{b['var']:.0f}。预期亏损的方向相反：一起持有为{b['es']:.1f}，小于相加的{2 * s['es']:.0f}。一个度量惩罚分散化，"
        "另一个奖励它。",

    "Philippe Artzner, Freddy Delbaen, Jean-Marc Eber and David Heath asked":
        "Philippe Artzner、Freddy Delbaen、Jean-Marc Eber和David Heath追问一个风险度量应当满足什么，并把答案称为一致性。<bookmark mark='a'/>额外一笔确定的损失，"
        "恰好增加那么多资本。<bookmark mark='b'/>头寸翻倍，风险翻倍。<bookmark mark='c'/>总是亏得更多的头寸风险更大。<bookmark mark='d'/>合并永远不会制造风险："
        "公司的资本至多等于各交易台资本之和。",

    "VaR's record.":
        "VaR的表现。<bookmark mark='a'/>它满足前三条：任何分位数都满足。<bookmark mark='b'/>对于偏斜的、离散的或极厚尾的损失，它不满足第四条，正如两只债券所示；"
        "对于正态或t分布，它碰巧成立。<bookmark mark='c'/>这个失效很要紧：一个交易台可以通过拆分头寸，或者卖出恰好位于分位数之外、度量看不到的风险，来压低报告的VaR。",

    "Expected shortfall passes.":
        "预期亏损通过了。<bookmark mark='a'/>它是alpha之外所有分位数的平均。<bookmark mark='b'/>等价地，它是在所有不把任何状态的概率放大超过一除以一减alpha倍的"
        "重新加权下的最坏期望损失：一组压力情景。<bookmark mark='c'/>期望的上确界是次可加的。所以预期亏损对任何分布都是一致的。",

    "In numbers. <bookmark mark='a'/> For a normal loss, expected shortfall":
        "用数字说明。<bookmark mark='a'/>对正态损失，预期亏损等于均值加上sigma乘以分位点处的密度再除以尾部概率。<bookmark mark='b'/>在99%下是2.67个sigma，"
        "而VaR是2.33。<bookmark mark='c'/>在97.5%下是2.34：对正态分布与99%的VaR相同，尾部一厚就更大。这种等价正是监管机构选择它的原因。",

    "The family behind it.":
        "它背后的家族。<bookmark mark='a'/>Carlo Acerbi的谱风险度量给每个分位数加权。<bookmark mark='b'/>当权重朝最坏结果递增时，它们恰好是一致的，"
        "相当于把风险厌恶写成一个函数。<bookmark mark='c'/>预期亏损对尾部等权、忽略其余部分；VaR只是一个点，根本不在这个家族里。",

    "And beyond. <bookmark mark='a'/> Hans Föllmer and Alexander Schied":
        "更进一步。<bookmark mark='a'/>Hans Föllmer和Alexander Schied把齐次性放宽为凸性：头寸翻倍，风险可能不止翻倍，这正是流动性不足造成的。"
        "<bookmark mark='b'/>每一个这样的度量，都是对一组情景的最坏期望损失，每个情景按其不合理程度被罚分。<bookmark mark='c'/>以相对熵作罚分，就是熵风险度量，"
        "即换了面貌的第8部分指数效用。",

    'f"Coherence also tells a firm how to split its capital.':
        "一致性还告诉公司如何分配资本。<bookmark mark='a'/>正齐次性给出欧拉定理：风险恰好等于每个头寸乘以其边际风险之和。<bookmark mark='b'/>对预期亏损，"
        "就是每个头寸在超过VaR的那些日子里的平均损失。<bookmark mark='c'/>在一个市场加上小盘股和价值股倾斜的组合上，市场承担了预期亏损的"
        "{100 * eu['share'][0]:.0f}%。<bookmark mark='d'/>价值因子承担了尾部的{100 * eu['share'][2]:.1f}%，而方差中只占{100 * eu['sd_share'][2]:.1f}%："
        "在最糟的日子里，它和市场一起下跌。",

    "So which? <bookmark mark='a'/> VaR is easy to explain":
        "那么选哪个？<bookmark mark='a'/>VaR容易解释、容易回测，看不见它那条线以外的东西，而且不是次可加的。<bookmark mark='b'/>预期亏损是一致的、看得见尾部，"
        "但更难估计，而且正如研究者章节所证明的，无法单独回测。<bookmark mark='c'/>监管机构在2016年把交易账户资本改为97.5%的预期亏损，而银行仍在旁边回测VaR。",

    "Pause and predict. A ninety-nine percent VaR model was used":
        "暂停并预测。一个99% VaR模型用了二百五十天，其中七天被突破。这个模型错了吗？你会如何判断，除了次数还会看什么？",

    # ------------------------------------------------------------------ Backtest
    'f"Chapter three, and the answer to the pause: probably.':
        "第3章，以及暂停问题的答案：很可能。七次例外，而预期只有二点五次，这把模型放进了巴塞尔的黄灯区，Kupiec检验在百分之五的水平上拒绝它，p值为"
        "{k['p_value']:.3f}。但次数只是一半的证据：例外是否扎堆出现，和有多少次同样重要。",

    "A forecast can be checked.":
        "预测是可以检验的。<bookmark mark='a'/>每一天，损失要么超过前一天晚上做出的预测，要么没有：这就是命中序列。<bookmark mark='b'/>如果预测正确，命中就是"
        "概率为一减alpha的独立抛硬币。<bookmark mark='c'/>Paul Kupiec的检验用似然比比较承诺的比率和观测到的比率，第2和21部分也这样做过。",

    "Regulators turned the count into a traffic light.":
        "监管机构把次数变成了红绿灯。<bookmark mark='a'/>在二百五十天里，四次以内是绿灯，资本为模型VaR的三倍。<bookmark mark='b'/>五到九次是黄灯，乘数递增。"
        "<bookmark mark='c'/>十次以上是红灯：乘数为四，模型要接受审查。",

    "Peter Christoffersen added the timing.":
        "Peter Christoffersen加入了时间维度。<bookmark mark='a'/>把命中视为一个两状态马尔可夫链：平静一天之后出现例外的概率，<bookmark mark='b'/>"
        "以及一次例外之后再出现例外的概率。<bookmark mark='c'/>正确的预测使两者相等：昨天的命中对今天毫无信息。<bookmark mark='d'/>把两个似然比相加，就同时检验了"
        "次数和时间。",

    'f"Six forecasters, every day from nineteen twenty-eight':
        "六个预测者，从1928年到2020年的每一天，每个{n['T']:,}次预测。<bookmark mark='a'/>用五百天数据的正态法在{100 * n['rate']:.2f}%的日子里被突破，"
        "是承诺的两倍多，而且一次例外之后第二天再被突破的比例是{100 * n['p11']:.0f}%。历史模拟法和RiskMetrics也失败了。<bookmark mark='b'/>按波动率过滤有帮助；"
        "用非对称的GARCH，即GJR，过滤后通过了两项检验，突破比例为{100 * g['rate']:.2f}%，例外不扎堆。<bookmark mark='c'/>再加上极值尾部则矫枉过正，"
        "{100 * e['rate']:.2f}%：过于谨慎，Kupiec同样拒绝它。",

    "Where the failures come from.":
        "失败来自哪里。<bookmark mark='a'/>整个2008年，五百天的正态VaR几乎不动，而损失越来越大：它的例外成批出现在九月和十月。<bookmark mark='b'/>经GARCH过滤的"
        "预测在几天内随波动率上升，损失大多停留在它之下。风险数字必须足够快地忘记平静，才能看见风暴。",

    'f"Year by year, the exceptions.':
        "逐年来看例外。<bookmark mark='a'/>正态法的柱子在危机年份高耸：三十年代、1987年、2008年，最糟的是{worst}年，{n_max}次例外，而承诺的是二点五次。"
        "<bookmark mark='b'/>过滤后的预测的柱子无论好年坏年都停在二点五的虚线附近：它在危机中出错的频率和平静时差不多，这正是一个预测应有的样子。",

    'f"The traffic light, calendar year by calendar year.':
        "按日历年看红绿灯。<bookmark mark='a'/>正态法在{ny}年里有{n['red']}年是红灯。<bookmark mark='b'/>GJR过滤的预测有{g['red']}年红灯、{g['yellow']}年黄灯："
        "大约就是一个正确模型自身运气不好会出现的次数。",

    'f"And the shortfall.':
        "还有预期亏损。<bookmark mark='a'/>Carlo Acerbi和Balazs Székely的Z2统计量追问，在超过VaR的那些日子里，损失是否像预期亏损承诺的那样大：如果是则为零，"
        "如果预期亏损太低则为正。<bookmark mark='b'/>在正确预测下模拟，这么多天数时它的5%临界值，对正态损失约为{c95:.2f}，对厚尾损失约为{c95t:.2f}："
        "几乎相同，正如他们所发现的。<bookmark mark='c'/>正态法的得分为{n:+.2f}，历史模拟法和RiskMetrics也失败了；GARCH过滤的预测得分在零或零以下。",

    "Three lessons. <bookmark mark='a'/> Backtests have little power:":
        "三条教训。<bookmark mark='a'/>回测的检验力很弱：一年里预期只有二点五次例外，所以一个错了一半的模型经常还是绿灯。<bookmark mark='b'/>扎堆是破绽：一个忽视波动率的"
        "模型，先在时间上失败，然后才在次数上失败。<bookmark mark='c'/>保守也不是免费的：一个为很小的风险收取过多资本的模型同样是错的。",

    "Pause and predict. The American market's worst day":
        "暂停并预测。美国市场自1926年以来最糟的一天亏损约百分之十七。在对所有这些日子拟合的正态分布下，这样的一天应该多久发生一次？",

    # ------------------------------------------------------------------ EVT
    "f'Chapter four, and the answer to the pause:":
        "第4章，以及暂停问题的答案：1987年10月19日是{e['z_worst']:.0f}个标准差。在正态分布下，这样一天的概率约为十的负{abs(e['log10_p_worst']):.0f}次方："
        "十的{yrs:.0f}次方年一遇，而宇宙才一百四十亿岁。正态分布在尾部不是错了一点，而是差得离谱。",

    'f"The tails. <bookmark mark=\'a\'/> Daily American returns':
        "尾部。<bookmark mark='a'/>美国自1926年以来的日收益超额峰度为{e['kurt']:.0f}，而正态分布为零。<bookmark mark='b'/>最糟的一天亏损{100 * e['worst']:.1f}%。"
        "<bookmark mark='c'/>远端的尾部按损失的幂次衰减，而不是像正态那样按平方的指数衰减，而这个幂次，即尾部指数，是可以估计的。",

    "The theorem that makes this possible.":
        "使这一切成为可能的定理。<bookmark mark='a'/>对几乎任何分布，超过高阈值的超出部分近似服从广义帕累托分布，形状参数为xi，尺度参数为beta。<bookmark mark='b'/>"
        "xi为正对应幂律尾部，指数为一除以xi；为零对应指数尾部；为负对应有终点的尾部。它对极值所起的作用，就像中心极限定理对和所起的作用。",

    'f"Peaks over threshold, on the American market.':
        "美国市场上的超阈值峰值法。<bookmark mark='a'/>把阈值取在日损失的第95百分位，{100 * e['u']:.2f}%，保留超过它的{e['n_u']:,}天。<bookmark mark='b'/>"
        "对它们的超出部分拟合广义帕累托：xi为{e['xi']:.2f}。<bookmark mark='c'/>尾部指数约为{1 / e['xi']:.0f}。<bookmark mark='d'/>拟合的尾部给出超出数据中"
        "任何一天的分位数和预期亏损。",

    "How well it fits.":
        "拟合得有多好。<bookmark mark='a'/>在对数刻度上，超过每个损失的超出比例：数据落在一条略微弯曲的线上。<bookmark mark='b'/>拟合的帕累托一直跟到1987年的崩盘，"
        "也就是末端那唯一的一个点。",

    'f"Does the answer depend on the threshold?':
        "答案取决于阈值吗？<bookmark mark='a'/>把阈值从第90百分位移到第99百分位，超出的天数从约两千五百天降到二百五十天。<bookmark mark='b'/>拟合的形状参数始终在"
        "{lo:.2f}到{hi:.2f}之间。当估计在不同阈值下保持稳定时，广义帕累托找到的是尾部，而不是阈值。",

    'f"Beyond the data.':
        "超出数据之外。<bookmark mark='a'/>在99%下，EVT和历史法一致，{100 * r99['evt'][0]:.1f}%和{100 * r99['hs'][0]:.1f}%，而正态法给出"
        "{100 * r99['normal'][0]:.1f}%。<bookmark mark='b'/>在99.99%下，即四十年一遇的一天，历史法只有两三个点；EVT外推出{100 * r9999['evt'][0]:.1f}%，"
        "预期亏损为{100 * r9999['evt'][1]:.1f}%；正态法仍然说{100 * r9999['normal'][0]:.1f}%。置信水平越高，正态法的误差就越大，没有上限。",

    'f"A second estimate, Bruce Hill\'s.':
        "第二种估计，Bruce Hill的。<bookmark mark='a'/>用最大的k个损失，尾部指数等于每个损失与第k个之比的对数的平均值的倒数。<bookmark mark='b'/>用最大的一百个，"
        "它给出约{h[2]:.1f}；用一千六百个，{h[-1]:.1f}。估计随k漂移，这是每个尾部估计量都有的偏差与方差的权衡。大约在三到五之间，这是股票的经典答案："
        "尾部很厚，但方差有限。",

    'f"Other tails.':
        "其他尾部。<bookmark mark='a'/>美国市场的收益尾部和损失尾部一样厚，按拟合的形状参数还更厚，{ur['xi']:.2f}对{ul['xi']:.2f}：它最大的上涨日出现在危机之中，"
        "在三十年代和2008年。<bookmark mark='b'/>比特币2017到2020年的损失形状参数为{bl['xi']:.2f}，而其收益的估计{br['xi']:+.2f}只来自六十二天：这提醒我们，"
        "四年数据得出的尾部估计大多是噪声。",

    "EVT for a forecast, after Alexander McNeil":
        "用于预测的EVT，依照Alexander McNeil和Rüdiger Frey。<bookmark mark='a'/>收益等于波动率乘以一个独立的冲击。<bookmark mark='b'/>用GARCH对波动率建模，"
        "使冲击接近独立，<bookmark mark='c'/>再用广义帕累托拟合冲击的尾部，那里理论的假设才成立。<bookmark mark='d'/>这就是第3章的第六个预测者：它的例外不扎堆，"
        "但在99%下过于谨慎。",

    "Three cautions.":
        "三点提醒。<bookmark mark='a'/>阈值是一种选择：太低，帕累托不适用；太高，数据太少。<bookmark mark='b'/>相依性会破坏理论，所以McNeil和Frey先做过滤。"
        "<bookmark mark='c'/>外推仍然是一个模型：超出数据之外的最佳猜测，不确定性很大，而不是对它的了解。",

    "Pause and predict. Bank stocks and insurance stocks":
        "暂停并预测。银行股和保险股的日相关系数约为0.8。高斯模型说，在银行最糟的百分之一的日子里，保险公司约有百分之四十的时间也处在自己最糟的百分之一。"
        "数据怎么说？",

    # ------------------------------------------------------------------ Depend
    'f"Chapter five, and the answer to the pause:':
        "第5章，以及暂停问题的答案：{100 * p['emp']['0.01']:.0f}%。在银行最糟的日子里，保险公司有{100 * p['emp']['0.01']:.0f}%的时间也处在自己最糟的日子，"
        "而相关系数相同的高斯模型说是{100 * p['gauss']['0.01']:.0f}%。模型把平均关系弄对了，却把崩盘弄错了。",

    "Paul Embrechts, Alexander McNeil and Daniel Straumann's pitfalls":
        "Paul Embrechts、Alexander McNeil和Daniel Straumann总结的相关性陷阱。<bookmark mark='a'/>零相关不等于独立。<bookmark mark='b'/>并非每个相关系数都可能："
        "对波动率差别很大的对数正态边缘分布，可达到的范围很窄。<bookmark mark='c'/>相关性也不决定尾部：同样的边缘分布、同样的相关系数，一起崩盘的概率可以大不相同。",

    "Separate the two.":
        "把两者分开。<bookmark mark='a'/>Abe Sklar的定理：任何联合分布都是其边缘分布用一个Copula粘合起来的。<bookmark mark='b'/>Copula就是去掉边缘分布之后的相依性。"
        "<bookmark mark='c'/>高斯Copula，第20部分的信用模型。<bookmark mark='d'/>以及学生t Copula，相关参数相同，却倾向于让极端值一起出现。",

    "Seen as points, with uniform marginals.":
        "画成点，边缘分布为均匀分布。<bookmark mark='a'/>相关系数0.7的高斯Copula：点云在角上变稀。<bookmark mark='b'/>相关系数相同、自由度为三的t Copula：角上填满了。"
        "数一数两者都落在各自最糟百分之五的点。",

    "The measure of joint crashes.":
        "一起崩盘的度量。<bookmark mark='a'/>尾部相依：已知一个变量处在极端尾部时，另一个也处在极端尾部的概率的极限。<bookmark mark='b'/>对高斯Copula，只要相关系数小于一，"
        "它就是零：共同的极端值变得罕见到不可能。<bookmark mark='c'/>对t Copula，它保持为正：相关系数0.8、自由度为四时约为一半。",

    'f"In the data: Kenneth French\'s industries,':
        "看数据：Kenneth French的行业组合，取四十九个行业全部有交易的每一天，从1969年起。<bookmark mark='a'/>银行与保险：数据为{p0['emp']['0.01']:.2f}，"
        "高斯为{p0['gauss']['0.01']:.2f}。<bookmark mark='b'/>石油与矿业：{p1['emp']['0.01']:.2f}对{p1['gauss']['0.01']:.2f}，不到一半。<bookmark mark='c'/>"
        "每一对中，一起崩盘都比高斯Copula允许的更常见；t Copula的极限更接近，尽管百分之一处的有限样本还不是极限。",

    'f"What the copula does to a portfolio\'s risk.':
        "Copula对组合风险有什么影响。两种资产，边缘分布同为厚尾、相关系数相同，用两种方式组合。<bookmark mark='a'/>在99%下，VaR几乎不变："
        "{100 * g['var'][0]:.2f}%对{100 * t['var'][0]:.2f}%。<bookmark mark='b'/>但99.9%之外的预期亏损从{100 * g['var999'][1]:.1f}%升到"
        "{100 * t['var999'][1]:.1f}%。Copula活在深尾，恰恰是99% VaR不看的地方。",

    'f"A trap.':
        "一个陷阱。<bookmark mark='a'/>四十九个行业在所有日子里的平均相关系数是{d['avg_all']:.2f}。<bookmark mark='b'/>在市场最糟的百分之五的日子里，它是"
        "{d['avg_bad']:.2f}：更低，这与每个交易员“一切都在一起下跌”的经验相反。<bookmark mark='c'/>这是一个统计假象：按结果挑选日子截断了取值范围，截断样本内的"
        "相关系数是有偏的。尾部相依问的是正确的问题；条件相关不是。",

    "This is not academic.":
        "这不是纸上谈兵。<bookmark mark='a'/>David Li的高斯Copula用一个相关系数为担保债务凭证的分层定价，即第20部分的模型。<bookmark mark='b'/>尾部相依为零，"
        "它让优先级分层看起来几乎没有风险。<bookmark mark='c'/>2007年和2008年，违约一起到来，违约总是这样；据报道，这个公式后来受到指责，尽管是使用者自己选择了"
        "忽视它遗漏的东西。",

    "Three lessons. <bookmark mark='a'/> Model the tail of the joint distribution":
        "三条教训。<bookmark mark='a'/>对联合分布的尾部建模，并用共同超越来检验它，而不是用相关系数。<bookmark mark='b'/>在所有日子上测得的分散化收益，"
        "在需要它的日子里更小。<bookmark mark='c'/>而相依性本身是不确定的：第7章追问，当对它一无所知时，VaR会有多糟。",

    "Pause and predict. A portfolio's daily volatility":
        "暂停并预测。一个组合的日波动为一百二十万美元。让它在一天内亏损一千万美元的、最合理的风险因子变动是什么？那个变动离中心有多少个标准差？",

    # ------------------------------------------------------------------ Stress
    "f'Chapter six, and the answer to the pause:":
        "第6章，以及暂停问题的答案：市场下跌{100 * abs(x[0]):.1f}%，规模和价值因子小幅下跌，距离约{r['distance']:.1f}个标准差。以给定金额亏损的最合理方式，"
        "是让每个因子按其与组合的协方差成比例地变动。这一章推导它，并把它与历史对照。",

    "Why a second kind of number.":
        "为什么需要第二种数字。<bookmark mark='a'/>VaR是一个用近期历史拟合的模型的分位数，对窗口从未见过的事情一言不发。<bookmark mark='b'/>压力测试点名一个事件，"
        "在它之下对今天的头寸重新估值。<bookmark mark='c'/>反向压力测试则问相反的问题：造成给定损失的最可能情景是什么？",

    'f"Historical scenarios, on a portfolio of the market':
        "历史情景，作用于一个市场加上小盘股和价值股倾斜的组合。<bookmark mark='a'/>1987年10月19日：亏损{a['loss_m']:.1f}百万，在因子的联合分布中距离"
        "{a['mahal']:.0f}个标准差。<bookmark mark='b'/>2008年10月，{b_['loss_m']:.1f}百万；<bookmark mark='c'/>2020年3月16日，{c['loss_m']:.1f}。"
        "每一天都是一个用此前年份拟合的VaR模型会称为不可能的日子。",

    'f"History\'s own ten-day scenarios.':
        "历史自己的十日情景。<bookmark mark='a'/>1929年10月，十个交易日下跌{100 * abs(w0['ret']):.0f}%；1987年10月；2008年10月；1940年5月，法国沦陷之时；"
        "以及2020年3月。<bookmark mark='b'/>每一个都约为十日VaR {scaled:.1f}%的三倍：这些是压力测试必须扛住的情景，而99%的数字本来就不是为容纳它们而设计的。",

    "Regulators turned scenarios into policy.":
        "监管机构把情景变成了政策。<bookmark mark='a'/>自2009年美国首次监管压力测试以来，它们每年发布严峻情景，并追问银行能否在其中保持足够的资本。"
        "<bookmark mark='b'/>情景是宏观路径加上市场冲击，结果决定资本缓冲并限制分红。<bookmark mark='c'/>但委员会选定的情景只能检验有人想象到的东西，而下一次危机通常是另一种。",

    "Reverse stress testing, as a formula.":
        "反向压力测试，写成公式。<bookmark mark='a'/>找到以协方差本身的度量衡量、离中心最近、恰好让组合亏损L的因子变动。<bookmark mark='b'/>拉格朗日条件使它与sigma乘w成比例："
        "每个因子按其与组合的协方差成比例地变动。<bookmark mark='c'/>它的距离等于损失除以组合的标准差。",

    'f"For the portfolio, whose daily standard deviation':
        "对这个日标准差为{100 * s['sd_daily']:.2f}百万美元的组合。<bookmark mark='a'/>要亏一千万，最合理的一天是市场下跌{100 * abs(r10['x'][0]):.1f}%，"
        "两个倾斜因子小幅下跌，距离{r10['distance']:.1f}个标准差。<bookmark mark='b'/>对照历史：1987年亏得更多，距离也是两倍多。公式找到的是通往一个损失的最便宜路线；"
        "历史表明，危机走的是昂贵的路线，让协方差认为不应一起变动的因子一起变动。",

    'f"And the dual question.':
        "还有对偶问题。<bookmark mark='a'/>Gerold Studer的最大损失：在k个标准差以内的所有情景中的最坏损失，对线性组合等于k乘以组合自身的标准差。"
        "<bookmark mark='b'/>取三，约为{3 * 100 * s['sd_daily']:.1f}百万。<bookmark mark='c'/>有期权时损失是弯曲的，椭球上的最坏点必须靠在椭球上处处对组合重新估值来找到。",

    "What stress tests leave out.":
        "压力测试遗漏了什么。<bookmark mark='a'/>在危机中，定义合理性的协方差本身就不一样了。<bookmark mark='b'/>单日情景假设组合能按冲击后的价格平仓。"
        "<bookmark mark='c'/>被迫卖出的人会让价格进一步变动，这就是第41部分的螺旋，任何静态情景都装不下它。",

    "Pause and predict. Three losses each have a ninety-nine percent VaR of nine":
        "暂停并预测。三个损失的99% VaR都是九，尾部为指数二的帕累托。对它们之间如何相依一无所知。它们之和的99% VaR最大可以是多少？",

    # ------------------------------------------------------------------ Uncertainty
    "f'Chapter seven, and the answer to the pause:":
        "第7章，以及暂停问题的答案：约{r['worst_lo']:.0f}。不是二十七，即三个VaR之和，也就是完全相依时给出的数，而是它的约{r['worst_lo'] / r['comonotonic']:.1f}倍。"
        "在厚尾下，对VaR最坏的相依结构并不是所有东西一起变动的那一种。",

    "The problem. <bookmark mark='a'/> Each loss's own distribution":
        "问题。<bookmark mark='a'/>每个损失自己的分布可以用它自己的数据估计。<bookmark mark='b'/>它们之间如何相依，尤其在尾部，往往无法估计。<bookmark mark='c'/>"
        "所以要求出在所有可能的相依结构下，总和的最坏VaR：一个无论Copula如何都成立的界。",

    "The algorithm. <bookmark mark='a'/> Discretise each loss's tail":
        "算法。<bookmark mark='a'/>把每个损失在alpha之外的尾部离散为N个分位数，每个损失一列。<bookmark mark='b'/>Paul Embrechts、Giovanni Puccetti和Ludger "
        "Rüschendorf的重排算法：把每一列按与其他列之和相反的顺序排列，重复直到不再变化。<bookmark mark='c'/>各行之和变得尽可能相等，其中最小的就是最坏的VaR。",

    "Six quantiles of three Pareto losses,":
        "三个帕累托损失的六个分位数，看它如何运作。<bookmark mark='a'/>开始时每一列的顺序都相同：同单调的情形，最小的行和等于三个VaR之和。<bookmark mark='b'/>"
        "每一轮都让一列对着其他列重新排序。<bookmark mark='c'/>大的数值分散到各行，行和趋于均衡，其中最小的那个上升：这就是最坏情形的VaR。",

    'f"The numbers, for three losses at ninety-nine percent.':
        "三个损失在99%下的数字。<bookmark mark='a'/>尾部指数为三时，独立给出{a['independent']:.1f}，完全相依给出{a['comonotonic']:.1f}，最坏情形为"
        "{a['worst_lo']:.1f}。<bookmark mark='b'/>尾部越厚差距越大：指数为一点五时，最坏情形是VaR之和的{b['worst_lo'] / b['comonotonic']:.1f}倍。"
        "把VaR相加，许多公司在不同风险类型之间就是这么做的，并不是一个安全的上界。",

    "Expected shortfall is better behaved again.":
        "预期亏损再一次表现得更好。<bookmark mark='a'/>因为它是次可加的，并且在损失同向变动时恰好可加，它在所有相依结构下的最坏情形就是各自预期亏损之和。"
        "<bookmark mark='b'/>又因为VaR从不超过ES，这个和也界定了最坏的VaR。一致性换来了一个可用的界。",

    "Where this bites.":
        "这在哪里起作用。<bookmark mark='a'/>在不同风险类型之间，市场、信用和操作损失分开测量再合并；相加假设完全相依，而对VaR这仍可能低估。<bookmark mark='b'/>"
        "在不同交易台之间，公司的VaR需要一个联合模型，它的分散化收益是真实的，但取决于那个模型。<bookmark mark='c'/>所以本系列公司在报告VaR时，把相依性界一并列出。",

    'f"And even with the model right, there is estimation error.':
        "即使模型正确，也还有估计误差。<bookmark mark='a'/>经验分位数的标准误等于二项标准误除以密度，而尾部的密度很低。<bookmark mark='b'/>对五百个正态日的历史模拟"
        "99% VaR，约为VaR本身的{100 * se / z:.0f}%。<bookmark mark='c'/>预期亏损平均最糟的五个点，噪声更大，厚尾会让两者都更糟。",

    "Model risk, from the public record.":
        "来自公开记录的模型风险。<bookmark mark='a'/>2012年1月，摩根大通首席投资办公室把其合成信用组合换到一个新的VaR模型，报告的数字大约减半，银行自己的工作组和"
        "美国参议院的报告后来都描述了这一点。<bookmark mark='b'/>报告描述了一个在电子表格中运行的模型，有手工复制，还有一个用总和代替平均值做除数、压低了波动率的公式。"
        "<bookmark mark='c'/>据报道，这个组合那一年亏损约六十二亿美元。一个降低风险的模型变更，恰恰最需要独立审查。",

    "Pause and predict. A neural network is trained to forecast":
        "暂停并预测。一个神经网络用1926到1990年的数据，根据近期波动率预测明天美国收益的百分之一分位数。在此后的三十年里，它能胜过一个经GARCH过滤的预测吗？",

    # ------------------------------------------------------------------ Learned
    'f"Chapter eight, and the answer to the pause: no.':
        "第8章，以及暂停问题的答案：不能。在1990年之后的三十年里，网络的弹球损失为{m['network']['pinball']:.2f}，而GARCH过滤预测为{m['gjr_fhs']['pinball']:.2f}，"
        "网络在{100 * m['network']['rate']:.2f}%的日子里被突破，Kupiec检验拒绝了它。一个学习分位数的模型不得不重新发现波动率聚集，而它做得不如本来就建立在它之上的模型。",

    "How to train a quantile.":
        "如何训练一个分位数。<bookmark mark='a'/>弹球损失在一侧按tau、另一侧按一减tau惩罚预测。<bookmark mark='b'/>它的期望值在真实分位数处最小，研究者章节会证明这一点。"
        "<bookmark mark='c'/>所以任何明天百分之一分位数的模型，都可以用平均弹球损失来拟合，并与其他模型比较。",

    'f"Robert Engle and Simone Manganelli\'s CAViaR.':
        "Robert Engle和Simone Manganelli的CAViaR。<bookmark mark='a'/>分位数本身对昨天的分位数和昨天的绝对收益做自回归。<bookmark mark='b'/>用1926到1990年拟合，"
        "它保留昨天分位数的{100 * b[1]:.0f}%。<bookmark mark='c'/>不假设任何分布：它直接按弹球损失拟合。",

    "And a quantile network.":
        "还有一个分位数网络。<bookmark mark='a'/>五个在前一天晚上已知的特征：波动率、昨天的变动、绝对收益的短期和长期平均，以及昨天的损失。<bookmark mark='b'/>"
        "十六个隐藏单元，刻意保持很小，因为百分之一分位数每十年只见到几百个尾部日子。<bookmark mark='c'/>用弹球损失训练到1990年，然后冻结，在此后的三十年里检验。",

    'f"The test.':
        "检验。<bookmark mark='a'/>GARCH过滤预测的弹球损失最低，{m['gjr_fhs']['pinball']:.2f}，例外出现在{100 * m['gjr_fhs']['rate']:.2f}%的日子里。"
        "<bookmark mark='b'/>CAViaR接近，{m['caviar']['pinball']:.2f}，并通过了两项回测。<bookmark mark='c'/>网络更差，{m['network']['pinball']:.2f}，被突破得太频繁；"
        "而普通的历史模拟法，{m['hs']['pinball']:.2f}，远远落在所有方法之后。",

    "Through the crisis.":
        "穿越危机。<bookmark mark='a'/>随着2008年9月波动率上升，三个预测都随收益下降。<bookmark mark='b'/>网络反应最慢，又恢复得太快：它从过去学到的是波动率的平均速度，"
        "而GARCH的过滤器对每一天作出即时反应。",

    'f"Is the difference real?':
        "差异是真实的吗？<bookmark mark='a'/>对每日弹球损失做Diebold–Mariano检验：网络对GARCH，t为{a['t']:.1f}；CAViaR，{b['t']:.1f}。<bookmark mark='b'/>"
        "两者都输了，但都没有在百分之五的水平上被拒绝。三十年的百分之一分位数几乎不足以区分好的模型，这本身就是这一章和第3章的教训。",

    "Why it lost.":
        "它为什么输。<bookmark mark='a'/>结构早已知道：日风险主要是波动率聚集和非对称性，GJR-GARCH用寥寥几个参数就把它们建了进去。<bookmark mark='b'/>尾部数据稀缺："
        "六十五年的训练里只有约六百五十个尾部日子。<bookmark mark='c'/>而1990年之后世界变了；会重新估计的过滤器能适应，冻结的网络不能。",

    "What would do better.":
        "什么能做得更好。<bookmark mark='a'/>更好的输入：隐含波动率和日内已实现度量携带日收益没有的信息。<bookmark mark='b'/>学习残差：让网络调整GARCH的预测，而不是取代它。"
        "<bookmark mark='c'/>以及用研究者章节推导的联合评分，把VaR和ES一起打分。",

    "Pause and predict. A ten-day ninety-seven and a half percent":
        "暂停并预测。一个大盘股组合的十日97.5%预期亏损为一千一百万美元。在巴塞尔的FRTB下，一个十日预期亏损相同的信用利差组合被假定需要四十天才能退出。"
        "规则对它意味着什么？",

    # ------------------------------------------------------------------ FRTB
    'f"Chapter nine, and the answer to the pause: twice as much.':
        "第9章，以及暂停问题的答案：翻倍。FRTB把十日预期亏损乘以流动性期限除以十的平方根，所以四十天使它翻倍：在这个组合上，从{hz[10]:.1f}变为{hz[40]:.1f}百万美元。"
        "规则的想法是对的，即不流动的头寸风险更大；它的平方根，正是第1章质疑过的假设。",

    "Three generations of rules.":
        "三代规则。<bookmark mark='a'/>1996年，银行可以用自己的99%十日VaR计算资本，至少乘以三，由红绿灯监督。<bookmark mark='b'/>危机之后，巴塞尔2.5加入了在一年动荡时期"
        "上测量的压力VaR。<bookmark mark='c'/>以及2016年起的交易账户根本性审查：97.5%的预期亏损、流动性期限、逐个交易台的审批，至今仍在分阶段实施。",

    "FRTB's measure.":
        "FRTB的度量。<bookmark mark='a'/>97.5%的预期亏损，对正态分布与99% VaR相同，尾部厚时更大。<bookmark mark='b'/>流动性期限通过级联进入：退出所需时间更长的因子"
        "在更长的期限上受冲击，各部分以平方和的平方根合并。<bookmark mark='c'/>预期亏损按一个压力年份校准，仿佛银行最糟的一年正在此刻发生。",

    'f"The horizons, roughly as the rules set them.':
        "期限，大致按规则的设定。<bookmark mark='a'/>大盘股和主要货币为十天：在一亿美元的组合上为{hz[0]['es']:.1f}百万。<bookmark mark='b'/>主权信用为四十天，"
        "{hz[2]['es']:.1f}；流动性最差的信用为一百二十天，{hz[-1]['es']:.1f}。同样的价格风险，如果需要四个月才能卖掉，所需资本就是三倍半。",

    "How the stress enters.":
        "压力如何进入。<bookmark mark='a'/>一组精简风险因子在压力年份上的预期亏损，再乘以今天全集与精简集预期亏损之比。<bookmark mark='b'/>之所以要精简集，是因为今天的许多"
        "因子在压力年份里没有价格；要让这种放大可信，精简集必须解释今天大部分的风险。",

    "And who may use a model.":
        "谁可以使用模型。<bookmark mark='a'/>每个交易台必须通过自己的VaR回测和一项损益归因检验。<bookmark mark='b'/>归因检验问风险模型的损益是否跟得上前台的损益："
        "漏掉一个因子就会让两者分道扬镳。<bookmark mark='c'/>真实价格太少的因子另收一笔压力资本，不计入预期亏损。",

    'f"Liquidity in the number itself.':
        "把流动性放进数字本身。<bookmark mark='a'/>Anil Bangia及合作者的流动性调整VaR加上穿越半个压力价差的成本。<bookmark mark='b'/>在一亿美元、价差十个基点的组合上，"
        "VaR从{q['var_m']:.2f}升到{q['lvar']:.2f}百万：对流动的组合影响很小。退出大额头寸更大的成本来自冲击。",

    'f"Part thirty-seven\'s square root again.':
        "又是第37部分的平方根。<bookmark mark='a'/>相对日成交量V卖出数量Q，成本约为一天的波动率乘以根号Q除以V。<bookmark mark='b'/>一个占日成交量五分之一的头寸，"
        "卖出要花掉{add:.2f}天的波动率，<bookmark mark='c'/>相当于99% VaR的五分之一，而在危机中成交量萎缩、波动率上升。流动性风险不是一个修正项；对大的组合，它是第二种风险。",

    "Risk numbers also set margin.":
        "风险数字也决定保证金。<bookmark mark='a'/>清算所的初始保证金就是一个VaR：在了结违约方头寸所需的天数内99%或99.5%的损失，即第21部分的清算。<bookmark mark='b'/>"
        "但一个反应迅速的VaR，正如第3章所建议的，会在崩盘中途提高追加保证金，迫使卖出：顺周期性，据报道在2020年3月清晰可见。<bookmark mark='c'/>所以规则加入了下限、"
        "在压力中释放的缓冲，以及每个窗口里都包含的压力数据：一个经过调和、不放大自己所测之物的预测。",

    "Pause and predict. The House's evening risk report":
        "暂停并预测。本系列公司的晚间风险报告列出了99%的单日VaR。为了让读者能够判断它，旁边还应该放哪三个数字？",

    # ------------------------------------------------------------------ House
    "The answer to the pause. <bookmark mark='a'/> First, the expected shortfall:":
        "暂停问题的答案。<bookmark mark='a'/>第一，预期亏损：坏日子有多坏。<bookmark mark='b'/>第二，回测：例外次数、它们是否扎堆，以及预期亏损检验。<bookmark mark='c'/>"
        "第三，压力：最糟的历史与反向压力损失，以及这个数字有多少取决于所假设的相依性。",

    "Chapter ten. The House's fortieth rule":
        "第10章。本系列公司的第40条规则属于它的风险部门，它现在为每一个交易台出报告。它像本系列对待每一个收益那样对待每一个风险数字：当作一个需要检验的预测。",

    "The first sheet. <bookmark mark='a'/> A normal VaR exceeded":
        "第一张汇总表。<bookmark mark='a'/>一个被突破次数是承诺两倍、预期亏损检验深陷红区的正态VaR，以及一个通过检验的GARCH过滤VaR。接近五的尾部指数。比高斯Copula"
        "允许的常见得多的共同崩盘。一个八个标准差之外的一千万美元亏损日。一个比VaR之和高出百分之七十的相依性最坏情形。还有一个没能胜过过滤器的学习模型。",

    "So the House's evening report has a shape.":
        "于是本系列公司的晚间报告有了固定的形态。<bookmark mark='a'/>VaR，旁边是预期亏损。<bookmark mark='b'/>预测者自己的业绩记录：被突破的频率、例外是否扎堆，"
        "以及预期亏损检验。<bookmark mark='c'/>压力损失、相依性界，以及退出的成本。只看第一行的读者知道得最少。",

    "And around it.":
        "以及它的周围。<bookmark mark='a'/>风险部门向董事会汇报，而不是向它所测量的交易台汇报。<bookmark mark='b'/>每个模型在上线前后都由没有参与建模的人验证。"
        "<bookmark mark='c'/>交易台的限额按预期亏损和压力损失设定，而VaR的例外则充当模型已经漂移的警报。",

    "What the rule means for the House's desks.":
        "这条规则对本系列公司各交易台意味着什么。<bookmark mark='a'/>波动率交易台和做市交易台持有负伽马和存货：它们的VaR需要完全重新估值，并把波动率作为风险因子。"
        "<bookmark mark='b'/>统计套利和系统化组合在相关性变化之前看起来是分散的：它们需要尾部相依和反向压力测试。<bookmark mark='c'/>数字资产交易台的交易场所和稳定币敞口"
        "是压力项目，有各自的限额，不计入VaR。",

    "Chapter three's timing test.":
        "第3章的时间检验。统计相邻两天的四种组合：平静接平静、平静接例外，依此类推，再比较例外之后出现例外的概率与平静之后出现例外的概率。",

    "Chapter four in two lines:":
        "两行代码概括第4章：拟合的广义帕累托尾部的分位数，以及它的预期亏损。",

    "Chapter six's reverse stress test:":
        "第6章的反向压力测试：组合的方差、与sigma乘w成比例的情景，以及它的距离。",

    "And Chapter seven: for each column,":
        "还有第7章：对每一列，求其他列之和，再把这一列重新排序，使它与之反向。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>预测、回测，以及尾部与不确定性。<bookmark mark='b'/>还有第40条规则。本系列公司报告的每一个风险数字都是一个预测，"
        "并附上它自己的回测。预期亏损与VaR并列。每份报告都附上模型看不见的压力损失和相依性界。",

    "The rule against three cases.":
        "用三个案例检验这条规则。<bookmark mark='a'/>一个一年内没有例外的VaR模型：问它是好，还是只是保守，并看十年而不是一年。<bookmark mark='b'/>一个分散化之后风险下降的组合："
        "问所用的度量是不是VaR，以及新头寸是不是恰好位于它的分位数之外。<bookmark mark='c'/>一个用高斯Copula建模的信用组合：要它的共同超越，并问相依性界会怎么说。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter three backtested VaR":
        "写给研究者。第3章靠计数回测VaR，而预期亏损只能借助VaR回测。本章证明其中的原因：VaR是可引出的，预期亏损不是，而两者合在一起是。随后在构造的分布上、"
        "在模拟的尾部上、在九十年的美国收益上检验每一个结论。",

    "The idea, from Tilmann Gneiting.":
        "这个思想来自Tilmann Gneiting。<bookmark mark='a'/>评分函数对照实际发生的结果给预测打分，分数越低越好。<bookmark mark='b'/>如果在真实分布下，报告泛函T的真实值"
        "平均得分最好，评分函数就对T是一致的。<bookmark mark='c'/>如果存在某个严格一致的评分，T就是可引出的。只有这样，才能按平均得分公平地给预测者排名。",

    "Lemma one: the pinball loss elicits the quantile.":
        "引理一：弹球损失引出分位数。<bookmark mark='a'/>把它的期望写成积分。<bookmark mark='b'/>对q求导：斜率等于低于q的概率减去tau。<bookmark mark='c'/>期望是凸的，"
        "其斜率恰好在tau分位数处为零。所以VaR是可引出的，第8章的比较是公平的。",

    "Lemma two, a necessary condition due to Kent Osband.":
        "引理二，Kent Osband给出的一个必要条件。<bookmark mark='a'/>如果两个分布的某个可引出泛函取值相同，它们的每一个混合也取同样的值。<bookmark mark='b'/>证明："
        "混合分布下的期望得分是各自期望得分的混合。<bookmark mark='c'/>每一个都在t处取最小值，所以它们的混合也是，而严格一致性使t成为唯一的最小点。可引出的泛函具有凸的水平集。",

    "The theorem. <bookmark mark='a'/> Take a sure loss of one,":
        "定理。<bookmark mark='a'/>取一个确定损失为一的分布，以及一个以百分之五的概率损失二、否则为零的分布。在90%下，两者的预期亏损都恰好是一。<bookmark mark='b'/>"
        "把它们各半混合：最糟的百分之十现在包含百分之二点五的二和百分之七点五的一，预期亏损为一又四分之一。水平集不是凸的，所以由引理二，任何形式的评分都无法引出预期亏损。",

    'f"Check one: the level sets, computed.':
        "检验一：计算水平集。<bookmark mark='a'/>两个99% VaR相同、都是{mv['var'][0]:.0f}的分布，以及它们的混合：VaR仍然相同。<bookmark mark='b'/>定理中预期亏损相同、"
        "都是{me['es'][0]:.2f}的那一对，以及它们的混合：{me['es'][2]:.2f}。",

    "Why the pair might work.":
        "为什么这一对可能行得通。<bookmark mark='a'/>Ralph Rockafellar和Stanislav Uryasev的公式，来自第30部分：预期亏损是v加上超出v的部分的期望（按比例缩放）关于v的最小值。"
        "<bookmark mark='b'/>导数恰好在VaR处为零。所以预期亏损是附着在分位数上的一个值，一个同时看到两者的评分可以把两者都确定下来。",

    "The second theorem, by Tobias Fissler and Johanna Ziegel.":
        "第二个定理，来自Tobias Fissler和Johanna Ziegel。<bookmark mark='a'/>有一族评分对VaR和预期亏损的组合是严格一致的。Andrew Patton、Ziegel和Rui Chen从中挑出一个成员，"
        "FZ0，它不需要调参，也与单位无关。<bookmark mark='b'/>所以这一对是可引出的，尽管预期亏损单独不是：两者的预测都能被公平地排名。",

    "Half of the proof is short enough to show.":
        "证明的一半短到可以展示。<bookmark mark='a'/>把分位数固定在真实值，把FZ0的期望得分只看作预期亏损预测的函数。<bookmark mark='b'/>求导。<bookmark mark='c'/>"
        "导数在e等于v减去低于v的期望超出部分除以tau处为零，而在真实分位数下，这恰好是超出它的收益的均值：预期亏损。另一半，即分位数也必须正确，来自其中的弹球项。",

    'f"Check two: the score\'s minimum.':
        "检验二：评分的最小值。<bookmark mark='a'/>四十万天自由度为四的学生t分布，以及真实值周围网格上每一对预测的平均FZ0得分，越低越亮。<bookmark mark='b'/>"
        "最小值恰好落在真实的VaR和预期亏损上：{100 * f['v_hat']:.2f}%和{100 * f['e_hat']:.2f}%。",

    'f"Check three: ranking the forecasters of Chapter three by FZ zero,':
        "检验三：用FZ0给第3章的预测者排名，在97.5%下，从1928年起的每一天。<bookmark mark='a'/>GARCH过滤的历史模拟得分最好。<bookmark mark='b'/>其他每个预测者都更差，"
        "Diebold–Mariano统计量从{tmin:.1f}到{tmax:.1f}，{worst_name}垫底。联合评分给出的排序与回测相同，但每个预测者只用一个数字，还附带对差异的检验。",

    'f"Check four: what a VaR test misses.':
        "检验四：VaR检验漏掉了什么。<bookmark mark='a'/>四年自由度为三的学生t分布，用一个调到恰好使99% VaR正确的正态分布来预测。<bookmark mark='b'/>它的预期亏损预测"
        "{p['es_normal']:.2f}比真实的{p['es_true']:.2f}低四分之一。<bookmark mark='c'/>Kupiec检验的拒绝率为{100 * p['kupiec']:.1f}%：就是它的显著性水平，"
        "所以它什么也看不见。<bookmark mark='d'/>预期亏损检验的拒绝率为{100 * p['z2']:.0f}%：更好，但仍然很低。四年不足以看清一条尾巴。",

    "What this changes.":
        "这改变了什么。<bookmark mark='a'/>传统的回测问一个模型能否被拒绝，这是一个弱问题。<bookmark mark='b'/>Fissler、Ziegel和Gneiting，以及Natalia Nolde与Ziegel，"
        "提出了比较式回测：按联合评分，银行的模型是否比一个标准模型更差？<bookmark mark='c'/>一个建立在评分差异之上的红绿灯，之所以可能，只因为这一对是可引出的。",

    "A striking corollary.":
        "一个惊人的推论。<bookmark mark='a'/>期望分位数是分位数的最小二乘版本，按构造就是可引出的。<bookmark mark='b'/>Johanna Ziegel，以及Fabio Bellini与Valeria Bignozzi"
        "证明，在只取决于分布的一致性风险度量中，期望分位数是唯一可引出的。监管机构选择的预期亏损不在其中。",

    "Where this sits. <bookmark mark='a'/> The theory:":
        "这项工作的位置。<bookmark mark='a'/>理论：Osband、Gneiting、Fissler和Ziegel、Ziegel、Bellini和Bignozzi。<bookmark mark='b'/>实践：Patton、Ziegel和Chen的"
        "动态预期亏损模型、Acerbi和Székely的检验，以及Nolde和Ziegel的比较式回测。<bookmark mark='c'/>以及本系列：第7部分的QLIKE和第27部分的样本外R平方，分别是方差和"
        "均值的一致评分，是同一个原理。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>在一两年的数据上就有检验力、又不依赖强假设的预期亏损检验。<bookmark mark='b'/>哪些系统性风险度量，比如第41部分的CoVaR，是可引出的，"
        "用哪些评分。<bookmark mark='c'/>以及在这一对的众多一致评分中，哪一个能按模型出错时银行实际亏多少来给模型排名。",

    "Pause and predict. The mean is elicited by squared error.":
        "暂停并预测。均值由平方误差引出。方差能单独被引出吗？用引理二和两个点质量试一试。",

    # ------------------------------------------------------------------ Outro
    "Part forty in thirteen lines.":
        "用十三行回顾第40部分。在险价值是一个分位数：它说明多常发生，从不说明有多严重，而预期亏损是超出它之后的均值。时间平方根法则低估了十日风险。VaR不是次可加的；"
        "预期亏损是一致的。一个正态VaR被突破的次数是承诺的两倍，而且成簇出现，而一个GARCH过滤的VaR通过了检验。尾部是帕累托的，指数接近五。高斯Copula没有尾部相依，"
        "而市场有。",

    "The most plausible way to lose a given amount":
        "以给定金额亏损的最合理方式是一个公式，而历史走的是更昂贵的路线。未知的相依性可以把VaR推到远高于各部分之和。学习出来的分位数模型没有胜过GARCH过滤器。"
        "监管转向了带流动性期限的预期亏损，而流动性本身就是第二种风险。研究者章节证明了什么可以被回测。还有本系列公司的规则：风险数字是一个预测，要附上它的回测来报告。",

    "Three lessons. <bookmark mark='a'/> A risk number is a forecast,":
        "三条教训。<bookmark mark='a'/>风险数字是一个预测，可以像任何预测一样被检验，报告时应附上它的记录。<bookmark mark='b'/>先波动率，后尾部：大多数失败来自忽视聚集。"
        "<bookmark mark='c'/>模型看不见的东西，尾部相依、流动性和未见过的情景，应该放在数字旁边，而不是藏在数字里面。",

    "The part on one card.":
        "一张卡片上的这一部分。预期亏损的两种写法。Kupiec的似然比和Z2统计量。超阈值峰值法的分位数。t分布和高斯分布的尾部相依。最合理的压力情景。以及VaR和预期亏损的联合评分。",

    "How this part connects.":
        "这一部分如何与其他部分相连。<bookmark mark='a'/>往回看：第2部分的保证金、第7部分的波动率模型、第20部分的Copula、第30部分的CVaR和第37部分的冲击，都在风险报告中汇合。"
        "<bookmark mark='b'/>横向看：第26部分对策略的回测和这一部分对风险的回测是同一个思想。<bookmark mark='c'/>往前看：第41部分的危机，正是风险数字一起失灵的地方。",

    "Six desk questions. Ten-day VaR from one-day?":
        "六个交易台问题。由一日VaR得十日VaR？如果每天独立且正态，是根号十倍，在真实数据上更多。<bookmark mark='a'/>为什么VaR不是一致的？它不是次可加的。"
        "<bookmark mark='b'/>如何回测它？数例外，并检验它们的时间分布。",

    "Beyond the data? Extreme-value theory.":
        "超出数据之外？极值理论。<bookmark mark='a'/>相关性漏掉了什么？尾部相依。<bookmark mark='b'/>预期亏损能被回测吗？单独不能；和VaR一起可以。完整解答见讲义。",

    "The research chapter's pause, answered.":
        "研究者章节暂停问题的答案。<bookmark mark='a'/>不能：位于负一和正一的两个点质量方差都为零，而它们的等权混合方差为一，所以水平集不是凸的。<bookmark mark='b'/>"
        "但均值和二阶矩各自都能由平方误差引出，而方差是这一对的函数：与预期亏损和VaR的结构相同。",

    "And twelve problems: normal VaR and shortfall;":
        "还有十二道习题：正态VaR和预期亏损；自相关下的平方根；非次可加性；Kupiec与红绿灯；扎堆；一个极值分位数；尾部相依；反向压力；一个相依性界；以及流动性期限。"
        "然后是两道资格考试题：完整的可引出性，以及预期亏损检验的基础。中英文解答见讲义。",

    "Where this comes back. Part forty-one follows":
        "这些内容会在哪里再出现。第41部分追踪杠杆和流动性，走进风险数字一起失灵的危机。第42部分让机器在这里测量的风险上交易。第43部分追问，是否有人的收益付得起他们承担的风险。",

    "The textbooks this part follows, and the papers it draws on, from Kupiec's test":
        "这一部分所依据的教科书和论文，从Kupiec的检验到联合评分。屏幕上的每个数字，都是本系列公司的代码根据Kenneth French截至2020年的日收益（即研究窗口），或通过模拟算出来的。",

    "The House can now say how much it might lose,":
        "本系列公司现在能说出自己可能亏多少，也知道自己错了时该怎么发现。<bookmark mark='a'/>接下来，第41部分：杠杆、流动性与危机。银行挤兑、甩卖，以及每一个风险数字"
        "同时失灵的螺旋。",
}
