"""Chinese narration for cs26: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第26部分：P 与 NP"

CHAPTERS = {
    "Hook": "找到与检查",
    "Polynomial": "1. 什么才算高效",
    "Hierarchy": "2. 更多时间，更多问题",
    "Np": "3. NP：答案可检查的问题",
    "Reductions": "4. 归约与完全性",
    "CookLevin": "5. Cook–Levin：SAT 是 NP 完全的",
    "Web": "6. 归约之网",
    "Everywhere": "7. 无处不在的 NP 完全性",
    "Numbers": "8. 强难与弱难",
    "CoNp": "9. coNP 与多项式层级",
    "Space": "10. 空间：博弈与交替",
    "Sqrt": "11. 平方根空间里的时间",
    "Ladner": "12. 介于 P 与 NP 完全之间",
    "Sat": "13. 实践中的 SAT",
    "Barriers": "14. 为什么它难",
    "Worlds": "15. 五个可能的世界",
    "Frontier": "16. 前沿：关于复杂性的复杂性",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In March 1956 Kurt Gödel wrote a letter to John von Neumann.":
        "1956年3月，Kurt Gödel 给 John von Neumann 写了一封信。<bookmark mark='a'/>机器显然可以对任何公式和任何数 n，判定这个公式有没有长度为 n "
        "的证明：把它们全试一遍就行。Gödel 写道，问题在于，对最好的机器而言，所需的步数增长得有多快。<bookmark mark='b'/>如果它只像 n 或 n 的平方那样"
        "增长，那么数学家在是非问题上的脑力劳动就可以完全由机器代替。<bookmark mark='c'/>von Neumann 当时身患癌症，奄奄一息，始终没有回信。"
        "<bookmark mark='d'/>这封信几十年后才被发现。它比其他任何人早了十五年，问出了这一部分的问题：找到一个证明，是否和检查一个证明一样容易？",
    "Here is the question in modern form.":
        "这是这个问题的现代形式。<bookmark mark='a'/>六十个点，一百一十二条连线。把每个点涂成蓝、黄或绿，使得没有连线连接同色的两点。<bookmark "
        "mark='b'/>如果有人递给你一种涂法，检查它很容易：每条连线看一次。五微秒。<bookmark mark='c'/>靠尝试每种可能来找，意味着三的六十次方种涂法，"
        "大约七千万亿年。<bookmark mark='d'/>我们第13章的求解器大约一毫秒就找到一种。但没人知道一种保证在每个图上都快的方法，也没人证明这样的方法"
        "不存在。找到与检查之间的这道鸿沟，就是 P 与 NP 问题。",
    "Part 26 of Computer Science, Built: P versus NP.":
        "计算机科学，从零搭建，第26部分：P 与 NP。<bookmark mark='a'/>这一部分包括：什么才算高效，以及区分时间类和空间类的定理；NP、归约，以及 "
        "Cook-Levin 定理，把它建成公式并求解；把上千个问题连在一起的归约之网，每一个都实际计算；coNP、多项式层级、博弈与空间，以及2025年一个"
        "关于时间与空间的惊喜；实践中的 SAT 求解器；为什么这个问题抵挡住了五十年的进攻；以及我们可能生活在其中的五个世界。",
    # ------------------------------------------------------------------ Polynomial
    "Chapter one. What counts as efficient.": "第1章。什么才算高效。",
    "Suppose a computer takes a microsecond per step.":
        "假设计算机每步用一微秒。<bookmark mark='a'/>一个需要 n 平方步的算法，处理一百个元素要十毫秒。n 立方要一秒。<bookmark mark='b'/>二的 n 次方"
        "在二十时没问题，在六十时毫无希望：三万六千年。到一百时，是四乘十的十六次方年。而 n 的阶乘在六十时，超过任何数量的宇宙寿命。<bookmark "
        "mark='c'/>宇宙的年龄是一百四十亿年。<bookmark mark='d'/>更快的硬件救不了指数算法。快一千倍的计算机，能让 n 平方算法处理大三十一倍的输入，"
        "却只能让二的 n 次方算法多处理十个元素。",
    "This is why theorists draw the line at polynomials.":
        "这就是为什么理论家把界线划在多项式上。<bookmark mark='a'/>Jack Edmonds 在1965年关于匹配的论文中，把运行时间以输入规模的多项式为界的算法"
        "称为好算法，他的开花算法就以这种方式在任意图中找到最大匹配。<bookmark mark='b'/>同一年，Alan Cobham 注意到，这类问题构成的类不依赖于机器。"
        "<bookmark mark='c'/>在单带上模拟多带图灵机会把时间平方，正如第1部分所示，而随机访问机至多是立方。多项式仍然是多项式。<bookmark "
        "mark='d'/>它们还能复合：一个多项式算法调用多项式子程序多项式次，仍然是多项式的。<bookmark mark='e'/>每种合理的计算模型都在这个类上一致，"
        "这一主张叫作扩展的 Church-Turing 论题，而第53部分的量子计算机是对它最严肃的挑战。<bookmark mark='f'/>也有保留。n 的一百次方毫无用处，"
        "而一点零零零一的 n 次方往往没问题。但自然问题很少落在那里，而一旦某个问题被证明属于 P，指数通常会降下来。",
    # ------------------------------------------------------------------ Hierarchy
    "Chapter two. More time, more problems.": "第2章。更多时间，更多问题。",
    "Can we prove that some problems need more time than others?":
        "我们能证明有些问题比别的需要更多时间吗？<bookmark mark='a'/>能，用第1部分的对角线论证再加一个时钟。Juris Hartmanis 和 Richard Stearns "
        "在1965年证明了它。<bookmark mark='b'/>造一台机器 D。给定一台机器 M 的描述，它在这个描述上运行 M，但在 f(n) 步后停止。若 M 接受，D 就拒绝；"
        "否则就接受。<bookmark mark='c'/>带时钟模拟要多付一个对数因子，所以 D 运行的时间比 f(n) 多一点点。<bookmark mark='d'/>现在假设某台机器 M 在 "
        "f(n) 步内判定 D 的语言。<bookmark mark='e'/>在 M 的描述上运行 D。时钟给了 M 足够的时间，所以 D 能完成 M 的计算并反着做。<bookmark "
        "mark='f'/>它们不一致，所以没有那么快的机器能判定它。<bookmark mark='g'/>特别地，P 严格小于指数时间。有些问题可证明地需要指数时间；只是我们"
        "证明不了任何 NP 问题是其中之一。",
    "Here is the map of the classes this part needs.":
        "这是这一部分需要的类的地图。<bookmark mark='a'/>对数空间，它的非确定版本，多项式时间，NP，多项式空间，指数时间，指数空间。每一个都在下一个"
        "之内。<bookmark mark='b'/>层级定理证明其中一些是不同的。P 不是指数时间；对数空间不是多项式空间。<bookmark mark='c'/>所以在 P 和指数时间之间，"
        "至少有一个包含是严格的，但没人知道是哪一个。也可能每一个都是严格的。<bookmark mark='d'/>空间与时间的行为不同，因为空间可以重复使用。运行 t 步"
        "的机器至多访问 t 个格子；而使用 s 个格子的机器，格局数至多是 s 的指数，所以它要么在那么多步内停机，要么永远循环。",
    "For space, nondeterminism can be removed at a modest price.":
        "对于空间，非确定性可以用适度的代价去掉。<bookmark mark='a'/>Walter Savitch，1970年。要判定格局 b 能否在 t 步内从 a 到达，就尝试每一个可能的"
        "中点 m，递归地问：m 能否在一半时间内从 a 到达，b 能否从 m 到达。<bookmark mark='b'/>我们在四、八、十六个节点的路径上运行了它。n 每翻一倍，"
        "递归深度加一。<bookmark mark='c'/>每层递归只记住三个格局，<bookmark mark='d'/>而一台使用空间 s 的非确定机器的格局数是 s 的指数，所以深度是 "
        "s 量级，总空间是 s 平方量级。<bookmark mark='e'/>时间则是另一回事：十六个节点要四万七千次调用，增长得比任何多项式都快。Savitch 节省的是空间，"
        "不是时间。<bookmark mark='f'/>推论：带猜测的多项式空间等于不带猜测的多项式空间。时间是否也这样，正是这一部分的问题。",
    # ------------------------------------------------------------------ Np
    "Chapter three. NP: problems with checkable answers.": "第3章。NP：答案可检查的问题。",
    "Here is the definition that makes the hook's question precise.":
        "这是让开头那个问题变精确的定义。<bookmark mark='a'/>验证器是一个多项式时间的程序，它接收输入和一个证书，即一个候选证明。<bookmark mark='b'/>"
        "如果对每个“是”的实例，都有某个短证书使验证器接受，而对每个“否”的实例都没有，这个问题就属于 NP。<bookmark mark='c'/>对着色问题，证书就是涂法。"
        "对可满足性，是赋值；对合数判定，是一个因子。<bookmark mark='d'/>注意这种不对称。“是”有一个你能检查的证明。“否”，比如“这个图不能着色”，可能"
        "根本没有短证明。这种不对称在第9章会再出现。",
    "The N in NP stands for nondeterministic, and the two views agree.":
        "NP 里的 N 代表非确定性，而两种观点是一致的。<bookmark mark='a'/>非确定机器在每个选择处分叉，只要有一个分支接受就接受。给定这样一台机器，证书"
        "就是沿一个接受分支的选择列表，<bookmark mark='b'/>验证器在多项式时间内重放这一个分支。<bookmark mark='c'/>反过来，给定验证器，一台非确定机器"
        "一位一位地猜出证书，再运行验证器。<bookmark mark='d'/>所以 NP 恰好就是非确定多项式时间。<bookmark mark='e'/>P 中的每个问题都属于 NP，因为验证器"
        "可以忽略证书。而 NP 包含于多项式空间，因为一台机器可以依次尝试每个证书，重复使用同样的格子。",
    "A few members of the class.":
        "这个类里的几个成员。<bookmark mark='a'/>可满足性、团、哈密顿回路和子集和：每个都有显而易见的证书，而对每一个，已知最好的算法都需要指数时间。"
        "<bookmark mark='b'/>图同构，即两个图在重新命名后是否相同，抵抗了几十年，直到 László Babai 在2015年找到一个拟多项式算法：不完全是多项式，"
        "但很接近。<bookmark mark='c'/>而素性判定结果属于 P：Manindra Agrawal、Neeraj Kayal 和 Nitin Saxena 在2002年找到一个确定性的多项式检验，"
        "当时 Kayal 和 Saxena 还是本科生。<bookmark mark='d'/>对前四个，除了指数算法什么都不知道。接下来几章说明它们为什么同生共死。",
    # ------------------------------------------------------------------ Reductions
    "Chapter four. Reductions and completeness.": "第4章。归约与完全性。",
    "Part 25 carried impossibility from problem to problem with reductions.":
        "第25部分用归约把不可能性从一个问题带到另一个问题。这里给它们加上预算。<bookmark mark='a'/>如果一个多项式时间函数 f 把 A 的每个实例变成答案相同"
        "的 B 的实例，就说 A 多项式时间归约到 B。<bookmark mark='b'/>那么 B 的快速求解器就给出 A 的快速求解器：算出 f，再去问。多项式套多项式仍是多项式。"
        "<bookmark mark='c'/>反过来读，如果 A 难，那么 B 至少一样难。<bookmark mark='d'/>而且归约可以串联：若 A 归约到 B，B 归约到 C，则 A 归约到 C。",
    "Now the key definitions.":
        "现在是关键的定义。<bookmark mark='a'/>如果 NP 中的每个问题都归约到某个问题，它就是 NP 难的。<bookmark mark='b'/>如果它此外本身也属于 NP，它就是 "
        "NP 完全的：这个类里最难的问题。<bookmark mark='c'/>只要有一个 NP 完全问题有多项式算法，通过复合归约，NP 中的每个问题都会有，P 就等于 NP。"
        "<bookmark mark='d'/>只要其中一个被证明没有多项式算法，它们就都没有。<bookmark mark='e'/>但 NP 完全问题是否存在，并不显然。要证明一个，你需要"
        "同时从 NP 中的每个问题归约过来，包括还没人想到的那些。Stephen Cook 和 Leonid Levin 做到的正是这一点。",
    "One more consequence of completeness.":
        "完全性的另一个推论。NP 是用是非问题定义的，但我们通常想要的是解本身。<bookmark mark='a'/>假设我们只有一个 SAT 的判定过程。把第一个变量设为一，"
        "问公式是否仍然可满足。若是，就保留；若否，它必须是零。然后是下一个变量。<bookmark mark='b'/>在第6章要用到的那个小公式上，五个问题，一个用来检查，"
        "每个变量一个，就得到一个满足赋值。这叫作自归约性。<bookmark mark='c'/>所以快速的判定过程也会带来快速的搜索：P 等于 NP 意味着能找到，而不只是"
        "能判定。<bookmark mark='d'/>每个 NP 完全问题都这样。分解因数是个有趣的例外：判定一个数是否为合数很容易，正如第3章所说，但找出一个因子似乎很难。",
    # ------------------------------------------------------------------ CookLevin
    "Chapter five. Cook-Levin: SAT is NP-complete.": "第5章。Cook-Levin：SAT 是 NP 完全的。",
    "Stephen Cook in 1971, and Leonid Levin independently in the Soviet Union":
        "1971年的 Stephen Cook，以及在苏联独立工作的 Leonid Levin，证明了可满足性是 NP 完全的。证明把整个计算写成一张表。<bookmark mark='a'/>任取 NP "
        "中的一个问题，由一台非确定机器在多项式时间内判定。我们的机器问输入里是否含有一：它向右移动，遇到一时可以猜测接受。<bookmark mark='b'/>把计算写成"
        "一张表格。第 t 行是 t 时刻的纸带，读写头所在的格子标上状态。这里输入是零、零、一、零；在时刻二，读写头到达那个一并作出猜测，此后一直停在接受"
        "状态。<bookmark mark='c'/>现在看一个小窗口，两行三列。<bookmark mark='d'/>机器是局部的：一步之内，只有读写头旁边的格子会变。<bookmark "
        "mark='e'/>所以一张有限的合法窗口清单，对我们的机器是四百零八个，就描述了每一种可能的步。<bookmark mark='f'/>如果表格中的每个窗口都在清单上，"
        "每一行就确实是上一行的后继。",
    "Now turn the tableau into a formula.":
        "现在把表格变成公式。<bookmark mark='a'/>对每个格子和每个符号，一个变量：当那个格子里是那个符号时为真。公式有四个部分。<bookmark mark='b'/>"
        "每个格子恰好有一个符号。<bookmark mark='c'/>第一行是输入，机器在左端处于开始状态。<bookmark mark='d'/>每个窗口都是合法的。<bookmark "
        "mark='e'/>并且在某处，出现了接受状态。<bookmark mark='f'/>满足赋值恰好就是一张接受的表格，所以公式可满足，当且仅当某个分支接受。<bookmark "
        "mark='g'/>表格是 T 乘 T 的，每个格子对应常数量的公式，所以规模是多项式的。<bookmark mark='h'/>而且构造只需要机器和输入，从不需要答案。这就是"
        "从 NP 中每个问题到 SAT 的多项式归约。",
    "We implemented the construction.":
        "我们实现了这个构造。<bookmark mark='a'/>对二到八个符号的输入，公式从三千个变量增长到两万三千个，大致是时间界的平方。<bookmark mark='b'/>我们的 "
        "SAT 求解器，也就是第13章讲解的那个，在不到一秒内找到满足赋值；对输入零、零、零、零，它证明不存在满足赋值。<bookmark mark='c'/>把赋值逐格读回，"
        "就重现了我们画的那张接受表格。一个关于机器的问题变成了一个关于公式的问题。",
    # ------------------------------------------------------------------ Web
    "Chapter six. The web of reductions.": "第6章。归约之网。",
    "Once one problem is NP-complete, the rest get easier.":
        "一旦有一个问题是 NP 完全的，其余的就容易了。<bookmark mark='a'/>要证明新问题 B 是 NP 完全的，只要把它放进 NP，再把 SAT 或任何已知的 NP 完全"
        "问题归约到它。<bookmark mark='b'/>第一步是三-SAT，每个子句至多三个文字：把长子句拆成一串由新变量连起来的短子句。<bookmark mark='c'/>这里有一个"
        "小公式：四个变量上的五个子句，十六种赋值中有七种满足它。<bookmark mark='d'/>我们会把它推过三个归约，求解每个伪装后的问题，再把答案翻译回来。",
    "First disguise: independent set.":
        "第一种伪装：独立集。在一个图中选出 k 个顶点，任意两个之间没有边。<bookmark mark='a'/>为每个子句做一个三角形，每个文字一个顶点。由于三角形的"
        "顶点两两相连，每个子句至多只能选一个。<bookmark mark='b'/>再把每个文字和它的每个否定副本连起来，这样就永远不会同时选中 x 和非 x。<bookmark "
        "mark='c'/>一个五个顶点的独立集，从每个子句选出一个文字，并且互相一致：这就是一个满足赋值。我们的求解器找到了一个，就是这五个绿色顶点。"
        "<bookmark mark='d'/>同样的五个顶点在补图中构成一个团，另外十个构成一个顶点覆盖。所以团和顶点覆盖也是 NP 完全的，几乎不费吹灰之力。",
    "Second disguise: colouring a graph with three colours.":
        "第二种伪装：用三种颜色给图着色。<bookmark mark='a'/>从一个三角形开始，它的三种颜色命名为真、假和基底。<bookmark mark='b'/>对每个变量，两个"
        "顶点 x 和非 x，彼此相连并都连到基底：其中一个必须是真色，另一个是假色。<bookmark mark='c'/>对每个子句，一个小部件，它的输出顶点只有在某个输入"
        "为真时才能是真色；三个文字就串两个，并把输出连到假和基底，迫使它为真。<bookmark mark='d'/>我们的公式变成一个四十一个顶点的图。写成给求解器的 "
        "SAT 问题，是一百二十三个变量。<bookmark mark='e'/>它找到的着色，读回成真值，满足原来的公式。<bookmark mark='f'/>而一个不可满足的公式，经过同样的"
        "构造，得到的图不能三着色。这一点我们也检查了。",
    "Third disguise, with no graphs at all: subset sum.":
        "第三种伪装，完全没有图：子集和。从这些数中挑一些，恰好凑出目标。<bookmark mark='a'/>每个数用十进制写，每个变量一列，每个子句一列。数 y i 在变量 "
        "i 的列上是一，在每个含有 x i 的子句列上也是一；z i 对非 x i 做同样的事。<bookmark mark='b'/>目标在每个变量列上是一，所以 y i 和 z i 恰好只能选"
        "一个：一个真值。<bookmark mark='c'/>它在每个子句列上是三。选中的文字在那里贡献一到三，每个子句的两个松弛数可以补足，但前提是至少有一个文字为真。"
        "<bookmark mark='d'/>没有哪一列会超过五个一，所以没有进位，各列互不干扰。<bookmark mark='e'/>绿色的行来自我们求解器的赋值，它们加起来恰好等于"
        "目标。数变成了逻辑。",
    "In 1972, a year after Cook, Richard Karp showed":
        "1972年，Cook 之后一年，Richard Karp 证明了二十一个著名问题是 NP 完全的。<bookmark mark='a'/>这是他的家谱。根是可满足性；由它出发，整数规划、团"
        "和三-SAT。由团出发，集合打包和顶点覆盖；由顶点覆盖出发，集合覆盖、反馈集和哈密顿回路问题。由三-SAT 出发，色数，然后是精确覆盖，再由此到 "
        "Steiner 树、三维匹配、背包、划分和最大割。<bookmark mark='b'/>Michael Garey 和 David Johnson 1979年的目录列出了三百多个，如今已有数千个。"
        "<bookmark mark='c'/>每一个都靠一个归约加入这个家族，它们同生共死：其中任何一个有了快速算法，就能解决全部。",
    # ------------------------------------------------------------------ Everywhere
    "Chapter seven. NP-completeness everywhere.": "第7章。无处不在的 NP 完全性。",
    "NP-completeness turns up in unexpected places.":
        "NP 完全性出现在意想不到的地方。<bookmark mark='a'/>2003年，Erik Demaine、Susan Hohenberger 和 David Liben-Nowell 证明了俄罗斯方块是 NP "
        "完全的：预先知道每一块，你能清空棋盘吗？<bookmark mark='b'/>Richard Kaye 在2000年证明，判定一个扫雷局面是否自洽是 NP 完全的。<bookmark "
        "mark='c'/>n 平方格的数独是 NP 完全的，出自 Takayuki Yato 和 Takahiro Seta。<bookmark mark='d'/>在最简单的格点模型中，找蛋白质能量最低的折叠"
        "方式也是。<bookmark mark='e'/>每一个都属于 NP，因为解很容易检查。每一个都是 NP 完全的，因为有人用下落的方块、地雷或格子造出了模拟公式的小部件。"
        "<bookmark mark='f'/>两人对弈、能下很久的游戏更难，第10章会说明。",
    "Engineers meet NP-hard problems every week.":
        "工程师每周都会遇到 NP 难问题。<bookmark mark='a'/>排考试、排班、把作业排到机器上。<bookmark mark='b'/>把物品装进箱子、集装箱，或者把虚拟机"
        "放到服务器上。<bookmark mark='c'/>甚至安装软件：判定一组带版本约束的软件包能否一起安装是 NP 完全的，研究 Debian 的学者在2006年证明了这一点。"
        "<bookmark mark='d'/>这就是为什么现代包管理器用类 SAT 的求解器解析依赖；第41部分会造一个。<bookmark mark='e'/>第13部分的寄存器分配就是图着色。"
        "<bookmark mark='f'/>NP 完全性是关于最坏情况的论断。实践中出现的实例往往很容易。<bookmark mark='g'/>应对之道：输入小或有结构时用精确求解器；"
        "用有保证的近似算法；或者用一个结果可以界定的启发式。",
    # ------------------------------------------------------------------ Numbers
    "Chapter eight. Strong and weak hardness.": "第8章。强难与弱难。",
    "Subset sum is NP-complete, yet Part 19 solved it with dynamic programming.":
        "子集和是 NP 完全的，可第19部分用动态规划解决了它。这矛盾吗？<bookmark mark='a'/>动态规划标出直到目标 W 的每个可达和，所以时间正比于 n 乘 W。"
        "<bookmark mark='b'/>但 W 是一个数，输入里只有它的各位数字。每多一位，W 和运行时间就乘以十：三十个六位数，比三十个四位数慢一百倍。<bookmark "
        "mark='c'/>这样的算法叫作伪多项式的。它对数的大小是多项式的，对输入的长度却不是。<bookmark mark='d'/>如果是十二位数，表格会有一万亿项。第24部分的"
        "折半相遇不在乎位数，这里用五十毫秒，但它对元素个数是指数的。",
    "This splits NP-hard problems in two.":
        "这把 NP 难问题分成了两类。<bookmark mark='a'/>有些是弱 NP 难的：只因为数可以大得天文才难。背包、子集和与划分。<bookmark mark='b'/>另一些是强 "
        "NP 难的：即使每个数都很小、用一进制写出来，也难。三划分、装箱、旅行商。<bookmark mark='c'/>Michael Garey 和 David Johnson 在1978年划下了这条线。"
        "<bookmark mark='d'/>弱难有一条出路：把数舍入成更少的位数。<bookmark mark='e'/>Oscar Ibarra 和 Chul Kim 在1975年对背包这样做了：在 n 和 epsilon "
        "分之一的多项式时间内，得到最优值的一减 epsilon 倍以内的解。<bookmark mark='f'/>除非 P 等于 NP，强 NP 难问题不可能有这样的方案。<bookmark "
        "mark='g'/>所以知道一个问题是 NP 难的，只是分析的开始：哪一类，能接近到什么程度，真实的输入有多大？",
    # ------------------------------------------------------------------ CoNp
    "Chapter nine. coNP and the polynomial hierarchy.": "第9章。coNP 与多项式层级。",
    "NP is lopsided: a yes comes with a short proof, a no need not.":
        "NP 是不对称的：“是”带着短证明，“否”却不一定。<bookmark mark='a'/>翻过来就是 coNP：“否”有短证明的问题。一个公式是重言式吗，即在每个赋值下都为真？"
        "“否”很容易证明：给出一个使它为假的赋值。“是”似乎要检查全部二的 n 次方行。<bookmark mark='b'/>NP 是否等于 coNP 尚未解决。如果 P 等于 NP，它们就"
        "相等，所以这是第二个、较弱的问题。<bookmark mark='c'/>在交集里，是两种答案都有证明的问题。分解因数是最著名的一个。<bookmark mark='d'/>如果有任何 "
        "NP 完全问题属于 coNP，两个类就会重合。这正是专家们怀疑分解因数不是 NP 完全的主要原因，尽管谁也不能快速分解。",
    "Why is factoring in both?":
        "为什么分解因数两边都在？<bookmark mark='a'/>问一个数 N 是否有不超过 k 的因子。<bookmark mark='b'/>无论哪种答案，证书都是完整的因数分解，加上每个"
        "因子是素数的证明。给定素因子，任何人都能检查乘积，并对每个 k 读出答案，是或否。<bookmark mark='c'/>可怎样简短地证明一个数是素数？Vaughan Pratt "
        "在1975年给出了方法。p 是素数，恰好当某个 g 的乘法阶是 p 减一，而这可以用 p 减一的素因子来检查，每个素因子再带着自己的证书。<bookmark mark='d'/>"
        "这是梅森素数二的六十一次方减一的证书：总共六十次检查，每次一个模幂。<bookmark mark='e'/>自2002年起，我们知道素性判定本身就属于 P。这种证书仍然"
        "是 NP 与 coNP 之交含义的最清晰图景。",
    "Alternate the quantifiers and you climb a ladder.":
        "交替使用量词，你就登上了一架梯子。<bookmark mark='a'/>底部是 P。NP 问是否存在一个短证书；coNP 问是否每个候选都失败。<bookmark mark='b'/>"
        "再上一层：是否存在一个规模为 k 的电路，使得对每个输入它都和这个电路一致？这是一个先存在后全称的问题，sigma 二。<bookmark mark='c'/>这就是第25部分"
        "的算术层级，只是每个量词都限制在多项式长度，由 Albert Meyer 和 Larry Stockmeyer 在1972年定义。<bookmark mark='d'/>如果 P 等于 NP，整架梯子就会"
        "塌缩到 P。更一般地，只要任意两个相邻层相等，它们之上的一切也都塌下来。<bookmark mark='e'/>所以“层级是无限的”是一个标准的赌注，比 P 不等于 NP "
        "稍强，许多定理，比如 Karp 和 Lipton 的定理，都是相对于它来陈述的。",
    # ------------------------------------------------------------------ Space
    "Chapter ten. Space: games and alternation.": "第10章。空间：博弈与交替。",
    "Polynomial space has its own complete problem.":
        "多项式空间有它自己的完全问题。<bookmark mark='a'/>取一个前面带着交替量词的公式：存在 x 一，对所有 x 二，存在 x 三，如此等等。整个式子为真吗？"
        "<bookmark mark='b'/>用递归求值：对第一个变量试两个值，再对每个值求剩下部分。<bookmark mark='c'/>递归只需要一个赋值和一个栈，所以空间是多项式的。"
        "<bookmark mark='d'/>时间可能是指数的，不过在我们的随机公式上，早早得出的答案剪掉了树的大部分。<bookmark mark='e'/>Larry Stockmeyer 和 Albert "
        "Meyer 在1973年证明，这个问题对多项式空间是完全的。<bookmark mark='f'/>可满足性是只有存在量词的特例。",
    "Alternating quantifiers are a game.":
        "交替的量词就是一场博弈。<bookmark mark='a'/>存在我的一步，使得对每个回应，存在我的一步，如此下去。广义地理游戏把这一点变得字面化：两人轮流沿箭头"
        "把棋子移到一个还没访问过的顶点，不能移动的人输。<bookmark mark='b'/>在这个图上，把棋子放到顶点零的人有必胜策略；我们的搜索看了十一个局面就证明了"
        "这一点。<bookmark mark='c'/>Thomas Schaefer 在1978年证明，任何量化公式都能变成一个地理游戏图，所以判定谁赢是 PSPACE 完全的。",
    "Real board games, generalized to n by n boards, sit here too.":
        "真实的棋类游戏，推广到 n 乘 n 的棋盘，也在这里。<bookmark mark='a'/>判定 Hex 一个局面谁赢是 PSPACE 完全的。不考虑劫争的围棋是 PSPACE 难的，"
        "出自 David Lichtenstein 和 Michael Sipser。采用日本劫规则，对局可以持续指数长，围棋就成为指数时间完全的，国际象棋和跳棋也是。<bookmark "
        "mark='b'/>多项式长度的游戏在多项式空间里；可能持续指数长的游戏到达指数时间。<bookmark mark='c'/>而指数时间完全意味着可证明地不在 P 中，由第2章的"
        "层级定理。<bookmark mark='d'/>广义国际象棋是少数几个我们能证明没有多项式算法的自然问题之一。",
    "Space also matters at the bottom.":
        "空间在底层也很重要。<bookmark mark='a'/>对数空间允许一个只读的输入，加上一把计数器和指针。<bookmark mark='b'/>它的非确定版本 NL 有一个自然的完全"
        "问题：有向图中是否有从 s 到 t 的路径？<bookmark mark='c'/>1987年和1988年，Róbert Szelepcsényi 和 Neil Immerman 独立证明了一个惊喜：NL 在补运算"
        "下封闭。诀窍是一层一层地数出可达的顶点，非确定地、但可验证地。所以对于空间，和我们对时间的预期不同，猜出一个“否”和猜出一个“是”一样容易。"
        "<bookmark mark='d'/>2005年，Omer Reingold 证明了无向图中的可达性根本不需要猜测。<bookmark mark='e'/>对数空间是否等于多项式时间，和 P 与 NP 一样悬而"
        "未决。",
    # ------------------------------------------------------------------ Sqrt
    "Chapter eleven. Time in square-root space.": "第11章。平方根空间里的时间。",
    "Every computation of t steps uses at most t cells of memory.":
        "每个 t 步的计算至多用 t 个存储格子。它总能用更少的吗？<bookmark mark='a'/>把计算画成网格：时间向下，纸带横向，切成 b 步、b 个格子的块。<bookmark "
        "mark='b'/>一个块最后的内容只取决于它上方的块和左右邻居。<bookmark mark='c'/>1977年，John Hopcroft、Wolfgang Paul 和 Leslie Valiant 利用这种结构，"
        "用大约 t 除以 log t 的空间模拟 t 步。<bookmark mark='d'/>将近五十年里没人改进它，许多人相信不可能好太多。<bookmark mark='e'/>2025年2月，Ryan "
        "Williams 证明了 t 步可以用大约 t 乘 log t 的平方根那么多的空间模拟。",
    "Williams's proof rests on a problem called tree evaluation.":
        "Williams 的证明依赖于一个叫作树求值的问题。<bookmark mark='a'/>树的叶子存着值；每个内部节点对孩子的值施加一个函数；求出根。<bookmark mark='b'/>"
        "显而易见的方法是每层保留一个值，<bookmark mark='c'/>人们曾猜想这本质上是最优的；证明它就能把对数空间和多项式时间分开。<bookmark mark='d'/>2024年，"
        "James Cook 和 Ian Mertz 推翻了这个猜想。他们的算法把计算写进已经装满其他数据的存储里，先加后减，于是同样的比特同时为许多目的服务。<bookmark "
        "mark='e'/>Williams 的一步是看出：任何计算的块结构都可以排成一个树求值实例，于是 Cook-Mertz 算法就能用上。",
    "How big a difference is it?":
        "差别有多大？<bookmark mark='a'/>对一万亿步，1977年的界允许约两百五十亿个格子；新的界约六百万个。<bookmark mark='b'/>它有一个惊人的推论。如果线性"
        "空间的问题总能在远少于平方的时间内解决，这个模拟就会与空间层级定理矛盾。所以有些能装进线性空间的问题，在多带机器上需要几乎平方的时间。"
        "<bookmark mark='c'/>这是朝着分离 P 与 PSPACE 迈出的一小步，离目标仍然很远。但它提醒我们未知有多少：一个五十年的界，倒在一个关于重用存储的新想法"
        "之下。",
    # ------------------------------------------------------------------ Ladner
    "Chapter twelve. Between P and NP-complete.": "第12章。介于 P 与 NP 完全之间。",
    "Suppose P is not NP.":
        "假设 P 不等于 NP。NP 中的每个问题是否非易即完全？<bookmark mark='a'/>不是。Richard Ladner 在1975年证明，如果 P 不同于 NP，NP 中就有既不在 P 中、"
        "也不是 NP 完全的问题。<bookmark mark='b'/>证明拿来 SAT，在上面打洞：对某些输入长度保留公式，对另一些把它们填充成平凡的。<bookmark mark='c'/>"
        "这些长度由一个缓慢的对角化过程选定。洞太多问题就会变容易，洞太少它仍然是完全的，<bookmark mark='d'/>构造在两者之间穿行，轮流挫败每个多项式算法和"
        "每个多项式归约。<bookmark mark='e'/>它造出的问题是人造的。真正的问题是，哪些自然问题住在中间。",
    "A few natural problems are suspected to be intermediate.":
        "有几个自然问题被怀疑是中间的。<bookmark mark='a'/>分解因数与离散对数：两者都在 NP 与 coNP 之交，而第30部分里 RSA 与 Diffie-Hellman 的安全性就"
        "建立在它们困难之上。<bookmark mark='b'/>图同构，现已知是拟多项式的；除非多项式层级塌缩，它不可能是 NP 完全的。<bookmark mark='c'/>还有最小电路规模"
        "问题，第16章会再谈。<bookmark mark='d'/>这些都没有被证明是中间的。任何一个都可能落进 P。<bookmark mark='e'/>与此同时，对一些很大的自然问题族，"
        "存在二分。Andrei Bulatov 和 Dmitriy Zhuk 在2017年独立证明，有限域上的每个约束满足问题要么在 P 中，要么是 NP 完全的，中间什么都没有。",
    # ------------------------------------------------------------------ Sat
    "Chapter thirteen. SAT in practice.": "第13章。实践中的 SAT。",
    "Satisfiability is NP-complete, yet industrial solvers handle":
        "可满足性是 NP 完全的，可工业级求解器能处理有数百万变量的公式。我们的求解器是这样工作的。<bookmark mark='a'/>决策：挑一个变量，优先选最近冲突里"
        "出现过的，给它一个值。<bookmark mark='b'/>传播：任何除一个文字外都为假的子句，强制最后那个文字为真；每个子句只盯住两个文字，让这一步很便宜。"
        "<bookmark mark='c'/>迟早某个子句会变成假。沿蕴涵链往回追，找出是哪些决策导致了它。<bookmark mark='d'/>学习一个新子句，永远排除那种组合。"
        "<bookmark mark='e'/>然后回跳，不是退一层，而是跳到新子句第一次起作用的那一层，再继续。<bookmark mark='f'/>再加上重启，就是这一部分一直在用的"
        "求解器，大约两百行 Python。<bookmark mark='g'/>在困难的随机公式上，与1962年的旧 DPLL 过程相比，随着 n 增大，它需要的步数更少，时间少得多。",
    "Where are the hard instances?":
        "难的实例在哪里？<bookmark mark='a'/>生成有 n 个变量、m 个子句的随机三-SAT 公式，改变两者的比值。子句少时，公式几乎总是可满足的，求解器立刻找到"
        "赋值。子句多时，几乎总是不可满足的，矛盾来得很快。<bookmark mark='b'/>在两者之间，每个变量约四点二七个子句处，可满足的概率跌过二分之一，求解器的"
        "工作量达到峰值：一百五十个变量时两千多次冲突，而两端只有寥寥几次。<bookmark mark='c'/>随着 n 增大，下降变得更陡：Ehud Friedgut 在1999年证明了"
        "阈值是尖锐的。它的确切位置由 Jian Ding、Allan Sly 和 Nike Sun 在2015年证明，但只针对长子句。对三-SAT，预测值约四点二七仍然是一个猜想。",
    "Solvers now settle questions in mathematics.":
        "求解器如今能解决数学问题。<bookmark mark='a'/>把从一到 n 的数涂色，使得同一种颜色里不含 x、y 和 x 加 y。三种颜色能到十三，到不了十四；我们的求解器"
        "瞬间否定了十四。四种颜色是四十四，这是我们求解器的涂法。<bookmark mark='b'/>五种颜色的答案是一百六十，由 Marijn Heule 在2017年用一个两拍字节的"
        "证明给出。<bookmark mark='c'/>或者用两种颜色给数涂色，使得没有毕达哥拉斯三元组同色。我们的求解器轻松涂好了前三千个。<bookmark mark='d'/>Heule、"
        "Oliver Kullmann 和 Victor Marek 在2016年证明，最多能做到七千八百二十四，再多一个都不行。他们的证明有两百太字节。<bookmark mark='e'/>没人读这样的"
        "证明。它们由一些自身正确性已被验证的小程序检查，所以我们信任的是检查器，而不是求解器。",
    # ------------------------------------------------------------------ Barriers
    "Chapter fourteen. Why it is hard.": "第14章。为什么它难。",
    "There are precise reasons the problem is hard":
        "这个问题难，有精确的理由：一些关于“哪些证明行不通”的定理。<bookmark mark='a'/>1975年，Theodore Baker、John Gill 和 Robert Solovay 给每台机器"
        "配上一个谕示。用一个谕示，即一个 PSPACE 完全问题，P 和 NP 变得相等。<bookmark mark='b'/>用另一个由对角化构造的谕示，它们可证明地不同。<bookmark "
        "mark='c'/>对角化和模拟，即第1部分和第2章的工具，在加上谕示后照样成立：它们可以相对化。<bookmark mark='d'/>所以只用它们构造的证明，会对两个谕示给出"
        "同样的结论，而这不可能。<bookmark mark='e'/>这就是为什么层级定理能把 P 和指数时间分开，却碰不到 NP。",
    "The next attack counted gates instead of steps.":
        "下一次进攻数的是门而不是步。<bookmark mark='a'/>如果 SAT 需要超多项式规模的电路，P 就不同于 NP。<bookmark mark='b'/>1980年代取得了真正的成功。"
        "奇偶函数无法用常数深度电路计算，Alexander Razborov 还对不含非门的电路证明了很大的下界。<bookmark mark='c'/>每个这样的证明都找出一个简单、可检查的"
        "性质，随机函数具有它，而小电路没有。<bookmark mark='d'/>1994年，Razborov 和 Steven Rudich 证明，任何这样的性质都能用来区分真正的随机函数和伪随机"
        "函数。<bookmark mark='e'/>所以如果强伪随机函数存在，而这正是第29部分的密码学所假设的，就没有自然证明能证明 P 不同于 NP。<bookmark mark='f'/>我们的"
        "密码学越好，就越难证明它所依赖的困难性。",
    "There is a third barrier.":
        "还有第三道壁垒。<bookmark mark='a'/>1990年代，算术化，即把公式变成多项式，给出了一些不能相对化的结果，比如第27部分要证明的 IP 等于 PSPACE。"
        "<bookmark mark='b'/>2008年，Scott Aaronson 和 Avi Wigderson 证明，这些技术满足一种推广的相对化，他们称之为代数化，而能代数化的证明同样解决不了 P "
        "与 NP。<bookmark mark='c'/>一个证明必须同时绕开这三道壁垒。<bookmark mark='d'/>有少数结果做到了。Ryan Williams 在2011年证明，非确定指数时间不包含"
        "于一类叫作 ACC 零的小电路之中，办法是证明：对这类电路的可满足性有更快的算法，就意味着针对它们的下界。<bookmark mark='e'/>第16章会回到这条路通向哪里。",
    # ------------------------------------------------------------------ Worlds
    "Chapter fifteen. Five possible worlds.": "第15章。五个可能的世界。",
    "In 1995 Russell Impagliazzo described five worlds":
        "1995年，Russell Impagliazzo 描述了五个世界，它们与我们所知的一切都相容，区别在于什么是难的。<bookmark mark='a'/>在算法国，P 等于 NP，或者差不多："
        "每个搜索问题都容易。<bookmark mark='b'/>在启发国，NP 在最坏情况下难，但任何人实际能生成的实例都容易。<bookmark mark='c'/>在悲观国，平均意义下存在"
        "难问题，却没有单向函数：两头都最糟，有难题却连保密都用不上。<bookmark mark='d'/>在迷你密码国，单向函数存在，足以做签名和私钥加密。<bookmark "
        "mark='e'/>在密码狂国，公钥密码存在，这是我们建造互联网所依托的世界，也是第30部分所假设的。<bookmark mark='f'/>我们不知道自己生活在哪个世界。每一个"
        "都与迄今证明的每个定理相容。",
    "What would P equals NP really mean?":
        "P 等于 NP 究竟意味着什么？<bookmark mark='a'/>Gödel 最先看到：任何有合理长度证明的定理都能由机器找到。<bookmark mark='b'/>排程、路径规划、蛋白质"
        "设计和芯片布局都能精确求解。<bookmark mark='c'/>学习会变得容易：找出与数据相符的最小模型。<bookmark mark='d'/>而几乎全部密码学都会崩溃，因为破解"
        "它是一个答案可检查的搜索问题。<bookmark mark='e'/>有一个前提。指数为一千的多项式，或者不给出算法的证明，在实践中改变不了多少。<bookmark mark='f'/>"
        "大多数研究者预期的是相反的答案：在 William Gasarch 2019年的调查中，百分之八十八的受访者，以及百分之九十九的专家，相信 P 不等于 NP。<bookmark "
        "mark='g'/>它是克雷数学研究所七个千禧年大奖难题之一，解决者可得一百万美元。",
    "Could P versus NP be one of Part 25's unprovable statements?":
        "P 与 NP 会不会是第25部分里那种不可证的命题？<bookmark mark='a'/>正如我们看到的，有些关于程序的真命题在集合论中没有证明。<bookmark mark='b'/>P "
        "不等于 NP 说的是：对每台机器和每个指数，都有某个输入击败它：一个带两个量词的命题，恰好是那种可能逃脱证明的类型。<bookmark mark='c'/>Juris Hartmanis "
        "和 John Hopcroft 在1976年证明，相对于某些谕示，这个问题确实独立于集合论。<bookmark mark='d'/>对不带谕示的问题，没有这样的证据，大多数研究者预期它"
        "终有一天会被一个普通的证明解决。<bookmark mark='e'/>Scott Aaronson 2016年的综述强调了一个讽刺：我们最强的下界，比如 Williams 的，都来自发现新算法。"
        "要证明某件事难，也许得先弄清什么是容易的。",
    # ------------------------------------------------------------------ Frontier
    "Chapter sixteen, the frontier. Complexity about complexity.": "第16章，前沿。关于复杂性的复杂性。",
    "The frontier asks about the complexity of complexity itself.":
        "前沿问的是复杂性本身的复杂性。<bookmark mark='a'/>我们精确算出了三输入的全部二百五十六个布尔函数各自最小的与或公式。<bookmark mark='b'/>多数函数"
        "需要五片叶子。奇偶函数需要十片，比其他任何函数都多。<bookmark mark='c'/>Valeriy Khrapchenko 在1971年证明，n 位奇偶函数需要 n 的平方，这里是九；"
        "实际是十。<bookmark mark='d'/>Claude Shannon 在1949年用计数证明，几乎每个 n 输入函数都需要指数规模的电路。<bookmark mark='e'/>然而，对 NP 中任何"
        "一个具体的函数，没人能证明超过约三点一乘 n 个门的下界，那是 Jiatu Li 和 Tianqi Yang 2022年的纪录。难的函数遍地都是，我们却指不出一个。",
    "Here is how far lower bounds have come.":
        "下界走到了这里。<bookmark mark='a'/>一般电路：三点一 n。公式：约 n 的三次方，出自 Johan Håstad 和 Avishay Tal。常数深度电路：奇偶函数有指数下界。"
        "对 ACC 零这个类，Williams 的算法方法现在把它和非确定拟多项式时间分开了。而 P 与 NP 需要的，是 SAT 对一般电路的超多项式下界，远远超出这一切。"
        "<bookmark mark='b'/>另一个纲领，几何复杂性理论，由 Ketan Mulmuley 和 Milind Sohoni 提出，用表示论去攻这个问题的代数版本。<bookmark mark='c'/>它最"
        "简单的形式在2016年被排除了，这个纲领正在用更精细的工具继续。",
    "The newest frontier is called meta-complexity":
        "最新的前沿叫作元复杂性：衡量某件事有多难，本身有多难？<bookmark mark='a'/>最小电路规模问题问：给定一个函数的完整真值表和一个数 s，是否有某个规模"
        "为 s 的电路计算它。<bookmark mark='b'/>它属于 NP，因为电路就是证书；在 P 和 NP 有名字之前，苏联研究者就把它当作一个蛮力搜索问题来研究，称之为 "
        "perebor。<bookmark mark='c'/>它是 NP 完全的吗？没人知道。2022年，Shuichi Hirahara 证明了一个偏函数版本是。<bookmark mark='d'/>而在2020年，"
        "Yanyi Liu 和 Rafael Pass 证明：单向函数存在，当且仅当某种限时版本的 Kolmogorov 复杂度在平均意义下是难的。<bookmark mark='e'/>所以密码学是否可能，"
        "是一个关于压缩字符串的问题，即带时钟的第25部分 Kolmogorov 复杂度。<bookmark mark='f'/>这些结果也许有一天会把上一章的那些世界连起来。它们是这个领域"
        "最活跃的研究之一。",
    "Six open problems.":
        "六个未解问题。<bookmark mark='a'/>P 与 NP 本身，以及它的表亲：NP 与 coNP，P 与 PSPACE，对数空间与 P。<bookmark mark='b'/>最小电路规模问题是否 "
        "NP 完全。<bookmark mark='c'/>分解因数或图同构是否属于 P。<bookmark mark='d'/>三-SAT 阈值的确切位置。<bookmark mark='e'/>Williams 的模拟还能推进多远。"
        "<bookmark mark='f'/>以及对任何具体函数的超线性电路规模下界。<bookmark mark='g'/>这一部分的研究问题取第四个的一个小的、可计算的情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们造了什么。多项式时间，以及它为何稳健。时间层级与 Savitch 定理，都给出了证明。作为可检查证书的 NP，以及 Cook 和 Levin 的表格，建成公式并"
        "求解。到独立集、团、覆盖、三着色和子集和的归约，每个都在真实公式上运行并映射回来。coNP、Pratt 证书和多项式层级；博弈、多项式空间，以及平方根空间里的"
        "时间。一个子句学习的 SAT 求解器和相变。还有壁垒、五个世界和元复杂性。",
    "Where this comes back.":
        "这些会在哪里再出现。第27部分给证明加上随机性和交互，抵达 PCP 定理。第29部分在单向函数上建立密码学，即 Impagliazzo 的迷你密码国；第30部分在分解"
        "因数和离散对数上建立公钥，即第12章的嫌疑对象。第41部分用 SAT 求解器解析软件包依赖。第53部分问量子计算机是否打破扩展的 Church-Turing 论题。而第54"
        "部分通过把验证条件交给像我们这样的求解器来证明程序正确。",
    "In practice.":
        "在实践中。学会在工作中识别 NP 难问题：排程、装箱、配置和依赖解析。然后照样去解，用 SAT、SMT 和整数规划求解器，它们每天都在处理工业实例。或者用第23"
        "部分有保证的方法去近似。硬件和软件验证都运行在 SAT 求解器上。而每一种密码都是对某个难题的押注；知道是哪一个，大有好处。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在这一部分的笔记里。随时暂停。第五道是动手题：把数独变成 SAT，用这一部分的求解器求解。最后一道标着星号，是研究问题：它的答案未知，"
        "笔记里说明了从哪里入手。",
    "Next time: proofs that use randomness.":
        "下一次：使用随机性的证明。证明者可以让你相信一个命题为真，却不告诉你为什么。交互让证明的能力指数级增强。而一个证明可以写成这样：随机读它的三个比特，"
        "就足以抓住任何错误，这就是为什么有些问题连近似都难。第27部分，证明与随机性。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
