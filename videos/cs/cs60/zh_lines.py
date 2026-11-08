"""Chinese narration for cs60: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第60部分：专用硬件"

CHAPTERS = {
    "Hook": "只做一件事的硬件",
    "Scaling": "1. 通用缩放的终结",
    "Roofline": "2. 屋顶线模型",
    "Systolic": "3. 脉动阵列",
    "Dataflow": "4. 哪个数留在原地",
    "Tpu": "5. TPU，以及更少的比特",
    "Gpu": "6. 再访 GPU",
    "Spatial": "7. 空间计算机：数据流、CGRA 与 FPGA",
    "Memory": "8. 在存储器旁边计算",
    "Sparsity": "9. 稀疏与近似",
    "Design": "10. 硬件是怎样设计的",
    "Job": "11. 硬件中的那项任务",
    "Frontier": "12. 前沿：面向语言模型的加速器",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    'f"Here is what things cost on a chip, in energy.':
        "这是芯片上各种事情的代价，用能量来算。<bookmark mark='a'/>把两个八位整数相加，大约要0.03皮焦耳。三十二位加法，0.1皮焦耳。八位乘法，0.2。三十二位浮点乘法，将近4。"
        "<bookmark mark='b'/>现在去取这些数。从芯片上一块小存储器读出六十四位，要10皮焦耳，比上面任何一种运算都贵。从一兆字节的片上存储器读，要100。"
        "<bookmark mark='c'/>而从芯片外的 DRAM 读，要1300到2600：一次读取，相当于多达{round(ratio, -4):,.0f}次八位加法。"
        "<bookmark mark='d'/>通用处理器的大部分能量既不花在运算上，也不花在取数上：它花在取指令、译码和调度指令上，以及在指令之间搬运数据。2010年，Rehan Hameed 和同事测量了一个视频编码器："
        "一块专为这一项工作而造的芯片，用的能量比运行它的通用核心少大约五百倍。",
    "This part's machine is very different from Pebble. <bookmark":
        "这一部分的机器和 Pebble 很不一样。<bookmark mark='a'/>它是一个由16个单元组成的网格，每个单元里只有第4部分的一个乘法器和一个加法器，外加一个累加和。"
        "<bookmark mark='b'/>每个时钟节拍，每个单元把刚收到的两个数相乘，把乘积加到自己的累加和上，再把这两个数传下去：蓝色的从左往右传，紫色的从上往下传。一个矩阵的各行从左边进入，另一个矩阵的各列从上边进入，"
        "每一个都比前一个晚一步，所以工作以一道斜向的波扫过网格。<bookmark mark='c'/>没有程序，不取任何指令，也没有寄存器堆。10个周期之后，网格里就是两个矩阵的乘积，它是一个门一个门地模拟出来的，"
        "并且经过了核对。",
    'f"This is Part 60 of Computer Science, Built.':
        "这是《计算机科学，从零搭建》的第60部分。<bookmark mark='a'/>我们会看到第二幕的免费加速为什么结束了，以及为什么答案是专用化；测量这台机器的屋顶线；用第4部分的乘法器搭一个脉动阵列，"
        "并一个门一个门地模拟它；读懂谷歌 TPU 论文里的数字；再访 GPU、空间计算机、近存计算和稀疏性；最后把那项任务本身变成一个电路，它大约用{1000 * row['seconds']:.0f}毫秒数完三十部小说。",
    # ------------------------------------------------------------------ s02_scaling
    "Chapter one. The end of general-purpose scaling.":
        "第一章。通用缩放的终结。",
    "Part 10 opened with this picture: fifty years of microproces":
        "第10部分以这张图开场：五十年的微处理器，画在对数刻度上。<bookmark mark='a'/>晶体管不断增加，大约每两年翻一番。<bookmark mark='b'/>三十年来，单个线程也随之变快，"
        "<bookmark mark='c'/>时钟频率也一样，每年提高大约三分之一。<bookmark mark='d'/>然后，在2005年前后，电压不再下降，登纳德缩放结束了，时钟频率也停住了：从那以后它就再没增长过。"
        "但花掉晶体管还有第二种方式。与其造出更多通用机器的副本，不如造一台只做一类工作的机器，而且做得浪费少得多。为了看清浪费在哪里，我们来数能量。",
    "Every instruction a general-purpose processor runs goes":
        "通用处理器执行的每条指令，都要走过第7部分流水线的各个流水级。<bookmark mark='a'/>它从指令缓存中取出，被译码，读取它的寄存器，被执行，再把结果写回。"
        "<bookmark mark='b'/>这些流水级里只有一个是我们要它做的工作。按 Mark Horowitz 给出的45纳米芯片的数据，一次三十二位加法要0.1皮焦耳，而仅仅从一块八千字节的小存储器，"
        "也就是一个指令缓存的大小，读出六十四位，就要10皮焦耳。<bookmark mark='c'/>所以把能量中有用的份额写成：运算本身除以全部。<bookmark mark='d'/>除了取指，把其他开销统统扔掉："
        "这个份额只会变大。<bookmark mark='e'/>代入数字：至多大约百分之一。一百份里有九十九份花在组织工作上，而不是做工作。",
    "The way out is not to make the fetch cheaper. It is to make":
        "出路不是让取指更便宜，而是让一条指令做更多的事。<bookmark mark='a'/>如果一次取指驱动 k 次运算，开销就由 k 份分摊，有用的份额就向1攀升。<bookmark mark='b'/>每条指令一次加法，"
        "是百分之一。<bookmark mark='c'/>一条向量指令，也就是第10部分的 SIMD，一次做16次加法：大约百分之十四。<bookmark mark='d'/>现在想象一条指令启动65536次八位乘加，"
        "在一个256乘256个单元的网格上。开销几乎消失了。这个网格不是想象出来的：它就是谷歌的 TPU，而这一部分会搭一个小的。搬运数据也要花能量：那是下一章的内容。",
    "In June 2018 John Hennessy and David Patterson gave their":
        "2018年6月，John Hennessy 和 David Patterson 发表了他们的图灵奖演讲，后来整理成文，题为《计算机体系结构的新黄金时代》。他们的论点是：登纳德缩放已经消失，摩尔定律正在放缓，"
        "剩下的通往大幅提升的道路是领域专用体系结构，理由有四条。<bookmark mark='a'/>第一，它能利用这个领域真正具有的那种并行：一个步调一致的单元网格，没有任何需要协调的东西。"
        "<bookmark mark='b'/>第二，它能管理自己的存储器，有意地填充缓冲区，而不是指望缓存猜对。<bookmark mark='c'/>第三，它用的精度可以不超过工作所需。"
        "<bookmark mark='d'/>第四，它的程序来自领域专用语言，这些语言让并行一目了然。每一条都是这一部分的一章。",
    "Specialization has a price, and Part 10 already named it.":
        "专用化是有代价的，第10部分已经说出了它的名字。<bookmark mark='a'/>加速器只加速它为之而造的那部分工作，比如说比例 f，加速某个倍数 s；其余部分照旧运行。"
        "<bookmark mark='b'/>所以加速比是1除以（1减 f，再加上 f 除以 s）。<bookmark mark='c'/>如果一个程序有十分之九适合加速器，而在那里快50倍，那么整体大约快8倍。"
        "<bookmark mark='d'/>而无论加速器多快，都超不过10倍。只做一件事的芯片，只有当这件事占了工作的大部分时才划算。2013年，谷歌预测，仅仅用神经网络做语音识别，就可能让它的数据中心所需的计算量翻一番，"
        "而神经网络做得最多的，就是矩阵乘法。",
    # ------------------------------------------------------------------ s03_roofline
    "Chapter two. The roofline model.":
        "第二章。屋顶线模型。",
    "Part 9 ended by naming the roofline model; now we derive it,":
        "第9部分最后提到了屋顶线模型；现在我们来推导它，就像 Samuel Williams、Andrew Waterman 和 David Patterson 在2009年做的那样。"
        "<bookmark mark='a'/>一个内核做 F 次浮点运算，在存储器和处理器之间搬运 Q 个字节。处理器每秒至多做 P 次运算；存储器每秒至多送来 beta 个字节。"
        "<bookmark mark='b'/>所以时间至少是 F 除以 P，也至少是 Q 除以 beta。<bookmark mark='c'/>用工作量除以时间："
        "速度至多是 P 与“F 除以 Q 再乘以 beta”两者中较小的那个。<bookmark mark='d'/>F 除以 Q 叫作算术强度，记作 I，也就是每搬运一个字节所做的运算次数。"
        "这个界是 P 与 I 乘 beta 中的最小值：强度低时是一道倾斜的屋顶，强度高时是一道平的屋顶。",
    'f"Intensity is a matter of counting. <bookmark':
        "强度就是数一数。<bookmark mark='a'/>axpy，第52部分最简单的内核，把 y 设为 a 乘 x 加 y。每个元素花两次运算，一次乘法和一次加法，以及24个字节：读 x 和 y，写 y，各8个字节。"
        "强度是十二分之一。<bookmark mark='b'/>规模为 n 的矩阵乘积做2n 立方次运算，却只需要读两个矩阵、写一个：24n 平方个字节。强度是 n 除以12，随 n 增长。"
        "<bookmark mark='c'/>这些是我们要测量的内核。向量内核都在1以下，而最大的矩阵乘积大约在{say(big['intensity'])}。接近这个理想值，正是第9部分的分块要做的事。",
    'f"Now the two roofs of the computer making this':
        "现在来看制作这个视频的这台计算机的两道屋顶。<bookmark mark='a'/>平屋顶：在一个核上，通过 NumPy 的 BLAS 给四种规模的矩阵乘积计时，取最好的：每秒大约{say(P)}吉次运算。"
        "<bookmark mark='b'/>斜屋顶：像 John McCalpin 的 STREAM 基准测试那样，流式处理{say_int(int(bw['array_mb']))}兆字节的数组，大到缓存装不下。"
        "四个内核的结果不一致，相差大约{say(max(bvals) / min(bvals))}倍；屋顶取其中最好的，每秒大约{say(B)}吉字节，而其他几个提醒我们，这是一道乐观的屋顶。"
        "<bookmark mark='c'/>两者相除：屋脊点大约在每字节{say(R)}次运算。一个内核至少要有这么高的强度，限制它的才会是处理器，而不是存储器。",
    "Here is the result, on logarithmic axes. <bookmark":
        "这是结果，画在对数坐标轴上。<bookmark mark='a'/>橙色的线就是屋顶：以我们测得的带宽随强度上升，直到在屋脊点碰上平的峰值。<bookmark mark='b'/>向量内核，"
        "axpy、点积、矩阵乘向量和模板计算，都在最左边，落在斜屋顶上或者它下面：它们的速度由存储器决定。<bookmark mark='c'/>矩阵乘积在屋脊点右边，紧贴在平屋顶下面：它们的速度由处理器决定。"
        "<bookmark mark='d'/>空心圆圈是第52部分对同样三级线性代数的计时，而那个红点就是那项任务本身，用 Python 数词，它的运算量估计为每字节4次。",
    'f"What does the picture tell us? <bookmark':
        "这张图告诉了我们什么？<bookmark mark='a'/>axpy 跑到了它斜屋顶的百分之{say_int(round(100 * pts[axpy]['fraction_of_roof']))}：在这台机器上，"
        "没有什么能让它快很多。模板计算只达到百分之{say_int(round(100 * pts[sten]['fraction_of_roof']))}，因为 NumPy 每做一次加法都要建一个临时数组，"
        "所以搬运的字节比我们数的多得多。<bookmark mark='b'/>矩阵乘积跑得离峰值不远，正如一个高强度的内核应有的样子。"
        "<bookmark mark='c'/>而那项任务比它的屋顶低了大约{say_int(int(round(js['roof_gflops'] / js['gflops'], -2)))}倍。拖住它的既不是存储器，"
        "也不是算术，而是解释器自己的指令，也就是第一章的开销。<bookmark mark='d'/>加速器抬高平屋顶，并把屋脊点推到很远的右边。谷歌的第一代 TPU 每秒做92万亿次运算，存储器每秒34吉字节，"
        "它的屋脊点在每字节大约{say_int(int(round(ridge_tpu, -2)))}次运算附近。只有矩阵乘积这样的工作才能喂饱它。",
    # ------------------------------------------------------------------ s04_systolic
    "Chapter three. A systolic array.":
        "第三章。脉动阵列。",
    'f"Start with what we want to compute. <bookmark':
        "先看我们要计算什么。<bookmark mark='a'/>两个四乘四的矩阵 A 和 B，以及它们的乘积 C。<bookmark mark='b'/>C 的每个元素都是 A 的一行乘以 B 的一列："
        "<bookmark mark='c'/>把对应的数两两相乘，<bookmark mark='d'/>再加起来。{', plus '.join((say_gates(int(p)) for p in prods))}："
        "{say_gates(C[0][0])}。<bookmark mark='e'/>每个元素四次乘加，共十六个元素：N 的立方，一共64次。1978年，"
        "孔祥重（H. T. Kung）和 Charles Leiserson 提出，给每个元素一个自己的单元，让数有节奏地从它身边流过，就像心脏泵出的血液。他们把它叫作脉动阵列（systolic array），"
        "名字来自心跳的收缩。",
    'f"Here is one cell. <bookmark mark=':
        "这是一个单元。<bookmark mark='a'/>第4部分的一个乘法器接收从左边来的八位数 a 和从上边来的八位数 b。一个加法器把乘积加到单元的累加和上，累加和存在第5部分的一个二十四位寄存器里。"
        "另外两个寄存器把 a 和 b 保持一个时钟节拍，再传下去，a 向右，b 向下。<bookmark mark='b'/>用达达树乘法器和 Kogge-Stone 加法器，"
        "这个单元有{say_gates(tr['gates'])}个门，深度是{say_gates(tr['depth'])}。用普通的阵列乘法器和行波进位加法器，它更小，{say_gates(ar['gates'])}个门，"
        "但深度是{say_gates(ar['depth'])}。<bookmark mark='c'/>正如第7部分所示，深度决定时钟，所以我们用树。两种都在4096个随机输入上一个门一个门地核对过。",
    "The trick is in the timing. <bookmark mark='a'/> Row i of A":
        "诀窍在于时序。<bookmark mark='a'/>A 的第 i 行晚 i 个周期进入网格的左边缘，所以数 A i k 在第 i 加 k 个周期进入，再过 j 个周期到达第 j 列。"
        "<bookmark mark='b'/>B 的第 j 列晚 j 个周期进入顶边，所以 B k j 在第 j 加 k 个周期进入，在第 i 加 j 加 k 个周期到达第 i 行。"
        "<bookmark mark='c'/>是同一个周期：必须相乘的两个数总是在正确的单元、正确的时刻相遇。<bookmark mark='d'/>最后一个乘积的三个下标都是 N 减1，在第3N 减3个周期，"
        "所以一次矩阵乘积要3N 减2个周期：对我们的四乘四网格是10个。<bookmark mark='e'/>而且因为单元在第 i 加 j 个周期开始工作，忙碌的单元组成一条条对角线，从左上角扫向右下角。",
    'f"Now watch it run, one clock tick at a time. Each':
        "现在看它运行，一次一个时钟节拍。每个单元显示它的累加和，以及它正在相乘的、来自 A 的蓝色数和来自 B 的紫色数。<bookmark mark='a'/>第一个周期只有角上的单元拿到一对数："
        "{say_gates(A[0][0])}乘{say_gates(B[0][0])}。第二个周期，它的两个邻居开始工作，而角上的单元再加上{say_gates(A[0][1])}乘{say_gates(B[1][0])}。"
        "盯住这个角：<bookmark mark='b'/>{', '.join((say_gates(x) for x in sums))}，它就完成了，而对面的角还没开始。工作的波斜着穿过网格，"
        "亮着的单元总在一条反对角线带上。<bookmark mark='c'/>每个数只从网格外取一次，然后被四个单元依次使用，共四次。这种复用就是第二章的算术强度，做进了导线里。",
    'f"Now the evidence. <bookmark mark=':
        "现在看证据。<bookmark mark='a'/>我们用第4部分的门和第5部分的寄存器，搭了每边2个、4个和8个单元的网格，给每个网格喂16对随机的八位矩阵，并让模拟器一个周期一个周期地走。"
        "<bookmark mark='b'/>每个都恰好用3N 减2个周期完成，而每一个乘积都和 NumPy 的精确整数答案一致。"
        "<bookmark mark='c'/>八乘八的网格有{say_gates(big['gates'])}个门，恰好是64个单元的量：别的什么都没有，没有控制，没有程序计数器。"
        "<bookmark mark='d'/>TPU 的网格每边256个单元，一共65536个。但先说一个这个设计没告诉我们就做出的选择：它让输出保持不动，而让两个输入都移动。这不是唯一的做法。",
    # ------------------------------------------------------------------ s05_dataflow
    "Chapter four. Which number stays put?":
        "第四章。哪个数留在原地？",
    "Every multiply-add in a neural network touches three":
        "神经网络里的每一次乘加都涉及三个数：一个权重、一个输入，以及它们要加到的部分和。<bookmark mark='a'/>第三章的网格把每个部分和留在它的单元里，让两个输入从旁边流过。"
        "这叫输出驻留（output-stationary）。<bookmark mark='b'/>但也可以让权重留下，只加载一次，而让输入横向流过、部分和向下流动。这叫权重驻留（weight-stationary），"
        "谷歌的 TPU 就是这样做的。<bookmark mark='c'/>或者也可以让输入留下。<bookmark mark='d'/>留下来的那个数只从存储器取一次，然后从乘法器旁边的寄存器里反复使用，"
        "而从 DRAM 读一次的能量是一次八位乘法的几千倍。Yu-Hsin Chen、Joel Emer 和 Vivienne Sze 2016年的 Eyeriss 芯片把这几种选择混合起来，让这种搬运最少。"
        "我们来看 TPU 的选择。",
    'f"Here is a weight-stationary grid, at gate level.':
        "这是一个门级的权重驻留网格。<bookmark mark='a'/>首先，用四个周期把权重沿各列向下移入，最后一行先进，直到每个单元都拿到自己的权重，用紫色表示。它们不会再移动。"
        "<bookmark mark='b'/>然后输入从左边流进来，共{say(m)}行，每一行比前一行晚一步。每个单元把流经的输入乘以自己的权重，加上从上面来的部分和，再把结果向下传。"
        "<bookmark mark='c'/>从底边出来的是乘积的一个元素，而下一行输入已经跟在后面了。权重只取了一次，每个用了{say(m)}次；输入流更长的话，它们会被用得更多。",
    "How much of the time is the grid doing useful work?":
        "网格有多少时间在做有用的工作？<bookmark mark='a'/>把它叫作利用率：完成的乘加次数，除以单元数乘以周期数。<bookmark mark='b'/>输出驻留网格在 N 平方个单元上，用3N 减2个周期，"
        "做 N 立方次乘加。<bookmark mark='c'/>约去 N 平方：N 除以3N 减2，它向三分之一下降。对单次矩阵乘积，一个单元有三分之二的时间在等那道波。"
        "<bookmark mark='d'/>权重驻留网格对 M 行输入做 M 乘 N 平方次乘加，用 N 个周期加载，M 加2N 减2个周期计算。<bookmark mark='e'/>再约一次：M 除以 M 加3N 减2。"
        "这个随着输入流变长而趋向1。<bookmark mark='f'/>两个公式都和我们刚才看到的门级模拟完全吻合。",
    "Here are the formulas as curves, with the simulations as":
        "这是画成曲线的公式，模拟结果画成点。<bookmark mark='a'/>输出驻留做单次乘积时，在二乘二网格上从二分之一开始，然后稳定地趋向三分之一。"
        "<bookmark mark='b'/>输入行数与网格列数相同的权重驻留更差，趋向四分之一，因为加载权重本身就要花 N 个周期。<bookmark mark='c'/>但给它一个长的输入流，行数是16倍，"
        "它在每种规模上都升到百分之八十以上。空心圆圈是门级网格，实心点是对更大网格的整数模型，全都落在曲线上。所以，只有当许多输入会经过同样的权重时，才应该让权重留下：在神经网络里，这就是一个批次。",
    # ------------------------------------------------------------------ s05_dataflow
    'f"Finally, the sizes that matter. <bookmark':
        "最后，看真正要紧的规模。<bookmark mark='a'/>对每边16、64和256个单元的网格，整数模型数出每种数据流的周期，把乘积和 NumPy 对照，而每个利用率都恰好等于它的公式。在256时，"
        "一次输出驻留的乘积只让网格三分之一的时间忙碌；带长输入流的权重驻留，超过百分之八十。<bookmark mark='b'/>保持一个权重不是免费的：每个单元需要多路选择器，在加载信号关闭时留住它的权重，在我们的电路里，"
        "每个单元多{say_n(round(e0))}个门。<bookmark mark='c'/>256乘256，权重驻留，用批次喂数据：这就是谷歌从2015年起放进数据中心的张量处理单元（TPU）的核心，也是下一章的主题。",
    # ------------------------------------------------------------------ s06_tpu
    "Chapter five. The TPU, and fewer bits.":
        "第五章。TPU，以及更少的比特。",
    "Google put its Tensor Processing Unit into its data centres":
        "谷歌在2015年把它的张量处理单元放进了数据中心，Norman Jouppi 和同事在2017年描述了它。<bookmark mark='a'/>它是挂在 PCI Express 总线上的协处理器：主机给它发送指令。"
        "<bookmark mark='b'/>它的中心是矩阵乘法单元，一个256乘256个单元的网格，每个单元是一个八位乘法器和一个加法器。<bookmark mark='c'/>权重来自8 GiB 的片外 DRAM，"
        "经过一个队列，从顶部加载进网格，并留在那里。激活值从左边流入，来自一个24 MiB 的缓冲区。<bookmark mark='d'/>三十二位的和从底部离开，经过非线性函数，再回到缓冲区，作为下一层的输入。",
    'f"Where does the paper':
        "论文里那个著名的数字是怎么来的？<bookmark mark='a'/>65536个单元。<bookmark mark='b'/>每个单元每个节拍做一次乘法和一次加法，算作两次运算，每秒7亿个节拍。"
        "<bookmark mark='c'/>乘起来：每秒{say_dec(peak / 1000000000000.0)}万亿次运算，也就是论文里说的92万亿次运算。"
        "<bookmark mark='d'/>除以权重存储器每秒34吉字节的带宽：就得到第二章的屋脊点，每取一个字节大约做{say_int(int(round(ridge, -2)))}次运算。",
    "Put the TPU's roof beside this machine's. <bookmark":
        "把 TPU 的屋顶放在这台机器的屋顶旁边。<bookmark mark='a'/>我们的，实测的，蓝色。<bookmark mark='b'/>TPU 的，橙色：平屋顶高出一千多倍，斜屋顶却几乎没动，"
        "因为它的权重来自普通的 DRAM。屋脊点滑到了很远的右边。<bookmark mark='c'/>论文为谷歌自己的网络画了这张图，其中大多数都在斜坡下面，受存储器限制，而不是受网格限制。"
        "<bookmark mark='d'/>它的头条结论，速度是同时期 CPU 和 GPU 的15到30倍，是真的，但这是一个关于推理、关于八位、关于那些网络的论断。",
    "The grid multiplies eight-bit integers, but weights are real":
        "网格乘的是八位整数，但权重是实数，所以要把它们量化。<bookmark mark='a'/>把每个数写成一个缩放因子 s 乘以一个小整数 q。<bookmark mark='b'/>选取缩放因子，"
        "使张量中绝对值最大的数变成127。<bookmark mark='c'/>然后除以缩放因子，舍入到最近的整数：255个等级之一。<bookmark mark='d'/>对这个向量，1.95决定了缩放因子；除以它之后，"
        "各个数落在等级之间，舍入把每个数挪动一点。<bookmark mark='e'/>从不超过半个台阶：这是第4部分的舍入论证，只是整个张量共用一个指数。",
    'f"Now a dot product, the work of one column.':
        "现在看一个点积，也就是一列的工作。<bookmark mark='a'/>把每个输入和权重都换成它的缩放因子乘以它的整数。<bookmark mark='b'/>缩放因子可以提到求和之外：网格把小整数的乘积加起来，"
        "每个输出再做一次乘法，就恢复了单位。<bookmark mark='c'/>和要多宽？每个乘积至多16129，十六位；256个这样的乘积装得进二十三位。三十二位的累加器不可能溢出。"
        "<bookmark mark='d'/>我们核对过：经过 int8，一个256乘256乘积中最大的和是{say_int(q['max_abs_int32_acc'])}，而用第四章的网格模型跑的一个切片，"
        "给出的正好是整数答案。",
    'f"Is eight bits enough? <bookmark':
        "八位够吗？<bookmark mark='a'/>我们用三种方式把两个随机矩阵相乘，与六十四位浮点数对照。float32 的误差是千万分之几；十六位输入，万分之几；八位，大约百分之一点五。"
        "<bookmark mark='b'/>这听起来很糟，直到你问一个网络需要什么。一个小分类器用 float32 和用 int8，"
        "在五千个测试点中的百分之{say_dec(100 * cl['agreement'])}上给出同样的答案，准确率的变化出现在第四位数字上。<bookmark mark='c'/>再看节省：按 Horowitz 的数据，"
        "一次八位乘法的能量大约是一次 float32 乘法的"
        "{FRACTION.get(int(e['ratios']['fp32_mult_over_int8_mult_energy']), 'a small fraction')}，而在我们自己用第4部分搭的电路里，"
        "门数大约是它的{FRACTION.get(round(g['24']['gates'] / g['8']['gates']), 'a small fraction')}。",
    # ------------------------------------------------------------------ s07_gpu
    "Chapter six. GPUs revisited.":
        "第六章。再访 GPU。",
    "Part 10 met the graphics processor's bargain: thousands of":
        "第10部分见识过图形处理器的交易：成千上万条简单的通道，而不是几个聪明的核心。<bookmark mark='a'/>线程以32个为一组的线程束运行，共用一条指令流。"
        "<bookmark mark='b'/>取一条指令、译码一次，32条通道各做一次乘加：第一章的开销，由32份分摊。<bookmark mark='c'/>代价是分歧。当各条通道在一个分支处意见不一时，"
        "线程束两条路径都要走，并关掉一部分通道。<bookmark mark='d'/>矩阵乘积从不分歧：每条通道都对不同的数做同样的乘加。所以在2017年，NVIDIA 加入了只做这件事的硬件。",
    "NVIDIA's Volta GPU of 2017 added tensor cores. <bookmark":
        "NVIDIA 2017年的 Volta GPU 加入了张量核心。<bookmark mark='a'/>每个张量核心每个时钟周期在四乘四矩阵上计算 D 等于 A 乘 B 加 C：四乘四乘四，一次64次乘加。"
        "<bookmark mark='b'/>每个输出把四个乘积加到它的初始值上，这正是第三章网格中的一个单元在四个节拍里做的事。<bookmark mark='c'/>乘积用十六位浮点数计算，和保持在三十二位：小位宽相乘，"
        "大位宽相加，和 TPU 一样。<bookmark mark='d'/>NVIDIA 没有公开张量核心是怎样连线的，所以这张图只是示意，但思路很清楚：一个小的矩阵乘法块，放在每个多处理器里。",
    "Count the multiply-adds that one instruction buys. <bookmark":
        "数一数一条指令能买到多少次乘加。<bookmark mark='a'/>标量核心：1次。第10部分的向量指令，十六个浮点数宽：16次。一个线程束的乘加：32次。"
        "<bookmark mark='b'/>而一次整个线程束的矩阵步骤，在十六乘十六的分块上：16的立方，4096次。<bookmark mark='c'/>所以把一次乘加的能量写成运算本身，"
        "加上由 n 次运算分摊的指令开销。<bookmark mark='d'/>每条指令四千次运算时，主宰第一章的开销几乎消失，而一块做矩阵工作的 GPU 开始像一个加速器了。",
    'f"Now the memory wall of Part 9, once more.':
        "现在再来一次第9部分的存储墙。<bookmark mark='a'/>这是这台机器实测的屋顶，以及 NVIDIA 数据手册上 Volta V100 的屋顶：普通通道上每秒15.7万亿次三十二位运算，"
        "堆叠存储器每秒900吉字节。<bookmark mark='b'/>张量核心把平屋顶抬高8倍，到125万亿次。但存储器还是那个，"
        "所以屋脊点从每字节大约{say_int(round(r32))}次运算移到大约{say_int(round(rt))}次。<bookmark mark='c'/>第二章的向量内核不管由哪块芯片运行，都在最左边的斜坡上。"
        "更快的算术只会让更多的工作等待存储器。这就是为什么此后的加速器都把算术和芯片旁边的堆叠存储器配在一起，那是第八章的主题；也是为什么另一种办法，复用，一代比一代更重要。",
    'f"How does any kernel climb that slope? By reuse,':
        "任何内核怎样爬上那道斜坡？靠复用，也就是第9部分的分块。<bookmark mark='a'/>为了算出输出的一个 b 乘 b 的分块，一个多处理器通过它的快速存储器读入 A 的一个条带和 B 的一个条带，每次一块。"
        "<bookmark mark='b'/>这个分块需要2b 平方 K 次运算，而条带里有2bK 个数，每个两字节。<bookmark mark='c'/>相除：强度是 b 除以2。分块越大，复用越多。"
        "<bookmark mark='d'/>要达到张量核心的屋脊点，b 必须大约是{say_int(round(need))}。没有哪一级快速存储器能单独做到这一点，所以真实的内核在每一级同时分块，寄存器、共享内存和缓存："
        "第9部分的教训，叠了三层。",
    # ------------------------------------------------------------------ s08_spatial
    "Chapter seven. Spatial machines: dataflow, coarse-grained":
        "第七章。空间计算机：数据流、粗粒度阵列与 FPGA。",
    "Every machine so far, the TPU's grid apart, does its work in":
        "到目前为止的每台机器，除了 TPU 的网格，都是在时间上展开工作的。<bookmark mark='a'/>这是一个小滤波器：每个输出等于3乘这个输入，加上2乘前一个输入。处理器把它作为八条指令，一条接一条地，"
        "通过同一个算术单元来运行，每个结果都是如此。<bookmark mark='b'/>空间计算机则把同样的计算在空间中铺开。每个运算有自己的单元，值沿着导线在它们之间流动，根本不取指令：程序变成了电路。",
    "The oldest spatial idea is dataflow. <bookmark mark='a'/>":
        "最古老的空间思想是数据流。<bookmark mark='a'/>把计算画成一张图，让每个节点在它的全部输入都到达时立刻触发。<bookmark mark='b'/>这里 a 和 b 到了，所以加法马上触发；"
        "减法必须等 d，而 d 来得晚。<bookmark mark='c'/>只有这时乘法才能触发。没有程序计数器：事件的顺序来自数据本身。"
        "<bookmark mark='d'/>Jack Dennis 和 David Misunas 在1975年提出了这样一种处理器，Arvind 在 MIT 的小组在1980年代造出了标记令牌机器。它们从未取代普通处理器，"
        "但第8部分的乱序核就是藏在普通处理器里的一个数据流引擎。",
    "Between the processor and fixed hardware sits the coarse-gra":
        "在处理器和固定硬件之间，是粗粒度可重构阵列，也就是 CGRA。<bookmark mark='a'/>它是一个由小处理单元组成的网格，每个处理单元有一个字宽的算术单元、一个寄存器和一个开关，与邻居相连。"
        "一份配置在数据开始流动之前，一次性地告诉每个处理单元做什么。<bookmark mark='b'/>为了运行这个循环，编译器把图的每个节点放到一个处理单元上。"
        "<bookmark mark='c'/>然后沿着邻居之间的导线为每条边布线。<bookmark mark='d'/>有一个难处：进入加法器的两条路径必须花同样多的周期，所以有一个处理单元什么都不做，只是把一个值传下去。"
        "布局和布线都是困难的搜索问题。",
    "Now let it run. <bookmark mark='a'/> On every tick a new x":
        "现在让它运行。<bookmark mark='a'/>每个节拍进来一个新的 x，每个处理单元都把结果传下去。乘3的乘法器处理这个 x，而乘2的乘法器处理一个更早的 x，它被延迟单元拖后了一个周期。"
        "<bookmark mark='b'/>在第五个节拍，第一个输出到达存数单元，从那以后每个周期离开一个结果，而处理器每个结果要八条指令。<bookmark mark='c'/>这是一条流水线，第7部分的思想，"
        "只不过是用程序本身做成的。",
    "The most flexible spatial machine is the FPGA. <bookmark":
        "最灵活的空间计算机是 FPGA，即现场可编程门阵列。<bookmark mark='a'/>它的基本构件是第3部分的查找表：十六位存储器加一个选择器。四个输入位从十六个条目中选出一个，所以这张表能计算四个输入的任何函数。"
        "这里是奇偶性。<bookmark mark='b'/>装入不同的位，同一张表就计算别的东西，比如是否至少有两个输入为1。<bookmark mark='c'/>FPGA 是这些查找表的海洋，"
        "每张表旁边有一个第5部分的触发器，它们之间是可编程的连线，还有一列列固化的乘法器和存储器。<bookmark mark='d'/>灵活是有代价的。Ian Kuon 和 Jonathan Rose 在2007年测量过："
        "同样的逻辑占用的面积大约是定制芯片的35倍，速度还慢好几倍。",
    "So spatial machines fill a spectrum. <bookmark mark='a'/> At":
        "所以空间计算机铺满了一条光谱。<bookmark mark='a'/>一端是 CPU，能运行任何程序，为每条指令付出代价；另一端是 TPU 这样的固定芯片，用最少的能量做一种工作。"
        "GPU、FPGA 和 CGRA 位于两者之间。<bookmark mark='b'/>2014年，微软在为必应（Bing）搜索结果排序的每台服务器里都放了一块 FPGA，把一个排序阶段的吞吐量提高了将近一倍。"
        "<bookmark mark='c'/>从2017年起，任何人都可以在亚马逊的云上租用 FPGA。<bookmark mark='d'/>而研究用的 CGRA，比如斯坦福的 Plasticine，"
        "把并行模式直接编译到阵列上。每种情况下，难的部分都是编译器，第十章会回到这一点。",
    # ------------------------------------------------------------------ s09_memory
    "Chapter eight. Computing near memory.":
        "第八章。在存储器旁边计算。",
    'f"Chapter one began with Mark Horowitz':
        "第一章从 Mark Horowitz 的表开始。把它换算到单个字节上。<bookmark mark='a'/>两个字节相加要0.03皮焦耳。从算术单元旁边的一块小存储器取一个字节，大约是它的40倍；"
        "从一兆字节的片上存储器取，是400倍。<bookmark mark='b'/>而从芯片外的 DRAM 取：一次六十四位的读取要1300到2600皮焦耳，所以一个字节大约要160到325皮焦耳。"
        "<bookmark mark='c'/>这相当于{say_int(int(ratio_lo))}到{say_int(int(ratio_hi))}次八位加法的能量，只为运进一个字节。对大多数程序来说，算术只是个舍入误差；"
        "账单是为运输开的。",
    "Why should distance cost energy? <bookmark mark='a'/>":
        "为什么距离要花能量？<bookmark mark='a'/>沿导线发送一个比特，就意味着给导线充电，而第10部分给出了这份能量：每次翻转大约是二分之一 C V 平方。"
        "<bookmark mark='b'/>导线的电容随长度增长。<bookmark mark='c'/>所以一个比特的能量随它走过的距离增长。寄存器离算术单元几微米，片上存储器几毫米，而 DRAM 在几厘米之外，"
        "要经过引脚、封装和电路板，那些导线的电容大得多。<bookmark mark='d'/>而且 DRAM 芯片必须打开整整一行存储单元，成千上万个，才能送出被请求的那几个。",
    "The first answer is to bring memory closer. <bookmark":
        "第一种回答是把存储器拉近。<bookmark mark='a'/>传统的 DRAM 内存条离处理器几厘米，隔着电路板，通过一条64根数据线宽的内存通道相连。"
        "<bookmark mark='b'/>高带宽存储器（HBM）在2013年标准化，它把几片 DRAM 晶粒一片叠一片，用穿过硅片的垂直导线把它们连起来，再把这一叠放在处理器旁边的一块硅片上，每叠有1024根数据线，"
        "长度只有几毫米。<bookmark mark='c'/>更短的导线每比特花的能量更少，而且同时工作的导线多得多。第六章的 GPU 就是这样得到每秒900吉字节的，后来的 TPU 也是。但数据仍然得走这一趟。",
    'f"The second answer is bolder: do the arithmetic':
        "第二种回答更大胆：在数据已经在的地方做算术。<bookmark mark='a'/>拿一件简单的活儿来说：把2.5亿个数加起来，一吉字节，分布在 DRAM 的16个存储体上。"
        "<bookmark mark='b'/>处理器必须把每个字节都拉过内存通道，超过10亿个。<bookmark mark='c'/>改为在每个存储体旁边放一个小加法器。每个加法器把自己那份加起来，"
        "只有16个八字节的部分和穿过通道，一共128个字节，少了大约{say_int(round(ratio / 1000000.0))}百万倍。<bookmark mark='d'/>存储体仍然要被读取，所以省下的是这一趟路，"
        "而不是整张账单。这适合复用少的工作：扫描、过滤、求和，也就是屋顶线的左边。UPMEM 在卖这样的存储器，三星在2021年发布了内部带算术的堆叠存储器。",
    "The boldest answer stops moving the weights at all.":
        "最大胆的回答干脆不再搬动权重。<bookmark mark='a'/>把每个权重存成行导线与列导线交叉处一个单元的电导。<bookmark mark='b'/>把输入作为电压加到各行上。根据欧姆定律，"
        "每个单元通过的电流等于它的电导乘以它的电压。<bookmark mark='c'/>再根据基尔霍夫定律，汇聚到一条列导线上的电流相加。<bookmark mark='d'/>所以各列的电流就是一个矩阵与向量的乘积，"
        "由物理一步算出，就在权重存放的地方。<bookmark mark='e'/>难处在于这是模拟的。数值会漂移、有噪声，只值几个比特，而边缘上的转换器本身也要花能量。用相变存储器或阻变存储器做的研究芯片，仍在攻克这个问题。",
    # ------------------------------------------------------------------ s10_sparsity
    "Chapter nine. Sparsity and approximation.":
        "第九章。稀疏与近似。",
    "A trained network is full of zeros. <bookmark mark='a'/>":
        "训练好的网络里满是零。<bookmark mark='a'/>这是剪枝之后的一行权重，以及它遇到的输入。<bookmark mark='b'/>稠密的引擎把每一对都乘一遍：16次乘法，其中11次是乘以零。"
        "<bookmark mark='c'/>便宜的办法是发现零就让乘法器停着不动，这能省能量，但省不了时间。<bookmark mark='d'/>更好的办法是跳过：只送进要紧的那5对，用5步得到同样的和。"
        "<bookmark mark='e'/>这些零是真实存在的。2015年，Song Han 和同事剪掉了 AlexNet 十分之九的权重而不损失准确率，然后造了一个引擎 EIE 来运行这样的网络。",
    "To skip zeros, the hardware must not store them. <bookmark":
        "要跳过零，硬件就不能存储它们。<bookmark mark='a'/>最常见的格式是压缩稀疏行（CSR）：非零值，一行接一行；<bookmark mark='b'/>每个旁边是它的列号；"
        "<bookmark mark='c'/>还有每一行从哪里开始。<bookmark mark='d'/>但下标也要占字节。这里稠密矩阵占24个字节，压缩后的占28个。"
        "<bookmark mark='e'/>有 z 个非零元时，只有当 z 乘以 b 与 c 之和小于 m n b 时，压缩才划算：密度必须低于 b 除以 b 与 c 之和。"
        "<bookmark mark='f'/>对八位的值和十六位的下标，要低于三分之一。而且每一次按列查找，都是从一个分散的地址读取。",
    "Arbitrary zeros make the work unpredictable, so in 2020":
        "任意分布的零让工作变得不可预测，所以在2020年，NVIDIA 的 A100 要求一种模式。<bookmark mark='a'/>把权重切成四个一组，<bookmark mark='b'/>每组保留最大的两个，"
        "其余置零。<bookmark mark='c'/>存下这8个幸存者，每个带一个两位的组内位置。<bookmark mark='d'/>在硬件里，每个位置驱动一个选择器，挑出对应的输入，于是两个乘法器做了四个的工作。"
        "<bookmark mark='e'/>每次都恰好是一半的乘法，每组三十二位变成二十位。剪枝之后要重新训练网络，以恢复它的准确率。",
    "Part 4 rounded to the nearest number. That is the best":
        "第4部分舍入到最近的数。这是最好的单一答案，但它是有偏的。<bookmark mark='a'/>设 x 位于从一个等级 L 到下一个等级 L 加 delta 的路程中、比例为 p 的地方。舍入到最近总是给出 L，"
        "差了 p 乘 delta。<bookmark mark='b'/>随机舍入抛一枚不均匀的硬币：以概率 p 向上，以概率1减 p 向下。<bookmark mark='c'/>期望结果是（1减 p）乘 L，"
        "加上 p 乘（L 加 delta）。<bookmark mark='d'/>展开：L 加 p delta。<bookmark mark='e'/>这正是 x：舍入在平均意义上是精确的。"
        "<bookmark mark='f'/>代价是噪声，方差为 p 乘（1减 p）乘 delta 平方，至多是 delta 平方的四分之一。",
    "Why want noise? <bookmark mark='a'/> Add a quarter of a":
        "为什么想要噪声？<bookmark mark='a'/>给一个存放在粗网格上的数，一次又一次地加上四分之一个台阶。精确的和稳步攀升。<bookmark mark='b'/>舍入到最近会把每个四分之一台阶都舍回去，"
        "所以存储的值永远不动。<bookmark mark='c'/>随机舍入平均每四次向上走一次，于是跟上了这个和。<bookmark mark='d'/>这就是低精度下第23部分的梯度下降：数百万次微小的更新。2015年，"
        "Suyog Gupta 和同事用十六位定点数训练网络，借助随机舍入，达到了三十二位浮点数的效果。",
    # ------------------------------------------------------------------ s10_sparsity
    'f"Approximate computing gives up accuracy on':
        "近似计算有意放弃精度。<bookmark mark='a'/>一个八位乘法器形成64个部分积，每个用一个与门，再按列把它们加起来。<bookmark mark='b'/>去掉最低四列里的那10个部分积，连同它们的加法器。"
        "<bookmark mark='c'/>答案至多差{say(bound)}，<bookmark mark='d'/>不到最大乘积的千分之一。<bookmark mark='e'/>这能接受吗？这取决于谁来读这个答案。"
        "第五章的八位分类器，分数差了大约百分之一，却只在百分之{say_dec(100 * (1 - cl['agreement']))}的点上改变了答案。图像、声音和学习能容忍误差；地址、分支和那项任务的词频不能。",
    # ------------------------------------------------------------------ s11_design
    "Chapter ten. How hardware is designed.":
        "第十章。硬件是怎样设计的。",
    "Chips are not drawn gate by gate. <bookmark mark='a'/> A":
        "芯片不是一个门一个门画出来的。<bookmark mark='a'/>设计者用 Verilog 或 VHDL 这些1980年代的语言写一份寄存器传输级描述，说明每个寄存器在下一个节拍保存什么。"
        "<bookmark mark='b'/>综合把它变成门，布局布线再把这些门排布到硅片上。<bookmark mark='c'/>2012年，伯克利的 Jonathan Bachrach 和同事发布了 Chisel，"
        "一种嵌入在 Scala 中的硬件描述：<bookmark mark='d'/>一个类，用某个位宽运行，就生成那个位宽的乘累加单元。<bookmark mark='e'/>这个系列从第3部分起就是这样工作的。"
        "我们的硬件描述是 Python，而第十一章的哈希级就是一个返回电路的函数。",
    "High-level synthesis starts from ordinary C. <bookmark":
        "高层次综合从普通的 C 开始。<bookmark mark='a'/>这是一个点积，多了一行，要求把循环流水化。<bookmark mark='b'/>工具把每次迭代拆成一次取数、一次乘法和一次加法，"
        "像第7部分的流水线那样让它们重叠，每个周期开始一次新的迭代。<bookmark mark='c'/>256次迭代用258个周期。<bookmark mark='d'/>有一件事不能重叠：每次加法都需要前一个和，"
        "所以加法器必须在一个周期内完成。<bookmark mark='e'/>许多做软件的人就是这样为第七章的 FPGA 编程的，尽管结果在很大程度上取决于 C 是怎么写的。",
    "Generators also changed how chips are planned. <bookmark":
        "生成器也改变了芯片的规划方式。<bookmark mark='a'/>传统的流程是瀑布式的：写规格、设计、花一年验证、做版图，过了好几年才有东西在硅片上跑起来，所以规格里的错误最后才被发现。"
        "<bookmark mark='b'/>2016年，伯克利的 Yunsup Lee、Andrew Waterman、Krste Asanovic 和同事描述了他们 RISC-V 芯片背后的敏捷做法："
        "始终保持一个能工作的设计，以小步修改它，并运行每一个版本，在模拟中或者在 FPGA 上。<bookmark mark='c'/>一路上流片一些小的测试芯片。有了生成器，一种新配置只是改改参数，而不是重写。",
    'f"Choosing among designs is design-space':
        "在多种设计之间做选择，就是设计空间探索。<bookmark mark='a'/>第三章搭了两种乘累加单元。按门数（面积的代理指标）和深度把每一种画出来。树形的有{say_int(tr['gates'])}个门，"
        "深度{say_int(tr['depth'])}；<bookmark mark='b'/>阵列形的，{say_int(ar['gates'])}个门，深度{say_int(ar['depth'])}。"
        "哪一个都不能两头都赢。<bookmark mark='c'/>把深度换算成时钟：每个门10皮秒，再加上寄存器的70皮秒。"
        "<bookmark mark='d'/>树形的周期是{say_int(int(tr['depth'] * gps + ffps))}皮秒，"
        "阵列形的是{say_int(int(ar['depth'] * gps + ffps))}皮秒。<bookmark mark='e'/>把面积乘以每个结果的时间，树形的赢了，大约好五分之一。"
        "真实的工具会扫过成千上万个这样的点。",
    'f"One knob moves a design further than any other:':
        "有一个旋钮比其他任何旋钮都更能改变设计：比特数。<bookmark mark='a'/>我们把同一个树形乘法器分别做成八位，用于 int8；十一位，也就是十六位浮点数的有效数；以及二十四位，三十二位浮点数的有效数。"
        "<bookmark mark='b'/>一个 n 乘 n 位的乘法器形成 n 平方个部分积，所以它应该按 n 平方增长。<bookmark mark='c'/>把每个门数除以 n 平方：每次都是大约6.5。"
        "<bookmark mark='d'/>三倍的位宽要花{say_int(round(g['24']['gates'] / g['8']['gates']))}倍的门，而深度只是缓慢增长。这就是第五章支持八位的理由，"
        "表示成设计空间中的一个点。",
    'f"Co-design chooses the algorithm and the hardware':
        "协同设计把算法和硬件放在一起选择，我们自己的单元就是一个例子。<bookmark mark='a'/>它的词哈希是 Daniel Bernstein 的，乘以33。<bookmark mark='b'/>33是32加1，"
        "<bookmark mark='c'/>而乘以32是一次移位，在硬件里只是改一下连线。所以哈希级就是两个加法器，{say_int(hs['gates'])}个门。"
        "<bookmark mark='d'/>同样的手法贯穿这一部分：为八位网格量化的网络；为张量核心做的四选二剪枝；bfloat16，谷歌的格式，用更少的比特得到 float32 的范围；"
        "还有 Tri Dao 2022年的 FlashAttention，它把模型的算术重排成能放进片上存储器的分块，又是第9部分的分块。",
    # ------------------------------------------------------------------ s12_job
    "Chapter eleven. The Job in hardware.":
        "第十一章。硬件中的那项任务。",
    'f"Here is the Job as a circuit, taking one byte on':
        "这是做成电路的那项任务，每个时钟节拍接收一个字节。<bookmark mark='a'/>第一级判断这个字节是不是字母，并给出它的五位编码。<bookmark mark='b'/>第二级维护这个词的滚动哈希："
        "33乘以哈希值，加上编码，用第4部分的两个加法器完成。<bookmark mark='c'/>一个词结束时，第三级把哈希折叠成一个十二位的下标，并把整个哈希值保留下来作为标签。"
        "<bookmark mark='d'/>第四级读出表中的那个条目，比较标签，加1，再写回去。<bookmark mark='e'/>各级之间的寄存器让四级同时工作，各自处理不同的字节，就像第7部分的流水线。"
        "<bookmark mark='f'/>总共{say_int(tm['gates'])}个门和{say_int(tm['flip_flops'])}个触发器，外加那张表。",
    'f"How fast can it tick? <bookmark':
        "它的节拍能有多快？<bookmark mark='a'/>分类要{say_int(st['classify']['depth'])}个门延迟，哈希要{say_int(st['hash']['depth'])}个，"
        "发出要{say_int(st['emit']['depth'])}个，计数要{say_int(st['count']['depth'])}个。<bookmark mark='b'/>但计数还要读表，"
        "而一次存储器读取要1纳秒，比所有逻辑加起来还长。<bookmark mark='c'/>所以周期是读表，加上19个门延迟，再加上寄存器：1260皮秒，"
        "大约{say_int(round(tm['clock_mhz']))}兆赫。<bookmark mark='d'/>关键路径是读表。单看逻辑，可以跑到3吉赫：账单又一次是为存储器开的。",
    "Now feed it the opening of Pride and Prejudice. <bookmark":
        "现在把《傲慢与偏见》的开头喂给它。<bookmark mark='a'/>It 的 I 进来了，一个周期之后，第一级保存着它的编码，9。<bookmark mark='b'/>哈希每个周期增长一个字母。"
        "<bookmark mark='c'/>空格结束了这个词；它的哈希移到第三级，变成一个下标和一个标签，<bookmark mark='d'/>在第五个周期，第四级把计数1写进那个槽。"
        "<bookmark mark='e'/>与此同时，下一个词已经在被哈希了。<bookmark mark='f'/>现在快一点：truth、universally、acknowledged，"
        "每个词都在它最后一个字母之后四个周期被计数，每个周期一个字节，从不停顿。",
    'f"Is it right? <bookmark mark=':
        "它对吗？<bookmark mark='a'/>我们把整个第一章，用这个单元的八个副本，一个门一个门地跑了一遍，并把一切都和软件比较。<bookmark mark='b'/>离开第三级的每个哈希都和软件的一样。"
        "<bookmark mark='c'/>每张表里存的，都恰好是表的模型所说应有的内容。<bookmark mark='d'/>前二十名和软件版那项任务的结果一字不差。"
        "<bookmark mark='e'/>而每个词要么被计数，要么丢失。有{say_int(r['inexact_words']).capitalize()}个词少计了：每张表每个下标只有一个槽，从不去别处找，"
        "所以槽已被占的词就存不下，而溢出寄存器会记下这一点。",
    'f"How big must the table be? For the thirty novels':
        "表要多大？对三十部小说，我们把它从四千个条目扫到四百万个。<bookmark mark='a'/>丢失的出现次数从一百多万降到三千以下，<bookmark mark='b'/>没能精确计数的词也随之减少。"
        "<bookmark mark='c'/>第17部分的生日论证用两个数就能预测这条曲线：n 个词放进 m 个槽，一个槽保持空着的概率大约是 e 的负 n 除以 m 次方，"
        "<bookmark mark='d'/>而超出已占用槽数的每个词都会少计。<bookmark mark='e'/>预测的误差在百分之几以内。在一百万个条目，也就是七兆字节时，"
        "这个单元丢掉百分之{say_dec(pct)}的出现次数，而前二十名是精确的。直接映射的表会丢词；第17部分的探测法不会，代价是多花周期。",
    "For more speed, use more units. <bookmark mark='a'/> Cut the":
        "要更快，就用更多的单元。<bookmark mark='a'/>在词的边界处把文本切成若干路，每一路有自己的单元和表，最后把各张表合并。<bookmark mark='b'/>一路处理三十部小说要31毫秒；四路要8毫秒；"
        "十六路，两毫秒多一点。<bookmark mark='c'/>六十四路大约1毫秒，但这时合并比读取更花时间：这是第一章的阿姆达尔定律。<bookmark mark='d'/>而且六十四路每秒需要23吉字节的文本，"
        "几乎是这台机器的存储器能送出的全部：又是屋顶线的斜坡。",
    'f"The ledger gets row twenty-one. <bookmark':
        "账本有了第二十一行。<bookmark mark='a'/>一个数词单元，以{say_int(round(row['clock_mhz']))}兆赫的频率每个周期处理一个字节，大约31毫秒数完三十部小说，"
        "是迄今最快的一行。<bookmark mark='b'/>第17部分在 Pebble 上的哈希表，每个字节大约花29个周期；这个电路只花1个，因为它根本不取指令。"
        "<bookmark mark='c'/>两条诚实的保留意见：文本必须每个周期送来一个字节，而一张七兆字节的表在1纳秒内应答，是乐观的。算术现在几乎是免费的；剩下的，又一次，是搬运数据。",
    # ------------------------------------------------------------------ s13_frontier
    "Chapter twelve, the frontier. Why does generating text one":
        "第十二章，前沿。为什么一次生成一个词的文本，会让一块芯片的大部分都闲着？",
    'f"The newest accelerators are built for language':
        "最新的加速器是为语言模型造的，而第二章的屋顶线解释了它们最难的问题。<bookmark mark='a'/>这是2022年一块数据中心 GPU 的屋顶线：每秒将近一千万亿次十六位运算，"
        "但它的存储器每秒只能送来{GPU_TBS}太字节，所以它的屋脊点大约在每字节{ridge:.0f}次运算。<bookmark mark='b'/>要生成一个词元，一个有 P 个参数的模型大约做2P 次运算，"
        "并且读一遍它的每一个权重，2P 个字节。这就是每字节一次运算。<bookmark mark='c'/>只服务一场对话时，芯片大约跑在它峰值的百分之{100 * att(1) / GPU_TFLOPS:.1f}。"
        "同时服务许多场对话，就能让每次读取的权重在整个批次中复用，那个点就沿着屋顶向上滑。<bookmark mark='d'/>每一种补救都又是存储墙：把用户凑成批；把权重量化到八位或四位，又是第4部分的浮点数；"
        "用一个小模型猜几个词元，再用大模型跑一遍来检验；还有，正如 Tri Dao 和同事在2022年用 FlashAttention 展示的，重排注意力的计算，让它留在片上存储器里。",
    "The largest models do not fit on one chip, and the frontier":
        "最大的模型装不进一块芯片，而前沿在于怎样把芯片组合起来。<bookmark mark='a'/>Cerebras 用一整片硅晶圆做成了一个处理器，它的存储器分散在几十万个核心之间，还有备用核心，好让布线绕开制造缺陷。"
        "<bookmark mark='b'/>其他大多数厂商走了相反的路：芯粒（chiplet），把几片小晶粒放在一个封装里，用又短又密的导线连接；它们的良率比一片巨大的晶粒更好，还能混用不同的制造工艺。"
        "<bookmark mark='c'/>而存储器被堆成一座座 DRAM 晶粒的塔，就放在处理器旁边，又宽又近，加速器的带宽就来自这里。<bookmark mark='d'/>这三者都是第八章那场战斗，只是规模更大："
        "缩短每个字节必须走的距离。",
    "Open problems. <bookmark mark='a'/> Placing and wiring":
        "开放问题。<bookmark mark='a'/>给几十亿个晶体管布局和布线，至今仍靠启发式方法，而学习出来的布局能否胜过它们，还有争议。<bookmark mark='b'/>正确性证明，第54部分那一种，"
        "用于整个加速器，而不只是一个单元。<bookmark mark='c'/>一个编译器，能把任意循环嵌套映射到单元网格上，做得和专家手工一样好。<bookmark mark='d'/>还有，"
        "让大模型的服务速度取决于它们的算术，而不是它们的存储器。<bookmark mark='e'/>这一部分的研究题回到了卵石。1981年，洪加威和孔祥重用一个红蓝卵石游戏，"
        "证明了经典的矩阵乘法必须在一个小而快的存储器和一个大而慢的存储器之间搬动多少个字。为一个单元网格找出同样的界，其中每个单元有自己的小存储器，并找出一种达到这个界的数据流。",
    # ------------------------------------------------------------------ s14_outro
    "What we built in this part. A roofline, measured on this":
        "我们在这一部分搭建了什么。一道在这台机器上实测的屋顶线，它告诉我们一个内核是在等算术还是在等存储器。一个用第4部分的门搭成的、会乘也会加的单元，以及由它们组成的网格，以一道斜向的波做矩阵乘法，一个门一个门地验证过。"
        "两种数据流，以及各自挣得的利用率。TPU 的交易：八位的乘积和三十二位的和，只花一小点能量。GPU、空间计算机、会计算的存储器，以及稀疏性，它们都是少搬字节的办法。还有做成电路的那项任务，每个周期数一个字节。"
        "贯穿始终的是一个想法：当免费的加速结束时，速度来自让机器适合工作。",
    "Where this comes back. The roofline was measured once, on":
        "它们会在哪里再出现。屋顶线只在一台机器上测了一次，而第61部分，也就是最后一部分，讲的是怎样测量才不会骗了自己。这一部分的开放问题，会在那里和其他所有开放问题一起汇集到一张地图上。而账本，"
        "连同这一部分的电路给出的第二十一行，会被最后读一次。",
    "In practice. Put each kernel on the roofline before you":
        "在实践中。优化一个内核之前，先把它放到屋顶线上，这样你就知道自己在哪道天花板下面。对循环分块，让每个取来的值被使用许多次。把推理量化到八位，并在真实数据上检查准确率，而不是在基准测试上。"
        "只把稠密、规整、并且大到足以抵消传输代价的工作交给加速器。还要剖析数据的搬运，而不只是算术。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：给数词单元加上线性探测，让它不再因为冲突而丢词，并测量这在门数和时钟速度上的代价。最后一道标了星号，是一道研究题："
        "洪加威和孔祥重的卵石游戏，在一个由小存储器组成的网格上玩。",
    "Next time, Part 61, the last part of the series: doing":
        "下一次，第61部分，也是这个系列的最后一部分：做研究。这个系列引用的每一个结果都是某个人做出来的。当一个没用到的环境变量的大小都能改变程序的速度时，你怎样测量才不会骗了自己？你怎样读一篇论文、找到一个问题，"
        "并知道它什么时候算解决了？而我们遇到的那些开放问题，在一张地图上处在什么位置？",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
PHRASES.update({"an eighth": "八分之一", "a ninth": "九分之一", "a tenth": "十分之一", "an eleventh": "十一分之一",
                "a twelfth": "十二分之一", "a sixteenth": "十六分之一", "a seventeenth": "十七分之一",
                "an eighteenth": "十八分之一", "a nineteenth": "十九分之一", "a twentieth": "二十分之一",
                "a small fraction": "一小部分"})
