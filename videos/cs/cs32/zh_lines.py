"""Chinese narration for cs32: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第32部分：虚拟内存"

CHAPTERS = {
    "Hook": "两个程序，一个地址",
    "Problem": "1. 保护与重定位",
    "Segments": "2. 基址与界限，以及段",
    "Paging": "3. 分页",
    "Tables": "4. 多级页表",
    "Tlb": "5. 快表（TLB）",
    "Faults": "6. 缺页",
    "Replacement": "7. 换出哪一页",
    "Curves": "8. 工作集与抖动",
    "Cow": "9. 写时复制、零页与 mmap",
    "KernelMap": "10. 内核自己的映射",
    "Alloc": "11. 内核分配器",
    "Virt": "12. 虚拟机",
    "Containers": "13. 容器",
    "PebbleVM": "14. PebbleOS 有了虚拟内存",
    "Frontier": "15. 前沿：翻译覆盖范围与分层内存",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Two copies of the same program run on our machine.":
        "同一个程序的两个副本在我们的机器上运行。<bookmark mark='a'/>每个副本都把自己的进程号存到同一个地址：十六进制的四零五零零四。"
        "然后各自让出处理器，好让另一个把自己的号码存到这个地址上。<bookmark mark='b'/>接着每个都把这个地址读回来。进程一读到一，进程二读到二。"
        "<bookmark mark='c'/>它们用的是同一个地址，却是两个不同的内存字节。<bookmark mark='d'/>程序使用的每一个地址都是虚拟的。硬件在每一次读、写和取指令时，"
        "都通过内核为这个进程维护的一张表来翻译它。这一部分把这种翻译做进 Pebble，并追问它的代价是什么、又换来了什么。",
    "Part 32 of Computer Science, Built: Virtual Memory.":
        "计算机科学，从零搭建，第32部分：虚拟内存。<bookmark mark='a'/>这一部分包括：程序为什么需要重定位和保护，以及页为什么胜出；页表，"
        "硬件在每次访问时遍历的那棵树，以及让它变快的缓存，在这台机器上实测；缺页，以及一趟磁盘之旅的代价；内存满了时该扔掉哪一页，包括最优解、"
        "一个著名的异常和真实系统中的策略；写时复制、内核自己的映射与 Meltdown，以及内核的分配器；还有虚拟机和容器，我们自己的操作系统将运行在"
        "我们亲手写的虚拟机监控器上。",
    # ------------------------------------------------------------------ Problem
    "Chapter one. Protection, and relocation.": "第1章。保护与重定位。",
    "In Part 31, PebbleOS gave each process its own region of physical memory.":
        "在第31部分，PebbleOS 给每个进程一块自己的物理内存区域。<bookmark mark='a'/>分词器被编译成在一兆字节处运行，那项任务在两兆字节处，"
        "每个程序只能在那里工作。这带来了四个问题。<bookmark mark='b'/>重定位：程序只能在链接时指定的位置运行，所以第二个副本需要再编译一次，"
        "而复制一个进程的 fork 根本做不到。<bookmark mark='c'/>保护：界限寄存器只守护一段连续的范围，所以两个进程不能共享一个库，代码也不能设为只读。"
        "<bookmark mark='d'/>大小：程序永远不能大于它的区域。<bookmark mark='e'/>还有碎片，下一章会展示。<bookmark mark='f'/>四个问题的解决办法是同一个："
        "给每个进程它自己的虚拟地址，让硬件翻译每一个地址。",
    "The idea came from Manchester.":
        "这个想法来自曼彻斯特。<bookmark mark='a'/>Atlas 计算机有一块小而快的磁芯存储器，和一个大六倍、慢得多的磁鼓。<bookmark mark='b'/>它的设计者让程序"
        "寻址一块大的存储器，由机器自动地、按需地在磁芯和磁鼓之间搬运五百一十二个字的固定大小的页。<bookmark mark='c'/>磁芯的每一页都有一个寄存器，"
        "记着它当前装的是哪一页。地址所在的页若与其中之一相符，就全速运行；否则机器陷入，把那一页取来。<bookmark mark='d'/>汤姆·基尔伯恩和同事们在1962年"
        "称之为单级存储系统。<bookmark mark='e'/>此后每一部手机、笔记本和服务器都以同样的方式工作，只是用内存和闪存代替了磁芯和磁鼓。",
    # ------------------------------------------------------------------ Segments
    "Chapter two. Base and bounds, and segments.": "第2章。基址与界限，以及段。",
    "The simplest translation adds a base.":
        "最简单的翻译是加上一个基址。<bookmark mark='a'/>进程使用从零开始的地址。硬件先把每个地址和界限比较，太大就报错。<bookmark mark='b'/>然后加上基址，"
        "也就是内核放置这个进程的物理地址。<bookmark mark='c'/>两个寄存器，一次加法和一次比较，进程就能装在任何地方，而且碰不到它范围之外的任何东西。"
        "第31部分已有界限；加上基址，就有了重定位。<bookmark mark='d'/>段把它推广：代码、数据、堆和栈各有一对基址和界限，于是每一段都能独自增长，"
        "代码也能共享。<bookmark mark='e'/>Burroughs B5000 在1961年就有了段，英特尔 8086 在1978年也有。现代 x86 处理器几乎完全放弃了它们，原因就在"
        "下一张图里。",
    "The trouble with segments is that they come in every size.":
        "段的麻烦在于它们大小各异。<bookmark mark='a'/>我们模拟了一千零二十四个单位的内存，大小随机的段不断到来和离开，每段放进第一个足够大的空洞。"
        "这是运行结束时的内存：彩色的是活着的段，红框是空洞。<bookmark mark='b'/>第一次拒绝来得很早：一个九十单位的请求，而空闲的有一百三十八个，"
        "却分散在八个空洞里，最大的只有六十三。<bookmark mark='c'/>整个运行中，有两百四十七个请求被拒绝。<bookmark mark='d'/>这正是第11部分 malloc 的问题，"
        "如今出现在内核里。<bookmark mark='e'/>可以把段挪到一起来紧缩内存，但复制时每个进程都得停下来。<bookmark mark='f'/>出路是让每一块都一样大。这样任何"
        "空闲块都能满足任何请求。这样的一块就叫页。",
    # ------------------------------------------------------------------ Paging
    "Chapter three. Paging.": "第3章。分页。",
    "Paging cuts memory into pieces of one size":
        "分页把内存切成同样大小的块，在我们的机器上是四 KiB，并分别翻译每一块。<bookmark mark='a'/>这是本部分开头的那个地址，写成二进制。"
        "<bookmark mark='b'/>低十二位是页内偏移，原样通过。<bookmark mark='c'/>高二十位是虚拟页号，要翻译的正是它。<bookmark mark='d'/>我们的硬件把页号再分成"
        "两个十位的索引，对应你马上会看到的两级表。<bookmark mark='e'/>而且因为物理内存的每个页框大小相同，任何空闲页框都能装任何页。块与块之间的碎片"
        "消失了；最多浪费每个区域最后一页的一部分。",
    "Each entry in a page table is one word.":
        "页表的每一项是一个字。<bookmark mark='a'/>高二十位指明物理页框。低位是标志。<bookmark mark='b'/>有效位表示这一页是否映射了。读、写、执行三位说明"
        "可以对它做什么，于是代码可以只执行，数据永远不被执行。用户位说明用户态程序能不能碰它。<bookmark mark='c'/>还有两位由硬件自己设置：访问位，"
        "每次使用时设置；脏位，每次写入时设置。<bookmark mark='d'/>内核把它们读回来。访问位告诉它哪些页在用，第7章需要它；脏位告诉它哪些页在页框"
        "被重用前必须写回磁盘。",
    "Now the walk itself, done in hardware":
        "现在看遍历本身，每当访问在第5章的那个缓存中未命中时，由硬件完成。<bookmark mark='a'/>控制寄存器 ptbr 保存当前进程一级表的物理地址。"
        "地址的前十位在那里选出一项，它指向一张二级表。<bookmark mark='b'/>接下来的十位在二级表中选出一项，它指明页框。加上偏移，就是物理地址。"
        "<bookmark mark='c'/>两个进程用的索引相同，但它们由内核建立的表指向不同的页框，所以同一个地址在一个进程里装着一，在另一个里装着二。"
        "<bookmark mark='d'/>每张一级表的第零项都相同：它映射内核，第10章会解释。",
    # ------------------------------------------------------------------ Tables
    "Chapter four. Multi-level page tables.": "第4章。多级页表。",
    "Why two levels?":
        "为什么要两级？一张平坦的表，三十二位地址空间里的一百万页每页一项，每个进程需要四 MiB，几乎全都写着“未映射”。<bookmark mark='a'/>所以表是一棵树。"
        "第一级有一千零二十四项，每项覆盖四 MiB。<bookmark mark='b'/>在我们的进程中只用了两项：第零项用一个大页映射内核，第一项指向进程的二级表。"
        "<bookmark mark='c'/>那张表只为真正映射的页设项。<bookmark mark='d'/>每一级解析页号的十位，就像第21部分的字典树。<bookmark mark='e'/>一个空的一级表项"
        "覆盖四 MiB，根本不需要二级表。<bookmark mark='f'/>所以我们的进程只需要八 KiB 的页表，而不是四 MiB。<bookmark mark='g'/>代价是每次翻译每一级都要读一次内存。",
    "Real machines go deeper.":
        "真实的机器层级更深。<bookmark mark='a'/>对我们的三十二位地址，平坦的表是四 MiB。对 x86-64 的四十八位，每个进程五百一十二 GiB。<bookmark mark='b'/>所以"
        "x86-64 用四级，每级九位，每张四 KiB 的表有五百一十二个八字节的表项。<bookmark mark='c'/>从2019年起，服务器可以用五级，支持五十七位地址，于是"
        "翻译缓存的一次未命中，在真正的读之前可能要读五次内存。<bookmark mark='d'/>有些设计把表倒过来，每个物理页框一项，用虚拟页号的哈希来查找；"
        "PowerPC 和 Itanium 就是这样做的。",
    # ------------------------------------------------------------------ Tlb
    "Chapter five. The translation lookaside buffer.": "第5章。快表，即翻译后备缓冲器。",
    "A walk costs two extra memory reads in our machine":
        "在我们的机器上，一次遍历要多读两次内存，在现代机器上最多五次，而且是每一次访问都要。解决办法是一个保存最近翻译的小缓存，即翻译后备缓冲器，"
        "简称 TLB，IBM 360 的 67 型在1967年就有了。<bookmark mark='a'/>我们在分页的 PebbleOS 上把那项任务作为两个进程来运行，用不同大小的 TLB。"
        "<bookmark mark='b'/>四项时，百分之三点五的访问未命中，需要遍历。八项时，不到百分之一。十六项时，一万一千次访问才有一次：两个程序的工作集都"
        "装得下。<bookmark mark='c'/>但每次上下文切换都会写入新的页表根，我们的硬件随之清空 TLB。每五百条指令切换一次，未命中增加到八倍。给每一项"
        "标上它所属的地址空间，即地址空间标识符，表项就能熬过切换：四十三次未命中，而不是五百零八次。<bookmark mark='d'/>真实的处理器有两级 TLB，"
        "带有标识，x86 称之为进程上下文标识符。",
    "On this machine we can watch the TLB from outside.":
        "在这台机器上，我们可以从外面观察 TLB。<bookmark mark='a'/>一个程序沿着一串指针穿过越来越多的页，每页只碰一个缓存行，我们为每一步计时。"
        "<bookmark mark='b'/>不超过六十四页时，每步不到两纳秒：每个翻译都在一级 TLB 里。<bookmark mark='c'/>超过六十四页，时间跳了一级：二级 TLB 更慢。"
        "<bookmark mark='d'/>再往后，遍历开始了，缓存本身也满了，每步的时间不断攀升。到六万五千页时，一步约一百纳秒。<bookmark mark='e'/>现在换成两 MiB 的页"
        "再来一遍。程序碰的缓存行完全相同，但每个 TLB 项覆盖的内存多了五百一十二倍，每步降到不到六十纳秒。<bookmark mark='f'/>这就是数据库和虚拟机要求"
        "大页的原因，也是 Linux 在可能时自动建立大页的原因。",
    # ------------------------------------------------------------------ Faults
    "Chapter six. Page faults.": "第6章。缺页。",
    "What happens when a program touches a page that is not mapped?":
        "程序碰到一个没有映射的页时会发生什么？<bookmark mark='a'/>它执行一条存储指令。TLB 里没有这一项，于是硬件遍历页表，发现表项无效。"
        "<bookmark mark='b'/>它陷入，原因是十五，地址放在 tval 里。<bookmark mark='c'/>内核检查这个地址是否在进程的内存范围之内，然后取一个空闲页框。"
        "它填充这个页框：新的堆页或栈页填零，否则从磁盘读入数据。它写好表项，用 eret 返回到同一条存储指令，这一次就成功了。<bookmark mark='d'/>出错的"
        "指令从未真正执行过，所以它可以简单地再执行一次。<bookmark mark='e'/>这就是按需调页：在被碰到之前什么都不映射。<bookmark mark='f'/>PebbleOS 现在就"
        "这样做。一个碰了十六个新堆页的程序发生十六次缺页，每次大约三千三百条内核指令，几乎全都在写零。",
    "When memory is full, a fault must first free a frame":
        "内存满了时，一次缺页必须先腾出一个页框，而其中的页总得有个去处。<bookmark mark='a'/>第3章的脏位决定它去哪里。<bookmark mark='b'/>干净的页，"
        "自从从文件读入后没有改过，可以直接丢掉：如果再需要，就再读一次。<bookmark mark='c'/>脏页必须先写出去，而堆页或栈页根本没有文件，所以只能去交换空间，"
        "那是专门为此留出的一个分区或文件。<bookmark mark='d'/>这让缺页的代价翻倍。在那项任务的序列上，用 LRU、八个页框时，百分之四十四的换出是脏页。"
        "<bookmark mark='e'/>所以内核不等缺页发生。一个换出守护进程，Linux 里叫 kswapd，在后台成批地把脏页写回，并备好一池空闲页框，让缺页时只需要读。",
    "How much does a fault cost?":
        "一次缺页要花多少？<bookmark mark='a'/>在这台机器上，碰一个已经映射的页要二十五纳秒。第一次碰一个全新的页，一次缺页加上把四 KiB 清零，"
        "要将近两微秒。<bookmark mark='b'/>必须从存储设备读取的缺页要糟得多：从闪存约一百微秒，从机械硬盘八毫秒。<bookmark mark='c'/>所以一次内存访问的"
        "平均代价取决于它多常缺页。<bookmark mark='d'/>用磁盘时，一千次访问里有一次缺页，内存就慢八十倍。即使一百万次里一次，也要多出百分之八。"
        "<bookmark mark='e'/>一个换页到磁盘的系统，只有在缺页比百万分之一还少时才可用，这就是内存耗尽时感觉像跌下悬崖的原因。",
    # ------------------------------------------------------------------ Replacement
    "Chapter seven. Which page to evict.": "第7章。换出哪一页。",
    "When memory is full and a fault needs a frame, some page must go.":
        "内存满了，而一次缺页需要一个页框时，必须有某一页离开。<bookmark mark='a'/>哪一页？<bookmark mark='b'/>拉斯洛·贝拉迪在1966年证明，最好的选择是"
        "下一次使用在最遥远未来的那一页。<bookmark mark='c'/>这是它在贝拉迪所用的引用串上、三个页框时的表现：七次缺页，没有任何策略能做得更好。"
        "<bookmark mark='d'/>证明是一个交换论证，就像第31部分里最短作业优先的那个。假设某个调度在一次缺页时换出页 f，而最优解会换出 e，于是 f 会在 e 之前"
        "再被需要。<bookmark mark='e'/>把它改为换出 e，然后照搬原来的调度。当 f 下一次被请求时，新调度要么命中，要么付出原调度本来也要付出的那一次缺页。"
        "所以新调度绝不会更差，而且与最优解多一致了一步。<bookmark mark='f'/>但这个最优解需要知道未来。它是一把尺子，而不是一个策略。真实的策略只能"
        "根据过去猜测未来。",
    "The simplest guess is first in, first out":
        "最简单的猜法是先进先出：换出装入最久的那一页。<bookmark mark='a'/>这是贝拉迪用的引用串，三个页框。每一列是一次引用；红点是缺页。九次缺页。"
        "<bookmark mark='b'/>现在给 FIFO 第四个页框。十次缺页。内存更多，缺页更多。<bookmark mark='c'/>贝拉迪、尼尔森和谢德勒在1969年发表了这个结果，"
        "它让人们大吃一惊，因为这意味着买更多内存可能让机器变慢。<bookmark mark='d'/>它很罕见：两万个随机串里我们只找到两个。但它确实会发生，而有些策略"
        "根本不可能出现它。",
    "A better guess: the past predicts the future.":
        "更好的猜法：过去预示未来。换出最久没有使用的那一页。<bookmark mark='a'/>在贝拉迪的串上，最近最少使用在三个页框时比 FIFO 还差，但从不出现异常。"
        "<bookmark mark='b'/>原因是包含性质。<bookmark mark='c'/>k 个页框时，LRU 恰好持有最近使用的 k 个页；k 加一个时，持有最近的 k 加一个，其中包括前者。"
        "<bookmark mark='d'/>所以任何在 k 个页框时命中的引用，在更多页框时也命中，增加内存永远不会增加缺页。有这种性质的算法叫栈算法，OPT 也是其中之一。"
        "<bookmark mark='e'/>我们检查了五千个随机串：LRU 没有任何异常。",
    "How far from the optimum can LRU be?":
        "LRU 离最优解能有多远？<bookmark mark='a'/>取四个页循环使用，三个页框。LRU 总是恰好换出下一个要用的页，所以每一次引用都缺页。<bookmark mark='b'/>"
        "知道未来的最优解，大约每三次才缺一次。在一百二十次引用上：一百二十次缺页，对四十二次。有 k 个页框时，对手能让任何确定性策略的缺页约为最优解的 k 倍。"
        "<bookmark mark='c'/>斯利特和塔扬在1985年证明这就是最坏情况：LRU，还有 FIFO，都在最优解的 k 倍之内，而没有任何确定性策略能保证更好。更有用的是，给 LRU "
        "k 个页框、最优解只给 h 个：倍数降到 k 除以 k 减 h 加一，当 LRU 有两倍内存时不到二。<bookmark mark='d'/>在那项任务的真实序列上还要更好。有两倍内存时，"
        "LRU 不只是在两倍之内，而是直接胜过最优解。真实的程序不是对手。",
    "True LRU would reorder a list on every memory access":
        "真正的 LRU 要在每次内存访问时重排一个列表，无论对硬件还是软件都太频繁了。实用的近似是时钟算法。<bookmark mark='a'/>每个页框保存硬件设置的访问位。"
        "<bookmark mark='b'/>缺页时，一根指针绕着页框扫过。访问位已置的页框得到第二次机会：清掉这一位，指针继续前进。第一个访问位为零的页框被换出。"
        "<bookmark mark='c'/>普通访问时什么也不做，只在缺页时动作。<bookmark mark='d'/>真实的内核改进了这个想法，而更新的策略，2Q、ARC 和 LIRS，还能防止一次"
        "扫描冲掉所有有用的页，下一章会展示。",
    # ------------------------------------------------------------------ Curves
    "Chapter eight. Working sets, and thrashing.": "第8章。工作集与抖动。",
    "How do the policies compare on a real program?":
        "这些策略在真实程序上比较起来如何？<bookmark mark='a'/>我们记录了那项任务在一段十六千字节的文本上的每一次内存引用，共十二万次，涉及三十九个"
        "一 KiB 的页，并在每一种内存大小下把它们重放给每一种策略。<bookmark mark='b'/>八个页框时，最优解缺页一万两千次，LRU 两万三千次，FIFO 两万九千次。"
        "<bookmark mark='c'/>LRU 处在最优解和 FIFO 之间，时钟算法紧随其后。<bookmark mark='d'/>而且因为 LRU 是栈算法，它的整条曲线只需扫一遍序列就能得到："
        "记录每一页再次被使用时在最近使用栈中有多深。这是马特森和同事们在1970年的技巧，至今仍用来确定缓存的大小。<bookmark mark='e'/>四十个页框时一切都"
        "装得下，只有第一次接触才缺页。",
    "Here is that trick worked by hand, on eight references.":
        "下面在八次引用上手算这个技巧。<bookmark mark='a'/>把页放在一个栈里，最近使用的在顶上。对每次引用，找出它的页有多深：这个深度就是它的栈距离。"
        "从未见过的页，距离为无穷大。<bookmark mark='b'/>然后把它移到顶上。页 b 在深度二被找到，a 在深度三，c 在深度四。<bookmark mark='c'/>现在是关键的事实。"
        "k 个页框的 LRU 恰好持有这个栈最上面的 k 页，所以一次引用命中，当且仅当它的距离不超过 k。<bookmark mark='d'/>数一数大于 k 的距离，就得到 LRU 的缺页数："
        "一个页框八次，两个七次，三个五次，四个四次。<bookmark mark='e'/>扫一遍就得到所有内存大小的结果。整条 LRU 曲线就是这样从那项任务序列的一遍扫描中得到的，"
        "至今缓存的大小也还是这样选的。",
    "LRU has a famous weakness.":
        "LRU 有一个著名的弱点。<bookmark mark='a'/>这是一条像数据库那样的序列：二十个热页反复使用，然后是对六十个页的一次扫描，每页只用一次，如此循环往复。"
        "<bookmark mark='b'/>三十二个页框时，LRU 几乎每次引用都缺页，时钟算法也一样。<bookmark mark='c'/>每次扫描都在热页再次被需要之前把它们挤出去，因为"
        "被扫描的页更新。<bookmark mark='d'/>自适应替换缓存 ARC 维护两个列表，只见过一次的页和见过两次的页，并在学习中移动两者的分界。LIRS 按一页最近两次"
        "使用之间的距离给页排序，所以只用一次的页永远不会挤掉常用的页。两者都好得多，LIRS 接近最优。",
    "Peter Denning gave the idea that ties this together.":
        "彼得·丹宁给出了把这一切串起来的思想。<bookmark mark='a'/>程序在时刻 t 的工作集，是它在最近 τ 次引用中用过的页的集合。<bookmark mark='b'/>这是沿着"
        "那项任务的序列、三种窗口下的工作集：任意一百次引用中，那项任务大约用九个页；在更长的窗口里，它会用到全部三十九个。<bookmark mark='c'/>丹宁为分时机器"
        "定下的规则：把每个运行中进程的工作集都留在内存里；如果装不下，就少运行几个进程。",
    "Break that rule and you get thrashing.":
        "违反这条规则，就会抖动。<bookmark mark='a'/>我们模拟了若干进程共享六十四个页框，每个进程的工作集为二十页，并且时不时要等待普通的输入输出。"
        "<bookmark mark='b'/>进程越多，处理器就用其他工作填满等待，三个进程时忙到一半。<bookmark mark='c'/>但四个二十页的工作集装不进六十四个页框。这时每个"
        "进程都缺页，每次缺页都要等那一个磁盘，利用率下降。<bookmark mark='d'/>八个进程时处理器几乎闲着，磁盘却从不停歇：机器全在换页。<bookmark mark='e'/>"
        "六十年代的操作系统学会了把整个进程移出内存来应对；Linux 在内存真正耗尽时，会杀掉一个进程。",
    # ------------------------------------------------------------------ Cow
    "Chapter nine. Copy-on-write, zero pages, and memory-mapped files.": "第9章。写时复制、零页与内存映射文件。",
    "Fork promises the child a copy of all the parent's memory.":
        "fork 承诺给子进程一份父进程全部内存的副本。虚拟内存让它不用复制就能兑现承诺。<bookmark mark='a'/>fork 只复制页表，于是两个进程指向同样的页框，"
        "并把两边的每一页都标为只读。<bookmark mark='b'/>读不花任何代价。<bookmark mark='c'/>当任一进程写一页时，这次写会出错。内核看到这一页是共享的，"
        "并非真的只读，就把它复制到一个新页框，把副本以可写方式映射给写的一方，再让这次写继续。<bookmark mark='d'/>只有真正被写的页才会被复制。fork 之后"
        "立刻 exec，也就是外壳的做法，几乎什么都不复制。Mach 内核在八十年代后期让这成为标准做法。",
    "On this machine: <bookmark mark='a'/> a parent using two hundred":
        "在这台机器上：<bookmark mark='a'/>一个使用两百五十六 MiB 的父进程 fork 不到六毫秒，因为只复制了页表。<bookmark mark='b'/>然后子进程在每一页写一个字节。"
        "每页的第一次写要三微秒：一次缺页，加上复制四 KiB。<bookmark mark='c'/>对同一页的第二次写要二十六纳秒，一次普通的存储。<bookmark mark='d'/>第31部分"
        "里带一 GiB 的 fork 用了三十三毫秒，全花在页表上。<bookmark mark='e'/>而一个写遍自己全部内存的子进程，最终还是要为复制买单，一次缺页一次缺页地付。",
    "The same machinery, mapping and faulting, serves three more purposes.":
        "同样的机制，映射加缺页，还有三个用途。<bookmark mark='a'/>进程申请了却从未写过的内存，从一个共享的全零页框读出零，第一次写时才得到私有的一页。"
        "<bookmark mark='b'/>mmap 把文件的页放进地址空间，于是读文件只是一次读内存；这些页来自内核对磁盘的缓存。<bookmark mark='c'/>共享库，第11部分的 libc，"
        "从同样的页框以只读方式映射进每个进程，所以一百个进程只持有一份副本。<bookmark mark='d'/>代价是，从映射文件的一次读，可能不知不觉地要等磁盘。",
    # ------------------------------------------------------------------ KernelMap
    "Chapter ten. The kernel's own mapping.": "第10章。内核自己的映射。",
    "Where does the kernel itself live?":
        "内核自己住在哪里？<bookmark mark='a'/>在每个进程的地址空间里。同样的内核页出现在每一张页表中，标为仅限内核态：用户态碰不到它们，但它们一直在那里。"
        "<bookmark mark='b'/>所以陷入时不需要切换页表：内核的代码和数据已经映射好了。<bookmark mark='c'/>在我们的 PebbleOS 中，它是每张一级表的第零项，"
        "一个四 MiB 的页。读它的用户程序会出错并被杀掉。<bookmark mark='d'/>而且因为进程的页也映射着，内核可以直接用进程传给它的地址来复制进程的缓冲区。",
    "In 2018 that arrangement broke.":
        "2018年，这种安排被打破了。<bookmark mark='a'/>Meltdown，第8部分预告过：在许多英特尔处理器上，用户态从内核地址读取确实会出错，但乱序核心在那之前"
        "已经推测性地用过这份数据了。<bookmark mark='b'/>数据通过缓存泄露出来，于是仅靠内核态标志位已经不能保住内核的秘密。<bookmark mark='c'/>解决办法是内核页表"
        "隔离。每个进程有两张表：在用户态几乎不映射内核，只映射处理入口的几页。<bookmark mark='d'/>现在每次系统调用和中断都必须切换页表。有地址空间标识时，"
        "切换很便宜；没有时，每次都要清空 TLB，有些负载慢了三分之一。<bookmark mark='e'/>这台机器的处理器报告自己不受影响，因为更新的芯片在硬件里修复了这个"
        "缺陷，Linux 在这里就跳过了隔离。",
    # ------------------------------------------------------------------ Alloc
    "Chapter eleven. How the kernel allocates memory for itself.": "第11章。内核如何为自己分配内存。",
    "The kernel needs memory too":
        "内核也需要内存：用于页表、进程控制块、网络缓冲区。它以物理页框为单位取用，而页框的经典分配器是伙伴系统，出自1965年的诺尔顿。"
        "<bookmark mark='a'/>内存保存在大小为二的幂的块中。三页的请求向上取整为四页。<bookmark mark='b'/>没有空闲的四页块，于是十六页分裂成两个八页，"
        "其中一个八页再分裂成两个四页。第一个四页交出去；被分出的另一半留在空闲链表上。<bookmark mark='c'/>每个块的伙伴，通过翻转它地址中的一位就能找到。"
        "<bookmark mark='d'/>所以释放很快：如果伙伴也空闲，就合并，再到大一级重试。碎片永远不会让两个空闲的伙伴并排躺着。",
    "Run it under random traffic":
        "让它承受随机的流量：一千零二十四页，三千步，每一步要么分配一到三十页，要么释放之前的一个块。<bookmark mark='a'/>块分裂了五百八十三次，合并了"
        "五百一十七次。<bookmark mark='b'/>没有一个请求被拒绝：始终有一个至少四分之一池大小的空闲块，通常是一半。<bookmark mark='c'/>第2章的段，在同样大小的池里，"
        "拒绝了两百四十七个。<bookmark mark='d'/>代价是块内部的浪费：五页要占一个八页的块。<bookmark mark='e'/>Linux 正是用它来管理物理页框，有十一种大小，"
        "从一页到一千零二十四页，你可以在 /proc/buddyinfo 里读到空闲链表。",
    "And here are this machine's own free lists":
        "这是这台机器自己的空闲链表，刚刚从 /proc/buddyinfo 读出来。<bookmark mark='a'/>每根柱子是一个阶：左边是单页，右边是四 MiB 的块。"
        "<bookmark mark='b'/>空闲的将近六 GiB。<bookmark mark='c'/>其中将近一半在最大的块里，随时可以为任何请求分裂，或者变成大页。<bookmark mark='d'/>而空闲的单页"
        "只有八个：释放的页几乎总能找到伙伴并合并。<bookmark mark='e'/>在一台跑了好几个星期的繁忙机器上，高阶的块会用光。这时一次大页请求就得等待紧缩：内核"
        "把页挪来挪去，同时更新它们的映射，以重建大的空闲块。",
    "But most of what a kernel allocates is small":
        "但内核分配的大部分东西都很小：一个套接字、一个打开的文件、一个一百字节左右的进程控制块。每个给一页就太荒唐了。<bookmark mark='a'/>杰夫·邦威克"
        "1994年为 SunOS 写的 slab 分配器，为每一种对象保留一个缓存。每个缓存把页切成恰好那么大的槽：一页装五十六个七十二字节的对象。"
        "<bookmark mark='b'/>一万个这样的对象，每个一页要四十一兆字节，用 slab 不到四分之三兆字节。<bookmark mark='c'/>还有邦威克的第二个想法：释放的对象回到"
        "它的 slab 时仍保持初始化状态，于是同类对象的下一次分配可以省去初始化。<bookmark mark='d'/>Linux 的分配器叫 SLUB，就源于它；在任何 Linux 机器上，"
        "slabtop 都能显示它的缓存。",
    # ------------------------------------------------------------------ Virt
    "Chapter twelve. Virtual machines.": "第12章。虚拟机。",
    "Virtual memory gives each process a private memory.":
        "虚拟内存给每个进程一块私有的内存。同样的技巧用在整台机器上，就给每个操作系统一台私有的计算机。IBM 的 VM/370 在1972年就做到了。"
        "<bookmark mark='a'/>把客户机内核原封不动地放在用户态运行，下面是一个小小的虚拟机监控器，只有它拥有真正的特权。<bookmark mark='b'/>每当客户机内核"
        "做特权操作，比如写控制寄存器，它就会陷入。监控器在它为这个客户机保存的寄存器副本上完成这个操作，然后返回。<bookmark mark='c'/>波佩克和戈德堡"
        "在1974年把条件说得精确。如果一条指令读取或改变机器的模式、控制状态或设备，就称它为敏感指令。<bookmark mark='d'/>如果它在用户态会陷入，就称它为"
        "特权指令。<bookmark mark='e'/>如果每条敏感指令都是特权指令，陷入并模拟就行得通。<bookmark mark='f'/>Pebble 通过了：全部四条特权指令，以及对设备页的"
        "每一次访问，在用户态都会陷入。<bookmark mark='g'/>当客户机自己的进程发起系统调用时，监控器把它转交回去：像硬件那样，在客户机的虚拟寄存器里保存"
        "程序计数器、设置原因，然后跳到客户机内核。",
    "We built that hypervisor for Pebble":
        "我们为 Pebble 写了这样一个监控器，并在它上面运行第31部分的内核，一条指令都没改。<bookmark mark='a'/>两个打印字母的进程：客户机内核退出到监控器"
        "将近六百次，大多是在上下文切换中读写控制寄存器。<bookmark mark='b'/>输出与原生运行完全相同，客户机执行的指令数也一样：客户机察觉不到。"
        "<bookmark mark='c'/>那项任务的流水线讲的是另一个故事。它通过控制台设备传送四千六百字节，几乎每一次退出都是一次设备访问，每字节一次。"
        "<bookmark mark='d'/>这就是真实的监控器提供半虚拟化设备的原因，Xen 在2003年就这样做，今天的 virtio 也是：客户机知道自己是虚拟的，一次退出交出"
        "整个缓冲区。",
    "The x86, the processor in most computers, failed":
        "x86，大多数计算机里的处理器，没有通过波佩克和戈德堡的检验。<bookmark mark='a'/>罗宾和欧文后来数出十七条不会陷入的敏感指令。其中一条 popf，"
        "在用户态运行时会悄悄忽略关中断的那一位，所以客户机内核甚至不知道自己失败了。<bookmark mark='b'/>VMware 在1999年的答案是二进制翻译：在客户机内核"
        "的代码运行时改写它，替换掉麻烦的指令，而用户代码直接运行。<bookmark mark='c'/>Xen 在2003年的答案是修改客户机内核，让它公开地调用监控器。"
        "<bookmark mark='d'/>后来英特尔和 AMD 在内核之下增加了一种新模式，x86 通过了检验。<bookmark mark='e'/>出人意料的是，亚当斯和阿格森测得第一代硬件方案"
        "比 VMware 的软件还慢，因为每次退出都太昂贵了。",
    "Memory needs virtualising too.":
        "内存也需要虚拟化。客户机内核用它以为是物理地址的东西建立页表；监控器有自己的一张表，把这些地址映射到真正的地址。<bookmark mark='a'/>现代硬件两张表"
        "都遍历。每个客户机表项位于一个客户机物理地址上，所以硬件在读它之前，必须先遍历主机的四级找到它，然后才能读。<bookmark mark='b'/>四个客户机层级，"
        "每级五次引用，再加四次翻译最终地址：一次 TLB 未命中要二十四次内存引用，而原生遍历只要四次。<bookmark mark='c'/>一般地，是 n 加一乘以 m 加一，再减一。"
        "<bookmark mark='d'/>在这种硬件出现之前，监控器维护影子页表，把两张表合二为一，还得捕捉客户机对自己页表的每一次修改。<bookmark mark='e'/>嵌套分页，"
        "AMD 在2007年、英特尔在2008年推出，结束了这种做法，代价是二维的遍历，这也是大页在虚拟机里更加重要的原因。",
    # ------------------------------------------------------------------ Containers
    "Chapter thirteen. Containers.": "第13章。容器。",
    "A virtual machine is one way to give a program its own world.":
        "虚拟机是给程序一个自己的世界的一种办法。<bookmark mark='a'/>每个客户机带着自己的内核，运行在监控器上。<bookmark mark='b'/>容器是另一种办法。"
        "只有一个内核，它只是向不同的进程组展示不同的视图：它们自己的进程号、自己的文件、自己的网络和用户。<bookmark mark='c'/>容器几毫秒就能启动，"
        "不带第二个内核。但一台机器上的所有容器都信任同一个内核，这就是我们稍后要回头讨论的代价。",
    "On Linux the views are called namespaces.":
        "在 Linux 上，这些视图叫命名空间。<bookmark mark='a'/>这是在这台机器上创建的一个，不需要任何特殊权限：一个新的用户命名空间和一个新的进程命名空间，"
        "里面跑着一个外壳。<bookmark mark='b'/>这个外壳以为自己是一号进程，而且是 root，用户零。让它列出进程，它只看到三个：它自己和它刚运行的两个命令。"
        "在外面，这台机器正运行着八十二个。<bookmark mark='c'/>命名空间有八种：进程、文件树、网络、用户编号，以及四种小一些的。<bookmark mark='d'/>第二种"
        "成分是控制组，它限制一组进程能用多少各种资源：处理器时间、内存、进程数等等。<bookmark mark='e'/>再加上一棵用来运行的文件树，就是一个容器。Docker "
        "在2013年把这三者组合成人人都能用的形式。",
    "Side by side.":
        "并排比较。<bookmark mark='a'/>虚拟机要启动一个内核，几秒钟；容器只是启动一个进程，几毫秒。<bookmark mark='b'/>每个虚拟机在内存里装着一整个客户机"
        "内核；容器共享一个内核及其磁盘缓存。<bookmark mark='c'/>但虚拟机通往主机的唯一的门是监控器和它那几种退出。容器的门是整个 Linux 系统调用接口，"
        "大约四百五十个调用。<bookmark mark='d'/>所以一个内核漏洞就能突破所有容器。<bookmark mark='e'/>2016年的 Dirty COW，正是第9章写时复制代码里的一个竞争，"
        "让任何进程都能写它只能读的文件。<bookmark mark='f'/>业界的答案是折中：谷歌的 gVisor 在用户空间放第二个内核，亚马逊的 Firecracker 把虚拟机做得足够小，"
        "大约一百二十五毫秒就能启动。<bookmark mark='g'/>亚马逊的无服务器函数，每一个都运行在这样的虚拟机里。",
    # ------------------------------------------------------------------ PebbleVM
    "Chapter fourteen. PebbleOS gains virtual memory.": "第14章。PebbleOS 有了虚拟内存。",
    "Our own machine has had all of this since chapter three.":
        "从第3章起，我们自己的机器就已经有了这一切。下面是它所需要的。<bookmark mark='a'/>硬件：Pebble 的内存管理单元，带两级遍历、十六项的 TLB，"
        "以及三种新的错误。<bookmark mark='b'/>引导程序为每个进程建一张页表，第零项是内核的超级页，代码页可读可执行，数据页可读可写。<bookmark mark='c'/>上下文切换"
        "多了两条指令，读入并写入页表基址寄存器，这也会清空 TLB。<bookmark mark='d'/>陷阱处理程序多了这一段：在进程范围之内、尚未映射的页上的缺页，得到一个"
        "清零的新页框，映射好，指令再执行一次。<bookmark mark='e'/>其他任何错误都杀掉进程，就像第31部分那样。<bookmark mark='f'/>总共四十六条指令：内核从"
        "两百八十四条增长到三百三十条。",
    "Here is the whole page table of the hook's first process":
        "这是开头那个第一个进程的整张页表，从我们的机器里读出来。<bookmark mark='a'/>库的代码，然后是三页输入输出缓冲区，然后是程序自己的代码，以及它的数据页，"
        "里面装着开头的那个单元。<bookmark mark='b'/>然后是两百四十九个从未映射的页，而在最顶端，是栈。<bookmark mark='c'/>这些位说明了一切。代码可读可执行，"
        "从不可写；数据可写，从不可执行；每一页都标为用户态可用；硬件在程序运行时设置了访问位和脏位。输出缓冲区是脏的，因为程序打印了东西。<bookmark mark='d'/>"
        "两百五十六页中映射了七页：一兆字节的地址空间只用了二十八 KiB 内存。<bookmark mark='e'/>而栈位于代码之上整整一 MiB 处，中间什么都不用付钱：两者都有"
        "增长的余地。",
    "Now four processes on one machine.":
        "现在，一台机器上四个进程。<bookmark mark='a'/>一个打印八个字母 A。<bookmark mark='b'/>一个把零写到自己的第一条指令上。它的代码页映射了，但不可写："
        "一次存储错误，原因十五，内核杀掉它。<bookmark mark='c'/>一个从它内存之外的地址读取：一次读取错误，原因十三，被杀掉。<bookmark mark='d'/>还有一个沿着"
        "它的堆往上走，碰了十六个新页。它发生十六次缺页，每次得到一个清零的页框，然后打印一个 G。<bookmark mark='e'/>控制台上只有幸存者的输出。"
        "<bookmark mark='f'/>写代码是保护错误；野读则完全在进程之外。<bookmark mark='g'/>两种情况下，硬件只负责报告，由内核决定，其他进程毫无察觉。",
    "Finally, the pipeline that has run through this series":
        "最后，是贯穿这套课程的那条流水线：分词器向那项任务供数据，作为两个进程，现在各自在自己的地址空间里。<bookmark mark='a'/>不分页时，第31部分的"
        "内核用五十五万八千条指令运行它。<bookmark mark='b'/>分页，并在启动时映射所有页，只多了十二条。<bookmark mark='c'/>分页并按需提供零页，发生七次缺页，"
        "多了两万两千条指令。<bookmark mark='d'/>输出逐字节相同。<bookmark mark='e'/>所以翻译本身几乎是免费的：每次切换为页表寄存器多两条指令，其余都由 TLB "
        "藏起来了。<bookmark mark='f'/>一次按需缺页大约三千条指令，几乎全在清零。<bookmark mark='g'/>按需调页换来的是内存：两个进程只需要二十四个页框，"
        "而不是一百四十六个，因为那项任务的哈希表大部分从未被碰过。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen. The frontier: translation reach, and memory in tiers.": "第15章。前沿：翻译覆盖范围与分层内存。",
    "The first frontier is reach":
        "第一个前沿是覆盖范围：TLB 不用遍历就能翻译多少内存。<bookmark mark='a'/>一个六十四项的一级数据 TLB，用四 KiB 的页，覆盖两百五十六 KiB，比这台机器的"
        "二级缓存还小。二级 TLB 有一千五百项，覆盖六 MiB。<bookmark mark='b'/>一台笔记本有十六 GiB；一台大服务器有四 TiB，是覆盖范围的一百万倍。"
        "<bookmark mark='c'/>大页把覆盖范围放大五百一十二倍，或者二十五万多倍。<bookmark mark='d'/>在第5章的阶梯上，对两百五十六 MiB 的指针追逐，用两 MiB 的页"
        "少花了百分之四十的时间。<bookmark mark='e'/>但大页在只用到一小部分时会浪费内存，而且需要两 MiB 连续的物理页框，繁忙机器上的伙伴分配器未必拿得出来。",
    "Research attacks reach from several sides.":
        "研究从几个方向进攻覆盖范围问题。<bookmark mark='a'/>直接段，2013年：给大服务器的堆一个基址与界限寄存器，与普通分页并存。<bookmark mark='b'/>冗余内存"
        "映射：一个小小的范围 TLB，每项覆盖一大段连续区域。<bookmark mark='c'/>Ingens 和 HawkEye：决定内核何时把小页提升为大页的策略，在进程之间公平，又不让"
        "内存膨胀。<bookmark mark='d'/>Midgard：让缓存工作在一个中间地址空间里，只在通往内存的路上才翻译。<bookmark mark='e'/>还有2023年的 Mosaic 页：把每一页"
        "限制在通过哈希选出的少数几个页框里，于是一个表项可以描述好几页。<bookmark mark='f'/>请注意第2章的段回来了：一大段连续的范围翻译起来很便宜。",
    "The second frontier is that memory is no longer one thing.":
        "第二个前沿是，内存不再是单一的东西。<bookmark mark='a'/>除了处理器自己通道上的 DRAM，服务器现在还能通过 CXL 接上更多内存，CXL 是 PCI Express 链路上的"
        "一种协议，延迟是本地的两到三倍。再往外，是磁盘。<bookmark mark='b'/>于是操作系统再次面对第7章的问题，只是换了个花样：不是换出哪一页，而是哪些页配得上"
        "快的那一层。<bookmark mark='c'/>而它几乎是盲的。内核只能从访问位了解使用情况，要读到新鲜的访问位，就得清除它们，并清空每个核心的 TLB。"
        "<bookmark mark='d'/>Meta 的 TPP，2023年，把冷页降到慢的一层，把在那里经常缺页的页提升上来；它现在已是 Linux 的一部分。<bookmark mark='e'/>处理器也能"
        "在硬件里对内存访问采样。内核能多准确、多便宜地用这种办法找到热页，仍是一个开放问题。",
    "The third frontier is the foundations.":
        "第三个前沿是基础。<bookmark mark='a'/>页表本身就是内存。硬件遍历器用普通的读取来读它们，而另一个核心上的内核可能正在修改它们，所以翻译继承了第10部分"
        "弱内存模型的全部困难。<bookmark mark='b'/>直到2022年，本·西姆纳和同事们才发表了一个精确的模型，描述虚拟内存在 Arm 处理器上的行为，经过硬件测试，"
        "并得到 Arm 架构师的认可。<bookmark mark='c'/>修改一个映射，意味着要打断每一个可能缓存了它的核心，即 TLB 击落，每次花费几微秒，限制了多核系统重新映射"
        "内存的速度。<bookmark mark='d'/>而像 seL4 这样经过验证的内核证明了自己页表代码的正确性，所依据的 MMU 模型本身却必须被信任。",
    "Six open problems. <bookmark mark='a'/> What should replace":
        "六个开放问题。<bookmark mark='a'/>当内存以太字节计时，什么应该取代四级基数树？<bookmark mark='b'/>内核何时应该组建大页，何时应该拆开，在 TLB 未命中与"
        "浪费的内存、紧缩的代价之间权衡？<bookmark mark='c'/>它怎样才能为分层内存找到热页，开销有界而且准确性可证？<bookmark mark='d'/>一个学习得来的预测器能把"
        "LRU 改进多少，同时在预测出错时仍保有保证？<bookmark mark='e'/>TLB 击落怎样才能扩展到几百个核心？<bookmark mark='f'/>在弱内存模型的处理器上，带嵌套分页的"
        "虚拟机监控器能被验证吗？<bookmark mark='g'/>本部分的研究问题取第二个问题的一个可计算的小情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们建造了什么。地址翻译，从 Atlas 到四级基数树，以及让它几乎免费的 TLB。缺页、按需调页，以及贝拉迪的最优解、他的异常，还有排除了 LRU "
        "出现异常的栈性质。工作集、抖动、写时复制，以及内核为自己使用的分配器。虚拟机，从波佩克和戈德堡到嵌套遍历，还有容器。还有带 MMU 的 PebbleOS，"
        "让每个进程运行在同样的地址上。",
    "Where this comes back.":
        "这些内容会在哪里再出现。在第33部分，线程共享同一个地址空间，这带来了竞争，以及我们刚见过的 TLB 击落。第34部分给 PebbleOS 加上磁盘，带页缓存和"
        "内存映射文件。第35部分的数据库维护自己的缓冲池和自己的替换策略。第45部分用微虚拟机和容器搭建云。第48部分再次遇到 LRU，作为服务前面的缓存。"
        "第55部分攻击内存安全，以及保护它的地址空间随机化。",
    "In practice. Look before you tune":
        "实践中。先观察再调优：进程的 smaps 文件、vmstat，以及 perf 对 TLB 未命中的计数。数据库和 Java 虚拟机通常需要显式的大页，而透明大页可能在内核"
        "紧缩内存时造成延迟尖峰。当一个进程消失时，内存耗尽杀手的理由记在内核日志里；给控制组设限，而不要依赖交换。大进程的 fork 会复制它的页表，所以要"
        "早点派生辅助进程，或者用 posix_spawn。还要记住，容器共享一个内核：不可信的代码应该放进虚拟机。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在本部分的讲义里。可以在任何一题上暂停。第五题是动手题：给 PebbleOS 加上写时复制的 fork。最后一题标着星号，是研究问题："
        "事后回看，决定在浪费内存的预算之内哪些区域值得用大页，这是 Ingens 和 HawkEye 靠启发式回答的那个问题的离线版本。",
    "Next time, Part 33: Concurrency.":
        "下一次，第33部分：并发。两个线程各给一个计数器加一，计数却只增加了一。Peterson 锁，被证明正确，然后被硬件的重排打破；锁、信号量、管程和死锁；"
        "以及内存模型的理论，和哪些原子操作能构造哪些。线程共享这一部分努力分开的一切。第33部分，并发。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分依据的书籍和论文列在屏幕上和讲义里。感谢观看。",
}

PHRASES = {}
