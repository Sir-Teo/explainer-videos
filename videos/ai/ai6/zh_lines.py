"""Chinese narration for ai6: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第6部分：经典机器学习'

CHAPTERS = {
    'Hook': '这一页是谁写的？',
    'LeastSquares': '1. 最小二乘法',
    'GaussMarkov': '2. 最佳线性无偏的直线',
    'Ridge': '3. 岭回归：收缩弱的方向',
    'Lasso': '4. 套索回归：软阈值与路径',
    'Logistic': '5. 逻辑回归',
    'Newton': '6. 牛顿法，以及跑掉的直线',
    'NaiveBayes': '7. 朴素贝叶斯：生成式还是判别式？',
    'LDA': '8. 费希尔的方向',
    'KNN': '9. 近邻，以及维数灾难',
    'Kernels': '10. 核函数：不抬升的抬升',
    'SVM': '11. 最宽的街道',
    'Trees': '12. 决策树：二十个问题',
    'Forests': '13. 装袋法与随机森林',
    'AdaBoost': '14. AdaBoost与指数损失',
    'GradientBoosting': '15. 二阶的梯度提升',
    'Metrics': '16. 诚实地记分',
    'Contest': '17. 比赛，以及两种文化',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    "Here's a page from a novel, a thousand words long":
        "这是一部小说里的一页，长1000个词，标点都去掉了。<bookmark mark='a'/>它是谁写的：简·奥斯汀，还是查尔斯·狄更斯？",

    'You might look for names or places.':
        "你也许会去找人名或地名。但在1964年，莫斯特勒与华莱士判定了《联邦党人文集》里那些有争议的篇章出自谁手，靠的是数小词，比如“upon”、“whilst”和“also”。<bookmark mark='a'/>所以，我们就用最常见的70个词在一页里出现得有多频繁，来描述这一页。<bookmark mark='b'/>这一页“the”用得很多，“not”用得很少，像狄更斯。奥斯汀用“not”、“very”和“be”，要多得多。",

    'f"Take just two of those numbers':
        "只取其中两个数：一页用“the”有多频繁，用“not”有多频繁，每一页就变成了一个点。<bookmark mark='a'/>这是来自5部小说的{n}页。两位作者大体上各占一边，但也有重叠。我们用其中{int((~test).sum())}页来训练，另外{int(test.sum())}页锁起来，留作测试。<bookmark mark='b'/>把两位作者区分开，是机器学习最古老的任务：分类。画一条直线？把它弄弯？问问邻居？提一连串问题？这一部分把这些办法都试一遍。",

    'The methods are older than the computers that run them.':
        "这些方法，比运行它们的计算机还要古老。1805年，勒让德用最小二乘法拟合轨道。<bookmark mark='a'/>1936年，罗纳德·费希尔找到了最能把几种鸢尾花分开的方向。<bookmark mark='b'/>1958年，弗兰克·罗森布拉特的感知机从例子中学会了一条直线，<bookmark mark='c'/>1967年，科弗和哈特证明了，简单地照抄最近的邻居能做得多好。<bookmark mark='d'/>然后是会提问的决策树，<bookmark mark='e'/>瓦普尼克的支持向量机，<bookmark mark='f'/>提升法，<bookmark mark='g'/>随机森林，以及维奥拉和琼斯实时找出人脸。<bookmark mark='h'/>接着是各种竞赛：Netflix的百万美元大奖，<bookmark mark='i'/>Kaggle，<bookmark mark='j'/>还有赢下其中许多场的XGBoost。<bookmark mark='k'/>而现在，是训练来一口气读懂整张表格的Transformer。",

    'This is Part 6 of AI, Built, and the start of act two':
        "这是《人工智能，从零搭建》的第6部分，也是第二幕“从数据中学习”的开始。<bookmark mark='a'/>这一部分讲：最小二乘法，以及它为什么是同类中最好的，岭回归和套索回归；逻辑回归、牛顿法和朴素贝叶斯；费希尔的方向和最近邻；核函数和支持向量机；决策树、森林和提升法；还有怎样诚实地记分。每种方法都只是几行numpy代码，每个数都是在这些书页上算出来的。",

    # ---------------------------------------------------------------- LeastSquares
    'Chapter one. Least squares.': '第1章。最小二乘法。',

    'The oldest method of all fits a line.':
        "最古老的方法，是拟合一条直线。这里有三个点。<bookmark mark='a'/>对任意一条直线，量一量每个点偏离它多远，竖直向上或向下量，再把每个偏差平方：名副其实，真的是一个正方形。<bookmark mark='b'/>最小二乘法挑出的，就是这些正方形总面积最小的那条直线。<bookmark mark='c'/>勒让德在1805年发表了它。而高斯早在4年前就用过它，用来预测失踪的小行星谷神星会在哪里重新出现。",

    "Why squares, and not the plain distances?":
        "为什么是平方，而不是直接用距离？高斯1809年的回答是：假设每个偏差都是钟形的随机噪声。<bookmark mark='a'/>数据出现的概率，是许多钟形曲线的乘积，每个点一个。<bookmark mark='b'/>取它的负对数，指数就变成了偏差平方之和。<bookmark mark='c'/>所以最可能的那条直线，恰好就是最小二乘的直线。平方，正是钟形噪声所要求的；下一章会说明，即使没有钟形，它也是最好的线性选择。",

    "There's a beautiful way to see the answer.":
        "有一种很美的方式来看这个答案。把三个高度写成三维空间里的一个点。<bookmark mark='a'/>每一条可能的直线都给出三个预测，所有这些预测合在一起，构成一个平面：也就是把一列1和一列x混合起来，所能到达的一切地方；那一列1让直线上下平移，那一列x让它倾斜。<bookmark mark='b'/>最好的直线，就是这个平面上离数据最近的那个点。从数据向平面作一条垂线。<bookmark mark='c'/>垂直，意味着剩下的那部分，与这两列都成直角：这些偏差里，已经没有直线还能修正的平移或倾斜了。把这一点写下来，就得到了正规方程，它直接给出最好的直线，根本不需要搜索。",

    'f"Here\'s least squares on real data.':
        "这是最小二乘法用在真实数据上。把第1部分那些书里的每个词都数一遍，再从最常见的往下排名。<bookmark mark='a'/>两条坐标轴都取对数刻度，最常见的1000个词，几乎恰好落在一条直线上。<bookmark mark='b'/>最小二乘的斜率是{beta[1]:.2f}：第r常见的词，出现的次数大约是第一名的r分之1。这就是齐普夫定律，而这条直线解释了{100 * z['r2']:.1f}%的变化：<bookmark mark='c'/>这些点围绕它们平均高度的所有散布里，这条直线解释了几乎全部，只剩下薄薄的一丝。",

    # ---------------------------------------------------------------- GaussMarkov
    'Chapter two. Why least squares is the best of its kind.': '第2章。为什么最小二乘法是同类中最好的。',

    "And if the noise isn't a bell?":
        "如果噪声不是钟形的呢？高斯在1821年给出了第二个答案，马尔可夫后来又重新发现了它：最小二乘仍然是最佳线性无偏估计。<bookmark mark='a'/>拿来任何另一个对数据是线性的估计：最小二乘，再加上某个矩阵D。<bookmark mark='b'/>要让它平均来说是对的，不管真实的直线是什么，D乘以A都必须为零。<bookmark mark='c'/>它的散布，是σ平方乘以这个矩阵，再乘以它的转置。<bookmark mark='d'/>展开：交叉项里含有D乘A，所以都消失了，剩下的是最小二乘的散布，加上D乘D转置。<bookmark mark='e'/>这一项只会增加。其他任何线性无偏估计，晃动得都更厉害。",

    'f"Let\'s check. Twelve points':
        "我们来验证一下。在同样的12个x上取12个点，每次都换上新的噪声。<bookmark mark='a'/>用最小二乘拟合它们，也用穿过两个端点的直线来拟合，后者同样是线性、无偏的。<bookmark mark='b'/>在{gm['R']:,}组数据上，两种斜率平均下来都等于真值，但最小二乘的方差是{G['ols']['var']:.4f}，和理论一致，而端点法的方差是它的{ratio:.1f}倍。",

    'f"Now step outside the rules.':
        "现在跳出规则之外。泰尔和森的估计，取所有两两之间斜率的中位数：它对数据不是线性的。<bookmark mark='a'/>在钟形噪声下，它输了，{ts_g:.4f}对{G['ols']['var']:.4f}。<bookmark mark='b'/>{verdict}",

    "f'With heavy-tailed noise of the same variance":
        "不过，换成方差相同、但尾巴很重的噪声，它就赢了：{ts_h:.4f}对{H['ols']['var']:.4f}。高斯–马尔可夫定理只保证，它在线性估计里是最好的。",

    'f"Even with heavy-tailed noise it doesn\'t win here':
        "即使换成重尾噪声，它在这里也没有赢：{ts_h:.4f}对{H['ols']['var']:.4f}。",

    'f"How should a computer solve it?':
        "计算机应该怎样求解？第3部分已经造好了工具。<bookmark mark='a'/>正规方程很快，<bookmark mark='b'/>但构造A转置乘A，会把条件数平方，而条件数每大10倍，就要损失一位有效数字。在这些书页上，问题还不大：{ls['kappa_A']:.1f}，平方后是{ls['kappa_AtA']:.0f}。<bookmark mark='c'/>QR分解求解同一个问题，却不用平方。<bookmark mark='d'/>而当有列重复的时候，伪逆会在所有最好的答案里，挑出最短的那个。",

    'f"Put the word \'not\' into the table twice.':
        "把“not”这个词放进表里两次。<bookmark mark='a'/>现在有两列完全相同，A转置乘A就不可逆了。{ne_say}<bookmark mark='b'/>伪逆则把“not”的权重恰好分成两半，{wa:.3f}和{wb:.3f}，给出的预测和之前一模一样。",

    "f'Solving the normal equations anyway":
        "硬去解正规方程，得到的权重大到10的{big}次方：那是被放大了的舍入误差。",

    "The normal equations can't be solved at all.": "正规方程根本解不出来。",

    # ---------------------------------------------------------------- Ridge
    'Chapter three. Ridge regression.': '第3章。岭回归。',

    'Seventy weights can lean on accidents':
        "70个权重，可能会去依赖训练页里的偶然巧合。岭回归给它们的大小定了个价：平方误差，加上λ乘以权重长度的平方。<bookmark mark='a'/>令梯度为零。在对角线上加上正的λ，这个矩阵就可逆了：1970年，霍尔和肯纳德就是这样挽救了几乎重复的列。<bookmark mark='b'/>现在用上第3部分的奇异值分解。<bookmark mark='c'/>拟合结果是数据中各个方向上的一个和：每个方向在目标里所占的份额，乘以一个因子，d平方除以d平方加λ。<bookmark mark='d'/>最小二乘把每个方向都完整保留。岭回归把每个方向都缩小，而奇异值小的那些弱方向，缩得最多。",

    'f"Here are the seventy directions':
        "这是训练页的70个方向，从最宽的到最窄的。<bookmark mark='a'/>下面是作者信息沿每个方向分布了多少：其中{100 * share:.0f}%落在前两个方向上。<bookmark mark='b'/>现在加大λ。等于1时，几乎什么都没缩小。等于30时，最窄的方向只保留{100 * f30:.0f}%。<bookmark mark='c'/>等于1000时，最宽的方向保留{100 * f1k_hi:.0f}%，最窄的只剩{100 * f1k_lo:.0f}%。这些因子的总和，数的是实际上还有多少个权重是自由的。",

    'f"Which lambda?':
        "λ取多少？留出一些书页，用其余的拟合，再在留出的那些上量误差；这样做10次，每次留出不同的十分之一：这就是10折交叉验证。<bookmark mark='a'/>误差在λ约为{lams[best]:.0f}时最低，相当于大约{df_best:.0f}个有效权重，而不是70个，{say}。<bookmark mark='b'/>这些书页很容易区分，所以惩罚项对准确率几乎没有影响；当词比书页还多时，它才要紧。岭回归保留每一个词，只是让它们变小。下一章的惩罚项，会把词扔掉。",

    'which costs nothing on the held-out pages': '而在留出的书页上，这毫无代价',

    "f'which costs a page or so on the held-out pages":
        "代价是在留出的书页上大约错一页：{100 * ta[best]:.1f}%对{100 * ta[0]:.1f}%",

    # ---------------------------------------------------------------- Lasso
    'Chapter four. The lasso.': '第4章。套索回归。',

    'A penalty is a budget.':
        "惩罚项就是一份预算。<bookmark mark='a'/>这里有两个权重，还有损失的等高线，损失的最低点在外面这里。<bookmark mark='b'/>岭回归给长度的平方定预算，是一个圆。蒂布希拉尼1996年提出的套索回归，也就是Lasso，给绝对值之和定预算：一个菱形。答案就在最低的那条等高线刚好碰到这个形状的地方。<bookmark mark='c'/>把预算缩小。圆给出的答案平滑地滑向零。菱形给出的答案却卡在一个角上，在那里，有一个权重恰好为零。",

    'How is it solved? One weight at a time.':
        "怎么求解？一次一个权重。<bookmark mark='a'/>把其他权重固定住，一个权重面对的，是一条抛物线，加上λ乘以它的绝对值。<bookmark mark='b'/>绝对值在零点有一个尖角，那里的斜率可以是负1到1之间的任何值。<bookmark mark='c'/>所以答案是软阈值：把最小二乘的值朝零移动λ，到零就停下。<bookmark mark='d'/>落在这条带子里的值，都恰好给出零。轮流访问每个词，逐个做阈值处理，直到什么都不再变化：这就是坐标下降，glmnet就是这样计算的。",

    'f"Here\'s the whole path on the pages':
        "这是书页上的整条路径：全部70个权重，用坐标下降在{n}个惩罚强度上算出，从最强一路放松到很弱。<bookmark mark='a'/>最先活过来的词是{names_say}。<bookmark mark='b'/>只用这{len(words8)}个词，分类器就能判对{100 * d['acc8']:.0f}%的留出书页。<bookmark mark='c'/>交叉验证在最好结果的一个标准误之内，挑出最稀疏的模型，保留了{d['n_selected']}个词，判对{100 * d['acc_one_se']:.1f}%。",

    'f"One weakness.':
        "它有一个弱点。给套索回归两个几乎一模一样的词：“not”，和它的一个带噪声的副本。<bookmark mark='a'/>当惩罚很强时，它只用其中一个孪生词，忽略另一个，这是一个任意的选择。<bookmark mark='b'/>邹和黑斯蒂在2005年提出的弹性网络，掺进一点岭回归，让两者分担权重：在同样的惩罚下，较小的那个孪生词承担了这一对权重的{100 * share_e:.0f}%。",

    # ---------------------------------------------------------------- Logistic
    'Chapter five. Logistic regression.': '第5章。逻辑回归。',

    'The simplest classifier draws a straight line.':
        "最简单的分类器，画的是一条直线。给每一页打一个分：它的两个词频的加权和，再加上一个常数。<bookmark mark='a'/>分数为正，就是狄更斯；为负，就是奥斯汀；而那条直线，就是分数恰好为零的地方。<bookmark mark='b'/>但分数不是概率。用S形函数把它压扁：很大的正分数变成1，很大的负分数变成0，而0变成二分之一。",

    'f"Over the whole plane, that makes a sheet':
        "在整个平面上，这就形成了一张曲面：狄更斯的概率，从奥斯汀那一侧，升到狄更斯那一侧。<bookmark mark='a'/>把每一个训练页，抬到它真实答案的高度：奥斯汀是0，狄更斯是1。这张曲面应该从它们近旁经过。<bookmark mark='b'/>拟合它，就是最小化平均意外度，也就是第1部分的交叉熵。最好的那张曲面，每页还剩{self.lg['loss_bits']:.2f}比特的意外度。",

    'f"Is there a single best sheet?':
        "最好的曲面只有一张吗？把损失写下来。<bookmark mark='a'/>S形函数的斜率，是它自己乘以1减它自己，所以<bookmark mark='b'/>梯度简单得漂亮：特征乘以“预测减真值”，和最小二乘一模一样。<bookmark mark='c'/>再求一次导：X转置S X，S里放的是每一页的p乘以1减p。<bookmark mark='d'/>在任何方向v上，这都是平方的加权和，永远不会是负的。这个损失是凸的：只有一只碗。<bookmark mark='e'/>在这些书页上，答案处的曲率在每个方向上都是正的{bowl}",

    ', so the bowl has one bottom.': '，所以这只碗只有一个谷底。',

    'f"Now the test: pages the method never saw.':
        "现在来测试：用这个方法从没见过的书页。只用两个词频，这条直线能判对其中的{100 * lg['acc2']:.0f}%。<bookmark mark='a'/>换成全部70个词频，同一个方法在{n_te}个测试页中判对了{round(lg['acc70'] * n_te)}个。一把小词，数一数，就是一枚指纹。",

    'f"So follow the slope downhill':
        "那就顺着坡往下走：梯度下降，和这个系列里每个模型都一样的做法。<bookmark mark='a'/>一开始每个权重都是0：对每一页都像抛硬币。每一步都沿着梯度的反方向推一下权重：<bookmark mark='b'/>这条线朝两位作者之间的空隙转过去，损失下降，大约到第{settle}步，它就稳定下来了。<bookmark mark='c'/>凸性排除了较差的局部最小值。这里的数据给出唯一的有限最佳拟合；步长选得稳定时，梯度下降从任意初始权重都会趋近它。",

    # ---------------------------------------------------------------- Newton
    "Chapter six. Newton's method.": '第6章。牛顿法。',

    'Gradient descent takes small steps.':
        "梯度下降走的是小步。牛顿法还用上了曲率：<bookmark mark='a'/>在你站的地方给损失拟合一条抛物线，然后直接跳到它的底部。<bookmark mark='b'/>用第5章的梯度和曲率，这一步就是X转置S X的逆，乘以X转置乘“y减p”。<bookmark mark='c'/>整理一下，每一步都是一个加权最小二乘问题，<bookmark mark='d'/>拟合的是一个“工作响应”。模型拿不准的书页，权重最大。<bookmark mark='e'/>1972年，内尔德和韦德伯恩把它变成了所有广义线性模型的引擎。",

    'f"Race them, from the same start.':
        "让它们从同一个起点赛跑。<bookmark mark='a'/>走了一步之后，牛顿法的直线已经接近答案；走了{settle}步，就到了。梯度下降走了同样多的步数，还在摆动着找位置。<bookmark mark='b'/>用全部70个词频时，最小化的是以纳特计的平均交叉熵，加上二分之一乘λ再乘权重范数的平方，其中λ等于{penalty:g}。图里的差距，是这个带惩罚目标减去它的最小值。牛顿法走{nn}步，就精确到最后一位；梯度下降要走{it6:,}步，才能差到百万分之一以内。接近谷底时，牛顿法每走一步，正确的位数就翻一倍。代价是：算上截距，每一步都要解一个{system_size}乘{system_size}的方程组，这就是为什么巨大的模型还是用梯度。",

    'f"Here\'s a trap.':
        "这里有个陷阱。用全部70个词频，有一条直线能把每一个训练页都完美分开。<bookmark mark='a'/>那样就不存在最好的直线了：把权重拉得更长，总能让概率更自信，让损失更小，一路逼近零。<bookmark mark='b'/>把惩罚减弱{pens[0] / pens[-1]:,.0f}倍，权重的长度就从{norms[0]:.1f}涨到{norms[-1]:.1f}，没有尽头。这又是一个保留一点惩罚的理由。<bookmark mark='c'/>换成不加惩罚的梯度下降，权重会永远增长下去，但它们的方向会慢慢稳定在间隔最宽的那条直线上：第11章的支持向量机。",

    'f"With all seventy rates, no line separates every training page':
        "用全部70个词频，没有哪条直线能把每个训练页都分开，所以最好的直线是存在的。<bookmark mark='a'/>惩罚项仍然在塑造它：<bookmark mark='b'/>把它减弱{pens[0] / pens[-1]:,.0f}倍，权重的长度从{norms[0]:.1f}涨到{norms[-1]:.1f}，然后稳定下来。<bookmark mark='c'/>在可分的数据上，它们会永远增长下去。",

    # ---------------------------------------------------------------- NaiveBayes
    'Chapter seven. Naive Bayes.': '第7章。朴素贝叶斯。',

    'Logistic regression models the answer directly.':
        "逻辑回归直接给答案建模。朴素贝叶斯给写作建模。<bookmark mark='a'/>假装每位作者写作时，都是一个个独立地抽词，狄更斯按概率θ D来抽。贝叶斯法则把它反转过来。<bookmark mark='b'/>取几率的对数。<bookmark mark='c'/>它是词数的加权和，再加一个常数：一条直线，和逻辑回归同属一族，只是权重是数出来的，不是拟合出来的。<bookmark mark='d'/>每个计数都加1，这是第1部分拉普拉斯的法则，这样就没有哪个词是不可能的。<bookmark mark='e'/>两种哲学：生成式模型描述数据是怎样产生的；判别式模型只描述那个决定。",

    'f"Which is better?':
        "哪个更好？吴恩达和乔丹的回答是：看你有多少数据。在随机挑选的书页上训练两者，从4页一直到全部，反复很多次，再在留出的书页上测试。<bookmark mark='a'/>{say}",

    'f"With a handful of pages, naive Bayes is ahead':
        "只有寥寥几页时，朴素贝叶斯领先：在{max(better)}个训练页以内，它的错误率更低。<bookmark mark='b'/>从{cross}页起，逻辑回归超过了它，而且一直在进步：用全部{sizes[-1]}页，它错{100 * lr_end:.1f}%，朴素贝叶斯错{100 * nb_end:.1f}%。这正是吴恩达和乔丹在2002年预言的交叉：生成式模型很快就达到它最好的水平，但它最好的水平更差，因为它的假设是错的。",

    'f"Here the expected crossover':
        "在这里，预期的交叉并没有清楚地出现。<bookmark mark='b'/>用全部{sizes[-1]}页，逻辑回归错{100 * lr_end:.1f}%，朴素贝叶斯错{100 * nb_end:.1f}%。",

}

ZH.update({
    'f"There\'s a second difference.':
        "还有第二个区别。当一个模型说70%的时候，它真的有70%的时候是对的吗？按给出的概率把书页分组，画出它们实际上是狄更斯的频率。诚实的概率，落在对角线上。<bookmark mark='a'/>逻辑回归的概率很接近：平均误差{e_lr:.3f}。<bookmark mark='b'/>朴素贝叶斯把每个词都当作独立的证据，所以它自信得离谱：{100 * ext:.0f}%的书页，得到的几率超过一百万比一。<bookmark mark='c'/>普拉特1999年的修正办法，是在训练页上，给它的分数拟合一个只有一个变量的逻辑回归，{end}",
    "f'and the error falls from": "误差从{e_nb:.3f}降到了{e_pl:.3f}。",
    'f"though here the error doesn\'t fall': "不过在这里，误差没有下降：{e_nb:.3f}到{e_pl:.3f}。",
})

ZH.update({
    # ---------------------------------------------------------------- LDA
    "Chapter eight. Fisher's discriminant.": '第8章。费希尔判别。',

    'In 1936, Ronald Fisher, separating species of iris':
        "1936年，罗纳德·费希尔在按花瓣的大小区分几种鸢尾花时，问了一个不同的问题：沿着哪个方向看，这两组的差别最大？<bookmark mark='a'/>选一个方向，把每一页都压到它上面。每位作者就变成了一堆。<bookmark mark='b'/>转动这个方向，两堆就会彼此靠拢，或者分开。费希尔的得分，是两堆中心之间的差距的平方，除以它们散开的程度。",

    'f"The best direction has a formula':
        "最好的方向有一个公式：两个中心之差，再用两位作者内部合并散布的逆来校正。<bookmark mark='w'/>这个校正的意思是：把空间拉伸，直到合并的作者内部散布变成圆的，再从一个中心指向另一个中心。<bookmark mark='a'/>在这里，它主要依靠“not”。<bookmark mark='b'/>在两堆的正中间切一刀，就得到一个分类器。它能判对{100 * acc:.0f}%的测试页{like_lr}<bookmark mark='c'/>当每一组都是形状相同的钟形分布时，这一刀，再按两位作者书页数量的不同稍作挪动，就是可能的最好切法。",

    ', the same as logistic regression.': '，和逻辑回归一样。',

    'f"Where does the formula come from?':
        "这个公式从哪里来？<bookmark mark='a'/>费希尔的得分，是两个二次型之比：作者之间的散布，除以作者内部的散布。<bookmark mark='b'/>令它的梯度为零，就得到一个广义特征值问题：S B乘w，等于J乘S W乘w。<bookmark mark='c'/>但S B的秩是1：它永远只指向两个均值之差的方向。<bookmark mark='d'/>所以答案是S W的逆，乘以这个差。<bookmark mark='e'/>在全部70个词频上，特征值求解器只找到一个非零特征值，它的特征向量与公式的吻合程度是{ld['cos_eig']:.6f}。{also}<bookmark mark='f'/>它最依赖{names}，留出的书页判对{100 * ld['acc70']:.0f}%。",

    'It also agrees with least squares on a zero-one target':
        '它也和以0、1为目标的最小二乘一致：只有两类时，两者是同一条直线。',
    'And least squares on a zero-one target points the same way.': '以0、1为目标的最小二乘也指向同一个方向。',

    # ---------------------------------------------------------------- KNN
    'Chapter nine. Nearest neighbours.': '第9章。最近邻。',

    'f"Here\'s a method with no line at all':
        "这个方法根本不用直线，菲克斯和霍奇斯在1951年写下了它。要给一页分类，就找出和它最像的那些训练页，也就是它的最近邻，让它们投票。<bookmark mark='a'/>从测试集里拿出这一页。<bookmark mark='b'/>它的15个最近邻：{15 - nd}个是奥斯汀的，{nd}个是狄更斯的。<bookmark mark='c'/>多数说了算。这里根本没有训练：模型就是数据本身。",

    'f"Colour every point of the plane':
        "按照邻居们会怎样投票，给平面上的每个点涂上颜色，就能看到这个方法的全部答案。<bookmark mark='a'/>只问1个邻居，区域就成了一块参差不齐的拼布，照抄训练页：训练页判对{100 * t1:.0f}%，新的书页却只有{100 * a1:.0f}%。<bookmark mark='b'/>邻居多了，就把它抹平。<bookmark mark='c'/>在留出的书页上，k等于{best_te}时最好，{100 * acc_b:.0f}%。{say_cv}",

    "f'Cross-validation, which never looks at the held-out pages":
        "交叉验证从不看留出的书页，它挑出的是同一个k。",

    'f"Cross-validation, which never looks at them':
        "交叉验证从不看它们，它挑出k等于{kcv}，在留出的书页上判对{100 * k_['acc_kcv']:.0f}%：留出书页上最好的那个k，有一部分是运气。",

    'f"How good can copying a neighbour be?':
        "照抄邻居能做得多好？科弗和哈特在1967年给出了答案。<bookmark mark='a'/>设η(x)是位于x的一页出自狄更斯的概率。最近邻的标签，是一枚独立的硬币，有它自己的η，所以出错就是两者不一致。<bookmark mark='b'/>数据足够多时，邻居就落在x上，错误率变成2乘η乘1减η。<bookmark mark='c'/>这至少是η和1减η中较小的那个，也就是任何规则在那里能做到的最好结果，<bookmark mark='d'/>而由詹森不等式，平均起来至多是最小可能错误率的两倍。<bookmark mark='e'/>在两个相互重叠的钟形分布上验证一下，那里最小可能的错误率是{100 * Rs:.1f}%。用{ns[-1]:,}个点，单个最近邻的错误率是{100 * e1n:.1f}%，接近它的极限{100 * lim:.1f}%，在上界{100 * bnd:.1f}%之内。让k随n一起增长，错误率就朝最好的结果降下去：{100 * ekn:.1f}%。",

    'f"There\'s a catch, and Richard Bellman named it':
        "这里有个陷阱，理查德·贝尔曼给它起了名字：维数灾难。<bookmark mark='a'/>在很多维里，一切都离一切很远，而且一样远。在一个立方体里撒点：在1维里，最近的点只是平均距离的一个零头；在1000维里，它是平均距离的{100 * nnf[-1]:.0f}%。<bookmark mark='b'/>要装下十分之一的数据，10维立方体的边长得有{float(ed['10']):.2f}：这样的邻域，已经不再是局部的了。<bookmark mark='c'/>在书页上，加上几列纯粹的噪声。最近邻从{100 * kn0:.0f}%跌到{100 * kn1:.0f}%，因为每一列噪声，都和一个真正的词一样算数。逻辑回归学会了忽略它们，只从{100 * lr0:.0f}%降到{100 * lr1:.0f}%。",

    # ---------------------------------------------------------------- Kernels
    'Chapter ten. Kernels.': '第10章。核函数。',

    'f"In 1958 Frank Rosenblatt\'s perceptron':
        "1958年，弗兰克·罗森布拉特的感知机从例子中学会了一条直线：每当它把一页分错，就把这一页加到权重上。<bookmark mark='a'/>如果有某条直线能带着一定的间隔把数据分开，诺维科夫证明了，它至多犯R除以γ的平方次错，就会停下。<bookmark mark='b'/>但有些模式根本没有这样的直线。异或：<bookmark mark='c'/>感知机永远停不下来，一百轮里犯了{k['xor_mistakes_100']}次错。明斯基和佩珀特1969年的书，让这类局限广为人知，也促成了神经网络的一个寒冬。<bookmark mark='d'/>有两条出路。学出新的特征，那是第9部分的故事。或者手工加上特征：给每个点添第三个数，x1乘x2，感知机犯了{k['xor_lift_mistakes']}次错之后，就把异或分开了。",

    "Here's the same idea with circles.":
        "同样的想法，用在圆上。没有哪条直线能把里面的点和外面的一圈分开。<bookmark mark='a'/>把每个点抬起来，高度等于它到中心距离的平方。<bookmark mark='b'/>现在，一个平面就能把它们分开：这个平面，是下一章的支持向量机在抬升后的点上找到的。<bookmark mark='c'/>从正上方看，这个平面切出的是一个圆：抬升空间里的一条直线，在原来的空间里是一条曲线。",

    'f"The lift can be expensive':
        "抬升可能代价很大：每个点的数一多，抬升后的特征就成倍增长。核技巧避开了它。<bookmark mark='a'/>取平面上一个点的这6个特征。<bookmark mark='b'/>它们的点积，展开以后，<bookmark mark='c'/>就是x点乘z加1，再平方：只用原来的两个数就算出来了，从来不用那6个。任何只需要点积的方法，比如支持向量机，都能免费地在抬升后的空间里运行。<bookmark mark='d'/>高斯核走得更远。把它展开，它的特征是坐标的每一个幂：无穷多个。只保留{len(errs)}个，它们就已经和高斯核相差在{within}以内了。",

    'f"Which similarity scores are allowed?':
        "哪些相似度是允许的？对于实值对称的相似度函数，存在特征空间中的点积表示，当且仅当每个格拉姆矩阵都是半正定的，也就是没有负的特征值。<bookmark mark='a'/>在{n}个训练页上，高斯核最小的特征值是{smallest}<bookmark mark='b'/>一个流行的冒牌货，点积的双曲正切，有{k['n_neg_sig']}个负特征值：没有任何特征能产生它，用它搭起来的支持向量机，解的也不再是一个凸问题。",



    'f"One more guarantee makes kernels practical.':
        "还有一个保证，让核方法变得实用。<bookmark mark='a'/>用任意的损失拟合任意一个函数，再加上对它大小平方的正惩罚。<bookmark mark='b'/>把这个函数分成两部分：一部分由训练点上的核函数组成，另一部分和它们全都垂直。<bookmark mark='c'/>在训练点上，垂直的那部分是看不见的：它不改变任何预测。<bookmark mark='d'/>它只会增加大小。所以它必须是零，答案就是训练点上核函数的加权和：这就是表示定理。<bookmark mark='e'/>验证一下：在{k['rep_dims']:,}个显式的随机特征上，对书页做岭回归，答案恰好落在书页自身特征张成的空间里，精确到最后一位。",

    # ---------------------------------------------------------------- SVM
    'Chapter eleven. Support vector machines.': '第11章。支持向量机。',

    'f"Many lines separate these two groups.':
        "能把这两组分开的直线有很多。瓦普尼克的问题是：哪一条最好？<bookmark mark='a'/>他的答案是：两侧空出的街道最宽的那一条。<bookmark mark='b'/>一个点到直线的距离，是它的得分除以w的长度。<bookmark mark='c'/>把w缩放到最近的点得分恰好为1；<bookmark mark='d'/>那么街道的宽度就是2除以w的长度，<bookmark mark='e'/>而最宽的街道，就是能让每个点都留在自己一侧的、最短的w。<bookmark mark='f'/>街道的两条边，只靠在{len(sv)}个点上，这些点就是支持向量。移动其他任何一个点，什么都不会改变。",

    'Real authors overlap, so no street is empty.':
        "真实的作者是重叠的，所以没有哪条街道是空的。1995年，科尔特斯与瓦普尼克允许点站到街道里，甚至站到错误的一侧，但要付出代价。<bookmark mark='a'/>这个代价就是铰链损失：安全地站在自己一侧的页，代价是零；一旦越界，代价就沿直线增长。<bookmark mark='b'/>把它和“对还是错”比一比，后者没法优化；再和逻辑回归的损失比一比：两者都是凸的，都是数错误次数的平滑替身。<bookmark mark='c'/>常数C设定这个代价：C大，街道窄，为每一页都去争；C小，街道宽，比较宽容。",

    'This is a constrained problem':
        "这是一个有约束的问题，第4部分的拉格朗日乘子能把它里外翻转。<bookmark mark='a'/>给每一页的约束配一个乘子α。<bookmark mark='b'/>令各个导数为零，就得出：权重是训练页本身的一个组合，而每个α都在0和C之间。<bookmark mark='c'/>代回去，问题就只和α有关，而书页只通过点积出现：换上一个核函数，街道就变弯了。<bookmark mark='d'/>KKT条件完成最后一步：每一页只要安全地离开街道，它的α就是零。只有支持向量才算数。<bookmark mark='e'/>普拉特的SMO一次解两个α，我们要运行的就是它。",

    'f"Now the pages, with a Gaussian kernel, solved by SMO.':
        "现在回到书页上，用高斯核，由SMO求解。<bookmark mark='a'/>C等于{Cs[0]:g}时，站在街道里很便宜：{s['n_train']}页里有{c0['n_sv']}页是支持向量，边界几乎不弯。<bookmark mark='b'/>加大C，街道就变窄：C等于{Cs[-1]:g}时，有{cb['n_sv']}个支持向量，边界绕着书页弯曲。每一个解都经过数值检验：屏幕上的原对偶相对间隙显示了近似程度。在C等于1时，按千分之一的容差检查，有{kk['outside'] + kk['bound_out']}个街道外或上界点未通过间隔检查；自由支持向量的最大间隔残差另行显示。<bookmark mark='c'/>10折交叉验证选出C等于{cvC:g}、核宽度{cvg:g}，判对{100 * s['acc_cv2']:.0f}%的留出书页；用全部70个词频，是{100 * s['acc70_rbf']:.1f}%。<bookmark mark='d'/>从1995年直到2012年前后深度网络接手，它一直是要打败的那个方法。",

    # ---------------------------------------------------------------- Trees
    'Chapter twelve. Decision trees.': '第12章。决策树。',

    'f"A decision tree plays twenty questions.':
        "决策树玩的是“二十个问题”的游戏。它学到的第一个问题是：这一页每1000个词里，“not”是否至多出现{root['t']:g}次？<bookmark mark='a'/>每个回答都把书页分成两组，每一组再有自己的下一个问题。<bookmark mark='b'/>每个问题，都用一条平行于坐标轴的直线切开平面，于是平面变成了一个个方格，每个方格按其中的多数来投票。",

    'f"Keep asking questions':
        "不停地问下去，这些方格就把训练页拟合得越来越好。<bookmark mark='a'/>但新的书页讲的是另一回事。深度为{best}时，它们的成绩最好，判对{100 * te_acc[best - 1]:.0f}%。<bookmark mark='b'/>让树一直长到底，它对自己的训练页能判对{100 * t['train_deep2']:.0f}%，对新的书页却只有{100 * t['acc_deep2']:.0f}%。<bookmark mark='c'/>在训练页上做交叉验证，不偷看，选出的深度是{cvd}。1984年，布雷曼、弗里德曼、奥尔申和斯通的CART，就是这样先把树长深，再剪回来。",

    '"How does the tree choose its question?':
        "树是怎样选问题的？它衡量每个方格有多混杂。<bookmark mark='a'/>三种不纯度：基尼不纯度，第1部分的熵，还有朴素的错误率。<bookmark mark='b'/>一个问题的增益，是父节点的不纯度，减去子节点按大小加权的不纯度。<bookmark mark='c'/>父节点里狄更斯的比例，是子节点比例的平均，<bookmark mark='d'/>所以只要不纯度曲线严格向下弯，詹森不等式就保证：只要子节点之间有差别，增益就是正的。错误率只是一顶帐篷，两侧都是直的：一个让两个子节点都更纯的分割，按它算可能毫无增益。<bookmark mark='e'/>扫过每一个阈值。{say}",

    'f"On the pages, all three agree on the first question':
        "在书页上，三种度量对第一个问题的意见一致：“not”每千词至多出现{best['gini']:g}次。",

    'f"On the pages, Gini picks':
        "在书页上，基尼不纯度选“not”至多{best['gini']:g}次；熵选{best['entropy']:g}；错误率选{best['error']:g}。",

    # ---------------------------------------------------------------- Forests
    'Chapter thirteen. Bagging and random forests.': '第13章。装袋法与随机森林。',

    'f"Why does averaging trees help?':
        "为什么把树平均起来有用？写出B棵树平均值的方差，每棵树的方差是σ平方，每两棵之间的相关系数是ρ。<bookmark mark='a'/>它是所有成对协方差之和：<bookmark mark='b'/>B个方差，加上B乘以B减1个协方差。<bookmark mark='c'/>于是：ρ乘σ平方，加上其余部分除以B。树越多，第二部分越小，但第一部分永远去不掉：相关性定下了一个下限。<bookmark mark='d'/>用模拟来验证：ρ等于二分之一时，{Bs[-1]:.0f}个副本的平均，保留了{rr[-1]:.3f}的方差，公式给出的是{0.5 + 0.5 / Bs[-1]:.3f}。",

    'f"On the pages, the trees\' correlation':
        "在书页上，树之间的相关性，来自共用同样的训练页。抽出{b['Rs']}个训练集，每个{b['m']}页，在每个训练集的重抽样上种{b['T']}棵树，再在留出的书页上测量σ平方和ρ。<bookmark mark='a'/>装袋得到的树，也就是布雷曼1996年的配方，是相关的：ρ是{bag['rho']:.3f}，这个下限挡住了平均的效果。<bookmark mark='b'/>布雷曼2001年的新招，是每问一个问题，只让它从随机挑出的几个词里选。{mid}<bookmark mark='c'/>{fit}",

    "f'The trees disagree more":
        "树之间的分歧变大了：用8个词时，ρ降到{rf8['rho']:.3f}，下限几乎消失，尽管每棵树自己更不稳定，σ平方是{rf8['s2']:.3f}，而装袋时是{bag['s2']:.3f}。",
    'f"Here rho doesn\'t fall': "在这里，ρ没有下降：用8个词时是{rf8['rho']:.3f}。",
    'f"The measured variances sit on the formula\'s curves':
        "测得的方差都落在公式的曲线上，处处相差不超过{100 * dev:.0f}%。",
    'f"The measured variances follow the formula\'s curves loosely':
        "测得的方差只是大致跟着公式的曲线走：最大的差距是{100 * dev:.0f}%，因为只有{b['Rs']}个训练集。",

    'f"Grow a forest of {n} on all the training pages.':
        "在全部训练页上种一片{n}棵树的森林。<bookmark mark='a'/>一棵长满的树，判对{100 * b['one_tree']:.0f}%的留出书页。<bookmark mark='b'/>森林升到{100 * fa[-1]:.1f}%：{n_te}页里判对{round(fa[-1] * n_te)}页。<bookmark mark='c'/>而且它能免费给自己打分：每个训练页，对那些重抽样时没抽到它的树来说，就是一个测试页。这个袋外估计给出的是{100 * fo[-1]:.0f}%，完全没有碰留出的书页。",

    # ---------------------------------------------------------------- AdaBoost
    'Chapter fourteen. Boosting.': '第14章。提升法。',

    'f"Boosting asks a different question':
        "提升法问的是另一个问题：许多弱规则，能不能组成一个强规则？1997年，弗罗因德和沙皮尔的AdaBoost回答：能。<bookmark mark='a'/>开始时，每个训练页的权重都一样，找出最好的单个问题，也就是一个树桩。它在{100 * e1:.0f}%的权重上判错了。<bookmark mark='b'/>现在把它判错的书页加重，再为重新加权后的书页找最好的树桩。<bookmark mark='c'/>重复下去。权重越来越集中在难判的书页上，也就是两位作者的交界处，而委员会的投票，每个树桩按它的α加权，把平面切分开来。",

    'Why those weights, and that alpha?':
        "为什么是这样的权重，这样的α？2000年，弗里德曼、黑斯蒂和蒂布希拉尼找到了答案。<bookmark mark='a'/>AdaBoost是在贪心地最小化指数损失：e的负间隔次方。再加一个树桩，乘以α。<bookmark mark='b'/>把指数拆开，旧委员会的那一部分，恰好就是每一页的权重。<bookmark mark='c'/>树桩判对的书页贡献e的负α次方，判错的贡献e的α次方。<bookmark mark='d'/>令导数为零，α就是“判对的几率”取对数的一半。<bookmark mark='e'/>在这里，数值搜索α与公式结果的差异只有百万分之几。",

    'f"On all seventy rates, run four hundred rounds.':
        "在全部70个词频上，跑400轮。<bookmark mark='a'/>指数损失稳步下降。<bookmark mark='b'/>它总是在训练错误率的上方，因为只要判错，e的负间隔次方就至少是1。<bookmark mark='c'/>{say}",

    "f'The training error hits zero at round {z0}, with":
        "训练错误率在第{z0}轮降到了零，此时留出错误率是{100 * te_z:.1f}%。观察到的最低留出错误率是第{best}轮的{100 * te.min():.1f}%；跑完{n}轮后的最终值是{100 * te[-1]:.1f}%。即使每个训练页都判对了，指数损失仍然可以继续作用于间隔，沙皮尔和同事们在1998年研究了这种联系。",

    'f"The training error hits zero at round {z0}, and':
        "训练错误率在第{z0}轮降到了零，留出书页上的错误率是{100 * te_z:.1f}%；再多跑几轮，也没有改善。",

    "Boosting's most famous success came in 2001.":
        "提升法最著名的成功，出现在2001年。保罗·维奥拉和迈克尔·琼斯在视频里实时找出人脸，用的是一台普通的700兆赫个人电脑。<bookmark mark='a'/>每一条弱规则，都是作用在一个矩形特征上的树桩：一条亮带的亮度减去旁边那条，就像较亮的额头下面颜色较深的眼睛。<bookmark mark='b'/>AdaBoost在超过16万个特征里，挑出了最好的几个。<bookmark mark='c'/>他们还把这些委员会串成一条级联：一个很小的委员会先一下子扔掉大部分窗口，只有难判的才会送到大的委员会那里。此后多年，相机都是这样找人脸的。",

    # ---------------------------------------------------------------- GradientBoosting
    'Chapter fifteen. Gradient boosting.': '第15章。梯度提升。',

    'Friedman saw, in 2001, that boosting is gradient descent':
        "2001年，弗里德曼看出，提升法就是在函数空间里做梯度下降：每一棵新树，都是沿着损失往下走的一小步。2016年，XGBoost把这一步推到了二阶。<bookmark mark='a'/>在当前模型附近展开损失：每一页贡献它的梯度g，也就是预测减真值，和它的曲率h，也就是p乘以1减p，再加上对叶子数量和叶子权重的惩罚。<bookmark mark='b'/>一棵树给同一片叶子里的每一页同样的权重，所以这些求和可以按叶子归拢。<bookmark mark='c'/>每片叶子都是关于它权重的一条抛物线：最好的权重是负的G除以H加λ，正是一步牛顿法。<bookmark mark='d'/>而一次分割的增益，就是一片叶子变成两片时，这些抛物线的谷底下降了多少。",

    'f"Check the formula on the pages.':
        "在书页上验证这个公式。第一轮里，每一页的概率都是二分之一。最好的第一个问题是：这一页用“{w}”是否至多{x['check_thr']:g}次？<bookmark mark='a'/>把两侧的梯度和曲率分别加起来。<bookmark mark='b'/>增益公式给出{gain:.3f}；把二阶目标逐片叶子算出来，得到{agree_s}<bookmark mark='c'/>损失真正下降了{true:.1f}：{under_s}",

    'the same, to every digit shown.': '同样的结果，显示的每一位都一样。',
    'the second-order picture is a cautious approximation here': '二阶的图景在这里是一个保守的近似，真实的损失降得更多。',
    'the second-order picture slightly overestimates it.': '二阶的图景略有高估。',

    'f"Watch it learn on the two plotted rates.':
        "看它在图上这两个词频上学习。<bookmark mark='a'/>一棵树：几个方格。<bookmark mark='b'/>10棵，30棵：在两位作者交界的地方，边界越来越清晰。<bookmark mark='c'/>训练损失一直在下降，但留出的书页在第{best}轮之后最好，判对{100 * acc[best - 1]:.1f}%。<bookmark mark='d'/>{end}",

    'f"By round {n} they\'ve slipped':
        "到第{n}轮，已经滑落到{100 * acc[-1]:.1f}%：每页只有两个数，多出来的细节拟合的是训练页，而不是作者。及早停下，本身就是这个方法的一部分。",
    'After that they stay there.': '之后一直保持在那里。',

    'f"On all seventy rates, compare the two kinds of step':
        "在全部70个词频上，用同样的树、同样的学习率，比较这两种步子。<bookmark mark='a'/>{first}<bookmark mark='b'/>在留出的书页上，二阶提升达到{100 * a2[-1]:.1f}%，一阶的是{100 * a1[-1]:.1f}%。",

    "f'The Newton leaves drive the training loss down much faster":
        "牛顿式的叶子让训练损失下降得快得多：{n}轮之后是每页{s2[-1]:.4f}比特，而普通梯度是{s1[-1]:.4f}比特。",
    "f'Here the plain gradient keeps up": "在这里，普通梯度跟得上：{s1[-1]:.4f}比特对{s2[-1]:.4f}比特。",

    # ---------------------------------------------------------------- Metrics
    'Chapter sixteen. Keeping score.': '第16章。记分。',

    'f"A classifier gives a score; we chose to cut at a half.':
        "分类器给出一个分数；我们选择在二分之一处切开。每一种切法，都是一种取舍。<bookmark mark='a'/>从最严格开始，什么都不叫作狄更斯。降低阈值：你找到了更多狄更斯的书页，也就是命中，但也开始把奥斯汀的书页叫作狄更斯，也就是误报。<bookmark mark='b'/>描出来的这条路径，就是ROC曲线，它来自第二次世界大战中的雷达操作员。<bookmark mark='c'/>它的面积有一个很美的含义：随机挑一页狄更斯和一页奥斯汀，狄更斯那页得分更高的概率。把全部{P * N:,}对数一遍：{mw:.4f}，恰好就是这个面积。",

    'f"Now make Dickens rare':
        "现在让狄更斯变得稀少，就像欺诈或疾病通常那样。保留奥斯汀的全部书页，狄更斯的只留{rr['n_dickens']}页。<bookmark mark='a'/>一条永远说“奥斯汀”的规则，现在准确率是{100 * rr['always_austen']:.0f}%，却毫无用处。<bookmark mark='b'/>ROC曲线几乎察觉不到：它的面积仍然大约是{rr['auc']:.2f}，因为它分别衡量每位作者的书页。<bookmark mark='c'/>精确率和召回率问的才是你关心的：在你叫作狄更斯的书页里，有多少真的是？{ap_s}",

    "f'Average precision falls from": "平均精确率从{base:.2f}跌到{rr['ap']:.2f}：现在大多数警报都是误报。",
    "f'Average precision moves from": "平均精确率从{base:.2f}变到{rr['ap']:.2f}。",

    'f"And how sure is any single number?':
        "那么，任何单个数字有多可靠？在两个词频上的逻辑回归，一遍又一遍地打分。<bookmark mark='a'/>在100种不同的随机训练、测试划分上，它的准确率从{100 * sa.min():.0f}%到{100 * sa.max():.0f}%不等：这是划分的运气。<bookmark mark='b'/>10折交叉验证让每一页都恰好当一次测试页。每一折单独看，会晃动大约{100 * fa.std():.0f}个百分点，<bookmark mark='c'/>但它们的平均很稳定：20种不同的洗牌，结果全都落在{100 * ca.min():.1f}%到{100 * ca.max():.1f}%之间。<bookmark mark='d'/>让整场比赛保持诚实的规则是：每一个选择都在训练页上做，测试页只在最后看一次。",

    # ---------------------------------------------------------------- Contest
    'Chapter seventeen. The contest.': '第17章。比赛。',

    'f"Here\'s the whole contest':
        "这就是整场比赛：每种方法都用同样的10折，覆盖全部书页，设置事先固定。<bookmark mark='a'/>只用两个词频，每种方法都落在{100 * lo2:.0f}%到{100 * hi2:.0f}%之间：两个数里，能装的信息就这么多。<bookmark mark='b'/>用全部70个，最好的是{best70['name']}，{100 * best70['70']['cv']:.1f}%。一棵单独的树只有{100 * tree70:.0f}%。{line_s}<bookmark mark='c'/>这就是经典机器学习的教训：对数据的描述，比方法有多巧妙更要紧。挑出70个小词，就完成了大部分工作。",

    'And the plain straight line, logistic regression, beats the boosted trees':
        "而最朴素的那条直线，逻辑回归，胜过了提升树：在这些书页上，证据确实是许多微小的词语效应之和，这正是直线的主场，朴素贝叶斯的公式早就暗示了这一点。",
    'Boosted trees edge out the straight line here.': '在这里，提升树略胜直线一筹。',

    'In 2001 Leo Breiman, who had left statistics':
        "2001年，曾经离开统计学去做咨询、后来又回来的利奥·布雷曼，描述了两种文化。大多数统计学家先假定数据是怎样产生的，再去估计这个模型。少数人，大多在统计学之外，把自然当作一个黑箱，只看一个方法对新数据预测得有多好。这一部分，一直属于第二种文化。<bookmark mark='a'/>竞赛让它成了常态。2006年，Netflix悬赏一百万美元，征求把评分预测提高10%的办法；<bookmark mark='b'/>2009年，几百个模型的融合赢得了它。<bookmark mark='c'/>Kaggle把比赛变成了一种职业，<bookmark mark='d'/>而在2015年，Kaggle博客上公布的29个获胜方案里，有17个用了XGBoost。",

    'Deep learning took over images, sound and language.':
        "深度学习接管了图像、声音和语言。为什么没有接管表格？2022年，格林斯塔因、瓦永和瓦罗科在45个、每个约一万行的表格数据集上做了测试，树的集成仍然胜过深度网络。<bookmark mark='a'/>他们给出的理由是：表格里有无用的列，而树根本不会去问它们；每一列都有自己的含义，网络却把它们搅在一起；而答案常常是一级一级地跳变，树画起来很容易。<bookmark mark='b'/>挑战者是一个只在几百万张合成表格上训练出来的Transformer，它把你的训练行当作提示读进去，一次前向传播就给出预测。TabPFN的第二版，2025年1月发表在《自然》上，在不到三秒内，胜过了一个调了四小时的集成，适用于至多一万行的表格。<bookmark mark='c'/>它的后继者能处理五万行，然后，今年五月，一百万行，按其开发者的统计，在TabArena排行榜上名列第一。<bookmark mark='d'/>六月的一项独立基准测试发现，它们在小型和中型表格上最好，而在大型的、会漂移的或非常宽的表格上，树依然领先。树和提升法，仍然是要打败的基准。",

    # ---------------------------------------------------------------- Outro
    "Let's take stock. Least squares is a projection":
        "我们来盘点一下。最小二乘法是一次投影，在线性无偏估计里是最好的。岭回归收缩弱的方向；套索回归的软阈值挑选词语。逻辑回归是一只凸的碗，牛顿法几步就找到碗底。朴素贝叶斯学得快，却一直有偏差，而且过于自信。单个邻居的错误率，至多是最好规则的两倍，但在很多维里，邻居们就被淹没了。核函数不抬升地抬升，支持向量机的对偶问题只需要它们。把树平均起来，能把方差降到由相关性决定的下限；提升法沿着指数损失往下走，XGBoost迈的是牛顿步。而一个诚实的分数，需要对的曲线，和没碰过的测试页。",

    'All of it comes back.':
        "这一切都会回来。交叉熵、梯度和曲率，是第9和第11部分里每个网络的训练方式，而softmax就是多类的逻辑回归。第7部分搭建统计模型：主成分、混合模型、贝叶斯。第8部分追问一个模型为什么能泛化，并遇到神经正切核，一个表现得像核机器的网络。第13部分把注意力读作核平滑器，而第31部分对语言模型提出我们对朴素贝叶斯提过的同一个问题：它的概率诚实吗？",

    'Here are eight problems to try':
        "这里有8道习题，从高斯–马尔可夫定理到XGBoost的增益。在这里暂停一下，动手做一做；完整的解答在这一部分的笔记里。",

    'Next time: statistical machine learning.':
        "下一次：统计机器学习。这一部分里的每种方法，都被告知了每个训练页是谁写的。<bookmark mark='a'/>第7部分把标签拿走，问一问：不靠标签，那里还有什么结构？书页散开的方向，它们聚成的簇，以及背后隐藏的原因。",

    'For more, The Elements of Statistical Learning':
        "想了解更多：黑斯蒂、蒂布希拉尼和弗里德曼的《统计学习基础》涵盖了这里的每一种方法，三位作者本身就参与创造了它们；毕晓普的《模式识别与机器学习》给出概率的视角；舍尔科普夫和斯莫拉的《用核学习》讲核方法。感谢观看，第7部分见。",
})

ZH.update({
    '"Why is Newton so fast at the end?':
        "为什么牛顿法在最后这么快？接近谷底时，损失几乎恰好是一条抛物线，每一步的误差，大约是上一步误差的平方。<bookmark mark='a'/>把一个很小的数平方，它小数点后的零就翻倍。<bookmark mark='b'/>在70个词频上，一步一步看，{say}",
    'f"the correct digits go {last[0]:.0f}, {last[1]:.0f}, {last[2]:.0f}: roughly doubling':
        "正确的位数依次是{last[0]:.0f}、{last[1]:.0f}、{last[2]:.0f}：大致翻倍，直到计算机的16位有效数字用完为止。",
    "f'the correct digits go {last[0]:.0f}, {last[1]:.0f}, {last[2]:.0f}.'":
        "正确的位数依次是{last[0]:.0f}、{last[1]:.0f}、{last[2]:.0f}。",
    'f"Here\'s what it learned, by counting.':
        "这是它靠计数学到的东西。每个词的权重，是狄更斯用这个词比奥斯汀多出多少倍，再取对数。<bookmark mark='a'/>奥斯汀最有力的词：{aw}。<bookmark mark='b'/>狄更斯的：{dw}。一个词每出现一次，就把它的权重加到这一页的对数几率上。",
    'f"One more weakness. Grow the same small tree':
        "还有一个弱点。在训练页的重抽样上，也就是有放回地抽取，把同样的小树种{len(roots)}次。<bookmark mark='a'/>第一个问题会变：有{len(words)}个不同的词当过第一个问题，最常见的是“{words[0]}”，{len(roots)}棵树里占了{n1}棵。再往下，树之间的分歧更大。<bookmark mark='b'/>在留出的书页上，它们的成绩从{100 * acc.min():.0f}%到{100 * acc.max():.0f}%不等。一棵树是高方差的学习器，而下一章，会把这个弱点变成长处。",
    'None of this went away; it moved inside the big models.':
        "这些都没有消失；它们搬进了大模型的内部。<bookmark mark='a'/>每个语言模型的最后一层，都是在整个词表上的逻辑回归。用最小二乘拟合的线性探针，从网络里读出概念，而岭回归的惩罚项，就是权重衰减。<bookmark mark='b'/>套索回归的绝对值惩罚，是稀疏自编码器从模型中提取特征的办法。核函数描述了非常宽的网络，而注意力就是一个核平滑器。<bookmark mark='c'/>最近邻变成了检索。提升树仍然在支撑全世界的表格和搜索排序，而朴素贝叶斯提出的那个问题，模型的概率到底有没有意义，如今每一个聊天机器人都要面对。",
})

ZH.update({
    'f"Here is what ridge does to the seventy weights':
        "这是岭回归对70个权重做的事，从很强的惩罚一直到几乎没有惩罚。<bookmark mark='a'/>随着λ减小，每个权重都平滑地从零长出来。{say_zero}<bookmark mark='b'/>岭回归还有另一种解读：如果在看到任何书页之前，你就相信权重都很小，也就是用一个钟形的先验，就像第5部分那样，那么它就是最可能的那组权重。在神经网络里，同样的惩罚叫作权重衰减。",
    'Not one weight ever reaches exactly zero.': '没有一个权重恰好等于零。',
    "f'Only {zeros} weights ever reach exactly zero.'": '只有{zeros}个权重恰好等于零。',
    'Why is that cut the best possible one?':
        "为什么这一刀是可能的最好切法？假设每位作者的书页都是一个钟形分布，两个钟形的形状相同。<bookmark mark='a'/>贝叶斯法则给出是狄更斯的对数几率。<bookmark mark='b'/>把两个二次型展开：因为形状相同，x乘x的项互相抵消，剩下的是关于x的一条直线。<bookmark mark='c'/>概率是一条直线的S形函数，恰好就是逻辑回归的形式，而它的权重就是费希尔的方向。LDA是生成式的，和朴素贝叶斯一样：它先估计两个钟形，再相除；逻辑回归则直接拟合那条直线。",
})

ZH.update({
    'f"How many words to keep?':
        "保留多少个词？对整条路径做交叉验证：对每个惩罚强度，在十分之九的训练页上拟合，在剩下的十分之一上打分，这样做10遍。<bookmark mark='a'/>误差在{int(nnz[b])}个词时最低。<bookmark mark='b'/>但曲线在那里几乎是平的，它的晃动，也就是一个标准误，和这些差别一样大。通常的规则，是在最好结果的一个标准误之内挑出最稀疏的模型：{int(nnz[o])}个词。",
    'f"Where did C and gamma come from?':
        "C和γ是从哪里来的？一个网格：{len(Cs)}种代价乘以{len(gs)}种核宽度，每一对都在训练页上用10折交叉验证打分。<bookmark mark='a'/>最好的一对平均判对{100 * cv.max():.1f}%，但{cv.size}种设置里有{near}种和它相差不到一个百分点。<bookmark mark='b'/>只有很小的C，街道里站人太便宜，边界几乎不弯，才会跌到{100 * worst:.0f}%。每页只有两个数时，方法不如数据要紧。",
    'f"Accuracy only counts right and wrong.':
        "准确率只数对和错。一个恰当的评分，比如第1部分的对数损失，还会为自信程度收费。<bookmark mark='a'/>{say}",
    'f"Naive Bayes gets {100 * c[\'acc\'][\'nb\']:.0f} percent':
        "朴素贝叶斯判对了{100 * c['acc']['nb']:.0f}%的书页，远多于两个词频的逻辑回归的{100 * c['acc']['lr2']:.0f}%，可它的对数损失反而更差，{nb['logloss']:.2f}对{l2['logloss']:.2f}：它一旦错了，就是以一百万比一的几率错，而对数损失会为这份自信的每一位数字收费。普拉特缩放把它降到{c['nb_platt']['logloss']:.2f}。",
    "f'Here the log loss tells the same story as accuracy":
        "在这里，对数损失和准确率说的是同一件事：朴素贝叶斯{nb['logloss']:.2f}，两个词频的逻辑回归{l2['logloss']:.2f}。",
})

PHRASES = {
    'zero, up to rounding.': '零，只差舍入误差。',
    'a ten-millionth': '千万分之一',
    'a millionth': '百万分之一',
    'a hundred-thousandth': '十万分之一',
    'a thousandth': '千分之一',
    '.': '。',
    'least squares': '最小二乘',
    'lasso': '套索回归',
    'logistic regression': '逻辑回归',
    'naive Bayes': '朴素贝叶斯',
    'LDA (Fisher)': 'LDA（费希尔）',
    '15 nearest neighbours': '15个最近邻',
    'linear SVM': '线性支持向量机',
    'Gaussian-kernel SVM': '高斯核支持向量机',
    'one tree (depth 4)': '单棵树（深度4）',
    'random forest (200)': '随机森林（200棵）',
    'AdaBoost (200 stumps)': 'AdaBoost（200个树桩）',
    'gradient boosting (100)': '梯度提升（100轮）',
}

# Scoped teaching/protocol corrections; production captures are regenerated after the source freeze.
ZH.update({
    "You might look for names or places.": "你也许会去找人名或地名。但在1964年，莫斯特勒与华莱士判定了《联邦党人文集》里那些有争议的篇章出自谁手，靠的是数小词，比如“upon”、“whilst”和“also”。<bookmark mark='a'/>所以，我们先固定一份词表：在完整的5部小说里，无需作者标签、在划分数据之前选出最常见的70个词，再用它们的词频描述每一页。<bookmark mark='b'/>这一页“the”用得很多，“not”用得很少，像狄更斯。奥斯汀用“not”、“very”和“be”，要多得多。",
    "f\"Take just two of those numbers": "只取其中两个数：一页用“the”有多频繁，用“not”有多频繁，每一页就变成了一个点。<bookmark mark='a'/>这是来自5部小说的{n}页。两位作者大体上各占一边，但也有重叠。我们用其中{int((~test).sum())}页来训练，另外{int(test.sum())}页不参与分类器拟合，留作测试。这是同样5部小说中的新片段，不是从未见过的小说；缩放参数和分类器都只在训练页上拟合。<bookmark mark='b'/>把两位作者区分开，是机器学习的核心任务之一：分类。画一条直线？把它弄弯？问问邻居？提一连串问题？这一部分把这些办法都试一遍。",
    "f\"Here is what ridge does to the seventy weights": "这是岭回归对70个权重做的事，从很强的惩罚一直到几乎没有惩罚。<bookmark mark='a'/>随着λ减小，原坐标系中的权重路径平滑变化；单个权重可能转向，或者穿过零。单调收缩的是奇异方向上的分量，并不是每一个坐标权重。{say_zero}<bookmark mark='b'/>岭回归还有另一种解读：如果在看到任何书页之前，你就相信权重都很小，也就是用一个钟形的先验，就像第5部分那样，那么它就是最可能的那组权重。在神经网络里，同样的惩罚叫作权重衰减。",
    "f\"The best direction has a formula": "最好的方向有一个公式：两个中心之差，再用两位作者内部合并散布的逆来校正。<bookmark mark='w'/>先用合并协方差的逆平方根W把空间白化；在那个空间里，合并的椭圆变成圆，再连接变换后的两个中心。<bookmark mark='pull'/>接着，用W转置把这个法向量映回原坐标。这两次逆平方根映射，合起来就给出费希尔公式里的完整逆矩阵，只差一个整体比例。<bookmark mark='a'/>在这里，它主要依靠“not”。<bookmark mark='b'/>在两堆的正中间切一刀，就得到一个分类器。它能判对{100 * acc:.0f}%的测试页{like_lr}<bookmark mark='c'/>当每一组都是形状相同的钟形分布时，这一刀，再按两位作者书页数量的不同稍作挪动，就是可能的最好切法。",
    "f\"Where does the formula come from?": "这个公式从哪里来？<bookmark mark='a'/>费希尔的得分，是两个二次型之比：作者之间的散布，除以作者内部的散布。<bookmark mark='b'/>令它的梯度为零，就得到一个广义特征值问题。当类内散布正定、两个均值不同时，要取最大的正特征值；零特征值的驻点并不使分离程度最大。<bookmark mark='c'/>但S B的秩是1：它永远只指向两个均值之差的方向。<bookmark mark='d'/>所以答案是S W的逆，乘以这个差。<bookmark mark='e'/>在全部70个词频上，特征值求解器只找到一个非零特征值，它的特征向量与公式的吻合程度是{ld['cos_eig']:.6f}。{also}<bookmark mark='f'/>它最依赖{names}，留出的书页判对{100 * ld['acc70']:.0f}%。",
    "It also agrees with least squares on a zero-one target": "它也和以0、1为目标的最小二乘有相同的系数方向。截距和分类阈值，仍然是另行选择的。",
    "f\"The lift can be expensive": "抬升可能代价很大：每个点的数一多，抬升后的特征就成倍增长。核技巧避开了它。<bookmark mark='a'/>取平面上一个点的这6个特征。<bookmark mark='b'/>它们的点积，展开以后，<bookmark mark='c'/>就是x点乘z加1，再平方：只用原来的两个数就算出来了，从来不用那6个。任何只需要点积的方法，比如支持向量机，都能免费地在抬升后的空间里运行。<bookmark mark='d'/>高斯核走得更远。把它展开，它的特征是坐标的每一个幂：无穷多个。做一个一维验证，令gamma等于1，保留前{len(errs)}个幂。在两个输入都位于负1.5到1.5的61乘61网格上，观察到的最大误差在{within}以内。",
    "f\"Many lines separate these two groups.": "能把这两组分开的直线有很多。瓦普尼克的问题是：哪一条最好？<bookmark mark='a'/>他的答案是：两侧空出的街道最宽的那一条。<bookmark mark='b'/>一个点到直线的距离，是它的得分除以w的长度。<bookmark mark='c'/>把w缩放到最近的点得分恰好为1；<bookmark mark='d'/>那么街道的宽度就是2除以w的长度，<bookmark mark='e'/>而最宽的街道，就是能让每个点都留在自己一侧的、最短的w。<bookmark mark='f'/>街道的两条边，只靠在{len(sv)}个点上，这些点就是支持向量。只要另一个点仍留在原来间隔的外侧，移动它就不会改变这个解。",
    "Real authors overlap, so no street is empty.": "真实的作者是重叠的，所以没有哪条街道是空的。1995年，科尔特斯与瓦普尼克允许点站到街道里，甚至站到错误的一侧，但要付出代价。<bookmark mark='a'/>这个代价就是铰链损失：安全地站在自己一侧的页，代价是零；一旦越界，代价就沿直线增长。<bookmark mark='b'/>把它和“对还是错”比一比，后者难以用梯度优化；再和逻辑回归的损失比一比。两者都是计数错误的凸替代损失；逻辑损失光滑，而铰链损失在间隔1处有一个折角。<bookmark mark='c'/>常数C设定这个代价：C大，街道窄，为每一页都去争；C小，街道宽，比较宽容。",
    "\"How does the tree choose its question?": "树是怎样选问题的？它衡量每个方格有多混杂。<bookmark mark='a'/>三种不纯度：基尼不纯度，第1部分的熵，还有朴素的错误率。<bookmark mark='b'/>一个问题的增益，是父节点的不纯度，减去子节点按大小加权的不纯度。<bookmark mark='c'/>父节点里狄更斯的比例，是子节点比例的平均，<bookmark mark='d'/>所以只要不纯度曲线严格向下弯，詹森不等式就保证：只要子节点之间有差别，增益就是正的。错误率是一顶帐篷，两侧都是直线：即使两个子节点的类别比例不同，只要都在二分之一的同一侧，按错误率计算的增益仍可为零。<bookmark mark='e'/>扫过每一个阈值。{say}",
    "f\"A classifier gives a score; we chose to cut at a half.": "分类器给出一个分数；我们选择在二分之一处切开。每一种切法，都是一种取舍。<bookmark mark='a'/>从最严格开始，什么都不叫作狄更斯。降低阈值：你找到了更多狄更斯的书页，也就是命中，但也开始把奥斯汀的书页叫作狄更斯，也就是误报。<bookmark mark='b'/>描出来的这条路径，就是ROC曲线，它来自第二次世界大战中的雷达操作员。<bookmark mark='c'/>它的面积有一个很美的含义：随机取一个狄更斯书页，它的分数高于随机取的一个奥斯汀书页的概率，再加上打平概率的一半。把全部{P * N:,}对数一遍：{mw:.4f}，恰好就是这个面积。",
    "f\"And how sure is any single number?": "那么，任何单个数字有多可靠？在两个词频上的逻辑回归，一遍又一遍地打分。<bookmark mark='a'/>在100种不同的随机训练、测试划分上，它的准确率从{100 * sa.min():.0f}%到{100 * sa.max():.0f}%不等：这是划分的运气。<bookmark mark='b'/>10折交叉验证让每一页都恰好当一次测试页。每一折单独看，会晃动大约{100 * fa.std():.0f}个百分点，<bookmark mark='c'/>但它们的平均很稳定：20种不同的洗牌，结果全都落在{100 * ca.min():.1f}%到{100 * ca.max():.1f}%之间。<bookmark mark='d'/>让整场比赛保持诚实的规则是：每一个选择都在训练页上做，最后才在测试页上看一次。这衡量的是同样5部小说的新片段，并且词表取自完整语料；它不衡量对从未见过的小说的迁移。",
    "Let's take stock. Least squares is a projection": "我们来盘点一下。最小二乘法是一次投影，在线性无偏估计里是最好的。岭回归收缩弱的方向；套索回归的软阈值挑选词语。逻辑回归是一只凸的碗，牛顿法几步就找到碗底。朴素贝叶斯学得快，却一直有偏差，而且过于自信。在大样本极限下，单个邻居的错误率至多是最好规则的两倍，但在很多维里，邻居们就被淹没了。核函数不抬升地抬升，支持向量机的对偶问题只需要它们。把树平均起来，能把方差降到由相关性决定的下限；提升法沿着指数损失往下走，XGBoost迈的是牛顿步。而一个诚实的分数，需要对的曲线，和没碰过的测试页。",
    "No sampled coefficient falls below our numerical tolerance of ten to the minus twelve.": "没有任何采样系数的绝对值低于我们十的负十二次方的数值容差。",
    "f\"At {near_zero} sampled coefficient-and-penalty pairs": "在{near_zero}个采样的“系数、惩罚强度”组合上，系数的绝对值低于十的负十二次方。",
    "f\"Now the test: chunks excluded from fitting": "现在来测试：从同样5部小说中取出、未参与拟合的片段。只用两个词频，这条直线判对了{100 * lg['acc2']:.0f}%。<bookmark mark='a'/>换成全部70个词频，同样的方法在{n_te}个测试页中判对了{round(lg['acc70'] * n_te)}个。{comparison}这个测试并不能确定它在从未见过的小说上有多准确。",
    "Here the seventy-rate model scores higher than the two-rate model.": "这里，70个词频的模型得分高于两个词频的模型。",
    "Here the seventy-rate and two-rate models tie.": "这里，70个词频和两个词频的模型打平。",
    "Here the seventy-rate model scores lower than the two-rate model; more features need not help.": "这里，70个词频的模型反而得分更低；更多特征未必有帮助。",
    "f\"The training error never reaches zero in these": "在这{n}轮中，训练错误率从未到零，最后是{100 * tr[-1]:.1f}%。留出错误率最后是{100 * te[-1]:.1f}%，观察到的最低值是第{best}轮的{100 * te.min():.1f}%。",
    "f\"Here are the measured log losses: naive Bayes": "这里测得的对数损失是：朴素贝叶斯{nb['logloss']:.2f}，两个词频的逻辑回归{l2['logloss']:.2f}。",
    "f\"Here's the contest: twelve named procedures": "这是比赛：12种具名流程，在同样5部小说书页的相同10折上比较，使用固定的全语料词表，参数预先设定。<bookmark mark='a'/>只用两个词频时，这些受测流程在这些折上的准确率落在{100 * lo2:.0f}%到{100 * hi2:.0f}%之间。<bookmark mark='b'/>换成全部70个词频，{winner_s}单棵树是{100 * tree70:.0f}%。{line_s}<bookmark mark='c'/>经典机器学习的一课是：数据的描述，比方法的巧妙更重要。这70个小词，做了大部分工作。",
    "A finite paired logistic-versus-boosting comparison is unavailable here.": "这里没有可用的、有限的逻辑回归与提升树配对比较。",
    "Logistic regression scores higher than boosted trees in these folds.": "在这些折上，逻辑回归得分高于提升树。对这个固定语料任务，小词效应的和是一种有用的描述。",
    "Logistic regression and boosted trees tie on mean accuracy in these folds.": "在这些折上，逻辑回归和提升树的平均准确率打平。",
    "Boosted trees score higher than logistic regression in these folds.": "在这些折上，提升树得分高于逻辑回归。"
})

ZH.update({
    "f\"Naive Bayes gets {100 * c['acc']['nb']:.0f} percent": "朴素贝叶斯判对了{100 * c['acc']['nb']:.0f}%的书页，高于两个词频的逻辑回归的{100 * c['acc']['lr2']:.0f}%，可它的对数损失更差，{nb['logloss']:.2f}对{l2['logloss']:.2f}。对数损失会为错误答案中自信程度的每一位数字收费。普拉特缩放后，测得的损失是{c['nb_platt']['logloss']:.2f}。"
})

ZH.update({
    "No sampled coefficient magnitude falls below our numerical tolerance of ten to the minus twelve.": "没有任何采样系数的绝对值低于我们十的负十二次方的数值容差。"
})

# Primary-source qualification: Beyond IID evaluates TabPFN-2.6, not TabPFN-3.
ZH.update({
    "Deep learning took over images, sound and language.": "深度学习接管了图像、声音和语言。为什么没有接管表格？2022年，格林斯塔因、瓦永和瓦罗科在45个、每个约一万行的表格数据集上做了测试，树的集成仍然胜过深度网络。<bookmark mark='a'/>他们给出的理由是：表格里有无用的列，而树根本不会去问它们；每一列都有自己的含义，网络却把它们搅在一起；而答案常常是一级一级地跳变，树画起来很容易。<bookmark mark='b'/>挑战者是一个只在几百万张合成表格上训练出来的Transformer，它把你的训练行当作提示读进去，一次前向传播就给出预测。TabPFN的第二版，2025年1月发表在《自然》上，在不到三秒内，胜过了一个调了四小时的集成，适用于至多一万行的表格。<bookmark mark='c'/>它的后继者能处理五万行，然后，今年五月，一百万行，按其开发者的统计，在TabArena排行榜上名列第一。<bookmark mark='d'/>2026年6月一项更广泛的基准测试，其共同作者中包括模型作者，评估的是TabPFN二点六，而不是TabPFN三。基础模型在小型和中型、独立同分布的表格上表现很强；在非独立同分布、大型或非常宽的数据上，传统树模型和深度模型揭示了它们的适用边界。这些比较针对特定版本和任务，树模型与深度模型都是必要的基线。"
})

# Benchmark/task conditioning from the primary papers; release numerals retained.
ZH.update({
    "Deep learning took over images, sound and language.": "深度学习接管了图像、声音和语言。为什么没有接管表格？2022年，格林斯塔因、瓦永和瓦罗科在45个、每个约一万行的表格数据集上做了测试，树的集成仍然胜过深度网络。<bookmark mark='a'/>他们给出的理由是：表格里有无用的列，而树根本不会去问它们；每一列都有自己的含义，网络却把它们搅在一起；而答案常常是一级一级地跳变，树画起来很容易。<bookmark mark='b'/>挑战者是一个只在大量合成表格上训练出来的Transformer，它把你的训练行当作提示读进去，一次前向传播就给出预测。TabPFN的第二版，2025年1月发表在《自然》上，在论文报告的分类基准配置中，用不到三秒，胜过了一个调了四小时的集成；该基准适用于至多一万行的表格。<bookmark mark='c'/>它的后继者能处理五万行，然后，在2026年5月，200个特征时处理100万行；按其开发者的报告，在TabArena排行榜上名列第一。<bookmark mark='d'/>2026年6月一项更广泛的基准测试，其共同作者中包括模型作者，评估的是TabPFN二点六，而不是TabPFN三。基础模型在小型和中型、独立同分布的表格上表现很强；在非独立同分布、大型或非常宽的数据上，传统树模型和深度模型揭示了它们的适用边界。这些比较针对特定版本和任务，树模型与深度模型都是必要的基线。",

    # Reviewed measured-score and recap-cue variants.
    "No finite seventy-rate mean accuracy is available here.":
        "这里没有可用的、有限的70词频平均准确率。",
    "f\"{best70['name']} has the highest mean accuracy, at {100 * best70['70']['cv']:.1f} percent.\"":
        "{best70['name']}的平均准确率最高，为{100 * best70['70']['cv']:.1f}%。",
    "f'{len(leaders70)} procedures tie for the highest mean accuracy, at {100 * best_mean:.1f} percent.'":
        "{len(leaders70)}种流程并列取得最高平均准确率，为{100 * best_mean:.1f}%。",
    "Let's take stock. <bookmark mark='linear'/> Least squares is a projection":
        "我们来盘点一下。<bookmark mark='linear'/>最小二乘法是一次投影，在线性无偏估计里是最好的。<bookmark mark='penalties'/>岭回归收缩弱的方向；套索回归的软阈值挑选词语。<bookmark mark='logistic_newton'/>逻辑回归是一只凸的碗，牛顿法几步就找到碗底。<bookmark mark='bayes'/>朴素贝叶斯学得快，却一直有偏差，而且过于自信。<bookmark mark='neighbours'/>在大样本极限下，单个邻居的错误率至多是最好规则的两倍，但在很多维里，邻居们就被淹没了。<bookmark mark='kernels'/>核函数不抬升地抬升，支持向量机的对偶问题只需要它们。<bookmark mark='averaging'/>把树平均起来，能把方差降到由相关性决定的下限；<bookmark mark='boosting'/>提升法沿着指数损失往下走，XGBoost迈的是牛顿步。<bookmark mark='evaluation'/>而一个诚实的分数，需要对的曲线，和没碰过的测试页。",
})
