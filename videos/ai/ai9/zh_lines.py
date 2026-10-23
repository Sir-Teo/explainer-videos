"""Chinese narration for ai9: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第9部分：神经网络'

CHAPTERS = {
    'Hook': '我们是怎么走到这里的',
    'Neurons': '1. 最早的神经元',
    'Perceptron': '2. 感知机在学习',
    'XOR': '3. 异或，以及第一次寒冬',
    'Backprop': '4. 反向传播',
    'Universal': '5. 一层，无所不能',
    'Barron': '6. 摆脱维数灾难',
    'Depth': '7. 深度带来了什么',
    'Revival': '8. 第二次寒冬，与复兴',
    'Init': '9. 推导初始化',
    'Chaos': '10. 混沌的边缘',
    'Residual': '11. 残差流',
    'Norm': '12. 归一化',
    'Block': '13. 现代的块',
    'KAN': '14. 柯尔莫哥洛夫–阿诺德网络',
    'NeuralLM': '15. 神经语言模型',
    'Outro': '回顾、习题，以及这些想法会在哪里再现',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'In 1943, a neurophysiologist and a young logician wrote down the first artificial neuron':
        "1943年，一位神经生理学家和一位年轻的逻辑学家，写下了第一个人工神经元：一个把输入加起来、总和够大就放电的单元。<bookmark mark='a'/>15年后，弗兰克·罗森布拉特造出了一个能从例子中学习的神经元，《纽约时报》报道说，海军希望它有一天能走路、能说话。<bookmark mark='b'/>1969年，一本书证明了单层这样的单元做不到什么，此后十年，很少有人再研究它们。<bookmark mark='c'/>1986年，反向传播训练出了夹在中间的隐藏层，<bookmark mark='d'/>网络学会了读手写的邮政编码。<bookmark mark='e'/>可是到了九十年代末，它们又一次过时了。<bookmark mark='f'/>2006年，人们找到了训练深层网络的办法；2012年，一个深层网络以巨大的优势赢下了ImageNet比赛。从那以后，这个领域再也没有回头。",

    'Here is what a network does, in one picture.':
        "网络在做什么，一张图就能说清。两条螺旋，彼此缠绕。没有哪条直线能把它们分开。<bookmark mark='a'/>这是一个小小的神经网络，3层，每层32个简单的单元，还没有经过任何训练。那些细线把平面切成一块一块，在每一块上，这个网络都恰好是线性的。<bookmark mark='b'/>现在，开始训练它。",

    "'The pieces swing around, and the boundary between the colours bends to follow the spirals, ' + verdict":
        "这些小块四处转动，两种颜色之间的边界也弯过来顺着螺旋走，{verdict}<bookmark mark='a'/>网络就是这么回事：许多平的小块，拼接在一起，由梯度下降摆放到位。这一部分讲的是：为什么这样行得通，是谁发现的，以及要让它行得通，需要些什么。",

    "f'until {100 * acc:.0f} percent of the points are on the right side.":
        '直到{100 * acc:.0f}%的点落在正确的一侧。',

    "f'and {100 * acc:.0f} percent of the points end up on the right side.":
        '最后{100 * acc:.0f}%的点落在正确的一侧。',

    'This is Part 9 of AI, Built, in the second act: learning from data.':
        "这是《人工智能，从零搭建》的第9部分，属于第二幕：从数据中学习。<bookmark mark='a'/>这一部分讲：感知机和它的证明；反向传播；网络能表示什么；深层网络为什么难训练，以及修正的办法；今天语言模型里的那种块；还有登上我们记分牌的一个神经语言模型。",

    # ------------------------------------------------------------------ Neurons
    'Chapter one. The first neurons.':
        '第1章。最早的神经元。',

    'In 1943, Warren McCulloch, a neurophysiologist, and Walter Pitts':
        "1943年，神经生理学家沃伦·麦卡洛克和年轻的逻辑学家沃尔特·皮茨，发表了《神经活动中内在思想的逻辑演算》。他们的神经元是一个开关。<bookmark mark='a'/>它的输入是0或1，每个输入都带着一个权重进来。<bookmark mark='b'/>当加权和达到一个阈值时，这个单元就放电，输出1。<bookmark mark='c'/>两个权重都取1、阈值取2，只有两个输入都打开时它才放电：这就是“与”。<bookmark mark='d'/>把阈值降到1，任何一个输入打开它就放电：这是“或”。<bookmark mark='e'/>一个输入、权重取负1、阈值取0，就得到“非”。用与、或、非，可以搭出任何逻辑公式，所以这些单元组成的网络，能算出逻辑电路能算的任何东西。可是每个权重都是手工设定的。什么也没有学。",

    'Where would learning come from? In 1949 the psychologist Donald Hebb':
        "学习从哪里来？1949年，心理学家唐纳德·赫布针对真实的神经元，提出了一个答案。<bookmark mark='a'/>当细胞A的轴突离细胞B足够近、能够激发它，并且反复地、持续地参与让它放电时，一个或两个细胞里就会发生某种生长过程或代谢变化，使得A作为让B放电的细胞之一，效率提高了。<bookmark mark='b'/>用符号来说：一条连接加强的幅度，和它两端的活动成正比。几十年后，人们把它概括成一句话：一起放电的细胞，连在一起。",

    'In 1958 Frank Rosenblatt, a psychologist at the Cornell Aeronautical Laboratory':
        "1958年，康奈尔航空实验室的心理学家弗兰克·罗森布拉特，把这两个想法放在了一起：一个麦卡洛克–皮茨单元，它的权重从例子中学出来。他把它叫作感知机。<bookmark mark='a'/>那年7月，他在一台IBM 704计算机上模拟演示了它：试了50次之后，它自己学会了区分标记在左边的卡片和标记在右边的卡片。<bookmark mark='b'/>《纽约时报》报道说，海军期待这台机器能走路、说话、看、写字、复制自己，并且意识到自己的存在。<bookmark mark='c'/>然后他把它造了出来。1960年展出的Mark I感知机，有一台由400个光电管组成的相机，20乘20，随机地连到512个联想单元上，这些单元再连到8个响应单元。<bookmark mark='d'/>它的权重是电位器，在它学习的时候由电动机转动。",

    'Two years later, at Stanford, Bernard Widrow and his student Ted Hoff':
        "两年后，在斯坦福，伯纳德·威德罗和他的学生特德·霍夫造出了ADALINE，一个自适应线性神经元，用的是另一条规则。<bookmark mark='a'/>感知机只在犯错之后才改权重，而且一改就是整个输入。<bookmark mark='b'/>威德罗和霍夫则写下一个例子上的平方误差，取的是阈值之前的值，<bookmark mark='c'/>求出它的梯度，<bookmark mark='d'/>然后在每个例子上都往下坡走一小步，步子和误差成正比。<bookmark mark='e'/>这就是最小均方规则，它就是随机梯度下降：本系列里训练每一个网络的那种更新，也是第11部分的主题。",

    # ------------------------------------------------------------------ Perceptron
    'Chapter two. The perceptron learns.':
        '第2章。感知机在学习。',

    "Here is Rosenblatt's learning rule, in modern notation.":
        "这是罗森布拉特的学习规则，用今天的记号来写。每个例子是一个点x，带着一个标签y，取正1或负1。<bookmark mark='a'/>感知机预测w点乘x的符号：也就是这个点落在w点乘x等于0的那条线的哪一侧。权重w是一根箭头，和那条线垂直。<bookmark mark='b'/>当它把一个例子判错时，就把y乘x加到w上。<bookmark mark='c'/>对一个落在错误一侧的正例来说，这会让箭头朝这个点转过去，那条线也随之摆动，把这个点放到它该在的一侧，至少离那一侧更近。就这么简单。再加一个恒为1的输入，这条线就有了偏置，不必穿过正中间。",

    'f"Here it is on {len(X)} points that some line can separate.':
        "这是它在{len(X)}个点上的表现，这些点可以被某条直线分开。一开始，它所有的权重都是0。<bookmark mark='a'/>每当它遇到一个落在错误一侧的点，那条线就跳一下。<bookmark mark='b'/>第一遍过数据，它犯了{pe[0]}次错，之后几遍又犯了{sum(pe[1:])}次。<bookmark mark='c'/>一共犯了{k}次错之后，整整一遍下来一次错也没有，它就停了：每个点都在自己的一侧。",

    'Is it guaranteed to stop? In 1962 Albert Novikoff proved':
        "它一定会停下来吗？1962年，阿尔伯特·诺维科夫证明：只要有某条直线能把数据分开，它就一定会停。<bookmark mark='p1'/>假设每个点到原点的距离都不超过R，<bookmark mark='p2'/>并且有某个单位向量w星，能把每个点放在它该在的一侧，还留有余地，这个余量叫作间隔γ。<bookmark mark='a'/>盯住两个数。第一个，w和w星的吻合程度。每犯一次错，就加上y x，而y x点乘w星至少是γ。<bookmark mark='b'/>所以犯了k次错之后，吻合程度至少是k乘γ：它和k成正比地增长。<bookmark mark='c'/>第二个，w的长度。犯错意味着y乘w点乘x不是正的，所以中间那一项帮不上忙：长度的平方，每次最多增加R的平方。<bookmark mark='d'/>犯了k次错之后，最多是k乘R的平方：长度只按k的平方根增长。<bookmark mark='e'/>可是和一个单位向量的吻合程度，永远不会超过长度。所以k乘γ，最多是根号k乘R。<bookmark mark='f'/>两边平方再相除：犯错的次数，最多是R除以γ的平方。一个按k增长的量，不可能长久地待在一个按根号k增长的量下面。",

    "That's the perceptron convergence theorem.":
        '这就是感知机收敛定理。这个上界和有多少个点无关，也和它们来的顺序无关，只取决于两类之间留了多大的空隙。',

    'f"For our points, R is {R:.2f} and the best margin gamma is {gamma:.3f}':
        "对我们这些点来说，R是{R:.2f}，最好的间隔γ是{gamma:.3f}，所以定理允许最多{bound:.0f}次错。它实际犯了{k}次。<bookmark mark='a'/>一个数据集接一个数据集地缩小间隔，在每个数据集上用不同的顺序把感知机跑20遍。<bookmark mark='b'/>上界总是成立，而且它很悲观：最差的一次，也只用掉了它的{100 * ratio:.0f}%。<bookmark mark='c'/>有两件事，这个定理并不保证。它找到的是一条能分开数据的线，而不是间隔最宽的那一条；找那一条，是第6部分的支持向量机。而如果没有任何直线能分开数据，感知机就永远停不下来。",

    # ------------------------------------------------------------------ XOR
    'Chapter three. XOR, and the first winter.':
        '第3章。异或，以及第一次寒冬。',

    'f"Here is the simplest thing a single unit cannot do.':
        "这是单个单元做不到的最简单的事。异或：恰好有一个输入打开时才放电。<bookmark mark='a'/>假设有一个阈值单元能做到。输入0、0不能放电，所以阈值是正的。<bookmark mark='b'/>每个输入单独打开时都必须放电，所以每个权重都至少是θ。<bookmark mark='c'/>两个一起打开时不能放电，所以两个权重加起来小于θ。<bookmark mark='d'/>可是把中间那一行加起来，它们至少是2倍θ，比θ大。矛盾了：没有哪条直线能把两个蓝点放在一侧、两个粉点放在另一侧。<bookmark mark='e'/>硬让感知机去跑，它永远也稳定不下来：在{n}遍里的每一遍，它都犯{min(xe)}到{max(xe)}次错。",

    'In 1969 Marvin Minsky and Seymour Papert of MIT published Perceptrons':
        "1969年，麻省理工学院的马文·明斯基和西摩·派珀特出版了《感知机》，一本用严谨的定理讨论这些机器能算什么的书。<bookmark mark='a'/>单层可训练的权重算不出奇偶性，也分不清一个图形是连通的还是断开的，除非它的某些单元一下子就能看到几乎整幅图。<bookmark mark='b'/>层数更多的网络能做得更多，他们也知道，但没有人知道怎么训练它们。对于这样的机器，作者写道：阐明或者推翻“这种扩展是贫瘠的”这一直觉判断，是一个重要的研究问题。<bookmark mark='c'/>1971年，罗森布拉特在一次划船事故中去世。经费和学生都转向了第2部分讲的符号主义人工智能。<bookmark mark='d'/>整个七十年代，只有少数人坚持了下来；福岛邦彦1980年的新认知机，是第10部分卷积网络的祖先；约翰·霍普菲尔德1982年的网络，又把物理学家们拉回了这个领域。",

    "What a single unit can't do, two layers can.":
        "单个单元做不到的，两层可以。在中间放两个单元，藏在输入和输出之间，然后用梯度下降训练所有的权重，用的是本系列第4部分自己写的自动微分。<bookmark mark='a'/>左边是输入的正方形，按网络对每一点的判断着色。<bookmark mark='b'/>右边是隐藏层眼中的同一个正方形：每一条网格线，都被两个tanh单元弯折过了；那条黄线，是输出单元画的直线。",

    'f"Now train. <bookmark mark=\'a\'/> The hidden layer bends and folds the square':
        "现在开始训练。<bookmark mark='a'/>隐藏层把正方形弯折起来，直到两个蓝点落在一条直线的一侧，两个粉点落在另一侧。这时，只会画直线的输出单元，任务就很轻松了。损失从{l0:.2f}降到{l1:.4f}。<bookmark mark='b'/>{caveat}",

    'f"One honest caveat: from {starts} random starts, {solved} found a solution like this.':
        '说句实话：从{starts}个随机起点出发，只有{solved}个找到了这样的解。其余的都卡住了，有一个点判错，困在损失的一个局部极小值里。这里放的是没有卡住的一个。',

    "f'All {starts} random starts found a solution like this one.":
        '{starts}个随机起点全都找到了这样的解。',

    # ------------------------------------------------------------------ Backprop
    'Chapter four. Backpropagation.':
        '第4章。反向传播。',

    'XOR showed what was missing: a way to train the units in the middle.':
        "异或暴露了缺的是什么：一种训练中间那些单元的方法。在输出端，误差一目了然：把答案和目标比一比。<bookmark mark='a'/>可是一个隐藏单元该负多大的责任？它对损失的影响，要经过它后面的每一个单元。<bookmark mark='b'/>把网络一层一层地写出来。一层的加权和z，等于一个权重矩阵乘上一层的输出，再加偏置；它的输出a，是用非线性函数φ把z弯折一下；损失取决于最后一层。<bookmark mark='c'/>第4部分的链式法则能回答这个问题，而且可以把它组织起来，只往回扫一遍，就同时回答每一个权重的问题。",

    'Define delta for a layer: how much the loss changes':
        "为每一层定义一个δ：这一层的加权和变化时，损失变化多少。<bookmark mark='a'/>在最顶层，它是现成的：损失对输出的梯度，乘上每个单元处弯折的斜率。<bookmark mark='b'/>现在往下走一层。第l层的和，只能通过它的输出影响损失，而输出又只能通过下一层的和影响损失。链式法则说：拿下一层的δ，通过同一个权重矩阵的转置送回来，再乘上弯折的斜率。<bookmark mark='c'/>一旦知道了一层的δ，它的权重的梯度，就是δ乘上进入这一层的输出，因为这些和对权重是线性的。<bookmark mark='d'/>两行公式，从顶层开始一层一层地用下去：这就是反向传播。",

    'Picture it as traffic.':
        "把它想成交通。<bookmark mark='a'/>前向传播时，数值往上流：每一层乘上自己的权重，再弯折一下。<bookmark mark='b'/>在顶上，损失把答案和目标比一比。<bookmark mark='c'/>反向传播时，误差沿着同样的导线往下流，经过转置后的矩阵，在每个单元处乘上它的弯折斜率，每一个权重都在误差经过时拿到自己的梯度。<bookmark mark='d'/>停下来预测一下：反向传播比前向传播贵多少？<bookmark mark='e'/>往回走时，每一层要做两次矩阵乘法，一次算δ，一次算权重的梯度；往前走只做一次。所以训练一步大约要花三次前向传播的代价，每个权重、每个例子大约6次算术运算。这个6会在第12部分再出现，就在估算训练语言模型的代价的那个公式里。",

    '"Let\'s check it on chapter three\'s XOR network, at random weights.':
        "我们在第3章的异或网络上，随便取一组权重，检验一下。<bookmark mark='a'/>这是它的9个梯度，用三种方法算出来：一种来自本系列自己的自动微分，它对网络一无所知；<bookmark mark='b'/>一种来自手写出来的δ公式；<bookmark mark='c'/>还有一种是蛮力法，把每个权重往上和往下各推一百万分之一，看损失怎么变。<bookmark mark='d'/>{agreement}",

    'They agree to the last printed digit.':
        '它们一直吻合到最后一位显示的数字。反向传播不是近似：它就是精确的梯度，扫一遍就全算出来，而蛮力法每个权重都要做两次前向传播。',

    "They agree to within the finite differences' own rounding.":
        '它们吻合到有限差分本身的舍入误差之内。反向传播就是精确的梯度，扫一遍就全算出来，而蛮力法每个权重都要做两次前向传播。',

    'The idea was found more than once.':
        "这个想法不止一次被人发现。<bookmark mark='a'/>1970年，芬兰的硕士生塞波·林纳因马描述了自动微分的反向模式，那时还完全没有网络的影子。<bookmark mark='b'/>1974年，保罗·韦伯斯在哈佛的博士论文里提出用这种方法训练网络，几乎没人注意。<bookmark mark='c'/>1986年，戴维·鲁梅尔哈特、杰弗里·辛顿和罗纳德·威廉斯在《自然》上表明：用反向传播误差训练出来的网络，能在隐藏单元里学到有用的特征，这个领域醒了过来。<bookmark mark='d'/>到1989年，杨立昆在贝尔实验室的网络已经在读手写的邮政编码了。隐藏层能训练了。下一个问题：它们能表示什么？",

    # ------------------------------------------------------------------ Universal
    'Chapter five. What one layer can do.':
        '第5章。一层能做到什么。',

    'Backpropagation can train any layer. So what can layers represent?':
        "反向传播能训练任何一层。那么，层能表示什么？先从一个单元说起，按今天网络的造法。它接收一些数，<bookmark mark='a'/>把每个数乘上一个权重再加起来，再加一个常数，和第6部分的逻辑回归一模一样，<bookmark mark='b'/>然后把结果弯折一下：小于0的都变成0。这个弯折叫作线性整流单元，也就是ReLU，2010年前后，它取代了平滑的S形曲线。<bookmark mark='c'/>沿着任何一个输入看，一个单元就是一个合页：先是平的，然后往上升。",

    'f"Add hinges together, each with its own position and slope':
        "把一个个合页加起来，每个都有自己的位置和斜率，就能画出一条曲线。<bookmark mark='a'/>两个合页，画出一条粗糙的折线。<bookmark mark='b'/>4个。8个。16个。64个，典型误差降到了{e64:.4f}。",

    'f"How fast does the miss shrink?':
        "误差缩小得有多快？<bookmark mark='p'/>在合页处把点连起来，得到一段段直的弦；在宽度为h的一段上，弦和一条光滑曲线的差距，最多是h的平方除以8，再乘上曲线的弯曲程度。<bookmark mark='a'/>n个合页均匀分布在区间上，h就是n加1分之6。<bookmark mark='b'/>所以误差按n的平方分之1下降：合页加倍，误差变成4分之1。最小二乘只会比连点做得更好。<bookmark mark='c'/>在双对数坐标上，这是一条斜率为负2的直线，实测的斜率是{slope:.2f}。",

    "Here's another way to see it.":
        "还有一种看法。<bookmark mark='a'/>取三个合页：一个往上，一个以两倍的陡度往下，再一个往上。<bookmark mark='b'/>它们的和是一个鼓包：先是0，升上去，降下来，再回到0。<bookmark mark='c'/>在一排点上各放一个鼓包，每个鼓包的高度等于曲线在那里的高度，再把它们加起来：就得到了这条曲线，用折线把点连起来。<bookmark mark='d'/>任何连续曲线都能这样画出来，想多精细就多精细。在更高的维度里，每个鼓包要用更多的单元，但这个想法依然成立。",

    "That's the universal approximation theorem, proved in 1989":
        "这就是万能近似定理。1989年，乔治·切本科对S形单元证明了它，库尔特·霍尼克、马克斯韦尔·斯廷奇库姆和哈尔伯特·怀特证明了一般的情形。1993年，摩西·莱什诺和同事们把它说清楚了：任何连续的激活函数都行，只要它不是多项式。<bookmark mark='a'/>它说的是，网络能表示出答案。<bookmark mark='b'/>它没说需要多少个单元，<bookmark mark='c'/>也没说训练能不能找到它们，<bookmark mark='d'/>也没说从例子里学到的东西，在新例子上还管不管用，那是第8部分的主题。第一个问题，有一个出人意料的答案。",

    # ------------------------------------------------------------------ Barron
    'Chapter six. Escaping the curse of dimensionality.':
        '第6章。摆脱维数灾难。',

    'One layer can draw anything; how many units does it take?':
        "一层能画出任何东西；那要多少个单元？一张表格也能做同样的事，网格上的每个点存一个值，而在一维里，连点正好就是一层合页。<bookmark mark='a'/>可是每个轴上放m个点的网格，在d维里就有m的d次方个点。<bookmark mark='b'/>反过来说：有n个点可以用，间距就是n的负d分之1次方，<bookmark mark='c'/>误差按n的负d分之2次方缩小。<bookmark mark='d'/>在100维里，要把误差减半，点数就得乘上2的50次方。这就是维数灾难，这个说法来自理查德·贝尔曼。",

    'In 1993 Andrew Barron showed that networks escape this':
        "1993年，安德鲁·巴伦证明，对一大类函数来说，网络能摆脱这个灾难，而原因一屏就写得下。取一个光滑的鼓包，一个d维的高斯函数。<bookmark mark='a'/>它恰好是一堆余弦波的平均，每个方向ω一个，按它的傅里叶变换加权。<bookmark mark='b'/>随机抽出n个方向，只对这n个波取平均：这就是一个有n个单元的网络，每个单元是一个方向上的波。<bookmark mark='c'/>在任何一点上，这都是n次独立抽样的平均，所以它的平方误差，等于一次抽样的方差除以n。<bookmark mark='d'/>余弦值在负1和1之间，所以误差最多是n分之1，哪里都没有d。<bookmark mark='e'/>既然随机的单元平均来说能做到这么好，就一定有某一组具体的n个单元做得至少一样好，在任何维度里都是。这个论证来自概率论，属于伯纳德·莫雷。",

    'f"Here it is, computed.':
        "这是算出来的结果。<bookmark mark='a'/>先看网格，在1维、2维、4维和8维里：线越来越平，斜率分别是{gs[1]:.1f}、{gs[2]:.1f}、{gs[4]:.2f}和{gs[8]:.2f}，接近负d分之2。在8维里，{g8n:,}个点的误差仍有{g8:.3f}。<bookmark mark='b'/>再看n个随机的余弦单元，在1维、4维、16维和64维里。四条线叠在一起，斜率在{min(sl.values()):.2f}到{max(sl.values()):.2f}之间：误差按n的平方根分之1下降，和维数无关。在64维里，{int(ns[-1]):,}个单元的误差是{mc64:.4f}。",

    "Barron's theorem says this for ordinary S-shaped units":
        "巴伦定理对普通的S形单元也说了同样的事，适用于每一个这样的函数：它的傅里叶变换按频率加权后，总量C f是有限的。平方误差最多是2 r C f的平方，除以n。<bookmark mark='a'/>他还证明了固定的基做不到什么：在你看到f之前就选好的任何n个函数，比如网格的那些，在这一类函数上最多只能做到n的负d分之1次方。网络之所以能摆脱，是因为它会按f来挑选单元的方向。<bookmark mark='b'/>代价是：对粗糙、起伏剧烈的函数，C f可能大得惊人，而且这个定理完全不管梯度下降能不能找到这些单元。不过，这是第一个线索，说明网络为什么能在高维里工作。",

    # ------------------------------------------------------------------ Depth
    'Chapter seven. What depth adds.':
        '第7章。深度带来了什么。',

    'If one layer can do anything, why stack them?':
        "既然一层就无所不能，为什么还要把层叠起来？答案就在一张图里。两个单元组成一顶帐篷：从0升到1，再降回来。<bookmark mark='a'/>把这顶帐篷送进另一顶帐篷，这条线就被折了两次：4段。<bookmark mark='b'/>3层，8段。5层，32段。每多一层，段数就翻一倍，而一层宽的网络，每加一个单元只多一段。<bookmark mark='c'/>2016年，马特乌斯·泰尔加斯基把它变成了一个定理：有些函数，又深又窄的网络能精确算出来，浅的网络却需要指数级多的单元。",

    'In two dimensions the same trick folds the plane.':
        "在二维里，同样的技巧会折叠平面。这是一个画着图的正方形：一个F，这样你就能分清它的镜像。<bookmark mark='a'/>一层ReLU可以算出x的绝对值的2倍减1：这会把正方形沿中线对折，再把这一半拉伸回原来的大小。<bookmark mark='b'/>现在按每个输入点落到哪里给它上色：图出现了两个互为镜像的副本。<bookmark mark='c'/>沿另一个方向再折一次：4个。然后是8个、16个、32个。<bookmark mark='d'/>每一层都让线性小块的数目翻倍，而网络其余部分在折好的正方形上画的任何东西，都会同时画进每一块里，带着镜像。深层网络可以重复利用它已经搭好的东西。",

    "Let's count pieces properly.":
        "我们来正式数一数小块。第一层的每个单元，都是平面上的一条线：一侧关闭，另一侧打开。<bookmark mark='a'/>处于一般位置的n条线，最多把平面切成1加n再加n选2块，这个经典的计数，1975年由托马斯·扎斯拉夫斯基推广到了超平面。<bookmark mark='b'/>对随机的线直接数一数，结果吻合。在平面上按n的平方增长；在d维里按n的d次方增长。<bookmark mark='c'/>深层网络能好得多：2014年，吉多·蒙图法尔和同事们证明，最大数目随深度指数增长，正如那些折叠所暗示的。",

    "f\"But that's what depth can do, with weights chosen by hand.":
        "不过，这只是深度在手工挑选权重时能做到的事。随机的网络又会怎样？这里是48个单元在切分平面，先排成1层，然后是2层、3层、4层和6层。<bookmark mark='a'/>小块的数目{trend}。2019年，鲍里斯·哈宁和戴维·罗尔尼克证明：在初始化时，典型网络的小块数大约是单元数的输入维数次方，远远不到最大值；他们在训练过程中也发现了同样的情况。<bookmark mark='b'/>我们的螺旋网络一开始有{n0:,}块，最后有{n1:,}块：{change}。深度的帮助来得更微妙：它让有用的函数，更容易被训练找到。",

    'training rearranged the pieces far more than it multiplied them':
        '训练主要是在重新摆放这些小块，而不是增加它们',

    # ------------------------------------------------------------------ Revival
    'Chapter eight. The second winter, and the revival.':
        '第8章。第二次寒冬，与复兴。',

    'f"Through the nineties, backpropagation worked for networks with one or two hidden layers.':
        "整个九十年代，反向传播对只有一两个隐藏层的网络是管用的。更深的网络几乎训练不动。<bookmark mark='a'/>1991年，慕尼黑的学生塞普·霍赫赖特找到了原因。到达前面某一层的梯度，是它上面每一层贡献一个因子的乘积，而这些因子很少接近1。<bookmark mark='b'/>这是一个50层的S形单元网络，按当年通常的方式设置，从顶上送下一个梯度。每一层都要把它乘上sigmoid的斜率，最多4分之1，再乘上权重：每层大约缩小{per:.1f}倍。<bookmark mark='c'/>到第一层时，它只剩10的负{e}次方。前面那几层，还不如冻住算了。",

    'Meanwhile, other methods were winning.':
        "与此同时，别的方法在赢。<bookmark mark='a'/>1995年，科琳娜·科尔特斯和弗拉基米尔·瓦普尼克提出了支持向量机：它是凸的，所以训练总能找到最好的答案，背后还有一套泛化理论。<bookmark mark='b'/>网络还守着几块阵地：1997年的LSTM，专门用来让梯度穿过时间，<bookmark mark='c'/>还有杨立昆的卷积网络，到九十年代末已经在读手写字和银行支票了。<bookmark mark='d'/>但对这个领域的大多数人来说，深层网络难训练，更难分析，注意力转向了核方法和图模型。对网络来说，这是第二次寒冬。",

    'A small community kept going, supported from 2004':
        "一个小圈子坚持了下来，从2004年起，得到了加拿大一个由杰弗里·辛顿领导的研究项目的支持。2006年，他和同事们找到了训练深层网络的办法。<bookmark mark='a'/>不要一次训练所有的层。先让一层在没有标签的情况下，学会为数据建模。<bookmark mark='b'/>把它冻住，再让下一层学会为第一层的输出建模；<bookmark mark='c'/>就这样一层层往上。<bookmark mark='d'/>然后用反向传播把所有层一起微调，从这些合理的权重出发，而不是从随机的权重出发。他们把它叫作深度信念网络；同一年，约书亚·本吉奥的团队和其他人也有类似的工作，“深度学习”这个名字就此叫开了。",

    'Then, within a few years, the pretraining turned out not to be needed.':
        "然后，没过几年，人们发现这种预训练其实不需要。<bookmark mark='a'/>显卡让训练快了很多倍；2010年，丹·奇雷尚和同事们用普通的深层网络、普通的反向传播，在手写数字上创下了纪录。<bookmark mark='b'/>更好的初始权重，来自泽维尔·格洛罗和约书亚·本吉奥，再加上ReLU，让信号得以存活。<bookmark mark='c'/>2012年，深层网络接管了语音识别，又凭借AlexNet接管了图像识别：那是第10部分的故事。<bookmark mark='d'/>2018年，本吉奥、辛顿和杨立昆共同获得了图灵奖。<bookmark mark='e'/>这一部分剩下的内容，会把这些修正办法一个一个讲清楚，连同它们的数学：初始化、混沌的边缘、残差流和归一化。",

    # ------------------------------------------------------------------ Init
    'Chapter nine. Initialization, derived.':
        '第9章。推导初始化。',

    'f"Before training, the weights are random. But random how?':
        "训练开始之前，权重是随机的。可是，怎么个随机法？关键在于它们的分散程度：这些随机的初始权重，离0有多远。让一个信号穿过50层，盯住它的大小。<bookmark mark='a'/>如果抽出的权重稍微小了一点，每一层都会把信号缩小固定的倍数。穿过50层之后，它缩小了大约{spoken(shrink)}倍：没了。<bookmark mark='b'/>如果稍微大了一点，它就会爆炸，涨到大约{spoken(grow)}。<bookmark mark='c'/>只有一种大小，能让它一层又一层地保持平稳。而梯度往回流的时候，也会以同样的方式消失或者爆炸。",

    'The right size follows from one line of probability.':
        "合适的大小，可以从一行概率推出来。<bookmark mark='a'/>一个单元把它的n个输入各乘一个权重，再加起来。<bookmark mark='b'/>如果权重彼此独立、均值为0，各项的方差就可以相加：和的方差，等于n乘权重的方差，再乘输入的典型平方。<bookmark mark='c'/>对于在0附近的tanh单元，输出约等于输入，所以要让方差一层一层保持不变，权重的方差就应该是n入分之1。<bookmark mark='d'/>往回走时，梯度要在它所连到的单元上求和，经过的是转置矩阵：这要求n出分之1。<bookmark mark='e'/>2010年，泽维尔·格洛罗和约书亚·本吉奥取了个折中：两者之和分之2。杨立昆早在1998年就建议过n入分之1，那是为前向传播考虑的。",

    'A ReLU changes the bookkeeping.':
        "ReLU改变了这本账。<bookmark mark='a'/>这是在那个平稳的网络里，中间一层的单元在弯折之前收到的东西：一个对称的钟形。<bookmark mark='b'/>ReLU扔掉了负的那一半，所以它输出的均方，正好是输入方差的一半。<bookmark mark='c'/>为了补回来，把权重的方差加倍：n分之2。这就是何恺明初始化，来自何恺明和同事们2015年的工作，也就是一分钟前那条平稳的线。",

    'f"Here is the inside of a fifty-layer tanh network, as a landscape.':
        "这是一个50层tanh网络的内部，画成一片地形。每一道山脊，是一层输出的直方图，第1层在最前面，第50层在最后面。<bookmark mark='a'/>按老的经验法则，权重在正负根号n分之1之间均匀取值，输出一层一层地缩小，典型大小从{sd['tanh_std'][0]:.2f}缩到大约10的负{e_std}次方：山脊塌成了0处的一根尖刺。<bookmark mark='b'/>用格洛罗和本吉奥的方差，n分之1，它们一直保持舒展，只是慢慢变窄，到最后一层是{sd['tanh_xavier'][-1]:.2f}。<bookmark mark='c'/>把权重取得太大，单元就会饱和：输出堆积在负1和正1处。可是梯度并没有消失：到达第一层的梯度，是顶上那个的{gs['tanh_big'][0] / gs['tanh_big'][-1]:,.0f}倍。它爆炸了，下一章会解释为什么。",

    # ------------------------------------------------------------------ Chaos
    'Chapter ten. The edge of chaos.':
        '第10章。混沌的边缘。',

    'f"Why is there one right size?':
        "为什么恰好有一个合适的大小？2016年和2017年，本·普尔、萨姆·舍恩霍尔茨、苏里亚·甘古利、亚沙·索尔-迪克斯坦和同事们用物理学回答了这个问题：平均场理论。<bookmark mark='a'/>让网络变得非常宽。这样，每个单元在随机权重上的加权和，就是一个高斯分布，一个数就能描述整整一层：它的和的方差，q。<bookmark mark='b'/>一层把q映射到下一层：把tanh平方，对高斯分布取平均，乘上权重的方差，再加上偏置的方差。<bookmark mark='c'/>把这个映射和对角线画在一起，然后反复迭代：阶梯收敛到一个不动点，这里q星等于{qstar:.2f}。不管输入是什么，长度在几层之内就稳定下来了。有意思的问题，是两个输入会怎样。",

    'f"Send two different inputs through, and follow their correlation':
        "送两个不同的输入进去，一层一层地跟踪它们的相关系数c。相同的输入始终相同，所以c等于1永远是一个不动点。它是吸引还是排斥，取决于映射在那里的斜率，叫作χ1。<bookmark mark='a'/>权重小的时候，χ1是{chi['ordered']:.2f}，小于1：这是有序相。每一对输入都被拉到一起，直到网络对每个输入都给出同样的输出。<bookmark mark='b'/>权重大的时候，χ1是{chi['chaotic']:.2f}：这是混沌相。挨得很近的输入被推开，相关系数降到{ends['chaotic']:.2f}，网络把它看到的一切都搅乱了。<bookmark mark='c'/>在两者之间，χ1恰好等于1：这就是混沌的边缘，相关系数变化得很慢，关于输入的信息能撑过整趟旅程。{survive}<bookmark mark='d'/>这些点是一个宽度为1000的真实网络，理论和它吻合。而χ1，也正是梯度在回程中每一层被缩放的倍数：小于1就消失，大于1就爆炸，正如你刚才看到的。",

    "f'After {L} layers, their correlation is only":
        '过了{L}层，它们的相关系数只有{ends[\'critical\']:.2f}：两个输入仍然分得清。',

    "f'Even here, after {L} layers, they have nearly merged.":
        '即使在这里，过了{L}层，它们也几乎合在一起了。',

    'f"Here is the whole picture for tanh networks':
        "这是tanh网络的全景图：对权重和偏置的每一种分散程度，画出χ1。蓝色是有序，粉色是混沌，<bookmark mark='a'/>两者之间那条黄线就是边缘。<bookmark mark='b'/>看它在底部、也就是偏置为0的地方落在哪里：权重方差是n分之{x0:.2f}。这正是上一章格洛罗的规则。<bookmark mark='c'/>对ReLU单元做同样的计算，得到χ1等于σw的平方除以2，所以边缘落在n分之2：何恺明的规则。这些初始化规则不只是整齐的记账。它们把网络放在了混沌的边缘上。",

    '"How deep can a network be and still train?':
        "网络能有多深，还训练得动？理论给出一个深度尺度，ξc：一个相关性能撑过多少层才被遗忘。恰好在边缘上，它是无穷大。<bookmark mark='a'/>舍恩霍尔茨和同事们发现，网络只要比大约6个深度尺度浅，就能训练。我们试了试：从5层到100层深的tanh网络，取12种权重方差，每一个都在同一个小任务上用同样的方法训练。<bookmark mark='b'/>亮的表示学会了；暗的表示停在瞎猜的水平。<bookmark mark='c'/>{verdict}<bookmark mark='c2'/>{deepest}<bookmark mark='d'/>再往前推，这个想法在2018年训练出了一万层深的卷积网络，靠的只是一个精心的初始化。第12部分会针对Transformer再回到这个问题。",

    'f"The bright region hugs the line':
        "亮的区域紧贴着那条线：在{100 * agree:.0f}%的格子上，“深度低于6个深度尺度就恰好能训练”这条规则，预测对了我们的结果。",

    "f'The rule of thumb agrees with our result on":
        '这条经验法则在{100 * agree:.0f}%的格子上和我们的结果一致：我们的训练比他们的更短、规模更小，所以边界更粗糙。',

    "f'At {L_deep} layers, only weight variances near the edge train":
        '在{L_deep}层时，只有边缘附近的权重方差训练得动：{deep_list}。',

    "f'At {L_deep} layers, only weight variances near the edge still train":
        "在{L_deep}层时，只有边缘附近的权重方差还训练得动：{deep_list}；到{depths[-1]}层，在{t['steps']}步内一个也训练不动。",

    # ------------------------------------------------------------------ Residual
    'Chapter eleven. The residual stream.':
        '第11章。残差流。',

    'Good initialization gets a signal through at the start':
        "好的初始化，能让信号在一开始顺利通过，但在一叠很深的层里，训练还是可能出岔子。2015年12月，何恺明和同事们发表了一个修正办法，简单到如今无处不在。<bookmark mark='a'/>不要让每一层取代前面的结果，而是让它往上加一点。这样，每一层都变成一个小小的修正，作用在一股径直流过的数字流上：这就是残差流。<bookmark mark='b'/>按照链式法则，每个模块的导数，都是恒等映射再加上一点额外的部分。<bookmark mark='w'/>跳跃连接这条路，把梯度原封不动地传回去，就像一根普通的导线，所以梯度总有一条畅通的路，一直回到第一层。本系列的每一个Transformer，都是这样搭起来的。",

    'f"Here it is on the spirals, with forty layers of thirty-two units.':
        "在那两条螺旋上试一试，网络有40层，每层32个单元。<bookmark mark='a'/>普通的层叠{plain_says}。<bookmark mark='b'/>同样的40层，加上残差连接，{res_says}。同样的宽度，同样的优化器，同样的步数。",

    "never learns anything: it's stuck at a coin flip":
        '什么也学不会：一直停在抛硬币的水平',

    "f'learns only slowly, to {100 * pf:.0f} percent":
        '只学得很慢，达到{100 * pf:.0f}%',

    "f'learn the spirals completely, within {first:,} steps":
        '在{first:,}步之内，就把螺旋完全学会了',

    "f'reach {100 * rf:.0f} percent of the points":
        '把{100 * rf:.0f}%的点分对了',

    'f"Why does the plain stack never learn?':
        "为什么普通的层叠永远学不会？在它们训练的时候，看看两者的内部：上面是每个网络对平面上每一点的判断；下面是有多少梯度到达它的40层中的每一层，用对数刻度。<bookmark mark='a'/>一开始，普通层叠的梯度在往下传的路上一层一层地缩小：第一层得到的梯度，比最后一层少了超过{big}倍。残差层叠的梯度大小都差不多，相差不到{rr:.0f}倍，因为每个块都是往一条流上做加法，梯度可以沿着这条流直接流回去。<bookmark mark='b'/>所以随着训练进行，残差层叠的判断弯过来贴合螺旋，它的梯度也一起缩小了{('ten' if round(fade) == 1 else ['a hundred', 'a thousand', 'ten thousand', 'a hundred thousand', 'a million'][min(round(fade), 6) - 2])}倍，因为需要修正的东西越来越少。普通层叠的判断始终是一种平平的颜色，处处一样，它的梯度只会越来越弱。",

    "There's another way to see what the stream does.":
        "还有一种方式来看这股流在做什么。<bookmark mark='a'/>最后一层，等于第一层加上所有块加进来的东西。<bookmark mark='b'/>它的导数，是一串“恒等再加一点”的因子的乘积，<bookmark mark='c'/>把它乘开，就得到2的L次方项：网络里的每一条路径各一项，从跳过所有块的那条，到穿过所有块的那条。残差网络是一大群深浅各异、共享权重的网络，安德烈亚斯·法伊特和同事们发现，大部分梯度走的是短的那些。<bookmark mark='d'/>这个想法有祖先：1997年LSTM的恒定误差传送带，以及鲁佩什·斯里瓦斯塔瓦、克劳斯·格雷夫和于尔根·施密德胡贝的高速公路网络，比ResNet早几个月。ResNet用152层赢下了ImageNet。而GPT-2把每个块的初始权重缩小到块数平方根分之1，这样残差流就不会随深度变大。",

    # ------------------------------------------------------------------ Norm
    'Chapter twelve. Normalization.':
        '第12章。归一化。',

    'The second fix rescales the numbers inside the network as it trains.':
        "第二个修正办法，是在训练时重新缩放网络内部的数。2015年，谢尔盖·约费和克里斯蒂安·塞格迪提出了批归一化。<bookmark mark='a'/>取一批例子，对每个特征，减去它在这一批上的平均值，再除以它的分散程度；然后让网络自己学一个缩放和平移。它让图像网络训练得快了很多，不过他们给出的理由，也就是减少“内部协变量偏移”，后来受到了质疑：2018年，麻省理工学院的一个团队认为，它主要是让损失地形变得更平滑。<bookmark mark='b'/>可是批归一化让每个例子都依赖于同一批里的其他例子，而且测试时还需要从训练中保存下来的平均值。2016年，吉米·巴、杰米·基罗斯和杰弗里·辛顿提出了层归一化：同样的算术，在单个例子的各个特征上做。每一个Transformer用的都是它的某个版本。",

    'Here is what layer normalization does to one vector.':
        "这是层归一化对一个向量做的事。<bookmark mark='a'/>把它的数平移，让平均值变成0，<bookmark mark='b'/>再把它们压缩，让分散程度变成1。<bookmark mark='c'/>2019年，张彪和里科·森里奇问：平移真的需要吗？他们的RMSNorm只除以均方根，也就是这些数的典型大小。从几何上看，它把每一个向量，不管长短，都送到同一个球面上，只保留它的方向。<bookmark mark='d'/>它更便宜，效果一样好，Llama、Qwen和DeepSeek用的都是它。",

    'f"What does normalization do to the gradient?':
        "归一化对梯度做了什么？取不带增益的RMSNorm。<bookmark mark='a'/>用商的求导法则，它的导数是一个常数，乘上单位矩阵减去到h自身方向上的投影。<bookmark mark='b'/>所以拉长h什么也不会改变，梯度也永远不会指向h的方向：这一层只在乎方向。层归一化的导数，还去掉了全1的方向，因为把所有数一起平移，也什么都不会改变。<bookmark mark='c'/>在d等于{d}时用自动求导测一下：RMSNorm的雅可比矩阵有{d - z_rms}个相等的奇异值和{z_rms}个零；层归一化是{d - z_ln}个和{z_ln}个，和推导的完全一样。<bookmark mark='d'/>前面那个常数，是向量大小的倒数：h加倍，梯度减半。变大的权重，得到的更新相应变小。归一化会自己稳住自己，它和权重衰减之间的相互作用，第11部分会讲。",

    'f"Where does the normalization go?':
        "归一化放在哪里？<bookmark mark='a'/>2017年的Transformer，是在把每个块的输出加到残差流上之后再归一化：后置归一化。<bookmark mark='b'/>2019年的GPT-2把它挪到了支路上，放在每个块之前，让残差流本身保持一个干净的累加和：前置归一化。2020年，Ruibin Xiong和同事们说明了这为什么重要：用后置归一化，训练开始时各层的梯度很不均匀，所以需要让学习率先预热。<bookmark mark='c'/>在我们自己的{depth}块模型里，用后置归一化时，最后一块的初始梯度是第一块的{rp:.1f}倍，用前置归一化时是{rq:.1f}倍。<bookmark mark='d'/>{verdict}<bookmark mark='e'/>故事还没完：2024年底的OLMo 2改为对每个块的输出做归一化；2025年何恺明、杨立昆和同事们的一篇论文，干脆用一个缩放过的tanh取代了归一化。",

    "f'Trained at the same learning rate with no warm-up, the pre-norm stack ends at":
        '用同样的学习率、不做预热来训练，前置归一化的层叠最后是每字符{fq:.2f}比特，后置归一化的是{fp:.2f}：后置归一化需要一个更温和的开头。',

    "f'Trained at the same learning rate, the post-norm stack actually ends lower here":
        '用同样的学习率训练，这里后置归一化的层叠反而更低，每字符{fp:.2f}比特，前置的是{fq:.2f}：在这样的深度和规模上，它训练得很好。',

    "f'Trained at the same learning rate, both end close together":
        '用同样的学习率训练，两者最后很接近，每字符{fp:.2f}和{fq:.2f}比特：在这么小的规模上，差别体现在梯度上，还没体现在结果上。',

    # ------------------------------------------------------------------ Block
    'Chapter thirteen. The modern block.':
        '第13章。现代的块。',

    "Inside today's blocks, the bend itself has changed.":
        "在今天的块里，弯折本身也变了。<bookmark mark='a'/>八九十年代的S形sigmoid和tanh，两端都是平的，这让梯度更容易消失。<bookmark mark='b'/>ReLU在正的一侧不会变平，但它对每个负输入的斜率都恰好是0，所以一个不再放电的单元，也就不再学习。<bookmark mark='c'/>2016年，丹·亨德里克斯和凯文·金佩尔从抛硬币推出了一个平滑的版本：以标准高斯分布落在输入x之下的概率，保留x。<bookmark mark='d'/>对硬币取平均，就是x乘Φ of x，也就是GELU，BERT和GPT-2用的就是它。<bookmark mark='e'/>它的表亲，x乘x的sigmoid，叫作SiLU或者Swish，2017年分别来自强化学习和一次自动搜索。两者都是平滑的，都会稍微低于0，对负输入也都会传回一点梯度。",

    'f"The bigger change is the gate.':
        "更大的变化是门控。<bookmark mark='a'/>一个ReLU单元，画成两个输入上的曲面，是一道折痕：一侧平，一侧是斜坡。<bookmark mark='b'/>2016年，扬·多芬和同事们用了门控单元，它把输入的一个投影乘上另一个投影。这里是最简单的一种：一个输入的SiLU，乘上另一个输入。它是一个马鞍面，一个乘积：它能根据另外一件事，打开或关掉一个特征。<bookmark mark='c'/>2020年，诺姆·沙泽尔在Transformer的前馈层里试了几种变体，SwiGLU胜出：一个投影的SiLU，乘上第二个投影，再用第三个矩阵投影回去。他的论文最后，把它的成功和其他一切一样，归功于“神的恩典”。<bookmark mark='d'/>三个矩阵而不是两个，所以为了保持参数数目不变，隐藏层宽度从模型宽度的4倍缩到3分之8倍。<bookmark mark='e'/>看公开的配置：GPT-2普通的MLP是它宽度的4倍；Llama 2的门控MLP是{l2['f']:,}，也就是4096的3分之8，向上取到256的倍数；后来的模型更宽。",

    'f"Now assemble the block.':
        "现在把块组装起来。<bookmark mark='a'/>残差流笔直向上。<bookmark mark='b'/>一条支路取一份经过RMS归一化的副本，做注意力运算，那是第13部分的主题，再把结果加回去。<bookmark mark='c'/>第二条支路再取一份归一化的副本，过一遍门控MLP，再加回去。<bookmark mark='d'/>把它叠起来，这里叠32次，就是Llama 3的主体；稍作改动，也就是Qwen、DeepSeek和其他模型的主体。<bookmark mark='e'/>按Llama 3 8B公开的配置来数：每个块的注意力有{r['attn'] / M:.1f}百万个权重，MLP有{r['mlp'] / M:.1f}百万个，所以块里{100 * mlp_share:.0f}%是门控MLP。32个块再加上嵌入，一共{r['total'] / 1000000000.0:.2f}十亿：正是它名字里的80亿。",

    'f"Does each piece earn its place?':
        "每一个部件都配得上它的位置吗？我们把块一个部件一个部件地搭起来，做成一个在30部小说上训练的字符模型：{int(b['depth'])}个块深，每个版本都在同样的数据上、从同样的随机种子训练{steps:,}步。<bookmark mark='a'/>{first}<bookmark mark='b'/>{second}<bookmark mark='c'/>{norms}<bookmark mark='c3'/>{extra}<bookmark mark='d'/>{third}",

    "f'Normalizing after each block, post-norm, stalls at {po:.2f} with no warm-up":
        '在每个块之后做归一化，也就是后置归一化，不做预热时卡在{po:.2f}；在块之前做归一化，用层归一化达到{pl:.2f}，用RMSNorm达到{pr:.2f}。',

    "f'Normalizing after each block reaches {po:.2f}; before it":
        '在每个块之后做归一化，达到{po:.2f}；在块之前，用层归一化是{pl:.2f}，用RMSNorm是{pr:.2f}。',

    "In a run this short, that's no better than the bare residual stream":
        '训练这么短，这并不比光秃秃的残差流更好：归一化换来的是稳定性，而模型越大，稳定性越重要。',

    "f'With no residual connections, the {int(b['depth'])}-block stack barely learns":
        "没有残差连接，{int(b['depth'])}块的层叠几乎学不动：{p:.2f}比特。",

    "f'Even without residual connections it learns, to {p:.2f} bits.":
        '即使没有残差连接，它也能学，达到{p:.2f}比特。',

    "f'The residual stream alone brings it to {r_:.2f}.":
        '光是残差流，就把它带到了{r_:.2f}。',

    'The residual stream alone, with no normalization, diverges at this learning rate.':
        '只有残差流、没有归一化，在这个学习率下发散了。',

    "f'The full modern block ends best, at {s_:.2f}.":
        '完整的现代块最后最好，{s_:.2f}。',

    "f'The full modern block reaches {s_:.2f}; on this small task the best was":
        '完整的现代块达到{s_:.2f}；在这个小任务上最好的是{best_name}，{final[best]:.2f}，几百分之一的差别，在单次训练的噪声范围之内。',

    # ------------------------------------------------------------------ KAN
    'Chapter fourteen. Kolmogorov':
        '第14章。柯尔莫哥洛夫–阿诺德网络。',

    "There's another way to build any function, and it's older than the perceptron.":
        "还有另一种方法能搭出任何函数，而且它比感知机还早。<bookmark mark='a'/>1900年，大卫·希尔伯特在他著名的问题里，第13个问的是：七次方程的解，能不能只用两个变量的函数写出来。<bookmark mark='b'/>1957年，安德烈·柯尔莫哥洛夫和他19岁的学生弗拉基米尔·阿诺德，给出了强得多的回答。<bookmark mark='c'/>立方体上n个变量的每一个连续函数，都是2n加1个一元函数之和，每个一元函数作用在另外n个一元函数的和上。<bookmark mark='d'/>你唯一需要的多元函数，就是加法。<bookmark mark='e'/>八十年代，研究网络的人注意到了它，并且争论起来：1989年，费德里科·吉罗西和托马索·波焦说它无关紧要，因为里面的函数可能极不规则；1991年，薇拉·库尔科娃回应说，光滑的近似版本是可行的，还带着误差界。",

    'In April 2024 Ziming Liu, Max Tegmark and colleagues':
        "2024年4月，Ziming Liu、马克斯·泰格马克和同事们把这个定理变成了一种架构。<bookmark mark='a'/>普通的网络在每条边上放一个数，在每个节点上放一个固定的弯折。<bookmark mark='b'/>柯尔莫哥洛夫–阿诺德网络在每条边上放一条可学习的曲线，也就是在一组格点上的光滑样条，节点上只做加法。和定理里的版本不同，这些层想叠多深就叠多深。<bookmark mark='c'/>他们报告说，小小的KAN拟合科学公式，比大得多的MLP更准，规模变大时误差下降得更快，而且你能读出学到的曲线，还原出公式。",

    '"Let\'s try it, on the example from their paper':
        "我们来试一试，用他们论文里的例子：e的sin(πx)加y平方次方。这是一个KAN，两个输入，五个隐藏节点，一个输出：十五条曲线，全是学出来的。<bookmark mark='a'/>看着它们训练。<bookmark mark='b'/>{shapes}<bookmark mark='c'/>{verdict}",

    "f'Some of the curves on x take the shape of a sine wave, and some on y of a parabola":
        '有几条关于x的曲线变成了正弦波的样子，有几条关于y的曲线变成了抛物线：最接近的，和正弦、平方的相关系数分别是{cs:.2f}和{cq:.2f}。公式的一部分，画成了图。',

    'f"The curves change shape as it learns, but they don\'t spell out the formula on their own':
        '曲线在学习中改变着形状，但它们自己并不会把公式拼出来：最接近正弦的一条，相关系数是{cs:.2f}，最接近平方的是{cq:.2f}。要从KAN里读出公式，还得剪枝、化简，就像论文里描述的那样。',

    'f"At first it types random symbols:':
        "一开始，它敲出的是随机的符号：它写的“单词”里，只有{100 * wr[0][4]:.0f}%是真正的单词。<bookmark mark='b'/>到第{s1:,}步，有{100 * wr[3][4]:.0f}%是；到最后，是{100 * wr[-1][4]:.0f}%，有了英语句子的节奏，虽然还没有它们的意思。",

    'f"The KAN ends with a test error of {kt:.4f}, {ratio:.0f} times smaller':
        'KAN最后的测试误差是{kt:.4f}，比MLP的{mt:.4f}小{ratio:.0f}倍，而参数数目差不多。',

    "f'The KAN ends at {kt:.4f} and the MLP at {mt:.4f}":
        'KAN最后是{kt:.4f}，MLP是{mt:.4f}：同样大小下，差不多打平。',

    "f'Here the MLP ends lower, {mt:.4f} against the KAN":
        '这里MLP最后更低，{mt:.4f}，KAN是{kt:.4f}。',

    '"Then came the debate.':
        "接着就是争论。<bookmark mark='a'/>{res}这正是那篇论文挑的那类任务。<bookmark mark='b'/>2024年7月，Runpeng Yu、Weihao Yu和Xinchao Wang公平地比较了两者，参数数目和运算量都相同，任务包括图像、文本、音频和表格。MLP总体上赢了。KAN在符号公式上赢了，而且在学新任务时，会忘掉更多旧任务。<bookmark mark='c'/>那年8月，KAN作者的续作转向了科学：寻找公式和守恒量。<bookmark mark='d'/>而在今天的语言模型内部，公开的配置显示，用的仍然是门控MLP。一个1957年的定理，找到的是一个小天地，而不是一场革命。",

    "f'On this function, a smooth formula, KANs reach lower errors per parameter":
        '在这个函数上，一个光滑的公式，KAN每个参数换来的误差更低：最好的KAN是{bk:.5f}，胜过最好的MLP的{bm:.5f}。',

    "f'On this function our best MLP, at {bm:.5f}, actually beats our best KAN":
        '在这个函数上，我们最好的MLP，{bm:.5f}，反而胜过了最好的KAN，{bk:.5f}。',

    # ------------------------------------------------------------------ NeuralLM
    'Chapter fifteen. A neural language model.':
        '第15章。神经语言模型。',

    'f"Now let\'s use a network for the task that runs through this whole series':
        "现在，我们用网络来做贯穿整个系列的那个任务：猜下一个字符。2003年，约书亚·本吉奥、雷让·迪沙尔姆、帕斯卡尔·文森特和克里斯蒂安·若万造出了第一个神经语言模型，针对的是单词。这里是它的设计，换成字符。取最后{n}个字符。<bookmark mark='a'/>每个字符都变成一个由{e}个数组成的向量，从一张表里查出来，而这张表本身也是学出来的。<bookmark mark='b'/>这些向量穿过一个由tanh单元组成的隐藏层。<bookmark mark='c'/>输出的是每一个可能的下一个字符的分数，再由第1部分的softmax变成概率。其中的每一个数，都靠反向传播一起学出来。",

    '"Train it on Part 1\'s thirty novels':
        "用梯度下降，在第1部分的30部小说上训练它，损失就用第1部分的交叉熵。曲线下面，是它在训练的每个时刻写出来的东西，总是用同一段开头、同一串随机数。<bookmark mark='a'/>{early}<bookmark mark='c'/>{end}",

    "f\"By the end it reaches {nn:.2f} bits per character, past":
        "到最后，它达到每字符{nn:.2f}比特，超过了Kneser–Ney的{kn:.2f}。",

    "f\"By the end it reaches {nn:.2f} bits per character: better than Part 1's best counting model":
        "到最后，它达到每字符{nn:.2f}比特：比第1部分最好的计数模型，{p1:.2f}，要好，但还不及Kneser–Ney的{kn:.2f}。只用这么点算力，最好的计数方法仍是个难缠的对手。",

    "f\"By the end it reaches {nn:.2f} bits per character: within {nn - p1:.2f}":
        "到最后，它达到每字符{nn:.2f}比特：和第1部分最好的计数模型，{p1:.2f}，只差{nn - p1:.2f}，离Kneser–Ney的{kn:.2f}还有距离。只用这么点算力，最好的计数方法仍是个难缠的对手。",

    '"Bengio\'s team found that their best results came from combining':
        "本吉奥的团队发现，他们最好的结果，来自把网络和一个计数模型结合起来：对两者的预测取平均。<bookmark mark='a'/>这个权重是在留出的文本上选定的，从不在测试段落上选。<bookmark mark='b'/>{said}",

    "f'Together, they reach {mix:.2f} bits: better than either alone":
        '两者合起来，达到{mix:.2f}比特：比任何一个单独用都好，因为它们犯的错误不一样。在测试段落上，有{100 * wins:.0f}%的字符，是网络比计数模型更有把握。',

    "f'Together, they reach {mix:.2f} bits, no better than the best":
        '两者合起来，达到{mix:.2f}比特，并不比两者中较好的那个更好。',

    'And the vectors the network scores each next character with':
        "还有网络给每个下一个字符打分时用的那些向量，没有人设计过它们，它们却自己组织了起来。沿着第7部分讲过的两个主方向来看，<bookmark mark='a'/>表现相似的字符，聚在一起：小写字母和小写字母在一起，大写字母和大写字母在一起，数字和数字在一起，标点占一个角落。这又是第3部分的词向量，只不过这一次，是作为预测的副产品学出来的。",

    "'On the scoreboard, two new rows: the first network, and the network with counting, ' + top_row":
        '记分牌上，添了两行新的：第一个网络，以及加上计数的网络，{top_row}。{gap}',

    "f'{behind:.2f} bits behind the best row above them'":
        '比它们上面最好的那一行还差{behind:.2f}比特',

    'the best machine on the board before GPT-2':
        '在GPT-2之前，它是记分牌上最好的机器',

    'the best machine on the board so far':
        '它是目前记分牌上最好的机器',

    "f\"<bookmark mark='a'/> But it's still far behind GPT-2.":
        "<bookmark mark='a'/>但它离GPT-2还差得很远。它只看得到{d['n_ctx']}个字符，而且所有的事，都得由一个隐藏层来做。本系列剩下的部分，讲的就是怎样缩小这个差距。",

    "f\"<bookmark mark='a'/> It sees only {d['n_ctx']} characters":
        "<bookmark mark='a'/>它只看得到{d['n_ctx']}个字符，而且所有的事，都得由一个隐藏层来做。第1部分的大模型还没有填进这张记分牌，它们会显示还有多远的路要走。",

    "Here's what it writes, from Part 5's prompt and three others":
        "这是它写出来的东西，接着第5部分的那段前文，还有另外三段前文往下写：<bookmark mark='a'/>看起来像英语，也像一个个单词，但还说不通。",

    # ------------------------------------------------------------------ Outro
    '"Let\'s take stock.':
        "我们来盘点一下。一个单元，就是一个加权和加一个阈值；只要有一条直线能分开数据，感知机就一定能从错误中把它学出来。一层做不了异或；两层可以，而反向传播往回扫一遍就能训练它们。一个隐藏层能逼近任何曲线，而对足够光滑的函数，所需单元的数目不会随维数爆炸。深度能把空间折成指数级多的小块。权重必须从混沌的边缘出发，对ReLU是n分之2，否则信号就会消失或爆炸；残差流和归一化，让梯度能流过很多层。{last}",

    'And a small network, trained on our books, beat every counting model':
        '而一个小小的网络，在我们的书上训练之后，打败了记分牌上所有的计数模型。',

    "f'And a small network, trained on our books, came within {nn_b - kn_b:.2f} bits":
        '而一个小小的网络，在我们的书上训练之后，和最好的计数模型只差{nn_b - kn_b:.2f}比特，和它混合之后，打败了记分牌上所有的计数模型。',

    "f'And a small network, trained on our books, ended {nn_b - kn_b:.2f} bits":
        '而一个小小的网络，在我们的书上训练之后，比最好的计数模型差了{nn_b - kn_b:.2f}比特。',

    'All of this comes back.':
        '这些都会再回来。在空间和时间上共享权重，就得到第10部分的卷积网络和循环网络。网络变大时，权重和学习率的尺度该怎么定，是第11和第12部分的主题。残差流是第13部分Transformer的主干，也是第30部分我们观察模型内部时读取的东西。归一化会在注意力内部再次出现。门控MLP，复制很多份，就成了第16部分的专家。而学到的嵌入，这里是字符的，后面会变成词元、图像和声音的嵌入。',

    'Here are six problems to try':
        '这里有六道题可以试一试，从感知机的学习率，到RMSNorm的雅可比矩阵。在这里暂停，把它们做一做；完整的解答在这一部分的笔记里。',

    'Next time: seeing and remembering.':
        '下一次：看与记。一种网络，让一个小小的滤波器在图像上滑动，处处共享权重；2012年，其中一个以巨大的优势赢下了ImageNet；带回路、能记住东西的网络，LSTM，以及第一个注意力机制；还有一个字符LSTM，登上我们的记分牌。',

    "Simon Prince's Understanding Deep Learning is the clearest modern textbook":
        '西蒙·普林斯的《理解深度学习》是最清楚的现代教材，而且可以免费阅读。感谢收看，我们第10部分再见。',
}

PHRASES = {
    # the depth chapter's verdicts
    'barely changes, and even falls': '几乎不变，甚至还减少了',
    'grows only slowly': '只是缓慢增长',
    'training multiplied them': '训练让它们成倍增加',
    # factors spoken in words
    '30 million': '3000万',
    '20 million': '2000万',
    '10 million': '1000万',
    '40 million': '4000万',
    'a billion': '10亿',
    'ten billion': '100亿',
    'a hundred billion': '1000亿',
    'a trillion': '1万亿',
    'ten trillion': '10万亿',
    'a hundred trillion': '100万亿',
    'a quadrillion': '1000万亿',
    'ten': '10',
    'a hundred': '100',
    'a thousand': '1000',
    'ten thousand': '1万',
    'a hundred thousand': '10万',
    'a million': '100万',
    # the block chapter's spoken variant names
    'the plain stack': '普通的层叠',
    'the residual stack without normalization': '没有归一化的残差层叠',
    'post-LayerNorm': '后置层归一化',
    'pre-LayerNorm': '前置层归一化',
    'pre-RMSNorm without the gate': '不带门控的前置RMSNorm',
    'the full block': '完整的块',
}
