"""Chinese narration for cs25: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第25部分：不可判定"

CHAPTERS = {
    "Hook": "三个问题，一个答案",
    "Classes": "1. 可判定与可识别",
    "Reductions": "2. 映射归约",
    "Rice": "3. Rice 定理",
    "Recursion": "4. 知道自己代码的程序",
    "Pcp": "5. Post 对应问题",
    "Tiles": "6. 铺满平面",
    "Hilbert": "7. 希尔伯特第十问题",
    "Godel": "8. 经由停机问题的 Gödel",
    "Degrees": "9. 谕示与算术层级",
    "Kolmogorov": "10. Kolmogorov 复杂度",
    "Omega": "11. Chaitin 的 Omega",
    "Beavers": "12. 再谈忙碌的海狸",
    "Boundary": "13. 可判定性在哪里终止",
    "Wild": "14. 野外的不可判定性",
    "Frontier": "15. 前沿：其他环上的希尔伯特第十问题",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Here are three questions from three different worlds.":
        "这里有来自三个不同世界的三个问题。<bookmark mark='a'/>第一个，几何。这里有十一块边缘涂色的正方形砖。用它们的复制品能铺满整个平面，"
        "并且相接的边颜色总相同吗？<bookmark mark='b'/>计算机搜索立刻就能找到一块十二乘十二的拼片，更大的也行。但它从来找不到一个重复的图案，"
        "而这不是偶然。<bookmark mark='c'/>第二个，数论。有没有整数 x 和 y，使得 x 的平方减去六十一倍 y 的平方等于一？费马在1657年把它当作挑战"
        "提了出来。<bookmark mark='d'/>把 y 一直试到七千八百万，二十秒里一无所获。最小的解里，x 接近十八亿。<bookmark mark='e'/>第三个，程序。"
        "一个程序能不读取自己的文件，就精确地打印出自己的源代码吗？<bookmark mark='f'/>能：这里有一个 Python 的，我们还用 Pebble 语言写了一个"
        "并运行了它。<bookmark mark='g'/>这一部分讲的是把它们连在一起的那个意外。这些问题中的每一个，都是某个没有算法能解决的一般问题的特例，"
        "而原因每一次都是第1部分的停机问题。",
    "Part 25 of Computer Science, Built: Undecidable.":
        "计算机科学，从零搭建，第25部分：不可判定。第五幕开始：极限与秘密。<bookmark mark='a'/>这一部分包括：哪些问题可以判定，哪些只能识别，"
        "以及如何把不可判定性从一个问题搬到另一个问题；Rice 定理，它禁止了几乎所有关于程序行为的问题；打印自身的程序；多米诺、砖块和丢番图方程，"
        "每一个里面都藏着一台图灵机；从停机问题证明的 Gödel 不完备定理；谕示；Kolmogorov 复杂度与 Chaitin 的 Omega；以及再一次的忙碌海狸，"
        "在那里可证明性本身也走到了尽头。",
    # ------------------------------------------------------------------ Classes
    "Chapter one. Decidable, and recognizable.": "第1章。可判定，与可识别。",
    "Part 1 proved that the halting problem cannot be decided.":
        "第1部分证明了停机问题不可判定。这一部分把这幅图画得更精确。<bookmark mark='a'/>一个语言是可判定的，如果有某台机器总会停机并正确回答"
        "是或否。<bookmark mark='b'/>它是可识别的，也叫递归可枚举，如果有某台机器对每个成员都停机并回答是，而对其余的允许永远运行下去。你终究会"
        "知道“是”；却可能永远不知道“否”。<bookmark mark='c'/>它是补可识别的，如果它的补集可识别：有机器能确认每一个“否”。<bookmark mark='d'/>"
        "核心的例子是 K：那些在得到自己的描述时会停机的机器的描述。<bookmark mark='e'/>K 是可识别的：只要运行这台机器，它一停就说是。那就是第1部分"
        "的通用机。<bookmark mark='f'/>但它不可判定；那是第1部分的对角线论证。",
    "Draw the classes.":
        "把这些类画出来。<bookmark mark='a'/>左边是可识别语言，右边是补可识别语言。<bookmark mark='b'/>它们的交集恰好是可判定语言。给定一个语言的"
        "识别器和它补集的识别器，让两者轮流各走一步并排运行。每个输入都属于某一边，所以总有一个会停下，你就知道答案了。<bookmark mark='c'/>K 在左边。"
        "所以它的补集，也就是在自身上永远运行的机器，不可能是可识别的，否则 K 就可判定了。<bookmark mark='d'/>还有些问题哪一边都不在。一台机器是否"
        "在每个输入上都停机，叫作 TOT，任何有限的证据都无法从任何一方确认它。第9章会测量它在外面有多远。",
    # ------------------------------------------------------------------ Reductions
    "Chapter two. Mapping reductions.": "第2章。映射归约。",
    "Almost every impossibility proof after the first one is a reduction.":
        "第一个不可能性证明之后，几乎每一个都是归约。<bookmark mark='a'/>说 A 映射归约到 B，如果有一个可计算函数 f，把每个关于 A 的问题变成一个答案"
        "相同的关于 B 的问题：成员落在 B 里面，非成员落在外面。<bookmark mark='b'/>那么 B 的判定器就给出 A 的判定器：算出 f，再去问。<bookmark "
        "mark='c'/>倒过来读，如果 A 不可判定，B 也必然不可判定。要证明一个新问题不可能，就证明停机问题能归约到它。",
    "Here is the start of the catalogue.":
        "这是这份目录的开头。<bookmark mark='a'/>一台机器是否接受给定输入，是可识别而不可判定的，因为 K 就是把机器运行在它自身上的特例。一台机器是否"
        "什么都不接受，是补可识别而不可判定的。两台机器是否接受同一个语言，哪一边都不在。而一台机器是否在每个输入上都停机，离得更远。<bookmark "
        "mark='b'/>技巧总是同一个：造一台新机器，忽略它自己的输入，去模拟那个困难的情形。<bookmark mark='c'/>这里，造一台 M′：如果 M 接受 w，"
        "它就接受一切，否则什么都不接受。问 M′ 是否什么都不接受，就是在问 M 是否接受 w。<bookmark mark='d'/>一次只做一个问题很乏味。下一章一次把"
        "它们全做掉。",
    # ------------------------------------------------------------------ Rice
    "Chapter three. Rice's theorem.": "第3章。Rice 定理。",
    "Henry Rice proved in 1953 that the halting problem is not an isolated case but the rule.":
        "Henry Rice 在1953年证明，停机问题不是孤立的个案，而是常态。<bookmark mark='a'/>如果一个程序性质只取决于程序计算什么，即它的输入输出行为，"
        "而不取决于它怎么写，就称它是语义的。<bookmark mark='b'/>如果有些程序有它、有些没有，就称它是非平凡的。<bookmark mark='c'/>在零上停机，"
        "从不除以零，计算一个排序函数，与给定程序等价：全都是语义的，全都非平凡。<bookmark mark='d'/>Rice 定理说，每一个这样的性质都不可判定。证明"
        "只是一个构造。假设那个从不作答的程序没有这个性质，而某个程序 Y 有。<bookmark mark='e'/>给定任意机器 M 和输入 w，造出 M′：在输入 x 上，"
        "先在 w 上运行 M，如果它结束了，再在 x 上运行 Y。<bookmark mark='f'/>如果 M 在 w 上停机，M′ 计算的恰好就是 Y 所计算的，所以它有这个性质。"
        "否则 M′ 对什么都不作答，所以没有。<bookmark mark='g'/>这个性质的判定器就会判定停机。如果是那个从不作答的程序有这个性质，就把论证用在它的"
        "补上。",
    "This shapes real software.":
        "这塑造了真实的软件。<bookmark mark='a'/>Fred Cohen 在1987年证明，没有程序能检测出每一种病毒，因为行为恶意是一个语义性质。<bookmark "
        "mark='b'/>没有编译器总能找到最好的等价程序，甚至找不全所有的死代码。<bookmark mark='c'/>也没有静态分析器能既可靠，从不漏掉 bug，又完备，"
        "从不误报。<bookmark mark='d'/>实践靠近似逃出去。类型检查器会拒绝一些正确的程序，正如第14部分所示；分析器宁可多报警告。<bookmark "
        "mark='e'/>或者限制语言，直到问题变得可判定，第54部分会在这样的限制之内证明真实程序的正确性。<bookmark mark='f'/>注意 Rice 没有禁止什么。"
        "关于程序文本的问题，它有多少个状态，是否含有循环，仍然很容易。",
    # ------------------------------------------------------------------ Recursion
    "Chapter four. Programs that know their own code.": "第4章。知道自己代码的程序。",
    "Can a program print its own source?":
        "一个程序能打印出自己的源代码吗？最直接的尝试会失败：打印语句必须包含自己的文本，而那段文本又包含打印语句，没完没了。<bookmark "
        "mark='a'/>诀窍是把程序拆成两半。在这个 Python 例子里，字符串 s 是整个程序的模板，留着一个洞。打印语句用加了引号的字符串自己去填这个洞。"
        "<bookmark mark='b'/>我们的 Pebble 语言没有字符串格式化，所以它的自打印程序更长：七百五十九行。其中大多数行把程序的其余部分存成数字，"
        "每个字符一个。<bookmark mark='c'/>然后尾部先从这些数据打印出头部，再打印每一条赋值语句，最后打印尾部。A 部分描述 B 部分；B 部分把 A 打印"
        "两遍，一遍作为代码，一遍作为它所编码的文本。<bookmark mark='d'/>我们在模拟器上运行了它：九万九千条指令，输出就是源代码，逐字节相同。",
    "Stephen Kleene turned the trick into a theorem in 1938.":
        "Stephen Kleene 在1938年把这个诀窍变成了定理。<bookmark mark='a'/>对于任何可计算的程序变换方式，都有一个程序的行为与它自己的变换结果完全"
        "一样。<bookmark mark='b'/>在实践中：一个程序总能得到自己的描述，然后拿它做任何想做的事。<bookmark mark='c'/>自打印程序是最简单的情形，"
        "程序只是把文本打印出来。<bookmark mark='d'/>这里用三行再讲一次停机问题。假设 H 能判定停机。写一个程序 R：取得自己的代码，问 H R 是否停机，"
        "然后反着做：H 说停机它就循环，H 说循环它就停机。H 在 R 上错了。<bookmark mark='e'/>不需要对角线表格，也不需要列出所有机器：自指只是一种"
        "编程技巧。<bookmark mark='f'/>正是同一个诀窍驱动着自我复制的病毒、第8章里 Gödel 的自指语句，以及 Ken Thompson 的特洛伊编译器，第55部分"
        "会把它造出来再抓住它。",
    # ------------------------------------------------------------------ Pcp
    "Chapter five. Post's correspondence problem.": "第5章。Post 对应问题。",
    "Here is a puzzle with no machines in it.":
        "这是一个里面没有机器的谜题。<bookmark mark='a'/>每张多米诺上面有一个字符串，下面有一个字符串。每种你想用几张就用几张，顺序随意，如果上面"
        "一行和下面一行拼出同一个字符串，你就赢了。<bookmark mark='b'/>对这四张，搜索找到一个五张的匹配：二、一、三、二、四。<bookmark mark='c'/>"
        "两行读出来都是 a b c a a a b c。<bookmark mark='d'/>Post 对应问题问的是：对任意一组有限的多米诺，匹配是否存在。<bookmark mark='e'/>"
        "Emil Post 在1946年证明，没有算法能回答它。搜索找到匹配时能确认它，但一般而言，没有什么能确认匹配不存在。",
    "Why are dominoes as hard as machines?":
        "为什么多米诺和机器一样难？<bookmark mark='a'/>拿一台很小的图灵机：在状态 q 读到一，它向右移动进入状态 p；在 p 读到零，它接受。<bookmark "
        "mark='b'/>我们把它变成多米诺。起始多米诺上面只有一个井号，下面是整个第一个格局。步骤多米诺改写读写头附近的内容。复制多米诺把纸带其余部分搬过去。"
        "清理多米诺让接受状态把纸带吞掉，最后一张多米诺把两行收尾。<bookmark mark='c'/>下面一行总比上面领先一个格局，所以上面要追上，唯一的办法就是"
        "一步一步写出下一个格局。<bookmark mark='d'/>我们的搜索找到了十三张的匹配。读井号之间的内容：q 一 零，然后一 p 零，然后一 零 a。那就是这台机器"
        "的接受过程。<bookmark mark='e'/>匹配存在当且仅当机器接受，所以多米诺的算法就会判定接受。Sipser 的教科书再加一个小技巧，强制起始多米诺放在最前面；"
        "思想都在这里了。",
    "How does undecidability show up in practice?":
        "不可判定性在实践中是什么样子？<bookmark mark='a'/>我们随机抽了两万组三张的多米诺，每个字符串一到三位。大多数没有搜索能找到的匹配；有匹配的"
        "那些，大多只用一张多米诺。<bookmark mark='b'/>我们抽到的最长的最短匹配是十五张。<bookmark mark='c'/>但这四张多米诺，是专门搜寻困难实例的"
        "爱好者找到的，它们最短的匹配也要两百零六张，我们的搜索证实了这一点。最短匹配能有多长，没有可计算的上界；如果有，我们只要搜索到那个上界就能判定"
        "这个问题。<bookmark mark='d'/>到底从哪里开始变得不可能？两张多米诺时问题可判定，这是1982年的定理。五张或更多时不可判定，由 Turlough Neary "
        "在2015年证明。<bookmark mark='e'/>三张和四张仍是未解之谜。",
    "Part 12 promised a proof that nobody can always detect an ambiguous grammar.":
        "第12部分许诺过一个证明：没有人总能检测出有歧义的文法。就在这里。<bookmark mark='a'/>从任意一组多米诺出发，造出这个文法。T 推导出某个多米诺"
        "序列的上半部分，后面跟着这个序列编号的倒序。B 对下半部分做同样的事。<bookmark mark='b'/>末尾的标记准确记录了用了哪些多米诺，所以每一半本身"
        "都没有歧义。<bookmark mark='c'/>一个字符串有两棵语法树，只可能一棵经由 T，一棵经由 B，且标记相同：同样的多米诺，上半部分拼出的字符串与下半部分"
        "相同。那就是一个匹配。<bookmark mark='d'/>所以文法有歧义当且仅当多米诺有匹配，判定歧义就会判定 Post 的问题。<bookmark mark='e'/>同样的构造"
        "还说明，两个文法是否有公共字符串，或者一个文法是否生成所有字符串，也都不可判定。语法分析器生成器于是改为报告冲突；那是一种近似，带着 Rice 的"
        "精神。",
    # ------------------------------------------------------------------ Tiles
    "Chapter six. Tiling the plane.": "第6章。铺满平面。",
    "In 1961 Hao Wang asked a question about square tiles with coloured edges.":
        "1961年，王浩问了一个关于边缘涂色的正方形砖的问题。<bookmark mark='a'/>不许旋转，两块砖相接的地方，边的颜色必须一致。给定一组有限的砖，"
        "它们的复制品能铺满整个平面吗？<bookmark mark='b'/>对这十一块，回溯搜索很容易找到正方形拼片：十二乘十二用了四万五千次尝试，二十乘二十用了"
        "四百万次。<bookmark mark='c'/>王浩猜想，任何能铺满平面的砖组，也能用一个重复的图案周期性地铺满。周期性的铺砌可以折叠到环面上，所以我们搜索了"
        "每一个小环面。每一个能搜完的都不可能。<bookmark mark='d'/>那是因为这些正是 Emmanuel Jeandel 和 Michael Rao 在2015年给出的十一块砖："
        "它们能铺满平面，但永远不是周期性的，而且他们证明了没有更小的砖组能做到这一点。",
    "Why should tiles be hard?":
        "砖块为什么会难？<bookmark mark='a'/>把一台图灵机的运行写成一张表，每一步一行，每一行是那一时刻的纸带，读写头所在的格子标上状态。为每一种"
        "格子做一块砖。<bookmark mark='b'/>选好边的颜色，使一行砖后面只能接上代表机器下一步的那一行。<bookmark mark='c'/>那么这些砖能铺满平面，"
        "恰好当机器永远运行，判定铺砌就会判定停机。<bookmark mark='d'/>Robert Berger 在1966年证明了这一点。难点在于强迫计算在每个地方、每个尺度上"
        "都发生，这需要一组只能非周期地铺砌的砖。他的那组有两万零四百二十六块。<bookmark mark='e'/>Raphael Robinson 把它降到六种形状，Roger "
        "Penrose 降到两种，Jarkko Kari 和 Karel Culik 降到十三块 Wang 砖，Jeandel 和 Rao 降到十一块。",
    "The sequence ended in 2023, with an amateur.":
        "这个序列在2023年由一位业余爱好者画上了句号。<bookmark mark='a'/>David Smith，一位喜欢摆弄形状的退休印刷技师，找到了一块单独的砖，能铺满平面，"
        "但只能非周期地铺。他和 Joseph Myers、Craig Kaplan、Chaim Goodman-Strauss 一起证明了它。<bookmark mark='b'/>它叫作“帽子”：十三个顶点，"
        "由六边形网格切出的八个风筝形组成。<bookmark mark='c'/>帽子还需要它的镜像；两个月后，同一个团队找到了“幽灵”，它不需要镜像。<bookmark "
        "mark='d'/>它回答了“einstein 问题”，德语意思是“一块石头”，这个问题自 Berger 的非周期砖组以来一直悬而未决。<bookmark mark='e'/>而且仍然"
        "成立的是：对任意一组有限的砖，没有算法能判断它能否铺满平面。",
    # ------------------------------------------------------------------ Hilbert
    "Chapter seven. Hilbert's tenth problem.": "第7章。希尔伯特第十问题。",
    "In 1900 David Hilbert asked for a process that decides":
        "1900年，David Hilbert 要求一种过程，对任何整系数多项式方程，判定它是否有整数解。<bookmark mark='a'/>Pell 方程说明了为什么搜索不够。D 等于"
        "十三时，最小解的 x 是六百四十九；六十一时，是一个十位数；九百九十一时，三十位。<bookmark mark='b'/>对 y 暴力搜索，十三的解要一百八十次尝试，二十九的要"
        "一千八百次，而六十一，二十秒里七千八百万次尝试一无所获。<bookmark mark='c'/>对 Pell 方程我们很幸运：连分数立刻就能找到答案，而且 Lagrange 证明了解总是存在。<bookmark mark='d'/>但一般"
        "来说，一次一无所获的搜索什么也没证明。答案可能在更远处，也可能根本没有。Hilbert 希望有一种方法，总能知道是哪一种。",
    "The answer took seventy years and four people.":
        "答案用了七十年和四个人。<bookmark mark='a'/>如果一个数集恰好是使某个多项式方程有解的参数之集，就称它是丢番图集。<bookmark mark='b'/>1961年，"
        "Martin Davis、Hilary Putnam 和 Julia Robinson 证明，只要指数运算是丢番图的，每个可识别集就都是丢番图集。<bookmark mark='c'/>1970年，"
        "二十二岁的 Yuri Matiyasevich 补上了缺口：关系 y 等于二的 x 次方是丢番图的，构造建立在斐波那契数之上。<bookmark mark='d'/>所以可识别集"
        "和丢番图集是同一回事。<bookmark mark='e'/>特别地，存在一个多项式，它有解恰好当第 n 号机器在自身上停机。<bookmark mark='f'/>Hilbert 问题"
        "的过程就会判定停机。这样的过程不存在。",
    "A striking corollary.":
        "一个惊人的推论。<bookmark mark='a'/>素数是一个可识别集，所以它是丢番图的，James Jones、佐藤大八郎、和田秀男和 Douglas Wiens 在1976年把这个"
        "多项式写了出来：二十六个变量，字母表里每个字母一个，次数二十五。<bookmark mark='b'/>代入任意非负整数。只要值是正的，它就是素数，而且每个素数"
        "都会出现。<bookmark mark='c'/>诀窍在于它的形状：k 加二，乘以一减去一串平方和。这只在每个平方都为零时为正，也就是十四个方程同时成立时，而它们"
        "成立恰好当 k 加二是素数。<bookmark mark='d'/>没人会这样找素数；随机输入几乎总给出负值。要点在于，素性和停机一样，可以写成一个方程。",
    # ------------------------------------------------------------------ Godel
    "Chapter eight. Gödel, through halting.": "第8章。经由停机问题的 Gödel。",
    "In 1931 Kurt Gödel needed arithmetic to talk about itself.":
        "1931年，Kurt Gödel 需要让算术谈论它自己。<bookmark mark='a'/>给每个符号一个编码数。<bookmark mark='b'/>然后把一个公式编码成素数幂的乘积："
        "二的第一个符号编码次方，乘以三的第二个符号编码次方，依此类推。零等于零是二乘二十七乘五：两百七十。一句“加零什么都不改变”的短陈述有四十七位。"
        "<bookmark mark='c'/>因式分解就能还原公式，所以什么都没丢。<bookmark mark='d'/>证明是一串公式，所以它也有一个编号，而一个数是否是另一个数的"
        "证明，是一项机械的检查。第1部分对机器做过同样的事，用的是描述字符串。Gödel 最先为逻辑做了这件事。",
    "Here is Gödel's first theorem, proved from Part 1's result in a minute.":
        "这是 Gödel 第一定理，用第1部分的结果一分钟就能证明。<bookmark mark='a'/>一个理论是一组公理和证明规则，机械到一个程序能列出它的全部定理。"
        "<bookmark mark='b'/>假设它是可靠的，只证明真的东西，并且强到能陈述一台机器在某个输入上停机。普通算术就可以。<bookmark mark='c'/>再假设它能"
        "证明每一条形如“机器 M 在 w 上不停机”的真命题。<bookmark mark='d'/>那我们就能判定停机。在 w 上运行 M，同时列举定理，寻找“M 不停机”。"
        "<bookmark mark='e'/>如果 M 停机，运行会结束。如果不停机，证明会出现。无论哪种我们都得到答案，而可靠性保证它正确。<bookmark mark='f'/>这不可能。"
        "所以存在真命题，说某台机器永远运行，而这个理论无法证明。每一个可靠的算术理论都是不完备的。",
    "The proof says some such statement exists.":
        "证明说这样的命题存在。递归定理让我们把它写出来。<bookmark mark='a'/>程序 R 取得自己的源代码，也就是第4章的诀窍，然后从短到长搜索理论中的每个"
        "证明，寻找“R 永不停机”的证明。找到了，它就停下。<bookmark mark='b'/>如果理论证明了 R 永不停机，R 就会找到这个证明并停机，理论就证明了一件"
        "假的事。<bookmark mark='c'/>所以可靠的理论永远不会证明它，R 永远搜索下去，而“R 永不停机”这个命题是真的，也是不可证的。<bookmark mark='d'/>"
        "它实际上在说：我不能被证明。这就是写成程序的 Gödel 语句。<bookmark mark='e'/>Gödel 自己的版本要求更少：只需理论是一致的，再加上 Barkley "
        "Rosser 在1936年的一个改进。",
    "Push one step further.":
        "再推进一步。<bookmark mark='a'/>我们刚才的论证本身可以在理论内部进行。理论能证明：如果我是一致的，那么 R 永不停机。<bookmark mark='b'/>所以"
        "如果它还能证明自己的一致性，它就能证明 R 永不停机，而我们刚看到它做不到。<bookmark mark='c'/>这就是第二不完备定理：没有一个强到足以做算术的"
        "一致理论能证明自己的一致性。<bookmark mark='d'/>它终结了 David Hilbert 在1920年代领导的纲领：用有限的、机械的手段证明全部数学的一致性。"
        "<bookmark mark='e'/>注意这个命题的形状。集合论的一致性说的是：某一个程序，那个寻找矛盾的程序，永不停机。<bookmark mark='f'/>这就是为什么第1部分"
        "能造出一台图灵机，它的忙碌海狸值集合论无法确定。第12章会回到这里。",
    # ------------------------------------------------------------------ Degrees
    "Chapter nine. Oracles and the arithmetic hierarchy.": "第9章。谕示与算术层级。",
    "Is halting the hardest problem there is?":
        "停机是最难的问题吗？<bookmark mark='a'/>Turing 在1939年问：如果一台机器有一个魔盒，一个谕示，能一步回答某个集合的成员资格，它能做什么？如果一台"
        "带 B 谕示的机器能解一个问题，就说这个问题图灵归约到 B。<bookmark mark='b'/>把停机集作为谕示交给一台机器。每一个形如“某个搜索会成功吗”的问题，"
        "现在都只是一步。<bookmark mark='c'/>但第1部分的对角线论证对谕示机同样有效：它们无法判定谕示机是否停机。那是一个新的、更难的问题，K 的跳跃。"
        "<bookmark mark='d'/>再给它一个谕示，再跳一次。有一座无限的问题之塔，每一个都严格比前一个更难。",
    "There is a ruler for this tower: count the alternating quantifiers.":
        "这座塔有一把尺子：数交替出现的量词。<bookmark mark='a'/>最底层是程序靠有界搜索就能解决的问题：x 是素数吗，M 在一百步内停机吗。<bookmark "
        "mark='b'/>前面加一个存在量词，存在一个时刻 t 使 M 已经停机，就得到 sigma 一：停机本身，以及第7章的方程。<bookmark mark='c'/>一个全称量词给出"
        "pi 一：M 永不停机。Goldbach 猜想和黎曼猜想也是，集合论的一致性也是；每一个都说某个搜索永远不会成功。<bookmark mark='d'/>两个量词。只在有限多个"
        "输入上停机是 sigma 二。<bookmark mark='e'/>在每个输入上都停机，TOT，是 pi 二：对每个输入，都有一个时刻。孪生素数猜想、Collatz 猜想，以及 P "
        "不等于 NP 也是，后者正是第26部分的主题。<bookmark mark='f'/>而在除有限多个以外的所有输入上停机是 sigma 三。<bookmark mark='g'/>Emil Post "
        "在1948年证明，每一层恰好是识别器借助下一层跳跃的谕示所能做的，而这些机器问题在各自的层级上都是完全的。",
    "One last question about the recognizable sets.":
        "关于可识别集的最后一个问题。<bookmark mark='a'/>到目前为止我们遇到的每一个不可判定集，都恰好和停机一样难。总是这样吗？<bookmark mark='b'/>Emil "
        "Post 在1944年提出这个问题，花了十二年才解决。莫斯科的 Albert Muchnik 和哈佛的本科生 Richard Friedberg 各自独立地造出两个可识别集，谁也不能"
        "计算对方，所以两者都严格位于可判定集和 K 之间。<bookmark mark='c'/>他们的技术，优先方法，分阶段构造这些集合，满足一张无限的要求清单，每个要求"
        "只被排在它前面的要求干扰有限多次。<bookmark mark='d'/>Gerald Sacks 后来证明，任意两个这样的度之间都还有另一个：这个结构是稠密的。<bookmark "
        "mark='e'/>然而人们找到的每一个自然问题，要么可判定，要么恰好和停机一样难。没人知道为什么。",
    # ------------------------------------------------------------------ Kolmogorov
    "Chapter ten. Kolmogorov complexity.": "第10章。Kolmogorov 复杂度。",
    "Andrey Kolmogorov, Ray Solomonoff and Gregory Chaitin":
        "Andrey Kolmogorov、Ray Solomonoff 和 Gregory Chaitin 在1960年代各自独立地用程序来度量信息。<bookmark mark='a'/>一个字符串的 Kolmogorov "
        "复杂度，是打印它的最短程序的长度。<bookmark mark='b'/>压缩器能让人感受一下它。我们给三个压缩器各喂了六种十万字节的数据。随机字节完全缩不了；"
        "输出反而略大。<bookmark mark='c'/>英文文本缩到约三分之一。圆周率的数字缩到百分之四十三，那恰好是用二进制写一个数字的代价。<bookmark "
        "mark='d'/>但在 Kolmogorov 的意义上，圆周率的数字并不随机：一个十九行的函数就能把它们全部打印出来。压缩器找不到那个程序。<bookmark "
        "mark='e'/>每个压缩器给出的都是复杂度的上界，而不是它的值，这一章会说明为什么没有什么能做得更好。",
    "Shortest program in which language?":
        "用哪种语言的最短程序？<bookmark mark='a'/>不变性定理说，这几乎无关紧要。对任意两台通用机，复杂度至多相差一个常数。<bookmark mark='b'/>证明："
        "U 是通用的，所以某个固定的程序能让 U 解释 V。<bookmark mark='c'/>把这个解释器放在 x 的最短 V 程序前面，就得到 x 的一个 U 程序，只比原来多出"
        "解释器的长度。<bookmark mark='d'/>交换角色，两种度量就相差不超过一个常数。<bookmark mark='e'/>所以一个字符串里的信息属于这个字符串本身。"
        "<bookmark mark='f'/>在 Python 和 Pebble 语言之间，这个常数就是用其中一种写的另一种的解释器的大小。",
    "Now a proof that takes a single line.":
        "现在是一个只要一行的证明。<bookmark mark='a'/>数一数程序。长度为零的有一个，长度为一的有两个，长度为二的有四个。所有短于 n 位的程序加起来是"
        "二的 n 次方减一个：比长度为 n 的字符串少。<bookmark mark='b'/>更一般地，短于 n 减 k 位的程序，至多只能打印出长度为 n 的字符串中二的负 k 次方"
        "那么大的比例。<bookmark mark='c'/>一千零二十四个字符串中至多一个能缩短十位，而在每种长度上，都有某个字符串根本缩不短。<bookmark mark='d'/>"
        "这样的字符串称为随机的：它没有比自身更短的描述。这也说明，每个压缩器都会把某些文件变大，就像我们的随机字节那样。",
    "Now the twist.":
        "现在是转折。<bookmark mark='a'/>1906年，Bertrand Russell 发表了一个他归功于图书管理员 G. G. Berry 的悖论：不能用少于六十个字母命名的最小的数。"
        "这句话用更少的字母命名了它。把这个悖论变成程序。<bookmark mark='b'/>如果复杂度可计算，这个函数就会返回第一个复杂度超过 L 的字符串。<bookmark "
        "mark='c'/>但把数 L 写进去之后，这个函数只有大约 log L 位，再加一个常数，而 L 很大时这远小于 L。<bookmark mark='d'/>一个短程序打印出了一个"
        "没有短程序的字符串。所以复杂度无法计算。<bookmark mark='e'/>Gregory Chaitin 把这一点推进到逻辑。不去计算 K，而是在一个可靠理论的证明里寻找"
        "“某个字符串的复杂度超过 L”的证明。<bookmark mark='f'/>同样的论证说明，一旦 L 超过某个取决于理论的常数，搜索必然失败。几乎每个字符串都是"
        "随机的，而超过某个固定的大小，没有理论能证明其中任何一个是随机的。",
    # ------------------------------------------------------------------ Omega
    "Chapter eleven. Chaitin's Omega.": "第11章。Chaitin 的 Omega。",
    "In 1975 Chaitin packed the halting problem into a single number.":
        "1975年，Chaitin 把停机问题装进了一个数里。<bookmark mark='a'/>随机挑一个程序：每一位抛一次硬币，直到这些位拼出一个完整的程序。<bookmark "
        "mark='b'/>如果没有程序是另一个程序的开头，这些概率加起来至多为一。<bookmark mark='c'/>Omega 就是你得到的程序终究会停机的概率：零和一之间的一个"
        "实数。<bookmark mark='d'/>你可以从下方逼近它。把所有程序并排运行，每有一个停机，就加上它的概率。<bookmark mark='e'/>这些和朝着 Omega 攀升，"
        "但没有任何东西会告诉你离它有多近。",
    "We cannot compute Omega, but we can compute a small cousin.":
        "我们算不出 Omega，但能算出一个小表亲。<bookmark mark='a'/>随机抽五千台三状态图灵机，每条规则随机决定写什么、往哪边移、转到另一个状态还是停机。"
        "给每台机器一个不断增长的步数预算，统计已停机的比例。<bookmark mark='b'/>它在攀升，起初很快。到十六步时达到百分之四十五，两千步之后再也没动过。"
        "<bookmark mark='c'/>我们见到的最长的停机运行是十一步。<bookmark mark='d'/>在这里我们知道曲线已经到头，靠的是第1部分：三状态的忙碌海狸运行二十一步，"
        "所以任何运行超过二十一步的三状态机器都永不停机。<bookmark mark='e'/>对一台通用机，这样的界不存在。知道曲线何时到头，就意味着知道每种大小的忙碌海狸。",
    "Omega is a strange number.":
        "Omega 是一个奇怪的数。<bookmark mark='a'/>Cristian Calude、Michael Dinneen 和 Chi-Kou Shu 在2002年为一台特定的通用机算出了前六十四位。对更大的"
        "机器，没人能做到。原因如下。<bookmark mark='b'/>假设你知道前 n 位。把每个程序并排运行，把停机程序的概率加起来，直到总和达到这 n 位。<bookmark "
        "mark='c'/>这时任何不超过 n 位、仍在运行的程序都永远不会停机：如果它停了，它的贡献会把总和推过 Omega。<bookmark mark='d'/>所以 Omega 的几千位"
        "就能解决 Goldbach 猜想、黎曼猜想和集合论的一致性，每一个都是某个短程序的停机问题。<bookmark mark='e'/>由此可知 Omega 是随机的：它的前 n 位"
        "压缩不了超过一个常数。<bookmark mark='f'/>而由第10章，一个可靠的理论只能确定它的有限多位。Robert Solovay 找到了一台通用机，集合论连它的一位"
        "都确定不了。",
    # ------------------------------------------------------------------ Beavers
    "Chapter twelve. Busy beavers, again.": "第12章。再谈忙碌的海狸。",
    "Three speeds of growth.":
        "三种增长速度。<bookmark mark='a'/>循环界限在开始前就固定的程序，逻辑学家称之为原始递归，能计算二的 n 次方、二的塔，以及任何固定层数的这类东西。"
        "<bookmark mark='b'/>第11部分遇到过 Wilhelm Ackermann 的函数，并许诺说明它为什么重要。它可计算，总会结束，却终将超过有界循环能计算的每一个函数。"
        "A 四四已经是一座二的塔，最顶上的指数是六万五千五百三十六。<bookmark mark='c'/>原因又是对角线论证。一个每个程序都会结束的语言，有一个总会结束的"
        "解释器，但这个解释器不能用这个语言写出来。<bookmark mark='d'/>如果能，那么 d 也能：d of x 是解释器在 x 上以 x 为输入运行，再加一。把 d 运行在"
        "它自己的代码上，就得到 d of d 等于 d of d 加一。这就是第14部分提到过的论证，说明了为什么类型化 lambda 演算不能解释它自己。<bookmark mark='e'/>"
        "而第三列连 Ackermann 也超过了。第1部分说过忙碌海狸超过每一个可计算函数。现在给出证明。",
    "The proof is a machine built in three pieces.":
        "证明是一台由三块拼成的机器。<bookmark mark='a'/>任取一个可计算函数 f，由一台有 c 个状态的机器计算。对每个 n，造一台机器，先把 n 写到纸带上，"
        "这要用 n 个状态；<bookmark mark='b'/>然后计算 f 的二 n，这要用 c 个状态；然后把这个数倒数到零，再多几个状态。<bookmark mark='c'/>它有 n 加一个"
        "常数个状态，停机前运行超过 f 的二 n 步。<bookmark mark='d'/>所以 n 加这个常数处的忙碌海狸大于 f 的二 n。<bookmark mark='e'/>一旦 n 大于这个常数，"
        "二 n 处的忙碌海狸就更大。忙碌海狸超过了 f，并且一直领先。<bookmark mark='f'/>没有可计算函数能给它设一个上界。",
    "Part 1 told how the five-state value was proved, and why six may be out of reach.":
        "第1部分讲过五状态的值是怎样证明的，以及为什么六状态也许遥不可及。这里是更大的地图。<bookmark mark='a'/>许多未解问题就是某一台小机器的停机问题。"
        "Tristan Stérin 和 Damien Woods 在2021年给出的一台十五状态机器，停机恰好当 Erdős 错了：他认为第八次方以后的每个二的幂在三进制下都有一个数字二。"
        "一台二十七状态的机器，2015年发布在网上，尚未经过仔细核查，在 Goldbach 猜想不成立时停机。七百四十四个状态编码了黎曼猜想。<bookmark mark='b'/>"
        "所以知道二十七处的忙碌海狸，至少在原则上就能解决 Goldbach：把那台机器运行那么久。<bookmark mark='c'/>而某台几百个状态的机器只在集合论不一致时"
        "停机，所以由第8章，集合论无法证明它的忙碌海狸值。任何可靠的理论都只能确定有限多个值。<bookmark mark='d'/>在六和四百三十二之间的某处，集合论的"
        "知识停住了。究竟在哪里，没人知道。",
    # ------------------------------------------------------------------ Boundary
    "Chapter thirteen. Where decidability ends.": "第13章。可判定性在哪里终止。",
    "Not every mathematical theory is undecidable.":
        "并不是每个数学理论都不可判定。这里是分界线所在。<bookmark mark='a'/>Mojżesz Presburger 在1929年证明，只有加法的整数的真理可以由机器判定，"
        "不过 Michael Fischer 和 Michael Rabin 证明这至少需要双重指数时间。<bookmark mark='b'/>Alfred Tarski 对带加法、乘法和序的实数证明了同样的事，"
        "连同整个欧几里得几何。<bookmark mark='c'/>给整数加上乘法，可判定性就丢了，由第8章。<bookmark mark='d'/>Julia Robinson 证明有理数也好不到哪去，"
        "因为整数可以在其中定义出来。<bookmark mark='e'/>如果只允许方程，不允许“对所有”，在有理数上呢？没人知道。那是这一部分的前沿。<bookmark "
        "mark='f'/>规律是：整数的乘法让数能够编码计算。实数逃脱了，因为没有公式能从中挑出整数。",
    "Undecidability also hides in pure algebra.":
        "不可判定性也藏在纯代数里。<bookmark mark='a'/>Max Dehn 在1911年问：给定一个由有限多个生成元和关系定义的群，你能判定生成元组成的一个词是否等于"
        "单位元吗？Pyotr Novikov 在1955年、William Boone 在1958年找到了没有算法能做到的群。<bookmark mark='b'/>或者拿几个三乘三的整数矩阵。它们按某种"
        "顺序、允许重复的某个乘积，会得到零矩阵吗？Michael Paterson 在1970年证明这不可判定，办法是把 Post 的多米诺变成矩阵。<bookmark mark='c'/>对二乘二"
        "的矩阵，没人知道。",
    "John Conway invented the strangest programming language of all.":
        "John Conway 发明了最奇怪的编程语言。<bookmark mark='a'/>一个程序是一串分数。从一个数开始；反复把它乘以列表中第一个能得到整数的分数；没有这样的"
        "分数时停下。<bookmark mark='b'/>这个列表叫 PRIMEGAME，从二开始。只看二的幂。十九步后，四，也就是二的平方。六十九步后，八。然后是三十二、一百二十八、"
        "二的十一次方。<bookmark mark='c'/>指数恰好是素数，按顺序。我们的运行在不到三百万步里得到了直到一百二十七的每个素数。<bookmark mark='d'/>为什么"
        "行得通？n 里各个素数的指数充当寄存器，每个分数是一条指令，减少某些寄存器、增加另一些。那就是第1部分的计数器机，它是通用的。<bookmark mark='e'/>"
        "所以一串分数是否终究会停下，是不可判定的。",
    "The most famous problem on the boundary is a children's puzzle.":
        "边界上最著名的问题是一个儿童谜题。<bookmark mark='a'/>偶数减半；奇数乘三加一。每个起点都会到达一吗？二十七要一百一十一步，途中爬过九千。<bookmark "
        "mark='b'/>一百万以内，最长的旅程从八十三万七千七百九十九出发：五百二十四步。<bookmark mark='c'/>二的六十八次方以下的每个起点都已检查过。<bookmark "
        "mark='d'/>Conway 在1972年证明，恰好这种形状的规则，即用 n 除以某数的余数来选一个线性映射，可以编码任何程序，所以一般问题不可判定。<bookmark "
        "mark='e'/>Collatz 规则本身也许就是这样的情形之一，真但不可证，也许只是非常难。没人知道是哪一种，而第1部分的 Antihydra 是它的表亲。",
    # ------------------------------------------------------------------ Wild
    "Chapter fourteen. Undecidability in the wild.": "第14章。野外的不可判定性。",
    "Programmers meet undecidability by accident.":
        "程序员会意外地撞上不可判定性。<bookmark mark='a'/>C++ 模板本来是为泛型容器设计的。2003年，Todd Veldhuizen 证明它们构成了一门在编译器内部运行的"
        "完整编程语言，这就是为什么编译器会在一个固定的模板深度停下。<bookmark mark='b'/>2017年，Radu Grigore 证明了 Java 泛型的子类型判定不可判定：没有"
        "编译器总能判断一个类型是否适配另一个。TypeScript 的类型系统也能运行任何程序，它的检查器在一个深度上限处放弃。<bookmark mark='c'/>2019年，Alex "
        "Churchill、Stella Biderman 和 Austin Herrick 用《万智牌》的卡牌造出了一台图灵机，所以判定一个给定局面谁赢是不可判定的。<bookmark mark='d'/>"
        "Stephen Dolan 证明，x86 的 mov 指令单独就是图灵完备的。<bookmark mark='e'/>而第1部分见过的 Conway 生命游戏，能运行由滑翔机组成的图灵机，比如这一个，"
        "沿对角线走过网格。<bookmark mark='f'/>教训是：给任何配置语言、类型系统或规则集足够的能力，关于它的某个问题就会变得不可判定。好的设计会有意识地决定"
        "在哪里停下。",
    "Undecidability reaches physics too.":
        "不可判定性也延伸到了物理。<bookmark mark='a'/>把一种材料建模成网格上的粒子，每个粒子只按同一条局部规则与邻居相互作用。<bookmark mark='b'/>它的"
        "谱隙，是在网格很大的极限下，把系统抬离最低能态所需的能量。<bookmark mark='c'/>有没有谱隙，很大程度上决定了材料的行为。<bookmark mark='d'/>2015年，"
        "Toby Cubitt、David Pérez-García 和 Michael Wolf 证明，对二维晶格，谱隙是否存在是不可判定的。<bookmark mark='e'/>他们的构造就是这一部分的缩影："
        "基态由 Robinson 的非周期砖构成，每块砖里运行一台图灵机，而谱隙是否闭合取决于这台机器是否停机。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen, the frontier.": "第15章，前沿。其他环上的希尔伯特第十问题。",
    "Hilbert asked about the integers.":
        "Hilbert 问的是整数。其他数系呢？<bookmark mark='a'/>高斯整数，形如 a 加 b 根号二的数，一般地，任意数域的整数环。机器能判定一个系数取自这样的数、"
        "要求解也取自这样的数的方程是否有解吗？<bookmark mark='b'/>1978年，Jan Denef 和 Leonard Lipshitz 提出了策略：证明普通整数在更大的环里构成一个丢番图集，"
        "Matiyasevich 定理就能搬过去。<bookmark mark='c'/>1980年代对许多数域做到了，2010年对所有数域也做到了，但要假设一个关于椭圆曲线的未证猜想。<bookmark "
        "mark='d'/>2024年12月，Peter Koymans 和 Carlo Pagano 对每个数域都证明了它，不需任何假设。<bookmark mark='e'/>关键是为每个数域找到在某个二次扩张里"
        "秩不增长的椭圆曲线，而他们是用加性组合找到的，也就是 Green-Tao 关于等差数列中素数的定理所用的工具。<bookmark mark='f'/>Levent Alpöge、Manjul "
        "Bhargava、Wei Ho 和 Ari Shnidman 沿另一条路独立得到了同样的结果。<bookmark mark='g'/>结合早先的工作，这个问题现在在每一个整数上有限生成的无限环上"
        "都不可判定。",
    "The rationals are different.":
        "有理数不一样。<bookmark mark='a'/>在有理数上，像 y 的平方等于 x 的立方减二这样的方程，是一个关于曲线上有理点的问题，那是算术几何的课题，而费马就知道"
        "点三、五。<bookmark mark='b'/>如果整数在有理数里构成一个丢番图集，这个问题就会像以前一样不可判定。<bookmark mark='c'/>但 Barry Mazur 在1992年"
        "猜想，有理点永远不会散布得足以做到这一点，大多数专家相信他。<bookmark mark='d'/>借助量词，整数是可以定义的：2009年的 Bjorn Poonen，以及2016年用"
        "单个“对所有”的 Jochen Koenigsmann。<bookmark mark='e'/>所以有理数的完整理论不可判定，正如第13章所说，但单是方程也许仍然可判定。那是逻辑与数论的"
        "伟大未解问题之一。<bookmark mark='f'/>即使在整数上，只有两个未知数的方程能否判定，也是未知的。",
    "A recurring frontier question is how small an undecidable problem can be.":
        "一个反复出现的前沿问题是：一个不可判定的问题最小能有多小。<bookmark mark='a'/>对自然数上的方程，九个未知数就够了，出自 Matiyasevich 和 James Jones。"
        "在整数上，孙智伟在2021年把它降到十一个。一个未知数时很容易；两个未知数，在整数上，没人知道。<bookmark mark='b'/>Post 的多米诺：五张就够，两张可判定，"
        "三张和四张未解。一台两状态、三符号的图灵机，被 Alex Smith 在2007年证明在一种弱的意义下是通用的。忙碌海狸在四百三十二个状态以下的某处离开集合论，"
        "矩阵致死性则停在二乘二。<bookmark mark='c'/>第三列里的每一个空缺，都是一个关于计算究竟从哪里开始的研究问题。",
    "Five open problems from this part.":
        "这一部分的五个未解问题。<bookmark mark='a'/>有理数上的希尔伯特第十问题。<bookmark mark='b'/>三张或四张多米诺的 Post 问题。<bookmark mark='c'/>"
        "一个中间度的自然问题，从来没人找到过。<bookmark mark='d'/>集合论失去对忙碌海狸掌控的确切位置。<bookmark mark='e'/>以及 Collatz 猜想如果为真，能否"
        "从普通的算术公理证明。<bookmark mark='f'/>这一部分的研究问题取第二个，三张多米诺的情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们造了什么。可判定、可识别与补可识别，以及把不可能性从一个问题带到下一个问题的归约。Rice 定理，它禁止了几乎所有关于程序行为的问题。"
        "打印自己源代码的程序，用 Python，也用 Pebble。多米诺、砖块和丢番图方程，每一个都藏着一台图灵机，还有帽子。从停机证明的 Gödel 定理；谕示与"
        "算术层级；Kolmogorov 复杂度与 Chaitin 的 Omega；以及忙碌海狸，在那里证明走到了尽头。",
    "Where this comes back.":
        "这些会在哪里再出现。第26部分用同样的对角线证明时间层级定理，并提出这一部分无法回答的问题：不是能不能，而是多快。第54部分证明程序正确，靠近似逃出"
        "Rice 定理。第55部分说明访问控制中的安全性不可判定，并在一个自打印程序上造出 Ken Thompson 的特洛伊编译器。第57部分把 Kolmogorov 的思想变成学习"
        "中的奥卡姆剃刀，第58部分把递归变成不动点，那是 Kleene 定理在语义学里的表亲。",
    "In practice.":
        "在实践中。每个静态分析器都是一种近似，在误报和漏报之间权衡，因为 Rice。没有完美的恶意软件扫描器，所以安全依赖沙箱和限制，而不是预测。语言设计者"
        "有意让配置文件、查询语言和某些类型系统达不到图灵完备，好让关于它们的问题保持可判定。编译器给模板和类型检查的深度设上限。而 Dijkstra 的那句话，"
        "测试能显示 bug 的存在却永远不能显示它们不存在，就是改头换面的停机问题。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在这一部分的笔记里。随时暂停。第五道是动手题：一个用 Pebble 语言写的、把自己的源代码倒着打印出来的程序。最后一道标着星号，是研究"
        "问题：它的答案未知，笔记里说明了从哪里入手。",
    "Next time: this part asked what can be computed at all.":
        "下一次：这一部分问的是究竟什么能被计算。第26部分问什么能被快速计算。1956年，Gödel 写信给 John von Neumann，问找到一个证明是否可能和检查一个证明"
        "一样容易。Cook 和 Levin 把那封信变成了一个问题，Karp 在另外二十一个问题里找到了它，而五十年的进攻都失败了。第26部分，P 与 NP。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
