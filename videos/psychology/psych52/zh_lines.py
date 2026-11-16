"""Chinese narration for psych52: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第52部分：为心智而设计'

CHAPTERS = {
    'Hook': '三分之二秒',
    'Predict': '1. 在你身上：指点与点击，以及四个数字',
    'Mhp': '2. 模型人类处理器',
    'Klm': '3. GOMS与击键层次模型',
    'Pointing': '4. 被测量的指点',
    'Menus': '5. 界面中的菲茨与希克',
    'Foraging': '6. 信息觅食',
    'Gulfs': '7. 鸿沟、可供性与示能符号',
    'Usability': '8. 需要多少用户？',
    'Charts': '9. 看数据',
    'Access': '10. 作为心理物理学的无障碍设计',
    'Habit': '11. 被设计的习惯与注意',
    'Ai': '12. 与机器对话',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：预测一张结账表单',
    'Frontier': '15. 前沿：模拟用户',
    'Outro': '回顾、习题与前路',
}

ZH = {
    "<bookmark mark='a'/> In the late nineteen eighties, a telephone company's operators handle":
        "<bookmark mark='a'/>二十世纪八十年代末，一家电话公司的接线员每年要处理数百万通电话。<bookmark mark='b'/>一种新的工作站被推荐给他们：每通电话击键更少，屏幕更好，每通电话都能节省时间。<bookmark mark='c'/>在这样的通话量下，每通电话的每一秒每年都值很多钱。<bookmark mark='d'/>韦恩·格雷、邦妮·约翰和迈克尔·阿特伍德在实地试用之前，就在纸上为接线员的知觉、思考和击键建立了模型。<bookmark mark='e'/>他们的模型说，新工作站会更慢，每通电话慢大约三分之二秒。",
    "Why can fewer keystrokes be slower? <bookmark mark='a'/> Because a call is a schedule. Som":
        "为什么更少的击键反而可能更慢？<bookmark mark='a'/>因为一通电话是一个日程表。有些步骤并行发生，只有最长的那条链决定时间。这是那项分析的一个玩具版本。<bookmark mark='b'/>新设计节省下来的击键，是在顾客还在说话时完成的，不在关键路径上。<bookmark mark='c'/>它新增的步骤却落在路径上，在那里每十分之一秒都算数。<bookmark mark='d'/>实地试用与模型一致。新工作站更慢，公司没有买它。",
    'So this part asks: can you predict how long a person will take to use something, before it':
        "所以这一部分要问：在一样东西造出来之前，你能预测一个人使用它要花多长时间吗？<bookmark mark='a'/>用户的工程模型：处理器、操作符、指点和菜单。<bookmark mark='b'/>人们如何在界面中搜索、行动和理解。<bookmark mark='c'/>用用户测试，以及阅读图表。<bookmark mark='d'/>还有无障碍、习惯，以及会回话的机器。",
    "This is Part 52 of Psychology, Built: designing for minds. <bookmark mark='a'/> We'll buil":
        "这是《心理学，从零搭建》的第52部分：为心智而设计。<bookmark mark='a'/>我们将搭建模型人类处理器和击键层次模型，通过把操作符相加来预测时间。我们将把指点测量为吞吐量，并在通道中引导移动。我们将设计菜单，跟随觅食者，并跨越诺曼的两道鸿沟。我们将追问一次测试需要多少用户，以及为什么那个著名的答案太小了。我们将把读图和看清对比度当作心理物理学。我们还将审视习惯、黑暗模式，以及会回话的机器。",
    'Chapter one. On you: point and click, and four numbers.':
        '第1章。在你身上：指点与点击，以及四个数字。',
    "First, your own hand. <bookmark mark='a'/> On the course site, targets of four sizes appea":
        "首先，用你自己的手。<bookmark mark='a'/>在课程网站上，四种大小的目标出现在四种距离上，你要尽快点击每一个。<bookmark mark='b'/>页面会拟合出你自己的直线：时间对难度指数（以比特计）。<bookmark mark='c'/>它还会根据你的点击实际落在哪里，给出你以每秒比特计的吞吐量。<bookmark mark='d'/>没有任何东西被存储或发送。",
    "Now four numbers. <bookmark mark='a'/> One: to delete a word, you can use a keyboard short":
        "现在是四个数字。<bookmark mark='a'/>第一：要删除一个单词，你可以用键盘快捷键，也可以用鼠标和菜单。菜单的路线慢多少？<bookmark mark='b'/>第二：一次有五名用户的可用性测试。它能找出界面中多大比例的问题？<bookmark mark='c'/>第三：读条形的长度或饼图扇区的角度。读角度的典型误差大多少？<bookmark mark='d'/>第四：养成一个新的日常习惯需要多少天？在这里暂停，把它们写下来。",
    'Chapter two. The Model Human Processor.':
        '第2章。模型人类处理器。',
    'In 1983 Stuart Card, Thomas Moran and Allen Newell drew a person as an engineer would. <bo':
        "1983年，斯图尔特·卡德、托马斯·莫兰和艾伦·纽厄尔像工程师那样画出了一个人。<bookmark mark='a'/>三个处理器，知觉的、认知的和运动的，各有一个周期时间，还有具备容量和衰减速率的记忆。<bookmark mark='b'/>每一个数字都来自第三幕和第五幕的实验，并且都给出了典型值、快值和慢值。<bookmark mark='c'/>他们的主张不是心智就是这样构造的，而是这已经准确到可以用来做设计。",
    "The model predicts by adding cycles. <bookmark mark='a'/> A simple reaction is perceive, d":
        "这个模型通过把周期相加来做预测。<bookmark mark='a'/>一次简单反应是知觉、决定、动作：两百四十毫秒，范围从大约一百到将近五百。<bookmark mark='b'/>问两个形状是否相同，就多一个认知周期：三百一十。<bookmark mark='c'/>问大写A和小写a是否是同一个字母，就多两个：三百八十。这就是第1部分的波斯纳和唐德斯，变成了算术。<bookmark mark='d'/>范围很宽。这个模型预测的是顺序和量级，而不是某一个人的那一毫秒。",
    'Chapter three. GOMS and the keystroke-level model.':
        '第3章。GOMS与击键层次模型。',
    "Card, Moran and Newell's next step was GOMS. <bookmark mark='a'/> Goals: what the user wan":
        "卡德、莫兰和纽厄尔的下一步是GOMS。<bookmark mark='a'/>目标：用户想要什么，比如删除一个单词。<bookmark mark='b'/>操作符：基本的动作，一次击键、一次指点、一次注视、一次思考的瞬间。<bookmark mark='c'/>方法：实现一个目标的操作符序列，比如快捷键或菜单。<bookmark mark='d'/>还有选择规则：用户如何挑选方法。如果我的手在键盘上，就用快捷键。",
    "The keystroke-level model is GOMS at its simplest. <bookmark mark='a'/> K, a keystroke: ab":
        "击键层次模型是GOMS最简单的形式。<bookmark mark='a'/>K，一次击键：对普通打字者约为四分之一秒。<bookmark mark='b'/>P，用鼠标指点：约一秒，是菲茨定律的平均。<bookmark mark='c'/>B，按下或松开按钮；一次点击是两个B。<bookmark mark='d'/>H，手在键盘和鼠标之间归位：十分之四秒。<bookmark mark='e'/>还有M，心理准备：一点三五秒，按规则放在每一个新的动作组块之前。<bookmark mark='f'/>一项任务的时间就是它的操作符之和，再加上系统的响应时间。",
    "Here are three ways to delete a word. <bookmark mark='a'/> Write each method as operators,":
        "这是删除一个单词的三种方式。<bookmark mark='a'/>把每种方法写成操作符，放上心理操作符，然后相加。<bookmark mark='b'/>键盘快捷键不到三秒。<bookmark mark='c'/>菜单路线要八秒多，是三倍，大部分花在指点和思考上。<bookmark mark='d'/>在卡德、莫兰和纽厄尔的测试中，这样的预测与用户的时间相差约百分之二十以内。但这个模型预测的是熟练、无差错的操作，对学习和差错一无所知。",
    "Skilled people don't do one thing at a time. <bookmark mark='a'/> The keystroke-level mode":
        "熟练的人不会一次只做一件事。<bookmark mark='a'/>击键层次模型把操作符一个接一个地相加，但熟练的人会让它们重叠。<bookmark mark='b'/>邦妮·约翰的CPM-GOMS把每个操作符画在它所用的资源上，眼睛、手或认知，并找出关键路径，也就是决定时间的那条链。<bookmark mark='c'/>在“欧内斯廷项目”中，它在新工作站接过任何一通电话之前，就预测出了每类电话的时间，以及新工作站的损失。<bookmark mark='d'/>对设计的启示：缩短一项任务意味着缩短它的关键路径，而不是数它的击键。",
    'Chapter four. Pointing, measured.':
        '第4章。被测量的指点。',
    "Part 51 met Fitts's law. Here it's measured the way designers measure it. <bookmark mark='":
        "第51部分遇到了菲茨定律。这里是设计师测量它的方式。<bookmark mark='a'/>Psyche指向距离从六十四到五百一十二像素、宽度从八到六十四像素的目标：十六种条件，每种二十四次动作。<bookmark mark='b'/>难度指数，即距离除以宽度再加一的对数，把全部十六种条件压到了一条直线上。<bookmark mark='c'/>大约十分之二秒，加上每比特十分之二秒，相关接近一。<bookmark mark='d'/>距离和大小精确地相互抵换。两者都加倍，什么都不变。",
    "One complication: people trade speed for accuracy. <bookmark mark='a'/> One person aims ca":
        "一个复杂之处：人会用速度换准确。<bookmark mark='a'/>一个人小心瞄准，另一个人乱点一气。<bookmark mark='b'/>所以要测量他们实际使用的宽度：他们落点离散程度的四点一三倍，这覆盖了正态分布的百分之九十六。<bookmark mark='c'/>吞吐量是有效难度指数除以动作时间，单位是每秒比特。这里约为三点八，在报告过的鼠标的范围之内。<bookmark mark='d'/>国际标准用它来比较设备：鼠标、触控板、操纵杆、眼动仪。<bookmark mark='e'/>每种设备、每个人一个数字，可以在研究之间比较。这就是为什么菲茨定律在七十年后仍在使用。",
    "Some movements aren't to a target but along a path. <bookmark mark='a'/> Johnny Accot and ":
        "有些动作不是指向一个目标，而是沿着一条路径。<bookmark mark='a'/>约翰尼·阿科特和翟树敏在1997年发现，在长度为A、宽度为W的通道中引导移动所需的时间，是一个常数加上b乘以A除以W。<bookmark mark='b'/>不是对数，而是比值，因为路径上的每一步都必须待在墙壁之内。<bookmark mark='c'/>级联菜单就是通道。一条通往子菜单的又窄又长的路径既慢又容易出错。<bookmark mark='d'/>解决办法是更宽的路径、子菜单关闭前一段宽容的延迟，或者干脆不用级联。",
    'Chapter five. Fitts and Hick in the interface.':
        '第5章。界面中的菲茨与希克。',
    "Fitts's law tells you where to put things. <bookmark mark='a'/> A target at the edge of th":
        "菲茨定律告诉你东西该放在哪里。<bookmark mark='a'/>屏幕边缘的目标不可能冲过头。光标会停在那里，所以它的有效宽度极大，点击起来很快。<bookmark mark='b'/>角落同时是两条边，是屏幕上最快的地方。<bookmark mark='c'/>饼状菜单把每一项都放在光标周围，距离同样短。<bookmark mark='d'/>而在触摸屏上，指尖很宽。无论定律关于距离怎么说，目标都需要有好几毫米宽。",
    "How many items should a menu hold? <bookmark mark='a'/> Take sixty-four commands. They cou":
        "一个菜单应该放多少项？<bookmark mark='a'/>取六十四条命令。它们可以是六层、每层两项，三层、每层四项，两层、每层八项，或者一个六十四项的菜单。<bookmark mark='b'/>对熟练用户，每一层花费一次希克选择和一次指点。宽的胜出，一个六十四项的菜单最快。<bookmark mark='c'/>但对一个不熟悉的菜单，用户会一项一项地扫视。选择时间线性增长，每层大约八项最好。<bookmark mark='d'/>所以希克定律只适用于用户知道东西在哪里的时候。否则就是第18部分的视觉搜索。",
    'Chapter six. Information foraging.':
        '第6章。信息觅食。',
    'In 1999 Peter Pirolli and Stuart Card argued that people looking for information behave li':
        "1999年，彼得·皮罗利和斯图尔特·卡德认为，寻找信息的人行为就像觅食的动物。<bookmark mark='a'/>这是一个来自行为生态学的想法，被用到了阅读上。<bookmark mark='b'/>一个页面就是一块食物斑块。它有用的事实起初来得很快，然后越来越慢。<bookmark mark='c'/>埃里克·查诺夫的边际价值定理说：当页面的收获速率降到整体最佳速率时就离开。从旅途起点画一条恰好与曲线相切的直线。旅途二十秒时，大约半分钟后离开。<bookmark mark='d'/>旅途越便宜，停留越短：下一个页面只要两秒时，在一个页面上停十秒；要八十秒时，停五十秒。快速的搜索引擎让读者走马观花。",
    "Foragers follow scent. <bookmark mark='a'/> Information scent is what a link tells you abo":
        "觅食者追随气味。<bookmark mark='a'/>信息气味是一个链接告诉你它背后有什么的那些东西：它的文字、它的图片、它在页面上的位置。<bookmark mark='b'/>用户会选择文字与自己目标最匹配的链接，当气味消散时就离开一个网站。<bookmark mark='c'/>所以要用用户会用的词来标注链接，而不是用机构自己给各部门起的名字。<bookmark mark='d'/>并用首次点击测试来检验。如果第一次点击是对的，任务通常就会成功。",
    'Chapter seven. Gulfs, affordances and signifiers.':
        '第7章。鸿沟、可供性与示能符号。',
    'Donald Norman described what goes wrong between a person and a device as two gulfs. <bookm':
        "唐纳德·诺曼把人与设备之间出问题的地方描述为两道鸿沟。<bookmark mark='a'/>执行的鸿沟是我想要的东西与系统提供的动作之间的距离。我该怎么做？<bookmark mark='b'/>评估的鸿沟是系统显示的东西与我需要知道的东西之间的距离。成功了吗？<bookmark mark='c'/>第51部分中三里岛的那盏灯就是一道评估的鸿沟。藏在三层菜单深处的命令是一道执行的鸿沟。<bookmark mark='d'/>设计要把两者都缩窄：可见的动作、即时的反馈，以及两者之间清楚的对应关系。",
    "Norman borrowed a word from James Gibson. <bookmark mark='a'/> An affordance is what an ob":
        "诺曼从詹姆斯·吉布森那里借来一个词。<bookmark mark='a'/>可供性是一个物体允许人做的事。一块平板可供推，一个把手可供拉。<bookmark mark='b'/>示能符号是告诉人可供性就在那里的东西：那块平板、一条下划线、一个凸起的按钮。<bookmark mark='c'/>一扇装着把手却必须推开的门，它的示能符号在撒谎。人们把它叫作“诺曼门”。<bookmark mark='d'/>屏幕处处可供触碰，所以每个动作都需要一个示能符号，而去掉了示能符号的扁平化设计会把动作藏起来。",
    'Chapter eight. How many users?':
        '第8章。需要多少用户？',
    "How many users does a usability test need? <bookmark mark='a'/> In 1993 Jakob Nielsen and ":
        "一次可用性测试需要多少用户？<bookmark mark='a'/>1993年，雅各布·尼尔森和托马斯·兰道尔写出了那条曲线。如果每个用户以概率p发现每个问题，n个用户就能发现其中一减去一减p的n次方。<bookmark mark='b'/>用他们约三分之一的平均p，五个用户能发现百分之八十四。于是就有了那条建议：用五个用户测试。<bookmark mark='c'/>但问题各不相同。有些几乎人人都会碰到，有些只有二十个用户中的一个才会碰到。在同样的平均p下，五个用户只能发现大约百分之六十，二十个用户仍然会漏掉将近五分之一。<bookmark mark='d'/>后来贾里德·斯普尔和威尔·施罗德的研究，以及劳拉·福克纳的研究，都发现在真实测试中五个用户会漏掉许多问题。有用的那部分建议依然成立：用小规模测试反复迭代。但不要宣称覆盖率。",
    "So what does a usability team actually use? <bookmark mark='a'/> Think-aloud tests: a user":
        "那么可用性团队实际上用什么？<bookmark mark='a'/>出声思考测试：用户做真实的任务，并说出自己在想什么。它们发现问题，而不是比率。<bookmark mark='b'/>像系统可用性量表这样的问卷：十个题目，得分从零到一百，在许多研究中平均约为六十八。<bookmark mark='c'/>任务指标：设定任务上的成功、时间和差错，报告时要带区间，而不只是平均值。<bookmark mark='d'/>而当问题是设计B是否比A更好时，就做实验：随机分配用户并测量。",
    'Chapter nine. Seeing data.':
        '第9章。看数据。',
    "Which chart lets a reader judge a number best? <bookmark mark='a'/> In 1984 William Clevel":
        "哪种图表最能让读者判断一个数值？<bookmark mark='a'/>1984年，威廉·克利夫兰和罗伯特·麦吉尔请人判断一个标记是另一个标记的百分之几，标记用不同的方式画出。<bookmark mark='b'/>沿共同刻度的位置判断得最好，然后是长度，然后是角度，再然后是面积、体积和明暗。<bookmark mark='c'/>杰弗里·希尔和迈克尔·博斯托克在2010年用众包工作者在网上重复了这项研究，发现了同样的顺序。<bookmark mark='d'/>在Psyche的版本中，长度的典型误差约为四个百分点，角度约为七个，几乎是两倍。",
    "Why does area mislead? <bookmark mark='a'/> Part 11's power law: perceived size grows as p":
        "为什么面积会误导人？<bookmark mark='a'/>第11部分的幂律：知觉到的大小随物理大小的某个指数次方增长。<bookmark mark='b'/>对长度，指数约为一。对面积约为零点七，对体积约为零点六。面积加倍，看起来只大了大约一点五倍。<bookmark mark='c'/>所以按数据缩放符号边长的图表会让面积变为四倍，夸大变化；按数据缩放面积的图表又会低估它。<bookmark mark='d'/>用位置和长度表示数量，用面积和颜色表示粗略的印象。",
    "Part 18 tells chart designers what pops out. <bookmark mark='a'/> A single feature, a red ":
        "第18部分告诉图表设计师什么会跳出来。<bookmark mark='a'/>单一特征，比如灰色标记中的一个红色标记，是并行找到的。<bookmark mark='b'/>一个特征组合，比如红色圆圈和灰色方块中的红色方块，需要串行搜索，而且很慢。<bookmark mark='c'/>所以用一个特征突出一样东西。什么都突出，就什么都没突出。<bookmark mark='d'/>还要使用知觉上均匀的色阶，明度的步长相等。彩虹色阶会凭空造出数据中并不存在的边界。",
    'Chapter ten. Accessibility as psychophysics.':
        '第10章。作为心理物理学的无障碍设计。',
    "Accessibility is psychophysics with a standard attached. <bookmark mark='a'/> The web's co":
        "无障碍设计就是附带了一套标准的心理物理学。<bookmark mark='a'/>网页的对比度是根据每种颜色的相对亮度计算的，范围从一到二十一。<bookmark mark='b'/>普通文字需要四点五比一。白底上的这种中灰色刚好通过。<bookmark mark='c'/>这个阈值来自第13部分。对比敏感度随年龄和低视力而下降，所以留出的余量是为他们准备的。<bookmark mark='d'/>绿底上的红色几乎没有亮度对比，大约一点三，对许多色盲读者来说则完全没有。",
    "Colour vision differs too. <bookmark mark='a'/> About one man in twelve, and one woman in ":
        "色觉也各不相同。<bookmark mark='a'/>在北欧血统的人中，大约每十二个男性中有一个、每两百个女性中有一个有红绿色觉缺陷，来源于第13部分的视锥细胞。<bookmark mark='b'/>一张只用红色和绿色区分线条的图表，对他们来说什么也没有区分。<bookmark mark='c'/>解决办法是冗余编码：颜色加上形状、位置、标签或虚线。<bookmark mark='d'/>而在明度和色相上都有差异的调色板，既能经受色觉缺陷，也能经受灰度打印。",
    "Motor and cognitive tolerances follow the same logic. <bookmark mark='a'/> Acuity falls wi":
        "运动和认知上的容差遵循同样的逻辑。<bookmark mark='a'/>视敏度随年龄下降，所以文字应当可以放大，版面应当可以重排。<bookmark mark='b'/>对于一只有震颤的手，菲茨定律意味着更大的目标和更大的间距。<bookmark mark='c'/>第31部分中晚年处理速度变慢，意味着可调节的时间限制，或者干脆不设时限。<bookmark mark='d'/>还有其他途径，只用键盘操作、屏幕阅读器和字幕，把同样的任务交给另一种感官。在人群边缘也能用的设计，通常对所有人都更好用。",
    'Chapter eleven. Habit and attention by design.':
        '第11章。被设计的习惯与注意。',
    "How long does a habit take? <bookmark mark='a'/> The popular answer, twenty-one days, trac":
        "养成一个习惯需要多久？<bookmark mark='a'/>流行的答案是二十一天，它可以追溯到1960年的一本自助书，以及关于病人术后适应的一句话。<bookmark mark='b'/>2010年，菲莉帕·拉利及同事让九十六个人每天重复一种自己选择的行为，并评定它感觉有多自动化，持续十二周。<bookmark mark='c'/>自动化程度上升后趋于平稳。它达到平台期百分之九十五的中位时间是六十六天，范围从十八天到两百五十四天。<bookmark mark='d'/>在围绕这个中位数抽取的九十六个Psyche的人中，大约二十个人里只有一个能在二十一天内达到。而且在那项研究中，漏掉一天并不会让曲线重新开始。",
    "Part 16's schedules are in your pocket. <bookmark mark='a'/> A variable-ratio schedule, a ":
        "第16部分的强化程式就在你的口袋里。<bookmark mark='a'/>变比率程式，即在不可预测的反应次数之后给予奖励，会产生高而稳定、难以消退的反应。<bookmark mark='b'/>下拉刷新、有时会出现好东西的信息流，以及随机时刻推送的通知，都是同一种程式。<bookmark mark='c'/>第17部分的预测误差解释了原因：不确定的奖励让信号保持活跃。<bookmark mark='d'/>这是否等于成瘾尚有争议。它是为了抓住注意力而设计的，这一点没有争议。",
    "The darker end has a name. <bookmark mark='a'/> In 2019 Arunesh Mathur and colleagues craw":
        "更黑暗的那一端有一个名字。<bookmark mark='a'/>2019年，阿鲁内什·马图尔及同事抓取了大约一万一千个购物网站，发现其中十分之一以上存在黑暗模式。<bookmark mark='b'/>虚假的紧迫感和稀缺感、隐藏的费用、预先勾选的选项、羞辱式确认，以及被故意弄得很难的取消。<bookmark mark='c'/>其中的心理学正是这个系列自己讲过的：第26部分的默认选项和损失厌恶，以及第34部分的社会认同，被用来对付用户。<bookmark mark='d'/>监管机构现在把其中几种认定为不公平，设计师可以逐一审查自己的流程。",
    'Chapter twelve. Talking to machines.':
        '第12章。与机器对话。',
    "What do people expect from an interface that talks? <bookmark mark='a'/> In 1996 Byron Ree":
        "人们对一个会说话的界面有什么期待？<bookmark mark='a'/>1996年，拜伦·里夫斯和克利福德·纳斯表明，人们会对计算机运用社交规则，礼貌、恭维和队友关系，而并不相信计算机是一个人。<bookmark mark='b'/>流畅、听起来像人的回答会抬高人们对它在各方面能力的预期。这是第35部分的读心，被语言开启了。<bookmark mark='c'/>而评估的鸿沟变宽了，因为一个错误的答案看起来和正确的答案一模一样。<bookmark mark='d'/>所以界面必须显示系统能做什么、不能做什么，以及它有多确定。这就是第51部分的校准过的信任。",
    "Conversation itself can be designed. <bookmark mark='a'/> Repair: conversations go wrong a":
        "对话本身也可以被设计。<bookmark mark='a'/>修复：对话总是出错，人们用一句快速的“你是说……？”来修补。好的系统会询问，并接受纠正。<bookmark mark='b'/>话轮转换：第23部分中话轮之间的间隔大约是两百毫秒，所以慢吞吞的回答感觉像犹豫。<bookmark mark='c'/>拟人化：一个名字和一种个性会增加使用和信任，无论这种信任是否应得。<bookmark mark='d'/>还有测量：任务成功率和差错的代价，而不是对话感觉有多愉快。第60部分会回到心智与机器。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    "Four new rows. The first: adding standard operator times predicts skilled users' task time":
        "新增四行。第一行：把标准的操作符时间相加，能把熟练用户的任务时间预测到约百分之二十以内。<bookmark mark='a'/>原始研究：卡德、莫兰和纽厄尔，1980年，超过一千二百项预测。<bookmark mark='b'/>后续记录：奥尔森夫妇以及约翰和基拉斯的综述，包括像“欧内斯廷项目”那样用于真实设计决策的模型。<bookmark mark='c'/>它只预测熟练、无差错的操作，别的不管；在这个范围内它站得住。<bookmark mark='d'/>已重复。",
    'The second: people judge quantities most accurately from position, then length, then angle':
        "第二行：人们从位置判断数量最准确，然后是长度，然后是角度，然后是面积。<bookmark mark='a'/>原始研究：克利夫兰和麦吉尔，1984年。<bookmark mark='b'/>后续记录：希尔和博斯托克2010年的众包重复研究，得到同样的顺序。<bookmark mark='c'/>这个排序是关于判断数值的；要发现一种模式或趋势，其他编码也可以做得很好。<bookmark mark='d'/>已重复。",
    "The third: testing with five users finds about eighty-five percent of an interface's usabi":
        "第三行：用五个用户测试能找出界面中约百分之八十五的可用性问题。<bookmark mark='a'/>原始研究：尼尔森和兰道尔，1993年。<bookmark mark='b'/>后续记录：斯普尔和施罗德的网站研究，以及福克纳从六十个用户中抽取的五人样本，发现的问题少得多，而且差异很大。<bookmark mark='c'/>公式是对的；它关于每个问题都同样容易被发现的假设是错的。<bookmark mark='d'/>有争议。",
    "And the fourth: a new habit forms in about twenty-one days. <bookmark mark='a'/> The origi":
        "第四行：一个新习惯大约二十一天就能养成。<bookmark mark='a'/>原始研究：马尔茨1960年自助书中的一句话。<bookmark mark='b'/>后续记录：拉利及同事为期十二周的研究，中位数六十六天，范围从十八天到两百五十四天。<bookmark mark='c'/>这个数字从来就不是一项发现；测得的时间更长，而且差异很大。<bookmark mark='d'/>失败。",
    "What the four have in common. <bookmark mark='a'/> Two are quantitative models of percepti":
        "这四行的共同点。<bookmark mark='a'/>有两行是知觉与动作的定量模型，经过用户检验，两者都重复成功了。<bookmark mark='b'/>另外两行是传播得比证据还快的经验法则。一行有争议，一行从来就不是一项发现。<bookmark mark='c'/>一条设计规则的好坏，取决于它下面的测量。<bookmark mark='d'/>所以这一部分问题的答案是：在心理学是定量的、并且经过检验的地方，用心理学做工程就行得通。",
    'Chapter fourteen. In practice: a checkout form, predicted.':
        '第14章。实践中：预测一张结账表单。',
    "Where is this a job? <bookmark mark='a'/> In UX research: interviews, usability tests and ":
        "这在哪里是一份工作？<bookmark mark='a'/>在用户体验研究中：访谈、可用性测试和日记研究，关注人们想做什么、在哪里失败。<bookmark mark='b'/>在定量用户体验研究中：大规模的调查、日志和实验，也就是第2到4部分、第46和47部分的日常运用。<bookmark mark='c'/>在设计系统中：共享的组件，其尺寸、对比度和状态都经过测试，让每个团队都继承下来。<bookmark mark='d'/>还有在无障碍设计和数据可视化中，要满足标准，要让读者正确判断图表。",
    "Here's a worked analysis. <bookmark mark='a'/> A checkout form with seven fields: name, em":
        "这是一个完整的分析示例。<bookmark mark='a'/>一张有七个字段的结账表单：姓名、电子邮件、卡号、有效期、安全码、地址，以及一个按钮。<bookmark mark='b'/>设计A让买家点击进入每一个字段。那是九次指点、十四次手部移动和十五个心理操作符：大约一分钟。<bookmark mark='c'/>设计B让他们用Tab键在字段之间切换，按回车提交。一次指点、一次手部移动，大约三十七秒：每个买家节省二十三秒。<bookmark mark='d'/>对打字快的人，节省得更多，因为占主导的是手部移动和思考，而不是打字。<bookmark mark='e'/>这项分析只要一个小时，在任何用户看到任何一张表单之前就能完成。然后用用户测试胜出的设计，找出模型看不到的差错。",
    "What does the model leave out? <bookmark mark='a'/> Errors: a mistyped card number costs f":
        "这个模型漏掉了什么？<bookmark mark='a'/>差错：一个输错的卡号代价远高于任何操作符。<bookmark mark='b'/>学习：第一次购买的人不是熟练用户，模型的心理操作符低估了他们的思考。<bookmark mark='c'/>信任与动机：买家究竟会不会完成。<bookmark mark='d'/>所以模型能很快地为专家给设计排序，而真实用户的测试能发现它发现不了的东西。",
    'Chapter fifteen. Frontier: simulated users.':
        '第15章。前沿：模拟用户。',
    "Can a model of a person test a design for us? <bookmark mark='a'/> Cognitive architectures":
        "一个人的模型能替我们测试设计吗？<bookmark mark='a'/>认知架构现在能看屏幕、移动一只模拟的手、犯错误，可以在任何人造出设计之前就在它上面运行。<bookmark mark='b'/>受人的局限约束的强化学习智能体，一种被称为计算理性的方法，被用来优化布局和键盘。<bookmark mark='c'/>语言模型被提出作为模拟用户，回答调查或试用界面。它们很便宜，保真度未知，这是第46部分的警告。<bookmark mark='d'/>而评估人工智能界面意味着测量人与助手在一起的表现：时间、差错和过度依赖，而不是模型的基准测试得分。",
    "And the open problems. <bookmark mark='a'/> Fidelity: how close must a simulated user be b":
        "还有开放的问题。<bookmark mark='a'/>保真度：一个模拟用户要接近到什么程度，它对设计的判决才能被信任？<bookmark mark='b'/>差错：时间的模型很好，差错和学习的模型要弱得多。<bookmark mark='c'/>长期使用：几个月里的习惯、疲劳和信任，而不是一次使用。<bookmark mark='d'/>还有谁的用户：由一个人群构建的模拟用户，可能只为那个人群做设计。",
    "First, your four numbers. <bookmark mark='a'/> The menu route to delete a word takes about":
        "首先，你的四个数字。<bookmark mark='a'/>用菜单删除一个单词所需的时间大约是快捷键的三倍。如果每个问题都同样容易被发现，五个用户能找出约百分之八十四的问题；如果问题各不相同，约百分之六十。角度被误判的程度几乎是长度的两倍。而一个新习惯的中位时间约为六十六天，范围从十八天到两百五十四天。<bookmark mark='b'/>在心理学是定量的地方，设计可以在造出来之前就被预测。",
    "Part fifty-two in twelve lines. <bookmark mark='a'/> The Model Human Processor: three proc":
        "第五十二部分，十二行。<bookmark mark='a'/>模型人类处理器：三个有周期时间的处理器。击键层次模型：把操作符相加。当操作符重叠时，缩短关键路径。根据点击落在哪里测量吞吐量。引导移动是比值，而不是对数。希克定律需要熟练的用户。觅食者按照边际价值定理离开页面。有两道鸿沟，可供性需要示能符号。五个用户找到的比承诺的少。位置胜过长度，长度胜过角度，角度胜过面积。对比度和颜色是心理物理学。而习惯需要数月才能养成，黑暗模式则把我们的偏差用来对付我们。",
    "Where this comes back. <bookmark mark='a'/> Selection, training and the design of work are":
        "这些内容会在哪里再次出现。<bookmark mark='a'/>选拔、培训和工作设计是第53部分。课堂中的学习与练习是第54部分。大规模的默认选项和助推是第55部分。心智与机器会在第60部分再次出现。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One adds k":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道把击键层次的操作符相加。一道把菲茨定律用于一个按钮。一道计算吞吐量。一道推演问题发现曲线。一道检验边际价值定理。一道计算对比度。最后带星号的一道，请你用三种方法规划对一个重新设计的页面的测试。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Card, Moran and N':
        '这一部分所依据的书籍和论文列在这里，也列在README中。卡德、莫兰和纽厄尔的书奠定了工程模型；诺曼的书是关于日常设计的经典；韦尔的书是关于可视化中知觉问题的最佳著作。',
    "Two parts of Act Twelve are done. <bookmark mark='a'/> This one designed the interface aro":
        "第十二幕的两部分已经完成。<bookmark mark='a'/>这一部分围绕人来设计界面。<bookmark mark='b'/>下一部分转向人本身：雇用谁、如何培训他们，以及什么让工作顺利。一项测试能预测谁会把一份工作做好吗？第53部分：工作中的人。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
