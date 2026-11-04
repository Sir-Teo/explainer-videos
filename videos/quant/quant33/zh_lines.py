"""Chinese narration for quant33: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 统计套利 (statistical arbitrage), 配对交易 (pairs trading),
距离法 (the distance rule), 协整 (cointegration), 对冲比率 (hedge ratio), 价差 (spread), 均值回归 (mean reversion),
奥恩斯坦-乌伦贝克过程 (Ornstein-Uhlenbeck process), 半衰期 (half-life), 均衡偏差 (equilibrium deviation), s分数
(s-score), 特征组合 (eigenportfolio), 残差 (residual), 卡尔曼滤波 (Kalman filter), 一步预测误差 (one-step forecast
error), 逆向策略 (contrarian), 领先-滞后 (lead-lag), 交叉自协方差 (cross-autocovariance), 即时性 (immediacy), 拥挤
(crowding), 套利的极限 (limits of arbitrage), 交易区间 (band), 首达时间 (first-passage time), 更新-报酬定理
(renewal-reward theorem), 小成本定律 (the small-cost law)."""

TITLE = '量化金融，从零搭建 · 第33部分：统计套利'

CHAPTERS = {
    'Hook': '橡皮筋上的两个价格',
    'History': '1. 从摩根士丹利的后台到量化公司',
    'Pairs': '2. 距离法配对',
    'Coint': '3. 协整与筛选问题',
    'OU': '4. 奥恩斯坦-乌伦贝克价差',
    'Residuals': '5. 特征组合与残差',
    'Kalman': '6. 会变的对冲比率',
    'LeadLag': '7. 反转与领先-滞后',
    'Deep': '8. 学习残差',
    'Crowding': '9. 流动性、拥挤与衰减',
    'Envelope': '10. 残差组合，登记并打开',
    'House': '11. 第33条规则：统计套利组合',
    'Research': '写给研究者：均值回归价差的最优交易区间',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-three. Statistical arbitrage":
        "第33部分。统计套利：交易那些本应一起变动的价格之间的差距，押注差距会收拢。",

    "Two prices that wander together.":
        "两个一起游走的价格。<bookmark mark='a'/>每一个都像随机游走，所以谁都无法预测。"
        "<bookmark mark='b'/>但它们之间的差距被一根橡皮筋拴着：会拉长，也会弹回。"
        "<bookmark mark='c'/>差距大时，卖出跑在前面的那个，买入落后的那个；差距合上时平仓。市场的方向无关紧要，要紧的只有那根橡皮筋。",

    'f"That is the textbook promise.':
        "这是教科书的承诺。<bookmark mark='a'/>这一部分来检验它。<bookmark mark='b'/>在美国各行业上，经典的配对规则半个世纪里是亏钱的。"
        "某一年通过协整检验的配对约占{100 * fr:.0f}%，只比毫无关联的随机游走的通过率高一倍左右，而且通过一次几乎说明不了下一次能否通过。"
        "<bookmark mark='c'/>留下来的东西更微妙：相对于因子模型的残差，按照为成本选定的区间交易，以及一套关于这个区间应该在哪里的精确理论。",

    "Where this sits. Part thirty-two followed trends":
        "这一部分在系列中的位置。第32部分跟随趋势；这一部分则逆着趋势下注，尺度是几天和单个证券。"
        "它用到第5部分的奥恩斯坦-乌伦贝克过程、第7部分的协整与卡尔曼滤波、第31部分的因子模型和成本，以及2007年8月的拥挤，那场拥挤恰恰始于这类组合。",

    "Edward Thorp's Princeton/Newport Partners traded":
        "Edward Thorp的Princeton/Newport Partners从1969年起做对冲的可转债套利；摩根士丹利的一个小组在1980年代中期交易股票配对；"
        "1988年David Shaw创立了自己的公司，同年文艺复兴的大奖章基金开始运作。"
        "<bookmark mark='a'/>学者们在1990年测量了它所收获的反转，在2006年重跑了配对规则，又在2007年看着它拥挤、崩溃。"
        "<bookmark mark='b'/>现代阶段：因子模型的残差、为奥恩斯坦-乌伦贝克过程推导的最优交易区间、作为收益来源的流动性，以及在残差路径上训练的神经网络。",

    "The plan: the history; pairs by distance":
        "本部分的安排：历史；距离法配对，重跑一遍；协整，以及为什么用它来筛选会误导；奥恩斯坦-乌伦贝克价差及其半衰期；"
        "相对于特征组合的残差；会变的对冲比率；反转与领先-滞后；在残差路径上训练的网络；流动性、拥挤与衰减；在封存年份上打开的残差组合；"
        "以及最优交易区间的一个精确公式。",

    "In the House, the research desk gets":
        "在本系列公司里，研究台得到一族新信号，组合台得到一个风险几乎全是特质风险的组合：正是第31部分的风险模型留下的那些残差。",

    # ------------------------------------------------------------------ History
    "Chapter one. Statistical arbitrage was not invented":
        "第一章。统计套利不是在大学里发明的。它生长于那些计算能力多于用途想法的交易台。",

    "The first firm file is older than the name.":
        "第一份公司档案比这个名字还老。Edward Thorp曾用概率击败二十一点，他与Jay Regan在1969年创立了Princeton/Newport Partners。"
        "他们买入模型认为便宜的可转债和认股权证，同时卖出相应股票，因此市场方向几乎无关紧要。"
        "按Thorp后来的说法，他为其中所含期权建立的模型，与Black和Scholes的公式很接近，而且早于后者发表：第10部分的公式，被当作交易工具使用。",

    "The name came from Morgan Stanley.":
        "这个名字来自摩根士丹利。1980年代中期，先是Gerry Bamberger，然后是Nunzio Tartaglia领导的小组，用计算机寻找价格已经分开的股票配对，"
        "押注它们重聚，而且规模很大。据报道，这个小组1987年赚了约五千万美元，在几个较弱的年份之后于1989年解散。它的成员把这个想法带到了整个华尔街。",

    "One of those alumni was David Shaw":
        "其中一位是David Shaw，来自哥伦比亚大学的计算机科学家，他在1988年创立了自己的公司。"
        "公司起步于股票上的计算机化统计套利：许多小的均值回归赌注，对市场和行业做了对冲，后来成长为最大的系统化投资公司之一。"
        "其设计正是这一部分要构建的：用因子模型去掉共同部分，再押注剩下的部分会回归。",

    "And Renaissance Technologies, founded":
        "还有文艺复兴科技，由数学家James Simons创立。它的大奖章基金始于1988年，据报道其收益远高于任何其他基金，而方法始终保密。"
        "它后来把外部投资者的钱退了回去，主要为自己的员工运作：这是第31部分所说的利润最大化规模，由一家拥有自己策略的公司选定。",

    "Morgan Stanley tried again.":
        "摩根士丹利又试了一次。<bookmark mark='a'/>1993年，Peter Muller在银行内部创立了一个量化小组，即Process Driven Trading；"
        "据报道，它用银行自有资本运作统计套利等策略，并在新规限制银行自营交易之后，于2012年分拆为独立公司。"
        "这段历史里同样的模式反复出现：方法起步于银行内部，最后落脚在独立公司。",

    "What changed. <bookmark mark='a'/> In the beginning":
        "变化在哪里。<bookmark mark='a'/>起初，只有少数交易台有计算机，价差很宽，竞争者行动迟缓：持有几周的配对能赚到很高的收益。"
        "<bookmark mark='b'/>后来价格改为十进制，市场电子化，许多公司运行同样的模型：持有期缩短到几天、几小时，每笔交易的优势也随之缩小。"
        "<bookmark mark='c'/>今天，这份收益主要是提供流动性的报酬，归于交易成本最低的人。",

    "Pause and predict. A strategy's edge is three basis points":
        "暂停并预测。一个策略每笔交易的优势是三个基点，每个头寸每天交易。当价差从十个基点降到两个基点时会怎样？为什么它仍可能变得更糟？",

    # ------------------------------------------------------------------ Pairs
    "Chapter two. In 2006 Evan Gatev":
        "第二章。2006年，Evan Gatev、William Goetzmann和Geert Rouwenhorst把交易台一直在用的规则写了下来，并在四十年的美国股票上做了检验。",

    "The rule has no model at all.":
        "这条规则根本没有模型。<bookmark mark='a'/>把每个资产的总收益指数归一化为一。"
        "<bookmark mark='b'/>在一年里，计算每一对路径之间的距离，保留最接近的二十对。"
        "<bookmark mark='c'/>在接下来的六个月里，当一对的差距超过其形成期标准差的两倍时，卖出高的、买入低的，在两条路径相交时平仓。"
        "<bookmark mark='d'/>这些都是原论文的选择，这里在历史完整的行业上原样重跑。",

    "The paper that made the rule famous.":
        "让这条规则出名的论文。<bookmark mark='a'/>Evan Gatev、William Goetzmann和Geert Rouwenhorst在1962年到2002年的美国股票上运行它。"
        "据报道，最好的二十对平均年化超额收益最高达到百分之十一。即使等一天再交易，从而去掉买卖价差反弹，利润依然存在，并且超过了他们的成本估计。"
        "但在后来的年份里利润较低，本系列公司马上会看到这种下降还在继续。",

    "One pair, the closest at the start":
        "一对配对，在2008年下半年开始时最接近的一对：电信业和商业服务业。<bookmark mark='a'/>在形成期的一年里，它们几乎同步变动。"
        "<bookmark mark='b'/>在交易窗口里，随着危机对两者的冲击不同，差距在一个月内就突破了区间，用了大约三个月才合上，然后又朝另一个方向张开。"
        "平静时期接近的一对，在危机里不一定接近。",

    'f"The result, decade by decade.':
        "结果，按十年来看。<bookmark mark='a'/>在1960和70年代，这条规则稳定地亏钱；在90年代和2010年代，它赚了一点。"
        "<bookmark mark='b'/>整个时期，扣除成本前的夏普比率是{a['sharpe']:.2f}，年收益{100 * a['mean']:+.1f}%。在行业上，最简单的配对规则不起作用。",

    "Why not? <bookmark mark='a'/> Whole industries carry momentum":
        "为什么不行？<bookmark mark='a'/>整个行业带有动量，Tobias Moskowitz和Mark Grinblatt发现了这一点：两个行业分开，往往是趋势的开始，而不是噪声在回归。"
        "<bookmark mark='b'/>股票不一样。在一个行业内部，股票的特质差距才是会回归的东西，原论文在1962年到2002年的股票上发现，扣除成本前每年最高可达百分之十一。"
        "<bookmark mark='c'/>而且这条规则没有模型：它从不问两条路径为什么一起变动，所以分不清暂时的差距和永久的断裂。",

    "And the literature agrees.":
        "文献也同意。<bookmark mark='a'/>Binh Do和Robert Faff发现，这条规则在股票上的收益在1980年代之后稳定下降，剩下的大部分是在动荡市场中赚到的。"
        "<bookmark mark='b'/>成本让情况更糟：每一次往返都要在两条腿上交易四次。"
        "<bookmark mark='c'/>没有理由的规则最先衰减。接下来的几章补上这个理由：一个关于价差为什么应该回归的模型。",

    "A backtest on portfolios hides the short leg.":
        "在组合上的回测掩盖了空头那条腿。在股票上它是真实的。<bookmark mark='a'/>借入股票来卖出要付费，通常很少，但难借的股票每年要付几十个百分点，"
        "而一对配对里贵的那只股票，往往正是别人都想做空的那只。"
        "<bookmark mark='b'/>出借人可以随时召回股票，Joseph Engelberg、Adam Reed和Matthew Ringgenberg表明，费用上升和被召回的风险本身就会阻止套利。"
        "<bookmark mark='c'/>规则也会改变：2008年9月，美国证券交易委员会暂时禁止做空数百只金融股。空头腿拿不住的配对，就不是配对。",

    "Pause and predict. A pair's gap reverts with a half-life":
        "暂停并预测。一对配对的差距以二十天的半衰期回归，你最多只能持有六个月。两倍标准差的触发线是太宽、太窄，还是差不多？",

    # ------------------------------------------------------------------ Coint
    "Chapter three. Part seven introduced cointegration":
        "第三章。第7部分介绍了协整：两条游走的序列，有一个不游走的组合。它是配对的正确模型。用它去寻找配对则是另一回事。",

    "The definition. <bookmark mark='a'/> Each log price has a unit root":
        "定义。<bookmark mark='a'/>每个对数价格都有单位根：它会游走。"
        "<bookmark mark='b'/>但某个组合，一个价格减去贝塔乘以另一个价格，是平稳的：这就是价差，贝塔就是对冲比率。"
        "<bookmark mark='c'/>格兰杰表示定理说，这时至少有一个价格会移动去合上差距。这种修正就是经济内容：有某种东西，套利者或者共同的原因，把这一对拉回到一起。",

    "The Engle-Granger test, from Part seven.":
        "第7部分的恩格尔-格兰杰检验。<bookmark mark='a'/>把一个对数价格对另一个做回归。<bookmark mark='b'/>检验残差是否有单位根。"
        "<bookmark mark='c'/>临界值是负三点三四，而不是负二：回归选择的对冲比率会让残差看起来尽可能平稳，所以检验必须要求更多。",

    'f"Now screen the industries, one year at a time.':
        "现在逐年筛选这些行业。<bookmark mark='a'/>在典型的一年里，约{avg:.0f}%的行业配对通过检验。"
        "<bookmark mark='b'/>对毫无共同之处的独立随机游走配对做同样的检验，有{fp:.1f}%通过：这是检验本身的假阳性率。"
        "所以行业的通过率大约是纯噪声的两倍。有些联系是真实的，但筛选在任何一年里找到的大多数配对都是偶然的。",

    'f"The harder test: does a pair that passes this year':
        "更难的检验：今年通过的配对，明年还能通过吗？<bookmark mark='a'/>在某一年通过的配对中，有{100 * c['persist']:.1f}%在下一年再次通过。"
        "<bookmark mark='b'/>对随机选的配对，这个比率是{100 * avg:.1f}%。通过一次，几乎不能证明会再次通过。用这个检验来挑选配对的筛选，挑选的主要是噪声。",

    'f"And the half-lives of the pairs that passed.':
        "再看通过的配对的半衰期。<bookmark mark='a'/>对每个价差拟合一个自回归；半衰期是对数二除以其系数对数的负值。"
        "<bookmark mark='b'/>中位数约为{c['half_life_median']:.0f}个交易日：回归很快，但这是在挑出这一对的同一年里测量的。"
        "一对配对之所以被选中，是因为它的价差恰好在那个样本里回归得快，所以测得的半衰期偏短。又是选择效应。",

    "Beyond pairs: baskets.":
        "配对之外：篮子。<bookmark mark='a'/>对多个价格，把它们的变化写成误差修正模型：每个价格的移动，部分是对系统偏离长期联系的程度作出的反应。"
        "<bookmark mark='b'/>这种反应的矩阵可以分解为速度和协整组合；它的秩就是独立价差的个数。"
        "<bookmark mark='c'/>Soren Johansen的检验从特征值读出这个秩，对整个篮子只做一次似然比检验。"
        "<bookmark mark='d'/>但筛选问题只会更大：一个资产范围的每个子集都是候选篮子，每检验一个篮子就是一次试验。",

    "The purest pair there is.":
        "最纯粹的配对。<bookmark mark='a'/>荷兰皇家石油和壳牌是两只上市股票，按六比四对同一个集团的现金流拥有固定的索取权。它们的价格本应完全绑定。"
        "<bookmark mark='b'/>Kenneth Froot和Emil Dabora发现，两者长期偏离平价，有时超过百分之十，而且每只股票都随自己的本土市场变动。"
        "<bookmark mark='c'/>据报道，长期资本管理公司在1998年倒下时就持有这笔交易。直到2005年两家公司合并，这个差距才彻底合上。即使有合同，价差也不会按你的时间表回归。",

    "The screening problem, and three answers.":
        "筛选问题，以及三种答案。<bookmark mark='a'/>有一千对，或者五百只股票之间的十二万五千对，任何检验都会有成千上万对偶然通过：第26部分的计数器同样适用于配对。"
        "<bookmark mark='b'/>有理由的配对，同一种产品、同一条供应链、同一家公司的两类股票，留存得好得多。"
        "<bookmark mark='c'/>或者干脆跳过配对：用因子模型去掉所有资产共有的部分，让每个资产的残差自己回归。",

    "Pause and predict. You test two thousand unrelated pairs":
        "暂停并预测。你在百分之五的水平上检验两千对互不相关的配对，保留通过的那些。大约有多少对？其中有多少明年还能再次通过？",

    # ------------------------------------------------------------------ OU
    "Chapter four. A spread that reverts needs a model":
        "第四章。会回归的价差需要一个描述它如何回归的模型。最简单、也是业界在用的，是第5部分的奥恩斯坦-乌伦贝克过程。",

    "The model. <bookmark mark='a'/> The spread is pulled toward its mean theta":
        "模型。<bookmark mark='a'/>价差以速度kappa被拉向均值theta，同时受到噪声的扰动。"
        "<bookmark mark='b'/>它在未来任何时刻的分布都是精确已知的：期望差距按指数衰减，方差稳定在sigma平方除以二倍kappa。"
        "<bookmark mark='c'/>对交易者来说，两个数描述一个价差：均衡标准差，决定赌注的大小；半衰期，决定赌注持续多久。",

    "Estimation is a regression.":
        "估计就是一个回归。<bookmark mark='a'/>按日抽样时，奥恩斯坦-乌伦贝克过程恰好是一阶自回归。"
        "<bookmark mark='b'/>它的斜率是e的负kappa次方，截距和噪声给出theta和均衡价差。"
        "<bookmark mark='c'/>所以本系列公司用价差自身的历史做最小二乘拟合，从斜率读出半衰期。",

    'f"A simulated spread with a half-life of ten days.':
        "一个半衰期为十天的模拟价差。<bookmark mark='a'/>它经常穿过均值，很少长时间远离。"
        "<bookmark mark='b'/>虚线是一又四分之一个均衡偏差，Avellaneda和Lee在那里开仓。用这三百天拟合，半衰期是{f['half_life']:.1f}天。长样本上，很接近。接下来看短样本。",

    'f"On a short one, the estimate is biased.':
        "在短样本上，估计是有偏的。<bookmark mark='a'/>自回归斜率在短样本里被向下拉，幅度约为一加三倍b除以样本长度：肯德尔偏差，与第6部分预测回归背后的偏差相同。"
        "<bookmark mark='b'/>模拟一个十天半衰期：用三十天估计，中位数是{out[30][0]:.1f}；用六十天，{out[60][0]:.1f}；用一年，{out[250][0]:.1f}。"
        "<bookmark mark='c'/>而一个保留看起来最快的价差的筛选，保留的正是偏差最大的估计。价差看起来比实际更快。",

    'f"How well sixty days pin down a speed.':
        "六十天能把速度定得多准。<bookmark mark='a'/>自回归斜率为零点九时，半衰期是{b9[1]:.1f}天，但上下两个标准误的范围，快的一端是{b9[2]:.1f}天，"
        "慢的一端到达斜率为一：完全不回归。<bookmark mark='b'/>价差越慢，范围越宽。s分数每天都用这个估计：一组s分数，就是一组非常不确定的速度。"
        "这正是研究章节的交易区间取决于价差的宽度、而不取决于其速度的原因之一。",

    "Where should the bands be?":
        "交易区间应该在哪里？<bookmark mark='a'/>William Bertram以闭式算出了奥恩斯坦-乌伦贝克价差上一笔交易的期望时长，以及使单位时间收益最大的区间。"
        "<bookmark mark='b'/>Tim Leung和Xin Li把进场和出场当作最优停时问题，考虑成本和止损。"
        "<bookmark mark='c'/>研究章节从首达时间出发证明了自己的一个版本，发现最优区间若以均衡偏差衡量，只取决于成本。",

    "The trading signal is the s-score.":
        "交易信号是s分数。<bookmark mark='a'/>价差离其拟合均值的距离，以均衡偏差为单位。"
        "<bookmark mark='b'/>Marco Avellaneda和Jeong-Hyun Lee在一又四分之一处开仓，在均值附近平仓，这些阈值是他们在美国股票上选出来的。"
        "<bookmark mark='c'/>而且他们只交易拟合半衰期短到足以估计的价差。为什么是这些阈值而不是别的，是研究章节的问题。",

    "Pause and predict. A spread's daily autoregressive slope":
        "暂停并预测。一个价差的日度自回归斜率是零点九五。它的半衰期是多少？用六十天的样本，平均会估计成多少？",

    # ------------------------------------------------------------------ Residuals
    "Chapter five. In 2010 Marco Avellaneda":
        "第五章。2010年，Marco Avellaneda和Jeong-Hyun Lee用更好的东西取代了配对：每个资产对一篮子因子，于是回归的是资产自己的残差。",

    "The idea. <bookmark mark='a'/> Write each asset's return":
        "思路。<bookmark mark='a'/>把每个资产的收益写成对少数几个共同因子的暴露，加上一个残差：这是第31部分的风险模型，只是因子取自数据。"
        "<bookmark mark='b'/>把残差累加起来：这就是去掉了市场、行业和风格之后的资产价格。"
        "<bookmark mark='c'/>把它当作奥恩斯坦-乌伦贝克价差，交易它的s分数。每个资产都和整个市场构成一对，完全不需要筛选配对。",

    "The factors are eigenportfolios.":
        "因子是特征组合。<bookmark mark='a'/>取过去一年日收益的相关矩阵及其特征向量，又是第30部分的谱。"
        "<bookmark mark='b'/>按每个特征向量投资，并按每个资产的波动率缩放。"
        "<bookmark mark='c'/>第一个特征组合是市场；接下来几个是行业和风格。在四十九个行业上，本系列公司保留五个，每月重新估计。",

    "The trade. <bookmark mark='a'/> Each day, regress each industry":
        "交易。<bookmark mark='a'/>每天，用过去六十天把每个行业对五个因子收益做回归。"
        "<bookmark mark='b'/>买入一个残差，意味着买入这个行业并卖出它的因子对冲，所以头寸没有市场、行业或风格暴露。"
        "<bookmark mark='c'/>组合只赚它的因子模型解释不了的部分，这正是第31部分的风险模型所说的特质风险。",

    "Avellaneda and Lee's own refinements.":
        "Avellaneda和Lee自己的改进。<bookmark mark='a'/>用多少个因子？他们用了十五个特征组合，或者用能解释百分之五十五方差所需的个数，也试过用行业基金作因子；"
        "第30部分的谱保留噪声边缘之上的特征值。"
        "<bookmark mark='b'/>他们按残差自身的漂移调整s分数，这样一个正在走趋势的残差就不会被误认为被拉伸的残差。"
        "<bookmark mark='c'/>他们还用成交量而不是天数来度量时间，据他们报告，这让残差回归得更干净。",

    'f"Avellaneda and Lee\'s rule on the industries':
        "Avellaneda和Lee的规则用在行业上，用他们的阈值。<bookmark mark='a'/>扣除成本前，残差会回归：按总头寸计每年{100 * ga['mean']:.1f}%，夏普比率{ga['sharpe']:.2f}。"
        "<bookmark mark='b'/>每边五个基点，行业和它的对冲都要付，扣除之后是{100 * na['mean']:+.1f}%，夏普比率{na['sharpe']:.2f}。"
        "回归是真实的；但在这样的成本下，它不足以付清自己的成本。",

    'f"Eight variations: three or five factors':
        "八个变体：三个或五个因子，三十天或六十天的窗口，以及两种开仓区间。<bookmark mark='a'/>扣除成本前，每一个都会回归。"
        "<bookmark mark='b'/>扣除成本后，每一个都亏钱，排名跟着换手率走：交易最少的规则亏得最少。"
        "扣除成本前最好的规则，夏普比率{bg:.2f}，扣除成本后亏损，为{bn:.2f}，因为它每天交易其组合的{bt:.0f}%。"
        "<bookmark mark='c'/>第九条规则用研究章节的公式、按每个行业自身对冲的成本来设定区间，并且只在残差穿过均值时平仓。"
        "它每天交易{100 * th['turnover']:.0f}%，是唯一留下一些东西的规则：扣除成本后的夏普比率{th['sharpe']:.2f}。它是在那八条失败之后才加上的，所以本系列公司登记它时，要按全部九次试验计。",

    'f"All nine rules on one picture.':
        "九条规则画在一张图上。<bookmark mark='a'/>扣除成本前，它们挤在一起，夏普比率都在{gm:.1f}左右。"
        "<bookmark mark='b'/>扣除成本后，它们沿着换手率落在一条直线上：日换手率每多十个百分点，夏普比率约减少{abs(10 * b1):.2f}。"
        "因子和窗口的选择只把一条规则上下挪一点；交易多少决定它在直线上的位置，而这决定了正负号。",

    'f"By era, for the registered rule.':
        "按时代来看登记的规则。<bookmark mark='a'/>扣除成本前，夏普比率分别是{g0:.2f}、{g1:.2f}和{g2:.2f}：1990年代最强，2003年到2010年最弱，之后部分回升。"
        "<bookmark mark='b'/>扣除成本后，分别是{n0:.2f}、{n1:.2f}和{n2:.2f}。几乎所有的净利润都是在第一个时代赚到的。同样的成本，对强的溢价是一笔小税，对弱的溢价则会把它抹掉。",

    "Why costs bite so hard here.":
        "为什么成本在这里咬得这么狠。<bookmark mark='a'/>每一笔残差交易都是两笔交易：资产本身，以及分散在许多其他资产上的因子对冲。"
        "<bookmark mark='b'/>一个行业已经平均掉了其中股票自身的大部分反转；单只股票回归得更多，交易成本也更高。"
        "<bookmark mark='c'/>交易台会在头寸之间轧差对冲，用期货交易因子那条腿，并按自己实际支付的成本来选择区间。",

    "One more reason the costs here are pessimistic.":
        "这里的成本偏悲观，还有一个原因。<bookmark mark='a'/>每个头寸都带着自己的因子对冲。"
        "<bookmark mark='b'/>但分别交易每个对冲，成本至少和交易它们的总和一样高，通常高得多，因为多头和空头的对冲会相互抵消。"
        "<bookmark mark='c'/>真实的交易台为整个组合只持有一个净对冲。这一部分对每个头寸的对冲分别收费，这是保守的选择，把轧差留作下一次登记。",

    "Pause and predict. A residual book earns a gross Sharpe ratio":
        "暂停并预测。一个残差组合扣除成本前的夏普比率是零点八，波动率百分之四，每天换手其总头寸的百分之二十。两条腿每边五个基点，还剩下什么？",

    # ------------------------------------------------------------------ Kalman
    "Chapter six. Cointegration assumes one fixed hedge ratio.":
        "第六章。协整假设一个固定的对冲比率。真实的关系会漂移。第7部分的卡尔曼滤波让对冲比率可以变动，而这样做也设下了一个陷阱。",

    "The model. <bookmark mark='a'/> One log price is an intercept":
        "模型。<bookmark mark='a'/>一个对数价格等于截距加上对冲比率乘以另一个对数价格，再加噪声。"
        "<bookmark mark='b'/>但截距和对冲比率本身是随机游走：一个由滤波器追踪的状态。"
        "<bookmark mark='c'/>只有一个选择要紧：状态噪声与观测噪声之比，它决定对冲比率能变得多快。",

    "The filter, from Part seven.":
        "第7部分的滤波器。<bookmark mark='a'/>每天，对系数的不确定性都会增长。<bookmark mark='b'/>增益决定相信今天的意外有多少。"
        "<bookmark mark='c'/>系数向今天的观测移动。<bookmark mark='d'/>而你能交易的价差用的是昨天的系数：它是滤波器的一步预测误差。记住这个说法。",

    'f"Bitcoin and ether, 2018 to 2020':
        "比特币和以太坊，2018年到2020年：两个有明显共同驱动的价格。<bookmark mark='a'/>用全部三年做一次回归，对冲比率是{k['beta_static']:.2f}。"
        "<bookmark mark='b'/>六十天滚动回归剧烈摆动，从接近零到接近三。<bookmark mark='c'/>卡尔曼滤波给出一个平滑、缓慢变化的比率，大约在三分之二和一之间。哪个价差才是该交易的？",

    'f"Test the two spreads.':
        "检验这两个价差。<bookmark mark='a'/>用固定比率，价差不协整，迪基-富勒统计量为{k['adf_static']:.2f}，半衰期约{k['hl_static']:.0f}天：慢得没法交易。"
        "<bookmark mark='b'/>用卡尔曼比率，统计量为{k['adf_kalman']:.1f}，压倒性地平稳，半衰期{k['hl_kalman']:.1f}天。它看起来像一对完美的配对。",

    "What the speed setting means.":
        "速度设定意味着什么。<bookmark mark='a'/>在稳态下，当信噪比很小时，滤波器的增益稳定在信噪比的平方根附近。"
        "<bookmark mark='b'/>所以这个滤波器是一个指数加权回归，以其增益的速率遗忘过去。"
        "<bookmark mark='c'/>万分之一的比率相当于约一百天的窗口；百分之一，约十天。在十天的窗口下，对冲比率变得足够快，能把价差吞掉，陷阱就合上了。",

    "It is a trap.":
        "这是一个陷阱。<bookmark mark='a'/>卡尔曼价差是滤波器的预测误差。"
        "<bookmark mark='b'/>好的滤波器的预测误差接近白噪声，所以它们当然会检验为平稳，半衰期约一天。"
        "<bookmark mark='c'/>价差看起来会回归，是因为对冲比率在移动以吸收每一个差距，而不是因为价格收敛。"
        "押注它，就是押注滤波器会自我修正，而它修正的方式是改变比率，不是移动价格。",

    "So: <bookmark mark='a'/> use the filter to size the hedge":
        "所以：<bookmark mark='a'/>用滤波器来确定对冲规模，而不是用它证明存在配对。"
        "<bookmark mark='b'/>在样本外检验价差，看它的利润，而不是它的平稳性。"
        "<bookmark mark='c'/>速度要选得慢：快的滤波器会制造回归，而每一次对速度的选择都是一次试验。",

    "Pause and predict. A filter's one-step forecast errors":
        "暂停并预测。一个滤波器的一步预测误差的自回归斜率是零点三。这一对是协整的吗？",

    # ------------------------------------------------------------------ LeadLag
    "Chapter seven. Every stat-arb book is, underneath, a contrarian":
        "第七章。每个统计套利组合，骨子里都是逆向策略：相对于某个参照，它买入下跌的，卖出上涨的。1990年，Andrew Lo和Craig MacKinlay问：这样的逆向策略到底是因为什么而获得报酬？",

    "The contrarian, in its purest form.":
        "最纯粹形式的逆向策略。<bookmark mark='a'/>按每个资产上一期的相对变动反向加权。<bookmark mark='b'/>它的利润是权重乘以本期收益之和。"
        "<bookmark mark='c'/>Bruce Lehmann在1990年发现，在股票中，上周的输家胜过上周的赢家。自然的解读是过度反应：价格冲过头再回来。Lo和MacKinlay表明这不是唯一的解读。",

    "Their decomposition is exact.":
        "他们的分解是精确的。<bookmark mark='a'/>逆向策略的期望利润是收益自协方差矩阵中的三项。"
        "<bookmark mark='b'/>第一项是自身反转：资产反转自己的变动。那是过度反应。"
        "<bookmark mark='c'/>第二项是交叉自协方差：一个资产的变动预测另一个资产的下一次变动。这同样向逆向策略付钱，完全不需要过度反应，只需要传播得慢的消息。"
        "<bookmark mark='d'/>第三项是成本：平均收益的离散程度。",

    'f"Lead-lag, measured on Kenneth French\'s size deciles':
        "领先-滞后，在Kenneth French的规模十分位组合上按周测量，从1963年开始。<bookmark mark='a'/>最大股票上周的收益预测最小股票本周的收益，相关系数{ld['large_to_small']:+.2f}。反过来是{ld['small_to_large']:+.2f}。"
        "<bookmark mark='b'/>小盘股也预测它们自己，{ld['small_own']:+.2f}：它们调整得慢，这是正的自相关，与过度反应相反。大盘股领先，小盘股跟随。",

    "The decomposition, computed.":
        "分解，算出来。<bookmark mark='a'/>对规模十分位组合，自身自相关让逆向策略亏钱，因为小盘股是延续而不是反转，而领先-滞后几乎恰好补回同样多：合计接近零。"
        "对行业，领先-滞后项更大，合计略为正。<bookmark mark='b'/>在两种情况下，恒等式都精确到最后一位：分解与实现的利润是同一个数。",

    "And the pattern did not last.":
        "而这个模式没有持续。<bookmark mark='a'/>1990年以前，小盘股强烈地跟随大盘股：自身延续大，领先-滞后也大。"
        "<bookmark mark='b'/>1991年以来，两项都缩小并改变了符号：小股票现在略有反转，也不再滞后。"
        "更快的市场、更便宜的交易，以及许多恰好在交易这种滞后的套利者，把它消除了。一个统计套利的利润来源，被测量出来，然后消失了。",

    "Two warnings about measured reversal.":
        "关于测得的反转，两个警告。<bookmark mark='a'/>Richard Roll的模型：成交随机地落在买价或卖价上，围绕着有效价格。"
        "<bookmark mark='b'/>所以即使有效价格是随机游走，记录下来的价格变化也是负自相关的。这种反转无法交易：它就是买卖价差本身。Bruce Lehmann在股票上的周度逆向利润，部分就是这个。"
        "<bookmark mark='c'/>而交易得晚的股票会把昨天的消息带进今天的收盘价，让领先-滞后出现在没人能据此行动的地方。组合和残差能减弱这两种效应，但不能消除它们。",

    "Why the unit and the horizon matter.":
        "为什么单位和期限很重要。<bookmark mark='a'/>在几天到一个月的尺度上，单只股票会反转：Narasimhan Jegadeesh和Bruce Lehmann。"
        "<bookmark mark='b'/>在三到十二个月的尺度上，行业会延续：Tobias Moskowitz和Mark Grinblatt发现了行业动量，并发现它解释了股票动量的很大部分。这就是第九章的行业逆向策略亏钱的原因。"
        "<bookmark mark='c'/>在三到五年的尺度上，两者又都反转，即Werner De Bondt和Richard Thaler的长期反转。回归是关于某个单位和某个期限的陈述，从来不是关于一般价格的陈述。",

    "What this means for a stat-arb book.":
        "这对统计套利组合意味着什么。<bookmark mark='a'/>逆向策略由两种不同的东西付钱，过度反应和传播缓慢的消息，风险也不同。"
        "<bookmark mark='b'/>因子模型去掉共同部分，也去掉了大部分领先-滞后；剩下的是每个资产自身的反转。"
        "<bookmark mark='c'/>领先-滞后在消息先到达一个市场、再到达另一个市场的地方存活：一只股票和它的供应商，一个指数和它的期货，一种币在两个交易所。",

    "Pause and predict. Every asset on its own follows a random walk":
        "暂停并预测。每个资产单独看都是随机游走，但大盘股的收益预测小盘股一周后的收益。逆向策略是赚钱还是亏钱？",

    # ------------------------------------------------------------------ Deep
    "Chapter eight. The s-score reads one number":
        "第八章。s分数从残差的路径中只读出一个数：它离均值有多远。网络可以读出整条路径的形状。它能找到更多吗？",

    "The claim. <bookmark mark='a'/> In 2021 Jorge Guijarro-Ordonez":
        "论断。<bookmark mark='a'/>2021年，Jorge Guijarro-Ordonez、Markus Pelger和Greg Zanotti把Avellaneda-Lee的流程拿来，每一步都改为学习得到。"
        "<bookmark mark='b'/>一个卷积变换器读取每个残差最近三十天的路径。<bookmark mark='c'/>配置直接按组合的夏普比率最大化来训练。"
        "他们报告在美国大盘股上有很高的样本外夏普比率，扣除交易成本后仍然盈利，来源是奥恩斯坦-乌伦贝克模型无法表达的趋势与回归模式。",

    "The machine-learning literature on stat arb, briefly.":
        "统计套利的机器学习文献，简要说。<bookmark mark='a'/>Christopher Krauss、Xuan Anh Do和Nicolas Huck在标普五百成分股的滞后收益上训练了深度网络、提升树和随机森林；"
        "据报道，他们的集成模型扣除成本前每天赚四十五个基点以上，扣除成本后少得多，而且在后来的年份里更少。"
        "<bookmark mark='b'/>深度统计套利那篇论文学习了整个流程，并报告对成本稳健。<bookmark mark='c'/>共同的线索：数千只单个股票，从多天数据中同时读出的信号，以及随时间的衰减。",

    "The House's version, smaller and honest.":
        "本系列公司的版本，更小也更诚实。<bookmark mark='a'/>输入是每个行业最近三十天的累计残差，从今天量起，以其自身波动率为单位。"
        "<bookmark mark='b'/>目标是明天的残差收益。<bookmark mark='c'/>训练到2012年，在2013到2016年上提前停止，在2017到2020年上测试，这几年没有被任何选择碰过。",

    "The network is Part twenty-seven's small ensemble":
        "这个网络是第27部分的小型集成：三十个输入，两个分别有三十二和十六个单元的隐藏层，三个随机种子平均，轻微的惩罚，以及提前停止。"
        "<bookmark mark='a'/>它比变换器小得多，但可以学到s分数忽略的任何路径形状：刚刚掉头的残差，仍在下跌的残差，冲过头的残差。",

    'f"On the test years.':
        "在测试年份上。<bookmark mark='a'/>网络的预测与明天残差之间的相关系数是{ic:.4f}：几乎为零。"
        "<bookmark mark='b'/>它的预测与s分数的原材料，即残差在一个月里移动了多远，几乎无关：相关系数{cr:.2f}。"
        "<bookmark mark='c'/>而昨天的残差变动本身什么也预测不了。日复一日可学的东西这么少，一个灵活的模型学到的大多是噪声。",

    'f"The test. <bookmark mark=\'a\'/> On the same days':
        "检验。<bookmark mark='a'/>在同样的日子里，普通的s分数规则扣除成本前的夏普比率是{s0:.2f}。"
        "<bookmark mark='b'/>网络扣除成本前是{s1:.2f}。<bookmark mark='c'/>扣除成本后，{s2:.1f}：因为它每天都按预测重新调仓，每天交易其组合的{tv:.0f}%，并为此付出代价。",

    "Why it fails here, and why that is not a verdict":
        "为什么它在这里失败，以及为什么这不是对那篇论文的判决。<bookmark mark='a'/>资产范围不对：四十九个行业几乎没有可预测的残差；那篇论文用的是数百只单个股票。"
        "<bookmark mark='b'/>目标不对：每天调仓的预测忽略了成本，而那篇论文按扣除成本后的夏普比率训练配置，所以它的网络学会少交易。"
        "<bookmark mark='c'/>而一个接近零的日度信号需要多年的数据才能与噪声区分开，每试一种结构就是又一次试验。",

    "The lessons. <bookmark mark='a'/> Flexibility pays only":
        "教训。<bookmark mark='a'/>只有当存在可发现的结构、有足够的数据，并且损失函数知道成本时，灵活性才有回报。"
        "<bookmark mark='b'/>在弱信号上，s分数的强先验，即残差会回归，浪费的数据更少。"
        "<bookmark mark='c'/>这场比较是公平的：同样的残差、同样的日子、同样的成本。这个网络不予登记。",

    "Pause and predict. A forecast has a daily information coefficient":
        "暂停并预测。一个预测在四十九个资产上的日度信息系数是零点零一。大约需要多少年的日度数据，才能让它的信息系数距零两个标准误？",

    # ------------------------------------------------------------------ Crowding
    "Chapter nine. A reversal strategy buys":
        "第九章。反转策略从急于卖出的人那里买入。它的收益就是这份急切的价格。这个想法解释了它何时赚钱、何时崩溃，以及为什么会衰减。",

    "The theory. <bookmark mark='a'/> Sanford Grossman and Merton Miller":
        "理论。<bookmark mark='a'/>Sanford Grossman和Merton Miller：必须现在交易的投资者接受更差的价格，站在另一边的人在价格恢复时获得报酬。反转就是即时性的价格。"
        "<bookmark mark='b'/>在危机中，流动性提供者自己的资本稀缺。"
        "<bookmark mark='c'/>所以反转的期望收益应该随市场压力上升。Stefan Nagel在美国股票上正好发现了这一点：反转收益随VIX上升，并在2008年达到顶峰。",

    'f"The House tests it on its own universe.':
        "本系列公司在自己的资产范围上检验它。<bookmark mark='a'/>把行业逆向策略的月度收益对一个月前的VIX做回归。"
        "<bookmark mark='b'/>斜率与零无法区分，t统计量为{n['t']:.2f}。<bookmark mark='c'/>而且行业逆向策略平均是亏钱的，夏普比率{n['sharpe']:.2f}。"
        "行业不是出售即时性的地方：它们是数百只股票的组合，急于卖出者造成的价格压力在其中被冲淡了。",

    'f"Month by month.':
        "逐月来看。<bookmark mark='a'/>对行业逆向策略，最平静的五分之一月份和压力最大的五分之一月份看起来一样：每月分别为{100 * n['low']:+.2f}%和{100 * n['high']:+.2f}%。"
        "<bookmark mark='b'/>教训关乎资产范围，而不是理论：流动性溢价存在于急于卖出会推动价格的地方，在单只股票、小盘股，以及因子模型的残差里。",

    "Why a reversal can widen before it closes.":
        "为什么一个反转在合上之前会先扩大。<bookmark mark='a'/>Andrei Shleifer和Robert Vishny：套利者管理的是别人的钱，投资者按近期收益评判他们。"
        "<bookmark mark='b'/>价差扩大会让套利者损失资本，投资者撤资，被迫的卖出又让价差进一步扩大。"
        "<bookmark mark='c'/>所以最好的交易恰恰在套利者资本最少的时候到来。套利的极限是资本的极限，而不是想法的极限。",

    "Who demands immediacy, concretely?":
        "具体是谁在要求即时性？<bookmark mark='a'/>一只股票被纳入指数时的指数基金：它们必须在同一天买入，Andrei Shleifer发现纳入会推高价格。"
        "<bookmark mark='b'/>遭遇资金流出的共同基金：Joshua Coval和Erik Stafford表明，它们的被迫卖出把价格压到价值以下，价格在随后几个月恢复。"
        "<bookmark mark='c'/>还有应付追加保证金或按日历再平衡的基金。每一个都是在意日期而不是价格的卖家，统计套利交易者因站在另一边而获得报酬。",

    "Crowding is the other face of liquidity.":
        "拥挤是流动性的另一面。<bookmark mark='a'/>2007年8月，第31部分讲过：随着一群人平掉同样的头寸，市场中性的统计套利组合在三天里损失惨重，然后反弹。"
        "<bookmark mark='b'/>统计套利特别容易拥挤，因为同样的数据和同样的因子模型会把不同的公司引向同样的残差交易。"
        "<bookmark mark='c'/>而反弹又是那个理论：被迫卖出就是不计价格地要求即时性，能撑住的人拿到了十年来最大的反转溢价。",

    "And decay. <bookmark mark='a'/> Avellaneda and Lee found":
        "还有衰减。<bookmark mark='a'/>Avellaneda和Lee发现，他们的残差策略在美国股票上的收益在2000年代初之后下降了，就像距离法在1980年代之后那样。"
        "<bookmark mark='b'/>交易一种反转的公司越多，它就被收割得越快，优势转移到更短的期限，然后进入做市，那是第38部分的主题。"
        "<bookmark mark='c'/>剩下的是每笔交易几个基点，归于执行成本最低的公司。",

    "Pause and predict. A reversal strategy earns two basis points":
        "暂停并预测。一个反转策略扣除成本前每天赚两个基点，每天交易其组合的百分之四十，每边成本五个基点。扣除成本后它赚多少？",

    # ------------------------------------------------------------------ Envelope
    "Chapter ten. One residual book, registered":
        "第十章。一个残差组合，在打开信封之前登记，并在扣除成本后，在2021年到2025年上只评判一次。",

    'f"The registration. <bookmark mark=\'a\'/> Five eigenportfolios':
        "登记。<bookmark mark='a'/>五个特征组合，六十天的残差，按每个行业自身成本设定的研究章节区间，在均值处出场。成本在两条腿上都收取，记入损益之内。"
        "<bookmark mark='b'/>它按{e['n_trials']}次试验计：失败的八个变体，加上它自己。计数器变为{n_now:,}。",

    'f"The envelope. <bookmark mark=\'a\'/> Five sealed years':
        "信封。<bookmark mark='a'/>残差组合封存的五年，扣除成本后。"
        "<bookmark mark='b'/>按总头寸计，它每年赚{100 * h['mean']:.1f}%，波动率{100 * h['vol']:.1f}%，最大回撤从未超过{abs(100 * h['maxdd']):.1f}%。一份小而稳定的市场中性收益：行业上的统计套利能有的就是这个量级。",

    'f"The numbers. <bookmark mark=\'a\'/> Before costs, the residuals reverted':
        "数字。<bookmark mark='a'/>扣除成本前，残差在封存年份上的回归与研究年份完全一样：夏普比率{hg:.2f}，对比{e['res_gross']['sharpe']:.2f}。溢价没有衰减。"
        "<bookmark mark='b'/>扣除成本后，{hn:.2f}，比研究年份略好。用月度收益计，标准误是{se:.2f}：为正，但与零无法区分。五年不足以证明三分之一的夏普比率。",

    'f"Year by year.':
        "逐年来看。<bookmark mark='a'/>五年中有{npos}年为正。最好的是{best}年，{vb:+.1f}%，它贡献了大部分；最差的是{worst}年，{vw:+.1f}%。"
        "<bookmark mark='b'/>没有哪一年是灾难。而2022年，股票和债券一起下跌的那一年，对残差来说是正收益的一年：这个组合没有可以亏掉的市场暴露。",

    'f"How much the verdict depends on the cost.':
        "结论有多依赖成本。<bookmark mark='a'/>同样的毛收益和换手率，按每边零到十个基点的每一种成本收费。"
        "<bookmark mark='b'/>组合在研究年份上约在{b0:.1f}个基点盈亏平衡，在封存年份上约在{b1:.1f}个基点。本系列公司假设的是五个。"
        "在四个基点时组合明显为正；在八个基点时亏钱。整个这一部分的结论就落在执行成本的几个基点之内，这就是第37部分要测量它的原因。",

    'f"Why the envelope was needed.':
        "为什么需要信封。<bookmark mark='a'/>第26部分：N条毫无价值的规则中最好的一条，其期望夏普比率是可预测的若干个标准误。"
        "<bookmark mark='b'/>九次试验时，这道门槛是{bar:.2f}。<bookmark mark='c'/>研究年份扣除成本后的夏普比率是{rs:.2f}，而这道门槛是{bar:.2f}："
        "单凭回测，本系列公司无法把这条规则与九条中最幸运的那条区分开。只有封存年份能做到，而五年还不足以确定。",

    'f"How to read it.':
        "怎么解读。<bookmark mark='a'/>扣除成本前，回归是真实而稳定的：没有衰减。"
        "<bookmark mark='b'/>扣除成本后，交易拿走了其中约{share:.0f}%。<bookmark mark='c'/>而唯一让组合转为正的杠杆是区间：交易得更少，阈值从成本推导出来。它比因子个数或窗口长度更重要。",

    "What would improve it, each a new registration.":
        "什么能改进它，每一项都是一次新的登记。<bookmark mark='a'/>更多资产、更便宜的腿：把对冲作为一个期货头寸来交易。"
        "<bookmark mark='b'/>在头寸之间轧差对冲，只为组合的净交易付费。<bookmark mark='c'/>测量成本，而不是假设成本，那是第37部分。",

    "Pause and predict. A book's true Sharpe ratio is point three.":
        "暂停并预测。一个组合的真实夏普比率是零点三。需要多少年的收益，它的估计值才能距零两个标准误？",

    # ------------------------------------------------------------------ House
    "Chapter eleven. The House's thirty-third rule":
        "第十一章。本系列公司的第33条规则：一个回归策略在本系列公司交易它之前必须展示什么。回归在扣除成本前容易找到，扣除成本后难以保住，"
        "所以这条规则主要关乎成本，以及找到这条规则所用的试验次数。",

    "The first sheet. <bookmark mark='a'/> Distance pairs on industries lost money.":
        "第一张汇总表。<bookmark mark='a'/>行业上的距离法配对亏钱。协整检验通过的配对大约是偶然的两倍，而一年后几乎没有再次通过的。"
        "卡尔曼价差看起来完美，却只是预测误差。组合之间的反转来自交叉项，而不是来自每个组合自身的过去。"
        "残差组合扣除成本前强烈回归，用标准区间扣除成本后亏损；研究章节的区间留下了一点。网络几乎什么也没学到。流动性的故事在行业上没有显现。"
        "而登记组合的封存年份是倒数第二行。",

    "Chapter four's fit in twelve lines.":
        "第四章的拟合，十二行代码。把明天的价差对今天的做回归；如果斜率不在零和一之间，价差就不是均值回归的，函数会如实说明，而不是编造一个速度。"
        "否则，速度是斜率对数的负值，均值是截距除以一减斜率，均衡偏差来自残差。s分数除以的正是最后这个数。",

    "The research chapter's theorem, as code.":
        "研究章节的定理，写成代码。利润率等于区间减去往返成本，再除以一个周期的期望长度：从区间回到均值的时间，加上从均值出发到达区间的时间。"
        "每一个都是由迪金公式得到的二重积分，用辛普森法则计算。四行代码，本系列公司交易的区间就来自它们。",

    "And Chapter seven's decomposition.":
        "还有第七章的分解。逆向策略的期望利润精确地分为：每个资产自身自协方差的负值，加上一个资产的过去预测另一个资产未来的交叉项，再加上平均收益的离散度。"
        "函数返回全部三项以及实际赚到的利润，所以每次运行都会检查这个恒等式。",

    "And the s-score itself.":
        "还有s分数本身。每天，对累计残差最近的六十个值拟合奥恩斯坦-乌伦贝克过程；如果拟合是均值回归的，分数就是今天离拟合均值的距离，以均衡偏差为单位，拟合出的速度也一并保留。"
        "不回归的残差根本得不到分数，也不会被交易。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>价差；配对；分解；定理；以及它的模拟检验。"
        "<bookmark mark='b'/>还有第33条规则。一个回归策略要进入本系列公司，必须展示：扣除每条腿的成本之后的利润，对冲也算在内；从这些成本推导出的区间，而不是凭习惯；"
        "挑选它时用过的每一个配对、窗口和区间，都计为试验；在样本外用利润而不是平稳性检验它的价差；并说明它的拥挤风险：还有谁持有同样的残差。",

    "Before it is traded, three practical limits.":
        "交易之前，有三个实际的限制。<bookmark mark='a'/>容量：残差组合自己的交易会推动它想便宜买入的价格，第31部分的平方根定律使每一美元的成本随规模增长。"
        "<bookmark mark='b'/>杠杆：一个波动率百分之三的组合必须加好几倍杠杆才值得运作，所以像2007年8月那样的一周会变成追加保证金。"
        "<bookmark mark='c'/>所以本系列公司按检验过的规模持有登记组合，只有在测得的成本显示有余地时才让它增长。",

    "And how the desk watches it.":
        "以及交易台如何监控它。<bookmark mark='a'/>每天：换手率对照其预算，实际支付的成本对照假设的五个基点，以及组合的因子暴露，它们应该为零。"
        "<bookmark mark='b'/>每周：残差的离散度，以及仍能拟合均值回归模型的比例；比例下降意味着因子模型已经不再描述市场。"
        "<bookmark mark='c'/>还有事先写好的止损：一周亏损超过三倍日波动率就把组合减半，现在就决定，而不是等到八月让拥挤的人群替它决定。",

    "The rule against three cases.":
        "用这条规则检验三个案例。<bookmark mark='a'/>一只展示夏普比率为三的配对基金：问这是不是扣除成本前的，筛选了多少对，对冲比率是否在同样的日子上拟合。"
        "<bookmark mark='b'/>一个半衰期为一天的篮子：问它的价差是不是滤波器的预测误差。"
        "<bookmark mark='c'/>一个在2007年8月亏损的残差组合：问还有谁持有同样的残差，以及这只基金能否撑过一周。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Every stat-arb book chooses bands":
        "写给研究者。每个统计套利组合都要选择交易区间，通常凭习惯：一又四分之一个偏差，或者两个。本章精确推导区间规则的利润率，以及使它最大的区间。",

    "The setup. <bookmark mark='a'/> An Ornstein-Uhlenbeck spread":
        "设定。<bookmark mark='a'/>一个奥恩斯坦-乌伦贝克价差，从其均值量起。"
        "<bookmark mark='b'/>规则在均值处等待；当价差到达距离为m的区间时，无论哪一侧，它押一个单位赌回归，并在价差回到均值时平仓。"
        "<bookmark mark='c'/>每次往返赚m，付成本c。宽区间每次赚得多但交易少；窄区间交易频繁但赚得少。问题在于速率。",

    "Lemma one, the renewal-reward theorem.":
        "引理一，更新-报酬定理。<bookmark mark='a'/>每个周期有两段：在均值处等待价差到达区间，然后持有直到它回来。由强马尔可夫性，每个周期都在均值处重新开始，所以各周期独立同分布。"
        "<bookmark mark='b'/>于是长期单位时间利润等于每个周期的期望报酬除以一个周期的期望长度。<bookmark mark='c'/>所以一切归结为两个期望首达时间。",

    "Lemma two, the first-passage times.":
        "引理二，首达时间。<bookmark mark='a'/>令f(x)为从x出发到达边界的期望时间。"
        "<bookmark mark='b'/>由迪金公式，奥恩斯坦-乌伦贝克生成元作用在f上等于负一，且f在边界上为零：这是第8部分的费曼-卡茨，每单位时间的运行成本为一。"
        "<bookmark mark='c'/>乘以积分因子，左边就成为一个精确的导数。方程积分两次即可。",

    "The two solutions.":
        "两个解。<bookmark mark='a'/>从负m到均值，远处的条件是斜率保持有界，这使内层积分从负无穷开始。"
        "<bookmark mark='b'/>从均值到任一侧的区间，对称性使均值处的斜率为零，这使内层积分从零开始。"
        "<bookmark mark='c'/>内层积分是误差函数，外层积分是一维数值积分。",

    "The theorem. <bookmark mark='a'/> The profit rate is the band minus the cost":
        "定理。<bookmark mark='a'/>利润率等于区间减去成本，除以两个期望首达时间之和。以均衡偏差度量空间，以一除以kappa为单位度量时间，问题就变成无量纲的。"
        "<bookmark mark='b'/>所以最优区间以均衡偏差计，只取决于以同样单位计的成本：一条普适曲线。回归速度缩放利润，但不移动区间。"
        "而在没有成本时，速率趋于一个有限的极限：sigma乘以根号下kappa除以pi。",

    "The two times. <bookmark mark='a'/> Holding":
        "两个时间。<bookmark mark='a'/>持有时间，从区间回到均值，随区间缓慢增长：离得越远，拉回的力越强。"
        "<bookmark mark='b'/>等待时间，从均值到区间，从零开始并爆炸式增长，因为逆着拉力到达远处的区间是罕见的。宽区间的代价是等待。",

    'f"The profit rate, for three costs.':
        "三种成本下的利润率。<bookmark mark='a'/>每条曲线从成本处的零开始上升，达到峰值，然后随着等待时间占据主导而下降。"
        "<bookmark mark='b'/>圆点是最优点：成本越高，最优区间越往外推。成本为十分之三个偏差时，最优区间是{b3['m']:.2f}个偏差：接近Avellaneda和Lee的一又四分之一，后者大约对应半个偏差的成本。",

    "And the universal curve.":
        "以及普适曲线。<bookmark mark='a'/>对每一个奥恩斯坦-乌伦贝克价差，无论速度如何，以偏差计的最优区间都是以偏差计的成本的这个函数。"
        "<bookmark mark='b'/>在成本接近零时它上升得很陡，大致像成本的立方根，与第31部分的不交易区间是同一个定律：小成本会把区间移动很多。一又四分之一的习惯只对一种成本是对的。",

    'f"A corollary that surprises people.':
        "一个让人意外的推论。<bookmark mark='a'/>对很小的区间，持有时间与区间成线性，等待时间则是二次的。"
        "<bookmark mark='b'/>所以在没有成本时，利润率趋于一个有限的极限，sigma乘以根号下kappa除以pi，而不是无穷大：无限频繁地交易并不能无限快地赚钱。"
        "<bookmark mark='c'/>以曲线的单位，是根号下二除以pi，即{t['frictionless']:.3f}。成本决定最优区间必须从这个极限退后多远。",

    "And the cube root can be made exact.":
        "而立方根可以做到精确。<bookmark mark='a'/>把两个首达时间对小区间展开，以均衡偏差为单位。回到均值的时间有一个负的二次项。"
        "<bookmark mark='b'/>到达区间的时间恰好有一个相反的二次项。在一个周期的长度里，它们相互抵消。"
        "<bookmark mark='c'/>所以线性项之后的第一个修正是三次的，令利润率的导数为零，得到：区间的立方等于成本的三倍。"
        "<bookmark mark='d'/>这就是小成本定律。最优区间是三倍成本的立方根，以均衡偏差计，没有自由常数，也与速度无关。而因成本损失的无摩擦利润比例，按成本的三分之二次方增长。",

    'f"Checked against the exact optimum.':
        "与精确最优值对照。<bookmark mark='a'/>成本为百分之一个偏差时，这个定律与精确区间相差在{e1:.1f}%以内；成本为{r3['c']:g}个偏差时，已经是很大的成本，相差仍在{e3:.0f}%以内。"
        "<bookmark mark='b'/>它与第31部分的不交易区间是同一个立方根，但原因不同：那里成本是与二次风险权衡，这里是与一个周期所需的时间权衡。",

    'f"A worked example.':
        "一个算例。<bookmark mark='a'/>一个宽百分之二的残差，半衰期八天，两条腿的往返成本二十个基点：成本是十分之一个偏差。"
        "<bookmark mark='b'/>最优区间是{mb:.2f}%，即{ms:.2f}个偏差，小成本定律给出{law:.2f}。"
        "<bookmark mark='c'/>一个周期大约需要{cyc:.0f}天，规则每持有一个单位每天赚{ra:.1f}个基点。Avellaneda和Lee一又四分之一个偏差的习惯，会宽出将近一倍。",

    "Checked by simulation, at half the optimal band":
        "用模拟来检验，在最优区间的一半、最优区间、以及它的一点五倍处，对三种成本。"
        "<bookmark mark='a'/>在细网格上，模拟的速率比定理低几个百分点，因为离散监测的路径会稍晚才被发现穿过区间。"
        "<bookmark mark='b'/>把两种网格大小外推到连续监测，每一行都回到定理的几个百分点以内，而且在每种情况下，最优点都是三者中最好的。",

    'f"And on data: the industries\' residuals of Chapter five.':
        "再看数据：第五章的行业残差。<bookmark mark='a'/>Avellaneda和Lee的固定区间扣除成本前的夏普比率是{al['gross']['sharpe']:.2f}，扣除成本后是{al['sharpe']:.2f}。"
        "<bookmark mark='b'/>定理的区间，按每个残差自身的成本从普适曲线读出，扣除成本前赚{th['gross']['sharpe']:.2f}，扣除成本后{th['sharpe']:.2f}，"
        "每天交易组合的{100 * th['turnover']:.0f}%，对比{100 * al['turnover']:.0f}%。理论告诉交易台，按它自己的成本，区间应该在哪里；残差究竟会不会回归，是数据的问题，第十章打开了它。",

    "Where the theorem sits.":
        "这个定理的位置。<bookmark mark='a'/>William Bertram对一个进场水平和一个出场水平使用了同样的更新论证，首达时间取自这个过程已知的级数。"
        "<bookmark mark='b'/>Tim Leung和Xin Li把进场和出场当作带贴现和止损的最优停时问题，答案是一对自由边界，而不是固定的周期。"
        "<bookmark mark='c'/>而第31部分的不交易区间，成本与二次风险的权衡，以同样的立方根增长：两个不同的问题，一个指数。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>区间取决于被估计的参数，带有肯德尔偏差；参数不确定下的最优区间，以及边交易边学习，都没有闭式解。"
        "<bookmark mark='b'/>联系会断裂的价差不是奥恩斯坦-乌伦贝克过程；同时检测断裂并交易区间，是开放问题。"
        "<bookmark mark='c'/>而一个由相关残差组成的完整组合，带有风险预算和平方根冲击，是一个多维的自由边界问题。",

    "Pause and predict. Two spreads have the same equilibrium deviation":
        "暂停并预测。两个价差有相同的均衡偏差和相同的成本，但其中一个回归速度快一倍。它们的最优区间和利润率如何比较？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-three in fourteen lines.":
        "第33部分，十四行。统计套利起步于1980年代摩根士丹利的一个配对交易台，后来成为量化公司的核心业务。行业上的距离法配对已经不赚钱。"
        "协整检验找到的配对大约是偶然的两倍，而几乎没有能通过两次的。奥恩斯坦-乌伦贝克价差从一个回归中给出速度、均值和宽度。"
        "相对于特征组合的残差在扣除成本前强烈回归。会变的对冲比率可以制造回归。逆向利润分为自身反转与领先-滞后。",

    "A network on residual paths learned almost nothing":
        "在残差路径上训练的网络几乎什么也没学到，它的交易又耗掉了其余的部分。流动性溢价在行业上没有显现，但拥挤在2007年显现了。"
        "研究章节的区间是唯一在扣除成本后保住利润的规则，在封存年份上它仍为正，扣除成本前的回归没有变化。而定理为每个价差给出一条曲线，小成本时遵循立方根定律。",

    "Six desk questions.":
        "六个交易台问题。两个价格是协整的：你交易什么，可能出什么错？交易价差；会出错的是联系本身、估计和筛选。"
        "<bookmark mark='a'/>什么是s分数？残差离其拟合均值的距离，以均衡偏差为单位。<bookmark mark='b'/>半衰期为一天的卡尔曼价差是配对吗？凭这个证据不是。",

    "Where does a contrarian's profit come from?":
        "逆向策略的利润从哪里来？自身反转与领先-滞后。<bookmark mark='a'/>为什么用标准区间的残差组合会亏钱？每笔交易都是两笔交易。"
        "<bookmark mark='b'/>区间应该如何依赖成本？通过一条曲线，在零附近是立方根。完整解答在讲义里。",

    "The pause questions, answered.":
        "暂停题的答案。更便宜的交易会让每个人都能交易它，从而缩小优势。<bookmark mark='a'/>两倍偏差的触发线适合二十天的半衰期和六个月的期限。"
        "<bookmark mark='b'/>两千对不相关的配对中，大约一百对通过，其中大约五对再次通过。",

    'f"A slope of point nine five is a half-life':
        "斜率零点九五对应{hl:.1f}天的半衰期，但六十天的数据通常会说大约{hlk:.0f}天。<bookmark mark='a'/>残差组合什么也留不下：扣除成本后每年{net6:.1f}%。"
        "<bookmark mark='b'/>而滤波器的预测误差说明的是滤波器有多好，而不是价格是否被绑在一起。",

    'f"When large caps lead small caps':
        "当大盘股领先小盘股时，逆向策略单靠交叉项就能赚钱。<bookmark mark='a'/>百分之一的信息系数需要大约{yrs_ic:.0f}年才能证明；零点三的夏普比率，大约{yrs_sr:.0f}年。"
        "<bookmark mark='b'/>两个基点的毛收益、百分之四十的换手率，什么也剩不下。<bookmark mark='c'/>速度快一倍，意味着同样的区间和两倍的利润。",

    "And twelve problems: a spread's speed":
        "还有十二道习题：价差的速度；筛选中的假通过；从曲线读出区间；扣除成本后的残差组合；逆向策略的交叉项；滤波器的误差；扣除成本后的反转；"
        "信息系数和夏普比率需要多久才能证明；以及小成本定律。然后是两道资格考试题：由迪金公式推导定理，以及无摩擦极限与立方根定律。中英文解答都在讲义里。",

    "Where this comes back. Part thirty-four goes inside":
        "这些内容会在哪里再次出现。第34部分走进运作统计套利组合的公司内部。第37部分测量一笔交易的真实成本，整个这一部分都依赖这个数。"
        "第38部分是做市，最短期限上的回归。终章会对每一行做紧缩检验。",

    "The textbooks this part follows":
        "这一部分所依据的教科书，以及它引用的论文，从1987年恩格尔和格兰杰的协整，到2021年的深度统计套利。"
        "屏幕上的每个数字都由本系列公司的代码，用Kenneth French的组合、Binance的K线和Cboe的VIX算出，示意图都已标明。",

    "The House now runs a residual book":
        "本系列公司现在运作一个残差组合：市场中性、小、稳定，几乎完全是对自己交易成本的押注。它知道回归容易找到、保住却很昂贵，而决定是哪一种的是区间，不是模型。"
        "<bookmark mark='a'/>下一部分，第34部分：走进量化公司。运作这些组合的公司如何组织、如何付酬、如何治理，以及为什么决定它们规模的是容量，而不是聪明。",

}
