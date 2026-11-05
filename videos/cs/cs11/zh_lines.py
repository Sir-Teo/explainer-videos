"""Chinese narration for cs11: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第11部分：运行中的程序"

CHAPTERS = {
    "Hook": "从文本到运行中的进程",
    "Life": "1. 程序的一生",
    "Data": "2. 内存中的数据",
    "Control": "3. 机器码里的控制流",
    "Stack": "4. 调用栈",
    "Recursion": "5. 递归、深度与尾调用",
    "Heap": "6. 堆",
    "Allocators": "7. 五个分配器，一条真实轨迹",
    "Theory": "8. 克努特法则与罗布森界",
    "Objects": "9. 目标文件",
    "Linking": "10. 一步一步地链接",
    "Dynamic": "11. 动态链接",
    "Loading": "12. 装载与地址空间",
    "Undefined": "13. 未定义行为",
    "Smash": "14. 栈溢出攻击",
    "Job": "15. 链接起来的任务",
    "Frontier": "16. 前沿：边界、语义、能力",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Until now every Pebble program has been one file":
        "到目前为止，每个 Pebble 程序都是一个手写的汇编文件，机器从地址零开始运行它。真实的程序不是这样的。<bookmark mark='a'/>这又是任务，按编译器会写的方式写成："
        "四个独立的文件。主循环；单词表，现在是堆上节点组成的链表；一个内存分配器；以及输入输出例程。每个文件单独汇编，每个都留着洞：在那些地方它用到一个名字，"
        "比如 lookup 或 alloc，却不可能知道它的地址。<bookmark mark='b'/>链接器把这些洞填上，把四个文件合成一个程序。<bookmark mark='c'/>它打印的二十个词"
        "和第6部分的程序一模一样，在第一章上甚至还快一点。",
    "And here is a program that does something its author never wrote.":
        "这里还有一个程序，它会做作者从没写过的事。<bookmark mark='a'/>它问你的名字，然后打招呼，把名字复制进一个六十四字节的缓冲区。<bookmark mark='b'/>"
        "给它一个名字，它就向你问好。<bookmark mark='c'/>给它八十一个精心挑选的字节，它就打印出 pwned，一个程序里根本没有的词。<bookmark mark='d'/>输入越过了"
        "缓冲区的末尾，覆盖了函数将要返回的地址，处理器就返回到了输入本身里面。要看懂这是怎么回事、又怎样阻止它，我们得先知道一个运行中的程序在内存里是怎样布局的。",
    "Here is where this part goes. <bookmark mark='a'/> How a program's data sits in memory":
        "这一部分要去的地方是这样的。<bookmark mark='a'/>程序的数据怎样待在内存里：字节和字、对齐、数组和指针。<bookmark mark='b'/>过程是怎样工作的：调用栈、"
        "栈帧，以及让分别编写的函数能互相调用的约定。<bookmark mark='c'/>堆：五个内存分配器跑在一个真实程序的分配序列上，以及说明任何分配器能做到多好的定理。"
        "<bookmark mark='d'/>目标文件、链接和装载，在 Pebble 上，也在这台计算机上。<bookmark mark='e'/>还有会出的错：未定义行为，以及栈溢出攻击，连同如今"
        "每个程序都自带的防御。",
    "This is Part 11 of Computer Science, Built":
        "这是《计算机科学，从零搭建》的第11部分，第三幕“和机器对话”的第一部分。<bookmark mark='a'/>这一部分讲：程序从源代码到进程的一生。字节、字节序和对齐，"
        "以及机器码里的控制流。调用栈、调用约定、递归和尾调用。堆和它的分配器，以及克努特的五十百分比法则和罗布森界。目标文件、静态和动态链接，以及地址空间。"
        "未定义行为、栈溢出攻击，以及由四个文件链接起来的任务。",
    # ------------------------------------------------------------------ Life
    "Chapter one. A program's life.": "第一章。程序的一生。",
    "A program goes through five hands on its way to running.":
        "一个程序在运行之前要经过五双手。<bookmark mark='a'/>它从源代码开始，一段人写的文本。<bookmark mark='b'/>编译器把它翻译成汇编语言；第13部分会搭一个。"
        "<bookmark mark='c'/>汇编器，第6部分搭过，把汇编变成机器字，但它一次只处理一个文件，所以只要文件用到别处定义的名字，它就得留一个洞，外加一张条子说明"
        "那里该填什么。这就是目标文件。<bookmark mark='d'/>链接器读入所有目标文件，决定每样东西放在哪里，并把每个洞填上。<bookmark mark='e'/>最后，操作系统的"
        "装载器把程序复制进内存，建好带着程序参数的栈，跳到它的第一条指令。现在它是一个进程了。",
    'f"Follow one call through.':
        "跟着一次调用走一遍。<bookmark mark='a'/>在源代码里，它是对 lookup 的一次调用，带着词和它的长度。<bookmark mark='b'/>在汇编里，它变成 call lookup。"
        "<bookmark mark='c'/>但 lookup 在另一个文件里，所以汇编器不可能知道它有多远。它发出一条偏移为零的跳转并链接，<bookmark mark='d'/>外加一张条子，一条重定位："
        "在我的代码第八十八个字节处，填上到 lookup 的距离，用跳转所用的 22 位形式。<bookmark mark='e'/>链接器把 main 的代码放在地址零，把表的代码放在它后面，"
        "于是 lookup 落在 {target}。它把距离，{(target - at) // 4} 条指令，写进那个洞。这个字的其余部分什么都没变。",
    # ------------------------------------------------------------------ Data
    "Chapter two. Data in memory.": "第二章。内存中的数据。",
    "Memory is a row of bytes, but most values are bigger than a byte.":
        "内存是一排字节，但大多数值都比一个字节大。<bookmark mark='a'/>一个 32 位的字要占四个字节，总得有人决定它们的次序。<bookmark mark='b'/>大端机器把最高位的"
        "字节放在前面，就像我们写数字那样；网络协议也这么做。<bookmark mark='c'/>小端机器把最低位的字节放在前面。x86、通常模式下的 Arm、RISC-V 和 Pebble "
        "都是小端，这台计算机证实了这一点：0A 0B 0C 0D 这四个字节在内存里依次是 0D、0C、0B、0A。<bookmark mark='d'/>这两个名字来自丹尼·科恩 1980 年的一份"
        "备忘录，取自《格列佛游记》里为该从哪一头敲开鸡蛋而打的仗。两种次序没有哪个更好；字节跨越网络或文件时把它们弄混，是一个经典的错误。",
    'f"Values also have to sit at sensible addresses.':
        "值还得放在合适的地址上。<bookmark mark='a'/>一个四字节的整数通常放在能被四整除的地址上，这样它就不会横跨两个缓存行，一次传输就能取到；Pebble 自己的"
        "取数就要求这样。<bookmark mark='b'/>所以编译器会给结构体加填充。一个字符、一个整数、一个字符，数据只有六个字节，但按这个次序排就要占{a[0]}个：第一个"
        "字符后面三个字节的填充，让整数对齐；末尾再三个，让这种结构体组成的数组也保持对齐。<bookmark mark='c'/>把最大的字段放在最前面，同样的数据装进{b[0]}个"
        "字节。<bookmark mark='d'/>任务的链表节点，两个指针和两个整数，在这台 64 位机器上是{n[0]}个字节，在指针只有四个字节的 Pebble 上是十六个。这些大小都是"
        "在这里测出来的：把结构体编译出来，再问它们。",
    "Arrays are the simplest structure of all.":
        "数组是最简单的结构。<bookmark mark='a'/>一个三行四列的二维数组<bookmark mark='b'/>一行接一行地存放，也就是行主序，在 C 和大多数语言里都是这样；Fortran "
        "则按列存。<bookmark mark='c'/>所以元素 i、j 的地址，是数组的起点加上四个字节乘以四 i 加 j。<bookmark mark='d'/>指针只是一个地址，给指针加一，加的是它"
        "所指对象的大小。数组下标就是指针运算：a 的第 i 项意思是 a 加 i 处的内容。而硬件里没有任何东西检查 i 是否在数组之内。第十四章会展示这要付出什么。",
    # ------------------------------------------------------------------ Control
    "Chapter three. Control flow in machine code.": "第三章。机器码里的控制流。",
    "Structured control flow disappears in machine code":
        "结构化的控制流在机器码里消失了：一切都变成分支。<bookmark mark='a'/>这是任务的两段，左边是类 C 的源代码，右边是 Pebble。<bookmark mark='b'/>if 变成"
        "绕过它主体的条件分支。注意那个范围测试的技巧：先减去 A，然后一次与 26 的无符号比较同时回答两个问题，因为任何小于 A 的值都会绕回成一个巨大的无符号数。"
        "编译器经常这样做。<bookmark mark='c'/>循环变成顶部一个决定是否离开的测试，加上底部一个跳回去的跳转。",
    "A switch statement with dense cases gets something better":
        "分支密集的 switch 语句会得到比一串 if 更好的东西。<bookmark mark='a'/>这是一个有八个分支的 switch，在这台计算机上用 gcc 开优化编译。<bookmark mark='b'/>"
        "先是一次边界检查：c 在零和七之间吗？<bookmark mark='c'/>然后它从编译器写在只读数据里的一张表中取出第 c 项，<bookmark mark='d'/>跳到那一项给出的地址。"
        "不管哪个分支，都是两次取数加一次间接跳转：一张跳转表。<bookmark mark='e'/>再看各个分支本身。每个都以一条跳到自己函数的普通跳转结束，而不是调用：因为"
        "之后没有别的事要做，编译器就让那个函数直接返回到我们的调用者。这就是尾调用，第五章还会回到它。",
    # ------------------------------------------------------------------ Stack
    "Chapter four. The call stack.": "第四章。调用栈。",
    "For functions written separately":
        "分别编写的函数，也许出自不同的人、不同的编译器，要互相调用，就必须约定规则：调用约定。这是 Pebble 的。<bookmark mark='a'/>参数放在 a0 到 a5，结果从 a0 "
        "带回。call 指令把返回地址放进 ra。<bookmark mark='b'/>寄存器分成两类。t0 到 t3 是临时寄存器：函数可以破坏它们，所以调用之后还需要某个的调用者得自己"
        "保存。s0 到 s2 正好相反：想用其中一个的函数，必须先保存旧值，返回前恢复，这样调用者就能依赖它们。栈指针始终按十六字节对齐。<bookmark mark='c'/>这些都不是"
        "硬件强制的。它是一份契约，真实的系统都把它写下来：Linux 和 macOS 的 System V 应用二进制接口，Windows 的微软接口，RISC-V 的 psABI。",
    "Here is what a function does with that contract.":
        "这是一个函数按这份契约做的事。<bookmark mark='a'/>lookup 会用到 s0、s1 和 s2，而且它会调用 alloc，后者会覆盖 ra。所以一进来它就把栈指针往下移十六个字节，"
        "把这四个都存在那里。这一块就是它的栈帧，也叫活动记录。<bookmark mark='b'/>它上面是调用它的函数 main 的栈帧，装着 main 的单词缓冲区。<bookmark mark='c'/>"
        "出去的时候，lookup 恢复这四个寄存器，把栈指针移回去，然后返回。每次调用压入一个帧，每次返回弹出一个，所以栈总是映照着正在进行的那一串调用。",
    "Watch it on a recursive function, the factorial.":
        "在一个递归函数上看看，阶乘。<bookmark mark='a'/>fact(10) 调用 fact(9)，后者调用 fact(8)，一直到一，每次调用压入一个帧，装着它自己的 n 和返回地址。"
        "<bookmark mark='b'/>这是在 Pebble 模拟器上逐条指令测出的栈深度：它爬升到十个帧，然后随着每次调用返回并相乘，退回到零。<bookmark mark='c'/>结果是十的"
        "阶乘，栈最深时是一百六十个字节。",
    # ------------------------------------------------------------------ Recursion
    "Chapter five. Recursion, depth, and tail calls.": "第五章。递归、深度与尾调用。",
    "Recursion can make the stack enormous.":
        "递归可以让栈变得巨大。<bookmark mark='a'/>威廉·阿克曼 1928 年的函数由三条短规则定义，第25部分会解释它为什么重要：它是可计算的，但增长得比任何固定层数的"
        "循环能算出的东西都快。<bookmark mark='b'/>我们在 Pebble 上运行了它。A(3, 6) 只是五百零九，但算它要调用十七万两千次，最深时栈上有五百一十一个帧。n 每增加"
        "一，调用次数大约变成四倍，深度翻倍。<bookmark mark='c'/>A(4, 2) 有将近两万位数字。这样的递归不只受时间限制，也受栈的限制。",
    'f"Some recursion can be made free.':
        "有些递归可以变得免费。<bookmark mark='a'/>这里递归调用是函数做的最后一件事；它的结果原样返回。这就是尾调用。<bookmark mark='b'/>那么就没有理由再回来："
        "这个帧里没有谁需要的东西。所以函数不必调用，直接跳到自己就行，最里面那一层返回时，它直接返回到最初的调用者。<bookmark mark='c'/>在 Pebble 上，用第一种"
        "办法把一百个数加起来，要用{a['deepest']:,}字节的栈和{a['steps']:,}条指令；第二种完全不用栈，指令也不到一半。Scheme 要求这种优化；C 编译器能做时就做，"
        "正如上一章的跳转表所示；Python 则有意从不这样做。",
    "What happens when the stack runs out?":
        "栈用完了会怎样？<bookmark mark='a'/>一个线程的栈大小是固定的，在它启动时就选好：Linux 上默认八兆字节，Windows 上一兆。<bookmark mark='b'/>在它下面，"
        "操作系统留了一个根本没有映射的保护页，所以越过末尾会被当作段错误抓住，而不是悄悄践踏别的内存。<bookmark mark='c'/>有自己运行时的语言会更早抓住它："
        "Python 在一千个帧时停下，Java 抛出栈溢出错误。<bookmark mark='d'/>两个函数互相调用，和一个函数调用自己一样算数。<bookmark mark='e'/>深递归的药方，是把"
        "待做的工作放进堆上一个显式的栈里，或者把它改成循环。",
    # ------------------------------------------------------------------ Heap
    "Chapter six. The heap.": "第六章。堆。",
    "The stack is perfect for data that lives exactly as long as a function call.":
        "栈非常适合那些寿命恰好和一次函数调用一样长的数据。<bookmark mark='a'/>但很多数据不是这样。<bookmark mark='b'/>任务的表比每一个往里添东西的调用都活得长，"
        "而且没人事先知道它会长多大。<bookmark mark='c'/>为此有了堆：向 malloc 要 n 个字节，你会得到一个指向它们的指针，一直有效，直到你用 free 把它们交还。"
        "<bookmark mark='d'/>这两个函数背后是一个难题。请求以任意次序、任意大小到来。分配器必须立刻决定每一个放在哪里，却不知道将来，而且一旦交出了地址，就再也"
        "不能移动这个块，因为程序握着指向它的指针。",
    "Here is the classic design.":
        "这是经典的设计。<bookmark mark='a'/>堆是一段被切成块的内存，每块开头有一个小小的头部，记着它的大小和是否在用。<bookmark mark='b'/>空闲块被串成一个链表。"
        "<bookmark mark='c'/>要分配，就沿着链表找一个足够大的块，交出它的前一部分，剩下的留在链表里。<bookmark mark='d'/>要释放，就把块标成空闲，如果邻居也空闲，"
        "就把它们合并成一个更大的块，免得堆碎成太小而用不上的碎片。<bookmark mark='e'/>找后一个邻居很容易，因为它的头部紧跟着我们。找前一个才是巧妙之处：高德纳"
        "1968 年的边界标签，把每个块的大小在它的最后一个字里也复制一份，于是前一个块一步就能找到。",
    'f"To compare allocators honestly we need real requests':
        "要公平地比较分配器，我们需要真实的请求，而不是编出来的。<bookmark mark='a'/>所以我们记录了一个真实的程序：Perl 数《傲慢与偏见》里的词，它建的哈希表和"
        "第17部分要搭的很像。我们写了自己的 malloc，记下每一个请求再调用真正的那个，并把它塞到 C 库前面，第十一章会解释这个技巧。<bookmark mark='b'/>十四万多次"
        "分配，大多数都很小：十六字节或更少，一个短词加上它的簿记那么大。<bookmark mark='c'/>随着表被填满，活着的数据一路攀升，到大约两兆字节。<bookmark mark='d'/>"
        "现在我们可以把这个序列原样重放给我们自己的分配器。",
    # ------------------------------------------------------------------ Allocators
    "Chapter seven. Five allocators, one real trace.": "第七章。五个分配器，一条真实轨迹。",
    "When several free blocks would do":
        "当好几个空闲块都可以时，一个请求该给哪一个？<bookmark mark='a'/>首次适配按地址顺序取它找到的第一个。下次适配做法一样，但每次搜索都从上次停下的地方开始，"
        "免得一遍遍重扫前面。最佳适配取能放下的最小的块，让最大的块保持完整。分离适配为每个大小类别各留一个链表，先在请求自己的类别里找。伙伴系统只允许大小为"
        "二的幂的块，这让切分和合并几乎不花代价。<bookmark mark='b'/>我们在同一个模拟的堆上实现了全部五种，把 Perl 的轨迹逐一重放给它们。",
    "Here are the results. <bookmark mark='a'/> The measure is fragmentation":
        "结果在这里。<bookmark mark='a'/>衡量标准是碎片率：每个分配器需要的堆，除以程序同时活着的字节数的最大值。一就是完美。<bookmark mark='b'/>首次适配、"
        "最佳适配和分离适配都落在一点一三左右：百分之十三的开销，大多是 Perl 那些小块上的头部和取整，而不是浪费掉的空洞。下次适配稍差一点。伙伴系统要多出将近"
        "百分之八十，因为把每个请求都取整到二的幂，平均浪费每个块的四分之一。<bookmark mark='c'/>速度是另一回事。本该很快的下次适配，在这条轨迹上每个请求要查看"
        "十七个块；分离适配不到一个，因为对的那个链表通常在表头就有块。<bookmark mark='d'/>浪费少、几乎不用搜索，这种组合正是真实分配器都建立在大小类别上的原因。",
    "The buddy system, from Kenneth Knowlton in 1965":
        "伙伴系统，肯尼思·诺尔顿 1965 年提出，用空间换简单。<bookmark mark='a'/>每个块都是二的幂。一个三十字节的请求把一个块劈成两半，再劈成两半，直到一个三十二"
        "字节的块正好放下。<bookmark mark='b'/>每一半的伙伴就在它自己的地址翻转一位的地方，翻的是块大小那一位，所以一次异或就能找到。<bookmark mark='c'/>一个块被"
        "释放而它的伙伴也空闲时，两者合并成它们的父块，并在上一层重复这个检查。<bookmark mark='d'/>这一切都很快。代价是取整：一个三十三字节的请求会得到六十四。"
        "块内部的浪费叫内部碎片；块之间的浪费，也就是首次适配受的苦，叫外部碎片。",
    "Real allocators combine these ideas.":
        "真实的分配器把这些想法组合起来。<bookmark mark='a'/>这台机器上的 C 库用的是 ptmalloc，它源自道格·利的分配器：按大小分的空闲块箱、边界标签和合并。"
        "<bookmark mark='b'/>更新的分配器，jemalloc、tcmalloc 和 mimalloc，把页切成同一大小类别的块，并给每个线程一个自己的空闲块缓存。<bookmark mark='c'/>"
        "非常大的请求干脆绕过堆，直接从操作系统拿新的页，那是第32部分的主题。<bookmark mark='d'/>每线程缓存又是第10部分的教训：一个共享的空闲链表会是每个核都在"
        "争抢的缓存行。<bookmark mark='e'/>在有垃圾回收的语言里，由运行时决定何时释放，第15部分会搭建它。",
    # ------------------------------------------------------------------ Theory
    "Chapter eight. Knuth's rule and Robson's bound.": "第八章。克努特法则与罗布森界。",
    "How many holes does a heap have?":
        "一个堆里有多少个空洞？高德纳在 1968 年找到了一条定律。<bookmark mark='a'/>在一个已经稳定到平衡态的堆里，有 N 个块在用，大约就有二分之一 p 乘 N 个空闲"
        "空洞，其中 p 是一次分配没有恰好用完它的空洞的概率。由于 p 通常接近一，空洞数大约是块数的一半。证明是一个计数论证。<bookmark mark='b'/>按两个邻居中有几个"
        "是空闲的，把在用的块分成三类：零个、一个、两个。<bookmark mark='c'/>每个空洞都夹在两个在用的块之间，因为相邻的空洞早就被合并了，所以空洞数的两倍等于 B "
        "加两倍的 C。<bookmark mark='d'/>现在问空洞怎样产生又怎样消失。释放一个 A 块产生一个新空洞；释放一个 C 块把两个空洞和它自己的空间合成一个；释放一个 B 块"
        "只是让一个空洞变大。<bookmark mark='e'/>而一次分配只有恰好用完一个空洞时才会消掉它。<bookmark mark='f'/>在平衡态里得失相抵，这说明 A 减 C 等于一减 p "
        "乘 N。代进去，空洞数就是二分之一 p N。",
    "We checked it.":
        "我们检验了它。<bookmark mark='a'/>一个首次适配的堆，分别有两百、一千和三千个块在用；每一步随机释放一个块，再分配一个随机大小的新块。我们数空洞，并通过"
        "统计分配切开空洞而不是用完它的频率来测量 p。<bookmark mark='b'/>每块的空洞数，对比二分之一 p：零点四三八对零点四三五；零点三九九对零点四零一；零点三八三"
        "对零点三八三。这条法则精确到可以拿来做规划。",
    "Knuth's rule describes the average heap.":
        "克努特法则描述的是平均的堆。最坏的呢？<bookmark mark='a'/>1971 年和 1974 年，约翰·罗布森证明了一个锐利的答案。如果一个程序活着的数据从不超过 M 字节，"
        "且没有块大于 n 个单位，那么对每一个分配器，都存在一个程序迫使它用上大约 M 乘以二分之一 log₂ n 再加一。<bookmark mark='b'/>这个程序是一个对手，它盯着"
        "分配器把东西放在哪里。它先用小块填满内存，再释放其中一半，挑选释放哪些，使得每个空洞都放不下下一个更大的尺寸。它把尺寸翻倍，重复。每一阶段都迫使分配器"
        "再拿大约 M 的一半的新内存。<bookmark mark='c'/>我们让这个对手对付我们的首次适配堆。尺寸每翻一倍，堆就长 M 的一半，那些点恰好落在罗布森的曲线上：块到四"
        "千字节时是四点五 M。<bookmark mark='d'/>这个界对任何从不移动块的分配器都成立。唯一的出路是移动它们、压实堆，而这需要知道每个指针在哪里：垃圾回收器，"
        "第15部分。",
}

PHRASES = {}

ZH.update({
    # ------------------------------------------------------------------ Objects
    "Chapter nine. Object files.": "第九章。目标文件。",
    "Now the same story on a real machine.":
        "现在在一台真实的机器上把这个故事再讲一遍。<bookmark mark='a'/>两个 C 文件。main 用到一个函数 count 和一个变量 total，它们住在另一个文件里；它也有自己的"
        "数据：一个指向字符串的指针，和一个文件私有的计数器。<bookmark mark='b'/>lib 定义了 count 和 total，还有一个弱变量，我们待会儿再说它。<bookmark mark='c'/>"
        "每个文件单独编译成一个目标文件，然后两者链接成一个程序。我们在这台计算机上编译它们，并用标准工具 readelf 读这些目标文件。",
    "An object file is a set of named sections.":
        "目标文件是一组有名字的节。<bookmark mark='a'/>这是 main.o 的。机器码在一个节里，字符串常量在一个只读节里。指针 greeting 有自己的一个节，因为它的值，"
        "也就是那个字符串的地址，现在还不知道。私有的计数器放进 bss：这个节只记下大小，因为它从全零开始，在文件里不占空间。然后是两个重定位节，也就是那些洞和"
        "填洞的东西，还有带着名字的符号表。<bookmark mark='b'/>这种格式叫 ELF，出自 1988 年美国电话电报公司的 System V，今天 Linux、各个 BSD 和大多数游戏机都在用。"
        "Pebble 的目标文件是它的一个玩具版。",
    "The symbol table says what each file offers and what it needs.":
        "符号表说明每个文件提供什么、需要什么。<bookmark mark='a'/>main.o 把 main 和 greeting 定义为全局符号，其他文件看得见；计数器则是局部的。它把 total、"
        "count 和 C 库的 printf 列为未定义：这里用到，别处定义。lib.o 全局地定义了 count 和 total，并把 verbose 定义为弱符号。它还需要 strlen：优化器认出 count "
        "的循环是在求字符串长度，就把它换成了一次库调用。<bookmark mark='b'/>重定位精确地说明哪些字节依赖哪个符号、以什么方式依赖：这里有从指令到目标的 32 位"
        "距离，有可能经过一张表的调用，那张表我们在第十一章会见到，还有给指针用的完整 64 位地址。",
    "From these tables the linker applies a few rules.":
        "根据这些表，链接器执行几条规则。<bookmark mark='a'/>某个文件需要的每个符号，都必须在某处有定义。<bookmark mark='b'/>同一个名字有两个强定义，是错误。"
        "<bookmark mark='c'/>一个强定义胜过任意多个弱定义，<bookmark mark='d'/>如果只有弱定义，就挑其中一个。<bookmark mark='e'/>去掉 lib.o，这台机器的链接器"
        "就报告未定义的引用；把它放进去两次，就报告重复定义。弱符号的存在，是为了让库可以提供一个程序能覆盖的默认实现，比如默认的错误处理函数，甚至 malloc 本身。",
    # ------------------------------------------------------------------ Linking
    "Chapter ten. Linking, step by step.": "第十章。一步一步地链接。",
    "Now our own linker, on the Job's four object files.":
        "现在用我们自己的链接器，处理任务的四个目标文件。<bookmark mark='a'/>每个文件都说明自己定义了什么、需要什么。main 定义了 start，需要 getc、lookup 和 "
        "report。表定义了 lookup 和 report，需要 alloc、putc 和 printnum。alloc 和 io 什么都不需要。<bookmark mark='b'/>第一件事是把每个需求和恰好一个定义配上对。"
        "这里每个名字都只定义了一次，所以每个都得到一个地址。<bookmark mark='c'/>漏掉分配器，或者把它放进去两次，Pebble 的链接器就会拒绝，抱怨的和这台机器的"
        "链接器一模一样。",
    "Step two: decide where everything goes.":
        "第二步：决定每样东西放在哪里。<bookmark mark='a'/>链接器先摆放所有文件的代码，按给出文件的顺序一个接一个，每段按十六字节对齐。然后是它们全部的数据。"
        "<bookmark mark='b'/>再然后是 bss 节，它们占地址，但在文件里不占字节：这里是分配器那三百八十四千字节的堆。<bookmark mark='c'/>所以程序文件只有八百六十四"
        "个字节，内存里的程序却将近四百千字节。既然每个节都有了地址，每个符号也就有了。",
    'f"Step three: fill the holes.':
        "第三步：把洞填上。<bookmark mark='a'/>四个文件里一共有{len(ps)}条重定位。每一条说明洞在哪里、是哪种洞、该填进哪个符号的地址。<bookmark mark='b'/>"
        "拿一条来看：表的代码用 la 载入它链表头的地址，汇编器把它发成一条 lui 加一条 ori，立即数都是零。head 现在住在 {hl['target']}。链接器把它拆成高二十二位"
        "{hi}和低十位{lo}，写进这两条指令。<bookmark mark='c'/>对一次调用，它把从调用处到函数的距离，以指令条数计，写进跳转的 22 位字段。<bookmark mark='d'/>"
        "静态链接器做的就是这些。把结果装载起来运行，四个文件就表现得像一个程序。",
    # ------------------------------------------------------------------ Dynamic
    "Chapter eleven. Dynamic linking.": "第十一章。动态链接。",
    'f"A two-line program that prints hello':
        "一个打印 hello 的两行程序，在这台计算机上用两种方式链接。<bookmark mark='a'/>静态链接时，它用到的那部分 C 库被复制进文件：{st['bytes'] / 1024:.0f}千"
        "字节。动态链接时，文件只有{dy['bytes'] / 1024:.0f}千字节，<bookmark mark='b'/>因为它只装着一张条子，说它需要 C 库，外加一份它要从库里取的函数清单："
        "这里只有 puts，带一个版本标签，说明它期望 glibc 的哪一版接口。<bookmark mark='c'/>代价是一点启动工作，找到并映射这个库，在这里大约十分之一毫秒。"
        "<bookmark mark='d'/>好处很大：内存里只有一份库，被每个用它的进程共享；修复库里的一个安全漏洞，就同时修好了每一个程序。ldd 会列出一个程序要装载什么。",
    "How does a call reach a library whose address is not known":
        "一次调用怎样到达一个直到程序运行才知道地址的库？<bookmark mark='a'/>共享库在不同的进程里装载在不同的地址，所以它的代码里不能有绝对地址。它被编译成"
        "位置无关代码：它需要的每个地址都放在一张数据表里，叫全局偏移表，由装载器填写。<bookmark mark='b'/>调用另一个库要经过过程链接表里的一个小桩，它跳到"
        "表里存着的地方。<bookmark mark='c'/>第一次调用时，表指回动态链接器，后者查到这个函数，把它的真实地址写进表里，<bookmark mark='d'/>然后跳过去。以后的"
        "每次调用都经过桩直达函数。这叫惰性绑定，也正是我们在 count 上看到 PLT32 重定位的原因。",
    "Dynamic linking has a remarkable side effect":
        "动态链接有一个了不起的副作用：你可以不碰程序就替换一个库函数。<bookmark mark='a'/>把 LD_PRELOAD 设成你自己的一个库，动态链接器就会先在它里面找，"
        "再找 C 库。<bookmark mark='b'/>于是 Perl 调用 malloc 时，到达的是我们的 malloc，它记下这个请求，再调用真正的那个，后者是通过请求同名的下一个定义找到的。"
        "<bookmark mark='c'/>第六章就是这样从一个没改过的 Perl 里记下将近二十七万七千个事件的。<bookmark mark='d'/>性能分析器和内存泄漏检查器用的是同一个技巧，"
        "有时恶意软件也是。",
    # ------------------------------------------------------------------ Loading
    "Chapter twelve. Loading and the address space.": "第十二章。装载与地址空间。",
    "Here is a real process on this computer":
        "这是这台计算机上的一个真实进程，按 Linux 在 /proc/self/maps 文件里的描述。<bookmark mark='a'/>最底下是程序本身：它的常量、代码和数据。它们上面是堆，"
        "随着 malloc 要更多内存而向上长。远在上方，是映射进这个空间的 C 库和动态链接器。最顶上是栈，它向下长。中间的空隙大得惊人，数以太字节计的地址根本没有"
        "映射。<bookmark mark='b'/>每个区域都有自己的权限。代码可以执行但不能写。数据和栈可以写但不能执行，这一点在第十四章会很要紧。",
    "Run a program that prints where things are, three times.":
        "运行一个打印各样东西位置的程序，运行三次。<bookmark mark='a'/>main 的地址、一个全局变量的地址、一个堆块的地址、栈上一个局部变量的地址，以及 C 库 "
        "printf 的地址。每次运行，每一个都不同。<bookmark mark='b'/>这就是地址空间布局随机化。它由 PaX 项目在 2001 年引入，如今到处都默认开启。它的意义在于"
        "安全：一个需要知道某样东西在哪里的攻击，比如第十四章那个，就只能去猜。<bookmark mark='c'/>把它关掉，栈每次都在同一个地址。",
    "Last, how does main get its arguments?":
        "最后，main 怎样拿到它的参数？<bookmark mark='a'/>当你键入 job pride.txt，操作系统的装载器把这些字符串复制到新进程栈的最顶端，在它们下面放一个指向"
        "这些字符串的指针数组，以空指针结尾，再下面是它们的个数。<bookmark mark='b'/>第一段运行的代码不是 main，而是一个叫 start 的小例程，它找到这些值，再拿"
        "它们调用 main。<bookmark mark='c'/>Pebble 的装载器，也就是我们链接器里的最后一个函数，建的正是这个布局，并把个数和数组放在 a0 和 a1 里传过去。",
    # ------------------------------------------------------------------ Undefined
    "Chapter thirteen. Undefined behaviour.": "第十三章。未定义行为。",
    "C leaves some operations undefined.":
        "C 把一些操作留作未定义。<bookmark mark='a'/>有符号整数溢出、读过数组的末尾、解引用空指针、释放之后还用那块内存。<bookmark mark='b'/>对这些，标准"
        "并不说程序会崩溃，或者给出错的答案。它什么也不说：任何行为都允许。<bookmark mark='c'/>这样做有它的理由。不同的机器处理溢出的方式不同，而检查每次"
        "数组访问要花时间。<bookmark mark='d'/>但现代的优化器得出了一个更尖锐的结论：既然正确的程序从不做这些事，编译器就可以假定它们永远不会发生，并按这个"
        "假定来优化。我们在这台计算机上测了这会带来什么。",
    "First, signed overflow.":
        "先看有符号溢出。<bookmark mark='a'/>一个函数问 x 加一是否大于 x。对最大的整数，x 加一会溢出。<bookmark mark='b'/>在真实的机器上，它绕回成最小的"
        "负数，所以诚实的答案是否。但 gcc 回答是，也就是一，因为如果溢出不可能发生，x 加一总是更大，它根本什么都不算。<bookmark mark='c'/>一个循环给一个正的"
        "计数器每次加十亿，直到它变成负数：不开优化跑了三圈，开了优化跑两圈。同样的源代码，两种行为。<bookmark mark='d'/>选项 -fwrapv 告诉 gcc 溢出会绕回，"
        "这时两个答案就都是诚实的了。",
    "Second, a null check.":
        "再看一次空指针检查。<bookmark mark='a'/>这个函数先通过一个指针读数，然后才检查这个指针是不是空的。<bookmark mark='b'/>不开优化，gcc 两样都编译出来："
        "取数、比较、提前返回。<bookmark mark='c'/>开了优化，整个函数就是一次取数加一次返回。理由是：程序已经解引用了 p，而解引用空指针是未定义的，所以 p 不可能"
        "是空的，所以这个检查永远不会触发。<bookmark mark='d'/>这不是假想。2009 年，Linux 内核网络隧道驱动里恰好就是这个模式，让编译器删掉了一个空指针检查，"
        "结果可以被利用。从那以后，Linux 一直用一个禁止这种优化的选项来编译。这一章的教训是：在 C 里，你想写的程序和你写下的程序可能不一样，而优化器只认你写下"
        "的那个。",
    # ------------------------------------------------------------------ Smash
    "Chapter fourteen. Smashing the stack.": "第十四章。栈溢出攻击。",
    "Here is the greeting program from the start of this part, on Pebble.":
        "这是本部分开头那个打招呼的程序，放在 Pebble 上。<bookmark mark='a'/>greet 建一个八十字节的栈帧。底部是装名字的六十四字节缓冲区；靠近顶部是保存的"
        "返回地址，回到调用者的路。<bookmark mark='b'/>它把缓冲区交给 gets，后者和 C 的 gets 一样，一直复制输入直到看见换行，不管有多长。<bookmark mark='c'/>"
        "复制是向上进行的，从缓冲区底部朝保存的返回地址去。所以一个长过七十六字节的名字就会碰到它。",
    'f"So here is the attack.':
        "攻击是这样的。<bookmark mark='a'/>它的第一部分是代码：{nb // 4}条 Pebble 指令，打印字母 p、w、n、e、d 然后停下，共{nb}个字节。<bookmark mark='b'/>"
        "然后是{pad}个字节的填充，填满缓冲区剩下的部分和那段空隙：到这里共七十六个字节。<bookmark mark='c'/>然后是恰好落在保存的返回地址上的四个字节：缓冲区"
        "自己的地址。<bookmark mark='d'/>gets 把它全部复制进去。greet 打印问候，从栈上恢复返回地址，而那个地址现在是我们的，然后返回，返回进了缓冲区，我们的代码"
        "就在那里运行。<bookmark mark='e'/>在模拟器上，它打印出 pwned。攻击者只需要知道一件事：栈在哪里；而在一台没有随机化的机器上，这永远不变。1988 年莫里斯"
        "蠕虫就是这样在互联网的 fingerd 服务器之间传播的，而 Aleph One 1996 年的文章《为了乐趣和利益粉碎栈》把它教给了所有人。",
    "Every program on this computer ships with defences":
        "这台计算机上的每个程序都带着针对这种攻击的防御，我们把每一种都做进了 Pebble。<bookmark mark='a'/>栈金丝雀：函数在返回地址下方存一个秘密的字，返回前"
        "检查它。溢出要碰到返回地址就必须踩坏金丝雀，于是程序报告错误并停下，而不是跳走。<bookmark mark='b'/>不可执行的栈：栈所在的页可以写，但不能运行，所以"
        "跳进缓冲区会出错。<bookmark mark='c'/>随机化：栈每次运行都在新的地方，所以攻击者的地址只是一个猜测。<bookmark mark='d'/>还有每个指针上的边界，它能在"
        "第一个越界的字节就抓住它；这是前沿一章的内容。<bookmark mark='e'/>没有哪一种单独就完美。攻击者对付不可执行栈的办法，是把程序里已有的代码片段缝合起来，"
        "也就是面向返回的编程，第55部分会讲它。",
    # ------------------------------------------------------------------ Job
    "Chapter fifteen. The Job, linked.": "第十五章。链接起来的任务。",
    "Here is the Job written the way a compiler would write it.":
        "这是按编译器的写法写出来的任务。<bookmark mark='a'/>main 把字母读进它自己栈帧里的一个缓冲区。表是堆上十六字节节点组成的链表，按单词第一次出现的次序"
        "排列，所以平局的打破方式和以前完全一样。分配器只是在 bss 的三百八十四千字节里往前推一个指针，从不释放任何东西，任务也只需要这些。输入输出例程里有 "
        "printnum，它把数字放在自己栈帧里的一个小缓冲区中。<bookmark mark='b'/>每个节点装着指向下一个节点的指针、指向单词字母的指针、它的长度和它的计数。"
        "<bookmark mark='c'/>每个函数都遵守第四章的调用约定。",
    "How does it compare with Part 6's single hand-written file?":
        "它和第6部分那个手写的单文件比怎么样？<bookmark mark='a'/>在一个段落、《傲慢与偏见》的第一章和两万字节上，输出每次都完全相同。<bookmark mark='b'/>"
        "在那个段落上，版本一慢了几个百分点：现在每个输入字节都要付出一次函数调用和返回。<bookmark mark='c'/>在更长的文本上它更快，两万字节时快百分之十一，因为"
        "顺着 next 指针走，每个表项比在数组里数过去少一条指令。<bookmark mark='d'/>栈从没深过三百二十个字节。<bookmark mark='e'/>原来结构在这里几乎不花什么。"
        "但算法没有变：每个词仍要为扫一遍词汇表付出代价。第13部分的编译器会自动写出这个程序，而第四幕会改变算法。",
    # ------------------------------------------------------------------ Frontier
    "Chapter sixteen. The frontier.": "第十六章。前沿。",
    "The defences of chapter fourteen all work around the real problem":
        "第十四章的那些防御，都是在绕开真正的问题：C 里的指针只是一个数，没有谁知道它背后的对象有多大。<bookmark mark='a'/>CHERI 项目，由剑桥大学和 SRI 从 "
        "2010 年开始，改造了硬件，让指针成为一种能力：一个地址，连同对象的边界和权限，外加一个程序无法伪造的隐藏标签位。<bookmark mark='b'/>每次取数和存数都要"
        "对照所用指针的边界检查，而新的指针只能从已有的指针造出来，而且永远不能变大。Arm 在 2022 年造出了原型处理器 Morello。<bookmark mark='c'/>我们在 Pebble "
        "的模拟器里加了一个微缩版：greet 取它缓冲区的地址时，这个指针得到六十四字节的边界，边界随它一起走。<bookmark mark='d'/>再跑一遍攻击，机器在第六十五个"
        "字节上陷入，那时还没碰到返回地址；诚实的名字照常得到问候。",
    "The second frontier is meaning.":
        "第二个前沿是含义。<bookmark mark='a'/>要证明一个编译器是正确的，你需要给源程序的含义一个精确的定义，连同未定义行为。<bookmark mark='b'/>泽维尔·勒鲁瓦"
        "的 CompCert 始于 2006 年，是一个 C 编译器，它的每一遍都在 Coq 证明助手里被证明，对每个没有未定义行为的程序都保持其含义；那些在其他每个编译器里都找到"
        "错误的测试，在它被证明的部分里一个也没找到。<bookmark mark='c'/>卡万·梅马里安、彼得·休厄尔和同事们的 Cerberus 项目，为程序员实际使用的 C 建立了一套"
        "可执行的语义。<bookmark mark='d'/>结果最难的问题是指针来源：一个指针被允许到达哪个对象，即使两个指针装着同一个地址。它的一个模型正在被标准化。"
        "<bookmark mark='e'/>仍然悬而未决的，是一套标准、优化器和数十亿行现有代码都能接受的语义。",
    "And the allocators of chapters six to eight have frontiers of their own.":
        "第六到第八章的分配器也有它们自己的前沿。<bookmark mark='a'/>罗布森界能被一个精心设计的分配器达到，但对大家都在用的策略，首次适配和最佳适配，确切的最坏"
        "情况至今未知。<bookmark mark='b'/>与此同时，真实的程序离最坏情况远得很。马克·约翰斯通和保罗·威尔逊 1998 年测量了真实的程序，发现好的策略只浪费百分之几，"
        "正如我们在 Perl 上看到的。<bookmark mark='c'/>真实程序为什么如此友好，从没有哪个模型解释过。<bookmark mark='d'/>而分配器如今是安全的战场：释放之后"
        "还使用内存，是大型 C 和 C++ 程序里最常见的严重错误之一，浏览器现在用延迟重用的隔离区、按类型分开的堆，以及像 Chrome 的 MiraclePtr 那样的智能指针来防御。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭了什么。程序从源代码到进程的一生。字节、对齐和数组，以及作为分支和跳转表的控制流。调用栈、它的栈帧，以及让分别编写的函数能够合作的调用"
        "约定。五个分配器跑在一个真实程序的十四万六千次分配上，克努特法则和罗布森界都由模拟证实。Pebble 的链接器和装载器，以及在这台计算机上测量的同一套机制，"
        "经过动态链接和随机化的地址空间。还有会出的错：未定义行为，以及栈溢出攻击和四种防御。",
    "Where this comes back.":
        "这些会在哪里再出现。写出我们这种代码的编译器是第13部分。能移动对象、从而摆脱罗布森界的垃圾回收器是第15部分。异常控制流、信号和系统调用是第31部分，地址"
        "空间背后的页是第32部分。证明程序和编译器正确是第54部分，而重用程序自身代码的攻击，以及你究竟能不能信任你的编译器这个问题，是第55部分。",
    "In practice. A debugger's backtrace":
        "在实践中。调试器的回溯就是沿着栈帧往上走。AddressSanitizer、Valgrind 和未定义行为检测器会在第十三、十四章那些错误发生时就找到它们。大多数构建错误是"
        "链接错误：未定义的引用、重复的符号、顺序不对的库。在大型服务器上，换一个分配器是最便宜的性能收益之一。而栈保护、不可执行页、随机化和控制流完整性，"
        "每一个主流工具链都默认开启。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在本部分的笔记里。随时可以暂停。第五题是一道动手题：用 Pebble 汇编写一个真正的分配器，并在 Perl 的轨迹上拿它和模拟器对照。最后一道"
        "标着星号，是研究题：它的答案尚不知道，笔记里写了从哪里入手。",
    "Next time. To build Part 13's compiler":
        "下一次。要搭第13部分的编译器，我们先需要阅读文本的理论：正则表达式、有限自动机和文法，以及由它们构造的语法分析器。第12部分，语言与自动机。",
    "The books and papers this part follows":
        "这一部分依据的书和论文都在屏幕上和笔记里。感谢观看。",
})

ZH.update({
    # ------------------------------------------------------------------ added: practice sections
    "A debugger reads the same structure on a real machine.":
        "调试器在真实的机器上读的是同一个结构。<bookmark mark='a'/>我们在这台计算机上编译了一个 C 写的阶乘，在 gdb 里运行，让它停在最深的那次调用，fact(1)。"
        "<bookmark mark='b'/>要它给出回溯，gdb 列出六个栈帧：五次 fact 调用和 main。<bookmark mark='c'/>它是沿着栈走过去找到它们的。每个栈帧都保存着调用者的帧地址"
        "和自己的返回地址，所以调试器从栈指针出发，就能一帧一帧地走。它报告的栈指针彼此相差三十二个字节，每个是 fact 的一个栈帧。<bookmark mark='d'/>保存的"
        "返回地址讲出了这串调用的故事：其中四个指向 fact 里的同一条指令，也就是递归调用之后的那一条；第五个返回进 main，而 main 的返回进启动它的 C 库。回溯不过"
        "如此。",
    "Real programs also link against libraries":
        "真实的程序还要链接库，而静态库不过是目标文件的一个归档。<bookmark mark='a'/>这是我们建的一个，libjob.a，里面有两个成员：count.o，以及带着一张"
        "十万字节表格的 unused.o。<bookmark mark='b'/>链接器从左到右读它的输入，并记着一份仍未定义的名字清单。读完 main.o，清单里有 count。<bookmark mark='c'/>"
        "在归档里，它只取那些能定义清单上某个名字的成员：count.o 进来了，unused.o 留在外面。",
    'f"Real programs also link against libraries':
        "真实的程序还要链接库，而静态库不过是目标文件的一个归档。<bookmark mark='a'/>这是我们建的一个，libjob.a，里面有两个成员：count.o，以及带着一张"
        "十万字节表格的 unused.o。<bookmark mark='b'/>链接器从左到右读它的输入，并记着一份仍未定义的名字清单。读完 main.o，清单里有 count。<bookmark mark='c'/>"
        "在归档里，它只取那些能定义清单上某个名字的成员：count.o 进来了，unused.o 留在外面。程序是{kb_ar}千字节；改为直接列出全部三个目标文件，则是{kb_obj}千"
        "字节。<bookmark mark='d'/>现在把库放在前面。链接器读到它时，还没有任何未定义的名字，所以它什么也不取；然后 main.o 需要 count，已经晚了。未定义的引用："
        "count。<bookmark mark='e'/>这就是为什么在命令行上，库要放在用到它的文件之后。",
    "The practical defence is to catch undefined behaviour as it happens.":
        "实用的防御，是在未定义行为发生时就抓住它。<bookmark mark='a'/>用未定义行为检测器编译，我们那个溢出的加法就会停下来报告：最大的 int 加一，无法用 int "
        "类型表示。<bookmark mark='b'/>AddressSanitizer 抓的是内存错误：在 malloc 给的一个六十四字节块的末尾之后写一个元素，<bookmark mark='c'/>从一个已经释放的"
        "块里读，<bookmark mark='d'/>以及越过栈上一个数组的末尾去写，正是下一章的那个错误。每份报告都给出地址、源代码的行号，对堆还会说明那个块是在哪里分配的。",
    'f"How does it know?':
        "它是怎么知道的？<bookmark mark='a'/>AddressSanitizer 在每次分配的周围加上有毒的红区，并且把释放的块在隔离区里放一阵子，而不是马上再分出去。"
        "<bookmark mark='b'/>它在影子内存里记下哪些字节可以碰：程序的每八个字节对应一个影子字节，零表示这八个字节都没问题。<bookmark mark='c'/>编译器在程序的每次"
        "取数和存数前面，都插入一次对影子的检查。<bookmark mark='d'/>这要付出代价。在这台机器上，我们统计《傲慢与偏见》词频的程序用了{w:.1f}倍的时间，而一个只做 "
        "malloc 和 free 的循环用了{m:.0f}倍。所以检测器在测试和模糊测试时打开，谷歌的 OSS-Fuzz 就用它们在开源代码里找到了数以万计的错误，而在生产环境中关掉。",
})
del ZH["Real programs also link against libraries"]
