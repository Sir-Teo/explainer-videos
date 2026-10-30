"""Chinese narration for ai5: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第5部分：运动中的随机'

CHAPTERS = {
    'Hook': '从噪声中来',
    'Bell': '1. 钟形曲线',
    'Gauss': '2. 多维的钟形曲线',
    'Likelihood': '3. 拟合钟形曲线：最大似然',
    'Fisher': '4. 估计能有多精确？',
    'Bayes': '5. 用分布表达信念',
    'MaxEnt': '6. 最大熵',
    'Tails': '7. 离平均值能有多远？',
    'Sampling': '8. 掷灌铅的骰子',
    'Decoding': '9. 语言模型怎样选词',
    'Markov': '10. 记性很短的链',
    'MonteCarlo': '11. 从随机样本里求答案',
    'ScoreFn': '12. 平均值的梯度',
    'MCMC': '13. 从无法直接采样的分布中采样',
    'Brownian': '14. 布朗运动',
    'Ito': '15. 伊藤引理',
    'SDE': '16. 带着推力的随机',
    'FokkerPlanck': '17. 密度自己的定律',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'Here are six hundred dots, scattered completely at random.':
        "这里有600个点，完全随机地散布着。<bookmark mark='a'/>现在，让每个点随意游荡。每一刻，它都会被随机地轻踢一下，同时还被一片箭头场轻轻推一把。<bookmark mark='b'/>看看随机性会搭出什么来。",
    "This is, in miniature, how today's image and video generators work.":
        "这就是当今图像和视频生成器工作方式的缩影。它们从噪声出发，让它一次一小步、随机地流动，最后变成一幅画面。<bookmark mark='a'/>那些箭头就是全部的秘密：网络要学的，正是它们。我们会在第21部分把它们搭出来。",
    'Run it the other way, with the arrows gone':
        "反过来运行，去掉箭头，这些字母又溶解回噪声。<bookmark mark='a'/>两个方向都是随机运动，描述它们的，是同一套数学。",
    'The mathematics is older than computers.':
        "这套数学比计算机还要古老。它始于1654年，帕斯卡和费马在通信中讨论：一局没下完的赌博，赌注该怎么分。<bookmark mark='a'/>伯努利证明了平均值会稳定下来；<bookmark mark='b'/>棣莫弗找到了钟形曲线；<bookmark mark='c'/>贝叶斯和拉普拉斯从结果倒推原因；<bookmark mark='d'/>高斯用它拟合行星轨道。<bookmark mark='e'/>爱因斯坦解释了花粉的抖动，<bookmark mark='f'/>费希尔让似然成为拟合模型的方法，<bookmark mark='g'/>伊藤清给随机运动配上了自己的微积分。<bookmark mark='h'/>在洛斯阿拉莫斯，最早的计算机被用来做采样，<bookmark mark='i'/>而今天，同样的想法决定着聊天机器人写出的每一个词，也把噪声变成图画。",
    'This is Part 5 of AI, Built, the last of the foundations.':
        "这是《人工智能，从零搭建》的第5部分，也是基础篇的最后一部分。<bookmark mark='a'/>这一部分讲：为什么和总是呈钟形，在一维和多维中；拟合、精度与信念；平均值会偏离多远；怎样抽取样本，以及语言模型怎样挑选下一个词；马尔可夫链与蒙特卡洛；还有随机运动，以及它自己的一套微积分。每一个结果，都在这里、在一台笔记本电脑上算出来。",

    # ------------------------------------------------------------------ 1. Bell
    'Chapter one. The bell curve.': '第1章。钟形曲线。',
    'f"Flip a fair coin and track the share of heads.':
        "抛一枚均匀的硬币，记下正面所占的比例。<bookmark mark='a'/>六组各5000次的抛掷，全都向二分之一靠拢，这里落在{lo:.3f}到{hi:.3f}之间：这就是雅各布·伯努利的大数定律，1713年出版。<bookmark mark='b'/>抛了n次之后，一组会偏离多少？大约是n的平方根分之一。这种偏离的形状，就是本章的主题。",
    'Here is the scatter made visible':
        "把这种偏离画出来：小球落过十二排钉子，在每颗钉子上向左或向右弹开，各占一半。<bookmark mark='a'/>小球落在哪里，就数出了它向右弹了几次。<bookmark mark='b'/>80个球，开始显出一个形状。",
    'A thousand make it unmistakable.':
        "1000个球，形状就毫无疑问了。<bookmark mark='a'/>数一数路径就得到精确的概率：12选k，除以2的12次方。<bookmark mark='b'/>贴着它们的那条光滑曲线，就是钟形曲线，也就是正态分布，它有中心μ和宽度σ，这里是6和根号3。棣莫弗在1733年找到了它，正是这些计数的极限。",
    'Why a bell, and why so often?':
        "为什么是钟形，又为什么这么常见？一颗骰子：六根一样高的柱子。<bookmark mark='a'/>两颗：一个三角形。三颗：已经开始变圆。<bookmark mark='b'/>六颗、十二颗：钟形曲线。<bookmark mark='c'/>这就是中心极限定理：把许多独立的小块加起来，不管每一块是什么形状，和都是钟形的，<bookmark mark='d'/>而它的宽度，随块数的平方根增长。拉普拉斯在1810年证明了它。",
    'Why? Two dice add up to s':
        "为什么？两颗骰子加起来等于s，有多少种把s拆开的方法：一颗是x，另一颗是s减x。<bookmark mark='a'/>换成密度，求和就变成积分，也就是卷积。<bookmark mark='b'/>用一个歪向一边的分布来画：指数分布。把它翻过来，滑到s，再相乘：重叠部分的面积，就是和在s处的密度。<bookmark mark='c'/>让s一路滑过去，这个面积就描出两块之和的密度。<bookmark mark='d'/>n块，就要做n减1次卷积。",
    'So convolve again and again.':
        "那就一次又一次地卷积。一个指数分布，全都挤在一边。<bookmark mark='a'/>两个、三个、五个：每次卷积都把它抹平、摊开。<bookmark mark='b'/>十个、三十个：歪斜消失了，剩下的就是钟形曲线。卷积是一种平均，而在平均之下，除了缩放，唯一不变的形状就是钟形曲线。",
    'f"How fast does the bell arrive?':
        "钟形曲线来得有多快？量一量和的累积分布与钟形曲线的累积分布之间最大的差距。<bookmark mark='a'/>对指数分布，它落在斜率为{es:.2f}的直线上：差距像n的平方根分之一那样缩小，64块之后是{ed[k64]:.3f}。<bookmark mark='b'/>这就是贝里-埃森定理：差距至多是一个常数，乘以三阶绝对矩除以宽度的立方，再除以n的平方根；测出来的差距就在它下面。<bookmark mark='c'/>{sym}",
    "f'The uniform pieces, symmetric, close the gap much faster":
        "均匀分布的小块是对称的，差距缩小得快得多：斜率{us:.1f}，像n分之一，因为没有偏斜，对钟形曲线的第一项修正抵消了。",
    "f'The uniform pieces close the gap at about the same rate":
        "均匀分布的小块，差距缩小的速度差不多，斜率{us:.1f}。",

    # ------------------------------------------------------------------ 2. Gauss
    'Chapter two. Bells in many dimensions.': '第2章。多维的钟形曲线。',
    'Start with the simplest cloud in the plane':
        "从平面上最简单的点云开始：两个独立的标准钟形分布，各沿一根坐标轴。<bookmark mark='a'/>任何维度的任何高斯分布，都是它经过一个线性映射：x等于μ加上L乘以z。<bookmark mark='b'/>这个映射可以用协方差Σ来概括，它等于L乘以L的转置：每一对坐标一起变化的程度。<bookmark mark='c'/>密度的等高线是椭圆，轴沿着协方差的特征向量，长度由特征值的平方根决定，这正是第3部分的内容。",
    'Now the question that matters for prediction':
        "现在是对预测最要紧的问题：如果知道了一部分坐标，x_b，其余的x_a还剩下什么？<bookmark mark='a'/>固定x_b，条件密度就是联合密度，再重新归一。<bookmark mark='b'/>它的对数，是协方差之逆的一个二次型，这个逆叫作精度矩阵。<bookmark mark='c'/>把关于x_a的项收集起来，配方：又是一个钟形分布，精度是Λ_aa。<bookmark mark='d'/>分块求逆，得到它的协方差：Σ_aa减去Σ_ab乘Σ_bb的逆乘Σ_ba，也就是舒尔补。<bookmark mark='e'/>而它的均值，从μ_a出发，按我们所知道的信息做一个线性的移动。",
    'f"Check it on samples.':
        "用样本来检验。抽出40万个点，留下落在x_2等于{a:g}的一条细带里的点。<bookmark mark='a'/>它们的x_1值构成一个钟形分布。公式预测它的均值是{m_th:.3f}，方差是{v_th:.3f}；细带里的{n_sl:,}个点给出{m_e:.3f}和{v_e:.3f}。{verdict}<bookmark mark='b'/>让细带滑动，条件均值就画出一条直线。高尔顿在1886年为父母和子女的身高画出了它，称之为回归：高个子父母的孩子也高，但没那么高。",
    'Both agree with the formulas to within the sampling error.':
        "两者都在抽样误差之内与公式吻合。",
    'Close, but not within the sampling error':
        "很接近，但超出了抽样误差：细带本身有宽度，这带来了一点偏差。",
    'This one formula does a great deal of work.':
        "这一个公式做了大量的工作。<bookmark mark='a'/>1960年，鲁道夫·卡尔曼用它追踪运动的物体，每来一次新的测量就条件化一次；他的滤波器为阿波罗飞船导航。<bookmark mark='b'/>高斯过程把钟形分布放在整个函数上，用数据拟合它，就是这样的条件化。<bookmark mark='c'/>而在第21部分，扩散模型从噪声往回走的每一步，都是一个高斯条件分布，用的正是这个公式。",

    # ------------------------------------------------------------------ 3. Likelihood
    'Chapter three. Fitting a bell to data.': '第3章。给数据拟合钟形曲线。',
    'Here are the thousand balls again.':
        "还是那1000个球。哪条钟形曲线最能描述它们？<bookmark mark='a'/>先试一条。这样给它打分：在每个球的位置，读出钟形曲线的高度。<bookmark mark='p'/>这个高度是概率密度：表示结果在那里有多拥挤。把直方图的柱子做得越来越窄，它就变成一条像这样的光滑曲线；<bookmark mark='q'/>两点之间曲线下方的面积，就是落在这两点之间的概率。对高度取对数，再对所有球求平均。这就是对数似然：这条钟形曲线，把球的实际落点预测得有多好。<bookmark mark='b'/>位置放错的钟形曲线，得分很低。<bookmark mark='c'/>太窄的也一样，<bookmark mark='d'/>太宽的也一样。<bookmark mark='e'/>最好的那一条，也就是最大似然拟合，是让数据显得最不意外的那一条。",
    'f"Score every possible bell':
        "给每一条可能的钟形曲线打分，每个中心、每个宽度，这些分数就构成一片地形。<bookmark mark='a'/>从第4部分我们知道怎样找到它的顶峰：沿着梯度往上爬。<bookmark mark='b'/>到了山顶，中心是这些球的平均值{m:.2f}，宽度是它们的离散程度{s_hat:.2f}，接近钉板预测的根号3。对钟形曲线来说，最大似然给出的，正是对数据最自然的两个概括。",
    "And here's the connection to everything else.":
        "这就是它和其他一切的联系。最大化平均对数似然，<bookmark mark='a'/>等于最小化平均意外度，<bookmark mark='b'/>而这就是第1部分的交叉熵，对照数据来计算。<bookmark mark='c'/>最大似然就是最小交叉熵。本系列的每一个模型，从一条钟形曲线到一个语言模型，都是这样训练的。",
    'f"Is maximum likelihood right on average?':
        "最大似然平均来说准吗？对中心，准。对宽度，不准。<bookmark mark='a'/>围绕样本自己的平均值去量离散程度，会少掉一点：样本平均值离数据，比真正的中心离得更近。<bookmark mark='b'/>平均下来，正好少掉一个σ的平方，<bookmark mark='c'/>所以最大似然的方差偏小，是真实值的n分之n减1。<bookmark mark='d'/>{verdict}随着n增大，偏差逐渐消失。1922年给似然命名的费希尔，关心的与其说是偏差，不如说是效率：误差最小能有多小。这就是下一章。",
    'f"Measured on {R:,} samples of five, the average is {mle[i5]:.3f}, against the predicted {th[i5]:.2f}; dividing':
        "在{R:,}组、每组5个的样本上测量，平均是{mle[i5]:.3f}，预测是{th[i5]:.2f}；除以n减1，也就是贝塞尔校正，得到{bes[i5]:.3f}。",
    "f'Measured on {R:,} samples of five":
        "在{R:,}组、每组5个的样本上测量，平均是{mle[i5]:.3f}，预测是{th[i5]:.2f}。",

    # ------------------------------------------------------------------ 4. Fisher
    'Chapter four. How precise can an estimate be?': '第4章。估计能有多精确？',
    'f"Here is a distribution with heavy tails, the Cauchy.':
        "这是一个尾巴很重的分布：柯西分布。它看起来像钟形曲线，但尾巴重到没有平均值：时不时就有一次抽样落到离谱的远处。<bookmark mark='a'/>试着用100次抽样估计它的中心。样本平均值毫无用处：它的离散程度永远不缩小；平均值的中间一半，在{ns[0]}次抽样时跨度{iqr[0]:.1f}，到{ns[-1]}次时仍是{iqr[-1]:.1f}。<bookmark mark='b'/>中位数好得多，<bookmark mark='c'/>最大似然更好。有没有一个最好的极限？",
    'f"There is, and Fisher found the key in 1925.':
        "有，费希尔在1925年找到了关键。<bookmark mark='a'/>分数是对数似然对参数的斜率：每个观测把估计往哪边拉、拉多大。<bookmark mark='b'/>在真实值处，它的平均为零，因为密度的积分永远是1。<bookmark mark='c'/>它的方差就是费希尔信息：数据把θ钉得有多牢。柯西分布的费希尔信息是二分之一；在20万次抽样上，我们测得{sv:.3f}。<bookmark mark='d'/>一个无偏估计随θ一比一地移动，所以它和分数的协方差是1。<bookmark mark='e'/>柯西-施瓦茨不等式说，协方差的平方至多是两个方差的乘积。所以，任何无偏估计的方差，都不可能低于n乘以信息的倒数：这就是克拉默-拉奥下界，由拉奥在1945年、克拉默在1946年证明。",
    'f"Now measure it. Multiply each estimate':
        "现在来测量。把每种估计的方差乘以n，这样一个理想的n分之一的估计就是一条水平线；下界是高度为2的那条线。<bookmark mark='a'/>中位数稳定在{med[-1]:.2f}，接近它的理论值π的平方除以4：比下界差了约四分之一，而且永远如此。<bookmark mark='b'/>最大似然起点很高，5次抽样时是{mle[0]:.1f}，但{verdict}<bookmark mark='c'/>这就是费希尔所说的有效性：在大样本下，没有什么能胜过最大似然。",
    "f'by {int(ns[-1])} draws it is {mle[-1]:.2f}, within a few percent":
        "到{int(ns[-1])}次抽样时是{mle[-1]:.2f}，与下界只差百分之几。",
    "f'by {int(ns[-1])} draws it is {mle[-1]:.2f}, still above":
        "到{int(ns[-1])}次抽样时是{mle[-1]:.2f}，仍在下界之上。",
    'With many parameters, the information becomes a matrix':
        "参数多了，信息就变成一个矩阵：分数的外积的平均。<bookmark mark='a'/>1998年，甘利俊一提出用它来度量梯度下降的步子，让一步的大小取决于模型的预测改变了多少，而不是权重：这就是自然梯度。<bookmark mark='b'/>2017年，弹性权重巩固用它来保护网络已经学会的东西。<bookmark mark='c'/>今天那些考虑曲率的优化器，逐层近似它，或者它的近亲。第11部分会接着讲。",

    # ------------------------------------------------------------------ 5. Bayes
    'Chapter five. Belief as a distribution.': '第5章。用分布表达信念。',
    'How often is a letter an e?':
        "字母是e的频率有多高？读之前，我们一无所知：从0到1的任何比例，看起来都一样可能。这就是一个信念，我们可以把它画成覆盖所有可能性的一条平线。<bookmark mark='a'/>贝叶斯法则，出自托马斯·贝叶斯1763年的论文，1774年又被拉普拉斯独立发现，它说明了证据到来时该怎样更新信念：把原来的信念，乘以每种可能性对证据的解释程度，再重新缩放，让总和回到1。<bookmark mark='b'/>“正比于”这个符号就是这个意思：相等，只差那一次缩放。",
    'f"Read the first ten letters':
        "读前10个字母：{ks[1]}个e。<bookmark mark='a'/>信念偏向{ks[1] / ns[1]:.1f}，但还很宽。<bookmark mark='b'/>读了100个字母，窄了一些。<bookmark mark='c'/>读了1000个，更窄。<bookmark mark='d'/>读了1万个，它成了{pk:.3f}附近的一个尖峰：95%的信念落在{ci[0]:.3f}到{ci[1]:.3f}之间。<bookmark mark='e'/>整段文字，全部{int(d['n_all']):,}个字母，给出{e_all:.3f}，在这个范围{('inside' if ci[0] < e_all < ci[1] else 'outside')}。",
    'f"Why did the belief keep this shape?':
        "信念为什么一直保持这个形状？<bookmark mark='a'/>每读一个字母，就乘进一个θ或1减θ，所以n个字母里有k个e时，似然就是θ的k次方乘以1减θ的n减k次方。<bookmark mark='b'/>从一个同样形状的先验出发，也就是贝塔分布，<bookmark mark='c'/>指数直接相加：信念始终是贝塔分布，更新就是计数。<bookmark mark='d'/>它的均值是k加a除以n加a加b：先验就像想象中的a个e和b个其他字母。先验是平的时候，这就是拉普拉斯1774年的接续法则：k加1除以n加2，读完前10个字母时是{m_flat:.2f}。<bookmark mark='e'/>不同的先验起点各不相同，同样的字母把它们拉到一起：读到1万个字母时，它们已经一致了。",
    'f"A belief can also be used to pick a single answer':
        "信念也可以用来挑出一个答案：后验的峰值，叫作MAP，最大后验估计。<bookmark mark='a'/>给模型的权重一个高斯先验，意思是小权重更可能，<bookmark mark='b'/>再给它的输出加上高斯噪声。<bookmark mark='c'/>MAP的答案，就是最小化平方误差加上λ乘以权重的平方大小：这正是训练几乎所有网络时用的权重衰减，λ等于噪声与先验宽度之比的平方。<bookmark mark='d'/>来自正弦波的10个点，配一个9次多项式。最大似然穿过每一个点，在点与点之间剧烈摆动。先验把它驯服了。{verdict}",
    'f"Over two hundred training sets, maximum likelihood':
        "在200个训练集上，最大似然的测试误差中位数是{d['mle_med']:.2f}；最好的λ，大约{lam_m:.0f}乘以10的负{lam_e}次方，把它降到{d['best_err']:.3f}。",
    "f'Over two hundred training sets, the prior did not help":
        "在200个训练集上，先验没有帮上忙：{d['best_err']:.3f}，对比{d['mle_med']:.3f}。",

    # ------------------------------------------------------------------ 6. MaxEnt
    'Chapter six. Maximum entropy.': '第6章。最大熵。',
    'Here is a puzzle from the physicist Edwin Jaynes.':
        "这是物理学家埃德温·杰恩斯出的一道谜题。一颗骰子被做了手脚，点数的平均是4.5，而不是3.5。每个面的概率是多少？<bookmark mark='a'/>平均为4.5的骰子有无穷多个：这个、这个、还有这个。<bookmark mark='b'/>杰恩斯的回答：挑那个不做任何多余假设的，也就是剩下的不确定性最多的那个，用第1部分的熵来衡量。任何更集中的分布，都在声称我们并不具备的知识。",
    "Finding it is part four's constrained optimization.":
        "找到它，就是第4部分的约束优化。<bookmark mark='a'/>最大化熵，满足两个约束：概率加起来是1，平均是4.5。<bookmark mark='b'/>给每个约束配一个拉格朗日乘子。<bookmark mark='c'/>令导数为零，每个概率的对数就成了点数的一条直线：<bookmark mark='d'/>k点的概率等于e的λk次方，再除以归一化常数Z。<bookmark mark='e'/>唯一的未知数是λ，而log Z的导数就是平均值，所以一个方程就能定下它。",
    'f"Solving that one equation is a tiny training run.':
        "解这一个方程，就是一次小小的训练。从均匀的骰子出发，λ为零，然后按平均值离4.5还差多少，推一推λ。<bookmark mark='a'/>骰子向大点数倾斜，最后停在λ等于{lam:.3f}：每个面的概率，大约是下一个面的{math.exp(lam):.2f}倍。<bookmark mark='b'/>它的熵是{H:.4f}奈特。另外两万颗随机造出、平均相同的骰子：{verdict}。",
    "f'the highest of them reaches {Hmax:.4f}, just under'":
        "其中最高的达到{Hmax:.4f}，刚好在它之下",
    'f"one of them reaches {Hmax:.4f}':
        "其中一颗达到{Hmax:.4f}，和最大值相当",
    'The same recipe gives the distributions this series keeps meeting.':
        "同一个配方，能得出本系列一再遇到的那些分布。<bookmark mark='a'/>在实数轴上，固定均值和方差，用数值方法求解，得到的就是钟形曲线：在给定宽度的分布里，它的不确定性最大。<bookmark mark='b'/>改为固定到零点的平均距离，得到的是拉普拉斯的双边指数分布。<bookmark mark='c'/>固定一个物理系统的平均能量，得到的是玻尔兹曼和吉布斯的分布，e的负能量除以温度次方，其中温度就是拉格朗日乘子。把能量换成分数，这就是每个语言模型最后那个softmax。<bookmark mark='d'/>它们都属于同一个家族，指数族；在指数族里，对数归一化常数的梯度就是平均值。所以用最大似然拟合它，就是让它的平均值与数据的平均值相等。",

    # ------------------------------------------------------------------ 7. Tails
    'Chapter seven. How far from the average?': '第7章。离平均值能有多远？',
    'f"The law of large numbers says an average settles.':
        "大数定律说，平均值会稳定下来。从数据中学习需要更多：它有多大可能仍然偏得很远？100次均匀抛掷，重复100万组。<bookmark mark='a'/>正面比例达到{0.5 + eps:g}的，占其中的{ex:.3f}。<bookmark mark='b'/>这里我们可以直接数，但模型的测试数据从不给我们看这张图。我们需要一个不管分布是什么都成立的保证，只知道每个值都在0和1之间。",
    'Each bound comes from the one before.':
        "每个界都来自前一个。<bookmark mark='a'/>马尔可夫不等式：一个永远不为负的量，不可能经常远大于它的平均值。<bookmark mark='b'/>把它用在到均值的距离的平方上：切比雪夫不等式，方差除以ε的平方，而n个数的平均，方差小n倍。<bookmark mark='c'/>切尔诺夫的想法：把马尔可夫不等式用在e的t乘以和次方上；独立性把它拆成乘积，尾部就随n指数下降。<bookmark mark='d'/>对0到1之间的值，霍夫丁引理给每个因子一个上界，<bookmark mark='e'/>取最好的t，就得到e的负2nε平方次方：霍夫丁不等式，1963年。",
    'f"Now put them against the truth':
        "现在把它们和真实值放在一起，用对数刻度。精确的尾部概率，和叠在上面的100万次模拟。<bookmark mark='a'/>马尔可夫的界几乎不下降；在ε等于{eps[j]:g}时，它允许{vals['markov']:.2f}。<bookmark mark='b'/>切比雪夫的界像ε的平方分之一那样下降：{vals['cheb']:.2f}。<bookmark mark='c'/>切尔诺夫和霍夫丁的界指数下降，在这里几乎重合：{vals['chern']:.3f}和{vals['hoeff']:.3f}。{verdict}霍夫丁的界仍是真实值{ex[j]:.3f}的{ratio:.0f}倍：这是对形状一无所知的代价。",
    'Each bound is tighter than the one before, and all of them are loose.':
        "每个界都比前一个更紧，但全都很松。",
    'Each bound holds here, but all of them loosely.':
        "每个界在这里都成立，但都很松。",
    'f"Turn it around.':
        "反过来问。要抛多少次，才能保证正面比例超出{e0:g}的情况，最多占{100 * d0:g}%？<bookmark mark='a'/>切比雪夫的界要求{need['chebyshev']:,}次；霍夫丁的，{need['hoeffding']:,}次；切尔诺夫的，{need['chernoff']:,}次。<bookmark mark='b'/>对均匀硬币，真实答案是{need['exact']}次：最好的界要求的次数是它的{best / need['exact']:.1f}倍，这是对所有分布都成立的代价。<bookmark mark='c'/>第8部分正是用它，从测试分数推出模型真实误差的界；第26部分用霍夫丁的界来探索。",

    # ------------------------------------------------------------------ 8. Sampling
    'Chapter eight. Rolling loaded dice.': '第8章。掷灌铅的骰子。',
    'A model never hands us a word, only a distribution':
        "模型从不直接给我们一个词，只给一个分布；要写出任何东西，都得掷一颗灌了铅的骰子。<bookmark mark='a'/>把概率从0到1首尾相接排开，每个字母占据的长度正好等于它的概率。<bookmark mark='b'/>随机均匀地选一个点，取它落在的那个字母：这就是累积分布函数的逆。<bookmark mark='c'/>这些字母是按第1部分的字母频率抽出来的。",
    'f"The same trick works for continuous distributions.':
        "同一个技巧也适用于连续分布。<bookmark mark='a'/>对指数分布，x等于负的对数1减u：两万次抽样与密度吻合，累积分布的最大差距是{float(d['ks_exp']):.3f}。<bookmark mark='b'/>逆函数难算的时候，约翰·冯·诺依曼1951年的拒绝采样只需要密度：在曲线上方的盒子里均匀地撒点，留下落在曲线下面的。<bookmark mark='c'/>留下的点就服从这个密度。代价是浪费：只留下{100 * rate:.1f}%，等于盒子高度的倒数，和预测的一样；而在高维中，这个比例会崩塌。",
    'The bell itself has no simple inverse CDF':
        "钟形分布本身没有简单的逆累积分布函数，但一对钟形分布有，用极坐标。<bookmark mark='a'/>两个独立的钟形分布，密度只取决于到中心的距离。<bookmark mark='b'/>所以角度是均匀的，而半径的平方的一半服从指数分布，我们刚学会怎么抽它。<bookmark mark='c'/>进去两个均匀随机数，出来两个独立的钟形分布：1958年的博克斯-穆勒变换。",
    'f"One more trick, used constantly in machine learning.':
        "还有一个技巧，机器学习里一直在用。要按分数的softmax挑选选项i，就给每个分数加上独立的冈贝尔噪声，也就是一个均匀随机数取两次负对数，<bookmark mark='a'/>再取最大的那个。<bookmark mark='b'/>胜出者恰好服从softmax：冈贝尔分布就是最大值的形状。<bookmark mark='c'/>20万次挑选与softmax对比：{verdict}它只需要分数，从来不需要归一化常数，并把采样变成了取最大值。",
    "f'they agree, with a chi-squared":
        "两者吻合，卡方值是{chi2:.1f}，自由度5，正是偶然所给的水平。",
    "f'chi-squared is {chi2:.1f}":
        "卡方值是{chi2:.1f}，超出了偶然应有的水平。",
    'f"Sampling can\'t be differentiated':
        "采样没法求导：选了就是选了。2017年，两个团队提出把它放松。把取最大值换成一个带温度τ的softmax：冈贝尔-softmax。<bookmark mark='a'/>冷的时候，τ等于0.1，每次抽样几乎都是独热的选择，最大的那一项平均是{onehot[0]:.2f}。<bookmark mark='b'/>τ等于1时更柔和，<bookmark mark='c'/>τ等于5时一片模糊，{onehot[-1]:.2f}。温度用忠实度换来平滑的梯度；第一代DALL-E的离散编码，就是这样训练的。",

    # ------------------------------------------------------------------ 9. Decoding
    'Chapter nine. How a language model chooses.': '第9章。语言模型怎样选词。',
    'f"A language model ends every step with a distribution':
        "语言模型的每一步，都以整个词表上的一个分布结束，解码就是从中挑选。<bookmark mark='a'/>这是GPT-2对下面这句话后一个词的分布：Spade sat down in the armchair, and。它最喜欢的词只占{100 * p1[0]:.0f}%。<bookmark mark='b'/>第一个旋钮是温度：在softmax之前把分数除以T，这就是第6章的吉布斯分布。",
    'f"Turn it down, below one':
        "把它调低，低于1，分布就向最喜欢的那几个词收紧。<bookmark mark='a'/>调高，它就变平，直到下一个词几乎可以是任何词。<bookmark mark='b'/>熵跟着旋钮变化：T等于0.5时{d['H0.5']:.1f}比特，1时{d['H1.0']:.1f}，2时{d['H2.0']:.1f}。",
    "Here's what comes out.":
        "看看写出来的东西。<bookmark mark='a'/>永远选最喜欢的词，稳妥但平淡。<bookmark mark='b'/>T等于0.5，仍然通顺。<bookmark mark='c'/>T等于1，按模型自己的分布采样，更怪，也更多样。<bookmark mark='d'/>T等于2，就散架了：那五万个不太可能的词，每个都很小，合起来却太常胜出。",
    'f"Temperature reshapes the distribution':
        "温度改变整个分布的形状，但那条由不太可能的词构成的长尾始终都在。其他旋钮把它切掉。<bookmark mark='a'/>GPT-2的两个真实时刻：一个是开放的，最喜欢的词占{100 * s0[0]:.0f}%；另一个几乎确定，它占{100 * s1[0]:.0f}%。<bookmark mark='b'/>top-k保留固定数目的词：在第二种情况下太多，在第一种情况下太少。<bookmark mark='c'/>top-p，也叫核采样，保留概率加起来达到p的最少的那些词，所以切口会自适应：在p等于0.9时，开放的情况保留{k09[0]:,}个词，确定的情况保留{k09[1]}个。<bookmark mark='d'/>min-p保留所有概率至少是最喜欢的词的某个比例的词：比例为0.1时，分别是{m01[0]}个和{m01[1]}个。",
    'f"Which rule writes best?':
        "哪种规则写得最好？我们在本系列自己的小模型上做了测试，它是用那三十部小说训练的：12段它从没见过的文字，每段续写8次，共17种设置。由一个更大的模型GPT-2来评判，看它对每段续写有多意外。<bookmark mark='a'/>{v0}<bookmark mark='b'/>{v1}<bookmark mark='c'/>贪心解码是评判者的最爱，然而它的四词片段里有{100 * rep_g:.0f}%是重复的，而任何采样设置至多只有{100 * rep_s:.1f}%：只看似然，就会奖励兜圈子。{v2}这正是霍尔茨曼的观点：好的文字，并不是最可能的文字。",
    'Every rule trades the same way':
        "每种规则都在做同样的交换：让评判者觉得更可能的设置，也让同一段的各个续写更加相似。",
    'The rules do not all trade predictability against diversity':
        "这些规则在可预测性和多样性之间的交换方式并不相同。",
    'The rules cover different ranges of diversity':
        "这些规则覆盖的多样性范围不同，没法在同一点上比较。",
    "f'At the same diversity the four rules are almost indistinguishable":
        "在相同的多样性下，四种规则几乎分不出高下：彼此相差不到每字符{spread:.3f}奈特。",
    "f'At the same diversity, {SPOKEN[best]} gives the text":
        "在相同的多样性下，{SPOKEN[best]}写出的文字，评判者觉得最可能：每字符{at[best]:.3f}奈特，而只用温度是{at['temp']:.3f}；在多样性最接近的一对设置上，它在{len(diff)}段文字中赢了{wins}段。",
    "f'At the same diversity, temperature alone does as well":
        "在相同的多样性下，只用温度，和任何截断规则一样好：每字符{at['temp']:.3f}奈特。",
    'f"Human prose sits between':
        "人写的文字处在中间：评判者对它的意外程度，相当于我们的模型在温度约为{Th:.1f}时写的文字。",
    '"Here is one passage, continued four ways.':
        "这是其中一段，用四种方式续写。<bookmark mark='a'/>{g_line}<bookmark mark='b'/>纯采样会跑题。<bookmark mark='c'/>截断规则介于两者之间。min-p在2024年被提出，是为了能安全地用更高的温度；2025年的一项重新分析对它提出质疑，认为证据比报告的要弱。第19部分会补上解码的另一半：限制哪些内容根本可以写出来。",
    'Greedy decoding circles back on itself, again and again.':
        "贪心解码一次又一次地兜回原处。",
    'Greedy decoding plays it safe, and stays flat.':
        "贪心解码求稳，也很平淡。",

    # ------------------------------------------------------------------ 10. Markov
    'Chapter ten. Markov chains.': '第10章。马尔可夫链。',
    'f"A Markov chain is randomness with a short memory':
        "马尔可夫链，是记性很短的随机：接下来发生什么，只取决于你现在在哪里。<bookmark mark='a'/>这一条是用第1部分的字母造出来的，只有三个状态：空格、元音、辅音。箭头上是接下来的概率：元音之后，有{100 * vc:.0f}%的时候是辅音。<bookmark mark='b'/>跟着一个行走者，数一数它在每个状态里待了多少时间。",
    'f"Keep going, and the shares settle':
        "继续走下去，比例就稳定了：{100 * pi3[0]:.0f}%是空格，{100 * pi3[1]:.0f}%是元音，{100 * pi3[2]:.0f}%是辅音，和书里一样。<bookmark mark='a'/>1913年，马尔可夫正是这样手工做的，用的是普希金的两万个字母。",
    'Follow the whole distribution instead of a single walker':
        "不跟单个行走者，而是跟踪整个分布，那么每走一步，就是乘一次那张概率表，也就是转移矩阵。<bookmark mark='a'/>走一步之后保持不变的那个分布，就是这条链的平稳分布。它是这个矩阵的一个特征向量，特征值为1，直接来自第3部分。",
    'f"Now all twenty-seven letters':
        "现在是全部27个字母，用第1部分的完整表格。从确定的状态出发：字母q。<bookmark mark='a'/>一步之后，几乎肯定是u。<bookmark mark='b'/>然后可能性逐渐散开，<bookmark mark='c'/>{k_forget}步之内，这条链就忘了自己从哪里出发：剩下的只是字母频率。<bookmark mark='d'/>它忘得有多快，由矩阵第二大的特征值决定，这里是{lam2:.2f}：每走一步，剩下的距离大约缩小到这个倍数。",
    'f"There is an easy way to know a distribution is stationary.':
        "有个简单的办法，判断一个分布是不是平稳的。<bookmark mark='a'/>假设在它之下，一步之内从i流向j的概率，和从j流向i的一样多：这叫细致平衡。<bookmark mark='b'/>对i求和，<bookmark mark='c'/>π乘以P就等于π：流量平衡，就什么都不变。<bookmark mark='d'/>这是充分条件，不是必要条件。英语就不平衡：{sx}之后接{sy}，比{sy}之后接{sx}常见{big:.0f}倍。<bookmark mark='e'/>{why_}但当我们在第13章构造用来采样的链时，细致平衡就是让它们落到目标分布上的办法。",
    'Words end in e far more often than they start with it.':
        "以e结尾的单词，远比以e开头的多。",
    'Its flows run more one way than the other.':
        "它的流量在一个方向上比另一个方向多。",
    'f"One minus the second eigenvalue is the spectral gap':
        "1减去第二个特征值，就是谱间隙；有瓶颈的链，谱间隙很小。<bookmark mark='a'/>这是41个格点上的游走，目标分布有两个势阱，中间隔着一道势垒，从最左端出发。<bookmark mark='b'/>左边的势阱几百步之内就填满了，<bookmark mark='c'/>但走了{ts[-1]:,}步之后，右边的势阱还在慢慢填。<bookmark mark='d'/>把势垒升高，谱间隙就缩小。以谱间隙的倒数为横轴，混合所需的步数沿着一条斜率为{float(d['slope']):.2f}的直线上升，从{int(tmix[0]):,}到{int(tmix[-1]):,}，落在理论给出的两个界之间。卡住的链，是第13章的核心难题。",

    # ------------------------------------------------------------------ 11. Monte Carlo
    'Chapter eleven. Monte Carlo.': '第11章。蒙特卡洛。',
    'The method was born at Los Alamos.':
        "这个方法诞生在洛斯阿拉莫斯。<bookmark mark='a'/>1946年，数学家斯坦尼斯瓦夫·乌拉姆在病后休养时，想知道单人纸牌有多大概率能玩通，他发现玩上一百局数一数，比去计算容易。<bookmark mark='b'/>约翰·冯·诺依曼把这个想法变成了追踪中子穿过炸弹核心的方法，<bookmark mark='c'/>1948年，克拉拉·冯·诺依曼和尼古拉斯·梅特罗波利斯在ENIAC上运行了它。梅特罗波利斯用那座赌场的名字给它命名。",
    "Here's a strange way to compute pi":
        "这是一种计算π的怪办法：完全随机地往一个正方形里扔飞镖。<bookmark mark='a'/>落在圆内的比例，就是圆占的面积比例，π除以4，所以这个比例的4倍就是π的估计。<bookmark mark='b'/>看着飞镖越积越多：它先是乱跳，然后逐渐逼近。",
    'f"After four thousand darts':
        "扔了4000支飞镖之后：{est[-1]:.3f}。<bookmark mark='a'/>阴影带表示这样一次实验通常会偏多远，它随飞镖数的平方根分之一而收窄。",
    'f"Repeat the experiment many times at each size':
        "在每个规模上把实验重复很多次，量出典型的误差。在对数刻度上，它落在一条斜率为{slope:.2f}的直线上。<bookmark mark='a'/>误差随样本数的平方根分之一缩小：每多一位精度，就要多一百倍的样本。<bookmark mark='b'/>这很慢，但这个速度与维度无关：在一百万维中也一样，而在那里任何网格都毫无希望。",
    'f"Monte Carlo has one weakness: rare events.':
        "蒙特卡洛有一个弱点：稀有事件。一个标准钟形分布落在4以上的概率有多大？精确地说，大约十万分之{true * 100000.0:.1f}。<bookmark mark='a'/>抽{n:,}个样本，只有{hits}个落在那里：偏差达{plain / true:.0f}倍。",
    'f"The fix is to cheat, and then correct for it.':
        "解决办法是先作弊，再纠正。<bookmark mark='a'/>从一个有一半时间落在那里的钟形分布中抽样。<bookmark mark='b'/>然后给每个样本加权：它在真实分布下比在你抽样的分布下可能多少倍。<bookmark mark='c'/>样本数相同，答案误差在{100 * abs(is_est / true - 1):.1f}%以内：这就是重要性采样。",
    'f"Importance sampling has a weakness of its own':
        "重要性采样也有自己的弱点：权重。<bookmark mark='a'/>数一数真正起作用的样本有多少，也就是有效样本量。<bookmark mark='b'/>目标是钟形分布，提议分布只宽{100 * (s - 1):.0f}%。在一维中，{n:,}个样本里有{m[0]:,.0f}个起作用；50维中，{m[i50]:.0f}个；200维中，测量值是{m[i200]:.0f}，而理论说连这都太乐观：{th[i200]:.3f}。少数几个样本承担了全部权重。<bookmark mark='c'/>这就是为什么强化学习要裁剪它的重要性比值，在第26部分。",

    # ------------------------------------------------------------------ 12. Score function
    'Chapter twelve. The gradient of an average.': '第12章。平均值的梯度。',
    'Much of machine learning ends with an average over random choices':
        "机器学习里的许多问题，最后都是对随机选择求平均：策略的期望奖励，采样出来的回答的期望得分。<bookmark mark='a'/>我们想要它的梯度，好改进模型。但被平均的那个东西可能根本没有斜率：一个时开时关的奖励，一个只说是或否的评判者。<bookmark mark='b'/>只有分布会随参数平滑地移动。怎样对采样求导？",
    'Move the gradient inside the integral':
        "把梯度移进积分里：只有密度依赖于θ。<bookmark mark='a'/>然后用对数导数技巧：p的梯度等于p乘以log p的梯度，<bookmark mark='b'/>于是梯度又成了一个平均：f乘以分数的平均，分数就是第4章里遇到的那个。采样，然后求平均；f本身从来不用求导。<bookmark mark='c'/>又因为分数的平均为零，从f里减去任何常数b都不改变答案：这就是基线。彼得·格林在1990年称之为似然比方法；罗纳德·威廉姆斯在1992年把它变成神经网络的学习规则，REINFORCE。",
    'f"The catch is noise.':
        "麻烦在于噪声。拿一个能核对的例子：对中心为1的钟形分布，求x平方的平均值的梯度；答案是2。<bookmark mark='a'/>这个估计量平均来说是对的，{n_:,}个样本上是{mean_sf:.3f}，但单个样本的估计方差是{v0:.0f}。<bookmark mark='b'/>基线能把它降下来：这里最好的基线，接近f的平均值，把方差降到{vstar:.0f}。<bookmark mark='c'/>当f确实有斜率时，还有更好的办法：把样本写成μ加噪声，然后穿过它求导，这就是重参数化技巧，方差是{vrep:.0f}。变分自编码器就是这样训练的，在第20部分；奖励和评判者则需要分数函数。",
    'f"The same estimator trains models with no gradient at all.':
        "同一个估计量，还能训练完全没有梯度的模型。给参数加上噪声来平滑f，它的梯度就是f在随机探测点上的值乘以探测方向的平均：这就是进化策略，2017年OpenAI的萨利曼斯和同事用它训练模拟机器人和玩Atari游戏的智能体。<bookmark mark='a'/>这里它沿一道弯曲的山谷下降，每步16个探测点。<bookmark mark='b'/>基线很重要：在起点测量，一次梯度估计的平方误差，没有基线时是{gp:.0f}，有基线时是{gb:.0f}，而梯度本身的大小只有{g2:.0f}。<bookmark mark='c'/>{verdict}强化学习的策略梯度，就是带基线的这个估计量，在第26部分。",
    "f'Without the baseline, {dp} of the 8 runs blow up and leave":
        "没有基线时，8次运行中有{dp}次发散，飞出了画面；有基线时，一次都没有。",
    "f'Without the baseline, {dp} of the 8 runs blow up; with it":
        "没有基线时，8次运行中有{dp}次发散；有基线时，只有{db}次。",
    "f'Here both reach the valley floor":
        "这里两者都到达了谷底：发散的，不加基线的有{dp}次，加基线的有{db}次。",

    # ------------------------------------------------------------------ 13. MCMC
    'Chapter thirteen. Markov chain Monte Carlo.': '第13章。马尔可夫链蒙特卡洛。',
    "Often there's no direct way to draw samples":
        "常常没有直接抽样的办法：我们能做的，只是计算每个点有多可能，而且只到一个未知常数为止，就像贝叶斯法则那样。<bookmark mark='a'/>这是一个有两个鼓包的密度。1953年，在洛斯阿拉莫斯，尼古拉斯·梅特罗波利斯、阿丽安娜和马歇尔·罗森布卢斯、奥古斯塔和爱德华·特勒，在MANIAC计算机上找到了从任何这类分布中采样的方法：随机游走。<bookmark mark='b'/>提出一个小的随机步子。往上坡走，就接受。<bookmark mark='c'/>往下坡走，就以两处高度之比为概率接受；否则原地不动。",
    'f"Only the ratio appears':
        "只出现比值，所以那个未知常数消掉了。<bookmark mark='a'/>继续走：到访的位置像密度一样堆积起来，因为这条马尔可夫链的平稳分布就是我们想要的那个。<bookmark mark='b'/>左边的鼓包占概率的三分之二，行走者有{100 * left:.0f}%的时间待在那里。它在1990年代让贝叶斯统计变得实用，物理学家至今仍这样对分子采样。",
    'Why does it work?':
        "为什么行得通？第10章的细致平衡。从x到y的一步，以概率q被提出，再以概率a被接受。<bookmark mark='a'/>平衡要求两个方向的流量相等，<bookmark mark='b'/>而这只确定了两个接受概率之比。<bookmark mark='c'/>让较大的那个等于1：这就是黑斯廷斯1970年给出的规则，适用于任何提议分布。<bookmark mark='d'/>提议对称时，q相互抵消，就是梅特罗波利斯的规则。",
    'f"There is another way to explore, from physics.':
        "还有一种探索方式，来自物理学。1908年，保罗·朗之万把流体中粒子的运动写成一股推力加上随机踢动。<bookmark mark='a'/>让推力等于分数，也就是log p的斜率，指向更可能的地方；让踢动是布朗运动；迈小步的话，就是一行代码。<bookmark mark='b'/>1500个粒子从噪声出发；它们上方，是它们的密度。<bookmark mark='c'/>密度流到两个鼓包上，与目标的距离从{l1[0]:.2f}降到{l1[-1]:.2f}，差不多是平滑所允许的最低值。{verdict}<bookmark mark='d'/>它的长期分布就是p本身，第17章会证明。用小批量估计分数，它在2011年被用来对神经网络的权重采样；用学出来的分数，它是最早的基于分数的图像模型的采样器。",
    "f'{100 * left:.0f} percent of the particles are in the left bump":
        "{100 * left:.0f}%的粒子在左边的鼓包里，接近它的三分之二。",
    "f'{100 * left:.0f} percent are in the left bump, short":
        "{100 * left:.0f}%在左边的鼓包里，不到它的三分之二：有些粒子还在山谷的另一边。",
    'f"How well do they mix?':
        "它们混合得怎么样？四个采样器，各跑两万步，重复五次，跟踪其中一个坐标。<bookmark mark='a'/>普通的梅特罗波利斯在两个鼓包之间来回大约{h['rwm0.7']:.0f}次，宽度也对。小步长的朗之万只穿越{h['ula0.05']:.0f}次。<bookmark mark='b'/>{v1}<bookmark mark='c'/>{v2}每个采样器都在拿精确换速度，而相距很远的两个鼓包会把它们全都难住；第21部分的出路，是先对一个模糊过的版本采样。",
    "f'The big-step Langevin hops between the bumps most":
        "大步长的朗之万在两个鼓包之间跳得最多，{h['ula0.3']:.0f}次，但它的宽度是{sp['ula0.3']:.2f}，而真实值是0.35：不加修正，大步子会把目标抹模糊。",
    "f'The big-step Langevin hops {h['ula0.3']:.0f} times and keeps":
        "大步长的朗之万跳了{h['ula0.3']:.0f}次，宽度保持在{sp['ula0.3']:.2f}。",
    "f'Adding the Metropolis correction removes the bias, {sp['mala0.3']:.2f}, but":
        "加上梅特罗波利斯修正，偏差就消失了，{sp['mala0.3']:.2f}，但它穿过山谷的提议大多被拒绝：只跳了{h['mala0.3']:.0f}次。",
    "f'Adding the Metropolis correction removes the bias, {sp['mala0.3']:.2f}, and":
        "加上梅特罗波利斯修正，偏差就消失了，{sp['mala0.3']:.2f}，并跳了{h['mala0.3']:.0f}次。",

    # ------------------------------------------------------------------ 14. Brownian
    'Chapter fourteen. Brownian motion.': '第14章。布朗运动。',
    'In 1827 the botanist Robert Brown':
        "1827年，植物学家罗伯特·布朗看到水中的花粉在不停地抖动，看不出任何原因。<bookmark mark='a'/>一个模型：随机地上下走的游走。8步。<bookmark mark='b'/>64步，每步更小。1024步。<bookmark mark='c'/>让每一步按步数的平方根分之一缩小，这样方差，也就是离起点的距离平方的平均，始终恰好是t，这些游走就收敛成一个随机对象：布朗运动。路易·巴舍利耶在1900年用它描述股价，诺伯特·维纳在1923年严格地构造了它。它处处连续，却又锯齿得处处没有斜率。",
    'f"Now draw sixty of them.':
        "现在画60条。<bookmark mark='a'/>在任何时刻，它们走到的位置服从一个钟形分布，中心为零，宽度是t的平方根。<bookmark mark='b'/>时间加倍，宽度大约变成1.4倍，而不是2倍：又是中心极限定理，因为位置是许多微小踢动之和。<bookmark mark='c'/>在两万条路径上，方差分别是{var[0]:.2f}、{var[1]:.2f}、{var[2]:.2f}和{var[3]:.2f}：就是t。",
    'In two dimensions, a cloud released at one point':
        "在二维中，从一点释放的一团粒子，散开成一个越来越宽的钟形。<bookmark mark='a'/>不跟踪粒子，而是跟踪密度，它服从一个完全没有随机性的方程：热方程。<bookmark mark='b'/>爱因斯坦在1905年得出了这一点，并用它论证分子是真实存在的；几年后，让·佩兰测量了这种抖动，数出了分子。",
    'f"Brownian paths have one more property':
        "布朗路径还有一个改变微积分的性质。把每一小步平方，再加起来。<bookmark mark='a'/>对光滑曲线，步子越小，这个和越趋于零。对布朗运动，它却沿着直线t稳步上升。<bookmark mark='b'/>每一步的平方，均值是Δt，<bookmark mark='c'/>方差是Δt平方的量级，<bookmark mark='d'/>所以总和的均值是t，而离散程度趋于零。在400条路径上：16步时是{qm[k[0]]:.2f}，上下浮动{qs[k[0]]:.2f}；1.6万步时是{qm[k[2]]:.3f}，上下浮动{qs[k[2]]:.3f}。与此同时，路径本身的长度却无限增长：已经是{tvm[k[2]]:.0f}。<bookmark mark='e'/>简写就是：dW的平方等于dt。这是保罗·莱维1940年的定理，也是下一章的规则。",

    # ------------------------------------------------------------------ 15. Itô
    "Chapter fifteen. Ito's lemma.": '第15章。伊藤引理。',
    'f"Ordinary calculus says the integral of W d W':
        "普通微积分说，W dW的积分是W平方的一半。对布朗运动，这取决于在每一小步的哪个位置取W的值。<bookmark mark='a'/>取左端点，也就是这一步之前的值。一点代数就把和拆成两部分。<bookmark mark='b'/>第一部分逐项相消，剩下W平方的一半。<bookmark mark='c'/>第二部分是平方步长之和的一半，第14章已经证明它等于t，而不是零。所以取左端点的积分，是W平方的一半减去二分之一。<bookmark mark='d'/>在{M:,}条路径上，随着步子变小，左端点的和向它收拢，{verdict}：两者的平均分别是{lm:.2f}和{sm:.2f}。取哪个点很重要，而对光滑曲线，这种事从不发生。",
    'and the midpoints give one half W squared exactly':
        "而取中点的和恰好给出W平方的一半",
    'and the midpoints approach one half W squared':
        "而取中点的和趋近W平方的一半",
    'f"The same thing changes the chain rule.':
        "同样的事改变了链式法则。把W的一个函数展开到二阶。<bookmark mark='a'/>在普通微积分里，平方项可以忽略。这里dW的平方等于dt，和我们保留的其他项一样大：<bookmark mark='b'/>链式法则多出一项，二分之一f的二阶导数乘dt。这就是伊藤引理，<bookmark mark='c'/>对任何漂移为μ、噪声为σ的过程，它的形式是这样的。<bookmark mark='d'/>在e的W次方上逐条路径地检验。有了这一项，差距随着步子变小而缩小，斜率是{sl:.2f}；没有它，差距停在大约{nr[-1]:.2f}。平均来说，时刻1的e的W次方是{em:.3f}，而不是1：正是e的平方根{eh:.3f}，和多出来的漂移预测的一样。",
    'This calculus has a dramatic history.':
        "这套微积分有一段充满戏剧性的历史。<bookmark mark='a'/>1940年，在法国军队服役的年轻数学家沃尔夫冈·德布林，给法国科学院寄去一个密封信封；他在那年6月去世，信封在2000年打开时，里面是同一个公式的一个版本。<bookmark mark='b'/>伊藤清在1944年发表了随机积分，1951年发表了这个公式。<bookmark mark='c'/>布莱克、斯科尔斯和默顿在1973年用它给期权定价；它也是第21部分让扩散模型运转的工具。<bookmark mark='d'/>取中点得到斯特拉托诺维奇积分，它保留普通的链式法则，却偷看了未来；左端点才是模拟真正能算出来的。",

    # ------------------------------------------------------------------ 16. SDE
    'Chapter sixteen. Stochastic differential equations.': '第16章。随机微分方程。',
    'Brownian motion is pure jiggle.':
        "布朗运动是纯粹的抖动。加上一股推力，就得到一个随机微分方程。在每一瞬间，x的变化等于一股推力，f(x)乘以dt，这里dt是极短的一小段时间，<bookmark mark='a'/>再加上一次随机踢动：g乘以dW，也就是这一小段时间里的那一小段布朗运动。<bookmark mark='b'/>要模拟它，就迈小步：先推，再踢，踢动的大小是步长的平方根。",
    'The simplest interesting one is a spring':
        "最简单又有意思的一个，是把粒子拉回零点的弹簧，再加上噪声。40个粒子从2.5出发。<bookmark mark='a'/>推力把它们拉回家，噪声让它们一直搅动，<bookmark mark='b'/>它们最终在零点附近稳定成一个钟形，宽度由两者之间的平衡决定。伦纳德·奥恩斯坦和乔治·乌伦贝克在1930年描述了它，它正是扩散模型的前向过程。",
    'f"How good is that simple scheme?':
        "这个简单的格式有多好？在精确答案已知的地方测试它：一个每一瞬间都按随机百分比增长的量，几何布朗运动，也就是股价的模型。<bookmark mark='a'/>用同样的随机踢动，粗步子偏离了精确路径，细步子则紧紧跟随。<bookmark mark='b'/>在{M:,}条路径上：{v}<bookmark mark='c'/>丸山仪四郎在1955年证明了这个格式收敛。扩散模型的采样器，本质上就是把这个格式倒过来运行，第21部分会花好几章讲怎样用更少的步子做得更好。",
    "f'The path-by-path error shrinks like the square root":
        "逐条路径的误差，随步长的平方根缩小，斜率{ss:.2f}：步长减半，误差只降低{100 * (1 - 2 ** (-ss)):.0f}%。平均值的误差则随步长本身缩小，斜率{ws:.2f}。",
    "f'The path-by-path error falls with slope":
        "逐条路径的误差以斜率{ss:.2f}下降，平均值的误差以斜率{ws:.2f}下降。",

    # ------------------------------------------------------------------ 17. Fokker-Planck
    'Chapter seventeen. The Fokker-Planck equation.': '第17章。福克-普朗克方程。',
    'Chapter fourteen found the heat equation':
        "第14章为纯噪声的粒子云找到了热方程。加上推力之后，一般的定律是这样的，从伊藤引理出发。<bookmark mark='a'/>取任意一个光滑的检验函数φ，作用在一个漂移为f、噪声为g的过程上。<bookmark mark='b'/>求平均：随机项的均值为零。<bookmark mark='c'/>把平均写成对密度p的积分。<bookmark mark='d'/>分部积分，把导数从φ挪到p上。<bookmark mark='e'/>既然这对每个φ都成立，被积函数就相等：这就是福克-普朗克方程，密度的一条确定性的定律。阿德里安·福克和马克斯·普朗克为分子写下了它；柯尔莫哥洛夫在1931年给出了一般的推导。",
    'Now the promise from chapter thirteen.':
        "现在兑现第13章的承诺。朗之万动力学的漂移是目标π的分数，噪声的方差是2。<bookmark mark='a'/>把它代入福克-普朗克方程。<bookmark mark='b'/>如果密度就是π，漂移项给出负的π的二阶导数，噪声项给出正的π的二阶导数，两者抵消：π保持不动。这就是为什么第13章的粒子会落到两个鼓包上，也是为什么只要知道分数，朗之万动力学就能对任何分布采样。",
    'f"Check it on the Ornstein-Uhlenbeck process.':
        "在奥恩斯坦-乌伦贝克过程上检验它。<bookmark mark='a'/>从有两个峰的数据出发，让每个点向零漂移并抖动。<bookmark mark='b'/>两万个粒子，和在网格上解出的方程，一起移动：直方图与解的差距不超过{max(d['hist_err']):.3f}，解与精确答案的差距不超过{max(d['fp_err']):.4f}。<bookmark mark='c'/>等得足够久，数据的痕迹就全部消失：只剩一个普通的标准钟形曲线。扩散模型对它的训练图像做的，正是这件事。",
    'Can the film run backwards':
        "这部影片能倒着放吗，从钟形曲线回到数据？1982年，布赖恩·安德森证明，时间反转之后，它是另一个随机微分方程，只多了一项：<bookmark mark='a'/>分数，也就是那一刻密度的对数的斜率，一支指向数据更可能之处的箭头。<bookmark mark='b'/>它指向上坡，朝着数据。",
    'Know the score at every noise level':
        "知道了每个噪声水平下的分数函数，也就是从数据滑向噪声这一路上的每一点，就能把噪声变成数据。<bookmark mark='a'/>它就是这一部分开头的那片箭头场。<bookmark mark='b'/>在那里，它是直接从那些字母精确算出来的。扩散模型则用一个网络，从数百万张图像中把它学出来，这是第21部分的内容。",

    # ------------------------------------------------------------------ Outro
    'f"Let\'s take stock.':
        "来盘点一下。许多独立的小块加起来，经过一次次卷积，就成了钟形曲线，差距像n的平方根分之一那样缩小。对钟形分布做条件化，得到的还是钟形分布。最大似然能达到费希尔的下界：对柯西分布，n乘以它的方差降到了{float(f['mle_nvar'][-1]):.2f}，下界是2。贝叶斯法则就是计数，先验就是正则化。最大熵给出指数族，softmax也在其中。霍夫丁的界要{need['hoeffding']}次抛掷，而{need['exact']}次就已足够，但它处处成立。采样把均匀随机数变成任何分布；解码在多样性和可预测性之间做交换。马尔可夫链按谱间隙的速度遗忘；蒙特卡洛的误差像根号n分之一那样下降，而重要性权重在高维中崩塌。梅特罗波利斯和朗之万能对只能计算的形状采样，而随机运动有它自己的微积分，它的密度服从福克和普朗克的定律。",
    'All of this comes back.':
        "这一切都会再回来。最大似然和费希尔信息，训练第6部分和第11部分的模型。贝叶斯、马尔可夫链和它们的采样器，在第7部分回来；集中不等式在第8部分变成泛化界。解码在第19部分得到扩展。分数函数梯度和重要性权重就是强化学习，在第26和第27部分。随机微分方程既描述第11部分里带噪声的训练，也描述第20和第21部分的生成。",
    'Here are six problems to try':
        "这里有六道习题，从卷积一直到奥恩斯坦-乌伦贝克过程的平稳钟形分布。在这里暂停，把它们做一做；完整的解答在本部分的笔记里。",
    'Next time, act two begins':
        "下一次，第二幕开始：从数据中学习。我们从经典方法讲起：最小二乘法和它的几何，它就是高斯噪声下的最大似然；逻辑回归；核方法和支持向量机；决策树和提升法。<bookmark mark='a'/>在深度学习之前，机器学习靠的就是它们，而在表格数据上，它们至今常常胜出。",
    "Blitzstein and Hwang's Introduction to Probability":
        "布利茨坦和黄的《概率导论》是很友好的入门书；麦凯的书里有讲蒙特卡洛方法最好的几章，莱文和佩雷斯的书则讲混合。感谢观看，第6部分见。",
}

PHRASES = {
    'space': '空格',
    'e': 'e',
    'inside': '之内',
    'outside': '之外',
    'top-k': 'top-k',
    'top-p': 'top-p',
    'min-p': 'min-p',
    'temperature alone': '只用温度',
}
