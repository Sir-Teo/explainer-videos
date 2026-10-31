"""Chinese narration for ai2: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第2部分：会思考的机器'

CHAPTERS = {
    'Hook': '四十年才将死',
    'Turing': '1. 机器能思考吗？',
    'Search': '2. 搜索',
    'AStar': '3. A*',
    'Heuristics': '4. 启发式从哪里来',
    'Local': '5. 爬山与退火',
    'Games': '6. 博弈与α-β剪枝',
    'Samuel': '7. 学会下棋的机器',
    'Logic': '8. 逻辑与归结',
    'SAT': '9. 可满足性',
    'Plans': '10. 约束与规划',
    'Knowledge': '11. 知识就是力量',
    'Eliza': '12. ELIZA',
    'Winters': '13. 寒冬',
    'Survives': '14. 留下来的东西',
    'Outro': '回顾、习题，以及它们会在哪里再出现',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'In 1958 Herbert Simon and Allen Newell predicted':
        "1958年，赫伯特·西蒙和艾伦·纽厄尔预言：十年之内，一台数字计算机将成为国际象棋世界冠军，除非规则禁止它参赛。<bookmark mark='a'/>结果用了39年。<bookmark mark='b'/>1997年5月，在纽约，IBM的深蓝以3.5比2.5击败了世界冠军加里·卡斯帕罗夫。",

    'Between those dates lies the first age of artificial intelligence':
        "这两个日期之间，是人工智能的第一个时代，也是本课程讲历史的起点。<bookmark mark='a'/>1950年，阿兰·图灵问：机器能思考吗？<bookmark mark='b'/>1956年，达特茅斯的一次研讨会给这个领域起了名字。<bookmark mark='c'/>程序学会了下跳棋、和人对话、在地图上找路、为机器人规划动作。<bookmark mark='d'/>然后，承诺跑到了成果前面，钱也断了：第一次寒冬。<bookmark mark='e'/>专家系统带来一轮繁荣，它崩溃时，又迎来第二次、更严酷的寒冬。<bookmark mark='f'/>到了最后，是一台创始人们一眼就能认出的国际象棋机器。",

    'The bet of that age was that intelligence could be written down:':
        "那个时代押下的赌注是：智能可以被写下来，<bookmark mark='a'/>写成在各种可能性中的搜索，由经验法则引导；写成博弈中的招法；写成逻辑；写成由专家一条条输入的知识。<bookmark mark='b'/>这场赌局只输了一半。搜索在AlphaZero里运行，逻辑在检查芯片的工具里运行，证明检查器给DeepMind的AlphaProof批改证明，今天的智能体也在做规划。<bookmark mark='c'/>而且本部分的每一个算法，都在这里、在这台电脑上运行，让我们看着它工作。",

    'This is Part 2 of AI, Built.':
        "这是《人工智能，从零搭建》的第2部分。<bookmark mark='a'/>这一部分讲：机器能计算什么、不能计算什么，以及图灵测试；搜索，从广度优先到A星，以及启发式从哪里来；局部搜索和模拟退火；博弈，从极小化极大和α-β剪枝，到塞缪尔的跳棋和深蓝；逻辑、可满足性及其相变，还有约束和规划；最后是知识：专家系统、ELIZA、两次寒冬，以及熬过寒冬留下来的东西。",

    # ------------------------------------------------------------------ Turing
    'Chapter one. Can machines think?':
        '第1章。机器能思考吗？',

    'Before anyone could ask whether machines think':
        "在有人能问机器会不会思考之前，得先有人说清楚机器是什么。阿兰·图灵在1936年做到了。<bookmark mark='a'/>一条分成格子的纸带，每格写一个符号；一个读写头，一次读一格；<bookmark mark='b'/>再加一张有限的规则表：处在这个状态、读到这个符号时，写下一个符号，向左或向右移一格，换到另一个状态。<bookmark mark='c'/>这张表能给一个二进制数加1：看它进位。<bookmark mark='d'/>图灵论证说，一个人按规则能算出的任何东西，这样的机器都能算；而且一台通用机器，从自己的纸带上读入另一台机器的规则表，就能模仿其中任何一台。这就是存储程序计算机的思想。",

    'Turing also showed what no machine can do.':
        "图灵还证明了，有些事任何机器都做不到。<bookmark mark='a'/>假设有某个程序H，能看任何程序P和输入x，并且总能回答：P在x上最终会停下来吗？<bookmark mark='b'/>那就造一个唱反调的程序D：给它一个程序，D去问H，这个程序拿自己的代码当输入时会不会停，然后反着做。<bookmark mark='c'/>现在让D在自己的代码上运行。它停下，恰好当H说它不停的时候；也就是恰好当它不停的时候。<bookmark mark='d'/>所以H不可能存在：一般来说，没有程序能判定程序会不会停机。同一年，阿隆佐·丘奇从另一条路得到了同样的极限。",

    'f"The limit appears even in tiny machines.':
        "这个极限在很小的机器上就会出现。固定两种纸带符号和工作状态的个数，另有一个停机状态。从全0纸带开始：这样的机器最多能运行多久，还能停下来？运行时间最长的那台叫作忙碌海狸，这个名字来自蒂博尔·拉多，1962年。<bookmark mark='a'/>4个状态的冠军，在这里一步画一行，在{d['bb4_steps']}步后停机。<bookmark mark='b'/>5个状态的冠军运行{d['bb5_steps']:,}步；我们重放这些步骤用了{d['bb5_seconds']:.1f}秒。<bookmark mark='c'/>要证明没有别的5状态机器运行得更久，一直等到了2024年，还要靠一份由计算机检查的证明。至于6个状态，没有人知道。",

    'In 1950 Turing turned to thinking itself':
        "1950年，图灵转向了思考本身，他没有给出定义，而是提出了一个游戏。<bookmark mark='a'/>一位提问者和两个看不见的玩家互发打字消息，一个是人，一个是机器，他必须说出谁是谁。<bookmark mark='b'/>他预言，到2000年左右，一位普通的提问者在问了五分钟之后，判断正确的机会不会超过70%。<bookmark mark='c'/>2025年，卡梅伦·琼斯和本杰明·伯根做了这个测试：扮演一个人设的GPT-4.5，有73%的时候被判定为人类，比真人被认出的次数还多。1966年的ELIZA，拿到了23%。",

    'Six years later, in the summer of 1956':
        "六年后，1956年夏天，约翰·麦卡锡、马文·明斯基、纳撒尼尔·罗切斯特和克劳德·香农把研究者们召集到达特茅斯学院，基于这样一个猜想：学习的每一个方面，或者智能的任何其他特征，原则上都可以被描述得足够精确，以至于可以造一台机器来模拟它。麦卡锡的提案给这个领域起了名字：人工智能。<bookmark mark='a'/>艾伦·纽厄尔、克利夫·肖和赫伯特·西蒙带来了一个已经能运行的程序：逻辑理论家。它证明了《数学原理》某一章前52个定理中的38个。<bookmark mark='b'/>它从每个定理倒推到子目标，用经验法则来选择：这是在一棵符号树中的搜索。<bookmark mark='c'/>1976年，纽厄尔和西蒙说出了那个时代的信条：物理符号系统具有通用智能行为的充分必要手段。",

    # ------------------------------------------------------------------ Search
    'Chapter two. Search.':
        '第2章。搜索。',

    'Start, apply moves, look for a goal':
        "从起点出发，施加动作，寻找目标：本部分的一切内容背后，都是这个模式。拿八数码来说：一个三乘三的框里有8块编了号的方块，还有一个空格。<bookmark mark='a'/>每一种摆法是一个状态；一个动作把一块方块滑进空格。<bookmark mark='b'/>目标是方块按顺序排好。<bookmark mark='c'/>这就是一个搜索问题：状态，有代价的动作，起点和目标测试。解能到达目标；最优解以最小的代价到达。<bookmark mark='d'/>八数码有181440个可以到达的状态，恰好是所有摆法的一半：一个奇偶性论证排除了另一半。",

    'f"The simplest strategy is breadth-first search':
        "最简单的策略是广度优先搜索：先看一步之内的所有状态，再看两步的，一圈一圈向外，用一个先进先出的队列保存边界。<bookmark mark='a'/>从目标开始运行，它就绘出了整个谜题的地图。圈越来越大：最宽的一圈在距离{peak}处，有{int(L[peak]):,}个状态。<bookmark mark='b'/>每个状态最多{d['max_depth']}步就能解开，而恰好有{len(d['hardest'])}个需要整整{d['max_depth']}步。广度优先搜索找到的是最短解，因为它处理完一层深度才去看下一层。代价是内存：整个边界。",

    'Search strategies differ only in which frontier state they expand next.':
        "各种搜索策略的区别，只在于下一个扩展边界上的哪个状态。<bookmark mark='a'/>广度优先取最老的。<bookmark mark='b'/>深度优先取最新的，沿着一条分支一直往下钻，再退回来：用的是栈，而不是队列。<bookmark mark='c'/>如果每个状态有b种选择，解在d步深处，广度优先可能要存下大约b的d次方个状态；深度优先保存的状态数大约是b乘以m，其中m是它探索到的最深层数，未必等于最浅解的深度：它可能永远钻下去。<bookmark mark='d'/>迭代加深更早已用于国际象棋，理查德·科尔夫在1985年分析了它的性质，它两者兼得：先深度优先搜到深度1，再到2，再到3。对指数分支的树，重复的工作很少，因为最后一层占了大头。",

    'f"When actions have different costs, expand the cheapest first':
        "当动作的代价不同时，就先扩展最便宜的：g最小的状态，g是目前找到的到它的最佳路径的代价。在图上，这就是艾兹格·迪杰斯特拉1959年的算法。<bookmark mark='a'/>这里它在一张地图上运行：起点在中间，目标在右边，挡在一堵墙后面；每走一步的代价就是这一步的长度。被扩展的区域像波前一样扩大，遇到墙就绕过去。<bookmark mark='b'/>它扩展了{n:,}个格子之后到达目标，找到的路径可以证明是最短的。<bookmark mark='c'/>但它往远离目标的方向，和朝着目标的方向，搜得一样远。它知道自己走了多远，却不知道自己要去哪里。",

    # ------------------------------------------------------------------ A*
    'Chapter three. A star.':
        '第3章。A星搜索。',

    'In 1968 Peter Hart, Nils Nilsson and Bertram Raphael':
        "1968年，斯坦福研究所的彼得·哈特、尼尔斯·尼尔森和伯特伦·拉斐尔，需要让Shakey，第一台能规划自己行动的移动机器人，快速找到路径。<bookmark mark='a'/>他们的算法叫A星，按f等于g加h来给边界排序。<bookmark mark='b'/>g是到目前为止的代价，和迪杰斯特拉算法里一样。<bookmark mark='c'/>h是对剩余代价的一个猜测：启发式。<bookmark mark='d'/>在地图上，就是到目标的直线距离。",

    'f"Here are the two searches on the same map.':
        "这是两种搜索在同一张地图上。<bookmark mark='a'/>迪杰斯特拉向四面八方扩散；A星的边界朝目标倾斜，绕过墙，然后停下。<bookmark mark='b'/>两者得到相同的最优代价{C:.1f}。迪杰斯特拉扩展了{nd:,}个格子；A星，{na:,}个。<bookmark mark='c'/>它们的形状不是偶然的。把最优代价记作C星。迪杰斯特拉只扩展g不大于C星的格子，而没有路径比直线更短，所以这些格子落在半径为C星的圆里。A星只扩展g加h不大于C星的格子，包括可能出现的边界平局，所以它们落在一个以起点和目标为焦点的椭圆里。<bookmark mark='d'/>我们检查了每一个被扩展的格子：{inside[0]:.0f}%在圆内，{inside[1]:.0f}%在椭圆内。",

    "Why is A star's path the shortest?":
        "为什么A星的路径是最短的？<bookmark mark='a'/>如果h从不高估，就说它是可采纳的：h(n)至多是h星(n)，也就是到目标的真实代价，而且在目标处h是0。<bookmark mark='b'/>用树搜索，或者在找到更便宜的路径时重新打开状态的图搜索，A星就是最优的。假设边界上有一个更差的目标G2。最优路径上一定也有某个状态n在边界上。<bookmark mark='c'/>它的f是g加h，<bookmark mark='d'/>由于h可采纳，这至多是g加h星，<bookmark mark='e'/>而由于n在最优路径上，g加h星恰好就是C星。<bookmark mark='f'/>G2的代价比C星大，而它的h是0。所以n总是先离开边界，最优目标也先于G2离开边界。",

    'To avoid reopening states on graphs, A star wants a little more.':
        "要在图上避免重新打开状态，A星需要的条件更多一点。<bookmark mark='a'/>如果对每一步从n到n撇，h(n)至多是这一步的代价加上h(n撇)，就说h是一致的：这是一个三角不等式，直线距离满足它。<bookmark mark='b'/>于是沿着一条路径，f从不下降。f(n撇)等于g(n)，加上这一步，再加上h(n撇)；<bookmark mark='c'/>由一致性，这至少是g(n)加h(n)：<bookmark mark='d'/>也就是f(n)。<bookmark mark='e'/>所以状态按f的顺序离开边界，A星第一次扩展一个状态时，就已经有了到它的最佳路径。",

    'f"One map proves little, so we ran {n_maps} random ones.':
        "一张地图说明不了什么，所以我们跑了{n_maps}张随机地图。<bookmark mark='a'/>扩展次数的中位数，迪杰斯特拉为{med[0]:,.0f}，A星为{med[1]:,.0f}。每张地图配对计算工作量比值，其中位数为{ratio:.0f}%，最优代价相同。<bookmark mark='b'/>把h乘以2，加权A星扩展的中位数是{med[2]:,.0f}个，路径平均长{100 * excess[2]:.0f}%，但绝不会超过最优的两倍。<bookmark mark='c'/>贪心搜索完全不管g：{med[3]:,.0f}个格子，但路径长{100 * excess[3]:.0f}%，而且毫无保证。速度与最优性的权衡。",

    # ------------------------------------------------------------------ Heuristics
    'Chapter four. Where heuristics come from.':
        '第4章。启发式从哪里来。',

    'f"A star is only as good as its heuristic.':
        "A星的好坏取决于它的启发式。好的启发式从哪里来？<bookmark mark='a'/>写下八数码的规则：如果方格A挨着方格B，并且B是空的，方块就可以从A移到B。<bookmark mark='b'/>现在作个弊。去掉“B是空的”，每块方块都能穿过别的方块走回家：这个更容易的谜题的代价，是各方块行距与列距之和，也就是曼哈顿距离。这里是{h2}。<bookmark mark='c'/>两个条件都去掉，每块放错的方块一步就跳回家：代价就是放错的方块数，这里是{h1}。<bookmark mark='d'/>真正的答案，从我们广度优先的地图上查：{len(d['path']) - 1}步。<bookmark mark='e'/>这是通用的配方，由朱迪亚·珀尔在八十年代初明确提出：把问题放松到容易为止，然后精确求解。去掉规则只会让解变短：白送的可采纳性。",

    'f"How much does the better guess buy?':
        "更好的猜测能换来多少？在八数码上运行A星，每种解长最多取100个局面。<bookmark mark='a'/>不用启发式时，在解长{dd}处，它平均扩展{last['astar_h0']:,.0f}个状态。<bookmark mark='b'/>数放错的方块：{last['astar_h1']:,.0f}个。<bookmark mark='c'/>曼哈顿距离：{last['astar_h2']:,.0f}个。<bookmark mark='d'/>有效分支因子，也就是同样大小、同样深度的均匀树的分支数，从{ebf['astar_h0']:.2f}降到{ebf['astar_h1']:.2f}，再降到{ebf['astar_h2']:.2f}：每向1靠近一步，都是指数级的节省。<bookmark mark='e'/>曼哈顿距离从不小于放错的方块数。对一致的启发式，占优关系不会增加A星必须扩展的、f小于最优代价的状态。在边界上，相同的f值及其平局处理方式会改变总扩展数。",

    'f"The fifteen-puzzle has about ten trillion states':
        "十五数码大约有10万亿个状态，多到画不出地图。1985年，理查德·科尔夫用IDA星最优地解出了随机局面：保持A星的排序，但以一系列深度优先搜索来运行，f的上限逐次提高，几乎不需要内存。<bookmark mark='a'/>这是它在打乱的局面上的表现。数放错的方块时，它很快撞上我们设的{d['caps']['misplaced']:,}个局面的上限而放弃，{len(rows)}次里有{n_cap['misplaced']}次。<bookmark mark='b'/>曼哈顿距离好得多。<bookmark mark='c'/>还能更好：精确地解一个更小的放松谜题，把答案记下来。只跟踪五块方块，忽略其余的，广度优先搜索就能给出从每一种摆放把它们送回家的精确代价。这就是模式数据库，约瑟夫·卡尔伯森和乔纳森·谢弗的想法。每张表只计算自己那五块方块的移动，其他方块的移动免费。三组方块互不重叠，每个真实动作只由一张表收费，所以三份代价可以相加。<bookmark mark='d'/>它生成的局面比曼哈顿距离少大约{ratio:,.0f}倍，因为它知道得更多：对一个随机局面，它平均猜{hm['pdb']:.0f}步，另外两个分别是{hm['manhattan']:.0f}和{hm['misplaced']:.0f}。",

    'The same idea scaled up.':
        "同样的想法被放大了。<bookmark mark='a'/>1997年，科尔夫用模式数据库找到了魔方的最优解。<bookmark mark='b'/>2019年，尔湾的一个团队改让神经网络来学习启发式，再把它用在加权A星里：它解开了每一个测试魔方，60.3%的时候找到的是最短解。<bookmark mark='c'/>对剩余代价的学习估计，就是强化学习所说的价值函数；由它引导的搜索，就是AlphaZero下棋的方式，见第26部分。",

    # ------------------------------------------------------------------ Local
    'Chapter five. Climbing and cooling.':
        '第5章。爬山与退火。',

    "Often the path doesn't matter":
        "很多时候路径并不重要，只有最终状态重要：一张时间表、一块芯片的布局、一条回路。这时只保留一个状态，一步步改进它。<bookmark mark='a'/>把状态想象成一片地形，高度表示好坏。爬山法总是走到最好的相邻状态。<bookmark mark='b'/>它很快，几乎不需要内存。<bookmark mark='c'/>但它会停在遇到的第一个山峰上，也就是局部极大值，而最高的山峰在别处。",

    'f"The classic test: eight queens on a chessboard':
        "经典的测试：在棋盘上放八个皇后，互不攻击。每列放一个皇后；一步就是把一个皇后在它那一列里移动；高度是互相攻击的皇后对数。<bookmark mark='a'/>两次最陡下降。左边，攻击数下降，然后停住：没有哪一步能让情况变好。<bookmark mark='b'/>右边，同样的规则找到了解。<bookmark mark='c'/>在{d['n_starts']:,}个随机起点上，它解出了{100 * p['success']:.0f}%，平均用{p['steps_ok']:.0f}步；其余的在{p['steps_fail']:.0f}步后卡住。<bookmark mark='d'/>允许在平台上横向移动，成功率就变成{100 * s['success']:.0f}%。或者每次卡住就重来：大约要试{1 / p['success']:.0f}次，总共大约{p['restart_steps']:.0f}步。",

    'Simulated annealing escapes local optima':
        "模拟退火靠偶尔往错的方向走，来逃出局部最优。<bookmark mark='a'/>随机提出一个改动。如果它降低代价，就接受；如果它把代价提高了ΔE，也以e的负ΔE除以T次方的概率接受，其中T是温度。<bookmark mark='b'/>为什么是这条规则？固定温度下，我们要求细致平衡：任意一对状态之间，两个方向的概率流量相等。<bookmark mark='c'/>上坡以这个概率被接受，下坡总是被接受，而提议是对称的。<bookmark mark='d'/>两边相除，<bookmark mark='e'/>玻尔兹曼分布就是平稳分布。经过足够混合后，各状态的访问频率服从这个分布。<bookmark mark='f'/>当T降向0时，这族平衡分布的概率质量集中到代价最小的状态。有限的降温过程未必始终保持平衡，也未必达到最优解。",

    'f"Here it is on a travelling-salesman problem':
        "这是它在一个旅行商问题上的表现：经过柏林52个地点的最短回路，一个最优解已知的标准测试。一步是把回路中的一段倒过来。<bookmark mark='a'/>一开始温度很高，被提出的改动有{a0:.0f}%被接受，回路乱成一团。<bookmark mark='b'/>随着降温，能通过的坏改动越来越少；交叉的边消失了，回路收拢成绕着城市各个聚集区的圈。<bookmark mark='c'/>到最后，只有{a_end:.1f}%被接受：退火变成了爬山法，只是从一个非常好的地方出发。{end}",

    "f'It ends at {best:,}: the proven optimum":
        '它最后停在{best:,}：正是已被证明的最优值{int(d[\'opt\']):,}。',

    "f'It ends at {best:,}, against the proven optimum":
        '它最后停在{best:,}，而已被证明的最优值是{int(d[\'opt\']):,}。',

    'f"Is the cooling worth it?':
        "降温值得吗？让三种方法的实际候选代价评估次数相同，初始化也计入。计算一次2-opt代价差计一次，给一个遗传算法子代打分也计一次；这不代表相同CPU时间。<bookmark mark='a'/>贪心回路总是去最近的未访问地点，即使从最好的起点出发，也长了{100 * (min(d['nn_lengths']) / opt - 1):.0f}%。对每个起点得到的回路都用2-opt改进后，最好结果是{min(d['nn2opt_lengths']):,}，可能来自另一个起点。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{hits}",

    "f'Annealing found the optimum itself in":
        '退火在{len(d[\'eq_anneal\'])}次运行中有{n_opt}次找到了最优解本身。',

    'Annealing never found the optimum itself.':
        '退火一次也没有找到最优解本身。',

    'f"On the same budget of {d[\'budget\']:,} candidate-cost evaluations, {order[0][0]} does best, averaging {order[0][1]:,.0f}; {order[1][0]} averages {order[1][1]:,.0f}, and {order[2][0]}, {order[2][1]:,.0f}."':
        "在同样{d['budget']:,}次候选代价评估的预算下，{order[0][0]}最好，平均{order[0][1]:,.0f}；{order[1][0]}平均{order[1][1]:,.0f}；{order[2][0]}平均{order[2][1]:,.0f}。",

    'f"A third idea keeps a whole population.':
        "第三种思路是保留一整个种群。<bookmark mark='a'/>约翰·霍兰德1975年提出的遗传算法，让更好的状态繁殖：一个孩子取两个父母的片段，再加一点随机变异。<bookmark mark='b'/>在我们的预算下，一个朴素版本最后比最优解高{ga_gap:.0f}%。交叉和变异可能破坏回路中好的片段。<bookmark mark='c'/>种群搜索迎来了第二春。2023年，DeepMind的FunSearch让一个语言模型来提出变异；2025年，AlphaEvolve用同样的方式演化程序，找到了一种只用48次乘法计算4乘4复数矩阵乘法的方法，比施特拉森1969年的方法少一次。",

    # ------------------------------------------------------------------ Games
    'Chapter six. Games and alpha-beta.':
        '第6章。博弈与α-β剪枝。',

    'f"Games were the field\'s favourite test':
        "博弈是这个领域最喜欢的测试：规则清楚，胜负清楚，还有一个会反击的对手。<bookmark mark='a'/>1928年，约翰·冯·诺依曼证明：在两人零和博弈中，假设对手下得完美，每一方都能保证一个值。<bookmark mark='b'/>所以往前看：轮到你走时取最大；轮到对手走时取最小。这就是极小化极大。<bookmark mark='c'/>1950年，克劳德·香农描述了一个这样构造的国际象棋程序，用一个公式给前瞻尽头的局面打分；他估计可能的对局大约有10的120次方种：远远多到无法搜到底。<bookmark mark='d'/>井字棋足够小。我们的极小化极大访问了{d['minimax']:,}个局面和{tot:,}盘完整的对局，发现双方都下得最好时，结果是{verdict}。",

    'f"Much of a game tree can be skipped.':
        "博弈树中不少部分可以跳过。这是一棵小树：你走，对手应，你再走，底部的局面都打了分。<bookmark mark='a'/>深度优先地搜索它，同时带着两个数：α，你已经有把握的最好分数；β，对手已经有把握的最好分数。<bookmark mark='b'/>一旦某个应对表明一步棋比你已有的更差，这步棋剩下的应对就都无关紧要，可以跳过。变灰的分支从来没被查看过：{n}个局面里的{len(pruned_all)}个，而顶部的答案仍然和极小化极大的完全一样。这就是α-β剪枝，约翰·麦卡锡在五十年代中期提出，历代α-β国际象棋引擎都广泛使用它。截断处的分数可能只是界，未必是精确值；我们用不等号标出来。根节点的答案仍然精确。",

    'f"How much can pruning save?':
        "剪枝能省多少？唐纳德·克努特和罗纳德·摩尔在1975年完整地分析了它。<bookmark mark='a'/>要证明一个局面恰好值v，需要两个界。<bookmark mark='b'/>至少值v：你的一步好棋，加上对手对它的每一个应对，每一层都如此：b的d除以2次方个叶子，向下取整。<bookmark mark='c'/>至多值v：你的每一步棋，各配一个驳斥。<bookmark mark='d'/>两个证明共享一条变化。所以在完美排序下，α-β评估的叶子数大约是整棵树的平方根的两倍：同样的工作量，可以搜两倍深。<bookmark mark='e'/>我们在完美排序的均匀树上做了检验：每个局面5种走法，深8层，{ex['all']:,}个叶子里评估了{ex['leaves']:,}个，正是公式给出的数；{len(u)}种情形{agree}一致。",

    'f"On a real game the savings are as large.':
        "在真实的棋上，节省同样巨大。四子棋，搜得越来越深。<bookmark mark='a'/>朴素的极小化极大每深一步大约增长7倍：深度{dd}时，有{mm / 1000000.0:.1f}百万个局面。<bookmark mark='b'/>走法随机排序的α-β：{ab:,.0f}个。<bookmark mark='c'/>先试看起来最好的那步：{abo:,.0f}个。<bookmark mark='d'/>再用一个知道真正最好那步的神谕，在深度{dpp}时：{per:,.0f}个，和极小化极大的{d['minimax'][dpp - 1]:,.0f}个的平方根同一个量级。这就是为什么走法排序成了国际象棋程序员的手艺。",

    # ------------------------------------------------------------------ Samuel
    'Chapter seven. Machines that learned to play.':
        '第7章。学会下棋的机器。',

    'In 1959 Arthur Samuel of IBM published a checkers program':
        "1959年，IBM的阿瑟·塞缪尔发表了一个跳棋程序，附带一个惊人的说法：可以给计算机编程，让它学会把跳棋下得比编写程序的人更好。<bookmark mark='a'/>它往前搜几步，用棋盘特征的加权和给局面打分：一个评分多项式。<bookmark mark='b'/>新颖之处在于：它通过下棋，自己调整权重。<bookmark mark='c'/>1962年，它在一盘有名的对局中赢了康涅狄格棋手罗伯特·尼利；尼利赢了复赛，而1966年，这个程序对世界冠军的八盘棋全部输掉。但重要的是这个想法，而“机器学习”这个说法，也是塞缪尔帮着推广开的。",

    "Samuel's delta idea is a seed of modern reinforcement learning.":
        "塞缪尔的δ思想，是现代强化学习的一颗种子。这里展示的是现代半梯度更新的对应形式；他的原始程序调整的是符号相关性与量化系数。<bookmark mark='a'/>记住评估函数给你上一个局面的静态分数。<bookmark mark='b'/>两步之后，从新局面往前搜索，倒推出一个分数：对同一盘棋更有根据的看法。<bookmark mark='c'/>两者之差，塞缪尔记作δ，说明旧分数错了多少。<bookmark mark='d'/>轻推权重，让它变小。<bookmark mark='e'/>两份副本对弈：Alpha学习，Beta保持权重不变，每当Alpha赢了，Beta就拿走它的权重。理查德·萨顿在1988年形式化时序差分学习时，就是在这个想法上继续前进的。",

    'f"We gave Samuel\'s method a game of our own':
        "我们给塞缪尔的方法找了一个我们自己的游戏：四子棋，五个程序员可能会挑的特征，搜索三步深。Alpha一开始所有权重都是0。<bookmark mark='a'/>这是它边下边变的权重；橙色的是我们在训练前手工设定的权重。<bookmark mark='b'/>在与Beta下的{G:,}盘棋里，权重各就各位。{signs}<bookmark mark='c'/>我们隔一段时间就冻结Alpha，让它和两个固定的对手下棋：未经训练的玩家，和我们手工设定的权重。",

    "f'The largest weight ends up on {top}":
        '最大的权重最后落在{top}上，五个特征中有{npos}个对它有利。',

    'f"After {d[\'games\']:,} games, in each of {len(runs)} runs:':
        "在{len(runs)}次运行中，每次下完{d['games']:,}盘之后：<bookmark mark='a'/>{v}<bookmark mark='b'/>{acc_v}这些曲线并不平滑：塞缪尔也看到过他的程序游移不定，有时还得手动把它重置。",

    "f'Graded against a perfect solver":
        '用完美求解器来评判，它的走法有{100 * min(acc):.0f}%到{100 * max(acc):.0f}%的时候能保住胜局或和局，未训练的是{100 * a0:.0f}%，手工权重是{100 * ap:.0f}%。',

    'Every run beats both opponents':
        '每次运行都击败了两个对手：在这个游戏上，塞缪尔的说法成立。它学会了下得比程序员写的权重更好。',

    'Every run beats the untrained player. Against our hand-set weights':
        '每次运行都击败了未训练的玩家。对我们手工设定的权重，各次运行大致打平，有的领先，有的落后：它从零开始，学到了和程序员的猜测差不多的水平。',

    'Every run beats the untrained player, but none beats':
        '每次运行都击败了未训练的玩家，但没有一次击败我们手工设定的权重：它学到了很多，但在这里，没有学到比程序员自己的猜测下得更好。',

    'Here the learner does not reliably beat':
        '在这里，学习者连未训练的玩家都不能稳定地击败；分数在一个个检查点之间摇摆，就像塞缪尔发现他自己的程序也会游移一样。',

    'Chess went the other way':
        "国际象棋走了另一条路：更多的搜索，更多手工打造的知识。<bookmark mark='a'/>1996年，加里·卡斯帕罗夫以4比2战胜了IBM的深蓝，团队把机器的规模翻了一倍。<bookmark mark='b'/>在1997年的复赛中，它运行480块专门设计的国际象棋芯片，平均每秒1.26亿个局面，评估函数有大约8000个特征，几乎全部由人手工调整。它以3.5比2.5获胜。<bookmark mark='c'/>搜索，加上人为设计的好局面的感觉：这正是香农1950年的配方，只是规模巨大。",

    'Checkers itself was finished off by search.':
        "跳棋本身最终被搜索终结了。<bookmark mark='a'/>乔纳森·谢弗的Chinook在1994年成为第一个赢得人类世界冠军头衔的程序。<bookmark mark='b'/>2007年，他的团队证明：大约有5乘10的20次方个局面的跳棋，在完美对弈下是和棋。<bookmark mark='c'/>抗拒这个配方的是围棋，没有人能写出好的评估函数。那需要一个学出来的评估函数：第26部分。",

    # ------------------------------------------------------------------ Logic
    'Chapter eight. Logic and resolution.':
        '第8章。逻辑与归结。',

    'The other great idea of the era was logic':
        "那个时代的另一个伟大想法是逻辑：把你知道的写下来，让机器推出由此得出的结论。<bookmark mark='a'/>三条事实。如果下雨，草地就湿。如果洒水器开着，草地就湿。正在下雨，或者洒水器开着。<bookmark mark='b'/>能推出草地是湿的吗？<bookmark mark='c'/>列出真和假的所有组合。<bookmark mark='d'/>在所有事实都成立的每一行里，“湿”也成立：这些事实蕴涵它。<bookmark mark='e'/>但n个符号就有2的n次方行。我们需要推导结论，而不是枚举所有世界。",

    'Real knowledge needs more. First-order logic':
        "真正的知识需要更多。一阶逻辑，来自1879年的戈特洛布·弗雷格，加入了对象、关系，以及“所有”和“存在”：对所有的x、y和z，如果x是y的父母，y是z的父母，那么x是z的祖父母。<bookmark mark='a'/>库尔特·哥德尔在1930年证明：每个有效的一阶句子都有证明，所以一台在证明中搜索的机器一定能找到它。<bookmark mark='b'/>但没有程序能在一般情况下判定有效性：如果答案是否，搜索可能永远不会结束。",

    "In 1965 Alan Robinson gave machines a resolution rule for automated deduction. <bookmark mark='a'/> Write every fact as a clause, an or of literals. If one clause contains x and another not x, resolve them: at least one of the rest must hold. <bookmark mark='b'/> To prove a goal, add its negation, here: the grass is not wet, <bookmark mark='c'/> and resolve until you derive the empty clause, a contradiction. <bookmark mark='d'/> Not wet and the rain rule give no rain; not wet and the sprinkler rule give no sprinkler; rain or sprinkler, with no sprinkler, gives rain; rain against no rain leaves nothing. <bookmark mark='e'/> Robinson proved the method sound and refutation-complete. First-order clauses also need factoring: unify same-sign literals within one clause. Without a resource cap, resolution and factoring can derive the empty clause whenever the clauses are inconsistent. Our bounded run can stop without an answer.":
        "1965年，艾伦·鲁滨逊给了机器一条用于自动演绎的归结规则。<bookmark mark='a'/>把每条事实写成一个子句，也就是若干文字的“或”。如果一个子句含有x，另一个含有非x，就把它们归结：剩下的部分至少有一个必须成立。<bookmark mark='b'/>要证明一个目标，就加入它的否定，这里是：草地不湿，<bookmark mark='c'/>然后不断归结，直到推出空子句，也就是一个矛盾。<bookmark mark='d'/>不湿和下雨那条规则，得到不下雨；不湿和洒水器那条规则，得到洒水器没开；下雨或洒水器，加上洒水器没开，得到下雨；下雨对上不下雨，什么都不剩。<bookmark mark='e'/>鲁滨逊证明这个方法是可靠的，而且是反驳完备的。一阶子句还需要因子化：合一同一子句内同号的文字。不加资源上限时，只要子句集不一致，归结与因子化就能推出空子句。我们有资源上限的运行，也可能没有得到答案就停止。",

    'With variables, resolution needs one more step.':
        "有了变量，归结还需要多一步。<bookmark mark='a'/>否定后的目标，只有在规则里的变量被匹配成安妮和艾达之后，才能和规则归结。找出最一般的这种代换，就是合一，鲁滨逊那篇论文的另一半。<bookmark mark='b'/>再走两步，就得到空子句。<bookmark mark='c'/>把子句限制成最多只有一个正文字，归结就变成了一种编程语言：Prolog，由阿兰·科尔默劳尔和菲利普·鲁塞尔于1972年在马赛创造，背后是罗伯特·科瓦尔斯基的理论。",

    '"Completeness is not efficiency. <bookmark mark=\'a\'/> Give the prover eight family facts and three rules, and ask whether Anne is an ancestor of Flora, four generations away. <bookmark mark=\'b\'/> " + sat_verdict + " <bookmark mark=\'c\'/> The set-of-support strategy, from Larry Wos and colleagues in 1965, resolves only pairs involving the negated goal or its descendants. " + sos_verdict + " <bookmark mark=\'d\'/> Provers live or die by such strategies. Resolution\'s descendants, like Vampire and E, still compete every year, and proof assistants call on them to fill in routine steps."':
        "完备不等于高效。<bookmark mark='a'/>给证明器八条家庭事实和三条规则，问安妮是不是弗洛拉的祖先，相隔四代。<bookmark mark='b'/>{sat_verdict}<bookmark mark='c'/>支持集策略，来自拉里·沃斯和同事1965年的工作，只归结涉及否定目标或其后代的子句对。{sos_verdict}<bookmark mark='d'/>定理证明器的成败，就取决于这样的策略。归结的后代，像Vampire和E，每年还在比赛，证明助手也会调用它们来补全常规步骤。",

    # ------------------------------------------------------------------ SAT
    'Chapter nine. Satisfiability.':
        '第9章。可满足性。',

    'Strip logic down to its core and you get one problem.':
        "把逻辑剥到只剩核心，就得到一个问题。<bookmark mark='a'/>给定一组子句，每个都是变量或其否定的“或”，能不能给每个变量赋真或假，让每个子句都成立？这就是可满足性，SAT。<bookmark mark='b'/>1971年，斯蒂芬·库克证明，列昂尼德·列文也独立地证明：任何解能被快速验证的问题，都能改写成SAT。这是第一个NP完全问题。<bookmark mark='c'/>然而，SAT求解器却成了AI最伟大的实用成功之一。",

    '"The classic method is DPLL':
        "经典的方法是DPLL，来自1960年的马丁·戴维斯和希拉里·普特南，1962年又和乔治·洛格曼、唐纳德·洛夫兰一起把它变得实用。<bookmark mark='a'/>传播：一个只剩一个文字未定的子句，会强迫那个文字成立。<bookmark mark='b'/>没有什么被强迫时，就分支：选一个变量，先试真，再传播。<bookmark mark='c'/>如果某个子句的每个文字都为假，就退回去，试另一个值。<bookmark mark='d'/>在我们的小公式上：{story}",

    '"In 1992 David Mitchell, Bart Selman and Hector Levesque':
        "1992年，大卫·米切尔、巴特·塞尔曼和赫克托·莱韦斯克问：随机公式是什么样子的？取n个变量，m个子句，每个子句有三个随机文字。<bookmark mark='a'/>每个变量对应的子句少时，几乎每个公式都可满足；多时，几乎没有一个可满足；在两者之间，概率像从悬崖上掉下去。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>随着n增大，这个台阶变成一次跳变，位置在比值4.27附近。物理学家用无序磁体理论里的一种方法，预言了4.267；数学家已经证明，阈值在3.52和4.49之间。一个逻辑问题里的相变，就像水结冰一样。",

    "f'The bigger the formulas, the sharper the step":
        '公式越大，台阶越陡：{n0}个变量时，概率从90%降到10%，跨越的比值区间是{w0:.2f}；{n1}个变量时，只有{w1:.2f}。',

    "f'Here the step is about as wide":
        '在这里，{n1}个变量的台阶和{n0}个变量的差不多宽。',

    '"The transition is also where the problems are hard. <bookmark mark=\'a\'/> Count DPLL\'s decisions: far below the threshold a solution is found almost at once, far above, a contradiction. <bookmark mark=\'b\'/> " + result':
        "相变的地方，也正是问题难的地方。<bookmark mark='a'/>数一数DPLL的决策次数：远低于阈值时，几乎马上就找到一个解；远高于阈值时，几乎马上就找到矛盾。<bookmark mark='b'/>{result}",

    'f"Modern solvers add one idea: learn from every mistake.':
        "现代求解器加了一个想法：从每一次错误中学习。<bookmark mark='a'/>这里一个求解器做了四个决策，每层一个，传播又推出了一连串赋值，每个箭头都从迫使它的那些文字指过来。<bookmark mark='b'/>这一连串以冲突告终。DPLL只会撤销最后一个决策。<bookmark mark='c'/>冲突驱动的子句学习会问：为什么？它把冲突往回追，找到每条路径都必经的第一个点：这里是x{uip}。<bookmark mark='d'/>这些原因变成一个新子句，它被原公式蕴涵，从此永远排除这个组合。<bookmark mark='e'/>然后求解器往回跳，越过无关的决策，回到第{bj}层。再加上聪明的分支和廉价的簿记，来自1996年的GRASP和2001年的Chaff，每个有竞争力的求解器都这样工作。",

    'f"Learning is not a small improvement.':
        "学习可不是小改进。问两个二进制加法电路会不会给出不同的答案，写成子句，使它们恰好在两个电路不一致时可满足。<bookmark mark='a'/>DPLL什么都不记，每多一位，决策次数就要乘以大约{growth:.0f}倍：{int(W[-1])}位加法器需要{dp[-1]:,.0f}次。<bookmark mark='b'/>我们的子句学习求解器需要{cd[-1]:,.0f}次冲突，{int(W[0])}位时是{cd[0]:,.0f}次；它还用{b64['conflicts']:,}次冲突，证明了两个{w64}位加法器在全部2的{2 * w64}次方个输入上都相等。",

    # ------------------------------------------------------------------ Plans
    'Chapter ten. Constraints and plans.':
        '第10章。约束与规划。',

    'Many problems are sets of constraints rather than paths.':
        "许多问题是一组约束，而不是路径。<bookmark mark='a'/>一个约束满足问题有一些变量，每个变量有一个取值的值域，还有一些排除某些组合的约束。<bookmark mark='b'/>数独就是一个：81个格子，每格取1到9，每一行、每一列、每一宫里各不相同。<bookmark mark='c'/>这种结构适合传播：大卫·沃尔茨在1975年用它给线条图里的线做标注，艾伦·麦克沃斯在1977年给出了通用算法。",

    'f"Arc consistency looks at one constraint at a time.':
        "弧相容一次只看一条约束。<bookmark mark='a'/>对每一对必须不同的格子，删掉第一个格子里那些第二个格子没给它留余地的值；某个格子的候选变少时，再复查它的邻居。<bookmark mark='b'/>每个给定的数字，都把自己的值从所在的行、列、宫里划掉，这些删除一路连锁下去。<bookmark mark='c'/>AC-3删掉了{len(log)}个值，多确定了{d['ac3_solved']}个格子，但解不出整道题：单靠传播在这里不够。<bookmark mark='d'/>和搜索结合起来，它就是决定性的。按阅读顺序的朴素回溯尝试了{vals[0]:,}次赋值；前向检查，{vals[1]:,}次；再加上先选剩余值最少的格子，{vals[2]:,}次；每次选择之后都维持完全的弧相容，{vals[3]:,}次。",

    'Planning is search where the states are descriptions.':
        "规划，是状态为描述的搜索。<bookmark mark='a'/>STRIPS由理查德·法伊克斯和尼尔斯·尼尔森在1971年为机器人Shakey提出，它把一个状态描述成一组事实，把一个动作描述成三张表。<bookmark mark='b'/>要把x叠到y上，你必须拿着x，并且y上面是空的；之后，x在y上，x上面是空的，手也空了，你不再拿着x，y上面也不再是空的。<bookmark mark='c'/>为什么要删除表？因为框架问题，由约翰·麦卡锡和帕特里克·海斯在1969年提出：在纯逻辑里，一个动作还必须说明它没改变的一切，而那几乎是一切。<bookmark mark='d'/>STRIPS干脆假设：动作没提到的东西，都保持原样。",

    '"Early planners solved goals one at a time.':
        "早期的规划器一次解决一个目标。杰拉尔德·萨斯曼找到了这样做会失败的最简单例子。<bookmark mark='a'/>C压在A上；B在桌上。目标：A在B上，并且B在C上。<bookmark mark='b'/>先把A放到B上：把C从A上拿开，放下，把A叠到B上。现在B得放到C上，<bookmark mark='c'/>而要移动B，就得再把A拿下来，第一个目标又被破坏了。{other}<bookmark mark='d'/>最短的计划由广度优先搜索找到，有{len(d['sussman_plan'])}步，并且把两个目标交错完成。",

    'Doing B on C first fails too':
        '先把B放到C上也会失败：那样不把B从C上拿开，就没法把A取出来。',

    'Doing B on C first happens to work here.':
        '先把B放到C上，在这里碰巧行得通。',

    'f"And the search space explodes.':
        "而且搜索空间会爆炸。<bookmark mark='a'/>{len(towers)}块积木，可以叠成{towers[-1]:,}种不同的摆法。<bookmark mark='b'/>在随机的{n_bfs}块积木问题上，盲目的广度优先搜索平均扩展{bfs_n:,.0f}个状态。<bookmark mark='c'/>解药还是第4章的想法：放松问题。忽略删除表，再廉价地近似估计剩余代价；寻找最短的放松计划，仍然是NP难的。可采纳的h max启发式，把搜索减到{hm_n:,.0f}个，仍能保证最优。<bookmark mark='d'/>受霍夫曼和内贝尔2001年的FF规划器启发，我们的FF式启发式从一个放松计划中数出不重复的动作。贪心搜索扩展{ff_n:,.0f}个状态，平均计划长度为{L_ff:.1f}步，而最优计划平均为{L_opt:.1f}步。这样的启发式、Graphplan，以及把规划当作可满足性问题，让通用规划器变得实用。",

    # ------------------------------------------------------------------ Knowledge
    'Chapter eleven. Knowledge is power.':
        '第11章。知识就是力量。',

    'Search and logic need something to reason about.':
        "搜索和逻辑需要有东西可推理。<bookmark mark='a'/>罗斯·奎利恩1968年的语义网络，把概念存成结点，把关系存成链接：金丝雀是一种鸟，鸟是一种动物。<bookmark mark='b'/>属性只存一次，然后被继承：金丝雀会呼吸吗？沿着is-a链接一路上到动物。<bookmark mark='c'/>例外放在更低的地方：企鹅是一种不会飞的鸟。<bookmark mark='d'/>马文·明斯基1974年的框架，把一个概念的槽和默认值打包在一起。这些想法以对象和类的形式，活在编程语言里。",

    'In the seventies a new kind of program captured the field':
        "七十年代，一种新程序占领了这个领域：专家系统，它的知识是一组如果—那么规则，在人类专家的帮助下写成。<bookmark mark='a'/>给它一些关于某种动物的事实。<bookmark mark='b'/>前向链接触发每一条条件成立的规则，把结论加进来，然后重复：有毛，就是哺乳动物；有尖牙和爪子的哺乳动物，是食肉动物；有暗斑的黄褐色食肉动物，是猎豹。<bookmark mark='c'/>第一个伟大的专家系统是DENDRAL，1965年由爱德华·费根鲍姆、布鲁斯·布坎南和乔舒亚·莱德伯格在斯坦福开始研制，它根据质谱推断分子结构。费根鲍姆的教训是：一个程序的力量，更多地来自它知道什么，而不是它推理得多聪明。",

    'f"Medicine was the showcase.':
        "医学是展示橱窗。MYCIN由爱德华·肖特利夫在七十年代中期于斯坦福研制，它用几百条像这样的规则，为血液感染和脑膜炎推荐抗生素。<bookmark mark='a'/>每条规则带一个确定性因子；几条规则意见一致时，新的证据填补剩余差距的一部分。<bookmark mark='b'/>0.6和0.5合起来是{comb[1]:.2f}；再加一条0.4的规则，就到了{comb[2]:.2f}。<bookmark mark='c'/>在1979年发表的一次盲测中，8位专家为10例脑膜炎的抗生素选择评分。MYCIN获得了65%的可接受评价比例，和它比较的斯坦福专科医生都没超过这个比例。它从未被用于病人。<bookmark mark='d'/>商业上的突破是R1，后来叫XCON，由约翰·麦克德莫特在1980年为数字设备公司编写，用来配置计算机订单。到八十年代中期，专家系统已经成了一个产业。",

    'The weak point was getting the knowledge in.':
        "弱点在于怎样把知识装进去。<bookmark mark='a'/>专家讲，知识工程师写规则；规则失败了就打补丁，每个领域都要好几个月，而规则越来越多，它们之间会以没人预料到的方式相互作用：这就是知识获取瓶颈。<bookmark mark='b'/>而且这些系统很脆：遇到一个没有规则覆盖的情况，人类专家会做出合理的事；规则库要么什么都不做，要么做出荒唐的事。<bookmark mark='c'/>道格拉斯·莱纳特得出了最大胆的结论：把常识本身写下来。他的Cyc项目始于1984年，已经手工录入了几百万条断言，至今仍在运行。",

    'Knowledge as a web of entities and relations':
        "把知识看作实体和关系之网，这个想法并没有死；它被放大了。<bookmark mark='a'/>2012年，谷歌推出了知识图谱，“是事物，不是字符串”：发布时就有五亿多个对象和35亿条事实，是从维基百科之类的来源收集来的，而不是一条条输入的。<bookmark mark='b'/>如今，知识图谱回答搜索引擎里的事实性问题。变的不是表示方法，而是知识从哪里来。",

    # ------------------------------------------------------------------ ELIZA
    'Chapter twelve. ELIZA.':
        '第12章。伊丽莎。',

    'In 1966 Joseph Weizenbaum at MIT published a program that held conversations':
        "1966年，麻省理工学院的约瑟夫·魏岑鲍姆发表了一个能对话的程序：ELIZA，名字来自《卖花女》里的卖花姑娘。它最有名的脚本DOCTOR，扮演一位心理治疗师，把你的陈述翻成问题。<bookmark mark='a'/>输入：我妈妈照顾我。<bookmark mark='b'/>ELIZA交换代词，<bookmark mark='c'/>再找出等级最高的关键词，这里是“我的”，以及一个模式：任意内容、“你的”、任意内容、一个家庭成员的词、任意内容。<bookmark mark='d'/>它取这个模式的下一条重组规则，把匹配到的片段拼进去。<bookmark mark='e'/>你家里还有谁照顾你。没有语法，没有意义：只有模式匹配和几百行脚本。",

    'f"Weizenbaum\'s paper printed a conversation with DOCTOR.':
        "魏岑鲍姆的论文印出了一段和DOCTOR的对话。我们按照论文的描述，用我们自己的一份短脚本，写了一个小ELIZA，再把用户那一边的话一句句输给它。<bookmark mark='a'/>它的{len(convo)}句回答里，有{n_same}句和1966年的一字不差。<bookmark mark='b'/>{why_}注意这个技巧：什么都匹配不上时，ELIZA会把你早先说过的话搬出来。读起来像是在留意你，甚至像有记忆。",

    'The one difference is in the last line':
        '唯一的不同在最后一句，那里没有关键词匹配，ELIZA退回去用它的记忆：两者都把男朋友搬了出来，只是措辞不同。',

    'f"{len(diff)} replies differ':
        '有{len(diff)}句回答不同，因为我们的短脚本里没有魏岑鲍姆那样的规则。',

    "Step outside the therapist's frame and the trick shows.":
        "一走出治疗师的框架，把戏就露馅了。<bookmark mark='a'/>问它一个事实，它会问你为什么问。让它给出一个证明，它把你的句子还给你，只是把代词换了过来。提到电脑，一条专门为此写的规则就会触发。什么都没有被理解；幻觉活在读者心里。",

    'What disturbed Weizenbaum was how people responded.':
        "让魏岑鲍姆不安的，是人们的反应。<bookmark mark='a'/>在他1976年的书《计算机的力量与人类的理性》里，他回忆说，他的秘书看着他写出这个程序，却请他离开房间，好让她和它私下谈谈；他写道，自己没想到，与这样一个简单程序的短暂接触，竟能在正常人身上引出如此强烈的错觉。<bookmark mark='b'/>把理解读进流畅的输出里，后来被称为伊丽莎效应。<bookmark mark='c'/>他的原始代码2021年在麻省理工学院被找到，2024年重新运行。2025年的图灵测试，用的是另一份以Python实现的DOCTOR脚本；在23%的对话里，人们把它当成了人。流畅就意味着理解吗？每个聊天机器人都会重新提出这个问题。",

    # ------------------------------------------------------------------ Winters
    'Chapter thirteen. The winters.':
        '第13章。寒冬。',

    'The founders had promised a great deal, soon.':
        "创始人们许诺了很多，而且说很快就能实现。到六十年代末，账单到期了。<bookmark mark='a'/>1966年，一个顾问委员会告诉美国政府，机器翻译比人工翻译更慢、更不准、更贵，对它的资助随之枯竭。<bookmark mark='b'/>1969年，明斯基和佩珀特的书《感知机》讲清了单层神经网络的局限，这条研究路线沉寂了十年。<bookmark mark='c'/>1973年，数学家詹姆斯·莱特希尔向英国科学研究委员会报告说，离开玩具问题，AI都败给了组合爆炸：也就是我们一直在数的那些搜索空间。<bookmark mark='d'/>他在电视上为这份报告辩护，对手是唐纳德·米奇、约翰·麦卡锡和理查德·格雷戈里。<bookmark mark='e'/>英国的资助缩减到只剩几个中心；在美国，DARPA转向军事目标。第一次寒冬一直持续到1980年前后。",

    'Expert systems brought the money back.':
        "专家系统把钱带了回来。<bookmark mark='a'/>公司们纷纷自建专家系统；1982年，日本启动了一个围绕逻辑编程的十年期第五代计算机项目，美国和英国也作出了回应。<bookmark mark='b'/>一个小产业专门出售Lisp机，一种为运行AI软件而造的工作站。<bookmark mark='c'/>1984年，罗杰·尚克和马文·明斯基警告美国人工智能协会，热情已经跑到了成果前面，并给接下来的事起了名字：AI寒冬。<bookmark mark='d'/>1987年，Lisp机的市场崩溃了，被普通工作站挤垮；专家系统原来维护起来很贵，又很脆；第五代项目在1992年结束，没有达到目标。<bookmark mark='e'/>第二次寒冬来了。有好些年，研究者们都避免说“人工智能”这个词。",

    'Beneath the funding story lay a scientific surprise.':
        "资助起落的背后，是一个科学上的意外。<bookmark mark='a'/>符号程序最擅长的，是人觉得难的事：逻辑、代数、国际象棋。<bookmark mark='b'/>它们最不擅长的，是任何孩子都毫不费力就能做的事：看、走路、抓握、听懂话、常识。<bookmark mark='c'/>汉斯·莫拉维克在1988年指出，让计算机在智力测验或跳棋上达到成人水平相对容易，而让它们拥有一岁婴儿的感知和行动能力却很难，甚至不可能。他认为，进化在感知和运动上花了几亿年；抽象推理只是薄薄的、新近的一层。这就是莫拉维克悖论。",

    'f"There is a measurable reason hand-written knowledge kept running out':
        "手写的知识总是不够用，有一个可以测量的原因，我们在第1部分的三十部小说里就能看到。<bookmark mark='a'/>把其中的词从最常见排到最少见。<bookmark mark='b'/>最常见的{need['0.5']}个词就占了全部文本的一半。覆盖90%需要{need['0.9']:,}个词；99%，{need['0.99']:,}个；99.9%，{need['0.999']:,}个。<bookmark mark='c'/>{d['n_types']:,}个不同的词里，有{d['once']:,}个只出现过一次。<bookmark mark='d'/>新的文本还会带来新词：在本系列的测试段落里，有{fresh:.1f}%的词在{d['n_tokens'] / 1000000.0:.1f}百万词的小说里从未出现过。语言、视觉和物理世界都是这个形状：少数常见情况，加上一条没有尽头的罕见长尾。给每种情况写一条规则，永远写不完。<bookmark mark='e'/>能写完的，是一种从数据中学习、能推广到没人写下的情况的方法。这就是本课程接下来要去的地方。",

    # ------------------------------------------------------------------ Survives
    'Chapter fourteen. What survives.':
        '第14章。留下来的东西。',

    'The symbolic era ended, but its machinery did not.':
        "符号时代结束了，但它的机器没有。<bookmark mark='a'/>深蓝是搜索加上人写的评估函数。<bookmark mark='b'/>二十年后，AlphaZero保留了搜索，用蒙特卡洛树搜索代替α-β，并通过自我对弈学出了评估函数；它每秒检查的局面，比它击败的那个国际象棋引擎少大约一千倍。<bookmark mark='c'/>由评估引导的搜索，是两者共同的骨架。第26部分会造一个。",

    'f"Logic found its biggest job in checking machines.':
        "逻辑最大的用武之地，是检查机器。<bookmark mark='a'/>1994年，奔腾处理器的除法电路里有一个缺陷，表里少了几项，让英特尔计提了4.75亿美元的费用。芯片厂商转向形式化验证，SAT求解器成了它的引擎之一。<bookmark mark='b'/>我们自己的小求解器，用{b['conflicts']:,}次冲突证明了两个{w}位加法器在全部2的{2 * w}次方个输入上都相等。<bookmark mark='c'/>在第{bug['bit']}位接错一根线，它就找到一个让两者不一致的输入：{bug['a']:,}加{bug['b']:,}，在{wb}位下应该得{bug['right']:,}；有缺陷的电路给出{bug['wrong']:,}。<bookmark mark='d'/>给SAT加上算术和数据结构的理论，就得到SMT求解器，比如微软的Z3；亚马逊在2022年报告说，它每天运行超过十亿次SMT查询，检查谁能访问什么。",

    'f"There are limits. ':
        "也有极限。<bookmark mark='a'/>让同一个求解器判断：a乘b和b乘a的乘积低位是否相等。<bookmark mark='b'/>在这些运行中，输入每多一位，冲突次数就增长大约{growth:.0f}倍：{int(W[-1])}位时是{M[-1]:,.0f}次。这是搜索上的困难，并不能证明不存在短证明。乘法器是SAT求解器出了名的难题；专门的代数方法能够提供帮助。",

    "Logic's other modern home is mathematics.":
        "逻辑在今天的另一个家是数学。<bookmark mark='a'/>在像Lean这样的证明助手里，一个小而可信的程序检查每一步，所以能编译通过的证明就是对的。<bookmark mark='b'/>DeepMind在2024年的AlphaGeometry，把一个提出辅助构造的语言模型和一个符号推理引擎配在一起。<bookmark mark='c'/>AlphaProof在Lean证明上运行AlphaZero式的搜索；它和AlphaGeometry 2一起，在2024年国际数学奥林匹克竞赛上解出了六道题中的四道，达到银牌水平。<bookmark mark='d'/>一年后，一个Gemini模型用自然语言写作，拿到了金牌分数，由奥赛的协调员评分。<bookmark mark='e'/>无论哪条路：网络生成，逻辑或评分者检查。",

    'Planning is back, inside language-model agents.':
        "规划回来了，就在语言模型智能体里。<bookmark mark='a'/>在用积木世界搭建的PlanBench上，2024年测试的最好的普通语言模型解出了63%的题，OpenAI的推理模型o1-preview解出了98%。<bookmark mark='b'/>把积木和动作的名字换成无意义的词，逻辑不变，o1-preview就跌到了53%；而经典规划器不管名字是什么，都能解出每一道题。<bookmark mark='c'/>一个实用的答案是把两者结合起来：先给定领域模型，语言模型用规划语言PDDL写出问题，经典规划器找出在那个形式模型内有效的计划。保证针对的是模型；模型的假设和语言模型的翻译，仍然需要检查。",

    'So the old argument, symbols or learning, ended in a merger.':
        "于是，符号还是学习的老争论，以合并告终。<bookmark mark='a'/>网络带来符号时代缺少的东西：感知、直觉、从数据中得出的猜测。<bookmark mark='b'/>符号带来网络无法保证的东西：穷尽的搜索、精确的逻辑、保证。<bookmark mark='c'/>今天最强的系统，让网络来提议，让一个符号过程来检查：AlphaZero、AlphaProof、FunSearch和AlphaEvolve，还有调用工具的智能体。这就是神经符号AI，<bookmark mark='d'/>我们会在强化学习、推理模型和智能体里再见到它。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        '我们来总结一下。图灵定义了机器能计算什么，以及不能计算什么。搜索靠尝试来找到解；带着可采纳启发式的A星，能找到代价最小的解，也能大幅减少搜索，而有效的启发式经常来自放松问题。退火用受控的随机性逃出局部最优。在走法排序很好的情况下，α-β剪枝能用同样的工作量，搜到大约两倍的深度。逻辑归结为归结法和可满足性，难题住在它的相变处，而子句学习让求解器变快。手写的知识撞上了长尾，这就是这个领域转向学习的原因。',

    'All of this comes back.':
        '这些都还会再出现。学来的权重取代手写的规则，靠的是感知机和反向传播，见第9部分。由学来的评估函数引导的搜索就是AlphaZero，见第26部分。在思维链上搜索，用可检查的答案给奖励，造就了第28部分的推理模型。规划和工具会在第29部分的智能体里回来。而验证、证明，以及谁来检查检查者，是第31部分为整个系列收尾的问题。',

    'Here are six problems to try':
        '这里有六道题，从一致的启发式到可满足性的阈值。在这里暂停，把它们做一遍；完整的解答在本部分的笔记里。',

    'Next time: meaning as geometry.':
        '下一次：意义即几何。对一个符号来说，“猫”离“狗”和离“车”一样远。第3部分把词变成向量，距离近就意味着相似，并且搭建本课程每个模型都要用到的线性代数：内积、特征值、奇异值分解。',

    "Russell and Norvig's textbook is the place to go deeper":
        '想深入学习，最好去读拉塞尔和诺维格的教科书：本部分的一切都在里面。至于历史，可以读尼尔斯·尼尔森的《人工智能的探索》。感谢观看，第3部分见。',

    # Corrected censored outcomes and their uncensored result branch.
    'Some runs reached the decision cap without an answer. The solid and dashed lines bound the SAT fraction; unknown is not unsatisfiable, and a censored crossing or width is unresolved.':
        '有些运行达到决策次数上限，仍未得出答案。实线与虚线给出可满足比例的下界和上界；未知不等于不可满足，受到截断影响的交点或宽度仍未确定。',

    'The sampled ratios do not bracket both window endpoints, so a width is unresolved.':
        '采样的比值范围没有覆盖窗口的两个端点，所以宽度仍未确定。',

    'Some runs are truncated at the decision cap. These medians describe observed work, including truncated runs; they do not locate the peak of completion work.':
        '有些运行在决策次数上限处被截断。这些中位数描述的是已经观察到的工作量，包括被截断的运行；它们不能定位完成求解所需工作量的峰值。',

    "f'For {n1} variables, the median peaks at a ratio of {pk:.1f}, at {med.max():,.0f} decisions, against {lo_side:,.0f} at the left edge and {hi_side:,.0f} at the right. Easy, hard, easy.'":
        '对{n1}个变量，中位数在比值{pk:.1f}处达到峰值，为{med.max():,.0f}次决策，而左边缘是{lo_side:,.0f}次，右边缘是{hi_side:,.0f}次。易、难、易。',


    # Actual stopping outcomes for capped and uncapped resolution runs.




    # Explicit outcome branches: no proof claim for capped runs.
    'f"The level-by-level search found a refutation after {sat[\'made\']:,} recorded clauses; the proof uses {sat[\'proof_len\']} clauses."':
        "逐层归结搜索记录了{sat['made']:,}个子句后找到反驳证明；证明用到{sat['proof_len']}个子句。",

    'f"The level-by-level search reached its cap of {sat[\'clause_cap\']:,} recorded clauses without finding a refutation. That leaves the goal unresolved by this run."':
        "逐层归结搜索达到记录{sat['clause_cap']:,}个子句的上限，仍未找到反驳证明。这次运行没有确定目标。",

    'f"The level-by-level search stopped with no new clauses after {sat[\'made\']:,} recorded clauses, without finding a refutation."':
        "逐层归结搜索记录了{sat['made']:,}个子句后，因没有新子句而停止，未找到反驳证明。",

    'f"The set-of-support search found a refutation after {sos[\'made\']:,} recorded clauses; the proof uses {sos[\'proof_len\']} clauses."':
        "支持集搜索记录了{sos['made']:,}个子句后找到反驳证明；证明用到{sos['proof_len']}个子句。",

    'f"The set-of-support search reached its cap of {sos[\'clause_cap\']:,} recorded clauses without finding a refutation. That leaves the goal unresolved by this run."':
        "支持集搜索达到记录{sos['clause_cap']:,}个子句的上限，仍未找到反驳证明。这次运行没有确定目标。",

    'f"The set-of-support search stopped with no new clauses after {sos[\'made\']:,} recorded clauses, without finding a refutation."':
        "支持集搜索记录了{sos['made']:,}个子句后，因没有新子句而停止，未找到反驳证明。",

}

PHRASES = {
    # the DPLL run on the illustrative formula, as describe() tells it
    'Try a true, which forces c, d and e, and a clause fails: back up. Try a false, which forces b. Try c true. '
    'Try d true, which forces e, and a clause fails: back up. Try d false, and every clause holds.':
        '试a为真，它迫使c、d和e成立，然后一个子句失败：退回。试a为假，它迫使b成立。试c为真。试d为真，它迫使e成立，'
        '又一个子句失败：退回。试d为假，每个子句都成立了。',
    # spliced into the tic-tac-toe verdict
    'a draw': '和棋',
    'a win for the first player': '先手胜',
    'a win for the second player': '后手胜',
    'all': '全部',
    'not all': '并非全部',
    # the equal-budget comparison
    'annealing': '退火',
    'restarted hill climbing': '带重启的爬山法',
    'the genetic algorithm': '遗传算法',
    # Samuel's features
    'lone stones in open lines': '开放线上的单子',
    'pairs in open lines': '开放线上的两子',
    'threes in open lines': '开放线上的三子',
    'stones in the centre': '中间列的棋子',
    "threats the opponent can't block at once": '对手无法立刻堵住的威胁',
}
