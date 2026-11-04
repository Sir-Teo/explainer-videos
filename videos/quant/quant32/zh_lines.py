"""Chinese narration for quant32: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 系统化宏观 (systematic macro), 另类溢价 (alternative premia),
趋势跟踪 (trend following), 时间序列动量 (time-series momentum, TSMOM), 危机阿尔法 (crisis alpha), 微笑曲线 (the
smile), 跨式组合 (straddle), 回望跨式 (lookback straddle), 波动率目标 (volatility targeting), 风险平价 (risk parity),
风险预算 (risk budget), 股债相关性 (stock-bond correlation), 套息 (carry), 展期收益 (roll yield), 升水/期货溢价
(contango), 贴水/现货溢价 (backwardation), 防御 (defensive), 卖出保险 (selling insurance), 月末效应 (turn of the
month), 隔夜收益 (overnight return), 并购套利 (merger arbitrage), 管理期货 (managed futures, CTA)."""

TITLE = '量化金融，从零搭建 · 第32部分：系统化宏观与另类溢价'

CHAPTERS = {
    'Hook': '危机阿尔法',
    'Trend': '1. 趋势跟踪',
    'Smile': '2. 微笑曲线与危机',
    'VolTarget': '3. 波动率目标',
    'RiskParity': '4. 风险平价与股债相关性',
    'Styles': '5. 价值、动量、套息与防御，无处不在',
    'Carry': '6. 看得见的套息',
    'Insurance': '7. 卖出保险',
    'Calendar': '8. 日历、夜晚与事件',
    'Envelope': '9. 趋势组合与风险平价组合，登记并打开',
    'House': '10. 第32条规则：宏观组合',
    'Research': '写给研究者：为什么趋势跟踪是做多跨式组合',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-two. Systematic macro":
        "第32部分。系统化宏观与另类溢价：按规则交易整个资产类别的组合，以及因承担他人想要甩掉的风险而获得的溢价。",

    'f"2008. <bookmark mark=\'a\'/> American stocks lost':
        "2008年。<bookmark mark='a'/>美国股票相对国库券亏损{abs(100 * y['spy']):.0f}%。六成股票、四成国债的平衡组合亏损{abs(100 * y['6040']):.0f}%。"
        "<bookmark mark='b'/>一条只是跟随每个市场趋势、在二十三只基金上做多或做空的规则，赚了{100 * y['trend']:.1f}%。AQR公布的趋势序列覆盖多得多的期货市场，赚了{100 * t['aqr']['y2008']:.0f}%。"
        "<bookmark mark='c'/>业界称之为危机阿尔法。这一部分要问：它是真的吗？为什么会发生？其余时间里它要付出什么代价？",

    "Three questions run through the part.":
        "贯穿这一部分的有三个问题。<bookmark mark='a'/>一条对价值毫无看法的规则，为什么能在崩盘中赚钱，又在其间慢慢吐回去？"
        "<bookmark mark='b'/>为什么加杠杆的债券组合能胜过股票组合？当股票和债券一起下跌时又会怎样？"
        "<bookmark mark='c'/>还有另类溢价：谁在支付它们？他们为什么要继续支付？",

    "What makes a premium alternative?":
        "什么让一种溢价成为“另类”？它是靠一条规则而不是靠持有市场赚到的收益，而且它必须有来源。"
        "<bookmark mark='a'/>风险溢价，是因承担一种在坏时候伤人的风险而获得的报酬。<bookmark mark='b'/>行为溢价，由反应不足或过度外推的投资者支付。"
        "<bookmark mark='c'/>结构性溢价，由那些无论价格如何都必须交易的参与者支付：对冲者、指数基金、养老基金。这一部分的每种溢价都要回答它属于哪一种，因为这决定了它能否存续。",

    "Where this sits. Parts thirty and thirty-one":
        "这一部分在系列中的位置。第30和31部分在单个证券上构建了组合及其风险模型。这一部分上升一个层次，到整个资产类别：股票指数、政府债券、信用、商品和货币，"
        "通过期货和基金交易。第24部分因子动物园的思想在这里以宏观组合的形式重新出现，每一种都有自己的危机。",

    "Richard Donchian ran a public":
        "Richard Donchian在1949年管理一只公开的趋势跟踪基金，买入突破近期高点的品种；Richard Dennis在1983年训练了他的“海龟”；"
        "Michael Adam、David Harding和Martin Lueck在1987年创立了AHL。<bookmark mark='a'/>桥水在1996年为Ray Dalio自己的信托推出全天候策略，"
        "Harding在1997年创立Winton，William Fung和David Hsieh在2001年表明趋势跟踪者的收益看起来像回望跨式组合。"
        "<bookmark mark='b'/>随后2008年让危机阿尔法成了推销口号；学者们在2012年命名了时间序列动量，把它追溯到1880年，在每个资产类别中发现了套息，"
        "并在2022年目睹股票和债券一起下跌。",

    "The plan: trend following, built and measured":
        "本部分的安排：趋势跟踪，构建并测量；微笑曲线，以及趋势为何在危机中获利；跨资产的波动率目标；风险平价、它的杠杆，以及六十年的股债相关性；"
        "一个世纪里无处不在的四种另类溢价；在本系列公司自己的基金中测量套息，以及原油价格变成负数的那一天；卖出保险；日历效应与夜晚；"
        "在封存年份上打开的两个组合；以及一个精确恒等式，说明为什么趋势跟踪是做多跨式组合。",

    "In the House, the macro desk":
        "在本系列公司里，第22部分为收益率曲线和基差建立的宏观部门，得到了它的系统化组合，而组合部门学会了把它们放在一起持有。",

    # ------------------------------------------------------------------ Trend
    "Chapter one. Trend following is the oldest":
        "第一章。趋势跟踪是最古老、也最简单的系统化策略：在每一个能交易的市场里，买入一直在涨的，卖出一直在跌的。",

    "The House's panel. <bookmark mark='a'/> Twenty-three":
        "本系列公司的资产面板。<bookmark mark='a'/>二十三只交易所交易基金，代替宏观基金交易的期货：国内外股票指数、三种国债、公司信用、从黄金到天然气的商品，以及七种货币。"
        "从2006年起的日度超额收益，2021到2025年封存。<bookmark mark='b'/>单纯持有它们的体验好坏参半：股票、债券和信用赚了钱；大多数商品和货币没有。",

    "The rule, as Tobias Moskowitz":
        "规则如下，正如Tobias Moskowitz、Yao Hua Ooi和Lasse Pedersen在2012年写下的那样。<bookmark mark='a'/>如果一个市场自身过去一年的超额收益为正就做多，为负就做空。"
        "不是比哪个市场表现最好，像第24部分的动量那样，而是看每个市场相对现金是否表现良好：时间序列动量。"
        "<bookmark mark='b'/>每个仓位按相同风险确定规模，单独来看每年百分之四十，所以平静的货币仓位大，天然气仓位小。"
        "<bookmark mark='c'/>每个市场获得相同的风险预算，每月调仓。<bookmark mark='d'/>整个组合缩放到百分之十的波动率，以便与任何其他组合比较。",

    'f"Over the research years. <bookmark mark=\'a\'/> Stocks rose most':
        "研究年份内。<bookmark mark='a'/>股票涨得最多，风险是两倍。趋势组合在2008年其他一切都下跌时上涨，之后十年大部分时间横盘。"
        "<bookmark mark='b'/>它的夏普比率为{m['sharpe']:.2f}，与股市的{s['sharpe']:.2f}大致相同，低于六四组合的{sx['sharpe']:.2f}，那是对平衡组合很友好的一段时期。"
        "但它与股票的相关性为{t['corr_spy']:+.2f}：一条同样好的收益流，却独立于市场波动。这种独立性正是趋势基金出售的东西。",

    "How sensitive is it to the choices?":
        "它对选择有多敏感？<bookmark mark='a'/>三种回看期和两种信号规模化方式。<bookmark mark='b'/>一个月的趋势在这里几乎没用。三个月和十二个月的有效，而简单的符号规则与更精细的规模化一样好。"
        "<bookmark mark='c'/>六种配置，六种都是试验：登记的是十二个月的符号规则，计数器会为其余五种收费。",

    'f"By asset class.':
        "按资产类别看。<bookmark mark='a'/>信用和商品的趋势最强；股票和债券较弱；货币的夏普比率为{cu:.2f}，这些年里完全没有趋势。"
        "<bookmark mark='b'/>整体比大多数组成部分都好，因为各类别的趋势关联很弱：第31部分意义上的广度，来自在不同时候形成趋势的市场。",

    'f"Is fourteen years enough?':
        "十四年够吗？<bookmark mark='a'/>Brian Hurst、Ooi和Pedersen在六十七个市场上把这个策略重建回1880年，发现它一个十年接一个十年地盈利，穿越战争、萧条和通胀。"
        "<bookmark mark='b'/>AQR公布的序列从1985年起覆盖五十八个期货市场，到2020年的夏普比率为{a['sharpe']:.2f}，未扣费用和成本。"
        "<bookmark mark='c'/>本系列公司的更低：市场更少，货币没有形成趋势，而且2008年之后的十年对每个趋势跟踪者都很艰难。",

    "The firm files. <bookmark mark='a'/> AHL was founded":
        "公司档案。<bookmark mark='a'/>AHL由Michael Adam、David Harding和Martin Lueck于1987年创立，按规则交易期货趋势，后来成为英仕曼集团的一部分，Man AHL是最大的管理期货业务之一。"
        "<bookmark mark='b'/>Harding离开后于1997年创立Winton；多年来它都是最大的趋势跟踪者之一，在2008年之后漫长而平淡的十年后，逐渐从纯趋势转向其他系统化信号。",

    "How a trend fund actually runs.":
        "趋势基金实际上是怎么运作的。<bookmark mark='a'/>它在一百多个市场上交易期货和远期：交易便宜，容易做空，而且是保证金交易，所以现金大多放在国库券里。"
        "<bookmark mark='b'/>十二个月的信号在每个市场每年只换手几次；期货的展期会额外产生交易。<bookmark mark='c'/>而费用很高：历史上是资产的百分之二加利润的百分之二十。"
        "对一个每年比国库券多赚百分之五的组合，这就是大部分收益，所以如今遵循同样规则的更便宜的基金在争夺同一批投资者。",

    "Horizon is the main design choice.":
        "期限是主要的设计选择。<bookmark mark='a'/>快趋势以周计，新危机开始时转向快，但交易频繁，容易被噪声来回打脸；这里一个月的信号几乎没赚钱。"
        "<bookmark mark='b'/>慢趋势以年计，便宜且稳健，但转向迟缓。大多数基金混合多种速度。"
        "<bookmark mark='c'/>证据也很长：Capital Fund Management的Yves Lempérière及其合作者，把跨期限、跨资产类别的趋势利润追溯到1800年。",

    "Pause and predict. A trend book holds twenty-three":
        "暂停一下，预测一下。一个趋势组合持有二十三个市场，每个单独按百分之四十的波动率确定规模，而整体只有百分之十。它的仓位是相关的、不相关的，还是相互抵消的？",

    # ------------------------------------------------------------------ Smile
    "Chapter two. The claim that sells":
        "第二章。推销趋势跟踪的说法是危机阿尔法。下面是证据、机制和代价。",

    "Each dot is a quarter":
        "每个点是一个季度：横轴是股市收益，纵轴是趋势组合收益。<bookmark mark='a'/>在股票最糟糕的两个季度，2008年最后一个季度和2020年第一个季度，趋势组合都赚了钱。"
        "<bookmark mark='b'/>但用一条曲线拟合全部五十五个季度，著名的微笑在这里很微弱，甚至略微弯向相反方向。第24部分在AQR的五十八个期货市场、三十五年的数据中发现了清晰的微笑。"
        "二十三只基金的十四年不足以看清形状，但足以看清崩盘。",

    "The mechanism is simple.":
        "机制很简单。<bookmark mark='a'/>市场上涨，规则做多。然后它开始下跌。<bookmark mark='b'/>有一段时间规则仍然做多并亏钱；一旦过去的收益转负，它就翻转做空，乘着剩下的跌势而下。"
        "<bookmark mark='c'/>持续数月的崩盘，比如2008年或1973年和2000年的熊市，正是这条规则的用武之地：它需要危机持续得比回看期更久。",

    'f"Year by year.':
        "逐年来看。<bookmark mark='a'/>2008年股票亏损{abs(100 * ys[2008]):.0f}%时，趋势组合获利。2009年股票反弹{100 * ys[2009]:.0f}%，它却亏了：市场转向时它还在做空。"
        "<bookmark mark='b'/>然后是十年的小幅盈利和偶尔的亏损，分别在{neg_mid}和{neg_last}年。没有哪一年是灾难；也很少有令人兴奋的年份。持有它就是这种感觉。",

    "So the claim needs a qualifier.":
        "所以这个说法需要加个限定。<bookmark mark='a'/>趋势在持续数月的慢危机中获利，它们让信号转为做空并保持下去。"
        "<bookmark mark='b'/>它在几天之内的崩盘中不赚钱，比如1987年10月，地板塌陷时它还在做多。"
        "<bookmark mark='c'/>它在反转中亏钱，即它做空时市场转向：2009年，也就是Kent Daniel和Tobias Moskowitz在横截面中称为动量崩溃的同一事件。",

    "There is an exact way to see why.":
        "有一个精确的方式来看清原因。<bookmark mark='a'/>取最纯粹的趋势规则：在一段日子里，持有等于迄今收益的仓位。"
        "<bookmark mark='b'/>它的利润是仓位乘以收益之和，经过一行代数，等于这一段总收益平方的一半，减去日收益平方和的一半。"
        "<bookmark mark='c'/>收益平方的一半是跨式组合的收益：无论哪个方向大幅波动都会赚钱。已实现方差的一半就是跨式组合的成本。趋势跟踪是做多跨式组合，由市场自身的方差来融资，研究章节会证明这意味着什么。",

    "The straddle explains the experience.":
        "跨式组合解释了这种体验。<bookmark mark='a'/>它的买方在风平浪静时付钱，所以趋势在震荡市中一点一点地亏。"
        "<bookmark mark='b'/>许多小亏和少数大赚：正偏度，卖出保险的镜像。<bookmark mark='c'/>William Fung和David Hsieh在2001年正是发现了这一点：趋势跟踪者的收益可以用回望跨式组合解释，即支付一段时间内最大波动的期权，通过交易期货来复制。",

    'f"How investors actually use it: as a diversifier.':
        "投资者实际上如何使用它：作为分散化工具。<bookmark mark='a'/>把六四组合的五分之一移入趋势组合，夏普比率从{sr0:.2f}升到{sr1:.2f}，最大跌幅从{dd0:.0f}%缩小到{dd1:.0f}%。"
        "<bookmark mark='b'/>移入五分之二，最大跌幅进一步缩小。一条不相关、在崩盘中为正的温和收益流，放在组合里比单独持有更有价值。",

    'f"A counter-example worth understanding.':
        "一个值得理解的反例。<bookmark mark='a'/>2020年第一季度是以周计而非以月计的崩盘，然而股票下跌{abs(100 * m[i]):.0f}%时，趋势组合赚了{100 * y[i]:.0f}%。"
        "<bookmark mark='b'/>赚钱的趋势早已就位：做多国债，其收益率已经下降了一年；做空已经走弱的商品。仍在做多的股票仓位亏了。"
        "<bookmark mark='c'/>危机阿尔法来自那些早已朝正确方向形成趋势的市场。它是跨市场的分散化，而不是对崩盘的预测。",

    "Pause and predict. Over a quarter":
        "暂停一下，预测一下。一个季度里，某市场的日收益之和恰好为零，但中间波动很大。线性趋势规则是赚钱还是亏钱？",

    # ------------------------------------------------------------------ VolTarget
    "Chapter three. Every book in this part":
        "第三章。这一部分的每个组合都缩放到目标波动率。这只是风险管理，还是也能赚到什么？",

    "The rule. <bookmark mark='a'/> Hold the target volatility":
        "规则如下。<bookmark mark='a'/>持有目标波动率除以昨天的预测，上限三倍。<bookmark mark='b'/>平静的市场敞口更大，动荡的市场敞口更小。"
        "<bookmark mark='c'/>只有当预期收益跟不上波动率时，它才能赚到什么。第8部分的Merton规则说，持有预期收益除以方差；如果预期收益大致恒定而方差摆动，那么波动率上升时最优敞口就下降。"
        "第8部分在美国市场上检验了九十四年。这里，在二十三种资产上。",

    "What it does, for American stocks":
        "对美国股票、以百分之十五为目标时，它做了什么。<bookmark mark='a'/>波动率预测在2008年、2011年和2020年飙升。"
        "<bookmark mark='b'/>敞口是它的镜像：2008年秋天降到一小部分，2017年的平静中达到三倍上限。每次再平衡都是一笔交易，这些摆动正是真实基金限制杠杆、平滑预测的原因。",

    'f"Nine of the twenty-three.':
        "二十三只中的九只。<bookmark mark='a'/>对美国股票，目标化把夏普比率从{s['raw']['sharpe']:.2f}提高到{s['vt']['sharpe']:.2f}，把最大回撤从{abs(100 * s['raw']['maxdd']):.0f}%降到{abs(100 * s['vt']['maxdd']):.0f}%。"
        "小盘股和新兴市场的夏普比率变差了，但回撤变小。<bookmark mark='b'/>对原油，回撤从{abs(100 * u['raw']['maxdd']):.0f}%降到{abs(100 * u['vt']['maxdd']):.0f}%，夏普比率仍为负：目标化管理风险，但不会在没有溢价的地方创造溢价。",

    'f"In total.':
        "总体而言。<bookmark mark='a'/>目标化提高了{n}只基金中{v['better']}只的夏普比率：不比抛硬币好。"
        "<bookmark mark='b'/>它降低了{v['dd_better']}只的最大回撤，大多是高风险资产：股票、信用和商品，它们的崩盘伴随高波动。对国债和货币，它大多只是在平静的年份增加了杠杆。",

    "The literature agrees with this table.":
        "文献与这张表一致。<bookmark mark='a'/>Alan Moreira和Tyler Muir发现，波动率管理的因子有很大的阿尔法。"
        "<bookmark mark='b'/>Scott Cederburg及其合作者检验了一百零三个策略，发现这些阿尔法在投资者能实时构建的组合中无法存续。"
        "<bookmark mark='c'/>英仕曼集团的Campbell Harvey及其合作者的发现与我们一致：对高风险资产，目标化削减左尾、略有帮助；对债券和货币，作用不大。",

    "Why macro books use it anyway.":
        "为什么宏观组合仍然使用它。<bookmark mark='a'/>跨市场来看，按波动率缩放就是风险预算。"
        "<bookmark mark='b'/>这样一种货币和天然气贡献相同的风险，组合就不只是它最波动的那个市场。"
        "<bookmark mark='c'/>代价是杠杆：资产越平静，达到目标需要的杠杆越多。第四章展示当平静的资产一起不再平静时，杠杆会造成什么。",

    "Why it helps risky assets in particular.":
        "为什么它特别有助于高风险资产。<bookmark mark='a'/>对股票，价格下跌会抬高波动率：第13部分的杠杆效应，而且波动率会聚集。"
        "<bookmark mark='b'/>所以目标化的股票仓位在抛售的头几天就会缩小，赶在最糟的时候之前；这就是回撤变小的来源。"
        "<bookmark mark='c'/>对债券和货币，它们的波动率在上涨和下跌时上升的机会差不多，目标化大多只是在市场平静时增加杠杆。",

    "One more caution: many hands follow this rule.":
        "还有一个警示：很多人都遵循这条规则。<bookmark mark='a'/>波动率控制基金、风险平价组合和趋势跟踪者都在波动率上升时削减敞口，而且衡量方式相似。"
        "<bookmark mark='b'/>在波动率上升时卖出，可能加深导致它的下跌；交易商和监管者曾指出这类规则在2018年2月和2020年3月的抛售中的作用。"
        "<bookmark mark='c'/>补救办法来自第31部分：更平滑的预测、更慢的再平衡，以及对敞口变化速度的限制。",

    "Pause and predict. Suppose an asset's expected return":
        "暂停一下，预测一下。假设一种资产的预期收益与其方差成比例上升。波动率目标会提高还是降低它的夏普比率？",

    # ------------------------------------------------------------------ RiskParity
    "Chapter four. Part thirty met risk parity":
        "第四章。第30部分把风险平价当作行业上的配置规则。这里它是它被发明的本来面目：一种持有整个资产类别的方式，以及一个关于它们如何共同变动的押注。",

    "Start with the balanced portfolio.":
        "从平衡组合开始。<bookmark mark='a'/>按金额，六成股票、四成债券。<bookmark mark='b'/>股票的波动率接近中期国债的三倍，所以按风险算，六四组合约百分之九十四是股票。"
        "<bookmark mark='c'/>它是一个带着缓冲垫的股票组合。金额上分散，风险上集中。",

    "Risk parity turns it around.":
        "风险平价把它倒过来。<bookmark mark='a'/>给每个资产类别相同的风险，而不是相同的金额。<bookmark mark='b'/>结果大部分是债券，而且很平静；要达到投资者想要的波动率，就加杠杆。"
        "<bookmark mark='c'/>为什么这可能赚钱？Cliff Asness、Andrea Frazzini和Lasse Pedersen认为，不能或不愿借钱的投资者通过买股票来获得风险，把股票价格推高，所以安全资产每单位风险提供更多收益：跨资产类别的押注低贝塔。",

    "The firm file. Bridgewater launched All Weather":
        "公司档案。按桥水自己的说法，它在1996年为Ray Dalio自己的信托推出全天候策略，以便在四种经济环境中的任何一种都能挺住：增长上升或下降，通胀上升或下降。"
        "每种环境都有表现好的资产，组合在它们之间平衡风险。后来它接受了养老基金和捐赠基金的资金，2025年与道富合作以交易所交易基金的形式向公众发售。它的弱点是它最不擅长应对的环境：通胀上升而增长下降。",

    'f"The House\'s version, on ten of the funds.':
        "本系列公司的版本，用其中十只基金。<bookmark mark='a'/>按金额，它大部分是债券和信用：每一美元资本对应{tot:.1f}美元的敞口。"
        "<bookmark mark='b'/>按风险，它大致平衡，但不完全：信用承担了{100 * rs['credit']:.0f}%，因为高收益债和公司债实际上与股票同向波动。",

    'f"The leverage dial.':
        "杠杆刻度盘。<bookmark mark='a'/>它随波动率移动：在2008年之后的动荡中降到{r['lev_min']:.2f}，在债券平静时升到{r['lev_max']:.2f}。"
        "<bookmark mark='b'/>杠杆恰恰在资产看起来最安全时上升，而那正是它们的相关性出现意外时伤害最大的时候。",

    'f"And the result, which is not what the brochure says.':
        "而结果并不像宣传册上说的那样。<bookmark mark='a'/>在这十四年里，风险平价的夏普比率为{rp['sharpe']:.2f}，低于六四组合的{sx['sharpe']:.2f}。"
        "它的波动率为{100 * rp['vol']:.1f}%，而目标是百分之十；最大跌幅为{abs(100 * rp['maxdd']):.0f}%。"
        "<bookmark mark='b'/>2008年，加了杠杆的信用与股票一起亏损。而在这些年里，六四组合拥有最好的搭档：每次股票下跌都会上涨的国债。",

    'f"That partnership is younger than most investors think.':
        "这种搭档关系比大多数投资者以为的要年轻。<bookmark mark='a'/>这是自1962年以来，美国股票与十年期国债在滚动三年窗口上的相关性。"
        "<bookmark mark='b'/>在70、80和90年代它是正的：按十年计约为{dec['1970']:+.2f}、{dec['1980']:+.2f}和{dec['1990']:+.2f}。债券和股票一起下跌。"
        "<bookmark mark='c'/>直到2000年之后它才转负，先是{dec['2000']:+.2f}，然后是{dec['2010']:+.2f}。每一个从2000年之后开始的平衡组合和风险平价回测，都建立在这个符号之上。",

    "Why does the sign change?":
        "为什么符号会变？<bookmark mark='a'/>当通胀是主要风险时，通胀上升的消息同时压低债券价格和未来利润的价值，两者一起下跌。"
        "<bookmark mark='b'/>当增长是主要风险时，坏消息同时压低利润和利率，股票下跌时债券上涨。"
        "<bookmark mark='c'/>John Campbell、Adi Sunderam和Luis Viceira表明，名义债券的贝塔随通胀对经济是好消息还是坏消息而变化。风险平价组合加了杠杆，押注这个符号保持为负。封存的年份将检验它。",

    "Leverage is not free.":
        "杠杆不是免费的。<bookmark mark='a'/>每借一美元都要付国库券利率加上一个价差。<bookmark mark='b'/>所以加杠杆组合的夏普比率，等于未加杠杆的夏普比率，减去每单位风险的价差成本。"
        "<bookmark mark='c'/>在两倍杠杆、半个百分点价差、未加杠杆波动率百分之五时，夏普比率下降零点零五。对通过期货融资的机构，这很小；对以零售利率借钱的个人，这就是全部优势。",

    "The four environments, as the firm describes them.":
        "按公司的描述，四种环境如下。<bookmark mark='a'/>增长超预期上升时，股票、信用和商品表现好；超预期下降时，名义债券表现好。"
        "<bookmark mark='b'/>通胀超预期上升时，通胀挂钩债券和商品表现好；超预期下降时，股票和名义债券表现好。给每种环境相同的风险，组合就不必依赖猜测下一个是什么。"
        "只有股票、债券和信用的风险平价组合覆盖了前两种，而暴露于第三种。",

    "Pause and predict. A risk-parity book is levered":
        "暂停一下，预测一下。一个风险平价组合有两倍半的杠杆，大部分是债券。某一年股票跌百分之二十，债券跌百分之十。这个组合大约亏多少？",

    # ------------------------------------------------------------------ Styles
    "Chapter five. Part twenty-four found four styles":
        "第五章。第24部分在个股中发现了四种风格。同样的四种出现在每个资产类别中，合在一起就是多资产基金出售的另类溢价。",

    "The four, as AQR's researchers apply them":
        "这四种风格，按AQR研究员在各资产类别中的用法。它们都是类别内部的多空策略：在市场之间互相排序。"
        "<bookmark mark='a'/>价值：买入相对某个锚点便宜的，比如五年来一直下跌的指数或商品，或低于购买力平价的货币。动量：买入过去一年的相对赢家。"
        "<bookmark mark='b'/>套息：买入价格不动时赚得最多的。防御：买入更安全、更稳定的市场，加杠杆到相同风险。",

    "Carry deserves a definition":
        "套息值得给出定义，因为它把各资产类别统一起来。<bookmark mark='a'/>Ralph Koijen、Tobias Moskowitz、Lasse Pedersen和Evert Vrugt把每个期货收益写成套息，即事先已知的部分，加上现货价格的变化。"
        "<bookmark mark='b'/>对货币，套息是利差。<bookmark mark='c'/>对债券，是收益率高于短期利率的部分加上骑乘收益。"
        "<bookmark mark='d'/>对商品，是现货与期货之间的差距。<bookmark mark='e'/>对股票指数，是股息率高于融资利率的部分。在每个类别中，买入高套息，卖出低套息。",

    'f"Ninety-five years of the four styles':
        "AQR公布的四种风格在各资产类别上九十五年的数据。<bookmark mark='a'/>每种风格的夏普比率大约在零点五到零点七之间。"
        "<bookmark mark='b'/>按等风险合在一起是{ms['sharpe']:.2f}：远超任何单独一种，而波动率只有{100 * ms['vol']:.1f}%。这个差距就是多风格基金的全部商业逻辑，下一张幻灯片解释它。",

    "Their paths. <bookmark mark='a'/> All four rise":
        "它们的路径。<bookmark mark='a'/>四种风格在这个世纪里都上涨了，没有一种是平稳上涨的。"
        "<bookmark mark='b'/>价值在2007年之后赚得很少，2018到2020年什么也没赚，那段时间被媒体称为量化寒冬，个股中的价值跌得最厉害；动量最糟糕的两年是2009年和1932年的急剧反弹。"
        "每种风格都有自己糟糕的十年，而这些糟糕的十年很少重合。",

    'f"The reason is the correlations.':
        "原因在于相关性。<bookmark mark='a'/>在各资产类别上，价值与动量负相关，{vm:+.2f}：一个买跌过的，一个买涨过的，所以一个糟糕的年份往往是另一个的好年份。其他组合接近零。"
        "<bookmark mark='b'/>四个夏普比率相近、平均相关性接近零的策略，合起来约是单个策略夏普比率的两倍：第31部分的基本定律，用在风格上而不是股票上。",

    "The fourth style needs a word":
        "第四种风格值得多说一句，因为它是风险平价的近亲。<bookmark mark='a'/>防御风格在每个类别中买入更安全的市场，加杠杆到相同风险，并卖出风险更高的市场。"
        "<bookmark mark='b'/>Andrea Frazzini和Lasse Pedersen的押注低贝塔解释了它：不能加杠杆的投资者推高了高风险资产的价格，所以安全资产向能加杠杆的人支付更高的单位风险收益。"
        "<bookmark mark='c'/>沿着国债收益率曲线，短期限每单位风险的收益一直高于长期限。防御和风险平价是对同一约束的同一押注，只是形状不同。",

    "And in the worst years for stocks.":
        "再看股票最糟糕的年份。<bookmark mark='a'/>在1926年以来全球股票指数最糟糕的六个日历年里，包括1931、1974、2002和2008年，合成风格大致持平或上涨。"
        "它们不像趋势跟踪那样是对冲工具，但也没有雪上加霜。这是另类溢价被推销的另一个理由。",

    "A striking fact sits under this table.":
        "这张表下面藏着一个惊人的事实。<bookmark mark='a'/>Cliff Asness、Tobias Moskowitz和Lasse Pedersen发现，股票中的价值与债券、货币和商品中的价值相关，动量也是如此，而这些市场之间毫无共同之处。"
        "<bookmark mark='b'/>他们把部分共同变动追溯到融资流动性：融资稀缺时，动量受损，价值获益。"
        "<bookmark mark='c'/>共同因子无法被分散掉，所以合成组合在危机中的表现，取决于融资朝哪个方向变动。",

    "Three cautions. <bookmark mark='a'/> This is a published backtest":
        "三点警示。<bookmark mark='a'/>这是一位管理这些策略的机构公布的回测，未扣费用和成本，早期几十年是用稀薄的数据重建的：是先验，不是业绩记录。"
        "<bookmark mark='b'/>有些溢价是风险的报酬：货币套息会崩盘，正如Markus Brunnermeier、Stefan Nagel和Lasse Pedersen所记录的。"
        "<bookmark mark='c'/>而随着这些风格变成产品，它们的投资者开始持有相同的仓位，这就是第31部分的拥挤，出现在资产类别的层面上。",

    "Pause and predict. Four styles, each with a Sharpe":
        "暂停一下，预测一下。四种风格，夏普比率都是零点六，平均相关性为零。它们的等风险合成能赚多少？如果相关性是零点三呢？",

    # ------------------------------------------------------------------ Carry
    "Chapter six. Carry is the part":
        "第六章。套息是收益中事先就能看到的那部分。在本系列公司自己的资产面板里，可以直接测量它：把每只基金与它跟踪的现货价格对比。",

    "The decomposition.":
        "分解如下。<bookmark mark='a'/>持有期货或存款的基金，赚到现货价格的变化，加上套息，减去费用。"
        "<bookmark mark='b'/>原油基金持有下个月的期货，在到期前卖出；当期货价格高于现货时，每次展期都会损失这个差距。"
        "<bookmark mark='c'/>货币基金持有外币存款，赚取外国利率。所以基金收益减去现货收益，就是测量出来的套息。",

    'f"Oil. <bookmark mark=\'a\'/> The spot price of crude':
        "原油。<bookmark mark='a'/>原油现货价格起起伏伏，期末略低：按对数计每年{100 * u['spot']:+.1f}%。"
        "<bookmark mark='b'/>原油基金每年亏损{abs(100 * u['fund']):.0f}%：每年约{100 * gap:.0f}个百分点的负套息，这是在大多处于期货溢价的市场中展期的成本。"
        "天然气更糟：基金收益每年{100 * g_['fund']:.0f}%，而现货为{100 * g_['spot']:.0f}%。为了持有商品而买这些基金的投资者，实际上持有的是展期。",

    "Why it happens. <bookmark mark='a'/> When storage is plentiful":
        "为什么会这样。<bookmark mark='a'/>储存充裕时，期货价格高于现货，以支付储存和利息：期货溢价，多头持有者会随每份期货向现货收敛而亏损。"
        "<bookmark mark='b'/>供应紧张或生产者大量套期保值时，期货价格低于现货：现货溢价，持有者获得报酬。John Maynard Keynes和John Hicks认为后者是常态，是对冲者支付给投机者的溢价。"
        "商品中的套息策略买入现货溢价的市场，卖出期货溢价的市场。",

    "Bonds have carry too.":
        "债券也有套息。<bookmark mark='a'/>债券赚取收益率高于短期利率的部分，再加上在向上倾斜的曲线上骑乘到更低收益率时的价格收益，第18部分称之为骑乘收益。"
        "<bookmark mark='b'/>所以债券的套息就是曲线的斜率：曲线陡峭时高，倒挂时为负。"
        "<bookmark mark='c'/>跨国家来看，套息交易买入陡峭的曲线、卖出平坦的曲线；在AQR的序列中，它是所有套息中回报最高的，一个世纪的夏普比率约为三分之二。",

    "f'The crisis file. In April 2020":
        "危机档案。2020年4月，需求崩溃，俄克拉荷马州库欣的储罐几近满载，即将到期的5月原油合约结算价为每桶负37.63美元：持有者要付钱才能让别人拿走。"
        "据报道，持有近月期货的原油基金转向了更远期的合约。从3月1日起，它的超额收益最多下跌了{worst:.0f}%。极端的期货溢价，是市场在告诉持有者：原油已无处可放。",

    "Currencies. <bookmark mark='a'/> Subtract the spot rate's change":
        "货币。<bookmark mark='a'/>从每只货币基金相对国库券的收益中减去即期汇率的变化，剩下的就是扣除费用后的利差。"
        "<bookmark mark='b'/>这些年里，只有澳元提供了正套息，每年约一个半百分点。日元、瑞士法郎和欧元的利率低于美国国库券，基金还要收费：负套息。"
        "2008年之后各地利率都接近零，经典的套息交易几乎无利可图。",

    'f"A carry book from the six funds:':
        "用六只基金构建一个套息组合：每月做多过去一年套息最高的两只，做空最低的两只。<bookmark mark='a'/>它一开始就遭遇崩盘：2008年最后一个季度亏损{abs(100 * b['q4_2008']):.0f}%，投资者逃离高收益货币，涌向日元和瑞士法郎。"
        "<bookmark mark='b'/>整个期间，夏普比率为{b['sharpe']:.2f}，偏度为{b['skew']:.2f}。套息是对崩盘风险的报酬，而在这些几乎没有套息可赚的年份里，崩盘就是故事的大部分。",

    "Three lessons. <bookmark mark='a'/> Carry, unlike most premia":
        "三条教训。<bookmark mark='a'/>与大多数溢价不同，套息可以事先看到：在曲线里、利率里、基差里。风险在于它无法控制的价格变化。"
        "<bookmark mark='b'/>套息是顺周期的：在危机中，随着加杠杆的持有者抛售，高套息资产一起下跌；与卖出保险相同的偏度，那是下一章。"
        "<bookmark mark='c'/>套息是许多产品的隐性成本：一只基金可能在它跟踪的东西毫无变化时稳步亏损。",

    "Pause and predict. Oil's one-month future":
        "暂停一下，预测一下。原油一个月期货比五十美元的现货高两美元，现货一年都不动。每月展期的基金大约亏多少？",

    # ------------------------------------------------------------------ Insurance
    "Chapter seven. Parts eleven and twelve":
        "第七章。第11和12部分测量了方差风险溢价：平均而言，期权比随后的波动率更贵。下面是系统化地卖出它们的感受。",

    "Cboe publishes a rule anyone could follow.":
        "Cboe公布了一条任何人都能遵循的规则。<bookmark mark='a'/>每个月卖出一份平值的一个月期标普500看跌期权。"
        "<bookmark mark='b'/>把全部行权价金额放在国库券里作为抵押，所以没有杠杆。<bookmark mark='c'/>赚取国库券利率和权利金，并在指数月末低于月初时支付差额。",

    "Fourteen years. <bookmark mark='a'/> The market":
        "十四年。<bookmark mark='a'/>市场，以及它的两次崩盘。<bookmark mark='b'/>还有看跌期权卖方：一条更平滑的线，月复一月地收取权利金，在崩盘中随市场下跌，回升得更慢，因为看跌期权卖方的上行空间被权利金封顶。",

    'f"The numbers. <bookmark mark=\'a\'/> The put seller had':
        "数字如下。<bookmark mark='a'/>看跌期权卖方的波动率约为市场的四分之三，最大跌幅更小，{abs(100 * p['maxdd']):.0f}%对{abs(100 * m['maxdd']):.0f}%。"
        "<bookmark mark='b'/>但夏普比率更低，{p['sharpe']:.2f}对{m['sharpe']:.2f}，月度偏度为{p['skew']:.2f}，是市场的三倍负：保险卖方的特征。",

    'f"What was it, really?':
        "它到底是什么？<bookmark mark='a'/>把看跌期权卖方对市场回归。<bookmark mark='b'/>贝塔为{v['beta']:.2f}，阿尔法为每年{100 * v['alpha']:+.1f}%：这些年里，卖出看跌期权主要是一种低贝塔的持有市场的方式。"
        "在更长的样本中，这个指数表现更好；这个样本在十四年里有两次崩盘。"
        "<bookmark mark='c'/>Roni Israelov和Lars Nielsen把期权卖出策略分解成几部分：股票贝塔、赚取方差溢价的做空波动率仓位，以及对市场近期方向的无意做空押注。只有中间那部分是溢价。",

    "The crisis file. On the fifth of February 2018":
        "危机档案。2018年2月5日，VIX指数一天之内翻了一倍多。支付VIX期货反向收益、被当作稳定收入卖给公众的交易所交易票据，一夜之间几乎失去全部价值，瑞信终止了它的XIV票据。"
        "这和PUT指数是同一笔交易，只是加了杠杆、每日重置，它展示了这种溢价的形状：多年的小额收益，在一天之内还回去。",

    "Who pays this premium?":
        "谁在支付这种溢价？<bookmark mark='a'/>养老基金、保险公司以及结构化产品背后的交易台，它们几乎不计价格地必须对冲下跌。"
        "<bookmark mark='b'/>Nicolae Gârleanu、Lasse Pedersen和Allen Poteshman说明了价格为何居高不下：吸收这种需求的交易商无法完美对冲，所以需求最大的期权，尤其是指数看跌期权，定价高于其期望收益。"
        "<bookmark mark='c'/>所以这是一种结构性溢价，只要对冲需求还在，它就应该持续。",

    "Put it next to trend following.":
        "把它和趋势跟踪放在一起。<bookmark mark='a'/>卖出保险：许多小赚，少数大亏。<bookmark mark='b'/>趋势跟踪：许多小亏，少数大赚。一个做空跨式，一个做多跨式。"
        "<bookmark mark='c'/>Antti Ilmanen在2012年综述了证据：市场倾向于奖励卖出保险和彩票的人，向买入它们的人收费。同时持有两者的宏观组合，一个付钱给它，另一个为它保险。",

    "Pause and predict. A put seller earns":
        "暂停一下，预测一下。一个看跌期权卖方连续五十个月每月赚百分之一，然后有一个月亏损百分之三十。它的平均月收益是多少？偏度是什么符号？",

    # ------------------------------------------------------------------ Calendar
    "Chapter eight. Some premia are not about":
        "第八章。有些溢价与持有哪种资产无关，而与何时持有有关。日历、时钟和公司事件都会在收益中留下痕迹。",

    'f"The turn of the month.':
        "月末效应。<bookmark mark='a'/>取每个月最后一个交易日和下个月的前三个交易日：约占全部交易日的五分之一。"
        "<bookmark mark='b'/>1926到1962年，它们赚到了市场全部超额收益的{100 * a['share_return']:.0f}%；1963到1990年，超过全部，{100 * b['share_return']:.0f}%，因为其他日子平均是亏钱的。"
        "<bookmark mark='c'/>1991年以来效应缩小了：{100 * cc['share_days']:.0f}%的日子贡献了{100 * cc['share_return']:.0f}%的收益。仍然存在，但小得多。",

    "The literature. <bookmark mark='a'/> Robert Ariel":
        "文献如下。<bookmark mark='a'/>Robert Ariel在1987年发现了它，Josef Lakonishok和Seymour Smidt在九十年的道琼斯数据上证实了它。"
        "<bookmark mark='b'/>通常的解释是资金流：工资、养老金缴款和基金流入在月末到达，并在之后几天投资。一个可预测的买家。"
        "<bookmark mark='c'/>而可预测的买家很容易被用期货抢先交易，这是效应缩小的原因之一。",

    'f"The night.':
        "夜晚。把标普500基金的每一天分成两部分：从收盘到第二天早上开盘，以及从开盘到收盘。"
        "<bookmark mark='a'/>自1993年以来，这只基金几乎全部的收益都是在隔夜赚到的：每年{100 * o['mean']:.1f}%，而交易时段只有{100 * i['mean']:.1f}%，几乎所有交易和新闻发布会都发生在交易时段。"
        "<bookmark mark='b'/>隔夜那条线的波动率也更小。",

    "Explanations. <bookmark mark='a'/> Dong Lou":
        "解释如下。<bookmark mark='a'/>Dong Lou、Christopher Polk和Spyros Skouras发现，动量的利润在隔夜累积，而大多数其他异象在日内赚钱，好像不同的客户群在开盘和交易时段内交易。"
        "<bookmark mark='b'/>承担隔夜跳空可能有溢价，因为那时的新闻无法交易。<bookmark mark='c'/>而且这不是白给的钱：只持有夜晚每天需要两笔交易，一年约五百笔，每笔几个基点，成本就吞掉了大部分收益。",

    'f"One more calendar effect, with an old proverb':
        "还有一个日历效应，配着一句老话：五月卖出，远离市场。<bookmark mark='a'/>把每年分成十一月到四月和五月到十月。1963年之前两半接近。"
        "1963到1990年，冬季半年每年赚{bw:.0f}%，夏季半年{bs:.0f}%，差距的t统计量为{bt:.1f}。1991年以来差距更小也更弱，{ct:.1f}。"
        "Sven Bouman和Ben Jacobsen在三十七个市场中的三十六个发现了它。它没有公认的解释，这正是下一张幻灯片的警示适用于它的原因。",

    'f"A newer clock: the Federal Reserve\'s.':
        "一个更新的时钟：美联储的时钟。<bookmark mark='a'/>1994年以来联邦公开市场委员会发布声明的{f['days']}天里，美国市场平均比国库券多赚{f['on']:.0f}个基点，其他日子只有{f['off']:.0f}个。"
        "<bookmark mark='b'/>不到百分之三的日子，却贡献了市场全部超额收益的{100 * f['share']:.0f}%。David Lucca和Emanuel Moench发现，这种漂移大多在公告之前的几个小时到来，而不是之后，没有标准的风险模型能解释这一点。",

    "Event-driven strategies harvest similar flows":
        "事件驱动策略在公司事件周围收割类似的资金流。<bookmark mark='a'/>并购套利在交易宣布后买入收购目标，如果交易完成就赚到价差。"
        "Mark Mitchell和Todd Pulvino发现它的收益看起来像卖出指数看跌期权：平静市场中稳定，市场急跌时与市场相关，因为那正是交易破裂的时候。"
        "<bookmark mark='b'/>指数调整迫使每只指数基金在同一天买入同一只股票；随着交易者学会提前布局，这一效应缩小了。"
        "<bookmark mark='c'/>价格在盈利意外之后会漂移数周，第28部分在文本中读到了同样的延迟。",

    "A warning comes with all of these.":
        "所有这些都伴随着一个警示。<bookmark mark='a'/>研究者可以尝试的日历规则有成千上万条：一周中的哪天、一月中的哪天、节假日、季节。Ryan Sullivan、Allan Timmermann和Halbert White把它们数了一遍。"
        "<bookmark mark='b'/>用第26部分White的现实检验对照这个规则全集，一个世纪道琼斯数据中的大多数日历效应不再显著。"
        "<bookmark mark='c'/>值得相信的那些伴随着机制，一种可预测的资金流，而这个机制也预测了它们的衰退。月末效应有一个机制；公告前漂移有一个候选机制；万圣节效应仍在寻找。"
        "本系列公司把第一个当作溢价，第二个当作问题，第三个当作一次试验。",

    "Pause and predict. An overnight strategy earns":
        "暂停一下，预测一下。一个隔夜策略成本前每年赚百分之十，每年交易五百零四次。每笔交易成本多少时它盈亏平衡？",

    # ------------------------------------------------------------------ Envelope
    "Chapter nine. Two books from this part":
        "第九章。这一部分的两个组合，在信封打开前登记，并在2021到2025年上一次性评判：这几年包含了一代人以来最糟糕的债券市场。",

    'f"The registrations.':
        "登记内容。<bookmark mark='a'/>趋势组合完全按第一章的构建，计入比较过的{nt}种回看期和规模化方式。第四章的风险平价组合，计入{nr}次。两者都是成本前、相对国库券的。"
        "<bookmark mark='b'/>计数器变为{n_now:,}。",

    "The envelope. <bookmark mark='a'/> Five years":
        "打开信封。<bookmark mark='a'/>五年：2021年的繁荣；阴影标出的2022年，通胀达到四十年来最高，美联储加息之快为八十年代初以来之最；以及之后的复苏。"
        "<bookmark mark='b'/>股票最终遥遥领先。趋势组合在2022年其他一切都下跌时上涨。风险平价在2022年跌得最多，之后再也没有恢复研究年份的节奏。",

    'f"The numbers. <bookmark mark=\'a\'/> On the research years the four books':
        "数字如下。<bookmark mark='a'/>在研究年份，四个组合的夏普比率相近。<bookmark mark='b'/>在封存年份，股票为{b['spy']['hold']['sharpe']:.2f}。"
        "趋势组合为{t['hold']['sharpe']:.2f}，标准误为{t['row']['holdout']['sharpe_se']:.2f}：为正，与它的研究期数值或零都无法区分。风险平价为{r['hold']['sharpe']:.2f}。"
        "五年无法按夏普比率给这些组合排名。但能检验每个组合是用来做什么的。",

    'f"2022. <bookmark mark=\'a\'/> Stocks lost':
        "2022年。<bookmark mark='a'/>股票相对国库券亏损{abs(100 * b['spy']['y2022']):.0f}%，六四组合亏损{abs(100 * b['6040']['y2022']):.0f}%，因为它的债券也下跌了。加了债券杠杆的风险平价亏损{abs(100 * b['rp']['y2022']):.0f}%。"
        "<bookmark mark='b'/>趋势组合赚了{100 * b['trend']['y2022']:.0f}%。危机阿尔法，出现在一场持续一整年的危机中：正是第二章所说它需要的那种危机。",

    'f"Where it came from.':
        "它来自哪里。<bookmark mark='a'/>做空债券，收益率全年上升：{100 * by['bonds']:+.0f}%。货币，乘着美元的上涨。信用，随债券一起下跌。"
        "<bookmark mark='b'/>商品贡献不大，而在震荡和反弹中下跌的股票让它亏了一点。这个组合靠做空平衡组合持有的资产赚钱。",

    'f"And the reason risk parity failed.':
        "以及风险平价失败的原因。<bookmark mark='a'/>在研究年份，美国股票与长期国债的日度相关性为{sb['research']:+.2f}。"
        "<bookmark mark='b'/>从2022年起，它每年都是正的：{yrs['2022']:+.2f}、{yrs['2023']:+.2f}、{yrs['2024']:+.2f}、{yrs['2025']:+.2f}。70、80和90年代的符号随着通胀回来了，正如第四章的历史所说的那样。"
        "<bookmark mark='c'/>随着债券波动率上升，规则降低了杠杆，平均降到{lev['mean']:.2f}倍，但那是在亏损已经发生之后。",

    'f"And the use Chapter two proposed':
        "以及第二章提出的用法，在封存年份上。<bookmark mark='a'/>把六四组合的五分之一移入趋势组合：它在2022年的亏损从{y0:.0f}%缩小到{y1:.0f}%，最大跌幅从{d0:.0f}%缩小到{d1:.0f}%，夏普比率从{s0:.2f}变为{s1:.2f}。"
        "分散化工具在它被需要的那一年完成了它的工作。",

    "How to read it. <bookmark mark='a'/> The trend book promised":
        "怎么解读。<bookmark mark='a'/>趋势组合承诺在慢危机中赚钱、在其他时候保持不相关。两者它都做到了。"
        "<bookmark mark='b'/>风险平价假设债券对冲股票。二十年来确实如此；2022年不再如此，而一个加了杠杆的组合对它不擅长的那一种状态毫无防御。"
        "<bookmark mark='c'/>业绩记录保留两行，它们的标准误都大于数值本身。终章会把它们和其他一切一起衡量。",

    "What the macro desk would do next.":
        "宏观部门下一步会做什么。<bookmark mark='a'/>对趋势组合：更多市场、用期货代替基金、混合多种回看期；每一项改变都是一次新试验，在新数据上评判。"
        "<bookmark mark='b'/>对风险平价：在确定杠杆之前，先在正的股债相关性下做压力测试，并给对冲通胀的资产单独的风险预算。"
        "<bookmark mark='c'/>对两者：先报告危机年份，因为这些组合就是为它们而持有的。",

    "Pause and predict. A trend book earned":
        "暂停一下，预测一下。一个趋势组合在五年里的夏普比率为零点二七。如果它真实的夏普比率是零点三，需要多少年才能离零两个标准误？",

    # ------------------------------------------------------------------ House
    "Chapter ten. The House's thirty-second rule":
        "第十章。本系列公司的第32条规则：一个溢价策略在本系列公司持有之前必须展示什么。持有溢价是为了它在坏年份的表现，所以规则首先问的是那些年份，然后才问平均值。",

    "The first sheet. <bookmark mark='a'/> Trend following earned":
        "第一张表。<bookmark mark='a'/>趋势跟踪赚到了温和的夏普比率，并在2008年赚钱。波动率目标降低回撤的次数多于提高收益的次数。"
        "在债券对冲股票的年份，风险平价落后于六四组合，而这个符号以前翻转过。四种风格合起来远好于任何单独一种。卖出看跌期权是带着肥左尾的市场贝塔。"
        "趋势规则的偏度与理论吻合。而在2022年，趋势组合赚钱，风险平价亏钱。",

    'f"How the books sit together.':
        "这些组合如何放在一起。<bookmark mark='a'/>风险平价与六四组合高度相关，{rc:+.2f}：同样资产的不同加权方式。"
        "<bookmark mark='b'/>趋势组合与两者几乎不相关，与六四组合为{tr:+.2f}。这就是为什么本系列公司的宏观部门把趋势放在平衡组合旁边，而不是取而代之："
        "一个是持有资产的溢价，另一个是跟随资产的溢价，它们在不同的年份失败。",

    "Chapter one's rule in eleven lines.":
        "第一章的规则，十一行代码。在每个月末，且仅在月末，回看整个回看窗口；要求九成的日子有数据；取过去收益的符号，或它相对波动率的大小；用百分之四十的风险预算除以资产的波动率；"
        "并持有到下一个月末。其中没有任何东西知道这个资产是什么。",

    "And the research chapter's identity:":
        "还有研究章节的恒等式：把收益切成若干段，持有迄今为止的收益，利润就等于这一段收益平方的一半减去平方和的一半，精确到最后一位。下面一行是这一章为它证明的偏度。",

    "And Chapter four's risk parity at one rebalance.":
        "还有第四章的风险平价，在一次再平衡时。对每个资产类别，类别内按波动率倒数加权；然后把该类别除以它自己的波动率，使每个类别承担相同的风险；"
        "然后在过去一年的协方差上把整个组合缩放到目标，杠杆上限是最后一道防线。相关性假设就藏在协方差估计里，所以一年新的相关性就能推翻它。",

    "The tools this part adds.":
        "这一部分新增的工具。<bookmark mark='a'/>趋势；风险预算；恒等式及其理论；评分；以及一个总收益基金价格的加载器。"
        "<bookmark mark='b'/>还有第32条规则。一个溢价策略只有满足以下条件才能进入本系列公司：展示它在它本应分散的资产最糟糕的年份里的表现；在夏普比率旁边说明它的偏度和最差月份；"
        "写下它的杠杆，以及杠杆所依赖的相关性假设；并解释谁在支付这个溢价、他们为什么会继续支付。",

    "The rule against three cases.":
        "用这条规则检验三个案例。<bookmark mark='a'/>一只卖出波动率的收益型基金：问它最差的月份、偏度，以及它的2008、2018和2020年。"
        "<bookmark mark='b'/>一份回测从2000年开始的风险平价推介：问回测期间的股债相关性是多少，以及它转正时会怎样。"
        "<bookmark mark='c'/>一个三年持平的趋势跟踪者：问这三年里是否有慢危机。在平静市场中买入的跨式组合，本来就应该亏掉它的权利金。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Chapter two showed":
        "写给研究者。第二章给出了一张图和一个恒等式。这一章把恒等式变成定理：趋势规则赚什么、它的收益是什么形状，以及为什么。",

    "The setup. <bookmark mark='a'/> One block of n returns":
        "设定。<bookmark mark='a'/>一段n个收益，一个月或一个季度的日子，标准化为单位波动率。"
        "<bookmark mark='b'/>线性趋势规则持有迄今为止的收益：上涨后做多，下跌后做空，走得越远持仓越多。"
        "<bookmark mark='c'/>它的利润是仓位乘以收益之和。第一章的符号规则是它更粗糙的近亲；这一个可以求解。",

    "Lemma one, the identity.":
        "引理一，恒等式。<bookmark mark='a'/>代入仓位，利润是每个较早收益乘以每个较晚收益之和。<bookmark mark='b'/>这一段总收益的平方，等于平方和加上两倍的这些交叉乘积。"
        "<bookmark mark='c'/>所以利润等于这一段收益平方的一半减去已实现方差的一半，对任何路径都成立：一个以这段自身方差融资的跨式组合。没有假设任何分布。",

    "Lemma two, the mean.":
        "引理二，均值。<bookmark mark='a'/>取期望。<bookmark mark='b'/>对平稳序列，每个滞后k的自协方差出现n减k次，再加上一个与漂移平方有关的项。"
        "<bookmark mark='c'/>对随机游走，自协方差为零，规则只赚到漂移的平方，在一个月里可以忽略不计。趋势跟踪的期望利润就是市场按滞后加权的自相关，别无其他。而偏度，正如我们将看到的，是白送的。",

    "Lemma three, the moments":
        "引理三，矩，针对独立正态收益。<bookmark mark='a'/>利润等于sigma平方乘以标准正态两两乘积之和。"
        "<bookmark mark='b'/>它的二阶矩：两个两两乘积之和相乘，只有当两对相同时期望才非零，所以是n选二。"
        "<bookmark mark='c'/>它的三阶矩：三对只有当每个下标恰好出现两次时期望才非零，而这恰好发生在三对是一个三角形的三条边时。三角形有n选三个，按顺序选边有三的阶乘种方式。",

    "Lemma four, the limit":
        "引理四，极限，所需条件远少于正态性。<bookmark mark='a'/>由中心极限定理，这一段的收益除以它的标准差趋于标准正态。"
        "<bookmark mark='b'/>由大数定律，已实现方差除以它的期望趋于一。<bookmark mark='c'/>把两者代入恒等式，由Slutsky定理，缩放后的利润趋于Z平方减一的一半：同样的平移卡方分布，适用于任何方差有限的独立收益。",

    "The theorem. <bookmark mark='a'/> The profit is a straddle":
        "定理。<bookmark mark='a'/>利润是跨式组合减去已实现方差；它的均值是按滞后加权的自协方差。"
        "<bookmark mark='b'/>在独立正态收益下，它的偏度等于二的二分之三次方乘以n减二，除以n乘n减一的平方根，从两天时的零上升到二倍根号二。"
        "在极限下，利润是自由度为一的平移卡方分布，所以只有当这一段的波动超过一个标准差时它才为正：约百分之三十二的时间。许多小亏，少数大赚，由构造决定，完全不需要自相关。",

    "Checked by simulation.":
        "用模拟检验。<bookmark mark='a'/>对从两天到一年的各段，模拟的偏度遵循定理：两天时为零，十天时超过二，逼近二倍根号二。"
        "<bookmark mark='b'/>赚钱的段所占比例从一半降向百分之三十二。恒等式在浮点数的最后几位上都成立。",

    "The limit law, drawn.":
        "画出极限分布。<bookmark mark='a'/>Z平方减一的一半：亏损有界，不超过这一段方差的一半，约在百分之六十八的段中发生。"
        "<bookmark mark='b'/>收益无界且罕见。这就是买入跨式组合的收益，也是趋势跟踪者的体验：权利金月复一月地悄悄付出，偶尔一次大赚。"
        "Marc Potters和Jean-Philippe Bouchaud在2005年把它写进了标题：趋势跟踪者亏的次数比赚的多。",

    "Here is the smile without noise.":
        "这是没有噪声的微笑。<bookmark mark='a'/>对美国股票，每个点是一个季度的日子：横轴是这一段的标准化收益，纵轴是线性规则的利润。"
        "<bookmark mark='b'/>曲线是S平方减平均已实现方差的一半。每个点恰好落在它自己的抛物线上，平移量就是它自己的已实现方差。"
        "第24部分在AQR数据中发现的相对市场的微笑，就是这条抛物线，因同时持有许多市场而变得模糊。",

    'f"And the twenty-three funds.':
        "再看二十三只基金。<bookmark mark='a'/>汇集每只基金的各段，月度段的偏度为{r21['skew']:.2f}，季度段为{r63['skew']:.2f}，理论值为{r21['theory']:.2f}和{r63['theory']:.2f}；"
        "真实收益有厚尾，使样本偏度带有噪声，但两者都很大且为正。赚钱的段占{100 * r21['win']:.0f}%和{100 * r63['win']:.0f}%，接近百分之三十二的极限。"
        "<bookmark mark='b'/>再看均值：在各基金之间，每只基金的平均利润与其自身自协方差给出的预测的相关性为{r21['corr_mean_pred']:.2f}和{r63['corr_mean_pred']:.2f}。"
        "形成趋势的基金，正是收益有自相关的基金，正如引理二所要求的。",

    'f"Why, then, is the registered book\'s skewness so much smaller?':
        "那么，为什么登记组合的偏度小得多？<bookmark mark='a'/>分散化。独立利润的三阶累积量相加，方差也相加，所以N个相等、独立市场的组合，偏度只有单个的根号N分之一。"
        "<bookmark mark='b'/>对二十三个市场上的月度段，这是{skn:.2f}。<bookmark mark='c'/>登记的组合用符号规则和一年回看期，月度偏度为{t['tsmom_monthly_skew']:.2f}：更小，但仍为正。广度买来夏普比率，卖掉偏度。",

    "And the sign rule of Chapter one?":
        "第一章的符号规则呢？<bookmark mark='a'/>它只取趋势的方向。<bookmark mark='b'/>它的利润大致等于波动的绝对大小，减去每次累计收益穿越零、仓位翻转时的损失：Fung和Hsieh的回望跨式。"
        "<bookmark mark='c'/>一个规则是波动平方上的跨式，另一个是波动绝对值上的跨式。两者都是凸的，都做多伽马，定理的形状在规则变化后保留下来，尽管常数不同。",

    "A generalisation.":
        "一个推广。<bookmark mark='a'/>任何线性趋势滤波器都按滞后给每个过去收益加权：移动平均、指数平均、突破。"
        "<bookmark mark='b'/>它的期望利润是滤波器与自协方差的内积。<bookmark mark='c'/>所以每单位风险最好的滤波器，是与市场自身自协方差结构相匹配的那个。在平稳条件下这有已知答案；难点在于自协方差会变。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>自协方差随状态、拥挤和政策而变；考虑到自身估计误差的最优自适应滤波器尚不可知。"
        "<bookmark mark='b'/>线性规则每天交易；做多跨式策略的最优不交易区间，以及它对偏度的影响，没有闭式解。"
        "<bookmark mark='c'/>以及谁在提供自相关：缓慢移动的资本、平滑利率的央行、对冲者、反应不足的投资者？随着趋势资本增长，它自己的交易可能会抹去它所收割的效应。",

    "Pause and predict. Returns are independent and normal.":
        "暂停一下，预测一下。收益独立且服从正态分布。在一个六十三天的段上，线性规则的期望利润是多少？偏度是多少？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-two in fourteen lines.":
        "用十四行回顾第32部分。二十三只基金上的趋势跟踪赚到了温和的夏普比率，与股票不相关，并在2008年赚钱；一个世纪的证据在更大的广度上说明了同样的事。"
        "它的微笑是慢危机中的危机阿尔法，以及反转中的亏损。波动率目标降低回撤比提高收益更可靠。风险平价用杠杆加债券来平衡风险，只要债券对冲股票就有效，而这种对冲的符号以前变过。"
        "四种风格跨资产类别合在一起，远比分开更有价值。",

    "Selling insurance pays until it does not.":
        "卖出保险一直赚钱，直到不再赚钱。日历效应在有资金流解释时是真实的，被交易后就会消退。在封存年份，趋势组合在2022年赚钱，而风险平价随着股债相关性转正亏得最多。"
        "研究章节证明了趋势规则是做多跨式组合，其偏度为二倍根号二，完全不需要自相关。",

    "Six desk questions.":
        "六个交易台问题。趋势跟踪为什么有正偏度？因为它恰好是做多跨式组合。<bookmark mark='a'/>它的期望收益来自哪里？只来自自相关。"
        "<bookmark mark='b'/>六四组合的风险有多少是股票？约百分之九十四。",

    "Risk parity lost more than sixty-forty in 2022":
        "风险平价在2022年比六四组合亏得多，因为它的杠杆和分散化同时失效。<bookmark mark='a'/>波动率目标只是有时提高夏普比率。"
        "<bookmark mark='b'/>卖出看跌期权的收益型基金必须展示它的偏度和最差月份。完整解答在讲义中。",

    "And twelve problems:":
        "还有十二道习题：六四组合的风险；等风险权重及其杠杆；合成风格；2022年的杠杆亏损；看跌期权卖方的均值与偏度；隔夜策略的盈亏平衡；随机游走下的趋势规则；偏度与分散化；"
        "证明一个夏普比率需要多久；以及收益随方差上升时的波动率目标。然后是两道资格考试题：定理的矩与极限分布，以及最优线性趋势滤波器。中英文解答都在讲义中。",

    "Where this comes back.":
        "这些内容在哪里再次出现。第33部分交易趋势的反面：配对和残差中的均值回归。第34部分走进运营这类组合的公司内部。第41部分回到去杠杆螺旋，包括2022年的英国国债危机。终章会对每一行做紧缩检验。",

    "The textbooks this part follows":
        "这一部分所依据的教科书，以及它引用的论文，从1987年的月末效应到2020年对波动率管理的批评。屏幕上的每个数字都由本系列公司的代码，"
        "从公开的基金价格、FRED、Kenneth French、Cboe和AQR公布的序列计算得出，示意图都有标注。",

    "The House's macro desk now runs":
        "本系列公司的宏观部门现在运行着一个趋势组合和一个风险平价组合，并且知道每一个是为哪种危机准备的。它的溢价来自风险、来自行为，或来自必须交易的参与者，"
        "它学会了问是哪一种，因为答案决定了一种溢价在被人知道之后能否存续。<bookmark mark='a'/>下一部分，第33部分：统计套利。配对、协整、因子模型的残差，以及交易均值回归的数学，那是这一部分所跟随的趋势的镜像。",
}
