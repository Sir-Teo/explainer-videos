"""Chinese narration for quant10: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第10部分：Black–Scholes–Merton'

CHAPTERS = {
    'Hook': '用股票和现金造出一份期权',
    'History': '1. 公式之前',
    'Replication': '2. 无风险组合',
    'Heat': '3. 解方程：倒着运行的热传导',
    'RiskNeutral': '4. 价格是一个期望',
    'Tree': '5. 二叉树及其极限',
    'Greeks': '6. 希腊字母的几何',
    'Ledger': '7. 对冲者的钱从哪里来',
    'WrongVol': '8. 用错误的波动率对冲',
    'Discrete': '9. 分步对冲',
    'Leland': '10. 为对冲付费：利兰波动率',
    'Solver': '11. 把公式反过来用',
    'Implied': '12. 第一条微笑曲线与基准曲面的第一行',
    'Carry': '13. 股息、借券与远期',
    'American': '14. 提前行权与自由边界',
    'BTC': '15. 在真实的比特币上卖出波动率',
    'Crash': '16. 1987年10月',
    'LTCM': '17. 诺贝尔奖，然后是LTCM',
    'Industry': '18. 业界：公式如何谋生',
    'Frontier': '19. 前沿：2023至2026年',
    'Research': '写给研究者：何时再平衡对冲',
    'Outro': '回顾、交易台问题与习题',
}

PHRASES = {
    "below": "低于",
    "above": "高于",
    "smaller than": "小于",
    "no better than": "并不优于",
    "It hits a floor,": "它撞上了一个底，",
    "It falls, but slowly, towards a floor,": "它在下降，但很慢，趋向一个底，",
    "the actual-volatility hedge": "按实际波动率对冲",
    "the implied-volatility hedge": "按隐含波动率对冲",
    "within a hundredth.": "相差不到百分之一。",
    "rounding level": "舍入误差的水平",
}

ZH = {
    'Part ten. Black, Scholes and Merton. In their continuous, frictionless model, an':
        '第10部分。布莱克、斯科尔斯和默顿。在连续交易、没有摩擦的模型里，期权可以用股票和现金复制。我们推导这个结论，检查它的局限，先从真实比特币行情上的一个简化实验开始。',
    'f"The first of October 2021. Bitcoin is about {b[\'pick_S0\']:,.0f} dollars. Suppo':
        "2021年10月1日，比特币约{b['pick_S0']:,.0f}美元。假设按当天现价卖出30天美元看涨期权，用DVOL的{100 * b['pick_iv']:.0f}%作为波动率代理，模型权利金为每100美元比特币{prem:.1f}美元；这不是实际看涨期权的成交价。<bookmark mark='a'/>比特币上涨{S[-1] - 100:.0f}%。<bookmark mark='b'/>到期支付{S[-1] - 100:.0f}，不对冲亏{S[-1] - 100 - prem:.0f}。停一下：每小时对冲会怎样？<bookmark mark='c'/>卖方从每份期权持有{b['pick_delta'][0]:.2f}个币单位开始，逐步接近1。白线最终赚{b['pick_pnl']:.2f}，尚未扣成本和融资。我们事后从{b['n']:,}个重叠窗口中选出盈利居中的这个窗口，用来说明机制，不代表可执行的交易业绩。",
    'f"The shares follow the model delta. Continuous replication cancels first-order ':
        "持股数量跟着模型Delta走。连续复制消除一阶股票风险，每小时对冲还留有误差。本例卖方赚的是Gamma加权的方差差。<bookmark mark='a'/>DVOL代理为{100 * b['pick_iv']:.0f}%，实际波动率为{100 * b['pick_rv']:.0f}%。仅凭两者之差还不能确定盈利，路径上的Gamma权重也重要。<bookmark mark='b'/>这正是公式背后的问题。",
    'The plan. The formula derived and solved three ways.':
        '本部分的计划。用三种方法推导并求解这个公式。把希腊字母看成同一个曲面。逐项拆开对冲者的盈利，以及对冲失败的方式：分步进行、遇到跳跃、有成本、用错波动率。在真实的市场上把公式反过来用，再加上股息和提前行权。还有真实数据：比特币、重放的1987年、1998年，以及交易台和研究者今天如何使用这个公式。',
    "And the House, the series' own quant firm":
        "我们的公司，也就是本系列自己的量化公司，开设了它的第一张交易台。到目前为止，它只有数据和资金。从这一部分起，它有了一个波动率交易台：一个定价器、一个对冲器、一个隐含波动率求解器，都写在本系列的代码库里，经过测试，后面每一部分都会用到。<bookmark mark='a'/>它的第一项工作，就是弄懂它即将据以交易的这个公式。",
    'Chapter one. Before the formula.':
        '第1章。公式之前。',
    'People priced options long before 1973.':
        "早在1973年之前，人们就在给期权定价。巴舍利耶1900年的博士论文，也就是本系列开始的地方，用随机游走给法国国债的期权定价，并与巴黎交易所的报价对照。<bookmark mark='a'/>之后这个想法沉睡了半个世纪。上世纪五六十年代，经济学家们重新发现了他，把随机游走换成对数正态的价格，并写下一份期权应该值多少：它的期望收益，贴现到今天。1961年的斯普伦克尔，1964年的博内斯，<bookmark mark='b'/>1965年的萨缪尔森。他们的公式看上去和我们的几乎一模一样。几乎。",
    'Here is the shape of the Sprenkle and Samuelson formula':
        "这是斯普伦克尔和萨缪尔森的看涨期权公式的样子：股价以期望增长率μ增长，乘以一个像概率一样的权重，减去行权价乘以另一个权重，整体再按利率ρ贴现。<bookmark mark='a'/>问题就在这里。μ是股票预期增长的速度；ρ是投资者持有像期权这样有风险的东西时要求的回报。这两个谁也不知道。停下来预测一下：两位投资者分别预期股票每年涨30%和跌10%。他们对这份看涨期权的价格看法一致吗？<bookmark mark='b'/>一致。Black–Scholes公式就是把这两个未知数都换成一个人人都查得到的数：无风险利率r。为什么期望收益无关紧要，正是本部分的内容。",
    'The way out came from three directions.':
        "出路来自三个方向。1967年，在二十一点上击败过赌场的爱德华·索普，和希恩·卡苏夫出版了一本关于认股权证的书，认股权证就是公司发行的长期期权：卖出定价过高的权证，并持有股票与之对冲。股价上涨时空头权证亏钱，股票赚钱，在今天的价格附近两者正好抵消：白色曲线在那里是平的，只在大幅变动时才向下弯，而这正是本部分的钱赚进和亏出的地方。据唐纳德·麦肯齐记载，到1967年，索普用的公式与Black–Scholes只差一个贴现因子。<bookmark mark='a'/>与此同时，咨询顾问费希尔·布莱克和麻省理工学院的年轻教授迈伦·斯科尔斯论证：对冲后的头寸没有市场风险，因此按资本资产定价模型，它只能赚取无风险利率。<bookmark mark='b'/>罗伯特·默顿看到了更深的原因：连续交易，对冲就是无风险的，因此只需要无套利这一条。<bookmark mark='c'/>《政治经济学杂志》最初以题目过于专门为由拒绝了布莱克和斯科尔斯的论文，《经济学与统计学评论》也拒绝了它。它最终于1973年发表在《政治经济学杂志》上，与默顿发表在《贝尔经济学杂志》上的论文同年问世。",
    'On the twenty-sixth of April 1973 the Chicago Board Options Exchange opened':
        "1973年4月26日，芝加哥期权交易所开业：只有看涨期权，16只股票，第一天成交911张合约；看跌期权到1977年才出现。费希尔·布莱克向交易员出售印好的理论价格表，社会学家唐纳德·麦肯齐认为，市场之所以按公式说的那样给期权定价，是因为交易员在用它，这是第18章的故事。<bookmark mark='a'/>他们开始用波动率来报期权的价，那是公式里唯一查不到的输入。<bookmark mark='b'/>1997年，斯科尔斯和默顿获得诺贝尔奖；布莱克已在两年前去世。现在我们来推导他们的发现。",
    'Chapter two. The riskless portfolio.':
        '第2章。无风险组合。',
    'Three things can be traded.':
        "有三样东西可以交易。一只股票，它的价格服从第5部分的几何布朗运动：它以一个谁也不知道的期望增长率μ漂移，并以波动率σ抖动。<bookmark mark='a'/>一份债券，或者说一个银行账户，以无风险利率r增长。<bookmark mark='b'/>还有一份期权，它的价值V取决于时间和股价，通过一个我们还不知道的函数。<bookmark mark='c'/>这些假设很理想化，本系列后面会一个一个地放掉它们：你可以连续交易，没有成本，可以按r借入和贷出，而且你知道σ。每一个被打破的假设，都会成为本部分或者后面某一部分的一章。",
    'Now the argument, done properly.':
        "现在把论证严格地走一遍。构造一个组合X：持有Delta股股票，其余放在银行。它是自融资的：没有钱进来，也没有钱出去，所以它只随股票的盈亏和银行付的利息变化。<bookmark mark='a'/>期权的变化，由伊藤引理，有一个漂移项，含时间导数、μ乘以S乘以斜率、二分之一σ平方S平方乘以曲率，再加一个噪声项：σS乘以斜率，乘以布朗增量。<bookmark mark='b'/>把股票自己的方程代入组合的变化，它也有一个漂移项和一个噪声项。<bookmark mark='c'/>如果组合要在每一条路径上复制期权，噪声项就必须相等，这就确定了对冲：Delta就是期权价值的斜率。<bookmark mark='d'/>然后漂移项也必须相等。写出来，含μ的项出现在两边，互相抵消。剩下的就是Black–Scholes方程。布莱克和斯科尔斯的论证是：对冲后的头寸没有风险，所以赚无风险利率；默顿的自融资复制得到同一个方程，而且是经得起推敲的版本。",
    'This is the surprise that took economists a decade to find.':
        "这就是让经济学家花了十年才发现的意外。两位交易员对股票的走向看法完全相反，一个预期每年涨30%，另一个预期亏损，<bookmark mark='a'/>却对期权的价格看法一致，因为两人都能用同样的方法把它造出来，而谁的观点都不进入制造过程。停下来问问自己：为什么对冲者可以不管μ，却不能不管σ？因为对冲去掉了方向，剩下的是变动的大小：σ平方乘以曲率Gamma的那一项，股票的任何头寸都抵消不掉它。这一项就是期权交易台的全部经济学，第7章讲的就是它。",
    'Chapter three. Solving the equation: heat, run backwards.':
        '第3章。解方程：倒着运行的热传导。',
    'Chapter two ended with an equation.':
        "第2章结束在一个方程上。现在我们来解它，就像布莱克和斯科尔斯发表的论文那样：它是数学物理中最古老的方程之一，换了一身衣服。把期权的价值画在股价的对数和距到期的剩余时间上。在到期时，也就是前沿，价值就是收益：一根在行权价处有折角的曲棍球杆。<bookmark mark='a'/>现在让时间倒着走。方程把曲线从收益里托起来，一片接一片地把折角磨圆，就像热量沿着一根一端热、一端冷的杆子扩散。<bookmark mark='b'/>方程实际上在算的是这个。在某个剩余时间，取这个紫色的钟形：热核，一个宽度随σ乘以剩余时间平方根增长的正态密度。把它乘以收益，给乘积涂上阴影，加起来：完整、未缩放的积分贴现后才是黄点处的Black价值。图中的核有漂移位移，核与阴影乘积的高度经过缩放，并只显示有限窗口。<bookmark mark='c'/>滑动钟形，黄点就沿着曲面走。价格的每一点，都是收益按高斯权重取的平均。",
    'In symbols. Measure time backwards from expiry':
        "用符号写。从到期倒着计时，用对数表示价格，链式法则把方程变成这样：时间导数等于二分之一σ平方乘以曲率，加一个漂移项，减去贴现项。<bookmark mark='a'/>再做两个代换去掉后两项：撤掉贴现，让对数价格随漂移一起平移。剩下的就是热方程，σ平方除以2扮演杆子的导热系数。<bookmark mark='b'/>热方程从给定初始分布出发的解，从傅里叶和拉普拉斯时代就已知道：把初始分布与一个方差为σ平方乘以τ的高斯函数做卷积。我们的初始分布就是收益。<bookmark mark='c'/>在行权价处把积分拆开，那是收益开始不为零的地方；每一半都是高斯积分，对第一半配方，就得到两个N。<bookmark mark='d'/>把代换撤回去，公式就出来了。在平移且未贴现的热方程坐标里，平滑程度依赖σ平方乘以τ。所以停下来预测一下：波动率加倍，折角融化需要多长时间？四分之一的时间。",
    'f"The House has both roads.':
        "我们公司两条路都有。它的定价器计算公式；它的热方程求解器自己做卷积，用数值方法，适用于任何收益，在折角处把积分拆开。<bookmark mark='a'/>在一份波动率20%的一年期平值看涨期权上运行：{h['lab']['heat']:.4f}和{h['lab']['formula']:.4f}。在九组股价和期限上，两者一致到小数点后{int(-np.floor(np.log10(h['max_err']))) - 1}位：同一个数，一个靠积分，一个靠公式。而卷积还能给公式从未写过的收益定价，这就是为什么第16部分的主力是热方程，而不是公式。这个方程还有第二种读法：价格是一个期望。下一章。",
    'Chapter four. The price as an expectation.':
        '第4章。价格是一个期望。',
    'The heat kernel was a Gaussian average of the payoff.':
        "热核是支付的高斯加权平均。第5部分的Feynman–Kac定理把它解释为路径期望。<bookmark mark='a'/>在这里常系数、无股息的Black–Scholes模型中，今天价值是按无风险利率r增长的股价路径上，到期支付的贴现期望。<bookmark mark='b'/>这不是按真实漂移μ取平均，而是使用另一个等价测度Q。在这个模型下，贴现股票是真鞅；正定价测度的存在，要结合第9部分讨论的可容许性与正则条件理解。",
    'f"Two worlds, built from the same random numbers.':
        "两个世界，由同一组随机数构造。琥珀色的是真实世界：股票的期望增长率是每年{100 * mu:.0f}%。<bookmark mark='a'/>在这些路径上平均一份一年期平值看涨期权的贴现收益，得到{d['mc_P']:.2f}。那不是期权的价格。<bookmark mark='b'/>紫色的是同样的路径，漂移换成无风险利率{100 * r:.0f}%：平均是{d['mc_Q']:.2f}，误差正负{d['se_Q']:.2f}，也就是Black–Scholes价格{d['exact']:.2f}。<bookmark mark='c'/>吉尔萨诺夫定理说，这两个世界是权重不同的同一组路径：用这个指数给每条真实世界的路径加权，真实世界的平均就变成风险中性的平均，{d['mc_W']:.2f}。其中的θ，也就是μ减r再除以σ，是风险的市场价格，期权的价格不需要知道它。路径扇显示80条路径，两个直方图各用6万个终值观测且共享计数尺度；定价均值使用40万个样本。",
    'The average can be done by hand.':
        "这个平均可以手算。<bookmark mark='a'/>在Q下，最终价格的对数服从正态分布，均值是r减二分之一σ平方，再乘以T。<bookmark mark='b'/>所以收在行权价之上的概率是N(d2)。<bookmark mark='c'/>而这些结果里最终价格的平均，贴现以后，是S0乘以N(d1)：配方把高斯分布平移了σ乘以根号T。减去K乘以贴现后的概率，又得到了公式，这是第二条路。第9部分也把N(d1)读成一个概率，是在以股票为计价单位的测度下。",
    'f"And by simulation, watched as it runs.':
        "再用模拟，看着它运行。八个独立的随机种子，每个都在Q下平均越来越多的贴现收益。只有一百个结果时，八个估计相差好几美元；这条带按n的平方根的倒数收窄，并收拢到公式上。<bookmark mark='a'/>琥珀色的是把同样的预算花在真实世界的路径上，再按吉尔萨诺夫因子重新加权。两条带收拢到同一个价格。{verdict}",
    'f"Here the reweighted estimator is the narrower one:':
        "这里重新加权的估计量反而更窄：它的标准差是普通估计量的{m['ratio']:.2f}倍，因为真实世界更高的漂移把更多路径送进了实值区，也就是收益所在的地方，而权重修正了这一点。这就是重要性抽样，第16部分会有意地使用它。",
    'f"Here the reweighted estimator is the wider one,':
        "这里重新加权的估计量更宽，标准差是普通估计量的{m['ratio']:.2f}倍：权重本身就是噪声。",
    'f"The two Ns are worth keeping.':
        "这两个N值得记住。N(d2)是看涨期权以实值到期的风险中性概率：这里是{d['N_d2']:.3f}，也就是阴影面积，我们的风险中性结果中有{100 * d['q_itm']:.1f}%以实值到期；在真实世界里是{100 * d['p_itm']:.1f}%。停一下：这份看涨期权值那个真实概率吗？不：Q的概率是价格，不是预测。<bookmark mark='a'/>N(d1)是Delta，{d['N_d1']:.3f}股。持有N(d1)股，借入K乘以e的负rT次方再乘以N(d2)，这个组合就是期权。下一章：同一个期望放在树上，以及它的极限。",
    'Chapter five. The tree and its limit.':
        '第5章。二叉树及其极限。',
    'f"The third road is the one that is easiest to see.':
        "第三条路最容易看清。考克斯、罗斯和鲁宾斯坦，1979年：一步，两种结果。股价从100变成120或90，行权价100的看涨期权值20或者0。<bookmark mark='a'/>持有三分之二股，<bookmark mark='b'/>借入60，这个复制品在两种状态下都与期权相同，所以它们的价格必须相同：{c0:.2f}。<bookmark mark='c'/>写成两个收益的平均，上涨状态的权重是三分之一，不管上涨的真实概率是多少。第9部分建立了这些；这里我们把它推向极限。",
    'f"Chop the year into steps':
        "把一年切成许多步，二叉树的节点就成了空间里的点：横向是时间，纵向是股价，高度是看涨期权的价值。这是一棵四步的树，每个节点都在倒推给出的价值上，后面半透明的是Black–Scholes曲面。<bookmark mark='a'/>十六步。<bookmark mark='b'/>六十四步。<bookmark mark='c'/>二百五十六步。节点越来越多，并落到曲面上：节点与曲面之间最大的差距从{t3['max_gap'][0]:.2f}降到{t3['max_gap'][-1]:.2f}，步数每乘以4，差距大约减半，最大的差距出现在收益有折角的地方。二叉树不是对某一点价格的近似。它是整个曲面的一个离散化的副本。误差用绝对对数现价行权价比小于0.4的未到期节点计算。视图只画现价50至200范围，每棵树最多显示500个节点。",
    'Why it must converge is a short calculation.':
        "它为什么必然收敛，只需一段简短的计算。每个节点都是它两个后继节点的贴现风险中性平均。<bookmark mark='a'/>上涨幅度取e的σ乘以根号Δt次方，风险中性概率就是二分之一加上一个根号Δt量级的修正。<bookmark mark='b'/>把两个后继节点的价值做泰勒展开：根号Δt的项带着斜率，Δt的项带着曲率。<bookmark mark='c'/>代入，合并同次项，除以Δt，这个递推就是Black–Scholes方程加上一个Δt量级的误差。二叉树就是离散化的方程。",
    'f"Add steps and the tree\'s price converges to the formula.':
        "步数增加，二叉树的价格收敛到公式。这是从一步到四百步的每一个价格，边算边画。它是锯齿形的。停下来预测一下：偶数步的树恰好在行权价上有一个节点。这些树的价格在公式之上，还是之下？<bookmark mark='a'/>这里是{side}：两族从两侧逼近，按N分之一收敛，还带着一个由行权价落在两个节点之间的位置决定的摆动，弗朗辛和马克·迪纳在2004年把它精确地算了出来，第16部分更平滑的树会把它消除。<bookmark mark='b'/>四百步时，二叉树给出{d['big_N_price']:.4f}；公式给出{exact:.4f}。",
    'f"The House\'s tree is one loop backwards from expiry':
        "我们公司的二叉树就是一个从到期倒推的循环，再为第14章的美式期权加一行。<bookmark mark='a'/>四步：{lab['4']:.4f}。六十四步：{lab['64']:.4f}。四百步：{lab['400']:.4f}；公式：{t3['exact']:.4f}。三条路，一个公式。价格已经从三条路得到。下一章：它怎么变动——希腊字母。",
    'Chapter six. The Greeks as geometry.':
        '第6章。希腊字母的几何。',
    'Every risk an options trader manages is a slope':
        "期权交易员管理的每一种风险，都是同一个曲面的一个斜率或一个弯曲：期权的价值，画在股价和剩余时间上。在到期时，也就是前沿，它就是收益。<bookmark mark='a'/>再往后，曲面升高并变得平滑：第3章里融化的折角。<bookmark mark='b'/>希腊字母就是它的各个斜率的名字。Delta是沿股价方向的斜率，Gamma是沿这个方向的弯曲，Theta是沿时间方向的斜率，而Vega，根本不是希腊字母，是波动率上升时整个曲面抬高多少。取距到期三个月的那一片，黄色的。",
    'Laid flat: on top the value':
        "把它摊平：上面是价值，在收益之上；中间是它的斜率Delta，也就是对冲中的股数，远低于行权价时为零，远高于行权价时为一。<bookmark mark='a'/>下面是曲率Gamma：Delta变化得多快，也就是对冲者要多频繁地交易。它集中在行权价附近。<bookmark mark='b'/>让时间流逝：价值压向收益，Delta变陡成一个台阶，Gamma尖成一根针。临近到期的平值期权，一个小小的变动就会让对冲从零股翻到整整一股。",
    'Each slope takes two lines, thanks to one identity':
        "每个斜率只需要两行推导，靠的是一个恒等式：S乘以d1处的正态密度，等于贴现后的行权价乘以d2处的密度。<bookmark mark='a'/>对公式求S的导数：d1和d2变化带来的项按这个恒等式互相抵消，Delta就是N(d1)。<bookmark mark='b'/>再求一次得到Gamma；Vega，也就是对σ的导数，结果是σ乘以T乘以S平方乘以Gamma。<bookmark mark='c'/>而方程本身把其中三个联系在一起。停下来预测一下：平值，没有利率，期限无限增长时，看涨期权的Delta会怎样？趋于1，因为d1是二分之一σ乘以根号T。",
    'Theta is the slope along time':
        "Theta是沿时间方向的斜率：股价不动时，期权每天损失多少。没有利率时，方程只有两项，<bookmark mark='a'/>它说Theta等于负二分之一σ平方S平方乘以Gamma。<bookmark mark='b'/>用公式在距到期三个月处计算：Gamma每年赚多少，粉色实线，时间每年花多少，蓝色虚线，两者正好重合。不为弯曲付出时间的代价，就不能拥有它。唯一的问题是股价的变动够不够付这笔账：那是下一章。",
    'Last, vega: how much the value rises with volatility.':
        "最后是Vega：波动率上升时价值增加多少。又是一个以行权价为中心的鼓包，随剩余时间变大，与Gamma正好相反。<bookmark mark='a'/>对Black–Scholes来说，它等于σ乘以剩余时间乘以S平方再乘以Gamma：Gamma、Theta和Vega是从三个角度看同一个鼓包。这里零利率、零收益率的普通看涨或看跌期权，买入就是做多Gamma、做空Theta、做多Vega；二阶希腊字母Vanna和Volga，会在第11部分随微笑一起出现。下一章：希腊字母怎样在对冲者的账本里变成钱。",
    "Chapter seven. Where the hedger's money comes from.":
        '第7章。对冲者的钱从哪里来。',
    "Take the seller's side:":
        "站在卖方一边：卖出一份期权，持有Delta股股票，期权按卖出时的波动率σi，也就是隐含波动率，来估值。股票则按世界实际交付的波动率σr，也就是已实现波动率，来运动。<bookmark mark='a'/>把期权的变化展开到二阶：对冲抵消了一阶项，剩下Theta乘以dt，加上二分之一Gamma乘以变动的平方。<bookmark mark='b'/>由伊藤引理，变动的平方是S平方乘以已实现方差再乘以dt。<bookmark mark='c'/>而Theta是负二分之一隐含方差乘以S平方乘以Gamma。所以账本每一瞬间赚二分之一Gamma乘以S平方，再乘以隐含方差与已实现方差之差：这是押注股价的波动比你收取的要小，并按Gamma加权。",
    'f"One interval at a time:':
        "一个区间一个区间地看：卖方收进Theta，付出二分之一Gamma乘以变动的平方；当变动恰好是σi乘以根号dt时两者抵消，这就是盈亏平衡的变动幅度。<bookmark mark='a'/>一条按20%每天对冲四次的路径：绿色区间留在带内，赚钱；红色区间亏钱，而且是按平方亏。这条路径的已实现波动率是{100 * L['rows'][j]['realized']:.0f}%；它有{100 * frac_in:.0f}%的区间赚钱，卖方却仍然亏损。",
    'f"The House\'s hedger keeps the score:':
        "我们公司的对冲器负责记账：每一步它给期权估值，把变化记到持股上，并把它拆成Gamma项、Theta项和剩下的部分。<bookmark mark='a'/>在已实现波动率分别为12%、28%和20%的三个季度里，残差，也就是二阶展开漏掉的部分，从不超过{max(res):.2f}。",
    'f"Now watch those three quarters':
        "现在看这三个季度，每天对冲四次，卖出一份按20%出售的三个月平值看涨期权。粉色：Gamma项，变动的平方花掉的钱。蓝色：Theta项，时间付给你的钱。白色：账本。<bookmark mark='a'/>已实现12%时，Theta的收入整个季度都跑赢Gamma的账单，账本最后是{L['rows'][0]['pnl']:.2f}，期权费是{L['premium']:.2f}。<bookmark mark='b'/>已实现28%时，Gamma的账单胜出，账本亏{-L['rows'][2]['pnl']:.2f}。<bookmark mark='c'/>已实现20%，正好是卖出时的波动率，两者抵消：{L['rows'][1]['pnl']:.2f}。股价的方向从来没有进入计算。",
    "f'Pause and predict: when realized equals implied":
        "停下来预测一下：已实现波动率等于隐含波动率时，每一条路径都会以零结束吗？每种情形两万条路径。已实现12%时，卖方平均赚{rows[0]['mean']:.2f}，有{100 * rows[0]['p_loss']:.0f}%的路径亏钱。已实现28%时，卖方平均亏{-rows[2]['mean']:.2f}。已实现20%时，平均是{rows[1]['mean']:+.2f}，散布是{rows[1]['sd']:.2f}，来自每天只对冲四次：那是第9章。盈利就是两个波动率之差，一个是报出来的，一个是活出来的。但用哪个波动率来对冲？下一章：用错误的波动率对冲。",
    'Chapter eight. Hedging with the wrong volatility.':
        '第8章。用错误的波动率对冲。',
    'Let the true instantaneous volatility vary with time and the path, while the cal':
        "让真实瞬时波动率随时间和路径变化，期权仍按固定sigma h定价和对冲。假设股价为连续扩散、零利率、无成本、连续自融资交易，并满足必要的正则性和可积性。<bookmark mark='a'/>伊藤公式用真实方差sigma t的平方。<bookmark mark='b'/>从期权微分中减去Delta乘股票增量。这不是期权减Delta乘股票的整体微分，后者还包含Delta变化项。<bookmark mark='c'/>积分得到卖方的方差差盈亏。<bookmark mark='d'/>凸支付的Gamma非负。若真实瞬时波动率几乎必然始终不超过sigma h，连续对冲就在这些假设下超复制。这是El Karoui、Jeanblanc和Shreve在1998年的结论，不涵盖跳跃、离散交易或成本。",
    'f"Dollar gamma is a landscape over time and spot. The displayed near-expiry spik':
        "美元Gamma形成时间与现价的地形，显示的临近到期尖峰截于500。<bookmark mark='a'/>在2万条模拟路径中，取实际波动率接近20%的{w['n_band']:,}条，再选择积分Gamma最大和最小的两条。这是刻意挑选的权重对比，不代表典型路径。图中同步显示路径和累计权重。<bookmark mark='b'/>积分Gamma之比为{cols['near'][-1] / cols['far'][-1]:.1f}。有限步长盈利分别为{w['pnl_near']:.2f}和{w['pnl_far']:.2f}；盈利比还受到离散对冲和实际方差微小差别的影响。",
    'f"Buy a call at twenty percent, then compare hedges on twenty thousand GBM paths':
        "按20%买入看涨期权，再在2万条恒定30%波动率、年漂移10%的GBM路径上比较对冲，零利率且无成本。停一下：哪个对冲终值更集中？<bookmark mark='a'/>若知道真实波动率，用它连续对冲可锁定{s30['locked']:.2f}；分步时标准差为{s30['act_sd']:.2f}。<bookmark mark='b'/>按20%对冲，样本均值{s30['imp_mean']:.2f}，标准差{s30['imp_sd']:.2f}。直方图共享分箱和计数尺度。这里样本均值接近，不意味着任意真实动态下期望都相等。<bookmark mark='c'/>另一个25%波动率样本中，{loss_more}的亏损路径更多。预先知道未来恒定波动率是一项假设，不是已经具备的预测。",
    'f"Across {len(rv):,} Heston paths, profit and realized volatility have correlati':
        "在{len(rv):,}条Heston路径中，盈利与实际波动率的相关系数为{w['corr_rv']:.2f}。图中显示前1500条，相关系数用全部4000条。<bookmark mark='a'/>对每条路径的Gamma加权方差差积分，相关系数为{w['corr_pred']:.2f}。近似关系仍含离散对冲残差，不是对随机波动率的精确复制。方差互换则不加期权Gamma权重。",
    'Chapter nine. Hedging in steps.':
        '第9章。分步对冲。',
    'At zero rates under driftless GBM, freeze gamma and spot over one short step. It':
        "在零利率、零漂移GBM下，一个短区间内冻结Gamma和现价。首阶误差是二分之一Gamma乘S平方、sigma平方、时间步长，再乘Z平方减1。<bookmark mark='a'/>给定区间起始信息，条件方差为二分之一Gamma平方乘S四次方、sigma四次方和时间步长平方。<bookmark mark='b'/>这些首阶中心化增量是鞅差，尽管Gamma权重依赖此前走势，方差仍可相加。在通常的矩和收敛条件下，总标准差渐近正比于时间步长的平方根。Boyle和Emanuel，1980年；下方平值近似为Derman和Kamal的经验公式。",
    'f"Here it is measured.':
        "这是实测结果。一份三个月平值看涨期权，按真实波动率20%卖出，整个季度对冲4次、8次、16次，一直到1024次。五个独立的随机种子，每个一万条路径，随着频率上升画成一条带。粉色线是我们刚推导的公式，灰色虚线是经验法则。<bookmark mark='a'/>这条带窄得像一条线：五个种子之间的差别从不超过{100 * ds['spread_max']:.1f}%，它们在对数坐标上的斜率在{sl.min():.3f}到{sl.max():.3f}之间：平方根定律。每周对冲留下大约{d['sd'][2]:.2f}的误差，期权费是{d['premium_bs']:.2f}；每天四次，大约{d['sd'][6]:.2f}。",
    'f"The spread is not the whole story':
        "散布不是全部；看看它的形状。每一步的误差是Z平方减一，它是偏的：大多数时候是小额盈利，偶尔股价跳过一步时是一笔大亏损。<bookmark mark='a'/>{skew_line}",
    'f"Hedged weekly, the seller\'s distribution leans left':
        "每周对冲时，卖方的分布向左偏，偏度{ds['skew_13']:.2f}；每天对冲四次时，{ds['skew_252']:.2f}：步数更多，每一步更小，加总起来更像正态分布。",
    "f'Here the skewness is":
        "这里每周对冲的偏度是{ds['skew_13']:+.2f}，每天四次是{ds['skew_252']:+.2f}。",
    'f"Add Poisson log-price jumps, twice a year with a minus five percent mean log j':
        "加入泊松对数价格跳跃，每年平均2次，平均对数跳幅为负5%。与对数收益方差率相同的GBM比较，单个Black波动率不能补全这个跳跃市场。没有跳跃时，频繁对冲降低误差。<bookmark mark='a'/>有跳跃时，测得的标准差从{J.mean(0)[0]:.2f}降到{J.mean(0)[-1]:.2f}。{floor_phrase}跳跃留下屏幕上这个精确的非线性余项，二分之一Gamma乘S平方和J平方只是小对数跳幅近似。虚线{jf['floor']:.2f}是在对数正态现价代理下积分得到的跳跃余项风险参考，并非这些Merton模拟路径的方差下界证明。增加频率不能消除无法张成的跳跃风险。",
    "Chapter ten. Paying for it: Leland's volatility.":
        '第10章。为对冲付费：利兰波动率。',
    'f"Every rebalance pays a cost':
        "每一次调整都要付成本，是交易金额的单边比例k。后面的Leland公式改用往返费率k，等于单边费率的两倍。这是它对上一章那份卖出的看涨期权的影响：横向是一个季度里的对冲次数；纵深是以基点计的成本；高度是期望成本加上一个对冲误差的标准差。<bookmark mark='a'/>成本为零时，对冲越多越好：我们网格里最好的是{free_best}次，也就是我们试过的最多次数。随着成本上升，远端抬起，出现一道山谷。<bookmark mark='b'/>金色的山脊描出谷底：成本为千分之二点五时，最好的是{lg['best'][4]}次，大约每周{lg['best'][4] / 13:.0f}次。停下来预测一下：成本加倍。对冲更频繁，还是更少？更少：山脊向左移。",
    "Hayne Leland's insight, in 1985":
        "海恩·利兰1985年的洞见：成本可以被定价。在一步里，Delta的变化是Gamma乘以股价的变动。<bookmark mark='a'/>每笔交易的成本是其金额乘以往返成本的一半，而一个正态变动的平均大小是根号下π分之二。<bookmark mark='b'/>换算到单位时间，成本是二分之一Gamma乘以S平方，也就是第7章的那个因子，再乘以一个像根号Δt分之一那样增长的量。<bookmark mark='c'/>所以把它吸收进波动率：按利兰的σL出售并对冲。误差按根号Δt缩小，成本按它的倒数增长：这就是那道山谷。",
    'f"In the House it is three lines.':
        "在我们公司里，它只有三行。<bookmark mark='a'/>第4题：往返成本0.2%，波动率20%，每天对冲需要{100 * lab['daily']:.1f}%，每周对冲需要{100 * lab['weekly']:.1f}%。<bookmark mark='b'/>检验一下，每周对冲，单边成本千分之二点五：按20%定价，卖方亏{-d['naive_mean']:.2f}；按利兰的{100 * d['sigma_leland']:.1f}%，亏{-d['leland_mean']:.2f}，剩下的是第一次建立对冲和最后平仓的成本，{d['end_costs']:.2f}，公式没有算进去。去掉它们：{d['leland_mid_mean']:+.2f}。",
    'f"Fix the transaction-cost rate and increase hedging frequency. Sigma L grows fr':
        "固定交易成本率，提高对冲频率。sigma L从{100 * rows_[0]['sigma_L']:.0f}%增至{100 * rows_[-1]['sigma_L']:.0f}%，权利金从{rows_[0]['premium']:.2f}增至{rows_[-1]['premium']:.2f}。极限中波动率发散，但零收益率Black看涨期权价格有界，趋近股价。<bookmark mark='a'/>在连续扩散、比例成本和相应可容许性条件下，Soner、Shreve和Cvitanic的完美超对冲结论归结为买入股票，并按模型的买卖价记账。Kabanov和Safarian说明原始固定成本Leland策略的误差为何未必趋零。{kab_line}这些是特定模型的极限，不是说权利金可以无限增长。实际的替代方案是不交易区间。",
    'f"In our runs its spread is still shrinking':
        '在我们的模拟里，它的散布仍在缩小，从{sd_first:.2f}到{sd_last:.2f}：失效发生在极限处，也发生在价格上。',
    'f"In our runs its spread stops shrinking':
        '在我们的模拟里，它的散布不再缩小：从{sd_first:.2f}到{sd_last:.2f}。',
    'Chapter eleven. Turning the formula inside out: implied volatility.':
        '第11章。把公式反过来用：隐含波动率。',
    'f"Traders invert a pricing model: given a price, find its implied volatility. Ca':
        "交易员反演定价模型：给定价格，求隐含波动率。持有成本、贴现和结算约定都是转换的一部分。<bookmark mark='a'/>这里取2025年12月10日一份比特币看涨期权的拟合远期和已报隐含波动率，生成未贴现的Black远期价值，再反演。它检验的是输入波动率的数值恢复，不是独立成交价的拟合。<bookmark mark='b'/>从Corrado–Miller近似出发，用带保护的牛顿步骤恢复到{100 * its[-1]:.2f}%。数值恢复不等于市场定价准确。",
    'When does a finite positive IV exist? With positive forward, strike and time, th':
        "什么时候存在有限正隐含波动率？远期、行权价和期限为正，所用价格单位下，价格必须严格介于内在价值与上界之间。边界对应零或无穷波动率的极限，不一致的报价没有这种解。用远期乘行权价的平方根归一化，价格只依赖对数价内外程度x和总波动率s。<bookmark mark='a'/>Vega为正，使边界内的解唯一。平值远期价值近似为0.4s。<bookmark mark='b'/>临近到期且深虚值时，Vega很小，价格误差会放大成波动率误差。括区间保护牛顿法。Jäckel在2015年的方法利用变换和高阶修正，在适用范围内达到浮点精度。",
    'f"The House\'s loop: tighten a bracket':
        "我们公司的循环：收紧区间，尝试一步牛顿迭代，如果这一步落在区间外，就把区间对半分。本部分新加了一行：已经收敛的报价被冻结，其他的继续迭代；以前，对半分的后备步骤可能把一个已经算完的报价打乱。<bookmark mark='a'/>在基准曲面的全部{r['n']}个报价上：达到十位小数的迭代次数中位数是{r['median']:.0f}，九成在{r['p90']:.0f}次以内，最多{r['max']}次，那是一份{r['worst_T_days']:.0f}天、深度虚值的看涨期权。",
    'f"Now all {r[\'n\']} quotes solve at once.':
        "现在全部{r['n']}个报价同时求解。左边，灰色：真实的微笑；每个橙色的点从我们公司的初始猜测出发，跳到它上面。右边：最大误差，对数坐标。<bookmark mark='a'/>到第{int(np.argmax(hm < -9))}次迭代，最大误差已低于十的负九次方。<bookmark mark='b'/>红色的是从固定的50%出发的普通牛顿法：{r['naive_broke']}个报价被甩到无穷大或零以下，{r['naive_unfinished']}个再也没有回来。停下来预测一下：一个深度虚值的报价，比应有的价格高出远期的万分之一。它的波动率会错多少？在最慢的那个报价上，{100 * r['tick_shift']:.0f}个点。下一章：在真实的微笑曲线上运行求解器。散点图只显示绝对对数价内外程度不超过0.9、存储的正隐含波动率小于3的点。非有限存储迭代值略去，不挪到边缘。原有诊断把非有限误差记为9.99，有限尖峰则不设上限完整显示。",
    "Chapter twelve. The first smile, and the Surface's first row.":
        '第12章。第一条微笑曲线与基准曲面的第一行。',
    'Now invert every option traded that morning':
        "现在把那天上午汇总报价中的隐含波动率画出来，横轴是行权价与远期之比的对数，每个到期日一条曲线。停下来预测一下：若常波动率Black–Scholes模型成立，曲线是什么形状？<bookmark mark='a'/>同一到期日应当平坦，可它们却微笑、倾斜。微笑对尾部支付的定价不同于常波动率对数正态模型。这涉及风险中性价格，不识别真实世界的崩盘概率。忘掉远期也会画出偏斜，第13章会检查这种影响。<bookmark mark='b'/>虚线是Vega加权拟合的结果，每个到期日一个波动率。",
    'Put every expiry together':
        "把所有到期日放在一起，就是本系列的基准曲面：两百五十多个隐含波动率，分布在行权价和期限上，冻结在一个上午。本系列的每一个定价模型都会对它校准，并以它评分。前面的短期微笑又陡又高：那是美联储公布利率决定的上午。<bookmark mark='a'/>灰色线是Black–Scholes的最大努力，每个到期日一个平的波动率：每个到期日的水平对了，别的都不对。",
    'f"The first Surface row: one volatility per expiry has vega-weighted IV RMSE {ro':
        "Surface第一行：每个到期日一个波动率，样本内Vega加权隐含波动率均方根误差{row['rmse_in']:.2f}点，参数不变时次日为{row['rmse_out']:.2f}点。它们是加权平均，不是最差报价误差。11个采样期限的拟合总方差不下降；这项归一化采样检查不是对插值、持有成本或执行的一般无套利认证。<bookmark mark='a'/>后续模型使用同样冻结的报价。DVOL为{100 * d['dvol_ref']:.1f}%，插值得到的30天平值隐含波动率为{100 * d['atm30']:.1f}%。指数包含两翼且构造不同，两者差值不是跨日期不变的修正。",
    'Chapter thirteen. Dividends, borrow and the forward.':
        '第13章。股息、借券与远期。',
    'Carry changes the forward: dividends, foreign interest, or securities-lending in':
        "持有成本改变远期：股息、外币利率，或理想模型下的证券出借收入，以可再投资的收益率q进入公式。常利率下，b等于r减q。<bookmark mark='a'/>提高q，风险中性路径扇向下倾斜，看涨贬值、看跌升值。停一下：看涨持股Delta呢？<bookmark mark='b'/>它也下降，还包含收益率贴现。<bookmark mark='c'/>把借券费当成这种收益率，需要对称的交易权限和再投资。真实难借券约束可能打破等式，第9部分已作强调。",
    'In symbols, the replication of chapter two with one change':
        "用符号写，就是第2章的复制，只改一处：对冲里的股票把收益率q付给持有它的人。<bookmark mark='a'/>对应各项，方程的漂移就变成r减q。<bookmark mark='b'/>像第3章那样求解，价格就是写在远期上的公式：贴现因子乘以，远期乘以N(d1)，减去行权价乘以N(d2)，d从远期量起。<bookmark mark='c'/>用股票对冲多一个贴现，e的负qT次方；用远期上的期货对冲，就是按r贴现的N(d1)。",
    'The same lognormal forward formula serves several models, with their assumptions':
        "同一个对数正态远期公式可服务几种模型，但要说明各自假设。连续收益率给出Merton的股票或指数扩展，外币利率给出Garman–Kohlhagen外汇公式，理想借券收益也可类似处理。<bookmark mark='a'/>利率确定、期货价对数正态时，Black的1976年公式贴现其期望支付。反向比特币期权需要币计价记账：币贴现因子为1时，权利金等于未贴现的Black远期价值除以F。现货美元价值则为现价乘币权利金。把已贴现美元权利金除以远期会混淆单位。已知现金股息可用托管股息后的风险资产分量建模，这是一种模型选择，不是普遍精确的股息修正。",
    'f"On the Surface, Bitcoin\'s carry is real and measured.':
        "在基准曲面上，比特币的持有成本是真实的，可以测量。对每个到期日，我们公司从看涨看跌平价读出远期，年化基差，也就是远期与现货之比的对数除以时间，在每年{100 * cr.min():.1f}%到{100 * cr.max():.1f}%之间，随期限上升：这是以币作抵押借美元的价格。<bookmark mark='a'/>现在忘掉它。用现货代替远期、不计持有成本，反解每一个报价。看涨期权的隐含波动率偏高，看跌期权的偏低：{mid['days']:.0f}天时分别偏{mid['calls']:+.1f}和{mid['puts']:+.1f}个点，{last['days']:.0f}天时偏{last['calls']:+.1f}和{last['puts']:+.1f}。一个纯粹由记账造成的偏斜，随期限增大。第7题请你用手算估计它。持有成本也决定了何时提前行权。下一章。",
    'Chapter fourteen. Early exercise and the free boundary.':
        '第14章。提前行权与自由边界。',
    'European options exercise at expiry; American options allow earlier exercise. Fo':
        "欧式期权到期行权，美式期权允许提前行权。无股息股票且利率非负时，看涨期权的下界不低于立即行权价值，因此提前行权没有优势。Merton，1973年；结论需要这些利率和收益率假设。<bookmark mark='a'/>利率为正时，看跌期权可能因提前收取行权价而获益。行权边界是最优停止问题，一般有限期看跌期权没有初等闭式公式。",
    'f"The tree of chapter five solves it':
        "第5章的二叉树能解它，只需多一行：每个节点取立即行权和继续等待两者中较大的。一份一年期看跌期权，利率5%。蓝色的欧式看跌期权在深度实值时跌到收益之下：活着反而不如行权值钱，原因是利息。<bookmark mark='a'/>品红色的美式看跌期权从不这样：它碰到收益就沿着收益走。平值时它值{d['american_put']:.4f}，欧式的是{d['european_put']:.4f}：提前行权溢价是{d['american_put'] - d['european_put']:.2f}，也就是阴影部分。",
    'Here is the whole early-exercise premium':
        "这是完整的提前行权溢价，美式看跌期权减去欧式的，画在股价和剩余时间上，每一点都由一棵二叉树算出。远高于行权价时它很小：没人会行使虚值的看跌期权。<bookmark mark='a'/>股价下跌时它增大，低于某个价格后，它恰好等于立即行权与欧式价值之差。金色曲线，形状改变的地方，就是自由边界：对每个剩余时间，行权变为最优的那个股价。临近到期时它升向行权价，等待的时间越长，它离行权价越远。",
    'f"In symbols: optimal stopping.':
        "用符号写：最优停止。<bookmark mark='a'/>在边界之上，方程成立；在它之下，价值就是收益。<bookmark mark='b'/>跨过边界，价值和斜率都要连上：第8部分的光滑粘贴。<bookmark mark='c'/>在停止区域把收益代入方程，出来的是负r乘以K：行权价上的利息。<bookmark mark='d'/>对贴现后的看跌期权用伊藤引理，取期望，溢价就是这笔利息，在看跌期权处于已行权状态的每一刻赚取，并按处于边界之下的概率加权：金仁俊，1990年；卡尔、贾罗和迈内尼，1992年。用二叉树的边界，定位在节点之间，积分给出{a['kim']:.4f}，二叉树给出{a['tree']:.4f}：{gap_line}停下来预测一下：利率降到零，边界会去哪里？去零。",
    'f"a gap of {abs(gap):.3f}':
        '相差{abs(gap):.3f}，那是边界剩下的误差。',
    'f"Brennan and Schwartz studied finite differences for the American put in 1977. ':
        "Brennan和Schwartz在1977年研究美式看跌期权的有限差分。<bookmark mark='a'/>Barone-Adesi和Whaley在1987年的近似简化提前行权溢价的时间依赖，再数值求解临界价的非线性方程。价格为{a['baw']:.4f}，树为{a['tree']:.4f}；临界价{a['baw_critical']:.1f}，树为{a['smooth_critical']:.1f}，都是数值近似。<bookmark mark='b'/>{div_line}现金股息树使用托管股息模型，行权时点结论以这个模型、一个已知股息和非负利率为条件。",
    'With one cash dividend the tree exercises a call only':
        '只有一笔现金股息时，二叉树只在股票除息前的那一刻行使看涨期权。',
    "With one cash dividend the tree's call exercise nodes cluster":
        '只有一笔现金股息时，二叉树上看涨期权的行权节点聚集在除息日之前。',
    'Chapter fifteen. Selling volatility on real Bitcoin.':
        '第15章。在真实的比特币上卖出波动率。',
    'f"Does the mechanism appear in historical prices? Every day at eight from {ts_da':
        "真实历史价格中有没有这个机制？从{ts_date(b['start'][0], '%B %Y')}起，每天8点用DVOL给假想的30天美元看涨期权定价，再在币安每小时对冲，共{b['n']:,}个重叠窗口。DVOL包含整条微笑，不是平值看涨期权可成交的报价。<bookmark mark='a'/>橙色是起始DVOL，青色是随后30天的实际波动率，都对齐到窗口起点。窗口均值分别为{100 * b['mean_iv']:.0f}%和{100 * b['mean_rv']:.0f}%。<bookmark mark='b'/>实际波动率有时会大幅超过代理值。这是零利率、未建模融资和执行约束的历史模型实验。实现把DVOL小时收盘值按提供的K线时间戳对齐，并插值补齐12个缺失现货小时。这里未验证入场时数据已经可用，因此不是时点可得的策略回测。",
    'f"Each dot is one overlapping window: the volatility gap across, hedged profit p':
        "每个点是一个重叠窗口，横轴为波动率差，纵轴为每100美元的对冲盈利。样本相关系数{corr:.2f}；Gamma权重使结果依赖路径。<bookmark mark='a'/>账本把Gamma、Theta和残差分开。这里残差显示的是绝对值均值，不是最大误差的上界。",
    'f"Across {b[\'n\']:,} windows, mean gross profit is {b[\'mean\']:.2f} per hundred on':
        "{b['n']:,}个窗口的毛利均值为每100美元{b['mean']:.2f}，平均模型权利金{np.mean(b['premium']):.2f}；{100 * b['p_win']:.0f}%的窗口盈利。每30天取一个窗口，{b['nonoverlap_n']}个不重叠窗口的均值为{b['nonoverlap_mean']:.2f}，普通标准误{b['nonoverlap_se']:.2f}，但它们仍可能相关。<bookmark mark='a'/>现货每单位成交额收2基点，均值降到{b['mean_cost']:.2f}，还没有期权价差和融资成本。Surface单个快照里DVOL比平值高{gap_pts:.1f}点。把这个差套到所有年份只能作敏感性示例，得到{adj:.2f}，并非可执行收益的估计。币结算还改变计价单位和对冲记账；这里的美元看涨实验没有实现反向合约。",
    'f"Replay all {n} non-overlapping windows. Below is each profit; on the right its':
        "重放全部{n}个不重叠窗口。下方是每次盈利，右边是Gamma和Theta，上方是累计均值及逐点90%的区块自助法区间。5个种子各重采样200次，显示区间计算的蒙特卡洛波动，不是5段独立市场历史。<bookmark mark='a'/>{band_line}区间依赖重采样假设，反复查看也不构成同时置信声明。结果描述的是按DVOL定价的模型实验。",
    'f"Even early on, the band sits above zero':
        "即使在一开始，这条带也在零之上，最后落在{r['final_lo']:.2f}到{r['final_hi']:.2f}之间。",
    "f'It lifts clear of zero only from":
        "直到{ts_date(fp, '%B %Y')}它才离开零，最后落在{r['final_lo']:.2f}到{r['final_hi']:.2f}之间。",
    'f"The worst month began on':
        "最糟的一个月从{ts_date(b['worst_start'], '%d %B %Y').lstrip('0')}开始，按{100 * b['worst_iv']:.0f}%卖出；三周后日元套息交易平仓，8月5日纽约开盘前VIX报到65。那个月的已实现波动率是{100 * b['worst_rv']:.0f}%；卖方亏了{-b['worst']:.2f}。许多小额盈利，加上偶尔一笔大亏损，偏偏发生在其他一切也在亏的时候：第12部分的“波动率末日”是加了杠杆的同一个故事。这个公式最糟的一天远在比特币之前。下一章：1987年10月。",
    'Chapter sixteen. October 1987.':
        '第16章。1987年10月。',
    'f"By the mid-1980s the hedge had become a product.':
        "到1980年代中期，这种对冲已经成了一种产品。海恩·利兰和马克·鲁宾斯坦，与约翰·奥布莱恩一起，出售投资组合保险：给养老基金的组合垫一个底，办法是用股指期货复制一份看跌期权，这正是鲁宾斯坦和利兰1981年发表的配方。<bookmark mark='a'/>复制看跌期权意味着价格下跌时持有更少的股票：在比市场低5%的一年期底线下，下跌10%会让这个模型卖掉{100 * ins['sold_on_10pct']:.0f}%的股票。<bookmark mark='b'/>在我们公司里：每天四行。",
    'f"Run it on the real 1987':
        "在真实的1987年上运行它，从7月1日开始，用肯尼斯·弗伦奇的日收益：白色是被保险的组合；蓝色是市场；黄色是股票的占比，10月5日是{100 * o5['w']:.0f}%。<bookmark mark='a'/>市场连跌数日，规则就卖出：到16日星期五是{100 * o16['w']:.0f}%。<bookmark mark='b'/>星期一市场跳空下跌，组合里仍有{100 * o19['w']:.0f}%是股票，直接穿过了底线；第二天早上，模型卖到只剩{100 * o20['w']:.0f}%。10月结束时是{eo['V']:.1f}，{floor_word}底线{ins['floor_value']:.1f}。<bookmark mark='c'/>布雷迪委员会的数字：六百亿到九百亿美元的资产买了保险，模型在下跌10%时要卖掉五分之一以上，而到那个星期一，本应卖出的一百二十亿美元里，实际卖出的不到四十亿。停下来预测一下：当所有人都遵循这条规则时会发生什么？",
    'f"The Brady Commission described a feedback mechanism: portfolio-insurance sales':
        "布雷迪委员会描述了一种反馈机制：组合保险卖盘压低期货，指数套利交易可能把压力传到现货，模型于是进一步卖出。这是多种机制之一，不表示每个投资者都遵循同一规则。<bookmark mark='a'/>French的市值加权美国市场下跌{-100 * c['ret']:.1f}%，标普500跌20.5%。对数收益为此前一年估计日标准差的{-c['z']:.0f}倍。代入高斯模型的尾概率极小，但不是数学上的不可能。Jackwerth和Rubinstein对另一个期货计算报告约10的负160次方。这些比较质疑的是校准后的分布模型，不是直接观测到的事件概率。",
    'And then options changed.':
        "然后期权变了。1987年10月之前，指数期权的隐含波动率几乎不依赖行权价：市场大致按Black–Scholes的世界定价。之后，虚值看跌期权，也就是崩盘保险，永久地比公式的单一波动率所允许的更贵。投资组合保险商之一的马克·鲁宾斯坦在1994年记录了这一变化。这就是第12章的偏斜，诞生于此。<bookmark mark='a'/>社会学家唐纳德·麦肯齐把这一事件读作述行性的一个案例：十四年里，公式帮助市场变得像公式，然后，在一天之内，市场不再像它了。第12部分讲的就是这个偏斜。十年后，它的两位创造者获得诺贝尔奖；又过一年，他们参与管理的基金崩溃了。下一章。",
    'Chapter seventeen. The Nobel, and then LTCM.':
        '第17章。诺贝尔奖，然后是LTCM。',
    'In October 1997 Merton and Scholes received the Nobel prize.':
        "1997年10月，默顿和斯科尔斯获得诺贝尔奖。两人都是一家对冲基金的合伙人：长期资本管理公司，由约翰·梅里韦瑟于1994年创立，他曾执掌所罗门兄弟的债券套利部门。<bookmark mark='a'/>它的交易是对冲后的价差：买入便宜的债券，卖出几乎相同但较贵的债券，等待价格收敛。它也卖出波动率，即长期指数期权，规模之大，据罗杰·洛温斯坦报道，其他交易员称它为“波动率中央银行”。按美国会计总署的统计，1997年底它的资产负债表约为资本的28倍，表外还有超过一万亿美元的衍生品。<bookmark mark='b'/>1998年8月，俄罗斯违约。投资者转向流动性更好的资产；LTCM的许多收敛头寸同时出现不利变动，隐含波动率跳升。到8月底，它亏掉了一半以上的资本，到9月，将近九成。",
    'f"This is the Cboe VIXCLS historical series for 1998, reconstructed under the la':
        "这是Cboe的1998年VIXCLS历史序列，按后来标普500方法回算，与当时如今称为VXO的指数不同。7月1日为{v['jul1']:.0f}。<bookmark mark='a'/>峰值为{v['peak']:.0f}。下方是每波动率点固定空头Vega的示意估值，省略Theta、凸性、期限结构和融资，不是LTCM真实期权组合或收益。波动率上升可能引起亏损和保证金要求，具体结果取决于合约与其余持仓。",
    'On the twenty-third of September':
        "9月23日，纽约联邦储备银行召集了十四家银行和证券公司，它们向基金注资大约35亿美元，接管了它，并慢慢平仓。大多数价差最终确实收敛了。停下来预测一下：如果能连续交易，对冲就没有风险。还有什么必须成立？<bookmark mark='a'/>被打破的，是本部分每一个对冲背后的假设：你能一直交易，你能为头寸融资直到它收敛，而其他人并不都在做同一笔交易。1987年打破了第一条。1998年三条全打破了。第41部分会用数据讲这个故事：保证金螺旋、甩卖，以及为什么流动性是任何公式都定不了价的风险因子。下一章：今天仍在运转的公式。",
    'Chapter eighteen. Industry: the formula at work.':
        '第18章。业界：公式如何谋生。',
    'How does the formula earn a living?':
        "这个公式靠什么谋生？在芝加哥期权交易所的交易池里，费希尔·布莱克出售印好的理论价格表，每个到期日一列，每个行权价一行。停下来预测一下：为什么要买一张表，而不是自己算？速度：在喊叫的人群里，读一个数比输入五个参数快。<bookmark mark='a'/>唐纳德·麦肯齐和尤瓦尔·米洛重建了接下来的事：做市商卖出价格表说贵的，买入它说便宜的，把价格拉向模型。<bookmark mark='b'/>公司围绕它成长起来。奥康纳联合公司1977年在芝加哥创立，据后来的引述，《纽约时报》1989年称它是美国金融期权交易所里最大的做市商；瑞士银行公司在1990年代初收购了它。",
    'On a modern desk the formula is less a model than a language.':
        "在现代的交易台上，这个公式与其说是模型，不如说是一种语言。价格用隐含波动率报，头寸用Vega，也就是每个波动率点多少美元来计，限额用希腊字母来设。公式是在波动率和钱之间翻译的词典。交易台常引用里卡多·雷博纳托的一句话：隐含波动率是一个错误的数，放进一个错误的公式，得出正确的价格。<bookmark mark='a'/>还有更尖锐的异议。埃斯彭·豪格和纳西姆·塔勒布在2011年主张：早在1973年之前，交易员就用经验法则和平价关系给期权定价，而且根本没有人把这个公式当作模型来用。把它当作一种论点，而不是测量结果；第12章的微笑是双方都援引的证据。",
    'f"At the forward, the undiscounted Black call value is F times the quantity two ':
        "平值远期处，未贴现Black看涨价值等于F乘括号内的2N减1，N的输入为二分之一sigma乘根号T。总波动率小时，近似为0.4F乘sigma乘根号T。<bookmark mark='a'/>对每个Surface到期日，用插值平值隐含波动率计算两个公式。总波动率{ind['s_max']:.2f}时，本例最大相对差为{100 * ind['max_abs_rel']:.1f}%。这是近似公式与Black模型价值的比较，不是独立可成交的平值报价比较。需要现值时，两边都要一致贴现。",
    "The formula sits in the plumbing. Futures options often use Black's lognormal co":
        "公式也在市场基础设施里。期货期权常用Black对数正态约定；负标的价格需要兼容模型，例如Bachelier或平移模型。VIX则使用一条期权价格带。<bookmark mark='a'/>Coinbase于2025年8月完成收购Deribit。iShares比特币信托期权于2024年11月19日在纳斯达克开始交易，纳斯达克报告首日353716份合约。这些是有日期的行业事实，不验证某个定价模型。",
    'Chapter nineteen. Frontier: 2023 to 2026.':
        '第19章。前沿：2023至2026年。',
    "Fifty years on, chapter eleven's problem is still a race.":
        "五十年后，第11章的问题仍是一场竞赛。仅在2026年：Schadner把隐含波动率写成封闭形式，作为逆高斯分布的一个分位数。法比安·勒弗洛克和杰雷克·希利问它能有多快。<bookmark mark='a'/>一个包括布兰卡·霍瓦特和汉斯·比勒在内的团队，把彼得·耶克尔的求解器包装成一个可微分的层，按他们的统计，在一块显卡上每秒反解十七亿九千万个报价。萨米拉·阿米里扬和尤尼斯·布泰布训练了一个带门控的神经网络来给出初始猜测，再用两步豪斯霍尔德迭代收尾。<bookmark mark='b'/>连推导也焕然一新：第3章的那条路，从高斯核到看涨期权价格，现在已经被计算机证明助手逐行检验过。这些都是预印本：把它们当作主张来读，而不是定论。",
    'f"A small two-input network learns total volatility from {nv[\'n_train\']:,} synth':
        "小型双输入网络用{nv['n_train']:,}份合成报价学习总波动率，训练5个种子。这是教学实现，不是带门控Householder方法的复现。右边保留每个训练损失记录和完整种子范围；左边是种子0在各检查点对输入报价隐含波动率的预测，坐标使用对数刻度。未训练预测最高达到{100 * max(nv['snaps'][keys[0]]):.0f}%，完整显示。<bookmark mark='a'/>各种子报价误差中位数再取中位数为{100 * g0:.2f}点，{cmp_word}Corrado–Miller的{100 * nv['cm_med']:.2f}。一步牛顿后的中位数为{100 * g1:.2f}点，两步为{two_txt}。{worst_line}中位精度不认证最坏情形，我们也未与论文进行运行时间基准比较。",
    'f"but the worst quote is still':
        '但最差的报价仍然差{100 * g2max:.0f}个点：深度虚值，在那里第11章那张平坦的曲面会把牛顿法甩来甩去。这就是为什么那些论文按区域给网络加门控、用三阶的一步收尾，也是为什么我们公司保留了它的区间括号。',
    'and even the worst quote of the Surface is at rounding level.':
        '连基准曲面上最差的报价也到了舍入误差的水平。',
    'Three more lines of work carry this part forward.':
        "还有三条研究线索把本部分推向前方。卡罗尔·亚历山大和合作者给Deribit实际挂牌的反向期权定了价。Matic、Packham和Härdle展示了对冲比特币期权真正需要什么：随机波动率和跳跃，而不只是Delta。<bookmark mark='a'/>约翰·赫尔和艾伦·怀特修正了Black–Scholes的Delta，考虑隐含波动率随价格的变动，即最小方差Delta；约翰内斯·鲁夫和王伟冠发现，这类简单回归的效果与神经网络相当。第13部分在比特币上拟合它。深度对冲、粗糙波动率和零日期权各有自己的部分。",
    'Part ten. A stock-and-cash strategy replicates a vanilla payoff under the stated':
        '第10部分。在明确的无摩擦扩散假设下，股票与现金策略复制普通期权支付。热核、风险中性期望和树得到同一价格。Gamma给方差差加权。离散对冲留下误差，跳跃带来未张成的风险。成本改变对冲；Leland波动率发散，仍不代表看涨价格无界。价格严格在边界内时，隐含波动率唯一，但数值条件仍重要。持有成本和行权约定也重要。比特币示例用模型权利金和重叠历史窗口，危机案例展示假设失效的代价。',
    'Three desk questions, the kind trading firms ask':
        "三个交易台问题，交易公司面试时会问的那种。心算一份平值看涨期权的价格：答案大约是0.4乘以σ乘以S乘以T的平方根，这里是8，精确值是7.97。<bookmark mark='a'/>你持有一份跨式组合，股价一周不动：你亏了一周的Theta，那是你没有用上的Gamma的价格。<bookmark mark='b'/>临近到期时平值数字期权的Delta：它会爆炸，这就是为什么卖出数字期权的交易台用很窄的看涨价差来对冲它们。完整的解答在本部分的说明里。",
    'And nine problems to work through':
        '还有九道习题：由公式推出平价关系和Delta，二叉树的鞅概率，波动率交易员的粗略估算，利兰波动率及其推导，提前行权，以及忘掉远期画出的偏斜。另外两道是资格考试题：退出时间的矩，以及最优带宽。英文和中文的解答都在本部分的说明里。',
    'Where this comes back:':
        '这些内容会在哪里再次出现：波动率交易员的公式在第11、12和32部分；基准曲面的新行在第12、13、14和17部分；作为控制问题的对冲在第17、37和38部分；二叉树、方程和模拟在第15和16部分；持有成本在第22部分；LTCM在第41部分。',
    'The textbook chapters this part covers':
        '这是本部分覆盖的教科书章节，以及它依据的论文。其中每一个数字，都由本系列自己的代码根据公开数据算出：Deribit的期权成交和DVOL，币安的价格，以及肯尼斯·弗伦奇的市场收益。',
    'The House now has a volatility desk:':
        "我们公司现在有了一个波动率交易台：一个定价器和一个热核求解器，一个也能为成本定价的对冲器，一个隐含波动率求解器，美式期权的近似，投资组合保险，以及用来评分的基准曲面。<bookmark mark='a'/>接下来，第11部分让一位交易员坐到这张台前：把头寸看成希腊字母，Gamma剥头皮，各种策略，以及做市商的账本。",
    'For the researcher: Chapter 9 hedged at equal times':
        '写给研究者：第9章在等间隔的时间对冲，发现误差像交易次数平方根的倒数那样下降。但没人规定交易必须等间隔。这里说明选择何时交易值多少，以及说明它最多能走多远的定理。',
    'Start from Chapter 9.':
        "从第9章开始。<bookmark mark='a'/>两次再平衡之间，对冲漏掉了二分之一伽马乘以平方变动，再减去它的平均：二分之一伽马、sigma平方、S平方、delta t，乘以Z平方减一。<bookmark mark='b'/>Z平方减一的方差是二。<bookmark mark='c'/>N步，每步方差正比于delta t的平方：总方差像N分之一那样下降，N乘以它趋于T的一半，乘以伽马平方、sigma四次方、S四次方积分的期望。对我们的三个月期期权，这个常数是十一点九。",
    'Locally freeze gamma, volatility and spot, approximating the price increment by ':
        "在局部冻结Gamma、波动率和现价，把价格增量近似为零漂移的算术布朗运动。<bookmark mark='a'/>绝对位移首次达到a时交易。这个局部模型中，退出时位移的平方严格等于a平方。<bookmark mark='b'/>首阶对冲误差随机，是因为退出时间随机。<bookmark mark='c'/>在停止鞅和可积性保证下，布朗退出时间的方差是平均退出时间平方的三分之二。<bookmark mark='d'/>冻结系数后的误差方差为六分之一Gamma平方乘a四次方，等平均长度的固定时间区间则为二分之一。这3倍差异是局部渐近比较，不是GBM有限带宽的精确恒等式。",
    "Allow the band to depend on current information. <bookmark mark='a'/> Minimize l":
        "让带宽依赖当前信息。<bookmark mark='a'/>在预期交易次数预算下，最小化首阶误差方差。<bookmark mark='b'/>本例凸看涨期权的局部拉格朗日条件给出价格带宽正比于Gamma的负二分之一次方，对应Delta阈值正比于Gamma平方根。<bookmark mark='c'/>预期交易次数乘终值误差方差趋近屏幕上的常数，本例2.64，等时间为11.9。柯西–施瓦茨不等式给出三分之一的比较。<bookmark mark='d'/>Fukasawa定理在结构、细化和一致可积条件下，对一类可容许的停止时刻规则，以误差的预期二次变差衡量风险。在这里零漂移、平方可积的例子中，它等于终值方差。这是渐近结论，不保证有限交易次数下最优。",
    'Simulate all of them on fine paths.':
        "在精细的路径上模拟所有规则。<bookmark mark='a'/>红色的等时间：误差像根号N分之一那样下降，落在公式预测的线上。<bookmark mark='b'/>蓝色的固定宽度价格带：斜率相同，线更低，标准差略多于一半。<bookmark mark='c'/>绿色的、正比于根号伽马倒数的带：又低一截。要用等时间达到它的误差，需要四倍半的交易次数。",
    'The constants.':
        "这些常数。<bookmark mark='a'/>等时间：理论十一点九，模拟值随N增大向它攀升。<bookmark mark='b'/>固定宽度的带，无论在价格上还是在Delta上，共享一个常数，约为四。<bookmark mark='c'/>最优带：理论二点六四，在二百五十六次交易时模拟为二点八，仍在从上方逼近。",
    'f"On Bitcoin minute closes, these thirty-day calls start every fifteen days in 2':
        "真实比特币分钟收盘价上，2019至2020年每15天开始一份30天看涨期权，窗口相互重叠。每份都用自己未来才实现的波动率；公共带宽阈值也用全部这些窗口调到目标平均交易次数，两者都是事后选择。<bookmark mark='a'/>约16次交易时，误差标准差为模型权利金的{f['time']['sd_pct_premium']:.0f}%对{f['fukasawa']['sd_pct_premium']:.0f}%。<bookmark mark='b'/>64次时为{l_['time']['sd_pct_premium']:.0f}%对{l_['fukasawa']['sd_pct_premium']:.0f}%。这项描述性时点比较不含成本，不是可部署策略的检验，也未识别正均值的成因。",
    'Three research directions, each requiring a precise model and objective. <bookma':
        "三个研究方向，都需要先明确模型和目标。<bookmark mark='a'/>把组合的比例成本与交易次数预算放在一起。成本敏感带宽和更广泛的离散化理论已经存在，本例没有解决联合设计的实际问题。<bookmark mark='b'/>量化只有几十次交易时的有限频率修正和不确定性。<bookmark mark='c'/>在既有研究之上，把选定准则扩展到跳跃、粗糙波动率和多资产，例如Rosenbaum和Tankov的工作。这些是需要具体定义的项目方向，不是说整个主题都尚未解决。",
    'Pause and predict. Equal-time hedging needs two hundred':
        '暂停预测。等时间对冲需要二百五十六次交易才能达到某个误差。用两个常数，十一点九和二点六四，最优带大约需要多少次？',
}

ZH.update({'Match variance C divided by N.': '令方差C除以N相同。带宽规则需要256乘2.64再除以11.9，渐近近似下约57次交易。'})
