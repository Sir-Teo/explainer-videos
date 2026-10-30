"""Chinese narration for ai4: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).

Numbers from our own runs stay placeholders, so the Chinese follows the data when it changes; sentences chosen by a
result (``verdict``, ``tail``, ...) are translated as templates of their own and spliced in.  Terms follow
videos/ai/AI_ZH_GUIDE.md and, for calculus, the Analysis series (导数、切线、隐函数定理).
"""

TITLE = '人工智能，从零搭建 · 第4部分：变化'

CHAPTERS = {
    'Hook': '40亿个导数',
    'Derivative': '1. 导数',
    'Gradient': '2. 多个输入：梯度',
    'Jacobian': '3. 会弯曲的映射：雅可比矩阵',
    'Layers': '4. 真实网络层的雅可比矩阵',
    'Modes': '5. 向前，还是向后？',
    'Backprop': '6. 手算反向传播',
    'Library': '7. 几页代码里的微积分',
    'Train': '8. 用我们的库来训练',
    'Floats': '9. 计算机里的数',
    'GradCheck': '10. 抵消，以及梯度检验',
    'Memory': '11. 内存：存下来，还是重算',
    'Newton': '12. 曲率与牛顿法',
    'HVP': '13. 黑塞-向量积',
    'Quadratic': '14. 二次函数上的下降；鞍点',
    'Lagrange': '15. 约束：拉格朗日乘子',
    'KKT': '16. 不等式、KKT条件与对偶',
    'Implicit': '17. 穿过不动点求导',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In part one we worked out a single derivative by hand":
        "在第1部分，我们亲手算出了一个导数：意外度对各个分数的梯度，也就是模型的猜测，减去真相。<bookmark mark='a'/>GPT-2有1.24亿个数。Qwen3-4B有40亿个。<bookmark mark='b'/>训练的每一步，都需要损失对其中每一个数的导数，而这些导数，谁也不会去手算。",

    "The mathematics is three centuries older than the computers":
        "这些数学，比运行它的计算机早了整整三个世纪。1684年，莱布尼茨发表了微积分，而牛顿也有他自己的一套，叫作流数。<bookmark mark='a'/>1788年，拉格朗日说明了怎样在约束之下求最优，<bookmark mark='b'/>1847年，柯西提出了一路走下坡的方法。<bookmark mark='c'/>卡鲁什，后来还有库恩和塔克，又加上了不等式。<bookmark mark='d'/>然后有了程序：1964年，文格特让程序在计算数值的同时，带着导数一起算，<bookmark mark='e'/>1970年，林纳因马把链式法则倒过来运行。<bookmark mark='f'/>1985年，一项标准规定了计算机怎样舍入，<bookmark mark='g'/>1986年，反向传播让神经网络变得可以训练。<bookmark mark='h'/>从2010年起，软件库把这一切都自动做了，<bookmark mark='i'/>而今天一些最大的模型，训练时用的数只有8位长。",

    "This is Part 4 of AI, Built":
        "这是《人工智能，从零搭建》的第4部分：变化，也就是学习的微积分。<bookmark mark='a'/>本部分讲：导数是最好的直线近似，还有真实网络层的导数；<bookmark mark='b'/>运行链式法则的两种方式，并把代价数清楚；手算反向传播，再搭出我们自己的库，用它训练一个模型；<bookmark mark='c'/>计算机里的数会出什么问题；<bookmark mark='d'/>内存；<bookmark mark='e'/>曲率，从牛顿法讲到一个训练好的网络的地形；<bookmark mark='f'/>最后是带约束的优化，结尾讲怎样穿过一个方程的解来求导。",

    # ------------------------------------------------------------------ Derivative
    "Chapter one. The derivative.":
        "第1章。导数。",

    "Zoom in on a smooth curve":
        "把一条光滑的曲线放大，越凑越近，<bookmark mark='a'/>它就开始像一条直线了。<bookmark mark='b'/>这条直线的斜率就是导数：输入每有一点小小的变化，输出会跟着变化多少。",

    "Written down: f at x plus a small step h":
        "写成式子：f在x加上一小步h处的值，大约等于f在x处的值，加上导数乘以h。<bookmark mark='a'/>步子越小，这个估计就越准。导数，就是一个函数在某一点附近最好的直线描述。",

    'f"Here is the precise version.':
        "下面是精确的说法。一个函数在x处可导，是说有一个数，也就是导数，能让直线近似好到这个地步：它的误差比步长本身缩得更快。<bookmark mark='a'/>拿第1部分的意外度曲线来量一量。在这张对数坐标图上，用真实斜率时，误差下降的斜率是{d['slope']:.2f}：像h的平方那样。<bookmark mark='b'/>换一个只偏了百分之十的斜率，误差就只像h那样下降，斜率是{d['slope_bad']:.2f}。步长越来越小时，只有一条直线胜出。所谓最好，就是这个意思。<bookmark mark='c'/>这个想法属于莱布尼茨，他在1684年发表；也属于牛顿，他在17世纪60年代就已经想出来，叫它流数。",

    'f"Let\'s use the definition once':
        "我们用这个定义算一次，就算意外度：以2为底、p分之1的对数。<bookmark mark='a'/>走一步h带来的变化，是两个对数之差，<bookmark mark='b'/>也就是一个比值的对数。<bookmark mark='c'/>在1附近，对数就是它自己的切线：1加u的对数等于u，再加上一个比u更小的误差。<bookmark mark='d'/>所以h前面的那个数，是负的p乘以ln 2分之1。<bookmark mark='e'/>在四分之一处，它等于{d['d1']:.2f}比特每单位p：正是放大镜里看到的斜率。",

    "A few derivatives come up over and over.":
        "有几个导数会一再出现。<bookmark mark='a'/>指数函数的导数就是它自己。<bookmark mark='b'/>对数的导数是x分之1。正因为这样，p变小时，意外度才会升得那么陡。<bookmark mark='c'/>还有链式法则，用于复合函数：f(g(x))的意思是，先做g，再做f。把f的斜率记作f的导数，那么f(g(x))的导数，就等于f的导数在g(x)处的值，乘以g的导数在x处的值。变化穿过一层层复合，一路相乘。",

    # ------------------------------------------------------------------ Gradient
    "Chapter two. Many inputs.":
        "第2章。多个输入。",

    'f"A loss depends on many numbers at once.':
        "损失同时取决于很多个数。如果只有两个，它就是平面上方的一张曲面。<bookmark mark='a'/>轻轻推动其中一个数，另一个保持不动，就得到一个偏导数：沿那条坐标轴的斜率。<bookmark mark='b'/>在一点附近，对曲面最好的平面近似，是一个平面，也就是切平面，它按这两个斜率倾斜；它的误差像距离的平方那样下降，和直线时一样：实测斜率是{d['pslope']:.2f}。<bookmark mark='c'/>把这些斜率收进一个向量，就得到了梯度。它指向上坡，而且，我们马上会证明，是最陡的那个方向。<bookmark mark='d'/>所以，朝相反的方向一步又一步地走，你就会滑进山谷。",

    "Why steepest? Pick any direction":
        "为什么是最陡？任选一个方向，一个单位向量u，问问沿这个方向的斜率是多少。<bookmark mark='a'/>切平面给出了答案：沿u的斜率，等于梯度与u的点积。<bookmark mark='b'/>按第3部分的柯西–施瓦茨不等式，点积至多等于两个长度的乘积，而u的长度是1：没有哪个方向，上升得比梯度的长度更快。<bookmark mark='c'/>只有两个向量平行时，等号才成立。<bookmark mark='d'/>所以，梯度自己的方向是最陡的上坡，它的反方向是最陡的下坡，而与它垂直的方向，高度保持不变。",

    'f"Seen from above, the surface becomes a map':
        "从正上方看，这张曲面就变成一张等高线图，每条线都在同一个高度上。<bookmark mark='a'/>让一个方向绕着这一点转一圈，读出沿它的斜率。<bookmark mark='b'/>正对着梯度时，斜率最大；<bookmark mark='c'/>沿着等高线，斜率是0；<bookmark mark='d'/>背对着梯度，斜率最负。<bookmark mark='e'/>用有限差分在720个方向上实测，最陡的斜率是{d['dmax']:.4f}，梯度的长度是{d['gnorm']:.4f}，两个方向相差{off:.2f}度：{verdict}。",

    "Walking downhill this way is the oldest method":
        "这样一路走下坡，是本系列里最古老的方法。<bookmark mark='a'/>1847年，奥古斯丁–路易·柯西想解出一条轨道的方程组，就把它们写成一个平方和，并提出逆着它的梯度一步步走。<bookmark mark='b'/>用今天的写法：下一个点，等于当前的点，减去步长η乘以那里的梯度。<bookmark mark='c'/>步子该多大，多快能走到，取决于曲率，这要到第14章，再到第11部分去讲。",

    # ------------------------------------------------------------------ Jacobian
    "Chapter three. Maps that bend.":
        "第3章。会弯曲的映射。",

    "Now let a function take a whole vector":
        "现在，让一个函数把一整个向量变成另一个向量，就像网络的一层所做的那样。<bookmark mark='a'/>这个映射会把平面弄弯：网格线都弯曲了。<bookmark mark='b'/>但凑近任何一点放大，弯曲的线就变直了。凑近看，每个光滑的映射都像一个矩阵：它的雅可比矩阵，也就是它所有偏导数排成的表。",

    "In general, a map from n numbers to m numbers":
        "一般来说，一个把n个数映成m个数的映射，有一个m乘n的雅可比矩阵：每个输出一行，每个输入一列，正是让直线近似最好的那一个矩阵。梯度只是只有一个输出时的特例。<bookmark mark='a'/>雅可比矩阵的行列式，第3部分讲过，它说明这个映射在那一点附近，把面积拉伸了多少。<bookmark mark='b'/>而映射的链式法则，就是矩阵乘法：一个映射接着另一个映射，它的雅可比矩阵，就是两者雅可比矩阵的乘积，每一个都在它的输入所落到的那一点上求出。这个乘积，就是反向传播的全部，第5章会讲清楚。",

    # ------------------------------------------------------------------ Layers
    "Chapter four. The Jacobians of real layers.":
        "第4章。真实网络层的雅可比矩阵。",

    'f"Real layers first.':
        "先看真实的网络层。最常见的一种是矩阵乘法：输入X，每个词元一行，乘以权重W。<bookmark mark='a'/>第j行第k列的一个权重，只碰到输出的第k列，所以它的梯度，把从上面传来的梯度G，乘以它乘过的那些输入，收集起来。<bookmark mark='b'/>这个求和本身就是一次矩阵乘法：X的转置乘以G。<bookmark mark='c'/>而输入的梯度，也就是继续流向下一层的那个，是G乘以W的转置。<bookmark mark='d'/>注意我们从来没有写下的东西：雅可比矩阵本身。对GPT-2的一个矩阵，在{T:,}个词元上，它会有{d['jac_entries'] / 1000000000000.0:.1f}万亿个数。反向传播只需要它与G的乘积，代价和这一层向前算时差不多。",

    "Next, the softmax, which turns scores into probabilities.":
        "接下来是softmax，它把分数变成概率。<bookmark mark='a'/>用商的求导法则来求导。<bookmark mark='b'/>把分式拆开，每一项都是p i乘以δ i j，减去p i乘以p j。<bookmark mark='c'/>写成矩阵：对角线上是这些概率，再减去p与它自己的外积。<bookmark mark='d'/>这是5个分数的情形，算出来的结果，和我们的库完全一致。它的每一行加起来都是0，因为给每个分数都加上同一个数，什么也不会变；它是对称的，没有负的特征值，其中一个是0。<bookmark mark='e'/>同样，我们从来不需要这个矩阵本身：它与一个向量的乘积，只要n步，而不是n的平方步；GPT-2的词表有5万个词元，这一点就很要紧。再接上交叉熵，它就化成第1部分的q减去p。",

    'f"Last, layer norm':
        "最后是层归一化：减去向量的平均值，再除以它的散布。<bookmark mark='a'/>x一动，平均值和散布也跟着动，所以雅可比矩阵有两处修正：一个投影，去掉全是1的那个方向，另一个去掉y本身的方向，再整体除以σ。<bookmark mark='b'/>对6个数算出来，它有{n_zero}个特征值是0，只差一个极小的ε，其余的都相等：梯度穿过层归一化往回流时，会丢掉任何本来会改变向量平均值或整体大小的部分。而这些，正是这一层扔掉的东西。",

    # ------------------------------------------------------------------ Modes
    "Chapter five. Forwards, or backwards?":
        "第5章。向前，还是向后？",

    "There are two ways to use a Jacobian":
        "有两种办法，可以用上雅可比矩阵而不必把它写出来。把一个方向往前推：如果输入移动v，输出就移动J乘以v，这叫雅可比-向量积。或者把一份敏感度往回拉：如果输出按权重u计较，输入的影响就是u的转置乘以J，这叫向量-雅可比积。<bookmark mark='a'/>一个网络是一串映射，从它的参数θ，一直到损失，它的雅可比矩阵，是各环雅可比矩阵的乘积。<bookmark mark='b'/>雅可比-向量积从右边乘这个乘积，按网络运行的顺序：这是前向模式。<bookmark mark='c'/>向量-雅可比积从左边乘，从损失开始：这是反向模式。无论哪一种，都差不多是把网络走一遍。要得到整个雅可比矩阵，就得每个输入做一次雅可比-向量积，或者每个输出做一次向量-雅可比积。",

    '"Let\'s count.':
        "我们来数一数。这些网络有两个64宽的隐藏层，有n个输入、m个输出，从1到256。对每一个，数出两种模式为整个雅可比矩阵花掉的乘加次数，以向前走一遍为单位。<bookmark mark='a'/>前向模式要走n遍，不管m是多少。<bookmark mark='b'/>反向模式要走m遍，不管n是多少。输入少、输出多：向前走。输入多、输出少：向后走。<bookmark mark='c'/>再在这台计算机上计时，{tail}",

    "f'across the {total} networks where the counts differ, the cheaper mode by count was also the faster in every one.'":
        "在计数不同的{total}个网络里，按计数更便宜的那种模式，每一次也都更快。",

    "f'across the {total} networks where the counts differ, the cheaper mode by count was also the faster in {agree} of them.'":
        "在计数不同的{total}个网络里，按计数更便宜的那种模式，有{agree}次也更快。",

    'f"Training is the extreme case':
        "训练是最极端的情形：每个参数都是一个输入，而损失只是一个输出。<bookmark mark='a'/>向前走，你得带着一个矩阵，每个参数一列。<bookmark mark='b'/>向后走，只要带一行，大小就是你走到的那一层。<bookmark mark='c'/>我们的小分类器有{P}个参数。前向模式要把{P}个方向推过它：数一数，是一次反向传播乘加次数的{cr:.0f}倍。{timing}两种梯度完全一致。<bookmark mark='d'/>换成GPT-2，就是1.24亿遍对一遍。所以每个网络都用反向模式训练，而用在神经网络上，它叫作反向传播。",

    'f"Timed, it is {tr_:.0f} times slower: less than the count':
        "计时的话，它慢{tr_:.0f}倍：比计数少，因为计算机的额外开销，在小矩阵上占的比重最大。",

    "f'Timed, it is {tr_:.0f} times slower, much as the count says.'":
        "计时的话，它慢{tr_:.0f}倍，和计数差不多。",

    "Reverse mode was found more than once.":
        "反向模式不止被发现过一次。1970年，塞波·林纳因马在赫尔辛基的硕士论文里描述了它，用来算清舍入误差怎样在一个程序里层层累积。<bookmark mark='a'/>1974年，保罗·韦伯斯在他的博士论文里提出用它来训练网络，<bookmark mark='b'/>1986年，大卫·鲁梅尔哈特、杰弗里·辛顿和罗纳德·威廉姆斯在《自然》上展示了它的威力：网络能学会它们自己的内部表示。<bookmark mark='c'/>在那之前，控制工程师在1960年前后就用过同样的反向递推，为火箭规划最好的飞行路线。",

    # ------------------------------------------------------------------ Backprop
    "Chapter six. Backpropagation, by hand.":
        "第6章。手算反向传播。",

    "Let's run it by hand, on the smallest network":
        "我们来手算一遍，用的是最小的网络，画成一张由运算组成的流程图，叫作计算图，每个圆圈是一个节点。一个输入x，乘以一个权重，加上一个偏置，也就是一个平移；<bookmark mark='s'/>接着是一个挤压函数，sigmoid，一条S形曲线，能把任何数压进0到1之间；最后是一个平方误差：与目标y的差距，再取平方。<bookmark mark='a'/>先向前算：数值从左往右流动，最后得到损失，0.854。",

    "Now backwards. Start at the loss":
        "现在往回算。从损失出发，梯度是1，然后一步步往回走。<bookmark mark='a'/>每一步都把从右边传来的梯度，乘以它自己的局部导数，再把结果传给左边。<bookmark mark='b'/>到了权重这里，梯度是负0.259：把权重调高一点点，损失就会下降，降幅大约是这一点的四分之一。每一步除了自己的导数，什么都不需要知道。",

    "One more rule. When a value feeds into two places":
        "还有一条规则。当一个值同时流向两个地方，<bookmark mark='a'/>从这两处传回来的梯度，要加在一起。<bookmark mark='b'/>整个算法就是这些：按相反的顺序访问各个节点，让每个节点把它的梯度，传回给它的输入。",

    "Now a real network, in matrices":
        "现在换一个真正的网络，用矩阵来写：一个输入x，一层权重W1加上tanh，第二层，一个softmax，再接交叉熵。把对一层的激活前的量z的梯度，叫作这一层的δ，也就是那里的误差信号。<bookmark mark='a'/>在最上面，δ2就是第1部分的答案：预测的概率，减去独热编码的真相。<bookmark mark='b'/>W2里的每个权重，都把一个输入乘进一个输出，所以它的梯度，就是那个输出的δ乘以那个输入：一个外积，δ2乘以a1的转置。<bookmark mark='c'/>要往下走一层，就把δ拉回穿过W2，对矩阵来说，就是乘以它的转置，再穿过tanh，乘以它的斜率。<bookmark mark='d'/>然后同样的规则再用一次：W1的梯度，是δ1乘以x的转置。这四行，就是反向传播，不管网络有多深。",

    'f"Here is that outer product for one example':
        "这是一个样本的那个外积，算出来的结果：隐藏层的误差信号是一列，乘以输入这一行。<bookmark mark='a'/>结果的每一行，都是同一个输入的倍数，所以这个矩阵的秩是{n_nonzero}：一个奇异值，后面全是舍入误差。<bookmark mark='b'/>一个批次把{B}个这样的矩阵加起来，这里的秩达到{rank_b}，这是一个{dh}乘{din}的矩阵所能有的最大秩。这种低秩结构，到第27部分用低秩适配器微调模型时还会出现。<bookmark mark='c'/>而这些手推出来的梯度，和我们的库、和PyTorch都一致，一直到计算机保留的最后几位。",

    # ------------------------------------------------------------------ Library
    "Chapter seven. The machine, in code.":
        "第7章。用代码写出这台机器。",

    'f"Here it is in code':
        "这就是它的代码：本系列自己的自动微分，一共大约{n_lines}行。<bookmark mark='a'/>每个运算都记住它的输入，还附带一个小函数，负责把梯度传回给每个输入。这是乘法：一个输入得到的梯度，等于传进来的梯度，乘以另一个输入。<bookmark mark='b'/>而backward函数按相反的顺序遍历这张图，把到达每个节点的梯度加起来，再继续往回传。",

    'f"Does it work?':
        "它管用吗？<bookmark mark='a'/>把每个数推动百万分之一，测一测损失变了多少，再拿来比较：两种梯度直到小数点后{fd_digits}位都一致，第10章会说明，推一下最多也只能告诉你这么多。<bookmark mark='b'/>再和PyTorch比，当今大多数模型都是用这个库训练的：两者一致到小数点后{pt_digits}位，这已经是计算机自身算术精度的极限。",

    "Backward needs an order":
        "反向计算需要一个顺序：一个节点，只有在它的每一个用处都报告回来之后，才能把梯度传下去。在图里做一次深度优先搜索，正好给出这样的顺序，叫作拓扑顺序，每个节点都排在它的输入之后。这是第6章的例子，由我们的库按这个顺序编了号。<bookmark mark='a'/>写出来，这张图就是一张列表，每一行是对前面几行做的一个基本运算。1964年，文格特就让程序保存这样的列表，让导数跟着数值一起算；今天的工具，把这份记录叫作磁带。<bookmark mark='b'/>向前时，数值沿着列表往下走。<bookmark mark='c'/>向后时，列表从底下往上走，每一行都把梯度送回给它用过的那几行。",

    "Ours is the smallest member of a long family.":
        "我们的库，是一个大家族里最小的成员。<bookmark mark='a'/>1980年，伯特·斯皮尔彭宁从普通程序里编译出了反向模式。<bookmark mark='b'/>2010年，来自蒙特利尔的Theano，要你先声明一张图，再把它连同梯度一起编译。<bookmark mark='c'/>2015年，Chainer在代码运行时记录这张图，叫作边运行边定义，而TensorFlow保留了一张静态图。<bookmark mark='d'/>2017年，PyTorch在GPU上做边运行边定义，就像我们的库在CPU上那样，<bookmark mark='e'/>2018年，JAX追踪整个函数，再对它做变换：求梯度、两种乘积、编译、批处理。<bookmark mark='f'/>三者里，你要写的那一行几乎一样。",

    # ------------------------------------------------------------------ Train
    "Chapter eight. Training with our library.":
        "第8章。用我们的库来训练。",

    "Before we train, look at the first gradient.":
        "训练之前，先看第一个梯度。把平均意外度对一个分数z i j求导：每一对以i开头的字母，都贡献它的猜测减去它的真相。<bookmark mark='a'/>收集起来，就是以i开头的字母对所占的比例，乘以第1部分的q减去p帽：模型的概率，减去数出来的概率。<bookmark mark='b'/>一开始，每个猜测都是27分之1。<bookmark mark='c'/>在这些书上算出来，库给出的梯度和这个公式完全一致，而推得最用力的，红色的那些，是最常见的字母对。梯度下降就是计数，只不过一点一点地数。",

    "Now let's use it. In part one, counting letter pairs":
        "现在来用它。在第1部分，统计字母对，让我们做到了每个字母3.33比特。<bookmark mark='a'/>这一次，什么都不数。模型有729个可调的分数，每一对字母一个，全都从0开始，由我们的库在那些书上，用梯度下降来训练。<bookmark mark='w'/>下方是这些分数写出的文字，每一步都用同样的骰子来抽：眼下，还只是噪声。",

    "The loss falls fast, then settles":
        "损失先是快速下降，然后稳定下来：停在3.33比特，正是计数得到的答案。<bookmark mark='a'/>而这些分数本身，也变成了计数的对数。这又是最大似然，只不过这次是一路下山走到的，而不是数出来的。<bookmark mark='b'/>同样的这个循环，换上更多的数、更好的模型，就能训练本系列里其余的一切。",

    # ------------------------------------------------------------------ Floats
    "Chapter nine. Numbers in a computer.":
        "第9章。计算机里的数。",

    "Every number in this series so far has been a float.":
        "到目前为止，本系列里的每一个数都是浮点数。1985年，一项标准，IEEE 754，主要由威廉·卡亨设计，规定了计算机怎样存储和舍入它们，好让每台机器都给出同样的答案。<bookmark mark='a'/>一个浮点数由符号位、指数和尾数组成：1点几的尾数，乘以2的指数次方。指数位换来范围，尾数位换来精度。<bookmark mark='b'/>FP32有8位指数、23位尾数。BF16保留了FP32的8位指数，尾数只有7位；FP16是5位和10位；而2022年的8位格式，是4位和3位，或者5位和2位。",

    'f"The gap between neighbouring floats':
        "相邻两个浮点数之间的间隔，叫作最后一位单位，它随着数本身一起增大：一级级台阶，每个2的幂一级。所以相对精度处处都一样：FP32大约有{info['fp32']['digits']:.1f}位十进制有效数字，BF16只有{info['bf16']['digits']:.1f}位。<bookmark mark='a'/>每种格式都有尽头。FP16到{info['fp16']['max']:,.0f}为止，4位指数的FP8到{info['e4m3']['max']:,.0f}为止，而BF16能和FP32走得一样远。正因为如此，BF16，谷歌为它的TPU设计的格式，训练时不需要FP16所需的损失缩放。硬件在第17部分讲，而把模型压进更少的位数，在第19部分讲。",

    'f"Rounding has consequences.':
        "舍入是有后果的。在BF16里，1加上256分之1还是1，257变成了256。就连0.1，在FP32里也不是0.1。<bookmark mark='a'/>把0.01加一万次；答案应该是100。<bookmark mark='b'/>FP32得到{ends['fp32']:.3f}。<bookmark mark='c'/>FP16卡在{ends['fp16']:g}，BF16卡在{ends['bf16']:g}：一旦和变得足够大，相邻浮点数的间隔就超过0.01的两倍，每加一次，都会被舍入回原处。<bookmark mark='d'/>如果数用BF16，而和用FP32来累加，就像GPU的矩阵单元那样，你会得到{ends['bf16_fp32acc']:.2f}，因为0.01本身被舍入成了{tenth:.6f}。",

    'f"Range has consequences too.':
        "范围也是有后果的。softmax要对分数取指数，而e的{math.ceil(ov['fp32'])}次方，对FP32来说就已经太大了；在FP16里，e的{ov['fp16']:.1f}次方就已经溢出。<bookmark mark='a'/>于是，1000、999和998这三个分数，都变成了无穷大，概率则变成了非数，NaN。<bookmark mark='b'/>办法是先减去最大的那个分数。指数之和的对数，等于最大值，<bookmark mark='c'/>加上另一个和的对数，而那个和里，每个指数都不超过0。<bookmark mark='d'/>什么都不会溢出，而最大的那一项恰好是1，所以和也不会变成0。<bookmark mark='e'/>同样这三个分数，现在给出了干净的概率，而我们库里的log-softmax，在第一行做的正是这件事。",

    # ------------------------------------------------------------------ GradCheck
    "Chapter ten. Cancellation, and the gradient check.":
        "第10章。抵消，以及梯度检验。",

    "One more way numbers go wrong":
        "数还有一种出错的方式，而它恰好说明了该怎样检验梯度。看1减cos x，再除以x的平方：x很小时，它非常接近二分之一。<bookmark mark='a'/>照原样在FP32里计算，x越小，误差就越是爆炸，<bookmark mark='b'/>到了x等于10的负4次方，cos x被舍入成恰好是1，答案成了0。<bookmark mark='c'/>这就是抵消：两个几乎相等的数相减，保留了它们的舍入误差，却丢掉了它们的大小，所以相对误差像x的平方分之1那样增长，正如预测的那样。FP64只是把它推迟了。<bookmark mark='d'/>换一种不做减法的写法，同一个式子在哪里都很准。",

    "A gradient check is a cancellation on purpose.":
        "梯度检验，就是故意制造的一次抵消。用泰勒定理，把f在x两边各展开一步。<bookmark mark='a'/>相减再除以2h：偶数次的项抵消了，剩下导数，加上一个截断误差，它像h的平方那样缩小。<bookmark mark='b'/>可是f的每个值都被舍入过，误差大约是u乘以f，u是单位舍入误差，而这次相减保留了这些误差，又除以一个很小的2h：于是舍入误差像h分之1那样增长。<bookmark mark='c'/>把两者加起来，<bookmark mark='d'/>令导数为0：最好的步长，是3乘以u乘以f、再除以三阶导数的立方根。步子太大，泰勒的误差占上风；太小，舍入误差占上风。",

    'f"Here it is measured':
        "这是实测的结果，用的是第7章的网络，沿8个随机方向，两种精度都有。<bookmark mark='a'/>在FP64里，误差从右边像h的平方那样下降，斜率是{d['slope_right_fp64']:.2f}，直到舍入误差接手，它又像h分之1那样回升。一个V字。<bookmark mark='b'/>在FP32里，同样的V字高得多，也更靠右。<bookmark mark='c'/>两个底，都落在公式说的地方：{verdict}。<bookmark mark='d'/>在最好的时候，FP64的检验能准到{mant(e64)}乘以10的负{expo(e64)}次方；FP32只能准到{mant(e32)}乘以10的负{expo(e32)}次方。所以要用FP64来检验梯度，步长取在单位舍入误差的立方根附近。第7章推动百万分之一，已经很接近了：那里的误差大约是{mant(e6)}乘以10的负{expo(e6)}次方。",

    "both within a factor of three of the prediction":
        "两者都在预测值的3倍之内",

    "the right order of magnitude, if not closer":
        "至少数量级是对的",

    # ------------------------------------------------------------------ Memory
    "Chapter eleven. Memory.":
        "第11章。内存。",

    "Reverse mode has a price, and it is memory.":
        "反向模式是有代价的，代价就是内存。<bookmark mark='a'/>向前走时，每一层的输出都必须留着，<bookmark mark='b'/>因为往回走时，每一步都要用到它：一层的雅可比矩阵取决于它的输入。<bookmark mark='c'/>只有等反向计算走到某一层，它的激活才能释放。所以内存随深度增长，也随批量和宽度增长；训练大模型时，把GPU塞满的，是激活，而不是权重，这是第18部分的问题。",

    "The way out is to trade memory for time.":
        "出路是用时间换内存。<bookmark mark='a'/>每隔k层只留一个输出，叫作检查点；反向计算走到某一段时，就从那一段的检查点出发，把这一段重新向前算一遍，只在需要的时候留着它的k个输出。<bookmark mark='b'/>内存等于n除以k个检查点，再加上一段的k个。<bookmark mark='c'/>它在斜率为0的地方最小，<bookmark mark='d'/>也就是k等于n的平方根时，这时内存是2倍的根号n，而不是n。<bookmark mark='e'/>代价是：每一段都要重算一次，大约多出一次向前计算。陈天奇和同事们在2016年把它用到了深度网络上；而安德烈亚斯·格里万克在1992年就已证明，递归地设置检查点，能把两种代价都降到对数级。",

    'f"Measured, on a chain of {n} layers.':
        "在一条{n}层的链上实测。<bookmark mark='a'/>同时保留的激活最多有多少，跟着n除以k再加k走：全部保留时是{int(peak[0])}个，最低点是{int(peak.min())}个，底部从k等于{lo}到{hi}都是平的，{verdict}。<bookmark mark='b'/>代价体现在计算次数上：全部保留时，向前算{int(evals[0])}层，用检查点时{int(evals[k_rt])}层，而什么都不留、每个输入都从头重算时，要{int(d['none_evals']):,}层。<bookmark mark='c'/>{scaling}在一条更深更宽的链上计时，检查点花的时间是原来的{ratio:.2f}倍，而每种做法得到的梯度，一位不差。",

    "f'and the square root of {n}, {rt}, is among them'":
        "而{n}的平方根{rt}，就在其中",

    "f'which is near the square root of {n}, {rt}, if not on it'":
        "就算不正好在{n}的平方根{rt}上，也离它很近",

    "On longer chains the best interval keeps tracking the square root.":
        "在更长的链上，最好的间隔一直跟着平方根走。",

    "On longer chains the best interval stays close to the square root.":
        "在更长的链上，最好的间隔一直离平方根不远。",

    # ------------------------------------------------------------------ Newton
    "Chapter twelve. Curvature.":
        "第12章。曲率。",

    "The gradient says which way is downhill.":
        "梯度告诉你哪边是下坡，却没告诉你，斜率本身在怎样变化。<bookmark mark='a'/>那是二阶导数，曲率。有多个输入时，它是一个由二阶导数组成的矩阵，叫作黑塞矩阵。<bookmark mark='b'/>它是对称的，所以按第3部分讲的，它有互相垂直的特征向量，也就是纯粹弯曲的方向，而它的特征值，说明曲面沿每个方向弯得有多厉害。<bookmark mark='c'/>两个都为正：是一个碗。一个为负：是一个鞍点，一个方向下坡，另一个方向上坡，第14章会专门讲它。",

    "The Hessian gives a better step.":
        "黑塞矩阵能给出更好的一步。一阶导数给出了最好的直线；加上二阶导数，就是最好的二次曲面。<bookmark mark='a'/>直接跳到这个二次曲面的最低点，也就是它的梯度为0的地方：<bookmark mark='b'/>这一步，等于负的H的逆乘以梯度。这就是牛顿法。<bookmark mark='c'/>1669年，牛顿用这个想法求方程的根，1690年，拉夫森把它简化，1740年，托马斯·辛普森把它推广到多个变量，并用来求最小值。",

    'f"A test: logistic regression':
        "做个测试：逻辑回归，第6部分会搭建的一种分类器，它有两个高度相关的特征，以至于曲率在两个方向上相差{d['kappa']:.0f}倍。<bookmark mark='a'/>梯度下降用的是永远安全的最大步长，它沿着山谷来回折返，要走{steps:,}步，才能离最小值不到10的负10次方。<bookmark mark='b'/>牛顿法只要{nsteps}步。<bookmark mark='c'/>数一数每一步之后它正确的位数：{d1}，然后{d2}，然后{d3}，{verdict}。<bookmark mark='d'/>麻烦在于黑塞矩阵本身：每一步都要用它解一个线性方程组，而对十亿个参数来说，它会有十亿的平方个元素。下一章会讲，怎样用上曲率，却从来不把它造出来。",

    # ------------------------------------------------------------------ HVP
    "Chapter thirteen. Curvature without the Hessian.":
        "第13章。不用黑塞矩阵的曲率。",

    "A Hessian with a billion rows is out of reach":
        "一个有十亿行的黑塞矩阵，是够不着的，但它与一个向量的乘积，却不是。<bookmark mark='a'/>H乘以v，就是沿着v移动时，梯度怎样变化。<bookmark mark='b'/>既然v是固定的，这就是一个数的梯度，也就是梯度与v的点积的梯度。<bookmark mark='c'/>而一个数的梯度，正是反向模式最擅长、最便宜的事：再运行它一次，穿过计算梯度本身的那些步骤，就能精确地得到H乘以v，代价只是一次梯度的几倍。巴拉克·珀尔马特在1994年发表了这个技巧。",

    'f"Check it on a small network':
        "在一个小网络上检验一下，我们马上就会见到它。<bookmark mark='a'/>与按笨办法造出来的完整黑塞矩阵相比，珀尔马特的乘积一致到舍入误差，而代价相当于{ratio:.1f}次梯度。<bookmark mark='b'/>对梯度做有限差分，又会画出一个V字，就像第10章那样，最好的时候误差是{mant(e)}乘以10的负{expo(e)}次方。<bookmark mark='c'/>而要了解曲率，有乘积就够了：拿一个向量反复乘以H，每次都重新归一化，它就会转向最陡的方向。对最大特征值的估计，收敛到了真实值。",

    'f"Now watch a landscape change':
        "现在来看，一个网络学习时，地形怎样变化。三条交错的螺旋，一个有{P}个参数的网络，以及它完整的黑塞矩阵，在训练中的{K}个时刻算出来。<bookmark mark='a'/>一开始，特征值向两边散开：起点在很多个方向上都是鞍点。<bookmark mark='b'/>随着网络拟合这些螺旋，负的曲率慢慢消失，{neg_v}。<bookmark mark='c'/>到最后，{out_v}，而有百分之{flat_end:.0f}的特征值在最大值的百分之一以内：一大团几乎平坦的方向，加上少数几个陡峭的方向，这正是莱文特·萨贡和同事们在2016年对真实网络报告的形状。而随着损失趋于0，整个谱也跟着缩小。",

    "f'from {neg0} clearly negative eigenvalues at the start to {negK}'":
        "从开始时{neg0}个明显为负的特征值，降到{negK}个",

    "f'{neg0} clearly negative eigenvalues at the start and {negK} at the end'":
        "开始时有{neg0}个明显为负的特征值，结束时有{negK}个",

    "f'{out_end} eigenvalues stand out above a tenth of the largest'":
        "有{out_end}个特征值，超过最大值的十分之一，显得很突出",

    # ------------------------------------------------------------------ Quadratic
    "Chapter fourteen. How fast is downhill?":
        "第14章。下山能有多快？",

    "Near a minimum every smooth loss looks like a quadratic bowl":
        "在最小值附近，每个光滑的损失看起来都像一个二次的碗，而在碗上，梯度下降可以精确地解出来。<bookmark mark='a'/>每一步都把位置乘以I减去η乘以H。<bookmark mark='b'/>在黑塞矩阵的特征向量下，这个矩阵是对角的，所以每个坐标各自缩小，缩小的倍数是1减去η乘以它的特征值。<bookmark mark='c'/>每个倍数的绝对值都必须小于1，所以步长必须小于2除以最大的曲率。<bookmark mark='d'/>而最慢的那个坐标决定了速度。最好的步长让两个极端互相平衡，速率是κ减1除以κ加1，其中κ，也就是条件数，是最大曲率与最小曲率之比。",

    'f"Here is a valley with kappa of twenty-five':
        "这是一个κ等于25的山谷：横向的弯曲程度是纵向的25倍。<bookmark mark='a'/>最陡的下坡方向，大多指向对面的谷壁，于是每一步都在两边谷壁之间来回折返，沿着谷底慢慢往前爬：要{v['gd_steps_to_1pct']}步，才能进到百分之一以内。<bookmark mark='b'/>动量把速度从一步带到下一步，效果更好，第11部分会推导原因。<bookmark mark='c'/>牛顿法的一步抵消了曲率，一下子就落到谷底。",

    'f"Measured on bowls from kappa of one to a thousand':
        "在κ从1到1000的碗上实测：橙色的速率，{verdict}。<bookmark mark='a'/>而所需的步数与κ成正比：在κ等于{k_big:,}时，把误差缩小一百万倍，要走{int(so[-1]):,}步。<bookmark mark='b'/>步长一旦超过2除以最大曲率，山谷里的步子就会越走越大，而不是越走越小，这里是从η等于{edge:.3f}开始。真实的损失并不是二次函数，但这正是每一条学习率规则背后的微积分，第11部分会在它的基础上搭建更快的方法。",

    'f"Saddles are where descent stalls.':
        "鞍点，是下降停滞的地方。这张曲面的中央有一个鞍点，上下各有一个最小值。<bookmark mark='a'/>从几乎正好在穿过鞍点的那条线上出发，只偏开一个很小的距离y0。这一路先滑向鞍点，那里的梯度几乎为0，于是就在那里等着，直到那一点点偏移长到足够大，才掉下去。<bookmark mark='b'/>在鞍点附近，偏移每一步都乘以1加η，所以等待的时间随着y0分之1的对数增长：实测，每差10倍，要多走{slope:.1f}步，{verdict}。<bookmark mark='c'/>如果正好从那条线上出发，它就永远走不开：梯度降到{mant(sg)}乘以10的负{expo(sg)}次方，而那一点并不是最小值。只有黑塞矩阵，凭它那个负的特征值，才分得出两者。实际训练中，随机梯度的噪声会把网络踢开；扬·多芬和同事们在2014年指出，在高维空间里，拖慢训练的主要是鞍点，而不是糟糕的极小值。",

    # ------------------------------------------------------------------ Lagrange
    "Chapter fifteen. Optimizing under constraints.":
        "第15章。在约束之下求最优。",

    "Often the numbers aren't free":
        "很多时候，这些数并不是自由的：概率加起来必须是1，预算不能超支。这里，要把f最小化，它的等高线是这些椭圆，但只能在这个圆上取值。<bookmark mark='a'/>沿着圆走，看两个箭头：f的梯度，和约束的梯度，后者笔直地指向圆外。<bookmark mark='b'/>只要f的梯度沿着圆有一个分量，你就能往那边滑，走得更低。<bookmark mark='c'/>所以在带约束的最小值处，那个分量是0：两个梯度互相平行。<bookmark mark='d'/>1788年，约瑟夫–路易·拉格朗日在他的《分析力学》里，把这幅图变成了一种方法。",

    'f"Write it down: at the constrained minimum':
        "写下来：在带约束的最小值处，f的梯度是约束梯度的一个倍数，等于负λ乘以它。<bookmark mark='a'/>拉格朗日的办法，是把约束并进一个函数，叫作拉格朗日函数，f加上λ乘以g，<bookmark mark='b'/>它在x和λ一起看时的普通驻点，恰好就是带约束的那些点：对λ求导，正好给回约束本身。<bookmark mark='c'/>对这个圆，乘子算出来是{d['lam']:.3f}。它是一个价格：约束稍微放松一点，最优值会下降得多快。",

    'f"A famous constrained problem':
        "一个著名的带约束问题：一个骰子，平均点数是4.5，而不是3.5。哪组概率，在这之外假设得最少？熵最大的那一组。<bookmark mark='a'/>让拉格朗日函数的导数为0，每个约束一个乘子，<bookmark mark='b'/>答案就是一个softmax：每一面的概率，是e的β乘以点数次方，再归一化。<bookmark mark='c'/>算出来，β等于{d['beta']:.3f}，而一个通用的求解器，落在同样的六个数上。埃德温·杰恩斯在1957年把它变成了一条推断原则。softmax就是从这里来的：它是平均分数固定时熵最大的分布，而它的温度，就是一个拉格朗日乘子。",

    "The same algebra gives reinforcement learning":
        "同样的代数，给了强化学习一个闭式解。把期望奖励，减去β乘以与参考策略之间的KL散度，最大化。<bookmark mark='a'/>再加上概率之和为1的约束，最好的策略，就是参考策略，按e的奖励除以β次方重新加权。<bookmark mark='b'/>这里是6个动作的情形，算出来，又用求解器核对过。第27部分的直接偏好优化，就是从这个公式出发的。",

    # ------------------------------------------------------------------ KKT
    "Chapter sixteen. Inequalities, and duality.":
        "第16章。不等式，以及对偶。",

    "Most constraints are inequalities":
        "大多数约束都是不等式：概率不能为负，间隔至少要有1。威廉·卡鲁什在他1939年的硕士论文里推出了这些条件；1951年，哈罗德·库恩和阿尔伯特·塔克又重新找到了它们。<bookmark mark='a'/>在最小值处，存在一组乘子μ，每个约束一个，使拉格朗日函数的梯度为0，每个约束都满足，每个乘子都不为负，<bookmark mark='b'/>而且每个乘子与它的约束的乘积都等于0：这叫互补松弛。<bookmark mark='c'/>要么最小值在里面，墙闲着，它的乘子是0，<bookmark mark='d'/>要么最小值在墙上，而乘子衡量墙推回来有多用力。",

    "The multipliers lead to a second problem.":
        "这些乘子引出了第二个问题。把它们固定住，对x自由地把拉格朗日函数最小化：这就是对偶函数，q(μ)。<bookmark mark='a'/>对任何可行的x，加上去的那些项都不超过0，所以对偶函数是f的一个下界，在所有能取到的地方都成立。<bookmark mark='b'/>最好的下界d星，至多等于真正的最小值p星：这叫弱对偶，对每个问题都成立。<bookmark mark='c'/>对有严格可行点的凸问题，两者相等：这叫强对偶。你可以解其中任何一个。",

    'f"Two small examples.':
        "两个小例子。把x的平方最小化，同时要求x至少为1。它的对偶函数是一个鼓包，升上去，正好碰到真正的最小值1：没有间隙。<bookmark mark='a'/>再看一个双势阱，同样的约束，但不是凸的。对偶的最好值是{d['nc_d']:.2f}，低于真正的最小值{d['nc_p']:.2f}：对偶间隙是{d['nc_gap']:.2f}。下界依然成立，只是不再紧了。",

    'f"Duality\'s most famous use':
        "对偶最著名的用处，是第6部分的支持向量机。在两个类别之间找出最宽的街道：最小的w，让每个点离这条线都至少有一个单位的间隔。<bookmark mark='a'/>它的对偶问题，每个点一个乘子，而且只通过点与点之间的点积依赖于这些点，核方法正是由此进来的。<bookmark mark='b'/>我们在20个点上把两个问题分别解了一遍：两个最优值{gap_word}。<bookmark mark='c'/>而互补松弛挑出了支持向量：只有{len(sv)}个乘子不为0，恰好对应街道边缘上的{len(sv)}个点。1992年，伯恩哈德·博泽、伊莎贝尔·居永和弗拉基米尔·瓦普尼克，正是在这个对偶问题上建立了这种方法。",

    # ------------------------------------------------------------------ Implicit
    "Chapter seventeen. Differentiating through an equation.":
        "第17章。穿过一个方程求导。",

    "Some layers aren't a fixed list of steps.":
        "有些层，并不是一串固定的步骤。深度平衡层把它的输出反复送回自己，直到不再变化：它的输出是不动点z星，满足z星等于f(z星, θ)。怎样穿过它做反向传播？<bookmark mark='a'/>对方程两边求导。<bookmark mark='b'/>把各项归拢：解的导数，等于I减J的逆，乘以直接的导数，只要这个逆存在，这就是隐函数定理。<bookmark mark='c'/>对一个损失，把它当作向量-雅可比积来算：在不动点上解一个线性方程组，不管走到那里用了多少次迭代，一路上什么都不用存。",

    'f"Check it on a tiny equilibrium layer':
        "在一个只有8个数的小平衡层上检验一下。<bookmark mark='a'/>通常的另一种做法是展开：迭代K次，再用我们的库，穿过所有这些迭代做反向传播。随着K增大，这个梯度以几何速度逼近隐式的梯度，<bookmark mark='b'/>每一步缩小到{d['rate']:.3f}倍，{verdict}，直到降到{mant(floor)}乘以10的负{expo(floor)}次方，也就是不动点本身的精度。<bookmark mark='c'/>展开要存下每一次迭代；隐式的梯度只需要答案。",

    "close to the spectral radius of J, as the theory says it should be":
        "和J的谱半径很接近，正如理论所说",

    "roughly doubling each step: quadratic convergence":
        "每一步大约翻一倍：这是二次收敛",

    "slower than the spectral radius alone would suggest":
        "比单看谱半径所预期的要慢",

    'f"And it trains.':
        "而且它能训练。一个有{int(d['d'])}个数的深度平衡模型，学着拟合这条曲线，每个梯度都是隐式算出来的，它的反馈矩阵始终保持为压缩映射。<bookmark mark='a'/>拟合越来越准，损失从{d['first_loss']:.3f}降到大约{mant(d['final_loss'])}乘以10的负{expo(d['final_loss'])}次方，{it_v}。<bookmark mark='b'/>白少杰、济科·科尔特和弗拉德连·科尔顿在2019年提出了这类模型。同样的技巧，也能穿过一个内层优化求导，比如元学习，或者穿过一个被当作网络层的求解器：凡是答案由一个方程而不是一份步骤定义的地方，都用得上。",

    "f'and the equilibrium takes longer to reach as it learns":
        "而且它学得越多，达到平衡要花的时间就越长，一开始要{it[0, 1]:.0f}次迭代，最后要{it[-1, 1]:.0f}次",

    "f'and the equilibrium takes {it[0, 1]:.0f} iterations":
        "而达到平衡，一开始要{it[0, 1]:.0f}次迭代，最后要{it[-1, 1]:.0f}次",

    # ------------------------------------------------------------------ Outro
    "Let's take stock. A derivative is the best straight line":
        "我们来盘点一下。导数是最好的直线，它的误差比步长缩得更快；梯度是最陡的方向，这由柯西–施瓦茨不等式保证；雅可比矩阵是最好的矩阵，而真实网络层的雅可比矩阵从来不造出来，只拿来做乘法。前向模式按输入付代价，反向模式按输出付代价，所以训练是倒着走的：反向传播，它给出的权重梯度，是误差信号与输入的外积。我们搭出了它，检验了它，还用它训练了模型。浮点数会舍入、会抵消，所以softmax要先减去最大值，梯度检验要挑好步长。检查点在平方根处用时间换内存。曲率决定了下降的速度，黑塞-向量积能便宜地触及它，而一个训练好的网络，黑塞矩阵大多是平的。约束带来了乘子、KKT条件和一个对偶问题，而一个方程的解，不必展开就能求导。",

    "This is the engine of everything that follows.":
        "这是后面一切的引擎。在第9部分，我们的库会训练本系列最早的那些神经网络；贯穿深度的一串雅可比矩阵，决定深度网络能不能学得起来，这在第9和第10部分；曲率、鞍点和更好的优化器，是第11部分的内容；对偶在第6部分搭起支持向量机，而第15章的闭式解，在第27部分变成直接偏好优化；数的格式和内存，会在第17到第19部分再次出现。",

    "Here are six problems to try":
        "这里有六道习题，从softmax的雅可比矩阵，到强化学习的闭式解。在这里暂停，把它们做一遍；完整的解答在本部分的讲义里。",

    "Next time: randomness.":
        "下一次：随机性。会动的概率分布，变成布朗运动的随机游走，只是估计值的梯度，还有扩散模型学着去消除的噪声。<bookmark mark='a'/>在进入模型本身之前，这是我们需要的最后一块数学。",

    "Griewank and Walther's Evaluating Derivatives":
        "格里万克和瓦尔特的《计算导数》，是自动微分方面的权威著作，而布隆代尔和鲁莱的《可微编程原理》，是一本现代的书。感谢观看，第5部分见。",
}

PHRASES = {
    # Gradient
    'exactly as the inequality says': '正如不等式所说',
    'close to what the inequality says': '和不等式所说的很接近',
    # Newton
    'roughly doubling each step: quadratic convergence': '每一步大约翻一倍：这是二次收敛',
    'growing faster every step': '每一步都增长得更快',
    # HVP
    'no eigenvalue stands out': '没有哪个特征值显得突出',
    # Quadratic
    'match the formula to rounding error': '和公式一致到舍入误差',
    'match the formula closely': '和公式非常接近',
    'just as predicted': '正如预测',
    'close to the prediction': '与预测很接近',
    # KKT
    'agree to every digit shown': '显示出来的每一位都一致',
    'agree to six digits': '一致到六位数字',
}
