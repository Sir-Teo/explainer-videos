"""Chinese narration for cs30: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第30部分：公钥"

CHAPTERS = {
    "Hook": "两个陌生人，一个秘密",
    "Puzzles": "1. 密钥分配与 Merkle 谜题",
    "Toolkit": "2. 工具箱：模运算",
    "Groups": "3. 群与离散对数",
    "DiffieHellman": "4. Diffie–Hellman",
    "Rsa": "5. RSA",
    "Oracle": "6. Bleichenbacher 的预言机",
    "Factoring": "7. 因数分解",
    "DiscreteLogs": "8. 离散对数",
    "Curves": "9. 椭圆曲线",
    "Signatures": "10. 签名",
    "Pki": "11. 证书与信任",
    "Tls": "12. TLS 1.3",
    "Shor": "13. Shor 的威胁",
    "Lattices": "14. 格",
    "Beyond": "15. 零知识、秘密共享与在秘密上计算",
    "Frontier": "16. 前沿：后量子，以及更远",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Alice and Bob have never met.":
        "Alice 和 Bob 从未见过面。他们想要一个只有彼此知道的秘密，而他们说的每一句话都被 Eve 听着。<bookmark mark='a'/>他们公开商定两个数："
        "一个素数，二十三，还有五。<bookmark mark='b'/>Alice 挑一个秘密的数，六；Bob 挑十五。谁也不告诉别人。<bookmark mark='c'/>Alice 发出五的"
        "六次方模二十三：八。Bob 发出五的十五次方：十九。<bookmark mark='d'/>现在 Alice 把 Bob 的十九升到她的六次方，Bob 把 Alice 的八升到他的"
        "十五次方。两人都得到二。<bookmark mark='e'/>Eve 听到了每一个数，二十三、五、八和十九，而秘密的二从未被说出口。<bookmark mark='f'/>两人"
        "都算出了五的六乘十五次方，只是走的路不同。Whitfield Diffie 和 Martin Hellman 在1976年发表了这个方法，它改变了密码学能做的事。",
    "With small numbers Eve could simply try every exponent.":
        "数很小时，Eve 可以把每个指数都试一遍。<bookmark mark='a'/>实际中，素数有两千零四十八位，六百一十七位十进制数字，而这次交换即使在 Python "
        "里也只要百分之几秒。<bookmark mark='b'/>要得到秘密，Eve 必须由幂求出指数：离散对数，在这种规模下没人知道怎么算。<bookmark mark='c'/>你的"
        "浏览器建立的每一个 HTTPS 连接，都以这样一次交换开始，通常是在椭圆曲线上。<bookmark mark='d'/>还要加上一个签名，因为 Alice 还必须知道，"
        "和她商定秘密的人是 Bob，而不是夹在中间的某个人。",
    "Part 30 of Computer Science, Built: Public Keys.":
        "计算机科学，从零搭建，第30部分：公钥。<bookmark mark='a'/>这一部分包括：为什么分发密钥曾是难题，以及解决它的数论；Diffie-Hellman，以及"
        "从零搭建的 RSA，外加对它填充的一次攻击；因数分解和离散对数如何被攻击，正是这决定了密钥长度；椭圆曲线、它们的签名，以及一个重复的数怎样"
        "毁掉了一台游戏机的安全；证书，以及我们两台机器之间一次完整的 TLS 握手；然后是量子威胁、应对它的格，以及在秘密上做计算的密码学。",
    # ------------------------------------------------------------------ Puzzles
    "Chapter one. Key distribution, and Merkle's puzzles.": "第1章。密钥分配与 Merkle 谜题。",
    "Everything in Part 29 assumed":
        "第29部分的一切都假定双方已经共享一把密钥。它从哪里来？<bookmark mark='a'/>如果每两个人都需要自己的密钥，n 个人就需要 n 乘 n 减一再除以二"
        "把密钥。八个人需要二十八把；一百万人需要五千亿把。<bookmark mark='b'/>历史上大部分时间，每把密钥都要在发送任何消息之前，由信使亲手送达。"
        "各国政府维持着成队的信使专门递送密钥材料。<bookmark mark='c'/>一个与每个人共享密钥的可信中心能减少数量，第55部分的 Kerberos 就是这样工作"
        "的；但这个中心什么都能读。<bookmark mark='d'/>在互联网上，陌生人每天相遇数十亿次，而且马上就需要密钥。",
    "In 1974 Ralph Merkle,":
        "1974年，伯克利的本科生 Ralph Merkle 在一份课程项目里提出了一条出路，而他的教授没看懂。<bookmark mark='a'/>Alice 制作许多谜题。每个谜题装着"
        "一个编号和一把密钥，用一把故意很弱、要花些力气才能找到的密钥锁住。<bookmark mark='b'/>Bob 随机挑一个谜题，解开它，公开宣布它的编号。"
        "<bookmark mark='c'/>Alice 查出这个编号对应哪把密钥。现在他们共享了它。<bookmark mark='d'/>Eve 听到了编号，却不知道它来自哪个谜题，只好一个"
        "个解谜题直到找到它：大约要解一半。<bookmark mark='e'/>我们跑了一遍。Bob 的工作量与 n 成正比；Eve 的工作量按 n 的平方增长。<bookmark "
        "mark='f'/>这个差距只是平方级的：一个下定决心、有台大计算机的 Eve 能追上来。<bookmark mark='g'/>而且，只用类似哈希的函数，它无法再改进，"
        "Boaz Barak 和 Mohammad Mahmoody 在2009年证明了这一点。真正的公钥系统需要数学结构。",
    "The structure was found twice.":
        "这种结构被发现了两次。<bookmark mark='a'/>在英国信号情报机构 GCHQ，James Ellis 在1970年论证了不需要共享秘密的加密是可能的。年轻的数学家 "
        "Clifford Cocks 在1973年找到了办法：本质上就是 RSA。Malcolm Williamson 在1974年找到了 Diffie-Hellman 交换。这一切都被保密。<bookmark "
        "mark='b'/>在公开世界里，Diffie 和 Hellman 于1976年发表，MIT 的 Rivest、Shamir 和 Adleman 于1977年找到了 RSA。GCHQ 直到1997年才讲出自己"
        "的故事。<bookmark mark='c'/>两者的思想相同：一把可以公之于众的密钥，锁住一个只有你能打开的秘密。接下来两章搭建它所需的数学。",
    # ------------------------------------------------------------------ Toolkit
    "Chapter two. The toolkit: modular arithmetic.": "第2章。工具箱：模运算。",
    "Public-key cryptography computes with numbers":
        "公钥密码学用几百位长的数计算，但总是在一个钟面上。<bookmark mark='a'/>在十二小时的钟面上，九加七等于四：除以十二后只保留余数。模 n 的"
        "算术从不让数超过 n。<bookmark mark='b'/>加、减、乘照常进行。问题在除法：要除以 a，你需要一个逆，一个与 a 相乘得一的数。<bookmark "
        "mark='c'/>逆存在，当且仅当 a 与 n 没有公因子。五乘五是二十五，在这个钟面上是一，所以五是它自己的逆；四没有逆。<bookmark mark='d'/>"
        "Gauss 在1801年写下了这套理论。而要快速求逆，需要一个比它早两千年的算法。",
    "Euclid's algorithm, from about 300 BC,":
        "Euclid 的算法，约公元前300年，求最大公约数。<bookmark mark='a'/>用四十六除两百四十，保留余数十；用十除四十六，依此类推，直到余数为零。"
        "最后一个非零余数，二，就是最大公约数。<bookmark mark='b'/>扩展的做法：一路带着两个系数，使每个余数都写成两百四十的某个倍数加上四十六的某个"
        "倍数。<bookmark mark='c'/>最后，二等于两百四十乘负九，加上四十六乘四十七。这就是 Bézout 等式。<bookmark mark='d'/>当最大公约数是一时，"
        "同一个等式就交给你一个逆。十七模三千一百二十的逆是两千七百五十三，我们会在 RSA 密钥里再见到这个数。<bookmark mark='e'/>步数只随位数增长，"
        "所以即使对六百位的数，这也是瞬间完成的。",
    "The other tool is raising to a huge power.":
        "另一个工具是求一个很大的幂。<bookmark mark='a'/>要算三的两百一十八次方模一千，不要乘两百一十七次。把指数写成二进制。<bookmark mark='b'/>"
        "然后从高位读它的各位。每读一位，把手上的数平方；遇到一，再乘以三。八次平方、五次乘法，答案是四百八十九。<bookmark mark='c'/>一个两千位的"
        "指数大约需要四千次乘法，而不是二的两千次方次。<bookmark mark='d'/>第16部分数过它的步数，第20部分的素性检验靠它运行，它还会在椭圆曲线上"
        "再次出现。<bookmark mark='e'/>有了 Euclid 和平方，六百位数的基本运算只要几毫秒。让它们能用于保密的，是结构，那是下一章的主题。",
    # ------------------------------------------------------------------ Groups
    "Chapter three. Groups, and the discrete logarithm.": "第3章。群与离散对数。",
    "Take the nonzero numbers modulo a prime,":
        "取模一个素数，二十三，的非零数，配上乘法。任意两个相乘得到另一个，每一个都有逆：这就是一个群。<bookmark mark='a'/>从一开始，不断乘以五："
        "五、二、十、四、二十，依此类推，在圆周上跳来跳去。<bookmark mark='b'/>二十二步之后，每个数都被访问过，我们回到了一。五生成了整个群。"
        "<bookmark mark='c'/>Gauss 证明了，对每个素数，这个群都像这样是循环的：有某个数生成它的全部。<bookmark mark='d'/>正向，从 x 到五的 x 次方，"
        "靠反复平方，即使对巨大的数也很容易。反向，从五的 x 次方回到 x，就是离散对数。那些跳跃正是它困难的原因。",
    "Not every number generates the group.":
        "并不是每个数都能生成这个群。<bookmark mark='a'/>一个数的阶，是它回到一所需的步数。<bookmark mark='b'/>这是全部二十二个数，按阶着色。每个阶都"
        "是一、二、十一或二十二：恰好是二十二的因数。<bookmark mark='c'/>这就是拉格朗日定理：在任何有限群中，每个元素的阶都整除群的大小。<bookmark "
        "mark='d'/>它立刻证明了费马小定理。这个群有 p 减一个元素，所以每个 a 的 p 减一次方都是一。<bookmark mark='e'/>对与 n 互素的数，共有 phi(n) "
        "个，同样的论证给出欧拉定理。第五章把 RSA 建在它上面。",
    "Here is what makes the discrete logarithm hard,":
        "这就是离散对数困难的原因，以素数一千零一十九为例。<bookmark mark='a'/>对每个指数画出二的 x 次方模这个素数。起初幂平稳增长，二、四、八；然后"
        "取模把它们绕回来，点像噪声一样散开。<bookmark mark='b'/>反向意味着给定一个高度，找出产生它的指数。<bookmark mark='c'/>没有趋势可循。最好的"
        "通用方法，第八章会搭建，大约需要 p 的平方根步；对两千位的素数，更好的方法是存在的，但仍然太慢。<bookmark mark='d'/>所以从 x 到 g 的 x 次方"
        "的映射，就人们所知，是一个单向函数：正向容易，反向难。第29部分说明了单向函数能给出全部对称密码学。这个函数还有额外的结构，而这结构给出了"
        "公钥。",
    # ------------------------------------------------------------------ DH
    "Chapter four. Diffie-Hellman.": "第4章。Diffie-Hellman。",
    "The idea is easiest with paint.":
        "用颜料来讲最容易。<bookmark mark='a'/>Alice 和 Bob 公开商定一种颜色，黄色。各自再秘密挑一种自己的颜色。<bookmark mark='b'/>各自把秘密颜色"
        "混进公开颜色里，把混合色发出去。混合容易；把混合色再分离成原来的颜色则不容易。<bookmark mark='c'/>Alice 把她的秘密颜色加进 Bob 的混合色；"
        "Bob 把他的加进 Alice 的。两人最后都得到黄、红、蓝三者混在一起：同一种颜色。<bookmark mark='d'/>Eve 看到了黄色和两种混合色，但要得到最终的"
        "颜色，她必须把其中一种混合色分离开。",
    "Now the mathematics.":
        "现在看数学。<bookmark mark='a'/>公开颜色是模一个素数的群的生成元 g。秘密是指数。混合就是求幂：Alice 发出 g 的 a 次方，Bob 发出 g 的 b 次方。"
        "<bookmark mark='b'/>Alice 把 Bob 的数升到 a 次方，Bob 把 Alice 的升到 b 次方，指数相乘，所以两人都得到 g 的 a b 次方。分离就是离散对数。"
        "<bookmark mark='c'/>安全假设叫计算 Diffie-Hellman：由 g、g 的 a 次方和 g 的 b 次方，没人能算出 g 的 a b 次方。<bookmark mark='d'/>证明通常"
        "需要更强的假设，判定 Diffie-Hellman：共享值甚至无法与群中的随机元素区分开。它在模 p 的整个群里不成立，所以实际系统在素数阶的子群里工作。"
        "<bookmark mark='e'/>然后把共享值哈希成密钥。同样的交换放在椭圆曲线上，第九章，更小也更快。",
    "Diffie-Hellman defeats a listener.":
        "Diffie-Hellman 挫败的是窃听者，挫败不了能篡改消息的人。<bookmark mark='a'/>Mallory 坐在 Alice 和 Bob 之间，截下 g 的 a 次方和 g 的 b 次方，"
        "用她自己的秘密分别和两边各做一次交换。<bookmark mark='b'/>在我们的运行中，Alice 最终与 Mallory 共享十五，Bob 与 Mallory 共享八。各自都以为"
        "密钥是和对方共享的。<bookmark mark='c'/>现在 Mallory 解密 Alice 发出的一切，阅读或改动，再为 Bob 重新加密。<bookmark mark='d'/>这次交换防住"
        "了窃听，防不住冒充。<bookmark mark='e'/>修复方法是 Bob 用一把 Alice 能验证的密钥给他那一半签名，这需要签名，以及某种信任公钥的方式：第十章"
        "和第十一章。",
    # ------------------------------------------------------------------ RSA
    "Chapter five. RSA.": "第5章。RSA。",
    "Diffie and Hellman described public-key encryption":
        "Diffie 和 Hellman 描述了公钥加密，却没有造出来。第二年，Ron Rivest、Adi Shamir 和 Leonard Adleman 造出来了。<bookmark mark='a'/>挑两个"
        "素数，这里是六十一和五十三，把它们相乘：三千二百三十三。这个乘积 n 是公开的。<bookmark mark='b'/>数一数小于 n 且与它没有公因子的数有多少："
        "phi(n)，只有知道这两个素数才容易算：三千一百二十。<bookmark mark='c'/>选一个公开指数，十七，用 Euclid 算出它模 phi 的逆：两千七百五十三，"
        "即私有指数。<bookmark mark='d'/>要加密消息六十五，把它升到十七次方模 n：两千七百九十。要解密，把它升到私有指数次方，六十五就回来了。"
        "<bookmark mark='e'/>n 和 e 这一对可以公开。解密需要 d，而算出 d 需要那两个素数。",
    "Why does this work?":
        "为什么这行得通？<bookmark mark='a'/>因为 d 是 e 模 phi(n) 的逆，e 乘 d 比 phi 的某个倍数大一。<bookmark mark='b'/>所以把密文升到 d 次方得到"
        " m 的 e d 次方，也就是 m 乘以 m 的 phi 次方的若干次幂。由第三章的欧拉定理，m 的 phi 次方是一，剩下的就是 m。<bookmark mark='c'/>欧拉定理"
        "要求 m 与 n 没有公因子；对极为罕见的那些有公因子的消息，分别模 p 和模 q 验证这个等式，再用中国剩余定理合起来。<bookmark mark='d'/>安全假设"
        "是：只知道 n 和 e，没人能在模 n 下开 e 次方根。<bookmark mark='e'/>分解 n 就能攻破它。是否有比分解更容易的攻破方法，至今未知。",
    "Real keys use primes of a thousand bits or more.":
        "真实的密钥用一千位或更大的素数。<bookmark mark='a'/>要找一个，就挑一个合适大小的随机奇数，用第20部分的 Miller-Rabin 检验测试它，一直试到"
        "有一个通过为止。素数很多：由素数定理，在这个规模下大约每三百五十五个奇数里有一个素数，我们的三次搜索分别用了三百五十四、九十九和三百六十次"
        "尝试。<bookmark mark='b'/>一把完整的两千位密钥用了不到一秒。<bookmark mark='c'/>直接解密要二十九毫秒。用一半大小的数分别模 p 和模 q 解密，"
        "再用中国剩余定理合起来，只要九毫秒：快了三倍多，这就是每个实现都把素数留在私钥里的原因。",
    "Raising to a power is not yet encryption.":
        "求幂还不等于加密。<bookmark mark='a'/>教科书式 RSA 是确定性的，按第29部分的定义它并不安全：攻击者可以加密自己的猜测再比较。<bookmark "
        "mark='b'/>它还是可延展的。把密文乘以二的 e 次方，里面的消息就翻倍。<bookmark mark='c'/>我们把「付给 Bob 一百美元」编码成一个数，把它的密文"
        "乘一下，解密出来恰好是这个数的两倍。<bookmark mark='d'/>标准的修复是最优非对称加密填充 OAEP，来自 Mihir Bellare 和 Phillip Rogaway：加密前"
        "先把消息与新鲜的随机数经过两个基于哈希的掩码混合。<bookmark mark='e'/>现在同一条消息的两次加密不同了，攻击者可以利用的结构也消失了。"
        "<bookmark mark='f'/>同一个陷门也能签名：把消息的哈希升到私有指数次方，任何人都能用公开指数检查它。先哈希很重要，因为原始签名也会相乘。"
        "<bookmark mark='g'/>RSA 的算术五十年来屹立不倒。包在它外面的填充却没有。",
    # ------------------------------------------------------------------ Oracle
    "Chapter six. Bleichenbacher's oracle.": "第6章。Bleichenbacher 的预言机。",
    "For twenty years, TLS used RSA to send the session key,":
        "二十年来，TLS 一直用 RSA 发送会话密钥，配一种叫 PKCS 一 一点五版的填充格式。<bookmark mark='a'/>填充后的消息以字节零和二开头，接着是随机的"
        "非零字节、一个零，然后是消息。<bookmark mark='b'/>服务器解密密文时检查这个格式，早期的服务器在格式不对时会发出不同的错误。这就是一个预言机，"
        "就像第29部分的填充预言机。<bookmark mark='c'/>把它和可延展性结合起来。把密文乘以 s 的 e 次方，服务器检查的就是 m 乘 s。<bookmark mark='d'/>"
        "每当它说填充有效，攻击者就知道 m 乘 s 模 n 落在一个窄窗口里。<bookmark mark='e'/>每个回答都缩小可能消息的集合。Daniel Bleichenbacher 在1998年"
        "说明了怎样选取 s，使这个集合缩到只剩一个数。",
    "We built a server that answers only valid or invalid,":
        "我们搭了一个只回答有效或无效的服务器，跑了这个攻击。<bookmark mark='a'/>曲线表示关于消息还剩多少位的不确定性。对两百五十六位的密钥，攻击者"
        "寻找第一个有效 s 时它下降得很慢，之后陡然下降，大约每次查询一位。<bookmark mark='b'/>一共三万三千次查询；对三百八十四位的密钥，十二万九千"
        "次。<bookmark mark='c'/>消息就出来了，不需要密钥，也不需要分解。<bookmark mark='d'/>对真实的密钥长度，这个攻击大约需要一百万次查询，它的名字"
        "由此而来。<bookmark mark='e'/>服务器一直在通过错误信息和时间泄露这一位：2017年的 ROBOT 研究发现，它对一些大型网站依然有效。<bookmark "
        "mark='f'/>TLS 1.3 干脆取消了 RSA 密钥传输，只用 Diffie-Hellman。",
    # ------------------------------------------------------------------ Factoring
    "Chapter seven. Factoring.": "第7章。因数分解。",
    "The simplest fast factoring method is John Pollard's,":
        "最简单的快速分解方法是 John Pollard 在1975年提出的。<bookmark mark='a'/>挑一个起始数并迭代：平方、加一、模 n。这些值看起来是随机的。"
        "<bookmark mark='b'/>现在想象把它们同时模我们要找的因子 p，一千零九。只有 p 种可能的值，所以按生日悖论，大约 p 的平方根步之后它们就开始重复。"
        "<bookmark mark='c'/>这里，经过七个值的尾巴之后，序列落进一个长度为十四的环。画出来，形状像希腊字母 rho。<bookmark mark='d'/>我们看不到模 p "
        "的值，但也不需要。模 p 重复意味着 p 整除两个值之差，所以这个差与 n 的最大公约数就是 p。<bookmark mark='e'/>果然：一千零九。<bookmark "
        "mark='f'/>第17部分的龟兔赛跑技巧不用存储整个序列就能发现这个环。",
    "How does rho scale?":
        "rho 的规模如何增长？我们分解了两个等长素数的乘积，从十位到三十四位。<bookmark mark='a'/>rho 大约需要较小素数的平方根步，也就是 n 的四次方根，"
        "所以它的时间随位数指数增长：在这张对数图上是一条直线。<bookmark mark='b'/>二次筛法，我们接下来就搭它，增长得比任何指数都慢：亚指数。"
        "<bookmark mark='c'/>在我们的 Python 里，在这些小规模上，两者很接近：三十四位时，rho 用了四十三秒，筛法八十七秒。<bookmark mark='d'/>但筛法的"
        "曲线是弯的。大约过了四十位它就胜出，之后差距无限扩大。对 RSA 大小的数，只有筛法要紧。",
    "The sieve rests on an old idea of Fermat's,":
        "筛法建立在 Fermat 的一个老想法上，由 Carl Pomerance 在1981年磨砺成形。<bookmark mark='a'/>如果你能找到 x 和 y，它们的平方模 n 相等，但它们既"
        "不相等也不互为相反数，那么 n 整除 x 减 y 乘以 x 加 y，一个最大公约数就能把它分开。<bookmark mark='b'/>为了造出这样的平方，取刚好大于 n 的平方"
        "根的 x，使 x 的平方减 n 比较小，只保留那些使它光滑的 x：即它是小素数的乘积。<bookmark mark='c'/>这是我们运行中的一个：一个十二位的值，完全分解"
        "成一千三百以下的素数。<bookmark mark='d'/>找到它们靠的是筛，就像 Eratosthenes 的筛：对每个小素数，标出它整除的位置，而不是逐个检验每个值。"
        "<bookmark mark='e'/>把每个光滑值的指数模二写成一个向量。一组和为零的向量，可以用二元域上的高斯消元找到，它们相乘在两边都是完全平方。<bookmark "
        "mark='f'/>对我们的二十位数：一百一十六个小素数，一百二十七个关系，其中四十六个的组合，然后就是因子。",
    "The fastest known method is the number field sieve,":
        "已知最快的方法是数域筛法，来自九十年代初，它把同样的想法带进代数数域。<bookmark mark='a'/>它的运行时间大致随位数的立方根的指数增长。<bookmark "
        "mark='b'/>公开的纪录记录着它：1991年一百位；1999年 RSA-155，一把五百一十二位的密钥；2020年 RSA-250，八百二十九位，代价约两千七百核年。"
        "<bookmark mark='c'/>一把两千零四十八位、六百一十七位数字的密钥，远在这条线之外，被评为约一百一十二位的安全性。<bookmark mark='d'/>但曲线是"
        "亚指数的，所以要更高的安全性，密钥长度必须迅速增长：一百二十八位安全需要三千零七十二位，两百五十六位安全需要一万五千位。椭圆曲线，第九章，"
        "要好得多。",
    # ------------------------------------------------------------------ Dlog
    "Chapter eight. Discrete logarithms.": "第8章。离散对数。",
    "Chapter three left a question:":
        "第三章留下一个问题：g 的 x 次方能多快被还原？试遍每个 x 要 p 步。Daniel Shanks 在1971年找到了平方根的方法。<bookmark mark='a'/>把未知的 x "
        "写成 i 乘 m 加 j，m 约为 p 的平方根。先走小步：对每个小于 m 的 j 存下 g 的 j 次方。<bookmark mark='b'/>再从目标出发走大步：h，h 除以 g 的 m "
        "次方，再除以 g 的 2m 次方，依此类推，每一个都到表里查。<bookmark mark='c'/>一旦匹配，x 就读出来了。大约两倍 p 的平方根次运算，以及平方根大小"
        "的内存。<bookmark mark='d'/>我们的运行：p 每多四位，时间大约乘以五，接近平方根预言的四。Pollard 的 rho 几乎不用内存就能做到同样的事。",
    "The square root is of the group's order,":
        "这个平方根是对群的阶而言的，而阶的结构很重要。<bookmark mark='a'/>Stephen Pohlig 和 Martin Hellman 在1978年证明，离散对数可以拆成 p 减一的每个"
        "素因子各一个更小的对数，再用中国剩余定理粘回去。<bookmark mark='b'/>这是一个八十四位的素数，它的 p 减一是一串小素数的乘积。<bookmark "
        "mark='c'/>最大的是一百零九，所以每一块都很小，整个对数不到一毫秒。<bookmark mark='d'/>安全素数是一个素数的两倍加一。那时 p 减一有一个巨大的"
        "素因子，没有什么能胜过完整的平方根。<bookmark mark='e'/>所以 Diffie-Hellman 的群用安全素数构造，或者在大素数阶的子群里工作。",
    "For the numbers modulo p there is something better than square roots,":
        "对模 p 的数，有比平方根更好的方法，因为数可以分解。<bookmark mark='a'/>如果 g 的某个幂恰好分解成小素数，它的指数就是这些素数对数的线性组合。"
        "<bookmark mark='b'/>收集足够多这样的光滑幂，解出线性方程组，就知道了每个小素数的对数。<bookmark mark='c'/>然后把目标乘以 g 的随机幂，直到乘积"
        "光滑，它的对数就出来了。我们的方法对一个三十位的素数只要十分之一秒。<bookmark mark='d'/>指数演算是亚指数的，和筛法一样，这就是整数上的 "
        "Diffie-Hellman 需要两千位素数的原因。<bookmark mark='e'/>更糟的是，代价高昂的第一阶段只依赖于素数，与具体的交换无关。<bookmark mark='f'/>2015年，"
        "Logjam 的研究者表明，仍接受旧的五百一十二位出口级群的服务器，在一次预计算之后几分钟就能被攻破；而少数几个被广泛共享的一千位素数，在一个国家"
        "机构的能力范围之内。<bookmark mark='g'/>椭圆曲线上的点无法分解成小块。在那里，人们只知道通用的平方根攻击。",
    # ------------------------------------------------------------------ Curves
    "Chapter nine. Elliptic curves.": "第9章。椭圆曲线。",
    "An elliptic curve is the set of points":
        "椭圆曲线是 y 的平方等于 x 的一个三次式的点的集合。这是 y 的平方等于 x 的立方减 x 加一。了不起的是，它的点可以相加。<bookmark mark='a'/>取两个"
        "点 P 和 Q。过它们的直线恰好再与曲线交于一点 R：三次方程有三个根，我们已知两个。<bookmark mark='b'/>把 R 关于 x 轴反射。这个点被定义为 P 加 Q。"
        "<bookmark mark='c'/>用这些整数点：负一、一 加上 零、一，等于 一、负一。<bookmark mark='d'/>再加上一个无穷远点作为零，竖直线在那里相交，以反射"
        "作为取负，这些点就构成一个群。<bookmark mark='e'/>结合律，即先加 P 和 Q 再加 R，与先加 Q 和 R 结果相同，是成立的，但证明要花真功夫。它是这条"
        "曲线最深刻的性质，我们只在数值上验证它。",
    "Adding a point to itself uses the tangent line.":
        "一个点加它自己要用切线。<bookmark mark='a'/>在 P，负一、一，曲线的斜率是一。<bookmark mark='b'/>切线在三、五处再次与曲线相交。反射之后，两倍 P "
        "是三、负五。<bookmark mark='c'/>用坐标表示，斜率、新的 x 和新的 y 来自几行代数。<bookmark mark='d'/>它们只用加、减、乘、除。所以同样的公式在任何"
        "域上都有意义，包括模一个素数的整数，在那里曲线不再是曲线，而变成一片散点。",
    "Over the integers modulo ninety-seven,":
        "在模九十七的整数上，曲线 y 的平方等于 x 的立方加二 x 加三变成了这样。<bookmark mark='a'/>九十九个点，加上无穷远点：一个一百阶的群。<bookmark "
        "mark='b'/>关于中线的对称就是反射，y 变成负 y。<bookmark mark='c'/>取一个点 G，不断加它：G、两倍 G、三倍 G。这些倍数在网格上毫无规律地跳来跳去，"
        "五十个之后才回到零。<bookmark mark='d'/>给定一个倍数 Q 等于 k 乘 G，求 k 就是椭圆曲线离散对数。<bookmark mark='e'/>计算 k 乘 G 很容易：倍加法，"
        "就是第二章的平方乘换了一身衣服。在标准曲线 P-256 上，用两百五十六位的数，Python 里要二十毫秒。",
    "Why use curves at all?":
        "为什么要用曲线？<bookmark mark='a'/>因为它们的密钥很小。同样的安全性，RSA 需要三千位的模数，曲线只需要两百五十六位；安全级别越高，差距越大。"
        "<bookmark mark='b'/>原因是上一章的指数演算：好曲线上的点无法拆成小因子，所以已知的攻击只有通用的平方根。<bookmark mark='c'/>Victor Miller 和 "
        "Neal Koblitz 在1985年各自独立地提出了曲线密码学。NIST 标准化了 P-256，2006年 Daniel Bernstein 设计了 Curve25519，既快又不容易实现错。"
        "<bookmark mark='d'/>它的 X25519 函数用 Montgomery 阶梯，不论密钥的位是什么，执行的操作都一样。<bookmark mark='e'/>我们的实现与 RFC 的测试向量"
        "一致，两方也商定出了同一个秘密。<bookmark mark='f'/>今天几乎每一个 TLS 连接都正是从这个计算开始的。",
    # ------------------------------------------------------------------ Signatures
    "Chapter ten. Signatures.": "第10章。签名。",
    "Encryption hides; a signature proves who wrote something.":
        "加密负责隐藏；签名证明是谁写的。椭圆曲线数字签名算法 ECDSA，签着网络上大部分证书和大部分比特币交易。<bookmark mark='a'/>签名时，挑一个新的"
        "随机数 k，取 k 乘 G 的 x 坐标作为 r，再把 k、消息的哈希和私钥组合成 s。<bookmark mark='b'/>验证时，任何持有公钥的人由 s 算出两个乘数，检查 G 和 "
        "Q 的一个组合是否落回 r。<bookmark mark='c'/>它成立，是因为那个组合恰好就是 k 乘 G。<bookmark mark='d'/>只有持有 d 的人能造出这样一对数，而任何"
        "人都能检查。<bookmark mark='e'/>由于糟糕的随机数会毁掉签名，RFC 6979 用 HMAC 由密钥和消息确定性地导出 k。<bookmark mark='f'/>我们的实现精确地"
        "复现了标准的测试签名。<bookmark mark='g'/>一切都系于 k：它必须保密、均匀，而且绝不能用两次。",
    "Here is what happens if k repeats.":
        "看看 k 重复时会发生什么。<bookmark mark='a'/>两条不同消息上的两个签名，用的是同一个随机数。每个签名的前一半 r 都相同：这就露馅了。<bookmark "
        "mark='b'/>把两个 s 相减：私钥抵消，剩下的部分由两个哈希给出 k。<bookmark mark='c'/>知道了 k，一行代数就给出私钥 d。<bookmark mark='d'/>我们的"
        "恢复正确地找出了两者，并为一条密钥主人从未批准的消息签了名；签名通过验证。<bookmark mark='e'/>这不是假设。2010年，fail0verflow 小组发现索尼给 "
        "PlayStation 3 软件签名时每次都用同一个 k，并从两个签名恢复出了主签名密钥。<bookmark mark='f'/>即使随机数只是偏了几位，只要签名足够多，也会通过"
        "第十四章的格方法泄露密钥。",
    # ------------------------------------------------------------------ PKI
    "Chapter eleven. Certificates, and trust.": "第11章。证书与信任。",
    "A signature tells you which key signed.":
        "签名告诉你是哪把密钥签的，却不告诉你那是谁的密钥。<bookmark mark='a'/>证书把一个名字绑定到一把公钥上，由证书颁发机构签名。这里，网站 pebble "
        "点 example 有一把密钥，由一个中间机构认证，而中间机构又由一个根机构认证。<bookmark mark='b'/>根的密钥不由任何人认证：它随浏览器或操作系统一起"
        "分发，在一个约一百五十张根证书的列表里。<bookmark mark='c'/>我们用自己的 ECDSA 签的这条链通过了验证。把网站名字改一个字符，签名就失败。攻击者"
        "用自己的密钥签的证书也会失败，因为没有受信任的根为它担保。<bookmark mark='d'/>所以信任是委托的：你信任根，根信任中间机构，中间机构为网站担保。",
    "The weakness of this system is its breadth.":
        "这个系统的弱点在于它的广度。<bookmark mark='a'/>任何受信任的根都能为任何名字签发证书，所以最不谨慎的那个机构决定了每个网站的安全。<bookmark "
        "mark='b'/>2011年，荷兰的证书机构 DigiNotar 被入侵，由受信任的根签发的 google 点 com 证书被用来拦截伊朗的用户。DigiNotar 被所有浏览器除名，随后"
        "破产。<bookmark mark='c'/>谷歌的 Ben Laurie 和 Adam Langley 给出的回应是证书透明：每张证书都必须记录在公开的、只能追加的日志里。<bookmark "
        "mark='d'/>这些日志就是第29部分的 Merkle 树。一个简短的证明表明某张证书在日志里，另一个证明表明日志只增长过，从未被改写。<bookmark mark='e'/>"
        "自2018年起，Chrome 拒绝无法证明已被记录的证书，所以错误签发的证书再也无法被秘密使用。<bookmark mark='f'/>而自2015年 Let's Encrypt 开始免费、"
        "自动地签发证书以来，网络的大部分已转向 HTTPS。",
    # ------------------------------------------------------------------ TLS
    "Chapter twelve. TLS 1.3.": "第12章。TLS 1.3。",
    "Everything so far comes together in TLS 1.3,":
        "前面的一切在 TLS 1.3 中汇合，它是 HTTPS 之下的协议，2018年标准化。我们在自己的两台机器之间跑了它的一个版本。<bookmark mark='a'/>客户端发出一个"
        "问候，里面有一把新鲜的 X25519 公钥。<bookmark mark='b'/>服务器回以它自己的公钥。现在双方都能算出同一个共享秘密，此后的每条消息都是加密的。"
        "<bookmark mark='c'/>服务器的下一批消息经过加密，带着它的证书链、对迄今所有对话的签名，以及一个叫 Finished 的 MAC。正是这个签名挫败了第四章"
        "的中间人：只有持有被认证密钥的人才能签出这份记录。<bookmark mark='d'/>客户端检查这一切，并发出自己的 Finished MAC。<bookmark mark='e'/>然后应用"
        "数据在认证加密下流动。一个往返，每项检查都通过了。",
    "Where do all those keys come from?":
        "这些密钥都从哪里来？<bookmark mark='a'/>交换得到的共享秘密经过 HKDF，这是 Hugo Krawczyk 用 HMAC 搭成的密钥派生函数；我们的实现与其标准的测试"
        "向量一致。<bookmark mark='b'/>它由一个秘密派生出握手、Finished MAC 和应用数据各自的密钥，每把都带标签，每把都混入了对话记录的哈希。所以只要"
        "攻击者改动任一个问候中的一个字节，什么都验证不过。<bookmark mark='c'/>交换用的密钥是临时的，用一次就丢弃。服务器的长期密钥只用来签名。"
        "<bookmark mark='d'/>这就是前向保密：攻击者记录下今天的流量，明年偷到服务器的密钥，仍然读不了它。用旧的 RSA 密钥传输，他们就能读。<bookmark "
        "mark='e'/>TLS 1.3 还删掉了早期版本中大部分出过错的东西：RSA 密钥传输、CBC 模式、自定义群、压缩和重新协商，它们都是著名攻击的对象。",
    # ------------------------------------------------------------------ Shor
    "Chapter thirteen. Shor's threat.": "第13章。Shor 的威胁。",
    "Every public-key system so far rests on factoring":
        "到目前为止的每个公钥系统，都建立在因数分解或离散对数之上。1994年，Peter Shor 证明量子计算机两者都能做到。关键在于，因数分解可以归结为寻找"
        "周期。<bookmark mark='a'/>取 N 等于十五、a 等于七，列出七的各次幂模十五：一、七、四、十三、一，然后再绕一圈。周期是四。<bookmark mark='b'/>七"
        "的四次方是一，所以十五整除七的平方减一乘以七的平方加一，最大公约数给出三和五。<bookmark mark='c'/>对二十一和三十五同样有效。<bookmark "
        "mark='d'/>对一个大的 N，周期长得天文数字一般，没有任何经典方法能比因数分解本身更快地找到它。<bookmark mark='e'/>量子计算机能把所有的幂放进"
        "叠加态，再用量子傅里叶变换读出周期，用时是多项式的。第53部分会搭建它，并在我们的模拟器上分解十五。<bookmark mark='f'/>同样的思想能在任何群"
        "里求离散对数。RSA、Diffie-Hellman 和椭圆曲线一起倒下。",
    "How close is the threat?":
        "威胁有多近？<bookmark mark='a'/>今天最大的量子计算机大约有一千个物理量子比特，噪声太大，在任何有用的规模上都跑不了 Shor 算法。<bookmark "
        "mark='b'/>攻破一把两千位的 RSA 密钥需要纠错，也就是把第28部分的主题移植到量子硬件上；Craig Gidney 2025年的估计是不到一百万个带噪量子比特，"
        "运行大约一周。<bookmark mark='c'/>这样的机器何时出现，没人知道。<bookmark mark='d'/>但对手现在就可以录下加密的流量，等机器到来时再解密，所以"
        "任何需要保密十年的秘密已经暴露在风险之中。<bookmark mark='e'/>2024年8月，美国标准机构发布了首批后量子标准：一个密钥封装机制 ML-KEM，以及两个"
        "签名方案。<bookmark mark='f'/>浏览器和大型网站已经启用了混合密钥交换，X25519 与 ML-KEM 一起用，只要其中任何一个安全，它就安全。<bookmark "
        "mark='g'/>对称密码学的处境要好得多：Grover 算法只把有效密钥长度减半。下一章搭建 ML-KEM 之下的数学。",
    # ------------------------------------------------------------------ Lattices
    "Chapter fourteen. Lattices.": "第14章。格。",
    "A lattice is a regular grid of points in space:":
        "格是空间里一组规则排列的点：几个基向量的所有整数组合。<bookmark mark='a'/>同一个格有许多组基。这两个又长又几乎平行的向量，九十、一百二十三和"
        "五十六、七十六，生成的点与这两个短向量完全相同。<bookmark mark='b'/>Gauss 的约化，从一个向量里减去另一个向量的倍数，几步就找到了短基。"
        "<bookmark mark='c'/>在二维这很容易。在几百维中，给定一组坏基去找一个短向量，被认为是困难的，而且与因数分解不同，还没有已知的量子算法能帮上"
        "忙。<bookmark mark='d'/>Arjen Lenstra、Hendrik Lenstra 和 László Lovász 在1982年提出的 LLL 算法，能在多项式时间内找到一个相当短的向量：与最短"
        "向量相差一个指数因子以内。密码学就生存在这个因子留出的缝隙里。",
    "LLL first appeared in cryptography as a weapon.":
        "LLL 最初是作为武器出现在密码学里的。<bookmark mark='a'/>1978年，Merkle 和 Hellman 提出把一串比特加密成一组公开权重中某个子集的和。<bookmark "
        "mark='b'/>这是我们二十个权重中的几个。<bookmark mark='c'/>陷门是一个简单的超递增序列，用模乘法伪装起来。<bookmark mark='d'/>Shamir 在1982年攻破"
        "了它；Lagarias 和 Odlyzko 证明，对这样的背包，秘密的比特构成由权重搭成的一个格中一个异常短的向量。<bookmark mark='e'/>我们的 LLL 找到了它，"
        "二十位全对。<bookmark mark='f'/>同一个工具能从有偏的随机数找出 ECDSA 密钥，也能攻破小指数选得不好的 RSA。<bookmark mark='g'/>所以基于格的方案必须"
        "把参数选在 LLL 及其更强的后继者远远够不到的地方。",
    "The problem post-quantum encryption uses":
        "后量子加密所用的问题，是 Oded Regev 在2005年提出的带误差学习。<bookmark mark='a'/>一个秘密向量 s；一个公开的随机矩阵 A；以及 b，它等于 A 乘 s "
        "加上一个小的随机误差，一切都模 q。没有误差，高斯消元能立刻找到 s。这点小噪声，就人们所知，让它变得困难：它是一个伪装起来的格问题。<bookmark "
        "mark='b'/>Regev 证明了一件不寻常的事：攻破随机实例，和解决最坏情况的格问题一样难，靠的是一个量子归约。密码学很少有这么强的保证。<bookmark "
        "mark='c'/>要加密一位，把公开样本中随机一个子集加起来，再加上这一位乘以 q 的一半。解密时减去秘密的贡献，剩下这一位乘 q 除以二，加上一点累积的"
        "噪声。这是四百次解密：零落在零附近，一落在 q 的一半附近，离边界很远。每一次都解密正确。",
    "Plain LWE needs enormous keys,":
        "普通的 LWE 需要巨大的密钥，所以标准用了结构。<bookmark mark='a'/>ML-KEM，以前叫 Kyber，处理模 x 的两百五十六次方加一的多项式，系数模三千三百"
        "二十九，排成小的向量和矩阵。<bookmark mark='b'/>多项式乘法用数论变换完成，也就是第19部分的 FFT 搬到有限域上：在我们的 Python 里，比课本式乘法"
        "快大约十二倍。<bookmark mark='c'/>我们实现了最小参数集的算术，加密了一百条两百五十六位的随机消息。每一位都解密正确。<bookmark mark='d'/>公钥"
        "八百字节，密文七百六十八字节：比椭圆曲线大，但对每次 TLS 握手都足够小。<bookmark mark='e'/>签名方面有一个格方案 ML-DSA，以及一个只用哈希函数"
        "搭成的保守方案 SLH-DSA。<bookmark mark='f'/>它的祖先是 Leslie Lamport 1979年的一次性签名：对消息哈希的每一位公布两个秘密的哈希，签名时每位揭示"
        "其中一个秘密。很大，而且只能用一次。<bookmark mark='g'/>用一棵 Merkle 树管理许多一次性密钥，就把它变成能签许多次的方案，其安全性只依赖于哈希"
        "函数。",
    # ------------------------------------------------------------------ Beyond
    "Chapter fifteen. Zero knowledge, secret sharing, and computing on secrets.": "第15章。零知识、秘密共享与在秘密上计算。",
    "Public-key ideas do more than encrypt and sign.":
        "公钥的思想不只能加密和签名。Claus Schnorr 的协议能证明你知道一个离散对数，而不泄露它。<bookmark mark='a'/>证明者承诺 g 的一个随机幂。<bookmark "
        "mark='b'/>验证者发出一个随机挑战。<bookmark mark='c'/>证明者回答 k 加 e 乘 x，由于 k 是随机的，它本身不透露任何关于 x 的信息。<bookmark "
        "mark='d'/>验证者检查一个等式。<bookmark mark='e'/>和第27部分一样，一个事先知道挑战的模拟者，不知道 x 也能造出看起来一样的对话记录：这就是零"
        "知识。<bookmark mark='f'/>Amos Fiat 和 Adi Shamir 的技巧用承诺与消息的哈希代替验证者，证明就变成了签名。<bookmark mark='g'/>我们的签名通过"
        "验证。<bookmark mark='h'/>SSH 和 Signal 用的签名 Ed25519 就是椭圆曲线上的 Schnorr，比特币也在2021年采用了 Schnorr 签名。",
    "A key that unlocks everything should not live in one place,":
        "一把能打开一切的密钥，不应该放在一个地方，也不应该交给一个人。Adi Shamir 1979年的答案是一个多项式。<bookmark mark='a'/>让秘密成为一个随机二次"
        "多项式在零处的值。把它在一、二、三、四、五处的值作为份额分发出去。<bookmark mark='b'/>任意三个份额就确定了这个多项式，靠第28部分的拉格朗日"
        "插值，于是也确定了秘密。在模一个素数的整数上，用我们的五个份额：一、二、三号份额给出三万一千三百三十七，二、四、五号也一样。<bookmark "
        "mark='c'/>两个份额与每一个可能的秘密都相容，所以它们什么也不透露：这里它们给出的是乱码。<bookmark mark='d'/>这些份额恰好是一个 Reed-Solomon "
        "码字。这个方案守护着备份密钥和门限签名，包括互联网 DNSSEC 根密钥的恢复。",
    "Two more ideas complete the picture.":
        "还有两个想法让图景完整。<bookmark mark='a'/>在多方计算中，几方各持一个私密输入，一起计算它们全部的一个函数，只得知结果。<bookmark mark='b'/>"
        "姚期智1986年的混淆电路，以及一年后 Goldreich、Micali 和 Wigderson 的协议，证明了任何函数都能这样计算。<bookmark mark='c'/>2008年，丹麦的甜菜农"
        "用一场以多方计算进行的拍卖确定了合同价格；今天，它被用来在不泄露密码的前提下对照泄露名单检查密码。<bookmark mark='d'/>全同态加密走得更远："
        "任何人都能在密文上计算，只有密钥持有者能读出结果。<bookmark mark='e'/>格加密允许这样做，但每次运算都会增加噪声，过一阵噪声就会淹没消息。2009年"
        "，Craig Gentry 找到了出路，自举：以同态方式计算解密本身，从而去掉旧的噪声。<bookmark mark='f'/>它曾比普通计算慢一万亿倍，如今已在生产中用于"
        "一些私密查询。<bookmark mark='g'/>还有差分隐私，来自《人工智能，从零搭建》第31部分，它保护的是从发布的数据中能学到的东西。",
    # ------------------------------------------------------------------ Frontier
    "Chapter sixteen. The frontier: post-quantum, and beyond.": "第16章。前沿：后量子，以及更远。",
    "Post-quantum cryptography rests on younger assumptions,":
        "后量子密码学建立在更年轻的假设上，有些没能幸存。<bookmark mark='a'/>格和哈希函数在2024年成为标准。2025年，一个基于编码的方案 HQC，建立在第28部分"
        "的数学之上，被选为基础不同的后备。<bookmark mark='b'/>但在2022年，两个领先的候选倒下了。Ward Beullens 用笔记本电脑一个周末就攻破了 Rainbow "
        "签名方案。Wouter Castryck 和 Thomas Decru 用一个核大约一小时攻破了基于椭圆曲线之间映射的 SIKE，用的是一个1997年的、从没人把它联系起来的定理。"
        "<bookmark mark='c'/>教训是老的：一个假设只有经受住多年的攻击才能赢得信任。这就是新系统把经典算法和后量子算法组合起来的原因，也是标准保留"
        "建立在不同数学上的后备方案的原因。",
    "Even lattices carry uncertainty.":
        "即使是格也带着不确定性。<bookmark mark='a'/>它们的安全级别是估计值：把已知最好的约化攻击外推到几百维。<bookmark mark='b'/>这些估计变动过，更好的"
        "筛法从每个方案的安全性中削掉了若干位。<bookmark mark='c'/>2024年4月，一篇预印本声称有一个在多项式时间内解带误差学习的量子算法，那将在新标准发布"
        "之前就攻破它们。<bookmark mark='d'/>不到十天，读者发现了一个错误，这个声称被撤回。<bookmark mark='e'/>没有任何证明说格问题能抵抗量子计算机。就像"
        " Shor 之前的因数分解一样，我们只知道还没有人找到办法。",
    "Six open problems.":
        "六个未解决的问题。<bookmark mark='a'/>因数分解或离散对数能否被普通计算机在多项式时间内解决。<bookmark mark='b'/>公钥加密能否像第29部分的一切那样"
        "由任意单向函数构造；Impagliazzo 和 Rudich 在1989年证明了标准的黑盒技术做不到。<bookmark mark='c'/>是否有量子算法能攻破新标准之下的格问题。"
        "<bookmark mark='d'/>选得好的椭圆曲线是否有比通用平方根更好的攻击。<bookmark mark='e'/>带误差学习的具体难度随维数增长得有多快，正是它决定了每一个"
        "后量子密钥长度。<bookmark mark='f'/>以及在加密数据上计算，能否便宜到接近在明文上计算。<bookmark mark='g'/>这一部分的研究题取第五个问题的一个"
        "可计算的小情形。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们搭建了什么。Merkle 谜题，以及从 Euclid 到拉格朗日的群的数论。Diffie-Hellman，以及从零写出的 RSA，外加困扰了它二十年的填充预言机。"
        "用 rho 和筛法做因数分解，用小步大步、Pohlig-Hellman 和指数演算求离散对数，正是它们决定了密钥长度。椭圆曲线、ECDSA，以及泄露了一台游戏机密钥"
        "的那个重复的随机数。证书和一次 TLS 1.3 握手。还有 Shor 的威胁，以及应对它的格。",
    "Where this comes back.":
        "这些内容在哪里还会出现。第37部分的 QUIC 把 TLS 1.3 放进传输协议本身。第38部分用签名在有机器撒谎时达成共识。第41部分给软件发布签名，第43部分"
        "在每两个服务之间加上双向 TLS。第53部分在我们的量子模拟器上运行 Shor 算法。第55部分回到认证：通行密钥，以及一个缺陷十七年无人察觉的著名协议。",
    "In practice.":
        "实践中。处处用 TLS 1.3，证书自动续期。优先用 X25519、Ed25519 或 P-256，RSA 只用大密钥。让经过审查的库来做签名，用确定性的或种子良好的随机数。"
        "打开混合后量子密钥交换，弄清楚你的哪些秘密需要保密十年以上。把私钥放在硬件里，备份分给几个人保管。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答见本部分的笔记。可以在任何一道上暂停。第五道是动手题：在我们的机器之间实现一次混合后量子握手。最后一道标着星号，是研究题："
        "小规模格攻击在哪里失效，是标准所依赖的问题，笔记里说明了从哪里入手。",
    "That completes Act Five, on limits and secrets.":
        "第五幕，极限与秘密，到此结束。接下来是第六幕：一台机器，许多程序。第31部分搭建内核：分时怎样让每个用户都以为自己拥有整台计算机，这需要怎样的"
        "保护，进程与系统调用，调度器，以及解释繁忙的服务器为什么比空闲的慢得多的排队论。第31部分，内核。",
    "The books and papers this part follows are on screen and in the notes.":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {}
