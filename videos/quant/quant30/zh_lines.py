"""Chinese narration for quant30: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 误差最大化 (error maximisation), 有效前沿 (efficient frontier),
全局最小方差组合 (global minimum-variance portfolio, GMV), 切点组合 (tangency portfolio), 马尔琴科–帕斯图尔定律
(Marchenko-Pastur law), 特征值裁剪 (eigenvalue clipping), 收缩 (shrinkage), 收缩强度 (shrinkage intensity), 非线性收缩
(nonlinear shrinkage), 先知估计 (oracle), 均衡收益 (equilibrium returns), 风险平价 (risk parity), 等风险贡献 (equal risk
contributions, ERC), 分层风险平价 (hierarchical risk parity, HRP), 条件风险价值 (CVaR), 鲁棒优化 (robust optimisation),
凯利组合 (Kelly portfolio), 通用组合 (universal portfolio), 多样性加权 (diversity weighting), 超额增长率 (excess growth
rate), 熵池化 (entropy pooling), 端到端 (end-to-end), 决策损失 (decision loss), 风险错觉 (risk illusion), Wishart矩阵."""

TITLE = '量化金融，从零搭建 · 第30部分：组合构建'

CHAPTERS = {
    'Hook': '优化器的承诺',
    'Michaud': '1. 误差最大化',
    'OneOverN': '2. 朴素的1/N',
    'Spectrum': '3. 高维中的协方差',
    'Shrink': '4. 收缩：Ledoit与Wolf',
    'Constraints': '5. 约束即收缩',
    'BlackLitterman': '6. Black–Litterman',
    'RiskParity': '7. 风险平价与HRP',
    'CVaR': '8. 鲁棒优化与CVaR',
    'Growth': '9. Kelly、Cover与Fernholz',
    'Views': '10. 熵池化',
    'EndToEnd': '11. 端到端组合',
    'Envelope': '12. 最小方差与HRP，登记并打开',
    'House': '13. 第30条规则：优化器',
    'Research': '写给研究者：优化器为什么低估自己的风险',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty. Portfolio construction":
        "第30部分。组合构建：如何把估计变成权重，为什么优化器会把误差变成信念，以及该怎么办。",

    'f"Give an optimizer five years of data':
        "给一个优化器四十九个行业五年的数据，要求它给出每月赚百分之一的组合。<bookmark mark='a'/>它承诺在{100 * med[2]:.1f}%的波动率下赚到百分之一。"
        "<bookmark mark='b'/>用真实情况来评判，它交付的是在{100 * med[0]:.1f}%的波动率下每月{100 * med[1]:.2f}%：大约一半的收益，{ratio:.0f}倍的风险。"
        "算术上没有任何错误。优化器完全按照指令行事，只是用的数字有一点点错。",

    "Where this sits. This part opens the fifth act":
        "本部分的位置。本部分开启第五幕：组合、策略与公司。第四幕追问哪些信号是真的；这一幕追问如何持有它们。第29部分以一条关于估计均值的定理结束；"
        "本部分讲的是估计的协方差，以及那些试图两者都不需要的规则。",

    "Harry Markowitz posed the problem in 1952":
        "Harry Markowitz在1952年提出了这个问题；John Kelly在1956年问了长期的问题；随机矩阵的数学在1967年出现，Robert Merton在1972年以闭式画出了前沿。"
        "<bookmark mark='a'/>然后是清算：Richard Michaud的误差最大化，Cover的通用组合，Black与Litterman的市场先验，以及物理学家清洗相关矩阵。"
        "<bookmark mark='b'/>再然后是现代的回答：作为线性规划的风险，被理解为收缩的约束，Ledoit与Wolf的估计量，令人谦卑的与1/N的较量，分层风险平价，以及非线性收缩。",

    "The plan: why optimizers maximise errors":
        "计划是：为什么优化器会最大化误差，以及1/N如何让它们难堪；随机矩阵理论对协方差矩阵说了什么；收缩，以及为什么约束是伪装的收缩；Black–Litterman、风险平价及其分层的表亲；"
        "鲁棒优化与尾部风险；增长，从Kelly到Cover和Fernholz；对整个分布的观点；一个直接学习权重的网络；两条在密封年份上打开的规则；以及优化器风险错觉的精确大小。",

    "In the House, the portfolio desk gets its optimizer":
        "在本系列公司里，组合交易台有了自己的优化器：知道自己噪声的估计量，需要更少估计的配置规则，以及一条关于任何优化组合必须如何报告自己的规则。",

    # ------------------------------------------------------------------ Michaud
    "Chapter one. Markowitz gave us the recipe in 1952":
        "第一章。Markowitz在1952年给了我们配方：输入预期收益和协方差，最优组合就出来了。优化器会怎样对待输入中的误差？",

    "The recipe.":
        "配方。<bookmark mark='a'/>找到给定均值下风险最小的全额投资组合。<bookmark mark='b'/>拉格朗日乘数以闭式给出权重，而最优组合的集合，即前沿，是一条双曲线。"
        "<bookmark mark='c'/>但均值和协方差是估计出来的，而优化器分辨不出估计和真相。",

    'f"First, how sensitive the recipe is.':
        "首先，这个配方有多敏感。<bookmark mark='a'/>取四十九个行业的最优组合，用它们真实的均值和协方差算出，然后把一个行业，即软件业的预期收益提高{100 * sv['shock_year']:.1f}个百分点每年："
        "这是用五年数据估计的均值的一个标准误。<bookmark mark='b'/>在一个总敞口为{sv['gross0']:.1f}的组合里，权重总共移动了{sv['dw_l1']:.2f}。"
        "<bookmark mark='c'/>软件业自己的权重从{sv['w0_self']:.2f}变为{sv['w0_self'] + sv['dw_self']:.2f}。而五年的数据会在全部四十九个均值上同时留下这么大的误差。",

    "An experiment with a known truth.":
        "一个已知真相的实验。<bookmark mark='a'/>取四十九个美国行业组合，把它们1970到2020年的均值和协方差宣布为真相。这是真实的前沿。"
        "<bookmark mark='b'/>现在从这个真相中抽取五年的收益，做估计，并画出这些估计所隐含的前沿。抽十二次。每一条估计的前沿都远在真实前沿的左边：每一条都以一小部分风险承诺同样的收益。",

    'f"Now ask each estimated optimizer for a portfolio earning one percent a month':
        "现在让每个估计出来的优化器给出每月赚百分之一的组合，再用真相来评判它。<bookmark mark='a'/>红色是每一个承诺的：在{pv:.1f}%的波动率下约百分之一，好过真实前沿所允许的。"
        "<bookmark mark='b'/>青绿色是它交付的：中位数为每月{dm:.2f}%，波动率{dv:.1f}%，是它所承诺风险的{ratio:.0f}倍，并且落在真实前沿之下。"
        "Richard Michaud把均值-方差优化称作误差最大化器：它专门寻找估计最讨喜的资产，而那些恰恰最可能是错的。",

    'f"With twenty years of data instead of five':
        "用二十年而不是五年的数据，这是上一章问题的答案。<bookmark mark='a'/>承诺的波动率向真实值上升，从每月{100 * a[2]:.1f}%到{100 * b[2]:.1f}%，"
        "真实的波动率从{100 * a[0]:.1f}%降到{100 * b[0]:.1f}%。最大的单个权重从{m['sims']['60']['maxw_median']:.2f}缩小到{m['sims']['240']['maxw_median']:.2f}。"
        "四倍的数据大致让损害减半：误差像样本量平方根的倒数那样下降，而二十年已经超过了大多数交易台愿意相信是平稳的长度。",

    'f"Michaud\'s own remedy was resampling.':
        "Michaud自己的药方是重抽样。<bookmark mark='a'/>从你自己的估计中模拟许多可信的数据集，在每一个上优化，再把权重平均。<bookmark mark='b'/>在同样的抽样上，"
        "重抽样组合交付的波动率中位数为每月{100 * mr[0]:.1f}%，而普通优化器为{100 * mp[0]:.1f}%：没有更好。每一次重抽样都从同样有缺陷的估计出发，"
        "平均无法消除它们共有的误差。Bernd Scherer在2002年对重抽样的评述得出了类似的结论。药方必须作用在估计本身上。",

    "Why it happens.":
        "为什么会这样。<bookmark mark='a'/>均值的误差造成的损害最大：Vijay Chopra和William Ziemba发现它们的代价大约是同样大小的方差误差的十倍。"
        "<bookmark mark='b'/>而协方差的逆会乘以它最小特征值的倒数，这些恰恰估计得最差，所以优化器最倚重它知道得最少的那些方向。"
        "<bookmark mark='c'/>在样本内，承诺总是看起来很好。写给研究者的一章精确地衡量它撒了多大的谎。",

    "Pause and predict. With twenty years of data instead of five":
        "暂停，预测一下。用二十年而不是五年的数据，估计的前沿会向真相移动多远？",

    # ------------------------------------------------------------------ 1/N
    "Chapter two. The simplest rule needs no estimates at all":
        "第二章。最简单的规则根本不需要估计：把钱平均分。有没有哪个优化器能在样本外胜过它？",

    "In 2009 Victor DeMiguel, Lorenzo Garlappi and Raman Uppal":
        "2009年，Victor DeMiguel、Lorenzo Garlappi和Raman Uppal进行了第23部分预告过的那场较量。<bookmark mark='a'/>十四个优化器，从普通的样本规则到贝叶斯和带约束的版本，"
        "在七个数据集上与等权比较。没有一个能稳定地胜过1/N。<bookmark mark='b'/>他们的校准是：样本均值-方差规则在二十五个资产时大约需要三千个月的数据才能胜过它，五十个资产时大约六千个月。"
        "那是二百五十年和五百年。",

    'f"Our own contest, on the forty-nine industries':
        "我们自己的较量，在1980到2020年的四十九个行业上，每条规则每月都用过去十年重新估计。<bookmark mark='a'/>1/N的夏普比率为{ew['sharpe']:.2f}。"
        "使用估计均值的样本切点组合是{tan['sharpe']:.2f}，换手率每月{100 * tan['turnover']:.0f}%。<bookmark mark='b'/>忽略均值、最小化方差的规则做得更好："
        "常相关收缩为{lw['sharpe']:.2f}，非线性收缩为{nl['sharpe']:.2f}，波动率远低于1/N。这场较量的教训不是优化失败了，而是估计的均值失败了。",

    'f"Now compare what each rule expected with what it got.':
        "现在比较每条规则预期的和它得到的。<bookmark mark='a'/>空心的柱子是每条规则根据自己的窗口为自己预测的波动率；实心的柱子是它在下一个月实现的。"
        "样本最小方差规则预测{100 * sg['pred_vol']:.1f}%，实际是{100 * sg['vol']:.1f}%。每一条对估计矩阵求逆的规则都低估了自己的风险；收缩过的低估得少一些。写给研究者的一章把这个差距变成一条定理。",

    'f"Costs change the ranking again.':
        "成本再次改变了排名。<bookmark mark='a'/>交易得多的规则要为此付钱。按每交易一美元十个基点计算，收缩的最小方差保留了{lw10:.2f}的夏普比率；按五十个基点，{lw50:.2f}。"
        "未收缩的样本规则每月换手{100 * sg['turnover']:.0f}%，跌到{sg50:.2f}。估计中的噪声出现了两次：一次在权重里，一次在跟随权重跳动所需的交易里。",

    'f"And the window matters most for the rule that shrinks nothing.':
        "而窗口对什么都不收缩的规则影响最大。<bookmark mark='a'/>四十九个行业、五年的数据时，样本最小方差规则实现的波动率是{100 * sa:.1f}%；十年时是{100 * sb:.1f}%。"
        "收缩的版本几乎不在乎：{100 * la:.1f}%和{100 * lb:.1f}%。收缩让交易台可以用一个短而新的窗口，而不会因此受罚。",

    "If neither the optimizer nor one over N is right, combine them.":
        "如果优化器和1/N都不对，就把它们结合起来。<bookmark mark='a'/>Raymond Kan和周国富在2007年提出了三基金规则：现金、估计的切点组合和估计的最小方差组合，按最小化估计误差预期损失的方式混合。"
        "<bookmark mark='b'/>Jun Tu和周国富随后把一个优化器直接与1/N结合，混合权重由数据选定。<bookmark mark='c'/>贯穿整个部分的共同线索是：每一种修正都是把某样东西朝更简单的东西收缩，"
        "无论是均值、协方差，还是权重本身。",

    "Pause and predict. One over N has no estimation error.":
        "暂停，预测一下。1/N没有估计误差。它错在哪里？什么时候这代价最大？",

    # ------------------------------------------------------------------ Spectrum
    "f'Chapter three. A covariance matrix of forty-nine industries":
        "第三章。一个四十九个行业的协方差矩阵有{n_par:,}个不同的数字，从几年的数据中估计出来。其中有多少是噪声？",

    'f"Random matrix theory answers it.':
        "随机矩阵理论回答了这个问题。<bookmark mark='a'/>取N个真正相互独立的序列，每个T个观测，构成它们的样本相关矩阵。<bookmark mark='b'/>Vladimir Marchenko和Leonid Pastur在1967年证明，"
        "它的特征值并不落在真相所在的一处：它们以已知的密度分布在一个已知的区间上，N相对T越大，区间越宽。<bookmark mark='c'/>对于{N}个序列和一年的日度数据，"
        "单是纯噪声就会让特征值分布在大约{lo:.1f}到大约{hi:.1f}之间。",

    'f"Now the industries, a year of daily returns from {year}.':
        "现在看行业，{year}年一年的日收益。<bookmark mark='a'/>首先是对照：把每个序列在时间上打乱，这会破坏所有相关性，但保留每个行业的收益。它的特征值几乎完全落在马尔琴科–帕斯图尔定律上。"
        "<bookmark mark='b'/>真实的特征值大多也落在同一个带内，这意味着它们与噪声无法区分。只有{y['n_above']}个越过了边界，其中一个极大：{lam[0]:.1f}，远在这根坐标轴之外，"
        "承载了全部方差的{100 * y['share1']:.0f}%。那就是市场：它一动，每个行业都跟着动。",

    "So the spectrum has three parts.":
        "所以谱有三个部分。<bookmark mark='a'/>市场模态，它的特征向量大致等量地持有每个行业。<bookmark mark='b'/>刚好在边界之上的几个板块模态。<bookmark mark='c'/>以及主体，它可能是噪声。"
        "优化器要对矩阵求逆，所以它倚重最小的特征值，而随机矩阵理论说，那些恰恰是被噪声压得最低的。",

    'f"Look inside the two modes that escaped the noise':
        "看看2019年逃出噪声的那两个模态的内部。<bookmark mark='a'/>最大特征向量的载荷：几乎每个行业都接近一除以根号四十九，即那条虚线。它就是市场。"
        "<bookmark mark='b'/>第二个让防御性行业，公用事业、啤酒、软饮料、家庭用品，与周期性行业对立：煤炭、航运、汽车、钢铁。两个方向的真实结构，以及{49 - y['n_above']}个方向的噪声。",

    'f"The market mode is not constant.':
        "市场模态并不恒定。<bookmark mark='a'/>逐年来看最大特征值所承载的方差份额：它在{int(yrs[k08])}年达到峰值{sh[k08]:.0f}%，2019年为{100 * y19['share1']:.0f}%。"
        "在危机中，相关性一起上升，分散化恰恰在需要它的时候消失。",

    'f"A calm year against a crisis year.':
        "一个平静的年份对比一个危机年份。<bookmark mark='a'/>2008年，市场模态膨胀到{b['lam'][0]:.1f}，占全部方差的{100 * b['share1']:.0f}%，而第二个模态缩小了。"
        "在危机中，结构坍缩成单一因子：行业不再是四十九个赌注，而是一个，这恰恰是一个建立在平静年份相关性之上的组合最暴露的时候。",

    "The first remedy follows directly.":
        "第一个药方直接由此而来。<bookmark mark='a'/>把相关矩阵分解为特征值和特征向量。<bookmark mark='b'/>保留噪声边界之上的特征值，把带内的每一个都换成它们的平均值："
        "Laurent Laloux、Pierre Cizeau、Jean-Philippe Bouchaud和Marc Potters，1999年。<bookmark mark='c'/>清洗后的矩阵保留了市场和板块，把其余的当作同一个水平的噪声。"
        "还有更好的清洗方法；下一章会见到最著名的那一个。",

    "Pause and predict. With forty-nine industries and only sixty months":
        "暂停，预测一下。四十九个行业，只有六十个月的数据，噪声带的边界在哪里？",

    # ------------------------------------------------------------------ Shrink (part)
    "Chapter four. The sample covariance spreads its eigenvalues too far apart.":
        "第四章。样本协方差把它的特征值分得太开了。我们应该把它拉回多远，朝向什么？",

    "Shrinkage. <bookmark mark='a'/> Take a weighted average":
        "收缩。<bookmark mark='a'/>取样本矩阵与一个简单目标的加权平均，这个目标因为参数很少，不会错得太离谱。<bookmark mark='b'/>在平方误差意义下，最优的权重是样本矩阵自身的噪声除以它到目标的距离："
        "样本越嘈杂，我们收缩得越多。<bookmark mark='c'/>Olivier Ledoit和Michael Wolf在2004年证明，以缩放的单位矩阵为目标时，两部分都可以从同一份数据中估计，"
        "而估计出的权重在N和T一起增长时收敛到最优值。",
    "Other targets.":
        "其他目标。<bookmark mark='a'/>保留每个方差，把每个相关系数设为平均值：常相关目标，出自Ledoit和Wolf那篇标题令人难忘的论文。<bookmark mark='b'/>或者一个单因子市场模型所隐含的协方差。"
        "<bookmark mark='c'/>每个好的目标都参数很少，所以噪声很小；它的偏差是代价，而最优强度买入的偏差恰好等于它所消除的噪声的价值。",

    "Linear shrinkage moves every eigenvalue by the same rule.":
        "线性收缩按同一条规则移动每个特征值。最著名的改进则不然。<bookmark mark='a'/>保留样本特征向量，选择新的特征值。<bookmark mark='b'/>如果我们知道真相，沿每个特征向量的最优选择就是那个方向上的真实方差。"
        "<bookmark mark='c'/>Ledoit和Wolf在2020年提出的解析非线性收缩，利用随机矩阵理论，仅从样本特征值本身就估计出了这个先知值：每个特征值得到它自己的收缩量。",

    'f"Here is what shrinkage does to the spectrum':
        "这是收缩对谱做的事，在一个模拟的十年窗口里。<bookmark mark='a'/>灰线是真相，红线是样本：顶部太大，底部太小得多，最小的小了{t_lo / s_lo:.1f}倍。"
        "那些最小的特征值是优化器以为几乎没有风险的方向。<bookmark mark='b'/>先知值是样本特征向量所允许的最好结果，它在底部高于真相，因为带噪声的特征向量混入了其他方向的风险。"
        "<bookmark mark='c'/>仅从样本算出的非线性估计量，几乎正好落在先知值上。",

    'f"A horse race, again against a known truth.':
        "一场赛马，同样以已知的真相为准。<bookmark mark='a'/>对每个估计量，构建最小方差组合并测量它的真实方差，表示为可能的最低值的倍数。<bookmark mark='b'/>用五年的数据，"
        "样本矩阵的组合有最小方差的{s60['sample']['gmv']:.1f}倍。收缩把它降到约{s60['LW const-corr']['gmv']:.1f}；非线性估计量降到{s60['nonlinear']['gmv']:.2f}。"
        "窗口越长差距越小，而Ledoit–Wolf估计量从不输。裁剪却可能输：用二十年的数据，它比普通样本矩阵还差，{s['sims']['240']['RMT clipped']['gmv']:.2f}对{s['sims']['240']['sample']['gmv']:.2f}，"
        "因为它扔掉了噪声带内部的真实结构。",

    'f"A third way to tame the matrix is structure.':
        "驯服这个矩阵的第三种方法是结构。<bookmark mark='a'/>假设收益由少数几个共同因子加上独立噪声驱动：那么协方差只需要载荷和每个资产的一个方差，而不是一千二百多个数字。"
        "<bookmark mark='b'/>只有一个因子，即市场模态时，它就是Ledoit和Wolf用作目标的单指数模型。<bookmark mark='c'/>在行业上，用单因子协方差的最小方差得到{p1['sharpe']:.2f}的夏普比率，"
        "位列本部分所有规则的前列，并且几乎准确地预测了自己的波动率：{100 * p1['pred_vol']:.1f}%对{100 * p1['vol']:.1f}%。参数很少的模型无法拟合噪声，所以它不会自欺。第31部分会构建一个完整的因子风险模型。",

    'f"On the real data, with ten-year windows.':
        "在真实数据上，用十年窗口。<bookmark mark='a'/>朝常相关的估计强度在{kmin:.2f}到{kmax:.2f}之间：常常有四分之一或更多的权重放在目标上。朝单位矩阵的强度则一直低于{kimax:.2f}，"
        "因为单位矩阵忽略了每个行业共有的市场模态，在这里是一个更差的目标。好的目标就是接近真相的目标。",

    "One more dial: the window.":
        "还有一个旋钮：窗口。<bookmark mark='a'/>更长的窗口能平均掉噪声，但会混入一个此后已经改变的协方差。误差是一个像N除以T那样下降的噪声项，加上一个随T增长的陈旧项。"
        "<bookmark mark='b'/>指数加权，即第7部分的RiskMetrics，平滑地权衡这两者。<bookmark mark='c'/>而日度数据在同样的日历窗口里提供二十倍的观测，这就是为什么风险交易台用日收益估计协方差，"
        "而对预期收益，明智地几乎什么都不估计。",

    "Pause and predict. If the true covariance really were a multiple of the identity":
        "暂停，预测一下。如果真实的协方差真的是单位矩阵的倍数，最优强度是多少？",

    # ------------------------------------------------------------------ Constraints
    "Chapter five. Practitioners have long added constraints":
        "第五章。实务人员早就给优化器加上约束，禁止卖空、限制仓位，并发现组合变得更好而不是更差。为什么一个限制会有帮助？",

    'f"The minimum-variance portfolio of the forty-nine industries, from the last ten years':
        "四十九个行业的最小方差组合，用研究数据的最后十年。<bookmark mark='a'/>不加约束时，它做多一些行业、做空另一些，每投资一美元就有{c['short_sum']:.2f}美元的空头。"
        "<bookmark mark='b'/>禁止卖空后，只有{c['n_pos']}个行业保留权重。受约束的组合看起来更粗糙，而在一项又一项研究中，它在样本外表现更好。",

    "Ravi Jagannathan and Tongshu Ma explained it in 2003.":
        "Ravi Jagannathan和Tongshu Ma在2003年解释了这一点。<bookmark mark='a'/>写出只做多最优解的条件：每个被压在零的权重对应一个乘数。<bookmark mark='b'/>现在把这些乘数从优化器想要做空的资产的协方差中减去。"
        "<bookmark mark='c'/>只做多的组合恰好就是这个修改后矩阵的无约束最小方差组合。我们在行业上验证了：两组权重一直到小数点后第六位都一致。",

    "What it means. <bookmark mark='a'/> The optimizer shorts an asset":
        "这意味着什么。<bookmark mark='a'/>当一个资产与其他资产的估计协方差很高时，优化器会做空它，而异常高的估计往往就是异常大的误差。"
        "<bookmark mark='b'/>约束恰好降低了这些协方差：它是收缩，精准地瞄准优化器正要利用的那些估计。<bookmark mark='c'/>代价是：当一个大的协方差是真的时，约束扔掉了一个真正的对冲。"
        "有了收缩得好的矩阵，约束就没那么重要了。",

    'f"Out of sample, on the industries. <bookmark mark=\'a\'/> With five-year windows':
        "在样本外，在行业上。<bookmark mark='a'/>用五年窗口，无约束的样本组合实现的波动率为{100 * a60['vol']:.1f}%；只做多时为{100 * b60['vol']:.1f}%：约束起的作用与正式的收缩一样大。"
        "用十年窗口时差距缩小，因为可供约束去除的噪声更少了。",

    "The idea generalises.":
        "这个想法可以推广。<bookmark mark='a'/>Victor DeMiguel、Lorenzo Garlappi、Francisco Nogales和Raman Uppal不是禁止卖空，而是限制组合的总敞口。"
        "<bookmark mark='b'/>上限为一就是只做多；没有上限就是无约束优化器；介于两者之间的是一族由数据调节的组合。<bookmark mark='c'/>而对权重平方和的限制，恰好就是朝单位矩阵的收缩，约束的乘数扮演强度的角色。"
        "约束和收缩是表达同一个想法的两种语言。",

    "Pause and predict. Add an upper limit of five percent":
        "暂停，预测一下。给每个权重加上百分之五的上限。它的乘数会改变哪些协方差，朝哪个方向？",

    # ------------------------------------------------------------------ Black-Litterman
    "Chapter six. In 1990, at Goldman Sachs":
        "第六章。1990年在高盛，Fischer Black和Robert Litterman遇到了第一章的问题：用估计均值喂养的优化器给出荒谬的组合。他们的回答是从市场本身出发。",

    'f"The first idea is to run the optimizer backwards.':
        "第一个想法是把优化器倒着运行。<bookmark mark='a'/>如果每个投资者都持有均值-方差组合，市场组合就是最优解。<bookmark mark='b'/>所以问：什么样的预期收益会让今天的市场权重成为最优？"
        "delta乘以协方差再乘以市场权重。这就是均衡收益，它和协方差一样稳定，因为没有估计任何均值。<bookmark mark='c'/>delta是市场的风险厌恶系数；用研究数据的最后十年，约为{b['delta']:.1f}。",

    "The second idea is Bayes.":
        "第二个想法是贝叶斯。<bookmark mark='a'/>把均衡收益当作先验：预期收益在它附近，不确定性与协方差成比例。<bookmark mark='b'/>把你相信的东西表达为观点，即线性的陈述，比如一个行业胜过另一个，每个都带一个置信度。"
        "<bookmark mark='c'/>后验均值是两者按精度加权的平均。没有观点时它就是市场；有了有把握的观点，它就朝观点移动，并且只在观点涉及的方向上移动。",

    'f"An example on the industries.':
        "一个行业上的例子。<bookmark mark='a'/>市场权重隐含着软件业每年应比现金多赚{100 * b['pi'][i]:.1f}%，公用事业{100 * b['pi'][j]:.1f}%。<bookmark mark='b'/>现在一个听起来看好软件的观点："
        "它每年会比公用事业多赚{view_pct:.0f}%。但均衡已经说是{100 * spread_eq:.1f}%。相对于市场，这个观点是看空的，后验价差降到{100 * spread_post:.1f}%。"
        "在Black–Litterman里，一个观点是关于市场尚未定价的东西的陈述。",

    'f"And the portfolio.':
        "再看组合。<bookmark mark='a'/>后验组合把{100 * abs(wd[k_out]):.1f}%的权重从软件业移到公用事业，其余每个行业都保持市场权重。"
        "<bookmark mark='b'/>比较那个天真的替代方案：把这十年的样本均值代入同一个优化器，权重绝对值之和为{b['gross_sample']:.0f}。<bookmark mark='c'/>Black–Litterman是把均值朝均衡收缩，而观点是唯一的偏离。",

    "Why the portfolio moved only along the view.":
        "为什么组合只沿着观点移动。<bookmark mark='a'/>用后验均值、以及因均值的剩余不确定性而放大的协方差来优化。<bookmark mark='b'/>Guangliang He和Robert Litterman证明，结果总是缩放后的市场组合，"
        "加上观点组合的加权和，别无其他。<bookmark mark='c'/>每个观点的权重随着它的置信度、以及它偏离均衡的程度而增长。一个与市场一致的观点什么也不增加。",

    'f"How much the view counts is set by its confidence.':
        "观点的分量由它的置信度决定。<bookmark mark='a'/>非常有把握时，在左边，后验价差就是观点本身，{y[0]:.1f}%；毫无把握时，在右边，它就是均衡，{y[-1]:.1f}%。"
        "中间是平滑的按精度加权的混合。选择omega和tau是这个方法的艺术，也是其使用者意见分歧的地方。",

    'f"Black-Litterman shrinks the means toward equilibrium.':
        "Black–Litterman把均值朝均衡收缩。一个更早的想法是把它们彼此靠拢。<bookmark mark='a'/>Philippe Jorion在1986年提出的贝叶斯–斯坦估计量，把每个均值拉向最小方差组合的均值，拉多少由数据决定。"
        "<bookmark mark='b'/>在行业上，数据选择了约{f['phi_mean']:.2f}：接近一半的距离。它改善了切点组合，从{st['sharpe']:.2f}到{bs['sharpe']:.2f}，杠杆只有原来的一小部分。"
        "但它救不了它。用十年收益估计的均值，就是太嘈杂，无法用来交易。",

    "Pause and predict. What happens to the posterior and the portfolio":
        "暂停，预测一下。如果观点的置信度为零，后验和组合会怎样？",

    # ------------------------------------------------------------------ Risk parity
    "Chapter seven. If expected returns are too noisy to use":
        "第七章。如果预期收益太嘈杂而无法使用，也许组合应该只从风险出发来构建。不是最小的风险，那会倚重最小的特征值，而是均匀分布的风险。",

    'f"Equal money is not equal risk.':
        "等额资金不等于等量风险。<bookmark mark='a'/>在四十九个行业的等权组合里，波动最大的{cols[i0]}贡献了{100 * rc_ew[i0]:.1f}%的方差，最平静的只有{100 * rc_ew.min():.1f}%。"
        "<bookmark mark='b'/>风险平价组合则选择权重，让每个行业贡献相同的份额：这里每个四十九分之一。",

    "The mathematics. <bookmark mark='a'/> Each asset's contribution to risk":
        "数学。<bookmark mark='a'/>每个资产对风险的贡献是它的权重乘以它的边际风险；由欧拉定理，它们加起来等于总风险。<bookmark mark='b'/>Florin Spinu在2013年找到了窍门："
        "最小化二分之一y Sigma y减去预算乘以log y之和，这是一个严格凸的问题。<bookmark mark='c'/>它的一阶条件说，每个y乘以它的边际风险等于它的预算：把y归一化，就得到了风险平价组合，唯一，几步牛顿法就能找到。",

    "Marcos López de Prado proposed a different route in 2016":
        "Marcos López de Prado在2016年提出了另一条路：分层风险平价。<bookmark mark='a'/>首先按相关性对资产聚类，这里用单链接，距离为根号下一减rho除以二。"
        "这棵树把一起变动的行业归在一起：底部的叶子就是按树的顺序排列的行业。然后，按这个顺序重排的协方差矩阵接近分块对角。",

    "What the ordering does.":
        "排序起了什么作用。<bookmark mark='a'/>左边是按Kenneth French文件列出的顺序排列的行业相关矩阵：结构很难看出。<bookmark mark='b'/>右边是同一个矩阵按树的顺序排列：相关行业的块沿对角线出现。"
        "HRP先在这些块之间分配，再在块内分配，所以一个块的估计误差不会泄漏到另一个块的权重里。",

    "Then the allocation, as the House runs it.":
        "然后是配置，按本系列公司的运行方式。把排好序的资产列表一分为二。给每一半它成员的逆方差组合，并按这两个组合方差的反比在两半之间分钱。在每一半内重复，直到单个资产。"
        "从不对任何矩阵求逆，所以最小、最嘈杂的特征值永远没有机会主导。",

    'f"Side by side.':
        "并排比较。<bookmark mark='a'/>这些规则从等额资金，经过等量风险，到最小方差。在样本内，最小方差的波动率远远最低，{100 * v['GMV']:.1f}%，而HRP为{100 * v['HRP']:.1f}%，风险平价为{100 * v['ERC']:.1f}%。"
        "但它集中了权重，并信任每一个估计；风险平价和HRP放弃了一些样本内的风险，换来不依赖于对一个嘈杂矩阵求逆的权重。这笔交易是否值得，要由样本外数据和信封来回答。",

    'f"Out of sample, on Chapter two\'s contest.':
        "在样本外，在第二章的较量里。<bookmark mark='a'/>风险平价和HRP如设计的那样落在1/N和最小方差之间：HRP的波动率{100 * h['vol']:.1f}%、夏普比率{h['sharpe']:.2f}，"
        "风险平价{100 * e['vol']:.1f}%和{e['sharpe']:.2f}，而1/N为{100 * w['vol']:.1f}%和{w['sharpe']:.2f}。它们交易得很少：HRP每月换手{100 * h['turnover']:.1f}%。"
        "它们的优点不是更高的收益；而是它们从不对嘈杂的矩阵求逆，所以从不爆炸。",

    "Pause and predict. Two uncorrelated assets, with volatilities of ten and twenty percent.":
        "暂停，预测一下。两个不相关的资产，波动率分别为百分之十和百分之二十。什么样的权重让它们的风险贡献相等？",

    # ------------------------------------------------------------------ CVaR (part)
    "Chapter eight. Two more ways to make the optimizer humble":
        "第八章。另外两种让优化器谦卑的方法：为最坏的输入做计划，以及用真正要紧的损失而不是方差来度量风险。",

    "Robust optimisation first.":
        "先说鲁棒优化。<bookmark mark='a'/>选择这样的权重：当自然从一组可信的预期收益中挑出最坏的那个时，它表现最好。<bookmark mark='b'/>让这组可信值成为估计周围的一个椭球，形状由估计自身的不确定性决定。"
        "<bookmark mark='c'/>最坏情况有闭式解：估计的收益减去kappa乘以这个押注的不确定性。优化器因倚重嘈杂的估计而被收费，这是在病根上治疗第一章的病。",

    "What robustness buys depends on the shape of the set.":
        "鲁棒性能买到什么，取决于这组可信值的形状。<bookmark mark='a'/>常见的选择让均值的不确定性等于协方差除以样本量。<bookmark mark='b'/>那么鲁棒组合与普通组合指向同一个方向：最坏情况的作用就像额外的风险厌恶。"
        "<bookmark mark='c'/>在预算固定为一时，更多的厌恶意味着一个偏向最小方差组合的混合，而最小方差组合不需要预期收益。这样做的鲁棒优化，重新发现了第二章的教训。",
    "Then a different risk.":
        "然后是另一种风险。<bookmark mark='a'/>条件风险价值：最坏百分之五结果中的平均损失。它能看到尾部有多深，而方差和风险价值看不到。"
        "<bookmark mark='b'/>Tyrrell Rockafellar和Stanislav Uryasev在2000年发现，它是对单个数alpha的最小化，而最小值点就是风险价值本身。"
        "<bookmark mark='c'/>在一组情景上，整个组合问题变成一个线性规划：每个情景一个辅助变量，求解器在不到一秒内给出答案。",

    "Why not simply minimise value at risk?":
        "为什么不直接最小化风险价值？<bookmark mark='a'/>两只债券，每只有百分之四的违约概率。各自单独时，95%风险价值都是零。合在一起，至少一只违约的概率是7.8%，"
        "所以这一对的风险价值是一次完全违约：按这个度量，分散化反而提高了风险。<bookmark mark='b'/>风险价值对权重不是凸的，最小化它的优化器会学会把损失藏在分位数之外一点点。"
        "<bookmark mark='c'/>CVaR是一致的：它总是奖励分散化，而最小化它是一个线性规划。",

    'f"The two portfolios\' losing months, 1970 to 2020.':
        "两个组合在1970到2020年间亏损的月份。<bookmark mark='a'/>灰色是最小方差组合的，红色是最小CVaR组合的，并标出了百分之五分位数。最小化CVaR把月份移出了尾部："
        "低于负百分之六的{n6a}个月变成了{n6b}个。代价是更多的中等损失，低于负百分之二的{n2a}个月变成了{n2b}个。它持有的行业也更少，因为它把自己拟合到几十个最坏的月份上。",

    'f"On the industries. <bookmark mark=\'a\'/> In sample, minimising CVaR':
        "在行业上。<bookmark mark='a'/>在样本内，最小化CVaR做到了它说的：CVaR为每月{100 * ci['min CVaR']['cvar']:.2f}%，而最小方差为{100 * ci['min variance']['cvar']:.2f}%。"
        "<bookmark mark='b'/>在十年窗口上滚动向前，顺序反过来了：最小CVaR实现的CVaR为{100 * co['min CVaR']['cvar']:.2f}%，最小方差为{100 * co['min variance']['cvar']:.2f}%。"
        "尾部是从它少数几个最坏的情景中估计的，{n_win}个中的{n_tail}个，而一个每个资产只喂{n_tail}个数的优化器会拟合它们。更好的风险度量比更差的需要更多的数据。",

    "Pause and predict. With a hundred and twenty monthly scenarios":
        "暂停，预测一下。有一百二十个月度情景时，其中有多少个决定95%的CVaR？99%呢？",

    # ------------------------------------------------------------------ Growth
    "Chapter nine. Mean-variance is a one-period idea.":
        "第九章。均值-方差是一个单期的想法。一个几十年不断再投资的投资者关心的是另一件事：财富复利增长得有多快。三个答案，来自三种传统。",

    'f"The first answer is Kelly\'s':
        "第一个答案是Kelly的，第8部分为单次押注推导过它。<bookmark mark='a'/>一个不断再平衡的组合的预期对数增长率等于均值减去方差的一半。"
        "<bookmark mark='b'/>它的最大化者是协方差的逆乘以超额收益：风险厌恶恰好为一的均值-方差，并且以概率一，是最终超越其他所有组合的那个。"
        "<bookmark mark='c'/>对1970到2020年的美国市场，这意味着{g['kelly']:.2f}倍的杠杆：增长最优的投资者每投资一美元要借将近两美元。",

    'f"Draw the growth rate against leverage.':
        "把增长率对杠杆画出来。<bookmark mark='a'/>公式是一条抛物线，在凯利比例处达到峰值。<bookmark mark='b'/>市场每月再平衡的实际路径在{f_emp:.2f}处达到峰值，相距不远。"
        "过了峰值，杠杆越多增长越少，在两倍凯利时增长率回落到无风险利率，而风险还在上升。而且峰值取决于一个估计的均值：这就是为什么谨慎的实务人员只押一半凯利或更少。",

    'f"Why half Kelly is not timidity.':
        "为什么半凯利不是胆怯。<bookmark mark='a'/>押注一个比例c的凯利杠杆，而这个杠杆是从估计的均值算出的。<bookmark mark='b'/>对估计误差取平均后的增长率：误差在惩罚项中加上了sigma平方除以T。"
        "<bookmark mark='c'/>最优比例是平方夏普比率除以它自己加T分之一：永远小于一。<bookmark mark='d'/>对美国市场，用五十一年的数据约为{c51:.2f}；用五年约为{c5:.2f}。半凯利正是估计误差所要求的。",

    "The second answer needs no model at all.":
        "第二个答案根本不需要模型。<bookmark mark='a'/>考虑资产的每一个固定比例再平衡组合，以及它到目前为止的财富。<bookmark mark='b'/>Thomas Cover在1991年提出的通用组合持有它们的平均，按各自的表现加权。"
        "<bookmark mark='c'/>他证明了，它的财富落后于事后选出的最佳组合至多一个随时间多项式增长的因子：无论市场如何，它都以与最佳固定组合相同的指数速度增长。",

    'f"Two industries that rarely move together':
        "两个很少一起变动的行业，{cv['pair'][0]}和{cv['pair'][1]}，从1970年起按月。<bookmark mark='a'/>曲线上的每一点是一个每月再平衡的固定组合，以及它的最终财富。"
        "事后最好的组合把{100 * cv['b_best']:.0f}%放在黄金上，财富增长{cv['best'][-1]:.0f}倍。<bookmark mark='b'/>事先一无所知的通用组合让财富增长了{cv['uni'][-1]:.0f}倍："
        "比值为{ratio:.2f}，远在Cover的界{cv['bound']}之内。还要注意，最佳组合胜过单独持有其中任一个行业：在波动的资产之间再平衡能赚到它们的分散化收益。",

    'f"Read Cover\'s bound per period.':
        "按每期来读Cover的界。<bookmark mark='a'/>通用组合与最佳固定组合之间增长率的差距像n的对数除以n那样缩小，对每一种可能的价格序列都成立，不需要任何模型。"
        "<bookmark mark='b'/>在我们的{n}个月里，最坏情况约为每月{100 * per:.2f}%，而实际的差距小得多。<bookmark mark='c'/>代价是：它只与固定组合竞争，而资产多时，界和计算量都增长得很快。",

    'f"The third answer is Robert Fernholz\'s stochastic portfolio theory':
        "第三个答案是Robert Fernholz的随机组合理论，它追问一个组合在不做任何预测的情况下何时能胜过市场。<bookmark mark='a'/>用每个资产的市场权重的p次方来加权，p小于一，这会偏向小的资产。"
        "Fernholz的主方程把它相对市场的收益分成一个有界的项，即市场多样性的变化，和一个只会累积的项：超额增长率，只要资产彼此分开它就为正。"
        "<bookmark mark='b'/>在四十九个行业上，多样性加权组合每年比市值加权多赚约{100 * sp['excess']:.1f}%：很小，因为行业少而宽泛；长期为正，正如理论所说，只要多样性不崩溃就必然如此。",

    "The quantity behind both results.":
        "两个结果背后的量。<bookmark mark='a'/>超额增长率：持有资产的平均方差与组合本身方差之差的一半。<bookmark mark='b'/>由凸性，它永远不会为负，只要资产不同步变动它就为正。"
        "<bookmark mark='c'/>一个再平衡到固定权重的组合，其增长等于它的资产对数价格的加权平均，加上这一项的累积。在相互偏离的资产之间再平衡就收获了它；这就是通用组合和多样性加权组合的优势来源。",

    "Pause and predict. An investor bets twice the Kelly fraction.":
        "暂停，预测一下。一个投资者押注两倍的凯利比例。增长率是多少，为什么？",

    # ------------------------------------------------------------------ Views
    "Chapter ten. Black-Litterman blends views":
        "第十章。Black–Litterman在正态假设下把观点融入预期收益。Attilio Meucci在2008年把它推广了：把任何观点施加在一整个情景分布上，并且尽可能少地改变它。",

    "The idea. <bookmark mark='a'/> Keep the historical scenarios":
        "想法是这样的。<bookmark mark='a'/>保留历史情景，只改变它们的概率：在满足观点的分布中，找到在相对熵意义下最接近先验的那个。"
        "<bookmark mark='b'/>答案按每个情景与观点的吻合程度，对它的概率做指数倾斜。<bookmark mark='c'/>倾斜对每个观点只有一个乘数，由一个小的凸问题求出，无论有多少个情景。",

    'f"A stress view on the industries\'':
        "对行业自1970年以来的{J}个月度情景施加一个压力观点：银行业平均每月亏损{abs(view):.0f}%。<bookmark mark='a'/>每条线是一个月的新概率，相对于先验的{J}分之一。"
        "与观点一致的月份被调高了权重：最多的是{y1}年{m1}、{y2}年{m2}和{y3}年{m3}。熵池化自己选出了危机，因为那些正是观点成立的月份。"
        "<bookmark mark='b'/>它的有效情景数是{v['ens']:.0f}：这个观点以轻柔的力度移动了分布。",

    'f"What the view did.':
        "观点做了什么。<bookmark mark='a'/>银行业降到了设定的水平；而因为观点是由真实的危机月份来满足的，其他行业也随之下跌：{cols[worst[0]]}和{cols[worst[1]]}跌得最多。"
        "<bookmark mark='b'/>波动率、相关性和尾部都与均值一起移动。<bookmark mark='c'/>而这里没有任何地方需要正态性：任何对概率是线性的观点都可以施加，包括对波动率、相关性或排序的观点。",

    'f"A second view, about risk rather than return.':
        "第二个观点，关于风险而不是收益。<bookmark mark='a'/>假设市场的波动率翻倍。这是关于二阶矩的陈述，它对概率仍然是线性的。"
        "<bookmark mark='b'/>施加后，市场的波动率从每年{100 * vv['vol_prior']:.1f}%变为{100 * vv['vol_post']:.1f}%。<bookmark mark='c'/>还有一件没人要求的事随之而来："
        "行业的平均相关性从{vv['corr_prior']:.2f}升到{vv['corr_post']:.2f}，因为历史上市场狂野的月份正是所有东西一起变动的月份。一个只把波动率放大的正态模型会错过这一点。",

    "Three practical points.":
        "三个实际要点。<bookmark mark='a'/>部分置信度就是后验概率与先验概率的混合。<bookmark mark='b'/>不等式，比如一个行业比另一个差，由同一个凸对偶处理。"
        "<bookmark mark='c'/>而这个方法只能重新加权已经发生过的东西。一场比样本中任何一次都严重的危机，必须先加入包含它的情景才能表达。",

    "Pause and predict. You impose a view that the prior already satisfies.":
        "暂停，预测一下。你施加了一个先验已经满足的观点。后验概率是什么？",

    # ------------------------------------------------------------------ End-to-end
    "Chapter eleven. The classical pipeline has two steps":
        "第十一章。经典的流水线有两步：先预测，再优化。一个神经网络可以跳过预测，直接学习权重，以投资者关心的那个量来训练。这有帮助吗？",

    "The design.":
        "设计。<bookmark mark='a'/>一个小网络根据每个行业自己的近期历史给它打分，softmax把分数变成和为一的正权重。<bookmark mark='b'/>它被训练来最大化组合的实现夏普比率，即决策本身，而不是预测的准确度。"
        "<bookmark mark='c'/>每个行业四个特征，在1975到2005年上训练，在2006到2020年上验证。",

    "The idea comes from published work.":
        "这个想法来自已发表的工作。<bookmark mark='a'/>Zihao Zhang、Stefan Zohren和Stephen Roberts训练了一个网络，把少数几只指数基金的近期价格直接映射为组合权重，以夏普比率为损失。"
        "<bookmark mark='b'/>他们报告在2011到2020年间胜过了所比较的经典配置。注意这个资产范围：只有几只基金，所以要学习的权重很少。我们的有四十九个。",

    'f"Training. <bookmark mark=\'a\'/> On the years it learns from':
        "训练。<bookmark mark='a'/>在它学习的年份上，网络的夏普比率稳步上升，到{tr[-1]:.2f}。<bookmark mark='b'/>在验证年份上它最终为{va[-1]:.2f}，低于简单等权持有每个行业的{e['valid']['ew']:.2f}。",

    'f"Against the alternatives.':
        "与替代方案比较。<bookmark mark='a'/>两步规则先用每个行业的滞后均值做预测，再用收缩的协方差优化，它在训练期得分较低，{e['train']['two']:.2f}，在验证期较高，{e['valid']['two']:.2f}。"
        "端到端学会了训练年份；带收缩的两步法学得少，保留得多。",

    'f"Why. <bookmark mark=\'a\'/> The network concentrated':
        "为什么。<bookmark mark='a'/>网络集中了：在验证期，它的最大权重平均为{100 * e['max_w_valid']:.0f}%，约{e['eff_n_valid']:.0f}个有效持仓。"
        "在月度数据上最大化夏普比率，会奖励押注那些恰好在样本内获胜的东西。<bookmark mark='b'/>决策损失里没有任何收缩，而{n_train}个月并不够学习。"
        "<bookmark mark='c'/>端到端学习在决策复杂时才物有所值，比如有约束、成本或不寻常的损失，并且数据充足。在这里，它就是第一章的误差最大化器，只是参数更多。",

    "There is a principled middle ground.":
        "有一条有原则的中间道路。<bookmark mark='a'/>经典流水线为了准确度拟合预测，然后假装预测是真的去优化。<bookmark mark='b'/>真正要紧的是决策的遗憾：按照预测而不是真相行动所损失的东西。"
        "<bookmark mark='c'/>Adam Elmachtoub和Paul Grigas给出了这个遗憾的一个凸上界，于是可以为它所服务的决策来训练预测，同时保留优化器的结构及其约束。这就是面向决策的学习的方向。",

    "Pause and predict. How would you build shrinkage into the network":
        "暂停，预测一下。在不改变损失的前提下，你会怎样把收缩加进网络？",

    # ------------------------------------------------------------------ Envelope
    "Chapter twelve. Two optimizers from this part":
        "第十二章。本部分的两个优化器，以及它们必须胜过的基准，登记并在2021到2025年上打开一次。",

    'f"The registration.':
        "登记。<bookmark mark='a'/>四十九个行业上的三条规则，每条每月用前十年重新估计：常相关收缩的最小方差，它在第二章的较量中领先；分层风险平价；以及1/N，作为基准。"
        "<bookmark mark='b'/>每个优化器都被计入我们为选出它而比较过的{e['n_trials']}个规则与窗口组合。计数器变为{n_now:,}。",

    'f"First the research years, on which the rules were chosen.':
        "先看研究年份，规则就是在它上面选出的。<bookmark mark='a'/>四十一年下来，三条规则的终点相近；收缩的最小方差以最小的风险到达那里，波动率{100 * lw['vol']:.1f}%，而1/N为{100 * ew['vol']:.1f}%，"
        "所以夏普比率更高，{lw['sharpe']:.2f}对{ew['sharpe']:.2f}。",

    "The envelope. <bookmark mark='a'/> Five years":
        "信封。<bookmark mark='a'/>五年：2021年的繁荣，2022年随利率上升而来的熊市，以及由少数几家科技公司领涨的复苏。<bookmark mark='b'/>三条规则都赚了钱，路径各不相同。",

    'f"The numbers.':
        "数字。<bookmark mark='a'/>在研究年份上，收缩的最小方差和HRP都胜过1/N。<bookmark mark='b'/>在密封的年份上，顺序反了过来：1/N的夏普比率为{ew['sharpe']:.2f}，HRP为{hp['sharpe']:.2f}，"
        "最小方差为{lw['sharpe']:.2f}。最小方差的风险仍然最小，{100 * lw['vol']:.1f}%对{100 * ew['vol']:.1f}%。而每一个差异都小于一个标准误，约{lw['sharpe_se']:.2f}：五年无法给这些规则排名。",

    'f"Can five years tell them apart?':
        "五年能把它们区分开吗？直接检验差异。<bookmark mark='a'/>两个夏普比率之差的标准误取决于两个策略有多相关：Jobson和Korkie的检验，加上Memmel的修正。"
        "<bookmark mark='b'/>1/N减去收缩的最小方差：{d1['diff']:+.2f}，标准误{d1['se']:.2f}。<bookmark mark='c'/>1/N减去HRP：{d2['diff']:+.2f}，标准误小得多，{d2['se']:.2f}，"
        "因为这两个组合的相关性为{100 * d2['rho']:.0f}%。两个差异都不显著。",

    'f"How to read it.':
        "该怎么读。<bookmark mark='a'/>最小方差承诺的是更小的风险，而不是更多的收益，它也交付了更小的风险，只是优势比研究期小：那时{100 * lw['vol_res']:.1f}%，现在{100 * lw['vol_hold']:.1f}%。"
        "<bookmark mark='b'/>这些年份奖励的是此前波动最大的行业：一个行业在这些年的收益与它前十年的波动率之间的相关性为{e['vol_return_corr']:.2f}。那些恰恰是基于风险的规则会回避的行业。"
        "<bookmark mark='c'/>业绩记录保留三行，它们的标准误大于彼此的差异，这本身就是诚实的发现。",

    "What a portfolio desk would do next.":
        "一个组合交易台接下来会做什么。<bookmark mark='a'/>把真实的约束和成本放进优化之内，而不是之后：第31部分正是这样做的。<bookmark mark='b'/>每月跟踪实现风险与预测风险；"
        "写给研究者的一章说明了差距应该有多大，所以更大的差距意味着协方差已经变了。<bookmark mark='c'/>只有当证据越过与原规则相同的门槛时才更改规则，因为一条新规则就是一次新试验。",

    "Pause and predict. Two rules each have a Sharpe ratio standard error":
        "暂停，预测一下。两条规则在五年里的夏普比率标准误各约为0.45，它们的收益相关性为百分之九十。它们之差的标准误是更大还是更小？",
    # ------------------------------------------------------------------ House
    "Chapter thirteen. The House's thirtieth rule":
        "第十三章。本系列公司的第30条规则：一个优化组合在本系列公司愿意交易它之前，必须如何报告自己。",

    "The first sheet. <bookmark mark='a'/> Optimizers fed with five years":
        "第一张表。<bookmark mark='a'/>用五年估计喂养的优化器，承诺的风险只是它们交付风险的一小部分。四十九个特征值中有两个高出噪声。收缩把样本组合的超额方差削减了好几倍。"
        "四十年来，朴素的规则不落下风，收缩的最小方差规则风险最小。在真实的窗口上，风险错觉比理论还大。而在密封的年份上，1/N位列第一，领先不到一个标准误。",

    "Chapter four's estimator, as the House implements it":
        "第四章的估计量，按本系列公司的实现，十二行。对收益去均值。目标是平均方差乘以单位矩阵。它到样本矩阵的距离，以及逐个观测测量的样本矩阵自身的噪声，给出强度，上限为一。"
        "不用调参，不用交叉验证：数据自己选择要多不信任自己。",

    "And the long-only optimizer, which this part had to write for itself":
        "还有只做多的优化器，本部分不得不自己写一个，因为通用求解器每个组合要花好几秒。这是一个原始有效集方法：在仍然自由的资产上，朝无约束最优解跳过去；"
        "如果某个权重会变负，就停在零并把它固定在那里；到达目标时，释放那个乘数表明它想回来的固定权重。它只需几毫秒，结果与通用求解器一致到最后一位。",

    "The tools this part adds. <bookmark mark='a'/> Covariance estimators":
        "本部分添加的工具。<bookmark mark='a'/>协方差估计量；Markowitz的规则；观点；基于风险的配置；尾部；增长；以及风险错觉的理论。<bookmark mark='b'/>还有第30条规则。"
        "一个优化组合只有满足以下条件才能进入本系列公司：它的协方差经过收缩或清洗，且方法有记录；它的风险既在样本内报告，也在权重没见过的数据上报告；它的总敞口、换手率和最大权重都有说明；"
        "并且在扣除成本后，与1/N以及一个完全不需要预期收益的基于风险的规则做了比较。",

    "The rule against three cases. <bookmark mark='a'/> A backtest with a volatility of four percent":
        "用这条规则检验三个案例。<bookmark mark='a'/>一个波动率为百分之四的回测：问窗口、资产数目和估计量；如果用的是样本矩阵，且资产数接近观测数，真实风险要大好几倍。"
        "<bookmark mark='b'/>一个总敞口为百分之三百的组合：它由估计的均值构建，必须在扣除成本后胜过1/N和一个收缩的最小方差规则。<bookmark mark='c'/>一只在2022年亏损的风险平价基金："
        "等量风险不等于没有风险，当债券和股票一起下跌时，它所依赖的相关性就不复存在了。",

    # ------------------------------------------------------------------ Research
    "For the researcher: Chapter two showed every rule that inverts":
        "写给研究者：第二章显示，每一条对估计协方差求逆的规则，承诺的风险都小于它交付的。对于样本最小方差组合，在正态收益下，这个谎言的大小可以精确计算。",

    "The setup. <bookmark mark='a'/> The minimum-variance portfolio of K assets":
        "设定。<bookmark mark='a'/>K个资产的最小方差组合是协方差的逆乘以全一向量，再归一化；它的方差是一除以一转置Sigma逆一。<bookmark mark='b'/>样本版本使用样本协方差，"
        "对正态收益，它是一个自由度为T减一的Wishart矩阵。<bookmark mark='c'/>两个数字：优化器用自己的估计报告的方差，以及它真正具有的方差。",

    "In sample first. <bookmark mark='a'/> The variance the optimizer reports":
        "先看样本内。<bookmark mark='a'/>优化器报告的方差是一除以全一向量在逆估计下的二次型。<bookmark mark='b'/>一个关于Wishart矩阵的经典结果，见Robb Muirhead的教科书："
        "对任何固定的向量，真实二次型与估计二次型之比是一个自由度为n减K加一的卡方变量，无论真实协方差是什么。<bookmark mark='c'/>所以报告的方差等于真实最小值乘以一个卡方除以n。"
        "它的均值是n减K加一除以n，当资产数与样本一起增长时，它趋于一减gamma。优化器报告的风险低于可能的最小风险。",

    "Why the lemma holds, in four lines.":
        "引理为什么成立，用四行说明。<bookmark mark='a'/>变换坐标，使固定向量成为第一个坐标轴；比值不变。<bookmark mark='b'/>逆矩阵左上角的元素是一除以一个舒尔补：对其他坐标回归之后剩下的第一个方差。"
        "<bookmark mark='c'/>对Wishart矩阵，这个舒尔补仍然是Wishart的，一个缩放的卡方，自由度少了K减一：其他每个坐标用掉一个。<bookmark mark='d'/>除以真实的舒尔补，比值就是一个自由度为n减K加一的卡方。"
        "优化器的乐观恰好就是那些丢失的自由度。",

    "Then out of sample. <bookmark mark='a'/> The ratio does not change":
        "然后是样本外。<bookmark mark='a'/>比值在线性坐标变换下不变，所以做白化：取真实协方差为单位矩阵。<bookmark mark='b'/>把估计的方向分成沿真实最优解的分量和其余部分。"
        "超额风险就是其余部分相对于指向正确方向那部分的大小。<bookmark mark='c'/>由Wishart矩阵的Bartlett分解，这两部分是独立的卡方，所以超额是一个F比值，正如Alexander Kempf和Christoph Memmel在2006年所证明的。"
        "<bookmark mark='d'/>它的均值：真实方差比最小值多出K减一除以n减K，趋于一除以一减gamma。",

    "Stated as a limit. <bookmark mark='a'/> As assets and observations grow together":
        "表述为极限。<bookmark mark='a'/>当资产数和观测数以比值gamma一起增长时，报告的方差趋于一减gamma乘以最小值，真实方差趋于最小值除以一减gamma，"
        "所以真实值超过报告值的倍数是一除以一减gamma的平方。gamma为二分之一时，是四倍。<bookmark mark='b'/>随机矩阵理论把同样的极限推广到远超正态收益的情形。",

    'f"Check it, with the industries\' own covariance as the truth.':
        "检验一下，以行业自己的协方差为真相。<bookmark mark='a'/>红线是优化器报告值的极限，青绿色线是它实际具有的值的极限。<bookmark mark='b'/>点是模拟，每个长度一千个样本。"
        "用十年数据时它们给出{s120['in']:.3f}和{s120['out']:.3f}，精确值为{s120['in_th']:.3f}和{s120['out_th']:.3f}。用五年数据时，真实方差是最小值的{s60['out']:.1f}倍，而优化器报告{s60['in']:.2f}。",

    "The whole distributions, for ten years of data.":
        "十年数据下的完整分布。<bookmark mark='a'/>每一个样本报告的都低于真实最小值：红色直方图完全落在一的左边。<bookmark mark='b'/>而每个样本的真实方差都在一的右边，这由最小值的定义决定，"
        "并带着一条长长的右尾：F分布的尾巴。优化器总是乐观的，从不是偶然的。",

    'f"The theorem is about the sample covariance, and shrinkage escapes it.':
        "这条定理是关于样本协方差的，而收缩逃脱了它。<bookmark mark='a'/>青绿色线是极限，红点是第四章对样本矩阵的模拟，落在线上。<bookmark mark='b'/>收缩的估计量远在下方："
        "在gamma约为0.8时，是最小值的{s60['nonlinear']['gmv']:.2f}倍，而不是{s60['sample']['gmv']:.1f}倍。丢失K减一个自由度，是自由估计每一个协方差的代价；结构化或收缩的估计不必全额支付。",

    'f"And on the real industries.':
        "再看真实的行业。<bookmark mark='a'/>用五年窗口，优化器报告的波动率为{100 * r60['pred_vol']:.1f}%，实际为{100 * r60['real_vol']:.1f}%：方差之比为{r60['ratio']:.0f}，"
        "而正态理论给出{r60['theory']:.0f}。用十年时，{r120['ratio']:.1f}对{r120['theory']:.1f}。真实收益比理论更糟，因为它们有厚尾，协方差也在漂移，但理论抓住了形状和大部分的大小。",

    'f"Does shrinkage cure the illusion?':
        "收缩能治好这个错觉吗？<bookmark mark='a'/>红线是样本矩阵在行业上的真实方差与报告方差之比，黄线是正态理论。<bookmark mark='b'/>先收缩协方差，这个比值就崩塌了："
        "五年窗口时从{r0:.0f}降到{l0:.1f}，十年时从{r2:.1f}降到{l2:.1f}。收缩的优化器仍然有一点自我恭维，但不再相差一个数量级。",

    "What to do with it.":
        "该怎么用它。<bookmark mark='a'/>在正态假设下，把报告的方差乘以这个因子，就得到对真实值的无偏预测。<bookmark mark='b'/>更好的是，先收缩：收缩的协方差给优化器留下更少可利用的误差，它的报告也更接近真相。"
        "<bookmark mark='c'/>而一般来说，永远不要让一个组合给自己的风险打分：在权重没见过的数据上测量它。",

    "Three open questions. <bookmark mark='a'/> Exact finite-sample laws":
        "三个开放问题。<bookmark mark='a'/>对厚尾、相依的收益，精确的有限样本分布律尚不清楚，而数据显示那里的错觉更大。<bookmark mark='b'/>对协方差最优的收缩，并不是对组合真实方差最优的收缩；目前只有部分答案。"
        "<bookmark mark='c'/>而当资产多于观测时，样本矩阵根本无法求逆；正则化的最小方差在那里能达到什么，仍在研究之中。",

    "Pause and predict. A hundred assets and two hundred and fifty observations.":
        "暂停，预测一下。一百个资产，二百五十个观测。真实方差大约是报告值的多少倍？",

    # ------------------------------------------------------------------ Outro
    "Part thirty in fourteen lines.":
        "用十四行回顾第30部分。用估计喂养的优化器，承诺的风险只是它交付的一小部分，因为它寻找最讨喜的误差。与1/N相比，使用估计均值的规则失败了，"
        "而用收缩协方差最小化方差的规则在风险上获胜。随机矩阵理论说，一个协方差矩阵的谱除了市场和少数板块之外，大部分与噪声无法区分。朝一个简单目标的收缩，无论线性还是逐个特征值，"
        "都把损害削减了好几倍；只做多约束是伪装的同一件事。Black和Litterman从市场出发。风险平价和HRP完全避免对矩阵求逆。",

    "Minimising tail risk needs more data than minimising variance.":
        "最小化尾部风险比最小化方差需要更多的数据。增长有自己的理论，从Kelly的杠杆到Cover的通用组合和Fernholz的多样性。熵池化把一个观点施加在整个分布上，并自己选出了危机。"
        "端到端训练的网络学会了它的训练年份。在密封的年份上，1/N位列第一，领先不到一个标准误。而写给研究者的一章证明了，样本最小方差组合总是低估自己的风险，低估的倍数它已算出。",

    "Six desk questions. Why does the optimizer love":
        "六个交易台问题。为什么优化器偏爱估计误差最大的资产？因为它最大化估计的回报与估计的风险之比，而最讨喜的估计错得最厉害。<bookmark mark='a'/>一个用五年窗口、报告百分之三波动率的四十九资产回测，"
        "报告的只是其真实方差的一小部分。<bookmark mark='b'/>而一个让组合变好的只做多约束不是运气：它是收缩。",

    "Black-Litterman with no views returns the market.":
        "没有观点的Black–Litterman返回市场组合。<bookmark mark='a'/>全凯利最大化长期增长，但通常太多了，因为它的输入是估计。<bookmark mark='b'/>而五年无法给两条标准误大于彼此差异的规则排名。完整的解答在讲义里。",

    "And twelve problems: a two-asset minimum-variance portfolio":
        "还有十二道习题：一个两资产的最小方差组合；它的风险平价表亲；五年窗口的噪声带；最优收缩强度；没有观点的Black–Litterman；凯利与两倍凯利；Cover的界；手算CVaR；"
        "两个情景上的熵池化；以及一百个资产的风险错觉。然后是两道资格考试题：样本最小方差组合风险的精确分布律，以及Jagannathan与Ma的定理。中英文解答都在讲义里。",

    "Where this comes back. Part thirty-one builds factor risk models":
        "这些内容会在哪里再出现。第31部分构建因子风险模型，即真实交易台使用的结构化协方差，并在有成本的情况下随时间交易。第32部分把风险平价用于跨资产类别。"
        "第40部分正确地度量风险，包括CVaR的一致性。收官部分会把这些行和其他一切一起做紧缩调整。",

    "The textbooks this part follows, and the papers it draws on, from Markowitz":
        "本部分依据的教科书，以及它引用的论文，从1952年的Markowitz到2020年的非线性收缩。屏幕上的每个数字都由本系列公司的代码根据Kenneth French的行业组合算出，模拟都已标明。",

    "The House now has a portfolio desk":
        "本系列公司现在有了一个组合交易台：知道自己噪声的估计量，需要更少估计的规则，以及在权重从未见过的数据上报告风险的责任。<bookmark mark='a'/>下一部分，第31部分：风险模型、成本与跨期交易。"
        "主动管理的基本定律，推导出来；因子风险模型；以及当每一笔交易都要花钱时，如何朝一个移动的目标交易。",
}

PHRASES = {"January": "1月", "February": "2月", "March": "3月", "April": "4月", "May": "5月", "June": "6月", "July": "7月",
           "August": "8月", "September": "9月", "October": "10月", "November": "11月", "December": "12月"}
