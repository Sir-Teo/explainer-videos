"""Chinese narration for psych51: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第51部分：人因学'

CHAPTERS = {
    'Hook': '两根手感相同的操纵杆',
    'Predict': '1. 在你身上：盯着时钟，以及四个数字',
    'Design': '2. 设计进去的差错',
    'Errors': '3. 失误、遗漏与错误',
    'Tmi': '4. 一盏讲错了故事的灯',
    'Workload': '5. 工作中的注意',
    'Vigilance': '6. 值守',
    'Rare': '7. 罕见的目标',
    'Awareness': '8. 态势感知',
    'Automation': '9. 自动化的讽刺',
    'Trust': '10. 信任与警报',
    'Systems': '11. 系统、检查单与机组',
    'Fatigue': '12. 作为一种可测量风险的疲劳',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：设计一次接管请求',
    'Frontier': '15. 前沿：监督会学习的机器',
    'Outro': '回顾、习题与前路',
}

ZH = {
    "In the 1940s, pilots of some bomber types kept doing something strange. <bookmark mark='a'":
        "在二十世纪四十年代，某些型号轰炸机的飞行员总是做一件奇怪的事。<bookmark mark='a'/>着陆之后，他们本想收起襟翼，却收起了起落架。<bookmark mark='b'/>两根操纵杆并排放着，形状相同，手感也相同。<bookmark mark='c'/>1947年，保罗·菲茨和理查德·琼斯收集了四百六十份飞行员差错报告，发现同样几种差错一再出现：操纵器件被混淆，仪表被读错。<bookmark mark='d'/>这些差错可以从驾驶舱预测出来，而不是从飞行员身上。<bookmark mark='e'/>人因学从这里开始。差错是设计进去的，也可以被设计出去。",
    "The fix was almost embarrassingly simple. <bookmark mark='a'/> Alphonse Chapanis made each":
        "解决办法简单得几乎令人尴尬。<bookmark mark='a'/>阿方斯·查帕尼斯把每根操纵杆的手柄做成它所控制之物的形状：控制机轮的是一个小轮子，控制襟翼的是一片襟翼。<bookmark mark='b'/>摸到轮子的手不用看就知道自己要动的是机轮。<bookmark mark='c'/>形状编码至今仍是驾驶舱的规则，与位置、颜色和运动方向的编码并用。",
    'So this part asks: when a person makes a fatal error with a machine, whose error is it? <b':
        "所以这一部分要问：当一个人用机器犯下致命的差错时，那是谁的差错？<bookmark mark='a'/>设计进去的差错，以及差错的种类。<bookmark mark='b'/>工作中的注意：负荷、警觉、罕见目标和态势感知。<bookmark mark='c'/>自动化、信任与警报。<bookmark mark='d'/>以及系统、检查单、机组和疲劳。",
    'This is Part 51 of Psychology, Built: human factors, and the first part of Act Twelve, psy':
        "这是《心理学，从零搭建》的第51部分：人因学，也是第十二幕“工作中的心理学”的第一部分。<bookmark mark='a'/>我们将看到兼容性和编码如何防止差错，并拟合菲茨定律和希克定律。我们将把差错分为失误、遗漏和错误。我们将测量工作负荷，看着警觉下降，并漏掉罕见的目标。我们将追问态势感知是什么，以及为什么可靠的自动化反而让接管更难。我们将把警报看作工程师选定的一个判断标准，把信任看作应当与可靠性相符的东西。我们还将认识瑞士奶酪模型、检查单、机组，以及作为一种可测量风险的疲劳。",
    'Chapter one. On you: watch the clock, and four numbers.':
        '第1章。在你身上：盯着时钟，以及四个数字。',
    "First, a watch of your own. <bookmark mark='a'/> In 1948 Norman Mackworth built a clock wh":
        "首先，来一次你自己的值守。<bookmark mark='a'/>1948年，诺曼·麦克沃斯造了一个时钟，它的指针每秒跳一格。<bookmark mark='b'/>偶尔它会一次跳两格。那就是信号，值守者要按一个键。<bookmark mark='c'/>雷达操作员盯着它看两个小时，他们的检出率在头半个小时内就下降了。<bookmark mark='d'/>在课程网站上，你可以自己盯九十秒。你的记录只保存在你的浏览器里。",
    "Now four numbers. <bookmark mark='a'/> One: in a two-hour watch for a rare signal, about s":
        "现在是四个数字。<bookmark mark='a'/>第一：在为罕见信号进行的两小时值守中，头半个小时大约能捕捉到百分之七十三的信号。最后半个小时是多少？<bookmark mark='b'/>第二：目标出现在一百个行李中的一个里，而不是两个中的一个。漏报率会怎样变化？<bookmark mark='c'/>第三：自动化每一万次需求失败一次，相对于每十次失败一次。人工接管中有多大比例能在七秒内完成？<bookmark mark='d'/>第四：清醒多少小时，对表现的损害相当于血液酒精浓度百分之零点零五？在这里暂停，把它们写下来。",
    'Chapter two. Error designed in.':
        '第2章。设计进去的差错。',
    "Some designs invite the wrong action. <bookmark mark='a'/> Spatial compatibility: the cont":
        "有些设计会诱发错误的动作。<bookmark mark='a'/>空间兼容性：左边灶头的开关放在左边。查帕尼斯的炉灶实验发现，只要布局打破了这种对应关系，就会出错。<bookmark mark='b'/>运动定型：向右转是增加，顺时针是关水龙头。这些是设计必须满足的预期，否则就要付出代价去克服。<bookmark mark='c'/>编码：形状、大小、颜色、位置和质地，几种同时使用，这样一种失效会被另一种发现。<bookmark mark='d'/>还有一致性：在操作员使用的每一个系统上，同一个动作都在同一个位置。",
    "Controls also take time to reach. <bookmark mark='a'/> In 1954 Paul Fitts showed that the ":
        "操纵器件还需要时间去够到。<bookmark mark='a'/>1954年，保罗·菲茨证明，击中一个目标所需的时间随其距离与宽度之比的对数增长。<bookmark mark='b'/>这里是四百次模拟的动作，斜率约为每比特零点一五秒。<bookmark mark='c'/>所以频繁或紧急的动作要用又大又近的目标。屏幕的边缘和角落是无限深的，因为指针会停在那里。<bookmark mark='d'/>而那些应当刻意费力的动作，则用又小又远的目标。",
    "Choices take time too. <bookmark mark='a'/> The Hick-Hyman law: reaction time grows with t":
        "选择也需要时间。<bookmark mark='a'/>希克-海曼定律：反应时随同等可能的选项数目的对数增长。<bookmark mark='b'/>不兼容的映射，比如右边的灯亮了要按左键，会多出一个转换步骤，而代价随选项增多而增长。<bookmark mark='c'/>在紧急情况下，每多一个比特都是时间。兼容的映射在压力下依然很快，不兼容的则会崩溃。<bookmark mark='d'/>第1部分的唐德斯就是用同样的方法测量心理阶段的。",
    'Chapter three. Slips, lapses and mistakes.':
        '第3章。失误、遗漏与错误。',
    "Not every error is the same failure. <bookmark mark='a'/> Slips: the right plan, the wrong":
        "并非每个差错都是同一种失败。<bookmark mark='a'/>失误：计划是对的，动作是错的，就像用起落架杆代替了襟翼杆。设计可以发现它们，靠编码和互锁。<bookmark mark='b'/>遗漏：计划是对的，却忘了一步。油箱盖没盖，或者在一次打断之后跳过了检查单上的一项。这是第19部分的工作记忆。<bookmark mark='c'/>错误：计划是错的，却执行得很好。一次误诊，或者把一条规则用在了不合适的地方。反馈和其他人能发现它们。<bookmark mark='d'/>还有违规：有意打破规则，往往是因为规则本身行不通。唐纳德·诺曼和詹姆斯·里森划出了这些界线。",
    "Jens Rasmussen added a ladder of control. <bookmark mark='a'/> Skill-based: fluent, automa":
        "延斯·拉斯穆森又加上了一个控制的阶梯。<bookmark mark='a'/>基于技能：流畅、自动的动作，又快又准，当注意力游离时容易失误。<bookmark mark='b'/>基于规则：如果这样，就那样。程序和习得的模式，其差错是好规则被误用。<bookmark mark='c'/>基于知识：在新情境中从第一原理出发推理。它缓慢而费力，大多数错误就出在这里。紧急情况常常把操作员推到这个阶梯的底层，而且是在最糟糕的时刻。",
    "This changes the question. <bookmark mark='a'/> The old view says the system is safe, and ":
        "这改变了问题。<bookmark mark='a'/>旧观点认为系统是安全的，人的差错是事故的原因。<bookmark mark='b'/>新观点认为人的差错是系统深处问题的症状，所以要问，这个动作在当时为什么说得通。<bookmark mark='c'/>正如西德尼·德克尔所说，事后看来，通向事故的道路一目了然。而操作员当时看到的是一片可能路径的森林。<bookmark mark='d'/>于是这一部分的问题变成了：是哪种设计让这个差错变得可能？",
    'Chapter four. A light that told the wrong story.':
        '第4章。一盏讲错了故事的灯。',
    "Here's what design-induced error looks like at scale. <bookmark mark='a'/> In 1979, at Thr":
        "这就是大规模的设计诱发差错的样子。<bookmark mark='a'/>1979年，在三里岛，一座核电站冷却回路中的泄压阀按设计打开，随后卡在了打开的位置。<bookmark mark='b'/>面板上的一盏灯熄灭了。它表示的是阀门已被命令关闭，而不是阀门已经关闭。<bookmark mark='c'/>操作员以为阀门已关，又把稳压器中上升的水位理解为水太多，于是减少了应急冷却。<bookmark mark='d'/>最初几分钟里响起了数百个警报，堆芯部分熔化。<bookmark mark='e'/>调查发现，操作员所做的正是他们的显示器和培训所暗示的事。",
    "What changed afterwards? <bookmark mark='a'/> Show the state: display what a component is ":
        "之后改变了什么？<bookmark mark='a'/>显示状态：显示部件实际在做什么，是测量出来的，而不是它被告知要做什么。<bookmark mark='b'/>给警报排优先级：给它们排序、分组，抑制后续连带的警报，让最初的原因保持可见。<bookmark mark='c'/>为意外而训练：在模拟器上练习程序没有覆盖的故障。<bookmark mark='d'/>还有法律规定的人因学：控制室设计审查成为发放执照的一部分。",
    'Chapter five. Attention at work.':
        '第5章。工作中的注意。',
    "How much can one person do at once? <bookmark mark='a'/> If attention were one pool, as a ":
        "一个人同时能做多少事？<bookmark mark='a'/>如果注意力是一个单一的资源池，也就是单一的瓶颈，那么任何两项任务都会相互干扰。<bookmark mark='b'/>克里斯托弗·威肯斯提出了多个资源池。当任务共享同一种通道（眼睛或耳朵）、同一种编码（空间或言语）、同一个阶段（知觉或反应）时，干扰更大。<bookmark mark='c'/>所以用眼睛飞行的飞行员用耳朵接听无线电，司机的导航是说出来的，而不是显示出来的。<bookmark mark='d'/>但即使是分开的资源池也共享一个中央执行系统。正如第18部分所示，打电话仍然会让司机刹车变慢。",
    "Workload has to be measured. <bookmark mark='a'/> The most used scale is NASA's task load ":
        "工作负荷必须被测量。<bookmark mark='a'/>最常用的量表是美国宇航局的任务负荷指数：六项从零到一百的评分，然后是十五次两两选择，判断对这项任务而言哪个量表更重要。<bookmark mark='b'/>得分用这些选择给每项评分加权：这里是六十，而原始平均值是五十一。<bookmark mark='c'/>还有其他测量方法：一项次要任务，主任务占用越多，它的表现就越差；还有瞳孔大小或心率变异性。<bookmark mark='d'/>没有哪一种测量就等于工作负荷。当它们不一致时，每一种都在告诉你一些东西。",
    'Chapter six. The watch.':
        '第6章。值守。',
    "Here's the decrement Mackworth found. <bookmark mark='a'/> Psyche's sixty watchers spend t":
        "这就是麦克沃斯发现的下降。<bookmark mark='a'/>Psyche的六十名值守者每人在时钟前待两个小时，大约每八十次跳动出现一次双跳。<bookmark mark='b'/>在头半个小时，他们检出了大约百分之七十三的信号。在最后半个小时，不到一半。<bookmark mark='c'/>麦克沃斯发现下降在头半个小时内就开始了，后来的研究在雷达、声呐、机场安检和质量控制中都发现了它。<bookmark mark='d'/>而且这不只是无聊。盯着罕见的信号是艰苦而有压力的工作。",
    "Is it sensitivity or criterion? Part 12's tools can tell. <bookmark mark='a'/> For each ha":
        "是敏感性还是判断标准？第12部分的工具可以分辨。<bookmark mark='a'/>每半小时的击中和虚报给出d撇和判断标准。<bookmark mark='b'/>这里d撇下降了：值守者的辨别能力变差了。<bookmark mark='c'/>判断标准上升了：值守者也更不愿意说“有信号”，所以虚报也减少了。在Psyche中，两者都是植入的。<bookmark mark='d'/>在真实的值守中，乔尔·西及同事的元分析发现，变化的是哪一个取决于任务，补救办法也不同：敏感性靠休息和辅助，判断标准靠反馈和预期。",
    "One caution. <bookmark mark='a'/> Here's the same watch for a single watcher, by half hour":
        "一个提醒。<bookmark mark='a'/>这是同一场值守中一名值守者每半小时的记录。<bookmark mark='b'/>每半小时大约只有七个信号，一个人的记录上下跳动。下降是真实的，但一个人的曲线无法可靠地显示它。<bookmark mark='c'/>又是第47部分的道理。群体曲线描述的是任务，个人曲线需要多得多的信号。<bookmark mark='d'/>这就是为什么用几分钟的数据来判断是否适合上岗的测试是靠不住的。",
    'Chapter seven. Rare targets.':
        '第7章。罕见的目标。',
    "Rare targets bring a second problem. <bookmark mark='a'/> Part 12 entered the row: in 2005":
        "罕见的目标带来第二个问题。<bookmark mark='a'/>第12部分记下了这一行：2005年，杰里米·沃尔夫、托德·霍洛维茨和娜奥米·肯纳让人在行李图像中寻找工具，当出现率很低时，他们漏掉的要多得多。<bookmark mark='b'/>信号检测论的解释是：当目标罕见时，说“没有”通常是对的，于是判断标准向上漂移。<bookmark mark='c'/>一个只向最优点移动三分之一的观察者，在一半行李中有目标时漏报百分之十六，在一百个中只有一个时漏报超过百分之四十。完全移到最优点反而会漏得更多。<bookmark mark='d'/>机场安检和癌症筛查都是低出现率的搜索。",
    "Expert eyes miss things too. <bookmark mark='a'/> In 2013 Trafton Drew, Melissa Vo and Jer":
        "专家的眼睛也会漏掉东西。<bookmark mark='a'/>2013年，特拉夫顿·德鲁、梅丽莎·沃和杰里米·沃尔夫在一张肺部扫描图中插入了一只小猩猩。<bookmark mark='b'/>眼动追踪显示，寻找结节的放射科医生直视过它，而大多数人没有报告它。<bookmark mark='c'/>专家对第18部分的非注意盲视并不免疫。专业训练让搜索对准预期中的东西。<bookmark mark='d'/>在筛查项目中，意外的发现正是没有人在寻找的那一个。",
    "So what helps? <bookmark mark='a'/> Insert targets: add known fake targets so prevalence f":
        "那么什么有帮助？<bookmark mark='a'/>插入目标：加入已知的假目标，让出现率感觉更高，判断标准保持在低位。机场系统就这样做。<bookmark mark='b'/>双人阅片：两名独立的阅片者，或者一名阅片者加一个算法。<bookmark mark='c'/>休息：用短时值守和轮换来对抗下降。<bookmark mark='d'/>还有反馈：告诉搜索者他们漏掉了什么，让他们的预期与世界相符。",
    'Chapter eight. Situation awareness.':
        '第8章。态势感知。',
    "What does an operator need to know, right now? Mica Endsley's answer in 1995 has three lev":
        "操作员此时此刻需要知道什么？米卡·恩兹利在1995年的回答有三个层次。<bookmark mark='a'/>第一层：知觉各个要素，比如空速、其他飞机、警告灯。<bookmark mark='b'/>第二层：把它们放在一起理解。这个模式对我的目标意味着什么？<bookmark mark='c'/>第三层：预测。那架飞机两分钟后会在哪里？专家的优势大多在第二层和第三层，在第24部分的组块和图式之中。",
    "Where does awareness fail? <bookmark mark='a'/> Debra Jones and Mica Endsley coded the awa":
        "感知在哪里失败？<bookmark mark='a'/>黛布拉·琼斯和米卡·恩兹利对航空事故报告中的感知差错进行了编码。<bookmark mark='b'/>大约四分之三在第一层。信息没有被知觉到，往往是因为它没有被显示、很难看清，或者根本没人去看。<bookmark mark='c'/>其余的大多在第二层：信息被看到了，但它的意义被错过了。<bookmark mark='d'/>这是一个设计目标。把要素放在眼睛本来就在看的地方，并显示它们意味着什么。",
    "How is awareness measured? <bookmark mark='a'/> The freeze probe, SAGAT: stop the simulato":
        "态势感知如何测量？<bookmark mark='a'/>冻结探查法SAGAT：停下模拟器，清空显示，就三个层次提问，并对照模拟器中的真实情况给回答打分。<bookmark mark='b'/>在线探查法SPAM：在任务进行、显示可见时提问，用回答所需的时间衡量知识有多现成。<bookmark mark='c'/>自评法SART，在运行之后进行。它们追踪的是自信，而第25部分已经表明自信是另一回事。<bookmark mark='d'/>还有一个批评。正如西德尼·德克尔所警告的，“丧失态势感知”可能变成事后归咎的标签。只有在任何人知道结果之前进行的测量才有用。",
    'Chapter nine. The ironies of automation.':
        '第9章。自动化的讽刺。',
    "Automation isn't all or nothing. <bookmark mark='a'/> In 1978 Thomas Sheridan and William ":
        "自动化不是全有或全无。<bookmark mark='a'/>1978年，托马斯·谢里登和威廉·韦普兰克列出了十个层级，从人做一切，到计算机提建议，再到计算机自行行动且不告诉任何人。<bookmark mark='b'/>2000年，拉贾·帕拉苏拉曼、谢里登和克里斯托弗·威肯斯又加上了阶段。你可以把获取信息、分析信息、做决定或执行分别自动化，每一项都有自己的层级。<bookmark mark='c'/>驾驶有自己的分级，从零到五。在二级，驾驶员每时每刻都在监督。在三级，汽车自己开，驾驶员必须在被要求时接管。<bookmark mark='d'/>所以问题不是要多少自动化，而是哪个功能、自动化到什么层级、人在做什么？",
    "In 1983 Lisanne Bainbridge named the ironies of automation. <bookmark mark='a'/> Designers":
        "1983年，莉莎妮·班布里奇提出了“自动化的讽刺”。<bookmark mark='a'/>设计者把人做得不好的任务自动化，把他们无法自动化的任务留给人。<bookmark mark='b'/>人变成了监视者。这是第18部分的警觉，被要求于一个无事可做的人。<bookmark mark='c'/>而当自动化失败时，人是后备。但技能不练就会退化，而落到人手里的故障都是难的那些。<bookmark mark='d'/>所以自动化越可靠，练习越少，失败时人就越没有准备。<bookmark mark='e'/>她的建议是让人保持练习：模拟器、手动阶段，以及显示自动化在做什么的显示器。",
    "Here's the irony as a model. <bookmark mark='a'/> Assume that an operator's median takeove":
        "这是这一讽刺的一个模型。<bookmark mark='a'/>假设随着练习和预期的消退，操作员的中位接管时间随两次故障之间时间的对数增长。这是一个假设，为了展示曲线的形状而选定。<bookmark mark='b'/>中位接管时间从自动化每十次需求失败一次时的约三秒半，增加到每一万次失败一次时的六秒。<bookmark mark='c'/>在七秒的时限内，起初百分之九十五的接管能够成功，到最后是百分之六十二。<bookmark mark='d'/>然而系统仍然变得更安全了。每次需求的失败从千分之五左右降到十万分之四左右，因为自动化失败得少多了。<bookmark mark='e'/>所以讽刺不在于自动化不安全，而在于残余风险转移到了人最没有准备的那一刻。",
    "Automation adds a new error: mode confusion. <bookmark mark='a'/> A mode is the automation":
        "自动化带来一种新的差错：模式混淆。<bookmark mark='a'/>模式是自动化当前对同一个输入的解读方式。<bookmark mark='b'/>1992年在斯特拉斯堡附近，一架空客的机组据信本想设定三点三度的下降航迹。自动驾驶仪处在垂直速度模式，同样的输入意味着每分钟三千三百英尺。<bookmark mark='c'/>两种模式在显示器上只差几个字符。<bookmark mark='d'/>在厄尔·维纳对航空公司飞行员的调查中，“它现在在做什么”是自动化驾驶舱里最常见的问题之一。<bookmark mark='e'/>设计规则：模式要少，不能有无声的模式切换，模式要显示在眼睛本来就在看的地方。",
    "Here's the takeover problem at its worst. <bookmark mark='a'/> In 2009, over the Atlantic ":
        "这是接管问题最糟糕的样子。<bookmark mark='a'/>2009年，在大西洋上空的夜里，结冰堵塞了一架空客的空速管。自动驾驶仪断开，把飞机交还给机组。<bookmark mark='b'/>操纵飞机的飞行员拉起了机头。飞机爬升、减速，然后失速。<bookmark mark='c'/>失速警告响起，随后在空速读数低到被判为无效时又安静了下来。压低机头这个正确的动作，反而让警告又响了起来。<bookmark mark='d'/>机组始终没有识别出失速，二百二十八人遇难。<bookmark mark='e'/>法国调查人员指出了在巡航高度被迫接管的意外、在那个高度手动飞行练习很少，以及一个教会了错误教训的警告。班布里奇的讽刺，同时出现。",
    'Chapter ten. Trust and alarms.':
        '第10章。信任与警报。',
    "How much should an operator believe a machine? <bookmark mark='a'/> John Lee and Katrina S":
        "操作员应该在多大程度上相信一台机器？<bookmark mark='a'/>约翰·李和卡特里娜·西在2004年说得很简单。目标不是高信任，而是校准过的信任，位于对角线上，与自动化实际有多可靠相匹配。<bookmark mark='b'/>对角线上方是误用：在自动化能力之外依赖它。自动化偏差，即听从错误的建议，或者漏掉它漏掉的东西。<bookmark mark='c'/>对角线下方是弃用：在几次虚警或一次鲜明的失败之后无视良好的自动化。<bookmark mark='d'/>信任跟随操作员能看到的东西，所以要显示自动化在这种情境下的可靠性，而不是平均可靠性。<bookmark mark='e'/>第26部分的算法厌恶是弃用，第13章的自满一行是误用。",
    "An alarm is Part 12's criterion, chosen by an engineer. <bookmark mark='a'/> A sensor read":
        "警报是第12部分的判断标准，由一位工程师选定。<bookmark mark='a'/>一个传感器读到的要么是噪声，要么是高出两个半标准差的事件，而事件是一百次读数中的一次。<bookmark mark='b'/>一个一个标准差的谨慎阈值能对百分之九十三的事件报警。但它的警报中只有百分之五到六是真的。<bookmark mark='c'/>操作员会学会这些概率。詹姆斯·布利斯发现，人们响应警报的频率大约等于警报为真的频率，而如果是这样，很少有事件得到响应。<bookmark mark='d'/>让最多事件得到响应的阈值大约是二点七，即便如此也只有百分之二十三。<bookmark mark='e'/>所以工程师设定了一个判断标准，操作员的信任又设定了第二个。两个都必须设计。",
    "So how do you build a better alarm? <bookmark mark='a'/> Raise the base rate. Alarm on com":
        "那么如何造出更好的警报？<bookmark mark='a'/>提高基础率。根据组合和趋势而不是单个读数报警，让更多警报是真的。<bookmark mark='b'/>给警报分级。罗伯特·索金的似然警报会说“可能”“很可能”或“确定”，让响应与之相称。<bookmark mark='c'/>延迟与适配。几秒钟的延迟，以及根据病人设定的界限，能去掉许多自行平息的警报。<bookmark mark='d'/>还要计数。每小时警报数和被处理的比例是可以测量的，设计审查可以设定目标。",
    "Here's what that looks like in a hospital. <bookmark mark='a'/> A monitored intensive-care":
        "这在医院里是这个样子。<bookmark mark='a'/>一张有监护的重症监护病床一天可以响起数百次警报。<bookmark mark='b'/>对床边监护仪的研究发现，这些警报大多是假的，或不需要任何处理。<bookmark mark='c'/>于是护士调低音量、放宽界限，或者不再听见它们。这就是“狼来了”效应，它是一个习得的判断标准。<bookmark mark='d'/>2013年，美国联合委员会在几起与无人响应的警报有关的死亡之后，发布了关于警报安全的警示。<bookmark mark='e'/>对于她们所面对的警报而言，护士的判断标准是理性的。要修的是警报。",
    'Chapter eleven. Systems, checklists and crews.':
        '第11章。系统、检查单与机组。',
    "Can a system be safer than its people? <bookmark mark='a'/> James Reason's answer is a pic":
        "一个系统能比它的人更安全吗？<bookmark mark='a'/>詹姆斯·里森的回答是一幅图：多层防御，就像一片片瑞士奶酪，每片都有洞。一次事故需要每一层同时有洞。<bookmark mark='b'/>取四层，每层十次失效一次。如果它们独立失效，那就是一万次一次事故。<bookmark mark='c'/>但洞可能有共同的原因：疲劳、走捷径的文化、一个糟糕的程序。如果各层之间的相关为零点六，大约是七十次一次。<bookmark mark='d'/>纵深防御只有在各层独立失效时才有效，而里森所说的“潜在条件”会让它们一起失效。",
    "The checklist is the simplest defence. <bookmark mark='a'/> Aviation's checklists began in":
        "检查单是最简单的防御。<bookmark mark='a'/>航空检查单始于1935年，当时一架新型轰炸机在试飞中坠毁，因为一个操纵锁没有解除。<bookmark mark='b'/>2009年，亚历克斯·海恩斯及同事把一份十九项的手术检查单带到了八个国家的八家医院。<bookmark mark='c'/>前后对比，死亡率从约百分之一点五降到百分之一以下，并发症从约百分之十一降到百分之七。<bookmark mark='d'/>但那是一项前后对比研究。在安大略省，当一项规定强制每家医院都使用检查单时，死亡和并发症都没有变化。<bookmark mark='e'/>检查单是通过拥有它的团队起作用的：那次停顿、那些名字，以及开口说话的许可。",
    "Here's the accident that changed crews. <bookmark mark='a'/> In 1977 two jumbo jets were d":
        "这是改变了机组的那次事故。<bookmark mark='a'/>1977年，两架大型喷气客机被转降到特内里费岛一座雾气笼罩的小机场。一架正沿跑道滑行，另一架在跑道尽头等待。<bookmark mark='b'/>等待的那位机长是一名资深的训练飞行员，他在没有获得起飞许可的情况下开始了起飞。<bookmark mark='c'/>他的随机工程师问另一架飞机是否已经离开跑道，机长说已经离开了。<bookmark mark='d'/>无线电通话相互重叠，而“我们现在正在起飞”对机组和塔台意味着不同的事。<bookmark mark='e'/>五百八十三人遇难。它至今仍是航空史上死亡人数最多的事故。",
    "After Tenerife, and other crashes where someone saw the problem and didn't say so, came cr":
        "在特内里费之后，以及在其他有人看到了问题却没有说出来的坠机之后，出现了机组资源管理。<bookmark mark='a'/>美国宇航局在二十世纪七十年代末的研究发现，大多数事故涉及机组在沟通、领导和决策上的失败，而不是飞行技术的失败。<bookmark mark='b'/>这种培训教人用分级的话术开口提出疑问、通报计划、交叉检查，并让机长的权威可以被质疑。这是针对第34部分的服从所做的设计。<bookmark mark='c'/>它推广到了手术室、急诊室、船舶和控制室。<bookmark mark='d'/>至于证据：态度和行为会可靠地改变。对事故的影响很难测量，因为事故很少见。这是第7章的问题，放大到了整个行业的层面。",
    'Chapter twelve. Fatigue as a measured risk.':
        '第12章。作为一种可测量风险的疲劳。',
    "Part 10 built the clocks. Here's what they cost at work. <bookmark mark='a'/> In 1997 Drew":
        "第10部分搭建了生物钟。这里是它们在工作中的代价。<bookmark mark='a'/>1997年，德鲁·道森和凯瑟琳·里德让人在连续清醒二十八小时的过程中做一项手眼追踪任务，又让同一批人在饮酒后做同样的任务。<bookmark mark='b'/>清醒约十七小时后，表现相当于血液酒精浓度百分之零点零五。清醒约二十四小时后，相当于百分之零点一。<bookmark mark='c'/>早上七点开始的班次到午夜就已清醒十七个小时。<bookmark mark='d'/>这里的线是按他们报告的结果画的。这种等价关系因任务而异，但量级是成立的。",
    "It's not only the hours. <bookmark mark='a'/> Part 10's two processes: sleep pressure buil":
        "不只是小时数。<bookmark mark='a'/>第10部分的两个过程：睡眠压力随清醒时长累积，昼夜节律钟在凌晨又加上一个低谷。<bookmark mark='b'/>因开车睡着而发生的车祸在清晨达到高峰，午后又有一个高峰。<bookmark mark='c'/>还有微睡眠，几秒钟的注意力丧失，当事人往往察觉不到。<bookmark mark='d'/>而疲倦的人对自己受损的程度判断得很差。又是第25部分的自信与准确不同步。<bookmark mark='e'/>所以一条只管小时数的规则会漏掉夜班的低谷和下班后漫长的回家车程。",
    "So how is fatigue managed? <bookmark mark='a'/> With limits on hours of service. They're s":
        "那么疲劳如何管理？<bookmark mark='a'/>用工作时长的限制。它们易于审核，却看不见生物钟，也看不见一个人实际睡了多少。<bookmark mark='b'/>用疲劳风险管理系统，它用双过程生物钟模型来模拟排班，在不追责的前提下收集疲劳报告，并作出调整。<bookmark mark='c'/>用对策：计划好的小睡、在低谷时饮用咖啡因、光照，以及夜班后有人送回家。<bookmark mark='d'/>至于住院医师，这是一个有争议的案例。一项缩短实习医生班次的试验发现严重差错减少了。后来规模更大的工作时长规定试验发现效果更小或好坏参半。排班很重要，每次交接班时发生的事也同样重要。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Four new rows. The first: in a long watch for rare signals, detection falls within the fir':
        "新增四行。第一行：在为罕见信号进行的长时间值守中，检出率在头半个小时内就下降，而且持续下降。<bookmark mark='a'/>原始研究：麦克沃斯的时钟，1948年。<bookmark mark='b'/>后续记录：西及同事的元分析，以及一篇把警觉视为艰苦、有压力的工作的综述。<bookmark mark='c'/>罕见的信号、漫长的值守和困难的辨别会让它更糟，休息、反馈和辅助会减轻它。<bookmark mark='d'/>已重复。",
    'The second: a short surgical safety checklist reduces deaths and complications. <bookmark ':
        "第二行：一份简短的手术安全检查单能减少死亡和并发症。<bookmark mark='a'/>原始研究：海恩斯及同事，2009年，八家医院的前后对比。<bookmark mark='b'/>后续记录：在安大略省的强制规定下没有变化，在一项阶梯楔形试验中并发症减少。<bookmark mark='c'/>在团队真正采用它的地方，它有帮助。作为文书工作强加下来，效果就缩小或消失。<bookmark mark='d'/>有争议。",
    'The third: people monitoring reliable automation detect its rare failures less well, and l':
        "第三行：监视可靠自动化的人，对它罕见的失败检出得更差，而且它过去越可靠就越差。<bookmark mark='a'/>原始研究：帕拉苏拉曼、莫洛伊和辛格，1993年。<bookmark mark='b'/>后续记录：一篇关于自满和自动化偏差的综述，涵盖实验室和现场任务，也包括专家。<bookmark mark='c'/>这是一种在大多数时候都说得通的注意力分配，这也是为什么单靠培训几乎无法消除它。<bookmark mark='d'/>已重复。",
    'And the fourth: seventeen to twenty-four hours awake impairs performance about as much as ':
        "第四行：清醒十七到二十四小时对表现的损害，大约相当于血液酒精浓度百分之零点零五到百分之零点一。<bookmark mark='a'/>原始研究：道森和里德，1997年。<bookmark mark='b'/>后续记录：威廉森和费耶的一组测试，得到相似的量级。<bookmark mark='c'/>这种等价关系因任务而异，但一个长班次结束时的损害，如果来自一杯酒，法律是禁止的。<bookmark mark='d'/>已重复。",
    "What the four have in common. <bookmark mark='a'/> Three are effects of the person in the ":
        "这四行的共同点。<bookmark mark='a'/>有三行是系统中的人的效应：随时间变化的注意、自动化下的注意，以及生物钟。<bookmark mark='b'/>它们重复得很好，因为它们建立在第10、12和18部分之上。<bookmark mark='c'/>有争议的那一行是一项干预。它通过团队和文化起作用，而强制规定复制不了这些。<bookmark mark='d'/>人的局限是稳定的。修补办法则取决于它们被放进的系统。",
    'Chapter fourteen. In practice: a takeover request, designed.':
        '第14章。实践中：设计一次接管请求。',
    "Where does this work get done? <bookmark mark='a'/> In aviation, where certification asks ":
        "这项工作在哪里进行？<bookmark mark='a'/>在航空领域，适航认证要求驾驶舱设计提供人因论证，事故征候以不追责的方式报告并分析。<bookmark mark='b'/>在医疗器械领域，可用性标准要求在可能因使用差错造成伤害的任务上，用真实用户进行测试。<bookmark mark='c'/>在核电、铁路和电网的控制室里：警报管理指标、程序设计和模拟器培训。<bookmark mark='d'/>还有在车辆上：驾驶员监测、接管请求，以及部分自动化汽车的驾驶员会移开视线的证据。",
    "Here's a worked design. <bookmark mark='a'/> The situation: a level-three car on a motorwa":
        "这是一个完整的设计示例。<bookmark mark='a'/>情境：高速公路上的一辆三级自动驾驶汽车。系统将在四十秒后到达它能处理的道路尽头，或者现在就遇到一个故障。<bookmark mark='b'/>我们知道的：第9章的接管时间随可靠性而拉长，脱离回路的驾驶员已经在第二层和第三层丧失了态势感知。<bookmark mark='c'/>目标：在时限用完之前，大多数驾驶员都稳定并掌控车辆，在模拟器中测量，判断标准事先写下来，正如第43部分所要求的。",
    "A takeover request, in four steps. <bookmark mark='a'/> Early: for a planned end of automa":
        "一次接管请求，分四步。<bookmark mark='a'/>提前：对于计划中的自动驾驶结束，在四十秒时给出提示，显示并说出来，并说明原因。<bookmark mark='b'/>请求，在大约十秒时：一个声音、一次座椅振动和一个显示。三个通道，威肯斯的每个资源池各一个。<bookmark mark='c'/>核查：在汽车交出控制之前，驾驶员监测确认眼睛看着路面、双手握着方向盘。<bookmark mark='d'/>还有后备方案。如果没有回应，汽车减速，在它能到达的最安全车道停下，并打开危险警示灯。<bookmark mark='e'/>每一步都是关于人的一个假设，先在模拟器中对照目标检验，再在道路上检验。",
    "All of this goes into a safety case. <bookmark mark='a'/> Its human-factors section lists ":
        "这一切都写进一份安全论证。<bookmark mark='a'/>其中人因的部分列出任务：人必须知觉、决定和做什么，以及在多长时间内。<bookmark mark='b'/>危害：对于每一步，那里可能发生的失误、遗漏和错误。<bookmark mark='c'/>证据：用户测试和模拟器研究，包括它们的样本、判断标准和失败。<bookmark mark='d'/>残余风险：还剩下什么，以及为什么可以接受，尽可能用数字表示。<bookmark mark='e'/>还有一个从现场学习的计划，阅读事故征候报告是为了设计，而不是为了追责。",
    'Chapter fifteen. Frontier: supervising learning machines.':
        '第15章。前沿：监督会学习的机器。',
    "What changes when the automation learns? <bookmark mark='a'/> Classic automation fails at ":
        "当自动化会学习时，什么变了？<bookmark mark='a'/>经典的自动化在已知的边界上失败。一个习得的系统可能在一个人看来很普通的输入上失败。<bookmark mark='b'/>一个助手自信、文笔流畅的回答，无论对错，都会引来第25部分那种对流畅的信任。<bookmark mark='c'/>可靠性会漂移。一次更新可能改变系统擅长的东西，所以上个月校准过的信任今天可能就错了。<bookmark mark='d'/>监视的规模扩大了。一名监督者可能同时看着许多车辆或智能体，那就是警觉和接管，成倍增加。",
    "Decision aids are already in high-stakes work. <bookmark mark='a'/> Radiology, pathology a":
        "决策辅助已经进入了高风险的工作。<bookmark mark='a'/>放射科、病理科和皮肤科都测试过有无算法建议时的阅片者。<bookmark mark='b'/>正确的建议让阅片者更好。错误的建议会把他们带偏，专家也不例外。那就是被测量出来的自动化偏差。<bookmark mark='c'/>设计问题就是这一部分的问题：何时显示建议、如何显示它的不确定性，以及谁先阅片。<bookmark mark='d'/>而评估的问题是人与机器在一起的表现，而不是机器单独的表现。",
    "And the open problems. <bookmark mark='a'/> Monitoring that measures an operator's readine":
        "还有开放的问题。<bookmark mark='a'/>能测量操作员准备程度的监测，而不只是测量眼睛看向哪里。<bookmark mark='b'/>解释：哪些解释能改善校准，哪些只会提高信任。<bookmark mark='c'/>技能：当机器大部分时间都在做事时，如何让人的技能保持鲜活。这是班布里奇的问题，至今仍未解决。<bookmark mark='d'/>还有测量：把险情和接管当作数据，并为习得系统建立共享、公开的事故报告。",
    "First, your four numbers. <bookmark mark='a'/> In the last half hour of a two-hour watch, ":
        "首先，你的四个数字。<bookmark mark='a'/>在两小时值守的最后半个小时，Psyche的值守者捕捉到了大约一半的信号。当目标从两个行李中有一个降到一百个中有一个时，漏报从百分之十六升到百分之四十二。当自动化从每十次需求失败一次变成每一万次失败一次时，七秒内完成的接管从百分之九十五降到百分之六十二。而清醒大约十七个小时对表现的损害，相当于血液酒精浓度百分之零点零五。<bookmark mark='b'/>每一个都是设计者可以事先规划的人的局限。没有一个是归咎于遇到它的那个人的理由。",
    "Part fifty-one in twelve lines. <bookmark mark='a'/> Error is designed in, through shape, ":
        "第五十一部分，十二行。<bookmark mark='a'/>差错是通过形状、位置和兼容性设计进去的。菲茨定律和希克定律预测动作和选择的时间。失误、遗漏、错误和违规需要不同的修补办法。显示状态，而不是命令。工作负荷是多种资源，用多种方法测量。警觉在头半个小时内就下降。罕见的目标会抬高判断标准。态势感知最常在知觉层面失败。可靠的自动化留下一个没有准备的人。警报是一个判断标准，信任是第二个。防御会因共同的原因一起失效。而疲劳是一种可测量、可管理的风险。",
    "Where this comes back. <bookmark mark='a'/> Fitts's and Hick's laws become an engineering ":
        "这些内容会在哪里再次出现。<bookmark mark='a'/>菲茨定律和希克定律在第52部分变成界面的工程模型。工作中的选拔和培训是第53部分。第56部分把目击者列队辨认当作一项检测任务。而人监督会学习的机器，会在第60部分再次出现。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applie":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道应用菲茨定律。一道求值守者的d撇和判断标准。一道问有多大比例的警报是真的。一道把四层奶酪叠起来。一道给任务负荷指数打分。一道求按时完成的接管比例。最后带星号的一道，请你为一台输液泵写安全论证中的人因部分。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Wickens and colle':
        '这一部分所依据的书籍和论文列在这里，也列在README中。威肯斯及同事的教科书是这一领域的参考书；里森的《人的差错》给了它词汇；德克尔的实地指南是关于“为什么这个动作在当时说得通”的最好的简短论证。',
    "Act Twelve has begun. <bookmark mark='a'/> This part put a person into a system and asked ":
        "第十二幕已经开始。<bookmark mark='a'/>这一部分把一个人放进一个系统，并追问系统应该在哪里弯曲。<bookmark mark='b'/>下一部分追问，心理学是否足够定量，可以用来做工程。二十世纪八十年代末，一家电话公司正要购买每通电话能节省几秒钟的工作站。一个在纸上搭建的操作员模型说，它们会更慢。第52部分：为心智而设计。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
