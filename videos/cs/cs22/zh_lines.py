"""Chinese narration for cs22: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第22部分：几何"

CHAPTERS = {
    "Hook": "左边、右边，还是在线上？",
    "Orient": "1. 唯一的基本操作",
    "Hulls": "2. 凸包",
    "Sweep": "3. 扫描线",
    "Gallery": "4. 守卫美术馆",
    "Voronoi": "5. Voronoi 图",
    "Delaunay": "6. Delaunay 三角剖分",
    "Lifting": "7. 提升映射",
    "Incremental": "8. 随机顺序与反向分析",
    "Lp": "9. 平面上的线性规划",
    "KdTree": "10. 范围查询",
    "PointLocation": "11. 点定位",
    "HighDim": "12. 高维空间",
    "Duality": "13. 对偶与火腿三明治",
    "Planning": "14. 移动机器人",
    "Frontier": "15. 前沿：精确性、3SUM 与最近邻",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Here is the most basic question in computational geometry.":
        "这是计算几何中最基本的问题。点 p 在过 q 和 r 的直线的左边、右边，还是在线上？<bookmark mark='a'/>取 q 为十二、十二，r 为二十四、"
        "二十四，把 p 放在离点二分之一、二分之一极近的地方，离直线只差几个浮点数步长。<bookmark mark='b'/>这个测试是一个二乘二行列式，答案"
        "不应取决于先列出哪个点。在双精度下它却取决于此。这样问，p 在左边；把三个点轮换一下，p 恰好在线上；再轮换，p 在右边。<bookmark "
        "mark='c'/>真正的答案是右边，每次都是。<bookmark mark='d'/>这不是罕见的意外：在这条直线附近，成千上万个最近的浮点数点得到互相矛盾的"
        "答案，而建立在矛盾答案上的算法会崩溃、陷入死循环，或者返回一个不凸的凸包。",
    "Kettner and his colleagues drew the picture in 2008.":
        "Kettner 和他的同事们在2008年画出了这幅图。<bookmark mark='a'/>取一半、一半周围二百五十六个步长之内的所有浮点数，一个六万五千点的"
        "网格，按浮点运算的回答给每个点上色：左边蓝色，右边绿色，线上灰色。真正的直线恰好沿着对角线。<bookmark mark='b'/>我们看到的不是干净"
        "的分界，而是一条斑驳的带子。<bookmark mark='c'/>把错误的答案标成红色：将近一万二千个。这一部分先修好这个测试，再在它之上构造平面上"
        "那些美丽的结构。",
    "Part 22 of Computer Science, Built: Geometry.":
        "计算机科学，从零搭建，第22部分：几何。<bookmark mark='a'/>这一部分包括：几乎不花代价就变得精确的方向测试；凸包、扫描线，以及美术馆的"
        "守卫；由抛物线扫描生长出的 Voronoi 图，和原来是三维凸包之投影的 Delaunay 三角剖分；随机化算法和为它们定价的反向分析；线性规划、"
        "范围查询、点定位和高维的诅咒；以及为机器人规划运动。",
    # ------------------------------------------------------------------ Orient
    "Chapter one. The one primitive.": "第1章。唯一的基本操作。",
    "Almost every algorithm in this part asks one question":
        "这一部分几乎每个算法都在一遍又一遍地问同一个问题。<bookmark mark='a'/>从 p 走向 q，r 在你的左边吗？答案是一个由坐标之差构成的二乘二"
        "行列式的符号。<bookmark mark='b'/>这个行列式是三角形 p q r 有向面积的两倍：<bookmark mark='c'/>三点逆时针转时为正，<bookmark "
        "mark='d'/>顺时针转时为负，共线时为零。<bookmark mark='e'/>凸包、扫描、三角剖分和点在多边形内的测试，都由这个符号构成。<bookmark "
        "mark='f'/>它的近亲内圆测试问的是一个点是否在过另外三点的圆内；它是一个三乘三行列式，我们会在 Delaunay 那里遇到它。",
    "Why does it fail?":
        "它为什么会出错？<bookmark mark='a'/>行列式是两个乘积之差，a 减 b。<bookmark mark='b'/>每次减法和乘法都被舍入到最近的双精度数，相对"
        "误差约为九百万亿分之一。<bookmark mark='c'/>在直线附近，a 和 b 几乎相等，它们的差极小：比计算它们时产生的舍入误差还小。这时结果的符号"
        "就是噪声。<bookmark mark='d'/>但误差可以被界住。Jonathan Shewchuk 证明，误差至多约为三个 epsilon 乘以 a 和 b 的大小。<bookmark "
        "mark='e'/>所以当算出的答案大于这个界时，它的符号一定是对的。<bookmark mark='f'/>否则，忽视这个问题是危险的：Kettner 的论文展示了教科书"
        "上的增量凸包丢失点、陷入循环，以及返回不凸的多边形。",
    "That gives Shewchuk's adaptive predicates.":
        "这就得到了 Shewchuk 的自适应谓词。<bookmark mark='a'/>先用浮点数计算行列式。<bookmark mark='b'/>如果它大于误差界，就停下：符号是确定的。"
        "<bookmark mark='c'/>否则就精确地再算一遍。Shewchuk 用扩展表示，即保存每一个丢失比特的双精度数之和；我们用有理数，慢一些但简单。"
        "<bookmark mark='d'/>我们对每种输入各测了两万次。在随机点上，普通浮点数从不出错，自适应测试也从不需要精确阶段，所以代价大约是一次裸"
        "乘法的两倍。在几乎共线的点上，浮点数差不多五次错一次，而自适应测试十次中有七次退回到精确运算。<bookmark mark='e'/>关键在于，只在答案"
        "可疑的地方才为精确性付费。<bookmark mark='f'/>另一条路是让坐标保持为小整数，这时计算本身就是精确的；这一部分的算法就是这样做的，用 "
        "Python 的无界整数。",
    # ------------------------------------------------------------------ Hulls
    "Chapter two. Convex hulls.": "第2章。凸包。",
    "The convex hull of a set of points is the smallest convex polygon":
        "一组点的凸包是包含它们全部的最小凸多边形：在钉子周围套上橡皮筋，然后松手。<bookmark mark='a'/>Ronald Graham 1972年的扫描从最低点"
        "出发，<bookmark mark='b'/>按其他点与它所成的角度排序，<bookmark mark='c'/>再按这个顺序走过它们，把目前的凸包保存在栈上。每个新点都要"
        "压入；但在此之前，只要栈顶两点与新点构成顺时针转向，栈顶那个点就不可能在凸包上，于是弹出。<bookmark mark='d'/>每个点压入一次、至多"
        "弹出一次，所以排序之后这一遍是线性的。<bookmark mark='e'/>Graham 在贝尔实验室需要它，为一台要画一万个点的绘图仪。",
    "We implemented five hull algorithms with counters":
        "我们实现了五个带计数器的凸包算法，在一万个分别取自正方形、圆盘和圆周的点上运行。<bookmark mark='a'/>正方形中随机点的凸包只有大约二十个"
        "顶点；圆盘中约七十五个；在圆周上，每个点都在凸包上。<bookmark mark='b'/>Jarvis 1973年的礼品包装法每一轮检查所有点找到一个凸包顶点，共 "
        "n 乘 h 次测试：在正方形上很便宜，在圆周上毫无希望。<bookmark mark='c'/>Graham 扫描和 Andrew 的单调链（按 x 排序，分别构造下凸包和上"
        "凸包），无论形状如何都大约花 n log n，几乎全花在排序上。<bookmark mark='d'/>快速凸包像快速排序那样划分点集，也像快速排序一样：随机输入"
        "上快，坏输入上是平方级。<bookmark mark='e'/>Timothy Chan 1996年的算法只需要 n log h，这是最优的，但它的常数因子很大。在这些"
        "规模下单调链胜出，大多数程序库用的也是它。",
    "Could a cleverer algorithm avoid the n log n?":
        "更聪明的算法能避开 n log n 吗？不能，证明是一个归约。<bookmark mark='a'/>假设你想给一些数排序。把每个数 x 提升为点 x、x 的平方。"
        "<bookmark mark='b'/>所有提升后的点都在一条抛物线上，而抛物线是凸的，所以它们每一个都是凸包的顶点。<bookmark mark='c'/>从最左点出发绕凸包"
        "走一圈，你就按排好的顺序遇到它们。<bookmark mark='d'/>所以任何凸包算法也是一个排序算法，只多线性的额外工作。第16部分证明了基于比较的"
        "排序需要 n log n；Michael Ben-Or 在1983年把这个界推广到用算术计算并检验符号的算法，而凸包算法正是这样做的。",
    "There is a loophole.":
        "这里有一个漏洞。<bookmark mark='a'/>下界要求每个点都在凸包上。当凸包只有 h 个顶点时，能只付 n log h 吗？<bookmark mark='b'/>Chan 的"
        "算法把点分成每组 m 个，用 Graham 扫描求出每组的凸包。<bookmark mark='c'/>然后像 Jarvis 那样包裹整个点集：为了找下一个顶点，它向每个小"
        "凸包询问从当前点出发的切线，二分查找用 log m 步就能回答。<bookmark mark='d'/>如果 m 等于 h，就是 h 轮、每轮 n 除以 m 乘 log m，总共 "
        "n log h。<bookmark mark='e'/>我们不知道 h，所以Chan 去猜：m 取四，然后十六，然后二百五十六，每次平方，在 m 轮之后放弃这个猜测。失败"
        "的猜测构成一个几何级数，在阶上不增加任何代价。<bookmark mark='f'/>Kirkpatrick 与 Seidel 在1986年最先达到 n log h，论文题为《终极平面凸包"
        "算法》。在三维中凸包仍需 n log n，用的是第八章的随机化方法。",
    # ------------------------------------------------------------------ Sweep
    "Chapter three. The sweep line.": "第3章。扫描线。",
    "Given n line segments, which pairs cross?":
        "给定 n 条线段，哪些对相交？检查每一对要 n 平方次测试，即使几乎没有相交。<bookmark mark='a'/>1979年，Jon Bentley 与 Thomas Ottmann 让"
        "一条竖直线从左到右扫过平面。它只在事件处停下：线段的端点，以及已被预测出的交点。<bookmark mark='b'/>一路上它维护状态：扫描线当前碰到的"
        "线段，从上到下排好序。<bookmark mark='c'/>关键的观察是，两条线段只有在状态中成为邻居之后才可能相交，所以我们只测试邻居：一条线段到来"
        "时，测它和两旁的；离开时，测被它隔开的两条；在交点处，交换位置的两条遇到新邻居。<bookmark mark='d'/>看扫描线移动。每个交点都是在它的两条"
        "线段刚成为邻居时做的一次测试中被发现的，到了交点它们在状态中交换位置。<bookmark mark='e'/>用平衡树存状态、用堆存事件，代价是 n 加 k "
        "再乘 log n，k 为交点数。",
    "We ran our sweep on short random segments in the unit square":
        "我们在单位正方形中的随机短线段上运行我们的扫描，从一百条到三千条，并与检查每一对的结果核对。<bookmark mark='a'/>事件数总是恰好每条线段"
        "两个、每个交点一个，而成对测试大约是事件数的两倍：三千条线段只要两万次测试，而不是四百五十万次。<bookmark mark='b'/>Bernard Chazelle 与 "
        "Herbert Edelsbrunner 后来把界削减到 n log n 加 k，这是最优的。<bookmark mark='c'/>这个想法比这个问题活得更久。扫描把一个二维问题变成"
        "一串一维问题，第五章将用一条扫过点集的线来构造 Voronoi 图。<bookmark mark='d'/>扫描用来计算地理信息系统中地图图层的叠加、检查芯片的设计"
        "规则，以及在 CAD 中求多边形的并与交。",
    # ------------------------------------------------------------------ Gallery
    "Chapter four. Guarding an art gallery.": "第4章。守卫美术馆。",
    "In 1973 Victor Klee asked a question about museums.":
        "1973年，Victor Klee 提出了一个关于博物馆的问题。美术馆是一个有 n 面墙的多边形；守卫站在一点，向各个方向看。对任意有 n 面墙的美术馆，多少"
        "名守卫就够了？<bookmark mark='a'/>Václav Chvátal 在1975年证明，n 除以三（向下取整）名总是足够，而且有时恰好需要这么多。<bookmark "
        "mark='b'/>这里说明为什么有些美术馆需要这么多：一把梳子。每个齿的尖端只能从那个齿内部看到，所以每个齿都需要自己的守卫，而有 k 个齿的梳子"
        "有三 k 加二面墙。",
    "Steve Fisk found a proof in 1978 that fits on a postcard.":
        "Steve Fisk 在1978年找到一个写得进明信片的证明。<bookmark mark='a'/>先用对角线把美术馆三角剖分。这总是可行的：Gary Meisters 证明了每个"
        "多边形都有一只耳朵，即三个相邻顶点所成的三角形位于多边形内部，一只一只地切下耳朵就完成三角剖分。<bookmark mark='b'/>沿对角线相连的三角形"
        "构成一棵树。把一个三角形的三个顶点涂成蓝、绿、黄；每个相邻三角形共享两个已着色的顶点，所以它的第三个顶点只剩一种颜色。走遍这棵树就给每个"
        "顶点着了色，而每个三角形都得到全部三种颜色。<bookmark mark='c'/>某种颜色至多用了 n 除以三次。<bookmark mark='d'/>在这种颜色的每个顶点"
        "上放一名守卫。每个三角形都有一名，而一个三角形从它的任何顶点都能被完全看到，所以整个美术馆都被看守住了。",
    "How fast can we triangulate?":
        "三角剖分能有多快？<bookmark mark='a'/>切耳朵是平方级的。<bookmark mark='b'/>把多边形分成单调的块，每块用一个栈在线性时间内三角剖分，"
        "得到 n log n。<bookmark mark='c'/>Bernard Chazelle 在1991年找到线性时间算法，这个里程碑复杂到没有人去实现它。<bookmark mark='d'/>Fisk 的"
        "论证给出一组守卫，而不是最少的一组：在两百个有六十个顶点的随机多边形上，最小的颜色类平均有十七名守卫。<bookmark mark='e'/>求真正的最小值"
        "是 NP 难的，2018年还证明了它和判定实数命题一样难，那是一个比 NP 略高的类。<bookmark mark='f'/>这个谜题背后是摄像头的布置、传感器的覆盖，"
        "以及显卡绘制的每个多边形的三角剖分。",
    # ------------------------------------------------------------------ Voronoi
    "Chapter five. Voronoi diagrams.": "第5章。Voronoi 图。",
    "Scatter n post offices over a city.":
        "在一座城市里散布 n 个邮局。对每个地址，哪一个最近？<bookmark mark='a'/>答案把平面分成区域，每个站点一个：Voronoi 图。<bookmark "
        "mark='b'/>它的边是到两个站点等距的点，即它们垂直平分线的一段。<bookmark mark='c'/>它的顶点到三个站点等距，是过三个站点且内部没有站点的"
        "圆的圆心。<bookmark mark='d'/>欧拉公式让它保持很小：至多二 n 减五个顶点和三 n 减六条边。<bookmark mark='e'/>Dirichlet 在1850年用过它，"
        "Georgy Voronoi 在1908年；John Snow 的1854年伦敦霍乱地图就是一张水泵的 Voronoi 图。",
    "Steven Fortune found, in 1986, a way to build the diagram with a sweep.":
        "1986年，Steven Fortune 找到了用扫描构造这个图的方法。难点在于，向下扫的直线在遇到一个区域的站点之前就先遇到了这个区域，所以它还无法知道"
        "下面有什么。<bookmark mark='a'/>Fortune 的回答是：考虑那些到扫描线上方某个站点与到扫描线本身一样近的点。对每个站点，它们构成一条抛物线。"
        "<bookmark mark='b'/>这些抛物线中最低的部分构成海滩线。海滩线上方的任何点都比扫描线更靠近某个站点，所以仍在扫描线下方的站点都不可能占有"
        "它：在海滩线上方，图已经是最终的了。<bookmark mark='c'/>随着扫描线移动，弧与弧相接的断点沿 Voronoi 边滑动，把边画出来。<bookmark "
        "mark='d'/>扫描线到达一个站点时，诞生一条新弧，一根逐渐变宽的细刺。<bookmark mark='e'/>当一条弧在两个邻居之间缩成零，三个站点到某一点的距离"
        "与到扫描线的距离都相等：那一点就是 Voronoi 顶点，扫描线恰好碰到过这三个站点的空圆的底部。<bookmark mark='f'/>只有这两种事件，所以用平衡树"
        "存海滩线，扫描只需 n log n。",
    "We implemented the sweep, with the beach line kept as a simple list":
        "我们实现了这个扫描，海滩线存为一个简单的列表，并在多达两千个随机站点上运行。<bookmark mark='a'/>每个 Voronoi 顶点恰好是一个圆事件，"
        "而它们总是有二 n 减二减 h 个，h 为凸包上的站点数。<bookmark mark='b'/>安排的圆事件远多于真正发生的：当一条新弧来到一条正在缩小的弧之下，"
        "预测的顶点就成了误报，被取消。<bookmark mark='c'/>每个顶点的三个站点构成 Delaunay 三角剖分的一个三角形，即下一章的主题；我们的三角形与一种"
        "完全不同的方法，第七章的提升映射，结果完全一致。<bookmark mark='d'/>普通列表使我们的扫描成为平方级；平衡树使它成为 n log n。",
    # ------------------------------------------------------------------ Delaunay
    "Chapter six. Delaunay triangulations.": "第6章。Delaunay 三角剖分。",
    "Connect the sites with triangles.":
        "用三角形把站点连起来。方法有很多；哪一种最好？<bookmark mark='a'/>Boris Delaunay 1934年的回答：只要过三个站点的圆内没有其他站点，就把它们"
        "连起来。<bookmark mark='b'/>这些圆恰好就是 Voronoi 顶点的空圆，所以 Delaunay 三角剖分是 Voronoi 图的对偶：每对相邻区域对应一条边。"
        "<bookmark mark='c'/>一个点是否在过另外三点的圆内，由一个符号决定，即内圆测试，一个最后一列为距离平方的三乘三行列式。和方向测试一样，它也"
        "可以做到精确。",
    "How do we find it? Charles Lawson's method":
        "怎样找到它？Charles Lawson 1977年的方法可以从任意三角剖分出发。<bookmark mark='a'/>这一个按从左到右的扫描遇到点的顺序把它们连起来，满是"
        "细长的三角形：<bookmark mark='b'/>它最小的角不到半度。<bookmark mark='c'/>看两个共享一条边的三角形。如果一个三角形的远端顶点落在另一个三角形"
        "的外接圆内，这条边就是不合法的；翻转它，换成四边形的另一条对角线。重复。<bookmark mark='d'/>十七次翻转之后，没有不合法的边了，剩下的就是 "
        "Delaunay 三角剖分。<bookmark mark='e'/>它的最小角增大了十倍，而 Robin Sibson 证明，在这些点的所有三角剖分中，Delaunay 的使最小角最大。"
        "<bookmark mark='f'/>翻转为什么总会停止？下一章会说明，每次翻转都把三维中的一个曲面往下压，而它不可能无限地降下去。",
    "The empty circles are worth having.":
        "空圆是值得拥有的。<bookmark mark='a'/>没有多余细长三角形的剖分正是模拟所需要的：有限元网格就是 Delaunay 网格，再通过加点来加密，如 Jim "
        "Ruppert 的算法。<bookmark mark='b'/>地形模型用这种方式连接散布的高程测量，而三角剖分给出了它们之间自然的插值。<bookmark mark='c'/>它还"
        "藏着其他问题的答案：每个点与它的最近邻之间有一条 Delaunay 边，最小生成树的每条边也是如此，我们马上就来核对。<bookmark mark='e'/>它可以"
        "用三种方法在 n log n 内构造：Fortune 的扫描、分治，或者最简单的，按随机顺序插入点，这是下下章的内容。",
    "Here is the claim tested.":
        "来检验这个说法。<bookmark mark='a'/>七十个点，灰色是它们的 Delaunay 三角剖分，绿色是它们的最小生成树，即连接所有点的最短网络。每条绿边都"
        "落在一条灰边上。<bookmark mark='b'/>原因是一个交换论证：如果树边 a b 不是 Delaunay 边，就会有某个点落在以 a b 为直径的圆内，离两端都更近，"
        "把它换进来会让树更短。<bookmark mark='c'/>所以第18部分的 Kruskal 算法只需看 Delaunay 边，大约每点三条。对八千个点，这是两万四千条边而不是"
        "三千二百万对，而得到的树与在所有点对上运行 Prim 算法的结果完全相同。Michael Shamos 与 Dan Hoey 在1975年由此给出了这个问题的第一个 n log n "
        "算法。",
    # ------------------------------------------------------------------ Lifting
    "Chapter seven. The lifting map.": "第7章。提升映射。",
    "Here is the most beautiful fact in this part.":
        "这是这一部分最美的事实。<bookmark mark='a'/>取一些点的 Delaunay 三角剖分，从上方看。<bookmark mark='b'/>现在把每个点竖直向上提升到抛物面 "
        "z 等于 x 平方加 y 平方上。<bookmark mark='c'/>提升后的点位于一只凸碗上，所以它们全都在三维凸包上。从下方看这个凸包：它的面都是三角形。"
        "<bookmark mark='d'/>为什么是这些三角形？取平面上的一个圆。它的点提升之后全都落在同一个平面上，因为在圆上 x 平方加 y 平方是 x 和 y 的线性"
        "函数。<bookmark mark='e'/>圆内的点提升后在那个平面之下，圆外的点提升后在它之上。<bookmark mark='f'/>所以过三个站点的圆是空的，恰好当其余所有"
        "提升点都在过这三点的平面之上：恰好当这三个提升点构成下凸包的一个面。<bookmark mark='g'/>Delaunay 三角剖分是提升点下凸包的投影。Kevin "
        "Brown 在1979年看出了这一点，而且它在每个维度都成立：d 维的 Delaunay 就是 d 加一维中的凸包。",
    "The lifting map also explains the in-circle test.":
        "提升映射也解释了内圆测试。<bookmark mark='a'/>把四个点的坐标连同提升后的高度写成一个四乘四行列式。<bookmark mark='b'/>它就是三维中的方向"
        "测试，一个体积的符号，问 d 的提升点是否在过其余三点的平面之下。<bookmark mark='c'/>在一个例子中，四乘四行列式和第六章的三乘三行列式都等于"
        "九十六，因为减去最后一行就把一个化成另一个。<bookmark mark='d'/>它也补完了第六章：一次 Lawson 翻转把提升曲面向上弯的一条边换成向下弯的一条，"
        "所以每次翻转曲面都下降；而三角剖分只有有限多个，所以翻转一定会停止。<bookmark mark='e'/>Voronoi 图则是把同一幅图翻过来：把每个站点提升为"
        "与抛物面相切的平面，Voronoi 区域就是它们上包络各个面的投影。<bookmark mark='f'/>我们核对了这个定理：scipy 对我们的提升点所求凸包的下表面，"
        "恰好就是 scipy 的 Delaunay 三角剖分。",
    # ------------------------------------------------------------------ Incremental
    "Chapter eight. Random order and backwards analysis.": "第8章。随机顺序与反向分析。",
    "The simplest way to build a Delaunay triangulation":
        "构造 Delaunay 三角剖分最简单的方法是一次加一个点。<bookmark mark='a'/>这里是一个三角剖分，以及一个要插入的新点。先找到包含它的三角形。"
        "<bookmark mark='b'/>再找出所有空圆被新点破坏的三角形，即与它冲突的三角形。<bookmark mark='c'/>把它们全部移除，留下一个围绕新点的星形空洞，"
        "再把新点连到空洞的每个顶点。<bookmark mark='d'/>新三角形的个数就是新点的度。<bookmark mark='e'/>从包含该点的三角形出发做 Lawson 翻转，"
        "一次一条边地完成的正是这个变化。问题是整个插入序列的代价是多少。",
    "In a bad order, a single insertion can change almost everything":
        "在坏的顺序下，一次插入可能改变几乎一切：一个点到来时可能与之前的全部 i 个点相连，总代价就成了平方级。<bookmark mark='a'/>在随机顺序下，"
        "一个漂亮的论证表明不会如此。<bookmark mark='b'/>把算法倒过来运行。看插入 i 个点之后的三角剖分。因为顺序是随机的，最后插入的点等可能是现有 i "
        "个点中的任何一个。<bookmark mark='c'/>它的期望度就是三角剖分的平均度，即边数的两倍除以 i，<bookmark mark='d'/>而欧拉公式说平面三角剖分的"
        "边数少于三 i。<bookmark mark='e'/>所以平均度小于六，每次插入平均新建不到六个三角形，无论点是什么。<bookmark mark='f'/>找到每个点的位置期望"
        "花费 n log n，用同样的论证作用于冲突列表，这是 Kenneth Clarkson 与 Peter Shor 在1989年引入的。<bookmark mark='g'/>Raimund Seidel 给这个"
        "技巧取名为反向分析。它以完全相同的方式为随机化快速排序、树堆以及下一章的线性规划定价。",
    "We counted the triangles our incremental algorithm creates.":
        "我们统计了增量算法创建的三角形。<bookmark mark='a'/>在随机点、随机顺序下，每种规模都是大约每点九个，略低于九 n 加一的界，每点大约三次"
        "翻转。<bookmark mark='b'/>然后是一个特意构造的坏集合：一条又长又几乎平直的凸链，再加上它中间上方的点，自上而下插入，使每个新点都与整条链"
        "相连。按那个顺序，工作量呈平方增长：一千六百个点要创建八十七万个三角形。<bookmark mark='c'/>把同样的点打乱，又回到一万三千个，每点八个。"
        "打乱只需一行代码，而保证对每个输入都成立。",
    # ------------------------------------------------------------------ Lp
    "Chapter nine. Linear programming in the plane.": "第9章。平面上的线性规划。",
    "A linear program asks for the point of a convex region":
        "线性规划求的是凸区域中沿给定方向走得最远的点。<bookmark mark='a'/>在平面上，区域是半平面的交，方向是一个向量 c。第23部分为成千上万个维度"
        "构造单纯形法；在二维中，Raimund Seidel 1991年的算法只要十几行。<bookmark mark='b'/>按随机顺序一次加一个约束，保存目前所见约束的最优解。"
        "<bookmark mark='c'/>如果当前最优解满足新约束，什么都不变。<bookmark mark='d'/>如果违反了，新的最优解必定在新约束的直线上，在那里求它是一个"
        "一维问题：把这条直线与之前的约束相交，得到一个区间，取较好的一端。看：九个约束中，只有三个移动了最优解。",
    "How much does this cost?":
        "这要花多少？<bookmark mark='a'/>又是反向分析。加入 i 个约束之后，最优解是两条约束线相交的角点。第 i 个约束是这 i 个中随机的一个，只有当它是"
        "那两个之一时，最优解才会移动。<bookmark mark='b'/>这种情况的概率至多是二除以 i，代价是 i 的阶。求和，期望工作量是线性的。<bookmark "
        "mark='c'/>我们在多达十万个随机约束上运行它。最优解移动的次数大约正如两倍调和数所预测，十万个约束中移动了二十三次，一维工作的总量每个约束"
        "不到三步，且随 n 增大而减少。在 d 维中同样的算法需要 d 的阶乘乘以 n，而 Nimrod Megiddo 在1984年证明，对任何固定维度都可以确定性地做到线性"
        "时间。",
    "The same trick solves a different problem":
        "同样的技巧解决另一个问题：包含一组点的最小圆，即在哪里立一根天线能覆盖一批房屋。<bookmark mark='a'/>按随机顺序加入点。新点在当前圆内时，"
        "什么都不变；它落在圆外时，新的最小圆必定经过它。<bookmark mark='b'/>求那个圆是低一层的同一个问题，边界上固定一个点，然后两个。<bookmark "
        "mark='c'/>一个圆至多由三个点决定，所以反向分析表明第 i 个点打破它的概率至多是三除以 i。<bookmark mark='d'/>我们数了：十万个点只重建了"
        "二十九次圆，在自然对数的三倍之内，整个计算在 Python 中用了半秒。<bookmark mark='e'/>Emo Welzl 的算法期望线性时间，而 Megiddo 在1983年已找到"
        "一个确定性的。",
    # ------------------------------------------------------------------ KdTree
    "Chapter ten. Range searching.": "第10章。范围查询。",
    "A database of shops, each with a position":
        "一个商店数据库，每家商店有一个位置，被要求找出地图上一个矩形内的所有商店。检查每家商店是线性的；我们希望答案所需时间接近答案本身的大小。"
        "<bookmark mark='a'/>Jon Bentley 1975年的 kd 树先在 x 的中位数处分开点集，再在每一半的 y 中位数处分开，再在每个四分之一的 x 中位数处分开，"
        "交替进行，直到每个格子只含一个点。<bookmark mark='b'/>构造需要 n log n，空间是线性的。<bookmark mark='c'/>回答查询时，从根往下进入每个与矩形"
        "相交的格子，报告其中的点。<bookmark mark='d'/>这里查询访问了一百一十九个节点中的四十六个。<bookmark mark='e'/>为什么这么便宜？一条竖直线每"
        "两层只穿过一条路径上的格子，大约 n 的平方根个，所以查询代价是矩形边界的根号 n 加上报告的 k 个点。<bookmark mark='f'/>Bentley 是在斯坦福读"
        "本科时发明它的。",
    "We built kd-trees of up to three hundred thousand random points":
        "我们为多达三十万个随机点构造了 kd 树，对每棵树各做了四十次小正方形查询。<bookmark mark='a'/>访问数一直低于根号 n 加 k：三十万个点大约访问"
        "三百三十个节点，而扫描要看全部的点。<bookmark mark='b'/>平方根是线性空间的代价，而且随维度变差：在 d 维中 kd 树的查询代价是 n 的一减 d 分之一"
        "次方，这是给第十二章的一个警告。",
    "If we can afford more space, queries get faster.":
        "如果负担得起更多空间，查询就更快。<bookmark mark='a'/>范围树是一棵按 x 建的平衡树，每个节点还保存按 y 排序的点。<bookmark mark='b'/>它使用 "
        "n log n 的空间，回答用 log 平方 n 加 k。<bookmark mark='c'/>Bernard Chazelle 与 Leonidas Guibas 用分散层叠去掉了一个 log：每个有序列表保存"
        "指向其孩子列表的指针，于是根处的一次二分查找就能服务一整条向下的路径。<bookmark mark='d'/>区间树和线段树回答另一个常见问题：哪些存储的区间"
        "包含给定的点。<bookmark mark='e'/>数据库使用 R 树，它把相邻的矩形装进 B 树的页中；PostGIS、SQLite 的空间索引和大多数地图服务器的底层都是"
        "它。",
    # ------------------------------------------------------------------ PointLocation
    "Chapter eleven. Point location.": "第11章。点定位。",
    "Your phone knows its coordinates":
        "你的手机知道它的坐标；它在哪个国家、哪个县、哪个时区？<bookmark mark='a'/>地图是由 n 条线段对平面的划分，点定位问的是哪个面包含查询点。"
        "<bookmark mark='b'/>第一个快速的答案来自1976年的 David Dobkin 与 Richard Lipton：过每个端点画一条竖直线。在一个竖条内没有两条线段相交，所以"
        "它们从下到上是有序的。<bookmark mark='c'/>一次查询是两次二分查找：一次找竖条，一次找点正下方的线段。这是 log n 时间。<bookmark mark='d'/>"
        "麻烦在于空间：一条长线段穿过许多竖条，可能在每一个里都要存一次，最坏情况下是 n 的平方。",
    "The fix is to stop the walls early.":
        "解决办法是让墙早点停下。<bookmark mark='a'/>从每个端点向上、向下各画一堵墙，但只延伸到最近的线段。平面就分成了梯形。<bookmark mark='b'/>这七条"
        "线段构成二十二个梯形，<bookmark mark='c'/>这不是巧合：每个梯形的左边由一个端点决定；一个左端点至多为两个梯形扮演这个角色，一个右端点为一个，"
        "所以梯形永远不超过三 n 加一个。在五条、二十条和八十条线段的各二十张随机地图上，每一张都恰好达到这个界。<bookmark mark='d'/>为了快速查询，"
        "按随机顺序插入线段，并记录每个梯形是怎样被分开的，这是一个形如有向无环图的搜索结构。<bookmark mark='e'/>Ketan Mulmuley 和 Raimund Seidel "
        "证明它的期望大小是线性的，查询是对数时间。<bookmark mark='f'/>证明是第三次用到反向分析。David Kirkpatrick 在1983年用一层层越来越粗的三角剖分，"
        "确定性地达到了同样的界。",
    # ------------------------------------------------------------------ HighDim
    "Chapter twelve. High dimensions.": "第12章。高维空间。",
    "Everything so far lives in the plane":
        "到目前为止的一切都在平面上，但第十章和第十一章的问题也会对几百维的数据提出：图像、文档，以及 AI 系列中的嵌入向量。<bookmark mark='a'/>在那里，"
        "几何表现得很奇怪。在立方体中取两千个随机点，测量它们到一个随机查询点的距离。在二维中，最远的点比最近的远一百倍；在一百维中，不到一点五倍；在"
        "一千维中，只远百分之十一。几乎每个点都几乎同样远，“最近”几乎失去了意义。<bookmark mark='b'/>这毁掉了 kd 树。它的剪枝只在查询球比格子小时才"
        "有效。对两万个点，找一个最近邻在二维中访问万分之六的节点，十二维中访问一半，二十四维中每一个都要访问：比扫描还糟。<bookmark mark='c'/>高维中"
        "精确的最近邻似乎要么需要指数级空间，要么需要接近线性的时间，前沿一章会回到这个问题。",
    "Two ideas rescue nearest neighbours by giving up exactness.":
        "有两个想法以放弃精确为代价挽救了最近邻。第20部分的局部敏感哈希是其一：让相近的点倾向于碰撞。另一个，也是今天实践中占主导的，是图。<bookmark "
        "mark='a'/>把每个点连到它的几个近邻，选取时让它们指向不同的方向。<bookmark mark='b'/>回答查询时，从任意处出发，不断走向离查询点更近的那个邻居，"
        "同时保留一份所见最好者的短列表。<bookmark mark='c'/>Yury Malkov 与 Dmitry Yashunin 的分层版本在上面加了更稀疏的层，就像跳表的快车道：在顶部"
        "跳几次远的，再在底部仔细搜索。<bookmark mark='d'/>我们为十六维中的两万个点构造了一个，这些点聚集在两百个中心周围；它有四层。<bookmark "
        "mark='e'/>这些图没有最坏情况的定理，但向量数据库运行的正是它们，为语言模型的检索提供支持。",
    "Here is what the layers and the choice of links buy":
        "这是分层和链接的选择在一百个查询上带来的效果。<bookmark mark='a'/>暴力搜索对每个查询要计算全部两万个距离。<bookmark mark='b'/>只把每个点"
        "连到最近邻居的单层图在成簇的数据上表现很差：链接留在簇内，贪心搜索陷进错误的簇：用窄的束宽时它找到的真正近邻不到一半，即使最宽的束也要花六百"
        "多次计算。<bookmark mark='c'/>用 HNSW 的规则，只有当一个邻居离新点比离已保留的邻居都近时才保留它，于是链接向四面展开并跨越簇；分层图用不到"
        "两百次距离计算就找到了真正 10 个最近邻中的百分之九十九点七，是暴力搜索的百分之一。<bookmark mark='d'/>FAISS 和 pgvector 这样的程序库运行的"
        "正是这个，它们在为语言模型提供数据的检索系统之下。",
    # ------------------------------------------------------------------ Duality
    "Chapter thirteen. Duality and the ham sandwich.": "第13章。对偶与火腿三明治。",
    "Some of geometry's best tricks change what the objects are.":
        "几何中一些最好的技巧改变了对象本身。<bookmark mark='a'/>把点 a、b 映到直线 y 等于 a x 减 b。左边的每个点都变成右边一条同色的直线。<bookmark "
        "mark='b'/>现在取过其中两个点的直线：白色那条。它变成一个点，而那个点恰好就是两条对偶直线的交点。<bookmark mark='c'/>这个映射还保持上下关系："
        "在直线上方的点变成在点上方的直线。所以关于点及过它们的直线的问题，变成了关于直线及其交点的问题，而后者有时容易回答得多。",
    "Dual lines meet in arrangements.":
        "对偶直线相交构成排列。<bookmark mark='a'/>一般位置的 n 条直线把平面分成大约 n 平方除以二个面。<bookmark mark='b'/>区域定理说，一条新直线穿过"
        "的那些面的边界总共只有 n 阶条边，所以整个排列可以在 n 平方时间内增量构造。<bookmark mark='c'/>这能回答这样的问题：n 个点中有没有三点共线？做"
        "对偶，再问是否有三条对偶直线经过排列的同一个顶点。<bookmark mark='d'/>n 平方，而没有人知道怎样从根本上做得更快；前沿一章会解释这不是偶然。"
        "<bookmark mark='e'/>同样的对偶把一组点的凸包变成半平面的交，这也是 Voronoi 图是平面的上包络的原因。",
    "One more theorem with a sandwich in its name.":
        "再看一个名字里有三明治的定理。<bookmark mark='a'/>散布一些红点和蓝点。有没有一条直线能同时把两组都平分？<bookmark mark='b'/>总是有。Arthur "
        "Stone 与 John Tukey 在1942年证明，在 d 维中一个超平面可以同时平分任意 d 个集合：在三维中就是面包、火腿和奶酪。<bookmark mark='c'/>这里有九个"
        "红点和九个蓝点，一条直线两侧各有四个红点和四个蓝点，线上各一个。<bookmark mark='d'/>我们通过尝试过一个红点和一个蓝点的直线找到它；Lo、"
        "Matoušek 与 Steiger 把点对偶成直线并加以剪枝，在线性时间内找到它。<bookmark mark='e'/>这样的平分切割正是几何分治均匀分配工作的方式。",
    # ------------------------------------------------------------------ Planning
    "Chapter fourteen. Moving a robot.": "第14章。移动机器人。",
    "A robot must get from here to the star":
        "机器人必须从这里到达星形处而不碰到障碍物。让它是一个只能滑动、不能转动的三角形。<bookmark mark='a'/>Tomás Lozano-Pérez 与 Michael Wesley "
        "在1979年的技巧是改变移动的对象。让机器人贴着一个障碍物滑一圈，它的参考角就描出一个更大的形状：被机器人扩大了的障碍物，一个 Minkowski 和。"
        "<bookmark mark='b'/>对每个障碍物都这样做。<bookmark mark='c'/>现在机器人是一个点，即它的参考角，必须避开扩大后的障碍物。这就是构形空间。"
        "<bookmark mark='d'/>绕多边形的最短路径只在它们的角上转弯，所以把每对彼此可见的角连起来：可见性图。<bookmark mark='e'/>第18部分的 Dijkstra "
        "算法求出穿过它的最短路线，真正的三角形沿着它走，每次转弯都擦过障碍物。",
    "The visibility graph needs the corners of every obstacle":
        "可见性图需要每个障碍物的角，而在更高维中根本没有这样的东西可以列出。<bookmark mark='a'/>Steven LaValle 的快速探索随机树只需要一个碰撞"
        "测试。往空间里随机投一个点，找到树上最近的节点，朝那个随机点走一小步，如果没有碰到任何东西就保留这一步。<bookmark mark='b'/>树向空旷处蔓延，"
        "因为大片未探索的区域吸引最多的样本，长到一百三十七个节点时它到达了目标。<bookmark mark='c'/>它的路径不是最短的；绿色那条才是。<bookmark "
        "mark='d'/>二十次运行中每棵树都找到了路，平均比最优长约百分之三十。后来的变体如 RRT 星会不断重连这棵树，收敛到最短路径。<bookmark mark='e'/>"
        "用一点长度换来完全不需要几何，这个交易让采样成为机器人学的标准做法。",
    "Real robots turn.":
        "真实的机器人会转动。<bookmark mark='a'/>转动增加一个维度：平面上刚体的构形空间是三维的，而一条有七个关节的机械臂生活在七维中。<bookmark "
        "mark='b'/>John Reif 在1979年证明，一般的钢琴搬运工问题，即许多部件一起移动，是 PSPACE 难的。<bookmark mark='c'/>John Canny 找到了一个关于维度"
        "单指数的精确算法，这大约是所能期望的最好结果。<bookmark mark='d'/>实践中，规划器采用采样，用概率路线图和像我们刚刚生长的那种随机树，它们为"
        "工厂机械臂和自动驾驶汽车做规划。<bookmark mark='e'/>同样的基本操作用于游戏中的碰撞检测、为模拟构造网格，以及为光线追踪"
        "组织场景，第51部分会构造它。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen. Frontier: exactness, three-sum, and nearest neighbours.": "第15章。前沿：精确性、3SUM 与最近邻。",
    "The frontier has three fronts.":
        "前沿有三条战线。第一条正是这一部分开始的地方。<bookmark mark='a'/>Chee Yap 的精确几何计算范式说：精确地判定每个谓词，组合结构，比如哪些点在"
        "凸包上、哪些三角形是 Delaunay 的，就总是对的。<bookmark mark='b'/>精确性是有代价的。在几乎共线的点上，我们的有理数方向测试比浮点数慢大约一百二十"
        "倍。<bookmark mark='c'/>自适应过滤器只在答案可疑的地方付这个代价，CGAL、LEDA 和 Shewchuk 的 Triangle 网格生成器都是这样工作的。<bookmark "
        "mark='d'/>真正退化的输入，比如三个点恰好共线，可以假装这些点被无穷小量一致地扰动过来处理。<bookmark mark='e'/>仍然困难的是构造新点。两条线段的"
        "交点需要比端点更多的比特，再对结果求交就更糟，所以长串的构造会无限增长。吸附舍入以稍微移动物体为代价使它们保持很小，而在三维中怎样把这做好仍是"
        "开放问题。",
    "The second front is a wall.":
        "第二条战线是一堵墙。<bookmark mark='a'/>3SUM 问题：给定 n 个数，是否有三个加起来等于零？排序后用两个指针走一遍需要 n 平方。<bookmark mark='b'/>"
        "现在把每个数 a 提升为点 a、a 的立方。三个数之和为零，恰好当它们的三个点在一条直线上；代数上只是一次因式分解。<bookmark mark='c'/>我们在十四个数"
        "上核对了它：<bookmark mark='d'/>和为零的两个三元组恰好就是两个共线的三元组。<bookmark mark='e'/>所以共线性至少和 3SUM 一样难，而 Anka "
        "Gajentaan 与 Mark Overmars 在1995年证明了一整族平面问题都是如此：用带状区域覆盖、分隔线段、在线段之间规划运动。<bookmark mark='f'/>最好的 3SUM "
        "算法只比 n 平方快对数因子，而不存在真正次平方算法的猜想，已成为细粒度复杂性的基础，第27部分会构造它。",
    "The third front is the one chapter twelve left open.":
        "第三条战线是第十二章留下的问题。<bookmark mark='a'/>对高维中的精确最近邻，单元探测模型中的下界表明，没有索引能既小又快。<bookmark mark='b'/>"
        "对近似最近邻有一套精确的理论。局部敏感哈希用 n 的一除以 c 平方次方的时间回答 c 近似最近邻查询，而任何不看数据的哈希方案都无法做得更好。<bookmark "
        "mark='c'/>Alexandr Andoni 与 Ilya Razenshteyn 在2015年证明，适应数据的哈希做得更好，二 c 平方减一分之一，而这也是最优的。<bookmark mark='d'/>"
        "然而第十二章的图索引在实践中胜过所有这些方法，背后几乎没有理论；Piotr Indyk 与 Haike Xu 找到了一些输入，让某些流行的图需要线性时间。<bookmark "
        "mark='e'/>只对特殊的数据，即倍增维数低的数据，以及特殊的建图规则，才有保证。",
    "Here is where things stand.":
        "现状如下。<bookmark mark='a'/>3SUM 能在真正次平方的时间内解决吗？<bookmark mark='b'/>Hopcroft 问题：给定 n 个点和 n 条直线，是否有某个点在某条"
        "直线上？Jiří Matoušek 的算法大约需要 n 的三分之四次方，Jeff Erickson 证明这个界对一类自然的算法是最优的；对所有算法，没有人知道。<bookmark "
        "mark='c'/>可导航图为什么这么好用？为 HNSW 这类图在真实数据上证明一个界，或者找到一族能击败它们的输入，都还是开放问题。<bookmark mark='d'/>"
        "这一部分的研究题针对第三个问题。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们构造了：一个从不出错、几乎不花代价的方向测试。五个凸包算法，以及界住它们全部的、来自排序的归约。扫描线，以及美术馆的守卫。用 "
        "Fortune 扫描得到的 Voronoi 图，用翻转和随机插入得到的 Delaunay 三角剖分，以及把它们合而为一的抛物面。反向分析、线性规划、kd 树、点定位、"
        "高维中的可导航图，以及一个在障碍物间滑行的机器人。",
    "Where this comes back.":
        "它们会在哪里再出现。第23部分用单纯形法把线性规划带到多维。第27部分在 3SUM 之上构造细粒度复杂性。第47部分的搜索引擎加入嵌入向量上的向量搜索，"
        "用的是第十二章的图；第48部分在地图上提供最近邻查询。第51部分用方向测试绘制三角形，图形学称之为边函数，并在包围体层次结构中追踪光线。第52部分"
        "回到浮点数和实数计算。",
    "In practice. Geographic systems like PostGIS":
        "在实践中。PostGIS 和 Google 的 S2 库这样的地理系统运行在精确谓词、R 树和多边形叠加之上。CGAL 和 Shewchuk 的 Triangle 为模拟构造 Delaunay "
        "网格。每块显卡都用方向测试做光栅化，每个游戏都要检测碰撞。机器人规划器搜索构形空间，而每个向量数据库都在搜索一张可导航图。",
    "Six problems, with full solutions in the part's notes.":
        "六道题，完整解答在这一部分的笔记里。可以在任何一题上暂停。第五题是构造题：用 Pebble 语言写方向测试和单调链，在模拟器上运行。最后一题标有星号，"
        "是研究题：它的答案未知，笔记里说明了从哪里入手。",
    "Next time, optimization.":
        "下一次，优化。许多问题是在一个多面体中选出最好的点。单纯形法沿多面体的棱行走；对偶从另一侧证明答案。当整数性让问题变难时，松弛和随机超平面仍能"
        "可证明地逼近，而在线情形下，即使看不到未来，你仍然可以有竞争力。第23部分，优化。",
    "The books and papers this part follows":
        "这一部分所依据的书籍和论文显示在屏幕上，也列在笔记里。感谢观看。",
}

PHRASES = {}
