"""Chinese narration for psych48: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第48部分：为行为建模'

CHAPTERS = {
    'Hook': '一条没有哪只动物走过的曲线',
    'Predict': '1. 在你身上：你的学习率，四个数字',
    'Model': '2. 认知模型是什么',
    'Fitting': '3. 拟合',
    'Recovery': '4. 参数恢复',
    'Sloppy': '5. 此消彼长的参数',
    'Compare': '6. 模型比较',
    'Goodfit': '7. 拟合得好也可能是坏事',
    'Hier': '8. 把人看作一个总体',
    'Law': '9. 一条其实是平均值的定律',
    'Levels': '10. 理性与资源理性',
    'Pdp': '11. 联结主义',
    'Llm': '12. 作为心灵模型的语言模型',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：表型、用户与辅导系统',
    'Frontier': '15. 前沿：摊销推断与被发现的模型',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'In 1956 the psychologist William Estes asked what a smooth learning curve means.':
        "1956年，心理学家威廉·埃斯蒂斯问：一条平滑的学习曲线意味着什么。<bookmark mark='a'/>这里是Psyche的一些学习者。每个人都在某一个试次上从猜测跳到知道，所以每条曲线都是一个台阶。<bookmark mark='b'/>把两百个这样的人平均起来，就出现了一条平滑、渐进的曲线。它不是任何一个学习者的形状。<bookmark mark='c'/>一个拟合这个平均值的模型，描述的是一个并不存在的心灵。这一部分讲的，就是如何不被模型欺骗的技艺。",
    'The series has fitted models all along.':
        "本系列一直在拟合模型。<bookmark mark='a'/>第17部分拟合了学习率。第25部分拟合了扩散模型，第40部分拟合了一个情绪模型。<bookmark mark='b'/>每一次，都是一个把参数变成行为的程序，加上一次寻找使数据最可能出现的参数的搜索。<bookmark mark='c'/>这一部分打开这套工具。参数能被恢复吗？模型能被区分吗？获胜的模型能重现数据的特征吗？<bookmark mark='d'/>一个模型本可能失败却没有失败时，它才不只是曲线拟合。",
    'So this part asks when a computational model of the mind is more than a curve fit.':
        "所以这一部分要问：什么时候，一个心灵的计算模型不只是曲线拟合。<bookmark mark='a'/>生成模型、似然与拟合。<bookmark mark='b'/>恢复、此消彼长与模型比较。<bookmark mark='c'/>后验预测、层级结构，以及平均值的危险。<bookmark mark='d'/>还有理性分析、神经网络，以及被当作心灵模型的语言模型。",
    'This is Part 48 of Psychology, Built: modelling behaviour.':
        "这是《心理学，从零搭建》第48部分：为行为建模。<bookmark mark='a'/>我们将把认知模型看作一个生成行为的程序。我们将用最大似然拟合它，使用多个起点，并遇到其中的陷阱。我们将检验参数能否被恢复，并看到两个此消彼长的参数。我们将比较模型，并检验这种比较能否把它们区分开。我们将问获胜的模型能否重现数据，并把人看作一个总体来拟合。我们还将看到描述不了任何人的平均值，然后是被当作心灵模型的神经网络和语言模型。",
    'Chapter one. On you: your learning rate, and four numbers.': "第1章。在你身上：你的学习率，四个数字。",
    "First, Part 17's bandit again.":
        "首先，再看第17部分的老虎机。<bookmark mark='a'/>Psyche玩两台机器；一台有百分之七十的时候付钱，到一半时它们互换。每个点是一次选择，付钱时为绿色。<bookmark mark='b'/>拟合Q学习者，学习率大约是零点四，逆温度接近五。真实值是零点三和五。<bookmark mark='c'/>在课程网站上，你可以自己来玩，看到你自己的学习率被拟合出来，旁边还会显示像你这样的学习率能从两百次选择中被恢复得多好。",
    'Now four numbers.':
        "现在写下四个数字。<bookmark mark='a'/>第一：一个学习者真实的学习率是零点四。从两百次选择中，拟合通常能接近到什么程度？<bookmark mark='b'/>第二：一个还倾向于重复选择的学习者的数据。模型比较有多大比例能选对模型？<bookmark mark='c'/>第三：六十个人中每个人的练习进步都是指数型的。什么曲线最能拟合他们的平均值？<bookmark mark='d'/>第四：三十个人，每人六十个试次。把他们看作一个总体来拟合，能把每个人学习率的误差减少多少？在这里暂停，把它们写下来。",
    'Chapter two. What a cognitive model is.': "第2章。认知模型是什么。",
    'What is a cognitive model?':
        "认知模型是什么？<bookmark mark='a'/>一个生成行为的程序：参数进去，选择出来，一个试次接一个试次。这是第17部分的学习者，写成八行。<bookmark mark='b'/>向前运行，它模拟人。向后运行，它的似然说明每个观察到的选择有多大可能。<bookmark mark='c'/>数据的似然，是模型给予这个人实际所做选择的概率，在所有试次上的乘积。<bookmark mark='d'/>罗伯特·威尔逊和安妮·柯林斯在2019年为这门技艺写了十条简单的规则。第一条是：先模拟，再拟合。",
    'Here are four models of the same bandit.':
        "这是同一台老虎机的四个模型。<bookmark mark='a'/>一枚有偏的硬币，一个参数。<bookmark mark='b'/>赢则留、输则换，带一些噪声。<bookmark mark='c'/>Q学习者，有一个学习率和一个逆温度。<bookmark mark='d'/>以及带持续性的Q学习者，一种重复上一次选择的倾向。<bookmark mark='e'/>每个都是关于选择如何做出的假设。这一部分其余的内容，就是问如何区分它们，以及该在多大程度上信任获胜者。",
    'Before fitting anything, simulate.':
        "在拟合任何东西之前，先模拟。<bookmark mark='a'/>运行每个模型，看看它做什么：每个四十名模拟玩家。<bookmark mark='b'/>一个简单的特征，是玩家在赢了之后、以及输了之后重复同一选择的频率。<bookmark mark='c'/>赢则留、输则换几乎从不在输后留下。Q学习者大约五次中留下三次，加上持续性之后，接近十次中留下九次。<bookmark mark='d'/>这些模型在看得见的地方意见不一，正是这一点使它们可以检验。先模拟，是威尔逊和柯林斯十条规则中的一条，这是有原因的。",
    'Chapter three. Fitting.': "第3章。拟合。",
    'Fitting is a search.':
        "拟合是一次搜索。<bookmark mark='a'/>对每个模型，找出使Psyche的两百次选择最可能出现的参数。<bookmark mark='b'/>贝叶斯信息准则对每个参数加一个惩罚，所以多出来的参数必须挣得自己的位置。<bookmark mark='c'/>Q学习者获胜。加上持续性拟合得稍好一点，但不足以抵偿它的代价。<bookmark mark='d'/>而获胜是相对的。四个模型中最好的那个，仍然可能是错的。",
    'Four traps in the search.':
        "搜索中的四个陷阱。<bookmark mark='a'/>局部最优：似然曲面可能有几个山峰，所以要从几个地方出发，保留最好的。<bookmark mark='b'/>边界：学习率必须在零和一之间，估计值落在边界上就是一个警告。<bookmark mark='c'/>没有似然：有些模型只能模拟。那就通过比较模拟和真实数据的概括统计量来拟合，或训练一个网络来反转模拟器。<bookmark mark='d'/>还有试次太少：几十次选择可能几乎约束不了两个参数。这是接下来两章的内容。",
    "Here's why restarts matter.":
        "这就是多个起点重要的原因。<bookmark mark='a'/>Psyche造出一个学得慢、选得果断、又倾向于重复选择的学习者，并从四十个随机起点出发，把三参数模型拟合到八十个试次上。<bookmark mark='b'/>十次中有七次到达最佳拟合：一个很低的学习率和一个很高的逆温度。<bookmark mark='c'/>其余的停在差三个对数似然单位的地方，讲的是另一个故事：一个学得更快、选得更随机、持续性更强的学习者。<bookmark mark='d'/>一个起点可能落在任何地方。用很多个，保留最好的，并报告有多少个结果一致。",
    'Chapter four. Parameter recovery.': "第4章。参数恢复。",
    'The first check on any model.':
        "对任何模型的第一项检查。<bookmark mark='a'/>在一个网格上选择真实参数。从每组参数模拟两百次选择，拟合，再把拟合得到的值对照真实值画出来。<bookmark mark='b'/>学习率恢复得很好。逆温度差一些，而且在它很高时最差，因为一个几乎确定性的选择者，很少透露它到底有多确定。<bookmark mark='c'/>如果一个参数不能从模拟数据中恢复，它在真实数据中的值就毫无意义。<bookmark mark='d'/>每篇建模论文都应该展示这张图，针对它自己的任务和它自己的试次数。",
    'So how many trials does a fit need?':
        "那么一次拟合需要多少个试次？<bookmark mark='a'/>在每个学习者五十、一百、两百和四百个试次下，运行同样的恢复研究。<bookmark mark='b'/>五十个试次时，拟合的学习率与真实值的相关只有大约零点六，逆温度还要更低。<bookmark mark='c'/>四百个试次时，两者都在零点九以上。<bookmark mark='d'/>试次数是一个设计决策，像功效一样，在收集数据之前用恢复研究来决定。",
    'Chapter five. Parameters that trade off.': "第5章。此消彼长的参数。",
    'Why is one parameter recovered better than another?':
        "为什么一个参数比另一个恢复得更好？看看整个似然。<bookmark mark='a'/>这是Psyche的两百次选择在学习率和逆温度每一种组合下的对数似然。越亮越可能。<bookmark mark='b'/>明亮的区域是一道弯曲的山脊，而不是一个山峰。较低的学习率配上较高的温度，几乎能同样好地解释数据。<bookmark mark='c'/>两者此消彼长：学得快、选得嘈杂，或学得慢、选得干脆。<bookmark mark='d'/>所以两组之间在一个参数上的差异，可能其实是另一个参数上的差异。在两个参数上一起比较人，或通过设计固定其中一个。",
    'The ridge shows up in repeated fits too.':
        "这道山脊在重复拟合中也会出现。<bookmark mark='a'/>取一个学习者，模拟四十次，每次都拟合。<bookmark mark='b'/>两个估计值呈负相关：一个偏高时，另一个往往偏低。<bookmark mark='c'/>一个学得快、选得嘈杂的学习者，和一个学得慢、选得干脆的学习者，做出的选择很相似。<bookmark mark='d'/>所以要把两者一起报告，在确定得好的东西上比较人，或者设计能把它们分开的任务，比如更多次的反转。",
    'Chapter six. Model comparison.': "第6章。模型比较。",
    'How to choose among models.':
        "如何在模型之间做选择。<bookmark mark='a'/>对嵌套模型，用似然比检验。<bookmark mark='b'/>AIC和BIC对每个参数加以惩罚，AIC着眼于预测，BIC着眼于在候选模型中找到真实的那个。<bookmark mark='c'/>交叉验证在一部分试次或人上拟合，预测其余的，是对推广最直接的检验。<bookmark mark='d'/>贝叶斯因子在先验上平均，权衡支持每个模型的证据：对灵活性是诚实的，对先验是敏感的。<bookmark mark='e'/>还有在群体上：不同的人可能使用不同的模型，所以要估计每个模型有多常见，而不仅仅是哪个模型在合并数据上获胜。",
    'And the comparison itself must be checked.':
        "比较本身也必须加以检验。<bookmark mark='a'/>Psyche从四个模型中的每一个模拟学习者，对每个数据集拟合全部四个模型，用BIC挑选。<bookmark mark='b'/>对角线是恢复；对角线之外是混淆。<bookmark mark='c'/>这里恢复得很好：每个模型的学习者中有十分之九以上被正确识别。少数持续性学习者仍然看起来像普通的Q学习者，因为他们的倾向太弱，两百次选择不足以抵偿第三个参数的代价。试次更少，或模型更相似，这个矩阵就会变得模糊。<bookmark mark='d'/>所以在真实数据上获胜的模型，也必须针对它自己的任务和试次数，用同样的方法检验。这次比较本来能够找到那些替代模型吗？",
    "Another way to compare: predict data the model hasn't seen.":
        "另一种比较方法：预测模型没见过的数据。<bookmark mark='a'/>三十个持续性学习者各玩两次。每个模型都在第一次上拟合，在第二次上评分。<bookmark mark='b'/>留出数据的预测只奖励能推广的东西，所以拟合噪声的多余参数会自动受到惩罚。<bookmark mark='c'/>真实的模型对新的一次预测得最好，而第一次数据上的BIC为十分之九以上的学习者选中了它。<bookmark mark='d'/>当两者不一致时，相信回答你所问问题的那一个：预测，还是哪个模型是真的。",
    'Chapter seven. A good fit can be bad.': "第7章。拟合得好也可能是坏事。",
    "A model that fits well isn't therefore a good model.":
        "一个拟合得好的模型，并不因此就是好模型。<bookmark mark='a'/>2000年，塞思·罗伯茨和哈罗德·帕施勒指出，只有当模型本可能失败时，拟合才有说服力。<bookmark mark='b'/>问一问模型产生不了什么数据。一个能拟合所有可能结果的模型，什么也解释不了。<bookmark mark='c'/>问一问数据的变异有多大。在噪声范围之内的拟合说明不了多少。<bookmark mark='d'/>问一问一个说得过去的替代模型是否拟合得一样好。<bookmark mark='e'/>最强的证据，是在数据之前就做出的、关于模型必须产生的某个效应的预测。",
    "Here's the check in practice.":
        "这是实践中的检查。<bookmark mark='a'/>Psyche的学习者有一种重复自己的倾向。拟合两个模型，再从每个拟合结果中模拟新数据。<bookmark mark='b'/>输了之后，学习者有大约百分之八十五的时候留在同一台机器上。普通Q学习者的模拟只有百分之七十。无论它的得分如何，它都产生不了这个效应。<bookmark mark='c'/>加上持续性，模拟就吻合了。<bookmark mark='d'/>斯特凡诺·帕尔明泰里、瓦伦丁·怀亚特和艾蒂安·克什兰在2017年把这定为规则：检查获胜的模型能否产生数据的特征，而不只是它得分最高。",
    "Roberts and Pashler's question can be drawn.":
        "罗伯茨和帕施勒的问题可以画出来。<bookmark mark='a'/>为每个模型取六十组随机参数，进行模拟。每个点是一个可能的玩家，按它输后留下和赢后留下的频率来放置。<bookmark mark='b'/>赢则留、输则换住在一个角落里。它输后留下的频率永远不会超过它的错误率所允许的程度。<bookmark mark='c'/>Q学习覆盖一条带子，加上持续性之后，几乎覆盖整个方块。<bookmark mark='d'/>一个能产生任何东西的模型，并不因为产生了这个结果就得到证实。要问它排除了什么。",
    'Chapter eight. People as a population.': "第8章。把人看作一个总体。",
    'Real studies rarely give each person two hundred trials.':
        "真实的研究很少给每个人两百个试次。<bookmark mark='a'/>Psyche造出三十个人，每人六十个试次，他们的学习率围绕一个总体平均值而不同。<bookmark mark='b'/>单独拟合时，每个估计都很嘈杂，有些还跑到了边界上。<bookmark mark='c'/>把他们看作从一个总体中抽取的来拟合，每个估计都被拉向群体，越不确定拉得越多。误差下降了将近一半。<bookmark mark='d'/>一个完整的贝叶斯层级模型对所有参数同时这样做，并估计人与人之间实际上差异多大，正如迈克尔·李和埃里克-扬·瓦根马克斯所讲授的。",
    'When does fitting people as a population pay?':
        "什么时候把人看作一个总体来拟合是值得的？<bookmark mark='a'/>四十个人，每种长度模拟四组。<bookmark mark='b'/>每人三十个试次时，单独拟合在对数几率尺度上偏差大约一个单位。看作总体时，大约一半。<bookmark mark='c'/>两百四十个试次时，两者很接近：每个人的数据足以说明自己。<bookmark mark='d'/>数据最少的地方，合并帮助最大：短任务、患者和儿童。",
    'Chapter nine. A law that was an average.': "第9章。一条其实是平均值的定律。",
    "Estes's warning has a famous case.":
        "埃斯蒂斯的警告有一个著名的例子。<bookmark mark='a'/>1981年，艾伦·纽厄尔和保罗·罗森布鲁姆表明，在许多技能中，练习曲线都遵循幂律。它成了练习定律。<bookmark mark='b'/>Psyche的六十个学习者每人都以指数方式加快，速率差别很大，而对几乎所有人来说，指数函数都比幂函数拟合得更好。<bookmark mark='c'/>但他们的平均值用幂律拟合得更好。<bookmark mark='d'/>2000年，安德鲁·希思科特、斯科特·布朗和道格拉斯·梅沃特对真实的练习数据逐人拟合，发现指数函数更胜一筹。这条定律描述的是平均值，而不是学习者。",
    'Chapter ten. Rational and resource-rational.': "第10章。理性与资源理性。",
    'Fitting asks how; another tradition asks why.':
        "拟合问的是怎样；另一个传统问的是为什么。<bookmark mark='a'/>约翰·安德森的理性分析，从心灵想要达成的目标出发，<bookmark mark='b'/>描述它所处的环境及其统计特征，<bookmark mark='c'/>对它的局限做最少的假设，<bookmark mark='d'/>推导出最优的行为，并与人进行比较。<bookmark mark='e'/>如果两者不同，就修改目标、环境或局限，而不是最优性。<bookmark mark='f'/>1991年，安德森与莱尔·斯库勒一起表明，记忆的遗忘曲线与信息在世界中再次被需要的频率相吻合。这是马尔的计算层次，被做成了一种方法。",
    'Real minds have limits.':
        "真实的心灵有局限。<bookmark mark='a'/>人对问题本身并不是最优的；但对问题加上他们的局限，他们可能是最优的。<bookmark mark='b'/>福尔克·利德和汤姆·格里菲思称之为资源理性分析：思考本身是有代价的，所以要问如何最好地使用有限的预算。<bookmark mark='c'/>第24部分的启发式和偏差，就成了一个无法计算一切的心灵的明智策略。<bookmark mark='d'/>危险在于：如果可以随意选择代价，任何行为都能被称为理性的。代价必须被测量，而不是为了拟合而选定。",
    'Resource-rational analysis can be computed.':
        "资源理性分析可以计算出来。<bookmark mark='a'/>在两个选项之间做选择，方法是对它们的差异进行抽样取证，每个样本都很弱。<bookmark mark='b'/>准确率随样本增加而上升，但越来越慢。<bookmark mark='c'/>现在对每个样本收费。最佳数目下降得很快：思考便宜时大约三十六个样本，代价高十倍时只要五个。<bookmark mark='d'/>一个只凭少数几个样本做决定的心灵，可能正在很好地利用它的时间。这就是对只凭一两个样本做决定的资源理性解读，而人们似乎常常正是这样做的。",
    'Chapter eleven. Connectionism.': "第11章。联结主义。",
    'A different kind of model came with the 1980s.':
        "二十世纪八十年代带来了另一种模型。<bookmark mark='a'/>1986年，戴维·鲁梅尔哈特、詹姆斯·麦克莱兰和PDP小组把认知建模为许多简单的单元，知识储存在单元之间的权重里，从例子中学得。<bookmark mark='b'/>网络带来了什么：分级的、学得的表征，无需写出而自行涌现的规则，以及优雅降级的损伤。<bookmark mark='c'/>它们的代价：一个拟合好的网络可能和它所模拟的心灵一样难以理解，而学习新东西可能抹去旧的，即第21部分的灾难性干扰。<bookmark mark='d'/>规则与网络之争，从英语过去时开始，持续了几十年。如今的语言模型是它的继承者。",
    'Chapter twelve. Language models as models of minds.': "第12章。作为心灵模型的语言模型。",
    'A new kind of candidate model.':
        "一种新的候选模型。<bookmark mark='a'/>可以把一个心理学实验以文字形式交给语言模型，并像给参与者评分那样给它的回答评分。<bookmark mark='b'/>2023年，马塞尔·宾茨和埃里克·舒尔茨把经典的判断任务交给了这样一个模型。在有些任务上，它的回答很像人，包括偏差在内；在另一些地方它失败了。<bookmark mark='c'/>后来，在许多实验的逐试次数据上微调过的模型，被提出作为人类选择的一般模型，能很好地预测留出的参与者。<bookmark mark='d'/>适用于任何模型的检查同样适用：恢复、与简单模型的比较，以及它是否出于正确的原因产生了那些效应。",
    'Which raises an old question in a new form.':
        "这就以新的形式提出了一个老问题。<bookmark mark='a'/>赞成的一方：如果一个模型能预测人们在新情境中的行为，它就学到了关于行为的某些真实的东西。<bookmark mark='b'/>反对的一方：一个和心灵一样复杂的模型，把解释的工作原封不动地留了下来。我们对它的理解，并不比对它所模仿的人更多。<bookmark mark='c'/>一条中间道路：把大模型当作一个基准。一个小而可解释的模型能捕捉多少可预测的行为？<bookmark mark='d'/>第60部分问这类系统是什么，第61部分问它们改变了科学的什么。",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Two new rows.':
        "两条新记录。第一条：反应时随练习下降，对每个学习者来说都遵循幂函数。<bookmark mark='a'/>原始研究：纽厄尔和罗森布鲁姆，1981年。<bookmark mark='b'/>记录：逐人拟合时，练习数据更支持指数函数。<bookmark mark='c'/>幂律出现在平均值中，正如第九章所计算的。<bookmark mark='d'/>在学习者的层次上，失败。",
    'The second: fitted model parameters':
        "第二条：拟合出的模型参数，比如学习率，是能跨任务推广的稳定特质，可以用作临床标志物。<bookmark mark='a'/>原始研究：蒙塔古及其同事在2012年阐述的计算精神病学纲领。<bookmark mark='b'/>记录：参数常常不能跨任务推广，重测信度也常常很低。<bookmark mark='c'/>在一个任务之内是有用的概括；作为特质，还不行。<bookmark mark='d'/>有争议。",
    'What the two have in common.':
        "这两条的共同点。<bookmark mark='a'/>两者都是从拟合中得出的关于个体的主张。<bookmark mark='b'/>第一条拟合了一个平均值，却称之为一个学习者。第二条拟合了学习者，却称拟合结果为一种特质。<bookmark mark='c'/>两者都被这一部分的检查抓住了：逐人拟合，在解释一个参数之前先检验恢复和信度。<bookmark mark='d'/>参数是一种测量，第3部分的问题同样适用于它。",
    'Chapter fourteen. In practice: phenotypes, users and tutors.': "第14章。实践中：表型、用户与辅导系统。",
    'Where fitted models of behaviour run.':
        "拟合出的行为模型在哪里运行。<bookmark mark='a'/>计算表型分析把任务模型拟合到患者身上，描述有什么不同。恢复和信度要放在第一位，第59部分会说明。<bookmark mark='b'/>用户建模把学习和探索拟合到人们使用产品的方式上，参数之间同样存在此消彼长。<bookmark mark='c'/>模拟用户在真实用户之前测试一个设计：便宜，但只和模型的恢复与预测一样好。<bookmark mark='d'/>辅导系统运行第45部分的知识追踪，即每个学习者的一个拟合模型，在每次作答后更新。<bookmark mark='e'/>它们都适用同一份清单：模拟、恢复、比较、检查预测、层级拟合，而且永远不要拟合一个平均值，然后称之为一个人。",
    'Chapter fifteen. Frontier: amortized inference and discovered models.': "第15章。前沿：摊销推断与被发现的模型。",
    'Three frontiers.':
        "三个前沿。<bookmark mark='a'/>摊销推断在数百万次模拟上训练一个网络，一次完成，把数据映射到参数。之后拟合一个新的人是瞬间的事，即使对没有似然的模型也是如此。<bookmark mark='b'/>模型发现在程序之间搜索，或者让网络提出方程，寻找最能预测留出人群的模型，然后检查它是否仍然可以解释。<bookmark mark='c'/>还有行为的基础模型。要算作心灵的模型，它需要能预测新的任务，出于正确的原因重现经典效应，并像任何其他模型一样接受检验。",
    'Open questions.':
        "开放的问题。<bookmark mark='a'/>一个参数需要多少个试次才能成为一种特质？<bookmark mark='b'/>一个模型能否既是强有力的预测者，又是一种解释？<bookmark mark='c'/>当每个候选模型都是错的时，模型比较应该如何进行？<bookmark mark='d'/>一个被发现的模型必须展示什么，才能被相信？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>零点四的学习率，从两百次选择中，通常能被恢复到相差百分之几以内。模型比较识别出了十分之九以上的持续性学习者。指数型学习者的平均值用幂律拟合得最好。把三十个人看作一个总体来拟合，使每个学习率的误差减少了将近一半。<bookmark mark='b'/>一个模型凭它通过的检查赢得信任，而不是凭它的拟合。",
    'Part forty-eight in twelve lines.':
        "用十二行总结第48部分。<bookmark mark='a'/>一个平均值可能描述不了任何人。认知模型是从参数到行为的程序，用最大似然拟合，使用多个起点和边界。在信任参数之前，先从模拟中恢复它们，并留意沿着山脊此消彼长的参数。用带惩罚的拟合或预测来比较模型，并检验这种比较能否恢复真实模型。拟合得好也可能是坏事，所以要问模型排除了什么，以及它能否产生那个效应。层级拟合在人与人之间借力。理性分析问为什么，网络问怎样。而预测还不是解释。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳遇到了似然、恢复、模型比较和层级结构，全都公开运行。绿色。<bookmark mark='b'/>第二个反驳遇到了用它们必须产生的效应、在它们没见过的数据上检验的模型。绿色。<bookmark mark='c'/>第三个，关于内省：这些是选择的模型，而不是报告的模型，所以这个反驳不会出现。绿色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>大脑数据的模型就在下一部分，第49部分。跨研究的证据分量是第50部分。以恢复为先的计算精神病学是第59部分。作为心灵的语言模型是第60部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道计算softmax选择。一道更新一个值。一道计算对数似然。一道用BIC比较两个模型。一道对跳跃式学习者求平均。一道收缩一个学习率。最后一道带星号，请你为一个新任务的新模型规划全部检查。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。法雷尔和莱万多夫斯基的书讲授这门技艺；李和瓦根马克斯讲授贝叶斯的版本；而威尔逊和柯林斯的十条规则写在一页纸上，在任何拟合之前都应该读一读。",
    'Five parts of the graduate toolkit done.':
        "研究生工具箱完成了五个部分。<bookmark mark='a'/>这一部分打开了整个系列一直在用的拟合工具。<bookmark mark='b'/>接下来是大脑。七十个团队拿到同一个脑成像数据集，却得出了不同的答案。一张脑图要成为证据，必须满足什么条件？第49部分：为大脑数据建模。",
    'How many learners does it take to make a law?':
        "需要多少个学习者才能造出一条定律？<bookmark mark='a'/>把k个Psyche的指数型学习者平均起来，每个k重复六十次，看哪条曲线更好地拟合平均值。<bookmark mark='b'/>只有一个学习者时，幂律只是靠噪声，大约十二次中赢一次。<bookmark mark='c'/>有三十个学习者时，它赢的比例是百分之八十八。把不同的速率平均起来，就制造出了幂律。<bookmark mark='d'/>这就是第47部分和这一部分的道理：先拟合个人，再描述总体，绝不能反过来。",
    'So what is a network model tested against?':
        "那么网络模型用什么来检验？<bookmark mark='a'/>过去式。鲁梅尔哈特和麦克莱兰的网络学会了英语的过去式，中间有一个下降：在说过went之后又说goed，就像儿童那样。史蒂文·平克和艾伦·普林斯认为，这个下降来自训练的安排方式。<bookmark mark='b'/>朗读。马克·塞登伯格和麦克莱兰的三角模型用同一组权重朗读规则词和不规则词，并预测了它们的命名时间。<bookmark mark='c'/>损伤。受损的网络先失去具体的知识，最后失去一般的知识，就像语义性痴呆患者那样。<bookmark mark='d'/>标准与这一部分中的任何模型相同。一个网络靠预测错误和时间的模式赢得一席之地，而不是靠准确。",
    'How should a language model be tested as a model of mind?':
        "应该如何把语言模型当作心智的模型来检验？<bookmark mark='a'/>当心污染。经典任务都在网上，模型可能读过答案，所以要用新的题目和新的故事。<bookmark mark='b'/>检验过程。它的错误，以及它在每道题上遇到的难度，与人的是否一致？第23部分中用惊异度预测阅读时间，就是这样一种检验。<bookmark mark='c'/>记住它是许多人，而不是一个人。模型的回答构成的分布并不是某一个人的，所以要把它与人与人之间的离散相比较，而不只是与均值比较。<bookmark mark='d'/>还要胜过基线：在宣称更多之前，先胜过每项任务的简单拟合模型。",
    "Here's a computational phenotype, worked.":
        "这是一个完整的计算表型示例。<bookmark mark='a'/>一家诊所想知道焦虑患者从损失中学习的方式是否不同。它使用一个多臂老虎机任务，每人两百次选择。<bookmark mark='b'/>首先，用候选模型模拟这个任务，检查对损失的学习率能否从两百次选择中恢复出来。<bookmark mark='c'/>用层级方法拟合，用交叉验证比较模型，并检查胜出的模型能否重现输后保持的模式。<bookmark mark='d'/>然后在预先登记的前提下，带着不确定性检验这个参数上的组间差异，并对一部分患者进行重测，看这个参数是否稳定。<bookmark mark='e'/>一个无法恢复或不稳定的参数不是表型，无论故事有多好。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
