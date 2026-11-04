"""Chinese narration for quant25: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 因子动物园 (factor zoo), 多重检验 (multiple testing), 族错误率
(familywise error rate), 错误发现率 (false discovery rate), 逐步下降 (step-down), 抽屉问题 (file drawer), 分岔路径 (forking
paths), 复现 (replication), 开源资产定价 (Open Source Asset Pricing), 经验贝叶斯 (empirical Bayes), 发表偏差 (publication
bias), 数据挖掘 (data mining), 收缩SDF (shrinkage SDF), 岭回归 (ridge), 交叉验证 (cross-validation), 双重选择 (double
selection), 弱因子 (weak factor), 三步估计 (three-pass estimator), 风险溢价PCA (RP-PCA), 工具化PCA (IPCA), 模型平均 (model
averaging), 盈亏平衡成本 (break-even cost)."""

TITLE = '量化金融，从零搭建 · 第25部分：因子动物园'

CHAPTERS = {
    'Hook': '两百枚硬币',
    'Count': '1. 数以百计的因子与上升的门槛',
    'MTest': '2. 多重检验：FWER与FDR',
    'Replicate': '3. 复现与开源资产定价',
    'Decay': '4. 衰减、收缩与发表偏差',
    'Mined': '5. 数据挖掘对同行评审',
    'KNS': '6. 收缩横截面',
    'FGX': '7. 驯服动物园',
    'Weak': '8. 弱因子',
    'PCA': '9. PCA、RP-PCA与IPCA',
    'Models': '10. 比较模型',
    'Track': '11. 收缩SDF，登记并打开',
    'House': '12. 第25条规则：SDF模型',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part twenty-five. The factor zoo:":
        "第25部分。因子动物园：数以百计已发表的跑赢市场的方法，以及如何把少数真实的与大量靠寻找得来的区分开。",

    "Two hundred trading strategies, each with twenty years":
        "两百个交易策略，各有二十年的月度收益，而且每一个都是纯粹的噪声：真实溢价恰好为零。<bookmark mark='a'/>按t统计量排序。大约四十分之一仅凭运气"
        "就越过了教科书上二的门槛，最好的一个t统计量接近三。如果作为作者唯一尝试过的策略发表，它看起来就像一项发现。<bookmark mark='b'/>"
        "金融学检验过的远不止两百个。",

    "Why does this happen in practice?":
        "这在实践中为什么会发生？<bookmark mark='a'/>抽屉问题：失败的策略不会被写成论文，所以读者只看到赢家，看不到它是从哪些输家中被挑出来的。"
        "<bookmark mark='b'/>还有分岔路径：即使是同一个想法也有许多版本，用哪些月份、哪些股票、什么权重、什么滞后，每一个选择都是一次检验，"
        "只是悄悄进行。<bookmark mark='c'/>解药是计数：报告尝试了多少个，并把最好的那个与同样数量的噪声策略中最好的那个比较。",

    "Here is how many predictors of stock returns were published":
        "这是在一个严谨的开源汇编中，逐年发表的股票收益预测变量的数量。<bookmark mark='a'/>1970年代只有几个，到2000年约五十个，到2016年超过两百个。"
        "John Cochrane称之为新因子的动物园。每一个在它的论文里都是显著的；正因如此才被发表。如果我们知道尝试过多少个，又会有多少仍然显著？",

    "The tools came from statistics first":
        "工具首先来自统计学：1979年Sture Holm的逐步下降程序，1995年Yoav Benjamini和Yosef Hochberg的错误发现率，2000年Halbert White针对数据窥探的现实检验。"
        "<bookmark mark='a'/>随着动物园扩大，金融学跟了上来：Cochrane在2011年给它命名，Campbell Harvey、Yan Liu和Heqing Zhu在2016年主张新因子的t统计量"
        "应当超过三。<bookmark mark='b'/>然后是一次处理许多因子的收缩和选择方法、复现研究，以及任何人都能核查的开源数据。",

    "The plan: the best of many noisy strategies":
        "本部分安排：多个噪声策略中最好的一个，以及门槛必须如何随计数上升；三种多重检验的修正方法；动物园能否复现；它衰减了多少、为什么；"
        "挖掘出的信号是否比发表的差；为一次处理数百个因子而构建的四种现代方法；如何比较模型；以及一个收缩贴现因子，登记并在封存的年份上打开。",

    "In the House, the research desk adds":
        "在House里，研究交易台加入了它的第一个收益统计模型：一个同时载荷于整个动物园、向谨慎方向收缩、并通过计算每一次试验来保持诚实的贴现因子。"
        "到本部分结束时，它会被登记，并像第二十四部分的因子那样在封存的年份上打开。",

    # ------------------------------------------------------------------ Count
    "Chapter one. The arithmetic of searching":
        "第一章。寻找的算术，以及它所要求的门槛。",

    "Why the best of two hundred looks good.":
        "为什么两百个中最好的一个看起来不错。如果n个独立策略都没有溢价，每个t统计量都接近标准正态，所有t都低于某个水平c的概率，就是正态概率的n次方。"
        "<bookmark mark='a'/>所以最大的那个随尝试次数增长，增长得很慢，大约是二倍对数n的平方根：十个策略约一点五，一百个约二点五，一千个约三又三分之一。"
        "你找到的最好t统计量衡量的是你搜索得多努力，至少和衡量策略本身一样多。",

    "Put a number on it.":
        "给它一个数字。t统计量为二点九，单独来看，单侧p值约为千分之二。<bookmark mark='a'/>但如果它是n次尝试中最好的，正确的问题是n次中最好的达到二点九"
        "的可能性有多大：一减去所有n个都不到的概率。<bookmark mark='b'/>对两百次独立尝试，约为百分之三十一。这个亮眼的结果，噪声大约三次就能产生一次。"
        "页面上同样的数字，取决于页面没有显示的一个计数，意义完全不同。",

    "Step back and look at a whole field":
        "退一步，像John Ioannidis看医学那样看整个领域。在研究者检验的所有想法中，有一部分是真的。检验以一定的检验力发现真想法，以概率阿尔法误报假想法。"
        "<bookmark mark='a'/>假设十个想法中有一个是真的，检验发现它的机会是一半。那么在所有越过通常门槛的结果中，只有大约一半是真的。把门槛提高到三，"
        "阿尔法降到千分之三：幸存者中约十分之九是真的，代价是漏掉一些真想法。这就是三这个门槛背后的算术。",

    "Simulated, with twenty years of monthly data each.":
        "模拟，每个策略二十年的月度数据。<bookmark mark='a'/>尝试十次，最好的噪声策略t接近一点五；五十次，超过二；两百次，接近二点八，"
        "如果你愿意把亏损的策略反过来叫做做空，则为三。阴影带显示了其中的运气：尝试两百次时，最好的t统计量达到三点五的情况二十次中会出现一次。",

    "Now apply that to the zoo itself.":
        "现在把它用到动物园本身。把迄今发表的每个预测变量计为一次检验，问什么样的t统计量能把出现哪怕一次错误发现的概率保持在百分之五以下。"
        "<bookmark mark='a'/>1980年，有五个预测变量，门槛约为二点五。到2000年，有五十个，超过三。到2016年，有两百个，三点七。而这只是一个下限："
        "它只计入已发表的预测变量，没有计入那数以千计被尝试过又悄悄放弃的。",

    "Campbell Harvey, Yan Liu and Heqing Zhu did this carefully.":
        "Campbell Harvey、Yan Liu和Heqing Zhu仔细地做了这件事。<bookmark mark='a'/>他们统计了到2012年已发表的三百一十六个因子，考虑了它们之间的相关性"
        "以及对从未发表的检验的估计，得出结论：新因子的t统计量应当超过三。<bookmark mark='b'/>不是三点七，因为因子是相关的，而Bonferroni的保证比金融学需要的更严格。"
        "<bookmark mark='c'/>Harvey在他的主席演讲中点明了真正的问题：奖励显著结果的激励，以及产生这些结果的搜索。",

    "Here is the zoo against those hurdles.":
        "这是动物园对照这些门槛的情况。每个预测变量在其论文自己使用的样本中的t统计量，从数据重建。<bookmark mark='a'/>百分之八十七超过二；百分之五十八超过三。"
        "三对动物园来说不是高门槛，因为动物园本来就是靠越过门槛组建起来的：我们看到的是那些发现了东西的论文。本部分其余内容要问的是，那些东西有多少能存活下来。",

    "You test two hundred strategies and report the best":
        "你检验了两百个策略，报告了最好的一个，t统计量为二点九。它诚实计算的p值是多少？计算它需要知道什么？",

    # ------------------------------------------------------------------ MTest
    "Chapter two. Three corrections for many tests":
        "第二章。针对多次检验的三种修正，以及每一种承诺了什么。",

    "The strictest goal: control the familywise error rate":
        "最严格的目标：控制族错误率，即你的发现中哪怕有一个是假的概率。<bookmark mark='a'/>Carlo Bonferroni的答案是把m个假设中的每一个都在阿尔法除以m的水平上检验。"
        "任何一个被错误拒绝的概率至多是各自概率之和，也就是阿尔法，无论检验之间如何相依。<bookmark mark='b'/>对两百一十二个预测变量，这意味着p值低于约万分之二，"
        "t统计量为三点七。安全，但严格到把t统计量不高的真实因子也扔掉了。",

    "Sture Holm improved it for free.":
        "Sture Holm免费地改进了它。把p值从小到大排序。最小的在阿尔法除以m上检验；如果通过，下一个在阿尔法除以m减一上检验，依此类推，在第一个失败处停止。"
        "每次拒绝都从族中去掉一个假设，所以下一个门槛可以低一点。保证与Bonferroni相同，而发现的数量从不更少。",

    "Yoav Benjamini and Yosef Hochberg changed the question.":
        "Yoav Benjamini和Yosef Hochberg改变了问题。不再控制出现任何错误发现的概率，而是控制错误发现率：你的发现中错误所占的预期比例。"
        "一个会依据许多发现行事的领域，可以容忍少数无效的发现，只要它们占比很小。<bookmark mark='a'/>他们的程序：给p值排序，画一条从q除以m上升到q的直线，"
        "拒绝直线下方最后一个之前的所有假设。",

    "The two error rates, in one table.":
        "两种错误率，在一张表里。在m次检验中，有些没有真实溢价，有些有。我们宣布其中R个显著；其中V个是错误发现。<bookmark mark='a'/>族错误率是V至少为一的概率。"
        "错误发现率是V除以R的期望：我们宣布的结果中错误的比例。有数百次检验和许多真实效应时，前者几乎不可能在不丢弃几乎一切的情况下保持很小；后者则可以。",

    "By hand, on five p-values.":
        "手算五个p值。<bookmark mark='a'/>Bonferroni在百分之一检验每一个：两个通过。<bookmark mark='b'/>Holm把最小的在百分之一检验，下一个在百分之一点二五，"
        "第三个在百分之一点六七，第四个在百分之二点五：三个通过，第四个在零点零三处失败。<bookmark mark='c'/>Benjamini和Hochberg把第k小的与百分之k比较："
        "第四个为百分之三，低于它百分之四的线，所以拒绝四个。目标越宽松，发现越多，其中可能为假的也越多。",

    "Here is the procedure on the zoo":
        "这是这个程序在动物园上的应用，用的是一个诚实的检验：每个预测变量在其论文发表后到2020年的收益，按论文声称的方向检验。这些收益是任何作者都不可能看到或挑选的。"
        "<bookmark mark='a'/>最小的八十个p值，排好序。Benjamini–Hochberg线从原点上升，线下最后一个p值是第二十四个。Bonferroni的门槛几乎贴在坐标轴上，"
        "只有少数几个能低于它。两者之间，是研究者愿意犯哪种错误的选择。",

    "The counts. <bookmark mark='a'/> In the original samples":
        "计数。<bookmark mark='a'/>在原始样本中，两百一十二个中有一百八十五个逐一显著，错误发现程序保留了一百八十四个。这是循环论证："
        "这些样本正是发现这些预测变量的地方。<bookmark mark='b'/>发表后，在没有人见过的收益上，五十九个在百分之五水平上逐一显著，二十四个通过错误发现率，"
        "只有七个通过Bonferroni。注意这并不等于说其余的是假的：发表后的样本更短、溢价更小，所以检验的检验力更低。多重检验关乎你能主张什么，而不是什么是真的。",

    "A better hurdle uses the data's own dependence.":
        "更好的门槛利用数据自身的相依性。Halbert White的现实检验减去每个策略的均值，使每个原假设都按构造成立，然后对整月重新抽样，每个策略用同样的月份，"
        "从而保留它们之间的相关性。<bookmark mark='a'/>门槛是重抽样中最佳t统计量的第九十五百分位。相关的策略共享运气，所以门槛比Bonferroni的低，而保证相同。"
        "Joseph Romano和Michael Wolf把它变成逐步下降，就像Holm对Bonferroni所做的那样。",

    "What does q mean in practice?":
        "q在实践中意味着什么？<bookmark mark='a'/>在百分之五时，发表后的二十四个发现中，预期约有一个是假的。<bookmark mark='b'/>更宽松的q，比如五分之一，"
        "会接纳更多候选，其中多达五分之一可能无效。对一个由许多弱信号组成的分散账簿来说，几个无效信号代价很小。对一个集中的押注来说，一个无效信号就是全部代价。"
        "合适的q取决于这些发现将被如何使用。",

    "Which to use? <bookmark mark='a'/> The familywise rate":
        "用哪一个？<bookmark mark='a'/>对你愿意押上声誉的单一主张，用族错误率；对由许多信号组成的组合，用错误发现率，那里少数无效信号只是稀释而不是毁掉组合。"
        "<bookmark mark='b'/>因子是相关的，自助法，从Halbert White到Joseph Romano和Michael Wolf，再到Harvey和Liu，联合重抽样，没那么保守。<bookmark mark='c'/>"
        "而每种方法都需要检验的次数，这只有研究者知道。这就是House要计算自己的试验次数的原因。",

    "You have a hundred candidate signals":
        "你有一百个候选信号，将等权交易其中最好的十个。你应该控制哪种错误率，在什么水平上？",

    # ------------------------------------------------------------------ Replicate
    "Chapter three. Does the zoo replicate?":
        "第三章。动物园能复现吗？两个彼此矛盾的著名答案，以及让任何人都能核查的开放数据。",

    "In 2020 Kewei Hou, Chen Xue and Lu Zhang rebuilt":
        "2020年，Kewei Hou、Chen Xue和Lu Zhang用一个统一的方法重建了四百五十二个异象：用纽约证券交易所的断点，使小股票不占主导，并用市值加权。"
        "<bookmark mark='a'/>百分之六十五达不到二的t统计量，基于交易摩擦的异象几乎全军覆没。门槛为二点八时，百分之八十二失败。看起来，这是一场像心理学那样的复现危机。",

    "Andrew Chen and Tom Zimmermann answered differently.":
        "Andrew Chen和Tom Zimmermann给出了不同的答案。<bookmark mark='a'/>他们为两百多个预测变量发布了开源代码和数据，每一个都完全按原论文的方式重建，"
        "使用论文自己的加权、断点和样本。<bookmark mark='b'/>这把两个被混在一起的问题分开了：论文自己的结果能否重现，以及这个效应能否经受一个统一的保守方法？"
        "<bookmark mark='c'/>这也给了动物园一份任何人都能核查的普查。它就是本部分所用的数据。",

    "What the open-source release contains.":
        "开源发布包含什么。<bookmark mark='a'/>每个预测变量一列月度收益，即完全按其论文构造的多空组合。<bookmark mark='b'/>以及每个预测变量的文档："
        "作者、期刊和年份，论文的样本和报告的t统计量，加权和分位数，数据类别，以及重建与原文不同之处的说明。<bookmark mark='c'/>这足以把每个预测变量"
        "放到它自己的样本内、样本外和发表后窗口里，这就是本部分计算的全部内容。",

    "Here is the first question answered.":
        "第一个问题的答案在这里。每个点是一个预测变量：其论文报告的t统计量，对Chen和Zimmermann重建得到的t统计量。<bookmark mark='a'/>百分之八十八重现了"
        "高于二的t统计量。大多数点落在对角线稍下方，通常约为发表值的十分之九：用今天版本的数据重建，一个信号通常比作者报告的略弱。论文大多描述了数据中存在的东西。"
        "它是否是一种溢价，是另一个问题。",

    "So why did Hou, Xue and Zhang find failure?":
        "那么Hou、Xue和Zhang为什么发现了失败？主要是构造方法。结果取决于信号，也取决于加权、断点、对微盘股的处理、样本和持有期。等权加上用全部股票确定的断点，"
        "让成千上万只微盘股——只占市场价值的几个百分点——主导了结果。用市值加权和交易所断点，许多异象缩向零，尤其是那些基于交易摩擦的，它们存在于最难交易的股票中。",

    "How much do microcaps matter?":
        "微盘股有多重要？Eugene Fama和Kenneth French把它们定义为低于交易所上市股票规模第二十百分位的股票。<bookmark mark='a'/>它们约占全部股票的五分之三，"
        "约占市场价值的百分之三。在等权组合中它们是大部分持仓；按市值加权，它们几乎可以忽略。它们的价差也最宽、借券也最难，所以存在于它们之中的溢价是最难获取的。",

    "Then the counter-argument.":
        "然后是反驳。<bookmark mark='a'/>Theis Jensen、Bryan Kelly和Lasse Pedersen在九十三个国家构造了一百五十三个因子，并建立了一个复现的贝叶斯模型。"
        "以CAPM阿尔法衡量，大多数因子能够复现；它们聚为十三个主题；并且在海外的样本外有效。<bookmark mark='b'/>他们把与Hou、Xue和Zhang的差距归因于检验的选择、"
        "把相关因子当作无关因子的修正，以及门槛。<bookmark mark='c'/>在他们的模型中，许多相关因子都有效，是对其中每一个的证据：一群表亲支持整个家族。"
        "两篇论文都很严谨。它们回答的是不同的问题。",

    "An anomaly has a t-statistic of four equal-weighted":
        "一个异象等权时t统计量为四，按交易所断点市值加权时为一点二。它是真的吗？你会交易它吗？规模多大？",

    # ------------------------------------------------------------------ Decay
    "Chapter four. Part three measured how anomalies decay":
        "第四章。第三部分测量了异象在发表后如何衰减。本章要问，一个统计学家本应预测到其中多少衰减。",

    "Treat each reproduced t-statistic":
        "把每个复现的t统计量看作预测变量的真实强度加上方差为一的噪声。真实强度在动物园中各不相同。<bookmark mark='a'/>那么对一个预测变量真实强度的最佳估计，"
        "会把它的t拉向动物园的平均值，拉的程度取决于离散中有多少是噪声。<bookmark mark='b'/>动物园的t统计量非常分散，方差接近六，所以噪声只占其中六分之一。"
        "仅凭抽样误差，一个预测变量应当保留约百分之八十三的强度。",

    "Two examples. <bookmark mark='a'/> A predictor with a t":
        "两个例子。<bookmark mark='a'/>t统计量为七的预测变量被稍稍拉低，到约六点五。<bookmark mark='b'/>处于边缘的二点五被拉高，拉向动物园接近四的平均值。"
        "以它所来自的动物园衡量，弱结果看起来比实际要好，因为动物园里满是强结果。这是第一个迹象，表明已发表数字周围的噪声不是全部：动物园本身是被选择出来的。",

    "What actually happened.":
        "实际发生了什么。每个预测变量在原始样本中的平均收益，对它发表后到2020年的平均收益。<bookmark mark='a'/>拟合斜率约为零点四，平均值从每月百分之零点七"
        "降到约四分之一个百分点：预测变量保留了百分之三十八的收益，而不是八十三。",

    "Put the two side by side.":
        "把两者并排放。<bookmark mark='a'/>仅凭抽样误差，一个预测变量应保留百分之八十三；数据显示的是三十八。<bookmark mark='b'/>差距需要另一个原因。"
        "超出纯噪声的选择，因为每篇论文都在样本内尝试过不止一种设定。发表后的套利：McLean和Pontiff发现，在交易最便宜的地方衰减最大，相关股票的交易量也在上升。"
        "还有变化的市场：更低的成本、更快的信息，以及更多的量化资金。",

    "David McLean and Jeffrey Pontiff separated the causes":
        "David McLean和Jeffrey Pontiff用一条巧妙的时间线把原因分开了。在论文样本结束到论文发表之间，预测变量处于样本外，但市场仍不知道它。"
        "<bookmark mark='a'/>在这个窗口中，收益比样本内低约四分之一：这就是统计偏差，即选择和噪声。发表后，收益低了百分之五十八。<bookmark mark='b'/>"
        "多出来的三十二个百分点，是发表本身造成的。投资者读了论文，然后交易。",

    "By the kind of data a predictor uses.":
        "按预测变量使用的数据类型来看。<bookmark mark='a'/>只用价格构造的信号，计算和交易都最便宜，保留得最少，不到十分之三。会计和分析师信号保留了三分之一多一点。"
        "少数几个基于机构持仓的信号几乎全部保留，但六个太少，不足为凭。这个规律符合套利：最容易利用的，衰减得最快。",

    "Can publication bias explain the rest?":
        "发表偏差能解释其余部分吗？<bookmark mark='a'/>Chen和Zimmermann对它建模：如果只有t高于二的结果被发表，已发表的t统计量就是一个截断样本。"
        "拟合这种截断，他们发现偏差很小，约为十分之一，因为大多数已发表的t远高于二。<bookmark mark='b'/>所以大部分衰减不是统计假象。发表之后发生了一些事：市场学会了，"
        "并通过交易把溢价消除了。<bookmark mark='c'/>一个实用规则：预期保留一个已发表异象收益的三分之一到一半，这是扣除成本之前。",

    "A new paper reports an anomaly":
        "一篇新论文报告了一个t统计量为三点五、每月百分之零点八的异象。如果从明年开始交易它，你会按什么收益来计划？为什么？",

    # ------------------------------------------------------------------ Mined
    "Chapter five. A test of the whole enterprise":
        "第五章。对整个事业的一次检验：发表的、有理论支持的预测变量，是否比靠蛮力找到的表现更好？",

    "Andrew Chen, Alejandro Lopez-Lira and Tom Zimmermann ran":
        "Andrew Chen、Alejandro Lopez-Lira和Tom Zimmermann做了这个实验。取成对的会计项目，构造每一个比率以及每一个比率的变化：约两万九千个信号，"
        "背后没有任何想法。<bookmark mark='a'/>对每个已发表的预测变量，找出在同样年份会越过t为二的那些挖掘信号：一个没有理论的数据挖掘者本会发表的东西。"
        "然后比较它们各自在样本结束后的表现。",

    "First, what chance alone would give.":
        "首先，仅凭偶然会得到什么。<bookmark mark='a'/>如果这两万九千个信号都没有任何溢价，在任何样本中仍会有约百分之四点五越过t为二：大约一千三百个假阳性。"
        "<bookmark mark='b'/>约八十个会越过三。所以挖掘者的赢家中肯定有许多无效信号。有趣的问题是，在样本外，它们是否比期刊的赢家表现更差。",

    "The answer is uncomfortable.":
        "答案令人不安。<bookmark mark='a'/>样本内可预测性中约有一半在样本外存活，而对同行评审的预测变量和挖掘出的预测变量来说，大约都是这一半。"
        "<bookmark mark='b'/>而且挖掘者先到一步：投资、股票发行和应计项目这些主题，在论文解释它们之前几十年就出现在挖掘信号中了。按这个证据，"
        "同行评审挑选信号的效果，与以二为门槛的蛮力差不多。",

    "A second result. <bookmark mark='a'/> Predictors whose":
        "第二个结果。<bookmark mark='a'/>论文把它们解释为风险补偿的预测变量，并不比其他的表现更好，在一些比较中还更差。<bookmark mark='b'/>"
        "这并不矛盾。真实的错误定价会在被交易时衰减，被贴上风险溢价标签的错误定价也是如此。标签很便宜；样本外收益不便宜。第二十三部分的规则，"
        "即每个溢价都必须说明其理由，仍然成立：理由是House知道要对什么做压力测试的依据，而不是溢价会持续的证明。",

    "Why does mining work at all?":
        "挖掘为什么会有效？Xuemin Yan和Lingling Zheng挖掘了约一万八千个基本面信号，并用自助法计算了仅凭偶然会产生什么。越过高门槛的信号远多于偶然所能解释的。"
        "会计数据确实包含关于未来收益的信息，所以一个细心的数据挖掘者和一个细心的理论家往往会找到同样的东西。数据挖掘不是问题。不计尝试次数的数据挖掘才是。"
        "有了计数，一个挖掘出的信号就可以像任何其他信号一样被评判。",

    "For the research desk. <bookmark mark='a'/> A mined signal":
        "对研究交易台而言。<bookmark mark='a'/>一个挖掘出的信号，如果诚实计数并在样本外检验，与一个已发表的信号是同等质量的证据。<bookmark mark='b'/>"
        "区分它们的是计数：挖掘者知道自己尝试了两万九千个，而论文很少说明它尝试过多少个版本。<bookmark mark='c'/>第二十九部分会构建House自己的阿尔法挖掘器，"
        "它们会把试验计数器推到数以百万计。",

    "A colleague mined ten thousand ratios":
        "一位同事挖掘了一万个比率，找到一个在1980到2000年t统计量为四点五、在2001到2020年为二点四的比率。它是一项发现吗？每个时期应当面对什么门槛？",

    # ------------------------------------------------------------------ KNS
    "Chapter six. Instead of choosing a few factors":
        "第六章。与其挑选几个因子，不如全部使用，然后收缩。",

    "Write Part twenty-three's discount factor":
        "把第二十三部分的贴现因子写成对所有因子同时线性。要精确地为它们定价，就要求它们的平均收益等于它们的协方差乘以载荷b。<bookmark mark='a'/>"
        "直接代入的解又是切点组合：协方差的逆乘以均值。有一百五十四个因子和五百七十六个月，这就是从非常嘈杂的均值估计出的一百五十四个载荷，"
        "而协方差的逆恰恰在风险最小的方向上放大了噪声。",

    "Serhiy Kozak, Stefan Nagel and Shrihari Santosh added a prior":
        "Serhiy Kozak、Stefan Nagel和Shrihari Santosh加入了一个先验：因子的预期收益与其风险成正比，从而使它们的任何组合都不会提供荒谬的高夏普比率。"
        "一个数字kappa，即先验的均方根夏普比率，决定了什么是合理的。<bookmark mark='a'/>b的后验均值是一个岭回归：协方差加上gamma乘以单位矩阵，求逆，再乘以均值。"
        "<bookmark mark='b'/>在主成分中意义很清楚。每个方向的载荷乘以其方差除以方差加gamma。方差小的方向，在那里一个微小的平均收益就意味着巨大的夏普比率，被收缩得最厉害。",

    "Two directions, in numbers.":
        "用数字看两个方向。两者每月都赚千分之二。一个方差为百分之一，另一个是它的百分之一。<bookmark mark='a'/>直接估计的贴现因子在小方向上的载荷多一百倍，"
        "因为同样的均值配上百分之一的方差，夏普比率高十倍。<bookmark mark='b'/>gamma取千分之一时，大方向保留其载荷的十分之九，小方向只保留十一分之一。"
        "收缩恰恰不信任那些建立在极小方差上的高夏普比率，而估计误差就藏在那里。",

    "Choose kappa by cross-validation.":
        "用交叉验证选择kappa。用三分之二的月份拟合，并用留出的三分之一来打分：贴现因子解释了它的平均收益的多少。<bookmark mark='a'/>在样本内，收缩越少，"
        "拟合总是越好，一直升向完美拟合。<bookmark mark='b'/>在样本外，拟合先上升，在每年约为一的先验夏普比率附近达到峰值，解释了留出均值的约百分之三十，"
        "然后随着收缩消失、估计变成嘈杂的切点组合而崩溃。这个形状就是第六部分关于过度拟合的教训，画成了资产定价的版本。",

    "Three details of that cross-validation.":
        "这个交叉验证的三个细节。<bookmark mark='a'/>折是连续月份的分块，而不是随机月份：收益成段聚集，随机月份会把同一场危机同时放进拟合集和检验集。"
        "<bookmark mark='b'/>得分是横截面R方，即贴现因子再现了多少留出的平均收益：这是样本外预测在定价上的对应物。<bookmark mark='c'/>而选择的是二十个网格值中的一个数，"
        "少到交叉验证本身不会严重过度拟合。",

    "What does the chosen discount factor load on?":
        "选中的贴现因子载荷于什么？<bookmark mark='a'/>短期反转遥遥领先，然后是行业动量、一个效率指标、季度盈利能力和中期动量。短期反转每个月都把整个组合换一遍，"
        "所以它的纸面收益是最受交易成本影响的。贴现因子是一个为动物园定价的统计对象。它还不是一只基金。",

    "A test inside the research window:":
        "研究窗口内的一次检验：用1973到2000年拟合，持有到2001到2020年。<bookmark mark='a'/>直接估计的切点组合在样本内声称夏普比率为十五，一个明显的假象，"
        "只保留了约六分之一。收缩贴现因子声称六，保留了约三分之一。等权声称不到三，保留了将近一半。<bookmark mark='b'/>一个组合被优化得越多，回吐得就越多。"
        "然而，在样本外且扣除成本前，优化过的组合在这里仍然胜过等权。动物园的纸面收益非常大，这本身就是一个警告。",

    "Three notes. <bookmark mark='a'/> Kozak, Nagel and Santosh also":
        "三点说明。<bookmark mark='a'/>Kozak、Nagel和Santosh还尝试了L1惩罚，使贴现因子变得稀疏。在原始特征上稀疏，拟合很差；在主成分上稀疏，则有效："
        "少数几个成分承载了它的大部分。<bookmark mark='b'/>这些是纸面收益，许多是等权的、每月调仓、做空微小股票：四的夏普比率是关于数据的陈述，不是关于一只基金的。"
        "<bookmark mark='c'/>House的版本只有一个参数，在研究窗口上从二十个值中选出：计数器上记二十次试验，在第十一章。",

    "Why does ridge shrinkage hurt the in-sample fit":
        "为什么岭收缩会损害样本内拟合却有助于样本外？它最不信任因子空间中的哪些方向？",

    # ------------------------------------------------------------------ FGX
    "Chapter seven. A test for the question":
        "第七章。每个新因子都应该面对的问题的一个检验：它增加了什么？",

    "The right question about a new factor":
        "关于新因子的正确问题，不是它自己的平均收益是否为正。许多新因子的平均收益为正，因为它们与旧因子重叠。问题是，在我们已有的一切之外，贴现因子是否需要它。"
        "<bookmark mark='a'/>在检验资产上，平均收益是对它们与所有因子的协方差的回归。但有数百个候选控制变量时，普通回归失效，而手工挑选控制变量又把搜索问题带了回来。",

    "The lasso selects variables automatically:":
        "lasso自动选择变量：一个绝对值惩罚把大多数系数恰好设为零。但一个lasso不够。它可能会丢掉一个仅因与新因子相关才重要的控制变量，"
        "于是新因子的系数悄悄吸收了缺失控制变量的效应。这就是由算法选出的遗漏变量偏差。",

    "A toy makes the danger concrete.":
        "一个玩具例子让危险变得具体。假设新因子在贴现因子中根本不起作用，但它与资产的协方差和一个起作用的旧因子的协方差有百分之九十的相关性。"
        "<bookmark mark='a'/>一个同时惩罚两者的lasso，可能保留新的、丢掉旧的。于是新因子看起来被定价了，借用了旧因子的溢价。第二步选择正是为此而设："
        "它保留旧因子，因为旧因子能预测新因子的协方差，借来的溢价被还了回去。",

    "Guanhao Feng, Stefano Giglio and Dacheng Xiu used double selection.":
        "Guanhao Feng、Stefano Giglio和Dacheng Xiu使用了双重选择。<bookmark mark='a'/>第一步，把资产的平均收益对它们与动物园的协方差做lasso："
        "哪些旧因子为这些资产定价？<bookmark mark='b'/>第二步，把资产与新因子的协方差对它们与动物园的协方差做lasso：哪些旧因子看起来像新因子？"
        "<bookmark mark='c'/>第三步，把平均收益对新因子的协方差以及两个lasso保留的所有变量做普通回归。新因子上的t统计量于是在选择之后仍然有效。",

    "On the open-source zoo:":
        "在开源动物园上：2011年起发表的二十五个预测变量，每一个都对照2003年前发表的五十三个进行检验，用其余预测变量作为检验资产，1973到2020年。"
        "这是平均收益最大的十二个。<bookmark mark='a'/>大多数自身的t统计量很强。<bookmark mark='b'/>在不加任何控制的情况下问贴现因子是否需要它们，通过的少一些。"
        "<bookmark mark='c'/>用双重选择后，只有少数几个仍然显著。",

    "As a funnel.":
        "画成漏斗。<bookmark mark='a'/>二十五个新预测变量中，二十一个自身有显著的平均收益。如果什么都不控制，十四个看起来能增加贴现因子。双重选择之后，五个。"
        "<bookmark mark='b'/>Feng、Giglio和Xiu在他们自己的数据上发现了同样的结果：给定动物园，大多数最近提出的因子是多余的，只有少数真正的补充。"
        "一个因子可以是真实的，即赚取溢价，却仍然什么也没增加。",

    "What it means. <bookmark mark='a'/> Real is not":
        "这意味着什么。<bookmark mark='a'/>真实不等于新：一个有真实溢价、却被旧因子张成的因子，对已经持有旧因子的投资者毫无增益。<bookmark mark='b'/>"
        "顺序很重要：检验问的是一个因子是否增加了它出现时的那个动物园。<bookmark mark='c'/>对研究交易台而言，每个候选因子在获得自己的一行之前，"
        "都要用选出的控制变量对照House的因子库进行检验。",

    "A new factor has a t-statistic of five on its own":
        "一个新因子自身的t统计量为五，但双重选择后它的贴现因子载荷不显著。检验告诉了你什么？你还会持有它吗？",

    # ------------------------------------------------------------------ Weak
    "Chapter eight. A statistical trap":
        "第八章。藏在第六部分两步回归里的一个统计陷阱：弱因子。",

    "The second pass of a Fama-MacBeth test":
        "Fama–MacBeth检验的第二步，把资产的平均收益对它们估计出的贝塔做回归。如果因子真的推动资产，贝塔就是分散的，斜率即溢价就能被很好地识别。"
        "<bookmark mark='a'/>但如果因子很弱，它真实的贝塔都接近零，估计出的贝塔大多是噪声。斜率变成噪声之比，没有理由接近真实溢价，而通常的标准误严重低估了不确定性。"
        "Raymond Kan和Chu Zhang证明，一个无用的因子可以这样看起来被定价了。",

    "A simulation. Fifty assets, forty years":
        "一个模拟。五十个资产，四十年，一个真实溢价为每月百分之零点五的因子。<bookmark mark='a'/>当因子很强、贝塔在一附近时，两步估计聚集在真值周围。"
        "<bookmark mark='b'/>让同一个因子变弱，贝塔在二十分之一附近，估计值从负零点六散布到正四分之三，中心接近零。两种情况的真值都是同样的百分之零点五。"
        "弱因子的溢价根本无法被这些检验资产识别。",

    "Why toward zero?":
        "为什么偏向零？每个估计出的贝塔是它的真值加噪声。<bookmark mark='a'/>于是第二步的斜率被贝塔离散中真实部分所占的比例所衰减：这就是变量误差，"
        "来自第六部分和第二十四部分的含噪声贝塔。<bookmark mark='b'/>如果真实贝塔在资产间的方差为百分之一、噪声为百分之四，估计的溢价收敛到真值的五分之一。"
        "对弱因子来说，信号很小，噪声占主导。",

    "And a second problem.":
        "还有第二个问题。一个模型很少包含为资产定价的所有因子。如果一个遗漏因子的贝塔与模型中因子的贝塔相关，它的溢价就会泄漏进估计值。"
        "<bookmark mark='a'/>Stefano Giglio和Dacheng Xiu证明，这种偏差不会随着数据增多而消失，而且同一个因子用不同的检验资产会得到不同的溢价。",

    "Their remedy has three passes.":
        "他们的补救有三步。<bookmark mark='a'/>第一步，对一大组检验资产做主成分分析：这些成分张成了推动资产的每一个因子，无论有没有人给它命名。"
        "<bookmark mark='b'/>第二步，为这些成分定价，它们的溢价能被很好地识别，因为它们按构造就是强的。<bookmark mark='c'/>第三步，用这些成分来表示所关心的因子；"
        "它的溢价随之得出。遗漏因子不再被遗漏。Giglio、Xiu和Dake Zhang的后续工作挑选检验资产，使弱因子也能被很好地测量。",

    "Two habits follow.":
        "由此有两个习惯。<bookmark mark='a'/>在估计任何溢价之前，先检查因子是否真的推动检验资产：它的贝塔的离散程度及其t统计量。<bookmark mark='b'/>"
        "对非交易因子，比如消费或通胀，要最为怀疑：它们常常很弱，用组合排序为它们估计出的溢价几乎可以是任何值。第二十三部分的消费模型就是一个例子。",

    "A macro factor's estimated premium":
        "一个宏观因子估计出的溢价为每月百分之零点八，t为二点五，但它在检验组合上的贝塔的t统计量都低于一。你得出什么结论？",

    # ------------------------------------------------------------------ PCA
    "Chapter nine. Let the data find the factors":
        "第九章。让数据自己找出因子：三种方法，以及每一种优化的是什么。",

    "Start with the zoo's covariance.":
        "从动物园的协方差开始。一百五十四个多空组合，但有多少个独立的方向？<bookmark mark='a'/>第一主成分解释了它们方差的三分之一，五个解释三分之二，十个解释四分之三。"
        "动物园表现为少数几个主题加上一条长尾，正如第二十四部分的十三个主题所暗示的那样。",

    "But PCA only looks at variance.":
        "但PCA只看方差。它从不看平均收益，所以可能错过一个波动很小却回报很大的方向，而这正是贴现因子所需要的。<bookmark mark='a'/>Martin Lettau和Markus Pelger"
        "的修正，风险溢价PCA：在取特征向量之前，加上平均收益的外积，用gamma加权。成分现在必须既解释组合如何一起变动，也解释它们平均赚多少。",

    "Look at the first component alone.":
        "单独看第一个成分。普通PCA的第一个成分解释了动物园方差的三分之一，而在样本外它的夏普比率基本为零。它是动物园最大的共同风险，许多多空腿一起移动，"
        "却没有回报。<bookmark mark='a'/>第一个风险溢价成分，向有回报的方向倾斜，单独在样本外的夏普比率就接近十分之九。只靠方差构建的贴现因子，一开始就站错了位置。",

    "Test it out of sample.":
        "在样本外检验。用1973到2000年估计成分，当时把它们组合成切点组合，并持有到2020年。<bookmark mark='a'/>用普通PCA，即使有十个成分，样本外夏普比率仍低于一："
        "方差大的方向不是有回报的方向。<bookmark mark='b'/>用风险溢价PCA，四个成分就超过一点五，五个达到二。少数选得好的方向就捕捉到了动物园收益的大部分。",

    "About gamma.":
        "关于gamma。<bookmark mark='a'/>它是一个旋钮：取负一，就是普通PCA；取得很大，第一个成分就直接指向平均收益本身。Lettau和Pelger用的值约为十。"
        "<bookmark mark='b'/>这里它在看检验期之前就固定为十，没有调参。<bookmark mark='c'/>它之所以有用，是因为尽管每个均值都很嘈杂，但许多组合的均值所指的方向"
        "测量得要准得多，这让溢价很大的弱因子变得可见。",

    "But pricing the whole zoo is harder":
        "但为整个动物园定价，比赚到它最好的组合要难。<bookmark mark='a'/>一百五十四个组合在样本外的均方根阿尔法：没有因子时每年约百分之五；有十个成分时，"
        "用任何一种方法都仍约为四。少数成分捕捉的是动物园最好的组合，而不是每个组合的平均收益。",

    "The third method works with individual stocks.":
        "第三种方法处理个股。Bryan Kelly、Seth Pruitt和Yinan Su的工具化PCA让每只股票的贝塔成为其特征的线性函数，比如规模、价值、动量等，并与潜在因子一起估计。"
        "公司的特征变化时，它的贝塔也随之变化。<bookmark mark='a'/>然后检验特征是否也进入阿尔法，即在风险之外预测收益。他们发现，有五个因子时并非如此："
        "特征就是协方差。这需要本系列所没有的个股数据；第二十七部分会用机器学习回到这个想法。",

    "Two lessons. <bookmark mark='a'/> What the statistics optimise":
        "两个教训。<bookmark mark='a'/>统计方法优化什么，就是什么模型：只看方差，同时看方差和均值，或者用随特征移动的贝塔来看定价误差。<bookmark mark='b'/>"
        "少数成分捕捉了动物园最好的组合，却不能为每个组合定价，这就是新异象不断被发现的原因。",

    "Why can the first principal component of the zoo":
        "为什么解释了动物园三分之一方差的第一主成分，几乎没有平均收益？这对用PCA构建贴现因子意味着什么？",

    # ------------------------------------------------------------------ Models
    "Chapter ten. Not whether a model is true":
        "第十章。不是问一个模型是否为真，而是问几个模型中哪个最好。",

    "Recall Part twenty-four's geometry":
        "回想第二十四部分的几何：一个模型在某些检验资产上的失败程度，恰好等于它们把最佳夏普比率提高到其因子所能达到的水平之上的程度。<bookmark mark='a'/>"
        "Francisco Barillas和Jay Shanken由此得出结论。对于可交易因子，比较两个模型根本不需要检验资产。更好的模型是其因子本身能达到更高平方夏普比率的那个，"
        "因为它留给任何资产去增加的更少。挑选检验资产，你几乎可以让任何模型获胜；这种比较无法被这样操纵。",

    "Why can test assets mislead?":
        "检验资产为什么会误导？<bookmark mark='a'/>当它们由一个模型自己的排序构造时，它们会偏袒这个模型：二十五个规模和价值组合适合三因子模型，因为它的因子就是用同样的排序构造的。"
        "<bookmark mark='b'/>当资产有很强的因子结构时，几乎任何与这个结构相关的因子看起来都能为它们定价，R方很高，正如Lewellen、Nagel和Shanken用故意无意义的因子所展示的。"
        "<bookmark mark='c'/>补救办法是夏普比率比较，以及建模者没有挑选过的检验资产。",

    "The usual suspects, compared that way.":
        "用这种方式比较常见的模型。<bookmark mark='a'/>CAPM在1967到1993年达到的平方夏普比率为十分之一；三因子十分之七；Carhart接近二；五因子接近三；"
        "加入动量三点五；q因子模型四点五；加入预期增长的q5模型为七。<bookmark mark='b'/>在样本外，即1994到2020年，排名基本保持，q5以接近一点五的夏普比率领先。"
        "但回想第二十四部分的第五章：预期增长因子使用了在同一份数据上拟合的预测，这值得怀疑。",

    "Now every model:":
        "现在看每一个模型：十个因子中包含市场的每一个子集，最多六个因子，三百八十二个模型。<bookmark mark='a'/>模型的样本内平方夏普比率与其样本外夏普比率的秩相关约为四分之三。"
        "这种比较不只是在拟合噪声。但榜首挤满了几乎打平的模型，彼此只是把一个盈利能力因子换成另一个，数据无法把它们分开。",

    "The five best in sample.":
        "样本内最好的五个。<bookmark mark='a'/>每一个都混合了各个家族：市场、规模、一个盈利能力因子、一个投资因子，以及预期增长。没有一个已发表的模型进入前五，"
        "但它们的组成部分进入了。最好的模型是现有模型组成的委员会。",

    "Fama and French used the same criterion":
        "Fama和French用同样的标准评价他们自己的模型。在“选择因子”一文中，他们发现加入动量、并用现金流而不是会计盈利来衡量盈利能力，提高了平方夏普比率。"
        "他们也提醒，这样的提高很小，部分是样本内的，正是上面那些几乎打平的结果所要求的那种谨慎。",

    "The Bayesian version gives each model a probability.":
        "贝叶斯版本给每个模型一个概率。Barillas和Shanken以闭式推导了每个模型的边际似然，并对多大的夏普比率是合理的设定先验，又是第六章的kappa。"
        "Svetlana Bryzgalova、Jiantao Huang和Christian Julliard把它推广到五十个因子的所有组合，两千万亿个模型。没有单一模型胜出。"
        "由此得到的贴现因子是稠密的：许多因子，每个权重都很小，只有在对模型取平均时才稳健。",

    "So: <bookmark mark='a'/> compare traded-factor models":
        "所以：<bookmark mark='a'/>用可交易因子模型的因子所能达到的平方夏普比率来比较它们，而不是用建模者挑选的检验资产。<bookmark mark='b'/>"
        "当榜首是一群几乎打平的模型时，对它们取平均，而不是加冕其中一个。这正是第六章的收缩贴现因子所做的。",

    "Model A beats model B on the twenty-five":
        "模型A在二十五个规模和价值组合上胜过模型B，但B的因子能达到更高的平方夏普比率。哪个更好？为什么检验资产会误导？",

    # ------------------------------------------------------------------ Track
    "Chapter eleven. The shrinkage discount factor, committed":
        "第十一章。收缩贴现因子，在打开封存年份之前就已确定。",

    "What is registered.":
        "登记了什么。<bookmark mark='a'/>第六章的贴现因子：一百五十四个预测变量，收缩程度在研究窗口上用交叉验证选出，权重在2020年12月冻结，并缩放到百分之十的波动率。"
        "<bookmark mark='b'/>旁边是一个完全没有估计的基准：所有预测变量等权。<bookmark mark='c'/>尝试了二十个kappa值，所以贴现因子计为二十次试验，基准计为一次。"
        "<bookmark mark='d'/>这个数据版本截止于2023年，所以信封里有三十六个月。策略的一切在读取其中第一个月之前就已固定、计算哈希并记录在案。",

    "Open it. <bookmark mark='a'/> In sample, the discount":
        "打开它。<bookmark mark='a'/>在样本内，贴现因子的夏普比率约为四点五，等权约为二。在封存的年份里，贴现因子在大致等于目标的波动率下每年赚了百分之三十五，"
        "夏普比率约为三；等权赚了百分之七，夏普比率约为二。只有三年数据，标准误约为零点六。动物园的纸面收益加上收缩，在研究窗口关闭之后仍然有效。",

    "The paths. <bookmark mark='a'/> The discount factor rose":
        "路径。<bookmark mark='a'/>贴现因子在三年中每年都上涨，2021和2022年涨得最多，而2022年股市下跌了，它的最差回撤约为百分之五。"
        "等权也稳步上涨，在2023年趋平。",

    "How much cost could it bear?":
        "它能承受多少成本？每年减去一个成本，再重新计算样本外的夏普比率。<bookmark mark='a'/>这条线稳步下降，在每年约百分之三十五处穿过零。听起来空间很大。"
        "实际没有听起来那么大：一百五十四条多空腿，许多在小股票上，有些每月换手，以百分之十的波动率加杠杆，每年的成本完全可能达到资本的百分之几十。"
        "答案取决于本部分还没有测量的数字。",

    "Before anyone gets excited, three caveats.":
        "在任何人兴奋之前，有三个注意事项。<bookmark mark='a'/>这些是纸面收益。许多预测变量是等权的、每月调仓、做空微小股票，而贴现因子最大的载荷是短期反转。"
        "现实的交易成本会去掉其中很大一部分，第二十六部分会收取这些成本。<bookmark mark='b'/>用一百五十四条多空腿达到百分之十的波动率，意味着总头寸是资本的许多倍，"
        "伴随着第二十一和第二十二部分的所有融资和保证金问题。<bookmark mark='c'/>它真正说明的是，这个估计方法，即对整个动物园的收缩，经受住了三个未见过的年份。"
        "这是关于一种方法的证据，还不是关于一只基金的。",

    "One subtle point.":
        "一个微妙之处。<bookmark mark='a'/>样本外的夏普比率不需要多重检验修正：它来自对一份没有任何选择拟合过的数据的一次查看。<bookmark mark='b'/>"
        "研究窗口的四点五确实需要修正：它是在二十个收缩值中选出的，用的预测变量本身也早已被它们的论文选择过。<bookmark mark='c'/>这就是计数器即使对样本外也很重要的原因。"
        "如果House为许多变体打开信封并报告最好的，封存的年份就会变成又一个研究窗口。每次登记只看一次，才能让它们保持干净。",

    "What happens to this row next.":
        "这一行接下来会怎样。<bookmark mark='a'/>第二十六部分用价差、冲击、借券费和融资重新为每条腿定价，一个扣除成本后的行将取代这个纸面行。"
        "<bookmark mark='b'/>第二十七部分用这些预测变量背后的特征构建非线性贴现因子，在同一个信封上打分。<bookmark mark='c'/>第三十部分在杠杆、换手率和容量的限制下，"
        "用一个合适的风险模型，把权重变成头寸。",

    "And the counter. <bookmark mark='a'/> Twenty trials":
        "还有计数器。<bookmark mark='a'/>贴现因子网格的二十次试验，基准的一次：从三百二十五到三百四十六。<bookmark mark='b'/>第二十六部分会把这个计数变成每次回测都需要的修正。",

    # ------------------------------------------------------------------ House
    "Chapter twelve. The House's twenty-fifth rule":
        "第十二章。House的第二十五条规则，以及研究交易台现在保有的贴现因子模型。",

    "Where the count comes from, part by part.":
        "计数从哪里来，逐个部分看。<bookmark mark='a'/>第三部分登记了两百二十二种配置，大多是已发表的预测变量；第六部分五十九种，大多是行业；第七部分十一个波动率模型；"
        "第二十四部分十个因子；本部分二十一个。迄今共三百四十六种配置，每一种都对应一行登记它的代码。研究交易台的主张只有这个数字那么诚实，而它只会上升。",

    "The first sheet. <bookmark mark='a'/> Two hundred noise":
        "第一张表。<bookmark mark='a'/>两百个噪声策略产生接近三的最佳t。动物园自己的Bonferroni门槛是三点七。发表后，五十九个预测变量逐一显著，二十四个通过错误发现率，"
        "七个通过Bonferroni。仅凭噪声，一个预测变量会损失六分之一的强度；发表让它损失了五分之三。二十五个新因子中有五个为动物园增加了东西。"
        "而收缩贴现因子的纸面夏普比率在未见过的年份上从四点五降到三，这是扣除成本之前。",

    "Three excerpts. The shrinkage discount factor:":
        "三段摘录。收缩贴现因子：协方差加上gamma乘以单位矩阵，对均值求解；一行代码，一个参数。风险溢价PCA：二阶矩加上gamma乘以均值的外积，然后取特征向量。"
        "还有双重选择：两个lasso，以及它们保留的并集。每一段都用一条其选择可以被计数的规则取代了研究者的自由裁量：收缩由交叉验证决定，成分由数量决定，"
        "控制变量由事先设定的惩罚决定。",

    "The research desk's new tools.":
        "研究交易台的新工具。<bookmark mark='a'/>多个中最好的一个及其所要求的门槛；逐步下降和错误发现程序；经验贝叶斯收缩；收缩贴现因子；潜在因子与模型比较；"
        "以及双重选择。<bookmark mark='b'/>还有第二十五条规则。每一个关于某个因子是真实的主张，都要说明其背后的检验次数，并越过这个次数所要求的门槛。"
        "每一个新因子在获得一行之前，都要用选出的控制变量对照House的因子库进行检验。预期收益来自对整个因子库收缩后的贴现因子，而不是来自最好的单次回测。"
        "每一个已发表的溢价，都按其报告规模的三分之一到一半来计划，这是扣除成本之前。",

    "Hold the rule against this part's cases.":
        "用本部分的案例检验这条规则。<bookmark mark='a'/>两百次尝试中最好的一个，t为二点九，其诚实的p值接近十分之三：规则在看二点九之前先要那个两百。"
        "<bookmark mark='b'/>一个t为五、却被因子库张成的新因子，得不到一行。<bookmark mark='c'/>一个每月百分之零点八的已发表异象，按它的三分之一到一半来计划。"
        "<bookmark mark='d'/>一个等权的微盘股效应，在任何人相信它之前先用市值加权重建。这些都不需要天才。只需要计数。",

    # ------------------------------------------------------------------ Outro
    "Part twenty-five in fourteen lines.":
        "用十四行回顾第25部分。两百个噪声策略产生接近三的最佳t统计量，因为多个中最好的一个随尝试次数的对数的平方根增长。动物园超过了两百个预测变量，"
        "它自己的Bonferroni门槛升到三点七；Harvey、Liu和Zhu要求三。发表后，四分之一的预测变量逐一显著，八分之一通过错误发现率，七个通过Bonferroni。"
        "动物园能否复现，取决于如何重建它。仅凭噪声，预测变量会保留大部分强度；实际记录只保留了三分之一多一点。挖掘出的信号与发表的表现一样好。"
        "而收缩贴现因子在适度收缩时样本外拟合最好。",

    "Double selection finds that most new factors":
        "双重选择发现，大多数新因子没有为动物园增加任何东西。弱因子的溢价，两步回归无法识别。风险溢价PCA找到了有回报的方向，普通PCA没有。"
        "工具化PCA让贝塔随特征移动。模型最好用其因子达到的夏普比率来比较，而榜首那些几乎打平的模型最好取平均。收缩贴现因子在三个未见过的年份上保留了大部分纸面表现。"
        "而House的规则：计数，越过计数所要求的门槛，对照因子库检验，收缩，并对已发表的结果打折。",

    "Six desk questions. Two hundred noise strategies:":
        "六个交易台问题。两百个噪声策略：预期最佳t约为二点八，如果允许翻转亏损者则为三。<bookmark mark='a'/>报告两百个中最好的一个，t为二点九，其诚实的p值约为十分之三。"
        "<bookmark mark='b'/>交易一百个信号中最好的十个，需要错误发现率：十个中有一个无效信号是稀释而不是毁掉。",

    "An anomaly that lives in equal-weighted microcaps":
        "一个存在于等权微盘股中的异象，可能是真的，却仍无法大规模交易。<bookmark mark='a'/>一篇新论文报告的每月百分之零点八，应按它的三分之一到一半来计划。"
        "<bookmark mark='b'/>而一个被因子库张成的因子，只有作为持有张成它的因子的更便宜方式时才值得持有。完整解答在讲义里。",

    "And ten problems: the distribution of the best of n":
        "还有十道习题：n个中最好者的分布；动物园的Bonferroni；五个p值上的三种程序；经验贝叶斯收缩；主成分中的岭回归，以及它不信任哪个方向；RP-PCA的特例；"
        "弱因子的衰减；Barillas和Shanken的比较；以及数据挖掘者偶然会找到什么。中英文解答都在讲义里。",

    "Where this comes back. Part twenty-six puts":
        "这些内容会在哪里再出现。第二十六部分把试验计数器放进每一次回测，并把它变成紧缩后的夏普比率。第二十七部分把特征交给机器学习的贴现因子。"
        "第二十九部分的阿尔法挖掘器尝试数以百万计的信号，并按计数加以紧缩。第三十部分把贴现因子的权重变成带成本和约束的组合。而终章会用本系列的全部计数紧缩每一行。",

    "The textbooks this part follows, and the papers it draws on, from Holm's":
        "本部分所依据的教科书，以及它引用的论文，从Holm的逐步下降检验到复现之争。屏幕上的每个数字都由House的代码根据公开数据算出，模拟都已标明。"
        "预测变量的收益来自Chen和Zimmermann的开源发布，任何人都可以下载并与这些数字核对。",

    "The research desk has a factor library":
        "研究交易台有了一个因子库、一个贴现因子模型，以及对自己试验次数的计数。它知道，多次尝试中最好的一个看起来比实际要好，已发表的溢价会缩水，"
        "大多数新因子对旧因子没有增益，而对整个动物园收缩后的组合，比任何单个赢家都是更好的猜测。<bookmark mark='a'/>下一部分，第二十六部分：不自欺的回测。"
        "回测说谎的每一种方式，每一种都埋了一个错误等你去找；成本、融资和借券；以及紧缩后的夏普比率。",
}

PHRASES = {}
