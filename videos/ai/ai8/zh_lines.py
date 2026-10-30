"""Chinese narration for ai8: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).

Numbers from our own runs stay placeholders, so the Chinese follows the data when it changes; sentences chosen by a
result (``verdict``, ``tail``, ...) are translated as templates of their own and spliced in.  Terms follow
videos/ai/AI_ZH_GUIDE.md and this part's glossary (README): 风险、经验风险、贝叶斯风险、打散、VC维、增长函数、
拉德马赫复杂度、间隔、PAC-贝叶斯、隐式偏好、双下降、良性过拟合、尖锐度、协变量偏移、重要性加权、可提取。
"""

TITLE = '人工智能，从零搭建 · 第8部分：拟合与泛化'

CHAPTERS = {
    'Hook': '差距',
    'Risk': '1. 风险，以及最好的规则',
    'BiasVariance': '2. 偏差与方差，推导',
    'Hoeffding': '3. 一条规则，然后是很多条',
    'VC': '4. 打散与VC界',
    'Rademacher': '5. 拉德马赫复杂度',
    'Margins': '6. 间隔',
    'PACBayes': '7. PAC-贝叶斯：一个有意义的界',
    'Stability': '8. 压缩与稳定性',
    'RandomLabels': '9. 记住毫无意义的东西',
    'MinNorm': '10. 隐式偏好：最小的拟合',
    'MaxMargin': '11. 隐式偏好：最宽的间隔',
    'DoubleDescent': '12. 双下降',
    'MoreDescents': '13. 样本数与训练轮数上的双下降',
    'Benign': '14. 良性过拟合',
    'Sharpness': '15. 平坦极小值与尖锐度之争',
    'Shift': '16. 分布偏移',
    'Memorization': '17. 语言模型里的记忆',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"In part six, a model that asked only its single nearest neighbour':
        "在第6部分，有一个模型只问离它最近的1个邻居，它对自己的训练页能判对{100 * (1 - tr[0]):.0f}%，对新的书页却只有"
        "{100 * (1 - te[0]):.0f}%。<bookmark mark='a'/>让更多的邻居来投票，两个错误率就会汇到一起。<bookmark mark='b'/>"
        "这道差距，正是机器学习的核心问题。模型是根据样本拟合出来的。凭什么它在别的东西上也管用？",

    "The question is old, and so are the first answers.":
        "这个问题很老，最早的回答也一样老。1963年，瓦西里·霍夫丁证明了，许多次独立抽样的平均值，会多么紧地聚集在它的均值周围。"
        "<bookmark mark='a'/>1971年，弗拉基米尔·瓦普尼克和阿列克谢·切尔沃年基斯把它变成了一套学习理论：一个模型能学会什么，取决于它能拟合多少东西。"
        "<bookmark mark='b'/>1984年，莱斯利·瓦利安特给“学习”本身下了定义：概率近似正确。<bookmark mark='c'/>1992年，杰曼、比嫩斯托克和杜尔萨"
        "给偏差与方差之间的两难起了名字；<bookmark mark='d'/>1999年，戴维·麦卡莱斯特给模型的平均给出了界，<bookmark mark='e'/>2002年，巴特利特和门德尔松"
        "用拟合噪声的能力来衡量容量。<bookmark mark='f'/>然后，深度学习打破了这幅图景：2017年，张驰原和同事们发现网络能把随机标签全部记住，"
        "<bookmark mark='g'/>2019年，贝尔金和同事们发现，越过了能把一切都拟合的那一点之后，测试误差又降了下来，<bookmark mark='h'/>2020年，巴特利特和同事们"
        "证明了拟合噪声在什么时候是无害的。<bookmark mark='i'/>从2021年起，卡里尼和同事们从语言模型里挖出了训练文本，<bookmark mark='j'/>到了2025年，"
        "已经有了对大语言模型真正说明问题的界，也有了法院就它们记住的东西作出的判决。",

    "This is Part 8 of AI, Built":
        "这是《人工智能，从零搭建》的第8部分：拟合与泛化，也就是模型为什么能在从没见过的数据上管用。<bookmark mark='a'/>本部分讲：风险，我们真正在乎的量，"
        "以及任何模型最好能做到什么程度；推导偏差与方差；<bookmark mark='b'/>一条规则在测试数据上的分数什么时候可信，在很多条规则里挑选时又有什么不同；"
        "<bookmark mark='c'/>用三种方法衡量容量，以及每种方法换来的保证；<bookmark mark='d'/>对神经网络依然有意义的界；<bookmark mark='e'/>"
        "推翻了经典图景的那些实验，以及此后的解释；<bookmark mark='f'/>最后讲测试数据来自别处时会发生什么，以及语言模型会一字不差地记住什么。",

    # ------------------------------------------------------------------ Risk
    "Chapter one. Risk, and the best possible rule.":
        "第1章。风险，以及最好的规则。",

    "To say what generalizing means, we need two numbers.":
        "要说清楚什么叫泛化，我们需要两个数。这里有一个小到可以完全了解的问题：两个类别，出现的可能性相同，每个类别的单个测量值x各有自己的分布。"
        "<bookmark mark='a'/>一个样本，就是从中抽出的40个点。<bookmark mark='b'/>一条规则h根据x猜类别，猜错时损失为1。它的风险，是世界可能送来的一切数据上的"
        "期望损失，也就是它在从没见过的数据上的错误率。<bookmark mark='c'/>它的经验风险，是在我们手头这个样本上的平均损失：训练误差。所谓泛化，"
        "就是后者能很好地指示前者，哪怕这条规则正是我们看着这个样本挑出来的。",

    'f"What\'s the best any rule could do?':
        "任何规则最好能做到什么程度？对x求平均：在x处猜错的概率。<bookmark mark='a'/>在每个x处，真实类别是1的概率为η(x)；最好的猜法是选更可能的那个类别，"
        "它猜错的概率是η和1减η中较小的那个。<bookmark mark='b'/>所以没有哪条规则能低于这个最小值的平均：贝叶斯风险，在这里就是两条曲线重叠部分的面积，"
        "{r['bayes']:.3f}。达到它的规则，在类别1更可能的地方都说1：在这里，是一个区间。<bookmark mark='c'/>它需要知道真实的分布，而我们永远不知道；"
        "它是衡量学习器的底线。1967年，科弗和哈特证明了，只看最近的1个邻居，在数据无穷多时，错误率至多是它的两倍。",

    'f"Now a learner. Suppose it may only use thresholds':
        "现在来一个学习器。假设它只能用阈值：x大于t就说1。它挑训练错误最少的那个阈值。<bookmark mark='a'/>每次用40个点，做30次，挑出来的阈值在最好的那个"
        "周围跳来跳去。<bookmark mark='b'/>在每个样本量下，对{r['draws']}个样本求平均。只有{n0}个样本时，训练误差是{100 * em[0]:.0f}%，可挑出来的规则"
        "真实风险是{100 * tm[0]:.0f}%：训练误差太乐观了，因为这条规则正是挑来在这些点上显得好看的。<bookmark mark='c'/>有{nN:,}个样本时，两者都稳定在"
        "{100 * rc:.1f}%附近，也就是最好的阈值的风险，并且一直高于贝叶斯风险{100 * bay:.1f}%。<bookmark mark='d'/>这样，超出的风险就分成了两部分："
        "近似误差，因为任何阈值都画不出一个区间；估计误差，因为样本是有限的。更多数据只能缩小后者；更丰富的模型族能缩小前者，而本部分接下来讲的，"
        "就是这会让后者付出什么代价。",

    # ------------------------------------------------------------------ BiasVariance
    "Chapter two. Bias and variance.":
        "第2章。偏差与方差。",

    'f"The classical answer starts with a setting small enough':
        "经典的回答，从一个小到能看清一切的场景讲起：一条光滑的曲线，还有从它上面抽取的16个带噪声的点。<bookmark mark='a'/>拟合一条直线。再抽16个新的点，"
        "重新拟合，一次又一次：它每次都以同样的方式，抓不住曲线的形状。这种系统性的偏离，就是偏差。<bookmark mark='b'/>拟合一个12次多项式：也就是x的"
        "各次幂之和，一直到x的12次方。次数，也就是最高的幂次，大致决定了曲线能拐几道弯。它从每个点穿过，可每次重新抽样，都得到一条截然不同的曲线。"
        "这就是方差。<bookmark mark='c'/>在两者之间，{best}次的拟合紧贴着真相。",

    "Why does the error split that way?":
        "误差为什么会这样分解？固定一个点x。答案y是真实曲线f加上方差为σ²的噪声，而拟合f帽取决于随机的训练集。<bookmark mark='a'/>噪声与拟合无关，平均为0，"
        "所以交叉项消失了：噪声的方差单独分了出来。<bookmark mark='b'/>在剩下的部分里，加上再减去平均拟合f拔。<bookmark mark='c'/>拟合偏离它自身平均的部分，"
        "平均起来也是0，所以又没有交叉项。<bookmark mark='d'/>剩下三块：平均拟合离真相的距离的平方，叫偏差；拟合在不同样本之间变化多少，叫方差；"
        "还有噪声。1992年，杰曼、比嫩斯托克和杜尔萨为神经网络给这个两难起了名字。",

    'f"Now measure all three, over':
        "现在把三者都量出来，每个次数都用{b['runs']}个训练集。<bookmark mark='a'/>偏差的平方随着模型越来越灵活而下降。<bookmark mark='b'/>方差上升。"
        "<bookmark mark='c'/>噪声是一道任何模型都低不下去的底线。三者之和是一个U形，最好的模型在U的底部：足够灵活，但不过分。<bookmark mark='d'/>"
        "这些圆圈是直接在新的带噪声的点上测出的误差：它们落在这个和上，每个次数都相差不到{100 * dev:.0f}%。三十年来，这个U形一直是教科书上的图景："
        "控制住灵活程度，就控制住了误差。请记住它；第12章会在它的右边以外，发现第二次下降。",

    # ------------------------------------------------------------------ Hoeffding
    "Chapter three. One rule, then many.":
        "第3章。一条规则，然后是很多条。",

    'f"Start with one rule, fixed in advance, and a test set.':
        "先从一条事先固定好的规则和一个测试集开始。每个测试样本都是一次抛硬币：规则要么错，要么对，测出的错误率就是这些硬币的平均。第5部分证明了"
        "霍夫丁不等式：n个介于0和1之间的独立数的平均，偏离它的均值ε的概率，至多是2乘以e的负2nε²次方。<bookmark mark='a'/>来看它实际发生。"
        "一条真实错误率为{100 * p:.0f}%的规则，在10个测试样本上测，测十万次：只有{100 * within[ns[0]]:.0f}%的测量结果落在正负5个百分点以内。"
        "<bookmark mark='b'/>40个样本时，{100 * within[ns[1]]:.0f}%。<bookmark mark='c'/>{ns[2]}个时，{100 * within[ns[2]]:.0f}%。"
        "<bookmark mark='d'/>{ns[3]}个时，{100 * within[ns[3]]:.0f}%：直方图按根号n分之1的速度收窄。",

    'f"On a log scale, the measured tail':
        "在对数坐标上，160个测试样本时实测的尾部概率像抛物线一样下降，霍夫丁的界也一样，而且始终在它上方。<bookmark mark='a'/>只用到方差的切比雪夫界，"
        "下降得要慢得多。<bookmark mark='b'/>那么，要有95%的把握离真相不超过5个百分点，需要多少个测试样本？如果知道真实错误率，恰好需要{ne}个。"
        "霍夫丁要求{nh:,}个，大约是{ratio:.1f}倍，但它对规则一无所知也能用。切比雪夫要求{nc:,}个。这就是为什么几千个样本的留出测试集，给出的分数是可信的。",

    'f"But a learner doesn\'t test one rule':
        "可学习器并不只测一条规则；它在同一份数据上，从许多条里挑最好的。这里有{K:,}条什么都不懂的规则，在{n}个标签是抛硬币的样本上打分。"
        "<bookmark mark='a'/>每条规则的训练误差都散布在50%附近，其中最好的那条得到{100 * best:.0f}%。<bookmark mark='b'/>在一万个新样本上，"
        "这个赢家的错误率是{100 * fresh:.1f}%。正是在许多规则里挑选，让分数说了谎。<bookmark mark='c'/>补救办法是联合界：任何一条规则偏离的概率，"
        "至多是各自概率之和。<bookmark mark='d'/>每一项都是一个霍夫丁尾部。<bookmark mark='e'/>令总和等于δ，解出来：以1减δ的概率，有限模型族里的每一条规则，"
        "误差都不超过“模型族大小的对数除以n”的平方根。挑选的代价，只随对数增长。",

    'f"As the family grows from one rule to a million':
        "模型族从1条规则增长到一百万条，在100个样本上打分，最好的训练误差从{100 * b100[0]:.0f}%降到{100 * b100[i6]:.0f}%，而标签纯粹是噪声。"
        "<bookmark mark='a'/>训练误差与真实误差之间的最大差距，在95%的情况下，从{100 * g100[0]:.0f}个百分点增长到{100 * g100[i6]:.0f}个，"
        "<bookmark mark='b'/>而联合界从{100 * bd100[0]:.0f}增长到{100 * bd100[i6]:.0f}，始终在它上方{tight}<bookmark mark='c'/>1984年，莱斯利·瓦利安特"
        "把这一点变成了学习的定义：概率近似正确。如果足够多的样本能让每条规则的分数，以很高的概率，可信到ε以内，这个模型族就是可学习的。"
        "对有限的模型族，样本数取模型族大小的对数除以ε²就够了。可是一条直线有无穷多个位置。下一章会好好地数一数。",

    # ------------------------------------------------------------------ VC
    "Chapter four. Shattering, and the VC bound.":
        "第4章。打散，以及VC界。",

    "A family of rules with infinitely many members can still be weak.":
        "一个有无穷多成员的规则族，照样可以很弱。拿平面上的直线和三个点来说。<bookmark mark='a'/>把这些点按八种可能方式中的任意一种涂色，总有一条直线"
        "能把两种颜色分开。<bookmark mark='b'/>四个点就不行了：没有哪条直线能分开这两种标注，也就是异或那种交叉的模式。<bookmark mark='c'/>如果一个规则族"
        "能产生一组点的每一种标注，就说它打散了这组点；它能打散的最大点集的大小，叫它的VC维，以瓦普尼克和切尔沃年基斯命名：平面上的直线是3，"
        "一般来说，线性规则的VC维比它读入的数的个数多1。",

    'f"What matters is not how many rules a family has':
        "要紧的不是一个规则族有多少条规则，而是在眼前这些点上，它能产生多少种不同的标注：这叫增长函数。<bookmark mark='a'/>对五个点，半平面能产生"
        "32种里的{n5}种。<bookmark mark='b'/>让一条直线转一圈，就能对每个n数出来：半平面恰好能实现n²减n加2种标注，{nN}个点时是{int(half[-1])}种，"
        "而全部有{int(p2[-1]):,}种。<bookmark mark='c'/>绍尔–谢拉引理说，这种事总会发生：一旦一个规则族打散不了某个大小d加1的点集，它的增长函数就是一个"
        "d次多项式，再也不会是2的n次方。<bookmark mark='d'/>直线上的区间，VC维是2，恰好达到它的上界。是多项式而不是指数，让一个无穷的规则族也能被学会。",

    'f"That count buys a bound.':
        "这个计数换来了一个界。证明分四步。<bookmark mark='a'/>第一步，把训练样本和另一个同样大小的、想象中的样本比较，叫作影子样本：如果训练误差和真实误差"
        "相差很远，那两个样本上的误差多半也相差很远。<bookmark mark='b'/>在两个样本合起来的点上，这个规则族至多相当于“2n处的增长函数”那么多条规则，"
        "这是一个有限的数，于是联合界和霍夫丁不等式都用得上。<bookmark mark='c'/>绍尔–谢拉引理把这个数变成一个多项式。<bookmark mark='d'/>解出ε："
        "差距按d乘log n除以n的平方根缩小。<bookmark mark='e'/>平面上的直线，在448页上，差距至多是{g['lines_plane']:.2f}。用全部70个词频的线性规则，"
        "是{g['lines_pages']:.2f}：几乎算不上保证；要把它降到0.1，大约需要{int(g['n10']):,}页。而第9章的网络，448页对三十万个权重，这个界就什么也说不出了。"
        "可那个网络照样泛化得很好。",

    # ------------------------------------------------------------------ Rademacher
    "Chapter five. Rademacher complexity.":
        "第5章。拉德马赫复杂度。",

    'f"Counting labellings needs a family\'s worst case.':
        "数标注，要看一个规则族最坏的情形。还有一种更直接的容量测试，就在你实际拥有的数据上做。给每个训练页一个随机标签，抛一次硬币，正1或负1，"
        "让规则族去拟合它们。<bookmark mark='a'/>只用一个词频的线性规则，只比一半多一点点。用全部70个，它能拟合{100 * acc[-1]:.0f}%的硬币：纯粹的噪声。"
        "<bookmark mark='b'/>对硬币求平均，规则族与随机符号能达到的最好相关性，就是它的经验拉德马赫复杂度，以汉斯·拉德马赫的随机正负1变量命名。"
        "一个能把噪声拟合得很好的规则族，可以让任何训练分数都显得漂亮。",

    "And it bounds the gap.":
        "而它能界住差距。以1减δ的概率，每条规则的真实风险至多是它的训练风险，加上损失的拉德马赫复杂度的两倍，再加上一个按根号n分之1缩小的项。"
        "<bookmark mark='a'/>证明的开头和VC的一样，用一个影子样本。<bookmark mark='b'/>把一个真实样本和它的影子孪生交换，就是一个随机符号，于是差距变成了"
        "与随机符号的相关性，完全不需要计数。<bookmark mark='c'/>又因为一个样本至多能让上确界变化n分之1，麦克迪尔米德不等式，霍夫丁不等式的一个近亲，"
        "让测出的复杂度集中起来。科尔钦斯基，以及巴特利特和门德尔松，在2002年前后给出了这个形式。",

    'f"For linear rules with weights of length at most B':
        "对权重长度至多为B的线性规则，复杂度可以精确算出来。<bookmark mark='a'/>对给定的符号，最好的权重向量指向输入的带符号和的方向，这是柯西–施瓦茨不等式，"
        "所以上确界等于n分之B乘以这个和的长度。<bookmark mark='b'/>詹森不等式把期望移到平方根里面，<bookmark mark='c'/>又因为独立的符号互不相关，"
        "交叉项消失了：得到n分之B乘以长度平方和的平方根，至多是B乘以最大长度R，再除以根号n。<bookmark mark='d'/>在书页上：测出的复杂度在每个样本量下"
        "都离这个界不到{100 * (1 - ratio):.0f}%，按根号n分之1下降。两万个随机方向只能达到{r['tried']:.2f}；公式给出的方向能达到{r['best']:.2f}。"
        "再注意少了什么：维数。只有权重的长度算数，下一章正是利用这一点。",

    # ------------------------------------------------------------------ Margins
    "Chapter six. Margins.":
        "第6章。间隔。",

    'f"The Rademacher bound for linear rules depends on the weights\' length':
        "线性规则的拉德马赫界取决于权重的长度，而不是权重有多少个。要用上这一点，就得量一量一条规则把数据分得多有把握：它的间隔，也就是每个样本"
        "在边界正确一侧离边界的距离。<bookmark mark='a'/>第6部分的支持向量机，挑的正是间隔最宽的那条线。<bookmark mark='b'/>在书页上，它把全部{n}个训练页"
        "都分开了，这是它们间隔的分布：最近的一页，离边界是最大输入长度的{m['min_margin']:.3f}。<bookmark mark='c'/>γ处的间隔损失，数的是离边界"
        "比γ还近的书页：规则判对了，但判得不够有把握的那一部分。",

    '"The bound comes in three steps.':
        "这个界分三步。<bookmark mark='a'/>把错误，也就是间隔为负时的1，换成一个斜坡：在0以下是1，在γ以上是0；它夹在错误和间隔损失之间。"
        "<bookmark mark='b'/>对这个斜坡用拉德马赫界。<bookmark mark='c'/>斜坡的斜率是γ分之1，而一个压缩引理说，利普希茨函数会按它的斜率放大复杂度："
        "差距是2BR除以γ根号n。输入的个数从没出现。1998年，彼得·巴特利特把这一点讲得很透：权重的大小，比权重的个数更重要。<bookmark mark='d'/>"
        "现在在书页上算一算。γ小：没有间隔损失，复杂度项却很大。γ大：反过来。{verdict}",

    'f"The best trade-off gives {m[\'best_bound\']:.2f}, more than':
        "最好的折中给出{m['best_bound']:.2f}，比抛硬币的错误率还高：这个界是空的，而实际的测试误差是{100 * (1 - m['test_acc']):.1f}%。"
        "间隔不变的话，大约需要{int(m['n_half']):,}页。我们的448页，对间隔界也不够。",

    'f"The best trade-off gives {m[\'best_bound\']:.2f}, below':
        "最好的折中给出{m['best_bound']:.2f}，低于抛硬币的错误率，而实际的测试误差是{100 * (1 - m['test_acc']):.1f}%。",

    '"Margins first explained a puzzle':
        "比深度学习的谜题早二十年，间隔就解释过一个谜题。提升法把许多弱分类器组合成一个分类器，这里每个弱分类器只是在一个词频上切一刀，"
        "并加大它分错的样本的权重。<bookmark mark='a'/>{first}<bookmark mark='b'/>{tail}<bookmark mark='c'/>沙皮尔、弗罗因德、巴特利特和李在1998年给出了解释："
        "训练点全都判对之后，后面的轮次还在不断把它们的间隔往外推，而间隔界只在乎间隔。同样的形状，训练误差为零之后继续训练，在新数据上反而更好，"
        "马上就要在神经网络上重现。",

    "f'On the pages, its training error reaches zero":
        "在书页上，它的训练误差在第{zero}轮降到0。",

    "On the pages, its training error falls quickly.":
        "在书页上，它的训练误差下降得很快。",

    "f'By the classical story":
        "按经典的说法，它应该到此为止，甚至开始过拟合。可实际上，新书页上的误差还在下降，从第{zero}轮的{100 * te[zero - 1]:.1f}%，"
        "降到第{kmin + 1}轮的{100 * te[kmin]:.1f}%，{end}",

    "f'and ends at":
        "最后在{T}轮时是{100 * te[-1]:.1f}%。",

    "After that, the error on new pages stays":
        "之后，新书页上的误差大致保持不变。",

    # ------------------------------------------------------------------ PACBayes
    "Chapter seven. PAC-Bayes":
        "第7章。PAC-贝叶斯：一个对网络有意义的界。",

    "Counting doesn't work for networks":
        "计数对网络不管用，那就换一个被界住的东西。不看单个网络，而看网络的一个分布，一团权重的云，去界住从中抽出的网络的平均误差。"
        "<bookmark mark='a'/>在看到任何数据之前，选一个关于权重的先验P。训练之后，后验Q就是数据把你推到的地方。<bookmark mark='b'/>戴维·麦卡莱斯特1999年的"
        "PAC-贝叶斯定理：以很高的概率，后验的真实误差接近它的训练误差，而接近到什么程度，只取决于一个数：Q相对于P的KL散度，也就是第1部分里，"
        "数据必须告诉你多少奈特信息的那个量。<bookmark mark='c'/>一个宽的、接近先验的后验，花不了几奈特，不管权重有多少个。",

    "The proof is short.":
        "证明很短。<bookmark mark='a'/>从一个测度变换开始：Q下的平均，至多是相对于P的KL散度，加上P下一个指数平均的对数。这其实是第1部分的吉布斯不等式"
        "换了个样子。<bookmark mark='b'/>对一个固定的网络，训练误差远离真实误差的概率是一个二项分布的尾部，所以n乘以两者散度的指数，平均起来至多是"
        "2根号n。先验是不看数据选的，所以对P求平均，这仍然成立。<bookmark mark='c'/>马尔可夫不等式把这个平均，变成一个以1减δ的概率成立的结论。"
        "<bookmark mark='d'/>取f为n乘以这个散度，再用凸性：就得到这个界。里面没有任何东西在数权重。",

    'f"Now our own. A network with':
        "现在来我们自己的。一个有{p['params']:,}个权重的网络，在{p['n']}页上训练：权重是样本的二十倍。按照朱盖特和罗伊2017年的方法，先验是一个高斯分布，"
        "中心在网络随机的初始权重上，在看到任何一页之前就选好了。<bookmark mark='a'/>先短暂地训练，再把权重变成一团云：围绕它们的一个高斯分布，然后直接优化"
        "这个界本身，优化{steps:,}步。看KL散度：它从几千开始下降，因为在权重无关紧要的地方，这团云会张开到先验那么宽。<bookmark mark='b'/>最后的账目。"
        "从这团云里抽出的两千个网络，在训练页上错{100 * p['e_hat']:.1f}%，有把握地说至多{100 * p['e_up']:.1f}%。KL散度是{p['kl']:.0f}奈特。"
        "<bookmark mark='c'/>{verdict}<bookmark mark='d'/>同样的想法，加上把网络狠狠压缩，2024年给出了语言模型的第一批非空的界，是洛特菲和同事们的工作；"
        "同年晚些时候，改为数词元而不是数文档，界又推广到了像Llama 2 70B这么大的模型。",

    'f"So the bound: the cloud\'s true error':
        "所以，这个界说：这团云的真实误差至多是{100 * p['bound']:.0f}%。和它在测试页上实际的{100 * p['test_Q']:.1f}%相比是松的，但这是一个真正的保证，"
        "针对的是一个权重远多于数据的网络，而VC界在这里毫无意义。",

    "f'The bound comes to":
        "这个界是{100 * p['bound']:.0f}%，并不比抛硬币好；这团云在测试页上实际错{100 * p['test_Q']:.1f}%。",

    # ------------------------------------------------------------------ Stability
    "Chapter eight. Compression, and stability.":
        "第8章。压缩，以及稳定性。",

    'f"A third way to say a rule is simple':
        "说一条规则简单的第三种方式：它能用自己的少数几个样本描述出来。这里有{c['n']}个点，以及把它们分开的、穿过原点的间隔最宽的那条线。"
        "<bookmark mark='a'/>只有{c['k']}个点贴在间隔上：它们是支持向量。{again}<bookmark mark='b'/>利特尔斯通和沃穆特在1986年证明，这样的学习器泛化起来"
        "就像只有k个参数的学习器：它的误差至多大约是k乘log n除以n。<bookmark mark='c'/>在这里是{100 * c['bound']:.1f}%，比直线的VC界紧得多。"
        "在书页上，这个机器需要{c['k_pages']}个支持向量，界是{c['bound_pages']:.2f}：一条规则简单与否，取决于它需要多少样本。压缩也是上一章网络的界"
        "变紧的办法：2018年阿罗拉和同事们的工作，以及语言模型的那些界，都先把网络压缩。",

    "Throw away the rest, train again":
        "把其余的点都扔掉，只用它们重新训练，得到的是同一条线，一位不差。",

    "Train again on those alone":
        "只用它们重新训练，得到的几乎是同一条线。",

    'f"A fourth: a rule is safe':
        "第四种：如果一条规则不太依赖任何单个样本，它就是可靠的。<bookmark mark='a'/>如果把一个训练样本换成另一个，学习器在任何地方的损失至多变化β，"
        "就说它是β稳定的。那么平均来说，它的真实误差至多比训练误差高β，因为把一个训练样本换成一个新样本，恰好就是一个训练点变成测试点的过程。"
        "<bookmark mark='b'/>布斯凯和埃利塞夫在2002年证明，带正则化的学习器是稳定的，β大约是λn分之1。<bookmark mark='c'/>在书页上对岭回归量一量："
        "把一个训练页换成一个留出的页，看任何一个预测会移动多远。正则化越强，变化越小。<bookmark mark='d'/>而对n来说，斜率是{slope_n:.2f}{close}",

    'f"Stability also applies to training itself.':
        "稳定性也适用于训练本身。把随机梯度下降跑两次，按同样的顺序访问样本，用在只差一页的两个训练集上。<bookmark mark='a'/>只有碰到那一页不同的样本时，"
        "两次运行才会分开：{E}遍之后，平均相差{mean_end:.3f}，共二十对。<bookmark mark='b'/>哈德特、雷希特和辛格在2016年证明，对凸的损失，"
        "这种漂移至多与步长乘以步数、再除以n成正比：训练得快，泛化得好。这里的界大约是实测漂移的{ratio:.0f}倍；成立，但很松。对网络来说，"
        "损失不是凸的，没有这么干净的结论，谜题也就从这里开始。",

    # ------------------------------------------------------------------ RandomLabels
    "Chapter nine. Memorizing nonsense.":
        "第9章。记住毫无意义的东西。",

    'f"Every bound so far charges for capacity.':
        "到目前为止，每个界都按容量收费。2016年，张驰原和同事们做了一个实验，说明了为什么对网络来说，这不可能是全部。拿一个网络来：一层层简单的单元，"
        "这里输入是70个词频，有两层，每层512个单元，还有两个输出，每位作者一个。这大约是{round(n_params, -3) // 1000}千个权重。用真实作者，"
        "在{n}个训练页上训练它。<bookmark mark='a'/>它把它们全都拟合了，在新书页上判对{100 * T[-1, 2]:.1f}%。<bookmark mark='b'/>现在把作者打乱，"
        "让每个标签都是随机的。同样的网络，同样的训练。",

    "It fits these too, every one of them":
        "它把这些也拟合了，每一个都不落，只是稍慢一点。它记住了毫无意义的东西。<bookmark mark='a'/>而在新书页上，它的表现就是瞎猜，这也是必然的。"
        "<bookmark mark='b'/>所以，同一个网络能记住任何东西。那么，数一数模型能拟合什么，就解释不了为什么在真实标签下，它找到的是一条在新书页上管用的规则。"
        "它的训练方式里，一定有什么东西偏爱简单的答案。接下来的两章，会在最简单的情形下证明这一点。",

    '"In what order does it memorize?':
        "它按什么顺序记住？把打乱后的书页分成两半：碰巧大约一半拿回了自己真实的作者，其余的拿到的是错的。<bookmark mark='a'/>网络判对一页打乱后的标签，"
        "这一页就亮起来。<bookmark mark='b'/>{order}有{int(r['n_params']):,}个权重来记{len(lab)}页，记住是很快的事。",

    "f'In the first few steps, the pages whose label happens to be true":
        "最初几步里，标签碰巧是真的那些书页领先：到第{int(steps[kg])}步，它们有{100 * ya[kg]:.0f}%判对了，其余的只有{100 * yd[kg]:.0f}%。"
        "网络先学到的，是两位作者真正的区别。然后它把剩下的记住，到第{int(steps[full])}步，每一页，不管标签真假，都拟合了。",

    "f'Both halves are fit at much the same pace":
        "两半拟合的速度差不多，到第{int(steps[full])}步全部拟合：这里网络没有先学到真正的规律，就直接记住了。",

    'f"Zhang and colleagues also turned the dial gradually':
        "张驰原和同事们还把旋钮一点点拧大，把越来越多的标签换成抛硬币。这是在书页上做的结果，每种设置三个随机种子。<bookmark mark='a'/>新书页上的准确率，"
        "从标签干净时的{100 * a0:.0f}%，降到全部随机时的{100 * a1:.0f}%{steady}<bookmark mark='b'/>而在每种设置下，网络都拟合了每一个训练标签，{pace}"
        "同样的网络，同样的训练，同样为零的训练误差，在新数据上却可以从极好一直到毫无用处。它学到什么取决于标签；任何只看网络、不看数据的度量，"
        "都分不清这些情形。",

    'f"taking longer the more labels are noise':
        "噪声标签越多，花的时间越长：标签干净时大约{f0:.0f}步，全部随机时{f1:.0f}步。",

    "f'in about {f0:.0f} to {f1:.0f} steps whatever the noise":
        "不管噪声多少，大约{f0:.0f}到{f1:.0f}步：在448页上，记住是很便宜的。",

    # ------------------------------------------------------------------ MinNorm
    "Chapter ten. Implicit bias: the smallest fit.":
        "第10章。隐式偏好：最小的拟合。",

    "When a model has more weights than training examples":
        "当模型的权重比训练样本还多时，它通常能把样本全部精确拟合，而且有无穷多种拟合法。三个权重，两个方程：<bookmark mark='a'/>这条线上的每一点，"
        "都同时精确满足两个方程。训练会挑哪一个？<bookmark mark='b'/>在平方误差上做梯度下降，从0出发。每一步都沿着输入的某个组合移动，所以路径永远离不开"
        "输入张成的那个平面。<bookmark mark='c'/>它和精确拟合的那条线交于一点：离原点最近的那一点，也就是权重最小的拟合。",

    "The proof is five lines.":
        "证明只有五行。<bookmark mark='a'/>一步梯度下降，减去的是X转置乘以残差。<bookmark mark='b'/>从0出发，每个迭代点都是训练输入的组合：它待在X的行空间里。"
        "<bookmark mark='c'/>步长足够小时，损失是凸的，会降到0，所以极限拟合了每一个样本。<bookmark mark='d'/>行空间里只有一个精确拟合：X转置乘以X乘X转置的逆、"
        "再乘以y，也就是伪逆解。<bookmark mark='e'/>任何别的精确拟合，都和它相差一个垂直于行空间的向量，所以由勾股定理，它更长。没人告诉梯度下降，"
        "它却选中了最小范数的拟合。这就是隐式偏好：算法自带的一种偏爱，没有哪个损失函数提出过这种要求。",

    'f"Check it with {n} equations in {d} unknowns.':
        "用{n}个方程、{d}个未知数来检验。<bookmark mark='a'/>从0出发，到伪逆解的距离一路下降，直到碰到双精度的极限，而权重在行空间之外的部分，自始至终"
        "都停在舍入误差的水平。<bookmark mark='b'/>换一个起点，梯度下降仍然满足每个方程，却停在离最小范数拟合{d1[-1]:.2f}远的地方，{which}所以答案也取决于起点："
        "网络从0附近、用很小的随机权重开始，而本系列的第9部分，讲的正是怎样选这个尺度。",

    "exactly the part of the starting point":
        "恰好是起点落在行空间之外的那一部分，任何一步都碰不到它。",

    "close to the part of the starting point":
        "接近起点落在行空间之外的那一部分。",

    # ------------------------------------------------------------------ MaxMargin
    "Chapter eleven. Implicit bias: the widest margin.":
        "第11章。隐式偏好：最宽的间隔。",

    'f"Classification has its own version.':
        "分类也有它自己的版本。当两类可以分开时，只要把权重放大，逻辑斯蒂损失就能要多小有多小，所以根本没有最小值，能分开它们的直线也有无穷多条。"
        "<bookmark mark='a'/>梯度下降朝哪个方向走？这里一步步地看，步数取对数刻度。走了一步之后，边界离间隔最宽的那条线有{a0:.0f}度。"
        "<bookmark mark='b'/>走了一百步，{rec[idx[0], 1]:.1f}度；一万步，{rec[idx[1], 1]:.1f}度；一百万步，{rec[idx[2], 1]:.1f}度。它慢慢转向支持向量机的那条线，"
        "而权重一直在变大，损失一直在变小。",

    "Why that line?":
        "为什么是那条线？<bookmark mark='a'/>负梯度是样本的一个加权和，每个样本的权重，取决于它被分得有多差。<bookmark mark='b'/>一旦每个点都判对了、"
        "权重又很大，这些权重就是负间隔的指数。<bookmark mark='c'/>指数衰减得太快，间隔最小的那些点压倒了其他一切：只有支持向量在掌舵。"
        "<bookmark mark='d'/>方向收敛到支持向量的一个正系数组合，这正是第4部分KKT条件下最大间隔解的形式。苏德里和同事们在2018年证明了这一点，还给出了速度："
        "权重像log t那样增长，方向的误差像log t分之1那样缩小。2020年，吕凯风和李建把它推广到了齐次神经网络。",

    'f"Measure it. <bookmark mark=\'a\'/> On a log axis of steps':
        "量一量。<bookmark mark='a'/>在步数的对数轴上，权重的范数是一条直线：步数每增加十倍，它大约增长{slope * math.log(10):.2f}，这是对数增长。"
        "<bookmark mark='b'/>角度在下降，很慢。{pace}一百万步之后，间隔是{m['margin_end']:.3f}，而最好可能是{m['gamma']:.3f}。这种慢有实际的一面："
        "训练误差到0之后很久，继续训练仍在改变模型，朝着更大的间隔，这又是提升法的故事，只不过现在成了关于梯度下降的定理。",

    "Angle times log t is nearly constant":
        "从一千步起，角度乘以log t几乎不变：正是log t分之1的速度。",

    'f"Angle times log t falls from':
        "在一千步到一百万步之间，角度乘以log t从{m['c_hi']:.0f}降到{m['c_lo']:.0f}，所以这里它收敛得仍比定理的最坏情形，也就是log t分之1，要快。",

    # ------------------------------------------------------------------ DoubleDescent
    "Chapter twelve. Double descent.":
        "第12章。双下降。",

    'f"Here\'s the curve that came back.':
        "这就是那条又降回来的曲线。把每一页变成p个随机特征：每个特征是70个词频的一个固定的随机组合，再经过一个把负数归零的弯折。只有特征上的权重"
        "是学出来的，用最小二乘法。<bookmark mark='m'/>特征比书页多时，有许多种拟合都能精确对上每个训练页，那就取权重最小的那个：在所有穿过这些点的曲线里，"
        "最平静的那条。<bookmark mark='a'/>特征少时，新书页上的误差先下降，然后随着p接近书页数又上升：这是经典的U形。<bookmark mark='b'/>恰好有{n}个特征，"
        "和书页一样多时，拟合被迫穿过每一个点，误差爆炸了。<bookmark mark='c'/>然后，越过这一点，误差又降了下来{how_low}",

    'f"{opening}Belkin and colleagues named it double descent':
        "{opening}2019年，贝尔金和同事们把它命名为双下降，同一年，纳基兰和同事们在深度网络里也发现了它。<bookmark mark='a'/>在整个第二次下降中，"
        "训练误差都是0，所以决定结果的不可能是它。决定结果的是你拿到的是众多精确拟合中的哪一个，而最小的那个最简单。<bookmark mark='n'/>{size}"
        "再联系第10章：从0出发的梯度下降，找到的恰好就是那个最小的拟合。",

    "More parameters than data, and better":
        "参数比数据多，在新数据上反而更好。",

    "More parameters than data, and still good":
        "参数比数据多，在新数据上依然不错。",

    "f'Its size tells the story":
        "它的大小说明了一切：在峰值处，拟合是被迫的，权重爆炸了，然后随着特征增加而缩小{ending}",

    "Past the peak, the smallest fit's weights shrink":
        "越过峰值后，最小拟合的权重随着特征增加而缩小。",

    'f"Why the peak, exactly at p equals n?':
        "为什么峰值恰好在p等于n处？用特征矩阵的奇异值分解，写出最小范数拟合。<bookmark mark='a'/>它是对各个方向求和，每个标签分量都除以它的奇异值σᵢ。"
        "<bookmark mark='b'/>标签里有一部分是任何特征都解释不了的噪声。<bookmark mark='c'/>这一部分被σ分之1放大，它的期望大小是噪声方差乘以σ²分之1的和。"
        "所以一切都系于最小的奇异值。<bookmark mark='d'/>这是p增大时特征矩阵的奇异值。特征少时，它们都离0很远。<bookmark mark='e'/>随着p接近n，最小的那个"
        "滑向0，在p等于n时只有{sm[kn]:.4f}：一个随机的方阵几乎是奇异的。<bookmark mark='f'/>越过这一点，特征比书页多时，最小奇异值又升了回来，"
        "噪声被分摊到几乎不影响新书页的那些方向上。",

    'f"The cure follows':
        "治法随之而来：别除以很小的数。岭回归给每个σ²都加上λ，于是最小的那些方向被压低，而不是被放大。<bookmark mark='a'/>λ取p的{lams[best]:g}倍时，"
        "在{n}个特征处的峰值消失了：那里的误差是{rd[kn, best]:.2f}，不加岭回归时是{te[kn]:.1f}。<bookmark mark='b'/>岭太小，留下一个鼓包；太大，"
        "拟合处处都太保守。纳基兰和同事们在2020年证明，调好的正则化能消除这类模型里的峰值。这个峰值从来不是什么自然规律：它是在特征刚刚够用时，"
        "精确拟合噪声造成的假象。",

    # ------------------------------------------------------------------ MoreDescents
    "Chapter thirteen. Double descent in samples":
        "第13章。样本数上的双下降，以及训练轮数上的双下降。",

    'f"If the peak sits where the number of parameters':
        "如果峰值出现在参数个数等于样本个数的地方，那么从另一边也能走到它。固定{p}个随机特征，给模型越来越多的书页。<bookmark mark='a'/>{rise}"
        "<bookmark mark='b'/>{after}<bookmark mark='c'/>加一点岭回归，曲线就只是下降。2019年，纳基兰和同事们在深度网络里发现了这种按样本数的版本："
        "对一个固定的模型，存在一个范围，在那里更多的数据反而有害。",

    "f'From {int(ns[j])} pages to":
        "从{int(ns[j])}页到{int(ns[k])}页，新书页上的误差上升了，从{med[j]:.2f}升到{med[k]:.1f}：更多的数据让模型变差了，因为更多的书页把它推向"
        "刚刚能拟合它们的那一点。",

    "The error doesn't rise here":
        "这里误差没有上升；更多的数据始终有帮助。",

    "Beyond that, more data helps again.":
        "越过那一点，更多的数据又有帮助了。",

    '"Nakkiran and colleagues also saw it in time':
        "纳基兰和同事们还在时间上看到了它：把一个网络训练得越来越久，它的测试误差可以先降、再升、又降。能做到这一点的最简单模型是线性的，"
        "输入有两种差别很大的尺度。<bookmark mark='a'/>梯度下降先学会大尺度的方向。{s1}<bookmark mark='b'/>{s2}<bookmark mark='c'/>{s3}"
        "<bookmark mark='d'/>按方向拆开，就是两条偏差–方差曲线，一快一慢，叠加在一起：这是黑克尔和耶尔马兹2021年的解释。训练误差自始至终都在下降。"
        "什么时候停止训练，不是一个只有一个答案的问题，第12部分的顿悟把这一点推到了极端。",

    "f'The test error falls, to its first low":
        "测试误差下降，在第{int(ts[i1])}步到达第一个低点，",

    'f"then rises, to a peak around step':
        "然后上升，在大约第{int(ts[i2]):,}步达到峰值，因为那些快的方向，正在把属于它们的那份噪声，以及它们表示不了的信号，拟合完。",

    "f'Only then do the slow directions":
        "直到这时，那些慢的方向，也就是装着其余信号的方向，才被学会，误差再次下降，降到{med[-1]:.2f}，远低于第一个低点。",

    "Here the error falls without a second rise.":
        "这里误差一路下降，没有第二次上升。",

    # ------------------------------------------------------------------ Benign
    "Chapter fourteen. Benign overfitting.":
        "第14章。良性过拟合。",

    "Double descent showed fits that pass through every noisy label":
        "双下降展示了穿过每个带噪声标签、却依然表现很好的拟合。精确拟合噪声，怎么会是无害的？<bookmark mark='a'/>一种插值的方法，是把整条曲线弯过去，"
        "去够每一个点；这会把各处的预测都弄坏。<bookmark mark='b'/>另一种，是几乎处处都沿着光滑的真相走，再用一根细细的尖刺，去够每个带噪声的标签，"
        "而这根尖刺几乎碰不到任何别的输入。这样的拟合训练误差为0，在新数据上却几乎和真相一样好。在高维空间里，这些尖刺是免费的。",

    'f"Bartlett, Long, Lugosi and Tsigler made this exact':
        "巴特利特、朗、卢戈西和齐格勒在2020年针对线性回归，把这一点讲得精确了。拿一百个带噪声的样本，信号只在五个强的方向上，用最小范数解把它们精确拟合。"
        "<bookmark mark='a'/>加上D个弱的方向，它们的总方差加起来很小：随着D增大，超额误差下降，有{int(Ds[-1]):,}个时降到{sp[-1]:.3f}，是噪声水平的"
        "{100 * sp[-1] / noise:.0f}%，尽管拟合复现了每一个带噪声的标签。这是良性的。<bookmark mark='b'/>换成加上D个和信号一样强的方向，超额误差就攀升到"
        "{iso[-1]:.1f}：拟合把权重摊到了要紧的方向上，丢掉了信号。这是有害的。",

    "Their theorem splits the excess error":
        "他们的定理把超额误差拆成一个偏差，以及一个方差，方差是噪声乘以两项。<bookmark mark='a'/>第一项拿强方向的个数和样本数比。<bookmark mark='b'/>"
        "第二项拿n和尾部的有效秩比：有多少个方向分担那点弱的方差。许多个小方向，每个都能吸收一点噪声，而不怎么移动预测：这些就是尖刺。"
        "<bookmark mark='c'/>而尾部作为整体，就像对强方向施加了一个岭惩罚，代价是一点偏差。<bookmark mark='d'/>所以，当信号是低维的、其余是一长串很小的方向时，"
        "插值就是良性的，真实数据和宽网络往往正有这样的谱。对真实的网络，情形多半介于两者之间：马利纳尔和同事们在2022年称之为温和过拟合。",

    # ------------------------------------------------------------------ Sharpness
    "Chapter fifteen. Flat minima":
        "第15章。平坦极小值，以及尖锐度之争。",

    "An older idea about why networks generalize":
        "关于网络为什么能泛化，有一个更早的想法：训练最后落进的那个山谷的形状。<bookmark mark='a'/>假设测试损失就是训练损失挪动了一点，因为测试数据"
        "和训练数据有一点不同。在平坦山谷的谷底，这点挪动几乎不花代价；在尖锐山谷的谷底，代价就大了。<bookmark mark='b'/>霍赫赖特和施密德胡伯在1997年认为，"
        "平坦的极小值更简单：它们的权重可以用更少的比特写下来。2017年，凯斯卡尔和同事们报告说，用大批量训练会找到更尖锐的极小值，泛化得也更差。",

    'f"Test it, small.':
        "在小规模上检验一下。{len(lam)}个网络从{s['n']}个由一个教师网络标注的点学习，用四种批量大小、两种步长和三个随机种子，{fit}。尖锐度是训练损失的"
        "黑塞矩阵的最大特征值，用第4部分的黑塞-向量积来量。<bookmark mark='a'/>{batches}<bookmark mark='b'/>{corr}大规模的研究至少在这一点上一致："
        "在许多设置下，尖锐度对泛化的预测并不稳定，安德留先科和同事们在2023年就是这样发现的。",

    "each trained until its training loss is equally small":
        "每个都训练到训练损失同样小为止",

    "each trained until its training loss is small, or for at most":
        "每个都训练到训练损失很小为止，或者至多训练四千轮",

    "f'Large batches do end sharper":
        "大批量确实停在更尖锐的地方：平均{big:.1f}，而批量为4时是{small:.2f}。",

    "f'Here large batches end flatter":
        "这里大批量反而停在更平坦的地方，而不是更尖锐：{big:.2f}，而批量为4时是{small:.2f}。",

    "f'And the sharper networks do worse":
        "而更尖锐的网络在新的点上确实更差：秩相关系数是{rho:+.2f}。平坦极小值的说法在这里成立。",

    "f'But the sharper networks are not the worse ones":
        "但更尖锐的网络并不是更差的那些：尖锐度和测试误差的秩相关系数是{rho:+.2f}。{lean}",

    "If anything, the sharper ones generalize better here.":
        "要说有什么区别，这里更尖锐的反而泛化得更好。",

    "Sharpness tells us almost nothing here.":
        "这里尖锐度几乎说明不了什么。",

    'f"There\'s a deeper problem':
        "还有一个更深的问题，是丁、帕斯卡努和两位本吉奥在2017年指出的。<bookmark mark='a'/>ReLU会把一个正的缩放原样传过去。<bookmark mark='b'/>所以把第一层"
        "乘以a，第二层除以a，网络计算的就是完全相同的函数，{exactly}。同样的预测，同样的测试误差。<bookmark mark='c'/>但在这些缩放之间，它的尖锐度"
        "变了{rng_:.0f}倍。量出来的尖锐度，取决于权重是怎么写下来的，而不只取决于网络在做什么，所以它不可能是全部的解释。后来有了不随缩放改变的版本，"
        "也有了专门去找平坦区域的训练方法，比如锐度感知最小化；尖锐度和步长有什么关系，是第11部分的稳定性边缘要讲的。",

    "f'to within {s":
        "误差在每个输出上都不超过{s['same']:.3f}",

    # ------------------------------------------------------------------ Shift
    "Chapter sixteen. Distribution shift.":
        "第16章。分布偏移。",

    "Everything so far assumed the test data comes from":
        "到目前为止，一切都假设测试数据和训练数据来自同一个分布。往往并非如此。这里真实的关系是一个三次函数，<bookmark mark='a'/>训练输入聚集在0.5附近，"
        "<bookmark mark='b'/>而我们将要被测试的输入聚集在0附近。从x到y的规则没有变，变的只是输入落在哪里：这叫协变量偏移。<bookmark mark='c'/>用最小二乘法"
        "拟合一条直线，它照顾的是训练区域，也就是大多数点所在的地方。<bookmark mark='d'/>按每个训练点的x在测试分布下可能性大多少来加权，这条直线就转过来，"
        "去照顾测试输入将要出现的地方。",

    "Why weights?":
        "为什么要加权？<bookmark mark='a'/>我们关心的风险，是对测试分布q求损失的平均。<bookmark mark='b'/>乘以再除以训练分布p。<bookmark mark='c'/>"
        "现在它变成了对训练输入求平均，求的是损失乘以比值q比p。<bookmark mark='d'/>所以加权后的训练误差，是测试误差的无偏估计。下平英寿在2000年提出了它。"
        "<bookmark mark='e'/>代价就是第5部分在重要性采样里遇到的那个：少数权重很大的点占了主导，有效样本量缩小了。",

    'f"Over a thousand runs of {n} training points':
        "跑一千次，每次{n}个训练点：普通的最小二乘法，测试误差是{r_ols:.3f}。<bookmark mark='a'/>{exact}<bookmark mark='b'/>把权重压平，取比值的平方根，"
        "是用一点偏差换更小的方差；{flat}：{s['flat_mean']:.3f}。<bookmark mark='c'/>实际中没人知道q比p。但一个训练来区分训练输入和无标签测试输入的分类器，"
        "能从它给出的几率估计出这个比值：{r_est:.3f}。<bookmark mark='d'/>精确的权重只留下{s['ess_mean']:.0f}个有效样本，总共{n}个。而协变量偏移还是"
        "容易的情形：当标签的频率变了，或者规则本身在漂移，补救办法就不一样了，有时甚至根本没有。第31部分会回到这个问题，把它当作在像真实世界那样的"
        "数据上评估模型的问题。",

    "f'Weighting by the exact ratio brings it to":
        "按精确的比值加权，误差降到{r_iw:.3f}，接近任何直线对测试输入所能做到的最好结果{s['best_risk']:.3f}。",

    "f'Weighting by the exact ratio gives":
        "按精确的比值加权，得到{r_iw:.3f}：这里没有明显的好处。",

    # ------------------------------------------------------------------ Memorization
    "Chapter seventeen. Memorization in language models.":
        "第17章。语言模型里的记忆。",

    "The last chapter is about what a model remembers exactly.":
        "最后一章讲模型会一字不差地记住什么。泛化不是照抄，但大模型两样都做。<bookmark mark='a'/>2019年，尼古拉斯·卡里尼和同事们把随机的秘密埋进训练数据，"
        "测量模型有多容易把它们吐出来。<bookmark mark='b'/>2021年，他们通过采样和筛选，从GPT-2里挖出了训练文本：一千八百个候选里，有六百多个是训练文档的逐字副本，"
        "其中一些带着姓名和联系方式。<bookmark mark='c'/>2023年，他们在大规模上做了测量：记忆随着模型大小、一段文字重复的次数，以及提示的长度，"
        "呈对数线性增长；有六十亿参数的GPT-J，至少记住了它训练数据的1%。<bookmark mark='d'/>他们的测试是：给模型一段来自训练数据的前缀，看贪心解码"
        "能不能一字不差地接下去。",

    'f"Run that test on our own novels model.':
        "在我们自己的小说模型上做这个测试。它的训练文本有{mtok:.1f}百万个词元，长段落很少重复：没有哪个64词元的段落出现超过{mmax}次。<bookmark mark='a'/>"
        "用一段训练文本的前32个词元作提示，在试过的{n_tried}个里，它一字不差地接出后32个的有{n_ex}个。<bookmark mark='b'/>{further}<bookmark mark='c'/>"
        "一个只把文本看过几遍的小模型，记住的是风格，而不是字句。让字句记牢的，是重复。",

    "f'But it gets further before its first mistake":
        "但对见得更多的段落，它在第一次出错前走得更远：只见过一次的段落，平均{r0:.1f}个词元；见过{topbin}次的，{rN:.1f}个；而从没见过的文本是{vrun:.1f}个。",

    "f'On average it gets {r0:.1f} tokens right":
        "平均来说，它在第一次出错前能接对{r0:.1f}个词元，和从没见过的文本差不多，那里是{vrun:.1f}个。",

    'f"To see repetition at work, plant it.':
        "要看重复怎样起作用，就把它种进去。在模型自己的文本上继续训练它，文本里种进它从没见过的段落：{per}段各种一次，另{per}段各种两次，以此类推，"
        "一直到{gN}次，还有{per}段从不种进去，作对照。<bookmark mark='a'/>在{S}步训练中，种得最多的段落最先变得可提取。<bookmark mark='b'/>最后："
        "只见过一次的段落有{e1:.0f}%、种了8次的有{e8:.0f}%、种了{gN}次的有{eN:.0f}%能一字不差地复现；对照组是{eC:.0f}%。{halfway}"
        "<bookmark mark='c'/>{trend}",

    "f'Half or more are extractable from":
        "从重复{g_half}次起，一半以上都可以提取。",

    "Extraction climbs with repetition":
        "可提取的比例随重复次数攀升，这和卡里尼及同事们、坎德帕尔及同事们在大规模上的发现一致；这也是对训练数据去重成为标准做法的原因。",

    "The trend with repetition is noisy":
        "在这个规模上，随重复次数变化的趋势有些杂乱，但它和卡里尼及同事们、坎德帕尔及同事们在大规模上发现的趋势一致，这也是对训练数据去重成为标准做法的原因。",

    "Since then, memorization has become":
        "从那以后，记忆成了一个实际的问题，也成了一个法律问题。<bookmark mark='a'/>对训练数据去重能减少记忆。<bookmark mark='b'/>2023年，纳斯尔和同事们发现，"
        "让一个聊天模型把一个词永远重复下去，它会渐渐跑偏，开始背诵训练数据。<bookmark mark='c'/>2025年，库珀和同事们证明，一些开放权重的模型记住了"
        "流行书籍的大段内容。<bookmark mark='d'/>法院对这意味着什么看法不一。2025年11月，慕尼黑的一家法院认定，模型记住的歌词就是一份复制品，"
        "这一判决仍在上诉中；<bookmark mark='e'/>而伦敦的高等法院认定，一个图像模型的权重不是复制品。那年6月，美国的法官认定训练本身属于合理使用。"
        "<bookmark mark='f'/>2026年初，研究者报告从一些商用聊天模型里提取出了几乎完整的书。一个模型是学会了还是抄下了，已经不只是学习理论的问题了。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来盘点一下。风险是世界可能送来的一切数据上的误差；训练误差会高估模型，而差距可以分成近似和估计两部分。误差可以分解为偏差、方差和噪声。"
        "由霍夫丁不等式，一条规则的测试分数是可信的；在许多条里挑选，代价是它们个数的对数；一个无穷的规则族，代价是它的增长函数，由绍尔和谢拉，"
        "这是一个多项式。拉德马赫复杂度和间隔用权重的大小来衡量容量；PAC-贝叶斯、压缩和稳定性给出的界，即使对网络也能说明些什么，我们的就是这样。"
        "然后是那些谜题：网络能记住噪声，梯度下降选中最小的拟合和最宽的间隔，误差会两次下降，过拟合可以是良性的，而平坦并不是全部的解释。"
        "当数据移动或重复时，泛化就让位给加权，也让位给记忆。",

    "Margins return in part nine":
        "间隔会在第9部分的感知机收敛证明里重现。训练会找到哪个极小值、它有多尖锐，是第11部分的主题。远大于数据的模型、顿悟和规模定律，"
        "是第12部分的主题。而留出分数、被污染的测试集、记忆与隐私，会在我们深入模型内部、追问能否信任它们的时候，在第30和第31部分回来。",

    "Here are six problems to try":
        "这里有六道习题可以试一试，从确定测试集要多大，到重要性权重的方差。在这里暂停，自己做一做；完整的解答在本部分的笔记里。",

    "Next time: networks themselves.":
        "下一次：网络本身。从感知机和它经历的寒冬，讲到反向传播；为什么一叠简单的层能逼近任何函数，深度怎样把空间切成一块块，以及怎样初始化、"
        "怎样让信号穿过很多层还保持活力。<bookmark mark='a'/>还有，第一个神经语言模型会登上记分牌。",

    "Shalev-Shwartz and Ben-David":
        "沙莱夫-施瓦茨和本-戴维的《理解机器学习》（Understanding Machine Learning），是讲这套理论最清楚的书，弗朗西斯·巴赫的《从第一性原理出发的学习理论》"
        "（Learning Theory from First Principles）是最新的。感谢收看，第9部分再见。",

    # short spliced clauses (also in PHRASES, for exact matches)
    ": for independent rules it's nearly tight.": "：对彼此独立的规则来说，它几乎是紧的。",
    ", shallower than the predicted minus one.": "，比预测的负1平缓。",
    ", close to the predicted minus one.": "，接近预测的负1。",
    ", steadily, as the share of wrong labels grows.": "，随着错误标签的比例增加而稳步下降。",
    ", though not quite to the bottom of the U.": "，不过没有完全降到U形的底部。",
    ", lower than the bottom of the U.": "，比U形的底部还低。",
    ", ending smaller than at the bottom of the U.": "，最后比在U形底部时还小。",
}

PHRASES = {
    # Hoeffding: tight
    ": for independent rules it's nearly tight. ": "：对彼此独立的规则来说，它几乎是紧的。",
    ": for independent rules it's nearly tight.": "：对彼此独立的规则来说，它几乎是紧的。",
    ". ": "。",
    ".": "。",
    # Margins: end
    "and stays there. ": "之后保持在那里。",
    "and stays there.": "之后保持在那里。",
    # Stability: close
    ", close to the predicted minus one.": "，接近预测的负1。",
    ", shallower than the predicted minus one.": "，比预测的负1平缓。",
    # RandomLabels: steady
    ", steadily, as the share of wrong labels grows. ": "，随着错误标签的比例增加而稳步下降。",
    ", steadily, as the share of wrong labels grows.": "，随着错误标签的比例增加而稳步下降。",
    ", though not evenly. ": "，不过降得并不均匀。",
    ", though not evenly.": "，不过降得并不均匀。",
    # DoubleDescent: how_low, ending
    ", lower than the bottom of the U.": "，比U形的底部还低。",
    ", though not quite to the bottom of the U.": "，不过没有完全降到U形的底部。",
    ", ending smaller than at the bottom of the U. ": "，最后比在U形底部时还小。",
    ", ending smaller than at the bottom of the U.": "，最后比在U形底部时还小。",
    # MoreDescents: empty sentences
    "": "",
    # Sharpness: exactly
    "to rounding error on every output": "每个输出都只差舍入误差",
    # Shift: flat
    "here that pays": "在这里是划算的",
    "here it doesn't quite pay": "在这里不太划算",
}
