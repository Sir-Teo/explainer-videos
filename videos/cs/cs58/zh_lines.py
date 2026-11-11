"""Chinese narration for cs58: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第58部分：语义学"

CHAPTERS = {
    "Hook": "一个程序意味着什么",
    "Operational": "1. 作为步骤的含义",
    "Denotational": "2. 作为数学的含义",
    "Domains": "3. 论域与不动点",
    "Adequacy": "4. 充分性与完全抽象",
    "Equivalence": "5. 两个程序什么时候相同",
    "Parametricity": "6. 免费的定理",
    "Axiomatic": "7. 霍尔逻辑，证明其可靠",
    "Effects": "8. 效应与单子",
    "Dependent": "9. 依赖类型",
    "Concurrency": "10. 进程与通道",
    "Frontier": "11. 前沿：真实语言的语义",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    'f"What does a program mean? Here is factorial,':
        "一个程序意味着什么？这里是阶乘，以及三种不同的回答。<bookmark mark='a'/>第一种，作为步骤：含义就是机器拿它做了什么。我们的解释器把 fact 3 改写了"
        "{f['steps']}个小步，一直化到6。<bookmark mark='b'/>第二种，作为数学对象：含义是一个函数，是一条近似链的极限。第一个近似什么都不知道，下一个知道0的阶乘，"
        "再下一个知道0和1的，而极限就是阶乘本身。<bookmark mark='c'/>第三种，作为定律：含义就是关于它能证明的东西，方程和霍尔三元组。<bookmark mark='d'/>"
        "这就是操作语义、指称语义和公理语义，而这一部分的深刻结果告诉我们，它们在什么时候一致。",
    'f"Why does this matter outside a classroom?':
        "这在课堂之外为什么重要？<bookmark mark='a'/>一个编译器是正确的，恰好当它输出的东西的含义等于它收到的东西的含义，CompCert 就是这样被证明的。"
        "<bookmark mark='b'/>一次重构是安全的，当没有哪个外围程序能把旧代码和新代码区分开。<bookmark mark='c'/>语言还可以先把含义写下来再设计："
        "WebAssembly 的规范在这门语言发布之前就已经是形式化的了。<bookmark mark='d'/>在这一部分，我们为一门小语言搭建三个解释器，并检查它们是否一致："
        "在我们试过的{a['n']}个随机程序里，有{a['agree']}个一致；然后我们证明为什么。",
    "This is Part 58 of Computer Science, Built. <bookmark":
        "这是《计算机科学，从零搭建》的第58部分。<bookmark mark='a'/>我们会给一门语言三种操作语义；在论域和最小不动点上搭建它的指称语义；追问两者在什么时候一致；"
        "用互模拟和逻辑关系判定两个程序什么时候相同；单凭类型推导出免费定理；再把含义推广到效应、依赖类型和相互通信的进程。",
    # ------------------------------------------------------------------ s02_operational
    "Chapter one. Meaning as steps. What does a machine do":
        "第一章：作为步骤的含义。机器拿一个程序做什么？",
    "We need a language small enough to reason about and large":
        "我们需要一门语言，小到足以推理，又大到足够有趣。<bookmark mark='a'/>它的项有整数和布尔值、变量、函数及其应用、条件式和算术，<bookmark mark='b'/>"
        "还有一个用于递归的构造：fix f x 箭头 e 是一个名叫 f、参数为 x 的函数，它的函数体可以调用 f 自己。<bookmark mark='c'/>有些项已经完成了：数、布尔值和函数。"
        "它们就是值，而一个程序的全部任务就是变成一个值。<bookmark mark='d'/>这是用 fix 写成的阶乘。在这整个部分里我们都会跟着它。",
    "Gordon Plotkin's structural operational semantics, from":
        "戈登·普洛特金的结构化操作语义，出自他1981年的奥胡斯讲义，用规则来定义计算的一步：横线上面是必须成立的条件，横线下面是由此得出的结论。<bookmark mark='a'/>"
        "搜索规则说明去哪里找。要让一个算术项走一步，先让它的左边走；一旦左边是值了，再让右边走。这就是从左到右的传值调用，被明确地写了出来。<bookmark mark='b'/>"
        "归约规则说明当搜索找到可以计算的东西时该做什么。两个数变成它们的和或积；条件为真的条件式变成它的第一个分支；作用于一个值的函数变成它的函数体，"
        "用这个值代换参数。<bookmark mark='c'/>而 fix 会把自己展开一层：函数体得到 x 的值，以及作为 f 的整个函数。",
    "Each step is a small theorem, with a proof tree.":
        "每一步都是一条小定理，带着一棵证明树。<bookmark mark='a'/>这是我们的解释器从阶乘轨迹的第四个项走到第五个项的那一步：3 乘 fact 括号 3 减 1，变成 3 乘 fact 2。"
        "<bookmark mark='b'/>从底部往上读这棵树。3 是值，所以这个乘积可以让它的右边走一步。fact 是值，所以这个应用可以让它的实参走一步。而 3 减 1 按算术走到 2。"
        "<bookmark mark='c'/>第一条定理：如果一个项能走到 e1，也能走到 e2，那么它们相等。这门语言是确定性的。证明是对推导做归纳：值从不走步，而每条搜索规则都要求"
        "它左边的一切都是值，所以任何时候至多只有一条规则适用。",
    'f"<bookmark mark=\'a\'/> Here is factorial of':
        "<bookmark mark='a'/>这是 3 的阶乘，来自我们的小步解释器，一次一步，每一步新出现的部分用黄色标出。<bookmark mark='b'/>注意项的长度。随着乘法越堆越多，"
        "它不断变长，每个乘法都在等它的右边：3 乘、2 乘、1 乘。这些待做的运算，就是第11部分的调用栈，被写进了项本身。<bookmark mark='c'/>到了基本情形，项塌缩下来，"
        "走了{f['steps']}步之后，它成了值{f['value']}。因为这门语言是确定性的，一次运行是一条线，而不是一棵树，而它末端的值，如果有的话，就是这个程序的含义。",
    'f"Small steps answer the question: what happens':
        "小步回答的问题是：接下来发生什么？有时候我们只想要答案。<bookmark mark='a'/>Gilles Kahn 1987年的自然语义把一个项直接和它的值联系起来：e 求值为 v。"
        "值求值为它自己；算术项先求值两边，再把它们结合起来；应用先求值函数，再求值实参，然后求值用实参代换之后的函数体。<bookmark mark='b'/>现在证明树就是整个计算。"
        "平方函数作用于 1 加 2：函数是值，实参求值为 3，函数体 3 乘 3 求值为 9。<bookmark mark='c'/>两种语义是一致的：e 求值为 v，恰好当 e 用小步到达 v。"
        "我们的大步求值器用环境代替代换，在{a['n']}个随机程序里，它和小步解释器在{a['agree']}个上一致。",
    "Neither semantics is how a real interpreter runs.":
        "这两种语义都不是真实解释器的运行方式。<bookmark mark='a'/>马蒂亚斯·费莱森和丹尼尔·弗里德曼1986年的 CEK 机保留三个寄存器：一个控制项，一个存放变量的环境，"
        "以及一个续延，也就是一个由栈帧组成的栈，说明拿下一个值做什么。<bookmark mark='b'/>这里它运行一个作用于 2 的函数。它把实参记在一个栈帧里，把函数求值为一个闭包，"
        "再求值实参，把 x 绑定到 2，然后借助另外两个栈帧算完 x 加 1。<bookmark mark='c'/>每次转移只做常数量的工作，所以它需要更多次转移：平均每个程序大约294次，"
        "而小步是73步。但每一个小步都要搜索并复制整个项。<bookmark mark='d'/>这就是第15部分的解释器循环，从规则推导了出来。",
    # ------------------------------------------------------------------ s03_denotational
    "Chapter two. Meaning as mathematics. What object does a":
        "第二章：作为数学的含义。一个程序代表的是什么对象？",
    "Operational semantics says what a machine does with a":
        "操作语义说的是机器拿一个程序做什么。指称语义由达纳·斯科特和 Christopher Strachey 在牛津开创，见于他们1971年的论文，它问的却是一个程序是什么。"
        "<bookmark mark='a'/>每个项都由语义括号映射到一个数学对象，叫作它的指称。项 fun x 箭头 x 乘 x 指称整数上的平方函数：一个序对的集合，仅此而已。"
        "<bookmark mark='b'/>另一个程序，x 乘 x 加 0，要走更多步，指称的却恰好是同一个函数。<bookmark mark='c'/>所以指称保留了算的是什么，而忘掉了怎么算。"
        "在我们能说两个程序可以互换之前，需要的恰恰就是这个。",
    "There is one equation for each construct, and the":
        "每种构造都有一个方程，而环境 rho 提供自由变量的值。<bookmark mark='a'/>数字的含义是它的数。变量的含义是环境所说的值。<bookmark mark='b'/>"
        "算术项的含义是把运算作用于它两边的含义；条件式的含义是这个分支或那个分支，取决于条件的含义。<bookmark mark='c'/>函数的含义是一个数学函数：给定 v，"
        "就是 x 绑定到 v 时它函数体的含义。应用的含义是把函数的含义作用于实参的含义。一个永远完不成的项，含义是底元，也就是未定义的元素，而底元会扩散到每一个运算中。"
        "<bookmark mark='d'/>注意，每个右边都只提到各部分的含义。这就是组合性：含义从叶子往上拼装起来，没有机器，也没有步骤的次序。<bookmark mark='e'/>"
        "还缺一种构造，而它正是有意思的那一个：fix。",
    "Let us compute one meaning by nothing but equations.":
        "我们只用方程来计算一个含义。<bookmark mark='a'/>平方函数作用于 1 加 2。<bookmark mark='b'/>按应用的方程，它的含义是把函数的含义作用于实参的含义。"
        "<bookmark mark='c'/>函数的含义是这样一个映射：把 v 送到 x 绑定到 v 时 x 乘 x 的含义；而 1 加 2 的含义是 3。<bookmark mark='d'/>应用这个映射："
        "x 绑定到 3 时 x 乘 x 的含义。<bookmark mark='e'/>那就是 3 乘 3，等于 9。第一章的大步证明树通过求值得到了同样的 9。这里根本没有求值，只有代数，"
        "每一行都由上一行以等量代换等量得出，就像我们在学校里化简任何式子那样。",
    "Compositionality pays for itself at once. <bookmark":
        "组合性立刻就有了回报。<bookmark mark='a'/>拿任何一个带洞的程序。这叫作上下文。<bookmark mark='b'/>填进两个含义相同的项，<bookmark mark='c'/>"
        "整个程序的含义就相同，无论上下文是什么。证明是对上下文做归纳，它之所以成立，是因为每个方程都只看各部分的含义。<bookmark mark='d'/>正是这一点允许优化器，"
        "比如第13部分的那个，在程序的任何地方把 x 乘 x 加 0 换成 x 乘 x：一条关于含义的局部事实，处处都能用。逆命题是否成立，也就是没有哪个上下文能区分的程序"
        "是否总有相等的含义，是第四章的问题。",
    "Recursion is where the mathematics has to work. <bookmark":
        "递归是数学必须真正出力的地方。<bookmark mark='a'/>fix f x 箭头 e 的含义应该是一个满足它自身定义的函数 g：把 v 映到函数体含义的那个映射，其中 f 绑定到 g 自己。"
        "<bookmark mark='b'/>把右边写成一个泛函 F，它把一个候选 h 变成一个改进了的候选。于是 g 等于 F 作用于 g：一个递归函数的含义是 F 的一个不动点。<bookmark mark='c'/>"
        "对阶乘来说，F 作用于 h，在 n 处的值，当 n 为 0 时是 1，否则是 n 乘 h 在 n 减 1 处的值。<bookmark mark='d'/>但一个方程可能有好几个解。这两个都是阶乘的 F "
        "的不动点：它们在自然数上一致，而在负数上，一个没有定义，另一个是 0。<bookmark mark='e'/>哪个才是含义？在负 1 上运行 fact，它会在负 2、负 3 上调用自己，永无止境。"
        "所以那里的答案是未定义的：定义得最少的不动点。把“最少”说精确，并证明它总是存在，这就是论域理论，下一章的内容。",
    # ------------------------------------------------------------------ s04_domains
    "Chapter three. Domains and fixed points. Why does every":
        "第三章：论域与不动点。为什么每个递归定义都有含义？",
    "To choose the least solution we need an order, and Dana":
        "要选出最小的解，我们需要一个序，而达纳·斯科特的洞见是按信息来给含义排序。<bookmark mark='a'/>在带底元的整数里，未定义的结果位于每个数的下方，而各个数并排而立："
        "知道结果是 3，既不比知道它是 4 多，也不比它少。<bookmark mark='b'/>函数按逐点的方式排序：一个函数在另一个下方，如果凡是前者有定义的地方，后者也有定义，并且取值一致。"
        "<bookmark mark='c'/>填入答案会沿着序往上走。改动答案则不会：h 比 f 有更多的答案，但它不在 f 的上方。",
    "Domains are partial orders with two extra properties.":
        "论域是多了两条性质的偏序。<bookmark mark='a'/>有一个最小元，底元：完全没有信息。<bookmark mark='b'/>而每条链，其中每个元素都至少和前一个定义得一样多，"
        "都有一个最小上界：在它们全体之上，又在其他每个上界之下。这就是完全偏序，cpo。<bookmark mark='c'/>在整数里，链至多往上爬一步。但在部分函数之间，"
        "一条链可以永远往上爬，而它的最小上界汇集了它们所有的答案。无穷的对象，比如定义在全体自然数上的阶乘，就是这样由有限的片段到达的。",
    "Kleene's theorem needs two properties of F. <bookmark":
        "克莱尼定理需要 F 的两条性质。<bookmark mark='a'/>它必须是单调的：输入的信息更多，输出的信息至少一样多。<bookmark mark='b'/>它还必须是斯科特意义下连续的："
        "F 作用于一条链的极限，等于 F 沿着这条链的极限。输出的任何有限部分只依赖于输入的有限部分。<bookmark mark='c'/>这是一个单调但不连续的函数。H 在它的实参是全函数时"
        "返回 1，否则返回底元。<bookmark mark='d'/>沿着部分阶乘函数的链，每个答案都是底元，所以极限是底元；但 H 作用于极限却是 1。<bookmark mark='e'/>没有程序能计算 H："
        "它会判定一个函数是否处处停机，这是第25部分停机问题的一个近亲。",
    "Now the theorem, usually credited to Stephen Kleene.":
        "现在来看这条定理，它通常归功于斯蒂芬·克莱尼。<bookmark mark='a'/>如果 D 是一个 cpo，F 是连续的，那么底元、F 作用于底元、F 作用于 F 作用于底元，如此下去，"
        "其极限就是 F 的最小不动点。<bookmark mark='b'/>第一，这是一条链：底元在 F 作用于底元的下方，因为底元在一切的下方；再把单调的 F 作用 n 次。<bookmark mark='c'/>"
        "第二，这是一个不动点。把 F 作用于极限。由连续性，F 可以移到里面去。<bookmark mark='d'/>F 作用于 F 的 n 次方，就是 F 的 n 加 1 次方：<bookmark mark='e'/>"
        "这是同一条链，只是去掉了打头的底元，所以极限相同。<bookmark mark='f'/>第三，它是最小的：由归纳，链上的每个元素都在任何不动点 d 的下方，所以它们的最小上界也在"
        "下方。<bookmark mark='g'/>这就是第13部分活跃性分析的那种往上爬；只是在这里它可能永远爬下去，而连续性把我们带到极限。",
    "Here is the theorem at work, computed by our instrument.":
        "这是这条定理在起作用，由我们的工具算出。<bookmark mark='a'/>从底元开始，也就是什么都不知道的函数。<bookmark mark='b'/>把阶乘的 F 作用一次，它就知道 0 的阶乘"
        "是 1。再作用一次，它就知道 0 和 1。每作用一次，就多一个答案。<bookmark mark='c'/>所以第 k 个函数是展开了 k 次的阶乘：凡是需要少于 k 次递归调用的输入，它都能回答。"
        "<bookmark mark='d'/>这条链永不停止，但它的最小上界是完整的阶乘，正是第二章在寻找的那个最小不动点，在负数上仍然没有定义。<bookmark mark='e'/>while 循环也是一样："
        "它的含义是展开一次的最小不动点，而第 k 个近似至多运行循环 k 次。",
    "The same ideas answered an old question about Church's":
        "同样的思想回答了关于丘奇 λ 演算的一个老问题，它来自第14部分：无类型演算到底有没有数学模型？<bookmark mark='a'/>在那里，每个项都是一个可以作用于任何项的函数，"
        "甚至可以作用于它自己，所以一个模型需要一个空间 D，它和从 D 到 D 的函数是同一个东西。<bookmark mark='b'/>对普通函数来说这是不可能的：由康托尔的对角线论证，"
        "从 D 到 D 的函数总是比 D 的元素多。<bookmark mark='c'/>达纳·斯科特在1969年的回答是只用连续函数，并把 D 构造成一个极限：一个论域，它的连续函数空间，"
        "那个空间的连续函数空间，如此下去，每一个都在下一个之中。<bookmark mark='d'/>这个极限 D 无穷，同构于它自己的连续函数空间：这是无类型 λ 演算的第一个数学模型。",
    # ------------------------------------------------------------------ s05_adequacy
    "Chapter four. Adequacy and full abstraction. Do the steps":
        "第四章：充分性与完全抽象。步骤和数学是一致的吗？",
    "We now have two meanings for every program: the steps of":
        "现在每个程序都有两种含义：第一章的步骤，以及第二章和第三章的数学。它们一致吗？<bookmark mark='a'/>可靠性：如果一个程序走到一个值，它的指称就是那个值的指称。"
        "计算从不改变含义。<bookmark mark='b'/>充分性：如果一个整数类型的完整程序的指称是一个数 n，而不是底元，那么机器真的会到达 n。<bookmark mark='c'/>两者合起来，"
        "数学就准确地预言了机器做什么，包括它会不会停。戈登·普洛特金在1977年为 PCF 证明了这一点，PCF 是一个带有数、布尔值和 fix 的有类型 λ 演算：本质上就是我们的"
        "语言，加上了类型。",
    "Soundness is the easy direction: show that one step":
        "可靠性是容易的那个方向：证明一步保持含义，然后数步数。<bookmark mark='a'/>拿 β 规则来说，一个函数作用于一个值。<bookmark mark='b'/>按方程，它的含义是那个映射，"
        "作用于这个值的含义。<bookmark mark='c'/>应用这个映射，就把 x 绑定到那个含义。<bookmark mark='d'/>再由一条代换引理，它对 e 做归纳来证明，那就是用这个值代换之后"
        "函数体的含义。<bookmark mark='e'/>fix 规则也是同样的做法，而这里恰恰是我们需要 fix 的含义是一个不动点的地方。<bookmark mark='f'/>充分性要难一些。试着对程序做归纳。"
        "到了一个应用，我们只知道函数的含义是某个数学函数，而关于整数的归纳假设对函数程序什么也没说。我们需要一个同时关于每一种类型的命题。",
    "That statement is a logical relation: one relation for":
        "这个命题就是一个逻辑关系：每种类型一个关系，每个都建立在更小的类型之上，就像梯子的横档。<bookmark mark='a'/>在最底下的横档，整数上：一个含义 d 与一个程序 e "
        "相关，如果 d 是底元，或者 e 求值为 d。<bookmark mark='b'/>在从 sigma 到 tau 的函数的横档上，d 与 e 相关，如果 d 是底元，或者 e 求值为一个函数值 v，而且每当"
        "一个含义 a 与一个实参程序相关时，d 作用于 a 就与 v 作用于那个程序相关。<bookmark mark='c'/>相关的实参得到相关的结果。<bookmark mark='d'/>每个横档只用到更小的类型，"
        "所以这个定义是良基的；这就是为什么这门语言必须是有类型的。",
    "The fundamental lemma: every well-typed closed program is":
        "基本引理：每个良类型的闭程序都与它自己的含义相关。<bookmark mark='a'/>难的情形是 fix，它的含义是一条克莱尼链的极限，这里是阶乘的那条。按定义，底元与任何东西"
        "都相关。<bookmark mark='b'/>如果一个近似与这个程序相关，那么下一个近似也相关，因为含义多展开一次，正好对应 fix 规则多用一次。<bookmark mark='c'/>而每个关系在链的"
        "极限下都是封闭的，这个性质叫作可容许性，所以极限，也就是含义本身，是相关的。<bookmark mark='d'/>现在在 int 类型上读这条引理。如果 e 的含义是一个数 n，"
        "<bookmark mark='e'/>那么 n 与 e 相关，<bookmark mark='f'/>而在最底下的横档上，这意味着 e 求值为 n。这就是充分性。",
    "Two programs are contextually equivalent when no context":
        "两个程序是上下文等价的，当没有哪个上下文能把它们区分开。<bookmark mark='a'/>如果两个项含义相同，那么由组合性，每个上下文都给它们相同的含义，再由充分性，给它们相同的"
        "行为。<bookmark mark='b'/>完全抽象是逆命题：等价的程序有相等的含义，所以模型看不出任何程序看不出的区别。普洛特金证明了斯科特的 PCF 模型不是完全抽象的。"
        "<bookmark mark='c'/>罪魁祸首是并行或：只要任一个实参为真，它就为真，即使另一个永远运行下去。它是连续的，所以它活在模型里，但没有哪个 PCF 程序能计算它。"
        "一个顺序的程序必须先看其中一个实参，而如果那一个死循环了，程序也就死循环了。<bookmark mark='d'/>所以两个只在并行或上不同的测试在 PCF 里是等价的，尽管它们的含义"
        "不同。<bookmark mark='e'/>而普洛特金证明，把并行或加进语言，模型就成了完全抽象的。",
    "A fully abstract model of PCF itself was found in the":
        "PCF 本身的完全抽象模型是在二十世纪九十年代，在博弈中找到的：由 Samson Abramsky、Radha Jagadeesan 和 Pasquale Malacaria，由 Martin Hyland 和 Luke Ong，"
        "还有 Hanno Nickau 独立地找到。<bookmark mark='a'/>一个类型变成程序与它的环境之间的一场博弈，双方轮流提问和回答。<bookmark mark='b'/>一个程序是一个策略，"
        "一条决定它下一步怎么走的规则。这里环境索要一个结果；程序索要它的实参；被告知是真，它就回答假。<bookmark mark='c'/>策略一次只走一步，所以必须同时询问两个实参的"
        "并行或不是一个策略：顺序性是内建的。<bookmark mark='d'/>接下来，我们直接追问两个程序什么时候相同。",
    # ------------------------------------------------------------------ s06_equivalence
    "Chapter five. When are two programs the same? Can we":
        "第五章：两个程序什么时候相同？不尝试每一个上下文，我们能证明它吗？",
    "Chapter four defined sameness: two programs are":
        "第四章定义了相同：两个程序是上下文等价的，当没有哪个上下文能把它们区分开。<bookmark mark='a'/>x 加 x 和 2 乘 x 是同一个函数吗？<bookmark mark='b'/>"
        "把每个都作用于 5，在它于 3 处的值上加 1，把它作用两次：每个测试都一致。<bookmark mark='c'/>但上下文有无穷多个，而测试不是证明。<bookmark mark='d'/>"
        "这一章给出两种从不对上下文做量化的方法：互模拟，它检查一步，然后再同样检查一步，永远如此；以及逻辑关系，它一种类型一种类型地建立相同。",
    "Programs that run forever are better compared by what":
        "永远运行的程序，最好按它们接下来能做什么来比较。这里有两台用米尔纳记法写成的小机器。<bookmark mark='a'/>两台都能先做 a 再做 b，或者先做 a 再做 c："
        "迹是相同的。<bookmark mark='b'/>但把 a 读作一枚硬币，把 b 和 c 读作茶和咖啡。第一台收下你的硬币，然后让你选；第二台在收硬币的同时就替你选好了。",
    "Bisimulation makes this a game. <bookmark mark='c'/> An":
        "互模拟把这变成一场博弈。<bookmark mark='c'/>攻击者在任意一台机器上走一步：在第一台上投一枚硬币。<bookmark mark='d'/>防守者必须在另一台上用同样的动作回应，"
        "于是就认定了一个分支。<bookmark mark='e'/>无论它选哪个，攻击者都去要那个分支给不了的饮料。<bookmark mark='f'/>攻击者总是赢，所以这两台机器不是互模拟的，"
        "而有一个公式说明了原因：第一台可以收下一枚硬币，然后同时提供两种饮料。",
    "The definition is David Park's, from nineteen eighty-one,":
        "这个定义来自 David Park，1981年，它精炼了罗宾·米尔纳关于 CCS 的工作。<bookmark mark='a'/>一个关系是互模拟，如果每当 p 与 q 相关时，p 的每一步都有 q 的"
        "一步与之匹配，动作相同，进入相关的状态，反过来也一样。<bookmark mark='b'/>把那些各步都匹配进 R 的状态对记作 F 作用于 R。<bookmark mark='c'/>互模拟等价是所有"
        "互模拟的并，<bookmark mark='d'/>由克纳斯特和塔斯基定理，它是 F 的最大不动点。<bookmark mark='e'/>第三章是从下面爬到最小不动点；这一个是从上面到达的。"
        "<bookmark mark='f'/>它的证明原理是余归纳：给出一个关系，再检查一步。",
    "Here coinduction proves two machines the same. <bookmark":
        "这里余归纳证明了两台机器相同。<bookmark mark='a'/>V 收一枚硬币，提供茶或咖啡，然后重新开始。W 做同样的事，但回到它起点的一个副本。<bookmark mark='b'/>"
        "给出一个关系：两个起点放在一起，两个等待状态放在一起，再把 V 的起点和 W 的副本放在一起。<bookmark mark='c'/>对每一对检查一步：每一步都落在一个相关的对里。"
        "<bookmark mark='d'/>所以这两台机器是互模拟的，永远如此，而这来自一次有限的检查。<bookmark mark='e'/>我们的检查器自己就能找到这样的关系：从一切都相关开始，"
        "不断拆分块，直到再没有变化。",
    "For functions, Samson Abramsky's applicative":
        "对函数来说，Samson Abramsky 1990年的应用式互模拟玩的是同样的博弈。<bookmark mark='a'/>如果一个程序求值为一个数，另一个必须给出同一个数；如果求值为一个函数，"
        "另一个也必须如此，而且两个函数体在给定任意同一个实参时，必须再次相关。<bookmark mark='b'/>我们的两个函数已经是值了。<bookmark mark='c'/>把两者都作用于同一个 n。"
        "<bookmark mark='d'/>代换。<bookmark mark='e'/>两者都给出 2n。<bookmark mark='f'/>一次一个实参，从不用上下文。由 Howe 的方法，这个关系是一个同余，"
        "所以在像我们这样的纯语言里，它和上下文等价重合。",
    "The second method builds sameness by induction on types:":
        "第二种方法按类型归纳地建立相同：第四章的梯子，如今架在两个程序之间。<bookmark mark='a'/>整数程序是相关的，如果它们给出同一个数，或者都发散。<bookmark mark='b'/>"
        "函数是相关的，如果它们把相关的实参送到相关的结果。<bookmark mark='c'/>基本性质，对类型推导做归纳：每个良类型的程序都与它自己相关。<bookmark mark='d'/>"
        "现在拿两个相关的程序。<bookmark mark='e'/>把两者都放进一个上下文：把基本性质用于这个上下文，它们保持相关。<bookmark mark='f'/>在最底下的横档上，这意味着结果相同。"
        "<bookmark mark='g'/>对每一个上下文都如此：这就是上下文等价，而没有检查任何一个上下文。",
    "Logical relations first proved that typed programs stop.":
        "逻辑关系最早证明的是有类型的程序会停。<bookmark mark='a'/>在基本类型上，可归约的项是那些有范式的项；在函数类型上，是那些把可归约的实参送到可归约的结果的项。"
        "<bookmark mark='b'/>可归约的项会正规化，这对类型做归纳。每个有类型的项都是可归约的，这对项做归纳，而难倒了朴素证明的应用情形，如今就是定义本身。这就是威廉·泰特"
        "1967年的方法。<bookmark mark='c'/>把这样一个证明读作程序，它就会做正规化：先求值成函数，再把范式读回来。Berger 和 Schwichtenberg 在1991年把这一点说得精确。"
        "<bookmark mark='d'/>我们的实现和逐步归约的结果一致。",
    # ------------------------------------------------------------------ s07_parametricity
    "Chapter six. Theorems for free. What does a type promise":
        "第六章：免费的定理。一个类型对这个类型的每一个程序承诺了什么？",
    "John Reynolds asked what it means for a type to hide":
        "约翰·雷诺兹问：一个类型隐藏某样东西，是什么意思？<bookmark mark='a'/>这里有两个计数器。一个从 0 往上数；另一个往下数，读出时把状态取负。<bookmark mark='b'/>"
        "客户只能通过 start、increment 和 read 看到状态。<bookmark mark='c'/>把第一个里的 n 与第二个里的负 n 关联起来。两个起点是相关的，increment 保持相关的状态相关，"
        "而 read 给出相等的数。<bookmark mark='d'/>雷诺兹1983年的抽象定理说，这样一来，任何在隐藏类型上多态的客户都无法区分这两者。<bookmark mark='e'/>用他的话说，"
        "类型结构是一种用来强制抽象层次的语法纪律。",
    "The idea behind the theorem is chapter five's ladder":
        "这条定理背后的思想又是第五章的梯子，多了一根新的横档。把每个类型都读作一个关系。<bookmark mark='a'/>整数相关，当它们相等。<bookmark mark='b'/>函数相关，"
        "当它们把相关的实参送到相关的结果。<bookmark mark='c'/>列表相关，当它们长度相同，并且逐个元素相关。<bookmark mark='d'/>而新的横档是：一个多态值与另一个相关，"
        "如果对每一对类型和它们之间的每一个关系，它的两个实例都相关。<bookmark mark='e'/>抽象定理：每个良类型的项在它自己的类型上都与它自己相关。多态函数无法检查它的"
        "实参，所以它必须同时尊重每一个关系。",
    "Now read off a theorem. <bookmark mark='a'/> Take any":
        "现在来读出一条定理。<bookmark mark='a'/>任取一个从 a 的列表到 a 的列表的函数 r。由抽象定理，r 在它的类型上与它自己相关。<bookmark mark='b'/>由“对所有”的横档，"
        "对任意类型 A 和 B，以及它们之间的任意关系 R，r 的两个实例在“R 的列表到 R 的列表”上相关。<bookmark mark='c'/>由函数的横档：相关的列表送到相关的列表。"
        "<bookmark mark='d'/>现在是唯一需要创意的一步：选 R 为一个函数 f 的图像。两个列表相关，恰好当把 f 映射到第一个上就得到第二个。<bookmark mark='e'/>取 ys 为"
        "map f 作用于 xs。<bookmark mark='f'/>结论就在这里：先 r 后 map f，等于先 map f 后 r，对每一个 f、每一个这个类型的 r 都成立，而不必读 r 的一行代码。",
    "Draw the theorem as a square. <bookmark mark='a'/> Start":
        "把这条定理画成一个正方形。<bookmark mark='a'/>从一个列表开始，把它反转，再把每个元素平方；或者先平方，再反转。<bookmark mark='b'/>两条路径汇合了。"
        "<bookmark mark='c'/>我们的性质测试尝试了四种重排：反转、取前三个、隔一个取一个、轮转，用的是随机列表和随机的二次函数 f。<bookmark mark='d'/>这条定律每次都成立。"
        "在第14部分我们只测试了线性函数；这个推导说明了为什么那从来就没必要。这条定理对 f 毫无要求。",
    "Wadler's paper of nineteen eighty-nine turned this into a":
        "瓦德勒1989年的论文把这变成了一种方法：写下一个类型，读出它的定理。拿 sort 来说，它接受一个比较函数。<bookmark mark='a'/>它的类型说，相关的比较函数给出相关的排序。"
        "<bookmark mark='b'/>取 R 为 f 的图像，两个比较函数相关，当比较 x 和 y 与比较 f x 和 f y 给出同样的答案。<bookmark mark='c'/>所以对一个保持并反映次序的 f，"
        "映射和排序可以交换。<bookmark mark='d'/>这个条件很要紧。我们的测试为平方函数找到了这个列表，而平方不是单调的：负 15 比负 6 小，但它的平方更大。<bookmark mark='e'/>"
        "先排序再平方，列表就乱了序；先平方再排序，它就是有序的。对于 2x 加 1，这条定律在每个列表上都成立。",
    "Free theorems hold only while the language keeps its side":
        "免费定理只有在语言守住它那一方的约定时才成立。<bookmark mark='a'/>这个 Java 方法有恒等函数的类型，但它在运行时检查实参的类型，遇到字符串就返回别的东西。"
        "免费定理说它必须是恒等函数，而它不是。<bookmark mark='b'/>一般递归也会让这些定理变形：现在每个类型都包含底元，瓦德勒证明了这时它们需要 f 是严格的。"
        "Haskell 的 seq 能把底元和一个函数区分开，让它们变形得更厉害。<bookmark mark='c'/>在约定成立的地方，它是有回报的。GHC 用一条改写规则融合列表流水线，"
        "foldr 作用于 build，它的正确性就是一条免费定理；模块也可以安全地替换它们隐藏的表示，就像雷诺兹的计数器那样。",
    # ------------------------------------------------------------------ s08_axiomatic
    "Chapter seven. Hoare logic, proved sound. Why should we":
        "第七章：霍尔逻辑，证明其可靠。我们为什么应该相信这些规则？",
    "Part fifty-four used Hoare's rules to prove programs":
        "第54部分用霍尔的规则证明程序是正确的。但这些规则只是纸上的符号。为什么要相信它们？<bookmark mark='a'/>一个三元组可以是可推导的：由规则搭建出来，比如这个由两条"
        "赋值组成的序列。<bookmark mark='b'/>它也可以是为真的：程序的每一次运行，只要从满足 P 的状态出发并且结束了，就结束在满足 Q 的状态里。<bookmark mark='c'/>"
        "真由操作语义定义，也就是第一章的步骤，如今用于命令。<bookmark mark='d'/>可靠性说每个可推导的三元组都为真。而斯蒂芬·库克在1978年证明了逆命题，"
        "附带一个我们之后会讲到的精确的前提：每个为真的三元组都可推导。",
    "First, the meaning of commands, in big steps. A state,":
        "首先是命令的含义，用大步表示。一个状态 sigma 给每个变量一个值。<bookmark mark='a'/>赋值更新一个变量。顺序组合先运行第一条命令，然后从第一条停下的地方运行第二条。"
        "<bookmark mark='b'/>测试为假的循环立刻停止。<bookmark mark='c'/>测试为真的循环把循环体运行一次，然后再次运行整个循环。<bookmark mark='d'/>注意，循环在它自己的前提里"
        "又出现了。关于循环的证明不能对程序做归纳，因为程序不会变小；它要对这次运行的推导做归纳，而推导会变小。",
    "Soundness is proved by induction on the derivation of the":
        "可靠性是对三元组的推导做归纳来证明的，每条规则一种情形。<bookmark mark='a'/>先看赋值，那条倒着走的规则。假设状态满足把 x 换成 e 之后的 Q。<bookmark mark='b'/>"
        "也就是说，这个断言在 sigma 中求值为真。<bookmark mark='c'/>一条代换引理，对断言做归纳来证明，把代换移进状态里：一旦 x 被更新为 e 的值，Q 就为真。"
        "<bookmark mark='d'/>所以更新后的状态满足 Q。<bookmark mark='e'/>而按赋值规则，这个更新后的状态是唯一可能的终止状态。<bookmark mark='f'/>顺序组合通过中间状态"
        "把两个假设串起来，而推论规则是纯粹的逻辑。",
    "The loop rule is the heart of the proof. Our outer":
        "循环规则是这个证明的核心。我们的外层假设是：循环体在不变量和测试都为真时开始，会保持不变量。我们必须证明循环保持它，并且在测试为假时离开。<bookmark mark='a'/>"
        "把阶乘写成一个循环，不变量是：x 不是负的，并且 y 乘以 x 的阶乘等于 3 的阶乘。<bookmark mark='b'/>从 x 等于 3 开始运行。<bookmark mark='c'/>循环体的每一遍"
        "都在测试为真、不变量成立时开始，所以外层假设再次给出不变量。<bookmark mark='d'/>当测试失败时，循环停下，此时不变量成立而测试不成立：y 是 6。<bookmark mark='e'/>"
        "证明用一个内层归纳做同样的事，对循环这次运行的推导做归纳。如果循环立刻停下，不变量仍然成立。否则循环体保持它，而运行的剩余部分有一个更短的推导。",
    "The same theorem can be proved against chapter two's":
        "同一条定理也可以对照第二章的指称来证明。<bookmark mark='a'/>在那里，一个循环的含义是一个泛函 phi 的最小不动点：做测试，然后要么运行循环体再继续，要么停下。"
        "<bookmark mark='b'/>称一个含义 w 是安全的，如果从任何满足不变量的状态出发，只要它给出答案，给出的答案就满足不变量而不满足测试。<bookmark mark='c'/>底元是安全的："
        "它从不给出答案。<bookmark mark='d'/>由循环体的假设，phi 保持安全性。<bookmark mark='e'/>所以克莱尼链上的每个近似都是安全的。<bookmark mark='f'/>"
        "安全性是一个在链的极限下封闭的性质，所以极限是安全的，<bookmark mark='g'/>而这个极限就是循环。这就是斯科特的不动点归纳；它恰恰又是第四章的可容许性。",
    "Now the converse. Cook's idea is to use the weakest":
        "现在看逆命题。库克的想法是使用最弱自由前置条件：从这些状态出发，命令要么结束在 Q 中，要么永远运行下去。<bookmark mark='a'/>对命令做归纳，以 wlp 打头的三元组"
        "是可推导的。<bookmark mark='b'/>在 while 的情形里，那个没人必须去发明的不变量，就是循环自己的 wlp，<bookmark mark='c'/>而循环规则的两个前提都为真。"
        "<bookmark mark='d'/>一个为真的三元组意味着 P 蕴含 wlp，<bookmark mark='e'/>所以推论规则完成了证明。<bookmark mark='f'/>为什么只是相对的？一个带 skip 的为真"
        "三元组不过是一个为真的算术命题，而由哥德尔，没有哪个证明系统能把它们全部列出来。所以库克假定为真的断言是给定的，并且断言能表达 wlp。<bookmark mark='g'/>"
        "第54部分的工具恰好就是在处理这些断言；这一章说明了它们的规则为什么是对的。",
    # ------------------------------------------------------------------ s09_effects
    "Chapter eight. Effects and monads. How can a mathematical":
        "第八章：效应与单子。一个数学含义怎么能描述一个会做事情的程序？",
    "Every meaning so far was pure: an integer expression":
        "到目前为止，每个含义都是纯的：一个整数表达式指称一个整数。<bookmark mark='a'/>真实的程序做得更多。12 除以 b 可能会失败。<bookmark mark='b'/>"
        "一个计数器可能被读取和修改。<bookmark mark='c'/>一个选择可能给出好几个答案。<bookmark mark='d'/>这些都不指称一个数。失败需要一个额外的值；状态需要一个函数，"
        "从旧的计数器得到一个结果和一个新的计数器；选择需要一个列表。<bookmark mark='e'/>Eugenio Moggi 在1989年和1991年统一地说明了这一点：把值和计算区分开，"
        "并让一个整数的计算的含义是 T 作用于整数的一个元素，其中 T 是一种叫作单子的结构。每一种效应都是对 T 的一种选择。",
    "A monad is three things. <bookmark mark='a'/> A type":
        "一个单子由三样东西组成。<bookmark mark='a'/>一个类型构造器 T，以及 return，它把一个值变成一个除此之外什么都不做的计算。<bookmark mark='b'/>还有 bind，"
        "它运行一个 A 的计算，并把它的值交给一个产生 B 的计算的函数。<bookmark mark='c'/>把一个程序想成由若干级组成的流水线，每一级接受一个普通的值，产生一个计算。"
        "<bookmark mark='d'/>bind 就是级与级之间的接头：它拆开上一级产生的东西，喂给下一级，而效应完全住在这些接头里。<bookmark mark='e'/>菲利普·瓦德勒1992年的论文"
        "把这带进了编程。Haskell 里的 do 块就是 bind，只是横过来写。",
    "Three monads, one shape of program. <bookmark mark='a'/>":
        "三个单子，同一种形状的程序。<bookmark mark='a'/>对异常来说，T 作用于 A 是一个 A 或者 Nothing，而一旦某一级失败了，bind 就跳过剩下的部分。<bookmark mark='b'/>"
        "12 除以 0 得到 Nothing；除以 3，加 1 之后得到 5；除以 4，得到 4。<bookmark mark='c'/>对状态来说，T 作用于 A 是一个函数，从计数器得到一个结果和一个新的计数器，"
        "而 bind 把计数器一路传下去。<bookmark mark='d'/>从 0 开始 tick 两次，再返回计数器的 10 倍：得到 20，计数器停在 2。<bookmark mark='e'/>对非确定性来说，"
        "T 作用于 A 是一个列表，而 bind 对每一种可能性各运行一次剩下的部分。<bookmark mark='f'/>从 1 到 4 中选 b，得到 12、6、4 和 3。<bookmark mark='g'/>"
        "变的只有接头。",
    "A monad must obey three laws, which make sequencing":
        "一个单子必须遵守三条定律，它们让顺序组合表现良好。<bookmark mark='a'/>左单位律：返回一个值再绑定它，就是直接应用下一级。<bookmark mark='b'/>右单位律："
        "绑定到 return 什么都不改变。<bookmark mark='c'/>结合律：怎样给流水线加括号都无关紧要。<bookmark mark='d'/>像第二章那样，用代数检查状态的第一条定律。<bookmark mark='e'/>"
        "展开 bind：一个关于计数器的函数，它运行 return a，并把结果和新的计数器交给 k。<bookmark mark='f'/>return a 在给定 s 时，是序对 a 和 s。<bookmark mark='g'/>"
        "所以 x 是 a，s 撇是 s。<bookmark mark='h'/>而一个把 k a 作用于自己参数的函数，就是 k a 本身。定律成立；另外两条也用同样的方法检查。",
    "There is a tidier way to state the laws. <bookmark":
        "还有一种更整洁的方式来陈述这些定律。<bookmark mark='a'/>把两个带效应的函数复合起来，f 从 A 到 B 的计算，g 从 B 到 C 的计算，做法是运行 f，再把它的结果绑定到 g。"
        "这就是 Kleisli 复合，以 Heinrich Kleisli 命名。<bookmark mark='b'/>拿左单位律来说，<bookmark mark='c'/>用新的复合重写它，<bookmark mark='d'/>"
        "再去掉 a：return 与 f 复合就是 f。<bookmark mark='e'/>同样，f 与 return 复合是 f，而复合满足结合律。<bookmark mark='f'/>带效应的函数构成一个范畴，"
        "return 是它的恒等。<bookmark mark='g'/>而这就是 Moggi 的语义：一个带有类型为 A 的自由变量、结果类型为 B 的程序指称一个 Kleisli 箭头，而 let 就是 bind。",
    "Gordon Plotkin and John Power, in two thousand and one,":
        "戈登·普洛特金和 John Power 在2001年从另一端出发：一种效应由它的运算给出。<bookmark mark='a'/>这里是 choose，它返回一个布尔值，以及 fail，它从不返回。"
        "<bookmark mark='b'/>用到它们的程序是一棵树：每个运算一个结点，每个答案一个分支，叶子上是值。<bookmark mark='c'/>马蒂亚·普雷特纳和普洛特金在2009年加入了处理器。"
        "处理器说明每个运算做什么，并把程序的剩余部分作为续延交给它，而运行程序就是折叠这棵树。<bookmark mark='d'/>一个处理器收集每一个结果：6 和 4。<bookmark mark='e'/>"
        "另一个做回溯：先试真，只有当它失败时，才试假。同一棵树：6。<bookmark mark='f'/>程序从未改变，变的只有它的处理器。OCaml 5 就是这样搭建它的效应的；异常、生成器和"
        "异步代码都可以写成处理器。",
    # ------------------------------------------------------------------ s10_dependent
    "Chapter nine. Dependent types. What if types could":
        "第九章：依赖类型。如果类型可以提到值，而证明就是程序，会怎样？",
    "Part 14 gave a first glimpse of types that mention":
        "第14部分让我们初次瞥见了提到值的类型；这里来看这个想法能走多远。<bookmark mark='a'/>想象一个类型族，A 里的每个 x 对应一个类型，每个都是立在它那个点上方的一根柱子。"
        "<bookmark mark='b'/>一个依赖函数从每一根柱子里挑出一个元素，所以它的结果类型依赖于它的实参。它的类型是一个大写的 Π。<bookmark mark='c'/>当 B 不提到 x 时，"
        "每根柱子都一样，Π 就是普通的箭头。<bookmark mark='d'/>一个依赖序对是一根柱子里的一个点：一个值 x，以及 B x 的一个元素。它的类型是一个大写的 Σ，<bookmark mark='e'/>"
        "而当 B 是常量时，就是普通的积。<bookmark mark='f'/>佩尔·马丁-洛夫的类型论始于1972年，就建立在这两者之上。",
    "Part 14's example, now in full: a list that carries its":
        "第14部分的例子，现在完整地来看：一个在类型里带着自己长度的列表。<bookmark mark='a'/>Vec A n 是恰好有 n 个 A 的元素的列表的类型。<bookmark mark='b'/>"
        "nil 的长度是 0，而 cons 作用于一个长度为 n 的向量，得到长度 n 加 1。<bookmark mark='c'/>现在 head 可以要求一个长度为 n 加 1 的向量，<bookmark mark='d'/>"
        "而 append 在给定长度 m 和 n 时，返回长度 m 加 n。<bookmark mark='e'/>把 7 和 2 接到 5 上。<bookmark mark='f'/>检查器计算出类型：2 加 1，也就是 3。"
        "<bookmark mark='g'/>而对空向量取 head，并不像在大多数语言里那样是运行时的崩溃；它在程序运行之前就被拒绝了，因为没有哪个 n 加 1 等于 0。",
    "Part 14 met the Curry–Howard correspondence. <bookmark":
        "第14部分遇到过柯里–霍华德对应。<bookmark mark='a'/>A 且 B 的证明是一个序对，A 或 B 的证明是其中之一的带标签的证明，A 蕴含 B 的证明是一个函数，而假是空类型。"
        "<bookmark mark='b'/>对所有 x，P x，是一个依赖函数：对每个 x 都有一个证明。<bookmark mark='c'/>存在一个 x 使得 P x，是一个依赖序对：一个见证，以及关于它的一个证明。"
        "<bookmark mark='d'/>而相等是一个类型，它唯一的构造子 refl 证明一个值等于它自己。<bookmark mark='e'/>对每个 n 都有一个更大的 m：证明是一个返回 n 加 1 的函数，"
        "带着一个它更大的证明。<bookmark mark='f'/>证明就是程序，而检查证明就是类型检查。",
    "Some theorems are proved by computing. <bookmark":
        "有些定理是靠计算来证明的。<bookmark mark='a'/>对第一个参数做递归来定义加法：0 加 n 是 n，m 的后继加 n 是 m 加 n 的后继。<bookmark mark='b'/>命题：2 加 2 等于 4，"
        "而证明就是 refl，它证明一个东西等于它自己。<bookmark mark='c'/>因为检查器会计算。2 加 2 是 1 加 2 的后继，<bookmark mark='d'/>也就是 0 加 2 的后继的后继，"
        "<bookmark mark='e'/>也就是带着两个后继的 2，<bookmark mark='f'/>4。两边到达同一个范式。<bookmark mark='g'/>但 n 加 0 算不下去：加法看的是它的第一个参数，"
        "而 n 是一个变量。<bookmark mark='h'/>它的证明是一个递归函数，它的第二种情形在一个更小的 n 上调用自己。归纳就是递归。",
    "Type checking must decide when two types are equal.":
        "类型检查必须判定两个类型什么时候相等。<bookmark mark='a'/>当它在期望长度 3 的地方遇到一个长度为 2 加 1 的向量时，它把两者都正规化，再作比较。<bookmark mark='b'/>"
        "这只有在正规化总会停下时才行得通。允许一个死循环的定义，bad 等于 bad，它就具有任何类型，连假也不例外：这个逻辑会证明一切，而检查会永远运行下去。<bookmark mark='c'/>"
        "所以证明助手只接受它们能看出会终止的函数，比如在结构上更小的参数上做递归。<bookmark mark='d'/>每个良类型的项都有范式，这是用第五章的方法证明的，也就是泰特的方法，"
        "让-伊夫·吉拉尔在1972年把它推广到了多态。<bookmark mark='e'/>马丁-洛夫1984年的理论带有外延相等，让类型检查变得不可判定；内涵的版本则让它保持可判定。",
    "This is why a proof assistant can be trusted. <bookmark":
        "这就是为什么证明助手可以信任。<bookmark mark='a'/>蒂埃里·科康和热拉尔·于埃1988年的构造演算成了 Coq 证明助手的核心，后来又扩展了归纳类型。<bookmark mark='b'/>"
        "围绕这个核心的是一个庞大、巧妙、不受信任的层：策略、自动化，以及一个展开器（elaborator），它补上用户省略的东西。它唯一的输出是一个证明项。<bookmark mark='c'/>"
        "内核是一个小小的类型检查器，它检查这个项，而只有内核必须是对的。<bookmark mark='d'/>这又是第54部分那个小而可信的内核的想法，而一个像这样的内核检查着第54部分那个"
        "经过验证的编译器 CompCert 的证明。",
    # ------------------------------------------------------------------ s11_concurrency
    "Chapter ten. Processes and channels. What does a program":
        "第十章：进程与通道。一个程序在和别的程序交谈时意味着什么？",
    "Chapter five compared machines; now we build them from":
        "第五章比较了机器；现在我们用零件来搭建它们。罗宾·米尔纳1980年的通信系统演算，CCS，语法非常小。<bookmark mark='a'/>一个动作是一个名字 a，它的补 a 拔，"
        "或者 tau，一个静默的内部步。<bookmark mark='b'/>一个进程是 0，它什么都不做；一个后面跟着进程的动作；一个选择；两个并行的进程；一个限制，它让一个名字成为私有的；"
        "或者一个具名进程，它可以调用自己。<bookmark mark='c'/>一个顾客投出一枚硬币，然后等着茶。<bookmark mark='d'/>一台机器接受一枚硬币，提供茶，然后重新开始。"
        "<bookmark mark='e'/>并排放在一起，互补的端口连接起来，而限制把两个名字对其他所有人隐藏起来。<bookmark mark='f'/>托尼·霍尔1978年的 CSP 同样用交换同步消息的进程"
        "来搭建程序；Go 的通道就源自它。",
    "The meaning of a process is a labelled transition system,":
        "一个进程的含义是一个带标迁移系统，由第一章那种风格的规则给出。<bookmark mark='a'/>一个动作前缀可以做它的动作，然后变成剩下的部分。<bookmark mark='b'/>"
        "一个选择可以做任何一边能做的事，而另一边被丢弃。<bookmark mark='c'/>在并行中，任何一边都可以单独移动，另一边不变。<bookmark mark='d'/>核心是通信：如果一边能做 a，"
        "另一边能做 a 拔，它们就一起走一个静默的 tau 步，两边同时移动。<bookmark mark='e'/>而一个受限制的名字不能从外面使用：a 或 a 拔上的移动被阻断，但 tau 可以通过。"
        "<bookmark mark='f'/>这五条规则，加上它们的镜像，再加一条展开具名进程的规则，就是 CCS 的全部。",
    "Let us derive the customer's first step. <bookmark":
        "我们来推导顾客的第一步。<bookmark mark='a'/>由动作规则，展开后的顾客可以做 coin 拔，然后变成 tea，再变成 0。<bookmark mark='b'/>机器可以做 coin，然后变成 tea 拔，"
        "再变成 V。<bookmark mark='c'/>通信规则把它们连起来：它们一起走一个 tau 步，到达两个剩余部分。<bookmark mark='d'/>限制让 tau 通过，所以这个封闭系统移动了。"
        "一个系统的每一步都是一个像这样的小证明。<bookmark mark='e'/>这个封闭系统只有两个 tau 步，先是硬币，然后是茶，之后什么也不会再发生。<bookmark mark='f'/>"
        "第五章的互模拟在这里适用，把 tau 步当作不可观察的：这是米尔纳的弱互模拟。从外面看，这个系统等价于 0。<bookmark mark='g'/>而强互模拟等价被 CCS 的每一个算子保持，"
        "所以相等的部件可以在任何系统里互换。",
    "In CCS the wiring is fixed: who can talk to whom never":
        "在 CCS 里，连线是固定的：谁能和谁交谈，永远不变。<bookmark mark='a'/>米尔纳、Joachim Parrow 和 David Walker 1992年的 π 演算，在名字上传送名字。在通道 x 上"
        "发送 y；在 x 上接收一个名字，把它叫作 z。它们相遇时，接收者用 y 代替 z 继续下去。<bookmark mark='b'/>现在，一个服务器创建一个私有通道 r，<bookmark mark='c'/>"
        "并且想通过公共通道 s 把它发给一个客户端。<bookmark mark='d'/>首先，r 的作用域被扩大到包括客户端，这是允许的，因为客户端没有提到 r。<bookmark mark='e'/>"
        "然后消息传了过去，客户端拿到了 r。作用域外溢了：两者现在共享一条私有的链路，别人谁也够不着。<bookmark mark='f'/>进程之间的链路是数据。一个携带着自己回复通道的请求，"
        "就像在 Go 里那样，恰恰就是这个。",
    "Concurrency's classic failure is now a precise question.":
        "并发的经典故障，现在成了一个精确的问题。<bookmark mark='a'/>一把锁，就像第33部分里那样，是一个可以被获取、然后被释放、永远如此的进程。<bookmark mark='b'/>"
        "线程一先获取锁 a，再获取 b，然后把两把都释放；线程二先获取 b，再获取 a。<bookmark mark='c'/>把封闭系统的每个状态画成一个点：横向是线程一走了多远，纵向是线程二。"
        "每一次获取和释放都是一个 tau 步。<bookmark mark='d'/>在两个线程会持有同一把锁的地方，没有状态。<bookmark mark='e'/>从起点开始探索：有19个状态是可达的。"
        "<bookmark mark='f'/>其中两个无路可走。一个是终点。另一个是死锁：每个线程持有一把锁，等着另一个线程的那把。死锁就是一个可达的、卡住了却没有完成的状态，"
        "而找到它是一次搜索，这正是第54部分的模型检验器所做的事。<bookmark mark='g'/>会话类型走得更远：一个通道的类型就是它的协议，就像第43部分的请求和回复，"
        "而建立在它们之上的一些类型系统能在程序运行之前就排除这样的死锁。",
    # ------------------------------------------------------------------ s12_frontier
    "Chapter eleven, the frontier. Can a whole real language":
        "第十一章，前沿。一整门真实的语言，能不能被赋予一个机器可以检查的含义？",
    "For decades semantics was done on paper, for small":
        "几十年来，语义学都是在纸上、为小语言而做的。<bookmark mark='a'/>后来，泽维尔·勒鲁瓦的 CompCert 在 Coq 证明助手里给 C 的一个很大的子集赋予了语义，并证明了它的"
        "编译器保持这个语义。<bookmark mark='b'/>CakeML 为 ML 的一种方言做了同样的事，它带有一个能编译自己的经过验证的编译器。<bookmark mark='c'/>而 WebAssembly 从它的"
        "第一个版本起就用第一章那样的小步规则来规定，它的类型系统后来在 Isabelle 里被证明是可靠的。<bookmark mark='d'/>仍然缺少的，是 C 的并发的完整语义、第33部分"
        "那个凭空出现的值的问题，以及人们实际在写的几乎每一种语言。",
    "The deepest frontier is about equality itself. <bookmark":
        "最深的前沿是关于相等本身的。<bookmark mark='a'/>在马丁-洛夫的类型论，也就是第九章依赖类型的基础里，a 等于 b 的一个证明本身就是一个值，属于某个类型。"
        "<bookmark mark='b'/>弗拉基米尔·沃埃沃茨基的一价公理说，等价的类型就是相等的，这正是数学家早已在用的推理方式。<bookmark mark='c'/>让它有意义的模型把相等读作"
        "一个空间里的路径，而同样两点之间的两条路径不一定是同一条路径。这就是同伦类型论，而几年之后的立方类型论让一价性能够计算。",
    "Open problems. <bookmark mark='a'/> Fully abstract models":
        "开放问题。<bookmark mark='a'/>真实语言的完全抽象模型，它恰好把没有哪个上下文能区分开的程序等同起来。<bookmark mark='b'/>一个 C 和 C++ 的内存模型，"
        "没有凭空出现的结果，而编译器仍然能遵守它。<bookmark mark='c'/>一种能把状态、异常、概率和并发组合起来的效应语义。<bookmark mark='d'/>还有在语言演变时依然可以维护的"
        "语义。<bookmark mark='e'/>这一部分的研究题是其中第二个：一种 C 的松弛内存语义，它禁止凭空出现的值，仍然允许真实编译器所做的优化，并且被证明两者都做到了。",
    # ------------------------------------------------------------------ s13_outro
    "What we built in this part. Three operational semantics":
        "我们在这一部分搭建了什么。一门语言的三种操作语义，小步、大步和 CEK 机，在我们试过的每个程序上都一致。一个指称语义，其中递归是由克莱尼链到达的最小不动点。"
        "充分性与完全抽象，以及 PCF 定义不出来的并行或。用互模拟和逻辑关系判定的等价，以及它们给出的正规化证明。参数性的免费定理；被证明可靠的霍尔逻辑；作为单子的效应；"
        "依赖类型；还有相互通信的进程。贯穿始终的是一个想法：含义是组合的，整体的含义由各部分的含义搭建而成。",
    "Where this comes back. Part 59's distributed algorithms":
        "它们会在哪里再出现。第59部分的分布式算法就是第十章那样的进程。第60部分把硬件描述成程序，它们的含义必须符合一个规约。第61部分把证明当作一种研究方法。"
        "而回头看，第54部分的验证和第55部分的可信编译器，都建立在这一部分的语义之上。",
    "In practice. Write a language's rules down before":
        "在实践中。在实现一门语言之前，先把它的规则写下来。用两个必须一致的解释器互相充当测试预言。用等价来为一次重构辩护，而不是靠希望。把效应放进类型里，"
        "让错误、状态和异步都显式可见。而当利害关系足够大时，把语义机械化。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：给我们的三个解释器都加上异常，并检查它们仍然一致。最后一道标了星号，"
        "是一道研究题：一个 C 的内存模型，它禁止凭空出现的值，同时仍然让编译器能做优化。",
    "Next time, Part 59: the theory of distributed computing.":
        "下一次，第59部分：分布式计算的理论。当每个进程只能看到它的邻居，或者有些会崩溃，或者有些会撒谎时，n 个进程能计算什么？有些答案是像 n 的迭代对数那样精确的下界，"
        "而其中一个来自代数拓扑。",
    "The books and papers this part follows are on screen and":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
