"""Chinese narration for cs43: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第43部分：API 与服务"

CHAPTERS = {
    "Hook": "八条谬误，与拆成三块的那项任务",
    "Rpc": "1. 跨越网络的调用",
    "Wire": "2. 线上的字节",
    "Schemas": "3. 会演化的模式",
    "Styles": "4. API 风格",
    "Delivery": "5. 至多一次、至少一次、恰好一次",
    "Design": "6. API 的设计与版本",
    "Queues": "7. 队列与发布/订阅",
    "Backpressure": "8. 背压",
    "Micro": "9. 单体与微服务",
    "Data": "10. 跨服务的数据",
    "Mesh": "11. 发现、路由与信任服务",
    "Time": "12. API 中的时间",
    "Job": "13. 拆成三个服务的那项任务",
    "Frontier": "14. 前沿：可以证明的服务",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "In the nineties, engineers at Sun Microsystems wrote down":
        "20世纪90年代，Sun Microsystems 的工程师们写下了一组假设：刚接触网络的程序员往往会这样假设，而它们都是错的。<bookmark mark='a'/>网络是可靠的。"
        "延迟为零。带宽是无限的。网络是安全的。拓扑不会改变。只有一个管理员。传输成本为零。网络是同构的。<bookmark mark='b'/>1994年，Peter Deutsch 在 Bill Joy 和 Tom Lyon "
        "更早的一份清单的基础上，写下了其中7条，James Gosling 又加上了第8条。每一条都很诱人，因为远程调用看起来和本地调用一模一样。<bookmark mark='c'/>而每一条，都曾让真实的系统垮掉。",
    "Three examples. <bookmark mark='a'/> In October 2018, GitHub":
        "举三个例子。<bookmark mark='a'/>2018年10月，GitHub 的两个数据中心之间断开了43秒。它的数据库跨越整个国家做了故障转移，写入落到了两边，网站在降级状态下运行了大约一天，工程师们才把两边的数"
        "据调和一致。网络并不可靠。<bookmark mark='b'/>2016年10月，一个由被入侵的摄像头和家用路由器组成的僵尸网络，名叫 Mirai，用流量淹没了 DNS 服务商 Dyn，网上许多最大的网站有好几个小时无"
        "法访问。网络并不安全。<bookmark mark='c'/>而在2021年10月，一条例行命令撤回了 Facebook 骨干网的路由。它的 DNS 服务器看不到骨干网，就让自己下线了，而工程师修复故障所需的工具，也在同"
        "一个网络后面。拓扑会改变，有时是一下子全变。",
    'f"Here is this part\'s experiment. <bookmark':
        "这是这一部分的实验。<bookmark mark='a'/>我们把那项任务拆成三个服务：一个给文本分词，一个统计词数，一个给词排名。分词服务把它的计数分成{w['chunks']}条消息发给计数服务，而所经过的网络会丢失"
        "5%的消息，并重复2%。<bookmark mark='b'/>为了应对丢失，分词服务会一直重试，直到计数服务确认。但一条被重试的消息也许其实已经到了，而一条被重复的消息会到两次。"
        "<bookmark mark='c'/>没有保护的话，计数就会往上漂：词 the 被数了{dict(wo['top'])['the']:,}次，而不是{dict(wo['true_top'])['the']:,}次，"
        "{wo['distinct']:,}个不同的词里，有{wo['wrong_counts']:,}个数错了。<bookmark mark='d'/>加上一个想法，给每条消息一个幂等键，每个计数就都准确无误。"
        "这一部分的大多数内容，讲的就是这种分量的想法，以及证明它们行得通的数学。",
    "This is Part 43 of Computer Science, Built, the fourth part":
        "这是计算机科学，从零搭建，第43部分，也是第八幕的第四部分。<bookmark mark='a'/>我们会看到，为什么远程调用永远不能做得和本地调用一模一样；推导出 Protocol Buffers 放到线上的字节，以及"
        "安全地修改模式的规则；比较各种 API 风格；证明恰好一次投递就是至少一次投递加上去重；并观察队列、重试、发件箱和 Saga，如何在网络出状况时，让一个由服务组成的系统保持正确。",
    # ------------------------------------------------------------------ s02_rpc
    "Chapter one. Calls across a network.":
        "第一章：跨越网络的调用。",
    "In 1984 Andrew Birrell and Bruce Nelson, at Xerox PARC,":
        "1984年，Xerox PARC 的 Andrew Birrell 和 Bruce Nelson 描述了如何让对另一台机器上某个过程的调用，看起来就像一次普通的调用。<bookmark mark='a'/>调用者调用一个"
        "本地过程，即客户端存根，名字和参数都一样。<bookmark mark='b'/>存根把参数编组成字节，运行时系统把它们发送到网络另一端。<bookmark mark='c'/>在服务器上，一个对应的存根把字节解组，再分"
        "派给真正的过程。<bookmark mark='d'/>结果沿同样的路径返回，调用者看到的只是一个返回值。存根由一个叫 Lupine 的程序生成。",
    "In 1994 Jim Waldo, Geoff Wyant, Ann Wollrath and Sam":
        "1994年，Sun 的 Jim Waldo、Geoff Wyant、Ann Wollrath 和 Sam Kendall 写了《关于分布式计算的一则笔记》（A Note on Distributed Computing）"
        "，论证这种假象无法维持。他们给出了四条理由。第一条是延迟。<bookmark mark='a'/>一次本地调用只花几纳秒。<bookmark mark='b'/>一次远程调用，在这一部分的延迟模型里，中位数大约10毫秒，"
        "第99百分位是30毫秒：<bookmark mark='c'/>多出六到七个数量级。<bookmark mark='d'/>一千次本地调用毫无察觉；一千次远程调用要花10秒。远程接口需要的是调用次数少，每次做很多事。",
    "The second reason is memory. <bookmark mark='a'/> Here the":
        "第二条理由是内存。<bookmark mark='a'/>这里，调用者把同一个对象传了两次，分别作为 a 和 b。在本地，这是同一个地址，传了两次。<bookmark mark='b'/>但地址只在一个进程内部才有意义，"
        "这是第32部分的教训，所以存根会复制它指向的内容，服务器收到的是两个各自独立的对象。<bookmark mark='c'/>服务器给其中一个加一时，另一个不变，调用者的原件也不变。"
        "<bookmark mark='d'/>第三条理由是并发：服务器同时运行许多客户端的调用，所以每个调用者都成了一个并发程序的一部分，带着第33部分讲过的所有隐患。",
    "The fourth reason is the deepest: partial failure. A single":
        "第四条理由最深刻：部分失败。一台计算机要么正常工作，要么不工作；而分布式系统可以坏掉一半。客户端发出一个请求，没有回复，它的超时触发了。发生了什么？<bookmark mark='a'/>也许请求丢了，调用根本没有执行。"
        "<bookmark mark='b'/>也许服务器做完了工作，然后在回复之前崩溃了。<bookmark mark='c'/>也许它回复了，而回复丢了。<bookmark mark='d'/>从客户端看，这三种情况一模一样"
        "：一片沉默。重试的话，后两种情况会让调用执行两次：对一次读取无伤大雅，对一笔付款却是灾难。",
    "Could a cleverer protocol remove the doubt? Part 38 proved":
        "更聪明的协议能消除这种不确定吗？第38部分证明了不能。<bookmark mark='a'/>客户端说：去做；服务器说：做完了；但服务器无法知道它的“做完了”有没有送到，于是客户端发一个确认，而这个确认本身也需要一个确认"
        "。<bookmark mark='b'/>取一个据称可行的最短交换。它的最后一条消息可能丢失，所以发送者不能依赖它，那么一个更短的交换也同样可行。不存在最短的交换。<bookmark mark='c'/>所以，一个 RP"
        "C 系统要么让调用至多执行一次，从不重试；要么至少执行一次，一直重试，直到得到回答。<bookmark mark='d'/>恰好一次，必须构建在调用本身之中。",
    "What survived from Birrell and Nelson is the stub generator.":
        "Birrell 和 Nelson 的工作中流传下来的，是存根生成器。<bookmark mark='a'/>接口只写一次，用一种接口描述语言来写：这里是一个只有一个调用的服务，以及它的消息。"
        "<bookmark mark='b'/>生成器写出存根，用双方各自使用的任何语言。<bookmark mark='c'/>这个想法从承载 NFS 文件系统的 Sun RPC 开始，经过 CORBA 和 Facebook "
        "的 Thrift，一直延续到 Google 的 gRPC。<bookmark mark='d'/>变了的是诚实。一次 gRPC 调用要带一个截止时间，并返回一个状态，比如超过截止时间（deadline exceeded）"
        "或不可用（unavailable）：它看起来像本地调用，但承认网络的存在。",
    # ------------------------------------------------------------------ s03_wire
    "Chapter two. Bytes on the wire.":
        "第二章：线上的字节。",
    "Start with the most common format of all. JSON writes":
        "从最常见的格式说起。JSON 把数字写成十进制文本，对精度只字不提，但 JavaScript 把每个数字都读成双精度数，也就是第4部分讲的64位浮点数，有53位有效位。<bookmark mark='a'/>在2的53次"
        "方以内，每个整数都是精确的；超过它，相邻的双精度数相差2。<bookmark mark='b'/>所以2的53次方加1，到达时变成了2的53次方：它正好在中间，于是舍入到偶数的那个邻居。"
        "<bookmark mark='c'/>19位的 id 更糟。在百亿亿附近，相邻的双精度数相差256，最后几位数字就变了。<bookmark mark='d'/>所以 API 把大的 id 当作字符串发送，而 JSON "
        "标准也警告说，更大的整数可能无法完好保留。",
    "Protocol Buffers, which Google open-sourced in 2008, write":
        "Protocol Buffers 由 Google 在2008年开源，它用另一种方式写整数：变长整数（varint）。<bookmark mark='a'/>拿150来说。它的二进制需要8位。"
        "<bookmark mark='b'/>从低位开始，把它们切成每组7位。<bookmark mark='c'/>先写低位的那组，并给每个字节一个最高位，说明后面是否还跟着一个字节："
        "第一个字节是1，最后一个字节是0。<bookmark mark='d'/>用十六进制写，就是九六、零一，正是编码指南给出的字节。<bookmark mark='e'/>所以小的数只占1个字节，每多7位就多1个字节，而最大"
        "的64位值需要10个字节。",
    "A message is a sequence of fields, and each field begins":
        "一条消息是一串字段，每个字段以一个标签开头。<bookmark mark='a'/>标签是字段编号左移三位，再并上一个线路类型：0 表示变长整数，1 和 5 分别表示8个和4个固定字节，2 表示任何带长度的东西。"
        "<bookmark mark='b'/>所以存放一个变长整数的字段1，标签是零八，而消息 a 等于150，就是零八、九六、零一。<bookmark mark='c'/>字符串是线路类型2："
        "字段2给出标签一二，然后是长度7，然后是单词 testing 的7个字节。<bookmark mark='d'/>嵌套消息和打包列表也都是按长度分隔的。我们的编码器逐字节地重现了指南里的每一个例子。",
    "Negative numbers expose a flaw. <bookmark mark='a'/> In":
        "负数暴露出一个缺陷。<bookmark mark='a'/>在补码里，负2的最高位是1，所以作为变长整数，64位全都得发送，要占10个字节。<bookmark mark='b'/>sint 类型用之字形编码（zigzag"
        "）解决这个问题，它把正负数交错排列。0 变成 0，负1变成1，1变成2，负2变成3。<bookmark mark='c'/>写成代码，就是左移一位，再与铺满整个字的符号位做异或。我们的版本与指南的表格一致，连极端值也一样"
        "。<bookmark mark='d'/>现在负2就是单个字节零三，正负两边的小数都保持很小：负1000只占2个字节，而不是10个。",
    'f"Put it together on one record: an id, a word, its':
        "把这些放到一条记录上：一个 id、一个词、它的计数、它所在的小说、一个分数和三个标记。<bookmark mark='a'/>写成紧凑的 JSON，它是{c['json_bytes']}个字节。"
        "<bookmark mark='b'/>写成 Protocol Buffers，它是{c['proto_bytes']}个，分数用之字形编码的 sint，标记用打包列表。<bookmark mark='c'/>节省主要来"
        "自名字：JSON 在每条记录里重复每个字段名，并把数字写成十进制文本，而 protobuf 发送的是一个字节的标签和一个变长整数。<bookmark mark='d'/>代价是，没有模式，这些字节就毫无意义："
        "零八说的是字段1，而不是 id。双方必须就模式达成一致，并在它变化时一直保持一致：这是下一章的内容。",
    # ------------------------------------------------------------------ s04_schemas
    "Chapter three. Schemas that evolve.":
        "第三章：会演化的模式。",
    "A schema is never changed everywhere at once. <bookmark":
        "模式从来不会在所有地方同时改变。<bookmark mark='a'/>服务器是一次升级几台的，即滚动部署，所以有一段时间，新旧代码并肩运行，互相发送消息。<bookmark mark='b'/>而且数据比代码活得久："
        "数据库或日志，第46部分会讲到，里面存着多年前写入的字节。<bookmark mark='c'/>所以一项修改必须向后兼容：新代码能读旧数据。<bookmark mark='d'/>而且通常它还必须向前兼容："
        "还没升级的旧代码，能读新代码写的东西。",
    "Part 14 has the answer. <bookmark mark='a'/> New code writes":
        "第14部分给出了答案。<bookmark mark='a'/>新代码写了一条有三个字段的记录；旧代码只期望两个。<bookmark mark='b'/>读取方按编号匹配字段：word 和 count 都在，类型也符合期望"
        "。<bookmark mark='c'/>novel 不认识，所以被跳过，不过 protobuf 会保留它的字节，以便转发。<bookmark mark='d'/>这就是宽度子类型："
        "字段更多的记录，可以放到任何期望字段更少的地方。当读取方要求的每个字段都在，而且类型兼容时，它就接受写入方的记录。<bookmark mark='e'/>反过来，一个要求 novel 的读取方，会拒绝每一条旧记录。",
    "Our checker applies that rule both ways to seven changes of":
        "我们的检查器把这条规则双向应用到一个小模式的七种修改上：一个必需的 word，字段1，和一个可选的 count，字段2。<bookmark mark='a'/>增加或删除一个可选字段，两个方向都安全。"
        "<bookmark mark='b'/>增加一个必需字段会破坏向后兼容：旧数据里从来没有它。删除一个必需字段会破坏向前兼容：旧的读取方仍然要求它。<bookmark mark='c'/>改变类型，两个方向都会破坏。"
        "<bookmark mark='d'/>把32位整数加宽到64位能通过，因为两者都是变长整数，不过旧的读取方会截断那些再也装不下的值。<bookmark mark='e'/>而给字段重新编号，两个方向都能通过。"
        "这个结论是错的。",
    "Here is why. <bookmark mark='a'/> Old code writes the count,":
        "原因在这里。<bookmark mark='a'/>旧代码把计数1226写成字段2：标签一零，然后是一个变长整数。<bookmark mark='b'/>新代码期望计数在字段5里。"
        "<bookmark mark='c'/>对它来说，字段2不认识，被跳过，而字段5不存在，所以计数读成了0。什么都没有报错；每个计数都悄无声息地丢了。<bookmark mark='d'/>真正的规则是："
        "字段的编号就是它的身份。永远不要改它，永远不要复用它，并且为删除的字段保留（reserve）它的编号和名字。<bookmark mark='e'/>而因为必需字段永远无法安全地增加或删除，proto3 干脆去掉了必需字段"
        "。",
    "Apache Avro, from the Hadoop project in 2009, makes a":
        "Apache Avro 来自2009年的 Hadoop 项目，它做了不同的取舍。<bookmark mark='a'/>它的字节里不带标签，也不带名字，只有按写入方顺序排列的值，整数用之字形编码的变长整数。"
        "<bookmark mark='b'/>所以读取方还需要写入方的模式，来自文件头，或者模式注册表。<bookmark mark='c'/>它对两个模式进行协调，按名字匹配字段。<bookmark mark='d'/>写入"
        "方缺少的字段，取读取方的默认值；读取方缺少的字段，被跳过。这是同一个子类型问题，只不过针对的是整个模式，而在这里，危险的修改是重命名。",
    "One cost is left. <bookmark mark='a'/> To read one field of":
        "还剩一项代价。<bookmark mark='a'/>要读取 protobuf 消息的一个字段，读取方得从头遍历标签，边走边解码。<bookmark mark='b'/>零拷贝格式按程序使用数据的方式来排布字节。"
        "一张偏移量表说明每个字段在哪里，<bookmark mark='c'/>所以读取计数只需一次加法和一次取数，直接从收到的缓冲区里取。<bookmark mark='d'/>Google 的 FlatBuffers，以及 "
        "Kenton Varda 的 Cap'n Proto，都是这样工作的；Varda 曾主持 Protocol Buffers 的第二版。<bookmark mark='e'/>代价是消息更大、带填充，而且陌生人发来的缓冲区"
        "，在沿着它的偏移量访问之前，必须先验证。",
    # ------------------------------------------------------------------ s05_styles
    "Chapter four. API styles.":
        "第四章：API 风格。",
    "Roy Fielding, one of the authors of HTTP's specification,":
        "Roy Fielding 是 HTTP 规范的作者之一，他在2000年的博士论文里，为 Web 的体系结构起了名字：表述性状态转移，即 REST。<bookmark mark='a'/>服务器知道的每样东西，都是一个有名"
        "字的资源，名字是一个 URL，比如编号42的书。<bookmark mark='b'/>客户端收到的只是它的一个表述，这里用 JSON，其中链接到其他资源，比如这本书的作者。<bookmark mark='c'/>每个资"
        "源都响应同样的几种方法，所以缓存或代理能理解任何请求。<bookmark mark='d'/>而且每个请求都是无状态的：它带着回答它所需的一切，所以任何副本都能回复。",
    "RFC 9110, the definition of HTTP's semantics published in":
        "RFC 9110 是2022年发布的 HTTP 语义定义，它按两个性质给方法分类。<bookmark mark='a'/>安全的方法完全不要求任何改变：GET、HEAD 和 OPTIONS 只读。"
        "<bookmark mark='b'/>幂等的方法可以改变东西，但发送两次和发送一次的预期效果相同：PUT 替换一个资源，DELETE 删除它，不管重复多少次都一样。POST 两者都不是，PATCH 也不一定是。"
        "<bookmark mark='c'/>正是这一点让重试变得安全。请求超时的客户端，无法知道请求是否已被执行。重复 PUT，购物车仍是预期的样子。<bookmark mark='d'/>重复 POST，则可能下出第二个订"
        "单：这是下一章的问题。",
    'f"Long lists come in pages, and there are two ways':
        "长列表是分页给出的，请求下一页有两种方式。<bookmark mark='a'/>用偏移量，客户端说：跳过我已有的行，再给我4行。这个信息流的第一页是第20行到第17行。<bookmark mark='b'/>现在顶部来"
        "了2条新行，所有行都往下移，跳过4行就落到了已经看过的行上。<bookmark mark='c'/>游标则说：给我比我看到的最后一行更旧的行。它不会重复。<bookmark mark='d'/>我们在1000行上、每页5"
        "0行，测量了这两种方式。每页新增3行时，偏移量重复了{r3['offset']['duplicates']}行；新增10行时，重复了{r10['offset']['duplicates']}行。"
        "游标一行也不重复。<bookmark mark='e'/>而且由于数据库要逐一走过每一个被跳过的行，即使没有插入，偏移量也要扫描10500行；游标只读取它返回的那1000行。",
    "Google's gRPC, open-sourced in 2015 from its internal system":
        "Google 的 gRPC 于2015年开源，源自它的内部系统 Stubby，它把 API 看作一组有类型的过程。<bookmark mark='a'/>服务在一个 protocol buffers 文件里声明，所以消息"
        "以第二章的紧凑二进制格式传输，并且为每种语言都生成存根。<bookmark mark='b'/>调用跑在 HTTP/2 上，一条连接上同时进行许多调用，每个调用都带一个截止时间。<bookmark mark='c'/>而"
        "且一次调用不必是一个请求加一个回复：服务器可以流式发送回复，客户端可以流式发送请求，两者也可以同时流式发送。",
    'f"GraphQL, released by Facebook in 2015, puts the':
        "GraphQL 由 Facebook 在2015年发布，它让客户端来决定形状。<bookmark mark='a'/>一个查询列出它想要的字段，想嵌套多深就嵌套多深，而响应恰好就是那个形状，取书不需要第二次往返。"
        "<bookmark mark='b'/>服务器为每个字段用一个解析器（resolver）来填充，而显而易见的解析器暗藏一个陷阱。一个查询取回50位作者；然后每位作者的 books 解析器，各自运行一次查询。"
        "这就是{n['naive']}次查询，即 N 加 1 问题；再加上每本书的评论，就是{n['nested_naive']}次。<bookmark mark='c'/>解决办法是批处理，按 Facebook 的 DataL"
        "oader 的风格：把一个时间片（tick）里请求的所有键收集起来，一起取回。{n['naive']}次查询变成{n['batched']}次，{n['nested_naive']}次变成"
        "{n['nested_batched']}次。<bookmark mark='d'/>而由于客户端可以写任意查询，公开的服务器会用持久化查询和开销上限来保护自己。",
    # ------------------------------------------------------------------ s06_delivery
    "Chapter five. At most, at least, exactly once.":
        "第五章：至多一次、至少一次、恰好一次。",
    "A sender can promise one of three things about how often a":
        "关于一条消息生效多少次，发送者可以做出三种承诺之一。<bookmark mark='a'/>至多一次：发送一次，从不重试。什么都不会重复，但丢了的消息就没了。<bookmark mark='b'/>至少一次："
        "一直重试，直到得到确认。什么都不会丢，但如果确认丢了，重试会让这次加一被执行两次。<bookmark mark='c'/>恰好一次：一直重试，直到得到确认，并让接收者记住它执行过的每条消息的标识符，遇到重复就跳过，但仍然"
        "再确认一次。",
    "We ran all three on one simulated network: ten thousand":
        "我们在同一个模拟网络上运行了这三种方式：10000次加一，消息丢失5%，确认也算在内，重复2%。<bookmark mark='a'/>至多一次数出9694：丢了306次。<bookmark mark='b'/>至少一次"
        "数出10754：多了754次。<bookmark mark='c'/>恰好一次数出10000，分毫不差。<bookmark mark='d'/>而且它在线上没有任何额外开销：同样的消息，同样的四轮重试，和至少一次一样。"
        "全部差别就在于一个标识符集合。",
    "A simulation samples executions; a model checker visits all":
        "模拟只是对执行过程抽样；模型检验器会访问所有的执行。<bookmark mark='a'/>我们的模型：两次加一，每次最多发送三次，直到得到确认，网络可以丢弃任何消息或确认，可以重复一条消息，也可以按任意顺序投递。"
        "广度优先搜索访问每一个可达状态。<bookmark mark='b'/>有去重时，共有4319个状态，其中没有一个状态的计数器超过2；只要两次加一都得到了确认，它就恰好是2。<bookmark mark='c'/>没有去"
        "重时，共有9579个状态，离起点6步就有一个违例。<bookmark mark='d'/>麻烦在于规模：每多一次加一，状态数大约要乘以20。",
    "Because the search is breadth-first, the violation it found":
        "因为搜索是广度优先的，它找到的违例是一条最短的违例。<bookmark mark='a'/>发送者发出0号加一；它的定时器在任何确认可能到达之前就触发了，于是它再发一次，然后第三次。"
        "<bookmark mark='b'/>网络把三份副本全部投递，而计数器不记任何标识符，就加了3。<bookmark mark='c'/>没有任何东西丢失，也没有凭空捏造：一个慢的网络加一个急躁的定时器，就足够了。"
        "有了去重，后两次投递就不会改变任何东西。",
    "A model checker covers one small case; a proof covers them":
        "模型检验器只覆盖一个小的情形；证明则覆盖所有情形。<bookmark mark='a'/>假设发送者重发每条消息，直到它被确认，接收者确认每一份副本，但每个标识符至多执行一次，并且网络是公平的："
        "一条被发送无穷多次的消息，终将被投递。那么每条消息都恰好被执行一次。<bookmark mark='b'/>绝不会两次：一个标识符只有在还不在接收者的集合里时才会被执行，并在同一步里加入集合。"
        "<bookmark mark='c'/>绝不会零次：确认只在一份副本到达之后才会发送，所以被确认的消息已经执行过了，而未被确认的消息会一直重发，直到公平性把它送达。<bookmark mark='d'/>而如果确认也是公"
        "平的，发送者就会停下来。<bookmark mark='e'/>我们的有界模型，检验的则是这个结论的条件形式。",
    "Payment APIs make this part of their interface. <bookmark":
        "支付 API 把这一点做成了接口的一部分。<bookmark mark='a'/>客户端为它打算进行的每一项操作，选一个新的随机键，随请求一起发送。服务器从卡上扣款，并把这个键和结果一起存下，在同一个事务里完成。"
        "<bookmark mark='b'/>响应丢了，于是客户端用同一个键重试，<bookmark mark='c'/>服务器返回存下的结果，而不是再扣一次款。<bookmark mark='d'/>第38部分的两位将军表明"
        "，客户端永远无法确定它的消息已经到达：恰好一次投递是不可能的。<bookmark mark='e'/>但恰好一次处理只需要至少一次投递，再加上一个会记住的接收者，而这一点我们刚刚证明了。",
    # ------------------------------------------------------------------ s07_design
    "Chapter six. Designing and versioning APIs.":
        "第六章：API 的设计与版本。",
    "Part 40 met Hyrum Wright's law: with enough users, every":
        "第40部分讲过 Hyrum Wright 的定律：只要用户足够多，一个系统每一种可观察到的行为，都会被某个人所依赖；而 API 的用户，是陌生人写的程序。<bookmark mark='a'/>"
        "假设每个消费方各自独立地以一个很小的概率 p，依赖某种附带的行为。那么有人依赖它的概率，就是 1 减去 1 减 p 的 N 次方。<bookmark mark='b'/>不管 p 有多小，"
        "消费方达到大约 0.7 除以 p 个时，这条曲线就越过二分之一，然后朝着必然一路攀升。<bookmark mark='c'/>而这些行为，没有人承诺过：字段的顺序、一条错误信息的措辞、一个碰巧排好了序的列表。",
    "So the only safe changes are ones nobody could have":
        "所以，唯一安全的改动，是没有人可能观察到的改动：添加。<bookmark mark='a'/>新增一个响应字段是安全的，前提是每个客户端都忽略它不认识的字段；新增一个可选参数也是安全的。"
        "<bookmark mark='b'/>删除一个字段，会破坏读取它的人。重命名一个字段、改变它的类型也一样，比如这里，一个以分为单位的价格变成了字符串；添加一个必填参数也一样。"
        "<bookmark mark='c'/>有些改动只是看起来像添加：一个新的枚举值，会破坏那些逐一处理每种情况、却没有默认分支的客户端。<bookmark mark='d'/>这就是第三章的兼容性规则，"
        "应用到了整个 API 上。",
    "When a break is unavoidable, it becomes a new version, and":
        "当破坏性的改动无法避免时，它就成为一个新版本，而旧版本被慢慢退役。<bookmark mark='a'/>第2版与第1版并排发布，第1版继续工作。<bookmark mark='b'/>然后第1版被弃用："
        "它的响应会宣布它停止服务的日期，放在一个 Sunset 头里，这个头在2019年被标准化为 RFC 8594，这样客户端就能预先看到。<bookmark mark='c'/>只有过了这段窗口期，它才停止应答。"
        "<bookmark mark='d'/>版本号可以放在路径里，一目了然，也容易路由；也可以放在头部里，让每个资源只有一个 URL。<bookmark mark='e'/>无论哪种，放在那里的都只有主版本号："
        "次版本和补丁版本的改动都是添加性的。",
    "Google's API design guide turns these lessons into a style.":
        "Google 的 API 设计指南把这些教训变成了一种风格。<bookmark mark='a'/>一个 API 是由资源组成的层级结构：集合，以及集合里的资源，用像文件系统那样的路径来命名。"
        "<bookmark mark='b'/>每个集合都有同样的标准方法：list、get、create、update 和 delete，映射到 HTTP 的方法上，并带有第四章讲的安全性和幂等性。"
        "<bookmark mark='c'/>其他任何操作都成为自定义方法，写在冒号后面，比如 undelete。<bookmark mark='d'/>要点在于可预测：用同样几个动词作用于不同的名词，"
        "客户端库、权限和文档都只需构建一次，就适用于每一个 API。",
    "How can a provider know which changes are safe, when that":
        "哪些改动是安全的，取决于消费方实际怎么用，那提供方怎么才能知道呢？去问它们。<bookmark mark='a'/>在消费者驱动的契约测试里，借助 Pact 这样的工具，"
        "每个消费方自己的测试会记录它发出的请求和它读取的响应字段，并把它们发布为一份契约。<bookmark mark='b'/>提供方的构建会用新代码，把每一份契约重放一遍。<bookmark mark='c'/>"
        "这里，提供方重命名了作者的姓名字段。网页客户端和计费服务从来不读它，所以通过。移动应用读它，所以失败，于是这项改动在发布之前就被拦了下来。<bookmark mark='d'/>"
        "契约把 Hyrum 定律从一个意外变成了一张清单。",
    "One old rule pulls the other way. <bookmark mark='a'/> Jon":
        "有一条古老的规则，却朝相反的方向拉。<bookmark mark='a'/>Jon Postel 的稳健性原则，出自1981年的 TCP 规范：对自己所做的要保守，对从别人那里接受的要宽容。"
        "<bookmark mark='b'/>但每一个被容忍的错误，都是可观察到的行为。发送方会开始依赖它，每个新的接收方也必须容忍它，于是真正的协议，就成了规范，再加上任何人曾经接受过的每一个意外。"
        "<bookmark mark='c'/>2023年，Martin Thomson 和 David Schinazi 在 RFC 9413 中主张相反的做法：积极地维护协议，对协议不允许的东西予以拒绝，"
        "要尽早、要显眼，趁错误还容易修正的时候。",
    # ------------------------------------------------------------------ s08_queues
    "Chapter seven. Queues, and publish and subscribe.":
        "第七章：队列与发布/订阅。",
    "Every call so far has been a conversation: the caller waits":
        "到目前为止，每一次调用都是一场对话：调用方等着被调用方工作，如果被调用方宕机了，调用就失败。<bookmark mark='a'/>消息队列在它们之间放了一个缓冲区。生产者把消息交给队列，然后继续往下做，"
        "即使消费者正在部署的过程中。<bookmark mark='b'/>等消费者回来，消息都在那里等着，它按自己的节奏逐一处理。生产者和消费者在时间上解耦了，在速率上也解耦了。"
        "<bookmark mark='c'/>"
        "这就是 Amazon 的简单队列服务（Simple Queue Service）、RabbitMQ、Apache Kafka 和 Google 的 Cloud Pub/Sub 背后的思想；2003年，"
        "Gregor Hohpe 和 Bobby Woolf 为它的各种模式编写了一份目录。",
    "A queue must not lose a message when a consumer crashes":
        "消费者处理一条消息到一半时崩溃，队列不能因此丢掉这条消息。<bookmark mark='a'/>所以，接收一条消息并不会删除它。工作者 A 接收了这个订单，队列就把它隐藏一段可见性超时，这里是30秒，"
        "这也是 Amazon 队列的默认值。只有当工作者完成之后，它才删除这条消息：这就是它的确认。<bookmark mark='b'/>但工作者 A 很慢。超时到期，消息重新出现，工作者 B 拿走了它。"
        "<bookmark mark='c'/>B 完成并删除了它。然后，从没崩溃过的 A 也完成了。这项工作做了两遍，却没有任何东西出故障：这就是至少一次投递，正在按设计运行。",
    "Some messages can never succeed: a malformed order, say,":
        "有些消息永远不可能成功：比如一个格式错误的订单，碰到它的每个工作者都会崩溃。<bookmark mark='a'/>每次失败都把它送回队列，如果没有上限，它会永远兜圈子，每次都浪费一个工作者。"
        "所以队列会统计接收次数，达到最大值之后，这里是5次，就把消息移到死信队列，交给人来检查。<bookmark mark='b'/>我们让2000条消息通过一个模拟的队列，每条的工作耗时5到20秒，"
        "每20条中有1条很慢，要40到90秒，每500条中有1条是毒消息。<bookmark mark='c'/>有98条消息被处理了不止一次，其中有些处理了3次，还有2条进了死信队列。教训和第五章一样："
        "消费者必须是幂等的。",
    "A queue gives each message to one consumer. Workers compete":
        "队列把每条消息交给一个消费者。工作者们竞争消息，工作由它们分担。<bookmark mark='a'/>发布/订阅则把每条消息交给每一个感兴趣的人。订单服务向一个主题发布一个事件：订单已下。"
        "<bookmark mark='b'/>每个订阅都收到自己的一份副本，放在自己的队列里：邮件、计费和分析各按自己的节奏读取，慢的那个不会拖住其他的。<bookmark mark='c'/>发布者不知道谁在听，"
        "所以添加新的订阅者不需要改动它。这又是解耦，既在于何时，也在于是谁。",
    "What about order? One queue with many workers cannot promise":
        "那顺序呢？一个队列配许多工作者，没法保证顺序：两个工作者赛跑，慢的那个最后完成。<bookmark mark='a'/>Kafka 的答案，2011年出自 LinkedIn，是一个分区的日志。"
        "每条消息都带一个键，比如一个客户，键的哈希值选出其中一个分区，于是同一个键的每条消息都落在同一个分区里，并且有序。<bookmark mark='b'/>顺序在一个分区之内成立，跨分区则不成立，而通常要紧的，"
        "正是每个客户自己的顺序。<bookmark mark='c'/>一个消费者组把分区分给它的成员，每个消费者提交一个偏移量：它读到了哪里。崩溃之后，它从自己的偏移量处继续。这个日志可以重放，"
        "而这正是第46部分开始的地方。",
    # ------------------------------------------------------------------ s09_backpressure
    "Chapter eight. Backpressure.":
        "第八章：背压。",
    "Put a queue in front of a service, and Part 31's arithmetic":
        "在一个服务前面放一个队列，第31部分的算术就接管了。<bookmark mark='a'/>到达是随机的，服务时间也是随机的，也就是 M M 1 队列，在系统中的平均时间是 1 除以 1 减负载，"
        "以服务时间为单位：负载一半时是2，90%时是10，99%时是100。<bookmark mark='b'/>模拟的结果：2、5.3、11.4、23.7，以及107。<bookmark mark='c'/>"
        "负载超过1，就不存在稳态：在5万次到达之后，负载为1.05时平均值超过1000个服务时间，负载为1.2时是4000个。",
    "An unbounded queue never refuses work. It turns overload":
        "一个无界队列从不拒绝工作。它把过载变成了等待。<bookmark mark='a'/>所以要给它设上界。留出20个请求的空间，一个到达的请求如果发现队列已满，就立刻被拒绝，并附上一个错误：请稍后再试。"
        "<bookmark mark='b'/>现在，即使负载达到120%，在系统中的平均时间也保持在16个服务时间以下。代价是明确的：负载为0.8时，每1000个请求有3个被卸除，到1.2时上升到17%。"
        "<bookmark mark='c'/>这就是背压。队列向发送方推回去，过载就对能采取行动的那一方变得可见了。",
    "Now add retries. A service answers a hundred requests a":
        "现在加上重试。一个服务每秒能应答100个请求，它的客户端每秒发送90个。<bookmark mark='a'/>它宕机了10秒，客户端在每次失败1秒后重试，叠加在新的工作之上。"
        "<bookmark mark='b'/>服务恢复时，它每秒要面对990个请求。每秒只有10个的余量，积压需要90秒才能排空：直到第119秒才恢复。真实的服务在过载时还会变慢，于是一场风暴可能自我维持下去，"
        "Bronson 和同事们在2021年称之为亚稳态故障。<bookmark mark='c'/>带抖动的指数退避把重试分散开：峰值是381，在第69秒恢复。<bookmark mark='d'/>"
        "重试预算做得更好。",
    "gRPC's retry throttling gives each client a bucket of":
        "gRPC 的重试限流给每个客户端一桶令牌。<bookmark mark='a'/>每次失败花掉一个令牌，每次成功挣回十分之一个，当桶里不到一半时，客户端就停止重试，立刻报告失败。"
        "<bookmark mark='b'/>在我们这次故障中，桶在第一秒之内就跌到一半以下：只有49次失败被重试。峰值是139，服务一恢复就回到了正常。<bookmark mark='c'/>代价是：900个请求，"
        "也就是故障期间到达的每一个请求，得到的都是错误而不是答案。这能否接受，是一个产品决策；另一种选择，是让所有人再多承受将近90秒的过载。",
    "These are one family of defences. <bookmark mark='a'/> A":
        "这些属于同一族防御手段。<bookmark mark='a'/>断路器（熔断器），由 Michael Nygard 在2007年的书《Release It!》中描述，它监视对一个依赖的调用。当失败超过一个阈值，"
        "它就打开，调用会立即失败，根本不发出去。冷却一段时间之后，它放一次试探调用通过：成功就闭合，失败就再次打开。<bookmark mark='b'/>负载卸除在门口就拒绝工作，先拒绝最廉价的。"
        "准入控制限制正在进行的请求数，并像 TCP 调整它的窗口那样调整这个上限。还有截止时间，第九章会把它沿着调用链往下传，它让服务可以丢掉调用方已经放弃了的工作。<bookmark mark='c'/>"
        "无限的缓冲区只会把过载变成延迟，把延迟变成超时，再把超时变成重试。",
    # ------------------------------------------------------------------ s10_micro
    "Chapter nine. Monoliths and microservices.":
        "第九章：单体与微服务。",
    "Now the architectural question. <bookmark mark='a'/> A":
        "现在来看架构问题。<bookmark mark='a'/>单体是一个程序，作为一个整体部署。它的模块以纳秒级的速度互相调用，共享一个数据库，也一起失败。<bookmark mark='b'/>"
        "微服务把这些模块拆成独立的程序，每个都有自己的数据，通过网络通信。<bookmark mark='c'/>收益主要在组织上。每个团队在准备好时部署自己的服务，并独立地扩展它；第40部分的康威定律说，"
        "系统反正会映照出团队的结构。<bookmark mark='d'/>失去的是：每一次调用现在都可能失败、变慢或者重复，这是第一章的教训；而两个服务共享的每一份数据，都成了第十章要解决的问题。",
    "So where should the cuts go? <bookmark mark='a'/> Eric":
        "那么，该在哪里切分呢？<bookmark mark='a'/>Eric Evans 2003年的书《领域驱动设计》（Domain-Driven Design），给出了大多数团队采用的答案：限界上下文。"
        "像“客户”这样一个词，对销售、计费和发货来说含义各不相同，每个上下文都应该拥有自己的模型，而不是共享一个巨大的模型。<bookmark mark='b'/>切得好，每个团队想什么时候部署就什么时候部署。"
        "<bookmark mark='c'/>切得不好，你就会得到两边最坏的东西：一个分布式单体，也就是只能一起部署的服务，因为它们共享一个数据库，或者一个库的版本，或者一串同步调用。它有网络的所有故障，"
        "却没有任何独立性。",
    "Microservices also turn one request into many. <bookmark":
        "微服务还把一个请求变成许多个。<bookmark mark='a'/>假设一个请求并行扇出到 k 个后端，并等待它们全部返回。每个后端通常都很快，中位数是10毫秒，但每100次调用中有1次会碰上糟糕的时刻："
        "一次停顿，或者一次重传。<bookmark mark='b'/>只有1个后端时，超过100毫秒的请求不到2%。有100个后端时，这个比例是46%，连中位数本身都变成了原来的4倍。"
        "<bookmark mark='c'/>k 个后端中至少有一个碰上糟糕时刻的概率，是 1 减去 0.99 的 k 次方：100个时是63%。后端很多时，实测的比例更低，因为并不是每个糟糕时刻都会超过100毫秒。"
        "这就是第39部分讲的规模下的尾延迟：许多个里最慢的那个说了算。",
    "If a request must be answered within a deadline, the":
        "如果一个请求必须在截止时间内得到应答，截止时间就应该随它一起传递。<bookmark mark='a'/>这个请求有150毫秒。网关用掉其中5毫秒，把剩下的145毫秒交给认证服务；认证服务用掉8毫秒，"
        "把137毫秒交给订单服务，就这样沿着关键路径一路往下。<bookmark mark='b'/>支付服务收到82毫秒，用了60毫秒，还剩22毫秒作为余量。<bookmark mark='c'/>"
        "gRPC 在每次调用中都携带剩余的时间，所以一个服务一旦发现自己的截止时间已过，就可以立刻停下，而不是去做没有人会读的工作。这就是第八章的教训，变得精确了。",
    # ------------------------------------------------------------------ s11_data
    "Chapter ten. Data across services.":
        "第十章：跨服务的数据。",
    "Chapter nine left us data that more than one service needs.":
        "第九章给我们留下了不止一个服务需要的数据。<bookmark mark='a'/>规则是，每个服务拥有自己的数据库：订单、支付和库存各自保存自己的表。<bookmark mark='b'/>"
        "任何服务都不直接读取别的服务的表；那样会把它们重新焊成一个程序。其他服务要通过它的接口来询问，或者监听它的事件。<bookmark mark='c'/>所以，下单就是两次写入：订单数据库里的一行，"
        "以及消息代理上的一个事件。两个系统，却没有跨越两者的事务：这就是双写问题。",
    "Suppose the service simply does the two writes in turn. We":
        "假设这个服务就是简单地依次做这两次写入。我们模拟了1万个订单，在两次写入之间有1%的概率崩溃。<bookmark mark='a'/>先提交，再发布：每个订单都保存了，但崩溃之后，没有事件发出。"
        "有110个订单从来没有人知道。<bookmark mark='b'/>先发布，再提交：崩溃会留下一个事件，对应的订单却从未保存。有110个幽灵订单被宣布了出去。<bookmark mark='c'/>"
        "交换顺序只是交换了故障，重试也帮不上忙：本该重试的那个进程，正是崩溃的那个。",
    "The cure is to make the two writes one. <bookmark mark='a'/>":
        "解药是把两次写入变成一次。<bookmark mark='a'/>在与订单相同的本地事务中，服务把事件插入一张发件箱（outbox）表。两行要么都提交，要么都不提交。<bookmark mark='b'/>"
        "一个中继发布尚未发送的行，然后把它们标记为已发送。如果它在两步之间崩溃，重启后就会再发布一次。<bookmark mark='c'/>所以发件箱永远不会丢失事件，也不会凭空捏造事件。它只可能重复，"
        "而第五章的去重会去掉重复。<bookmark mark='d'/>在同样的1万个订单上：没有丢失，没有幽灵，有110个无害的重复。<bookmark mark='e'/>"
        "像 Debezium 这样的变更数据捕获工具，则改为读取数据库自己的预写日志，第46部分会展示这一点。",
    "An action that spans services needs more. <bookmark":
        "跨越多个服务的操作需要更多手段。<bookmark mark='a'/>1987年，Hector Garcia-Molina 和 Kenneth Salem 提出了 saga（长事务）："
        "把一个长事务写成一串短的本地事务，每个都立即提交，并配有一个撤销它的补偿操作。我们的订单 saga 依次预留库存、扣款、预订快递员，然后确认。<bookmark mark='b'/>这里，库存预留了，"
        "卡也扣了款，然后订不到快递员。<bookmark mark='c'/>于是 saga 倒着运行：先给卡退款，再释放库存。补偿是一种语义上的撤销，是一笔退款，而不是抹掉那笔扣款；它会一直重试，直到成功，"
        "所以它必须是幂等的。",
    "We ran ten thousand orders through the saga, with failures":
        "我们让1万个订单通过这个 saga，在前三步注入故障。<bookmark mark='a'/>9359个完成了；641个被补偿。<bookmark mark='b'/>106个在预留库存时失败，"
        "317个在扣款时失败，218个在预订快递员时失败。<bookmark mark='c'/>有57次补偿失败并被重试。而处于半完成状态的订单，也就是钱扣了却没有库存，或者订了快递员却没有付款，数量是零。",
    "Sagas pay for this. <bookmark mark='a'/> Each step commits":
        "saga 是要付出代价的。<bookmark mark='a'/>每一步都立即提交，所以没有隔离性：另一个请求可能恰好在退款之前，看到订单已付款。<bookmark mark='b'/>设计上用语义锁来绕开它，"
        "在 saga 结束之前把订单标记为待处理；还有可交换的更新，用加和减，而不是覆盖。<bookmark mark='c'/>可以由一个编排器来驱动这些步骤，也可以让服务对彼此的事件做出反应："
        "这叫编舞式协作（choreography）。<bookmark mark='d'/>为什么不跨服务使用两阶段提交呢？第39部分讲过，参与者会一直持有锁，直到协调者做出决定，而一个死掉的协调者会把它们全部阻塞。",
    # ------------------------------------------------------------------ s12_mesh
    "Chapter eleven. Finding, routing and trusting services.":
        "第十一章：发现、路由与信任服务。",
    "Before a client can call a service, it must find one of its":
        "客户端在调用一个服务之前，必须先找到它的一台服务器。<bookmark mark='a'/>每个实例在启动时注册自己，注册中心则不断检查它是否健康。"
        "<bookmark mark='b'/>客户端询问当前有哪些健康的地址。<bookmark mark='c'/>一个不再响应健康检查的实例会被剔除，请求也不再发往它。"
        "<bookmark mark='d'/>最朴素的注册中心就是 DNS：服务有一个名字，每个实例有一个地址。但应答会被缓存，所以 DNS 迟迟忘不掉一台已经死掉的服务器。",
    "Which server should take each request? <bookmark mark='a'/>":
        "每个请求该由哪台服务器来处理？<bookmark mark='a'/>如果随机选择，有些队列会因为运气不好而排得很长。“两个选择的力量”随机问两台服务器有多忙，"
        "然后挑负载较轻的那台。<bookmark mark='b'/>50台服务器、负载90%时，随机选择的平均值是10个服务时间，第99百分位是49；轮询大约把平均值减半，"
        "把尾部压到21；两个选择则把它们降到2.6和9。<bookmark mark='c'/>第20部分的球与箱解释了原因：只有一个随机选择时，n 个箱子里最满的那个"
        "大约装 log n 除以 log log n 个球；有两个选择时，大约是 log log n。Azar、Broder、Karlin 和 Upfal 在1994年证明了这一点。",
    "Every service needs retries, timeouts and encryption.":
        "每个服务都需要重试、超时和加密。<bookmark mark='a'/>服务网格（service mesh）把它们从应用程序里拿了出来：每个服务旁边运行一个边车代理（sidecar），"
        "比如 Envoy，每一次调用都经过它。<bookmark mark='b'/>边车会带着退避去重试，强制执行超时，并在一台服务器不断失败时打开断路器，不再调用它。"
        "<bookmark mark='c'/>边车之间运行双向 TLS，也就是第30部分那种两端都出示证书的握手，这样服务器就能知道是哪个服务在调用它；SPIFFE 为每个工作负载命名。"
        "<bookmark mark='d'/>控制平面，比如 Istio 或 Linkerd，负责分发配置和证书。",
    "Services must also know who is calling. OAuth 2.0, RFC":
        "服务还必须知道是谁在调用。OAuth 2.0，即 RFC 6749，让用户可以授予一个应用有限的访问权限，而不必交出密码。<bookmark mark='a'/>应用把浏览器"
        "引导到授权服务器，<bookmark mark='b'/>用户在那里登录并表示同意。<bookmark mark='c'/>授权服务器把浏览器送回来，带着一个短期有效的授权码，"
        "<bookmark mark='d'/>应用再用它换取一个访问令牌和一个刷新令牌。有了 PKCE，应用一开始只发送了一个秘密的哈希，现在才揭示这个秘密本身，"
        "所以被偷走的授权码毫无用处。<bookmark mark='e'/>访问令牌随每次调用发往资源服务器，刷新令牌则用来给它续期。",
    "Access tokens are often JSON Web Tokens, RFC 7519.":
        "访问令牌通常是 JSON Web Token，即 RFC 7519。<bookmark mark='a'/>它由三段 base64 用点连接而成：一个指明算法的头部，一个由声明组成的载荷，"
        "这里是角色为 reader 的 ada，以及一个覆盖前两者的签名。<bookmark mark='b'/>我们的第一个验证器完全照头部说的做。把载荷改成 admin，签名就验证失败。"
        "<bookmark mark='c'/>但是把算法设成 none，这是标准为不加保护的令牌所允许的，再去掉签名，这个验证器就会接受一个自称 admin 的令牌。"
        "<bookmark mark='d'/>修复办法写在 RFC 8725 里：服务器要固定它所期望的算法。我们固定了算法的验证器，拒绝了这两种伪造。",
    "A bearer token is a capability: whoever holds it may use":
        "持有者令牌（bearer token）是一种能力（capability）：谁持有它，谁就能使用它。Macaroon 由 Birgisson 及其同事在2014年提出，"
        "是任何持有者都可以削弱的能力。<bookmark mark='a'/>签发者用自己的密钥对一个标识符签名。<bookmark mark='b'/>每一条附加条件（caveat），"
        "比如只限照片、只限读取、只到12月为止，都用上一个签名来签，所以持有者不需要密钥就能收窄一个令牌；而要去掉一条附加条件，就得把一次哈希倒推回去。"
        "<bookmark mark='c'/>签发者重新计算这条链，并检查每一条附加条件。第55部分会再回到它们。",
    # ------------------------------------------------------------------ s13_time
    "Chapter twelve. Time in APIs.":
        "第十二章：API 中的时间。",
    "A computer has more than one clock, and Part 38 showed that":
        "一台计算机有不止一个时钟，而第38部分表明，没有哪两台机器的时钟是一致的。<bookmark mark='a'/>墙上时钟（wall clock）告诉你日期和一天中的时刻。"
        "它由 NTP 设置，也由人来设置，而且它会跳变，既可能往前跳，也可能往回跳。<bookmark mark='b'/>用它给一个请求计时，如果请求运行期间时钟被往回拨，"
        "算出来的耗时就是负的。<bookmark mark='c'/>单调时钟只会往前走。它作为日期毫无意义，在另一台机器上也毫无意义，"
        "但它正是用来做超时、重试和测量延迟的那个时钟。",
    "Time zones make the wall clock stranger still. <bookmark":
        "时区让墙上时钟变得更加古怪。<bookmark mark='a'/>2026年3月8日，在纽约，时钟从凌晨2点直接跳到3点。中间那一个小时在那里根本不存在。"
        "<bookmark mark='b'/>从1点半开始，加上一小时的墙上时间，Python 的 zoneinfo 给出的是2点半，一个那天并不存在的时刻。<bookmark mark='c'/>"
        "经由 UTC 换算之后，它是夏令时3点半：恰好晚了真实的一个小时。<bookmark mark='d'/>偏移量也不都是整小时。豪勋爵岛比 UTC 早10个半小时，"
        "而且它的时钟每次调整也只有半个小时。",
    "UTC also has extra seconds. <bookmark mark='a'/> The":
        "UTC 还有多出来的秒。<bookmark mark='a'/>地球的自转并不稳定，为了让时钟与它保持同步，偶尔会插入一个闰秒：时钟显示23点59分60秒。"
        "<bookmark mark='b'/>自1972年以来，一共加了27个。认定每分钟都是60秒的代码，会碰上一分钟有61秒的情况，2012年的那个闰秒就让好几家大型网站的服务器卡死了。"
        "<bookmark mark='c'/>从2008年起，Google 改为把这多出来的一秒抹匀（smear）：让时钟连续几个小时走得稍慢一点，于是没有哪个时钟会显示60。"
        "<bookmark mark='d'/>而在2022年，国际计量大会决定，到2035年停止增加闰秒。",
    "Then there are the bits a time is stored in. <bookmark":
        "然后是存储时间所用的那些位。<bookmark mark='a'/>Unix 时间计算的是从1970年起的秒数。在一个有符号的32位整数里，最大值是2的31次方减1，"
        "对应2038年1月19日凌晨3点14分7秒。<bookmark mark='b'/>再过一秒，进位一路传到符号位，时钟就显示1901年12月。<bookmark mark='c'/>"
        "操作系统已经改用64位，但只要某个文件格式、数据库列或协议字段只保留了32位，这个错误就依然存在。",
    "So an API that handles time keeps a few rules. <bookmark":
        "所以，一个处理时间的 API 要遵守几条规则。<bookmark mark='a'/>用 UTC 存储时刻。<bookmark mark='b'/>对于本地时间，比如一场会议，"
        "要保存时区的名字，America 斜杠 New York，而不是偏移量：偏移量一年变两次，而时区的规则会随法律改变。<bookmark mark='c'/>在线路上，"
        "写成 ISO 8601，采用 RFC 3339 规定的格式，并带上偏移量。<bookmark mark='d'/>用单调时钟测量时长。<bookmark mark='e'/>"
        "并且永远不要靠加秒数来做日历运算：在纽约，2026年3月8日只有23个小时。",
    "Clocks also meet chapter five's idempotency keys. <bookmark":
        "时钟还会碰上第五章的幂等键。<bookmark mark='a'/>一个键只保留有限的时间，这里是10分钟，键过期之后才到达的请求会被当作新请求。"
        "<bookmark mark='b'/>如果检查键的那个服务快了2分钟，键就会提前过期，第9分钟的一次重试就会被扣第二次款。<bookmark mark='c'/>所以，"
        "让一个时钟来决定过期，把键保留得远比任何客户端的重试都久；而在跨机器的顺序很重要的地方，使用第39部分的混合逻辑时钟，"
        "而不是指望墙上时钟彼此一致。",
    # ------------------------------------------------------------------ s14_job
    "Chapter thirteen. The Job as three services.":
        "第十三章：拆成三个服务的那项任务。",
    'f"Here is the Job split across a network.':
        "这是被拆分到网络上的那项任务。<bookmark mark='a'/>分词器读取我们30本小说的前{w['words']:,}个词，每200个词为一块，每块给计数器发一条消息，"
        "消息里带着这一块的词计数。计数器把它们加起来，排名器再向它要出现最多的词。<bookmark mark='b'/>我们模拟的网络会丢掉5%的消息，确认消息也算在内，"
        "还会重复2%。<bookmark mark='c'/>所以分词器会重试每一块，直到收到确认。这用了三轮，算上重试和确认，一共{w['messages']}条消息。"
        "其中{w['lost']}条丢失，{w['duplicated']}条被重复。",
    'f"Now vary the network. <bookmark mark=':
        "现在改变网络。<bookmark mark='a'/>在完美的网络上，重试从不发生，两个版本都完全准确。随着网络变差，没有保护的计数器算错的词越来越多："
        "在丢失20%、重复10%时，5882个词里有{sw[-1]['without_wrong']:,}个是错的，总共多算了{sw[-1]['without_over']:,}个计数。"
        "<bookmark mark='b'/>每一个错误都是多算。重试永远不会丢失数据；它只会重复数据。<bookmark mark='c'/>有了幂等键，在每一种比率下计数都完全准确。"
        "唯一的代价是流量：随着网络变差，消息从{sw[0]['messages']}条增加到{sw[-1]['messages']}条。",
    'f"What did the fix cost? <bookmark mark=':
        "这个修复花了多少代价？<bookmark mark='a'/>每条消息都带着一个给它命名的键：哪个分词器，哪一块。<bookmark mark='b'/>计数器保存它已经应用过的键的集合。"
        "键已经见过的消息会被跳过，但仍然会再确认一次，因为丢掉的可能正是第一次确认。<bookmark mark='c'/>这里是每块一个键，一共{w['chunks']}个，"
        "而且键必须和计数记录在同一个事务里，否则两者之间的一次崩溃就会破坏这个保证。<bookmark mark='d'/>键不能永远保留下去。要么每个键都保留到"
        "不再可能有重试到达为止，要么给每个发送者一个序号，只保留已应用的最大序号，就像 TCP 对字节所做的那样。<bookmark mark='e'/>工业界正是这么做的："
        "支付 API 在每个请求上都接受一个幂等键，而从2017年起，Kafka 的生产者会给它们的消息编号，让代理服务器（broker）能够丢弃重复的消息。",
    "Why not let the network layer handle it? TCP already":
        "为什么不让网络层来处理呢？TCP 已经能把字节恰好一次、按顺序地送达。<bookmark mark='a'/>但 TCP 的保证止于套接字。如果计数器加上了一块，"
        "然后在确认之前崩溃了，重试会经由一条新的连接到来，而 TCP 没有办法知道这是一次重复。<bookmark mark='b'/>这就是 Jerome Saltzer、David Reed "
        "和 David Clark 在1984年提出的端到端论证：一个需要应用知识的功能，只能在端点上完成。较低的层可以让它更快，但永远不能让它正确。"
        "<bookmark mark='c'/>所以，恰好一次是整个系统的性质，而不是任何一个协议的性质：它是至少一次的投递，加上一个幂等的效果，"
        "而且幂等的记录要和效果本身一起保存。",
    # ------------------------------------------------------------------ s15_frontier
    "Chapter fourteen, the frontier. Can a system of services be":
        "第十四章，前沿。一个由多个服务组成的系统，能被证明是正确的吗？",
    "One line of research treats a protocol between services as":
        "有一条研究路线，把服务之间的协议当作一种类型。<bookmark mark='a'/>从上方把整个对话一次写出来：客户端发出一个订单，订单服务请支付服务扣款，"
        "支付服务回答成功或被拒，订单服务再确认或拒绝。<bookmark mark='b'/>这个全局描述可以投影到每个参与者上，给每个服务一个它自己的局部类型："
        "它接收什么，发送什么，按什么次序。<bookmark mark='c'/>编译器可以对照每个服务的投影来检查它，如果每一个都符合，整个系统就不会死锁，"
        "也不会收到意料之外的消息。这就是会话类型，由 Kohei Honda 在1993年提出，2008年扩展到多方；还有编舞式编程（choreographic programming），"
        "由 Fabrizio Montesi 等人发展起来。悬而未决的问题是，它们能在多大程度上延伸到这一部分讨论的那些故障：丢失的消息、重试和崩溃。",
    'f"In chapter five we checked every execution of a':
        "在第五章，我们检查了一个小协议的每一种执行。<bookmark mark='a'/>一条消息、一次重试时，有{g[0]['states']}个状态；四条消息时，"
        "有{g[-1]['states']:,}个。状态空间随系统规模指数增长，所以模型检验器能完整覆盖小的实例，对大的实例却完全无能为力。<bookmark mark='b'/>"
        "即便如此，小的实例也能找出真正的错误。Amazon 的工程师为 DynamoDB、S3 和其他服务编写了 TLA+ 模型，发现了一些没有任何测试捕获过的微妙错误。"
        "<bookmark mark='c'/>要覆盖所有规模，就需要证明。2015年，用 Dafny 写的 IronFleet 和用 Coq 写的 Verdi 证明了分布式系统的正确性，"
        "其中包括一个复制状态机和一个键值存储，一直证明到实际运行的代码。",
    "Between models and production there is testing of the whole":
        "在模型和生产之间，还有对整个系统的测试。<bookmark mark='a'/>FoundationDB 背后的团队把他们的数据库构建成可以整个在一个进程里运行，"
        "面对模拟的网络、模拟的磁盘和模拟的时钟，注入各种故障，而且每次运行都能从一个随机种子精确重现。<bookmark mark='b'/>Kyle Kingsbury 的 Jepsen "
        "测试会对真实的集群制造网络分区，并检查它们记录下来的历史；许多数据库都被证明违反了它们自己公布的保证。<bookmark mark='c'/>还有混沌工程，"
        "从2011年 Netflix 的 Chaos Monkey 开始，它故意杀掉生产环境中的机器，让恢复每天都得到演练。<bookmark mark='d'/>我们自己的模拟器，"
        "就是其中第一种的微缩版：它的网络带有种子，所以这一部分里每一条丢失的消息都能被精确重放。",
    "Open problems. <bookmark mark='a'/> Protocol types that":
        "开放问题。<bookmark mark='a'/>能把故障考虑在内的协议类型：丢失的消息、重试和崩溃，同时仍然能排除错误。<bookmark mark='b'/>可以证明的兼容性："
        "判定一个 API 的新版本能让每一个现有客户端继续工作，不只是它的类型，还包括它的行为。<bookmark mark='c'/>能扩展到真实服务系统的验证，"
        "而代价和写测试差不多。<bookmark mark='d'/>以及针对整个调用图的重试策略，可以证明它不会把一次小的过载变成一次大的过载。<bookmark mark='e'/>"
        "这一部分的研究题，要求做一个兼容性检查器，证明每一个现有客户端面对新版本时，仍能完成它的协议的每一次运行，即使消息会丢失、重复和乱序。",
    # ------------------------------------------------------------------ s16_outro
    "What we built in this part. Protocol Buffers' wire format":
        "我们在这一部分搭建了什么。从第一性原理出发的 Protocol Buffers 线路格式，逐字节对照已公布的示例；以及作为子类型问题的模式演化。"
        "会重复行的偏移量分页，和从不重复的游标分页。恰好一次投递，在一个模型的每一种执行中检验过，它就是至少一次投递加上去重。重试风暴，"
        "以及终结它们的退避和预算。发件箱（outbox），把丢失的事件变成我们可以去除的重复；还有 saga，撤销它们无法完成的事情。以及随扇出增长的尾部延迟。"
        "贯穿其中的是一个想法：远程调用可能以本地调用不可能的方式失败，所以每条消息都必须丢了也安全，重复也安全。",
    "Where this comes back. Part 44 measures what a change does":
        "它们会在哪里再出现。第44部分用对照实验，测量一项改动对使用它的人有什么影响。第45部分把服务运行在来来去去的租用机器上。"
        "第46部分把发件箱变成一条流，用上日志和变更数据捕获。第48和第49部分用这些积木设计完整的系统。第50部分让它们保持运行，"
        "靠的是服务等级目标和错误预算。",
    "In practice. Change APIs only by adding, never reuse a":
        "实践中。修改 API 只能做加法，永远不要重用字段编号，分页要用游标而不是偏移量。给每一次调用设一个截止时间并把它向下传递，"
        "重试时要用退避、抖动和预算。给每一次写操作一个幂等键，通过发件箱发布事件，而不是做两次独立的写入。把工作流构建成 saga，"
        "让它的补偿操作本身也是幂等的，并确保有人去读死信队列。服务之间用双向 TLS 相互认证，固定验证令牌所用的算法，并用 UTC 存储时间。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一题上暂停。第五题是一道动手题：给我们的 saga 加上快递员超时，"
        "并证明一个幂等的补偿操作能让每一个订单都保持一致。最后一题，标着星号，是一道研究题：证明一个服务的新版本能让每一个现有客户端继续工作，"
        "即使是在一个会丢失、重复和乱序的网络上。",
    "Next time, Part 44: people and products. Software is used":
        "下一次，第44部分：人与产品。软件是给人用的，而两者都可以测量。菲茨定律（Fitts's law）可以从香农的信道容量推出来，"
        "希克定律（Hick's law）是一次选择的熵；而在直觉不够用的地方，工业界会做对照实验，用的统计方法很容易出错。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书籍和论文，都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
