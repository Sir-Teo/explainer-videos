"""Chinese narration for psych54: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第54部分：学习的科学'

CHAPTERS = {
    'Hook': '二西格玛',
    'Predict': '1. 在你身上：两份单词表，以及四个数字',
    'Retrieval': '2. 提取练习',
    'Spacing': '3. 间隔与交错',
    'Bjork': '4. 学习与表现之别',
    'Ranked': '5. 十种学习技巧，排个名次',
    'Load': '6. 认知负荷',
    'Myths': '7. 迷思',
    'Tutoring': '8. 辅导',
    'Scheduler': '9. 安排复习',
    'Reading': '10. 学习阅读',
    'Beliefs': '11. 关于能力的信念',
    'Feedback': '12. 反馈',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：重新设计一门课的学习计划',
    'Frontier': '15. 前沿：AI辅导与能迁移的东西',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    'In 1984 the educational psychologist Benjamin Bloom published a challenge. <bookmark mark=':
        "1984年，教育心理学家本杰明·布鲁姆发出了一个挑战。<bookmark mark='a'/>在他的学生所做的研究中，接受一对一辅导的学生，比在三十人班级里上课的学生高出约两个标准差。<bookmark mark='b'/>接受辅导的普通学生，胜过了班上百分之九十八的人。<bookmark mark='c'/>没有哪所学校能给每个孩子配一位辅导老师，于是布鲁姆向教育界发起挑战：找到同样好的集体教学方法。<bookmark mark='d'/>这个挑战成了教育技术的奠基承诺。",
    "Forty years on, the two sigma has shrunk. <bookmark mark='a'/> The original studies were s":
        "四十年过去，二西格玛缩水了。<bookmark mark='a'/>最初的研究规模小、时间短，用的测验是专门为所教内容编制的。<bookmark mark='b'/>库尔特·范莱恩2011年对人类辅导的综述发现，效应约为零点八个标准差，而不是二，最好的计算机辅导系统也接近这个水平。<bookmark mark='c'/>大型的学校辅导试验发现的收益是零点几个标准差，在校内每天进行的高强度辅导中更大一些。<bookmark mark='d'/>而证据最强的学习方法，恰恰是学生认为不如重读有效的那些。<bookmark mark='e'/>第20和第21部分的记忆研究变成了一个工程问题：下一次复习应该在什么时候？",
    "So this part asks: what's the best way to learn something, and why do learners choose the ":
        "所以这一部分要问：学东西最好的方法是什么，为什么学习者偏偏选了相反的做法？<bookmark mark='a'/>提取、间隔与交错，以及它们为什么感觉更糟。<bookmark mark='b'/>十种技巧的排名、认知负荷，以及那些迷思。<bookmark mark='c'/>为学习者建模的辅导系统和复习调度器。<bookmark mark='d'/>还有阅读、信念与反馈。",
    "This is Part 54 of Psychology, Built: the science of learning. <bookmark mark='a'/> We'll ":
        "这是《心理学，从零搭建》第54部分：学习的科学。<bookmark mark='a'/>我们会把提取练习、间隔和交错带进课堂。我们会区分学习与表现，并认识流畅性错觉。我们会给十种学习技巧排名，并为认知负荷做设计。我们会检验学习风格和其他迷思。我们会诚实地衡量辅导的效果，并在Psyche身上让几种复习调度器比赛。我们还会看看阅读、思维模式，以及大规模的反馈。",
    'Chapter one. On you: two lists, and four numbers.':
        '第1章。在你身上：两份单词表，以及四个数字。',
    "First, an experiment on you. <bookmark mark='a'/> On the course site there are two lists o":
        "首先，一个在你身上做的实验。<bookmark mark='a'/>课程网站上有两份词对表。一份连续学习三遍，另一份学习三遍、中间穿插别的任务。<bookmark mark='b'/>先预测你会把哪一份记得更好。<bookmark mark='c'/>测验在页面的最后。大多数人预测集中学习的那份，而大多数人记住更多的是间隔学习的那份。<bookmark mark='d'/>任何东西都不会被存储或发送。你的两个分数只留在页面上。",
    "Now four numbers. <bookmark mark='a'/> One: Bloom's tutoring gain was two standard deviati":
        "现在是四个数字。<bookmark mark='a'/>第一：布鲁姆的辅导收益是两个标准差。后来对人类辅导的综述发现了多少？<bookmark mark='b'/>第二：Psyche学习一份单词表，然后复习四次，要么挤在一次学习中，要么分散在四周里。两个月后，两种方式下它分别能回忆多少？<bookmark mark='c'/>第三：在关于绩效反馈的研究中，有多大比例发现反馈让表现变差了？<bookmark mark='d'/>第四：给一整个国家的九年级学生上一节成长型思维课。它对成绩的影响有多大？在这里暂停，把答案写下来。",
    'Chapter two. Retrieval practice.':
        '第2章。提取练习。',
    "Is a test only a measurement? <bookmark mark='a'/> In 2006 Henry Roediger and Jeffrey Karp":
        "测验只是一种测量吗？<bookmark mark='a'/>2006年，亨利·罗迪格和杰弗里·卡皮克让学生阅读一篇短文，然后要么再读一遍，要么在没有反馈的情况下做一次回忆测验。<bookmark mark='b'/>五分钟后，重读的一组领先。<bookmark mark='c'/>一周后，做过测验的一组记得更多。提取会强化它所提取的东西。这就是第21部分的测试效应。<bookmark mark='d'/>这里的柱子是已发表的平均值，为近似值。",
    "Which kind of test? <bookmark mark='a'/> Recall, writing the answer out, does more than re":
        "用哪一种测验？<bookmark mark='a'/>回忆，也就是把答案写出来，比认出答案作用更大，前提是学习者能够做到。<bookmark mark='b'/>当错误选项看起来合理时，选择题依然有效，因为每个选项都要被排除，而那也是提取。<bookmark mark='c'/>甚至在学习之前做测验也有帮助。先猜错，再读到答案，胜过只读。林赛·里奇兰及其同事在2009年证明了这一点。<bookmark mark='d'/>不管用的是太难而答不出、又从未被纠正的测验。提取需要成功，或者需要反馈。",
    "And in classrooms? <bookmark mark='a'/> Short, frequent, low-stakes quizzes improve later ":
        "那么在课堂上呢？<bookmark mark='a'/>简短、频繁、低风险的小测验能提高之后的考试成绩，在初中和大学都是如此。<bookmark mark='b'/>当错误答案事后得到纠正时，提取的帮助最大。<bookmark mark='c'/>被测过的事实会被记住。向新问题的迁移较小，但当小测验要求应用时，迁移是存在的。<bookmark mark='d'/>学生之所以不这样做，是因为测验感觉像失败，而重读感觉像学习。",
    'Chapter three. Spacing and interleaving.':
        '第3章。间隔与交错。',
    "Part 21 found spacing's ridgeline. Here it is again, as a design rule. <bookmark mark='a'/":
        "第21部分找到了间隔效应的山脊线。这里它再次出现，作为一条设计规则。<bookmark mark='a'/>Psyche学习一遍，隔一段时间再学一遍，之后接受测验。<bookmark mark='b'/>如果测验在一周之后，最佳间隔是两三天。如果测验在一年之后，最佳间隔是三个月或更长。<bookmark mark='c'/>间隔太长的代价很小，间隔太短的代价很大。<bookmark mark='d'/>所以要按你需要用到这些知识的日期来安排复习，而不是按下一次小测验。",
    "Interleaving is spacing's cousin. <bookmark mark='a'/> Blocked practice is ten problems of":
        "交错是间隔的近亲。<bookmark mark='a'/>分块练习是先做十道同一类型的题，再做十道下一类型的。交错练习则把它们混在一起。<bookmark mark='b'/>2007年，道格·罗勒和凯莉·泰勒发现，练习计算立体体积的学生，在分块练习时做得更好，但一周后比交错练习的学生差得多。<bookmark mark='c'/>交错迫使学习者自己选择方法，而这正是考试和生活会要求的。分块练习则直接告诉了他们。<bookmark mark='d'/>一项数学课堂试验在一个月后发现了收益。<bookmark mark='e'/>当类别容易混淆时它帮助最大。对于差别很大的主题，收益很小。",
    'Chapter four. Learning against performance.':
        '第4章。学习与表现之别。',
    "Why does the better method feel worse? <bookmark mark='a'/> Psyche studies once and review":
        "为什么更好的方法感觉更糟？<bookmark mark='a'/>Psyche学习一遍，再复习四次：要么一次做完，要么每周一次。<bookmark mark='b'/>在第五天，突击看起来好得多：超过百分之九十，而间隔学习者只有约百分之三十，它正该复习了。<bookmark mark='c'/>到第六十天，是百分之十四对百分之七十四。<bookmark mark='d'/>罗伯特·比约克和伊丽莎白·比约克把这称为学习与表现之间的差别。练习过程中的表现，是学习效果的糟糕指南，而那些让练习变慢的困难，往往正是让学习持久的困难。他们称之为合意困难。",
    "The trap has a name: the illusion of fluency. <bookmark mark='a'/> Rereading makes the tex":
        "这个陷阱有个名字：流畅性错觉。<bookmark mark='a'/>重读让文本感觉熟悉，而熟悉感觉就像知道。这是第25部分的信心，被误导了。<bookmark mark='b'/>内特·科内尔和罗伯特·比约克发现，大多数学习者认为集中学习画家风格的效果更好，即使他们从交错学习中学到的更多。<bookmark mark='c'/>路易斯·德斯劳里尔斯及其同事发现，物理学学生在主动学习的课堂上学到的更多，却认为这些课教给他们的更少。<bookmark mark='d'/>在两百二十五项研究中，斯科特·弗里曼及其同事发现，传统讲授课堂上的学生不及格的可能性，约为主动学习课堂的一点五倍。<bookmark mark='e'/>所以需要用他们自己身上的证据告诉学习者：难的方法才有效。这正是在你身上做的那个实验的用意。",
    'Chapter five. Ten techniques, ranked.':
        '第5章。十种学习技巧，排个名次。',
    'In 2013 John Dunlosky and colleagues rated ten study techniques by their evidence. <bookma':
        "2013年，约翰·邓洛斯基及其同事按证据给十种学习技巧打分。<bookmark mark='a'/>两种获得高效用：练习测验和分散练习。<bookmark mark='b'/>三种获得中等效用：精细化提问，即追问一个事实为什么成立；自我解释；以及交错练习。<bookmark mark='c'/>五种获得低效用：总结、划重点、关键词记忆法、为文本构建意象，以及重读。<bookmark mark='d'/>效用的评判依据是每种技巧在不同学习者、材料、任务和时间间隔上的推广程度，以及来自真实课程的证据。最受欢迎的两种技巧，划重点和重读，排在最后。",
    "Why do the top two work? <bookmark mark='a'/> Retrieval: each successful recall makes the ":
        "为什么排在前两位的有效？<bookmark mark='a'/>提取：每一次成功的回忆都让记忆以后更容易被提取，并暴露出哪些东西还不知道。<bookmark mark='b'/>间隔：在有一些遗忘之后复习，比在记忆还新鲜时复习作用更大，这正是第21部分的模型所预测的。<bookmark mark='c'/>二者合起来就是间隔提取练习：在数周内反复使用的抽认卡，以及累积式小测验。<bookmark mark='d'/>代价是二者都感觉缓慢而费力，而流畅性错觉指向相反的方向。",
    'Chapter six. Cognitive load.':
        '第6章。认知负荷。',
    "John Sweller's cognitive load theory starts from Part 19. <bookmark mark='a'/> Working mem":
        "约翰·斯威勒的认知负荷理论从第19部分出发。<bookmark mark='a'/>对于新材料，工作记忆一次只能容纳几个元素。<bookmark mark='b'/>内在负荷是材料要求学习者同时把握的元素数量。<bookmark mark='c'/>外在负荷是教学本身附加的：图在这里，图的标注却在那边，或者没有指导的搜索。<bookmark mark='d'/>设计目标是削减外在负荷，让工作记忆用在材料上：样例、直接标在图上的标注，以及文字和图像各用一个通道。",
    "Here is the theory as a budget, drawn schematically. <bookmark mark='a'/> A novice solving":
        "这里把理论画成一份预算，是示意图。<bookmark mark='a'/>一个解决新类型问题的新手，必须同时把握目标、已知条件和对方法的搜索。这超出了上限，所以几乎没有剩余容量去学习方法本身。<bookmark mark='b'/>同一个新手学习一道样例时，把握的是步骤，而不是搜索，于是容纳得下。<bookmark mark='c'/>专家已经把方法组块化了，就像第24部分所展示的，所以材料只占大约一个元素，而阅读一道多余的样例是额外的负荷，毫无收获。<bookmark mark='d'/>所以最好的形式取决于学习者已经掌握了什么，随着专长增长，这些柱子会移动。<bookmark mark='e'/>柱子的高度是示意性的。这一理论中的量很少被这样直接地测量，这也是对它的主要批评。",
    "Worked examples show the theory at work. <bookmark mark='a'/> Novices who study solved pro":
        "样例展示了这一理论的作用。<bookmark mark='a'/>学习已解出题目的新手，比自己解同样题目的新手学到更多。<bookmark mark='b'/>但对于已经掌握方法的学习者，样例是多余的，自己解题效果更好。这就是专长逆转效应。<bookmark mark='c'/>所以要逐步撤掉支持：先是完整的样例，然后是部分样例，最后是题目。<bookmark mark='d'/>同一个设计，对不同的学习者却是错的。这是第47部分的问题，出现在课堂上。",
    'Chapter seven. Myths.':
        '第7章。迷思。',
    "Do people learn best in their own style? <bookmark mark='a'/> The meshing hypothesis says ":
        "人们在自己的风格下学得最好吗？<bookmark mark='a'/>匹配假设认为，按学习者偏好的风格施教能改善学习。<bookmark mark='b'/>2008年，哈罗德·帕什勒、马克·麦克丹尼尔、道格·罗勒和罗伯特·比约克阐明了检验它所需的条件：这种交叉，即每种风格都从自己的方法中学得最好。<bookmark mark='c'/>在少数采用这种设计的研究中，几乎没有一项发现它，还有几项发现了相反的模式，或者什么也没发现。<bookmark mark='d'/>人们确实有偏好。按偏好施教却没有帮助。决定形式的是内容：地图是视觉的，诗歌是要听的。",
    "Other myths fare no better. <bookmark mark='a'/> People aren't left-brained or right-brain":
        "其他迷思也好不到哪里去。<bookmark mark='a'/>人并不分左脑型学习者和右脑型学习者。两个半球几乎参与所有事情，就像第7部分展示的那样。<bookmark mark='b'/>我们也不是只用了百分之十的大脑。成像显示，一天之中几乎所有脑区都会活跃。<bookmark mark='c'/>笔记本电脑做笔记是一个更接近的案例。一项研究发现，在概念性问题上，手写笔记胜过电脑笔记，而一项预注册的重复研究没有发现可靠的差异。账本称之为存在争议。<bookmark mark='d'/>迷思之所以长存，是因为它们讨好了学习者和教师，而没有人去做交叉检验。",
    'Chapter eight. Tutoring.':
        '第8章。辅导。',
    "How big is the tutoring effect, really? <bookmark mark='a'/> Bloom's two sigma came from a":
        "辅导效应到底有多大？<bookmark mark='a'/>布鲁姆的二西格玛来自几项短期研究，所用的测验与课程内容对齐。<bookmark mark='b'/>库尔特·范莱恩2011年的综述发现，人类辅导约为零点八，而对解题每一步都作出回应的计算机辅导系统几乎同样好。<bookmark mark='c'/>安德烈·尼科、菲利普·奥雷奥普洛斯和文森特·关2020年对学校辅导随机试验的综述发现，平均约为零点四，由教师和助教在上课时间进行的辅导效果最大。<bookmark mark='d'/>这仍然是教育中最大的效应之一。账本记作：已重复，但效应较小。",
    "How does a tutoring system model the learner? <bookmark mark='a'/> The inner loop gives fe":
        "辅导系统如何为学习者建模？<bookmark mark='a'/>内循环对一道题的每一步给出反馈和提示，就像一位好的人类辅导老师那样。<bookmark mark='b'/>外循环选择下一道题，用第45部分的知识追踪来估计每项技能的掌握程度。<bookmark mark='c'/>掌握学习在估计值超过约零点九五时才继续往前，而不是在时间用完时。<bookmark mark='d'/>它做不到的是激励学生、从表情中察觉困惑，或者建立关系，而人类辅导老师的效果，可能有很大一部分就在这里。",
    'Chapter nine. Scheduling reviews.':
        '第9章。安排复习。',
    "Spaced repetition began with boxes. <bookmark mark='a'/> In Sebastian Leitner's system of ":
        "间隔重复始于几个盒子。<bookmark mark='a'/>在塞巴斯蒂安·莱特纳20世纪70年代的系统里，一张抽认卡被回忆出来就升入上一个盒子，没回忆出来就退回第一个盒子，而越高的盒子复习得越少。<bookmark mark='b'/>1987年，彼得·沃兹尼亚克的SM-2算法在每次复习后，把每张卡片的间隔乘以一个难易系数。它至今仍运行在许多抽认卡应用中。<bookmark mark='c'/>2016年，伯尔·塞特尔斯和布伦丹·米德用数百万学习者的复习记录拟合了半衰期回归，预测每个单词的半衰期，正如第21部分所展示的。<bookmark mark='d'/>而前沿把它当作最优控制问题：在一个记忆模型下，选择复习时间，使需要时能记住的东西最多。",
    "Here are four schedules, raced on Psyche at equal study time. <bookmark mark='a'/> Sixty i":
        "这里是四种复习安排，在学习时间相等的条件下，在Psyche身上比赛。<bookmark mark='a'/>六十个项目在第零天学习，每个项目在第二十八天之前复习四次，测验在第六十天。<bookmark mark='b'/>全部挤在一次学习中，回忆率是百分之十七。<bookmark mark='c'/>间隔逐渐拉长，是百分之六十七。间隔相等，是百分之七十一。在很长的延迟之后，逐渐拉长并不更好，杰弗里·卡皮克和亨利·罗迪格也发现了这一点。<bookmark mark='d'/>模型的选择，也就是使第六十天预测回忆率最高的安排，表现与等间隔差不多，它的间隔越到后面越短。<bookmark mark='e'/>最要紧的是有没有间隔。安排的形状没那么重要，而且取决于测验日期。",
    "But best on the test day isn't the only goal. <bookmark mark='a'/> Here are the same four ":
        "但测验当天最好并不是唯一的目标。<bookmark mark='a'/>这里是同样的四种安排，针对一个项目，每天都跟踪，而不是只看第六十天。<bookmark mark='b'/>集中学习在六十天中只有大约十七天保持在一半以上。<bookmark mark='c'/>逐渐拉长的间隔让它六十天都保持在一半以上，因为早期的复习赶在第一次遗忘之前。<bookmark mark='d'/>模型的安排是为第六十天选的，它让回忆率在早期下滑，大约五十二天在一半以上。<bookmark mark='e'/>只考一次试的学习者想要最后一种。护士或飞行员可能在任何一天需要用到这个知识，想要的是第二种。目标决定安排。",
    "More reviews, or better-placed ones? <bookmark mark='a'/> Massed, even eight reviews in on":
        "更多的复习，还是位置更好的复习？<bookmark mark='a'/>集中学习，即使在一次学习中复习八遍，也只能达到约四分之一。<bookmark mark='b'/>间隔学习，四周后复习一次就已经达到百分之四十。<bookmark mark='c'/>一次复习放在哪里，比复习多少次更有价值。<bookmark mark='d'/>对于一个每周只有一小时的学习者，调度器的工作就是把这一小时花在即将遗忘的地方。",
    'Chapter ten. Learning to read.':
        '第10章。学习阅读。',
    "Why did the reading wars end? Start with a model. <bookmark mark='a'/> In 1986 Philip Goug":
        "阅读之争为什么结束了？从一个模型说起。<bookmark mark='a'/>1986年，菲利普·高夫和威廉·滕默提出，阅读理解是单词解码与语言理解的乘积。只要其中一个为零，阅读也就为零。<bookmark mark='b'/>这里是四百名模拟儿童，按理解程度着色。听力好却不会解码的孩子，读得和解码好却不理解的孩子差不多一样差。<bookmark mark='c'/>这是两个不同的问题，需要两种不同的教学：一种需要自然拼读，另一种需要词汇和知识。",
    "For decades, the reading wars were fought between two views. <bookmark mark='a'/> Whole-la":
        "几十年来，阅读之争在两种观点之间展开。<bookmark mark='a'/>全语言教学认为，孩子学阅读就像学说话一样，从意义和语境中学会。<bookmark mark='b'/>证据表明，英语拼写与发音的对应足够系统，明确而系统的自然拼读教学对初学者有帮助，对有风险的孩子帮助最大。美国国家阅读小组在2000年得出了这一结论。<bookmark mark='c'/>作为一种策略来教的、根据图画和语境猜词，训练的恰恰是熟练读者不做的事。第18部分的眼动几乎落在每一个词上。<bookmark mark='d'/>安妮·卡斯尔斯、凯瑟琳·拉斯特尔和凯特·内申在2018年作了总结：先教自然拼读，再培养流畅性、词汇和知识。解码是必要的，但不是充分的。",
    'Chapter eleven. Beliefs about ability.':
        '第11章。关于能力的信念。',
    "Can a lesson about the brain change grades? <bookmark mark='a'/> The idea is that students":
        "一节关于大脑的课能改变成绩吗？<bookmark mark='a'/>这个想法是：相信能力可以增长的学生在挫折后更能坚持，而一节短课就能教会这种信念。<bookmark mark='b'/>早期的小型研究报告了很大的效应；第一根柱子是示意性的。维多利亚·西斯克及其同事2018年的元分析发现，对学业成绩的效应约为零点零八。<bookmark mark='c'/>随后，戴维·耶格尔及其同事为大约一万两千名美国九年级学生开设了一节五十分钟的在线课程，并进行了随机分配。成绩较低的学生的成绩提高了约十分之一个绩点，总体上变化不大。<bookmark mark='d'/>小，真实，而且便宜。对于一节不到一小时的课，账本记作：已重复，但效应较小。",
    "For whom, and where? <bookmark mark='a'/> The national study found the effect only in scho":
        "对谁有效，在哪里有效？<bookmark mark='a'/>这项全国性研究只在同伴规范支持迎接挑战的学校中发现了效应。这节课需要肥沃的土壤。<bookmark mark='b'/>异质性本身就是发现，而不是脚注。零点零八的平均值，可能掩盖了一些人的零点二和大多数人的零，这正是第47部分的观点。<bookmark mark='c'/>风险在于，“表扬努力”变成一句口号，却没有课程的内容。<bookmark mark='d'/>所以要按一项干预的大小、对谁有效、成本多少、与什么替代方案相比来解读它。",
    'Chapter twelve. Feedback.':
        '第12章。反馈。',
    "Does feedback always help? <bookmark mark='a'/> In 1996 Avraham Kluger and Angelo DeNisi p":
        "反馈总是有帮助吗？<bookmark mark='a'/>1996年，亚伯拉罕·克鲁格和安杰洛·德尼西汇总了六百多个关于反馈对绩效影响的效应。<bookmark mark='b'/>平均效应是正的，约为零点四个标准差。<bookmark mark='c'/>但在超过三分之一的比较中，反馈让表现变差了。<bookmark mark='d'/>把注意力引向自我的反馈，即对人的表扬或批评，往往有害。关于任务、关于如何改进的反馈，往往有帮助。<bookmark mark='e'/>同一个词，指的是效果相反的干预。",
    'What should the feedback say? <bookmark mark=\'a\'/> After a wrong answer, being told "wrong':
        "反馈应该说些什么？<bookmark mark='a'/>答错之后，只被告知“错了”作用不大，因为学习者仍然不知道正确答案。哈罗德·帕什勒及其同事在2005年发现了这一点。<bookmark mark='b'/>有帮助的是正确答案，而当任务需要理解而不只是回忆时，解释的帮助最大。<bookmark mark='c'/>在以低信心答对之后，反馈也有帮助。安德鲁·巴特勒、杰弗里·卡皮克和亨利·罗迪格证明，它能把一次猜测变成真正知道的东西。<bookmark mark='d'/>而令人意外的是，以高信心犯下的错误纠正得最好。意外标记了它们，就像第17部分的预测误差。",
    "So what does feedback that works look like? <bookmark mark='a'/> It's about the task: what":
        "那么，有效的反馈是什么样子的？<bookmark mark='a'/>它关于任务：什么是对的，要改变什么，下一步是什么。<bookmark mark='b'/>它是及时的，趁尝试还留在记忆里。对于提取练习，那就是答完之后立刻反馈。<bookmark mark='c'/>它会被付诸行动，有再试一次的机会。没有第二次尝试的反馈，是没有练习的信息。<bookmark mark='d'/>而且它不只是一个分数。分数告诉你站在哪里，而不是如何改进。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    "Five new rows; testing and spacing are Part 21's. The first: mixing problem types during p":
        "五个新条目；测试和间隔是第21部分的。第一条：在练习中混合不同题型能提高之后的表现，尽管分块练习在学习过程中看起来更好。<bookmark mark='a'/>原始研究：罗勒与泰勒，2007年。<bookmark mark='b'/>记录：一项数学课堂试验，以及一项发现类别容易混淆时收益最大的元分析。<bookmark mark='c'/>它的作用方式是迫使学习者选择方法。<bookmark mark='d'/>已重复。",
    "The second: teaching matched to a learner's preferred style improves learning. <bookmark m":
        "第二条：按学习者偏好的风格施教能改善学习。<bookmark mark='a'/>原始来源：邓恩夫妇1978年为教师提出的模型。<bookmark mark='b'/>记录：帕什勒及其同事对交叉检验的综述，以及一项没有发现交互作用的直接检验。<bookmark mark='c'/>偏好是真实的；按偏好匹配没有帮助。<bookmark mark='d'/>失败。",
    'The third: one-to-one tutoring raises achievement by about two standard deviations. <bookm':
        "第三条：一对一辅导能把学业成绩提高约两个标准差。<bookmark mark='a'/>原始研究：布鲁姆，1984年。<bookmark mark='b'/>记录：范莱恩的综述约为零点八，学校随机试验约为零点四。<bookmark mark='c'/>仍然是教育中最大的效应之一。<bookmark mark='d'/>已重复，但效应较小。",
    "The fourth: teaching students that ability can grow improves achievement. <bookmark mark='":
        "第四条：教导学生能力可以增长，能提高学业成绩。<bookmark mark='a'/>原始研究：布莱克韦尔、特热斯涅夫斯基和德韦克，2007年。<bookmark mark='b'/>记录：一项元分析约为零点零八，以及一项全国性试验，在支持性的学校中对成绩较低的学生有效。<bookmark mark='c'/>小、便宜，而且因人而异。<bookmark mark='d'/>已重复，但效应较小。",
    'And the fifth: students who take notes by hand learn more than those who type. <bookmark m':
        "第五条：手写笔记的学生比打字的学生学得更多。<bookmark mark='a'/>原始研究：穆勒和奥本海默，2014年。<bookmark mark='b'/>记录：一项预注册的重复研究和一项多中心研究，都没有发现可靠的优势。<bookmark mark='c'/>打字的人逐字记录得更多；这是否会损害学习，尚未确定。<bookmark mark='d'/>存在争议。",
    "What the five have in common. <bookmark mark='a'/> The techniques built on memory research":
        "这五条有什么共同点。<bookmark mark='a'/>建立在记忆研究之上的技巧，交错练习，就像测试和间隔一样，站住了。<bookmark mark='b'/>流行的观念，学习风格和手写笔，要么失败，要么摇摆，而那些著名的数字，二西格玛和思维模式，都缩水了。<bookmark mark='c'/>学习者自己的判断指向错误的方向，因为流畅感觉就像在学习。<bookmark mark='d'/>所以这就是这一部分问题的答案。最有效的学习方法感觉更难，这正是学习者选择相反做法的原因。",
    "Chapter fourteen. In practice: a course's study plan, redesigned.":
        '第14章。实践中：重新设计一门课的学习计划。',
    "Where is this a job? <bookmark mark='a'/> In course design: curricula with cumulative revi":
        "这在哪里是一份工作？<bookmark mark='a'/>在课程设计中：包含累积复习的课程体系，以及要求提取和应用的考核。<bookmark mark='b'/>在教育技术中：抽认卡和辅导产品，它们的调度器和学生模型就是这一部分的数学。<bookmark mark='c'/>在企业培训中，一天的工作坊就是集中练习，把它分散开来花费不多，留下的却更多。<bookmark mark='d'/>还有在评估中：对产品和项目的随机试验，以之后的学习来评判，而不是以学习者感觉多满意来评判。",
    "Here's a worked redesign of a twelve-week statistics course. <bookmark mark='a'/> Before: ":
        "这里是一门为期十二周的统计学课程的重新设计实例。<bookmark mark='a'/>之前：讲课，每周一份关于当周主题的习题，一次期中考试和一次期末考试，学生在考前重读幻灯片。<bookmark mark='b'/>提取：每次课开始时做一个五道题的小测验，低风险，并讨论答案。<bookmark mark='c'/>间隔：每份习题都包含两道三周前和六周前的题目，期末考试是累积的，并事先说明。<bookmark mark='d'/>交错：每份习题的最后三分之一混合了不同种类的检验，不加标签，因为选择检验方法本身就是技能。<bookmark mark='e'/>负荷：先给样例，逐步过渡到补全题，再到完整的题目。<bookmark mark='f'/>评估：一个学期后对同样的题目做延迟测验，与去年的学生比较，并告诉学生为什么这门课感觉更难。",
    'Chapter fifteen. Frontier: AI tutors and what transfers.':
        '第15章。前沿：AI辅导与能迁移的东西。',
    "Will a machine tutor close the two sigma? <bookmark mark='a'/> Conversational tutors built":
        "机器辅导能弥合二西格玛的差距吗？<bookmark mark='a'/>基于语言模型的对话式辅导可以覆盖每一个学生。早期的随机试验结果不一，设计的细节很重要。<bookmark mark='b'/>这里有一个拐杖问题。用助手来回答练习题的学生，可能在练习中做得更好，而在之后没有助手的测验中做得更差。这又是表现与学习之别。<bookmark mark='c'/>被设计成给提示而不是给答案的辅导系统，目的是保留合意困难。<bookmark mark='d'/>调度器正在从数百万次复习中学习出来，应该通过随机比较来评判。",
    "And the open problems. <bookmark mark='a'/> Transfer: what learning carries to new problem":
        "还有那些悬而未决的问题。<bookmark mark='a'/>迁移：什么样的学习能带到新的问题和新的情境中，以及如何为迁移而教。<bookmark mark='b'/>动机：如果学习者半途而废，最好的技巧也会失败，那么怎样让有效的学习成为人们愿意选择的学习？<bookmark mark='c'/>规模：为什么效应从试点到系统推广时会缩小，以及如何阻止它。<bookmark mark='d'/>还有测量：测量持久学习的测验，而不是测量当天表现的测验。",
    "First, your four numbers. <bookmark mark='a'/> Later reviews put human tutoring at about z":
        "先看你的四个数字。<bookmark mark='a'/>后来的综述把人类辅导定在约零点八个标准差，学校试验约为零点四。Psyche的突击复习在第六十天只剩百分之十七，间隔复习是百分之七十一。超过三分之一的反馈研究发现表现变差了。而全国性的思维模式课程让一些学生的成绩提高了约十分之一个绩点。<bookmark mark='b'/>感觉像学习的，和真正产生学习的，指向相反的方向。",
    "Part fifty-four in twelve lines. <bookmark mark='a'/> Two sigma became about half a sigma,":
        "第五十四部分，十二句话。<bookmark mark='a'/>二西格玛变成了约半个西格玛，而这仍然很大。测验本身就是一次学习。按需要用到的日期安排复习。交错练习容易混淆的题目。练习中的表现会误导人。测试和间隔在十种技巧中名列前茅。削减外在负荷，并逐步撤掉样例。学习风格没能通过交叉检验。辅导系统在内外两个循环中为学习者建模。复习放在哪里，胜过复习多少次。阅读需要解码和理解。思维模式和反馈的效应很小，只对一部分人有效，有时还是负的。",
    "Where this comes back. <bookmark mark='a'/> Interventions that shrink at scale are Part 55":
        "这些内容会在哪里再出现。<bookmark mark='a'/>规模一大就缩水的干预，是第55部分的主题。记忆在第56部分走上法庭。学习的机器与学习的心智在第60部分相遇。而第62部分的学位论文可以恰当地检验一项学习干预。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads ":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道解读山脊线。一道编写复习安排。一道应用阅读简单观。一道计算一个小效应所需的样本量。一道在答错后更新知识追踪。一道设计学习风格的检验。最后带星号的一道，请你重新设计一门你熟悉的课程。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Make It Stick is ':
        '这一部分所依据的书籍和论文列在这里，也列在README中。《认知天性》（Make It Stick）是写给学习者的最好的短书；邓洛斯基及其同事的综述把证据集中在一处；比约克夫妇的章节解释了合意困难。',
    "Four parts of Act Twelve are done. <bookmark mark='a'/> This one turned memory research in":
        "第十二幕的四部分已经完成。<bookmark mark='a'/>这一部分把记忆研究变成了工程，并发现学习者在往反方向用力。<bookmark mark='b'/>下一部分从课堂扩大到整个国家。为什么助推离开实验室就会缩水？第55部分：大规模行为改变。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
