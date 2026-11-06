"""Chinese narration for cs28: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第28部分：纠错码"

CHAPTERS = {
    "Hook": "被划伤的消息",
    "Channel": "1. 噪声与重复",
    "Distance": "2. 汉明距离",
    "Hamming": "3. 汉明(7,4) 码",
    "Bounds": "4. 一个码能有多好？",
    "Fields": "5. 有限域",
    "ReedSolomon": "6. Reed–Solomon 码",
    "Qr": "7. 我们的二维码",
    "Crc": "8. 循环码与 CRC",
    "Shannon": "9. Shannon 定理",
    "Viterbi": "10. 卷积码与 Viterbi 算法",
    "Ldpc": "11. LDPC 码与置信传播",
    "Polar": "12. 极化码",
    "Storage": "13. 存储用的码",
    "Frontier": "14. 前沿：容量与局部性",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In 1947 Richard Hamming was running calculations on a relay computer at Bell Labs.":
        "1947年，Richard Hamming 在贝尔实验室的一台继电器计算机上跑计算。工作日里，出错的作业有操作员重启；到了周末，没有人在。<bookmark "
        "mark='a'/>这台机器用五中取二码存储每一位数字，所以能检测出坏掉的一位。检查一旦报警，它就丢下这个作业去做下一个，到了星期一，Hamming "
        "发现自己的工作没了。<bookmark mark='b'/>他后来这样讲这个故事：既然机器能检测出错误，为什么不能找到错误的位置并把它纠正？<bookmark "
        "mark='c'/>他在1950年发表的答案，开创了纠错码的理论。早两年，Claude Shannon 已经证明了这种码最远能走多远。填平两者之间的差距用了五十年，"
        "这一部分就沿着这条路走。",
    "Here is a code you use every day.":
        "这是一种你每天都在用的码。<bookmark mark='a'/>这个二维码有二十五乘二十五个方块，装着四十四个字节：二十二个是消息，二十二个是校验。你可以"
        "扫一扫。<bookmark mark='b'/>现在把它中间涂掉一块。四十四个字节里有八个错了，而且解码器并不知道是哪八个。<bookmark mark='c'/>它照样读出来："
        "CS, Built, Part 28。<bookmark mark='d'/>到这一部分结束时，我们会亲手搭好每一步：有限域、Reed-Solomon 码，以及找回这条消息的解码器。",
    "Part 28 of Computer Science, Built: Error-Correcting Codes.":
        "计算机科学，从零搭建，第28部分：纠错码。<bookmark mark='a'/>这一部分包括：有噪信道和最简单的码；汉明距离和汉明码；任何码能好到什么程度的"
        "极限，以及一个完美码；有限域、Reed-Solomon 码和我们自己的二维码；用第5部分的移位寄存器搭成的循环冗余校验；Shannon 定理，以及终于达到它的"
        "那些码；存储用的码；还有前沿。",
    # ------------------------------------------------------------------ Channel
    "Chapter one. Noise and repetition.": "第1章。噪声与重复。",
    "Shannon's simplest model of noise is the binary symmetric channel.":
        "Shannon 最简单的噪声模型是二元对称信道。<bookmark mark='a'/>每一位以一减 p 的概率原样通过，以 p 的概率翻转，与其他每一位都相互独立。"
        "<bookmark mark='b'/>它很粗糙，但被宇宙射线击中的存储单元、划花的光盘和微弱的无线电，大体上都像这样。<bookmark mark='c'/>还有别的信道：在"
        "擦除信道里，一位丢了，但你知道是哪一位；真实的噪声也常常成串出现。<bookmark mark='d'/>对付它们，工具都一样：加入冗余，让接收方能把损伤"
        "撤销。",
    "Here is what noise does to a picture, and what codes do about it.":
        "这是噪声对一幅图做的事，以及码能怎样应对。<bookmark mark='a'/>一幅三千八百四十个像素的黑白图像。<bookmark mark='b'/>原样通过一个每二十位"
        "翻转一位的信道，它满是斑点地到达：一百七十九个像素错了。<bookmark mark='c'/>每个像素发三遍再表决，错误降到二十二个，但流量变成三倍。"
        "<bookmark mark='d'/>汉明码，也就是第3章的码，错六十个，而发送的位数还不到两倍。哪种交换更划算取决于信道；这一部分的其余内容，就是要比两者"
        "都做得更好。",
    "The obvious code: say everything several times.":
        "最显然的码：每句话说好几遍。<bookmark mark='a'/>每一位发送 n 次，让接收方做多数表决。只有超过一半的副本翻转，它才会出错。<bookmark "
        "mark='b'/>在每十位翻转一位的信道上，三份副本把错误降到百分之三以下，九份降到千分之一以下。但码率，也就是信道中承载真实数据的比例，按 n "
        "分之一下降。<bookmark mark='c'/>二十五份副本把错误降到大约六百万分之一，这时只有百分之四的信道在承载数据。<bookmark mark='d'/>1940年代的"
        "工程师以为这是一条定律：可靠性越高，代价就是码率越低，没有尽头。Shannon 证明了它是错的，第9章会讲。不过先来看一幅图。",
    # ------------------------------------------------------------------ Distance
    "Chapter two. Hamming distance.": "第2章。汉明距离。",
    "Hamming's first idea was a way to measure how different two words are.":
        "Hamming 的第一个想法，是一种衡量两个字有多不同的办法。<bookmark mark='a'/>汉明距离数出它们不同的位置：这两个字在两处不同。<bookmark "
        "mark='b'/>它像一个真正的距离：从 x 到 z 的代价，绝不会超过经过 y 的代价。<bookmark mark='c'/>在二元对称信道上，每多一次翻转，收到的字"
        "就更不可能出现，所以最可能被发送的码字，就是离收到的字最近的那个。<bookmark mark='d'/>解码变成了几何：找最近的码字。",
    "Picture all words of three bits as the corners of a cube.":
        "把所有三位的字想象成一个立方体的顶点。<bookmark mark='a'/>每一位是一个坐标轴，每条棱是一次翻转。重复码只用两个顶点，零零零和一一一，相隔"
        "三条棱。<bookmark mark='b'/>在每个码字周围画一个球：一次翻转能到达的字。两个球互不接触，所以任何一次翻转，都能退回到较近的码字来纠正。"
        "<bookmark mark='c'/>在四维里，取含偶数个一的八个字，也就是超立方体每隔一个的顶点。任意两个至少相距二。<bookmark mark='d'/>一次翻转落到一个"
        "奇数的字上，所以能被检测出来；但那个字离好几个码字一样近：这个错误无法纠正。",
    "The smallest distance between two codewords decides what a code can do.":
        "两个码字之间的最小距离，决定了一个码能做什么。<bookmark mark='a'/>距离为 d 时，至多 d 减一次翻转永远不能把一个码字变成另一个，所以总能被"
        "检测出来。而至多 d 减一的一半次翻转能被纠正，因为这个半径的球互不重叠。<bookmark mark='b'/>也可以折中：纠正少数错误，同时检测更多。"
        "<bookmark mark='c'/>擦除比错误便宜。如果你知道哪些位置缺了，其中任意 d 减一个都能补上，因为只有一个码字与剩下的部分吻合。第7章的二维码正要"
        "用到这一点。",
    # ------------------------------------------------------------------ Hamming
    "Chapter three. Hamming's code.": "第3章。汉明码。",
    "Hamming's construction fits in a picture.":
        "Hamming 的构造可以装进一幅图。<bookmark mark='a'/>画三个互相重叠的圆。把四个数据位，这里是一零一一，放在四块重叠区域里，再在每个圆独占的"
        "区域放一个校验位，使每个圆里一的个数都是偶数。<bookmark mark='b'/>为四位数据发送七位。<bookmark mark='c'/>现在信道翻转了其中一位。<bookmark "
        "mark='d'/>接收方重新数一遍：圆 A 和 C 是奇数，B 仍是偶数。翻转的那一位一定在 A 和 C 里面、B 外面，而只有一块区域是这样：它是 d 二。"
        "<bookmark mark='e'/>七个位置中的每一个都落在一种不同的圆的组合里，所以任何一次翻转都能被定位并纠正；没有翻转时，每个圆都是偶数。",
    "The same code as a matrix.":
        "同一个码，写成矩阵。<bookmark mark='a'/>把一到七的二进制写成一个三行矩阵 H 的各列。<bookmark mark='b'/>码字就是被 H 映到零的字；H 的每一行"
        "就是三个圆中的一个。<bookmark mark='c'/>如果信道翻转了第 j 位，乘以 H 就得到第 j 列：伴随式用二进制拼出了错误的位置。我们翻转过的字给出一零"
        "一：五。<bookmark mark='d'/>这个构造对任意个校验 r 都成立：二的 r 次方减一个位置，其中除 r 个之外全是数据。<bookmark mark='e'/>而且这个码"
        "是完美的：十六个码字周围半径为一的球各含八个字，合起来恰好把长度为七的全部一百二十八个字各覆盖一次。没有浪费任何空间。",
    "Hamming's construction gives a whole family.":
        "Hamming 的构造给出一整个家族。<bookmark mark='a'/>用 r 个校验时，块长是二的 r 次方减一，码率逐渐逼近一：r 等于七时，七个校验带一百二十位"
        "数据。但每一块不论多长，都仍然只能纠正一个错误。<bookmark mark='b'/>所以长的汉明码适合错误罕见又孤立的信道，比如内存。<bookmark "
        "mark='c'/>最后一行就是你服务器里的那种：六十四个数据位、七个汉明校验位和一个总奇偶位，每个内存字七十二位。",
    "How much does it help?":
        "它帮了多大忙？<bookmark mark='a'/>用对数刻度看：不编码时，错误率就是 p。三倍重复大致把它平方，代价是三分之一的码率。汉明码以七分之四的码率"
        "做得差不多一样好。在每一百位翻转一位时，汉明码留下的错误不到万分之九，而不是一百。<bookmark mark='b'/>模拟的点与精确曲线吻合。<bookmark "
        "mark='c'/>汉明码至今无处不在。纠错内存给每个64位的字配八个校验位：一个汉明码加一个总奇偶位。<bookmark mark='d'/>它能纠正任何一次翻转，"
        "检测任何两次：这是抵御宇宙射线、以及第5部分的 Rowhammer 攻击的一部分防线，不过攻击者后来找到了一次翻转好几位的办法。",
    # ------------------------------------------------------------------ Bounds
    "Chapter four. How good can a code be?": "第4章。一个码能有多好？",
    "Every code trades rate for distance.":
        "每个码都在用码率换距离。<bookmark mark='a'/>对长码，把码率对相对距离作图，也就是最小距离除以码长：相对距离为 delta 的码能纠正 delta 一半"
        "比例的错误。<bookmark mark='b'/>有些极限很容易。Singleton 界：码率加相对距离至多为一。汉明界：码字周围的球必须装得下。还有 McEliece、"
        "Rodemich、Rumsey 和 Welch 的线性规划界，在距离大时是已知最好的。没有任何码能高过其中最低的那条。<bookmark mark='c'/>从下面看，Edgar Gilbert "
        "和 Rom Varshamov 证明了随机码能达到一减 delta 的熵。<bookmark mark='d'/>两者之间有一道缝隙，它已经悬而未决了将近七十年。<bookmark "
        "mark='e'/>没有人知道哪一族长的二元码能胜过随机码。",
    "A few codes meet Hamming's bound exactly.":
        "有几个码恰好达到汉明界。<bookmark mark='a'/>1949年，Marcel Golay 发表了一个长度二十三、携带十二位的码，由这个多项式生成。<bookmark "
        "mark='b'/>我们列出了全部四千零九十六个码字。最轻的非零码字重量为七，所以这个码能纠正任意三个错误。<bookmark mark='c'/>半径为三的球含两千"
        "零四十八个字，四千零九十六个这样的球恰好填满全部二的二十三次方个字。这个码是完美的。<bookmark mark='d'/>Aimo Tietäväinen 在1973年证明，"
        "重复码、汉明码和这个码，是仅有的完美二元码。<bookmark mark='e'/>它的扩展版本传回了旅行者号拍摄的木星和土星彩色照片。<bookmark mark='f'/>"
        "它还能搭出 Leech 格：Henry Cohn 等人在2017年基于 Maryna Viazovska 的方法证明，这是二十四维里堆积球最密的方式。",
    # ------------------------------------------------------------------ Fields
    "Chapter five. Finite fields.": "第5章。有限域。",
    "The codes of the next chapters compute with polynomials,":
        "接下来几章的码都用多项式计算，所以需要一种数：行为像有理数，但数量有限。<bookmark mark='a'/>这就是域：可以加、减、乘，并且可以除以除零之外"
        "的任何数。<bookmark mark='b'/>模一个素数的整数构成一个域。在这张模七的乘法表里，每一行恰好有一个1，所以每个非零数都有逆。<bookmark "
        "mark='c'/>模八就不行：二乘四等于零，二没有逆。<bookmark mark='d'/>在任何域里，d 次的非零多项式至多有 d 个根。Reed-Solomon 码就靠这一个"
        "事实撑起来。<bookmark mark='e'/>Évariste Galois 发现，每个素数的幂都有一个有限域，其他大小都没有。",
    "Computers want a field whose elements are bytes.":
        "计算机想要一个元素是字节的域。两百五十六是二的八次方，所以这样的域存在。<bookmark mark='a'/>把一个字节读作一个多项式，它的各位就是系数。"
        "<bookmark mark='b'/>加法是异或。乘法：把多项式相乘，再对一个固定的、不能分解的八次多项式取余；二维码用的就是这一个。<bookmark mark='c'/>"
        "现在取 alpha，也就是字节二，它代表 x，不断乘它：一、二、四，一直到一百二十八，然后取余开始起作用，得到二十九。<bookmark mark='d'/>在序列"
        "重复之前，全部两百五十五个非零字节恰好各出现一次。alpha 生成了整个域。<bookmark mark='e'/>所以每个非零字节都是 alpha 的某次幂，乘法变成"
        "指数相加：两次查表加一次加法，就像计算尺用对数做乘法。<bookmark mark='f'/>而乘以 alpha 本身，是一次移位加一次有条件的异或：恰好就是第5部分"
        "的线性反馈移位寄存器。",
    "Why that polynomial?":
        "为什么是那个多项式？<bookmark mark='a'/>系数是比特的八次多项式共有两百五十六个。其中三十个不能分解，这三十个中任何一个都能搭出一个两百五十六"
        "个元素的域；事实上它们搭出的都是同一个域，只是标号不同。<bookmark mark='b'/>其中十六个还是本原的：x 的各次幂走遍每个非零字节。二维码用的是"
        "其中一个。<bookmark mark='c'/>第29部分的 AES 用的是一个不可约但不是本原的多项式，所以它的表是用 x 加一的各次幂造的。<bookmark mark='d'/>"
        "我们用暴力全部检查了一遍；Gauss 的计数公式预言了三十，Euler 函数预言了十六。",
    # ------------------------------------------------------------------ ReedSolomon
    "Chapter six. Reed-Solomon codes.": "第6章。Reed-Solomon 码。",
    "In 1960 Irving Reed and Gustave Solomon turned the root-counting fact into a code.":
        "1960年，Irving Reed 和 Gustave Solomon 把数根的事实变成了一种码。<bookmark mark='a'/>把消息，这里是三个数，读作一个多项式的系数。"
        "<bookmark mark='b'/>码字就是它在九个点上的值。<bookmark mark='c'/>进去三个数，出来九个。<bookmark mark='d'/>两个不同的二次多项式至多在两个"
        "点上相等，因为它们的差至多有两个根。所以任意两个码字在九个位置中至少有七个不同。<bookmark mark='e'/>一般地，距离是 n 减 k 加一：恰好是第4章"
        "的 Singleton 界。同样长度和码率的码，没有能做得更好的。<bookmark mark='f'/>运算其实是模一个素数，一千零九，但这里每个值都比它小，所以你可以"
        "把它想象成一条普通的抛物线。",
    "Now damage the codeword.":
        "现在损坏这个码字。<bookmark mark='a'/>九个值里有三个到达时是错的，接收方不知道是哪三个。<bookmark mark='b'/>Lloyd Welch 和 Elwyn Berlekamp "
        "的方法引入一个未知的错误定位多项式 E，它恰好在坏点上为零。于是在每个点上，不论好坏，y 乘 E 都等于 f 乘 E；记 Q 为 f 乘 E，这就是一个线性"
        "方程组。<bookmark mark='c'/>解出来再用 Q 除以 E，就得回消息五、三、二，而 E 的根恰好是三个被损坏的位置。红点弹回到曲线上。<bookmark "
        "mark='d'/>九个值、三个未知，至多三个错误能被修好：冗余的一半。<bookmark mark='e'/>擦除更容易：丢掉任意六个值，剩下的三个就用拉格朗日插值"
        "确定这条抛物线。<bookmark mark='f'/>实际的解码器用更快的 Berlekamp-Massey 算法，再加上 Chien 搜索和 Forney 公式；我们的二维码解码器就是"
        "这样做的。",
    "Erasures are easier still.":
        "擦除还要更容易。<bookmark mark='a'/>假设九个值丢了六个，接收方知道是哪六个。<bookmark mark='b'/>只有一条二次曲线经过剩下的三个点，拉格朗日"
        "公式直接把它写出来：<bookmark mark='c'/>对幸存的点求和，每个点乘上一个在它自己那里为一、在其他点为零的多项式。<bookmark mark='d'/>模一千"
        "零九计算，得回五、三、二：消息，以及随之而来的每个丢失的值。<bookmark mark='e'/>所以 Reed-Solomon 码能修复的擦除数等于校验符号数，是未知"
        "错误的两倍。第7章和第13章正用到这一点。",
    "Reed-Solomon codes are everywhere.":
        "Reed-Solomon 码无处不在。<bookmark mark='a'/>光盘用两个交织的 RS 码，能扛住几千位长的划痕。旅行者号以来的深空任务把它和一个卷积码，第10章"
        "的那种，配成一对。二维码用它，RAID-6 阵列和第13章的存储系统也用它，还有调制解调器、数字电视和固态硬盘。<bookmark mark='b'/>原因是它的"
        "符号是字节：一串坏位只会损坏少数几个符号。<bookmark mark='c'/>而且它善用擦除：坏掉的磁盘或读不出的斑点，位置是已知的，每个这样的擦除只花"
        "一个校验符号，而不是两个。",
    # ------------------------------------------------------------------ Qr
    "Chapter seven. Our QR code.": "第7章。我们的二维码。",
    "Masahiro Hara's team at Denso Wave designed the QR code in 1994 to track car parts.":
        "1994年，电装公司原昌宏的团队为了追踪汽车零件，设计了二维码。我们的是版本二：二十五乘二十五个模块。<bookmark mark='a'/>三个定位方块让摄像头"
        "找到这个码和它的朝向。<bookmark mark='b'/>定时条纹和一个对齐方块，即使在弯曲的表面上也能恢复网格。<bookmark mark='c'/>十五个格式位记录纠错"
        "等级和掩码，存两份，并由一个小码保护。<bookmark mark='d'/>其余都是数据：四十四个字节按两列宽的之字形排布，再与八种掩码之一做异或，掩码的"
        "选择是为了避免大色块和像定位图案的花样。<bookmark mark='e'/>我们选了 Q 级：二十二字节的消息和二十二个 Reed-Solomon 校验字节，足以修复任意"
        "十一个错误字节，或者二十二个位置已知的缺失字节。<bookmark mark='f'/>我们的编码器对每种掩码都与一个标准库生成完全相同的模块，所以你的手机能"
        "读它。",
    "Here is where each of the forty-four bytes lives.":
        "这是四十四个字节各自所在的地方。<bookmark mark='a'/>每个字节占一块八个模块、两列宽的区域，从右下角开始在码上来回蛇行。<bookmark mark='b'/>"
        "前二十二个装消息：一个模式标记、长度、文本和填充。<bookmark mark='c'/>后二十二个是 Reed-Solomon 校验，用的是实践中的生成多项式形式：消息"
        "多项式上移之后，除以一个以 alpha 的前二十二次幂为根的多项式，把余数附在后面。<bookmark mark='d'/>所以整个码字在这二十二个点上为零。解码器"
        "就在那里求值：没出错时二十二个伴随式全为零，否则它们编码了字节在哪里、怎样被损坏。",
    "Here is the decoder working on the small scratch, step by step.":
        "这是解码器处理那道小划痕的过程，一步一步。<bookmark mark='a'/>它把读到的四十四个字节当作多项式，在 alpha 的二十二个幂上求值。干净的码给出"
        "全零；这些不是。<bookmark mark='b'/>Berlekamp-Massey 算法把伴随式变成一个错误定位多项式，这里是八次：解码器现在认为有八个字节错了。"
        "<bookmark mark='c'/>Chien 搜索逐个位置尝试，找到八个根，<bookmark mark='d'/>恰好就是被涂料改变的那八个字节。<bookmark mark='e'/>Forney "
        "公式给出每处的错误值，异或把它去掉。四十四个字节全部复原。",
    "Now we damage it, three ways.":
        "现在用三种方式损坏它。<bookmark mark='a'/>一道小划痕把五十六个模块涂白。八个字节出错。这在码能自己找到的十一个错误之内，文本回来了。"
        "<bookmark mark='b'/>一块更长的污迹毁了十五个字节。作为未知错误，这太多了：解码器的定位多项式没有自洽的根，它宁可放弃也不乱猜。但扫描器能看到"
        "损坏在哪里。告诉解码器这块污迹碰到了哪十八个字节，它就把它们当作擦除处理，而二十二个擦除是允许的。文本回来了。<bookmark mark='c'/>涂掉整整"
        "一条，二十四个字节被碰到：两种方式下都超过了二十二个校验字节能覆盖的范围。什么都救不了，解码器如实报告失败。",
    # ------------------------------------------------------------------ Crc
    "Chapter eight. Cyclic codes and CRCs.": "第8章。循环码与 CRC。",
    "Most of the time a network only needs to notice damage, and ask again.":
        "大多数时候，网络只需要发现损坏，然后重新索取。<bookmark mark='a'/>循环冗余校验把比特看作一个多项式的系数，系数是零或一。<bookmark mark='b'/>"
        "在消息后面补几个零，除以一个固定的生成多项式，这里是 x 的三次方加 x 加一。在这个域上做长除法，就是异或，没有借位。<bookmark mark='c'/>把"
        "消息连同余数一起发出去。现在整个字能被生成多项式整除。<bookmark mark='d'/>接收方再除一次；余数不为零，就说明有东西变了。<bookmark "
        "mark='e'/>在硬件里，这是一个移位寄存器，在生成多项式为一的地方放上异或抽头，正是第5部分的线性反馈移位寄存器，每个时钟吃进一位。<bookmark "
        "mark='f'/>三十二位的版本守护着每个以太网帧、每个 zip 文件和每张 PNG 图片。我们的实现在每个测试串上都与 zlib 的一致。",
    "In hardware the division is a shift register.":
        "在硬件里，这个除法是一个移位寄存器。<bookmark mark='a'/>三个触发器保存当前的余数，异或门放在生成多项式为一的位置。从顶端移出的那一位被反馈"
        "回这些门。<bookmark mark='b'/>把消息一个时钟一位地送进去。<bookmark mark='c'/>最后一位之后，寄存器里就是余数，一零零，与纸上的长除法一样。"
        "<bookmark mark='d'/>真实的网络芯片把同样的代数展开，每个时钟处理几十甚至几百位。",
    "What does a CRC catch?":
        "CRC 能抓住什么？<bookmark mark='a'/>收到的字与发出的字之间差一个错误多项式，只有生成多项式整除它时，损坏才会被漏掉。<bookmark mark='b'/>突发"
        "错误，即一串长度不超过校验位数的错误，是 x 的某次幂乘以一个次数更低的多项式，生成多项式永远除不尽它。我们的八位 CRC 抓住了我们试过的每一个"
        "长度不超过八的突发，每种长度三万个。<bookmark mark='c'/>长度九的突发大约每一百二十八次漏掉一次，随机的乱码每两百五十六次漏掉一次，与代数"
        "的预言完全一致。<bookmark mark='d'/>以太网的三十二位 CRC 能抓住每一个不超过三十二位的突发，随机损坏每四十亿次才漏一次。<bookmark mark='e'/>"
        "但它不是密码学哈希：任何人都能改掉消息再把 CRC 修好。第29部分会造出能抵御这种事的哈希。",
    # ------------------------------------------------------------------ Shannon
    "Chapter nine. Shannon's theorem.": "第9章。Shannon 定理。",
    "In 1948, two years before Hamming's paper, Claude Shannon had already settled the big question.":
        "1948年，比 Hamming 的论文早两年，Claude Shannon 已经解决了那个大问题。<bookmark mark='a'/>每个信道都有一个容量。在它之下，任何码率都有这样"
        "的码：只要足够长，错误概率可以要多小有多小。<bookmark mark='b'/>在它之上，没有码能行。<bookmark mark='c'/>所以噪声并不会像第1章的重复码"
        "暗示的那样，把码率逼向零：它只拿走一个固定的比例。对二元对称信道，容量是一减 p 的熵。每十位翻转一位时，信道的百分之五十三仍能以任意少的错误"
        "承载数据。<bookmark mark='d'/>熵是第21部分的不确定性度量：信道在每一位上要花这么多位去对付噪声。<bookmark mark='e'/>对比一下重复码，它要"
        "降到信道的百分之四，才能达到六百万分之一的错误。",
    "We can watch the theorem start to work.":
        "我们可以看着这个定理开始起作用。<bookmark mark='a'/>取码率二分之一的随机线性码，用一张表完美地解码，表里记着每个伴随式最可能对应的错误。"
        "<bookmark mark='b'/>在翻转百分之五、容量零点七一的信道上，码越长，块错误越低：从长度八时的百分之十一，降到二十八时的百分之五。<bookmark "
        "mark='c'/>在翻转百分之十五时，容量低于二分之一，错误反而上升。<bookmark mark='d'/>正好在容量处，它几乎不动。这些码长很小，所以趋势很温和，"
        "但它的方向就是 Shannon 定理。<bookmark mark='e'/>而这里就是那个花了五十年的难点：解码一个随机码需要一张有二的 n 减 k 次方项的表。Shannon "
        "证明了好码存在。找到能快速解码的码，是后来的全部故事。",
    "Shannon's argument is a counting argument.":
        "Shannon 的论证是一个计数论证。<bookmark mark='a'/>发送 n 位；大约 p n 位会翻转，所以收到的字落在以发送字为中心、半径 p n 的球面附近。"
        "<bookmark mark='b'/>那个球面上大约有二的 n H(p) 次方个字，也就是人工智能，从零搭建第一部分里的典型错误。<bookmark mark='c'/>现在完全随机地"
        "选二的 n R 次方个码字，把收到的字解码为球面包含它的那个码字。<bookmark mark='d'/>另一个码字也落进这个球的概率大约是二的负 n 乘 C 减 R 次方。"
        "<bookmark mark='e'/>码率低于容量时，它就趋于零，这是对随机码取平均的结果，所以至少有一个码有这么好。<bookmark mark='f'/>逆定理用的是 Fano "
        "不等式：没有码能推过超出容量的信息。<bookmark mark='g'/>这个证明什么也没构造。达到容量的实用码，也就是接下来三章的码，又花了四十五年。",
    # ------------------------------------------------------------------ Viterbi
    "Chapter ten. Convolutional codes and the Viterbi algorithm.": "第10章。卷积码与 Viterbi 算法。",
    "Hamming and Reed-Solomon codes work on fixed blocks.":
        "汉明码和 Reed-Solomon 码处理固定的块。Peter Elias 1955年的卷积码处理的是流。<bookmark mark='a'/>每个输入位移进一个小寄存器，寄存器的两个"
        "奇偶位输出：码率二分之一。这条消息，一零一一零零，产生这些位对。<bookmark mark='b'/>寄存器有四个状态，把它们随时间画出来就是一张网格图："
        "每条可能的消息都是穿过它的一条路径。<bookmark mark='c'/>解码就是找出输出最接近收到内容的那条路径。Andrew Viterbi 在1967年看出，每一步只需"
        "为每个状态保留进入它的最好路径；在某个状态上输掉的路径，以后永远赢不了。<bookmark mark='d'/>这就是动态规划，第19部分的思想：每一位八次比较，"
        "不论消息多长。",
    "We sent twenty thousand random bits through the code at each noise level.":
        "在每个噪声水平上，我们让两万个随机位通过这个码。<bookmark mark='a'/>信道翻转百分之二的位时，Viterbi 解码器每一万个数据位只留下大约六个半"
        "错误，而不是两百个。在百分之零点五时，一个也没有。<bookmark mark='b'/>真实系统用六十四个状态的寄存器，并用软判决：接收方传递的是它对每一位"
        "有多确信，而不只是一个零或一。<bookmark mark='c'/>David Forney 在1966年展示了怎样组合码：内层一个卷积码，外层一个 Reed-Solomon 码，用来"
        "清理 Viterbi 解码器留下的短串错误。<bookmark mark='d'/>这一组合飞上了旅行者号，而卷积码支撑过 GSM、早期的 Wi-Fi 和 4G 的控制信道。",
    # ------------------------------------------------------------------ Ldpc
    "Chapter eleven. LDPC codes and belief propagation.": "第11章。LDPC 码与置信传播。",
    "In his 1960 thesis Robert Gallager proposed codes defined by sparse parity checks:":
        "Robert Gallager 在1960年的博士论文里提出了由稀疏奇偶校验定义的码：每一位只参与三个校验，每个校验只涉及六位。<bookmark mark='a'/>把比特画在"
        "一边，校验画在另一边，某位参与某个校验就连一条线，就像 Michael Tanner 在1981年做的那样。<bookmark mark='b'/>解码沿着这些边传递消息。每一位"
        "根据信道和其他校验，告诉它的校验自己是一的可能性有多大。<bookmark mark='c'/>每个校验根据它看到的其他位，回复这一位应该是什么。<bookmark "
        "mark='d'/>反复进行，直到每个校验都满足。这就是置信传播，人工智能，从零搭建第七部分里的消息传递；在稀疏图上，每一轮的时间与码长成正比。",
    "Here is the decoder at work on one block of our code.":
        "这是解码器处理我们的码的一个块的过程。<bookmark mark='a'/>在百分之七的噪声下，三百四十二位到达时被翻转了。一轮又一轮，置信越来越明确，错误"
        "渐渐消融：十四轮之后一个不剩。<bookmark mark='b'/>在百分之九时，四百三十二位被翻转，解码器卡在三百个左右，不论运行多久。<bookmark mark='c'/>"
        "但它知道：有些奇偶校验仍不满足，所以失败的块会被报告出来，而不是悄悄放行。",
    "We built a rate-one-half code of length four thousand eight hundred,":
        "我们造了一个码率二分之一、长度四千八百、图中没有短环的码，在每个噪声水平上解码一百个带噪的块。<bookmark mark='a'/>翻转率到百分之七又四分之一"
        "为止，每个块都完美恢复。然后，在一两个百分点之内，几乎全部失败：这就是瀑布。<bookmark mark='b'/>Tom Richardson 和 Rüdiger Urbanke 的密度演化"
        "预言了这类码在很长时悬崖的位置：百分之八点四。这个码率下的 Shannon 极限是十一。<bookmark mark='c'/>在擦除信道上，这个预言是一行递推，我们精确"
        "算出：零点四二九四，而容量是二分之一。<bookmark mark='d'/>让不同的位参与不同数目的校验，能填平剩下的大部分差距。2001年，Sae-Young Chung、"
        "Forney、Richardson 和 Urbanke 设计出了离 Shannon 极限只有千分之四分贝的这种码。",
    "The history is strange.":
        "这段历史很奇特。<bookmark mark='a'/>Gallager 的码需要的计算量超出了1960年代硬件的能力，于是被遗忘了三十年。<bookmark mark='b'/>1993年，"
        "Claude Berrou、Alain Glavieux 和 Punya Thitimajshima 提出了 Turbo 码：两个卷积码，其中一个吃进打乱过的数据副本，解码时来回交换置信。"
        "<bookmark mark='c'/>他们声称性能离 Shannon 极限只差零点几个分贝，许多听众以为是弄错了。并没有错，而那个解码器后来被证明就是置信传播。"
        "<bookmark mark='d'/>1996年，David MacKay 和 Radford Neal 重新发现了 Gallager 的码，发现它们同样出色。<bookmark mark='e'/>如今 LDPC 码支撑"
        "着 Wi-Fi、卫星电视、万兆以太网、5G 数据信道和固态硬盘里的闪存。<bookmark mark='f'/>Turbo 码承载过 3G 和 4G，以及2000年以来航天器的数据。",
    # ------------------------------------------------------------------ Polar
    "Chapter twelve. Polar codes.": "第12章。极化码。",
    "Here is Arıkan's construction for eight bits.":
        "这是 Arıkan 对八位的构造。<bookmark mark='a'/>同一个步骤做三级：把下面的线异或进上面的线，先跨两半，再跨四分之一，最后在相邻之间。<bookmark "
        "mark='b'/>解码按顺序处理各个输入，每个都用到前面的结果，所以每个输入看到一条属于自己的信道。<bookmark mark='c'/>从一个丢一半比特的擦除信道"
        "出发，这八条信道已经天差地别：第一条几乎总被擦除，最后一条几乎从不。<bookmark mark='d'/>所以把数据放在最好的四条信道上，其余四条冻结为零，"
        "收发双方都知道。",
    "In 2009 Erdal Arıkan found a code that provably reaches capacity,":
        "2009年，Erdal Arıkan 找到了一种可证明达到容量的码，解码器和排序一样便宜。<bookmark mark='a'/>从一个一半时间擦除每一位的信道出发。<bookmark "
        "mark='b'/>用它两次，发送 u 一异或 u 二，以及 u 二。先解码 u 一：它需要两个输出，所以它看到一条更差的信道，擦除概率是二 epsilon 减 epsilon "
        "平方。再在已知 u 一的情况下解码 u 二：它有两次机会，所以看到一条更好的信道，epsilon 平方。<bookmark mark='c'/>一遍又一遍地做。每翻一倍，"
        "信道就更加分化：这里是直到六十四条时全部信道的擦除概率。<bookmark mark='d'/>到一千零二十四条信道时，已有三分之一近乎完美，三分之一近乎无用，"
        "中间的还在不断缩小。<bookmark mark='e'/>总容量始终不变，所以变得完美的比例恰好趋于容量。把数据放在好的上面，把坏的冻结为零。",
    "Decoding follows the construction.":
        "解码沿着构造进行。<bookmark mark='a'/>一次解码一位，每位都用到已经做出的判决，时间是 N log N。<bookmark mark='b'/>我们在二元对称信道上发送"
        "码率二分之一的极化码。远低于容量时，较长的码出错更少；当信道逼近容量，两者都崩溃。<bookmark mark='c'/>在实际码长下，朴素的逐次消除并不是最好"
        "的解码器。Ido Tal 和 Alexander Vardy 保留一个候选路径的短列表，再用第8章的 CRC 挑出正确的那条。<bookmark mark='d'/>2016年，5G 的标准组织"
        "为控制信道选择了极化码，为数据选择了 LDPC 码：从 Arıkan 的论文到几十亿部手机，十年。",
    # ------------------------------------------------------------------ Storage
    "Chapter thirteen. Codes for storage.": "第13章。存储用的码。",
    "Storage is the erasure channel:":
        "存储就是擦除信道：坏掉的磁盘，大家都知道它坏了。<bookmark mark='a'/>RAID-5 加一块磁盘，逐字节存放其余所有磁盘的异或，所以任何一块坏掉都能"
        "重建。<bookmark mark='b'/>RAID-6 再加一块校验盘，是第5章那个域里的加权和，每块磁盘用 g 的不同次幂。<bookmark mark='c'/>如果两块磁盘坏掉，"
        "每个字节位置给出两个方程、两个未知数，而域让我们能解出它们。<bookmark mark='d'/>我们把两块丢失的磁盘精确地重建了。<bookmark mark='e'/>这是一个"
        "有两个校验符号的 Reed-Solomon 码，横跨各磁盘来读；Linux 按照 Peter Anvin 的方式这样实现它。",
    "At data-centre scale, machines fail every day.":
        "在数据中心的规模上，机器每天都在坏。<bookmark mark='a'/>简单的防御是每样东西存三份，磁盘数变成三倍。<bookmark mark='b'/>一个把每块数据分成十份、"
        "再加四个校验的 Reed-Solomon 码，能扛住任意四份丢失，只用一点四倍的空间。Facebook 的 f4 温存储和 Hadoop 的文件系统用的正是这个。<bookmark "
        "mark='c'/>代价在修复：重建丢失的一份，要通过网络读取另外十份。<bookmark mark='d'/>微软的 Azure 存储多加一点校验，每个六份的本地组一个，所以"
        "常见的单份修复只需读六份。<bookmark mark='e'/>在给定存储量下，修复时最少要读多少，自成了一个研究领域。",
    "One more storage and broadcast trick.":
        "再来一个存储和广播的技巧。<bookmark mark='a'/>Michael Luby 2002年的 LT 码，让每个输出块是随机一小撮源块的异或。<bookmark mark='b'/>发送方"
        "可以像喷泉一样永远产生输出，接收方只要收集到足够多，从任何来源、按任何顺序，到了哪些算哪些。<bookmark mark='c'/>解码靠剥离：只含一个未知源块"
        "的输出就揭示了它，把它代入各处，如此反复。<bookmark mark='d'/>用 Luby 的鲁棒孤波度分布，一百个源块我们需要多出大约百分之三十的块，一千个要"
        "百分之十八，一万个要百分之九。<bookmark mark='e'/>Amin Shokrollahi 的 Raptor 码加了一个预编码，把开销降到百分之几；它们承载着移动网络中的"
        "广播视频和多媒体。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fourteen. The frontier:": "第14章。前沿：容量与局部性。",
    "Some of the newest results are about the oldest codes.":
        "一些最新的结果，关于的是最老的码。<bookmark mark='a'/>Reed-Muller 码始于1954年，它对多元低次多项式求值。<bookmark mark='b'/>它们能达到 "
        "Shannon 容量吗？在擦除信道上，Shrinivas Kudekar 等人在2016年证明了能，只用到这些码的对称性。<bookmark mark='c'/>对每个二元对称信道，"
        "Emmanuel Abbe 和 Colin Sandon 在2023年证明了它，距这些码诞生将近七十年。<bookmark mark='d'/>另一个想法：错误多到无法唯一解码时，返回一个短的"
        "候选列表。<bookmark mark='e'/>Madhu Sudan 在1997年证明，Reed-Solomon 码可以列表解码，远远超过距离的一半。<bookmark mark='f'/>而 Venkatesan "
        "Guruswami 和 Atri Rudra 找到了折叠 Reed-Solomon 码，能纠正的错误比例逼近一减码率：这是可能的最好结果。",
    "Sometimes you need one bit of a huge encoded file, not all of it.":
        "有时你只需要一个巨大编码文件里的一位，而不是全部。<bookmark mark='a'/>Hadamard 码存储消息的每一种奇偶。要得到第 i 位，就在一个随机位置 a "
        "和把 a 的第 i 位翻转后的位置各读一次码字；两者的异或就是这一位。<bookmark mark='b'/>两次读取各自落在一个均匀随机的位置上，所以如果有 delta "
        "比例被损坏，答案正确的概率至少是一减二 delta。我们的测量值正好略高于这条线，而对十五对读取取多数几乎总是对的。<bookmark mark='c'/>这是一种"
        "局部可解码码，第27部分线性性测试的近亲。<bookmark mark='d'/>代价是长度：k 位要二的 k 次方个位置。只读两三次就能解码的码最短能有多短，是一个"
        "重大的未解问题，上下界之间差距巨大。",
    "Two linked breakthroughs came in 2021.":
        "2021年出现了两项相互关联的突破。<bookmark mark='a'/>局部可测试码让你只读几个随机符号，就能判断一个字是码字，还是离每个码字都很远。<bookmark "
        "mark='b'/>几十年来，没人知道这样的码能否同时具有常数码率和常数相对距离，也就是所谓的 c 立方码。<bookmark mark='c'/>Irit Dinur、Shai Evra、"
        "Ron Livne、Alexander Lubotzky 和 Shahar Mozes 造出了它们，Pavel Panteleev 和 Gleb Kalachev 也独立地造出了，用的是高维扩展图。<bookmark "
        "mark='d'/>Panteleev 和 Kalachev 的构造还给出了第一批好的量子 LDPC 码，回答了一个二十年的老问题。<bookmark mark='e'/>没有纠错，量子计算机"
        "根本无法工作，第53部分会讲到。<bookmark mark='f'/>而局部可测试码，正是第27部分的 PCP 定理的原料。",
    "Six open problems.":
        "六个未解问题。<bookmark mark='a'/>是否有长的二元码能胜过 Gilbert 和 Varshamov 的随机码。<bookmark mark='b'/>在那个界和线性规划界之间，真相"
        "在哪里。<bookmark mark='c'/>是否有任何显式构造能哪怕追平随机码。<bookmark mark='d'/>只读三个符号的局部可解码码最短能有多短。<bookmark "
        "mark='e'/>快速解码器在短码长下能多接近容量，这对控制消息和物联网很重要。<bookmark mark='f'/>以及 Reed-Muller 码能否用高效的解码器达到容量，"
        "而不只是原则上可以。<bookmark mark='g'/>这一部分的研究题取第五个问题的一个小而可计算的情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭建了什么。有噪信道和重复码。汉明距离，以及伴随式能说出坏位的汉明码。任何码能好到什么程度的界，以及被逐一列举的完美 Golay 码。"
        "字节的域，用 Berlekamp 和 Welch 的方法解码的 Reed-Solomon 码，以及我们自己的二维码，被三种方式划伤。用第5部分的移位寄存器搭成的 CRC。在随机码"
        "上看到的 Shannon 定理。以及达到他的极限的那些码：Viterbi 的网格图、LDPC 的瀑布和极化。",
    "Where this comes back.":
        "这些内容在哪里再次出现。第29部分搭建 AES，它的 S 盒就是字节域中的求逆。第30部分的秘密共享，用的正是一个 Reed-Solomon 码来拆分密钥。第34部分"
        "把 RAID 和校验和放进文件系统，第36部分给每个以太网帧加上 CRC，第45部分计算纠删编码的云存储能存活多久。而第53部分需要编码，量子计算机才能"
        "工作。",
    "In practice.":
        "实践中。处处检测错误，用 CRC 或校验和，失败就重试。在重试不可能或太慢的地方纠正错误：内存、深空、广播。优先利用擦除：如果你知道缺了什么，"
        "码能修复两倍的量。修复必须快时选复制，存储成本为主时选纠删码。并且使用经过测试的库：这些运算很容易出微妙的错，这也是为什么我们拿自己的实现"
        "与 zlib 和一个二维码库对照。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在本部分的笔记里。可以在任何一题上暂停。第五题是动手题：用本部分的函数做一个更小的二维码，再用你的手机读出来。最后一题标了"
        "星号，是研究题：它的答案还不知道，笔记里写了从哪里入手。",
    "Next time: secrets.":
        "下一次：秘密。这一部分的码对抗的是随机噪声。第29部分面对的是一个对手。从频率分析和恩尼格玛机，到 Shannon 的完美保密，再到从零搭建的 AES，"
        "建在同一个字节域上，配上让它能安全使用的工作模式、哈希和消息认证码。第29部分，秘密。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分所依据的书籍和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
