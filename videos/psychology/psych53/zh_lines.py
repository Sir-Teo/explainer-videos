"""Chinese narration for psych53: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第53部分：工作中的人'

CHAPTERS = {
    'Hook': '霍桑的灯光',
    'Predict': '1. 在你身上：两位候选人，以及四个数字',
    'History': '2. 测试一个国家',
    'Validity': '3. 效度与效标',
    'Corrections': '4. 为什么观测到的效度会误导人',
    'Century': '5. 一个世纪的证据，被修订了',
    'Interviews': '6. 面试',
    'Utility': '7. 从相关到金钱',
    'Fairness': '8. 公平',
    'Algorithms': '9. 招聘中的算法',
    'Goals': '10. 目标',
    'Pay': '11. 薪酬，以及金钱挤出了什么',
    'Teams': '12. 满意度、团队与人们在哪里工作',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：设计一套选拔系统',
    'Frontier': '15. 前沿：新的测评，老的问题',
    'Outro': '回顾、习题与前路',
}

ZH = {
    "Every course on psychology at work begins with the same story. <bookmark mark='a'/> From 1":
        "每一门讲工作中心理学的课程都以同一个故事开头。<bookmark mark='a'/>从1924年到1927年，在芝加哥附近西方电气公司的霍桑工厂，工程师们改变了工人组装电话零件的房间里的照明。<bookmark mark='b'/>按照这个故事的说法，他们把灯调亮，产量上升；把灯调暗，产量又上升了。<bookmark mark='c'/>得出的教训是：工人回应的是被关注、被关心，而不是工作条件。<bookmark mark='d'/>后来在这家工厂进行的研究，由弗里茨·勒特利斯伯格和威廉·迪克森在1939年写成报告，使它成为工作中人际关系学说的奠基传说。<bookmark mark='e'/>“霍桑效应”也进入了每一本方法教科书，包括第2部分。",
    "What do the data actually show? <bookmark mark='a'/> The illumination studies were never p":
        "数据实际上显示了什么？<bookmark mark='a'/>照明研究从未被正式发表，其数据一度被认为已经遗失。<bookmark mark='b'/>2011年，经济学家史蒂文·莱维特和约翰·李斯特找到了原始的产量记录并加以分析。<bookmark mark='c'/>在实验期间产量确实上升了，但它也随季节上升，而且照明的变化总是落在周末之后的星期一。<bookmark mark='d'/>数据中霍桑效应的证据很微弱。那个著名的“上升了又上升”大多来自后来的复述。<bookmark mark='e'/>工作心理学真正的历史没那么浪漫，却更有用。它关乎能做出预测的数字。",
    "So this part asks: how well can anyone predict who will be good at a job? <bookmark mark='":
        "所以这一部分要问：谁能在多大程度上预测一个人会把一份工作做好？<bookmark mark='a'/>效度：一种方法与后来表现之间的相关，以及它们为什么会误导人。<bookmark mark='b'/>一个世纪的证据，以及它在2022年的修订。<bookmark mark='c'/>金钱、公平与算法。<bookmark mark='d'/>还有目标、薪酬、团队，以及人们在哪里工作。",
    "This is Part 53 of Psychology, Built: people at work. <bookmark mark='a'/> We'll define va":
        "这是《心理学，从零搭建》的第53部分：工作中的人。<bookmark mark='a'/>我们将定义效度，并直面“工作表现究竟如何测量”这个问题。我们将看到不可靠性和全距限制如何掩盖效度，以及校正如何可能过头。我们将追问，在2022年的修订之后，哪些招聘方法具有预测力。我们将把一个相关系数变成金钱。我们将计算不利影响，以及效度与多样性之间的边界。我们还将审视目标、激励、金钱挤出了什么、团队，以及居家办公。",
    'Chapter one. On you: two candidates, and four numbers.':
        '第1章。在你身上：两位候选人，以及四个数字。',
    "First, a choice. <bookmark mark='a'/> Two candidates. A has the much better test score and":
        "首先，做一个选择。<bookmark mark='a'/>两位候选人。A的测验分数高得多，面试礼貌但相当平淡。B的分数低得多，面试热情、自信、令人难忘。你雇谁？<bookmark mark='b'/>大多数人倾向于B。面试感觉像是证据。<bookmark mark='c'/>在Psyche的世界里，用这一部分将要论证的效度，在一千对这样的候选人中，A表现更好的占百分之五十七。<bookmark mark='d'/>不是十拿九稳。即使是更好的预测指标，也有大部分表现解释不了。这就是这一部分的数字的真实大小。",
    "Now four numbers. <bookmark mark='a'/> One: a test that truly correlates zero point five w":
        "现在是四个数字。<bookmark mark='a'/>第一：一项与工作表现的真实相关为零点五的测验。在已经用它录用的人当中，你会观察到多大的相关？<bookmark mark='b'/>第二：在2022年对招聘方法的综述中，哪一种单一方法表现最好，它的效度是多少？<bookmark mark='c'/>第三：在所有申请人中有一半能胜任的情况下，你用一项效度为零点三的测验录用前五分之一。你录用的人中有多大比例能胜任？<bookmark mark='d'/>第四：一家托儿所开始对晚接孩子的家长罚款。晚接的情况会怎样？在这里暂停，把它们写下来。",
    'Chapter two. Testing a nation.':
        '第2章。测试一个国家。',
    "Psychology at work began before the tests. <bookmark mark='a'/> Frederick Taylor's scienti":
        "工作中的心理学在测验之前就开始了。<bookmark mark='a'/>弗雷德里克·泰勒的科学管理为每个动作计时，寻找唯一最佳的方法，并按件计酬。<bookmark mark='b'/>1913年，雨果·闵斯特伯格把实验室心理学应用于工作，为有轨电车司机和电话接线员设计测验。<bookmark mark='c'/>弗兰克和莉莲·吉尔布雷斯研究动作，莉莲·吉尔布雷斯还关注疲劳和工人本身。<bookmark mark='d'/>但他们当时都还说不出一项测验能在多大程度上预测谁会把工作做好。",
    "Then came a war. <bookmark mark='a'/> It's Part 32's story. When the United States entered":
        "然后来了一场战争。<bookmark mark='a'/>这是第32部分的故事。美国参加第一次世界大战时，罗伯特·耶基斯的委员会编制了团体测验：给能读英语的新兵用的阿尔法测验，给不能读的人用的贝塔测验。<bookmark mark='b'/>大约一百七十五万名新兵接受了测验，这是第一次大规模测验。<bookmark mark='c'/>测验把人分配到不同的岗位和军官培训中。后来用它们给各民族群体排序，则是糟糕的科学和更糟糕的政策。<bookmark mark='d'/>战后，测验进入了工业界，人事心理学开始用相关系数来追问这一部分的问题。",
    'Chapter three. Validity and the criterion.':
        '第3章。效度与效标。',
    "What does it mean for a test to predict a job? <bookmark mark='a'/> Criterion-related vali":
        "一项测验能预测一份工作，这是什么意思？<bookmark mark='a'/>效标关联效度是一个预测指标（一项测验或一次面试）与一个效标（通常是后来的表现）之间的相关。<bookmark mark='b'/>这是Psyche的申请人。测验的真实效度是零点五，以上司评分为效标时，观测到的相关约为零点三九。<bookmark mark='c'/>对心理学来说，零点五的相关已经很大了，却仍是一团很宽的点云。许多高分者表现不佳，反之亦然。<bookmark mark='d'/>预测性设计先测试申请人，然后等待。同时性设计测试现有员工，成本更低，但会对第4章的校正产生影响。",
    "And then there's the criterion problem. <bookmark mark='a'/> What is performance? Output, ":
        "然后是效标问题。<bookmark mark='a'/>什么是表现？产出、质量、帮助同事、不造成伤害。研究者区分任务绩效、周边绩效和反生产行为。<bookmark mark='b'/>谁来评定？通常是一位上司，一年一次。<bookmark mark='c'/>在史蒂文·斯卡伦、迈克尔·芒特和梅纳德·戈夫对多评价者反馈的分析中，评分方差中属于评分者的部分多于属于被评者的部分。<bookmark mark='d'/>两位上司对同一批人的评分一致性约为零点五。这就是第3部分的衰减，被内置在每一个效度之中。",
    'Chapter four. Why observed validities mislead.':
        '第4章。为什么观测到的效度会误导人。',
    "Why does a good test look weak among the people it hired? <bookmark mark='a'/> A company h":
        "为什么一项好的测验在它录用的人当中看起来很弱？<bookmark mark='a'/>一家公司根据测验录用前五分之一，只观察这些人的表现。<bookmark mark='b'/>在被录用者中，测验分数的离散不到申请人的一半，观测到的相关降到零点一九。<bookmark mark='c'/>测验仍然有效。被录用的人平均更好。但在那窄窄的一片里，相关无法显示这一点。<bookmark mark='d'/>所以公司越挑剔，它自己的测验看起来就越弱。这是好测验被弃用的原因之一。",
    "Two corrections, applied in order, can undo the damage. <bookmark mark='a'/> First, criter":
        "两种校正按顺序进行，可以消除这种损害。<bookmark mark='a'/>首先是效标的不可靠：除以在职者中评分信度的平方根。得到零点二五。<bookmark mark='b'/>然后是全距限制。桑代克的第二种情形公式利用申请人离散与录用者离散之比，得到零点四九。<bookmark mark='c'/>申请人中的真值是零点五。做对了，校正就能恢复它。<bookmark mark='d'/>但如果用错了比例或用错了信度，它们同样可能校正过头。这是下一章的故事。",
    'Chapter five. A century of evidence, revised.':
        '第5章。一个世纪的证据，被修订了。',
    "Which hiring methods predict, and how well? <bookmark mark='a'/> In 1998 Frank Schmidt and":
        "哪些招聘方法有预测力，有多强？<bookmark mark='a'/>1998年，弗兰克·施密特和约翰·亨特总结了八十五年的研究。能力测验和工作样本测验的效度接近零点五。<bookmark mark='b'/>2022年，保罗·萨基特及同事按研究设计逐一重做了全距限制校正。<bookmark mark='c'/>几乎每一个估计值都下降了，能力测验降得最多，降到约零点三。结构化面试现在以约零点四位居榜首。<bookmark mark='d'/>排名的变化小于大小的变化。结构化、工作知识，以及工作本身的样本，仍然领先。",
    "How does a correction overshoot? <bookmark mark='a'/> The old practice corrected every stu":
        "校正是怎样过头的？<bookmark mark='a'/>旧的做法用一个从别处借来的典型比例，对每一项研究都做全距限制校正。<bookmark mark='b'/>但大多数效度研究是同时性的。在职者从未按所研究的测验被挑选过，所以他们的全距几乎没有受到限制。<bookmark mark='c'/>在Psyche中，一项没有全距限制的研究观测到零点三九。借来的校正把它抬到零点七八，而真值是零点五。<bookmark mark='d'/>校正是关于数据如何被过滤的一个模型。模型错了，它就会增加偏差而不是消除偏差。这是第50部分的道理，用在了招聘上。",
    'Chapter six. The interview.':
        '第6章。面试。',
    "Why does a conversation feel so informative? <bookmark mark='a'/> In Psyche's model, an un":
        "为什么一次谈话感觉信息量这么大？<bookmark mark='a'/>在Psyche的模型中，非结构化面试看到了某种真实的东西，却埋在第一印象、融洽感和面试官自己的偏好之中。它的效度约为零点一八。<bookmark mark='b'/>一个把这种印象看得比测验更重的招聘者，表现会比只用测验略差。<bookmark mark='c'/>杰森·达纳、罗宾·道斯和纳撒尼尔·彼得森在2013年发现，面试官即使从回答完全随机的面试中也会形成自信的印象，而且宁愿有这样的面试也不愿没有面试。<bookmark mark='d'/>同样的信息按固定规则组合，预测得最好。这就是第39部分的精算预测，用在了工作中。",
    "Structure is the fix, and it's well understood. <bookmark mark='a'/> Base the questions on":
        "结构化是解决办法，而且已经被理解得很透彻。<bookmark mark='a'/>根据工作分析，也就是这份工作实际需要什么，来设计问题。<bookmark mark='b'/>给每位候选人同样的问题，按同样的顺序，询问过去的行为或可能面对的情境。<bookmark mark='c'/>对照事先写好的差、中、好答案的例子给每个回答评分。<bookmark mark='d'/>还要用几位独立的评分者，在任何人讨论候选人之前，按规则取平均。斯科特·海豪斯把对这一切的抗拒称为对直觉的顽固依赖。",
    'Chapter seven. From a correlation to money.':
        '第7章。从相关到金钱。',
    "What is a validity of zero point three worth? <bookmark mark='a'/> In 1939 H. C. Taylor an":
        "零点三的效度值多少？<bookmark mark='a'/>1939年，H. C. 泰勒和J. T. 拉塞尔用表格回答了这个问题。假设所有申请人中有一半能胜任，你用效度为r的测验录用其中一部分。<bookmark mark='b'/>效度为零点三、录用前五分之一时，百分之六十七的录用者能胜任，而随机录用是百分之五十。<bookmark mark='c'/>同一项测验在你能挑剔的时候更有价值。如果你录用十个申请人中的九个，几乎什么都不会改变。<bookmark mark='d'/>当录取比例很小时，一个适中的相关就是实实在在的收益。这些表格在1939年就让这一点显而易见了。",
    'Hubert Brogden, Lee Cronbach and Goldine Gleser turned validity into money. <bookmark mark':
        "休伯特·布罗格登、李·克龙巴赫和戈尔丁·格莱泽把效度变成了金钱。<bookmark mark='a'/>录用N个人、为期T年的收益，等于效度，乘以表现一个标准差的货币价值，乘以录用者在预测指标上高出平均多少，再减去测验成本。<bookmark mark='b'/>取一百个录用者、五年、一个标准差每年值两万、录用申请人的前五分之一、每次测验一百。<bookmark mark='c'/>结构化面试值将近六百万。按2022年估计的能力测验，约四百万。按1998年的估计，本来是七百万。<bookmark mark='d'/>以金钱计的标准差是最不可靠的数字。对一名更好的员工值多少的估计差异很大，所以要把这些钱看作一个量级，而不是一个承诺。",
    'Chapter eight. Fairness.':
        '第8章。公平。',
    "Can a valid test be unfair? <bookmark mark='a'/> Take two groups of applicants and a cut t":
        "一项有效的测验会不公平吗？<bookmark mark='a'/>取两组申请人，以及一条总体录用五分之一的分数线。影响比是得分较低组的录取率除以另一组的录取率。<bookmark mark='b'/>美国的指导原则把低于零点八的比值标记出来，这就是五分之四规则。它是审查的触发点，而不是判决。<bookmark mark='c'/>仅仅零点四个标准差的差异，就会造成百分之十三对百分之二十三的录取率，比值约为零点五五。<bookmark mark='d'/>挑剔的分数线会放大均值上的小差异，因为起作用的是尾部，正如第32部分所示。",
    "The law entered in 1971. <bookmark mark='a'/> In Griggs versus Duke Power, the US Supreme ":
        "法律在1971年介入。<bookmark mark='a'/>在格里格斯诉杜克电力公司案中，美国最高法院裁定，一项排斥黑人工人、又未被证明与工作相关的文凭要求和能力倾向测验不合法。<bookmark mark='b'/>这就是差别影响：一种造成不利影响的做法必须被证明与工作相关，而一个歧视性更小的替代方案可以胜诉。<bookmark mark='c'/>心理学家还会问差别预测：同样的分数在每个群体中预测同样的表现吗？研究大多发现斜率相似，截距的差异则随着效标改进而缩小。<bookmark mark='d'/>所以一项测验可以对每个人都同样有效，却仍然产生不利影响。公平有好几种定义，而且它们相互冲突。第60部分会再谈这个问题。",
    "Organizations can choose where to stand. <bookmark mark='a'/> Take two predictors: an abil":
        "组织可以选择站在哪里。<bookmark mark='a'/>取两个预测指标：一项能力测验，效度零点三一，群体差异零点八个标准差；一次结构化面试，效度零点四二，群体差异零点三。这些输入是示意性的。<bookmark mark='b'/>以各种比例给它们加权。只用面试得到更高的影响比，这里也得到更高的效度；只用测验两者都最低。<bookmark mark='c'/>效度最高的组合给出约零点四二的影响比。站在曲线的哪一点，是由组织的价值观而不是数据选择的权衡。<bookmark mark='d'/>而在2022年的修订之后，这种权衡变得温和了，因为效度最高的预测指标不再是群体差异最大的那些。",
    'Chapter nine. Algorithms in hiring.':
        '第9章。招聘中的算法。',
    "What does a model learn from past hiring? <bookmark mark='a'/> A model trained to predict ":
        "一个模型会从过去的招聘中学到什么？<bookmark mark='a'/>一个被训练来预测谁被录用、或谁得到好评的模型，学到的是那些决策所奖励的任何东西。<bookmark mark='b'/>2018年，有报道称一家大公司的实验性简历筛选系统会给与女性相关的词打低分，这是从十年来以男性为主的录用中学来的。公司放弃了它。<bookmark mark='c'/>这又是效标问题。模型的目标是过去人的判断，而不是表现。<bookmark mark='d'/>而去掉群体标签并不能去掉群体。学校、俱乐部和职业经历中的空档都是代理变量。",
    "So how do you audit an algorithm? <bookmark mark='a'/> Ask the same question as for any te":
        "那么如何审核一个算法？<bookmark mark='a'/>问与任何测验同样的问题：在一个新样本中，这个分数能预测测量良好的表现吗？<bookmark mark='b'/>在真实申请人身上按群体计算录取率和影响比。<bookmark mark='c'/>有些法律现在要求这样做。纽约市自2023年起要求对自动化招聘工具进行年度独立偏差审计。<bookmark mark='d'/>还要告诉候选人使用了某种工具，以及它测量的是什么。",
    'Chapter ten. Goals.':
        '第10章。目标。',
    "Most textbooks still teach two older theories first.":
        "大多数教科书仍然先讲两个更早的理论。<bookmark mark='a'/>1959年，弗雷德里克·赫茨伯格和同事请工程师和会计描述他们对工作感觉特别好"
        "或特别糟的时候。好的时候关乎成就、认可和工作本身；糟的时候关乎薪酬、上司和工作条件。于是赫茨伯格得出结论：两者是分开的，"
        "保健因素只能消除不满，只有激励因素才能激励。<bookmark mark='b'/>换了别的方法，这种划分就站不住了。用同样的方式提问，"
        "人们会把好事归功于自己，把坏事归咎于环境，这就是第35部分的自我服务偏差；用别的测量，两张清单会有重叠。"
        "<bookmark mark='c'/>1964年，维克托·弗鲁姆把动机写成一个乘积：努力取决于对“尝试能带来表现”的期望，乘以“表现能带来回报”的可能，"
        "再乘以对回报有多想要。<bookmark mark='d'/>当温德琳·范埃尔德和亨克·蒂埃里在1996年汇总这些检验时，每一部分都与努力和表现有适度的相关，"
        "而把它们乘起来几乎没有增加什么。接下来的目标设定，记录要强得多。",
    "Does do your best get people's best? <bookmark mark='a'/> From the nineteen sixties, Edwin":
        "“尽力而为”能让人发挥出最好的水平吗？<bookmark mark='a'/>从二十世纪六十年代起，埃德温·洛克和加里·莱瑟姆发现，具体而困难的目标比“尽力而为”带来更高的表现。<bookmark mark='b'/>数百项研究，在实验室和工作场所中，都发现了这一效应。它是工作心理学中重复得最多的结果之一。<bookmark mark='c'/>目标引导注意、提高努力、维持坚持，并促使人们寻找策略：这是第28部分的动机，用在了工作中。<bookmark mark='d'/>但它需要承诺和反馈。一个没人接受的目标，或者一个没人能看到的进展，作用甚微。",
    "Goals can also go wrong. <bookmark mark='a'/> A hard performance goal on a task people hav":
        "目标也可能出问题。<bookmark mark='a'/>在人们还没学会的任务上设定困难的绩效目标可能有害。先设定学习目标。<bookmark mark='b'/>被计数的东西会改善，没被计数的东西可能被忽视或被钻空子。这就是古德哈特定律。<bookmark mark='c'/>正如莫里斯·施魏策尔及同事所发现的，差一点就达到目标的人更可能谎报。<bookmark mark='d'/>所以要设计多个目标，包括质量，配以诚实的测量和学习的空间。",
    'Chapter eleven. Pay, and what money crowds out.':
        '第11章。薪酬，以及金钱挤出了什么。',
    "Does paying for performance get performance? <bookmark mark='a'/> In the nineteen nineties":
        "为绩效付酬能换来绩效吗？<bookmark mark='a'/>二十世纪九十年代，一家美国汽车玻璃公司把安装工从小时工资改为按每块挡风玻璃计酬，并保证最低收入。<bookmark mark='b'/>爱德华·拉齐尔分析了公司的记录。人均产出上升了约百分之四十四。<bookmark mark='c'/>大约一半来自同一批工人更卖力地工作，大约一半来自谁加入、谁留下。激励既推动人，也筛选人。<bookmark mark='d'/>在产出易于计数、质量易于检查的地方，计件工资有效。在不是这样的地方，它奖励的是错误的东西。",
    "Money can also crowd out what it replaces. <bookmark mark='a'/> In Israel in the late nine":
        "金钱也可能挤出它所替代的东西。<bookmark mark='a'/>二十世纪九十年代末，在以色列，研究者观察了十家托儿所，其中六家对晚接孩子的家长引入了一笔小额罚款。<bookmark mark='b'/>晚接并没有减少。它反而增加了，大约是原先水平的两倍。<bookmark mark='c'/>而当罚款取消后，晚接仍然居高不下。<bookmark mark='d'/>乌里·格尼茨和阿尔多·鲁斯蒂基尼的解读是：罚款把一种社会义务变成了一个价格，而且是一个便宜的价格。金钱挤出了规范。<bookmark mark='e'/>这是一项引人注目、被广泛引用、却没有大规模重复过的现场实验。账本如实记下了这一点。",
    'Chapter twelve. Satisfaction, teams and where people work.':
        '第12章。满意度、团队与人们在哪里工作。',
    "Is a happy worker a productive one? <bookmark mark='a'/> The hypothesis is old, and it was":
        "快乐的员工就是高效的员工吗？<bookmark mark='a'/>这个假说很古老，曾一度被宣告死亡，因为早期的综述只发现了很小的相关。<bookmark mark='b'/>2001年，蒂莫西·贾奇及同事在三百一十二个样本中对不可靠性进行了校正，发现相关约为零点三。<bookmark mark='c'/>但方向是怎样的？做得好会让人满意，反过来也一样，相关说不清楚。<bookmark mark='d'/>敬业度调查测量的是同一块领域，带着第46部分关于问题如何被回答的告诫。",
    "Every team has someone in charge, and leadership is one of the largest literatures in work psychology.":
        "每个团队都有一个负责的人，而领导力是工作心理学中文献最多的领域之一。<bookmark mark='a'/>它始于一个实验。1939年，库尔特·勒温、"
        "罗纳德·利皮特和拉尔夫·怀特为十岁的男孩办了课后俱乐部，由受过训练的成年人分别用专制、民主或放任的风格来带领。专制的俱乐部要么变得好斗，"
        "要么变得冷漠；民主的俱乐部最受男孩们喜欢。那只是几个小团体，它被记住的次数远多于被重复的次数。<bookmark mark='b'/>寻找领导者特质的研究"
        "在20世纪40年代被宣告失败，后来又复兴了：2002年，蒂莫西·贾奇和同事发现，大五人格能预测谁会成为领导者、谁被评为有效，其中外向性最强。"
        "<bookmark mark='c'/>俄亥俄州立大学的研究用两个维度来描述领导者：关怀，即对人的关心；以及结构，即对任务的关心。2004年，贾奇、罗纳德·皮科洛"
        "和雷姆斯·伊利斯发现两者都与结果有关，关怀更多关乎满意度，结构更多关乎绩效。<bookmark mark='d'/>过去四十年的主流观点是变革型领导："
        "领导者激励追随者，并改变他们想要的东西。它的问卷与结果的相关很好。但在2013年，达安·范克尼彭贝格和西姆·西特金认为，这些问卷把领导者的行为"
        "和它的效果混在一起，而且通常由评定结果的同一批人来填写，所以这些相关说明的东西比看上去要少。<bookmark mark='e'/>一个包含了自己结果的测量，"
        "就是第3部分的效度问题，出现在组织的最高层。",
    "Teams have their own psychology. <bookmark mark='a'/> In 1999 Amy Edmondson found that in ":
        "团队有自己的心理学。<bookmark mark='a'/>1999年，埃米·埃德蒙森发现，在一家制造公司的团队中，相信团队对人际冒险是安全的这一共同信念，能预测学习行为和绩效。<bookmark mark='b'/>更早，她在医院病区中发现，更好的团队报告的差错更多，不是因为犯得更多，而是因为他们愿意说出来。<bookmark mark='c'/>这与第51部分相连：机组资源管理就是经过训练的心理安全。<bookmark mark='d'/>大多数证据是相关性的、来自调查，而能提高心理安全的干预更难检验。",
    "And where people work can be randomized. <bookmark mark='a'/> In 2015 Nicholas Bloom and c":
        "而人们在哪里工作是可以随机分配的。<bookmark mark='a'/>2015年，尼古拉斯·布卢姆及同事报告了在一家中国旅游公司进行的一项试验。自愿参加的呼叫中心员工被随机分配到在家工作九个月。<bookmark mark='b'/>绩效提高了约百分之十三，主要是因为休息和病假更少而接了更多电话，离职率下降了约一半。<bookmark mark='c'/>但在家工作者的晋升率下降了，许多人之后选择回到办公室。<bookmark mark='d'/>后来对混合办公的试验发现绩效变化不大、离职率更低。答案取决于工作和安排。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Four new rows. The first: in the Hawthorne lighting studies, output rose whenever the ligh':
        "新增四行。第一行：在霍桑照明研究中，只要照明一变化产量就上升，因为工人知道自己在被研究。<bookmark mark='a'/>原始研究：勒特利斯伯格和迪克森的记述，1939年。<bookmark mark='b'/>后续记录：莱维特和李斯特对重新找到的产量记录的分析，证据微弱。<bookmark mark='c'/>被观察可能有影响，但霍桑是一个糟糕的例子。<bookmark mark='d'/>故事与记录不符。",
    'The second: structured interviews predict job performance better than unstructured ones. <':
        "第二行：结构化面试比非结构化面试更能预测工作表现。<bookmark mark='a'/>原始研究：麦克丹尼尔及同事的元分析，1994年。<bookmark mark='b'/>后续记录：1998年的施密特和亨特，以及2022年的萨基特及同事，差距反而扩大了。<bookmark mark='c'/>每一个效度的大小都变了；结构化的优势没有变。<bookmark mark='d'/>已重复。",
    'The third: ability tests predict job performance with a corrected validity of about zero p':
        "第三行：能力测验预测工作表现的校正效度约为零点五，是最好的单一预测指标。<bookmark mark='a'/>原始研究：施密特和亨特，1998年。<bookmark mark='b'/>后续记录：萨基特及同事修订到约零点三，以及一篇为更大校正辩护的回应。<bookmark mark='c'/>争论的是校正，而不是数据。<bookmark mark='d'/>有争议。",
    'And the fourth: a small fine for late pick-up at daycare increased late pick-ups. <bookmar':
        "第四行：托儿所对晚接的小额罚款增加了晚接。<bookmark mark='a'/>原始研究：格尼茨和鲁斯蒂基尼，2000年，十家托儿所。<bookmark mark='b'/>后续记录：一篇综述发现挤出效应在某些情境中存在，在另一些中不存在。<bookmark mark='c'/>一项引人注目的现场实验，没有大规模重复。<bookmark mark='d'/>未被直接检验。",
    "What the four have in common. <bookmark mark='a'/> The famous stories, Hawthorne and the f":
        "这四行的共同点。<bookmark mark='a'/>最有名的故事，霍桑和罚款，是检验最少的。<bookmark mark='b'/>朴素的结果，结构化，重复得最好，就像第28部分的目标设定。<bookmark mark='c'/>而这个领域里最大的那个数字，在重新思考其校正之后变动了三分之一。<bookmark mark='d'/>所以这一部分问题的答案是：工作心理学能做出预测，但很适度；它诚实的数字比它的故事要小。",
    'Chapter fourteen. In practice: a selection system, designed.':
        '第14章。实践中：设计一套选拔系统。',
    "Where is this a job? <bookmark mark='a'/> In talent assessment: designing and validating t":
        "这在哪里是一份工作？<bookmark mark='a'/>在人才测评中：在专业指导原则和法律之下，设计并验证测验、面试和评价中心。<bookmark mark='b'/>在人力分析中：公司内部的离职、绩效和敬业度数据，第47部分的层次和第2部分的因果都适用于此。<bookmark mark='c'/>在薪酬设计中：奖励重要之事、又不挤出不付钱之事的薪酬体系。<bookmark mark='d'/>还有在敬业度调查中，运用第46部分的问题编写方法，诚实地报告变化。",
    "Here's a worked design: a hundred hires from five hundred applicants. <bookmark mark='a'/>":
        "这是一个完整的设计示例：从五百名申请人中录用一百人。<bookmark mark='a'/>从工作分析开始：任务，以及完成这些任务所需的知识、技能和能力。<bookmark mark='b'/>使用一次结构化面试，加上一项工作知识测验或一个工作样本测验，按规则评分，按固定权重组合。<bookmark mark='c'/>组合的预期效度在零点四五左右，五年的效用以百万计，而测验成本以万计。<bookmark mark='d'/>在试点样本上检查不利影响。如果比值低于零点八，就沿着边界寻找一个效度相近、歧视性更小的替代方案。<bookmark mark='e'/>然后进行预测性验证：一年后收集绩效，用一个好的效标，只对实际发生的全距限制进行校正。<bookmark mark='f'/>还要保存一份决策日志，在拿到数据之前写好：什么算成功，以及系统在什么情况下会被修改。",
    'Chapter fifteen. Frontier: new assessments, old questions.':
        '第15章。前沿：新的测评，老的问题。',
    "Do new ways of assessing people predict better? <bookmark mark='a'/> Game-based assessment":
        "新的测评方式预测得更好吗？<bookmark mark='a'/>基于游戏的测评为特质和能力给谜题和游戏打分。它们很吸引人，但对工作表现的效度证据很薄弱。<bookmark mark='b'/>自动化面试用模型给视频或文字回答打分。结构化是内置的，但分数测量的是什么仍需要老式的验证。<bookmark mark='c'/>语言模型给论文和工作样本打分。它们可靠而快速，也可能继承它们所学的那些评分中的偏差。<bookmark mark='d'/>还有不靠评分的绩效：客观记录和许多评分者，而不是一年一次的评分。一个更好的效标会改变这一部分中的每一个效度。",
    "And the open problems. <bookmark mark='a'/> Corrections: how restricted were the samples b":
        "还有开放的问题。<bookmark mark='a'/>校正：每一个效度背后的样本受到了多大的全距限制？2022年的争论还没有定论。<bookmark mark='b'/>远程和混合办公：对晋升、学习和创新的长期影响，而不只是对产出。<bookmark mark='c'/>算法公平：当各种定义相互冲突时，一个招聘模型应该满足哪一种公平的定义。<bookmark mark='d'/>还有效度随时间的变化，因为工作变化得比验证研究进行得更快。",
    "First, your four numbers. <bookmark mark='a'/> A test with a true validity of zero point f":
        "首先，你的四个数字。<bookmark mark='a'/>一项真实效度为零点五的测验，在它录用的人当中只显示约零点一九。在2022年的综述中，最好的单一方法是结构化面试，约为零点四二。效度为零点三、录用前五分之一时，百分之六十七的录用者能胜任，而随机录用是百分之五十。托儿所的罚款让晚接大约翻了一番。<bookmark mark='b'/>适度的相关，经过诚实的校正，在用于许多决策时价值巨大。",
    "Part fifty-three in twelve lines. <bookmark mark='a'/> Hawthorne's story outlived its data":
        "第五十三部分，十二行。<bookmark mark='a'/>霍桑的故事比它的数据活得更久。效度是与一个效标的相关。评分很嘈杂，评分者占了评分的一半。选拔会掩盖效度，校正可以恢复它，但错误的校正会过头。2022年，结构化面试位居榜首，能力测验约为零点三。非结构化的印象会稀释好的预测指标。泰勒-拉塞尔表和效用分析把相关变成结果。分数线会放大群体差异，所以要在边界上做选择。算法学到的是它被给予的效标。目标有效，罚款可能变成价格。而满意度、心理安全和人们在哪里工作，都可以被检验。",
    "Where this comes back. <bookmark mark='a'/> Learning and training are Part 54. Incentives,":
        "这些内容会在哪里再次出现。<bookmark mark='a'/>学习与培训是第54部分。大规模的激励、默认选项和助推是第55部分。法庭上的测验与判断是第56部分。算法中的公平会在第60部分再次出现。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One correc":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道对一个效度做两次校正。一道计算效用。一道应用五分之四规则。一道求组合的效度。一道对面试评分者使用斯皮尔曼-布朗公式。一道问什么时候需要校正。最后带星号的一道，请你为一个你熟悉的岗位设计一套选拔系统。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Cronbach and Gles':
        '这一部分所依据的书籍和论文列在这里，也列在README中。克龙巴赫和格莱泽的书把选拔变成了决策理论；施密特和亨特，以及萨基特及同事，是应当放在一起读的两篇总结；莱维特和李斯特展示了一个著名的故事在它自己的数据中是什么样子。',
    "Three parts of Act Twelve are done. <bookmark mark='a'/> This one predicted who would do a":
        "第十二幕的三部分已经完成。<bookmark mark='a'/>这一部分预测谁会把一份工作做好，发现诚实的数字比故事要小。<bookmark mark='b'/>下一部分走进学校。为什么感觉最好的学习习惯效果最差？第54部分：学习的科学。",
    "Here's one structured question, worked.":
        "这是一个完整的结构化问题示例。<bookmark mark='a'/>为一名病房护士准备的问题：讲一次你在监护仪报警之前就注意到病人病情恶化的经历。<bookmark mark='b'/>评分锚点事先写好。一分：等着别人告诉自己。三分：注意到并报告了。五分：注意到、采取了行动、逐级上报，并核查了结果。<bookmark mark='c'/>两名面试官各自独立评分，然后取平均；相差超过一分的，对照锚点而不是对照印象进行讨论。<bookmark mark='d'/>当问题明显与工作有关时，候选人往往认为面试更公平。<bookmark mark='e'/>代价是每个岗位花一个下午写题。收获是面试所能买到的最大的效度提升。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
