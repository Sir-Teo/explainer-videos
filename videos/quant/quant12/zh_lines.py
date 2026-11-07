"""Chinese narration for quant12: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第12部分：波动率曲面'

CHAPTERS = {
    'Hook': '恐惧的形状',
    'Smile': '1. 读懂微笑',
    'Dynamics': '2. 曲面如何移动',
    'Arbitrage': '3. 静态套利：不可能的形状',
    'SVI': '4. SVI：五个数描述一条微笑',
    'SSVI': '5. SSVI：一个公式描述整张曲面',
    'LocalVol': '6. 推导杜皮尔局部波动率',
    'Gyongy': '7. 久恩吉：每个模型都有一个局部波动率孪生',
    'Forward': '8. 局部波动率的未来',
    'VarSwap': '9. 方差互换：直接买入波动率',
    'Replicate': '10. 在真实比特币上复制；波动率互换',
    'VIX': '11. VIX，以及我们自己的指数',
    'VRP': '12. 方差风险溢价的测量',
    'Moments': '13. 期权价格对未来说了什么',
    'ETP': '14. VIX期货、展期与做空波动率票据',
    'Volmageddon': '15. 波动率末日：2018年2月5日',
    'Gamma': '16. 交易商Gamma与当日到期期权',
    'Learning': '17. 学习曲面',
    'Industry': '18. 谁在构建曲面，谁在出售曲面',
    'Frontier': '19. 前沿，2023–2026',
    'Research': '写给研究者：从含噪价格中读出密度',
    'Outro': '回顾、交易台问题与习题',
}

PHRASES = {
    'the network even beats it, ': '网络甚至胜过它，',
    'fitted to each week it does better, ': '按周单独拟合时它更好，',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part twelve. The volatility surface.":
        "第12部分。波动率曲面。布莱克和斯科尔斯假设只有一个波动率。市场却为每个执行价、每个到期日报出不同的波动率，它画出的形状，就是市场的恐惧地图。",

    'Here is the Surface, our frozen Bitcoin pricing example. Each white dot is an im':
        "这是曲面，我们冻结的比特币定价示例。每个白点都是由期权标记价格还原的隐含波动率，汇总了午夜到中午的记录，并非同一时刻可成交的报价。<bookmark mark='a'/>拟合误差不到一个波动率点。无套利充分条件覆盖了已报价的到期日，却不覆盖任意接近零的期限。<bookmark mark='b'/>读它的形状：沿执行价是微笑，沿到期日是期限结构。本部分介绍这些形状、检验以及建立在其上的模型与合约。",

    "How did the surface become the market's language? Black and Scholes' 1973 model ":
        "曲面怎样成为市场语言？布莱克与斯科尔斯1973年的模型提供单一波动率基准。<bookmark mark='a'/>1987年10月的崩盘使股票指数下行偏斜尤其突出，却不是首次可能偏离平坦微笑。<bookmark mark='b'/>Cboe在1993年推出原始VIX。杜皮尔、德曼与卡尼以及鲁宾斯坦在1994年发展局部波动率和隐含树方法；方差期权串研究推动了2003年的VIX改版。<bookmark mark='c'/>随后出现期货与波动率挂钩票据，2018年暴露其重置风险。<bookmark mark='d'/>比特币带来DVOL、波动率期货与ETF期权。这些发展分别回应不同的定价、对冲或指数构建问题。",

    'Here is a simplified one-volatility benchmark, shown as a flat plane. It is not ':
        "这里将简化的单一波动率基准画成平面，并不是说1987年前每个市场微笑都平坦。暂停预测：在这个拟合比特币示例中，哪个角升得最高？<bookmark mark='a'/>短期下行角。平面弯成2025年12月拟合的有限视图。所画执行价、期限和波动率范围是显示选择，并不是全部无报价尾部。隐含波动率仍是价格语言，而曲面组织了一组期权价格。",

    "The plan. Reading the smile as a distribution;":
        "本部分的安排。把微笑读成一个分布；曲面如何移动，哪些形状不可能存在。拟合：SVI、SSVI和杜皮尔局部波动率。把波动率当作资产："
        "在真实比特币上做方差互换，重建VIX，以及市场为方差支付的溢价。2018年爆仓的那些产品，以及交易商的对冲。最后是学习曲面的神经网络、"
        "构建曲面的机构，以及前沿研究。",

    "In the House, this part builds the surface builder.":
        "在我们的公司里，本部分搭建曲面构建器。<bookmark mark='a'/>从现在起，波动率交易台报出的每一个价格都从它拟合的曲面上读出，而这张曲面要先通过第9部分的"
        "套利检查器。这一部分试验计数器不会变动：我们在这里测量的一切，都是价格或描述，而不是在检验一个策略。",

    # ------------------------------------------------------------------ Smile
    "Chapter one. The smile, read.": "第1章。读懂微笑。",

    "Here are three slices of the Surface":
        "这是基准曲面的三个切片：一个短期、一个中期和一个长期到期日。每个点是一个报价。<bookmark mark='a'/>每个切片都是一条微笑：两翼都高于中间。"
        "这一天左翼又高于右翼：这是偏斜，为防范下跌支付的溢价。<bookmark mark='b'/>短期的弯曲最大；长期的更平坦，也更稳定。"
        "整个这一部分里，我们用对数价值度k来度量执行价，即执行价与远期之比的对数；用总隐含方差w来度量微笑：波动率的平方乘以时间。"
        "在这两个坐标里，定理都变得简单。",

    'Why this shape? Option prices are expectations under a risk-neutral law. Gaussia':
        "为什么会有这种形状？期权价格是风险中性分布下的期望。高斯对数收益率给出平坦的布莱克—斯科尔斯微笑。<bookmark mark='a'/>示意密度改变对数收益率的偏度参数：负值相对抬高看跌，正值反之。<bookmark mark='b'/>正的峰度参数抬高两翼。多项式可能变成负数，因此示例将其截为非负、重新归一化，再平移对数收益率以保持远期均值。所以滑块参数未必等于最终分布的精确矩。<bookmark mark='c'/>灰色一阶公式是局部近似，在平值附近最可靠。",

    'As algebra: correct the standardized log-return Gaussian by Hermite polynomials.':
        "代数上，用埃尔米特多项式修正标准化对数收益率的高斯密度。<bookmark mark='a'/>定价并作一阶反演，得到巴克斯、福雷西和吴的倾斜直线与曲率修正。<bookmark mark='b'/>这是微笑斜率与对数收益偏度的局部联系，并不意味着任意分布下两者总是同号。第13章会说明平值附近偏斜为何可能与整个分布的偏度不同。<bookmark mark='c'/>在日历套利条件成立时，固定远期价内程度上的隐含总方差必须随期限非递减；其期限增量定义远期隐含方差，而不是现实方差预测。",

    'f"Now the same two coordinates through time: {n} Wednesdays of Bitcoin surfaces ':
        "现在把同样两个坐标放到时间里：自2021年4月以来的{n}个周三的比特币曲面，每一张都用当天早上的成交重建。上方是四个期限的平值波动率。<bookmark mark='a'/>平均而言期限结构向上倾斜，从一周的{m7:.0f}%到六个月的{m180:.0f}%。但在{inv:.0f}%的周里它会倒挂，短端跳到长端之上：那是崩盘和逼空的周，恐惧关乎当下。<bookmark mark='b'/>下方是三十天偏斜，看跌更贵时为红色，看涨更贵时为金色。比特币的微笑在{cs:.0f}%的周里偏向看涨。标普500自1987年崩盘后通常偏向看跌；比特币的买家却常常为上涨付出比为崩盘更多的钱。暂停一下，预测：在局部对数收益示例里，正的偏度参数使平值附近微笑向哪边倾斜？向看涨一侧。微笑曲线是一张快照。下一章：整个曲面怎样移动。",

    # ------------------------------------------------------------------ Dynamics
    "Chapter two. How the surface moves.": "第2章。曲面如何移动。",

    "Here is the Surface's thirty-day smile, against fixed strikes.":
        "这是基准曲面的三十天微笑，画在固定的执行价上。移动现价：微笑会去哪里？<bookmark mark='a'/>粘性执行价：每个执行价保持自己的波动率，曲线不动，"
        "平值点沿着它滑动。粘性价值度，或者说粘性delta：微笑随现价一起移动。<bookmark mark='b'/>而局部波动率，即第6章的模型，让它朝相反方向移动。"
        "伊曼纽尔·德曼在1999年把这些称为波动率的几种状态。暂停一下，预测：现价下跌5%，偏斜是每1%价值度0.4个波动率点，粘性执行价。"
        "平值波动率呢？高出两个点。",

    'f"Desks quote by delta.':
        "交易台按delta报价。二十五delta看涨期权满足N(d1)等于四分之一：大约在远期之上三分之二个标准差。<bookmark mark='a'/>风险逆转读出斜率，"
        "蝶式读出曲率：基准曲面在三十天上分别是{rr:+.1f}和{bf:+.1f}个点。<bookmark mark='b'/>为了度量所处的状态，洛伦佐·贝尔戈米的偏斜粘性比R，"
        "把每单位对数现价引起的平值波动率变动，除以偏斜。<bookmark mark='c'/>粘性执行价给出1；粘性价值度给出0。<bookmark mark='d'/>"
        "而当R不等于1时，每个固定执行价的波动率都会随现价变动，于是delta多出一个vega项。",

    'f"Test the rules on {n} pairs of consecutive weeks:':
        "在{n}对相邻周上检验这些规则：用本周的三十天微笑预测下周的，分别固定价值度或固定执行价。粘性价值度平均误差{mm:.2f}个波动率点，"
        "粘性执行价{ms:.2f}，粘性执行价只在{sb:.0f}%的周里胜出。<bookmark mark='a'/>现在直接估计这个比率：把平值波动率的周变动对对数现价的变动回归，"
        "再除以平均偏斜。点估计是{rhat:.1f}，t统计量为{tstat:.1f}。{branch}",

    "This time the slope is clearly not zero:":
        "这一次斜率明显不为零：比特币上涨时平值波动率下降。除以一个很小的平均偏斜，比率落在2附近，即局部波动率的数值；斜率的符号比比率的大小更可信。",

    "Do not believe it.":
        "别信它。斜率与零无法区分，比特币的平均偏斜也接近零，两个小而嘈杂的数之比无法识别。在偏斜陡峭而稳定的股票指数上，同样的回归是有信息的；"
        "在这里我们无从判断。",

    'f"Real surfaces do not follow any one rule.':
        "真实的曲面不遵循任何一条规则。所以直接测量它们怎样移动。取每周从一个月到六个月的网格对数变化，六十八个数，求它的主成分，"
        "正如拉马·孔特和若泽·达丰塞卡在2002年对指数期权所做的。<bookmark mark='a'/>第一个成分是水平：整张曲面一起上下呼吸。它解释了{e1:.0f}%的方差。"
        "<bookmark mark='b'/>第二个成分让偏斜倾斜，看跌对看涨：{e2:.0f}%。<bookmark mark='c'/>第三个让短端与长端反向，并让微笑弯曲：{e3:.0f}%。"
        "每周三个数承载了六十八个数运动中的{tot:.0f}%，维度之低、三个形状之相似，都与孔特和达丰塞卡在标普500上的发现一致。第17章将让一个神经网络找到它自己的坐标。"
        "在拟合任何曲面之前，先要知道哪些形状是不可能的。下一章。",

    # ------------------------------------------------------------------ Arbitrage
    "Chapter three. Static arbitrage: the shapes no market can draw.": "第3章。静态套利：任何市场都画不出的形状。",

    'f"Here is a smile that looks perfectly reasonable:':
        "这是一条看起来完全合理的微笑：一年期的原始SVI曲线，参数由一位名叫阿克塞尔·福格特的分析师在网上发布，盖瑟尔和雅基耶把它用作警示例子。"
        "<bookmark mark='a'/>在它下面，是微笑的一个函数g(k)，从左往右画出。看它穿过右翼的时候。<bookmark mark='b'/>它跌到了零以下。g为负的地方，"
        "隐藏在微笑中的概率密度也为负。在那里构建蝶式组合：它的价格是远期的{flm:.1f}百万分之一，一个永不为负的收益，价格却是负的。"
        "<bookmark mark='c'/>数额很小，埋在远处的翼里，在价格图上看不出来。这正是交易台检查g而不是价格的原因：喂给这条微笑的定价引擎，会悄悄地卖出套利。",

    "The derivation. Write Black's formula in log-moneyness and positive, smooth tota":
        "推导从对数价内程度与正的、光滑的总方差下的布莱克公式开始。<bookmark mark='a'/>看涨价格对执行价求两次导数，得到一个正因子乘以g。<bookmark mark='b'/>g非负意味着密度非负；完整的蝶式无套利刻画还需要适当的尾部边界条件。有限网格扫描本身不是全局证明。<bookmark mark='c'/>对具有所述持有成本归一化的非负鞅，凸序要求固定远期价内程度上的总方差随期限非递减。<bookmark mark='d'/>李的矩公式将总方差除以绝对对数价内程度的渐近上极限限制为二；它约束极端尾部，并不约束有限图上的每一个斜率。",

    'f"Is the Surface itself clean?':
        "基准曲面本身干净吗？像一个粗心的交易台那样，每个到期日单独拟合SVI，再比较相邻的到期日。<bookmark mark='a'/>在{nb}对中，"
        "较晚到期日的总方差跌到了较早到期日之下：曲线相交，红色区域里一个日历价差的成本低于零。它们全都出现在几天后到期的那几个到期日，"
        "那里每条拟合只靠寥寥几个报价支撑。<bookmark mark='b'/>每个切片单独看都通过了第9部分的逐个执行价检查器，违规{viol}处。"
        "套利藏在切片之间，所以曲面必须作为一张曲面来拟合。",

    'f"Lee\'s bound on the Surface. These are the fitted SVI asymptotic wing slopes, c':
        "曲面上的李界限。这里比较的是拟合SVI的渐近翼部斜率与上限二。<bookmark mark='a'/>最长期限的看跌翼为{bl}，看涨翼为{br}。若把拟合尾部无限外推，李公式的反演给出约{1 + pr:.1f}的上尾临界矩幂；它并不保证临界端点处的矩有限，也不识别没有报价的真实尾部。暂停预测：渐近翼部斜率为二点五呢？<bookmark mark='b'/>它违反必要的尾部界限，应拒绝或修正这种外推；这不是卖出无保护远端看涨期权的指令。接下来是SVI。",

    # ------------------------------------------------------------------ SVI
    "Chapter four. SVI: a smile in five numbers.": "第4章。SVI：五个数描述一条微笑。",

    'In 2004 Jim Gatheral published SVI, stochastic volatility inspired, used at Merr':
        "2004年，吉姆·加瑟拉尔发表了SVI，即受随机波动率启发的参数化，1999年起已在美林使用。它用五个参数将总方差写成双曲线。<bookmark mark='a'/>a整体抬高曲线，b控制翼部斜率。<bookmark mark='b'/>rho使其倾斜，m使其平移，sigma使顶点圆滑。施加约束后，渐近直线翼是一种符合李斜率界限的实用参数化。李定理并不要求每条可行微笑都具有完全笔直的翼部。",

    "The formula. <bookmark mark='a'/> Far out,":
        "公式。<bookmark mark='a'/>在远处，平方根变成绝对值：两翼是斜率为b乘以rho加减一的直线；令导数为零得到底部。<bookmark mark='b'/>"
        "李的界变成一个参数盒：b乘以一加rho的绝对值，至多为2。<bookmark mark='c'/>交易台报的是跳跃翼形式：平值方差与偏斜、两翼的斜率、最小值。"
        "盖瑟尔和雅基耶在2011年证明，赫斯顿模型的隐含方差在长期限下恰好变成SVI。<bookmark mark='d'/>固定m和sigma后，拟合对其余参数是线性的，"
        "这是Zeliade在2009年给出的化简，把搜索降到二维。",

    'f"Here is the House\'s fitter. The residual is the weighted gap in total variance':
        "这是我们公司的拟合器。残差是总方差的加权差。六个起点，从每个起点做一次有界最小二乘搜索，边界包含李的界：b乘以一加rho的绝对值永远不超过2。<bookmark mark='a'/>在基准曲面的{days:.0f}天到期日上运行它，{n}个报价，按vega加权：五个数，拟合误差在{rm:.2f}个波动率点以内。",

    'f"Watch the fit happen. Six starts drawn at random, the worst of them {hi:.0f} v':
        "看拟合如何发生。六个随机起点，最差的离报价{hi:.0f}个波动率点，最好的{lo:.0f}个。每条线是一个起点当前的猜测；右边是每次计算残差后的误差，取对数坐标。<bookmark mark='a'/>在{n0}到{n1}次计算之内，每个起点都落在同一条曲线上，误差{best:.3f}个波动率点。在这个示例中，六个起点得到了相近拟合；这不能证明每个到期日的优化问题都很温和。麻烦始于把到期日分开拟合，正如第3章所示。",

    'f"And here is the whole Surface in the trader\'s coordinates, one row per expiry.':
        "这是用交易员坐标表示的整张基准曲面，每行一个到期日。平值方差随期限上升，偏斜psi很小，两翼变陡：在最长的到期日，看跌翼为{pw:.2f}，看涨翼为{cw:.2f}。<bookmark mark='a'/>十一条拟合中最小的g是{gmin:.2f}：在负一到一的对数价内程度采样网格上，没有发现负g。有限扫描不是对所有执行价的证明。克劳德·马蒂尼和阿丽安娜·明戈内在2022年准确刻画了哪些SVI参数能保证这一点；而第3章表明，逐个干净的切片仍可能相交。解决办法是把曲面作为一个整体来拟合。下一章：SSVI。",

    # ------------------------------------------------------------------ SSVI
    "Chapter five. SSVI: the whole surface in one formula.": "第5章。SSVI：一个公式描述整张曲面。",

    "SVI fits one expiry.":
        "SVI拟合一个到期日。盖瑟尔和安托万·雅基耶2014年的曲面SVI，一次拟合全部到期日。先为每个到期日取一个数：theta，平值总方差，"
        "它必须随期限上升。看，它沿着左侧墙面攀升。<bookmark mark='a'/>然后在每个theta上挂同一条微笑，宽度由一个函数phi(theta)决定，"
        "倾斜由一个相关系数rho决定。<bookmark mark='b'/>把切片扫在一起，就得到一张只有三个形状参数、外加各个theta的曲面。",

    'f"The House\'s fitter maps unconstrained search variables to constrained paramete':
        "本行的拟合器将无约束搜索变量映射为有约束参数。双曲正切约束rho；eta乘以一加rho绝对值不超过二；正增量的累加保证theta非递减。这对该幂律形式施加了日历条件，但当gamma超过二分之一时，单靠eta上限不能证明蝶式条件。<bookmark mark='a'/>过滤后的报价得到rho为{f['rho']:.2f}、eta为{f['eta']:.2f}、gamma为{f['gamma']:.2f}，vega加权误差为{rm:.2f}个波动率点。下一节定理给出剩余的期限限制。",

    'f"Now watch it fit, in three dimensions. White dots are the quotes. This start i':
        "现在在三维中看它拟合。白点是报价。这个起点是{nr}个中最差的，大约差{start:.0f}个波动率点。右边是每次计算后的误差，回放的起点为紫色，其他为灰色。<bookmark mark='a'/>曲面抬起、倾斜、折叠到这些点上，镜头随之环绕。<bookmark mark='b'/>每个起点最终都落在同一误差的{max(finals) - min(finals):.4f}以内，即{min(finals):.2f}个点。一个十二参数的拟合，覆盖过滤后的报价。搜索期间施加日历约束，但不能保证每个中间曲面都没有蝶式套利。",

    'f"The theorems. Here is SSVI,':
        "定理。这是带幂律phi的SSVI。<bookmark mark='a'/>盖瑟尔和雅基耶证明，它没有日历套利，当且仅当theta上升且theta乘以phi保持在一个区间内；"
        "对幂律，这个区间总是成立。<bookmark mark='b'/>对蝶式套利，他们给出了一个充分条件：关于theta和phi的两个不等式。<bookmark mark='c'/>"
        "代入幂律。第二个不等式在theta趋于零时保持有界，当且仅当gamma至多为二分之一。在基准曲面上，gamma为{gm:.3f}。{branch}",

    "So the fit is provably free of butterflies at every maturity.":
        "所以这个拟合在每个期限上都可证明没有蝶式套利。",

    "And here an honest caveat.":
        "这里要诚实地说明一点。拟合出的gamma大于二分之一，所以充分条件在theta极小时失效：它只在大约千万分之一以上成立，覆盖了每个实际报价的到期日，"
        "但并非原则上的每个theta。直接检查，拟合切片上最小的g仍然明显为正。",

    'f"What does consistency cost?':
        "一致性要付出什么代价？逐个到期日，单独拟合该到期日的SVI误差为金色，对照整体一个SSVI的误差为橙色。<bookmark mark='a'/>在第一个到期日，"
        "SVI误差{a0:.1f}个点，SSVI为{b0:.1f}；在最后一个，{a1:.1f}对{b1:.1f}。{nsvi}个自由参数在样本内总是拟合得更好。但它们彼此相交，"
        "正如第3章所示，在到期日之间不可信。交易台从不能被套利的曲面上报价，并在最初几天为此付出代价，因为一个微笑形状跟不上那里的报价；"
        "一个月以后差距只有零点几个点。eSSVI之类的扩展让倾斜随期限变化，缩小了部分差距。"
        "拟合好的曲面是一张价格表。下一章：藏在其中的模型——杜皮尔的局部波动率。",
}

ZH.update({
    # ------------------------------------------------------------------ LocalVol
    "Chapter six. Dupire's local volatility, derived.": "第6章。推导杜皮尔局部波动率。",

    'Can one model reprice every option on the surface at once? Let volatility depend':
        "一个模型能同时为曲面上的每个期权重新定价吗？让波动率只取决于价格和日期：一个关于S和t的确定性函数sigma，但代入的价格是随机的。半透明的这张，是基准曲面的隐含波动率。<bookmark mark='a'/>实心的这张，是从它的斜率算出、能复现它的局部波动率。<bookmark mark='b'/>把镜头降下来，沿着执行价方向看：局部曲面更陡，大约是隐含曲面的两倍，在短端弯得最厉害。隐含波动率是由价格定义的有效参数，并非对路径上局部波动率作普通的无条件平均。",

    "If the price diffuses with volatility sigma of S and t,":
        "如果价格以关于S和t的波动率sigma扩散，它的密度满足第5部分的福克–普朗克方程。<bookmark mark='a'/>把看涨价格对期限求导，放进积分，<bookmark mark='a2'/>"
        "再分部积分两次：收益的二阶导数是执行价处的一个尖峰，只有那里的密度留了下来。<bookmark mark='b'/>除以第9部分的密度，即看涨价格对执行价的二阶导数："
        "这就是布鲁诺·杜皮尔1994年的公式。<bookmark mark='c'/>用总方差表示，分母就是第3章的g：日历条件和蝶式条件，恰好就是局部方差为正的条件。"
        "<bookmark mark='d'/>在短期限下，贝雷斯蒂基、布斯卡和弗洛朗在2002年证明，隐含波动率是从现价到执行价之间局部波动率的调和平均："
        "所以隐含偏斜是局部偏斜的一半。",

    'f"In the House it is three small functions. Gatheral\'s g, local variance as the ':
        "在我们的公司里，这是三个小函数。盖瑟尔的g，局部方差等于时间斜率除以g，以及用中心差分从任意总方差函数求出斜率。<bookmark mark='a'/>在基准曲面的SSVI上，分别取七天、三十天和九十天运行。g始终远高于零，三十天时最小值为{g30:.2f}，所以被检验的局部方差网格有定义；在平值处，局部波动率比隐含波动率低几个点，这是该拟合曲面及其期限、执行价导数的结果，并非普遍的高低关系。",

    'f"Check the factor of two on the Surface.':
        "在基准曲面上检验这个二倍关系。在每个期限，平值处的局部偏斜除以隐含偏斜。<bookmark mark='a'/>它在{lo:.2f}到{hi:.2f}之间：大约是2，"
        "但不恰好是2。这个定理是短期限下的结论，而直线上的平均忽略了微笑的曲率。暂停一下，预测：三十天的隐含偏斜是每单位对数价值度{i30:.3f}。"
        "局部偏斜呢？<bookmark mark='b'/>{l30:.3f}：几乎翻倍。",

    'f"The same year, Derman and Kani':
        "同一年，高盛的德曼和卡尼在一棵树上构建了局部波动率，马克·鲁宾斯坦也构建了他自己的隐含树。灰色的是一棵等间距的树。<bookmark mark='a'/>"
        "现在放置每个新节点，使这棵树能为上一层每个节点处的看涨或看跌期权正确定价。节点被拉伸，各分支的局部波动率从蓝到红，在下方最高。"
        "<bookmark mark='b'/>用四十步覆盖三个月，树自己在到期时的微笑，在平值附近与基准曲面相差{err:.2f}个波动率点以内，节点波动率与杜皮尔的函数相差"
        "{gap:.1f}个点。同一年构建的一棵树和一个公式，是同一个东西。"
        "为什么一个关于价格和时间的函数就够了？下一章：Gyöngy定理。",

    # ------------------------------------------------------------------ Gyongy
    "Chapter seven. Gyöngy's theorem: every model has a local-volatility twin.":
        "第7章。久恩吉定理：每个模型都有一个局部波动率孪生。",

    'Why can one function of price and time reproduce a stochastic-volatility diffusi':
        "为什么价格与时间的一个函数能重现随机波动率扩散的边际分布？在固定风险中性测度下，假定价格是连续伊藤过程、持有成本为零，并满足适当的可积性与存在条件。田中公式给出看涨价格的期限导数。<bookmark mark='a'/>在执行价处条件化，得到密度乘以瞬时方差的条件期望。<bookmark mark='b'/>与杜皮尔公式比较，局部方差就是这个条件期望。捷翁吉的模仿定理及其扩展在适当正则性下支持相应的马尔可夫扩散。它不适用于任意跳跃或所有可能模型。<bookmark mark='c'/>它匹配每个单独时点的分布，而非跨时点的联合分布。",

    'f"Check it by simulation.':
        "用模拟来检验。取一个随机波动率模型，赫斯顿模型，参数接近比特币，跑十万条三个月的路径。每条路径按终点波动率着色。<bookmark mark='a'/>"
        "在终点，每条路径是一个点：价格停在哪里，以及那一刻有多波动。一团点云，看不到任何函数。<bookmark mark='b'/>现在让一块薄板滑过它，"
        "在每个价格处平均板内路径的方差：这些金色的点。<bookmark mark='c'/>然后另起炉灶，用傅里叶方法在赫斯顿模型中给期权定价，把这些价格代入杜皮尔公式："
        "紫色的线。点落在线上，在各个执行价上相差{gap:.1f}个波动率点以内。给定价格下的期望方差，就是杜皮尔的局部方差。",

    'f"Now simulate the fitted Surface\'s local volatility. This is a finite numerical':
        "现在模拟拟合曲面的局部波动率。这是有限数值再定价检验，包含时间离散与蒙特卡洛误差。这里是51天微笑。<bookmark mark='a'/>从500、2000、8000到40000条路径，估计逐步稳定。<bookmark mark='b'/>在采样执行价上，{r1['days']}天相对于拟合微笑的均方根误差为{r1['rmse_ssvi']:.2f}个波动率点，{r0['days']}天为{r0['rmse_ssvi']:.2f}个点。这是平均误差，不是一致误差上界，也不证明所有执行价都被精确重现。四分之一天的离散步长对短端更困难。匹配今天的边际价格仍不能确定明天的联合动态。",

    # ------------------------------------------------------------------ Forward
    "Chapter eight. Local volatility's future.": "第8章。局部波动率的未来。",

    'f"In the ideal continuous model, local volatility reproduces a suitable arbitrag':
        "在理想连续模型中，局部波动率重现适当的无套利输入曲面；数值拟合仍有离散误差。它对明天说了什么？把现价向上移，看它隐含的微笑。<bookmark mark='a'/>在粘性价值度下，微笑随现价一起移动。在局部波动率下，它却朝另一边滑动：局部波动率函数固定在绝对价格上，当现价爬过低波动率区域时，通往每个执行价路径上的平均会反向变化。<bookmark mark='b'/>在基准曲面自己的局部波动率上测得，偏斜粘性比为{R:.2f}。2002年，帕特里克·哈根、迪普·库马尔、安德鲁·列斯涅夫斯基和黛安娜·伍德沃德把这作为他们的批评：一个微笑与市场反向移动的模型，无论今天拟合得多完美，delta都会算错。",

    "Here is why, in three lines.":
        "原因只需三行。一阶近似下，执行价K处的隐含波动率，是现价与执行价中点处的局部波动率。<bookmark mark='a'/>对执行价求导：局部斜率的一半。"
        "固定执行价对现价求导：也是局部斜率的一半。在看跌偏斜下它为负，所以现价上升会降低每个固定执行价的隐含波动率：微笑逆着变动的方向移动。"
        "<bookmark mark='b'/>在平值处，执行价和现价一起移动，两个一半相加，平值波动率随完整的局部斜率移动：两倍的隐含偏斜。比率为2。"
        "<bookmark mark='c'/>哪些产品在乎？远期起始期权按两个未来价格之比赔付：它的价值是一个未来的微笑，没有任何普通期权能确定它。"
        "<bookmark mark='d'/>而局部波动率的偏斜随时间变平，所以它的未来微笑比今天的更平。",

    'f"Simulate forty thousand paths and price unit payoffs on the return ratio over ':
        "模拟四万条路径，为每个未来30天窗口的收益比率单位支付定价。这种比率期权省略了以资产规模加权的远期起始支付中的起始现价乘数。<bookmark mark='a'/>从现在起，百分之九十和一百一十执行价之间的偏斜为{s0:.1f}个点，基准曲面为{st:.1f}个点。<bookmark mark='b'/>起始日从15天推至90天后，这个模型的偏斜减至{s90:.1f}个点。这取决于当前校准，并非普遍的局部波动率定理，也不是未来市场微笑的预测。暂停预测：单时点边际分布相同，是否意味着60天后开始的30天比率期权价格相同？不是，联合分布很重要。第13部分比较这些模型。",

    # ------------------------------------------------------------------ VarSwap
    "Chapter nine. Variance swaps: buying volatility itself.": "第9章。方差互换：直接买入波动率。",

    "A variance swap pays, at expiry,":
        "方差互换在到期时支付价格实际实现的方差，减去今天约定的固定执行价。要对冲它，你需要紫色的曲线：从远期量起的一个对数。没有交易所挂出这个收益。"
        "<bookmark mark='a'/>但你可以构建它。取执行价离远期最近的期权，买入的数量是执行价间距的两倍除以执行价的平方。然后是外面一个，"
        "下方用看跌，上方用看涨，权重相同。<bookmark mark='b'/>曲棍球棒之和向对数曲线弯曲，红色残差缩到远处的两翼，那里执行价用完了。",

    "Why the log? For a positive continuous diffusion, Ito's formula relates quadrati":
        "为什么用对数？对正的连续扩散，伊藤公式将对数价格的二次变差与对数支付及动态交易收益联系起来。精确定价恒等式假定零利率、零股息、可积鞅与连续无成本对冲。<bookmark mark='a'/>卡尔和马丹把光滑支付写成现金、远期与期权串。<bookmark mark='b'/>负对数的二阶导数是一除以K平方；年化方差执行价使用二除以T乘全部虚值期权串的积分。<bookmark mark='c'/>理想恒等式在这些扩散与可积性假设内不依赖具体模型。有限执行价与离散再平衡会引入误差。<bookmark mark='d'/>对数跳跃会增加修正：对数跳幅平方与对冲支付二乘以e的J次方减一减J不同。其主导差异是三次项，并非大跳跃下精确的三次公式。",

    'f"Now the real strip:':
        "现在看真实的期权串：基准曲面上的三十天比特币期权，每根柱子是它在方差执行价中所占的份额。红色的看跌期权权重最大：K平方分之一在低执行价处最大，"
        "而下方正是微笑最贵的地方。<bookmark mark='a'/>只保留远期附近的执行价，再逐步放宽窗口。在百分之二十以内，执行价读数为{x20:.1f}%；"
        "完整的期权串为{kv:.1f}。{sh:.0f}%的方差位于离远期超过百分之二十的期权里，这就是为什么一个在报价终止处截断的指数读数偏低。"
        "<bookmark mark='b'/>暂停一下，预测：为什么方差执行价{kv:.1f}高于平值波动率{atm:.1f}？因为期权串拥有整条微笑，而两翼比中间更贵。",

    'f"Jumps are where the replication leaks.':
        "跳跃是复制漏水的地方。假设价格以对数计跳一次，幅度为J。方差互换支付J的平方，即绿色曲线。对冲后的期权串支付二乘以e的J次方减一减J，即紫色曲线。"
        "<bookmark mark='a'/>上涨时两者几乎一致。下跌时它们分开：以对数计下跌百分之二十，对冲会少付这次跳跃方差的大约{pct:.0f}%。"
        "卖出方差并用期权对冲的人，做空了崩盘；这也是单只股票的方差互换带有上限的原因之一。"
        "下一章：在真实比特币上运行这个复制。",

    # ------------------------------------------------------------------ Replicate
    "Chapter ten. Replicating a variance swap on real Bitcoin, and the volatility swap.":
        "第10章。在真实比特币上复制方差互换，以及波动率互换。",

    'f"Take {day} as a hypothetical pricing reconstruction. The reference time is eig':
        "以{day}为假设定价重建。参考时间是八点，但拟合曲面汇总标记价格直到中午，因此并不能证明八点可按该价格成交。令利率与成本为零，使用有限的模型期权串，并跟随币安接下来30天的小时路径。<bookmark mark='a'/>紫线是将运行中的现价代入期权串的内在支付，并非剩余期限的市场价值。它与假设的现货对冲之和近似运行中的已实现方差线。<bookmark mark='b'/>最终合计为{tot:.3f}，小时方差为{rvf:.3f}，初始方差执行价折为波动率是{kv:.1f}%。有限执行价、交易场所与参考价差异以及离散收益都会留下误差；这不是德瑞比上的精确自融资成交。",

    "In the House's code, the replication is nine lines:":
        "在我们公司的代码里，复制只有九行：权重、期权串的成本、它在到期时的收益、对冲沿路径的收益，以及用来比较的已实现方差。<bookmark mark='a'/>"
        "在那个月上运行，复制方差和已实现方差在小数点后第三位上一致。",

    'f"Here are {n} overlapping thirty-day windows, beginning every Wednesday. They a':
        "这里有{n}个从每周三开始、相互重叠的30天窗口，并不是独立月份。小时对冲误差的标准差为{sdh:.4f}，平均已实现方差为{mean:.3f}。<bookmark mark='a'/>若每天再平衡，却仍以小时方差为目标，差值的标准差为{sdd:.3f}。即使采样时钟相同，也会有收益高阶项和截断误差，并不能精确复制离散对数收益平方。<bookmark mark='b'/>合成的挂牌式执行价网格使模型方差执行价平均改变{lg:.1f}个波动率点。这是离散与截断比较，而非观察到的可成交合约表现。",

    "The algebra. A contract samples the price n times":
        "代数。合约对价格采样n次，把对数收益的平方加总。<bookmark mark='a'/>对冲赚取的是简单收益；展开对数，复制误差是收益三次方之和。"
        "<bookmark mark='b'/>波动率互换支付已实现方差的平方根。平方根是凹的：展开到二阶。<bookmark mark='c'/>它的公平执行价是方差执行价的平方根，"
        "减去方差的方差除以八倍执行价的二分之三次方。没有任何期权串能交付这个：你需要知道波动率本身会有多波动。",

    'f"Here is Jensen\'s inequality in historical data. Each dot is one overlapping wi':
        "这是历史数据中的詹森不等式。每个点是一段重叠窗口的已实现方差。<bookmark mark='a'/>样本均值的平方根为{a:.1f}%，平方根的均值为{b:.1f}%，相差{gp:.1f}个点。局部二阶近似给出{ap:.1f}，因方差大幅波动而高估。这些是现实样本平均值，并非市场公平执行价。<bookmark mark='b'/>对相同支付期限、在同一风险中性测度下，波动率互换的公平执行价不超过方差互换公平执行价的平方根。只有该测度下已实现方差恒定时才取等号。这个定价不等式并不能将历史均值变成可交易价格。",

    # ------------------------------------------------------------------ VIX
    "Chapter eleven. The VIX, and our own.": "第11章。VIX，以及我们自己的指数。",

    'f"The VIX is a discretized, annualized variance-price measure, quoted as a volat':
        "VIX是一种离散化、年化的方差价格度量，以波动率报价。找到不高于远期的K零点，下方用看跌、上方用看涨，K零点取两者平均，以执行价间距除以执行价平方为权重，再减去规定的修正项。<bookmark mark='a'/>比特币示例将这个公式用于30天两侧可用到期日的模型标记价格，并未复现完整的SPX指数资格与流动性规则。<bookmark mark='b'/>两个到期日的值为{s1:.1f}%与{s2:.1f}%，总方差插值得到{ours:.1f}%。小时DVOL观测为{dv:.1f}%。汇总与时间聚合不同，因此这些不是同步、可成交的指数价格。",

    "On paper: the discretized strip with one correction. <bookmark mark='a'/> The st":
        "写在纸上：离散化的期权串加一个修正。<bookmark mark='a'/>期权串本应在远期处从看跌切换到看涨，但实际在略低的K0处切换；在两者之间，它在本该持有看跌的地方持有看涨，平价关系展开到二阶，给出规定减项的近似依据。这是离散化修正，并非连续期权串的精确恒等式。<bookmark mark='b'/>然后把三十天前后的两个到期日按总方差线性组合。这就是Cboe在2003年9月与高盛共同设计的重建；罗伯特·惠利1993年的原版，平均的是标普100的平值隐含波动率。",

    'f"Compare the fitted proxy with DVOL over {n} Wednesdays. Deribit\'s March 2021 i':
        "在{n}个周三比较拟合代理指标与DVOL。德瑞比于2021年3月推出的指数使用相关的方差期权串方法，并有自己的流动性、Delta与平滑规则。<bookmark mark='a'/>两者相关系数为{c_:.3f}；我们的代理指标平均高出{gm:.1f}个点，样本标准差为{gs:.1f}个点。无报价翼部的模型外推可能起作用，报价筛选、标记价格拟合与不同观测窗口也可能起作用；比较并未识别单一原因。暂停预测：其余正支付期权串不变，删去百分之二十以外的执行价，会去掉正贡献，截断方差估计随之下降。",

    'f"And the VIX itself, back to 1990,':
        "再看VIX本身，回溯到1990年，即Cboe重新计算的历史起点。长期平静，偶有尖峰：1998年、2002年、金融危机，以及有记录以来的最高收盘"
        "{mxv:.2f}，出现在2020年3月16日。<bookmark mark='a'/>最大的单日涨幅并不在其中：它是2018年2月5日，{j1:+.0f}%，即第15章的主题。"
        "<bookmark mark='b'/>下方是VIX除以它的三个月版本。低于1，期限结构向上倾斜：自2007年12月以来{cg:.0f}%的交易日如此。"
        "2018年2月2日这个比率为{r1:.3f}；2月5日为{r2:.3f}。"
        "下一章：VIX比随后实现的波动率高出多少。",
})

ZH.update({
    # ------------------------------------------------------------------ VRP
    "Chapter twelve. The variance risk premium, measured.": "第12章。方差风险溢价的测量。",

    'f"The desk question: why is implied above realized on average?':
        "交易台问题：为什么隐含平均高于已实现？自2021年4月起每个周三，我们的公司从当天早上的曲面上读出三十天方差互换利率，橙色；三十天后测量比特币"
        "实际实现的方差，绿色。<bookmark mark='a'/>看平均值逐渐累积：2021年的牛市、2022年的崩盘、2023年的平静、ETF带来的上涨。<bookmark mark='b'/>"
        "最终：隐含平均{im:.0f}%，已实现{re_:.0f}%。溢价在{sp:.0f}%的周里为正，考虑到相邻三十天窗口四周的重叠后，纽维–韦斯特t统计量为{tt:.1f}。",

    'Why can variance carry a premium? Under a consistent stochastic discount factor ':
        "为什么方差可能具有溢价？在一致的随机贴现因子m与相同期限下，方差的风险中性期望减去现实期望，等于它与m的协方差除以m的均值。<bookmark mark='a'/>这是定价恒等式，并不是报价执行价与某一次未来实现值之间的恒等式。<bookmark mark='b'/>正协方差提供保险解释；单靠样本平均值不能证明它，也不能保证符号普遍为正。<bookmark mark='c'/>重叠窗口使用四阶巴特利特权重的纽维—韦斯特估计。这种有限滞后选择不能消除所有可能的依赖。<bookmark mark='d'/>博勒斯莱夫、陶兴和周研究过股票收益可预测性；我们的比特币比较仍是回顾性的描述。",

    'f"Consider normalized model short-variance payoffs: the fitted variance strike m':
        "考虑归一化的模型卖出方差支付：拟合方差执行价减去随后已实现方差，不含执行与融资成本。<bookmark mark='a'/>最差窗口始于2021年5月12日，以方差单位计的损益为{w:.2f}；最好为{b:.2f}，样本偏度为{sk:.2f}。<bookmark mark='b'/>累计线是相互重叠、每周起始支付的加总，而不是复利账户收益或独立下注序列。阴影回撤相对于该加总序列的运行高点。即使{sp:.0f}%的窗口支付为正，也不能证明是有吸引力且可执行的策略。",

    'f"In this sample the mean fitted variance gap is positive in each calendar year.':
        "在这个样本中，每个日历年的拟合方差差额均值均为正。<bookmark mark='a'/>下一期收益回归将拟合方差执行价减去过去已实现方差作为描述性协变量。曲面汇总记录直到中午，因此并未建立八点可用的可交易信息集。全样本斜率t统计量为{t1:+.2f}，2024至2025年为{t2:+.2f}。这些特定拟合没有提供明确的斜率证据，但不能拒绝零，并不证明不存在可预测性。这不是已注册的策略评估，不声称增加新的试验。博勒斯莱夫、陶兴和周的股票结果使用不同资产、期限与构造。",

    "It is significant, which would be worth a registered test":
        "它是显著的，在任何人据此交易之前，值得做一次登记过的检验。",

    "Nothing: the slope is indistinguishable from zero,":
        "什么也没有：无论全样本还是最近两年，斜率都与零无法区分。不管比特币的方差溢价是在为什么付费，它都预测不了比特币的下一个月。",

    'f"The S&P 500 since 1990:':
        "1990年以来的标普500：VIX为橙色，之后二十一个交易日的已实现波动率为绿色。<bookmark mark='a'/>橙色一直在上方：平均{a:.1f}对{b:.1f}，"
        "VIX的平方在{s:.0f}%的交易日高于已实现方差。例外是那些没有任何指数及时定价的尖峰；最糟的起始日期是2020年2月下旬。<bookmark mark='b'/>"
        "伊恩·迪尤–贝克尔等人发现，溢价集中在最短的期限上。"
        "方差只是期权价格告诉我们的一件事。下一章：它们关于未来还说了什么。",

    # ------------------------------------------------------------------ Moments
    "Chapter thirteen. What option prices say about the future.": "第13章。期权价格对未来说了什么。",

    'f"Change the strip weights to price other payoffs. <bookmark mark=\'a\'/> Equal we':
        "改变期权串权重，就能为其他支付定价。<bookmark mark='a'/>等权重给出简单总收益率的方差，这是马丁SVIX所依据的对象。<bookmark mark='b'/>对三次对数收益支付，期权串使用其二阶导数，正比于六x减三x平方再除以K平方；三次的是支付函数，而不是权重。将对数矩中心化、标准化，得到巴克希、卡帕迪亚和马丹的偏度构造。<bookmark mark='c'/>拟合且截断的30天期权串给出年化对数收益波动率{sq:.1f}%、对数收益偏度{sk:.2f}、峰度{ku:.1f}。这些不同于简单收益方差，尾部估计依赖于观察执行价之外的模型外推。",

    "Carr and Madan's identity gives a flat strip for simple-return variance. <bookma":
        "卡尔—马丹恒等式用等权期权串表示简单收益方差。<bookmark mark='a'/>令R为资产总收益率、m为随机贴现因子，Rf为确定的无风险总收益率。现实预期超额收益等于风险中性方差除以Rf，再减去mR与R的协方差。<bookmark mark='b'/>马丁界限要求该协方差非正。这是实质性条件，不能由一条微笑或历史崩盘中的方差上升来证明。<bookmark mark='c'/>对数收益的幂则给出对数矩的期权串。<bookmark mark='d'/>中心化并标准化，得到偏度与峰度。连续且精确的价格给出不依赖模型的公式；有限报价仍留下尾部与平滑假设。",

    'f"Here are both, every Wednesday since 2021.':
        "这是两者自2021年以来每个周三的数值。上方是偏度，为正时为金色。<bookmark mark='a'/>第1章发现微笑在{cs:.0f}%的周里偏向看涨；"
        "完整的风险中性偏度却只在{pp:.0f}%的周里为正。它们测量的是不同的东西：风险逆转比较平值附近的两个执行价，偏度则衡量整个分布，"
        "即使在平值附近看涨期权受追捧的周，比特币远处的左尾也定价很贵。<bookmark mark='b'/>下方的峰度始终远高于3。本周偏度与下个月收益之间的相关系数为"
        "{cr:.2f}：这是描述，不是策略。",

    'f"What does the conditional bound say? Martin\'s equity application motivates usi':
        "这个有条件界限说明什么？马丁的股票研究提出，在协方差条件成立时，可将期权隐含的简单收益方差用作下界。<bookmark mark='a'/>对比特币期权串，将30天统计量除以其年分数，样本平均为{a:.0f}%，2024至2025年为{b:.0f}%。这是简单年化，不是复利一年收益保证。<bookmark mark='b'/>暂停预测：数值很大是否足以支持买入比特币？不是。本分析并未为比特币建立必要的协方差条件；模型外推与回顾性报价窗口还有额外限制。未验证假设下的下界，不是预测或可执行建议。",

    # ------------------------------------------------------------------ ETP
    "Chapter fourteen. VIX futures, the roll, and short-volatility notes.": "第14章。VIX期货、展期与做空波动率票据。",

    'f"A VIX future settles on a special opening quotation built from the opening pri':
        "VIX期货按选定SPX期权开盘价格构建的特别开盘报价结算，并非普通实时VIX读数。这是2017年6月到2018年3月每一天的整条期货曲线，画成一条带子：横向是日期，向后是距到期的天数，向上是价格，VIX本身是前端的白点。<bookmark mark='a'/>几乎每天曲线都向上倾斜：期货高于现货指数，越远的期货越高。在这些交易日中，第二个月合约有{cg:.0f}%高于第一个月合约，中位数高出{ms:.1f}%。<bookmark mark='b'/>然后是那条红线。2018年2月5日，近月期货从{f0:.2f}涨到{f1:.2f}，曲线翻折过来：现货升水，近端高于远端。",

    'Four lines. In the ideal model with deterministic rates, a volatility future is ':
        "四行公式。在利率确定的理想模型下，波动率期货是结算指数的风险中性期望。詹森不等式以指数平方期望的平方根为上界，而非现实预测。<bookmark mark='a'/>短期期货指数在前两个合格合约之间展期。<bookmark mark='b'/>正向曲线描述今天不同期限的价格，并不保证明天某个合约价格下跌，也不保证空头获利。<bookmark mark='c'/>对无摩擦的每日重置目标，再平衡名义金额等于L平方减L，乘当日指数收益，再乘票据变动前的价值。负一倍和正二倍杠杆下均为二rN。这定义收盘目标敞口调整，而不是每家发行人的真实交易时间表。",

    'f"In the House, the index is a loop over days,':
        "在我们的公司里，指数是一个按日循环，权重从第一个月移向第二个月；票据是一减每日收益的连乘，下限为零。<bookmark mark='a'/>"
        "喂给它Cboe的结算价。2018年2月5日，重建的指数上涨{100 * r5:.1f}%，所以反向票据损失了同样多：几乎全部。",

    'f"Run the historical reconstruction. The hypothetical daily inverse note gained ':
        "运行历史重建。假设的每日反向票据在2017年6月至12月上涨{g17:.0f}%。<bookmark mark='a'/>2月5日下跌{abs(f5):.1f}%。下方柱形表示目标再平衡买入额相对于票据变动前价值的倍数；大柱接近该价值的两倍。示例不包含费用、真实成交、发行人选择与盘中提前终止条款，因此不是对XIV精确合约净值的重建。暂停预测：变动前净值十亿美元、指数上涨百分之十、每日负一倍杠杆，目标敞口调整为两亿美元。这个算术说明潜在需求，并未识别实际市场冲击。",

    # ------------------------------------------------------------------ Volmageddon
    "Chapter fifteen. Volmageddon: the fifth of February, 2018.": "第15章。波动率末日：2018年2月5日。",

    'f"On Monday the fifth of February 2018,':
        "2018年2月5日星期一，在VIX历史上最平静的一年之后，指数一天之内从{b:.2f}升到{a:.2f}，这是有记录以来最大的单日涨幅。当晚，"
        "瑞士信贷发行的XIV崩溃了，这份票据支付短期VIX期货每日变动的反向收益。第二天上午，银行宣布了其募集说明书所称的加速事件："
        "在5日盘中，票据的指示价值跌到了前一收盘价一百零八美元的五分之一或以下。我们用Cboe结算价重建的指数，让一份负一倍票据当天损失{n:.0f}%。",

    'f"The VIX through that year: calm, then the spike. <bookmark mark=\'a\'/> VIX divi':
        "那一年的VIX：先平静，再激增。<bookmark mark='a'/>VIX除以VIX3M从周五的{r1:.3f}升至周一的{r2:.3f}。<bookmark mark='b'/>每日反向与杠杆目标可能要求在上涨后买入波动率期货。若大额订单遇到有限流动性，就可能放大变动。简单的重置算术说明了这种潜在反馈渠道，却不能识别2月崩盘中实际对冲需求的规模或因果占比。发行人可以提前或通过其他工具对冲，真实执行需要单独证据。",

    "The firm files, from the public record.":
        "来自公开记录的机构档案。投资者后来指控，瑞士信贷自己在收盘后的对冲交易推动了XIV的崩溃；2021年第二巡回上诉法院认定这些操纵指控的陈述"
        "足以成立，并将案件发回重审；银行对指控提出了抗辩。这些是指控，不是认定。<bookmark mark='a'/>幸存下来的ProShares SVXY，在2月27日把杠杆降到"
        "负二分之一。<bookmark mark='b'/>约翰·格里芬和阿明·沙姆斯发现，恰恰在VIX结算拍卖时，标普期权的成交量出现尖峰，与试图影响结算的行为一致；"
        "Cboe对他们的结论提出异议。<bookmark mark='c'/>2012年，瑞士信贷曾暂停发行TVIX，此后它的价格大幅偏离其价值。那些年的卖期权基金，LJM和"
        "安联的结构性阿尔法，是第11部分的危机档案。",

    'A daily inverse note can lose its entire value when its index rises enough. Our ':
        "每日反向票据在指数充分上涨时可能损失全部价值。我们的每日收盘示例将净值下限设为零，真实提前终止条款可能在盘中触发。<bookmark mark='a'/>VIX期货展期敞口与方差互换保险属于相关波动率风险，却不是相同交易或支付。2018年的剧烈变动吞没了此前收益。暂停预测：为何目标重置对冲可能集中在收盘附近？每日承诺的收益确定了日末敞口目标，但这不意味着不能提前管理风险，也不能证明所有发行人的交易方式相同。接下来是期权交易商反馈。",

    # ------------------------------------------------------------------ Gamma
    "Chapter sixteen. Dealer gamma, and options that expire the same day.": "第16章。交易商Gamma，以及当日到期的期权。",

    "Dealers hedge the options they sell,":
        "交易商对冲他们卖出的期权，Gamma的符号决定对冲往哪边推。一个模拟的交易日，重复三次，每分钟的消息完全相同。灰色：没有交易商。<bookmark mark='a'/>"
        "绿色：做多Gamma的交易商，上涨时卖、下跌时买；路径更平静。红色：做空Gamma的交易商，因为公众从他们手里买了期权；他们追逐每一次变动，"
        "路径摆动更大。<bookmark mark='b'/>在最后半小时，交易商完成白天推迟的对冲，做空Gamma的路径会沿着原来的方向继续走。",

    "Here is a linear feedback model. Gamma is the position's delta sensitivity per u":
        "这是一个线性反馈模型。Gamma表示持仓Delta对单位价格变动的敏感度。中性化所需的份额交易是负Gamma乘以价格变动；h表示其美元名义金额，因此还要乘S。<bookmark mark='a'/>将lambda定义为每美元交易引起的价格冲击。若全部立即对冲，解不动点后，外部变动被除以一加lambda Gamma S。<bookmark mark='b'/>正Gamma抑制，处于稳定范围的负Gamma放大。奇点是线性示例的极限，并不预测真实价格无限大。<bookmark mark='c'/>模拟将一半对冲推迟，盘中分母为一加二分之一k，收盘收益包含负二分之一k乘此前收益。<bookmark mark='d'/>GEX需要合约规模与假定的交易商方向；未平仓量本身不能识别该方向。",

    'f"Sweep k over two thousand simulated days per value and five seeds. The bands s':
        "对每个k值模拟两千天，使用五个种子。带状区域显示完整的最小至最大范围，而非置信区间。<bookmark mark='a'/>左图比较的是最后半小时之前收益在不同模拟日期之间的标准差，相对于无交易商版本的比值，并非每天分钟收益平方之和。将一半对冲推迟后，k为负二分之一时该标准差为{vs:.2f}倍，正二分之一时为{vl:.2f}倍。<bookmark mark='b'/>空头情形下，收盘收益对先前收益的斜率为{ss:+.2f}。这些关系来自指定模拟，并未识别真实市场中交易商的因果影响。",

    'The public record. Baltussen, Da, Lammers and Martens document intraday momentum':
        "公开记录。巴尔图森、达志、拉默斯和马滕斯在六十多个期货市场记录了日内动量，并发现与对冲反馈相符的证据。<bookmark mark='a'/>Cboe报告，2025年8月当日到期合约占SPX期权成交量的62.4%，并非所有与标普500相关的期权。<bookmark mark='b'/>短期限定价与反馈研究使用不同持仓、流量度量，结论有所不同；庞大的未平仓量本身不能证明交易商产生破坏稳定的需求。<bookmark mark='c'/>研究也在特定样本中记录了散户交易成本与亏损。暂停预测：在本示例假设下，负Gamma放大局部变动，正Gamma抑制变动。真实市场里，单凭符号都不能保证价格钉在某个挂牌执行价。",

    # ------------------------------------------------------------------ Learning
    "Chapter seventeen. Learning surfaces.": "第17章。学习曲面。",

    'f"Can a network find its own coordinates? A variational autoencoder squeezes eac':
        "神经网络能找到自己的坐标吗？变分自编码器把每周的曲面，一百零二个波动率，压缩成两个数再重建。这里它在2021年4月以来的每一周上训练：左边是FTX崩溃的那一周，在每个检查点上的重建；右边是误差，五个种子画成带。<bookmark mark='a'/>起初重建的微笑模糊地贴着平均值；几百步之内它们找到了水平，然后是形状。<bookmark mark='b'/>三千步之后误差为{r0:.1f}个波动率点，五个种子的差别在{max(rs) - min(rs):.2f}以内。样本内基准，同一批网格上的两个主成分，最小化的是标准化对数网格的平方误差，误差为{pc:.1f}。两种方法都在全部这些周上拟合与评估；这是重建比较，而不是预测。",

    'f"Where did each week land in the two-number space?':
        "每一周落在两数空间的什么位置？每个点是一周，按平值波动率从蓝到红着色。<bookmark mark='a'/>颜色沿着一个方向自行排开。网络从未被告知什么是水平，"
        "但它的两个数之一与平值波动率的相关系数为{ca:+.2f}。另一个承载了部分偏斜：{cs:+.2f}。马克西姆·贝热龙、尼古拉斯·冯、约翰·赫尔和"
        "齐西斯·普洛斯在2022年对外汇和股票曲面展示了同样的结果。",

    "Now walk through the space the network learned, decoding":
        "现在在网络学到的空间里漫步，把每个点解码回一张曲面。把水平那个数从负二移到正二，整张曲面升高：平静的市场变成恐慌的市场。<bookmark mark='a'/>"
        "移动另一个数，改变的是形状而不是高度。<bookmark mark='b'/>这些是从未发生、但本可能发生的曲面：风险管理的情景，也是填补缺失报价的平滑方法。"
        "一个提醒：除非教给它，网络对套利一无所知。",

    "The autoencoder maximizes the evidence lower bound:":
        "自编码器最大化证据下界：重建得好，同时让编码接近标准正态。<bookmark mark='a'/>教会它套利是第二个想法。让一个小网络直接表示总方差，"
        "导数由自动微分给出。<bookmark mark='b'/>再把第3章的两个条件作为惩罚项，加在一组完全没有报价的点上：这是阿克雷尔、塔加索夫斯卡和瓦特2020年的做法。",

    'f"Watch it train on the Surface.':
        "看它在基准曲面上训练。百分之八十的报价用于训练，百分之二十留出。左边是它的三十天和九十天微笑与报价的对比，下方是配置点网格，"
        "g为负的地方标红。开始时网格的{100 * g0:.0f}%是红色。<bookmark mark='a'/>微笑向报价弯曲；随着惩罚生效，红点一个个熄灭。"
        "右边是留出报价上的误差，三个种子画成带。",

    'f"The scores. Across three same-date quote splits, the penalized network\'s mean ':
        "成绩。在同一日期的三次报价划分中，带惩罚网络的留出均方根误差平均为{a:.2f}个波动率点，不带惩罚为{b:.2f}，使用相同训练子集的SSVI为{c:.2f}。这是插值检验，不是新日期测试。未惩罚拟合平均有{rgm:.1f}%的审计网格出现负g。带惩罚拟合没有采样负g，但一个运行仍存在日历违反：最差采样占比为{100 * pc.max():.3f}%，现在不再舍入隐藏。即使采样标记全为零，也不能证明全局无套利。<bookmark mark='a'/>vega加权误差分别为网络的{pv:.2f}和SSVI的{sv:.2f}；度量改变时排序可能改变。SSVI具有可解释参数与适用于限定范围的解析充分条件。网络惩罚本身既不保证尾部，也不保证安全外推。",

    "So the penalized network beats SSVI on quotes it never saw.":
        "所以带惩罚的网络在从未见过的报价上胜过了SSVI。",

    "So SSVI holds its own on quotes it never saw.":
        "所以SSVI在从未见过的报价上不落下风。",

    "Weighted by vega, as a desk would weigh them,":
        "像交易台那样按vega加权，网络仍然胜出。",

    "But weight the errors by vega, as a desk would,":
        "但像交易台那样按vega给误差加权，顺序就反过来了：SSVI胜出，因为网络的优势在远处的两翼，那里的期权很便宜。",

    # ------------------------------------------------------------------ Industry
    "Chapter eighteen. Who builds surfaces, and who sells them.": "第18章。谁在构建曲面，谁在出售曲面。",

    "An index is the public face of the surface. Cboe's original VIX used S&P 100 opt":
        "指数是曲面的公开面孔。芝商所原始VIX使用标普100期权，2003年改版采用SPX期权串；2004年推出期货，2006年推出期权。<bookmark mark='a'/>德瑞比于2021年3月推出DVOL，2023年推出其期货。Cboe于2023年推出VIX1D，IBIT期权于2024年11月开始交易。Coinbase于2025年8月14日完成收购德瑞比；其申报文件记录总对价约43亿美元，而早前29亿美元的公告以不同日期估值股票部分。<bookmark mark='b'/>交易所可以发布定义明确的截断指数；要推断连续执行价方差价格，仍需对无报价尾部及目标合约的采样、跳跃与持有成本约定作出假设。",

    "Behind the indices, the field was written by dealers' quants,":
        "在指数背后，这个领域是由交易商的量化研究员写就的，其中很多是公开发表的研究。在高盛的量化策略组：德曼和卡尼的隐含树、德曼的波动率状态，"
        "以及德梅特菲、德曼、卡马尔和邹的方差互换报告，后者成了交易台的手册。<bookmark mark='a'/>在巴黎银行，布鲁诺·杜皮尔的局部波动率。在美林，"
        "SVI，1999年起在内部使用，2004年由盖瑟尔公开。<bookmark mark='b'/>在丹斯克银行，耶斯佩尔·安德烈亚森和布赖恩·胡格的波动率插值，"
        "每个到期日用一步隐式有限差分，从稀疏报价构建无套利曲面，快到能随报价实时运行。<bookmark mark='c'/>银行的曲面构建器做了哪些我们没做的事？"
        "远期中的股息和利率、日内标记、一个模型覆盖多个标的、用于风险的压力曲面，以及给审计留下的每一次拟合记录。",

    "Here is the House's surface builder: SVI and its trader's coordinates; SSVI and ":
        '这就是本行的曲面构建器：SVI与交易员坐标；SSVI及其充分条件的期限范围；采样蝶式与翼部诊断；公式和树形式的局部波动率；用于方差、指数与矩的期权串；期货指数与每日重置票据示例；以及具有网格惩罚并明确报告剩余违反的神经拟合。测试检验这些实现，但不为每个拟合曲面、每个外推执行价或每个未来市场情景背书。最后是研究前沿。',

    # ------------------------------------------------------------------ Frontier
    "Chapter nineteen. The frontier, 2023 to 2026.": "第19章。前沿，2023到2026。",

    "Four lines of current research, each checked against the paper.":
        "四条当前的研究，每一条都对照了论文。鲁本·维德曼、安托万·雅基耶和卢卡斯·戈农，ICLR 2025：算子深度平滑。不像第17章那样每张曲面拟合一个网络，"
        "他们训练一个神经算子，把任意一天的原始报价直接映射成一张光滑曲面，训练数据是十年的标普500日内期权，无套利条件内置于训练之中。<bookmark mark='a'/>"
        "米莲娜·武莱蒂奇和拉马·孔特的VolGAN，把明天的整张曲面与指数一起生成，对情景重新加权使其无套利，并用来检验对冲：这是自编码器漫步的动态版本。"
        "<bookmark mark='b'/>布莱恩·凯利等人把个股的曲面当作图像来读，发现它们能在样本外预测哪些股票会跑赢：这是第27部分的主题。<bookmark mark='c'/>"
        "克劳德·马蒂尼和阿丽安娜·明戈内解决了本部分的两个开放问题：没有蝶式套利的SVI参数的精确集合，以及一个倾斜可随期限变化、整体无套利的SSVI版本。",

    'f"Here is a latent-conditioned regression illustration, rather than a replicatio':
        "这里是潜在坐标条件化的回归示例，并非图神经算子的复现。它输入对数价内程度、期限平方根，以及从该周完整拟合网格得到的两个编码。最终回归器在前百分之八十的周上训练，从{first}起的周被留出。但自编码器使用了所有周，包括这些较晚日期；它们完整的当前网格也用来生成编码。因此这是条件重建检验，而不是完全未见日期的预测。<bookmark mark='a'/>三个种子的回归器误差为{mt:.2f}个波动率点。{d:.2f}的基准是用所有周拟合的两个主成分，并将重建网格的坐标限制在支持范围内；它不是自编码器的解码器。SSVI的{s_:.2f}误差来自对每个测试周自身报价的拟合。方法所依赖的信息不同，并不是公平的预测竞赛。",

    "The network beats the decoder:":
        "网络胜过了解码器：直接读取报价有帮助。",

    "The network does not beat the decoder:":
        "网络没有胜过解码器：限制来自这两个数，而不是网络。",

    "Elsewhere on the frontier:":
        "前沿的其他方向：当日到期期权的曲面，第16章已经见过；用路径依赖和粗糙波动率联合拟合标普500和VIX的微笑，那是第14部分；神经校准器和市场生成器，"
        "那是第17部分。<bookmark mark='a'/>暂停一下，预测：一个曲面生成器每天都通过套利检查器。它是一个好的风险模型吗？不一定。静态无套利对曲面如何移动、"
        "尾部有多大一无所知；第40部分正是在这一点上检验风险模型。",

    # ------------------------------------------------------------------ Outro
    'Part twelve in twelve lines. Smiles contain distributional information, with loc':
        '十二行回顾第12部分。微笑包含分布信息，但存在局部近似与尾部假设。SVI拟合切片，SSVI提供需要核查条件适用域的曲面。局部波动率可以匹配适当扩散的边际分布，却不能确定联合动态。连续对冲的方差恒等式在有限执行价与离散时钟下成为近似。VIX是按规定构建的方差价格指数。历史方差差额是描述性的，回归不能拒绝零不代表证明不可预测。每日重置产品与交易商对冲在指定假设下可能形成反馈。神经重建与采样套利惩罚是实用工具，不是全局保证或完全未见日期的预测。',

    'f"The House\'s twelfth rule.':
        "我们公司的第十二条规则。波动率交易台只从通过套利检查器的拟合曲面上报价，每个奇异期权的价格都要说明它假设了哪种动态，局部、随机还是粗糙，"
        "因为正如第8章所示，同一张曲面可以来自截然不同的未来。<bookmark mark='a'/>这一部分描述市场、为产品定价；它没有登记任何策略，所以试验计数器仍然是{tr}。",

    'Three desk questions. A positive variance-price gap is consistent with insurance':
        "三个交易台问题。贴现因子的相关协方差为正时，正的方差价格差额符合保险解释；样本本身不能证明该机制。<bookmark mark='a'/>在零持有成本与可积性假设下，连续扩散方差由连续执行价期权串和连续现货对冲复制；采样、跳跃、执行价截断与成本会留下修正。<bookmark mark='b'/>在局部短期限偏斜示例中，现价下跌百分之五，粘性执行价下平值波动率约升两个点，粘性价内程度下不变，局部波动率下约升四个点。二倍是近似而非普遍规律。完整解答见讲义。",

    "And nine problems:":
        "还有九道习题：杜皮尔公式、对数合约的期权串、SSVI的两个条件、局部偏斜的二倍关系、马丁的下界、从布莱克公式推出盖瑟尔的g，以及波动率互换的凸性。"
        "其中两道是资格考试题：蝶式估计的偏差与方差，以及相关的价格误差。中英文解答都在笔记中。",

    "Where this comes back.":
        "这些内容会在哪里再次出现。随机波动率和跳跃，在第13部分，修正远期微笑。粗糙波动率，以及标普500和VIX微笑的联合，在第14部分。第15部分的奇异期权"
        "从这张曲面上定价。神经校准器在第17部分回归，期权隐含信号在第27部分，方差溢价作为因子和风险，在第32和40部分。",

    "The textbook chapters this part covers,":
        "本部分涵盖的教科书章节和引用的论文，都列在笔记里。数据包括基准曲面和用Deribit成交重建的两百四十三张周度曲面、币安的比特币价格、Deribit的DVOL、"
        "圣路易斯联储的VIX及其三个月版本、雅虎财经的标普500，以及Cboe的VIX期货结算价。",

    "The volatility desk can now read, fit and trade the surface.":
        "波动率交易台现在能够读懂、拟合并交易这张曲面了。<bookmark mark='a'/>下一部分，第13部分：随机波动率与跳跃。赫斯顿、SABR和贝茨，"
        "校准到基准曲面上，以及为什么它们的微笑像真实的微笑那样移动。",

    # ------------------------------------------------------------------ Research (the PhD layer)
    "For the researcher: Part 9 showed that butterflies":
        "写给研究者：第9部分说明，蝶式价差除以其宽度的平方，收敛到风险中性密度。这个极限假设价格是精确的。真实价格带有误差，而二阶导数会放大它们。这里说明放大多少，以及让两种误差平衡的宽度。",

    "Take the butterfly estimate.":
        "看蝶式估计。<bookmark mark='a'/>三个执行价相隔h的看涨期权价格，每个都带有大小为s的独立误差，以权重一、负二、一组合，再除以h的平方。"
        "<bookmark mark='b'/>把价格做泰勒展开。奇数项相互抵消；由于看涨期权的二阶导数就是密度，剩下的是密度，加上十二分之h平方乘以它的二阶导数。宽的蝶式让密度变模糊。"
        "<bookmark mark='c'/>再看误差：方差中的权重是一、四、一，除以h的四次方。窄的蝶式读到的主要是噪声。",

    "There is a locally preferred width under these assumptions. <bookmark mark='a'/>":
        "在这些假设下，存在一个局部优选宽度。<bookmark mark='a'/>均方误差的主导泰勒近似由随h四次方增长的偏差平方，加上随h负四次方缩小的方差组成。它要求密度足够光滑，局部曲率非零。<bookmark mark='b'/>最小化该近似，得到864乘s平方除以曲率平方的八次方根。对于任意噪声或很宽的蝶式，它不是精确的全局最优值。<bookmark mark='c'/>在这个局部平衡点，两项相等，近似均方根误差按s的平方根缩放。因此将价格误差标准差减半，会使近似均方根误差降低约百分之三十。",

    "f'Simulate it: a lognormal at sixty percent volatility":
        "模拟一下：波动率百分之六十的对数正态，三十天，平值处的蝶式。<bookmark mark='a'/>价格误差为远期价格的千分之二个百分点时，随着蝶式变宽，误差急剧下降，"
        "等偏差占上风后又回升。<bookmark mark='b'/>误差更大时，整条曲线上移，最佳宽度右移。<bookmark mark='c'/>星号标出公式的最佳宽度：价格误差为百分之一个百分点时，"
        "是远期的{r1['h_star']:.1f}%，模拟的最佳值是{r1['h_best_sim']:.1f}%。比这更窄，估计就主要是噪声：在最窄的宽度上，它比要估计的密度本身还大。",

    'f"The numbers. <bookmark mark=\'a\'/> At the two smaller noise levels, the at-the-':
        "看这些数值。<bookmark mark='a'/>在两个较小噪声水平下，平值公式给出约百分之五点四和八点一，接近采样最小值。最大噪声下公式给出百分之十二点一，超出模拟百分之十的上限。报告的采样最小值位于边界，并不能确认公式预测的最优点；看跌翼也有同样限制。<bookmark mark='b'/>这里的相对误差是主导近似公式在其自身最优点的均方根误差。噪声增大五倍，近似值乘以{rs[1] / rs[0]:.2f}，即五的平方根；有限宽度模拟误差未必精确遵循该规律。",

    'f"What scale do real trade--mark differences have? Across the two frozen days, t':
        "真实成交价与标记价差异有多大？两个冻结日期的稳健离散度约为参考标的每一百单位中的{b['noise_sd']:.3f}。<bookmark mark='a'/>它包含价差、模型标记与异质成交，并不能识别独立测量误差的标准差。<bookmark mark='b'/>将该数字代入独立误差的对数正态示例，并使用拟合平值波动率，得到局部宽度{b['h_star']:.1f}%，即两侧各跨越几个挂牌执行价。这是条件敏感性计算，不是实证确定的最优带宽。<bookmark mark='c'/>在相同假设下，相邻执行价噪声的标准差约为参考密度的{100 * sd_adj / q_atm:.0f}%。这是一倍标准差尺度，并非置信上界。平滑方法及其假设会实质影响密度估计。",

    "Three open questions. <bookmark mark='a'/> Non-negativity and normalization rest":
        "三个开放问题。<bookmark mark='a'/>非负性与归一化约束密度估计量；施加形状约束可能有帮助，但不能保证在每种情形下都减小误差。现实相关报价误差下的速率取决于统计模型。<bookmark mark='b'/>蝶式权重之和为零，因此共同的加性价格误差会抵消，执行价的仿射误差也会抵消。一般陈旧误差或远期相关误差未必属于这两种形式。放大效应由相关结构而非单纯的陈旧程度决定。<bookmark mark='c'/>尾部观测稀少、价差较宽，置信带对外推假设尤其敏感。",

    "Pause and predict. A better data feed":
        "暂停预测。一个更好的数据源把价格误差降到十六分之一。最佳蝶式宽度和最佳密度误差各变为原来的多少？",
})

ZH.update({'Under the leading local approximation, width scales with the fourth root of the ': '在主导局部近似下，宽度按误差标准差的四次方根缩放，因此减半。密度均方根误差按其平方根缩放，因此降为四分之一。'})
