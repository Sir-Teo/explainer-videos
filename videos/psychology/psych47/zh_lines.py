"""Chinese narration for psych47: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第47部分：随时间变化的人'

CHAPTERS = {
    'Hook': '二十个词，一个结论',
    'Predict': '1. 在你身上：一团点云，四个数字',
    'Repeated': '2. 重复测量',
    'Shrink': '3. 随机截距与随机斜率',
    'Crossed': '4. 参与者与题目，交叉',
    'Stimuli': '5. 刺激也是样本',
    'Growth': '6. 增长',
    'Simpson': '7. 一个人内部的辛普森悖论',
    'Centre': '8. 个体内与个体间',
    'Ergodic': '9. 遍历性',
    'Esm': '10. 密集纵向数据',
    'Cause': '11. 随时间的因果',
    'Tipping': '12. 临界点',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：用户、患者与仪表盘',
    'Frontier': '15. 前沿：关于一个人的科学',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'In 1973 the psychologist Herbert Clark looked at a generation of studies of language.':
        "1973年，心理学家赫伯特·克拉克审视了一代语言研究。<bookmark mark='a'/>它们检验一个效应能否推广到新的人。却从未检验它能否推广到新的词。<bookmark mark='b'/>Psyche运行了两百项完全无效的启动研究：三十个人，二十个词，而词与词之间各不相同。<bookmark mark='c'/>只按参与者分析，大约一半结果显著。承诺的是百分之五。<bookmark mark='d'/>把词也当作样本，比率就回到百分之五或更低。这个修正花了三十年才成为常规。",
    "Clark's point is about generalizing across stimuli.":
        "克拉克的观点关乎跨刺激的推广。<bookmark mark='a'/>还有一个更深的版本，是整个系列中最难的。<bookmark mark='b'/>一个在人与人之间成立的关系，不一定在其中任何一个人身上成立。<bookmark mark='c'/>大多数心理学理论关乎后者：当某样东西变化时，一个心灵内部发生了什么。<bookmark mark='d'/>而大多数研究测量的是前者：许多人，每人测一次。<bookmark mark='e'/>这一部分讲的就是如何把它们区分开。",
    'So this part asks when a finding about people is a finding about a person.':
        "所以这一部分要问：什么时候，关于人们的发现，才是关于一个人的发现。<bookmark mark='a'/>重复测量与多层模型。<bookmark mark='b'/>参与者和刺激，都作为样本。<bookmark mark='c'/>个体内与个体间，以及遍历性。<bookmark mark='d'/>还有时间中的生活：日记、惰性和临界点。",
    'This is Part 47 of Psychology, Built: people over time.':
        "这是《心理学，从零搭建》第47部分：随时间变化的人。<bookmark mark='a'/>我们将模拟“把语言当作固定效应”的谬误。我们将构建多层模型，看它们如何收缩，并让参与者与题目交叉。我们将问一个主张需要多少刺激。我们将把个体内的关系与个体间的关系分开。我们将构建一个其平均值描述不了任何人的总体。我们还将跟随时间中的生活：日记、情绪惰性，以及临界点之前的预警信号。",
    'Chapter one. On you: one cloud, and four numbers.': "第1章。在你身上：一团点云，四个数字。",
    'First, a cloud of points.':
        "首先，一团点云。<bookmark mark='a'/>每个点是一个人的一次测量：十二个人，每人十五次。<bookmark mark='b'/>在所有人之中，x上升时y下降。<bookmark mark='c'/>现在猜一猜。对一个人来说，在他的x比平时高的那天，他的y是更高还是更低？<bookmark mark='d'/>在课程网站上，你可以看到同一团点云，按人着色。",
    'Now four numbers.':
        "现在写下四个数字。<bookmark mark='a'/>第一：三十个人，二十个词，没有效应，只按参与者分析。假阳性率是多少？<bookmark mark='b'/>第二：在你刚看到的点云里，当一个人的x上升时，他的y是上升还是下降？<bookmark mark='c'/>第三：两种特质在人与人之间相关零点六。有多大比例的人，在自己身上随时间表现出大约这样的相关？<bookmark mark='d'/>第四：一个人真实的日间惰性是零点四。用二十天的数据估计，平均会得到多少？在这里暂停，把它们写下来。",
    'Chapter two. Repeated measures.': "第2章。重复测量。",
    'Most experiments measure each person many times.':
        "大多数实验会对每个人测量很多次。<bookmark mark='a'/>传统的分析把试次平均成每人每条件一个数字，再比较这些平均值。<bookmark mark='b'/>丢掉的是：人们在效应上的差异有多大，试次之间差异有多大，用了哪些刺激，以及效应在实验过程中如何变化。<bookmark mark='c'/>而当试次数量不等时，每个人的分量都一样，不管测得多准。<bookmark mark='d'/>一个针对每个试次的模型保留了全部这些：多层模型，或称混合模型。",
    "Here's the model.":
        "这就是模型。<bookmark mark='a'/>在试次层面，每个人有自己的一条线：一个截距和一个斜率。<bookmark mark='b'/>在人的层面，这些线从一个由线组成的总体中抽取。β是平均效应。G表示人们在效应上差异多大。σ平方是试次之间的噪声。<bookmark mark='c'/>南·莱尔德和詹姆斯·韦尔在1982年写出了它的一般形式。《统计学，从零搭建》在它的第25部分拟合这个模型，这一部分用的就是那里的代码。",
    'How much is one more observation worth?':
        "多一次观测值多少？<bookmark mark='a'/>一个人的观测共享这个人。这里组内相关，也就是方差中属于个人的那部分，是零点三。<bookmark mark='b'/>对于总均值，这些观测只相当于更少的独立观测，按这个公式计算。点是模拟的研究。<bookmark mark='c'/>一百个人每人十次，就是一千次观测，相当于大约两百七十次独立观测。每人五十次，大约三百二十次，接近三百三十的上限。<bookmark mark='d'/>对于关于人们的问题，更多的人胜过更多的观测。对于一个人内部变化的问题，则正好相反。",
    'Chapter three. Random intercepts and slopes.': "第3章。随机截距与随机斜率。",
    "What's one person's slope?":
        "一个人的斜率是多少？<bookmark mark='a'/>Psyche造出四十个人，每人十五次有噪声的观测，他们的斜率确实不同。<bookmark mark='b'/>每个人自己的回归是无偏的，但有噪声。多层模型把每个斜率拉向平均值，越嘈杂的人拉得越多。这叫作部分合并。<bookmark mark='c'/>误差下降大约三分之一。从其他所有人那里借力，能更好地描述每个人。<bookmark mark='d'/>这是詹姆斯和斯坦的收缩，用在人身上。但它假设每个人都和其他人相似。",
    'How hard does the model pull?':
        "模型拉得有多用力？<bookmark mark='a'/>多层估计是这个人自己的斜率和总体斜率的加权平均。<bookmark mark='b'/>权重是自身斜率的变异中真实而非噪声的那部分所占的比例。<bookmark mark='c'/>每人十五次观测时，模型给每个人自己的斜率略多于一半的权重。六十次时，大部分权重。<bookmark mark='d'/>所以数据越少的人被拉得越远。这对数据是公平的，但一个观测很少的不寻常的人，会显得比实际更普通。",
    'Chapter four. Participants and items, crossed.': "第4章。参与者与题目，交叉。",
    'Why does the by-participant test fail?':
        "按参与者的检验为什么会失败？<bookmark mark='a'/>词各不相同：有的容易，有的难，而每个条件只有十个词。<bookmark mark='b'/>每个参与者看到的都是同样的二十个词，所以词的怪癖出现在每个人的平均值里。<bookmark mark='c'/>按参与者的检验看到三十个意见一致的人，把词的怪癖误当成了效应。<bookmark mark='d'/>一个同时为参与者和题目设置随机效应的模型知道每边只有十个词。真正起作用的检验大约有十八个自由度，而不是二十九个。",
    'How much structure should the model have?':
        "模型应该有多少结构？<bookmark mark='a'/>克拉克自己的补救办法，是把按参与者和按题目的检验合成一个，略为保守。<bookmark mark='b'/>交叉混合模型同时为参与者和题目拟合随机效应，正如哈拉尔德·巴扬、道格拉斯·戴维森和道格拉斯·贝茨在2008年所展示的。<bookmark mark='c'/>戴尔·巴尔及其同事在2013年主张：保持最大化。纳入设计所允许的每一个随机斜率，否则错误率会再次上升。<bookmark mark='d'/>汉内斯·马图舍克及其同事在2017年回应说，最大化模型会损失功效，而且常常不收敛。要依据证据简化，而不是依据习惯。<bookmark mark='e'/>一个不收敛的模型是在告诉你：数据估计不了你要求的东西。",
    'The danger runs both ways.':
        "危险是双向的。<bookmark mark='a'/>现在词之间几乎没有差别，但参与者在效应本身上不同：有的人为正，有的人为负，平均为零。<bookmark mark='b'/>这时按题目的检验失败了，假阳性大约百分之十二，按参与者的检验也不安全。<bookmark mark='c'/>把两者都当作随机，才能守住防线。<bookmark mark='d'/>这就是保留随机斜率的理由：设计所允许的每一种变异来源，都必须进入检验。",
    'Chapter five. Stimuli are a sample too.': "第5章。刺激也是样本。",
    'Stimuli limit power too.':
        "刺激也限制功效。<bookmark mark='a'/>Psyche用三十个参与者运行一个真实的启动效应，研究中的词从八个到四十八个不等。<bookmark mark='b'/>二十个词时，效应被发现的次数不到三分之一。四十八个时，大约三分之二。<bookmark mark='c'/>增加参与者解决不了这个问题。关于词的不确定性一直存在，不管有多少人看到它们。<bookmark mark='d'/>查尔斯·贾德、雅各布·韦斯特福尔和戴维·肯尼在2012年指出：要像规划参与者数量一样仔细地规划刺激的数量。",
    'Tal Yarkoni pushed the point further in 2022.':
        "2022年，塔尔·亚尔科尼把这一点推得更远。<bookmark mark='a'/>一项用一个任务研究自我损耗、或用十二张照片研究面孔的研究，支持的是关于那个任务、那些照片的主张。<bookmark mark='b'/>口头上的主张远比检验它的统计模型宽泛。<bookmark mark='c'/>所以，要么扩大模型，对任务、刺激、实验者和情境进行抽样，并把它们当作随机的。<bookmark mark='d'/>要么把主张缩小到被抽样的范围。<bookmark mark='e'/>第43部分的重复研究改变了实验室。很少有研究改变它们的刺激。",
    'So which should a study add, people or items?':
        "那么一项研究该增加的是人，还是题目？<bookmark mark='a'/>这是同一个真实效应的功效，人和题目都在变化。<bookmark mark='b'/>沿着一列往下，更多的参与者几乎没有帮助。词的变异仍然在那里。<bookmark mark='c'/>沿着一行往右，更多的词帮助很大。<bookmark mark='d'/>在这样的设计中，一项十五个人、四十个词的研究，胜过一项一百二十个人、十个词的研究。",
    'Chapter six. Growth.': "第6章。增长。",
    'Growth is the same model, with time as the predictor.':
        "增长是同一个模型，以时间作为预测变量。<bookmark mark='a'/>第31部分的增长曲线和第44部分的潜在斜率就是这个模型：每个人自己的起点和速率。<bookmark mark='b'/>现在加入一个也会变化的预测变量：每次测量时的睡眠、压力或练习。<bookmark mark='c'/>它的单一系数混合了两个问题。睡得多的人表现更好吗？一个人在睡得多的那些夜晚之后表现更好吗？<bookmark mark='d'/>把预测变量分成这个人的平均值和这次测量偏离平均值的部分，各给一个系数。接下来的两章说明为什么。",
    "Here's what goes wrong if you don't split.":
        "这是不拆分时会出的问题。<bookmark mark='a'/>Psyche造出两百个孩子，测量五周。平均而言练习更多的孩子正是那些学得吃力的孩子，但任何一个孩子在练习更多的那一周都表现更好。<bookmark mark='b'/>只放进一次时，练习得到单一的系数，是两个相反效应的混合。<bookmark mark='c'/>拆分之后，这一周的偏离得到大约正零点四，比植入的一半略少，因为五周只能粗略地确定每个孩子的平均值；而孩子的平均值得到大约负零点四，与植入的一致。<bookmark mark='d'/>给一个孩子的建议，“这周多练习”，需要的是第一个数字。混合的系数会把它低估一半以上。",
    'Chapter seven. Simpson inside a person.': "第7章。一个人内部的辛普森悖论。",
    "Here's the cloud from chapter one again.":
        "再看第一章的那团点云。<bookmark mark='a'/>按人给点着色，每个人自己的点云都向上倾斜。<bookmark mark='b'/>在人与人之间斜率为负；在每个人内部斜率为正。<bookmark mark='c'/>举个例子：打字更快的人错误更少，因为他们更熟练。但任何一个打字员，打得比平时快时，错误都会更多。<bookmark mark='d'/>这是辛普森悖论，发生在一个心灵的尺度上。关于一个人的答案就在数据里，却不在相关系数里。",
    'Make it concrete.':
        "把它具体化。<bookmark mark='a'/>为每个人拟合自己的直线：十二个斜率。<bookmark mark='b'/>每一个都是正的。<bookmark mark='c'/>合并的斜率是负的，落在它们所有人之外。它不是研究中任何一个人的斜率。<bookmark mark='d'/>这就是检验一个关于个人的主张的方法：它是否一个人一个人地成立？",
    'Chapter eight. Within against between.': "第8章。个体内与个体间。",
    'The repair is simple.':
        "修正很简单。<bookmark mark='a'/>把每个预测变量分成这个人自己的平均值和今天偏离它的部分，各给一个斜率。<bookmark mark='b'/>个体内斜率回答关于一个人的问题：这里大约是正零点六，与植入的一致。<bookmark mark='c'/>个体间斜率回答关于人们的问题：大约负一。<bookmark mark='d'/>而合并的斜率哪个问题都不回答。它是一种混合，按x在个体内和个体间各变化多少来加权。",
    "There's an old name for the mistake.":
        "这个错误有一个古老的名字。<bookmark mark='a'/>1950年，威廉·鲁宾逊表明，移民较多的美国各州识字率较高，尽管移民识字的比例更低。跨州的相关对个人什么也没说。<bookmark mark='b'/>往下一个层次也是如此。跨人的相关，对一个人如何运作说明得很少。<bookmark mark='c'/>发现焦虑的人睡得少，并不能说明一个人在焦虑的夜晚睡得少。<bookmark mark='d'/>问题决定数据。关于一个人的主张，需要对个人的重复测量。",
    'One more way to get a person wrong: ignore them.':
        "还有一种把人弄错的方式：忽略他们。<bookmark mark='a'/>三十个人，每人二十次测量。每人有自己的斜率，平均斜率为零。<bookmark mark='b'/>把全部六百个点放进一个回归，它的检验有百分之十五的时候显著。<bookmark mark='c'/>为每个人拟合斜率，再检验这三十个斜率，就是百分之五，与承诺的一致。<bookmark mark='d'/>重复的单位是人。检验必须数人，而不是数点。带随机斜率的多层模型做到了这一点，还做得更多。",
    'Chapter nine. Ergodicity.': "第9章。遍历性。",
    'Peter Molenaar gave the problem a mathematical name.':
        "彼得·莫勒纳尔给这个问题起了一个数学的名字。<bookmark mark='a'/>当一个过程在总体中的统计量等于它在一个成员身上随时间的统计量时，这个过程就是遍历的。<bookmark mark='b'/>这需要两个条件：每个人遵循同一个模型，而且这个模型不随时间改变。<bookmark mark='c'/>2004年，莫勒纳尔指出，心理过程几乎从不同时满足这两个条件。人与人不同，而且人在发展。<bookmark mark='d'/>所以群体分析，无论规模多大，本身都描述不了任何一个个体。",
    'Psyche builds a population to see what that means.':
        "Psyche构建了一个总体，来看看这意味着什么。<bookmark mark='a'/>两百个人，每人一百次测量。人们在两种特质上存在稳定的差异，而每个人的两种特质以自己的方式一起变化。<bookmark mark='b'/>在任何时刻，在人与人之间，两种特质的相关大约是零点六。<bookmark mark='c'/>在个人内部，相关从强烈的负相关散布到强烈的正相关。接近群体相关的人不到十分之一，几乎一半是负的。<bookmark mark='d'/>2018年，阿伦·费希尔、约翰·梅达利亚和贝尔图斯·耶罗尼穆斯发现真实样本就是这样，个体之间的变异比群体所暗示的大好几倍。",
    'So what should you use to predict one person?':
        "那么，应该用什么来预测一个人？<bookmark mark='a'/>假设你想预测一个人的两种特质以后会如何一起变化。用群体的相关，还是用这个人自己最初的几次测量？<bookmark mark='b'/>在这个总体中，群体的数字平均偏差大约零点六五，无论群体有多少数据。<bookmark mark='c'/>这个人自己的五次测量偏差大约零点四；四十次，大约零点一三。<bookmark mark='d'/>当人与人差异这么大时，关于这个人的一点点数据，胜过关于其他所有人的大量数据。",
    'Chapter ten. Intensive longitudinal data.': "第10章。密集纵向数据。",
    'To study a person, measure a person often.':
        "要研究一个人，就要经常测量一个人。<bookmark mark='a'/>在经验取样中，手机一天询问好几次，持续数周：你感觉如何，你在哪里，你在做什么？<bookmark mark='b'/>每个人都变成一条时间序列，有自己的均值、自己的离散，以及每个时刻有多少延续到下一个时刻。<bookmark mark='c'/>这种延续就是自回归，或称惰性：一种挥之不去的情绪。<bookmark mark='d'/>从几条序列中，可以得到一个人的各种状态如何相互预测的网络：针对个人的，而不是总体平均。",
    'Inertia became a measure of risk.':
        "惰性成了一个风险指标。<bookmark mark='a'/>2010年，彼得·库彭斯、尼古拉斯·艾伦和丽莎·希伯报告说，挥之不去的情绪与抑郁症状相伴。<bookmark mark='b'/>但围绕一个人自己的均值估计的惰性，是偏向零的。真实值为零点四时，二十次测量平均只得到大约零点三，十次得到的不到真实值的一半。<bookmark mark='c'/>偏差大约是一加三φ，除以测量次数。回答提示次数较少的人显得惰性更低：如果两组的依从性不同，这就是一个混杂。<bookmark mark='d'/>而事实证明，惰性在一个人的均值和离散之外几乎没有增加什么。这记在账本里。",
    'How many prompts does a diary need?':
        "一份日记需要多少次提示？<bookmark mark='a'/>假设一次提示中的情绪，百分之四十属于这个人，百分之六十属于这个时刻。<bookmark mark='b'/>把k次提示平均起来，第3部分的斯皮尔曼-布朗公式给出这个人平均值的信度。<bookmark mark='c'/>一周的每日提示大约给出零点八。四周，大约零点九五。<bookmark mark='d'/>但那些时刻并不是噪声。它们的离散、它们的惰性、它们对事件的反应，正是经验取样的目的所在。",
    'Chapter eleven. Cause over time.': "第11章。随时间的因果。",
    'Back to cause, with what this part has added.':
        "带着这一部分新增的东西，回到因果。<bookmark mark='a'/>第44部分展示了这个陷阱。一个交叉滞后面板模型，在特质从未相互作用的人身上，发现一种特质驱动另一种，因为人与人之间稳定的差异渗进了滞后效应。<bookmark mark='b'/>修正的办法是给每个人每种特质一个自己的水平，让滞后效应描述偏离这个水平的部分。<bookmark mark='c'/>它至少需要三个波次，越多越好。波次很少时，一个人的水平知道得很粗略，滞后效应就有偏差，正像第十章的惰性那样。<bookmark mark='d'/>它仍然排除不了一个随时间变化的第三变量，也选择不了滞后的长度。一天、一个月和一年可能给出不同的答案。<bookmark mark='e'/>最强的设计，是在随机的时间为一个人改变一件事，然后观察：单个案实验，或微随机化试验。",
    'How many waves does the repair need?':
        "这个修正需要多少波次？<bookmark mark='a'/>Psyche造出五百个人，他们有稳定的特质，以及从一种特质到另一种的、零点二的真实个体内滞后效应。<bookmark mark='b'/>用每个人偏离自己观测均值的部分来估计它。<bookmark mark='c'/>三个波次时，它大约得出零点一二。十个时，几乎正确。五十个时，正确。<bookmark mark='d'/>波次太少会使个体内滞后效应偏向零，因为每个人的均值太不确定。密集的设计能解决这个问题。",
    'Chapter twelve. Tipping points.': "第12章。临界点。",
    'Some changes are not gradual.':
        "有些变化不是渐进的。<bookmark mark='a'/>Psyche构建了一种停留在低谷中的情绪。山谷慢慢变平，直到状态翻转到另一个山谷。<bookmark mark='b'/>在翻转之前，系统从每次小扰动中恢复得越来越慢，所以每个时刻都与之前的时刻相似。<bookmark mark='c'/>自相关和方差上升。这叫作临界慢化。<bookmark mark='d'/>马滕·舍弗及其同事在湖泊、气候和渔业的转变之前发现了这一特征。2014年，英格丽德·范德莱姆普特及其同事在情绪中寻找它。",
    'Can it warn in time?':
        "它能及时预警吗？<bookmark mark='a'/>有一份长而连续的记录时，上升的自相关能在一半以上的翻转之前发出预警，而在没有翻转时几乎从不报警。<bookmark mark='b'/>换成同样这些生活的一份嘈杂的每日日记，预警只出现在四分之一的翻转之前，而在从未翻转的人中，大约六分之一会报警。<bookmark mark='c'/>一个在复发过程中被追踪的人显示出了这个信号。在许多人身上的前瞻性检验发现它很弱。<bookmark mark='d'/>理论是成立的。情绪是否就是这样的系统，日记能否及时看到这个信号，仍是开放的问题。账本的结论是有争议。",
    'One choice the analyst makes changes the answer.':
        "分析者的一个选择就会改变答案。<bookmark mark='a'/>换一组新的六十个会翻转的生活，和六十个从不翻转的。只改变滚动窗口的宽度。<bookmark mark='b'/>窄的窗口几乎在任何翻转之前都不报警。宽的窗口在十次中有七次之前报警。<bookmark mark='c'/>但误报也随之上升，从大约百分之二升到大约百分之十二。<bookmark mark='d'/>窗口、去趋势和阈值，都是花园里的岔路。在数据之前把它们定下来，否则预警就是事后才找到的。",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Three new rows.':
        "三条新记录。第一条：把一项研究的刺激当作固定的、而不是当作样本，会远比承诺的更频繁地发现无法推广的效应。<bookmark mark='a'/>原始研究：克拉克，1973年。<bookmark mark='b'/>记录：贾德、韦斯特福尔和肯尼的模拟，以及巴尔及其同事的模拟。<bookmark mark='c'/>它既是实验的结果，也是算术的结果，正如开头所计算的。<bookmark mark='d'/>已重复。",
    'The second: emotions that linger predict depression':
        "第二条：挥之不去的情绪能预测抑郁，超出情绪变化幅度所能预测的。<bookmark mark='a'/>原始研究：库彭斯、艾伦和希伯，2010年。<bookmark mark='b'/>记录：在许多日记数据集中，动态指标在一个人的均值和离散之外几乎没有增加什么。<bookmark mark='c'/>惰性与抑郁有关，但它的大部分信号与更简单的概括指标是共享的，而且很难估计。<bookmark mark='d'/>有争议。",
    'The third: rising autocorrelation and variance warn':
        "第三条：上升的自相关和方差预示着进入或走出抑郁的转变。<bookmark mark='a'/>原始研究：范德莱姆普特及其同事，2014年。<bookmark mark='b'/>记录：一个在复发过程中被追踪的人，以及在许多人身上信号很弱的前瞻性检验。<bookmark mark='c'/>理论上成立；对于用日记测量的情绪，尚无定论。<bookmark mark='d'/>有争议。",
    'What the three have in common.':
        "这三条的共同点。<bookmark mark='a'/>每一条都关乎主张所处的层次：题目、个人，还是时刻。<bookmark mark='b'/>第一条已经确定，因为它是算术。忽略一个变异来源，错误率就会上升。<bookmark mark='c'/>另外两条对来自单个人的、短而嘈杂的序列要求太多。<bookmark mark='d'/>关于一个人的主张，需要关于这个人的数据：对每个人，许多次测量。",
    'Chapter fourteen. In practice: users, patients and dashboards.': "第14章。实践中：用户、患者与仪表盘。",
    'The question of this part runs through practice.':
        "这一部分的问题贯穿实践。<bookmark mark='a'/>产品指标：更多使用某个功能的用户参与度更高。使用它会让一个用户参与度更高吗？只有用户内部的数据，或者一项实验，才能回答。<bookmark mark='b'/>实验：随机分配用户，并在随机化的层次上分析。来自同一个用户的多次会话并不独立，而许多检验把它们当作独立的。<bookmark mark='c'/>个性化健康：一个可穿戴设备记录一个人好几个月，足以建立这个人自己的模型，如果问题是关于这个人的。<bookmark mark='d'/>学习和辅导：从横断面数据中读出的建议，是关于人们的建议，而不是关于你的。<bookmark mark='e'/>还有题目和提示：任何用了几个精心挑选的刺激、提示或情景的测试，都是从中抽取的样本。要把它们作为随机的纳入，或者缩小主张。",
    'Chapter fifteen. Frontier: the science of one.': "第15章。前沿：关于一个人的科学。",
    'Three frontiers.':
        "三个前沿。<bookmark mark='a'/>大规模的个体特异性科学：为每个人建立一个模型，用他们自己几个月的数据拟合，再在成千上万个人之间比较。<bookmark mark='b'/>需要多少数据：一个主张需要多少刺激、多少次测量、多少人，像功效一样在每个层次上同时规划。<bookmark mark='c'/>还有数据流与模型：手机和可穿戴设备持续记录睡眠、活动和言语。把它们与心灵的模型连接起来是新的事，而隐私是第一位的。",
    'Open questions.':
        "开放的问题。<bookmark mark='a'/>哪些心理过程足够接近遍历，使群体研究能够描述个体？<bookmark mark='b'/>一个人的模型需要多少次测量，才能胜过总体的模型？<bookmark mark='c'/>能否从人们实际愿意提供的数据中读出预警信号？<bookmark mark='d'/>一个领域应当如何选择和报告它的刺激，使它的主张说清楚自己涵盖了什么？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>只按参与者分析时，关于“无”的研究大约一半结果显著。在点云中，一个人的x上升时y也上升，尽管在人与人之间它是下降的。在自己身上表现出群体相关的人不到十分之一。而二十天会把零点四的真实惰性变成大约零点三。<bookmark mark='b'/>数据的层次必须与主张的层次相匹配：题目、个人，还是时刻。",
    'Part forty-seven in twelve lines.':
        "用十二行总结第47部分。<bookmark mark='a'/>刺激是样本，忽略它们会让假阳性飙升。对试次求平均会丢掉结构。多层模型是回归之中的回归，部分合并能更好地描述每个人。参与者和题目是交叉的，模型可以是最大化的，也可以是简约的。功效也来自刺激。把预测变量分成个人均值和偏离，因为关系在一个人内部可能反转。遍历性很少成立，所以群体可能描述不了任何人。日记把每个人变成一条时间序列，而惰性的估计是有偏的。随时间的因果需要个体内的变化。临界点之前会先慢下来，尽管日记很难看到。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳遇到了多层模型、最小F′、遍历性和临界慢化，都经过模拟和拟合。绿色。<bookmark mark='b'/>第二个反驳，即心灵无法被实验，遇到了个体内的实验：单个案实验和微随机化试验。绿色。<bookmark mark='c'/>第三个，关于内省。日记是一天多次的自我报告：对记忆的依赖更少，但仍然是内省。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>逐人拟合的行为模型就在下一部分，第48部分。以被试和体素为层次的大脑数据是第49部分。跨研究的证据分量是第50部分。一次针对一个人的计算精神病学是第59部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道计算最小F′。一道收缩一个斜率。一道把一个预测分成个体内和个体间。一道预测惰性的偏差。一道求题目给精度设定的上限。一道求一种情绪的方差。最后一道带星号，请你设计一项关于个体内睡眠与焦虑的日记研究。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。尼尔·博尔格和让-菲利普·洛朗索的书讲授日记数据；格尔曼和希尔通过实例讲授多层模型；斯奈德斯和博斯克的书是标准参考。",
    'Four parts of the graduate toolkit done.':
        "研究生工具箱完成了四个部分。<bookmark mark='a'/>这一部分让数据的层次与主张的层次相匹配。<bookmark mark='b'/>接下来是模型本身。什么时候，一个心灵的计算模型不只是曲线拟合？第48部分：为行为建模。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
