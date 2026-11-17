"""Chinese narration for psych46: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第46部分：标度、调查与选择'

CHAPTERS = {
    'Hook': '哪种罪行更严重？',
    'Predict': '1. 在你身上：十二次比较，四个数字',
    'Thurstone': '2. 比较判断律',
    'Luce': '3. 卢斯的选择公理',
    'Utility': '4. 随机效用',
    'Context': '5. 公理失效之处',
    'Models': '6. 情境效应的模型',
    'Conjoint': '7. 联合分析',
    'Process': '8. 在问题与回答之间',
    'Effects': '9. 问题效应',
    'Scales': '10. 评定量表',
    'Quality': '11. 在线数据的质量',
    'Nps': '12. 一个数字统治一切？',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：定价、民调与排行榜',
    'Frontier': '15. 前沿：因果、偏好与模拟的受访者',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'In 1927 Louis Thurstone, in Chicago, gave students a list of offences.':
        "1927年，路易斯·瑟斯顿在芝加哥给学生们一份罪行清单。<bookmark mark='a'/>对每一对罪行：哪一个更严重？<bookmark mark='b'/>没有人能说出纵火在某个尺度上有多严重。但每个人都能说出两种罪行中哪一种更坏。<bookmark mark='c'/>人们意见不一，同一个人两次回答也可能不同。瑟斯顿看出，这种不一致本身就是信息。<bookmark mark='d'/>从选择每一边的人所占的比例，他推导出一把严重程度的尺子：为没有单位的东西给出一个数字。",
    'From those comparisons grew a whole science of choice.':
        "从这些比较中，生长出一整门关于选择的科学。<bookmark mark='a'/>瑟斯顿：每个选项唤起一个波动的印象，选择跟随较大的那个。<bookmark mark='b'/>1959年，邓肯·卢斯用一条关于选择的公理取代了这些印象。<bookmark mark='c'/>1974年，丹尼尔·麦克法登用同一个模型预测人们会如何出行，这项工作后来获得了诺贝尔经济学奖。<bookmark mark='d'/>1982年，研究表明，一个没有人会选的诱饵会改变人们选什么。公理失效了，偏好随菜单而弯曲。",
    'So this part asks how to turn I prefer this one into a number':
        "所以这一部分要问：如何把“我更喜欢这个”变成一个数字，以及在问题和回答之间发生了什么。<bookmark mark='a'/>成对比较、瑟斯顿定律和卢斯公理。<bookmark mark='b'/>随机效用、逻辑模型，以及它失效的地方。<bookmark mark='c'/>诱饵、折中，以及为产品定价的联合分析研究。<bookmark mark='d'/>还有在一个调查问题和它的回答之间发生了什么。",
    'This is Part 46 of Psychology, Built: scaling, surveys and choice.':
        "这是《心理学，从零搭建》第46部分：标度、调查与选择。<bookmark mark='a'/>我们将推导瑟斯顿定律，并把它拟合到真实的偏好上。我们将用一个总是向上爬的简单算法拟合卢斯的模型。我们将说明，带有恰当噪声的随机效用会给出逻辑模型。我们将用一个模型构建出诱饵效应和折中效应。我们将做一项联合分析研究，为它的属性定价。我们还将跟随一个调查问题直到它的回答，经过反应风格和净推荐值。",
    'Chapter one. On you: twelve comparisons, and four numbers.': "第1章。在你身上：十二次比较，四个数字。",
    "First, a small version of Thurstone's task.":
        "首先，做一个小型的瑟斯顿任务。<bookmark mark='a'/>每一对，快速选一个。<bookmark mark='b'/>四个选项组成六对。数一数每个选项赢了几次。<bookmark mark='c'/>再检查一下自己。如果你选了海边而不是城市，选了城市而不是家，那你是不是也选了海边而不是家？<bookmark mark='d'/>在课程网站上，你可以自己做十二次比较，看它们变成一把尺子，还会遇到一个诱饵。",
    'Now four numbers to write down.':
        "现在写下四个数字。<bookmark mark='a'/>第一：九种蔬菜，每一对都比较。有多大比例的人喜欢玉米胜过芜菁？<bookmark mark='b'/>第二：两个选项各占一半。加入第三个选项，它在两个属性上都比第一个差。第一个选项的份额会怎样？<bookmark mark='c'/>第三：两种无关的特质，各用六道方向相同的题目测量，有些人对什么都同意。两个量表的相关有多强？<bookmark mark='d'/>第四：来自两百名顾客的净推荐值。它的误差范围是多少分？在这里暂停，把它们写下来。",
    'Chapter two. The law of comparative judgment.': "第2章。比较判断律。",
    "Thurstone's idea.":
        "瑟斯顿的想法。<bookmark mark='a'/>每个选项唤起一个时刻在变化的印象：一个均值为s的正态分布。<bookmark mark='b'/>选择归于较大的印象。两个独立正态之差仍是正态，方差加倍。这就是他的情形五：离散相等，没有相关。<bookmark mark='c'/>把正态曲线反过来，每个比例就给出尺子上的一段距离。这是第12部分的信号检测，用在两个刺激之间。<bookmark mark='d'/>百分之五十意味着没有距离。百分之八十四意味着一个单位。而百分之百意味着尺子说不出有多远。",
    'Here is the method on real preferences.':
        "这是这个方法在真实偏好上的应用。<bookmark mark='a'/>J. P. 吉尔福德的学生比较了九种蔬菜的每一对。每个方格是喜欢行胜过列的人所占的比例。<bookmark mark='b'/>情形五把三十六个比例变成九个数字：芜菁在最底下，玉米在最上面。<bookmark mark='c'/>而这九个数字能重现全部比例，平均误差大约三个半百分点。一个维度几乎就够了。<bookmark mark='d'/>这把尺子的零点和单位是任意的。用第3部分的话说，它是等距尺度。",
    'How many judges does a scale need?':
        "一把尺子需要多少评判者？<bookmark mark='a'/>取九个均匀分布的刺激，在情形五下模拟评判小组。<bookmark mark='b'/>五个评判者时，每个尺度值大约偏差三分之一个标准差。二十五个时，大约八分之一。一百个时，十六分之一。<bookmark mark='c'/>小组每扩大到四倍，误差就减半：平方根定律，和任何平均值一样。<bookmark mark='d'/>所以一个小组可以给相距很远的刺激排序，却排不了相距十分之一个标准差的刺激。",
    "Chapter three. Luce's choice axiom.": "第3章。卢斯的选择公理。",
    "Luce's starting point was an axiom, not a mechanism.":
        "卢斯的出发点是一条公理，而不是一个机制。<bookmark mark='a'/>选择一个选项而不是另一个的几率，不取决于还提供了什么别的选项。这叫作无关选项的独立性。<bookmark mark='b'/>如果它成立，每个选项就有一个强度，确定到相差一个公共因子。从一条关于选择的假设，得到一个比率尺度。<bookmark mark='c'/>对于成对比较，它就是布拉德利和特里1952年的模型，换一种形式，就是阿帕德·埃洛的国际象棋等级分。<bookmark mark='d'/>取对数，强度就变成一把像瑟斯顿那样的尺子，只是用逻辑曲线代替了他的正态曲线。",
    "Fitting Luce's model is easy.":
        "拟合卢斯的模型很容易。<bookmark mark='a'/>数出每个选项赢的次数，以及每一对之间比较的次数。<bookmark mark='b'/>然后按这条规则一遍又一遍地更新每个强度。每次更新都会增加似然。这是一种极小化-极大化算法。<bookmark mark='c'/>在蔬菜数据上，它大约需要九十次更新，卢斯的尺子和瑟斯顿的几乎完全一致。<bookmark mark='d'/>两者之间的斜率就是那条老经验法则：逻辑曲线是被拉伸了大约一点七倍的正态曲线。",
    "Luce's model now runs leaderboards, so how many votes does one need?":
        "卢斯的模型如今运行着排行榜，那么一个排行榜需要多少票？<bookmark mark='a'/>二十个参赛者，具有布拉德利-特里强度。每一票比较随机的一对，排行榜就是拟合结果。<bookmark mark='b'/>四百票之后，顺序几乎是对的。<bookmark mark='c'/>但真正最好的那个排在第一位的时候还不到一半。三千两百票之后，大约五次中有四次。<bookmark mark='d'/>整体顺序学得很快，顶端却学得很慢，因为顶端的相邻者相差很小，比较它们的票又很少。要报告区间，而不仅仅是名次。",
    'Chapter four. Random utility.': "第4章。随机效用。",
    'Economists reached the same formula by another road.':
        "经济学家沿着另一条路得到了同样的公式。<bookmark mark='a'/>每个选项的效用，是来自其属性的系统部分，加上一个随机部分。<bookmark mark='b'/>如果随机部分相互独立，并服从冈贝尔分布，也就是许多冲击中最大者的规律，那么一个选项成为最佳的概率恰好就是逻辑模型。<bookmark mark='c'/>Psyche用四十万次模拟选择来检验它。份额与公式在小数点后第三位上一致。<bookmark mark='d'/>于是卢斯公理与随机效用相遇了。同一个公式，来自一个机制。",
    'Daniel McFadden made the model a tool.':
        "丹尼尔·麦克法登把这个模型变成了工具。<bookmark mark='a'/>在条件逻辑模型中，效用是一个选项各属性的加权和，比如出行时间、费用和步行，权重由人们观察到的选择拟合出来。<bookmark mark='b'/>在旧金山湾区的BART轨道交通系统开通之前，他的通勤者模型预测了它在出行中的份额。<bookmark mark='c'/>这个预测接近实际观察到的份额，而工程预测则高得太多。<bookmark mark='d'/>这个方法传播到交通规划、市场营销、能源和卫生经济学，并使他在2000年获得了诺贝尔奖。",
    'Chapter five. Where the axiom fails.': "第5章。公理失效之处。",
    "The axiom's most famous failure.":
        "这条公理最著名的失效。<bookmark mark='a'/>一个通勤者在汽车和红色巴士之间无所谓：一半对一半。<bookmark mark='b'/>加入一辆蓝色巴士，除了颜色完全相同。公理让汽车对红色巴士的几率保持一比一，所以每个选项得到三分之一。<bookmark mark='c'/>但蓝色巴士只是分走了乘巴士的人。汽车保持一半，每辆巴士得到四分之一。<bookmark mark='d'/>当选项相似时公理会失效，因为它们的随机部分是相关的，而不是独立的。嵌套逻辑模型和混合逻辑模型允许这一点。",
    "Menus also bend preferences in ways that similarity can't explain.":
        "菜单还会以相似性解释不了的方式弯曲偏好。取两个选项A和B，各自在一个属性上更好。<bookmark mark='a'/>1982年，乔尔·休伯、约翰·佩恩和克里斯托弗·普托加入了一个在两个属性上都比A稍差的诱饵。A的份额上升了。没有人选诱饵，可它起了作用。<bookmark mark='b'/>1989年，伊塔马尔·西蒙森改为加入一个极端选项，现在处在中间的A得益了。这是折中效应。<bookmark mark='c'/>而阿莫斯·特沃斯基在1972年已经表明，一个新选项主要从与它相似的选项那里夺取份额。<bookmark mark='d'/>每一种都打破了卢斯公理：菜单改变了同样两个选项之间的几率。",
    'Chapter six. Models of context effects.': "第6章。情境效应的模型。",
    'What kind of chooser bends with the menu?':
        "什么样的选择者会随菜单而弯曲？<bookmark mark='a'/>Psyche通过比较来权衡。在每个时刻，它看一对选项在一个属性上的比较。较好的得分，较差的失分，而损失比收益显得更重。<bookmark mark='b'/>A的诱饵在每一方面都输给A，所以A得分，从百分之五十升到大约四分之三。B的诱饵作用相反。<bookmark mark='c'/>在A另一侧的一个极端选项，把A放到了中间，在那里它永远不会输得很多，A的份额上升了。<bookmark mark='d'/>一个机制，两种效应，而A或B的价值都没有改变。",
    'The model also says when these effects should appear.':
        "这个模型还说明了这些效应应当在什么时候出现。<bookmark mark='a'/>两者都随权衡时间增长。更多的比较给了菜单更多发挥作用的机会。<bookmark mark='b'/>折中效应需要很多次比较。比较很少时，它就消失了。<bookmark mark='c'/>这是一个可检验的预测：时间压力应当缩小情境效应。实验在折中效应上发现了这一点。<bookmark mark='d'/>第25部分的序列抽样模型，扩展到多个选项后，也做出同类的预测。",
    'Chapter seven. Conjoint analysis.': "第7章。联合分析。",
    'Conjoint analysis turns the logit into a tool for designing products.':
        "联合分析把逻辑模型变成了设计产品的工具。<bookmark mark='a'/>每个任务展示三款产品，由四个属性的不同水平组合而成：价格、电池、相机和品牌。选一个。<bookmark mark='b'/>每个人做十二个任务，各水平按设计变化，所以每个属性的效应可以被分离出来。<bookmark mark='c'/>这些选择用条件逻辑模型拟合，每个水平有一个部分价值。",
    'Does it work?':
        "它有效吗？<bookmark mark='a'/>Psyche模拟了六百个人，每人都有自己的部分价值，围绕着一个已知的平均值，就是那些黄线。<bookmark mark='b'/>逻辑模型的估计值靠近平均值，略有收缩，因为人与人不同。混合逻辑模型可以为这种离散建模。<bookmark mark='c'/>支付意愿是部分价值之比。两天续航的电池值大约一百六十美元，出色的相机大约九十美元，都接近植入的数值。<bookmark mark='d'/>需要记住的一个假设：各属性的价值是可以相加的。",
    'With the part-worths, a firm can simulate a market.':
        "有了部分价值，一家公司就可以模拟一个市场。<bookmark mark='a'/>三款手机在售，预测的份额如图。<bookmark mark='b'/>把第一款降到五百美元，它的份额升到大约一半，按比例从两个对手那里夺来。这又是逻辑模型的公理，红色巴士之类全都在内。<bookmark mark='c'/>真实的市场还加上调查做不到的东西：知名度、可得性，以及完全不买的选择。<bookmark mark='d'/>联合分析是陈述选择的模型。要拿它与人们的实际行为对照检查。",
    'How many respondents does a conjoint study need?':
        "一项联合分析研究需要多少受访者？<bookmark mark='a'/>在每种规模下把同一项研究运行四十次。竖条包含了中间百分之八十的估计值。<bookmark mark='b'/>只有五十人时，两天续航的电池可能值大约一百二十美元到将近两百美元之间的任何数。<bookmark mark='c'/>有八百人时，与植入的一百五十美元相差在大约十五美元以内。<bookmark mark='d'/>支付意愿是两个估计值之比，比其中任何一个都更嘈杂。在给产品定价之前，先给精度定价。",
    'Chapter eight. Between the question and the answer.': "第8章。在问题与回答之间。",
    'A survey question looks like a measurement.':
        "一个调查问题看起来像一次测量。它其实是一个小任务。<bookmark mark='a'/>受访者必须理解它。过去一周、经常、家庭：每个词不同的人读起来都不一样。<bookmark mark='b'/>提取：在记忆中搜索相关的事件，带着第20部分所有的遗忘和时间错误。<bookmark mark='c'/>判断：把想到的东西组合成一个答案，靠计数、估计，或凭总体印象。<bookmark mark='d'/>报告：把判断对应到提供的类别上，也许还会修饰一下，让自己显得好些。<bookmark mark='e'/>罗杰·图兰若的模型把每一种调查误差都定位在这些步骤中的某一步，每一步都有自己的补救办法。",
    'Doing all four steps carefully takes effort.':
        "认真完成全部四步需要付出努力。<bookmark mark='a'/>1991年，乔恩·克罗斯尼克提出，当动机或能力较低时，受访者会走捷径。他称之为满意即止，这是第24部分赫伯特·西蒙的词。<bookmark mark='b'/>弱满意即止：第一个可以接受的答案、表示同意、选中间的类别。<bookmark mark='c'/>强满意即止：不知道、在整个表格中都给同一个答案，或者随机点击。<bookmark mark='d'/>它随难度和疲劳而增加：在长问卷的后段、在难的问题上、在动机较低的受访者中。<bookmark mark='e'/>补救办法在设计里：更短的调查、清楚的问题，以及让人在乎的理由。",
    'Chapter nine. Question effects.': "第9章。问题效应。",
    'The same question, asked differently, gets different answers.':
        "同一个问题，问法不同，得到的回答也不同。<bookmark mark='a'/>1941年，唐纳德·拉格问美国人：国家应当禁止反对民主的公开演讲，还是应当允许它们？不允许这类演讲的人，比主张禁止的人更多，尽管这两个问题在逻辑上是一样的。<bookmark mark='b'/>顺序：同样两个问题，以不同的顺序提出，得到不同的回答，因为第一个问题为第二个设定了框架。<bookmark mark='c'/>锚定：提供的类别暗示了什么是正常的。一个从“最多半小时”开始的看电视时长量表，会让回答往下移。<bookmark mark='d'/>还有社会赞许性：投票、锻炼和慈善被多报，饮酒被少报，当面访问比在线调查更甚。",
    'One habit can manufacture a finding.':
        "一个习惯就能制造出一个发现。<bookmark mark='a'/>Psyche造出两种无关的特质，各有六道题，再加上一些对什么说法都同意的人。李·克龙巴赫在1946年描述了这种反应定势。<bookmark mark='b'/>所有题目方向相同时，这种风格同时加进两个分数，它们的相关大约是零点二五，尽管特质本身并不相关。<bookmark mark='c'/>平衡题目方向，一半题目反向计分，这种风格在每个总分中相互抵消。<bookmark mark='d'/>两份问卷之间的相关，可能只是两种作答方式之间的相关。",
    'Chapter ten. Rating scales.': "第10章。评定量表。",
    "Thurstone's scaling was slow.":
        "瑟斯顿的标度法很慢。<bookmark mark='a'/>1932年，伦西斯·利克特提出了一条捷径。不必让评判者工作好几个星期，只要请人们对许多陈述表示同意或不同意，再把回答加起来。<bookmark mark='b'/>总分几乎一样好，而且便宜得多，它成了调查的标准格式。<bookmark mark='c'/>每道题都是一个等级反应，就像第45部分那样：潜在态度上的阈值，而不是相等的步长。<bookmark mark='d'/>反应风格就住在这些类别里。有些人偏用极端，另一些人偏用中间，与他们的态度无关。",
    'How many points should a scale have?':
        "一个量表应该有几个点？<bookmark mark='a'/>Psyche把一个连续的态度切成几个可能性相等的类别，然后看它保留了多少。<bookmark mark='b'/>两个点保留大约零点八的相关。五个点保留大约零点九四，七个点大约零点九六。再多，几乎就没有更多了。<bookmark mark='c'/>真实的受访者还会带来他们自己的代价：点越多，花的力气越多，反应风格的空间也越大。<bookmark mark='d'/>五个或七个带标签的点，是通常的折中。",
    'Chapter eleven. Data quality online.': "第11章。在线数据的质量。",
    'Online panels made surveys cheap, and raised a question':
        "在线样本库让调查变得便宜，也带来一个问题：是谁在回答，他们在读题吗？<bookmark mark='a'/>Psyche造出两个各六道题的量表，它们的特质相关零点三，并让一些受访者对表格中的每道题都给出同一个答案。<bookmark mark='b'/>当直线作答者达到百分之三十时，α系数从零点七五升到零点九以上。量表看起来更可靠了。<bookmark mark='c'/>两个量表之间的相关从零点二四升到零点七五：一种由不读题制造出来的关系。<bookmark mark='d'/>粗心的回答并不是削弱结果的噪声。它们可以制造结果。",
    'So how are careless respondents found?':
        "那么怎样找出粗心的受访者？<bookmark mark='a'/>注意力检查，比如“本题请选择不同意”。它们能抓住一些人，惹恼另一些人，还可能让认真的人在之后的作答有所不同。<bookmark mark='b'/>反应时：快得不可能的页面是最便宜的标记。<bookmark mark='c'/>一致性：同一个问题问两次，或者一道反向题与它的孪生题回答得一样。<bookmark mark='d'/>机器人和欺诈：重复的回答、复制的文字、不可能的组合。如今语言模型能写出看似合理的回答，这就更难了。<bookmark mark='e'/>还有一条规则：在看结果之前就决定排除标准，就像第43部分那样，并报告排除了多少人。",
    'How many checks?':
        "要做几次检查？<bookmark mark='a'/>在一道五点题上，随机作答者有五分之一的运气通过一次检查。假设一个认真的人五十次中失误一次。<bookmark mark='b'/>一次检查能抓住五分之四的随机作答者。三次能抓住百分之九十九以上。<bookmark mark='c'/>但五次检查会排除将近十分之一的认真的人，而那些失误的人并不是随机的十分之一。<bookmark mark='d'/>两到三次检查，事先确定，是通常的答案。还要注意，一个恰好总是选中指定答案的直线作答者，每次都能通过。",
    'Chapter twelve. One number to rule them all?': "第12章。一个数字统治一切？",
    'In 2003 Fred Reichheld published the one number you need to grow.':
        "2003年，弗雷德·赖克哈尔德发表了“你增长所需的唯一数字”。<bookmark mark='a'/>一个问题：从零到十，你有多大可能向别人推荐我们？<bookmark mark='b'/>十一个回答被分成三组。用推荐者，即九分和十分的百分比，减去贬损者，即零到六分的百分比。<bookmark mark='c'/>其主张是：它比其他满意度指标更能预测一家公司的增长。<bookmark mark='d'/>2007年，蒂莫西·凯宁厄姆及其同事随时间检验了它，它并不比其他指标更好。账本的结论：失败。",
    "It's also a noisy number.":
        "它还是一个嘈杂的数字。<bookmark mark='a'/>来自两百名顾客时，这个分数的标准误大约是五个半百分点：误差范围大约是正负十一。<bookmark mark='b'/>所以月与月之间五个点的变化通常只是噪声。<bookmark mark='c'/>把十一个点合并成三组会损失一点信息。每款产品各有两百名顾客时，它在大约百分之九十的时候能挑出两款产品中较好的那一款，比简单的平均分稍差一点。<bookmark mark='d'/>一个合理的追踪指标，只要报告时附上它的误差。但不是增长的定律。",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Four new rows.':
        "四条新记录。第一条：一个比某个选项差、但不比另一个选项差的诱饵，会提高支配它的那个选项的份额。<bookmark mark='a'/>原始研究：休伯、佩恩和普托，1982年。<bookmark mark='b'/>记录：使用图片和真实的描述时，它很弱或不存在，在许多产品类别中都没有出现。<bookmark mark='c'/>用表格中的数字呈现时很稳健，当支配关系需要用眼睛看出来时就弱得多。<bookmark mark='d'/>有争议。",
    'The second: asking whether something should be forbidden or allowed':
        "第二条：问某件事应当被禁止还是应当被允许，会得到不同的回答。<bookmark mark='a'/>原始研究：拉格，1941年。<bookmark mark='b'/>记录：舒曼和普雷瑟的分组问卷实验，以及后来跨越多个主题的研究。<bookmark mark='c'/>措辞和顺序效应是调查研究中最可靠的发现之一。<bookmark mark='d'/>已重复。",
    'The third: some people agree with statements regardless of content.':
        "第三条：有些人无论内容如何都同意陈述。<bookmark mark='a'/>原始研究：克龙巴赫，1946年。<bookmark mark='b'/>记录：在平衡量表中有一个独立的风格因子，而且这种风格在一个人身上一年之内保持稳定。<bookmark mark='c'/>平衡的计分方向能在总分中抵消它。<bookmark mark='d'/>已重复。",
    'And the fourth: the net promoter score predicts growth better than other measures.':
        "第四条：净推荐值比其他指标更能预测增长。<bookmark mark='a'/>原始研究：赖克哈尔德，2003年。<bookmark mark='b'/>记录：随时间检验，它并不比其他指标更好。<bookmark mark='c'/>一个简单的追踪数字，而不是增长的最佳预测指标。<bookmark mark='d'/>失败。",
    'What the four have in common.':
        "这四条的共同点。<bookmark mark='a'/>有两条关乎测量工具：措辞和反应风格会改变回答，而且很可靠。<bookmark mark='b'/>一条关乎选择。在支配关系容易看出的地方，诱饵效应是真实的，在别处则很脆弱。<bookmark mark='c'/>一条是商业主张，提出时并没有检验它的数据。<bookmark mark='d'/>测量工具的效应重复得最好。它们关乎人们如何作答，而这正是调查最直接测量的东西。",
    'Chapter fourteen. In practice: pricing, polls and leaderboards.': "第14章。实践中：定价、民调与排行榜。",
    'Where these models run.':
        "这些模型在哪里运行。<bookmark mark='a'/>定价：在产品发布前做基于选择的联合分析，决定以什么价格提供哪些功能，之后再用销售数据核对。<bookmark mark='b'/>调查设计：在正式施测前做认知访谈，让人们边回答边说出想法，以发现被误读的词。<bookmark mark='c'/>民意调查：措辞和顺序固定并公开，用分组样本测量它们的效应。抽样和加权是《统计学，从零搭建》的第18部分。<bookmark mark='d'/>还有交通和卫生：关于人们如何出行、患者会选择哪种治疗的离散选择模型。",
    'One more place these models run.':
        "这些模型还在一个地方运行。<bookmark mark='a'/>国际象棋等级分、体育排名，以及用人们的投票为AI聊天机器人排名的竞技场，都是把布拉德利和特里的模型拟合到胜负上。<bookmark mark='b'/>所以它们面对着瑟斯顿的问题。一个维度够吗？比较是相互独立的吗？<bookmark mark='c'/>由谁来决定比较哪一对很重要。如果强者只和强者相遇，尺子就会被拉伸。<bookmark mark='d'/>投票者是一个样本。一个竞技场的等级分，是关于它的投票者的偏好的事实，而不是关于所有人的。<bookmark mark='e'/>要报告不确定性。比误差还小的差距，不是排名。",
    'Chapter fifteen. Frontier: causes, preferences and simulated respondents.': "第15章。前沿：因果、偏好与模拟的受访者。",
    'Three frontiers.':
        "三个前沿。<bookmark mark='a'/>用于因果的联合分析。政治学家在联合分析任务中随机化候选人或移民的属性，并把每个属性的平均效应解读为因果效应。<bookmark mark='b'/>学习偏好。推荐系统从点击中学习，语言模型则用一个关于人们在两个回答中更喜欢哪一个的布拉德利-特里模型，按人类偏好进行调整。瑟斯顿的方法就在它们里面。<bookmark mark='c'/>还有模拟的受访者：用某个人的口吻回答调查问题的语言模型。便宜、快速，效度未知。第60部分会回到它们。",
    'Open questions.':
        "开放的问题。<bookmark mark='a'/>调查中陈述的选择，什么时候能预测人们实际购买什么、投票给谁、做什么？<bookmark mark='b'/>一个比较模型能否解释全部三种情境效应，以及它们如何依赖于时间？<bookmark mark='c'/>一个偏好模型应当如何对待意见不同的人，而不是把他们平均掉？<bookmark mark='d'/>模拟的受访者什么时候，如果有的话，能代替真实的受访者？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>百分之九十三的人喜欢玉米胜过芜菁。在下方加一个诱饵后，Psyche的第一个选项在短暂权衡后保持一半的选择，长时间权衡后大约四分之三。方向相同计分的无关量表，仅仅由于默许倾向就相关大约零点二五。来自两百名顾客的净推荐值，误差范围大约是十一个点。<bookmark mark='b'/>选择有结构，菜单会弯曲它们，而回答带着测量工具的指纹。",
    'Part forty-six in twelve lines.':
        "用十二行总结第46部分。<bookmark mark='a'/>不一致的比较携带着信息。瑟斯顿把比例变成正态印象之间的距离。卢斯从一条公理推导出比率尺度，用一个向上爬的算法拟合。带冈贝尔噪声的随机效用给出逻辑模型。相似的选项打破公理。诱饵和折中显示菜单在弯曲选择，一个比较型的选择者能同时产生两者，时间越长越明显。联合分析从选择中为属性定价。回答一个调查问题意味着理解、提取、判断和报告。措辞、顺序、风格和满意即止都会留下痕迹。粗心的回答能制造相关。而一个数字，仍然是一个带误差的数字。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳，即数学无法应用于心灵，遇到了瑟斯顿定律、布拉德利-特里模型、逻辑模型和联合分析，都经过拟合和检验。绿色。<bookmark mark='b'/>第二个反驳，即心灵无法被实验，遇到了关于措辞和顺序的分组问卷实验，以及按设计变化的菜单。绿色。<bookmark mark='c'/>第三个，关于内省。比较对内省的要求比评分少，但调查回答是报告，带有已知的扭曲。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>随时间变化的人，以及一个人的内部，就在下一部分，第47部分。拟合和比较行为模型，包括选择模型，是第48部分。跨研究的证据分量是第50部分。作为参与者的语言模型是第60部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道应用瑟斯顿定律。一道检验卢斯公理。一道计算逻辑模型的份额。一道重做红色巴士。一道为相机定价。一道求净推荐值及其误差。最后一道带星号，请你设计一项能测量自身措辞和顺序效应的调查。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。肯尼思·特雷恩的书是离散选择的标准著作，可在网上免费阅读；图兰若、里普斯和拉辛斯基的书讲的是回答调查的心理学；舒曼和普雷瑟的实验至今仍是问题效应最好的示范。",
    'Three parts of the graduate toolkit done.':
        "研究生工具箱完成了三个部分。<bookmark mark='a'/>这一部分把偏好和回答变成了数字，并显示了这些数字在哪里弯曲。<bookmark mark='b'/>接下来是时间与个体。什么时候，关于人们的发现，才是关于一个人的发现？第47部分：随时间变化的人。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
