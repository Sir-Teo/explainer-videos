"""Chinese narration for ai16: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第16部分：稀疏'

CHAPTERS = {
    'Hook': '一次只用几个专家',
    'Origins': '1. 相互竞争的专家，1991',
    'Router': '2. top-k门控与路由器的梯度',
    'Ours': '3. 训练一个混合专家模型',
    'Balance': '4. 坍缩，与Switch的损失',
    'LossFree': '5. 不靠损失的负载均衡',
    'Fine': '6. 细粒度专家与共享专家',
    'Capacity': '7. 容量与被丢弃的词元',
    'Parallel': '8. 分布在多块芯片上的专家',
    'Counting': '9. 数参数，以及升级',
    'Special': '10. 专家学到了什么',
    'Depth': '11. 深度混合',
    'Mass': '12. 注意力有多稀疏？',
    'Designs': '13. 设计出来的稀疏注意力',
    'Lottery': '14. 彩票假设',
    'Structured': '15. 四选二，以及稀疏的激活',
    'Frontier': '16. 前沿，2026年末',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    'f"DeepSeek-V3 has six hundred and seventy-one billion parameters.':
        "DeepSeek-V3有6710亿个参数。<bookmark mark='a'/>可它每读一个词元，只用其中的{ds['active'] / 1000000000.0:.0f}0亿个。"
        "它的每个专家层里有{n}个小网络，叫作专家；路由器把每个词元只送到其中{k}个，外加一个人人共享的专家。"
        "<bookmark mark='b'/>看：每个词都点亮不同的几个。<bookmark mark='c'/>而模型还在变得更稀疏。2026年7月发布的Kimi K3，"
        "每层有{k3['experts']}个专家，每个词元用其中{k3['k']}个，外加{k3['shared']}个共享专家：每个词元只用到它"
        "{100 * k3['frac']:.1f}%的权重。",

    'How did we get here? Three threads, which this part follows.':
        "我们是怎么走到这一步的？有三条线索，这一部分会一条条讲。<bookmark mark='a'/>第一条是专家。1991年，罗伯特·雅各布斯、"
        "迈克尔·乔丹、史蒂文·诺兰和杰弗里·辛顿提出：用一个门控，来决定几个网络里该由哪一个作答。<bookmark mark='b'/>2017年，"
        "诺姆·沙泽尔和同事们，辛顿也在其中，让它变得稀疏：成千上万个专家，每个词元只运行几个，参数多达1370亿。"
        "<bookmark mark='c'/>谷歌用GShard和Switch Transformer把它做大，做到1.5万亿参数；2023年Mixtral把它开源，"
        "DeepSeek-V3又让它成了前沿的标准做法。<bookmark mark='d'/>第二条线索，是只读一部分过去内容的注意力："
        "2019年起的固定模式，滑动窗口，以及2025年由模型自己学会挑选的模式。<bookmark mark='e'/>第三条最古老：去掉权重。"
        "1990年扬·勒丘恩的最优脑损伤，2018年的彩票假设，还有2020年英伟达做进芯片里的四选二模式。",

    'This is Part 16 of AI, Built: using only some of a model at a time.':
        "这是《人工智能，从零搭建》的第16部分：每次只用模型的一部分。<bookmark mark='a'/>本部分的内容：混合专家，"
        "从1991年的起源讲到路由器的梯度，并在我们自己的字符数据上训练；怎样让每个专家都有活干，推导Switch的损失，"
        "再讲DeepSeek不靠损失的偏置；容量、芯片和参数的计数；专家学到了什么，以及深度混合；只读一部分过去内容的注意力，"
        "在一个回忆任务上训练；最后是稀疏的权重和激活，从彩票假设讲到四选二模式。每个实验都在这台电脑上跑。",

    # ---------------------------------------------------------------- Origins
    'Chapter one. Competing experts, 1991.': '第1章。相互竞争的专家，1991。',

    'In 1991 the question was how to make several networks share one job':
        "1991年的问题是：怎样让几个网络分担同一份工作，而不是训练一个网络什么都做。<bookmark mark='a'/>雅各布斯、乔丹、"
        "诺兰和辛顿的答案，就是混合专家。几个小网络，也就是专家，各自给出一个猜测；一个门控，就是再加一个矩阵和一个softmax，"
        "决定对这个输入该多信任每一个专家。答案就是按信任程度混合起来的结果。<bookmark mark='b'/>门控给出的数，"
        "就像第7部分的混合权重，只不过它们随输入而变：对一个输入，门控倚重专家2；对另一个输入，倚重专家4。"
        "<bookmark mark='c'/>他们的测试，是分辨许多人说出的元音。",

    'The new idea was in the loss.':
        "新意在损失函数里。<bookmark mark='a'/>最直接的损失是拟合混合结果：门控加权和的平方误差。<bookmark mark='b'/>"
        "它的梯度让每个专家都去追混合结果的误差，于是每个专家学什么，都取决于其他所有专家：它们在合作，"
        "结果每个专家对所有事情都负一点责任。<bookmark mark='c'/>雅各布斯和同事们换了个做法：把这些专家看成一个高斯混合，"
        "也就是第7部分的混合模型，去最小化负对数似然。<bookmark mark='d'/>这样一来，每个专家追的是自己的误差，"
        "<bookmark mark='e'/>再乘上h，也就是它恰好是负责者的后验概率：门控有多信任它，乘以它对答案已经解释得有多好。"
        "第7部分的EM管这个叫责任。一个专家，从它本来就赢的样本里学得最多。它们相互竞争，于是成了专才。",

    '"Here\'s that difference, trained on this computer.':
        "这就是两者的区别，在这台电脑上训练出来。一条曲线有三段：上升、平台、下降；四个专家各自只能画一条直线，"
        "门控看着x来分配。<bookmark mark='a'/>同一个混合模型，用两种方式训练。注意曲线下方的门控。<bookmark mark='b'/>"
        "{verdict}<bookmark mark='v'/>{own}",

    "f'Competing, the gate ends up sure of itself":
        "竞争的时候，门控最后很有把握：平均把{100 * sa[0]:.0f}%的信任给了同一个专家；合作的时候只有{100 * sb[0]:.0f}%，"
        "两种各跑了3个随机种子。",

    "f'Here the two end up about equally decided":
        "这里两种方式最后差不多一样果断：竞争时把{100 * sa[0]:.0f}%的信任给一个专家，合作时是{100 * sb[0]:.0f}%。",

    "f'With competition, {min(oa)} to {max(oa)} experts":
        "竞争的时候，有{min(oa)}到{max(oa)}个专家各自占据曲线的一段，一段对应一种走势，混合结果拟合得{fit_word}：每个专家只做一件简单的事。",

    'In those early mixtures, every expert ran on every input':
        "在早期的混合模型里，每个专家对每个输入都要运行，门控只负责加权。<bookmark mark='a'/>1994年，乔丹和雅各布斯把门控"
        "叠成层级结构，用EM来训练。<bookmark mark='b'/>2017年，诺姆·沙泽尔和谷歌的同事们，把混合专家变成了一种扩大模型的办法。"
        "只保留门控分数最高的k个，其余的设为负无穷，这样它们的门控正好是0，那些专家根本不用运行。<bookmark mark='c'/>"
        "再给分数加一点噪声，让路由器不停地试试别的专家。<bookmark mark='d'/>这样，专家的数量可以一直增长，"
        "而每个词元的计算量不变：他们在LSTM的层与层之间放了成千上万个专家，参数达到1370亿，容量是以前模型的一千多倍。"
        "这一部分里的每个模型，用的都是这种稀疏的混合专家。",

    # ---------------------------------------------------------------- Router
    "Chapter two. Top-k gates, and the router's gradient.": '第2章。top-k门控，与路由器的梯度。',

    "Here's one layer of a modern mixture of experts.":
        "这是现代混合专家模型的一层。每个Transformer块里的前馈网络，变成了几个更小的网络，也就是专家。"
        "<bookmark mark='a'/>路由器，只是一个矩阵，给这个词元对每个专家打一个分。<bookmark mark='b'/>只有分数最高的k个算数："
        "这里是8个里挑2个。这些专家运行，其余的不运行。<bookmark mark='c'/>它们的输出按门控加权相加：门控是只在被选中专家的"
        "分数上做的softmax，所以加起来等于1。这是Mixtral的门控，也是大多数模型用的门控。",

    'What does the router learn from? Take the gradient of the loss':
        "路由器从哪里学？对某个分数s j求损失的梯度。<bookmark mark='a'/>输出只通过门控依赖分数，所以按链式法则，"
        "它是对被选中的专家求和：u i，也就是专家i的输出把损失推高多少，乘以门控的导数。<bookmark mark='b'/>门控是一个softmax，"
        "它的雅可比矩阵就是第4部分的g i乘以括号里δ i j减g j。<bookmark mark='c'/>把各项合起来：梯度等于g j乘以u j减u bar，"
        "u bar是被选中专家按门控加权的平均。一个被选中的专家，帮得比平均多，它的分数就被调高；帮得少，就被调低。"
        "<bookmark mark='d'/>而没被选中的专家没有门控，它的分数完全得不到梯度。<bookmark mark='e'/>路由器只能了解它试过的专家。"
        "一个没被选中的专家会不会做得更好，它永远不会知道。",

    'f"Let\'s check it. One token, eight experts':
        "来验证一下。一个词元，8个专家，都是随机的线性映射，选中前2个，用平方误差。<bookmark mark='a'/>把每个分数上下各挪动百万分之一，"
        "看损失怎么变：这就是有限差分求出的梯度。<bookmark mark='b'/>公式给出的柱子一样，自动微分也一样："
        "相对于最大的柱子，它们在小数点后{p1}位都一致。<bookmark mark='c'/>{E}根柱子里有{E - int(r['nonzero'])}根正好是0："
        "只有被选中专家的分数会动。我们在下一章要训练的混合专家层的路由器上做了同样的检验，它的每一个权重："
        "小数点后{p2}位都一致。",

    'Pause and predict. With one expert per token':
        "停下来预测一下。每个词元只用一个专家，而且门控重新归一化成1，路由器能学到什么？<bookmark mark='a'/>"
        "这是四种门控的并排比较。两个专家，用softmax或DeepSeek的sigmoid来混合，被选中的两个分数会学习。"
        "<bookmark mark='b'/>Switch的单个专家乘的是完整softmax的概率，所以通过softmax的分母，每个分数都会学习。"
        "<bookmark mark='c'/>但如果把单个专家的门控重新归一化，它就永远正好是1：路由器什么也学不到，永远学不到。"
        "这就是Switch保留原始概率的原因。<bookmark mark='d'/>不管哪种，路由器都只能从它试过的东西里学习；"
        "所以它需要噪声来探索，而且，后面几章会讲到，还需要帮助来分担工作。",

    # ---------------------------------------------------------------- Ours
    'Chapter three. A mixture, trained.': '第3章。训练一个混合专家模型。',

    'f"Now we build one.':
        "现在我们自己造一个。第13部分的Transformer，缩小到笔记本电脑跑得动：2个块，64个数宽，读三十部小说里的64个字符。"
        "<bookmark mark='a'/>第一个模型里，每个块的前馈层是稠密的，宽256。<bookmark mark='b'/>在混合专家模型里，它变成8个专家，"
        "每个宽度减半，路由器为每个字符挑2个：每个字符的计算量一样，用到大约{cm['active'] / 1000.0:.0f}千个参数，"
        "可总共有{cm['total'] / 1000.0:.0f}千个。<bookmark mark='c'/>第三个是拥有全部这些参数的稠密模型，前馈层宽4倍，"
        "计算量是3倍。每个模型都从3个随机种子各训练一次，用的是完全相同的字符。",

    '"Here are all nine runs.':
        "这是全部9次训练。在训练的8个时刻测留出数据上的每字符比特数；每条线是3个种子的平均，"
        "阴影带从最好的种子到最差的种子。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}",

    "f'The mixture pulls ahead of the dense model with the same arithmetic by step":
        "到第{when:,}步，混合专家模型超过了计算量相同的稠密模型，而且一直领先，每个种子都是这样：最后每字符{mv[0]:.3f}比特，"
        "对比{av[0]:.3f}。",

    "f'On average the mixture ends ahead":
        "平均来看，混合专家模型最后领先于计算量相同的稠密模型，{mv[0]:.3f}比特对{av[0]:.3f}，但3个种子里只有{wins}个是这样。",

    "f'The mixture does not beat the dense model":
        "混合专家模型没能胜过计算量相同的稠密模型：{mv[0]:.3f}比特对{av[0]:.3f}。",

    "f'The dense model with all the parameters does better still":
        "拥有全部参数的稠密模型更好，{tv[0]:.3f}，这也应该：它做了3倍的工作。混合专家模型走完了这段差距的"
        "{100 * (av[0] - mv[0]) / max(av[0] - tv[0], 1e-09):.0f}%，计算量只有它的三分之一。",

    "f'And the dense model with all the parameters, doing three times":
        "而拥有全部参数、计算量是3倍的稠密模型，最后是{tv[0]:.3f}：在同样短的训练之后，并不比混合专家模型更好。",

    'f"And here is the mixture\'s routing as it trains':
        "这是混合专家模型训练时的路由，回放出来：每个常见字符的词元，被送到了哪些专家，两个块都有。<bookmark mark='a'/>"
        "一开始路由器是随机的，几乎均匀：平均来说，一个字符最常去的专家只拿到它{100 * sharp[0]:.0f}%的词元。"
        "<bookmark mark='b'/>不到{steps[2]}步，路由器就拿定了主意：{100 * sharp[2]:.0f}%。<bookmark mark='c'/>{settle}"
        "<bookmark mark='q'/>专家们最后各自做什么，是第10章的问题。",

    'f"Then it settles':
        "然后它稳定下来，到最后是{100 * sharp[-1]:.0f}%，而随着专家越来越擅长分给它们的东西，这个模式还在不断变化。",

    "f'And it stays that decided":
        "之后它一直这么果断，到最后是{100 * sharp[-1]:.0f}%。",

    '"One caution before we celebrate.':
        "高兴之前，先提个醒。<bookmark mark='a'/>混合专家模型的计算量和那个小稠密模型一样，但在这台电脑上，它一步训练要花的时间是"
        "{howlong}<bookmark mark='h'/>按专家给词元排序、把它们收集起来、再把答案散回去，这些都要花时间，而计算量的统计看不见它们。"
        "<bookmark mark='b'/>大实验室靠专为路由打造的内核和硬件把时间赢回来，又在芯片之间搬运词元上输掉一些，这是第8章的话题。",

    'f"{slow:.1f} times as long as the dense model':
        "稠密模型的{slow:.1f}倍。",

    # ---------------------------------------------------------------- Balance
    "Chapter four. Collapse, and Switch's loss.": '第4章。坍缩，与Switch的损失。',

    '"A router learns only from the experts it tries.':
        "路由器只从它试过的专家身上学习。那么，它不再去试的那些专家会怎样？不加任何帮助，训练我们的混合专家模型，"
        "看看词元是怎么分配的。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>这是一个富者愈富的循环：被选中越多的专家，"
        "训练得越多，变得越好，又被选得更多；挨饿的专家不再学习，它的参数就浪费了。沙泽尔在2017年就看到了这一点，"
        "称之为自我强化的不平衡。",

    "f'Left alone, the router plays favourites.":
        "放任不管，路由器就会偏心。在3个种子里最差的那个，也就是这里画的，最忙的专家最后拿到公平份额的{worst:.1f}倍；"
        "在3个种子和两个块里，一共有{ns}个专家，最后拿到的不到公平份额的四分之一。",

    "f'In our small model the router stays fairly even":
        "在我们的小模型里，路由器自己就保持得相当均匀：最坏的情况下，最忙的专家最后也只有公平份额的{worst:.1f}倍。大模型就没这么幸运了。",

    'f"Shazeer\'s team met this in 2017':
        "沙泽尔的团队2017年就遇到了这个问题，并加了损失来对付它。<bookmark mark='a'/>第一个：把每个专家在一批数据上的门控值加起来，"
        "叫作它的重要性，然后惩罚这些总和的变异系数的平方，变异系数就是标准差除以均值。只有每个专家同样重要的时候，它才是0。"
        "<bookmark mark='b'/>对我们那个不均衡的路由器，按它的词元份额来算，变异系数是{cv:.2f}。<bookmark mark='c'/>"
        "停下来想一想：为什么要除以均值？因为这样，惩罚就不在乎门控整体有多大，只在乎它们分布得有多不均匀。"
        "第二个损失让期望的词元数也均衡，因为重要性相同，词元数仍然可能不同。",

    'The classic fix adds a penalty to the loss.':
        "经典的修正办法，是在损失里加一项惩罚。每个专家有两个数。<bookmark mark='a'/>f i，这一批里真正送到专家i的词元槽份额："
        "这是个计数，所以没有梯度。<bookmark mark='b'/>P i，路由器给专家i的平均概率：这个是可微的。<bookmark mark='c'/>"
        "Switch Transformer的惩罚，是α乘以E，再乘以f i乘P i的和，α取百分之一。<bookmark mark='d'/>为什么是这个乘积？"
        "如果路由器的概率和词元的实际去向一致，它就是E乘以f i平方的和；由柯西–施瓦茨不等式，它至少是1，"
        "当且仅当每个专家都拿到E分之1时取等号。<bookmark mark='e'/>而它的梯度，按每个专家已经有多忙，把它的概率往下压："
        "越受宠的，被压得越狠。<bookmark mark='f'/>GShard早一年就用过类似的惩罚；2022年，ST-MoE又加了第二个，z损失，"
        "防止路由器的分数变得太大。",

    '"Here is our mixture again, the same seed':
        "还是我们的混合专家模型，同一个种子，加惩罚和不加惩罚各训练一次。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}"
        "<bookmark mark='c'/>但这个惩罚是第二个目标，和第一个目标相互竞争。α太小，路由器会坍缩；α太大，"
        "它会把路由从预测最好的方向上扭开。下一章去掉了这个两难。",

    'f"With Switch\'s penalty at its usual strength, the busiest expert falls from {bn.mean():.1f} to {ba.mean():.1f} times a fair share, on average over seeds and blocks, and':
        "用Switch惯用的惩罚强度，最忙的专家从公平份额的{bn.mean():.1f}倍降到{ba.mean():.1f}倍，这是对种子和块的平均；"
        "挨饿的专家从{int(sn.sum())}个降到{int(sa.sum())}个。",

    'f"With Switch\'s penalty at its usual strength, the busiest expert falls':
        "用Switch惯用的惩罚强度，最忙的专家从公平份额的{bn.mean():.1f}倍降到{ba.mean():.1f}倍，这是对种子和块的平均。",

    'f"With Switch\'s penalty at its usual strength, the loads barely change':
        "用Switch惯用的惩罚强度，负载几乎没变：最忙的专家从公平份额的{bn.mean():.1f}倍变成{ba.mean():.1f}倍。",

    "f'And the model is better for it":
        "模型也因此更好了：{va[0]:.3f}比特对{vn[0]:.3f}，因为干活的专家才会学习。",

    "f'But the model is no better for it":
        "但模型并没有因此变好：{va[0]:.3f}比特对{vn[0]:.3f}。",

    "f'In held-out bits it makes little difference here":
        "在留出数据的比特数上，这里差别不大：{va[0]:.3f}对{vn[0]:.3f}。",

    # ---------------------------------------------------------------- LossFree
    'Chapter five. Balancing without a loss.': '第5章。不靠损失的负载均衡。',

    'In 2024 DeepSeek removed the trade-off.':
        "2024年，DeepSeek去掉了这个两难。给每个专家一个偏置，就一个数，<bookmark mark='a'/>只在挑选前k个的时候，"
        "把它加到专家的分数上。<bookmark mark='b'/>混合被选中专家的门控，只用分数本身，所以偏置只改变谁干活，"
        "从不改变模型算出的结果。<bookmark mark='c'/>每一步之后，看一看负载：比平均忙的专家，偏置往下调一小步γ；"
        "闲着的，往上调。没有额外的损失，也就没有梯度和语言模型作对。<bookmark mark='d'/>王岚和同事们报告说，"
        "它比辅助损失均衡得更好，困惑度也更低；DeepSeek-V3就是这样训练的。",

    "Here is DeepSeek-V3's router exactly":
        "这是DeepSeek-V3路由器的精确形式，它已经成了一个模板。<bookmark mark='a'/>每个专家的分数来自一个sigmoid，"
        "是它自己的“是或否”，而不是让专家们相互竞争的softmax。<bookmark mark='b'/>前k个按分数加均衡偏置来挑。"
        "<bookmark mark='c'/>门控只用分数，重新缩放到加起来等于1。<bookmark mark='d'/>还有一个共享专家，每个词元都会经过它，"
        "用来存放大家都需要的东西。<bookmark mark='e'/>在前14.3万亿个词元里，偏置每步调千分之一，之后就冻结；"
        "一个很小的额外损失，防止单个序列挤到少数几个专家上；而且从没有丢弃过任何词元。",

    '"Here are all three rules at once':
        "三种规则同时回放整个训练过程：每根柱子是一个专家在第一个块里拿到的词元份额。<bookmark mark='a'/>{left}"
        "<bookmark mark='m'/>{mid}<bookmark mark='r'/>右边，偏置让每个专家都保持在公平份额附近。<bookmark mark='b'/>"
        "下面是偏置本身：每一个，都是它的专家太忙或太闲的次数的累计。",

    'On the left, with no balancing, the shares drift apart.': '左边，不做均衡，份额渐渐拉开。',
    'On the left, with no balancing, the shares wander.': '左边，不做均衡，份额来回游移。',
    "In the middle, Switch's loss pulls them part of the way back.": '中间，Switch的损失把它们拉回来一部分。',
    "In the middle, Switch's loss pulls them back.": '中间，Switch的损失把它们拉了回来。',

    '"The scoreboard, over three seeds each.':
        "成绩表，每种各3个种子。<bookmark mark='a'/>{v}<bookmark mark='w'/>{w}<bookmark mark='b'/>提醒一句：我们的偏置模型"
        "还用了DeepSeek的sigmoid门控，而另外两个用的是softmax门控，所以这是在比较路由器，不只是在比较均衡规则。"
        "<bookmark mark='c'/>DeepSeek得出的结论是：靠引导选择来均衡，而不是靠改动损失。",

    "f'The bias balances best":
        "偏置均衡得最好，训练全程的不平衡度最小，{mx['moe']:.2f}；用损失是{mx['aux']:.2f}，什么都不用是{mx['none']:.2f}。",

    'f"Here Switch\'s loss balances best':
        "这里Switch的损失在训练全程均衡得最好，{mx['aux']:.2f}，偏置是{mx['moe']:.2f}。",

    'Surprisingly, the unbalanced router has the smallest imbalance here.':
        '出人意料的是，这里不做均衡的路由器，不平衡度反而最小。',

    "f'In held-out bits the bias model is best as well":
        "在留出数据的比特数上，偏置模型也是最好的：{vb['moe']:.3f}，用损失是{vb['aux']:.3f}，什么都不用是{vb['none']:.3f}。",

    "f'In held-out bits, though, the best is":
        "不过在留出数据的比特数上，最好的是{best_name}：{vb[best_bits]:.3f}，偏置是{vb['moe']:.3f}。",

    # ---------------------------------------------------------------- Fine
    'Chapter six. Fine-grained and shared experts.': '第6章。细粒度专家与共享专家。',

    'In January 2024 Damai Dai and colleagues at DeepSeek':
        "2024年1月，DeepSeek的戴达迈和同事们问：一个专家应该多大？<bookmark mark='a'/>Mixtral用几个大专家，挑2个。"
        "<bookmark mark='b'/>把每个专家切成4个小的，挑4倍那么多：参数一样，每个词元的计算量也一样，但每个词元的组合由更细的零件拼成。"
        "<bookmark mark='c'/>再留出一个专家，让每个词元共享，这样每个词元都需要的东西，比如常用词和语法，只学一次，"
        "而不必复制进每个专家里。他们把这两招叫作细粒度切分和共享专家隔离。",

    'They reported that it pays.':
        "他们报告说这样做划算。<bookmark mark='a'/>在20亿参数的规模上，DeepSeekMoE追平了GShard的设计，"
        "而后者的专家参数和计算量是它的1.5倍。<bookmark mark='b'/>扩大到160亿，它追平了Meta的稠密模型LLaMA 2 7B，"
        "计算量只用大约40%。这些是作者自己的数字；我们在自己的模型上验证一下这个想法。",

    'f"Why should finer pieces help?':
        "为什么更细的零件会有帮助？数一数一个词元能组成多少种团队。<bookmark mark='a'/>8个专家里挑2个，有{c1}种挑法。"
        "<bookmark mark='b'/>32个里挑8个，计算量相同，有{c2 / 1000000.0:.1f}百万种。<bookmark mark='c'/>这个数像k的幂次一样增长："
        "它被夹在N除以k的k次方，和e乘N除以k的k次方之间。<bookmark mark='d'/>DeepSeek自己的例子：16个专家挑2个，有{d1}种团队；"
        "每个切成4份，64个里挑8个，就有{d2 / 1000000000.0:.1f}十亿种。每个词元都能拿到一支更贴合它的团队。",

    '"We trained all three':
        "我们把三种都训练了，参数相同，每个字符的计算量也相同，各2个种子。<bookmark mark='a'/>{v1}<bookmark mark='v'/>{v2}"
        "<bookmark mark='b'/>在前沿，方向很清楚：DeepSeek-V3有256个细粒度专家，挑8个，外加1个共享；Kimi K3有896个，挑16个，共享2个。",

    'f"Cutting the experts finer helps':
        "把专家切细有帮助：{mf:.3f}比特，粗粒度的混合是{mc:.3f}，而且种子之间不重叠。",

    "f'Cutting the experts finer helps":
        "把专家切细有帮助：{mf:.3f}比特，粗粒度的混合是{mc:.3f}，不过种子之间有重叠。",

    'f"Cutting the experts finer doesn\'t help':
        "在我们的规模上，把专家切细没有帮助：{mf:.3f}比特，粗粒度的混合是{mc:.3f}。",

    "f'Adding a shared expert helps a little more": "再加一个共享专家，又好了一点：{msh:.3f}。",
    "f'A shared expert adds nothing here": "在这里，共享专家没带来什么：{msh:.3f}。",
    "f'With a shared expert, {msh:.3f}": "加上共享专家，{msh:.3f}：比单纯细粒度稍差一点。",

    # ---------------------------------------------------------------- Capacity
    'Chapter seven. Capacity, and dropped tokens.': '第7章。容量，与被丢弃的词元。',

    'On real hardware, each expert gets a buffer of fixed size':
        "在真实的硬件上，每个专家分到一个固定大小的缓冲区，这样每块芯片都能事先知道自己的工作量。<bookmark mark='a'/>容量："
        "一个因子c，乘以专家在这批数据里的公平份额，k N除以E。<bookmark mark='b'/>选中某个专家的词元一旦超过这个数，"
        "多出来的就被丢弃：它们跳过这一层，由残差连接带着往前走，就好像这一层不存在。<bookmark mark='c'/>GShard和Switch训练时"
        "用的因子是1到1.25，并且接受少量被丢弃的词元。路由器越不均匀，丢得越多。",

    'How much is dropped?':
        "会丢掉多少？专家i被要求的槽位数，是f i乘以k N，也就是它在全部槽位里的份额。<bookmark mark='a'/>它的缓冲区能装c乘以k N除以E。"
        "<bookmark mark='b'/>装不下的部分就被丢弃。<bookmark mark='c'/>除以槽位总数，丢弃的份额就是对所有专家求和：每个专家的份额超出c除以E的部分。"
        "<bookmark mark='d'/>停下来预测一下：路由完全均匀时，什么因子一个都不丢？1。如果有一个专家拿到两倍份额，因子为1时丢掉的正好是多出来的那部分："
        "全部槽位的E分之1。",

    'f"We can measure this on our trained routers':
        "我们可以在训练好的路由器上测一下：事后加上容量限制，数一数丢了多少。<bookmark mark='a'/>因子为1时，不均衡的路由器丢掉"
        "{100 * dn:.0f}%的词元槽，用Switch损失训练的丢掉{100 * da:.0f}%，用无损失偏置的丢掉{100 * db:.0f}%。<bookmark mark='r'/>"
        "{remain}<bookmark mark='b'/>换成比特，因子为1让不均衡的模型每字符多花{ln_:.3f}比特，偏置模型多花{lb_:.3f}。"
        "<bookmark mark='t'/>{two}",

    "Even perfect balance on average isn't balance in every batch":
        '平均上完美均衡，不等于每一批都均衡，所以还是会丢掉一些。',

    'With the bias, almost nothing is dropped at all.': '用偏置的话，几乎什么都没丢。',

    "f'At a factor of {fin[i2]:g}, almost nothing": "因子为{fin[i2]:g}时，它们几乎都没有损失。",

    "f'Even at a factor of {fin[i2]:g}":
        "即使因子为{fin[i2]:g}，不均衡的路由器仍然损失{float(loss['none'][:, i2].mean()):.3f}比特。",

    '"What if the limit is there during training?':
        "如果训练时就有这个限制呢？<bookmark mark='a'/>{v}<bookmark mark='b'/>{w}<bookmark mark='c'/>还有一种避免丢弃的办法："
        "反过来，让每个专家挑自己的词元，叫作专家选择，是周彦祺和同事们2022年提出的。它天生完全均衡，但一个专家怎么挑，"
        "取决于整批数据，包括后面才出现的词元，这个问题第11章还会遇到。DeepSeek-V3一个词元都不丢：它的均衡足够好，"
        "内核也足够灵活，来多少收多少。",

    "f'Trained with a capacity factor of one from the start":
        "从一开始就用因子1训练，路由器学会了适应：丢弃率从早期的{100 * early:.0f}%降到最后的{100 * late:.1f}%。",

    "f'Trained with a capacity factor of one, it drops about":
        "用因子1训练，它在整个过程中大约丢掉{100 * late:.1f}%的词元槽。",

    "f'The cost: {cf[0]:.3f}": "代价是：{cf[0]:.3f}比特，不加限制是{nocf[0]:.3f}。",
    "f'And it costs almost nothing": "而且几乎没有代价：{cf[0]:.3f}比特，不加限制是{nocf[0]:.3f}。",

    # ---------------------------------------------------------------- Parallel
    'Chapter eight. Experts across chips.': '第8章。分布在多块芯片上的专家。',

    "A model with hundreds of experts doesn't fit on one chip":
        "有几百个专家的模型，一块芯片装不下，所以专家要分散开：这叫专家并行，第18部分会搭建它。这里是8个专家放在4块GPU上。"
        "<bookmark mark='a'/>每块GPU上有一部分词元，而路由器可以把它们送到任何地方。<bookmark mark='b'/>所以每个MoE层都以一次全对全通信开始，"
        "每块GPU把每个词元送到它的专家所在的GPU，<bookmark mark='c'/>再以另一次全对全通信结束，把答案送回家。",

    'f"How expensive is that?':
        "这有多贵？拿DeepSeek-V3来说，一个词元，一个MoE层。<bookmark mark='a'/>它把一个{c['d']:,}维向量复制8份发出去，用8比特的数，"
        "再收回8个答案，用16比特：一共{p['v3_bytes'] / 1000.0:.0f}KB。<bookmark mark='b'/>8个专家在它上面做"
        "{p['v3_flops'] / 1000000.0:.0f}百万次运算。<bookmark mark='c'/>也就是每搬一个字节，做{p['v3_intensity']:,.0f}次运算："
        "等于专家宽度的2倍，不管什么模型都是这样。<bookmark mark='d'/>可一块做8比特运算的GPU，要从InfiniBand每读一个字节就做"
        "大约{p['ridge_ib']:,.0f}次运算，才不会闲着，这是第17部分的屋顶线。直接这样发送的话，网络花的时间是专家计算的"
        "{ratio:.0f}倍。<bookmark mark='e'/>所以DeepSeek让每个词元最多只去8台机器中的4台，每台机器只过一次InfiniBand，"
        "到了机器内部再经NVLink分发，发送时用8比特，剩下的开销，靠算一批的同时传另一批来藏起来。",

    'f"And balance, which looked like a matter of using every parameter':
        "而均衡，看起来是为了用上每个参数，其实也关乎速度。把我们训练好的专家放到4块GPU上，每块2个，数一数每块GPU分到多少工作。"
        "<bookmark mark='a'/>下一层开始之前，每块GPU都得做完，所以一步的时间取决于最忙的那块GPU。不做均衡，它是公平份额的"
        "{sl['none']:.2f}倍；用Switch的损失，{sl['aux']:.2f}倍；用偏置，{sl['moe']:.2f}倍。<bookmark mark='b'/>"
        "在真实的集群上，这个倍数会乘到每个MoE层的时间上。",

    # ---------------------------------------------------------------- Counting
    'Chapter nine. Counting parameters, and upcycling.': '第9章。数参数，以及升级。',

    'f"What do numbers like six hundred and seventy-one billion parameters':
        "6710亿个参数、370亿个激活，这样的数字到底数的是什么？我们可以从DeepSeek-V3公开的配置里算出来。<bookmark mark='a'/>"
        "一个专家是一个SwiGLU网络：3个{c['d']:,}乘{c['moe_ffn']:,}的矩阵，{a['expert'] / 1000000.0:.0f}百万个参数。"
        "<bookmark mark='b'/>每个MoE层有{c['routed']}个，一共{a['n_moe']}个MoE层：{P['routed'] / 1000000000.0:.0f}0亿，"
        "几乎就是全部。<bookmark mark='c'/>注意力，也就是第15部分的潜在注意力，在全部{c['layers']}层里加起来是"
        "{P['attention'] / 1000000000.0:.1f}十亿。<bookmark mark='d'/>再加上3个稠密层、共享专家、路由器和嵌入，总数是"
        "{a['total'] / 1000000000.0:.1f}十亿：就是报告里的6710亿。<bookmark mark='e'/>一个词元每层用9个专家，8个路由专家加1个共享专家，"
        "再加上其余所有部分：{a['active_with_embed'] / 1000000000.0:.1f}十亿，就是报告里的370亿。",

    'f"Drawn to scale, DeepSeek-V3\'s parameters':
        "按比例画出来，DeepSeek-V3的参数几乎全是路由专家。<bookmark mark='a'/>一个词元只用其中的"
        "{100 * a['active_with_embed'] / a['total']:.1f}%。在这一小片里，专家占{100 * ex_share:.0f}%，"
        "而每个词元都完整使用的注意力占{100 * at_share:.0f}%。<bookmark mark='b'/>同样的算术也解释了Mixtral的名字。"
        "8乘70亿应该是560亿，可Mixtral 8x7B只有{mx['total'] / 1000000000.0:.1f}十亿，因为只有前馈层被复制了8份；注意力是共享的。"
        "每个词元它用{mx['active'] / 1000000000.0:.1f}十亿。<bookmark mark='c'/>当你看到DeepSeek-V3写着6850亿时，"
        "那里面包括了一个提前预测第二个词元的模块，也就是第18部分的多词元预测。",

    'Training a big mixture from scratch is expensive.':
        "从头训练一个大的混合专家模型很贵。如果你已经有一个好的稠密模型呢？<bookmark mark='a'/>把它的前馈层复制进每个专家，"
        "加一个新的路由器，然后接着训练。<bookmark mark='b'/>刚复制完的那一刻，新模型算出的结果和旧模型一模一样："
        "每个被选中的专家给出同样的答案，而门控加起来等于1。接下来的训练，会把这些副本拉开。<bookmark mark='c'/>"
        "阿兰·小松崎和同事们2022年把它叫作稀疏升级；2024年，Qwen的第一个混合专家模型也是这样做出来的。",

    '"We tried it.':
        "我们试了一下。一个只有一个专家宽的稠密模型，训练1000步，然后复制成8个专家，再训练1000步；旁边是同一个一直保持稠密的模型，"
        "以及我们从头训练的混合专家模型。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}",

    "f'The upcycled model drops below the dense one":
        "升级后的模型马上就低于它的来源稠密模型，最后是{vu[0]:.3f}比特，而训练同样久的稠密模型是{vh[0]:.3f}。",

    "f'The upcycled model ends at {vu[0]:.3f}, about where":
        "升级后的模型最后是{vu[0]:.3f}，和稠密模型差不多，{vh[0]:.3f}。",

    "f'It even ends ahead of the mixture trained from scratch":
        "它甚至最后超过了从头训练的混合专家模型，{vm[0]:.3f}，训练计算量只用了后者的{pc_:.0f}%。",

    "f'It ends close to the mixture trained from scratch":
        "它最后和从头训练的混合专家模型很接近，{vm[0]:.3f}，训练计算量只用了后者的{pc_:.0f}%。",

    'f"It doesn\'t catch the mixture trained from scratch':
        "它没追上从头训练的混合专家模型，{vm[0]:.3f}，但训练计算量只花了后者的{pc_:.0f}%。",

    # ---------------------------------------------------------------- Special
    'Chapter ten. What experts learn.': '第10章。专家学到了什么。',

    '"What do the experts learn?':
        "专家们学到了什么？这是我们的混合专家模型在最后一个块里，把每个常见字符的词元送到了哪里：每列是刚读到的一个字符，"
        "每行是一个专家。<bookmark mark='a'/>{found}<bookmark mark='b'/>但这是关于字符本身，还是关于接下来会出现什么？我们可以测一测。",

    "f'Some patterns appear":
        "出现了一些规律：{len(vow)}个元音里有{cv}个主要去专家{ev + 1}；{len(punct)}个空格和标点里有{cp}个去专家{ep + 1}。没有人教过它。",

    "There's structure, but not the neat specialties": "有结构，但不是你想象的那种整齐的专长。",

    '"Mutual information, from part one':
        "互信息，来自第1部分：选中哪个专家，能告诉你关于一个字符的多少比特。<bookmark mark='a'/>{v1}<bookmark mark='v'/>{v2}"
        "<bookmark mark='b'/>打乱后的柱子代表偶然：一个不看字符的路由器，在这么多文本上会得到的分数。<bookmark mark='c'/>{v3}",

    "f'The choice of expert says most about the character just read":
        "选中哪个专家，最能说明刚读到的那个字符：最后一个块里是{cur:.2f}比特，对下一个字符是{nxt:.2f}，对前一个字符是{prv:.2f}。",

    "f'In the last block the choice says more about the character to come":
        "在最后一个块里，选择对下一个字符说明得更多，{nxt:.2f}比特，比对刚读到的字符还多，{cur:.2f}。",

    "f'In the last block the choice says most about the character before":
        "在最后一个块里，选择最能说明前一个字符，{prv:.2f}比特。",

    'So the experts sort tokens mostly by what they are':
        '所以专家们主要按词元本身在表面上是什么来分拣它们，而不是按模型要预测什么：路由器是对当前词元的一次快速查表。',

    'So the router is sorting by what the model must predict.': '所以路由器是按模型要预测的东西来分拣的。',

    'f"With thirty-two smaller experts there\'s more room to sort':
        "换成32个更小的专家，就有更多分拣的余地：选择对当前字符说明了{fcur:.2f}比特，8个专家时是{cur:.2f}。",

    "f'With thirty-two smaller experts, the choice says":
        "换成32个更小的专家，选择对当前字符说明了{fcur:.2f}比特，和8个专家时差不多。",

    'The big models look similar.':
        "大模型看起来也类似。<bookmark mark='a'/>Mistral对Mixtral的分析，没有找到专管生物学或哲学这类主题的专家。"
        "反而是语法：Python里的self、缩进，常常由同一个专家处理，相邻的词元也常常去同一个专家。<bookmark mark='b'/>"
        "2024年完全开源的混合专家模型OLMoE，发现了更明显的专长，按领域，也按词汇。<bookmark mark='c'/>这个名字有点误导。"
        "一个专家并不是化学专家；它是网络里的一小片，路由器学会了去找它，往往出于文本表面上的原因。",

    '"And the scoreboard':
        "还有记分牌，本系列在《马耳他之鹰》一章上的持续测试。<bookmark mark='a'/>{v}<bookmark mark='w'/>{w}",

    'f"On the scoreboard\'s passage, our mixture scores {m:.2f} bits a character, ahead':
        "在记分牌的测试段落上，我们的混合专家模型每字符{m:.2f}比特，领先于计算量相同的稠密模型，{da:.2f}；"
        "拥有全部参数的稠密模型是{dt:.2f}。",

    'f"On the scoreboard\'s passage, our mixture scores {m:.2f} bits a character, against':
        "在记分牌的测试段落上，我们的混合专家模型每字符{m:.2f}比特，计算量相同的稠密模型是{da:.2f}，拥有全部参数的是{dt:.2f}。",

    'f"They\'re behind Part 13\'s transformer':
        "它们都落后于第13部分的Transformer，{tf:.2f}；那个模型读4倍长的上下文，宽2倍，深也2倍：稀疏买来的是容量，不是上下文。",

    'f"Part 13\'s transformer scores': "第13部分的Transformer是{tf:.2f}。",

    # ---------------------------------------------------------------- Depth
    'Chapter eleven. Mixture-of-depths.': '第11章。深度混合。',

    'Experts make the width sparse.':
        "专家让宽度变得稀疏。深度能不能也稀疏？每个词元都需要每一层吗？<bookmark mark='a'/>2024年，谷歌DeepMind的大卫·拉波索"
        "和同事们给一些块配上了自己的路由器。它给序列里的每个词元打分；只有前k个经过这个块，注意力和前馈层都是，"
        "其余的沿着残差流跳过它。<bookmark mark='b'/>这个块的输出乘上路由器的分数，所以路由器能从损失中学习，就像混合专家一样。"
        "<bookmark mark='c'/>他们发现，每隔一个块、只让八分之一的词元通过，效果最好；从他们的模型采样，快了百分之五十以上。",

    'What does it save?':
        "它省下多少？在一个让T个词元里的c这一部分通过的块里，<bookmark mark='a'/>矩阵只作用在c T个词元上，"
        "<bookmark mark='b'/>而注意力只在被选中的词元之间计算，是c T的平方个分数。<bookmark mark='c'/>c取八分之一，"
        "矩阵的工作是八分之一，注意力是六十四分之一。<bookmark mark='d'/>4个块里每隔一个做路由，按每个词元算，"
        "矩阵的开销大约是完整模型的十六分之九。",

    '"We trained it. Our four-block transformer':
        "我们训练了它。我们的4块Transformer，第2和第4块做路由，对比2块、3块和4块的稠密模型。一个轴是每个字符的计算量，"
        "另一个轴是留出数据的比特数。<bookmark mark='a'/>稠密模型连成一条线：块越多，计算越多，比特越少。<bookmark mark='b'/>"
        "{v}<bookmark mark='w'/>{w}",

    "f'The routed models sit below the dense line":
        "做路由的模型落在稠密模型那条线的下方：同样的计算量，深度混合预测得更好，八分之一时是{m12:.3f}比特，"
        "同样计算量的稠密模型是{at12:.3f}。",

    "f'At an eighth of the tokens":
        "八分之一的词元时，做路由的模型落在稠密模型那条线下方，{m12:.3f}比特，同样计算量的稠密模型是{at12:.3f}。",

    "f'At half the tokens": "一半词元时，做路由的模型落在稠密模型那条线下方，{m50:.3f}对{at50:.3f}。",

    'At our scale the routed models land on or above the dense line':
        '在我们的规模上，做路由的模型落在稠密模型那条线上或线的上方：它们省了计算，但赢不过花同样计算量的稠密模型。',

    "f'Against the full four-block model":
        "和完整的4块模型相比，只让八分之一的词元通过，多花{m12 - l4:.3f}比特，省下{100 * (1 - fl['mod12'] / fl['dense_l4']):.0f}%的计算。",

    '"Which tokens get the deep treatment?':
        "哪些词元得到了深度处理？这是留出文本中的一段：亮起来的，是做路由的块处理的字符。<bookmark mark='a'/>"
        "路由器偏爱{key}：其中{100 * float(cs[key]):.0f}%都被它选中。<bookmark mark='b'/>但有个问题。挑出一个序列的前八分之一，"
        "就得看整个序列，包括后面的词元，而一次写一个词元的模型做不到这一点。论文用一个额外的损失，训练路由器去预测它自己的top-k选择，"
        "这样生成的时候它就能独自决定。<bookmark mark='c'/>{v}",

    "f'Deciding alone, the router sends {100 * frac:.0f} percent of the tokens through, close":
        "独自决定时，路由器让{100 * frac:.0f}%的词元通过，接近它训练时的八分之一，比特数几乎没变，{cf[0]:.3f}对{cb[0]:.3f}。",

    "f'Deciding alone, the router sends {100 * frac:.0f} percent of the tokens through, not":
        "独自决定时，路由器让{100 * frac:.0f}%的词元通过，不是它训练时的八分之一，比特数从{cb[0]:.3f}变成{cf[0]:.3f}："
        "这是个真实的差距，论文用一个专门训练的小预测器来弥补它。",

    # ---------------------------------------------------------------- Mass
    'Chapter twelve. How sparse is attention?': '第12章。注意力有多稀疏？',

    'Attention reads every earlier token':
        "注意力要读之前的每一个词元，所以它的开销随长度的平方增长。<bookmark mark='a'/>最早的办法，是事先把模式定死。"
        "2019年OpenAI的稀疏Transformer，读一个局部窗口，再加每隔k个的一个键，开销按长度的1.5次方增长。<bookmark mark='b'/>"
        "2020年，Longformer加了几个人人都读的全局键，谷歌的BigBird又加上随机的键，并证明这样的模式在原理上不损失表达能力。"
        "<bookmark mark='c'/>2023年的Mistral 7B只保留一个滑动窗口，靠层层叠加让信息传得更远。第19部分会测量窗口在服务时省下多少。"
        "<bookmark mark='d'/>但这些都是事先决定一个查询可以读哪些键。这和注意力实际去的地方相符吗？",

    'Pause and predict. If each query may keep only eight keys':
        "停下来预测一下。如果每个查询只能保留8个键，哪种选法损失更小：最近的8个，还是查询自己打分最高的8个？<bookmark mark='a'/>"
        "窗口算起来便宜：它是事先定好的。按分数挑，得先有分数。",

    'f"Attention looks at every earlier token, but how much':
        "注意力会看之前的每个词元，可它真正用到了多少？拿第13部分的Transformer来说，对每个查询，把它的键按权重排序。"
        "<bookmark mark='a'/>每条线是一个头：前k个键占了多少注意力。平均来说，在128到256个键里，前16个键占了{100 * m16:.0f}%。"
        "大部分注意力都落在少数几个键上。",

    'f"So let each query use only k keys.':
        "那就让每个查询只用k个键。哪k个？<bookmark mark='a'/>最简单的是最近的几个，也就是滑动窗口：用{kk[i8]}个键，"
        "每字符{wn[i8]:.2f}比特。<bookmark mark='b'/>更好的办法，是取它权重最高的{kk[i8]}个键：{tk[i8]:.2f}。"
        "<bookmark mark='c'/>{within}",

    'f"With {kk[-1]} keys chosen by score, it\'s within {tk[-1]':
        "按分数挑{kk[-1]}个键，和用全部键只差{tk[-1] - full:.3f}比特。",

    'f"With {kk[-1]} keys chosen by score, it\'s within a thousandth':
        "按分数挑{kk[-1]}个键，和用全部键的差距不到千分之一比特。",

    # ---------------------------------------------------------------- Designs
    'Chapter thirteen. Sparse attention, by design.': '第13章。设计出来的稀疏注意力。',

    'f"Choosing by score is what real models now do.':
        "按分数挑，正是现在的真实模型在做的。<bookmark mark='a'/>这是我们Transformer里的一个查询，以及它怎样给最后48个键分配权重。"
        "这些键加起来占了它{100 * float(r['strip_mass']):.0f}%的注意力，而大部分落在离末尾很远的几个字符上。<bookmark mark='b'/>"
        "滑动窗口只保留最后8个键：它们只占{100 * float(r['window']):.0f}%。<bookmark mark='c'/>DeepSeek的原生稀疏注意力，"
        "把过去切成块，再把每一块压缩成一个摘要。<bookmark mark='d'/>查询给这些摘要打分，把最好的几块完整读一遍，"
        "再保留一个最近词元的窗口：{100 * float(r['nsa']):.0f}%，用了{int(r['nsa_keys'])}个键。<bookmark mark='e'/>"
        "在DeepSeek-V3.2里，一个又小又快的索引器给过去的每个词元打分，查询只关注得分最高的那些：真实模型里是2048个，"
        "这里是8个，占了{100 * float(r['topk']):.0f}%。<bookmark mark='f'/>两者的诀窍都在于：找出重要的键，必须比关注全部键便宜得多。",

    'In equations:':
        "写成公式：<bookmark mark='a'/>NSA的输出是三个注意力的门控加权和：对块的摘要、对选中块的完整内容、对最近的窗口，"
        "门控由模型学出来。<bookmark mark='b'/>DSA的索引器用几个小头给过去的每个词元打分：是一组被整流的点积的加权和，"
        "负的分数全部置为0，也就是第9部分的ReLU，全部用8比特数计算：每个数都取整到256个值之一，以节省时间和内存。"
        "<bookmark mark='c'/>然后真正的注意力只在前2048个上运行。<bookmark mark='d'/>索引器仍然要看每一对，但它非常小，"
        "所以昂贵的部分现在随长度乘以2048增长，而不是随长度的平方增长。",

    'f"Can a model learn where to look?':
        "模型能学会看哪里吗？我们需要一个看哪里很要紧的任务。<bookmark mark='a'/>每个序列开头有8条事实，每条是一个词元，"
        "把一个键和一个值绑在一起：比如键3对应值11。<bookmark mark='b'/>然后是40个填充词元。<bookmark mark='c'/>"
        "然后逐个问这些键，模型必须答出对应的值。它需要的那条事实，至少在40个词元之前。<bookmark mark='d'/>"
        "我们用全注意力训练小Transformer，再用三种稀疏模式训练，每种都允许每个查询用{int(d['keys'])}个键："
        "滑动窗口；块选择，也就是查询自己那一块4个，加上平均键得分最高的那一块，就像MoBA和NSA；"
        "以及一个可以挑任意键的学出来的索引器，就像DeepSeek的稀疏注意力。",

    '"Here\'s training, the share of answers right.':
        "这是训练过程，答对的比例。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}"
        "<bookmark mark='d'/>{v4}",

    'f"Full attention learns it completely':
        "全注意力完全学会了：{100 * fw:.0f}%。滑动窗口看不到那些事实，一直停在偶然水平附近，{100 * ww:.0f}%。",

    "f'Full attention reaches": "全注意力达到{100 * fw:.0f}%，窗口是{100 * ww:.0f}%。",

    "f'Block selection gets {100 * bw:.0f} percent: it learns": "块选择达到{100 * bw:.0f}%：它学会了找到正确的块。",

    "f'Block selection gets {100 * bw:.0f} percent: an average key is a blurry":
        "块选择达到{100 * bw:.0f}%：平均键是一个模糊的摘要，有时会挑错块。",

    "f'Block selection gets {100 * bw:.0f} percent: an average key is too blurry":
        "块选择只有{100 * bw:.0f}%：平均键这个摘要太模糊，找不到正确的块。",

    "f'And the learned indexer": "而从全注意力模型出发、学出来的索引器，只用8个键就达到了{100 * iw:.0f}%。",

    "f'The learned indexer, started from the full model": "从全注意力模型出发、学出来的索引器达到{100 * iw:.0f}%。",

    "f'Imposing a pattern on the full model without retraining is a different story: its own":
        "不重新训练，直接给全注意力模型套上一种模式，就是另一回事了：它自己得分最高的8个键保留了{100 * ti:.0f}%，"
        "所以信息都在，只要能便宜地找到它。",

    "f'Imposing a pattern on the full model without retraining is a different story: even":
        "不重新训练，直接给全注意力模型套上一种模式，就是另一回事了：即使是它自己得分最高的8个键，也只保留了{100 * ti:.0f}%。",

    'f"This year\'s frontier combines the ideas.':
        "今年的前沿把这些想法结合了起来。<bookmark mark='a'/>2026年4月发布的DeepSeek-V4，把每{a['m']}个键和值压缩成一个条目，"
        "再由一个闪电索引器为每个查询挑出最好的{a['topk'][0]:,}个，外加最后{a['window']}个词元的窗口，负责局部细节。"
        "<bookmark mark='b'/>另一些层把{a['m2']}个压成1个，剩下的全部读一遍。<bookmark mark='c'/>它的索引器有{a['idx_heads']}个头，"
        "用{a['idx_bits']}比特的数计算。<bookmark mark='d'/>在一百万个词元时，DeepSeek报告说，每个词元的计算量是V3.2的"
        "{100 * a['flops']:.0f}%，缓存是{100 * a['kv']:.0f}%。缓存省下了什么，是第15部分的话题；怎样提供服务，是第19部分的。",

    # ---------------------------------------------------------------- Lottery
    'Chapter fourteen. Lottery tickets.': '第14章。彩票假设。',

    'f"The third kind of sparsity is the oldest':
        "第三种稀疏最古老：去掉权重。<bookmark mark='a'/>1990年，扬·勒丘恩、约翰·登克和萨拉·索拉，按海森矩阵的估计，"
        "去掉对损失伤害最小的权重，称之为最优脑损伤。<bookmark mark='b'/>2015年，韩松和同事们展示了能去掉多少："
        "剪掉最小的权重，再训练，重复，AlexNet缩小了{F.HAN['alexnet']}倍，VGG缩小了{F.HAN['vgg']}倍，准确率不变。"
        "<bookmark mark='c'/>但有件怪事早就为人所知：剪出来的小网络，从头训练，效果反而更差。2018年，乔纳森·弗兰克尔"
        "和迈克尔·卡宾发现，它只有从原来的初始权重出发才训练得好。<bookmark mark='d'/>他们的猜想：一个随机的大网络里，"
        "藏着一个小的子网络，一张中奖彩票，单独训练也能达到同样的准确率。大网络，只是你买够彩票的方式。",

    'f"How do you find a ticket?':
        "怎样找到一张彩票？训练、剪枝、回卷、重复。<bookmark mark='a'/>训练网络；去掉幅度最小的{int(100 * d['rate'][0])}%的权重；"
        "把幸存的权重回卷到训练早期的值，这里是第{int(d['rewind'])}步；然后再训练。回卷到训练开始后几步，而不是最开头，"
        "是弗兰克尔后来为更大的网络找到的修正。<bookmark mark='b'/>我们的网络读3个字符，猜下一个。这是它权重的一角，"
        "一轮一轮地，看掩码怎样变稀，直到只剩{100 * rem[-1]:.0f}%。<bookmark mark='c'/>对照组：同样的掩码配新的随机权重，"
        "以及同样大小的随机掩码。",

    '"Here are the three, round by round':
        "这是三者一轮轮的结果，随着网络变得越来越稀。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}"
        "<bookmark mark='d'/>问题在于：找到最小的那张彩票，用了{int(d['rounds']) + 1}次完整的训练。彩票假设改变了人们对大网络"
        "为什么好训练的看法。要在实践中节省计算，稀疏必须能便宜地找到，还得适合硬件：这是下一章的内容。",

    'f"The ticket stays as good as the dense network':
        "一直到只剩{100 * rem[best - 1]:.0f}%的权重，彩票都和稠密网络一样好，在某些大小上甚至还好一点。",

    "f'The ticket stays as good as the dense network":
        "一直到只剩{100 * rem[best - 1]:.0f}%的权重，彩票都和稠密网络一样好。",

    'Even the ticket loses ground from the first round of pruning.': '从第一轮剪枝开始，就连彩票也在退步。',

    "f'With the same masks but fresh random weights, the network does worse":
        "同样的掩码配上新的随机权重，网络就更差，在最稀的时候差{gap:.2f}比特：初始权重很重要，不只是保留了哪些连接。",

    'With the same masks but fresh random weights, the network does about as well':
        '同样的掩码配上新的随机权重，网络在这里差不多一样好：在这么小的规模上，掩码比初始权重更重要。',

    "f'Random masks of the same size do worst of all": "同样大小的随机掩码最差，在最稀的时候是{rm[-1]:.2f}比特。",

    "f'Random masks of the same size end at": "同样大小的随机掩码最后是{rm[-1]:.2f}比特。",

    # ---------------------------------------------------------------- Structured
    'Chapter fifteen. Two in four, and sparse activations.': '第15章。四选二，以及稀疏的激活。',

    "Removing half the weights doesn't make a network twice as fast.":
        "去掉一半权重，并不会让网络快一倍。零是零散分布的，而GPU是按稠密的块来读、来乘的。<bookmark mark='a'/>"
        "这是我们稠密模型第一个前馈矩阵的一角。<bookmark mark='b'/>2020年，英伟达的A100引入了一个折中：四选二。"
        "每4个相邻的权重里，正好有2个必须是0。<bookmark mark='c'/>这样，矩阵每组只需存2个值和2个小的位置索引，"
        "第17部分的稀疏张量核心就能以稠密速度的2倍来乘它。",

    '"What does two in four cost?':
        "四选二要付出什么代价？我们把稠密模型的每个权重矩阵都剪了，3个种子。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}"
        "<bookmark mark='c'/>{v3}这就是英伟达的做法：剪一次，再训练。对大语言模型，2023年的SparseGPT不用再训练就能剪枝，"
        "用的是第19部分GPTQ那一套方法。",

    "f'Pruning half the weights hurts":
        "剪掉一半权重是有代价的：按幅度、任意模式，每字符多{un - dense[0]:.2f}比特；强制成四选二，多{mg - dense[0]:.2f}；"
        "随机剪，多{rd - dense[0]:.1f}。",

    'f"Wanda\'s score, which weighs each weight by the size of the inputs it multiplies':
        "Wanda的分数，把每个权重按它所乘输入的大小加权，效果更好：多{wd - dense[0]:.2f}。",

    'f"Wanda\'s score, which weighs each weight by the size of its inputs':
        "Wanda的分数，把每个权重按输入的大小加权，在这里并没有更好：多{wd - dense[0]:.2f}。",

    "f'A short retraining with the pattern held":
        "保持模式不变、短暂地再训练一下，就补回了大部分差距：{int(p['ft_steps'])}步之后，只比稠密模型多{mf - dense[0]:.2f}比特。",

    "f'A short retraining recovers part of it":
        "短暂的再训练补回了一部分：{int(p['ft_steps'])}步之后，还差{mf - dense[0]:.2f}比特。",

    'f"Sparsity also hides in the activations.':
        "稀疏也藏在激活里。<bookmark mark='a'/>这是我们稠密模型前馈层经过GELU之后的激活：其中{100 * sh:.0f}%小于十分之一。"
        "激活为0的神经元，既不用计算，它的权重也不用读。<bookmark mark='b'/>那就把最小的那些置为0，看看代价是多少。"
        "置零一半，每字符多{d50:.3f}比特；置零百分之九十，多{d90:.2f}。",

    'f"With ReLU the zeros are exact.':
        "用ReLU的话，零是精确的。在彩票那一章的小ReLU网络里，训练结束时，对一个给定的输入，{100 * fin:.0f}%的隐藏单元正好是0。"
        "<bookmark mark='a'/>2022年，李宗霖和同事们发现，T5-Base只有百分之三的激活不为零，称之为懒惰神经元现象。"
        "<bookmark mark='b'/>现代模型用GELU和SwiGLU，没有精确的零；但2024年TEAL把Llama最小的百分之四十到五十的激活置零，"
        "损失很小，解码最多快了1.8倍，因为一个零，意味着一列权重不用读。<bookmark mark='c'/>这一部分的共同线索："
        "只有硬件能跳过的稀疏，才划算。",

    # ---------------------------------------------------------------- Frontier
    'Chapter sixteen. The frontier, late 2026.': '第16章。前沿，2026年末。',

    'f"Where has all this led?':
        "这一切走到了哪里？这是过去三年的大型开源混合专家模型，按每层有多少专家排开。<bookmark mark='a'/>2023年12月，"
        "Mixtral有8个。一年后，DeepSeek-V3有256个，外加一个共享专家。<bookmark mark='b'/>2025年，大家纷纷跟进：Qwen3，"
        "有384个专家的Kimi K2，GLM-4.5，OpenAI的gpt-oss，MiniMax，还有有512个专家的Qwen3-Next。<bookmark mark='c'/>"
        "2026年，有GLM-5、Qwen3.5、DeepSeek-V4、这周发布的Mistral Large 4，以及Kimi K3：每层{k3['experts']}个专家，"
        "挑{k3['k']}个。它们几乎都是细粒度的，大多数还保留了共享专家。",

    'f"And by the share of the model each token uses.':
        "再看每个词元用到模型的多大比例。<bookmark mark='a'/>Mixtral每个词元用{100 * fr['mixtral']:.0f}%的权重；"
        "DeepSeek-V3是{100 * fr['dsv3']:.1f}%。<bookmark mark='b'/>最新的只用3%到5%：DeepSeek-V4-Pro {100 * fr['dsv4']:.1f}%，"
        "Kimi K3 {100 * fr['kimik3']:.1f}%，这里最稀疏的{sparsest}，{100 * lowest['frac']:.1f}%。一个万亿参数的模型，"
        "每个词元的成本只相当于一个三百亿到五百亿参数的稠密模型。<bookmark mark='c'/>闭源模型里也有混合专家："
        "谷歌Gemini 1.5和2.5的报告都写明是稀疏混合专家，OpenAI开源的gpt-oss也是，不过大多数实验室不公开它们的架构。",

    'And attention.':
        "再看注意力。<bookmark mark='a'/>2025年2月，DeepSeek的原生稀疏注意力和月之暗面的MoBA，都选择过去内容的块，"
        "而MoBA已经在为Kimi的长文本请求服务。<bookmark mark='b'/>9月，DeepSeek-V3.2的索引器开始挑单个的词元。"
        "<bookmark mark='c'/>并非人人都信服：MiniMax的M2回到了全注意力，说他们的高效混合方案在常规基准上和全注意力不相上下，"
        "但在多步推理上有欠缺。<bookmark mark='d'/>但到了2026年，GLM-5采用了DeepSeek的稀疏注意力，DeepSeek-V4先压缩再挑选，"
        "MiniMax在M3上又回到了稀疏注意力，而Kimi K3主要用线性注意力，那是第15部分的话题。<bookmark mark='e'/>"
        "所以2026年的配方是：许多细粒度专家，一个共享专家，靠引导而不是靠惩罚来均衡，以及先压缩、再挑选的注意力。",

    # ---------------------------------------------------------------- Outro
    '"Let\'s take stock.':
        "我们来盘点一下。1991年，专家们学会了竞争和专精。路由器只从它试过的专家身上学习，所以需要噪声来探索，需要帮助来分担。"
        "{ours}<bookmark mark='o'/>放任不管，路由器会偏心；Switch的损失和DeepSeek的偏置让工作分散开，而偏置做到这一点，"
        "不会扭曲模型。更细的专家、共享专家、容量和芯片，都出自同一幅图景。注意力也能挑自己的键，只要这个选择是学出来的。"
        "权重也可以剪：中奖彩票确实存在，而四选二是硬件能用上的模式。",

    'Our own mixture beat a dense model with the same arithmetic.': '我们自己的混合专家模型，胜过了计算量相同的稠密模型。',

    "Our own mixture didn't beat a dense model": '在我们这么小的规模上，我们自己的混合专家模型没能胜过计算量相同的稠密模型。',

    'All of this comes back.':
        "这些都会再出现。让专家和四选二变快的张量核心和互连，是下一次，第17部分的话题。第18部分在成千上万块芯片上训练，"
        "用到专家并行和它的全对全通信。第19部分为专家和稀疏注意力提供服务。图像和视频模型也用专家，在第22部分。"
        "而在第30部分，稀疏出现在网络内部：只偶尔激活的特征，用稀疏自编码器找出来。",

    'Here are six problems to try':
        '这里有6道习题，从路由器的梯度到数Mixtral的参数。在这里暂停，动手做一做；完整的解答在本部分的笔记里。',

    'Next time: silicon.':
        "下一次：硅。为什么这一切都跑在GPU上，又被什么限制：运算、内存，以及芯片之间的连线。<bookmark mark='a'/>第17部分。",

    'To go further, the Switch Transformer and DeepSeek-V3 papers':
        '想深入了解，Switch Transformer和DeepSeek-V3的论文是很好的起点。谢谢观看，第17部分见。',
}

PHRASES = {
    # spliced short values
    'about as well': '差不多一样好',
    'better': '更好',
    'worse': '更差',
    "about as long as the dense model's. ": '和稠密模型差不多。',
    "Switch's loss": 'Switch的损失',
    'no balancing at all': '完全不做均衡',
    'the bias': '偏置',
    # kinds of characters (mixture-of-depths)
    'vowels': '元音',
    'consonants': '辅音',
    'capitals': '大写字母',
    'spaces': '空格',
    'punctuation': '标点',
}
