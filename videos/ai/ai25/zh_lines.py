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
        "斯德哥尔摩，2024年10月。<bookmark mark='a'/>诺贝尔化学奖一半授予大卫·贝克，表彰他用计算机设计蛋白质；另一半授予谷歌DeepMind的"
        "德米斯·哈萨比斯和约翰·江珀，表彰AlphaFold，一个能预测蛋白质折叠成什么形状的神经网络。<bookmark mark='b'/>就在前一天，"
        "物理学奖授予了约翰·霍普菲尔德和杰弗里·辛顿，表彰的正是第20部分讲过的那些神经网络。<bookmark mark='c'/>几十年来，测定一个蛋白质的"
        "形状，一个实验室可能要花好几年。AlphaFold几分钟就能预测出一个，误差常常不到一个原子的宽度。",

    'f"Here is the idea this part is built on.':
        "这一部分建立在这样一个想法上。五个带电粒子：一个玩具分子。把它在空间里转一转，它本身什么也没变，所以它的能量也不可能变。"
        "<bookmark mark='a'/>我们用三千个这样的分子训练网络去预测能量，然后把其中一个转上整整一圈。<bookmark mark='b'/>一个普通网络"
        "根本不知道转动是无害的：分子转动时，它的答案摆动了{rng_m:.2f}个单位。<bookmark mark='c'/>训练时给它看转过的副本，它摆动{rng_a:.2f}。"
        "<bookmark mark='d'/>而一个建立在粒子间距离上的网络，根本看不见转动：它的答案变化{tiny}，离真实能量差{inv_err:.2f}。",

    'less than a millionth of a unit, rounding error':
        '不到百万分之一个单位，只是舍入误差',

    'less than a ten-thousandth of a unit, rounding error':
        '不到万分之一个单位，只是舍入误差',

    'That is the question of this part:':
        "这就是本部分的问题：一个网络知道了问题的对称性，能得到什么？这又为科学带来了什么？<bookmark mark='a'/>我们会从群和图讲起，"
        "经过随分子一起转动的网络，一直讲到折叠蛋白质的系统、<bookmark mark='b'/>预报天气的系统、<bookmark mark='c'/>寻找新材料的系统，"
        "<bookmark mark='d'/>以及证明定理的系统。一路上的每个实验都在这台机器上计算；关于那些大系统的每个数字，都引自它们自己的论文。",

    'This is Part 25 of AI, Built':
        "这是《人工智能，从零搭建》的第25部分，也是第四幕的最后一部分。<bookmark mark='a'/>本部分的内容：对称性，以及一个函数尊重对称性"
        "是什么意思；<bookmark mark='o2'/>图，在图上传递消息的网络，以及它们能分辨什么的极限；<bookmark mark='o3'/>随分子一起转动的网络；"
        "<bookmark mark='o4'/>蛋白质，从折叠问题到AlphaFold和蛋白质设计；<bookmark mark='o5'/>场：天气、神经算子，以及对材料的搜索；"
        "<bookmark mark='o6'/>还有数学，从奥赛几何，到机器能检查的证明，再到靠搜索做出的发现。",

    # ------------------------------------------------------------------ History
    'Chapter one. How we got here.':
        '第1章。我们是怎么走到这里的。',

    "This part's story has three threads":
        "这一部分的故事有三条线索，起点相隔很远。<bookmark mark='m0'/>1950年，冯·诺依曼的团队在ENIAC上做出了第一次计算机天气预报。"
        "<bookmark mark='m1'/>1958年，约翰·肯德鲁靠X射线衍射，第一次看到了一个蛋白质的三维结构，肌红蛋白；1961年，克里斯蒂安·安芬森证明"
        "蛋白质能自己重新折叠：它的氨基酸序列决定了它的形状。<bookmark mark='m2'/>1968年，鲍里斯·魏斯费勒和安德烈·莱曼发表了一种检验"
        "两个图是否相同的方法，后来人们发现，它恰好衡量了图网络能看见什么。<bookmark mark='m3'/>蛋白质数据库在1971年开张，里面有7个结构；"
        "<bookmark mark='m4'/>欧洲中期天气预报中心在1979年发布了第一次预报。<bookmark mark='m5'/>1989年，卷积网络把图像的对称性，"
        "也就是平移，做进了网络层里，第10部分讲过。<bookmark mark='m6'/>1994年，约翰·莫尔特和克日什托夫·菲德利斯创办了CASP，"
        "一个预测蛋白质结构的盲测比赛；<bookmark mark='m7'/>2005年，马尔科·戈里、加布里埃莱·蒙法尔迪尼和弗朗科·斯卡塞利提出了"
        "能在图上工作的神经网络。",

    'Then, within a decade, the threads met.':
        "然后，在十年之内，这几条线索汇合了。<bookmark mark='d0'/>2017年，图网络有了通用的配方，消息传递，同时也有了处理集合和分子的"
        "网络。<bookmark mark='d1'/>2018年，DeepMind的第一代AlphaFold赢得了CASP；两年后，AlphaFold 2的精度接近了实验。<bookmark "
        "mark='d2'/>随分子一起转动的网络，以及能学会物理方程整体解的网络，在2021年相继出现。<bookmark mark='d3'/>到2022年，两亿多个蛋白质"
        "的预测结构已经可以免费下载。<bookmark mark='d4'/>2023年，一个图网络在大多数指标上胜过了世界上最好的天气模型，另一个提出了"
        "数以百万计的新晶体。<bookmark mark='d5'/>2024年有了诺贝尔奖、AlphaFold 3，还有能解奥赛题的机器；<bookmark mark='d6'/>2025年，"
        "AI天气预报进入了日常业务运行，进化搜索找到了新的数学；<bookmark mark='d7'/>而在2026年，保罗·埃尔德什留下的一些未解问题被AI系统"
        "解决了，其中一个还附上了计算机检查过的证明。",

    'What ties these together is one recipe.':
        "把这些串起来的是同一个配方。<bookmark mark='a'/>问一问：你的数据里什么是无关紧要的。对图像来说，物体在哪个位置：所以用卷积。"
        "<bookmark mark='b'/>对一组点来说，是它们的顺序。<bookmark mark='c'/>对一个图来说，是它的节点碰巧怎么编号。<bookmark mark='d'/>对一个"
        "分子来说，是它在空间里怎么转、怎么移。<bookmark mark='e'/>蛋白质同时具有以上所有这些。<bookmark mark='f'/>天气场位于球面上，"
        "不应该依赖它被存储时用的网格。<bookmark mark='g'/>相比之下，语言没有多少对称性可以利用，这也是Transformer要从数据里学出结构的"
        "原因之一。<bookmark mark='h'/>迈克尔·布朗斯坦、琼·布鲁纳、塔科·科恩和佩塔尔·韦利奇科维奇把这个纲领称为几何深度学习。"
        "把对称性放进模型有三种办法：给它看数据变换后的副本，先把每个输入摆成标准姿态，或者把对称性做进网络层里。本部分主要讲第三种。",

    # ------------------------------------------------------------------ Symmetry
    'Chapter two. Invariance and equivariance.':
        '第2章。不变性与等变性。',

    'f"A symmetry is a transformation that leaves what matters unchanged.':
        "对称是一种变换，它让要紧的东西保持不变。把一个正方形转九十度，你得到的还是同一个正方形。<bookmark mark='a'/>转四次，"
        "你就回到了起点。<bookmark mark='b'/>一个问题的所有变换构成一个群：可以一个接一个地做，有一个什么都不做的变换，而且每个变换都能"
        "撤销。<bookmark mark='c'/>正方形有四种转法。十六个点的排列方式构成一个置换群，有十六的阶乘个元素，大约{n16 / 1000000000000.0:.0f}"
        "万亿。<bookmark mark='d'/>空间的转动构成一个连续群，SO(3)，有无穷多个元素；而一幅图像有它的平移。",

    'Now a function of the data, f:':
        "现在考虑数据的一个函数f：这里是我们的五个粒子在一个时间单位之后各自会到哪里。<bookmark mark='a'/>先转动输入，再应用f，"
        "<bookmark mark='b'/>或者先应用f，再转动输出。<bookmark mark='c'/>如果两条路总是得到同一个结果，f就是等变的：输入怎么变换，输出就"
        "怎么变换。<bookmark mark='d'/>如果输出根本不变，f就是不变的：比如分子的能量，或者图像的类别。<bookmark mark='e'/>中间的网络层"
        "需要等变性，这样关于输入被怎么转过的信息才会保留下来，而不是被扔掉；最终的答案常常需要不变性。",

    'There is a way to make any function equivariant.':
        "有一个办法能让任何函数变成等变的。在群上对它取平均：对每个变换g，先变换输入，再应用f，再在输出上撤销g。<bookmark mark='a'/>"
        "给这个平均喂一个转过的输入，h作用在x上。<bookmark mark='b'/>把g乘h改名叫g撇：g跑遍整个群，g撇也跑遍整个群，所以这还是同一个和。"
        "<bookmark mark='c'/>乘积的逆把顺序倒过来，<bookmark mark='d'/>于是h可以提到和的外面。不管f是什么，这个平均都是等变的。<bookmark "
        "mark='e'/>问题在于代价：群里每个元素都要算一次，十六个点就是十六的阶乘次，空间转动则是无穷多次。<bookmark mark='f'/>数据增强是"
        "便宜的版本：每个训练样本随机做一个变换，然后寄希望于网络自己学会剩下的部分。",

    'f"Here is the check, computed on our five-particle system':
        "检验来了，在我们的五粒子系统上计算：四个网络，用同样的数据、同样的步数训练。<bookmark mark='a'/>先停下来预测一下：输入转动时，"
        "哪个网络的答案会精确地跟着转？<bookmark mark='b'/>等变网络EGNN，我们会在第7章搭建它：它对转过、平移过的输入给出的答案，偏差只有"
        "{eg_tiny}个单位，只是舍入误差。<bookmark mark='c'/>直接吃原始坐标的消息传递网络能精确地处理重新编号，因为它对邻居求和，但处理不了"
        "转动。<bookmark mark='d'/>普通的MLP一样都做不到精确；训练时给它看转过的副本，它的转动误差是{ma['err']:.2f}，{aug_verdict}。"
        "<bookmark mark='e'/>这就是本章的教训：做进网络层里的对称性精确成立，对每个输入都成立；从样本里学来的对称性只是近似成立，"
        "而且只在它见过的数据附近成立。",

    'smaller than its own error, but not zero':
        '比它自己的预测误差小，但不是零',

    # ------------------------------------------------------------------ Sets
    'Chapter three. Functions of sets.':
        '第3章。集合上的函数。',

    'f"Sixteen points in the plane, drawn from one of four shapes':
        "平面上的十六个点，来自四种形状之一：一个环、一个圆盘、一条线段，或者两团点。任务是说出是哪一种。<bookmark mark='a'/>普通网络"
        "需要把输入排成一个列表，所以我们给点编号，喂给它三十二个坐标。<bookmark mark='b'/>但编号是任意的。重新编号，图没变，列表却变了。"
        "<bookmark mark='c'/>一个用八千组集合训练出来的普通网络，看到的却是一个新输入：{mlp_line}。<bookmark mark='d'/>一个为集合而建的"
        "网络，Deep Sets，给出完全相同的答案，它也必须如此。",

    "f'its belief that this is a ring goes from":
        '它认为这是一个环的把握，从{100 * pm[0]:.0f}%变成了{100 * pm2[0]:.0f}%',

    "f'it changes its mind: from":
        '它改了主意：从{names[int(pm.argmax())]}变成了{names[int(pm2.argmax())]}',

    'The theorem behind Deep Sets':
        "Deep Sets背后的定理，来自曼齐尔·扎希尔等人，2017年：一个集合函数忽略元素的顺序，当且仅当它能写成先对元素求一个函数phi的和，"
        "再接另一个函数rho。<bookmark mark='a'/>一个方向很容易：求和与顺序无关。<bookmark mark='b'/>另一个方向，给每个可能的元素编号，"
        "令phi(x)等于四的负编号次方。<bookmark mark='c'/>那么这个和写成四进制，第k位是1当且仅当第k个元素在集合里：没有进位，所以不同的"
        "集合给出不同的和。<bookmark mark='d'/>这个和是一一对应的；所以集合的任何函数都是这个和的函数：先把和还原，再应用f。<bookmark "
        "mark='e'/>对实数集合，扮演同样角色的是幂和：x、x平方，一直到x的n次方的和，按牛顿恒等式能确定n个数；爱德华·瓦格斯塔夫等人"
        "证明了，更短的和做不到连续地确定它们。",

    'As a network, this is simple.':
        "做成网络，这很简单。<bookmark mark='a'/>同一个小网络phi单独读每个点，<bookmark mark='b'/>把结果加起来，<bookmark mark='c'/>"
        "第二个网络rho读这个和。<bookmark mark='d'/>phi的权重被所有点共享，就像卷积在不同位置之间共享权重。<bookmark mark='e'/>同一年的"
        "PointNet用最大值代替了求和。而一个没有位置信息的Transformer把它的词元当作一个集合：把输入重新排序，每个输出都跟着它的输入移动，"
        "这是集合上的一个等变函数。",

    'f"Now train them, on {n0} sets up to':
        "现在来训练，从{n0}组集合到{n_big:,}组，每种三个种子，步数相同。<bookmark mark='a'/>只用{n0}组集合，Deep Sets就已经有"
        "{100 * a_ds[0]:.0f}%的时候是对的。<bookmark mark='b'/>普通MLP是{100 * a_ml[0]:.0f}%，{mlp_vs}：它必须从样本里学会，十六的阶乘种"
        "排列其实是同一个东西。<bookmark mark='c'/>给它看重新排序的副本帮助很大：{n0}组集合时是{100 * a_au[0]:.0f}%。{reach_txt}。"
        "{last}：{100 * a_ds[-1]:.0f}%对{100 * a_au[-1]:.0f}%。<bookmark mark='d'/>但副本只能近似地教会对称性：把同一个测试集重新排序，"
        "普通MLP在{100 * f_ml:.0f}%的集合上改了答案，用副本训练的那个在{100 * f_au:.0f}%的集合上改了答案，而Deep Sets一个也没改。",

    'At the largest size the copies have nearly caught up':
        '在最大的规模上，副本几乎追上来了',

    'Even at the largest size Deep Sets stays ahead':
        '即使在最大的规模上，Deep Sets仍然领先',

    "f'and even with {n_big:,} sets it stays below":
        '而且即使用{n_big:,}组集合，它仍然不如Deep Sets只用{n0}组时的水平',

    "f'and it needs {reach_m[0]:,} sets to reach":
        '它需要{reach_m[0]:,}组集合，才能达到Deep Sets用{n0}组时的水平',

    "f'The MLP with reordered copies needs":
        '用重新排序副本训练的MLP，需要{reach[0]:,}组集合才能追上这个水平',

    "f'The MLP with reordered copies never matches":
        '用重新排序副本训练的MLP，即使用{n_big:,}组集合，也追不上这个水平',

    'So building the symmetry in did two things:':
        "所以把对称性做进去带来了两件事：它节省了数据，因为要学的东西少了；它还让答案精确地与顺序无关，对每个输入都是如此，而不只是对"
        "像训练数据的那些输入。接下来是图：带连接的集合。",

    # ------------------------------------------------------------------ Messages
    'Chapter four. Message passing.':
        '第4章。消息传递。',

    'A graph is a set with connections:':
        "图是带连接的集合：一些节点，以及某些节点对之间的边。这是十氢萘，十个碳原子，十一根化学键。<bookmark mark='a'/>计算机把它存成"
        "一张表，邻接矩阵，凡是两个节点相连的地方就记一个1。<bookmark mark='b'/>但节点的编号是任意的。换一种编号，矩阵看起来就不一样了，"
        "行和列被打乱了，可分子还是同一个。<bookmark mark='c'/>所以图上的网络必须对重新编号等变：把节点置换一下，网络对各节点的答案也按"
        "同样方式置换，其他什么都不变。<bookmark mark='d'/>图无处不在：分子、道路图、社交网络、天气模型用的网格，还有蛋白质，在空间里"
        "离得近的残基就连起来。",

    'In 2017 Justin Gilmer and colleagues at Google':
        "2017年，谷歌的贾斯汀·吉尔默等人把这一族网络统一成一种形式：消息传递。每个节点保存一个状态，一个向量h。<bookmark mark='a'/>每一层，"
        "每个节点从邻居那里收集消息，消息是两个状态和这条边的一个学出来的函数M，然后把它们加起来。<bookmark mark='b'/>接着，它用旧状态和"
        "这个和来更新自己的状态。<bookmark mark='c'/>经过几层之后，一个读出函数把所有节点的状态加起来，给出关于整个图的答案。"
        "<bookmark mark='d'/>因为每一步都是对邻居求和，节点怎么编号就无关紧要：这个网络从构造上就是等变的，和Deep Sets一样。<bookmark "
        "mark='e'/>托马斯·基普夫和马克斯·韦林的图卷积网络是最简单的情形：对邻居的状态按度归一化后取平均，再乘一个权重矩阵。",

    'The idea is older than its name.':
        "这个想法比它的名字更早。<bookmark mark='a'/>1997年，亚历山德罗·斯佩尔杜蒂和安东尼娜·斯塔里塔就训练过读带标签的树和图的网络。"
        "<bookmark mark='b'/>2005年，马尔科·戈里等人提出了图神经网络，节点状态根据邻居反复更新，直到稳定。<bookmark mark='c'/>2014年，"
        "琼·布鲁纳等人通过图的谱来定义卷积，在随后两年里被简化成图卷积网络。<bookmark mark='d'/>2015年，大卫·杜维诺等人学出了分子的指纹。"
        "<bookmark mark='e'/>随后吉尔默的消息传递网络预测了十三万四千个小分子的十三种量子性质，其中十一种达到了化学精度。<bookmark "
        "mark='f'/>彼得·巴塔利亚等人则论证说，图是让网络具备关系结构的通用办法。",

    'f"Let\'s train one. Three hundred people in three communities':
        "我们来训练一个。三百个人，分在三个社群里，友谊大多在社群内部：{100 * intra:.0f}%的边在社群内，平均每人大约{deg:.0f}条。每个人"
        "只带着一个关于自己社群的、微弱而嘈杂的线索，而且只有{n_lab}个人有标签。<bookmark mark='a'/>一个两层的图卷积网络从这些标签和图里"
        "学习：看它对其他所有人的猜测，按社群上色。<bookmark mark='b'/>每一层都混入邻居，所以两层能看到两跳远。<bookmark mark='c'/>一个只看"
        "每个人自己线索的MLP猜对了{100 * np.mean(acc_m):.0f}%；图网络猜对了{100 * np.mean(acc_g):.0f}%，三个种子的平均。{verdict}。",

    'Passing messages more than doubles what the hints alone give':
        '传递消息让结果比只看线索时翻了一倍还多',

    'Passing messages lifts it well above the hints alone':
        '传递消息让结果远远超过只看线索的水平',

    'Passing messages helps only a little here':
        '在这里，传递消息只帮了一点点',

    'That is message passing:':
        "这就是消息传递：一个学出来的邻居求和，重复多次，于是经过L层之后，每个节点都听到了L跳以内的所有节点。这就引出一个问题："
        "这样的网络能分辨什么？",

    # ------------------------------------------------------------------ WL
    "Chapter five. What message passing can't see.":
        '第5章。消息传递看不见的东西。',

    'f"In 1968 Boris Weisfeiler and Andrei Leman described colour refinement':
        "1968年，鲍里斯·魏斯费勒和安德烈·莱曼描述了颜色细化，这是检验两个图是否其实是同一个图、只是编号不同的标准的第一步检验。"
        "<bookmark mark='a'/>每个节点一开始都是同一种颜色。<bookmark mark='b'/>每一轮，一个节点的新颜色，是它的旧颜色加上邻居们的颜色的"
        "一个名字。这里，有三个邻居的碳原子先分了出来。<bookmark mark='c'/>然后是它们的邻居分出来，依此类推，直到不再变化。如果两个图"
        "最后某种颜色的数量不同，它们肯定不是同一个图。<bookmark mark='d'/>十氢萘和联环戊烷，跑了{rounds - 1}轮：{verdict}。可一个是两个"
        "共用一条边的六元环，另一个是由一根键连起来的两个五元环。这个检验对这个差别视而不见。",

    'At every round the two molecules have exactly the same colours':
        '每一轮，两个分子的颜色种类和数量都完全相同，所以检验说它们可能是同一个图',

    'The colour counts differ, so the test tells them apart':
        '颜色的数量不同，所以检验能把它们分开',

    'And no message-passing network can do better.':
        "而且没有哪个消息传递网络能做得更好。定理来自许凯宇等人，以及克里斯托弗·莫里斯等人，2019年：如果颜色细化在t轮之后分不开两个节点，"
        "那么任何消息传递网络在t层之后也分不开它们。<bookmark mark='a'/>用归纳法。一开始，一切都相等。<bookmark mark='b'/>如果两个节点在"
        "下一轮得到同样的颜色，那么它们原来的颜色相同，邻居颜色的多重集也相同。<bookmark mark='c'/>根据归纳假设，它们原来的状态相同，"
        "邻居状态的多重集也相同。<bookmark mark='d'/>一层网络恰好只用这些来计算新状态，所以新状态也相同。<bookmark mark='e'/>而且这个上界"
        "是能达到的：先对邻居求和、再接一个MLP，也就是图同构网络，能分开颜色细化能分开的每一对图。",

    'f"Why a sum? Because the aggregation must not lose information':
        "为什么要求和？因为聚合不能丢掉邻居多重集的信息。<bookmark mark='a'/>一个节点的邻居是a、a、b、b，另一个节点的邻居是a、b："
        "它们的平均一样，最大值也一样，只有和不一样。<bookmark mark='b'/>后果在这里，计算所得：让随机图的每个节点从相同的特征出发，让一个"
        "一层的网络算出每个节点的度。用求和，误差是{sum_rm:.2f}。<bookmark mark='c'/>用平均或最大值，分别是{mean_rm:.2f}和{max_rm:.2f}："
        "在它们看来每个节点都一样，所以只能猜平均度数，误差就是度数本身的离散程度，{sd:.2f}。",

    'f"Now make a network fail on purpose.':
        "现在故意让一个网络失败。取{n}个节点的、由若干个环组成的图，问：里面有没有三角形？<bookmark mark='a'/>在颜色细化看来，这些图"
        "全都一样：每个节点都有两个邻居，邻居又各有两个邻居，一直如此。所以根据定理，任何消息传递网络对它们都必须给出同一个答案。"
        "<bookmark mark='b'/>{gin_line}<bookmark mark='c'/>{rni_line}<bookmark mark='d'/>一个把特征放在节点对上、并通过每个第三个节点"
        "更新每一对的网络，能直接看见三角形：{100 * np.mean(acc['pair']):.1f}%。记住这个构造：一对节点，通过第三个节点来更新。它是"
        "AlphaFold的核心。",

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

    'f"How bad is it? On random graphs, hardly at all:':
        "这有多严重？在随机图上几乎不成问题：颜色细化分开了{rp}对不同的图中的{rs}对。<bookmark mark='a'/>在每个节点都有三个邻居的图上，"
        "{gp}对里它分开了{gsep}对。<bookmark mark='b'/>各种补救办法都是加进邻居求和造不出来的信息：给节点的k元组上色，而不是给单个节点，"
        "代价按n的k次方增长；数一数三角形这样的小模式；给节点位置，随机的或者谱的；或者让注意力去看每一对节点。<bookmark mark='c'/>顺便"
        "一提，判断两个图是否相同，至今不知道是容易还是困难；拉斯洛·巴拜在2016年证明了，它最多需要拟多项式时间。",

    # ------------------------------------------------------------------ Depth
    'Chapter six. Deep graph networks.':
        '第6章。深层图网络。',

    'Graph networks are usually shallow':
        "图网络通常很浅，两到四层，而图像网络能有好几百层。这里是原因之一。把图卷积的权重去掉，它就是对邻居求平均，一遍又一遍。"
        "<bookmark mark='a'/>这个平均矩阵是对称的，所以它有一组正交归一的特征向量，特征值最大是1。<bookmark mark='b'/>用它作用k次，就把"
        "每个特征值变成k次方。<bookmark mark='c'/>除了第一项，其他各项都会消失，而第一项在每个节点上都是同一个模式，只是按度的平方根"
        "缩放。<bookmark mark='d'/>趋近的速度是几何级数的，速率是第二大特征值的k次方。<bookmark mark='e'/>每个节点最后都有同样的特征："
        "过平滑。李其迈等人在2018年描述了它，大野健太和铃木大慈证明了带权重和ReLU的网络也是如此。",

    'f"Here it is on our three-community graph.':
        "这是它在我们三社群图上的样子。一个衡量邻居之间差别有多大的量，狄利克雷能量，每做一轮平均就记一次。<bookmark mark='a'/>在这个"
        "对数坐标上，它沿直线下降，十六轮下降了{mags:.0f}个数量级，正是第二大特征值{lam2:.3f}预言的速率。<bookmark mark='b'/>换成图像："
        "节点的特征按社群上色，一开始是噪声；几轮平均把社群分开了，这就是两层网络有用的原因；而很多轮之后，一切都缩成了一个点。",

    'f"Now with weights and training.':
        "现在加上权重和训练。同样的图任务，深度从两层到六十四层，每种三个种子。<bookmark mark='a'/>{best_txt}；{col_txt}。<bookmark "
        "mark='b'/>{res_txt}：跳跃连接让每个节点自己的信息不被平均掉，这正是让图像网络变深的同一个办法，第9部分讲过。<bookmark mark='c'/>"
        "有了权重之后，坍缩的一部分也是优化问题：梯度必须反向穿过所有那些平均。",

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
        "当答案依赖远处的节点时，第二个问题就出现了。<bookmark mark='a'/>L跳以内的节点数可以指数增长，<bookmark mark='b'/>可它们所有的"
        "信息都得一层一层地挤进需要它的那个节点上一个固定大小的向量里。<bookmark mark='c'/>乌里·阿隆和埃兰·亚哈夫在2021年把这叫作"
        "过挤压；杰克·托平等人把它追溯到瓶颈，也就是曲率为负的边。<bookmark mark='d'/>补救办法：重新连图，加入能看见一切的节点，或者让"
        "注意力直接触及每个节点。",

    'Attention is the third idea.':
        "注意力是第三个想法。<bookmark mark='a'/>一个节点不再平等地加总它的邻居，而是给它们加权：在佩塔尔·韦利奇科维奇2018年的图注意力"
        "网络里，权重是一个学出来的分数在邻居上的softmax。<bookmark mark='b'/>沙凯德·布罗迪、乌里·阿隆和埃兰·亚哈夫注意到，原来的分数"
        "对每个节点给邻居排的顺序都一样，于是把非线性挪到里面，修正了它。<bookmark mark='c'/>而第13部分的Transformer恰好就是这个：完全图上"
        "的注意力，每个词元都是其他每个词元的邻居。<bookmark mark='d'/>图Transformer再把图的结构作为编码加回来，告诉网络每个节点在哪里。"
        "<bookmark mark='e'/>而AlphaFold核心的那个网络，是在残基对上做注意力，并由三角形来偏置：上一章那个节点对网络的成年版。",

    'So deep graph networks fight two forces:':
        "所以深层图网络要对抗两股力量：反复平均会抹掉节点之间的差别，而瓶颈会挤压远处的信息。跳跃连接和注意力能顶回去。"
        "接下来：空间本身的对称性。",

    # ------------------------------------------------------------------ Rotations
    'Chapter seven. Networks that turn with the molecule.':
        '第7章。随分子一起转动的网络。',

    'For molecules and materials the symmetry is':
        "对分子和材料来说，对称性是空间刚体运动的群，E(3)：转动、反射和平移。<bookmark mark='a'/>分子的能量在所有这些变换下都不变。"
        "<bookmark mark='b'/>对位置求导：链式法则带出了R的转置。<bookmark mark='c'/>两边乘上R，<bookmark mark='d'/>而力是能量梯度的负值，"
        "所以力随分子一起转动：它是等变的。能量的不变模型通过求导就免费得到了等变的力，大多数机器学习势函数正是这样计算力的。",

    'How do you build that into a network?':
        "怎样把它做进网络里？最简单的答案是维克托·加西亚·萨托拉斯、埃米尔·霍格布姆和马克斯·韦林2021年提出的E(n)等变图网络。每个原子有"
        "特征h和位置x。<bookmark mark='a'/>两个原子之间的消息只看它们的特征和它们之间距离的平方，别的都不看：转动或移动分子，不会改变任何"
        "消息。<bookmark mark='b'/>然后每个原子沿着位置之差移动，用学出来的标量加权。<bookmark mark='c'/>它的特征由加起来的消息更新，所以"
        "保持不变。<bookmark mark='d'/>现在把输入转一转、移一移。消息不变，位置之差被R转动，而平移在每个差里都抵消了，所以新位置就是旧"
        "位置转过、移过的结果。等变性，一行一行地证明出来。<bookmark mark='e'/>四年前的SchNet只用距离，得到的是不变的能量。",

    'f"EGNN carries two kinds of information:':
        "EGNN携带两种信息：标量，它不转；位置，它像向量一样转。更丰富的模型携带更多。<bookmark mark='a'/>球面上的任何函数都能用球谐函数"
        "展开，有0阶、1阶、2阶，以及更高阶。<bookmark mark='b'/>这里是计算出来的结果：一次转动对2阶以内的九个球谐函数做了什么：它只在"
        "同一阶之内混合它们，分成1、3、5三块；块外面的元素，小数点后{dp}位都是零。<bookmark mark='c'/>所以网络可以为每一阶保留特征，"
        "每一阶用自己的那一块来转，再用克莱布什–戈尔丹规则把两个特征组合成新的阶，这和量子力学里角动量相加的规则是同一套。<bookmark "
        "mark='d'/>这就是张量场网络的设计，也是NequIP和MACE的设计，它们是当今最精确的机器学习力场之一。",

    'f"Does it pay? Our five-body system again:':
        "这值得吗？还是我们的五体系统：已知粒子的位置和运动，预测它们在时刻1的位置。四个网络，同样的三千步训练，训练系统从一百个到"
        "{sizes[-1]:,}个，每种三个种子。<bookmark mark='a'/>虚线是最简单的猜测：每个粒子都沿直线继续走。<bookmark mark='b'/>{mlp_txt}。"
        "{aug_txt}：{m['mlp_aug']:.3f}。<bookmark mark='c'/>直接用原始坐标的消息传递：{m['gnn']:.3f}。<bookmark mark='d'/>EGNN："
        "{m['egnn']:.4f}，{ratio_txt}。{cross}。",

    'With only a hundred, EGNN already beats every other network':
        '只用一百个，EGNN就已经胜过了用三十倍数据训练的所有其他网络',

    "f'With a hundred systems its error is":
        '用一百个系统，它的误差是{eg_small:.4f}；其他网络里最好的那个，要用全部{sizes[-1]:,}个系统才达到{best_other_big:.4f}',

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
        "这就是支持等变性的理由：数据里不需要花任何力气去教网络，转过的分子还是同一个分子。蛋白质也是分子，本部分剩下的内容，讲的是这些"
        "想法把科学带到了哪里，先从所有分子里最难的那一种讲起。",

    # ------------------------------------------------------------------ Folding
    'Chapter eight. The protein-folding problem.':
        '第8章。蛋白质折叠问题。',

    'A protein is a chain of amino acids':
        "蛋白质是一条由氨基酸连成的链，氨基酸有二十种，由一个基因写出。<bookmark mark='a'/>在水里，这条链折叠成一个精确的形状，而形状"
        "决定了它做什么：切断另一个分子，抓住一个病毒，在细胞膜上打开一个通道。<bookmark mark='b'/>1958年，约翰·肯德鲁看到了第一个："
        "肌红蛋白，他让X射线穿过它的晶体，这让他和马克斯·佩鲁茨获得了诺贝尔奖。<bookmark mark='c'/>蛋白质数据库在1971年开张时有7个结构；"
        "<bookmark mark='d'/>今天它收录了超过25万个。<bookmark mark='e'/>可我们知道几十亿个蛋白质的序列，而测定一个结构可能要好几年。"
        "于是就有了这个问题：从序列读出形状。",

    'f"Two facts frame the problem.':
        "两个事实框定了这个问题。<bookmark mark='a'/>1961年，克里斯蒂安·安芬森用尿素让一种酶，核糖核酸酶，展开；把尿素洗掉之后，这条链"
        "自己折了回去，又能工作了。所以，形状的信息全在序列里。<bookmark mark='b'/>但在1969年，赛勒斯·列文索尔指出，这条链不可能靠把形状"
        "全试一遍来找到它。<bookmark mark='c'/>一条{N}个残基的链，每个关节只给三种选择：那就大约是10的{int(math.log10(conf))}次方种形状。"
        "<bookmark mark='d'/>每秒试十万亿种，要花10的{int(math.log10(years))}次方年，而宇宙的年龄大约是10的10次方年。<bookmark mark='e'/>"
        "可蛋白质折叠只需要几微秒到几秒。大自然不是在盲目搜索，后来证明，计算机也不该盲目搜索。",

    'In 1994 John Moult and Krzysztof Fidelis turned the problem into a contest':
        "1994年，约翰·莫尔特和克日什托夫·菲德利斯把这个问题变成了一场比赛，CASP：每两年一次，预测那些已经测定但还没发表的结构。"
        "<bookmark mark='a'/>预测用GDT打分，大致是落在真实位置几埃以内的残基所占的百分比。<bookmark mark='b'/>二十年里进展缓慢。后来，"
        "进化提供了一条线索。<bookmark mark='c'/>把许多物种里同一个蛋白质的序列对齐：如果两个位置在折叠后挨在一起，一个位置的突变常常会"
        "被另一个位置补偿，所以这两列会一起变化。2011年前后，统计方法学会了从这种比对里读出接触。<bookmark mark='d'/>而在2018年的CASP13，"
        "DeepMind的第一代AlphaFold用一个深度网络，为每一对残基预测它们距离的直方图，再用梯度下降把一条链折成与之相符的形状。在43个"
        "最难的结构域里，它在24个上达到了高精度，第二名只有14个。",

    'Why distances? Because a full table of distances fixes a shape.':
        "为什么是距离？因为一张完整的距离表就能确定一个形状。这是我们那个三螺旋束的五十二个原子之间的所有距离。<bookmark mark='a'/>"
        "把它们平方，再做中心化，<bookmark mark='b'/>就得到原子位置之间的点积矩阵，因为距离的平方等于两个长度的平方和减去两倍的点积。"
        "<bookmark mark='c'/>它的特征向量把坐标还原出来：经典多维尺度分析，1952年。恰好有三个非零特征值，空间的每一维一个，<bookmark "
        "mark='d'/>重建出来的链和原来的一致，误差只是舍入误差。<bookmark mark='e'/>但只能精确到镜像：一个结构和它的镜像，所有距离完全"
        "相同。蛋白质在这一点上并不对称。它的螺旋都是右手螺旋。",

    'f"AlphaFold 1 had only predicted distances':
        "AlphaFold 1手里只有预测的距离，带噪声，而且只有它确信离得近的那些对。那我们就照它的做法来：只保留小于{f['cut']:.0f}埃的对，"
        "占{100 * frac:.0f}%，加上{f['noise']:.0f}埃的噪声，从一团随机乱线出发，用梯度下降移动原子，直到它们的距离相符。<bookmark "
        "mark='a'/>看它折起来。<bookmark mark='b'/>从{n}个随机起点出发，{verdict}。<bookmark mark='c'/>一个只预测距离的模型，或者任何"
        "在反射下不变的东西，都没法确定是哪一个。AlphaFold 2需要一种能分清左手和右手的表示。",

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
        "AlphaFold 2是约翰·江珀等人在2020年代表DeepMind参加CASP14的系统，它分两个阶段工作。<bookmark mark='a'/>它从序列出发，在基因"
        "数据库里搜索相关序列，排成一个多序列比对，再加上相似蛋白质的已知结构。<bookmark mark='b'/>第一阶段是Evoformer，有四十八个模块"
        "那么深，对这些信息进行推理，<bookmark mark='c'/>第二阶段是结构模块，把结果变成每个原子的坐标，并给每个残基一个置信度。"
        "<bookmark mark='d'/>然后整个系统再跑一遍，输入它自己的输出。<bookmark mark='e'/>Evoformer维护两种表示：一种给比对，每条序列的"
        "每个残基一个向量；一种给残基对，每一对残基一个向量，这是AlphaFold 1距离直方图的、学出来的后代。",

    'Each Evoformer block passes information both ways between them.':
        "每个Evoformer模块都在这两者之间双向传递信息。<bookmark mark='a'/>沿着每条序列，残基彼此做注意力，而残基对的表示会偏置这个注意力："
        "网络对残基对的看法，影响它怎么读序列。<bookmark mark='b'/>沿着每一列，同一个位置在不同物种之间做注意力。<bookmark mark='c'/>"
        "反过来，比对里两列的外积，在所有序列上平均，更新这两个位置组成的那一对：这是共进化的学习版本，两列一起变化。",

    'The new idea is in how the pairs update each other.':
        "新想法在于残基对怎样互相更新。把残基对的表示看成是对每两个残基之间距离的猜测。<bookmark mark='a'/>这些猜测不可能互相独立："
        "对任何第三个残基k，从i到j的距离最多是从i到k的距离加上从k到j的距离。<bookmark mark='b'/>所以Evoformer用每一对i、j所在的每个"
        "三角形的另外两条边来更新它：对k求和，把i k和j k这两对的乘积加起来，再加门控，这叫“外向”更新。<bookmark mark='c'/>指向内的边"
        "也同样处理一遍。<bookmark mark='d'/>在残基对矩阵里，元素i j收集第i行和第j行，一个位置一个位置地对应起来。<bookmark mark='e'/>"
        "三角注意力用注意力权重做同样的事。<bookmark mark='f'/>这是第5章的教训在实际中的应用：一个在节点对上、通过第三个节点更新的网络，"
        "能看见单节点消息传递看不见的结构。",

    'f"Does it work? A small test, computed here.':
        "它管用吗？这里计算一个小测试。随机的、像蛋白质一样的链，{p['n']}个残基；模型看到四分之一残基对的距离，带噪声，要把所有的都填出来，"
        "这代替了比对告诉AlphaFold的信息。<bookmark mark='a'/>两个同样大小、同样训练的模型：一个单独更新每一对；另一个用三角更新。"
        "<bookmark mark='b'/>只根据两个残基在链上隔多远来猜缺失的距离，误差是{sep:.1f}埃。单独更新每一对得到{mp:.1f}：它没法做得更好，"
        "因为它从不看别的残基对。<bookmark mark='c'/>{verdict}，{vtxt}。",

    "f'Triangle updates cut it to":
        '三角更新把它降到{mt:.1f}，小了{mp / mt:.1f}倍',

    'f"Triangle updates don\'t help here':
        '三角更新在这里没有帮助：{mt:.1f}',

    "f'and their guesses break the triangle inequality":
        "而且它的猜测违反三角不等式的次数少了{viol['pairwise'] / max(viol['triangle'], 1e-09):.0f}倍",

    'though their guesses break the triangle inequality no less often':
        '不过它的猜测违反三角不等式的次数并没有更少',

    'And at CASP14, in 2020, it worked.':
        "而在2020年的CASP14上，它成功了。<bookmark mark='a'/>AlphaFold 2在所有目标上的中位数得分是92.4 GDT，在最难的目标上是87.0，而"
        "大约九十分，按非正式的看法，就能和实验相比了。<bookmark mark='b'/>它的主链误差中位数不到1埃，0.96，第二名是2.8；作为对比，"
        "一个碳原子的直径大约是1.5埃。<bookmark mark='c'/>“我们在这个问题上卡了将近五十年：蛋白质是怎么折叠起来的，”约翰·莫尔特说；"
        "CASP的组织者认定AlphaFold 2对单条蛋白质链给出了一个解答。",

    "So the Evoformer's two ideas:":
        "所以Evoformer的两个想法是：让比对和残基对互相提供信息，用三角形让残基对保持一致。剩下的，是把残基对变成一个结构，而且不能"
        "弄丢左和右的区别。",

    # ------------------------------------------------------------------ Structure
    'Chapter ten. AlphaFold 2: frames, FAPE and recycling.':
        '第10章。AlphaFold 2：坐标系、FAPE与循环。',

    'The structure module treats each residue as a rigid body:':
        "结构模块把每个残基当作一个刚体：由三个主链原子组成的小三角形，有它自己的坐标系，一个旋转加一个位置。<bookmark mark='a'/>它一开始"
        "把所有坐标系都堆在原点，一团“残基气体”，然后移动它们。<bookmark mark='b'/>它的注意力叫不变点注意力：在每个残基自己的坐标系里放置"
        "一些学出来的点，按这些点在空间里靠得多近来给残基对打分。<bookmark mark='c'/>整个蛋白质做一次刚体运动，每个点都以同样方式移动，"
        "所以这些距离、以及注意力，都不会变。<bookmark mark='d'/>然后每一层用一个以该坐标系自身坐标表达的更新，轻轻推动每个坐标系，所以"
        "更新会随蛋白质一起转动：又一次，等变性被做了进去。",

    'What should the network be trained to minimize?':
        "网络应该被训练去最小化什么？AlphaFold 2的答案是坐标系对齐点误差，FAPE。<bookmark mark='a'/>站在残基i的坐标系里看原子j：这就"
        "给出了残基i眼中原子j的位置。<bookmark mark='b'/>对每个原子、从每个坐标系都这样看，在预测里和真实结构里都看，把差别平均起来，每个"
        "差别都截断在十埃，免得少数几个离谱的原子主导结果。<bookmark mark='c'/>把整个结构做一次刚体运动，这个运动就抵消了：FAPE不在乎"
        "蛋白质在哪里、朝哪个方向。<bookmark mark='d'/>但坐标系是用右手法则从三个原子构造出来的。镜像不是刚体运动，所以FAPE能看出来。",

    'f"Here is the difference, measured on our bundle and its reflection.':
        "差别在这里，在我们的螺旋束和它的镜像上测量。<bookmark mark='a'/>每个距离都一样，所以距离的误差是{dm:.2f}。<bookmark mark='b'/>"
        "可FAPE是{fm:.2f}，比把每个原子随机移动整整1埃还要差，那样的代价是{f['fape_noisy']:.2f}。<bookmark mark='c'/>而第8章用梯度下降"
        "折出来的那些结构，光靠距离分不开，现在被干净地分开了：落在真实折叠上的得分{gf:.2f}，落在镜像上的得分{bf:.2f}。",

    'f"The last trick is recycling:':
        "最后一招是循环：把整个网络再跑一遍，输入它自己上一次的输出，这样第一个粗糙的结构就能让网络把比对读得更清楚。<bookmark "
        "mark='a'/>训练时，跑几遍是随机的，梯度只流过最后一遍，所以每多跑一遍都不多占内存。<bookmark mark='b'/>我们把它加到了第9章的三角"
        "模型上。{verdict}，{vs}。",

    "f'A second pass cuts the error from":
        '第二遍把误差从{m[0]:.2f}埃降到{m[1]:.2f}埃；最好的是跑{best}遍，{m.min():.2f}',

    "f'In our toy the extra passes change little":
        '在我们的玩具里，多跑几遍变化不大：从{m[0]:.2f}埃到最好的{m.min():.2f}埃',

    'and with four passes it beats the same network trained without recycling':
        '而且跑四遍时，它胜过了不用循环训练的同一个网络',

    'f"though even with four passes it doesn\'t beat':
        '不过即使跑四遍，它也没有胜过不用循环训练的同一个网络，{one:.2f}',

    'In July 2021 DeepMind published AlphaFold 2 with its code;':
        "2021年7月，DeepMind发表了AlphaFold 2，并公开了代码；同一个月，大卫·贝克的团队发表了RoseTTAFold，一个基于同样洞见的三轨网络。"
        "<bookmark mark='a'/>DeepMind和EMBL的欧洲生物信息研究所一起发布了预测结构，先是人类蛋白质组和另外二十种生物，然后在2022年发布了"
        "两亿多个蛋白质的结构，几乎覆盖了所有已知序列。<bookmark mark='b'/>每个预测都带着网络自己的置信度，一个残基一个残基地给出，叫pLDDT。"
        "<bookmark mark='c'/>两年后，诺贝尔奖来了。<bookmark mark='d'/>但AlphaFold 2对每条链只预测一个静止的形状，对蛋白质怎样运动、"
        "怎样结合DNA、怎样夹住一个药物分子，说得很少。那是下一步。",

    'So: residues as rigid frames,':
        "所以：残基是刚性的坐标系，由看不见蛋白质怎么转的注意力来移动；一个不在乎刚体运动、却在乎反射的损失；还有一个会读自己的答案、"
        "再试一次的网络。",

    # ------------------------------------------------------------------ AF3
    'Chapter eleven. AlphaFold 3: diffusion over atoms.':
        '第11章。AlphaFold 3：原子上的扩散。',

    'In May 2024 Google DeepMind and Isomorphic Labs published AlphaFold 3.':
        "2024年5月，谷歌DeepMind和Isomorphic Labs发表了AlphaFold 3。<bookmark mark='a'/>细胞结构里能找到的几乎任何东西它都能处理："
        "蛋白质链、DNA和RNA、类药小分子、离子、化学修饰过的残基，并预测它们怎样待在一起。<bookmark mark='b'/>比对只经过四个模块的处理，"
        "<bookmark mark='c'/>主干是Pairformer，也就是Evoformer的残基对部分，四十八个模块，三角更新原样保留。<bookmark mark='d'/>大的改变"
        "在最后。结构模块，连同它的坐标系和不变注意力，都没有了。取而代之的是一个扩散模型，直接写出每个原子的坐标。",

    "Diffusion is Part 21's idea, applied to atoms.":
        "扩散是第21部分的想法，用在了原子上。<bookmark mark='a'/>给一个结构的坐标加噪声，从轻微到纯噪声的每个水平都加，训练一个网络去"
        "除掉噪声。然后从纯噪声出发，一步一步除掉它。这是我们一个小模型的样本，从噪声变成一条链。<bookmark mark='b'/>惊奇之处来了。在花了"
        "四章把对称性做进网络之后，AlphaFold 3的论文明明白白地说，架构里不需要对转动和平移的不变性或等变性。<bookmark mark='c'/>取而代之的"
        "是，每个训练结构都先中心化，再随机转动：数据增强，也就是第2章说的那条便宜的路。<bookmark mark='d'/>生成模型还可能在根本没有"
        "结构的地方，比如松软的区域，编造出结构；AlphaFold 3也用AlphaFold-Multimer的预测来训练，这教会了它把这些区域留成松散伸展的链。",

    'f"So is equivariance worth it, for a generator?':
        "那么，对生成模型来说，等变性值得吗？我们可以在一个玩具上检验这个问题。平面上四千条紧凑的链，每条十二个原子，键长为1。"
        "<bookmark mark='a'/>两个去噪器，训练步数相同：一个对转动等变，像EGNN；另一个是普通MLP，每条链都随机转过之后才给它看，就像"
        "AlphaFold 3的网络那样。<bookmark mark='b'/>它们的样本。<bookmark mark='c'/>键长：等变模型平均偏差{e['bond']:.3f}，普通模型"
        "{m['bond']:.3f}。碰撞，也就是两个原子叠在一起：{100 * e['clash']:.1f}%的链对{100 * m['clash']:.1f}%。{verdict}，{nn_line}。"
        "<bookmark mark='d'/>在AlphaFold 3的规模上，用整个蛋白质数据库和一个大网络训练，DeepMind选择了喂给转过副本的普通网络：用数据和"
        "算力代替内置的对称性。",

    'and neither simply copies its training chains':
        '而且两者都没有只是照抄训练链',

    'though the samples sit closer to training chains than real new chains do':
        '不过样本离训练链比真正的新链离得更近',

    'The equivariant denoiser draws better chains on both counts':
        '等变去噪器在两项上都画出了更好的链',

    'The plain network, trained on turned copies, does as well or better on both counts':
        '用转过副本训练的普通网络，在两项上都一样好或者更好',

    'On drug-like molecules bound to proteins':
        "对于结合在蛋白质上的类药分子，DeepMind报告说AlphaFold 3比最好的传统对接方法精确百分之五十，在蛋白质复合物和抗体上也胜过"
        "前代。<bookmark mark='a'/>它先以一个免费服务器的形式提供给非商业用途，2024年11月又向学术界开放了代码和权重。<bookmark mark='b'/>"
        "几个月之内，开放的复现就出现了：Chai-1、Boltz-1、Protenix。<bookmark mark='c'/>2025年，Boltz-2加上了对分子结合强度的预测，"
        "OpenFold联盟预览了一个完全开放的模型。<bookmark mark='d'/>2026年2月，Isomorphic Labs报告了一个专有的后继系统，在新的抗体–抗原对"
        "上，做出高精度预测的比例是AlphaFold 3的2.3倍，这是按他们自己的基准测出来的。",

    'AlphaFold 3 kept the pair stack,':
        "AlphaFold 3保留了残基对的部分，把几何交给了扩散，让网络从转过的副本里学会对称性。预测也可以倒过来：从你想要的形状，到一个能"
        "折成它的蛋白质。",

    # ------------------------------------------------------------------ Design
    'Chapter twelve. Designing proteins.':
        '第12章。设计蛋白质。',

    'Structure prediction goes from a sequence to a shape.':
        "结构预测是从序列到形状。<bookmark mark='a'/>设计走的是反方向：从你想要的形状出发，比如一个能结合病毒的结合子、一个催化剂的支架，"
        "找到一条能折成它的序列。<bookmark mark='b'/>这是大卫·贝克毕生的工作，也是2024年诺贝尔奖的另一半。2003年，他的团队设计出了Top7，"
        "一种自然界从未见过的折叠，用的是Rosetta能量函数来搜索序列；他们做出来的蛋白质按设计折叠了。二十年来，这样的设计需要专家投入"
        "大量精力，而且大多数尝试都失败了。",

    'Deep learning changed both halves of design,':
        "深度学习改变了设计的两半，先从序列说起。<bookmark mark='a'/>2022年，贝克实验室的尤斯图斯·道帕拉斯等人做出了ProteinMPNN：它把"
        "主链读成一个图，每个残基与空间中离它最近的邻居相连，<bookmark mark='b'/>传递由距离构成的消息，所以答案不可能依赖主链怎么转，"
        "<bookmark mark='c'/>然后一次写一个氨基酸，按随机顺序，每个都以已经写好的那些为条件。<bookmark mark='d'/>给它天然蛋白质的主链，"
        "它能还原出52.4%的天然氨基酸，Rosetta是32.9%，而且它设计的序列按预期折叠的次数要多得多。",

    'Then the backbone. In 2023 Joseph Watson and colleagues':
        "然后是主链。2023年，约瑟夫·沃森等人发表了RFdiffusion。<bookmark mark='a'/>他们拿来结构预测器RoseTTAFold，微调它去除残基坐标系"
        "上的噪声：位置上加高斯噪声，朝向上做随机转动，从噪声到一条主链走两百步。可以让它把一个功能基序保持在原位、结合一个靶标，或者"
        "满足某种对称性。<bookmark mark='b'/>设计流程变成了：扩散出一条主链；让ProteinMPNN为它写八条序列；<bookmark mark='c'/>只保留"
        "AlphaFold 2能折回到设计上的序列，误差在两埃以内、而且有把握；<bookmark mark='d'/>然后才进实验室。<bookmark mark='e'/>对于结合子，"
        "百分之十九的设计在实验中成功了，大约是早先基于Rosetta方法的一百倍；一个流感结合子测出来的结构，离它的设计只有0.63埃。",

    'f"Our toy denoiser from the last chapter shows the idea in miniature.':
        "上一章的玩具去噪器能把这个想法缩小了展示出来。这是它的训练：损失，以及在每个检查点用同样八个噪声种子抽出的样本。<bookmark "
        "mark='a'/>一开始是乱线；然后是键长正确的链；然后是像训练集那样的紧凑折叠。<bookmark mark='b'/>而且它们是新的：样本的中位数离"
        "最近的训练链{nn_s:.2f}，而它从没见过的真实链是{nn_h:.2f}，{novel}。",

    'about as far from their nearest training chain as genuinely new chains are':
        '和真正的新链离最近训练链差不多远',

    'closer to training chains than genuinely new chains are, a sign of some copying':
        '比真正的新链离训练链更近，这说明有一些照抄',

    'Since then the field has moved fast.':
        "从那以后，这个领域发展得很快。<bookmark mark='a'/>2024年，谷歌DeepMind的AlphaProteo为医学上重要的靶标设计了结合子，<bookmark "
        "mark='b'/>BindCraft通过在AlphaFold 2本身里做梯度下降来设计结合子，<bookmark mark='c'/>EvolutionaryScale的ESM3，一个覆盖序列、"
        "结构和功能的语言模型，写出了一个和任何天然蛋白都相差很远的新荧光蛋白。<bookmark mark='d'/>2025年，贝克实验室的RFdiffusion3在单个"
        "原子的层面上做设计，包括DNA周围和酶的内部，<bookmark mark='e'/>BoltzGen也作为一个开放的选择出现了。<bookmark mark='f'/>这么强大的"
        "工具可能被滥用；2024年，这个领域的许多研究者签署了负责任生物设计的承诺，包括对DNA合成进行筛查。",

    'Design, in one line:':
        "一句话说设计：扩散出一条主链，为它写一条序列，检查这条序列能不能折回去，然后才把它做出来。现在从分子走向整个星球。",
})

ZH.update({
    # ------------------------------------------------------------------ Weather
    'Chapter thirteen. Weather on a mesh.':
        '第13章。网格上的天气。',

    'Weather forecasting became physics in 1904':
        "1904年，天气预报变成了物理学：维尔赫姆·皮耶克尼斯把它描述成一个初值问题，测出此刻的大气，再把流体方程向前推进。<bookmark "
        "mark='a'/>刘易斯·弗赖·理查森在第一次世界大战期间试着用手算：为欧洲的两个点做一次六小时预报，算了大约六个星期，结果错了一百四十五"
        "百帕。他梦想有一个大厅，六万四千人步调一致地计算天气。<bookmark mark='b'/>1950年，朱尔·查尼、拉格纳·弗约托夫特和约翰·冯·诺依曼"
        "在ENIAC上做出了最早的几次预报：二十四小时的天气，大约要算二十四小时。<bookmark mark='c'/>欧洲中期天气预报中心在1979年发布了"
        "第一批预报；此后几十年里，更好的物理、更好的数据和更大的计算机，大约每十年让有用的预报时效多出一天。",

    'Machine learning came to this in the 2020s':
        "到了2020年代，机器学习来到了这里，用ERA5训练，那是ECMWF对1940年以来全球天气的重建。2023年，谷歌DeepMind的雷米·拉姆等人发表了"
        "GraphCast。<bookmark mark='a'/>大气存储在一个经纬度网格上，一百万个点，每个点二百二十七个数：风、温度、湿度等等，分布在三十七个"
        "高度上。但这样的网格在两极附近点挤得太密，所以GraphCast改在一个网格网上工作：<bookmark mark='b'/>一个正二十面体，细分六次，保留"
        "每一层的边，于是有的边很短，有的边横跨大陆，一条消息几步就能穿过整个星球。这是我们自己的小版本，在一个正方形上。<bookmark "
        "mark='c'/>把格点编码到网格网上，传递十六次消息，再解码回格点：由最近的两个状态得到下一个状态，六小时之后。<bookmark mark='d'/>"
        "它用三十九年的ERA5，在三十二个TPU上训练了四个星期，几分钟不到就能做出一次十天预报，并在1380个检验目标中的百分之九十上胜过了ECMWF"
        "旗舰的确定性预报。",

    'Ours is a toy atmosphere:':
        "我们的是一个玩具大气：一个二维流体，在一个首尾相接的正方形上，被一个固定的图样搅动，又被摩擦减弱，于是涡旋生成、漂移、合并、"
        "消亡。它是混沌的，就像天气。<bookmark mark='a'/>一个小的编码–处理–解码网络在刚才那个网格网上，从三十二次模拟中一步一步地学习，"
        "然后自己往前推，把每次预测再喂回去。<bookmark mark='b'/>上面一行是真实情况；下面一行是我们的网络，从同一个起点出发。有一段时间"
        "两者一致；然后它们渐行渐远。",

    '"Scored over eight new runs: the error, step by step.':
        "在八次新的模拟上打分：误差，一步一步看。<bookmark mark='a'/>{s1}。<bookmark mark='b'/>{s2}，{s3}。<bookmark mark='c'/>{s4}。"
        "GraphCast训练时最多展开十二步，正是为了这个原因：从自己逐渐偏离的预测里学习。",

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

    "In our toy the long edges don't help over the first ten steps":
        '在我们的玩具里，长边在前十步里没有帮助',

    'There is a deeper problem.':
        "还有一个更深的问题。用平方误差训练的网络学会预测的是可能发生的情况的平均，而在很远的将来，许多种可能天气的平均是一片模糊。"
        "<bookmark mark='a'/>预报员用集合预报来应对不确定性：从略有不同的起点出发跑很多次。2024年，谷歌DeepMind的GenCast学会了用扩散来"
        "抽样下一个状态：五十个以上的样本组成一个集合，它在1320个目标中的97.2%上胜过了ECMWF自己的集合预报，提前一天半以上时是99.8%。"
        "<bookmark mark='b'/>然后，学出来的模型投入了日常业务。2025年2月25日，ECMWF让自己的人工智能预报系统投入业务运行，一个图网络编码器"
        "和解码器包着一个Transformer，那年7月又推出了它的集合版本；<bookmark mark='c'/>谷歌在11月发布了WeatherNext 2，12月，美国的NOAA"
        "让它的第一批AI全球模型投入运行。",

    'So the weather became a graph problem:':
        "于是天气变成了一个图问题：一个包住星球的网格网，几步就能穿过它的消息，以及为未来中无法知道的那一部分准备的扩散。接下来："
        "学会整个方程的网络。",

    # ------------------------------------------------------------------ Operators
    'Chapter fourteen. Neural operators.':
        '第14章。神经算子。',

    'Fields evolve by equations.':
        "场按方程演化。这是伯格斯方程，流体流动的一个一维漫画：一个波，在快的地方变陡，又被黏性抹平。<bookmark mark='a'/>从这个起点出发，"
        "一个时间单位之后，解是这个样子。<bookmark mark='b'/>求解器要走几千个小步才能到那里，而且每次被问都得重走一遍。一个网络可以学会从"
        "起点到终点的映射，但普通网络只处理一个固定长度的数列：用六十四个点训练，它就只认识六十四个点。<bookmark mark='c'/>我们想学的是"
        "算子本身，一个从函数到函数的映射，在任何分辨率上都能读。<bookmark mark='d'/>陈天平和陈宏在1995年证明了网络可以逼近算子；"
        "DeepONet和傅里叶神经算子都发表于2021年，让它变得实用。",

    'The Fourier neural operator, from Zongyi Li':
        "傅里叶神经算子出自李宗仪、阿妮玛·阿南德库马尔、安德鲁·斯图尔特等人，它从一个积分形式的网络层出发：每个点的新值，通过一个核"
        "kappa，混合了整个场。<bookmark mark='a'/>如果核只依赖于偏移量，这个积分就是一个卷积，而卷积定理把它变成傅里叶变换的乘积。"
        "<bookmark mark='b'/>所以直接学核的变换：给最低的那些频率各学一个复数权重，我们的模型里是十六个，其余的丢掉。<bookmark mark='c'/>"
        "由此得出三件事。权重属于频率，不属于格点，所以同一个网络能读任何细到足以容纳这些频率的网格。输入平移，输出也跟着平移。而每一层"
        "的代价比一次快速傅里叶变换多不了多少。",

    'f"We trained one on a thousand solutions':
        "我们用伯格斯方程的一千个解训练了一个，采样在{res}个点上，以一个伪谱求解器的答案为准。<bookmark mark='a'/>这是它对一个从没见过的"
        "起点的预测，在训练的各个检查点上，旁边是学习曲线。<bookmark mark='b'/>最后，它在留出的起点上的相对误差是{100 * e_fin:.1f}%。",

    'f"Now the test that matters.':
        "现在是真正要紧的测试。两个网络都只在六十四个点上训练过。从{R[0]}个点到{R[-1]:,}个点去读它们。<bookmark mark='a'/>{f_txt}。"
        "<bookmark mark='b'/>{c_txt}。<bookmark mark='c'/>{coarse}。FourCastNet是最早的学习型天气模型之一，2022年推出，它就建立在这种"
        "傅里叶层的一个变体上。",

    "f'The CNN, as good as":
        'CNN在它自己的网格上能达到{100 * ec[i_tr]:.1f}%，到最细的网格上变成了{100 * ec[-1]:.0f}%：它的核是五个格点宽，所以在更细的网格上'
        '只能看到线上更窄的一段',

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

    'f"A crystal is a pattern of atoms repeated in space':
        "晶体是原子在空间里重复排列的图样，它的对称性属于230种空间群之一，1891年就分类完了。哪些晶体存在？<bookmark mark='a'/>取两种元素"
        "A和B，以及它们所有可能的化合物，每个都有一个形成能，用密度泛函理论计算，每个要花好几个小时的计算机时间。<bookmark mark='b'/>"
        "如果没有其他化合物的混合物能量更低，这个化合物就是稳定的：也就是说，它落在这些点的下凸包上。<bookmark mark='c'/>在凸包上方的化合物"
        "宁愿分解成它的邻居，它高出凸包多少，说明它有多不稳定。在这个体系里，有{words_num(n_st)}个化合物在凸包上。",

    'In 2023 Amil Merchant, Ekin Dogus Cubuk and colleagues':
        "2023年，谷歌DeepMind的阿米尔·默钱特、埃金·多古斯·丘布克等人发表了GNoME，用于材料探索的图网络。<bookmark mark='a'/>它通过替换"
        "已知晶体里的元素、以及随机搜索，来生成候选晶体；<bookmark mark='b'/>图网络建立在原子间距离之上，因而与晶体怎么转无关，用来预测每个"
        "候选的能量；<bookmark mark='c'/>密度泛函理论检查最有希望的那些；<bookmark mark='d'/>每一次检查都变成下一轮的训练数据。<bookmark "
        "mark='e'/>此前，计算方法总共找到了大约四万八千种稳定晶体。GNoME报告了220万种相对已知一切都稳定的晶体，其中38.1万种在新的凸包上。"
        "它挑出来、被DFT确认的比例升到了百分之八十以上，而早先的工作只有百分之一左右；而且它的预测中有736种，已经被其他实验室独立地做出来了。",

    'f"We can run the flywheel on a made-up chemistry:':
        "我们可以在一个虚构的化学体系上转动这个飞轮：二十种虚构的元素，两两组合，九种配比，四种晶体类型，共{m['n_candidates']:,}个候选，"
        "它们的“DFT”能量是一个隐藏的公式，我们每次只揭开六十个。<bookmark mark='a'/>一开始知道其中百分之三。每一轮，用所有已知的数据训练"
        "一个小集成模型，预测其余的，检查相对于已知凸包看起来最稳定的六十个，再把它们加进来。命中，就是落在那个凸包下方的一次挑选。"
        "<bookmark mark='b'/>随机挑选的命中率是{100 * h_r.mean():.0f}%。<bookmark mark='c'/>代理模型的挑选在第一轮命中{100 * h_m[0]:.0f}%，"
        "{trend}。<bookmark mark='d'/>它的误差从{mae[0]:.3f}降到{mae[-1]:.3f}，{rounds}轮之后，它找到了{m['n_stable']}个真正稳定的化合物中的"
        "{F['model'][:, -1].mean():.0f}个，而随机挑选找到{F['random'][:, -1].mean():.0f}个。",

    "f'and it climbs as the surrogate learns":
        '而且随着代理模型的学习不断上升，从第一轮的{100 * h_m[0]:.0f}%升到最后一轮的{100 * h_m[-1]:.0f}%',

    "f'and it stays around":
        '而且一直在{100 * h_m.mean():.0f}%左右：在我们的玩具里，代理模型从一开始就不错',

    'The claims drew pushback from chemists.':
        "这些说法遭到了化学家的质疑。<bookmark mark='a'/>2024年，安东尼·奇塔姆和拉姆·谢沙德里随机抽查了GNoME的一批预测，发现很少有证据表明"
        "其中有同时称得上新颖、可信又有用的化合物；许多预测把原子排成整齐的有序结构，而真实晶体里这些原子是随机混排的；他们认为这些是晶态"
        "化合物，还算不上材料。<bookmark mark='b'/>同一年，批评者对一个机器人实验室报告四十一种新化合物所依据的X射线分析提出了异议；"
        "2026年1月，这篇论文被更正为五十七个目标中的三十六种化合物。<bookmark mark='c'/>工具在不断进步，适用于任何元素的通用学习势函数，"
        "能按指定性质提出晶体的生成模型，<bookmark mark='d'/>但教训留了下来：预测出来的晶体只是一个假设，把它做出来才是检验。",

    'In materials, then, the network is a cheap first opinion':
        "所以在材料领域，网络是一个便宜的初步意见，让昂贵的检查物尽其用。而在数学里，检查可以是完美的。",

    # ------------------------------------------------------------------ Proofs
    'Chapter sixteen. Geometry and proofs.':
        '第16章。几何与证明。',

    'Mathematics has something no other science has:':
        "数学有一样别的科学都没有的东西：一个骗不了的检查器。第28部分讲了强化学习怎样利用完美的检查器；这里讲检查器从哪里来。<bookmark "
        "mark='a'/>在Lean这样的证明助手里，定理和证明都是代码，一个小小的内核检查每一步推理：这一个说的是，n乘以n加1是偶数。<bookmark "
        "mark='b'/>计算机进入证明是在1976年，肯尼斯·阿佩尔和沃尔夫冈·哈肯检查了没有人能手工检查的大量情形，证明了四色定理；2005年，"
        "乔治·贡蒂埃对整个证明做了形式化检查。<bookmark mark='c'/>托马斯·黑尔斯对开普勒猜想的证明在2014年得到了形式化验证，<bookmark "
        "mark='d'/>2022年，Lean社区用大约十八个月，把达斯汀·克劳森和彼得·舒尔茨的一个困难的新定理形式化了。<bookmark mark='e'/>Lean的库"
        "Mathlib现在收录了大约二十九万条定理，这是任何机器证明者立足的基础。",

    'Olympiad geometry was the first olympiad subject to fall.':
        "奥赛几何是第一个被攻下的奥赛科目。2024年1月，谷歌DeepMind的陈天如、梁明唐等人发表了AlphaGeometry。<bookmark mark='a'/>没有人类"
        "证明可学，他们就自己造：随机的前提，一个推出所有后果的符号引擎，再从每个新事实回溯到它恰好需要的东西。一亿条带证明的定理。"
        "<bookmark mark='b'/>其中百分之九需要一个题目里从未提到的点，一条辅助构造，这是奥赛几何里有创造性的那一步；一个语言模型学会了"
        "提出这些点，其余的交给引擎。<bookmark mark='c'/>在三十道奥赛题上，它在规定时间内解出了二十五道，此前最好的方法是十道，它的引擎"
        "单独是十四道，GPT-4是零道；金牌得主平均解出25.9道。<bookmark mark='d'/>一年后，AlphaGeometry 2解出了2000年以来所有奥赛几何题的"
        "百分之八十四。",

    'Then the olympiad itself, which Part 28 followed in detail.':
        "然后是奥赛本身，第28部分详细讲过。<bookmark mark='a'/>2024年，在Lean里工作的AlphaZero方法AlphaProof，加上负责几何的"
        "AlphaGeometry 2，拿到了四十二分里的二十八分，离金牌差一分。<bookmark mark='b'/>2025年，谷歌的Gemini Deep Think和OpenAI的一个"
        "实验模型各自拿到三十五分，正好是金牌线，证明是用普通语言写的。<bookmark mark='c'/>而在2026年7月的上海，两家中国公司，华为和"
        "小红书，报告它们的系统拿到了满分，四十二分里的四十二分，解答提交给了组织方评分，据法新社报道；六百六十六名学生里也有七人拿了"
        "四十二分。奥赛作为对机器的测试，已经接近饱和。",

    'Beyond contests, the frontier is research mathematics.':
        "在比赛之外，前沿是研究级的数学。<bookmark mark='a'/>把非形式的数学翻译成Lean，也就是自动形式化，速度猛然加快：2025年9月，初创公司"
        "Math Inc.报告说，它的智能体Gauss用大约三个星期，把强素数定理形式化了，大约两万五千行Lean代码。<bookmark mark='b'/>2026年1月，"
        "OpenAI的GPT-5.2 Pro和Harmonic的证明器Aristotle合作，解决了埃尔德什第728号问题，最后给出的是一个Lean证明。<bookmark mark='c'/>"
        "谷歌DeepMind的一个团队让Gemini处理了七百个标为未解的保罗·埃尔德什问题：解决了十三个，五个靠的是看来是新的论证，八个是因为答案"
        "原来已经在文献里了。<bookmark mark='d'/>两点提醒。形式化证明恰好证明它的陈述，所以译错的陈述证明的是错的东西；而且，正如密切关注"
        "的数学家们所说，最先被攻下的都是比较容易的问题。",

    'With a perfect checker, search can be trusted:':
        "有了完美的检查器，搜索就可以信任：放手去生成，只留下通过检查的。最后一章讲的正是这个。",

    # ------------------------------------------------------------------ Search
    'Chapter seventeen. Discovery by search.':
        '第17章。靠搜索做发现。',

    'When the checker is exact, discovery becomes a loop.':
        "当检查是精确的，发现就变成了一个循环。<bookmark mark='a'/>提出一个候选，一段程序或一个构造；<bookmark mark='b'/>精确地给它打分；"
        "<bookmark mark='c'/>保留最好的，再变化它们。<bookmark mark='d'/>第26部分讲过的AlphaTensor，用一个AlphaZero网络来提出候选。"
        "2023年12月，谷歌DeepMind的贝尔纳迪诺·罗梅拉–帕雷德斯等人在FunSearch里让一个语言模型来写Python程序，程序库分散在不同的岛上，"
        "就像进化中的种群。<bookmark mark='e'/>它在八维空间里找到了一个帽集，五百一十二个点，其中没有三点共线，超过了已知的四百九十六个，"
        "这是这个问题二十年来最大的一次跃进。",

    'f"Let\'s run that loop ourselves':
        "我们自己来跑这个循环，用FunSearch的一个问题：在线装箱。<bookmark mark='a'/>物品一个一个到来，每个都必须立刻放进一个箱子。一条规则"
        "来决定：给物品放得下的每个箱子打分，挑分最高的。<bookmark mark='b'/>经典的规则是最佳适配：挑剩余空间最小的箱子。<bookmark "
        "mark='c'/>我们把这样的打分当作公式来进化，用随机的变异和交叉代替语言模型，按它们在八个训练序列上用了多少箱子来评判。{evo_line}。"
        "<bookmark mark='d'/>{res_line}。<bookmark mark='e'/>2025年的一项独立研究对语言模型进化出来的启发式方法也有同样的发现：它们常常"
        "无法推广到培育它们的那些实例之外。",

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

    "f'At rank seven, {r7[1]} of":
        '秩为七时，{r7[2]}个起点里有{r7[1]}个找到了：一个类似施特拉森的算法，它把随机矩阵乘对到小数点后{vdp}位',

    'In May 2025 Google DeepMind combined both lines in AlphaEvolve.':
        "2025年5月，谷歌DeepMind在AlphaEvolve里把这两条线合在了一起。<bookmark mark='a'/>Gemini模型提出对整段程序的修改，评估器给它们"
        "打分，进化保留最好的。<bookmark mark='b'/>它的成果之一：用四十八次乘法计算四乘四复数矩阵的乘积，胜过了把施特拉森的技巧用两次"
        "得到的四十九次，那是1969年以来的纪录。<bookmark mark='c'/>它是通过进化一段基于梯度的分解搜索代码做到的，正是我们刚才跑的那一类"
        "搜索。<bookmark mark='d'/>几个星期之内，法国的三位研究者，让–纪尧姆·迪马、克莱芒·佩尔内和亚历山大·塞多格拉维奇，推导出了一个"
        "只用有理系数的四十八次算法。<bookmark mark='e'/>AlphaEvolve还在十一维空间里让593个球同时接触一个中心球，创下新纪录；在五十多个"
        "未解问题上，它有四分之三追平了已知最好的答案，五分之一做得更好。<bookmark mark='f'/>在谷歌内部，它找到的一条调度规则为公司收回了"
        "0.7%的算力；它加速的一个内核让Gemini的训练时间缩短了百分之一。<bookmark mark='g'/>2025年11月，陶哲轩等人让它去处理六十七个问题，"
        "并发表了它的发现，以及它失败的地方。",

    'Discovery by search, then:':
        "所以，靠搜索做发现：放手去提出，精确地检查，留下经得起检查的。只要检查是精确的，它就管用，这就是数学和算法走在最前面的原因。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来总结一下。对称是一种不应该改变答案的变换，网络可以从构造上精确地尊重它，也可以从样本里近似地学会它。求和造出集合上的"
        "函数；对邻居求和造出图网络，它恰好看见颜色细化看见的东西，叠得太深又会丢失细节。把转动做进去，让我们的分子模型在同样的数据下"
        "好得多。AlphaFold通过用三角形保持一致的残基对来读一个蛋白质，用坐标系把它搭起来，用一个分得清左右的损失给它打分，它的后继者则"
        "把原子交给了扩散。天气在网格网上运行；方程被学成算子；晶体被成百万地筛选；而在数学里，检查器是完美的，搜索就能做出发现。",

    'All of this comes back.':
        "这一切都还会回来。<bookmark mark='a'/>由网络引导、由精确检查器评判的搜索，就是下一次要讲的AlphaZero，以及第28部分的推理模型。"
        "<bookmark mark='b'/>一个把世界向前推演的学习型模拟器，就像我们的网格网络，是第29部分的世界模型。<bookmark mark='c'/>网络的各层"
        "表示了什么，它的特征是否尊重我们期望的对称性，是第30部分的主题。<bookmark mark='d'/>而CASP的盲测，以及一个几乎被机器做到饱和的"
        "奥赛，引出了第31部分的问题：到底该怎样评估。",

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
