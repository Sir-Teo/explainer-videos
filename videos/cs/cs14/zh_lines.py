"""Chinese narration for cs14: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第14部分：λ 与类型"

CHAPTERS = {
    "Hook": "一种只由函数构成的语言",
    "Terms": "1. 项、变量与代换",
    "Beta": "2. 归约与范式",
    "Church": "3. 无中生有的编程",
    "Recursion": "4. 没有名字的递归",
    "Strategies": "5. 求值策略",
    "Confluence": "6. 丘奇–罗瑟，以及德布鲁因",
    "Types": "7. 简单类型",
    "Safety": "8. 良类型的程序不会出错",
    "Normalization": "9. 每个有类型的程序都会停",
    "Inference": "10. 欣德利–米尔纳推断",
    "SystemF": "11. 多态与免费定理",
    "CurryHoward": "12. 命题即类型",
    "Dependent": "13. 依赖类型与线性类型",
    "Data": "14. 数据、子类型与渐进类型",
    "Frontier": "15. 前沿：类型论的边缘",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Here is the Job once more, written in a new language":
        "这又是任务，用一种新语言写成：λ-核心，这一部分要搭建的语言。它有函数、列表和序对，其余的不值一提。<bookmark mark='a'/>注意少了什么。"
        "没有一个类型标注。bump 把表里一个单词的计数加一，count 遍历所有单词，job 把各部分组合起来。<bookmark mark='b'/>可是编译器知道每个函数的类型。"
        "它自己推出了它们，用了几百个微小的步骤。<bookmark mark='c'/>其中有些类型含有一个变量，写作 'a。bump 适用于单词，但也同样适用于数字，或者任何能比较"
        "相等的东西。这一点机器也发现了。",
    "And underneath the lambda core there is something even smaller.":
        "在 λ-核心之下，还有更小的东西。<bookmark mark='a'/>这是二加三，只用函数写成：没有数字，没有加法，只有函数作用于函数。<bookmark mark='b'/>一条规则，"
        "一遍又一遍地应用，改写它，<bookmark mark='c'/>直到它停下。结果是数字五，或者说，一个把 f 作用于 x 五次的函数。阿隆佐·丘奇在二十世纪三十年代发现，"
        "这一条规则足以计算一切可计算的东西。第1部分见过他的 λ 演算；这一部分要认真对待它。",
    "Here is where we are going.":
        "我们要去的地方是这样的。<bookmark mark='a'/>数字、布尔值、列表和递归，全部只用函数搭建。<bookmark mark='b'/>为什么求值的顺序能决定程序是否结束，又为什么"
        "它永远改变不了答案。<bookmark mark='c'/>类型，以及一个证明：良类型的程序不会出错。<bookmark mark='d'/>机器怎样推断出没有人写过的类型。<bookmark "
        "mark='e'/>还有这门学科最深的惊喜：一个类型就是一条定理，而这个类型的程序就是它的证明。",
    "This is Part 14 of Computer Science, Built":
        "这是《计算机科学，从零搭建》的第14部分，属于第三幕“和机器对话”。<bookmark mark='a'/>这一部分讲：λ 项、代换和 β 归约。丘奇编码，以及 Y 组合子。"
        "求值策略，以及丘奇–罗瑟定理。简单类型、安全性定理和正规化。欣德利–米尔纳推断、System F 和免费定理。还有柯里–霍华德对应，以及依赖类型、线性类型和渐进类型。",
    # ------------------------------------------------------------------ Terms
    "Chapter one. Terms, variables and substitution.": "第一章。项、变量与代换。",
    "Church's lambda calculus has exactly three kinds of term.":
        "丘奇的 λ 演算恰好有三种项。<bookmark mark='a'/>变量。抽象，λx. t，它是一个参数为 x、函数体为 t 的函数，不写名字。还有应用，f 作用于 a。整个语言就"
        "这些。<bookmark mark='b'/>项其实是树。这是 λx. x x，作用于 λy. y，再作用于 z。应用结点画成 @ 符号。<bookmark mark='c'/>两条约定让书写简短：应用向左"
        "结合，所以 f a b 表示 f a 再作用于 b；而 λ 的函数体尽可能向右延伸。",
    "Variables come in two kinds.":
        "变量分两种。<bookmark mark='a'/>在 λx. f x y 中，x 是约束的：它指向引入它的那个 λ，就像函数的参数。<bookmark mark='b'/>f 和 y 是自由的。它们指向项"
        "之外的东西，项的含义取决于它们最终是什么。<bookmark mark='c'/>约束变量叫什么名字无关紧要。λx. x 和 λy. y 是同一个函数，恒等函数；只在约束变量名上"
        "不同的项叫作 α 等价，正如 f(x) 对 x 的积分就是 f(t) 对 t 的积分。",
    "Computation in the lambda calculus is substitution":
        "λ 演算里的计算就是代换：要应用一个函数，就用实参替换它的参数。这比看上去微妙。<bookmark mark='a'/>拿 λx. λy. x 来说：一个接受两个参数、返回第一个的"
        "函数。把它作用于一个自由变量 y。<bookmark mark='b'/>天真地用 y 替换 x，得到 λy. y：恒等函数。自由的 y 被内层的 λ 捕获了，含义变了。<bookmark "
        "mark='c'/>正确的答案是先把约束的 y 改名为 y'，得到 λy'. y：仍然是一个忽略参数、返回 y 的函数。<bookmark mark='d'/>避免捕获的代换由这些规则定义，"
        "条件就在最后一条里。把它弄对，是每个编程语言实现者遇到的第一个错误，也是闭包存在的原因，第15部分会讲到。",
    # ------------------------------------------------------------------ Beta
    "Chapter two. Reduction and normal forms.": "第二章。归约与范式。",
    "The calculus computes with a single rule, called beta reduction.":
        "这个演算只用一条规则计算，叫作 β 归约。<bookmark mark='a'/>凡是一个 λ 作用于一个实参，这一对就是一个可约式。<bookmark mark='b'/>把它替换成函数体，"
        "并用实参代换参数。<bookmark mark='c'/>可约式可以出现在更大的项里的任何位置，甚至在另一个 λ 的函数体内，而任何可约式都可以在任何时候归约。<bookmark "
        "mark='d'/>λx. x x 作用于 z，变成 z z。就这么多。",
    "Here is a step on the tree.":
        "这是树上的一步。<bookmark mark='a'/>整个项是一个可约式：λx. x x，作用于一个本身也是可约式的实参。<bookmark mark='b'/>归约外层的那个，把实参代入 x 的"
        "两处出现。实参被复制了，连同它的可约式：现在有两个。<bookmark mark='c'/>归约第一个副本，还剩一个。这种复制是后面大部分内容的根源：各种策略之间代价的"
        "差别，以及编译器为什么要共享工作而不是重复它。",
    "Here is two plus three again, slowly.":
        "再看一遍二加三，慢一点。<bookmark mark='a'/>数 n 是把 f 作用于 x n 次的函数，而 plus 接受 m 和 n，在 n 次应用之上再作用 f m 次。<bookmark mark='b'/>"
        "每一行归约黄色标出的可约式。先是 plus 一个一个吞下它的参数。然后三作用于 f 和 x，展开成三次 f 的应用，二又在外面加上两次。<bookmark mark='c'/>最后一行"
        "没有可约式了。它是一个范式：答案，f 的五次应用。",
    "Not every term has a normal form.":
        "并不是每个项都有范式。<bookmark mark='a'/>Ω 把 λx. x x 作用于它自己。<bookmark mark='b'/>一步 β 归约得到的恰好是同一个项，下一步还是一样，永远如此。"
        "Ω 没有范式：它是 λ 演算的死循环。<bookmark mark='c'/>更糟的是，有些项沿一条路径有范式，沿另一条却会无限循环。这是一个忽略第一个参数的函数，作用于 Ω "
        "和 z。<bookmark mark='d'/>先归约外层，答案是 z，两步。坚持先归约 Ω，就永远结束不了。<bookmark mark='e'/>所以归约的顺序很重要。第五章会研究它。",
    # ------------------------------------------------------------------ Church
    "Chapter three. Programming with nothing.": "第三章。无中生有的编程。",
    "If the language has nothing but functions, then data must be functions too.":
        "如果语言里只有函数，那么数据也必须是函数。丘奇展示了怎么做。<bookmark mark='a'/>布尔值是在两个东西之间的选择。true 接受两个参数，返回第一个；false 返回"
        "第二个。<bookmark mark='b'/>于是 if b then x else y 根本不需要特殊规则：它就是 b 作用于 x 和 y。<bookmark mark='c'/>p and q 是 p 作用于 q 和 p："
        "如果 p 为真，它选 q；如果 p 为假，它选 p，也就是假。or 是它的镜像。<bookmark mark='d'/>我们的归约器验证了每张表的全部四行，每行四步，每个答案都正是"
        "函数 true 或函数 false 本身。",
    "Numbers are repetitions.":
        "数字就是重复。<bookmark mark='a'/>数 n 是接受 f 和 x、把 f 作用于 x n 次的函数。零一次也不作用，返回 x。一作用一次。二把 x 包在两次 f 的应用里，"
        "依此类推：把每个 f 想象成套在里面那个外面的一个盒子。<bookmark mark='b'/>后继接受一个数 n，让它把 f 作用 n 次，然后在外面再作用一次。",
    "With repetition, arithmetic falls out.":
        "有了重复，算术自然就出来了。<bookmark mark='a'/>plus m n 在 n 次应用之上再作用 f m 次。<bookmark mark='b'/>times m n 拿“把 f 作用 n 次”这个函数，"
        "把它重复 m 次。<bookmark mark='c'/>而幂是最奇怪也最短的：n 作用于 m。把“乘以 m”这个函数作用 n 次，从一开始。<bookmark mark='d'/>我们的归约器计算三加四、"
        "三乘四和二的三次方，分别用六步、九步和十六步 β 归约，每个范式都恰好是预期的数。",
    "Pairs come just as easily.":
        "序对同样容易。<bookmark mark='a'/>a 和 b 的序对是一个等待选择器 s 的函数，它把 a 和 b 交给 s。取第一个就传入选择器 true，取第二个就传入 false。"
        "<bookmark mark='b'/>减法要难一些。一个数能把 f 作用 n 次，却没有办法撤销一次作用。斯蒂芬·克莱尼在 1932 年找到了答案，据说是在看牙医的时候。<bookmark "
        "mark='c'/>改用序对来计数。从 (0, 0) 开始，n 次把序对 (a, b) 换成 (b, b + 1)。n 步之后序对是 (n - 1, n)，它的前一半就是前驱。<bookmark mark='d'/>"
        "它能用，但很慢：n 每增加一，我们的归约器就要多走十步。丘奇数证明了什么是可能的，而不是一种高效的表示。",
    "Lists follow the same pattern.":
        "列表遵循同样的模式。<bookmark mark='a'/>列表是一个有两个参数 c 和 n 的函数。空列表返回 n。头为 h、尾为 t 的列表把 c 作用于 h 和尾部产生的东西。所以列表 "
        "1, 2, 3 就是 c 1 (c 2 (c 3 n))。<bookmark mark='b'/>列表就是它自己的循环：把加法作为 c、零作为 n 交给它，它就把自己加起来了。让数字成立的也是同一个"
        "思想：一个数据结构由你能对它做什么来定义。<bookmark mark='c'/>布尔值、数字、序对和列表，全部由 λ、变量和应用搭建，别无他物。",
    # ------------------------------------------------------------------ Recursion
    "Chapter four. Recursion without names.": "第四章。没有名字的递归。",
    "How can a function call itself, when functions have no names?":
        "函数没有名字，它怎么调用自己？<bookmark mark='a'/>我们想定义阶乘：n 为零时是一，否则是 n 乘以 n 减一的阶乘。<bookmark mark='b'/>可是在 λ 演算里，"
        "没有办法在 fact 自己的定义里写出名字 fact。<bookmark mark='c'/>所以把递归调用变成一个参数。F 接受一个函数 self，返回一个在较小情形下调用 self 的阶乘。"
        "F 是一个普通的 λ 项。<bookmark mark='d'/>我们要的是这样一个函数 fact：F 作用于 fact 之后还是 fact。用数学的语言说，fact 是 F 的不动点。我们只需要一种"
        "找不动点的办法。",
    "Haskell Curry's Y combinator finds them.":
        "哈斯凯尔·柯里的 Y 组合子能找到它们。<bookmark mark='a'/>Y 接受 f，把 λx. f (x x) 作用于它自己。<bookmark mark='b'/>看它在某个 g 上运行。一步代入 g。"
        "<bookmark mark='c'/>下一步进行自作用，出来的是 g，作用于我们刚才那个项。<bookmark mark='d'/>所以 Y g 归约成 g 作用于某个本身等于 Y g 的东西。Y g 是 g "
        "的不动点，对每个 g 都成立。<bookmark mark='e'/>仔细看，它又是 Ω：同样那个无限循环的自作用，只是每个副本外面都包了一层 g，所以循环每转一圈，g 就多一次"
        "使用自己的机会。",
    "Now combine everything so far.":
        "现在把目前的一切组合起来。<bookmark mark='a'/>有了丘奇数、布尔值、乘法和克莱尼的前驱，F 是一个普通的项，而 Y F 就是阶乘。我们的归约器对 n 从零到四求值，"
        "答案是一、一、二、六和二十四。<bookmark mark='b'/>递归，来自没有名字的函数。<bookmark mark='c'/>但看看代价。四的阶乘要一万多步，n 每多一，工作量就成倍"
        "增长。正规序在求值之前复制实参，然后分别求值每个副本。下一章讲的正是这个。",
    "One wrinkle.":
        "还有一个小问题。<bookmark mark='a'/>真实的语言大多在调用函数之前先求值实参，这叫传值调用。在传值调用下，Y F 永远不停：它在 F 有机会决定是否需要之前就去"
        "求值 x x，而那个自作用会无限展开。<bookmark mark='b'/>解决办法是 Z 组合子，它把自作用包在一个 λ 里，让它只在真正被调用时才求值。在传值调用下，Z F 会停。"
        "<bookmark mark='c'/>最后一点观察：每个 λ 项都有不动点，同样的技巧作用在程序而不是函数上，就能造出一个打印自身源代码的程序。那是克莱尼的递归定理，第25"
        "部分会再遇到它。",
}

ZH.update({
    # ------------------------------------------------------------------ Strategies
    "Chapter five. Evaluation strategies.": "第五章。求值策略。",
    "A term usually contains several redexes":
        "一个项通常含有好几个可约式，而规则并没有说先归约哪一个。由策略来决定。<bookmark mark='a'/>正规序总是取最左、最外层的可约式，即使在 λ 内部。<bookmark "
        "mark='b'/>应用序取最左、最内层的：实参先于接收它的函数。<bookmark mark='c'/>编程语言从不在 λ 内部归约，因为函数体只在被调用时才运行。传名调用把实参"
        "不经求值地传过去，ALGOL 60 就是这样。<bookmark mark='d'/>传值调用先求值每个实参：C、Java、OCaml 和 Python 都是。<bookmark mark='e'/>而传需调用，"
        "也就是惰性求值，是带记忆的传名调用：实参在第一次需要时求值，结果被重用。Haskell 就是这样。",
    "Here is the term from chapter two":
        "这是第二章的那个项：一个返回第一个参数的函数，作用于 a 和 Ω。<bookmark mark='a'/>正规序和传名调用先归约外层，两步结束，答案是 a。应用序和传值调用坚持"
        "在调用之前求值 Ω，永远结束不了。<bookmark mark='b'/>那个函数根本不需要 Ω。会等待的策略在寻找答案上从不更差，本章最后会把这一点说清楚。",
    "Strategies also differ in cost.":
        "策略在代价上也不同。<bookmark mark='a'/>我们在一台计数 β 步数的机器上，用同一个实参，三乘三，运行三个函数。<bookmark mark='b'/>当函数体使用参数三次时，"
        "传名调用把实参求值了三遍：四十三步对三十三步。<bookmark mark='c'/>当函数体根本不用它时，传值调用照样求值，就输了。<bookmark mark='d'/>传需调用两头都赢："
        "它至多求值一次实参，而且只在需要时求值。克里斯托弗·沃兹沃思在 1971 年描述了这种共享，Haskell 就是这样运行的。",
    "One theorem settles which strategy is safest.":
        "有一条定理裁定了哪种策略最安全。<bookmark mark='a'/>如果一个项有范式，正规序就一定能到达它。柯里和费斯在 1958 年证明了这条标准化定理。<bookmark "
        "mark='b'/>所以正规序从不错过存在的答案。它可能浪费工作，而真实的语言大多为了速度和可预测性选择传值调用，接受有些本不必循环的程序会循环。<bookmark "
        "mark='c'/>但两种策略会不会找到不同的答案？那是下一章的主题。",
    # ------------------------------------------------------------------ Confluence
    "Chapter six. Church Rosser, and de Bruijn.": "第六章。丘奇–罗瑟，以及德布鲁因。",
    "Strategies can disagree about whether we finish.":
        "策略可能在“是否结束”上意见不一。它们会在答案上意见不一吗？<bookmark mark='a'/>这是一个小项的所有可能归约，由我们的归约器算出：λx. x x，作用于 λy. y，"
        "再作用于 z。它有两个可约式，所以第一步有两种走法。归约外层会复制内层，得到两个副本要归约，顺序随意。<bookmark mark='b'/>六个项，七个单步，每条路径无论"
        "怎么绕，都终止在同一个地方：z z。",
    "That was no accident.":
        "这不是巧合。<bookmark mark='a'/>丘奇和罗瑟在 1936 年证明：如果项 M 经过任意多步归约到 N1，也归约到 N2，那么存在某个项 P，两者都能到达。把它画成一个"
        "菱形：无论走哪两个方向，路径都能重新汇合。<bookmark mark='b'/>所以范式如果存在，就是唯一的，因为范式不能再归约，两个不同的范式永远无法相遇。策略改变的是"
        "我们是否到达、多快到达，从不改变到达的是什么。<bookmark mark='c'/>证明里有一个漂亮的技巧。单步并不能合成菱形，因为一步可能复制一个可约式，而复制出来的"
        "要两步才能完成。但平行归约，一次归约任意选定的一组可约式，确实一步就能闭合，平行步的菱形拼在一起就得到了这条定理。",
    "A slightly bigger term already has a large graph of possible reductions.":
        "稍大一点的项就已经有一张很大的归约图。<bookmark mark='a'/>这个项有三十个项，由九十三个单步相连。<bookmark mark='b'/>我们的归约器检查了图中的每一对项："
        "每一对都有公共的归约结果，而且恰好有一个范式。这条定理，在一个小例子上得到了验证。",
    "Names cause trouble":
        "名字会带来麻烦：α 等价，以及第一章的捕获陷阱。尼古拉斯·德布鲁因在 1972 年搭建最早的证明检查器之一时，把它们去掉了。<bookmark mark='a'/>把每个变量换成"
        "一个数：沿着树往上，要经过多少个 λ 才能到达约束它的那个。λx. x 就是 λ. 0。二，λf x. f (f x)，变成 λ. λ. 1 (1 0)。<bookmark mark='b'/>现在 α 等价的"
        "项字面上完全相同，捕获也不可能发生了。<bookmark mark='c'/>编译器和证明助手内部使用这种表示，而第15部分会用环境彻底取代代换，真实的解释器就是这样运行的。",
    # ------------------------------------------------------------------ Types
    "Chapter seven. Simple types.": "第七章。简单类型。",
    "Add booleans and numbers to the calculus":
        "给演算加上布尔值和数字，有些程序就毫无意义了。<bookmark mark='a'/>if 0 then true else false。true 的后继。一个布尔值的前驱。true 作用于 0。一个函数是否"
        "为零。<bookmark mark='b'/>每一个都停在一个不是答案的地方，没有规则可用。它卡住了。在真实的机器上，同样的错误就是一次崩溃，或者更糟，一个由本来另有含义"
        "的位算出来的无声的错误答案。<bookmark mark='c'/>类型在程序运行之前就排除这样的程序。罗宾·米尔纳在 1978 年把它概括成一句口号：良类型的程序不会出错。"
        "接下来两章会证明它。",
    "The simply typed lambda calculus adds types to the language.":
        "简单类型 λ 演算给语言加上了类型。<bookmark mark='a'/>类型是 Bool，或者 Nat，或者函数类型 A → B。<bookmark mark='b'/>项和以前一样，带有布尔值、数字和"
        "它们的运算，只是每个 λ 都要声明参数的类型。<bookmark mark='c'/>A → B 是从 A 到 B 的函数的类型。箭头向右结合，所以 Nat → Nat → Nat 是一个有两个数字"
        "参数的函数。<bookmark mark='d'/>丘奇在 1940 年引入这个系统，不是为了编程，而是为了保持逻辑的一致：无类型的演算能表达悖论。",
    "The type checker applies a handful of rules":
        "类型检查器应用寥寥几条规则，写法和第13部分一样：横线上方是必须已知的，下方是由此推出的。<bookmark mark='a'/>变量的类型由上下文给出。<bookmark "
        "mark='b'/>要给函数定型，就假定参数具有声明的类型，再给函数体定型；函数的类型是从前者到后者的箭头。<bookmark mark='c'/>从 A 到 B 的函数作用于一个 A，"
        "得到一个 B，而且只接受 A。<bookmark mark='d'/>数的后继是数；if 需要一个布尔条件和两个同类型的分支。整个检查器就这些。",
    "Typing a whole term builds a tree of rules":
        "给整个项定型会建起一棵规则树，叫作推导。<bookmark mark='a'/>这里我们的检查器给 λx:Nat. succ x 作用于 2 定型。底部是结论：这个项的类型是 Nat，由应用"
        "规则得出。它上面是两个前提：函数的类型是 Nat → Nat，由抽象规则得出，而这又建立在假定 x 是 Nat 时给 succ x 定型的基础上。实参 2 是 Nat，因为它是零的后继"
        "的后继。<bookmark mark='b'/>每个良类型的项都有这样一棵树，检查器的工作正是把它建出来。对把 twice 作用于 succ 和 3 的项，这棵树有十六条规则。",
    "Typed terms run the same way as before":
        "有类型的项和以前一样运行，按传值调用一小步一小步地走。<bookmark mark='a'/>twice 作用于 succ 和 3。先归约函数位置，把 succ 代入 f。然后实参 3 进去。内层"
        "的应用必须先完成，外层的才能触发，答案是五。<bookmark mark='b'/>每一步都由一条规则支持，名字写在左边，而下一章要证明关于每一个这样的步骤的一件事。",
    # ------------------------------------------------------------------ Safety
    "Chapter eight. Well-typed programs cannot go wrong.": "第八章。良类型的程序不会出错。",
    "Milner's slogan is a theorem with two halves.":
        "米尔纳的口号是一条分成两半的定理。<bookmark mark='a'/>进展性：一个封闭的良类型项，要么是一个值，也就是完成了的答案，要么能走一步。它永远不会卡住。"
        "<bookmark mark='b'/>保持性：如果一个良类型的项走了一步，结果具有相同的类型。<bookmark mark='c'/>把两者沿程序的任意一次运行结合起来。由保持性，每个项都"
        "具有类型 T，所以由进展性，每个项要么是答案，要么能再走一步。良类型的程序永远不会到达卡住的状态。",
    "The proofs go by induction on the typing derivation":
        "证明按类型推导做归纳，每条规则一种情形。这是进展性里有意思的那个情形。<bookmark mark='a'/>项是一个应用 f a，其中 f 的类型是 A → B，a 的类型是 A。"
        "<bookmark mark='b'/>由归纳，f 是值或者能走一步。如果能走一步，f a 也能。<bookmark mark='c'/>如果 f 是值，那么因为它的类型是箭头，它必定是一个 λ：函数"
        "类型的值只有函数。这个小引理叫典范形式，类型正是在这里发挥作用。<bookmark mark='d'/>然后实参是值或者能走一步；如果是值，整个项就是一个可约式。<bookmark "
        "mark='e'/>对 if，条件要么还差一步，要么是 Bool 类型的值，只能是 true 或 false。在每种情形下，类型都规定了哪些值能出现在哪些位置，于是卡住的组合一个也"
        "留不下来。",
    "Preservation rests on one lemma.":
        "保持性依赖于一个引理。<bookmark mark='a'/>唯一会大幅改变项的形状的一步是 β 归约，它用实参代换参数。<bookmark mark='b'/>给这个可约式定型时，我们在假定 x "
        "是 A 的情况下给函数体 t 定了型，又把实参 s 定型为 A。<bookmark mark='c'/>代换引理说：把一个真正的 A 放在假定为 A 的地方，函数体的类型保持不变。它本身也"
        "通过对 t 的推导做归纳来证明。有了它，保持性就逐个情形地成立了。",
    "We can also check the theorems by machine":
        "我们也可以用机器检查这些定理，就像第13部分检查编译器那样。<bookmark mark='a'/>我们的生成器构造了五千个随机的封闭项，每个都按构造就是良类型的。<bookmark "
        "mark='b'/>我们把每一个运行到底，总共五万多步，每一步之后都重新检查类型。<bookmark mark='c'/>没有一个项卡住过，也没有一个类型改变过。<bookmark mark='d'/>"
        "而且每一个都结束了，最多四十七步。最后这一点不是我们的生成器的巧合。它是下一章的定理。",
    "How far does this reach in practice?":
        "这在实践中能走多远？<bookmark mark='a'/>Standard ML 在 1990 年得到了完整的形式定义，它的安全性后来被机器检查过。<bookmark mark='b'/>Java 和 C# 在设计上"
        "是类型安全的，Java 虚拟机会验证它加载的字节码。<bookmark mark='c'/>安全的 Rust 是内存安全的，RustBelt 项目在 2018 年证明了这一点，并允许不安全代码存在于"
        "承诺维护不变式的库内部。<bookmark mark='d'/>C 和 C++ 不安全：一个类型完全正确的 C 程序也能写过数组的末尾，就像第11部分展示的那样。<bookmark mark='e'/>"
        "还要注意这句口号没说什么。不会出错的意思是永不卡住。它不意味着程序会终止，也不意味着它算出了你想要的东西。",
    # ------------------------------------------------------------------ Normalization
    "Chapter nine. Every typed program stops.": "第九章。每个有类型的程序都会停。",
    "Try to give a type to the heart of omega":
        "试着给 Ω 的核心 λx. x x 一个类型。<bookmark mark='a'/>x 被作用于某个东西，所以它必须是一个函数，类型为某个 A → B。<bookmark mark='b'/>但 x 也是它所作用"
        "的那个东西，所以 x 的类型必须是 A。<bookmark mark='c'/>于是 A 等于 A → B，又等于 (A → B) → B，如此永无止境。<bookmark mark='d'/>没有有限的类型是解。"
        "<bookmark mark='e'/>我们的推断引擎，也就是开场那个，正是带着这样的抱怨放弃的：无限类型。Ω 没有类型，Y 组合子也没有。",
    "In fact no typed term runs forever.":
        "事实上，没有一个有类型的项会永远运行。<bookmark mark='a'/>威廉·泰特在 1967 年证明：简单类型演算里每个良类型的项都能到达范式，无论选择哪种归约顺序。"
        "<bookmark mark='b'/>按项的大小做归纳这种显而易见的证明行不通，因为一步 β 归约可能通过复制实参让项变大。<bookmark mark='c'/>泰特的想法是证明一个更强的性质，"
        "按类型归纳地定义。一个数是好的，如果它会终止。一个函数是好的，如果它把每个好的实参都送到好的结果。<bookmark mark='d'/>然后证明每个有类型的项都是好的，而"
        "每个好的项都会终止。这种方法如今叫作逻辑关系，从此一直是类型论的主力工具。",
    "The difference shows up in a simple experiment.":
        "这个差别在一个简单的实验里就能看出来。<bookmark mark='a'/>我们生成了两千个随机的无类型项，每个用正规序运行至多四百步：有一百三十六个还在运行。<bookmark "
        "mark='b'/>上一章的五千个有类型的项，没有一个运行得很久。对它们，这条定理告诉了我们任何测试都无法告诉的事：它们每一个都会停下。",
    "Termination has a price.":
        "终止是有代价的。<bookmark mark='a'/>如果每个有类型的程序都会停，那么这个演算就表达不了永远运行的程序，所以它不是图灵完备的。它甚至无法包含自己的解释器，"
        "由第25部分的对角线论证可知。<bookmark mark='b'/>编程语言用一个不动点算子 fix 把一般递归买回来，它的规则说：从 T 到 T 的函数的 fix 具有类型 T。<bookmark "
        "mark='c'/>ML、Haskell 和 OCaml 都包含它，它们的程序可能会循环。Agda、Rocq 和 Lean 这样的证明助手拒绝它，只接受可以证明会终止的递归，原因第十二章会讲清"
        "楚：在这些语言里，一个类型就是一条定理，而一个循环的程序能证明任何东西。",
    # ------------------------------------------------------------------ Inference
    "Chapter ten. Hindley Milner inference.": "第十章。欣德利–米尔纳推断。",
    "In the hook, nobody wrote a type, yet the machine knew them all.":
        "在开场，没有人写类型，机器却全都知道。原理是这样的。<bookmark mark='a'/>拿把 f 作用两次的函数来说。<bookmark mark='b'/>给每个未知量一个类型变量：f 是某个"
        "类型 α，x 是某个类型 β。<bookmark mark='c'/>每次使用都增加一个方程。f 作用于 x 说明 α 必须是从 β 到某个 γ 的函数。<bookmark mark='d'/>f 作用于 f x 说明"
        " α 也是从 γ 到某个 δ 的函数。<bookmark mark='e'/>推断就是求解这些类型之间的方程，这叫作合一。",
    "Alan Robinson gave the algorithm in 1965":
        "艾伦·鲁宾逊在 1965 年为自动定理证明给出了这个算法。<bookmark mark='a'/>变量与类型之间的方程，把这个变量绑定到那个类型，在它出现的每一处。<bookmark "
        "mark='b'/>两个函数类型之间的方程拆成两个方程：参数相等，结果相等。<bookmark mark='c'/>两个不同的类型构造子，比如 int 和 bool，不能相等：这是一个类型错误。"
        "<bookmark mark='d'/>一个变量不能绑定到包含它自己的类型：那就是 Ω 的无限类型。<bookmark mark='e'/>合一成功时，它找到的是最一般的解，其他每个解都是它的"
        "特例。",
    "Here is our engine's own trace for twice.":
        "这是我们的引擎对 twice 的推断轨迹。<bookmark mark='a'/>它为 f 和 x 假定新的变量。从 f x，它把 f 的变量绑定到一个从 x 的变量到一个新变量的函数。从外层的"
        "应用，它必须把这个函数类型与另一个合一，拆成两次绑定。<bookmark mark='b'/>剩下的就是主类型：对任何类型 'a，一个从 'a 到 'a 的函数，再加一个 'a，得到一个 "
        "'a。<bookmark mark='c'/>组合同样干净利落，有三个独立的类型变量。这就是米尔纳 1978 年论文里的算法 W；罗杰·欣德利在 1969 年已经找到了组合逻辑的主类型。",
    "One more ingredient makes this practical.":
        "还有一个要素让它变得实用。<bookmark mark='a'/>用 let 绑定恒等函数，把它用在一个数和一个布尔值上：程序的类型是 int * bool。可是把恒等函数作为参数传进去，"
        "再同样用两次，推断就失败了。<bookmark mark='b'/>let 绑定的名字会被泛化：一旦它的类型被求出，其中的自由类型变量就变成“对所有”，每次使用都得到新的副本。"
        "<bookmark mark='c'/>λ 绑定的参数不会，因为它的各次使用必须一致。<bookmark mark='d'/>这个限制是可判定性的代价。乔·韦尔斯在 1994 年证明，对完全多态，也就"
        "是下一章的 System F，推断是不可判定的。",
    "Here is the whole Job, as the hook promised.":
        "这是完整的任务，正如开场所承诺的。<bookmark mark='a'/>十一个定义，几百次合一，没有一个标注。反转适用于任何东西的列表。lower 和 is_letter 作用于字符编码。"
        "bump 和 count 适用于任何支持相等比较的单词类型，insert 和 sort 适用于任何第二部分是计数的序对。<bookmark mark='b'/>这些类型变量精确地说明了每个函数不关心"
        "什么，而且是被发现的，不是被声明的。",
    "Inference is fast on real programs, but it has a famous worst case.":
        "推断在真实程序上很快，但它有一个著名的最坏情形。<bookmark mark='a'/>f0 把参数和它自己配成一对。f1 把 f0 作用两次，所以结果是序对的序对。<bookmark "
        "mark='b'/>每新一行都把前一个函数作用两次，类型的大小就平方一次：n 行之后，有 2 的 2^n 次方个叶子。<bookmark mark='c'/>我们的引擎把类型保存为一张共享的图，"
        "所以连 f5 都能在一毫秒内处理完，可要是写出来，f5 的类型会有四十多亿个叶子。<bookmark mark='d'/>迈尔森，以及克福里、蒂乌伦和乌日楚因，在 1990 年证明："
        "判定一个 ML 程序是否可定型，对指数时间是完全的。没有人会写这样的程序，所以这个算法照样到处在用。",
})

ZH.update({
    # ------------------------------------------------------------------ SystemF
    "Chapter eleven. Polymorphism and free theorems.": "第十一章。多态与免费定理。",
    "ML allows for all only at the outside of a type.":
        "ML 只允许“对所有”出现在类型的最外层。System F 允许它出现在任何地方。<bookmark mark='a'/>类型多了一个量词，对所有 α；项多了以类型为参数的函数：大写的 "
        "Λα，以及作用于一个类型。让-伊夫·吉拉尔在 1972 年为逻辑找到了这个系统，约翰·雷诺兹在 1974 年为编程独立地找到了它。<bookmark mark='b'/>恒等函数先接受一个"
        "类型 α，再接受一个该类型的值。<bookmark mark='c'/>现在，一个函数可以接受多态的恒等函数作为参数，并在两种类型上使用它，这是 ML 无法定型的。<bookmark "
        "mark='d'/>代价是类型必须写出来：推断是不可判定的。",
    "System F gives chapter three's encodings honest types.":
        "System F 给第三章的编码以诚实的类型。<bookmark mark='a'/>布尔值接受同一种任意类型的两个东西，返回其中一个。数接受一个从某类型到自身的函数和一个起始值，返回"
        "该类型的值。τ 的列表就是它自己的折叠。<bookmark mark='b'/>这些类型的每个项都表现得像一个布尔值、一个数或一个列表。而且 System F 和简单类型演算一样总会终止，"
        "这是吉拉尔证明的；然而它能表达二阶算术能证明为全函数的每一个函数：几乎一切数学家会称为函数的东西。",
    "A polymorphic type constrains a program more than you might expect.":
        "多态类型对程序的约束比你想象的更多。<bookmark mark='a'/>类型为“对所有 α，α → α”的函数对它的参数一无所知，所以除了参数本身没有别的可返回：它必定是恒等函数，"
        "或者永不返回。<bookmark mark='b'/>“对所有 α，α → α → α”必定返回两个参数之一：它是一个丘奇布尔值。<bookmark mark='c'/>而一个从 α 的列表到 α 的列表的函数"
        "无法查看元素内部。它能做的只是重排、丢掉一些或复制一些，而且只能依据列表的形状。<bookmark mark='d'/>所以它与 map 可交换：先改变元素还是后改变，结果相同。"
        "雷诺兹称之为参数性，菲利普·瓦德勒 1989 年的论文把这类结果叫作免费定理：你从类型上就能读出它们，不必看程序。",
    "We can test the free theorem in the lambda core.":
        "我们可以在 λ-核心里检验这条免费定理。<bookmark mark='a'/>对四个推断类型为 'a list -> 'a list 的函数：反转、取前三个、隔一个取一个、把每个元素复制一遍，"
        "我们在两百个随机列表和随机线性函数 f 上比较了先 g 后 map f 与先 map f 后 g。<bookmark mark='b'/>它们每次都一致。<bookmark mark='c'/>一个类型较不一般、为 "
        "int list -> int list 的函数，给每个元素加一，第一次尝试就打破了这条定律。只有类型才做出了承诺。<bookmark mark='d'/>编译器会使用这样的定律。Haskell 编译器 "
        "GHC 把 map f (map g l) 改写成一个循环，这是安全的，因为类型保证了它。",
    # ------------------------------------------------------------------ CurryHoward
    "Chapter twelve. Propositions as types.": "第十二章。命题即类型。",
    "Here is the deepest idea in this part.":
        "这是这一部分最深刻的思想。<bookmark mark='a'/>把类型读作命题。函数类型 A → B 就是命题“A 蕴含 B”，而这个类型的函数就是它的证明：给它 A 的证据，它就产生 B 的"
        "证据。<bookmark mark='b'/>序对是“A 且 B”的证明。带标签的并，一个 A 或一个 B，并注明是哪一个，是“A 或 B”的证明。没有任何值的空类型是假，而“非 A”是从 A 到"
        "空类型的函数，它永远不可能真正被调用。<bookmark mark='c'/>证明就是程序。而简化一个证明，去掉经由某个引理的绕路，恰好就是用 β 归约运行这个程序。哈斯凯尔·柯里"
        "在 1934 年注意到了最初的迹象；威廉·霍华德在 1969 年把它完整地写了下来。",
    "If proofs are programs, a theorem prover is a program synthesizer.":
        "如果证明就是程序，定理证明器就是程序合成器。<bookmark mark='a'/>我们的证明器搜索给定类型的 λ 项。“A 蕴含 B 蕴含 A”是接受 x 和 y、返回 x 的函数：常函数组合子。"
        "组合证明了三段论：由 A 蕴含 B 和 B 蕴含 C，得 A 蕴含 C。交换序对证明了“且”可交换。对带标签的并做情形分析证明了“或”可以消去。<bookmark mark='b'/>最后一行是"
        "一颗小宝石：非非（A 或非 A）。它听起来像排中律，却无需排中律就能证明。程序是一个巧招：它拿到一个反驳 x，然后用它来反驳它自己。",
    "Some theorems of ordinary logic have no program at all.":
        "普通逻辑的有些定理根本没有程序。<bookmark mark='a'/>排中律，A 或非 A。双重否定消去。皮尔士定律。还有德摩根律的一半。它们真值表的每一行都为真。<bookmark "
        "mark='b'/>可是我们的证明器一个程序也找不到，而且马上我们就会证明不存在这样的程序。程序的逻辑是直觉主义逻辑，在其中，证明必须构造出它所断言的东西。<bookmark "
        "mark='c'/>想想类型为“A 或非 A”的程序得做什么：返回 A 的证据或 A 的反驳，并说明是哪一个。对每个命题 A 都如此。它就能判定一切了。",
    "To show that no program exists":
        "要证明不存在程序，我们需要一个世界，在其中公式不成立，而程序仍然有意义。索尔·克里普克在 1965 年提供了一个。<bookmark mark='a'/>想象知识的状态，它只会向上"
        "增长。在下面的世界 w0 中，我们还不知道 A。在它上面的世界里，我们知道了。<bookmark mark='b'/>在 w0，A 不被知道。非 A 也不被知道，因为非 A 意味着 A 永远不会被"
        "知道，而在上面它被知道了。所以 A 或非 A 在 w0 不成立。<bookmark mark='c'/>而每个有程序的公式在每个这样的模型中都成立。所以排中律没有程序。我们的搜索为前三条"
        "定律各找到一个这样的两世界模型，为德摩根律找到一个三世界模型。",
    "There is a twist.":
        "还有一个转折。<bookmark mark='a'/>1990 年，蒂莫西·格里芬注意到，皮尔士定律，这个任何纯函数都证明不了的定律，恰好是一个叫“带当前续延调用”的算子的类型。"
        "<bookmark mark='b'/>它把计算的剩余部分捕获为一个函数，于是程序可以跳回去重来：它可以先承诺一个 A，如果被要求兑现，再改变答案。经典逻辑对应于带控制的程序。"
        "<bookmark mark='c'/>第15部分会搭建续延。<bookmark mark='d'/>而命题即类型是第54部分证明助手的基础，在那里，检查一个证明就是给一个程序做类型检查。",
    # ------------------------------------------------------------------ Dependent
    "Chapter thirteen. Dependent and linear types.": "第十三章。依赖类型与线性类型。",
    "So far, types and values have lived apart.":
        "到目前为止，类型和值是分开的。依赖类型让类型可以提到值。<bookmark mark='a'/>Vec A n 是长度恰好为 n 的 A 的列表的类型：长度是类型的一部分。<bookmark "
        "mark='b'/>把长度为 m 的向量接到长度为 n 的向量上，得到长度 m + n，类型检查器会验证这个算术。<bookmark mark='c'/>head 只接受长度为 n + 1 的向量。取空列表的头"
        "不再是运行时的崩溃；它是一个类型错误。<bookmark mark='d'/>zip 要求两个长度相同的向量。",
    "Two type formers make this work.":
        "两种类型构造让它成立。<bookmark mark='a'/>Π：结果类型依赖于参数值的函数，比如接受 n、返回长度为 n 的向量的函数。在柯里–霍华德之下，它是全称量词，对所有 n。"
        "<bookmark mark='b'/>Σ：第二个分量的类型依赖于第一个分量的序对，比如一个长度和一个该长度的向量。它是存在量词，存在一个 n。<bookmark mark='c'/>佩尔·马丁-洛夫"
        "在 1972 年到 1984 年之间以这些为基础建立了构造性数学的整个基础。科康和于埃 1988 年的构造演算成了证明助手 Coq，如今叫 Rocq。Agda 和 Lean 随后出现，如今数学家"
        "们用 Lean 形式化研究级的证明。<bookmark mark='d'/>因为类型里含有程序，检查一个类型可能意味着运行一个程序。这就是为什么这些语言坚持每个程序都要终止：第九章的"
        "定理，如今成了设计要求。",
    "A different refinement counts uses.":
        "另一种细化计数使用的次数。<bookmark mark='a'/>我们的检查器统计每个经典组合子使用每个参数的次数。恒等、组合和翻转把每个参数恰好用一次：它们是线性的。常函数把"
        "第二个参数丢掉：仿射的，至多一次。W 和 S 复制了其中一个：相关的，至少一次。<bookmark mark='b'/>让-伊夫·吉拉尔 1987 年的线性逻辑把假设当作资源，用一次就"
        "消耗掉。<bookmark mark='c'/>在编程中，资源是实实在在的：必须恰好关闭一次的文件句柄、一把锁、一块必须释放一次且之后不再使用的内存。",
    "The most widely used language with such types is Rust.":
        "拥有这类类型、使用最广的语言是 Rust。<bookmark mark='a'/>Rust 里的 String 只有一个所有者。把它赋给另一个变量就是移动它，旧名字不能再用：一种仿射类型。这里"
        "这台机器上的 rustc 以错误 E0382，“借用已移动的值”，拒绝了这个程序。<bookmark mark='b'/>除了移动，值还可以被借用：被任意多个读者借用，或者被一个写者借用，"
        "但永远不能同时。在向量里还有一个活着的引用时往里推入元素，如果向量搬动了存储，那个引用就会悬空，于是 rustc 拒绝。<bookmark mark='c'/>结果是不需要垃圾回收器的"
        "内存安全，线程之间也没有数据竞争，这一切都在程序运行之前检查。第55部分在追问什么值得信任时会回到 Rust。",
    # ------------------------------------------------------------------ Data
    "Chapter fourteen. Data, subtyping and gradual types.": "第十四章。数据、子类型与渐进类型。",
    "Real functional languages organise data as algebraic data types.":
        "真实的函数式语言把数据组织成代数数据类型。<bookmark mark='a'/>一个形状要么是带半径的圆，要么是带宽和高的矩形：积的和。<bookmark mark='b'/>这又是柯里和霍华德的"
        "“或”与“且”，这次是作为数据。<bookmark mark='c'/>match 逐个情形地拆开一个形状，编译器会检查每种情形都被覆盖，所以以后添加一个三角形，它会指出每一个必须修改的"
        "函数。<bookmark mark='d'/>option 类型，要么什么也没有，要么有某个东西，取代了空指针，它的发明者托尼·霍尔称之为他的十亿美元错误。<bookmark mark='e'/>口号是："
        "让非法的状态无法表示。",
    "Object-oriented languages add subtyping.":
        "面向对象语言加入了子类型。<bookmark mark='a'/>如果 S 是 T 的子类型，类型为 S 的项可以用在任何期望 T 的地方：狗可以出现在任何期望动物的地方。<bookmark "
        "mark='b'/>对函数，规则很微妙。从 A 到 B 的函数可以代替从 A' 到 B' 的函数，条件是它的结果更具体，而参数更一般。<bookmark mark='c'/>结果沿相同方向变化，即协变。"
        "参数沿相反方向变化，即逆变。<bookmark mark='d'/>而可变数组既被读，像结果，又被写，像参数。所以它必须是不变的：狗的数组不是动物的数组。",
    "Not every language follows the rule.":
        "并不是每种语言都遵守这条规则。<bookmark mark='a'/>这是一个很短的 TypeScript 程序。狗的数组被赋给一个类型为动物数组的变量，往里推入一只猫，然后让狗数组的第二个"
        "元素叫一声。<bookmark mark='b'/>TypeScript 的检查器，在最严格的模式下，接受了它。<bookmark mark='c'/>而在这台机器上用 node 运行结果，失败了：bark 不是一个函数。"
        "<bookmark mark='d'/>TypeScript 故意让数组协变，用可靠性换方便。Java 在 1995 年对数组做了同样的选择，代价是在运行时检查每一次数组写入。一个类型系统可以有用而"
        "不可靠，但那样它承诺的就少了。",
    "Finally, a compromise most working programmers now use.":
        "最后，是如今大多数在职程序员都在用的一种折中。<bookmark mark='a'/>渐进类型由杰里米·西克和瓦利德·塔哈在 2006 年提出，它加入一个写作 any 或问号的类型，与一切"
        "兼容，于是程序可以一次给一个函数加上类型。TypeScript、Python 的类型提示和 Hack 都是这样。<bookmark mark='b'/>在 TypeScript 里，类型被直接擦除，any 会关掉检查："
        "把四十二传给一个期望字符串的函数能通过检查器，运行时打印出“非数”。<bookmark mark='c'/>可靠的渐进类型，比如 Typed Racket，会在有类型和无类型代码相遇的每一处"
        "插入检查，而这些检查有代价：2016 年的一项研究发现，有些组合慢了一百多倍。让可靠的渐进类型变得廉价，仍是一个研究问题。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen. Frontier: the edges of type theory.": "第十五章。前沿：类型论的边缘。",
    "Start with a puzzle from chapter ten.":
        "从第十章的一个谜题开始。ML 类型推断对指数时间是完全的，可编译器在几百万行代码上运行它毫无问题。<bookmark mark='a'/>我们用任务的定义，一遍遍复制，直到三百"
        "五十二个定义，给我们的引擎计时：时间呈直线增长。<bookmark mark='b'/>指数级的例子需要 let 套 let，每一层都复制上一层，而真实程序不是那个样子。戴维·麦卡莱斯特"
        "在 2003 年证明，嵌套深度有界时，推断几乎是线性的。<bookmark mark='c'/>完整地说明哪些程序是难的、实践为什么如此仁慈，仍是开放问题。",
    "Dependent types are powerful but demand proofs.":
        "依赖类型很强大，却要求证明。精化类型试图得到这种力量而不要证明。<bookmark mark='a'/>精化类型是基本类型加一个谓词：get 接受一个数组和一个大于等于零、小于数组"
        "长度的整数。<bookmark mark='b'/>每次调用产生一个逻辑条件，由 SMT 求解器，比如第13部分的 z3，证明或反驳。<bookmark mark='c'/>LiquidHaskell、F* 和 Dafny 都是"
        "这样工作的，已经被用来证明数组访问安全、协议不变式以及密码学代码的正确性。<bookmark mark='d'/>开放的问题是：在人必须亲自写证明之前，自动化能走多远。",
    "At the deep end, type theory is being used to rethink the foundations of mathematics.":
        "在最深处，类型论正被用来重新思考数学的基础。<bookmark mark='a'/>在依赖类型论中，a = b 本身是一个类型，它的值是 a 与 b 相等的证明。<bookmark mark='b'/>菲尔兹奖"
        "得主弗拉基米尔·沃埃沃茨基提出把这些证明读作空间中的路径，于是有了同伦类型论。<bookmark mark='c'/>它的核心原则，一价公理，说的是等价的类型就是相等的，这正是数学"
        "家实际推理的方式。<bookmark mark='d'/>可是作为公理加入，它就打破了第八章的承诺：使用公理的程序可能会卡住。<bookmark mark='e'/>2015 年起的立方类型论把一价性变成"
        "一条具有计算内容的定理，于是使用它的程序依然能运行。已经有了实现，比如 Cubical Agda；让它们又快又好用，是当前的工作。",
    "Another frontier is typing what programs do":
        "另一个前沿是给程序做了什么定型，而不只是给它返回什么定型。<bookmark mark='a'/>int → int 这个类型完全没说一个函数是否读文件、抛异常，或者永远运行。<bookmark "
        "mark='b'/>普洛特金和普雷特纳 2009 年的效应处理器给异常、生成器、异步代码等等提供了统一的机制：效应是一个请求，而处理器，一个定界续延，回应它。<bookmark "
        "mark='c'/>OCaml 5 在 2022 年发布了它们，Koka 之类的语言在类型中追踪效应。<bookmark mark='d'/>让在职程序员愿意接受、又能编译成快速代码的效应类型，仍在研究之中。",
    "Here is where the field stands.":
        "这个领域现在的状况是这样的。<bookmark mark='a'/>可靠的渐进类型能否变得廉价，并有运行时代价的可证明上界？<bookmark mark='b'/>哪些更丰富的类型系统能保持推断"
        "可判定？二阶多态可以，三阶及以上不行，这是克福里和韦尔斯证明的；中间的领域仍在测绘之中。<bookmark mark='c'/>依赖类型能否进入主流语言，而不要求每一行都有证明？"
        "<bookmark mark='d'/>一价性能否快到足以用于日常数学？<bookmark mark='e'/>这一部分的研究问题处理的是第一个。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭建了什么。λ 项、不会捕获的代换和 β 归约。只用函数构造的布尔值、数字、序对和列表，以及来自 Y 组合子的递归。决定我们能否结束的策略，以及说明它们"
        "改变不了答案的丘奇–罗瑟定理。简单类型，连同进展性、保持性和泰特的正规化定理，在成千上万个随机程序上做了检验。欣德利–米尔纳推断，它在没有标注的情况下给任务"
        "定了型，还有它双重指数的最坏情形。System F 和免费定理。以及命题即类型，用证明搜索找到程序，用克里普克模型说明哪些定律没有程序。",
    "Where this comes back.":
        "这些会在哪里再出现。第15部分把 λ-核心变成真正的运行时，有环境、闭包、续延、虚拟机和垃圾回收器，并在上面运行任务，得到账本的第六行。第25部分证明这一部分所依赖"
        "的对角线定理和递归定理。第43部分把类型放到服务之间的边界上。第54部分用 Lean 和 Rocq 证明程序正确。第55部分回到 Rust，而研究层的第58部分追问程序的含义是什么。",
    "In practice.":
        "在实践中。类型推断无处不在：在 OCaml 和 Haskell 中是完全的，在 Rust、Swift 和 TypeScript 中是局部的。Java、C#、Go 和 Rust 的泛型就是参数多态，一次检查，"
        "对每种类型都有效。带模式匹配的和类型已经传播到 Rust、Swift、Kotlin、Scala，甚至 Python。渐进类型检查器让团队可以一次一个文件地给大型代码库加上类型。同样的"
        "思想推进到依赖类型，就能验证数学、一个 C 编译器和一个操作系统内核。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是动手题：给 λ-核心加上自己的数据类型和模式匹配，并支持推断，再用它们改写任务的一部分。最后"
        "一道标着星号，是研究问题：它的答案还没有人知道，笔记里说明了从哪里入手。",
    "Next time.":
        "下一次。λ-核心有了运行时：用闭包和环境代替代换，用续延把栈变成数据，一台字节码虚拟机，以及一个由三种颜色表述的不变式保证正确的垃圾回收器。第15部分，运行时。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分依据的书和论文都在屏幕上，也在笔记里。感谢观看。",
})

PHRASES = {}
