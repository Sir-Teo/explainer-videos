"""Chinese narration for cs47: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第47部分：搜索引擎"

CHAPTERS = {
    "Hook": "数十亿网页中的十个",
    "Text": "1. 词、词干与齐普夫",
    "Index": "2. 倒排索引",
    "Boolean": "3. 合并倒排表",
    "Compression": "4. 压缩倒排表",
    "Ranking": "5. 从 tf-idf 到 BM25",
    "Evaluation": "6. 这个排序好吗？",
    "Topk": "7. 快速求前 k 名",
    "Links": "8. 链接与随机冲浪者",
    "Crawl": "9. 爬取网页",
    "Serving": "10. 大规模服务",
    "Spelling": "11. 拼写纠错与自动补全",
    "Ltr": "12. 排序学习",
    "Dense": "13. 稠密检索",
    "Engine": "14. 为小说打造的搜索引擎",
    "Frontier": "15. 前沿：检索及其极限",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "How do you find the ten most useful pages among hundreds of":
        "如何在几分之一秒内，从几千亿个网页中找出最有用的十个？<bookmark mark='a'/>第一个搜索引擎 Archie 于1990年在麦吉尔大学写成，它索引的是 FTP 服务器上的文件名，而不是文件的内容。"
        "到1994年，已经有了网络爬虫和网页目录；1995年，AltaVista 能快速地搜索整个网络的全文。<bookmark mark='b'/>1998年，"
        "谢尔盖·布林（Sergey Brin）和拉里·佩奇（Larry Page）描述了 Google：它把网页之间的链接当作投票，起步时的索引有2400万个网页。"
        "<bookmark mark='c'/>今天的索引容纳几千亿个网页，给它们排序时，除了词，还要用学习得到的模型和稠密向量。",
    "A search engine rests on five ideas, and each is a piece of":
        "搜索引擎建立在五个思想之上，每一个都是这个系列遇到过的一段数学。<bookmark mark='a'/>倒排索引把一次查询变成对有序列表的合并。<bookmark mark='b'/>压缩让这些列表小到可以放进内存。"
        "<bookmark mark='c'/>一个关于“相关”含义的概率模型，给出了名为 BM25 的排序公式。<bookmark mark='d'/>一个在链接之间漫游的随机冲浪者，给出了 PageRank。"
        "<bookmark mark='e'/>而向量把文档放在意思相同的查询附近，并通过在一张图上搜索找到它们。",
    'f"In this part we build one, for the thirty novels':
        "在这一部分里，我们为这个系列的30部小说建造一个。<bookmark mark='a'/>小说被切成{ix['docs']:,}个400词的段落，并建立索引：{ix['terms']:,}个不同的词项，"
        "{ix['postings']:,}个倒排项。<bookmark mark='b'/>向它查询 white whale，也就是白鲸，它就给段落排序，并为每一段显示匹配词周围的一段摘要。"
        "<bookmark mark='c'/>到这一部分结束时，其中每一步都会是我们自己的：分词器、索引、压缩、排序，以及对排序好坏的评估。",
    "This is Part 47 of Computer Science, Built. <bookmark":
        "这是计算机科学，从零搭建，第47部分。<bookmark mark='a'/>我们会在小说上拟合齐普夫定律和 Heaps 定律；建立倒排索引，并用尽可能少的比较求它的列表的交集；用长度由我们推导出来的编码压缩这些列表；"
        "从一个相关性模型推导出 BM25，并测量它；用 WAND 跳过大部分工作；用随机游走给网页排序；找出近似重复；还要按意思搜索，向量用乘积量化压缩，再通过一张分层的图来搜索。",
    # ------------------------------------------------------------------ s02_text
    "Chapter one. Words, stems and Zipf.":
        "第一章：词、词干与齐普夫。",
    "A search engine sees characters, and its first job is to":
        "搜索引擎看到的是字符，它的第一项工作是确定哪些是词。<bookmark mark='a'/>我们的分词器保留连续的字母和数字，并把它们转成小写，这样句首的 Whale 和句中的 whale 就成了同一个词项。"
        "大小写折叠是有代价的：它也把国名 US 和 us 合并了。<bookmark mark='b'/>接下来是停用词，48个短词，比如 the、of 和 a。在简·奥斯汀（Jane Austen）的第一句话里，"
        "它们占了23个词元中的12个。我们的索引保留它们，因为短语查询需要它们，但排序查询会把它们丢掉。<bookmark mark='c'/>最后，词干提取把每个词削成一个词干，"
        "于是 acknowledged、acknowledges 和 acknowledging 都变成同一个词项。",
    "Martin Porter published his stemmer in 1980, and it is still":
        "Martin Porter 在1980年发表了他的词干提取器，至今仍广泛用于英语。<bookmark mark='a'/>它不用词典：大约60条后缀规则，分5步，按顺序应用。跟着 generalizations 走一遍。"
        "第一步去掉复数。第二步把 ization 变成 ize，第三步把 alize 变成 al，第四步去掉 al，剩下 gener。<bookmark mark='b'/>一条规则只有在词剩下的部分足够长时才能触发。"
        "Porter 用元音—辅音对的个数来度量一个词干：gener 有两对，所以它的 al 可以去掉；而 riv 只有一对，所以 rival 保留词尾。"
        "<bookmark mark='c'/>我们的实现重现了全部20个已发表的例子。它把 whaling 和 whales 合并成 whale，"
        "把 connection、connected 和 connecting 合并成 connect。<bookmark mark='d'/>它也会出错：general 和 generous 都变成 gener，"
        "而 ran 永远遇不到 run。词形还原器带着一部词形词典，能修正这两个问题，但要付出代价。",
    "Now count. The thirty novels hold four and a half million":
        "现在来计数。30部小说共有450万个词元，61720个不同的词。<bookmark mark='a'/>最常见的 the 出现了23万次：每20个词元就有一个。前20个词占了全部文本的将近三分之一。"
        "<bookmark mark='b'/>把频率对排名作图，两个轴都取对数刻度，点就落在一条直线附近。这就是齐普夫定律：George Kingsley Zipf 在20世纪30和40年代描述了它，"
        "频率大致与排名的倒数成正比。在排名10到1万之间拟合，我们的直线斜率是负1.21。<bookmark mark='c'/>在另一端，22888个词，超过词汇表的三分之一，恰好只出现一次。"
        "所以索引必须既能廉价地处理少数巨大的倒排表，也能廉价地处理数量庞大的极小倒排表。",
    "How fast does the vocabulary grow as we read? <bookmark":
        "我们读得越多，词汇量增长得有多快？<bookmark mark='a'/>这是见过的不同词的数目，对读过的词元数作图，一部小说接一部小说。它先陡峭上升，然后越来越慢，但从不趋于平坦：每本书都带来新的名字和新的词。"
        "<bookmark mark='b'/>Gustav Herdan，以及后来的 Harold Heaps，把它描述为一个幂律：词汇量的增长等于一个常数乘以词元数的 β 次方。我们拟合得到的 β 是0.485，"
        "接近二分之一，所以文本增加到100倍，词汇量大约增加到10倍。<bookmark mark='c'/>末尾的跳跃是《尤利西斯》（Ulysses），它在我们的顺序中排在最后，新词也最丰富。"
        "<bookmark mark='d'/>词干提取让词汇量减少三分之一，降到40692个词项。这些词项就是下一章的词典。",
    # ------------------------------------------------------------------ s03_index
    "Chapter two. The inverted index.":
        "第二章：倒排索引。",
    "Without an index, every query must read all four and a half":
        "没有索引，每次查询都必须读完小说的全部450万个词元。<bookmark mark='a'/>不妨想象一张表：每个词项一行，每个段落一列，在词项出现的地方做上标记。对我们的小说来说，这是40692行乘11261列："
        "4.58亿个格子。<bookmark mark='b'/>其中只有236万个被标记，大约百分之零点五。<bookmark mark='c'/>所以只保留标记：对每个词项，保留包含它的那些段落的有序列表，"
        "叫作它的倒排表（postings）。文本侧过来，就变成了一个倒排索引：从词到段落。",
    "An inverted index has two parts. <bookmark mark='a'/> The":
        "倒排索引有两部分。<bookmark mark='a'/>词典保存每个词项，连同它的文档频率，即包含它的段落数，以及它的列表开始的位置。whale 出现在390个段落里，Ahab 出现在181个段落里。"
        "词典可以是第17部分的哈希表，也可以是一棵有序的树，后者还支持前缀搜索。<bookmark mark='b'/>倒排表按递增顺序保存段落编号，每个编号都带着词项出现的位置。后面几章都依赖这个顺序：有序列表可以合并，"
        "相邻的编号彼此接近。<bookmark mark='c'/>whale 以一串连续的编号开头，从段落659到669：那是《白鲸》（Moby-Dick）的开头，有好几页关于鲸的引文。词会聚集，而聚集的东西可以压缩。",
    "How is the index built? The simplest way is to sort.":
        "索引是怎么建起来的？最简单的办法是排序。<bookmark mark='a'/>按顺序读段落，为每个段落里的每个词项记下一对：词项和段落编号。<bookmark mark='b'/>把这些对按词项排序，"
        "同一个词项之内再按段落排序。<bookmark mark='c'/>现在每个词项的对都挨在一起，依次读出它们，就得到它的倒排表，而且已经有序。小说产生236万对；每对8字节，就是19兆字节，在内存里排一次序就够了。"
        "<bookmark mark='d'/>一次网络爬取产生的对，远远多于任何内存能容纳的数量。所以能装下多少就排多少，把每个排好序的块作为一个归并段写到磁盘，再合并这些归并段：原封不动的第16部分的外部排序。"
        "这就是基于块的排序索引构建。",
    "Blocked sorting needs a table from every term to an integer,":
        "分块排序需要一张从每个词项到一个整数的表，并且始终留在内存里；而且它要排序的那些对，本可以在到达时就分好组。<bookmark mark='a'/>单遍内存式索引构建，"
        "由 Steffen Heinz 和 Justin Zobel 在2003年描述，改用一个哈希表。每个词项映射到一个不断增长的列表，而且因为段落按顺序到达，每个列表生来就是有序的。"
        "<bookmark mark='b'/>内存满了，就把词项排序，把这个块写到磁盘，然后表清空，重新开始。<bookmark mark='c'/>最后，像第16部分那样，一次性合并所有的块。"
        "我们自己的构建器就是只有一个块的这个算法：对每个段落只扫一遍。",
    "Real collections change. <bookmark mark='a'/> New documents":
        "真实的文档集合会变化。<bookmark mark='a'/>新文档进入内存中的一个小索引，与其他索引并排被搜索；它满了，就作为一个段写出去。<bookmark mark='b'/>大小相同的段会被合并，"
        "就像二进制计数器的进位，所以每个倒排项只被复制对数次。<bookmark mark='c'/>被删除的文档在一个位图里做标记，并在下一次合并时丢掉。"
        "Lucene 是 Elasticsearch 和 OpenSearch 底下的库，它把索引保存为不可变的段，大体就以这种方式合并：这正是第34部分日志结构合并树的设计。",
    # ------------------------------------------------------------------ s04_boolean
    "Chapter three. Merging postings.":
        "第三章：合并倒排表。",
    "A query for whale and sea wants the passages on both":
        "查询 whale 和 sea，要的是同时出现在两个倒排表上的段落。<bookmark mark='a'/>因为两个列表都有序，走一遍就能找出它们。在每个列表上各放一根手指，比较两个数。如果相等，这个段落就是一个答案，"
        "两根手指都前进；如果不等，指着较小数的那根手指前进。<bookmark mark='b'/>每次比较至少让一根手指前进，所以这一遍的代价至多是两个列表长度之和。"
        "<bookmark mark='c'/>同样的走法也能计算 OR，保留它经过的一切，以及 AND NOT。超过两个词项时，从最短的列表开始，因为交集只会越变越小。",
    "When one list is much longer than the other, most of the":
        "当一个列表比另一个长得多时，沿着它走的大部分路程都是浪费。<bookmark mark='a'/>所以加上捷径。在一个有 n 个倒排项的列表里，每隔根号 n 个倒排项，就有一个同时指向前方根号 n 处。"
        "前进之前先查看捷径：如果它的目标仍不大于另一个列表的当前段落，就跳过去。<bookmark mark='b'/>平方根平衡了两种代价：捷径越多，占的空间和要做的检查就越多；捷径越长，越过头的次数就越多。"
        "Alistair Moffat 和 Justin Zobel 在1996年研究了压缩倒排表中的跳跃。<bookmark mark='c'/>在小说上，"
        "查询 the AND whale 的比较次数从11137次降到1790次。",
    "Galloping, from Part 24, goes further. <bookmark mark='a'/>":
        "第24部分的倍增查找走得更远。<bookmark mark='a'/>依次取短列表里的每个段落，在长列表里找它：向前探1个位置，然后2个、4个、8个、16个，不断加倍，直到某次探测越过头。"
        "<bookmark mark='b'/>然后在最后一段间隔里做二分查找。Jon Bentley 和 Andrew Yao 在1976年描述了这种无界查找。"
        "<bookmark mark='c'/>用这种方法在长度为 n 的列表里找 m 个元素，代价大约是 m 乘以 n 除以 m 的对数，当 m 很小时远少于逐个走。the AND whale 现在只需1418次比较；"
        "love AND marriage 需要1915次，而合并需要2680次。",
    "Here are all three on five queries over the novels.":
        "这是三种方法在小说的5个查询上的表现。<bookmark mark='a'/>当两个列表长度相近时，比如 whale 和 sea，或者 Elizabeth 和 Darcy，合并或跳跃获胜，倍增查找则白白浪费了它的探测。"
        "<bookmark mark='b'/>当一个列表长5倍或29倍时，倍增查找获胜，在 the AND whale 上快了将近8倍。<bookmark mark='c'/>所以搜索引擎按长度之比来选择，或者使用自适应算法，"
        "比如 Erik Demaine、Alejandro López-Ortiz 和 Ian Munro 的算法，它们在任何组合上都表现良好。而且比较次数并不是全部代价：第24部分的无分支循环，"
        "以及一次比较多个编号的 SIMD 指令，同样重要。",
    "Some queries are phrases: white whale, the two words":
        "有些查询是短语：white whale，两个词相邻且有序。<bookmark mark='a'/>这就是我们的倒排表保留位置的原因。先像之前那样求段落列表的交集。然后，在每个同时含有两个词的段落里，"
        "把 whale 的每个位置往回移一位，再与 white 的位置求交集。<bookmark mark='b'/>每个留下来的位置，都是这个短语开始的地方。<bookmark mark='c'/>在小说里，"
        "有125个段落同时含有 white 和 whale，但只有64个含有这个短语。有3个段落含有 call、me 和 Ishmael，而恰好只有一个含有这个短语：第一章的第一行。"
        "<bookmark mark='d'/>位置并不是免费的：一共有450万个，另外还有240万个段落编号。下一章把这一切都变小。",
    # ------------------------------------------------------------------ s05_compression
    "Chapter four. Compressing postings.":
        "第四章：压缩倒排表。",
    "Chapter two's index holds two point three six million":
        "第二章的索引有236万个倒排项：作为32位整数，光是文档编号就占9.5兆字节，而网络索引要多得多。<bookmark mark='a'/>这是包含 whale 的前12个段落。"
        "<bookmark mark='b'/>列表是有序的，所以改为存储相邻编号之差：间隔。第一个间隔是编号加1，因为我们的编码从1开始。<bookmark mark='c'/>一个出现在 N 个段落中 f 个里的词项，"
        "间隔平均为 N 除以 f：对 whale 来说大约是29。频繁的词项间隔短；罕见的词项间隔长，但数量少。所以给小的数短的编码。",
    "The simplest code works in whole bytes. <bookmark mark='a'/>":
        "最简单的编码以整字节为单位。<bookmark mark='a'/>每个字节携带间隔的7位，外加一个标记最后一个字节的标志位。<bookmark mark='b'/>1和5装得进一个字节；660有10位二进制数字，"
        "所以要两个字节。<bookmark mark='c'/>在整个索引上：每个倒排项8.67位，大约是32位的四分之一。解码只需一次掩码、一次移位和一次测试，所以很快。"
        "<bookmark mark='d'/>但间隔为1仍然要花8位。",
    "Now we write bits. <bookmark mark='a'/> A gap g has floor of":
        "现在我们按位来写。<bookmark mark='a'/>一个间隔 g 有 log₂g 向下取整再加1位二进制数字，第一位总是1。<bookmark mark='b'/>Peter Elias 1975年的 γ 编码，"
        "先用若干个0写出第一位之后还有多少位，再写出这些数字：一共是 log g 向下取整的2倍再加1位。100要13位。<bookmark mark='c'/>《人工智能，从零搭建》第1部分说明过，"
        "当一个值的概率是2的负 L 次方时，为它花 L 位是最理想的。所以 γ 编码适合按 g 平方分之一衰减的间隔。<bookmark mark='d'/>δ 编码把位数本身用 γ 编码来写：100要11位。在我们的索引上，"
        "γ 编码每个倒排项花5.64位，δ 编码花5.54位。",
    "But we know each list's length, so fit the code to it.":
        "但我们知道每个列表的长度，所以可以让编码去适应它。<bookmark mark='a'/>如果每个段落都独立地包含一个词项，概率 p 等于 f 除以 N，那么间隔服从几何分布。"
        "<bookmark mark='b'/>Solomon Golomb 1966年的编码把 g 减1除以一个参数 M：商用一进制写，余数用二进制写。<bookmark mark='c'/>商也服从几何分布，"
        "而一进制每多一步就多一位，当每一步概率减半时它是最理想的。<bookmark mark='d'/>所以令1减 p 的 M 次方等于二分之一：M 大约是平均间隔的0.69倍，对 whale 来说接近20。"
        "<bookmark mark='e'/>Rice 编码把 M 向下取到2的幂，这样余数恰好占 k 位：这里是4位。",
    "Here are Rice codes with k equal to two. <bookmark":
        "这是 k 等于2时的 Rice 编码。<bookmark mark='a'/>1到4的间隔占3位，此后每多4，就只多加一个1。<bookmark mark='b'/>每个列表用它自己的 k，"
        "Rice 编码在整个索引上每个倒排项花4.96位。<bookmark mark='c'/>而且存在一个下限。从 N 个段落中选出含有某个词项的 f 个，携带的信息是 N 选 f 的对数位：这里是每个倒排项4.74位。"
        "Rice 编码与它相差不到百分之五。",
    "Rice codes decode one bit at a time, through branches, so":
        "Rice 编码要一位一位地解码，还要经过分支，所以现代搜索引擎多花几位来换取速度。<bookmark mark='a'/>取一块间隔，找出其中最宽的。<bookmark mark='b'/>让每个间隔都用那么多位，"
        "并排紧挨着打包：没有标志位，没有一进制，没有分支。<bookmark mark='c'/>然后第24部分的 SIMD 指令一次解包4个间隔。"
        "<bookmark mark='d'/>2006年的 PForDelta 把罕见的大间隔作为异常值另存，而 Lemire 和 Boytsov 2015年的编解码器每秒能解码数十亿个整数。",
    # ------------------------------------------------------------------ s06_ranking
    "Chapter five. From tf-idf to BM25.":
        "第五章：从 tf-idf 到 BM25。",
    "Boolean retrieval answers yes or no, but a reader wants the":
        "布尔检索只回答是或否，但读者想先看到最好的段落。<bookmark mark='a'/>一个词在一个段落里反复出现，就更能说明这个段落，所以按它的词频加权，并用对数加以抑制：第10个 whale 增加的分量少于第1个。"
        "<bookmark mark='b'/>而罕见的词比常见的词说明得更多：Karen Spärck Jones 在1972年用 N 除以文档频率的对数给每个词项加权。"
        "<bookmark mark='c'/>whale 出现在我们的390个段落里，权重是3.36；Darcy 出现在171个段落里，权重是4.19。",
    "Gerard Salton's SMART system made this geometry. <bookmark":
        "Gerard Salton 的 SMART 系统把这变成了几何。<bookmark mark='a'/>一个段落是一个向量，每个词项一维，以这些权重为坐标；查询也是一个向量。"
        "<bookmark mark='b'/>按与查询夹角的余弦给段落排序：点积除以两者的长度。<bookmark mark='c'/>除以长度，可以避免一个长段落只因为长就胜出；我们的 tf-idf 除以长度的平方根，"
        "作为一个廉价的替代。<bookmark mark='d'/>但为什么是这些权重？到目前为止，什么都没有说明。",
    "In 1977 Stephen Robertson stated the principle that answers":
        "1977年，Stephen Robertson 陈述了回答这个问题的原理。<bookmark mark='a'/>按文档相关的概率给文档排序。<bookmark mark='b'/>如果这些概率是对的，"
        "并且各文档是否相关彼此独立，那么对任何 k，都没有别的顺序能让前 k 名中相关文档的期望数目更多。<bookmark mark='c'/>证明是一次交换：把截断线以下一个可能性更大的文档，"
        "与截断线以上一个可能性更小的文档对调，期望数目就会下降。<bookmark mark='d'/>所以排序归结为从词出发估计一个概率。",
    "The binary independence model is the simplest estimate.":
        "二元独立模型是最简单的估计。<bookmark mark='a'/>按概率排序，就是按几率排序。<bookmark mark='b'/>贝叶斯法则把几率颠倒过来，而先验几率对每个段落都相同，所以可以消掉。"
        "<bookmark mark='c'/>把一个段落看作若干词项的出现或缺失，在给定相关性的条件下彼此独立。<bookmark mark='d'/>对数几率就变成对段落所含查询词项的求和，"
        "每一项的权重取决于它在相关段落中出现的可能性大多少。<bookmark mark='e'/>对相关性一无所知时，令 p 为二分之一；由于几乎每个段落都不相关，令 u 为文档频率除以 N。结果就得到 idf，是推导出来的，"
        "而不是猜出来的：Robertson 和 Spärck Jones，1976年。",
    "But that model counts a word once, however often it appears,":
        "但这个模型对一个词只计一次，不管它出现多少次，而一个说了20次 whale 的段落，更可能是关于鲸的。<bookmark mark='a'/>Stephen Harter 1975年的双泊松模型认为，"
        "一个段落要么是关于这个词项的，要么不是，两种情况下计数都服从泊松分布；它所蕴含的权重随计数增长，然后趋于平稳。<bookmark mark='b'/>Robertson 和 Walker 在1994年用一条曲线来近似它："
        "词频乘以 k1 加1，再除以词频加 k1。出现一次时它等于1，并逐渐上升，趋向 k1 加1。<bookmark mark='c'/>k1 接近0时，它又成了二元模型；随着 k1 增大，它就变成原始计数。",
    "One more correction. <bookmark mark='a'/> A long passage":
        "再做一项修正。<bookmark mark='a'/>长段落重复一些词，是因为它长，而不是因为它更多地关于这些词。所以 BM25 把 k1 乘以1减 b、再加上 b 乘以段落长度与平均长度之比。"
        "<bookmark mark='b'/>一个两倍于平均长度的段落，需要出现更多次才能得到同样的权重；b 为0时没有归一化，b 为1时完全归一化。<bookmark mark='c'/>合在一起：来自二元模型的 idf，"
        "来自双泊松的饱和，以及长度。这就是 BM25，1994年在 TREC 上首次运行，也是 Lucene 的默认设置，k1 为1.2，b 为0.75。",
    # ------------------------------------------------------------------ s07_evaluation
    "Chapter six. Is the ranking good?":
        "第六章：这个排序好吗？",
    "To improve a ranking, we have to measure it. <bookmark":
        "要改进一个排序，就必须先测量它。<bookmark mark='a'/>这是一个包含10个段落的排序，相关的段落用颜色标出。<bookmark mark='b'/>前 k 名的精确率，是前 k 名中相关段落所占的比例："
        "读者看到的东西有多少是有用的。<bookmark mark='c'/>前 k 名的召回率，是全部相关段落中被前 k 名包含的比例。这里共有6个相关段落，其中一个始终没有被检索到。"
        "<bookmark mark='d'/>往下读得越远，召回率只会上升，而精确率往往下降，所以单个截断点只讲出了故事的一部分。",
    "Average precision folds the list into one number. <bookmark":
        "平均精确率把这个列表折叠成一个数。<bookmark mark='a'/>在每个出现相关段落的排名上，取到那里为止的精确率：一分之一、三分之二、四分之三，依此类推。<bookmark mark='b'/>把它们加起来，"
        "除以相关段落的总数，所以那个从未被检索到的段落算作0：这里是0.59。它奖励把相关段落排得靠前，并且把它们全部找到。<bookmark mark='c'/>它在多个查询上的平均值就是 MAP。在我们的9个测试查询上，"
        "截取前10个结果，BM25 得0.80，tf-idf 得0.75。",
    "But relevance comes in degrees, and readers rarely reach the":
        "但相关性是分等级的，而读者很少读到底部。Järvelin 和 Kekäläinen 2002年的度量同时处理了这两点。<bookmark mark='a'/>每个段落得到一个等级，以及2的等级次方减1的增益，"
        "所以一个高度相关的段落抵得上3个相关的段落。<bookmark mark='b'/>每个增益都按它的排名加1的对数打折扣：排名第1的完全计入，排名第10的不到三分之一。总和就是折损累计增益。"
        "<bookmark mark='c'/>再除以所有被评判过的段落按理想顺序排列时的同一个总和，每个查询的得分就落在0到1之间，不管它有多少相关段落。这里是0.80。",
    "All of these need judgments. <bookmark mark='a'/> A test":
        "这些都需要相关性评判。<bookmark mark='a'/>一个测试集固定了文档、查询和评判，让各个系统在同等条件下比较，就像 Cyril Cleverdon 在20世纪60年代的 Cranfield 实验那样。"
        "<bookmark mark='b'/>但没有人能为每个查询评判每一篇文档。从1992年起，NIST 的文本检索会议（TREC）把每个提交系统的前100个结果汇集成一个池，评估员只评判这个池；任何没被评判的都算作不相关。"
        "<bookmark mark='c'/>池会漏掉相关文档，但 Justin Zobel 在1998年发现，系统之间的比较大多仍然成立。<bookmark mark='d'/>我们的评判更粗糙：9个查询，每个针对一部小说，"
        "由一条规则而不是由人来分级。",
    "Here are our nine queries. <bookmark mark='a'/> For most,":
        "这是我们的9个查询。<bookmark mark='a'/>对大多数查询，两种排序器都把前十名填满了相关段落，nDCG 为1：名字很容易。"
        "<bookmark mark='b'/>Sherlock Holmes 在两种排序器上都得0.60，而错在我们。前十名中有4个来自《巴斯克维尔的猎犬》（The Hound of the Baskervilles），"
        "里面也有 Holmes，但我们的规则只算《冒险史》（Adventures）。一个糟糕的分数，可能来自一次糟糕的评判。<bookmark mark='c'/>vampire count 是一次真正的失败："
        "《基督山伯爵》（The Count of Monte Cristo）里满是 count 这个词。<bookmark mark='d'/>平均下来，BM25 得0.85，tf-idf 得0.83。",
    "Is that difference real, or luck? <bookmark mark='a'/> Pair":
        "这个差别是真的，还是运气？<bookmark mark='a'/>按查询把两种排序器配成对。6个查询打平，3个偏向 BM25，没有一个偏向 tf-idf。<bookmark mark='b'/>如果两者都不更好，"
        "每个没打平的查询就像一次公平的抛硬币。<bookmark mark='c'/>抛3次全是正面的概率是八分之一，把全是反面也算上就是四分之一：p 等于0.25。9个查询分辨不出来。"
        "<bookmark mark='d'/>这就是为什么 TREC 的评测任务用大约50个主题，并配合第44部分的配对检验和功效计算；而在生产中，评判过的数据集之外还要加上点击和在线实验，这是第十二章要讲的。",
    # ------------------------------------------------------------------ s08_topk
    "Chapter seven. Top k, fast.":
        "第七章：快速求前 k 名。",
    "A reader wants ten results, not a ranking of every passage.":
        "读者要的是10个结果，而不是每个段落的排序。<bookmark mark='a'/>最简单的求值方法按文档顺序一起遍历查询中所有词项的倒排表，给含有其中任何一个词的每个段落打分，并在一个最小堆里保留最好的10个。"
        "<bookmark mark='b'/>那个堆里最小的分数就是阈值 θ：要超过的分数。<bookmark mark='c'/>对查询 the sea，我们的11261个段落中有11257个被打分，而除了10个分数，"
        "其余全被丢掉。",
    "Better to know, before scoring, the most a passage could":
        "最好能在打分之前，就知道一个段落最多能得多少分。<bookmark mark='a'/>建索引时，为每个词项存下它对任何段落所能做出的最大贡献。第五章的饱和本来就给它设了上限；存下的最大值更紧。"
        "<bookmark mark='b'/>假设 θ 是2.6。一个只含 captain 和 ship 的段落最多得2分，所以它进不了前十，也就不必打分。"
        "<bookmark mark='c'/>只有含 ahab 的段落才可能。Turtle 和 Flood 1995年的 max-score 正是这么做的：那些上界加起来也达不到 θ 的词项，永远不会提出候选。",
    "Broder and his colleagues, in 2003, made the bound into a":
        "Broder 和同事在2003年把这个上界变成一种遍历，叫作 WAND，意思是弱的，或者说加权的 AND。<bookmark mark='a'/>每个词项有一个游标。按游标所指的文档给它们排序，"
        "再按这个顺序把它们的上界加起来：第一个使总和超过 θ 的游标就是枢轴。<bookmark mark='b'/>更早的文档都不可能达到 θ，所以每个更早的游标都直接跳到枢轴文档，用的是第三章的跳跃指针或倍增查找。"
        "<bookmark mark='c'/>当它们全都落在它上面时，这个文档才被完整地打分。这里13个文档中有4个被打分：恰好就是含有 ahab 的那些。",
    "On the novels, with BM25 and a real, rising threshold, the":
        "在小说上，用 BM25 和一个真实的、不断上升的阈值，节省是巨大的。<bookmark mark='a'/>对 white whale，在含有某个查询词项的1610个段落中，WAND 只给235个打分。"
        "对 the sea，大约十分之一：the 这个词无处不在，但它的上界很小。<bookmark mark='b'/>pride prejudice 节省最少：两个词都罕见，上界都高，将近一半的候选都必须检查。"
        "<bookmark mark='c'/>在每个查询中，前十名都与穷举打分完全相同，分数一分不差。WAND 是安全的：它从不拿准确性换速度。",
    "One maximum per term is loose: a single passage that says":
        "每个词项只存一个最大值是宽松的：一个说了40次 whale 的段落，就为整个列表定下了上界。<bookmark mark='a'/>Ding 和 Suel 在2011年为每一块倒排项都存了一个最大值，放在跳跃数据旁边。"
        "<bookmark mark='b'/>WAND 选出枢轴之后，块最大 WAND 检查这些更紧的最大值，并跳过达不到 θ 的整块，连解码都不用。<bookmark mark='c'/>它仍然是安全的。"
        "Lucene 在2019年采用了它；从那以后，Elasticsearch 默认只精确统计到1万个匹配，因为统计全部就意味着访问全部。",
    "Other shortcuts trade a little exactness for speed.":
        "其他捷径用一点精确性换取速度。<bookmark mark='a'/>分层索引把每个词项的倒排表拆开：得分最高的放在第一层，其余的放在第二层。<bookmark mark='b'/>查询先搜索第一层，"
        "只有在返回的好答案少于10个时才继续。Manning、Raghavan 和 Schütze 的教科书里的冠军列表，只保留每个词项最好的几个文档。<bookmark mark='c'/>这些都是不安全的："
        "一个只在词项组合上才强的段落可能被漏掉，而第六章的指标能测出这种损失。<bookmark mark='d'/>各层也可以按每个网页的质量分数来排列，比如从链接计算出来的分数。",
    # ------------------------------------------------------------------ s09_links
    "Chapter eight. Links and the random surfer.":
        "第八章：链接与随机冲浪者。",
    "Words say what a page is about, not whether it is any good.":
        "词说明一个网页是关于什么的，而不说明它好不好。<bookmark mark='a'/>谢尔盖·布林和拉里·佩奇在1998年把网页之间的链接读作投票：如果重要的网页链接到一个网页，它就重要，"
        "而每个网页把自己的票分给它的各个链接。<bookmark mark='b'/>这个定义是循环的，一个故事解开了它。一个冲浪者在每个网页上点击一个随机链接，时不时地，他厌倦了，就跳到一个随机的网页。"
        "<bookmark mark='c'/>从长远看，冲浪者在每个网页上花的时间比例，就是它的 PageRank。<bookmark mark='d'/>布林和佩奇还把每个链接的文字作为描述其目标的词编入索引。",
    "Write it down. <bookmark mark='a'/> With probability d the":
        "把它写下来。<bookmark mark='a'/>冲浪者以概率 d 跟随一个链接；否则就随机跳转到任何地方。所以一个网页的排名，是随机跳转的那一份，即1减 d 除以网页总数，加上 d 乘以流入的排名，"
        "每个网页把自己的排名平均分给它的每个链接。布林和佩奇建议 d 取0.85。<bookmark mark='b'/>一个没有链接的网页，把它的排名传给所有网页。<bookmark mark='c'/>写成矩阵形式，"
        "排名向量就是 Google 矩阵对应特征值1的特征向量：一条马尔可夫链的平稳分布，就像第18部分那样。<bookmark mark='d'/>随机跳转让每个网页都连到其他每个网页，"
        "所以根据 Perron–Frobenius 定理，这个向量存在而且唯一。",
    "To compute it, start from the uniform vector and multiply by":
        "要计算它，从均匀向量出发，一遍又一遍地乘以这个矩阵。<bookmark mark='a'/>我们的合成网络有400个网页，每个链接到至多4个更早的网页，按它们已有的链接数成比例地选，"
        "另外还有一个由20个网页组成的链接农场。<bookmark mark='b'/>每一步，变化至少缩小为原来的 d 倍，而这里更快：40步之后缩小到百万分之一。这个界不依赖网页的数目，所以几十亿个网页的网络也只需要几十遍。"
        "<bookmark mark='c'/>排名最高的网页是最老的那些，优先连接让它们成了枢纽。",
    "Jon Kleinberg, at the same time, read links differently.":
        "与此同时，Jon Kleinberg 用另一种方式解读链接。<bookmark mark='a'/>权威是被好的枢纽链接的网页；枢纽是链接到好的权威的网页。每个分数都是另一种分数沿链接的总和。"
        "<bookmark mark='b'/>反复迭代并归一化，两个向量就收敛到 A 转置 A 和 A A 转置的主特征向量，也就是链接矩阵的奇异向量。Kleinberg 在一个查询结果的邻域上运行它。"
        "<bookmark mark='c'/>在我们的网络上，它很容易被带偏。排名第一的权威是农场的目标，排名第一的枢纽是一个农场网页，而全部20个农场网页都在最好的20个枢纽之中。",
    "That farm is link spam: twenty pages linking to one target":
        "那个农场就是链接作弊：20个网页链接到同一个目标，也互相链接。<bookmark mark='a'/>没有它，这个目标，也就是我们网络中最新的网页，在400个网页中排第346。"
        "<bookmark mark='b'/>有了它，在420个网页中排第114：每个农场网页收下它那份随机跳转的排名，再把大部分传出去。<bookmark mark='c'/>防御随之而来。2005年，"
        "各大搜索引擎就一个 nofollow 属性达成一致，用于网站不为之担保的链接，比如评论里的链接。TrustRank 由 Gyöngyi、Garcia-Molina 和 Pedersen 在2004年提出，"
        "它只随机跳转到经过人工核查的网页。今天，链接只是许多信号中的一个，由学习得到的排序器组合起来，第十二章会展示这一点。",
    # ------------------------------------------------------------------ s10_crawl
    "Chapter nine. Crawling the web.":
        "第九章：爬取网页。",
    "Before anything can be indexed, it must be fetched.":
        "任何东西在被索引之前，都必须先被抓取。<bookmark mark='a'/>爬虫从待抓取队列（frontier）里的种子地址出发。它取出一个地址，查找主机，检查网站的 robots.txt，下载网页并解析它。"
        "<bookmark mark='b'/>找到的每个链接都要规范化，让一个网页只有一个地址，再与已经见过的地址比对，那是第17部分那样的一个指纹哈希集合。新的地址加入待抓取队列。"
        "<bookmark mark='c'/>文本也要算指纹，这样副本就不会被索引两次。Heydon 和 Najork 的 Mercator 在1999年阐述了这种设计。爬虫还必须逃离陷阱，比如一个日历永远链接到下一天。",
    "The frontier decides what to fetch next, and it serves two":
        "待抓取队列决定下一个抓取什么，它要同时满足两个要求。<bookmark mark='a'/>优先级：重要的、变化快的网页先抓，放在 Mercator 的前端队列里。<bookmark mark='b'/>还有礼貌："
        "绝不猛击同一台服务器。每个后端队列只放一个主机，一个堆记录每个主机下一次可以联系的时间。Manning、Raghavan 和 Schütze 的教科书里有一条常用规则："
        "等待的时间大约是上一次从那个主机抓取所用时间的10倍。<bookmark mark='c'/>网站也会声明自己的意愿。Martijn Koster 1994年的 robots 排除约定，列出爬虫不应触碰的路径；"
        "2022年它成为一项互联网标准，RFC 9309。一个有礼貌的爬虫同时从成千上万个主机抓取，而对每一个都慢慢地抓。",
    "The web changes after it is crawled, so a crawler must come":
        "网页被爬取之后还会变化，所以爬虫必须回来。<bookmark mark='a'/>这是两个网页，一个经常变化，一个很少变化，以同样的频率重访。在一次变化和下一次访问之间，我们的副本是过时的。"
        "<bookmark mark='b'/>如果一个网页以速率 λ 随机变化，而我们每隔时间 I 重访一次，那么我们的副本保持新鲜的时间比例是：1减 e 的负 λI 次方，再除以 λI。"
        "<bookmark mark='c'/>Junghoo Cho 和 Hector Garcia-Molina 在2000年发现了一个出人意料的结果。在预算固定时，以同样的频率重访每个网页，胜过按变化频率成比例地重访；"
        "而最好的策略对变化最快的网页反而访问得更少，因为它们的副本几乎立刻就过时了。",
    "Much of the web is copied: mirrors, syndicated articles,":
        "网络上很多内容是复制的：镜像、转载的文章、只差一条广告的网页。<bookmark mark='a'/>Moses Charikar 2002年的 SimHash 生成一种指纹，文本稍有变化，它也只变化一点。"
        "把文本切成相互重叠的三词瓦片，把每个瓦片哈希成64位。<bookmark mark='b'/>对每个位的位置，凡是这一位为1的瓦片就加1，为0的就减1。<bookmark mark='c'/>指纹保留这些和的符号。"
        "一个小的修改只改变几个瓦片，很少会翻转一个符号。<bookmark mark='d'/>这就是第20部分的随机超平面草图：每一位说明文档的瓦片向量位于一个随机超平面的哪一侧。",
    "How well does it work on the novels? <bookmark mark='a'/> We":
        "它在小说上效果如何？<bookmark mark='a'/>我们给200个段落算了指纹，并随机替换其中的词。替换一个词，平均让2.4位改变；替换80个词，也就是段落的五分之一，大约改变20位。不相关的段落相差大约32位，"
        "即64的一半，而最接近的一对不相关段落相差22位。<bookmark mark='b'/>Manku、Jain 和 Das Sarma 2007年在 Google 发现，对80亿个网页来说，3位是一个好的阈值。"
        "为了快速搜索，把指纹切成4块，每块16位。<bookmark mark='c'/>3个不同的位至多破坏3块，所以总有一块完全一致，而在4张有序表里对每块做一次精确查找，就能找到所有候选。",
    # ------------------------------------------------------------------ s11_serving
    "Chapter ten. Serving at scale.":
        "第十章：大规模服务。",
    'f"One machine cannot hold the web\'s index, or answer':
        "一台机器既装不下整个网络的索引，也回答不了全世界的查询，所以索引必须被切成若干块。<bookmark mark='a'/>把它想象成一个矩阵：每个词项一行，每个段落一列，每个倒排项一个点。"
        "我们的矩阵有{ix['terms']:,}行、{ix['docs']:,}列，而且几乎是空的。<bookmark mark='b'/>按列切，每个分片就是一部分段落的一个完整的小索引：按文档划分。"
        "<bookmark mark='c'/>按行切，每台服务器保存某些词项的完整倒排表：按词项划分。矩阵是同一个；不同的是一次查询引起的工作。",
    'f"Follow the query whale sea through each layout.':
        "顺着查询 whale sea 走一遍这两种布局。<bookmark mark='a'/>按文档划分时，代理（broker）把整个查询发给每个分片。每个分片在自己那四分之一的段落上算出自己的前十名，代理再合并4个短列表。"
        "打分需要整个文档集合的统计量，比如 idf，在各分片之间共享。<bookmark mark='b'/>按词项划分时，只有保存这两个词项的两台服务器工作，但其中一台必须把它的整个列表，{n_whale}个倒排项，"
        "发给另一台，由后者求交集，找出{row['hits']}个段落。<bookmark mark='c'/>网络搜索引擎选择了按文档划分：Barroso、Dean 和 Hoelzle 在2003年描述的 Google 集群，"
        "把它的索引切成了由文档组成的分片。",
    "Document partitioning has a price, which Part 39 called the":
        "按文档划分有一个代价，第39部分称之为规模下的尾部。<bookmark mark='a'/>一个查询要等它最慢的分片。假设像 Dean 和 Barroso 在2013年那样，每台服务器每100个请求中有一个很慢。"
        "只涉及一台服务器的查询，每100次中慢1次；必须等100台服务器的查询，每100次中慢63次。<bookmark mark='b'/>一种补救办法是对冲请求：在一小段延迟之后，把同一个请求再发一份给另一个副本，"
        "谁先回答就用谁。在他们的测试中，它把第99.9百分位数从1800毫秒降到74毫秒，只多了百分之二的请求。<bookmark mark='c'/>另一种办法是不等掉队者就作答。",
    "A real deployment is a grid. <bookmark mark='a'/> The":
        "真实的部署是一张网格。<bookmark mark='a'/>列是分片，每个保存索引的一部分；行是副本，完全相同的拷贝。一个查询访问每个分片的一个副本，按负载来选。"
        "<bookmark mark='b'/>当一台机器出故障时，而在一个大集群里总有一台是坏的，代理就把那个分片的工作发给另一份拷贝，用户什么也察觉不到。<bookmark mark='c'/>这张网格朝两个方向增长。"
        "每秒查询更多？加一行副本。<bookmark mark='d'/>索引更大？加一列分片，每个分片更小，所以每个都回答得更快。容量和规模是两个独立的旋钮。",
    "The cheapest query is one you have already answered.":
        "最便宜的查询是你已经回答过的查询。<bookmark mark='a'/>查询的偏斜和词一样：正如第一章在小说上发现的，少数查询极其常见，大多数很罕见，所以一小撮热门查询整天反复出现。"
        "<bookmark mark='b'/>代理前面的结果缓存，为这一小撮查询保存整页答案。命中的请求不碰任何分片就直接返回。缓存条目必须过期，因为它们底下的索引一直在变。"
        "<bookmark mark='c'/>未命中的请求走完整条路径，而尾部就在那里。在每个分片内部，第二个缓存把热门词项的倒排表保留在内存里。Baeza-Yates 和同事在2007年证明，最值得保留的词项，"
        "是那些被查询使用的频率相对于其列表长度较高的词项。",
    # ------------------------------------------------------------------ s12_spelling
    "Chapter eleven. Spelling and autocomplete.":
        "第十一章：拼写纠错与自动补全。",
    'f"A user types {\' \'.join(row[\'typed\'])}. What did':
        "一位用户输入了 {' '.join(row['typed'])}。他想输入的是什么？<bookmark mark='a'/>把这个错误建模为一条经过噪声信道发送的消息：想要的词进去，手指把它弄乱，出来一个拼写错误。"
        "这里有两个字母被对调了。<bookmark mark='b'/>要解码，就选出那个使先验概率乘以“信道把它变成这个错误的概率”达到最大的词。<bookmark mark='c'/>先验是一个语言模型；"
        "我们的先验只是每个词在小说里的计数。信道模型说明哪些失误是常见的；我们的信道模型对每次编辑收取固定的罚分。Kernighan、Church 和 Gale 在1990年则从真实的打字错误中把它学了出来。"
        "<bookmark mark='d'/>这就是贝叶斯法则。",
    'f"The channel needs a distance between a typo and a':
        "信道需要一个拼写错误与一个词之间的距离。<bookmark mark='a'/>这就是第21部分的编辑距离：把一个字符串变成另一个所需的最少插入、删除和替换次数。"
        "<bookmark mark='b'/>把一个词横放在顶上，另一个竖放在侧边。每个格子取它三个邻居中最便宜的那个再加1，或者在字母相同时免费取它的对角邻居。这就是第19部分的动态规划，一行一行地填。"
        "<bookmark mark='c'/>角上的格子是{D[len(a)][len(b)]}：对调一对相邻字母要花两次替换。Damerau 在1964年观察到，对调两个相邻字母是最常见的失误之一，于是把它算作一次编辑。",
    "Comparing a typo with every word in the vocabulary is":
        "把一个拼写错误与词汇表中的每个词比较是浪费。Burkhard 和 Keller 1973年的树做得更好。<bookmark mark='a'/>每个词挂在它的父节点下面，连接它们的边标着两者之间的编辑距离。"
        "<bookmark mark='b'/>要找出与一个拼写错误相差一次编辑以内的词，先算出它到根的距离 d。因为编辑距离是一种度量，三角不等式表明，匹配只可能位于标着 d 减1到 d 加1的那些边下面，"
        "其他每棵子树都不用访问就跳过。<bookmark mark='c'/>在小说的词汇表上，容差为2时，我们的树仍要计算全部距离的大约三分之一：当容差相对于词本身较大时，剪枝的效果很弱。",
    'f"Here is the whole corrector on seven inputs, with':
        "这是整个纠错器在7个输入上的表现，词汇表取自小说，共{sp['vocab']:,}个词。"
        "<bookmark mark='a'/>拼错的 captain、Elizabeth、separate、monster 和 London 都被修复了。"
        "<bookmark mark='b'/>{same['typed'].capitalize()} 本身已经是一个词：它在两次编辑以内有{same['candidates']}个邻居，但没有一个常见到值得做这次改动，"
        "所以它保持不变。<bookmark mark='c'/>还有一个改错了。recieve 变成了 relieve，因为 relieve 只差一次替换，而 receive 在普通的编辑距离下差两次。Damerau 的换位，"
        "或者从真实失误中学出的信道，就能把它改对。<bookmark mark='d'/>真实的纠错器还会读周围的词，并从查询日志中学习人们接下来重新输入了什么。",
    "Better still is to catch the query before it is finished.":
        "更好的做法是在查询输完之前就把它截住。<bookmark mark='a'/>自动补全是沿着一棵字典树往下走，也就是第17部分的前缀树。输入 c、a，那个节点下面的每个词都是候选。"
        "<bookmark mark='b'/>按在小说中的计数排序，最好的5个是 can、came、called、cannot 和 can't。<bookmark mark='c'/>要在不访问整棵子树的情况下找到它们，"
        "就在每个节点存下它下面任何地方的最大计数。然后一个优先队列总是展开最有希望的节点，前 k 名大约在 k 乘以深度那么多步之后就出来，不管词汇表有多大。"
        "<bookmark mark='d'/>或者干脆在每个节点直接存下前几名，用内存换速度。真实的搜索引擎按人们搜索什么来给补全排序。",
    # ------------------------------------------------------------------ s13_ltr
    "Chapter twelve. Learning to rank.":
        "第十二章：排序学习。",
    'f"BM25 is one signal. A web engine has hundreds.':
        "BM25 只是一个信号。网络搜索引擎有几百个。<bookmark mark='a'/>对每个查询和段落，它计算一个特征向量：BM25 和 tf-idf，短语是否出现，词项挨得多近，长度，"
        "在网络上还有 PageRank 和以往用户的点击。<bookmark mark='b'/>手工调一个给上百个这样的特征加权的公式是没有希望的，所以由一个模型从分过级的查询中学习它，就像我们第六章的{n_q}个查询，"
        "但要成千上万个，由人来分级。微软公开的 MSLR 数据集用136个特征描述每个查询和网页。<bookmark mark='c'/>模型输出一个用来排序的分数。真正的问题是用什么损失来训练它。",
    "There are three families of loss. <bookmark mark='a'/>":
        "损失有三大类。<bookmark mark='a'/>逐点方法用回归预测每个段落的等级，一次一个。但用户看到的只是一个顺序，而且不同查询之间的等级无法比较。<bookmark mark='b'/>成对方法看的是段落对："
        "只要一个段落比另一个好，它的分数就应该更高。Burges 和同事2005年的 RankNet，对两个分数之差使用逻辑斯谛损失。但它对每一对排错的段落一视同仁，不管是在页面顶部，还是在远远的下方。"
        "<bookmark mark='c'/>列表方法用我们关心的度量，比如 nDCG，来评判整个列表。但 nDCG 只在两个分数交叉时才变化，所以它没有有用的梯度。",
    "Burges and colleagues found a way round that in 2006.":
        "Burges 和同事在2006年找到了绕过它的办法。<bookmark mark='a'/>取6个分过级的段落，按模型当前的顺序排列。<bookmark mark='b'/>RankNet 的梯度，"
        "每有一个更差的段落排在它上面，就把它往上推，每有一个更好的段落排在它下面，就把它往下推，推动的幅度只取决于两个分数。<bookmark mark='c'/>LambdaRank 把每一对的推力，"
        "乘以两者交换位置时 nDCG 会改变多少。现在靠近顶部的对占主导，而页面下方的对几乎不算数。<bookmark mark='d'/>诀窍在于根本不写出损失：定义你想要的梯度，也就是那些 lambda，然后跟着它走。"
        "段落 C 最好，得到最强的推力。",
    'f"Lambdas are gradients, and AI, Built Part 6 showed':
        "lambda 就是梯度，而《人工智能，从零搭建》第6部分已经说明了，对表格特征上的梯度该怎么做：提升树。<bookmark mark='a'/>LambdaMART 从某些分数出发，算出每个段落的 lambda，"
        "并拟合一棵小的回归树，用特征来预测它们，再以一个小的权重加上去。<bookmark mark='b'/>然后重新计算 lambda，再用另一棵树拟合它们。在我们的图中，"
        "nDCG 从{nd[0]:.2f}升到{nd[1]:.2f}，然后升到{last}。<bookmark mark='c'/>因为树是按特征分裂的，模型能推广到它从未见过的查询。"
        "一个建立在这些 lambda 梯度上的集成模型，赢得了2010年 Yahoo 的排序学习挑战赛，而 LightGBM 和 XGBoost 把它作为一个标准的目标函数提供。",
    "Judged queries are expensive; clicks are free, but biased.":
        "评判过的查询很昂贵；点击是免费的，但有偏差。<bookmark mark='a'/>人们大多只看页面的顶部，所以一次点击既取决于结果显示在哪里，也取决于它是否相关。"
        "<bookmark mark='b'/>Joachims 和同事在2005年用眼动追踪证明了这一点：当前两个结果被悄悄对调时，用户仍然更常点击第一个。"
        "<bookmark mark='c'/>在 Craswell 和同事的级联模型中，用户沿着页面往下读，点击第一个看起来合适的结果。<bookmark mark='d'/>要从点击中学习，又不把旧的排序学回来，"
        "就给每次点击乘以“它的位置被看到的概率”的倒数，这个概率通过随机对调结果来测量：这就是无偏排序学习。",
    # ------------------------------------------------------------------ s14_dense
    "Chapter thirteen. Dense retrieval.":
        "第十三章：稠密检索。",
    'f"Everything so far matches words. <bookmark':
        "到目前为止，一切都是在匹配词。<bookmark mark='a'/>一个关于在大洋上航行的查询，与一个关于海上一艘船的段落得分为0，因为它们没有共同的词项。"
        "<bookmark mark='b'/>稠密检索把这个问题搬进几何。一个编码器，也就是《人工智能，从零搭建》第24部分的嵌入，把每个段落映射成一个向量，只做一次，离线完成，而查询在查询时才映射；相关性就是一个点积。"
        "<bookmark mark='c'/>相关的段落落在彼此附近，检索就变成了最近邻搜索。<bookmark mark='d'/>我们自己的向量只是一个替代品：tf-idf 由一个随机矩阵投影到{dim}维，"
        "这是第20部分的技巧。它们保留的是词的几何，而不是意思的几何；一个训练过的编码器，比如 Karpukhin 和同事2020年的稠密段落检索器，从例子中学习意思。",
    'f"A float vector per passage costs':
        "每个段落一个浮点向量，要花{row8['float_bytes']}字节；十亿个段落就需要几百吉字节。Jegou、Douze 和 Schmid 2011年的乘积量化把它缩小。"
        "<bookmark mark='a'/>把每个向量切成{m}个子向量，每个{s}维。<bookmark mark='b'/>在每个子向量的空间里，把所有段落聚成256组，只存下最近的那个中心的编号：1字节。"
        "向量就变成了{row8['bytes']}字节。<bookmark mark='c'/>8个位置中每个位置有256种选择，组合出天文数字般多的编码，而所需的中心却非常少。"
        "<bookmark mark='d'/>搜索不需要解压：一次性算出查询到每个中心的距离，每个段落的距离就是8次查表的和。",
    'f"How much does compression cost? We measured it on':
        "压缩的代价有多大？我们在{p['dim']}维的段落向量上用100个查询测量了它。<bookmark mark='a'/>每个段落2字节时，"
        "PQ 能找到真正最近的10个中的百分之{100 * rows[0]['recall10']:.0f}；8字节时，百分之{100 * rows[2]['recall10']:.0f}；16字节时，"
        "百分之{100 * rows[3]['recall10']:.0f}，而大小只有精确向量{rows[0]['float_bytes']}字节的十六分之一。"
        "<bookmark mark='b'/>平方误差从单位向量的{rows[0]['mse']:.2f}降到{rows[-1]['mse']:.2f}。"
        "<bookmark mark='c'/>所以真实的系统只用这些编码来筛出一份短名单：一个倒排文件挑出几个要扫描的簇，编码给其中的内容排序，最好的那些再被精确地重新打分，就像 Faiss 库里那样。",
    'f"Even compressed, a full scan is too slow at web':
        "即使压缩过，在网络规模上做全量扫描也太慢了。Malkov 和 Yashunin 的分层可导航小世界图避开了它。<bookmark mark='a'/>每个点被赋予一个随机的层级，层级按几何级数变稀："
        "在我们这张由{h['n']:,}个段落向量组成的图里，{lv[0]:,}个只在最底层，只有{lv[top]}个到达第{top}层。每一层都连接相近的邻居，就像跳表的快速通道。"
        "<bookmark mark='b'/>搜索从顶层进入，以长跳贪心地走向查询，降一层，再以更短的跳重复，直到在最底层用一次束搜索收集最近的那些点。<bookmark mark='c'/>更宽的束换来更高的召回率："
        "束宽为{mid['ef']}时，找到真正前十名的百分之{100 * mid['recall10']:.0f}，用了{mid['distance_calls']:.0f}次距离计算，大约是暴力搜索的{frac}。",
    "In practice both kinds run side by side. <bookmark":
        "实践中，两种检索并排运行。<bookmark mark='a'/>BM25 给出一个排序，稠密检索器给出另一个，而它们的分数处在互不相关的尺度上。<bookmark mark='b'/>倒数排名融合，"
        "由 Cormack、Clarke 和 Buettcher 在2009年提出，它不管分数：每个列表给一个段落60加它的排名分之一，由总和来决定。两个列表都喜欢的段落会升到顶部。"
        "<bookmark mark='c'/>词能抓住名字和罕见词项；向量能抓住同义改写。而在编码器从未见过的文档集合上，2021年的 BEIR 基准发现，BM25 往往仍然很难被超越。"
        "<bookmark mark='d'/>前几名段落的读者越来越多地是一个语言模型，就像《人工智能，从零搭建》第15部分的检索增强生成那样。",
    # ------------------------------------------------------------------ s15_engine
    "Chapter fourteen. A search engine for the novels.":
        "第十四章：为小说打造的搜索引擎。",
    "Here is our engine, end to end. <bookmark mark='a'/> A query":
        "这是我们的搜索引擎，从头到尾。<bookmark mark='a'/>一个查询到来：the hound on the moor。<bookmark mark='b'/>它和段落一样被分词，停用词被丢掉，"
        "其余的词被提取词干，这样它就能与索引的词项匹配。<bookmark mark='c'/>搜索引擎取出每个词项的倒排表。<bookmark mark='d'/>它用 BM25 给候选打分，"
        "让 WAND 跳过那些进不了前十的候选。<bookmark mark='e'/>然后返回最好的10个段落，每个都附有一段围绕第一个匹配词截取的摘要。",
    "Four queries and their best answers. <bookmark mark='a'/>":
        "4个查询和它们的最佳答案。<bookmark mark='a'/>the white whale 和 call me Ishmael 都指向《白鲸》，指向那些词聚集的段落。"
        "<bookmark mark='b'/>pride and prejudice 指向简·奥斯汀的那部小说，the hound on the moor 指向《巴斯克维尔的猎犬》。"
        "<bookmark mark='c'/>这里没有任何东西知道这些书讲的是什么。排序完全来自哪些词罕见、它们出现在哪里，以及段落有多长。",
    'f"How big is it? <bookmark mark=\'a\'/> Our index':
        "它有多大？<bookmark mark='a'/>我们的索引有{n / 1000000.0:.1f}百万个倒排项。存成普通的32位整数，光是文档编号就要大约{32 * n / 8 / 1000000.0:.1f}兆字节。"
        "<bookmark mark='b'/>用 Golomb–Rice 编码存间隔，大约{c['bits_per_posting']['rice'] * n / 8 / 1000000.0:.1f}兆字节，每个倒排项5位。"
        "<bookmark mark='c'/>而且没有任何编码能好得多：从 N 个文档中选出含有一个词项的 f 个，携带 N 选 f 的对数位信息，"
        "在这里折合每个倒排项{bnd['bound_bits_per_posting']:.2f}位。Golomb–Rice 与这个极限只差百分之几，除非有一种编码能利用倒排项聚集的方式。",
    "And what a web search engine adds. <bookmark mark='a'/>":
        "再看网络搜索引擎还要加上什么。<bookmark mark='a'/>几千亿个网页，而不是11000个段落，一遍又一遍地爬取；几百种语言，还有同义词和实体；由学习得到的模型组合起来的几百个排序信号；"
        "链接权威性和对作弊的防御；成千上万台机器；以及发布几分钟后就必须能被搜到的新闻。<bookmark mark='b'/>但核心是一样的。Lucene，"
        "Elasticsearch、OpenSearch 和 Solr 底下的开源库，默认用 BM25 排序，在像我们这样压缩过的倒排列表上进行。",
    # ------------------------------------------------------------------ s16_frontier
    "Chapter fifteen, the frontier. What should a search engine":
        "第十五章：前沿。既然机器能写出答案，搜索引擎应该返回什么？",
    'f"Vector search is where theory lags furthest behind':
        "向量搜索是理论最落后于实践的地方。<bookmark mark='a'/>我们自己的分层图用大约{rows[0]['distance_calls']:.0f}次距离计算，"
        "找到真正最近的10个段落中的百分之{100 * rows[0]['recall10']:.0f}；用大约{rows[-1]['distance_calls']:.0f}次，"
        "找到百分之{100 * rows[-1]['recall10']:.0f}；而暴力搜索要{h['n']:,}次。<bookmark mark='b'/>像这样的图索引赢得了各项基准测试，但它们没有最坏情况下的保证："
        "在对抗性的数据上，贪心的遍历可能停滞在离答案很远的地方。<bookmark mark='c'/>局部敏感哈希有保证，但在实践中落败，而最近的理论才刚刚开始解释可导航图何时有效。弥合这道鸿沟是一个未解决的问题。",
    "Between words and vectors, research has found middle":
        "在词和向量之间，研究找到了一些折中的做法。<bookmark mark='a'/>学习型稀疏检索让一个模型把每篇文档改写成带权重的词项，包括文档中并不含有的词，这样本部分的倒排索引就能继续工作；"
        "2021年的 SPLADE 是其中最知名的。<bookmark mark='b'/>延迟交互为每个词元保留一个向量，并在查询时逐一匹配它们，就像 ColBERT 在2020年所做的：更精确，也大得多。"
        "<bookmark mark='c'/>而混合系统干脆两者都运行，词用于名字和罕见词项，向量用于意思，再融合分数。<bookmark mark='d'/>一个引人注目的未解事实：在模型从未见过的文档集合上，"
        "BM25 往往仍然很难被超越。为什么，以及如何让学习得到的检索器具备泛化能力，都是未解决的问题。",
    "Finally, search is changing what it is for. <bookmark":
        "最后，搜索的用途正在改变。<bookmark mark='a'/>在《人工智能，从零搭建》讲过的检索增强生成中，一个像我们这样的搜索引擎找出段落，由一个语言模型根据它们写出答案，并附上引用。搜索引擎成了模型的记忆，"
        "用户也许根本看不到排好序的列表。<bookmark mark='b'/>生成式检索走得更远：模型记住整个文档集合，自己输出相关文档的标识符，这让更新索引成了难点。"
        "<bookmark mark='c'/>如何评估一个写出来的答案而不是一个排好序的列表，如何检查它是否忠实于来源，以及如何让模型的记忆像索引一样保持新鲜，都是未解决的问题。",
    "Open problems. <bookmark mark='a'/> Guarantees for":
        "未解决的问题。<bookmark mark='a'/>在人们实际拥有的数据上，为基于图的最近邻搜索提供保证。<bookmark mark='b'/>在从未见过的文档集合上胜过 BM25 的学习型检索器。"
        "<bookmark mark='c'/>当人工评判太少时，如何评估排序和写出的答案。<bookmark mark='d'/>还有能添加和删除文档而无需重新训练的生成式索引。"
        "<bookmark mark='e'/>这一部分的研究题要求：在内在维度较低的数据上，也就是真实文档集合似乎所属的情形，给出一个召回率和查询时间都可证明的图索引。",
    # ------------------------------------------------------------------ s17_outro
    "What we built in this part. Zipf's and Heaps' laws, fitted":
        "这一部分我们构建了什么。在小说上拟合的齐普夫定律和 Heaps 定律。一个倒排索引，以及求它的列表交集的三种方法，从线性合并到倍增查找。长度由我们推导出来的间隔编码，它把一个倒排项从32位缩到大约5位。"
        "从概率排序原理出发的 BM25，用 nDCG 来测量；WAND，它在只完整打分一小部分候选的情况下找到同样的前十名；作为随机冲浪者平稳分布的 PageRank；用于近似重复的 SimHash；"
        "以及用乘积量化压缩、通过分层图搜索的向量。一个思想贯穿其中：一个好的索引在查询到来之前，就完成了几乎全部的工作。",
    "Where this comes back. Parts 48 and 49 design a search":
        "这些内容会在哪里再出现。第48和49部分设计一个搜索服务：如何给它分片、加缓存并保持它新鲜。第50部分让像它这样的服务系统保持健康。第56部分用谱图理论回到 PageRank 背后的特征向量。第57部分会问，"
        "学习得到的排序器何时能够泛化。而第60部分着眼于为向量搜索和推理打造的硬件。",
    "In practice. Normalize text the way your users type it, stem":
        "实践中。按用户输入的方式规范化文本，谨慎地提取词干，并为短语查询保留原始的词。把倒排表有序地、分块压缩地存储，附上跳跃数据和分数上界。把 BM25 当作要超越的基线，并在评判过的查询上调优它。保留一组评判过的查询，"
        "测量 nDCG，在发布一项排序改动之前先检验显著性。还有，把词法检索和稠密检索结合起来，并测量近似向量搜索漏掉了多少。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：给我们的搜索引擎加上块最大 WAND，为每一块倒排项设一个分数上界，并测量它能多跳过多少。最后一道标有星号，是研究题："
        "一个用于最近邻搜索的图索引，对人们实际搜索的那类数据，在召回率和速度上都有保证。",
    "Next time, Part 48: system design, and its building blocks.":
        "下一次，第48部分：系统设计，以及它的构件。每个设计者都应该随身带着的那些数字；负载均衡器和缓存，以及它们命中率的算术；分片和复制；限流器和队列；还有如何把它们组合成一个设计的形状。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
PHRASES.update({"one, the ideal order": "1，也就是理想的顺序", "fifth": "五分之一", "sixth": "六分之一",
                "seventh": "七分之一", "eighth": "八分之一", "fraction": "一小部分"})
