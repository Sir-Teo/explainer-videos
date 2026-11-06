"""Chinese narration for cs21: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第21部分：字符串"

CHAPTERS = {
    "Hook": "四种方法找 Queequeg",
    "Naive": "1. 最直接的匹配",
    "RabinKarp": "2. 滚动哈希",
    "Kmp": "3. Knuth、Morris 与 Pratt：从不回头",
    "BoyerMoore": "4. Boyer 与 Moore：向前跳",
    "AhoCorasick": "5. 一次匹配许多模式",
    "SuffixTree": "6. 后缀树",
    "SuffixArray": "7. 后缀数组",
    "Bwt": "8. Burrows–Wheeler 变换",
    "FmIndex": "9. 搜索压缩文本：FM 索引",
    "Lz": "10. 压缩（上）：Lempel 与 Ziv",
    "Entropy": "11. 压缩（下）：给符号编码",
    "Align": "12. 序列比对",
    "Diff": "13. Myers 的 diff",
    "Rsync": "14. 大规模的滚动哈希：rsync 与分块",
    "Period": "15. 周期、回文与 Lyndon 词",
    "Frontier": "16. 前沿：和信息量一样小的索引",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"Queequeg, the harpooner of Moby-Dick.':
        "Queequeg，《白鲸》里的鱼叉手。他的名字在三十部小说、两千五百万字节的文本中出现在哪里？<bookmark mark='a'/>最直接的方法在每个位置"
        "把名字与文本比较：大约两千五百万次字符比较，差不多每个字符一次。<bookmark mark='b'/>Knuth、Morris 与 Pratt 的算法保证每个字符"
        "最多比较两次，而且从不回头。<bookmark mark='c'/>Boyer 与 Moore 的算法先看名字的末尾，然后向前跳：三百五十万次比较，少了七倍。"
        "<bookmark mark='d'/>而由文本的一种奇特排列，即 Burrows–Wheeler 变换，构造的索引，只用十六次小小的查表就能回答，与小说的长度无关。"
        "<bookmark mark='e'/>四种方法找到的都是同样的 {d['hits']} 处。",
    "Text is the oldest kind of data":
        "文本是最古老的一种数据，这一部分讲我们对它做的四件事。<bookmark mark='a'/>我们搜索它，用由模式构造的自动机，以及所有后缀的索引。"
        "<bookmark mark='b'/>我们压缩它。zlib 把小说压到大约三分之一，而一种对文本排序的变换做得更好。<bookmark mark='c'/>我们比较它："
        "每一次 git diff 都在网格上计算一条最短路径，我们会在这门课自己的教学大纲的历史上运行一次。<bookmark mark='d'/>我们还同步它，"
        "只发送变化的部分，用第20部分的滚动哈希找出来。",
    "Part 21 of Computer Science, Built: Strings.":
        "计算机科学，从零搭建，第21部分：字符串。<bookmark mark='a'/>这一部分包括：找一个模式的五种方法；为整个语料构造的后缀树和后缀数组；"
        "Burrows–Wheeler 变换和 FM 索引，它不用解压就能搜索文本；Lempel–Ziv 压缩及其背后的熵编码器；比对、diff 和 rsync；周期与回文；"
        "以及和文本中的信息量一样小的索引。",
    # ------------------------------------------------------------------ Naive
    "Chapter one. Matching, the obvious way.": "第1章。最直接的匹配。",
    "Put the pattern under the text at the first position":
        "把模式放在文本的第一个位置下面，从左到右比较，直到某个字符不同。然后滑动一位，重新开始。<bookmark mark='a'/>在大多数位置，第一个字符"
        "就已经不同，所以工作量接近每个文本字符一次比较。当模式确实匹配时，比如这里的位置零和七，我们要付出它的全部长度。",
    "f'On the whole corpus, {words(d['n'])} characters":
        "在整个语料，{words(d['n'])} 个字符上，对我们试过的每个模式，朴素方法的代价都只比每字符一次比较多一点点。英文文本对它很友好："
        "大多数位置一开始就失败，就连 the 这样的常用词，代价也不到一点一。",
    "Why is English so kind?":
        "英文为什么这么友好？<bookmark mark='a'/>在每个对齐位置，只有第一个字符匹配了才比较第二个，前两个都匹配了才比较第三个，依此类推。"
        "<bookmark mark='b'/>所以每个位置的比较次数是一，加上模式第一个字母的频率，加上它前两个字母的频率，依此类推。这些频率下降得很快："
        "小说中以 Q 开头的位置很少，以 Qu 开头的更少。<bookmark mark='c'/>用小说自己的频率来算，这个公式对实测次数的预测精确到小数点后第四位。"
        "<bookmark mark='d'/>the 这个词代价最高，因为所有位置中有百分之七以 t 开头，又有百分之二以 t h 开头。",
    "The worst case is easy to build.":
        "最坏情形很容易构造。<bookmark mark='a'/>在一段全是 a 的文本里，搜索一串以 b 结尾的 a。每个对齐位置都先匹配 m 减一个字符才失败。"
        "<bookmark mark='b'/>次数恰好是 n 减 m 加一，再乘 m：十万个字符、一千个字母的模式，要做九千九百万次比较。<bookmark mark='c'/>只有四个"
        "字母的 DNA、二进制文件，以及任何想拖慢服务器的人，都会遇到这种情形。接下来的三章会消除它。",
    # ------------------------------------------------------------------ RabinKarp
    "Chapter two. Rolling hashes.": "第2章。滚动哈希。",
    "Richard Karp and Michael Rabin, in 1987":
        "1987年，Richard Karp 与 Michael Rabin 用上了第20部分的指纹。<bookmark mark='a'/>把每个 m 个字符的窗口读成一个以 b 为底、模一个"
        "素数 p 的数，与模式的数比较。<bookmark mark='b'/>窗口滑动一位并不需要重新求和：<bookmark mark='c'/>减去离开的字符，乘以底数，再加上"
        "进来的字符。<bookmark mark='d'/>每个位置只需常数的工作量，只有两个数相等时才比较字符。<bookmark mark='e'/>如果底数是随机选的，两个不同的"
        "窗口得到同一个数，仅当一个 m 减一次的非零多项式在这个底数处为零，Schwartz–Zippel 说这的概率至多是 m 减一除以 p。",
    'f"Here is Queequeg in Moby-Dick':
        "这是用指纹在《白鲸》的 {words(d['n'])} 个字符中搜索 Queequeg，模数取不同大小的素数。<bookmark mark='a'/>模数在一百左右时，大约每一百个"
        "窗口就有一个偶然碰撞：一万两千次误报，几乎正好是我们预期的 n 除以 p。每次误报只花几次字符比较，从不导致错误答案，因为指纹相同时总要核对。"
        "<bookmark mark='b'/>模数达到一百万时，误报消失了，剩下的比较只是在确认真正的匹配。<bookmark mark='c'/>这种方法真正的长处是一次检查许多"
        "同样长度的模式：把它们的指纹放进一个哈希集合；它也能在二维上用于图像。<bookmark mark='d'/>它的后代运行着 rsync 和去重备份，即第十四章。",
    # ------------------------------------------------------------------ Kmp
    "Chapter three. Knuth, Morris and Pratt: never look back.": "第3章。Knuth、Morris 与 Pratt：从不回头。",
    "Suppose j characters of the pattern have matched":
        "假设模式的 j 个字符已经匹配，而下一个失败了。<bookmark mark='a'/>朴素方法滑动一位，重读已经看过的文本。但这 j 个文本字符正是模式的前 j 个"
        "字符，所以我们不用看就知道它们。<bookmark mark='b'/>唯一有用的问题是：模式可以移动多远，而已看到的部分仍然匹配？答案是这 j 个字符中既是"
        "真前缀又是后缀的最长者，叫作边界。<bookmark mark='c'/>移动模式使边界对齐，然后从同一个文本位置继续比较。文本只从左到右读一遍，从不回退。"
        "<bookmark mark='d'/>对模式 a b a b a c a，在 a b a b a 之后边界是 a b a，所以我们就当已经匹配了三个字符继续。这张表只由模式算出，用线性"
        "时间，方法是让模式对自己运行同样的想法。",
    "The failure table is really a finite automaton":
        "失配表其实是一个有限自动机，就是第12部分从正则表达式构造的那种。<bookmark mark='a'/>状态 q 的意思是：最后读到的 q 个字符与模式的前 q 个"
        "相同。每个匹配的字符使状态右移一格。<bookmark mark='b'/>失配时沿边界返回：在状态五读到 b，意味着最后读到的是 a b a b，即状态四。其他所有"
        "转移都回到起点。<bookmark mark='c'/>现在把文本一个字符一个字符地喂给它，完全不回溯。当它到达状态七时，模式刚好结束。",
    'f"How much work is that?':
        "这要多少工作？<bookmark mark='a'/>每次比较要么匹配，文本位置右移；要么失败，模式的起始位置右移。<bookmark mark='b'/>两者都至多右移 n 次，"
        "<bookmark mark='c'/>所以总共至多两倍 n 次比较，再加上构造表的线性工作。这是一个摊还论证，就像第16部分的倍增数组：单个字符可能花好几次比较，"
        "但平均下来从不多。<bookmark mark='d'/>第一章的最坏情形让朴素方法花了一千万次比较，这里只要 {words(d['worst_cmp'])} 次。<bookmark "
        "mark='e'/>在小说上，Knuth–Morris–Pratt 并不比朴素搜索快；但无论文本是什么，它都从不更慢。",
    # ------------------------------------------------------------------ BoyerMoore
    "Chapter four. Boyer and Moore: skip ahead.": "第4章。Boyer 与 Moore：向前跳。",
    "In 1977 Robert Boyer and J Strother Moore":
        "1977年，Robert Boyer 与 J Strother Moore 把比较的方向反了过来。<bookmark mark='a'/>把模式放在文本下面，先比较它的最后一个字符。"
        "<bookmark mark='b'/>这里文本在模式的 g 处是一个空格，而空格在 Queequeg 中根本不出现。所以任何覆盖这个空格的对齐都不可能匹配，模式可以跳过"
        "它的整个长度。<bookmark mark='c'/>如果这个字符确实出现在模式中，就滑动到刚好让它最右边的那次出现对齐。看文本中被看过的字符有多少。",
    "The full algorithm has two rules.":
        "完整的算法有两条规则。<bookmark mark='a'/>坏字符规则把失配的文本字符与它在模式中最后一次出现对齐。<bookmark mark='b'/>好后缀规则利用已经"
        "匹配的部分：模式的这个后缀必定在更左边再次出现，所以移到它的下一个副本。取两者中较大的移动。<bookmark mark='c'/>这些表的代价与模式和字母表"
        "成线性，加上 Galil 的改进，连最坏情形也是线性的。典型情形远好于线性：大约 n 除以 m 个窗口。<bookmark mark='d'/>Nigel Horspool 只保留了"
        "坏字符规则，在普通文本上几乎没有损失。<bookmark mark='e'/>这就是 grep 快的原因。它的作者 Mike Haertel 在2010年解释说，它根本不去看大部分"
        "字节。",
    "The good-suffix rule deserves an example.":
        "好后缀规则值得举个例子。<bookmark mark='a'/>这里模式 ANPANMAN 对在文本下面，从右往左比较，M A N 匹配之后出现失配。<bookmark mark='b'/>"
        "无论下一个可能的对齐在哪里，那里的文本仍以 M A N 结尾，所以模式在它下面必须有匹配的部分。<bookmark mark='c'/>ANPANMAN 没有另一个 M A N，"
        "但它的前缀 A N 是 M A N 的后缀，又是一个边界，所以模式可以滑动到那个 A N 对齐。<bookmark mark='d'/>这是移动六位而不是一位，而且这里正好"
        "落在一个匹配上；整张表在搜索开始前就由模式算好。<bookmark mark='e'/>在英文上，坏字符规则做了大部分工作，因为字母表很大；在只有四个字母的 "
        "DNA 上，好后缀规则才显出价值。",
    "We measured three random patterns of each length in Moby-Dick.":
        "我们在《白鲸》中对每种长度测量了三个随机模式。<bookmark mark='a'/>Knuth–Morris–Pratt 每个字符大约比较一次，与长度无关。<bookmark "
        "mark='b'/>Boyer–Moore 对两个字母的模式每字符大约比较半次，八个字母时六分之一，六十四个字母时二十分之一：模式越长，读的文本越少。"
        "<bookmark mark='c'/>Horspool 的简化版几乎与它完全重合。在英文上，好后缀规则很少起作用。<bookmark mark='d'/>在整个语料中找 Queequeg，"
        "Boyer–Moore 做了三百五十万次比较，比朴素方法少七倍，而 grep 搜完两千五百万字节大约只要二十毫秒。",
    # ------------------------------------------------------------------ AhoCorasick
    "Chapter five. Many patterns at once.": "第5章。一次匹配许多模式。",
    "Often we want many patterns at once":
        "我们常常想一次找许多模式：每个病毒特征码、每个禁用词、名单上的每个名字。每个模式搜一遍，就要一遍又一遍地读文本。<bookmark mark='a'/>"
        "1975年，Alfred Aho 与 Margaret Corasick 把所有模式放进一棵字典树，即它们前缀构成的树。<bookmark mark='b'/>读文本时，只要字符匹配就沿"
        "字典树往下走。失配时，沿失配链接走到已读部分仍在字典树中的最长真后缀：从 s h，链接指向 h。<bookmark mark='c'/>每个状态还列出在那里结束的"
        "所有模式：到达 s h e 时报告 she，也报告 he。<bookmark mark='d'/>这就是 Knuth、Morris 与 Pratt 的失配函数，从一条线推广到一棵树，而且"
        "文本只读一遍。",
    "How are the failure links found?":
        "失配链接是怎样找出来的？<bookmark mark='a'/>广度优先，从根开始一层一层地做。失配链接总是指向更浅的状态，所以到达一个状态时，它的链接可能"
        "需要的每个状态都已经处理过了。<bookmark mark='b'/>对状态 s 经字符 c 到达的孩子 t，从 s 自己的失配链接出发，不断沿链接走，直到某个状态有 "
        "c 孩子；<bookmark mark='c'/>t 的链接就是那个孩子。<bookmark mark='d'/>对 s h e：s h 链接到 h，而 h 有一个 e 孩子，所以 s h e 链接到 "
        "h e。<bookmark mark='e'/>每个状态还继承它所链接状态的输出，she 正是这样报告 he 的。<bookmark mark='f'/>总工作量与所有模式的总长度成线性，"
        "用的是与 Knuth–Morris–Pratt 相同的摊还论证。",
    'f"We built the automaton for {d[\'patterns\']} character names':
        "我们为小说中的 {d['patterns']} 个人物名字构造了自动机：Elizabeth、Ahab、Queequeg、Holmes、Raskolnikov 等等。<bookmark mark='a'/>"
        "字典树有 {d['states']} 个状态。在语料上走一遍用了两千五百万步。<bookmark mark='b'/>每个名字单独搜索，就要把文本读四十五遍，超过十亿个"
        "字符。<bookmark mark='c'/>这些是子串计数，所以 Jo 也算上了 John 和 Joe；真正的工具会加上词边界。<bookmark mark='d'/>同样的自动机运行在"
        "多模式的 grep、杀毒软件和网络入侵检测器里。",
    # ------------------------------------------------------------------ SuffixTree
    "Chapter six. Suffix trees.": "第6章。后缀树。",
    "What if the text, rather than the pattern, is fixed":
        "如果固定不变的是文本而不是模式，而我们要搜索它许多次呢？<bookmark mark='a'/>取 banana 加上结束标记后的每个后缀，把它们全部存进一棵树。"
        "从根出发的每条路径拼出一个子串，每片叶子是一个完整的后缀；方框标明它从哪里开始。<bookmark mark='b'/>树只在后缀开始不同的地方分叉，所以至多有 "
        "n 片叶子，分叉节点少于 n 个。<bookmark mark='c'/>边上的标签存成指向文本的两个指针，所以整棵树只占线性空间。<bookmark mark='d'/>要找一个"
        "模式，就从根往下走：m 步，与文本多长无关，走到的位置下面的叶子就是它的出现位置。a n a 停在有两片叶子的分支里，位置一和三。",
    "Building the tree naively, one suffix at a time":
        "朴素地一次插入一个后缀来构造这棵树，要走过平方级数量的字符。<bookmark mark='a'/>Esko Ukkonen 的算法改为一次扩展一个字符，把前 i 个字符"
        "的树变成前 i 加一个字符的树。<bookmark mark='b'/>两个技巧让这一步很便宜。后缀链接把 c 后接 alpha 的节点连到 alpha 的节点，于是算法可以从"
        "一个后缀跳到下一个更短的后缀，而不必从根往下走：这又是第五章的失配链接。<bookmark mark='c'/>叶子边保持开放，终点是文本当前的末尾，所以所有"
        "叶子一次同时长一个字符，不花任何代价。<bookmark mark='d'/>每一步要么加一片叶子，要么沿一条后缀链接走，摊还计数表明总工作量是线性的。"
        "<bookmark mark='e'/>与 Knuth–Morris–Pratt 和 Aho–Corasick 同样的链接、同样的记账：字符串算法一再重新发现同一个想法。",
    "Many questions become walks in this tree.":
        "许多问题都变成在这棵树上行走。<bookmark mark='a'/>最长重复子串就是最深的分叉节点。<bookmark mark='b'/>在《白鲸》中，它是一个一百个字符的"
        "章节标题，在目录里出现一次，又在该章开头出现一次。<bookmark mark='c'/>把两段文本放进同一棵树，同时有来自两者的叶子的最深节点给出它们的最长"
        "公共子串，用线性时间，而动态规划需要平方时间。<bookmark mark='d'/>不同子串的个数就是所有边的总长度：<bookmark mark='e'/>《白鲸》有七千"
        "四百一十亿个。<bookmark mark='f'/>Peter Weiner 在1973年第一个用线性时间构造出这棵树；Esko Ukkonen 1995年的算法在线构造，一次一个字符。"
        "<bookmark mark='g'/>代价是内存：文本的每个字符要十到二十个字节。对这些小说而言就是半个 GB。下一章用一小部分空间保留几乎全部的能力。",
    # ------------------------------------------------------------------ SuffixArray
    "Chapter seven. Suffix arrays.": "第7章。后缀数组。",
    "Udi Manber and Gene Myers kept the suffix tree's power":
        "Udi Manber 与 Gene Myers 用少得多的内存保留了后缀树的能力。<bookmark mark='a'/>取文本的每个后缀，按字典序排序。<bookmark mark='b'/>"
        "然后丢掉后缀本身，只保留每个后缀从哪里开始：一个由 n 个整数组成的数组，就是后缀数组。<bookmark mark='c'/>模式的每次出现都是某个后缀的开头，"
        "而以同一个模式开头的后缀在排序后彼此相邻。这里是以 t 开头的四个后缀。<bookmark mark='d'/>所以两次二分查找就能找到这一段，至多 m 乘 log n "
        "次字符比较，这一段的大小就是出现次数。",
    'f"With the suffix array and its LCP array':
        "有了后缀数组和它的 LCP 数组，最长重复子串就是两个相邻后缀的最长公共前缀中最大的那个。<bookmark mark='a'/>对整个语料，我们用 numpy 比较"
        "相邻后缀来计算它，每轮把检查的长度加倍。<bookmark mark='b'/>胜出者长 {r['length']} 个字符，而且不是正文：它是一串章节标题，第一章、"
        "第二章、第三章，与几百个字符之后它自己的一份副本重叠。<bookmark mark='c'/>只看《白鲸》，最长的重复是印了两次的章节标题。真正的正文几乎从不"
        "重复，第20部分搜索近似重复时也发现了这一点。",
    "How do you sort twenty-five million suffixes":
        "怎样给两千五百万个后缀排序，每个后缀最长可达两千五百万个字符？<bookmark mark='a'/>先按第一个字符给它们排名。<bookmark mark='b'/>然后"
        "注意到，按前两倍 k 个字符排名，就等于给数对排序：后缀前 k 个字符的排名，以及其后 k 个字符的排名，而后者正是另一个后缀的排名。<bookmark "
        "mark='c'/>不断让 k 加倍，直到每个后缀都有自己的排名：log n 轮排序。<bookmark mark='d'/>线性时间的算法也存在；2009年的 SA-IS 递归地给一部分"
        "后缀排序，再推导出其余的，快速的程序库用的就是它。<bookmark mark='e'/>同时，保存排序后每对相邻后缀的最长公共前缀，Kasai 等人说明了怎样用"
        "线性时间算出它。<bookmark mark='f'/>有了这两个数组，后缀树能回答的每个问题都能再次回答，而内存只要四分之一。",
    'f"We built the suffix array of all':
        "我们为小说的全部 {words(d['n'])} 个字符构造了后缀数组，用 numpy 的排序做前缀倍增，不到两分钟。<bookmark mark='a'/>它占一百 MB，每个字符"
        "四个字节。<bookmark mark='b'/>现在任何模式都是一对二分查找：Queequeg 的两百五十三次出现只用了一百六十七次字符比较就找到了，而扫描一遍要两千"
        "五百万次。<bookmark mark='c'/>《白鲸》的 LCP 数组表明，相邻后缀平均共享八个字符，所以二分查找每一步很少比较超过几个字符。",
    # ------------------------------------------------------------------ Bwt
    "Chapter eight. The Burrows–Wheeler transform.": "第8章。Burrows–Wheeler 变换。",
    "In 1994 Michael Burrows and David Wheeler":
        "1994年，Michael Burrows 与 David Wheeler 发表了 Wheeler 多年前就发现的一种变换。<bookmark mark='a'/>写下文本的每个旋转，这里是 banana "
        "加上结束标记。<bookmark mark='b'/>给这些旋转排序。现在第一列就是文本的字母按顺序排好。<bookmark mark='c'/>最后一列就是变换的结果：a n n b、"
        "结束标记、a a。<bookmark mark='d'/>最后一列的每个字符，是文本中紧挨在它那一行之前的字符。开头相似的行排在一起，<bookmark mark='e'/>所以"
        "它们前面的字符也聚在一起。<bookmark mark='f'/>在《白鲸》中，以 h e 开头的行将近四分之三以 t 结尾，所以排序后的文本里有同一个字母的长串。",
    "Sorting threw away the order of the text, or seemed to.":
        "排序丢掉了文本的顺序，至少看起来如此。<bookmark mark='a'/>关键事实是：最后一列的第 k 个 a 与第一列的第 k 个 a 是文本中同一个字符。"
        "<bookmark mark='b'/>以 a 开头的行按 a 后面的内容排序，以 a 结尾的行也是，因为那个 a 之后的文本正是每个旋转的其余部分。<bookmark mark='c'/>"
        "所以从以结束标记结尾的那一行出发，它就是文本本身。读它的最后一个字符，沿箭头跳到以同一个字符开头的那一行，然后重复。<bookmark mark='d'/>"
        "文本倒着出来，每跳一次一个字符。<bookmark mark='e'/>我们用这种方法反演了整部《白鲸》的变换，一字不差地得回了这部小说。",
    "Why does sorting make text more predictable?":
        "为什么排序使文本更容易预测？<bookmark mark='a'/>行是按每个位置之后的内容排序的，而最后一列存的是它之前的内容。<bookmark mark='b'/>所以变换"
        "把文本的字符按上下文分组列出：先是所有出现在 h e 之前的字符，然后是所有在 h i 之前的，依此类推。<bookmark mark='c'/>每组之内有一两个字符"
        "占主导。在 h e 之前大多是 t。<bookmark mark='d'/>因此一个适应当前分组的简单编码器，大约付出 k 阶熵，即根据旁边 k 个字符预测每个字符的代价，"
        "而且它对所有 k 同时做到，不需要被告知 k。<bookmark mark='e'/>对《白鲸》，没有上下文时是四点四比特，有一个字符时三点五，有两个字符时二点八。"
        "<bookmark mark='f'/>Giovanni Manzini 在2001年把这一点精确化了。",
    "Here is the opening of Moby-Dick, and a stretch of its transform.":
        "这是《白鲸》的开头，以及它的变换中的一段。<bookmark mark='a'/>变换里满是连续串。整部小说一百二十万个字符，只有五十多万个连续串。<bookmark "
        "mark='b'/>前移编码把每个字符替换为它在最近见过的字符列表中的位置，于是一个连续串变成一串零：<bookmark mark='c'/>熵从每字符四点四比特降到"
        "二点七。<bookmark mark='d'/>这就是 Julian Seward 在1996年发布的 bzip2 的配方：变换，前移，再加 Huffman。在这部小说上它比 zlib 的 "
        "Lempel–Ziv 好四分之一。",
    # ------------------------------------------------------------------ FmIndex
    "Chapter nine. Searching compressed text: the FM-index.": "第9章。搜索压缩文本：FM 索引。",
    "Paolo Ferragina and Giovanni Manzini saw in 2000":
        "2000年，Paolo Ferragina 与 Giovanni Manzini 看出这个变换本身就是一个索引。<bookmark mark='a'/>排好序的行就是第七章排好序的后缀，所以一个"
        "模式的所有出现是一段连续的行。倒着读模式就能找到这一段。<bookmark mark='b'/>从最后一个字符 a 开始：第一到三行以 a 开头。<bookmark "
        "mark='c'/>哪些行以 n a 开头？它们是 LF 映射把那些最后一个字符为 n 的 a 行送去的地方，而最后一列中 n 的两次计数，第一行之前和第四行之前，"
        "说明它们落在哪里：第五和第六行。<bookmark mark='d'/>对 a n a 再做一次：第二和第三行。<bookmark mark='e'/>两行，两次出现。模式的每个字符"
        "花两次 rank 查询，与文本多长无关。",
    "Real FM-indexes answer rank queries":
        "真正的 FM 索引回答 rank 查询时，并不把变换按字节存储。<bookmark mark='a'/>小波树把字母表一分为二，每个字符写一个比特：前一半写零，后一半"
        "写一。<bookmark mark='b'/>然后对每一半的字符递归地做同样的事：log sigma 层比特向量。<bookmark mark='c'/>要数位置 i 之前有多少个 n，就问顶层"
        "在 i 之前有多少个一，带着这个计数进入右孩子，再问一次。<bookmark mark='d'/>Guy Jacobson 在1989年说明了怎样只用极少的额外比特，在常数时间内"
        "回答二进制 rank。<bookmark mark='e'/>压缩这些比特向量，或者把树做成 Huffman 编码的形状，整个索引就只占大约文本压缩后的大小。",
    "Here it is on the whole corpus.":
        "这是它在整个语料上的表现。<bookmark mark='a'/>统计任何模式都只要不到一毫秒，每个字符几次 rank 查询，不管模式出现一次还是二十万次。要找出某次"
        "出现在哪里，就沿 LF 映射往回走，直到遇到一行保留了后缀数组条目；我们每三十二个保留一个。<bookmark mark='b'/>我们的教学版本把变换存成普通字节，"
        "每六十四行存一次 rank 计数，比文本还大。<bookmark mark='c'/>真正的 FM 索引用小波树把变换压缩存储，接近压缩文本的大小：这些小说的变换压缩到"
        "七 MB。所以索引比它所搜索的书还小。<bookmark mark='d'/>BWA 和 Bowtie 这样的 DNA 比对工具，正是这样把数十亿条短读段比对到人类基因组上的。",
    # ------------------------------------------------------------------ Lz
    "Chapter ten. Compression, part one: Lempel and Ziv.": "第10章。压缩（上）：Lempel 与 Ziv。",
    "In 1977 Abraham Lempel and Jacob Ziv":
        "1977年，Abraham Lempel 与 Jacob Ziv 提出了 zip、gzip 和 PNG 背后的想法。<bookmark mark='a'/>从左到右读文本。只要接下来的一段最近出现过，"
        "就不再写它：写一个数对，它有多长、在多远之前。这是《双城记》的开头。It was the、of times、it was the：每一次重复都变成一条指回它首次出现的弧。"
        "<bookmark mark='b'/>搜索在一个窗口内往回看，DEFLATE 中是三十二 KB，匹配长度从三到二百五十八个字符。<bookmark mark='c'/>快速找到最长匹配是一个"
        "哈希问题：为窗口中每个三字符前缀建索引，沿着有相同前缀的较早位置组成的链走。",
    "DEFLATE, the format inside zip and gzip":
        "DEFLATE，zip 和 gzip 里面的格式，把 Lempel–Ziv 与 Huffman 结合在一起。<bookmark mark='a'/>字面字节和匹配长度共用一个有二百八十六个符号的"
        "字母表，距离有自己的三十个。<bookmark mark='b'/>大的数值编码成一个桶加几个额外的原始比特，使 Huffman 字母表保持很小。<bookmark mark='c'/>"
        "输出的每个块带着自己的一对 Huffman 编码，而这些编码本身也被压缩。<bookmark mark='d'/>压缩器最巧妙的技巧是惰性匹配：在确定一个匹配之前，先看"
        "晚一个字符开始是否会得到更长的匹配。这正是我们的简单版本主要缺少的。<bookmark mark='e'/>从一到九的级别在压缩器搜索得多努力与速度之间权衡，"
        "而解压总是很快，不过是复制字节。<bookmark mark='f'/>Phil Katz 在1993年为 PKZIP 设计了它；它在1996年成为标准，从此无处不在。",
    "A year later Ziv and Lempel gave a second scheme.":
        "一年后，Ziv 与 Lempel 给出了第二种方案。<bookmark mark='a'/>维护一个短语词典。读出词典中已有的最长短语，写下它的编号，再把这个短语加上下一个"
        "字符作为新条目加入词典。<bookmark mark='b'/>短语一次长一个字符，所以文本中常见的片段很快就有了自己的编号。<bookmark mark='c'/>Terry Welch 的"
        "变体 LZW 一开始就把每个单字节放进词典。Unix 的 compress 命令和 GIF 图像用的就是它。<bookmark mark='d'/>Ziv 与 Lempel 证明了一件了不起的事："
        "对任何平稳遍历的信源，每字符的比特数趋于信源的熵率，即可能的最好结果。<bookmark mark='e'/>这种方法是通用的。它不需要文本的模型，只需要足够多的"
        "文本。",
    "We wrote an LZ77 compressor with hash chains":
        "我们写了一个带哈希链的 LZ77 压缩器，像 DEFLATE 那样用 Huffman 编码给它的输出计价，在三部小说上运行。<bookmark mark='a'/>在《白鲸》上它找到"
        "二十二万个匹配，平均大约五个字符长，只有两万三千个字符需要直接写出。<bookmark mark='b'/>它与最强设置下的 zlib 相差不到百分之六，zlib 多了惰性"
        "匹配，在确定之前先试晚一个位置。LZW 差不多一样好。<bookmark mark='c'/>会排序的 bzip2 在小说上做得更好，xz 又更好，因为它对每个匹配之后可能"
        "出现什么建模。<bookmark mark='d'/>DEFLATE，即 Lempel–Ziv 加 Huffman，存在于每个 zip 文件、每张 PNG 图像和每个压缩过的网页中。",
    # ------------------------------------------------------------------ Entropy
    "Chapter eleven. Compression, part two: coding the symbols.": "第11章。压缩（下）：给符号编码。",
    "Lempel–Ziv finds the repetition; then the symbols must be written in bits.":
        "Lempel–Ziv 找出重复；然后还得把符号写成比特。<bookmark mark='a'/>Shannon 说，概率为 p 的符号值 log 一除以 p 个比特，平均值就是熵。"
        "<bookmark mark='b'/>第19部分的 Huffman 编码给每个符号整数个比特，与熵相差不到一比特。<bookmark mark='c'/>通常这就够了。但设想一个信源，"
        "其中一个符号的概率是百分之九十五：它的熵每符号不到十分之三比特，而 Huffman 仍然给每个符号花一整个比特，多了三倍以上。<bookmark mark='d'/>"
        "最后一列 rANS，在每种偏斜度下都只比熵多不到百分之一。<bookmark mark='e'/>在《白鲸》的字节上，没有哪个符号占主导，Huffman 的整数比特只多花"
        "不到百分之一。",
    "Arithmetic coding solved this in the 1970s":
        "算术编码在1970年代解决了这个问题，把整条消息当作一个数，但它很慢。<bookmark mark='a'/>Jarek Duda 的非对称数字系统把消息保存为一个整数 x，"
        "把每个符号推入其中。<bookmark mark='b'/>用 x 除以符号的频率，乘以总数，再加上余数和符号的偏移。<bookmark mark='c'/>这里 f 是符号在 M 中所占的"
        "频率。<bookmark mark='d'/>每一步大约把 x 乘以一除以符号的概率，所以比特数恰好增加它的信息量。<bookmark mark='e'/>实际中，x 通过不断输出低位"
        "字节而保持在一个机器字之内，解码则把同样的算术倒过来运行。<bookmark mark='f'/>Duda 在2009到2014年间发表的工作，使熵编码像算术编码一样紧凑，"
        "又像 Huffman 一样快。zstd、Apple 的 LZFSE 和 JPEG XL 里都有它。我们用四十行写了一个按字节工作的版本；它在每个测试上都能还原。",
    "With a coder that reaches the entropy":
        "有了一个能达到所给概率之熵的编码器，剩下的唯一问题就是这些概率有多好。<bookmark mark='a'/>把《白鲸》的每个字节单独看，熵是四点四比特。知道"
        "前一个字节时三点五。知道前两个时二点八。<bookmark mark='b'/>预测越好，比特越少：压缩就是预测。<bookmark mark='c'/>这是一条从 PPM 经上下文"
        "混合通往 AI 系列中语言模型的路，那个系列的第一部分发现，它们是我们拥有的最好的文本压缩器。<bookmark mark='d'/>在另一端，Yann Collet 的 zstd "
        "结合了 Lempel–Ziv、Huffman 和 ANS，为速度而调校，如今是世界上大量基础设施的默认压缩器。",
    # ------------------------------------------------------------------ Align
    "Chapter twelve. Alignment.": "第12章。序列比对。",
    "Part 19's edit distance becomes, in biology, an alignment.":
        "第19部分的编辑距离，在生物学中变成了比对。<bookmark mark='a'/>1970年，Saul Needleman 与 Christian Wunsch 填写了同样的表格，但是用要最大化"
        "的得分：字母匹配有奖励，失配和空位有罚分。<bookmark mark='b'/>每个格子取三者中最好的：用一对字符延长比对，或在任一边加一个空位。<bookmark "
        "mark='c'/>这里是 intention 对 execution，第19部分的例子。<bookmark mark='d'/>真正的生物学用从进化中学来的替换矩阵给氨基酸打分，而且开启"
        "一个空位比延长它罚得更多，因为一次长的插入比许多次短的更可能。",
    "Often only part of two texts is related.":
        "两段文本常常只有一部分相关。<bookmark mark='a'/>Temple Smith 与 Michael Waterman 给每个格子加了第四个选择：零，意思是在这里重新开始一段"
        "比对。<bookmark mark='b'/>最好的局部比对是表中任何位置的最高格子，往回追溯直到得分降为零。<bookmark mark='c'/>这是《基督山伯爵》中那封匿名信"
        "的两个版本，第20部分的 MinHash 标出了它们。Smith–Waterman 找到它们共有的那一段，逐词对齐，绕过第二个版本改写过的地方。",
    "Real gaps are not independent.":
        "真实的空位并不相互独立。<bookmark mark='a'/>生物学和 diff 都偏爱一个长空位而不是许多短空位，所以长度为 l 的空位花一笔开启费，再加每个字符一笔"
        "小费用。<bookmark mark='b'/>单张表格无法这样计价，因为一个格子不知道它的邻居是否已经在空位之中。<bookmark mark='c'/>Osamu Gotoh 的办法是保留"
        "三张表：M 表示以一对字符结尾的比对，<bookmark mark='d'/>X 表示以一个串中的空位结尾的，<bookmark mark='e'/>Y 表示另一个串中的空位。在 X 或 Y "
        "之内移动只付延长费；从 M 进入它们要付开启费。<bookmark mark='f'/>时间仍是两个长度之积，第19部分 Hirschberg 的分治技巧把内存降到线性。",
    "The table is quadratic, and genomes are long.":
        "表格是平方级的，而基因组很长。<bookmark mark='a'/>两个人类基因组需要十的十八次方个格子。<bookmark mark='b'/>1990年的 BLAST，是全部科学中被"
        "引用最多的论文之一，它用哈希表找出短的精确种子，只在种子周围延长比对。<bookmark mark='c'/>现代的读段比对工具用第九章的 FM 索引找种子。"
        "<bookmark mark='d'/>满足于启发式方法是有原因的：真正次平方时间的精确编辑距离算法，会推翻强指数时间假设，即第19部分的前沿和第27部分的主题。"
        "<bookmark mark='e'/>我们能做的是利用相似性：当距离 d 很小时，只有表格的一条带有关，工作量是 n 乘 d。下一章正是这样做的。",
    # ------------------------------------------------------------------ Diff
    "Chapter thirteen. Myers' diff.": "第13章。Myers 的 diff。",
    "Every git diff answers one question":
        "每次 git diff 都回答一个问题：把一个文件变成另一个，最短的行插入和删除列表是什么？Gene Myers 把它画成一张图。<bookmark mark='a'/>把旧文件的行"
        "放在上边，新文件的行放在左边。<bookmark mark='b'/>向右一步删除旧文件的一行，向下一步插入新文件的一行；每步花费一。<bookmark mark='c'/>只要两行"
        "相等就有一条对角线，它保留这一行，不花任何代价。<bookmark mark='d'/>一个 diff 是从左上角到右下角的一条路径，最好的 diff 就是最短路径，即第18部分"
        "的问题，在网格上。<bookmark mark='e'/>对 Myers 自己的例子，A B C A B B A 对 C B A B A C，五次编辑，并尽可能多地走免费的对角线。",
    "Dijkstra's algorithm would work, but Myers found something better in 1986.":
        "Dijkstra 算法也行，但 Myers 在1986年找到了更好的办法。<bookmark mark='a'/>用 x 减 y 给对角线编号。有 D 次编辑的路径只能停在负 D 到 D 的对角线"
        "上。<bookmark mark='b'/>对 D 等于零、一、二，依此类推，每条对角线只保留沿它走得最远的那条路径。<bookmark mark='c'/>每条新路径是最好的邻居路径加"
        "一次编辑，然后沿它能走的每条免费对角线滑下去，Myers 称之为蛇。<bookmark mark='d'/>第一条到达角落的路径就是一个最短的 diff，用 n 加 m 再乘 D 的"
        "工作量，所以相似的文件很快。<bookmark mark='e'/>Bram Cohen 的 patience diff 先锚定在每个文件中恰好出现一次的行上，这能让代码块保持完整。"
        "<bookmark mark='f'/>而三方合并，git merge 的核心，把两个分支分别与它们的共同祖先做 diff，只在两边都改了同样的行时才报告冲突。",
    'f"We ran our Myers diff':
        "我们把自己的 Myers diff 运行在这门课自己教学大纲的每一次修改上，{d['revisions']} 个版本，这个文件现在已超过三千行。<bookmark mark='a'/>第一次"
        "大改写改了一千四百行，在 Python 中用了半秒。<bookmark mark='b'/>大多数提交只改几行，只要几毫秒：n 乘 D 中的 D 在起作用。<bookmark mark='c'/>"
        "我们用经典的平方时间最长公共子序列计算核对了每个结果；全都是最小的。<bookmark mark='d'/>git 自己的 diff，即使加上 minimal 选项，在 {len(rows)} "
        "次修改中有 {diffs} 次多出两到四行。git 先把它判断为无用的行放到一边，这种为速度而设的启发式偶尔会多花一两行。",
    # ------------------------------------------------------------------ Rsync
    "Chapter fourteen. Rolling hashes at scale: rsync and chunking.": "第14章。大规模的滚动哈希：rsync 与分块。",
    "You have last week's copy of a large file":
        "你有一个大文件上周的副本，服务器有今天的版本，区别只是中间插入了一句话。怎样更新你的副本而不必全部下载？<bookmark mark='a'/>直接的方案是把两个"
        "文件切成固定的块，只发送哈希不同的块。<bookmark mark='b'/>但插入会让它之后的一切都移位。我们在《白鲸》中间插入了二十四个字节：<bookmark "
        "mark='c'/>一半的固定块现在都不同了，尽管几乎什么都没变。",
    'f"Andrew Tridgell and Paul Mackerras':
        "Andrew Tridgell 与 Paul Mackerras 1996年的 rsync 用滚动哈希解决了这个问题。<bookmark mark='a'/>接收方对它的每个块算两次哈希，一次弱的，一次"
        "强的，然后发送这个列表。<bookmark mark='b'/>发送方在新文件上一次一个字节地滑动窗口，在任何偏移处寻找任何旧块。<bookmark mark='c'/>弱校验和由"
        "两个累加和组成，窗口滑动时用常数时间更新，就像第二章的指纹。<bookmark mark='d'/>只有弱校验和匹配时，才检查代价高的强哈希。<bookmark "
        "mark='e'/>对我们修改过的《白鲸》，{d['rsync_matched']} 个旧块在原位或移位后被找到，只有大约三 KB 需要作为字面文本发送。",
    'f"rsync needs the old file':
        "rsync 需要旧文件的块哈希，而一个有数百万文件的备份系统负担不起把它们全部保存。<bookmark mark='a'/>基于内容的分块把这个想法倒过来。让内容决定"
        "在哪里切：在字节上运行滚动哈希，在它的值以十三个零结尾的地方切开，加上最小块大小的限制，大约每十 KB 切一次。<bookmark mark='b'/>插入只改变它"
        "附近的哈希，所以它之后的切点落在与以前相同的地方。<bookmark mark='c'/>《白鲸》被切成 {d['cdc_chunks']} 块；修改之后，恰好只有一块是新的，"
        "十四 KB。<bookmark mark='d'/>每块只按它的哈希存一次，一个缓慢变化的磁盘的一千次夜间备份，代价比一次多不了多少。去重备份工具和云文件同步就是"
        "这样工作的。",
    # ------------------------------------------------------------------ Period
    "Chapter fifteen. Periods, palindromes and Lyndon words.": "第15章。周期、回文与 Lyndon 词。",
    "Some structure lives inside a single string.":
        "有些结构存在于单个字符串之内。<bookmark mark='a'/>如果一个字符串的每个字符都等于 p 位之后的那个，它就有周期 p。这个串有周期五和八。<bookmark "
        "mark='b'/>周期恰好是 n 减去第三章的边界，所以失配函数把它们全部列了出来。<bookmark mark='c'/>Nathan Fine 与 Herbert Wilf 在1965年证明：如果"
        "一个字符串有周期 p 和 q，且长度至少是 p 加 q 减去它们的最大公约数，那么这个公约数也是它的周期。<bookmark mark='d'/>五和八的公约数是一，所以有这"
        "两个周期的十二个字符的串只能是同一个字母的重复；我们的串只有十一个字符，逃过了这一点，这说明这个界是紧的。<bookmark mark='e'/>正是这个引理让快速"
        "匹配器能向前跳而不漏掉任何东西；Crochemore 与 Perrin 的双向算法，即 C 库 memmem 内部的算法，就依赖于它。",
    "What is the longest palindrome in the novels?":
        "这些小说中最长的回文是什么？<bookmark mark='a'/>围绕每个可能的中心向外扩展，对一串 a 这样的文本是平方级的。<bookmark mark='b'/>Glenn Manacher "
        "1975年的算法注意到，在已经找到的回文之内，每个中心都对应另一侧的一个镜像，所以它的半径可以从镜像的半径开始，而不必从零开始。<bookmark "
        "mark='c'/>最远回文的右边界只会向右移动，这使整个扫描是线性的。<bookmark mark='d'/>我们在全部三十部小说的字母上运行它，共一千九百万个，忽略单个"
        "字母的连续串。胜出者有十九个字母，是《尤利西斯》里的 Lenehan：able was I ere I saw Elba。",
    "One more piece of structure.":
        "再看一种结构。<bookmark mark='a'/>Lyndon 词按字典序严格小于它的每一个旋转。<bookmark mark='b'/>陈国才、Ralph Fox 与 Roger Lyndon 证明，"
        "每个字符串都能以唯一的方式分解为一串不递增的 Lyndon 词。<bookmark mark='c'/>banana 是 b、an、an、a。mississippi 是 m、iss、iss、ipp、i。"
        "<bookmark mark='d'/>Jean-Pierre Duval 用线性时间和常数额外内存找到了这种分解。<bookmark mark='e'/>这听起来像是一件奇事，但它给出了不需要结束"
        "标记的 Burrows–Wheeler 变换，而 Lyndon 词是2017年那个证明的关键：长度为 n 的字符串的极大重复少于 n 个。",
    # ------------------------------------------------------------------ Frontier
    "Chapter sixteen. Frontier: indexes as small as the information.": "第16章。前沿：和信息量一样小的索引。",
    "The frontier concerns texts that repeat themselves.":
        "前沿关注的是自我重复的文本。<bookmark mark='a'/>数一数 Burrows–Wheeler 变换中的连续串个数，记作 r。对六点五 MB 的小说，每个连续串大约两个"
        "字符。对这门课教学大纲全部二十七个版本拼接起来的同样长度的文本，只有十三万个连续串：每个五十个字符。<bookmark mark='b'/>xz 把这些版本压缩了"
        "六十倍。<bookmark mark='c'/>这样的集合到处都是：有版本的文档、每个软件项目的历史，最重要的是基因组。<bookmark mark='d'/>一个泛基因组包含数千个"
        "人类基因组，每个与其他的有百分之九十九点九相同。<bookmark mark='e'/>FM 索引的大小跟随文本的统计熵，而统计熵几乎察觉不到一个基因组重复了另一个。"
        "对这样的集合，它太大了。",
    "The answer is an index whose size depends on r.":
        "答案是一种大小取决于 r 的索引。<bookmark mark='a'/>把变换存成它的连续串，向后搜索只需在连续串的边界上做 rank 查询。<bookmark mark='b'/>多年来"
        "的障碍是定位：每 s 行一个后缀数组样本，代价是 n 除以 s，远大于 r。<bookmark mark='c'/>2018年，Travis Gagie、Gonzalo Navarro 与 Nicola Prezza "
        "证明，只在连续串的端点采样后缀数组就够了，得到一个 r 阶个字的完整索引，每次出现用 log log n 时间报告。<bookmark mark='d'/>后来的工作在同样的空间"
        "内让每一步 LF 只需常数时间。<bookmark mark='e'/>那么 r 与 Lempel–Ziv 的短语数 z 相比有多大？Dominik Kempa 与 Tomasz Kociumaka 在2020年证明 r "
        "至多是 z 乘以 log n 的平方，解决了一个长期存在的猜想。<bookmark mark='f'/>一整个重复度度量的阶梯已经建立起来，开放的问题是快速索引能在上面降到"
        "多低。",
    "The other frontier is the wall that chapter twelve ran into.":
        "另一个前沿是第十二章撞上的那堵墙。<bookmark mark='a'/>除非强指数时间假设不成立，编辑距离、最长公共子序列和动态时间规整都没有真正次平方的算法。"
        "<bookmark mark='b'/>但输入常常是可压缩的，比对可以在 Lempel–Ziv 短语而不是字符上进行，从而加速。<bookmark mark='c'/>近似完全绕过了这堵墙：在"
        "几乎线性的时间内得到常数倍的近似。<bookmark mark='d'/>而当距离 d 很小时，Landau 与 Vishkin 的算法用 n 加 d 的平方时间，这正是 diff 在相似文件上"
        "很快背后的理论。",
    "Here is where things stand.":
        "现状如下。<bookmark mark='a'/>是否存在一种索引，大小为 Lempel–Ziv 短语的个数，并且统计任何模式出现次数的时间接近模式的长度？<bookmark "
        "mark='b'/>编辑距离能否在近线性时间内近似到一加 epsilon 倍以内？<bookmark mark='c'/>长度为 n 的字符串到底最多能有多少个极大重复？少于 n 个，但"
        "确切的常数未知。<bookmark mark='d'/>这一部分的研究题针对第一个问题。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们构造了：朴素搜索及其最坏情形；滚动哈希；Knuth、Morris 与 Pratt 的自动机；Boyer 与 Moore 的跳跃；一次匹配许多模式的 Aho–Corasick。"
        "为全部小说构造的后缀树和后缀数组。Burrows–Wheeler 变换和 FM 索引。Lempel–Ziv、Huffman 和 ANS。比对、Myers 的 diff、rsync 和基于内容的分块。"
        "周期、回文与 Lyndon 词。",
    "Where this comes back.":
        "它们会在哪里再出现。第27部分证明编辑距离平方之墙背后的条件下界。第28部分在信息论中加入噪声，构造纠错码。第34和35部分压缩存储引擎和列式存储。"
        "第41部分在 Myers 的 diff 之上构造 git 的合并，在增量压缩之上构造它的 packfile。第47部分的搜索引擎用到倒排索引和近似重复检测，第57部分把学习"
        "与压缩联系起来。",
    "In practice. grep and ripgrep":
        "在实践中。grep 和 ripgrep 结合了 Boyer–Moore 循环、自动机和向量指令。你见过的每个压缩文件，要么是 Lempel–Ziv，要么是 Burrows–Wheeler 变换，"
        "或者两者都有，底层是 Huffman 或 ANS。DNA 比对工具搜索 FM 索引并使用 BLAST 的种子。git 用 Myers 算法及其变体做 diff，rsync 和去重备份依靠"
        "滚动哈希。",
    "Six problems, with full solutions in the part's notes.":
        "六道题，完整解答在这一部分的笔记里。可以在任何一题上暂停。第五题是构造题：用 Pebble 语言写 Horspool 搜索，在模拟器上运行于这些小说。最后一题"
        "标有星号，是研究题：它的答案未知，笔记里说明了从哪里入手。",
    "Next time, geometry.":
        "下一次，几何。它看起来很简单，直到计算机算错：一个浮点数的方向测试可能会说某个点同时位于一条直线的两侧。把谓词做对，美丽的结构就随之而来：凸包、"
        "由抛物线海滩线生长出的 Voronoi 图，以及作为抛物面上凸包之投影的 Delaunay 三角剖分。第22部分，几何。",
    "The books and papers this part follows":
        "这一部分所依据的书籍和论文显示在屏幕上，也列在笔记里。感谢观看。",
}

PHRASES = {}
