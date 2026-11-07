"""Chinese narration for quant11: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第11部分：交易期权'

CHAPTERS = {
    'Hook': '伽马对时间损耗',
    'Greeks': '1. 头寸即希腊字母，以及损益归因',
    'Scalp': '2. 真实路径上的伽马剥头皮',
    'Frequency': '3. 多久对冲一次',
    'SecondOrder': '4. vega、vanna与volga',
    'Strategies': '5. 策略：各押注什么，又赚了多少',
    'Premium': '6. 期权收益中的波动率溢价',
    'VRP': '7. 预测者的优势，以及下多大的注',
    'MarketMaker': '8. 做市：价差',
    'Inventory': '9. 库存，以及一个会学习的做市商',
    'Hedging': '10. 对冲整本账',
    'Expiry': '11. 到期与钉住风险',
    'Early': '12. 提前行权、合成头寸与股息博弈',
    'Dispersion': '13. 离散度与隐含相关性',
    'India': '14. 印度的到期日热潮，以及彩票的回报',
    'Case': '15. 案卷：SEBI与简街（指控）',
    'ShortVol': '16. 危机档案：做空波动率爆仓之时',
    'Industry': '17. 业界：谁在为期权做市',
    'Frontier': '18. 前沿：学会交易期权',
    'Research': '写给研究者：基于需求的期权定价',
    'Outro': '报价引擎、回顾、交易台问题与习题',
}

ZH = {
    'Part eleven. Trading options: Greek exposures, hedging, quotes, inventory and ex':
        '第十一部分，期权交易：希腊值敞口、对冲、报价、库存与到期。历史重放用于讲解记账和模型局限，并非可执行策略收益。',
    'A desk question. Long a straddle, delta-hedged, in a quiet week: how do you lose':
        "一个交易台问题：买入跨式、Delta对冲，在平静的一周如何亏损？<bookmark mark='a'/>零利率与收益率下，局部首阶分解包含平方变动的Gamma收益、Theta的模型方差支出，以及隐含波动率变化的Vega项。现价不动仍损失Theta，隐含波动率下降也损害多Vega跨式。利润取决于Gamma加权变动、标记变化、高阶项与成本，而非单个实际波动率数字是否高于隐含波动率。",
    'f"A hypothetical dollar straddle on the real May 2021 spot path. The model price':
        "在真实的2021年5月现货路径上，考察假设美元跨式。模型以DVOL的{100 * s['iv']:.0f}%给30天平值跨式定价，按小时无成本对冲；DVOL是指数代理，不是跨式成交报价。<bookmark mark='a'/>5月19日崩盘时，现价远低于行权价；全月实际波动率为{100 * s['rv']:.0f}%。跨式资金翻倍了吗？<bookmark mark='b'/>模型损益为{s['pnl']:.1f}，权利金{s['premium']:.1f}。接近行权价时Gamma条增长，现价离开后放慢。变动顺序与发生位置很重要；小时收盘输入、插值和反向合约约定限制了交易解释。",
    'How did options become a trade in volatility?':
        "期权是怎么变成波动率交易的？1973年，芝加哥期权交易所开业，推出标准化合约，同年布莱克和斯科尔斯发表论文；没过几年，交易员就带着印好的模型价值表走进交易大厅。<bookmark mark='a'/>1985年，劳伦斯·格洛斯滕和保罗·米尔格罗姆解释了做市商的价差为什么存在，海恩·利兰解释了对冲要花多少钱。<bookmark mark='b'/>1987年，黑色星期一永久地重新给指数看跌期权定了价，而就在几个月前，萨斯奎哈纳刚刚成立，专做期权市场。<bookmark mark='c'/>然后是卖出波动率的几十年，以及它崩溃的日子：2018年2月和2020年3月。2021年，散户发现了短期期权；2024年，拥有按合约数计全球最大衍生品交易所的印度，开始给自己的热潮降温。",
    'The plan. Positions as Greeks':
        '本部分的安排。头寸即希腊字母，逐项解释真实一天的损益，以及每种结构押注的是什么。真实路径上的伽马剥头皮，以及多久对冲一次。波动率溢价、预测者的优势，以及下多大的注。做市：价差、库存、一个会学习的做市商，以及对冲整本账。到期、钉住、提前行权和离散度。印度的到期日热潮，以及监管机构对简街的案件，该公司对此提出异议。然后是一份危机档案、业界和前沿。',
    'In the House, the volatility desk opened in Part ten.':
        "在我们的公司里，波动率交易台在第10部分开张。<bookmark mark='a'/>这一部分给它配上期权报价引擎：把账本看成希腊字母，报价朝库存的反方向倾斜，以及知道交易成本的对冲。",
    'Chapter one. Positions as Greeks, and the profit and loss explain.':
        '第1章。头寸即希腊字母，以及损益归因。',
    'f"An options trader\'s book is one surface':
        "期权交易员的账本是一张曲面：它的价值随标的价格和剩余时间而变。这是一个跨式组合的曲面：沿执行价的一道山谷，到期时变成收益的V字。<bookmark mark='a'/>取今天，距到期三十天：黄色的切片。在执行价处画它的切线，就是白线，斜率是delta。切片在切线两侧都向上弯：这个碗就是伽马，价格变动dS时账本赚二分之一伽马乘dS的平方，就是绿色那段长度。<bookmark mark='b'/>现在让十天过去。整个切片朝收益曲线下沉：这段下降，红色那段长度，就是时间损耗，是账本为这个碗付的钱。<bookmark mark='c'/>伽马多头交易员押注绿色胜过红色：押注标的在这十天里的变动超过约{dS:.1f}，也就是波动率乘以时间的平方根。",
    'f"Now the algebra. A finite-step Taylor approximation in spot, time and implied ':
        "现在看代数。现价、时间与隐含波动率的有限步长泰勒近似给出Delta、Gamma、Theta、Vega，现价与波动率的混合导数Vanna，以及波动率的二阶导数Volga。<bookmark mark='a'/>画面闭式公式针对零利率、零收益率的普通欧式看涨期权；组合希腊值是各头寸之和。<bookmark mark='b'/>固定模型波动率时，Black–Scholes把Theta与Gamma联系起来。<bookmark mark='c'/>Delta对冲步长的首阶损益是二分之一Gamma乘现价平方，再乘平方收益减模型方差乘步长。波动率50%时，日度首阶盈亏平衡变动多大？<bookmark mark='d'/>按日历日约{be:.1f}%。高阶变动、隐含波动率变化、跳跃和成本都会改变比较。<bookmark mark='e'/>对每个普通期权，Vega等于波动率乘剩余时间乘现价平方乘Gamma。共同波动率与到期日下，多Gamma意味着多Vega；跨期限或波动率标记时，整个组合没有这一比例。",
    'f"In the House this is one function.':
        "在我们的公司里，这就是一个函数。一本账是一串期权腿；它的希腊字母就是各条腿的和。<bookmark mark='a'/>交易台用现金来报这些数：delta以标的的美元计，伽马是价格变动百分之一时的利润，vega按每个波动率点，theta按每天。这是Surface那天的一本五条腿的比特币账本：买入一个平值跨式组合，卖出两份低百分之十的看跌，买入一份高百分之十的看涨。<bookmark mark='b'/>运行它。这本账持有{c['delta']:,.0f}美元的delta多头，价格变动百分之一时伽马带来{c['gamma_1pct']:.0f}美元，每个波动率点{c['vega_pt']:.0f}美元，每天付出{-c['theta_day']:.0f}美元的时间损耗。",
    'f"Every morning a risk system does what this chart does':
        "每天早上，风险系统都做这张图做的事：损益归因。把这本账带到第二天的Surface上。隔夜比特币变动了{100 * e['move']:+.1f}%，三十天波动率从{100 * e['atm0']:.1f}%降到{100 * e['atm1']:.1f}%。<bookmark mark='a'/>逐项拼出这一天。delta贡献了大部分，{e['delta']:,.0f}美元。伽马加了{e['gamma']:,.0f}，theta拿走{-e['theta']:,.0f}，vega是{e['vega']:,.0f}。<bookmark mark='b'/>然后是交叉项：vanna{e['vanna']:+,.0f}，因为现货和波动率一起下跌；volga只有几美元。<bookmark mark='c'/>完整重新估值亏了{-e['actual']:,.0f}，而{branch}归因失败时，交易台就有一项它没在衡量的风险。伽马是最值得关注的一项。下一章：在真实路径上交易它。",
    "f'the six terms explain all but":
        '这六项解释了除{share:.1f}%以外的全部。',
    "f'{share:.0f} percent is left over":
        '剩下{share:.0f}%：对二阶级数来说，这一天的变动太大了。',
    'Chapter two. Gamma scalping, on a real path.':
        '第2章。真实路径上的伽马剥头皮。',
    'Here is the scalper at work, hour by hour.':
        "这是剥头皮者逐小时的工作。每个小时，对冲都重置为跨式组合的delta。因为跨式组合是伽马多头，对冲总是逆市交易：下跌后买入，就是绿点，上涨后卖出，就是红点，每个来回都锁定一点波动的收益。<bookmark mark='a'/>月中比特币下滑时，跨式组合的delta趋向负一，对冲一路买入，最后几乎持有一整枚比特币。<bookmark mark='b'/>崩盘之后，执行价已经很远。跨式组合变成了一份深度实值的看跌期权，几乎是线性的，伽马很小，对冲几乎不再交易，而时间损耗还在继续收费。",
    'Why so little, in so violent a month?':
        "这么剧烈的一个月，为什么赚这么少？看看伽马住在哪里。这片地形是跨式组合的美元伽马，即伽马乘S的平方，随价格和日期变化：也就是每一次平方变动值多少钱。它是沿执行价的一道山脊，越接近到期越尖锐。<bookmark mark='a'/>现在把真实路径放上去，黄色那条。前两周比特币在执行价附近徘徊，路径爬上了山脊。<bookmark mark='b'/>然后它滑了下去，19日的崩盘，也就是全年最大的变动，发生在下面的低地上，在那里一次平方变动几乎什么都赚不到。",
    'f"Here is the proof that order matters.':
        "这是顺序重要的证明。保留这个月的七百二十个小时收益率，把顺序打乱两千次。每个打乱后的月份，已实现方差都完全相同。<bookmark mark='a'/>但对冲跨式组合的利润到处都是，平均为{sh['mean']:.1f}。<bookmark mark='b'/>那真实的月份呢？{real:+.1f}：{say}先慢慢滑离执行价、再在低地上崩盘，几乎是最差的顺序。<bookmark mark='c'/>停下来预测一下：把崩盘挪到第二天。<bookmark mark='d'/>{then}",
    "f'only {pct:.1f} percent of the reorderings":
        '只有{pct:.1f}%的打乱顺序赚得更少。',
    "f'{pct:.0f} percent of the reorderings":
        '{pct:.0f}%的打乱顺序赚得更少。',
    "f'It earns more, {early:+.1f}, but far less":
        '它赚得更多，{early:+.1f}，但远少于打乱后的平均：崩盘来得早，比特币整个月都远离执行价。',
    "f'It earns more, {early:+.1f}: the big moves":
        '它赚得更多，{early:+.1f}：大的变动现在发生在现货靠近执行价的时候。',
    "f'It earns even less":
        '它赚得更少，{early:+.1f}。',
    'f"In symbols. Sum the leading step identity: squared returns receive the dollar-':
        "用符号写出来：把步长首阶恒等式相加，每个平方收益按当时的美元Gamma加权，高阶项和跳跃项保留在余项中。<bookmark mark='a'/>给定路径的损益由路径决定，不只是实际方差的函数；重排变动会改变权重，洗牌实验说明这种依赖。<bookmark mark='b'/>对连续路径、零利率与收益率，负两倍对数支付使二分之一Gamma乘现价平方等于1。它的静态虚值期权条带权重为2除以行权价平方，再加连续股票对冲便得到连续二次变差。有限个平方收益之和是采样近似，跳跃还需修正；第十二部分会推导复制。<bookmark mark='c'/>这里是House的有限步长账本。五月路径的Gamma项为{s['gamma'][-1]:+.1f}，Theta项为{s['theta'][-1]:+.1f}，净损益{s['pnl']:+.1f}，余项仍保留。Gamma scalping就是对冲；下一章看频率。",
    'Chapter three. How often to hedge.':
        '第3章。多久对冲一次。',
    'f"Part ten showed that hedging at discrete times':
        "第10部分说明，离散时点对冲会留下误差。那么剥头皮者该多久对冲一次？让三个人在同一个月、同一个跨式组合上赛跑。一个每小时再对冲，绿色；一个每天一次，橙色；还有一个只在价格自上次交易以来变动百分之二时才交易，金色。<bookmark mark='a'/>看它们的对冲：每小时的是一条平滑曲线，每天的是一道台阶，按变动触发的只在有事发生时才迈一步。<bookmark mark='b'/>它们的账目在旁边赛跑。{race_say}",
    "f'They end within {spread:.1f}":
        '它们最后相差不到{spread:.1f}：在一个月里，变动的顺序比规则更重要。',
    'f"They end {spread:.1f} apart':
        '它们最后相差{spread:.1f}：在一个月里，规则的时点可以很要紧。',
    'f"Now every month.':
        "现在看每一个月。从2021年4月到2025年11月，每周按DVOL买入一个三十天跨式组合，共{f['n']}个，用三条规则分别对冲。每个点是一个跨式组合：它的利润，对应已实现波动率超过隐含波动率多少。<bookmark mark='a'/>这些点云沿着差值排成一线，正如第10部分的恒等式所要求的。{mean_say}<bookmark mark='b'/>频率买到的是精度。标准差从每天对冲的{d['sd']:.2f}降到每小时的{h['sd']:.2f}，利润也更紧密地跟着波动率差：相关系数{d['corr']:.2f}对{h['corr']:.2f}。<bookmark mark='c'/>而精度要花钱。每笔交易收十个基点，每小时对冲者的均值降到{hc['mean']:.2f}，每天对冲者是{dc['mean']:.2f}。所有均值都是负的，原因相同：DVOL高于实现的波动率，也就是第6章的溢价。",
    'The means barely differ':
        '均值几乎没有差别：更频繁地对冲，平均来说并不让交易更好。',
    'Here the means do differ':
        '这里均值确实不同，差别超过了噪声。',
    'f"Under a correctly specified continuous diffusion and regular hedging, the lead':
        "在模型正确的连续扩散和规则对冲条件下，中心化对冲首阶误差的标准差按步长平方根缩放；这不证明频率永远不改变均值。<bookmark mark='a'/>局部冻结Gamma的比较可单独考察自相关：平稳小时收益的日方差等于24倍小时方差，再加加权自协方差。<bookmark mark='b'/>负自相关使小时平方变动和的期望更大；比特币缓存的日方差与24倍小时方差之比为{vr:.3f}，它是描述统计，不是完整盈利检验。<bookmark mark='c'/>价格带针对变动幅度，但小时网格可能超越阈值，交易之间Theta仍在累积；不能普遍保证更少交易保持同等精度。<bookmark mark='d'/>正自相关时，冻结Gamma比较倾向于让变动延续；Gamma变化、跳跃、漂移和成本都可能改变结论。下一章看波动率希腊值。",
    "f'For Bitcoin from 2021 to 2025 the daily variance":
        '对2021到2025年的比特币，日方差是二十四个小时方差的{vr:.3f}倍：日内只有一丝均值回复，小到无关紧要。',
    "f'For Bitcoin from 2021 to 2025 the ratio":
        '对2021到2025年的比特币，这个比值是{vr:.3f}：频率改变了你得到的报酬。',
    'Chapter four. Vega, vanna and volga':
        '第4章。vega、vanna与volga：风险逆转与蝶式价差。',
    "Chapter one's Taylor series had two cross terms.":
        "第1章的泰勒级数有两个交叉项。为了看清它们，把vega本身画成一张曲面，横轴是执行价和隐含波动率，对象是一份三十天期权。<bookmark mark='a'/>三面旗子：二十五delta的看跌、平值期权、二十五delta的看涨，交易台就用这三份期权报出一条微笑。<bookmark mark='b'/>在平值处沿波动率轴走，黄色那条：vega几乎不变。它对波动率的斜率，也就是volga，接近零。<bookmark mark='c'/>在两翼，绿色那条，vega随波动率上升而爬升：volga为正，翼部期权在波动率上升时持有更多波动率。<bookmark mark='d'/>跨过各个执行价，曲面在看跌一侧朝一个方向倾斜，在看涨一侧朝另一个方向：这个倾斜就是vanna，即波动率变动时delta怎么变。",
    'The algebra is two lines.':
        "代数只有两行。d一对波动率求导：负的d二除以sigma。<bookmark mark='a'/>链式法则给出vanna，等于负的正态密度乘d二除以sigma；以及volga，等于vega乘d一乘d二除以sigma。<bookmark mark='b'/>在平值处，d一和d二分居零的两侧，乘积很小，所以volga几乎为零，就是那条平的黄线。在二十五delta处，两者都在同一侧，离开约三分之二个标准差，volga为正。<bookmark mark='c'/>这就是为什么交易台除了平值波动率，还用两个数报出微笑。风险逆转，即看涨翼的波动率减看跌翼的，是一翼多头、另一翼空头：它是市场给vanna的价格。蝶式价差，即两翼平均减去中间，是volga的价格。<bookmark mark='d'/>停下来预测一下：vega相同时，跨式和宽跨式哪个volga更多？宽跨式：它是由翼部组成的。这个看跌翼符号描述要求总波动率低于0.674。风险逆转与蝶式是报价坐标和风险敞口代理，并非某个单独希腊值的独立价格。",
    'f"Can three quotes rebuild a whole smile?':
        "三个报价能重建一整条微笑吗？这就是vanna-volga方法，外汇交易台的主力工具，由安东尼奥·卡斯塔尼亚和法比奥·梅尔库里奥在2007年写下。先用平坦的平值波动率给每个执行价定价，再加一个对冲：三份支柱期权的数量，使它们合起来具有这个执行价自己的vega、vanna和volga。<bookmark mark='a'/>每个执行价有三个权重，由一个三乘三的方程组解出；这就是它们，扫过各个执行价，它们携带的价格修正变成了洋红色的微笑。<bookmark mark='b'/>在Surface那天，风险逆转是{100 * so['rr']:+.1f}个点，蝶式价差是{100 * so['bf']:+.1f}。{vsay}三个数就承载了一条微笑的大部分；两翼还需要更多。",
    "f'Between the ten-delta strikes":
        "在两个十delta执行价之间，重建的微笑与拟合的微笑均方根误差为{so['rmse_in']:.2f}个波动率点；在远翼，最多相差{so['maxerr_wing']:.0f}。",
    "f'Here it misses by":
        "这里即使在两个十delta执行价之间，也相差{so['rmse_in']:.1f}个波动率点。",
    'f"Now two years of these two numbers':
        "现在看这两个数两年来的样子，每个星期三，配上比特币的价格。<bookmark mark='a'/>{wsay}蝶式价差一直为正：两翼总比中间贵。卖出风险逆转的交易员在卖vanna；卖出蝶式价差的在卖volga。第12部分会为整条微笑怎么移动建模。每种策略都是这些希腊字母的组合。下一章：各种策略及其收益。",
    'f"Unlike an equity index':
        '股票指数的看跌期权总是更贵，比特币不同，它的风险逆转只在{100 * share:.0f}%的星期为负：上涨行情里，市场为看涨期权付了高价。',
    'f"Like an equity index':
        '和股票指数一样，比特币的风险逆转在{100 * share:.0f}%的星期为负。',
    'Chapter five. Strategies':
        '第5章。策略：每种结构押注什么，又赚了多少。',
    'Every standard structure is a shape.':
        "每种标准结构都是一个形状。这是一个月期期权持有一周后的利润，横向是现货的变动，从左到右，纵深是隐含波动率的变动，从前到后；绿色为盈，红色为亏。跨式组合是一道两端翘起、并随波动率向上倾斜的山谷：伽马多头，vega多头。<bookmark mark='a'/>让时间过去，三周：整道山谷沉下去。这就是时间损耗。<bookmark mark='b'/>现在变形。宽跨式：同样的押注，更宽的山谷，更便宜。<bookmark mark='c'/>风险逆转，买入上方的看涨、卖出下方的看跌：一个倾斜的平面，押注方向，几乎没有vega。<bookmark mark='d'/>蝶式价差：一座小山，倒过来的跨式，什么都不发生时它赢。<bookmark mark='e'/>看涨价差：押涨，但有上限。<bookmark mark='f'/>最后是日历价差，买第二个月、卖第一个月：大幅变动时亏，波动率上升时赚，同时是伽马空头和vega多头。",
    'The table a trader carries in their head.':
        "交易员脑子里的那张表。每种结构：伽马的符号、vega、delta，以及它押注什么。<bookmark mark='a'/>结构的希腊字母是各条腿的和。跨式组合的伽马是平值期权的两倍。日历价差同时是vega多头和伽马空头，因为vega像时间的平方根那样增长，伽马像时间平方根的倒数那样缩小。<bookmark mark='b'/>停下来预测一下：每周在真实的比特币微笑上买入，这些结构里哪个亏钱最频繁？",
    'f"Here is the record.':
        "这是记录。2024年和2025年的每个星期三，在当天真实的Deribit微笑上买入每种结构，二十八天后按比特币价格结算。<bookmark mark='a'/>每种{nW}笔交易，逐周填满。<bookmark mark='b'/>问题的答案：{st['worst']}，它在{100 * (1 - worst['win']):.0f}%的星期里亏钱。看白色的中位数：{med_say}黄色的均值更高，被少见的大赢拉高，也就是尾部。<bookmark mark='c'/>{rr_say}<bookmark mark='d'/>{tsay}一个资产、两年、一段上涨行情，能显示这些形状做了什么；不能证明其中任何一个有优势。这些形状背后有一个持久的数字。下一章：波动率溢价。",
    'below zero for every structure':
        '每种结构都低于零：这是时间损耗的故事。',
    "f'below zero for {n_neg}":
        '六种里有{n_neg}种低于零：这是时间损耗的故事。',
    'The risk reversal made money on average':
        '风险逆转平均赚钱，是因为比特币在这两年里上涨了，与波动率无关。',
    'The risk reversal lost on average':
        '风险逆转平均亏钱，因为微笑的倾斜成本超过了趋势带来的收益。',
    'f"No structure\'s mean':
        '没有哪种结构的均值t统计量超过{best_t:.1f}。',
    "f'The largest t-statistic":
        '最大的t统计量是{best_t:.1f}。',
    'Chapter six. The volatility risk premium, in option returns.':
        '第6章。期权收益中的波动率风险溢价。',
    'f"Now hedge the weekly hypothetical four-week straddles. Prices come from fitted':
        "现在对每周开始的假设四周跨式进行对冲。价格来自拟合的每日微笑，而非可执行买卖报价；对冲使用币安小时收盘价。每格跟踪一个窗口，窗口互相重叠。<bookmark mark='a'/>多数最终为红色。<bookmark mark='b'/>均值为每百元比特币{p['mean']:.2f}，采用4阶滞后的Newey–West t统计量为{p['t']:.1f}。阴影是另一种启发式带：普通标准误的两倍，再乘根号4，不是经过校准的置信区间。<bookmark mark='c'/>这个缓存历史模型未计可执行价差、费用与合约约定；负均值只描述此样本，不保证卖方盈利，也不唯一解释方差风险溢价。",
    "f'The mean is {p['mean']:.2f} per hundred":
        "均值是每一百个比特币{p['mean']:.2f}，纽伊–韦斯特t统计量为{p['t']:.1f}：买入波动率再对冲，稳定地亏钱。",
    "f'The mean is {p['mean']:.2f}, with":
        "均值是{p['mean']:.2f}，t统计量只有{p['t']:.1f}：噪声太大，下不了结论。",
    'f"The academic record says the same.':
        "学术记录说的一样。约书亚·科瓦尔和泰勒·舒姆韦在2001年发现，构造成没有市场暴露的标普500平值跨式组合，平均每周亏约百分之三。<bookmark mark='a'/>古尔迪普·巴克希和尼昆杰·卡帕迪亚在2003年改为对冲它们：delta对冲后的收益为负，平值处最负，这正是波动率风险的负价格所预言的。<bookmark mark='b'/>在比特币同样的九十六周里，未对冲的跨式组合平均每四周亏掉权利金的{100 * -p['straddle_ret_mean']:.0f}%，中位数是{100 * p['straddle_ret_median']:.0f}%，噪声太大；{hsay}。对冲剥掉了方向，也就是掩盖溢价的噪声。",
    'the hedged one shows it clearly':
        '对冲后的则清楚地显示了它',
    'even hedged it is hard to see':
        '即使对冲后也很难看出',
    'Interpret the identity under its assumptions: continuous diffusion paths, contin':
        "须在假设下解释恒等式：连续扩散路径、连续无成本对冲、零利率与收益率、固定模型隐含波动率。<bookmark mark='a'/>对凸期权，若隐含方差超过以Gamma乘现价平方归一化加权的预期实际方差，买方的期望损益为负。<bookmark mark='b'/>若初始权利金是正确的Q测度价格，对冲策略可容许且可积，那么零成本对冲终值收益的Q期望为零。<bookmark mark='c'/>其P期望是对冲期权风险溢价。负的经验估计符合波动率风险被定价的解释，但不证明唯一机制；实际数据中的跳跃、交易成本和有限步长误差都重要。<bookmark mark='d'/>卖方为什么仍会失败？第十六章看崩盘风险。先看预测比较能确立什么。",
    "Chapter seven. A forecaster's edge, tested, and how much to bet.":
        '第7章。预测者的优势：检验它，以及下多大的注。',
    "Chapter six measured a historical premium. Part ten's hypothetical dollar calls ":
        "第六章测量了历史溢价。第十部分的假设美元看涨期权用DVOL代理定价，并按小时用现货对冲，并非可执行的Deribit交易。<bookmark mark='a'/>卖方可以尝试比较隐含波动率与预测。这里HAR系数每周仅用此前日期重新拟合，但缓存输入包含入场当日完整方差，包括早八点入场之后的小时；次日预测又被用作月度代理。因此这是回顾性诊断，不是入场时可得的信号。<bookmark mark='b'/>绿线是随后一个月的实际波动率，按窗口起点对齐。尖峰仍很重要，但这个比较不能确立可交易的预测优势。",
    'f"Split disjoint thirty-day windows by the cached diagnostic. When DVOL exceeded':
        "把互不重叠的30天窗口按缓存诊断分组。DVOL高于它时，假设卖出看涨期权每百元比特币赚{e['nonoverlap_on']:.2f}，否则赚{e['nonoverlap_off']:.2f}。<bookmark mark='a'/>组间差除以普通标准误约为{diff / se_d:.1f}。窗口不重叠不代表独立，入场日的信息泄漏也使它不能称为交易检验。<bookmark mark='b'/>登记簿中已有代码设定，但记录本身不证明登记早于计算。本章计数为{env['trials']}；登记与这个t统计量都不能修复当时不可得的信息。",
    'With one asset, this sample has only a few dozen disjoint months; they need not ':
        "单一资产的样本只有几十个互不重叠的月份，它们未必独立。跨越数千只股票可以增加观察对象。Amit Goyal与Alessio Saretto每月按历史波动率减隐含波动率对美国股票排序，买入隐含波动率远低于自身历史的跨式，卖出远高于自身历史的跨式。<bookmark mark='a'/>1996至2006年，这个多空组合获得了较高的平均收益。第二十五部分会问：计入所有尝试过的排序后，还有多少结果成立。",
    'f"Sizing has another trap. Expected log wealth is approximately f times the mean':
        "仓位大小还有陷阱。预期对数财富近似为杠杆乘均值，减去二分之一杠杆平方乘二阶矩；二次近似最优值是均值除以二阶矩。图中的均值除方差启发式约{k['f_gauss']:.0f}，不是精确的高斯Kelly解。<bookmark mark='a'/>高斯损失尾部无界；红线只使用最坏的已观测损失，是样本破产边界，不是未来损失的保证界限。<bookmark mark='b'/>这些{k['n']}个月度窗口互相重叠；样本拟合最优值{k['f_emp']:.1f}靠近边界，说明答案多么依赖最坏那次观察。<bookmark mark='c'/>一半杠杆保留{100 * half / k['g_max']:.0f}%的拟合增长，并能承受两倍已观测最坏损失；更大的未知损失仍可能破产。这个诊断不提供可执行的杠杆建议。下一章看双边报价。",
    "f'The curve keeps rising":
        "曲线一直上升，直到撞上{k['f_ruin']:.0f}处的墙：在这个样本里，最优点就是最差月份所允许的、离破产最近的地方，这只说明样本还没见过更差的月份。",
    "f'The curve peaks at":
        "曲线在{k['f_emp']:.0f}处见顶，远在{k['f_ruin']:.0f}处的墙之前。",
    'Chapter eight. Making a market':
        '第8章。做市：价差，以及你在和谁交易。',
    'The classic market-making interview game.':
        "经典的做市面试游戏。请为一次掷骰子做市。期望点数是三点五，所以你围绕它报价：三点三买，三点七卖。价差是你的收入，也是你的保护。<bookmark mark='a'/>然后面试官说：点数是偶数。你的公允价值跳到四，报价也随之移动。这个教训统治着每一个期权交易台：和你交易的人可能知道些什么，所以每笔交易之后，公允价值往往朝不利于你的方向移动。劳伦斯·格洛斯滕和保罗·米尔格罗姆在1985年称之为逆向选择。",
    "Glosten and Milgrom's model, running.":
        "格洛斯滕和米尔格罗姆的模型，跑起来。一项资产要么一文不值，要么值一；只有部分交易者知道是哪一种。这里它实际值一，百分之三十的交易者知道，所以他们总是买；其余的人随机买或卖。做市商分不清他们。<bookmark mark='a'/>于是它把卖价报成有人买入时的期望价值，把买价报成有人卖出时的期望价值。每笔交易都是证据：一次买入把它的信念往上推，一次卖出往下推。<bookmark mark='b'/>一笔接一笔，信念朝真相爬升，报价随之上移，价差收窄：一旦做市商知道了价值，就没什么可怕的了，也就没有价差。价差是不知道对面是谁的代价。",
    'The algebra of it.':
        "它的代数。由贝叶斯公式，卖价是给定一次买入的期望价值：价值高时，所有知情交易者都买，其他人里有一半买。<bookmark mark='a'/>在机会均等时：价差等于知情者比例乘以不确定性。<bookmark mark='b'/>要在真实交易上测量它，就把它拆开。做市商的优势是交易那一刻相对公允价值收取的部分。盯市回报是一段时间后剩下的部分，期权重新估值、delta对冲也计入。<bookmark mark='c'/>两者之差就是逆向选择。这里s表示主动成交方向，Delta是期权多头Delta，s乘整个对冲收益，期权价先转换为美元，再除以每波动率点Vega，标记价只是估值代理。初始优势减后续标记收益还包含价格发现和标记模型误差，不是被单独识别的纯逆向选择成分。后续标记取所请求时距之后的第一笔成交，不一定恰好在该时刻；未计费用与执行。",
    'f"Now real flow.':
        "现在看真实的订单流。Deribit上某个星期三上午的每一笔比特币期权交易，落在执行价对到期日的平面上：吃单方买入是金色，卖出是蓝色，交易越大点越大。<bookmark mark='a'/>在2024和2025年的{fl['days']}个星期三里，共有{fl['n']:,}笔交易。按vega算，吃单方买入和卖出虚值看涨的数量大致相当，看跌也一样：做市商的账本并不是一边倒的。",
    'f"And the spread\'s split.':
        "再看价差的拆分。这是我们公司的盯市回报函数：交易时的优势，然后是之后每次重新估值，计入delta对冲，以波动率点计。<bookmark mark='a'/>先在一天上运行，再在所有天上。相对Deribit自己的标记价格，做市商交易时的平均优势是{c[0]:.2f}个波动率点。<bookmark mark='b'/>五分钟后{c[1]:.2f}；半小时后{c[2]:.2f}；一小时后{c[3]:.2f}。{ksay}最大的那些交易付出更宽的优势，{cb[0]:.2f}，而且回吐得更多：一小时后只剩{cb[3]:.2f}。做市商向它们多收是对的。<bookmark mark='c'/>所以，停下来预测一下：你的报价被成交，然后市场朝不利于你的方向走。价差是太窄还是太宽？如果每次都这样，就是太窄：那是定价过低的逆向选择。每次成交都留下库存。下一章：怎么处理它。",
    "f'An hour later it keeps about":
        '一小时后，它保留了其中约{100 * kept:.0f}%：其余的回到了知道价格去向的交易者手里。',
    "f'An hour later it keeps {100":
        '一小时后，它保留了{100 * kept:.0f}%：这里的逆向选择很小。',
    'Chapter nine. Inventory':
        '第9章。库存：最优报价，以及一个会学习的做市商。',
    'f"An options market maker quotes volatility to clients':
        "期权做市商向随机到来的客户报波动率，有的来买，有的来卖。围绕公允价值固定报价的交易台，任由库存漂移，这里最多达到{a['max_abs']:.0f}个单位的vega。<bookmark mark='a'/>让报价朝库存反方向倾斜，多头时报低、空头时报高，同样的客户留下的账本保持在{b['max_abs']:.0f}以内，只损失少量价差收入。报价该倾斜多少？这是一个控制问题，而且有精确答案。",
    'Write it down.':
        "把它写下来。客户成交一个报价的强度，随报价离公允价值的距离指数下降。做市商最大化利润减去库存的持续惩罚，这是马尔科·阿韦拉内达和萨沙·斯托伊科夫的问题，采用阿尔瓦罗·卡特亚和塞巴斯蒂安·哈伊蒙加尔的形式。<bookmark mark='a'/>动态规划给出持有q的价值所满足的哈密顿–雅可比–贝尔曼方程。<bookmark mark='b'/>它的一阶条件：每个报价离公允价值k分之一，再加上多一单位库存带来的价值变化。<bookmark mark='c'/>奥利维耶·盖昂、夏尔–阿尔贝·勒阿勒和华金·费尔南德斯–塔皮亚给出了长期限近似：库存多头时两个报价都下移，与q成正比。<bookmark mark='d'/>对期权来说，q是vega，萨沙·斯托伊科夫和梅赫迈特·萨拉姆在2009年正是这样做的。而且因为做市商无法完美对冲，客户需求本身就会推动期权价格，加尔莱亚努、佩德森和波特什曼证明了这一点。停下来预测一下：持有二十个vega的多头，报价上调还是下调？下调：你想卖出。",
    'In the House, the quoting rule is a few lines':
        "在我们的公司里，报价规则只有几行：中间价朝vega库存的反方向移动，超过限额时只报一边。<bookmark mark='a'/>在公允波动率百分之六十时运行。空头二十个vega，它报高四个点，为了买回；多头二十个，报低四个点，为了卖出。",
    'f"Now let a machine find the answer':
        "现在让机器在不知道模型的情况下找到答案。这个游戏：二十一个库存水平，每边七个报价距离，客户随机到来。动态规划精确地解出它：白色那一列，一道台阶，多头时把报价压低，空头时抬高。<bookmark mark='a'/>学习者是表格型Q学习，能找到答案的最简单方法：它只看到客户到来和成交，维护一张表，记录在每个库存下每个报价有多好。五个随机种子；带子是它们的分布范围。<bookmark mark='b'/>看它那一列，种子零，从噪声锐化成台阶，它的价值也在爬升。{msay}闭式公式对齐到同样的网格，得到{glft:.0f}%；对称报价，不管多宽，一旦库存要付代价就亏钱。<bookmark mark='c'/>学习者在很少到达的库存上最嘈杂。这是学出来的做市商的老实教训：它们在有数据的地方学会。",
    "f'After eight hundred thousand simulated clients":
        '经过八十万个模拟客户，五个种子达到最优值的{pct.min():.0f}%到{pct.max():.0f}%。',
    'f"Put the trained quoter to work':
        "让训练好的报价者在两千个新客户上工作，旁边是最好的对称报价，到达顺序完全相同。<bookmark mark='a'/>{lsay}倾斜，是做市商既做下去又保持小规模的方法。第10章对冲剩下的部分。",
    "f'The learned quoter trades all day":
        "学出来的报价者整天都在交易，靠倾斜把库存保持在几个单位以内，得分{L['score']:.0f}；对称的那个为了让库存小，报得太宽，几乎不成交，得分{Sy['score']:.0f}。",
    'f"Here the symmetric quoter scores':
        "这里对称报价者得分{Sy['score']:.0f}，学习者{L['score']:.0f}。",
    'Chapter ten. Hedging the book':
        '第10章。对冲整本账：用其他期权对冲伽马和vega，以及有成本时的对冲。',
    'f"The underlying hedges delta and nothing else.':
        "标的只能对冲delta。要对冲伽马和vega，交易台得交易其他期权。把账本想成希腊字母空间里的一支箭头，横向是伽马，纵向是vega：一个卖出的跨式组合指向左下。<bookmark mark='a'/>交易台能交易的每份期权都是另一支箭头：七天期权几乎全是伽马，六十天的主要是vega。<bookmark mark='b'/>所以把它们缩放，短的取{sol['n1']:.2f}份，长的取{sol['n2']:.2f}份，首尾相接：它们把账本的箭头恰好送回原点。<bookmark mark='c'/>然后才交易标的，处理剩下的delta。",
    'In symbols, a two by two system':
        "写成符号，是一个二乘二的方程组：两份期权的数量，使它们的伽马和vega抵消账本的。<bookmark mark='a'/>然后是股票，放在最后，因为股票的delta是一，没有其他希腊字母。<bookmark mark='b'/>当两份期权的vega与伽马之比不同时，它可解，而第1章的恒等式说这个比值随到期日增长。<bookmark mark='c'/>停下来预测一下：你必须消掉伽马、保留vega。用短期期权还是长期期权？短期的：它们以很少的vega便宜地携带伽马。",
    'f"Does it work?':
        "有效吗？在一万条路径上模拟一个卖出的跨式组合，用三种方式对冲：只对冲delta；加上用七天期权对冲伽马；再加上用六十天期权对冲vega。<bookmark mark='a'/>波动率恒定时，只对冲delta会留下{G['delta']['sd']:.2f}的标准差，就是第10部分的离散对冲误差。伽马对冲去掉其中{100 * cut_g:.0f}%，vega没什么可加的。<bookmark mark='b'/>现在让波动率本身游走，就像赫斯顿模型那样。只对冲delta留下{H['delta']['sd']:.2f}，加上伽马对冲留下{H['delta-gamma']['sd']:.2f}。{hsay}这里使用不断滚动的合成对冲期权，按当前现货波动率用Black–Scholes标记，Heston模拟中也一样，并非Heston期权价格；未计期权价差、融资与执行约束。",
    "f'Once volatility moves":
        '一旦波动率会动，vega对冲就有了用处：它去掉伽马对冲剩下部分的{100 * cut_h:.0f}%。',
    "f'Even with volatility moving":
        '即使波动率会动，vega对冲也只多去掉{100 * cut_h:.0f}%。',
    'f"One vega number hides the term structure.':
        "一个vega数字掩盖了期限结构。这是一本账按到期分桶的vega。<bookmark mark='a'/>交易台可以用一份九十天期权把总量归零：平行对冲。<bookmark mark='b'/>现在让期限结构变陡，短端上升四个点，长端下降一个半点。总vega为零的这本账亏了{-bk['after']:.2f}，只比未对冲时的{-bk['before']:.2f}少一点。纳西姆·塔勒布在《动态对冲》里的教训：按桶对冲vega。",
    'f"Whalley and Wilmott derived a small-cost asymptotic no-trade band in 1997. Wit':
        "Whalley与Wilmott于1997年推导了小成本渐近不交易带。带内不动，带外交易回边缘。<bookmark mark='a'/>在此模型中，半宽是比例成本乘现价乘Gamma平方、除以风险厌恶参数后取立方根，并含画面中的常数与贴现因子。距到期15天，现价90时宽度{hw[90.0]:.3f}，行权价处{hw[100.0]:.3f}，现价110时{hw[110.0]:.3f}。<bookmark mark='b'/>本例接近行权价时最宽。这条渐近规则依赖目标与模型，并非普遍最优的交易带。",
    'Can a network learn the band':
        "一个网络能在没人告诉它的情况下学会这条带吗？汉斯·比勒及其合作者的深度对冲，训练一个小网络在每一步决定把对冲朝delta移动多远，通过模拟器训练，最小化利润方差加上成本乘以价格kappa。<bookmark mark='a'/>看它学习，三个种子画成一条带。左边是它在期权生命中段学到的策略：对冲与delta的差距被它补上的比例，对应差距的大小。它一开始是平的，然后学会放过小差距、补上大差距：一条柔性的带。",
    'The scoreboard: risk against cost':
        "记分板：同样路径上的风险对成本，越靠左下越好。每六小时再对冲最安全也最贵；惠利–威尔莫特带画出更好的曲线。<bookmark mark='a'/>深度对冲者，三种成本权重，第一种有三个种子，落在那条曲线附近，没人告诉它带是什么。经典答案已经非常好；学习器的价值在于它能扩展到没有公式的账本，那是第17部分。每份期权终会到期。下一章：到期那天会发生什么。",
    'Chapter eleven. Expiry, and pin risk.':
        '第11章。到期与钉住风险。',
    'f"Options are most dangerous at the end.':
        "期权在最后时刻最危险。这是最后一天里执行价附近的伽马：一道山脊，越接近到期越成为尖峰。<bookmark mark='a'/>在执行价处，它随剩余时间平方根的倒数增长。波动率百分之五十时，到期前一天是{gd:.2f}，前一小时是{gh:.2f}，前一分钟是{gm:.1f}。离开执行价，它就塌缩为零。",
    'Gamma is how fast delta moves':
        "伽马是delta变化的速度，所以delta变成了一个台阶。还剩一天时，它平滑地越过执行价；还剩一分钟时，一点点变动就让它从零翻到一，对冲者必须为噪声把整个头寸来回交易。<bookmark mark='a'/>钉住风险是卖方的相关问题。如果股票恰好收在你卖出的期权的执行价上，你要到第二天早上才知道是否被行权：周末持有一整个单位、方向未知的delta。",
    'Can hedging move the price itself?':
        "对冲能推动价格本身吗？先看平值处的伽马：第1章的公式，d一取零。<bookmark mark='a'/>净伽马多头的账本对每次变动都反向再对冲：价格涨时卖，跌时买。<bookmark mark='b'/>如果它的交易推动价格，冲击是线性的kappa，那么这股流量就会顶回变动。<bookmark mark='c'/>解出价格变化：波动率被除以一加kappa乘以对冲者的伽马。马尔科·阿韦拉内达和迈克尔·利普金的洞见：在执行价附近、临近到期时，伽马爆炸，有效波动率崩塌，价格被钉住。<bookmark mark='d'/>停下来预测一下：如果对冲者是净伽马空头，是钉住还是排斥？",
    'f"Simulate it.':
        "模拟它。两千条路径，期权最后两天，对冲者在执行价一百处是净伽马多头，他们的交易会推动价格。<bookmark mark='a'/>路径散开，然后在临近到期时被拉向执行价，终点的直方图在一百处长出一个尖峰：{100 * p['long']['near']:.0f}%的路径结束在离它半个点以内，没有对冲者时是{100 * p['none']['near']:.0f}%。<bookmark mark='b'/>把符号反过来。净伽马空头的对冲者涨时买、跌时卖，执行价变成排斥的：尖峰处变成一个洞，{100 * p['short']['near']:.1f}%。这就是问题的答案：伽马空头会排斥。",
    'f"Does it happen?':
        "现实中会发生吗？倪晓燕、尼尔·皮尔逊和艾伦·波特什曼在2005年发现，有上市期权的美国股票在到期星期五更常收在执行价附近，在做市商再对冲应当把价格钉住的地方最明显。约瑟夫·戈莱兹和延斯·雅克韦特在标普500期货上也发现了它。<bookmark mark='a'/>比特币呢？Deribit的期权在星期五早上八点（世界协调时）到期，按其指数三十分钟均值结算，执行价每隔一千美元一个。测量比特币五年里每个小时、以及星期五到期时离最近的千元整数有多远。<bookmark mark='b'/>在所有小时里，{100 * al['share']:.1f}%的收盘价落在离执行价一百美元以内，和随机预期一样。在星期五到期时是{100 * f8['share']:.1f}%；月度到期时{100 * mo['share']:.1f}%；到期前一小时{100 * f7['share']:.1f}%，与随机无异。{verdict}有些期权到不了到期日。下一章：提前行权，以及它留下的钱。千美元网格只是代理，不是实际上市行权价集合的重建；币安收盘价也不是Deribit结算均价。二项z忽略依赖与基准估计，不识别对冲的因果作用。Deribit也有每日到期，现金结算与实物交割的指派风险不同。",
    "f'With a z of {f8['z']:.1f} on":
        "在{f8['n']}个星期五上z为{f8['z']:.1f}，这只是提示，不是结论：严格的检验应当使用那三十分钟均值本身。",
    "f'With a z of {f8['z']:.1f}, that":
        "z为{f8['z']:.1f}，这是钉住的有力证据。",
    'Chapter twelve. Early exercise':
        '第12章。提前行权、合成头寸与股息博弈。',
    'An American option can be exercised any day.':
        "美式期权任何一天都可以行权。什么时候该行权？先看看涨期权。因为现在就能行权，它至少值内在价值。<bookmark mark='a'/>但由看涨看跌平价，欧式看涨期权至少值股价减去贴现后的执行价，因为看跌期权有价值：这比今天行权更多，今天行权要现在就付执行价，而不是以后。<bookmark mark='b'/>于是有罗伯特·默顿1973年的结果：对不派息的股票，美式看涨期权永远不该提前行权。停下来预测一下：深度实值的看涨，没有股息，该行权锁定收益吗？不：卖掉它，或者做空股票来对冲。<bookmark mark='c'/>股息改变了这一点。在股票除息之前，行权得到S减K。继续持有得到的是股价下跌一个股息后的看涨期权，由平价写成股价减股息、减贴现执行价、再加一份看跌。<bookmark mark='d'/>所以股息大于或等于执行价利息加看跌期权价值时，行权是最优选择之一：深度实值、股息大、剩余时间短。这里假设非负利率、无成本借贷与交易、单次已知现金股息且此后无股息。等号处行权与继续持有价值相同；画面比较的是内在价值大于或等于继续持有价值。",
    'f"See it on a tree.':
        "在树上看。我们公司的树，给一份看涨期权定价，股票在两个月到期前三周派息二；虚线是除息日。阴影节点是实值的。<bookmark mark='a'/>在每个节点比较行权和持有。金色节点是行权更好的地方，每一个都在除息前的最后一步上，而且深度实值：别处一个都没有。<bookmark mark='b'/>在最深的那个节点，股息{e['D']:.0f}与执行价利息{e['carry']:.2f}加看跌期权{e['put']:.3f}赛跑：股息轻松胜出。正是这项权利，让美式看涨值{e['price']:.2f}，而欧式只值{e['european']:.2f}。",
    'Two words from every options floor.':
        "每个期权交易大厅都有的两个词。同一执行价的看涨减看跌是合成远期，第9部分的平价。<bookmark mark='a'/>股票加上一个合成远期空头，就是转换套利，无风险。<bookmark mark='b'/>它的镜像是反转套利：做市商就是这样把看涨变成看跌的。",
    'f"And the trading game around it.':
        "还有围绕它的交易游戏。在除息日前一天，一些实值看涨期权的持有人忘了行权。持有对应空头、又没被指派的人，就留下了股息的价值。于是有交易员同时买入和卖出同样数量的同一份看涨期权，即对敲，然后把自己的多头全部行权。<bookmark mark='a'/>行权被随机指派给空头。<bookmark mark='b'/>按期望，未平仓量为OI，行权比例为e，对敲规模为w，收益等于w乘股息乘一减e，再乘OI除以OI加w：w越大，就越接近全部被遗忘的价值。这一次抽签里，玩家有{L['mine_free']}份空头逃过了指派。<bookmark mark='c'/>维罗妮卡·普尔、汉斯·斯托尔和罗伯特·惠利在2008年记录了这些被遗忘的钱，郝佳、阿夫纳·卡莱和斯图尔特·梅休记录了它吸引来的成交量激增。下一章：指数期权与成分股期权的对比，以及它们之间的相关性。",
    'Chapter thirteen. Dispersion, and implied correlation.':
        '第13章。离散度与隐含相关性。',
    'An index is a basket':
        "指数是一篮子股票，它的波动率取决于成分股一起变动的程度。取五十只股票，每只波动率百分之三十。平均相关性上升时，它们的相关矩阵越来越热。<bookmark mark='a'/>当它们各自独立变动时，指数很平静：百分之四的波动率，成分股的噪声互相抵消。相关性升向一时，抵消消失，指数变得和单只成分股一样波动。<bookmark mark='b'/>所以，指数期权的价格对照成分股期权的价格，就是相关性的价格。",
    'f"Draw the index volatility over two inputs':
        "把指数波动率画在两个输入上：平均相关性，以及成分股的波动率。它随两者上升。<bookmark mark='a'/>现在市场告诉你指数的隐含波动率：在那个高度切开曲面，百分之二十。黄色曲线是与它一致的所有组合。<bookmark mark='b'/>读出成分股的隐含波动率，百分之三十，相匹配的相关性约为{r30:.2f}。这个数就是隐含相关性。",
    'f"The algebra. An index\'s variance':
        "代数。指数的方差等于成分股方差的加权和，加上每一对的协方差。<bookmark mark='a'/>把每一对的相关性都换成同一个数再求解：这就是隐含相关性，芝加哥期权交易所用标普500最大的五十只成分股计算它的隐含相关性指数，用的就是这个方法。<bookmark mark='b'/>成分股多时，自身方差项消失，隐含相关性就是指数波动率与成分股平均波动率之比的平方。停下来预测一下：指数百分之二十，成分股百分之三十。<bookmark mark='c'/>在我们公司里：先是三只股票的玩具例子，再是五十只。约{c3['big']:.2f}，九分之四。",
    'f"Here is the real thing':
        "这是真实的数据：芝加哥期权交易所三个月隐含相关性指数，2006年以来的每一天。<bookmark mark='a'/>它在危机中飙升，那时一切一起下跌：2011年12月欧债危机期间是{c3['max']:.0f}，2020年3月是{Y['2020']['max']:.0f}。<bookmark mark='b'/>再看末尾：创纪录的低点，2024年7月{Y['2024']['min']:.1f}，2025年1月{Y['2025']['min']:.1f}，几只巨型科技股带动指数，其余股票各走各的：正是离散度交易，即做空指数波动率、做多成分股波动率，能赚钱的条件。约斯特·德里森、帕斯卡尔·梅恩豪特和格里戈里·维尔科夫在2009年证明，隐含相关性往往高于事后实现的相关性：这就是相关性风险溢价，也是指数期权贵的原因。COR3M于2021年7月推出，画出的更早数据是回溯历史。隐含相关性低本身不确立分散交易盈利，还须考虑实际相关性、成分股波动率、对冲权重与成本。",
    'f"The trade.':
        "这笔交易。卖出指数的跨式组合，买入成分股的跨式组合，按vega匹配，全部每天对冲。每个成分股跨式收取自己的已实现减隐含方差；卖出的指数跨式支付指数的。把指数项换成和的方差，利润就由隐含减已实现相关性驱动。<bookmark mark='a'/>模拟它：二十只股票，指数期权按二分之一的隐含相关性定价，四百种实际相关性情景。每个点是一个情景：利润跟着这个差值，相关系数{ds['corr']:.2f}，{100 * ds['share_right_sign']:.0f}%的时候符号与预测相同。<bookmark mark='b'/>左边，实现相关性高于隐含的地方，它亏钱。那就是崩盘：一切一起下跌。离散度交易靠做空崩盘来赚取相关性溢价。下一章：按合约数计全球最大的期权市场，以及谁在交易它。",
    "Chapter fourteen. India's expiry-day boom":
        '第14章。印度的到期日热潮，以及彩票的回报。',
    "India's National Stock Exchange has been the world's largest derivatives exchange":
        "多年来，印度国家证券交易所按成交合约数一直是全球最大的衍生品交易所，其中大多是短期指数期权，许多由个人买入。2024年9月，印度监管机构SEBI公布了他们的结局：截至2024年3月的一年里，百分之九十一的股票衍生品个人交易者亏了钱，三年净亏损约一点八万亿卢比，约合二百一十亿美元。<bookmark mark='a'/>SEBI从2024年11月起收紧规则：每个交易所只保留一个指数的周度到期，合约更大，到期日加收保证金。<bookmark mark='b'/>次年的亏损仍超过一万亿卢比，仍有百分之九十一的人亏损。这些交易的另一边总有人。",
    'f"What does a short-dated, out-of-the-money option pay its buyer?':
        "一份短期虚值期权给买方带来什么？印度的散户数据是汇总的，所以换一个市场来测量这种工具。这是六十张真实的彩票：在Deribit上买入的比特币虚值期权，从一百个星期三上午中随机抽取，每一份都在两天内到期。<bookmark mark='a'/>到期。大多数变灰：一文不值。只有寥寥几张赚回的多于成本。<bookmark mark='b'/>在一百个星期三里，共{o['n_buy']:,}张这样的彩票：{100 * o['worthless']:.0f}%到期作废，{100 * o['profitable']:.0f}%赚回的多于成本。按权利金加权，买方每一美元拿回{100 * (1 + o['ret_buy']):.0f}美分。<bookmark mark='c'/>提醒一句：卖出这类期权的吃单方作为一个群体并没有更好，而且Deribit的吃单方不是印度的散户。这里比较的是工具，不是人。",
    'Why do short-dated options make the premium so stark?':
        "为什么短期期权让溢价如此明显？在没有漂移时，期权的期望收益就是用将要实现的波动率算出的布莱克–斯科尔斯公式，而它的价格用的是隐含波动率。<bookmark mark='a'/>对一个离价外固定距离的执行价，随着到期临近，价格由一个指数项主导：e的负k平方除以二sigma平方tau次方。<bookmark mark='b'/>取比值，指数被乘上了tau分之一：只要隐含高于实现，每一美元权利金的期望收益就会随到期临近而崩塌。对一份虚值百分之五的看涨，隐含五十、实现四十五，还剩一个月时买方拿回大部分权利金，还剩几小时时几乎什么都拿不回。精确曲线和近似一致。<bookmark mark='c'/>停下来预测一下：十个人里九个亏钱，这能证明期权定价过高吗？不能：公平的彩票也大多数时候输。按权利金加权的收益才回答这个问题，而它是负的。下一章：那个市场的一个案例，根据监管者的指控。",
    'Chapter fifteen. A case file':
        '第15章。一份案卷：印度监管机构对简街的临时命令。这些是指控，该公司提出异议。',
    'On the third of July 2025':
        "2025年7月3日，印度证券交易委员会对简街集团的四个实体发布了一项临时命令。这些是指控，是在该公司陈述意见之前作出的，该公司对此提出异议。SEBI指控，在银行指数Bank Nifty的到期日，该公司上午买入指数成分股和期货，托住指数，同时建立指数下跌时获利的大额指数期权头寸，然后在下午卖出，压低指数。<bookmark mark='a'/>命令扣押了四千八百四十三亿卢比，约合五亿美元，即它所称的非法所得。简街表示对这些认定提出异议。",
    'The public record, in order.':
        "按时间顺序的公开记录。2024年4月，简街在纽约起诉对冲基金千禧管理公司和自己的两名前交易员，指控他们拿走了一个交易策略；一次听证会透露它涉及印度期权。该案于当年12月和解，条款未公开。<bookmark mark='a'/>然后是2025年7月的临时命令，以及同月的托管存款和交易禁令的解除。<bookmark mark='b'/>2025年9月，该公司向证券上诉法庭上诉，称没有拿到辩护所需的文件。<bookmark mark='c'/>据法律媒体报道，2026年10月，法庭就这一争议保留了裁决。截至撰写时，对这些指控还没有最终认定，本课程也不作评判。",
    'Why would anyone trade like that?':
        "为什么会有人那样交易？一个使用虚构数字的玩具模型可以展示其机制；它不是任何事情的证据。上午买入，把指数推高一点。<bookmark mark='a'/>与此同时，建立一个指数下跌时获利、且规模远大于这些交易的指数期权头寸。<bookmark mark='b'/>下午卖出两倍的数量，到收盘把指数压低两点。现货和期货交易大致打平，但期权的收益取决于它的规模。<bookmark mark='c'/>这个玩具模型只说明一件事：为什么监管机构要把到期日、期权头寸规模与标的交易放在一起看。",
    'Generalize the toy.':
        "把玩具模型推广。设Q是推动指数的交易，D是期权敞口。交易的成本约为lambda乘Q的平方：沿Q的一道槽。期权的收益约为D乘以交易造成的变动，二lambda乘Q：沿D的一道坡。<bookmark mark='a'/>令总和为零，边界是一条直线，D等于Q的一半，黄色那条。在绿色一侧，即使推动价格的交易亏钱，整体也赚钱。所以监察要把期权头寸和现货交易放在同一块屏幕上看。从2025年10月起，SEBI九月一日的通函要求交易所按delta衡量，检查每个实体日内的指数期权头寸，净额上限为五千亿卢比。区分操纵与对冲的，是意图和模式：留给监管机构和法庭权衡。下一章：卖出波动率爆仓时会发生什么。",
    'Chapter sixteen. A crisis file':
        '第16章。一份危机档案：做空波动率爆仓之时。',
    'f"Chapter six\'s premium is real':
        "第6章的溢价是真的，这里是它所补偿的东西。两本示意性的账，跑过2017到2020年。每本每个月卖出一份比市场低百分之三的一个月期看跌期权，再在更低处买一份对冲用的看跌：一本在虚值百分之十七点五，另一本在虚值百分之四十。两本每天都按VIX加一个固定偏斜估值。<bookmark mark='a'/>平静的市场里两本都赚钱；更便宜、更深的对冲赚得稍多一点。2018年2月：VIX一天之内翻倍。<bookmark mark='b'/>然后是2020年3月。市场一个月跌去三分之一，VIX突破八十。三年平静期里，更便宜的对冲每一百省下了{extra:.1f}；一个月里，它的账比另一本多亏了{-worse:.1f}。<bookmark mark='c'/>在这个示意里，深度对冲的账后来恢复了，因为还活着的账可以卖出昂贵的期权。已经关闭的基金不能。",
    "Two historical cases. The SEC's 2021 complaint alleged that LJM misrepresented i":
        "两个历史案例。SEC的2021年起诉书指控LJM虚报风控，2018年2月波动率飙升使其两个交易日损失超过10亿美元、逾80%。此后的记录包括终局判决，以及2026年9月设立的公平基金，不能省略这一后续处理。<bookmark mark='a'/>安联环球投资美国公司的Structured Alpha基金在2020年3月损失超过70亿美元市值；检方把它与逾32亿美元本金损失区分。美国业务于2022年5月认罪，综合解决方案包括赔偿、罚款和没收。SEC记载一份报告删去一个数字，把崩盘损失42%改为4%。这里的教训是隐瞒风险与风控，不是说所有做空波动率策略都涉及欺诈。",
    'Why do short-volatility books fail all at once?':
        "为什么做空波动率的账会同时失败？卖出看跌期权是Delta多头、Gamma与Vega空头。<bookmark mark='a'/>在崩盘中，价格下跌与隐含波动率上升让这些方向项同时亏损；Theta和高阶项仍需计入。<bookmark mark='b'/>任何宽度的同到期日、同数量看跌价差，到期支付负债都不超过行权价差，最大净损失还应减去初始净收入。保护腿越远，这个上限越大；在35%下跌中，虚值40%的保护腿到期仍无支付。这不消除到期前的保证金与流动性风险。下一章看做市行业。",
    'Chapter seventeen. The industry':
        '第17章。业界：谁在为期权做市，又是怎么做的。',
    'First the scale.':
        "先看规模。美国每一份上市期权都由同一家公司清算，即期权清算公司，它站在买卖双方之间。2019年它清算了约五十亿份合约。<bookmark mark='a'/>然后散户来了，短期期权也随之而来：2021年一百亿，2023年一百一十亿，按它自己的年报，2025年一百五十三亿。每一个执行价，整天都得有人报价。这些OCC总量同时包括期权与期货。清算说法针对美国上市证券期权，不包括美国所有期货期权。",
    'Who is on the other side of retail?':
        "散户的对手是谁？斯韦特兰娜·布里兹加洛娃、安娜·帕夫洛娃和塔伊西娅·西科尔斯卡娅追踪了这一点。按她们的测量，散户交易已占美国期权成交量的百分之六十以上，期权的订单流付费近百分之九十来自三家批发商：城堡证券、萨斯奎哈纳和沃尔弗林。散户偏爱便宜的短期期权，付出很宽的价差，平均亏钱。<bookmark mark='a'/>德米特里·穆拉维约夫和尼尔·皮尔逊展示了另一面：一个对照随股价移动的公允价值择时下单的交易者，付出的有效价差不到常规测量的百分之四十。<bookmark mark='b'/>停下来预测一下：批发商为什么要为你的订单付钱给券商？因为平均而言，你的订单不是知情的：第8章的逆向选择，反过来运行。",
    'The firms, from the public record.':
        "来自公开记录的公司。萨斯奎哈纳1987年5月成立，起家于期权做市；据它自己的招聘启事，它的培训教授博弈论和扑克。<bookmark mark='a'/>Optiver和IMC分别于1986年和1989年在阿姆斯特丹期权交易大厅起步，如今在全球以电子方式报价。<bookmark mark='b'/>简街成立于2000年，为基金、债券和期权做市。<bookmark mark='c'/>记录里也有麻烦。2008年，美国商品期货监管机构指控Optiver的交易员在2007年的一个月里至少十九次试图通过在收盘前大量交易来操纵石油和汽油期货的结算价格；2012年的一项同意令让公司及其交易员支付了一千四百万美元。",
    'And how does a desk run':
        "一个交易台是怎么运转的，按公司公开的描述、也按本部分搭建的样子？一个循环。拟合一张波动率曲面，第12部分，并在报价和成交到来时重新拟合。<bookmark mark='a'/>围绕它以波动率报出买卖价，朝库存反方向倾斜，第9章。让每个希腊字母，按到期和执行价，都在限额之内。用期货自动对冲delta，用其他期权对冲伽马和vega，第10章。<bookmark mark='b'/>每天早上，逐项解释昨天，第1章，追查任何解释不了的部分。<bookmark mark='c'/>在这个循环之外，交易场所的规则塑造着交易：到期怎么结算，适用什么保证金和持仓限额，交易所发布哪些指数。最后，前沿。",
    'Chapter eighteen. The frontier':
        '第18章。前沿：学会交易期权。',
    'f"Try a historical walk-forward replay before discussing the papers. The target ':
        "先看历史向前滚动重放，再讨论论文。目标是每周三开始、随后四周的假设对冲跨式损益。<bookmark mark='a'/>四个输入为隐含波动率减HAR、减此前实际波动率、风险逆转和期限斜率。微笑从当日记录重建，尚未确立全部输入在早八点入场时已可得。<bookmark mark='b'/>岭回归与二层提升树用更早的结果重新拟合，并留四周间隔；这处理了重叠结果，却不能修复报价时点，也不认证可交易回测。<bookmark mark='c'/>代码设定已在登记簿中，截至本部分计数为{f['trials']}；记录不证明登记早于计算。我们保留原始重放及其局限。",
    'Watch it run.':
        "看它运行。每周两个模型都在过去的数据上重新拟合，做出一个预测，带着训练集五次自助重抽样拟合给出的区间。白线是实际发生的。右边是各自的累计样本外误差，对照最简单的预测：过去的平均值。<bookmark mark='a'/>预测贴着一个略为负的水平几乎不动，而实际结果在两侧大幅摆动。带状区域是5次普通自助重拟合的最小与最大值，不是置信区间或预测区间；重叠周次的推断须处理依赖。所有已记录的结果、预测与累计误差均保留完整尺度。",
    'f"The verdict.':
        "结论。{say}<bookmark mark='a'/>九十六个重叠的星期、一个资产，诚实的预期就是如此，这也是前沿论文要用数百万观测的原因。停下来预测一下，第26部分的教训：一个试了四十次才找到t为三的模型，真正值多少？扣除尝试次数之后，要少得多。",
    'Neither model can tell a good week from a bad one: their correlations with the outcome are about zero. What':
        '两个模型都分不清好星期和坏星期：它们与结果的相关性约为零。它们学到的是数据确实显示的唯一一件事，即波动率的买方平均亏钱，所以它们几乎每周都说卖，赚到的也就是一直卖出所赚的。溢价活了下来；择时没有。',
    'Neither model can tell a good week from a bad one: their correlations with the outcome are about zero, and':
        '两个模型都分不清好星期和坏星期：它们与结果的相关性约为零，它们赚到的是溢价，不是择时。',
    'The models show some timing ability':
        '模型显示出一些择时能力，需要第二个样本来确认。',
    'What the frontier has.':
        "前沿有什么。图兰·巴利、海纳·贝克迈尔、马蒂亚斯·默尔克和弗洛里安·魏格特用两百六十五个特征、一千二百万条1996到2020年的观测训练非线性模型：它们对delta对冲后的股票期权收益的预测，好到多空组合扣除成本后仍能盈利，而基于期权的特征最重要。<bookmark mark='a'/>曹杰、约翰·赫尔和合作者用分布式强化学习，在有成本时用第二份期权对冲伽马和vega：第10章的问题，被学会了。<bookmark mark='b'/>巴尔达奇、贝尔戈和盖昂把多期权做市化简为少数几个风险因子，使之可解；方舟和许海清训练了一个强化学习者，在各执行价和到期日上设定价差：第9章，规模化。<bookmark mark='c'/>深度对冲是第17部分；当日到期期权是第12部分。",
    'f"The House now has Greek reports, hedge ledgers and quoting tools. <bookmark ma':
        "House已有希腊值报告、对冲账本和报价工具。<bookmark mark='a'/>表格列出各方法对应的实现。<bookmark mark='b'/>第十一条规则：设置希腊值限额、计入成本、解释损益，并规划到期处理。本部分已有两个设定记录，截至本部分计数为{f['trials']}；登记条目本身不确立前瞻验证。",
    'The recap. Greek explains are local approximations. Gamma weights the path. Freq':
        '回顾：希腊值分解是局部近似；Gamma对路径加权。频率改变误差与成本，本样本不能分辨其均值效应。波动率报价坐标描述多种敞口。历史模型亏损不保证卖方利润，标记价格也只是公允价值代理。库存控制依赖模型，到期Gamma集中于行权价附近，相关性交易需要匹配敞口。崩盘损失检验保护宽度、流动性、杠杆与如实披露；每个结果都要伴随假设。',
    'Three desk questions. A hedged straddle in a quiet week':
        "三个交易台问题。安静一周里对冲后的跨式组合，损失时间价值，如果隐含波动率下降还损失vega。<bookmark mark='a'/>骰子：先围绕三点五报价，知道是偶数后围绕四报价，并问问自己为什么有人告诉你。<bookmark mark='b'/>还有一份深度实值的美式看涨，明天派息二，利率百分之四，还剩两个月，看跌值三十美分：行权，因为股息胜过六十六美分的利息加上看跌期权。完整解答见笔记。",
    'And ten problems':
        '还有十道习题：伽马–时间损耗积分，到期时的伽马，两资产的隐含相关性，有知情对手的骰子游戏，对冲带的标度，vanna和volga，离散度交易的符号，以及最优报价的方向。其中两道是资格考试题：交易商的需求压力，以及它在明确矩条件下的局部累积量展开。中英文解答见笔记。',
    'Where this comes back.':
        '这些内容会在哪里再出现。微笑、方差互换、当日到期期权和交易商伽马在第12部分。随机波动率在第13部分为账本的vega风险建模，奇异期权的希腊字母在第15部分。深度对冲在第17部分长大，第26部分清点每个优势背后的回测次数。逆向选择和库存在订单簿与做市部分回归，价格冲击以及操纵为何可能，则在执行和市场中的机器两部分。',
    'The books this part draws on':
        '本部分依据的书，都由交易员写成，还有相关论文，从做市商的经典模型到这十年的机器学习。数据是Deribit的成交和隐含波动率指数、币安的比特币价格、芝加哥期权交易所的隐含相关性指数、肯尼斯·弗伦奇的市场和行业数据，以及监管机构自己的研究、命令和起诉书。',
    'The volatility desk can now quote, hedge and size.':
        "波动率交易台现在能报价、对冲和定仓位了。<bookmark mark='a'/>下一部分，第12部分：波动率曲面。为什么隐含波动率取决于执行价和期限，如何无套利地拟合它，以及局部波动率如何看待它。",
    'For the researcher: Chapter 9 noted':
        '写给研究者：第9章提到，做市商的库存会移动它的报价，而需求本身也会移动期权价格。这里是第二个事实的理论：为什么终端用户的净需求会弯曲微笑，它弯曲哪些期权，以及什么时候它弯曲不了。',
    'A simplified dealer problem, under a fixed martingale measure Q and zero rates a':
        "这是简化的交易商问题，固定鞅测度Q，利率与收益率为零。<bookmark mark='a'/>按离散时点对冲每个期权，再把支付减对冲收益的余项减去自身期望。<bookmark mark='b'/>令q表示交易商卖出数量，持仓因此为负q；市场出清令q等于客户需求d。<bookmark mark='c'/>在这个均值方差示例中，首阶条件是在模型基准上，加上风险厌恶系数乘余项协方差矩阵乘需求。交叉影响的符号取决于协方差。<bookmark mark='d'/>Gârleanu、Pedersen与Poteshman于2009年发展了更丰富的动态需求定价理论；这里的单期计算说明机制，不复现其完整均衡，也不识别市场风险溢价。",
    'Three consequences.':
        "三个推论。<bookmark mark='a'/>一个期权自身的需求对其价格的推动，正比于它有多难对冲。<bookmark mark='b'/>对一个执行价的需求会移动其他执行价，正比于它们残差的协方差：相邻执行价共享大部分不可对冲的风险，所以需求会沿着微笑扩散。<bookmark mark='c'/>而在布莱克和斯科尔斯的世界里，连续对冲、没有跳跃，残差消失，效应也随之消失：价格由复制决定，不管谁想要什么。",
    'How large is the residual?':
        "残差有多大？模拟一个像比特币那样的跳跃扩散，每天对一个月期期权做Delta对冲。<bookmark mark='a'/>有跳跃时，残差是标的的百分之一到二，在平值处最大。<bookmark mark='b'/>去掉跳跃，它下降一半或更多。<bookmark mark='c'/>再改成每小时对冲，它几乎消失。市场越完全，需求移动价格的余地就越小。这是零漂移模型示例，不是拟合的比特币规律。所报跳跃均值与尺度是对数跳跃参数；跳跃情形用4万条路径，两个扩散比较各用8000条。",
    "f'Now apply demand.":
        "现在加上需求。<bookmark mark='a'/>灰线是跳跃模型的风险中性微笑：已经因为跳跃而偏斜。<bookmark mark='b'/>对单独一份八十五看跌期权的需求，按构造把它自己的波动率抬高一个点，同时把八十看跌抬高{p85[0]:.1f}个点，甚至把一百二十看涨抬高{p85[-1]:.1f}个点。<bookmark mark='c'/>对每个看跌期权的需求让偏斜变陡：八十处{pu[0]:.1f}个点，一百二十处{pu[-1]:.1f}个点。<bookmark mark='d'/>对看涨期权的需求让它向另一边倾斜。微笑的形状承载着需求的形状。",
    'f"Compare the first-order line with exponential tilting of these forty thousand ':
        "把首阶直线与这4万个中心化余项的指数倾斜比较，保持Delta对冲固定。这是有限经验样本的计算，不是优化对冲后的效用价格，也不证明总体指数矩存在。<bookmark mark='a'/>小头寸时两者接近。<bookmark mark='b'/>期权余项是卖方交易商的负债，其正偏度为{i['skew_eps']:.1f}；经验边际溢价在{q[j1]:.2f}单位时比直线高{100 * r1:.0f}%，4单位时高{100 * r4:.0f}%。非线性与样本尾部敏感性很重要，这些百分比属于这次有限模拟。",
    "f'What does demand look like?":
        "需求是什么样子？在曲面那两天的Deribit成交中，数一数穿越价差的那一方，作为终端用户的粗略代理。<bookmark mark='a'/>在平值附近，买卖平衡；一个月以内，吃单方是虚值看跌期权的净卖方，{100 * f['otm_put_short']['net_share']:+.0f}%。<bookmark mark='b'/>一个月以上，吃单方是虚值看跌期权的净买方，占其vega的{100 * f['otm_put_long']['net_share']:+.0f}%，并且是虚值看涨期权的净卖方，{100 * f['otm_call_long']['net_share']:+.0f}%：买入保护，卖出上行，一个领口。理论说，这样的流量应当让长期限的偏斜变陡。两天只能描述它；检验需要多年的数据。这里只统计有隐含波动率记录且距到期超过一天的合格成交。主动成交方未必是终端客户；汇总的买认沽、卖认购不识别同一投资者，也不证明领口策略或需求的因果影响。",
    "Three open questions. <bookmark mark='a'/> Dealers' risk aversion":
        "三个开放问题。<bookmark mark='a'/>交易商的风险厌恶无法观测。它随资本和亏损而变，所以把需求效应与变化的风险分开很难。<bookmark mark='b'/>第6章的波动率溢价中，有多少是对定价风险的补偿，有多少是吸收对冲需求的价格，仍有争论。<bookmark mark='c'/>而在有许多交易商、库存跨期持有、以及第9章的报价动态下，应在明确模型下比较均衡价格与报价动态。",
    'Pause and predict. Demand arrives for the eighty-five put.':
        '暂停预测。对八十五看跌期权的需求来了。以美元计，九十看跌和八十看跌哪个涨得更多？以隐含波动率计呢？为什么两个答案可能不同？',
}

PHRASES = {
    "straddle": "跨式组合", "strangle": "宽跨式组合", "risk reversal": "风险逆转", "butterfly": "蝶式价差",
    "call spread": "看涨价差", "calendar": "日历价差",
    "the hedged one shows it clearly": "对冲后的则清楚地显示了它", "even hedged it is hard to see": "即使对冲后也很难看出",
}

ZH.update({'The ninety put rises more in dollars; the eighty put rises more in implied volatility': '90认沽的美元价格涨得更多；80认沽的隐含波动率涨得更多，因为其Vega更低。美元影响与波动率影响衡量的是不同的量。'})

ZH.update({'This sample does not resolve a mean difference; that is not proof of equal expected profits.': '这个样本不能分辨均值差异，但这不证明期望利润相同。'})
