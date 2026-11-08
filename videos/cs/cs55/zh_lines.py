"""Chinese narration for cs55: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第55部分：对信任的信任"

CHAPTERS = {
    "Hook": "每一层都会泄漏",
    "Threats": "1. 威胁模型与原则",
    "Memory": "2. 内存破坏，以及面向返回的编程",
    "Safety": "3. 内存安全",
    "Hardware": "4. 当硬件泄漏时",
    "Auth": "5. 你是谁？身份认证",
    "Access": "6. 访问控制",
    "Isolation": "7. 隔离",
    "Web": "8. Web",
    "Networks": "9. 受到攻击的网络",
    "Supply": "10. 供应链",
    "Trojan": "11. 关于对信任的信任的反思",
    "Ddc": "12. 抓住特洛伊木马",
    "Tower": "13. 整座塔，从头到尾",
    "Frontier": "14. 前沿：这个系列的开放问题",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "This series built a tower, from gates to a cluster, and":
        "这个系列搭了一座塔，从门电路一直搭到集群，并且在每一层都宣称：上面的一层不必关心下面的一层是怎么工作的。<bookmark mark='a'/>安全，正是这个说法失效的地方。反复敲打内存的一行，它邻居里的比特就会翻转。"
        "越过一个分支去推测执行，一个秘密就会在缓存里留下痕迹。让缓冲区溢出，一个函数就会返回到攻击者的输入里。<bookmark mark='b'/>一个内核漏洞可以越过沙箱的墙；编译器可以插入一个在任何源代码里都看不到的后门；"
        "一条 BGP 通告就能偷走互联网的一块地址；在网页表单里输入的一个字符串会变成代码；而在2024年，一个压缩库的维护者在里面藏了一个后门，藏了两年。<bookmark mark='c'/>攻击者只需要一个薄弱的层。"
        "防御者却必须守住所有的层。",
    "And then there is the attack that closes this series.":
        "然后是为这个系列收尾的那种攻击。<bookmark mark='a'/>在1984年的图灵奖演讲里，肯·汤普森描述了一个编译器：每当它编译 login 程序，就插入一个后门；每当它编译一个编译器，就把它自己插进去。"
        "<bookmark mark='b'/>我们把它造出来了。这里是我们干净的编译器的哈希，被植入木马的那个编译器的哈希，<bookmark mark='c'/>以及一个编译器的哈希，它是由被植入木马的二进制文件，"
        "用干净的源代码重新构建出来的。后两个一模一样，逐字节相同。<bookmark mark='d'/>把木马从每一个源文件里删掉，它仍然永远活在二进制文件里，仍然让一个秘密密码进入 login。到这一部分结束时，"
        "我们会抓住它。",
    "This is Part 55 of Computer Science, Built, the last part":
        "这是《计算机科学，从零搭建》的第55部分，也是这门学位课程的最后一部分。<bookmark mark='a'/>我们会先列出威胁模型和经典的设计原则；破坏内存，不注入代码就把 gadget 串成链，然后看内存安全证明了什么；"
        "顺着硬件追踪泄漏；做身份认证，并用模型检验器找出一个著名协议的缺陷；做访问控制与隔离；攻破 Web、网络和供应链；搭建肯·汤普森的特洛伊木马并抓住它；最后，从一个与非门到一个集群，把整座塔再走最后一遍。",
    # ------------------------------------------------------------------ s02_threats
    "Chapter one. Threat models, and principles.":
        "第一章：威胁模型与原则。",
    "Before any attack or defence, one question: what does it":
        "在讨论任何攻击或防御之前，先问一个问题：一个系统“安全”意味着什么？<bookmark mark='a'/>经典的回答是三个承诺。机密性：只有应该读它的人才能读。完整性：只有应该改它的人才能改。可用性："
        "需要的时候它就在那里。<bookmark mark='b'/>三者只要有一个被破坏，系统就算被攻破了，而不同的系统对这三者的看重不同。银行更怕转账被伪造，而不是信息泄露；医院可能更怕记录丢失，而不是被人读到。"
        "安全从来不是绝对的；它永远是某个东西的安全，是针对某个人的安全。",
    "To defend a system you first describe the fight. That":
        "要保卫一个系统，先要描述这场较量。这份描述就是威胁模型。<bookmark mark='a'/>它列出值得保护的资产：这里是一个登录程序、文件和密钥。<bookmark mark='b'/>它围绕那个必须正确的部分画出一条信任边界，"
        "那就是可信计算基，并承认其中的一切都是被信任的，不论它配不配得上。<bookmark mark='c'/>它指明对手以及对手能做什么：能不能发送数据包，运行一个程序，待在同一台机器上，贿赂一个维护者？"
        "<bookmark mark='d'/>它还描绘出攻击面，也就是每一条进入的途径。危险永远在于模型遗漏的东西，因为那恰恰是攻击者会去找的地方。",
    "This part is a tour of attacks, so here are the":
        "这一部分是一次攻击之旅，所以先列出路标，日期都是这个系列有把握的。<bookmark mark='a'/>1988年，莫里斯蠕虫在早期的互联网上传播，部分是靠一个网络服务里的缓冲区溢出。<bookmark mark='b'/>1996年，"
        "一位以 Aleph One 为笔名写作的作者发表了一篇文章，把栈溢出讲得足够仔细，任何人都能跟着做。<bookmark mark='c'/>2014年，行锤攻击表明，软件可以翻转它从未碰过的内存里的比特；"
        "2018年，Spectre 和 Meltdown 表明，推测执行会泄露秘密；2024年，人们发现一个被广泛使用的压缩库里藏着后门。<bookmark mark='d'/>四十年，涵盖了我们所搭的塔的每一层。",
    "Fifty years ago Jerome Saltzer and Michael Schroeder":
        "五十年前，Jerome Saltzer 和 Michael Schroeder 把整个主题提炼成了几条设计原则，而这些原则几乎没有过时。<bookmark mark='a'/>让机制小到可以检查。默认拒绝，"
        "并有意识地授予访问权。每次访问都要检查，每一次都检查，不留任何跳过检查的捷径。<bookmark mark='b'/>不要把安全建立在设计保密之上，这个想法比他们更早，来自十九世纪的 Kerckhoffs："
        "假设敌人了解这个系统。对最危险的操作，要求不止一把钥匙。<bookmark mark='c'/>只给每个部分它所需要的权限；用户之间尽可能少地共享机制；而最重要的是，要让它好用，因为人们无法忍受的控制措施，"
        "人们就会把它关掉。他们还列出了两条：提高攻击者的工作因子，以及在无法阻止被攻破时，把它记录下来。",
    "There is a deep asymmetry underneath all of this.":
        "这一切的底下，有一种深刻的不对称。<bookmark mark='a'/>攻击者只需要找到一条路进去。防御者必须同时守住每一层，从硬件到供应链，而只要有一层薄弱就够了。<bookmark mark='b'/>这就是为什么实用的回答都很朴素。"
        "纵深防御：许多道并不完美的墙，这样攻破一道并不等于赢下全局。把可信计算基保持得小到你能承受的程度，因为其中的每一样东西，都必须是对的。还有现代安全的工作假设：你已经被攻破了，所以你还要计划如何发现它并恢复。"
        "这一部分的其余内容，会一层一层地走过这些层，并展示每一层是怎样泄漏的。",
    # ------------------------------------------------------------------ s03_memory
    "Chapter two. Memory corruption, and return-oriented":
        "第二章：内存破坏，以及面向返回的编程。",
    "We begin where Part 11 left a loose thread. A function":
        "我们从第11部分留下一个线头的地方开始。一个函数把它的局部变量放在栈上：这里是一个64字节的缓冲区、一些保存的寄存器，以及就在它们上方、这个函数将要返回到的地址。<bookmark mark='a'/>现在用一个没有边界的例程把输入复制进缓冲区。"
        "这就是 C 语言的 gets，它危险到在2011年被从语言里删除了。<bookmark mark='b'/>给它超过64字节，它就会一路写过缓冲区，覆盖保存的寄存器，再覆盖保存的返回地址。函数返回时，"
        "它会跳到那些被覆盖的字节所指的任何地方。<bookmark mark='c'/>让它指回缓冲区，那里现在放着攻击者自己的指令，于是程序就归他们了。这就是1988年莫里斯蠕虫用过的、1996年 Aleph One 的文章讲解的那种溢出。",
    "Three defences answered this attack, and we ran our":
        "有三种防御来应对这种攻击，我们让自己的 Pebble 溢出在每一种组合下都跑了一遍。<bookmark mark='a'/>栈金丝雀，是紧挨在返回地址之前的一个秘密的字，在退出时检查；溢出要碰到返回地址，"
        "会先改掉它。<bookmark mark='b'/>写异或执行，意思是内存可写或可执行，但绝不兼得，所以栈可以存放攻击者的字节，但处理器拒绝运行它们。<bookmark mark='c'/>地址空间布局随机化把地址打散，"
        "所以攻击者写下的那个地址，通常指向无处。<bookmark mark='d'/>看这张表：三者中的任何一个，都会把一次干净的接管变成一次崩溃，或者一次被抓住的尝试。现在攻击者需要同时击败这三者。",
    "ASLR is a probability, not a wall, so let us do the":
        "ASLR 是一种概率，而不是一堵墙，所以我们像第27部分那样来算一算。<bookmark mark='a'/>地址里有 k 个随机比特，就有 2 的 k 次方种等可能的放置方式，而一个固定的攻击只猜其中一种，"
        "所以它成功的概率是 2 的负 k 次方。<bookmark mark='b'/>如果每次尝试布局都重新随机化，那么到第一次命中所需的尝试次数，就是一个几何随机变量，均值是 p 分之一，也就是 2 的 k 次方。"
        "<bookmark mark='c'/>这是已发表的典型布局的熵：32位系统在一个基址上只有16比特，大约试65000次就能暴力破解，Shacham 和同事在2004年就做到了；64位系统则接近30比特。"
        "<bookmark mark='d'/>在 Pebble 上，一个可以运行的小版本精确地印证了这个公式：64种放置方式里，有一种匹配，比率是64分之1。",
    "W, xor, X stops injected code. In 2007 Hovav Shacham":
        "写异或执行能挡住被注入的代码。2007年，Hovav Shacham 表明，它挡不住攻击者。<bookmark mark='a'/>不用新代码，而是重用已经在那里的代码：以返回指令结尾的短指令序列，称为 gadget。"
        "<bookmark mark='b'/>溢出现在往栈上写下一串返回地址。每一次返回都跳到一个 gadget，它做一点工作，再返回到下一个。<bookmark mark='c'/>我们的 Pebble 二进制文件里有8个 gadget，"
        "用其中的一条链，就能让程序在写异或执行完全开启的情况下，打印出它的词并停机。栈上的代码一行也没有运行过。<bookmark mark='d'/>金丝雀仍然会最先被触发，这就是为什么真实的攻击链还需要一次泄漏。"
        "教训是：控制流是要保卫的资产。",
    "So defend control flow directly. <bookmark mark='a'/>":
        "那就直接保卫控制流。<bookmark mark='a'/>控制流完整性，由 Martin Abadi 和同事在2005年提出，在每一次间接跳转或返回时，检查目标是不是编译器允许的那一个；落在 gadget 中间的链会失败。"
        "<bookmark mark='b'/>影子栈为每个返回地址保留一份受保护的副本，如今已经做进了硬件。<bookmark mark='c'/>CHERI 让每个指针成为一个携带着自己边界的能力（capability）"
        "，所以伪造的指针造不出来。<bookmark mark='d'/>每一种都抬高了代价；没有一种能终结这场战争。能不能让语言本身使这个错误不可能发生？",
    # ------------------------------------------------------------------ s04_safety
    "Chapter three. Memory safety.":
        "第三章：内存安全。",
    "Canaries, W, xor, X and control-flow integrity all fight":
        "金丝雀、写异或执行和控制流完整性，都是在溢出被写出来之后才去对付它。这一章的问题是：我们能不能干脆不再写出它。这个问题之所以重要，原因是一个数字。<bookmark mark='a'/>2019年前后，"
        "Microsoft 和 Chromium 项目报告了同一件事：它们严重的安全漏洞里，大约70%是内存安全漏洞。<bookmark mark='b'/>缓冲区溢出，释放后使用，重复释放，读过数组末尾，未初始化的内存。"
        "不是什么巧妙的密码学攻破，而是同样的那几种错误，在允许人们犯这些错误的语言里，一遍又一遍地被犯下。<bookmark mark='c'/>如果一门语言能禁止这整个类别，它就能消除人们实际发布出去的大部分漏洞。",
    "Rust's answer reaches back to Part 14 and the typed":
        "Rust 的回答要追溯到第14部分和带类型的 λ 演算。<bookmark mark='a'/>在普通的类型系统里，有一条叫作收缩的规则：只要一个变量在作用域内，你想用多少次就能用多少次。<bookmark mark='b'/>去掉这条规则，"
        "就得到仿射类型，其中一个值最多只能用一次。Rust 的整套规矩都建立在这上面：每个值恰好有一个所有者，把它赋给别人就是移动它，于是旧的名字不能再用了。<bookmark mark='c'/>你可以把一个值借出去，"
        "而不是移动它。共享借用给出许多读者而没有写者；独占的可变借用给出一个写者，其他人都不行。每一次借用都会结束，把值还给它的所有者；但移动是最终的，使用你已经移动走的东西，是编译错误，而不是崩溃。",
    "To see what the rule buys, we built a toy borrow checker":
        "为了看看这条规则换来了什么，我们搭了一个玩具借用检查器，在10个小程序上运行它。<bookmark mark='a'/>它强制执行四件事，每一件都是一类真实错误的成因。移动之后不得使用，否则就是悬空引用。"
        "不得同时有两个可变借用，否则就是数据竞争。共享借用和可变借用不得同时存在，所以没有人在另一个人修改一个值的时候去读它。引用不得比它所指向的值活得更久，那就是换了个名字的释放后使用。<bookmark mark='b'/>每个被拒绝的程序，"
        "都是带着理由、在编译时被拒绝的，而每个合理的程序都被接受；移动一个值然后使用目的地，没问题，在它的生命周期内借出去，也没问题。<bookmark mark='c'/>这就是微缩版的借用检查器：它把那整整70%变成了编译器在程序运行之前就能抓住的错误。",
    "What exactly has been proved? <bookmark mark='a'/> A":
        "到底证明了什么？<bookmark mark='a'/>借用检查器接受的程序，从构造上就没有释放后使用，没有重复释放，没有数据竞争，也没有悬空指针。这种不存在是有保证的，而不只是测试过的。<bookmark mark='b'/>但有些事情确实需要裸指针，"
        "所以 Rust 保留了一个逃生口，标记为 unsafe，你用它来构建所有其他人所依赖的安全数据结构。危险并没有被消除；它被圈进了一些小块里，人可以对它们逐一审查。<bookmark mark='c'/>而在这里，"
        "这个系列把一个圈合上了。2018年，RustBelt 项目给出了一个机器检查的证明：即使把标准库里的那些 unsafe 代码计算在内，这个类型系统依然是可靠的，这正是第54部分的想法：缩小可信的基础，"
        "然后验证它。<bookmark mark='d'/>它不是万灵药。逻辑错误依然存在，unsafe 的核心仍然必须是对的，而世界上现有的 C 和 C++ 不会自己重写，这个问题我们留给前沿。",
    # ------------------------------------------------------------------ s05_hardware
    "Chapter four. When the hardware leaks.":
        "第四章：当硬件泄漏时。",
    "Start at the bottom of the tower, with the memory itself,":
        "从塔的最底层开始，从内存本身开始，回想第5部分。<bookmark mark='a'/>选两行 DRAM，轮流打开它们，一遍又一遍，以机器允许的最快速度。<bookmark mark='b'/>每一次激活，"
        "都会在物理上干扰它们之间的那一行，从它的单元里漏走一点电荷，而这些单元，程序根本从来没有碰过。<bookmark mark='c'/>2014年，Yoongu Kim 和同事测量了这一点：在129条 DDR3 内存条里，"
        "有110条出现了比特翻转，有些只需要大约139000次激活，远远落在一个64毫秒的刷新周期之内。一个可靠性的余量，悄悄变成了安全的边界。<bookmark mark='d'/>这些防御，更频繁地刷新、"
        "对激活计数、纠错码，每一种都有帮助，也每一种后来都被绕过了：2020年，新的访问模式在配备了所有这些措施的 DDR4 上翻转了比特。",
    "Now climb one layer, to the processor, and recall Part 8.":
        "现在往上爬一层，到处理器，回想第8部分。<bookmark mark='a'/>为了保持快速，核心会猜一个分支往哪边走，并在猜测被检验之前就往前跑。这里它猜一个下标在界内，于是推测地读过了数组的末尾，"
        "然后用那个秘密字节去触碰探测数组的一行。<bookmark mark='b'/>当猜测被证明是错的，处理器会把这些工作回滚：在体系结构层面，那些指令从未发生过。但它所触碰的那条缓存行依然是热的，这一点它无法撤销。"
        "<bookmark mark='c'/>于是攻击者给每一行的读取计时；快的那一行，就指明了那个秘密字节。这个计时的技巧是 Flush and Reload，由 Yarom 和 Falkner 在2014年提出，"
        "而2018年披露的 Spectre 和 Meltdown，正是靠它读到了跨越边界的内存，而每一次边界检查、每一个特权位都说这条边界是关闭的。",
    "Rowhammer and Spectre are two cases of a wider truth, the":
        "行锤攻击和 Spectre 是一个更宽泛的真相的两个例子，也是第8部分和第29部分一再遇到的那个真相。<bookmark mark='a'/>一次计算说出的，比它的输出更多。它通过自己花多长时间、耗多少电力、"
        "在缓存里留下什么，甚至电容发出的声音，泄露信息。<bookmark mark='b'/>经典的例子是一个遇到第一个错误字节就停下的比较。猜测对的部分越多，它运行得越久，于是时间悄悄告诉攻击者他们有多接近，"
        "他们就一次一个字节地恢复出一个秘密。Paul Kocher 在1996年表明，单靠计时就能攻破真实的密码学。<bookmark mark='c'/>防御的办法，是写出这样的代码：它的运行时间和内存使用完全不依赖于那个秘密，"
        "于是那条线是平的。这叫作恒定时间代码，它既是一种技术，也同样是一种纪律。",
    "Step back, because these share one shape, and it is the":
        "退后一步，因为这些情形有着同一个形状，它就是整个系列的主线。<bookmark mark='a'/>每一层都做出一个承诺，好让上面的一层不必往下看。内存保存你写进去的东西。被回滚的工作不留痕迹。你得到的只有答案。"
        "<bookmark mark='b'/>侧信道，就是底下的物理，电荷、时间、共享的缓存，透过这个承诺显露出来。<bookmark mark='c'/>而且修复从来不是免费的：一道推测屏障或者更快的刷新，"
        "要付出真实的性能代价，所以第9部分的屋顶线朝错误的方向移动了。<bookmark mark='d'/>这个领域所选择的方向，是不再假装，并把硬件和软件之间的一份契约写下来，准确说明下面一层承诺不泄漏什么，"
        "好让上面一层终于可以依赖它。",
    # ------------------------------------------------------------------ s06_auth
    "Chapter five. Who are you? Authentication.":
        "第五章：你是谁？身份认证。",
    "Start with the oldest answer: something you know.":
        "从最古老的回答开始：你知道的东西。<bookmark mark='a'/>一个由 L 个符号组成的密码，每个符号取自 N 个字符的字母表，它是 N 的 L 次方种可能中的一种。<bookmark mark='b'/>它以比特计的熵，"
        "是这个数目以2为底的对数，<bookmark mark='c'/>也就是 L 乘以 N 的以2为底的对数。<bookmark mark='d'/>每秒测试 R 次猜测，攻击者预期要搜索一半的空间：2 的 H 次方除以 2R。"
        "<bookmark mark='e'/>以每秒100亿次猜测计，这是一块显卡上的快速哈希，8个小写字母只能撑大约10秒；16个能撑大约7万年。",
    "But entropy assumes a random choice, and people do not":
        "但熵假设的是随机选择，而人们并不随机选择。<bookmark mark='a'/>大型研究，包括 Joseph Bonneau 在2012年的那一项，发现人们的选择接近齐普夫定律：第 r 流行的密码，"
        "被选中的概率与 r 分之一成正比。<bookmark mark='b'/>在我们这个有1000万个密码的示意模型里，猜10次就覆盖18%的用户，猜100万次覆盖86%。<bookmark mark='c'/>这个占比是调和数的比值，"
        "而调和数就是一个对数，<bookmark mark='d'/>所以每把猜测次数增加到10倍，就加上同样大的一块，大约14个百分点。",
    "Assume the password file will be stolen, and make the":
        "假设密码文件会被偷走，并让这次偷窃换不来多少东西。<bookmark mark='a'/>只存哈希。不加盐的话，相同的密码给出相同的哈希，一张预先算好的表就能把它们全部破解。<bookmark mark='b'/>给每个用户一个随机的盐，"
        "让每一项都不同，于是每个用户都必须单独攻击。<bookmark mark='c'/>然后有意把哈希做慢：时间与速率成反比，<bookmark mark='d'/>所以从每秒100亿次猜测降到每秒10次，"
        "是10亿倍的差距：8个小写字母现在每个核心要超过300年。<bookmark mark='e'/>这就是第29部分的 bcrypt、scrypt 和 Argon2，后两者还要求用内存。",
    "A second factor proves something you have. <bookmark":
        "第二因素证明的是你拥有的东西。<bookmark mark='a'/>验证器应用的验证码遵循 RFC 6238，发布于2011年。手机和服务器共享一把密钥，各自把时间除以30秒并向下取整，得到一个计数器。"
        "<bookmark mark='b'/>各自对这个计数器取一个 HMAC，在哈希自己所指的位置截取4个字节，并保留最后6位或8位数字。<bookmark mark='c'/>我们的实现精确地复现了标准里的测试值。"
        "<bookmark mark='d'/>在59秒时计数器是1，验证码末尾的6位数字，和较早的基于计数器的验证码在计数器为1时的一样：是同一种计算。<bookmark mark='e'/>但它仍然是要键入的，"
        "所以假页面可以把它转发出去。",
    "Passkeys drop the shared secret, using Part 30's":
        "通行密钥（passkey）抛开了共享的秘密，用的是第30部分的签名。<bookmark mark='a'/>注册时，设备为这一个网站生成一对密钥，只把公钥那一半交给服务器。<bookmark mark='b'/>登录时，"
        "服务器发来一个随机的挑战，浏览器加上它真正在与之通信的源，设备对两者一起签名。<bookmark mark='c'/>服务器检查签名。没有任何秘密需要键入，被偷走的数据库也登录不了任何人。<bookmark mark='d'/>一个外观相似的网站，"
        "只能得到一个对错误的源的签名，或者什么也得不到。这就是 WebAuthn，自2019年起是 W3C 推荐标准。",
    "Across a network, logging in is a protocol. <bookmark":
        "跨越网络登录，是一个协议。<bookmark mark='a'/>1978年，Roger Needham 和 Michael Schroeder 提出了这一个：Alice 把一个一次性随机数（nonce）"
        "和她的名字，封装给 Bob 发过去；他把她的随机数连同他自己的一个返回；她再把他的那个返回。<bookmark mark='b'/>1995年，Gavin Lowe 把它放进模型检验器里跑了一遍。Alice 与入侵者开启了一次诚实的会话，"
        "入侵者把她的消息重新为 Bob 封装。Bob 的回复是为 Alice 封装的，所以入侵者原样转发而不读它，于是 Alice 把 Bob 的随机数返回给了入侵者。<bookmark mark='c'/>Bob 相信他在和 Alice 说话，"
        "而入侵者握有了他的秘密。<bookmark mark='d'/>我们第54部分的检验器，在19个状态之中找到了同样的攻击。<bookmark mark='e'/>Lowe 的修复只是一个名字：Bob 把他自己的名字放进回复里，"
        "攻击就不再存在。",
    # ------------------------------------------------------------------ s07_access
    "Chapter six. Access control.":
        "第六章：访问控制。",
    "Authentication says who you are; access control decides":
        "身份认证说明你是谁；访问控制则决定你随后可以做什么。<bookmark mark='a'/>Butler Lampson 1971年的论文《保护》（Protection），给了这个领域它的图景：一个矩阵，"
        "侧边是主体，比如用户和进程，顶端是客体，比如文件，每个格子里是一方对另一方持有的权限。<bookmark mark='b'/>引用监视器在每一次访问时都查询它。<bookmark mark='c'/>但真实的系统有几百万个主体和客体，"
        "几乎每个格子都是空的，所以没有人把矩阵完整地存起来。",
    "So systems store it in slices, and there are two ways to":
        "所以系统是把它切成片来存的，有两种切法。<bookmark mark='a'/>沿着一列切，随对象保存：访问控制列表，也就是谁可以碰这个文件，以及怎样碰。Unix 的权限位就是一种压缩过的访问控制列表。"
        "<bookmark mark='b'/>沿着一行切，由主体持有：一张能力（capability）的列表，能力是不可伪造的令牌，既指明一个对象，又带着对它的一项权利，就像文件描述符那样，打开之后，只靠是否持有来检查。"
        "<bookmark mark='c'/>列表放在对象上，撤销就容易；令牌握在手里，委托就容易，避免一个经典的错误也容易。",
    "Norm Hardy described that mistake in 1988, and called it":
        "Norm Hardy 在1988年描述了那个错误，并把它叫作混淆代理（confused deputy）。<bookmark mark='a'/>一个编译器服务可以写它自己的两个文件，一个计费日志和它的调试输出，"
        "而客户端指定调试输出所用的文件。<bookmark mark='b'/>在环境权限（ambient authority）之下，服务用自己的权限来写，不管给它的是什么名字，所以指定了计费文件的客户端，会让它被覆盖，"
        "凭的是客户端从未拥有过的权限。我们的运行恰好就是这样。<bookmark mark='c'/>有了能力，客户端就必须交出输出文件的令牌，而它只持有调试文件的令牌，所以这次写入被拒绝。<bookmark mark='d'/>指名一个东西，"
        "和持有对它的权利，变成了同一个动作。",
    "Sometimes the rule is about secrecy, not ownership.":
        "有时规则关乎保密，而不是所有权。<bookmark mark='a'/>1973年，David Bell 和 Leonard LaPadula 把军事密级形式化了：每个主体和客体都带有一个标签，包括一个级别和一组类别。"
        "<bookmark mark='b'/>一个主体只能读它的标签所支配的东西：不得上读。<bookmark mark='c'/>而它只能写入标签支配自己的对象：不得下写，所以一个秘密的进程不能复制进一个未分级的文件。"
        "<bookmark mark='d'/>把两条串起来，一个主体从一个对象复制到另一个对象的任何东西，都只会往上走，绝不往下。<bookmark mark='e'/>我们的检查结果与此一致，包括一条升了一级却依然被拒绝的流动，"
        "原因是缺少一个类别。Biba 1977年的模型是它的镜像，针对的是完整性。",
    "Protection states also change, as owners grant rights.":
        "保护状态也会改变，因为所有者会授予权限。<bookmark mark='a'/>1976年，Harrison、Ruzzo 和 Ullman 把一个系统建模成一组命令，每条命令是对矩阵的一次测试，后面跟着若干基本的修改。"
        "这里，所有者可以授予读权限，也可以授予所有权本身。<bookmark mark='b'/>它安全吗？有没有哪一串命令，能把读权限放进一个原本没有它的格子里？<bookmark mark='c'/>我们的广度优先搜索立刻就发现了一处泄漏："
        "Alice 授予 Eve 读权限。<bookmark mark='d'/>一个唯一的命令是撤销的系统，是安全的。但我们的搜索是有界的，所以“安全”指的是在预算之内安全。",
    "Could a better search always answer? No, and the reason":
        "更好的搜索能不能总是给出答案？不能，原因在第25部分。<bookmark mark='a'/>取任意一台图灵机。把每个纸带格子做成一个主体，把它的符号，以及读写头所在之处的状态，写在对角线上，并让每个格子拥有下一个格子："
        "矩阵就是纸带。<bookmark mark='b'/>机器的每条规则变成一条命令。<bookmark mark='c'/>停机状态的那项权限，恰好在机器停机时出现，所以判定安全性，就等于判定停机。<bookmark mark='d'/>只有对受限的系统，"
        "安全性才是可判定的，比如那些每条命令只做一处修改的系统：这是支持采用简单保护规则的一个有力理由。",
    # ------------------------------------------------------------------ s08_isolation
    "Chapter seven. Isolation.":
        "第七章：隔离。",
    "The first wall between programs is one we built in Parts":
        "程序之间的第一堵墙，是我们在第31和32部分搭起来的。<bookmark mark='a'/>每个进程都有一张页表，并且只能指称它的页表所映射的内存。<bookmark mark='b'/>两个进程使用同一个地址，"
        "第1页，却到达了不同的页框，彼此毫不知情。<bookmark mark='c'/>触碰一个没有映射的页，或者一个留给内核的页，硬件就会陷入内核。只有内核可以修改页表，因为只有它是在模式位被设置的情况下运行的。"
        "<bookmark mark='d'/>所以这堵墙恰好和内核一样强，而它那几千万行代码中的每一行，都是被信任的。<bookmark mark='e'/>seL4 内核大约有一万行，已被证明会强制执行它的隔离。",
    "Processes are one rung on a ladder of walls. <bookmark":
        "进程只是墙的阶梯上的一级。<bookmark mark='a'/>语言沙箱在一个进程里运行好几个程序。进程共享一个内核。容器是被赋予了自己对文件和名字的视图的进程，仍然在同一个内核上。虚拟机各自带着一个内核，"
        "共享一个虚拟机管理程序。独立的机器只共享网络。<bookmark mark='b'/>往右走，共享的东西越来越少，墙越来越强，但每一级运行和启动的代价都更高。<bookmark mark='c'/>而逃逸会穿过任何被共享的东西："
        "任何内核漏洞，比如2016年那个叫 Dirty COW 的写时复制竞争，都可能是一次容器逃逸。<bookmark mark='d'/>2015年，一个叫 VENOM 的漏洞，出在一个被模拟的软盘控制器里，"
        "让一台虚拟机攻击了它的宿主机。",
    "A process can also shrink its own power. <bookmark":
        "一个进程也可以缩小自己的权力。<bookmark mark='a'/>浏览器的渲染器要解析恶意的页面，所以它一启动，就给自己的系统调用装上一个过滤器。<bookmark mark='b'/>白名单上的调用，"
        "比如 read、write 和 exit，可以通过。打开文件、启动程序和创建套接字则被拒绝，所以即使是被攻击者完全控制的渲染器，也几乎只能做计算。<bookmark mark='c'/>这就是被机械化的最小权限："
        "Linux 自2005年起就以 seccomp 的形式提供它，自2012年起，过滤器是以小型 BPF 程序的形式来写的。<bookmark mark='d'/>FreeBSD 在2010年的 Capsicum 走得更远："
        "调用一次之后，进程就丢掉每一个全局名字，只保留它手里持有的描述符，也就是上一章的那些能力。",
    "The browser is where these walls meet strangers' code":
        "浏览器，是这些墙每天与陌生人的代码相遇的地方。<bookmark mark='a'/>一个有特权的浏览器进程与网络和磁盘打交道，每个网站都在它自己的沙箱化渲染器里运行。<bookmark mark='b'/>在 Spectre 之后，"
        "同一个地址空间里的任何东西，都可能被推测执行读到，所以网站之间的墙必须是一个进程，2018年，Chrome 在桌面端默认打开了站点隔离。<bookmark mark='c'/>在页面内部，WebAssembly，"
        "自2017年起存在于每一个主流浏览器中，是一个进程之内的沙箱：每一次加载，都要对照它的线性内存做检查，控制流只能到达经过验证的代码。<bookmark mark='d'/>64位的引擎会把32位下标所能到达的整个范围保留下来，"
        "再加上保护页，所以边界检查就是第32部分的分页，由硬件来完成。",
    "Every wall so far trusts the kernel. An enclave turns":
        "到目前为止，每一堵墙都信任内核。飞地（enclave）把这一点反了过来。<bookmark mark='a'/>Intel 自2015年起的 SGX，让应用程序封存一块内存区域，处理器会把它加密，并且连操作系统和虚拟机管理程序也不让碰，"
        "它还可以向远程的一方证明里面是什么代码。<bookmark mark='b'/>但操作系统仍然管理着飞地的页表。2015年，Xu、Cui 和 Peinado 表明，它可以取消页的映射，并观察飞地在哪些页上出错；"
        "当一个分支取决于一个秘密时，那串页的序列就把它拼写了出来。<bookmark mark='c'/>2018年，Foreshadow 用推测执行直接读出了飞地的内存。<bookmark mark='d'/>飞地依然与它所排除的对手共享核心、"
        "缓存和页表。隔离的好坏，只取决于没有被共享的东西。",
    # ------------------------------------------------------------------ s09_web
    "Chapter eight. The web.":
        "第八章：Web。",
    "A web page runs code from whoever sent it, so the browser":
        "网页会运行发送它的任何人的代码，所以浏览器需要一条规则，规定这些代码可以碰谁的数据。<bookmark mark='a'/>这就是同源策略，而一个源由三样东西组成：协议、主机和端口。<bookmark mark='b'/>脚本只能读来自它自己那个源的东西。"
        "改变协议或端口，或者加上一个子域名，它就是陌生人。<bookmark mark='c'/>但页面仍然可以向它读不了的源发送请求，大多数 Web 攻击就存在于这道缝隙里，或者存在于那些溜进某个源内部的代码里。",
    "The first way in is to slip inside. <bookmark mark='a'/>":
        "第一种进入的办法，是溜进去。<bookmark mark='a'/>一个网站通过模板显示评论，而有人发表的评论是一段脚本。<bookmark mark='b'/>被原样粘贴进去，它的字节就会作为标记，"
        "到达浏览器的 HTML 解析器，也就是第42部分的那台状态机。<bookmark mark='c'/>解析我们的输出，会发现一个活动的 script 元素，它会以网站自己的权限运行，并读取用户的 cookie："
        "这就是跨站脚本。<bookmark mark='d'/>把同样的字节转义，解析器就只看到文本。<bookmark mark='e'/>防御是层层叠加的：按上下文转义，一条拒绝内联脚本的内容安全策略（Content Security Policy）"
        "，以及脚本看不见的 HTTP-only cookie。",
    "The second way in uses the gap. <bookmark mark='a'/> You":
        "第二种进入的办法，利用的是那道缝隙。<bookmark mark='a'/>你在登录着银行的时候，访问了一个恶意页面，它提交了一个指向银行的隐藏表单。<bookmark mark='b'/>你的浏览器发出这个请求，"
        "并且像对银行的每一个请求那样，附上你的会话 cookie。<bookmark mark='c'/>银行看到一个有效的会话，于是照办。<bookmark mark='d'/>浏览器就是第六章的那个混淆代理，"
        "把自己的环境权限借给任何指名银行的人。<bookmark mark='e'/>修复办法也来自那一章：同站 cookie 不随像这样的跨站请求发送，而每个真实表单里的秘密令牌，就是恶意页面读不到的一种能力。",
    "Now the same confusion on a server, with Part 35's":
        "现在是服务器上的同一种混淆，用的是第35部分的数据库引擎。<bookmark mark='a'/>一次查询，通过把用户的输入粘贴进 SQL 文本来构造它的查询语句。<bookmark mark='b'/>输入 2，"
        "解析器就把列 id 与字面量 2 比较，返回一行。<bookmark mark='c'/>输入字母 i、d，解析器就读到了第二个列名。id 等于 id，对每一行都成立，过滤条件就消解了，于是我们的引擎返回了全部三个秘密。"
        "<bookmark mark='d'/>什么都没有溢出，什么都没有靠猜：输入到达了解析器，并改变了程序的形状。注入在1998年被公开描述，至今仍是最常见的 Web 缺陷之一。",
    "The cure is not to hunt for dangerous characters. It is":
        "解药不是去搜寻危险字符。它是第12部分关于解析的那一课。<bookmark mark='a'/>把模板解析一次，给每个值留一个洞，这样在任何输入到达之前，树的形状就已经固定；然后把值作为现成的叶子放进去，"
        "绝不作为文本。<bookmark mark='b'/>这样绑定之后，i、d 只是一个字符串，没有哪个用户叫这个名字。<bookmark mark='c'/>把经典的登录攻击载荷用两种方式各跑一遍。粘贴进去的时候，"
        "它们到达我们的解析器，解析器会在它不支持的语法上停下；而一个完整的数据库会照办。绑定之后，每一个都只是一个奇怪的用户名。",
    "Beneath it all sits Part 30's public-key infrastructure,":
        "在这一切的底下，是第30部分的公钥基础设施，而它也可能失效。<bookmark mark='a'/>你的浏览器信任一个根机构的库，而其中任何一个都可以为任何名字担保。<bookmark mark='b'/>2011年，"
        "荷兰的机构 DigiNotar 被攻破，一份针对每一个 google 点 com 地址的证书被签发出来，并被用来拦截伊朗的用户。<bookmark mark='c'/>固定了 Google 密钥的 Chrome 注意到了；"
        "各个浏览器移除了 DigiNotar，它在当年之内就破产了。<bookmark mark='d'/>结构性的修复，是2013年起的证书透明度（Certificate Transparency），它把每一份证书放进公开的、"
        "只能追加的 Merkle 日志里，所以流氓证书藏不住。",
    # ------------------------------------------------------------------ s10_networks
    "Chapter nine. Networks under attack.":
        "第九章：受到攻击的网络。",
    "Every packet carries two addresses, and the network only":
        "每个数据包都带着两个地址，而网络只关心其中一个。<bookmark mark='a'/>路由器按目的地址转发，也就是第36部分的最长前缀匹配，而沿途没有任何东西检查源地址。<bookmark mark='b'/>所以攻击者可以在那里写上别人的地址。"
        "<bookmark mark='c'/>数据包照常传输，反射器回答它，而回答被送到了伪造的源地址，一个从未发出过请求的受害者那里。<bookmark mark='d'/>修复办法自2000年起就已为人所知，"
        "即最佳当前实践第38号：每个边缘网络丢弃源地址不属于自己的数据包。它只在部署的地方起作用，而并非到处都部署了。",
    "Add a protocol whose answer is bigger than its question,":
        "加上一个回答比提问更大的协议，伪造的源地址就成了一根杠杆。<bookmark mark='a'/>攻击者每秒发送 n 个小请求，每个 q 字节，全都声称来自受害者。<bookmark mark='b'/>每个反射器用 r 字节来回答，"
        "而每一个回答都落到了受害者身上。<bookmark mark='c'/>用一个速率除以另一个速率，n 就消掉了：<bookmark mark='d'/>受害者收到的，是攻击者所发出的 A 倍，A 是回答的大小除以提问的大小。"
        "<bookmark mark='e'/>这需要 UDP，没有握手；而一个 TCP 连接必须先证明它的源地址能够接收，第37部分的握手在做安全的工作。",
    "How big is A? <bookmark mark='a'/> America's computer":
        "A 有多大？<bookmark mark='a'/>美国的计算机应急小组在2014年公布了实测的放大系数：一种管理协议大约是6，设备发现和 DNS 是几十；<bookmark mark='b'/>一种老的诊断服务和 NTP，"
        "也就是时间协议，是几百。<bookmark mark='c'/>2018年出现了 memcached，一种有些人让它向互联网敞开的缓存服务器：最高达到51000。那年2月，GitHub 承受了其中大约每秒1.35太比特。"
        "<bookmark mark='d'/>1兆比特的伪造提问，变成51吉比特的回答。防御办法：过滤源地址，关闭开放的反射器，并在第37部分的任播边缘吸收其余的流量。",
    'f"Between networks, BGP believes what it is':
        "在网络之间，BGP 别人说什么就信什么。<bookmark mark='a'/>在第36部分那个有125个网络的互联网上，一个地址块的所有者宣告它，所有网络就都往那里路由。<bookmark mark='b'/>如果一个陌生人宣告同一个地址块，"
        "离它更近的{say(origin)}个网络，就会相信这个陌生人。<bookmark mark='c'/>如果它宣告里面一个更具体的地址块，最长前缀就在所有地方胜出，每个网络都把流量送往错误的方向：这就是巴基斯坦电信2008年对 YouTube 做的事，"
        "出于失误。<bookmark mark='d'/>有签名的路由起源，也就是 RPKI，一个网络一个网络地修复它：在四分之一的网络做检查的情况下，仍有{say(rov)}个被骗。",
    'f"Part 37 met Kaminsky':
        "第37部分见过 Kaminsky 对 DNS 的攻击。这是它的算术。<bookmark mark='a'/>在每一场赛跑中，攻击者发送 k 个伪造的回答，每一个都在猜解析器的那个 H 比特的数。<bookmark mark='b'/>一个新的随机名字，"
        "让每场赛跑都成为一次新的尝试，所以赛跑的期望次数是 p 分之一：2 的 H 次方除以 k。<bookmark mark='c'/>只有16比特的查询标识符，每场赛跑伪造100个，就是大约{say(ex['fixed port'])}场赛跑，"
        "大约一分钟。<bookmark mark='d'/>2008年的修复把源端口也随机化了：多出16比特，大约{say(mil)}00万场赛跑，约{say(sec['random port'] / 86400)}天。"
        "<bookmark mark='e'/>随机性只是抬高了价格。用 DNSSEC 给回答签名，则消除了这个猜测。",
    "So what should a program believe about the network?":
        "那么，一个程序应该相信网络的什么？什么都不信。<bookmark mark='a'/>在你和一台服务器之间，隔着链路、服务提供商、解析器和中转网络，其中任何一个都可能读取、丢弃、延迟或伪造。<bookmark mark='b'/>第36部分的端到端论证说，"
        "要把重要的事情放在两端去做，TLS 正是这样做的：两端之间用第30部分的数学商定的密钥，守护所说的内容、它到达时是否未被更改，以及是谁作了回答，只要证书可靠。<bookmark mark='c'/>任何加密都守护不了的，"
        "是数据包到底到不到得了，以及谁在和谁说话。可用性是用容量和过滤换来的，而不是用密钥。",
    # ------------------------------------------------------------------ s11_supply
    "Chapter ten. Supply chains.":
        "第十章：供应链。",
    "A program trusts far more than its compiler. <bookmark":
        "一个程序所信任的，远远不止它的编译器。<bookmark mark='a'/>它点名了3个依赖；这些依赖又点名了6个；那6个再点名12个，每一个都出自陌生人之手，并以你的程序的权限运行。<bookmark mark='b'/>如果每一个独立地以 1 减 p 的概率是干净的，"
        "那么全部 n 个都干净的概率，就是 1 减 p 的 n 次方。<bookmark mark='c'/>取对数；<bookmark mark='d'/>当 p 很小时，1 减 p 的对数约等于负 p，<bookmark mark='e'/>所以什么都没有坏的概率，"
        "大约是 e 的负 np 次方。<bookmark mark='f'/>1000个包，万分之一是坏的：出问题的概率是十分之一，这是由最不小心的那个陌生人决定的。",
    "In 2021 Alex Birsan turned a resolver's own rules against":
        "2021年，Alex Birsan 把解析器自己的规则变成了对付它自己的武器。<bookmark mark='a'/>公司把内部的包放在一个私有注册表里，用的名字会在公开的代码里泄露出去。<bookmark mark='b'/>在公共注册表上，"
        "用更高的版本号发布同一个名字，<bookmark mark='c'/>那么一个两处都会查找的安装程序，就会选最高的那个，不管它在哪里；陌生人的安装脚本就在公司内部运行了起来。他触达了几十家公司，并向它们报告了此事。"
        "<bookmark mark='d'/>修复办法是名字和哈希：一个你所拥有的命名空间，每个名字只对应一个注册表，并且每个包都用它的内容哈希固定下来，也就是第41部分的锁文件。",
    "The build is another way in. <bookmark mark='a'/>":
        "构建，是另一条进入的路。<bookmark mark='a'/>SolarWinds 出售 Orion，这是一款监控网络的软件，因此被信任可以接触这些网络。<bookmark mark='b'/>处于它构建环境内部的攻击者，"
        "让构建在运行时插入了一个后门，所以源代码仓库一直是干净的，<bookmark mark='c'/>随后每个二进制文件都用公司自己的密钥签了名，作为例行更新发布出去。<bookmark mark='d'/>2020年12月披露这件事时，"
        "是 FireEye 在调查它自己遭到的一次攻破时发现的，SolarWinds 给出的安装了它的客户数量是不到18000家。<bookmark mark='e'/>签名是真的。它说明的是谁构建了这个二进制文件，"
        "而不是它由什么构建而成。",
    "And sometimes the supplier is the attacker. <bookmark":
        "而有时，供应商就是攻击者。<bookmark mark='a'/>2021年，一个新人开始向 xz-utils 提交补丁，那是一个压缩库，几乎存在于每一个 Linux 系统里，由一位志愿者维护。<bookmark mark='b'/>另一些账号催促他把工作分出去，"
        "于是这个新人成了共同维护者。<bookmark mark='c'/>2024年初，有两个发布版本带着一个后门。<bookmark mark='d'/>它不在审阅者阅读的仓库里，而在各发行版用来构建的发布归档里，"
        "在那里，一份被修改过的构建脚本，把藏在二进制测试文件里的代码解包进了这个库。<bookmark mark='e'/>在 OpenSSH 的服务器通过 systemd 加载这个库的地方，它拦截了对客户端密钥的检查，"
        "所以只有攻击者的密钥才能打开它。",
    "It was found by accident. <bookmark mark='a'/> On the":
        "它是意外被发现的。<bookmark mark='a'/>2024年3月29日，Andres Freund，一位在 Debian 的不稳定分支上做基准测试的 PostgreSQL 开发者，注意到 SSH 服务器占用了意料之外的处理器时间，"
        "登录大约慢了半秒，还有一个内存检查器在报错。<bookmark mark='b'/>他追查到了那个压缩库，并公开报告了此事。<bookmark mark='c'/>主要发行版的稳定版本还没有发布它。两年耐心的准备，"
        "被半秒钟毁掉了，而发现这半秒的是一位工程师：这是第四章的侧信道，难得一次地为防御方服务。",
    "The defences make each link checkable. <bookmark":
        "这些防御让每一环都可以检查。<bookmark mark='a'/>一次提交由它的哈希命名；构建记录下有签名的来源证明，包括哪份源代码、哪个构建者；制品的哈希被固定在一个锁文件里；部署者检查这两者。<bookmark mark='b'/>SLSA 框架，"
        "起于2021年，给这份证据评级；软件物料清单列出每一个组件，这样当下一个后门被发现时，每个人都能立刻知道自己是否在运行它。<bookmark mark='c'/>而可重现构建，让任何人都能从源代码重新构建并逐字节比较，"
        "下一章就从这里开始。<bookmark mark='d'/>这一切都没有检查源代码是否诚实。那仍然需要人去阅读它。",
    # ------------------------------------------------------------------ s12_trojan
    "Chapter eleven. Reflections on trusting trust.":
        "第十一章：关于对信任的信任的反思。",
    "Ken Thompson's lecture, published in 1984, builds its":
        "肯·汤普森那篇1984年发表的演讲，分三个阶段构建它的攻击，我们会把每一个都搭出来。<bookmark mark='a'/>编译器是一个把源文本变成字节的程序；这里的语言是 Python，二进制文件就是它编译出来的代码，"
        "但别的都无关紧要。<bookmark mark='b'/>login 程序只接受一个密码。<bookmark mark='c'/>编译这个编译器的源代码，你得到一个499字节的编译器二进制文件。<bookmark mark='d'/>用这个二进制文件去编译 login 的源代码，"
        "你得到一个 login 二进制文件。编译器可以编译任何程序，包括它自己的源代码：汤普森所需要的一切。<bookmark mark='e'/>那个被标出来的空槽，只是为了让我们的演示容易看懂。",
    "Stage one is an ordinary backdoor. <bookmark mark='a'/>":
        "第一阶段是一个普通的后门。<bookmark mark='a'/>给 login 加一行：如果密码是一个魔法词，就放他们进去。<bookmark mark='b'/>编译之后，诚实的 login 放行正确的密码，"
        "拒绝其他一切。带后门的那个也放行魔法词，并且仍然拒绝错误的猜测，所以使用它的人什么也察觉不到。<bookmark mark='c'/>但这一行就在 login 的源代码里，任何阅读源代码的人都会看到。"
        "攻击必须离开源代码。",
    "Stage two moves the line out of login and into the":
        "第二阶段把这一行从 login 里移出来，放进编译器。<bookmark mark='a'/>编译器会看它正在编译的是什么。如果它认出了 login，就在编译之前悄悄加上后门。<bookmark mark='b'/>现在 login 的源代码是诚实的，"
        "任何人都可以审计它。<bookmark mark='c'/>但经过这个编译器编译，login 出来的长度是279字节，而不是236字节，里面带着魔法词。<bookmark mark='d'/>我们只是把问题挪了个地方："
        "这个花招现在在编译器的源代码里，而编译器也有读者。",
    "Stage three is the clever one, and it is Part 25's quine.":
        "第三阶段是最巧妙的，它就是第25部分的自打印程序（quine）。<bookmark mark='a'/>教编译器第二个花招：当它编译一个编译器时，把木马本身插进输出里。为此，木马必须知道自己的文本。<bookmark mark='b'/>把它写成一个带一个洞的模板 T，"
        "再把 T 粘贴进它自己的那个洞，形成块 B。<bookmark mark='c'/>在 B 的内部，变量 q 保存着模板。<bookmark mark='d'/>所以把 q 粘贴进 q，就是把 T 粘贴进 T，"
        "<bookmark mark='e'/>也就是 B。木马可以写出一份与自己一模一样的副本，就像自打印程序打印出它自己的源代码一样。<bookmark mark='f'/>而这意味着，编译器的源代码不再需要包含它了。",
    "Now delete every trace of the trojan from the compiler's":
        "现在把木马的每一点痕迹，都从编译器的源代码里删掉。<bookmark mark='a'/>拿起被植入木马的二进制文件，让它去编译那份干净的源代码。<bookmark mark='b'/>它认出这是一个编译器，"
        "并把自己插进去。它产生的二进制文件，有同样的1119字节，和同样的哈希：<bookmark mark='c'/>与我们开始时的那个二进制文件逐位相同。<bookmark mark='d'/>所以这个循环是一个不动点。"
        "你想从干净的源代码重新构建多少次编译器都行，每一代又都是木马。<bookmark mark='e'/>而它们中的每一个，在编译诚实的 login 时，仍然放行魔法词。",
    "That is the whole attack. <bookmark mark='a'/> Search":
        "这就是整个攻击。<bookmark mark='a'/>在每一个源文件里搜索那个魔法密码，你找不到它。<bookmark mark='b'/>然而你所运行的编译器带着木马，你所运行的 login 放行魔法词。"
        "<bookmark mark='c'/>汤普森的寓意很直白：再多的源代码层面的验证或审查，也不能保护你不去使用不可信的代码。<bookmark mark='d'/>他还指出，他本可以挑任何处理程序的程序下手，"
        "汇编器、装入程序，甚至硬件的微码，而且层次越低，这样的错误就越难发现。他把这个想法归功于1970年代空军对 Multics 的一次评审。看起来毫无希望。下一章表明，并非如此。",
    # ------------------------------------------------------------------ s13_ddc
    "Chapter twelve. Catching the trojan.":
        "第十二章：抓住特洛伊木马。",
    "In 2005 David Wheeler published the answer, and in 2009":
        "2005年，David Wheeler 发表了答案，2009年，他的论文证明了它。<bookmark mark='a'/>保留你怀疑的那个二进制文件 A，以及编译器的源代码 c，它你是可以阅读的。<bookmark mark='b'/>再加上第二个编译器 T，"
        "独立写成。它可以很慢，或者很老，或者并不完美；它不需要在一般意义上被信任。<bookmark mark='c'/>我们的是一个参考编译器，它从不检查它所编译的是什么，所以它不可能带有一个能认出编译器的木马。"
        "<bookmark mark='d'/>唯一的假设是，A 和 T 没有以同样的方式被植入木马：木马得同时存在于两者之中。",
    "The procedure has two stages. <bookmark mark='a'/> Stage":
        "这个过程分两个阶段。<bookmark mark='a'/>第一阶段：用那个独立的编译器编译源代码 c，得到一个新的编译器二进制文件 X。它的字节会与 A 的不同，因为不同的编译器写出的代码不同。<bookmark mark='b'/>第二阶段："
        "再编译一次 c，这一次用 X，得到 Z。<bookmark mark='c'/>现在假设 A 确实是由 c 编译出来的。那么 X 和 A 是由同一份源代码构建的，行为相同，所以对相同的输入给出相同的输出："
        "Z 等于 A 作用于 c 的结果。<bookmark mark='d'/>而一个编译器编译它自己的源代码，会复现它自己，所以 A 作用于 c 的结果就是 A。<bookmark mark='e'/>检验就是把 Z 和 A 逐位比较。",
    "First, run it on an honest compiler. <bookmark mark='a'/>":
        "首先，在一个诚实的编译器上运行它。<bookmark mark='a'/>在第一阶段，被怀疑的那个产生499字节，独立的编译器产生498字节，哈希不同。这是预料之中的：两个编译器，是写同一个程序的两种方式。"
        "<bookmark mark='b'/>在第二阶段，这两个二进制文件都去编译同一份源代码，<bookmark mark='c'/>结果逐位相同，并且与 A 相同。<bookmark mark='d'/>结论："
        "A 确实就是它的源代码所说的那样。",
    "Now the binary from the last chapter. <bookmark":
        "现在是上一章的那个二进制文件。<bookmark mark='a'/>第一阶段：被怀疑的那个在编译干净的源代码时，插入它的木马，给出1119字节；独立的编译器给出诚实的498字节。<bookmark mark='b'/>第二阶段："
        "被怀疑的这一系又一次复现出木马，而 X，一个由诚实的编译器构建的诚实的编译器，产生出诚实的二进制文件。<bookmark mark='c'/>它们不同。<bookmark mark='d'/>木马被发现了。"
        "木马可以骗过任意多的阅读，但它不可能存在于一个它从未碰过的编译器里。",
    "Comparing bit for bit assumes a build gives the same bits":
        "逐位比较，是假定一次构建每次给出同样的比特，而真实的构建往往并非如此。<bookmark mark='a'/>我们的玩具构建会把时间和目录戳进它的头部，所以 Alice 和 Bob 构建同一份源代码，"
        "得到不同的哈希，比较就什么也证明不了。<bookmark mark='b'/>把时间和路径固定下来，这两次构建就相同了。<bookmark mark='c'/>自2013年起，Tor 和 Debian 项目带头推动让真实的构建可重现："
        "固定的时间戳，排好序的文件列表，没有构建路径。可重现构建让任何人都能重新构建一个发布版并检查它，这也就检查了发布版是否与公开的源代码一致，而这正是 xz 所利用的那道缺口。",
    "Where does the trusted compiler come from? <bookmark":
        "那个可信的编译器从哪里来？<bookmark mark='a'/>自举项目的回答，是从一颗种子把它长出来：一个只有几百字节的程序，用十六进制写成，小到一个人可以读完。它构建一个很小的汇编器，汇编器构建一个最小的 C 编译器，"
        "然后是一个小的真正的编译器，再然后是一个早期的 GCC，最后是现代的工具链。GNU Guix 在2023年宣布了这样一次全源码自举。<bookmark mark='b'/>然后，多样化双重编译证明一个二进制文件就是它的源代码所说的那样。"
        "它假定第二个编译器没有以同样的方式被植入木马，所以要使用几个不同来源的。<bookmark mark='c'/>而且它无法证明源代码是诚实的：仍然得有人去读它。",
    # ------------------------------------------------------------------ s14_tower
    "Chapter thirteen. The tower, end to end.":
        "第十三章：整座塔，从头到尾。",
    "Follow the Job one last time, from the bottom. <bookmark":
        "最后一次，从最底层开始跟随那项任务。<bookmark mark='a'/>一行 Python 数出30本小说的词，大约2500万字节。在它的下面，是一个由两个开关构成的与非门，然后是一个加法器和一个寄存器，"
        "然后是 Pebble，也就是第6部分的计算机，靠流水线、缓存和多个核心变快。<bookmark mark='b'/>在它上面运行着机器码、一个编译器、一个运行时、一个哈希表，以及带着陷阱和页的 PebbleOS，"
        "一个文件系统和一个数据库。<bookmark mark='c'/>再往上，是数据包和 TCP，Raft 和 MapReduce，以及云上一个集群里的服务，而在最顶端，是那项任务。这当中的每一样，都是在这个系列里，"
        "由它下面的那一层搭起来的，而每一层都相信它下面的那一层会信守承诺。",
    "Now ask each layer what it trusts, and how this series":
        "现在问问每一层，它信任什么，以及这个系列是怎样赢得这份信任的。<bookmark mark='a'/>开关信任物理让它非开即关；香农的代数把开关变成了逻辑，而第5部分的亚稳态显示了它在哪里失效。<bookmark mark='b'/>门信任它们的真值表，"
        "我们对真值表做过穷举检查。<bookmark mark='c'/>算术信任它的加法器，加法器是拿算术本身来检查的。<bookmark mark='d'/>指令集信任门，而门级的机器在随机程序上与模拟器一致。"
        "<bookmark mark='e'/>每一个更快的核心，给出的都是第6部分的答案，而这就是体系结构所承诺的全部。它从未对时间作过任何承诺，而 Spectre 就住在那里。",
    "<bookmark mark='a'/> Machine code trusts that a call":
        "<bookmark mark='a'/>机器码相信一次调用会返回到它来的地方；第2章打破了这一点，而金丝雀、不可执行的内存和随机化的布局为它设防。<bookmark mark='b'/>语言相信编译器会保持含义："
        "我们对自己的编译器做了差分模糊测试，没有发现不一致，用 z3 证明了改写规则，而在这一部分里，还拿一个编译器与一个独立的编译器做了对照检查。<bookmark mark='c'/>算法建立在不变量和证明之上，"
        "然后是测量。<bookmark mark='d'/>内核的隔离，建立在内存单元检查每一次访问之上。<bookmark mark='e'/>而存储承诺，已提交的写入能熬过一次崩溃，我们靠让它崩溃来测试了这一点。",
    "<bookmark mark='a'/> The network promises bytes in order,":
        "<bookmark mark='a'/>网络承诺字节按顺序到达，而 TCP 在丢包和乱序的情况下信守了这个承诺；但是谁发送了这些字节，则需要第30部分的密钥。<bookmark mark='b'/>副本信任 Raft 会达成一致，"
        "我们靠注入故障检查了这一点。<bookmark mark='c'/>服务相信一次重试只会生效一次，幂等键使这一点成真。<bookmark mark='d'/>而位于顶端的应用，自己什么也没有赢得。它继承了它下面的每一条理由，"
        "也继承了每一处泄漏。",
    "Put the reasons side by side, and there are only a few":
        "把这些理由并排放在一起，只有寥寥几种。<bookmark mark='a'/>证明，用于数学和算法。穷举检查，用于门。与独立参考的一致，用于处理器和编译器，这与 Wheeler 的想法相同。注入故障，"
        "用于存储、网络和副本。还有对每一次访问都做检查的硬件。<bookmark mark='b'/>这一部分的那些泄漏，是某一层依赖了一个无人检查过的承诺的地方：内存单元是相互独立的，推测执行不留痕迹，二进制文件与它的源代码相符，"
        "路由通告是诚实的。每一处，都越过了本应把它藏起来的边界。",
    "So here is the tower, lit from end to end. <bookmark":
        "于是，这就是整座塔，从头到尾被点亮。<bookmark mark='a'/>每一层都把它下面的一层藏起来，并信任它。<bookmark mark='b'/>凡是这份信任是靠一个证明、一次检查、一个独立的参考、"
        "一次注入的故障或一把密钥赢得的地方，这一层就守住了。<bookmark mark='c'/>凡是它只是被假定的地方，这一部分就发现了一次攻击。这就是对信任的信任归根结底的含义：不是对任何某一层的信仰，"
        "而是对每一层都有一个理由。",
    # ------------------------------------------------------------------ s15_frontier
    "Chapter fourteen, the frontier. What did this series meet":
        "第十四章，前沿。这个系列遇到了哪些没有人知道答案的问题？",
    "Along the way this series met questions that nobody can":
        "一路上，这个系列遇到了一些没有人能回答的问题。<bookmark mark='a'/>P 是否等于 NP，以及单向函数，连同全部的现代密码学，到底是否存在。矩阵乘法能有多快。第6个忙碌海狸数，现在第5个终于在2024年被证明了。"
        "伸展树是否最优。唯一博弈猜想。随机性到底有没有真正的帮助。为什么我们无法证明任何一个显式的函数需要很多的门。<bookmark mark='b'/>还有实际的问题：C 的内存模型，能做些有用事情的量子计算机，"
        "以及人们实际建造的规模上的经过验证的软件。第61部分会把这每一个都作为研究回过头来讨论。",
    "Three frontiers of trust in particular. <bookmark":
        "尤其是信任方面的三个前沿。<bookmark mark='a'/>大规模的内存安全：重写或加固数十亿行 C 和 C++，内置于硬件的能力，以及关于 Rust 中 unsafe 角落的证明。<bookmark mark='b'/>推测执行："
        "不通过时间泄漏任何东西的处理器，代价是人们能够接受的，以及硬件与软件之间关于什么可以泄漏的精确契约。<bookmark mark='c'/>还有自举：从一个只有几百字节、人可以阅读的种子程序出发，把一整套现代的工具链搭起来，"
        "让汤普森的攻击无处藏身。<bookmark mark='d'/>每一个，都把一个非正式的承诺，也就是一层会把它下面的东西隐藏起来，变成可以检查的东西。",
    "Open problems. <bookmark mark='a'/> Whether one-way":
        "开放问题。<bookmark mark='a'/>单向函数是否存在，这是第29和30部分全部内容所依赖的假设。<bookmark mark='b'/>一个可以证明没有瞬态执行泄漏、而且代价很低的处理器。"
        "<bookmark mark='c'/>把 C 可信地自动翻译成一门内存安全的语言。<bookmark mark='d'/>以及弄清我们所运行的软件里面有什么，以及谁能改动它。<bookmark mark='e'/>这一部分的研究题，"
        "把最后几章连在了一起：一整套软件栈，从一颗小到可以审计的种子出发搭起来，每一步都可重现，每一次翻译都经过正确性证明，这样信任它就不再意味着信任任何人。",
    # ------------------------------------------------------------------ s16_outro
    "Part 1 began with two piles of pebbles and one rule: if":
        "第1部分从两堆石子和一条规则开始：如果两堆不同，就从大的那堆里拿走和小的那堆一样多的石子，两堆相等时停下。<bookmark mark='a'/>24和18变成了6和6，而6就是最大公约数，是由一个对数字一无所知的人找到的。"
        "<bookmark mark='b'/>那条规则就是一个算法，而希尔伯特的问题，是否每一个这样的问题都能由一条规则来解决，引出了图灵的机器，图灵的机器又引出了这个系列所搭建的一切。",
    "Ten acts built one tower. <bookmark mark='a'/> Gates and":
        "十幕搭起了一座塔。<bookmark mark='a'/>门电路、算术和存储变成了一台计算机，流水线和缓存让它变快。语言和编译器让我们能与它对话；算法告诉它该做什么；而计算的极限和秘密的数学，告诉我们它永远做不到什么，"
        "以及它能把什么藏起来。<bookmark mark='b'/>内核让一台机器运行许多程序；网络和共识把许多机器连起来；工程、服务和云让人们能够在这些之上大规模地搭建；而最后一幕向外看去，看向像素、数值、"
        "量子机器、证明，以及信任。<bookmark mark='c'/>每一层都建立在它下面的一层之上，而其中的每一层都是在这里搭起来的，除了下面的那一层，别无所依。",
    'f"And the Job, counting the words of thirty':
        "而那项任务，数出三十本小说里的词，一路上都在记着它的账本。<bookmark mark='a'/>第6部分的单周期 Pebble 用了{first['seconds']:.0f}秒；第15部分的λ演算机器用了好几个小时；"
        "缓存、核心、编译器、算法、网络和服务，让那根柱条沿着坐标轴来回移动。<bookmark mark='b'/>第20行是其中最朴素的：在这台机器上的一行 Python，大约{last['seconds']:.1f}秒。"
        "这个系列的每一层都在这一行里面，这正是搭建这座塔的意义：这样你需要写的，就只有这一行。",
    "Six problems, with full solutions in the part's notes.":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：在我们的编译器里藏一个不同的木马，并表明多样化双重编译依然能抓住它。最后一道标有星号，是研究题：一整套软件栈，从一颗小到可以阅读的种子长出来，"
        "每一步都经过证明。",
    "This is where the degree ends. The final reading list is":
        "学位课程到这里结束。最后的阅读书单在屏幕上和笔记里：这整个系列所倚重的书，以及这一部分背后的论文。第十一幕继续走向研究前沿，共六个部分，水平相当于博士第一年，写给任何想继续攀登的人。谢谢你和我一起把它搭起来。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
