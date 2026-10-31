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


    "This is Part 4 of AI, Built":
        "这是《人工智能，从零搭建》的第4部分：变化，也就是学习的微积分。<bookmark mark='a'/>本部分讲：导数是最好的直线近似，还有真实网络层的导数；<bookmark mark='b'/>运行链式法则的两种方式，并把代价数清楚；手算反向传播，再搭出我们自己的库，用它训练一个模型；<bookmark mark='c'/>计算机里的数会出什么问题；<bookmark mark='d'/>内存；<bookmark mark='e'/>曲率，从牛顿法讲到一个训练好的网络的地形；<bookmark mark='f'/>最后是带约束的优化，结尾讲怎样穿过一个方程的解来求导。",

    # ------------------------------------------------------------------ Derivative
    "Chapter one. The derivative.":
        "第1章。导数。",

    "Zoom in on a smooth curve":
        "把一条光滑的曲线放大，越凑越近，<bookmark mark='a'/>它就开始像一条直线了。<bookmark mark='b'/>这条直线的斜率就是导数：输入每有一点小小的变化，输出会跟着变化多少。",

    "Written down: f at x plus a small step h":
        "写成式子：f在x加上一小步h处的值，大约等于f在x处的值，加上导数乘以h。<bookmark mark='a'/>步子越小，这个估计就越准。导数，就是一个函数在某一点附近最好的直线描述。",

    'f"The idea is Leibniz\'s, in print in 1684':
        "这个想法属于莱布尼茨，他在1684年发表；也属于牛顿，他在17世纪60年代就已经想出来，叫它流数。<bookmark mark='a'/>下面是精确的说法。一个函数在x处可导，是说有一个数，也就是导数，能让直线近似好到这个地步：它的误差比步长本身缩得更快。<bookmark mark='b'/>拿第1部分的意外度曲线来量一量。在这张对数坐标图上，用真实斜率时，误差下降的斜率是{d['slope']:.2f}：像h的平方那样。<bookmark mark='c'/>换一个只偏了百分之十的斜率，误差就只像h那样下降，斜率是{d['slope_bad']:.2f}。步长越来越小时，只有一条直线胜出。所谓最好，就是这个意思。",

    'f"Let\'s use the definition once':
        "我们用这个定义算一次，就算意外度：以2为底、p分之1的对数。<bookmark mark='a'/>走一步h带来的变化，是两个对数之差，<bookmark mark='b'/>也就是一个比值的对数。<bookmark mark='c'/>在1附近，对数就是它自己的切线：1加u的对数等于u，再加上一个比u更小的误差。<bookmark mark='d'/>所以h前面的那个数，是负的p乘以ln 2分之1。<bookmark mark='e'/>在四分之一处，它等于{d['d1']:.2f}比特每单位p：正是放大镜里看到的斜率。",

    "A few derivatives come up over and over.":
        "有几个导数会一再出现。<bookmark mark='a'/>指数函数的导数就是它自己。<bookmark mark='b'/>对数的导数是x分之1。正因为这样，p变小时，意外度才会升得那么陡。<bookmark mark='c'/>还有链式法则，用于复合函数：f(g(x))的意思是，先做g，再做f。把f的斜率记作f的导数，那么f(g(x))的导数，就等于f的导数在g(x)处的值，乘以g的导数在x处的值。变化穿过一层层复合，一路相乘。",

    # ------------------------------------------------------------------ Gradient
    "Chapter two. Many inputs.":
        "第2章。多个输入。",

    'f"A loss depends on many numbers at once.':
        "损失同时取决于很多个数。如果只有两个，它就是平面上方的一张曲面。<bookmark mark='a'/>轻轻推动其中一个数，另一个保持不动，就得到一个偏导数：沿那条坐标轴的斜率。<bookmark mark='b'/>在一点附近，对曲面最好的平面近似，是一个平面，也就是切平面，它按这两个斜率倾斜；它的误差像距离的平方那样下降，和直线时一样：实测斜率是{d['pslope']:.2f}。<bookmark mark='c'/>把这些斜率收进一个向量，就得到了梯度。它指向上坡，而且，我们马上会证明，是最陡的那个方向。<bookmark mark='d'/>所以，朝相反的方向一步又一步地走，你就会滑进山谷。",



    "Walking downhill this way is the oldest method":
        "这样一路走下坡，是本系列里最古老的方法。<bookmark mark='a'/>1847年，奥古斯丁–路易·柯西想解出一条轨道的方程组，就把它们写成一个平方和，并提出逆着它的梯度一步步走。<bookmark mark='b'/>用今天的写法：下一个点，等于当前的点，减去步长η乘以那里的梯度。<bookmark mark='c'/>步子该多大，多快能走到，取决于曲率，这要到第14章，再到第11部分去讲。",

    # ------------------------------------------------------------------ Jacobian
    "Chapter three. Maps that bend.":
        "第3章。会弯曲的映射。",

    "Now let a function take a whole vector":
        "现在，让一个函数把一整个向量变成另一个向量，就像网络的一层所做的那样。<bookmark mark='a'/>这个映射会把平面弄弯：网格线都弯曲了。<bookmark mark='b'/>但凑近任何一点放大，弯曲的线就变直了。凑近看，每个光滑的映射都像一个矩阵：它的雅可比矩阵，也就是它所有偏导数排成的表。",



    "Only near a gain of one does it hold steady.":
        "只有增益接近1时，它才保持稳定。",

    # ------------------------------------------------------------------ Layers
    "Chapter four. The Jacobians of real layers.":
        "第4章。真实网络层的雅可比矩阵。",

    'f"Real layers first.':
        "先看真实的网络层。最常见的一种是矩阵乘法：输入X，每个词元一行，乘以权重W。<bookmark mark='a'/>第j行第k列的一个权重，只碰到输出的第k列，所以它的梯度，把从上面传来的梯度G，乘以它乘过的那些输入，收集起来。<bookmark mark='b'/>这个求和本身就是一次矩阵乘法：X的转置乘以G。<bookmark mark='c'/>而输入的梯度，也就是继续流向下一层的那个，是G乘以W的转置。<bookmark mark='d'/>注意我们从来没有写下的东西：雅可比矩阵本身。对GPT-2的一个矩阵，在{T:,}个词元上，它会有{d['jac_entries'] / 1000000000000.0:.1f}万亿个数。反向传播只需要它与G的乘积，代价和这一层向前算时差不多。",


    'f"Last, layer norm':
        "最后是层归一化：减去向量的平均值，再除以它的散布，这里先不加可学习的缩放和平移。<bookmark mark='a'/>x一动，平均值和散布也跟着动，所以雅可比矩阵有两处修正：一个投影，去掉全是1的那个方向，另一个压低径向的变化，再整体除以σ。<bookmark mark='b'/>对6个数算出来，{n_small}个特征值的绝对值小于千分之一，其余的都相等。均值的平移被完全去掉；尺度变化被大幅压低，但ε会留下少量敏感度。",

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






    # ------------------------------------------------------------------ Memory
    "Chapter eleven. Memory.":
        "第11章。内存。",








    # ------------------------------------------------------------------ Newton
    "Chapter twelve. Curvature.":
        "第12章。曲率。",




    # ------------------------------------------------------------------ HVP
    "Chapter thirteen. Curvature without the Hessian.":
        "第13章。不用黑塞矩阵的曲率。",

    "A Hessian with a billion rows is out of reach":
        "一个有十亿行的黑塞矩阵，是够不着的，但它与一个向量的乘积，却不是。<bookmark mark='a'/>H乘以v，就是沿着v移动时，梯度怎样变化。<bookmark mark='b'/>既然v是固定的，这就是一个数的梯度，也就是梯度与v的点积的梯度。<bookmark mark='c'/>而一个数的梯度，正是反向模式最擅长、最便宜的事：再运行它一次，穿过计算梯度本身的那些步骤，就能精确地得到H乘以v，代价只是一次梯度的几倍。巴拉克·珀尔马特在1994年发表了这个技巧。",






    # ------------------------------------------------------------------ Quadratic
    "Chapter fourteen. How fast is downhill?":
        "第14章。下山能有多快？",





    # ------------------------------------------------------------------ Lagrange
    "Chapter fifteen. Optimizing under constraints.":
        "第15章。在约束之下求最优。",

    "Often the numbers aren't free":
        "很多时候，这些数并不是自由的：概率加起来必须是1，预算不能超支。这里，要把f最小化，它的等高线是这些椭圆，但只能在这个圆上取值。<bookmark mark='a'/>沿着圆走，看两个箭头：f的梯度，和约束的梯度，后者笔直地指向圆外。<bookmark mark='b'/>只要f的梯度沿着圆有一个分量，你就能沿那个分量的反方向滑动，走得更低。<bookmark mark='c'/>所以在带约束的最小值处，那个分量是0：两个梯度互相平行。<bookmark mark='d'/>1788年，约瑟夫–路易·拉格朗日在他的《分析力学》里，把这幅图变成了一种方法。",




    # ------------------------------------------------------------------ KKT
    "Chapter sixteen. Inequalities, and duality.":
        "第16章。不等式，以及对偶。",


    "The multipliers lead to a second problem.":
        "这些乘子引出了第二个问题。把乘子固定住，问拉格朗日函数在任意x上能低到什么程度：这就是对偶函数，q(μ)。<bookmark mark='a'/>对任何可行的x，加上去的那些项都不超过0，所以对偶函数是f的一个下界，在所有能取到的地方都成立。<bookmark mark='b'/>最好的下界d星，至多等于真正的最小值p星：这叫弱对偶，对每个问题都成立。<bookmark mark='c'/>对有严格可行点的凸问题，两者相等：这叫强对偶。两者给出相同的最优值。",



    # ------------------------------------------------------------------ Implicit
    "Chapter seventeen. Differentiating through an equation.":
        "第17章。穿过一个方程求导。",



    "close to the spectral radius of J, as the theory says it should be":
        "和J的谱半径很接近，正如理论所说",

    "roughly doubling each step: quadratic convergence":
        "每一步大约翻一倍：这是二次收敛",

    "slower than the spectral radius alone would suggest":
        "比单看谱半径所预期的要慢",


    "f'and the equilibrium takes longer to reach as it learns":
        "而且它学得越多，达到平衡要花的时间就越长，一开始要{it[0, 1]:.0f}次迭代，最后要{it[-1, 1]:.0f}次",

    "f'and the equilibrium takes {it[0, 1]:.0f} iterations":
        "而达到平衡，一开始要{it[0, 1]:.0f}次迭代，最后要{it[-1, 1]:.0f}次",

    # ------------------------------------------------------------------ Outro

    "This is the engine of everything that follows.":
        "这是后面一切的引擎。在第9部分，我们的库会训练本系列最早的那些神经网络；贯穿深度的一串雅可比矩阵，决定深度网络能不能学得起来，这在第9和第10部分；曲率、鞍点和更好的优化器，是第11部分的内容；对偶在第6部分搭起支持向量机，而第15章的闭式解，在第27部分变成直接偏好优化；数的格式和内存，会在第17到第19部分再次出现。",

    "Here are six problems to try":
        "这里有六道习题，从softmax的雅可比矩阵，到强化学习的闭式解。在这里暂停，把它们做一遍；完整的解答在本部分的讲义里。",

    "Next time: randomness.":
        "下一次：随机性。会动的概率分布，变成布朗运动的随机游走，只是估计值的梯度，还有扩散模型学着去消除的噪声。<bookmark mark='a'/>在进入模型本身之前，这是我们需要的最后一块数学。",

    "Griewank and Walther's Evaluating Derivatives":
        "格里万克和瓦尔特的《计算导数》，是自动微分方面的权威著作，而布隆代尔和鲁莱的《可微编程原理》，是一本现代的书。感谢观看，第5部分见。",
    'f"In part one we worked out a single derivative by hand: the gradient of the surprise with respect to the scores, the model\'s guess minus the truth, for natural-log cross-entropy. In bits there is an extra factor of one over ln two. <bookmark mark=\'a\'/> The recorded parameter counts are about {p[\'gpt2\'] / 1000000.0:.0f} million for GPT-2 and {p[\'qwen3_4b\'] / 1000000000.0:.2f} billion for Qwen3-4B. Each source is labeled on screen. <bookmark mark=\'b\'/> In full-parameter training, every step needs the derivative of the loss with respect to every trainable parameter, and nobody works those out by hand."': "在第1部分，我们亲手算出了一个导数：意外度对各个分数的梯度，也就是模型的猜测减去真相，这里使用自然对数交叉熵。若损失以比特为单位，还要乘以ln 2分之1。<bookmark mark='a'/>记录的参数个数，GPT-2约为{p['gpt2'] / 1000000.0:.0f}百万，Qwen3-4B约为{p['qwen3_4b'] / 1000000000.0:.2f}十亿。各自的数据来源标在屏幕上。<bookmark mark='b'/>在全参数训练中，每一步都需要损失对每个可训练参数的导数，而这些导数，谁也不会去手算。",
    "The mathematics is three centuries older than the computers that run it. Leibniz printed the calculus in 1684, while Newton had his own, his fluxions. <bookmark mark='a'/> In 1788 Lagrange showed how to optimize under constraints, <bookmark mark='b'/> and in 1847 Cauchy proposed walking downhill. <bookmark mark='c'/> Karush, and then Kuhn and Tucker, added inequalities. <bookmark mark='d'/> Then came programs: in 1964 Wengert had one carry derivatives along with its values, <bookmark mark='e'/> and in 1970 Linnainmaa ran the chain rule backwards. <bookmark mark='f'/> In 1985 a standard fixed how computers round, <bookmark mark='g'/> and in 1986 Rumelhart, Hinton and Williams demonstrated learning hidden representations with backpropagation. <bookmark mark='h'/> From 2010, libraries did all of it automatically, <bookmark mark='i'/> and some of today's largest models train with numbers only eight bits long.": "这些数学，比运行它的计算机早了整整三个世纪。1684年，莱布尼茨发表了微积分，而牛顿也有他自己的一套，叫作流数。<bookmark mark='a'/>1788年，拉格朗日说明了怎样在约束之下求最优，<bookmark mark='b'/>1847年，柯西提出了一路走下坡的方法。<bookmark mark='c'/>卡鲁什，后来还有库恩和塔克，又加上了不等式。<bookmark mark='d'/>然后有了程序：1964年，文格特让程序在计算数值的同时，带着导数一起算，<bookmark mark='e'/>1970年，林纳因马把链式法则倒过来运行。<bookmark mark='f'/>1985年，一项标准规定了计算机怎样舍入，<bookmark mark='g'/>1986年，鲁梅尔哈特、辛顿和威廉姆斯展示了怎样用反向传播学习隐藏表示。<bookmark mark='h'/>从2010年起，软件库把这一切都自动做了，<bookmark mark='i'/>而今天一些最大的模型，训练时用的数只有8位长。",
    "Why steepest? At a differentiable point, pick any direction, a unit vector u, and ask for the slope that way. <bookmark mark='a'/> The tangent plane answers it: the slope along u is the gradient dotted with u. <bookmark mark='b'/> By the Cauchy–Schwarz inequality from Part 3, a dot product is at most the product of the lengths, and u has length one: no direction climbs faster than the length of the gradient. <bookmark mark='c'/> If the gradient is nonzero, the maximum occurs in its positive direction. <bookmark mark='d'/> So the gradient's own direction is the steepest way up, its opposite the steepest way down, and the directions at right angles give zero first-order change. If the gradient is zero, every directional derivative is zero.": "为什么是最陡？在函数可微的一点，任选一个方向，一个单位向量u，问问沿这个方向的斜率是多少。<bookmark mark='a'/>切平面给出了答案：沿u的斜率，等于梯度与u的点积。<bookmark mark='b'/>按第3部分的柯西–施瓦茨不等式，点积至多等于两个长度的乘积，而u的长度是1：没有哪个方向，上升得比梯度的长度更快。<bookmark mark='c'/>梯度非零时，最大值在它的正方向取得。<bookmark mark='d'/>所以，梯度自己的方向是最陡的上坡，它的反方向是最陡的下坡，而与它垂直的方向，一阶变化为零。若梯度是零向量，所有方向导数都为零。",
    'f"Seen from above, the surface becomes a map of contour lines, each at one height. <bookmark mark=\'a\'/> Swing a direction around the point and read the slope. <bookmark mark=\'b\'/> It\'s largest straight along the gradient, <bookmark mark=\'c\'/> zero along the tangent to the contour line, <bookmark mark=\'d\'/> and most negative pointing against it. <bookmark mark=\'e\'/> Measured by finite differences in seven hundred and twenty directions, the steepest slope is {d[\'dmax\']:.4f}, the gradient\'s length is {d[\'gnorm\']:.4f}, and the two directions are {off:.2f} degrees apart: {verdict}."': "从正上方看，这张曲面就变成一张等高线图，每条线都在同一个高度上。<bookmark mark='a'/>让一个方向绕着这一点转一圈，读出沿它的斜率。<bookmark mark='b'/>正对着梯度时，斜率最大；<bookmark mark='c'/>沿等高线的切线方向，斜率是0；<bookmark mark='d'/>背对着梯度，斜率最负。<bookmark mark='e'/>用有限差分在720个方向上实测，最陡的斜率是{d['dmax']:.4f}，梯度的长度是{d['gnorm']:.4f}，两个方向相差{off:.2f}度：{verdict}。",
    "In general, a map from n numbers to m numbers has an m by n Jacobian: one row per output, one column per input, the one matrix that makes the straight-line guess best. A gradient is the special case of a single output. <bookmark mark='a'/> For this two-dimensional map, the absolute value of the Jacobian's determinant, from part three, gives the local area factor. <bookmark mark='b'/> And the chain rule for maps is matrix multiplication: the Jacobian of one map after another is the product of their Jacobians, each taken where its input lands. Applying this chain rule backwards is the basis of backpropagation, as chapter five will show.": "一般来说，一个把n个数映成m个数的映射，有一个m乘n的雅可比矩阵：每个输出一行，每个输入一列，正是让直线近似最好的那一个矩阵。梯度只是只有一个输出时的特例。<bookmark mark='a'/>对这个二维映射，雅可比矩阵行列式的绝对值，第3部分讲过，给出了局部的面积缩放比。<bookmark mark='b'/>而映射的链式法则，就是矩阵乘法：一个映射接着另一个映射，它的雅可比矩阵，就是两者雅可比矩阵的乘积，每一个都在它的输入所落到的那一点上求出。反向应用这条链式法则，是反向传播的基础，第5章会讲清楚。",
    'f"Chain many maps and their Jacobians multiply. The product\'s norm is at most the product of the individual norms; it need not equal it. Here is a deep stack of tanh layers, {L} of them, with random weights scaled by a gain. We plot the mean log of the product\'s largest singular value, with the range across seeds. This is the maximum possible amplification, also for the transposed product in backpropagation, not what happens in every direction. A norm below one shrinks every direction; a norm above one allows growth in some direction. <bookmark mark=\'a\'/> At gain {gains[0]:g}, the mean log size ends at {m0:.1f}. <bookmark mark=\'b\'/> At gain {gains[4]:g}, it ends at {m4:.1f}. <bookmark mark=\'c\'/> {verdict} Such products help explain vanishing and exploding gradients. Parts 9 and 10 return to how initialization affects their scale."': "把很多映射串起来，它们的雅可比矩阵就相乘。乘积的范数至多等于各个范数的乘积，并不一定相等。这里是一叠很深的tanh层，一共{L}层，随机权重按一个增益缩放。画的是雅可比乘积最大奇异值的对数，再对种子取平均，并画出不同种子的范围。它表示最大可能的放大倍数，反向传播中转置乘积也一样，并不代表每个方向都会这样变化。范数小于1时，所有方向都缩小；范数大于1时，某个方向可以放大。<bookmark mark='a'/>增益为{gains[0]:g}时，平均对数大小最终为{m0:.1f}。<bookmark mark='b'/>增益为{gains[4]:g}时，最终为{m4:.1f}。<bookmark mark='c'/>{verdict}这样的乘积有助于解释梯度消失和梯度爆炸，第9和第10部分会再讲初始化怎样影响它们的尺度。",
    "Next, the softmax, which turns scores into probabilities. <bookmark mark='a'/> Differentiate with the quotient rule. <bookmark mark='b'/> Split the fraction, and every entry is p i times delta i j, minus p i times p j. <bookmark mark='c'/> As a matrix: the probabilities on the diagonal, minus the outer product of p with itself. <bookmark mark='d'/> Here it is for five scores, computed, and matching our library. Its rows add to zero, because adding the same number to every score changes nothing; and it is symmetric with no negative eigenvalues, one of them zero. <bookmark mark='e'/> Again we never need the matrix: its product with a vector takes n steps instead of n squared, which matters with GPT-2's fifty thousand tokens in the vocabulary. Joined with the cross-entropy, it collapses to Part 1's q minus p when the loss uses natural logarithms; a loss in bits adds a factor of one over ln two.": "接下来是softmax，它把分数变成概率。<bookmark mark='a'/>用商的求导法则来求导。<bookmark mark='b'/>把分式拆开，每一项都是p i乘以δ i j，减去p i乘以p j。<bookmark mark='c'/>写成矩阵：对角线上是这些概率，再减去p与它自己的外积。<bookmark mark='d'/>这是5个分数的情形，算出来的结果，和我们的库完全一致。它的每一行加起来都是0，因为给每个分数都加上同一个数，什么也不会变；它是对称的，没有负的特征值，其中一个是0。<bookmark mark='e'/>同样，我们从来不需要这个矩阵本身：它与一个向量的乘积，只要n步，而不是n的平方步；GPT-2的词表有5万个词元，这一点就很要紧。再接上交叉熵，它就化成第1部分的q减去p，这里损失使用自然对数；若以比特为单位，还要乘以ln 2分之1。",
    'At gain one, its mean log size stays within one power of ten of zero.': '增益为1时，最终的平均对数大小与0相差不到一个数量级。',
    'Even at gain one, its mean log size ends more than one power of ten from zero.': '即使增益为1，最终的平均对数大小与0也相差超过一个数量级。',
    '"Let\'s count. These are networks with two hidden layers of sixty-four, with n inputs and m outputs, from one to two hundred and fifty-six. We count dense derivative matrix products and tanh multiplications, relative to a reference primal pass; this is not every scalar operation. <bookmark mark=\'a\'/> The full Jacobian takes n forward directions. <bookmark mark=\'b\'/> Or m reverse directions. Few inputs and many outputs favor forward mode; many inputs and few outputs favor reverse mode. <bookmark mark=\'c\'/> Timings include primal computation and implementation overhead, separately from the derivative count. In this recorded benchmark, " + tail': "来数一数。这些网络都有两层宽度64的隐藏层，输入数n、输出数m从1到256。我们统计稠密的导数矩阵乘法和tanh乘法，以一次原始前向计算的参考工作量为单位；这不是所有标量运算的总数。<bookmark mark='a'/>完整雅可比矩阵需要n个前向方向。<bookmark mark='b'/>或者m个反向方向。输入少、输出多，通常有利于前向模式；输入多、输出少，通常有利于反向模式。<bookmark mark='c'/>计时还包括原始数值计算和实现开销，与导数工作量分开。在这次记录的基准测试中，{tail}",
    'f"Training is the extreme case: every parameter is an input, and the loss is a single output. <bookmark mark=\'a\'/> Forwards, you carry a matrix with a column for every parameter. <bookmark mark=\'b\'/> Backwards, a single row, the size of the layer you\'ve reached. <bookmark mark=\'c\'/> Our small classifier has {P} parameters. Forward mode pushes {P} directions through it: counted, {cr:.0f} times the dense derivative work of one backward pass, counting matrix products and tanh multiplications. Only parameter gradients are requested, not an input gradient. {timing} The measured gradient difference is shown. <bookmark mark=\'d\'/> For GPT-2 the same column-by-column strategy would require {p[\'gpt2\']:,} directions against one reverse pass. That is why standard large-parameter gradient training usually uses reverse mode, called backpropagation for neural networks. Forward and hybrid methods still have other uses."': "训练是一个极端：每个参数都是输入，损失只有一个输出。<bookmark mark='a'/>向前，要带着一个矩阵，每个参数一列。<bookmark mark='b'/>向后，只需要一行，长度等于当前这一层的大小。<bookmark mark='c'/>这个小分类器有{P}个参数。稠密前向模式把{P}个方向推过网络：只统计导数矩阵乘法和tanh乘法，工作量是一次反向计算的{cr:.0f}倍。这里只请求参数梯度，不请求输入梯度。{timing}屏幕上给出了两种梯度的实测差异。<bookmark mark='d'/>对GPT-2，同样逐列计算的策略需要{p['gpt2']:,}个方向，而反向只需一遍。这就是为什么通常的大参数梯度训练采用反向模式；对神经网络，它叫反向传播。前向和混合方法仍有其他用途。",
    'f"Here is that outer product for one example, computed: the error signal at the hidden layer, a column, times the input, a row. <bookmark mark=\'a\'/> Every row of the result is a multiple of the same input, so the matrix has rank at most one. Here its measured rank is {n_nonzero}: {one_rank}. <bookmark mark=\'b\'/> A batch adds {B} such matrices, so its rank is at most the batch size and the matrix dimensions. Here it reaches rank {rank_b}, {batch_rank}. That structure comes back when models are fine-tuned with low-rank adapters in Part 27. <bookmark mark=\'c\'/> And these hand-derived gradients match our library and PyTorch with the recorded maximum absolute differences shown here, including zero if they coincide."': "这是一个样本的外积，实际算出来了：隐藏层的误差信号是一列，乘上输入这一行。<bookmark mark='a'/>结果的每一行，都是同一输入的倍数，所以矩阵的秩至多为1。这里测得的秩是{n_nonzero}：{one_rank}。<bookmark mark='b'/>一个批次把{B}个这样的矩阵相加，所以秩不超过批次大小，也不超过矩阵的两个维度。这里达到秩{rank_b}，{batch_rank}。这种结构，到第27部分用低秩适配器微调模型时还会出现。<bookmark mark='c'/>这些手推的梯度，与我们的库、与PyTorch的最大绝对差，都按实际记录显示；如果完全相同，就显示0。",
    'f"Does it work? <bookmark mark=\'a\'/> Nudge each checked number a millionth in both directions, take the central difference, and compare: {fd_result}. Chapter ten explains the limits of that numerical check. <bookmark mark=\'b\'/> Against PyTorch, an independent automatic differentiation implementation, {pt_result}. These are absolute errors, not a count of matching printed digits."': "它管用吗？<bookmark mark='a'/>把每个被检验的数，向两个方向各推动百万分之一，取中心差分，再比较：{fd_result}。第10章会解释这种数值检验的局限。<bookmark mark='b'/>再和独立的自动微分实现PyTorch比较，{pt_result}。这里报告的是绝对误差，不是打印出来的小数有多少位相同。",
    "Before we train, look at the first gradient. Differentiate the average natural-log surprise, in nats, with respect to one score, z i j: every pair of letters that starts with i adds its guess minus its truth. <bookmark mark='a'/> Collected, that's the share of pairs starting with i, times Part 1's q minus p hat: the model's probabilities minus the counted ones. <bookmark mark='b'/> At the start every guess is one twenty-seventh. <bookmark mark='c'/> Computed on the books, the library's gradient matches the formula, and the biggest pushes, in red, go to the commonest pairs. Gradient descent is counting, done a little at a time. The plots report bits by dividing the natural-log loss by log two.": "训练之前，先看第一个梯度。把以纳特为单位的平均自然对数意外度，对一个分数z i j求导：每一对以i开头的字母，都贡献它的猜测减去真相。<bookmark mark='a'/>收集起来，就是以i开头的字母对所占的比例，乘以第1部分的q减去p帽：模型的概率，减去数出来的概率。<bookmark mark='b'/>一开始，每个猜测都是27分之1。<bookmark mark='c'/>在这些书上算出来，库给出的梯度与公式一致，而推得最用力的红色项，对应最常见的字母对。梯度下降就是计数，只不过一点一点地做。图里把自然对数损失除以log二，换成比特。",
    'f"Now let\'s train. Counting gives a reference of {d[\'H_cond\']:.3f} bits per letter. <bookmark mark=\'a\'/> The training loop instead samples letter pairs from the books. It learns 729 raw scores, initially zero, with Adam. The picture shows their row-normalized natural log probabilities, not the raw scores. Its scale is shared with the counted comparison: values below minus eight are equally dark. <bookmark mark=\'w\'/> Underneath, samples use the same random dice at every checkpoint. Heatmaps are after the labeled update; the curve records minibatch loss just before that update. The final train and new-text numbers use the full respective corpora."': "现在开始训练。计数给出的参考值，是每个字母{d['H_cond']:.3f}比特。<bookmark mark='a'/>训练循环则从书里抽取字母对，用Adam学习729个原始分数，初始都为0。图中显示的是逐行归一化的自然对数概率，不是原始分数。它与计数对照采用同一刻度：低于负8的值，都显示为最暗。<bookmark mark='w'/>下方的样本，在每个检查点都用同样的随机骰子。热图对应标注那一步更新之后的状态；曲线记录该步更新之前的小批次损失。最后的训练集与新文本数值，则分别用完整语料评估。",
    'f"{loss_verdict} <bookmark mark=\'a\'/> {correlation_verdict} Raw scores can shift by a different constant in each row without changing probabilities, so the comparison uses normalized logs. Maximum likelihood connects the counting solution to the optimization objective; a finite run need not reach it. <bookmark mark=\'b\'/> The same optimization loop, with richer models, trains the later systems in this series."': "{loss_verdict}<bookmark mark='a'/>{correlation_verdict}每行原始分数都可以加上不同的常数，而不改变概率，所以比较的是归一化后的对数。最大似然把计数解与优化目标联系起来；有限次训练不一定达到那个解。<bookmark mark='b'/>后续系统用更丰富的模型，运行的仍是这样的优化循环。",
    'f"How large a step can plain full-batch gradient descent take here? Chapter fourteen will derive the local quadratic stability scale, two over the largest curvature. It is not a global guarantee as curvature changes. <bookmark mark=\'a\'/> At the start, every score zero, the Hessian\'s largest eigenvalue is {d[\'lam0\']:.4f}, which would allow steps up to {d[\'eta0\']:.0f}. <bookmark mark=\'b\'/> But the counting solution has curvature {d[\'lam_star\']:.3f}, giving a local scale of {d[\'eta_star\']:.0f}. <bookmark mark=\'c\'/> " + verdict': "在这里，普通的全批次梯度下降，步子能迈多大？第14章会推导局部二次近似下的稳定性尺度，2除以最大曲率；曲率会变化，所以它不是全局保证。<bookmark mark='a'/>开始时，所有分数为0，黑塞矩阵的最大特征值是{d['lam0']:.4f}，对应的步长尺度是{d['eta0']:.0f}。<bookmark mark='b'/>计数解的曲率是{d['lam_star']:.3f}，局部尺度为{d['eta_star']:.0f}。<bookmark mark='c'/>{verdict}",
    "Every number in this series so far has been a float. In 1985 one standard, IEEE 754, designed largely by William Kahan, specified basic operations and rounding. The same format, operation and rounding mode agree; changing the order or fusing operations can change a program's answer. <bookmark mark='a'/> A normal finite float has a sign, an exponent and a mantissa: one point the mantissa, times two to the exponent. Exponent bits buy range; mantissa bits buy precision. <bookmark mark='b'/> Float32 has eight and twenty-three. Bfloat16 keeps float32's eight exponent bits and only seven for the mantissa; float16 has five and ten; and the eight-bit formats of 2022 have four and three, or five and two. The E4M3 finite variant shown here reserves NaN but has no infinities.": "到目前为止，本系列里的数都用浮点数表示。1985年，主要由威廉·卡亨设计的IEEE 754，规定了基本运算和舍入。同一格式、同一运算、同一舍入模式，结果一致；改变运算顺序或融合运算，程序的答案仍可能改变。<bookmark mark='a'/>一个正规有限浮点数，由符号、指数和尾数组成：1点几的尾数，乘以2的指数次方。指数位换来范围，尾数位换来精度。<bookmark mark='b'/>FP32有8位指数、23位尾数。BF16保留FP32的8位指数，尾数只有7位；FP16是5位和10位；2022年的8位格式，是4位和3位，或者5位和2位。这里显示的E4M3有限数版本，保留NaN，但没有无穷大。",
    'f"The gap between neighbouring floats, the unit in the last place, grows with the number itself: a staircase, one step per power of two in the normal range. Normal relative precision is about {info[\'fp32\'][\'digits\']:.1f} decimal digits in float32, {info[\'bf16\'][\'digits\']:.1f} in bfloat16. Below the smallest normal number, subnormals instead have a fixed absolute gap: two to the minus twenty-four for float16. Relative error can then grow to one on underflow. The plot enumerates format values; some device arithmetic flushes subnormals to zero. <bookmark mark=\'a\'/> Each format also ends somewhere. Float16 stops at {info[\'fp16\'][\'max\']:,.0f}, the four-bit-exponent FP8 at {info[\'e4m3\'][\'max\']:,.0f}, while bfloat16 keeps float32\'s exponent range. That is why bfloat16, Google\'s format for its TPUs, usually avoids the loss scaling often needed with float16. Part 17 covers the hardware, and Part 19 how models are squeezed into fewer bits still."': "相邻浮点数的间隔，叫作最后一位单位；在正规范围里，它随着数值增大，按2的幂一级一级跳。正规数的相对精度，FP32约有{info['fp32']['digits']:.1f}位十进制数字，BF16约有{info['bf16']['digits']:.1f}位。在最小正规数以下，次正规数采用固定的绝对间隔：对FP16，是2的负24次方。发生下溢时，相对误差可以达到1。图里枚举的是格式能表示的值；有些设备运算会把次正规数直接清零。<bookmark mark='a'/>每种格式也有上限。FP16到{info['fp16']['max']:,.0f}为止，4位指数的FP8到{info['e4m3']['max']:,.0f}为止，而BF16与FP32有相近的指数范围。所以，谷歌TPU使用的BF16，通常不需要FP16经常用到的损失缩放。硬件在第17部分讲，进一步压缩模型的位数在第19部分讲。",
    'f"Rounding has consequences. In bfloat16, one plus one two-hundred-and-fifty-sixth is one, and 257 is 256. Even 0.1 is not 0.1 in float32. <bookmark mark=\'a\'/> Add 0.01 ten thousand times; the answer should be 100. <bookmark mark=\'b\'/> Float32 gets {ends[\'fp32\']:.3f}. <bookmark mark=\'c\'/> Float16 stalls at {ends[\'fp16\']:g}, and bfloat16 at {ends[\'bf16\']:g}: once the sum is big enough, the gap between floats is more than twice 0.01, and every addition rounds back to where it was. <bookmark mark=\'d\'/> In this experiment, keep each input in bfloat16 and accumulate sequentially in float32: {ends[\'bf16_fp32acc\']:.2f}, because 0.01 itself was rounded to {tenth:.6f}. Mixed-precision matrix units use the same wider-accumulation idea; their reduction order can differ."': "舍入是有后果的。在BF16里，1加256分之1还是1，257变成256。就连0.1，在FP32里也不是精确的0.1。<bookmark mark='a'/>把0.01加一万次，数学上的答案应该是100。<bookmark mark='b'/>FP32得到{ends['fp32']:.3f}。<bookmark mark='c'/>FP16停在{ends['fp16']:g}，BF16停在{ends['bf16']:g}：和足够大之后，相邻浮点数的间隔超过0.01的两倍，每次相加都会舍入回原处。<bookmark mark='d'/>这次实验把每个输入保存在BF16里，再按顺序用FP32累加，得到{ends['bf16_fp32acc']:.2f}，因为0.01本身已被舍入成{tenth:.6f}。混合精度矩阵单元也采用更宽精度累加的思路，但归约顺序可能不同。",
    'f"Range has consequences too. The softmax exponentiates its scores, and e to the power {math.ceil(ov[\'fp32\'])} is already too big for float32; in float16, e to the {ov[\'fp16\']:.1f} is. <bookmark mark=\'a\'/> So scores of a thousand, nine hundred and ninety-nine and nine hundred and ninety-eight become infinities, and the probabilities become not a number. <bookmark mark=\'b\'/> The fix is to subtract the largest score first. The log of a sum of exponentials is the maximum, <bookmark mark=\'c\'/> plus the log of a sum in which every exponent is at most zero. <bookmark mark=\'d\'/> For finite scores, no shifted exponential overflows, and the largest term is exactly one, so the sum can\'t vanish either. Very small terms may underflow harmlessly to zero. <bookmark mark=\'e\'/> The same three scores now give clean probabilities, and our library\'s log-softmax does exactly this, in its first line."': "范围也是有后果的。softmax对分数取指数，而e的{math.ceil(ov['fp32'])}次方，对FP32已经太大；在FP16里，e的{ov['fp16']:.1f}次方就会溢出。<bookmark mark='a'/>因此，1000、999和998这三个分数，取指数后都成为无穷大，概率成为非数NaN。<bookmark mark='b'/>办法是先减去最大分数。指数之和的对数，等于最大值，<bookmark mark='c'/>加上另一个和的对数，其中每个指数都不大于0。<bookmark mark='d'/>对有限分数，平移后的指数函数不会上溢；最大项恰为1，所以总和不会为0。很小的项可能下溢为0。<bookmark mark='e'/>同样三个分数，现在给出正常概率；库里的log-softmax第一行正是这样做的。",
    "f'The observed forward-to-reverse call-time ratio is {tr_:.2f}. These means include different implementation and graph-building costs, with no confidence interval; the work count is not a universal lower bound for optimized forward differentiation.'": '前向与反向调用的实测时间比是{tr_:.2f}。这些均值包含不同的实现和建图开销，没有置信区间；这里的工作量统计，也不是优化过的前向微分所必需的通用下界。',
    'one nonzero singular direction, up to rounding': '除舍入误差外，有一个非零奇异方向',
    'the zero outer product in this example': '这个例子的外积恰好为零',
    'a numerical rank that depends on the displayed tolerance': '这个数值秩取决于所用的容差',
    'the maximum for this shape': '达到了这个形状允许的最大值',
    'below the maximum for this shape': '低于这个形状允许的最大值',
    "f'the largest absolute difference is {mantissa} times ten to the {int(exponent)}'": '最大绝对差为{mantissa}乘10的{int(exponent)}次方',
    'the largest absolute difference is exactly zero in this comparison': '这次比较的最大绝对差恰好为0',
    'f"After {d[\'steps\']} Adam updates, the full-training loss is {train:.3f} bits per letter, within 0.02 bits of the counting reference {target:.3f}. This is a finite-run result."': "经过{d['steps']}次Adam更新，完整训练语料的损失为每个字母{train:.3f}比特，与计数参考值{target:.3f}的差距小于0.02比特。这是有限次训练的结果。",
    'f"After {d[\'steps\']} Adam updates, the full-training loss is {train:.3f} bits per letter; its difference from the counting reference is {gap:+.3f} bits. This finite run has not matched the reference within 0.02 bits."': "经过{d['steps']}次Adam更新，完整训练语料的损失为每个字母{train:.3f}比特；与计数参考值的差是{gap:+.3f}比特。这次有限训练尚未在0.02比特的范围内匹配参考值。",
    'f"On {correlation[\'count\']} letter pairs whose counted conditional probability exceeds {correlation[\'threshold\']:g}, the normalized log probabilities have Pearson correlation {corr:.3f} with the counted log probabilities."': "在计数条件概率大于{correlation['threshold']:g}的{correlation['count']}个字母对上，归一化后的对数概率，与计数对数概率的皮尔逊相关系数为{corr:.3f}。",
    'f"For the recorded mask of {correlation[\'count\']} letter pairs, Pearson correlation is undefined; no correlation value is inferred."': "所记录的掩码包含{correlation['count']}个字母对，皮尔逊相关系数未定义；这里不推断任何相关系数。",
    'f"Over the final {d[\'metrics\'][\'final_tail_states\']} recorded states, step {e2:.0f} has mean loss {m[2]:.3f} bits and range {sp[2]:.4f}; step {e3:.0f} has mean {m[3]:.3f} and range {sp[3]:.4f}. Only the first is within our 0.001-bit late-window variation criterion. That describes this finite window, not convergence for all future updates."': "在最后{d['metrics']['final_tail_states']}个记录状态里，步长{e2:.0f}的平均损失为{m[2]:.3f}比特，范围宽度为{sp[2]:.4f}；步长{e3:.0f}的平均值为{m[3]:.3f}，范围宽度为{sp[3]:.4f}。只有前者满足晚期窗口内变化小于0.001比特的判据。这只描述有限窗口，不保证之后所有更新都会收敛。",
    'f"Over the final {d[\'metrics\'][\'final_tail_states\']} recorded states, steps {e2:.0f} and {e3:.0f} have mean losses {m[2]:.3f} and {m[3]:.3f} bits, with ranges {sp[2]:.4f} and {sp[3]:.4f}. The displayed local stability scale is not a universal convergence test."': "在最后{d['metrics']['final_tail_states']}个记录状态里，步长{e2:.0f}和{e3:.0f}的平均损失分别为{m[2]:.3f}和{m[3]:.3f}比特，范围宽度分别为{sp[2]:.4f}和{sp[3]:.4f}。图中的局部稳定性尺度不是通用的收敛检验。",
    "One more way numbers go wrong, and it explains how to check a gradient. Take one minus cos x, over x squared: for small x it is very nearly one half. <bookmark mark='a'/> Computed as written, in float32, the error explodes as x shrinks, <bookmark mark='b'/> and at x of ten to the minus four, cos x rounds to exactly one, and the answer is zero. <bookmark mark='c'/> This is cancellation: subtracting two nearly equal numbers keeps their rounding errors but loses their size, so the relative error grows like one over x squared, just as predicted. Float64 only delays it. <bookmark mark='d'/> Rewritten without the subtraction, the same formula avoids that cancellation over this sampled range. Errors below the display floor, including zero, are drawn at the floor.": "数还有一种出错的方式，而它恰好说明了该怎样检验梯度。看1减cos x，再除以x的平方：x很小时，它非常接近二分之一。<bookmark mark='a'/>照原样在FP32里计算，x越小，误差就越是爆炸，<bookmark mark='b'/>到了x等于10的负4次方，cos x被舍入成恰好是1，答案成了0。<bookmark mark='c'/>这就是抵消：两个几乎相等的数相减，保留了它们的舍入误差，却丢掉了它们的大小，所以相对误差像x的平方分之1那样增长，正如预测的那样。FP64只是把它推迟了。<bookmark mark='d'/>换一种不做减法的写法，同一个式子在这段抽样范围内就能避开这种抵消。低于显示下限的误差，包括0，都画在下限处。",
    "A gradient check is a cancellation on purpose. Expand f a step either side of x, by Taylor's theorem. <bookmark mark='a'/> Subtract and divide by two h: the even terms cancel, leaving the derivative plus a truncation error that shrinks like h squared. <bookmark mark='b'/> But each value of f was rounded, by about u times f, u the unit roundoff, and the subtraction keeps those errors while dividing by a tiny 2 h: a rounding error that grows like one over h. <bookmark mark='c'/> Add the two, <bookmark mark='d'/> and set the derivative to zero: this local model predicts a step near the cube root of three u times the absolute value of f over the absolute third derivative, when that derivative is nonzero. Too large a step and Taylor's error wins; too small and rounding does.": "梯度检验，就是故意制造的一次抵消。用泰勒定理，把f在x两边各展开一步。<bookmark mark='a'/>相减再除以2h：偶数次的项抵消了，剩下导数，加上一个截断误差，它像h的平方那样缩小。<bookmark mark='b'/>可是f的每个值都被舍入过，误差大约是u乘以f，u是单位舍入误差，而这次相减保留了这些误差，又除以一个很小的2h：于是舍入误差像h分之1那样增长。<bookmark mark='c'/>把两者加起来，<bookmark mark='d'/>令导数为0：在三阶导数不为0时，这个局部模型预测，将3乘以u乘以f的绝对值，再除以三阶导数的绝对值，对整个比值开立方，就得到这个局部模型预测的步长。步子太大，泰勒的误差占上风；太小，舍入误差占上风。",
    'f"Here it is measured, on chapter seven\'s network, along the same eight random directions in both precisions. The solid curves are pointwise median errors, and the shaded bands show the range. <bookmark mark=\'a\'/> First inspect float64 for the competition between truncation and rounding. {slope_v} <bookmark mark=\'b\'/> Now compare float32. <bookmark mark=\'c\'/> Each dot marks the minimum of the median curve actually drawn; it is not the median of the eight best steps. {verdict} <bookmark mark=\'d\'/> {error_v} For comparison, {step_v} The local error model guides the step choice; the measured curve checks it. Values outside the displayed error range are shown at its stated floor or ceiling."': "这是实测结果，用的是第7章的网络，两种精度沿着相同的8个随机方向。实线是每个步长处误差的中位数，阴影带表示范围。<bookmark mark='a'/>先看FP64里截断误差和舍入误差怎样竞争。{slope_v}<bookmark mark='b'/>再比较FP32。<bookmark mark='c'/>每个圆点都标出实际画出的中位数曲线的最低点，并不是8个各自最优步长的中位数。{verdict}<bookmark mark='d'/>{error_v}作为对照，{step_v}局部误差模型指导步长选择，实测曲线用来检验它。超出显示误差范围的值，画在注明的下限或上限处。",
    'A finite comparison with the prediction is unavailable.': '无法给出与预测值的有限数值比较。',
    'Both plotted median-curve optima are within a factor of three of the predicted steps.': '画出的两条中位数曲线，其最优步长都在各自预测步长的3倍以内。',
    "f'The largest discrepancy is a factor of {factor:.1f}; the prediction is an error-model estimate, not a guarantee.'": '最大的偏差是{factor:.1f}倍；预测来自误差模型，并不是保证。',
    "f'Its fitted right-hand slope is {slope:.2f}.'": '拟合得到的右侧斜率是{slope:.2f}。',
    'There are too few eligible samples for a fitted right-hand slope.': '符合条件的样本太少，无法拟合右侧斜率。',
    'f"At chapter seven\'s step of a millionth, the float64 median error is {e6:.2e}."': '第7章取百万分之一步长时，FP64的中位数误差是{e6:.2e}。',
    "At chapter seven's step of a millionth, a finite float64 median error is unavailable.": '第7章取百万分之一步长时，无法给出有限的FP64中位数误差。',
    "f'The smallest median errors are {e64:.2e} in float64 and {e32:.2e} in float32.'": '最小的中位数误差，FP64为{e64:.2e}，FP32为{e32:.2e}。',
    'At least one precision has no finite median-error optimum to report.': '至少有一种精度，无法报告有限的中位数误差最优点。',
    "Reverse mode has a price, and it is memory. <bookmark mark='a'/> On the ordinary forward pass, every layer's output is kept, <bookmark mark='b'/> because on the way back each step needs it: a layer's Jacobian depends on its input. <bookmark mark='c'/> Only as the backward pass reaches a layer can its activations be freed. So the memory grows with the depth, and with the batch and the width too; training large models, activations can become a major share of GPU memory, alongside parameters and optimizer state, which is Part 18's problem.": "反向模式是有代价的，代价就是内存。<bookmark mark='a'/>普通的向前计算会保留每一层的输出，<bookmark mark='b'/>因为往回走时，每一步都要用到它：一层的雅可比矩阵取决于它的输入。<bookmark mark='c'/>只有等反向计算走到某一层，它的激活才能释放。所以内存随深度增长，也随批量和宽度增长；训练大模型时，除了参数和优化器状态，激活也可能占据显存的很大一部分，这是第18部分的问题。",
    "The way out is to trade memory for time. <bookmark mark='a'/> Keep only every k-th output, a checkpoint; when the backward pass reaches a segment, run that segment forward again from its checkpoint, and keep its k outputs just while they're needed. <bookmark mark='b'/> The memory is n over k checkpoints plus one segment of k. <bookmark mark='c'/> It's smallest where its slope is zero, <bookmark mark='d'/> at k equal to the square root of n, where it is two root n instead of n. <bookmark mark='e'/> The cost: every segment is recomputed once, about one extra forward pass. Tianqi Chen and colleagues brought this to deep networks in 2016; Andreas Griewank had shown in 1992 that recursive checkpoint schedules can use logarithmic storage and logarithmic recomputation overhead, relative to the original linear evaluation cost: total work of order n log n in that model. Today it is one line in PyTorch, and FlashAttention uses the same trade, recomputing attention's weights in the backward pass instead of storing them, as Part 19 shows.": "出路是用时间换内存。<bookmark mark='a'/>每隔k层只留一个输出，叫作检查点；反向计算走到某一段时，就从那一段的检查点出发，把这一段重新向前算一遍，只在需要的时候留着它的k个输出。<bookmark mark='b'/>内存等于n除以k个检查点，再加上一段的k个。<bookmark mark='c'/>它在斜率为0的地方最小，<bookmark mark='d'/>也就是k等于n的平方根时，这时内存是2倍的根号n，而不是n。<bookmark mark='e'/>代价是：每一段都要重算一次，大约多出一次向前计算。陈天奇和同事们在2016年把它用到了深度网络上；而安德烈亚斯·格里万克在1992年就已证明，递归检查点方案可以使用对数级的存储，以及相对于原本线性计算代价的对数级重算开销：在这个模型里，总工作量是n乘以log n的量级。今天，在PyTorch里这只需要一行代码；FlashAttention也做同样的交换：在反向传播时重新算出注意力权重，而不是把它们存下来，第19部分会讲到。",
    'f"Counted in an ideal activation-liveness model, on a chain of {n} layers. <bookmark mark=\'a\'/> The most activations held at once follows n over k plus k: {int(peak[0])} if you keep everything, and {int(peak.min())} at the minimum. The minimizing intervals span k of {lo} to {hi}. {verdict} <bookmark mark=\'b\'/> The price is in evaluations: {int(evals[0])} layers run forward if everything is kept, {int(evals[k_rt])} with checkpoints, and {int(d[\'none_evals\']):,} if nothing is kept and every input is recomputed from the start. <bookmark mark=\'c\'/> {scaling} Timed on a deeper, wider chain, checkpoints cost {ratio:.2f} times the time in this benchmark. {gradient_v} This counts logical activation lifetimes, not measured physical memory; parameters, gradients, allocator behavior and temporary workspace are excluded."': "按理想的激活存活模型，在一条{n}层的链上计数。<bookmark mark='a'/>同时存活的激活峰值跟着n除以k再加k走：全部保留时是{int(peak[0])}个，最小值是{int(peak.min())}个。达到最小值的间隔，k从{lo}跨到{hi}。{verdict}<bookmark mark='b'/>代价体现在计算次数上：全部保留时向前运行{int(evals[0])}层，使用检查点时是{int(evals[k_rt])}层，而什么都不留、每个输入都从头重算时是{int(d['none_evals']):,}层。<bookmark mark='c'/>{scaling}在一条更深更宽的链上计时，这次基准测试中检查点花的时间是原来的{ratio:.2f}倍。{gradient_v}这里统计的是逻辑上的激活存活期，并不是实测物理内存；参数、梯度、分配器行为和临时工作区都不计入。",
    "f'The square-root reference, {rt:g}, lies in that span.'": '平方根参考值{rt:g}，落在这个跨度内。',
    "f'The square-root reference is {rt:g}; it lies outside that observed span.'": '平方根参考值是{rt:g}，落在这个观测跨度之外。',
    'No finite longer-chain comparison is available.': '没有可用的有限数值来比较更长的链。',
    "f'Across the tested longer-chain candidates, selected k divided by root n ranges from {min(ratios):.2f} to {max(ratios):.2f}.'": '在测试过的更长链候选中，选中间隔k除以根号n的比值，从{min(ratios):.2f}到{max(ratios):.2f}。',
    'f"The maximum absolute gradient discrepancy is {d[\'worst\']:.2e}."': "梯度的最大绝对差是{d['worst']:.2e}。",
    'The gradient comparison is not finite.': '梯度比较结果不是有限值。',
    "The gradient says which way is downhill. It doesn't say how the slope itself is changing. <bookmark mark='a'/> That's the second derivative, curvature. With many inputs it's a matrix of second derivatives, the Hessian. <bookmark mark='b'/> For a twice continuously differentiable function it is symmetric, so, from part three, it has perpendicular eigenvectors, the directions of pure curvature, and its eigenvalues say how sharply the surface bends along each. <bookmark mark='c'/> This quadratic is a bowl when both are positive. With mixed signs it is a saddle at its stationary origin. Mixed curvature at an arbitrary point does not establish stationarity.": "梯度告诉你哪边是下坡，却没告诉你，斜率本身在怎样变化。<bookmark mark='a'/>那是二阶导数，曲率。有多个输入时，它是一个由二阶导数组成的矩阵，叫作黑塞矩阵。<bookmark mark='b'/>对于二阶连续可微的函数，它是对称的，所以按第3部分讲的，它有互相垂直的特征向量，也就是纯粹弯曲的方向，而它的特征值，说明曲面沿每个方向弯得有多厉害。<bookmark mark='c'/>对这里的二次函数，两个都为正时是碗面。正负号混合时，它在作为驻点的原点处是鞍点。任意一点处曲率正负混合，本身并不能说明那里是驻点。",
    "The Hessian gives a better step. The first derivative made the best straight line; with the second, the local quadratic. When the Hessian is positive definite, this quadratic has a minimum. <bookmark mark='a'/> Solve for that minimum, where its gradient is zero: <bookmark mark='b'/> the step is minus H inverse times the gradient. That's Newton's method. <bookmark mark='c'/> Newton used the idea in 1669 for roots of equations, Raphson simplified it in 1690, and Thomas Simpson extended it in 1740 to several variables and to finding minima.": "黑塞矩阵能给出更好的一步。一阶导数给出了最好的直线；加上二阶导数，就是局部二次近似。黑塞矩阵正定时，这个二次函数有最小值。<bookmark mark='a'/>求出这个最小值，也就是梯度为0的地方：<bookmark mark='b'/>这一步，等于负的H的逆乘以梯度。这就是牛顿法。<bookmark mark='c'/>1669年，牛顿用这个想法求方程的根，1690年，拉夫森把它简化，1740年，托马斯·辛普森把它推广到多个变量，并用来求最小值。",
    'f"A test: logistic regression, a classifier Part 6 builds, with two correlated features. The curvature ratio at the reference solution is {d[\'kappa\']:.0f}. <bookmark mark=\'a\'/> Gradient descent uses the conservative step one over L, where L globally bounds curvature. {gd_summary} <bookmark mark=\'b\'/> {nw_summary} These are iteration counts, not equal amounts of work per step. <bookmark mark=\'c\'/> {digit_v} Local quadratic convergence requires a sufficiently close starting point and a nonsingular Hessian with suitable smoothness; three digit counts alone do not certify it. <bookmark mark=\'d\'/> The catch is the Hessian itself: each step solves a linear system with it, and for a billion parameters it would have a billion squared entries. The next chapter uses curvature without ever building it."': "做个测试：逻辑回归，第6部分会搭建的一种分类器，它有两个相关特征。参考解处的曲率比是{d['kappa']:.0f}。<bookmark mark='a'/>梯度下降使用保守步长1除以L，其中L是曲率的全局上界。{gd_summary}<bookmark mark='b'/>{nw_summary}这些是迭代次数，每一步的工作量并不相同。<bookmark mark='c'/>{digit_v}局部二次收敛要求初始点足够接近、黑塞矩阵非奇异，并满足相应的光滑性条件；只看三次正确位数，不能证明这一点。<bookmark mark='d'/>麻烦在于黑塞矩阵本身：每一步都要用它解一个线性方程组，而对十亿个参数来说，它会有十亿的平方个元素。下一章会讲，怎样用上曲率，却从来不把它造出来。",
    'f"{method}\'s objective-gap comparison is unavailable because the numerical reference is not stationary."': '{method}的目标函数差比较不可用，因为数值参考解尚未达到驻点条件。',
    'f"{method} first meets its {criterion} threshold at step {result[\'first_hit_step\']}."': "{method}在第{result['first_hit_step']}步首次满足{criterion}阈值。",
    'f"{method} has not met its {criterion} threshold by its cap of {result[\'cap\']} steps; the observed run is censored."': "{method}达到{result['cap']}步的迭代上限时，仍未满足{criterion}阈值；这次观测在上限处被截断。",
    "f'{method} did not produce a finite converged result; its status is {status}.'": '{method}没有得到有限的收敛结果；状态是{status}。',
    'Three finite positive recorded errors are unavailable for a correct-digit comparison.': '缺少三个有限且为正的误差记录，无法比较正确位数。',
    'The recorded counts increase in these steps.': '记录的位数在这几步中增加。',
    'The recorded counts do not increase at every step.': '记录的位数并非每一步都增加。',
    "f'Correct-digit estimates are {digits[0]:.1f}, {digits[1]:.1f}, and {digits[2]:.1f}. {trend}'": '估算的正确位数依次是{digits[0]:.1f}、{digits[1]:.1f}和{digits[2]:.1f}。{trend}',
    'f"Check it on the stored final parameters of a small network. <bookmark mark=\'a\'/> Against the full Hessian, the maximum product discrepancy is {d[\'hv_full_diff\']:.2e}. In this benchmark a product takes {ratio:.1f} times a gradient\'s time. <bookmark mark=\'b\'/> The best recorded finite-difference relative error is {d[\'fd_best\']:.2e}. <bookmark mark=\'c\'/> Repeated products and normalization are power iteration. With a strictly dominant eigenvalue magnitude and a nonzero initial projection on its eigenspace, they approach that eigenspace. The eigenvalue may be negative: largest magnitude is not largest algebraic value. {power_v} Display floors and ceilings are stated below the plots."': "在一个小网络保存下来的最终参数上检验。<bookmark mark='a'/>与完整黑塞矩阵相比，乘积的最大差是{d['hv_full_diff']:.2e}。这次基准测试中，一次乘积花的时间是一次梯度的{ratio:.1f}倍。<bookmark mark='b'/>记录中最好的有限差分相对误差是{d['fd_best']:.2e}。<bookmark mark='c'/>反复做乘积并归一化，就是幂迭代。若某个特征值的模严格占优，初始向量在它的特征子空间上的投影又不为0，迭代就会趋向那个子空间。这个特征值可能为负：模最大，并不等于代数值最大。{power_v}图下方注明了显示的下限和上限。",
    'f"Now watch a landscape change as a network learns three interleaved spirals. This network has {P} parameters, with its full Hessian computed at {K} stored checkpoints. Accuracy is on the {len(y)} training examples. <bookmark mark=\'a\'/> {initial_v} <bookmark mark=\'b\'/> The signed-log plot divides each spectrum by its own absolute spectral radius, so its shape and absolute size must be read separately. {neg_v} <bookmark mark=\'c\'/> Final counts: {final_v} Absolute scale: {radius_v} The cutoffs are stated relative to each checkpoint\'s spectral radius. High-positive is a selected cutoff, not a fitted statistical outlier test. Sagun and colleagues studied concentration of neural network Hessian spectra in 2016; this small training example reports its own measured outcome."': "现在来看，一个网络学习三条交错螺旋时，地形怎样变化。这个网络有{P}个参数，在保存的{K}个检查点上计算了完整黑塞矩阵。准确率是在{len(y)}个训练样本上测得的。<bookmark mark='a'/>{initial_v}<bookmark mark='b'/>带符号的对数图，把每个谱除以它自己的绝对谱半径，因此形状和绝对大小必须分开读。{neg_v}<bookmark mark='c'/>最终计数：{final_v}绝对尺度：{radius_v}这些阈值都是相对于各个检查点的谱半径定义的。高正值只是一个选定阈值，并不是拟合得到的统计离群值检验。萨贡和同事们在2016年研究了神经网络黑塞谱的集中现象；这里的小型训练例子，报告的是它自己的实测结果。",
    'f"For this stored spectrum the signed dominant-magnitude target is {power[\'target\']:.3g}; the final relative error is {last:.2e}."': "对这个保存下来的谱，模占优的带符号目标值是{power['target']:.3g}；最终相对误差是{last:.2e}。",
    'A finite final comparison with a unique signed nonzero dominant-magnitude target is unavailable, so that convergence comparison is omitted.': '无法给出与唯一、带符号且非零的模占优目标之间的有限最终比较，因此不显示这项收敛比较。',
    'The initial Hessian has both positive and negative curvature directions. That alone does not establish a stationary saddle point.': '初始黑塞矩阵同时有正曲率方向和负曲率方向；仅凭这一点，不能把起点判为驻点鞍点。',
    'The stored initial spectrum does not have both positive and negative eigenvalues.': '保存的初始谱并没有同时出现正、负特征值。',
    'Relative negative-curvature counts are unavailable for an empty spectrum.': '谱为空，无法给出相对负曲率计数。',
    "f'The count below the stated negative cutoff decreases from {a} to {b} between the first and final checkpoints.'": '在首个和最终检查点之间，低于注明的负值阈值的数量，从{a}减少到{b}。',
    "f'The count below the stated negative cutoff increases from {a} to {b} between the first and final checkpoints.'": '在首个和最终检查点之间，低于注明的负值阈值的数量，从{a}增加到{b}。',
    "f'The count below the stated negative cutoff is {a} at both endpoints; intermediate checkpoints may differ.'": '首尾两个检查点，低于注明的负值阈值的数量都是{a}；中间的检查点可能不同。',
    'A finite absolute spectral-radius comparison is unavailable.': '无法给出绝对谱半径的有限数值比较。',
    "f'The absolute spectral radius decreases from {a:.3g} to {b:.3g}.'": '绝对谱半径从{a:.3g}减少到{b:.3g}。',
    "f'The absolute spectral radius increases from {a:.3g} to {b:.3g}.'": '绝对谱半径从{a:.3g}增加到{b:.3g}。',
    "f'The absolute spectral radius is {a:.3g} at both endpoints.'": '首尾两个检查点的绝对谱半径都是{a:.3g}。',
    'f"At the final checkpoint, {final[\'high_positive\']} eigenvalues exceed the chosen positive cutoff, and {100 * final[\'flat\']:.0f} percent lie inside the stated relative near-zero cutoff."': "在最终检查点，有{final['high_positive']}个特征值超过所选的正值阈值，有百分之{100 * final['flat']:.0f}位于注明的相对近零阈值内。",
    'At the final checkpoint the relative cutoff counts are undefined.': '最终检查点的相对阈值计数没有定义。',
    "On a quadratic bowl with a positive-definite Hessian, gradient descent can be solved exactly. <bookmark mark='a'/> Each step multiplies the position by I minus eta H. <bookmark mark='b'/> In the Hessian's eigenvectors that matrix is diagonal, so each coordinate shrinks on its own, by one minus eta times its eigenvalue. <bookmark mark='c'/> Every factor must be less than one in size, so the step must be positive and smaller than two over the largest curvature. <bookmark mark='d'/> And the slowest coordinate sets the pace. The best step balances the two extremes, and the rate is kappa minus one over kappa plus one, where kappa, the condition number, is the largest curvature over the smallest. This factor bounds the position-error norm; the quadratic objective shrinks by at most its square.": "在黑塞矩阵正定的二次碗上，梯度下降可以精确解出来。<bookmark mark='a'/>每一步都把位置乘以I减ηH。<bookmark mark='b'/>在黑塞矩阵的特征向量基下，这个矩阵是对角的，所以各个坐标独立地乘以1减η乘它的特征值。<bookmark mark='c'/>每个倍数的绝对值都必须小于1，因此步长必须为正，而且小于最大曲率分之2。<bookmark mark='d'/>最慢的坐标决定速度。最好的步长平衡两个极端，倍数是κ减1除以κ加1；条件数κ，就是最大曲率与最小曲率之比。这是位置误差范数的上界倍数；二次目标值的收缩倍数，至多是它的平方。",
    'f"Here is a valley with kappa of twenty-five: it bends twenty-five times more sharply across than along. <bookmark mark=\'a\'/> The steepest way down points mostly at the opposite wall, so the steps zigzag from wall to wall and crawl along the floor. For the objective to fall below one percent of its initial value, {gd_summary}. <bookmark mark=\'b\'/> Momentum carries speed from step to step. {momentum_verdict} Part 11 derives the method. <bookmark mark=\'c\'/> Newton\'s step undoes the curvature and lands at the bottom at once."': "这是κ为25的山谷：横向比纵向弯得厉害25倍。<bookmark mark='a'/>最陡的下坡方向大多指向对面的谷壁，所以步子来回折返，沿谷底慢慢挪动。要让目标值降到初始值的1%以下，{gd_summary}。<bookmark mark='b'/>动量把速度从一步带到下一步。{momentum_verdict}第11部分会推导这个方法。<bookmark mark='c'/>牛顿步把曲率抵消，一步就落到谷底。",
    'f"Measured on bowls from kappa of one to a thousand: the rates, in orange, {verdict}. <bookmark mark=\'a\'/> The grey curve is the large-kappa norm-error estimate. At kappa {k_big:,}, {step_verdict}. Triangles mark capped or unresolved runs, not converged counts. <bookmark mark=\'b\'/> The theoretical stability boundary is two over the largest curvature. {stability_verdict} Real losses are not quadratics, but this is the calculus behind every learning-rate rule, and Part 11 builds the faster methods on it."': "在κ从1到1000的碗上实测，橙色的倍数{verdict}。<bookmark mark='a'/>灰线是κ很大时的位置误差范数估计。κ为{k_big:,}时，{step_verdict}。三角形标出触及上限或未解决的运行，不把它们算成已收敛的步数。<bookmark mark='b'/>理论稳定边界是最大曲率分之2。{stability_verdict}真实损失不是二次函数，但这些微积分支撑着学习率规则，第11部分会在此基础上搭建更快的方法。",
    'f"A saddle can delay descent. Here\'s a surface with a saddle at the centre and a minimum above and below it. <bookmark mark=\'a\'/> Start almost on the line through the saddle, a tiny distance y nought off it. The walk slides in towards the saddle, where the gradient nearly vanishes, and waits, until the tiny offset has grown enough to fall off. <bookmark mark=\'b\'/> Near the saddle the offset grows by one plus eta each step, so the local prediction is logarithmic in one over y nought. We fit only runs that reached absolute y above one half; {verdict}. Capped runs are marked separately. <bookmark mark=\'c\'/> Start exactly on the line and it never leaves: the gradient falls to {mant(sg)} times ten to the minus {expo(sg)}, at a point that is not a minimum. Only the Hessian, with its negative eigenvalue, tells them apart. In practice the noise of stochastic gradients kicks a network off; Yann Dauphin and colleagues argued in 2014 that in many dimensions saddles, more than bad minima, are what slow training."': "鞍点可能拖慢下降。这张曲面中央有一个鞍点，上下各有一个最小值。<bookmark mark='a'/>几乎从穿过鞍点的那条线出发，只偏离很小的y零。轨迹滑向鞍点，梯度几乎消失，然后等待，直到那一点偏移长得足够大，才滑落下去。<bookmark mark='b'/>鞍点附近，偏移每一步乘以1加η，因此局部预测与1除以y零的对数成正比。我们只拟合绝对y超过二分之一的运行；{verdict}。触及上限的运行单独标出。<bookmark mark='c'/>恰好从那条线上出发，就一直出不去：梯度降到{mant(sg)}乘10的负{expo(sg)}次方，却不是最小值。黑塞矩阵里的负特征值，才能把它们区分开。实际训练中，随机梯度的噪声会把网络踢开；2014年，Yann Dauphin和同事提出，在很多维里，拖慢训练的往往是鞍点，而不只是坏的最小值。",
    'f"Write it down: at the constrained minimum, the gradient of f is a multiple of the constraint\'s gradient, minus lambda times it. <bookmark mark=\'a\'/> Lagrange\'s device folds the constraint into a single function, the Lagrangian, f plus lambda times g. <bookmark mark=\'b\'/> Stationarity in x and lambda gives necessary conditions for a regular constrained optimum, not a guarantee of a minimum. The derivative in lambda gives back the constraint. <bookmark mark=\'c\'/> At the numerical circle candidate, the multiplier is {d[\'lam\']:.3f}. {circle_verdict} At a regular optimum it is a signed price: how the optimal value changes as the circle\'s squared radius changes."': "写下来：在受约束的最小值处，f的梯度是约束梯度的一个倍数，也就是负λ乘它。<bookmark mark='a'/>拉格朗日把约束折进一个函数：拉格朗日函数，f加λ乘g。<bookmark mark='b'/>对x和λ取驻点，得到正则受约束最优点的必要条件，不是最小值的保证。对λ求导，会把约束还给我们。<bookmark mark='c'/>在圆上的数值候选点，乘子为{d['lam']:.3f}。{circle_verdict}在正则最优点，它是一个带符号的价格：圆的半径平方改变时，最优值怎样变化。",
    'f"A famous constrained problem: a die whose average roll is 4.5, not 3.5. Which probabilities assume the least beyond that? The ones with the most entropy. <bookmark mark=\'a\'/> Set the Lagrangian\'s derivative to zero, with one multiplier for each constraint, <bookmark mark=\'b\'/> and the answer is a softmax: each face\'s probability is e to the beta times the face, normalized. <bookmark mark=\'c\'/> Computed, beta is {d[\'beta\']:.3f}. {agreement} Edwin Jaynes made this a principle of inference in 1957. It\'s where the softmax comes from: it is the maximum-entropy distribution with a fixed average score. In this convention beta is inverse temperature, one over T, and it is the score-constraint multiplier."': "一个著名的约束问题：骰子的平均点数是4.5，不是3.5。除了这个条件，哪种概率分布做的额外假设最少？熵最大的那一个。<bookmark mark='a'/>每个约束放一个乘子，令拉格朗日函数的导数为0，<bookmark mark='b'/>答案就是softmax：各面的概率正比于e的β乘点数次方，再归一化。<bookmark mark='c'/>算出的β为{d['beta']:.3f}。{agreement}埃德温·杰恩斯在1957年把它变成了推断原则。这给出了softmax的一种来源：固定平均分数时的最大熵分布。按这里的约定，β是逆温度，也就是1除以T，也是平均分数约束的乘子。",
    'f"The same algebra gives reinforcement learning one of its closed forms. Maximize the expected reward, minus a positive beta times the KL divergence from a positive reference policy. Here beta names the KL penalty, so it plays the temperature role, unlike the inverse-temperature beta for the die. <bookmark mark=\'a\'/> With the constraint that the probabilities add to one, the best policy is the reference, reweighted by e to the reward over beta. <bookmark mark=\'b\'/> Here for six actions. {agreement} Part 27\'s direct preference optimization starts from this formula."': "同样的代数，给出强化学习里的一个闭式解：最大化期望奖励，减去正的β乘相对参考策略的KL散度，而且参考策略的每个动作概率都为正。这里β表示KL惩罚，起温度的作用，和刚才骰子里的逆温度β不同。<bookmark mark='a'/>加上概率和为1的约束，最优策略就是参考策略，再按e的奖励除以β次方重新加权。<bookmark mark='b'/>这里有六个动作。{agreement}第27部分的直接偏好优化，就从这个公式出发。",
    "Most constraints are inequalities: a probability can't be negative, a margin must be at least one. William Karush worked out the conditions in his 1939 master's thesis; Harold Kuhn and Albert Tucker found them again in 1951. <bookmark mark='a'/> Under a constraint qualification, at a minimum there are multipliers mu, one per constraint, with the gradient of the Lagrangian zero, every constraint met, every multiplier non-negative, <bookmark mark='b'/> and each multiplier times its constraint equal to zero: complementary slackness. <bookmark mark='c'/> Either the minimum is inside and the wall is idle, its multiplier zero, <bookmark mark='d'/> or the minimum is on the wall. Its multiplier may be positive or zero; in this right-hand example it is positive and measures how hard the wall pushes.": "大多数约束是不等式：概率不能为负，间隔必须至少为1。威廉·卡鲁什在1939年的硕士论文里写出了这些条件；哈罗德·库恩和阿尔伯特·塔克在1951年又发现了它们。<bookmark mark='a'/>满足约束资格条件时，在最小值处，每个约束都有一个乘子μ，使拉格朗日函数的梯度为0，每个约束都满足，每个乘子都非负，<bookmark mark='b'/>而且每个乘子乘自己的约束，等于0：这叫互补松弛。<bookmark mark='c'/>最小值可以在内部，墙不起作用，乘子为0；<bookmark mark='d'/>也可以在墙上。此时乘子可能为正，也可能为0。右边这个例子里，它为正，量出墙推回来有多用力。",
    'f"Two small examples. Minimize x squared, keeping x at least one. Its dual function is a hump that rises to touch the true minimum, one, exactly: no gap. <bookmark mark=\'a\'/> Now a double well, the same kind of constraint, and no convexity. On finite grids, the estimated primal value is {d[\'nc_p\']:.2f} and the best estimated dual value is {d[\'nc_d\']:.2f}, a difference of {d[\'nc_gap\']:.2f}. These are grid estimates, not a certified continuous dual bound. The exact weak-duality theorem still holds; this numerical picture illustrates how a gap can arise."': "两个小例子。最小化x平方，要求x至少为1。它的对偶函数鼓起一个山峰，恰好碰到真正的最小值1：没有间隙。<bookmark mark='a'/>换成双井、类似的约束，却不再凸。在有限网格上，原问题的估计值是{d['nc_p']:.2f}，最好的对偶估计值是{d['nc_d']:.2f}，差值为{d['nc_gap']:.2f}。这些只是网格估计，不是经过认证的连续对偶下界。精确的弱对偶定理仍然成立；这张数值图演示了间隙可能怎样出现。",
    'f"Duality\'s most famous use: the support vector machine of Part 6. Find the widest street between two classes: the smallest w that puts every point at least one unit of margin from the line. <bookmark mark=\'a\'/> Its dual has one multiplier per point, and depends on the points only through their dot products, which is what lets kernels in. Minimizing over the free intercept also requires the label-weighted multipliers to sum to zero. <bookmark mark=\'b\'/> We attempted separate primal and dual solves on {len(X)} points. {solver_verdict} The candidate objective values are displayed with six decimal places. <bookmark mark=\'c\'/> We ring the points whose {len(sv)} multipliers exceed the stated numerical zero threshold; {len(tight)} points have margins within the stated tolerance of one. At an optimum, a positive multiplier forces a point onto a margin, but a margin point can have a zero multiplier in degenerate data. Bernhard Boser, Isabelle Guyon and Vladimir Vapnik built the method on this dual in 1992."': "对偶最著名的用途之一，是第6部分的支持向量机。在两类之间找最宽的街道：让w尽可能小，同时让每个点的函数间隔至少为1。<bookmark mark='a'/>对偶给每个点一个乘子，而且只通过点积依赖数据，这正是核方法能进来的地方。对自由截距取最小，还要求按类别标签加权的乘子之和为0。<bookmark mark='b'/>我们在{len(X)}个点上，分别尝试求解原问题和对偶问题。{solver_verdict}候选目标值显示六位小数。<bookmark mark='c'/>圈出乘子高于数值零阈值的点，共{len(sv)}个；另有{len(tight)}个点的间隔，在给定容差内等于1。在最优点，正乘子一定使点落在间隔边界上；但退化数据里的边界点，可以有零乘子。伯恩哈德·博泽、伊莎贝尔·居永和弗拉基米尔·瓦普尼克，在1992年从这个对偶建立了方法。",
    "Some layers aren't a fixed list of steps. A deep equilibrium layer feeds its output back into itself until nothing changes: its output is the fixed point z star, which satisfies z star equals f of z star and theta. How do you backpropagate through that? <bookmark mark='a'/> Differentiate both sides of the equation. <bookmark mark='b'/> Collect the terms: the derivative of the solution is the inverse of I minus J, times the direct derivative, as long as that inverse exists, which is the implicit function theorem. <bookmark mark='c'/> For a loss, run it as a vector-Jacobian product: one linear solve at the fixed point, however many iterations it took to get there. No history of iteration states is needed, but parameters, local derivatives and the linear solver still take memory. If the loss also depends directly on theta, add that direct derivative.": "有些层，不是一张固定的步骤清单。深度平衡层把输出反馈给自身，直到不再变化：输出是满足z星等于f作用于z星和θ的不动点。怎样反向传播穿过它？<bookmark mark='a'/>对方程两边求导。<bookmark mark='b'/>把项收集起来：解的导数，是I减J的逆，乘直接导数；前提是这个逆存在，这就是隐函数定理。<bookmark mark='c'/>对损失，用向量—雅可比积来做：在不动点解一个线性方程组，不管此前迭代了多少步。无需保留迭代状态的历史，但参数、局部导数和线性求解器仍然占内存。如果损失还显式依赖θ，就再加上那个直接导数。",
    'f"Check it on a layer with an {d[\'initial_state_dimension\']}-dimensional state; {solve_verdict}. The displayed residual and contraction bound describe this iteration solver; invertibility of I minus J is the separate differentiation condition. <bookmark mark=\'a\'/> The usual alternative is to unroll: run K iterations and backpropagate through all of them with our library. As K grows, that gradient is compared with the implicit candidate. <bookmark mark=\'b\'/> {rate_statement} For the final comparisons, {floor_verdict}. This is not a certified bound on fixed-point accuracy. <bookmark mark=\'c\'/> Unrolling stores every iteration; implicit differentiation avoids that history while retaining the equilibrium state and linear-solver workspace."': "用一个状态维数为{d['initial_state_dimension']}的层来检查；{solve_verdict}。显示的残差和压缩界，描述的是这套迭代求解器；I减J可逆，是另一个关于求导的条件。<bookmark mark='a'/>通常的替代办法是展开：运行K次迭代，再用我们的库反向传播穿过全部步骤。随着K增长，把那个梯度和隐式候选梯度比较。<bookmark mark='b'/>{rate_statement}对最后几次比较，{floor_verdict}。这不是不动点精度的认证界。<bookmark mark='c'/>展开要存下每次迭代；隐式求导避开这段历史，同时保留平衡状态和线性求解器工作空间。",
    'f"And it trains. A deep equilibrium model with a {d[\'training_state_dimension\']}-dimensional state and {d[\'parameter_count\']} trainable scalars is fitted using implicit candidate gradients, with its feedback matrix kept at spectral norm at most {d[\'contraction_caps\'][\'training\']:g}. <bookmark mark=\'a\'/> The stored fits replay the run; {loss_verdict}, and {it_v}. {solve_counts} Capped solves are not counted as converged equilibria. For the final comparison input, {final_solve}. <bookmark mark=\'b\'/> Shaojie Bai, Zico Kolter and Vladlen Koltun proposed such models in 2019. The same trick differentiates through an inner optimization, in meta-learning, or through a solver used as a layer: wherever the answer is defined by an equation rather than a recipe."': "它也能训练。这个深度平衡模型的状态维数为{d['training_state_dimension']}，有{d['parameter_count']}个可训练标量，使用隐式候选梯度拟合，同时让反馈矩阵的谱范数至多为{d['contraction_caps']['training']:g}。<bookmark mark='a'/>保存的拟合曲线回放这次运行；{loss_verdict}，而{it_v}。{solve_counts}达到迭代上限的求解，不算作已经收敛的平衡。对最后用于比较的输入，{final_solve}。<bookmark mark='b'/>邵杰·白、Zico Kolter和Vladlen Koltun在2019年提出了这样的模型。同样的技巧，也能对元学习的内层优化求导，或者对作为一层的求解器求导：答案由一个方程，而不只是一份步骤清单定义时，就用得上。",
    "Let's take stock. A derivative is the best straight line, the one whose error shrinks faster than the step; a gradient, the steepest direction, by Cauchy–Schwarz; a Jacobian, the best matrix, and real layers' Jacobians need not be formed, only multiplied. For the full Jacobian, forward mode pays per input and reverse mode per output, so training runs backwards: backpropagation, whose weight gradients are outer products of an error signal and an input. We built it, checked it and trained with it. Floats round and cancel, so softmaxes subtract their maximum and gradient checks pick their step. Checkpoints trade memory for recomputation work in an ideal activation-memory model. Curvature sets the pace of descent, and Hessian-vector products reach it cheaply. Our measured spectrum distinguishes directions using stated relative cutoffs. Constraints bring multipliers, KKT and a dual problem: positive multipliers imply active constraints, and a free SVM intercept adds a label-weighted zero-sum constraint. An equation's solution can be differentiated when its local implicit-function conditions hold.": '来总结。导数是误差比步长缩得更快的那条最佳直线；根据柯西–施瓦茨，梯度给出最陡方向；雅可比矩阵是最佳矩阵近似。真实层的雅可比矩阵无需显式构造，只要做乘法。要求整个雅可比矩阵时，前向模式按输入计费，反向模式按输出计费，所以训练倒着跑：反向传播里的权重梯度，是误差信号和输入的外积。我们搭建、检查，也用它训练。浮点数会舍入、会抵消，所以softmax减去最大值，梯度检验要选步长。检查点在理想激活内存模型里，用重计算工作换内存。曲率决定下降速度，黑塞—向量积能低成本接近它。我们的实测谱，用明确的相对阈值区分方向。约束带来乘子、KKT和对偶问题：正乘子意味着约束活跃；SVM的自由截距，还要求按标签加权的乘子之和为0。满足局部隐函数条件时，也能对方程的解求导。',
    'a finite comparison with the predicted rates is unavailable': '无法得到与预测倍数的有限比较',
    'match the predicted norm-error factors within one millionth': '与预测的位置误差范数倍数之差都小于百万分之一',
    "f'have a largest absolute difference of {gap:.6f} from the predicted norm-error factors'": '与预测的位置误差范数倍数，最大的绝对差是{gap:.6f}',
    'there are too few resolved escape runs for a finite slope comparison': '已解决的逃离运行太少，无法得到有限的斜率比较',
    'the measured slope is within ten percent of the local linear prediction': '实测斜率与局部线性预测相差不到10%',
    'the measured slope is larger than the local linear prediction': '实测斜率大于局部线性预测',
    'the measured slope is smaller than the local linear prediction': '实测斜率小于局部线性预测',
    "f'the threshold was reached after {int(hit):,} updates'": '在{int(hit):,}次更新后达到了阈值',
    'f"the threshold was not reached within the cap of {int(record[\'cap\']):,} updates"': "在{int(record['cap']):,}次更新的上限内，没有达到阈值",
    'the threshold crossing is unresolved; no converged step count is reported': '阈值是否越过仍未解决；不报告已经收敛的步数',
    'Momentum has a smaller final position-error norm over this equal update budget.': '相同更新预算下，动量的最终位置误差范数更小。',
    'Momentum does not have a smaller final position-error norm over this equal update budget.': '相同更新预算下，动量的最终位置误差范数并没有更小。',
    "f'The first sampled step size whose norm after one hundred updates exceeds its initial norm is {edge:.3f}.'": '在抽样步长里，100次更新后的范数首次超过初始范数，对应的步长是{edge:.3f}。',
    'No sampled step size has a norm after one hundred updates above its initial norm.': '没有一个抽样步长，在100次更新后的范数超过初始范数。',
    'The comparison solver did not report success; agreement is not established.': '比较求解器没有报告成功，因此尚未建立一致性。',
    'The comparison solver reports success, but a finite probability comparison is unavailable.': '比较求解器报告成功，但无法得到有限的概率比较。',
    'The comparison solver reports success and agrees within the stated probability tolerance.': '比较求解器报告成功，并且在给定的概率容差内一致。',
    "f'The comparison solver reports success, but its largest probability difference is {difference:.6f}, outside the stated tolerance.'": '比较求解器报告成功，但最大的概率差为{difference:.6f}，超出了给定容差。',
    'The optimizer reports success; constraint and stationarity residuals are at most one millionth.': '优化器报告成功，约束和驻点残差都不超过百万分之一。',
    'The numerical candidate has not passed all stated solver, feasibility and stationarity checks.': '数值候选点尚未通过全部求解器、可行性和驻点检查。',
    'Both optimizers report success and all listed feasibility, stationarity, slackness and gap checks pass their tolerances.': '两个优化器都报告成功；给出的可行性、驻点、互补松弛和间隙检查，都通过各自的容差。',
    'The candidate solutions have not passed all solver and residual checks; the displayed values are not certified optima.': '候选解尚未通过全部求解器和残差检查，显示的数值不是经过认证的最优值。',
    'a finite geometric-rate comparison is unavailable': '无法得到有限的几何速率比较',
    'within 0.15 of the spectral radius in this measured fit': '在这次实测拟合里，与谱半径相差不到0.15',
    'slower than the spectral-radius reference in this measured fit': '在这次实测拟合里，比谱半径参考所示的收敛更慢',
    'faster than the spectral-radius reference in this measured fit': '在这次实测拟合里，比谱半径参考所示的收敛更快',
    'f"the iteration met its residual tolerance after {int(record[\'iterations\'])} updates"': "迭代在{int(record['iterations'])}次更新后满足了残差容差",
    'f"the iteration hit its cap of {int(record[\'cap\'])} updates before meeting the residual tolerance"': "迭代在满足残差容差之前，达到了{int(record['cap'])}次更新的上限",
    'the iteration has a non-finite result; a converged fixed point is unavailable': '迭代结果非有限，无法得到已经收敛的不动点',
    'a finite comparison floor is unavailable': '无法得到有限的比较平台',
    'the final comparisons include a numerically zero gradient difference': '最后几次比较中，出现了数值上为0的梯度差',
    "f'the smallest final gradient-comparison difference is {floor:.6g}'": '最后几次梯度比较的最小差异是{floor:.6g}',
    'a finite first-to-final loss comparison is unavailable': '无法得到有限的初始与最终损失比较',
    'the final recorded loss is lower than the initial loss': '最后记录的损失低于初始损失',
    'the final recorded loss is higher than the initial loss': '最后记录的损失高于初始损失',
    'the initial and final recorded losses are equal': '初始和最终记录的损失相同',
    'f"The fitted per-step factor is {d[\'rate\']:.3f}, {verdict}."': "拟合的每步倍数是{d['rate']:.3f}，{verdict}。",
    'A finite fitted per-step gradient-gap factor is unavailable.': '无法得到有限的每步梯度差拟合倍数。',
    "f'mean iteration work increases from {it[0, 1]:.0f} updates initially to {it[-1, 1]:.0f} finally'": '平均迭代开销，从最初{it[0, 1]:.0f}次更新，增加到最后{it[-1, 1]:.0f}次',
    "f'mean iteration work is {it[0, 1]:.0f} updates initially and {it[-1, 1]:.0f} finally'": '平均迭代开销，最初为{it[0, 1]:.0f}次更新，最后为{it[-1, 1]:.0f}次',
    'f"Of {training[\'count\']} training solves, {training[\'converged\']} converged, {training[\'capped\']} hit the cap and {training[\'nonfinite\']} were non-finite."': "{training['count']}次训练求解中，{training['converged']}次收敛，{training['capped']}次达到上限，{training['nonfinite']}次结果非有限。",
}

PHRASES = {
    # Jacobian
    'Only near a gain of one does it hold steady.': '只有增益接近1时，它才保持稳定。',
    'Even near a gain of one it drifts.': '即使增益接近1，它也会漂移。',
    # Gradient
    'exactly as the inequality says': '正如不等式所说',
    'close to what the inequality says': '和不等式所说的很接近',
    # Newton
    # HVP
    # Quadratic
    'match the formula to rounding error': '和公式一致到舍入误差',
    'match the formula closely': '和公式非常接近',
    'just as predicted': '正如预测',
    'close to the prediction': '与预测很接近',
    # KKT
    'agree to every digit shown': '显示出来的每一位都一致',
    'agree to six digits': '一致到六位数字',
    'Gradient descent': '梯度下降',
    'Newton': '牛顿法',
    'gradient norm': '梯度范数',
    'objective gap to the numerical reference': '相对数值参考解的目标函数差',
    'converged': '已收敛',
    'capped': '达到迭代上限',
    'nonfinite': '非有限值',
    'reference-unconverged': '参考解未收敛',
}
