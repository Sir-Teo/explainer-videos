"""Chinese narration for quant24: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 因子 (factor), 多空组合 (long-short portfolio), 规模
(size), 价值 (value), 动量 (momentum), 盈利能力 (profitability), 投资 (investment), 账面市值比 (book-to-market), 2 x 3排序
(2 x 3 sort), GRS检验 (GRS test), Fama–MacBeth回归 (Fama-MacBeth regression), 张成检验 (spanning test), 时间序列动量
(time-series momentum), 动量崩盘 (momentum crash), 波动率缩放 (volatility scaling), 押注低贝塔 (betting against beta),
质量减垃圾 (quality minus junk), 套息 (carry), 价值价差 (value spread), 重估 (revaluation), 绿色溢价 (greenium), 因子
择时 (factor timing), 因子动量 (factor momentum), 壳价值 (shell value), 换手率因子 (turnover factor), 业绩记录 (Track
Record), 试验计数器 (trial counter)."""

TITLE = '量化金融，从零搭建 · 第24部分：因子'

CHAPTERS = {
    'Hook': '六美元',
    'Tests': '1. 检验因子模型：GRS与Fama–MacBeth',
    'SizeValue': '2. 规模、价值与三因子',
    'Momentum': '3. 动量：跨股票与跨时间',
    'Crash': '4. 动量崩盘',
    'Profit': '5. 盈利能力、投资、五因子与q',
    'LowRisk': '6. 低风险',
    'Everywhere': '7. 处处可见的价值与动量；套息；质量',
    'ValueDecade': '8. 价值失去的十年',
    'Green': '9. 绿色收益',
    'Timing': '10. 因子择时与因子动量',
    'China': '11. 中国的因子',
    'Firms': '12. 因子行业',
    'Track': '13. 业绩记录开启',
    'House': '14. 第24条规则：因子库',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part twenty-four. Factors:":
        "第24部分。因子：半个世纪以来解释了股票收益大部分的那几个组合，以及House第一批在从未见过的数据上打分的策略。",

    'f"Six dollars, put to work in July 1963.':
        "六美元，1963年7月开始投入。一美元投入扣除国库券后的股票市场，五美元投入多空组合，各自买入一类股票、卖出另一类。<bookmark mark='a'/>"
        "市场把它的一美元变成了约{r['series']['MKT'][-1]:.0f}美元。小盘对大盘、价值对成长、盈利强对盈利弱、投资保守对投资激进：各自变成四五美元。"
        "<bookmark mark='b'/>而动量，去年的赢家对去年的输家，变成了{r['series']['UMD'][-1]:.0f}美元，而且根本没有净投入资金。这些就是经典因子。"
        "本部分要问：每一个是什么、如何被发现、为什么可能有回报，以及它是否仍然有效。",

    'f"And then there are the months when a factor breaks.':
        "然后，还有因子崩溃的那些月份。2009年3月，市场从低点回升。在危机中跌得最深的股票，银行和周期股，恰恰是动量策略做空的那些，而它们涨得最快。"
        "<bookmark mark='a'/>三个月里动量亏损约百分之{abs(100 * w['cum_umd']):.0f}，而市场上涨了百分之{100 * w['cum_mkt']:.0f}。十年的收益，"
        "一个春天就没了。第四章会把这次崩盘拆开来看。",

    "What is a factor? In this part, a portfolio.":
        "什么是因子？在本部分里，它是一个组合。按某个特征给股票排序，小盘、便宜或上涨，买入具备这个特征的，卖出不具备的。因子的收益就是两者之间的价差，"
        "一种建仓不花钱的超额收益。<bookmark mark='a'/>因子模型于是提出一个很强的主张：少数几个这样的价差就能为一切定价。每个组合的预期超额收益，"
        "都等于它在这些因子上的贝塔乘以因子的平均收益。这就是第二十三部分的套利定价理论，只是因子终于有了名字。",

    "How the factors were found.":
        "因子是怎样被发现的。在1970年代和1980年代初，它们是作为对CAPM的检验出现的：Fischer Black、Michael Jensen和Myron Scholes发现证券市场线太平，"
        "Sanjoy Basu发现便宜的股票跑赢了它们的贝塔，Rolf Banz发现小盘股也是如此。<bookmark mark='a'/>Eugene Fama和Kenneth French在1992和1993年"
        "把规模和价值合成三因子模型；Narasimhan Jegadeesh和Sheridan Titman记录了动量；Mark Carhart把它加了进去。<bookmark mark='b'/>然后是第二波："
        "动量的崩盘、时间序列动量、所有市场中的价值与动量、押注低贝塔、五因子与q因子、中国自己的模型，以及价值最糟糕的十年。",

    "The plan: how to test a factor model":
        "本部分安排：如何检验因子模型，以及检验每个模型所用的二十五个组合；规模、价值和动量，以及动量的崩盘；盈利能力、投资和低风险；"
        "所有市场中的价值与动量，以及套息；用数字衡量价值失去的十年；绿色收益、因子择时和中国；出售因子的公司；最后，业绩记录开启。",

    "In the House, the research desk builds its first library":
        "在House里，研究交易台建立了它的第一个库：因子，每一个都附有它的历史、它的崩盘和它的理由。本部分的每个结果都来自截止到2020年12月的数据，"
        "直到最后几章，此后封存的年份才第一次被打开。",

    # ------------------------------------------------------------------ Tests
    "Chapter one. Before any factor, the tests":
        "第一章。在讲任何因子之前，先讲每个因子模型都必须通过的检验，以及检验它所用的二十五个组合。",

    "Here are the test assets of half a century of research.":
        "这就是半个世纪研究所用的检验资产。每只美国股票，每年6月按规模分成五组，并独立地按账面权益与市值之比分成五组：二十五个组合。"
        "<bookmark mark='a'/>它们在1963到2020年超出国库券的平均收益。横着读任何一行，收益从成长到价值上升；竖着读大多数列，收益从小盘到大盘下降。"
        "小盘价值股每年赚了近百分之十三，小盘成长股百分之四。<bookmark mark='b'/>而它们的市场贝塔都接近一。CAPM分不出这些组合，数据却能。"
        "一个好的模型必须解释这张网格。",

    "The first test runs through time.":
        "第一种检验沿时间进行。把每个组合的超额收益对因子做回归。如果因子本身就是超额收益，模型就只做一个预测：每个截距，每个阿尔法，都为零。"
        "<bookmark mark='a'/>Michael Gibbons、Stephen Ross和Jay Shanken构造了联合检验。把阿尔法堆在一起，用残差协方差的逆加权，"
        "使那些容易对冲的组合上的阿尔法权重更大，再除以一加上因子自身的平方夏普比率。在正态误差下，它服从精确的F分布。",

    "The statistic has a beautiful reading.":
        "这个统计量有一个优美的解读。它的分子恰好等于把检验组合加入因子后，可达到的最佳平方夏普比率上升了多少。<bookmark mark='a'/>"
        "所以当一个模型的因子已经包含第二十三部分第二章的切点组合时，它就能通过检验。而那些看起来很小、却出现在残差风险很低的组合上的阿尔法，"
        "会让它失败，因为这些组合可以加杠杆变成很高的夏普比率。",

    "The second test runs across assets.":
        "第二种检验跨资产进行。这是Eugene Fama和James MacBeth在1973年提出的方法：每个月，把当月收益对各组合的贝塔做回归。斜率就是当月每单位贝塔的回报。"
        "<bookmark mark='a'/>把所有月份的斜率平均，得到每个因子溢价的估计，用斜率自身逐月的变动求它的标准误。Jay Shanken的修正会放大这个标准误，"
        "因为贝塔本身也是估计出来的。一个被定价的因子，其溢价远离零，而截距，即完全没有贝塔的组合的收益，应当为零。",

    "Run both tests on the twenty-five portfolios":
        "在二十五个组合上运行这两种检验，1963到2020年。<bookmark mark='a'/>CAPM被决定性地拒绝，平均定价误差为每年二点三个百分点。"
        "Fama和French的三因子把它减半，降到一点一，Carhart的动量因子和五因子模型又减少了一点。<bookmark mark='b'/>而每个模型仍然被拒绝，"
        "p值低于十万分之一。这很正常。有七百个月的数据，检验强大到足以拒绝任何不是严格成立的模型。有用的问题不是模型是否错误，而是错得多严重、错在哪里。",

    "Where the models fail, cell by cell.":
        "模型在哪里失败，一格一格地看。<bookmark mark='a'/>在CAPM下，阿尔法与价值对齐：右边是红色，便宜的股票每年比它们的贝塔所预测的多赚多达五个百分点。"
        "<bookmark mark='b'/>以规模和价值为因子后，网格的大部分都变淡了。<bookmark mark='c'/>有一个角落没有。小盘成长股每年比这两个模型的预测少赚约五个半百分点，"
        "在五因子下仍少赚三个多百分点。小盘、昂贵、常常不盈利，还在增发股票：这是每个模型都留下的角落，第五章会回到这里。",

    "Another view: each portfolio's average return":
        "换个角度：每个组合的平均收益对模型的预测。<bookmark mark='a'/>在CAPM下，预测值挤在一个很窄的带里，因为贝塔几乎没有差别，"
        "而平均收益从百分之四到百分之十三不等：一道竖直的涂抹。<bookmark mark='b'/>在三因子下，点都落在直线附近，橙色的价值组合在右上方，"
        "红色的小盘成长组合远在直线下方。",

    "Three lessons for using these tests.":
        "使用这些检验的三个教训。<bookmark mark='a'/>当因子是可交易的组合时，时间序列阿尔法就是检验本身；横截面回归多了一个自由截距，"
        "并检验每个溢价是否等于因子自身的均值。<bookmark mark='b'/>谨慎选择检验资产：按规模和价值排序，等于把答案放进了问题里，"
        "Jonathan Lewellen、Stefan Nagel和Jay Shanken要求也用行业和其他排序。<bookmark mark='c'/>问模型错得多严重，而不是是否错误："
        "比较定价误差，或者每个模型的因子能达到的平方夏普比率。",

    "A model is rejected with a p-value of one in a thousand":
        "一个模型以千分之一的p值被拒绝，但它的平均定价误差只有每年零点三个百分点。你会用它吗？你会检查什么？",

    # ------------------------------------------------------------------ SizeValue
    "Chapter two. The first two factors":
        "第二章。前两个因子：规模和价值，以及由它们构成的三因子模型。",

    "Size and value began as anomalies":
        "规模和价值起初是异象，是CAPM的失败。<bookmark mark='a'/>Sanjoy Basu在1977年发现，相对于盈利便宜的股票跑赢了它们的贝塔。"
        "<bookmark mark='b'/>Rolf Banz在1981年发现，小公司也是如此，最小的公司尤其明显。<bookmark mark='c'/>Barr Rosenberg和同事在1985年发现，"
        "相对于账面价值便宜的股票跑赢了昂贵的股票，并把论文命名为市场无效的有力证据。<bookmark mark='d'/>然后Eugene Fama和Kenneth French在1992年证明，"
        "规模和账面市值比一起吸收了其他变量，连贝塔也被吸收，并在1993年把它们变成两个组合，作为因子与市场并列。",

    "How the factors are built, on forty made-up stocks.":
        "用四十只虚构的股票看因子是怎样构造的。每年6月，画出每只股票的规模对它的账面市值比。<bookmark mark='a'/>按规模在纽约证券交易所股票的中位数处切分，"
        "只用交易所的股票，这样成千上万的纳斯达克小公司不会决定这条线。<bookmark mark='b'/>按账面市值比在交易所股票的第三十和第七十百分位处切分。"
        "得到六个组合，每个都按市值加权。<bookmark mark='c'/>规模因子是三个小盘组合的平均减去三个大盘组合的平均。价值因子是两个便宜组合的平均减去两个昂贵组合的平均。"
        "每个因子在另一个特征上都是平衡的，所以规模不会暗中就是价值，价值也不会暗中就是规模。",

    "Here is each factor since 1926.":
        "这是1926年以来的每个因子。<bookmark mark='a'/>规模每年赚约两个半百分点，t统计量略高于二。价值赚四个百分点，t为三。<bookmark mark='b'/>"
        "但看看它们的形状：长长的攀升和长长的平坦期。规模的大部分收益发生在1980年以前，而价值在2007年以后回吐了很大一部分。一个因子的平均值，"
        "是对一条很不均匀的路径的概括。",

    "Now split the history at the year size was published.":
        "现在在规模被发表的那一年把历史切开。<bookmark mark='a'/>1981年以前，小盘股每年跑赢大盘股约三个半百分点。此后四十年，只有一个百分点，"
        "t统计量约为零点六：与零无法区分。价值也减半了，降到两个半百分点，不过仍为正。<bookmark mark='b'/>而且规模有日历。在一月，小盘股平均每月跑赢大盘股"
        "两个百分点；在其余十一个月，几乎为零。<bookmark mark='c'/>David McLean和Jeffrey Pontiff在近百个异象中发现了同样的规律：它们的收益在样本外低了约四分之一，"
        "发表后低了一半多。看起来像溢价的东西，有一部分是被发表纠正的错误定价，有一部分从来就不存在。",

    "Decade by decade.":
        "逐个十年来看。<bookmark mark='a'/>规模很不稳定：在1930年代、1960年代和2000年代很大，在1950年代、1980年代、1990年代和2010年代为负或持平。"
        "价值更稳定，直到2010年代之前每个十年都为正，2010年代它第一次整整十年都在亏损。第八章会衡量那十年。",

    "Why should either pay?":
        "它们为什么会有回报？第二十三部分的三种理由都适用。<bookmark mark='a'/>风险：Fama和French认为，便宜的公司常常陷入困境，价值承载着一种市场贝塔漏掉的"
        "艰难时期风险。<bookmark mark='b'/>错误：Josef Lakonishok、Andrei Shleifer和Robert Vishny认为，投资者外推过去的增长，为光鲜的股票付出过高的价格，"
        "并在增长回落时失望。<bookmark mark='c'/>而规模可能被测错了：Cliff Asness和同事发现，把低质量的小公司排除之后，规模溢价重新出现，而且比以前更稳定。",

    "The size premium fell from three and a half percent":
        "规模溢价从1981年以前的三个半百分点降到之后的一个百分点。它是死了、从未存在，还是藏起来了？什么证据能把它们区分开？",

    # ------------------------------------------------------------------ Momentum
    "Chapter three. Momentum:":
        "第三章。动量：经典因子中最强、也最奇怪的一个。",

    "Narasimhan Jegadeesh and Sheridan Titman's recipe":
        "这是Narasimhan Jegadeesh和Sheridan Titman在1993年的做法。每个月，按过去十二个月的收益给股票排序，去掉最近一个月。买入赢家，卖出输家，"
        "持有一个月，然后重复。<bookmark mark='a'/>因子版本，上涨减下跌，像规模和价值一样，用规模和过去收益的二乘三排序构造，"
        "但每个月而不是每年调仓一次。它的交易量大得多，这关系到成本，是第二十六部分的主题。",

    "Sort every American stock into ten portfolios":
        "按过去一年的收益把每只美国股票分进十个组合，跟踪九十四年。<bookmark mark='a'/>收益几乎一级一级地上升：去年的输家每年只比国库券多赚约一个百分点，"
        "去年的赢家多赚十五个百分点。没有任何公司特征，没有任何会计数字，只有它最近的价格。在有效市场里这不应该发生，Eugene Fama称动量为头号异象。",

    "Why skip the latest month?":
        "为什么跳过最近一个月？因为收益有三个期限，方向各不相同。<bookmark mark='a'/>在一个月的尺度上，收益反转：上个月的赢家下个月往往会跌一点，"
        "部分是买卖价差的反弹，部分是对提供流动性的回报。<bookmark mark='b'/>在二到十二个月的尺度上，收益延续。<bookmark mark='c'/>在三到五年的尺度上，"
        "收益又反转了，正如Werner De Bondt和Richard Thaler所发现的，这是一种接近价值的规律。动量存在于中间的期限。",

    "The momentum factor's record, ninety-four years.":
        "动量因子九十四年的记录。<bookmark mark='a'/>每年七个半百分点，夏普比率接近一半，t统计量四点五：经典美国因子中最强的。<bookmark mark='b'/>"
        "而偏度为负三，最差月份为负百分之五十三，回撤达百分之七十八。动量一小步一小步地赚取溢价，又在几个可怕的月份里把它还回去。",

    "Momentum has a second form.":
        "动量还有第二种形式。Tobias Moskowitz、Yao Hua Ooi和Lasse Pedersen单独考察每一个期货市场。如果它自己过去一年的超额收益为正，就做多；为负，就做空；"
        "每个头寸都调整到相同的预期波动率。<bookmark mark='a'/>把它在五十八个市场上取平均，包括股指、债券、货币和商品，就得到时间序列动量。"
        "没有任何东西与其他东西相互排名，所以整个账簿可以做多一切，也可以做空一切。这就是管理期货基金做了几十年的趋势跟踪，写成了一个因子。",

    "AQR publishes the factor, updated, from 1985.":
        "AQR公布了这个因子的更新版本，从1985年开始。<bookmark mark='a'/>每个资产类别单独的夏普比率约为零点六。合在一起，超过一：股指、债券、货币和商品中的趋势"
        "几乎相互独立，所以组合远比任何一部分平稳。<bookmark mark='b'/>它与股票动量相关，相关系数约为零点四，但不是同一回事。而在2008年，"
        "市场下跌百分之三十八时，时间序列动量赚了百分之二十五。",

    "Plot each quarter's time-series momentum return":
        "把每个季度的时间序列动量收益对股票市场的收益作图。<bookmark mark='a'/>拟合得最好的曲线是一个微笑。在大幅下跌的季度，趋势跟踪者已经做空并获利；"
        "在大幅上涨的季度，他们做多并获利；在平静的季度，他们来回被打脸，亏一点。这就是第十一部分中做多市场跨式期权的收益形状，"
        "也是趋势跟踪被当作危机保险出售的原因。迄今为止，这是一种平均收益为正的保险。",

    "Why does it work? The leading explanations are behavioural.":
        "它为什么有效？主要的解释是行为方面的。<bookmark mark='a'/>反应不足：消息在投资者之间传播得很慢，听到消息的人又锚定在旧有的看法上，"
        "所以价格会在几个月里向消息漂移。<bookmark mark='b'/>第二十三部分的处置效应：投资者过早卖出赢家、死守输家，这在两个方向上都减慢了调整。"
        "<bookmark mark='c'/>风险方面的解释一直很难找到。平均而言，动量在坏时候并不更差。但它有一种特殊的、灾难性的风险，这就是下一章。",

    "Cross-sectional momentum is always long winners":
        "截面动量总是做多赢家、做空输家；时间序列动量可以做空一切。你预期哪一个在崩盘中表现更好？在随后的反弹中呢？",

    # ------------------------------------------------------------------ Crash
    "Chapter four. The momentum crash:":
        "第四章。动量崩盘：它何时发生、为什么发生，以及能做些什么。",

    "Here are the two years month by month":
        "这是逐月的这两年，蓝色是市场，粉色是动量。<bookmark mark='a'/>在2008年市场下跌时，动量表现很好：它的空头一侧满是银行和周期性公司，"
        "那一年最大的输家。<bookmark mark='b'/>然后市场在2009年3月掉头。那些按破产定价的输家反弹得最猛。动量3月亏损百分之十二，4月百分之三十四，"
        "5月百分之十三：三个月里损失了约一半的价值，而市场上涨了四分之一。",

    "It had happened before.":
        "这以前就发生过。1932年7月，道琼斯指数见底，比1929年的高点低了百分之八十九。<bookmark mark='a'/>在7月和8月，市场上涨了百分之八十多，"
        "由跌得最深的股票领涨。动量在两个月里亏损了百分之七十四，这是它有记录以来最差的两个月。模式是一样的：漫长的熊市、满是被压垮股票的空头一侧，以及一次突然的反弹。",

    "The six worst months in ninety-four years.":
        "九十四年里最差的六个月。<bookmark mark='a'/>1932年夏天的两个月；2009年4月；1939年9月，欧洲的战争让市场急涨；2001年1月，纳斯达克的反弹；"
        "以及1938年6月。每一个都出现在市场的急剧反弹中。动量崩盘不是随机的。它们的类型是可以预测的，日期却不能。",

    "Kent Daniel and Tobias Moskowitz explained the mechanism.":
        "Kent Daniel和Tobias Moskowitz解释了其中的机制。动量的市场贝塔不是固定的。它等于过去一年中赢家的贝塔减去输家的贝塔。<bookmark mark='a'/>"
        "在漫长的熊市之后，输家是随市场跌得最狠的股票：杠杆最高、贝塔最高的公司。于是动量最终做空了一个贝塔非常高的组合，"
        "相当于一笔没有人选择去做的、押注市场不会反弹的大赌注。",

    "Measure it. Split the months by whether the market had fallen":
        "测量一下。按市场在过去两年是否下跌把月份分开。<bookmark mark='a'/>在正常时期，动量的贝塔约为零，每年赚约百分之十一。<bookmark mark='b'/>"
        "在熊市中它的贝塔降到负零点五，市场继续下跌时它表现很好。<bookmark mark='c'/>但在熊市中市场上涨的月份，它的贝塔约为负一，"
        "以每年接近百分之五十的速度亏损。崩盘就藏在那一百个月里。",

    "Draw it as a payoff.":
        "把它画成收益图。在熊市中，如果市场继续下跌，动量赚一点；如果市场上涨，它亏很多。<bookmark mark='a'/>这就是第十部分中卖出市场看涨期权的形状。"
        "动量投资者在不知不觉中卖出了对反弹的期权，而这些期权恰恰在波动率最高、崩盘之后最值钱。溢价是真实的，偶尔到来的账单也是。",

    "One repair is simple.":
        "有一种修补很简单。动量的崩盘出现在它的波动率已经很高的时候，所以那时少持有一些。Pedro Barroso和Pedro Santa-Clara每个月把这个因子缩放到固定的预期波动率，"
        "只用过去六个月的数据。<bookmark mark='a'/>在九十四年里，夏普比率从约一半升到四分之三；偏度从负三升到负零点八；最差回撤从百分之七十八降到百分之四十六。"
        "2009年的崩盘被减半。<bookmark mark='b'/>Daniel和Moskowitz自己的版本更进一步，同时预测均值和方差，并在熊市中减少动量的持仓。",

    "Three cautions.":
        "三个提醒。<bookmark mark='a'/>缩放只用过去的数据，所以没有前视偏差。但窗口、目标和上限是由了解这段历史的研究者选的，第二十六部分会把这类选择计入试验次数。"
        "<bookmark mark='b'/>它的推广性不好：Scott Cederburg和同事发现，实时实施时，波动率管理对动量有帮助，对大多数其他因子却没有。"
        "<bookmark mark='c'/>而在崩盘中，每只动量基金都做空同样的股票。当它们反弹时，所有人必须同时买入。这就是拥挤，一条贯穿本系列其余部分的线索。",

    "The market has fallen forty percent over two years":
        "市场两年里下跌了百分之四十，刚刚一个月上涨了百分之十。动量的贝塔约为负一。你会怎样处理动量头寸？如果你错了，代价是什么？",

    # ------------------------------------------------------------------ Profit
    "Chapter five. Two more factors":
        "第五章。另外两个因子，盈利能力和投资，以及由它们构成的两个竞争模型。",

    "Start from the dividend discount model":
        "像Fama和French那样，从股利贴现模型出发。一家公司的市值，是它能派发的现金流的贴现：盈利减去增加账面权益所需的投资。<bookmark mark='a'/>"
        "除以账面权益。在稳定的权益回报率和稳定的增长下，市值与账面值之比只取决于三样东西：盈利能力、投资和贴现率。<bookmark mark='b'/>反过来看。"
        "固定其中两个，更高的预期收益就表现为更高的账面市值比，或者更高的盈利能力，或者更低的投资。价值、盈利能力和投资，是通向同一个不可观测的贴现率的三扇窗。",

    "In numbers. A firm earning twelve percent":
        "用数字说。一家账面回报率为百分之十二、每年增长百分之五、以百分之九贴现的公司，账面市值比约为零点六。<bookmark mark='a'/>让它的盈利能力变差，"
        "它的账面市值比就翻了一倍多：风险没有任何变化，它看起来却像一只价值股。让它投资更多，它看起来就像成长股。让它风险更高，它看起来又像价值股。"
        "<bookmark mark='b'/>所以一只便宜的股票，可能是因为风险高而便宜，也可能只是因为生意差。只有控制了盈利能力和投资，价值才能衡量贴现率。",

    "The evidence came first, as usual.":
        "和往常一样，证据先出现。Robert Novy-Marx用毛利润，即收入减去销售成本，除以总资产来衡量盈利能力：这个数字在大多数会计选择之前就已确定。"
        "盈利能力强的公司赚得更多，可靠程度和便宜的公司差不多。而由于盈利能力强的公司往往昂贵，盈利能力策略往往做多成长股，天然对冲了价值。"
        "他称之为价值的另一面。",

    "In 2015 Fama and French added two factors.":
        "2015年，Fama和French增加了两个因子。按经营盈利能力的稳健减疲弱，以及按总资产增长的保守减激进：投资少的公司对投资多的公司。"
        "<bookmark mark='a'/>1963年以来，每个因子每年都赚约三个百分点，和价值一样，但波动更小，t统计量更高。而投资与价值高度相关，约为零点七："
        "便宜的公司通常就是不在扩张的那些。",

    "Now a striking test.":
        "现在做一个惊人的检验。把价值的收益对其他四个因子做回归。<bookmark mark='a'/>只对市场和规模，价值每年有接近四个百分点的阿尔法。"
        "<bookmark mark='b'/>加入盈利能力和投资后，阿尔法消失了，降到约负一个百分点，t为负零点八。Fama和French自己报告了这一点：在他们自己的五因子模型里，"
        "价值，这个让他们出名的因子，是多余的。它的溢价被它对少投资公司的倾斜所解释。",

    "A rival model arrived the same year":
        "同一年，一个竞争模型从另一个方向出现。Kewei Hou、Chen Xue和Lu Zhang从公司的投资决策出发。公司会一直投资，直到再增加一单位资本的边际成本"
        "等于它将带来的贴现利润。重新整理后，预期收益随预期盈利能力上升，随投资下降。不需要投资者心理，不需要消费，只需要公司的一阶条件。"
        "<bookmark mark='a'/>他们的因子从1967年开始：投资和盈利能力每年分别赚约四和六个百分点，后来的预期增长因子接近十个百分点，t统计量超过十。"
        "价值在它们面前同样没有阿尔法。",

    "Which model wins?":
        "哪个模型胜出？<bookmark mark='a'/>Francisco Barillas和Jay Shanken展示了如何比较它们：比较它们的因子所能达到的最佳平方夏普比率。"
        "五因子和q模型都胜过三因子，加入动量对两者都有帮助；没有明确的赢家。<bookmark mark='b'/>它们对原因的看法也不同：Fama和French把因子解读为风险，"
        "Hou、Xue和Zhang解读为无论贴现率由什么驱动、公司的最优投资，Robert Stambaugh和Yu Yuan解读为错误定价。<bookmark mark='c'/>还有一个提醒："
        "预期增长因子使用的预测，是在它被检验的同一份数据上拟合出来的。t统计量为十，值得第二十五部分那样的审视。",

    "In the five-factor model value has no alpha.":
        "在五因子模型里价值没有阿尔法。一个持有盈利能力和投资因子的投资者，还应该持有价值吗？什么会改变你的答案？",

    # ------------------------------------------------------------------ LowRisk
    "Chapter six. The low-risk anomaly":
        "第六章。低风险异象：把第二十三部分那条平的线变成一个因子。",

    "Part twenty-three found the security market line too flat":
        "第二十三部分发现证券市场线太平：低贝塔股票赚得太多，高贝塔股票赚得太少。Andrea Frazzini和Lasse Pedersen把它变成了一个因子。"
        "估计每只股票的贝塔，相关系数用五年数据、波动率用一年数据，再把它向一收缩。<bookmark mark='a'/>然后按贝塔给股票排序，把低贝塔的一半加杠杆到贝塔为一，"
        "把高贝塔的一半去杠杆到一，做多前者、做空后者。结果没有市场暴露，而且它加杠杆持有安全的股票，这恰恰是受约束的投资者做不到的。",

    "AQR publishes the factor for twenty-four countries.":
        "AQR公布了二十四个国家的这个因子。<bookmark mark='a'/>在美国，1930年以来押注低贝塔每年赚八个百分点，夏普比率约零点七，t统计量接近七，"
        "是这个窗口里最强的经典美国股票因子。在全球，1987年以来，九个百分点，夏普比率零点九。<bookmark mark='b'/>它并非没有风险。美国版本在最糟糕的时候亏掉了一半多的价值。",

    "The same pattern appears with plain volatility.":
        "用普通的波动率也会出现同样的规律。按过去的波动程度把股票分成五组。<bookmark mark='a'/>前四组的平均收益差不多，每年七到十个百分点，"
        "最波动的五分之一则降到四个百分点，而波动率从百分之十二升到百分之二十八。夏普比率从接近零点六降到不到零点二。Andrew Ang、Robert Hodrick、Yuhang Xing"
        "和Xiaoyan Zhang发现了最极端的版本：特质波动率高的股票，即那种根本不应被定价的风险，赚得最少。",

    "Three explanations, all about constraints or preferences":
        "三种解释，都关于约束或偏好，没有一种关于风险。<bookmark mark='a'/>杠杆：不能借钱的投资者买高风险股票来追求收益，把它们的价格抬高。"
        "<bookmark mark='b'/>彩票：有很小机会获得巨大收益的高波动股票被高估，这是第二十三部分的前景理论。<bookmark mark='c'/>基准：以指数为考核基准的基金经理，"
        "无法持有加杠杆的安全股票而不偏离指数，所以高贝塔股票成了试图跑赢指数的捷径。",

    "And a critique worth taking seriously.":
        "还有一个值得认真对待的批评。<bookmark mark='a'/>Robert Novy-Marx和Mihail Velikov认为，押注低贝塔公布的收益依赖于其构造的细节：排名权重、"
        "来自不匹配窗口的贝塔，以及集中在小型、流动性差的股票上的杠杆；按常规方法构造，它赚得少得多。<bookmark mark='b'/>它的成本和融资与纸面收益相去甚远。"
        "<bookmark mark='c'/>而简单的排序说明了原因：低波动股票的原始收益只比高波动股票多一点点；异象在于风险调整后的收益，需要杠杆才能获取。",

    "A pension fund that cannot borrow wants more return. Should it buy":
        "一只不能借钱的养老基金想要更高的收益。它应该买高贝塔股票，还是低贝塔股票加上一些股指期货？低风险异象又说明了其他所有人的选择是什么？",

    # ------------------------------------------------------------------ Everywhere
    "Chapter seven. If value and momentum are real":
        "第七章。如果价值和动量是真实的，它们应当出现在每个市场里。是这样吗？",

    "Cliff Asness, Tobias Moskowitz and Lasse Pedersen defined":
        "Cliff Asness、Tobias Moskowitz和Lasse Pedersen在八个市场里用同样的方式定义价值和动量。<bookmark mark='a'/>在四个股票市场中，"
        "价值是账面市值比，动量是过去一年的收益。<bookmark mark='b'/>在各国股指中，同样如此，只是以整个国家为单位。<bookmark mark='c'/>"
        "在货币、商品和政府债券中，价值是长期便宜程度的某种度量，比如一种货币在五年里实际汇率变得便宜，或者一种商品下跌了五年；动量仍然是过去一年。"
        "没有针对某个市场的调参。",

    "The results, updated to 2020.":
        "结果，更新到2020年。<bookmark mark='a'/>价值在全部八个市场中夏普比率都为正，动量在全部八个市场中也都为正，尽管各自在某处较弱：动量在日本，两者在债券。"
        "<bookmark mark='b'/>在每一个市场中，它们的相关系数都为负，大约在负四分之一到负三分之二之间。<bookmark mark='c'/>所以五五组合在每个市场都胜过任何一个单独持有。",

    "The arithmetic is chapter one of Part twenty-three.":
        "其中的算术是第二十三部分的第一章。把两个波动率相近的策略混合：平均收益保留下来，而在负相关下大部分风险相互抵消。<bookmark mark='a'/>"
        "所有市场合在一起，价值单独的夏普比率为零点四，动量为零点六。它们的相关系数为负零点六，五五组合的夏普比率超过一。原因是机械性的："
        "一项资产通常是因为下跌才变得便宜，这使它成为动量的输家。价值和动量彼此相抵，各自掩护对方最糟糕的年份。",

    "Here are the paths.":
        "这是它们的路径。<bookmark mark='a'/>价值和动量，各自覆盖所有市场，轮流攀升：1990年代末价值下沉时动量上升，2000年代初价值上升，2009年动量崩盘。"
        "<bookmark mark='b'/>组合是一条更平稳的线。它的最差回撤为百分之十，而单独持有任何一个约为三分之一。它在这里增长得更慢，只是因为波动率只有一半；"
        "加杠杆到同样的风险，它会把两者都甩在后面。",

    "A third style travels too: carry.":
        "第三种风格也能推广：套息。Ralph Koijen、Moskowitz、Pedersen和Evert Vrugt把一项资产的套息定义为价格不变时它能赚到的收益：对期货合约而言，"
        "就是现货价格与期货价格之间的差距。<bookmark mark='a'/>每个预期收益都等于套息加上预期价格变化。套息策略做多高套息、做空低套息，"
        "押注价格的变化小于套息所承诺的。第二十二部分的货币套息交易就是其中一例。",

    "AQR's century of factor premia includes carry":
        "AQR的一个世纪因子溢价数据包含四个资产类别中的套息。<bookmark mark='a'/>它在四个类别中都为正，在政府债券中最强，买入高收益、曲线陡峭的部分一直有回报，"
        "在各国股指中最弱。<bookmark mark='b'/>四个中有三个呈负偏：就像第二十二部分的货币套息一样，套息平稳地赚钱，又突然地亏钱。",

    "And quality. Cliff Asness, Andrea Frazzini and Lasse Pedersen":
        "还有质量。Cliff Asness、Andrea Frazzini和Lasse Pedersen问：投资者应该为什么样的东西多付钱？一家盈利、增长、安全并派发盈利的公司。"
        "在这四个方面给每只股票打分，买入最好的，卖出最差的。<bookmark mark='a'/>1957年以来，质量减垃圾每年赚四个百分点，夏普比率超过一半，"
        "市场贝塔为负：它在崩盘中表现最好，那时投资者逃向质量。令人困惑的是价格。质量股只比垃圾股贵一点点，相对于它们带来的东西，贵得太少了。",

    "What does it mean that the same styles work":
        "同样的风格在如此不同的市场中都有效，这意味着什么？<bookmark mark='a'/>也许是一种共同的风险：Asness、Moskowitz和Pedersen发现，所有市场中的价值和动量"
        "都以相反的方向载荷于资金流动性。<bookmark mark='b'/>也许是共同的行为：外推、反应迟缓和有限的套利资本并非股票所特有。<bookmark mark='c'/>"
        "无论哪种，对组合的教训都一样：先在风格和市场之间分散。这是最便宜的降低风险的方法。",

    "Momentum and value are negatively correlated. Why hold both, if":
        "动量和价值负相关。如果各自都有正溢价，为什么两个都持有？什么时候两个都持有会令人失望？",

    # ------------------------------------------------------------------ ValueDecade
    "Chapter eight. Value's lost decade":
        "第八章。价值失去的十年，用数字衡量，以及它证明了什么、没有证明什么。",

    "From January 2007 to the autumn of 2020, value lost.":
        "从2007年1月到2020年秋天，价值一直在亏。<bookmark mark='a'/>价值因子中的一美元跌到四十二美分，回撤百分之五十七，是它历史上最严重的。"
        "这十四年里平均每年负百分之五，而此前八十年是正百分之五点五。<bookmark mark='b'/>便宜的股票，包括银行和能源，越来越便宜；昂贵的股票，"
        "首先是科技股，越来越昂贵。",

    "How surprising was it?":
        "这有多意外？假设价值的真实溢价保持在过去的平均水平。那么一个低到这种程度的十四年平均值，距离它约四个标准误。<bookmark mark='a'/>在正态收益下这很罕见，"
        "在厚尾下没那么罕见，但确实是一个意外。不过把这个算术反过来。夏普比率约为一半时，真实的溢价需要大约二十年的数据才能使t统计量达到二。"
        "十年既不能证明一个因子有效，也不能证明它已经失效。",

    "Much of the loss shows up in prices, not in businesses.":
        "亏损的大部分体现在价格上，而不是生意上。价值价差比较的是最便宜的百分之三十股票的账面市值比与最昂贵的百分之三十的账面市值比。"
        "<bookmark mark='a'/>1926年以来，它围绕约一点五（取对数后）的中位数徘徊。到2020年，它达到二点四，高于百分之九十六的年份，上一次见到这个水平是在1930年代，"
        "互联网泡沫顶峰时也接近过。价值股相对于成长股变得异常便宜。",

    "Rob Arnott, Campbell Harvey, Vitali Kalesnik":
        "Rob Arnott、Campbell Harvey、Vitali Kalesnik和Juhani Linnainmaa把价值的收益分成两部分：价差的变化，他们称之为重估，以及其余的一切。"
        "失去的十年大部分是重估：成长股只是相对于价值股变得更贵了。<bookmark mark='a'/>把第二十三部分的Campbell–Shiller恒等式用于价差本身。"
        "今天的宽价差之后，要么是价差收窄带来的价值高收益，要么是价值公司的利润进一步落后。恒等式说不出是哪一个。",

    "Four explanations were offered.":
        "人们给出了四种解释。<bookmark mark='a'/>账面价值过时了：Andrea Eisfeldt、Edward Kim和Dimitris Papanikolaou证明，会计账面权益漏掉了无形资本，"
        "研发、品牌、组织，把它们加回去的价值因子表现好得多。<bookmark mark='b'/>利率下降：成长股是长久期资产，现金流在遥远的将来，而利率在整个十年里都在下降。"
        "<bookmark mark='c'/>资金流：被动资金和动量资金流向成长股，而第二十三部分发现这些市场缺乏弹性。<bookmark mark='d'/>或者是运气不好："
        "Ronen Israel、Kristoffer Laursen和Scott Richardson发现，价差扩大了，而便宜公司的基本面并不比平常更差。",

    "Details matter, too.":
        "细节也很重要。Fama和French用上一年12月的价格计算账面市值比，价格可能已经过时十八个月。Cliff Asness和Andrea Frazzini用当前价格。"
        "<bookmark mark='a'/>在同样的十四年里，他们的版本每年亏约两个半百分点，而不是五个。同样的想法，不同的细节，一半的亏损："
        "这提醒我们，所谓“价值因子”是一族组合，而不是单一的事实。",

    "The verdict.":
        "结论。<bookmark mark='a'/>这十年证明，一个夏普比率为一半的因子可以连亏十四年，任何持有它的人都必须能等那么久，还要能向客户解释这种等待。"
        "<bookmark mark='b'/>它没有证明价值已死；证据从来没有强到能被十年推翻。<bookmark mark='c'/>而接下来发生的事是封存的。本部分的研究截止于2020年12月，"
        "正处在价值的谷底。第十三章会打开信封。",

    "It is December 2020, and the value spread":
        "现在是2020年12月，价值价差处于第九十六百分位。你预期价值接下来会怎样？你能有多大把握？",

    # ------------------------------------------------------------------ Green
    "Chapter nine. Environmental, social and governance investing":
        "第九章。环境、社会与治理投资，以及因子的预期收益与实现收益之间的区别。",

    "Lubos Pastor, Robert Stambaugh and Lucian Taylor built":
        "Lubos Pastor、Robert Stambaugh和Lucian Taylor建立了均衡模型。一些投资者从持有绿色公司中获得满足，不喜欢棕色公司。"
        "他们把绿色股票的价格抬高，直到其预期收益变低：投资者接受较低的收益来持有自己喜欢的东西。<bookmark mark='a'/>但实现的收益包含意外。"
        "如果对气候的关注上升得比任何人预期的都多，这些投资者会把绿色股票抬得更高、把棕色股票压得更低。于是绿色股票可以跑赢好几年，"
        "而它们的预期收益始终更低。",

    "A made-up decade shows the trap.":
        "一个虚构的十年揭示了这个陷阱。绿色股票的定价使其每年赚百分之五，棕色股票百分之七：就是那两条虚线。<bookmark mark='a'/>现在让对气候的关注每年都比预期多上升一点。"
        "绿色股票从每次意外中获益，棕色股票受损，绿色以很大的优势赢下这十年。<bookmark mark='b'/>看回测的分析师会得出结论：绿色股票有溢价。"
        "模型说的正好相反：它们的预期收益一直更低，跑赢只是一次性的重新定价，除非关注度继续超预期上升，否则不会重演。",

    "The evidence fits.":
        "证据与之相符。<bookmark mark='a'/>Pastor、Stambaugh和Taylor发现，2012到2020年美国绿色股票确实跑赢了棕色股票，而一旦把由新闻报道衡量的、"
        "气候关注度意外上升的月份考虑进去，跑赢就消失了。<bookmark mark='b'/>Patrick Bolton和Marcin Kacperczyk发现了另一面：排放更高的公司收益更高，"
        "即碳溢价。<bookmark mark='c'/>所以绿色倾斜不是额外预期收益的来源。它是一种押注：关注度上升得比价格已经假设的更快。",

    "There is also a measurement problem.":
        "还有一个测量问题。Florian Berg、Julian Koelbel和Roberto Rigobon比较了六家主要的ESG评级机构。它们对同一批公司的评级相关系数只有约零点四到零点七，"
        "而信用评级几乎完全一致。大部分分歧在于测量什么以及如何测量。用一家机构的评分构造的因子，与用另一家构造的是不同的组合，"
        "而在事后被修订的评级上做回测，正是第三部分警告过的那种陷阱。",

    "The lesson reaches beyond green investing.":
        "这个教训不止适用于绿色投资。<bookmark mark='a'/>当一个特征变得流行时，它变流行的那段时期仅凭重新定价就会显示出高收益，"
        "从那段时期估计出的溢价连符号都是错的。<bookmark mark='b'/>2010年代的成长股和1981年以前的小盘股也是如此：回测的平均值包含估值的变化，"
        "而估值不可能永远朝一个方向变化。",

    "A green fund beat the market by three percent":
        "一只绿色基金连续五年每年跑赢市场三个百分点，它的营销材料说绿色股票有溢价。你需要看到什么才会相信？",

    # ------------------------------------------------------------------ Timing
    "Chapter ten. Holding a factor through a lost decade is hard.":
        "第十章。在失去的十年里一直持有一个因子很难。能不能改为择时？",

    "There are two natural ways to time a factor.":
        "给因子择时有两种自然的方法。<bookmark mark='a'/>按估值：当它的多头一侧相对于空头一侧异常便宜时多持有一些。<bookmark mark='b'/>"
        "或者按它自己的过去：多持有最近表现好的因子。<bookmark mark='c'/>Cliff Asness称之为塞壬之歌。信号很弱，而按价差给价值择时，"
        "实际上是再加一剂价值。一个择时的账簿，分散程度比看起来要低。",

    "Test the first idea on value itself.":
        "用价值本身检验第一种想法。每年12月的价值价差；下一年价值的收益。九十三年。<bookmark mark='a'/>斜率为正，正如第二十三部分的恒等式所说："
        "更宽的价差之后，价值的年份更好。但t统计量约为一点八，R方为百分之五。2020年底，拟合线指向下一年价值约百分之十二的收益，是平均值的三倍。"
        "R方只有百分之五，这只是概率的一点倾斜，不是任何人应该拿整个公司去押的预测。",

    "A more disciplined version comes from Valentin Haddad":
        "一个更有纪律的版本来自Valentin Haddad、Serhiy Kozak和Shrihari Santosh。他们不是逐个给五十个异象择时，而是取异象组合中少数几个主要的主成分，"
        "又是第二十三部分的APT，并用各自的估值价差来预测它们。<bookmark mark='a'/>然后用协方差矩阵把预测组合起来，就像Markowitz那样。"
        "他们报告择时组合远好于静态组合，并得出结论：贴现因子的波动率，即Hansen–Jagannathan那个量，随时间变化很大。这个方法把预测的数量保持在很少，"
        "这是对过度拟合弱信号的唯一防线。",

    "The second idea: factor momentum.":
        "第二种想法：因子动量。Sina Ehsani和Juhani Linnainmaa把第三章的时间序列动量用于因子本身。每个月，持有过去一年为正的每个因子，"
        "做空过去一年为负的每个因子。用六个美国因子来做，规模、价值、盈利能力、投资、动量和短期反转，从1964年开始。",

    "The result. <bookmark mark='a'/> Factor momentum works:":
        "结果。<bookmark mark='a'/>因子动量有效：夏普比率约零点六，t统计量超过四。因子确实有趋势。<bookmark mark='b'/>但在这里，"
        "简单地一直等额持有全部六个因子要好得多：夏普比率超过一。每个因子大部分时间本来就是被做多的，而因子动量每做空其中一个月，"
        "就放弃了那个因子的溢价和它带来的分散化。择时不是免费的。",

    "And a surprising link.":
        "还有一个令人惊讶的联系。把股票动量因子对因子动量做回归。<bookmark mark='a'/>股票动量的阿尔法降到每年约两个百分点，t为一：统计上，什么也没剩下。"
        "Ehsani和Linnainmaa的解读是，去年上涨的股票大多是暴露于去年上涨的因子的股票。个股中的动量，也许就是因子中的动量，一次看一只股票而已。",

    "So: <bookmark mark='a'/> timing signals explain":
        "所以：<bookmark mark='a'/>择时信号只能解释因子一年收益的百分之几；它们只有在跨许多因子、许多年时才有帮助，交易成本还会拿走一部分。"
        "<bookmark mark='b'/>预测少数几个组合，而不是每一个异象，因为每多一个预测，就多一次过度拟合的机会。<bookmark mark='c'/>"
        "把默认做法定为稳定地持有一组分散的因子，择时只在边际上进行。",

    "A factor-momentum rule would have sold value in 2019 and 2020":
        "一个因子动量规则会在价值连续两年表现不好之后，于2019和2020年卖出价值。那是一个好规则还是运气不好？你需要多少年才能分辨？",

    # ------------------------------------------------------------------ China
    "Chapter eleven. The world's second-largest stock market":
        "第十一章。世界第二大股票市场，以及它需要的因子。",

    "China's A-share market differs from America's":
        "中国的A股市场在一些对因子很重要的方面与美国不同。<bookmark mark='a'/>它的大部分交易由个人投资者完成，股票换手的频率是美国的好几倍。"
        "<bookmark mark='b'/>上市是配给的：首次公开发行需要监管批准，排队很长。所以一家上市公司本身就有价值，可以作为一个壳，让私人公司通过借壳上市。"
        "<bookmark mark='c'/>最小的上市公司在一定程度上是按壳来定价的，它们的收益跟随被收购的概率，而不是它们自己的生意。",

    "Jianan Liu, Robert Stambaugh and Yu Yuan wrote":
        "Jianan Liu、Robert Stambaugh和Yu Yuan把一家中国小公司的价格写成其业务价值，加上借壳的概率乘以其上市资格的价值。对这样的公司来说，"
        "规模和估值比率衡量的是壳，而不是公司。所以在构造任何因子之前，他们先去掉最小的百分之三十的股票。这本身就是一个教训：同一个特征在不同的制度下可能意味着不同的东西。",

    "Their model, CH-four, has four factors.":
        "他们的模型CH-4有四个因子。市场，以及<bookmark mark='a'/>规模，像美国那样在剩下的股票上构造。<bookmark mark='b'/>价值，用盈利价格比而不是账面市值比来衡量，"
        "因为在中国它吸收了所有其他估值比率。<bookmark mark='c'/>还有一个换手率因子，悲观减乐观：交易量远超平常的股票，是散户热情把价格抬高的那些，"
        "它们随后会落后。这是为个人交易者的市场构造的情绪因子。",

    "The factors from 2000 to 2020, beside America's":
        "2000到2020年的这些因子，与同期的美国因子并列。<bookmark mark='a'/>中国市场的波动大得多，夏普比率更低。<bookmark mark='b'/>它的价值因子每年赚约百分之十三，"
        "夏普比率超过一，而美国价值在同样的二十一年里几乎什么也没赚到。换手率因子每年赚九个百分点。在个人交易者的市场里，情绪和便宜带来的回报远高于美国。",

    "The paths, twenty-one years.":
        "二十一年的路径。<bookmark mark='a'/>价值几乎稳步攀升，换手率也是；规模更弱，也更起伏。而规模和价值高度负相关，约为负零点六："
        "在中国，小公司就是昂贵的公司，即使去掉最小的那些，仍有壳溢价的痕迹。",

    "Two lessons. <bookmark mark='a'/> Institutions shape factors.":
        "两个教训。<bookmark mark='a'/>制度塑造因子。上市规则制造了壳溢价；个人交易者的市场制造了换手率溢价。因子是关于某个市场的事实，而不是关于一般股票的事实。"
        "<bookmark mark='b'/>而制度会变。监管机构在2016年收紧了借壳上市的规则，随着量化基金在中国大量涌现，它的因子也暴露于与美国同样的拥挤之中，"
        "这是第二十九部分要讲的故事。",

    "Chinese value earned a Sharpe ratio above one":
        "中国价值在2000到2020年的夏普比率超过一，而美国价值几乎什么也没赚到。你预期它会继续吗？什么会让它停下来？",

    # ------------------------------------------------------------------ Firms
    "Chapter twelve. The firms that turned the factors into funds":
        "第十二章。把因子变成基金的公司，依据公开记录来描述。",

    "The first firm built on the factors was Dimensional":
        "第一家建立在因子之上的公司是Dimensional Fund Advisors，1981年由David Booth和Rex Sinquefield创立，就在Banz发表规模效应的那一年。"
        "它最初的目的是让养老基金系统地投资于小公司，这些公司此前大多被机构组合忽视。后来它加入了价值和盈利能力，并与Eugene Fama和Kenneth French密切合作。"
        "它的基金基于规则，但不是通常意义上的指数基金：它们围绕目标耐心地交易，以降低成本。Dimensional是作为只做多、低换手率产品的因子。",

    "The second is AQR Capital Management":
        "第二家是AQR Capital Management，1998年由Cliff Asness和来自高盛量化团队的同事创立。它在各个资产类别中运行第七章的风格，价值、动量、套息和防御，"
        "既做多空也做只做多，并公布了本部分所用的数据集。据报道，它的资产在2018年约为两千二百六十亿美元。然后价值最糟糕的几年到来，客户撤走了其中很大一部分，"
        "正如第二十三部分Shleifer和Vishny的模型对任何被投资者按近期收益评判的套利者所预测的那样。",

    "The third is the factor exchange-traded fund.":
        "第三类是因子交易所交易基金。<bookmark mark='a'/>指数提供商公布价值、动量、质量、低波动和规模指数的规则，基金以低成本、公开透明的方式跟踪它们。"
        "<bookmark mark='b'/>它们只做多，而且通常很宽泛：是对因子的倾斜，而不是论文中的多空组合。<bookmark mark='c'/>而公开的规则是可预测的交易。"
        "其他交易者可以在指数纳入一只股票之前买入、在剔除之前卖出，代价由基金持有人承担。",

    "What does a long-only factor fund actually hold?":
        "一只只做多的因子基金实际持有什么？大约是市场，再加上多空因子的一部分，典型的价值基金为五分之一到五分之二。<bookmark mark='a'/>它的大部分风险是市场的。"
        "因子表现为相对于指数的跟踪误差，每年几个百分点。对这样的基金来说，价值失去的十年，就是十年里每年落后基准一两个百分点：不是崩盘，但足以失去大部分客户。",

    "And costs. <bookmark mark='a'/> Value and profitability rebalance":
        "还有成本。<bookmark mark='a'/>价值和盈利能力每年调仓一次。动量每月调仓，一年内要把组合换手好几次，所以它的成本最高。<bookmark mark='b'/>"
        "Andrea Frazzini、Ronen Israel和Tobias Moskowitz用AQR自己的交易测量了成本，发现它们远低于学术估计：经典因子在那家公司的规模上经得起成本。"
        "Robert Novy-Marx和Mihail Velikov发现，许多较小的异象经不起。<bookmark mark='c'/>还有容量：追随一个因子的资金越多，它自己的交易就越会把价格推向不利方向。"
        "第二十六部分把成本放进每一次回测；第三十七部分测量冲击。",

    "A long-only value fund trailed its index":
        "一只只做多的价值基金连续十年每年落后其指数一个半百分点。是基金坏了、因子坏了，还是都没有？你会问基金经理什么？",

    # ------------------------------------------------------------------ Track
    "Chapter thirteen. Since Part one, five years of data":
        "第十三章。从第一部分起，五年的数据一直被封存。现在第一次有策略被打开到这些数据上。",

    "The rules, set in Part one.":
        "规则在第一部分就已定下。<bookmark mark='a'/>从2021年1月到2025年12月的每个月都被封存；它的指纹已被记录，本部分没有任何内容看过它。"
        "<bookmark mark='b'/>一个策略必须在信封打开之前登记：它代码的哈希、它的定义、它的成本模型，以及尝试过多少个版本。<bookmark mark='c'/>"
        "信封只打开一次。用不同代码的第二次打开会被拒绝，而结果无论如何都会被展示。",

    "Ten rows enter the Track Record:":
        "十行进入业绩记录：市场、Fama–French的五个因子和动量，以及AQR的押注低贝塔、质量减垃圾、时间序列动量和价值–动量组合。每一个都完全按其作者公布的方式登记，"
        "所以这里没有选择任何参数，每一个计为一次试验。<bookmark mark='a'/>然后信封打开，每一行都用同样的占位成本模型打分，从市场每年二十分之一个百分点到动量的三个百分点，"
        "直到第二十六部分替换它。",

    "Here is the Track Record's first page.":
        "这是业绩记录的第一页。<bookmark mark='a'/>左边是每个因子在研究窗口中的夏普比率及其标准误。<bookmark mark='b'/>右边是它在封存的五年里的表现："
        "年收益、夏普比率、最差回撤，以及扣除占位成本后的夏普比率。注意标准误：在很长的研究样本中约为七分之一，在五年里接近一半。"
        "五年无法把一半的夏普比率与零区分开。",

    "As a picture: pale bars for the research window":
        "画成图：浅色的条是研究窗口，深色的条是封存的年份，附一个标准误。<bookmark mark='a'/>市场比它的历史表现更好，价值和盈利能力也是，"
        "价值在五年里反弹了百分之四十多。<bookmark mark='b'/>规模每年都在亏损。动量、投资、押注低贝塔和质量赚得很少，时间序列动量远低于它的历史。"
        "<bookmark mark='c'/>价值–动量组合几乎和以往一模一样。平均而言，夏普比率从约零点六降到三分之一。",

    "Year by year, a few rows.":
        "逐年看几行。<bookmark mark='a'/>2022年是决定性的一年：随着利率上升，市场下跌百分之二十一，价值上涨百分之三十二，动量百分之二十，"
        "时间序列动量百分之二十五，它做空了价格正在下跌的债券。<bookmark mark='b'/>2023年市场上涨五分之一，价值、动量和趋势全都亏损。"
        "规模在五年中的每一年都在亏损。一个因子的五年只是几次抽样，每一次都由那一年的一个大主题主导。",

    "How to read it honestly.":
        "如何诚实地解读。<bookmark mark='a'/>因子衰减了，大致如关于发表的研究所预测的：平均夏普比率从约零点六降到三分之一。<bookmark mark='b'/>"
        "但标准误接近一半，没有哪一行与它的历史有显著差异，只有一行明显高于零。五年不足以评判一个因子。<bookmark mark='c'/>真正守住的是分散化："
        "负相关的价值–动量组合再次实现了它的夏普比率，而单个因子散落在它周围。这是值得记住的结果。",

    "And the trial counter, which records":
        "还有试验计数器，它记录本系列尝试过的每一种配置。<bookmark mark='a'/>十次登记，每次一次试验，把它从三百一十五带到三百二十五。每个只算一次，"
        "因为这里没有做任何选择：定义来自它们的作者。<bookmark mark='b'/>但作者们在发表之前尝试了多少个版本？这个问题，因子动物园，就是第二十五部分。",

    # ------------------------------------------------------------------ House
    "Chapter fourteen. The House's twenty-fourth rule":
        "第十四章。House的第二十四条规则，以及它为研究交易台开设的因子库。",

    "The factor library's first sheet.":
        "因子库的第一张表。<bookmark mark='a'/>动量：经典美国因子中最好的夏普比率和最差的偏度，一个月亏损百分之五十三。缩放到固定波动率后，比率更好，尾部温和得多。"
        "价值：十四年的亏损和百分之五十七的回撤。价值和动量，在每个市场中都负相关，组合的夏普比率超过一。以及最初封存的五年：经典因子的平均夏普比率下降了约三分之一，"
        "正如已发表的异象会衰减那样。",

    "Three excerpts from the new library.":
        "新库中的三段摘录。波动率缩放：每个月，因子在过去六个月的已实现波动率，以及目标除以它得到的头寸，上限为三。因子动量：每个因子过去一年的复合收益及其符号。"
        "还有回撤：路径的滚动高点，以及路径已跌到它下方多远。每一段都只用当时已知的信息，这就是House的第一条规则在起作用。之所以有回撤，"
        "是因为本部分最重要的数字都不是平均值：它们是最差的月份、最差的十年，以及下跌的深度。",

    "The library, on the research desk.":
        "研究交易台上的因子库。<bookmark mark='a'/>统计量与回撤；阿尔法、张成检验和联合检验；Fama–French的构造；动量的崩盘，测量并加以缓和；择时和默认账簿；"
        "股利贴现模型给出的因子存在的理由；以及业绩记录本身。<bookmark mark='b'/>还有第二十四条规则。House持有的每一个因子都按公布的方式定义，在看到数据之前。"
        "它由整条路径来评判，它最差的月份、最差的十年，以及它崩盘的状态，而不是由它的平均值。它被放在一个分散的账簿中持有，按风险确定规模，只在边际上择时。"
        "并且它在业绩记录上只打分一次，无论结果如何。",

    "Hold the rule against this part's cases.":
        "用本部分的案例检验这条规则。<bookmark mark='a'/>2009年春天的动量：按崩盘状态来评判，熊市之后负一的贝塔是看得见的，而按风险确定规模，它的头寸早已减半。"
        "<bookmark mark='b'/>价值失去的十年：在分散的账簿里，它是拖累而不是毁灭，而一个事先被告知会有十年跟踪误差的客户也许会留下来。<bookmark mark='c'/>"
        "规模被发现之后：按公布的方式定义并诚实打分，它的下降就记录在案。<bookmark mark='d'/>还有绿色收益：在一个特征变流行期间测得的溢价是一次重新定价，"
        "规则要求先给出理由。这些都不能预测接下来的五年。它们决定的是House能在那五年里承受住什么。",

    # ------------------------------------------------------------------ Outro
    "Part twenty-four in fourteen lines.":
        "用十四行回顾第24部分。1963年的六美元变成了四到四十美元。每个因子模型都被联合检验拒绝，有用的问题是拒绝的程度：规模和价值把CAPM的定价误差减半。"
        "规模和价值用二乘三排序构造，两者在发表后都赚得更少。动量是最强的经典因子，在股票中如此，作为趋势在每个资产类别中也是如此。它在熊市后的反弹中崩盘，"
        "那时它做空的是贝塔最高的股票，而按波动率缩放能驯服崩盘。盈利能力和投资来自股利贴现模型，并让价值变得多余。低风险股票赚得和高风险股票一样多。",

    "Value and momentum work in every market":
        "价值和动量在每个市场都有效，并且相互对冲，套息和质量也能推广。价值连亏十四年，它的价差在研究窗口结束时接近历史纪录。绿色股票可以在预期收益更低的同时跑赢。"
        "择时信号很弱，持有全部胜过择时。中国需要自己的因子。行业把因子作为倾斜来出售，附带跟踪误差和成本。业绩记录开启了：经典因子衰减了，大致如已发表的异象那样，"
        "而分散的组合守住了。",

    "Six desk questions. Why hold both value and momentum?":
        "六个交易台问题。为什么同时持有价值和动量？因为两者都有回报，而且相互对冲：组合的夏普比率接近任何一个的两倍，只有在两者一起下跌时才令人失望。"
        "<bookmark mark='a'/>一个被拒绝但定价误差很小的模型，可能仍是正确的工具；看看它的误差在哪里。<bookmark mark='b'/>而规模溢价在1981年后的下降，"
        "t统计量只有零点六，无法把死亡与噪声区分开。",

    "After a bear market and a sharp rebound":
        "在熊市和一次急剧反弹之后，减少或对冲动量：它负一的贝塔是一笔没有人选择的赌注。<bookmark mark='a'/>一只不能借钱的养老基金应该买低贝塔股票并加上期货，"
        "这与受约束的投资者通常的做法相反。<bookmark mark='b'/>接近纪录的价值价差会把概率适度地向价值倾斜。完整解答在讲义里。",

    "And ten problems: the GRS statistic as a gain":
        "还有十道习题：GRS统计量作为夏普比率的增量，以及只有一个资产时的情形；手算二乘三排序；股利贴现模型的账面市值比；价值–动量组合；反弹中动量的贝塔；"
        "崩盘中的波动率缩放；手算押注低贝塔；一个因子需要多少年；以及一只绿色股票的实现收益与预期收益。中英文解答都在讲义里。",

    "Where this comes back.":
        "这些内容会在哪里再出现。第二十五部分面对此后发表的数以百计的因子，并问其中有多少是真的。第二十六部分构建带成本和融资的回测，并正式介绍试验计数器。"
        "第二十七部分把这些因子背后的特征交给机器学习。第三十部分把因子账簿作为组合来构建；第三十二部分把趋势和套息作为系统化宏观来运行；"
        "第三十三部分讲述2007年8月的量化地震，那时拥挤的因子组合一起平仓。",

    "The textbooks this part follows, and the papers it draws on":
        "本部分所依据的教科书，以及它引用的论文，从对CAPM的最早检验到因子动量和绿色收益。屏幕上的每个数字都由House的代码根据公开数据算出，示意性的例子都已标明。",

    "The research desk now has a library":
        "研究交易台现在有了一个因子库，业绩记录有了最初的十行。<bookmark mark='a'/>下一部分，第二十五部分：因子动物园。自这些因子之后，又有数以百计的因子被发表。"
        "其中有多少是真的？当成千上万个因子被尝试过之后，t统计量该如何评判？什么能经受住复现？",
}

PHRASES = {}
