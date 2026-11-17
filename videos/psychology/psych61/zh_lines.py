"""Chinese narration for psych61: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第61部分：下一代心理学'

CHAPTERS = {
    'Hook': '一百六十支团队',
    'Predict': '1. 在你身上：一个实验空间，以及四个数字',
    'Explain': '2. 解释与预测',
    'Teams': '3. 大团队科学',
    'Scale': '4. 数以百万计的参与者',
    'Who': '5. 谁被抽样',
    'Integrative': '6. 整合式实验设计',
    'Discovery': '7. 机器辅助的理论',
    'Code': '8. 写成代码的理论',
    'Selection': '9. 坏科学的自然选择',
    'Traces': '10. 数字痕迹',
    'Automation': '11. 研究的自动化',
    'Ranked': '12. 按证据排序的改革提议',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：委托经得起检验的研究',
    'Frontier': '15. 前沿：一门研究自身的科学',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    "In 2020 Matthew Salganik and colleagues ran a contest. <bookmark mark='a'/> A hundred and ":
        "2020年，马修·萨尔加尼克及其同事举办了一场竞赛。<bookmark mark='a'/>一百六十支团队拿到了关于大约四千个家庭的数千个变量，可以用任何他们喜欢的方法，预测孩子生活中的六项结果，比如他们十五岁时的成绩。<bookmark mark='b'/>最好的模型只比一个用四个变量的回归好一点点，而且解释的变异很少。<bookmark mark='c'/>这是在普赛克模拟的一个队列上进行的同一场竞赛。一百六十支团队中最好的得分是零点一三，四变量回归也是，而上限是零点二，没有任何模型能超过。<bookmark mark='d'/>一个解释得多、预测得少的领域，必须决定自己是为了什么。",
    'So this part asks: what would psychology look like if it were designed today? <bookmark ma':
        "所以这一部分问：如果心理学在今天被设计出来，它会是什么样子？<bookmark mark='a'/>预测、解释，以及如何两者兼得。<bookmark mark='b'/>更大的团队，更大、更广的样本。<bookmark mark='c'/>被设计成空间而不是点的实验，写成代码的理论，以及帮助寻找理论的机器。<bookmark mark='d'/>一个关于研究共同体本身的模型，以及按“是否有效”的证据排序的改革提议。",
    "This is Part 61 of Psychology, Built: the next psychology. <bookmark mark='a'/> We'll sepa":
        "这是《心理学，从零搭建》的第61部分：下一代心理学。<bookmark mark='a'/>我们将把解释和预测区分开，并说明各自能换来什么。我们将解读多实验室研究中的异质性，以及大样本能修正什么、不能修正什么。我们将把一个实验设计成一个空间，配上一个代理模型。我们将把一个理论写成代码，让它做出冒险的预测。我们将在两套激励下运行一个研究共同体的模型。我们还将按“是否有效”的证据给改革提议排序。",
    'Chapter one. On you: a space of experiments, and four numbers.':
        '第一章。在你身上：一个实验空间，以及四个数字。',
    "First, an experiment on you. You're testing whether a reminder raises attendance at appoin":
        "首先，一个在你身上做的实验。你在检验提醒是否能提高预约的到诊率，也就是第55部分的问题。<bookmark mark='a'/>你必须做出十个设计选择：短信还是电话，提醒一次还是三次，有没有署名的发送者，等等。每个选择有两个选项，所以一共有一千零二十四种可能的实验。在脑子里选一个，就像一项标准研究那样。<bookmark mark='b'/>现在，这是在普赛克构建的世界里，每一种实验中的真实效应。<bookmark mark='c'/>一个格子，一项研究：同一个问题，不同的答案。超过四分之一的格子方向相反。你选的是哪一个？",
    "Now four numbers. <bookmark mark='a'/> One: a hundred and sixty teams with thousands of va":
        "现在是四个数字。<bookmark mark='a'/>第一：一百六十支团队用数千个变量预测一个孩子的学业成绩。最好的留出R平方是多少？<bookmark mark='b'/>第二：一个效应在四十个实验室里进行，实验室之间没有真实差异。各实验室的估计值相差多远？<bookmark mark='c'/>第三：一百万名自我选择的志愿者。偏差会随着区间一起缩小吗？<bookmark mark='d'/>第四：实验室按发表数量被模仿，持续两百代。已发表的阳性结果中有多大比例是假的？在这里暂停，把它们写下来。",
    'Chapter two. Explanation and prediction.':
        '第二章。解释与预测。',
    "What is psychology for? There are two goals. <bookmark mark='a'/> Explanation identifies c":
        "心理学是为了什么？有两个目标。<bookmark mark='a'/>解释识别原因和机制，通常是在一个样本中检验某个系数是否不等于零。<bookmark mark='b'/>预测准确地预报新的个案，用模型没见过的数据来评判。<bookmark mark='c'/>2017年，塔尔·亚尔科尼和雅各布·韦斯特福尔主张，心理学选择了解释，而它的模型在样本外往往预测得很差，这也应该让做解释的人担忧。<bookmark mark='d'/>这是第59部分的一课：样本内的拟合会美化每一个模型，解释性的模型也不例外。",
    "Here is the problem in one picture. <bookmark mark='a'/> Psyche's cohort has four hundred ":
        "这是一幅图里的问题。<bookmark mark='a'/>普赛克的队列有四百个基线变量，其中四个有明确的效应，其余的都很微小。一个模型用最小二乘法在一千人身上拟合，再在另外三千人身上评分。<bookmark mark='b'/>在样本内，每加一个变量R平方就上升，用上全部四百个时超过一半。<bookmark mark='c'/>在新的人身上，它在四个变量时达到峰值，约为零点一六，然后跌到零以下：比直接预测平均值还差。<bookmark mark='d'/>真实的上限约为零点二。结果的大部分是噪声，没有任何方法能超越它。<bookmark mark='e'/>一篇解释性的论文报告的是红色曲线。它还应当回答的问题是金色的那条。",
    "How do you have both? <bookmark mark='a'/> Jake Hofman and colleagues proposed integrative":
        "怎样两者兼得？<bookmark mark='a'/>杰克·霍夫曼及其同事在2021年提出了整合式建模：同时也用留出预测来评分的因果模型。<bookmark mark='b'/>报告上限：考虑到结果中的噪声，它到底有多可预测？<bookmark mark='c'/>一个只解释了一点点变异的理论，仍然可以是正确而有用的，因为小的原因在整个人群中会累加起来。<bookmark mark='d'/>而一个预测得很好的模型，仍然可能在原因上是错的，这是第47部分关于个体内和个体间的一课。",
    'Chapter three. Big team science.':
        '第三章。大团队科学。',
    "What happens when one study is run in dozens of labs? <bookmark mark='a'/> From 2014 the M":
        "当一项研究在几十个实验室里进行时，会发生什么？<bookmark mark='a'/>从2014年起，多实验室项目用同一份方案，在全世界几十个实验室里重做经典效应。<bookmark mark='b'/>2018年，心理科学加速器把几十个国家的数百个实验室联合起来，研究由网络共同选定。<bookmark mark='c'/>ManyBabies把婴儿研究，也就是第30部分的主题，跨实验室汇集起来，而这类研究的样本一直很小。<bookmark mark='d'/>代价是：每项研究要花数年，需要协调，而功劳由数百位作者分享。",
    "Here's what forty labs look like. <bookmark mark='a'/> Psyche's effect, a d of zero point ":
        "这是四十个实验室的样子。<bookmark mark='a'/>普赛克的效应，d等于零点三，在四十个实验室里进行，每个实验室一百人，实验室之间没有真实差异。<bookmark mark='b'/>估计值仍然从大约负零点一分布到零点七。那只是抽样误差，也是你的第二个数字。<bookmark mark='c'/>如果实验室之间有真实差异，I平方从百分之十九上升到百分之三十六。<bookmark mark='d'/>在多实验室项目2中，理查德·克莱因及其同事发现，二十八个效应中的大多数，在大约六十个样本之间的异质性很小。一个实验室的单个结果主要反映的是抽样，而不是它的文化。",
    "What does big team science cost? <bookmark mark='a'/> Time: a protocol agreed by dozens of":
        "大团队科学的代价是什么？<bookmark mark='a'/>时间：一份由几十个实验室商定、经过翻译、并获得每个伦理委员会批准的方案，需要的是几年，而不是几个月。<bookmark mark='b'/>功劳：一篇论文有数百位作者，所以贡献声明，说明谁设计、谁执行、谁分析，取代了署名的顺序。<bookmark mark='c'/>效应的选择：被检验的都是有名的效应，而一个联盟仍然可能挑选容易在线上做的研究。<bookmark mark='d'/>而它换来的是：效应及其在不同地方之间的离散程度的估计，这是任何单个实验室都给不了的。",
    'Chapter four. Millions of participants.':
        '第四章。数以百万计的参与者。',
    "What can a sample of a million fix? Here are experiments at that scale. <bookmark mark='a'":
        "一个一百万人的样本能修正什么？这里有这种规模的实验。<bookmark mark='a'/>Sea Hero Quest是一款手机游戏，它的关卡测量空间导航，在几十个国家有数百万人玩过，安托万·库特罗及其同事在2018年报告了结果。<bookmark mark='b'/>道德机器收集了大约四千万个决定，内容是无人驾驶汽车应当保全谁，来自两百三十三个国家和地区。<bookmark mark='c'/>还有一个大约六十七万人参加的语法测验，被用来估计学习一门语言的能力何时下降。",
    "But size fixes only one thing. <bookmark mark='a'/> Psyche's population has a true mean of":
        "但规模只能修正一件事。<bookmark mark='a'/>普赛克的总体真实均值为零，而得分较高的人稍微更可能报名参加。<bookmark mark='b'/>从一百名到一百万名志愿者，百分之九十五区间缩小了一百倍。<bookmark mark='c'/>它是围绕零点二二缩小的，而不是零。这是你的第三个数字。<bookmark mark='d'/>规模修正的是噪声。它修正不了谁选择了参加，也修正不了一个游戏测量的是什么，那是第3部分的效度。",
    "How big is a biased million? <bookmark mark='a'/> In 2018 Xiao-Li Meng wrote the error of ":
        "一个有偏的一百万到底有多大？<bookmark mark='a'/>2018年，孟晓犁把样本均值的误差写成三项的乘积：参与与否和答案之间的相关、总体中未被抽到的比例，以及答案的离散程度。<bookmark mark='b'/>没有随机化，这个相关不会随着样本增大而缩小。<bookmark mark='c'/>算一下：相关为零点零零五，一个微小的倾斜，总体三亿人，抽取百分之一的样本，也就是三百万人。<bookmark mark='d'/>它的误差相当于一个大约四百人的简单随机样本。<bookmark mark='e'/>一个小的随机样本可以胜过一个巨大的自我选择样本。对于估计均值，人是怎样被选中的，比选中了多少人更重要。",
    'Chapter five. Who is sampled.':
        '第五章。谁被抽样。',
    "A decade after WEIRD, who does psychology study? <bookmark mark='a'/> In Part 38, Joseph H":
        "WEIRD被提出十年之后，心理学研究的是谁？<bookmark mark='a'/>在第38部分，约瑟夫·亨里奇、史蒂文·海因和阿拉·诺伦扎扬表明，大多数参与者是西方的、受过教育的、工业化的、富裕的和民主的。<bookmark mark='b'/>2021年，安贝尔·盖尔·塔尔迈尔、塞西莉亚·托斯卡内利和杰弗里·阿内特发现，在顶尖期刊中，来自美国和欧洲的样本仍然占绝大多数，作者更是如此。<bookmark mark='c'/>代价就是第38部分讲过的：错觉和公平博弈在不同社会之间各不相同。<bookmark mark='d'/>补救办法是全球网络、资助当地的实验室，以及在每篇论文的摘要里报告抽样的是谁。",
    "There's a second default: English. <bookmark mark='a'/> In 2022 Damian Blasi and colleague":
        "还有第二个默认：英语。<bookmark mark='a'/>2022年，达米安·布拉西及其同事表明，认知科学中关于语言与思维的研究，大多使用说英语的人。<bookmark mark='b'/>英语是不寻常的：它的拼写、固定的语序、很少的语法标记。<bookmark mark='c'/>关于阅读，也就是第23部分的主题，以及关于对词语和类别的记忆的主张，都建立在这一种语言上。<bookmark mark='d'/>检验在于一个发现在与英语不同的语言中是否成立，而这个问题常常从未被问过。",
    "One remedy is to say whom the finding is about. <bookmark mark='a'/> In 2017 Daniel Simons":
        "一个补救办法，是说明这个发现是关于谁的。<bookmark mark='a'/>2017年，丹尼尔·西蒙斯、正田佑一和史蒂芬·林赛提议，每篇论文都以一份关于概括性限制的声明结尾：作者预期结果对哪些人、刺激、程序和情境成立，以及为什么。<bookmark mark='b'/>一个来自某个城市一百二十名本科生的、关于“人”的主张，就变成了关于他们的主张，除非作者进一步论证。<bookmark mark='c'/>它把没有说出的概括性变成了一个可检验的预测。在声明范围之外的重复是一次检验，而不是一次失败。<bookmark mark='d'/>它还让抽样成为一个设计决定。要主张更多，就要更广泛地抽样，正如多实验室项目所做的。",
    'Chapter six. Integrative experiment design.':
        '第六章。整合式实验设计。',
    "What if an experiment were a space, not a point? <bookmark mark='a'/> In 2024 Abdullah Alm":
        "如果一个实验是一个空间，而不是一个点呢？<bookmark mark='a'/>2024年，阿卜杜拉·阿尔马图克及其同事用设计回应了第58部分里纽厄尔的抱怨。<bookmark mark='b'/>列出关于一个问题的各个实验彼此不同的维度。这就定义了一个空间。<bookmark mark='c'/>在这个空间里抽取许多点，通常在线上并行进行。<bookmark mark='d'/>在整个空间上拟合一个效应的代理模型，让各个理论竞相预测没有人做过的格子。<bookmark mark='e'/>结果是一张效应在哪里成立的地图，而不是两个格子之间的争论。",
    "Here it is with the reminder experiment. <bookmark mark='a'/> Its thousand and twenty-four":
        "这是用提醒实验来做的。<bookmark mark='a'/>它的一千零二十四个格子中，随机做了一百二十个，每个都带有噪声。<bookmark mark='b'/>代理模型包含十个主效应和它们的四十五个两两交互，用岭惩罚拟合。<bookmark mark='c'/>对没有人做过的九百零四个格子，它的预测与真实值的相关是零点九九。<bookmark mark='d'/>单独一项研究只会报告其中一个点。这个空间显示出哪些选择要紧，以及效应在哪里反转。在普赛克中效应确实这么简单；真实的空间可能需要做更多的格子。",
    'Chapter seven. Machine-assisted theory.':
        '第七章。机器辅助的理论。',
    "Can a machine help find a theory? <bookmark mark='a'/> In 2021 Joshua Peterson and colleag":
        "一台机器能帮助找到一个理论吗？<bookmark mark='a'/>2021年，约书亚·彼得森及其同事收集了对将近一万对赌局的选择，也就是第26部分的choices13k，远多于此前任何一项研究。<bookmark mark='b'/>他们拟合了被约束在不同理论类别中的神经网络，并加以比较。<bookmark mark='c'/>学到的最好的理论包含了前景理论的各个部分，并显示出它们在哪里随情境弯曲。<bookmark mark='d'/>机器负责搜索，人仍然要阅读和评判它找到的东西。",
    "Machines can also choose the next experiment. <bookmark mark='a'/> In adaptive design, aft":
        "机器还能选择下一个实验。<bookmark mark='a'/>在自适应设计中，每做完一个试次或一项研究，你就选择最能区分仍然站得住的那些理论的下一个，这是杰伊·明和马克·皮特发展起来的方法。<bookmark mark='b'/>它的做法是在实施之前，计算关于哪个理论正确的期望信息量。<bookmark mark='c'/>这和第45部分的自适应测验是同一个思想：问那个你还无法预测其答案的问题。<bookmark mark='d'/>防线是：理论和停止规则要事先固定，否则自适应就变成了分岔路径。",
    "Here's adaptive design in Psyche. <bookmark mark='a'/> There are two theories of forgettin":
        "这是在普赛克中做的自适应设计。<bookmark mark='a'/>有两个关于遗忘的理论，一个幂律和一个指数，参数都固定。它们在中等延迟时几乎一致，在短延迟和长延迟时分开。<bookmark mark='b'/>每个模拟的人都按幂律遗忘，每个试次是一次回忆测验。固定设计在十个延迟之间轮流。它需要中位数二十五次测验，才能有百分之九十五的把握判断哪个理论正确。<bookmark mark='c'/>自适应设计在每次测验之前问：哪个延迟信息量最大？它几乎每次都选最长的延迟，因为在那里指数模型预测几乎回忆不起来，于是它只需要十一次测验。<bookmark mark='d'/>这就是丹尼尔·卡瓦尼亚罗、杰伊·明和马克·皮特发展的准则，他们最早的演示之一用的正是这一对理论。当每次测验都代价高昂时，比如对患者或婴儿，这种节省最要紧。",
    'Chapter eight. Theory as code.':
        '第八章。写成代码的理论。',
    "What would it take for a theory to be derivable? <bookmark mark='a'/> Verbal theories are ":
        "一个理论要怎样才能被推导出来？<bookmark mark='a'/>口头理论是模糊的。“焦虑使注意偏向威胁”预测了一个方向，却没有大小、时间进程或边界。<bookmark mark='b'/>它们很灵活：几乎任何结果事后都能和它们调和起来。<bookmark mark='c'/>一个写成代码的模型做出你能计算的预测，包括出人意料的预测。<bookmark mark='d'/>这个系列就是这个想法：普赛克用一个你可以阅读其代码的模型，计算出每一章的主张。",
    "Here is what writing a theory as code does. <bookmark mark='a'/> The verbal version: pract":
        "这就是把一个理论写成代码的作用。<bookmark mark='a'/>口头版本：练习让人变快，收益递减。<bookmark mark='b'/>写成代码，这句话就必须做出选择。幂律，还是指数？那是第48部分那条后来被证明是平均结果的定律。<bookmark mark='c'/>两者对早期试次的预测相同，对后期试次的预测不同。幂律在一千个试次之后仍在改善，而指数已经停了。<bookmark mark='d'/>把它写下来，就暴露了这句话隐藏的选择，并指明了能解决它的实验：长时间练习，逐个人拟合。",
    "Theory construction can be a method. <bookmark mark='a'/> Denny Borsboom and colleagues pr":
        "理论构建可以是一种方法。<bookmark mark='a'/>丹尼·博斯布姆及其同事提议，从稳健的现象出发，构建一个能产生它们的形式模型，并检查它确实能产生。<bookmark mark='b'/>艾丽斯·范罗伊和焦苏埃·巴焦主张先有理论再检验：在用数据检验一个理论之前，先问它究竟能不能产生这种行为。<bookmark mark='c'/>然后是冒险的预测：一个理论禁止的结果，在研究之前写下来。那就是第62部分的注册报告。<bookmark mark='d'/>什么才算一次推导？另一个人运行这段代码，得到同样的预测。",
    'Chapter nine. The natural selection of bad science.':
        '第九章。坏科学的自然选择。',
    "What do incentives do to methods? <bookmark mark='a'/> In 2016 Paul Smaldino and Richard M":
        "激励会对方法产生什么影响？<bookmark mark='a'/>2016年，保罗·斯马尔迪诺和理查德·麦克尔里思为努力程度不同的实验室建模。更细心意味着更少的假阳性，也意味着更少的研究。<bookmark mark='b'/>只有阳性结果被发表，发表更多的实验室会被模仿，通过它们的学生，也通过招聘。<bookmark mark='c'/>没有人作弊。每个实验室都是诚实的，是选择在起作用。<bookmark mark='d'/>他们对文献中统计功效的回顾发现，六十年来没有改善。",
    "Here's the model run. <bookmark mark='a'/> Psyche has a hundred labs. One hypothesis in te":
        "这是模型的运行结果。<bookmark mark='a'/>普赛克有一百个实验室。十个假设中有一个是真的，统计功效是零点八。<bookmark mark='b'/>只发表阳性结果，并模仿发表最多的实验室。努力崩溃了，已发表的阳性结果中有百分之八十八是假的。这是你的第四个数字。<bookmark mark='c'/>现在换成注册报告：方法在结果出现之前就被评审，每个结果都发表。努力保持住了，假的比例大约是五分之二。十个假设中只有一个是真的，所以仍有一些假阳性。<bookmark mark='d'/>改变被选择的东西，方法就会跟着改变。单靠劝诫做不到。",
    'Chapter ten. Digital traces.':
        '第十章。数字痕迹。',
    "Can language online measure a population's health? <bookmark mark='a'/> In 2015 Johannes E":
        "网上的语言能测量一个人群的健康吗？<bookmark mark='a'/>2015年，约翰内斯·艾希施泰特及其同事报告说，美国各县推文的语言预测心脏病死亡，比一个由人口和健康因素构成的模型更好。<bookmark mark='b'/>愤怒和敌意的词与更多的死亡相伴，表示投入和乐观的词与更少的死亡相伴。<bookmark mark='c'/>2018年，尼古拉斯·布朗和詹姆斯·科因指出，发推文的人并不是死去的那些人，而且结果会随所纳入的县和所选的分析而变化。<bookmark mark='d'/>这是第47部分的警告：县一级的关联对个人几乎说明不了什么。",
    "Here's the trap in that study's design, simulated. <bookmark mark='a'/> Psyche has three t":
        "这是那项研究设计中的陷阱，模拟出来。<bookmark mark='a'/>普赛克有三千个县，每县一千人。一个县的收入同时降低了当地人的敌意发帖和心脏风险。<bookmark mark='b'/>跨县来看，语言和心脏病的相关约为零点六。<bookmark mark='c'/>跨个人来看，约为零点零六，而在一个县内部是零。一个人的用词，对他们自己的心脏什么也说明不了。<bookmark mark='d'/>县一级的相关是真实的，仍然可以用来绘制地图。把它当作关于个人的事实来读，就是生态学谬误。<bookmark mark='e'/>所以一项痕迹研究必须说明它的主张处在哪个层面，以及这些单位之间还有什么不同。",
    "What do digital traces need? <bookmark mark='a'/> Validity: a word count is not a feeling,":
        "数字痕迹需要什么？<bookmark mark='a'/>效度：一个词频计数不是一种感受，所以要像第3部分那样，用人来检验这个测量。<bookmark mark='b'/>正确的层面：群体的主张来自群体的数据，个人的主张需要个人的数据。<bookmark mark='c'/>留出检验：用没有参与建模的地区或人来给预测评分。<bookmark mark='d'/>还有同意和伤害：这些痕迹不是为研究而提供的，而推断健康或特质可能伤害被推断的人。",
    'Chapter eleven. Automating research.':
        '第十一章。研究的自动化。',
    "What can machines do in a lab? <bookmark mark='a'/> As assistants: searching and summarizi":
        "机器在实验室里能做什么？<bookmark mark='a'/>作为助手：检索和总结文献，编写分析代码，并检查它。<bookmark mark='b'/>作为模拟参与者：在研究之前预试材料、预测结果，但受第60部分所说的硅基样本局限的约束。<bookmark mark='c'/>作为审稿人：检查统计和报告，就像自动检查p值的工具已经在做的那样。<bookmark mark='d'/>还有风险：流畅的错误、编造的参考文献，以及一种向模型早已说过的东西靠拢的文献。",
    "Some checks a machine can run on every paper. <bookmark mark='a'/> Computational reproduci":
        "有一些检查，机器可以在每篇论文上运行。<bookmark mark='a'/>计算可重复性：在作者的数据上重新运行他们的代码，并核对论文中的每一个数字。对有数据政策的期刊的审计发现，许多论文无法以这种方式重现。<bookmark mark='b'/>一致性：第50部分的statcheck、GRIM和SPRITE，在投稿时运行。<bookmark mark='c'/>代码形式的预注册，正如第43部分那样：注册的分析就是运行的分析，任何偏离都会被打印出来。<bookmark mark='d'/>而它们都检查不了的是：测量是否有效，样本是否合适，问题是否值得问。",
    "So what must stay human? <bookmark mark='a'/> Choosing the question: what's worth knowing,":
        "那么，什么必须留给人？<bookmark mark='a'/>选择问题：什么值得知道，为了谁。<bookmark mark='b'/>责任：一个具名的人为每一个主张和每一个数字负责。<bookmark mark='c'/>与人的接触：同意、照护，以及参与者自己对这项研究的看法。<bookmark mark='d'/>还有对证据的判断：账本里的状态是决定，是有理由的。",
    'Chapter twelve. Proposals, ranked by evidence.':
        '第十二章。按证据排序的改革提议。',
    'Which reforms work? Here are the proposals, ranked by the evidence that they do. <bookmark':
        "哪些改革有效？这里是各项提议，按证明它们有效的证据排序。<bookmark mark='a'/>更大的样本和功效分析：证据很强，因为重复率随功效上升，正如第4部分所展示的。<bookmark mark='b'/>注册报告：很强。发表的零结果多得多，而它们的质量被评为至少同样高。<bookmark mark='c'/>开放数据和代码：证据良好。错误被发现并得到更正，尽管采用仍不完全。<bookmark mark='d'/>大团队科学：良好，能对异质性给出精确的回答，但缓慢而昂贵。<bookmark mark='e'/>单独的预注册：好坏参半。计划往往含糊，偏离也没有报告。<bookmark mark='f'/>整合式设计和形式理论：前景可观，但很少有检验它们是否加快了发现的研究。<bookmark mark='g'/>还有降低显著性阈值：有人主张，但没有检验过。",
    'Chapter thirteen. The Ledger.':
        '第十三章。账本。',
    "Four new rows. The first: children's life outcomes are hard to predict, whatever the metho":
        "四个新行。第一行：无论用什么方法，儿童的人生结果都很难预测。<bookmark mark='a'/>原始研究：萨尔加尼克及其同事，2020年。<bookmark mark='b'/>记录：那一项研究内部的一百六十支团队；还没有其他队列。<bookmark mark='c'/>上限在结果本身，而不在方法。<bookmark mark='d'/>尚未直接检验。",
    'The second: most effects vary little between labs and countries beyond sampling error. <bo':
        "第二行：大多数效应在实验室和国家之间的变化，超出抽样误差的部分很小。<bookmark mark='a'/>原始研究：多实验室项目1，2014年。<bookmark mark='b'/>记录：多实验室项目2，以及一项对许多重复项目的回顾。<bookmark mark='c'/>情境的影响比单项研究所暗示的要小。<bookmark mark='d'/>已重复。",
    "The third: experiments online give results comparable to the lab. <bookmark mark='a'/> The":
        "第三行：在线实验给出与实验室相当的结果。<bookmark mark='a'/>原始研究：杰米恩及其同事，2012年。<bookmark mark='b'/>记录：经典范式在一个众包平台上被重现。<bookmark mark='c'/>前提是注意数据质量和计时。<bookmark mark='d'/>已重复。",
    "And the fourth: county tweets predict heart disease deaths. <bookmark mark='a'/> The origi":
        "第四行：各县的推文能预测心脏病死亡。<bookmark mark='a'/>原始研究：艾希施泰特及其同事，2015年。<bookmark mark='b'/>记录：一项重新分析发现结果很脆弱。<bookmark mark='c'/>充其量是一个群体层面的关联。<bookmark mark='d'/>有争议。",
    "What the four have in common. <bookmark mark='a'/> The methods of the next psychology alre":
        "这四行的共同点。<bookmark mark='a'/>下一代心理学的方法已经有了记录：在线实验室和多实验室设计都能重复。<bookmark mark='b'/>预测设定了令人谦卑的上限，而数字痕迹需要在正确的层面上验证。<bookmark mark='c'/>改变一个领域的，是它选择什么：注册的结果、共享的数据和大团队。<bookmark mark='d'/>所以这一部分问题的答案是：如果在今天设计，心理学会更大、更广、更形式化，并且会选择严谨。",
    'Chapter fourteen. In practice: commissioning research that holds up.':
        '第十四章。实践中：委托经得起检验的研究。',
    "Where is this a job? <bookmark mark='a'/> In research operations: running studies at scale":
        "这在哪里是一份工作？<bookmark mark='a'/>在研究运营中：在公司里大规模地开展研究，配有被试库、质量检查，以及记录做过什么的登记册。<bookmark mark='b'/>在实验平台上，它们每年运行数千个在线实验，并设有防止偷看和分岔路径的护栏。<bookmark mark='c'/>在预测中：给“哪些发现会站得住”的预测打分的竞赛和市场，正如第50部分。<bookmark mark='d'/>还有在资助者和编辑之中，他们设计激励：注册报告、数据政策和重复研究资助。",
    "You're paying for a study. What do you ask for? <bookmark mark='a'/> The decision the stud":
        "你在为一项研究付钱。你要提出什么要求？<bookmark mark='a'/>这项研究将为之提供依据的决定，以及会改变这个决定的最小效应。<bookmark mark='b'/>一份注册过的计划：假设、根据功效分析得出的样本量、主要结果，以及分析代码。<bookmark mark='c'/>为研究付钱，而不是为结果付钱。这就是注册报告的规则。<bookmark mark='d'/>描述样本：是谁、在哪里、怎样招募的，用的是什么语言。<bookmark mark='e'/>以及交付数据和代码，如果决定重大，还要预留一次重复研究的预算。",
    'Chapter fifteen. Frontier: a science that studies itself.':
        '第十五章。前沿：一门研究自身的科学。',
    "Can a field measure its own progress? First, what's new. <bookmark mark='a'/> Metascience ":
        "一个领域能测量自己的进步吗？先说新进展。<bookmark mark='a'/>元科学对期刊政策、同行评审和培训开展随机试验。<bookmark mark='b'/>活的综述随着研究的出现更新元分析，像账本一样标注日期。<bookmark mark='c'/>研究网络让跨文化检验成为第一项研究，而不是最后一项。<bookmark mark='d'/>代理模型和自适应设计选择下一个实验。",
    "And the open problems. <bookmark mark='a'/> How to tell a field that's accumulating knowle":
        "还有悬而未决的问题。<bookmark mark='a'/>如何区分一个正在积累知识的领域和一个没有积累的领域。<bookmark mark='b'/>如何奖励对大团队、数据和重复研究的贡献。<bookmark mark='c'/>形式理论和整合式设计是否加快了发现，要作为干预来检验。<bookmark mark='d'/>以及是什么限制了人生的可预测性，它能否被提高。",
    "First, your four numbers. <bookmark mark='a'/> In the real challenge the best held-out R s":
        "先说你的四个数字。<bookmark mark='a'/>在真实的竞赛中，最好的留出R平方约为零点二，出现在六项结果中的两项上，其余的低得多；在普赛克中是零点一三。没有真实差异的四十个实验室，给出的估计值从大约负零点一到零点七。一百万名自我选择的志愿者，给出了一个围绕零点二二的偏差、正负零点零零二的区间。而按发表数量的选择，让百分之八十八的阳性结果是假的。<bookmark mark='b'/>上限、噪声、偏差和激励：一个被重新设计的领域必须围绕这四个事实来构建。",
    "Part sixty-one in twelve lines. <bookmark mark='a'/> Life outcomes have low ceilings of pr":
        "十二行总结第六十一部分。<bookmark mark='a'/>人生结果的可预测性上限很低。要解释也要预测，就在样本外给因果模型评分。在许多实验室之间，大多数异质性很小。规模修正的是噪声，修正不了选择或效度。大多数参与者和作者仍然是WEIRD的，而且说英语。实验可以是空间，配上代理模型。机器可以搜索理论的空间，由人来评判。写成代码的理论能做出冒险的预测。按发表数量的选择会培育出坏的方法。数字痕迹需要在正确的层面上验证。自动化的是任务，不是责任。按证据给改革排序，功效和注册报告排在最前。",
    "Where this comes back. <bookmark mark='a'/> Everything does, in Part 62: a registered repo":
        "这些内容会在哪里再出现。<bookmark mark='a'/>一切都会，在第62部分：一份从头到尾执行完的注册报告，普赛克的整套测验和完整的账本，以及全部六十二个部分的开放问题。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds ":
        "七道习题，完整解答在这一部分的README里。<bookmark mark='a'/>一道求上限。一道计算许多实验室的离散程度。一道解读一个巨大的有偏样本。一道数清一个设计空间。两道推演斯马尔迪诺和麦克尔里思的算术。最后一道带星号，请你写一份委托研究的简报。如果你想试试，就在这里暂停。",
    "The books and papers behind this part are listed here and in the README. Salganik's book i":
        '这一部分背后的书和论文列在这里，也列在README里。萨尔加尼克的书是关于用数字数据做研究的最好入门；亚尔科尼和韦斯特福尔的论文阐明了预测的理由；斯马尔迪诺和麦克尔里思的模型展示了激励如何塑造方法。',
    "Four parts of the frontier are done. <bookmark mark='a'/> This one designed the next psych":
        "前沿的四个部分已经完成。<bookmark mark='a'/>这一部分设计了下一代心理学。<bookmark mark='b'/>最后一部分去做它：一个问题，走完一份注册报告，在数据出现之前接受评审，执行，并且无论结果如何都如实报告。然后结清账目，回答康德的反对意见。第62部分：学位论文。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
