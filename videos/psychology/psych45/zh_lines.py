"""Chinese narration for psych45: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第45部分：项目反应理论'

CHAPTERS = {
    'Hook': '不同的题目，同一把尺子',
    'Predict': '1. 在你身上：一次自适应测验，四个数字',
    'Classical': '2. 经典理论做不到的事',
    'Rasch': '3. 拉施模型',
    'Params': '4. 两个和三个参数',
    'Info': '5. 信息量',
    'Estimate': '6. 估计',
    'Cat': '7. 自适应测验',
    'Ratings': '8. 评定量表',
    'Dif': '9. 作为统计量的公平',
    'Linking': '10. 链接与等值',
    'Surveys': '11. 大规模测评',
    'Tracing': '12. 追踪学习',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：考试、诊所与机器',
    'Frontier': '15. 前沿：时间、生成的题目与学习系统',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'Two pupils of exactly the same ability take a reading test.':
        "两个能力完全相同的学生参加一次阅读测验。<bookmark mark='a'/>一个拿到简单的试卷，另一个拿到难的，两份试卷没有一道共同的题目。<bookmark mark='b'/>他们的期望得分分别约为十分之八和十分之三。<bookmark mark='c'/>分数说明一个人在这些题目上的表现，却说不出他们在别的题目上会怎样。<bookmark mark='d'/>所以这一部分的问题是：做了不同题目的人，能放到同一把尺子上吗？",
    'The answer came from Denmark.':
        "答案来自丹麦。<bookmark mark='a'/>二十世纪五十年代，数学家格奥尔格·拉施受托比较儿童在没有共同题目的不同测验上的阅读水平。<bookmark mark='b'/>在1960年的书中，他为一个人与一道题的单次相遇建模：成功的几率只取决于能力减去难度。<bookmark mark='c'/>于是人和题目分离开来。比较能力可以不依赖题目，比较题目也可以不依赖人。<bookmark mark='d'/>从这个想法中产生了自适应测验、关于不公平题目的统计定义、全国性的学生知识调查，以及追踪学习者掌握了什么的方法。",
    'So this part asks how to measure with questions that differ from person to person.':
        "所以这一部分要问：当每个人回答的题目都不同，如何测量。<bookmark mark='a'/>经典分数做不到的事，以及能做到的拉施模型。<bookmark mark='b'/>区分度、猜测，以及一道题能告诉你多少。<bookmark mark='c'/>估计、自适应测验和评定量表。<bookmark mark='d'/>还有公平的题目、相互链接的试卷、全国性调查，以及学习。",
    'This is Part 45 of Psychology, Built: item response theory.':
        "这是《心理学，从零搭建》第45部分：项目反应理论。<bookmark mark='a'/>我们将构建拉施模型，并推导为什么总分就是你需要的全部。我们将加入区分度和猜测，并衡量每道题告诉你多少。我们将在真实测验数据上，用边际最大似然估计题目参数。我们将构建一个自适应测验，并与固定试卷比较。我们将拟合评定量表，找出不公平的题目，并链接两份试卷。我们还将看到全国性调查如何报告一个总体，以及软件如何追踪学习者掌握了什么。",
    'Chapter one. On you: an adaptive test, and four numbers.': "第1章。在你身上：一次自适应测验，四个数字。",
    'First, watch an adaptive test at work.':
        "首先，看一次自适应测验是如何工作的。Psyche来做这次测验，真实能力是一点三。<bookmark mark='a'/>每道题的选择，都是在当前估计值上信息量最大的那一道：这个人大约有一半机会答对的题。<bookmark mark='b'/>答对就给更难的题，答错就给更容易的。每个标记都位于那道题的难度上。<bookmark mark='c'/>估计值周围的带子随着每次作答而收窄，当标准误降到零点三以下时测验停止。<bookmark mark='d'/>在课程网站上，你可以自己做一次简短的自适应测验。它不计分，也不保存任何东西。",
    'Now four numbers to write down.':
        "现在写下四个数字。<bookmark mark='a'/>第一：一个从三百道题的题库中出题的自适应测验，在标准误达到零点三时停止。它大约会出多少道题？<bookmark mark='b'/>第二：最好的固定试卷需要多少道题才能同样准确？<bookmark mark='c'/>第三：一项法学院入学考试中的五道题，由一千人作答。每道题都需要自己的区分度吗，还是最简单的模型就够了？<bookmark mark='d'/>第四：两个群体的能力相差零点八个标准差。在一道完全公平的题目上，他们的答对比例相差多少？在这里暂停，把它们写下来。",
    'Chapter two. What classical theory cannot do.': "第2章。经典理论做不到的事。",
    'Classical test theory, from Part 3, has three blind spots.':
        "第3部分讲的经典测验理论有三个盲点。<bookmark mark='a'/>第一：一道题的难度是答对它的人所占的比例。<bookmark mark='b'/>把同样的十道题给一个较弱的群体和一个较强的群体。中间那道题，一个群体大约十分之四答对，另一个群体大约十分之七。<bookmark mark='c'/>所以题目的难度取决于样本，而正如开头所示，一个人的分数取决于测验。两者都不单单属于题目或人。<bookmark mark='d'/>可是这些题目各自只有一个难度，是Psyche制作它们时就设定好的。",
    'The third blind spot.':
        "第三个盲点。<bookmark mark='a'/>经典理论对所有人给出同一个测量标准误：标准差乘以一减信度的平方根。<bookmark mark='b'/>但一份由中等难度题目组成的测验，能很好地测量中等水平的人，对两端的人却测得很差。<bookmark mark='c'/>项目反应理论为每个能力水平给出一个标准误，取决于题目在那里提供了多少信息。它在中间最小，向两端增大。<bookmark mark='d'/>所以有三件事要解决：难度不依赖样本的题目，不依赖测验的分数，以及每个人自己的误差。",
    'Chapter three. The Rasch model.': "第3章。拉施模型。",
    "Rasch's model is one encounter.":
        "拉施的模型是一次相遇。<bookmark mark='a'/>一个人有能力θ。一道题有难度b，在同一把尺子上。<bookmark mark='b'/>成功的对数几率等于能力减去难度。所以能力恰好等于题目难度的人，有一半的机会。<bookmark mark='c'/>每道题的曲线形状相同，只是沿能力轴平移。它叫作项目特征曲线。<bookmark mark='d'/>一次相遇，两个参数。其余一切，都来自把多次相遇乘在一起。",
    'Now the property Rasch prized.':
        "现在看拉施最珍视的性质。<bookmark mark='a'/>在任何一道题上比较两个人。他们对数几率之差就是他们的能力之差，无论用的是哪道题。<bookmark mark='b'/>在任何一个人身上比较两道题。差值就是它们的难度之差，无论是谁作答。<bookmark mark='c'/>拉施称之为特定客观性：比较人时不受题目影响，比较题目时不受人影响。<bookmark mark='d'/>只有当每道题的曲线斜率都相同时它才成立。斜率不同，比较的结果就取决于你看的位置。",
    "And the Rasch model's best property.":
        "还有拉施模型最好的性质。<bookmark mark='a'/>问：给定总分，一种作答模式有多大可能？把式子写出来，能力就消掉了。剩下的只与题目有关。<bookmark mark='b'/>这里是一项法学院入学考试的五道题上、答对两道的四种模式，分别在三个非常不同的能力水平上。概率完全相同。<bookmark mark='c'/>所以总分携带了作答中关于能力的全部信息。而题目参数可以在完全消去能力的情况下估计。这叫作条件最大似然。",
    'Chapter four. Two and three parameters.': "第4章。两个和三个参数。",
    "Real items aren't all alike.":
        "真实的题目并不都一样。<bookmark mark='a'/>区分度a，是曲线上升的陡峭程度。陡峭的题目能在其难度附近把人清楚地区分开，平坦的题目几乎区分不了。<bookmark mark='b'/>猜测c是一个下限。在四选一的题目上，即使能力最低的人也能答对大约四分之一。<bookmark mark='c'/>艾伦·伯恩鲍姆把这些两参数和三参数模型写进了洛德和诺维克1968年的教科书，弗雷德里克·洛德1980年的书使它们成为标准。<bookmark mark='d'/>代价是：斜率不相等时，总分不再是充分统计量，特定客观性也随之失去。",
    'Does it matter in practice?':
        "这在实践中重要吗？<bookmark mark='a'/>这里是法学院入学考试的五道题，由一千人作答，正是达雷尔·博克和罗伯特·利伯曼在1970年拟合过的数据。<bookmark mark='b'/>拉施模型只有一个共同斜率，两参数模型每道题有自己的斜率。<bookmark mark='c'/>似然比在四个自由度上大约只有半个点。在这里，额外的斜率什么也没换来。<bookmark mark='d'/>再看曲线所在的位置。这些题目很容易，所以这份测验能很好地区分能力弱的考生，却几乎区分不了能力强的。",
    'Chapter five. Information.': "第5章。信息量。",
    'How much does one answer tell us?':
        "一次作答能告诉我们多少？<bookmark mark='a'/>一道题的信息量，是单次作答中关于能力的费希尔信息：区分度的平方，乘以P，再乘以一减P。<bookmark mark='b'/>它在题目难度与人的能力相遇处达到峰值，高度为a的平方除以四。陡峭的题目提供很多信息，但范围很窄。<bookmark mark='c'/>信息量在题目之间相加，标准误是它平方根的倒数。所以测验是可以设计的：把信息量放在需要做决定的地方。<bookmark mark='d'/>有猜测时，低能力处的信息量会下降，因为答对可能只是运气。",
    'Now the law-school items.':
        "现在看法学院的题目。<bookmark mark='a'/>它们的测验信息量在大约负一点八处达到峰值，远低于普通考生的水平。<bookmark mark='b'/>即使在峰值处也只有大约零点六：标准误至少为一点三，比被测量的人之间的离散还大。<bookmark mark='c'/>五道题可以粗略地给一群人排序，却不能精确地定位某一个人。<bookmark mark='d'/>解决办法是在需要的地方增加题目。这正是自适应测验所做的。",
    'Chapter six. Estimation.': "第6章。估计。",
    "Here's the puzzle.":
        "这里有一个难题。要估计题目参数，你需要人的能力；要估计能力，你又需要题目参数。<bookmark mark='a'/>联合方法同时估计两者。但能力参数随人数增加而增加，题目的估计无论增加多少人都一直有偏。<bookmark mark='b'/>条件方法以每个总分为条件，于是能力消失了。它是精确的，但只适用于拉施模型。<bookmark mark='c'/>边际方法把能力看作从一个总体中抽取的，比如正态总体，然后把它积分掉。<bookmark mark='d'/>也就是每种作答模式的似然，在能力上取平均。",
    'Darrell Bock and Murray Aitkin made the marginal approach practical in 1981, with EM.':
        "1981年，达雷尔·博克和默里·艾特金用EM算法使边际方法变得可行。<bookmark mark='a'/>用一组能力格点代替积分，按正态曲线加权。<bookmark mark='b'/>在E步中，根据每个人的作答和当前的题目参数，求出每个人在格点上的后验。<bookmark mark='c'/>在M步中，每道题变成在格点上的一次加权逻辑回归：每个能力上有这么多期望人数，这么多期望答对数。<bookmark mark='d'/>在法学院的题目上，对数似然先上升，然后停住。估计值与已发表的拟合结果在小数点后三位上一致。",
    'With the items known, each person\'s ability follows.':
        "题目参数已知，每个人的能力就随之得出。<bookmark mark='a'/>最大似然找出使作答最可能的那个能力。全对或全错时，它是无穷大。<bookmark mark='b'/>期望后验估计是后验的均值，以总体为先验。它总是有限的，并被拉向均值。<bookmark mark='c'/>只有五道题时，后验标准差停留在零点八附近。先验的一几乎没有缩小。<bookmark mark='d'/>这种收缩，对于给一个人做最佳猜测是对的，对于描述一个总体却是错的，第十一章会说明。",
    'Chapter seven. Adaptive testing.': "第7章。自适应测验。",
    'An adaptive test is four steps, repeated.':
        "自适应测验是四个步骤的重复。<bookmark mark='a'/>估计：从总体均值开始，每次作答之后更新后验。<bookmark mark='b'/>选择：在当前估计值上信息量最大的未用题目。<bookmark mark='c'/>提问。<bookmark mark='d'/>当标准误足够小，或测验足够长时停止。<bookmark mark='e'/>每个人做的是自己的测验，但每个分数都在同一把尺子上，因为题目事先已经标定过。这就是拉施思想的回报。",
    'How much does it save?':
        "它能节省多少？<bookmark mark='a'/>Psyche让一千个模拟的人做一个由三百道已标定题目组成的题库。<bookmark mark='b'/>自适应测验平均在大约十七道题后停止。<bookmark mark='c'/>为普通人设计的最好的固定试卷，要达到同样的精度需要大约三十五道题。随机组成的固定试卷需要更多。<bookmark mark='d'/>对远离平均水平的人节省最多，而固定试卷恰恰把他们测得最差。",
    'The costs.':
        "代价。<bookmark mark='a'/>曝光。第一道题在均值处信息量最大，所以每个人都会做到它。在这里，每一个考生都做到了。一旦在网上流传，它就不再是测验题了。<bookmark mark='b'/>所以真实的测验会在少数几道最好的题中随机选择，或者限制每道题的使用率。<bookmark mark='c'/>测验还必须覆盖它的各个主题，所以选择是受约束的。<bookmark mark='d'/>它还需要一个有数百道题的题库，每道题都在足够多的人身上预测过，才能知道它的曲线。",
    'Chapter eight. Rating scales.': "第8章。评定量表。",
    'Questionnaires rarely have right answers.':
        "问卷很少有正确答案。它们有类别，从非常不同意到非常同意。<bookmark mark='a'/>杉岛富美子的等级反应模型给每一级一个阈值：在这个态度水平上，一个人回答至少这一类别的可能性开始大于不回答。<bookmark mark='b'/>这是1992年一项欧洲调查中的一道题：多亏了科学和技术，后代将有更多的机会。<bookmark mark='c'/>每个类别有自己的曲线，在态度轴上占据自己的一段。<bookmark mark='d'/>杰夫·马斯特斯的分部评分模型是它的拉施版本。",
    'Fit all four positively worded items.':
        "拟合全部四道正向表述的题目。<bookmark mark='a'/>三百九十二人，每题四个类别。<bookmark mark='b'/>关于未来的那道题区分度最高：它最清楚地按态度把人区分开。<bookmark mark='c'/>而第一个阈值远远低于人们所在的位置。几乎没有人非常不同意，所以那些类别携带的信息很少。<bookmark mark='d'/>第46部分会问：在问题和回答之间发生了什么，以及是否每个人都以同样的方式使用这些类别。",
    'Chapter nine. Fairness as a statistic.': "第9章。作为统计量的公平。",
    'When is an item unfair?':
        "一道题什么时候是不公平的？<bookmark mark='a'/>Psyche造出两个各三千人的群体，平均能力相差零点八个标准差，再造出十五道完全公平的题目。<bookmark mark='b'/>在第八题上，两个群体的答对比例相差大约十五个百分点。这是影响：群体之间的差异，而不是题目中的差异。<bookmark mark='c'/>所以改为比较能力相同的人，按总分匹配。两个群体的曲线彼此重合。<bookmark mark='d'/>在统计意义上，当能力相同的人有不同的机会时，一道题才是不公平的。这叫作项目功能差异。",
    'Testing companies screen every item this way.':
        "测验公司就是这样筛查每一道题的。<bookmark mark='a'/>在每个总分上做一个二乘二的表，群体对答对或答错，然后把各个总分上的比值比合并起来。保罗·霍兰德和多萝西·塞耶在1988年把曼特尔和亨塞尔的方法引入了测验领域。<bookmark mark='b'/>在公平的题目上，这个指标接近零：可以忽略。<bookmark mark='c'/>现在只对焦点群体把第八题的难度提高零点八。曲线分开了，指标把它标进最严重的一类。<bookmark mark='d'/>一个标记是交给内容专家的问题，而不是判决：这道题里有什么偏向某一个群体？",
    'Chapter ten. Linking and equating.': "第10章。链接与等值。",
    'A test given every year faces a problem.':
        "一项每年举行的测验面临一个问题。<bookmark mark='a'/>它的题目必须更换，否则会泄露。<bookmark mark='b'/>但每年的标定都把当年的人放在均值为零、标准差为一的位置。尺子的零点随着考生群体移动。<bookmark mark='c'/>如果今年的学生能力更强，单独标定会掩盖这一点，并使今年的题目看起来比实际更难。<bookmark mark='d'/>解决办法是共同题，称为锚题，两年都使用，它们的难度把两把尺子绑在一起。",
    "Here's linking at work.":
        "这是链接的实际操作。<bookmark mark='a'/>Psyche造出两份各三十道题的试卷，共享十道锚题。今年的学生能力更强，差异也更大。<bookmark mark='b'/>分别标定每份试卷，锚题的两组难度落在一条直线上，但不在对角线上。<bookmark mark='c'/>这条直线的斜率和截距来自锚题的均值和标准差。这里是一点二一和零点四三，真实值是一点二和零点五。<bookmark mark='d'/>链接之前，新题目的难度偏差大约零点四。链接之后，不到零点一。",
    'Linking puts the items on one scale.':
        "链接把题目放到同一把尺子上。等值把分数也放上去。<bookmark mark='a'/>每份试卷都有一条测验特征曲线：每个能力上的期望得分，现在用的是去年的尺子。<bookmark mark='b'/>今年的试卷稍难一些。在它上面得十五分，所对应的能力在去年的试卷上大约得十六分。<bookmark mark='c'/>真分数等值就是在两条曲线之间对读：从一个分数，到一个能力，再到另一份试卷的分数。<bookmark mark='d'/>所以及格线可以每年都意味着同样的东西，尽管没有哪两年用的是同一份测验。",
    'Chapter eleven. Large-scale assessment.': "第11章。大规模测评。",
    'National surveys of what students know have a different goal.':
        "全国性的学生知识调查有不同的目标。<bookmark mark='a'/>它们想在整个课程范围内描述一个国家的学生，这意味着题目远多于一个学生能回答的数量。<bookmark mark='b'/>所以它们使用矩阵抽样：把题目池分成若干题本，每个学生回答一本。<bookmark mark='c'/>总体测得很好，每个学生却测得很差。六道题无法定位一个人。<bookmark mark='d'/>所以调查报告的是群体，而不是学生。这就是为什么全国性调查不给个人分数。",
    'How then do you describe the population?':
        "那么怎样描述总体呢？<bookmark mark='a'/>每个学生的期望后验估计都被拉向均值。所以分数的离散从一降到大约零点七，两个群体之间零点四的真实差距只显示为大约零点二。<bookmark mark='b'/>似真值是从每个学生的后验中随机抽取的值，而不是后验的均值。离散恢复了，但差距仍然被压缩。<bookmark mark='c'/>从一个包含这些群体的模型，也就是条件模型中抽取，差距也恢复了。<bookmark mark='d'/>罗伯特·米斯列维在1991年阐述了这一点。似真值不是分数。对每一组分别分析，再把结果合并，就像多重插补一样。",
    'Chapter twelve. Tracking learning.': "第12章。追踪学习。",
    'Testing assumes ability holds still.':
        "测验假设能力保持不变。辅导软件的假设正好相反。<bookmark mark='a'/>1995年，阿尔伯特·科贝特和约翰·安德森把每项技能看作一个隐藏状态，未知或已知，把每次练习看作一次学会它的机会。<bookmark mark='b'/>作答是有噪声的：未掌握时的幸运猜中，已掌握时的失误。这是一个隐马尔可夫模型。<bookmark mark='c'/>Psyche模拟了五百名学生，每人练习十次，拟合恢复出了学习率、猜测率和失误率。<bookmark mark='d'/>当技能已被掌握的概率超过大约百分之九十五时，辅导系统就让学生继续前进。",
    'Here is one simulated student.':
        "这是一个模拟的学生。<bookmark mark='a'/>在每次作答之前，模型认为技能已被掌握的概率。<bookmark mark='b'/>第一次答错，使它保持在低位。然后每次答对都使它迅速上升，因为连续两次猜中不太可能。<bookmark mark='c'/>几次练习之内它就超过百分之九十五：按这个规则，达到了掌握。<bookmark mark='d'/>同样的过滤器为每项技能、每个学生运行，在被成千上万名学生使用的辅导系统中。",
    'Two other ways to track.':
        "另外两种追踪方法。<bookmark mark='a'/>来自国际象棋的埃洛等级分：每次作答之后，学习者的等级分上升，题目的等级分下降，变化量是步长乘以意外程度。<bookmark mark='b'/>在同样的作答上运行，后面的练习题看起来更容易了。但它们是同一项技能。是学习者学会了。<bookmark mark='c'/>一个假设能力不变的模型，会把学习误读为题目容易。追踪学习需要一个关于变化的模型。<bookmark mark='d'/>深度知识追踪改用了神经网络。它最初的巨大优势，在与调好的简单模型比较时缩小了。这记在账本里。",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Two new rows.':
        "两条新记录。第一条：自适应测验能用少得多的题目，常常大约一半，达到固定测验的精度。<bookmark mark='a'/>原始研究：戴维·韦斯，1982年。<bookmark mark='b'/>记录：维纳及其同事综述的自适应测验项目，以及PROMIS的自适应健康问卷。<bookmark mark='c'/>节省的多少取决于题库，并且必须控制曝光。<bookmark mark='d'/>已重复，正如第七章所计算的。",
    'The second: a neural network predicts':
        "第二条：神经网络预测学生作答的能力远好于贝叶斯知识追踪。<bookmark mark='a'/>原始研究：皮耶什及其同事，2015年。<bookmark mark='b'/>记录：加入了遗忘和能力的知识追踪与它不相上下，而重复的记录夸大了它的优势。<bookmark mark='c'/>神经模型在大型日志上的预测确实略好，但最初的差距大部分来自一个弱的基线和一个数据伪影。<bookmark mark='d'/>已重复，但更小。",
    'What the two have in common.':
        "这两条的共同点。<bookmark mark='a'/>两者都是关于效率的主张：更少的题目，更好的预测。<bookmark mark='b'/>第一条站住了，因为它背后的模型事先经过了检验。<bookmark mark='c'/>第二条缩小了，因为比较不公平：一个强的新模型对一个弱的旧模型。<bookmark mark='d'/>一种新方法的优势，最多只有旧方法最好的版本所允许的那么大。",
    'Chapter fourteen. In practice: exams, clinics and machines.': "第14章。实践中：考试、诊所与机器。",
    'Where it runs.':
        "它在哪里运行。<bookmark mark='a'/>入学考试和资格考试，其中许多是自适应的。新题目先不计分地放在正式测验里试用，然后再标定。<bookmark mark='b'/>把人放到一个共同等级尺度上的语言测验。<bookmark mark='c'/>针对疲劳、疼痛和抑郁等症状的临床题库，几道自适应问题就能代替一份长问卷。<bookmark mark='d'/>还有学习平台，在那里由知识追踪和埃洛等级分决定下一道练习。",
    'And one new kind of test-taker.':
        "还有一种新型的考生。<bookmark mark='a'/>人工智能系统的基准就是测验：难度和区分度各不相同的题目，给许多考生作答。<bookmark mark='b'/>用项目反应模型拟合这些系统的作答，一小组信息量高的题目给系统排序的效果，几乎和成千上万道题一样好。<bookmark mark='c'/>区分度很低或为负的题目常常是标错了的，而每个系统都答对的题目什么也告诉不了你。<bookmark mark='d'/>同样的问题仍然适用。题目标定了吗？它对每一类系统的功能都相同吗？当系统变化时，尺子稳定吗？《统计学，从零搭建》在第64部分讨论这个问题。",
    'Chapter fifteen. Frontier: time, generated items and learning systems.': "第15章。前沿：时间、生成的题目与学习系统。",
    'Three frontiers.':
        "三个前沿。<bookmark mark='a'/>反应时。每次作答都伴随一个时间。维姆·范德林登的层级模型把速度看作第二种特质，把第25部分的决策模型与测验连接起来。<bookmark mark='b'/>生成的题目。语言模型可以写出成千上万道题，它们的难度可以从特征上预测，但每一道仍然需要在人身上标定。<bookmark mark='c'/>还有学习系统。一个在题目之间、或在版本之间不断进步的考生，打破了能力保持不变的假设。",
    'Open questions.':
        "开放的问题。<bookmark mark='a'/>什么时候一个快速的错误回答是猜测，一个缓慢的正确回答来自一个细心的思考者？<bookmark mark='b'/>生成的题目能不能不在人身上逐一预测就完成标定？<bookmark mark='c'/>当考生，无论是人还是机器，变化得比题目还快时，尺子应该如何保持稳定？<bookmark mark='d'/>一个自适应测验能否在仍然选择信息量最大的题目的同时，对每个群体都公平？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>自适应测验出了大约十七道题。最好的固定试卷需要大约三十五道才能达到同样的精度。对于法学院的题目，拉施模型就够了：额外的斜率只换来半个点的似然。而在一道完全公平的题目上，相差零点八的两个群体相差大约十五个百分点：这是影响，不是偏差。<bookmark mark='b'/>先把题目放到同一把尺子上，测验就可以更短、更公平，并且年年可比。",
    'Part forty-five in twelve lines.':
        "用十二行总结第45部分。<bookmark mark='a'/>经典难度取决于样本，分数取决于测验。在拉施模型中，成功的对数几率是能力减去难度。这带来特定客观性和充分的总分。区分度和猜测再增加两个参数。信息量在题目之间相加，标准误是它平方根的倒数。题目参数用边际最大似然估计，能力用后验估计。自适应测验用大约一半的题目达到同样的精度。等级反应模型为评定量表建模。公平比较的是能力相同的人，因为差距不等于偏差。锚题把今年的尺子与去年的链接起来。调查用似真值报告总体。知识追踪则跟随不断变化的能力。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳，即数学无法应用于心灵，遇到了拟合真实测验、与已发表结果一致的拉施模型和等级反应模型，以及一个从零搭建的自适应测验。绿色。<bookmark mark='b'/>第二个反驳，即心灵无法被实验：题目是通过实验标定的，经过预测、偏差检查和链接。绿色。<bookmark mark='c'/>第三个，关于内省：能力是由作答测量的，而不是由对内心状态的报告测量的，但态度题目仍然依赖自我报告。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>问题与回答之间发生了什么，就在下一部分，第46部分。随时间变化的能力和学习是第47部分。拟合行为模型是第48部分。把整个文献当作证据来阅读是第50部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道计算拉施概率。一道求一道题的信息量。一道求一份测验的标准误。一道手工验证充分性。一道链接两份试卷。一道运行一步知识追踪。最后一道带星号，请你设计一份在两种语言中效果相同的自适应问卷。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。苏珊·恩布雷森和史蒂文·赖斯的书是给心理学家最友好的入门；弗雷德里克·洛德的书是经典；范德林登主编的手册涵盖了这一部分的每个模型，还有更多。",
    'Two parts of the graduate toolkit done.':
        "研究生工具箱完成了两个部分。<bookmark mark='a'/>这一部分把回答了不同问题的人放到了同一把尺子上。<bookmark mark='b'/>接下来是回答本身。如何把“我更喜欢这个”变成一个数字，在问题和回答之间又发生了什么？第46部分：标度、调查与选择。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
