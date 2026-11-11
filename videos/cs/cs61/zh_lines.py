"""Chinese narration for cs61: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第61部分：做研究"

CHAPTERS = {
    "Hook": "结果从哪里来",
    "Research": "1. 什么是研究",
    "Bias": "2. 测量偏差",
    "Rigor": "3. 严谨地测量",
    "Benchmarks": "4. 基准测试与可复现性",
    "Proof": "5. 作为研究的证明",
    "Reading": "6. 阅读与评审",
    "Problems": "7. 寻找问题",
    "Writing": "8. 写作",
    "Frontier": "9. 开放问题地图",
    "Bridges": "10. 几个系列交汇的地方",
    "Pebble": "11. 最后一次看石子",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    'f"Here is one C program, compiled once, timed on':
        "这是一个 C 程序，只编译一次，在这台机器上计时。<bookmark mark='a'/>每次运行之间，我们唯一改变的，是一个程序从来不读的环境变量的大小，从空的到4千字节。<bookmark mark='b'/>"
        "中位时间的变动最多达到百分之{100 * b['env_spread']:.0f}。2009年，Todd Mytkowicz 和同事们表明，这样的改变会移动栈的起始位置，连带改变热点数据的对齐，而单是这一点，"
        "就可能决定两种编译器设置里哪一种看起来更快。<bookmark mark='c'/>但我们看到的这个波动，是那种效应，还是只是噪声？这台机器每次运行都会随机化栈的起始位置，这会把效应抹平；第二章会表明，"
        "单凭噪声就足以解释我们看到的东西。把这两者区分开，并且不骗自己，就是这一部分要讲的。",
    "This series has quoted perhaps a thousand results. Where do":
        "这个系列大概引用了上千个结果。它们是从哪里来的？<bookmark mark='a'/>每一个都始于一个问题，它尖锐到答案有可能是错的。<bookmark mark='b'/>然后是一种方法：一个证明、一次测量，"
        "或者造出来的某个东西。<bookmark mark='c'/>然后是证据，好到足以说服一个巴不得你出错的怀疑者。<bookmark mark='d'/>最后是一篇论文，写出来让别人能够检验。最后这一部分，"
        "讲的就是你自己怎样做到这些。",
    "This is Part 61 of Computer Science, Built, the last part":
        "这是《计算机科学，从零搭建》的第61部分，也是这个系列的最后一部分。<bookmark mark='a'/>我们会重现测量偏差；用区间和重复，严谨地给事情计时；看看基准测试是怎样失效的；用证明和计算机搜索来解决猜想，"
        "或者至少解决它们的小情形；学习阅读、评审、寻找问题和写作；最后把这个系列遇到过的开放问题汇集到一张地图上。",
    # ------------------------------------------------------------------ s02_research
    "Chapter one. What research is.":
        "第一章：什么是研究。",
    "Research begins with a question, but not just any question.":
        "研究始于一个问题，但不是随便什么问题。<bookmark mark='a'/>环境会影响速度吗？照这样问，没有任何实验能回答说不。<bookmark mark='b'/>把它磨尖：哪个变量，哪个程序，哪台机器，"
        "和什么相比。现在答案两种都有可能，正是这一点让它值得一问。<bookmark mark='c'/>一个尖锐的问题变成一个假设；假设给出一个预测；而一次检验去核对这个预测。<bookmark mark='d'/>"
        "如果检验本可以驳倒它，却没有驳倒，这个假设就存活下来，暂时如此。如果它被驳倒了，你就学到了东西，然后带着一个更好的假设回来。1934年，哲学家 Karl Popper 把这一点当作科学主张的标志："
        "某个观察有可能证明它是错的。一个你已经知道答案的问题不是研究，一个任何结果都无法反驳的主张也不是。",
    "Computer science answers questions with three kinds of":
        "计算机科学用三种证据来回答问题。<bookmark mark='a'/>第一种是证明：从公认的公理出发的一串步骤，比如第25部分里图灵1936年的证明：没有任何程序能判定停机。读者检查每一步，或者，从第54部分起，"
        "由证明助手来检查。<bookmark mark='b'/>第二种是实验：一次受控的、重复进行的比较，比如这一部分核心的测量偏差研究。当别人再做一遍并得到同样的答案时，它就得到了检验。"
        "<bookmark mark='c'/>第三种是构造：把东西造出来，并表明它能工作，比如 Dennis Ritchie 和 Ken Thompson 1974年关于 Unix 的论文，"
        "Unix 就是第31部分背后的系统。当别人使用它、而它经得住考验时，它就得到了检验。<bookmark mark='d'/>大多数论文把这三种混在一起：造一个系统，测量它，再加一条关于它为什么能工作的定理。"
        "一篇论文主张什么，决定了它欠读者哪种证据。",
    "Results travel as papers, and papers have a shape.":
        "结果以论文的形式传播，而论文有固定的形状。<bookmark mark='a'/>标题和作者；摘要；引言；背景；想法或设计；评估，或者证明；相关工作；结论；以及参考文献。顺序因领域而异，但这些部分反复出现。"
        "<bookmark mark='b'/>摘要用大约四句话讲完整个故事：背景、问题、我们做了什么，以及我们发现了什么。<bookmark mark='c'/>其余每一部分，回答每个读者、"
        "也是每个审稿人都会问的三个问题之一。它重要吗？这是引言的任务：问题是什么，为什么重要，再加一份贡献清单。<bookmark mark='d'/>它对吗？这是评估或证明的任务，并且要说明它们的局限。"
        "<bookmark mark='e'/>它新吗？这是相关工作的任务：已经知道了什么，以及这篇论文究竟增加了什么。第六章会带着这些问题去读论文。",
    "Where do papers go? In most sciences, to journals. Computer":
        "论文发到哪里？在大多数科学里，发到期刊。计算机科学与众不同。<bookmark mark='a'/>它的主要发表场所是严格筛选的会议。一篇论文要赶一个固定的截止日期，由程序委员会的三名或更多成员审读，"
        "作者可以写一份简短的答辩（rebuttal），几个月之内论文就被接收或拒绝，然后在报告中宣讲，并印进会议论文集。<bookmark mark='b'/>许多会议历史悠久：操作系统原理研讨会始于1967年，"
        "理论研讨会 STOC 始于1969年，程序设计语言研讨会 POPL 始于1973年；许多会议的接收率不到四分之一。<bookmark mark='c'/>期刊的运作方式不同：随时可以投稿，"
        "然后经过一轮又一轮的审稿和修改，可能要花几个月甚至几年。在计算机科学里，期刊上登的常常是会议论文更长、更完整的版本，而预印本会先出现在 arXiv 上。<bookmark mark='d'/>2009年，"
        "Lance Fortnow 主张，这个领域应该长大，重新转向期刊。争论仍在继续。",
    '''f"Here is this part's own experiment, written as''':
        "这是这一部分自己的实验，按一篇论文的写法写出来。<bookmark mark='a'/>问题：一个没用到的环境变量，或者链接的顺序，会不会改变这台机器上一个 C 程序的运行时间？"
        "<bookmark mark='b'/>方法：{say(sizes)}种大小，每种运行{say(reps)}次，交错进行；{say(len(B['link']))}种链接顺序，"
        "每种运行{say(link_runs)}次；把中位数和每次运行之间的噪声相比较。<bookmark mark='c'/>证据：在各种大小之间，"
        "中位数相差大约百分之{say(100 * B['env_spread'])}；在各种链接顺序之间，相差不到百分之一，两者都在噪声范围之内。<bookmark mark='d'/>效度威胁，"
        "这是诚实的论文从不跳过的一节：一台共享的机器，一个程序，一个编译器，并且地址随机化是开着的。<bookmark mark='e'/>结论：这里没有显示出效应，而这和没有效应不是一回事。下一章会把这个实验拆开来看。",
    # ------------------------------------------------------------------ s03_bias
    "Chapter two. Measurement bias.":
        "第二章：测量偏差。",
    "Why would a variable nobody reads matter? <bookmark":
        "一个没人读的变量，为什么会有影响？<bookmark mark='a'/>Linux 启动一个程序时，会把环境字符串和参数复制到新栈的最顶端，然后是指向它们的指针，只有在这些下面，程序自己的栈帧才开始。"
        "<bookmark mark='b'/>所以环境里每多一个字节，都会把每一个栈帧往下推。把一个热点局部变量的地址写成：栈顶，减去环境，再减去其他所有东西。<bookmark mark='c'/>"
        "调用约定让栈保持16字节对齐，所以这个地址以16字节为一步移动。<bookmark mark='d'/>在第9部分讲过的一个64字节的缓存行里，它可以落在4个位置上，<bookmark mark='e'/>"
        "而在一个4千字节的页里，可以落在256个位置上。一个跨越两个缓存行的对象，要访问两次；而一次读取，如果它的地址和前面某次存储的地址在低12位上相同，就可能被处理器拦住，因为处理器起初只比较这几位。你碰到哪种情况，"
        "取决于环境。",
    'f"Here is the first experiment from the hook':
        "这又是开场的第一个实验，这次多给出一些我们测到的东西。<bookmark mark='a'/>对{say(len(ENV))}种环境大小中的每一种，从空的到4千字节，每步{say(STEP)}字节，"
        "我们把程序运行{say(B['reps'])}次，交错进行，让机器里缓慢的变化平均地落在每一种设置上。黄色的点是中位数；它们相差大约百分之{say(100 * B['env_spread'])}。"
        "<bookmark mark='b'/>蓝色的点是每{say(B['reps'])}次里最快的一次；它们相差大约百分之{say(100 * MIN_SPREAD)}。<bookmark mark='c'/>"
        "现在看右边：紧接着，又对一个不变的设置，也就是空环境，运行了{say(len(ONE))}次。它们的范围是百分之{say(100 * ONE_RANGE)}，"
        "是全部中位数波动的{say(ONE_RANGE / B['env_spread'])}倍。在把任何事归咎于栈之前，我们得先知道机器自己会动多少。",
    'f"The second experiment changes nothing in the':
        "第二个实验不改源代码里的任何东西，只改交给链接器的三个目标文件的顺序。<bookmark mark='a'/>链接器按这个顺序排布代码，所以每个函数都落到一个新地址上。这会改变热循环与处理器取指令所用的块怎样对齐，"
        "也会改变它的分支共用分支预测器的哪些表项。<bookmark mark='b'/>这是每种顺序各运行{say(len(LINK[0]['runs']))}次的结果，环境为空。中位数相差不到百分之一，"
        "远远落在各次运行的散布之内。<bookmark mark='c'/>在这台机器上，对这个小循环，链接顺序没有显示出我们能检测到的效应。这和没有效应不是一回事：一个比噪声还小的效应，看起来恰恰就是这样。",
    "This is what Todd Mytkowicz, Amer Diwan, Matthias Hauswirth":
        "这正是 Todd Mytkowicz、Amer Diwan、Matthias Hauswirth 和 Peter Sweeney 2009年在 ASPLOS 上报告的，论文标题是《没做任何明显的错事，"
        "却产生了错误的数据》（Producing Wrong Data Without Doing Anything Obviously Wrong）。<bookmark mark='a'/>"
        "他们在试过的每一种处理器和两种编译器上，以及大多数 SPEC CPU2006 的 C 程序里，都发现了测量偏差。改变环境大小或链接顺序，就可能改变编译器的 O3 设置看起来是否比 O2 更快。"
        "在他们调查的一百多篇近期论文中，没有一篇充分考虑到了这一点。<bookmark mark='b'/>他们提出了两种补救办法。设置随机化：在许多随机选择的设置下测量，报告分布，而不是一个碰巧的点。"
        "<bookmark mark='c'/>以及因果分析：当你认为一个效应有某个原因时，只改变那个原因，并检查效应是否随之而来。<bookmark mark='d'/>2013年，"
        "Charlie Curtsinger 和 Emery Berger 做出了 Stabilizer，它在程序运行时不断地重新随机化内存布局。",
    'f"So what does our measurement show? <bookmark':
        "那么，我们的测量说明了什么？<bookmark mark='a'/>假设起作用的只有噪声。从{say(len(POOL))}次空环境的运行中，抽出{say(len(ENV))}个中位数，"
        "每个取{say(B['reps'])}次运行，测量它们的波动，再把这个过程重复4000次。<bookmark mark='b'/>单凭噪声，通常就会给出大约百分之{say(100 * NULL_MED)}。"
        "我们的百分之{say(100 * B['env_spread'])}稳稳地落在其中。<bookmark mark='c'/>我们已经表明：当一个没用到的变量增大时，"
        "中位数变动了百分之{say(100 * B['env_spread'])}；在不同的链接顺序之间，变动不到百分之一。<bookmark mark='d'/>我们没有表明是环境造成了这个变动。而且，"
        "有一个理由让它可能根本没有起作用：在这台机器上，地址随机化是开着的，Linux 每次运行都让栈从不同的位置开始，以16字节为一步。我们核对过："
        "一个很小的 C 程序在{say(stk['runs'])}次运行中打印出了{say(stk['distinct'])}个不同的地址。这相当于替我们做了一次设置随机化，它把对齐效应抹进了每一种设置的噪声里。要找到原因，"
        "你得把它关掉，再去干预。",
    # ------------------------------------------------------------------ s04_rigor
    "Chapter three. Measuring rigorously.":
        "第三章：严谨地测量。",
    'f"We ran the Job in plain Python {say(N)} times':
        "我们用普通的 Python，在同一份文本上把那项任务运行了{say(N)}次，文本大约有{say(T['bytes'] / 1000000.0)}百万个字符。<bookmark mark='a'/>每个点是一次运行。"
        "它们之间什么都没变，可它们还是散开了。<bookmark mark='b'/>报告最好的那次，你声称的是{ms(TIMES.min())}；报告最差的那次，你声称的是{ms(TIMES.max())}，"
        "慢了百分之{say(100 * (TIMES.max() / TIMES.min() - 1))}；平均值是{ms(TIMES.mean())}。<bookmark mark='c'/>2007年，"
        "Andy Georges、Dries Buytaert 和 Lieven Eeckhout 调查了 Java 性能论文怎样报告计时，发现许多论文只给出一个数，几次运行中最好的一次，或者一个平均值，"
        "却没有任何衡量它有多不确定的指标。<bookmark mark='d'/>他们表明，这样的方法可能会误导人，甚至会搞错两个系统哪一个更快；他们主张改用重复运行和置信区间。",
    'f"Georges and his colleagues also separated two':
        "Georges 和同事们还区分了两个问题。<bookmark mark='a'/>一个带即时编译器的运行时，比如第15部分的那个，开始时很慢，在解释执行，随着它编译热点代码而变快。启动性能是最初几次迭代的时间："
        "要测量它，就把运行时启动许多次，给每次的第一次迭代计时。<bookmark mark='b'/>稳态性能是预热之后的时间：在每次运行内部，反复迭代，直到计时稳定下来，对这些取平均，而且仍然要在几次全新的运行之间重复，"
        "因为每次运行编译代码的方式都可能略有不同。<bookmark mark='c'/>这是我们的那项任务，按运行顺序排列。我们用的 Python 没有即时编译器，计时也没有显示出任何趋势："
        "最慢的是第{say(slow)}次运行。这里的关键不是预热，而是机器自己的噪声。",
    'f"How sure is a mean? The textbook formula':
        "一个平均值有多可靠？教科书上的公式假定计时服从钟形曲线。自助法（bootstrap）是 Bradley Efron 1979年提出的想法，它的假定要少得多。<bookmark mark='a'/>"
        "从我们的{say(N)}次运行和它们的平均值开始。<bookmark mark='b'/>现在把这个样本当作整个世界：从中有放回地随机抽取{say(N)}次运行，这样有些会出现两次，有些一次也不出现，"
        "再取这个重抽样本的平均值。<bookmark mark='c'/>再做一次，再做一次；每个重抽样本给出的平均值都略有不同。<bookmark mark='d'/>经过几千次重抽样，这些平均值形成一个分布，"
        "它中间的95%，就是一个95%置信区间：这里是从{ms(clo)}到{ms(chi)}。同样的办法也适用于中位数，或者两个程序时间的比值，这些情形手头都没有现成的教科书公式。",
    '"How many runs are enough? <bookmark':
        "要运行多少次才够？<bookmark mark='a'/>这是在我们运行了{', '.join((say(w['runs']) for w in NARROW[:-1]))}和{say(w1['runs'])}次之后"
        "的自助法区间。它在变窄：{say(w0['runs'])}次运行之后，宽{say(1000 * (w0['hi'] - w0['lo']))}毫秒；{say(w1['runs'])}次之后，"
        "宽{say(1000 * (w1['hi'] - w1['lo']))}毫秒。<bookmark mark='b'/>为什么是这个速度？独立运行的方差可以相加，所以 n 次运行的平均值的方差，"
        "等于一次运行的方差除以 n。<bookmark mark='c'/>开平方：平均值的散布按 n 的平方根分之一下降。<bookmark mark='d'/>区间大约有四个这样的量那么宽，所以要把它减半，"
        "你需要四倍的运行次数。虚线就是这个预测，而我们的区间跟着它走。<bookmark mark='e'/>还要注意，中心在漂移。这个公式假定你测量的时候机器不变；而一台共享的机器会变，"
        "这就是我们为什么要把各种设置交错进行，也是为什么一个区间的诚实程度，只能和这个假定一样。",
    "Last, how to average speedups. <bookmark mark='a'/> Two":
        "最后，怎样对加速比取平均。<bookmark mark='a'/>两个程序，两个基准测试：A 在第一个上用1秒，在第二个上用4秒；B 在每个上都用2秒。<bookmark mark='b'/>"
        "用 B 的时间除以 A 的时间，再取平均：1.25，所以 B 慢了四分之一。反过来，用 A 的除以 B 的，再取平均：也是1.25，所以 A 慢了四分之一。两者不可能都对。<bookmark mark='c'/>"
        "几何平均数是这些比值之积的 n 次方根。<bookmark mark='d'/>把每个比值都倒过来，它也恰好倒过来，所以无论你按哪个方向相除，无论你以哪台机器为基准做归一化，它给出的结论都一样。"
        "<bookmark mark='e'/>取对数之后，它就是普通的平均值，快一倍和慢一倍在这里相互抵消。这里它给出的是1：打平。Philip Fleming 和 John Wallace 在1986年提出了这个论证。"
        "<bookmark mark='f'/>但要看清它没有说什么：把两个基准测试各跑一次，B 在4秒内跑完，A 要5秒。对一个固定的工作负载，总时间才是诚实的概括。",
    # ------------------------------------------------------------------ s05_benchmarks
    "Chapter four. Benchmarks and reproducibility.":
        "第四章：基准测试与可复现性。",
    "A benchmark is a promise: a program whose speed stands for":
        "基准测试是一个承诺：一个程序，它的速度代表你所关心的那些程序的速度。<bookmark mark='a'/>Reinhold Weicker 1984年的 Dhrystone 很小，而且是人工合成的。"
        "它能整个放进缓存，它的大部分时间花在少数几个字符串操作上，编译器和库可以专门针对它来调优。<bookmark mark='b'/>由计算机制造商在1988年创立的 SPEC 联盟，改用真实的程序，"
        "并且每隔几年就更换一次它的测试套件。<bookmark mark='c'/>然而它的第一套测试里包含了 matrix300，一个矩阵乘法。正如 Hennessy 和 Patterson 所讲述的，"
        "编译器学会了把它变换得如此彻底，以至于它只测量了那一个技巧，于是它在下一套里被去掉了。<bookmark mark='d'/>后来，2006年套件里的 libquantum 声名狼藉，"
        "编译器给它带来的加速远远超过其他程序；2017年的套件里已经没有它了。每一次，分数上去了，而人们实际运行的程序却没有。",
    "Economists have a name for this. <bookmark mark='a'/> In":
        "经济学家给这种现象起了个名字。<bookmark mark='a'/>1975年，Charles Goodhart 观察到，一种统计规律一旦被用作控制的杠杆，往往就会失效；"
        "人类学家 Marilyn Strathern 后来把它表述为：当一个度量成为目标，它就不再是一个好的度量。<bookmark mark='b'/>一个基准测试开始时，是对我们想要的东西的度量：真实的程序跑得快。"
        "把分数变成目标，力气就会流向任何能抬高分数的东西，包括专门针对基准测试本身的调优。<bookmark mark='c'/>分数不断上升，而真实的程序不再跟着它走。<bookmark mark='d'/>"
        "有时这是故意的。2013年，人们发现有几款手机在识别出基准测试应用时会提高时钟频率；2015年，人们发现大众的柴油车能检测到排放测试，只在那时才排放得更干净。",
    "SPEC's answer to Goodhart is a careful score and strict":
        "SPEC 对 Goodhart 的回答，是一种精心设计的分数和严格的规则。<bookmark mark='a'/>用一台固定的参考机器所用的时间，除以每个基准测试的时间，得到一个越大越好的比值。"
        "<bookmark mark='b'/>分数是这些比值的几何平均数，也就是第三章的那种平均。<bookmark mark='c'/>把两台机器的分数相除，参考时间就约掉了，所以排名不取决于选了哪台参考机器。"
        "<bookmark mark='d'/>然后是规则。基础（base）结果必须对同一种语言的每个基准测试使用同一组编译器选项；峰值（peak）结果可以逐个调优。每个结果都要公开它的硬件、软件和编译选项，"
        "并在 SPEC 发布之前经过审查。而当一个基准测试失效时，它会随下一套测试被淘汰。",
    # ------------------------------------------------------------------ s05_benchmarks
    'f"The same pressure acts on researchers.':
        "同样的压力也作用在研究者身上。<bookmark mark='a'/>在运行和结论之间，有许多合理的选择：用平均值、中位数，还是最快的一次；要不要剔除离群值；展示哪些基准测试。2011年，"
        "Joseph Simmons、Leif Nelson 和 Uri Simonsohn 在心理学中表明，随意组合这些选择，几乎能让任何东西看起来都显著；"
        "Andrew Gelman 和 Eric Loken 把它叫作“小径分岔的花园”。<bookmark mark='b'/>一个在5%水平上的诚实检验，每20次会误报1次，另外19次保持安静。"
        "<bookmark mark='c'/>在 k 次独立尝试中，全部保持安静的概率是这个数的 k 次方，<bookmark mark='d'/>所以至少误报一次的概率是1减去它，<bookmark mark='e'/>"
        "尝试20次时，大约是百分之{say(100 * P_ANY)}。<bookmark mark='f'/>在系统研究中，拿我们最快的环境大小和最慢的相比，你就从一个程序从来不读的变量那里，"
        "得到了百分之{say(100 * GAIN)}的加速。补救办法是：在看到结果之前就定好分析方法，报告每一个基准测试和每一次运行，并且把设置随机化。",
    "The last defence is to let others check. <bookmark":
        "最后一道防线，是让别人来检验。<bookmark mark='a'/>ACM 区分了三个层次。如果同一个团队用同样的设置再次得到某个结果，它就是可重复的（repeatable）；"
        "如果另一个团队用作者的制品（artifact）得到它，它就是可复现的（reproducible）；如果另一个团队用自己的一套设置得到它，它就是可复制的（replicable）。<bookmark mark='b'/>"
        "2016年，Christian Collberg 和 Todd Proebsting 报告说，他们尝试获取并构建数百篇系统论文背后的代码；其中许多，他们都做不到。<bookmark mark='c'/>"
        "从2011年起，许多会议开展了制品评估：一个委员会运行作者的代码和数据，论文可以因制品而获得徽章，分别表示制品可以获取、能够工作，以及结果已被复现。<bookmark mark='d'/>这个系列遵守同样的规则。"
        "屏幕上每一个测量出来的数，都由代码库里的代码计算出来，存进缓存，并能用一条命令重新计算，这样任何人都能检验它。",
    # ------------------------------------------------------------------ s06_proof
    "Chapter five. Proof as research.":
        "第五章：作为研究的证明。",
    "A conjecture is a statement someone believes and nobody has":
        "猜想是有人相信、却还没有人证明的命题。<bookmark mark='a'/>1742年，Christian Goldbach 和莱昂哈德·欧拉在通信中得出了这样一个猜想：每个大于2的偶数都是两个素数之和。"
        "<bookmark mark='b'/>接着是证据：到2014年，它已经对直到4乘10的18次方的每个偶数核对过，而它仍然是一个猜想。<bookmark mark='c'/>它只能以两种方式离开这种状态。"
        "一个反例驳倒它，就像1966年一次计算机搜索驳倒了欧拉的一个猜想。<bookmark mark='d'/>或者一个证明让它成为定理，就像1976年的四色问题，见第18部分。<bookmark mark='e'/>"
        "然后，证明本身也要被检查：2005年，由一个证明助手完成。",
    'f"What does a search prove? <bookmark':
        "一次搜索能证明什么？<bookmark mark='a'/>这是我们的 Goldbach 检查，简化过的：先用筛法筛出素数，然后依次对每个素数，划掉它能补成的那些偶数。到最后，什么都不剩。"
        "<bookmark mark='b'/>这次运行证明了一条定理：从4到200万的每个偶数，都是两个素数之和。有限多个情形，每一个都核对过。<bookmark mark='c'/>改动一个符号，改成任意大小，"
        "它就成了 Goldbach 猜想，而任何搜索都够不着它。<bookmark mark='d'/>搜索给你的，是对余量的感觉。200万以下最难的情形是{say(G['worst'])}，"
        "它只需要{say(G['worst_p'])}，也就是第{say(WORST_RANK)}个素数；而一个反例，需要小于 n 的一半的每个素数都失败。",
    'f"Our Collatz check is cleverer than it looks.':
        "我们的 Collatz 检查比看上去更巧妙。<bookmark mark='a'/>偶数减半，奇数乘3再加1。从7出发，路径爬升到52，然后落到5。<bookmark mark='b'/>程序在那里就停了，"
        "因为每个小于7的起点都已经到达1。<bookmark mark='c'/>这就是第2部分的强归纳法：假设对每个更小的起点结论都成立；<bookmark mark='d'/>证明从 n 出发的路径会降到 n 以下；"
        "<bookmark mark='e'/>那么结论对 n 也成立。计算机对每个小于{lim}的 n 证明了这一步，所以每个小于{lim}的起点都会到达1。<bookmark mark='f'/>"
        "对每一个 n 证明这一步，就是整个 Collatz 问题。",
    "Search shines when a conjecture is false. <bookmark":
        "搜索在猜想为假的时候最能大显身手。<bookmark mark='a'/>1769年，欧拉猜想，要至少 k 个 k 次方数才能加起来等于一个 k 次方数：三个立方数，四个四次方数，五个五次方数。"
        "<bookmark mark='b'/>所以四个五次方数之和永远不应该是一个五次方数。<bookmark mark='c'/>1966年，Leon Lander 和 Thomas Parkin 用计算机搜索，"
        "找到了这样的四个数。<bookmark mark='d'/>核对一下：27、84、110和133，各自的五次方。<bookmark mark='e'/>它们的和恰好是144的五次方。他们的短文只有几行长；"
        "它不需要别的东西。<bookmark mark='f'/>四次方的情形在1988年被攻破：Noam Elkies 找到了一个反例，而 Roger Frye 的搜索找到了最小的那个。",
    "Sometimes the small cases lie. <bookmark mark='a'/> Give":
        "有时候，小情形会撒谎。<bookmark mark='a'/>给每个数一个符号：如果它的素因数个数是奇数，重复的也算在内，就记负1；如果是偶数，就记正1。12是2乘2乘3：负1。"
        "<bookmark mark='b'/>素数得负1；4，也就是2乘2，得正1。<bookmark mark='c'/>维持一个累计和。它在2、4、6、10和16处碰到0，而从不升到0以上。"
        "<bookmark mark='d'/>George Pólya 猜想它永远不会升到0以上。<bookmark mark='e'/>1958年，Brian Haselgrove 证明了这个猜想是错的，"
        "却没有找到在哪里失败；1980年，Minoru Tanaka 找到了第一个失败点，在9亿600万附近。一次到200万的搜索，会让这个猜想看起来确定无疑，而第一个失败点，还远在这个范围的四百多倍之外。",
    'f"Each way of checking a proof asks you to trust':
        "每一种检查证明的方式，都要你信任不同的东西。<bookmark mark='a'/>第2部分用两行、靠鸽巢原理证明了：六个人里，要么有三个人彼此认识，要么有三个人彼此陌生。你信任的是论证和读它的人。"
        "<bookmark mark='b'/>第2部分还用穷举法检查了全部32768种着色。四色定理、Thomas Hales 1998年对开普勒猜想的证明，以及第26部分那个两百太字节的证明，都是这样做的："
        "你信任的是一个程序、它的编译器和机器。<bookmark mark='c'/>证明助手检查每一步推理，你只需要信任它的内核，在第54部分里是{say(LCF['kernel_lines'])}行。"
        "四色定理在2005年就是这样检查的，开普勒猜想则由 Hales 的 Flyspeck 项目在2014年检查完毕。<bookmark mark='d'/>一条定理的可靠程度，只等于你所信任的东西里最不可靠的那一个。",
    # ------------------------------------------------------------------ s07_reading
    "Chapter six. Reading and reviewing.":
        "第六章：阅读与评审。",
    "In 2007 Srinivasan Keshav published a short note called How":
        "2007年，Srinivasan Keshav 发表了一篇短文，题为《如何阅读一篇论文》（How to Read a Paper）。它的建议是分三遍读。<bookmark mark='a'/>第一遍用五到十分钟："
        "标题、摘要和引言；各节的标题，但不看下面的内容；结论；再扫一眼参考文献。这足以决定要不要继续读。<bookmark mark='b'/>第二遍最多用一个小时。除了证明和细枝末节，什么都读，而且要仔细读图："
        "坐标轴标了吗？有误差线吗？每张图显示的，是正文所声称的东西吗？把你没读过的参考文献标出来。<bookmark mark='c'/>第三遍留给你必须完全理解、或者要评审的论文。Keshav 的指示是重新创造这项工作："
        "做出和作者一样的假设，把它重建出来，再加以比较。对初学者来说，这可能要花许多个小时。",
    "The first pass ends with five questions, which Keshav calls":
        "第一遍读完时，要回答五个问题，Keshav 称之为五个 C。这里有一篇摘要，可以拿来试一试。它是虚构的，只为说明问题。<bookmark mark='a'/>类别（Category）：这是哪一类论文？一篇系统论文："
        "一种新设计，加上测量。<bookmark mark='b'/>背景（Context）：它建立在哪些别的论文和哪些理论之上？第17部分的哈希表，以及一节我们还没读的相关工作。<bookmark mark='c'/>"
        "正确性（Correctness）：这些假设看起来成立吗？光看摘要，你还说不准。<bookmark mark='d'/>贡献（Contributions）：它增加了什么？一种设计和一次加速。"
        "<bookmark mark='e'/>清晰度（Clarity）：它写得好吗？很简短，但有些地方含糊。五分钟之后，你就知道要不要读下去，以及读的时候要找什么。",
    'f"In the second pass, look for what is not said.':
        "第二遍读的时候，要找那些没说出来的东西。把主张再读一遍，一个短语一个短语地读，问问自己需要什么才会相信它。<bookmark mark='a'/>“在三十部小说上”：哪些文本？三十部小说只是文本的一个样本，"
        "而第四章已经展示了基准测试是怎样失效的。<bookmark mark='b'/>“快2.1倍”：来自多少次运行，区间是多少？我们自己的那项任务，在同一份文本上运行{say(len(TIMES))}次，"
        "波动了百分之{say(RUN_SPREAD)}。而如果有好几个输入，加速比是怎样取平均的？<bookmark mark='c'/>“比标准计数器”：哪一个，由谁调优，在哪台机器上？在第二章里，"
        "一个没用到的环境变量让我们的中位数变动了百分之{say1(ENV_SPREAD)}。<bookmark mark='d'/>“额外内存很少”：少是多少？一个形容词站在了本该是数字的位置上。"
        "<bookmark mark='e'/>还要注意完全缺失的东西：局限、效度威胁、代码。当一篇论文没有说出自己的任何弱点时，审稿人就得自己去找。",
    'f"The third pass is the hardest, and the one that':
        "第三遍最难，也最能教会你东西。<bookmark mark='a'/>这一部分在第二章做过一次，对象是 Todd Mytkowicz、Amer Diwan、"
        "Matthias Hauswirth 和 Peter Sweeney 2009年的论文：链接顺序和环境的大小会让测量产生偏差。<bookmark mark='b'/>重建会逼着每一个没说出口的选择暴露出来。哪个程序？"
        "哪台机器，有多忙？多少种大小，多少次运行？<bookmark mark='c'/>每一个问题我们都得自己回答，而我们找到了一个答案：{say(len(B['env']))}种大小，"
        "每种运行{say(B['reps'])}次，波动百分之{say1(ENV_SPREAD)}，在噪声之内。<bookmark mark='d'/>还有一个光靠阅读永远不会提出的问题：栈每次运行都从同一个地址开始吗？"
        "在这台机器上不是。<bookmark mark='e'/>所以，这次重建并没有驳倒那篇论文。它发现，论文自己提出的补救办法，设置随机化，早就开着了。",
    "Reviewing is reading with a duty attached. Most review":
        "评审，是带着责任的阅读。大多数评审表要的都是同样几样东西。<bookmark mark='a'/>首先是一份概述，用你自己的话写，让作者能看出你理解了他们。<bookmark mark='b'/>然后是优点："
        "说出哪里好，而且要真心实意。<bookmark mark='c'/>然后是缺点，这里的功夫在于把致命的和可以修补的分开，而对每一个可修补的缺陷，要说出怎样修补。评判的是投来的这篇论文，而不是你自己会写的那篇。"
        "<bookmark mark='d'/>然后是作者能回答的问题。<bookmark mark='e'/>还有一个评定，以及你对它有多大把握。评审是保密的，而且是写给一个人看的：具体、礼貌、可检验。"
        "Alan Jay Smith 1990年给审稿人写的指南《审稿人的任务》（The Task of the Referee），至今仍然值得一读。",
    # ------------------------------------------------------------------ s08_problems
    "Chapter seven. Finding problems.":
        "第七章：寻找问题。",
    "In 1986 Richard Hamming, who spent three decades at Bell":
        "1986年，在贝尔实验室工作了三十年的 Richard Hamming 做了一次演讲，题为《你和你的研究》（You and Your Research）。其中最有名的故事是关于午饭的。"
        "<bookmark mark='a'/>Hamming 和化学家们坐在一起，问他们这个领域的重要问题是什么。一个星期后，他问他们正在研究哪些重要问题。再后来又问：如果你做的事情不重要，你为什么要做它？"
        "<bookmark mark='b'/>他对“重要”的含义很讲究。<bookmark mark='c'/>他说，时间旅行、瞬间传送和反重力，意义会极其重大，但它们不是重要问题，因为我们没有下手的办法。"
        "<bookmark mark='d'/>一个问题之所以重要，是因为它意义重大，而你又能看到一条进去的路。<bookmark mark='e'/>他观察到，伟大的科学家脑子里总装着十到二十个这样的问题，"
        "一旦有个新想法和其中某一个有关，他们就放下别的事情，去追它。",
    "Hamming said that knowledge and productivity are like":
        "Hamming 说，知识和产出就像复利：两个能力差不多的人，一个多努力百分之十，一辈子下来，产出会是另一个的两倍多。<bookmark mark='a'/>把这个比喻当真，当作一个示意："
        "在已有的基础上每年增长百分之十，n 年之后，比值就是1.1的 n 次方。<bookmark mark='b'/>它什么时候等于2？<bookmark mark='c'/>取对数：n 乘以1.1的对数，等于2的对数。"
        "<bookmark mark='d'/>所以 n 大约是0.693除以0.095：七年多一点。<bookmark mark='e'/>这次演讲还讲了别的习惯：把门开着，好接住打扰带来的线索；"
        "把星期五下午留给伟大的思考。",
    "George Pólya's How to Solve It, from 1945, is a short book":
        "George Pólya 1945年的《怎样解题》（How to Solve It）是一本讲怎样找到解法的小书。<bookmark mark='a'/>它分四个阶段：理解问题，拟定计划，执行计划，以及回顾。"
        "<bookmark mark='b'/>为了拟定计划，它给出了一些问题。你知道一个相关的问题吗？一个特殊情形，或者一个更一般的情形？你能画个图吗，或者倒着推？<bookmark mark='c'/>"
        "Pólya 自己的例子：用一个4夸脱的桶和一个9夸脱的桶，恰好打上来6夸脱的水。从目标出发。<bookmark mark='d'/>大桶里的6，是9减3。<bookmark mark='e'/>小桶如果已经装着1，"
        "就恰好能再装进3。<bookmark mark='f'/>而1是9减4，再减4。<bookmark mark='g'/>把这条链正着读：那就是解法。第2部分搜索了一个水壶问题的每一个状态；倒着推则不需要搜索。",
    'f"A limit study measures the headroom before you':
        "极限研究在你花上好几年去追逐提升空间之前，先把它测出来。<bookmark mark='a'/>第7部分问过：在那项任务上，分支预测最好能有多好。两位计数器每一百个分支预测错{say1(w0)}个；"
        "我们9千字节的 TAGE，错{say1(w1)}个。<bookmark mark='b'/>完全没有存储限制时，错{say1(w2)}个。所以单靠存储，每一百个大约能再多赢回三个，剩下的需要另一类预测器。"
        "<bookmark mark='c'/>阿姆达尔定律就是一行字的极限研究：把工作中比例为 p 的部分加速 s 倍。<bookmark mark='d'/>让 s 无限增大，收益的上限就是1除以（1减 p）。"
        "<bookmark mark='e'/>那项任务有百分之99.7的指令花在一次线性查找上，所以去掉它，最多能快{say(AM['job_limit'])}倍。<bookmark mark='f'/>"
        "账本表明这个提升空间是真实存在的：第13部分要{say(R13['seconds'])}秒，用上第17部分的哈希表后，不到1秒。",
    'f"Working backwards scales up to research: start':
        "倒着推可以放大到研究上：从理想出发，问问是什么挡在路上。<bookmark mark='a'/>对缓存来说，理想是已知的。1966年，Laszlo Belady 描述了它：逐出在未来最晚才会被用到的那个块，"
        "没有任何策略的缺失比它更少。<bookmark mark='b'/>挡在路上的是：未来是未知的。<bookmark mark='c'/>所以问题就是从过去预测复用，而每一种策略，从最近最少使用开始，"
        "都可以用它离理想有多近来衡量。<bookmark mark='d'/>那项任务也是如此：理想是每个字节只碰一次，而第60部分用硬件做到了这一点，大约{say(1000 * R60['seconds'])}毫秒。"
        "第17部分的哈希表在每个字节上大约花{say(CPB17)}个周期，所以问题就是减少每个字节的工作量。<bookmark mark='e'/>理想告诉你成功值多少，障碍点出问题是什么，"
        "而 Hamming 的检验问的是：你有没有下手的办法。",
    # ------------------------------------------------------------------ s09_writing
    "Chapter eight. Writing.":
        "第八章：写作。",
    'f"Writing up research is making an argument, and':
        "把研究写出来，就是在构造一个论证；1958年，哲学家 Stephen Toulmin 画出了论证的形状。拿这一部分第二章自己的结果来说。<bookmark mark='a'/>主张（claim）"
        "是你想让读者接受的东西：一个没用到的环境变量，没有可测量地改变程序的速度。<bookmark mark='b'/>数据（data）是它所依据的事实：在{say(len(B['env']))}种大小上，"
        "每种运行{say(B['reps'])}次，中位数相差百分之{say1(ENV_SPREAD)}。<bookmark mark='c'/>依据（warrant）说明这些数据为什么支持这个主张：单凭噪声，"
        "根本没有那个变量，也会给出这么大的波动。<bookmark mark='d'/>支撑（backing）说明依据为什么成立：4000次模拟实验。<bookmark mark='e'/>限定（qualifier）"
        "说明主张能延伸多远：在这台机器上，对这个程序。<bookmark mark='f'/>而反驳（rebuttal）说明它什么时候会失效：除非地址随机化正掩盖着一个真实的效应。薄弱的论文止步于主张和数据。",
    # ------------------------------------------------------------------ s09_writing
    "A paper makes many claims, and each one needs its own":
        "一篇论文会提出许多主张，每一个都需要它自己的证据。这里有一个可以在任何草稿上做的检验，用第六章那篇虚构的论文来演示。<bookmark mark='a'/>首先，列出引言提出的每一个主张，包括顺带提到的那些。"
        "<bookmark mark='b'/>然后，为每个主张找到支持它的那一节、那张图或那条定理。“Skim 对每个词只做一次哈希”：这是算法，在第3节。“快2.1倍”：图4，前提是它有区间，并且说明了基线是什么。"
        "<bookmark mark='c'/>“额外内存很少”，以及“适用于任何语言”：论文里没有任何东西支持这两条。<bookmark mark='d'/>每一条这样的主张，要么删掉，要么补上证据。无论你做不做，"
        "审稿人都会做这个检验。一篇好的引言会让它变得容易：说清楚每一项贡献在哪里得到展示。",
    'f"A figure should carry the claim, and the same':
        "一张图应该承载主张，而同样的数据，可以被做得承载相反的主张。这是第二章的三种链接顺序。<bookmark mark='a'/>左边只有中位数，坐标轴在最小值下方一点点就截断了。"
        "最高的柱子是最矮那根的{say1(TALL)}倍高，而标题宣称链接顺序会改变速度。<bookmark mark='b'/>右边是同一个实验："
        "全部{say(sum((len(r['runs']) for r in LINK)))}次运行，标出了中位数，坐标轴能显示出波动。中位数相差不到百分之一；每种顺序内部的各次运行，"
        "波动在百分之{say(min(RUN_SPREADS))}到百分之{say(max(RUN_SPREADS))}之间。<bookmark mark='c'/>它的标题陈述的，是这张图所支持的主张。"
        "Edward Tufte 在1983年这样表述这条规则：数字的表示，应当与它们所代表的量成正比。展示波动，标明单位，让读者能检验你。",
    "This series holds itself to a rule: every number on screen":
        "这个系列给自己定了一条规则：屏幕上的每一个数，要么由我们自己的代码算出来，要么已经发表并注明了出处。下面是一个计算出来的数怎样传递的。<bookmark mark='a'/>一个仪器，"
        "也就是一个带有自己测试的 Python 模块，负责做实际的工作：这里是测量偏差实验。<bookmark mark='b'/>一个计算脚本把每一项运行一次，把结果以 JSON 格式存进缓存，放在这一部分的名字下面。"
        "<bookmark mark='c'/>场景加载它。场景从不计算实验，也从不手敲一个数字。<bookmark mark='d'/>而旁白是用同一个值格式化出来的，所以你听到的句子不可能和测量结果不一致。"
        "<bookmark mark='e'/>在另一台机器上重新运行这个仪器，依赖它的每一张图、每一句话都会随之改变。你不必信任我们；你可以检验。",
    'f"Three kinds of number appear in this series,':
        "这个系列里出现三种数，每一种都带着自己的标签。<bookmark mark='a'/>计算出来的数来自我们的仪器，在这台机器上得出，并且会说明这一点：百分之{say1(ENV_SPREAD)}的波动，"
        "200万以下最难的 Goldbach 情形，350这个上限。<bookmark mark='b'/>已发表的数，会在旁白里注明作者和年份：Goldbach 猜想核对到4乘10的18次方，"
        "Pólya 猜想在9亿600万附近失效。<bookmark mark='c'/>示意性的数在屏幕上有标记：虚构论文里的2.1，第三章里的1秒和4秒。<bookmark mark='d'/>"
        "读者信任那些教他们怎样检验的作者。Hamming 说得很直白：把工作做出来是不够的；你必须写得清楚，还要去做报告，让人们会去读、会去听。"
        "Justin Zobel 的《计算机科学写作》（Writing for Computer Science）就是前一件事的手册。",
    # ------------------------------------------------------------------ s10_frontier
    "Chapter nine, the frontier. What is still unknown, and":
        "第九章：前沿。还有什么是未知的？你又会从哪里开始？",
    "Here is every open problem the series met, as a sky over":
        "这是这个系列遇到过的每一个开放问题，画成塔上方的一片星空。<bookmark mark='a'/>每颗星都是一个没人回答过的问题，标着我们在哪些部分遇到它，以及它最早被提出的年份。有些已经有几十年了：P 与 NP，"
        "从1971年起；矩阵乘法的指数，从1969年施特拉森带来的惊喜起；电路的门数，从1949年的香农起。<bookmark mark='b'/>有些最近有了进展：第五个忙碌海狸数在2024年被证明，"
        "而矩阵乘法的纪录还在一点点往下降。<bookmark mark='c'/>它们没有一个已经解决，每一个都是某个人一生的工作。这一章剩下的部分要问：一个人会怎样着手其中的一个。",
    'f"One honest way to start is with the small':
        "一种诚实的起步方式，是从小情形入手。<bookmark mark='a'/>1742年，Goldbach 和欧拉在通信中得出了这个猜想：每个大于2的偶数都是两个素数之和。我们的筛法在不到1秒内，"
        "核对了直到{g['limit']:,}的每个偶数，并发现最难的是{g['worst']:,}，它最小的素数搭档是所有偶数里最大的。<bookmark mark='b'/>Collatz 问题出自1937年，它说："
        "偶数减半，奇数乘3加1，最终总会到达1。每个小于一百万的起点都做到了；最慢的要走{rec['steps']}步。<bookmark mark='c'/>核对小情形，永远证明不了一条关于所有数的定理，但它能找到反例，"
        "提示规律，并显示出证明在哪里得下最大的功夫。",
    "How do you choose? <bookmark mark='a'/> Richard Hamming":
        "怎样选择？<bookmark mark='a'/>Richard Hamming 问他的同事们，他们领域里的重要问题是什么，然后问他们为什么不去研究这些问题。<bookmark mark='b'/>"
        "这个系列里每一个标了星号的问题，都有一个更小的版本，某个人是可以把它做完的。<bookmark mark='c'/>许多突破都是把一件新工具带到一个老问题上：把拓扑带到一致问题上，把谱带到流上，"
        "把 SAT 带到证明上。<bookmark mark='d'/>而一项极限研究，就像第7部分的那样，会告诉你有没有值得争取的提升空间。<bookmark mark='e'/>所以最后这道研究题，由你自己来定义："
        "从这个系列里挑一颗星，找到它最小的、尚未解决的特殊情形，并解决它。",
    # ------------------------------------------------------------------ s11_bridges
    "Chapter ten. Where the series meet.":
        "第十章：几个系列交汇的地方。",
    'f"This series has two older siblings: AI, Built,':
        "这个系列有两个年长的兄弟：《人工智能，从零搭建》，31个部分，讲机器怎样学习；以及《分析学，从零搭建》，10个部分，讲极限的数学，从实数一直讲到谱定理。<bookmark mark='a'/>"
        "它们共享的不只是一种风格。这是《人工智能，从零搭建》第1部分选出的三十部小说，从《傲慢与偏见》到《尤利西斯》。<bookmark mark='b'/>《人工智能，从零搭建》用它们训练模型，"
        "并在一段没有任何模型训练过的文字上，给每个模型打分。<bookmark mark='c'/>这个系列的那项任务数它们的词：大约{say(round(NBYTES / 1000000.0))}兆字节，"
        "大约{say1(NWORDS / 1000000.0)}百万个词，从第6部分的 Pebble 一直数到第60部分的电路。<bookmark mark='d'/>《分析学，从零搭建》一部小说也不读，"
        "但它证明了另外两个系列一直依靠的那些定理。",
    "Draw the three series as towers, one floor for each part:":
        "把三个系列画成三座塔，每一部分一层：左边是《人工智能，从零搭建》，中间是这个系列，右边是《分析学，从零搭建》。<bookmark mark='a'/>第一座桥是每个模型都要跨过的那座。"
        "第23部分让梯度下降和牛顿法同台较量；《人工智能，从零搭建》的第11部分，用这一步的后代来训练每一个网络：动量、Adam，以及学习率调度。<bookmark mark='b'/>第57部分问过，"
        "学习到底什么时候是可能的，用的是 PAC 界和 VC 维；《人工智能，从零搭建》的第8部分对真实的模型问同一个问题，用的是 Rademacher 复杂度和双下降。<bookmark mark='c'/>"
        "第60部分搭了一个脉动阵列，并把它放到屋顶线上；《人工智能，从零搭建》的第17部分把 GPU 放到同一道屋顶线上，并对矩阵乘积分块，好爬上去。<bookmark mark='d'/>而香农1948年的论文，"
        "垫在这两者下面。第28部分用典型集证明了他的信道定理；《人工智能，从零搭建》的第1部分，在通往交叉熵的路上遇到了同样的典型集，而交叉熵正是每个语言模型训练时所用的损失。",
    "On the other side stands analysis. <bookmark mark='a'/> The":
        "另一边是分析学。<bookmark mark='a'/>最低的那座桥最古老。图灵1936年的论文题为《论可计算数》（On Computable Numbers）：如果一台机器能写出一个实数的各位数字，"
        "这个实数就是可计算的。《分析学，从零搭建》的第1部分构造了实数，并用康托尔的对角线论证证明它们是不可数的。机器可以一一列出，所以几乎每一个实数，都是没有机器能写出来的。<bookmark mark='b'/>"
        "第19部分的快速傅里叶变换，来自1965年的 Cooley 和 Tukey，它计算的是《分析学，从零搭建》第9部分的傅里叶变换，只不过取在有限个点组成的一个环上，而不是整条直线上。"
        "<bookmark mark='c'/>而第52部分的迭代，首先是牛顿法，之所以收敛，原因正是《分析学，从零搭建》第2部分所证明的：柯西序列，以及带余项的泰勒定理，余项还说明了收敛有多快。",
    "Some ideas stand on all three towers at once. Take the step":
        "有些想法同时立在三座塔上。拿训练每个模型的那一步来说。<bookmark mark='a'/>《分析学，从零搭建》第2部分的泰勒定理：f 在 x 加 h 处的值，等于 f 在 x 处的值，加上斜率乘 h，"
        "再加上中间某一点处二阶导数的一半，乘以 h 的平方。<bookmark mark='b'/>现在取第23部分的那一步：h 等于负 eta 乘以斜率。中间那一项变成负 eta 乘以斜率的平方。"
        "<bookmark mark='c'/>如果曲率从不超过 L，最后一项至多是 L 除以2，乘 eta 的平方，再乘斜率的平方，所以 f 至少下降 eta 乘以（1减 L eta 除以2），再乘斜率的平方。"
        "<bookmark mark='d'/>取 eta 等于1除以 L，每一步至少让 f 下降斜率的平方除以2L。<bookmark mark='e'/>这个不等式说明了学习率为什么有一个上限，这是《人工智能，"
        "从零搭建》第11部分早早讲过的一课：步子迈得比2除以 L 还远，这个保证就没有了。在多维情形下，斜率变成梯度，也就是《分析学，从零搭建》第4部分的导数。",
    "Draw every crossing at once, and three buildings start to":
        "把所有的交汇一次画出来，三座建筑开始看起来像一座。<bookmark mark='a'/>交汇不止这七处。第18部分的 PageRank，是《人工智能，从零搭建》第5部分的一条马尔可夫链；第20部分的随机投影，"
        "是它第3部分的 Johnson–Lindenstrauss 引理；第54部分的证明助手，就是它第25部分的 Lean。<bookmark mark='b'/>而一道好的研究题，常常就住在一座桥上："
        "一件在一边已经是常规的工具，在另一边却还没人试过。",
    # ------------------------------------------------------------------ s12_pebble
    "Chapter eleven. The pebble, the last time.":
        "第十一章：最后一次看石子。",
    'f"Part 1 began with a game for someone who knows':
        "第1部分从一个给完全不懂数字的人玩的游戏开始：两堆石子，一条规则。<bookmark mark='a'/>如果两堆不一样多，就从大的那堆里拿走和小的那堆一样多的石子。"
        "{say(steps[0][0]).capitalize()}和{say(steps[0][1])}变成{say(steps[1][0])}和{say(steps[1][1])}，"
        "然后是{say(steps[2][0])}和{say(steps[2][1])}，然后是{say(steps[3][0])}和{say(steps[3][1])}，<bookmark mark='b'/>"
        "而{say(PEB['gcd'])}就是它们的最大公约数。<bookmark mark='c'/>1928年，希尔伯特和阿克曼问：是否每一个数学问题都能像这样解决，用一种机械的程序，像玩家移动石子那样移动符号："
        "这就是判定问题（Entscheidungsproblem）。<bookmark mark='d'/>1936年，图灵回答：不能。而为了证明这一点，他首先必须准确地说出机械的程序是什么。他的答案是一台机器，"
        "而这个系列里的其他一切，都建立在它之上。",
    "Then the series climbed, from the mathematics at the":
        "然后，这个系列从底部的数学开始往上爬。<bookmark mark='a'/>第3部分只用一种门，与非门（NAND），搭出了所有的门，<bookmark mark='b'/>到第6部分，这些门已经成了 Pebble，"
        "一台32位的计算机，它运行了那项任务。<bookmark mark='c'/>流水线、缓存和四个核让它变快；<bookmark mark='d'/>链接器、编译器、类型和垃圾回收器让我们能和它说话；"
        "<bookmark mark='e'/>算法告诉它该做什么。<bookmark mark='f'/>PebbleOS 让许多程序分享它，并把它们的数据保存在磁盘上；<bookmark mark='g'/>"
        "我们自己的 TCP、Raft 和 MapReduce，把许多台 Pebble 连在一起；<bookmark mark='h'/>而 Web、服务和云，把这一整套东西放到了人们面前。"
        "<bookmark mark='i'/>在这一叠层的旁边立着两根柱子：一根是极限，也就是任何机器都算不出来的东西、守不住的秘密；一根是实践，也就是人们怎样一起建造这样的东西。<bookmark mark='j'/>"
        "而在第55部分，我们问过这一切是否值得信任，看着一个编译器对自己撒谎，又看着第二个编译器把它揭穿。",
    'f"The Job kept score the whole way: count the':
        "那项任务一路都在记分：数出三十部小说里的词，列出最常见的二十个。<bookmark mark='a'/>这是账本的每一行，一共{say(len(LED))}行，画在每一格相差十倍的刻度上。"
        "第6部分的单周期 Pebble 需要{say(FIRST['seconds'])}秒。<bookmark mark='b'/>"
        "第{say(SLOWEST['part'])}部分的λ演算机器用了{say_dec(hrs)}小时，而缓存、编译器、哈希表、内核、网络和集群，把这根柱子推来推去。<bookmark mark='c'/>"
        "最后一行是第60部分的数词电路：大约{say(1000 * LAST['seconds'])}毫秒，前提是文本每个周期到达一个字节。大多数行，是由这个系列搭建的机器算出来的；少数几行，是在这台机器上原生计时的。",
    'f"So how much faster did the series make the Job?':
        "那么，这个系列让那项任务快了多少？<bookmark mark='a'/>用第一行除以最后一行：{say(FIRST['seconds'])}秒，"
        "除以大约{say(1000 * LAST['seconds'])}毫秒，<bookmark mark='b'/>加速比大约是{say(SPEEDUP)}倍。<bookmark mark='c'/>"
        "这个比值是{say(STEPS)}步的乘积，每一步从一行到下一行，而它们并不都指向同一个方向。<bookmark mark='d'/>其中{say(SLOWER).capitalize()}步变慢了，"
        "因为每一行既改变了运行的快慢，也改变了测量的对象：加上了一个内核、一个网络或者一个集群。向前最大的一步是{say(RATIOS[BEST])}倍，从第{say(b_from)}部分到第{say(b_to)}部分；"
        "向后最大的一步是{say(1 / RATIOS[WORST])}倍，从第{say(w_from)}部分到第{say(w_to)}部分。<bookmark mark='e'/>而典型的一步，按第三章对比值取平均的规则，"
        "是总数的{ordinal(STEPS)}次方根：每一行大约快{say_dec(GEO, 2)}倍。",
    "At the top of the tower the floors stop, and the sky of":
        "到了塔顶，楼层到头了，第九章的星空从这里开始：<bookmark mark='a'/>P 与 NP，单向函数，矩阵乘法的指数，第六个忙碌海狸数，还有其余的问题，每一个都是我们在往上爬的路上某处遇到的。"
        "<bookmark mark='b'/>希尔伯特曾希望，一种程序就能解决所有这样的问题。图灵的回答意味着，永远不会有任何机器做到这一点，所以这片天空永远不会空：总会有一个问题，等着某个人去着手。",
    "Every floor of that tower, and every star above it, began":
        "那座塔的每一层，以及它上方的每一颗星，都是像第1部分那样开始的：<bookmark mark='a'/>从一颗小石子开始，按一条规则移动。罗马人把这样的石子叫作 calculus。"
        "<bookmark mark='b'/>它仍然是计算机由之构成的最小的东西：一个标记，要么在，要么不在，一次按一条规则移动。",
    # ------------------------------------------------------------------ s13_outro
    "The last act went past the degree, to the first year of":
        "最后一幕越过了学位，走进研究的第一年。<bookmark mark='a'/>知道一个图的形状的特征值；关于学习何时可能的定理；每个程序的三种含义；分布式进程能计算什么的极限；为单一工作而造的硬件；以及在这一部分，"
        "这个系列里每一个结果得以做出的方法。",
    "And that is the whole map: sixty-one parts. <bookmark":
        "这就是整张地图：61个部分。<bookmark mark='a'/>它从两堆石子和一条规则开始，结束在一些还没有人能回答的问题上。每一层都建在它下面那一层之上，而每一层都是在这里搭起来的，从门到集群，"
        "从一个证明到一个协议。",
    "Six problems, the last of the series, with full solutions":
        "六道习题，也是这个系列的最后几道，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：在栈保持不动的情况下，重做这一部分自己的实验，并用置换检验来判断，被噪声掩盖的那个效应是否真的存在。"
        "最后一道标了星号，是第九章的那道研究题，也是这个系列的最后一句话：挑一个开放问题，找到它最小的、尚未解决的情形，并解决它。",
    "If you want to keep going, here is a shelf. <bookmark":
        "如果你想继续走下去，这里有一个书架。<bookmark mark='a'/>关于机器：Harris 和 Harris，Patterson 和 Hennessy，以及 Bryant 和 O'Hallaron。关于语言："
        "Abelson 和 Sussman，Appel，以及 Pierce。关于算法：Cormen、Leiserson、Rivest 和 Stein 合写的那本书，以及 Kleinberg 和 Tardos。关于理论："
        "Sipser，Arora 和 Barak，以及 Motwani 和 Raghavan。关于系统：Arpaci-Dusseau 夫妇，Kurose 和 Ross，以及 Kleppmann。关于软件："
        "Brooks 和 Ousterhout。而关于研究本身：Hamming 的演讲，以及 Pólya 的《怎样解题》。",
    "This is the end of Computer Science, Built. Thank you for":
        "《计算机科学，从零搭建》到这里就结束了。感谢你把它全部看完。这些开放问题是真实的，其中一些会被这样的人解决：他们恰恰从这个系列起步的地方出发，带着几颗石子和一条规则。挑一个，开始吧。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
