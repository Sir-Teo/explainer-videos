"""Chinese narration for cs53: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第53部分：量子计算"

CHAPTERS = {
    "Hook": "Feynman 的问题",
    "Reversible": "1. 遗忘的代价",
    "Qubit": "2. 量子比特",
    "Entangle": "3. 门、张量积与纠缠",
    "Circuits": "4. 电路与通用性",
    "Interference": "5. 作为资源的干涉",
    "Simon": "6. Bernstein–Vazirani 与 Simon",
    "Qft": "7. 量子傅里叶变换",
    "Phase": "8. 相位估计",
    "Shor": "9. Shor 算法",
    "Grover": "10. Grover 搜索",
    "Bqp": "11. 量子计算机做不到的事",
    "Qec": "12. 量子纠错",
    "Frontier": "13. 前沿：密钥、化学与硬件",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "In 1981 Richard Feynman gave a talk with a simple question:":
        "1981年，Richard Feynman 做了一次演讲，提出一个简单的问题：计算机能模拟物理吗？<bookmark mark='a'/>对经典物理，可以。但一个由量子粒子组成的系统，"
        "要用一个复数来描述它们状态的每一种组合，这个复数叫作振幅。<bookmark mark='b'/>10个两态粒子大约需要1000个振幅，放得进16千字节。20个需要16兆字节。30个，16吉字节；40个，"
        "16太字节；50个，16拍字节。<bookmark mark='c'/>300个粒子需要的数，比可观测宇宙中的原子还多。Feynman 怀疑没有任何经典计算机能跟得上，于是提出了另一条路：用量子部件来造计算机，"
        "让自然去做算术。",
    "Part 1 met the extended Church–Turing thesis: any reasonable":
        "第1部分遇到过扩展的丘奇–图灵论题：任何合理的计算机，都能被一台概率图灵机以至多多项式级的减速模拟。<bookmark mark='a'/>1985年，David Deutsch 描述了一台通用量子计算机。"
        "<bookmark mark='b'/>1994年，Peter Shor 证明这样的机器能在多项式时间内分解大数，这将攻破第30部分的密码学。<bookmark mark='c'/>1996年，"
        "Lov Grover 证明它能用大约列表长度的平方根那么多步，搜索一个无序列表，而且没有任何量子算法能做得更好。<bookmark mark='d'/>2024年，一项实验显示，随着码变大，量子纠错变得更好，"
        "而不是更差。<bookmark mark='e'/>如果能造出大型的机器，扩展的论题就是错的。这一部分搭建其中的数学，再搭一个模拟器，并在上面运行每一个算法。",
    "This is Part 53 of Computer Science, Built. <bookmark":
        "这是计算机科学，从零搭建，第53部分。<bookmark mark='a'/>我们从遗忘一位的能量代价开始，以及从不遗忘的计算。然后是量子比特、Bloch 球和纠缠；干涉，每一个量子算法背后的资源；"
        "量子傅里叶变换，用第19部分的蝶形搭成；Shor 算法，在我们自己的模拟器上分解15和21；Grover 搜索；纠错；以及一份诚实的说明：量子计算机做不到什么。",
    # ------------------------------------------------------------------ s02_reversible
    "Chapter one. The cost of forgetting. Does computing have to":
        "第一章：遗忘的代价。计算一定要耗费能量吗？",
    "Most of the logic we built in Part 3 throws information":
        "我们在第3部分搭建的逻辑，大多会把信息扔掉。<bookmark mark='a'/>一个与门把四种可能的输入映到两种可能的输出。三种不同的输入都给出零，一旦看到这个零，你就说不出它是其中哪一种。"
        "<bookmark mark='b'/>这种遗忘是免费的吗？想象一下最简单的存储器：盒子里的一个分子，中间有一堵墙。在左边表示零，在右边表示一。<bookmark mark='c'/>要擦除这一位，"
        "也就是不管它原来存的是什么都把它置为零，就抽出墙，把一个活塞推到中间，再把墙放回去。<bookmark mark='d'/>两种可能的状态变成了一种。物理学告诉我们，失去的不确定性不会凭空消失："
        "它最终以热的形式进入周围环境。",
    "In 1961 Rolf Landauer, at IBM, put a number on it. <bookmark":
        "1961年，IBM 的罗尔夫·兰道尔给它定了一个数。<bookmark mark='a'/>擦除一个值未知的位，让存储器从两种可能的状态变成一种。<bookmark mark='b'/>它的熵减少了 Boltz"
        "mann 常数乘以2的对数。<bookmark mark='c'/>热力学第二定律说，总熵不能减少，所以至少有这么多的熵必须由热带到周围环境中：至少是 k T 乘以2的对数。"
        "<bookmark mark='d'/>在室温，也就是300开尔文下，<bookmark mark='e'/>每一位大约是3乘以10的负21次方焦耳，也就是千分之18电子伏特。"
        "<bookmark mark='f'/>在这个极限下每秒擦除10亿亿次，大约要耗费3毫瓦。真实的晶体管每次开关耗费的远远超过这个数。2012年，里昂的一个团队用双势阱激光阱里的一颗玻璃珠测量到了它。",
    "The way out is to compute without merging states. <bookmark":
        "出路是计算时不合并状态。<bookmark mark='a'/>托马索·托福利的门接受三位，只有在前两位都是一时才翻转第三位。<bookmark mark='b'/>它的表在八行中只动了两行，把它们交换："
        "它是一个置换，所以没有两个输入共享同一个输出，什么都没丢，连用两次就回到输入。<bookmark mark='c'/>爱德华·弗雷德金的门在第一位为一时交换第二位和第三位；它甚至保持一的个数不变，就像台球一样。"
        "<bookmark mark='d'/>两者都不扔掉任何东西，然而，把第三个输入置为零，托福利门写出的就是 a 且 b。给定常数输入，这两种门中的任何一种都能搭出任意布尔电路。逻辑并不需要遗忘。",
    "Charles Bennett, also at IBM, showed in 1973 that any":
        "同样在 IBM 的查尔斯·贝内特在1973年证明，任何计算都可以可逆地完成。<bookmark mark='a'/>给电路三个寄存器：输入，一块全为零的工作区，以及一个全为零的输出。"
        "<bookmark mark='b'/>先可逆地计算：工作区现在存着答案 f(x)，以及一堆中间垃圾。<bookmark mark='c'/>然后用受控非门把答案复制到输出里，这一步也是可逆的。"
        "<bookmark mark='d'/>最后把第一个电路倒着运行一遍。它把工作区连同垃圾一起变回零。从来没有擦除过任何东西，所以不欠任何热量。<bookmark mark='e'/>代价是大约两倍的步数，"
        "以及中途存放垃圾的空间。而这个技巧会在这一部分的每一个量子算法里再次出现：留下的垃圾会和答案保持纠缠，破坏干涉。",
    "Now write a reversible gate as a matrix acting on its basis":
        "现在把一个可逆门写成作用在它的基态上的矩阵。<bookmark mark='a'/>托福利门变成一个8乘8的矩阵，每一行和每一列都恰好有一个1：一个置换。"
        "<bookmark mark='b'/>非门是最小的一个。<bookmark mark='c'/>置换矩阵恰好就是元素只有0和1的那些酉矩阵。允许任意的酉矩阵，比如这一个，计算依然是可逆的，"
        "但不再是对状态的洗牌：它是一次旋转。<bookmark mark='d'/>这一步是在三篇论文里迈出的。1980年，Paul Benioff 把图灵机描述为一个量子力学系统。1982年，"
        "Feynman 提出用量子部件做成的计算机来模拟物理。1985年，David Deutsch 定义了通用量子计算机。下一章认识它的单元：量子比特。",
    # ------------------------------------------------------------------ s03_qubit
    "Chapter two. The qubit. What does one quantum bit actually":
        "第二章：量子比特。一个量子比特究竟存着什么？",
    "A qubit's state is a vector with two components, called":
        "一个量子比特的状态是一个有两个分量的向量，这两个分量叫作振幅：α 乘以状态零，加上 β 乘以状态一。<bookmark mark='a'/>把两个基态画成互相垂直的两根轴，把状态画成它们之间的一根单位箭头。"
        "<bookmark mark='b'/>测量时，我们以 α 平方的概率看到零，以 β 平方的概率看到一。这就是1926年的 Born 规则，也正是箭头长度为1的原因：概率之和必须是1。"
        "<bookmark mark='c'/>转动箭头，概率就平滑地变化。<bookmark mark='d'/>但振幅也可以是负的，一般来说是复数。这根箭头给出的概率和第一根一样，却是一个不同的状态。概率只能相加；"
        "振幅却能相互抵消，而量子算法正是建立在这个差别之上。",
    "How many numbers does a qubit need? <bookmark mark='a'/>":
        "一个量子比特需要多少个数？<bookmark mark='a'/>α 和 β 是复数，所以是四个实数，再加一个约束：剩下三个。<bookmark mark='b'/>把整个状态乘以一个相位，"
        "任何测量都分辨不出差别，所以我们可以去掉这个整体相位。剩下的、有物理意义的，是两个振幅之间的相对相位 φ。<bookmark mark='c'/>又因为两者大小的平方之和为1，它们就是同一个角的余弦和正弦，"
        "我们把这个角叫作 θ 除以2。<bookmark mark='d'/>两个角：球面上的一个点。<bookmark mark='e'/>在零对一的测量里，相对相位是看不见的。加态和减态都给出各一半的概率，"
        "只差一个符号。然而两者的差别已经大到两个状态所能达到的极限：在下一章里，一个门会把前者变成零，把后者变成一。",
    "Felix Bloch's sphere draws every state of one qubit as a":
        "Felix Bloch 的球面，把一个量子比特的每一个状态画成球上的一个点。<bookmark mark='a'/>θ 是纬度：零位于北极，一位于南极。<bookmark mark='b'/>把箭头向下倾到赤道"
        "，就到了加态，一个等权叠加。<bookmark mark='c'/>φ 是经度，也就是相对相位。沿赤道走一圈，会经过加 i 态、减态和减 i 态，它们的概率都是各一半。"
        "<bookmark mark='d'/>注意这个半角做了什么。零和一是互相垂直的向量，但在球面上它们是相对的两极；加态和减态也是相对的。每一对正交的状态，都位于一条直径的两端。"
        "<bookmark mark='e'/>对电子的自旋来说，这根箭头就是这样一根轴：沿着它测量，一定会发现自旋朝上。",
    "What does a measurement see on the sphere? <bookmark":
        "测量在球面上看到的是什么？<bookmark mark='a'/>根据 Born 规则，得到零的概率是 θ 的一半的余弦的平方。<bookmark mark='b'/>倍角公式把它变成1加上余弦 θ，再除以2。"
        "<bookmark mark='c'/>而余弦 θ 恰好就是箭头的高度 z。得到零的概率等于1加高度，再除以2：在北极是必然的，在南极是不可能的，在赤道上任何地方都是一半对一半，不管相位如何。"
        "<bookmark mark='d'/>测量可不温和。测量之后，状态就是我们看到的那个答案：箭头已经跳到了一个极点，其余的信息都没了。<bookmark mark='e'/>要问另一根轴，就先把它转到竖直方向，"
        "再测量。",
    "So a qubit's state takes a continuum of values. <bookmark":
        "所以一个量子比特的状态取值于一个连续统。<bookmark mark='a'/>我们能在里面存下一个完整的实数吗？<bookmark mark='b'/>不能。一次测量只返回一位，并毁掉其余部分。"
        "Alexander Holevo 在1973年证明，单独发送的 n 个量子比特，至多能携带 n 位经典信息。<bookmark mark='c'/>量子计算机的威力不在于存储。"
        "它来自许多量子比特在任何人观看之前一起发生的事情：它们的振幅成倍增多，并且相互干涉。<bookmark mark='d'/>在物理上，量子比特就是任何一个控制良好的二能级系统：超导电路的两个能级，"
        "或者一个被囚禁离子的两个能级；被激光光镊抓住的原子；或者一个光子的偏振。对所有这些，数学都是一样的。",
    # ------------------------------------------------------------------ s04_entangle
    "Chapter three. Gates, tensor products and entanglement. What":
        "第三章：门、张量积与纠缠。两个量子比特能做到哪些两个比特做不到的事？",
    "A one-qubit gate is a two by two unitary matrix: on the":
        "单量子比特门是一个2乘2的酉矩阵：在 Bloch 球上，就是一次旋转。<bookmark mark='a'/>Hadamard 门是绕 x 和 z 之间那根轴转半圈，把零变成加态。"
        "<bookmark mark='b'/>T 门在一的振幅上加一个八分之一圈的相位：绕竖直轴转八分之一圈。<bookmark mark='c'/>两个 T 门组成 S 门，转四分之一圈，到加 i 态。"
        "<bookmark mark='d'/>绕 x 轴转半圈，把零变成一：一个量子的非门。<bookmark mark='e'/>酉的意思是，U 的共轭转置乘以 U 等于单位矩阵：长度保持不变，"
        "所以概率之和仍然是1，而且每个门都可以撤销。",
    "Now two qubits. <bookmark mark='a'/> Two independent qubits":
        "现在看两个量子比特。<bookmark mark='a'/>两个独立的量子比特，由它们状态的张量积来描述。<bookmark mark='b'/>乘出来：四种结果各有一个振幅。"
        "<bookmark mark='c'/>但任何平方和为1的四个振幅都是允许的，不只是那些能分解成乘积的。<bookmark mark='d'/>每多一个量子比特，数目就翻一倍："
        "n 个量子比特有2的 n 次方个振幅。<bookmark mark='e'/>一个乘积态只需要2n 个数。不能分解的状态是纠缠的，一般需要全部2的 n 次方个数：这就是 Feynman 的模拟会耗尽内存的原因。",
    "The basic two-qubit gate is the controlled-NOT, which flips":
        "基本的双量子比特门是受控非门（CNOT），当第一个量子比特为一时，它翻转第二个。<bookmark mark='a'/>让两个量子比特都从零开始。<bookmark mark='b'/>对第一个做一次 Hada"
        "mard，零零和一零就得到相等的振幅。<bookmark mark='c'/>CNOT 把一零变成一一。我们的模拟器给出：一半的机会是零零，一半是一一，没有别的：这是一个 Bell 态。"
        "<bookmark mark='d'/>它是两个分开的量子比特吗？那样的话，α δ 等于零，所以 α 或 δ 为零，那么留下来的某个振幅也会消失。矛盾：这个状态是纠缠的。"
        "<bookmark mark='e'/>测量任何一个量子比特：结果是随机的，但另一个总是与它一致。",
    "Agreeing on random bits is easy: toss a coin in advance.":
        "在随机位上达成一致很容易：事先抛一枚硬币就行。这个游戏需要的更多。<bookmark mark='a'/>裁判随机发给 Alice 一位 x，发给 Bob 一位 y，两人不能交流。"
        "如果他们答案的异或等于 x 且 y，他们就赢：他们必须一致，除非两个问题都是一。<bookmark mark='b'/>经典策略为每个问题固定一个答案。<bookmark mark='c'/>把四个条件异或起来"
        "。左边每个答案都出现两次，相互抵消；右边得到一。所以至多三个能成立。<bookmark mark='d'/>没有任何经典策略的胜率能超过四分之三，我们对全部16种策略的搜索证实了这一点。",
    "Give Alice and Bob one qubit each of a Bell pair. <bookmark":
        "给 Alice 和 Bob 各一个 Bell 对中的量子比特。<bookmark mark='a'/>每个人沿着由问题决定的角度测量；他们一致的概率是两角之差的余弦平方。"
        "<bookmark mark='b'/>Alice 用0度或45度，Bob 用正负22.5度。在三种情况下，两个角相差22.5度：一致的概率是八分之 π 的余弦平方。"
        "<bookmark mark='c'/>在第四种情况下，它们相差67.5度，不一致的概率也恰好一样高。<bookmark mark='d'/>大约百分之85，对百分之75；我们的模拟器也这么说。"
        "没有传递任何消息。<bookmark mark='e'/>Boris Tsirelson 在1980年证明，没有任何量子策略能做得更好，而第27部分的 MIP* 等于 RE，正是从这样的游戏里成长起来的。",
    "No quantum computer can copy an unknown state; the proof":
        "没有任何量子计算机能复制一个未知的状态；证明只要三行。<bookmark mark='a'/>假设有一台酉机器能复制每一个状态：ψ 变成 ψ ψ，φ 变成 φ φ。"
        "<bookmark mark='b'/>取这两行的内积。酉变换保持内积，所以 φ 和 ψ 的重叠等于它自己的平方。<bookmark mark='c'/>所以重叠是0或1："
        "一台机器只能复制那些相同或者正交的状态。<bookmark mark='d'/>CNOT 能完美地复制零和一，但输入加态时，它做出的是一个 Bell 对，而不是两个加态：我们的模拟器算出重叠是二分之一。"
        "<bookmark mark='e'/>这曾让纠错看起来不可能，也正是窃听者会被抓住的原因。",
    # ------------------------------------------------------------------ s05_circuits
    "Chapter four. Circuits and universality. Which gates are":
        "第四章：电路与通用性。哪些门就够用了？",
    "Deutsch's quantum circuit model of 1989 is the standard one.":
        "Deutsch 1989年的量子电路模型，是标准的模型。<bookmark mark='a'/>每根线是一个量子比特，时间从左向右流：这里是一个 Hadamard、一个 CNOT、一个 T 门，以及测量。"
        "<bookmark mark='b'/>每一步是一个酉矩阵，电路就是它们的乘积。矩阵从右向左作用，所以第一个门写在最后。<bookmark mark='c'/>两个量子比特中只作用于其中一个的门，"
        "是它与单位矩阵的张量积。<bookmark mark='d'/>写出来，H 的每个元素乘以一份单位矩阵：4乘4。有 n 个量子比特时，这些矩阵每边是2的 n 次方，所以没有哪个模拟器会真的构造它们。",
    "Which gates do we need? <bookmark mark='a'/> Take chapter":
        "我们需要哪些门？<bookmark mark='a'/>拿第一章的托福利门来说。<bookmark mark='b'/>它可以用 Hadamard 门、T 门及其逆，以及 CNOT 搭出来。"
        "<bookmark mark='c'/>6个 CNOT、7个 T 门和2个 Hadamard；在我们的模拟器上乘出来，它恰好就是托福利门的置换。所以经典计算机能做的任何事，量子计算机都能做。"
        "<bookmark mark='d'/>1995年，Adriano Barenco 和同事们证明，CNOT 加上任意的单量子比特门，能精确地搭出任何酉矩阵。"
        "<bookmark mark='e'/>麻烦在于“任意”这个词：单量子比特门构成一个连续统，但真实的机器只提供一份简短而固定的菜单。",
    "Can two fixed gates, H and T, approximate every rotation?":
        "两个固定的门，H 和 T，能逼近每一个旋转吗？<bookmark mark='a'/>取乘积 T H T H。<bookmark mark='b'/>H T H 是绕 x 轴转八分之一圈，"
        "T 是绕 z 轴转八分之一圈。<bookmark mark='c'/>两者合起来成为一个旋转，转角是一圈的一个无理数倍。<bookmark mark='d'/>所以它的幂永远不会回到起点：对零一次又一次地作用，"
        "这些点会稠密地填满绕它的轴的一个圆。用 H 做共轭，得到第二根轴，而两者的乘积能逼近任何旋转。<bookmark mark='e'/>T 是必不可少的：没有它，由 H、S 和 CNOT 组成的电路，"
        "能在普通计算机上被高效地模拟。这就是 Gottesman–Knill 定理。",
    "But we also want few gates. Robert Solovay and Alexei Kitaev":
        "但我们还希望门少。Robert Solovay 和 Alexei Kitaev 各自独立地证明，门的数目只按1除以精度的对数的某个幂增长。<bookmark mark='a'/>证明是一个递归：先粗略地逼近，"
        "再用两个大约是剩余误差平方根大小的旋转的对易子，消去这个小误差，而这两个旋转各自在下一层被逼近。<bookmark mark='b'/>每一层把误差提升到二分之三次方，并把长度乘以5。"
        "<bookmark mark='c'/>展开 k 层。<bookmark mark='d'/>要达到精度 ε，需要二分之三的 k 次方像1除以 ε 的对数那样增长。"
        "<bookmark mark='e'/>所以长度按这个对数的大约4次方增长。对 H 和 T，后来的数论方法只需要这个对数的一个倍数。",
    "Every result in this part comes from a simulator of about a":
        "这一部分的每一个结果，都来自一个大约100行的模拟器。<bookmark mark='a'/>它把全部2的 n 次方个振幅存在一个数组里。要作用一个门，它把数组看成一个立方体，每个量子比特一根轴，"
        "把门的轴移到前面，乘以那个小矩阵，再把它们移回去。<bookmark mark='b'/>作用在一个量子比特上的门，成对地混合振幅，每对的下标只在那个量子比特的那一位上不同。"
        "<bookmark mark='c'/>在第一个量子比特上，配对的伙伴相隔4：这是第19部分 FFT 蝶形的一级，会在第七章再次出现。<bookmark mark='d'/>每个门都要流过所有振幅，"
        "每个16字节，在每个上只做很少的算术：受内存带宽限制，落在第9部分屋顶线的错误一侧。",
    "Real programs use libraries that build these same circuits.":
        "真实的程序使用构造同样电路的库。<bookmark mark='a'/>这是第三章的 Bell 电路，分别写在我们的模拟器、IBM 的 Qiskit 和 Google 的 Cirq 里。"
        "<bookmark mark='b'/>我们的模拟器打印出振幅：零零和一一上都是0.707。<bookmark mark='c'/>真实的设备从不显示这些。它返回的是被测量位的样本，大约一半零零，一半一一。"
        "<bookmark mark='d'/>而在电路运行之前，编译器会把它改写成机器的原生门，把每个双量子比特门安排到物理上相连的量子比特上，在需要的地方插入交换门。",
    # ------------------------------------------------------------------ s06_interference
    "Chapter five. Interference as a resource. Where does a":
        "第五章：作为资源的干涉。量子加速从哪里来？",
    "<bookmark mark='a'/> Flip a fair coin, then flip it again.":
        "<bookmark mark='a'/>抛一枚公平的硬币，再抛一次。概率沿着每条路径相乘，在路径之间相加，抛两次之后，结果仍然是一次抛硬币。<bookmark mark='b'/>现在对零作用两次 Hadama"
        "rd。振幅也沿着路径相乘、在路径之间相加，但它们带着符号。通向一的一条路径带上了一个负号。<bookmark mark='c'/>所以通向一的两条路径相互抵消，通向零的两条路径相互加强：结果是零，而且是确定的。"
        "<bookmark mark='d'/>代数用两行说的是同一件事。这种抵消就是干涉，而随机化算法的概率只能相加，做不到这一点。",
    "First we need the function as a gate. <bookmark mark='a'/>":
        "首先，我们需要把函数做成一个门。<bookmark mark='a'/>谕示把 x 和 y 映到 x 和 y 异或 f(x)。它是可逆的，而第一章的计算、复制、反计算，能从任何经典电路把它搭出来，不留下垃圾。"
        "<bookmark mark='b'/>现在把目标量子比特置为减态。<bookmark mark='c'/>如果 f(x) 是零，什么都不翻转。如果 f(x) 是一，减态的两项交换位置，"
        "这就等于同一个状态乘以负1。<bookmark mark='d'/>无论哪种情况，目标出来时都没有改变，而输入带上了一个符号：负1的 f(x) 次方。答案被反冲到了相位里。在单个基态上，符号是看不见的，"
        "但在叠加态里，它是一个相对符号，而相对符号会干涉。",
    "David Deutsch's problem of 1985 is the first in which":
        "David Deutsch 1985年的问题，是干涉获胜的第一个问题。<bookmark mark='a'/>一个函数把一位映到一位。它的两个值相等吗？在经典计算里，你必须求值两次。"
        "<bookmark mark='b'/>把输入量子比特置于等权叠加，把目标置于减态。<bookmark mark='c'/>一次查询就把两个答案同时反冲进相位。提出第一个符号，剩下的部分在两个值一致时是加号，"
        "不同时是减号。<bookmark mark='d'/>最后一个 Hadamard 把加变成零，把减变成一。<bookmark mark='e'/>常数函数总是给出零，平衡函数总是给出一，只要一次查询。"
        "这个电路从来没有得知 f 的任何一个值，只得知我们问的那一个事实。",
    "In 1992 Deutsch and Richard Jozsa scaled this up to n bits.":
        "1992年，Deutsch 和 Richard Jozsa 把它推广到 n 位。函数被承诺要么是常数，要么是平衡的，也就是恰好在一半的输入上为零。<bookmark mark='a'/>对四个量子比特做 Had"
        "amard，得到16个相等的振幅。<bookmark mark='b'/>谕示在每一个上盖上一个符号，再做一次 Hadamard，把它们汇到一起。对常数函数，每个符号都一致，所有振幅都堆到零零零零上。"
        "<bookmark mark='c'/>对平衡函数，符号恰好在那里相互抵消，振幅落到别的地方，每个函数落到不同的地方。<bookmark mark='d'/>为什么？最后一组 Hadamard 之后，"
        "全零的振幅是各个符号的平均值：f 是常数时为正负1，是平衡的时为零。<bookmark mark='e'/>我们的模拟器测到全零的概率，要么是1，要么是0。确定性的经典算法在最坏情况下需要9次求值；"
        "这里只需要1次。",
    "This is the recipe for the next five chapters. <bookmark":
        "这就是接下来五章的配方。<bookmark mark='a'/>用 Hadamard 铺开到每一个输入上；用谕示把每个输入的答案标记在它的相位里；然后作用一个变换，让错误的答案在其中相互抵消。"
        "<bookmark mark='b'/>人们很容易说，量子计算机是在并行地尝试每一个答案。但在谕示之后立刻测量，你得到的是一个随机的输入和它的值，不比一次经典查询更好。全部的收益都在第三步。"
        "<bookmark mark='c'/>而对 Deutsch–Jozsa，我们应该诚实。它的优势只是相对于必须确定无误的算法而言的。一个检查 k 个随机输入的随机化经典测试，"
        "被平衡函数骗过的概率至多是2的1减 k 次方。查询10次，它几乎从不出错。要对随机化算法取得指数级的差距，需要一个更难的问题，而 Daniel Simon 找到了一个。",
    # ------------------------------------------------------------------ s07_simon
    "Chapter six. Bernstein–Vazirani and Simon. Can a quantum":
        "第六章：Bernstein–Vazirani 与 Simon。量子计算机能快上指数倍吗？",
    "Ethan Bernstein and Umesh Vazirani, in 1993, hid a whole":
        "1993年，Ethan Bernstein 和 Umesh Vazirani 把一整个字符串藏进了一个函数里。<bookmark mark='a'/>这个函数把 x 映到 x 与一个秘密字符串 s 共有的那些位"
        "的奇偶性。<bookmark mark='b'/>在经典计算里，每次查询返回一位，所以你最多只能一次问一个位置：4位要4次查询，n 位要 n 次。<bookmark mark='c'/>在量子计算里，"
        "运行和 Deutsch–Jozsa 同样的电路。谕示在每个输入上盖上符号：负1的 s 点乘 x 次方。<bookmark mark='d'/>而这个符号的模式，"
        "恰好就是 Hadamard 从字符串 s 生成的模式，把第五章的公式倒过来读就知道。<bookmark mark='e'/>Hadamard 是自己的逆，所以最后一组 Hadamard 返回 s。"
        "<bookmark mark='f'/>我们的模拟器以概率1测到一零一一，也就是那个秘密，只用了一次查询。",
    "In 1994 Daniel Simon found a problem with an exponential":
        "1994年，Daniel Simon 找到了一个有指数级差距的问题。<bookmark mark='a'/>一个定义在 n 位字符串上的函数，被承诺以一种特殊的方式二对一：两个输入发生碰撞，"
        "恰好当它们按异或相差一个隐藏字符串 s。求 s。<bookmark mark='b'/>这是三位时的八个输入。每种颜色是一对：x 和 x 异或 s。<bookmark mark='c'/>在经典计算里，"
        "唯一的线索是碰撞，即两个输入有相同的输出；它们的异或就是 s。q 次查询大约有 q 平方除以2个配对，每一对是碰撞的概率是2的 n 减1次方分之一。<bookmark mark='d'/>所以第一次碰撞大约需要"
        "2的二分之 n 次方次查询。这就是第17部分的生日界，而 Simon 证明，没有任何经典算法，哪怕是随机化的，能做得好很多。",
    "Simon's circuit has two registers. <bookmark mark='a'/>":
        "Simon 的电路有两个寄存器。<bookmark mark='a'/>Hadamard 把第一个寄存器铺开到每一个输入上，一次查询把 f(x) 写进第二个寄存器。"
        "<bookmark mark='b'/>假设第二个寄存器读出某个值。有两个输入给出这个值，x0 和 x0 异或 s，所以第一个寄存器留在恰好这两者的等权叠加里。"
        "<bookmark mark='c'/>再做一次 Hadamard。每个输出 y 得到两份贡献，当 y 点乘 s 为零时符号一致，为一时符号相反。<bookmark mark='d'/>所以每个 y 点乘 s "
        "等于一的 y 都被抵消。<bookmark mark='e'/>留下来的，概率全都相等，是那些与 s 正交的 y。运行一次，就得到 s 必须满足的一个随机线性方程。",
    "Now collect equations. <bookmark mark='a'/> Our simulator's":
        "现在收集方程。<bookmark mark='a'/>我们的模拟器第一次运行给出一一零：所以 s 的前两位相等。第二次给出零零一：s 的最后一位是零。<bookmark mark='b'/>看着候选者。"
        "有7个非零字符串可能是 s。第一个方程排除了其中4个，第二个又排除了2个。<bookmark mark='c'/>剩下一个，一一零，它就是那个隐藏的字符串。<bookmark mark='d'/>一般来说，"
        "n 减1个独立的方程决定 s。每次运行以至少一半的概率给出一个新的独立方程，平均来说，比 n 次多一点的运行就够了，<bookmark mark='e'/>再用模二的高斯消去法收尾：对 n 是多项式的，"
        "而经典的是2的二分之 n 次方。",
    "Simon's result was the first exponential separation between":
        "Simon 的结果，是量子计算与随机化经典计算之间第一个指数级的分离。<bookmark mark='a'/>在对数坐标上，差距一目了然：经典代价是2的二分之 n 次方，一条陡峭上升的直线，"
        "而量子代价像 n 那样增长。<bookmark mark='b'/>而 Simon 的算法，和 Peter Shor 同一年发表的那个算法有着完全相同的形状。把异或换成普通的加法，"
        "把隐藏字符串换成隐藏的周期 r；把 Hadamard 换成量子傅里叶变换，把线性代数换成连分数。<bookmark mark='c'/>两者都是在一个群上寻找函数的隐藏周期，"
        "而同样的配方能对每一个阿贝尔群解决这个问题。<bookmark mark='d'/>有一点要小心。这个分离是相对于一个黑盒而言的。它并不证明，在任何不借助黑盒来陈述的问题上，量子计算机都胜过经典计算机，"
        "第十一章会解释这一点。",
    # ------------------------------------------------------------------ s08_qft
    "Chapter seven. The quantum Fourier transform. Can two to the":
        "第七章：量子傅里叶变换。2的 n 次方个振幅，能用大约 n 平方个门来变换吗？",
    "Part 19 met the discrete Fourier transform, and the fast":
        "第19部分认识了离散傅里叶变换，以及计算它的快速算法。<bookmark mark='a'/>量子版本是作用在振幅上的同一个变换：基态 j 变成每一个 k 的等权叠加，相位是 ω 的 j k 次方。"
        "<bookmark mark='b'/>ω 是一个单位根，绕圆周的若干分之一圈；对8个点，是八分之一圈。<bookmark mark='c'/>把矩阵的每个元素画成一根指向它的相位的箭头。"
        "第一行每列转八分之一圈，第二行转四分之一圈，依此类推。<bookmark mark='d'/>它恰好就是第19部分的矩阵，乘以根号 N 分之一，好让它是酉的。在经典计算里，"
        "FFT 对 N 个数需要大约 N log N 次运算。对2的 n 次方个数，这对 n 是指数级的。",
    "Here is the fact that makes the quantum transform cheap.":
        "这就是让量子变换变得便宜的那个事实。<bookmark mark='a'/>把输出下标 k 写成二进制。每一项的相位分裂成因子，k 的每一位各一个，<bookmark mark='b'/>而对所有位串求一个乘积"
        "的和，等于一组和的乘积。<bookmark mark='c'/>所以一个基态的变换，是 n 个单量子比特的乘积，每一个都是零和一的等权混合，带着各自的相位。<bookmark mark='d'/>整圈不起作用，"
        "所以第 l 个量子比特的相位只看见 j 的最后 l 位，读成一个二进制小数。<bookmark mark='e'/>对三个量子比特上的 j 等于5：半圈、四分之一圈，以及八分之五圈。没有任何东西是纠缠的。"
        "每个输出量子比特只需要一个 Hadamard 和几次旋转。",
    "The circuit comes straight from Part 19's fast Fourier":
        "这个电路直接来自第19部分的快速傅里叶变换。<bookmark mark='a'/>FFT 分级进行。每一级把下标只差一位的元素成对组合：一个蝶形。<bookmark mark='b'/>在量子计算机上，"
        "混合每一对只差一位的元素，就是一个单独的门：对那个量子比特做一次 Hadamard，正如第四章的模拟器所展示的。<bookmark mark='c'/>在两级之间，FFT 要乘以旋转因子，也就是 ω 的幂，"
        "取决于下标的其他位。它们变成了由其他量子比特控制的相位旋转。<bookmark mark='d'/>在这种形式的 FFT 里，输出按位反转的顺序出现，电路在末尾用交换门来修正。每一级的 N 除以2个蝶形，"
        "变成了一个单独的 Hadamard。",
    "Count the gates. <bookmark mark='a'/> On four qubits: the":
        "数一数门。<bookmark mark='a'/>在四个量子比特上：第一个得到一个 Hadamard 和三个受控旋转，下一个得到一个 Hadamard 和两个，依此类推，最后是两个交换。"
        "<bookmark mark='b'/>第 l 个量子比特需要一个 Hadamard 和 n 减 l 个旋转，所以总数是 n 乘以 n 加1再除以2，加上 n 除以2个交换：对2的 n 次方个点，"
        "是 n 平方量级的门。<bookmark mark='c'/>我们的模拟器在一个随机状态上运行这个电路，并与 numpy 的 FFT 比较。两者在舍入误差范围内一致，大约是10的负16次方。"
        "<bookmark mark='d'/>在8个量子比特上，电路有40个门，而 FFT 需要2048次运算，而且这个差距随 n 指数级增长。",
    "So what is it good for? <bookmark mark='a'/> Feed it a":
        "那它有什么用？<bookmark mark='a'/>给它一个周期性的状态：四个相等的振幅，相隔4，从1开始。<bookmark mark='b'/>变换之后，全部振幅都落在16除以4的倍数上，"
        "中间的一切都被干涉掉了。偏移量跑进了相位里，这里用颜色表示，而周期跑进了峰的位置里。<bookmark mark='c'/>这时一次测量会采到 N 除以 r 的一个倍数，这正是第九章里 Shor 算法所需要的。"
        "<bookmark mark='d'/>它不适合做什么：读出傅里叶系数。运行一次只得到一个样本。而把任意数据装进振幅，代价和数据本身一样大。<bookmark mark='e'/>1994年，"
        "Don Coppersmith 还证明，最小的那些旋转可以去掉，只剩下 n log n 量级的门，得到一个很接近的近似。",
    # ------------------------------------------------------------------ s09_phase
    "Chapter eight. Phase estimation. How do we read an":
        "第八章：相位估计。我们怎样读出一个特征值？",
    "Every unitary has eigenvectors, states it only multiplies by":
        "每个酉矩阵都有特征向量，也就是它只乘以一个数的那些状态。<bookmark mark='a'/>因为酉矩阵保持长度，这个数的大小是1：它是单位圆上的一个点，e 的2π i θ 次方。"
        "<bookmark mark='b'/>只作用在特征向量上时，这个相位是全局的，任何测量都看不见它。<bookmark mark='c'/>所以让一个处于加态的量子比特来控制这个酉矩阵。特征向量出来时没有改变，"
        "而相位被反冲到控制量子比特上，就像第五章那样。<bookmark mark='d'/>在控制量子比特的 Bloch 球上，从上方看，它的箭头绕竖直轴转过2π θ。这里 θ 是0.3，也就是转108度。"
        "这一章的问题是：怎样把这个角读到许多位。",
    "One qubit turned by theta gives at best a bit or two of":
        "一个转过 θ 的量子比特，至多给出 θ 的一两位。要得到许多位，就去问更多的量子比特。<bookmark mark='a'/>把 t 个计数量子比特置于加态。第一个控制 U 一次，下一个控制 U 两次，"
        "然后四次，依此类推，不断加倍。<bookmark mark='b'/>每个控制量子比特得到2的 k 次方乘以 θ，去掉整圈。对 θ 等于0.3：十分之三、十分之六、十分之二、十分之四、十分之八，"
        "然后又是十分之六。<bookmark mark='c'/>加倍会移动 θ 的二进制小数点，所以每个量子比特存着 θ 从某一位开始往后的各位。<bookmark mark='d'/>把这些量子比特乘出来，"
        "状态就是对 j 求和的 e 的2π i j θ 次方。这恰好是第七章的乘积形式。如果 θ 等于 m 除以2的 t 次方，计数寄存器存的就是 m 的傅里叶变换。",
    "Run the inverse Fourier transform on the counting register.":
        "对计数寄存器运行逆傅里叶变换。<bookmark mark='a'/>结果 m 的振幅是 T 个相位的平均值，每一步转过 θ 减去 m 除以 T。<bookmark mark='b'/>把这些项画成首尾相接的箭"
        "头。对最接近 θ 乘以 T 的那个 m，它们转得很慢，几乎排成一条直线，平均值很长。再往外一个结果，它们转得更快，卷过大半圈，大部分相互抵消。又是干涉。<bookmark mark='c'/>这个和是一个几何级"
        "数，它的大小给出每个结果的概率。<bookmark mark='d'/>对最近的 m，剩下的角至多是半步，这时概率至少是 π 平方分之4，大约百分之40。事实上它通常要大得多，"
        "而如果 θ 恰好等于 m 除以 T，概率就是1。",
    "Here is our simulator's run: theta nought point three, six":
        "这是我们模拟器的一次运行：θ 等于0.3，6个计数量子比特。<bookmark mark='a'/>64个结果上的分布。<bookmark mark='b'/>θ 乘以64等于19.2，落在两个结果之间，"
        "峰在19，测到它的概率是0.875。<bookmark mark='c'/>用二进制读是0.010011，也就是六十四分之十九，0.296875：θ 精确到6位。"
        "<bookmark mark='d'/>因为19.2不是整数，有些概率泄漏到邻居20和18上。每多一个计数量子比特，误差减半，而比想要的位数多用几个量子比特，就能让错误的答案变得很少见。",
    "Phase estimation is the workhorse of quantum algorithms.":
        "相位估计是量子算法的主力。<bookmark mark='a'/>下一章的 Shor 算法，就是对模 N 乘以 a 这个运算做相位估计，它的特征值揭示出我们需要的阶。"
        "<bookmark mark='b'/>在化学中，一个分子时间演化的相位给出它的能级。<bookmark mark='c'/>作用在 Grover 的旋转上，它能数出解的个数。"
        "<bookmark mark='d'/>但精度不是免费的。受控的幂把 U 作用1次、2次、4次，一直到32次：6位要作用63次，每多一位，工作量就翻倍，除非这些幂有捷径，就像模幂运算可以靠反复平方那样。"
        "<bookmark mark='e'/>Alexei Kitaev 1995年的原始版本，一次只用一个控制量子比特，从重复的运行中估计每个加倍后的角，再用经典方法把答案组合起来。",
    # ------------------------------------------------------------------ s10_shor
    "Chapter nine. Shor's algorithm. How does finding a period":
        "第九章：Shor 算法。找到一个周期，怎样就能分解一个数？",
    "Part 30's RSA rests on factoring being hard. Shor reduced":
        "第30部分的 RSA 建立在因数分解很难之上。Shor 把因数分解归结为寻找周期。<bookmark mark='a'/>列出7模15的幂：1、7、4、13，然后又是1。这个序列以周期4重复，也就是7的阶。"
        "<bookmark mark='b'/>如果阶 r 是偶数，a 的 r 次方减1就是 N 的倍数，而它可以分解为平方差。<bookmark mark='c'/>除非 a 的二分之 r 次方等于负1，"
        "N 不整除任何一个括号，所以每个括号都和 N 共有一个真因子，欧几里得算法能找到它：48和50给出3和5。<bookmark mark='d'/>随机选的 a 至少有一半的时候管用，而除了找 r 之外，"
        "一切都很快。",
    "Chapter eight promised that order finding is phase":
        "第八章承诺过，求阶就是相位估计。<bookmark mark='a'/>模 N 乘以 a 是可逆的，因为 a 有逆元，所以它是一个酉矩阵 U。从1出发，它沿着一个环走：1、7、4、13，再回来。"
        "<bookmark mark='b'/>把一个状态铺开在这个环上，每走一步，把它的相位扭转 r 分之 s 圈。<bookmark mark='c'/>U 把每一项向前移一步，而扭转作为一个相位出来："
        "这是一个特征向量，特征值是 e 的2π i 乘 r 分之 s 次方。<bookmark mark='d'/>把全部 r 个特征向量加起来，扭转在除了1以外的每个地方都相互抵消。所以普通的状态1，"
        "就是它们的一个等权叠加。<bookmark mark='e'/>对它做相位估计，返回 r 分之 s，s 是随机的。受控的幂来自反复平方，而这部分算术，大约 n 的立方个门，占了大部分代价。",
    "Our simulator factors fifteen, with a equal to seven, using":
        "我们的模拟器分解15，取 a 等于7，用9个计数量子比特，也就是15的4位的两倍再加1：512个结果。<bookmark mark='a'/>逆傅里叶变换之后，全部概率落在四个尖峰上，每个四分之一，"
        "位于512除以4的倍数处，正如第七章所预言的。<bookmark mark='b'/>384除以512是四分之三，它的分母就是阶，4。<bookmark mark='c'/>结果为256的一次运行给出二分之一，"
        "因为 s 和 r 有公因子，而结果为0的一次运行什么也给不出。我们的20次运行中，有9次直接找到了4。<bookmark mark='d'/>一个诚实的说明："
        "我们的模拟器把 a 的 x 次方模 N 直接写进了工作寄存器。",
    "Twenty-one, with a equal to two, is less tidy: the order is":
        "21，取 a 等于2，就没那么整齐了：阶是6，而6不整除2048。<bookmark mark='a'/>所以峰落在结果之间，概率泄漏到邻居上：最近的上面大约百分之11，再下一个上面将近百分之3。"
        "<bookmark mark='b'/>假设一次运行给出1707。把1707除以2048展开成连分数，这是伪装起来的欧几里得算法，在分母超过21之前停下：六分之五。"
        "<bookmark mark='c'/>阶是6。2的立方是8，而7和9与21分别共有因子7和3。<bookmark mark='d'/>为什么这样管用？只要2的 t 次方至少是 N 的平方，"
        "最近的结果就离 r 分之 s 足够近，以至于 r 分之 s 必定是一个渐近分数。<bookmark mark='e'/>给出三分之二或二分之一的运行，得到的是6的一个约数，"
        "而两个这样的约数的最小公倍数就能把它恢复出来。",
    "<bookmark mark='a'/> The best known classical method, Part":
        "<bookmark mark='a'/>已知最好的经典方法，第30部分的数域筛法，用时大致按 e 的位数的立方根次方增长。Shor 算法大约需要 n 的立方个门。在对数坐标上，一条曲线不断攀升，另一条几乎不升。"
        "<bookmark mark='b'/>筛法的纪录是 RSA-250，829位，在2020年花了大约2700核年。<bookmark mark='c'/>Shor 的方法也能求离散对数，"
        "所以 Diffie–Hellman 和椭圆曲线会和 RSA 一起倒下。<bookmark mark='d'/>要小心一点：早期分解15和21的硬件实验，用的是借助答案的知识简化过的电路，Smolin、"
        "Smith 和 Vargo 在2013年指出了这一点。",
    # ------------------------------------------------------------------ s11_grover
    "Chapter ten. Grover's search. How fast can a quantum":
        "第十章：Grover 搜索。量子计算机能多快找到一根针？",
    "Grover's algorithm looks for one marked item w among N,":
        "Grover 算法在 N 个项中寻找一个被标记的项 w，用的是一个把 w 的振幅符号翻转的谕示。<bookmark mark='a'/>一切都发生在一个平面上：被标记的状态，以及未标记项的均匀叠加。"
        "起始状态位于未标记轴上方一个小角 θ 处，正弦 θ 等于根号 N 分之一。<bookmark mark='b'/>谕示把状态关于未标记轴作反射。<bookmark mark='c'/>扩散步骤把它关于起始状态作"
        "反射。<bookmark mark='d'/>两次反射合成一次旋转，转角是两面镜子夹角的两倍：2θ。k 轮之后，角度是2k 加1，乘以 θ。这里 N 是64，六轮把状态带到刚好越过竖直的位置。",
    "The same rounds, seen as the sixty-four amplitudes.":
        "同样的这几轮，换成64个振幅来看。<bookmark mark='a'/>开始时它们都相等，各是八分之一。<bookmark mark='b'/>谕示把被标记的振幅翻到轴的下方。"
        "<bookmark mark='c'/>对振幅来说，扩散步骤的意思是：把每一个替换成平均值的两倍减去它自己，也就是关于平均值的反演。平均值降了一点，所以未标记的振幅稍稍缩小，而被标记的那个，远在平均值之下，"
        "一下跳到远在它之上。<bookmark mark='d'/>重复。六轮之后，被标记的振幅是0.998。<bookmark mark='e'/>继续下去，它又会下降，因为未标记的振幅变成了负的：旋转转过头了。",
    "Our simulator's success probability against the number of":
        "我们模拟器的成功概率随轮数的变化，与公式完全吻合：2k 加1乘以 θ 的正弦平方。<bookmark mark='a'/>当角度达到直角时，它达到峰值，大约在四分之 π 乘以根号 N 轮之后：对64个项，"
        "是六轮，成功率百分之99.7。<bookmark mark='b'/>运行更久，它就下降：12轮之后几乎为零，然后又爬升。和经典搜索不同，更多的工作可能让答案更差。"
        "<bookmark mark='c'/>随着 N 增大，轮数按根号 N 增长，而按随机顺序进行的经典搜索，平均需要查看大约 N 除以2次：对65000个项，是201轮，对大约32000次查看。",
    "Chapter eight promised another use for Grover's rotation.":
        "第八章承诺过 Grover 旋转的另一个用处。<bookmark mark='a'/>如果 N 个项中有 M 个被标记，同样的图景依然成立，只是正弦平方 θ 等于 M 除以 N。"
        "每一轮都是平面上转过2θ 的一次旋转。<bookmark mark='b'/>一个旋转的特征值是 e 的正负2i θ 次方：它的角度写在它的相位里。<bookmark mark='c'/>所以对 Grover "
        "步骤做相位估计，就能读出 θ，而 N 乘以正弦平方 θ，不必找到解就能数出解的个数。这就是量子计数，出自 Brassard、Høyer 和 Tapp 1998年的工作，它还能告诉我们该运行多少轮。"
        "<bookmark mark='d'/>没有什么要求必须用 Hadamard。把它们换成任何一个以概率 p 成功的算法，大约根号 p 分之一轮，就能取代 p 分之一次重复。",
    "Could a cleverer algorithm beat root N? No. <bookmark":
        "更聪明的算法能胜过根号 N 吗？不能。<bookmark mark='a'/>把每次运行与一个什么都不标记的谕示的运行作比较。一次查询至多能把两者推开的距离，是算法在那一刻放在 w 上的振幅的两倍。"
        "<bookmark mark='b'/>对 w 的全部 N 种选择求和。这些振幅的平方总和为1，所以它们的和至多是根号 N，而 T 次查询总共至多能把所有运行推开2T 根号 N。"
        "<bookmark mark='c'/>但要说出 w，N 次运行中的每一次，最终都必须与什么都不标记的运行相距一个固定的距离。<bookmark mark='d'/>所以 T 至少是一个常数乘以根号 N，"
        "这是贝内特、Bernstein、Brassard 和 Vazirani 在1997年证明的。<bookmark mark='e'/>对 n 位密钥的暴力搜索，只从2的 n 次方降到2的二分之 n 次方："
        "仍然是指数级的。",
    # ------------------------------------------------------------------ s12_bqp
    "Chapter eleven. What quantum computers cannot do. Where does":
        "第十一章：量子计算机做不到的事。BQP 在各个复杂性类中处于什么位置？",
    "What exactly can a quantum computer do efficiently?":
        "量子计算机究竟能高效地做什么？<bookmark mark='a'/>这个类是 BQP，由 Bernstein 和 Vazirani 在1993年定义。一个问题属于它，如果对 n 位的输入，"
        "一个经典程序能在多项式时间内写出一个电路，它由第四章门集中的多项式个门组成，最后测量一个量子比特。<bookmark mark='b'/>在“是”实例上，它以至少三分之二的概率接受；在“否”实例上，"
        "至多三分之一。<bookmark mark='c'/>这些三分之一是任意取的：运行 k 次取多数，错误就随 k 指数级下降，就像第27部分的 BPP 那样。"
        "<bookmark mark='d'/>而且 BQP 包含 BPP：第一章的托福利门能让任何经典电路变成可逆的，而对一个新的量子比特做 Hadamard，就是一枚公平的硬币。",
    "Where does BQP sit among the classical classes? <bookmark":
        "BQP 在经典的复杂性类中处于什么位置？<bookmark mark='a'/>如我们所见，它包含 BPP。<bookmark mark='b'/>至于上界，像 Feynman 那样写出一个结果的振幅："
        "对穿过中间基态的每一条路径求和，沿每条路径相乘，在路径之间相加，就像第五章那样。<bookmark mark='c'/>只用 Hadamard 门和托福利门，它们就足以完成任何量子计算，"
        "这时每条路径的权重都是正负同一个小数。振幅就是正路径的条数减去负路径的条数，再乘以一个比例因子。<bookmark mark='d'/>经典机器可以一次加一条路径，重复利用它的内存：指数时间，但多项式空间。"
        "而比较这两个计数，就把 BQP 放进了 PP 之内，这是 Adleman、DeMarrais 和 Huang 在1997年证明的。<bookmark mark='e'/>这些包含关系，没有一个已知是严格的。",
    "Does BQP contain the NP-complete problems? Nobody knows, but":
        "BQP 包含 NP 完全问题吗？没有人知道，但证据说不包含。<bookmark mark='a'/>这是大多数研究者相信的图景，尽管其中没有一点被证明。因数分解和离散对数既在 BQP 中，也在 NP 中，"
        "而且人们不认为它们是 NP 完全的。<bookmark mark='b'/>NP 完全问题位于 BQP 之外。暴力搜索只能获得平方根的加速：16个变量的65000种赋值，仍然需要201轮 Grover 迭代。"
        "而且相对于一个随机谕示，贝内特、Bernstein、Brassard 和 Vazirani 证明了 NP 不包含于 BQP。<bookmark mark='c'/>一个快速的量子算法必须利用结构，"
        "就像 Shor 算法那样。<bookmark mark='d'/>BQP 还可能伸到 NP 之外：相对于一个谕示，Raz 和 Tal 在2018年证明了它逃出了整个多项式层级。",
    "If quantum computers are more powerful, an experiment should":
        "如果量子计算机更强大，实验就应该能表明这一点。<bookmark mark='a'/>2011年，Scott Aaronson 和 Alex Arkhipov，以及独立地，Bremner、"
        "Jozsa 和 Shepherd，找到了一些采样任务：它们对量子硬件来说很自然，而在复杂性假设之下，对经典机器很难：一个高效而精确的经典采样器，会让多项式层级坍塌。"
        "<bookmark mark='b'/>2019年，Google 的团队报告，在53个量子比特上从随机电路中采样，用了大约200秒，并估计一台超级计算机要用1万年。"
        "<bookmark mark='c'/>IBM 回应说，更好地利用磁盘存储，一台超级计算机大约只需要两天半。<bookmark mark='d'/>2020年，中国的一个团队报告了一个光子版本。"
        "<bookmark mark='e'/>到2022年，张量网络方法已经模拟出了2019年的那个任务。较量还在继续，而扩展的丘奇–图灵论题，如今正在实验室里接受检验。",
    "Two limits bind every quantum algorithm. <bookmark":
        "有两个限制约束着每一个量子算法。<bookmark mark='a'/>第一个是 Beals、Buhrman、Cleve、Mosca 和 de Wolf 在1998年提出的多项式方法。"
        "每次查询把振幅乘以某个关于一个输入位的线性式，所以 T 次查询之后，每个振幅都是输入位的一个次数至多为 T 的多项式，<bookmark mark='b'/>而接受概率的次数至多是2T。"
        "<bookmark mark='c'/>奇偶性随每一位翻转，所以逼近它需要次数为 N 的多项式，而计算 N 位的奇偶性需要 N 除以2次查询。第五章的 Deutsch 技巧恰好做到了这一点。"
        "<bookmark mark='d'/>没有承诺时，量子查询至多节省一个多项式因子。指数级的加速，比如 Simon 和 Shor 的那些，需要结构。<bookmark mark='e'/>第二个是 Holevo"
        " 界：n 个量子比特至多携带 n 位经典信息。",
    # ------------------------------------------------------------------ s13_qec
    "Chapter twelve. Quantum error correction. How do we protect":
        "第十二章：量子纠错。一个既不能复制、也不能查看的状态，我们怎样保护它？",
    "Part 28 protected bits by copying them and reading the":
        "第28部分保护位的办法，是复制它们并读取这些副本。对量子比特，这三个想法看起来都行不通，一些顶尖的物理学家曾怀疑量子计算机能否做得可靠。<bookmark mark='a'/>第一，"
        "第三章的不可克隆定理禁止复制。<bookmark mark='b'/>第二，读取一个量子比特会毁掉它：测量一个叠加态，你只剩下零或一。<bookmark mark='c'/>第三，错误是连续的："
        "一个量子比特可以漂移任意小的角度。<bookmark mark='d'/>1995年，Peter Shor 找到了绕过这三点的办法，Andrew Steane 在1996年找到了另一种：用纠缠把状态铺开，"
        "只测量奇偶性，它们揭示错误，却不透露关于状态的任何信息。",
    "The simplest code protects against bit flips. <bookmark":
        "最简单的码防的是位翻转。<bookmark mark='a'/>两个 CNOT 把一个量子比特铺开到三个上，成为一个纠缠态，而不是三个副本。<bookmark mark='b'/>假设中间的量子比特翻转了。"
        "<bookmark mark='c'/>借助额外的量子比特，测量两个奇偶性：第一个和第二个是否一致，第二个和第三个是否一致？两项给出相同的答案，所以我们得知错误在哪里，而对振幅一无所知。"
        "<bookmark mark='d'/>每一种单个翻转点亮一种不同的模式，也就是伴随式，就像第28部分的汉明码那样。把出错的那个翻回来，我们的模拟器在全部四种情况下都恢复了原来的振幅。",
    "The third obstacle, continuous error, dissolves when the":
        "第三个障碍，连续的错误，在测量伴随式时就消解了。<bookmark mark='a'/>一个小小的、不想要的转角为 ε 的旋转，是什么都不做与一次完整位翻转的组合。"
        "<bookmark mark='b'/>作用在编码后的状态上，它产生无错误与一次完整翻转的叠加。<bookmark mark='c'/>测量伴随式会迫使它作出选择：以余弦平方 ε 的概率，没有错误；"
        "以正弦平方 ε 的概率，一次完整的翻转，而我们知道怎样撤销它。<bookmark mark='d'/>而一个量子比特上的任何错误，都是四种的组合：什么都没有、位翻转、相位翻转，或者两者都有。"
        "纠正了位翻转和相位翻转，其他一切也就都纠正了。",
    "Qubits suffer a second kind of error: a phase flip, which":
        "量子比特还会遭受第二种错误：相位翻转，它把加态变成减态。<bookmark mark='a'/>在 Hadamard 基下，相位翻转就是位翻转，所以同一个码转个方向，就能抓住它。"
        "<bookmark mark='b'/>Shor 把两者嵌套起来：三个块防相位翻转，每个块三个量子比特防位翻转，一共九个。<bookmark mark='c'/>一个块中任何地方的相位翻转，"
        "都会改变那个块的符号，比较相邻块的校验就会亮起来。<bookmark mark='d'/>每个校验都是 Pauli 算符的一个乘积，它让每个码字保持不变。"
        "Daniel Gottesman 1997年的稳定子形式体系，就用这种方式描述整族的码：这里九个量子比特上的八个校验，留下一个逻辑量子比特。",
    "The leading design today is the surface code, from Alexei":
        "今天领先的设计是表面码，它来自 Alexei Kitaev 1997年的环面码，由 Dennis、Kitaev、Landahl 和 Preskill，以及 Fowler 和同事们在2012年发展起来。"
        "<bookmark mark='a'/>数据量子比特位于网格的角点上。每个面测量它各个角的奇偶性：蓝色的面抓位翻转，紫色的面抓相位翻转，而每个校验只涉及近邻。"
        "<bookmark mark='b'/>一次位翻转点亮它旁边的蓝色面。<bookmark mark='c'/>一串翻转只点亮它的两端，而解码器用能解释它们的最短链，把点亮的面配成对。"
        "<bookmark mark='d'/>只有一条横穿整个格子的链才不会被看见：在距离为5时，这需要5个错误，而任意两个错误都能被纠正。",
    "Take the simplest case: the repetition code against":
        "取最简单的情形：针对独立位翻转的重复码。<bookmark mark='a'/>距离为 d、用多数表决时，只有超过一半的位翻转，这个码才会失败。<bookmark mark='b'/>对小的 p，"
        "第一个失败项占主导，所以逻辑错误率像 p 的 d 加1再除以2次方那样下降。<bookmark mark='c'/>在阈值以下，这里是二分之一，码越大越好：在百分之1时，距离每增加一级，错误大约除以30。"
        "在阈值以上，越大越差。<bookmark mark='d'/>真实噪声下的真实码，阈值接近百分之1。2024年，Google 的团队把一个表面码从距离3增大到5再到7，每一步大致把逻辑错误减半：在硬件上，"
        "明确地处于阈值之下。",
    # ------------------------------------------------------------------ s14_frontier
    "Chapter thirteen, the frontier. What will quantum computers":
        "第十三章：前沿。量子计算机究竟会改变什么？又会在什么时候？",
    "Quantum mechanics also protects secrets. <bookmark":
        "量子力学也能保护秘密。<bookmark mark='a'/>在贝内特和 Brassard 1984年的协议里，Alice 发送随机的位，每一位都编码在随机选定的两组基之一中。Bob 用随机的基测量每一位，"
        "之后他们公开比较所用的基，只保留两人一致的那些位置。<bookmark mark='b'/>没有人偷听时，我们模拟中保留下来的位完全一致。<bookmark mark='c'/>窃听者要了解任何东西就必须测量，"
        "而用错误的基测量会扰动状态：保留下来的位中有四分之一会出错，Alice 和 Bob 就会察觉。<bookmark mark='d'/>更紧迫的防御根本不需要量子硬件。2024年，"
        "美国标准机构 NIST 发布了后量子算法，用格和基于哈希的问题取代 RSA 和椭圆曲线，这些问题还不知道会被 Shor 算法攻破；迁移正在进行，因为今天记录下来的数据，以后可能被解密。",
    "How far away is a machine that breaks today's cryptography?":
        "一台能攻破今天密码学的机器还有多远？<bookmark mark='a'/>资源估计下降得很快。2019年，Craig Gidney 和 Martin Ekerå 估计，分解一个2048位的 RSA 密钥，"
        "大约需要2000万个带噪量子比特，运行大约8小时。2025年，Gidney 把它降到了100万个量子比特以下，用时不到一周。<bookmark mark='b'/>两者都假设物理错误率大约是千分之一，"
        "并使用第十二章的表面码；今天最大的机器有几百到大约一千个物理量子比特。<bookmark mark='c'/>决定性的一步，是随着码变大而改进的纠错，而在2024年，Google 的团队展示了它："
        "距离每增加一级，逻辑错误率大致减半。我们的重复码在纸面上表现得好得多，但它只纠正位翻转，而一个真实的码还必须抓住相位错误。",
    "What are they likely to be good for? <bookmark mark='a'/>":
        "它们可能擅长什么？<bookmark mark='a'/>第一，Feynman 自己的问题：模拟分子和材料，它们的电子纠缠得太厉害，经典方法应付不了，而量子计算机恰恰是合适的那种机器。"
        "<bookmark mark='b'/>第二，密码分析，这就是为什么向新密码学的迁移已经开始了。<bookmark mark='c'/>在别的地方，理由就弱一些。为推荐系统和优化提出的几种量子加速，"
        "经过仔细审视之后，都被新的经典算法追平了，第一个是 Ewin Tang 在2018年的算法。<bookmark mark='d'/>从2019年起，关于采样任务上量子优势的声称，一再受到更好的经典模拟的挑战。"
        "较量还在继续，这本来就该如此。",
    "Open problems. <bookmark mark='a'/> Whether quantum":
        "未解问题。<bookmark mark='a'/>量子计算机能否快速求解 NP 完全问题：没有已知的算法，大多数研究者预期也不会有。<bookmark mark='b'/>一个具有已证明的、"
        "可验证的指数级加速的实际问题。<bookmark mark='c'/>因数分解对经典计算机究竟是否困难，这一点就像第26部分的每一个下界一样，没有人能证明。"
        "<bookmark mark='d'/>还有每个逻辑量子比特所需物理量子比特更少的码。<bookmark mark='e'/>这一部分的研究题问的是，分解一个2048位数的机器能有多小：在千分之一的错误率下，"
        "物理量子比特的最小时空体积，以及与之匹配的下界。",
    # ------------------------------------------------------------------ s15_outro
    "What we built in this part. The energy cost of erasing a":
        "这一部分我们搭建了什么。擦除一位的能量代价，以及避开它的可逆计算。量子比特，一个由两个复振幅组成的单位向量，以及在 Bloch 球上旋转它的门。纠缠，它能赢下一个任何经典策略都赢不了的游戏，"
        "以及禁止复制的那条定理。干涉，每一个算法背后的资源：Deutsch–Jozsa、Bernstein–Vazirani 和 Simon。量子傅里叶变换，用第19部分的蝶形搭成；相位估计；Shor 算法，"
        "在我们自己的模拟器上分解15和21；Grover 的平方根搜索，以及它不可能被超越的证明；还有纠错，它把许多带噪的量子比特变成较少的好量子比特。",
    "Where this comes back. Part 54 proves programs correct, and":
        "这些内容会在哪里再出现。第54部分证明程序是正确的，同样的逻辑可以推广到量子程序。第55部分问我们能信任什么，后量子迁移也包括在内。第56部分的扩展图能构造好的码，经典的和量子的都有。"
        "第58部分赋予程序数学意义。第60部分为单一的任务搭建硬件，而今天的每一台量子计算机都是这样。",
    "In practice. Find every place your systems rely on RSA or":
        "实践中。找出你的系统中依赖 RSA 或椭圆曲线的每一个地方，并规划向新标准的迁移。在一个开源工具包里试验小电路，先在模拟器上。一台笔记本电脑能存下大约30个量子比特的完整状态向量；对浅电路，张量网络能走得更远。"
        "拿任何声称的加速与最好的经典算法比较，而不是与朴素的算法比较。还有，关注逻辑错误率，而不是原始的量子比特数目。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：用我们的模拟器对35运行 Shor 算法，并数一数要运行多少次才能找到阶。最后一道标有星号，是研究题："
        "能分解一个2048位数的最小机器，以及没有更小的机器能做到的证明。",
    "Next time, Part 54: proving programs correct. Testing can":
        "下一次，第54部分：证明程序是正确的。测试能表明错误的存在，却永远不能表明它们不存在。弗洛伊德和霍尔把程序变成了逻辑公式，而今天，整个编译器和操作系统内核都带有经过机器检查的证明。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
