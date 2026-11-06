"""Chinese narration for cs27: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第27部分：证明与随机性"

CHAPTERS = {
    "Hook": "不读全文的检查",
    "Classes": "1. 随机复杂性类",
    "Derandom": "2. 以困难换随机",
    "Circuits": "3. 电路下界",
    "Communication": "4. 通信复杂性",
    "Interactive": "5. 交互式证明",
    "Sumcheck": "6. Sum-check 与 IP = PSPACE",
    "ZeroKnowledge": "7. 零知识",
    "Pcp": "8. PCP 定理",
    "Approx": "9. 近似的困难性",
    "Ugc": "10. 唯一博弈猜想",
    "FineGrained": "11. 细粒度复杂性",
    "Parameterized": "12. 参数化复杂性",
    "Counting": "13. 计数",
    "Average": "14. 平均情形与单向函数",
    "Frontier": "15. 前沿：MIP* = RE 与实践中的证明",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "A proof used to mean a document you read from beginning to end.":
        "证明，过去指的是一份从头读到尾的文件。这一部分从三个方向打破这个观念。<bookmark mark='a'/>第一：证明可以写成这样一种形式，只读其中随机的"
        "几位就够了。正确的证明总能通过；而一个假命题的任何证明，都会以很高的概率被识破。<bookmark mark='b'/>第二：证明可以是一场对话。一个证明者声称"
        "某个公式有七个满足赋值。我们随机提问，在模九十七下运算时，撒谎的证明者大约五次能蒙混过关一次；而在一百万元素的域上，我们的试验中一次也没有。"
        "<bookmark mark='c'/>第三：证明可以除了命题为真之外什么也不泄露。你可以相信一个图能三着色，却对它一无所知；作弊者撑过三百轮的机会不到十亿分之一。"
        "<bookmark mark='d'/>每一种都用确定性换来一个出错的机会，而这个机会可以要多小就有多小。",
    "Part 27 of Computer Science, Built: Proofs and Randomness.":
        "计算机科学，从零搭建，第27部分：证明与随机性。<bookmark mark='a'/>这一部分包括：随机算法的复杂性类，以及为什么随机性也许终究不增加能力；"
        "电路下界，包括我们亲手测量的切换引理；双方之间的通信；交互式证明，从图非同构到 sum-check 协议与 IP 等于 PSPACE；零知识；PCP 定理，以及它"
        "为什么让近似变难；唯一博弈猜想；细粒度复杂性与参数化复杂性；计数；还有2020年一个把证明与量子纠缠和停机问题联系起来的结果。",
    # ------------------------------------------------------------------ Classes
    "Chapter one. Randomized classes.": "第1章。随机复杂性类。",
    "Part 20 used coins to make algorithms simpler and faster.":
        "第20部分用硬币让算法更简单、更快。这里是它们所定义的类，由 John Gill 在1977年命名。<bookmark mark='a'/>RP 允许单侧错误：从不错说“是”，"
        "而真正的“是”至少有一半的时候被说出。合数判定是经典例子，用的是 Miller-Rabin 测试。<bookmark mark='b'/>coRP 是它的镜像。<bookmark "
        "mark='c'/>ZPP 从不出错，但运行时间是随机变量，就像随机选枢轴的快速排序。<bookmark mark='d'/>而 BPP 允许两侧都出错，在每个输入上至多三分之一。"
        "<bookmark mark='e'/>它们层层嵌套：P 在 ZPP 之内，ZPP 恰好等于 RP 与 coRP 的交，它又在 BPP 之内，BPP 在多项式空间之内。<bookmark "
        "mark='f'/>注意，概率是对算法自己的硬币而言的。输入是任意的，甚至可以由对手挑选。",
    "Why a third?":
        "为什么是三分之一？任何小于二分之一的常数都行，因为错误可以压下去。<bookmark mark='a'/>用新的硬币把算法运行 k 次，取多数答案。<bookmark "
        "mark='b'/>只有超过一半的运行出错，多数才会出错。我们计算了精确的二项式尾部：一百零一次运行把错误从三分之一降到万分之三以下；两百零一次，降到"
        "大约两百万分之一。<bookmark mark='c'/>人工智能，从零搭建中的尾部界，Chernoff 界，保证了随 k 指数衰减。<bookmark mark='d'/>所以三分之一这个"
        "门槛是任意的：任何与二分之一保持距离的错误率，都定义同一个类。",
    "Amplification has a surprising consequence.":
        "放大有一个出人意料的推论。<bookmark mark='a'/>一直放大，直到每个输入上的错误低于二的负 n 加一次方：对一百位的输入，大约一千一百次运行。"
        "<bookmark mark='b'/>长度为 n 的输入有二的 n 次方个，所以一串随机硬币对其中任何一个是坏的概率，至多是二的 n 次方乘以错误率：低于一半。"
        "<bookmark mark='c'/>所以存在某一串硬币，对这个长度的每个输入都是好的。<bookmark mark='d'/>把它固化进电路，随机性就消失了：每个输入长度一个"
        "多项式规模的电路。Leonard Adleman 在1978年证明了这一点。<bookmark mark='e'/>而 Michael Sipser、Péter Gács 和 Clemens Lautemann 证明了，"
        "BPP 位于第26部分多项式层级的第二层。",
    # ------------------------------------------------------------------ Derandom
    "Chapter two. Hardness against randomness.": "第2章。以困难换随机。",
    "Part 20's frontier previewed the idea; here is how it works.":
        "第20部分的前沿一章预告过这个想法；下面是它的原理。<bookmark mark='a'/>从一个很短的真随机种子开始，只有对数多位。选出它的许多位置子集，彼此"
        "重叠极少，这叫组合设计，再对每个子集施加一个困难函数 f。每施加一次，得到一个输出位。<bookmark mark='b'/>Noam Nisan 和 Avi Wigderson 在1988年"
        "证明，重叠很小让这些输出几乎相互独立。<bookmark mark='c'/>如果某个小电路能把这串输出和真硬币区分开，混合论证就能把它变成一个计算 f 的小电路，"
        "与 f 的困难性矛盾。<bookmark mark='d'/>所以这串输出骗过每个小电路，而随机算法正是这样的电路。种子是对数长，种子就只有多项式多个：全部试一遍，"
        "取多数。完全不用硬币。",
    "Here is the problem at the centre of derandomization.":
        "这是去随机化的核心问题。<bookmark mark='a'/>这个行列式，范德蒙德行列式，等于所有差的乘积吗？对十个变量把它展开，会产生超过三百五十万项。"
        "<bookmark mark='b'/>换个办法：在模一个素数下随机取值，比较两边：大约十分之一毫秒。Richard DeMillo 与 Richard Lipton、Jacob Schwartz 与 "
        "Richard Zippel 证明了，一个 d 次的非零多项式在随机点上为零的概率至多是 d 除以 p。<bookmark mark='c'/>真的恒等式通过了每一次测试。一个假的，"
        "只改了一个符号，在域很小时蒙混过关的频率略低于界所允许的；在一百万的域上，五千次尝试中一次也没有。<bookmark mark='d'/>所以恒等测试有快速的"
        "随机算法。没人知道一个确定性的多项式算法。",
    "This turns into a striking trade-off.":
        "这变成了一个惊人的权衡。<bookmark mark='a'/>Russell Impagliazzo 和 Avi Wigderson 在1997年证明：如果某个指数时间可解的问题需要指数规模的电路，"
        "那么 P 等于 BPP。<bookmark mark='b'/>几乎所有人都相信这个假设，所以几乎所有人都相信，随机性不给多项式时间算法增加额外的能力。<bookmark "
        "mark='c'/>反方向也部分成立：Valentine Kabanets 和 Impagliazzo 证明，从多项式恒等测试中去掉硬币，本身就会证明新的电路下界。<bookmark "
        "mark='d'/>所以去随机化和下界是同一个问题的两面。<bookmark mark='e'/>素性判定是招牌例子：从1970年代起就有随机测试，2002年起有了确定性的多项式"
        "测试。<bookmark mark='f'/>实践中没人用确定性测试：Miller-Rabin 快得多。",
    # ------------------------------------------------------------------ Circuits
    "Chapter three. Circuit lower bounds.": "第3章。电路下界。",
    "Circuits give a purely combinatorial way at P versus NP.":
        "电路给出一条纯组合的路，通向 P 与 NP。<bookmark mark='a'/>P/poly 是这样一类问题：每个输入长度都有一个多项式规模的电路。<bookmark "
        "mark='b'/>它包含 P，而由 Adleman 定理，也包含 BPP。<bookmark mark='c'/>所以证明 SAT 需要超多项式规模的电路，就能把 P 和 NP 分开，不涉及任何"
        "机器，只有门。<bookmark mark='d'/>Richard Karp 和 Richard Lipton 证明，如果 SAT 真有小电路，多项式层级就会塌缩到第二层。<bookmark "
        "mark='e'/>所以多数人相信 SAT 需要大电路，但证明它会撞上第26部分的障碍。<bookmark mark='f'/>能证明的是受限电路的下界。第一个成功的是常数深度的"
        "电路。",
    "Johan Håstad's tool is the random restriction.":
        "Johan Håstad 的工具是随机限制。<bookmark mark='a'/>这是一个析取范式的公式：二十个项，每项是三个文字的与，再把它们或起来，共十四个变量。"
        "<bookmark mark='b'/>把每个变量固定为一个随机值，只是以概率 p 让它保持自由。<bookmark mark='c'/>大多数项死掉了：一个假文字就能杀死一项。只要"
        "有一项变真，整个公式就为真。<bookmark mark='d'/>剩下的东西非常小。这个限制留下的函数，用深度为二的决策树就能计算。",
    "How often does a restriction leave something complicated?":
        "一个限制多久会留下复杂的东西？<bookmark mark='a'/>我们在每个 p 值上施加一千五百个随机限制，并算出剩余函数的精确决策树深度。Håstad 的切换引理"
        "把深度达到 s 或以上的概率限制在五 p w 的 s 次方以内，而在这个界适用的地方，测得的频率都远在界内。<bookmark mark='b'/>浅的决策树可以正着写，"
        "也可以反着写，所以与的或切换成或的与。<bookmark mark='c'/>反复施加限制，常数深度的电路就一层一层地塌缩。<bookmark mark='d'/>但奇偶函数从不"
        "塌缩：限制它，得到的是自由变量的奇偶。<bookmark mark='e'/>所以奇偶函数需要指数大的常数深度电路，这是 Furst、Saxe 与 Sipser，Ajtai，以及 "
        "Yao 的结果，由 Håstad 做到了精确。",
    "Other restricted models fell too.":
        "其他受限模型也相继被攻破。<bookmark mark='a'/>Alexander Razborov 和 Roman Smolensky 证明，即使允许模三计数的门，奇偶函数仍需要指数规模；他们的"
        "方法是用一个低次多项式近似整个电路。Razborov 还证明，没有非门的单调电路计算团问题需要超多项式规模。而 Ryan Williams 把非确定指数时间和 "
        "ACC 零分开了。<bookmark mark='b'/>他的证明很不寻常：对这类电路，一个只比尝试全部二的 n 次方个输入稍快一点的可满足性算法，就意味着对它们的下界。"
        "<bookmark mark='c'/>算法蕴含下界。这是迄今唯一越过了第26部分那些障碍的方法。",
    # ------------------------------------------------------------------ Communication
    "Chapter four. Communication complexity.": "第4章。通信复杂性。",
    "In 1979 Andrew Yao asked a clean question:":
        "1979年，姚期智提出了一个干净的问题：如果 Alice 持有一个输入，Bob 持有另一个，要计算关于两者的某个量，他们必须交换多少位？<bookmark mark='a'/>"
        "以相等为例。两个 n 位串相同吗？<bookmark mark='b'/>有了随机性，这很便宜。Alice 把她的串看作一个多项式，随机取一个点，把这个点和取值发过去："
        "第20部分的指纹，做成了协议。不同的串在随机点上相等的概率至多是 n 除以 q。<bookmark mark='c'/>对只有一处不同的一千位串，在一百万的域上，我们"
        "两万次试验从未出错。对一万亿位的串，一百六十二位就够了。<bookmark mark='d'/>没有随机性，Alice 必须发送全部 n 位，而这可以证明。",
    "How do you prove that a protocol needs many bits?":
        "怎样证明一个协议需要很多位？<bookmark mark='a'/>把函数写成矩阵，Alice 的输入作行，Bob 的作列。一个交换 c 位的协议把这个矩阵切成至多二的 c "
        "次方个矩形，每个矩形取值不变。<bookmark mark='b'/>对相等问题，矩阵是单位阵。没有哪个矩形能包含两个对角线上的一：包含 x, x 和 y, y 的矩形也"
        "包含 x, y，而那里是零。<bookmark mark='c'/>所以需要二的 n 次方个矩形，也就是 n 位。<bookmark mark='d'/>线性代数通过矩阵的秩给出同样的界。"
        "<bookmark mark='e'/>有些函数连随机性也对付不了。判定两个集合是否相交需要线性多位，不论随机与否。<bookmark mark='f'/>而秩的对数是否总能在多项式"
        "意义上预测真实代价，就是对数秩猜想，自1988年起悬而未决。",
    "This explains a design choice from Part 20.":
        "这解释了第20部分的一个设计选择。<bookmark mark='a'/>一个有 s 位内存的流式算法就是一个单向协议：Alice 在数据流的前一半上运行它，再把内存交给 "
        "Bob。<bookmark mark='b'/>所以任何能回答不相交问题的流式问题，都需要线性内存。<bookmark mark='c'/>精确的不同元素计数、精确的频率矩、精确的最"
        "频繁元素，都这样倒下了。<bookmark mark='d'/>Noga Alon、Yossi Matias 和 Mario Szegedy 在1996年与那些草图算法一起证明了这些界。<bookmark "
        "mark='e'/>HyperLogLog 和 Count-Min 做近似，是因为它们不得不如此。",
    # ------------------------------------------------------------------ Interactive
    "Chapter five. Interactive proofs.": "第5章。交互式证明。",
    "How do you prove that two graphs are different?":
        "怎样证明两个图是不同的？要证明相同，顶点的对应关系就是一份简短的证书。要证明不同，还不知道有什么证书。但一场对话可以做到。<bookmark mark='a'/>"
        "验证者抛一枚硬币，选出两个图之一，打乱它的顶点标号，把结果给证明者看。<bookmark mark='b'/>拥有无限计算能力的证明者说出它来自哪个图。<bookmark "
        "mark='c'/>答案与硬币一致，验证者就接受。<bookmark mark='d'/>如果两个图真的不同，证明者总能分辨，我们诚实的证明者每次都答对了。<bookmark "
        "mark='e'/>如果它们相同，打乱后的图不带有关于硬币的任何信息，证明者只能猜：在我们的两千轮里是百分之四十九。<bookmark mark='f'/>二十轮就能把"
        "虚张声势者的机会压到百万分之一以下。<bookmark mark='g'/>交互证明了一件已知的书面证明都证明不了的事。",
    "The general setting is called IP.":
        "一般的框架叫作 IP。<bookmark mark='a'/>一个多项式时间、会抛硬币的验证者，与一个全能的证明者交换消息。<bookmark mark='b'/>真命题必须以高概率被"
        "接受，<bookmark mark='c'/>假命题必须以高概率被拒绝，不论证明者怎样尝试。<bookmark mark='d'/>Shafi Goldwasser、Silvio Micali 和 Charles "
        "Rackoff 在1985年提出了这个想法，同时提出了一个证明传递多少知识的问题。<bookmark mark='e'/>László Babai 独立地定义了 Arthur-Merlin 博弈，其中"
        "验证者的硬币对证明者公开。<bookmark mark='f'/>Goldwasser 和 Sipser 证明，藏起硬币没有区别。<bookmark mark='g'/>NP 是只有一条消息、没有硬币的"
        "特例。交互还能多给多少？答案在下一章。",
    # ------------------------------------------------------------------ Sumcheck
    "Chapter six. Sum-check and IP equals PSPACE.": "第6章。Sum-check 与 IP 等于 PSPACE。",
    "In 1990 Carsten Lund, Lance Fortnow, Howard Karloff and Noam Nisan found the key idea:":
        "1990年，Carsten Lund、Lance Fortnow、Howard Karloff 和 Noam Nisan 找到了关键想法：把逻辑变成代数。<bookmark mark='a'/>非 x 变成一减 x；与变成"
        "乘法；三个文字的或，变成一减去它们否定的乘积。<bookmark mark='b'/>在零和一上，这个多项式与公式一致，所以满足赋值的个数，就是这个多项式在布尔"
        "立方体上的和。<bookmark mark='c'/>但这个多项式在有限域的任何点上也有定义；我们用模九十七的整数。它在每个变量上的次数至多是子句数，五。<bookmark "
        "mark='d'/>证明者声称这个和是七。<bookmark mark='e'/>验证者没法把二的 n 次方项加起来。下面看它怎样照样检查。",
    "The protocol peels off one variable per round.":
        "协议每轮剥掉一个变量。<bookmark mark='a'/>第一轮，证明者发来一个单变量多项式：让 x 一保持自由，其余变量都对零和一求和。它以六个值的形式发送，"
        "足以确定一个五次多项式。<bookmark mark='b'/>验证者检查它在零和一处的值之和等于声称值七，然后随机取一个域元素，三十，声称值就变成多项式在那里的值："
        "三十三。第二轮把 x 一固定为三十，做同样的事，依此类推。<bookmark mark='c'/>最后一轮之后，验证者在四个随机值处把算术化的公式求值一次，得到九十一，"
        "恰好等于最后的声称值。接受。<bookmark mark='d'/>验证者每轮只做几次域运算，再加一次求值，而不是把二的 n 次方项加起来。",
    "What if the prover lies?":
        "如果证明者撒谎呢？<bookmark mark='a'/>比如它声称是八。它的第一个多项式在零和一处之和必须是八，所以它不是真正的多项式。<bookmark mark='b'/>两个"
        "不同的 d 次多项式至多在 d 个点上相等。<bookmark mark='c'/>所以唯一的希望是，验证者的随机点恰好落在假多项式与真多项式相等的地方；这时谎言就消失了。"
        "这种事发生的概率至多是 d 除以 p。<bookmark mark='d'/>否则，假的声称就带进下一轮；如果它撑过了每一轮，最后的求值会揭穿它。<bookmark mark='e'/>"
        "我们造了最好的作弊者，它的假多项式与真多项式在尽可能多的点上相等。模九十七时，它在三千次运行中存活了百分之十九点三，而界是十九点一。<bookmark "
        "mark='f'/>在一百万元素的域上，它一次也没存活。",
    "This was a breakthrough.":
        "这是一个突破。<bookmark mark='a'/>Sum-check 表明，计数解的个数也有交互式证明，远远超出 NP。<bookmark mark='b'/>几周后，Adi Shamir 把它推广到"
        "量化公式：全称变成乘积，存在变成一减乘积，同样逐轮检查的办法依然管用。<bookmark mark='c'/>一个保持次数很低的技巧让它能通过 n 个量词。<bookmark "
        "mark='d'/>反方向上，最优的证明者可以在多项式空间里模拟。<bookmark mark='e'/>所以 IP 等于 PSPACE：一个带硬币的多项式时间验证者，可以被说服相信"
        "任何能在多项式空间里证明的事，比如从给定局面出发谁能赢一盘棋。<bookmark mark='f'/>而且这个证明不可相对化：存在预言机，相对于它这个结论不成立。"
        "它是第一个越过第26部分第一道障碍的重大技术。",
    # ------------------------------------------------------------------ ZeroKnowledge
    "Chapter seven. Zero knowledge.": "第7章。零知识。",
    "Here is the classic story.":
        "这是一个经典故事。<bookmark mark='a'/>一个山洞呈环形，后面有一扇门，只有念出秘密口令才能打开。<bookmark mark='b'/>Peggy 从两条路之一走进去，"
        "Victor 在外面等着。然后 Victor 喊出她应该从哪条路回来。<bookmark mark='c'/>如果她知道口令，总能照办，必要时打开那扇门。如果不知道，她有一半的时候"
        "会被抓住。<bookmark mark='d'/>二十轮之后，虚张声势者存活的概率是百万分之一。<bookmark mark='e'/>而 Victor 对口令一无所知。他本可以找一个不知道"
        "口令的演员拍出一模一样的视频，只要把失败的回合剪掉。<bookmark mark='f'/>这就是零知识的定义：验证者看到的一切，他都能自己模拟出来。",
    "Oded Goldreich, Silvio Micali and Avi Wigderson showed in 1986":
        "Oded Goldreich、Silvio Micali 和 Avi Wigderson 在1986年证明，通过三着色，NP 中的每个问题都有零知识证明。这是 Petersen 图，证明者知道怎样给它"
        "着色。<bookmark mark='a'/>每一轮，证明者先随机打乱三种颜色，<bookmark mark='b'/>然后对每个顶点的颜色做承诺，这里是公布一个随机数和颜色拼起来的"
        "哈希。之后它不能再改颜色，而哈希不泄露任何信息。<bookmark mark='c'/>验证者指定一条边。<bookmark mark='d'/>证明者打开边两端的两个承诺，<bookmark "
        "mark='e'/>验证者检查两种颜色不同、哈希吻合。然后一切重新开始，换一次新的打乱。",
    "Is it sound?":
        "它可靠吗？<bookmark mark='a'/>我们给一个作弊的证明者一种着色，十五条边中有两条是坏的。<bookmark mark='b'/>只要验证者选中其中之一，它就被抓住。"
        "<bookmark mark='c'/>在两千次运行中，k 轮后仍未被发现的比例服从一减十五分之二的 k 次方：五轮后百分之四十七，二十轮后百分之六。只有一条坏边的"
        "作弊者撑得更久，是一减 m 分之一的 k 次方。<bookmark mark='d'/>三百零一轮能把它也压到十亿分之一以下。",
    "And what does the verifier learn?":
        "那验证者学到了什么？<bookmark mark='a'/>每一轮，它看到一条边两端的两种不同颜色。因为颜色是刚刚打乱的，这一对颜色是均匀随机的。<bookmark "
        "mark='b'/>一个根本不知道任何着色的模拟器，可以产生完全相同的东西：随机挑两种不同的颜色。<bookmark mark='c'/>各六千轮下来，真实记录和模拟记录中，"
        "每一种有序颜色对出现的频率都约为六分之一。<bookmark mark='d'/>验证者能从对话中算出的任何东西，它都能从模拟中算出，所以除了这个图可以着色之外，"
        "它什么也没学到。<bookmark mark='e'/>Amos Fiat 和 Adi Shamir 展示了怎样用对话的哈希代替验证者的硬币，把这类证明变成签名；第30部分会用到它，"
        "今天的区块链也在用。",
    # ------------------------------------------------------------------ Pcp
    "Chapter eight. The PCP theorem.": "第8章。PCP 定理。",
    "Here is the most surprising theorem in this part.":
        "这是这一部分最令人惊讶的定理。<bookmark mark='a'/>任取一个有 NP 证明的命题，比如某个公式可满足。这个证明可以用多项式长度、以一种特殊的稳健"
        "格式重写，使得一个只抛对数多枚硬币、只读其中常数多位的验证者就能检查它。<bookmark mark='b'/>正确的证明总被接受。<bookmark mark='c'/>如果命题是"
        "假的，每一份声称的证明至少有一半的时候被拒绝。<bookmark mark='d'/>这就是 PCP 定理，1992年由 Sanjeev Arora 与 Shmuel Safra，以及 Arora、Carsten "
        "Lund、Rajeev Motwani、Madhu Sudan 与 Mario Szegedy 证明。<bookmark mark='e'/>Johan Håstad 后来证明三位就够了。只要证明写得得法，随机读它的三位，"
        "就和读完全部一样令人信服。",
    "The full proof is long, but its flavour fits in a small experiment.":
        "完整的证明很长，但它的味道可以装进一个小实验。<bookmark mark='a'/>一个八位输入的布尔函数是不是奇偶函数，即某个输入子集的异或？<bookmark "
        "mark='b'/>Manuel Blum、Michael Luby 和 Ronitt Rubinfeld 提出了一个测试：随机取两个输入 x 和 y，检查 f(x) 加 f(y) 是否等于 f(x 异或 y)。"
        "<bookmark mark='c'/>它读三个值，奇偶函数总能通过。<bookmark mark='d'/>我们拿一个奇偶函数，在越来越多的地方把它改坏，并算出测试拒绝的精确概率。"
        "<bookmark mark='e'/>距离小的时候，它服从三 delta 减六 delta 平方，这是 Mihir Bellare 等人证明的界。<bookmark mark='f'/>离每个奇偶函数都很远的"
        "函数经常被抓住。PCP 的构造这样编码证明：每个错误的证明都离每个正确的证明很远，而像这样的测试能发现差别。",
    "In 2005 Irit Dinur gave a new proof, combinatorial and much shorter.":
        "2005年，Irit Dinur 给出了一个新证明，是组合的，而且短得多。<bookmark mark='a'/>把证明看作一个约束图上的赋值。<bookmark mark='b'/>可满足性本身"
        "就给出这样一个图：若公式不可满足，至少一个约束失败：一个约束的间隙。<bookmark mark='c'/>Dinur 证明的每一步把图变成扩展图，也就是第56部分研究的"
        "那种，并用图上的游走代替约束，使违反约束的比例翻倍。<bookmark mark='d'/>第二步再把字母表缩回来，只损失一个常数因子。<bookmark mark='e'/>经过对数"
        "多轮之后，必须有常数比例的约束失败，而图仍是多项式大小：这就是 PCP 定理。<bookmark mark='f'/>一个最初靠繁重代数证明的结果，变成了四十页的组合"
        "论证。",
    # ------------------------------------------------------------------ Approx
    "Chapter nine. Hardness of approximation.": "第9章。近似的困难性。",
    "Why does a statement about proofs matter for algorithms?":
        "一个关于证明的命题，为什么对算法重要？<bookmark mark='a'/>把验证者每一种可能的测试读作对证明各位的一条约束，于是证明就是一个赋值。<bookmark "
        "mark='b'/>若命题为真，某个赋值满足每条约束。<bookmark mark='c'/>若命题为假，每个赋值都违反常数比例的约束。<bookmark mark='d'/>所以一个能分辨"
        "这两种情形、或者在这个间隙之内近似最优比例的算法，就能判定 SAT。Feige、Goldwasser、Lovász、Safra 和 Szegedy 在1991年发现了这个联系，早于定理"
        "本身。",
    "The sharpest example is MAX-3SAT:":
        "最鲜明的例子是 MAX-3SAT：满足尽可能多的三文字子句。<bookmark mark='a'/>给每个变量抛一枚硬币。每个子句只有三个文字都失败时才失败，概率八分之一，"
        "所以随机赋值平均满足八分之七的子句。我们的测量：每次都是百分之八十七点五。<bookmark mark='b'/>Johan Håstad 在2001年证明，在完全可满足的公式上，"
        "哪怕比八分之七好一点点也是 NP 难的。<bookmark mark='c'/>硬币是最优的。<bookmark mark='d'/>当然，在随机公式上，局部搜索能找到满足百分之九十七到"
        "一百的赋值。近似的困难性说的是最坏情况。",
    "For several problems the PCP theorem gives exactly matching limits.":
        "对好几个问题，PCP 定理给出恰好吻合的极限。<bookmark mark='a'/>MAX-3SAT，在八分之七。模二线性方程组，在二分之一：又是随机赋值。集合覆盖，"
        "贪心算法的 ln n 因子无法改进。团，无法在 n 的一减 epsilon 次方之内近似。<bookmark mark='b'/>然后是顶点覆盖，第23部分的简单算法能做到两倍以内，"
        "但已知的困难性只到根号二以下；还有最大割，Goemans 和 Williamson 的半定规划能做到零点八七八，而困难性止于十七分之十六。<bookmark mark='c'/>这些"
        "间隙就是下一章的主题。",
    # ------------------------------------------------------------------ Ugc
    "Chapter ten. The Unique Games Conjecture.": "第10章。唯一博弈猜想。",
    "In 2002 Subhash Khot proposed a conjecture about a simple kind of constraint problem.":
        "2002年，Subhash Khot 就一类简单的约束问题提出了一个猜想。<bookmark mark='a'/>给每个顶点一个从零到 k 减一的标签。每条边要求一端的标签等于另一端"
        "的标签加上某个常数，模 k。一端的标签唯一决定另一端：所以叫唯一博弈。<bookmark mark='b'/>如果每条约束都能满足，有一个简单的算法：固定一个标签，"
        "然后传播。<bookmark mark='c'/>Khot 猜想，把几乎所有约束都能满足的博弈，与几乎没有约束能满足的博弈区分开，是 NP 难的。<bookmark mark='d'/>几乎"
        "可满足，恰恰是传播失效的地方：一条被违反的边就会把标签带偏。",
    "We can watch propagation fail.":
        "我们可以看着传播失败。我们在三千个顶点、九千条边上埋下一种标签，用七种标签，然后改坏比例为 epsilon 的约束。<bookmark mark='a'/>没有改坏时，"
        "从任何顶点传播都满足每条约束。<bookmark mark='b'/>改坏百分之五时，埋下的标签仍满足百分之九十五，但传播只得到八十三：搜索树里每条坏边，都会把它"
        "下面的一切带坏。<bookmark mark='c'/>到百分之二十，传播跌到一半，而随机标签得到七分之一。<bookmark mark='d'/>半定规划好得多，只损失大约 epsilon "
        "乘 log k 的平方根，这是 Moses Charikar 与 Konstantin、Yury Makarychev 兄弟在2006年证明的。<bookmark mark='e'/>猜想说，在常数意义上，没有任何"
        "高效算法能做得更好。",
    "Part 23 met the conjecture's consequences; here is the whole picture.":
        "第23部分见过这个猜想的推论；下面是全貌。<bookmark mark='a'/>如果它成立，顶点覆盖的两倍因子就是最优的，<bookmark mark='b'/>Goemans 和 Williamson "
        "在最大割上的零点八七八也是。<bookmark mark='c'/>Prasad Raghavendra 在2008年证明，它会让同一个半定规划，一举成为每个约束满足问题的最优近似算法。"
        "<bookmark mark='d'/>也有反对它的证据：Sanjeev Arora、Boaz Barak 和 David Steurer 找到了唯一博弈的亚指数算法。<bookmark mark='e'/>还有支持它的"
        "证据：2018年，Subhash Khot、Dor Minzer 和 Muli Safra 证明了二对二定理，一个稍弱的版本，<bookmark mark='f'/>它已经表明顶点覆盖难以近似到根号二"
        "以下。<bookmark mark='g'/>猜想本身仍未解决。",
    # ------------------------------------------------------------------ FineGrained
    "Chapter eleven. Fine-grained complexity.": "第11章。细粒度复杂性。",
    "NP-hardness separates polynomial from exponential.":
        "NP 难把多项式和指数分开。许多实际问题更精细：平方时间真的必要吗？<bookmark mark='a'/>细粒度复杂性用几个猜想来回答。强指数时间假设说，长子句的"
        "可满足性不可能比二的 n 次方快很多。第21部分用它处理了编辑距离。3SUM 猜想说，找出和为零的三个数需要平方时间，它解释了为什么第22部分的许多几何"
        "问题抗拒更快的算法。而全源最短路径猜想覆盖了一族立方时间的图问题。<bookmark mark='b'/>从 SAT 到平方时间问题的联系，是 Ryan Williams 的一个漂亮"
        "技巧。把变量分成两半，把每个半赋值变成一个向量，每个子句一个坐标，如果这一半已经满足该子句，这个坐标就是零。<bookmark mark='c'/>两个向量正交，"
        "当且仅当它们合起来满足每个子句。<bookmark mark='d'/>所以正交向量问题若有真正低于平方的算法，就会打破强指数时间假设。<bookmark mark='e'/>这些问题"
        "不是关于 P 与 NP 的。它们关心的是指数。",
    "We ran the reduction.":
        "我们运行了这个归约。<bookmark mark='a'/>六个随机公式，每个有二十四个变量、一百零一个子句。每一半变量给出四千零九十六个向量，每个子句一个坐标。"
        "<bookmark mark='b'/>在每个公式上，寻找正交对给出的答案都与我们的 SAT 求解器一致。<bookmark mark='c'/>而向量对的个数是四千零九十六的平方，"
        "等于二的二十四次方：恰好是赋值的个数。暴力求解正交向量，就是暴力求解 SAT。<bookmark mark='d'/>所以任何把 N 平方改进一个多项式因子的算法，都会"
        "在可满足性上胜过二的 n 次方。慢的那几行是不可满足的公式，那里每一对都得检查。",
    "Here are the two baselines on this machine.":
        "这是两个基准算法在这台机器上的表现。<bookmark mark='a'/>我们给两个算法喂的都是无解的实例，所以它们必须做完全部工作。<bookmark mark='b'/>n 每"
        "翻一倍，代价约为四倍：平方。四千个向量要十分之六秒；四千个数，四分之三秒。<bookmark mark='c'/>这些猜想很微妙：Allan Grønlund 和 Seth Pettie "
        "在2014年从 3SUM 上削掉了对数因子，所以现在的猜想只要求不存在多项式级的改进。<bookmark mark='d'/>对工程师来说，条件下界是一条停止规则：别再找"
        "更好的指数了，去优化常数、并行或近似吧。",
    # ------------------------------------------------------------------ Parameterized
    "Chapter twelve. Parameterized complexity.": "第12章。参数化复杂性。",
    "Some NP-hard problems are easy when a parameter is small.":
        "有些 NP 难问题在某个参数很小时是容易的。<bookmark mark='a'/>顶点覆盖要找 k 个顶点碰到每条边。任取一条边；它的两端之一必在覆盖中。对这两种选择"
        "分支，再以 k 减一递归。这棵树至多有二的 k 加一次方个节点。<bookmark mark='b'/>在我们四十个顶点的图上，规模为十二的覆盖用了不到八千个节点、八"
        "毫秒；尝试每个十二顶点的集合则意味着五十五亿个。<bookmark mark='c'/>Jonathan Buss 加了一条预处理规则：邻居多于 k 个的顶点必在任何小覆盖中，"
        "取走这些之后，一个“是”实例至多剩下 k 平方条边。<bookmark mark='d'/>所以在搜索开始之前，每个实例都缩成一个规模为 k 的多项式的核。",
    "This is the theory of fixed-parameter tractability, built by Rodney Downey and Michael Fellows.":
        "这就是固定参数可解性的理论，由 Rodney Downey 和 Michael Fellows 建立。<bookmark mark='a'/>如果一个问题能在 f(k) 乘以 n 的多项式的时间内解决，"
        "f 是任意函数，它就是 FPT 的。<bookmark mark='b'/>顶点覆盖是 FPT 的；纪录大约是一点二七的 k 次方。<bookmark mark='c'/>相比之下，团问题是 W[1] 难"
        "的：人们相信它需要 n 的 k 次方。<bookmark mark='d'/>另一个参数，树宽，衡量一个图有多像树。<bookmark mark='e'/>Bruno Courcelle 证明，任何能用"
        "一元二阶逻辑表达的性质，在树宽有界的图上都能在线性时间内检查。<bookmark mark='f'/>着色、哈密顿圈和独立集，在这类图上都变得容易，而许多真实网络"
        "就属于这类图。",
    # ------------------------------------------------------------------ Counting
    "Chapter thirteen. Counting.": "第13章。计数。",
    "NP asks whether a certificate exists.":
        "NP 问的是证书是否存在。<bookmark mark='a'/>Leslie Valiant 在1979年定义了 #P 类：数出证书的个数。<bookmark mark='b'/>有多少个赋值满足这个公式？"
        "第6章的 sum-check 协议正是这样的计数。<bookmark mark='c'/>这是矩阵的两个著名函数。它们只差一个符号。<bookmark mark='d'/>带符号的行列式，用高斯"
        "消元在立方时间内算出。<bookmark mark='e'/>不带符号的积和式，当矩阵只含零和一时，数的是一个二部图的完美匹配。<bookmark mark='f'/>Valiant 证明积和"
        "式是 #P 完全的。找到一个完美匹配很容易，正如第18部分所示；数出它们则和数任何 NP 问题的解一样难。",
    "We timed both on random zero-one matrices, with exact integers.":
        "我们在随机零一矩阵上用精确整数给两者计时。<bookmark mark='a'/>已知最好的积和式算法仍是 Herbert Ryser 1963年的：对列的子集做容斥，大约二的 n 次方"
        "步。<bookmark mark='b'/>n 等于二十时，我们的矩阵有超过两万亿个完美匹配，数完用了二点三秒。<bookmark mark='c'/>同一个矩阵的行列式用了四分之一毫秒，"
        "而二百乘二百的行列式不到一秒。<bookmark mark='d'/>每多两行，积和式的时间约乘以四。一个符号，隔开了多项式与指数。",
    "How much power does counting give?":
        "计数能给出多大的能力？<bookmark mark='a'/>户田诚之助在1991年证明，带 #P 预言机的机器能判定第26部分多项式层级中的一切。一次计数抵得上任意多层交替"
        "量词。<bookmark mark='b'/>Leslie Valiant 和 Vijay Vazirani 证明，随机约束可以隔离出单个解，所以即使对承诺至多有一个解的公式，判定可满足性也是难的。"
        "<bookmark mark='c'/>近似计数弱得多：Larry Stockmeyer 证明它只需要一个 NP 预言机加上随机性。<bookmark mark='d'/>而对非负矩阵的积和式，Mark "
        "Jerrum、Alistair Sinclair 和 Eric Vigoda 在2004年找到了多项式时间的近似，<bookmark mark='e'/>用的是一条对随机匹配采样的马尔可夫链，正是人工智能，"
        "从零搭建第5部分的马尔可夫链蒙特卡罗。<bookmark mark='f'/>还有一个精确的特例：Pieter Kasteleyn 在1961年数出了平面图的完美匹配，办法是巧妙地选择"
        "符号，把积和式变成行列式。",
    # ------------------------------------------------------------------ Average
    "Chapter fourteen. Average case, and one-way functions.": "第14章。平均情形与单向函数。",
    "NP-completeness is about the worst case.":
        "NP 完全性说的是最坏情况。密码学需要在随机实例上就难的问题。<bookmark mark='a'/>这是最受欢迎的测试案例。取一个一千个顶点的随机图，偷偷把其中 k 个"
        "顶点之间的边全部加上。<bookmark mark='b'/>随机图本身就有约两倍 log n 个顶点的团，这里大约二十。<bookmark mark='c'/>所以 k 一旦超过二十，藏起来的"
        "团就是唯一那么大的团，尝试每个顶点集合就能找到它。<bookmark mark='d'/>一个多项式算法，取度数最高的顶点再清理一下，在七十以下什么也找不到，从八十"
        "起每个团都能找到，接近 n log n 的平方根。<bookmark mark='e'/>谱方法改进了常数，可以到根号 n 的任意倍数，但在那之下没人知道多项式算法。<bookmark "
        "mark='f'/>“不存在这样的算法”这个猜想，如今像 SETH 一样被当作假设，用来解释统计和机器学习中的问题为什么有同样的间隙。",
    "Cryptography needs something stronger:":
        "密码学需要更强的东西：一个容易计算、却在随机输入上难以求逆的函数。<bookmark mark='a'/>乘法是经典的候选。<bookmark mark='b'/>把两个四十位的素数"
        "相乘，大约五十纳秒。用 Pollard 的 rho 方法分解它们的乘积，用了半秒。<bookmark mark='c'/>Rho 大约需要 N 的四次方根步，所以每多八位，代价约乘以四。"
        "<bookmark mark='d'/>已知最好的方法，数域筛法，更快，但仍比多项式差：829位的挑战数 RSA-250 在2020年被攻破，用了大约两千七百个核年。<bookmark "
        "mark='e'/>然而没人证明过任何函数是单向的。这样的证明会推出 P 不等于 NP。",
    "This is the bridge to the next acts of the series.":
        "这是通向本系列下几幕的桥梁。<bookmark mark='a'/>Leonid Levin 在1986年开创了平均情形完全性的理论。<bookmark mark='b'/>Johan Håstad、Russell "
        "Impagliazzo、Levin 和 Michael Luby 证明，任何单向函数都能变成伪随机生成器。<bookmark mark='c'/>由此得到私钥加密、签名，以及第7章的承诺："
        "Impagliazzo 的 Minicrypt。第29部分会把它建起来。<bookmark mark='d'/>Miklós Ajtai 找到了格上的问题，其随机实例与最坏实例一样难，<bookmark "
        "mark='e'/>而 Oded Regev 的带误差学习把它变成了能抵御量子计算机的公钥加密，如今已经标准化，见第30部分。<bookmark mark='f'/>没人能做到的，是把密码学"
        "建立在 NP 完全问题之上：Joan Feigenbaum 与 Lance Fortnow，以及 Andrej Bogdanov 与 Luca Trevisan 的结果表明，标准技术做不到。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen. The frontier:": "第15章。前沿：MIP* 等于 RE，以及实践中的证明。",
    "Each new kind of verifier has reached a larger class.":
        "每一种新的验证者都到达了更大的类。<bookmark mark='a'/>读一份证明，得到 NP。<bookmark mark='b'/>用随机硬币询问一个证明者，得到 PSPACE，这是第6章"
        "的定理。<bookmark mark='c'/>1988年，Michael Ben-Or、Shafi Goldwasser、Joe Kilian 和 Avi Wigderson 问：如果有两个证明者，分开审问，就像关在不同"
        "房间里的嫌疑人呢？László Babai、Lance Fortnow 和 Carsten Lund 在1991年证明，这能到达非确定指数时间。它是 PCP 定理的种子。<bookmark mark='d'/>"
        "然后允许证明者共享量子纠缠。2020年，季铮锋、Anand Natarajan、Thomas Vidick、John Wright 和袁浩森证明，这个类一路跳到了 RE。<bookmark mark='e'/>"
        "一个多项式时间的验证者，可以被说服相信某个程序会停机，而这是任何算法都无法判定的问题。",
    "The result reached far beyond complexity theory.":
        "这个结果的影响远远超出了复杂性理论。<bookmark mark='a'/>验证者检验证明者的回答是否呈现只有纠缠才能产生的关联，也就是第53部分描述的那种贝尔"
        "测试。<bookmark mark='b'/>纠缠帮助诚实的证明者，但也帮助作弊者，这正是这类博弈难以分析的原因。<bookmark mark='c'/>关键一步是压缩验证者：一个博弈"
        "检查一个更大的博弈，后者又检查一个更大的，于是一场有限的对话就能为一个无界的计算作证。<bookmark mark='d'/>作为推论，物理学中的 Tsirelson 问题答案"
        "是否定的：量子关联的两种自然数学模型是不同的。<bookmark mark='e'/>而 Alain Connes 1976年的嵌入猜想，算子代数中的一个核心问题，是错的。<bookmark "
        "mark='f'/>一篇关于交互式证明的长篇证明，解决了纯数学中的一个问题。",
    "Meanwhile, interactive proofs went into production.":
        "与此同时，交互式证明投入了生产。<bookmark mark='a'/>配方是：把计算写成电路，把电路变成多项式，用 sum-check 或 PCP 检查它们，用密码学方法对多项式"
        "做承诺，再用对话记录的哈希代替验证者的随机硬币，这是 Amos Fiat 和 Adi Shamir 的技巧。<bookmark mark='b'/>结果是一份几百字节的证明，任何人都能在"
        "几毫秒内检查，不论那个计算有多长。<bookmark mark='c'/>Joe Kilian 和 Silvio Micali 在1990年代看到了这一点；Goldwasser、Kalai 和 Rothblum 在2008年"
        "把委托计算建立在 sum-check 之上。<bookmark mark='d'/>Jens Groth 2016年的系统只需要三个群元素，Zcash 同年就用这样的证明做隐私支付。<bookmark "
        "mark='e'/>Rollup 在别处执行成千上万笔交易，只上传一份证明。<bookmark mark='f'/>零知识虚拟机证明一个完整的 RISC-V 程序被正确执行。<bookmark "
        "mark='g'/>代价在证明者那一方，它仍比直接运行程序慢好几个数量级；让它变快，是一场正在进行的竞赛。",
    "Six open problems.":
        "六个未解问题。<bookmark mark='a'/>随机性是否曾经帮助多项式时间计算，以及能否不先证明电路下界就证明这一点，Kabanets 和 Impagliazzo 证明这几乎无法"
        "回避。<bookmark mark='b'/>唯一博弈猜想是否成立。<bookmark mark='c'/>三个细粒度猜想之间是什么关系：任何两个之间都不知道有归约。<bookmark mark='d'/>"
        "Valiant 的代数版 P 与 NP：积和式是否需要超多项式规模的代数电路？<bookmark mark='e'/>密码学能否建立在 NP 完全问题之上。<bookmark mark='f'/>以及最"
        "简单的测试能有多可靠：线性性测试的精确拒绝曲线，我们在第8章测量了它的开头。<bookmark mark='g'/>这一部分的研究题取第六个问题的一个小而可计算的情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭建了什么。随机复杂性类，放大，以及用数字呈现的 Adleman 定理；由困难得到的伪随机性。让公式塌缩的随机限制，以及相等问题的通信代价。"
        "交互式证明，以及逐步运行的 sum-check，以预测的概率抓住作弊者。零知识，配一个谁也分辨不出真假的模拟器。PCP 定理、线性性测试，以及为什么硬币是 "
        "MAX-3SAT 的最佳近似；唯一博弈猜想。细粒度复杂性与参数化复杂性，计数，以及密码学所需要的平均情形。",
    "Where this comes back.":
        "这些内容在哪里再次出现。第28部分搭建构成 PCP 的编码：Reed-Solomon，它就是多项式求值，以及只读几个符号就能检验的编码。第29部分从单向函数搭建伪"
        "随机生成器。第30部分用 Fiat 和 Shamir 的办法把零知识变成签名，在格上搭建公钥，并概述简洁证明。第53部分会遇到纠缠，以及 MIP* 背后的那个博弈。"
        "第56部分搭建扩展图，Dinur 证明的引擎。而第57部分用类似第14章的密码学假设，说明为什么有些学习问题是难的。",
    "In practice.":
        "实践中。用指纹比较巨大的文件，只要几十位而不是全部。用简洁证明检查你没有亲自运行的计算。用零知识证明你知道一个秘密而不泄露它。把条件下界当作停止"
        "规则。而当一个难题有一个小参数时，先把实例缩成核，再去搜索。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在本部分的笔记里。可以在任何一题上暂停。第五题是动手题：用 Fiat-Shamir 变换做一个非交互的 sum-check 证明。最后一题标了星号，"
        "是研究题：它的一般答案还不知道，笔记里写了从哪里入手。",
    "Next time: errors.":
        "下一次：错误。1947年，Richard Hamming 的周末作业总因坏位而死掉，于是他教机器去纠正它们。多项式，正是驱动 sum-check 的那些，变成了能经受划痕的"
        "编码。Claude Shannon 证明了噪声的代价有多大，而人们花了五十年才达到他的极限。我们会划花一个二维码，再把它的信息找回来。第28部分，纠错码。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分所依据的书籍和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
