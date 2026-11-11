"""Chinese narration for cs56: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第56部分：谱图与扩展图"

CHAPTERS = {
    "Hook": "特征值对一张图知道些什么",
    "Laplacian": "1. 拉普拉斯矩阵",
    "Fiedler": "2. 瑞利商与 Fiedler 向量",
    "Cheeger": "3. Cheeger 不等式",
    "Walks": "4. 随机游走与混合",
    "Expanders": "5. 扩展图",
    "Zigzag": "6. 显式扩展图：之字形乘积",
    "Uses": "7. 扩展图的用处",
    "Electrical": "8. 作为电网络的图",
    "Solvers": "9. 拉普拉斯求解器与稀疏化子",
    "Maxflow": "10. 从电流到最大流",
    "Frontier": "11. 前沿：高维扩展图",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "Here are two graphs. <bookmark mark='a'/> Each has sixteen":
        "这里有两张图。<bookmark mark='a'/>每张都有16个顶点排成一个环，外加一些额外的边。左边的额外边是近邻之间的短弦；右边的则是随机连的。<bookmark mark='b'/>画出来，它们看上去"
        "差不多。但有一个数能把它们区分开：由图构造出的一个矩阵的第二小特征值。<bookmark mark='c'/>左边它很小：这张图很容易切成两半，在它上面的随机游走要过很久才会忘掉自己从哪里出发。右边它几乎大了三"
        "倍：没有哪个割是便宜的，游走混合得很快。这一部分讲的，就是一张图的特征值知道些什么。",
    'f"The same number, computed for three graphs this':
        "同一个数，对这个系列已经搭建过的三张图算出来。<bookmark mark='a'/>第18部分的城市网格有{city['n']}个路口，它的第二特征值非常小：大约{city['lambda2']:.3f}。网"
        "格很容易从中间切开，特征向量找到的那个割只穿过少数几条道路。<bookmark mark='b'/>第36部分那张由提供商和客户组成的互联网，以及一张由我们某部小说里相邻出现的词构成的图，连通得要好得多。"
        "<bookmark mark='c'/>到这一部分结束时，我们会知道：为什么这一个特征值限定了一张图有多难切开、混合得有多快、怎样传导电流，以及这些事实怎样在2022年引出了已知最快的最大流算法。",
    "This is Part 56 of Computer Science, Built, and the first":
        "这是《计算机科学，从零搭建》的第56部分，也是第十一幕“研究前沿”的第一部分。<bookmark mark='a'/>我们会搭建一张图的拉普拉斯矩阵并读出它的特征值；用 Fiedler 向量切分图，并证明 Ch"
        "eeger 不等式；测量随机游走混合得有多快；构造扩展图，也就是稀疏却无法切开的图；把图当作电路；再沿着这些电路，走到一个以几乎线性的时间运行的最大流算法。",
    # ------------------------------------------------------------------ s02_laplacian
    "Chapter one. The Laplacian, the matrix that sees the shape":
        "第一章：拉普拉斯矩阵，看得见图的形状的矩阵。",
    "Start with a small graph: five vertices and five edges.":
        "从一张小图开始：5个顶点，5条边。<bookmark mark='a'/>写下两个矩阵。度矩阵 D 的对角线上是每个顶点的邻居个数。<bookmark mark='b'/>邻接矩阵 A 在两个顶点相连的地方是1"
        "。<bookmark mark='c'/>它们的差，D 减 A，就是这张图的拉普拉斯矩阵。<bookmark mark='d'/>读其中一行，第三个顶点的那一行：对角线上是它的度，3，它的三个邻居各对应一个负1"
        "。<bookmark mark='e'/>所以每一行的和都是零，拉普拉斯矩阵把全1向量变成零。这个名字来自物理：一个顶点处的拉普拉斯算子，把它的值与邻居的值作比较，在相差一个符号的意义下，是一种离散的二阶导数。",
    "Why this matrix? Because of the number it gives when you put":
        "为什么是这个矩阵？因为在它两边放上同一个向量时，它给出的那个数：x 转置 L x，其中 x 是用数给顶点做的任意一种标注。<bookmark mark='a'/>把 L 拆成两部分。"
        "<bookmark mark='b'/>度的那部分，一个顶点碰到几条边，就把它的平方计几次；邻接的那部分，对每一条边给出两端乘积的两倍。<bookmark mark='c'/>把两者都按边归拢：每条边带来 x "
        "i 的平方，加 x j 的平方，减去两者乘积的两倍。<bookmark mark='d'/>这正是一个完全平方。拉普拉斯矩阵的二次型，就是对所有的边，把每条边两端之差的平方加起来。"
        "<bookmark mark='e'/>把每条边想成一根弹簧，把 x 想成各个顶点的高度：这就是弹簧里储存的能量。沿着边变化缓慢的标注，储存的能量很少，这里是7个单位。<bookmark mark='f'/>同"
        "样的五个值，重新排列成沿着边跳变的样子，储存的是39。",
    "That energy is never negative, so every eigenvalue of the":
        "这个能量从不为负，所以拉普拉斯矩阵的每个特征值都至少是零。<bookmark mark='a'/>我们从最小的开始编号：λ1，它总是零，对应全1向量；然后是 λ2，一直到 λn。"
        "<bookmark mark='b'/>能量什么时候恰好为零？只有当没有哪条边两端有差：也就是 x 在图的每个连通的块上都是常数。<bookmark mark='c'/>这张图有两块，所以有两种互相独立的方式做"
        "到这一点：点亮左边那块，<bookmark mark='d'/>或者右边那块。所以零是一个二重特征值。一般地，零特征值的个数就是连通分量的个数。<bookmark mark='e'/>现在加上一座桥。图连通了，"
        "一个零特征值升了起来，但升得不高：λ2 很小，因为只有一条边勉强把两半连在一起。",
    "So lambda two is zero exactly when the graph falls apart,":
        "所以 λ2 恰好在图散开时为零，而它的大小说明图连得有多牢。<bookmark mark='a'/>这里是四张8个顶点的图，从最稀疏的连通图，也就是路径，经过环和立方体，一直到完全图。"
        "<bookmark mark='b'/>它们的第二特征值从大约0.15一路爬到8。<bookmark mark='c'/>Miroslav Fiedler 在1973年研究了这个数，把它命名为代数连通度。加一条"
        "边永远不会让它变小，下一章会证明这一点；而且只要图不是完全图，它就至多等于点连通度，也就是删去后能让图不连通的最少顶点数。对于画面只能隐约暗示的东西，它是一个稳健而连续的度量。",
    "Real graphs rarely fall apart completely, but they often":
        "真实的图很少完全散开，但常常差一点就散开了。<bookmark mark='a'/>这张图有120个顶点，分成两个各有60个顶点的预设社区，社区内部的边很密，社区之间很稀。"
        "<bookmark mark='b'/>它最小的12个特征值：照例先是零；然后是一个与众不同的特征值，大约是3；接着是主体部分，从4.5以上开始。<bookmark mark='c'/>这个规律推广了恰好散开的"
        "情形：一张几乎散成 k 块的图，有 k 个接近零的特征值，后面跟着一个间隙。",
    "One adjustment makes graphs with very uneven degrees":
        "做一个调整，就能让度数非常不均匀的图也可以相互比较。<bookmark mark='a'/>在拉普拉斯矩阵两边，都按每个度的平方根分之一做缩放。<bookmark mark='b'/>展开来，这个归一化拉普拉斯"
        "矩阵就是单位矩阵减去一个重新缩放过的邻接矩阵。<bookmark mark='c'/>它的特征值位于0到2之间，它的零特征值仍然数出连通分量的个数，而且每个顶点都按它的度来计权，所以一个枢纽顶点无法一手遮天。"
        "<bookmark mark='d'/>开场在这个系列自己的图上测量的就是这个版本：第18部分的城市网格勉强连在一起，而互联网和小说里的词则连得紧密得多。第三章的 Cheeger 不等式和第四章的随机游走，讲的"
        "都是这个矩阵。",
    # ------------------------------------------------------------------ s03_fiedler
    "Chapter two. Rayleigh quotients, and the Fiedler vector.":
        "第二章：瑞利商，以及 Fiedler 向量。",
    "Chapter one promised that adding an edge never lowers lambda":
        "第一章承诺过，加一条边永远不会让 λ2 变小。证明它、还能证明更多东西的工具，是瑞利商：一种标注的能量除以它的大小。<bookmark mark='a'/>因为 L 是对称的，它的特征向量可以取成标准正交的，于"
        "是任何 x 都是它们的组合。<bookmark mark='b'/>在这组基下，交叉项消失了：能量是各个特征值乘以系数平方之和，大小是系数平方之和。<bookmark mark='c'/>所以瑞利商是特征值的一"
        "个加权平均，每个特征值的权重，就是 x 有多少落在它的特征向量方向上。<bookmark mark='d'/>移动权重，平均值就跟着移动，但它永远不会跑出特征值的范围。<bookmark mark='e'/>它"
        "的最小值，零，来自把全部权重放在第一个特征向量，也就是常数向量上。",
    "Now forbid the constant vector: allow only labellings":
        "现在禁止常数向量：只允许与全1向量正交的标注，也就是各个值之和为零的标注。<bookmark mark='a'/>那么第一个权重就是零，<bookmark mark='b'/>平均只在 λ2 及以上的特征值之间"
        "进行，它永远不会比 λ2 小。<bookmark mark='c'/>把全部权重放在第二个特征向量上，平均值就恰好达到 λ2。所以，在与常数向量正交的向量里，λ2 是最小的瑞利商。"
        "<bookmark mark='d'/>一般的表述是 Courant–Fischer 定理：第 k 个特征值，是在所有 k 维子空间上，取子空间内部最差的那个商，再取其中最好的。Ernst Fischer 在1"
        "905年证明了它，Richard Courant 在1920年做了推广。<bookmark mark='e'/>第一章的承诺在这里兑现了。加一条边，就给每个向量的能量加上一个平方，所以每个商都会上升，每个特征值"
        "也随之上升。",
    "Why should an eigenvector know where to cut? Write a cut as":
        "为什么一个特征向量会知道该在哪里切？把一个割写成一个向量：一边是负1，另一边是正1。<bookmark mark='a'/>同一边内部的边对能量毫无贡献；穿过割的边贡献4。所以能量是被切断的边数的四倍。"
        "<bookmark mark='b'/>求把图分成两个相等的半边的最佳割，也就是最小二等分，就是在和为零的正负1向量上把能量最小化。这个问题是 NP 困难的。<bookmark mark='c'/>所以把它放松"
        "：允许任何实数值，只要和相同、长度相同。最小值只会下降，<bookmark mark='d'/>而由 Courant–Fischer 定理，放松后的最小值是 n 除以4乘以 λ2：这是每一种二等分的一个下界，而"
        "达到它的向量就是第二个特征向量。",
    "Here is the second eigenvector of the bridged graph, drawn":
        "这是那张带桥的图的第二个特征向量，用颜色画出来：蓝色表示负的分量，橙色表示正的分量，越亮表示越大。<bookmark mark='a'/>它在一个簇上为负，在另一个簇上为正，在桥的两端绝对值最小，它就在那里变号"
        "。<bookmark mark='b'/>在网格上，它是沿着长边的一道缓慢的波，所以它建议的割径直穿过中间，也就是第18部分那座城市的便宜割。<bookmark mark='c'/>把顶点按它们的值排成一列，就"
        "得到 Fiedler 序。在零处把它分开，就把两个簇分开了。<bookmark mark='d'/>Fiedler 在1975年证明，这并非偶然：在一张连通图里，向量值不为负的那些顶点，总是构成一个连通的块。",
    "Now a graph too large to read by eye: chapter one's hundred":
        "现在是一张大到无法用肉眼读懂的图：第一章那张120个顶点、有两个预设社区的图。<bookmark mark='a'/>只根据边，不看标签，算出第二个特征向量，并画出每个顶点的分量，其中前60个顶点属于社区 A。"
        "<bookmark mark='b'/>A 的每个顶点分量都为负，B 的每个顶点分量都为正。这些符号恰好恢复了预设的社区。没有人告诉过这个矩阵哪个顶点属于哪里。",
    "With more than two communities, use more eigenvectors.":
        "社区多于两个时，就用更多的特征向量。<bookmark mark='a'/>这张图有三个簇，每两个簇之间由一条边相连，所以它有三个很小的特征值。<bookmark mark='b'/>给每个顶点一个坐标，取它在"
        "第二和第三个特征向量里的分量。各个簇收缩成三团紧密的点，任何一种简单的点聚类方法，比如 k-means，都能把它们分开。<bookmark mark='c'/>这就是谱聚类，其形式由 Jianbo Shi 和 "
        "Jitendra Malik 在2000年为图像分割而推广，又由 Andrew Ng、Michael Jordan 和 Yair Weiss 在2001年推广。<bookmark mark='d'/>要给有几十"
        "亿条边的图做分片，METIS 这样的多级划分器更快，它出自 George Karypis 和 Vipin Kumar 之手，但追求的是同一个目标：被切断的边少，各部分均衡。",
    # ------------------------------------------------------------------ s04_cheeger
    "Chapter three. Cheeger's inequality, and the sweep cut.":
        "第三章：Cheeger 不等式，以及扫描割。",
    "Chapter two cut graphs with an eigenvector; now we prove how":
        "第二章用一个特征向量切分图；现在我们证明它切得有多好。<bookmark mark='a'/>一组顶点的体积是它们的度之和，<bookmark mark='b'/>一个割的导率，是它穿过的边数，除以较小一侧的体"
        "积。<bookmark mark='c'/>切下三个顶点要穿过两条边，但这一侧很小：导率是四分之一。<bookmark mark='d'/>在两个簇之间切，穿过同样的两条边，一侧却大得多：九分之一。"
        "<bookmark mark='e'/>一张图的导率就是它最佳割的导率，而找到它是 NP 困难的。<bookmark mark='f'/>Cheeger 不等式说，归一化拉普拉斯矩阵的 λ2 从两边把它夹住：至"
        "少是 λ2 的一半，至多是 λ2 两倍的平方根。Jeff Cheeger 在1970年对弯曲的流形证明了它；图的版本在二十世纪八十年代相继出现。",
    "The easy direction says that a cheap cut forces a small":
        "容易的那个方向说，一个便宜的割迫使特征值很小。<bookmark mark='a'/>把归一化拉普拉斯矩阵的 λ2 写成对向量 y 的一个最小值，方法是代入 x 等于 D 的平方根乘以 y。现在我们只需要一个好"
        "的测试向量。<bookmark mark='b'/>任取一个集合 S，在 S 上放它的体积分之一，在 S 以外放负的另一侧体积分之一。它按度加权的和为零，所以是允许的。<bookmark mark='c'/>只"
        "有被切断的边两端有差，而且这些差大小都相同。<bookmark mark='d'/>一个因子约掉了，<bookmark mark='e'/>剩下的两项，每一项都至多是较小体积分之一。所以对每一个 S，λ2 都至"
        "多是 S 的导率的两倍，对最佳的那个 S 尤其如此。",
    "The hard direction is the surprise: a small eigenvalue":
        "困难的那个方向才令人意外：一个小的特征值保证存在一个便宜的割，而且证明会把它找出来。从特征向量 y 开始，它的商就是 λ2。<bookmark mark='a'/>把它的分量摆在一条直线上。"
        "<bookmark mark='b'/>找到点 c，使它两侧的体积都至多一半，再把一切都平移 c。这样分子不变，分母只会变大。<bookmark mark='c'/>现在把平移后的向量拆成正的部分和负的部分。穿"
        "过任何一条边，两部分差的平方加起来至多是原来的那个，所以其中有一部分的商不大于 λ2。<bookmark mark='d'/>把它叫作 z：从不为负，只占至多一半的体积，商至多是 λ2。",
    "<bookmark mark='a'/> Scale z so its largest entry is one,":
        "<bookmark mark='a'/>缩放 z，让它最大的分量是1，在0和1之间均匀地取一个 t，留下那些值的平方至少是 t 的顶点。一个顶点被留下的概率是 z i 的平方，而当 t 落在一条边两端的平方之间"
        "时，这条边就被切断。<bookmark mark='b'/>所以被切断的边数的期望是一些平方之差的和，<bookmark mark='c'/>柯西–施瓦茨不等式把它拆成两个平方根："
        "<bookmark mark='d'/>第一个是 z 的商的分子，第二个至多是根号二乘以它的分母。<bookmark mark='e'/>体积的期望恰好就是那个分母。所以平均而言，被切断的边数除以体积，至多是 "
        "λ2 两倍的平方根。<bookmark mark='f'/>一定有某个阈值做得至少和平均一样好，而每个阈值集合都是 Fiedler 序一端的一段。所以有某个扫描割满足这个界。",
    "So the algorithm is simple. <bookmark mark='a'/> Sort the":
        "所以算法很简单。<bookmark mark='a'/>把顶点按它们在特征向量中的分量排序。<bookmark mark='b'/>取第一个顶点，再取前两个，再取前三个，计算每个前缀的导率，每个顶点越过去时就更"
        "新一次割。<bookmark mark='c'/>保留最好的那个。在我们的小图上，最好的前缀是前六个，也就是两个簇之间的割。<bookmark mark='d'/>在第二章那张120个顶点的图上，导率曲线在60"
        "处降到最低：<bookmark mark='e'/>恰好是预设的划分。一个特征向量，一次排序；Cheeger 不等式保证，在平方根的尺度上衡量，答案离最优永远不远。",
    "Finally, a check. <bookmark mark='a'/> Fifty-three connected":
        "最后，做一次检验。<bookmark mark='a'/>53张12个顶点的连通随机图，小到可以把全部2047个割都试一遍，找出最佳割。<bookmark mark='b'/>每张图都落在两条曲线之间。"
        "<bookmark mark='c'/>扫描割也像证明所承诺的那样，停在上面那条曲线以下，并在53张图中的32张上找到了真正最好的割。<bookmark mark='d'/>两边都无法改进超过一个常数。超立方体"
        "恰好达到下界，而在一个很长的环上，导率确实是 λ2 的平方根量级。",
    # ------------------------------------------------------------------ s05_walks
    "Chapter four. Random walks, and how fast they mix.":
        "第四章：随机游走，以及它们混合得有多快。",
    "Put a walker on a vertex and let it step to a random":
        "在一个顶点上放一个游走者，让它一次又一次地走到一个随机的邻居，并跟踪它在哪里的概率。<bookmark mark='a'/>每一步，每个顶点都把自己的概率平均分给它的邻居：乘以 D 的逆乘 A。"
        "<bookmark mark='b'/>一开始把全部质量放在最左边的一个顶点上，看它扩散开来：先遍及它自己的簇，然后慢慢地越过两座桥。<bookmark mark='c'/>它会在哪里稳定下来？试着给每个顶点与"
        "它的度成正比的质量，d i 除以边数的两倍。<bookmark mark='d'/>走一步，每个邻居恰好把它的那一份送回来，度又重新出现了：这个分布不会改变。它是平稳分布，在一张不是二分图的连通图上，从任何起点"
        "出发都会收敛到它。",
    "<bookmark mark='a'/> On a bipartite graph, such as this":
        "<bookmark mark='a'/>在二分图上，比如这个有8个顶点的环，游走者在两侧之间交替：全部质量都在偶数顶点上，然后都在奇数顶点上，永远如此。它永远不会稳定。<bookmark mark='b'/>解"
        "药是懒惰。每一步以二分之一的概率留在原地，否则就移动。现在质量会扩散，并稳定下来。<bookmark mark='c'/>用度的平方根对懒惰游走做共轭：<bookmark mark='d'/>出现的是二分之一乘"
        "以单位矩阵加上重新缩放过的邻接矩阵，也就是单位矩阵减去归一化拉普拉斯矩阵的一半。<bookmark mark='e'/>所以懒惰游走的特征值，是1减去 N 的特征值的一半：全都在0和1之间，最大的恰好是1，下一"
        "个是1减去 λ2 的一半，也就是谱隙。",
    "Here is why the gap sets the speed. <bookmark mark='a'/>":
        "下面说明为什么谱隙决定速度。<bookmark mark='a'/>把初始分布用懒惰游走的特征向量写出来。每一步把沿第 i 个特征向量的分量乘以 μi。第一个分量，μ1 等于1，就是平稳分布本身，它保持不变。"
        "<bookmark mark='b'/>让游走运行，其他每个分量都按几何级数衰减。<bookmark mark='c'/>最后消失的是第二个分量，它每一步只缩小到1减去谱隙的一半。在这张图上，两座桥让谱隙很小，"
        "所以那一个模态，也就是两个簇之间的不平衡，在其他模态消失之后还久久不散。",
    "<bookmark mark='a'/> Measure the distance from stationarity":
        "<bookmark mark='a'/>用总变差，也就是差值之和的一半，来衡量离平稳分布的距离，并把混合时间定义为：从任何起点出发，这个距离第一次不超过四分之一时的步数。<bookmark mark='b'/>"
        "除了平稳模态，每个模态每一步都至少缩小到1减去谱隙的一半，柯西–施瓦茨不等式把这个结果换算成总变差，代价是最小平稳概率分之一的平方根。<bookmark mark='c'/>1减 x 至多是 e 的负 x 次方"
        "，<bookmark mark='d'/>所以游走在谱隙分之一，乘以那个最小概率分之四的对数步之内就会混合。<bookmark mark='e'/>而最慢的模态迫使它至少要走大约谱隙分之二乘以二的对数那么多步。"
        "<bookmark mark='f'/>所以，在相差一个对数的意义下，混合时间就是谱隙分之一。",
    "Now measure. Four graphs on sixty-four vertices: a cycle, an":
        "现在来测量。四张64个顶点的图：一个环，一个8乘8的网格，一张每个顶点都有4个邻居的随机图，以及一个杠铃图，也就是由一条边连起来的两个稠密的团。<bookmark mark='a'/>在每张图的一个顶点上开始一"
        "次懒惰游走。<bookmark mark='b'/>随机图15步就混合了，网格要51步；环和杠铃图走了300步之后还差得很远。<bookmark mark='c'/>它们的谱隙在走任何一步之前就讲出了同一个故事"
        "，而我们能测到的每个混合时间，都落在两个界之间。<bookmark mark='d'/>杠铃图的谱隙是所有图里最小的，尽管它的边最多：那一座桥是一个导率极小的割，而由 Cheeger 不等式，极小的导率迫使谱隙也极小。",
    "PageRank, from Part 18, is a random walk with a restart.":
        "第18部分的 PageRank 是一个带重启的随机游走。<bookmark mark='a'/>冲浪者以0.85的概率跟随一个随机链接；否则就跳到一个均匀选取的网页。<bookmark mark='b'/>这一"
        "跳换来了一个谱隙：Taher Haveliwala 和 Sepandar Kamvar 在2003年证明，这个矩阵的其他特征值的绝对值都不大于阻尼因子。所以幂迭代的误差每一步至少缩小那个因子。"
        "<bookmark mark='c'/>在第18部分那张有两万个网页的随机网络上，每一步的变化下降得还要更快，每步大约缩小到0.58，52步就达到10的负12次方。随机链接造出一张混合得很快的图：也就是下一章的扩展图。",
    # ------------------------------------------------------------------ s06_expanders
    "Chapter five. Expanders: graphs that are sparse, and yet":
        "第五章：扩展图，稀疏却无法切开的图。",
    "What makes a graph an expander? <bookmark mark='a'/> Take":
        "是什么让一张图成为扩展图？<bookmark mark='a'/>取 Petersen 图，10个顶点，每个的度都是3，挑出外圈的五个。<bookmark mark='b'/>边扩展数的是离开一个集合的边，按每"
        "个顶点平均：这里五条边离开五个顶点，比值是1，而在至多一半顶点的集合里，没有哪个做得更好。<bookmark mark='c'/>顶点扩展数的是一个集合能到达的新邻居：内圈的全部五个。"
        "<bookmark mark='d'/>谱扩展要求，除了最大的那个特征值 d 以外，每个特征值的绝对值都很小：这里是3、1和负2，所以 λ 是2。<bookmark mark='e'/>第三章的 Cheeger"
        " 不等式，按度 d 重新缩放之后，把第一种和第三种联系起来：d 下方一个很宽的间隙，意味着没有便宜的割。让图越长越大时保持这个间隙，它们就构成一族扩展图。",
    "<bookmark mark='a'/> Take any two sets of vertices, S and T,":
        "<bookmark mark='a'/>任取两组顶点 S 和 T，数一数它们之间的边。<bookmark mark='b'/>一张度相同的随机图，大约会有 d 乘 S 乘 T 除以 n 条。"
        "<bookmark mark='c'/>扩展图混合引理说，一张扩展图对所有的集合对同时都接近这个数：误差至多是 λ 乘以两个集合大小之积的平方根。<bookmark mark='d'/>用密度来读：从 S 连到"
        " T 的边所占的比例，就是两个密度的乘积，误差在 λ 除以 d 之内。一个小的 λ，让一张固定的稀疏图，在每个大集合看来都像是随机的。",
    "<bookmark mark='a'/> Write the count as the indicator of S,":
        "<bookmark mark='a'/>把这个计数写成 S 的指示向量，乘 A，再乘 T 的指示向量。<bookmark mark='b'/>把每个指示向量拆成它的平均，也就是全1向量的一个倍数，加上一个与全1"
        "向量正交的余项。<bookmark mark='c'/>展开。A 把全1向量送到 d 乘全1向量，所以两个交叉项都消失了。<bookmark mark='d'/>全1、A、全1，是各个度之和，于是第一项恰好就是"
        "随机图的那个计数。<bookmark mark='e'/>剩下的就是误差。A 把与全1正交的向量仍然映到与全1正交的向量，并且至多把它们拉长 λ 倍，所以由柯西–施瓦茨不等式，误差至多是 λ 乘以两个余项的长度"
        "，而每个余项都比它的指示向量短。<bookmark mark='f'/>这就是那个引理。",
    "How small can lambda be? <bookmark mark='a'/> Compare any":
        "λ 能有多小？<bookmark mark='a'/>把任何一张正则图和度为 d 的无穷树作比较。<bookmark mark='b'/>A 的2k次方的迹数的是闭游走，它等于各个特征值的这个次方之和：最大的那"
        "个贡献 d 的2k次方，其他每个至多贡献 λ 的2k次方。<bookmark mark='c'/>但每个顶点至少有树上那么多条闭游走：形状的个数是一个卡特兰数，而每向外走一步，至少有 d 减1种选择。"
        "<bookmark mark='d'/>把两者结合起来，<bookmark mark='e'/>取 k 为 log n 的一个小倍数，λ 就只能比 d 减1的平方根的两倍低一个趋于零的量。"
        "<bookmark mark='f'/>这就是 Alon–Boppana 界。达到它的图叫作 Ramanujan 图；Lubotzky、Phillips 和 Sarnak 在1988年造出了最早的几族。",
    "Now measure. <bookmark mark='a'/> One random regular graph":
        "现在来测量。<bookmark mark='a'/>对五种度，从3到12，每种取一张400个顶点的随机正则图。<bookmark mark='b'/>最大的特征值总是 d；黄色的曲线是 Ramanujan 界。"
        "<bookmark mark='c'/>测到的每个 λ 都正好落在它下方：度为3时是2.82对2.83，度为12时是6.42对6.63。抛硬币就能接近最好的可能；第十一章会说明为什么。"
        "<bookmark mark='d'/>再看混合引理，在200对随机集合上：最坏的误差从大约五分之一到大约三分之一，远在 λ 之内。",
    "Do expanders exist? Counting says yes, as in Part 2.":
        "扩展图存在吗？计数说存在，就像第2部分那样。<bookmark mark='a'/>让左边 n 个顶点中的每一个，都在右边随机挑 d 个邻居。<bookmark mark='b'/>一个集合 S 的所有邻居都落"
        "在某个集合 T 里，只有当它的全部 d 乘 S 条边都落在那里时才会发生。<bookmark mark='c'/>对每个大小为 s 的 S 和每个大小为 α 乘 s 的 T 取联合界，"
        "<bookmark mark='d'/>给二项式系数估个界，<bookmark mark='e'/>再把各个幂收拢：当 d 大于 α 加1、而且集合很小时，括号里的量小于二分之一。"
        "<bookmark mark='f'/>对所有大小求和，某个小集合失败的概率小于1，所以存在某张图永远不会失败。Mark Pinsker 在1973年用的就是这样的计数。<bookmark mark='g'/>"
        "但抛硬币不是一种构造：一张有2的100次方个顶点的随机图，连存都存不下。",
    # ------------------------------------------------------------------ s07_zigzag
    "Chapter six. Explicit expanders, and the zig-zag product.":
        "第六章：显式扩展图，以及之字形乘积。",
    "Chapter five ended on a problem. <bookmark mark='a'/>":
        "第五章留下了一个问题。<bookmark mark='a'/>显式的意思是：有一段短程序，给它一个用比特串表示的顶点和一个边的标号，它能在这个比特串长度的多项式时间内返回那个邻居。"
        "<bookmark mark='b'/>第一族来自1973年的 Grigory Margulis：顶点是模 m 的数对，邻居来自几个固定的线性映射。<bookmark mark='c'/>他的证明没有给出明确的"
        "常数；Ofer Gabber 和 Zvi Galil 在1981年补上了一个，而 Lubotzky、Phillips 和 Sarnak 的 Ramanujan 图依赖于深刻的数论。2000年，Omer Rein"
        "gold、Salil Vadhan 和 Avi Wigderson 找到了一种构造，它的证明只有一页长。",
    "<bookmark mark='a'/> Take a big graph G, here five vertices":
        "<bookmark mark='a'/>取一张大图 G，这里是5个度为4的顶点，再取一张小图 H，它的每个顶点对应 G 的一个顶点上的一条边：一个4-环。<bookmark mark='b'/>把 G 的每个顶"
        "点换成一朵云，也就是 H 的一个副本，它的点就是 G 的边接入的端口。乘积的一个顶点，就是一朵云加一个端口。<bookmark mark='c'/>一条边是三步移动。Zig：在云内部走 H 的一步。"
        "<bookmark mark='d'/>大步：从那个端口沿着 G 的边离开。<bookmark mark='e'/>Zag：在新的云里，再走 H 的一步。<bookmark mark='f'/>Zig 有两种选"
        "择，zag 有两种：度是4，不管 G 的度是多少。<bookmark mark='g'/>我们的更大：G 是60个顶点、度为8，H 是8个顶点、度为3，得到480个度为9的顶点。",
    "<bookmark mark='a'/> Write one step as three matrices: a":
        "<bookmark mark='a'/>把一步写成三个矩阵：在每朵云里走 H 的一步，大步，它只是置换端口，再走 H 的另一步。<bookmark mark='b'/>H 是扩展图，所以它的一步几乎就是跳到一个"
        "均匀的端口：1减 λH 份的这种跳跃，加上 λH 份的一个范数至多为1的矩阵。<bookmark mark='c'/>乘开。有一项两边都用均匀跳跃；其余三项合起来，不超过它们的权重。"
        "<bookmark mark='d'/>那一项就是 G 自己的游走：在一朵云上取平均，从一个随机端口走 G 的边，再取一次平均。在与均匀向量正交的方向上，它按 λG 缩小。"
        "<bookmark mark='e'/>所以乘积的 λ 至多是 λG 和1的一个混合。<bookmark mark='f'/>整理一下：乘积的谱隙至少是 G 的谱隙乘以1减 λH 的平方：缩小了一个固定的因子，"
        "但永远不会闭合。",
    "Now the product we built. <bookmark mark='a'/> G, of degree":
        "现在看我们造出的乘积。<bookmark mark='a'/>度为8的 G，归一化的 λ 大约是三分之二；8个顶点、度为3的 H，大约是四分之三。<bookmark mark='b'/>乘积测得0.81：一张真"
        "正的扩展图，度为9。<bookmark mark='c'/>Reingold、Vadhan 和 Wigderson 更精细的界保证它至多是0.91；我们证明的谱隙界给出0.98。"
        "<bookmark mark='d'/>他们最简单的界，λG 加 λH 加 λH 的平方，在这里几乎是2，什么也说明不了。它是为 λ 很小的 H 准备的。",
    "Now the construction. <bookmark mark='a'/> Fix one small":
        "现在来做构造。<bookmark mark='a'/>固定一张小扩展图 H，它有 D 的4次方个顶点，度为 D，λ 至多是五分之一。它的大小是常数，所以可以靠搜索找到。<bookmark mark='b'/>然"
        "后交替进行：平方，它把 λ 平方，却把度乘起来；再和 H 做之字形乘积，它把度拉回来。<bookmark mark='c'/>如果 G t 的度是 D 的平方，λ 至多是五分之二，那么它的平方的度是 D 的4次"
        "方，恰好是 H 的大小，λ 至多是二十五分之四。<bookmark mark='d'/>之字形乘积加上五分之一和二十五分之一，<bookmark mark='e'/>又得到五分之二：同样的保证，而顶点数变成 D"
        " 的4次方倍。<bookmark mark='f'/>再做一处改进，在平方之前把两张一半大小的图做张量积，就让求每个邻居的时间成为 log N 的多项式。",
    "It paid off in 2005. <bookmark mark='a'/> In an undirected":
        "它在2005年得到了回报。<bookmark mark='a'/>在一张无向图里，从 s 能到达 t 吗？广度优先搜索要记住它见过的每个顶点。随机游走只需要对数大小的内存，Aleliunas 和合作者在1979"
        "年证明了这一点，但它需要硬币。<bookmark mark='b'/>Omer Reingold 把硬币去掉了：重复一轮操作，用一张固定的小扩展图做之字形乘积，再做几次平方。"
        "<bookmark mark='c'/>每一轮都让度保持为常数，并让谱隙至少翻倍，直到它成为一个常数。一张连通图的谱隙一开始至少是 N 的某个多项式分之一，所以对数多轮就能让每个连通分量都成为扩展图，直径是 l"
        "og N 量级。<bookmark mark='d'/>然后从 s 出发，试遍这个长度的每一条游走：一串常数大小的标号，用对数大小的内存就够了。对称对数空间等于对数空间。",
    # ------------------------------------------------------------------ s08_uses
    "Chapter seven. Expanders at work: saving random bits,":
        "第七章：扩展图的用处：节省随机比特，纠正错误，以及证明定理。",
    "Parts 20 and 27 amplified randomized algorithms by rerunning":
        "第20和第27部分通过重复运行来放大随机算法。<bookmark mark='a'/>假设一个算法读 r 个随机比特，只有一个坏集合，至多占全部比特串的一半，能骗过它。<bookmark mark='b'/>各"
        "次独立运行全部失败的概率，是二分之一的运行次数次方，但每次运行都要花 r 个新比特。<bookmark mark='c'/>换一种做法：把全部2的 r 次方个比特串放在一张常数度的显式扩展图上。随机挑一个起点，"
        "然后游走：<bookmark mark='d'/>每一步只花度的对数那么多比特。<bookmark mark='e'/>这些样本不再独立了。它们全都落在 B 里的可能性有多大？",
    "<bookmark mark='a'/> Start uniform. Each step moves with the":
        "<bookmark mark='a'/>从均匀分布开始。每一步先用游走矩阵 M 移动，再用投影 P 只保留 B 上的质量；剩下的，就是每个样本都是坏的概率。<bookmark mark='b'/>看其中一步。把"
        "一个落在 B 上的向量 x，拆成沿全1向量的部分和其余部分；M 让第一部分保持不变。<bookmark mark='c'/>第一部分很小，因为 B 很小：柯西–施瓦茨不等式把它限制在 μ 乘以 x 以内。其余部"
        "分按 λ 缩小。<bookmark mark='d'/>所以每一步花掉一个因子 μ 加 λ，<bookmark mark='e'/>于是所有样本都落在 B 里的概率，至多是 μ 乘以 μ 加 λ 的 t 次方。"
        "平均值也行：David Gillman 在1998年为这样的游走证明了一个切尔诺夫界。",
    "What does it buy? <bookmark mark='a'/> Take an illustrative":
        "它换来了什么？<bookmark mark='a'/>取一个用作说明的算法，它有256个随机比特和一半的坏集合，再取一张 λ 为四分之一、度为2的10次方的扩展图：每一步10个比特。"
        "<bookmark mark='b'/>每一步把失败概率的界乘以四分之三。<bookmark mark='c'/>要让误差降到2的负20次方，独立运行需要5120个比特；游走需要46步，716个比特。"
        "<bookmark mark='d'/>游走每把误差减半一次，只付一个常数；重新运行则要付完整的 r。",
    "Part 28 drew parity-check codes as graphs of bits and":
        "第28部分把奇偶校验码画成由比特和校验组成的图，这是沿用 Michael Tanner 1981年的做法。<bookmark mark='a'/>这里是一个玩具：12个比特，每个比特在3个校验里。1996年，M"
        "ichael Sipser 和 Daniel Spielman 问，扩展能换来什么。<bookmark mark='b'/>取一小组比特 S。如果恰好只有一条来自 S 的边到达某个校验，这个校验就是一个唯一邻居"
        "。<bookmark mark='c'/>每个唯一的校验占用 S 的一条边，每个共享的校验至少占用两条。<bookmark mark='d'/>如果小集合到达的校验数，超过它们边数的四分之三，"
        "<bookmark mark='e'/>那么 S 的边有一半以上终止在唯一的校验上。<bookmark mark='f'/>所以一个落在小集合上的非零字会通不过某个校验：它不是码字，于是码距很大。",
    "Expansion also gives a decoder. <bookmark mark='a'/> Send":
        "扩展还能给出一个解码器。<bookmark mark='a'/>发送全零；到达时有两个比特翻转了。<bookmark mark='b'/>每个涉及奇数个错误比特的校验都不满足：一共四个。"
        "<bookmark mark='c'/>规则是：如果一个比特有超过一半的校验不满足，就翻转它。<bookmark mark='d'/>第一个错误比特符合条件；翻转它，剩下三个不满足的校验。"
        "<bookmark mark='e'/>现在第二个错误比特的三个校验全都不满足；翻转它，每个校验都满意了。<bookmark mark='f'/>Sipser 和 Spielman 证明，在足够好的扩展图上，只"
        "要错误不超过长度的一个固定比例，这个方法总是有效：总有某个错误比特符合条件，而每次翻转都让不满足的计数下降：线性时间。",
    "Expanders also drive Irit Dinur's proof of the PCP theorem,":
        "扩展图还驱动了 Irit Dinur 对第27部分 PCP 定理的证明。<bookmark mark='a'/>把一个问题写成图的边上的约束，就像着色那样。如果它不可满足，m 个约束中至少有一个失败：间隙是 m"
        " 分之一。<bookmark mark='b'/>每一轮做三件事：把图变成扩展图，损失一个常数因子；把约束换成长度为 t 的游走，于是间隙随 t 增长；再把字母表缩回去，又损失一个常数。"
        "<bookmark mark='c'/>取 t 为一个很大的常数，每一轮都让间隙至少翻倍，直到一个上限，同时让图增大一个常数倍。<bookmark mark='d'/>经过对数多轮之后，间隙是常数，规模是多项式"
        "。<bookmark mark='e'/>游走之所以管用，是因为在扩展图上，它们碰到坏边的频率，大约和独立样本一样。",
    "<bookmark mark='a'/> In 2012 Ankit Singla, Chi-Yao Hong,":
        "<bookmark mark='a'/>2012年，Ankit Singla、Chi-Yao Hong、Lucian Popa 和 Brighten Godfrey 提出了 Jellyfish：把一个数据中心的"
        "交换机随机地连在一起。<bookmark mark='b'/>随机正则图几乎是 Ramanujan 图，正如第五章所测，所以路径保持很短，也没有哪个割是瓶颈。<bookmark mark='c'/>而且它扩容得"
        "很从容：切断一条链路，把它的两端都连到新的交换机上。<bookmark mark='d'/>2016年的 Xpander 有意把这样的网络设计成扩展图。接下来，把拉普拉斯矩阵当作电路。",
    # ------------------------------------------------------------------ s09_electrical
    "Chapter eight. Graphs as electrical networks.":
        "第八章：作为电网络的图。",
    "Part 3 built logic from switches driven by voltages; now":
        "第3部分用电压驱动的开关搭建了逻辑；现在电路以数学的身份回来了。把图的每条边变成一个电阻，再给每个顶点一个电压。<bookmark mark='a'/>欧姆定律：沿一条边的电流，是它的电导乘以它两端的电压降。"
        "<bookmark mark='b'/>基尔霍夫定律：从一个顶点流出的电流，对它的各条边求和，等于从外部注入那里的电流。<bookmark mark='c'/>把欧姆定律代入基尔霍夫定律。"
        "<bookmark mark='d'/>展开：这个顶点的电压乘以它的加权度，减去它的邻居们的电压。<bookmark mark='e'/>这就是拉普拉斯矩阵的一行。所有的行合在一起说的是 L x 等于 b：输入"
        "电压，输出注入的电流。Gustav Kirchhoff 在1847年写下了这些方程。",
    "Now drive the circuit. <bookmark mark='a'/> Inject one amp":
        "现在给电路通电。<bookmark mark='a'/>在 s 注入1安培，再从 t 把它引出：b 在 s 处是正1，在 t 处是负1。它的分量之和为零，而这恰好是一个拉普拉斯方程组可解所需要的。"
        "<bookmark mark='b'/>电压是 L 的伪逆作用在 b 上，相差一个常数，所以把 t 设为零，再按电压给每个顶点着色。<bookmark mark='c'/>电流沿着每条边向低处流，电压降大的地方"
        "就粗。<bookmark mark='d'/>而在每个内部顶点，流进多少就流出多少：这里流进0.45，流出0.09和0.36。",
    "How hard is it to push current from s to t? <bookmark":
        "把电流从 s 推到 t 有多难？<bookmark mark='a'/>有效电阻，就是推动1安培所需的电压。<bookmark mark='b'/>用向量 e s 减 e t 读出那个电压差，"
        "<bookmark mark='c'/>它就是 b 本身，而电压是 L 的伪逆乘以 b：这是关于拉普拉斯矩阵伪逆的一个二次型。<bookmark mark='d'/>它也是电流消耗的能量：第一章那个差的平方和，"
        "在这些电压处，<bookmark mark='e'/>化成了同一个形式。<bookmark mark='f'/>在你熟悉的电路上验证一下：两个1欧姆的电阻，串联是2，并联是二分之一。我们那个有9个电阻的电路，大"
        "约是1.36。",
    "Which of all the ways to send one unit from s to t does":
        "从 s 到 t 输送一个单位的所有方式里，电流会选哪一种？<bookmark mark='a'/>给每个单位流一个能量：电阻乘以流量的平方，对所有边求和。<bookmark mark='b'/>把任何一个流写成"
        "电流加上一个环流，环流在每个顶点处都是平衡的。<bookmark mark='c'/>交叉项消失了：由欧姆定律，它是电压降乘以环流，按顶点重新归组之后，每个电压乘的都是一个为零的净流量。"
        "<bookmark mark='d'/>所以电流的能量最小，而这个能量就是有效电阻：这就是 Thomson 原理。<bookmark mark='e'/>把这个单位分到两条路径上，代价是1.5；只走一条路径，是"
        "3。<bookmark mark='f'/>一个推论：降低任何一个电阻，都不会让有效电阻升高。",
    "Now let a random walker loose. Its commute time is the":
        "现在放出一个随机游走者。它的往返时间，是从 s 走到 t 再走回来的期望步数。<bookmark mark='a'/>设 φ(u) 是从 u 到达 t 的期望时间：走一步，然后取邻居们的平均。"
        "<bookmark mark='b'/>乘以度，<bookmark mark='c'/>它就是一个拉普拉斯方程组：注入的是各个度，在 t 处引出全部的2m。到达 s 的时间，叫作 ψ，满足同样的方程组。"
        "<bookmark mark='d'/>相减：度抵消了，φ 减 ψ 是2m 乘以1安培时的电压。<bookmark mark='e'/>在 s 和 t 处读出：往返时间是2m 乘以有效电阻，这是 Chandra"
        "、Raghavan、Ruzzo、Smolensky 和 Tiwari 在1989年证明的。Doyle 和 Snell 1984年的书早已把游走和电路联系在一起。",
    "Test it. <bookmark mark='a'/> A five by five grid has forty":
        "检验一下。<bookmark mark='a'/>一个5乘5的网格有40条边。从一角到对角，它的有效电阻大约是2.14，所以公式预测往返时间大约是171步。<bookmark mark='b'/>这是一个游走者"
        "，在四处游荡。<bookmark mark='c'/>两千次模拟的往返，平均是174步，在抽样误差之内。一个关于游荡的问题，变成了一个拉普拉斯方程组。",
    "One classic from Doyle and Snell's book. <bookmark":
        "Doyle 和 Snell 书里的一个经典问题。<bookmark mark='a'/>George Pólya 在1921年证明，正方晶格上的随机游走必定会回到家；在立方晶格上则未必。"
        "<bookmark mark='b'/>用电路的话说：恰好当从原点到无穷远的电阻是无穷大时，它必定会回来。<bookmark mark='c'/>在平面上，把每一层正方形的壳都短接成一个结点；由瑞利的原理，这只"
        "会降低电阻。<bookmark mark='d'/>剩下的是一束束并联的边，每束4条、12条、20条，再串联起来。<bookmark mark='e'/>8k 加4分之一求和是无穷大，所以游走者会回到家。"
        "<bookmark mark='f'/>在三维空间里，一股分散在大约 k 的平方条边的壳层上的电流，能量是有限的，所以由 Thomson 原理，电阻是有限的。",
    # ------------------------------------------------------------------ s10_solvers
    "Chapter nine. Laplacian solvers, and the sparse graphs that":
        "第九章：拉普拉斯求解器，以及让它们变快的稀疏图。",
    "Everything that follows needs to solve L x equals b fast.":
        "接下来的一切，都需要快速地解 L x 等于 b。高斯消元要花立方时间，而且正如第52部分所示，会把稀疏矩阵填满。共轭梯度法做得更好。<bookmark mark='a'/>第 k 次迭代的结果由 b、L b、L"
        " 的平方乘 b 等等构成：要乘 k 次 L。<bookmark mark='b'/>而 L 的 j 次方乘 b，只在 j 跳以内才不为零。<bookmark mark='c'/>在一条路径上观察它，电流从一端流"
        "进，从另一端流出。答案是一条笔直的斜坡，但每次迭代只能从两端各向内延伸一个顶点。<bookmark mark='d'/>一般地，迭代次数像条件数的平方根那样增长，条件数就是最大特征值除以 λ2。又长又细的图条件"
        "很差；扩展图则不然。",
    "The cure for bad conditioning is preconditioning: solve with":
        "条件差的解药是预条件：用一个更容易解的相近矩阵来解，再让共轭梯度法修正两者的差别。<bookmark mark='a'/>对拉普拉斯矩阵来说，天然的相近矩阵是一张更稀疏的图 H 的拉普拉斯矩阵，它的二次型保持在"
        " G 的1加减 ε 倍之内，<bookmark mark='b'/>而且对每个向量 x 同时成立：每一种能量，因而每一个割。Spielman 和滕尚华把这样的 H 叫作谱稀疏化子。"
        "<bookmark mark='c'/>于是预条件后的方程组，所有特征值都接近1。<bookmark mark='d'/>我们的测试图有300个顶点和13657条边。它的稀疏化子保留1591条，共轭梯度法的迭代"
        "次数从67次降到14次。",
    "Which edges can a sparsifier drop? <bookmark mark='a'/> Two":
        "稀疏化子可以去掉哪些边？<bookmark mark='a'/>两个各有8个顶点的团，由一座桥相连。按有效电阻给每条边着色。<bookmark mark='b'/>桥的电阻是1：它是唯一的通道，两个团之间的每个"
        "割都依赖于它。团内部的一条边电阻是四分之一：有很多别的路线能替它干活。<bookmark mark='c'/>而且总量是固定的。每个电阻都是一个二次型；<bookmark mark='d'/>把它们归拢成一个迹"
        "；<bookmark mark='e'/>一张连通图的各条边的加权电阻，加起来等于 n 减1。这是1949年的 Foster 定理。电阻是一份重要性的预算，总共 n 减1，不管有多少条边。",
    "In 2008 Daniel Spielman and Nikhil Srivastava turned that":
        "2008年，Daniel Spielman 和 Nikhil Srivastava 把这份预算变成了一个算法。<bookmark mark='a'/>按与权重乘有效电阻成正比的概率抽取边。"
        "<bookmark mark='b'/>抽 q 条，每条抽中的边的权重设为 q 与它的概率之积的倒数。<bookmark mark='c'/>平均而言，样本的拉普拉斯矩阵恰好就是 G 的。"
        "<bookmark mark='d'/>大约抽 n log n 除以 ε 的平方次，一个矩阵集中不等式就能让它以很高的概率准确到1加减 ε 倍以内。<bookmark mark='e'/>从我们的两个团里抽40"
        "次，保留了那座桥，并让两个团变稀；均匀抽取有一半的时候会漏掉那座桥，连同两半之间的每一条路径。<bookmark mark='f'/>随后 Joshua Batson、Spielman 和 Srivastava"
        " 证明，线性条数的边总是足够。对完全图，他们的稀疏化子能与边数多一倍的 Ramanujan 扩展图相媲美：两倍 Ramanujan 稀疏化子。",
    "But computing an effective resistance means solving a":
        "但是计算一个有效电阻，就意味着解一个拉普拉斯方程组，而我们要的是全部 m 个。<bookmark mark='a'/>改写那个二次型。<bookmark mark='b'/>在两个伪逆之间插入 L，"
        "<bookmark mark='c'/>再通过边–顶点关联矩阵把 L 分解开。<bookmark mark='d'/>现在每个电阻都是同一个矩阵的两列之间距离的平方。<bookmark mark='e'/>距离"
        "在随机投影下得以保持：这是《人工智能，从零搭建》和第20部分草图里的 Johnson–Lindenstrauss 引理。一个大约 log n 行的随机矩阵，能把每一个这样的距离都保持在1加减 ε 倍之内。"
        "<bookmark mark='f'/>所以 log n 次拉普拉斯求解，就能一下子给出每一个电阻。<bookmark mark='g'/>稀疏化子需要电阻，电阻需要求解器，这个循环被一个先出现的求解器打破了。",
    "The simplest sparse graph is a spanning tree. <bookmark":
        "最简单的稀疏图是一棵生成树。<bookmark mark='a'/>在网格上铺一棵蛇形的树。<bookmark mark='b'/>树漏掉的一条边，必须用它在树中的路径来替代；那条路径的长度就是这条边的伸展度，"
        "这里是11。<bookmark mark='c'/>树是图的一部分，而每条边的代价至多是它的伸展度乘以它的树路径，所以条件数至多是总伸展度。<bookmark mark='d'/>而树上的方程组，可以通过一片片"
        "剥掉叶子，在线性时间内解出。<bookmark mark='e'/>一棵带中央脊柱的树伸展得更少，条件也更好。<bookmark mark='f'/>Spielman 和滕尚华在2004年，用低伸展度树和稀疏化"
        "子搭建了一个递归：用一棵树加上几条边做预条件，消去度为一和二的顶点，再递归下去。拉普拉斯方程组变得可以在近线性时间内求解。",
    # ------------------------------------------------------------------ s11_maxflow
    "Chapter ten. From electrical flows to maximum flow.":
        "第十章：从电流到最大流。",
    "Part 18 met maximum flow: push as much as possible from s to":
        "第18部分见过最大流：在不超过任何一条边容量的前提下，从 s 向 t 推送尽可能多的流量，当时用增广路径解决了这个问题。<bookmark mark='a'/>这里是一个网络，容量从1到4；它的最大流是4。"
        "<bookmark mark='b'/>电流很诱人，因为一次拉普拉斯求解，在近线性时间内，就能把全部流量一下子分摊到每条路径上送过去。给每条边的电阻设为容量的平方分之一，这样宽的边导电就好。"
        "<bookmark mark='c'/>但电流对容量一无所知。从 s 到 a 的那条边容量是2，却被要求承载将近3：拥塞是1.41。",
    "Current breaks capacities, but not by much on average, and":
        "电流会突破容量，但平均来说突破得不多，原因就是 Thomson 原理。<bookmark mark='a'/>给每条边一个权重，从1开始，电阻是权重除以容量的平方。<bookmark mark='b'/>假设某"
        "个值为 F 的流能满足容量限制。电流的能量不超过那个流的能量，而后者至多是各个权重之和。<bookmark mark='c'/>把电流的能量逐条边写出来，<bookmark mark='d'/>它说的是：拥塞平"
        "方的加权平均至多是1。少数边可以溢出，但只是少数。<bookmark mark='e'/>我们的第一个电流让一条边溢出了41%，而加权的平方平均远低于1。",
    "So use the overflow to adjust the weights. <bookmark":
        "所以，用溢出来调整权重。<bookmark mark='a'/>算一个电流；按拥塞的比例，提高每条边的权重，也就是它的电阻；然后重复，并把各次的流取平均。溢出的边变得昂贵，下一次的电流就会避开它们。"
        "<bookmark mark='b'/>这就是第23部分的乘性权重方法，电流充当专家的那一步。<bookmark mark='c'/>一轮又一轮，平均流的最大拥塞从1.41向1下降。"
        "<bookmark mark='d'/>30轮之后，把平均流缩小到满足容量为止：它承载了最大流的97%。<bookmark mark='e'/>2011年，Paul Christiano、Jonathan Ke"
        "lner、Aleksander Mądry、Daniel Spielman 和滕尚华把这个循环打磨成了当时已知最快的无向图近似最大流算法。",
    "The other road from circuits to flows runs through":
        "从电路通往流的另一条路，经过内点法，那是在第23部分和 Karmarkar 一起见过的。<bookmark mark='a'/>最大流是一个线性规划。<bookmark mark='b'/>把硬性的容量限制换成"
        "一个对数障碍函数，它在任一限制处都升到无穷大。<bookmark mark='c'/>每一个牛顿步，都在流量守恒的约束下，最小化一个二次模型：一个线性项加上一个加权平方和。"
        "<bookmark mark='d'/>这就是一个电流的能量，每条边的电阻就是它的障碍函数的曲率，而当这条边快满时，曲率会急剧增大。<bookmark mark='e'/>所以每一步就是一次拉普拉斯求解，电流会"
        "自己绕开已满的边。大约 m 的平方根步，就能在大约 m 的二分之三次方的时间内给出精确的流；接下来的十年，都花在减少步数上。",
    "In 2022 Li Chen, Rasmus Kyng, Yang Liu, Richard Peng,":
        "2022年，Li Chen、Rasmus Kyng、Yang Liu、Richard Peng、Maximilian Probst Gutenberg 和 Sushant Sachdeva 迈出了最后一步。"
        "<bookmark mark='a'/>一个电流步，把一个小改变分摊到每一条路径上，而且每一次都需要重新求解。<bookmark mark='b'/>他们把它换成了它在另一种范数下的近亲：收益与长度之比最好的环"
        "流，而最好的那个是单独一个圈。<bookmark mark='c'/>铺下一棵生成树：树外的每一条边恰好闭合一个圈，<bookmark mark='d'/>而当这棵树的伸展度很低时，这些圈中有一个，与最好的那个"
        "相差在一个不大的因子之内。<bookmark mark='e'/>他们的方法需要 m 的1加小 o(1) 次方步，再用动态数据结构让这些树保持最新，每一步花 m 的小 o(1) 次方。"
        "<bookmark mark='f'/>结果是：有向图上的精确最大流和最小费用流，在几乎线性的时间内求解。",
    "Step back and look at the exponent. <bookmark mark='a'/> In":
        "退后一步，看看指数。<bookmark mark='a'/>1972年，埃德蒙兹和卡普的增广路径要 n 乘 m 的平方步，在稀疏图上是立方。<bookmark mark='b'/>1998年，安德鲁·戈德堡和 "
        "Satish Rao 达到了大约 m 的二分之三次方。<bookmark mark='c'/>电流在2011年为无向图上的近似流打破了这道屏障，<bookmark mark='d'/>2022年，对有向图上的精"
        "确流，指数降到了1。<bookmark mark='e'/>这条路从基尔霍夫的方程出发，经过快速拉普拉斯求解器、电流和内点法，走到了低伸展度树上的圈。这个算法仍然复杂得远远无法在实践中运行，前沿一章会把这一点列"
        "入未解决的问题。",
    # ------------------------------------------------------------------ s12_frontier
    "Chapter eleven, the frontier. What happens when triangles,":
        "第十一章，前沿。当不只是边，连三角形也必须扩展时，会发生什么？",
    "An expander is a graph in which every set of vertices has":
        "扩展图是这样一张图：每一组顶点都有很多条边离开它。<bookmark mark='a'/>高维扩展图对一个复形提出同样的要求：顶点、边和三角形，粘合在一起。<bookmark mark='b'/>在每个顶点周围"
        "，碰到它的那些三角形构成一张小图，叫作它的链接。<bookmark mark='c'/>当一个复形是连通的，并且每个链接本身都是扩展图时，它就是高维扩展图。<bookmark mark='d'/>令人意外的是一"
        "条从局部到整体的原理，可以追溯到1973年的 Howard Garland，并在最近十年被加强：如果每个链接都扩展得足够好，那么在三角形之间移动的随机游走，就会在整个复形上快速混合。"
        "<bookmark mark='e'/>与普通扩展图不同，有界度的例子无法靠随机抽取得到；已知的构造来自深刻的代数。",
    "In a few years high-dimensional expanders have settled old":
        "短短几年间，高维扩展图就解决了一些老问题。<bookmark mark='a'/>2019年，Nima Anari、Kuikui Liu、Shayan Oveis Gharan 和 Cynthia Vinzan"
        "t 证明，一个简单的随机游走能快速地对任何拟阵的基进行抽样，解决了 Mihail 和 Vazirani 的一个猜想，随后谱独立性又把这种方法带到了统计物理中的模型上。<bookmark mark='b'/>20"
        "22年，两个小组造出了具有常数码率、常数距离和常数局部性的局部可测试码，以及第53部分所需要的那种好的量子低密度码。<bookmark mark='c'/>而 Irit Dinur 对第27部分 PCP 定理的"
        "证明，早已用扩展图来放大间隙；更高维的扩展图是通往更强版本的一条路。<bookmark mark='d'/>在每一种情形里，扩展都把一个局部的检查变成了一个全局的保证。",
    "How small can a regular graph's second eigenvalue be?":
        "一张正则图的第二特征值能有多小？<bookmark mark='a'/>Alon 和 Boppana 证明，在极限情况下，它不能低于 d 减1的平方根的两倍。达到这个界的图叫作 Ramanujan 图。"
        "<bookmark mark='b'/>我们第五章的随机正则图正好落在这条曲线下方，而 Joel Friedman 在2008年证明，随机正则图能以任意小的差距接近它。<bookmark mark='c'/>2"
        "015年，Adam Marcus、Daniel Spielman 和 Nikhil Srivastava 证明，对每一种度，都存在二分的 Ramanujan 图，用的是一种新方法，多项式的交错族，它还解决了 K"
        "adison–Singer 问题。",
    "Open problems. <bookmark mark='a'/> Simple explicit":
        "未解决的问题。<bookmark mark='a'/>对每一种度，都有简单的显式 Ramanujan 图。<bookmark mark='b'/>小集合几乎按完整的度增长的显式扩展图。"
        "<bookmark mark='c'/>把几乎线性时间的最大流从一个定理变成实用的软件。<bookmark mark='d'/>还有最稀疏割的最佳近似，Arora、Rao 和 Vazirani 那个平方根 lo"
        "g 的界仍然屹立不倒。<bookmark mark='e'/>这一部分的研究题，是 Raghavendra 和 Steurer 的小集合扩展假设：判断一张图里的小集合是否扩展，在计算上是困难的。它会推出第27部"
        "分的唯一博弈猜想，而没有人知道它是否成立。",
    # ------------------------------------------------------------------ s13_outro
    "What we built in this part. The Laplacian, whose quadratic":
        "我们在这一部分搭建了什么。拉普拉斯矩阵，它的二次型是一种标注的能量，它的第二特征值说明一张图连得有多紧。Fiedler 向量和扫描割，由 Cheeger 不等式为它们提供保证。随机游走，它们的混合时间由谱隙决定"
        "。扩展图，随机的和 Ramanujan 的，以及显式地构造它们的之字形乘积。作为电网络的图，其中往返时间就是电阻，还有通往几乎线性时间最大流的稀疏化子和求解器。贯穿始终的是一个想法：一张图的特征值，用寥寥几个数"
        "概括了它的整体形状。",
    "Where this comes back. Part 58 meets fixed points again, in":
        "它们会在哪里再出现。第58部分在程序的含义中再次遇到不动点。第59部分在每个结点只能看到自己邻域的图上运行算法，并证明这种视野必须延伸多远。而第61部分把这一部分的未解决问题，唯一博弈猜想，放到尚属未知之事的地图上。",
    "In practice. Spectral clustering embeds a graph by its":
        "在实践中。谱聚类用图最底部的那些特征向量来嵌入一张图，然后对这些点做聚类。多级划分器为分片和并行计算切分图。PageRank 是一个带重启的随机游走。数据中心网络已经建在类似扩展图的拓扑上。而拉普拉斯方程组每天"
        "都在用预条件共轭梯度法和多重网格求解。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：自己构造一个之字形乘积，并把它的第二特征值与 Reingold、Vadhan 和 Wigderson 的界作比较。最后一道标"
        "了星号，是一道研究题：判断小集合是否扩展，是不是困难的。",
    "Next time, Part 57: learning theory. When can a machine":
        "下一次，第57部分：学习理论。机器什么时候能从样例中学习，它需要多少样例，而当经典理论说庞大的神经网络不应该泛化时，它们为什么还能泛化？",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
