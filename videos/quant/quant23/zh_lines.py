"""Chinese narration for quant23: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 均值–方差前沿 (mean-variance frontier), 全局最小方差组合
(global minimum-variance portfolio), 切点组合 (tangency portfolio), 资本市场线 (capital market line), 分离定理 (separation
theorem), 证券市场线 (security market line), 押注低贝塔 (betting against beta), 随机贴现因子 (stochastic discount factor),
Hansen–Jagannathan界 (HJ bound), 套利定价理论 (APT), 跨期资本资产定价模型 (ICAPM), 欧拉方程 (Euler equation), 广义矩估计
(GMM), 股权溢价之谜 (equity premium puzzle), 无风险利率之谜 (risk-free rate puzzle), 习惯形成 (habit), 长期风险 (long-run
risk), 罕见灾难 (rare disasters), 事后理性价格 (ex post rational price), 过度波动 (excess volatility), 中介资产定价
(intermediary asset pricing), 需求弹性 (demand elasticity), 无弹性市场假说 (inelastic markets hypothesis), 套利的限制
(limits of arbitrage), 噪声交易者 (noise traders), 前景理论 (prospect theory), 处置效应 (disposition effect), 暴涨 (run-up),
理性泡沫 (rational bubble)."""

TITLE = '量化金融，从零搭建 · 第23部分：风险与收益'

CHAPTERS = {
    'Hook': '风险值多少',
    'Markowitz': '1. Markowitz：前沿',
    'Tobin': '2. 现金、切点组合与估计误差',
    'CAPM': '3. CAPM与那条平的线',
    'SDF': '4. 一个定价方程：贴现因子',
    'APT': '5. 多个因子：APT与ICAPM',
    'CCAPM': '6. 消费与GMM',
    'Puzzle': '7. 股权溢价之谜',
    'Shiller': '8. 价格波动太大',
    'Intermediary': '9. 中介机构为资产定价',
    'Inelastic': '10. 需求系统与无弹性市场',
    'Behaviour': '11. 行为与套利的限制',
    'Bubbles': '12. 泡沫',
    'House': '13. 第23条规则：研究交易台',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part twenty-three. Risk and return.":
        "第23部分。风险与收益。第三幕问的是东西必须值多少钱。第四幕问的是它们支付多少，以及为什么。",

    'f"A dollar put into the American stock market in July 1926':
        "1926年7月投入美国股市的一美元，股息再投资。<bookmark mark='a'/>到2025年底，它值大约{h['end_stocks'] / 1000:.1f}千美元。"
        "<bookmark mark='b'/>同样一美元投入一个月期国库券：大约{h['end_bills']:.0f}美元。一个世纪里，每年百分之十对百分之三。这个差距就是股权溢价，"
        "它是本部分的核心数字。它为什么这么大？它是对风险的报酬吗？如果是，是哪种风险？还是说，它是一个细心的投资者本可以利用的错误？",

    "Every theory in this part has the same shape.":
        "本部分的每个理论都有同样的形状。一个资产超过现金的预期收益，等于它对某种风险的暴露贝塔，乘以市场为这种风险收取的价格兰姆达。争论总是关于哪种风险："
        "市场的、消费的、银行资本的，还是根本没有风险。<bookmark mark='a'/>而它们每一个都是同一个方程的特例：任何东西的价格，都是它的支付乘以一个贴现因子的期望。"
        "到第四章我们就会得到它。",

    "How we got here.":
        "我们是怎么走到这里的。1952年，Harry Markowitz把分散化变成了数学；James Tobin加入了现金；William Sharpe等人推导出资本资产定价模型；"
        "Robert Merton和Stephen Ross允许多种风险。<bookmark mark='a'/>Robert Lucas从消费出发为资产定价，Robert Shiller表明价格的波动远超其背后的股息，"
        "Lars Hansen造出了检验这一切的工具，Rajnish Mehra和Edward Prescott发现，对任何合理的风险厌恶来说，股权溢价都太大了。"
        "<bookmark mark='b'/>然后是套利的限制、互联网泡沫、罕见灾难，以及最新的答案：中介机构的资产负债表和无弹性的需求决定价格。",

    "The plan: the frontier of risk and return":
        "本部分安排：推导风险与收益的前沿，以及为什么估计出来的前沿令人失望；资本资产定价模型，以及数据画出的那条平的线；这一切背后的那个方程，以及它对任何模型施加的界；"
        "消费，以及它解不开的谜；波动太大的价格；中介机构与无弹性市场；还有行为、套利的限制与泡沫。",

    "In the House, the research desk opens.":
        "在House里，研究交易台开张了。它的第一个产品不是一个策略，而是一个框架：任何头寸因其承担的风险，应当获得多少预期收益。",

    # ------------------------------------------------------------------ Markowitz
    "Chapter one. Harry Markowitz's frontier":
        "第一章。Harry Markowitz的前沿：哪些组合值得持有。",

    "Two assets, each with twenty percent volatility, one expected":
        "两个资产，波动率都是百分之二十，一个预期收益百分之六，另一个百分之十。<bookmark mark='a'/>把它们混合，随着权重变化描出混合组合的风险与收益。"
        "如果两者完全同步变动，这条线是直的：混合只改变收益，不改变风险。<bookmark mark='b'/>随着相关系数下降，这条线向左弯曲，到负一时它触及零风险。"
        "只要不是完全相关，总有某种混合比任何一个资产单独持有的风险都低；这个混合究竟在哪里，是本章结尾的问题。人们常引用Markowitz的话说，"
        "分散化是金融中唯一的免费午餐，原因就在这里。",

    "With many assets, ask the same question":
        "有许多资产时，对每个目标收益问同样的问题：在所有具有该预期收益、资金全部投入的组合中，哪个方差最小？<bookmark mark='a'/>拉格朗日函数一行就给出答案。"
        "最优权重只是两个组合的组合：协方差矩阵的逆乘以均值，以及协方差矩阵的逆乘以全一向量。每个有效组合都是同样两只基金的混合。"
        "<bookmark mark='b'/>而方差作为目标收益的函数是一条抛物线；在均值和波动率的平面上是一条双曲线。投资者叫它子弹。",

    "One portfolio on the frontier is special":
        "前沿上有一个组合很特别：它的鼻尖，全局最小方差组合。它的权重只需要协方差矩阵，一个预期收益都不需要。这一点很重要，因为协方差的估计比均值精确得多，"
        "下一章会展示均值估错时会发生什么。",

    'f"Now real assets: ten American industries':
        "现在换成真实资产：十个美国行业，1990年以来的月度数据。<bookmark mark='a'/>每个行业单独是一个点。<bookmark mark='b'/>由它们构造的前沿："
        "每个行业都远在前沿以内，因为每个行业单独承担着混合可以分散掉的风险。<bookmark mark='c'/>最小方差组合的波动率为百分之{100 * gm['sd']:.0f}，"
        "低于任何单个行业，也低于市场本身。",

    "But look at the weights the optimiser wants":
        "但看看优化器为它最好的组合要的权重。<bookmark mark='a'/>做空电信百分之三十，做多零售和公用事业各超过百分之四十，做空包罗万象的“其他”行业超过一半。"
        "这些不是对行业的洞见。它们是优化器在追逐平均收益中的微小差异，而这些平均收益的测量误差巨大：三十一年的平均收益，标准误仍然约为每年两个半百分点。"
        "Markowitz的机器在最大化收益的同时，也最大化了误差。",

    "Two assets, each with twenty percent volatility, correlation one half.":
        "两个资产，波动率都是百分之二十，相关系数一半。最小方差权重是多少，它的波动率是多少？",

    # ------------------------------------------------------------------ Tobin
    "Chapter two. Add a riskless asset":
        "第二章。加入一个无风险资产，前沿就变成一条直线。",

    "Now add a riskless asset: cash, earning the bill rate.":
        "现在加入一个无风险资产：现金，赚取国库券利率。任何风险组合与现金的混合，都沿着一条从国库券利率出发的直线移动。最好的那条线最陡，"
        "它在一个组合处与子弹相切，那就是切点组合。<bookmark mark='a'/>James Tobin的分离定理随之而来：使用相同估计的每个人都持有同一个风险组合，即切点组合，"
        "区别只在于旁边放多少现金。这条线的斜率，就是这些资产能提供的最大夏普比率。谨慎的投资者把三分之一的钱放在切点组合、其余放在国库券；大胆的投资者借钱，"
        "持有相当于自己资本一点五倍的切点组合。两人持有的股票相同、比例也相同。选择组合与选择风险是两个独立的决定，这就是一只基金能服务于它从未见过的投资者的原因。",

    'f"Draw it on the industries.':
        "在行业上画出来。<bookmark mark='a'/>从国库券利率出发把一条线向上转，直到它刚好碰到前沿。<bookmark mark='b'/>这就是资本市场线，切点就是切点组合，"
        "夏普比率为{t['sharpe']:.2f}。股票市场本身为{f['mkt_sharpe']:.2f}，位于前沿以内：在这个样本里，一个行业组合本可以轻松击败它。"
        "但事先能做到吗？",

    'f"Test it honestly.':
        "老老实实地检验一下。用1990到2007年拟合切点组合，然后从2008年持有这些权重到2020年，即研究窗口的终点。<bookmark mark='a'/>样本内，它的夏普比率是{o['in_sharpe']:.2f}。"
        "样本外它只有{o['oos_sharpe']:.2f}，不如市场的{o['mkt_sharpe']:.2f}，不如简单地等额持有十个行业的{o['eq_sharpe']:.2f}，"
        "也不如从未看过一个平均收益的最小方差组合的{o['gmv_sharpe']:.2f}。<bookmark mark='b'/>Victor DeMiguel、Lorenzo Garlappi和Raman Uppal在许多数据集上"
        "发现了同样的结果：估计均值的误差淹没了优化的收益。这是量化投资的第一课，第三十部分会回到这里。",

    "Practitioners have three remedies":
        "从业者有三种补救办法，第三十部分会认真讲。<bookmark mark='a'/>收缩估计：把各个均值拉向彼此，把协方差拉向一个简单的结构。<bookmark mark='b'/>约束权重；"
        "Ravi Jagannathan和Tongshu Ma证明，禁止卖空的作用类似于收缩。<bookmark mark='c'/>或者从均衡出发：Fischer Black和Robert Litterman从能使市场组合"
        "成为最优的预期收益开始，这正是下一章的思想。",

    "A mean return is estimated from thirty years":
        "一个平均收益用三十年、波动率百分之十八的数据估计。它的标准误是多少？要多少年才能减半？",

    # ------------------------------------------------------------------ CAPM
    "Chapter three. The capital asset pricing model":
        "第三章。资本资产定价模型：如果每个人都持有切点组合会推出什么，以及数据说的是什么。",

    "Suppose everyone uses the same estimates.":
        "假设每个人都使用相同的估计。那么每个人都持有同一个风险组合，而每一股都必须有人持有，所以这个组合就是市场本身。<bookmark mark='a'/>"
        "切点条件于是对每个资产都给出一个结论：它的预期超额收益与它和市场的协方差成正比。<bookmark mark='b'/>除以市场的方差，就得到William Sharpe、John Lintner"
        "和Jan Mossin的资本资产定价模型：一个资产赚取它的贝塔乘以市场溢价。只有市场风险得到报酬。能被分散掉的风险，无论多大，都一无所得。",

    "The model makes one sharp prediction.":
        "这个模型做出一个尖锐的预测。把每个组合的平均超额收益对它的贝塔作图，这些点应当落在一条过原点的直线上，斜率等于市场溢价：证券市场线。"
        "<bookmark mark='a'/>Fischer Black、Michael Jensen和Myron Scholes在1972年按贝塔给股票排序来检验它。结果这条线太平了。二十年后，Eugene Fama"
        "和Kenneth French发现它几乎是平的。",

    "Before testing the line, a word on how betas are measured":
        "检验这条线之前，先说说贝塔是怎么测的，因为单只股票的贝塔噪声很大。一只特质波动率为百分之三十的股票，用五年月度收益对波动率百分之十五的市场估计，"
        "其贝塔的不确定性约为正负四分之一。<bookmark mark='a'/>把平均收益对这样含噪声的贝塔做回归，斜率会偏向零，这是经典的变量误差问题。所以Fischer Black、"
        "Michael Jensen和Myron Scholes，以及后来的Fama和MacBeth，都按贝塔把股票分成组合：一百只股票的组合，其贝塔几乎可以精确测出，"
        "所以组合之间的平线不能归咎于噪声。<bookmark mark='b'/>从业者还会收缩。Marshall Blume发现贝塔会向一漂移，所以终端屏幕上的调整贝塔是估计值的三分之二"
        "加三分之一。Oldrich Vasicek的贝叶斯版本按每只股票自身估计的不确定程度来收缩。",

    'f"Here it is on sixty-two years of data':
        "这是五十七年的数据：按贝塔排序的十个组合，贝塔从{b[0]:.1f}到{b[-1]:.1f}。<bookmark mark='a'/>模型的线：过原点，每单位贝塔以市场溢价"
        "每年百分之{100 * c['mkt_prem']:.0f}上升。<bookmark mark='b'/>数据的线：截距百分之{100 * s['intercept']:.1f}，斜率{100 * s['slope']:.1f}，"
        "不到预测的一半。最安全的股票赚得远比模型允许的多，最有风险的股票只比平均水平多赚一点。",

    'f"If the line is flat, there is a trade.':
        "如果这条线是平的，就有一笔交易。把贝塔最低的组合加杠杆到贝塔为一，把最高的去杠杆到一，做多前者、做空后者。<bookmark mark='a'/>在这些十分位组合上，"
        "它每年赚百分之{100 * c['bab_mean']:.1f}。Andrea Frazzini和Lasse Pedersen称之为押注低贝塔，并给出了一个理由：许多投资者不能借钱，所以为了更高的收益，"
        "他们买风险更高的股票而不是给安全的股票加杠杆，从而把它们的价格抬高。Fischer Black在1972年就提出过同样的看法。",

    "Richard Roll pointed out in 1977":
        "Richard Roll在1977年指出，CAPM等价于一个命题：市场组合是有效的。而模型里的市场是全部财富：股票、债券、房屋，以及人们未来收入的价值，"
        "后者没有人能观测到。每一次用股票指数做的检验，检验的都只是这个指数是否有效，仅此而已。这个模型也许无法检验；但它在股票指数上的失败不是假的。",

    "A stock has a beta of one point five":
        "一只股票的贝塔为一点五，特质波动率百分之六十；市场溢价为百分之六。它应当比现金多赚多少？为什么那百分之六十无关紧要？",

    # ------------------------------------------------------------------ SDF
    "Chapter four. The single equation":
        "第四章。每一个风险与收益模型背后的那个方程。",

    "Here is the equation. The price of any payoff":
        "方程是这样的。任何支付的价格，都是这个支付乘以一个随机贴现因子m的期望；在一美元最值钱的那些世界状态里，m很大。第九部分证明了，只要没有套利，"
        "这样的m就存在。<bookmark mark='a'/>对一个收益率，价格是一；对一个超额收益，价格是零。<bookmark mark='b'/>所以任何东西的预期超额收益，"
        "等于它与贴现因子的协方差的相反数。在坏时候、在m高的时候赚钱的资产是保险，赚得少。在好时候赚钱的资产必须提供更多。风险溢价关乎你什么时候拿到钱，"
        "而不是支付波动多大。",

    "Every model in this part is a choice of m.":
        "本部分的每个模型都是对m的一种选择。<bookmark mark='a'/>如果m是市场收益的线性函数，就得到CAPM。<bookmark mark='b'/>如果它是消费增长的某次幂，"
        "就是消费模型。<bookmark mark='c'/>如果它是某些因子的线性函数，就是第二十四部分研究的那类因子模型。<bookmark mark='d'/>如果它是一美元对做市交易商的价值，"
        "就是第九章的中介模型。方程永远是同一个；经济学在m里。",

    "This equation is an old friend in new clothes.":
        "这个方程是换了新衣服的老朋友。贴现因子的期望是一除以无风险总收益，所以把m除以它的均值，就得到一个概率密度。<bookmark mark='a'/>用它给真实世界的概率加权，"
        "就得到第四和第九部分的风险中性测度，在它之下每个价格都是一个贴现的期望。衍生品交易台和研究交易台用的是同一个对象：一个叫它Q，另一个叫它m。"
        "Q只是把概率向一美元最值钱的那些状态倾斜。<bookmark mark='b'/>所以风险溢价就是两个期望之间的差距：真实世界的期望与风险中性的期望。期权价格揭示后者；"
        "历史估计前者。第十二部分的方差风险溢价，正是针对波动率测出的这个差距。",

    "The equation has a powerful consequence.":
        "这个方程有一个强有力的推论。把超额收益版本写成均值之积加上一个协方差，再把协方差写成相关系数乘以两个波动率。<bookmark mark='a'/>相关系数至多为一，"
        "所以贴现因子的波动率相对于其均值，至少要等于夏普比率。Lars Hansen和Ravi Jagannathan在1991年用它一次检验整类模型：不管你的m是什么，它至少要这么波动。",

    'f"So how volatile must m be?':
        "那么m必须多波动？<bookmark mark='a'/>1963年以来，市场单独的夏普比率约为每年{h['sr_mkt']:.2f}。十个行业最优组合为{h['sr_ind']:.2f}。"
        "二十五个按规模和价值排序的组合，样本内为{h['sr_ff25']:.2f}；用前一半拟合、在后一半持有，仍有{h['sr_ff25_oos']:.2f}。"
        "<bookmark mark='b'/>任何能为这些资产定价的模型，都需要一个每年波动率至少为其均值一半、更可能接近其整个均值的贴现因子。这是一个非常波动的一美元边际价值。",

    "With gross returns the bound becomes a cup":
        "用总收益时，这个界变成一个杯子：对贴现因子每一个可能的均值，给出它所能有的最小波动率。<bookmark mark='a'/>现在试试最自然的贴现因子：消费增长的负伽马次幂。"
        "<bookmark mark='b'/>风险厌恶低时，它远在杯子下方：消费几乎不动，m也几乎不动。只有伽马超过约二十时它才碰到杯子，而那时它的均值已远低于一，"
        "这意味着利率远高于我们见过的任何水平。这就是画成图的股权溢价之谜，第六和第七章会把它拆开。",

    "An asset shows a Sharpe ratio of two.":
        "一个资产的夏普比率是二。这个界对任何能为它定价的模型说了什么？你首先会怀疑什么？",

    # ------------------------------------------------------------------ APT
    "Chapter five. Two ways to more than one risk factor":
        "第五章。通向多个风险因子的两条路：套利，与对冲。",

    "Stephen Ross took a different route in 1976.":
        "Stephen Ross在1976年走了另一条路。假设收益由少数几个共同因子驱动，再加上在资产之间几乎独立的噪声。<bookmark mark='a'/>那么有了许多资产，"
        "你就能构造一个对任何因子都没有暴露、噪声被分散掉的组合：几乎无风险。如果它赚得比现金多，就存在套利。所以预期收益必须近似地是因子贝塔的线性函数。"
        "套利定价理论完全不需要关于投资者的假设；但它不告诉你是哪些因子，也不告诉你它们支付多少。",

    "Here is the arbitrage in numbers, with one factor.":
        "用数字看这个套利，只有一个因子。两个充分分散的组合：A的贝塔为一，预期收益百分之八；B的贝塔为二，预期收益百分之十二。现金支付百分之三。"
        "<bookmark mark='a'/>持有两单位A、做空一单位B。权重之和为一，贝塔是二减二：零。预期收益是十六减十二，百分之四。<bookmark mark='b'/>"
        "一个无风险组合支付百分之四，而现金只付百分之三：以百分之三借钱买入它，不承担风险、不用自己的钱就赚一个百分点。交易者会一直这样做，"
        "直到A和B每单位贝塔的报酬相同，都是百分之五：B的价格下跌，直到它的预期收益为百分之十三。这就是APT的全部：每个充分分散的组合都必须落在关于贝塔的同一条直线上。",

    'f"Which factors? One answer is to let the data choose.':
        "哪些因子？一个答案是让数据来选。取四十九个行业，找出它们收益的主成分，就像第十八部分对收益率曲线所做的那样。<bookmark mark='a'/>"
        "第一个主成分解释了全部方差的百分之{100 * sh[0]:.0f}，它几乎就是市场：相关系数{a['corr_pc1_mkt']:.2f}。<bookmark mark='b'/>"
        "接下来的几个各自只增加几个百分点。股票收益有很强的因子结构，正如Ross所假设的。",

    'f"But do these components explain why some industries':
        "但这些主成分能解释为什么有些行业赚得比其他行业多吗？<bookmark mark='a'/>把行业的平均收益对它们在第一个主成分上的暴露做回归：R方几乎为零。"
        "三个主成分，仍然几乎为零；十个，{r2[-1]['r2']:.2f}。<bookmark mark='b'/>让收益一起变动的东西，不一定是投资者得到报酬的东西。Serhiy Kozak、"
        "Stefan Nagel和Shrihari Santosh认为，被定价的因子藏在那些小的主成分里，这就是为什么找到它们是第二十四和第二十五部分的难题。",

    "Robert Merton's intertemporal model gives the other route.":
        "Robert Merton的跨期模型给出另一条路。一个活很多期的投资者不仅关心自己的财富，还关心这些财富将遇到的机会：未来的利率、未来的预期收益、未来的波动率。"
        "在这些机会变差时赚钱的资产是一种对冲，就像保险一样，赚得更少。所以被定价的因子是市场，再加上任何能预测未来的东西；如果认真对待，这条规则能约束因子的搜寻。",

    "A factor explains forty percent of the variance":
        "一个因子解释了股票收益方差的百分之四十，却完全解释不了它们的平均收益。它是风险因子吗？什么会让它成为风险因子？",

    # ------------------------------------------------------------------ CCAPM
    "Chapter six. Pricing assets by what they do to consumption":
        "第六章。按资产对消费的影响来定价，并加以检验。",

    "Where does the discount factor come from in economics?":
        "在经济学里，贴现因子从哪里来？来自人。一个本可以今天多买一点某资产的投资者，放弃了这笔钱现在的效用，换来它将来支付的贴现期望效用。在最优处两者相等。"
        "<bookmark mark='a'/>所以贴现因子是边际效用之比，明天的比今天的：在幂效用下，就是消费增长的负伽马次幂，伽马是相对风险厌恶系数。一美元在消费下降的状态里最值钱。"
        "这就是Robert Lucas和Douglas Breeden的消费模型。",

    "With log-normal consumption the model gives two clean predictions.":
        "在对数正态消费下，这个模型给出两个清晰的预测。<bookmark mark='a'/>一个资产的溢价等于风险厌恶乘以它与消费增长的协方差：人们缩减开支时股票表现差，"
        "所以股票必须多付。而无风险利率等于不耐心，加上伽马乘以预期增长，再减去一个小的预防性项。同一个伽马必须同时解释两者。",

    'f"Now the data, every year since 1948.':
        "现在看数据，1948年以来的每一年。<bookmark mark='a'/>人均实际消费每年增长约百分之二，波动率只有百分之{100 * p['sd_dc']:.1f}：非常平滑。"
        "<bookmark mark='b'/>股票市场的实际收益波动率为百分之{100 * p['sd_rm']:.0f}，是它的九倍，而两者只是松散相关，相关系数{p['corr']:.2f}。"
        "消费下降时股票确实会跌，但消费几乎不下降。",

    "How do you estimate gamma without modelling the whole economy?":
        "不为整个经济建模，怎么估计伽马？Lars Hansen和Kenneth Singleton在1982年的洞见：欧拉方程必须对每一个收益、在每一个事先已知的状态下成立。"
        "把它的误差乘以今天已知的任何东西，平均值都应当为零。<bookmark mark='a'/>Hansen的广义矩估计，第六部分讲过，选择让这些平均值最接近零的参数；"
        "当条件多于参数时，它的J统计量检验这些条件能否同时成立。",

    'f"Fit it to the data.':
        "用数据拟合。<bookmark mark='a'/>风险厌恶约为{g:.0f}，标准误为{sg:.0f}：很大，而且几乎没有被确定下来。时间贴现因子贝塔为{b:.1f}："
        "大于一，仿佛人们看重未来甚于现在。<bookmark mark='b'/>这并非偶然。这么大的伽马会让人们拼命平滑不断增长的消费，这本应把利率推得很高；"
        "只有低于零的不耐心才能把利率压在我们看到的低水平上。Philippe Weil称之为无风险利率之谜。由于数据年份太少，J检验无法拒绝这个模型，但没有经济学家相信这些数字。",

    "Why does the same gamma that explains":
        "为什么能解释巨大股权溢价的同一个伽马，会预测出很高的无风险利率？",

    # ------------------------------------------------------------------ Puzzle
    "Chapter seven. The equity premium puzzle":
        "第七章。股权溢价之谜，以及它的三个答案。",

    'f"Put chapter six\'s numbers into the premium formula.':
        "把第六章的数字代入溢价公式。扣除通胀后，市场每年比国库券多付{100 * p['prem']:.1f}个百分点。它与消费的协方差是相关系数{p['corr']:.2f}乘以两个波动率："
        "一个极小的数。<bookmark mark='a'/>要让它们相符，伽马必须约为{p['gamma_implied']:.0f}。一个如此厌恶风险的人，会付出财富的百分之{pay:.0f}"
        "来避开一个赢或输百分之十的公平赌局：为了逃避一次抛硬币，几乎付出全部下行损失。几乎没有人是这样的。",

    "Rajnish Mehra and Edward Prescott put the puzzle":
        "Rajnish Mehra和Edward Prescott在1985年给出了这个谜的经典形式。一个仔细校准的Lucas经济，风险厌恶最高到十，最多只能产生每年三分之一个百分点的股权溢价。"
        "数据显示的是百分之六。而提高风险厌恶来弥补差距，又让无风险利率冲破屋顶。此后四十年的研究，很大程度上都是在试图回答他们。下面是三个最重要的答案。",

    "First, habits.":
        "第一，习惯。John Campbell和John Cochrane让效用取决于消费超出习惯水平的部分，而习惯水平缓慢地跟随过去的消费。<bookmark mark='a'/>"
        "当衰退把消费压向习惯水平时，盈余缩小，有效风险厌恶飙升。于是投资者恰恰在股票已经下跌时要求很高的溢价，这让价格波动、收益可预测，"
        "正如第八章将发现的那样，而核心的伽马并不大。",

    "Second, long-run risk.":
        "第二，长期风险。Ravi Bansal和Amir Yaron提出，消费增长包含一个很小但非常持久的成分，逐年几乎看不见，外加缓慢变化的波动率。在关心不确定性何时消解的偏好下，"
        "投资者害怕关于长期的消息，而股息暴露于其中的股票必须支付很高的溢价。困难在于，这个关键成分按其构造就很难测量。",

    'f"Third, disasters.':
        "第三，灾难。Thomas Rietz在1988年、Robert Barro在2006年都认为，平静国家的数据漏掉了罕见的灾难：战争、萧条、革命。Barro统计了二十世纪三十五个国家的灾难："
        "产出收缩百分之十五或以上，每年发生的概率约为百分之一点七，平均收缩百分之二十九。<bookmark mark='a'/>没有灾难时，风险厌恶为四只能给出六分之一个百分点的溢价。"
        "<bookmark mark='b'/>有了灾难，约为百分之{p29[k4]:.0f}；如果平均灾难有百分之四十那么深，则为{p40[k4]:.0f}。一个非常坏的结果的小概率，"
        "再取伽马次幂，就做到了平滑的消费做不到的事。",

    "Where does that leave us?":
        "那么我们处在哪里？<bookmark mark='a'/>溢价是对在坏时候承担风险的报酬，而季度消费太平滑，显示不出坏时候能有多坏。<bookmark mark='b'/>习惯、长期风险和灾难"
        "都能拟合平均溢价；它们在波动率、可预测性和市场期权价格上的预测不同，如今正是在这些地方检验它们。<bookmark mark='c'/>对投资者来说，教训是：对崩盘风险的溢价是真实的，"
        "它付给那些能撑过崩盘的人。",

    "In a disaster model with a two percent yearly chance":
        "在一个每年有百分之二的概率下跌百分之三十的灾难模型里，深度虚值的指数看跌期权定价会和没有灾难的模型有什么不同？",

    # ------------------------------------------------------------------ Shiller
    "Chapter eight. Robert Shiller's question":
        "第八章。Robert Shiller的问题：股价的波动是否大到无法用股息的消息来解释？",

    "Suppose a stock is worth its expected dividends":
        "假设一只股票的价值是它以固定利率贴现的预期股息。那么今天的价格，就是市场对某个事后可以算出来的东西的预测：实际到来的股息的现值，Shiller称之为事后理性价格，"
        "p星。<bookmark mark='a'/>理性预测的误差与预测本身不相关，所以p星的方差等于价格的方差加上误差的方差。因此价格必须比p星更平滑。"
        "一个预测永远不可能比它所预测的东西更波动。",

    'f"Here is Shiller\'s picture, updated':
        "这是更新后的Shiller的图，用Shiller公布的1871年以来的数据，经通胀和市场长期增长调整。<bookmark mark='a'/>实际支付的股息的现值是一条平滑、缓慢的线："
        "股息本身就没怎么变。<bookmark mark='b'/>价格围绕它摆动，经过1920年代的繁荣、1970年代的低迷、1990年代末的泡沫。它的标准差是{s['sd_p']:.2f}，"
        "而p星是{s['sd_pstar']:.2f}。如果价格是以固定贴现率对股息的理性预测，这就不可能发生。",

    "John Campbell and Shiller turned the observation into an identity.":
        "John Campbell和Shiller把这个观察变成了一个恒等式。用价格–股息比写出对数收益，并在其平均值附近线性化。<bookmark mark='a'/>向前迭代，"
        "今天的股息率就等于贴现的未来收益减去贴现的未来股息增长。这不是模型，而是会计，对任何资产都成立。<bookmark mark='b'/>所以股息率的方差必须恰好分成两部分："
        "关于未来收益的消息，和关于未来股息的消息。",

    'f"Measure the split on Shiller\'s century and a half of data.':
        "在Shiller一个半世纪的数据上测量这个分解。<bookmark mark='a'/>在十五年内被解释的部分中，股息率变动的约百分之{100 * share_r:.0f}是关于未来收益的消息。"
        "<bookmark mark='b'/>关于股息的消息几乎什么也解释不了，而且符号还是反的。股价相对股息高的时候，不是因为股息即将上升，而是因为未来收益即将变低。"
        "John Cochrane在美国金融学会的主席演讲中说得很简单：驱动价格的是贴现率，而不是现金流。",

    "What does it mean?":
        "这意味着什么？<bookmark mark='a'/>要么贴现率确实变化很大，因为投资者对风险的胃口时涨时落，正如上一章的习惯模型所预测的；要么投资者的预期摆动过度，"
        "正如Shiller本人所主张的。证据相同，解读相反。<bookmark mark='b'/>2013年，诺贝尔委员会把奖同时授予了Eugene Fama、Lars Hansen和Robert Shiller。"
        "<bookmark mark='c'/>对预测者来说，实际的结论更窄：收益在若干年的尺度上可预测，在几个月的尺度上几乎不可预测，而且在样本外很脆弱，正如第六部分所发现的。",

    "The market's dividend yield is at a record low.":
        "市场的股息率处于历史最低。按Campbell–Shiller恒等式，接下来必须发生什么？两者之中你会押哪一个？",

    # ------------------------------------------------------------------ Intermediary
    "Chapter nine. Perhaps the investor whose discount factor matters":
        "第九章。也许贴现因子起作用的那个投资者根本不是家庭，而是交易商。",

    "Households own most stocks in the end":
        "股票最终大多为家庭所有，但家庭很少直接交易债券、期权、互换或货币。交易商才交易。Zhiguo He和Arvind Krishnamurthy认为，这些市场上的边际投资者是中介机构，"
        "所以它对一美元的估值就是贴现因子。当交易商的资本稀缺时，一美元对它们价值很高，它们必须持有的资产要为承担这种稀缺支付溢价。Zhiguo He、Bryan Kelly"
        "和Asaf Manela直接测量了这种稀缺：纽约联储一级交易商的权益资本比率。",

    "Why should a dealer's capital matter so much?":
        "为什么交易商的资本这么重要？算一张资产负债表。一个交易商持有一百美元资产，权益十美元：资本比率百分之十。<bookmark mark='a'/>资产下跌百分之五。"
        "债务不会下跌，所以全部损失都从权益里出，权益减半为五美元，比率降到约百分之五。<bookmark mark='b'/>要以五美元权益回到百分之十，交易商只能持有五十美元资产："
        "它必须卖掉九十五美元中的四十五美元。<bookmark mark='c'/>每个交易商都对同样的资产做同样的事，价格再次下跌，下一轮损失开始。Markus Brunnermeier"
        "和Lasse Pedersen称之为损失螺旋和保证金螺旋。所以恰恰在资本稀缺时，一美元对交易商最值钱，在那些时刻下跌的资产必须支付溢价。",

    'f"Here is their measure':
        "这是他们的测度：交易商母公司的市值权益占权益加债务的比例。<bookmark mark='a'/>它在危机中下降：1974年、1987年、2000年代初，尤其是2008到2009年的冬天，"
        "那时它降到约百分之{100 * r[k]:.0f}。一个在这个比率下降时表现差的资产，恰恰在必须持有它的人最承受不起的时候亏钱。",

    'f"Their test is ambitious':
        "他们的检验雄心勃勃：一个因子，即这个资本比率的冲击，应当能为交易商做市的每个市场上的资产定价。<bookmark mark='a'/>取他们的股票、美国国债、主权债券、期权、"
        "信用违约互换、商品和货币组合，用第六部分的两步回归对市场和资本因子做检验。<bookmark mark='b'/>资本风险的价格在七个类别中的六个为正，而且大小相近。"
        "在股票上，它把平均收益被解释的比例从CAPM的{cl['stocks']['r2_capm']:.2f}提高到{cl['stocks']['r2']:.2f}。商品是例外。"
        "一个关于谁缺资本的单一测度，在原本几乎没有共同点的市场之间走得很远。",

    "There is a rival measure.":
        "还有一个与之竞争的测度。<bookmark mark='a'/>Tobias Adrian、Erkko Etula和Tyler Muir用美联储资金流量表中券商的杠杆：杠杆上升时交易商资金充裕，"
        "一美元对它们价值较低。<bookmark mark='b'/>两篇论文在什么重要的符号上有分歧，在谁的资产负债表上也有分歧：券商的账面杠杆，还是其母公司的市值资本。"
        "<bookmark mark='c'/>但两者都指向同一个思想，也就是第二十二部分各种基差背后的思想：当做市的人受到约束时，价格就会偏离仅由基本面决定的水平。",

    "If dealers' capital prices assets":
        "如果交易商的资本为资产定价，那么银行权益下跌时，第二十二部分的抛补利率平价基差应当怎样变化？为什么？",

    # ------------------------------------------------------------------ Inelastic
    "Chapter ten. Prices are set where demand meets supply":
        "第十章。价格由需求与供给相交决定；股票的需求曲线有多陡？",

    "The models so far say what investors should demand":
        "到目前为止的模型说的是投资者应当需求什么；Ralph Koijen和Motohiro Yogo问的是他们实际需求什么。他们根据每个机构向SEC报送的季度持仓，"
        "估计它对每只股票的需求：组合权重是股票价格和特征的函数，而价格就是让所有需求加起来等于流通股数的那个水平。<bookmark mark='a'/>关键数字是需求弹性："
        "股价上涨百分之一时，投资者想要的股数减少多少。在教科书模型里它极大，因为错误定价的股票会被套利掉。在持仓数据里它很小。",

    "Here is how the logit turns holdings into an elasticity.":
        "下面看logit怎样把持仓变成弹性。投资者持有的股数等于它的资产乘以组合权重，再除以价格。<bookmark mark='a'/>在logit中，一只股票的权重随该股票自身的市值变化，"
        "斜率为贝塔零，因为其他权重必须让出位置而略有衰减。<bookmark mark='b'/>所以每个投资者的弹性等于一减去贝塔零乘以一减权重。<bookmark mark='c'/>"
        "指数基金按市值比例持有每只股票：贝塔零为一，它的弹性几乎恰好为零。价格再高，它也不会少买一股。在每只股票上保持固定金额的投资者，贝塔零为零，弹性为一。"
        "只有强烈逆价格而行的投资者，即贝塔零为很大负数的价值投资者，才是有弹性的。市场的弹性是按持仓加权的平均：如果市场的百分之七十像指数一样持有、其余按固定金额持有，"
        "弹性约为三分之一。Koijen和Yogo的估计显示，大多数机构需求比教科书模型假设的更靠近无弹性的一端。",

    "Why it matters, in a picture.":
        "用一张图说明它为什么重要。股票的供给是固定的。<bookmark mark='a'/>如果需求有弹性，曲线平坦，一个新买家把它向右推，价格几乎不动：价格一高于价值，"
        "就有别人卖出。<bookmark mark='b'/>如果需求陡峭、缺乏弹性，同一个买家就会把价格推得很远，因为其他持有者是配置固定的养老基金，以及必须以任何价格持有每一股的指数基金。",

    "Xavier Gabaix and Ralph Koijen estimated the elasticity":
        "Xavier Gabaix和Ralph Koijen根据股票与债券之间的资金流，估计了整个市场的弹性。他们发现它约为五分之一。<bookmark mark='a'/>所以乘数约为五："
        "流入股市的一美元会让它的市值上升约五美元。一千亿美元的净买入，即市场的五分之一个百分点，会让价格上涨约百分之一。他们称之为无弹性市场假说；如果它是对的，"
        "推动价格的不只是消息，还有资金流，Shiller发现的大量波动就是市场在吸收这些资金流。",

    "The consequences are large if it is right.":
        "如果它是对的，后果很大。<bookmark mark='a'/>随着指数基金增长，市场中以任何价格持有每一股的部分越来越大，需求变得更加缺乏弹性。<bookmark mark='b'/>"
        "回购自家股票的公司是市场难以轻易吸收的买家。<bookmark mark='c'/>它也有争议：把资金流和引起资金流的消息分开很难，而在近似替代品之间更容易套利的单只股票，"
        "比整个市场更有弹性。",

    "If the market's elasticity is a fifth":
        "如果市场的弹性是五分之一，把市场的百分之一从债券转到股票会对价格产生什么影响？谁在卖？",

    # ------------------------------------------------------------------ Behaviour
    "Prospect theory, in two curves.":
        "两条曲线说明前景理论。<bookmark mark='a'/>左边是收益或损失的感受。Amos Tversky和Daniel Kahneman估计，损失的分量约为同等收益的二又四分之一倍，"
        "而且曲线在两侧都变平：亏掉的第二个一千美元没有第一个那么痛。<bookmark mark='b'/>右边是概率的权重。小概率被高估：百分之一的机会感觉像百分之五点五；"
        "大概率被低估。<bookmark mark='c'/>把这些放进市场，投资者就会为彩票付出过高的价格，也就是有很小机会获得巨大收益的股票。Nicholas Barberis和Ming Huang"
        "证明这样的股票随后应当赚得更少，而偏度最大的股票，包括新股和仙股，确实如此。",

    "Prospect theory leaves a fingerprint in trading records.":
        "前景理论在交易记录里留下了指纹。Terrance Odean研究了一家折扣券商的一万个账户。在投资者卖出任何东西的每一天，Odean都计算账户中盈利股票被卖出的比例。"
        "<bookmark mark='a'/>以及亏损股票被卖出的比例。盈利股票被卖出的倾向约为亏损股票的一点五倍，尽管卖掉的盈利股票随后跑赢了留下的亏损股票。"
        "投资者从买入价衡量盈亏，讨厌把账面亏损变成实际亏损：这就是处置效应。",

    "Chapter eleven. Behavioural finance":
        "第十一章。行为金融，以及为什么套利不总能修复行为造成的问题。",

    "Nicholas Barberis and Richard Thaler described":
        "Nicholas Barberis和Richard Thaler把行为金融描述为建立在两大支柱之上。<bookmark mark='a'/>第一是套利的限制：纠正一个错误定价的资产本身就有风险、有成本。"
        "价格可能在回归之前偏离得更远，借股票来做空要花钱，套利者的资本是有限的。<bookmark mark='b'/>第二是心理：系统性的错误，比如外推近期收益、过度自信、"
        "对损失的感受强于收益，它们首先制造了错误定价。单有其中一个是不够的。套利能修复的错误会被修复；没有错误，限制也就无从限制。",

    "The cleanest example came at the peak of the dot-com bubble.":
        "最干净的例子出现在互联网泡沫的顶峰。2000年3月，3Com把它的子公司Palm的百分之五卖给公众，并承诺把其余部分分给自己的股东，"
        "每股3Com约分得一点五股Palm。<bookmark mark='a'/>Palm上市第一天，市场给3Com的估值低于它所持有的Palm股票：Owen Lamont和Richard Thaler算出，"
        "公司其余业务的估值约为负二百二十亿美元。这个套利一目了然，报纸上都登了。限制它的是能借来做空的Palm股票太少，以及借券的成本。",

    "Andrei Shleifer and Robert Vishny made the limit precise.":
        "Andrei Shleifer和Robert Vishny把这个限制说得很精确。噪声交易者把价格压到价值以下；套利者用手头的资金买入，价格等于价值减去他们吸收不了的部分。"
        "<bookmark mark='a'/>但套利者投资的是别人的钱，而投资者按近期收益评判他们。亏损之后，资金就会被撤走。<bookmark mark='b'/>所以如果错误定价加深，"
        "套利者恰恰在机会变好的时候失去资本，价格会跌得比单靠噪声交易者推动的更深。",

    "In numbers: a stock worth one dollar":
        "用数字说：一只价值一美元的股票，噪声交易者先悲观三十美分、再悲观四十美分，套利资金为二十美分。<bookmark mark='a'/>第一次冲击后，价格为九十美分。"
        "没有赎回的话，第二次冲击会把它带到八十美分。<bookmark mark='b'/>投资者在亏损后撤资越多，价格就越低；撤资敏感度为三时，降到六十美分。"
        "套利恰恰在最需要的时候最无力：1998年对冲基金就是这样失败的，2008年和2020年3月各种基差也是这样扩大的。",

    "Three ideas recur on the psychological side.":
        "心理方面有三个反复出现的思想。<bookmark mark='a'/>噪声交易者风险：如果悲观者在价格恢复之前可能变得更悲观，那么即使资产本身没有风险，"
        "短期限的套利者也面临风险。<bookmark mark='b'/>外推：调查显示，投资者在高收益之后预期更高的收益，与第八章所说的理性预期恰好相反。<bookmark mark='c'/>"
        "还有前景理论，正如那两条曲线所示：损失的分量约为收益的两倍，小概率被高估，这会让类似彩票的股票变贵。每一个都预测出第二十四部分将作为因子来检验的规律。",

    "You run an arbitrage fund":
        "你管理一只套利基金，一个你很有把握的头寸一个月亏了百分之二十。你的投资者可以按月赎回。你怎么办？所有像你一样的人会对价格做什么？",

    # ------------------------------------------------------------------ Bubbles
    "Chapter twelve. Bubbles":
        "第十二章。泡沫，以及是否有人能看到它的到来。",

    "What is a bubble?":
        "什么是泡沫？<bookmark mark='a'/>Eugene Fama的挑战：如果涨了很多的价格并不会可预测地下跌，这个词就毫无意义；它只是事后诸葛亮。<bookmark mark='b'/>"
        "Robert Shiller的回答：泡沫是一场乐观情绪的流行病，上涨的价格吸引买家，他们的买入又推高价格。<bookmark mark='c'/>这个分歧可以检验："
        "找出历史上每一次急剧的暴涨，看看之后发生了什么。",

    'f"The bubble everyone remembers.':
        "每个人都记得的那个泡沫。<bookmark mark='a'/>以科技和互联网公司为主的纳斯达克综合指数，从1995年初到2000年3月涨了近七倍。<bookmark mark='b'/>"
        "它在2000年3月10日见顶，约为{pk['v']:,.0f}点，到2002年10月已经跌去百分之{abs(100 * (tr['v'] / pk['v'] - 1)):.0f}。"
        "它花了十五年才重新见到那个高点。事后看它像个泡沫。事前看，它是否以一种可测量的方式像个泡沫？",

    'f"Robin Greenwood, Andrei Shleifer and Yang You':
        "Robin Greenwood、Andrei Shleifer和Yang You接受了Fama的挑战。找出每一个两年内价格翻倍的美国行业，既按绝对值、也相对于市场。<bookmark mark='a'/>"
        "然后问之后发生了什么。<bookmark mark='b'/>在Kenneth French的四十九个行业上，1926年以来共有{b['n']}次这样的暴涨。"
        "其中百分之{100 * b['p_crash']:.0f}崩盘了，即两年内从高点下跌百分之四十。然而这两年的平均收益是{100 * b['mean_next']:+.0f}%。"
        "双方都对：暴涨之后崩盘的可能性大得多，但那些继续上涨的暴涨赚得足够多，让平均值为正。",

    "Every run-up, by when it happened":
        "每一次暴涨，按发生时间和价格涨了多少排列。<bookmark mark='a'/>红色的崩盘了，其他的没有。它们成簇出现：1930年代的复苏、1960年代末的狂飙年代、"
        "1980年的商品繁荣、1990年代末，以及2020年代。<bookmark mark='b'/>Greenwood、Shleifer和You发现，崩盘可以事先部分区分出来：波动率上升、股票发行量大、"
        "年轻公司多的暴涨，崩盘得更频繁。也就是说，可以按概率预测；永远无法预测时间。",

    "Can a bubble be rational?":
        "泡沫可以是理性的吗？把价格写成基本价值加一个泡沫项。如果泡沫预期恰好以要求收益率增长，定价方程仍然成立：持有它的人没有犯任何错误。<bookmark mark='a'/>"
        "Olivier Blanchard和Mark Watson让它可以破裂。它每年以某个概率存活，为了让人愿意持有，它在存续期间必须增长得更快，以补偿破裂的风险。"
        "<bookmark mark='b'/>要求收益率为百分之五、每年有十分之一的概率破裂时，它每年上涨约百分之十七，预期持续十年。<bookmark mark='c'/>但理论把它限制得很紧。"
        "泡沫不能为负，所以一旦破裂就永远无法重新开始，而且它必须从资产第一次交易时就存在。它不能存在于任何有最终支付的东西上，比如债券。它也不能永远比经济增长得快。"
        "理性泡沫是可能的；但它们不能很好地描述纳斯达克。",

    "Theory has two strands.":
        "理论有两条线索。<bookmark mark='a'/>理性泡沫，即以恰好等于要求收益率的速度增长的、高于价值的价格，只能在特殊条件下存活。<bookmark mark='b'/>"
        "更有用的是这样的证据：老练的投资者骑在泡沫上而不是与之对抗。Markus Brunnermeier和Stefan Nagel发现，1999年对冲基金大量持有科技股，并在顶峰之前撤出。"
        "如果聪明的钱选择择时骑泡沫而不是做空它，泡沫就会变大。<bookmark mark='c'/>对风险经理来说，教训和套息交易教给我们的一样：暴涨改变的是崩盘的概率，"
        "而不是日期，所以要按崩盘来确定头寸规模。",

    "An industry has doubled in two years against the market.":
        "一个行业两年内相对市场翻了一倍。大约一半的情况下随后会崩盘，但随后的平均收益为正。你会做空它吗？",

    # ------------------------------------------------------------------ House
    "Chapter thirteen. The House's twenty-third rule":
        "第十三章。House的第二十三条规则，给本部分开张的那个交易台：研究。",

    "The research desk's first sheet":
        "研究交易台的第一张表，每个数字都来自本部分。<bookmark mark='a'/>一个夏普比率在样本外下降超过一半、被等权重击败的切点组合。一条只有CAPM所说约三分之一陡的证券市场线。"
        "二十五个在样本内要求贴现因子比任何消费模型给出的都更波动的组合。解释溢价所需的接近七十的风险厌恶。波动超过股息所能解释的价格。以及大约一半会崩盘的行业暴涨。"
        "每一个都既是测量也是警告：任何东西的预期收益，都是金融中最难知道的数字。",

    "Three excerpts from the House's new module":
        "House新模块中的三段摘录承载了本部分的大部分内容。切点组合：用协方差矩阵对预期超额收益求解，再归一化。Hansen–Jagannathan界：同样的求解，"
        "它的平方根是这些资产能构成的最高夏普比率，也是任何贴现因子必须具有的最小波动率。还有Shleifer和Vishny的两个价格：当套利者的钱跑掉时，第二个价格跌得更深。"
        "前两个是同一行线性代数。这是本部分最深刻的一点：组合选择和定价模型是从两边看同一个对象，所以预期收益中的每一个误差都会变成组合中的误差，"
        "并被协方差矩阵的逆放大。",

    "This part has given three kinds of explanation":
        "本部分给出了三种解释，说明一样东西为什么会有回报。<bookmark mark='a'/>风险：资产在坏时候亏钱，溢价是这一点的价格。交易台必须说出那个坏状态，"
        "并检查资产在那里确实亏钱。<bookmark mark='b'/>约束：溢价付给有资产负债表来持有资产的人。交易台必须说出是谁的资本，以及它收缩时会发生什么。"
        "<bookmark mark='c'/>错误：溢价是一种错误定价，被某种套利的限制保持着。交易台必须说出偏差和限制，并预期溢价一旦公开就会缩小。<bookmark mark='d'/>"
        "三者并不互斥，数据也很少能在它们之间作出裁决。但理由对确定规模很重要：风险溢价恰恰在你害怕的状态里支付，而错误可能一夜之间就被纠正。",

    "In practice the rule becomes a pipeline":
        "在实践中，这条规则变成一条流程，第四幕后面的每一部分都要经过它。<bookmark mark='a'/>主张：这个资产或策略获得溢价，而且是在一个明确的世界状态下支付。"
        "<bookmark mark='b'/>理由，在打开数据之前就写下来。<bookmark mark='c'/>估计，附上标准误，以及一路上尝试过的变体数目。<bookmark mark='d'/>样本外："
        "在估计从未见过的数据上的表现，与等权重和市场相比。<bookmark mark='e'/>压力：它最差的一个月，以及那时还有谁必须卖出。<bookmark mark='f'/>最后是台账："
        "结果记入House的业绩记录，无论溢价是否存活都保留下来，这样交易台自己的试验次数就永远不会被遗忘。第二十四部分会把第一批因子送进这条流程。",

    "The research desk opens with these tools.":
        "研究交易台带着这些工具开张。<bookmark mark='a'/>前沿、最小方差组合和切点组合；贝塔与证券市场线；贴现因子的界及其用于GMM的欧拉方程；那个谜的算术；"
        "Shiller的事后理性价格和Campbell–Shiller分解；以及套利的限制、资金流乘数和暴涨。<bookmark mark='b'/>还有第二十三条规则。House使用的每一个预期收益，"
        "都要附上它的标准误和背后的试验次数。每一个溢价都要给出理由，是风险、约束还是错误，以及它在哪个坏状态下支付。每一组组合权重都要在样本外与等权重比较来评判。"
        "每一个溢价都按它的崩盘而不是它的平均值来确定规模。",

    "Hold the rule against this part's cases.":
        "用本部分的案例检验这条规则。<bookmark mark='a'/>优化器：一个在样本外与等权重比较来评判的切点组合，永远不会按它的样本内夏普比率去交易。"
        "<bookmark mark='b'/>一个t统计量为二点四的新异象：规则先要问它是试了多少次才找到的、它为什么应当有回报、它在哪个状态下亏钱，然后才有人去看回测曲线。"
        "<bookmark mark='c'/>套利基金：一笔按投资者离开的那个月来确定规模的收敛交易。<bookmark mark='d'/>还有翻倍的行业：按崩盘确定规模的头寸，不需要知道日期。"
        "这些都不会让预期收益更容易知道。它们让House对自己知道得多么少保持诚实。",

    # ------------------------------------------------------------------ Outro
    "Part twenty-three in fourteen lines.":
        "用十四行回顾第23部分。1926年投入美国股票的一美元变成了一万七千多美元；投入国库券，只有二十五美元。Markowitz画出了值得持有的组合的前沿。"
        "Tobin证明，有了现金，每个人都持有同一个风险组合，而估计误差表明它的权重几乎无法知道：在样本外，等权重表现更好。CAPM说只有贝塔得到报酬，"
        "而证券市场线是平的。一个方程，价格等于预期贴现支付，包含了每一个模型，Hansen和Jagannathan给出了它的贴现因子必须多波动的下界。"
        "APT和Merton的ICAPM允许多个因子，只要它们得到报酬。用GMM估计的消费模型，需要一个大到几乎测不准的风险厌恶。",

    "That is the equity premium puzzle, and habits":
        "这就是股权溢价之谜，习惯、长期风险和罕见灾难是它的候选答案。Shiller发现价格比它们所预测的股息波动得多，Campbell和Shiller证明这些摆动关乎未来收益。"
        "交易商的资本在一个又一个市场上为资产定价。股票需求缺乏弹性，所以资金流推动价格。行为制造错误定价，而套利恰恰在套利者的钱用完时失败。"
        "暴涨预测崩盘，按概率而不是按时间。House的第二十三条规则要求每个溢价给出它的标准误、它的理由，以及它在哪个坏状态下支付。",

    "Six desk questions. Two assets of twenty percent":
        "六个交易台问题。两个波动率百分之二十、相关系数一半的资产：各持一半，波动率为百分之十七点三。<bookmark mark='a'/>按一种解读，证券市场线是平的，"
        "是因为不能借钱的投资者为了风险而买高贝塔股票，把它们抬高了；押注低贝塔一直有回报。<bookmark mark='b'/>夏普比率为二的资产需要每年波动率达百分之二百的贴现因子；"
        "先怀疑数据，再怀疑理论。",

    "The equity premium needs a risk aversion near seventy":
        "股权溢价需要接近七十的风险厌恶，因为消费很平滑，而且与股票只是松散相关。<bookmark mark='a'/>历史最低的股息率之后，必然是低收益或快速的股息增长，"
        "而历史说是收益。<bookmark mark='b'/>需求弹性为五分之一时，把市场的百分之一转入股票会让价格上涨约百分之五，直到少数不受约束的持有者卖出足够多来吸收它。"
        "完整解答在讲义里。",

    "And ten problems: the frontier by Lagrange":
        "还有十道习题：用拉格朗日乘数求前沿；两资产最小方差组合；切点组合的夏普比率即Hansen–Jagannathan界；一个平均收益需要多少年；推导CAPM及其贴现因子；"
        "用数字看无风险利率之谜；灾难中的边际效用；Campbell–Shiller常数；以及手算Shleifer和Vishny的价格。中英文解答都在讲义里。",

    "Where this comes back.":
        "这些内容会在哪里再出现。第二十四部分用Fama–MacBeth回归和GRS检验来检验因子，从押注低贝塔开始。第二十五部分面对数以百计的因子，用试验次数和一个收缩的贴现因子。"
        "第二十六部分构建不会骗过作者自己的回测。第二十七部分用机器学习学出预期收益和贴现因子。第三十部分构建能经受估计误差的组合，第三十二部分按崩盘确定另类溢价的规模。",

    "The textbooks this part follows":
        "本部分所依据的教科书，以及它引用的论文，从Markowitz 1952年的十二页论文到无弹性市场假说。屏幕上的每个数字都由House的代码根据公开数据算出，"
        "示意性的模型都已标明。",

    "That opens Act Four, on return premia":
        "第四幕“收益溢价”和House的研究交易台由此开启。<bookmark mark='a'/>下一部分，第二十四部分：因子。规模、价值、动量、盈利能力和低风险，"
        "每一个都用本部分和第六部分的工具检验，每一个都讲它的历史和它的崩盘，每一个都记入House的业绩记录。",
}

PHRASES = {}
