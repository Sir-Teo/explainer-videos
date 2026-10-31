"""Chinese narration for ai3: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第3部分：有意义的向量'

CHAPTERS = {
    'Hook': '词住在哪里',
    'Vectors': '1. 向量与内积',
    'Einsum': '2. 张量与einsum',
    'Matrices': '3. 矩阵让空间动起来',
    'Projection': '4. 投影与最小二乘',
    'Eigen': '5. 方向不变的向量',
    'Power': '6. 幂迭代，现场运行',
    'SVD': '7. 每个矩阵：转、拉、再转',
    'LowRank': '8. 最好的低秩副本',
    'Norms': '9. 一个矩阵有多大？',
    'Spectra': '10. 随机矩阵与训练过的权重',
    'GaLore': '11. 梯度是低秩的',
    'Words': '12. 从计数得到词向量',
    'SGNS': '13. word2vec其实是在计数',
    'HighDim': '14. 生活在768维',
    'JL': '15. 约翰逊–林登斯特劳斯引理，证明',
    'Geometry': '16. GPT-2歪斜的空间',
    'Netflix': '17. 现实中的低秩',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    'In part one, a model learned to guess the next letter by counting':
        "在第1部分，一个模型靠计数学会了猜下一个字母，然后撞上了一堵墙：每个上下文都是一座孤岛。<bookmark mark='a'/>把the dog barked读上100遍，也没让它学到关于the hound barked的任何东西。",

    'f"Every modern model fixes this the same way.':
        "每一个现代模型，都用同一种办法解决这个问题：给每个词一个位置，<bookmark mark='a'/>也就是空间里的一个点，这些点的选法，让用法相近的词最后靠在一起。<bookmark mark='b'/>这是{len(words)}个词，放在GPT-2给它们安排的位置上：动物在一个区域，颜色在另一个区域，然后是数字、地点、家庭、身体，还有动词。",

    'The picture is a shadow.':
        "这幅图只是一个影子。<bookmark mark='a'/>GPT-2实际上给它的50257个词元，每个都配了一串768个数，我们把它们压扁成3个，留下的是这些词散得最开的3个方向。<bookmark mark='b'/>凑近看，dog和其他动物待在一起。",

    'Here is dog, all 768 numbers.':
        "这是dog，全部768个数。<bookmark mark='a'/>这是puppy。<bookmark mark='b'/>这是tobacco。<bookmark mark='c'/>其中有两个是一路的，到第1章，我们会学会衡量它们有多接近。",

    'The mathematics is older than the machines.':
        "这些数学比机器老得多。1844年，赫尔曼·格拉斯曼描述了可以相加、可以伸缩的量，而且是任意多维的。<bookmark mark='a'/>1858年，阿瑟·凯莱写下了矩阵的代数。<bookmark mark='b'/>贝尔特拉米和若尔当发现了奇异值分解，<bookmark mark='c'/>希尔伯特给特征值起了名字。<bookmark mark='d'/>埃卡特和杨证明了怎样只留下最要紧的部分。<bookmark mark='e'/>然后是意义：约翰·弗斯说，要了解一个词，就看它和什么词为伴。<bookmark mark='f'/>约翰逊和林登斯特劳斯把维数压了下去。<bookmark mark='g'/>潜在语义分析把词放进了一个空间，<bookmark mark='h'/>Netflix悬赏一百万美元，征求填补一个大半是空的矩阵的办法。<bookmark mark='i'/>接着是word2vec，<bookmark mark='j'/>还有LoRA、GaLore和Muon：同样的线性代数，进入了今天的训练。",

    'This is Part 3 of AI, Built.':
        "这是《人工智能，从零搭建》的第3部分。<bookmark mark='a'/>这一部分讲：向量、点积和einsum；投影、特征向量和奇异值分解，每一个都会推导；范数、随机矩阵，以及训练往权重里写进了什么；词向量；高维空间的几何；还有实际中的低秩。每个数都是算出来的，小到一台笔记本电脑就能跑。",

    # ---------------------------------------------------------------- Vectors
    'Chapter one.': '第1章。向量，以及两个向量有多像。',

    'A vector is an arrow from the origin':
        "向量是从原点出发的一支箭头，<bookmark mark='a'/>也同样可以看成一串数：沿每条轴走多远。<bookmark mark='b'/>平面上是两个数，空间里是三个，GPT-2里一个词是768个。<bookmark mark='c'/>格拉斯曼在1844年就看出，代数根本不在乎有多少个数。可是四十年里几乎没人读他的书。",

    'Two moves make all of linear algebra.':
        "整个线性代数，只用两个动作。<bookmark mark='a'/>把两个向量相加：先沿一个走，再沿另一个走。<bookmark mark='b'/>再就是缩放：拉长、缩短，或者翻转。把两个动作混起来，a乘u加b乘v，<bookmark mark='c'/>箭头尖扫过整个平面：u和v就是一组基，每个向量在这组基下，都有唯一的一对坐标。",

    'How alike are two vectors? <bookmark mark=\'a\'/> Multiply them':
        "两个向量有多像？<bookmark mark='a'/>把它们逐个坐标相乘，再加起来：这就是点积，也叫内积。它是对称的，对每个位置都是线性的，一个向量和自己的点积，就是它长度的平方。<bookmark mark='b'/>画一个三角形，三条边是a、b和a减b。第三条边的平方，是一个点积。<bookmark mark='c'/>把它展开。<bookmark mark='d'/>欧几里得的余弦定理，从另一条路算出同一条边。<bookmark mark='e'/>两相比较：点积等于两个长度，乘以它们夹角的余弦。",

    'Is that cosine always between minus one and one':
        "这个余弦总在负1和1之间吗？哪怕在768维里？这就是柯西–施瓦茨不等式。<bookmark mark='a'/>对任何数t，a减t乘b的长度的平方，都不可能是负的。<bookmark mark='b'/>如果b是零向量，不等式显然成立。否则，把它展开：一条关于t的抛物线。<bookmark mark='c'/>一条从不跌到0以下的抛物线，最多只有一个根，所以它的判别式不可能是正的。<bookmark mark='d'/>整理一下：点积的绝对值至多是两个长度的乘积。<bookmark mark='e'/>转动b，看着：当b和a在同一直线上，无论同向还是反向，抛物线都会碰到0。所以两个词之间的夹角，是有意义的。",

    'f"Divide by the two lengths and you get the cosine similarity':
        "除以两个长度，就得到余弦相似度，它在负1到1之间。<bookmark mark='a'/>拿GPT-2的词来说：dog和puppy，{c[1]:.2f}。dog和cat，{c[3]:.2f}。dog和tobacco，{c[2]:.2f}。<bookmark mark='b'/>在768维里画不出夹角，但可以算出来：把两串数逐个相乘，再加起来。",

    'f"Here is why this matters.':
        "这为什么重要？在第1部分，网络最后给每个可能的下一个词元打一个分，softmax再把分数变成概率。<bookmark mark='a'/>在GPT-2里，每个分数都是一个点积：模型最后的状态，和每个词元的向量相点乘，用的正是词元一开始的那些向量。<bookmark mark='b'/>在“埃菲尔铁塔位于哪座城市”这句话之后，点积最大的是{toks[0]}、{toks[1]}、{toks[2]}。<bookmark mark='c'/>softmax给{toks[0]}的概率是{100 * prob[0]:.1f}%。",

    # ---------------------------------------------------------------- Einsum
    'Chapter two.': '第2章。张量，以及注意力所用的记法。',

    'f"A number, a vector, a matrix: zero, one and two axes.':
        "一个数、一个向量、一个矩阵：零根、一根、两根轴。<bookmark mark='a'/>一批文本是一串句子，每句是一串词元，每个词元是一串数：三根轴，机器学习管它叫张量。<bookmark mark='b'/>注意力把这些数分给{e['heads']}个头：四根轴。这样的数组相乘，需要一种能给轴起名字的记法。",

    'Multiplying two matrices: entry i k':
        "两个矩阵相乘：结果的第i行第k列，是A的第i行和B的第k列逐项相乘，再对j求和。<bookmark mark='a'/>1916年，爱因斯坦在写广义相对论时，写烦了求和号，干脆把它省掉：一个指标出现两次，就表示对它求和。<bookmark mark='b'/>程序把这个想法做成了einsum，每根轴用一个字母表示。<bookmark mark='c'/>出现在输出里的字母保留；只出现在输入里的字母被求和消掉。计算量也一目了然：所有字母的每一种组合，做一次乘加，这里是i乘j乘k。",

    'One function does all of these.':
        "一个函数，就能做这些事。<bookmark mark='a'/>点积：相乘，全部加起来。<bookmark mark='b'/>外积：什么都不求和，得到一个秩为1的矩阵。<bookmark mark='c'/>矩阵乘向量。<bookmark mark='d'/>转置，只是换个顺序。<bookmark mark='e'/>迹。<bookmark mark='f'/>还有一整批矩阵乘法，字母b一路带着走。",

    'f"Here is attention, Part 13\'s subject, in this notation.':
        "用这种记法写注意力，也就是第13部分的主题。<bookmark mark='a'/>每个词元的向量，投影成查询、键和值，再分给各个头。<bookmark mark='b'/>每个查询和每个键做点积：e被求和消掉。<bookmark mark='c'/>softmax把分数变成权重，权重再对值求平均。<bookmark mark='d'/>最后把各个头合并回去。<bookmark mark='e'/>从字母里直接读出计算量。对{n:,}个词元，打分每层大约要{ms / 1000000.0:,.0f}百万次乘加，投影要{mp / 1000000.0:,.0f}百万次。打分随长度的平方增长：这就是长上下文昂贵的原因。",

    'f"The letters also show that order matters.':
        "这些字母还说明，顺序很重要。<bookmark mark='a'/>A是{a:,}乘{b}，B是{b}乘{c:,}，C是{c:,}乘{d}。<bookmark mark='b'/>先乘A和B，途中就造出一个{a:,}乘{c:,}的矩阵：{L:,}次乘加。<bookmark mark='c'/>先乘B和C：{R:,}次。结果一样，便宜了{fac:.0f}倍。<bookmark mark='d'/>einsum可以自己找出便宜的顺序；这里，它先乘{first}。",

    # ---------------------------------------------------------------- Matrices
    'Chapter three.': '第3章。矩阵让空间动起来。',

    'A matrix moves every vector at once.':
        "一个矩阵，同时移动所有的向量。<bookmark mark='a'/>它让原点留在原处，让网格线保持笔直、平行、间距均匀：这就是线性映射。<bookmark mark='b'/>看整个平面怎样移动。",

    'Where does each vector go?':
        "每个向量去了哪里？<bookmark mark='a'/>只要看两支箭头就够了：两支基向量落在哪里。这两个落点，就是矩阵的两列。<bookmark mark='b'/>坐标为1和2的向量，落在1乘第一列，加2乘第二列。这就是矩阵乘向量的意思。",

    'One map after another is again a map':
        "一个映射接着另一个映射，仍然是一个映射，它的矩阵就是两个矩阵的乘积。<bookmark mark='a'/>但顺序很重要：先转再剪切，不同于先剪切再转。<bookmark mark='b'/>1858年，阿瑟·凯莱把矩阵本身当成研究对象，规则正是这样；他的朋友詹姆斯·约瑟夫·西尔维斯特，八年前就给它们起了名字。",

    'One number says how much a map stretches area':
        "有一个数，说明映射把面积拉大了多少：行列式。<bookmark mark='a'/>单位正方形变成一个平行四边形，它的面积是行列式的绝对值，符号记录朝向。<bookmark mark='b'/>行列式到了0，整个平面被压成一条线，信息就永远丢了。<bookmark mark='c'/>小于0，平面被翻了过来，就像把一页纸扣过去。",

    'That squashing has a name':
        "这种压扁有个名字，而且这一部分后面都用得着。<bookmark mark='a'/>这个矩阵把整个平面送到一条线上：它的两列指向同一个方向。<bookmark mark='b'/>所有东西落到的那条线，叫列空间，它的维数就是秩，这里是1。<bookmark mark='c'/>有一整条线上的向量，都落到了0：这叫零空间。<bookmark mark='d'/>维数总是加得起来：秩加上零空间的维数，等于列数。一个低秩的矩阵，就是一张大表，却只含有很少几个独立的方向。",

    # ---------------------------------------------------------------- Projection
    'Chapter four.': '第4章。投影，以及最近的点。',

    'The dot product measured a shadow':
        "点积量的是影子；这里，把影子算准。<bookmark mark='a'/>过a的直线上，哪一点离b最近？<bookmark mark='b'/>它是a的某个倍数，<bookmark mark='c'/>是让误差，也就是b减去这一点，垂直于直线的那一个：根据勾股定理，其他点都更远。<bookmark mark='d'/>解出这个倍数。<bookmark mark='e'/>投影就是一个矩阵乘b：a乘a转置，除以a点a。一个秩为1、专找影子的矩阵。",

    'Now project onto a subspace':
        "现在投影到一个子空间上：也就是矩阵A的列能组合出来的一切。<bookmark mark='a'/>最近的点是A乘某个x帽，误差同时垂直于每一列。<bookmark mark='b'/>乘开来：正规方程。<bookmark mark='c'/>如果各列线性无关，A转置A就可逆。<bookmark mark='d'/>投影矩阵：A，乘A转置A的逆，再乘A转置。<bookmark mark='e'/>投影两次，不会再有变化；而且P是对称的。<bookmark mark='f'/>勒让德在1805年以最小二乘法的名字发表了它，高斯在1809年也发表了，他早就用它找到了失踪的小行星谷神星。",

    'This is the most used calculation in statistics.':
        "这是统计学里用得最多的计算。<bookmark mark='a'/>十四个点，一条直线。A的两列是一列1和x的值；最好的直线，就是把y的值投影到这两列张成的平面上。<bookmark mark='b'/>误差垂直于两列：误差加起来是0，误差乘x加起来也是0。<bookmark mark='c'/>回归、从网络里读出一个概念的线性探针、用平方误差训练的最后一层：全都是这个投影。",

    'Projections are easiest with an orthonormal basis':
        "用标准正交基做投影最省事，也就是一组互相垂直、长度为1的箭头：这时投影就是Q乘Q转置。<bookmark mark='a'/>格拉姆和施密特的方法，能从任何一组基造出这样的基。先把第一个向量缩放到长度1。<bookmark mark='b'/>从第二个向量里，减去它在第一个上的影子；剩下的就垂直了。<bookmark mark='c'/>再缩放，如此重复。<bookmark mark='d'/>把系数留下来，就把A写成了Q乘一个三角矩阵R：这就是QR分解。",

    'f"On a computer every step rounds':
        "在计算机上，每一步都要舍入，舍入误差会越积越多。我们在希尔伯特矩阵上做了测试，它的各列几乎线性相关。<bookmark mark='a'/>经典的方法失去正交性的程度，和条件数的平方成正比：条件数为10的{ex(mid['kappa'])}次方时，它的Q偏差大约是10的负{-ex(mid['cgs'])}次方。{dead}<bookmark mark='b'/>改进的方法，每次从更新过的向量上取影子，损失只和条件数成正比。<bookmark mark='c'/>阿尔斯通·豪斯霍尔德1958年的反射法，一直保持垂直，偏差大约是10的负{-ex(last['householder'])}次方，也就是机器精度。<bookmark mark='d'/>正规方程也有经典方法的毛病：一构造A转置A，条件数就平方了。在最难的情形，QR的答案偏差是10的负{-ex(last['err_qr'])}次方，{worst}所以各种程序库都用QR来解最小二乘。",

    ' By the end, its vectors are not perpendicular at all.':
        "到最后，它的向量已经完全不垂直了。",

    ' against an error bigger than the answer itself':
        "而正规方程的误差，比答案本身还大。",

    "f' against ten to the minus {-ex(last['err_normal'])}":
        "而正规方程是10的负{-ex(last['err_normal'])}次方。",

    # ---------------------------------------------------------------- Eigen
    'Chapter five.': '第5章。特征向量，以及谱定理。',

    'Most vectors are knocked off their line by a matrix.':
        "大多数向量，都会被矩阵撞离自己所在的直线。<bookmark mark='a'/>有些不会：它们留在自己的直线上，只被拉长、缩短，或者反向。<bookmark mark='b'/>它们就是特征向量，拉伸的倍数就是特征值。这时A减λI必须把一个方向压成0，所以它的行列式为0：这是一个关于λ的多项式方程。",

    'Symmetric matrices, equal to their mirror image':
        "对称矩阵，也就是沿对角线翻过来不变的矩阵，性质最好。<bookmark mark='a'/>它们的特征值是实数，而且总能选出一组标准正交的特征向量基。<bookmark mark='b'/>所以这个映射就是：把特征向量转到坐标轴上，沿每根轴按特征值拉伸，再转回去。<bookmark mark='c'/>A等于Q乘Λ乘Q转置；对Q这样的旋转，转置就是同一个旋转，倒过来。这就是谱定理。",

    'Why does it always work? The proof has three steps.':
        "为什么总是成立？证明分三步。<bookmark mark='a'/>第一，特征值是实数：把A夹在一个特征向量和它的复共轭之间。因为A是实的、对称的，中间这个数等于它自己的共轭，所以λ等于λ的共轭。<bookmark mark='b'/>第二，特征值不同的特征向量互相垂直：把A从点积的一边挪到另一边，两个特征值必须相等，除非点积为0。<bookmark mark='c'/>第三，A把垂直于一个特征向量的空间映到它自己，于是在里面重复同样的步骤：用归纳法，得到一整组。柯西在1829年证明了第一部分；希尔伯特把它推广到了无穷维。",

    'One number connects eigenvalues to what follows':
        "有一个数，把特征值和后面的内容连起来：瑞利商，x转置A x，除以x转置x。<bookmark mark='a'/>在特征向量基下，它是各个特征值的加权平均。<bookmark mark='b'/>所以当x转动时，它总在最小和最大的特征值之间，只有沿着特征向量才取到它们。<bookmark mark='c'/>最大特征值的特征向量回答了一个问题：A最偏爱哪个方向？它还会以主成分、幂迭代和奇异值分解的样子回来。",

    'Covariance matrices describe how data spreads':
        "协方差矩阵描述数据怎样散开：<bookmark mark='c'/>对角线上，是每个坐标变化多少；对角线外，是两个坐标一起变化多少。沿一个单位方向的散布，正是协方差的瑞利商，所以散得最开的方向，就是最大特征值的特征向量。<bookmark mark='a'/>这就是主成分，皮尔逊在1901年、霍特林在1933年提出。<bookmark mark='b'/>只留下最前面几个，我们就是这样把GPT-2的词画在三维里的。",

    # ---------------------------------------------------------------- Power
    'Chapter six.': '第6章。幂迭代：计算机怎样找到特征向量。',

    'Eigenvalues are roots of a polynomial':
        "特征值是一个多项式的根，768乘768的矩阵，多项式就是768次的。阿贝尔证明，四次以上不存在通用的根式求根公式，所以计算机使用数值方法。<bookmark mark='a'/>对这里的对称矩阵，起点沿主特征向量的分量必须非零；乘A，缩放到长度1，重复。<bookmark mark='b'/>在这个例子里，每乘一次，都偏向A拉伸得最多的方向，箭头就转到了主特征向量上。",

    'Why it works takes four lines.':
        "为什么有效，四行就够了。<bookmark mark='a'/>取一个对称矩阵，起点沿主特征向量的分量必须非零。把起点写在标准正交的特征向量基下。<bookmark mark='b'/>乘k次，每一部分都被它的特征值的k次方拉伸。<bookmark mark='c'/>把最大的提出来：其他每一部分，都乘上一个小于1的比值的k次方。<bookmark mark='d'/>所以夹角按λ2比λ1的k次方缩小：在对数坐标上是一条直线。<bookmark mark='e'/>特征值的估计还要快一倍，因为瑞利商在驻点处，方向上的小误差几乎不改变它。",

    'f"Now real matrices.':
        "现在看真实的矩阵。<bookmark mark='a'/>GPT-2那50257个词元向量的协方差，768乘768：它最大的两个特征值之比是{dg['ratio']:.3f}，误差每一步缩小到{dg['rate_measured']:.3f}倍，一直降到机器的舍入误差。随机的起点几乎垂直于答案，正弦是{s0:.4f}；第14章会解释原因。<bookmark mark='b'/>第1部分的字母表：比值是{dl['ratio']:.3f}，实测{dl['rate_measured']:.3f}。<bookmark mark='c'/>虚线是预测：{verdict}。",

    'both measured rates are within 0.01 of their predicted ratios': '两个实测速率与各自预测比值的差都小于0.01',

    'f"the largest absolute gap from the predicted ratios is {rate_gap:.3f}"':
        '与预测比值之间，最大的绝对差是{rate_gap:.3f}',

    'The method is from 1929':
        "这个方法出自1929年，作者是理查德·冯·米泽斯和希尔达·波拉切克-盖林格。<bookmark mark='a'/>1998年，它给整个网络排了名：PageRank就是链接矩阵最大特征值的特征向量。<bookmark mark='b'/>2018年，谱归一化每个训练步只做一步幂迭代，防止各层拉伸过度。<bookmark mark='c'/>今天程序库里的例程，是它的改进版：克雷洛夫方法，源于科尼利厄斯·兰乔斯1950年的工作。",

    # ---------------------------------------------------------------- SVD
    'Chapter seven.': '第7章。奇异值分解。',

    'Not every matrix is symmetric.':
        "不是每个矩阵都对称。很多甚至不是方阵。<bookmark mark='a'/>但每一个矩阵，无一例外，都能分成三个因子：一次正交坐标变换，沿坐标轴拉伸或投影，再一次正交变换。这些坐标变换可以是旋转，也可以是反射。我们的例子用的是两次旋转。<bookmark mark='b'/>这就是奇异值分解：A等于U乘Σ乘V转置。",

    'Where do the turns and stretches come from?':
        "这些旋转和拉伸是从哪里来的？<bookmark mark='a'/>A转置A是对称的，而且从不为负：x转置A转置A x是一个长度的平方。<bookmark mark='b'/>所以谱定理给了它一组互相垂直的特征向量v，特征值是σ的平方。<bookmark mark='c'/>对非零σ，把每个v送进A，再除以σ。若有零奇异值，就把两边补成完整的标准正交基。<bookmark mark='d'/>这些u也互相垂直，长度为1。<bookmark mark='e'/>所以A把互相垂直的v送到互相垂直的u，按σ拉伸：这就是分解。<bookmark mark='f'/>贝尔特拉米和若尔当在1873和1874年发现了它；吉恩·戈卢布和威廉·卡汉1965年的算法，计算机至今还在用。",

    'The stretches are the singular values.':
        "这些拉伸倍数，就是奇异值。<bookmark mark='a'/>单位圆总是变成一个椭圆，奇异值就是它的半轴。<bookmark mark='b'/>让一个单位向量转一整圈，看它的像有多长。最长的时候就是σ1：矩阵能把任何向量拉伸的最大倍数。这叫谱范数。",

    # ---------------------------------------------------------------- LowRank
    'Chapter eight.': '第8章。一个矩阵最好的低秩副本。',

    'Written out, the decomposition makes any matrix':
        "把分解写开，任何矩阵都是一些简单的块之和，<bookmark mark='a'/>每一块是一列乘一行，再乘一个奇异值。块的个数就是秩；低秩的表，就是几块就能拼出来的表。<bookmark mark='b'/>留下最大的k块，就得到最接近的秩为k的矩阵。没有别的更接近：这就是埃卡特–杨定理，1936年。",

    "Why can't anything beat them?":
        "为什么没有更好的？<bookmark mark='a'/>外尔1912年的不等式：A的奇异值往后挪k位，至多等于A减B的奇异值，加上B的第k加1个奇异值。<bookmark mark='b'/>如果B的秩是k，最后那一项就是0。<bookmark mark='c'/>一个矩阵大小的平方，等于它奇异值平方的和，第9章会说明，所以B的误差，至少是A的奇异值尾巴。<bookmark mark='d'/>留下前k块，正好达到这条尾巴。",

    'f"A picture is a matrix too':
        "一张图片也是一个矩阵：{h}行，每行{w}个灰度值。<bookmark mark='a'/>它最好的秩1副本是一列乘一行：条纹、天空和地平线。<bookmark mark='b'/>秩2、4、8：山出现了。秩{ranks[k8]}用{100 * store[k8] / pix:.0f}%的数，留住了{100 * energy[k8]:.1f}%的平方大小。<bookmark mark='c'/>然后是树；到了秩{ranks[-1]}，就很难和原图区分了。<bookmark mark='d'/>每一处的误差，都正好是略去的奇异值。",

    'f"Part 1\'s table of letter pairs':
        "第1部分的字母对表，26乘26，表里是概率的平方根。<bookmark mark='a'/>第一块是一个可分离的近似：逐项平方，再归一化，就得到两个字母互相独立的分布。<bookmark mark='b'/>加上第二块、第三块、第五块、第十块，<bookmark mark='c'/>误差正好按略去的奇异值减小：一块之后是全体的{err[0]:.2f}，两块之后是{err[1]:.2f}。",

    'f"The pieces mean something.':
        "这些块是有意义的。<bookmark mark='a'/>看这张表偏离独立的程度：每个计数，对比字母互不相干时应有的计数。把字母沿它最强的方向排开。<bookmark mark='b'/>一端是：{', '.join(left5[:-1])}，{left5[-1]}。{found_say}",

    'No one told the computer what a vowel is.':
        "没有人告诉计算机什么是元音。只靠计数，它发现了元音和辅音轮流出现。",

    'Most of the vowels gather at one end':
        "只靠计数，大部分元音聚到了一端。",

    'Low rank is everywhere in machine learning.':
        "低秩在机器学习里无处不在。<bookmark mark='a'/>1990年，潜在语义分析用截断的奇异值分解，按意义检索文档。<bookmark mark='b'/>2021年，LoRA只学习每个权重的一个低秩变化，就微调了巨大的模型：对GPT-3，要训练的数少了一万倍。<bookmark mark='c'/>2024年，DeepSeek让注意力的键和值穿过一个低秩瓶颈。第15和第27部分会搭建它们。",

    # ---------------------------------------------------------------- Norms
    'Chapter nine.': '第9章。一个矩阵有多大？',

    'A matrix has two natural sizes.':
        "一个矩阵有两种自然的大小。<bookmark mark='a'/>弗罗贝尼乌斯范数把它当成一串数：各数平方和的平方根。谱范数把它当成一个映射：它把任何向量拉伸的最大倍数，也就是最大奇异值。<bookmark mark='b'/>弗罗贝尼乌斯范数的平方，是A转置A的迹，<bookmark mark='c'/>而迹是特征值之和，也就是奇异值的平方和：这正是第8章缺的那一步。<bookmark mark='d'/>所以谱范数至多是弗罗贝尼乌斯范数，后者又至多是前者的根号r倍。<bookmark mark='e'/>两者之比的平方叫稳定秩，数的是有多少个方向承载着矩阵的大小。",

    'f"Here are the stable ranks of GPT-2\'s 48 block matrices':
        "这是GPT-2各层48个矩阵的稳定秩；每个最多可以到{full}。<bookmark mark='a'/>和MLP同样形状的随机矩阵是{rnd['stable']:.0f}；理论预测{rnd['stable_pred']:.0f}。<bookmark mark='b'/>训练过的矩阵在{lo:.0f}到{hi:.0f}之间：{verdict}。稳定秩越小，说明矩阵的大小越集中在少数几个方向上。",

    'every one is below half of this MLP-shaped random reference': '每一个都低于这个MLP形状随机参考值的一半',

    'every one is below this MLP-shaped random reference': '每一个都低于这个MLP形状的随机参考值',

    'at least one reaches or exceeds this MLP-shaped random reference': '至少有一个达到或超过这个MLP形状的随机参考值',

    'f"Norms multiply through a network.':
        "范数在网络里一层层相乘。<bookmark mark='a'/>先按A拉伸再按B拉伸，至多拉伸两者的乘积。让一个向量穿过{L}层随机矩阵。<bookmark mark='b'/>每层拉伸{gains[2]:g}倍，它的长度增长到{big:,.0f}倍。<bookmark mark='c'/>每层{gains[0]:g}倍，就缩到{small:.5f}。只有接近1，信号才能活下来：这是第9部分的主题。",

    'f"The largest stretch over the smallest is the condition number':
        "最大拉伸除以最小拉伸，就是条件数：一个矩阵能把误差放大多少。<bookmark mark='a'/>解A x等于b，b里有一个小误差。<bookmark mark='b'/>x的误差，至多是这个误差除以最小奇异值，<bookmark mark='c'/>而b至多是最大奇异值乘x。<bookmark mark='d'/>相除：相对误差至多放大κ倍。<bookmark mark='e'/>计算机的舍入，就扮演b里的误差。条件数为一百万时，64位运算大约丢掉答案的10的负{-ex(s6['e64'])}次方；32位丢掉10的负{-ex(s6['e32'])}次方。{lost}GPT-2条件最差的矩阵，大约达到10的{ex(kmax)}次方。",

    "f' From a condition number of ten to the {ex(dead32)}":
        "条件数到了10的{ex(dead32)}次方，32位的答案就根本不算答案了。",

    'f"The spectral norm has become an optimizer.':
        "谱范数变成了一个优化器。<bookmark mark='a'/>沿着梯度G，谱大小为1的哪一步让损失变化最大？用奇异值分解写出G。<bookmark mark='b'/>每个对角元至多是1，所以最好的一步是U乘V转置：把梯度的每个拉伸都设成1。<bookmark mark='c'/>这就是Muon的归一化方向；下降时取它的负方向。用五次牛顿–舒尔茨迭代算出来，这些矩阵乘法把奇异值推向1。在一个真实的梯度上，有{100 * tiny:.0f}%的奇异值不到它最大奇异值的百分之一。我们先把梯度除以它的弗罗贝尼乌斯范数。<bookmark mark='d'/>五步之后，{100 * near:.0f}%落在0.6到1.3之间。第11部分会搭建这个优化器。",

    # ---------------------------------------------------------------- Spectra
    'Chapter ten.': '第10章。随机矩阵，以及训练往网络权重里写进了什么。',

    'f"What does pure noise look like':
        "纯粹的噪声，从特征值看是什么样？<bookmark mark='a'/>1955年，尤金·维格纳用随机矩阵的特征值，模拟重原子核的能级，发现了一条定律。<bookmark mark='b'/>1967年，马尔琴科和帕斯图尔找到了长方形矩阵的定律：在大矩阵极限下，W乘W转置除以M的特征值，趋近一个固定的区间和形状，由长宽比决定。我们不证明它，而是检验它。<bookmark mark='c'/>一个768乘3072的随机矩阵，和GPT-2的MLP同样形状：{len(ev)}个特征值，<bookmark mark='d'/>上面画着这条定律。{esc}",



    'f"Now a trained matrix: GPT-2\'s layer':
        "再看一个训练过的矩阵：GPT-2第{int(s['layer'])}层，它MLP的第一个矩阵，按同样的方式缩放。<bookmark mark='a'/>大多数特征值落在一个主体里，形状很像这条定律。<bookmark mark='b'/>但有{above}个严格落在图上的边界之外，不加2%的额外余量；最大值是边界值的{top:.1f}倍。这是有限样本的比较，并不是硬性的支撑区间保证。<bookmark mark='c'/>只是因为数值特别吗？把同样这些数打乱，放到随机的位置。{shuf}信息在排列里：学到的几个强方向。",



    'f"We can summarize a spectral tail':
        "我们可以用拟合的幂律密度，概括谱的尾部：密度按λ的负α次方下降。<bookmark mark='a'/>2019年，查尔斯·马丁和迈克尔·马奥尼用随机矩阵理论，研究训练过的网络里的重尾结构。这里从1.5到5的阴影带，只是描述性的比较，并不是通用的准确率标准。<bookmark mark='b'/>GPT-2的48个矩阵里，有{n_in}个拟合落在这个范围。{fit_summary}单凭一个拟合指数，不能证明幂律模型成立。独立高斯参考矩阵的极限主体有紧支撑，而不是幂律尾部。",

    'f"The same in this series\' small novels model.':
        "这个系列在小说上训练的小模型，也是一样。<bookmark mark='a'/>初始化时，它的{n}个矩阵是随机的：总共{sum(a_in)}个特征值严格高于各自的极限边界。<bookmark mark='b'/>训练之后，{every}{min(a_tr)}到{max(a_tr)}个严格落在边界之外，用的是同一个阈值，不加2%的额外余量。训练在一片噪声的海洋里，写下了一点结构。",

    # ---------------------------------------------------------------- GaLore
    'Chapter eleven.': '第11章。梯度是低秩的。',

    'A gradient is a matrix too':
        "梯度也是一个矩阵，有它自己的奇异值。<bookmark mark='a'/>一层把每个词元的向量x变成W x。<bookmark mark='b'/>根据链式法则，也就是第4部分的主题，一个权重的梯度，是对各个词元，把那个输出处的误差乘上输入，再加起来。<bookmark mark='c'/>所以梯度是一些外积之和，每个词元贡献一个秩1的块。<bookmark mark='d'/>它的秩至多是词元的个数。实际中，它往往是近似低秩的：误差和输入集中在几个共同的方向上。",

    'f"Here is a real gradient, from a small transformer':
        "这是一个真实的梯度，来自一个在小说上训练的小Transformer：一个{shape[0]}乘{shape[1]}的矩阵。<bookmark mark='a'/>它的奇异值，从大到小，对数坐标。在第{tr[0]['step']}步，前八个方向承载了梯度平方能量的{100 * tr[0]['top8']:.1f}%。<bookmark mark='b'/>实测前八个方向的占比，在第{pk['step']}步达到最大，{100 * pk['top8']:.1f}%。<bookmark mark='c'/>最后第{last['step']}步，占比是{100 * last['top8']:.1f}%，而方向一共有{n}个。游标把每一张谱，和完整能量占比轨迹上的同一步对齐。",

    'f"That is GaLore\'s idea':
        "这就是GaLore的想法，来自Jiawei Zhao、阿尼玛·阿南德库马尔、田渊栋和同事，2024年。Adam为每个权重保存两个滑动平均：一个70亿参数的模型，就多出140亿个数。<bookmark mark='a'/>GaLore把每个梯度投影到它前r个奇异方向上，<bookmark mark='b'/>在那里运行Adam，每隔一段时间更新这些方向。<bookmark mark='c'/>对我们的模型：Adam要保存{mems['adam']:,}个数，秩32时{mems['galore32']:,}个，秩8时{mems['galore8']:,}个。在大规模上，论文报告优化器内存最多减少65%，而且配合8位状态，在一张24GB的显卡上预训练了一个70亿参数的模型。",

    'f"Does a narrow window cost anything?':
        "窄窗口有代价吗？我们用Adam，以及秩32和秩8的GaLore训练这个模型。每种方法都用种子0的验证结果，从三个学习率中选出最好的，再用这个学习率跑种子0、1、2；报告的三个种子里，包含了调参用的种子。<bookmark mark='a'/>训练曲线先做八个样本的移动平均，再画均值和从最小值到最大值的带状范围，不做硬性的损失截断。<bookmark mark='b'/>留出数据上的损失：Adam {mean['adam']:.3f}，秩32 {mean['galore32']:.3f}，秩8 {mean['galore8']:.3f}。<bookmark mark='c'/>{verdict}",

    'f"GaLore wins, but most of the gap':
        "GaLore胜出，但差距的大部分，也就是{100 * split_share:.0f}%，来自GaLore给矩阵更小的步长，好让其余部分以完整的学习率训练：给Adam同样的步长，它达到{mean['adamsplit']:.3f}。在这个实验里，低秩窗口带来了剩下的提升。",

    'f"The gap comes from GaLore\'s smaller steps':
        "差距来自GaLore给矩阵更小的步长：给Adam同样的步长，在实测波动范围内，它也一样好，{mean['adamsplit']:.3f}。",

    "Adam given GaLore's step sizes does not close the gap":
        "给Adam同样的步长，也追不上：在这里，低秩窗口本身起了作用。",

    'GaLore matches Adam within the spread of the seeds':
        "在随机种子的波动范围内，GaLore和Adam一样好，内存却只用了一小部分。",

    'GaLore falls short of Adam here':
        "在这里GaLore不如Adam，这是在这个规模上省内存的代价。",

    'f"Compare LoRA, Part 27\'s tool.':
        "对比一下第27部分的工具LoRA。<bookmark mark='a'/>LoRA把权重的变化永远固定在秩r。<bookmark mark='b'/>GaLore让每一步是低秩的，但窗口会移动。<bookmark mark='c'/>600步之后，一个矩阵的总变化，用秩8窗口时有效秩是{r8['eff']:.0f}，Adam是{ra['eff']:.0f}：{tail}",

    "so its total change is far richer than rank 8.":
        "所以它的总变化远比秩8丰富。这是GaLore对LoRA局限的回答；只需要一点小改动的时候，第27部分就用LoRA。",

    "close to the window's own rank.": "接近窗口本身的秩。",

    # ---------------------------------------------------------------- Words
    'Chapter twelve.': '第12章。从计数得到词向量。',

    "Part 1's counting model treated every word as an island.":
        "第1部分的计数模型，把每个词都当成一座孤岛。办法来自语言学里的一个老想法。<bookmark mark='a'/>1954年，泽利格·哈里斯指出，出现在相同上下文里的词，意思往往相近。<bookmark mark='b'/>1957年，约翰·弗斯说：要了解一个词，就看它和什么词为伴。<bookmark mark='c'/>1990年，斯科特·迪尔韦斯特、苏珊·杜迈斯和同事把它变成了算法：数一数词在文档里出现的次数，做奇异值分解，按意义而不是按拼写来检索。",

    'f"We\'ll do it with the thirty novels.':
        "我们用那三十部小说来做。<bookmark mark='a'/>取最常见的一万个词，数每一对词在四个词以内同时出现多少次：一亿个格子，来自{w['n_words'] / 1000000.0:.2f}百万词的文本。<bookmark mark='b'/>再按第1部分的办法，把计数变成意外度：两个词相遇的次数，是偶然相遇的多少倍，取对数，就是点互信息。只留下它的正的部分。<bookmark mark='c'/>monday和morning：{w['show_pairs'][0][3]:.2f}。the和of一起出现了{int(w['show_pairs'][-1][2]):,}次，可它们和什么词都相遇：{w['show_pairs'][-1][3]:.2f}。<bookmark mark='d'/>做SVD用的表，还会先把上下文分布取四分之三次方并归一化，再只保留正值。",

    'f"Keep the table\'s hundred strongest directions':
        "用奇异值分解，留下这张表最强的一百个方向。<bookmark mark='a'/>每个词得到一百个数。<bookmark mark='b'/>与相同的词为伴的词，最后靠得很近。星期一的近邻是：{', '.join(say['monday'])}。数字三的近邻是：{', '.join(say['three'])}。狗和船也各自找到了同伴。{extra}没有人给它一本词典。",

    ' Perezvon is a dog in The Brothers Karamazov, and the Pequod':
        "Perezvon是《卡拉马佐夫兄弟》里的一条狗，Pequod是亚哈船长的船。",

    ' Perezvon is a dog in The Brothers Karamazov.':
        "Perezvon是《卡拉马佐夫兄弟》里的一条狗。",

    " The Pequod is Ahab's ship.": "Pequod是亚哈船长的船。",

    'f"How many directions does meaning need?':
        "意义需要多少个方向？只留下最强的几个。<bookmark mark='a'/>只留{ks[0]}个时，这二十个近邻里，只有{hits0}个是最终的近邻。<bookmark mark='b'/>留{ks[1]}个，<bookmark mark='c'/>{ks[2]}个，<bookmark mark='d'/>{ks[3]}个，<bookmark mark='e'/>以及全部{ks[-1]}个。我们的阈值是：五个近邻里，至少三个进入最终的十个近邻。{order[0]}在测试的{settle[order[0]]}个方向时，最先跨过阈值；{order[3]}则在{settle[order[3]]}个时跨过。这只是第一次跨过阈值，并不是说此后的近邻都固定不变。最强的方向承载大的格局；细致的意义在更后面。",

    'f"Directions mean something too.':
        "方向也有意义。<bookmark mark='a'/>从法国走到巴黎，再从英国出发，走同样的一步。<bookmark mark='b'/>{land_say}男人之于国王，正如女人之于：{mk[0]}，然后是{mk[1]}。<bookmark mark='c'/>我们从书里的词对，比如男和女、单数和复数、现在时和过去时，造了{at['all']['n']}道这样的题，最近的词有{100 * at['all']['acc']:.0f}%是对的，候选词有一万个。另一个测试只在有类别标注的词里搜索：每个类别词的五个最近邻，动物、颜色、数字等等，有{100 * pu['purity']:.0f}%属于同一类别，碰运气只有{100 * pu['chance']:.0f}%。",

    'The nearest word to where you land is London.': "落点最近的词，正是伦敦。",

    "f'The nearest word to where you land is {first}.'": "落点最近的词是{first}。",

    # ---------------------------------------------------------------- SGNS
    'Chapter thirteen.': '第13章。word2vec，原来是换了个样子的计数。',

    'f"In 2013 Tomas Mikolov and colleagues at Google':
        "2013年，谷歌的托马斯·米科洛夫和同事用一个猜谜游戏学习词向量。<bookmark mark='a'/>每个词有两个向量，一个在它作为中心词时用，一个在它作为邻居时用。<bookmark mark='b'/>训练会通过逻辑函数，提高一个词和它真实邻居的点积，并降低它和{K}个随机词的点积。<bookmark mark='c'/>这就是带负采样的跳字模型，word2vec的核心：便宜到几小时就能学完几十亿个词。",

    'f"We trained it on the novels':
        "我们在小说上训练它，用和计数时相同的词表和名义窗口。对高频词做下采样，会改变实际的上下文序列。四个词和它们的最近邻，下面是损失。<bookmark mark='a'/>开始时是随机的。<bookmark mark='b'/>{steps[1]}步之后，近邻都是最常见的词：它们最先被推动。<bookmark mark='c'/>到第{steps[mid]:,}步，意义出现了：three和{', '.join(snaps[mid]['three'][:3])}在一起。<bookmark mark='d'/>到最后，monday和{proper(snaps[-1]['monday'][0])}在一起，father和{snaps[-1]['father'][0]}在一起。没有任何东西告诉它，什么是一天，什么是亲戚。",

    'Why do guessing and counting agree?':
        "为什么猜测和计数会一致？2014年，奥默·列维和约阿夫·戈德堡说明了原因。<bookmark mark='a'/>把一个词和一个上下文的对数目标收集起来：这一对作为真实邻居出现若干次，作为负样本出现的次数，大约是k乘这个词的计数，再乘这个上下文的采样概率。<bookmark mark='b'/>把它们的点积x当作自由的；令导数为0。<bookmark mark='c'/>两个逻辑函数项之比是e的x次方。<bookmark mark='d'/>取对数：这使对数目标达到最大。如果负样本服从经验上下文分布，最好的点积就是点互信息减去log k。若像我们的训练一样，用平滑后的负采样分布，就把它的采样概率代入同一个对数计数比：这是广义的平移点互信息。",

    'f"Let\'s check it on the':
        "来检验一下，用最常见的{V}个词，运行三千步Adam。我们统计的是至少出现五次的{ex['cells']:,}个观测词对。<bookmark mark='a'/>每个向量{dims[0]}个数时，原则上所有点积都可以自由取值，但有限步训练不等于收敛证明：与广义平移点互信息相比，实测中位误差是{r0['median_err']:.3f}。<bookmark mark='b'/>{dims[1]}个数时，点散开了：{r1['median_err']:.2f}。<bookmark mark='c'/>{dims[2]}个数时，{r2['median_err']:.2f}。短的向量，只能装下这张表的一个低秩版本。",

    'f"And the real run, ten thousand words':
        "那么真实的训练，一万个词，每个一百个数呢？<bookmark mark='a'/>对它至少见过{lg['min_count']}次的{int(lg['n']):,}个词对：训练出的点积，对比它自己训练数据里的平移点互信息。<bookmark mark='b'/>相关系数{lg['r']:.2f}，斜率{lg['slope']:.2f}。{verdict}",

    'They agree closely, though the low rank pulls':
        "两者吻合得很好，只是低秩把两头往中间拉了一些。",

    'They agree only loosely':
        "两者只是大致吻合：一百个数装不下整张表，而且训练停得早。",

    'f"Which is better?':
        "哪个更好？<bookmark mark='a'/>在我们的类比题上，计数得到{100 * a1['all']['acc']:.0f}%，word2vec是{100 * a2['all']['acc']:.0f}%。{verdict}在类别近邻上，{100 * p1['purity']:.0f}对{100 * p2['purity']:.0f}。列维、戈德堡和达根在2015年发现，用同样的细心调参，两类方法相差无几。<bookmark mark='b'/>2014年的GloVe，直接拟合计数的对数。<bookmark mark='c'/>这些方法都给每个词一个向量：河岸的bank和银行的bank共用一个。第13和第14部分让向量随上下文变化。",

    'On analogies the two methods are about even.': '在类比题上，两种方法差不多。',

    'On analogies word2vec does better.': '在类比题上，word2vec更好。',

    'On analogies the counting method does better.': '在类比题上，计数的方法更好。',

    # ---------------------------------------------------------------- HighDim
    'Chapter fourteen.': '第14章。生活在768维。',

    'f"Our intuition comes from three dimensions':
        "我们的直觉来自三维，到了768维，它会误导我们。<bookmark mark='a'/>两个随机方向：在二维，什么角度都有。<bookmark mark='b'/>在三维，直角附近已经最常见。<bookmark mark='c10'/>在十维，散布是{sd[10]:.1f}度。<bookmark mark='c'/>在一百维，夹角围绕90度的标准差是{sd[100]:.1f}度，<bookmark mark='d'/>在768维，标准差是{sd[768]:.1f}度。",

    'f"Why? <bookmark mark=\'a\'/> The cosine':
        "为什么？<bookmark mark='a'/>余弦是点积除以两个长度，而每个长度都接近根号d，后面会看到。<bookmark mark='b'/>点积是d个独立乘积之和，每个均值为0、方差为1：方差是d。<bookmark mark='c'/>除以d的平方：余弦的方差是d分之1。<bookmark mark='d'/>从d等于2到{int(ds[-1])}实测，点都落在线上；在768维，{var[k768]:.5f}，对比{1 / 768:.5f}。",

    'f"So high-dimensional space is roomy.':
        "所以高维空间很宽敞。<bookmark mark='a'/>768维里一万个随机方向：每一对的夹角都在{angle_low}到{angle_high}度之间。<bookmark mark='b'/>模型把一个概念，也就是一个特征，存成一个方向；只要这些方向近似垂直就行，特征就可以远多于维数：这叫叠加，第30部分就靠它读懂模型。",

    'f"Now lengths.':
        "再看长度。<bookmark mark='a'/>d越大，一个随机向量的长度越集中在根号d附近。<bookmark mark='b'/>它的平方是d个平方之和，<bookmark mark='c'/>均值是d，方差是2d。<bookmark mark='d'/>平方根在d附近，每变化1只变化2倍根号d分之1，所以d很大时，长度的散布大约是根号2分之1：绝对长度不断增长，它的绝对散布趋近一个常数。直方图把长度除以根号d，所以相对散布会收窄。在768维实测，{nsd[k768]:.3f}。",

    'f"Volume is stranger.':
        "体积更奇怪。它按半径的d次方增长，所以半径为99%的内球，只占体积的0.99的d次方。<bookmark mark='a'/>在三维，最外面百分之一的壳占体积的{100 * shell['3']:.1f}%。在一百维，{100 * shell['100']:.1f}%。<bookmark mark='b'/>在768维，{100 * shell['768']:.2f}%：一个高维的球，几乎全是皮。",

    # ---------------------------------------------------------------- JL
    'Chapter fifteen.': '第15章。最少要多少个数，才能保住距离？',

    'f"A consequence that sounds impossible.':
        "一个听起来不可能的推论。<bookmark mark='a'/>把GPT-2的一千个向量乘上同一个随机矩阵，把768个数压成几个。这里抽样了{len(d0):,}对点，量的是普通距离，每个目标维数用一个随机映射。<bookmark mark='b'/>压到{ks[0]}个，距离全乱了；{ks[1]}个、{ks[2]}个：好一些。<bookmark mark='c'/>到{ks[3]}个，有{w_a:.0f}%的距离变化不到10%；到{ks[4]}个，{w_b:.1f}%。",

    'f"The Johnson-Lindenstrauss lemma, from 1984':
        "约翰逊–林登斯特劳斯引理，1984年，这里用的是达斯古普塔和古普塔2003年的形式。<bookmark mark='a'/>要让n个点之间的每个距离平方都保持在1加减ε倍以内，随机投影到与log n除以ε平方成比例的维数就够了。<bookmark mark='b'/>对我们的一千个点、10%的误差：{int(j['jl_k']):,}维。起始的维数根本没有出现。我们来证明它。",

    'Fix one pair, and let x be their difference':
        "固定一对点，令x是它们的差，长度为1。<bookmark mark='a'/>R x的每个坐标，都是一些独立正态数之和：仍是正态的，方差为1。<bookmark mark='b'/>长度的平方是k个这样的平方之和：卡方分布，均值为k。<bookmark mark='c'/>切尔诺夫的技巧：对e的t倍它次方用马尔可夫不等式，而它的平均值我们确切知道。<bookmark mark='d'/>选最好的t，再估计对数：拉长超过ε的概率随k指数下降，缩短也一样。<bookmark mark='e'/>对所有点对用联合界：一旦k达到4 log n除以那个小量，出任何差错的概率都小于1。好的投影一定存在，而随机的投影至少以n分之1的概率成功。",

    'f"Now the data.':
        "现在看数据。<bookmark mark='a'/>对一对点，距离平方变化超过{100 * eps:.0f}%的概率，正好是一个卡方尾巴，黄色那条。这里量的是距离平方的误差。<bookmark mark='b'/>五个随机映射的平均实测比例，与这个概率最多相差{worst_gap:.4f}；线段表示范围。共用一个映射的点对，并不独立。<bookmark mark='c'/>虚线的切尔诺夫界在精确概率上方：在{int(k768['k'])}维，是{k768['chernoff']:.2f}，而精确值是{k768['exact_fail']:.3f}。",

    'f"The lemma promises every pair at once.':
        "引理保证的是所有点对同时成立。<bookmark mark='a'/>所有点对里最差的那一对，每个k取五个随机矩阵。线段从最小值画到最大值，圆点是均值。<bookmark mark='b'/>{bound_verdict}这个置信度比较，和刚才证明的经典存在性结论，是分开的。<bookmark mark='c'/>而且在最坏的情况下，没有任何映射能好太多：2017年，卡斯珀·格林·拉森和杰拉尼·纳尔逊证明了，log n除以ε平方在常数倍以内是最优的。",

    # ---------------------------------------------------------------- Geometry
    'Chapter sixteen.': '第16章。GPT-2歪斜的空间。',

    'f"Random directions in 768 dimensions are nearly perpendicular':
        "768维里的随机方向几乎垂直，余弦是0，上下浮动{1 / np.sqrt(768):.3f}。可训练出的向量不是随机的。我们从1000到19999号词元里抽样了两千个，并不是整个词表。<bookmark mark='a'/>其中两个词元向量之间，平均余弦是{g['cos_random_mean']:.2f}：它们都往同一边歪，这个空间是各向异性的。每个向量和全词表向量的均值之间，平均余弦是{g['mean_vec_cos']:.2f}。<bookmark mark='b'/>减去均值，平均余弦降到{g['cos_centred_mean']:.3f}。",

    'f"Even centred, the spread is uneven.':
        "即使中心化了，散布也不均匀。<bookmark mark='a'/>第一主方向承载了{100 * share[0]:.1f}%的散布，均匀分配只有{100 * iso:.2f}%。<bookmark mark='b'/>按每个词元在GPT-2词表里的编号着色：编号只是合并顺序的粗略代理，并不是实测词频的排名。第一个方向跟着它走，秩相关系数{rho:.2f}。<bookmark mark='c'/>Jun Gao和同事在2019年解释了这一点：训练主要把罕见词元的向量推离各种上下文，于是罕见的词元漂到了一起。连第一个方向也去掉，也就是Mu和Viswanath 2018年的“去掉顶部方向”，平均余弦从{abtt[0]:.3f}降到{abtt[1]:.4f}。",

    'f"Inside the network it is stronger.':
        "在网络内部，这个现象更强。<bookmark mark='a'/>让GPT-2读记分牌的测试段落，一层一层看：不同位置之间的平均余弦，在输入处是{L[0]['cos']:.2f}，中间大约{mid['cos']:.2f}，最后一次归一化后是{final['cos']:.2f}。不含输入层，最大值是第{peak['layer']}层的{peak['cos']:.2f}。这演示了卡温·埃塔亚拉赫2019年测到的窄锥现象。<bookmark mark='b'/>在第{mid['layer']}层，768维里只有三个维度，它们对平均余弦的带符号贡献就占了{100 * mid['top3_share']:.0f}%；这不是平方方差的占比。蒂姆基和范施尼德尔称之为离群维度。<bookmark mark='c'/>每层中心化之后，余弦降到0附近。原始的余弦，量到的这种共同的倾斜，和意义一样多。",

    'f"Lopsided or not, directions carry meaning':
        "歪不歪斜，方向都承载着意义：我们计数得到的向量，把england送到了{an[0]}。<bookmark mark='a'/>2013年，米科洛夫、Yih和Zweig在神经网络的词向量里，发现了同样的规律。<bookmark mark='b'/>2022年，纳尔逊·埃尔哈格和同事展示了小网络把比维数更多的特征，存成近似垂直的方向。<bookmark mark='c'/>2024年，Kiho Park、Yo Joong Choe和Victor Veitch把它说清楚了：概念就是方向，但要用对的内积，不一定是普通的点积。<bookmark mark='d'/>沿着这些方向读取和操控模型，是第30部分的主题。",

    # ---------------------------------------------------------------- Netflix
    'Chapter seventeen.': '第17章。现实中的低秩：推荐与检索。',

    "Low rank's most famous test came from a DVD rental company.":
        "低秩最有名的一次检验，来自一家DVD租赁公司。<bookmark mark='a'/>2006年10月，Netflix公开了一亿条评分，来自480189位用户、17770部电影，悬赏一百万美元，谁能把留出评分预测得比它自己的系统好10%。<bookmark mark='b'/>这张表大半是空的：每位用户平均只有大约两百条评分。<bookmark mark='c'/>12月，一位署名西蒙·芬克的程序员贴出一个短程序，用梯度下降分解这张表，在排行榜上一跃而上。2009年，BellKor's Pragmatic Chaos队获胜，用的是几百个模型的组合，其中很多都是那种分解的改进版。",

    'f"The model is a sum.':
        "模型是一个和。<bookmark mark='a'/>一个平均分，加上用户的宽厚，加上电影的质量，再加上两个各有k个口味数的向量的点积。<bookmark mark='b'/>拟合已有的评分，同时让向量保持小；用户和电影的偏置，还各有一个单独的固定惩罚。<bookmark mark='c'/>一张满的表，第8章就有答案；有空洞就没有公式，只能沿梯度下降。<bookmark mark='d'/>我们造了一个小世界来检验：{m['users']:,}位用户，{m['items']:,}部电影，{m['n_ratings']:,}条评分，来自六种隐藏的类型，方法本身看不到它们。",

    'f"Training replayed, at rank':
        "回放训练过程，秩为{int(rp['rank'])}。<bookmark mark='a'/>训练用的评分上误差在降，留出的评分上也在降：从{h[0, 2]:.2f}星降到{h[-1, 2]:.3f}。{tail}<bookmark mark='b'/>右边，是每部电影的向量，画在它最强的两个方向上，按隐藏的类型着色，也画出各类型的平均位置。<bookmark mark='c'/>每部电影最近的十部电影里，有{100 * m['genre_nn']:.0f}%和它同类型，碰运气只有{100 * m['genre_chance']:.0f}%。{genre_verdict}",



    'f"How much taste does it take?':
        "口味需要多少个方向？所有方法都在相同的训练加验证评分上重新拟合，再用同一批从未碰过的测试评分评估。只猜平均分，误差是{m['rmse_mean']:.3f}星。<bookmark mark='a'/>加上宽厚和质量：{m['rmse_bias']:.3f}。<bookmark mark='b'/>再加上口味向量，秩从1到32，各三个随机种子。误差在秩{best}时最低，{vals[best].mean():.3f}{why_best}",


    'f"Factorization has a weakness':
        "矩阵分解有个弱点：新用户没有向量。今天的推荐系统用的是双塔。<bookmark mark='a'/>一个网络把用户的历史变成向量，另一个把电影的信息变成向量；分数就是它们的点积。<bookmark mark='b'/>训练让每位用户真正看过的电影，在一批里得分最高，同时按负采样分布校正。在理想的候选分类推导中，校正后的logit表达密度比，而原始分数表示条件对数概率，差一个只和用户有关的常数。我们按原始分数排序；再加热门先验，是单独的消融实验，并不是恢复概率的步骤。有限步训练未必达到这个理想。<bookmark mark='c'/>宏平均召回率，先计算每位用户所有合格的留出心头好里，有多少比例进入前十，再对用户取平均。新用户各从五部电影开始。{warm_summary}另外，{cold_summary}",





    'Retrieval is, at heart, one matrix product':
        "检索说到底是一次矩阵乘法，而技巧在于大部分都不用算。<bookmark mark='a'/>2016年，YouTube把推荐描述成在视频向量之间找最近邻。<bookmark mark='b'/>2017年，Facebook的FAISS在GPU上搜索十亿个向量。<bookmark mark='c'/>2020年，稠密段落检索把问题和段落放进同一个空间，现在的助手回答之前，就是这样找到要读的东西。第29部分会用上它。",

    # ---------------------------------------------------------------- Outro
    "Let's take stock.":
        '来总结一下。向量是带着几何的一串数；点积由柯西–施瓦茨保证，衡量相似程度。einsum给轴起名字，也数出计算量。投影找到最近的点，而运算的顺序很重要。对称矩阵沿互相垂直的方向拉伸，幂迭代能找到它们；每个矩阵都是转、拉、再转，最大的几块就是它最好的低秩副本，也允许反射，以及长方形的奇异值块。有些训练过的权重和梯度，把大小集中在强方向上。计数和猜测，通过相关的共现统计联系起来；平滑负采样给出广义的平移点互信息。而在高维里，独立的随机方向几乎垂直。随机投影能以明确的概率保住距离平方，低秩则帮助填满空着的表。',

    'All of it comes back.':
        "这些都会再出现。第4部分搭建计算每个梯度的链式法则。第9部分让每层的拉伸保持在1附近，深层网络才训练得动。第11部分搭建Muon，也就是谱范数下的最速下降。第13部分用einsum把注意力写成点积。第15部分让长上下文的记忆穿过低秩，第27部分通过它做微调，第30部分读取并操控模型内部的方向。",

    'Here are eight problems to try':
        "这里有八道题，从三角不等式到约翰逊–林登斯特劳斯引理的证明。在这里暂停，自己做一做；完整的解答在这一部分的讲义里。",

    'Next time: change.':
        "下一次：变化。这一部分里，一切都是静止的，只有那几章训练了东西，而梯度我们是拿来就用的。<bookmark mark='a'/>第4部分会搭建导数、链式法则，以及让它反向穿过几十亿个数的那台机器。",

    'For more, Gilbert Strang':
        "想深入的话，吉尔伯特·斯特朗的《线性代数与数据学习》是很友好的伙伴，特雷费森和鲍的书讲清了运算顺序为什么重要，罗曼·韦尔希宁的《高维概率》解释了大空间为什么这样表现。谢谢观看，第4部分见。",
    'f"At {confidence:g} percent confidence over the random map,': "对随机映射，以{confidence:g}%的置信度，图上第一个非平凡的界出现在k等于{good[0][2]}时。在{int(last['k'])}维，它保证距离平方的畸变至多为{last_bound:.2f}；实测最差点对的均值是{np.mean(last['worst']):.2f}。",
    "f'At {confidence:g} percent confidence, a nontrivial bound": '在{confidence:g}%置信度下，只有图上已获认证的维数有非平凡的界；最后一个抽样维数没有这样的界。',
    "f'At {confidence:g} percent confidence, none of these dimensions": '在{confidence:g}%置信度下，这些维数都无法从这个联合界得到小于1的非平凡ε。这说明界在这里没有提供有效信息，并不表示实测映射失败了。',
    ', near the six hidden genres in this synthetic world.': '，接近这个人造世界里隐藏的六种类型。',
    'f" With no vector penalty, held-out error rises': '没有向量惩罚时，留出误差从最低的{best:.3f}回升到{other:.3f}星。',
    'f" With no vector penalty, held-out error finishes': '没有向量惩罚时，留出误差最后是{other:.3f}星，没有明显的后期回升。',
    'f"{rebound} Its final error is': '{rebound}把最终误差和有向量惩罚时的{last:.3f}星相比：{comparison}。两次训练都保留相同的偏置惩罚。',
    "f'{above} eigenvalues lie strictly beyond the plotted limiting edge;": '{above}个特征值严格落在图上的极限边界之外；有限样本可以越过它。',
    "f'After shuffling, {sh_above} eigenvalues lie strictly beyond": '打乱后，{sh_above}个特征值严格落在同一个极限边界之外。',
    'f"Our displayed layer has alpha': "图上这一层的α是{s['alpha']:.2f}，用{s['n_tail']}个尾部特征值拟合，双侧KS距离是{s['ks']:.3f}。",
    'Our displayed layer has no available power-law tail fit under this selection rule.': '按这个选择规则，图上这一层没有可用的幂律尾部拟合。',
    'The final genre-neighbour agreement exceeds the without-self chance baseline.': '最终，近邻同类型的比例，高于排除自身后的随机基线。',
    'The final genre-neighbour agreement does not exceed the without-self chance baseline.': '最终，近邻同类型的比例，没有高于排除自身后的随机基线。',
    'f"For {name}, recall is unavailable:': '对{name}，召回率不可用：{users}位参与评估的用户，共有{targets}个合格的留出目标。没有目标的用户被排除，因此这里没有热门推荐对照。',
    'f"For {name}, both recall measurements are unavailable': '对{name}，虽然有{users}位参与评估的用户和{targets}个合格目标，但两项召回测量都不可用，无法进行有限数值的比较。',
    'f"For {name}, two-tower recall is unavailable': '对{name}，{users}位用户和{targets}个合格目标上的双塔召回率不可用；热门推荐的召回率是{popularity:.2f}。无法比较。',
    'f"For {name}, two-tower recall is {recall:.2f}': '对{name}，双塔召回率是{recall:.2f}，来自{users}位用户和{targets}个合格目标；但热门推荐的召回率不可用。无法比较。',
    'f"For {name}, macro recall reaches': '对{name}，宏平均召回率达到{recall:.2f}，热门推荐是{popularity:.2f}，评估了{users}位用户和{targets}个合格目标。{comparison}',
    'The two towers beat popularity for this cohort.': '对这组用户，双塔胜过热门推荐。',
    'The two towers do not beat popularity for this cohort.': '对这组用户，双塔没有胜过热门推荐。',
}

PHRASES = {
    'known users': '已知用户',
    'new users': '新用户',
    'higher than': '更高',
    'lower than': '更低',
    'within 0.01 stars of': '相差不超过0.01星',
    'every matrix has': '每个矩阵都有',
    'the matrices have': '各矩阵有',
    'close to the prediction': '和预测很接近',
    'B and C': 'B和C',
    'A and B': 'A和B',
    'A and C': 'A和C',
}
