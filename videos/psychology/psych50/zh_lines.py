"""Chinese narration for psych50: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第50部分：证据的分量'

CHAPTERS = {
    'Hook': '两摞试验',
    'Predict': '1. 在你身上：一个不可能的均值，以及四个数字',
    'Pool': '2. 合并研究',
    'Moderators': '3. 调节变量',
    'Funnel': '4. 看见过滤',
    'Correct': '5. 对它进行校正',
    'Replications': '6. 元分析与重复研究的对照',
    'Designs': '7. 去除过滤的研究设计',
    'Forensics': '8. 法证统计学',
    'Fraud': '9. 伪造，被发现了',
    'Analysts': '10. 许多分析者，一份数据',
    'Theory': '11. 理论危机',
    'Audit': '12. 审计账本',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：综述、供应商与文件抽屉',
    'Frontier': '15. 前沿：比率、机器人与激励',
    'Outro': '回顾、习题与前路',
}

ZH = {
    "In 2008 Erick Turner and colleagues put two piles side by side. <bookmark mark='a'/> In on":
        "2008年，埃里克·特纳及同事把两摞材料并排放在一起。<bookmark mark='a'/>一摞是在美国监管机构登记的七十四项抗抑郁药试验。另一摞是期刊刊登出来的内容。<bookmark mark='b'/>按照监管机构的解读，大约一半的试验结果是阳性的。<bookmark mark='c'/>这些试验几乎全部发表了。其余的大多根本没有发表，或者被写得好像是阳性的。<bookmark mark='d'/>所以在期刊上，几乎每一项试验看起来都是阳性的，平均效应看起来比实际大了大约三分之一。<bookmark mark='e'/>药物并非无用。是文献被过滤了。",
    "Psyche can build the same two piles. <bookmark mark='a'/> Seventy-four trials of a drug wi":
        "Psyche可以搭建同样的两摞。<bookmark mark='a'/>七十四项试验，药物有真实而适度的效应。每一项阳性试验都发表了，其余的发表了大约三分之一。<bookmark mark='b'/>左边是全部七十四项，大约一半是阳性的。右边是发表的五十一项，四分之三是阳性的。<bookmark mark='c'/>合并全部试验，效应约为零点三一。只合并发表的，约为零点三七。没有任何造假。光是过滤就造成了这一切。",
    'So this part asks what a whole literature says, and whether it can be trusted to say it. <':
        "所以这一部分要问：整个文献在说什么，它说的能信吗？<bookmark mark='a'/>合并研究，以及研究中隐藏的调节变量。<bookmark mark='b'/>看见过滤，并对它进行校正。<bookmark mark='c'/>去除过滤的研究设计，以及抓出不可能数字的法证方法。<bookmark mark='d'/>许多分析者、薄弱的理论，以及用这个系列自己的工具审计这个系列自己的账本。",
    "This is Part 50 of Psychology, Built: the weight of evidence. <bookmark mark='a'/> We'll c":
        "这是《心理学，从零搭建》的第50部分：证据的分量。<bookmark mark='a'/>我们将用固定效应和随机效应合并研究，并画出预测区间。我们将看到调节变量为什么会隐藏起来。我们将阅读漏斗图，并在已知真相的文献上运行每一种校正方法。我们将看到注册报告去除了什么。我们将用GRIM、SPRITE和statcheck检验报告的数字，看看伪造的数据是如何被发现的。我们还将画出一条设定曲线，认识米尔的悖论，并用账本自己的工具审计账本。",
    'Chapter one. On you: a mean that cannot be, and four numbers.':
        '第1章。在你身上：一个不可能的均值，以及四个数字。',
    "First, a test you can do in your head. <bookmark mark='a'/> Twenty-eight people each give ":
        "首先，一个你可以在脑子里做的检验。<bookmark mark='a'/>二十八个人每人给出一到七之间的一个整数。<bookmark mark='b'/>所以总和是一个整数，均值就是这个总和除以二十八。<bookmark mark='c'/>总和一百四十五得到五点一八。一百四十六得到五点二一。没有任何总和能得到五点一九。<bookmark mark='d'/>所以报告的均值五点一九是不可能的：一个笔误、一次没人提到的排除，或者更糟。<bookmark mark='e'/>在课程网站上，你可以亲自检验五个报告的均值。",
    "Now four numbers. <bookmark mark='a'/> One: twenty-eight people answer one question on a o":
        "现在是四个数字。<bookmark mark='a'/>第一：二十八个人在一到七的量表上回答一个问题，论文报告的均值是五点一九。可能吗？<bookmark mark='b'/>第二：一种药的真实效应是零点二，只有显著的试验外加少数其他试验被发表。对已发表试验的元分析会发现什么？<bookmark mark='c'/>第三：一份真实效应很小的数据，九十六种说得通的分析。有多大比例结果显著？<bookmark mark='d'/>第四：在这个系列的账本迄今为止的两百六十三项发现中，有多大比例失败或被撤回？在这里暂停，把它们写下来。",
    'Chapter two. Combining studies.':
        '第2章。合并研究。',
    "There are two models of a literature. <bookmark mark='a'/> The fixed-effect model says eve":
        "一个文献有两种模型。<bookmark mark='a'/>固定效应模型说，每项研究估计的是同一个真实效应，所以每项研究按其精度加权。<bookmark mark='b'/>随机效应模型说，每项研究都有自己的真实效应，以标准差tau围绕一个均值分布。<bookmark mark='c'/>当tau大于零时，与固定权重相比，大研究的分量减少，小研究的分量增加，而I平方是变异中真实部分的比例。<bookmark mark='d'/>心理学的效应随样本、材料和实验室而变化，所以随机效应是通常的默认选择。《统计学，从零搭建》在它的第25部分推导了这两种模型。",
    "Here's a forest plot, built by hand. <bookmark mark='a'/> Fifteen simulated studies, each ":
        "这是一张手工搭建的森林图。<bookmark mark='a'/>十五项模拟研究，每项是一个按权重确定大小的方块，带着它的区间。<bookmark mark='b'/>随机效应的均值约为零点四一，区间约从零点三到零点五：那个金色的菱形。<bookmark mark='c'/>tau约为零点一七，I平方约为一半：研究之间的离散有一半是真实的。<bookmark mark='d'/>红线是预测区间：一项新研究的真实效应可能落在的范围。从几乎为零到将近零点八。",
    "Two intervals, two questions. <bookmark mark='a'/> The confidence interval is about the av":
        "两个区间，两个问题。<bookmark mark='a'/>置信区间关乎像这样的研究的平均效应。<bookmark mark='b'/>预测区间关乎下一项研究，或你自己情境中的效应。<bookmark mark='c'/>存在真实的异质性时，后者要宽得多，而实践者需要的正是它。<bookmark mark='d'/>研究很少时，要用哈通和克纳普基于t分布的区间，因为通常的区间太窄了。<bookmark mark='e'/>还要报告tau，而不只是I平方。I平方取决于研究有多精确。tau的单位就是效应的单位。",
    'Chapter three. Moderators.':
        '第3章。调节变量。',
    "When effects vary, ask why. <bookmark mark='a'/> A feature of each study, such as the age ":
        "当效应各不相同时，要问为什么。<bookmark mark='a'/>每项研究的一个特征，比如样本的年龄、剂量，或者是否在线进行，成为它的效应的一个预测变量。<bookmark mark='b'/>这是一个以研究为个案、按精度加权的回归，剩余的离散是tau平方。<bookmark mark='c'/>但它的个案很少，它的预测变量也不是随机分配的。在一个特征上不同的研究，在许多别的方面也不同。<bookmark mark='d'/>所以调节变量是跨研究的一种相关，就像第47部分的人际间斜率：一个需要通过设计来检验的假设。",
    "And moderators hide. <bookmark mark='a'/> Make half the studies' true effect larger by zer":
        "而且调节变量会隐藏起来。<bookmark mark='a'/>让一半研究的真实效应大零点二，同时另有其他真实变异。<bookmark mark='b'/>有二十项研究时，找到这个调节变量的概率不到三分之一。有四十项时，略多于一半。<bookmark mark='c'/>要达到百分之八十的统计功效，大约需要八十项研究。<bookmark mark='d'/>所以在一项典型的元分析中，没有找到调节变量说明不了多少。而在尝试过的许多调节变量中找到一个，又是第4部分的岔路花园。",
    'Chapter four. Seeing the filter.':
        '第4章。看见过滤。',
    "Here's what a filter looks like. <bookmark mark='a'/> Each dot is a study, placed by its e":
        "这就是过滤的样子。<bookmark mark='a'/>每个点是一项研究，按其效应和标准误放置。小研究位置高、分布宽。<bookmark mark='b'/>没有过滤时，点云是一个围绕真值对称的漏斗。灰色的点是进行过的每一项研究。<bookmark mark='c'/>蓝色的是发表了的。红线是一项研究变得显著的位置，它左边的小研究不见了。<bookmark mark='d'/>这是一个被咬掉了一边的漏斗。发表了的小研究是运气好的那些。",
    "Two tools read the bite. <bookmark mark='a'/> Egger's test regresses each study's effect o":
        "两种工具来解读这个缺口。<bookmark mark='a'/>埃格检验把每项研究的效应对其标准误做回归。斜率意味着小研究显示出更大的效应，这里它明显存在。<bookmark mark='b'/>截距是一项完全没有误差的研究会发现的效应。这就是PET，这里它给出约零点一三。<bookmark mark='c'/>朴素的合并估计约为零点四一，而真值是零点二。<bookmark mark='d'/>PEESE把直线弯曲，给出约零点三。PET-PEESE按一条规则在两者之间选择。两者都不恰好是真值，下一章要问它们中任何一个对的频率有多高。",
    "But not every lopsided funnel is publication bias. <bookmark mark='a'/> Small studies may ":
        "但并不是每一个歪斜的漏斗都是发表偏倚。<bookmark mark='a'/>小研究可能真的有更大的效应：更密集的处理、更精挑的样本、更好的执行保真度。<bookmark mark='b'/>恰好与研究规模对齐的异质性会造成同样的斜率。<bookmark mark='c'/>有些效应量与它们自己的标准误相关联，这会通过算术让漏斗倾斜。<bookmark mark='d'/>而研究很少时，单凭偶然就会让漏斗歪斜。<bookmark mark='e'/>不对称是关于小样本研究效应的一个警告。只有预先注册才能显示缺失的研究。",
    'Chapter five. Correcting for it.':
        '第5章。对它进行校正。',
    "Five families of correction. <bookmark mark='a'/> Trim-and-fill trims the studies that mak":
        "校正有五大类。<bookmark mark='a'/>剪补法剪掉让漏斗歪斜的研究，补上它们的镜像，再重新合并。<bookmark mark='b'/>PET-PEESE取标准误为零时的效应，来自上一章的回归。<bookmark mark='c'/>选择模型对过滤本身建模，也就是一项不显著研究被发表的概率，并把它与效应一起估计。<bookmark mark='d'/>p曲线只使用显著的结果，追问什么样的真实效应会让它们的p值呈现出现在的样子。<bookmark mark='e'/>z曲线做同样的事，同时允许研究的统计功效各不相同。",
    "Psyche runs all of them on literatures where the truth is known. <bookmark mark='a'/> Fift":
        "Psyche在已知真相的文献上运行所有这些方法。<bookmark mark='a'/>每一行五十个模拟文献。每个格子是一种方法的平均估计值，接近真值时为绿色，远离时为红色。<bookmark mark='b'/>在底部没有过滤时，一切都有效。<bookmark mark='c'/>有过滤时，朴素估计和剪补法都远高于真值。<bookmark mark='d'/>PET-PEESE平均而言是无偏的，但在什么都没有时波动很大。<bookmark mark='e'/>当研究真的各不相同时，p曲线就失效了：在异质性那一行，它报告的值是真值的两倍多。<bookmark mark='f'/>选择模型表现最好，但只是因为Psyche的过滤恰好是它所假定的那一种。真实的过滤没有这么整齐。",
    "So no method works everywhere. <bookmark mark='a'/> In 2019 Evan Carter and colleagues ran":
        "所以没有一种方法处处有效。<bookmark mark='a'/>2019年，埃文·卡特及同事在许多种模拟文献上做了同样的练习，每种方法都在某处失败了。<bookmark mark='b'/>每种校正都假定了一种特定的过滤。当真实的过滤不同时，答案也就不同。<bookmark mark='c'/>报告几种方法，把它们之间的分歧当作诚实的不确定性。<bookmark mark='d'/>这些方法发现问题的能力强于修复问题的能力。修复的办法是停止过滤。",
    'Chapter six. Meta-analyses against replications.':
        '第6章。元分析与重复研究的对照。',
    "What happens when the same effect is measured both ways? <bookmark mark='a'/> Psyche makes":
        "当同一个效应用两种方式测量时，会发生什么？<bookmark mark='a'/>Psyche制造了十个小的真实效应。对每一个，有一个包含六十项研究的被过滤的文献，以及一项每组一千五百人的重复研究。<bookmark mark='b'/>每个点都在对角线上方。元分析的结果平均约为重复研究的两倍半。<bookmark mark='c'/>2020年，阿曼达·克瓦文、埃里克·斯特罗姆兰和马格努斯·约翰内松找到了十五个既有元分析、又有多地点预先注册重复研究的真实效应。元分析的结果大约大了三倍。<bookmark mark='d'/>校正方法缩小了差距，但没有消除它，正如上一章所预测的。",
    "So a meta-analysis can be precise and wrong. <bookmark mark='a'/> Pooling more filtered st":
        "所以一项元分析可能既精确又错误。<bookmark mark='a'/>合并更多被过滤的研究，只会让区间围绕错误的数字变窄。<bookmark mark='b'/>一项元分析不可能比它所合并的文献更好。<bookmark mark='c'/>一项大型的预先注册研究，分量可以超过一百项未注册的小研究。<bookmark mark='d'/>这就是为什么账本的记录大多是多地点重复研究，而不是元分析。",
    'Chapter seven. Designs that remove the filter.':
        '第7章。去除过滤的研究设计。',
    "The filter can be prevented. <bookmark mark='a'/> A registered report is reviewed and acce":
        "过滤是可以预防的。<bookmark mark='a'/>注册报告在数据产生之前就接受评审并被接收。被评判的是问题和方法，无论发现了什么，论文都会发表。<bookmark mark='b'/>2021年，安妮·谢尔、米切尔·席延和丹尼尔·拉肯斯把它们与标准论文作了比较。百分之九十六的标准论文支持了它们的第一个假设。注册报告则是百分之四十四。<bookmark mark='c'/>那是第43部分的一行。这个差距正是过滤所预测的，尽管注册报告也可能提出更冒险的问题。<bookmark mark='d'/>对一个文献而言，解药是分母：进行过的每一项研究都可见。",
    "Three more designs do the same. <bookmark mark='a'/> Trial registries: every clinical tria":
        "还有三种设计也能做到这一点。<bookmark mark='a'/>试验注册库：每一项临床试验在开始之前就登记，并写明其结局指标。那就是特纳能够清点的那一摞。<bookmark mark='b'/>多地点方案：一个方案，许多实验室，每个结果都报告，就像第43部分那样。没有哪个实验室能把自己的阴性结果收进抽屉。<bookmark mark='c'/>还有序贯设计：事先规划好查看数据的时机，用边界来守住错误率。那是第4部分的偷看，变得诚实了。每一种都通过让报告的决定独立于结果而起作用。",
    'Chapter eight. Forensic statistics.':
        '第8章。法证统计学。',
    "The opening's test has a name. <bookmark mark='a'/> In 2017 Nick Brown and James Heathers ":
        "开头的那个检验有一个名字。<bookmark mark='a'/>2017年，尼克·布朗和詹姆斯·希瑟斯称之为GRIM：n个整数回答的均值必须是n分之一的倍数，误差在舍入范围内。<bookmark mark='b'/>对小样本而言，许多报告的均值根本不可能出现。这里有五个，其中两个是不可能的。<bookmark mark='c'/>他们检验了已发表论文中的均值，发现许多不一致，其中一些导致了更正和撤稿。<bookmark mark='d'/>它只需要均值、样本量和量表。",
    'GRIM checks a mean. SPRITE checks a mean and a standard deviation together. <bookmark mark':
        "GRIM检验一个均值。SPRITE同时检验一个均值和一个标准差。<bookmark mark='a'/>詹姆斯·希瑟斯及同事提出，搜索符合报告的均值、标准差、样本量和量表的样本。<bookmark mark='b'/>Psyche的搜索为这里的每一对都找到了一个二十人的样本，所以这些数字是可能的。<bookmark mark='c'/>如果没有样本符合，或者唯一符合的样本很荒谬，比如每个人都回答一或七，那么这些数字就值得追问。<bookmark mark='d'/>重构出来的不是数据。它显示的是数据可能是什么样子。",
    "A third check reads the statistics themselves. <bookmark mark='a'/> A reported t, its degr":
        "第三种检验读的是统计量本身。<bookmark mark='a'/>报告的t值、它的自由度和它的p值必须一致。这里有六个；其中一个声称p小于零点零五，而检验给出的约为零点零八。<bookmark mark='b'/>2016年，米歇尔·纽伊滕及同事用一个程序检查了八种期刊中超过二十五万个p值。大约一半的论文至少有一处不一致，大约八分之一的论文有一处跨越了零点零五。<bookmark mark='c'/>大多数错误很小。跨越那条线的错误偏向于显著。",
    'Chapter nine. Fabrication, detected.':
        '第9章。伪造，被发现了。',
    "Sometimes the numbers are invented. <bookmark mark='a'/> A 2012 field study reported that ":
        "有时数字是编造出来的。<bookmark mark='a'/>一项2012年的现场研究报告说，在保险单的顶部而不是底部签署诚实保证，会让客户更诚实地报告自己的里程。<bookmark mark='b'/>2021年，独立分析者查看了公开的数据。行驶里程从零到五万均匀分布，没有一个高于五万。<bookmark mark='c'/>真实的驾驶里程会在中等距离处堆积，然后缓慢变稀，就像蓝色的条形。均匀分布、边缘陡峭的数字，就像红色的那些，正是随机数生成器制造出来的。<bookmark mark='d'/>这篇论文被撤回了，后来的一项大型研究发现先签名没有任何效果。",
    "What gives fabrication away? <bookmark mark='a'/> Distributions: too flat, too smooth, or ":
        "是什么暴露了伪造？<bookmark mark='a'/>分布：太平、太光滑，或者在真实数据应当逐渐变少的地方有一个陡峭的边缘。<bookmark mark='b'/>数字：末位数字分布不均匀，或者在测量值应当精确的地方出现了取整的值。<bookmark mark='c'/>好得过头的结果：效应在研究之间过于一致，或者方差相对于样本量过于相似。<bookmark mark='d'/>还有文件本身：电子表格的历史、字体和排序显示出手工添加的行。所有这些都需要数据。开放数据让造假变得可以发现。第36部分的拉票研究也是这样被发现的。",
    'Chapter ten. Many analysts, one dataset.':
        '第10章。许多分析者，一份数据。',
    "How much does the analyst matter? <bookmark mark='a'/> In 2018 Raphael Silberzahn, Eric Uh":
        "分析者有多重要？<bookmark mark='a'/>2018年，拉斐尔·西尔伯察恩、埃里克·乌尔曼及同事给二十九个团队同样的数据和一个问题：肤色较深的足球运动员会被裁判出示更多红牌吗？<bookmark mark='b'/>各团队选择了不同的模型、协变量和排除规则。他们的估计从没有效应到将近三倍的比值不等。<bookmark mark='c'/>大约三分之二发现了显著效应，三分之一没有。<bookmark mark='d'/>离散来自分析，就像第49部分的七十个团队，没有任何人行为不端。",
    "The remedy is to show every analysis at once. <bookmark mark='a'/> One simulated dataset w":
        "补救办法是同时展示每一种分析。<bookmark mark='a'/>一份真实效应很小的模拟数据，九十六种说得通的分析：用哪些协变量、哪种异常值规则、原始值还是取对数。<bookmark mark='b'/>排序后，估计值从几乎为零到约零点二，金色的是显著的：大约一半。<bookmark mark='c'/>萨拉·斯蒂根及同事称之为多元宇宙，乌里·西蒙松、约瑟夫·西蒙斯和莱夫·纳尔逊则称之为设定曲线。<bookmark mark='d'/>展示整条曲线，而不是你喜欢的那一种分析。",
    'Chapter eleven. The theory crisis.':
        '第11章。理论危机。',
    "Some argue the deepest problem was never statistics. <bookmark mark='a'/> Paul Meehl spent":
        "有人认为最深层的问题从来就不是统计。<bookmark mark='a'/>保罗·米尔花了几十年对比物理学和他所说的“软心理学”。<bookmark mark='b'/>在物理学中，一个理论预测一个数字，所以更好的测量让检验更难，理论可能无法通过。<bookmark mark='c'/>在心理学的许多领域，一个理论只预测一个方向，所以更好的测量反而让检验更容易。<bookmark mark='d'/>这是因为在真实数据中，几乎所有东西都和几乎所有东西有一点相关。米尔称之为“垃圾因子”。<bookmark mark='e'/>所以一个方向符合预测的显著结果，无论样本多大，对理论来说都是很弱的证据。",
    "Here's Meehl's paradox, computed. <bookmark mark='a'/> In Psyche's world every pair of var":
        "这是计算出来的米尔悖论。<bookmark mark='a'/>在Psyche的世界里，每一对变量都有一点相关，而一个毫无真理成分的理论随机预测一个方向。<bookmark mark='b'/>用三十个人，它的预测中大约有百分之六在预测方向上显著。<bookmark mark='c'/>用一万个人，约百分之四十四：接近一半，对于一个一无所知的理论而言。<bookmark mark='d'/>大样本治得了噪声，治不了薄弱的理论。",
    "What would stronger theories look like? <bookmark mark='a'/> They predict numbers, or at l":
        "更强的理论会是什么样子？<bookmark mark='a'/>它们预测数字，或者至少是数据可能与之矛盾的形状和顺序。这是第48部分的问题：这个模型排除了什么？<bookmark mark='b'/>它们是形式模型，写成程序，所以预测是推导出来的，而不是争论出来的。<bookmark mark='c'/>它们用强推断来检验：两个对立的理论，以及一个其中之一必定失败的实验。<bookmark mark='d'/>它们还说明一个主张覆盖什么：哪些人、哪些刺激、哪些情境。<bookmark mark='e'/>第4部分的改革让检验变得诚实。只有更好的理论才能让检验变得严格。",
    'Chapter twelve. The Ledger, audited.':
        '第12章。审计账本。',
    "Now the series audits itself. <bookmark mark='a'/> Through Part 49 the Ledger holds two hu":
        "现在这个系列审计它自己。<bookmark mark='a'/>到第49部分为止，账本收录了两百六十三项发现。<bookmark mark='b'/>大约三分之二站住了，包括那些效应变小了的，以及教科书故事是错的那些。<bookmark mark='c'/>大约五分之一有争议。<bookmark mark='d'/>大约七分之一失败或被撤回。",
    "Where did the findings hold? <bookmark mark='a'/> By act, perception, learning and cogniti":
        "这些发现在哪里站住了？<bookmark mark='a'/>按幕来看，知觉、学习和认知站住的比例在百分之八十或以上。<bookmark mark='b'/>动机、发展、社会和临床心理学大约站住一半，并且占了大部分失败。<bookmark mark='c'/>按原始研究的年代来看，1960年以前的发现几乎总能站住，二十一世纪头十年的发现大约站住一半。",
    "Read the audit with this part's own tools. <bookmark mark='a'/> The Ledger isn't a random ":
        "用这一部分自己的工具来解读这次审计。<bookmark mark='a'/>账本不是一个随机样本。它收录的是一门课程会讲授的发现，既有著名的，也有有争议的。<bookmark mark='b'/>老的发现有一个世纪的时间接受检验，失败了就会被遗忘。幸存者偏差美化了过去。<bookmark mark='c'/>对知觉和学习的精确、可重复的测量构成强检验。依赖情境、用小样本研究的效应构成弱检验。<bookmark mark='d'/>这与重复研究项目发现的模式相同：能否幸存可以由样本量、效应量以及主张有多令人意外来预测。<bookmark mark='e'/>每一行都有它的来源和核查日期，所以这次审计可以重做，也应该重做。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Five new rows. The first: the journal literature on antidepressants overstated their effic':
        "新增五行。第一行：关于抗抑郁药的期刊文献夸大了它们的疗效。<bookmark mark='a'/>原始研究：特纳及同事，2008年。<bookmark mark='b'/>后续记录：对监管机构数据的元分析，以及一项包括未发表试验在内、涵盖五百多项试验的网络元分析。<bookmark mark='c'/>药物有效，但效果适度。已发表的记录让它们看起来更好。<bookmark mark='d'/>已重复。",
    'The second: meta-analyses of published studies estimate effects about as large as large pr':
        "第二行：对已发表研究的元分析估计出的效应，与大型预先注册重复研究的估计大致一样大。<bookmark mark='a'/>原始研究：以2010年的自我损耗元分析为例。<bookmark mark='b'/>后续记录：第43部分的注册重复研究，以及克瓦文及同事的十五项比较，元分析的结果大约大了三倍。<bookmark mark='c'/>元分析继承了它的文献的过滤。<bookmark mark='d'/>失败。",
    "The third: a substantial share of psychology articles report a p-value that doesn't match ":
        "第三行：相当一部分心理学论文报告的p值与它自己的检验统计量不符。<bookmark mark='a'/>原始研究：巴克和维彻茨，2011年。<bookmark mark='b'/>后续记录：statcheck对二十五万个p值的普查，发现大约一半的论文至少有一处不一致。<bookmark mark='c'/>大多数错误很小，严重的那些偏向于显著。<bookmark mark='d'/>已重复。",
    "The fourth: researchers' pooled beliefs predict which findings will replicate. <bookmark m":
        "第四行：研究者汇总起来的信念能预测哪些发现会重复成功。<bookmark mark='a'/>原始研究：德雷伯及同事的预测市场，2015年。<bookmark mark='b'/>后续记录：后来的重复研究项目中的预测市场和调查。<bookmark mark='c'/>这个领域本来能分辨出来；它还是发表了那些脆弱的发现。<bookmark mark='d'/>已重复。",
    'And the fifth: discoveries made with rigour-enhancing practices replicate at near the rate':
        "第五行：用增强严谨性的做法得出的发现，重复成功的比率接近其统计功效所预测的比率。<bookmark mark='a'/>原始研究：普罗茨科及同事，2023年。<bookmark mark='b'/>后续记录：这篇论文在2024年因其自身的预先注册和报告问题被撤回。<bookmark mark='c'/>这些做法仍然是合理的；支持它们的这份证据没有了。<bookmark mark='d'/>已撤回。",
    "What the five have in common. <bookmark mark='a'/> All five are about the literature itsel":
        "这五行的共同点。<bookmark mark='a'/>五行都关乎文献本身：什么被发表、如何被合并、如何被报告，以及这个领域对自己的薄弱之处了解得有多清楚。<bookmark mark='b'/>只有在存在分母的地方，过滤才是可见的：一个注册库、一个多实验室方案、一整套p值。<bookmark mark='c'/>改革者自己的工作也受到同样标准的检验。有一行是撤稿。<bookmark mark='d'/>所以这一部分问题的答案是：证据的分量，就是那些无论发现了什么都会被看见的研究的分量。",
    'Chapter fourteen. In practice: reviews, vendors and file drawers.':
        '第14章。实践中：综述、供应商与文件抽屉。',
    "Where is a literature weighed for a decision? <bookmark mark='a'/> In evidence reviews, me":
        "在哪里为了做决定而权衡一个文献？<bookmark mark='a'/>在证据综述中，医学和政策领域按方案合并试验：检索一切，包括注册库和未发表的数据，评定确定性等级，并说明理由。<bookmark mark='b'/>在对供应商“有科学证明”这一说法的尽职调查中：哪些研究、一共做了多少、谁出的钱，以及预测区间对你自己的情境说了什么。<bookmark mark='c'/>在指南中，当合并估计缩小时，指南应当改变，而它们往往比证据滞后好几年。<bookmark mark='d'/>还有在新闻报道中，一项新研究就是一项研究，真正的新闻是它在漏斗中所处的位置。",
    "Every organization has its own file drawer. <bookmark mark='a'/> A company runs hundreds o":
        "每个组织都有自己的文件抽屉。<bookmark mark='a'/>一家公司每年做数百项实验。胜出的那些被展示出来，其余的被遗忘。<bookmark mark='b'/>那个胜出者档案就是一个被过滤的文献。它的平均提升被夸大了，和开头完全一样。<bookmark mark='c'/>所以要把每一项实验，连同事先声明的指标和结果，保存在一个可检索的登记册里。<bookmark mark='d'/>然后合并它们，用第48部分的层级方法把胜出者向基础率收缩，并在以它们为基础继续推进之前，把最大的那些再测一次。<bookmark mark='e'/>在这里，分母同样是解药。",
    'Chapter fifteen. Frontier: rates, robots and incentives.':
        '第15章。前沿：比率、机器人与激励。',
    "Three frontiers. <bookmark mark='a'/> Are replication rates rising? Larger samples and pre":
        "三个前沿。<bookmark mark='a'/>重复成功率在上升吗？自2015年以来，更大的样本和预先注册已经普及。更新的发现是否重复得更好，正在测量之中，目前尚不清楚。<bookmark mark='b'/>自动化检查：statcheck、GRIM及其后继者现在在投稿时就运行，语言模型也在阅读论文寻找错误，而它们自己的错误率也有待测量。<bookmark mark='c'/>还有作为演化的激励。2016年，保罗·斯马尔迪诺和理查德·麦克尔里思表明，如果发表更多的实验室被效仿，那么产生更多假阳性的方法就会传播开来，而无需任何人作弊。第61部分会再谈这一点。",
    "Open questions. <bookmark mark='a'/> Can a filtered literature ever be corrected after the":
        "开放的问题。<bookmark mark='a'/>一个被过滤的文献能在事后被校正吗，还是只能被取代？<bookmark mark='b'/>一个领域的发现中应该有多大比例被重复，重复哪些？<bookmark mark='c'/>一项元分析应该如何权衡一项注册研究和一项未注册研究？<bookmark mark='d'/>如果是否发表总是在结果出来之前就决定，文献会是什么样子？",
    "First, your four numbers. <bookmark mark='a'/> A mean of five point one nine from twenty-e":
        "首先，你的四个数字。<bookmark mark='a'/>二十八个整数回答得出五点一九的均值是不可能的。一个真实效应为零点二的被过滤文献，合并后约为零点四。九十六种说得通的分析中大约一半结果显著。账本中大约七分之一的行失败或被撤回。<bookmark mark='b'/>一个文献作为证据的分量，与其中无论发现了什么都会被看见的部分成正比。",
    "Part fifty in twelve lines. <bookmark mark='a'/> The published pile isn't the pile of stud":
        "第五十部分，十二行。<bookmark mark='a'/>发表的那一摞不是进行过的研究的那一摞。固定效应假定只有一个真值，随机效应假定一个分布，而预测区间回答的是实践者的问题。调节变量会隐藏起来，因为元回归的个案很少，而且没有随机分配。被过滤的漏斗被咬掉了一块，可以用埃格检验、PET和PEESE来解读。每一种校正方法都会在某处失败，被过滤的元分析的结果约为重复研究的三倍。注册报告去除了过滤。GRIM、SPRITE和statcheck不需要数据就能检验数字，而开放数据让伪造变得可以发现。有许多分析者和一份数据时，要展示整条曲线。大样本治得了噪声，治不了薄弱的理论。",
    "Kant's wager. <bookmark mark='a'/> The first objection met pooling, correction and forensi":
        "康德的赌注。<bookmark mark='a'/>第一条反对意见遇到了合并、校正和法证方法，每一种都在已知真相的文献上检验过。绿色。<bookmark mark='b'/>第二条遇到了注册和多地点的设计：对科学本身的运作方式所做的实验。绿色。<bookmark mark='c'/>还有第三条。审计清点的是结果而不是报告，但一个领域的信念仍然在引导它选择检验什么。琥珀色。",
    "Where this comes back. <bookmark mark='a'/> Every part of Act Twelve, psychology at work, ":
        "这些内容会在哪里再次出现。<bookmark mark='a'/>第十二幕“工作中的心理学”的每一部分都用这个标准来评判自己的做法。激励和科学的科学是第61部分。而这个系列以一篇必须达到这个标准的学位论文结束，那是第62部分。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One pools ":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道合并三项研究。一道求I平方。一道画出预测区间。一道应用GRIM。一道重新计算一个p值。一道决定当PET和朴素估计不一致时该报告什么。最后带星号的一道，请你为一个你怀疑被过滤了的文献规划一项元分析。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Borenstein and co':
        '这一部分所依据的书籍和论文列在这里，也列在README中。博伦斯坦及同事教的是元分析；特纳的论文是对过滤最清晰的描绘；米尔1978年的论文至今仍是关于一个显著结果能说明什么的最尖锐的论证。',
    "The graduate toolkit is complete. <bookmark mark='a'/> Seven parts built the methods a res":
        "研究生工具箱完成了。<bookmark mark='a'/>七个部分搭建了研究者在学位之后使用的方法，而这一部分把它们用在了文献本身。<bookmark mark='b'/>第十二幕把心理学带到工作中：驾驶舱和控制室、产品和办公室、教室、法庭和诊所。它从设计遇到第三幕到第六幕所讲的人的局限的地方开始。第51部分：人因学。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
