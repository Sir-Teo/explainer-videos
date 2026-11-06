"""Chinese narration for cs46: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第46部分：日志、流与数据仓库"

CHAPTERS = {
    "Hook": "日志",
    "Partitioned": "1. 分区日志",
    "Throughput": "2. 每秒搬运一吉字节",
    "Cdc": "3. 把变更当作事件",
    "Dataflow": "4. 事件时间与处理时间",
    "Exactly": "5. 恰好一次的状态",
    "Sketches": "6. 生产中的流式算法",
    "Warehouse": "7. 数据仓库",
    "Columnar": "8. 列式文件",
    "Dremel": "9. 列中的嵌套数据",
    "Lakehouse": "10. 对象存储上的表",
    "Mpp": "11. 千台机器上的查询",
    "Quality": "12. 值得信赖的数据",
    "Job": "13. 作为流的那项任务",
    "Frontier": "14. 前沿：流、表及其极限",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "A log, in the sense of this part, is the simplest data":
        "本部分所说的日志，是能记住时间的最简单的数据结构：记录一条接一条地追加，每条带一个编号，即它的偏移量（offset），而且永不改动。"
        "<bookmark mark='a'/>我们已经一次又一次地遇到它。数据库在动数据之前，先把每一次变更写进日志。Raft 就一份日志达成一致，每个副本按顺序应用它。"
        "Git 的历史是一份快照的日志。第43部分的发件箱（outbox）是一份事件的日志。<bookmark mark='b'/>2013年，曾搭建 LinkedIn 数据基础设施的"
        " Jay Kreps 提出，日志是实时数据的统一抽象：是在一家公司所有系统之间搬运数据的正确方式。",
    "Here is the argument. <bookmark mark='a'/> A company has":
        "论证是这样的。<bookmark mark='a'/>一家公司有数据源，比如数据库和点击流；也有需要这些数据的系统：搜索索引、缓存、数据仓库、反欺诈模型。"
        "把每个数据源直接连到每个消费者，你就要建16条管道，每条都有自己的格式、自己的故障。<bookmark mark='b'/>换个做法，在中间放一份日志。"
        "每个数据源都往里追加，每个消费者都从中读取：只要8条连接。<bookmark mark='c'/>每个消费者保存自己的位置，按自己的节奏读，还能回头重放历史。"
        "新的消费者从头开始，逐步追上。",
    "So every company's data ends up in two places. <bookmark":
        "所以，每家公司的数据最终都落在两个地方。<bookmark mark='a'/>一份只追加的日志，记录发生的一切。<bookmark mark='b'/>一个面向列的数据仓库，"
        "它的布局是为了一次性回答关于全部数据的问题。<bookmark mark='c'/>而在两者之间，是流处理器，随着数据流动持续地计算答案。<bookmark mark='d'/>"
        "我们会看到，难点在于时间：事件会迟到、会乱序、会重复到达，而正确的答案必须经受住这三者。",
    "This is Part 46 of Computer Science, Built. <bookmark":
        "这是计算机科学，从零搭建，第46部分。<bookmark mark='a'/>我们会构建一个带消费者组的分区日志；把数据库的变更变成一条流；"
        "给事件窗口一种能经受迟到的时间概念；为运行中的计算做检查点，让它恢复时具有恰好一次的状态；把一个列式文件拆开，一直拆到它的编码，"
        "以及让嵌套数据能存进列里的那些级别；最后把那项任务做成一条小说流上实时更新的前20名。",
    # ------------------------------------------------------------------ s02_partitioned
    "Chapter one. The partitioned log.":
        "第一章：分区日志。",
    "Kafka was built at LinkedIn by Jay Kreps, Neha Narkhede and":
        "Kafka 由 Jay Kreps、Neha Narkhede 和 Jun Rao 在 LinkedIn 构建，并于2011年发表。<bookmark mark='a'/>一个主题（topic），"
        "也就是一条有名字的流，比如页面浏览，被分成若干分区，每个分区都是一份日志：记录追加在末尾，按偏移量编号，永不改动。<bookmark mark='b'/>"
        "在磁盘上，一个分区是一串段文件，每个以它的第一个偏移量命名，并带有一个指向其中的稀疏索引。只有最后一个段会被写入；默认每满1吉字节就开始一个新段。"
        "<bookmark mark='c'/>一个消费者的全部状态，就是每个分区一个数字：下一个要读的偏移量。它把这个数字提交回 broker，崩溃之后就从那里接着读。",
    "Which partition does a record go to? <bookmark mark='a'/>":
        "一条记录该进哪个分区？<bookmark mark='a'/>生产者对记录的键做哈希。这里的键是单词，用 CRC32 哈希到4个分区里。<bookmark mark='b'/>"
        "键相同的记录总落在同一个分区，所以同一个键的记录保持顺序，我们的模拟器对每个键都检查了这一点。按键有序是 Kafka 的保证，"
        "通常也正是应用所需要的：同一位客户的所有变更，按顺序排好。<bookmark mark='c'/>跨分区则完全没有顺序。而热键造成热分区："
        "常见词塞满了两个分区，另一个分区却只装着一条 ship。",
    "Readers share the work through a consumer group. <bookmark":
        "读者通过消费者组来分担工作。<bookmark mark='a'/>每个分区恰好由一个成员读取，所以一个组最多可以扩展到和分区数一样多的成员，"
        "而另一个组可以独立地读同一份日志。这里3个成员各持有4个分区。<bookmark mark='b'/>第4个成员加入，组进行再均衡。范围分配重新切出4段连续的分区，"
        "移动了6个分区。粘性分配器只移动3个，这是可能的最少数目，因为新成员需要3个。<bookmark mark='c'/>接着2号成员离开：范围分配移动4个分区，"
        "粘性分配器只移动2号成员原有的那3个。每个被移动的分区都会暂停，直到新的所有者从已提交的偏移量处接着读。",
    "A log cannot grow for ever, and there are two ways to":
        "日志不能永远增长下去，遗忘有两种方式。<bookmark mark='a'/>按时间：比保留期更老的整个段会被删除，保留期默认是7天，起始偏移量随之前移。"
        "删除一个文件很便宜，这正是要有段的原因之一。<bookmark mark='b'/>按键：压实（compaction）主题只为每个键保留最新的一条记录，"
        "位于它原来的偏移量处；而值为空的记录，即墓碑（tombstone），会删除它的键。<bookmark mark='c'/>剩下的就是最新状态，而这就够了："
        "在我们的模拟器里，对50个键的2000次更新压实成50条记录，由它们重建出的表一模一样。",
    "Finally, a partition must survive losing a machine, so it is":
        "最后，分区必须经得起失去一台机器，所以它要复制。<bookmark mark='a'/>每个分区由一个 broker 担任领导者，承接所有写入；"
        "跟随者像消费者那样从它那里拉取。当同步副本集中的每个副本都拿到一条记录，它就算已提交，并对消费者可见；这个位置就是高水位。"
        "<bookmark mark='b'/>落后的跟随者会被移出这个集合，所以一块慢盘拖不住整个主题，高水位照样前进。确认设为 all，并且至少2个副本同步，"
        "那么每一次已确认的写入都有两份拷贝。<bookmark mark='c'/>这是第39部分的单主复制，而不是 Raft 的多数派：f 加 1 个副本能经受 f 次故障；"
        "而控制器，如今它本身也是一份 Raft 日志，只从同步副本集中挑选新的领导者。",
    # ------------------------------------------------------------------ s03_throughput
    "Chapter two. Moving a gigabyte a second.":
        "第二章：每秒搬运一吉字节。",
    "Why a gigabyte a second? <bookmark mark='a'/> It is roughly":
        "为什么是每秒一吉字节？<bookmark mark='a'/>这大约是一条万兆网络链路的承载量。在 Kafka 论文的实验里，一条消息是200字节，"
        "所以每秒一吉字节就意味着500万条消息，每条200纳秒。<bookmark mark='b'/>把这份预算放到第34部分的存储模型旁边："
        "从闪存做一次随机读，要花400份预算；从机械硬盘做一次，要花6万5千份。<bookmark mark='c'/>所以任何一条消息都不能等待任何东西："
        "不能等寻道，不能等一次往返，甚至不能有专属于自己的一次系统调用。接下来的一切，都是一次为许多条消息付账。",
    "The first answer is Part 34's rule: write in long runs.":
        "第一个答案是第34部分的准则：长串地写。<bookmark mark='a'/>日志别的什么都不做。生产者只追加，每个消费者只从自己的偏移量往前读，"
        "于是磁盘看到的是长长的顺序访问，内核的预读会在任何人开口之前就把页取来。<bookmark mark='b'/>在第34部分的模型磁盘上，"
        "这是每秒150兆字节，而随机访问只有每秒三分之一兆字节。<bookmark mark='c'/>也没有索引要维护，所以有一周的数据时，"
        "一次追加的代价和没有数据时一样。而不同磁盘、不同 broker 上的分区，带宽可以相加：7块这样的磁盘，就是每秒一吉字节。",
    "The second answer: never send one message alone. <bookmark":
        "第二个答案：永远不单独发送一条消息。<bookmark mark='a'/>生产者把发往同一分区的消息收集成一个批次，用一次请求发出整个批次。"
        "broker 原样追加它，消费者也以同样的方式取回它。<bookmark mark='b'/>每个请求都有固定的开销，而一个批次把它分摊给其中所有的消息。"
        "在 Kafka 论文里，一个生产者逐条发送时每秒发出5万条消息，按每批50条发送时则是40万条。<bookmark mark='c'/>代价是批次攒满期间几毫秒的延迟。"
        "而且批次比单条消息好压缩得多，因为相邻的记录会重复彼此的字段。",
    "The third answer is to stop touching the bytes. <bookmark":
        "第三个答案，是不再碰这些字节。<bookmark mark='a'/>用显而易见的方式提供数据时，数据要从磁盘复制进内核的页缓存，再进程序的缓冲区，"
        "再回到内核的套接字缓冲区，最后送到网卡：按 Kafka 论文的算法，4次复制、2次系统调用。<bookmark mark='b'/>sendfile 调用让内核"
        "把文件的页直接交给套接字，中间那两次复制，连同一次系统调用，就都消失了。<bookmark mark='c'/>这之所以可行，只是因为 broker 从不查看消息内部："
        "磁盘上的字节，就是生产者发出的字节，也就是消费者收到的字节。像 TLS 那样在程序里加密，就放弃了零拷贝。",
    "The last answer is to let the operating system do the":
        "最后一个答案，是让操作系统来做缓存。<bookmark mark='a'/>Kafka 把每个批次写进文件系统，自己不保留任何缓存。内核的页缓存装着最近的尾部，"
        "所以跟得上的消费者从内存读取，根本不用去问磁盘。<bookmark mark='b'/>重放昨天数据的消费者要从磁盘读，但是顺序读。程序的堆里没有第二份拷贝，"
        "没有垃圾回收器去清扫数百万条消息，而且 broker 重启后缓存依然是热的。<bookmark mark='c'/>持久性来自第一章的副本，"
        "而不是强制把每次写入刷到磁盘。这些选择合在一起，让 Jay Kreps 在2014年报告：3台普通机器每秒写入200万条。",
    # ------------------------------------------------------------------ s04_cdc
    "Chapter three. Changes as events.":
        "第三章：把变更当作事件。",
    "A company's data lives first in databases, and other systems":
        "一家公司的数据首先存放在数据库里，而其他系统需要它的副本：搜索索引、缓存、数据仓库。<bookmark mark='a'/>诱人的设计是双写："
        "应用先写数据库，再写索引。<bookmark mark='b'/>如果它在两次写之间崩溃，数据库说12，索引说10，而且永远如此，任何地方都不报错。"
        "<bookmark mark='c'/>更糟的是，两个写入者可能竞争，两个系统以相反的顺序应用它们的写入。<bookmark mark='d'/>解药是只写一次，写进数据库，"
        "再从那一个权威的顺序推导出其他所有副本：也就是数据库提交的顺序。",
    "And the database already writes that order down. <bookmark":
        "而数据库本来就把这个顺序记了下来。<bookmark mark='a'/>每一次已提交的变更，都先进入它的预写日志，那是第35部分讲的。"
        "变更数据捕获（CDC）读取这份日志，把每个变更作为一个事件发布出去。<bookmark mark='b'/>一次更新、一次插入和一次删除，"
        "变成一个以行 id 为键的主题里的3个事件，于是每一行的变更都保持顺序，和第一章一样。<bookmark mark='c'/>一个事件带着该行变更前后的内容，"
        "以及它在日志中的位置。PostgreSQL 通过逻辑解码公开它的日志，MySQL 通过它的二进制日志，而 Debezium 把两者都变成流。"
        "<bookmark mark='d'/>开始时，连接器先给表做一个快照，然后恰好从快照所看到的那个位置起，跟随日志。",
    "Raw change capture has one drawback: it publishes the":
        "原始的变更捕获有一个缺点：它发布的是数据库的内部表，每个读者都会依赖上这些表的列。第43部分的发件箱解决了这个问题。"
        "<bookmark mark='a'/>在把订单42标记为已付款的那个事务里，服务还会往发件箱表插入一行，描述这个事件。两者要么都提交，要么都不提交。"
        "<bookmark mark='b'/>变更数据捕获只跟随发件箱，把其中的行发布到一个主题。<bookmark mark='c'/>事件是一份设计出来的契约，“订单已付款”，"
        "而不是某张表的拷贝，于是那张表现在可以自由地改变结构。<bookmark mark='d'/>投递仍然是至少一次：连接器如果在记录自己的位置之前崩溃，"
        "就会再发布一遍，所以读者按事件的标识符丢弃重复。",
    "Now turn the picture around. If every change is an event,":
        "现在把这幅图倒过来看。如果每个变更都是一个事件，那么当前状态就是对迄今为止所有事件的汇总。<bookmark mark='a'/>开一个账户，"
        "存入50，取出20，再存入10，余额依次是0、50、30、40。<bookmark mark='b'/>状态是一次折叠：从空开始，在事件上运行一个 apply 函数。"
        "同样的事件，总是得到同样的状态。<bookmark mark='c'/>所以流和表是同一样东西的两种视图。折叠一条变更流得到一张表；"
        "把一张表的每次变更记录下来，就得到一条流。第一章的压实主题正是如此：2000次更新折叠成50行。",
    "Event sourcing, as Martin Fowler described it in 2005,":
        "事件溯源（event sourcing），正如 Martin Fowler 在2005年描述的，就是用这种方式构建整个应用。<bookmark mark='a'/>命令先对照当前状态检查，"
        "如果有效，就往日志里追加事件，而这份日志就是权威记录系统。<bookmark mark='b'/>每一类问题都有自己的读模型，也就是对同一批事件的一次折叠："
        "余额、对账单、搜索索引、反欺诈特征。把写模型和读模型分开，叫作命令查询职责分离，即 CQRS。有缺陷的视图可以通过重放来重建。"
        "<bookmark mark='c'/>代价是：读模型落后于日志，所以用户可能无法立刻看到自己的写入。事件要永久保留，所以它们的模式必须演进，"
        "如第43部分所讲，而且要遗忘一个人很难。重放的代价还随历史增长，这要靠快照来限制。",
    # ------------------------------------------------------------------ s05_dataflow
    "Chapter four. Event time and processing time.":
        "第四章：事件时间与处理时间。",
    'f"Every event in a stream carries two times.':
        "流中的每个事件都带着两个时间。<bookmark mark='a'/>它的事件时间是它发生的时刻，由记录这次点击的手机打上时间戳。<bookmark mark='b'/>"
        "它的处理时间是管道看到它的时刻，总是更晚：一段网络延迟、一个队列，或者一部在隧道里的手机。<bookmark mark='c'/>把每个事件画出来，"
        "横轴是事件时间，纵轴是到达时间。这里有{n}个模拟事件，每秒{rate}个，随着处理时钟走动而出现。如果没有延迟，它们会落在对角线上；"
        "大多数落在对角线稍上方，最慢的大约迟到{maxd:.0f}秒。<bookmark mark='d'/>所以，一条统计某一分钟点击数的管道，"
        "无法凭自己的时钟判断那一分钟的事件是否已经全部到达。",
    'f"The Dataflow model of Tyler Akidau and his':
        "Google 的 Tyler Akidau 和同事在2015年提出的 Dataflow 模型，首先问的是：结果在事件时间里属于哪里。<bookmark mark='a'/>"
        "滚动窗口把时间切成固定的片段，这里是{size}秒，所以每个事件恰好落在一个窗口里。<bookmark mark='b'/>滑动窗口有大小和步长，"
        "这里是每{step}秒一个{size}秒的窗口，所以每个事件属于两个窗口。<bookmark mark='c'/>会话窗口是从数据中找出来的：一个用户的一段连续活动，"
        "以{gap:.0f}秒的空隙结束，所以一个迟到的事件可能把两个会话合并成一个。<bookmark mark='d'/>这三种都是在事件时间里定义的："
        "答案取决于发生了什么，而不是管道何时听说。",
    'f"The second question is when, in processing time, a':
        "第二个问题是：在处理时间里，什么时候可以给出结果。<bookmark mark='a'/>水位线（watermark）是管道不断更新的一个断言："
        "不会再有更早的事件还在路上。如果对数据源了如指掌，它可以是精确的；通常它只是一个猜测。<bookmark mark='b'/>我们的水位线是"
        "迄今见过的最大事件时间减去{lag:.0f}秒，像阶梯一样跟在事件后面爬升。<bookmark mark='c'/>{n}个事件中有{len(late)}个到达时落在它后面："
        "它们迟到了。<bookmark mark='d'/>前十秒的窗口在水位线越过10时关闭，大约在第{fire:.0f}秒，此时收到了它{tot}个事件中的{inn}个。"
        "最后一个事件又晚了{miss[0][1] - fire:.1f}秒才到，而已经给出的答案是错的。",
    'f"How long should the watermark wait? We sent':
        "水位线应该等多久？我们让{total:,}个模拟事件通过十秒的窗口。<bookmark mark='a'/>不设滞后时，答案在窗口结束后"
        "{r0['mean_latency']:.0f}秒给出，有{r0['dropped']}个事件因为太迟而被丢弃。等待5秒，丢弃{lag5['dropped']}个。<bookmark mark='b'/>"
        "等待一分钟，只丢弃{rows[-1]['dropped']}个，{rows[-1]['windows']}个窗口中有{rows[-1]['exact']}个是精确的，"
        "但每个答案都迟了一分钟以上。<bookmark mark='c'/>出路是：在5秒时给出答案，把每个窗口的状态多保留一分钟，每当有迟到事件到达就修正它。"
        "每个窗口最终都是精确的，而第一批答案来得和以前一样快。",
    'f"The last two questions are when to emit and how':
        "最后两个问题是：何时输出，以及前后相继的答案之间是什么关系。<bookmark mark='a'/>触发器决定窗口的结果何时发出：提前发出，"
        "作为推测性的答案；准时发出，在水位线越过时；以及迟到发出，每个迟到事件一次。<bookmark mark='b'/>累积方式决定每次触发意味着什么。"
        "丢弃模式只输出新增的部分。累积模式每次输出整个窗口：5，然后9，然后10。带撤回时，每次触发还会撤回上一个答案，"
        "所以跨窗口求和的消费者不会把任何东西算两次。<bookmark mark='c'/>我们允许一分钟迟到的那次运行，触发了{al['refinements']}次修正。"
        "<bookmark mark='d'/>是什么、在哪里、何时、如何：Dataflow 模型对每条管道都问这四个问题。",
    # ------------------------------------------------------------------ s06_exactly
    "Chapter five. Exactly-once state.":
        "第五章：恰好一次的状态。",
    "A stream processor keeps state: running counts, open":
        "流处理器保存着状态：运行中的计数、尚未关闭的窗口、连接操作的缓冲区。<bookmark mark='a'/>状态按键分区，就像它所读的日志一样，"
        "所以每个键的计数恰好存在一个工作节点上，每个事件经过时都更新它。<bookmark mark='b'/>然后一个工作节点崩溃，它的状态就没了。"
        "日志里仍然存着每个事件。问题是从哪里恢复。重放得太晚，事件就被漏掉；太早，它们就被计了两次。",
    "Paris Carbone and his colleagues gave Apache Flink its":
        "Paris Carbone 和同事在2015年为 Apache Flink 给出了答案，它是第38部分 Chandy 与 Lamport 快照算法的后裔。<bookmark mark='a'/>"
        "记录从两个数据源流出，经过两个按键计数器，流向一个输出端（sink）。<bookmark mark='b'/>要做一个检查点，每个数据源记下自己的偏移量，"
        "并注入一个屏障（barrier），这是一个随记录一起传播的标记。<bookmark mark='c'/>有两个输入的计数器要等屏障在两个输入上都到达，"
        "同时扣住先送来屏障的那个输入，好让它的状态反映屏障之前的每个事件，而不包括之后的任何事件。这就是对齐。<bookmark mark='d'/>"
        "然后它在后台把状态复制到存储中，再把屏障传下去。<bookmark mark='e'/>当输出端收到全部屏障，检查点就完成了："
        "这些偏移量和状态描述了贯穿整个计算的一个一致切面。没有环、屏障又对齐时，不需要保存任何在途记录。",
    # ------------------------------------------------------------------ s06_exactly
    'f"We crashed our keyed counter on purpose. <bookmark':
        "我们故意让按键计数器崩溃。<bookmark mark='a'/>{N:,}个事件，3个工作节点，流运行期间不断做检查点。在偏移量{crash:,}处，每个工作节点都丢失了状态。"
        "<bookmark mark='b'/>恢复时载入最后一个完整的检查点，它来自偏移量{r0:,}，并把数据源倒回到同一位置。有{rep}个事件被处理了第二次。<bookmark mark='c'/>但它们遇到的状态，"
        "是它们第一次到达之前的样子，所以最终计数与一次从未出故障的运行完全相同。<bookmark mark='d'/>如果倒回数据源，却保留崩溃时的计数，那{c['naive_overcount']}个事件就会被计两次："
        "这就是至少一次。<bookmark mark='e'/>如果跳过重放，它们就丢了：这就是至多一次。恰好一次，意味着状态和位置一起恢复。",
    "Inside, the state is now exact; outside, some results may":
        "在内部，状态现在是精确的；在外部，有些结果可能已经被看到了两次。<bookmark mark='a'/>一种修正是幂等的输出端。每个结果都以更新插入（upsert）的方式写入，以它的窗口和键为键，"
        "所以把同样的答案再写一遍，表不会有任何变化。<bookmark mark='b'/>另一种是事务性的输出端。自上一个检查点以来写出的一切，都进入一个读者看不到的未提交事务；检查点完成时，它就提交。"
        "<bookmark mark='c'/>崩溃之后，这个未提交的事务被中止，其中的记录重新写一遍，所以读者对每条记录只看到一次。<bookmark mark='d'/>这就是第39部分的两阶段提交，由检查点充当协调者；"
        "Kafka 在2017年有了它所需要的事务。",
    "So exactly-once is never the property of one component.":
        "所以，恰好一次从来不是某一个组件的性质。<bookmark mark='a'/>它需要一个能倒回到某个偏移量的数据源，这就是日志总是位于这些管道最前端的原因；需要与这些偏移量一起做检查点的状态；"
        "还需要一个幂等的或事务性的输出端。<bookmark mark='b'/>去掉任何一个，保证就不成立了：不能倒回的数据源会丢失事件，而发送电子邮件的输出端会把邮件发两次。<bookmark mark='c'/>即便如此，"
        "事件仍可能被处理不止一次；精确的是它们的效果。这就是第36部分 Saltzer、Reed 和 Clark 的端到端论证：保证只能在两端做出。",
    # ------------------------------------------------------------------ s07_sketches
    "Chapter six. Streaming algorithms in production.":
        "第六章：生产中的流式算法。",
    'f"The first question asked of a stream is often what':
        "对一条流提出的第一个问题，往往是什么最频繁。<bookmark mark='a'/>第20部分的 Misra 与 Gries 摘要只需一遍就能回答它，这里用{k - 1}个计数器，"
        "处理{N / 1000000.0:.1f}百万个词。<bookmark mark='b'/>它报告的每个计数都偏低，但至多偏低词的总数除以{k}，大约{bound / 1000:.0f}千，"
        "所以真实计数落在每个估计值上方的虚线框里，<bookmark mark='c'/>而任何比这更频繁的词都一定会被保留下来。<bookmark mark='d'/>在生产中，要紧的是这类摘要可以合并："
        "每个工作节点为每个窗口里自己的那个分区做摘要，这些摘要合并起来仍有同样的保证，正如 Pankaj Agarwal 和同事在2012年所证明的。",
    'f"Counting distinct items exactly needs memory for':
        "精确地统计不同元素，需要为每个元素都占用内存。<bookmark mark='a'/>第20部分的 HyperLogLog 只保留一些小寄存器，每个寄存器记录落进它的那些哈希值中最长的一串前导零。"
        "在语料的{h['distinct']:,}个不同的词上，它的误差从用{lo['bytes']:.0f}字节时的大约四分之一，降到用12千字节时的不到百分之一。<bookmark mark='b'/>用3千字节，"
        "词汇量的误差就在百分之零点二以内，还能同样统计出450万个不同的五词短语。<bookmark mark='c'/>两个草图合并时，在每个位置保留较大的那个寄存器，所以每小时的不同用户数可以汇总成每天的。"
        "<bookmark mark='d'/>数据仓库把这样的草图存在表里，BigQuery 的 HyperLogLog 函数就是这样做的。",
    'f"Latency is judged by its median and its':
        "评判延迟，看的是它的中位数和第99百分位数。<bookmark mark='a'/>Zohar Karnin、Kevin Lang 和 Edo Liberty 的 KLL 草图保留若干层样本，每一层的元素所代表的值，"
        "是下一层的两倍。在{q['n']:,}个模拟的延迟上，只保留{r0['stored']}个元素，它的中位数就很接近。<bookmark mark='b'/>但在远端的尾部，"
        "它的第99.9百分位数是{r0['estimates']['0.999']:.0f}，而真实值是{ex['0.999']:.0f}：按秩只错了百分之零点五，按值却不到真实值的一半。"
        "<bookmark mark='c'/>Ted Dunning 和 Otmar Ertl 的 t-digest 直接对付尾部，它的簇在中位数附近很大，在两端极小。KLL 保证的是秩；"
        "t-digest 则在延迟问题所关心的地方准确。",
    "Joining two streams is harder than joining two tables,":
        "连接两条流比连接两张表更难，因为哪一边都永远不完整。<bookmark mark='a'/>这里订单和付款按订单号连接，一笔付款如果在订单之后10分钟内到来，就算数。"
        "<bookmark mark='b'/>只要还可能有付款到达，每个订单就作为状态保存着。一旦水位线越过它之后的10分钟，这个订单就离开状态：或者已经连接上，或者在外连接中被单独输出。"
        "<bookmark mark='c'/>在那之后才来的付款，什么也找不到。<bookmark mark='d'/>所以状态的大小是事件速率乘以窗口长度。流与表的连接，表像第三章那样由它的变更日志保持最新，"
        "它保存的则是那张表。",
    "These sketches share the property that matters most in":
        "这些草图都具有在生产中最要紧的那个性质。<bookmark mark='a'/>每一个都可以在每个分区、每个窗口上分别构建，两个合并成一个后仍有同样的保证：把计数器相加，保留较大的寄存器，压实合并后的样本。"
        "<bookmark mark='b'/>所以一千个工作节点各自为自己的那份数据做草图，一棵合并树产生答案，而数据仓库可以每小时存一个草图，再按天或按年汇总。<bookmark mark='c'/>数据仓库，"
        "正是第七章接下来要去的地方。",
    # ------------------------------------------------------------------ s08_warehouse
    "Chapter seven. The warehouse.":
        "第七章：数据仓库。",
    "First, an argument about architecture. <bookmark mark='a'/>":
        "首先，是一场关于架构的争论。<bookmark mark='a'/>2011年，Nathan Marz 提出了后来被称为 Lambda 架构的方案：用批处理作业从整份日志重新计算每个答案；又因为批处理落后好几个小时，"
        "再并行运行一个流作业处理最近的部分，在查询时把两者合并。每个答案都要写两遍，写在两个必须彼此一致的系统里。<bookmark mark='b'/>2014年，Jay Kreps 问：为什么不只写一遍？"
        "在他的 Kappa 架构里只有流作业。要修改它，就启动第二个版本，从偏移量0开始读日志，让它追上来，再把读者切换过去。<bookmark mark='c'/>批不过是有界的流：有了事件时间窗口和重放，"
        "正如 Tyler Akidau 在2015年所论证的，流处理是批处理的超集。",
    "A warehouse exists because two kinds of question want":
        "数据仓库之所以存在，是因为两类问题需要不同的机器。<bookmark mark='a'/>业务数据库为联机事务处理（OLTP）而建，回答大量的小请求：取出1042号订单，修改它的数量，提交，在几毫秒内完成，"
        "只碰到按键找到的几行。<bookmark mark='b'/>分析问的恰恰相反：按产品汇总的销售额，覆盖有史以来的每一笔订单。Edgar Codd 在1993年把它命名为联机分析处理（OLAP）。"
        "每个查询读取每一行的两三列，什么也不写。<bookmark mark='c'/>放在同一个数据库上，长时间的扫描会让短事务饿死。所以业务系统把每一行的数据存放在一起，放在第35部分的 B 树里；而它的数据的一份副本，"
        "或成批载入，或从它的变更日志流过来，送进一个为扫描而建的数据仓库。",
    "Inside, the design Ralph Kimball set out in 1996 still":
        "在仓库内部，Ralph Kimball 在1996年提出的设计至今仍占主导。<bookmark mark='a'/>中心是一张事实表：每个业务事件一行，这里是一笔销售，存放你要加总的数字，以及键。它很窄，却有几十亿行长。"
        "<bookmark mark='b'/>围绕它的是维度表，描述谁、什么、哪里、何时：日期、门店、产品、顾客。它们很宽，满是文本，但很小。<bookmark mark='c'/>画出来，键从中心向外辐射，像一颗星，"
        "这个模式由此得名：星型模式。事实是你度量的东西；维度是你用来筛选和分组的东西。",
    "A typical question joins the facts to two dimensions: sales":
        "一个典型的问题把事实表与两个维度连接：某一年里按月份和类别统计的销售额。<bookmark mark='a'/>计划几乎是自己写出来的。筛选每个小维度，用留下来的行建一张哈希表，这就是第35部分的哈希连接。"
        "然后让巨大的事实表从这些哈希表旁边流过一遍，保留键命中的行，再分组。第11章正是把这件事分摊到许多台机器上。<bookmark mark='b'/>雪花模式把维度进一步规范化：产品表指向类别表，类别表再指向部门表。"
        "重复更少，连接更多。<bookmark mark='c'/>但维度都很小，重复很少有影响，所以大多数数据仓库保留更简单的星型。",
    "Dimensions change, slowly. <bookmark mark='a'/> A customer,":
        "维度会变，只是变得很慢。<bookmark mark='a'/>一位顾客 Ann，从利兹搬到了约克。她的那一行该怎么办？<bookmark mark='b'/>最简单的答案，Kimball 的第一类，直接覆盖城市。"
        "但这样一来，她在利兹的每一笔消费，现在都被报告成在约克的销售，而去年的报表再跑一遍，结果就变了。<bookmark mark='c'/>第二类保留历史。旧的那一行得到一个结束日期，新的一行开始，带着新的代理键42。"
        "每笔销售都指向它发生时为真的那个版本。<bookmark mark='d'/>维度变成了一份版本的日志，一张能说出任意日期什么为真的表，这正是第10章时间旅行的起点。",
    # ------------------------------------------------------------------ s09_columnar
    "Chapter eight. Columnar files.":
        "第八章：列式文件。",
    "A warehouse query reads a few columns of many rows, so store":
        "数据仓库的查询读取很多行的少数几列，所以按列来存表。<bookmark mark='a'/>一张小小的销售表。<bookmark mark='b'/>逐行写出，像业务数据库那样存放，每一行的值挨在一起。"
        "<bookmark mark='c'/>逐列写出，挨在一起的就变成了每一列的值。<bookmark mark='d'/>现在求总金额。行式布局要读每一行的每一个字节；列式布局只读连续的一段，占文件的四分之一，"
        "而且是顺序读取，第34部分说过，磁盘偏爱这种方式。<bookmark mark='e'/>而且一列里的值都是同一种类型，常常重复，比混杂的一行好压缩得多。C-Store 在2005年提出了这个论点。",
    "Parquet, created at Twitter and Cloudera in 2013, is the":
        "Parquet 于2013年诞生于 Twitter 和 Cloudera，如今大多数数据仓库和数据湖共用的就是这种列式文件。<bookmark mark='a'/>文件的开头和结尾都是4个魔数字节：P、A、R、1。"
        "在两者之间，行被切成行组，即可以并行读取的大块水平切片。<bookmark mark='b'/>在一个行组里，每一列是一个连续的列块。<bookmark mark='c'/>列块又分成页，页是编码和压缩的单位："
        "通常先是一个字典页，然后是数据页，每页包含一个小页头、级别和值。<bookmark mark='d'/>文件尾存着模式，以及每个列块的位置、编码和统计信息。读取器先取文件尾，再直接定位到它需要的那些列块。",
    "Each chunk then picks its encodings. <bookmark mark='a'/>":
        "然后每个列块选择自己的编码。<bookmark mark='a'/>这是一列词，按原样存储，每个字符串都完整写出。<bookmark mark='b'/>字典编码把每个不同的词在字典页里只存一次，"
        "再把每个值替换成它的小整数索引。<bookmark mark='c'/>索引所需的位数只取决于字典的大小，这里是两位，所以把它们按位打包：8个值占2个字节。<bookmark mark='d'/>排序之后，"
        "相等的索引挨在一起，第21部分的游程编码把每一段存成一个计数和一个值。<bookmark mark='e'/>而缓慢递增的时间戳，存下第一个值，再存一串小的差值：这就是增量编码。",
    "What do these save on real text? <bookmark mark='a'/> We":
        "这些编码在真实文本上能省多少？<bookmark mark='a'/>我们取小说中的30万个词作为一列。按原样存储，连同它们的长度，要占2.58兆字节。<bookmark mark='b'/>不同的词有30515个，"
        "所以索引需要15位；加上字典页，一共0.93兆字节，大约三分之一。单用 gzip 稍好一点，0.8。<bookmark mark='c'/>按阅读顺序，一个词几乎从不连续重复8次，所以游程编码毫无帮助。把这一列排序，"
        "游程编码就能让它减半，降到0.47，不到原样的五分之一。<bookmark mark='d'/>10万个时间戳从800千字节缩小到138千字节，每个11位。而且两者都只需简单的算术就能还原，解码比 gzip 便宜得多。",
    "Statistics give the largest saving of all: not reading.":
        "统计信息带来最大的节省：根本不读。<bookmark mark='a'/>这里有100万行，分成10个行组，还有一个查询，要找 x 在42万到43万之间的行。<bookmark mark='b'/>如果表按 x 排序，"
        "每个行组的最小值和最大值离得很近，只有一个行组与过滤条件重叠。另外9个连打开都不用就被跳过：过滤条件已经被下推到了扫描里。<bookmark mark='c'/>如果是随机顺序，每个行组几乎都跨越整个范围，"
        "10个都必须读。<bookmark mark='d'/>所以，只有当数据按人们用来过滤的列排序或聚集时，统计信息才有回报，这就是表的布局如此重要的原因。",
    # ------------------------------------------------------------------ s10_dremel
    "Chapter nine. Nested data in columns.":
        "第九章：列中的嵌套数据。",
    "Real data is rarely flat: logs and documents are records":
        "真实的数据很少是扁平的：日志和文档都是嵌套在记录里的记录。Dremel 是 Google 的交互式查询引擎，由 Sergey Melnik 和同事在2010年描述，它照样把这些记录存进了列里。"
        "<bookmark mark='a'/>这里有三本书，有重复的章节，每章又有重复的关键词。有一章没有关键词；有一本书没有章节。<bookmark mark='b'/>模式说明哪些字段是必需的，哪些会重复。"
        "<bookmark mark='c'/>取一列，chapters 点 keywords，写出它的值：sea、whale、inn、Highbury。结构不见了。哪些关键词同属一章，或者同属一本书？"
        "而且那个空的章节和那本空的书都消失了。每个值旁边的两个小数字，能把这一切都找回来。",
    "The first number is the repetition level. <bookmark":
        "第一个数字是重复级别。<bookmark mark='a'/>对每个值，它依次说明这个值是在路径上的哪个重复字段处重复。0表示开始了一条新记录。1表示同一本书里的一个新章节。2表示同一章里的又一个关键词。"
        "<bookmark mark='b'/>沿着这一列走一遍。sea 开始第一本书：0。whale 跟在它后面，在同一章里：2。inn 开始一个新章节：1。<bookmark mark='c'/>空的章节仍然需要一个位置，"
        "一个级别为1的空值；没有章节的那本书也一样，一个级别为0的空值。Highbury 开始一本新书：0。这条路径上有两个重复字段，所以级别从0到2。",
    "The second number, the definition level, says how much of":
        "第二个数字是定义级别，它说明路径中有多少部分存在。<bookmark mark='a'/>沿着 chapters 点 keywords，数一数那些可选的或重复的字段中，真正存在的有几个。"
        "<bookmark mark='b'/>一个真实的关键词，有它的章节，也有它自己：2，即最大值。<bookmark mark='c'/>空的章节存在，但没有关键词：1。没有章节的书两者都没有：0。"
        "<bookmark mark='d'/>所以空值从不作为一个值存储，只表现为一个低于最大值的级别，它准确地说明缺失的部分从哪里开始。由必需字段组成的列不需要定义级别，不在任何重复字段之内的列不需要重复级别，"
        "所以扁平的表什么代价也不用付。",
    "A reader rebuilds the records from the levels alone, without":
        "读取器只凭这些级别就能重建记录，根本不用看到那棵树。<bookmark mark='a'/>按顺序读这些数对。重复级别为0，就开始一条新记录。定义级别为0，表示这条记录没有章节，我们继续往下。否则，"
        "重复级别小于等于1就开一个新章节，定义级别为2就往里追加一个关键词。<bookmark mark='b'/>读完六个数对，三本书就原样回来了：前两章分别有两个和一个关键词，第三章是空的，一本空书，还有 Highbury。"
        "<bookmark mark='c'/>而且因为每一列都带着自己的级别，查询可以只重建它读取的那部分记录，其余部分完全不碰。",
    "Why is this worth the trouble? <bookmark mark='a'/> The":
        "为什么值得这么麻烦？<bookmark mark='a'/>级别是很小的整数，这里每个两位，像其他任何列一样按位打包、做游程编码；在规整的数据里它们几乎是常数，几乎不占空间。一个缺失的值只花费它的级别。作为回报，"
        "嵌套的记录获得了列存储的全部好处：关于关键词的查询只读关键词和它们的级别，别的什么都不读。<bookmark mark='b'/>Dremel 的论文报告说，在万亿行的表上做聚合只需几秒，"
        "这个系统后来成了 Google BigQuery 背后的引擎。<bookmark mark='c'/>Parquet 采用了同样的级别，存在每一个数据页里。在内存中，Apache Arrow 用另一种方式存放同样的树："
        "用指向子数组的偏移量，加上标记空值的位图。",
    # ------------------------------------------------------------------ s11_lakehouse
    "Chapter ten. Tables on object storage.":
        "第十章：对象存储上的表。",
    "A data lake is a folder of chapter eight's files in object":
        "数据湖就是对象存储里的一个文件夹，装着第八章的那些文件。这算是一张表吗？<bookmark mark='a'/>一个作业把它的输出写成三个文件。<bookmark mark='b'/>一个读者在写到一半时列出文件夹，"
        "看到的是两个，于是不声不响地算出了半个答案。<bookmark mark='c'/>崩溃的作业会把它的文件留在那里，而覆盖意味着先删除、再写入。第45部分的对象存储让每个对象都是原子的，但没有任何东西能跨越两个对象。"
        "而且列出一百万个文件需要一千次请求，一次接一次。",
    "Apache Iceberg, begun at Netflix, and Delta Lake, from":
        "始于 Netflix 的 Apache Iceberg 和来自 Databricks 的 Delta Lake 给出了同样的答案：把文件清单也存在文件里。<bookmark mark='a'/>在 Iceberg 中，"
        "一张表是一棵树：数据文件；列出它们的清单文件（manifest）；每个快照一个清单列表；以及一个存放模式和历史的元数据文件。一次提交自底向上写出新文件，不改动任何已有文件。"
        "<bookmark mark='b'/>然后它在目录服务（catalog）里切换一个指针，从旧的元数据文件指向新的。这一个原子步骤就是提交：读者要么看到全部，要么什么也看不到。"
        "<bookmark mark='c'/>新快照复用旧的清单文件，所以一次提交只需几个小文件。<bookmark mark='d'/>清单文件还记录各列的取值范围，所以查询规划器不用列出任何东西就能剪掉文件。",
    "Delta Lake keeps the same information as a log. <bookmark":
        "Delta Lake 把同样的信息存成一份日志。<bookmark mark='a'/>数据旁边的一个文件夹里存着编了号的提交，每个提交列出新增和删除的文件。<bookmark mark='b'/>按顺序重放，"
        "就得到这张表：两个文件，然后第三个，然后前两个被压实成一个，然后又一个。表是对它的日志的一次折叠，也就是第三章的事件溯源，只不过就存在对象存储本身里。<bookmark mark='c'/>每10次提交，"
        "一个 Parquet 检查点记录下折叠后的状态，所以读者只需重放其后的部分。<bookmark mark='d'/>而提交意味着创建下一个编号，前提是还没有人创建过：这是一次条件写入，S3 从2024年起提供了这种功能。",
    "Two jobs commit to the same table at once. <bookmark":
        "两个作业同时向同一张表提交。<bookmark mark='a'/>两者都读取了版本41，不加锁地工作，只在提交时检查：这就是第35部分 Kung 和 Robinson 的乐观并发控制。"
        "<bookmark mark='b'/>作业 A 先完成，创建了版本42。作业 B 也尝试42，失败了：这个名字已被占用。<bookmark mark='c'/>B 读取 A 提交的内容。"
        "如果 A 没有碰过 B 读过或重写的任何东西，比如两者都只是追加，B 就以43重试，只写一条新的日志项。<bookmark mark='d'/>如果 A 重写了 B 读过的文件，B 的工作就过时了，必须重做。",
    "How much does contention cost? <bookmark mark='a'/> Our":
        "争用的代价有多大？<bookmark mark='a'/>我们的仪器模拟一些写入者，每个提交50次，每次提交前做随机长度的工作，平均一个单位。<bookmark mark='b'/>当每次提交都冲突时，"
        "失败者要重做它们的工作。16个写入者时，每次提交要重试将近4次，而16个写入者的提交速率还不到1个写入者的3倍。<bookmark mark='c'/>当写入者只追加时，失败者只需重新编号，"
        "16个写入者的提交速度是1个的11倍。所以，让并发的写入者只做追加，或者去碰不同的分区。",
    "Because commits never change old files, every old version is":
        "因为提交从不改动旧文件，每个旧版本都还在。<bookmark mark='a'/>在 Spark SQL 中，两种格式都可以按某个版本或某个时间戳来读取，从一个较早的快照开始。"
        "<bookmark mark='b'/>一次错误的写入，可以通过恢复到更早的版本来撤销，而恢复本身又是一次新的提交。审计可以问一份报表在去年三月看到的是什么，模型可以用它们最初见到的数据重新训练。"
        "<bookmark mark='c'/>之后，一次清理（vacuum）会删除近期任何快照都不再需要的文件。<bookmark mark='d'/>Armbrust 和同事在2021年给这个结果起了名字："
        "湖仓（lakehouse），在廉价存储上的开放文件之上，提供数据仓库的保证。",
    # ------------------------------------------------------------------ s12_mpp
    "Chapter eleven. Queries on a thousand machines.":
        "第十一章：千台机器上的查询。",
    "A warehouse query is too big for one machine, so it runs on":
        "数据仓库的查询对一台机器来说太大了，所以它要在许多台机器上运行。<bookmark mark='a'/>表的文件分散在各个工作节点上，协调节点把执行计划切成若干片段，每个工作节点都在自己的那一份数据上运行这些片段。"
        "<bookmark mark='b'/>每个工作节点先按门店统计自己的行数，这是一次部分聚合，于是它发送的是三个数字，而不是它的那些行。<bookmark mark='c'/>接着，一个交换（exchange）"
        "算子把每个门店哈希到一个工作节点，由它把这个门店的部分计数加起来：这就是第39部分 MapReduce 的洗牌，只不过发生在一个查询内部。<bookmark mark='d'/>协调节点收集答案。"
        "DeWitt 的 Gamma 机器在1986年就是这个形状；今天的 Redshift、BigQuery、Snowflake 和 Trino 也是。",
    "Joins are where the network bill comes from: a big table, B,":
        "网络账单来自连接（join）：一张大表 B，在 N 个工作节点上与一张小表 S 相连接。<bookmark mark='a'/>广播连接把 S 的一整份副本发给每个工作节点。B 从不移动；"
        "每个工作节点用第35部分的哈希连接，把自己那一份 B 与这份副本连接起来。代价是 S 的行数，乘以 N。<bookmark mark='b'/>洗牌哈希连接按连接键把两张表都重新分区，让匹配的行在同一个工作节点上相遇。"
        "只有当一行本来就位于正确的工作节点上时，它才留在原地，这种情况是 N 次里有1次，所以代价是 B 加 S，再乘以1减 N 分之一。",
    "Which is cheaper? <bookmark mark='a'/> In our cost model B":
        "哪个更便宜？<bookmark mark='a'/>在我们的代价模型里，B 有10亿行，每行100字节，有100个工作节点，S 从1万行增长到1亿行。"
        "<bookmark mark='b'/>广播的代价随 S 成十倍地增长。洗牌无论 S 多大，都要花大约100吉字节，因为 B 占了大头。<bookmark mark='c'/>令两种代价相等："
        "只要 S 小于大约 B 除以 N，广播就更划算，这里是1000万行，即 B 的百分之一。<bookmark mark='d'/>优化器根据估计的大小来选择，而且很谨慎，因为每个工作节点都必须把副本放在内存里："
        "Spark 默认只广播它估计小于10兆字节的表。一个错误的估计，也就是第35部分对大小的猜测，会让任何一种选择都变成灾难。",
    'f"Hashing spreads keys evenly, not rows. <bookmark':
        "哈希让键均匀分布，而不是让行均匀分布。<bookmark mark='a'/>如果某个键很热，它的所有行都会去往同一个工作节点。<bookmark mark='b'/>我们测了一下：16个工作节点上有20万行，"
        "其中一个键占了五分之一。最忙的工作节点分到的几乎是它应得份额的4倍，而一个查询只有在最慢的工作节点完成时才算完成。第39部分的备份任务帮不上忙：那个工作节点并不慢，只是它的那一份太大了。"
        "<bookmark mark='c'/>解决办法是加盐（salting）：把热键拆成8个随机的子键，并把小表一侧与它匹配的行复制8份。现在，"
        "最慢的工作节点承担的是理想值的{s['slowdown_salted']:.1f}倍。<bookmark mark='d'/>第六章的高频项（heavy hitter）草图能廉价地找出热键，"
        "而 Spark 的自适应执行会在查询运行时拆分倾斜的分区。",
    "Inside each worker, how operators pass data matters as much":
        "在每个工作节点内部，算子之间如何传递数据，和网络同样重要。<bookmark mark='a'/>第35部分的迭代器模型，也就是 Volcano 的模型，每次调用传递一行：每一行、每一个算子，都要一次函数调用和一次分支。"
        "<bookmark mark='b'/>向量化执行来自2005年的 MonetDB X100，它传递的是一批数据：每一列大约一千个值，在 DuckDB 里是2048个。"
        "<bookmark mark='c'/>过滤器在价格列上跑一个紧凑的循环，写出一个选择向量，也就是通过过滤的那些位置；求和只读取金额列中这些位置上的值。"
        "<bookmark mark='d'/>没有函数调用的循环会变成第24部分的 SIMD 指令，而且常常作用在第八章的字典编码上。另一种答案来自 HyPer：把每个查询编译成机器码。",
    # ------------------------------------------------------------------ s13_quality
    "Chapter twelve. Data you can trust.":
        "第十二章：值得信赖的数据。",
    "The first threat to a pipeline is its input changing shape.":
        "对一条管道的第一个威胁，是它的输入改变了形状。<bookmark mark='a'/>订单记录多了一个货币字段；去年的记录没有它。<bookmark mark='b'/>向后兼容问的是：新的读者能否读取旧数据？能，"
        "因为新字段有默认值，由读者填上。向前兼容问的是：旧的读者能否读取新数据？同样能；它们会跳过自己不认识的字段。<bookmark mark='c'/>Avro 的规则对每一种改动都有定论。没有默认值的字段会破坏向后兼容，"
        "把整数加宽会破坏向前兼容，而重命名两者都会破坏。<bookmark mark='d'/>模式注册表（schema registry）会在生产者使用每个新版本之前，按其主题的规则检查它，默认是向后兼容。"
        "而 Iceberg 用编号来指代列，所以在那里重命名是安全的：这就是第43部分的 API 演进，用在了数据上。",
    "Most pipelines begin in a database that another team owns.":
        "大多数管道都起始于另一个团队拥有的数据库。<bookmark mark='a'/>订单服务写入它的表，并通过第三章的发件箱，把变更发布到一个主题。<bookmark mark='b'/>数据契约让这个接口变得明确，"
        "就像 API 一样：字段和类型；含义，比如金额以便士为单位、含税；新鲜度；归属；以及允许哪些改动。<bookmark mark='c'/>消费者在契约之上构建，从不依赖这个服务的内部表。"
        "<bookmark mark='d'/>现在，一位开发者把 amount 改名为 total。契约在生产者的持续集成中接受检查，所以这次改动在那里、在部署之前就失败了，而不是三天后才在某个仪表盘上暴露出来。"
        "破坏性的改动需要一个新版本，与旧版本并行运行。",
    "Contracts say what data should be; tests check what it is.":
        "契约说的是数据应该是什么样；测试检查的是它实际是什么样。<bookmark mark='a'/>dbt 用 SQL 构建数据仓库的表，在 dbt 里，测试就放在每张表旁边：这个键唯一，而且从不为空；这个状态只取这几个值；"
        "每个客户都存在于客户表中。<bookmark mark='b'/>每个测试都会编译成一个查询，找出违反它的行；查询什么都没返回，测试就通过。<bookmark mark='c'/>在第十三章的小说流上运行这样的测试。"
        "唯一性测试找出了被发送两次的两本书。把单词总数与数据源对账，能抓出不去重的管道，它高了将近百分之七；也能抓出过早的水位线，它低了百分之十。<bookmark mark='d'/>数据量和新鲜度检查，"
        "能抓住那些没人为之写过规则的故障。",
    "Tables are built from tables, and their dependencies form a":
        "表由表构建而成，它们的依赖构成一张图。<bookmark mark='a'/>数据源供给暂存表，暂存表供给分析师查询的数据集市，数据集市再供给仪表盘、模型和报表。dbt 从每个模型的 SQL 里的引用读出这张图，"
        "并按拓扑顺序构建：这就是第41部分的构建系统，只是用表代替了文件。<bookmark mark='b'/>现在，暂存的支付表上有一个测试失败了。沿着边向前走，这张图会列出现在所有可疑的东西；这些构建会停下来，"
        "它们的负责人会收到通知。<bookmark mark='c'/>沿着边向后走，就会走向原因：支付接口。<bookmark mark='d'/>列级血缘能把范围进一步缩小，"
        "而 OpenLineage 标准让引擎在运行时报告这些边。",
    "Tests help most before anyone reads the data. <bookmark":
        "测试在任何人读取数据之前最有用。<bookmark mark='a'/>第十章的表让这件事变得廉价：一个作业写出它的新快照，但不发布它，读者看到的仍是版本41。"
        "<bookmark mark='b'/>测试在这个暂存的快照上运行。如果通过，发布就是一次原子的指针交换，每个读者同时切换到版本42。<bookmark mark='c'/>如果失败，这个快照永远不会被发布，"
        "读者继续使用上一个好的版本。这就是写入、审计、发布（write, audit, publish），Iceberg 用表的分支来支持它。<bookmark mark='d'/>所以，信任是工程造出来的："
        "在数据产生的地方有契约，每一步都有测试，有血缘来追踪故障，还有原子的发布。",
    # ------------------------------------------------------------------ s14_job
    "Chapter thirteen. The Job as a stream.":
        "第十三章：作为流的那项任务。",
    "The Job, one last time in a new shape. <bookmark mark='a'/>":
        "那项任务，最后一次，换一个新的形状。<bookmark mark='a'/>30部小说以流的形式到达，每本书一个事件，每个事件携带它的词，以及它在出版时间表中的位置，作为它的事件时间。"
        "<bookmark mark='b'/>大多数书在应到时间之后一两秒到达。有3本迟到了20秒，就像来自一部曾经离线的手机。<bookmark mark='c'/>还有2本被发送了两次，因为生产者重试了。"
        "要做的是一个前20名，它在每一刻都正确，并且最终与前面每一部分的批处理答案相同。",
    'f"We ran three pipelines over the same stream.':
        "我们在同一条流上运行了三条管道。<bookmark mark='a'/>第一条按书去重，并把计数保存为状态：它数出{r['exactly once']['total']:,}个词，它的前20名与批处理答案完全一致。"
        "<bookmark mark='b'/>第二条不去重。被发送两次的两本书被数了两次，得到{r['no dedup']['total']:,}个词，计数是错的。"
        "<bookmark mark='c'/>第三条使用一个等待5秒的水位线，并丢弃更晚到达的一切，所以那3本迟到的书不见了：{r['watermark lag 5 s']['total']:,}个词。"
        "<bookmark mark='d'/>流的状态是对其事件的一次折叠，对每个键只应用一次，并与数据源的偏移量一起做检查点。而且因为这个前20名是针对全部时间的，它根本不需要水位线；如果是按窗口的答案，"
        "就要面对第四章那个选择：要么等待，要么出错。",
    'f"The ledger gets row seventeen. <bookmark':
        "账本添上第17行。<bookmark mark='a'/>在一台机器上作为流的那项任务：处理全部30本书大约要{row['seconds']:.0f}秒，已去重，结果精确。"
        "<bookmark mark='b'/>它比最好的那几行批处理要慢，因为它做了一条流所需要的记账工作。它换来的是一个每处理完一本书就是最新的答案，而不是等到最后一本之后才有。",
    # ------------------------------------------------------------------ s15_frontier
    "Chapter fourteen, the frontier. Can every query be kept up":
        "第十四章：前沿。每个查询都能被廉价地保持最新吗？",
    "Streams and tables are converging. <bookmark mark='a'/> Take":
        "流和表正在趋于融合。<bookmark mark='a'/>取一个针对表的查询，有连接、过滤、计数，并要求它的答案随着行的到达始终保持最新。<bookmark mark='b'/>不是重新运行它，"
        "而是把每个变更作为一个增量（delta）推过执行计划：一条新订单变成一条连接后的行，它要么通过过滤，要么不通过，并让某一个计数改变1。这就是增量视图维护，它的承诺是工作量与变更成正比，而不是与数据成正比。"
        "<bookmark mark='c'/>Frank McSherry 和同事在2013年提出的差分数据流（differential dataflow），把它推广到了迭代和递归的计算；"
        "Mihai Budiu 和同事在2023年提出的 DBSP，给出了一套代数，能让任何流式查询变成增量的。<bookmark mark='d'/>哪些查询能被廉价地维护、需要多少状态，仍是未解决的问题；对于某些连接，"
        "可以证明，做不到。",
    'f"How small can a summary of a stream be? <bookmark':
        "一条流的摘要能有多小？<bookmark mark='a'/>这是对20万个延迟值做的一个 KLL 草图。保留其中{q['rows'][0]['stored']}个，它给出的中位数与真实排名相差约百分之一以内；"
        "保留{q['rows'][-1]['stored']:,}个，就在百分之零点零几以内。<bookmark mark='b'/>KLL 由 Zohar Karnin、"
        "Kevin Lang 和 Edo Liberty 在2016年提出，它在常数因子以内是最优的：在最坏情况下，没有任何摘要能做得好很多。<bookmark mark='c'/>像这样的下界，"
        "从1996年 Noga Alon、Yossi Matias 和 Mario Szegedy 的工作开始，在任何东西建成之前，就告诉设计者什么是不可能的。<bookmark mark='d'/>未解决的问题仍然存在："
        "在尾部，那里相对精度最要紧；在既能合并、又能保护隐私的草图上；以及在能回答连接的摘要上。",
    'f"The deepest limit is time. <bookmark mark=':
        "最深的极限是时间。<bookmark mark='a'/>水位线是一个猜测：猜不会再有更早的事件到达，而每一种等待多久的选择，都是在完整性和延迟之间做权衡：从两秒内得到五分之四的事件，到一分钟后只差一个事件。"
        "<bookmark mark='b'/>先早早回答，再加以修正，就能摆脱这种权衡：一个5秒的水位线，加上允许一分钟的迟到，触发了{al['refinements']}次修正，最终每个窗口都是精确的。代价是状态，"
        "以及必须接受修正的消费者。<bookmark mark='c'/>有保证的水位线，从测得的延迟推导出来；以及一套所有引擎都认同的流式 SQL 语义：这些都是未解决的问题。",
    "Open problems. <bookmark mark='a'/> Which queries can be":
        "未解决的问题。<bookmark mark='a'/>哪些查询能被增量地维护，时间与每次变更成正比，又需要多少状态。<bookmark mark='b'/>有保证的水位线，从测得的延迟推导出来，而不是靠猜。"
        "<bookmark mark='c'/>小的摘要，能以有界的误差回答连接和分组（group-by）。<bookmark mark='d'/>还有从工作负载中学习出来的布局：一张表应该采用哪种排序顺序、分区方式和编码。"
        "<bookmark mark='e'/>这一部分的研究题问的是：哪些按窗口的流连接能被精确地维护，而所用空间的增长比窗口本身更慢。",
    # ------------------------------------------------------------------ s16_outro
    "What we built in this part. A partitioned log, where order":
        "这一部分我们构建了什么。一个分区日志，其中顺序按键保持，消费者组分担各个分区；还有一个压实后的日志，它用50条记录而不是2000条，重建出同样的状态。作为事件折叠的状态。基于事件时间的窗口，"
        "以及在完整性和延迟之间做权衡的水位线，除非答案允许事后修正。屏障快照，让一次计算可以崩溃，再以恰好一次的状态恢复。列式文件，它的字典和游程让一列词只占原来大小的一小部分；还有 Dremel 的两种级别，"
        "把嵌套记录放进扁平的列。一个思想贯穿其中：按顺序、只记录一次发生了什么，那么每个答案都能被推导出来，并且能再推导一次。",
    "Where this comes back. Part 47 builds a search index from a":
        "这些内容会在哪里再出现。第47部分从一个文档日志构建搜索索引，并让它保持最新。第48和49部分用这些部件设计信息流、时间线和分析系统。第50部分把日志、指标和追踪用在运行中的系统本身。第57部分会问，"
        "在这种规模的数据上能学到什么；第55部分则问，要信任交付这些数据的管道，需要做到什么。",
    "In practice. Key a log by whatever must stay in order, give":
        "实践中。用必须保持顺序的那个东西作为日志的键，为未来留出足够的分区，并压实那些保存状态的日志。按事件时间给流开窗，有意识地选择它们的迟到容许，并把结果写入能容忍重复的输出端。从数据库的日志或发件箱捕获变更，绝不靠写两次。"
        "把表存成列式文件，按人们最常用的过滤条件排序或聚簇。还有，广播连接中较小的一侧，并在热键找上你之前先找到它们。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：给我们的流处理器加上滑动窗口和允许迟到，并测量它需要保存多少状态。最后一道标有星号，是研究题：在一条流的窗口上，哪些连接能被精确地维护，"
        "而所用内存比窗口本身更少。",
    "Next time, Part 47: search engines. How do you find the ten":
        "下一次，第47部分：搜索引擎。如何在五分之一秒内，从几十亿个网页中找出最相关的十个？倒排索引把搜索变成合并有序列表，压缩让它们留在内存里，一个关于相关性的概率模型给出 BM25，而一个随机冲浪者给出 PageRank。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
