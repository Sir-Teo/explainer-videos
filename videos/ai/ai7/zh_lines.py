"""Chinese narration for ai7: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第7部分：统计机器学习'

CHAPTERS = {
    'Hook': '没人标注的结构',
    'PCA': '1. 主成分的两种求法',
    'PPCA': '2. 把PCA变成概率模型',
    'ICA': '3. 鸡尾酒会',
    'EM': '4. 混合模型与EM算法',
    'Topics': '5. 主题模型',
    'HMM': '6. 隐马尔可夫模型',
    'BaumWelch': '7. 鲍姆–韦尔奇，以及会听的机器',
    'Translation': '8. 靠计数来翻译',
    'KneserNey': '9. 从Good–Turing到Kneser–Ney',
    'Infini': '10. 无穷元模型',
    'Graphs': '11. 把模型画成图',
    'Causes': '12. 从图到因果',
    'GP': '13. 高斯过程',
    'Occam': '14. 贝叶斯奥卡姆剃刀',
    'BayesOpt': '15. 贝叶斯优化',
    'VI': '16. 变分推断',
    'Outro': '回顾、习题，以及这些想法会在哪里再现',
}

ZH = {
    # ---------------------------------------------------------------- chapter cards
    'Chapter one. Principal components, two ways.': '第1章。主成分的两种求法。',
    'Chapter two. PCA as a probability model.': '第2章。把PCA变成概率模型。',
    'Chapter three. The cocktail party.': '第3章。鸡尾酒会。',
    'Chapter four. Mixtures, and the EM algorithm.': '第4章。混合模型，以及EM算法。',
    'Chapter five. Topic models.': '第5章。主题模型。',
    'Chapter six. Hidden Markov models.': '第6章。隐马尔可夫模型。',
    'Chapter seven. Baum-Welch, and machines that listen.': '第7章。鲍姆–韦尔奇，以及会听的机器。',
    'Chapter eight. Translation by counting.': '第8章。靠计数来翻译。',
    'Chapter nine. Kneser-Ney, from Good-Turing.': '第9章。Kneser–Ney平滑：从古德–图灵估计说起。',
    'Chapter ten. The infinity-gram.': '第10章。无穷元模型。',
    'Chapter eleven. Models as pictures.': '第11章。把模型画成图。',
    'Chapter twelve. From graphs to causes.': '第12章。从图到因果。',
    'Chapter thirteen. Gaussian processes.': '第13章。高斯过程。',
    'Chapter fourteen. Bayesian Occam': '第14章。贝叶斯奥卡姆剃刀。',
    'Chapter fifteen. Bayesian optimization.': '第15章。贝叶斯优化。',
    'Chapter sixteen. Variational inference.': '第16章。变分推断。',

    # ---------------------------------------------------------------- Hook

    'How did we get here? In 1901 Karl Pearson':
        "我们是怎么走到这里的？1901年，卡尔·皮尔逊想找一条离一团点最近的直线。1933年，哈罗德·霍特林想找数据变化最大的那些方向，并把它们叫作主成分。<bookmark mark='a'/>到了二十世纪六十年代，工程师和密码破译者学会了对看不见的状态进行推理：1967年，安德鲁·维特比的解码器；1970年，伦纳德·鲍姆的训练方法。<bookmark mark='b'/>1977年，登普斯特、莱尔德和鲁宾证明，一个算法，也就是EM，几乎能拟合任何缺了几块的模型。<bookmark mark='c'/>朱迪亚·珀尔给这个领域带来了一种用图来做不确定性推理的语言。<bookmark mark='d'/>在IBM，弗雷德·耶利内克的团队把语音识别，后来又把翻译，都变成了统计问题：计数，平滑，让数据来做决定。<bookmark mark='e'/>到了九十年代，第2部分专家系统手写的规则，让位给了从数据中学来的概率。<bookmark mark='f'/>2003年的主题模型和2006年的高斯过程专著，为机器学习就是统计学的十年画上句号。<bookmark mark='g'/>深度学习吸收了这一切，却没有取代它。ELBO训练着今天的生成模型，混合模型把词元分给专家，前向算法为语音做对齐，上万亿词上的n元组检查着语言模型背下了什么。",

    'This is part seven of AI, Built: models with hidden parts':
        "这是《人工智能，从零搭建》的第7部分：带有隐藏部分的模型，方向、来源、状态和函数，我们从来观测不到它们，只能推断。<bookmark mark='a'/>这一部分讲：隐藏的方向和来源，从主成分一直讲到鸡尾酒会；<bookmark mark='r2'/>混合模型，以及拟合它们的EM算法，还有k均值和主题模型；<bookmark mark='r3'/>隐马尔可夫模型，以及它们在语音和翻译中掀起的统计革命；<bookmark mark='r4'/>最好的计数方法，最后是一个覆盖全部30部小说的无穷元模型；<bookmark mark='r5'/>图模型，以及它们关于因果能告诉我们什么；<bookmark mark='r6'/>还有贝叶斯的工具箱：高斯过程、奥卡姆剃刀、贝叶斯优化和变分推断。每一种方法都会写出来，并真的运行。",

    # ---------------------------------------------------------------- PCA
    'f"Pearson and Hotelling asked two different questions.':
        "皮尔逊和霍特林问了两个不同的问题。<bookmark mark='h'/>这又是那些书页，只取70个词频中的两个，“the”和“not”，各自缩放到分散程度为1。<bookmark mark='a'/>皮尔逊要的是离这些点最近的那条直线：平均平方距离最小，也就是这些红色的小线段。<bookmark mark='b'/>霍特林要的是点分散得最开的那个方向。<bookmark mark='c'/>把直线转一转，两样都看着。每一页的长度平方，按勾股定理，分成沿着直线的部分和垂直于直线的部分。所以保留下来的分散，加上损失掉的距离，在每个角度上都是同一个总数，{total:.2f}。<bookmark mark='d'/>离点最近的直线，就是分散最大的直线。两个问题，一个答案。",

    'f"Here\'s why, in a few lines.':
        "原因只要几行就能说清。数据沿着一个单位向量u的分散程度，是u转置乘C乘u，其中C是协方差矩阵。<bookmark mark='a'/>我们要让它最大，同时保持u的长度为1，所以引入一个拉格朗日乘子λ。<bookmark mark='b'/>令梯度为零，就得到一个特征向量方程：C乘u等于λ乘u。<bookmark mark='c'/>两边左乘u转置：沿着一个特征向量的分散，就是它的特征值。所以最好的方向，就是特征值最大的那个特征向量。<bookmark mark='d'/>而损失掉的距离，等于总数减去保留下来的分散，所以让一个最小，就是让另一个最大。<bookmark mark='e'/>用k个方向，剩下的误差，恰好等于我们舍掉的那些特征值之和。在这些书页上，用5个方向，误差是{err[5]:.2f}，总共70个单位的方差里的这么多，而且这个恒等式对每一个k都成立。",

    'f"Principal components find the directions in which data varies the most.':
        "主成分找的是数据变化最大的那些方向。先从协方差矩阵开始：它是70乘70的，记录着每一对词频是怎样一起变动的。<bookmark mark='a'/>它是对称的，所以按第3部分讲的，它的特征向量互相垂直，而每个特征值都说明，有多少变化落在它那个特征向量的方向上。<bookmark mark='b'/>第一个方向占了全部变化的{100 * share[0]:.1f}%，下一个占{100 * share[1]:.1f}%，然后就一路降下去了。",


    'What are these directions? Each one is a recipe':
        "这些方向是什么？每个方向都是一份配方，说明怎样把70个词频混合起来。<bookmark mark='a'/>第一个方向，一边是“not”、“be”、“very”和“she”，另一边是“the”、“and”和“out”。这就是奥斯汀对狄更斯，而且从来没有人告诉过它，哪一页是谁写的。<bookmark mark='b'/>第二个方向，一边是“I”、“me”、“you”、“said”和“my”，另一边是“of”和“their”。这是对话对叙述：书页之间另一个大的差别。",


    # ---------------------------------------------------------------- PPCA

    'The best W and sigma, by maximum likelihood':
        "按最大似然，最好的W和σ有闭式解。<bookmark mark='a'/>W的各列可以指向第1章里排在最前面的k个特征向量，每一列按特征值减去噪声方差后的平方根来拉伸。旋转隐藏坐标轴，也能得到同样好的拟合。<bookmark mark='b'/>而噪声，就是所有被舍掉的方向的平均方差。<bookmark mark='c'/>把噪声缩到零，就又回到了普通的PCA。所以PCA一直都是一个概率模型的极限，而现在它有了似然。",


    "f'Held-out pages are most likely with":
        "留出的书页在{best}个隐藏方向时可能性最大，每页{te[best]:.1f}奈特，胜过完整的协方差矩阵的{full:.1f}：其余的方向大多是噪声。",

    "f'Held-out pages peak at":
        "留出的书页在{best}个隐藏方向时达到峰值，每页{te[best]:.1f}奈特，但完整的协方差矩阵也一样好，{full:.1f}：在这些书页上，每个方向都带着一点信号。",


    # ---------------------------------------------------------------- ICA
    'In 1953 the psychologist Colin Cherry':
        "1953年，心理学家科林·彻里问：在一个嘈杂的房间里，我们是怎么跟得住一个人的声音的？这就是鸡尾酒会问题。<bookmark mark='a'/>这是给机器的版本。两个人同时说话。<bookmark mark='b'/>两个麦克风，各自听到两人声音的不同混合，离谁近，谁的声音就大。<bookmark mark='c'/>写成符号，x等于A乘s：我们录到的声音，是一个混合矩阵乘以那两个声音。可是矩阵和声音我们都不知道。我们手里只有x。",


    "f'The voices have kurtosis":
        "两个声音的峰度是{ks[0]:.2f}和{ks[1]:.2f}；白化后的混合是{km[0]:.2f}和{km[1]:.2f}，更靠近0。",

    "f'Here the voices have kurtosis":
        "这里两个声音的峰度是{ks[0]:.2f}和{ks[1]:.2f}，白化后的混合是{km[0]:.2f}和{km[1]:.2f}。",

    '"Turn the white cloud to that angle':
        "把这团白化的点转到那个角度，读出两个输出。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>独立成分分析起源于八十年代让尼·埃罗和克里斯蒂安·于唐的电路，经过1994年皮埃尔·科蒙的定义，以及贝尔和谢诺夫斯基的信息最大化方法。把它用在自然图像的小块上，它会找出边缘检测器，就像视觉皮层里的那样。今天，它被用来从脑电记录里清除眨眼的干扰；而它的想法，找出数据在其上稀疏而独立的那些方向，正是第30部分稀疏自编码器背后的字典学习。",

    "f'The two outputs follow the voices with correlations of":
        "两个输出跟随两个声音的相关系数是{r_ica.min():.4f}，甚至更高。光靠白化，只能做到{r_pca.max():.2f}。",

    "f'The outputs follow the voices with correlations of":
        "两个输出跟随两个声音的相关系数是{r_ica.min():.2f}和{r_ica.max():.2f}。",

    # ---------------------------------------------------------------- EM
    'PCA finds directions. A mixture model goes further':
        "主成分分析找的是方向。混合模型更进一步：它假设每个点都出自几个隐藏来源中的一个，每个来源都是自己的一条钟形曲线，然后设法把这些来源找回来。这是沿前两个方向排开的书页，没有颜色：我们不知道哪一页是谁写的。<bookmark mark='a'/>先猜两条钟形曲线，位置放得很差。期望最大化算法，简称EM算法，在两个步骤之间交替进行。<bookmark mark='b'/>E步：对每一页，每条钟形曲线生成它的可能性有多大？这就给每一页涂上了一种介于两色之间的颜色。<bookmark mark='c'/>M步：按这些颜色加权，把每条钟形曲线重新拟合到书页上。",





    'f"It matches the authors {100 * km[\'agree\']:.0f} percent of the time, a little below':
        "它与作者吻合的比例是{100 * km['agree']:.0f}%，比EM的{100 * km['agree_em']:.0f}%稍低一点：硬性的选择，扔掉了对边界附近书页的那份犹豫。",

    'f"It matches the authors {100 * km[\'agree\']:.0f} percent of the time, as well as':
        "它与作者吻合的比例是{100 * km['agree']:.0f}%，和EM的{100 * km['agree_em']:.0f}%一样好。",

    # ---------------------------------------------------------------- Topics
    'A mixture model gives each page one hidden source.':
        "混合模型给每一页一个隐藏的来源。可一本书同时讲着好几件事。2003年，戴维·布莱、吴恩达和迈克尔·乔丹为此写下了一个模型：潜在狄利克雷分配，也就是主题模型。<bookmark mark='a'/>它的故事是这样的。有K个主题，每个主题是词上的一个分布。<bookmark mark='b'/>每一段文本有自己的主题配比，从一个狄利克雷分布里抽出来，这个分布偏爱只由少数几个主题组成的配比。<bookmark mark='c'/>每个词分两步生成：先从这段文本的配比里挑一个主题，再从这个主题里挑一个词。<bookmark mark='d'/>只有词是观测到的。主题、配比、每个词的主题，都是隐藏的，我们要把它们全推断出来。",


    'though, with the smoothing we add, not on every round': '不过因为我们加了平滑，并不是每一轮都升',

    'f"Here are all twelve topics after forty rounds':
        "这是40轮之后的全部12个主题，每个主题列出它最常见的词，以及它出现得最多的那部小说。<bookmark mark='a'/>没有人给它们起名字，但你读得出来。最常出现在{l['main'][c3[0]]}里的那个主题，打头的词是“{l['top'][c3[0]][0]}”，在{l['main'][c3[1]]}里的那个是“{l['top'][c3[1]][0]}”，在{l['main'][c3[2]]}里的那个是“{l['top'][c3[2]][0]}”。其余的就不那么好命名了。<bookmark mark='b'/>这是{l['ex_title']}里的一段，每个词按它最可能的主题上色。它的配比是：{100 * th[top2[0]]:.0f}%是一个主题，{100 * th[top2[1]]:.0f}%是另一个。<bookmark mark='c'/>有十来年的时间，主题模型是历史学家和社会科学家阅读那些多得读不完的档案的办法。如今，这项工作大多交给了嵌入向量，但那个想法，一篇文档是若干隐藏主题的混合，仍是同一幅图。",

    # ---------------------------------------------------------------- HMM


    'Second: which hidden states produced the letters?':
        "第二个问题：是哪些隐状态生成了这些字母？只改一处：把求和换成取最大值。<bookmark mark='a'/>现在每个圆圈里存的，是通向它的那一条最佳路径的概率，我们再记下它是从哪个状态来的：每个圆圈只有一根亮起来的箭头指进来。<bookmark mark='b'/>到了最后，取较好的那个终点状态，顺着指针往回走。这就是最可能的路径，精确地找出来，而不用把它们全试一遍。<bookmark mark='c'/>安德鲁·维特比在1967年发表了这个算法，用来给纠错码解码；它进了手机，也上了太空探测器，还为语音解码了几十年。",


    # ---------------------------------------------------------------- BaumWelch

    'f"Give it two hidden states,':
        "给它两个隐状态、书里的{h['n']:,}个字母，再加上随机的初始猜测。<bookmark mark='b'/>然后运行鲍姆–韦尔奇算法，看看每个状态学会了发射什么。",


    'This is how machines learned to listen.':
        "机器就是这样学会听的。二十世纪七十年代，詹姆斯·贝克的DRAGON系统，以及弗雷德·耶利内克在IBM的团队，把语音识别当成了一个统计问题。<bookmark mark='a'/>把声音切成帧，每秒一百帧，每一帧是一个特征向量。<bookmark mark='b'/>把语言里的每一个音，都建成一个小小的隐马尔可夫模型，从左到右三个状态，再把它们串成词。<bookmark mark='c'/>每个状态从一个高斯混合模型里发射特征向量：第4章的混合模型，装进了第6章的链里，全都用鲍姆–韦尔奇算法，在好几个小时的录音上训练出来。<bookmark mark='d'/>一本发音词典把音变成词，再由一个关于词序列的计数模型，也就是第9章的主题，在听起来差不多的句子之间做选择。维特比算法找出最好的那一句。<bookmark mark='e'/>数据胜过了规则。归在耶利内克名下的那句话，最有名的说法是：每当我开除一个语言学家，语音识别器的表现就提高。他自己记得的措辞不同，但意思流传了下来。<bookmark mark='f'/>这套设计统治了语音识别三十年，直到2012年前后，深度网络取代了高斯混合模型，后来又取代了整条流水线。第23部分接着讲。",

    # ---------------------------------------------------------------- Translation
    'In 1947 Warren Weaver':
        "1947年，在战时主持过美国科研工作的沃伦·韦弗写道，一篇俄文文章，也许就是用奇怪的密码写成的英文，等着人去破译。<bookmark mark='a'/>机器翻译最初的几十年用的却是规则，1966年，一份政府报告，也就是ALPAC报告，判定它们失败了。<bookmark mark='b'/>二十年后，耶利内克在IBM的语音团队，把韦弗的话当了真。假装法文本来是英文，只是经过了一条有噪声的信道。<bookmark mark='c'/>要解码，就去找一个英文句子，它本身就很可能出现，这由语言模型来判断；而且很可能变成眼前这句法文，这由翻译模型来判断。<bookmark mark='d'/>他们用EM，从加拿大议会以两种语言发布的议事记录里，一百多万对句子中，学出了翻译模型。",


    '"Now translate sentences it never saw':
        "现在翻译它从没见过的句子，一个词一个词地查表。<bookmark mark='a'/>有些译得完全正确。有些把形容词放在名词后面，是法语的习惯。译得有多好？2002年，IBM的基肖尔·帕皮内尼和同事提出了一个谁都能算的分数：BLEU。<bookmark mark='b'/>数一数输出里的单个词、两个词、三个词和四个词的片段，有多大比例出现在人工的参考译文里，把它们的对数取平均，再惩罚太短的输出。<bookmark mark='c'/>{verdict}<bookmark mark='d'/>真正的系统会学出自己的词序：先是IBM后来的几个模型，然后是基于短语的翻译，它从2006年起一直支撑着谷歌翻译，直到2016年被神经网络取代。而模型1的那张对齐表，在2014年以注意力的形式回来了，那是一种学出来的软对齐。",

    "f'Word by word, our Model 1 scores {b1['bleu']:.2f}. Swap":
        "逐词翻译，我们的模型1得分是{b1['bleu']:.2f}。把法语的形容词挪到它的名词前面，这是语言学家会写的一条规则，分数就升到了{b2['bleu']:.2f}。",

    "f'Word by word, our Model 1 scores {b1['bleu']:.2f}; one":
        "逐词翻译，我们的模型1得分是{b1['bleu']:.2f}；加上一条调整词序的规则，仍然是{b2['bleu']:.2f}。",

    # ---------------------------------------------------------------- KneserNey
    '"Counting fails on what it has never seen':
        "计数在从没见过的东西上会失灵，而大多数东西都是没见过的。解决办法来自破译密码。在布莱奇利园，艾伦·图灵和他的助手杰克·古德，需要知道那些还从没见过的东西出现的概率。古德在1953年发表了这个方法，并把功劳归于图灵。<bookmark mark='a'/>设N下标r是恰好被见过r次的不同东西的个数。一个见过r次的东西，实际上值r星：r加1，乘上N下标r加1，再除以N下标r。而所有没见过的东西，加起来的概率是N下标1除以N，也就是恰好见过一次的那部分所占的比例。<bookmark mark='b'/>我们拿小说里的词对来检验：在一半里数，再到另一半里去核对。<bookmark mark='c'/>{verdict}",

    "f'It works. A pair seen once":
        "它管用。在小说的一半里见过一次的词对，在另一半里平均出现{r1['held']:.2f}次；Good–Turing只凭计数就预测出了{r1['gt']:.2f}。",

    "f'A pair seen once in one half":
        "在小说的一半里见过一次的词对，在另一半里平均出现{r1['held']:.2f}次；Good–Turing预测的是{r1['gt']:.2f}。",

    'f"Look at what a count loses between the two halves':
        "看看一个计数在两半之间损失了多少：r，减去同样那些词对在另一半里的平均次数。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>所以不必为每个r都套一个公式，只要从每个见过的计数里减去一个固定的折扣D，再把省下来的分给没见过的东西。这就是绝对折扣，也是Kneser–Ney的前一半。",

    "f'From two times on, the loss is nearly the same":
        "从2次开始，每个计数的损失几乎都一样，在{disc[1:].min():.2f}到{disc[1:].max():.2f}之间。肯尼斯·丘奇和威廉·盖尔1991年在新闻语料里看到的也是这样。",

    "f'The loss ranges from":
        "损失从{disc.min():.2f}到{disc.max():.2f}不等。",




    # ---------------------------------------------------------------- Infini



    "f'this context still appears":
        "这个上下文仍然出现了{counts[-1]}次，再多一个字符，它就消失了。",



    'f"Mixed with Kneser–Ney, it gives {mix:.3f} bits per character, against Kneser–Ney\'s {kn:.3f}: barely':
        "和Kneser–Ney混合，得到每字符{mix:.3f}比特，而Kneser–Ney是{kn:.3f}：几乎没有进步。在一部新小说里，长的匹配太少了。",

    'f"Mixed with Kneser–Ney, it gives {mix:.3f} bits per character, against Kneser–Ney\'s {kn:.3f}: no':
        "和Kneser–Ney混合，得到每字符{mix:.3f}比特，而Kneser–Ney是{kn:.3f}：在一部这些书从没见过的小说上，没有任何进步。",

    # ---------------------------------------------------------------- Graphs
    'Every model in this part can be drawn the same way':
        "这一部分的每个模型，都能用同一种方式画出来：<bookmark mark='q'/>每个量画一个圆圈，<bookmark mark='o'/>观测得到的涂上阴影，<bookmark mark='h'/>隐藏的留空，<bookmark mark='r'/>只要一个量直接依赖另一个，就画一根箭头。<bookmark mark='a'/>混合模型：先是一个隐藏的选择，选哪个来源，然后是一页书，每一页都这样重复一遍。<bookmark mark='b'/>隐马尔可夫模型：一串隐状态，每个都发射出一个字母。<bookmark mark='c'/>这幅图就是一个公式。一切的概率是一个乘积，也就是那个大大的π：每个圆圈乘上一个概率，每个概率只以指向它的那些圆圈为条件，也就是它的父节点。这就是贝叶斯网络：朱迪亚·珀尔为不确定性下的推理所创造的语言。",

    "Part one's language models fit the same picture":
        "第1部分的语言模型，也套得进同样的图：每个靠前的字母，都有一根箭头指向每个靠后的字母。<bookmark mark='a'/>没有什么是隐藏的，但也没有做任何简化：每个因子，都是根据全部过去做出的预测。这样的因子，靠计数是填不出来的。神经网络可以，从第9部分开始。",

    'f"A graph also tells you, without any numbers': "不用任何数字，一张图还能告诉你哪些东西是相互独立的。信息沿着路径流动，而路径上的连接点只有三种。<bookmark mark='a'/>在链里，多云导致下雨，下雨导致草地湿。一旦知道下了雨，云就不再告诉你关于草地的任何事：观测到中间那个，就把路径堵上了。<bookmark mark='b'/>在叉里，云既导致下雨，也让人较少开洒水器。两者看起来有关联：下雨的日子里，洒水器开着的比例是{100 * fk['p_s_r']:.0f}%，不下雨的日子里是{100 * fk['p_s_nr']:.0f}%。知道了云的情况，这个关联就消失了。<bookmark mark='c'/>对撞点是最奇怪的。下雨和洒水器本来相互独立，但两者都会把草地弄湿，而观测到湿草地，就把它们连了起来。{verdict}<bookmark mark='d'/>珀尔和他的学生把这三种情况变成了一条规则，d分离，可以从图上读出图所蕴含的条件独立关系。",

    "f'Simulate it: rain alone has a":
        "模拟一下：单独来看，下雨的概率是{100 * co['p_r']:.0f}%。草地湿了，这个概率升到{100 * co['p_r_w']:.0f}%。但如果草地湿了，而洒水器开着，它又回到{100 * co['p_r_ws']:.0f}%：洒水器把湿草地解释掉了。",

    "f'Simulate it: rain alone {100":
        "模拟一下：单独来看，下雨是{100 * co['p_r']:.0f}%；草地湿时是{100 * co['p_r_w']:.0f}%；草地湿而洒水器开着时是{100 * co['p_r_ws']:.0f}%。",

    'f"Pictures also tell us how to compute.': "图还告诉我们怎样计算。把模型重画成因子图：变量画成圆圈，乘积里的每个因子画成一个小方块，每个因子是一张数表。<bookmark mark='a'/>要求一个变量的概率，就得把其余所有变量的每一种组合都加起来。朱迪亚·珀尔1982年提出的信念传播，改为传递消息。<bookmark mark='b'/>每个圆圈告诉它的邻居，根据它那一侧的全部信息，它相信什么。先从叶子往上传到根，<bookmark mark='c'/>再往回传下来。<bookmark mark='d'/>把传入的消息与本地因子相乘，再归一化，就得到它的精确概率。在树上它是精确的：{exact_say}<bookmark mark='e'/>加上一个闭合成环的因子，同样的消息一圈又一圈地传，就只是近似的了，这里大约差了{loopy:.4f}。可是，有环的信念传播，正在为手机和卫星链路里的纠错码解码，而它的消息，就是第25部分图神经网络里的消息传递。",

    "f'it agrees with summing all":
        "它和把全部{2 ** n}个状态加起来的结果，一直吻合到最后几位。",

    "f'it differs from summing all":
        "它和把全部{2 ** n}个状态加起来的结果，相差{err:.4f}。",

    # ---------------------------------------------------------------- Causes
    'A real study, from 1986':
        "这是1986年的一项真实研究：取肾结石的两种办法，开放手术，和一种微创的经皮手术。<bookmark mark='a'/>对小结石，开放手术成功得更多。<bookmark mark='b'/>对大结石，开放手术也成功得更多。<bookmark mark='c'/>可是把所有病人放在一起，微创手术赢了。<bookmark mark='d'/>这就是辛普森悖论，它可不是算术上的把戏。医生把开放手术多半给了难治的病例，也就是大结石。把所有病人放在一起比较，就把治疗的效果和病例的难度搅在了一起。你会选哪种治疗？光凭数据说不出来。你得知道数据是从哪里来的。",

    'f"Draw where the data came from.':
        "把数据的来历画出来。结石的大小，影响了医生选择哪种治疗，也影响了成功与否。<bookmark mark='a'/>所以从治疗到成功有两条路径：直接的那条，是我们想要的效果；还有一条经过结石大小的后门，混杂就从这里进来。<bookmark mark='b'/>朱迪亚·珀尔的问题不是“做了开放手术的病人里，成功率是多少”，而是“如果给所有人都做开放手术，成功率会是多少”：也就是给定do x时的y。“做”的意思，是剪断所有指向治疗的箭头：治疗由人手来定，而不是由结石来定。<bookmark mark='c'/>如果有一个变量，这里是结石大小，挡住了所有的后门，那么“做”的效果，就能从只是“看”到的数据里算出来。对结石大小求平均，<bookmark mark='d'/>用每种大小内部的成功率，按每种大小在所有人中的常见程度加权。<bookmark mark='e'/>对肾结石来说，结果更支持{better}：{100 * adj['A']:.0f}%对{100 * adj['B']:.0f}%。这就是后门调整；珀尔的do演算，精确地说明了这样的公式什么时候存在。",

    '"To be sure, build a world where we know the truth.':
        "为了确认，我们造一个知道真相的世界。一半的病人是重症；医生给大多数重症病人治疗；治疗让康复率提高10个百分点，而重症让它降低35个百分点。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>相关不是干预。珀尔把它叫作一架梯子：看，做，以及想象如果当初不是这样会怎样。随机试验靠强制手段爬上了第二级。而第30部分在神经网络内部爬这一级：手动设定一个激活值，看看什么会跟着改变。",

    "f'Compare the treated with the untreated":
        "拿接受治疗的和没接受治疗的比，治疗看起来是有害的：{c['naive']:+.2f}。通过后门对严重程度做调整：{c['adjusted_sim']:+.3f}。现在来做实验，给每个病人掷一次硬币：{c['experiment']:+.3f}。调整找回了本来只有实验才能揭示的东西。",

    "f'The naive comparison gives":
        "朴素的比较给出{c['naive']:+.2f}，调整后是{c['adjusted_sim']:+.3f}，实验是{c['experiment']:+.3f}。",

    # ---------------------------------------------------------------- GP
    'Sometimes the hidden thing is a whole function.':
        "有时候，隐藏的东西是一整个函数。这是《远大前程》每一页用“her”的频率，从小说开头一直到结尾。随着故事在人物之间切换，它时起时落。<bookmark mark='a'/>高斯过程，是函数上的一个概率分布；这里的核函数让这些函数光滑。高斯的意思是钟形：在每一页，取值都是不确定的，最可能落在一条钟形曲线的中间附近。<bookmark mark='k'/>核函数k，说的是两页的取值有多么同步变化：两页离得近，就变化得很同步；离得远，就几乎互不相干。在看到任何数据之前，这是从中抽出的5个函数：它们弯弯曲曲，每道弯都有一个典型的宽度，叫作长度尺度。<bookmark mark='b'/>现在，以这些书页为条件。只有从数据近旁经过的函数，才能留下来。",

    'f"Their average is the best guess':
        "它们的平均就是最佳猜测，周围的那条带子表示不确定性。<bookmark mark='a'/>长度尺度大约是{g['ell']:g}页，它不是手工设定的：在这个长度尺度下，数据出现的概率最大。<bookmark mark='b'/>只给模型看前20页，固定核函数的设置，带子在这些书页之外又张开了。这是模型假设之下的不确定性，可以帮助决定下一步该看哪里。",

    'Why is conditioning so easy?':
        "为什么取条件这么容易？先减去均值。在高斯过程下，我们见过的那些书页，和任何一页新书上的取值，是联合高斯的，协方差由核函数给出。<bookmark mark='a'/>而一个高斯分布，以它的一部分坐标为条件，仍然是高斯分布。配方就能求出它的均值和方差。<bookmark mark='b'/>均值是观测值的加权和：在这个例子里，离得近的书页权重最大。<bookmark mark='c'/>固定核函数的设置，方差是先验方差减去数据能解释的部分。它根本不看取值本身，只看书页在哪里。拉斯穆森和威廉斯2006年的那本书，就把整个学科建立在这两行公式上。",

    '"Now watch the band shrink as pages land':
        "现在看着书页以随机的顺序一页页落下，带子跟着收窄。没有数据时，它就是先验：处处都是同样宽的带子。<bookmark mark='a'/>每一页都把函数在它附近钉住，带子在那里收紧。<bookmark mark='b'/>全部{ns[-1]}页都看过之后，平均的不确定性从{msd[0]:.1f}降到了{msd[-1]:.1f}。在书页之间，核函数认为频率还可能游移的地方，带子仍然张着。<bookmark mark='c'/>最早这样做的是采矿工程师：丹尼·克里格在五十年代估计钻孔之间的金矿品位，乔治·马特龙把它发展成一套理论，叫作克里金法。机器学习在九十年代把它接了过来。",

    # ---------------------------------------------------------------- Occam
    'Chapter thirteen chose its length scale': "第13章用一个我们还没解释过的量选出了长度尺度：边缘似然，也叫证据。它是数据在模型下的概率，对先验允许的每一个函数取平均。<bookmark mark='a'/>对高斯过程来说，这个平均可以精确地算出来：数据服从高斯分布，协方差是核矩阵加上噪声。<bookmark mark='b'/>取对数，会得到两项随模型改变的部分，以及一个归一化常数。<bookmark mark='c'/>一项衡量拟合：数据和模型的协方差吻合得有多好。<bookmark mark='d'/>另一项是复杂度的惩罚：那个对数行列式，衡量的是这个模型本来能生成多少种不同的数据集。一个灵活的模型，会把它的概率摊得很薄。",

    'f"Here are the two terms for the rate of \'her\'': "这是《远大前程》里“her”的频率对应的这两项，长度尺度在变，噪声和信号的水平固定在拟合出的值上。<bookmark mark='a'/>短的长度尺度给出弯弯曲曲的函数，能跟上每一页：拟合很好。长的长度尺度很平滑，会错过那些书页。<bookmark mark='b'/>但弯曲的函数本来能生成太多别的数据集，所以要付出很大的复杂度惩罚。<bookmark mark='c'/>再加上常数项，总对数证据在中间达到峰值，大约是{best:.1f}页。不需要任何留出的数据：证据自己就在拟合和复杂度之间做了权衡。这就是贝叶斯奥卡姆剃刀。",

    'David MacKay drew the reason in 1992.':
        "1992年，戴维·麦凯把其中的道理画了出来。把一个模型可能生成的每一个数据集排开，画出模型给每一个的概率。每条曲线下的面积都是1。<bookmark mark='a'/>简单的模型，把把握押在少数几个数据集上。灵活的模型几乎什么都能生成，所以给每一个的都只有一点点。<bookmark mark='b'/>对于我们真正看到的数据，中间的那个模型赢了：灵活得足以解释它，又不至于灵活到什么都押。",

    'f"One more test, where we know the answer': "再做一个知道答案的测试：从一条三次曲线上取{len(xp)}个点，加上噪声。用贝叶斯线性回归，拟合各种次数的多项式，从一条水平线一直到12次。<bookmark mark='a'/>下面的图使用另一组不加正则化的最小二乘拟合。在这组参照模型中，次数增加时，训练误差不会上升。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>拟合与复杂度：同样的权衡，从另一面来看，就是第8部分的主题。",

    "f'The evidence peaks at degree {best}, the true": '证据在{best}次时达到峰值，正是真实的次数；而单独的最小二乘参照误差，随次数增加不会上升。',

    "f'The evidence peaks at degree {best}; the true": '证据在{best}次时达到峰值；真实的次数是{true}。单独的最小二乘参照误差，随次数增加不会上升。',

    # ---------------------------------------------------------------- BayesOpt
    'Every model in this series has knobs.':
        "这个系列里的每个模型都有旋钮。这里有一个：Kneser–Ney的折扣D，每一阶都用同一个值。每试一次，就要构建一个模型，再在留出的文本上给它打分：在这里只要几秒，可对一个大型网络来说要好几天。所以我们想用尽可能少的尝试，找到最好的D。<bookmark mark='a'/>贝叶斯优化在这个未知的分数上放一个高斯过程，然后在每个候选点上问：我们能指望它比目前最好的好多少？<bookmark mark='b'/>对高斯分布来说，答案有一个公式，叫作期望改进。一项奖励预测的分数低：利用。另一项奖励带子宽：探索。<bookmark mark='c'/>约纳斯·莫库斯在七十年代提出了这种方法；唐纳德·琼斯和同事在1998年让期望改进成为标准；2012年，贾斯珀·斯努克和同事证明，用它调神经网络，比专家调得还好。",

    '"Here it runs. Two random tries to start.': "这就是它运行的样子。先随机试两次。灰色的带子是高斯过程对分数的信念；下面黄色的曲线是期望改进，每一步都把峰值缩放为一。峰值所在的位置，就是下一步该看的地方。<bookmark mark='a'/>每落下一个新的分数，带子就在那里收紧，下一个要看的地方也跟着移动。它大多朝着低分走去，偶尔也去查一查带子还很宽的地方。<bookmark mark='b'/>{verdict}<bookmark mark='b2'/>{verdict2}<bookmark mark='c'/>探索与利用，是第26部分的老虎机问题换了个样子。DeepMind在2016年那场比赛之前，就是这样调AlphaGo的设置的。",

    "f'After {b['evals']} evaluations it has found":
        "经过{b['evals']}次评估，它找到了D等于{b['best_D']:.2f}，得分{b['best_bits']:.4f}比特，和{b['grid_evals']}次评估的网格搜索一样好。",

    "f'After {b['evals']} evaluations its best is":
        "经过{b['evals']}次评估，它最好的结果是D等于{b['best_D']:.2f}，{b['best_bits']:.4f}比特，而{b['grid_evals']}次评估的网格搜索是{b['grid_best_bits']:.4f}。",

    "f'One tuned discount even beats":
        "一个调出来的折扣，甚至胜过了根据计数的计数估计出的那些折扣，后者是{b['gt_bits']:.4f}：那个公式是一个不错的猜测，但不是最优解。",

    "f'The discounts estimated from counts of counts do as well":
        "根据计数的计数估计出的那些折扣也一样好，{b['gt_bits']:.4f}。",

    # ---------------------------------------------------------------- VI
    'For most models with hidden parts, the exact answer': "对大多数带有隐藏部分的模型来说，精确的答案，也就是隐变量的后验，是一个我们算不出来的形状。<bookmark mark='p'/>后验，就是看到数据之后，我们对那些隐藏的东西的信念：也就是第5部分那种更新过的信念。第5部分用马尔可夫链，从这样的形状中采样。变分推断换了个做法：它从一个简单的家族里，挑出最接近的形状，这里是单个高斯分布，然后用它来代替。这里把两个形状放到有限网格上近似，并在图示窗口内归一化。<bookmark mark='a'/>在什么意义上最接近？用第1部分的KL散度，方向是从q到p。从一个很差的猜测出发，让这个高斯分布顺着下坡滑下去。",

    'It settles on one bump and ignores the other.': "它停在一个鼓包上，不管另一个。这个方向的KL散度，会因为q在p几乎没有概率的地方放了概率而惩罚它，所以q躲进了单独一个众数里，也就是分布的单独一个峰。<bookmark mark='a'/>反过来量，从p到q，拟合出的高斯分布就会盖住两个鼓包，还溢到中间的空白地带。两者都没有错：它们回答的是不同的问题。<bookmark mark='b'/>这一切背后的恒等式是：数据的对数概率，等于一个下界，也就是证据下界ELBO，再加上那个KL散度。ELBO是一个我们算得出来的分数，它永远落在真实值的下方。<bookmark mark='c'/>把它往上推，KL散度就不得不缩小，把q拖向p。第20部分的变分自编码器，正是这样训练的。",

    'Where does that identity come from?':
        "这个恒等式是从哪里来的？三行就够了。数据的对数概率与z无关，所以在q下对它求平均，什么也不会改变。<bookmark mark='a'/>按贝叶斯法则，p(x)等于联合分布除以后验。<bookmark mark='b'/>乘上再除以q，把对数拆成两部分。<bookmark mark='c'/>第一部分是ELBO，也就是证据下界；第二部分是从q到真实后验的KL散度。<bookmark mark='d'/>这又是第4章EM的那个下界。EM能让KL变成零，因为那里的后验算得出来。若限制了可用的分布家族，变分推断即使找到它能表示的最佳q，也可能留下正的差距。",

    'f"Now a model where we can check everything.': "现在来看一个什么都能核对的模型。取奥斯汀的{d['N']}页书，看它们用“the”的频率。把它建模成一条均值未知、精度也未知的钟形曲线，配上常用的共轭先验，这样精确的后验是知道的：这是它的等高线。<bookmark mark='a'/>变分推断假装我们算不出它，去找q(μ)乘q(τ)：两个独立的因子，也就是平均场家族。<bookmark mark='b'/>坐标上升一次更新一个因子：一个变量最好的log q，是对另一个变量取平均后的对数联合分布。<bookmark mark='c'/>一开始让q窄得过分。每一轮都提高ELBO。这里的{preview_updates}次早期更新只是预览，不是收敛检验。<bookmark mark='d'/>现在跳到保存的第{last_sweep}轮做核对。数据的精确对数概率是{d['logp']:.2f}；ELBO加上数值积分得到的KL，吻合到小数点后第三位。<bookmark mark='e'/>{verdict}",

    'f"Mean field is a little too sure of itself': "平均场有点过于自信：q给μ的分散程度是{sdq:.2f}，而真实值是{d['sd_mu_true']:.2f}，因为它忽略了μ和τ之间的相互牵连。",

    'f"Here q\'s spread for mu': "这里q给μ的分散程度是{sdq:.2f}，真实值是{d['sd_mu_true']:.2f}。",

    'f"CAVI needs expectations in closed form.': "CAVI需要闭式的期望。对神经网络来说根本没有，所以我们改用样本来跟随ELBO的梯度。<bookmark mark='a'/>老办法叫得分函数法，用f乘上log q的梯度。它是无偏的，但噪声很大。<bookmark mark='b'/>2013年，迪德里克·金马和马克斯·韦林，以及几个月后独立提出的达尼洛·雷森德和同事，把样本写成均值加噪声，这样梯度就能穿过样本本身流过去：这就是重参数化技巧。<bookmark mark='c'/>边缘分箱也包括落在显示范围之外的估计。期望一样，平均起来答案也一样；但这里它的分散程度是{r['rep_sd']:.1f}，而得分函数法是{r['score_sd']:.1f}，方差小了{r['ratio']:.0f}倍。",


    # ---------------------------------------------------------------- Outro


    "Here are six problems, from Pearson's line":
        "这里有六道习题，从皮尔逊的直线，到珀尔的do算子。请在这里暂停，自己做一做；完整的解答在这一部分的讲义里。",

    'Next time: the deepest question in machine learning.':
        "下一次：机器学习里最深刻的问题。一个模型拟合了它的训练数据；凭什么它在别的数据上也管用？<bookmark mark='a'/>偏差与方差，瓦普尼克与切尔沃年基斯的界，能把随机标签背下来的网络，还有那条先下降、再上升、然后又下降的曲线。",

    "Bishop's Pattern Recognition and Machine Learning covers most of this part":
        "毕晓普的《模式识别与机器学习》涵盖了这一部分的大部分内容；拉斯穆森和威廉斯的书讲高斯过程，珀尔的《因果论》讲因果。感谢观看，第8部分见。",
    "A common alternative avoids forming the covariance matrix: part three's singular value decomposition of the data itself. Z equals U, sigma, V transpose. <bookmark mark='a'/> The rows of V transpose are the principal directions, and each singular value, squared and divided by the number of pages, is an eigenvalue. <bookmark mark='b'/> On the pages the two agree to the last digits of floating point. Working on Z directly is also more accurate: squaring the data to make C squares its condition number.": "一种常见的替代方法，不必构造协方差矩阵：直接对数据做第3部分的奇异值分解。Z等于U、Σ、V转置。<bookmark mark='a'/>V转置的各行，就是主方向；每个奇异值，平方之后除以书页数，就是一个特征值。<bookmark mark='b'/>在这些书页上，两者一直吻合到浮点数的最后几位。直接在Z上算还更准确：把数据平方得到C，会把条件数也平方。",
    'f"Seen along the first three directions, the authors already sit apart. <bookmark mark=\'a\'/> A single cut along the first direction sorts {100 * p[\'split\']:.0f} percent of these same pages correctly. The directions were fitted without author labels; we used the labels to choose the sign and this cut. PCA is part three\'s eigenvectors, put to work: the cheapest way to see a cloud of high-dimensional data."': "沿着前三个方向看，两位作者已经各占一边了。<bookmark mark='a'/>只沿第一个方向切一刀，就能把{100 * p['split']:.0f}%的同一组书页分对。方向的拟合没有用作者标签；但方向的正负，以及这一刀的位置，是用标签选的。主成分分析，简称PCA，正是让第3部分的特征向量派上了用场：要看清一团高维数据，这是最省事的办法。",
    "PCA finds directions, but it isn't a probability model: it can't say how likely a new page is. In the late nineteen nineties, Michael Tipping and Christopher Bishop, and independently Sam Roweis, gave it one. <bookmark mark='a'/> Imagine each page begins as a few hidden numbers, z, drawn from a standard bell curve. <bookmark mark='b'/> A matrix W maps them up into the seventy word rates, onto a flat sheet through the data. <bookmark mark='c'/> Then noise of the same size in every direction blurs the sheet. <bookmark mark='d'/> Add it up, and a page is Gaussian, with covariance W W transpose plus sigma squared times the identity: a few big directions, and a fog around them.": "PCA能找到方向，但它不是概率模型：它说不出一页新书出现的可能性有多大。二十世纪九十年代末，迈克尔·蒂平和克里斯托弗·毕晓普，以及独立工作的萨姆·罗维斯，把它变成了一个模型。<bookmark mark='a'/>设想每一页都起源于几个隐藏的数z，它们从标准的钟形曲线里抽出来。<bookmark mark='b'/>一个矩阵W把它们映射到70个词频上，落在穿过数据的一张平面上。<bookmark mark='c'/>然后，在每个方向上大小都一样的噪声，把这张平面弄模糊。<bookmark mark='d'/>合起来，一页书就服从高斯分布，协方差是W乘W转置，再加上σ平方乘单位矩阵：几个大的方向，外加一层雾。",
    'f"A likelihood lets us choose how many hidden directions to keep. Fit on part six\'s {p[\'n_train\']} training pages, use the {p[\'n_test\']} held-out pages for validation and model selection. <bookmark mark=\'a\'/> On the training pages, adding directions cannot lower the maximum likelihood, though ties are possible. <bookmark mark=\'b\'/> " + verdict': "有了似然，就能选择保留多少个隐藏方向。在第6部分的{p['n_train']}页训练书页上拟合，用留出的{p['n_test']}页做验证和模型选择。<bookmark mark='a'/>在训练书页上，增加方向不会降低最大似然，但可能持平。<bookmark mark='b'/>{verdict}",
    "Probabilistic PCA sits in a family. <bookmark mark='a'/> Charles Spearman's factor analysis, from 1904, is the same model with a separate noise level for every variable. <bookmark mark='b'/> Probabilistic PCA ties them into one, which is why the eigenvectors fall out. <bookmark mark='c'/> And replace W with a neural decoder and add a learned variational encoder, and you reach the variational autoencoder of part twenty: the same hidden z, the same picture, a curved sheet instead of a flat one.": "概率PCA属于一个家族。<bookmark mark='a'/>查尔斯·斯皮尔曼1904年的因子分析，是同一个模型，只是每个变量各有自己的噪声水平。<bookmark mark='b'/>概率PCA把它们统一成一个，所以特征向量才会自然地冒出来。<bookmark mark='c'/>再把W换成神经网络解码器，并加上学习到的变分编码器，就走到了第20部分的变分自编码器：同样的隐藏z，同样的图，只是平面换成了曲面。",
    '"Plot the two microphones against each other, moment by moment, and the mixing shows as a slanted, squashed shape. <bookmark mark=\'a\'/> First, whiten: chapter one\'s principal components, rescaled to unit spread. The two outputs are now uncorrelated. But they\'re still mixed: turn this white cloud by any angle, and it stays uncorrelated, so correlation alone can never tell us which way is right. <bookmark mark=\'b\'/> The central limit theorem motivates looking for non-Gaussian directions in mixtures of independent signals. Here the contrast is excess kurtosis: for a centered, unit-variance output, the fourth moment minus three. A Gaussian gives zero, though zero alone does not prove Gaussianity. " + clt_say + f" <bookmark mark=\'c\'/> So turn the direction until the output is as far from Gaussian as possible. Aapo Hyvärinen\'s FastICA does it with a fixed-point step; here we record {d[\'iters\']} fixed-point steps."': "把两个麦克风的信号对着画出来，一个时刻一个点，混合就表现为一个歪斜、压扁的形状。<bookmark mark='a'/>第一步，白化：也就是第1章的主成分，再缩放到单位分散。两个输出现在不相关了。但它们仍然是混在一起的：把这团白化后的点转任意一个角度，它都仍然不相关，所以光靠相关性，永远说不出哪个方向才对。<bookmark mark='b'/>中心极限定理启发我们，在独立信号的混合中寻找非高斯方向。这里的对比量是超额峰度：输出先中心化并缩放到单位方差，再取四阶矩减3。高斯分布给出0，但仅仅等于0，并不能证明它是高斯分布。{clt_say}<bookmark mark='c'/>所以就转动方向，直到输出离高斯分布越远越好。阿波·许韦里宁的FastICA用一个不动点迭代来做这件事，这里记录了{d['iters']}次不动点迭代。",
    'f"Then again: E, M, E, M. <bookmark mark=\'a\'/> Here the exact posterior E step and the constrained M step cannot lower the same likelihood. Each covariance has a fixed eigenvalue floor, and the M step maximizes the bound within that constraint. <bookmark mark=\'b\'/> By the last displayed round, the pages each bell claims match the true authors {100 * g[\'agree\']:.0f} percent of the time. Nobody told it there were authors at all. EM applies to many hidden-variable models when its E and M steps can be computed; it\'s the next chapter\'s engine too."': "然后再来：E、M、E、M。<bookmark mark='a'/>这里，取精确后验的E步和带约束的M步，不会降低同一个似然。每个协方差都有固定的特征值下限，M步在这个约束内最大化下界。<bookmark mark='b'/>在最后显示的一轮，每条曲线认领的书页，有{100 * g['agree']:.0f}%与真实作者一致。没有人告诉过它，这些书页还有作者之分。只要E步和M步能够计算，EM就适用于许多带隐藏变量的模型；它也是下一章的引擎。",
    "When does EM avoid going downhill? Use the exact posterior in E, and do not lower the same bound in M. Write the log-likelihood as a sum over the hidden choice z: which bell made this point. <bookmark mark='a'/> Multiply and divide by any distribution q over z. <bookmark mark='b'/> The log of an average is at least the average of the logs: that's Jensen's inequality, because the log curves downward. So we get a lower bound, B, that we can compute. <bookmark mark='c'/> How far below? The gap is exactly a KL divergence, between q and the posterior over z. It vanishes when q is the posterior, and that is the E step: it makes the bound touch. <bookmark mark='d'/> The M step then maximizes the bound over the parameters. Chain the three facts: the new likelihood is above the bound, the bound went up, and it started touching. The likelihood can never fall under those conditions. This also covers a generalized EM step that increases the bound without maximizing it. That's the principle in Dempster, Laird and Rubin's 1977 paper.": "EM在什么条件下不会走下坡？E步用精确后验，M步不降低同一目标的下界。把对数似然写成对隐藏选择z的求和：是哪条钟形曲线生成了这个点。<bookmark mark='a'/>乘上再除以z上的任意一个分布q。<bookmark mark='b'/>平均值的对数，至少等于对数的平均值：这是詹森不等式，因为对数函数向下弯。于是我们得到了一个算得出来的下界B。<bookmark mark='c'/>它比真实值低多少？差距恰好是一个KL散度，介于q和z的后验之间。当q就是后验时，差距消失，这正是E步：它让下界贴上来。<bookmark mark='d'/>然后M步在参数上把下界推到最大。把三件事串起来：新的似然在下界之上，下界升高了，而且一开始是贴着的。在这些条件下，似然不会下降。广义EM只需提高下界，不必把它推到最大，也符合这个原则。这就是登普斯特、莱尔德和鲁宾1977年论文中的原理。",
    "Here's that bound for real, on the pages. Each panel follows a straight line through the parameters, from one round's bells to the next round's. The yellow curve is the log-likelihood. <bookmark mark='a'/> The green curve is the bound that round's E step built: always below, touching at the start. <bookmark mark='b'/> The M step jumps to the top of the green curve, and the yellow curve, above it, can only be higher there. <bookmark mark='c'/> The first step, from a poor start, is a leap; later displayed steps are small. Each maximizing update raises the same bound within the feasible set; these closed-form updates need no gradient learning rate.": "这是那个下界的真实样子，就在这些书页上。每个面板沿着参数空间里的一条直线，从一轮的钟形曲线走到下一轮的。黄色曲线是对数似然。<bookmark mark='a'/>绿色曲线是那一轮的E步构造出来的下界：始终在下方，在起点处贴住。<bookmark mark='b'/>M步跳到绿色曲线的顶点，而在它上方的黄色曲线，在那里只会更高。<bookmark mark='c'/>第一步从一个很差的起点出发，是一大跃；后面显示的步子较小。每次最大化，都在可行范围内提高同一个下界；这些闭式更新不需要梯度学习率。",
    'f"Now make EM\'s choices hard. Instead of soft colours, each page joins whichever centre is nearest; then each centre moves to the mean of its pages. That\'s k-means, Stuart Lloyd\'s algorithm from Bell Labs in 1957. <bookmark mark=\'a\'/> From the same poor start, we display {km[\'iters\']} recorded rounds, and the average squared distance never rises. <bookmark mark=\'b\'/> This is the small-variance limit of a Gaussian-mixture EM model: take round, equal-weight bells and take their width toward zero: points with a unique nearest centre make hard choices, while exact distance ties can remain soft. At the smallest width shown, {100 * hard[-1]:.0f} percent of pages have responsibility above ninety-nine percent. <bookmark mark=\'c\'/> " + verdict': "现在把EM的选择变成硬的。不再用介于两色之间的颜色，每一页直接归到离它最近的中心；然后每个中心移到它那些书页的平均位置。这就是k均值，斯图尔特·劳埃德1957年在贝尔实验室提出的算法。<bookmark mark='a'/>从同一个很差的起点出发，我们显示了{km['iters']}轮记录，平均平方距离从不增加。<bookmark mark='b'/>这是高斯混合EM模型的小方差极限：取一样大、权重相等的球形钟形曲线，让宽度趋于0。最近中心唯一的点，会作出硬选择；距离恰好相同的点，仍可能保留软分配。在显示的最小宽度下，{100 * hard[-1]:.0f}%的书页，其责任度超过99%。<bookmark mark='c'/>{verdict}",
    'f"We cut the thirty novels into {l[\'D\']:,} sections of {l[\'seg\']:,} words, keep the {l[\'V\']:,} commonest words that aren\'t names or little function words, and ask for twelve topics. <bookmark mark=\'a\'/> The topics start as the words of a few random sections: noise. Blei\'s original method fits them by variational EM, which chapter sixteen will explain: an E step that guesses each section\'s mix, and an M step that rebuilds each topic from the words assigned to it. <bookmark mark=\'b\'/> Watch six of the topics take shape, alongside the bound scored after each round. {rise}"': "我们把30部小说切成{l['D']:,}段，每段{l['seg']:,}个词，保留最常见的{l['V']:,}个词，去掉人名和那些小小的虚词，然后要求得到12个主题。<bookmark mark='a'/>这些主题一开始只是几段随机文本里的词：一片噪声。布莱最初的方法用变分EM来拟合，第16章会解释它：E步猜测每一段的主题配比，M步根据分到每个主题的词，重建这个主题。<bookmark mark='b'/>看着其中6个主题逐渐成形。同时看每轮结束后计算的下界。{rise}",
    'f"On these validation pages, {best} hidden directions score {score:.1f} nats per page, {comparison} the full covariance\'s {full:.1f}. We used these pages to choose k, so this is not a fresh test. This comparison does not identify which directions are true signal."': '在这些验证书页上，{best}个隐藏方向得到每页{score:.1f}奈特，{comparison}完整协方差的{full:.1f}奈特。我们用同一组书页选择k，所以这不是一次新的测试。这个比较不能识别哪些方向是真实信号。',
    'f"It matches the authors {100 * agreement:.0f} percent of the time, {comparison} EM\'s {100 * em_agreement:.0f} percent. These are the agreements in this run, not a general ranking of the algorithms."': '它与作者吻合的比例是{100 * agreement:.0f}%，{comparison}EM的{100 * em_agreement:.0f}%。这只是本次运行的吻合率，不是对两种算法的一般排名。',
    "Third: how does the model learn A and B from letters alone? It's chapter four's EM again, and for this model it's called Baum–Welch. <bookmark mark='a'/> Run the forward sweep, and a mirror image, the backward sweep: beta is the probability of the letters still to come, from each state. <bookmark mark='b'/> Alpha times beta, divided by the probability of the whole text, is the chance that the chain was in state i at time t. That's the E step's soft colouring, one per letter. <bookmark mark='c'/> The same trick gives the chance of each move, from i to j, at each moment. <bookmark mark='d'/> The M step just counts: expected moves from i to j, over expected visits to i; expected emissions of each letter, over expected visits. For transitions, leave out the final time, which has no outgoing move. Exact E and M steps cannot decrease the likelihood; at a fixed point it stays unchanged.": "第三个问题：模型怎样只从字母中学出A和B？这又是第4章的EM，用在这个模型上，它叫鲍姆–韦尔奇算法。<bookmark mark='a'/>先做前向扫描，再做一个镜像的后向扫描：β是从每个状态出发，后面那些字母出现的概率。<bookmark mark='b'/>α乘β，除以整段文本的概率，就是链在时刻t处于状态i的概率。这就是E步的软上色，每个字母一个。<bookmark mark='c'/>同样的办法，给出每一时刻从i到j的每一次转移的概率。<bookmark mark='d'/>M步只是数一数：从i到j的期望转移次数，除以访问i的期望次数；每个字母的期望发射次数，除以期望访问次数。计算转移时要去掉最后一个时刻，因为它没有下一步。精确的E步和M步不会降低似然；到了不动点，似然可以保持不变。",
    'f"The learned emission tables: {partition_voice} <bookmark mark=\'a\'/> From the first state, the chain switches to the second {100 * A[0, 1]:.0f} percent of the time; from the second back to the first, {100 * A[1, 0]:.0f} percent. These are two directional probabilities. Nobody supplied vowel labels. Cave and Neuwirth studied this two-state English-letter experiment in 1980."': "学到的两张发射表是这样的：{partition_voice}<bookmark mark='a'/>从第一个状态转到第二个状态的概率是{100 * A[0, 1]:.0f}%；从第二个回到第一个，是{100 * A[1, 0]:.0f}%。这是两个方向各自的概率。没有人提供元音标签。凯夫与诺伊维尔特在1980年研究过这种英语字母的两状态实验。",
    'f"Our Kneser–Ney tables use up to {d[\'M\']} characters of context. Longer tables become expensive. The novels hold {int(types[1]):,} different pairs of characters, and {int(types[-1]):,} different strings of {len(types)}. But a count is just a search through the text, and searching can be fast. <bookmark mark=\'a\'/> Take every suffix of the text: the text from each position to the end. Here\'s a tiny one. <bookmark mark=\'b\'/> Sort them alphabetically. That\'s a suffix array, from Udi Manber and Gene Myers in 1990. <bookmark mark=\'c\'/> Every occurrence of any string, of any length, is now one contiguous block of the list, found by binary search, and the block\'s size is the count. <bookmark mark=\'d\'/> For the thirty novels that\'s {d[\'n\']:,} suffixes, with {4 * d[\'n\'] / 1000000.0:.1f} decimal megabytes of positions. Our replay searches at most {INF_CAP} characters of context. In 2024 Jiacheng Liu and colleagues combined indexes covering five trillion tokens of public text, and called the resulting unbounded-context model an infinity-gram."': "我们这套Kneser–Ney计数表使用到{d['M']}个字符的上下文，再长的表就会很昂贵。这些小说里有{int(types[1]):,}种不同的两字符组合，还有{int(types[-1]):,}种长度为{len(types)}的不同字符串。可一个计数，不过是在文本里搜一下，而搜索可以很快。<bookmark mark='a'/>取出文本的每一个后缀：从每个位置一直到结尾的那段文本。这是一个很小的例子。<bookmark mark='b'/>按字母顺序把它们排好。这就是后缀数组，由乌迪·曼伯和吉恩·迈尔斯在1990年提出。<bookmark mark='c'/>任何一个字符串，不论多长，它的每一次出现，现在都是列表里连续的一块，用二分查找就能找到，而这一块的大小，就是它的计数。<bookmark mark='d'/>30部小说一共是{d['n']:,}个后缀，位置信息占{4 * d['n'] / 1000000.0:.1f}个十进制兆字节。我们的回放最多搜索{INF_CAP}个字符的上下文。2024年，刘嘉程和同事把覆盖五万亿个公开文本词元的索引组合起来，并把得到的无界上下文模型叫作无穷元模型。",
    'f"Now predict the passage. At each character, take the context before it and extend it to the left, one character at a time, up to {INF_CAP} characters, counting as we go. <bookmark mark=\'a\'/> The first count here is {counts[0]:,}. An extra character can keep the count unchanged or reduce it. At {L} characters, " + last + f" <bookmark mark=\'b\'/> The infinity-gram predicts from the longest context the novels contain: whatever followed it there. <bookmark mark=\'c\'/> Over the Maltese Falcon passage, the longest match is usually about {d[\'median_L\']:.0f} characters, and at most {d[\'max_L\']}: the novels have never seen most of Hammett\'s sentences, but they\'ve seen their pieces."': "现在来预测评分段落。在每个字符处，取它前面的上下文，向左一个字符一个字符地延伸，最多到{INF_CAP}个字符，一路计数。<bookmark mark='a'/>这里第一个计数是{counts[0]:,}。每多加一个字符，计数可能不变，也可能减少。到了{L}个字符时，{last}<bookmark mark='b'/>无穷元模型根据小说里出现过的最长上下文来预测：看那里接下来出现过什么。<bookmark mark='c'/>在《马耳他之鹰》的评分段落上，最长的匹配通常约有{d['median_L']:.0f}个字符，最多{d['max_L']}个：这些小说没见过哈米特的大多数句子，却见过其中的片段。",
    'f"How good is it? On its own, the infinity-gram\'s single most likely next character is right {100 * acc:.0f} percent of the time. <bookmark mark=\'a\'/> But {100 * zero:.0f} percent of the time it gives the true character no chance at all, because it never saw it after that context. One zero, and the bits are infinite. <bookmark mark=\'b\'/> So it\'s mixed with Kneser–Ney, with a weight for each length band and for whether the index has one or several possible next characters. <bookmark mark=\'c\'/> " + verdict + " <bookmark mark=\'d\'/> In Liu\'s paper, a decontaminated 360-billion-token Pile index assigned the true next token probability above one half on 47 percent of held-out Pile tokens: a lower bound on next-token accuracy, separate from the five-trillion-token combined index. Mixing such counts also helped neural models. These indexes can trace generated phrases back to matching training documents."': "它有多好？单靠自己，无穷元模型给出的最可能下一个字符，有{100 * acc:.0f}%的时候是对的。<bookmark mark='a'/>但有{100 * zero:.0f}%的时候，它给真实字符零概率，因为它从没在那个上下文后面见过这个字符。只要一个零，比特数就是无穷大。<bookmark mark='b'/>所以把它和Kneser–Ney混合：每个长度区间分别设权重，还区分索引里只有一种、还是多种可能的后续字符。<bookmark mark='c'/>{verdict}<bookmark mark='d'/>刘等人的论文里，去污染后的Pile索引包含3600亿个词元；对留出的Pile文本，有47%的词元，其真实下一个词元获得了超过二分之一的概率。这是下一词元准确率的一个下界，和五万亿词元的组合索引是两件事。混合这些计数也帮助了神经模型。这样的索引还可以把生成的短语追溯到相匹配的训练文档。",
    'f"Back to part one\'s scoreboard. The best counting model on that scored passage used {best1} characters of context and reached {p1[best1]:.2f} bits per character on the passage. <bookmark mark=\'a\'/> Longer contexts should help, but they\'re rare: most long contexts in the passage appeared only a handful of times in thirty novels, if at all. Part one\'s best passage score is at {best1} characters. <bookmark mark=\'b\'/> {trend}"': "回到第1部分的记分牌。在那个评分段落上，最好的计数模型用了{best1}个字符的上下文，得到每字符{p1[best1]:.2f}比特。<bookmark mark='a'/>更长的上下文本该有帮助，但它们很罕见：测试段落里大多数长的上下文，在30部小说里只出现过寥寥几次，甚至根本没出现过。第1部分在这个段落上的最佳分数，出现在{best1}个字符处。<bookmark mark='b'/>{trend}",
    'f"Reinhard Kneser and Hermann Ney\'s smoothing, from 1995, has two ideas. <bookmark mark=\'a\'/> First, absolute discounting: shave the fixed discount off every count you\'ve seen, <bookmark mark=\'c\'/> and use the savings to back off to a shorter context, one character fewer: blend the two. <bookmark mark=\'b\'/> Second, judge the shorter contexts by their variety. In the novels, \'{d[\'word\']}\' appears {d[\'word_count\']:,} times, but its number of distinct predecessors is {d[\'word_prev\']}; its most common predecessor is \'{d[\'word_top_prev\']}\'. \'{d[\'other\']}\' is about as common, and follows {d[\'other_prev\']:,} different words. <bookmark mark=\'d\'/> After an unfamiliar word, \'{d[\'other\']}\' is the far better guess. So the shorter contexts count how many different contexts something follows, not how often it appears."': "莱因哈德·克内泽尔和赫尔曼·奈伊1995年提出的平滑方法，有两个想法。<bookmark mark='a'/>第一，绝对折扣：从每一个见过的计数里，削掉那个固定的折扣，<bookmark mark='c'/>再用省下来的量，回退到少一个字符的上下文，把两者混合起来。<bookmark mark='b'/>第二，用多样性来衡量较短的上下文。在这些小说里，“{d['word']}”出现{d['word_count']:,}次，却只跟在{d['word_prev']}个不同的词后面；它最常见的前一个词是“{d['word_top_prev']}”。“{d['other']}”的常见程度差不多，却跟在{d['other_prev']:,}个不同的词后面。<bookmark mark='d'/>遇到一个不熟悉的前词时，“{d['other']}”就是更好的猜测。所以较短的上下文，数的是一个东西跟在多少种不同的上下文后面，而不只是出现了多少次。",
    'f"With {k[\'best\']} characters of context, selected on the validation books, Kneser–Ney reaches {k[\'best_bits\']:.2f} bits per character on the passage. <bookmark mark=\'a\'/> For two decades, from speech recognition to machine translation, a Kneser–Ney model was the language model in the noisy channel. Stanley Chen and Joshua Goodman\'s careful comparison in 1998 found a modified Kneser–Ney variant best among the methods they tested. But why stop at {k[\'best\']} characters?"': "用验证集里的书选出{k['best']}个字符的上下文后，Kneser–Ney在评分段落上达到每字符{k['best_bits']:.2f}比特。<bookmark mark='a'/>有二十年，从语音识别到机器翻译，有噪信道里的语言模型都是Kneser–Ney这一类。斯坦利·陈和乔舒亚·古德曼1998年的细致比较发现，在他们测试的方法里，一种改进版Kneser–Ney表现最好。但为什么要停在{k['best']}个字符呢？",
    'f"Hidden states can also unfold in time. A hidden Markov model has a state we can\'t see, moving like part five\'s Markov chain, with transition probabilities A. <bookmark mark=\'a\'/> At every step the state emits something we can see, a letter, from its own table of chances, B. <bookmark mark=\'b\'/> Here is a two-state model of the letters in the books; we\'ll train it in the next chapter. {preference} <bookmark mark=\'c\'/> Leonard Baum and his colleagues worked out the mathematics in the late 1960s, at the Institute for Defense Analyses. Three questions follow. How likely is a sentence? Which states produced it? And how do we learn A and B?"': "隐藏的状态，也可以随时间展开。隐马尔可夫模型有一个我们看不见的状态，像第5部分的马尔可夫链那样移动，转移概率是A。<bookmark mark='a'/>每一步，状态都发射出一个我们看得见的东西，一个字母，按照它自己的一张概率表B。<bookmark mark='b'/>这是书中字母的一个两状态模型，我们下一章再训练它。{preference}<bookmark mark='c'/>伦纳德·鲍姆和同事在六十年代末，在美国国防分析研究所，把其中的数学弄清楚了。接下来有三个问题。一个句子有多大可能？是哪些状态生成了它？以及，A和B怎样学出来？",
    'f"First: how likely is a sentence? Summing over every possible sequence of hidden states would take two to the power of its length. The forward algorithm does it in one sweep. <bookmark mark=\'a\'/> Lay the states out as a lattice, one column per letter. Let alpha of a state be the probability of the letters so far, ending in that state. <bookmark mark=\'b\'/> By the Markov property, each alpha is a sum over the state before: its alpha, times the chance of the move, times the chance of the new letter. <bookmark mark=\'c\'/> Sweep left to right, and the last column adds up to the probability of the letters. For \'there\' and a space, that\'s about {tot * 10000000.0:.1f} in ten million, exactly the sum over all {2 ** T} paths. For the whole {f[\'n\']}-letter sentence, the sum has two to the {f[\'n\']} terms; the sweep takes a few hundred multiplications. <bookmark mark=\'d\'/> Part twenty-three\'s speech recognizers train with CTC, which runs a related forward sum over the allowed ways of lining up sound with text, including blank labels."': "第一个问题：一个句子有多大可能？把每一种可能的隐状态序列都加起来，要做2的句子长度次方那么多项。前向算法一遍就能做完。<bookmark mark='a'/>把状态排成一个网格，每个字母一列。设一个状态的α，是到目前为止这些字母出现、并且停在这个状态的概率。<bookmark mark='b'/>按马尔可夫性质，每个α都是对前一个状态的求和：它的α，乘上转移的概率，再乘上新字母的概率。<bookmark mark='c'/>从左到右扫过去，最后一列加起来，就是这些字母的概率。对“there”加一个空格来说，大约是一千万分之{tot * 10000000.0:.1f}，恰好等于对全部{2 ** T}条路径的求和。对整个{f['n']}个字母的句子，那个求和有2的{f['n']}次方项；而扫一遍只要几百次乘法。<bookmark mark='d'/>第23部分的语音识别器用CTC来训练，它用相关的前向求和，遍历声音和文本之间允许的对齐方式，其中还包括空白标签。",
    "Here's Shannon's sentence from part one, with one most likely complete hidden-state sequence. <bookmark mark='a'/> These colours come from the whole path, using both letter emissions and state transitions, rather than choosing each state's label independently. Nobody told the model what a vowel is.": "这是第1部分香农的那个句子，配上一条最可能的完整隐状态序列。<bookmark mark='a'/>这些颜色来自整条路径，同时考虑字母的发射概率和状态的转移概率，而不是给每个位置单独挑一个状态。从来没有人告诉过模型什么是元音。",
    'f"Here\'s IBM\'s Model 1, on a tiny parallel corpus of {d[\'n_train\']} French and English sentences that we wrote. <bookmark mark=\'a\'/> The model has one table: t of e given f, the chance that a French word turns into an English word. Here we condition on the English length, and learn the direct English-given-French table, reversing the earlier noisy-channel direction. Each English word chooses equally among the French positions and NULL; the normalization is one over the number of choices, for every English word. Comparing different output lengths also needs a length prior. The alignments are hidden. <bookmark mark=\'b\'/> EM again. Start with every translation equally likely. <bookmark mark=\'c\'/> In the E step, each English word spreads its credit over the French words in its sentence; in the M step, the table is rebuilt from that credit. Because \'chat\' appears exactly where \'cat\' does, the credit piles up, and \'le\' is pushed toward \'the\', which frees \'chat\'. <bookmark mark=\'d\'/> After thirty rounds, \'chat\' becomes \'{best[3][0]}\' with probability {best[3][1]:.2f}, and the alignment of this sentence is sharp, though Model 1 can\'t tell the two \'le\'s apart: it has no idea of word order."': "这是IBM的模型1，用在我们自己写的小型平行语料上，一共{d['n_train']}句法文和英文。<bookmark mark='a'/>模型只有一张表t，也就是给定法文词f时，英文词e的概率。这里先固定英文的长度，学习从法文到英文的直接概率表，方向和前面有噪信道的例子相反。每个英文词在法文的各个位置和NULL之间等概率选择；每生成一个英文词，都要除以可选位置的数量，作归一化。要比较不同的输出长度，还需要长度的先验。谁和谁对齐，是隐藏的。<bookmark mark='b'/>又是EM，一开始，每种翻译都一样可能。<bookmark mark='c'/>在E步，每个英文词把功劳分给它所在句子里的各个法文词；在M步，根据这些功劳重建概率表。因为“chat”恰好出现在“cat”出现的地方，功劳就越积越多；而“le”被推向“the”，这又把“chat”解放了出来。<bookmark mark='d'/>30轮之后，“chat”以{best[3][1]:.2f}的概率变成“{best[3][0]}”，这个句子的对齐也变清晰了，不过模型1分不清那两个“le”：它对词序一无所知。",
    'The first emission table favours spaces and vowels, the second consonants.': '第一张发射表偏爱空格和元音，第二张偏爱辅音。',
    'The two emission tables learn different letter preferences; this fit does not exactly split vowels from consonants.': '两张发射表学到了不同的字母偏好；这次拟合并没有把元音和辅音精确分开。',
    'The first emission table favours space and a, e, i, o and u; the second favours consonants.': '第一张发射表偏爱空格和a、e、i、o、u，第二张偏爱辅音。',
    'This fit learns different letter preferences, but not an exact split of vowels and consonants.': '这次拟合学到了不同的字母偏好，但不是元音和辅音的精确划分。',
    "Across these measured orders, Kneser–Ney's passage score never rises.": '在这些实测阶数中，Kneser–Ney在这个段落上的分数没有上升。',
    'Kneser–Ney improves some of these scores, but more context does not improve every measured order.': 'Kneser–Ney改善了其中一些分数，但增加上下文，并没有让每一个实测阶数都变好。',
    'this context appears exactly once.': '这个上下文恰好出现一次。',
    "f'this context still appears {counts[-1]} times.'": '这个上下文仍然出现{counts[-1]}次。',
    'f"Mixed with Kneser–Ney using these held-out weights, it gives {mix:.3f} bits per character, against Kneser–Ney\'s {kn:.3f}: a small gain, and the scoreboard\'s last counting row."': '用这些在留出文本上拟合的权重，与Kneser–Ney混合，得到每字符{mix:.3f}比特，而Kneser–Ney是{kn:.3f}：一点小小的进步，也是记分牌上最后一行计数模型。',
    'One more step. Our CAVI example fit one shared posterior': "再走一步。前面的CAVI例子，对整组书页拟合了一个共享后验。对于局部隐变量，例如第5章每篇文档的混合比例，推断则会为每个样例单独拟合一个q。<bookmark mark='a'/>换个做法，训练一个网络，也就是编码器，让它对任何输入都输出q的参数：这叫摊销推断。<bookmark mark='b'/>用重参数化技巧采样z，再把它解码回去，用ELBO同时训练两个网络。<bookmark mark='c'/>这就是变分自编码器，第20部分会搭一个。同一个下界，还在第21部分训练扩散模型。",
    'f"Here are part six\'s {p[\'n\']:,} pages again, each a point in {p[\'d\']} dimensions, seen along the three directions in which they vary most. But this time, nobody tells us who wrote which. <bookmark mark=\'a\'/> Can the data reveal its own hidden structure? <bookmark mark=\'b\'/> A model that assumes there are two hidden sources, and fits them with no labels at all, finds two groups. <bookmark mark=\'c\'/> And they\'re the two authors: {100 * g[\'agree\']:.0f} percent of the pages land with the right one."': "这又是第6部分的{p['n']:,}页，每一页都是{p['d']}维空间里的一个点，这里是沿着它们变化最大的三个方向看过去的样子。不过这一次，没有人告诉我们哪一页是谁写的。<bookmark mark='a'/>数据能自己揭示出隐藏的结构吗？<bookmark mark='b'/>有一个模型，假设背后有两个隐藏的来源，在完全没有标签的情况下去拟合它们，结果找出了两组。<bookmark mark='c'/>而这两组，正是那两位作者：{100 * g['agree']:.0f}%的书页，都落到了正确的作者那一组。",
    "Let's take stock. <bookmark mark='pca'/> Principal components are the covariance's eigenvectors: the line of greatest spread, and the line closest to the data, at once; add noise, and they become a probability model. <bookmark mark='ica'/> Independent components unmixed two voices. <bookmark mark='em'/> With an exact posterior E step and an M step that never lowers the same bound, EM cannot lower the likelihood. K-means is its small-variance limit, <bookmark mark='topics'/> and a topic model is a mixture of mixtures. <bookmark mark='hmm'/> Hidden Markov models found vowels with no labels, <bookmark mark='alignment'/> and EM's alignments started statistical translation. <bookmark mark='counting'/> Good–Turing and Kneser–Ney counted what hadn't been seen, and a suffix array counted contexts of any length. Graphs gave us independence, <bookmark mark='graphs'/> message passing, and, <bookmark mark='causes'/> with do, cause and effect. <bookmark mark='gp'/> Gaussian processes put probabilities on whole functions, chose their own length scale by Occam's razor, <bookmark mark='optimization'/> and chose where to look next. <bookmark mark='vi'/> And variational inference turned an impossible posterior into an optimization.": "盘点一下。<bookmark mark='pca'/>主成分是协方差矩阵的特征向量：分散最大的直线，也是离数据最近的直线；加上噪声，就成了概率模型。<bookmark mark='ica'/>独立成分分开了两个声音。<bookmark mark='em'/>当E步取精确后验、M步不降低同一个下界时，EM就不会降低似然。k均值是它的小方差极限，<bookmark mark='topics'/>主题模型是混合的混合。<bookmark mark='hmm'/>隐马尔可夫模型无师自通地发现了元音，<bookmark mark='alignment'/>EM的对齐开启了统计翻译。<bookmark mark='counting'/>Good–Turing和Kneser–Ney数出了没见过的东西，后缀数组数出了任意长的上下文。图给了我们独立性、<bookmark mark='graphs'/>消息传递，加上<bookmark mark='causes'/>do，还有因果。<bookmark mark='gp'/>高斯过程给函数赋予概率，靠奥卡姆剃刀选长度尺度，还<bookmark mark='optimization'/>选出下一步看哪里。<bookmark mark='vi'/>变分推断把算不出的后验，变成了优化问题。",
    "Hidden parts come back everywhere. <bookmark mark='alignment'/> Model 1's alignments return as attention, a soft alignment learned inside the network, in part thirteen. <bookmark mark='state'/> State-space models, in part fifteen, carry a hidden state through time, <bookmark mark='experts'/> and mixtures of experts, in part sixteen, are mixtures with a learned way of choosing. <bookmark mark='forward'/> The forward algorithm trains speech recognizers in part twenty-three. <bookmark mark='gp'/> An infinitely wide network is a Gaussian process, in part twelve. <bookmark mark='elbo'/> The ELBO and the reparameterization trick train autoencoders and diffusion models. <bookmark mark='causes'/> Setting a network's activations by hand is the do operator, in part thirty. <bookmark mark='counting'/> And Kneser–Ney is the row the first neural language model has to beat, in part nine.": "隐藏的部分会处处再现。<bookmark mark='alignment'/>模型1的对齐，在第13部分变成注意力，一种学出来的软对齐。<bookmark mark='state'/>第15部分的状态空间模型，带着隐状态穿过时间；<bookmark mark='experts'/>第16部分的混合专家，是会学着选择的混合模型。<bookmark mark='forward'/>前向算法在第23部分训练语音识别器。<bookmark mark='gp'/>无限宽的网络就是高斯过程，见第12部分。<bookmark mark='elbo'/>ELBO和重参数化技巧训练自编码器和扩散模型。<bookmark mark='causes'/>手动设定激活值就是do算子，见第30部分。<bookmark mark='counting'/>而Kneser–Ney，是第9部分第一个神经语言模型要打败的那一行。",
    'In this run the recorded bound never decreases.': '这次运行记录的下界没有下降。',
    'With our smoothing and finite updates, this recorded bound can decrease; the plot shows the measured trace.': '带平滑的有限次更新可能降低这个下界；图中画的是实测轨迹。',
}

PHRASES = {
    'and, like every EM, it never falls': '而且和所有的EM一样，从不下降',
    'open surgery': '开放手术',
    'the keyhole method': '微创手术',
    'Pride and Prejudice': '《傲慢与偏见》',
    'A Tale of Two Cities': '《双城记》',
    'Moby Dick': '《白鲸》',
    'The Adventures of Sherlock Holmes': '《福尔摩斯探案集》',
    'Great Expectations': '《远大前程》',
    'Frankenstein': '《弗兰肯斯坦》',
    'Dracula': '《德古拉》',
    'The Picture of Dorian Gray': '《道林·格雷的画像》',
    'Jane Eyre': '《简·爱》',
    'Middlemarch': '《米德尔马契》',
    'Emma': '《爱玛》',
    'Wuthering Heights': '《呼啸山庄》',
    'The Hound of the Baskervilles': '《巴斯克维尔的猎犬》',
    'The Count of Monte Cristo': '《基督山伯爵》',
    'War and Peace': '《战争与和平》',
    'Treasure Island': '《金银岛》',
    'Jekyll and Hyde': '《化身博士》',
    'The War of the Worlds': '《世界大战》',
    'The Time Machine': '《时间机器》',
    'Heart of Darkness': '《黑暗之心》',
    'Huckleberry Finn': '《哈克贝利·费恩历险记》',
    'Tom Sawyer': '《汤姆·索亚历险记》',
    'Crime and Punishment': '《罪与罚》',
    'The Brothers Karamazov': '《卡拉马佐夫兄弟》',
    'The Great Gatsby': '《了不起的盖茨比》',
    'The Yellow Wallpaper': '《黄色墙纸》',
    'The Awakening': '《觉醒》',
    'Little Women': '《小妇人》',
    'A Christmas Carol': '《圣诞颂歌》',
    'Ulysses': '《尤利西斯》',
    'higher than': '高于',
    'lower than': '低于',
    'equal at the shown precision to': '按图示精度，与之相同的是',
    'In this run the recorded bound never decreases.': '这次运行记录的下界没有下降。',
    'With our smoothing and finite updates, this recorded bound can decrease; the plot shows the measured trace.': '带平滑的有限次更新可能降低这个下界；图中画的是实测轨迹。',
}
