"""Chinese narration for philosophy14: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '哲学，从零搭建 · 第14部分：改变主意'

CHAPTERS = {
    'Hook': '你该放弃什么？',
    'Moves': '1. 三种改变方式',
    'AGM': '2. AGM公设',
    'Spheres': '3. 球面与剩余集',
    'Iterated': '4. 再改一次',
    'Ramsey': '5. 如果',
    'Gardenfors': '6. 加登福斯的不可能性定理',
    'Counter': '7. 反事实条件句',
    'Trivial': '8. 条件句的概率',
    'McGee': '9. 当肯定前件式失效',
    'Defaults': '10. 跳到结论',
    'KLM': '11. 常态的逻辑',
    'Argue': '12. 相互攻击的论证',
    'Machines': '13. 会改变主意的机器',
    'Outro': '回顾、习题，以及它们会在哪里再出现',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part 13 told us how degrees of belief should move":
        "第13部分告诉我们信念度应当如何随证据移动。本部分对信念本身，以及对指导改变的那类句子——条件句——提出同样的问题。"
        "<bookmark mark='a'/>蒯因说，没有任何陈述可以免于修正。<bookmark mark='b'/>但当某样东西必须放弃时，逻辑并不说是哪一样。",
    "Here is the simplest case.":
        "这是最简单的情形。<bookmark mark='a'/>你相信所有天鹅都是白的，相信这只鸟是天鹅，也相信在这种光线下你的眼睛可靠。"
        "<bookmark mark='b'/>然后你看到这只鸟是黑的。<bookmark mark='c'/>四者合在一起不一致。<bookmark mark='d'/>逻辑告诉你某样东西必须放弃。"
        "它没有告诉你是哪一样，也没有告诉你还有多少东西要随之放弃。你是放弃“所有天鹅都是白的”，连同由它推出的每一个信念？还是怀疑自己的眼睛？"
        "本部分讲的就是这种选择的逻辑。",
    "The plan. <bookmark mark='a'/>Three ways to change a mind":
        "计划如下。<bookmark mark='a'/>改变主意的三种方式，以及学到与更新之间的区别。<bookmark mark='b'/>AGM公设——推理机会逐一检验——以及刻画它们的"
        "球面。<bookmark mark='c'/>改了再改。<bookmark mark='d'/>然后是条件句：拉姆齐检验，以及加登福斯的定理：它不能与修正共存，这是本部分在墙上的砖。"
        "<bookmark mark='e'/>反事实条件句，以及为什么条件句的概率不是任何命题的概率。<bookmark mark='f'/>一个肯定前件式的反例，以及跳到结论的逻辑。"
        "<bookmark mark='g'/>相互攻击的论证；以及必须改变主意的机器，包括大型语言模型。",
    # ------------------------------------------------------------------ Moves
    "Chapter one. Three ways to change.":
        "第一章。三种改变方式。",
    "A detective's case makes the three moves concrete.":
        "一位侦探的案子让三种操作变得具体。<bookmark mark='a'/>案情有四种可能：管家干的、女仆干的、两人都干了，或者都不是。<bookmark mark='b'/>侦探"
        "相信是管家干的，对女仆没有把握：这些世界在她的内圆盘里。其余世界按可信程度排在一圈圈的环上。<bookmark mark='c'/>扩充加入一个与已有信念相容的信念："
        "女仆有不在场证明，圆盘缩小到一个世界。<bookmark mark='d'/>修正加入一个与已有信念相冲突的信念：管家有不在场证明。她必须放弃某些东西，于是"
        "移到管家无辜的世界中最可信的那个：是女仆干的。<bookmark mark='e'/>收缩去掉一个信念而不加入它的否定：她不再相信是管家干的，并把最可信的替代"
        "——女仆——当作一种可能。",
    "Revision has a cousin that is easy to confuse with it.":
        "修正有一个容易与之混淆的近亲。<bookmark mark='a'/>你相信书和杂志恰好有一个在地板上。现在：书不在地板上。<bookmark mark='b'/>如果你是得知了这一点，"
        "那么你对书的看法错了，所以在地板上的一定是杂志。<bookmark mark='c'/>但如果是一个机器人刚把书捡了起来，那是世界变了。每种可能性各自移动：杂志"
        "还在原处，而你不再知道那是哪里。胜野裕文和阿尔贝托·门德尔松称第二种操作为更新。<bookmark mark='d'/>推理机确认，更新违反了下一章的一条公设。"
        "并非每一次改变主意都是修正。",
    "One postulate has divided the field.":
        "有一条公设让这个领域分裂。<bookmark mark='a'/>恢复公设：如果你放弃A又把A拿回来，你就拥有起初的一切。<bookmark mark='b'/>斯文·奥韦·汉松的例子。"
        "你相信克娄巴特拉有一个儿子，因此相信她有一个孩子。<bookmark mark='c'/>一位历史学家对那个孩子提出怀疑，于是你放弃了它，儿子也随之而去。"
        "<bookmark mark='d'/>然后有了新证据：她确实有一个孩子。<bookmark mark='e'/>恢复公设说，你必须再次相信她有一个儿子。<bookmark mark='f'/>但那个孩子"
        "可能是个女儿。<bookmark mark='g'/>对逻辑封闭的信念集来说，恢复公设是白送的；对机器实际存储的有限信念库来说，它是一个真正的选择，而信念库修正"
        "的理论拒绝它。",
    # ------------------------------------------------------------------ AGM
    "Chapter two. The AGM postulates.":
        "第二章。AGM公设。",
    "The theory of belief change has three founders.":
        "信念改变理论有三位奠基人。<bookmark mark='a'/>法哲学家卡洛斯·阿尔丘龙问：一部法典中废除了一条法律之后会怎样？它的哪些推论还保留下来？"
        "<bookmark mark='b'/>彼得·加登福斯问理性信念应当如何改变，以及条件句是什么意思。<bookmark mark='c'/>逻辑学家大卫·梅金森看出这是同一个问题。他们"
        "1985年的论文给这个理论取了名字：AGM。<bookmark mark='d'/>它的方法是本系列一再遇到的那种：不去定义唯一正确的修正，而是陈述任何理性修正都必须"
        "满足的约束，再看什么满足它们。<bookmark mark='e'/>指导思想是最小改变：当你必须放弃某些东西时，尽可能少放弃。",
    "The eight postulates for revision.":
        "修正的八条公设。<bookmark mark='a'/>封闭性：结果是一个信念集，对逻辑封闭。<bookmark mark='b'/>成功性：新信息被相信。<bookmark mark='c'/>包含性："
        "修正加入的东西不超过单纯扩充所加的。<bookmark mark='d'/>真空性：如果消息与你的信念不冲突，就什么也不丢；修正就是扩充。<bookmark mark='e'/>一致性："
        "除非消息本身矛盾，结果是一致的。<bookmark mark='f'/>外延性：逻辑等价的消息给出相同的结果。<bookmark mark='g'/>最后两条管合取。超扩充：按A且B修正，"
        "不比先按A修正再加入B更大胆。<bookmark mark='h'/>子扩充：而且，如果B与按A的修正相容，也不更胆小。<bookmark mark='i'/>前六条是基本公设；最后两条把"
        "按不同输入的修正联系在一起。",
    "Contraction has its own postulates.":
        "收缩有它自己的公设。<bookmark mark='a'/>结果是一个信念集；它不含任何新东西；如果你本来不相信A，就什么都不变；除非A是逻辑真理，你确实不再相信它。"
        "<bookmark mark='b'/>恢复公设，第一章里那条有争议的：收缩之后再加回来，什么都不丢。还有外延性。<bookmark mark='c'/>通过列维和哈珀的恒等式——下一章"
        "会遇到——这六条恰好对应修正的那六条基本公设。",
    "Which ways of revising pass?":
        "哪些修正方式能通过？<bookmark mark='a'/>推理机取三个原子、八个世界，用每一对命题去检验每一条公设。<bookmark mark='b'/>四个算子。按球面修正，"
        "下一章会讲到。穆克什·达拉尔的修正，保留改变原子数最少的世界。佐藤健的修正，保留改变原子集合在包含意义下极小的世界。还有玛丽安娜·温斯利特的"
        "更新。<bookmark mark='c'/>球面和达拉尔通过全部八条。<bookmark mark='d'/>佐藤的违反子扩充。<bookmark mark='e'/>温斯利特的更新也违反；而且正如书和杂志"
        "所表明的，一旦你相信的不止一个世界，它也违反真空性。<bookmark mark='f'/>当信念是世界的集合时，封闭性和外延性自动成立。",
    "Here is the Reasoner's counterexample to Satoh.":
        "这是推理机给出的佐藤修正的反例。<bookmark mark='a'/>你相信一个世界，其中p、q、r都为真。你按A修正，A排除了这个世界，留下三个。"
        "<bookmark mark='b'/>到达它们要改变r，或改变q，或同时改变p和r。<bookmark mark='c'/>前两种改变是极小的，所以按A修正保留那两个世界。"
        "<bookmark mark='d'/>再加入B，就只剩一个。<bookmark mark='e'/>但按A且B一起修正，竞争者是改变q，或改变p和r：两个集合互不包含，所以两者都保留。"
        "<bookmark mark='f'/>按更多的信息修正，反而保留了更多。子扩充失效。<bookmark mark='g'/>像达拉尔那样数改变的个数，而不是比较改变的集合，就能恢复这条"
        "公设。最小改变需要一个能比较一切的度量。",
    # ------------------------------------------------------------------ Spheres
    "Chapter three. Spheres and remainders.":
        "第三章。球面与剩余集。",
    "Adam Grove gave the postulates a picture in 1988.":
        "亚当·格罗夫在1988年给这些公设画了一幅图。<bookmark mark='a'/>把可能世界围绕你的信念排成嵌套的球面。内圆盘里是你认为可能的世界：这里只有一个，"
        "p、q、r都为真。向外每一环都比上一环稍不可信。<bookmark mark='b'/>要按A修正，就把球面向外扩，直到某个球面碰到A，然后相信那里的A世界。"
        "<bookmark mark='c'/>得知非p：第一环上恰有一个这样的世界。<bookmark mark='d'/>得知非p或非q：第一环上有两个世界合格。<bookmark mark='e'/>得知非p且非q："
        "你必须走到第二环。<bookmark mark='f'/>得知非r：一个世界。<bookmark mark='g'/>格罗夫定理：满足全部八条AGM公设的修正，恰好就是球面修正。同一类修正也"
        "可以由信念的牢固度排序得出，也可以由胜野和门德尔松的忠实预序得出。",
    "Contraction has its own construction.":
        "收缩有它自己的构造。<bookmark mark='a'/>要放弃p，就尽可能多地保留你的信念，同时不蕴涵p。这样一个极大部分叫作剩余集。<bookmark mark='b'/>这里有四个，"
        "每个p为假的世界对应一个：每个剩余集恰好接纳其中一个。<bookmark mark='c'/>保留哪个？只挑一个，即极大选择，你就太大胆了：你把没有p时事情会怎样的"
        "每个问题都定下来了。<bookmark mark='d'/>只保留所有剩余集共有的东西，即全交，你又太胆小：几乎什么都留不下。<bookmark mark='e'/>正确答案在两者之间："
        "保留最好的那些剩余集共有的东西，由一个选择函数挑选。<bookmark mark='f'/>AGM的表示定理：这些部分交收缩恰好就是满足基本公设的收缩；当选择来自一个"
        "排序时，它们也满足补充公设。",
    "The three operations are linked.":
        "这三种操作是相互联系的。<bookmark mark='a'/>艾萨克·列维的恒等式由收缩构造修正：要接受A，先放弃非A腾出地方，再加入A。<bookmark mark='b'/>威廉·哈珀"
        "的恒等式反过来：要放弃A，只保留你在得知非A时也会保留的东西。<bookmark mark='c'/>推理机在这些球面上，对每个命题检验了两者。<bookmark mark='d'/>球面"
        "还给出一个牢固度的次序：一个信念的牢固程度，就是它不成立的最近世界有多远。p且q，以及单独的p，在第一环就会丢失；p或q在第二环；p或q或r要到第三环。"
        "<bookmark mark='e'/>加登福斯和梅金森证明，收缩可以由这样一个次序来定义：当某样东西必须放弃时，放弃最不牢固的。",
    # ------------------------------------------------------------------ Iterated
    "Chapter four. Changing again.":
        "第四章。再改一次。",
    "AGM describes a single revision.":
        "AGM描述的是单次修正。<bookmark mark='a'/>它接受一个信念集及其球面，返回一个信念集。<bookmark mark='b'/>可要再修正一次，你需要围绕新信念的球面，"
        "而AGM对它们几乎什么都没说。<bookmark mark='c'/>所以一种信念状态必须不只是所信之事的集合：它是所有世界按可信程度的一个排序。"
        "<bookmark mark='d'/>阿德南·达尔维什和朱迪亚·珀尔提出了关于这个排序应当如何改变的公设。",
    "Wolfgang Spohn's ranking functions are the natural tool.":
        "沃尔夫冈·斯波恩的秩函数是天然的工具。<bookmark mark='a'/>每个世界得到一个非负整数：如果得知它是现实的，会有多意外。零表示一点也不意外。"
        "<bookmark mark='b'/>一个命题的意外程度，等于它最不意外的那个世界的意外程度。<bookmark mark='c'/>当非A令人意外时，你就相信A，相信得多牢固，就由有多"
        "意外来度量。<bookmark mark='d'/>这里你相信p，牢固度为二；相信q，牢固度为一。<bookmark mark='e'/>秩的行为就像对数尺度上的概率：最小值扮演加法的"
        "角色，加法扮演乘法的角色。斯波恩在秩上定义了条件化，并由此给出一种迭代修正的理论。",
    "Why do ranks behave like probabilities?":
        "秩为什么表现得像概率？<bookmark mark='a'/>把秩为k的世界读作概率量级为ε的k次方，ε是某个很小的数。<bookmark mark='b'/>于是概率之和由其中最大的一项"
        "主导，也就是最小的秩；概率之积变成秩之和；条件化变成减法。<bookmark mark='c'/>斯波恩以强度n对A作条件化，就是第13部分的杰弗里规则，用数量级写出来。"
        "<bookmark mark='d'/>按这种看法，信念就是接近一到只有数量级才要紧的信念度。",
    "Start from that ranking and revise by not p.":
        "从那个排序出发，按非p修正。四个算子。<bookmark mark='a'/>克雷格·布蒂利耶的自然修正，把最可信的非p世界移到最底层，其余一切保持原有次序。"
        "<bookmark mark='b'/>阿巴亚·纳亚克的字典序修正，把每个非p世界都放在每个p世界之下：这条消息成了你所知最牢固的东西。<bookmark mark='c'/>斯波恩的条件化"
        "按选定的强度，把非p世界下移、把p世界上移。<bookmark mark='d'/>一个失忆算子只保留新信念，把其余一切压平。四者对单次修正都满足AGM公设。",
    "Darwiche and Pearl's four postulates constrain the ordering.":
        "达尔维什和珀尔的四条公设约束这个排序。<bookmark mark='a'/>前两条：按mu修正时，mu世界之间的次序不动，非mu世界之间的次序也不动。另两条：原本"
        "比某个非mu世界更可信的mu世界，修正后仍更可信；原本至少同样可信的，也绝不会落到它后面。<bookmark mark='b'/>推理机用每一对命题，按四条公设检验四个"
        "算子。自然修正和字典序修正都通过。<bookmark mark='c'/>强度固定为一的斯波恩条件化违反后两条：如果非mu原本被更牢固地不相信，按mu条件化反而会削弱"
        "这个信念。<bookmark mark='d'/>失忆算子违反前三条：它忘掉了每一个条件信念。",
    "Darwiche and Pearl's example shows why the postulates matter.":
        "达尔维什和珀尔的例子说明了这些公设为什么重要。<bookmark mark='a'/>你看到一只鸟；它看上去是红的，而且会飞。<bookmark mark='b'/>然后有人告诉你它不是红的。"
        "两个主体都移到它不是红的世界中最可信的那个，并且仍然相信它会飞。<bookmark mark='c'/>然后你看得更清楚了：它终究是红的。自然修正者回到那只会飞的红鸟。"
        "失忆修正者相信它是红的，却不再知道它会不会飞：第一次修正抹掉了“如果它是红的，它就会飞”这个条件信念。<bookmark mark='d'/>理性的修正必须保留消息"
        "不涉及的东西。",
    # ------------------------------------------------------------------ Ramsey
    "Chapter five. If.":
        "第五章。如果。",
    "Logic's own conditional is the material conditional.":
        "逻辑自己的条件句是实质条件句。<bookmark mark='a'/>只有当前件真、后件假时它才为假，在其余每一行都为真。<bookmark mark='b'/>所以，如果月亮是奶酪做的，"
        "二加二就等于五：为真，因为月亮不是。<bookmark mark='c'/>如果我中了彩票，我就会变穷：只要我没中，就为真。<bookmark mark='d'/>更糟的是：否认一个实质"
        "条件句，就使你承诺其前件。否认“如果上帝存在，祈祷就会应验”，你就证明了上帝存在。<bookmark mark='e'/>这些是实质蕴涵的悖论。逻辑的“如果”和我们的"
        "并不完全一样。",
    "Logic has offered two repairs, met earlier in the series.":
        "逻辑提出过两种补救，本系列前面已经遇到。<bookmark mark='a'/>C·I·刘易斯的严格条件句，见第4部分：必然地，如果A则C。没有哪个世界有A而无C。但一个"
        "不可能的前件严格蕴涵一切。<bookmark mark='b'/>还有艾伦·安德森和努埃尔·贝尔纳普的相干条件句，见第5部分，它要求前件和后件有共同内容，因而拒绝了奶酪"
        "和算术那样的例子。<bookmark mark='c'/>两者都改进了逻辑。都没有解释“如果”如何依赖于我们所知道的东西，而本部分其余部分正是去看这一点。",
    "Ernest Adams pointed out that English has at least two conditionals.":
        "欧内斯特·亚当斯指出，英语至少有两种条件句。<bookmark mark='a'/>如果奥斯瓦尔德没有杀肯尼迪，那就是别人杀的。为真：肯尼迪确实被某人杀了。"
        "<bookmark mark='b'/>如果奥斯瓦尔德当时没有杀肯尼迪，别人也会杀他。很可能为假，除非有第二个枪手在等着。<bookmark mark='c'/>同样的前件，同样的后件，"
        "不同的真值。第一种，直陈条件句，关于在我们所知之下事情是怎样的。第二种，反事实条件句，关于事情本来会怎样。第七章和第八章依次讨论它们。",
    "Frank Ramsey, in 1929, gave a test for conditionals":
        "弗兰克·拉姆齐在1929年给出了一个检验条件句的方法，它塑造了此后的一切。<bookmark mark='a'/>要判断“如果p，那么q”，就把p假设性地加到你所知道的东西里，"
        "看q是否随之而来。<bookmark mark='b'/>罗伯特·斯托内克和随后的加登福斯把它变成一条原则：你相信“如果A则C”，恰当按A修正会让你相信C。"
        "<bookmark mark='c'/>以那位侦探为例。如果不是管家干的，就是女仆干的？<bookmark mark='d'/>按管家无辜来修正：最近的这样的世界是女仆干的那个。"
        "<bookmark mark='e'/>所以她相信这个条件句。<bookmark mark='f'/>拉姆齐检验把信念修正变成了“如果”的一种语义。它看起来显然正确。下一章表明，它与AGM"
        "公设结合在一起是不可能的。",
    # ------------------------------------------------------------------ Gardenfors
    "Chapter six. Gärdenfors's impossibility.":
        "第六章。加登福斯的不可能性定理。",
    "Gärdenfors proved it in 1986.":
        "加登福斯在1986年证明了它。两个要素。<bookmark mark='a'/>第一，拉姆齐检验使修正具有单调性。如果信念集H包含信念集K，它就包含K的条件句；按拉姆齐"
        "检验，这些条件句说明了K的修正包含什么；所以H的修正至少包含同样多的东西。<bookmark mark='b'/>第二，保持性，它由AGM的真空性推出：与你的信念相容的"
        "消息不让你付出任何代价。<bookmark mark='c'/>定理：没有一个非平凡的修正系统同时满足两者。非平凡只是指：某个信念集让三个两两互斥的命题都保持敞开。",
    "Here is the proof, on three worlds.":
        "这是证明，在三个世界上。<bookmark mark='a'/>A、B、C各在一个世界中为真。从一个让三者都敞开的信念集K出发。<bookmark mark='b'/>按A或B扩充，得到K一；"
        "按A或C扩充，得到K二。<bookmark mark='c'/>再单按A扩充，得到H。<bookmark mark='d'/>现在按B或C修正K一和K二。这条消息与两者都相容，所以按保持性，它就是"
        "简单地加进去：K一现在相信B，K二相信C。<bookmark mark='e'/>H包含K一和K二所相信的一切，包括它们的条件句。所以按单调性，H按B或C的修正必须落在它们"
        "两者的修正之内：既在b之内，又在c之内。<bookmark mark='f'/>推理机尝试每一个候选。相信b违反第二个约束；<bookmark mark='g'/>相信c违反第一个；"
        "<bookmark mark='h'/>两者都敞开则两个都违反。<bookmark mark='i'/>什么都不剩：H按一个相容命题的修正竟必须不一致。矛盾。",
    "Something has to give.":
        "总得放弃点什么。<bookmark mark='a'/>艾萨克·列维的回答：条件句根本不是信念。它们表达的是你倾向于如何修正，所以不属于信念集。"
        "<bookmark mark='b'/>或者削弱保持性：一旦条件句是信念，相容的消息也可能让你失去其中一些。<bookmark mark='c'/>约斯塔·格拉内证明，拉姆齐检验与胜野和"
        "门德尔松意义上的更新——而不是修正——是相容的。<bookmark mark='d'/>或者把检验限制在事实性语句上。<bookmark mark='e'/>每一种回答都承认，条件句拒绝被当作"
        "普通信念。这是本部分在墙上那块砖的一半；刘易斯在第八章提供另一半。",
    # ------------------------------------------------------------------ Counter
    "Chapter seven. Counterfactuals.":
        "第七章。反事实条件句。",
    "Counterfactuals got their modern semantics":
        "反事实条件句的现代语义来自1968年的罗伯特·斯托内克和1973年的大卫·刘易斯。<bookmark mark='a'/>“如果A本来成立，C就会成立”在一个世界为真，当C在离它"
        "最近的所有A世界都成立。<bookmark mark='b'/>近，就是总体上的相似，每个世界离自己最近。<bookmark mark='c'/>刘易斯允许并列；斯托内克坚持总有恰好一个"
        "最近的A世界。<bookmark mark='d'/>这又是格罗夫的球面，只不过现在以一个世界而不是一个信念集为中心。<bookmark mark='e'/>肯定前件式成立：如果A在这里为真，"
        "那么这里就是最近的A世界。<bookmark mark='f'/>但五个对实质条件句有效的推理失效了。推理机为每一个构造了一个小模型。",
    "Strengthening the antecedent, Nelson Goodman's match.":
        "前件强化，纳尔逊·古德曼的火柴。<bookmark mark='a'/>如果我划了这根火柴，它就会着。为真：划了火柴的最近世界里，火柴是干的，而且着了。"
        "<bookmark mark='b'/>如果我划了它而它是湿的，它就会着。为假：最近的这样的世界里，湿火柴着不起来。<bookmark mark='c'/>往前件里加东西，可能把你带到更远的"
        "世界。",
    "Transitivity, from Stalnaker.":
        "传递性，来自斯托内克。<bookmark mark='a'/>如果J·埃德加·胡佛出生在俄国，他就会是共产党人。如果他是共产党人，他就会是叛徒。<bookmark mark='b'/>但不能"
        "推出：如果他出生在俄国，他就会是叛徒。<bookmark mark='c'/>最近的共产党人胡佛是美国的叛徒；最近的俄国胡佛是忠诚的苏联公民。",
    "Contraposition.":
        "换质位。<bookmark mark='a'/>如果歌德活过了1832年，他现在仍然已经去世。为真。<bookmark mark='b'/>换质位：如果歌德现在还活着，他就没有活过1832年。"
        "荒谬。<bookmark mark='c'/>他活下去的最近世界，仍然是他早已去世的世界。",
    "Conditional excluded middle, with Quine's Bizet and Verdi.":
        "条件排中律，用蒯因的比才与威尔第。<bookmark mark='a'/>如果他们是同胞，比才会是意大利人吗？还是威尔第会是法国人？<bookmark mark='b'/>两个同胞世界"
        "同样近。刘易斯：两个条件句都不为真，它们的析取也不成立。<bookmark mark='c'/>斯托内克坚持只有一个最近世界，以保住条件排中律；推理机确认，一旦打破"
        "并列它就成立，并说在两者之间的选择是不确定的。",
    "Simplifying disjunctive antecedents.":
        "析取前件的简化。<bookmark mark='a'/>如果西班牙参战，无论站在哪一边，它都会加入轴心国：考虑到佛朗哥，这是合理的。<bookmark mark='b'/>简化：如果西班牙"
        "加入了同盟国，它就会加入轴心国。荒谬。<bookmark mark='c'/>然而在日常说话中，这种简化似乎是有效的；许多语义学家如今把析取前件当作一种特殊情形。",
    "Which semantics is right?":
        "哪种语义是对的？<bookmark mark='a'/>刘易斯的线段：如果这条线长于一英寸。有些世界里它长一英寸半，一又三分之一，一又四分之一，如此类推：没有最近的那个。"
        "<bookmark mark='b'/>斯托内克假设总有一个最近的前件世界，这为他换来了条件排中律。<bookmark mark='c'/>刘易斯允许并列，并去掉了极限假设：当这个世界周围"
        "的某个球面使实质条件句处处成立时，反事实条件句为真。<bookmark mark='d'/>推理机确认，一旦打破比才与威尔第的并列，排中律就成立，如斯托内克所说。"
        "<bookmark mark='e'/>那么，什么让世界相似？刘易斯1979年的回答，对第17部分的因果关系很重要：首先避免对定律的大违背，然后尽可能多地保留具体事实。",
    "Kit Fine raised the strongest objection to similarity.":
        "基特·法恩对相似性提出了最有力的反驳。<bookmark mark='a'/>如果尼克松按下了按钮，就会有一场核浩劫。<bookmark mark='b'/>这肯定是真的。"
        "<bookmark mark='c'/>但一个他按下按钮、一个小小的电路故障让导弹没有发射的世界，远比一个发生核战争的世界更像我们的世界。所以相似性似乎让这个反事实"
        "条件句为假。<bookmark mark='d'/>刘易斯在1979年的回答是说明哪些相似性算数，按重要性排序：第一，避免大范围、普遍的违背定律；第二，保留尽可能大的完全"
        "吻合的区域；第三，连小的违背也要避免；而具体事实的近似吻合几乎无关紧要。<bookmark mark='e'/>于是最近的世界里有一个小小的奇迹让按钮被按下，此后定律"
        "照常运行。核浩劫的世界胜出。刘易斯把他的因果理论和时间的方向都建立在这个排序上；第17部分来检验它。",
    "Counterfactuals now explain the decisions of machines.":
        "反事实条件句如今被用来解释机器的决定。<bookmark mark='a'/>桑德拉·瓦赫特、布伦特·米特尔施泰特和克里斯·罗素提议，用最近的那个结果相反的世界来解释"
        "一个自动化决定。<bookmark mark='b'/>取一条简单的贷款规则。<bookmark mark='c'/>一位收入五万美元、工作了两年的申请人被拒。<bookmark mark='d'/>把每一项"
        "改变分别计数，最近的批准是：如果你的收入多一万五千美元，你就会获批。<bookmark mark='e'/>用直线距离来量，则是收入多一万二千美元、工作多七个月。"
        "<bookmark mark='f'/>哪个世界算最近是一种选择，它改变申请人得到的解释。刘易斯的相似性问题，出现在信贷办公室里。",
    # ------------------------------------------------------------------ Trivial
    "Chapter eight. The probability of conditionals.":
        "第八章。条件句的概率。",
    "How likely is a conditional to be true?":
        "一个条件句为真的可能性有多大？<bookmark mark='a'/>从一副牌里抽一张。如果它是红的，它就是红心。<bookmark mark='b'/>按实质条件句来读，除非这张牌是红方块，"
        "条件句都为真：四分之三。<bookmark mark='c'/>但几乎每个人都说二分之一：给定它是红的，它是红心的机会。乔纳森·埃文斯和大卫·奥弗等心理学家多次证实了这一点。"
        "<bookmark mark='d'/>欧内斯特·亚当斯把它变成一个论题：“如果A，C”的可断言度是给定A时C的条件概率。<bookmark mark='e'/>罗伯特·斯托内克走得更远：存在"
        "一个命题“如果A则C”，它的概率就是那个条件概率。大卫·刘易斯在1976年证明这不可能。",
    "Here is Lewis's proof, on three worlds.":
        "这是刘易斯的证明，在三个世界上。<bookmark mark='a'/>一个信念度在三个世界上各分三分之一：A且C，A且非C，以及两者都不。给定A时C的信念度是二分之一。"
        "假设某个命题X对这个信念度、以及对它通过条件化所能变成的一切，都具有给定A时C的概率。<bookmark mark='b'/>以C为条件。全部质量滑到A且C的世界上，"
        "现在给定A时C是确定的；所以X必须包含那个世界。<bookmark mark='c'/>改为以非C为条件。现在给定A时C的概率为零，所以X必须不含另外两个世界。"
        "<bookmark mark='d'/>所以X就是C，它的概率是三分之一。<bookmark mark='e'/>可它应当是二分之一。矛盾。<bookmark mark='f'/>一般地，这个论证表明，只要两个A世界"
        "都可能，条件句的概率就必须等于C本身的概率：条件概率坍缩为普通概率，这就是平凡性。",
    "The Reasoner checks the result by brute force.":
        "推理机用穷举来检验这个结果。<bookmark mark='a'/>它取一个小模型上的每个命题，以及一个对条件化封闭的信念度族中的每个信念度：每个世界集合上的均匀信念度。"
        "<bookmark mark='b'/>四个世界时，十六个命题、十二个信念度：没有哪个命题能对其中超过六个符合条件概率。<bookmark mark='c'/>三个世界时，同样没有命题行得通。"
        "<bookmark mark='d'/>只有在平凡模型里，没有A成立而C不成立的世界时，才有一个行得通，而那里条件句反正是确定的。",
    "Lewis also said what the probability of a counterfactual is.":
        "刘易斯还说明了反事实条件句的概率是什么。<bookmark mark='a'/>取四个世界上的一个信念度。要以A为条件，就删去非A世界，把它们的质量按比例分到A世界上："
        "<bookmark mark='b'/>给定A时C是二分之一。<bookmark mark='c'/>若改为对A成像，就让每个非A世界把它的质量送到它自己最近的A世界。<bookmark mark='d'/>这里C的"
        "概率变成零点六。<bookmark mark='e'/>刘易斯证明，斯托内克反事实条件句的概率恰好就是成像后的概率，而不是条件概率。反事实条件句是命题，而直陈条件句，"
        "如果亚当斯是对的，则表现得像别的什么东西。",
    "The Reasoner sets out the cluster as a Price List.":
        "推理机把这一组主张列成代价清单。<bookmark mark='a'/>四个主张：条件句的概率就是条件概率，对每个信念度都如此；理性的信念度在条件化之后仍然理性；条件句在"
        "每个世界或真或假；而且某个信念度使条件概率不同于普通概率。<bookmark mark='b'/>合在一起不一致；任何一个都可以放弃。<bookmark mark='c'/>欧内斯特·亚当斯和"
        "多萝西·埃金顿放弃第三个：直陈条件句没有真值条件；接受一个条件句，就是有高的条件信念度。<bookmark mark='d'/>刘易斯和弗兰克·杰克逊放弃第一个：“如果”是"
        "实质的，条件概率只度量它有多可断言。<bookmark mark='e'/>另一些人实际上放弃第二个：条件句所表达的命题随信念度而变，如巴斯·范弗拉森、以及最近的贾斯汀·"
        "Khoo和马修·曼德尔克恩所主张。<bookmark mark='f'/>放弃第四个会使信念度变得平凡，没有人这么做。",
    "This is the fourteenth brick in the Wall.":
        "这是墙上的第十四块砖。<bookmark mark='a'/>梦想：条件句是普通的命题，按拉姆齐检验被相信，并且被相信的程度就是条件概率。<bookmark mark='b'/>墙：刘易斯的平凡性"
        "定理，以及加登福斯的不可能性定理。<bookmark mark='c'/>它们逼出的东西：条件句也许根本不陈述事实；或者，如果陈述事实，它们所陈述的事实随我们所知而变。"
        "无论哪种，“如果”都不是像“且”或“或”那样的联结词。",
    # ------------------------------------------------------------------ McGee
    "Chapter nine. When modus ponens fails.":
        "第九章。当肯定前件式失效。",
    "Vann McGee published a counterexample":
        "范·麦吉在1985年发表了一个肯定前件式的反例。<bookmark mark='a'/>1980年大选前，民调显示共和党人罗纳德·里根遥遥领先；民主党人吉米·卡特远远排第二；"
        "以独立身份参选的共和党人约翰·安德森远远落后。<bookmark mark='b'/>考虑：如果一个共和党人获胜，那么如果里根没赢，安德森就会赢。这是确定的：他们是仅有的"
        "共和党人。<bookmark mark='c'/>以及：一个共和党人会获胜。很可能。<bookmark mark='d'/>肯定前件式给出：如果里根没赢，安德森就会赢。但这非常不可能：如果里根"
        "没赢，几乎肯定是卡特赢。<bookmark mark='e'/>你可以相信两个前提而拒绝结论。而里根确实赢了；所以前提为真，结论似乎为假。",
    "What has gone wrong?":
        "哪里出了问题？<bookmark mark='a'/>第一个前提是一个嵌套条件句，而嵌套条件句遵守输入-输出律：“如果A，那么如果B，C”与“如果A且B，C”说的是同一件事。"
        "<bookmark mark='b'/>麦吉证明，任何具有输入-输出律、且其概率为亚当斯条件概率的条件句，都必定在某处违反肯定前件式。<bookmark mark='c'/>实质条件句保住了"
        "肯定前件式，代价是它的悖论。<bookmark mark='d'/>安格莉卡·克拉策的语言学给出了一个诊断：“如果”根本不是联结词。“如果”从句限制一个情态词，无论它是说"
        "出来的还是隐含的。<bookmark mark='e'/>那么麦吉的第一个前提量化的是共和党人获胜的那些世界，结论量化的是所有世界，这个论证从来就不是肯定前件式的一个实例。",
    "A second puzzle, from Niko Kolodny and John MacFarlane.":
        "第二个谜题，来自尼科·科洛德尼和约翰·麦克法兰。<bookmark mark='a'/>十名矿工被困在两个竖井之一，我们不知道是哪一个。<bookmark mark='b'/>如果我们封住A井"
        "而他们在A里，就全部获救；如果他们在B里，就全部遇难。B井也一样。<bookmark mark='c'/>如果两个都不封，无论他们在哪里，都会有一名矿工遇难。"
        "<bookmark mark='d'/>看起来为真的是：如果他们在A里，我们应当封A；如果他们在B里，我们应当封B。<bookmark mark='e'/>他们不是在这个就是在那个里；所以，按"
        "分情形推理，我们应当封A，或者应当封B。<bookmark mark='f'/>但显然我们哪个都不该封。条件性的“应当”，就像麦吉的条件句，依赖于所知道的东西，而经典的推理"
        "规则在这种依赖之下不能原封不动地保留。",
    # ------------------------------------------------------------------ Defaults
    "Chapter ten. Jumping to conclusions.":
        "第十章。跳到结论。",
    "Artificial intelligence met belief revision from another direction.":
        "人工智能从另一个方向遇上了信念修正。<bookmark mark='a'/>被告知特威蒂是一只鸟，你就推断特威蒂会飞。<bookmark mark='b'/>再被告知特威蒂是一只企鹅，你就推断"
        "特威蒂不会飞。<bookmark mark='c'/>经典逻辑做不到这一点。它是单调的：增加前提永远不会去掉结论。<bookmark mark='d'/>日常推理是非单调的。"
        "<bookmark mark='e'/>“鸟会飞”不是“所有鸟都会飞”这个假的概括；它是一个缺省，除非有别的东西说不，否则成立。1980年《人工智能》的一期专刊推出了三种缺省"
        "逻辑。",
    "Raymond Reiter's default logic is the best known.":
        "雷蒙德·雷特的缺省逻辑最为著名。<bookmark mark='a'/>一条缺省规则说：如果是鸟，而且“会飞”与你所信的相一致，就推断会飞。<bookmark mark='b'/>一致性检查"
        "指向最终的信念集，所以结论是一个不动点，叫作外延：一个信念集，它恰好为它到达那里所用的缺省提供了理由。<bookmark mark='c'/>推理机通过尝试每一组缺省来"
        "找出外延。事实是特威蒂是一只鸟、企鹅是鸟、企鹅不会飞，<bookmark mark='d'/>此时有一个外延，其中特威蒂会飞。<bookmark mark='e'/>加入特威蒂是一只企鹅。"
        "现在“不会飞”被推出，缺省被阻断，<bookmark mark='f'/>唯一的外延里特威蒂飞不起来。",
    "Defaults can conflict.":
        "缺省之间可能冲突。<bookmark mark='a'/>理查德·尼克松既是贵格会教徒，又是共和党人。贵格会教徒缺省地是和平主义者；共和党人缺省地不是。"
        "<bookmark mark='b'/>推理机找到两个外延：在一个里，贵格会的缺省被触发并阻断了另一个；在第二个里则相反。<bookmark mark='c'/>轻信的推理者挑一个。"
        "<bookmark mark='d'/>怀疑的推理者只相信每个外延都共有的东西，<bookmark mark='e'/>因此对尼克松是否和平主义者不作任何结论。这个选择会在两章之后、论证相互"
        "攻击的时候再次出现。",
    "Two other logics from 1980 are still in use.":
        "1980年的另外两种逻辑至今仍在使用。<bookmark mark='a'/>约翰·麦卡锡的限定：写下“不反常的鸟会飞”，然后只保留反常之物尽可能少的模型。企鹅必须是反常的；"
        "仅仅是鸟的特威蒂不必如此，所以特威蒂会飞。<bookmark mark='b'/>还有失败即否定，以及雷特的封闭世界假设：如果没有列出从波士顿到东京的航班，就推断没有。"
        "每一次数据库查询、每一个Prolog程序都是这样推理的。<bookmark mark='c'/>它们都会跳到新信息可能撤回的结论。",
    "Defaults were meant to solve the frame problem":
        "缺省本是为了解决约翰·麦卡锡和帕特里克·海斯的框架问题：怎样不用无穷无尽的公理就说出，你行动时大多数事情保持不变。<bookmark mark='a'/>史蒂夫·汉克斯和"
        "德鲁·麦克德莫特的耶鲁射击问题检验了它。给枪上膛，等待，然后向弗雷德开枪。假设事物通常不变，并使改变最少。<bookmark mark='b'/>推理机找到两个极小模型。"
        "在预期的那个里，枪一直上着膛，弗雷德在开枪时死去。<bookmark mark='c'/>在另一个里，枪在等待时莫名其妙地退了膛，弗雷德活了下来。每个都恰好有一处反常，"
        "所以最小化无法选择。<bookmark mark='d'/>补救随之而来：偏好较晚的改变而非较早的，或者把因果定律内置到逻辑中。而格奥尔格·戈特洛布证明，用雷特的缺省进行"
        "推理比任何NP问题都难，除非多项式谱系坍缩。跳到结论并不便宜。",
    # ------------------------------------------------------------------ KLM
    "Chapter eleven. The logic of normality.":
        "第十一章。常态的逻辑。",
    "Sarit Kraus, Daniel Lehmann and Menachem Magidor asked":
        "萨里特·克劳斯、丹尼尔·莱曼和梅纳赫姆·马吉多尔问，所有合理的可废止推理有什么共同之处。<bookmark mark='a'/>他们的语义：A可废止地蕴涵B，当B在最常态的"
        "A世界里成立。<bookmark mark='b'/>一个偏好模型按常态程度给世界排序。<bookmark mark='c'/>最常态的鸟世界里鸟会飞，所以“鸟”可废止地蕴涵“会飞”。"
        "<bookmark mark='d'/>最常态的企鹅世界里企鹅不会飞。<bookmark mark='e'/>这又是格罗夫的球面图。",
    "From that semantics come the rules.":
        "规则就从这种语义中来。<bookmark mark='a'/>推理机在两个小模型上检验它们，一个是分层的，常态分等级；一个只是偏好的，有些世界不可比较。<bookmark mark='b'/>"
        "自反性、合取、析取、谨慎单调性和切割在两者中都成立。它们一起构成P系统，可废止推理的核心。<bookmark mark='c'/>理性单调性说的是：当你得知某件你并不预期"
        "为假的事时，可以保留一个结论；它在分层模型中成立，在偏好模型中失效。<bookmark mark='d'/>而普通的单调性在两者中都失效，这正是应该的。",
    "System P has a second, probabilistic, foundation.":
        "P系统还有第二个基础，一个概率的基础。<bookmark mark='a'/>欧内斯特·亚当斯把缺省“A通常是B”读作：给定A时B的概率接近一。<bookmark mark='b'/>按他的意义，"
        "一个结论被推出，如果只要让前提的概率足够接近一，就能让它的概率随你所愿地接近一。<bookmark mark='c'/>朱迪亚·珀尔和赫克托·格夫纳证明，亚当斯的语义所认可的"
        "规则恰好就是P系统。<bookmark mark='d'/>单调性失效，这正是应该的：给定是鸟，会飞的可能性大；给定是鸟且是企鹅，会飞的可能性小。<bookmark mark='e'/>第13部分"
        "的概率与本部分的排序，得出了同一种常态的逻辑。",
    "Which defeasible conclusions follow from a set of defaults?":
        "一组缺省能推出哪些可废止的结论？朱迪亚·珀尔的Z系统给出一个标准答案，与莱曼和马吉多尔的理性闭包相同。<bookmark mark='a'/>把缺省分层。“鸟会飞”和“鸟有翅膀”"
        "能与其余一切同时满足：第0层。“企鹅是鸟”和“企鹅不会飞”只有在把前者放到一边之后才能满足：第1层。<bookmark mark='b'/>然后按每个世界违反的最高层来给它排序，"
        "再从最常态的世界读出结论。<bookmark mark='c'/>推理机的答案：鸟会飞；企鹅不会；企鹅是鸟；红色的鸟会飞，因为红色无关紧要。<bookmark mark='d'/>但企鹅有翅膀吗？"
        "Z系统不说。企鹅在一个方面是例外，这个例外淹没了另一项继承。这就是淹没问题。<bookmark mark='e'/>莱曼的字典序闭包数违反的缺省个数，而不只看最高层，"
        "就把翅膀找了回来。",
    "Step back.":
        "退一步看。<bookmark mark='a'/>A可废止地蕴涵B，B属于K按A的修正，以及K相信“如果A则B”：<bookmark mark='b'/>三个领域，可废止推理、<bookmark mark='c'/>信念修正、"
        "<bookmark mark='d'/>以及条件句。<bookmark mark='e'/>大卫·梅金森和彼得·加登福斯在1991年证明，前两者是同一个理论的两面：理性后承关系恰好就是一个固定信念集"
        "的AGM修正。<bookmark mark='f'/>一个世界的排序，画成球面或写成秩，构成了这三者的基础，而加登福斯的定理标出了它们唯一不能完全合并的地方。",
    # ------------------------------------------------------------------ Argue
    "Chapter twelve. Arguments that attack.":
        "第十二章。相互攻击的论证。",
    "In 1995 Phan Minh Dung made a radical abstraction.":
        "1995年，潘明勇作出了一个大胆的抽象。<bookmark mark='a'/>忘掉论证说了什么；只保留哪个论证攻击哪个。<bookmark mark='b'/>一组论证如果彼此都不攻击，就是"
        "无冲突的。<bookmark mark='c'/>如果它还为自己的每个成员辩护——每个成员的每个攻击者都被某个成员攻击——它就是可接受的。<bookmark mark='d'/>根基外延是谨慎的"
        "答案：接受不受攻击的论证，拒绝它们所攻击的，如此重复，直到不再变化。<bookmark mark='e'/>偏好外延是大胆的答案，即极大的可接受集；稳定外延攻击它之外的一切。"
        "<bookmark mark='f'/>潘明勇证明，缺省逻辑、逻辑程序设计，以及n人博弈的解，都是这一个结构的实例。",
    "Three small frameworks show the semantics at work.":
        "三个小框架展示这些语义如何运作。<bookmark mark='a'/>复位：c攻击b，b攻击a。c不受攻击，所以在内；b在外；a得到c的辩护，又回到内。<bookmark mark='b'/>相互"
        "攻击：a和b互相攻击。谨慎的根基外延两个都不接受，两者都是未定。大胆的偏好语义给出两个答案，a或b，就像尼克松菱形的两个外延。<bookmark mark='c'/>奇环："
        "a攻击b，b攻击c，c攻击a。没有论证能得到辩护，唯一的偏好外延是空集，而且根本没有稳定外延，这是一个微型的悖论。",
    "Here is a trial.":
        "这是一场审判。<bookmark mark='a'/>控方：一位证人看见了他。辩方：她喝醉了。控方：她的血检是干净的。辩方：检测被污染了。控方：实验室的记录显示没有污染。"
        "<bookmark mark='b'/>根基语义给这条链打上标记：记录不受攻击，所以在内；污染在外；血检在内；醉酒在外；证人的证词成立。<bookmark mark='c'/>现在辩方声称记录"
        "被篡改了，而控方又反驳这一点：一个相互攻击。根基外延现在是空集，有两个偏好外延，各属一方。<bookmark mark='d'/>一个怀疑的法庭只接受每个外延都接受的东西，"
        "于是判无罪；一个轻信的法庭两种都可能。在真实的法律中，这样的僵局由举证责任来裁决。",
    "Argumentation frameworks are used well beyond philosophy.":
        "论辩框架的用途远远超出哲学。<bookmark mark='a'/>在法律中，亨利·普拉肯的ASPIC加和Carneades等系统为结构化论证和举证责任建模。<bookmark mark='b'/>在医学和"
        "政策中，用于展示其理由及对这些理由之反驳的决策支持。<bookmark mark='c'/>在软件主体之间的谈判中，它们交换的不只是报价，还有论证。<bookmark mark='d'/>在论证"
        "挖掘中，从文本里找出主张和攻击；IBM的Project Debater在2019年与人类冠军辩论。<bookmark mark='e'/>还有让大型语言模型相互辩论来检验它们的提议。"
        "<bookmark mark='f'/>每一次，问题都是潘明勇的那个：哪些论证能在它们的攻击者面前幸存？",
    # ------------------------------------------------------------------ Machines
    "Chapter thirteen. Machines that change their minds.":
        "第十三章。会改变主意的机器。",
    "The first machines to change their minds were truth maintenance systems":
        "最早会改变主意的机器是真值维护系统，由乔恩·多伊尔在1979年引入。<bookmark mark='a'/>每个信念记录它的理由。<bookmark mark='b'/>“会飞”被相信，是因为"
        "“鸟”被相信而“企鹅”没有；“能迁徙”依赖于“会飞”。<bookmark mark='c'/>当系统得知这只鸟是企鹅时，它撤回“会飞”，以及依赖于它的一切，其余什么都不动。"
        "<bookmark mark='d'/>约翰·德克莱尔基于假设的版本同时追踪所有的假设组合。它们是汉松意义上的信念库修正，被实现了出来。",
    "Databases face the same problem.":
        "数据库面临同样的问题。<bookmark mark='a'/>一张表给安列了两份薪水，违反了每人一份薪水的规则。<bookmark mark='b'/>马塞洛·阿雷纳斯、莱奥波尔多·贝尔托西和"
        "扬·霍米茨基提议，同时以每一种极小的方式修复它。一次修复是数据的一个极大一致部分：恰好就是第三章的剩余集。<bookmark mark='c'/>一个答案如果在每次修复中"
        "都成立，就是确定的，这是第十章的怀疑策略。<bookmark mark='d'/>鲍勃挣四万：确定。安挣得多于四万五千：确定，因为她的两份薪水都是。<bookmark mark='e'/>安"
        "挣五万：不确定。一致查询回答就是在数据库里运行的AGM部分交。",
    "A modern version of the problem.":
        "这个问题的一个现代版本。<bookmark mark='a'/>一个知识库，或一个语言模型，相信一名足球运动员效力于巴塞罗那，因而住在西班牙，背景事实是：巴塞罗那的球员住在"
        "西班牙，巴黎的球员住在法国，只能有一个俱乐部、一个国家。<bookmark mark='b'/>消息：他现在效力于巴黎。<bookmark mark='c'/>局部编辑只翻转俱乐部，其余什么都"
        "不碰。推理机发现结果与背景不一致：他效力于巴黎，却住在西班牙。<bookmark mark='d'/>AGM修正移到与消息和背景都一致的最近世界：巴黎、法国，而不是西班牙。"
        "推论随着编辑一起改变。<bookmark mark='e'/>编辑大型语言模型内部事实的方法，如ROME和MEMIT，能很好地改变目标事实，但罗伊·科恩及其合作者发现，它们常常恰恰"
        "漏掉了这些涟漪效应。它们缺少的，正是第一条AGM公设：对后承的封闭。",
    "What do machines need from this part?":
        "机器需要从本部分得到什么？<bookmark mark='a'/>一个可能性的排序，而不只是事实的清单，这样它们才知道放弃什么。<bookmark mark='b'/>封闭性，这样推论才会随改变"
        "而动。<bookmark mark='c'/>记忆，这样反复的修正才能保留消息不涉及的东西。<bookmark mark='d'/>带例外的缺省，以及处理它们之间冲突的策略。"
        "<bookmark mark='e'/>还有对“如果”的谦逊：条件句不只是又一些待存储的事实。",
    # ------------------------------------------------------------------ Outro
    "Let's gather what we built.":
        "让我们把搭建的东西汇总一下。<bookmark mark='a'/>三种改变方式，以及更新。<bookmark mark='b'/>AGM公设，经过检验，以及实现它们的球面与剩余集。"
        "<bookmark mark='c'/>用秩来改了再改。<bookmark mark='d'/>拉姆齐检验与加登福斯的定理。<bookmark mark='e'/>反事实条件句，以及刘易斯的平凡性定理，它们一起"
        "构成本部分的砖。<bookmark mark='f'/>受到质疑的肯定前件式，以及缺省的逻辑。<bookmark mark='g'/>还有相互攻击的论证，以及会修正的机器。",
    "The Reasoner has three new modules.":
        "推理机有了三个新模块。<bookmark mark='a'/>修正：在球面上的扩充、修正和收缩，穷举检验的AGM公设与达尔维什--珀尔公设，以及加登福斯的定理。条件句："
        "反事实模型与平凡性搜索。以及可废止推理：缺省外延、Z系统、KLM规则，以及潘明勇的框架。<bookmark mark='b'/>墙也有了它的第十四块砖。",
    "Six problems, with full solutions":
        "六道习题，完整解答在本部分的笔记里。<bookmark mark='a'/>在一个排序上的修正与收缩；全交修正与补充公设；迭代修正，自然的与失忆的；一个反事实模型；"
        "换个数字的刘易斯证明；以及一个论辩框架。在这里暂停，试着做一做。",
    "Where this comes back.":
        "它们会在哪里再出现。<bookmark mark='a'/>归纳与确证，在第15部分。反事实与因果，在第17部分。科学中的理论变化，在第18部分。定律与机遇，在第24部分。"
        "以成像来选择的因果决策论，在第33部分。还有会推理、修正和论辩的机器，在终章。<bookmark mark='b'/>下一部分，第15部分：归纳问题。",
    "The books and papers this":
        "本部分所依据的书和论文都在屏幕上，也在笔记里。感谢观看。",
}
