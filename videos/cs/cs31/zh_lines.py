"""Chinese narration for cs31: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第31部分：内核"

CHAPTERS = {
    "Hook": "一台机器，许多程序",
    "History": "1. 从批处理到分时",
    "Protection": "2. 保护：模式位",
    "Traps": "3. 陷阱与系统调用",
    "Process": "4. 进程",
    "Switch": "5. 上下文切换",
    "Fork": "6. fork、exec 和 wait",
    "Scheduling": "7. 调度：FCFS、SJF、SRTF",
    "Mlfq": "8. 轮转与多级反馈队列",
    "Share": "9. 按比例分享：彩票、步幅、CFS",
    "Multi": "10. 多个处理器",
    "RealTime": "11. 实时",
    "Queueing": "12. 排队论",
    "Designs": "13. 内核的设计",
    "PebbleOS": "14. PebbleOS 运行那项任务",
    "Frontier": "15. 前沿：经过验证的内核与微秒级调度",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In 1960 a computer cost millions of dollars":
        "1960年，一台计算机要花几百万美元，而它大部分时间都在等待。<bookmark mark='a'/>让一个人坐在控制台前，模式总是一样的：想十秒钟，"
        "然后要半秒钟的计算。<bookmark mark='b'/>处理器有百分之九十五的时间闲着。<bookmark mark='c'/>第一个办法是批处理：把程序打在穿孔卡片上交给操作员，"
        "几个小时后再来取打印结果。机器一直忙着，程序员却在等。<bookmark mark='d'/>第二个办法是分时：接上许多终端，轮流给每个用户一小段时间的整台"
        "机器。<bookmark mark='e'/>于是每个用户都看到一台属于自己的完整计算机，而计算机自己则在处理一个队列。",
    "By the end of this part, our own machine will do the same.":
        "到这一部分结束时，我们自己的机器也会这样做。这是 PebbleOS，一个我们即将写出的内核，正在 Pebble 计算机上启动，装着两个程序。"
        "<bookmark mark='a'/>每个程序把自己的字母，A 或 B，打印二十四次。<bookmark mark='b'/>图上显示，一条指令一条指令地，谁占着处理器：程序 A，"
        "然后是内核，橙色，然后是程序 B。定时器每九百条指令打断一次正在运行的程序，内核把处理器交给另一个。<bookmark mark='c'/>输出交错在一起。"
        "两个程序都不知道对方存在。<bookmark mark='d'/>十五次切换，十四次定时器中断，五十二次系统调用。<bookmark mark='e'/>而在这里，内核自己执行了"
        "全部指令的百分之四十四，因为每一个字母都是一次对内核的请求。让它变便宜，也是这个故事的一部分。",
    "Part 31 of Computer Science, Built: The Kernel":
        "计算机科学，从零搭建，第31部分：内核，也是第六幕的开始。<bookmark mark='a'/>这一部分包括：分时是怎样开始的；操作系统需要的保护硬件，"
        "我们把它加进 Pebble；陷阱与系统调用；进程，以及在进程之间切换的代价；fork、exec 和外壳；调度器，从先来先服务到 Linux 里的那一个，"
        "以及有截止期限的机器所遵循的规则；解释为什么繁忙的服务器会变慢的排队论；最后是 PebbleOS 运行那项任务。",
    # ------------------------------------------------------------------ History
    "Chapter one. From batch to time-sharing.": "第1章。从批处理到分时。",
    "Five systems tell the story.":
        "五个系统讲述了这个故事。<bookmark mark='a'/>1956年，通用汽车和北美航空为 IBM 704 写了一个监控程序，上一个作业一结束就装入下一个：这就是批处理，"
        "也可以说是第一个操作系统。<bookmark mark='b'/>1961年，麻省理工学院 Fernando Corbató 的小组演示了 CTSS，兼容分时系统。时钟在一小段时间后"
        "打断每个用户的程序，转到下一个，内存保护把各个程序隔开。它最终能同时服务约三十个用户。<bookmark mark='c'/>Multics 于1965年由麻省理工、"
        "贝尔实验室和通用电气开始，目标是像电网一样的计算公用设施，有保护环和一棵文件树。它雄心勃勃而又一再延期，贝尔实验室退出了。"
        "<bookmark mark='d'/>于是贝尔实验室的两个人，Ken Thompson 和 Dennis Ritchie，1969年在一台闲置的 PDP-7 上写了个小一些的东西：Unix。"
        "他们1973年用 C 重写了它，1974年发表了论文。<bookmark mark='e'/>1991年，芬兰学生 Linus Torvalds 宣布了一个为他的个人电脑写的、免费的"
        "类 Unix 内核。如今 Linux 运行着大多数服务器、每一部安卓手机，以及全世界最快的五百台超级计算机中的每一台。<bookmark mark='f'/>这一部分的"
        "思想都在1961年到1974年间定型，也正是你口袋里那部手机里的思想。",
    "How many users can share one machine? Treat each user as a loop.":
        "一台机器能让多少用户共享？把每个用户看作一个循环。<bookmark mark='a'/>想十秒钟，然后要半秒钟的处理器时间，再等回答。<bookmark mark='b'/>我们"
        "模拟了这个过程，处理器由所有等待者平分，这正是快速时间片轮转所近似的。<bookmark mark='c'/>用户很少时，没人需要等：响应时间就是那半秒的工作。"
        "<bookmark mark='d'/>但处理器每秒只能做两个作业，而二十个各想十秒钟的用户，每秒大约就要两个。超过二十一个用户，机器就一直忙着，每多一个用户，"
        "所有人的响应时间都多出半秒。<bookmark mark='e'/>拐点就在两条直线相交的地方，模拟结果沿着它们走。<bookmark mark='f'/>这是来自封闭排队理论的"
        "交互式响应时间定律：响应时间等于用户数除以吞吐量，再减去思考时间。我们会在第12章回到排队。",
    # ------------------------------------------------------------------ Protection
    "Chapter two. Protection, and the mode bit.": "第2章。保护，以及模式位。",
    "Before time-sharing, the one program running owned the machine":
        "在分时之前，正在运行的那一个程序拥有整台机器，什么都能做。同时有几个程序时，其中任何一个都能用三种方式毁掉所有人的一天。<bookmark "
        "mark='a'/>用一条指令：让机器停机，或者重新编程某个设备。<bookmark mark='b'/>用内存：写坏内核，或者写坏别的程序的数据。<bookmark mark='c'/>"
        "还有用时间：一个永远不把处理器还回来的循环。<bookmark mark='d'/>在我们至今搭建的 Pebble 上，任何一个程序里的一条 halt 就让一切停下。"
        "<bookmark mark='e'/>所以硬件必须从普通程序手里拿走三样东西：一些指令、大部分内存，以及对时间的控制。<bookmark mark='f'/>而且要求回它们，"
        "必须有且只有一条路：经过内核。",
    "Here is what Pebble gains, in under two hundred lines of the emulator.":
        "这是 Pebble 新得到的东西，在模拟器里不到两百行。<bookmark mark='a'/>四条指令，用的是我们在第6部分留空的操作码。ecall 陷入内核；它是唯一的门。"
        "eret 从陷阱返回。还有两条指令读写控制寄存器。<bookmark mark='b'/>控制寄存器保存着模式、陷阱在哪里发生以及为什么、陷阱应该去哪里、一个"
        "倒计时定时器，以及正在运行的程序可以触碰的内存边界。<bookmark mark='c'/>还有一位状态：模式。机器在内核态启动，降到用户态的唯一方式是 eret。"
        "<bookmark mark='d'/>在用户态，特权指令是非法的，任何超出边界或落在设备页里的地址都是故障。<bookmark mark='e'/>定时器按指令倒数；到零时它打断"
        "正在运行的程序，把处理器交还给内核。IBM 的 System/360 在1964年就有同样的想法，把两种模式叫作问题态和管理态。",
    "Now the test. PebbleOS starts four processes, three of them hostile.":
        "现在来测试。PebbleOS 启动四个进程，其中三个怀有敌意。<bookmark mark='a'/>一个把字母 A 打印十二次。一个执行 halt。一个往内核的内存里写一个零。"
        "还有一个循环六万次，从不调用内核。<bookmark mark='b'/>halt 在用户态是非法指令：硬件拒绝执行并陷入，内核杀死那个进程。那次写入超出了进程的边界："
        "又一次陷入，又一次杀死。<bookmark mark='c'/>那个霸占处理器的进程被定时器打断了一百二十一次，其他进程在间隙里运行。好的进程打印出全部十二个字母。"
        "<bookmark mark='d'/>每一种情况下，出错的指令都没有完成。硬件把它拦下，跳进内核，由内核决定怎么办。<bookmark mark='e'/>而只要程序守规矩，保护"
        "几乎不花代价：硬件在每次访问时做一次比较，与访问本身并行进行。",
    # ------------------------------------------------------------------ Traps
    "Chapter three. Traps, and the system call.": "第3章。陷阱，以及系统调用。",
    "A program asks the kernel for something by setting up its request in registers":
        "程序向内核要东西，是把请求放进寄存器，这里是三号调用，取得我的进程号，然后执行 ecall。<bookmark mark='a'/>硬件随即在一步之内做五件事。它保存"
        "程序计数器，好知道回到哪里。它记录原因：一次 ecall，若是故障还有出错的地址。它关掉中断。它切换到内核态，并记住原来的模式。它跳到内核在启动时"
        "选定的那一个地址。<bookmark mark='b'/>程序无法选择落在内核的哪里，这正是要点：每个请求都经过内核控制的同一道门。<bookmark mark='c'/>eret 撤销"
        "后三步，程序从它的 ecall 之后继续。<bookmark mark='d'/>同一个机制服务于指令本身引起的每一个事件，从 ecall 到除以零。<bookmark mark='e'/>来自外部"
        "的中断，比如定时器，也用同样的五步，发生在正在运行的程序的两条指令之间。",
    "Now follow one system call all the way down.":
        "现在把一次系统调用一路跟到底。一个进程调用 getpid，我们记下进程再次运行之前内核执行的每一条指令。<bookmark mark='a'/>每一条竖条是一条指令，"
        "按它的用途着色。<bookmark mark='b'/>先是二十六条指令把程序的寄存器存进它的进程控制块，因为内核自己马上要用这些寄存器。<bookmark mark='c'/>然后"
        "二十三条查明这是哪个调用。<bookmark mark='d'/>真正的工作只要三条指令：取出进程号，存到程序的 a0 将被恢复的地方。<bookmark mark='e'/>然后又是"
        "二十六条把每个寄存器放回去，eret 返回。<bookmark mark='f'/>七十八条指令，为了返回一个数。<bookmark mark='g'/>对于带缓冲区的调用，内核先检查"
        "缓冲区是否位于调用者的内存之内。传入一个指向内核的指针的程序，得到的是一个错误，而不是内核的秘密。",
    "On a real machine, this one, the numbers look like this.":
        "在一台真实的机器上，就是这一台，数字是这样的。<bookmark mark='a'/>一次普通的函数调用要一点五纳秒。<bookmark mark='b'/>向内核要进程号要一百一十二"
        "纳秒：大约七十五次函数调用。硬件陷入是其中一部分。保存状态是一部分。而自2018年以来，第8部分讲的针对 Spectre 和 Meltdown 的防御，给每一次"
        "穿越都增加了工作。<bookmark mark='c'/>有些请求完全不用陷入。Linux 把一页内核代码和数据映射进每个进程，叫作 vDSO，所以读时钟就是一次普通的"
        "函数调用：二十九纳秒，不用切换模式。",
    "Because each call has a fixed cost, programs ask for as much as they can at once.":
        "因为每次调用都有固定的代价，程序会一次要尽可能多。<bookmark mark='a'/>这里我们读一个已经在内存里的文件，缓冲区从一个字节到一个 MiB。<bookmark "
        "mark='b'/>每次调用一个字节，每字节要两百一十八纳秒。<bookmark mark='c'/>每次调用四 KiB，每字节只要十分之一纳秒，少了两千倍。<bookmark mark='d'/>"
        "在复制本身占主导之前，这条线的斜率是负一：每次调用的固定价格，分摊到更多字节上。<bookmark mark='e'/>用 strace 看一个真实的程序，它会打印每一次"
        "系统调用：单词计数程序 wc 用五百一十七次调用读完八 MiB，每次十六 KiB。<bookmark mark='f'/>这就是为什么 C 的 getc 传统上是一个基于缓冲区的宏，"
        "也是为什么我们的 PebbleOS 程序都链接一个一次读四 KiB 的小库。",
    # ------------------------------------------------------------------ Process
    "Chapter four. The process.": "第4章。进程。",
    "A process is a program while it runs":
        "进程就是正在运行的程序：代码，加上运行时变化的一切。<bookmark mark='a'/>这是 PebbleOS 下那项任务的进程：一 MiB 的内存，从它的下界到上界。"
        "最底下是每个进程都链接的小库和它的两个缓冲区。然后是任务本身编译出的代码，不到两 KiB。然后是它的全局变量，主要是第17部分的哈希表。最上面是"
        "栈，向下生长。<bookmark mark='b'/>进程的其余部分住在内核里，在它的进程控制块中。<bookmark mark='c'/>它的状态；它的十五个寄存器和程序计数器，"
        "每次陷入时保存；它的边界；它的编号；它的输入从哪里来、输出到哪里去；还有几个计数器。<bookmark mark='d'/>这就是内核在任意一条指令处停下一个程序、"
        "以后再若无其事地恢复它所需要的全部。<bookmark mark='e'/>PebbleOS 在一张表里放四个这样的块。Linux 里对应的东西有几百个字段，但思想相同。",
    "Every process moves through a few states.":
        "每个进程都在几个状态之间移动。<bookmark mark='a'/>它被创建并装入，变为就绪：能够运行，在等处理器。<bookmark mark='b'/>内核调度它，它开始运行。"
        "<bookmark mark='c'/>定时器触发时，它回到就绪，另一个进程得到处理器。<bookmark mark='d'/>当它要的东西还没有到，比如从空管道读字节，它就被阻塞，"
        "在字节到达、它被唤醒之前不花任何代价。<bookmark mark='e'/>当它调用 exit，它就结束了。<bookmark mark='f'/>这些数字是在 PebbleOS 里数出来的，"
        "当时我们的两个进程正在一段短文上运行那项任务：四十一次调度，三十八次定时器中断，一次等待管道。<bookmark mark='g'/>任何时刻，每个处理器上有"
        "一个进程在运行，就绪的可以有任意多个。<bookmark mark='h'/>选择下一个运行哪个就绪进程，就是调度器的全部工作，也是第7到第11章的主题。",
    # ------------------------------------------------------------------ Switch
    "Chapter five. The context switch.": "第5章。上下文切换。",
    "To switch from process A to process B, the kernel does three things.":
        "要从进程 A 切换到进程 B，内核做三件事。<bookmark mark='a'/>一次陷阱把它带进来，来自定时器或系统调用，它把 A 的寄存器和程序计数器存进 A 的"
        "进程控制块。<bookmark mark='b'/>调度器选中 B。<bookmark mark='c'/>然后内核装入 B 保存的寄存器，设置 B 的边界，用 eret 返回，进入 B，恰好在 B "
        "上次被停下的那条指令。<bookmark mark='d'/>在 PebbleOS 里，每个进程是十八个字，一次经由 yield 的切换要一百一十八条内核指令。<bookmark "
        "mark='e'/>真实的内核保存得更多：浮点和向量寄存器，在支持 AVX-512 的处理器上有两 KiB，而且它还要切换地址空间，那是第32部分的主题。"
        "<bookmark mark='f'/>两个进程都察觉不到。各自恢复时，寄存器都和离开时一模一样。",
    "How long does a switch take on a real machine?":
        "在真实的机器上，一次切换要多久？标准实验是：两个进程用两根管道连起来，把一个字节来回传。<bookmark mark='a'/>每一方都必须阻塞，直到对方回应，"
        "所以每一次往返都迫使发生两次上下文切换和四次系统调用。<bookmark mark='b'/>两个进程在同一个处理器上时，一次往返要二点九微秒。<bookmark "
        "mark='c'/>两个进程在不同处理器上时要慢得多，这里是二十五微秒，因为另一个核已经睡了，必须用处理器之间的中断唤醒，而在虚拟机上这很昂贵。"
        "<bookmark mark='d'/>而最大的代价在这个测量里往往看不见：换进来的进程发现缓存里满是另一个进程的数据，在重新填满之前都跑得很慢。<bookmark "
        "mark='e'/>所以调度器不应该比必要时切换得更频繁。必要的频率是多少，就是时间片的问题。",
    # ------------------------------------------------------------------ Fork
    "Chapter six. Fork, exec, and wait.": "第6章。创建进程：分叉、执行与等待。",
    "Unix creates processes with three calls.":
        "Unix 用三个调用创建进程。<bookmark mark='a'/>fork 把调用它的进程变成两个。父进程和子进程完全相同，内存内容相同，打开的文件也相同，只是 fork 在"
        "子进程中返回零，在父进程中返回子进程的编号。<bookmark mark='b'/>exec 把一个进程正在运行的程序换成另一个，进程本身和它打开的文件保持不变。"
        "<bookmark mark='c'/>wait 让父进程睡眠，直到某个子进程退出，然后交回它的退出码。<bookmark mark='d'/>为什么把 fork 和 exec 分开？因为在两者之间，"
        "子进程还在运行外壳的代码，它可以用普通的调用整理好自己的文件，再变成新的程序。输出重定向和管道就是这样实现的，启动程序的那个调用不需要任何特殊"
        "支持。",
    "With those three calls a shell is short.":
        "有了这三个调用，外壳就很短。这一个是二十五行 C，在这台机器上运行。<bookmark mark='a'/>它读入一行，在竖线处拆开。对每条命令它 fork 一次；子进程"
        "用 dup2 把管道接到自己的标准输入或输出上，然后 exec 那条命令。<bookmark mark='b'/>父进程关掉自己那份管道，等两个子进程结束。<bookmark "
        "mark='c'/>我们输入了 echo hello world，然后是 echo the cat sat，经管道送进 tr，它把小写转成大写。<bookmark mark='d'/>管道是内核里一个有两端的"
        "缓冲区。echo 往一端写；tr 从另一端读；谁也不知道对方存在。Doug McIlroy 在1973年把管道推进了 Unix，它改变了人们写程序的方式：小工具，连在一起。",
    "What does a new process cost?":
        "新建一个进程要多少代价？<bookmark mark='a'/>在这台机器上，一次子进程立即退出的 fork 要一百五十微秒。fork 之后 exec 一个很小的程序要大约一又四分之一"
        "毫秒，一次调用里两件事都做的 posix_spawn 也差不多。<bookmark mark='b'/>但看看父进程占用内存时会发生什么。占用一 GiB 时，fork 要三十三毫秒。"
        "<bookmark mark='c'/>fork 并不复制内存本身：它复制内存的映射表，把每一页标记为以后有人写时才复制。这个技巧属于第32部分。但映射表随内存增长。"
        "<bookmark mark='d'/>2019年，来自微软、波士顿大学和苏黎世联邦理工学院的研究者指出，fork 已不适合现代系统，新代码应当使用 spawn。<bookmark "
        "mark='e'/>PebbleOS 根本没有 fork。只有边界而没有重定位，一个进程的副本需要完全相同的地址。第32部分给每个进程自己的地址，那时 fork 才成为可能。",
    # ------------------------------------------------------------------ Scheduling
    "Chapter seven. Scheduling: first come first served":
        "第7章。调度：先来先服务、短作业优先，以及最短剩余时间优先。",
    "A scheduler decides which ready process runs next.":
        "调度器决定下一个运行哪个就绪进程。它应该优化什么？<bookmark mark='a'/>对批处理作业，是周转时间：从到达到完成。对坐在键盘前的人，是响应时间："
        "程序要多久才第一次有所动作。等待时间：一个作业就绪却没在运行的时长。吞吐量：每秒完成多少作业。还有公平。<bookmark mark='b'/>这些目标互相冲突。"
        "我们会看到，对周转时间最好的顺序会让长作业挨饿，而为了好的响应时间频繁切换会损失吞吐量。",
    "The simplest scheduler runs jobs in the order they arrive":
        "最简单的调度器按到达顺序运行作业，一直到完成：先来先服务。<bookmark mark='a'/>三个作业同时到达。A 需要一百个刻度的处理器时间，B 和 C 各需要十个。"
        "<bookmark mark='b'/>如果 A 恰好排在最前面，B 和 C 就在它后面等，像山路上跟在卡车后面的小汽车。完成时间是一百、一百一十和一百二十：平均周转时间"
        "一百一十。这就是护航效应。<bookmark mark='c'/>改为先运行短作业，它们在十和二十时完成，A 仍在一百二十时完成。平均值降到五十。",
    "Shortest first is not just better here":
        "短作业优先不只是在这里更好：对于一开始就全部在场的作业，它是最好的顺序，证明只需一次交换。<bookmark mark='a'/>取任意一个顺序，其中长度为 L 的长"
        "作业紧排在长度为 S 的短作业之前。<bookmark mark='b'/>交换它们。<bookmark mark='c'/>短作业现在早 L 完成，长作业晚 S 完成，其他每个作业的完成时间都"
        "和以前一样。<bookmark mark='d'/>所以完成时间的总和变化 S 减 L，是负数。<bookmark mark='e'/>长作业排在短作业之前的顺序总能改进，所以最好的顺序里"
        "没有这种情形：短的优先。<bookmark mark='f'/>每当有新作业到达就做同样的交换，可以证明即使作业陆续到达，最短剩余处理时间优先也是最优的。Linus "
        "Schrage 在1968年证明了这一点。",
    "Jobs do not all arrive at the start.":
        "作业并不都在开始时到达。<bookmark mark='a'/>这里 A 独自开始，B 和 C 十个刻度后到达。短作业优先从不打断正在运行的作业，所以 B 和 C 要等 A 全部"
        "做完：平均周转时间一百零三。<bookmark mark='b'/>最短剩余时间优先会抢占：B 到达时需要十个刻度，A 还需要九十个，A 就被放到一边。平均值降到五十。"
        "<bookmark mark='c'/>在八成负载下到达的四百个随机作业上，最短剩余时间优先的平均周转时间最好，只有先来先服务的一半。下一章的轮转，响应时间最好。"
        "<bookmark mark='d'/>但这一切都假定调度器知道每个作业要运行多久，而它并不知道。真实的调度器靠猜，根据每个进程最近几次运行了多久。",
    # ------------------------------------------------------------------ Mlfq
    "Chapter eight. Round robin, and the multi-level feedback queue.": "第8章。轮转，以及多级反馈队列。",
    "For people at keyboards, response time is what matters":
        "对坐在键盘前的人，要紧的是响应时间，办法是轮流来。<bookmark mark='a'/>三个各三十个刻度的作业。先来先服务要到六十个刻度后才回应第三个作业。"
        "<bookmark mark='b'/>轮转给每个作业五个刻度的时间片，然后转到下一个：每个作业都在十个刻度内开始，平均响应时间从三十降到五。<bookmark mark='c'/>"
        "但看看完成时间。每个作业都一直运行到快结束，所以平均周转时间从六十升到八十五。对等长的作业，轮转是周转时间最差的顺序。<bookmark mark='d'/>这就是 "
        "CTSS 的分时：每个时间片结束时一次定时器中断，换下一个就绪作业。",
    "How long should the quantum be?":
        "时间片应该多长？我们在那四百个随机作业上运行轮转，每次切换计一个刻度的代价。<bookmark mark='a'/>时间片为一个刻度时，处理器一半的时间花在切换上。"
        "机器实际上过载了，队列爆炸。<bookmark mark='b'/>大约十二个刻度时，响应时间最低。<bookmark mark='c'/>时间片很长时，轮转又变回先来先服务。<bookmark "
        "mark='d'/>真实的内核选几毫秒的时间片，比一次切换长一千倍，所以切换的开销不到百分之一。",
    "Shortest first needs to know the future.":
        "短作业优先需要知道未来。轮转对它视而不见。Corbató 的多级反馈队列，来自1962年的 CTSS，从行为中学到它。<bookmark mark='a'/>有好几个队列，各有一个"
        "优先级。高的队列总是先运行，同一队列内作业轮流。<bookmark mark='b'/>每个新作业从最顶层开始，那里的时间片很短。<bookmark mark='c'/>在某一层用完"
        "配额的作业会被降级：它已经表明自己会长时间连续计算。<bookmark mark='d'/>每隔一段时间，所有作业都回到顶层。我们会看到为什么。<bookmark mark='e'/>"
        "这里有两个长计算 H1 和 H2，和一个交互式作业 I，它计算一个刻度，然后等九个刻度的输入。长计算沉到底层。I 从不用完配额，留在顶层，一就绪就运行。"
        "<bookmark mark='f'/>它在三百四十一个刻度时完成，轮转下则是六百四十一，而没有人告诉调度器哪个作业是哪种。",
    "Any rule based on behaviour can be gamed.":
        "任何基于行为的规则都能被钻空子。规则四的第一个版本规定，作业只要为输入或输出让出处理器，它的配额就重置。<bookmark mark='a'/>于是一个聪明的程序"
        "计算九个刻度，象征性地读一个刻度，再接着计算，总是刚好落在十个刻度的时间片之内。<bookmark mark='b'/>它看起来永远不像长计算，留在顶层队列，占去机器"
        "的百分之八十九。把每个作业在某一层的时间按总量计算，不管它怎样拆开，就修好了：这个钻空子的程序降到百分之十七。<bookmark mark='c'/>另一个危险是"
        "饥饿。三个交互式作业让顶层队列一直忙着，底层的一个长作业在一千五百个刻度里只得到十个。<bookmark mark='d'/>规则五，定期提升到顶层，保证它每两百个"
        "刻度得到一个时间片。<bookmark mark='e'/>这个设计的各种变体调度过 Solaris 和 BSD 系统，Windows 至今仍会提升刚等待完的线程的优先级。",
    # ------------------------------------------------------------------ Share
    "Chapter nine. Proportional share": "第9章。按比例分享：彩票、步幅，以及 Linux 的完全公平调度器。",
    "Sometimes we want shares, not priorities":
        "有时我们要的是份额，而不是优先级：机器的四分之三给 A，四分之一给 B。<bookmark mark='a'/>Carl Waldspurger 和 William Weihl 在1994年提出的彩票"
        "调度，给 A 三百张彩票、B 一百张，每个时间片随机抽一张。<bookmark mark='b'/>平均而言 A 得到四分之三。但在任何一次运行中，一百二十个时间片之后，A 的"
        "份额可能是三分之二到百分之八十五之间的任何值。<bookmark mark='c'/>一年后 Waldspurger 给出了确定性的版本，步幅调度。每个作业的步幅是一个大数除以"
        "它的彩票数，每个作业还保存一个行程值。运行行程最小的作业，再把它的步幅加上去。<bookmark mark='d'/>步幅调度在每个时刻都保持恰好三比一，误差不超过"
        "一个时间片。",
    "How unfair is the lottery?":
        "彩票有多不公平？Waldspurger 的度量是：让两个等长、彩票相同的作业运行，用第一个的完成时间除以第二个的。一表示完全公平。<bookmark mark='a'/>对只有"
        "一个时间片的作业，哪个先完成都可能，两种方法的比值都是二分之一。<bookmark mark='b'/>对十个时间片的作业，彩票平均为零点八二，步幅为零点九五。"
        "<bookmark mark='c'/>随机抽取只是慢慢地拉平，误差按抽取次数平方根的倒数缩小；步幅的误差则按次数本身的倒数缩小。<bookmark mark='d'/>彩票也有别的"
        "优点：它不保存状态，客户可以把自己的彩票借给代它工作的服务器。",
    "Linux took a different road to proportional share.":
        "Linux 走了另一条通往按比例分享的路。自2007年起，它的主调度器，Ingo Molnár 的完全公平调度器，为每个任务记录一个虚拟运行时间。<bookmark "
        "mark='a'/>任务运行时虚拟运行时间增长，权重越大的任务增长越慢。<bookmark mark='b'/>调度器总是运行虚拟运行时间最小的任务，并把任务按它排在一棵"
        "红黑树里，就是第17部分的平衡树，所以选择只需对数时间。<bookmark mark='c'/>任务 a 和 b 交替。c 在第四十个刻度到达时，从最小的虚拟运行时间开始，"
        "而不是从零开始，否则它在追赶期间会独占处理器。<bookmark mark='d'/>权重来自 nice 值：每一级是一点二五倍。nice 为零的任务对 nice 为五的任务，得到"
        "百分之七十五点四，正如权重所预测。<bookmark mark='e'/>2023年，Linux 6.6 用 EEVDF 取代了它，这是1995年的一个算法，保持同样的份额，又给每个任务一个"
        "虚拟截止期限，让需要短而频繁时间片的任务及时得到它们。",
    # ------------------------------------------------------------------ Multi
    "Chapter ten. Many processors.": "第10章。多个处理器。",
    "With several processors, the first question is where the queue lives.":
        "有好几个处理器时，第一个问题是队列放在哪里。<bookmark mark='a'/>一个共享队列很简单，负载均衡得完美，但每个核取作业都要给它加锁，而且作业在恰好空闲"
        "的那个核上运行，离它留在另一个核缓存里的数据很远。<bookmark mark='b'/>所以 Linux 从2.6版起给每个核一个队列。<bookmark mark='c'/>一直待在同一个核上"
        "的作业，会发现自己的数据还在那个核的缓存里。这叫作亲和性。<bookmark mark='d'/>搬动工作很贵。在这里，在另一个核上唤醒一个作业要二十五微秒，同一个核"
        "上只要三微秒。<bookmark mark='e'/>但队列会渐渐失衡，所以内核定期搬动工作，从忙的核搬到闲的核，先试附近的核。",
    "For programs that split themselves into many small tasks":
        "对于把自己拆成许多小任务的程序，有比均衡器更好的方案。<bookmark mark='a'/>每个工作者有自己的双端任务队列，在底部压入和弹出。没活干的工作者随机挑"
        "另一个，从它队列的顶部偷一个。<bookmark mark='b'/>我们模拟了一个分叉-汇合计算，工作量八万三千个单位，关键路径七十一。<bookmark mark='c'/>Blumofe "
        "和 Leiserson 在1999年证明，工作窃取的期望完成时间是工作量除以工作者数，再加上关键路径的若干倍。<bookmark mark='d'/>模拟结果正好落在这条线上，直到"
        "六十四个工作者，它们快了六十倍，只偷了四百八十七次。<bookmark mark='e'/>偷窃之所以少，是因为队列顶部放着最老的任务，它通常也是最大的。<bookmark "
        "mark='f'/>这就是 Cilk、Java 的 fork-join 池、Go 的运行时，以及 Rust 的 Rayon 和 Tokio 里面的调度器。",
    # ------------------------------------------------------------------ RealTime
    "Chapter eleven. Real time.": "第11章。实时。",
    "In a car's brakes or an aircraft's controls":
        "在汽车制动或飞机控制中，迟到的答案就是错误答案。周期任务每隔一段时间释放一份工作，在下次释放前完成。<bookmark mark='a'/>任务一每五个刻度需要两个刻度，任务二每七个刻度需要四个刻度，总利用率约百分之九十七。<bookmark mark='b'/>速率单调调度给周期较短的任务较高固定优先级。<bookmark mark='c'/>到第七个刻度，任务二只得到三个刻度，少一个，因此错过截止期。<bookmark mark='d'/>最早截止期优先每次运行绝对截止期最近的任务，在这里能满足全部截止期。<bookmark mark='e'/>Liu 与 Layland 的定理假定任务独立、可抢占、相对截止期等于周期、单处理器，且无阻塞与调度开销。在这些条件下，EDF 在总利用率不超过一时成功。<bookmark mark='f'/>固定优先级更简单；若过载仅来自低优先级工作，高优先级任务仍受保护。若高优先级任务自己的需求已过多，它们也会错过截止期。",
    "For rate-monotonic scheduling, Liu and Layland found a simple sufficient test.":
        "对速率单调调度，Liu 与 Layland 给出了一个简单的充分条件。<bookmark mark='a'/>利用率不超过 n 乘以二的 n 分之一次方减一时，所有截止期都能满足。一项任务时界为一，两项约百分之八十三，四项约百分之七十六；项数增大后趋近 ln 二。<bookmark mark='b'/>证明的关键是同步释放的最坏情况，紧界任务集的周期处于两倍范围内。<bookmark mark='c'/>这只是充分条件。我们按目标利用率生成四项任务，再把工作量舍入为整数刻度，因此实际利用率会改变。<bookmark mark='d'/>响应时间分析计算每项任务的最坏响应，比充分利用率界接受更多样本。这些是有限采样结果，不是普遍接受率。<bookmark mark='e'/>EDF 接受的恰是实际总利用率不超过一的样本；在目标利用率接近百分之百时，舍入可使接受比例低于一。<bookmark mark='f'/>当周期彼此整除时，固定优先级能利用整个处理器。周期十、二十、四十的例子利用率为八分之七，所有响应时间都不超过周期。",
    "Days after Mars Pathfinder landed in July 1997":
        "1997年7月，火星探路者着陆几天后，它的计算机开始反复自行重启。<bookmark mark='a'/>有三个任务很关键。一个低优先级的气象任务拿到了信息总线的锁。高优先级"
        "的总线管理任务到来，等这把锁。然后一个不需要锁的中优先级通信任务抢占了气象任务，并且运行了很久。<bookmark mark='b'/>高优先级任务现在被卡在一个中优先级"
        "任务后面：优先级反转。它错过了截止期限，看门狗断定出了严重问题，重启了系统。<bookmark mark='c'/>解药是优先级继承：当一个任务持有更高优先级任务想要的"
        "锁时，它以那个更高的优先级运行。<bookmark mark='d'/>现在气象任务很快用完了锁，总线管理任务在第十三个刻度完成。<bookmark mark='e'/>喷气推进实验室的"
        "工程师在地球上的一台航天器复制品上重现了这个故障，上传了对 VxWorks 操作系统一个设置的修改，打开了继承，修好了它。",
    # ------------------------------------------------------------------ Queueing
    "Chapter twelve. Queueing theory.": "第12章。排队论。",
    "Queueing theory begins with a law so general":
        "排队论从一条普遍到几乎是同义反复的定律开始。<bookmark mark='a'/>画出到达服务器的顾客累计数，在它下面画出已离开的累计数。<bookmark mark='b'/>两条"
        "曲线之间，每一条横带是一位顾客，从到达到离开：它的宽度就是这位顾客在系统中的时间。<bookmark mark='c'/>现在按竖列读同一块面积：任何时刻，两条曲线"
        "之间的高度就是系统里的顾客数。<bookmark mark='d'/>所以所有人的时间之和，等于在场人数的积分。<bookmark mark='e'/>两边都除以时间长度。左边是单位时间"
        "的到达数乘以每人的平均停留时间；右边是系统里的平均人数。L 等于 lambda W。John Little 在1961年给出了一般性的证明：它对任何队列、任何顺序、任何分布"
        "都成立。<bookmark mark='f'/>在我们八成负载的模拟里，两边一直吻合到小数点后第三位。",
    "The simplest queue with randomness in it is called M/M/1":
        "带随机性的最简单的队列叫 M/M/1：顾客以速率 lambda 随机到达；一个服务器以速率 mu 处理他们，每个作业花的时间是随机的、服从指数分布。<bookmark "
        "mark='a'/>它的状态就是系统里的顾客数。到达以速率 lambda 把它推高一，完成以速率 mu 把它拉低一。<bookmark mark='b'/>长期来看，相邻状态之间每一道"
        "切口两侧的流量必须平衡：lambda 乘以 n 的概率，等于 mu 乘以 n 加一的概率。<bookmark mark='c'/>所以概率按比值 rho 几何递减，rho 是 lambda 除以 mu，"
        "也就是服务器忙碌的时间比例。<bookmark mark='d'/>系统里的平均人数是 rho 除以一减 rho。<bookmark mark='e'/>由利特尔法则，平均停留时间是一除以 mu 减 "
        "lambda。",
    "Plot one over one minus rho":
        "画出一除以一减 rho，即以服务时间为单位的平均响应时间。<bookmark mark='a'/>这就是曲棍球杆。圆点是我们的模拟，每个负载一百万个作业，它们就落在公式上。"
        "<bookmark mark='b'/>负载百分之五十时，一个请求花的时间是空闲机器上的两倍。<bookmark mark='c'/>百分之九十时是十倍：比百分之五十时差五倍，而服务器只"
        "多干了百分之八十的活。<bookmark mark='d'/>尾部更糟：在百分之九十的负载下，一百个请求中有一个要花四十六个服务时间，因为这个队列的响应时间本身就服从"
        "指数分布。<bookmark mark='e'/>接近百分之百时，每多一个百分点的负载都比上一个更贵，这就是为什么做容量规划的人瞄准百分之五十到七十，也是为什么一台昨天"
        "看起来还好的服务器，今天只多了一点流量就会倒下。",
    "Why so steep? Watch the number of jobs in the system over time.":
        "为什么这么陡？看系统里的作业数随时间的变化。这是一次随机游走：每次到达加一，每次完成减一，而且不能低于零。<bookmark mark='a'/>负载百分之五十时，游走"
        "被牢牢地往下拉，一阵阵到达很快就消化掉。<bookmark mark='b'/>负载百分之九十时，这股拉力很弱。一阵到达就堆起十五或二十个的队列，要很久才消化，所以大多数"
        "作业到达时都看到一群人。<bookmark mark='c'/>平均值把这一点藏起来了：队列通常要么很短、要么很长，而人们记住的正是那些很长的时段。",
    "Exponential service times are a convenient assumption.":
        "指数分布的服务时间是一个方便的假设。Felix Pollaczek 和 Aleksandr Khinchine 求出了任意服务时间分布下的平均响应时间。<bookmark mark='a'/>它通过"
        "变异系数的平方，C 平方，依赖于方差。<bookmark mark='b'/>负载百分之八十，平均服务时间为一：如果每个作业都恰好花一，平均响应是三。服务时间服从指数"
        "分布时是五。许多短作业夹着几个长作业时是二十三。<bookmark mark='c'/>同样的负载、同样的均值，波动大的服务器比稳定的慢将近八倍。<bookmark mark='d'/>"
        "少数长作业挡住了后面所有人：这是第7章的护航效应，如今写成了公式。",
    "The order of service matters as much.":
        "服务的顺序同样要紧。同样的负载、同样的作业、三种规则。<bookmark mark='a'/>处理器共享，也就是时间片极小的轮转，有一个了不起的性质：它的平均响应时间"
        "是平均大小除以一减 rho，不论大小怎样分布。方差伤不了它。<bookmark mark='b'/>最短剩余处理时间优先是最优的，由第7章的交换论证可知，Schrage 在1968年"
        "证明了这一点：对指数分布的大小，二点三六对五。<bookmark mark='c'/>对于重尾分布的大小，也就是文件、网页和数据中心作业实测的那种，先来先服务比 SRPT "
        "差十三倍。<bookmark mark='d'/>通常的担心是大作业会挨饿。Mor Harchol-Balter 和她的同事证明，在网页服务器上它们几乎不受影响，还做出了一个按这种方式"
        "调度连接的服务器。",
    # ------------------------------------------------------------------ Designs
    "Chapter thirteen. Kernel designs.": "第13章。内核的设计。",
    "How much of the operating system should run in kernel mode?":
        "操作系统有多少部分应该在内核态运行？主要有四种答案。<bookmark mark='a'/>宏内核，比如 Unix 和 Linux，把一切都放在里面：文件系统、驱动程序、网络栈、"
        "内存和调度。它们之间的调用就是普通的函数调用，这很快，但任何一个驱动程序的错误都能让整台机器崩溃。<bookmark mark='b'/>微内核只把最少的东西放在里面，"
        "进程间消息、内存和调度，把文件系统和驱动程序作为普通进程运行。崩溃的驱动程序可以重启，但现在每个请求都要付出消息和切换的代价。<bookmark mark='c'/>"
        "外核走得更远：内核只负责安全地分配硬件，每个应用程序把自己的操作系统作为库链接进来。<bookmark mark='d'/>单一内核则把一个应用程序和它所需的那部分操作"
        "系统代码链接成一个映像，直接运行在虚拟机管理程序上，那是第32部分的主题。",
    "The choice was argued in public.":
        "这个选择曾被公开辩论。1992年1月，教学系统 MINIX 的作者 Andrew Tanenbaum 发帖说 Linux 已经过时：<bookmark mark='a'/>他写道，宏内核是倒退回"
        "七十年代的一大步。<bookmark mark='b'/>Linus Torvalds 回答说，微内核在理论上也许更干净，但 Linux 现在就能用，而且很快。<bookmark mark='c'/>争论的"
        "焦点是消息的代价。Mach 的消息很慢，但 Jochen Liedtke 在 L4 内核中证明，围绕消息设计内核，进程间的消息可以快一个数量级。<bookmark mark='d'/>规模"
        "说明了一切。PebbleOS 是两百八十四条指令。seL4 是 L4 家族中的一个微内核，大约八千七百行 C，在2009年成为第一个有机器检查过的证明、证明它确实按规格"
        "行事的通用内核。Linux 有三千多万行，大部分是驱动程序。<bookmark mark='e'/>实践中，胜出者都是混合的：macOS 是 Mach 微内核与 BSD Unix 的融合，汽车里"
        "跑着 QNX 微内核，Linux 则把驱动程序作为模块加载。",
    # ------------------------------------------------------------------ PebbleOS
    "Chapter fourteen. PebbleOS runs the Job.": "第14章。PebbleOS 运行那项任务。",
    "Now PebbleOS runs the Job, and the Job becomes two processes":
        "现在 PebbleOS 来运行那项任务，任务变成两个用管道连起来的进程，就像 Unix 用户会写的那样。<bookmark mark='a'/>第一个进程 tok 从纸带读入文本，每行"
        "写出一个小写单词。它是用我们自己的语言写的十八行。<bookmark mark='b'/>第二个是 job，第17部分的哈希表程序，一字未改。它从管道读入单词，就像那是小说"
        "本身，并打印出同样的二十行。<bookmark mark='c'/>两者都由第13部分的编译器编译，只有一处改变：getc 和 putc 变成对那个小库的调用，它与内核一次交换"
        "四 KiB。<bookmark mark='d'/>内核搬运字节，阻塞必须等待的那一端，每两万条指令抢占一次每个进程。",
    "Here is a short passage of seven thousand bytes going through.":
        "这是一段七千字节的短文在流过。<bookmark mark='a'/>上面的图显示谁占着处理器：tok 是蓝色，job 是黄色，它们之间的内核是橙色。<bookmark mark='b'/>"
        "下面是管道里等待的字节数。tok 按四 KiB 一阵地写，管道被填满；job 读，管道被排空。<bookmark mark='c'/>十五次上下文切换，三十八次定时器中断，十来次"
        "系统调用，还有一次 job 不得不等一个空管道。<bookmark mark='d'/>两个程序都不知道对方存在，也不知道自己被打断了。<bookmark mark='e'/>输出与任务的"
        "二十行逐字节相同，在全部三十二段测试文本上都是如此。",
    "What does all this cost?":
        "这一切要多少代价？我们在三十二段文本上运行这条流水线，数出每一个进程和内核里的每一条指令，然后拟合这些计数，推算到全部三十部小说。<bookmark "
        "mark='a'/>每个文本字节：tok 里三十四条指令，job 里五十条，内核里二十三条。一共一百零七条。<bookmark mark='b'/>第17部分的裸程序需要三十九条。"
        "<bookmark mark='c'/>内核那一份几乎全是复制，一次一个字节：从纸带复制到 tok，从 tok 复制到管道，从管道复制到 job。<bookmark mark='d'/>tok 是单个"
        "程序从来不用做的额外工作，而 job 每字节多付十一条指令，因为现在每次 getc 都是一次函数调用。<bookmark mark='e'/>在 PebbleOS 下单独运行时，job 需要"
        "它裸运行时指令数的一点四四倍。<bookmark mark='f'/>拟合的计数与拟合时留出的文本吻合，误差约在百分之二以内。<bookmark mark='g'/>这里的代价是复制，"
        "后面的部分会消除它：第32部分让进程共享页面，第34部分让数据移动时不必由处理器碰每一个字节。",
    "So the ledger gets row eleven.":
        "于是账本得到了第十一行。<bookmark mark='a'/>二十六点七亿条指令，在第8部分的乱序核心上，按与第八行相同的速率、相同的内存停顿计价，每次陷入和每次返回"
        "再加三十五个周期的流水线排空。<bookmark mark='b'/>二点一七秒，裸程序是零点八一秒：慢了二点七倍。像第15部分那一行带垃圾回收的结果一样，它退步了，这是"
        "诚实的结果。<bookmark mark='c'/>操作系统不会让一个程序变快。它让许多程序彼此安全，让它们共享机器，并让两个彼此一无所知的程序像一个程序那样协作。让这"
        "变得便宜，是接下来三个部分的工作。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fifteen. The frontier": "第15章。前沿：经过验证的内核，以及微秒级的调度。",
    "The kernel is the one program everything else trusts":
        "内核是其他一切都信任的那个程序，所以证明在这里回报最大。<bookmark mark='a'/>2009年，悉尼 NICTA 的一个团队证明了 seL4，一个八千七百行 C 的微内核，"
        "精确地实现了它的形式化规格：它不会崩溃、不会缓冲区溢出、不会解引用坏指针。后来的工作把证明一直推到机器码，并证明了 seL4 让进程的数据既完整又保密。"
        "<bookmark mark='b'/>2016年的 CertiKOS 验证了一个同时在多个核上运行的内核。2017年的 Hyperkernel 让验证变成一键式的，用 SMT 求解器自动检查每个系统"
        "调用。<bookmark mark='c'/>代价是障碍。seL4 的证明大约二十万行，约二十人年的工作。<bookmark mark='d'/>即便如此，它已经在一架自主直升机上飞过，那是 "
        "DARPA 的一个项目，专业攻击者都没能攻进去。<bookmark mark='e'/>悬而未决的问题是：验证一个有 Linux 的速度和功能的内核，而证明的工作量增长不快于代码。",
    "The second frontier is speed.":
        "第二个前沿是速度。数据中心的服务可能在半微秒内回应请求，而它的用户在意的是千分之一最慢的那个。<bookmark mark='a'/>我们模拟了十六个核，服务一种类似"
        "键值存储的混合负载：几乎所有请求都花半微秒，每两百个里有一个是花五百微秒的扫描。<bookmark mark='b'/>每个核一个队列，网卡通常就是这样分发请求的，落在"
        "扫描后面的短请求就得等它：负载百分之七十时，第九十九点九百分位是四千微秒。<bookmark mark='c'/>一个共享队列好得多，但当十六个核恰好都在忙着扫描时，"
        "短请求还是要等。<bookmark mark='d'/>每五微秒抢占一次，即使每次抢占损失一微秒，也能把它降到十。<bookmark mark='e'/>这正是2019年的 Shinjuku 系统所做"
        "的，它借助虚拟化硬件的技巧，才能那么快地打断一个核。相比之下，Linux 的定时器每一到四毫秒才响一次。",
    "How short should the quantum be?":
        "时间片应该多短？<bookmark mark='a'/>太长，短请求就要排在扫描后面。<bookmark mark='b'/>太短，抢占的代价就吃掉了核。时间片为一微秒时，扫描花在被抢占上的"
        "时间和运行的时间一样多，机器过载，一次扫描要七点五毫秒。<bookmark mark='c'/>这里最好的时间片大约是两微秒。<bookmark mark='d'/>但没有公式告诉我们这一点。"
        "即使是多服务器、一般作业大小的队列，连平均响应时间都没有精确的闭式解，所以这些选择只能靠模拟和尝试。",
    "The third frontier changes what a kernel is.":
        "第三个前沿改变了内核是什么。eBPF 让普通用户把小程序装进正在运行的 Linux 内核。<bookmark mark='a'/>统计系统调用、过滤网络包、执行安全策略。<bookmark "
        "mark='b'/>运行任何东西之前，内核的验证器检查程序的每条路径都会结束，每次内存访问都在界内：第25部分的停机问题，靠只允许简单到可以检查的程序而避开。"
        "<bookmark mark='c'/>然后即时编译器把它变成机器码，每当它的事件发生，内核就运行它。<bookmark mark='d'/>它如今用来跟踪生产系统，为大型网站转发数据包。"
        "<bookmark mark='e'/>但验证器和编译器本身就是复杂的代码，它们的错误已经变成了接管内核的途径。<bookmark mark='f'/>所以研究者在验证验证器：PREVAIL 用"
        "抽象解释，Jitterbug 证明即时编译器正确，Agni 用机器检查验证器对取值范围的算术。",
    "Six open problems.":
        "六个悬而未决的问题。<bookmark mark='a'/>经过验证的内核能否有 Linux 的性能和广度。<bookmark mark='b'/>多服务器、一般作业大小的队列的精确响应时间，"
        "排队论至今还没有。<bookmark mark='c'/>当每次抢占都要花时间时，多核上针对尾延迟的最佳调度。<bookmark mark='d'/>多核芯片上的最坏情况时序，一个核的内存"
        "流量会拖慢另一个，这正是多核处理器难以用于安全攸关系统的原因。<bookmark mark='e'/>eBPF 验证器能接受多少程序，同时仍然可靠而快速。<bookmark "
        "mark='f'/>以及一个不知道作业大小的调度器，能多接近最短剩余时间优先；Mor Harchol-Balter 的小组用 Gittins 指数取得了进展。<bookmark mark='g'/>本部分"
        "的研究问题，取第三个问题的一个小的、可计算的情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭建了什么。分时，从 CTSS 到 Linux。给 Pebble 的模式位、陷阱和定时器，以及一个使用它们的内核。进程、上下文切换，还有 fork、exec 和一个"
        "外壳，都在这台机器上测量过。调度器，从先来先服务到多级反馈队列、彩票、步幅和 Linux 自己的那一个，外加短作业优先最优的证明。速率单调和最早截止期优先，"
        "以及火星上的一个错误。还有排队论：利特尔法则、曲棍球杆，以及为什么方差和顺序都很重要。",
    "Where this comes back.":
        "它们会在哪里再出现。第32部分给每个进程自己的地址，让 fork 变便宜，也让一台机器能假装成好几台。第33部分处理抢占带来的竞争。第34部分给 PebbleOS 加上"
        "磁盘、它的中断和一个文件系统。第40部分把利特尔法则用于在制品，第43部分用于服务之间的队列。第45和第50部分用排队论规划容量，用 eBPF 找出时间花在哪里。",
    "In practice. Before optimising, count the system calls":
        "在实践中。优化之前，先用 strace、perf 或 bpftrace 数一数系统调用。把它们成批处理，用大缓冲区或 Linux 的 io_uring，让 vDSO 来回答时钟。在大程序里"
        "优先用 posix_spawn 而不是 fork，把对延迟敏感的线程绑定到核上。记住 nice 值和控制组权重不过是公平调度器里的份额。规划服务器时让它运行在百分之五十到七十，"
        "盯住第九十九百分位，而不是平均值。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在本部分的笔记里。可以在任何一道上暂停。第五道是动手题：给 PebbleOS 一个 sleep 调用和一个步幅调度器。最后一道标着星号，是研究问题："
        "当抢占要花时间时，时间片应该多短，前沿那一章的微秒级调度器都是靠尝试来定的。",
    "Next time, Part 32: Virtual Memory.":
        "下一次，第32部分：虚拟内存。每个进程都以为自己拥有一大块私有的、连续的内存，而没有一个是真的。页表、让它们变快的地址转换缓存，以及缺页；内存满了时把"
        "哪一页扔出去，以及更多内存反而可能带来更多缺页的意外；还有建在它们之上的虚拟机和容器。PebbleOS 将得到一个内存管理单元。第32部分，虚拟内存。",
    "The books and papers this part follows are on screen and in the notes.":
        "本部分所依据的书和论文，都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
