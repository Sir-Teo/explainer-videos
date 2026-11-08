"""Chinese narration for cs59: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第59部分：分布式计算理论"

CHAPTERS = {
    "Hook": "n 个进程能计算什么",
    "Models": "1. 模型与故障",
    "Local": "2. 局部性：给环着色",
    "Linial": "3. Linial 的下界",
    "Sync": "4. 同步系统中的一致及其界",
    "Async": "5. 异步：FLP 与随机性",
    "Shared": "6. 共享内存与共识层级",
    "Topology": "7. 拓扑：为什么 k 集合一致不可能",
    "Detectors": "8. 故障检测器",
    "Communication": "9. 一致的代价",
    "Population": "10. 种群协议",
    "Frontier": "11. 前沿：局部性的复杂性",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "A million processes stand in a ring, each knowing only its":
        "一百万个进程站成一个环，每个进程只知道自己的标识符和它后继的标识符。它们必须用三种颜色给自己着色，使任何两个邻居的颜色都不相同。<bookmark mark='a'/>一开始，每个标识符就是它自己的颜色：一百万种颜色。"
        "<bookmark mark='b'/>每一轮，每个进程把自己的颜色和后继的颜色相比较，找出它们第一个不同的比特，然后把这个比特的位置和取值作为自己的新颜色。邻居之间仍然各不相同，"
        "而一个 b 比特的颜色会缩短到大约 log b 比特。<bookmark mark='c'/>一百万种颜色变成38种，然后是12种、8种、6种，再过3轮，就去掉了大于2的颜色。"
        "<bookmark mark='d'/>一百万个进程用7轮，换成十亿个也只多一点点：这个轮数就是到达1之前要取多少次对数，记作 log star，也就是迭代对数。",
    "This part asks three questions. <bookmark mark='a'/> What":
        "这一部分提出三个问题。<bookmark mark='a'/>当每个进程只能看到几跳之内的东西时，什么能被局部地计算？Nathan Linial 在1992年证明，我们的7轮本质上已经是最好的了："
        "没有任何算法能在少于大约 n 的迭代对数轮内给一个环三着色。<bookmark mark='b'/>当进程会出故障时，什么能达成一致？如果三个进程中有一个撒谎，它们就无法达成一致；f 次崩溃需要 f 加一轮；"
        "而如果根本没有时钟，第38部分的 FLP 定理就排除了一致的可能。<bookmark mark='c'/>还有，究竟什么能被计算？有些任务是不可能的，而原因后来证明是拓扑上的。"
        "<bookmark mark='d'/>第38部分搭建了 Raft。这一部分是它底下的理论。",
    "This is Part 59 of Computer Science, Built. <bookmark":
        "这是《计算机科学，从零搭建》的第59部分。<bookmark mark='a'/>我们会先确定模型；用迭代对数轮给环着色，并证明没有人能做得更好；证明面对崩溃和撒谎者时一致的极限；用随机性战胜不可能性；"
        "攀登共享对象的共识层级；见识 k 集合一致不可能性的拓扑证明；最后讲故障检测器、一致的代价，以及为化学计算机设计的协议。",
    # ------------------------------------------------------------------ s02_models
    "Chapter one. Models and faults.":
        "第一章。模型与故障。",
    "A model fixes three things: how time behaves, how processes":
        "一个模型确定三件事：时间如何表现，进程如何交谈，以及它们可能怎样出故障。先说时间。<bookmark mark='a'/>在同步系统里，进程按步调一致的轮前进。每一轮，每个进程发出它的消息，每条消息都在这一轮结束前到达，"
        "然后每个进程进行计算。所以，如果一条预期的消息没有到达，它的发送者肯定已经出了故障。<bookmark mark='b'/>在异步系统里，一条消息要走多久、一个进程跑得多快，都没有上界。"
        "<bookmark mark='c'/>一条还没到的消息可能仍在路上，所以没有哪个进程能把一个慢的邻居和一个死掉的邻居区分开，这正是第38部分 FLP 定理的根源。"
        "<bookmark mark='d'/>真实的网络介于两者之间：Dwork、林奇（Lynch）和 Stockmeyer 提出的部分同步，其中的上界只是最终成立，而 Raft 就生活在这里。",
    "Next, how processes talk. <bookmark mark='a'/> In message":
        "接下来，进程如何交谈。<bookmark mark='a'/>在消息传递中，进程是网络的节点，只能沿着网络的链路发送消息来通信，而消息可能被延迟、重排或丢失。<bookmark mark='b'/>在共享内存中，"
        "进程从不发送任何东西：它们读写共享的寄存器，或者使用更强的对象，比如第33部分的比较并交换，而第六章会按能力给这些对象排序。<bookmark mark='c'/>这两个世界比看上去更接近。Hagit Attiya、"
        "Amotz Bar-Noy 和 Danny Dolev 在1995年证明，只要多数进程是正确的，消息就能模拟一个共享寄存器，所以为一个模型写的算法常常也能在另一个模型里运行。",
    "Third, how processes fail. <bookmark mark='a'/> A crashed":
        "第三，进程如何出故障。<bookmark mark='a'/>一个崩溃的进程就是停下来，可能停在发送一轮消息的半途，而且再也不回来。<bookmark mark='b'/>遗漏故障更微妙：进程还在运行，"
        "但它的一些消息从未发出，或者从未被收到。<bookmark mark='c'/>而一个拜占庭进程可以做任何事，包括对不同的进程说不同的话。这个名字来自莱斯利·兰波特（Leslie Lamport）、"
        "Robert Shostak 和 Marshall Pease 1982年关于拜占庭将军的论文。<bookmark mark='d'/>每一种都包含前一种，所以能扛住撒谎者的算法，也能扛住崩溃。"
        "<bookmark mark='e'/>这一部分的每个界，都是针对 n 个进程、其中至多 f 个有故障来陈述的，而故障越难对付，代价就越高。",
    "The problem at the centre of the theory is consensus.":
        "这个理论的中心问题是共识。<bookmark mark='a'/>每个进程从一个输入开始，这里是一个比特，并且必须决定一个输出。<bookmark mark='b'/>三条规则：一致性，没有两个正确的进程做出不同的决定；"
        "有效性，如果所有输入都是同一个值，那么决定就是这个值；终止性，每个正确的进程最终都会做出决定。没有有效性的话，总是决定零就行了。<bookmark mark='c'/>这是这一部分将要证明的地图。在同步轮和崩溃之下，"
        "能容忍任意多个故障，代价是 f 加一轮。拜占庭故障需要多于三 f 个进程，除非消息带有签名。<bookmark mark='d'/>没有同步，就没有任何确定性算法能扛住哪怕一次崩溃，但硬币能救我们；而在共享内存中，"
        "答案取决于给了你哪些对象。",
    "One more pair of models measures something else: not fault":
        "还有一对模型衡量的是别的东西：不是容错，而是距离。<bookmark mark='a'/>在 LOCAL 模型中，网络本身就是输入。没有故障，每个节点都有唯一的标识符，在每个同步轮里，"
        "每个节点都可以给每个邻居发送任意大小的消息。唯一的代价是轮数。<bookmark mark='b'/>每一轮，信息移动一跳。<bookmark mark='c'/>CONGEST 模型也一样，"
        "只是一条消息只能携带大约 log n 个比特，也就是几个标识符，所以带宽也很重要。<bookmark mark='d'/>在 LOCAL 中，每个问题都能在与网络直径一样多的轮数内解决：收集整个图，然后计算。"
        "有趣的问题是，在少得多的轮数内能做到什么，而接下来两章就针对给环着色回答这个问题。David Peleg 2000年的书确定了这些名字。",
    # ------------------------------------------------------------------ s03_local
    "Chapter two. Locality: colouring a ring.":
        "第二章。局部性：给环着色。",
    "The LOCAL model turns distance into time. <bookmark":
        "LOCAL 模型把距离变成时间。<bookmark mark='a'/>把16个节点放在一个有向环上，每个节点都知道哪个邻居是它的后继，然后盯住一个节点 v。<bookmark mark='b'/>每一轮，"
        "每个节点把它知道的一切告诉两个邻居。一轮之后，v 知道一跳之内的标识符；t 轮之后，它知道半径为 t 的整个邻域，此外一无所知。"
        "<bookmark mark='c'/>所以一个 t 轮算法只不过是一个从这种视野到输出的函数，而在环上，一个视野就是排成一行的二 t 加一个标识符。<bookmark mark='d'/>标识符很重要：在一个匿名环上，"
        "每个节点永远看到同样的东西，没有任何确定性算法能给它着色。有了标识符，我们就从一个用 n 种颜色的合法着色出发，并且必须把它缩减到三种。",
    "Here is Richard Cole and Uzi Vishkin's trick of 1986, on":
        "这是 Richard Cole 和 Uzi Vishkin 1986年的技巧，用的是我们运行中的数字。<bookmark mark='a'/>节点 v 的标识符是1999591；它后继的标识符是1664200。"
        "把两者都写成二进制。<bookmark mark='b'/>找出它们不同的最低位：这里是第0位。<bookmark mark='c'/>新颜色是这个位置的两倍，加上 v 自己在那一位上的比特：2乘0，加1，等于1。"
        "<bookmark mark='d'/>每个节点同时这样做，接下来的几轮在新的、更短的颜色上进行；在第3轮，v 在第2位找到第一个不同之处，变成了4。"
        "<bookmark mark='e'/>一个21位的标识符只有21个位置，所以一轮之后，至多剩下42种颜色。",
    "Why can neighbours never collide? <bookmark mark='a'/> Take":
        "为什么邻居永远不会冲突？<bookmark mark='a'/>取 v、它的后继 w，以及 w 的后继。节点 v 通过和 w 比较来选择它的位置，而 w 是和它自己的后继比较的。"
        "<bookmark mark='b'/>假设 v 和 w 得到同样的新颜色。二 i 加一个比特同时决定了位置和比特，所以它们选择了同一个位置 i，并且在那里有相同的比特。"
        "<bookmark mark='c'/>但 v 选 i，恰恰因为在这个位置上它的颜色和 w 的颜色不同，这就矛盾了。<bookmark mark='d'/>不论标识符是什么，新的着色都是合法的，所以这一步可以重复；"
        "而因为每个节点只有一个后继要比较，所有节点可以同时行动。",
    "How quickly do the colours shrink? <bookmark mark='a'/> If":
        "颜色缩减得有多快？<bookmark mark='a'/>如果每种颜色都能用 b 个比特表示，位置 i 至多是 b 减一，所以新颜色，也就是二 i 加一个比特，小于二 b。"
        "<bookmark mark='b'/>把它写出来需要一加 b 的对数个比特：一轮之内，颜色的长度大致塌缩为它自身的对数。<bookmark mark='c'/>在我们的运行里：21位，然后是6位、4位、3位。"
        "这个界允许第一轮之后有42种颜色，而运行实际用了38种；然后是12、8和6，正好等于界。<bookmark mark='d'/>到了3位，这个技巧就不再有帮助了：二 i 加一个比特又一次小于6。"
        "<bookmark mark='e'/>由于每一轮取一次对数，到达6种颜色所需的轮数，大约等于把 n 降到一个常数所需的对数次数。",
    "Now watch it run. <bookmark mark='a'/> Twenty-four":
        "现在看它运行。<bookmark mark='a'/>我们百万节点环上的24个相邻节点，每个都以它21位的标识符开始：一百万种颜色。<bookmark mark='b'/>比特技巧运行一轮，环就降到38种颜色；"
        "然后是12、8、6。<bookmark mark='c'/>然后换另一个步骤接手。颜色为5的节点从不相邻，所以它们可以同时重新着色，每个都取0、1、2中两个邻居都没用的最小那个。然后去掉颜色4，再去掉颜色3。"
        "<bookmark mark='d'/>7轮，而我们的仪器检查了这一百万条边中的每一条：没有两个邻居颜色相同。",
    "The count of rounds has a name. <bookmark mark='a'/> Log":
        "这个轮数有一个名字。<bookmark mark='a'/>n 的迭代对数，是到达1之前要取以2为底的对数的次数：65536变成16、4、2、1；四次对数。<bookmark mark='b'/>它增长得慢得离谱："
        "2的65536次方，远远多于宇宙中的原子数，它的迭代对数是5。<bookmark mark='c'/>Cole 和 Vishkin 的轮数紧跟着它：从10个节点到一百万个，我们的仪器需要 n 的迭代对数再加两三轮。"
        "<bookmark mark='d'/>所以给一个环三着色几乎只要常数时间。更聪明的规则能在常数时间内做到吗？下一章的回答是：不能。",
    # ------------------------------------------------------------------ s04_linial
    "Chapter three. Linial's lower bound.":
        "第三章。Linial 的下界。",
    "Nathan Linial proved in 1987, in a paper published in full":
        "Nathan Linial 在1987年证明了迭代对数是无法打败的，论文的完整版发表于1992年。<bookmark mark='a'/>在一个有向环上，t 轮之后，一个节点知道以它为中心的二 t 加一个标识符，"
        "仅此而已。<bookmark mark='b'/>所以任何 t 轮算法都是一个从这种窗口到颜色的函数 f，而它后继的颜色，就是 f 作用于平移一位之后的同一个窗口。<bookmark mark='c'/>要得到合法着色，"
        "f 必须给每个窗口和它的平移不同的颜色，因为任何一行互不相同的标识符都会出现在某个环上。<bookmark mark='d'/>所以 f 合法地着色了一个以窗口为顶点的图，即邻域图，因此这个图的色数必须至多是三。",
    "The neighbourhood graph is enormous, so the argument studies":
        "邻域图非常庞大，所以论证只研究它的一部分。<bookmark mark='a'/>只保留标识符递增的窗口，并把它们和各自递增的平移连起来；对长度为 k 的窗口，把这个图叫作 B k。"
        "<bookmark mark='b'/>子图需要的颜色永远不会更多，所以对环的一个 t 轮三着色，也就三着色了 B 二 t 加一。<bookmark mark='c'/>现在看最小的情形，长度为一的窗口。"
        "任何两个标识符都构成一个递增对，所以 B 一就是 n 个顶点上的完全图，<bookmark mark='d'/>它需要 n 种颜色。<bookmark mark='e'/>证明从长窗口一路走到短窗口，每次减少一个标识符，"
        "计算颜色最多能增长得多快。",
    "Here is the heart of the proof. <bookmark mark='a'/> If":
        "这就是证明的核心。<bookmark mark='a'/>如果长度为 k 的窗口能用 c 种颜色合法着色，那么长度为 k 减一的窗口就能用二的 c 次方种颜色着色。"
        "<bookmark mark='b'/>给每个短窗口着上一个集合：f 给它所有递增扩展的颜色，每个扩展多加一个标识符 y。<bookmark mark='c'/>假设两个相邻的短窗口得到了同一个集合。第一个集合包含 a，"
        "也就是第一个窗口用 x k 扩展之后的颜色。<bookmark mark='d'/>所以 a 也在第二个集合里：第二个窗口用某个更大的 y 扩展之后，颜色也是 a。"
        "<bookmark mark='e'/>但这两个长窗口在 B k 中是相邻的，而且颜色相同，这是不可能的。所以集合着色是合法的，<bookmark mark='f'/>而它的值是 c 种颜色的子集："
        "至多有二的 c 次方个。",
    "Let us run the lemma on five identifiers. <bookmark":
        "我们在五个标识符上运行这个引理。<bookmark mark='a'/>这些是长度为二的窗口，也就是递增对，a b 和 b c 相连。<bookmark mark='b'/>这里三种颜色就够了；"
        "一种做法是按 a 减一和 b 减一不同的最高位来给 a b 着色。<bookmark mark='c'/>现在给每个标识符一个集合，里面是以它开头的那些对的颜色。1得到全部三种；5不是任何对的开头，得到空集。"
        "<bookmark mark='d'/>五个集合各不相同，所以它们合法地着色了五个顶点上的完全图，正如引理所承诺的：至多允许8个集合，而需要的是5个。",
    "Now apply the lemma again and again. <bookmark mark='a'/> A":
        "现在一次又一次地应用这个引理。<bookmark mark='a'/>一个 t 轮算法三着色长度为二 t 加一的窗口。短一个标识符，至多8种颜色；然后是256种；然后是2的256次方种；如此下去，一直到长度为一的窗口，"
        "它需要 n 种。<bookmark mark='b'/>所以 n 至多是一座由二 t 个2叠成、顶上再放一个3的指数塔。<bookmark mark='c'/>每取一次对数就剥掉一层，"
        "所以 n 的迭代对数至多是二 t 加二，<bookmark mark='d'/>于是 t 至少是 n 的迭代对数的一半，再减一。<bookmark mark='e'/>对我们的百万节点环，迭代对数是5，"
        "所以每个算法至少需要2轮；Cole 和 Vishkin 的算法用了7轮。常数不同，增长方式却一样。",
    "Look at the shape of that proof. <bookmark mark='a'/> A":
        "看看这个证明的形状。<bookmark mark='a'/>一个问题的 t 轮算法，变成了一个派生问题的更快算法，然后再来一次，直到对一个显然没有零轮算法的问题，也必须存在一个零轮算法。"
        "<bookmark mark='b'/>Linial 的引理就是这样的一步，用一个标识符的视野，换来指数级更多的颜色。<bookmark mark='c'/>2019年，Sebastian Brandt 证明，"
        "对一大类在局部看起来像树的图上的问题，派生问题可以机械地计算出来，所以可以用程序来搜索下界：这就是轮消除。<bookmark mark='d'/>Linial 的论文也走了另一个方向，在迭代对数轮内，"
        "用 delta 平方量级的颜色，给任何最大度为 delta 的图着色。<bookmark mark='e'/>第十一章会回到这张地图。",
    # ------------------------------------------------------------------ s05_sync
    "Chapter four. Synchronous agreement and its bounds.":
        "第四章。同步系统中的一致及其界。",
    "With synchronous rounds and crashes, agreement has a simple":
        "有了同步轮，面对崩溃，一致有一个简单的算法。<bookmark mark='a'/>在 FloodSet 中，每个进程保存它见过的值的集合。每一轮它把这个集合发给所有人，并把收到的加进来；f 加一轮之后，"
        "它决定集合中最小的值。<bookmark mark='b'/>四个进程，一次崩溃。在第1轮，进程2，唯一持有零的进程，只给进程3发了消息就崩溃了。<bookmark mark='c'/>在第2轮，进程3把零传了下去，"
        "于是所有人都决定零。<bookmark mark='d'/>为什么行得通？f 加一轮里只有 f 次崩溃，那么必有某一轮没有崩溃。在这个干净的轮里，每个活着的进程都听到了其他所有进程，所以此后它们的集合相等，并且一直相等。"
        "集合相等，最小值就相等。",
    "Is the extra round really needed? <bookmark mark='a'/> Here":
        "多出来的那一轮真的必要吗？<bookmark mark='a'/>看对手如何只用 f 轮击败 FloodSet，这里 f 等于2。只有进程1持有零。在第1轮，它只把零发给进程2，然后崩溃。"
        "<bookmark mark='b'/>在第2轮，进程2只把它传给进程3，然后也崩溃了。<bookmark mark='c'/>进程3决定零；进程4从没听说过它，决定一。"
        "<bookmark mark='d'/>我们的仪器穷举检查了 FloodSet：每一种输入，以及谁崩溃、何时崩溃、谁还能收到它的消息的每一种模式。用 f 轮或更少，它总能找到一个破坏一致性的执行。用 f 加一轮，"
        "每个执行都一致，对四个进程、两次崩溃，一共56848个执行，全部如此。",
    "FloodSet needs f plus one rounds; could a cleverer algorithm":
        "FloodSet 需要 f 加一轮；更聪明的算法能用更少的轮吗？不能，而证明是一条链。<bookmark mark='a'/>假设某个算法总是在 f 轮内做出决定。把执行排成一行，从所有输入都是零的执行开始，"
        "它必须决定零，到所有输入都是一的执行为止。<bookmark mark='b'/>每个执行和下一个的差别如此之小，以至于某个正确的进程在两者中看到的完全一样。"
        "<bookmark mark='c'/>这个进程在两者中做出同样的决定，而一致性把所有人都拖着一起走，<bookmark mark='d'/>所以沿着这条链，决定从不改变：零等于一。"
        "<bookmark mark='e'/>这条链每次改变一个输入，先让那个进程崩溃，并且每次移除一条消息。最后一轮的消息只改变它接收者的视野；更早的消息，要先在下一轮让它的接收者沉默才能移除，代价是再多一次崩溃。"
        "每轮一次崩溃：f 次崩溃覆盖 f 轮，永远覆盖不了 f 加一轮。",
    "Now let processes lie. Pease, Shostak and Lamport proved in":
        "现在让进程撒谎。Pease、Shostak 和兰波特在1980年证明，拜占庭一致需要多于三 f 个进程；最干净的证明来自1986年的费希尔（Fischer）、林奇和 Merritt，是一个六边形。"
        "<bookmark mark='a'/>取任何一个为三个进程 A、B、C 设计、要扛住一个撒谎者的协议。<bookmark mark='b'/>把六个诚实的副本连成一个环，零副本的输入是零，一副本的输入是一，"
        "每个副本都把它在环上的两个邻居当作另外两个进程。<bookmark mark='c'/>任意两个邻居看到的，恰好是它们在一个三进程执行中会看到的，在那个执行里，第三个进程撒谎，对每一方扮演不同的副本。"
        "所以有效性使 A 零和 B 零决定零，使 B 一决定一，而一致性使每一对邻居相同。<bookmark mark='d'/>绕环一周，零等于一。"
        "<bookmark mark='e'/>我们的仪器在这个六边形上运行了一个自然的两轮多数协议，它在必然出错的地方出错：C 零与 A 一不一致，C 一与 A 零不一致。",
    "That bound assumes a liar can claim anything about what":
        "这个界假定撒谎者可以随意声称别人说过什么。第30部分的签名夺走了这种能力。<bookmark mark='a'/>在 Danny Dolev 和 Ray Strong 1983年的协议中，发送者给它的值签名。"
        "一个进程如果在第 r 轮收到一个带有 r 个不同签名的值，并且第一个是发送者的签名，它就接受这个值，加上自己的签名，再转发出去。<bookmark mark='b'/>f 加一轮之后，如果它恰好接受了一个值，"
        "就决定这个值，否则决定一个默认值。<bookmark mark='c'/>为什么正确的进程会一致？一个正确的进程在第 f 轮之前接受的值会被转发，所以一轮之后所有人都会接受它。"
        "一个在最后一轮才第一次被接受的值带有 f 加一个签名，所以其中有一个签名者是正确的，并且更早就转发过它。<bookmark mark='d'/>一个给两个值签名的发送者，会在所有人面前暴露。"
        "<bookmark mark='e'/>它适用于任意多个有故障的进程，用 f 加一轮，也就是最少的轮数。",
    # ------------------------------------------------------------------ s06_async
    "Chapter five. Asynchrony: FLP and randomness.":
        "第五章。异步：FLP 与随机性。",
    "Part 38 told this theorem's story; here is the machinery of":
        "第38部分讲过这个定理的故事；这里是它证明的机制。<bookmark mark='a'/>三个进程，其中任何一个都可能崩溃。把初始格局排成一行，每次改变一个输入。全零必须决定零，全一必须决定一。"
        "<bookmark mark='b'/>假设没有哪个初始格局是二价的。那么在某处，有两个相邻的格局价相反，这里是 C 一和 C 二。<bookmark mark='c'/>它们只在进程2的输入上不同。"
        "<bookmark mark='d'/>让进程2从一开始就崩溃，运行这两个格局。其他进程在两次执行中看到的完全一样，所以它们做出同样的决定。<bookmark mark='e'/>但一个初始格局是零价的，另一个是一价的。"
        "所以某个初始格局是二价的：单凭输入，并不能确定结果。",
    "The second step is the heart. <bookmark mark='a'/> Take a":
        "第二步是核心。<bookmark mark='a'/>取一个二价格局 C，以及任何一个待执行的步骤 e：进程 p 接收消息 m。让对手先走其他任意步骤，然后才执行 e。<bookmark mark='b'/>论断是："
        "其中有些结果仍然是二价的，所以对手可以投递 e，而不让决定发生。<bookmark mark='c'/>假设不是这样，那么每个结果都是单价的。两种价都必须出现，因为从 C 出发，两种决定都仍然可以达到。"
        "<bookmark mark='d'/>所以在某处有两个相邻的格局 C 零和 C 一，相差一步 e 撇，对第一个执行 e 得到零价，对第二个执行 e 得到一价。把它叫作一个决定性的步骤。",
    "Two cases destroy it. <bookmark mark='a'/> If e prime is a":
        "两种情形摧毁了它。<bookmark mark='a'/>如果 e 撇是 p 以外某个进程的步骤，这两步就可交换：按任何顺序执行，都得到同一个格局。<bookmark mark='b'/>那么 D 一可以从 D 零到达，"
        "一个一价格局位于一个零价格局之下。这不可能。<bookmark mark='c'/>如果 e 撇是 p 自己的步骤，就让 p 沉默。一个能扛住一次崩溃的协议，必须有一个从 C 零出发的有限执行，叫它 sigma，"
        "其中 p 从不行动，而有人做出了决定。<bookmark mark='d'/>sigma 不涉及 p 的任何步骤，所以它和 p 的两个步骤都可交换。从它的终点 A 出发，一条路径到达零价，另一条到达一价。"
        "<bookmark mark='e'/>所以 A 是二价的，可在那里已经做出了决定。无论哪种情形，都是矛盾。",
    "The third step builds the bad run. <bookmark mark='a'/> Keep":
        "第三步构造那个坏的执行。<bookmark mark='a'/>把进程放在一个队列里。每个阶段，取下一个进程，以及等着它的最老的那条消息；第二个引理让对手恰好投递这条消息，并再次落在一个二价格局上。"
        "<bookmark mark='b'/>永远重复下去。每个进程都走了无穷多步，每条消息都到达了，没有人崩溃，也没有人做出决定。<bookmark mark='c'/>这就是1985年的那个定理。注意，崩溃从未发生。"
        "仅仅是它的可能性，就迫使协议等待，而等待正是对手所利用的。",
    "Michael Ben-Or's protocol of 1983 escapes by flipping coins,":
        "Michael Ben-Or 1983年的协议靠抛硬币逃脱，并且能扛住任何少数进程的崩溃。<bookmark mark='a'/>每个阶段有两次投票。首先，每个进程发送它的值，并等待其中 n 减 f 个。"
        "如果全部 n 个进程中超过一半报告了同一个值，它就提议这个值，否则提议一个问号。<bookmark mark='b'/>然后它等待 n 减 f 个提议。v 的提议多于 f 个：决定 v。至少一个：采纳 v。一个也没有："
        "抛硬币。<bookmark mark='c'/>为什么它是安全的？在一个阶段里，永远不会有两个不同的值被提议，因为每个都需要多数的报告。<bookmark mark='d'/>而如果有人决定了 v，"
        "就有多于 f 个进程提议了它。每个进程至多错过 f 个提议，所以每个进程都会看到一个 v 并采纳它，<bookmark mark='e'/>于是在下一个阶段，所有地方都决定 v。",
    "Safety never depends on the coins; termination does.":
        "安全性从不依赖硬币；终止性才依赖。<bookmark mark='a'/>在任何阶段，抛硬币的进程都可能全部落在其他进程持有的那个值上，概率至少是二的 n 次方分之一。"
        "<bookmark mark='b'/>每个阶段都是一次全新的尝试，所以连续 t 个阶段都失败的概率，至多是一减二的负 n 次方，再取 t 次方，"
        "<bookmark mark='c'/>而期望的等待至多是二的 n 次方个阶段，再加一个阶段用来决定。<bookmark mark='d'/>我们的仪器用对半分的输入运行它，并让略少于一半的进程崩溃。"
        "四个进程平均用了4.8个阶段；六个，9.3个；八个，18.2个；十个，33.9个。<bookmark mark='e'/>每次执行都一致并且结束了，但平均值大约每多两个进程就翻一倍。一枚公共硬币，所有人看到的都一样，"
        "就能让它变成常数。",
    # ------------------------------------------------------------------ s07_shared
    "Chapter six. Shared memory and the consensus hierarchy.":
        "第六章。共享内存与共识层级。",
    "Now the processes share memory instead of sending messages.":
        "现在进程共享内存，而不再发送消息。<bookmark mark='a'/>最简单的共享对象是原子寄存器。进程读它、写它，每个操作虽然要花时间，但表现得就像是在它的区间内的某一个瞬间发生的。第33部分把这叫作可线性化。"
        "<bookmark mark='b'/>与一次写重叠的读，可能返回旧值，也可能返回新值，但这些瞬间会排成一个顺序的历史。<bookmark mark='c'/>进展的标准是无等待：每个操作都在它自己的有界步数内完成，"
        "即使其他所有进程都已经崩溃。没有锁，也不等任何人。这就是共享内存版本的扛住 n 减一次崩溃。",
    "Reading many registers at once is harder than it looks.":
        "一次读很多寄存器，比看上去要难。<bookmark mark='a'/>快照对象让每个进程更新它自己的寄存器，并且像在同一瞬间那样扫描所有寄存器。我们能用寄存器构造它吗？<bookmark mark='b'/>收集："
        "一个一个地读寄存器。<bookmark mark='c'/>与此同时进程2写了一次，第二次收集就不同了。<bookmark mark='d'/>再收集一次。连续两次收集相等，意味着中间什么都没变，"
        "所以这次收集就是一个真正的快照。<bookmark mark='e'/>但忙碌的写者可能让扫描者永远重试。解决办法来自1993年的 Afek、Attiya、Dolev、Gafni、Merritt 和 Shavit："
        "每次更新先做一次扫描，并把它存在自己的值旁边。一个扫描者如果看到某个进程移动了两次，就借用那个进程的扫描，那次扫描完全是在它自己的扫描期间做的。至多 n 加一次收集之后，必有某个进程移动了两次，所以每次扫描都是无等待的。",
    "Maurice Herlihy turned this into a ranking in 1991.":
        "莫里斯·赫利希（Maurice Herlihy）在1991年把这变成了一个排名。<bookmark mark='a'/>一个对象的共识数，是用它的副本和寄存器能解决无等待共识的最大进程数。"
        "<bookmark mark='b'/>寄存器，甚至快照，共识数都是一。<bookmark mark='c'/>测试并设置、交换、取并加、队列和栈，共识数是二。第33部分用测试并设置搭建过两进程共识；队列也能做到。"
        "把“赢”和“输”依次放进队列。每个进程写下自己的提议，然后出队：拿到“赢”的决定自己的值，另一个决定对方的值。<bookmark mark='d'/>比较并交换，以及链接加载与条件存储，位于无穷大。"
        "<bookmark mark='e'/>这个排名是有分量的：没有任何对象能无等待地实现更高一级的对象，所以不存在只用寄存器构造的无等待队列。",
    "Why can registers not do it for even two processes? Part 33":
        "为什么寄存器连两个进程都做不到？第33部分勾勒过这个论证；这里是它的各种情形。<bookmark mark='a'/>无等待协议的每次执行都是有限的，所以沿着二价格局走下去，我们会到达一个临界格局：它是二价的，"
        "但 p 的下一步使它变成零价，q 的下一步使它变成一价。<bookmark mark='b'/>如果 p 的那一步是读，它只改变 p。在 q 走了一步之后，两个格局只在 p 的内部不同。q 的读也一样，只是角色互换。"
        "<bookmark mark='c'/>如果它们写的是不同的寄存器，这两步可交换，顺序无关紧要。<bookmark mark='d'/>如果它们写的是同一个寄存器，q 的写会掩盖 p 的写。"
        "<bookmark mark='e'/>无论哪种情况，q 单独运行时，看到的都是同样的内存和它自己同样的状态。它必须做出决定，而且决定相同，尽管一边是零价的，另一边是一价的。",
    "The same method shows why test-and-set stops at two.":
        "同样的方法说明了为什么测试并设置止步于二。<bookmark mark='a'/>取三个进程和一个临界格局。两个决定性的步骤必须是对同一个对象的测试并设置：读和写已经被上一个证明排除，而作用于不同对象的步骤可交换。"
        "<bookmark mark='b'/>让 p 先走然后 q，或者 q 先走然后 p。无论哪种，这个比特最后都被置位，每个寄存器的内容都相同；只有 p 和 q 知道谁赢了。"
        "<bookmark mark='c'/>现在第三个进程 r 单独运行。它看到同样的内存，有同样的状态，所以做出同样的决定，可一边是零价的，另一边是一价的。<bookmark mark='d'/>只有两个进程时就没有 r，"
        "这就是为什么测试并设置对两个进程管用。<bookmark mark='e'/>比较并交换能逃脱，是因为它返回它找到的东西：任何去看的人都能知道谁赢了。",
    # ------------------------------------------------------------------ s08_topology
    "Chapter seven. Topology: why k-set agreement is impossible.":
        "第七章。拓扑：为什么 k 集合一致不可能。",
    "Maurice Herlihy and Nir Shavit's idea was to draw a task as":
        "赫利希和 Nir Shavit 的想法，是把一个任务画成一个形状。<bookmark mark='a'/>两个进程，蓝色的 p 和橙色的 q，各自从一个比特开始。一个顶点是一个进程连同它的值，"
        "一条边把能在同一次执行中出现的值连起来。四种组合都能出现，所以输入构成一个正方形。<bookmark mark='b'/>共识的输出只是两条边：都决定零，或者都决定一。"
        "<bookmark mark='c'/>任务是一个映射 delta，把每个输入单纯形映到它允许的输出。输入零和零只允许零和零。<bookmark mark='d'/>输入零和一允许任何一条边，但绝不允许混合。",
    "Now run a protocol. In each round a process writes its":
        "现在运行一个协议。每一轮，一个进程写下它的状态，然后对内存做一次即时快照，这是 Borowsky 和 Gafni 引入的一种轮。<bookmark mark='a'/>从输入零和一开始。如果 p 先走，它只看到自己，"
        "而 q 看到两者；如果一起走，两者都看到两者；如果 q 先走，它只看到自己。这条边变成了一条由三段组成的路径。<bookmark mark='b'/>每多一轮，又把每一段切成三段：始终是一条连通的路径。"
        "<bookmark mark='c'/>在一端，p 是单独运行的。它无法把这和一个两个输入都是零、而 q 很慢的执行区分开，所以它必须决定零；在另一端，q 必须决定一。"
        "<bookmark mark='d'/>决定在某处发生切换，而那条边就是一个它们意见不一的执行。",
    "With three processes the same thing happens in two":
        "有三个进程时，同样的事情发生在二维里。<bookmark mark='a'/>输入构成一个三角形，每个进程一个顶点。<bookmark mark='b'/>一轮即时快照把它切成13个三角形，"
        "三个进程的每一种排序方式各一个，允许并列。中间的三角形是三个一起走的执行；这个角上的三角形，是 p 零首先单独走的执行。<bookmark mark='c'/>每个小三角形的每种颜色各有一个顶点："
        "在一次执行中同时出现的三个视野。<bookmark mark='d'/>两轮得到169个。不管多少轮，协议复形都是这个三角形的一个细分，没有洞，而这正是不可能性证明要用到的。",
    "The tool is a lemma Emanuel Sperner proved in 1928.":
        "工具是 Emanuel Sperner 在1928年证明的一个引理。<bookmark mark='a'/>把一个三角形切成许多小三角形，并给顶点着色：三个角分别是0、1和2；边上的顶点，取那条边两个端点颜色之一；"
        "内部的顶点，随便什么颜色。<bookmark mark='b'/>那么某个小三角形具有全部三种颜色；事实上，这样的三角形有奇数个，这里是64个中的19个。<bookmark mark='c'/>证明数的是门，"
        "也就是颜色为0和1的边。对所有小三角形求和，内部的门被数两次，边界上的门被数一次。<bookmark mark='d'/>一个彩虹三角形恰好有一扇门，其他三角形有零扇或两扇。"
        "<bookmark mark='e'/>所以彩虹三角形的数目，与边界门的数目奇偶性相同，而边界门都在0到1的那条边上，那里颜色切换了奇数次。再用200种随机着色，在一个由100个三角形组成的更细的网格上：总是奇数。",
    "Soma Chaudhuri asked in 1990 about a weaker agreement.":
        "Soma Chaudhuri 在1990年问到一种更弱的一致。<bookmark mark='a'/>在 k 集合一致中，每个进程决定其中一个输入，而被决定的不同值至多有 k 个。"
        "<bookmark mark='b'/>有 f 次崩溃时，如果 k 大于 f，就很容易：等待 n 减 f 个值，然后决定最小的那个。<bookmark mark='c'/>那更小的 k 呢？取三个进程，允许两个值，"
        "不等待，并让进程 i 的输入就是 i。<bookmark mark='d'/>一个进程只能决定它见过的编号，所以一个角决定它自己的编号，而边上的一个顶点决定那条边两个端点之一。这就是一个 Sperner 着色。"
        "<bookmark mark='e'/>所以某个三角形是彩虹的：一次决定了三个值的执行。1993年，三个团队证明了一般情形：只要 k 至多是 f，k 集合一致就不可能。",
    "Herlihy and Shavit turned the picture into a theorem.":
        "赫利希和 Shavit 把这幅图变成了一个定理。<bookmark mark='a'/>用寄存器运行一个无等待协议，会细分输入复形。<bookmark mark='b'/>决定是从这个细分到输出的一个映射，"
        "它把每个顶点送到同一个进程的一个顶点，把每个单纯形送到 delta 允许的一个输出。<bookmark mark='c'/>异步可计算性定理说，这就是全部：一个任务能用寄存器无等待地解决，"
        "恰好当这样的细分和这样的映射存在。可解性变成了一个关于形状的问题。<bookmark mark='d'/>2004年的哥德尔奖授予了赫利希和 Shavit，以及萨克斯（Saks）和 Zaharoglou，以表彰这项工作。",
    # ------------------------------------------------------------------ s09_detectors
    "Chapter eight. Failure detectors.":
        "第八章。故障检测器。",
    "Chapter five showed that one possible crash makes":
        "第五章表明，一次可能的崩溃就让异步共识变得不可能。1996年，Tushar Chandra 和 Sam Toueg 问：关于崩溃，要知道多少才够？<bookmark mark='a'/>给每个进程一个本地的预言机，"
        "即故障检测器，它输出它当前怀疑已经崩溃的那些进程。<bookmark mark='b'/>当进程3崩溃时，其他进程的检测器逐渐开始怀疑它。<bookmark mark='c'/>但检测器可能出错。进程1怀疑进程5，"
        "而进程5只是慢了，等它的消息到达，进程1又重新信任它。<bookmark mark='d'/>关键的洞见是，用检测器可能犯的错误来描述它们，而不是用它们的构造方式。",
    "How is such a detector built? With heartbeats. <bookmark":
        "这样的检测器怎么构造？用心跳。<bookmark mark='a'/>进程 q 每个周期发送一次心跳，如果在超时时间内一次都没到，p 就怀疑 q。<bookmark mark='b'/>一次心跳被延迟了，计时器到期，"
        "p 怀疑了一个健康的 q。等心跳到达，p 重新信任 q，并把超时时间加倍。<bookmark mark='c'/>当 q 真的崩溃时，心跳停止，p 就永远怀疑它。<bookmark mark='d'/>在部分同步下，"
        "一旦网络稳定下来，心跳之间的间隔至多是延迟上界加上周期。每犯一次错，超时时间就加倍，<bookmark mark='e'/>所以犯了对数次错误之后，就不会再犯了。"
        "<bookmark mark='f'/>结果是一个最终完美的检测器。",
    "Chandra and Toueg sorted detectors by two properties.":
        "Chandra 和 Toueg 按两个性质给检测器分类。<bookmark mark='a'/>完备性：每个崩溃的进程最终都会被每个正确的进程永远怀疑，或者在弱的版本里，被某个正确的进程永远怀疑。"
        "<bookmark mark='b'/>准确性：强的版本是，没有进程在崩溃之前被怀疑；弱的版本是，某个正确的进程从不被怀疑。<bookmark mark='c'/>还有最终的版本，它们只在某个未知的时刻之后才成立。"
        "<bookmark mark='d'/>这就得到八个类。<bookmark mark='e'/>但如果每个进程把自己的怀疑转发给所有人，弱完备性就会变成强完备性，于是剩下四个类。"
        "<bookmark mark='f'/>我们的心跳检测器是最终完美的，而最弱的那个，最终强检测器，将会被证明已经足够。",
    "Here is Chandra and Toueg's algorithm for an eventually":
        "这是 Chandra 和 Toueg 针对最终强检测器和正确多数的算法。<bookmark mark='a'/>协调者一轮一轮地轮换，每个人都把一个估计值发给它，上面标着这个估计值被采纳的轮次。"
        "<bookmark mark='b'/>在第1轮，协调者很慢，检测器怀疑它，其他进程拒绝它并继续前进。错误只花费时间，从不损害安全性。<bookmark mark='c'/>在第2轮，进程2收集到多数的估计值，"
        "取最新的那个并提议它；其他进程采纳它并确认。<bookmark mark='d'/>有了多数的确认，它就做出决定。<bookmark mark='e'/>安全性靠的是计数：两个多数总是共享一个进程，"
        "所以之后的每个协调者都会看到被采纳的值。",
    "Why must a majority be correct? <bookmark mark='a'/> Split":
        "为什么必须有多数是正确的？<bookmark mark='a'/>把进程分成两半，一半输入零，一半输入一，并允许其中一半崩溃。<bookmark mark='b'/>在执行一中，右半边在开始时就崩溃了。"
        "左半边必须自己做决定；它只见过零，所以它决定零，时间是某个 t A。<bookmark mark='c'/>在执行二中，左半边崩溃，右半边决定一，时间是 t B。<bookmark mark='d'/>在执行三中，"
        "没有人崩溃，但跨越两半的消息很慢，每一半都怀疑另一半，直到两边都做出决定，而最终准确性允许这样。<bookmark mark='e'/>每一半看到的都和以前一样：一半决定零，另一半决定一。"
        "<bookmark mark='f'/>强检测器则根本不需要多数。",
    "Is eventually strong the least a detector can offer?":
        "最终强是一个检测器能提供的最少的东西吗？<bookmark mark='a'/>Omega 只输出一个进程，也就是领导者。各处的输出可能不一致，也可能改变，被信任的进程也可能崩溃，"
        "<bookmark mark='b'/>但最终，每个正确的进程都会永远信任同一个正确的进程。<bookmark mark='c'/>1996年，Chandra、Vassos Hadzilacos 和 Toueg 证明，"
        "任何能用来解决共识的检测器都能模拟 Omega：它是最弱的。<bookmark mark='d'/>证明重用了第五章的价论证：用采样得到的检测器输出模拟各种执行，找出决定结果的那一步；走这一步的进程必定是正确的。"
        "<bookmark mark='e'/>Omega 与最终强检测器等价，它就是 Paxos 和 Raft 中的领导者选举。",
    "Real systems turn suspicion into a number. <bookmark":
        "真实系统把怀疑变成一个数。<bookmark mark='a'/>Naohiro Hayashibara 和同事们2004年提出的 phi 累积故障检测器，用一个分布去拟合最近心跳之间的间隔。"
        "<bookmark mark='b'/>随着时间过去而没有心跳，心跳仍在路上的可能性就越来越小，<bookmark mark='c'/>而 phi 就是这个概率以10为底的对数的相反数。"
        "<bookmark mark='d'/>当 phi 超过阈值时就怀疑：阈值为8，意味着出错的概率是一亿分之一。<bookmark mark='e'/>还有2002年的 SWIM，它随机探测成员，"
        "并用 gossip 传播结论，所以不管组有多大，检测给每个进程带来的代价都相同。",
    # ------------------------------------------------------------------ s10_communication
    "Chapter nine. The cost of agreement.":
        "第九章。一致的代价。",
    "How expensive is agreement? Count the messages. <bookmark":
        "一致有多贵？数一数消息。<bookmark mark='a'/>在一轮全对全的通信中，n 个进程中的每一个都向其他 n 减一个进程发送消息：七个进程就是42条消息。"
        "<bookmark mark='b'/>第四章的泛洪协议把这重复 f 加一轮。<bookmark mark='c'/>要对付三分之一的进程出故障，这大约是 n 的立方的三分之一。"
        "<bookmark mark='d'/>兰波特、Shostak 和 Pease 最初的拜占庭协议要糟糕得多：进程转发每一条名字链，消息数像 n 的 f 加一次方那样增长。"
        "<bookmark mark='e'/>我们数的是正确的进程发送的消息，或者它们携带的字，每个字是一个值或一个签名。这些代价中，哪些是必需的？",
    "In 1985 Danny Dolev and Rüdiger Reischuk showed that much of":
        "1985年，Danny Dolev 和 Rüdiger Reischuk 证明，其中很大一部分是必需的。<bookmark mark='a'/>每个确定性的拜占庭一致协议都有这样的执行："
        "其中正确的进程发送 n 加 f 平方量级的消息，而签名也帮不上忙。<bookmark mark='b'/>把谁给谁发消息画成一个矩阵；全对全的通信会把它填满。"
        "<bookmark mark='c'/>证明找出一个由 f 除以二个进程组成的集合 V，其中每个进程都必须收到大约 f 除以二条消息：<bookmark mark='d'/>至少是 f 平方除以四。"
        "<bookmark mark='e'/>允许最多的故障，也就是 n 的三分之一，这大约是 n 平方除以36：二次的，不管是什么协议。<bookmark mark='f'/>他们还证明了，"
        "带认证的协议需要 n 乘 f 量级的签名。",
    "Here is the heart of it, as Ittai Abraham and colleagues":
        "这是它的核心，按照 Ittai Abraham 和同事们在2019年的重述。<bookmark mark='a'/>假设一个协议发送的消息总是少于 f 除以二的平方条。腐化一个由 f 除以二个进程组成的集合 V，"
        "它们行为诚实，但忽略各自收到的前 f 除以二条消息。<bookmark mark='b'/>消息这么少，V 中就有某个成员 p 收到的少于 f 除以二条：它忽略了一切。"
        "<bookmark mark='c'/>现在看第二个世界：p 是诚实的，而改为腐化那几个给 p 写过消息的进程，它们对 p 保持沉默。故障仍然少于 f 个。"
        "<bookmark mark='d'/>其他所有进程看到的又是第一个世界。p 什么都没听到，决定某个固定的值 b；给发送者另一个值，有效性就会让其余进程决定那个值。",
    "Practical protocols meet this cost in different ways.":
        "实用的协议以不同的方式应对这个代价。<bookmark mark='a'/>PBFT，即 Miguel Castro 和芭芭拉·利斯科夫（Barbara Liskov）1999年的协议，"
        "让每个副本把自己的投票发给其他每个副本：每个阶段 n 乘 n 减一条消息。<bookmark mark='b'/>HotStuff，来自2019年的 Maofan Yin、Dahlia Malkhi、"
        "Michael Reiter、Guy Golan Gueta 和 Ittai Abraham，改为把投票发给领导者。<bookmark mark='c'/>领导者把二 f 加一张投票合并成一个门限签名，即法定人数证书，"
        "再把这单独一个字发回去：每个阶段二乘 n 减一条消息。<bookmark mark='d'/>是线性的，而不是二次的，而且在更换领导者时仍然保持线性，而 PBFT 的视图变更要花费 n 的立方量级的字。",
    "Does that beat Dolev and Reischuk? No. <bookmark mark='a'/>":
        "这打败了 Dolev 和 Reischuk 吗？没有。<bookmark mark='a'/>一个有故障的领导者可以干脆保持沉默；它的视图就浪费了，HotStuff 接着换到下一个领导者。"
        "<bookmark mark='b'/>如果连续有 f 个坏领导者，每个视图大约花费 n 个字，<bookmark mark='c'/>所以总数是 f 乘 n，而 f 是 n 的三分之一时，这又是二次的了。"
        "下界说的是最坏情况，而最坏情况就是一连串的坏领导者。<bookmark mark='d'/>而且这个界是紧的。最坏情况下为二次的协议，同步情形由 Atsuki Momose 和 Ling Ren 在2021年找到，"
        "部分同步情形由 Pierre Civit 和同事们在2022年找到。",
    "The bound is for deterministic protocols. What does":
        "这个界针对的是确定性协议。随机性能买到什么？<bookmark mark='a'/>选一个小的随机委员会，让它内部达成一致，再让它告诉所有人：c 平方加 c 乘 n 条消息。"
        "<bookmark mark='b'/>如果出故障的进程不到全部的三分之一，一个随机委员会有一半出故障的概率，相对于它的规模是指数级地小，<bookmark mark='c'/>所以一个对数规模的委员会就够了，"
        "<bookmark mark='d'/>代价降到大约 n log n。<bookmark mark='e'/>麻烦在于自适应对手，它会在委员会一公布就腐化它。Algorand，"
        "由 Jing Chen 和 Silvio Micali 提出，让成员秘密地自我选出，并且只发言一次。<bookmark mark='f'/>但面对还能抹掉已经发出的消息的对手，Abraham 和同事们证明，"
        "即使是随机化协议也需要 f 平方。<bookmark mark='g'/>随机性还能买到时间：Pesech Feldman 和 Silvio Micali 达到了期望常数轮。",
    # ------------------------------------------------------------------ s11_population
    "Chapter ten. Population protocols.":
        "第十章。种群协议。",
    "The last model is the most minimal of all. In 2004 Dana":
        "最后一个模型是所有模型中最精简的。2004年，Dana Angluin、James Aspnes、Zoë Diamadi、迈克尔·费希尔（Michael Fischer）"
        "和 René Peralta 设想了由一群鸟携带的微型传感器。<bookmark mark='a'/>这些个体是匿名的，每一个都是一个有限状态机，它的状态数不随种群规模增长。"
        "<bookmark mark='b'/>一个随机调度器每次挑选两个个体，两者都按照一条固定的规则更新。<bookmark mark='c'/>时间用并行时间来计：交互次数除以 n。"
        "<bookmark mark='d'/>最简单的协议是传染。一个知情的个体告诉它遇到的任何个体，于是在对数并行时间内，所有个体都知道了。<bookmark mark='e'/>没有哪个个体会知道计算已经结束；"
        "答案只需要稳定下来。",
    "Can such agents decide which of two opinions is in the":
        "这样的个体能判断两种意见中哪一种占多数吗？<bookmark mark='a'/>四个状态就够了：强意见 A 和 B，以及弱意见小 a 和小 b。当两个相反的强意见相遇时，两者都变成弱的。"
        "<bookmark mark='b'/>一个强个体会转化另一方的一个弱个体。<bookmark mark='c'/>注意强计数之间的差。抵消会去掉一个强 A 和一个强 B，"
        "<bookmark mark='d'/>而转化只涉及弱个体，<bookmark mark='e'/>所以强 A 减强 B 永远等于初始的差额。<bookmark mark='f'/>如果 A 一开始领先，"
        "强 A 就永远不会用完；强 B 必定会用完，因为只要两者都还在，它们就会不断相遇；然后每个弱 b 都会被转化。所有个体都输出 A。<bookmark mark='g'/>它总是对的，不过平局永远不会稳定下来。",
    "Here is our instrument's run: a hundred agents, fifty-two":
        "这是我们仪器的一次运行：100个个体，52个支持 A，48个支持 B，差额为4。<bookmark mark='a'/>强个体是实心的，弱个体是空心的。在几个单位的并行时间之内，大多数强意见就已经抵消了。"
        "<bookmark mark='b'/>强计数一起下降，而它们的差从不变化：27减23，一直到4减0。<bookmark mark='c'/>最后一个强 B 在时间20就已经消失了。"
        "<bookmark mark='d'/>然后4个强 A 必须找到剩下的每一个弱 b，这个缓慢的收尾占去了大部分时间。58个单位之后，每个个体都说 A。",
    "Why so slow? Look at the mop-up. <bookmark mark='a'/> With m":
        "为什么这么慢？看看收尾。<bookmark mark='a'/>还剩 m 个强 A 时，某个特定的弱 b 在一次给定的交互中遇到其中一个的概率，是二 m 除以 n 乘 n 减一。"
        "<bookmark mark='b'/>还剩 k 个弱 b 时，某个 b 被转化的概率是这个概率的 k 倍。<bookmark mark='c'/>依次等待每一个，得到一个调和和，"
        "<bookmark mark='d'/>再除以 n，大约是 n 除以二 m，再乘以 n 的自然对数。<bookmark mark='e'/>我们的仪器在差额为2的情况下，分别用50、100、200和400个个体运行："
        "64、136、284和673个单位，与估计很接近。<bookmark mark='f'/>更多的状态会让它快得多：2021年，David Doty 和同事们用对数个状态达到了对数时间。",
    "If a small chance of error is acceptable, three states and":
        "如果可以接受一个小的出错概率，三个状态和对数时间就够了。<bookmark mark='a'/>在 Dana Angluin、James Aspnes 和 David Eisenstat 2008年的协议中，"
        "当 x 遇到 y 时，响应者变成空白；<bookmark mark='b'/>而一个意见遇到空白时，就招募它。<bookmark mark='c'/>意见相互击倒，又相互招募，较大的一方像滚雪球一样越滚越大。"
        "<bookmark mark='d'/>它以高概率在对数并行时间内收敛，而且只要差额大于大约 n 乘 log n 的平方根，就会收敛到初始的多数。<bookmark mark='e'/>很快，但在票数接近时可能出错。"
        "<bookmark mark='f'/>2012年，Luca Cardelli 和 Attila Csikász-Nagy 注意到，控制细胞周期的开关具有同样的结构。",
    "What, exactly, can a population compute? <bookmark":
        "一个种群到底能计算什么？<bookmark mark='a'/>一个经典的例子：是否至少有五只鸟生病了？每个个体最多数到五。当两个个体相遇时，一个取两者之和，另一个降为零；一旦某个和达到五，两者都说“是”，"
        "而“是”会像传染一样扩散。<bookmark mark='b'/>多数也是同一类问题：x A 大于 x B 意味着 x A 减 x B 至少是一，这是一个阈值。<bookmark mark='c'/>阈值、"
        "余数以及它们的组合，就是半线性谓词，也就是 Presburger 算术的那些谓词。Angluin 和同事们证明了它们全都能被计算，而在2006年，Angluin、Aspnes 和 Eisenstat 证明了别的都不能。"
        "<bookmark mark='d'/>平方数和二的幂就不能。<bookmark mark='e'/>化学反应网络是用分子实现的同一个模型；在不出错的情况下，它们恰好能计算半线性函数，而 DNA 可以实现它们。",
    # ------------------------------------------------------------------ s12_frontier
    "Chapter eleven, the frontier. Which local problems need how":
        "第十一章，前沿。哪些局部问题需要多少轮？",
    "Linial's bound has grown into a theory. <bookmark mark='a'/>":
        "Linial 的界已经发展成了一套理论。<bookmark mark='a'/>局部可检验标号问题，是这样一种问题：每个节点只看自己的邻域就能验证解，比如着色。"
        "Moni Naor 和 Larry Stockmeyer 在1995年引入了它们。<bookmark mark='b'/>在环和路径上，每个这样的问题要么需要常数时间，要么需要迭代对数时间，要么需要关于 n 线性的时间，"
        "中间什么都没有。三着色是迭代对数的；偶数环上的二着色是线性的，因为一个节点必须知道自己位置的奇偶性。<bookmark mark='c'/>在树和一般图上，图景要丰富得多，而用轮消除这样的工具去描绘它，是活跃的研究领域。",
    "Three threads have moved fast. <bookmark mark='a'/> In 2020":
        "有三条线索进展很快。<bookmark mark='a'/>2020年，Václav Rozhoň 和 Mohsen Ghaffari 展示了如何在多对数轮内，确定性地把任何网络划分成直径很小的簇，"
        "这个问题悬而未决了几十年，许多确定性算法都由此而来。<bookmark mark='b'/>在 CONGEST 模型中，每条消息只有对数个比特，而最短路径、割和匹配都从通信复杂性得到了下界。"
        "<bookmark mark='c'/>而随机性对局部性究竟有多大帮助，仍在一个问题一个问题地确定之中。<bookmark mark='d'/>同样的想法如今也在普通算法内部运行，给出快速的并行方法和亚线性时间方法。",
    "Open problems. <bookmark mark='a'/> The exact number of":
        "开放问题。<bookmark mark='a'/>在一般图上求极大独立集所需的确切轮数。<bookmark mark='b'/>用比最大度多一种的颜色进行确定性着色，能否和随机化着色一样快。"
        "<bookmark mark='c'/>面对一个在协议运行中选择腐化谁的对手，拜占庭一致的通信代价。<bookmark mark='d'/>还有状态很少的、最快的多数种群协议。"
        "<bookmark mark='e'/>这一部分的研究题是第一个：在 LOCAL 模型中确定性地计算极大独立集，找到相互匹配的上界和下界。",
    # ------------------------------------------------------------------ s13_outro
    "What we built in this part. Models of distributed":
        "我们在这一部分搭建了什么。分布式计算的模型，以及它们允许的故障。Cole 和 Vishkin 用7轮给一个百万节点的环着色，以及 Linial 关于迭代对数不可避免的证明。崩溃的 f 加一轮界，"
        "以及证明三个进程扛不住一个撒谎者的六边形。逃脱 FLP 的随机化共识；共享对象的共识层级；k 集合一致不可能性的拓扑证明；故障检测器；还有匿名个体种群的协议。贯穿始终的是一个想法：在分布式系统中，每个进程无法知道的东西，"
        "限制了所有进程能做的事。",
    "Where this comes back. Part 60's accelerators are networks":
        "它们会在哪里再出现。第60部分的加速器是由处理单元组成的网络，它们给邻居传递消息。第61部分会问如何选择一个开放问题，以及如何诚实地测量。而回头看，它是第38部分的共识、第39部分的复制，"
        "以及第54部分所检验的那些协议底下的理论。",
    "In practice. State the fault model: which failures, and how":
        "在实践中。陈述故障模型：哪些故障，有多少。对拜占庭故障，没有任何协议能容忍三分之一或更多的进程撒谎。使用部分同步：安全性始终成立，网络稳定下来之后就有进展。在确定性做不到的地方，用随机性打破对称。"
        "并用 gossip 传播状态，它在对数轮之内就能到达所有人。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：实现 Ben-Or 的随机化共识，并测量它的轮数如何增长。最后一道标了星号，是一道研究题：LOCAL 模型中极大独立集的相互匹配的界。",
    "Next time, Part 60: hardware built for one job. When the":
        "下一次，第60部分：为单一工作而造的硬件。当免费的加速结束时，答案是专用化。我们在 Pebble 的门级模拟器里搭建一个脉动阵列，把它放到屋顶线模型上，最后用硬件来完成那项任务。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
