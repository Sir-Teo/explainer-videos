"""Chinese narration for cs44: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第44部分：人与产品"

CHAPTERS = {
    "Hook": "演示之母",
    "Fitts": "1. 指点是一条信道",
    "Choice": "2. 选择，以及预测一项任务的用时",
    "Perception": "3. 感知及其阈值",
    "Colour": "4. 颜色",
    "Text": "5. 屏幕上的文字",
    "Access": "6. 无障碍",
    "Usability": "7. 评估可用性",
    "Abtest": "8. A/B 测试",
    "Peeking": "9. 看得太勤",
    "Cuped": "10. 更少的噪声，同样的真相",
    "Pitfalls": "11. 大规模下的陷阱",
    "Bandits": "12. 老虎机与指标",
    "Frontier": "13. 前沿：小心地测量人",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "On the ninth of December 1968, in San Francisco, Douglas":
        "1968年12月9日，在旧金山，Douglas Engelbart 坐在一个舞台上，面前是一块屏幕、一个键盘，还有一个底下装着轮子的小木盒。<bookmark mark='a'/>在九十分钟里，"
        "他向一千名工程师展示了计算机能为一个人做些什么。屏幕上有一个指针，跟着他的手移动，靠的就是他的实验室发明的那个盒子：鼠标。<bookmark mark='b'/>文字链接到别的文字，点击一处就打开另一处：超文本。"
        "<bookmark mark='c'/>一位远在三十英里外的同事，同时编辑着同一份文档，<bookmark mark='d'/>他的脸出现在屏幕上的一个窗口里。"
        "<bookmark mark='e'/>这是一个完整可用的系统，叫作 NLS，出自 Engelbart 在斯坦福研究所的实验室。后来，人们称它为“演示之母”。",
    "The ideas took fifteen years to reach ordinary desks.":
        "这些想法花了十五年，才走上普通人的办公桌。<bookmark mark='a'/>在施乐帕洛阿尔托研究中心（Xerox PARC），1973年的 Alto 把窗口、图标和鼠标放到了一台个人计算机上。1979年，"
        "乔布斯（Steve Jobs）前去参观，随后在1984年有了 Macintosh，一年之后有了 Windows。万维网在1991年到来，多点触控手机在2007年到来。"
        "<bookmark mark='b'/>每一步都是一场关于人的争论：人能看到什么、够到什么、记住什么、决定什么，以及有多快。这一部分把这些争论当作科学来对待。",
    'f"Two kinds of measurement run through this part.':
        "贯穿这一部分的有两种测量。<bookmark mark='a'/>第一种测量的是人。指向一个目标所用的时间，随它的距离与宽度之比的对数增长，精确到所有的点都落在一条直线上。这就是 Fitts 定律，它来自香农的信道容量。"
        "<bookmark mark='b'/>第二种测量的是产品：用真实用户比较两个版本的对照实验。它们有自己的陷阱。这里，我们比较两个完全相同的版本，一个月里每天检查一次；"
        "这样的实验中有{100 * pk['fpr_peeking'][-1]:.0f}%宣布了一个其实并不存在的赢家，而检验承诺的只有5%。",
    "This is Part 44 of Computer Science, Built, the last part of":
        "这是计算机科学，从零搭建，第44部分，也是第八幕的最后一部分。<bookmark mark='a'/>我们将从信道容量推导出 Fitts 定律，从熵推导出 Hick 定律；在任何人动手之前，预测一项任务要花多长时间；"
        "把颜色变成公式，并为色盲观众检查这个系列自己的调色板；然后在产品上做实验，推导它们的统计功效，看清为什么每天早上查看结果会破坏实验，以及怎样安全地查看。",
    # ------------------------------------------------------------------ s02_fitts
    "Chapter one. Pointing is a channel.":
        "第一章：指点是一条信道。",
    "In 1954 the psychologist Paul Fitts asked people to tap a":
        "1954年，心理学家 Paul Fitts 让人们拿着一支金属触笔，在两块金属板之间来回敲击，在不失手的前提下越快越好。<bookmark mark='a'/>每块板有一个宽度，两块板之间隔着一段距离。"
        "<bookmark mark='b'/>把两块板移得更远，或者把它们做得更窄，敲击就会变慢。距离加倍的代价，大约和宽度减半相同：只有距离与宽度之比才要紧，而时间随这个比值的对数增长。他当时正在读香农，"
        "于是把论文题为《人类运动系统的信息容量》。",
    "Fitts's analogy was Shannon's channel capacity from Part 28.":
        "Fitts 的类比，是第28部分讲过的香农信道容量。<bookmark mark='a'/>一条信道以比特计的容量，随一加信噪比的对数增长。<bookmark mark='b'/>在指点中，距离扮演信号，"
        "宽度扮演这次运动所能容忍的噪声。难度指数，即距离除以宽度再加一的对数，数的是一次运动必须传递的比特数。这是 Scott MacKenzie 在1992年给出的形式；它永远不会是负数，"
        "而且比 Fitts 的原始形式拟合得更好。<bookmark mark='c'/>于是，运动时间等于一个常数，用于启动和停止，再加上斜率乘以比特数。斜率的单位是秒每比特，它的倒数是一个吞吐量：一只手的带宽。",
    'f"Why a logarithm? David Meyer and colleagues, in':
        "为什么是对数？David Meyer 和同事们在1988年给出了一个答案。<bookmark mark='a'/>一次运动是一连串子运动。每一次都瞄准目标的中心，落点的误差与它走过的距离成正比；如果没打中，就再来一次。"
        "<bookmark mark='b'/>所以每次修正，都把剩余的距离缩小一个大致固定的倍数，修正的次数就随距离与宽度之比的对数增长。<bookmark mark='c'/>我们在二十个目标上模拟了这只手，有近有远，"
        "有宽有窄。<bookmark mark='d'/>这些点落在一条直线上，R 平方为{f['r2']:.2f}。斜率是每比特{f['b']:.3f}秒：我们这只模拟的手，"
        "吞吐量是每秒{f['throughput_bits_per_s']:.1f}比特。据 Soukoreff 和 MacKenzie 2004年的研究，人们用鼠标测得的吞吐量是每秒几比特。",
    'f"Designers exploit a loophole.':
        "设计师会利用一个漏洞。<bookmark mark='a'/>指针不能离开屏幕。瞄准屏幕边缘上的目标，就不可能冲过头：指针会停在那里，就好像目标无限深。<bookmark mark='b'/>在我们的模拟中，"
        "同一个目标放在中间要{e['normal']:.2f}秒，放在边缘只要{e['edge']:.2f}秒：手可以一甩而过，不必修正。"
        "<bookmark mark='c'/>这就是为什么1984年的 Macintosh 把唯一的菜单栏放在屏幕的最顶端，也是为什么角落，相当于两重边缘，是所有地方中最快能到达的。",
    "Some movements must stay inside a path. <bookmark mark='a'/>":
        "有些运动必须保持在一条路径之内。<bookmark mark='a'/>要到达一个子菜单，指针得沿着父菜单项移动，如果途中滑了出去，子菜单就会关闭。"
        "<bookmark mark='b'/>Johnny Accot 和 Shumin Zhai 在1997年证明，穿过一条隧道所需的时间，与它的长度除以宽度成正比，并沿着路径累加。这是线性的，不是对数的，"
        "所以隧道的代价比目标大得多。<bookmark mark='c'/>嵌套菜单就是串联起来的隧道。补救办法是：更宽的菜单项、更浅的菜单，以及能容忍指针斜着朝它们移动的子菜单。",
    # ------------------------------------------------------------------ s03_choice
    "Chapter two. Choosing, and predicting how long a task will":
        "第二章：选择，以及预测一项任务的用时。",
    "In 1952 William Hick lit one of several lamps and timed how":
        "1952年，William Hick 点亮若干盏灯中的一盏，测量人们按下灯下方的按键要用多长时间。反应时间随灯的数目加一的对数增长，那个“一”算的是一盏灯都不亮的可能。"
        "<bookmark mark='a'/>这里有一个选择者，每做一次比较，就把候选项减半，也就是第16部分的二分查找。七盏灯，加上一盏都不亮的可能，一共八种可能，三次比较就能找到其中任意一种。"
        "<bookmark mark='b'/>我们模拟了这个选择者，启动要五分之一秒，每次比较大约0.15秒，灯从一盏到十盏。时间对比特数是一条直线，R 平方为0.999：每一比特的不确定性，代价都一样。",
    'f"A year later Ray Hyman made the choices unequally':
        "一年之后，Ray Hyman 让各个选项出现的可能性不再相等，结果反应时间跟随的是这次选择的熵，而不是选项的个数。<bookmark mark='a'/>拿一个菜单来说，它的第一项有70%的时候被选中。"
        "它的熵是{sk['H']:.2f}比特，而五个等可能的选项是{sk['uniform_H']:.2f}比特。<bookmark mark='b'/>提是非题的最佳方式，是从最可能的那一项问起："
        "一个问题就解决了70%的情况，再用三个问题解决其余的，<bookmark mark='c'/>平均{sk['questions']:.1f}个问题。这正是《人工智能，从零搭建》第1部分的哈夫曼编码，它永远不会比熵更短。"
        "设计准则随之而来：把最可能的选项放在最前面，或者把它设为默认。",
    "Hick's law is often stretched too far. <bookmark mark='a'/>":
        "Hick 定律常常被引申得太远。<bookmark mark='a'/>它描述的是：当你已经知道有哪些选项时，必须在其中做出的决定。<bookmark mark='b'/>逐项阅读一个不熟悉的菜单，是一种搜索，"
        "搜索时间随项数增长，而不是随它的对数增长。<bookmark mark='c'/>而且，练习会让斜率变平：一个知道每样东西在哪里的专家，根本不再选择，而是直接指过去。",
    "Stuart Card, Thomas Moran and Allen Newell turned these laws":
        "Stuart Card、Thomas Moran 和 Allen Newell 把这些定律变成了一种工程工具。<bookmark mark='a'/>他们的 GOMS 分析把一项任务描述为：一个目标，比如删除一个文件；"
        "<bookmark mark='b'/>实现目标的方法，每种方法是一串基本操作符：伸手去拿鼠标、指向、点击、按一个键；<bookmark mark='c'/>以及在方法之间做选择的选择规则。给每个操作符一个时间，"
        "你就能在任何人把它造出来之前，预测一项任务要花多长时间。",
    'f"The keystroke-level model, which Card, Moran and':
        "击键层次模型（keystroke-level model）由 Card、Moran 和 Newell 在1980年发表，是最简单的版本；按下按钮这一项，是 David Kieras 后来在指南里加上的。"
        "<bookmark mark='a'/>对一个普通打字者来说，一次击键要0.28秒，用鼠标指向要1.1秒，按一下按钮要十分之一秒，把手在键盘和鼠标之间移动要0.4秒，片刻的心理准备要1.35秒。"
        "<bookmark mark='b'/>把每种方法写成一串操作符，再把它们加起来。通过菜单删除一个文件：{cases['delete a file: menu']['seconds']:.1f}秒。用快捷键："
        "{cases['delete a file: keyboard shortcut']['seconds']:.2f}秒。<bookmark mark='c'/>通过对话框重命名："
        "{cases['rename: dialog']['seconds']:.2f}秒；在原处直接重命名：{cases['rename: inline (F2)']['seconds']:.2f}秒。"
        "<bookmark mark='d'/>黄色的方块是思考的时刻，它们占了大头。更快的设计，通常是要求更少决定的设计，而不是要求更少按键的设计。",
    # ------------------------------------------------------------------ s04_perception
    "Chapter three. Perception and its thresholds.":
        "第三章：感知及其阈值。",
    "The first thresholds are in time. In 1968 Robert Miller, at":
        "第一类阈值在时间上。1968年，IBM 的 Robert Miller 问：计算机必须多快地回应一个人？此后，这个答案被一再重述：1991年由 Card、Robertson 和 Mackinlay，"
        "1993年由 Jakob Nielsen。<bookmark mark='a'/>不到十分之一秒，响应感觉是瞬时的：结果本身就是所需的全部反馈。<bookmark mark='b'/>不到一秒，延迟会被察觉，"
        "但用户的思路不会被打断。<bookmark mark='c'/>不到十秒，注意力还能维持，前提是界面表明工作正在进行。<bookmark mark='d'/>超过这个时间，人们就会转身离开：要显示真实的进度，"
        "并让他们去做别的事。",
    "Direct manipulation is stricter than a tenth of a second.":
        "直接操纵的要求，比十分之一秒还要严格。<bookmark mark='a'/>当你在手指下拖动某样东西时，任何延迟都会表现为手指和那样东西之间的一道缝隙。2012年，"
        "微软研究院的 Albert Ng 和同事们造了一块几乎没有延迟的触摸屏，发现人们在上面拖动时，能察觉到只有几毫秒的延迟。<bookmark mark='b'/>每一次输入都要走过一条流水线："
        "传感器、操作系统、应用程序、渲染、合成和显示器。每个要等待下一帧的阶段，都可能多出整整一帧，在60赫兹下是16.7毫秒，也就是第42部分的帧预算。延迟会累加，所以每个阶段都必须做预算。",
    "The second kind of threshold is in size. <bookmark":
        "第二类阈值在大小上。<bookmark mark='a'/>两根短条相差十分之一个单位，这个差别很容易看出来。<bookmark mark='b'/>把同样的十分之一加到一根长条上，它几乎就消失了。"
        "<bookmark mark='c'/>要同样明显，差别就必须随着条的长度一起增长。<bookmark mark='d'/>韦伯（Ernst Weber）在19世纪30年代发现了这一点：最小可觉差是刺激的一个固定比例，"
        "这个比例因感官而异。<bookmark mark='e'/>1860年，费希纳（Gustav Fechner）数了这些台阶，得出结论：感觉随刺激的对数增长。这就是为什么响度用分贝来度量，也是为什么，正如下一章会展示的，"
        "屏幕会把更多的编码花在暗色调上。",
    "Some differences need no search at all. <bookmark mark='a'/>":
        "有些差别根本不需要搜索。<bookmark mark='a'/>一群蓝色标记里的一个红色标记，一眼就能看到，不管蓝色的有多少个。<bookmark mark='b'/>一群竖直线条里的一条倾斜线条也是这样。"
        "颜色、大小、朝向和运动，在注意力到来之前，就已经在整个视野里被并行处理了。<bookmark mark='c'/>但是，请在这里找出那条红色的倾斜线条，它混在红色的竖直线条和蓝色的倾斜线条之中。"
        "每种特征单独来看都到处都是，眼睛只好一个一个地检查这些标记。<bookmark mark='d'/>Anne Treisman 和 Garry Gelade 在1980年把这一点发展成了特征整合理论。对界面来说："
        "用单独一种特征，标出那件唯一要紧的东西。",
    "<bookmark mark='a'/> Watch these six numbers while the":
        "<bookmark mark='a'/>在屏幕闪烁的时候，盯着这六个数字。每闪一次，其中一个就会变。1997年，Ronald Rensink、Kevin O'Regan 和 James Clark 证明，"
        "当两幅画面之间隔着一个短暂的空白时，即使很大的变化，也会在好几秒内不被察觉。<bookmark mark='b'/>在这里，错误从17变成了71。一个重新加载的页面，或者一个在滚动时更新的数值，恰恰就是这样一个空白。"
        "<bookmark mark='c'/>所以，界面应该把目光引向变化了的地方：给它加上动画，或者短暂地高亮它。",
    # ------------------------------------------------------------------ s05_colour
    "Chapter four. Colour.":
        "第四章：颜色。",
    "Light is a spectrum, energy spread across wavelengths.":
        "光是一种光谱，是分布在各个波长上的能量。<bookmark mark='a'/>眼睛用三种视锥细胞来测量它，它们分别对短、中、长波长敏感。<bookmark mark='b'/>无论光谱是什么样子，都被归结为三个响应。"
        "<bookmark mark='c'/>两个光谱只要三个响应相同，看起来就一模一样：这叫同色异谱（metamer），也是为什么三种原色就能模仿我们看到的大多数颜色。<bookmark mark='d'/>1931年，"
        "CIE 根据配色实验确定了一个标准观察者，也就是 XYZ 空间。sRGB 标准由 HP 和微软在1996年制定，它在 XYZ 中定义了三种原色和一个白点，几乎每块屏幕、每个网页都默认采用它。",
    'f"An sRGB pixel stores code values from 0 to 255,':
        "一个 sRGB 像素存储的是从0到255的编码值，而它们并不是光的量。<bookmark mark='a'/>传递曲线接近2.4次幂，把编码映射成光。<bookmark mark='b'/>编码128，"
        "也就是范围的正中间，发出的光只有白色的{100 * gm['code_128_light']:.1f}%。<bookmark mark='c'/>白色一半的光，是这个浅得多的灰色，b c b c b c。"
        "<bookmark mark='d'/>这条曲线之所以存在，是因为韦伯和费希纳：编码上相等的步长，大致就是感知明度上相等的步长，所以编码被花在了眼睛能分辨的地方。代价是，混合、缩放和光照都必须先转换到线性光，"
        "这是第51部分的一个主题。",
    "Code values say nothing about how different two colours":
        "编码值并不能说明两种颜色看起来差多少。<bookmark mark='a'/>屏幕能显示的每一种颜色，都位于这个由红、绿、蓝构成的立方体里。<bookmark mark='b'/>感知空间把这个立方体弯折变形，"
        "让距离代表差异。CIELAB 来自1976年，给出明度和两条对立轴：从绿到红，从蓝到黄。<bookmark mark='c'/>OKLab 由 Björn Ottosson 在2020年发表，经过重新拟合，"
        "使相等的距离看起来更接近相等，并且颜色变亮时色相保持不变。这里是这个系列自己的调色板在其中的位置，还有立方体的红色顶点。<bookmark mark='d'/>我们的转换通过了检验：白色在 CIELAB 中明度为100，"
        "在 OKLab 中为1，sRGB 的红色落在公布的数值上。",
    'f"About eight percent of men of European ancestry,':
        "在欧洲血统的男性中，大约8%有色觉缺陷，女性中约0.5%，大多是红绿方面的；这些是近似的公开数据。<bookmark mark='a'/>这是这个系列的调色板，在典型视觉下的样子。"
        "<bookmark mark='b'/>它下面，是同样六种颜色，针对三种视锥细胞缺失的情况所做的模拟，用的是 Machado、Oliveira 和 Fernandes 2009年的模型。"
        "<bookmark mark='c'/>对每一种视觉，找出 OKLab 中最接近的一对颜色。<bookmark mark='d'/>诚实的发现关乎我们自己。在绿色盲（deuteranopia）下，"
        "这个系列用来表示“假”的红色，和用来表示内核的橙色，相距只有{pairs['deuteranopia']['closest'][0][2]:.3f}：几乎是同一种颜色。在这些视频里，红色意味着错误，"
        "所以红色永远不能是唯一的信号。",
    'f"Colour also decides whether text can be read.':
        "颜色还决定了文字能不能读清楚。<bookmark mark='a'/>《Web 内容无障碍指南》（WCAG）里的对比度，比较的是两个相对亮度，它们在线性光中计算，各自再加上一个代表眩光的小常数。"
        "<bookmark mark='b'/>我们调色板里的每种颜色，在深色背景上都超过了4.5，这是普通文字所要求的水平；其中有{n7}种还超过了7。<bookmark mark='c'/>不过，光有对比度还不够。"
        "一张只用红色和橙色来区分两个数据系列的图表，<bookmark mark='d'/>在绿色盲下就变成了一个系列。<bookmark mark='e'/>再给每个系列配上一个形状和一个直接标注，这张图表就经受住了考验。"
        "教训是：永远不要只用颜色；还要加上形状、位置或标注。",
    # ------------------------------------------------------------------ s06_text
    "Chapter five. Text on screens.":
        "第五章：屏幕上的文字。",
    "A letter on a screen begins as a shape, not as pixels.":
        "屏幕上的一个字母，起初是一个形状，而不是像素。<bookmark mark='a'/>字体把每个字形存储为一个轮廓：由贝塞尔（Bézier）曲线构成的闭合路径，由曲线上的锚点固定，又被拉向曲线外的控制点。"
        "<bookmark mark='b'/>TrueType 由 Apple 在1991年发布，用的是二次曲线；PostScript 字体用的是三次曲线。无论哪种，一个轮廓都适用于所有字号。"
        "<bookmark mark='c'/>要画出它，就把像素网格叠在轮廓上，问每个像素的中心是否在里面：从中心发出一条射线，数它穿过轮廓多少次，用的是第22部分的方向测试。奇数次就意味着在里面。"
        "第51部分会用同样的方法光栅化三角形。",
    'f"Here is the word Job, drawn by FreeType, the':
        "这是单词 Job，由开源光栅化器 FreeType 以四种字号画出来。<bookmark mark='a'/>每个像素只用一位时，像素要么亮，要么灭。在{sizes[0]}像素的字号下，"
        "整个单词只分到{lo['w']}乘{lo['h']}个像素，曲线变成了阶梯。<bookmark mark='b'/>抗锯齿让一个像素可以部分点亮：它的灰度，就是轮廓覆盖它的比例，所以一条落在像素三分之一处的边缘，"
        "依然能显示出它的位置。<bookmark mark='c'/>小号的单词用了{lo['grey_levels']}级灰度，大号的用了{hi['grey_levels']}级。在8像素时，一笔大约只有一个像素宽，"
        "它落在哪里就很要紧了。",
    # ------------------------------------------------------------------ s06_text
    "Coverage alone does not make small text sharp. <bookmark":
        "仅有覆盖率，并不能让小字变得清晰。<bookmark mark='a'/>这里有三根完全相同的竖笔，就像字母 m 的几条腿，每根宽1.4个像素。一根变成横跨两个像素的灰色污迹，一根一侧是实心的，一根铺开到三个像素上。"
        "相等的笔画，看起来并不相等。<bookmark mark='b'/>字体微调（hinting）解决了这个问题。一个 TrueType 字体里带着一些小程序，也就是光栅化器内部一台栈式机器的字节码，"
        "它们在每个字号下把轮廓的点移到像素边界上，于是每根竖笔都恰好是清晰的一个像素宽。<bookmark mark='c'/>这在8到12像素时最要紧，那时一笔就只有一个像素；在高密度的屏幕上，就没那么要紧了。",
    "A liquid-crystal pixel is really three stripes: red, green":
        "液晶屏的一个像素，其实是三条条纹：红、绿、蓝。<bookmark mark='a'/>把像素当作一个整体，一根从三分之一处开始的竖笔，就会变成两个暗淡的灰色。<bookmark mark='b'/>把条纹一条一条地点亮，"
        "边缘就能定位到三分之一个像素：水平分辨率变成了三倍。<bookmark mark='c'/>微软在 Windows XP 中以 ClearType 的名字推出了这项技术，并配有一个滤波器，把每条边缘分散到相邻的条纹上，"
        "以掩盖彩色的镶边。<bookmark mark='d'/>它需要知道条纹的排列顺序，所以把平板电脑转个方向，它就失效了；等到屏幕足够密，苹果在2018年的 macOS 中把它关掉了。",
    "<bookmark mark='a'/> A very long line sends the eye a long":
        "<bookmark mark='a'/>一行太长，眼睛就要走很远，才能回到下一行的开头，而且很容易落到错误的一行上。"
        "<bookmark mark='b'/>Robert Bringhurst 的《印刷风格要素》（The Elements of Typographic Style）认为，舒适的一行是45到75个字符；"
        "Web 内容无障碍指南（WCAG）在最严格的级别上，要求最多80个字符，行距至少1.5倍。<bookmark mark='c'/>同样字号的字体，看起来可能差别很大，因为 x 字高，也就是小写字母的高度，各不相同；"
        "为屏幕设计的 Verdana 和 Georgia，x 字高都很大。<bookmark mark='d'/>文字还需要对比度：第42部分推导出了这个比值，正文需要4.5比1。",
    # ------------------------------------------------------------------ s07_access
    "Chapter six. Accessibility.": "第六章：无障碍。",
    "Accessibility is design for people whose bodies or minds":
        "无障碍，是为身体或心智与设计者不同的人所做的设计。<bookmark mark='a'/>世界卫生组织估计，大约13亿人，也就是世界人口的16%，身有严重的残疾。"
        "<bookmark mark='b'/>而这条界线是模糊的。微软的包容性设计工具包画出了一个谱系：一个只有一只手臂的人、一个手臂骨折的人，和一个抱着婴儿的家长，都需要一部能单手操作的手机。失明、白内障，"
        "和司机盯着路面的眼睛，也是如此；耳聋、耳部感染，和一间嘈杂的酒吧，也是如此。<bookmark mark='c'/>残疾是人与设计之间的不匹配，而随着年龄增长，几乎每个人都会遇到一次。",
    "Each kind of assistive technology asks something different":
        "每一类辅助技术，对软件的要求都不一样。<bookmark mark='a'/>屏幕阅读器朗读的，是第42部分从页面构建出的无障碍树：这是一个按钮，名字叫 Buy。"
        "<bookmark mark='b'/>有的人只能按一两个开关，用手、用脚，或者用一口气，他们让一个高亮框在各个控件之间逐个移动，所以每个操作都必须能按这个顺序到达。"
        "<bookmark mark='c'/>放大器把屏幕放大；指南要求文字能放大到两倍，并且页面在320像素宽时仍然可用。<bookmark mark='d'/>语音控制按名字来操作：说“点击 Buy”，"
        "它就必须找到一个控件，其无障碍名称包含那个看得见的词。",
    "f\"Chapter one's law has an accessibility reading.":
        "第一章的定律，也可以从无障碍的角度来读。<bookmark mark='a'/>在给定的距离下，目标越宽，就越快点中。用第一章拟合的结果，一个480像素外、16像素宽的目标，大约需要{rows[0][2]}毫秒，"
        "一个44像素宽的目标需要{rows[2][2]}毫秒。<bookmark mark='b'/>对于手部震颤、落点很分散的人来说，这个差别决定了目标到底能不能点中。"
        "WCAG 2.2 规定的最小尺寸是24乘24个 CSS 像素，或者在较小的目标周围留出足够的空间。<bookmark mark='c'/>而且，任何靠拖动完成的操作，也必须能用一次点按完成，所有的操作都必须能用键盘完成。",
    "Some disabilities affect memory, attention or reading.":
        "有些残疾影响记忆、注意力或阅读。<bookmark mark='a'/>对他们，以及对每一个疲惫或匆忙的人来说，规则主要是克制：浅白的用词，简短的句子，以及在每个页面上都保持不变的导航，这样就不必重新学习任何东西。"
        "<bookmark mark='b'/>时间限制应当带有提醒，并提供延长的办法，否则就不该存在。<bookmark mark='c'/>WCAG 2.2 新增规定，登录不能依赖记忆或解谜：要让密码管理器能填写输入框，"
        "也要允许人们粘贴。<bookmark mark='d'/>视频还需要字幕，包括那些重要的声音，这既是为了失聪的观众，也是为了每一个在火车上关掉声音观看的人。",
    "Designing for the edges usually helps the middle. <bookmark":
        "为边缘人群做的设计，通常也会帮到中间的人。<bookmark mark='a'/>路缘坡道是轮椅使用者争取来的；如今每个推婴儿车、拉行李箱或骑自行车的人都在用它，这种模式被称为路缘坡道效应。字幕是为失聪观众做的，"
        "却在每一个嘈杂的房间里被人阅读。<bookmark mark='b'/>建筑师 Ronald Mace 把这称为通用设计：一种设计，面向尽可能广泛的人群，而不是事后再加一个特殊版本。"
        "<bookmark mark='c'/>Web 的指南建立在四条原则之上。内容必须可感知、可操作、可理解，并且足够健壮，能与辅助技术配合工作。<bookmark mark='d'/>对比度属于第一条；第42部分推导了它，"
        "第四章检查了这个系列的配色。",
    # ------------------------------------------------------------------ s08_usability
    "Chapter seven. Evaluating usability.": "第七章：评估可用性。",
    "How do you find out what is wrong with a design before your":
        "怎样才能赶在用户之前，发现一个设计的毛病？最便宜的办法是检查它。<bookmark mark='a'/>1994年，Jakob Nielsen 从数百个可用性问题中提炼出十条经验法则：让人们看到系统在做什么，"
        "说他们的语言，让他们能撤销，保持一致，预防错误，让选项看得见，而不是靠记忆，等等。<bookmark mark='b'/>在启发式评估中，几位评估者各自独立地对照这份清单检查设计，然后汇总他们的发现。"
        "<bookmark mark='c'/>它又快又便宜。但它找到的是专家预料到的问题，而真实的人会发现别的问题。",
    "To find what real people stumble on, watch them. <bookmark":
        "要找到真实的人会在哪里绊倒，就去观察他们。<bookmark mark='a'/>在出声思维研究中，参与者拿到真实的任务，比如给朋友买一张票，并被要求一边做，一边说出自己在想什么。"
        "<bookmark mark='b'/>每一次犹豫、每一个错误的猜测、每一次退回，都标出一个问题，而他们说的话解释了原因：这个人不知道该在哪里说明，这张票是给别人的。"
        "<bookmark mark='c'/>主持人保持安静，从不帮忙。Clayton Lewis 在1982年，把这种方法从言语报告的心理学引入了 IBM 的界面设计。规则是：观察人们做什么，而不是问他们会做什么。",
    'f"How many participants are enough? Jakob Nielsen':
        "需要多少名参与者才够？Jakob Nielsen 和 Thomas Landauer 在1993年用一个模型给出了回答。<bookmark mark='a'/>假设每个用户独立地以同样的概率 L 遇到每一个问题。"
        "在他们研究的那些项目上取平均，L 约为{L:.2f}。<bookmark mark='b'/>一个用户错过某个问题的概率，是1减 L。n 个用户全都错过它的概率，是1减 L 的 n 次方，因为相互独立的概率相乘，"
        "就像第2部分那样。<bookmark mark='c'/>所以，被发现的问题所占的比例，是1减去这个值。<bookmark mark='d'/>一个用户能发现{100 * vals[0]:.0f}%，"
        "两个发现{100 * vals[1]:.0f}%，三个{100 * vals[2]:.0f}%，四个{100 * vals[3]:.0f}%，五个{100 * vals[4]:.0f}%：这就是那个著名的说法，"
        "五个用户就能发现大部分问题。",
    'f"The model assumed every problem is equally easy to':
        "这个模型假设每个问题都同样容易被发现。真实的问题并非如此。<bookmark mark='a'/>这是每个问题都以相同概率被发现时的曲线。<bookmark mark='b'/>现在让可见度变化："
        "少数问题几乎人人都会碰到，许多问题只有少数人碰到。我们从一个平均值同样是0.31的 Beta 分布中，抽取每个问题的概率。在五个用户时，被发现的比例从{100 * u5:.0f}%降到了{100 * v5:.0f}%。"
        "<bookmark mark='c'/>现在要发现{100 * u5:.0f}%，需要{n_match}个用户，因为很少有人碰到的那些问题，恰恰是最久才会被看见的，而平均值把它们掩盖了。",
    "So the five-user rule needs care. <bookmark mark='a'/> L is":
        "所以，五用户法则需要谨慎对待。<bookmark mark='a'/>L 是对许多项目取的平均，它随产品、任务和人群而变化。<bookmark mark='b'/>一个二十个用户里只有一个会碰到的问题，"
        "五个用户能发现它的概率不到四分之一，无论它有多严重；这就是为什么罕见但代价高昂的故障，还需要别的方法：日志、客服电话，以及下一章的实验。<bookmark mark='c'/>这条曲线真正支持的，是迭代。"
        "一轮15个用户几乎能找出今天这个设计中的所有问题，但其中大部分是前5个用户找到的；把这些修好，接下来的5个用户就会发现那些被旧问题掩盖住的问题。Nielsen 自己的建议是三轮，每轮五人。",
    # ------------------------------------------------------------------ s09_abtest
    "Chapter eight. The A/B test.": "第八章：A/B 测试。",
    "Where intuition runs out, run an experiment. <bookmark":
        "直觉用尽的地方，就做实验。<bookmark mark='a'/>每个到来的用户，都由抛硬币来分配：正面，看现在的页面；反面，看新的页面。<bookmark mark='b'/>因为做决定的是硬币，而不是人，"
        "两组之间只有偶然的差别，在每一项特征上都是如此，甚至包括没人测量过的特征，比如其中有多少是回头客。<bookmark mark='c'/>组足够大时，第20部分讲的集中现象，会让它们的平均值几乎相等。所以，"
        "如果两组之后的表现不同，原因要么是这项改动，要么是偶然。这就是罗纳德·费希尔（Ronald Fisher）的随机化实验，而统计检验衡量的，正是这个偶然。",
    "f\"Here is the standard test. <bookmark mark='a'/>":
        "这是标准的检验。<bookmark mark='a'/>每一组都有一部分用户发生转化，观察到的差异，是 B 的转化率减去 A 的转化率。<bookmark mark='b'/>假设这项改动毫无作用："
        "那么两组共享同一个转化率，把两组合并起来就能估计它。<bookmark mark='c'/>一个比率的方差，是 p 乘以1减 p，再除以 n，而两组的方差相加。"
        "<bookmark mark='d'/>用差异除以由此得到的标准误。样本很大时，z 近似服从标准正态分布，而 p 值就是在什么都没变的情况下，z 离零这么远的概率。<bookmark mark='e'/>各一万名用户中，"
        "500次转化对560次，是12%的提升，但 z 只有{z:.2f}，p 值是{pv:.3f}：在5%的水平上并不显著。",
    "A test can be wrong in two ways. <bookmark mark='a'/> If the":
        "检验可能以两种方式出错。<bookmark mark='a'/>如果改动毫无作用，估计出的差异会围绕零散布，散布的幅度是一个标准误。我们在超过1.96个标准误时宣布胜者，所以有5%的时候会被骗：这就是 alpha。"
        "<bookmark mark='b'/>如果改动确实带来了 delta 的提升，估计值就会围绕 delta 散布，而每当它没能越过那条线，我们就错过了一个真实的效应：这就是 beta，而1减 beta 就是功效。"
        "<bookmark mark='c'/>要有80%的功效，delta 必须位于那条线之外0.84个标准误处。",
    'f"That picture is a recipe for the sample size.':
        "这张图，就是计算样本量的配方。<bookmark mark='a'/>delta 必须等于1.96加0.84个标准误，而标准误是 sigma 乘以 n 分之2的平方根。<bookmark mark='b'/>解出 n。"
        "<bookmark mark='c'/>常数算出来是15.7，所以 n 约为16乘 sigma 的平方，除以 delta 的平方：这是每个做实验的人都熟悉的经验法则。"
        "<bookmark mark='d'/>在5%的转化率上，5%的相对提升，每组大约需要{r5['n_per_arm'] / 1000:.0f}千名用户；"
        "经验法则给出的是{r5['rule_16'] / 1000:.1f}千名。提升减半，所需人数就变成四倍：1%的提升，每组大约需要{rows_[0]['n_per_arm'] / 1000000.0:.0f}百万名用户。",
    'f"Formulas built on approximations deserve a check.':
        "建立在近似之上的公式，值得核对一下。<bookmark mark='a'/>我们模拟了两千次实验，真实提升为5%，每组{full['n']:,}名用户。"
        "<bookmark mark='b'/>检验在其中{100 * full['power']:.1f}%的实验里发现了这个提升，正是我们设计的80%，误差在模拟的噪声之内。<bookmark mark='c'/>用户减半，"
        "标准误就增大到根号2倍，delta 现在只是勉强越过那条线。功效降到{100 * half['power']:.0f}%：一个真实的改进，有一半的时候被错过了。<bookmark mark='d'/>更糟的是，"
        "当这样的检验真的得出显著结果时，它会夸大效应，因为只有那些幸运的高估，才能越过那条线。",
    # ------------------------------------------------------------------ s10_peeking
    "Chapter nine. Looking too often.": "第九章：看得太勤。",
    "Here is an experiment with nothing in it: two identical":
        "这里有一个什么都没有的实验：两个完全相同的版本，也就是一次 A/A 测试，每组每天一千名用户，转化率为5%。<bookmark mark='a'/>每天早上，都有人对到目前为止的全部数据，运行上一章的 z 检验。"
        "<bookmark mark='b'/>既然没有差异，p 值就无处落定。在任何一天，它落在0到1之间任何位置的可能性都相同，而且它一天天地游走，<bookmark mark='c'/>有时离红线很近。这六个实验中，"
        "有一个跌到了红线以下，就在最后一个早上。看的次数足够多，它们中的任何一个都可能这样。",
    'f"Now simulate four thousand of them, and stop each':
        "现在模拟四千个这样的实验，每个实验在它的 p 值第一次跌破5%的那个早上就停下来，宣布胜者。<bookmark mark='a'/>第一天，有{f[0]}%停下，和承诺的一样。一周之后，{f[1]}%已经停下。两周之后，"
        "{f[2]}%。<bookmark mark='b'/>到第三十天，在根本没有效应的实验中，有{100 * fpr[-1]:.0f}%宣布了一个效应。<bookmark mark='c'/>同样这些实验，"
        "如果只在最后看一次，结果是{100 * pk['fpr_final_only']:.0f}%。检验从来没有错；错的是停止规则。5%是对一次查看的承诺，而不是对三十次。",
    "f\"Why does looking hurt? <bookmark mark='a'/> Turn":
        "为什么多看会有害？<bookmark mark='a'/>把每个 p 值变回它的 z 统计量。当 z 超过1.96时，检验就拒绝。<bookmark mark='b'/>没有真实差异时，"
        "z 是一个随机游走除以其长度的平方根：这是第20部分的集中现象，动了起来。<bookmark mark='c'/>重对数律由亚历山大·辛钦（Aleksandr Khinchin）在1924年证明，"
        "它说 z 的峰值会不断回到大约根号下2 log log n 的高度，而这个值会无限增长。<bookmark mark='d'/>所以一个被永远盯着的游走，会越过任何一条固定的线。三十次相互独立的检验，"
        "会给出{100 * indep:.0f}%的假阳性；每天的查看共享了大部分数据，所以我们看到的是{100 * pk['fpr_peeking'][-1]:.0f}%，但每多看一次，都会增加一些。",
    "The fix is a test built to be watched. <bookmark mark='a'/>":
        "解决办法，是一种专门为被盯着看而构建的检验。<bookmark mark='a'/>亚伯拉罕·瓦尔德（Abraham Wald）的序贯检验，比较的是数据在有效应时的似然，与在无效应时的似然；"
        "Herbert Robbins 在1970年，把这个比值在一系列合理的效应上取了平均。<bookmark mark='b'/>当它达到 alpha 分之一，也就是20时，就停下。"
        "<bookmark mark='c'/>没有效应时，这个比值是一场公平的赌局：无论玩多久，它的期望值都保持为1，而 Ville 不等式说，它曾经达到20的概率至多是二十分之一。"
        "<bookmark mark='d'/>换成 z 的单位，边界就不再是平的：它起点很高，然后缓慢下降。"
        "<bookmark mark='e'/>Ramesh Johari、Pete Koomen、Leonid Pekelis 和 David Walsh 把这变成了始终有效的 p 值，每天早上查看都是安全的。",
    'f"We ran the mixture test on the same traffic,':
        "我们在同样的流量上运行了混合检验，每天查看一次。<bookmark mark='a'/>每天做 z 检验，有{100 * pk['fpr_peeking'][-1]:.0f}%的假阳性。"
        "<bookmark mark='b'/>混合检验的散布按5%的提升来调时，假阳性是{100 * sq['null']['rejected']:.1f}%；按10%的提升来调时，"
        "是{100 * sq['null_tau']['rejected']:.1f}%。两者都低于5%。<bookmark mark='c'/>现在给新版本一个真实的10%提升。在三十天内，"
        "第一个检验有{100 * sq['lift10']['rejected']:.0f}%的时候能抓住它，中位数在第{sq['lift10']['median_day']:.0f}天；"
        "第二个是{100 * sq['lift10_tau']['rejected']:.0f}%，在第{sq['lift10_tau']['median_day']:.0f}天。"
        "<bookmark mark='d'/>一个功效为80%的固定样本检验，每组需要将近三万名用户：整整一个月，只看一次。这就是其中的权衡：每次查看都有效，代价是功效。",
    # ------------------------------------------------------------------ s11_cuped
    "Chapter ten. Less noise, same truth.": "第十章：更少的噪声，同样的真相。",
    "Most of the variation in a metric has nothing to do with the":
        "一个指标中的大部分变化，都与实验无关。一个上个月花了很多钱的用户，这个月很可能也会花很多，不管他看到的是哪个版本。<bookmark mark='a'/>把每个用户在实验期间的指标，与他在前一个月的同一指标画在一起。"
        "指标的散布，主要取决于这个用户是谁。<bookmark mark='b'/>2013年，微软的 Alex Deng、Ya Xu、Ron Kohavi 和 Toby Walker，把这个补救办法称为 CUPED。"
        "<bookmark mark='c'/>从每个用户身上，减去他的过去所预测的部分：theta 乘以他实验前那段时间的指标与其平均值之差。<bookmark mark='d'/>点云变平了，散布缩小了。"
        "而两个版本之间的差异，丝毫没有改变。",
    "How much does it help? <bookmark mark='a'/> Expand the":
        "它能帮多大的忙？<bookmark mark='a'/>把调整后指标的方差展开：Y 的方差，减去2倍 theta 乘以协方差，再加上 theta 的平方乘以 X 的方差。"
        "<bookmark mark='b'/>这是关于 theta 的一条抛物线，在导数为零的地方最小：也就是协方差除以 X 的方差，即回归直线的斜率。<bookmark mark='c'/>把它代回去，方差就等于原来的方差，"
        "乘以1减 rho 的平方，rho 是过去与现在的相关系数。<bookmark mark='d'/>而真相保持不变，因为 X 是在随机化之前测量的：从期望上看，两组过去的平均值相同，所以这项调整去掉的是噪声，而不是效应。"
        "由此只有一条规则：永远不要用任何可能被实验处理改变的东西来做调整。",
    # ------------------------------------------------------------------ s11_cuped
    'f"We checked the formula on simulated experiments:':
        "我们在模拟实验上检验了这个公式：每组两万名用户，五种相关系数，每种重复两千次。<bookmark mark='a'/>蓝色的柱是用了 CUPED 之后测得的方差，除以不用时的方差；黄色的标记是 1 减 ρ 的平方。"
        "<bookmark mark='b'/>两者吻合：从过去什么也说明不了时的毫无帮助，<bookmark mark='c'/>到相关系数为 0.7 时方差降到 {r7['ratio']:.2f}，"
        "0.9 时降到 {r9['ratio']:.2f}。<bookmark mark='d'/>方差按用户数的倒数下降，所以 0.7 的相关系数大约相当于 {1 / r7['ratio']:.0f} 倍的流量，"
        "0.9 大约相当于 {1 / r9['ratio']:.0f} 倍：几周的实验，换成一行算术。",
    'f"Here is what that means for one':
        "来看看这对一次实验的结论意味着什么。<bookmark mark='a'/>真实的效应是 0.02 个标准差。不用 CUPED，95% 置信区间向两侧伸出的距离，几乎和效应本身一样大，只是勉强避开了零。"
        "<bookmark mark='b'/>现在提高与过去的相关性。在 0.5 时，区间窄了一点；<bookmark mark='c'/>在 0.7 时，"
        "窄了 {100 * (1 - r7['ci_cuped'] / r7['ci_plain']):.0f}%；<bookmark mark='d'/>在 0.9 时，"
        "窄了 {100 * (1 - r9['ci_cuped'] / r9['ci_plain']):.0f}%，不到原来宽度的一半。<bookmark mark='e'/>同样的用户，同样的效应；"
        "去掉的只是每个用户自己的历史早已解释了的那部分噪声。",
    "CUPED belongs to an old family. <bookmark mark='a'/> When":
        "CUPED 属于一个古老的家族。<bookmark mark='a'/>当用户分成行为不同的几组，比如轻度用户和重度用户，波动的一部分就落在组与组之间。"
        "<bookmark mark='b'/>分层法在每一组内部比较两个版本，再给各组加权，于是组间的那部分就从噪声里消失了。<bookmark mark='c'/>一般地，把指标对处理、以及处理之前测得的协变量做回归；"
        "处理的系数就是效应。CUPED 是只有一个协变量的情形，而这个协变量可以是一个模型根据过去做出的预测。<bookmark mark='d'/>Winston Lin 在 2013 年证明，加上交互项以后，"
        "这样做在大样本下不会损害精度。",
    # ------------------------------------------------------------------ s12_pitfalls
    "Chapter eleven. Pitfalls at scale.":
        "第十一章：大规模下的陷阱。",
    'f"Experiments report dozens of metrics. Take twenty,':
        "实验会报告几十个指标。取二十个，再取一个哪个指标都没有改变的改动。<bookmark mark='a'/>每个指标都有 5% 的机会看起来显著。<bookmark mark='b'/>跑一次实验，有一个指标亮了；"
        "再跑一次，亮的是另一个。<bookmark mark='c'/>至少有一个亮起来的概率，是 1 减去 0.95 的 20 次方，即 {100 * m['theory']:.0f}%；"
        "我们的模拟得到的是 {100 * m['naive']:.0f}%。<bookmark mark='d'/>报告那个动了的指标，你报告的通常就是噪声：这是第2部分的计数，掉转过来对准了我们自己。",
    'f"The cure is to be less impressed the more you':
        "解药是：看得越多，就越不要轻易被打动。<bookmark mark='a'/>Bonferroni 校正把阈值除以检验的次数：安全，但严格。<bookmark mark='b'/>1995年，"
        "Yoav Benjamini 和 Yosef Hochberg 提出了一条更温和的线：把 p 值排好序，把第 i 小的那个与 α 乘以 i 除以 k 相比较。"
        "<bookmark mark='c'/>直到最后一个落在线下的点为止，所有的点都算作发现。<bookmark mark='d'/>这控制的是错误发现率，也就是发现之中错误发现所占比例的期望。在什么都不是真的情况下，"
        "我们的实验里只有 {100 * m['bh']:.0f}% 做出了任何发现。",
    'f"Before reading any metric, check the split.':
        "读任何指标之前，先检查分组。<bookmark mark='a'/>一个五五开的测试，结束时一组有 {bad['a']:,} 名用户，另一组有 {bad['b']:,} 名，看上去很接近。"
        "<bookmark mark='b'/>皮尔逊（Pearson）卡方检验不同意：卡方值是 {bad['chi2']:.1f}，这么大的差距靠运气出现，大约是一万次里 {10000 * bad['p']:.0f} 次。"
        "<bookmark mark='c'/>{fine['a']:,} 对 {fine['b']:,}，则只是寻常的运气。<bookmark mark='d'/>不匹配意味着有什么东西不均匀地去掉了用户：一次重定向，"
        "一个机器人过滤器，一次让某个版本停止记录日志的崩溃。剩下的用户不再可比，所以每个指标都值得怀疑。",
    'f"Averages can reverse. <bookmark':
        "平均值可能会反转。<bookmark mark='a'/>一次改版在桌面端转化得更好，"
        "{100 * rates['new']['desktop']:.1f}% 对 {100 * rates['old']['desktop']:.0f}%，<bookmark mark='b'/>在移动端也更好，"
        "{100 * rates['new']['mobile']:.1f} 对 {100 * rates['old']['mobile']:.0f}。<bookmark mark='c'/>可是总体上它转化得更差："
        "{100 * rates['new']['overall']:.1f}% 对 {100 * rates['old']['overall']:.1f}%。<bookmark mark='d'/>它的访客大多在移动端，"
        "而在那里谁的转化率都更低；总体转化率又是按流量给各个细分加权的：这就是辛普森悖论，得名于 Edward Simpson 1951年的论文。<bookmark mark='e'/>随机化测试让两组有同样的构成，"
        "所以出现这样的构成本身就是一个警告：分组中途变了，或者根本没有随机化。",
    "A two-week test measures two weeks of behaviour. <bookmark":
        "一个为期两周的测试，测到的是两周的行为。<bookmark mark='a'/>一个新按钮被点击，是因为它新：这就是新奇效应，一种会消退的提升。<bookmark mark='b'/>与之相反的是首因效应："
        "习惯了旧设计的人，一开始会磕磕绊绊。<bookmark mark='c'/>所以，要把效应画成用户第一次看到改动以来的天数的函数，看看还没有养成习惯的新用户，并且一直跑到曲线变平为止。"
        "<bookmark mark='d'/>而当用户彼此影响时，比如市场里的买家，测试本身就是有偏的；这一点留给前沿一章。",
    "The last pitfall is wanting to believe. <bookmark mark='a'/>":
        "最后一个陷阱，是想要相信。<bookmark mark='a'/>Twyman 定律，以英国受众研究者 Tony Twyman 命名，由 Ron Kohavi 定为实验的一条规则：任何看起来有趣或与众不同的数字，"
        "通常都是错的。<bookmark mark='b'/>一个测试报告收入上涨了 38%。<bookmark mark='c'/>庆祝之前，先检查分组，检查日志记录是否变了，找找有没有机器人或者某一个极大的客户，"
        "再让一次 A/A 测试走同一条流水线。<bookmark mark='d'/>真正的改进通常很小。巨大的改进，通常是一个 bug。",
    # ------------------------------------------------------------------ s13_bandits
    "Chapter twelve. Bandits and metrics.":
        "第十二章：老虎机与指标。",
    "An A/B test gives the worse version half its traffic until":
        "A/B 测试有意让较差的版本一直拿到一半的流量，直到结束。老虎机算法（bandit），得名于赌场里被称作“独臂强盗”的老虎机，会一边学习，一边转移流量。<bookmark mark='a'/>《人工智能，"
        "从零搭建》第26部分见过其中最古老的好规则：汤普森采样，来自 1933年的 William Thompson。为每个版本的转化率保持一个信念。<bookmark mark='b'/>对每个访客，"
        "从每个信念中抽出一个可信的转化率，然后展示抽到的值更高的那个版本。<bookmark mark='c'/>随着证据到来，信念会变窄，而一个版本被尝试的频率，恰好等于它仍然可能是最好那个的概率。",
    'f"We raced the two on':
        "我们让两者在 {b['n']:,} 名访客上比赛，两个版本的转化率分别是 {100 * pa:.0f}% 和 {100 * pb:.1f}%。<bookmark mark='a'/>与始终展示更好的那个相比，"
        "五五分组大约损失 {b['regret_ab']:.0f} 次转化：这是它的遗憾。汤普森采样大约损失 {b['regret_ts']:.0f} 次。<bookmark mark='b'/>但看看各自学到了什么。"
        "分组测出的差异，标准差是 {100 * b['sd_ab']:.2f} 个百分点。老虎机算法让较差的版本饿着，精度大约差了 {ratio:.0f} 倍，它的区间很容易就包含零。"
        "<bookmark mark='c'/>所以：要优化、只在乎回报的时候，用老虎机算法，比如一个只活一天的标题；要弄清一个效应有多大，用 A/B 测试。",
    "An experiment must know what better means. <bookmark":
        "一个实验必须知道“更好”是什么意思。<bookmark mark='a'/>公司会选定一个北极星指标：一个代表为用户交付的价值的数字，这里是每周活跃买家数。<bookmark mark='b'/>它下面是驱动指标，"
        "变化更快，而且团队真的能改变它们。<bookmark mark='c'/>它们旁边是护栏指标：加载时间、崩溃、退订、客服工单，无论别的方面改善了多少，这些都不能变差。"
        "<bookmark mark='d'/>当 Ron Kohavi 所说的总体评价标准有所改善，而且没有任何护栏指标退步时，一个改动才会上线。",
    "Any metric can be gamed by the experiments meant to improve":
        "任何指标，都可能被本该改善它的实验钻空子。<bookmark mark='a'/>经济学家古德哈特（Charles Goodhart）在 1975年就货币目标指出了这一点；"
        "人类学家 Marilyn Strathern 给了它那句著名的表述：当一个度量变成目标，它就不再是一个好的度量。<bookmark mark='b'/>使劲推高点击，标题党就赢了；在它所代表的东西开始下降之后，"
        "指标还在继续上升。<bookmark mark='c'/>一个学习系统找到这个缺口，比任何人都快：这就是奖励投机，出自《人工智能，从零搭建》第31部分。<bookmark mark='d'/>防御的办法是：多个指标、"
        "护栏、长期保留组，以及去问用户。",
    "A short-term number can also turn a product against its":
        "一个短期的数字，也可能让产品反过来对付它的用户。<bookmark mark='a'/>2010年，设计师 Harry Brignull 给暗黑模式（dark patterns）起了名字："
        "诱骗人们去做他们本不想做的事情的设计。<bookmark mark='b'/>订阅只要点一下，退订要六步。一个预先勾好的框。一项到最后一步才出现的费用。一个嘲弄你的拒绝按钮。"
        "<bookmark mark='c'/>而一个只计算今天注册数的实验，会自己发现这些设计，并把每一个都算作胜利。",
    "Every A/B test is an experiment on people, usually a":
        "每个 A/B 测试都是一次在人身上做的实验，通常是无害的。<bookmark mark='a'/>2014年，Adam Kramer、Jamie Guillory 和 Jeffrey Hancock 报告说，"
        "在 2012年1月的一周里，大约 68.9万名 Facebook 用户被展示了更少的正面帖子，或者更少的负面帖子。<bookmark mark='b'/>他们自己发的帖子，也朝同一个方向轻微偏移。"
        "<bookmark mark='c'/>反应很强烈：没有人被征求过意见，期刊发表了一份编辑部关注声明。<bookmark mark='d'/>1979年的《贝尔蒙报告》要求对人的研究做到尊重个人、有益和公正；"
        "很少有产品测试会经过伦理委员会，但这些原则同样适用。<bookmark mark='e'/>不监视任何人的测量，留给前沿一章。",
    # ------------------------------------------------------------------ s14_frontier
    "Chapter thirteen, the frontier. What can an experiment not":
        "第十三章，前沿：一个实验看不到什么？",
    'f"Every test in this part assumed that what happens':
        "这一部分的每个测试都假设，一个用户身上发生的事，不取决于另一个用户身上发生的事。市场打破了这一点。<bookmark mark='a'/>我们模拟了一万名买家和三千件商品。处理让买家的购买意愿提高了六个百分点。"
        "<bookmark mark='b'/>但供给有限，所以实验组买家多拿走的每一件商品，都是对照组买家得不到的一件。"
        "<bookmark mark='c'/>A/B 测试报告的提升是 {100 * lim['ab_estimate']:.1f} 个百分点。把处理推给所有人，"
        "销量上升 {100 * lim['true_global']:.1f}：几乎为零，因为限制从头到尾都是供给。供给充足时，两者一致。<bookmark mark='d'/>解决办法是把彼此不相互作用的整个单元随机化："
        "整座城市，或者交替的时间段，称为轮换实验（switchback）；在社交网络里，则是朋友组成的聚类，这是 Johan Ugander 和同事在 2013年提出的。在干扰之下设计实验，是一个活跃的领域。",
    "A second limit is time. <bookmark mark='a'/> A test runs for":
        "第二个限制是时间。<bookmark mark='a'/>一个测试跑两周；而公司关心的事，人们明年是否还在用这个产品，要一年才能看到。新奇感会消退，习惯会养成，一个短期测试可能指错方向。"
        "<bookmark mark='b'/>一个答案是 Susan Athey、Raj Chetty、Guido Imbens 和 Hyunseung Kang 的替代指数：从许多过去的实验中学习短期信号如何预测长期结果，"
        "再把这个预测当作指标。<bookmark mark='c'/>另一个答案是长期运行的保留组：让少数用户几个月都留在旧产品上，用他们来衡量许多次上线累积起来的效应。"
        "<bookmark mark='d'/>替代指标什么时候可信，它可能错多少，都还是开放问题。",
    'f"A third limit is privacy: some things should be':
        "第三个限制是隐私：有些东西应当在不监视任何人的情况下测量。<bookmark mark='a'/>最古老的技巧，是 Stanley Warner 1965年提出的随机化回答。问一个敏感问题。每个人四次里有三次如实回答，"
        "其余时候就抛一枚硬币，改为给出硬币的答案。<bookmark mark='b'/>任何一个单独的答案都透露不出确定的信息，但只要撤销已知的噪声，就能还原总体中的比例。<bookmark mark='c'/>代价是精度："
        "真实比例为 20% 时，私密估计的误差大约是同样规模的诚实调查的 1.5 倍，我们试过的每种规模都是如此。用今天的话说，这就是本地差分隐私，ε 大约是 {pr['epsilon']:.1f}。"
        "<bookmark mark='d'/>2014年，Google 的 RAPPOR 用它来统计浏览器数据；2016年，Apple 用它来统计键盘数据；而 2020年的美国人口普查，则在中心化的层面上，"
        "对公布的表格应用了差分隐私。",
    "Finally, models. Fitts's and Hick's laws were the first":
        "最后是模型。菲茨定律和希克定律，是最早的关于人在计算机前的模型，而研究正在构建更丰富的模型。<bookmark mark='a'/>计算理性把人看作一个智能体，在自身感知和记忆的限制下，尽可能做出最好的决策，"
        "并从第一性原理出发，预测指点、打字和视觉搜索。<bookmark mark='b'/>模拟用户让设计者在任何人看到界面之前就能测试它；语言模型现在也被尝试用作合成的参与者，而谨慎是有充分理由的。"
        "<bookmark mark='c'/>而针对每个人自适应的界面，带来了它们自己的问题：自适应什么时候有帮助，什么时候又会让产品变得不可预测？<bookmark mark='d'/>在所有这些下面，是同一个问题："
        "预测在多大程度上能取代测量？",
    "Open problems. <bookmark mark='a'/> Interference:":
        "开放问题。<bookmark mark='a'/>干扰：为市场和社交网络设计的实验，既要无偏，又仍有足够的功效检测出小的效应。<bookmark mark='b'/>长期效应：知道短期替代指标什么时候可信，"
        "并给出它们可能错多少的界。<bookmark mark='c'/>私密的实验：在差分隐私下做 A/B 测试，而功效上的代价最小。<bookmark mark='d'/>以及足够准确的用户模型，能够取代第一轮真人测试。"
        "<bookmark mark='e'/>这一部分的研究题，把这一部分的两个想法结合起来：一个针对存在干扰的实验、始终有效的序贯检验，无论你看多少次，它的错误率都成立。",
    # ------------------------------------------------------------------ s15_outro
    "What we built in this part. Fitts's law, out of a noisy":
        "我们在这一部分搭建了什么。菲茨定律，出自一条由一次次修正动作构成的噪声信道；希克定律，出自一次选择的熵。由几个操作符预测任务用时。把颜色当作公式，并检查了这个系列自己的调色板的对比度，以及它对色盲观众的效果。"
        "一项可用性研究需要多少用户，以及为什么著名的五个人可能太少。A/B 测试及其样本量，每天都看所带来的假赢家，一个可以放心去看的序贯检验，还有 CUPED，它去掉了用户的过去已经解释了的那部分方差。贯穿其中的是一个想法："
        "人是可以测量的，但要测量得好，需要像对待任何其他实验一样小心。",
    "Where this comes back. Parts 45 and 50 run experiments on":
        "它们会在哪里再出现。第45和第50部分在基础设施本身上做实验，形式是金丝雀发布和分阶段上线。第46部分搭建流水线，记录这些实验所分析的每一个事件。第47部分给搜索结果排序，并测量排序是否有帮助。"
        "第51部分在 GPU 上绘制字形和颜色。而第57部分会提出这一部分统计问题的更深版本：我们在一些人身上测到的东西，什么时候能推广到其余的人？",
    "In practice. Make frequent targets big and close, and use":
        "实践中。把常用的目标做得又大又近，并利用屏幕的边和角。在十分之一秒内响应，过了一秒就显示进度，过了十秒就让人们可以去做别的事。文字的对比度至少要 4.5 比 1，永远不要把颜色当作唯一的信号，"
        "并且通过色盲模拟看看你的设计。用少数几个用户、经常测试，在两轮之间修好他们发现的问题。还有，在实验开始之前定好样本量，或者使用序贯检验，并且始终检查分组是不是你要求的那样。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整的解答在这一部分的笔记里。可以在任何一道上暂停。第五道是一道动手题：用老办法纠正每天偷看的问题，把 α 分给三十次查看，再把它的功效与序贯检验相比较。最后一道，标着星号，是一道研究题："
        "一个在实验中的人彼此影响时仍然有效的序贯检验。",
    "Next time, Part 45, and the start of Act Nine: the cloud. A":
        "下一次是第45部分，也是第九幕的开始：云。一个现代应用按秒租用它的计算机，计算机就在一座体育场那么大的建筑里。在下面是电力和冷却的预算，缩小成微虚拟机的虚拟机，用装箱算法放置的容器，"
        "以及不断让现状去符合应有状态的控制回路。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文，列在屏幕上，也在笔记里。感谢收看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
