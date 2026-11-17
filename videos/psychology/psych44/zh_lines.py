"""Chinese narration for psych44: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第44部分：潜变量'

CHAPTERS = {
    'Hook': '一个矩阵，三个图表',
    'Predict': '1. 在你身上：画一个模型，四个数字',
    'Paths': '2. 赖特的路径',
    'Cfa': '3. 因子模型，验证性的',
    'Estimate': '4. 最大似然估计',
    'Fit': '5. 拟合吗？',
    'Full': '6. 测量与结构',
    'Invariance': '7. 测量不变性',
    'Mediation': '8. 中介',
    'Equivalent': '9. 等价模型',
    'Time': '10. 随时间的潜变量',
    'Networks': '11. 因子还是网络？',
    'Reading': '12. 读一篇SEM论文',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：调查、测验与人力分析',
    'Frontier': '15. 前沿：因果发现、贝叶斯与动态拟合',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'Here is a correlation matrix for three variables.':
        "这是三个变量的相关矩阵。<bookmark mark='a'/>一千名模拟个体，由一条链生成：X导致M，M导致Y。<bookmark mark='b'/>现在拟合三个图表：这条链、反过来的链，以及一个以M为两者共同原因的分叉。它们拟合这些数据完全一样好，精确到小数点后两位。<bookmark mark='c'/>数据说不出哪个图表是真的。只有研究的设计能说。",
    'The idea has two roots.':
        "这个想法有两个源头。<bookmark mark='a'/>1921年，遗传学家休厄尔·赖特在变量之间画上箭头，并说明它们的相关如何从箭头得出。他称之为路径分析。<bookmark mark='b'/>斯皮尔曼早已用一个看不见的共同因子来解释相关，见第32部分。<bookmark mark='c'/>1969年，卡尔·约雷斯科格把两者结合起来：由指标测量的因子，因子之间的箭头，全部用最大似然估计。<bookmark mark='d'/>结构方程模型成了心理学陈述关于不可观测之物的理论的标准方式。它的常见滥用，是忘记那些拟合得同样好的图表。",
    'So this part asks how to model something you can':
        "所以这一部分要问：如何为你观察不到的东西建模，又如何知道这个模型不是虚构。<bookmark mark='a'/>路径、因子，以及把它们连起来的模型。<bookmark mark='b'/>估计、拟合，以及人们用来评判它的临界值。<bookmark mark='c'/>不变性、中介，以及拟合得同样好的模型。<bookmark mark='d'/>还有时间、网络，以及如何阅读一篇用到这一切的论文。",
    'This is Part 44 of Psychology, Built':
        "这是《心理学，从零搭建》第44部分：潜变量，也是研究生工具箱的开端。<bookmark mark='a'/>我们将推导赖特的追踪规则。我们将构建因子模型，识别它，并用最大似然估计它。我们将评判拟合：卡方检验、RMSEA、CFI，以及取决于模型的临界值。我们将对回归做不可靠性校正，并检验一个测量在两个群体中意思是否相同。我们将看到中介为何仍然是相关性的。我们还会遇到等价模型、随时间的增长，以及因子与网络之争。",
    'Chapter one. On you: draw a model, and four numbers.': "第1章。在你身上：画一个模型，四个数字。",
    'First, three stories.':
        "先看三个故事。<bookmark mark='a'/>压力扰乱睡眠，睡眠使情绪变差。或者情绪低落扰乱睡眠，睡眠加重压力。或者睡眠差同时加重压力和情绪低落。<bookmark mark='b'/>把每个故事画成图表。三个都蕴含同样的相关矩阵，对任何数据都拟合得一样好。<bookmark mark='c'/>同样三个变量上，有一个图表确实不同：压力和情绪都扰乱睡眠。它蕴含压力与情绪不相关，因此可以被拒绝。在课程网站上，你可以试着画一个和真实模型拟合得同样好的模型。",
    'Now four numbers to write down before the part answers them.':
        "现在写下四个数字，等这一部分来回答。<bookmark mark='a'/>一：九项能力测验、三个因子、三百零一名儿童。模型能通过精确拟合的卡方检验吗？<bookmark mark='b'/>二：两种特质相关零点五，每种由三个载荷为零点六的条目测量。总分之间的相关是多少？<bookmark mark='c'/>三：一个随机化的治疗，一个测量的中介，没有真实的间接效应。分析仍然能找到一个吗？<bookmark mark='d'/>四：有多少个不同的图表能与真实图表一样好地拟合一个相关矩阵？在这里暂停，把它们写下来。",
    "Chapter two. Wright's paths.": "第2章。赖特的路径。",
    "Wright's rule turns arrows into correlations.":
        "赖特的规则把箭头变成相关。<bookmark mark='a'/>取标准化的变量，箭头表示直接效应，没有回路。<bookmark mark='b'/>两个变量的相关，等于连接它们的每一条路径上各系数乘积之和。<bookmark mark='c'/>路径可以先逆着箭头走、再顺着走，但不能先顺后逆，也不能两次经过同一个变量。<bookmark mark='d'/>这里，A与D的相关是a乘c加b乘d。而B与C的相关是a乘b，尽管两者谁也不导致谁，是经由它们的共同原因A。",
    "In matrix form, Wright's rule is one line.":
        "写成矩阵，赖特的规则只有一行。<bookmark mark='a'/>每个变量等于指向它的箭头加上一个扰动。B存放箭头，psi存放箭头未能解释部分的协方差。<bookmark mark='b'/>蕴含的协方差是I减B的逆，乘psi，再乘它的转置。把这个逆展开成I加B加B的平方，依此类推，每一次幂就是某一长度的路径之和。这就是赖特的规则。<bookmark mark='c'/>普赛克对任何没有回路的模型计算它，测试再用追踪规则核对。",
    'Chapter three. The factor model, confirmed.': "第3章。因子模型，验证性的。",
    'Now the factor model.':
        "现在看因子模型。<bookmark mark='a'/>1939年，卡尔·霍尔津格和弗朗西丝·斯温福德给两所学校的三百零一名儿童做了九项测验：三项视觉、三项言语、三项速度。<bookmark mark='b'/>验证性模型声称每项测验只测量一个因子，别无其他，因子之间可以相关。缺失的箭头就是主张。<bookmark mark='c'/>蕴含的协方差矩阵是lambda、phi、lambda转置，再加theta：载荷、因子协方差，以及每项测验自己的误差方差。",
    'Before estimating, count.':
        "估计之前，先数一数。<bookmark mark='a'/>因子本身没有单位，所以把每个因子的一个载荷固定为一，或把它的方差固定为一，给它一个尺度。<bookmark mark='b'/>已知量是九个方差和三十六个协方差，共四十五个。<bookmark mark='c'/>未知量是六个自由载荷、三个因子方差、三个因子协方差和九个误差方差，共二十一个。<bookmark mark='d'/>剩下二十四个自由度，也就是二十四个可检验的约束。一个因子至少需要三个指标才能单独被识别。<bookmark mark='e'/>未知量多于已知量的模型根本无法估计；两者一样多的模型完美拟合，却什么也没检验。",
    'Chapter four. Estimation by maximum likelihood.': "第4章。最大似然估计。",
    'Estimation means choosing the unknowns':
        "估计，就是选择让模型最接近数据的那些未知量。<bookmark mark='a'/>如果数据是多元正态的，最小化这个差异就是最大化似然。当且仅当模型重现观测到的协方差时，它等于零。<bookmark mark='b'/>普赛克从粗略的初值出发，对二十一个未知量做数值最小化，大约半秒。<bookmark mark='c'/>而样本量乘以这个最小值，如果模型完全正确，就服从以模型自由度为自由度的卡方分布。",
    'Here is the model, fitted to Holzinger':
        "这是拟合到霍尔津格和斯温福德那些儿童身上的模型。<bookmark mark='a'/>标准化载荷从约零点四到零点九。<bookmark mark='b'/>因子之间相关：视觉与言语、视觉与速度都略低于零点五，言语与速度约零点三。<bookmark mark='c'/>卡方是八十五，自由度二十四。<bookmark mark='d'/>每个数字都与R的参考软件包lavaan一致到小数点后三位。测试会检查这一点。",
    'Chapter five. Does it fit?': "第5章。拟合吗？",
    'First, the chi-square test of exact fit.':
        "先看精确拟合的卡方检验。<bookmark mark='a'/>如果模型完全正确，统计量会来自这条曲线，中心在二十四附近。<bookmark mark='b'/>数据给出八十五。模型被决定性地拒绝。<bookmark mark='c'/>单一的一般因子要差得多。<bookmark mark='d'/>但没有哪个关于真实人群的模型是完全正确的，只要人数够多，检验会拒绝每一个模型。它回答的是一个没人真正问过的问题。",
    'So people use approximate fit.':
        "所以人们改用近似拟合。<bookmark mark='a'/>RMSEA衡量每个自由度、每个人的失拟。<bookmark mark='b'/>CFI问模型比一个完全没有相关的模型好多少。<bookmark mark='c'/>TLI问同样的问题，但对复杂度加以惩罚。<bookmark mark='d'/>SRMR则是平均残差相关。<bookmark mark='e'/>1999年，胡立德和彼得·本特勒根据对少数几类模型的模拟提出了临界值：CFI至少零点九五，RMSEA至多零点零六。按这些标准，这个模型不合格。而这些临界值在成千上万篇论文里成了规则。",
    'But a cut-off only means something':
        "但临界值只对某个特定模型才有意义。<bookmark mark='a'/>普赛克从拟合出的模型中抽取两百个三百零一名儿童的样本，再从遗漏了一个交叉载荷的同一模型中抽取两百个。<bookmark mark='b'/>模型正确时，几乎所有RMSEA都落得很低。<bookmark mark='c'/>模型错误时，它们散得更高，但大多数仍低于惯用临界值，几乎每个CFI也都通过。固定临界值放过了一个错误的模型。<bookmark mark='d'/>2023年，丹尼尔·麦克尼什和梅利莎·沃尔夫提出动态临界值：从你自己的模型模拟来设定它们。固定的零点零六可能过严得多，也可能过宽得多。",
    'Chapter six. Measurement and structure.': "第6章。测量与结构。",
    'A full structural equation model has two layers.':
        "完整的结构方程模型有两层。<bookmark mark='a'/>测量模型：每个潜变量及其指标，连同它们的误差。<bookmark mark='b'/>结构模型：潜变量本身之间的箭头，一种对从未被观测之物的回归。<bookmark mark='c'/>因为误差被建模了，结构箭头就不含测量误差。这是第3部分的衰减校正，在模型内部完成。",
    'Here is the correction at work.':
        "看看校正的效果。<bookmark mark='a'/>普赛克制造两种相关为零点五的特质，各由三个载荷为零点六的条目测量，共五百人。<bookmark mark='b'/>总分的信度约为零点六，相关只有约零点三。<bookmark mark='c'/>双因子模型恢复出约零点五：特质之间的关系，而不是测验之间的。<bookmark mark='d'/>校正的好坏取决于测量模型。如果条目还测量了别的东西，校正的就是错的东西。",
    'The loadings also say how reliable a scale is.':
        "载荷还说明一个量表有多可靠。<bookmark mark='a'/>总分中真分数所占的比例，等于载荷之和的平方，除以它再加上误差方差。这就是麦克唐纳的ω系数。<bookmark mark='b'/>对霍尔津格与斯温福德的三个因子，ω与第3部分的alpha一致。<bookmark mark='c'/>但只有载荷相近时它们才一致。载荷为零点九、零点八、零点三和零点二时，alpha约为零点六，ω约为零点六七。alpha低估了。<bookmark mark='d'/>alpha假设载荷相等。因子模型检验这个假设，而不是直接做出它。",
    'Chapter seven. Measurement invariance.': "第7章。测量不变性。",
    'Before comparing two groups on a test':
        "在用一份测验比较两个群体之前，先问这份测验在两组中意思是否相同。<bookmark mark='a'/>形态不变性：每组是同一个图表，同样的测验载荷在同样的因子上。<bookmark mark='b'/>度量不变性：载荷相同，因子的一个单位使每项测验移动同样多。比较相关和回归需要它。<bookmark mark='c'/>标量不变性：截距也相同，因子得分相同的人预期测验分也相同。比较均值需要它。<bookmark mark='d'/>威廉·梅雷迪思在1993年把这架梯子形式化。没有第三级，均分的差异可能是测验的差异，而不是人的差异。第32和第38部分欠下了这一章。",
    "Holzinger and Swineford's children came from two schools.":
        "霍尔津格和斯温福德的儿童来自两所学校。<bookmark mark='a'/>在两校同时拟合三因子模型。<bookmark mark='b'/>令载荷相等，代价很小：卡方的变化可以接受。<bookmark mark='c'/>令截距相等，代价约为四十：被拒绝。对能力相同的儿童，有些测验在一所学校更容易。<bookmark mark='d'/>如果照样假定标量不变性，格兰特-怀特学校在言语因子上看起来高出半分以上。按现状，数据并不支持这种比较。这些数字与lavaan完全一致。",
    'Chapter eight. Mediation.': "第8章。中介。",
    'A treatment works. Through what?':
        "一种治疗有效。通过什么？<bookmark mark='a'/>X是治疗，M是提出的机制，Y是结局。<bookmark mark='b'/>M对X回归得到路径a。Y对M和X回归得到路径b和直接效应。<bookmark mark='c'/>间接效应是a乘b，配以自助法区间。鲁本·巴伦和戴维·肯尼在1986年写下了这个配方，它已被引用数万次。<bookmark mark='d'/>陷阱在这里。X可以随机化，但M不能。Y对M的回归是观察性的，带着由此而来的一切混杂。",
    'Watch the trap close.':
        "看陷阱如何合上。<bookmark mark='a'/>普赛克做一个实验。X被随机化，X升高M。但M对Y毫无作用。一个未被测量的特质U同时升高M和Y。<bookmark mark='b'/>配方发现间接效应约为零点一七，区间远离零。一个机制，显著，却是假的。<bookmark mark='c'/>随机化X保护的是总效应，而不是它在各路径之间的分割。",
    'So what would show a mechanism?':
        "那么什么才能显示机制？<bookmark mark='a'/>操纵M：第二个实验，直接改变机制，然后观察Y。<bookmark mark='b'/>或者平行设计：在机制被阻断和未被阻断时分别施加治疗。<bookmark mark='c'/>至少，做一次敏感性分析：M与Y之间的混杂要有多强，才能抹去间接效应？<bookmark mark='d'/>或者少说一点：仅凭一个随机化的X，只说与中介一致，绝不说由它解释。<bookmark mark='e'/>约翰·布洛克、唐纳德·格林和夏尚在2010年提出了这一点，标题是：是的，但机制是什么？别指望有简单的答案。本章的账本条目，是一个在被操纵时失败的中介变量。",
    'Chapter nine. Equivalent models.': "第9章。等价模型。",
    'Psyche makes three variables, with X causing M':
        "普赛克制造三个变量，X导致M，M导致Y。现在拟合四个图表。<bookmark mark='a'/>真实的链。<bookmark mark='b'/>反过来的链：Y导致M，M导致X。<bookmark mark='c'/>分叉：M导致两者。<bookmark mark='d'/>前三个拟合得完全相同，每一位小数都一样。它们蕴含同一件事：给定M时，X与Y独立。数据永远无法在它们之间选择。<bookmark mark='e'/>只有对撞结构不同。它说X与Y独立，而数据拒绝了它。",
    'This is general.':
        "这是普遍的。<bookmark mark='a'/>1993年，罗伯特·麦卡勒姆及其同事表明，大多数已发表的模型都有等价模型，常常还很多，其中箭头被反转或被相关代替。<bookmark mark='b'/>在对五十三项已发表应用的调查中，几乎没有一项承认它们。<bookmark mark='c'/>好的拟合只说明模型属于数据无法区分的一族。箭头来自设计、时间顺序和理论，而不是来自拟合。<bookmark mark='d'/>又是第2部分的教训。方向是实验来检验的，而不是相关矩阵宣布的。",
    'Chapter ten. Latent variables over time.': "第10章。随时间的潜变量。",
    'Measure the same people four times.':
        "对同一批人测量四次。<bookmark mark='a'/>增长曲线模型给每个人两个潜变量：起点在哪里，变化有多快。<bookmark mark='b'/>载荷是固定的，不是估计的：起点为一、一、一、一，斜率为零、一、二、三。<bookmark mark='c'/>斜率的方差说明人们的变化方式是否不同。它与起点的相关说明高分者是回落还是领先。<bookmark mark='d'/>这与第31部分儿童增长曲线背后的混合模型是同一个模型，只是画成了图表。",
    'Now two traits, measured at three waves.':
        "现在看两种特质，测量三次。比如孤独与情绪低落。<bookmark mark='a'/>交叉滞后面板模型让每种特质预测下一次的自己。<bookmark mark='b'/>也让每种预测对方，控制过去的分数。<bookmark mark='c'/>如果某一次的孤独预测下一次的情绪低落，它就被解读为驱动因素。成千上万篇论文都这样解读。",
    'Here is the catch.':
        "问题就在这里。<bookmark mark='a'/>普赛克制造两千人，测量四次。他们在两种特质上有稳定的差异，稳定部分彼此相关。但在任何一个人内部，两种特质互不影响。<bookmark mark='b'/>交叉滞后面板照样发现了效应，离零约十一个标准误，因为过去的分数只是稳定特质的一个有噪声的替身。<bookmark mark='c'/>在每个人内部，效应为零。<bookmark mark='d'/>埃伦·哈马克、丽贝卡·凯珀和拉乌尔·格拉斯曼在2015年指出了这一点。随机截距模型把稳定的人与每次之间的变化分开，而说一种特质驱动另一种，是关于变化的主张。",
    'Chapter eleven. Factors or networks?': "第11章。因子还是网络？",
    'Two pictures of a disorder.':
        "障碍的两幅图景。<bookmark mark='a'/>在第一幅里，一个隐藏的原因，即障碍本身，产生每一个症状，就像诊断类别所假设的那样。<bookmark mark='b'/>在第二幅里，也就是第39部分的症状网络，没有隐藏的原因。症状彼此导致。<bookmark mark='c'/>丹尼·博斯博姆和安热莉克·克拉默在2013年为第二幅辩护：睡眠差导致疲劳，疲劳导致注意力差，注意力差导致担忧。不需要一个隐藏的抑郁。",
    'Can data decide between the pictures?':
        "数据能在两幅图景之间做出判断吗？<bookmark mark='a'/>普赛克写下一个单一因子，载荷为零点八、零点七、零点六和零点五。相关随之而来。<bookmark mark='b'/>现在计算偏相关。它们构成一个网络：每一对都相连，载荷最大处的边最强。<bookmark mark='c'/>这个网络精确重现了相关。任何协方差矩阵都有一个完美拟合它的网络。<bookmark mark='d'/>约斯特·克鲁伊斯和冈特·马里斯在2016年证明了更强的结果。对是或否的症状，网络、潜变量模型和共同原因模型是同一个分布。第39部分陈述过它；这里是最简单的情形，计算出来。拟合无法做出判断。",
    'So what could decide?':
        "那么什么能做出判断？<bookmark mark='a'/>干预。只治疗睡眠。在网络里，疲劳和注意力也应该改善；在共同原因下，它们不应改善。<bookmark mark='b'/>时间。有了每个人数周的个体内数据，如第47部分，今天的睡眠能预测同一个人明天的疲劳吗？<bookmark mark='c'/>还有稳定性。从几百人估计出的网络可能因样本而变，所以在解读它的边之前，先做自助法。<bookmark mark='d'/>答案也可能是两者都有：共同原因和直接联系并存。问题在于各占多少。",
    'Chapter twelve. Reading an SEM paper.': "第12章。读一篇SEM论文。",
    'Here is an abstract, invented for practice':
        "这是一份为练习而虚构的摘要，形式你会经常见到。四百一十二名员工，一次性调查。工作负荷导致倦怠，倦怠导致离职意向。模型拟合良好，倦怠完全中介了这一效应。<bookmark mark='a'/>一次性调查：导致是一个方向，一个时间点的数据无法显示。<bookmark mark='b'/>拟合良好：按固定临界值，而它们会放过错误的模型，而且反向的链拟合得完全一样。<bookmark mark='c'/>完全中介：中介变量没有被操纵，这里什么都没被操纵。<bookmark mark='d'/>它确实显示的：这三个测量之间的关系，与一条链所蕴含的一致。其他图表也一样。",
    'Eight questions for any paper with a path diagram.':
        "对任何带路径图的论文，问八个问题。<bookmark mark='a'/>图表画出来了吗，每个固定和自由参数都标出了吗，自由度给了吗？哪些等价模型拟合得同样好，为什么把它们排除？对那些需要时间或实验的箭头，数据是随时间收集的，或来自实验吗？报告了卡方吗，拟合是针对这个模型评判的，而不是按固定临界值吗？模型是否在看过拟合后修改过，论文说了吗？比较群体之前检验了不变性吗？测量可靠吗，测量被建模了吗？数据和代码公开吗，以便另一位分析者拟合不同的图表？",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Three new rows. The first is a mediator':
        "三个新条目。第一个是一个中介变量：自我控制依赖血糖，所以损耗会降低它，一杯含糖饮料能恢复自我控制。<bookmark mark='a'/>原始研究：盖利奥特及其同事，2007年。<bookmark mark='b'/>记录：一项预注册的含糖饮料检验，以及一项血糖文献的元分析。<bookmark mark='c'/>一个根据相关选出的中介变量，在被操纵时失败了，母效应自我损耗也失败了。<bookmark mark='d'/>重复失败。",
    'The second is a theorem.':
        "第二个是一条定理。潜因子模型和直接相互作用的网络，可以蕴含完全相同的反应分布。<bookmark mark='a'/>原始研究：克鲁伊斯与马里斯，2016年。<bookmark mark='b'/>记录：马斯曼及其同事把网络模型与项目反应模型形式化地联系起来。<bookmark mark='c'/>这是定理，不是实验。拟合无法在隐藏原因和相互因果系统之间做出判断；干预和时间可以。<bookmark mark='d'/>已重复，作为数学。",
    'The third: fixed cut-offs for fit indices':
        "第三个：拟合指数的固定临界值能普遍地区分好模型和坏模型。<bookmark mark='a'/>原始研究：胡立德与本特勒，1999年。<bookmark mark='b'/>记录：一篇附带模拟的批评，以及为每个模型计算的动态临界值。<bookmark mark='c'/>在它们得出的条件下有用；作为普遍规则，会误导。<bookmark mark='d'/>重复失败。",
    'What the three have in common.':
        "三者的共同点。<bookmark mark='a'/>每一条都是关于模型的主张，而不是关于某一项研究的数据。<bookmark mark='b'/>中介变量被人为改变时失败了。临界值在其来源的模拟之外失败了。定理成立，因为它是定理。<bookmark mark='c'/>模型也是一种主张。它进入账本，也可能失败。",
    'Chapter fourteen. In practice: surveys, tests and people analytics.': "第14章。实践中：调查、测验与人力分析。",
    'Where these models earn their keep.':
        "这些模型在哪里发挥作用。<bookmark mark='a'/>测验效度验证：在新样本中验证新问卷的因子结构，并由载荷得出信度。<bookmark mark='b'/>跨国调查：在按国家、语言或群体给敬业度或幸福感分数排名之前，先检验不变性。<bookmark mark='c'/>人力分析：把敬业度、倦怠和离职意向作为潜变量，对测量误差建模，而不是忽略它。<bookmark mark='d'/>还有市场营销：顾客满意度、信任和忠诚度的模型，以及广告中的态度模型。",
    'In every one of these settings, one question':
        "在所有这些场合，有一个问题最有用。<bookmark mark='a'/>还有什么图表能同样好地拟合这些数据，又有什么能区分它们？<bookmark mark='b'/>一个说敬业度驱动留任的仪表板，只画出了几个拟合箭头中的一个。<bookmark mark='c'/>跨团队或跨国家比较的分数，首先需要标量不变性。<bookmark mark='d'/>最便宜的答案往往是实验：为一些团队改变一件事，然后观察。",
    'Chapter fifteen. Frontier: causal discovery, Bayes and dynamic fit.': "第15章。前沿：因果发现、贝叶斯与动态拟合。",
    'Can the arrows be found, rather than assumed?':
        "箭头能被找出来，而不是被假设吗？<bookmark mark='a'/>拿第九章的四个图表来说。对链、反向链和分叉，数据揭示了边，却揭示不了方向。<bookmark mark='b'/>只有对撞结构的方向能确定，因为在知道M之前，X和Y是独立的。<bookmark mark='c'/>彼得·斯皮尔特斯、克拉克·格莱穆尔和理查德·沙因斯的PC算法之类，检验条件独立，返回拟合的那一族图表，只确定数据迫使的方向。<bookmark mark='d'/>它们假设每个共同原因都被测量了，没有哪种独立是巧合。在一切背后都有潜在特质的心理学数据里，这很少成立。<bookmark mark='e'/>一个开放问题：当变量本身就是有噪声的测量时，因果发现能增加多少？",
    'Two more frontiers.':
        "还有两个前沿。<bookmark mark='a'/>贝叶斯结构方程模型给小的交叉载荷加上先验，让它们接近零而不是恰好为零，这是本特·穆滕和季霍米尔·阿斯帕鲁霍夫在2012年提出的。它对小样本有帮助，而先验必须报告并加以变动。<bookmark mark='b'/>动态拟合从这个模型模拟，加入设定大小的错误设定，再由模拟设定临界值，这是丹尼尔·麦克尼什和梅利莎·沃尔夫提出的。它把第五章的教训变成常规。<bookmark mark='c'/>还有开放问题：哪些错误设定对所问的问题重要，多大算太大？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>三因子模型没有通过精确拟合检验，卡方为八十五，自由度二十四。特质相关零点五时，总分相关约零点三。没有中介时也能发现中介：零点一七，区间不含零。这里有另外两个图表与真实图表拟合得一模一样；在已发表的模型中，常常还多得多。<bookmark mark='b'/>模型可以被拒绝却有用，被校正却仍然错，显著却是假的，而且从来不是唯一的。",
    'Part forty-four in twelve lines.':
        "第四十四部分，十二行。<bookmark mark='a'/>相关是连接两个变量的各条路径之和。因子模型是一个图表，写成矩阵方程。识别固定尺度，并用矩数来清点参数。最大似然把图表拟合到协方差上。卡方检验迟早拒绝每个模型，固定临界值则放过错误的模型。对测量建模可以消除衰减。只有在标量不变时才比较均值。随机化的治疗并不随机化中介变量。等价模型拟合完全相同，所以箭头来自设计。交叉滞后面板把稳定的人和变化混为一谈。因子和网络可以蕴含同样的数据。还有读路径图的八个问题。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反对意见，说数学不能用于心灵，遇到了赖特的规则、最大似然、拟合与不变性，全都计算出来，并与参考实现核对。<bookmark mark='b'/>第二个，说心灵不能做实验：模型的箭头是实验必须检验的主张，拟合做不到。琥珀色。<bookmark mark='c'/>第三个，关于内省：指标大多是问卷。模型处理它们的随机误差，而不是偏差。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再出现。<bookmark mark='a'/>每个条目背后的潜在特质，就在下一部分，第45部分。随时间的个体内模型在第47部分。行为模型的拟合与比较在第48部分。跨研究的证据分量在第50部分。",
    'Seven problems, with full solutions':
        "七道习题，完整解答在本部分的README里。<bookmark mark='a'/>一道追踪路径。一道清点参数和自由度。一道计算RMSEA。一道做衰减校正。一道检验不变性。一道寻找等价模型。最后一道带星号，要你把一份摘要用两种方式重画，并设计能区分它们的研究。如果想试试，就在这里暂停。",
    'The books and papers behind this part':
        "这一部分背后的书和论文列在这里和README中。雷克斯·克莱因的教材是标准课程；肯尼思·博伦的书讲数学；朱莉娅·罗勒关于相关与因果的短文，是了解一个图表能主张什么、不能主张什么的最佳入门。",
    'The graduate toolkit has begun.':
        "研究生工具箱已经开始。<bookmark mark='a'/>这一部分为没有人观察到的东西建模，并说明了拟合能说什么、不能说什么。<bookmark mark='b'/>接下来，是一个人与一道题的单次相遇。做了不同题目的两个人，如何放到同一个量尺上？第45部分：项目反应理论。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
