"""Chinese narration for ai25: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第25部分：对称与科学'

CHAPTERS = {
    'Hook': '把分子转一转',
    'History': '1. 我们是怎么走到这里的',
    'Symmetry': '2. 不变性与等变性',
    'Sets': '3. 集合上的函数',
    'Messages': '4. 消息传递',
    'WL': '5. 消息传递看不见的东西',
    'Depth': '6. 深层图网络',
    'Rotations': '7. 随分子一起转动的网络',
    'Folding': '8. 蛋白质折叠问题',
    'Evoformer': '9. AlphaFold 2：Evoformer',
    'Structure': '10. AlphaFold 2：坐标系、FAPE与循环',
    'AF3': '11. AlphaFold 3：原子上的扩散',
    'Design': '12. 设计蛋白质',
    'Weather': '13. 网格上的天气',
    'Operators': '14. 神经算子',
    'Materials': '15. 百万量级的材料',
    'Proofs': '16. 几何与证明',
    'Search': '17. 靠搜索做发现',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'Stockholm, October 2024.':
        "斯德哥尔摩，2024年10月。<bookmark mark='a'/>诺贝尔化学奖一半授予大卫·贝克，表彰蛋白质设计；另一半授予谷歌DeepMind的德米斯·哈萨比斯"
        "和约翰·江珀，表彰AlphaFold，一个能预测蛋白质折叠成什么形状的网络。<bookmark mark='b'/>前一天，物理学奖授予了约翰·霍普菲尔德和"
        "杰弗里·辛顿，表彰第20部分讲过的那些网络。<bookmark mark='c'/>测定一个蛋白质的形状，实验室可能要花好几年；AlphaFold几分钟就能预测出一个。",

    'f"Here is the idea this part is built on.':
        "这就是本部分立足的想法。五个带电粒子，一个玩具分子：把它转一转，它的能量不可能变。<bookmark mark='a'/>我们用三千个这样的分子训练网络"
        "去预测能量，然后把这一个转了整整一圈。<bookmark mark='b'/>普通网络不知道转动无害：它的答案摆动了{rng_m:.2f}个单位。<bookmark "
        "mark='c'/>训练时给它看转过的副本，摆动{rng_a:.2f}。<bookmark mark='d'/>一个建立在粒子间距离之上的网络看不见这次转动：它的答案只变了"
        "{tiny}，离真实能量{inv_err:.2f}。",

    'less than a millionth of a unit, rounding error':
        '不到百万分之一个单位，只是舍入误差',

    'less than a ten-thousandth of a unit, rounding error':
        '不到万分之一个单位，只是舍入误差',

    'That is the question of this part:':
        "这就是本部分的问题：一个网络知道了它所处理问题的对称性，能得到什么？这又为科学做了什么，<bookmark mark='a'/>在蛋白质、<bookmark "
        "mark='b'/>天气、<bookmark mark='c'/>材料<bookmark mark='d'/>和数学里？每个实验都在这里计算；关于大系统的每个数字都引自它们的论文。",

    'This is Part 25 of AI, Built':
        "这是《人工智能，从零搭建》的第25部分，也是第四幕的最后一部分。<bookmark mark='a'/>内容包括：对称性，以及一个函数尊重对称性是什么意思；"
        "<bookmark mark='o2'/>图、消息传递，以及它的极限；<bookmark mark='o3'/>随分子一起转动的网络；<bookmark mark='o4'/>蛋白质，从折叠问题"
        "到AlphaFold和蛋白质设计；<bookmark mark='o5'/>场：天气、神经算子，以及材料；<bookmark mark='o6'/>还有数学，从奥赛几何到经过检查的"
        "证明，再到靠搜索做出的发现。",

    # ------------------------------------------------------------------ History
    'Chapter one. How we got here.':
        '第1章。我们是怎么走到这里的。',

    "This part's story has three threads":
        "本部分的故事有三条线索，起点相隔很远。<bookmark mark='m0'/>第一次计算机天气预报，1950年。<bookmark mark='m1'/>第一个在三维中看到的"
        "蛋白质，1958年；1961年，克里斯蒂安·安芬森发现序列决定形状。<bookmark mark='m2'/>1968年，一个判断两个图是否相同的测试，后来发现它"
        "衡量的正是图网络能看见什么。<bookmark mark='m3'/>蛋白质数据库，1971年；<bookmark mark='m4'/>欧洲天气中心的第一次预报，1979年；"
        "<bookmark mark='m5'/>内置了图像对称性的卷积，1989年；<bookmark mark='m6'/>CASP的盲测比赛，1994年；<bookmark mark='m7'/>最早的图神经"
        "网络，2005年。",

    'Then, within a decade, the threads met.':
        "然后，在十年之内，这些线索交汇了。<bookmark mark='d0'/>2017年：消息传递，以及处理集合和分子的网络。<bookmark mark='d1'/>2018年："
        "第一代AlphaFold赢得CASP；2020年，AlphaFold 2接近实验水平。<bookmark mark='d2'/>2021年：随分子一起转的网络，以及学会方程解的网络。"
        "<bookmark mark='d3'/>2022年：两亿多个蛋白质的预测结构。<bookmark mark='d4'/>2023年：一个图网络在大多数指标上预报得比世界上最好的"
        "天气模型还准，另一个提出了数百万种新晶体。<bookmark mark='d5'/>2024年：诺贝尔奖，AlphaFold 3，机器解出奥赛题；<bookmark "
        "mark='d6'/>2025年：AI预报投入日常业务，进化搜索带来新的数学；<bookmark mark='d7'/>2026年：埃尔德什的未解问题被AI解决。",

    'What ties these together is one recipe.':
        "把这些串起来的是同一个配方。<bookmark mark='a'/>问问你的数据有什么是无关紧要的。对图像来说，是物体在哪里：于是有了卷积。<bookmark "
        "mark='b'/>对一组点来说，是它们的顺序。<bookmark mark='c'/>对一个图来说，是节点怎么编号。<bookmark mark='d'/>对一个分子来说，是它"
        "怎么转、怎么移。<bookmark mark='e'/>蛋白质这些全都有。<bookmark mark='f'/>天气场位于球面上，与网格无关。<bookmark mark='g'/>语言几乎"
        "没有对称性，所以Transformer要从数据中学习结构。<bookmark mark='h'/>布朗斯坦、布鲁纳、科恩和韦利奇科维奇把这称为几何深度学习。对称性"
        "进入模型有三条路：转换过的副本，一个标准姿态，或者尊重它的网络层；本部分主要讲第三条。",

    # ------------------------------------------------------------------ Symmetry
    'Chapter two. Invariance and equivariance.':
        '第2章。不变性与等变性。',

    'f"A symmetry is a transformation that leaves what matters unchanged.':
        "对称是一种让要紧的东西保持不变的变换。把正方形转九十度：还是同一个正方形。<bookmark mark='a'/>转四次就回到原处。<bookmark "
        "mark='b'/>一个问题的变换构成一个群：可以复合，有一个什么都不做的变换，而且每个变换都能撤销。<bookmark mark='c'/>正方形有四种转动；"
        "十六个点的排列有十六的阶乘种，大约{n16 / 1000000000000.0:.0f}万亿。<bookmark mark='d'/>空间的转动构成一个连续群，SO(3)；"
        "图像则有它的平移。",

    'Now a function of the data, f:':
        "现在来看数据的一个函数f：这里是我们五个粒子各自在一个时间单位之后的位置。<bookmark mark='a'/>先转输入，再用f，<bookmark mark='b'/>"
        "或者先用f，再转输出。<bookmark mark='c'/>如果两条路总是一致，f就是等变的。<bookmark mark='d'/>如果输出根本不变，f就是不变的，比如能量，"
        "或者图像的标签。<bookmark mark='e'/>中间层需要等变，这样输入的朝向才不会被扔掉；最终答案则常常需要不变。",

    'Any function can be made equivariant':
        "任何函数都能通过在群上取平均变成等变的：对每个g，先变换输入，再用f，再撤销g。<bookmark mark='a'/>给这个平均输入一个转过的x，也就是"
        "h作用在x上。<bookmark mark='b'/>把g乘h改名为g′：g走遍整个群时，g′也走遍整个群，所以和不变。<bookmark mark='c'/>乘积的逆要倒过顺序，"
        "<bookmark mark='d'/>于是h从和里提了出来：无论f是什么，平均都是等变的。<bookmark mark='e'/>代价是：群里每个元素算一次，十六个点就是"
        "十六的阶乘次，空间转动则是无穷多次。<bookmark mark='f'/>数据增强是便宜的版本：每个样本随机变换一次，指望网络学会其余的。",

    'f"Here is the check on our five-particle system':
        "这是在我们五粒子系统上的检验：四个网络，同样的数据，同样的步数。<bookmark mark='a'/>停下来预测一下：输入转动时，哪个网络的答案会"
        "精确地跟着转？<bookmark mark='b'/>等变网络EGNN，第7章会搭建它：它转过、平移过的答案只差{eg_tiny}个单位，是舍入误差。<bookmark "
        "mark='c'/>读原始坐标的消息传递网络能精确处理重新编号，处理不了转动。<bookmark mark='d'/>普通MLP两样都不行；用转过的副本训练后，它的"
        "转动误差是{ma['err']:.2f}，{aug_verdict}。<bookmark mark='e'/>做进网络层的对称性在每个输入上都精确成立；从例子里学来的只是近似成立，"
        "而且只在数据附近。",

    'smaller than its own error, but not zero':
        '比它自己的预测误差小，但不是零',

    # ------------------------------------------------------------------ Sets
    'Chapter three. Functions of sets.':
        '第3章。集合上的函数。',

    'f"Sixteen points in the plane, from one of four shapes':
        "平面上的十六个点，来自四种形状之一：圆环、圆盘、线段，或者两团。说出是哪一种。<bookmark mark='a'/>普通网络需要一个列表，所以我们"
        "给这些点编号，喂给它三十二个坐标。<bookmark mark='b'/>但编号是任意的：重新编号，图还是那张图，列表却变了。<bookmark mark='c'/>一个"
        "用八千个集合训练过的普通网络看到一个新输入：{mlp_line}。<bookmark mark='d'/>为集合而建的Deep Sets给出完全相同的答案，它也必须如此。",

    "f'its belief that this is a ring goes from":
        '它认为这是一个环的把握，从{100 * pm[0]:.0f}%变成了{100 * pm2[0]:.0f}%',

    "f'it changes its mind: from":
        '它改了主意：从{names[int(pm.argmax())]}变成了{names[int(pm2.argmax())]}',

    'The theorem behind Deep Sets':
        "Deep Sets背后的定理，出自曼齐尔·扎希尔等人2017年的工作：一个集合函数与顺序无关，当且仅当它是先对各元素求同一个函数phi的和，"
        "再接一个函数rho。<bookmark mark='a'/>一个方向很容易：和与顺序无关。<bookmark mark='b'/>另一个方向：给每个可能的元素编号，令phi(x)"
        "等于四的负编号次方。<bookmark mark='c'/>用四进制写，元素k在集合里，和的第k位就恰好是1：没有进位，所以不同的集合给出不同的和。"
        "<bookmark mark='d'/>于是集合的任何函数都是这个和的函数。<bookmark mark='e'/>对于实数集合，由牛顿恒等式，幂和起到同样的作用。",

    'As a network, this is simple.':
        "做成网络，这很简单。<bookmark mark='a'/>同一个小网络phi读每个点，<bookmark mark='b'/>结果加起来，<bookmark mark='c'/>第二个网络rho"
        "读这个和。<bookmark mark='d'/>phi的权重被所有点共享，就像卷积在各个位置共享权重。<bookmark mark='e'/>同一年的PointNet用最大值代替了"
        "求和。而一个没有位置编码的Transformer把它的词元当作一个集合：输入重新排序，输出也跟着重新排序。",

    'f"Now train them on {n0} up to':
        "现在来训练，从{n0}组集合到{n_big:,}组，每种三个种子，步数相同。<bookmark mark='a'/>只用{n0}组集合，Deep Sets就有"
        "{100 * a_ds[0]:.0f}%的时候是对的。<bookmark mark='b'/>普通MLP是{100 * a_ml[0]:.0f}%，{mlp_vs}。<bookmark mark='c'/>重新排序的副本"
        "帮助很大：{n0}组集合时是{100 * a_au[0]:.0f}%。{reach_txt}。{last}：Deep Sets是{100 * a_ds[-1]:.0f}%，副本是{100 * a_au[-1]:.0f}%。"
        "<bookmark mark='d'/>但副本只能近似地教会对称性：把同样的测试集合重新排序，普通MLP在{100 * f_ml:.0f}%的集合上改了答案，用副本训练的"
        "那个在{100 * f_au:.0f}%的集合上改了答案，Deep Sets一个也没改。",

    'At the largest size the copies have nearly caught up':
        '在最大的规模上，副本几乎追上来了',

    'Even at the largest size Deep Sets stays ahead':
        '即使在最大的规模上，Deep Sets仍然领先',

    'At the largest size the copies have caught up and passed it':
        '在最大的规模上，副本追上并超过了它',

    'f"Before the full comparison, watch one training run':
        "在完整比较之前，先看每种网络的一次训练，用{n}组训练集合，每两百步检查一次留出集上的准确率。<bookmark mark='a'/>"
        "{ds_txt}。<bookmark mark='b'/>普通MLP{mlp_txt}。<bookmark mark='c'/>看重新排序副本的MLP{aug_txt}。",

    "f'Deep Sets passes eighty percent after {d80:,} steps":
        'Deep Sets在{d80:,}步之后超过80%，最后达到{e_ds:.0f}%',

    "f'Deep Sets never passes eighty percent; it ends at":
        'Deep Sets始终没有超过80%，最后停在{e_ds:.0f}%',

    "f'never gets to eighty percent; it ends at":
        '始终没有达到80%，最后停在{e_ml:.0f}%',

    "f'passes eighty percent only at step {m80:,}":
        '直到第{m80:,}步才超过80%，最后达到{e_ml:.0f}%',

    "f'never gets to eighty percent either; it ends at":
        '也始终没有达到80%，最后停在{e_au:.0f}%',

    "f'gets there too, but later, at step {a80:,}":
        '也做到了，但更晚，在第{a80:,}步，最后达到{e_au:.0f}%',

    "f'gets there at step {a80:,} and ends at":
        '在第{a80:,}步做到了，最后达到{e_au:.0f}%',

    "f'and even with {n_big:,} sets it stays below":
        '而且即使用{n_big:,}组集合，它仍然不如Deep Sets只用{n0}组时的水平',

    "f'and it needs {reach_m[0]:,} sets to reach":
        '它需要{reach_m[0]:,}组集合，才能达到Deep Sets用{n0}组时的水平',

    "f'The MLP with reordered copies needs":
        '用重新排序副本训练的MLP，需要{reach[0]:,}组集合才能追上这个水平',

    "f'The MLP with reordered copies never matches":
        '用重新排序副本训练的MLP，即使用{n_big:,}组集合，也追不上这个水平',

    'So building the symmetry in did two things:':
        "所以，把对称性做进去带来了两件事：节省了数据，并且让答案在每个输入上都严格与顺序无关。接下来是图：带连接的集合。",

    # ------------------------------------------------------------------ Messages
    'Chapter four. Message passing.':
        '第4章。消息传递。',

    'A graph is a set with connections:':
        "图是带连接的集合：节点，以及某些节点对之间的边。这是十氢萘，十个碳原子，十一根键。<bookmark mark='a'/>计算机把它存成一个邻接矩阵，"
        "两个节点相连的地方就是1。<bookmark mark='b'/>换一种方式给节点编号，它的行和列就被打乱了，而分子还是同一个。<bookmark mark='c'/>所以"
        "图上的网络必须对重新编号等变：把节点重新排列，它的答案也同样重新排列。<bookmark mark='d'/>图无处不在：分子、道路图、社交网络、天气"
        "网格，还有蛋白质，空间上挨得近的残基相连。",

    'In 2017 Justin Gilmer and colleagues at Google':
        "2017年，谷歌的贾斯汀·吉尔默等人把这些网络归入一个统一的形式：消息传递。每个节点保存一个状态，一个向量h。<bookmark mark='a'/>每一层，"
        "每个节点把来自邻居的消息加起来，消息是两个状态和这条边的一个学出来的函数M，<bookmark mark='b'/>然后由旧状态和这个和更新自己的状态。"
        "<bookmark mark='c'/>一个读出把最后的状态加起来，给出关于整个图的答案。<bookmark mark='d'/>每一步都是对邻居求和，所以编号无关紧要。"
        "<bookmark mark='e'/>托马斯·基普夫和马克斯·韦林的图卷积网络是最简单的情形：按度数归一化，平均邻居的状态，再乘一个权重矩阵。",

    'The idea is older than its name.':
        "这个想法比它的名字更早。<bookmark mark='a'/>1997年，亚历山德罗·斯佩尔杜蒂和安东尼娜·斯塔里塔在带标签的图上训练网络。<bookmark "
        "mark='b'/>2005年，马尔科·戈里等人提出了图神经网络，节点状态由邻居反复更新，直到稳定。<bookmark mark='c'/>2014年，琼·布鲁纳等人通过"
        "图的谱来定义卷积。<bookmark mark='d'/>2015年，大卫·杜维诺等人学会了分子的指纹。<bookmark mark='e'/>后来，吉尔默的网络预测了小分子的"
        "十三种量子性质，其中十一种达到化学精度。<bookmark mark='f'/>而彼得·巴塔利亚等人论证说，图是让网络具备关系结构的通用方式。",

    'f"Let\'s train one. Three hundred people in three communities':
        "我们来训练一个。三百个人，分在三个社群里，友谊大多在社群内部：{100 * intra:.0f}%的边在社群内，平均每人大约{deg:.0f}条。每个人只带着"
        "关于自己社群的一点微弱、嘈杂的线索，而且只有{n_lab}个人有标签。<bookmark mark='a'/>一个两层的图卷积网络从这些标签和图中学习：看它对"
        "其他所有人的猜测。<bookmark mark='b'/>两层能看到两跳。<bookmark mark='c'/>只看每个人自己线索的MLP猜对{100 * np.mean(acc_m):.0f}%；"
        "图网络猜对{100 * np.mean(acc_g):.0f}%，三个种子的结果。{verdict}。",

    'Passing messages more than doubles what the hints alone give':
        '传递消息让结果比只看线索时翻了一倍还多',

    'Passing messages lifts it well above the hints alone':
        '传递消息让结果远远超过只看线索的水平',

    'Passing messages helps only a little here':
        '在这里，传递消息只帮了一点点',

    'That is message passing:':
        "这就是消息传递：对邻居学出来的求和，一遍遍重复，于是L层之后，每个节点都听到了L跳以内的一切。这样的网络能分辨什么？",

    # ------------------------------------------------------------------ WL
    "Chapter five. What message passing can't see.":
        '第5章。消息传递看不见的东西。',

    'f"In 1968 Boris Weisfeiler and Andrei Leman described colour refinement':
        "1968年，鲍里斯·魏斯费勒和安德烈·莱曼描述了颜色细化，这是判断两个图在编号之外是否相同的标准初步测试。<bookmark mark='a'/>每个节点"
        "一开始都是同一种颜色。<bookmark mark='b'/>每一轮，节点的新颜色由它的旧颜色和邻居的颜色命名：这里，有三个邻居的碳原子分了出来。"
        "<bookmark mark='c'/>然后是它们的邻居，直到不再变化。颜色计数不同，图就不同。<bookmark mark='d'/>十氢萘和联环戊烷，{rounds - 1}轮："
        "{verdict}。可一个是共用一条边的两个六元环，另一个是由一根键连起来的两个五元环。",

    'At every round the two molecules have exactly the same colours':
        '每一轮，两个分子的颜色种类和数量都完全相同，所以检验说它们可能是同一个图',

    'The colour counts differ, so the test tells them apart':
        '颜色的数量不同，所以检验能把它们分开',

    'And no message-passing network can do better.':
        "而且没有哪个消息传递网络能做得更好。Keyulu Xu等人，以及克里斯托弗·莫里斯等人，在2019年证明：如果颜色细化在t轮之后分不开两个节点，"
        "那么没有消息传递网络能在t层之后分开它们。<bookmark mark='a'/>用归纳法：一开始，一切都相同。<bookmark mark='b'/>下一轮颜色相同的两个"
        "节点，原来颜色相同，邻居颜色的多重集也相同；<bookmark mark='c'/>于是按归纳假设，状态相同，邻居状态的多重集也相同，<bookmark "
        "mark='d'/>一层网络从这些算出的新状态也就相同。<bookmark mark='e'/>而且这个上界能达到：求和之后接一个MLP，也就是图同构网络，能分开"
        "颜色细化能分开的一切。",

    'f"Why a sum? Aggregation must not lose information':
        "为什么是求和？聚合不能丢掉关于邻居多重集的信息。<bookmark mark='a'/>邻居a、a、b、b和邻居a、b的平均值相同，最大值也相同；只有和不同。"
        "<bookmark mark='b'/>计算一下：给一个随机图的每个节点同样的特征，让一个单层网络说出每个节点的度。用求和，误差在{sum_rm:.2f}以内。"
        "<bookmark mark='c'/>用平均或最大值，分别是{mean_rm:.2f}和{max_rm:.2f}，几乎不比度数的离散程度{sd:.2f}好：在它们看来，每个有邻居的"
        "节点都一样。",

    'f"Now make a network fail on purpose.':
        "现在故意让一个网络失败。{n}个节点、由若干个环组成的图：里面有没有三角形？<bookmark mark='a'/>在颜色细化看来，它们全都一样：每个节点"
        "都有两个邻居，邻居又各有两个邻居，一直如此。所以任何消息传递网络对它们都必须给出同一个答案。<bookmark mark='b'/>{gin_line}<bookmark "
        "mark='c'/>{rni_line}<bookmark mark='d'/>一个把特征放在节点对上、通过每个第三个节点更新每一对的网络，{pair_line}。记住这个构造："
        "它是AlphaFold的核心。",

    "f'sees triangles directly: {100 * min(p_ok):.1f}":
        '能直接看见三角形：每个种子都达到{100 * min(p_ok):.1f}%或更高，而且它的训练曲线在几百步之内就离开了基准比例',

    "f'can see triangles directly: {words_num(len(p_ok))}":
        '能直接看见三角形：三个种子里有{words_num(len(p_ok))}个达到了{100 * max(p_ok):.1f}%，不过其余的停在了基准比例',

    'can see triangles in principle, though in our budget':
        '原则上能看见三角形，但在我们的预算里它始终没学会',


    "f'Every graph gets exactly the same output":
        '每个图得到的输出完全相同，一位都不差，所以GIN最多只能总是回答有：{100 * np.mean(acc[\'gin\']):.1f}%，也就是基准比例。',

    'f"GIN\'s outputs barely differ between graphs':
        'GIN对不同的图给出的输出几乎没有差别：{100 * np.mean(acc[\'gin\']):.1f}%。',

    'Giving every node a few random numbers breaks the symmetry in principle, but in our budget':
        '给每个节点几个随机数，原则上能打破对称，但在我们的预算内，GIN始终没学会利用它们：三个种子全都停在基准比例。',

    "f'Giving every node a few random numbers breaks the symmetry: in all three seeds":
        '给每个节点几个随机数就打破了对称：三个种子里，GIN都学会了找三角形，准确率{100 * min(learned):.1f}%或更高。',

    "f'Giving every node a few random numbers breaks the symmetry in principle, but it is hard":
        '给每个节点几个随机数，原则上能打破对称，但很难学会：三个种子里有{words_num(nl)}个学会了，达到{100 * max(learned):.1f}%，'
        '其余的停在基准比例。',

    'f"How bad is it in practice? On random graphs':
        "实际中有多糟？在随机图上，几乎不成问题：颜色细化分开了{rp}对不同图中的{rs}对。<bookmark mark='a'/>在每个节点都有三个邻居的图上，"
        "{gp}对中只分开了{gsep}对。<bookmark mark='b'/>补救办法是加入邻居求和构造不出来的东西：给节点的元组上色，代价按n的k次方增长；数三角形"
        "和其他小图案；位置；或者覆盖每一对的注意力。<bookmark mark='c'/>图同构本身是容易还是困难，至今未知；拉斯洛·鲍鲍伊在2016年证明了"
        "拟多项式时间就够了。",

    # ------------------------------------------------------------------ Depth
    'Chapter six. Deep graph networks.':
        '第6章。深层图网络。',

    'Graph networks are usually shallow':
        "图网络通常很浅，两到四层；图像网络则超过一百层。原因之一：把图卷积的权重去掉，它就是一个对邻居的平均，一遍又一遍地做。<bookmark "
        "mark='a'/>平均矩阵是对称的，有正交归一的特征向量，特征值都不超过1。<bookmark mark='b'/>用它k次，就把每个特征值变成k次方。<bookmark "
        "mark='c'/>除第一项以外的每一项都衰减掉了；第一项在每个节点上是同一个图样，按度数的平方根缩放。<bookmark mark='d'/>衰减速率是第二"
        "特征值的k次方。<bookmark mark='e'/>每个节点最后都有同样的特征：过平滑，由Qimai Li等人在2018年命名。",

    'f"Here it is on our three-community graph:':
        "这是在我们的三社群图上：狄利克雷能量，也就是邻居之间差多少，在每一轮平均之后的值。<bookmark mark='a'/>在这个对数坐标上它沿直线下降，"
        "十六轮下降了{mags:.0f}个数量级，正是第二特征值{lam2:.3f}预言的速率。<bookmark mark='b'/>用图来看：特征一开始是噪声；几轮平均把社群"
        "分开，这就是两层网络有帮助的原因；很多轮之后，一切都坍缩成一个点。",

    'f"Now with weights and training:':
        "现在加上权重和训练：同一个任务，深度从二到六十四，每个深度三个种子。<bookmark mark='a'/>{best_txt}；{col_txt}。<bookmark mark='b'/>"
        "{res_txt}：跳跃连接让每个节点自己的信息不被平均掉，正是第9部分里让图像网络变深的那个办法。<bookmark mark='c'/>坍缩的一部分也是优化"
        "问题：梯度必须穿过所有这些平均反传回来。",

    "f'The plain network does best with {best} layers'":
        '普通网络在{best}层时最好',

    "f'The plain network does best with the fewest":
        '普通网络在最少的{best}层时最好',

    "f'from {collapse[0]} layers on":
        '从{collapse[0]}层开始，普通网络就只有瞎猜的水平，大约三分之一',

    'the plain network weakens with depth but never falls to chance':
        '普通网络随深度变弱，但从没跌到瞎猜的水平',

    'f"The residual network, which adds':
        '残差网络把每一层的输出加回到它的输入上，在{depths[-1]}层时仍保持在{100 * R[-1]:.0f}%',

    "f'Even the residual network falls":
        '连残差网络也下降了，{depths[-1]}层时跌到{100 * R[-1]:.0f}%',

    'A second problem appears when the answer depends on distant nodes.':
        "当答案依赖远处的节点时，第二个问题就出现了。<bookmark mark='a'/>L跳以内的节点可以指数增长，<bookmark mark='b'/>可它们所有的信息都得挤进"
        "一个固定大小的向量。<bookmark mark='c'/>乌里·阿隆和埃兰·亚哈夫在2021年把这叫作过挤压；杰克·托平等人把它追溯到瓶颈。<bookmark "
        "mark='d'/>补救：重新连图，加入能看见一切的节点，或者直接对每个节点做注意力。",

    'Attention is the third idea.':
        "注意力是第三个想法。<bookmark mark='a'/>节点不再平等地加总邻居，而是给它们加权：在彼得·韦利奇科维奇2018年的图注意力网络里，权重是"
        "学出来的分数的softmax。<bookmark mark='b'/>沙凯德·布罗迪等人的GATv2修正了一个缺陷：原来的分数对每个节点都按同样的方式给邻居排序。"
        "<bookmark mark='c'/>第13部分的Transformer，就是完全图上的这种网络；<bookmark mark='d'/>图Transformer再把图加回来，编码每个节点所处的"
        "位置。<bookmark mark='e'/>而AlphaFold的核心是残基对上的注意力，由三角形加偏置：上一章的节点对网络，长大了。",

    'So deep graph networks fight two forces:':
        "所以深层图网络要对抗两股力量：反复平均会抹掉节点之间的差别，而瓶颈会挤压远处的信息。跳跃连接和注意力能顶回去。"
        "接下来：空间本身的对称性。",

    # ------------------------------------------------------------------ Rotations
    'Chapter seven. Networks that turn with the molecule.':
        '第7章。随分子一起转动的网络。',

    'For molecules the symmetry is':
        "对分子来说，对称是空间刚体运动构成的群，E(3)：转动、反射、平移。<bookmark mark='a'/>分子的能量在所有这些变换下不变。<bookmark "
        "mark='b'/>两边对位置求导：链式法则带出了R的转置。<bookmark mark='c'/>乘以R，<bookmark mark='d'/>又因为力是能量梯度的负值，力就随分子"
        "一起转：等变。所以一个不变的能量模型，免费给出等变的力。",

    'How do you build that into a network?':
        "怎样把它做进网络里？最简单的答案是维克多·加西亚·萨托拉斯、埃米尔·胡赫博姆和马克斯·韦林2021年的E(n)等变图网络。每个原子有特征h和"
        "位置x。<bookmark mark='a'/>两个原子之间的消息只看它们的特征和距离的平方，别的都不看。<bookmark mark='b'/>每个原子沿着位置差移动，"
        "由学出来的标量加权；<bookmark mark='c'/>它的特征由加总的消息更新，保持不变。<bookmark mark='d'/>把输入转一转、移一移：消息不变，位置差"
        "跟着R转，平移抵消，于是新位置就是旧位置转过、移过的样子。<bookmark mark='e'/>2017年的SchNet只用了距离。",

    'f"EGNN carries scalars, which don\'t turn':
        "EGNN携带标量，它们不转；还有位置，它们像向量一样转。更丰富的模型携带更多。<bookmark mark='a'/>球面上的任何函数都能用零阶、一阶、二阶"
        "以及更高阶的球谐函数写出来。<bookmark mark='b'/>这里计算的是一次转动对阶数不超过二的九个球谐函数做了什么：它只在每一阶内部混合，分成"
        "一、三、五三个块；块外精确到小数点后{dp}位都是零。<bookmark mark='c'/>所以网络可以保留每一阶的特征，用各自的块来转，再按量子角动量的"
        "克莱布什–戈尔丹规则把它们组合起来：<bookmark mark='d'/>这就是张量场网络、NequIP和MACE的设计，它们属于当今最精确的学习力场。",

    'f"Does it pay? Our five-body system again:':
        "值得吗？还是我们的五体系统：预测粒子在时刻一的位置。四个网络，同样三千步训练，训练系统从一百个到{sizes[-1]:,}个，每种三个种子。"
        "<bookmark mark='a'/>虚线是最简单的猜测：每个粒子都沿直线走下去。<bookmark mark='b'/>{mlp_txt}。{aug_txt}：{m['mlp_aug']:.3f}。"
        "<bookmark mark='c'/>读原始坐标的消息传递网络：{m['gnn']:.3f}。<bookmark mark='d'/>EGNN：{m['egnn']:.4f}，{ratio_txt}。{cross}。",

    'With only a hundred, EGNN already beats every other network':
        '只用一百个，EGNN就已经胜过了用三十倍数据训练的所有其他网络',

    "f'Trained on {n_beat:,} systems, EGNN already beats":
        '只用{n_beat:,}个系统训练，EGNN就已经胜过了用{n_all:,}个系统训练的所有其他网络',

    "f'Even at {n_all:,} systems, no other network":
        '即使到了{n_all:,}个系统，也没有别的网络比得上它',

    "f'The plain MLP ends at {m['mlp']:.3f}, no better":
        "普通MLP最后是{m['mlp']:.3f}，不比那个{cvm:.3f}的猜测好",

    "f'The plain MLP ends at {m['mlp']:.3f}, below":
        "普通MLP最后是{m['mlp']:.3f}，比那个{cvm:.3f}的猜测低",

    'f"{ratio:.0f} times smaller':
        '比MLP的小{ratio:.0f}倍',

    'f"Here is training itself, for the runs on':
        "这是训练本身，用{big:,}个系统的那几次训练：一个网络从没见过的测试系统，它的五个粒子，以及它们到时刻1真正走到哪里，蓝色的轨迹。"
        "<bookmark mark='a'/>叉号是每个网络在训练各个检查点预测的终点。<bookmark mark='b'/>EGNN的叉号落到了圆圈上；最后它预测的位置"
        "平均偏差{err_e:.2f}。MLP的偏差是{err_m:.2f}。",

    'That is the case for equivariance:':
        "这就是支持等变性的理由：不用花任何数据去教网络，转过的分子还是同一个分子。蛋白质也是分子；本部分其余的内容把这些想法带进科学，"
        "从最难的分子讲起。",

    # ------------------------------------------------------------------ Folding
    'Chapter eight. The protein-folding problem.':
        '第8章。蛋白质折叠问题。',

    'A protein is a chain of amino acids':
        "蛋白质是一条由氨基酸连成的链，氨基酸有二十种，由一个基因写出。<bookmark mark='a'/>在水里它折叠成一个精确的形状，而形状决定了它做什么："
        "切断一个分子，抓住一个病毒，打开一个通道。<bookmark mark='b'/>1958年，约翰·肯德鲁用X射线晶体学看到了第一个，肌红蛋白。<bookmark "
        "mark='c'/>蛋白质数据库在1971年开张时有7个结构；<bookmark mark='d'/>今天它收录了超过25万个。<bookmark mark='e'/>可我们知道几十亿条"
        "序列，而测定一个结构可能要好几年。于是就有了这个问题：从序列读出形状。",

    'f"Two facts frame the problem.':
        "有两个事实给这个问题定了框架。<bookmark mark='a'/>1961年，克里斯蒂安·安芬森用尿素让核糖核酸酶解开折叠；洗掉尿素后，它自己折了回去，"
        "重新起作用：序列里就装着形状。<bookmark mark='b'/>但1969年，赛勒斯·列文索尔指出，一条链不可能靠逐个尝试来找到形状。<bookmark "
        "mark='c'/>给一条{N}个残基的链的每个关节三种选择：大约是十的{int(math.log10(conf))}次方种形状。<bookmark mark='d'/>每秒试十万亿个，"
        "也要十的{int(math.log10(years))}次方年；宇宙的年龄是十的十次方年。<bookmark mark='e'/>可蛋白质在几微秒到几秒内就折叠好了。自然不会"
        "盲目搜索，计算机也不该。",

    'In 1994 John Moult and Krzysztof Fidelis turned the problem into a contest':
        "1994年，约翰·莫尔特和克日什托夫·菲德利斯把这个问题变成了一场比赛，CASP：每两年一次，预测那些已经测定、但尚未发表的结构。<bookmark "
        "mark='a'/>预测用GDT打分，大致是落在真实位置几埃以内的残基所占的百分比。<bookmark mark='b'/>二十年里进展很慢；然后，进化给出了线索。"
        "<bookmark mark='c'/>把许多物种的同一种蛋白质对齐：两个位置相互接触时，一处的突变常常由另一处来补偿，所以这两列一起变化；大约从2011年"
        "起，统计方法就能从中读出接触。<bookmark mark='d'/>2018年的CASP13上，DeepMind的第一代AlphaFold为每一对残基预测距离的直方图，再用"
        "梯度下降把链折成与之相符：在43个最难的结构域中，有24个达到高精度，第二名是14个。",

    'Why distances? Because a full table of distances fixes a shape.':
        "为什么是距离？因为一张完整的距离表就确定了一个形状。这是我们螺旋束五十二个原子之间的所有距离。<bookmark mark='a'/>把它们平方，再中心化，"
        "<bookmark mark='b'/>就得到原子位置之间的点积，因为距离的平方等于两个长度的平方和减去两倍点积。<bookmark mark='c'/>它的特征向量把坐标"
        "还原出来：经典多维尺度分析，1952年。只有三个特征值非零，每个维度一个，<bookmark mark='d'/>还原出的链与原来的一致，只差舍入误差。"
        "<bookmark mark='e'/>但只能确定到一个镜像，镜像的距离完全相同；而蛋白质不是镜像对称的：它们的螺旋是右手螺旋。",

    'f"AlphaFold 1 predicted only distances':
        "AlphaFold 1只预测距离，带噪声，而且只针对它确信挨得近的残基对。我们也这样做：只保留{f['cut']:.0f}埃以内的残基对，占"
        "{100 * frac:.0f}%，加上{f['noise']:.0f}埃的噪声，<bookmark mark='a'/>然后从一团随机的乱线出发，用梯度下降移动原子，直到距离吻合。"
        "<bookmark mark='b'/>从{n}个随机起点出发，{verdict}。<bookmark mark='c'/>凡是在反射下不变的东西，包括距离，都分不清是哪个。"
        "AlphaFold 2需要一种分得清左右的表示。",

    "f'{words_num(len(good))} of the {n} land":
        '{n}次里有{words_num(len(good))}次落在真实的折叠上，{words_num(len(bad))}次落在它的镜像上，而镜像和距离吻合得一样好',

    'Distances pin down a shape, but only up to its mirror image.':
        "距离能确定一个形状，但只能精确到镜像。记住这一点；AlphaFold 2对此的回答，是它最巧妙的部分之一。",
}

PHRASES = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
    'eight': '8', 'nine': '9', 'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14',
    'fifteen': '15', 'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20',
    'ring': '环', 'disc': '圆盘', 'segment': '线段', 'two blobs': '两团点',
    'about a billionth': '大约十亿分之一', 'less than a billionth': '不到十亿分之一',
    'about a hundred-millionth': '大约一亿分之一', 'about a ten-millionth': '大约千万分之一',
    'about a millionth': '大约百万分之一', 'about a hundred-thousandth': '大约十万分之一',
    'about a ten-thousandth': '大约万分之一',
    'Turned copies help the MLP': '转过的副本对MLP有帮助',
    "close to the MLP's": '和MLP的差不多',
    'still as large as its own error': '仍然和它自己的预测误差一样大',
    'Each wins on one count': '两者各赢一项',
    'At rank seven our search found none': '秩为七时，我们的搜索一个也没找到',
}

ZH.update({
    'Turned copies barely help it at this budget':
        '在这个预算下，转过的副本几乎帮不上忙',

    # ------------------------------------------------------------------ Evoformer
    'Chapter nine. AlphaFold 2: the Evoformer.':
        '第9章。AlphaFold 2：Evoformer。',

    'AlphaFold 2, which John Jumper and colleagues at DeepMind entered':
        "AlphaFold 2是约翰·江珀等人在2020年代表DeepMind参加CASP14的系统，它分两个阶段工作。<bookmark mark='a'/>它在基因数据库里搜索"
        "相关序列，排成一个多序列比对，再找相似的已知结构。<bookmark mark='b'/>Evoformer有四十八个模块那么深，对这些信息进行推理；<bookmark "
        "mark='c'/>结构模块把结果变成原子，并给每个残基一个置信度。<bookmark mark='d'/>然后整个系统在自己的输出上再跑一遍。<bookmark mark='e'/>"
        "Evoformer为比对中每条序列的每个残基保留一个向量，为每一对残基保留一个向量，后者继承了AlphaFold 1的距离直方图。",

    'Each Evoformer block passes information both ways between them.':
        "每个Evoformer模块都在这两者之间双向传递信息。<bookmark mark='a'/>沿着每条序列，残基彼此做注意力，残基对的表示给这个注意力加上偏置。"
        "<bookmark mark='b'/>沿着每一列，同一个位置在不同物种之间做注意力。<bookmark mark='c'/>反过来，比对里两列的外积，在所有序列上平均，"
        "更新这两个位置组成的那一对：学出来的共进化。",

    'The new idea is in how the pairs update each other.':
        "新想法在于残基对怎样互相更新。把残基对的表示看成是对每个距离的猜测。<bookmark mark='a'/>这些猜测不可能互相独立：对任何第三个"
        "残基k，从i到j的距离最多是i到k加上k到j。<bookmark mark='b'/>所以每一对i、j都用它所在的每个三角形的另外两条边来更新：对k求和，把i k"
        "和j k这两对的乘积加起来，再加门控，这叫“外向”更新；<bookmark mark='c'/>指向内的边也同样处理。<bookmark mark='d'/>在矩阵里，元素i j"
        "收集第i行和第j行。<bookmark mark='e'/>三角注意力用注意力权重做同样的事。<bookmark mark='f'/>第5章的教训：通过第三个节点更新的节点对，"
        "能看见单个节点看不见的东西。",

    'f"Does it work? A small test, computed here.':
        "它管用吗？这里计算一个小测试。随机的、像蛋白质一样的链，{p['n']}个残基；模型看到四分之一的距离，带噪声，要把其余的填出来，"
        "这代替了比对告诉AlphaFold的信息。<bookmark mark='a'/>两个同样大小、同样训练的模型：一个单独更新每一对，另一个用三角更新。"
        "<bookmark mark='b'/>只根据两个残基在链上隔多远来猜缺失的距离，误差是{sep:.1f}埃。单独更新每一对得到{mp:.1f}，{pw_txt}。"
        "<bookmark mark='c'/>{verdict}，{vtxt}。",

    'no better: it never looks at the other pairs, and it knows the gap':
        '并没有更好：它从不看别的残基对，而且它只知道链上八以内的间隔',

    'hardly better, because it never looks at the other pairs':
        '几乎没有更好，因为它从不看别的残基对',

    "f'Triangle updates cut it to":
        '三角更新把它降到{mt:.1f}，小了{mp / mt:.1f}倍',

    'f"Triangle updates don\'t help here':
        '三角更新在这里没有帮助：{mt:.1f}',

    "f'and their guesses break the triangle inequality":
        "而且它的猜测违反三角不等式的次数少了{viol['pairwise'] / max(viol['triangle'], 1e-09):.0f}倍",

    'though their guesses break the triangle inequality no less often':
        '不过它的猜测违反三角不等式的次数并没有更少',

    'f"Here is the training itself, replayed:':
        "这是训练过程本身的回放：两个模型对一条留出链的猜测。<bookmark mark='a'/>第0步，两个模型的猜测都没有什么特别的。<bookmark "
        "mark='b'/>几百步之内，两个都学会了容易的部分：链上相邻的残基在空间里也挨得近，也就是对角线上的那条深色带。<bookmark mark='c'/>"
        "剩下的部分，也就是链上相隔很远的残基又在哪里碰到一起，需要别的残基对；<bookmark mark='d'/>在下面的曲线上，{beat_txt}。",

    'the triangle model never gets below the per-pair model':
        '三角模型始终没有低于逐对模型',

    'f"the triangle model passes the per-pair model\'s final error':
        "三角模型在第{b_step:,}步就超过了逐对模型的最终误差，而且继续下降，到{e_tri:.1f}埃，逐对模型是{e_pw:.1f}埃",

    'And at CASP14, in 2020, it worked.':
        "而在2020年的CASP14上，它成功了。<bookmark mark='a'/>AlphaFold 2在所有目标上的中位数得分是92.4 GDT，在最难的目标上是87.0；"
        "按非正式的看法，大约九十分就能和实验相比。<bookmark mark='b'/>它的主链误差中位数是0.96埃，第二名是2.8；一个碳原子的直径大约是1.5埃。"
        "<bookmark mark='c'/>“我们在这个问题上卡了将近五十年：蛋白质是怎么折叠起来的，”约翰·莫尔特说；CASP称之为一个解答，针对单条链。",

    "So the Evoformer's two ideas:":
        "所以Evoformer的两个想法是：让比对和残基对互相提供信息，用三角形让残基对保持一致。下一步：把残基对变成一个结构，而且不弄丢左和右。",

    # ------------------------------------------------------------------ Structure
    'Chapter ten. AlphaFold 2: frames, FAPE and recycling.':
        '第10章。AlphaFold 2：坐标系、FAPE与循环。',

    'The structure module treats each residue as a rigid body:':
        "结构模块把每个残基当作一个刚体：由三个主链原子组成的三角形，有它自己的坐标系，一个旋转加一个位置。<bookmark mark='a'/>它一开始"
        "把所有坐标系都放在原点，一团“残基气体”，然后移动它们。<bookmark mark='b'/>它的不变点注意力在每个残基的坐标系里放置一些学出来的点，"
        "按这些点靠得多近来给残基对打分。<bookmark mark='c'/>蛋白质的一次刚体运动让每个点都同样移动，所以注意力不会变。<bookmark mark='d'/>"
        "每一层用一个以该坐标系自身坐标表示的更新，轻轻推动每个坐标系，所以更新随蛋白质一起转动：等变性，做在了里面。",

    'What should the network be trained to minimize?':
        "网络应该被训练去最小化什么？AlphaFold 2的答案是坐标系对齐点误差，FAPE。<bookmark mark='a'/>站在残基i的坐标系里看原子j。"
        "<bookmark mark='b'/>对每个原子、从每个坐标系都这样看，在预测里和真实结构里都看，把差别平均起来，每个差别截断在十埃，免得离群值主导"
        "结果。<bookmark mark='c'/>整个结构的刚体运动会抵消：FAPE不管蛋白质在哪里、朝哪个方向。<bookmark mark='d'/>但坐标系是用右手法则从"
        "三个原子构造的，而镜像不是刚体运动，所以FAPE能看出来。",

    'f"Here is the difference, measured on our bundle and its reflection.':
        "差别在这里，在我们的螺旋束和它的镜像上测量。<bookmark mark='a'/>每个距离都一样，所以距离误差是{dm:.2f}。<bookmark mark='b'/>"
        "可FAPE是{fm:.2f}，比把每个原子随机移动整整1埃还差，那样是{f['fape_noisy']:.2f}。<bookmark mark='c'/>而第8章那些光靠距离分不开的"
        "折叠，现在被干净地分开了：落在真实折叠上的得分{gf:.2f}，镜像{bf:.2f}。",

    'f"The last trick is recycling:':
        "最后一招是循环：把网络在它自己上一次的输出上再跑一遍，这样一个粗糙的初始结构就能让网络把比对读得更清楚。<bookmark mark='a'/>"
        "训练时，跑几遍是随机的，梯度只流过最后一遍，所以多跑几遍不多占内存。<bookmark mark='b'/>我们把它加到了第9章的三角模型上。"
        "{verdict}，{vs}。",

    "f'A second pass cuts the error from":
        '第二遍把误差从{m[0]:.2f}埃降到{m[1]:.2f}埃；最好的是跑{best}遍，{m.min():.2f}',

    "f'In our toy the extra passes change little":
        '在我们的玩具里，多跑几遍变化不大：从{m[0]:.2f}埃到最好的{m.min():.2f}埃',

    'and with four passes it beats the same network trained without recycling':
        '而且跑四遍时，它胜过了不用循环训练的同一个网络',

    'f"though even with four passes it doesn\'t beat':
        '不过即使跑四遍，它也没有胜过不用循环训练的同一个网络，{one:.2f}：我们的玩具送回去的只是它对残基对的猜测，回路里没有结构，'
        '而在AlphaFold 2里，循环确实有帮助',

    'In July 2021 DeepMind published AlphaFold 2 with its code;':
        "2021年7月，DeepMind发表了AlphaFold 2，并公开了代码；同一个月，大卫·贝克的团队发表了基于同样洞见的RoseTTAFold。<bookmark "
        "mark='a'/>随后，DeepMind和EMBL的欧洲生物信息研究所一起发布了两亿多个蛋白质的预测结构，<bookmark mark='b'/>每个都带着网络自己逐个"
        "残基给出的置信度，pLDDT。<bookmark mark='c'/>两年后，诺贝尔奖来了。<bookmark mark='d'/>但AlphaFold 2对每条链只预测一个静止的形状，"
        "对蛋白质怎样结合DNA、怎样夹住一个药物分子，说得很少：这是下一步。",

    'So: residues as rigid frames,':
        "所以：残基是刚性的坐标系，由看不见蛋白质怎么转的注意力来移动；一个不在乎刚体运动、却在乎反射的损失；还有一个会读自己的答案、"
        "再试一次的网络。",

    # ------------------------------------------------------------------ AF3
    'Chapter eleven. AlphaFold 3: diffusion over atoms.':
        '第11章。AlphaFold 3：原子上的扩散。',

    'In May 2024 Google DeepMind and Isomorphic Labs published AlphaFold 3.':
        "2024年5月，谷歌DeepMind和Isomorphic Labs发表了AlphaFold 3。<bookmark mark='a'/>细胞结构里的几乎任何东西它都能处理，蛋白质链、"
        "DNA和RNA、类药分子、离子、修饰过的残基，并预测它们怎样待在一起。<bookmark mark='b'/>比对只经过四个模块；<bookmark mark='c'/>主干是"
        "Pairformer，也就是Evoformer的残基对部分，四十八个模块，三角更新原样保留。<bookmark mark='d'/>大的改变在最后：结构模块连同它的坐标系，"
        "被一个扩散模型取代，它直接写出每个原子的坐标。",

    "Diffusion is Part 21's idea, applied to atoms.":
        "扩散是第21部分的想法，用在了原子上。<bookmark mark='a'/>给一个结构的坐标加噪声，从轻微到纯噪声的每个水平都加，训练一个网络去"
        "除掉噪声；然后从噪声出发，一步一步除掉它。这是我们的一个小模型，从噪声变成一条链。<bookmark mark='b'/>惊奇之处来了，就在花了四章把"
        "对称性做进网络之后：AlphaFold 3的论文说，它的架构不需要对转动或平移的不变性或等变性。<bookmark mark='c'/>每个训练结构只是先中心化，"
        "再随机转动：数据增强，第2章那条便宜的路。<bookmark mark='d'/>扩散还可能在松软的区域编造出结构；用AlphaFold-Multimer的预测来训练，"
        "教会了AlphaFold 3让这些区域保持松散。",

    'f"So is equivariance worth it, for a generator?':
        "那么，对生成模型来说，等变性值得吗？做一个玩具测试：平面上四千条紧凑的链，每条十二个原子，键长为1。<bookmark mark='a'/>两个"
        "去噪器，训练时间一样长：一个对转动等变，像EGNN；另一个是普通MLP，每条链都随机转过之后才给它看，就像AlphaFold 3那样。<bookmark "
        "mark='b'/>它们的样本。<bookmark mark='c'/>键长：等变模型平均偏差{e['bond']:.3f}，普通模型{m['bond']:.3f}。碰撞，也就是两个原子"
        "叠在一起：{100 * e['clash']:.1f}%的链对{100 * m['clash']:.1f}%。{verdict}，{nn_line}。<bookmark mark='d'/>在AlphaFold 3的规模上，"
        "有整个蛋白质数据库，DeepMind选择了转过的副本：用数据和算力代替内置的对称性。",

    'and neither simply copies its training chains':
        '而且两者都没有只是照抄训练链',

    'though the samples sit closer to training chains than real new chains do':
        '不过样本离训练链比真正的新链离得更近',

    'The equivariant denoiser draws better chains on both counts':
        '等变去噪器在两项上都画出了更好的链',

    'The plain network, trained on turned copies, does as well or better on both counts':
        '用转过副本训练的普通网络，在两项上都一样好或者更好',

    'On drug-like molecules bound to proteins':
        "对于结合在蛋白质上的类药分子，DeepMind报告说AlphaFold 3比最好的传统方法精确百分之五十。<bookmark mark='a'/>它先以免费服务器的"
        "形式提供，2024年11月又向学术界开放了代码和权重；<bookmark mark='b'/>开放的复现随之而来：Chai-1、Boltz-1、Protenix。<bookmark "
        "mark='c'/>2025年，Boltz-2加上了对结合强度的预测。<bookmark mark='d'/>2026年2月，Isomorphic Labs报告了一个专有的后继系统：在它"
        "自己的新抗体–抗原对基准上，做出高精度预测的比例是AlphaFold 3的2.3倍。",

    'AlphaFold 3 kept the pair stack,':
        "AlphaFold 3保留了残基对的部分，把几何交给了扩散，从转过的副本里学会对称性。预测也可以倒过来：从你想要的形状，到一个能折成它的"
        "蛋白质。",

    # ------------------------------------------------------------------ Design
    'Chapter twelve. Designing proteins.':
        '第12章。设计蛋白质。',

    'Structure prediction goes from a sequence to a shape.':
        "结构预测是从序列到形状。<bookmark mark='a'/>设计走的是反方向：从你想要的形状，比如一个能结合病毒的结合子或一个催化剂的支架，到一条"
        "能折成它的序列。<bookmark mark='b'/>这是大卫·贝克毕生的工作，也是2024年诺贝尔奖的另一半。2003年，他的团队用Rosetta能量函数设计出了"
        "Top7，一种自然界从未见过的折叠，它按设计折叠了。不过二十年来，大多数设计都失败了。",

    'Deep learning changed both halves of design,':
        "深度学习改变了设计的两半，先从序列说起。<bookmark mark='a'/>2022年，贝克实验室的尤斯图斯·道帕拉斯等人做出了ProteinMPNN：它把主链"
        "读成一个图，每个残基与空间中离它最近的邻居相连，<bookmark mark='b'/>传递由距离构成的消息，所以主链朝哪个方向都无关紧要，<bookmark "
        "mark='c'/>然后按随机顺序一次写一个氨基酸，每个都以已经写好的那些为条件。<bookmark mark='d'/>在天然主链上，它能还原出52.4%的"
        "天然氨基酸，Rosetta是32.9%。",

    'Then the backbone. In 2023 Joseph Watson and colleagues':
        "然后是主链。2023年，约瑟夫·沃森等人发表了RFdiffusion。<bookmark mark='a'/>他们微调结构预测器RoseTTAFold，让它去除残基坐标系上的"
        "噪声，位置和朝向上的噪声，从噪声到一条主链走两百步，还可以让它保持一个基序、结合一个靶标或者满足某种对称性。<bookmark mark='b'/>"
        "流程是：扩散出一条主链；让ProteinMPNN为它写八条序列；<bookmark mark='c'/>只保留AlphaFold 2能折回到设计上的那些，误差在两埃以内、"
        "而且有把握；<bookmark mark='d'/>然后才进实验室。<bookmark mark='e'/>对于结合子，百分之十九成功了，大约是早先成功率的一百倍；一个流感"
        "结合子测出来的结构，离它的设计只有0.63埃。",

    'f"Our toy denoiser from the last chapter shows the idea in miniature.':
        "上一章的玩具去噪器能把这个想法缩小了展示出来。这是它的训练：损失，以及在每个检查点用同样八个噪声种子抽出的样本。<bookmark "
        "mark='a'/>一开始是乱线；然后是键长差不多正确的链；{last_stage}。<bookmark mark='b'/>它们是新的吗？样本的中位数离最近的训练链"
        "{nn_s:.2f}，而它从没见过的真实链是{nn_h:.2f}：{novel}。",

    "then compact folds like the training set's":
        '然后是像训练集那样的紧凑折叠',

    "f'then compact folds, though {100 * clash_s:.0f} percent":
        '然后是紧凑的折叠，不过最后的样本里仍有{100 * clash_s:.0f}%有两个原子挨得太近，而训练链从来不会这样',

    'farther than genuinely new chains are: not copies':
        '比真正的新链离得更远：不是照抄，但也还不完全像真的',

    'about as far from their nearest training chain as genuinely new chains are':
        '和真正的新链离最近训练链差不多远',

    'closer to training chains than genuinely new chains are, a sign of some copying':
        '比真正的新链离训练链更近，这说明有一些照抄',

    'Since then the field has moved fast.':
        "从那以后，这个领域发展得很快。<bookmark mark='a'/>2024年，谷歌DeepMind的AlphaProteo为医学靶标设计了结合子，<bookmark mark='b'/>"
        "BindCraft通过在AlphaFold 2本身里做梯度下降来设计结合子，<bookmark mark='c'/>EvolutionaryScale的ESM3，一个覆盖序列、结构和功能的"
        "语言模型，写出了一个和任何天然蛋白都相差很远的荧光蛋白。<bookmark mark='d'/>2025年，RFdiffusion3逐个原子地做设计，<bookmark "
        "mark='e'/>BoltzGen也作为一个开放的选择出现了。<bookmark mark='f'/>这么强大的工具可能被滥用；2024年，许多研究者签署了负责任生物设计"
        "的承诺，包括对DNA合成进行筛查。",

    'Design, in one line:':
        "一句话说设计：扩散出一条主链，为它写一条序列，检查这条序列能不能折回去，然后才把它做出来。现在从分子走向整个星球。",
})

ZH.update({
    # ------------------------------------------------------------------ Weather
    'Chapter thirteen. Weather on a mesh.':
        '第13章。网格上的天气。',

    'Weather forecasting became physics in 1904':
        "1904年，天气预报变成了物理学：维尔赫姆·皮耶克尼斯把它表述成一个初值问题，测出此刻的大气，再把流体方程向前推进。<bookmark "
        "mark='a'/>刘易斯·弗赖·理查森在第一次世界大战期间试着用手算：花了六个星期，为两个点做出一次六小时预报，结果错了一百四十五百帕。"
        "<bookmark mark='b'/>1950年，最早的计算机预报在ENIAC上运行，算得和天气本身差不多快。<bookmark mark='c'/>欧洲中期天气预报中心，"
        "ECMWF，在1979年发布了第一次预报；此后，预报大约每十年多出一天的技巧。",

    'Machine learning came to this in the 2020s':
        "到了2020年代，机器学习来到了这里，用ERA5训练，那是ECMWF对1940年以来全球天气的重建。2023年，谷歌DeepMind的雷米·拉姆等人发表了"
        "GraphCast。<bookmark mark='a'/>大气存储在一个经纬度网格上，一百万个点，每个点二百二十七个数，在两极附近挤得很密；GraphCast改在一个"
        "网格网上工作：<bookmark mark='b'/>一个细分六次的正二十面体，保留每一层的边，于是一条消息几步就能穿过整个星球。这是我们的小版本，在一个"
        "正方形上。<bookmark mark='c'/>编码到网格网上，传递十六次消息，再解码：由最近的两个状态得到六小时之后的状态。<bookmark mark='d'/>它不到"
        "一分钟就能做出一次十天预报，并在1380个目标中的百分之九十上胜过了ECMWF旗舰的确定性预报。",

    'Ours is a toy atmosphere:':
        "我们的是一个玩具大气：一个二维流体，在一个首尾相接的正方形上，被一个固定的图样搅动，又被摩擦减弱，于是涡旋生成、漂移、合并、消亡："
        "混沌，就像天气。<bookmark mark='a'/>一个小的编码–处理–解码网络在我们的网格网上，从三十二次模拟中一步一步地学习，然后在自己的预测上"
        "往前推。<bookmark mark='b'/>上面是真实情况；下面是我们的网络，从同一个起点出发。它们一致一段时间，然后渐行渐远。",

    '"Scored over eight new runs: the error, step by step.':
        "在八次新的模拟上打分：误差，一步一步看。<bookmark mark='a'/>{s1}。<bookmark mark='b'/>{s2}，{s3}。GraphCast训练时最多展开"
        "十二步，正是为了这个原因，从自己逐渐偏离的预测里学习；我们的网络在训练的最后阶段展开两步。<bookmark mark='c'/>{s4}，这是每个网络"
        "各训练一次的结果。",

    "f'One step ahead its error is":
        '提前一步，它的误差是{rm[0]:.2f}，而假设什么都不变的误差是{pers[0]:.2f}',

    "f'Even one step ahead it is no better":
        '即使只提前一步，它也不比假设什么都不变更好',

    "f'It stays ahead of persistence for {hor} steps'":
        '在{hor}步之内它都领先于持续性预报',

    "Its lead over persistence is short-lived":
        '它对持续性预报的领先很短暂',

    "f'and after {cross_c} steps it is worse":
        '而{cross_c}步之后，它比直接预报平均状态还差，每个混沌系统的预报最终都会这样',

    'and it stays better than the average state throughout':
        '而且自始至终都比平均状态好',

    'The long edges matter:':
        '长边是重要的：只用最短边的同一个网络，在前十步里表现更差',

    "f'Over the first ten steps the long edges make no difference":
        '在前十步里，长边没有带来差别；它们的作用在后面：到第二十步，只用最短边的网络误差是{e20f:.1f}，而多尺度网格是{e20m:.1f}',

    "In our toy the long edges don't help, at any lead time":
        '在我们的玩具里，无论提前多少步，长边都没有帮助',

    'There is a deeper problem.':
        "还有一个更深的问题。用平方误差训练，网络预测的是可能发生的情况的平均，而在很远的将来，许多种天气的平均是一片模糊。<bookmark "
        "mark='a'/>预报员用集合预报来应对：从略有不同的起点出发跑很多次。2024年，谷歌DeepMind的GenCast学会了用扩散来抽样下一个状态；它的"
        "集合预报在1320个目标中的97.2%上胜过了ECMWF的集合预报。<bookmark mark='b'/>然后，学出来的模型投入了日常业务：2025年2月是ECMWF的"
        "人工智能预报系统，那年7月是它的集合版本，<bookmark mark='c'/>11月是谷歌的WeatherNext 2，12月是美国NOAA的第一批AI全球模型。",

    'So the weather became a graph problem:':
        "于是天气变成了一个图问题：一个包住星球的网格网，几步就能穿过它的消息，以及为未来中无法知道的那一部分准备的扩散。接下来："
        "学会整个方程的网络。",

    # ------------------------------------------------------------------ Operators
    'Chapter fourteen. Neural operators.':
        '第14章。神经算子。',

    'Fields evolve by equations.':
        "场按方程演化。这是伯格斯方程，流体流动的一个一维漫画：一个波，在快的地方变陡，又被黏性抹平。<bookmark mark='a'/>从这个起点出发，"
        "一个时间单位之后，解是这个样子。<bookmark mark='b'/>求解器每次都要走几千个小步。一个网络可以学会从起点到终点的映射，但普通网络只处理"
        "一个固定长度的数列：用六十四个点训练，它就只认识这些点。<bookmark mark='c'/>我们要的是算子本身，一个从函数到函数的映射，在任何分辨率"
        "上都能读。<bookmark mark='d'/>陈天平和陈宏在1995年证明了网络可以逼近算子；DeepONet和傅里叶神经算子在2021年让它变得实用。",

    'The Fourier neural operator, from Zongyi Li':
        "傅里叶神经算子出自李宗仪、阿妮玛·阿南德库马尔、安德鲁·斯图尔特等人，它从一个积分形式的网络层出发：每个点的新值，通过一个核"
        "kappa，混合了整个场。<bookmark mark='a'/>如果核只依赖于偏移量，这个积分就是一个卷积，卷积定理把它变成傅里叶变换的乘积。<bookmark "
        "mark='b'/>所以直接学核的变换：给最低的那些频率各学一个复数权重，这里是十六个，其余的丢掉。<bookmark mark='c'/>权重属于频率，不属于"
        "格点，所以网络能读任何细到足以容纳它们的网格；平移直接穿过；而一层的代价大约是一次快速傅里叶变换。",

    'f"We trained one on a thousand solutions':
        "我们用伯格斯方程的一千个解训练了一个，采样在{res}个点上，以一个伪谱求解器的答案为准。<bookmark mark='a'/>这是它对一个从没见过的"
        "起点的预测，在训练的各个检查点上，旁边是学习曲线。<bookmark mark='b'/>最后，它在留出的起点上的相对误差是{100 * e_fin:.1f}%。",

    'f"Now the test that matters.':
        "现在是真正要紧的测试。两个网络都只在六十四个点上训练过。从{R[0]}个点到{R[-1]:,}个点去读它们。<bookmark mark='a'/>{f_txt}。"
        "<bookmark mark='b'/>{c_txt}。<bookmark mark='c'/>{coarse}。FourCastNet是最早的学习型天气模型之一，2022年推出，它就建立在这种"
        "傅里叶层的一个变体上。",

    "f'The CNN, at {100 * ec[i_tr]:.1f} percent":
        'CNN在它自己的网格上是{100 * ec[i_tr]:.1f}%，到最细的网格上变成了{100 * ec[-1]:.0f}%：它的核即使加了空洞，也是按格点来量的，'
        '所以在更细的网格上只能看到线上更窄的一段',

    "f'The CNN also transfers:":
        'CNN也能迁移：在它自己的网格上{100 * ec[i_tr]:.1f}%，在最细的网格上{100 * ec[-1]:.1f}%',

    'f"Below its training resolution':
        '在低于训练分辨率的{R[0]}个点上，算子的误差是{100 * ef[0]:.1f}%：这么粗的网格会把解形成的陡峭锋面抹平',

    'f"Even below its training resolution':
        '即使在低于训练分辨率的{R[0]}个点上，算子的误差也是{100 * ef[0]:.1f}%',

    'f"The Fourier neural operator\'s error stays':
        '傅里叶神经算子的误差在它自己的网格上是{100 * ef[i_tr]:.1f}%，在{R[-1]:,}个点、细{fine}倍的网格上是{100 * ef[-1]:.1f}%',

    'f"The Fourier neural operator\'s error grows':
        '傅里叶神经算子的误差从它自己网格上的{100 * ef[i_tr]:.1f}%，增长到{R[-1]:,}个点上的{100 * ef[-1]:.1f}%',

    'Learn the operator, not the grid.':
        "学算子，不学网格。属于频率的权重可以带到任何分辨率上，这正是一个物理世界的模型应该做到的。从场走向晶体。",

    # ------------------------------------------------------------------ Materials
    'Chapter fifteen. Materials by the million.':
        '第15章。百万量级的材料。',

    'f"A crystal is a pattern of atoms repeated in space;':
        "晶体是原子在空间里重复排列的图样；它的对称性属于230种空间群之一，1891年就分类完了。哪些晶体存在？<bookmark mark='a'/>取两种元素"
        "A和B，以及它们可能的化合物，每个都有一个由密度泛函理论算出的形成能，每个要花好几个小时的计算机时间。<bookmark mark='b'/>如果没有"
        "其他化合物的混合物能量更低，这个化合物就是稳定的：它落在下凸包上。<bookmark mark='c'/>在凸包上方的化合物宁愿分解成它的邻居；它的"
        "高度说明它有多不稳定。这里有{words_num(n_st)}个化合物在凸包上。",

    'In 2023 Amil Merchant, Ekin Dogus Cubuk and colleagues':
        "2023年，谷歌DeepMind的阿米尔·默钱特、埃金·多古斯·丘布克等人发表了GNoME，用于材料探索的图网络。<bookmark mark='a'/>它通过替换"
        "已知晶体里的元素、以及随机搜索，来生成候选；<bookmark mark='b'/>建立在原子间距离之上、因而与转动无关的图网络，预测它们的能量；"
        "<bookmark mark='c'/>密度泛函理论检查最有希望的那些；<bookmark mark='d'/>每一次检查都变成下一轮的训练数据。<bookmark mark='e'/>此前，"
        "计算方法找到了大约四万八千种稳定晶体；GNoME报告了220万种，其中38.1万种在新的凸包上，它挑出来、被DFT确认的比例升到了百分之八十以上，"
        "而此前只有百分之一左右。",

    'f"We can run the flywheel on a made-up chemistry:':
        "我们可以在一个虚构的化学体系上转动这个飞轮：二十种虚构的元素，两两组合，九种配比，四种晶体类型，共{m['n_candidates']:,}个候选，"
        "它们的“DFT”能量是一个隐藏的公式，每次只揭开六十个。<bookmark mark='a'/>一开始知道百分之三。每一轮，用已知的数据训练一个小集成模型，"
        "检查预测会落到其余一切的凸包下方最远的六十个。命中，就是挑中一个真正稳定的化合物。<bookmark mark='b'/>随机挑选的命中率是"
        "{100 * h_r.mean():.0f}%，大约就是稳定候选所占的比例，{100 * share:.0f}%。<bookmark mark='c'/>代理模型的挑选在第一轮命中"
        "{100 * h_m[0]:.0f}%，{trend}。<bookmark mark='d'/>它的误差从{mae[0]:.3f}降到{mae[-1]:.3f}，{rounds}轮之后，它找到了{m['n_stable']}个"
        "真正稳定的化合物中的{F['model'][:, -1].mean():.0f}个，而随机挑选找到{F['random'][:, -1].mean():.0f}个。",

    "f'and it climbs as the surrogate learns":
        '而且随着代理模型的学习不断上升，从第一轮的{hm0:.0f}%升到最后一轮的{hm1:.0f}%',

    "f'rise to {hmax:.0f}, and then fall, to":
        '升到{hmax:.0f}%，然后随着最容易找到的稳定化合物被用光而下降，最后一轮是{hm1:.0f}%；仍是随机命中率的好几倍',

    "f'and then fall, to {hm1:.0f} in the last round":
        '然后随着最容易找到的稳定化合物被用光而下降，最后一轮是{hm1:.0f}%；仍是随机命中率的好几倍',

    "f'and it stays around":
        '而且一直在{100 * h_m.mean():.0f}%左右：在我们的玩具里，代理模型从一开始就不错',

    'The claims drew pushback from chemists.':
        "这些说法遭到了化学家的质疑。<bookmark mark='a'/>2024年，安东尼·奇塔姆和拉姆·谢沙德里随机抽查了GNoME的一批预测，发现很少有证据"
        "表明其中有同时称得上新颖、可信又有用的化合物；许多预测把原子排成整齐的有序结构，而真实晶体里这些原子是随机混排的。<bookmark "
        "mark='b'/>批评者还对一个机器人实验室报告四十一种新化合物所依据的X射线分析提出了异议；2026年1月，这篇论文被更正为五十七个目标中的"
        "三十六种。<bookmark mark='c'/>工具在不断进步，通用势函数，晶体生成器，<bookmark mark='d'/>但教训留了下来：预测出来的晶体只是一个"
        "假设，把它做出来才是检验。",

    'In materials, then, the network is a cheap first opinion':
        "所以在材料领域，网络是一个便宜的初步意见，让昂贵的检查物尽其用。而在数学里，检查可以是完美的。",

    # ------------------------------------------------------------------ Proofs
    'Chapter sixteen. Geometry and proofs.':
        '第16章。几何与证明。',

    'Mathematics has something no other science has:':
        "数学有一样别的科学都没有的东西：一个骗不了的检查器。<bookmark mark='a'/>在Lean这样的证明助手里，定理和证明都是代码，一个小小的内核"
        "检查每一步推理；这一个说的是，n乘以n加1是偶数。<bookmark mark='b'/>计算机进入证明是在1976年，阿佩尔和哈肯的四色定理，2005年乔治·"
        "贡蒂埃对它做了形式化检查。<bookmark mark='c'/>托马斯·黑尔斯对开普勒猜想的证明在2014年得到了形式化验证，<bookmark mark='d'/>2022年，"
        "Lean社区把达斯汀·克劳森和彼得·舒尔茨的一个困难的新定理形式化了。<bookmark mark='e'/>Lean的库Mathlib现在收录了大约二十九万条定理；"
        "第28部分会讲强化学习拿这样的检查器做了什么。",

    'Olympiad geometry fell first.':
        "奥赛几何最先被攻下。2024年1月，谷歌DeepMind的陈天如、梁明唐等人发表了AlphaGeometry。<bookmark mark='a'/>没有人类证明可学，他们"
        "就自己造：随机的前提，一个推出所有后果的符号引擎，再从每个新事实回溯到它需要的东西：一亿条带证明的定理。<bookmark mark='b'/>其中"
        "百分之九需要一个题目里从未提到的点，一条辅助构造，这是有创造性的那一步；一个语言模型学会了提出这些点，其余的交给引擎。<bookmark "
        "mark='c'/>在三十道奥赛题上，它解出了二十五道，此前最好的方法是十道，它的引擎单独是十四道，GPT-4是零道；金牌得主平均解出25.9道。"
        "<bookmark mark='d'/>一年后，AlphaGeometry 2解出了2000年以来国际数学奥林匹克几何题的百分之八十四。",

    'Then the olympiad itself, which Part 28 follows in detail.':
        "然后是奥赛本身，第28部分会详细讲。<bookmark mark='a'/>2024年，在Lean里工作的AlphaZero方法AlphaProof，加上负责几何的"
        "AlphaGeometry 2，拿到了四十二分里的二十八分，离金牌差一分。<bookmark mark='b'/>2025年，谷歌的Gemini Deep Think和OpenAI的一个"
        "实验模型各自拿到三十五分，正好是金牌线，证明是用普通语言写的。<bookmark mark='c'/>而在2026年7月的上海，华为和小红书报告拿到了满分，"
        "四十二分里的四十二分，解答提交给了组织方评分，据法新社报道；六百六十六名学生里也有七人拿了四十二分。作为对机器的测试，奥赛已经"
        "接近饱和。",

    'Beyond contests, the frontier is research mathematics.':
        "在比赛之外，前沿是研究级的数学。<bookmark mark='a'/>自动形式化，也就是把非形式的数学翻译成Lean，速度猛然加快：2025年9月，初创公司"
        "Math Inc.报告说，它的智能体Gauss用大约三个星期，把强素数定理形式化了，大约两万五千行Lean代码。<bookmark mark='b'/>2026年1月，"
        "OpenAI的GPT-5.2 Pro和Harmonic的证明器Aristotle解决了埃尔德什第728号问题，最后给出的是一个Lean证明。<bookmark mark='c'/>谷歌"
        "DeepMind的一个团队让Gemini处理了七百个未解的埃尔德什问题：解决了十三个，五个靠的是看来是新的论证，八个是因为答案原来已经在文献里了。"
        "<bookmark mark='d'/>两点提醒：形式化证明恰好证明它的陈述，所以译错的陈述证明的是错的东西；而且最先被攻下的都是比较容易的问题。",

    'With a perfect checker, search can be trusted:':
        "有了完美的检查器，搜索就可以信任：放手去生成，只留下通过检查的。最后一章讲的正是这个。",

    # ------------------------------------------------------------------ Search
    'Chapter seventeen. Discovery by search.':
        '第17章。靠搜索做发现。',

    'When the checker is exact, discovery becomes a loop.':
        "当检查器是精确的，发现就变成了一个循环。<bookmark mark='a'/>提出一个候选，一段程序或一个构造；<bookmark mark='b'/>精确地给它打分；"
        "<bookmark mark='c'/>留下最好的，再变化它们。<bookmark mark='d'/>2022年的AlphaTensor用一个AlphaZero网络来提出候选。2023年12月，"
        "谷歌DeepMind的贝尔纳迪诺·罗梅拉-帕雷德斯等人的FunSearch把提出者换成了一个写Python的语言模型，程序放在彼此分开的岛上，就像进化中的"
        "种群。<bookmark mark='e'/>它在八维空间里找到了一个帽集，五百一十二个点，没有三点共线，超过了已知的四百九十六个。",

    'f"Let\'s run that loop ourselves':
        "我们自己来跑这个循环，用FunSearch的一个问题：在线装箱。<bookmark mark='a'/>物品一个一个到来，每个都必须立刻放进一个箱子。一条规则"
        "来决定：给物品放得下的每个箱子打分，挑分最高的。<bookmark mark='b'/>经典的规则是最佳适配：挑剩余空间最小的箱子。<bookmark "
        "mark='c'/>我们把这样的打分当作公式来进化，用随机的变异和交叉代替语言模型，按它们在八个训练序列上用了多少箱子来评判。{evo_line}。"
        "<bookmark mark='d'/>{res_line}。<bookmark mark='e'/>{gen_line}。",

    "Ours carried over; but an independent study in 2025":
        '我们的规则迁移过去了；不过2025年的一项独立研究发现，语言模型进化出来的启发式方法常常无法推广到培育它们的那些实例之外',

    'An independent study in 2025 found the same of heuristics':
        '2025年的一项独立研究对语言模型进化出来的启发式方法也有同样的发现：它们常常无法推广到培育它们的那些实例之外',

    "f'Within {int(gens[-1])} generations":
        '{int(gens[-1])}代之内，它在训练实例上比最佳适配好{gain:.2f}个百分点',

    "f'In {int(gens[-1])} generations it never beats":
        '{int(gens[-1])}代里，它在训练实例上从没胜过最佳适配',

    "f'On new, longer sequences of items, both evolved rules":
        '在新的、更长的物品序列上，两条进化出来的规则仍然都胜过最佳适配：{tests[0]:.2f}%和{tests[-1]:.2f}%，对{bf_te:.2f}%',

    'f"On new, longer sequences, {words_num(len(better))}':
        '在新的、更长的序列上，{words_num(len(tests))}条进化出来的规则中有{words_num(len(better))}条胜过最佳适配，{min(better):.2f}%对'
        '{bf_te:.2f}%；另一条没有',

    'f"On new, longer sequences of items, neither evolved rule':
        '在新的、更长的物品序列上，两条进化出来的规则都没有胜过最佳适配的{bf_te:.2f}%：进化找到的东西，是为它的训练实例量身定做的',

    'f"Matrix multiplication is the purest case.':
        "矩阵乘法是最纯粹的例子。<bookmark mark='a'/>按教科书的方法，两个n乘n矩阵相乘要做n的三次方次乘法。<bookmark mark='b'/>把这个乘积"
        "写成一个三向张量；<bookmark mark='c'/>那么，把这个张量写成R个简单乘积之和的每一种写法，都是一个只用R次乘法的算法。<bookmark "
        "mark='d'/>1969年，福尔克尔·施特拉森为二乘二矩阵找到了七次的算法，而不是八次；两年后，什穆埃尔·维诺格拉德证明了七就是最少的。"
        "<bookmark mark='e'/>我们用数值方法搜索这些分解，每个秩从三十个随机起点出发。{s6}。{s7}。",

    "f'At rank six, none of the":
        '秩为六时，{r6[2]}个起点没有一个能把误差降到{r6[3]:.2f}以下：根本不存在六次乘法的算法可找',

    "f'At rank six, {r6[1]} starts report zero error":
        '秩为六时，有{r6[1]}个起点报告误差为零，这会和定理矛盾：是数值上的假象',

    'f"For three by three matrices the record, Julian Laderman\'s from 1976, is twenty-three multiplications, and':
        '对三乘三矩阵，纪录是朱利安·拉德曼1976年给出的二十三次乘法；我们在这个秩上的{n3_tries}个起点里，有{n3_ok}个找到了',

    'f"For three by three matrices the record, Julian Laderman\'s from 1976, is twenty-three multiplications; from':
        '对三乘三矩阵，纪录是朱利安·拉德曼1976年给出的二十三次乘法；在这个秩上从{n3_tries}个起点出发，在二十六上也一样多，我们的搜索'
        '离零只差{tiny3}，却始终没有精确到零：矩阵一变大，精确的分解就成了大海里的针',

    "f'At rank seven, {r7[1]} of":
        '秩为七时，{r7[2]}个起点里有{r7[1]}个找到了：一个类似施特拉森的算法，它把随机矩阵乘对到小数点后{vdp}位',

    'In May 2025 Google DeepMind combined both lines in AlphaEvolve.':
        "2025年5月，谷歌DeepMind在AlphaEvolve里把两条路线结合了起来。<bookmark mark='a'/>Gemini模型对整段程序提出修改，评估器给它们打分，"
        "进化留下最好的。<bookmark mark='b'/>它的成果之一：用四十八次乘法完成四乘四复矩阵的乘法，打破了把施特拉森的技巧用两次得到的四十九次，"
        "那是1969年以来的纪录，<bookmark mark='c'/>靠的是进化一个像我们这样的分解搜索。<bookmark mark='d'/>几个星期之内，法国的三位研究者找到了"
        "一个系数为有理数的四十八次方案。<bookmark mark='e'/>它还把十一维空间里能与中心球相切的球数提高到593个；在五十多个未解问题上，四分之三"
        "追平了已知最好的答案，五分之一改进了它。<bookmark mark='f'/>在谷歌内部，它找到的一条调度规则收回了公司0.7%的算力。<bookmark "
        "mark='g'/>2025年11月，陶哲轩等人在六十七个问题上试用了它，连失败也一并发表了。",

    'Discovery by search, then:':
        "所以，靠搜索做发现：放手去提出，精确地检查，留下经得起检查的。只要检查是精确的，它就管用，这就是数学和算法走在最前面的原因。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来盘点一下。对称是一个不应该改变答案的变换；网络可以精确地尊重它，靠构造；也可以近似地尊重它，靠例子。求和构成集合上的函数；"
        "对邻居求和构成图网络，它看见的正是颜色细化看见的，叠得太深就会变模糊。内置转动让我们的分子模型在同样的数据上好得多。AlphaFold通过"
        "用三角形保持一致的残基对来读蛋白质，用坐标系把它搭起来，再用一个分得清左右的损失来打分；它的后继者把原子交给了扩散。天气在网格网上"
        "运行，方程被当作算子来学，晶体按百万量级筛选，而在检查器完美的地方，搜索带来发现。",

    'All of this comes back.':
        "这一切都还会再出现。<bookmark mark='a'/>由网络引导、由精确检查器评判的搜索，就是下一次的AlphaZero，以及第28部分的推理模型。"
        "<bookmark mark='b'/>一个把世界向前推演的学习型模拟器，就像我们的网格网络，就是第29部分的世界模型。<bookmark mark='c'/>网络的各层"
        "表示了什么，它们是否尊重我们期望的对称，是第30部分的主题。<bookmark mark='d'/>而CASP的盲测和一个几乎饱和的奥赛，引向第31部分的问题："
        "到底该怎样评估。",

    'Here are six problems to try,':
        "这里有六道习题，从等变映射的复合到傅里叶层。在这里暂停一下，动手做一做；完整的解答在本部分的讲义里。",

    'Next time, the fifth act: agency.':
        "下一次，第五幕：能动性。本章的搜索循环，提出、检查、保留最好的，变成了从奖励中学习：智能体行动，世界给出回应，智能体不断改进，"
        "一直到AlphaZero，我们会亲手训练一个。第26部分：强化学习，从贝尔曼到AlphaZero。",

    'To go deeper, Bronstein, Bruna, Cohen':
        "想深入了解，布朗斯坦、布鲁纳、科恩和韦利奇科维奇关于几何深度学习的书是整个这一部分的地图，威廉·汉密尔顿的小书把图网络讲得"
        "很清楚。感谢收看，我们第26部分再见。",
})

ZH.update({
    "f'{rng_i:.4f} of a unit":
        '{rng_i:.4f}个单位，比单纯的舍入误差大',
})
