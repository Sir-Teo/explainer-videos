"""Chinese narration for cs20: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第20部分：作为资源的随机性"

CHAPTERS = {
    "Hook": "几千字节里的高频词",
    "LasVegas": "1. 拉斯维加斯与蒙特卡洛",
    "Freivalds": "2. 用硬币检验乘积",
    "Identity": "3. 这个多项式是零吗？",
    "Karger": "4. 用收缩求最小割",
    "Primes": "5. 几毫秒内的素数",
    "Walks": "6. 求解 SAT 的随机游走",
    "Bins": "7. 球与箱，以及两个选择的力量",
    "Bloom": "8. 布隆过滤器",
    "Stream": "9. 数据流：一遍扫描，很少的内存",
    "JobSketch": "10. 几千字节里的作业：账本第9行",
    "Distinct": "11. 统计不同元素：HyperLogLog",
    "Ams": "12. 为二阶矩画草图",
    "Lsh": "13. 近似重复：MinHash 与 LSH",
    "ProbMethod": "14. 概率方法",
    "Derand": "15. 去掉硬币，以及硬币从哪里来",
    "Frontier": "16. 前沿：随机性有用吗？",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Here are the most common words in the thirty novels, counted twice.":
        "这是三十部小说中最常见的词，数了两遍。<bookmark mark='a'/>左边是第17部分的程序，它把每个不同的词都存进一张哈希表。右边是这一部分的"
        "程序。两边的计数一致，二十个词、二十个数都一样。<bookmark mark='b'/>但第一个程序需要将近两兆字节，第二个只要十八点五千字节，少了一百倍。"
        "<bookmark mark='c'/>第二个程序根本不存储它所统计的词，只留几十个候选。它靠抛硬币做到这一点，而且只是以很高的概率完全正确。到这一部分"
        "结束时，我们会知道这个概率有多高。",
    "That is the theme of this part: a coin flip can stand in for cleverness.":
        "这就是这一部分的主题：抛一枚硬币可以代替聪明。<bookmark mark='a'/>有了硬币，我们可以在 n 的平方时间内检验一个声称的矩阵乘积，而不必"
        "重新计算。<bookmark mark='b'/>我们可以通过随机收缩边找到网络最薄弱的环节。<bookmark mark='c'/>我们可以在几毫秒内检验一个三百位的数"
        "是否为素数，第30部分的密码学就依赖于此。<bookmark mark='d'/>我们还可以用一小部分内存统计一个数据流。每一次，我们付出的代价是一个很小的、"
        "可以证明的概率：答案错误，或者等待很久。",
    "Part 20 of Computer Science, Built: Randomness as a Resource.":
        "计算机科学，从零搭建，第20部分：作为资源的随机性。<bookmark mark='a'/>这一部分包括：两类随机算法，以及重复如何缩小它们的错误；用随机点"
        "检验乘积和多项式；割、素数、随机游走，以及两个选择的力量；布隆过滤器和数据流草图，最后是十八千字节里的作业；概率方法；以及硬币能否去掉、"
        "它们从哪里来。",
    # ------------------------------------------------------------------ LasVegas
    "Chapter one. Las Vegas and Monte Carlo.": "第1章。拉斯维加斯与蒙特卡洛。",
    "An algorithm that flips coins can gamble in two ways.":
        "一个抛硬币的算法可以用两种方式下注。<bookmark mark='a'/>拉斯维加斯算法总是正确，只有运行时间取决于硬币。第16部分的随机快速排序就是"
        "一例。<bookmark mark='b'/>蒙特卡洛算法运行固定的时间，它的答案可能出错，出错的概率我们可以给出上界，再让它要多小就有多小。这一部分的"
        "大多数算法是蒙特卡洛算法。<bookmark mark='c'/>两种情形中，随机性都属于算法本身。我们对输入不作任何假设：保证对每一个输入都成立，只对"
        "算法自己的硬币取平均。",
    'f"Here is a Las Vegas algorithm at work':
        "这是一个正在工作的拉斯维加斯算法：随机选主元的快速排序，作用于 {words(d['n'])} 个键，运行 {d['runs']} 次。每根柱子统计做了那么多次"
        "比较的运行次数。<bookmark mark='a'/>平均值是 {words(round(d['mean']))}，第16部分的精确公式预测的是 {words(round(ex))}。<bookmark "
        "mark='b'/>各次运行大约向两边分散 {words(round(d['sd']))}，最慢的一次做了 {words(d['max'])} 次。<bookmark mark='c'/>最坏情形大约是"
        "两百万次比较，原则上可能发生，但它需要一长串糟糕的主元，概率小得根本观察不到。<bookmark mark='d'/>而每一次运行都正确地排好了序。只有"
        "时间是一场赌博。",
    "A Monte Carlo algorithm that errs half the time sounds useless.":
        "一个有一半时间出错的蒙特卡洛算法听起来毫无用处。其实不然，因为我们可以再运行一次。<bookmark mark='a'/>这一部分的许多算法只有单侧错误："
        "它们说“否”时一定正确，说“是”时出错的概率至多为二分之一。用新的硬币运行 k 次，只有每次都说“是”才相信“是”。k 次必须全部被骗，"
        "而它们相互独立，所以错误降到二分之一的 k 次方。<bookmark mark='b'/>十次给出千分之一。四十次大约是万亿分之一，比硬件本身在计算过程中"
        "出故障的可能还小。<bookmark mark='c'/>如果两侧都会出错，比如以大于二分之一的概率 p 正确，就取 k 次运行的多数。人工智能系列中的"
        "霍夫丁不等式说，多数结果出错的概率随 k 指数地变小。",
    # ------------------------------------------------------------------ Freivalds
    "Chapter two. Checking a product with a coin.": "第2章。用硬币检验乘积。",
    "Someone hands you two n by n matrices, A and B, and a third, C":
        "有人交给你两个 n 乘 n 的矩阵 A 和 B，以及第三个矩阵 C，声称 C 是它们的乘积。<bookmark mark='a'/>重新计算乘积来检验，要做 n 的三次方"
        "次乘法；用第19部分最好的方法是 n 的 2.37 次方，而那些方法反正也不实用。<bookmark mark='b'/>1977年，Rūsiņš Freivalds 提出了更便宜的"
        "办法。抛 n 枚硬币，得到一个由零和一组成的随机向量 r。先算 B 乘 r，再用 A 乘它，同时算 C 乘 r：三次矩阵与向量的乘法，大约三倍 n 的"
        "平方次运算。<bookmark mark='c'/>如果两个向量不同，C 肯定是错的。<bookmark mark='d'/>如果相同，C 大概是对的，我们可以用新的硬币再试。"
        "有多大概率是对的？",
    "Suppose C is wrong.":
        "假设 C 是错的。<bookmark mark='a'/>那么差 D，即 A B 减 C，不是零矩阵。<bookmark mark='b'/>它的某个元素 d i j 非零，而检验只有在 D r "
        "是零向量时才通过，所以特别地，要求它的第 i 个分量为零。<bookmark mark='c'/>这个分量等于 d i j 乘 r j，再加上其他硬币贡献的和 s。"
        "<bookmark mark='d'/>想象先抛除 r j 以外的所有硬币。硬币是独立的，所以这不改变任何东西，但现在 s 是一个固定的数。<bookmark mark='e'/>"
        "要让这个分量为零，r j 必须等于负 s 除以 d i j：一个特定的值。r j 的两种结果中至多有一种能做到。<bookmark mark='f'/>所以无论 A、B、C "
        "是什么，错误的 C 通过的概率至多为二分之一，k 轮独立检验让它通过的概率至多为二的负 k 次方。<bookmark mark='g'/>按方便的顺序揭开硬币的"
        "技巧叫作延迟决定原理，我们还会再用到它。",
    'f"On this machine, with matrices of size {d[\'n\']}.':
        "在这台机器上，矩阵大小为 {d['n']}。<bookmark mark='a'/>把它们相乘需要一百六十亿次浮点运算，由一个高度优化的库完成，大约八分之一秒。"
        "检验需要两千四百万次运算。<bookmark mark='b'/>这少了将近七百倍，但矩阵与向量的乘法把时间花在等待内存上，所以按秒算，检验只快了大约 "
        "{d['ratio']:.0f} 倍，这是第9部分的提醒。<bookmark mark='c'/>现在看错误。我们篡改了乘积的一个元素，检验了几千次。一轮检验大约一半的"
        "时间让它通过，两轮是四分之一，依此类推，正好落在上界上。<bookmark mark='d'/>只有一个元素错误时上界是紧的，因为只有一枚硬币起作用。"
        "<bookmark mark='e'/>当许多元素都错时，许多硬币起作用，错误的乘积一次也没有通过。",
    # ------------------------------------------------------------------ Identity
    "Chapter three. Is this polynomial zero?": "第3章。这个多项式是零吗？",
    "Here is a claimed identity:":
        "这是一个声称的恒等式：x 减 y，乘 y 减 z，再乘 z 减 x，与一个展开式。<bookmark mark='a'/>不去展开，而是代入随机数并比较。对 S 的每个"
        "大小，我们做了两万次。<bookmark mark='b'/>这个声称是错的：有一个符号写错了，所以两边相差二倍 x z 的平方，一个三次多项式。它只在 x 或 z "
        "为零时为零，这就是为什么一致率比引理的界三除以 S 稍低一点。S 有一千个值时，五百次检验中被骗一次；二十次检验全被骗的概率低于十的负五十"
        "次方。<bookmark mark='c'/>这个想法可以推广。八乘八范德蒙德矩阵的行列式等于一个差的乘积，展开后是一个有四万项的多项式。在五十个随机点上"
        "对一个大素数取模来计算两边，每次只要不到一毫秒，而且每次都一致。",
    'f"A less obvious polynomial.':
        "一个不那么明显的多项式。<bookmark mark='a'/>取一个图，构造它的 Tutte 矩阵：对每条边 i j，在对角线上方放一个变量 x i j，下方放负 x i j。"
        "<bookmark mark='b'/>对这个图，行列式是一个完全平方，它的两项各对应一个完美匹配，即恰好覆盖每个顶点一次的一组边。<bookmark mark='c'/>"
        "William Tutte 在1947年证明，图有完美匹配当且仅当这个行列式是非零多项式。但它可能有指数多项。<bookmark mark='d'/>László Lovász 在1979年"
        "看出我们根本不必展开它：代入模一个素数的随机数，用消元法算一次行列式，错误由 Schwartz–Zippel 控制。<bookmark mark='e'/>我们在四十八个"
        "随机图上试了它，这些图都在匹配开始出现的阈值附近。其中 {have} 个有完美匹配，行列式每次都与 Edmonds 的开花算法一致。行列式很适合并行"
        "计算，所以这成了快速并行匹配算法的途径。",
    "One more use of the same idea.":
        "同一个想法的另一个用途。<bookmark mark='a'/>Alice 有这些小说，两千五百万字节，Bob 有一份可能不同的副本。为了比较而传送整个文件代价太高。"
        "<bookmark mark='b'/>Alice 把她的文件看成一个巨大的数 a，随机选一个六十一位的素数 p，发送 p 和 a 模 p：十六个字节。Bob 用他自己的数"
        "模 p 来比较。<bookmark mark='c'/>我们把 Bob 副本中的一个比特翻转了。两个余数完全不同，计算一个大约要七分之一秒。<bookmark mark='d'/>"
        "不同的文件什么时候会给出相同的余数？只有当 p 整除它们的差时，而这个差是一个有两亿个比特的数。这样的数至多有几百万个与 p 一样大的素因子，"
        "而这么大的素数有几亿亿个。所以误判的概率大约是百亿分之一，换第二个素数再试一次，就把它平方。第21部分把这变成 Rabin 与 Karp 的字符串"
        "搜索，让余数沿着文本滚动。",
    # ------------------------------------------------------------------ Karger
    "Chapter four. A minimum cut by contraction.": "第4章。用收缩求最小割。",
    "A cut of a graph splits its vertices into two sides":
        "图的一个割把顶点分成两边；割的大小是两边之间的边数。这个图有两个稠密的簇，由三条边相连，所以它的最小割大小为三。求最小割是一个经典问题，"
        "通常用最大流来解。<bookmark mark='a'/>David Karger 1993年的算法简单得几乎令人难为情。随机选一条边并收缩它：把它的两个端点合并成一个"
        "顶点，保留所有其他边，丢掉自环。重复直到只剩两个顶点。它们之间的边就是一个割。<bookmark mark='b'/>这一次运行把三座桥一直保留到最后，"
        "找到了最小割。",
    'f"Run it again with other coins.':
        "用别的硬币再运行一次。<bookmark mark='a'/>这一次，途中有一座桥被收缩了，两个簇被合并在一起。<bookmark mark='b'/>剩下的结果是把单个顶点"
        "与其余部分切开，一个大小为 {d['fail_cut']} 的割。每次运行都可能失败，那么它多常成功？",
    "The analysis is as short as the algorithm.":
        "分析和算法一样短。固定一个大小为 k 的最小割 C。<bookmark mark='a'/>每个顶点至少有 k 条边，否则这一个顶点周围的边就构成一个更小的割。"
        "<bookmark mark='b'/>所以至少有 n k 除以二条边，第一条随机边落在 C 中的概率至多为二除以 n。<bookmark mark='c'/>收缩从不产生更小的割，"
        "所以同样的论证在每一步都成立，先是 n 减一个顶点，再是 n 减二个，依此类推。<bookmark mark='d'/>C 能存活到最后，当且仅当它在每一步都"
        "存活。把乘积写出来，几乎所有项都消掉了：<bookmark mark='e'/>成功概率至少是二除以 n 乘 n 减一，即 n 选二分之一。<bookmark mark='f'/>"
        "还有一个免费的推论。一个特定的最小割至少以这个概率成为输出，而不同的割是不同的结果，所以没有哪个图的最小割超过 n 选二个。",
    'f"We ran the contraction twenty thousand times':
        "我们在双簇图上运行了两万次收缩。每根柱子统计结果为该大小的割的运行次数。<bookmark mark='a'/>最小割出现在 {d['success']:.0%} 的运行中。"
        "上界保证至少一百二十分之一，不到百分之一，所以在这个图上实际情况大约好十五倍。<bookmark mark='b'/>上界是最坏情形，其余的交给重复：运行 "
        "n 选二乘 log n 次，保留最小的割，出错的概率至多为 n 分之一。<bookmark mark='c'/>最坏情形是真实存在的。在一个十个顶点的环中，十条边中"
        "任意两条都构成一个最小割，一共四十五个，正好是 n 选二。各次运行找到了全部四十五个，每个大约四十五次中出现一次，所以这里上界是精确的。",
    # ------------------------------------------------------------------ Primes
    "Chapter five. Primes in milliseconds.": "第5章。几毫秒内的素数。",
    "Part 30 will need prime numbers three hundred digits long":
        "第30部分需要三百位长的素数，而且需要很多。用试除法检验一个，要做十的一百五十次方次除法。<bookmark mark='a'/>费马小定理给出了一条捷径。"
        "如果 n 是素数，那么对每个不被 n 整除的 a，a 的 n 减一次方模 n 等于一。<bookmark mark='b'/>所以只要找到一个 a 使它不等于一，n 就"
        "一定是合数。二的九十次方模九十一是六十四，<bookmark mark='c'/>所以九十一是合数，而我们没有找到任何因子就知道了这一点。<bookmark "
        "mark='d'/>但有些底数会说谎。三的九十次方模九十一是一，就好像九十一是素数一样。<bookmark mark='e'/>每次检验都很便宜：反复平方法计算这个"
        "幂，n 的每一位大约只需一次平方。",
    'f"Worse, some composites fool every base.':
        "更糟的是，有些合数能骗过所有底数。<bookmark mark='a'/>这里是 n 等于五百六十一时从一到五百六十的底数，五百六十一等于三乘十一乘十七。"
        "每个与它没有公因子的底数，全部 {d['fermat_liars']} 个，都通过了费马检验。<bookmark mark='b'/>Alwin Korselt 在1899年解释了原因："
        "这种情况恰好在 n 无平方因子、且对它的每个素因子 p，p 减一都整除 n 减一时发生。五百六十能被二、十和十六整除。<bookmark mark='c'/>"
        "Robert Carmichael 在1910年找到了最早的例子。一百万以下有 {d['carmichael_count']} 个，1994年 Alford、Granville 与 Pomerance 证明了"
        "它们有无穷多个。费马检验需要修补。",
    'f"Gary Miller in 1976 and Michael Rabin in 1980 found the repair.':
        "Gary Miller 在1976年、Michael Rabin 在1980年找到了修补的办法。<bookmark mark='a'/>模一个素数，一的平方根只有一和负一，因为 x 的平方"
        "减一分解为 x 减一乘 x 加一，而在域中，乘积为零仅当某个因子为零。<bookmark mark='b'/>把 n 减一写成二的幂乘一个奇数 d，先算 a 的 d 次方，"
        "再不断平方，直到 a 的 n 减一次方。<bookmark mark='c'/>对素数来说，这个序列要么全是一，要么在第一个一之前的某处出现负一。<bookmark "
        "mark='d'/>看五百六十一取底数二：二百六十三、一百六十六、六十七，然后是一。<bookmark mark='e'/>六十七的平方是一，但它既不是一也不是负一："
        "这是任何素数都不可能有的一的平方根。费马检验被骗了，这个检验没有。<bookmark mark='f'/>Rabin 证明，对每个奇合数，至多四分之一的底数会说谎。"
        "五百六十一只有 {d['strong_liars']} 个。<bookmark mark='g'/>搜索两万以下的每个奇合数，最坏的是九，恰好四分之一，所以这个界不能改进。四十个"
        "随机底数给出的错误低于四的负四十次方，大约十的负二十四次方。",
    # ------------------------------------------------------------------ Walks
    "Chapter six. Random walks that solve SAT.": "第6章。求解 SAT 的随机游走。",
    "A 2-SAT formula is an and of clauses":
        "2-SAT 公式是若干子句的合取，每个子句是两个文字的析取。第18部分用蕴含图的强连通分量精确地解决了它。<bookmark mark='a'/>Christos "
        "Papadimitriou 在1991年分析了一种笨得多的方法。从任意赋值开始。只要有子句不成立，就挑一个，用硬币选它的两个变量之一并翻转。<bookmark "
        "mark='b'/>它完全不利用结构。凭什么它会结束？",
    'f"For 3-SAT the same walk works, but worse.':
        "对 3-SAT，同样的游走也行，但更差。<bookmark mark='a'/>现在一个不成立的子句有三个变量，其中可能只有一个是该翻转的，所以 D 下降的概率只有"
        "三分之一。<bookmark mark='b'/>游走会远离解，所以 Uwe Schöning 在1999年每翻转三倍 n 次就从一个新的随机赋值重新开始。<bookmark "
        "mark='c'/>仔细计算表明，每次重启成功的概率大约是四分之三的 n 次方，所以大约四分之三的倒数的 n 次方次重启就够了：仍是指数，但远少于二的 n "
        "次方个赋值。<bookmark mark='d'/>我们在能造出的最难的小实例上测试了它：阈值处恰有一个满足赋值的随机公式，用穷举法核实。<bookmark "
        "mark='e'/>有 {last['n']} 个变量时，游走平均需要大约 {last['mean_restarts']:.0f} 次重启，低于针对最坏情形的 Schöning 上界，而穷举法"
        "要试大约一百万个赋值。今天已知最好的算法，Paturi、Pudlák、Saks 与 Zane 算法的后继者，能降到大约一点三的 n 次方。是否存在好得多的算法，"
        "正是第27部分指数时间假设背后的问题。",
    # ------------------------------------------------------------------ Bins
    "Chapter seven. Balls into bins, and the power of two choices.": "第7章。球与箱，以及两个选择的力量。",
    "Throw balls into bins at random.":
        "把球随机扔进箱子。最满的箱子会有多满？这个问题决定了哈希表的链（第17部分）或服务器集群的队列平衡得有多好。<bookmark mark='a'/>左边，"
        "二十四个球各自进入十二个箱子中的一个随机箱子。右边，每个球看两个随机箱子，进入较空的那个。<bookmark mark='b'/>两边由同样的随机数驱动："
        "左边用第一个选择，右边两个都用。<bookmark mark='c'/>一个选择会让一些箱子空着，另一些堆得很高。两个选择则出奇地均匀。",
    'f"Now with n balls and n bins':
        "现在是 n 个球和 n 个箱子，n 从一千到一百万。<bookmark mark='a'/>一个选择时，最满的箱子大约有 log n 除以 log log n 个球；旁边一列就是这个"
        "公式，它只在一个非常缓慢地趋于一的因子之内正确，所以测得的负载更高。<bookmark mark='b'/>两个选择时，最满的箱子大约有 log log n 除以 "
        "log 二个球，再加一个常数。一百万个球时：十对四。<bookmark mark='c'/>在一百万时，一个选择的负载服从泊松分布，装有 k 个球的箱子占 e 的负一"
        "次方除以 k 的阶乘，有 {d['hist_one'][-1]} 个倒霉的箱子装了 {len(d['hist_one']) - 1} 个。两个选择时没有超过 "
        "{len(d['hist_two']) - 1} 的。规则上一个微小的改变，结果上一个指数级的改变。这就是两个选择的力量，来自 Azar、Broder、Karlin 与 Upfal "
        "1994年的工作。",
    # ------------------------------------------------------------------ Bloom
    "Chapter eight. Bloom filters.": "第8章。布隆过滤器。",
    "In 1970 Burton Bloom asked how to test membership":
        "1970年，Burton Bloom 问：如果偶尔接受一个错误的“是”，能否用远少于集合本身的内存来检验成员关系？<bookmark mark='a'/>取一个全为零的"
        "比特数组和三个哈希函数。<bookmark mark='b'/>要加入一个词，就把它哈希三次，把那三个比特置一。这里加入《白鲸》中的六个词。<bookmark "
        "mark='c'/>词本身没有存在任何地方。只剩下比特。",
    "To ask whether a word is in the set, check its three bits.":
        "要问一个词是否在集合中，就检查它的三个比特。<bookmark mark='a'/>dog：它有一个比特是零，所以 dog 肯定从未加入。<bookmark mark='b'/>"
        "boat：也有一个零，肯定不在。<bookmark mark='c'/>ocean：它的三个比特都被 whale 置了一，所以过滤器说“是”，错了。这是一个假阳性。"
        "<bookmark mark='d'/>deck：也说“是”，它的比特由 harpoon 和 Queequeg 置一。布隆过滤器对集合中的词从不说“否”，但有时对不在集合中的词"
        "说“是”。这有多常见？",
    "Suppose we add n words to m bits with k hash functions":
        "假设我们用 k 个哈希函数把 n 个词加入 m 个比特，并假定哈希真正随机。<bookmark mark='a'/>某个特定比特被全部 k n 次哈希错过的概率是一减 m "
        "分之一的 k n 次方，约等于 e 的负 k n 除以 m 次方。<bookmark mark='b'/>一个从未加入的词，如果它的 k 个比特恰好都被置一，就是假阳性：概率"
        "约为一减去上面那个数，再取 k 次方。<bookmark mark='c'/>这里有一个平衡。哈希函数少，每次探查很可能碰到置一的比特；哈希函数多，数组会被"
        "填满。<bookmark mark='d'/>微积分给出最好的 k，即 m 除以 n 乘 log 二，此时恰好一半的比特被置一。错误率约为 0.6185 的 m 除以 n 次方。"
        "<bookmark mark='e'/>每个词每多一个比特，错误率大约除以 1.6，每个词十个比特给出大约百分之一，无论词是什么、有多长。",
    'f"Now a real one: all {words(d[\'n\'])} distinct words':
        "现在看一个真实的：小说中全部 {words(d['n'])} 个不同的词，每个词十个比特，用十万个不是小说中词的随机字符串来查询。<bookmark mark='a'/>"
        "紫色曲线是公式，绿色的点是我们对每个哈希函数个数测得的值。<bookmark mark='b'/>在最好的 k 即七时，有百分之 "
        "{best['measured'] * 100:.2f} 的非词溜了过去，预测值是 {best['theory'] * 100:.2f}，而且几乎恰好一半的比特被置一。<bookmark "
        "mark='c'/>每个词十六个比特时，这个比例降到两千分之一。<bookmark mark='d'/>过滤器占七十千字节，而光是这些词的字母就要四百四十千字节，"
        "它也从没漏掉一个真正在集合中的词。<bookmark mark='e'/>计数过滤器允许删除，布谷鸟过滤器在低错误率时更好，几乎每个日志结构的数据库都为"
        "每个文件保存一个布隆过滤器来跳过磁盘读取，第34部分会展示这一点。",
    # ------------------------------------------------------------------ Stream
    "Chapter nine. Streams: one pass, little memory.": "第9章。数据流：一遍扫描，很少的内存。",
    "First, a fair sample.":
        "首先，一个公平的样本。我们想从数据流中均匀地选出 k 项，但不知道它会有多长。<bookmark mark='a'/>蓄水池抽样，按 Jeffrey Vitter 1985年的"
        "描述：保留前 k 项。第 i 项到来时，以 k 除以 i 的概率保留它，并随机扔掉 k 项中的一项。<bookmark mark='b'/>由归纳法，到目前为止见过的每一项"
        "都恰好以 k 除以 i 的概率在样本中。当下一项到来时，一项留下，除非新来者被保留并选中了它的位置，算一下，k 除以 i 就变成 k 除以 i 加一。"
        "<bookmark mark='c'/>我们从一百项中抽五项，抽了五万次：每一项被选中的次数都接近期望的两千五百次。<bookmark mark='d'/>这里是从小说全部"
        "四百六十万个词中一遍扫描、均匀抽出的八个词。",
    "Next, the frequent items, the Job's own question.":
        "接下来是频繁项，正是作业自己的问题。<bookmark mark='a'/>Jayadev Misra 与 David Gries 在1982年给出了一个确定性方法，用 k 减一个计数器。"
        "已有计数器的词加一。新词占用一个空闲计数器。没有空闲计数器的新词让每个计数器减一，减到零的计数器被释放。<bookmark mark='b'/>每次减法一次"
        "抵消 k 个词：新来的一个，以及每个计数器各一个，所以它至多发生 n 除以 k 次。因此每个计数至多偏低 n 除以 k，任何比 n 除以 k 更频繁的词一定"
        "留存下来。<bookmark mark='c'/>在小说上用九十九个计数器，n 除以 k 大约是四万六千。高于它的十三个词全部留存，每个大约少计三万九千，低于它的"
        "词可能消失。第二遍扫描，只统计留存下来的词，就能得到精确的计数。但估计值本身很差。硬币能做得更好吗？",
    "Graham Cormode and S. Muthukrishnan's Count-Min sketch":
        "Graham Cormode 与 S. Muthukrishnan 2005年的 Count-Min 草图保存一张小表：d 行，每行 w 个计数器，每行一个独立的哈希函数。<bookmark "
        "mark='a'/>要加入一个词，每行哈希一次，把那些计数器各加一。<bookmark mark='b'/>要估计一个词的计数，看同样的 d 个计数器，取最小值。"
        "<bookmark mark='c'/>每个计数器都等于这个词的真实计数，加上在那里与它碰撞的其他词的计数。碰撞只会增加，所以估计值从不偏低，而最小值选出了"
        "碰撞最少的那一行。",
    'f"How large can the error be?':
        "误差能有多大？<bookmark mark='a'/>在一行中，多出的部分是哈希到同一个计数器的其他词的总计数。用一个好的哈希族，每个其他词以 w 分之一的概率"
        "落在那里，所以期望的多余量至多为 N 除以 w，N 是数据流的长度。由马尔可夫不等式，多余量达到它的 e 倍的概率至多为 e 分之一。<bookmark "
        "mark='b'/>只有每一行都那么糟，最小值才会那么糟，而各行相互独立，所以概率相乘。<bookmark mark='c'/>取 w 为 e 除以 epsilon，d 为 log "
        "一除以 delta，那么每个估计值以一减 delta 的概率落在真实值的 epsilon N 之内。<bookmark mark='d'/>内存取决于 epsilon 和 delta，与有多少个"
        "不同的词无关。<bookmark mark='e'/>在小说上，用四行、每行 1021 个计数器，保证的上界大约是 {words(round(c['bound']))}，没有一个词接近它，"
        "典型的多余量大约是 {words(round(c['mean_err']))}。用两行时，百分之零点三的词超过了它，远在定理允许的百分之十三点五之内。",
    # ------------------------------------------------------------------ JobSketch
    "Chapter ten. The Job in kilobytes.": "第10章。几千字节里的作业。",
    "Here is the function that runs once per word":
        "这是每个词运行一次的函数，由第13部分的编译器编译。<bookmark mark='a'/>首先是四个计数器的位置，每个是前一个加上步长 g，用一次减法而不是"
        "除法来回绕。<bookmark mark='b'/>估计值是四个计数器中最小的，<bookmark mark='c'/>只有等于它的计数器才被增加。<bookmark mark='d'/>"
        "然后是让程序便宜的那个检验：如果堆已满，而这个词的估计值打不过最弱的候选，就结束。英语中几乎每个词都在这里停下。<bookmark mark='e'/>"
        "已经是候选的词得到新的估计值，在堆中下沉。<bookmark mark='f'/>其他的词加入，或者取代最弱的候选。",
    'f"What does it remember?':
        "它记住了什么？<bookmark mark='a'/>草图是一万六千字节。候选、它们的字母、堆和槽另外大约占两千字节。<bookmark mark='b'/>一共 "
        "{words(total)} 字节，十八点五千字节，在一个连续的块中。<bookmark mark='c'/>第17部分的版本保存每个不同的词，将近五万八千个，每个一个"
        "条目和一个槽：{d['v2_bytes'] / 1000000.0:.1f} 兆字节。<bookmark mark='d'/>少了一百倍。<bookmark mark='e'/>而十八点五千字节装得进第9部分"
        "的一级缓存，所以一旦最初几百个词触及了每一行，程序就再也不会缺失。我们把一段 {d['passage_bytes'] // 1000} 千字节的文本的每次读写都送进"
        "缓存模型来验证：一共 {d['traced_lines']} 行，八路组中任何一组从未超过 {d['max_lines_per_set']} 行。",
    'f"So the ledger gets its ninth row.':
        "于是账本有了第九行。程序的 {big(d['instructions'])} 条指令每一条都在模拟器上运行过，大约每字节文本 {d['per_byte']:.0f} 条，输出与精确计数"
        "逐词逐位一致。<bookmark mark='a'/>按第8部分的处理器计价：一秒，比哈希表慢四分之一。<bookmark mark='b'/>草图对每个词做的工作更多，它那一串"
        "比较每个周期执行的指令更少。<bookmark mark='c'/>哈希表有四千四百万个周期花在等待内存上；草图只有四万六千个。<bookmark mark='d'/>第九行"
        "不是一次提速。它买的是内存：少一百倍，多四分之一的时间。这种交换正是流算法的全部意义，因为对真实的数据流，词汇表是装不下的。",
    'f"But was the exact answer luck?':
        "但这个精确的答案是运气吗？哈希函数就是算法的硬币，所以我们用 C 把同一个算法以二十个不同的哈希函数、在几种草图大小下重新运行。<bookmark "
        "mark='a'/>在程序自己的大小，即四行、每行 1021 个计数器时，报告的前二十名在二十个哈希函数中有五个完全正确，词和计数都对，而程序自己的那个"
        "就是这五个之一。平均二十个词中有 19.1 个正确，从未少于十八个。<bookmark mark='b'/>典型的闯入者是一个在每一行都与常用词碰撞的罕见词："
        "{ex[0]}，它在小说中出现{occ}，被估计为将近五万九千。<bookmark mark='c'/>普通更新从未完全"
        "正确，两行的草图平均只对了十四个词。把宽度加倍到 32 千字节，百分之七十的运行完全正确，64 千字节时是百分之九十五。<bookmark mark='d'/>"
        "这是一个蒙特卡洛算法：内存和时间是有保证的，答案很可能是对的，更多的内存换来更高的概率。<bookmark mark='e'/>还有一个便宜的修补办法。在二十次"
        "运行的每一次中，真正的前二十名都在三十二个候选之中。再扫描一遍文本，只精确统计这三十二个词，每次都会给出精确的答案。",
    # ------------------------------------------------------------------ Distinct
    "Chapter eleven. Counting distinct things: HyperLogLog.": "第11章。统计不同元素：HyperLogLog。",
    "How many different words are in the novels?":
        "小说中有多少个不同的词？精确地数它们，意味着要记住所有的词。<bookmark mark='a'/>Philippe Flajolet 与 Nigel Martin 在1985年有一个更好的"
        "主意。把每个词哈希成一串看起来随机的比特，看它以多少个零开头。重复的词每次都哈希成同样的值，所以重复不改变任何东西。<bookmark mark='b'/>"
        "以 rho 减一个零开头、然后是一个一的哈希，概率是二的负 rho 次方。看到一个这样的哈希，就像连续抛出那么多次正面：在它出现之前，你大约需要二的 "
        "rho 次方个不同的数据项。<bookmark mark='c'/>所以只记住见过的最大秩。这大约需要 log log n 个比特，对你会遇到的任何数量的词都只要五个比特。"
        "<bookmark mark='d'/>但单个记录噪声很大。一个幸运的哈希，估计值就翻倍。",
    "The cure is to average many records.":
        "解药是对许多记录取平均。<bookmark mark='a'/>用每个哈希的前几个比特选择 m 个寄存器之一，每个寄存器保存送到它那里的哈希的最大秩。这是处理完"
        "小说全部词汇后的六十四个寄存器。<bookmark mark='b'/>Philippe Flajolet 和他的同事在2007年用调和平均把它们组合起来，调和平均不会被少数幸运的"
        "寄存器骗到，再乘一个校正偏差的常数。<bookmark mark='c'/>相对误差大约是一点零四除以 m 的平方根。<bookmark mark='d'/>当数据项很少、许多"
        "寄存器还空着时，它改为数空寄存器的个数。",
    'f"We ran HyperLogLog on the novels':
        "我们在小说的词汇上运行 HyperLogLog，对每种寄存器个数用三十个不同的哈希函数。<bookmark mark='a'/>测得的误差沿着表格向下遵循一点零四除以根号 "
        "m：十六个寄存器，偏差四分之一；四千个，百分之一点五，只用三千字节。<bookmark mark='b'/>在四百六十万个词的整个数据流上，估计值是 "
        "{words(round(d['est_corpus']))}，真实值是 {words(d['distinct'])}。<bookmark mark='c'/>而在小说中每一个五词短语上，四百五十万个不同的短语，"
        "同样的三千字节偏差为百分之零点五。精确计数需要一张几十兆字节的表。<bookmark mark='d'/>这就是为什么数据库和分析引擎近似地回答 count "
        "distinct 查询，背后是 HyperLogLog。",
    # ------------------------------------------------------------------ Ams
    "Chapter twelve. Sketching the second moment.": "第12章。为二阶矩画草图。",
    "Counting distinct items and counting the stream's length":
        "统计不同的数据项和统计数据流的长度，是同一个家族的两个情形。<bookmark mark='a'/>第 p 阶频率矩是对所有数据项求和，每项是它的计数的 p 次方。"
        "<bookmark mark='b'/>F 零是不同数据项的个数，即上一章。<bookmark mark='c'/>F 一是数据流的长度，一个计数器就能跟踪。<bookmark mark='d'/>"
        "F 二是计数的平方和，衡量数据流有多集中。<bookmark mark='e'/>它是数据库在那一列上做表的自连接时的行数，当网络看到大量相同的数据包涌来时，它会"
        "猛增。<bookmark mark='f'/>对小说来说它是一千七百七十四亿，单是 the 这个词就贡献了百分之三十。能否不统计每个词就估计 F 二？",
    "Noga Alon, Yossi Matias and Mario Szegedy showed how in 1996":
        "Noga Alon、Yossi Matias 与 Mario Szegedy 在1996年展示了做法，那篇论文开创了流算法的理论。<bookmark mark='a'/>给每个数据项一个随机符号，"
        "正一或负一，只保存一个数 Z：每当一个数据项到来，就加上它的符号。<bookmark mark='b'/>最后，Z 是每个数据项的符号乘它的计数之和。把它平方。"
        "你得到计数的平方，即 F 二，再加上交叉项，每个交叉项是两个不同符号的乘积。<bookmark mark='c'/>独立的符号相乘平均为零，所以 Z 平方的期望恰好"
        "是 F 二。<bookmark mark='d'/>它的方差至多是 F 二平方的两倍，而这个计算只需要四元独立的符号，一个小的哈希函数就能提供。<bookmark mark='e'/>"
        "对 k 个副本取平均，把相对误差降到根号下 k 分之二，再取几个这样的平均值的中位数，就让大的误差变得指数地不可能。<bookmark mark='f'/>均值的"
        "中位数是一个值得记住的技巧：对每个均值用切比雪夫不等式，对中位数用切尔诺夫界。",
    # ------------------------------------------------------------------ Lsh
    "Chapter thirteen. Near-duplicates: MinHash and locality-sensitive hashing.":
        "第13章。近似重复：MinHash 与局部敏感哈希。",
    "Search engines, plagiarism detectors and the people who clean training data":
        "搜索引擎、抄袭检测器，以及为语言模型清洗训练数据的人，都需要找出几乎相同的文档。<bookmark mark='a'/>用瓦片来表示一段文字，即每一串连续的"
        "五个词。<bookmark mark='b'/>两段文字的相似程度，就是它们共有的瓦片所占的比例：杰卡德相似度，交集的大小除以并集的大小。<bookmark mark='c'/>"
        "这两行来自《基督山伯爵》中同一封信的两个版本，它们十个不同的瓦片中共有四个，因为改动一个词会破坏包含它的每一个瓦片。<bookmark mark='d'/>"
        "小说中有三万四千个四十词以上的段落。比较每一对，意味着将近六亿次集合比较。",
    "Andrei Broder found a shortcut in 1997, at the search engine AltaVista.":
        "Andrei Broder 在1997年于搜索引擎 AltaVista 找到了一条捷径。<bookmark mark='a'/>用一个哈希函数把所有瓦片排成一个随机顺序，看两个集合并集中"
        "的第一个瓦片。<bookmark mark='b'/>两个集合的最小哈希相同，当且仅当这第一个瓦片同时属于两者；这里它只在 A 中，所以它们不同。由对称性，并集中"
        "每个瓦片成为第一个的可能性相同。<bookmark mark='c'/>所以两个最小值相同的概率恰好等于杰卡德相似度。<bookmark mark='d'/>用一百个哈希函数"
        "重复，每个段落就变成一个由一百个数组成的签名。两个签名一致的位置所占的比例估计它们的相似度，误差大约在百分之五以内。",
    "Signatures are short, but there are still six hundred million pairs of them.":
        "签名很短，但仍然有六亿对。<bookmark mark='a'/>最后一个技巧，Piotr Indyk 与 Rajeev Motwani 的局部敏感哈希，把签名本身再哈希一次。把每个签名"
        "切成二十段，每段五个数，把每一段放进一张哈希表。<bookmark mark='b'/>两个段落只有在某一段完全相同时才成为候选。<bookmark mark='c'/>一段相同的"
        "概率是 J 的五次方，所以成为候选的概率是一减去一减 J 的五次方的二十次方。<bookmark mark='d'/>这条曲线是一个台阶：相似度低于大约一半的对几乎"
        "从不被比较，高于十分之七的几乎总被比较。我们植入了六百个编辑过的段落副本，每种相似度下被找到的比例都沿着这条曲线。",
    'f"Now the novels.':
        "现在看小说。<bookmark mark='a'/>三万四千个段落，三百五十万个瓦片，六亿对。计算全部签名用了两秒，分段又用了三秒。它只产生了 "
        "{d['candidates']} 对候选。<bookmark mark='b'/>为了核对，我们用倒排索引找出了共有哪怕一个不常见瓦片的每一对段落，并计算了它们的精确相似度。"
        "全部三十部小说中，只有七对共享五分之一的短语。<bookmark mark='c'/>高于阈值的两对都被找到了：两个版本中的一份目录，以及《基督山伯爵》中那封"
        "匿名信，它被引用了不止一次，版本各不相同。其余的，《战争与和平》中重复的一道作战命令和《觉醒》中重复的一段，都落在台阶以下，正如曲线所预测的。"
        "<bookmark mark='d'/>小说家很少重复自己；网络却时时如此。谷歌的爬虫用这个想法的一个近亲，Moses Charikar 的 SimHash，来发现近似重复的网页，"
        "而带分段的 MinHash 是清洗语言模型训练数据的标准步骤。",
    # ------------------------------------------------------------------ ProbMethod
    "Chapter fourteen. The probabilistic method.": "第14章。概率方法。",
    'f"Colour every edge of a complete graph red or blue.':
        "把一个完全图的每条边涂成红色或蓝色。Frank Ramsey 在1930年证明，只要图足够大，无论怎么涂，总有 k 个顶点之间的边全是同一种颜色。<bookmark "
        "mark='a'/>对四个顶点，十七个顶点是不够的。左边是十七个顶点的完全图的一个随机涂色：平均有 {d['k4_mean']:.0f} 组四个顶点是单色的。<bookmark "
        "mark='b'/>右边是一个巧妙的涂色，当两个顶点之差是模十七的平方数时涂蓝色，它一组都没有。十八个顶点则总会有一组，所以拉姆齐数 R(4, 4) 是十八。"
        "<bookmark mark='c'/>对五，没有人知道答案：它在四十三和四十六之间。对大的 k，巧妙的涂色用完了，但硬币没有。",
    "In 1947 Paul Erdős turned the question around.":
        "1947年，Paul Erdős 把问题反过来问。<bookmark mark='a'/>用一枚公平的硬币给每条边涂色。一组特定的 k 个顶点全部同色的概率是二乘二的负 k 选二"
        "次方。<bookmark mark='b'/>对所有的组求和：如果单色组的期望个数小于一，那么一定有某种涂色一组都没有，因为一个随机变量不可能总是高于它自己的"
        "平均值。<bookmark mark='c'/>这个算术对 n 直到大约二的 k 除以二次方都成立。所以拉姆齐数至少是这么多。<bookmark mark='d'/>这是对每个 k，计数"
        "能达到多远。证明表明这样的涂色存在，甚至几乎每一种涂色都可以，但它没有告诉我们怎样写下一个。<bookmark mark='e'/>七十五年后，仍没有人能构造出"
        "接近这么好的涂色。<bookmark mark='f'/>上界四的 k 次方在2023年第一次被改进，改为四减 epsilon 的 k 次方，<bookmark mark='g'/>而来自硬币的"
        "下界自1947年以来几乎没有动过。",
    "Sometimes the good outcome is very unlikely, and counting fails.":
        "有时好的结果非常不可能出现，计数就失效了。<bookmark mark='a'/>假设有许多坏事件，每个的概率都很小，为 p，并且每个只与其余事件中的 d 个"
        "不独立。<bookmark mark='b'/>如果 e 乘 p 乘 d 加一至多为一，那么以正的概率它们一个都不发生。<bookmark mark='c'/>这就是 Erdős 与 Lovász "
        "1975年的洛瓦兹局部引理。概率可以指数地小，但它不是零，所以好的结果存在。<bookmark mark='d'/>例如，一个 k-SAT 公式，如果每个子句与少于大约二的 "
        "k 次方除以 e 个其他子句共享变量，它总是可满足的。<bookmark mark='e'/>三十五年来，这个证明没有给出找到赋值的办法。然后在2010年，Robin Moser "
        "与 Gábor Tardos 证明最朴素的算法就行：只要有子句为假，就给它的变量新的随机值。<bookmark mark='f'/>我们构造了一些 10-SAT 公式，每个子句与大约"
        "三百个其他子句相交，在引理的条件之内。每个公式需要的重新抽样次数，大约只和开始时为假的子句数一样多，远在 m 除以 d 的上界之内。",
    # ------------------------------------------------------------------ Derand
    "Chapter fifteen. Removing the coins, and where they come from.": "第15章。去掉硬币，以及硬币从哪里来。",
    "Can the coins be removed? Sometimes, mechanically.":
        "硬币能去掉吗？有时可以，而且是机械地。<bookmark mark='a'/>看最大割：把图的顶点分成两边，使跨越两边的边尽可能多。它是 NP 难的，第26部分会"
        "证明。<bookmark mark='b'/>随机分割以二分之一的概率切断每条边，所以平均切断一半。<bookmark mark='c'/>现在一次放置一个顶点，把每个顶点放在与"
        "已放置的顶点之间切断更多边的那一边。<bookmark mark='d'/>每一步，在已有选择下的期望割，是两种可能选择的平均，所以较好的选择不会低于它。它从 m "
        "除以二开始，从不下降，所以最终的割，已不再随机，至少是 m 除以二。<bookmark mark='e'/>在一个有二百六十五条边的随机图上，随机分割平均切断一半，"
        "两千次中最好的切断了一百六十二条。沿着期望确定性地走下来，切断了一百七十六条。",
    "There is a second way.":
        "还有第二种办法。<bookmark mark='a'/>最大割的论证一次只看一条边，只涉及两个顶点的硬币。<bookmark mark='b'/>所以硬币不必完全独立，只需两两"
        "独立。<bookmark mark='c'/>两两独立的比特很便宜。取 k 个真正随机的比特 s，让顶点 i 取 s 在 i 的二进制展开为一的那些位上的奇偶性。<bookmark "
        "mark='d'/>任意两个这样的比特都是独立且公平的，所以 k 枚硬币变成了大约二的 k 次方枚。<bookmark mark='e'/>可能的种子只有大约 n 个，我们可以"
        "确定性地试遍每一个，保留最好的割：期望保证其中有一个达到 m 除以二。<bookmark mark='f'/>有限独立性、小偏差空间和扩展图上的游走，第56部分，是"
        "把少量随机比特拉长使用的一般工具。",
    'f"Every algorithm in this part assumed fair, independent coins.':
        "这一部分的每个算法都假定有公平、独立的硬币。计算机通常没有，而是用伪随机数生成器代替。<bookmark mark='a'/>在二十世纪六七十年代，许多科学"
        "程序使用 IBM 的 RANDU：乘以六万五千五百三十九，再模二的三十一次方。<bookmark mark='b'/>这是它连续输出的两千五百个三元组，画成立方体中的点。"
        "它们看起来是随机的。<bookmark mark='c'/>现在转动立方体。<bookmark mark='d'/>乘数是二的十六次方加三，把它平方可以看出，每个输出等于前一个的"
        "六倍减去再前一个的九倍，模二的三十一次方。<bookmark mark='e'/>所以九 u 减六 v 加 w 总是整数，每个点都落在仅仅 {len(d['planes'])} 个平面"
        "之一上。任何用 RANDU 在空间中取样的模拟，取样的都只是十五张薄片。Donald Knuth 称它真正可怕。",
    # ------------------------------------------------------------------ Frontier
    "Chapter sixteen. Frontier: does randomness help?": "第16章。前沿：随机性有用吗？",
    "There is, conditionally.":
        "有，在一定条件下。<bookmark mark='a'/>把 BPP 称为：用硬币的多项式时间算法能以至多三分之一的错误解决的问题。<bookmark mark='b'/>假设我们有一个"
        "伪随机数生成器，能把对数个真正随机的比特拉长成 n 个比特，任何小电路都无法把它们与硬币区分开。<bookmark mark='c'/>那么我们就可以试遍每一个种子，"
        "只有多项式多个，再取多数答案。完全不用硬币。<bookmark mark='d'/>Noam Nisan 与 Avi Wigderson，随后 Russell Impagliazzo 与 Wigderson，"
        "展示了怎样从任何足够难的函数构造这样的生成器。<bookmark mark='e'/>如果某个能在指数时间内解决的问题需要指数大的电路，那么 P 等于 BPP：每个随机"
        "算法都能以多项式的减速去随机化。<bookmark mark='f'/>难的函数造出好的硬币。大多数复杂性理论学者相信 P 等于 BPP，第27部分会把这个论证进一步展开。",
    "And the converse holds too, which is why the question is so hard.":
        "而反方向也成立，这就是这个问题如此困难的原因。<bookmark mark='a'/>多项式恒等式检验问：一个算术电路计算的是否是零多项式。<bookmark mark='b'/>"
        "有硬币时它很容易：在一个随机点上求值，第3章。<bookmark mark='c'/>没有硬币时，不知道任何多项式时间算法。<bookmark mark='d'/>Valentine "
        "Kabanets 与 Russell Impagliazzo 在2004年证明，一个确定性算法本身就会证明一种电路下界，而那种下界复杂性理论已经追寻了五十年。<bookmark "
        "mark='e'/>所以去掉这一枚硬币，与下界方面的重大未解问题一样难。<bookmark mark='f'/>一些特殊情形已经解决，比如稀疏多项式和某些受限的电路，"
        "2016年的匹配结果也来自这一研究方向。",
    "For sketches, the theory is unusually complete.":
        "对于草图，理论异常完整。<bookmark mark='a'/>把不同数据项的个数统计到一加减 epsilon 以内，需要大约一除以 epsilon 平方个比特，再加 log n，"
        "2010年 Daniel Kane、Jelani Nelson 与 David Woodruff 恰好达到了它。二阶矩类似。对更高阶的矩，多项式大小的空间被证明是必需的。Count-Min "
        "在估计单个计数上接近最优，而在小空间里找出精确的前几名是不可能的：作业的草图必定有时会出错。<bookmark mark='b'/>下界来自通信复杂性。如果存在"
        "一个小草图，两个人就可以互相传递它，解决一个被证明需要长时间交谈的问题。第27部分会证明这些。",
    "Here is where things stand. <bookmark mark='a'/> Does P equal BPP":
        "这就是现状。<bookmark mark='a'/>P 等于 BPP 吗？能否不先证明电路下界就证明它？<bookmark mark='b'/>多项式恒等式有没有确定性的多项式时间检验？"
        "<bookmark mark='c'/>有没有人能写下一个完全图的涂色，和随机涂色一样好？2016年以后，借助双源提取器，显式构造有了巨大的进步，但仍有差距。"
        "<bookmark mark='d'/>能否不用硬币，对每个图都在并行中快速找到完美匹配？<bookmark mark='e'/>这一部分的研究题处理的是第二个。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part. Las Vegas and Monte Carlo":
        "这一部分我们造了什么。拉斯维加斯与蒙特卡洛，以及放大。Freivalds 的检验和 Schwartz–Zippel 引理，以及完美匹配和指纹。Karger 的随机收缩。"
        "Miller–Rabin。求解可满足性的随机游走，球与箱，以及两个选择的力量。布隆过滤器、蓄水池、Misra–Gries 和 Count-Min，以及十八千字节里的作业。"
        "HyperLogLog、AMS 草图和 MinHash。概率方法，以及去掉硬币的办法。",
    "Where this comes back. Part 21 turns fingerprints":
        "这些会在哪里再出现。第21部分把指纹变成 Rabin 与 Karp 的字符串搜索，第22部分用局部敏感哈希寻找最近邻。第23部分随机地舍入线性规划，包括最大割"
        "著名的 0.878。第27部分发展 BPP、硬度与随机性，以及数据流的下界。第29部分构造密码学生成器，第30部分需要大素数。第34部分的存储引擎为每个文件"
        "保存一个布隆过滤器；第46和47部分在生产中运行草图和 SimHash；第48部分的负载均衡器使用两个选择，而第56部分构造扩展图。",
    "In practice. Databases put Bloom filters in front of their files":
        "在实践中。数据库在文件前面放布隆过滤器，用 HyperLogLog 回答 count distinct 查询。路由器用草图跟踪频繁项，负载均衡器在两台服务器中挑较闲的"
        "那台。现代缓存用一个 Count-Min 过滤器决定保留什么。网络爬取的数据和语言模型的训练集用 MinHash 去重。而每一次安全连接都从随机素数和一个密码学"
        "生成器开始。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整的解答在这一部分的讲义里。在任何一道上都可以暂停。第五道是动手题：用 Pebble 语言实现 HyperLogLog，这门语言没有位运算，所以秩"
        "要靠反复折半得到。最后一道标着星号，是研究题：它的答案还不知道，讲义里说了从哪里开始。",
    "Next time, the oldest data of all, text.":
        "下一次，最古老的数据：文本。高效地搜索它，引出了由模式构造的自动机、所有后缀的索引，以及一种把一本书排成可压缩的字符串的可逆变换，让我们可以在"
        "小说保持压缩的状态下搜索它们。而每一次 git diff 原来都是网格上的一条最短路径。第21部分，字符串。",
    "The books and papers this part follows":
        "这一部分所依据的书和论文都在屏幕上，也在讲义里。感谢收看。",
    'f"Fix one satisfying assignment, x star':
        "固定一个满足赋值 x 星，令 D 为我们的赋值与它不同的变量个数。<bookmark mark='a'/>一个不成立的子"
        '句两个文字都为假，但 x 星至少使其中一个为真，所以在这两个变量中，我们至少有一个与 x 星不同。<bookmark m'
        "ark='b'/>随机翻转两者之一，以至少二分之一的概率使 D 向零靠近一步。<bookmark mark='c'/>于"
        '是 D 在从零到 n 的直线上做随机游走，被推向零的次数至少和远离的一样多。这就是赌徒破产问题。从任何起点出发，到达零的'
        "期望时间至多为 n 的平方。<bookmark mark='d'/>这是一次游走，从八步之外开始。它用了 {len(pa"
        "th) - 1} 次翻转。我们甚至可能更早停下，停在另一个解上。<bookmark mark='e'/>所以运行二倍 n"
        ' 平方步。如果公式可满足，马尔可夫不等式说我们失败的概率至多为二分之一，其余的交给重复。这个上界针对最坏的公式：在多达三'
        '百二十个变量的随机可满足公式上，游走每个变量只需要大约两次翻转。',
    "On the novels. <bookmark mark='a'/> One copy of the sketch is wild":
        "在小说上。<bookmark mark='a'/>草图的单个副本很狂野：这是四百个 F 二的单次估计，各自除以真实值。它"
        "们从接近零分散到大好几倍，偶尔大十倍，但它们的平均值是对的。<bookmark mark='b'/>对 k 个副本取平均"
        "，正如预测的那样收紧，大约是根号下 k 分之二。<bookmark mark='c'/>九个平均值的中位数切掉了偶尔出现"
        '的坏平均值。每组六十四个副本、共九组时，四十次试验中最坏的一次偏差百分之十七，只用了不到六百个数。Z 的每个副本都是计数'
        '向量与随机符号的点积，即一次随机投影，也就是人工智能系列中的 Johnson–Lindenstrauss 思想；而且因为'
        '它是线性的，两个数据流的草图直接相加即可。',
    'Part 17 kept every distinct word of the novels':
        "第17部分保存了小说中的每个不同的词，将近五万八千个。如果我们负担不起呢？<bookmark mark='a'/>在流模"
        "型中，数据项只经过一次，<bookmark mark='b'/>无法存下来，<bookmark mark='c'/>而内"
        "存远小于数据流，往往比其中不同数据项的个数还小。<bookmark mark='d'/>路由器、传感器、日志和查询规划器"
        '都生活在这个世界里。',
    'f"Where is the waste?':
        "浪费在哪里？<bookmark mark='a'/>早期的收缩几乎从不碰到最小割，<bookmark mark='b'/"
        ">所以所有风险都在最后。<bookmark mark='c'/>Karger 与 Clifford Stein 在199"
        "6年只收缩到大约 n 除以根号二个顶点，这时割仍以至少二分之一的概率存活，<bookmark mark='d'/>然后递"
        "归两次，保留较好的结果。<bookmark mark='e'/>这需要 n 平方 log n 的时间，成功概率大约是一除"
        "以 log n，而不是一除以 n 的平方。<bookmark mark='f'/>在我们四十八个顶点的测试图上，一次普通"
        "收缩成功的比例是 {d['karger_success']:.0%}；Karger–Stein 的四十次运行全部成功。",
    "Freivalds' check is a special case of a more general fact.":
        "Freivalds 的检验是一个更一般事实的特例。<bookmark mark='a'/>一个不恒为零的多项式不可能在太"
        '多点上为零：如果 p 的次数为 d，每个变量都从集合 S 中随机选取，那么 p 在该点为零的概率至多为 d 除以 S 的'
        '大小。这就是 Schwartz–Zippel 引理，大约在1980年由 Schwartz、Zippel，以及 DeMil'
        "lo 与 Lipton 各自独立发现。<bookmark mark='b'/>只有一个变量时，它就是 d 次多项式至多有"
        " d 个根这一事实。<bookmark mark='c'/>变量更多时，把 p 写成第一个变量的多项式，最高次数为 k。"
        '要么它的最高次系数为零，由归纳假设，概率至多为 d 减 k 除以 S；要么 p 成为一个变量的非零 k 次多项式，为零的'
        '概率至多为 k 除以 S。两者相加是 d 除以 S。',
    'Now we can find big primes:':
        "现在我们可以找大素数了：随机选大小合适的奇数，保留第一个通过四十轮检验的。<bookmark mark='a'/>n 附"
        '近大约每 log n 个数中有一个素数，所以一次 1024 位的搜索大约要试三百五十个奇数候选。<bookmark ma'
        "rk='b'/>几乎所有候选在第一轮就失败，在这里一轮要三毫秒，用纯 Python 找一个 1024 位素数大约用了一秒"
        "。<bookmark mark='c'/>2002年，Manindra Agrawal、Neeraj Kayal 与 N"
        'itin Saxena 找到了一个多项式时间的确定性检验，解决了一个非常古老的问题。但它慢得多，<bookmark ma'
        "rk='d'/>每个密码学库仍然在抛硬币。",
    "Why? <bookmark mark='a'/> Let beta i be the number of bins":
        "为什么？<bookmark mark='a'/>令 beta i 为至少装有 i 个球的箱子数。<bookmark ma"
        "rk='b'/>一个球只有在它的两个箱子都已至少有 i 个球时，才会落在第 i 加一层，<bookmark mark='"
        "c'/>概率大约是 beta i 除以 n 的平方。所以每一层的比例大约是下一层比例的平方。<bookmark mark"
        "='d'/>平方让它迅速崩塌：四分之一、十六分之一、二百五十六分之一、六万五千分之一，大约 log log n 步之后就"
        "低于 n 分之一。<bookmark mark='e'/>一个选择时没有平方，只有 k 的阶乘分之一。<bookmark"
        " mark='f'/>d 个选择时负载是 log log n 除以 log d，所以大部分收益来自第二个选择。<book"
        "mark mark='g'/>负载均衡器正是用这条规则，布谷鸟哈希给每个键两个位置。",
    'Modern generators are far better.':
        "现代的生成器好得多。<bookmark mark='a'/>1998年的梅森旋转算法是 Python random 模块"
        '背后的算法，能通过常见的统计检验，但它是线性的：六百二十四个输出就暴露了以后的每一个输出。用于模拟没问题，用于保密毫无用'
        "处。<bookmark mark='b'/>PCG 和 xoshiro 更小、更快；numpy 用的是 PCG。<boo"
        "kmark mark='c'/>ChaCha20 这样的密码学生成器的设计目标是：只要密码是安全的，任何高效的检验都无法"
        "把它们与硬币区分开；第29部分会构造它们。<bookmark mark='d'/>而种子来自物理噪声，由操作系统汇集起来"
        '。',
    "Many of this part's coins have since been removed, one problem at a time.":
        "这一部分的许多硬币后来都被去掉了，一次一个问题。<bookmark mark='a'/>素性检验在2002年有了确定性的"
        '多项式检验；对数空间的连通性检验在2005年去掉了随机游走；近线性时间的最小割在2015年、对带权图在2024年成为确定'
        '性的；2016年，Fenner、Gurjar 与 Thierauf 几乎去掉了并行二部图匹配中的硬币。<bookmark'
        " mark='b'/>每一项都花了多年，各需要自己的想法。这一再成功，背后有没有一般的原因？",
    'Now the Job itself, rebuilt so that it never stores the vocabulary.':
        "现在是作业本身，重新构造成从不存储词汇表。<bookmark mark='a'/>一个四行、每行 1021 个计数器的 "
        "Count-Min 草图估计每个词的计数。<bookmark mark='b'/>只保留三十二个词，作为前二十名的候选，"
        "放在按估计值排序的堆里；一个词的估计值超过最弱的候选时就取代它。<bookmark mark='c'/>一张有一百二十八"
        '个槽的表在候选中查找一个词，被逐出的候选通过把邻居向后移动来删除，即 Knuth 的算法 R。<bookmark mar'
        "k='d'/>Estan 与 Varghese 的保守更新只增加处于最小值的计数器：它仍然从不偏低，但给其他词增加的要少"
        "得多。<bookmark mark='e'/>而双重哈希每个词只用一次除法就给出全部四行的位置。",
}

PHRASES = {"once": "一次"}
