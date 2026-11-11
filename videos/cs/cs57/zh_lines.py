"""Chinese narration for cs57: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第57部分：学习理论"

CHAPTERS = {
    "Hook": "学习在什么时候是可能的",
    "Pac": "1. 概率近似正确",
    "Vc": "2. VC 维",
    "Margins": "3. 间隔与 Rademacher 复杂度",
    "Boosting": "4. 提升法",
    "Online": "5. 在线学习",
    "Bandits": "6. 老虎机",
    "Limits": "7. 什么学不会",
    "Overparam": "8. 参数比数据还多",
    "Compression": "9. 学习就是压缩",
    "Frontier": "10. 前沿：压缩方案与上下文学习",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    'f"Here is a puzzle that learning theory had to face.':
        "这里有一个学习理论不得不面对的谜题。<bookmark mark='a'/>我们用一个使用 p 个特征的线性模型，去拟合50个带噪声的样例。特征很少时，模型太简单。随着 p 增大，在新数据上的误差上升，先是缓慢"
        "，然后陡峭：这是过拟合的经典图景。<bookmark mark='b'/>在 p 等于50时，模型能拟合任何东西，连噪声也一起拟合，测试误差随之爆炸。<bookmark mark='c'/>然后，越过这一点，再"
        "增加更多的参数，误差反而又降了下来，降到比起点还低：在{best['p']}个特征时，它比任何参数少于样例的模型都低。这就是双下降。要理解它，我们首先需要经典理论：学习究竟在什么时候是可能的，又需要多少样例？",
    "AI, Built showed machines that learn. This part asks what":
        "《人工智能，从零搭建》展示了会学习的机器。这一部分要问的是，关于它们能证明些什么。<bookmark mark='a'/>一个学习器需要多少样例，它的答案才是概率近似正确的？Leslie Valiant 在19"
        "84年把这个问题表述得精确，而答案是一个数：VC 维。<bookmark mark='b'/>如果根本不存在分布，每个样例都由一个对手来挑选呢？那么正确的度量是遗憾，而答案中包括第44部分的老虎机。"
        "<bookmark mark='c'/>还有，无论数据有多少，什么东西永远无法被高效地学会？那里的答案来自密码学。",
    "This is Part 57 of Computer Science, Built. <bookmark":
        "这是《计算机科学，从零搭建》的第57部分。<bookmark mark='a'/>我们会定义概率近似正确学习；证明 VC 维决定了需要多少样例；看看为什么支配感知机和提升法的是间隔，而不是维数；在对手面前在线学"
        "习，并给遗憾定界；遇到无法被高效学会的问题；最后回到双下降，以及作为压缩的学习。",
    # ------------------------------------------------------------------ s02_pac
    "Chapter one. Probably approximately correct.":
        "第一章：概率近似正确。",
    "In 1984 Leslie Valiant asked what it should mean for a":
        "1984年，Leslie Valiant 问：一台机器从样例中学习，应该意味着什么？<bookmark mark='a'/>大自然固定一个输入上的分布，学习器永远看不到它；还固定一个目标，它来自学习器知道的一个"
        "类：这里是一个隐藏的矩形。<bookmark mark='b'/>学习器收到 m 个样例，每个都从这个分布中抽取，并带着它的标签；然后返回一个假设：这里是围住正例点的最紧的方框。"
        "<bookmark mark='c'/>它的误差，是假设与目标不一致的那片区域的概率，用红色标出。<bookmark mark='d'/>Valiant 要求：在样本的随机性上，以至少1减 delta 的概率，"
        "误差至多是 epsilon，<bookmark mark='e'/>而且对每一个分布、每一个目标都成立，所用的样例和计算量都是 epsilon 分之一和 delta 分之一的多项式。概率地、近似地、正确。",
    "Start with a finite class that contains a perfect hypothesis":
        "从一个包含完美假设的有限类开始，这是可实现的情形；如果一个假设的误差超过 epsilon，就称它是坏的。<bookmark mark='a'/>一个固定的坏假设，在每个随机样例上存活下来的概率小于1减 epsi"
        "lon，所以它在全部 m 个样例上都存活下来的概率至多是 e 的负 epsilon m 次方。<bookmark mark='b'/>由第2部分的联合界，任何一个坏假设存活下来的概率，至多是类的大小乘以这个数。"
        "<bookmark mark='c'/>要求它至多是 delta，<bookmark mark='d'/>然后求解：m 至少是 epsilon 分之一，乘以类大小的对数加上 delta 分之一的对数。"
        "<bookmark mark='e'/>对1000个假设，epsilon 和 delta 都取0.05，199个样例就足够了，无论返回的是哪一个一致的假设。类的大小只通过它的对数进入。",
    "Usually no hypothesis is perfect. The agnostic model asks":
        "通常没有哪个假设是完美的。不可知模型只要求学习器与类中最好的假设相差在 epsilon 以内，而自然的学习器，就是让自己在样本上的误差最小。<bookmark mark='a'/>对一个固定的假设，样本误差是 "
        "m 次独立抛硬币的平均，第20部分的霍夫丁不等式说，它偏离真实值超过 epsilon 的概率，至多是2乘以 e 的负2 m epsilon 平方次方。<bookmark mark='b'/>一个联合界覆盖整个类"
        "，<bookmark mark='c'/>求解得到，m 的量级是类大小的对数除以 epsilon 的平方。<bookmark mark='d'/>于是样本上最好的假设，与所有假设中最好的那个相差在2 epsil"
        "on 以内。<bookmark mark='e'/>噪声的代价是一个平方：对同样的1000个假设，需要2120个样例，是原来的十倍多。",
    "Most interesting classes are infinite, rectangles for":
        "大多数有意思的类都是无限的，比如矩形；然而矩形是可以学会的，用的是 Kearns 和 Vazirani 教科书开篇的那个论证。<bookmark mark='a'/>学习器返回围住正例的最紧的方框，它位于目标之"
        "内。沿着目标的四条边画四个条带，每个的概率是 epsilon 除以4。如果每个条带里都落有一个样例，方框漏掉的就只是条带的一部分，所以它的误差至多是 epsilon。<bookmark mark='b'/>一个"
        "条带被全部 m 个样例错过的概率，是1减 epsilon 除以4的 m 次方。<bookmark mark='c'/>对四个条带取联合界，<bookmark mark='d'/>令它低于 delta，"
        "<bookmark mark='e'/>就得到 epsilon 分之4乘以 delta 分之4的对数个样例，哪里都没有类的大小。",
    "How loose is that? Our instrument learned this rectangle two":
        "这个界有多松？我们的仪器在8种样本量下，各把这个矩形学了200次。<bookmark mark='a'/>平均误差像 m 分之一那样下降。<bookmark mark='b'/>第95百分位数，是实际误差以1减"
        " delta 的概率低于的那个值，这正是定理所界定的量。<bookmark mark='c'/>界处处都在它上方；从100个样例开始，高出2到3倍。这个常数，是为每一个分布都给出保证所付的代价，而不只是为我们采"
        "样所用的均匀分布。",
    "So what replaces the size of the class? <bookmark mark='a'/>":
        "那么，用什么来代替类的大小？<bookmark mark='a'/>半平面和矩形一样，是无限的。但学习器遇到的，只是这个类在它的样本上做了什么。<bookmark mark='b'/>10个点可以有1024种标"
        "注方式。<bookmark mark='c'/>半平面只能产生其中的92种；我们的仪器用线性规划检查了每一种标注。<bookmark mark='d'/>这个行为的计数，也就是增长函数，可以取代类的大小；而第二"
        "章会证明，有一个数，VC 维，控制着它。",
    # ------------------------------------------------------------------ s03_vc
    "Chapter two. The VC dimension.":
        "第二章：VC 维。",
    "In 1971 Vladimir Vapnik and Alexey Chervonenkis measured an":
        "1971年，Vladimir Vapnik 和 Alexey Chervonenkis 衡量一个无限的类，不是看它的大小，而是看它能用多少种方式标注点。<bookmark mark='a'/>在平面上取三个不共"
        "线的点，把每个涂成绿色或红色：有8种方式。<bookmark mark='b'/>对其中每一种，都有一条直线把绿点放在一侧、红点放在另一侧；我们的仪器用线性规划逐一检查了。"
        "<bookmark mark='c'/>一个类如果能实现一个点集的每一种标注，就说它打散了这个点集，<bookmark mark='d'/>而 VC 维，就是这个类能打散的最大点集的大小。对半平面，它至少是3。",
    "Can half-planes shatter four points? <bookmark mark='a'/> At":
        "半平面能打散四个点吗？<bookmark mark='a'/>在正方形的四个角上，16种标注中有14种是可分的，但对角同色的那两种不行。<bookmark mark='b'/>一个包含两个绿点的半平面，也包含它"
        "们之间的线段；另一侧包含红色的线段；两条对角线相交，所以没有哪条直线行得通。<bookmark mark='c'/>如果有一个点位于另外三个点构成的三角形内部，就把它涂成与其他点不同的颜色，同样的论证依然适用。"
        "<bookmark mark='d'/>任何四个点都落入这两种情形之一：这是1921年的 Radon 定理，它在 d 维中能把任意 d 加2个点一分为二。<bookmark mark='e'/>所以半平面的 V"
        "C 维是3，d 维中半空间的是 d 加1，矩形的是4。<bookmark mark='f'/>下界只需要一个被打散的点集；上界则必须击败每一个点集。",
    "Behind the VC dimension is a function. <bookmark mark='a'/>":
        "VC 维背后是一个函数。<bookmark mark='a'/>增长函数对每个 m，计算这个类在任意 m 个点上最多能产生多少种标注。<bookmark mark='b'/>一个能打散一切的类，会沿着2的 m "
        "次方走，就是那条灰线：在10个点时是1024。<bookmark mark='c'/>半平面，一种标注一种标注地数下来，一直跟着它走到3个点，也就是 VC 维，然后就落了下去，落到92，也就是 m 的平方减 m"
        " 加2。<bookmark mark='d'/>黄色曲线，是我们马上要只从 VC 维出发证明的界。越过 VC 维之后，增长只是多项式的。",
    "Norbert Sauer and Saharon Shelah proved independently, in":
        "Norbert Sauer 和 Saharon Shelah 在1972年各自独立地证明了其中的原因。<bookmark mark='a'/>如果 VC 维是 d，增长函数至多是大小不超过 d 的子集的个数。"
        "<bookmark mark='b'/>这里是正方形四个角的14种标注，按前三个点分组。这些行构成 H1；加了框的行，也就是在最后一个点的两种标签下都出现的那些，构成 H2。14等于8加6。"
        "<bookmark mark='c'/>用归纳法。H1 至多打散 d 个点；H2 至多打散 d 减1个，否则这个类就会打散那个点集再加上最后一个点。<bookmark mark='d'/>把两个界都写成求和，"
        "<bookmark mark='e'/>帕斯卡法则把它们加成 m 的那个求和：当 m 至少是 d 时，至多是 e m 除以 d 的 d 次方。一个多项式。",
    "The growth function can now replace the class size, through":
        "现在，借助一个影子样本，增长函数就可以取代类的大小。<bookmark mark='a'/>再抽 m 个点。如果一个一致的假设，真实误差超过 epsilon，那么它至少以二分之一的概率，在 epsilon m "
        "除以2个影子点上出错。所以坏事件的概率，至多是关于2 m 个点的某个事件的两倍。<bookmark mark='b'/>在这些点上，这个类至多有“2 m 处的增长函数”那么多种行为；而在两半之间随机交换，把一个"
        "假设的全部 k 个错误都藏进影子那一半的概率，至多是2的负 k 次方。<bookmark mark='c'/>令它等于 delta 并求解，<bookmark mark='d'/>Sauer 和 Shelah "
        "就把增长函数变成 d 乘以一个对数。<bookmark mark='e'/>对矩形，d 是4：这个界是成立的，但比我们的测量高出一个数量级。它只知道 VC 维。",
    "Together these give the fundamental theorem of PAC learning,":
        "把这些合起来，就是 PAC 学习的基本定理，由 Blumer、Ehrenfeucht、Haussler 和 Warmuth 在1989年明确写出。<bookmark mark='a'/>对二分类，四件事是等价的"
        "：VC 维有限、一致收敛、能被任何样本误差最小化器学会，以及不可知可学习。<bookmark mark='b'/>所需的样例数被确定下来：存在完美假设时，大约是 d 除以 epsilon；不存在时，是 d 除以"
        " epsilon 的平方。<bookmark mark='c'/>反方向是“没有免费的午餐”论证：如果这个类能打散2 m 个点，一个见过其中 m 个的学习器，对其余的点一无所知。"
        "<bookmark mark='d'/>某个目标会迫使误差至少是八分之一，而且概率至少是七分之一。VC 维无限时，多少数据都不够。",
    # ------------------------------------------------------------------ s04_margins
    "Chapter three. Margins and Rademacher complexity.":
        "第三章：间隔与 Rademacher 复杂度。",
    "The oldest learning machine is the one Part 7 put inside a":
        "最古老的学习机器，就是第7部分放进处理器里的那一个。<bookmark mark='a'/>罗森布拉特（Frank Rosenblatt）1958年的感知机，用一个加权和的符号来预测。它预测错时，就把这个样例连"
        "同它的符号加到权重上；否则什么也不做。<bookmark mark='b'/>看它在一些能被某条直线分开的点上运行。每犯一次错，黄线就摆动一次，直到没有点落在错误的一侧。<bookmark mark='c'/>"
        "是什么控制着错误的次数？不是点的个数，也不是维数，而是间隔：最佳分隔线周围那条空白带的宽度，相对于数据的半径而言。<bookmark mark='d'/>Albert Novikoff 在1962年证明，感知机"
        "无论运行多久，至多犯 R 除以 gamma 的平方次错。",
    "The proof watches two quantities. Assume every example has":
        "证明盯住两个量。假设每个样例的长度至多是 R，并且有一个单位向量 w 星以间隔 gamma 把它们分开。<bookmark mark='a'/>第一，进展。一次错误加上 y x，它在 w 星上的投影至少是 ga"
        "mma，所以 k 次错误之后，投影至少是 k gamma：线性增长。<bookmark mark='b'/>第二，长度。长度的平方增加2倍的 y 乘以 w 点乘 x，这在出错时不是正的，再加上至多 R 的平方。"
        "所以 k 次错误之后，长度至多是根号 k 乘以 R：平方根增长。<bookmark mark='c'/>投影永远不会超过长度。<bookmark mark='d'/>所以 k gamma 至多是根号 k 乘 R"
        "，k 至多是 R 除以 gamma 的平方。<bookmark mark='e'/>线性增长不可能长久地待在平方根之下：半径为1、间隔为十分之一时，至多100次错误。",
    "Our instrument tested the claim. <bookmark mark='a'/> It":
        "我们的仪器检验了这个说法。<bookmark mark='a'/>它在单位球面上放了2000个点，全都与一个随机超平面至少相距十分之一，维数分别是2、10、100和1000，并运行感知机，直到完整地过一遍都不出"
        "错。<bookmark mark='b'/>错误次数是4、23、38和34：都在 Novikoff 的100之下，而且从100维到1000维基本持平。<bookmark mark='c'/>半空间的 VC 界随"
        "维数增长；间隔界只看几何。<bookmark mark='d'/>第7部分的分支预测器在硬件中运行这个更新，但分支历史很少是可分的，所以那里这个保证并不成立，只能测量错误率。",
    "Margins need a complexity measure that is not a count.":
        "间隔需要一种不是计数的复杂度度量。Rademacher 复杂度问的是：这个类能把纯噪声拟合得多好。<bookmark mark='a'/>为每个样本点抛一枚均匀的硬币，得到随机标签，找出与它们最吻合的假设，再对"
        "所有硬币结果把这个吻合程度取平均。<bookmark mark='b'/>对直线上的阈值，最好的阈值也只能抓住每次抽取中噪声的一部分。<bookmark mark='c'/>一个能打散样本的类，能完美匹配每一次"
        "抽取；它什么都能解释，所以它对真实数据的拟合什么也证明不了。<bookmark mark='d'/>定理，按 Peter Bartlett 和 Shahar Mendelson 2002年的形式：以1减 del"
        "ta 的概率，每个假设的真实误差至多是它的样本误差，加上2倍的 Rademacher 复杂度，再加上一个根号 m 分之一量级的项。<bookmark mark='e'/>Massart 引理用增长函数来界定这个"
        "复杂度，所以 VC 界随之而来；而有了间隔，它可以小得多。",
    "For linear classifiers with bounded weights, the Rademacher":
        "对权重有界的线性分类器，Rademacher 复杂度五行就能算出。<bookmark mark='a'/>在长度至多为 lambda 的所有权重上，w 与带符号的点之和的点积的上确界，"
        "<bookmark mark='b'/>由柯西–施瓦茨不等式，等于 lambda 乘以这个和的长度。<bookmark mark='c'/>Jensen 不等式把期望移进一个平方根里。"
        "<bookmark mark='d'/>把平方展开，交叉项消失，因为独立的符号互不相关，<bookmark mark='e'/>剩下的就是 lambda R 除以根号 m。维数从未出现。"
        "<bookmark mark='f'/>Vladimir Koltchinskii 和 Dmitry Panchenko 在2002年把它变成了一个间隔界：真实误差至多是间隔小于 rho 的样本点所占的比例，加"
        "上一个 R 除以 rho、再除以根号 m 的项。<bookmark mark='g'/>R 除以 rho 的平方扮演了维数的角色：恰好就是 Novikoff 的那个量。<bookmark mark='h'/>支"
        "持向量机，来自1995年的 Corinna Cortes 和 Vapnik，直接最大化这个间隔。提升法，我们接下来会看到，也是如此。",
    # ------------------------------------------------------------------ s05_boosting
    "Chapter four. Boosting.":
        "第四章：提升法。",
    "A strong learner reaches any error with any confidence. A":
        "强学习器能以任意的置信度达到任意小的误差。弱学习器只承诺，在每个分布上，误差比二分之一低一点点。<bookmark mark='a'/>这里没有哪一条单独的规则能行：400个点，圆内是绿色。我们的弱学习器画的是"
        "决策树桩，在一个坐标上取一个阈值。<bookmark mark='b'/>权重相等时，最好的树桩说“处处都在外面”，在占百分之28.5的绿点上出错。<bookmark mark='c'/>改变权重，最好的树桩就"
        "变了：现在它切在大约0.6处，加权误差是三分之一。<bookmark mark='d'/>Michael Kearns 和 Leslie Valiant 问过：弱学习真的更弱吗？1990年，Robert Sch"
        "apire 证明了并非如此。",
    "Freund and Schapire's AdaBoost, from 1995, made boosting":
        "Freund 和 Schapire 1995年的 AdaBoost，让提升法变得实用。<bookmark mark='a'/>给每个样例保持一个权重，一开始都相等。每一轮，向弱学习器要一条加权误差小的规则，"
        "<bookmark mark='b'/>并给它一票，误差越小，这一票越重。<bookmark mark='c'/>然后重新加权：它判错的样例，权重乘大，其余的乘小，再把权重归一化。"
        "<bookmark mark='d'/>看1轮、2轮、5轮和20轮之后：远离圆的容易的点缩小了，权重堆积到边界上，最重的那个点承担了它最初份额的大约4.5倍。<bookmark mark='e'/>最终的分类器"
        "是一次加权多数投票。",
    "Freund and Schapire proved that the training error falls":
        "Freund 和 Schapire 证明，训练误差指数式地下降。<bookmark mark='a'/>把更新展开：每个最终权重，是 e 的负 y F 次方，F 是加权投票，再除以 m 和各归一化因子的乘积。"
        "<bookmark mark='b'/>在一个训练错误上，y F 不是正的，所以 e 的负 y F 次方至少是1，于是训练误差至多是 e 的负 y F 次方的平均。<bookmark mark='c'/>最终权"
        "重之和是1，所以这个平均就是各归一化因子的乘积。<bookmark mark='d'/>用 AdaBoost 的投票权，每个归一化因子是2乘以根号下 epsilon 乘以1减 epsilon。"
        "<bookmark mark='e'/>误差为二分之一减去优势 gamma 时，它等于根号下1减4 gamma 平方，至多是 e 的负2 gamma 平方次方。<bookmark mark='f'/>所以训练误"
        "差至多是 e 的负的2倍优势平方和次方。<bookmark mark='g'/>在我们的圆上，它在第57轮第一次达到零，从第108轮起一直保持为零。",
    "Freund and Schapire also showed that boosting is a game.":
        "Freund 和 Schapire 还证明了，提升法是一场博弈。<bookmark mark='a'/>做一个矩阵，每个样例一行，每条弱规则一列，规则判对的地方是绿色。提升器在行上挑一个分布；弱学习器用最好的一"
        "列来回应。<bookmark mark='b'/>弱可学习性说，总有某一列拥有2 gamma 的优势。<bookmark mark='c'/>于是冯·诺依曼的极小极大定理给出各列的一个加权投票，它在每一行上都以"
        "2 gamma 的间隔判对。<bookmark mark='d'/>AdaBoost 的重新加权，就是第23部分的乘性权重，在行上运行：看权重移向上一条被选中的规则判错的那些行。它的投票趋近于极小极大的那一个。",
    "Then came a surprise. <bookmark mark='a'/> Training error is":
        "接着出现了一个意外。<bookmark mark='a'/>从第108轮起，训练误差永久为零，而经典直觉说，更多的轮次只会增加复杂度，所以测试误差应该上升。<bookmark mark='b'/>它没有：在之后"
        "的200轮里，它一直徘徊在百分之3附近。<bookmark mark='c'/>解释来自1998年的 Schapire、Freund、Peter Bartlett 和 Wee Sun Lee，那就是间隔：归一化"
        "的投票把一个样例判对得有多果断。这里是5轮、20轮、100轮和300轮之后的训练间隔：在每个点都已判对很久之后，提升法还在不断把最小的间隔往上推。<bookmark mark='d'/>他们的定理用小于 the"
        "ta 的训练间隔所占的比例，加上一个与弱规则的 VC 维和 theta 有关的项，来界定测试误差，而与轮数无关。",
    "The same mechanism is boosting's weakness. <bookmark":
        "同一个机制也是提升法的弱点。<bookmark mark='a'/>把百分之5的标签翻转。每一条合理的规则都会把某个翻转过的点判错，所以它的权重一轮又一轮地被乘大。<bookmark mark='b'/>到第2"
        "0轮，那23个被翻转的点，占数据不到百分之6，却握有百分之18的权重。<bookmark mark='c'/>在同样带噪声的测试标签上，测试误差在第27轮最低，然后慢慢爬升，因为提升法记住了这些错误。"
        "<bookmark mark='d'/>补救的办法是提前停止，或者缩小每一票；Jerome Friedman 2001年的梯度提升，把这个想法推广到任意损失。AdaBoost 让 Freund 和 Schapi"
        "re 获得了2003年的哥德尔奖。",
    # ------------------------------------------------------------------ s06_online
    "Chapter five. Learning online.":
        "第五章：在线学习。",
    "Now drop the distribution. An adversary picks each example,":
        "现在把分布去掉。一个对手挑选每个样例，我们预测它的标签，然后看到真相，并统计错误的次数。<bookmark mark='a'/>假设 N 个假设中有一个是完美的。减半算法保留那些仍然一致的假设，用它们的多数来预"
        "测。一次错误意味着多数错了，所以至少有一半被扔掉，<bookmark mark='b'/>而真正的那个永远不会被扔掉。<bookmark mark='c'/>所以错误至多有以2为底 N 的对数那么多次：对102"
        "4个阈值，是10次。<bookmark mark='d'/>在随机样例上，它在200轮里犯了2次错。<bookmark mark='e'/>一个总是问幸存者中间位置的对手，能逼出全部10次。"
        "<bookmark mark='f'/>Nick Littlestone 在1988年证明，一个类最好的错误界是一个数，也就是它的 Littlestone 维。对整条直线上的阈值，它是无限的，尽管它们的 VC 维是1。",
    "Usually no expert is perfect. <bookmark mark='a'/>":
        "通常没有哪位专家是完美的。<bookmark mark='a'/>Littlestone 和 Manfred Warmuth 的加权多数算法，发表于1994年：一开始每位专家的权重都是1，用加权投票来预测，并把"
        "每位说错的专家的权重减半。<bookmark mark='b'/>如果算法出错，至少一半的权重投错了票而被减半，所以总权重至多降到原来的四分之三。<bookmark mark='c'/>最好的专家犯了 m 次错"
        "，仍然握有二分之一的 m 次方。<bookmark mark='d'/>取对数：错误至多大约是最好专家错误次数的2.4倍，再加上以2为底 N 的对数。没有哪个确定性的规则能做得好很多，因为对手可以让它每一轮都错"
        "。所以我们引入随机。",
    "Freund and Schapire's Hedge, from 1997, plays expert i with":
        "Freund 和 Schapire 1997年的 Hedge，以正比于权重的概率采用专家 i，并把每个权重乘以 e 的负 eta 乘以该专家损失次方。遗憾就是它的期望损失减去最好专家的损失。盯住总权重的对数。"
        "<bookmark mark='a'/>从下方看：总权重至少是最好专家的权重。<bookmark mark='b'/>从上方看：每一轮，由霍夫丁引理，这个对数下降 eta 乘以我们的期望损失，上下相差 eta "
        "平方除以8。<bookmark mark='c'/>把各轮加起来，<bookmark mark='d'/>把两者放在一起，<bookmark mark='e'/>选 eta 为8 log N 除以 T 的平方根"
        "：遗憾至多是 T log N 除以2的平方根。<bookmark mark='f'/>平均到每一轮，它趋于零。这又是第23部分的乘性权重。",
    "Hedge against twenty experts with random losses for two":
        "让 Hedge 对付20位损失随机的专家，进行2000轮，其中一位比其余的略好一些。<bookmark mark='a'/>虚线是这个 eta 下的保证，最终达到54.7。"
        "<bookmark mark='b'/>测得的遗憾在 Hedge 寻找最好专家时攀升，然后在30.7处变平。<bookmark mark='c'/>在这么随机的损失上，跟随领先者做得还要好：9。"
        "<bookmark mark='d'/>但对手可以毁掉它：两位专家的损失交替出现，于是领先者总是即将输掉的那一位。跟随领先者几乎每一轮都输，而每位专家只各输一半的轮次，它的遗憾线性增长。",
    "Could a cleverer algorithm beat root T? No. <bookmark":
        "更聪明的算法能打败根号 T 吗？不能。<bookmark mark='a'/>取两位专家，每一轮抛一枚均匀的硬币来决定哪一位输。<bookmark mark='b'/>无论我们怎么下，平均每轮都输二分之一：一共"
        " T 除以2。<bookmark mark='c'/>但运气更好的那位专家，输掉的是 T 除以2，减去专家1的计数游荡出去的距离。<bookmark mark='d'/>这是一个随机游走；这里有10条。它的平均"
        "距离大约是 T 除以2 pi 的平方根，所以每个算法都要承受大约0.4倍根号 T 的遗憾。<bookmark mark='e'/>有 N 位专家时，同样的想法给出 Hedge 自己的那个 T log N 除以2"
        "的平方根：它的常数无法再改进。",
    "The experts are one case of a larger game. <bookmark":
        "专家问题是一场更大博弈的一个特例。<bookmark mark='a'/>每一轮我们选一个点，然后对手揭示一个凸的损失。Martin Zinkevich 在2003年证明，第23部分的梯度下降在这里也行得通：逆"
        "着这一轮的梯度走一步，再投影回允许的集合。<bookmark mark='b'/>这里的损失是一些抛物线，它们的中心四处跳动，而我们的点追着它们跑。<bookmark mark='c'/>设 D 是集合的直径，"
        "G 是梯度的一个上界，遗憾至多是 D 平方除以2 eta，加上 eta G 平方 T 除以2；<bookmark mark='d'/>取最好的 eta，就是 D G 根号 T。"
        "<bookmark mark='e'/>而且在线可以变成批量：把训练集一次一个样例地喂进去，再对下过的各个点取平均。由凸性，这个平均点的期望风险，至多比最好的高出遗憾除以 T。",
    # ------------------------------------------------------------------ s07_bandits
    "Chapter six. Bandits.":
        "第六章：老虎机。",
    "Herbert Robbins posed this problem in 1952. <bookmark":
        "Herbert Robbins 在1952年提出了这个问题。<bookmark mark='a'/>一排老虎机，每台以自己隐藏的概率付钱。每一轮我们拉一根拉杆，只看到它的回报。要找到最好的拉杆，我们必须探索；要"
        "赚钱，我们必须利用。<bookmark mark='b'/>度量是遗憾：一直拉最好的拉杆能赚到的，减去我们赚到的。<bookmark mark='c'/>按拉杆分组，它就是每根拉杆的差距乘以我们拉它的次数。"
        "<bookmark mark='d'/>我们的四根拉杆付钱的概率分别是0.5、0.45、0.4和0.3。<bookmark mark='e'/>第44部分的 A/B 测试在固定的时间里均匀地探索，然后定下来，为"
        "每一次拉较差的拉杆付出代价。老虎机算法则边走边调整。",
    "The first strategy is optimism. <bookmark mark='a'/> For":
        "第一种策略是乐观。<bookmark mark='a'/>对每根拉杆，保持平均回报，再加上一个随着它被拉而缩小的加分：2 log t 除以它被拉次数的平方根。拉指标最高的那根，指标就是它合理范围内的最好情形。"
        "<bookmark mark='b'/>由霍夫丁不等式，真实均值比平均值高出 epsilon 的概率至多是 e 的负2 n epsilon 平方次方。<bookmark mark='c'/>有了这个加分，指标低"
        "于真实值的概率至多是 t 的负4次方。<bookmark mark='d'/>看一次示意性的运行。差的拉杆的柱子随着被尝试而缩短，直到够不着最好拉杆的柱子；在那之后，它们被尝试的频率，只跟 log t 的增长一样快。",
    "Peter Auer, Nicolò Cesa-Bianchi and Paul Fischer proved in":
        "Peter Auer、Nicolò Cesa-Bianchi 和 Paul Fischer 在2002年证明，这个指标，UCB1，遗憾只像 log T 那样增长。<bookmark mark='a'/>设想一根"
        "差的拉杆，比最好的低一个差距 delta。<bookmark mark='b'/>它的平均值至多比它的均值高 w，而它的指标又加上一个 w。<bookmark mark='c'/>如果我们拉了它，它的指标就胜过"
        "了最好拉杆的指标，而后者高于 mu 星。所以 mu i 加2 w 达到了 mu 星，除非发生罕见的失败。<bookmark mark='d'/>求解：至多拉8 log T 除以 delta 平方次。"
        "<bookmark mark='e'/>乘以各个差距，再为失败加上一个常数。<bookmark mark='f'/>对我们的拉杆，5000轮下来，这大约是2400，而实测是159：成立，但很松。",
    "The second strategy is older. William Thompson proposed it":
        "第二种策略更古老。William Thompson 在1933年提出了它，心里想的是医学治疗。<bookmark mark='a'/>为每根拉杆的均值保持一个后验：在均匀先验下，就是一个由它的成功和失败次数确定"
        "的贝塔分布。试得多的拉杆，分布窄；很少试的，分布宽。<bookmark mark='b'/>每一轮，从每个后验中抽一个猜测，拉猜测最高的那根。<bookmark mark='c'/>于是每根拉杆被拉的概率，恰好"
        "等于在已有数据下它是最好拉杆的概率，所以不确定的拉杆仍然有机会。<bookmark mark='d'/>2012年，人们证明了它对这类拉杆达到最优的速率。",
    "Here are the three strategies on our arms, averaged over a":
        "这里是三种策略在我们的拉杆上的表现，对100次各5000轮的运行取平均。<bookmark mark='a'/>ε-贪心每20轮随机探索一轮，并为此永远付出代价：它的遗憾最终是线性的。"
        "<bookmark mark='b'/>UCB1 和汤普森采样弯了下来。<bookmark mark='c'/>任何人最多能弯到什么程度？Tze Leung Lai 和 Robbins 在1985年证明，任何在"
        "每个问题上都表现良好的策略，都必须把每根差的拉杆，拉大约 log T 除以它的硬币与最好硬币之间的散度那么多次。<bookmark mark='d'/>对我们的拉杆，这是17.4 log T。UCB1 在159"
        "，位于它之上；汤普森采样大约在50，在这个 T 下位于它之下，而定理允许这样：它讲的是 T 增长时的速率。",
    "Why can nobody beat log T? <bookmark mark='a'/> Take a bad":
        "为什么没人能打败 log T？<bookmark mark='a'/>取一根付钱概率为0.45的差拉杆。在另一个世界里，它付0.5，是最好的。拉20次之后，两个世界看起来差不多；"
        "<bookmark mark='b'/>拉200次之后，它们分开了；拉2000次之后，就清清楚楚了。<bookmark mark='c'/>把它们混淆的概率，像 e 的负 n 乘以它们的散度次方那样下降。"
        "<bookmark mark='d'/>在第二个世界里混淆，每一轮都要损失一份，所以这个概率必须大约是 T 分之一，于是 n 至少是 log T 除以散度。<bookmark mark='e'/>而如果对手把差"
        "距设成根号下 K 除以 T，T 轮就找不到最好的拉杆：遗憾大约是根号 K T。<bookmark mark='f'/>老虎机算法如今运行着推荐和广告分配，代价是失去一个更干净的实验。",
    # ------------------------------------------------------------------ s08_limits
    "Chapter seven. What cannot be learned.":
        "第七章：什么学不会。",
    "Data is rarely what limits learning. <bookmark mark='a'/>":
        "限制学习的很少是数据。<bookmark mark='a'/>规模为 s 的电路至多有2的 s log s 量级次方个，所以第一章的界说，多项式个样例就够了。麻烦在于时间：找到一个能拟合的假设。"
        "<bookmark mark='b'/>取那些由三个“与”组成的“或”的公式，就像这一个。Leonard Pitt 和 Valiant 在1988年证明，找到一个与数据一致的这种公式是 NP 难的。"
        "<bookmark mark='c'/>但把“或”分配到各个“与”上：同一个函数就是若干子句的“与”，每个子句从每一项中取一个文字。<bookmark mark='d'/>三个文字的子句数量不多，而 Valia"
        "nt 的消去算法能在多项式时间内学会它们。这个类是容易的；难的是它自己的表示。<bookmark mark='e'/>所以真正的限制，必须无论学习器输出什么都成立。",
    "Michael Kearns and Leslie Valiant found such limits in":
        "Michael Kearns 和 Leslie Valiant 在密码学中找到了这样的限制；期刊版本发表于1994年。<bookmark mark='a'/>取一个公钥密码系统。任何拿到公钥的人都能加密随机比特"
        "，所以任何人都能制作带标签的样例：一个密文，以及藏在里面的那个比特。<bookmark mark='b'/>目标概念就是解密函数。<bookmark mark='c'/>如果某一类函数能计算解密，那么这个类的一"
        "个学习器，喂给它这些样例，就会返回一个假设，它解密一个新的挑战密文，效果比瞎猜好。这就攻破了这个密码系统。<bookmark mark='d'/>所以，如果 RSA 或因数分解是困难的，就没有高效的算法能学会小"
        "的布尔公式或有限自动机，无论它输出什么。<bookmark mark='e'/>而如果第29部分的伪随机函数存在，小电路即使通过提问也学不会。",
    "Kearns also defined a gentler kind of learner. <bookmark":
        "Kearns 还定义了一种更温和的学习器。<bookmark mark='a'/>统计查询学习器从不查看单个样例；它请求关于样例及其标签的某个函数的平均值，并得到一个误差在容差 tau 以内的结果。这样的学习器"
        "经得起带噪声的标签，而在平均损失上做梯度下降就是其中一种。<bookmark mark='b'/>现在让标签是一个未知的 k 比特集合的奇偶性。不同的奇偶函数彼此正交。<bookmark mark='c'/>任"
        "何查询都可以拆成一个不管标签的部分，和一个与标签相关的部分，而只有后者依赖于那个集合。<bookmark mark='d'/>由 Bessel 不等式，这些相关性的平方和至多是1，所以每次查询至多能对 tau "
        "平方分之一个集合提供信息。<bookmark mark='e'/>其余的集合看起来完全一样，所以找到那个集合至少需要 tau 平方乘以 n 选 k 次查询。",
    "Here are sparse parities of three bits among n, from four":
        "这里是 n 个比特中3个比特的稀疏奇偶，来自400个随机样例。<bookmark mark='a'/>没有哪个单独的比特与标签的相关性超出抽样噪声。<bookmark mark='b'/>对三比特集合的搜索，至"
        "多要尝试 n 选3个，而它确实试了：在 n 等于22时，1540个中试了1508个。<bookmark mark='c'/>然而奇偶性对代数来说很容易。每个样例都是二元域上的一个线性方程，而第52部分的高斯消元"
        "，在这个域上进行，用大约2 n 个样例，不到1毫秒就能解出它。奇偶性是可学的，只是不能靠统计。<bookmark mark='d'/>翻转几个标签，消元就失效了。带噪声的奇偶学习被认为是困难的；已知最好的算法，"
        "出自 Avrim Blum、Adam Kalai 和 Hal Wasserman，需要2的 n 除以 log n 次方的时间。<bookmark mark='e'/>这又是第7部分的奇偶分支：没有哪个单独的历史"
        "比特能预测它。",
    "So the map of what can be learned has three walls. <bookmark":
        "所以，可学之物的地图有三道墙。<bookmark mark='a'/>外墙是统计的：VC 维无限的类，无论多少数据都学不会。<bookmark mark='b'/>在它里面，是计算之墙。小的公式、自动机和电路只"
        "需要很少的样例，但学会它们就会攻破密码学。<bookmark mark='c'/>再往里，是统计查询之墙。合取式和带间隔的半空间位于它里面，经得起噪声；<bookmark mark='d'/>奇偶函数位于两墙之"
        "间，只能用代数学会，而一个错误的标签就能把它毁掉。Avrim Blum 和同事在1994年证明，这道墙由一个数决定，也就是统计查询维：一个类包含多少个几乎正交的函数。",
    # ------------------------------------------------------------------ s09_overparam
    "Chapter eight. More parameters than data.":
        "第八章：参数比数据还多。",
    "Here is the experiment of the hook again, with both errors.":
        "这又是开场的那个实验，这次两种误差都画了出来。50个带噪声的样例；一个线性模型，用的是200个高斯特征中的前 p 个，用最小二乘拟合，解有很多个时选最小的那个。<bookmark mark='a'/>训练误差随"
        " p 增大而下降，从 p 等于50开始就是零，只差第4部分浮点数的舍入：模型插值了数据，连噪声一起。<bookmark mark='b'/>测试误差在阈值处升到52，<bookmark mark='c'/>然后"
        "下降，在200个参数时降到0.78，低于最小模型的1.03。Mikhail Belkin、Daniel Hsu、Siyuan Ma 和 Soumik Mandal 在2019年把它命名为双下降。在这个简单的设定"
        "里，根本没有第一个谷：一本经典教科书会停在最小的模型上，错过远处那个更好的。",
    "Why is this a puzzle? <bookmark mark='a'/> Chapter three":
        "为什么这是个谜题？<bookmark mark='a'/>第三章用一个类拟合纯噪声的能力来衡量它：随机的符号，以及这个类与它们所能达到的最好相关性。<bookmark mark='b'/>一个参数至少和样例一样"
        "多的模型，能拟合任何标注，所以这个复杂度取到它的最大值，1。<bookmark mark='c'/>于是界变得毫无用处：测试误差至多是训练误差，零，加1，再加更多。<bookmark mark='d'/>Chi"
        "yuan Zhang 和同事在2017年证明，真实的网络就是这样。标准的图像网络在随机标签的 CIFAR-10 上拟合到零训练误差，然后当然只能以瞎猜的水平预测；而在真实标签上，同样的网络泛化得很好。"
        "<bookmark mark='e'/>所以答案不在类里。它在于算法挑中了哪一个插值解。",
    "Past the threshold there are more unknowns than equations.":
        "越过阈值，未知数就比方程多。<bookmark mark='a'/>画出最小的情形：一个样例，两个参数。这条直线上的每一个点都恰好拟合这个样例；一般地，解构成一个 p 减 n 维的平坦子空间。"
        "<bookmark mark='b'/>我们的实验挑长度最小的那个。从原点开始让一个圆变大，直到碰到这条直线。<bookmark mark='c'/>它碰到的地方，半径与直线垂直，也就是沿着样例本身的方向。一般"
        "地，最小范数解是 X 的各行的一个组合。<bookmark mark='d'/>把它代入方程并求解：X 转置，乘以 X 乘 X 转置的逆，再乘以 y。这就是伪逆，也就是我们实验里用的那一个。",
    "Nobody trains a network by calling the pseudo-inverse. But":
        "没有人通过调用伪逆来训练网络。但他们确实运行梯度下降。<bookmark mark='a'/>在平方误差上，每一步减去 X 转置乘以残差：这是各行的一个组合。<bookmark mark='b'/>从零出发，你"
        "就永远不会离开行空间。<bookmark mark='c'/>看：黄色路径笔直地沿着样例的方向前进，停在直线上最小的那个解处。<bookmark mark='d'/>从别处出发，它就落在直线上的别处。所以从零出"
        "发，极限既拟合数据，又位于行空间中，而只有一个解同时做到这两点。<bookmark mark='e'/>算法自己选中了最小范数：这是一种隐式偏好。对可分数据上的逻辑损失，梯度下降朝着最大间隔的方向前进，又是第三章的间隔。",
    "Why does the error explode at the threshold, and fall after":
        "为什么误差在阈值处爆炸，又在它之后下降？<bookmark mark='a'/>拟合出的参数与真实参数之差，来自一个偏差，以及作用在噪声上的伪逆，而这里的噪声包括模型看不到的那些特征。"
        "<bookmark mark='b'/>参数少于样例时，噪声项的平均值是噪声方差乘以 p 除以 n 减 p 减1：这是一个逆 Wishart 矩阵的均值。<bookmark mark='c'/>参数更多时，把同"
        "样的论证转置过来，得到 n 除以 p 减 n 减1。<bookmark mark='d'/>当 p 接近 n 时，两者都会爆炸，这时 X 是方阵，它最小的奇异值接近零：这是第52部分的病态。"
        "<bookmark mark='e'/>对一个范数为1的目标画出的公式曲线，在峰的两侧都与我们的测量吻合。越过峰之后，多余的方向分担了噪声，而最小的解把它压了下去。",
    # ------------------------------------------------------------------ s10_compression
    "Chapter nine. Learning is compression.":
        "第九章：学习就是压缩。",
    "William of Ockham said not to multiply entities beyond":
        "奥卡姆的威廉（William of Ockham）说，如无必要，勿增实体。学习理论把它变成了一个定理。<bookmark mark='a'/>用一种无前缀码描述每个假设，就像这棵树的叶子。Kraft 不等式说，"
        "2的负码长次方加起来至多是1。<bookmark mark='b'/>所以按这些比例分配失败概率 delta：短的假设分到大的一份。<bookmark mark='c'/>按第一章的论证，误差超过 epsilo"
        "n 的假设在 m 个样例上存活的概率是 e 的负 epsilon m 次方；令它等于这个假设的那一份。<bookmark mark='d'/>求解：它的误差至多是它以比特计的长度乘以 log 2，加上 delt"
        "a 分之一的对数，全部除以 m。联合界总共至多花掉 delta。Anselm Blumer、Andrzej Ehrenfeucht、David Haussler 和 Manfred Warmuth 在1987年"
        "把它称为奥卡姆剃刀。短的描述能够泛化，不是因为大自然是简单的，而是因为短的描述很少。",
    "Nick Littlestone and Manfred Warmuth turned this around in":
        "Nick Littlestone 和 Manfred Warmuth 在1986年把它反了过来。<bookmark mark='a'/>200个点，由一个隐藏的矩形标注。<bookmark mark='b'/>"
        "只保留4个：最极端的那几个正例点。只用它们，重建最紧的方框，它就把全部200个点都标对了。这是一个大小为4的压缩方案。<bookmark mark='c'/>它为什么能泛化？固定保留哪4个位置。方框只依赖于这几"
        "个点，所以另外196个，就是它恰好拟合上的新样例。<bookmark mark='d'/>对至多 m 的 k 次方种选择取联合界，<bookmark mark='e'/>求解：k log m 加上 delta "
        "分之一的对数，除以 m 减 k。<bookmark mark='f'/>这里它是0.123。方框的真实误差是0.017；这个界是安全的，而且与第一章的界同一个量级。",
    "Compression explains chapter three's puzzle too. <bookmark":
        "压缩也解释了第三章的谜题。<bookmark mark='a'/>只保留感知机判错的那些样例，按它遇到的顺序。只在这些样例上运行它：它按同样的顺序犯同样的错误，最后得到同样的权重，而这组权重拟合所有的点。"
        "<bookmark mark='b'/>所以感知机是一个压缩方案，它的大小就是它的错误次数，至多是间隔平方分之一，这里是100，无论维数是多少。<bookmark mark='c'/>在2000个点上，VC 维"
        "爬升到1000，<bookmark mark='d'/>而这个方案从来不需要超过38个点。<bookmark mark='e'/>压缩界一直保持在大约七分之一以下，即使在1000维，那里没有任何 VC 界能说出"
        "什么。起决定作用的是间隔，而不是维数，因为大的间隔意味着短的描述。",
    "There is a third way to say the same thing, as a message.":
        "还有第三种方式说同一件事：把它当作一条消息。<bookmark mark='a'/>接收者有这200个点，需要它们的标签。<bookmark mark='b'/>一个一个地发，就是200比特。"
        "<bookmark mark='c'/>按频率编码，200个中有41个正例，大约146比特。<bookmark mark='d'/>但发送方框那4个点的下标，大约31比特，接收者就能重建方框，每个标签随之而来。"
        "把这31比特喂给奥卡姆的界，它给出0.121：这正是压缩界的答案，只是被看作一条消息。<bookmark mark='e'/>Jorma Rissanen 1978年的最小描述长度原则，选择这样的假设：描述它所"
        "需的比特，加上描述它的例外所需的比特，总和最小。<bookmark mark='f'/>这就是第21部分那些压缩器的交易：声称的每一条规律，都必须用比特为自己买单。",
    "Put the bounds side by side. <bookmark mark='a'/> The finite":
        "把这些界并排放在一起。<bookmark mark='a'/>第一章的有限类，奥卡姆剃刀的比特，压缩方案保留的点，以及第二章的 VC 维。<bookmark mark='b'/>每一个说的都是同一件事：误差像复"
        "杂度乘以一个对数、再除以样例数那样下降。<bookmark mark='c'/>压缩蕴含学习。那么学习是否蕴含压缩，而且方案能小到 VC 维那么小？Littlestone 和 Warmuth 在1986年提出了"
        "这个问题，它至今悬而未决。那就是前沿。每一种度量，归根到底，数的都是学习器必须记住的东西。",
    # ------------------------------------------------------------------ s11_frontier
    "Chapter ten, the frontier. Is learning exactly compression?":
        "第十章，前沿。学习恰好就是压缩吗？",
    'f"A learner that generalizes must, in some sense,':
        "一个能泛化的学习器，在某种意义上一定压缩了它的数据。<bookmark mark='a'/>这里有{c['m']}个点，由一个隐藏的矩形标注。<bookmark mark='b'/>只保留其中4个：最左、最右、"
        "最低和最高的正例点。<bookmark mark='c'/>穿过这4个点的最紧的方框，把{c['m']}个点中的每一个都标注得{ok}。Nick Littlestone 和 Manfred Warmuth 把这"
        "叫作样本压缩方案，并在1986年证明，大小为 k 的方案给出的学习界，很像 VC 维为 k 时的界。<bookmark mark='d'/>Warmuth 猜想，每个 VC 维为 d 的类，都有一个大小与 d "
        "成正比的方案。2016年，Shay Moran 和 Amir Yehudayoff 证明，大小为 d 的指数的方案总是存在。线性大小是否总是可能，至今仍未解决。",
    "The newest puzzle comes from language models. <bookmark":
        "最新的谜题来自语言模型。<bookmark mark='a'/>在提示里给它看几个输入–输出样例，一个训练好的模型就能预测一个新输入的答案，而它的权重没有任何改变。<bookmark mark='b'/>202"
        "2年，Shivam Garg 和同事用由线性回归问题组成的提示训练 Transformer，发现它们与最小二乘的表现相当；还有一些构造表明，注意力可以执行梯度下降的步骤。<bookmark mark='c'/>"
        "理论仍然缺少的，是一个界，说明这在什么时候行得通，以及一个提示需要多少样例。<bookmark mark='d'/>双下降的第二次下降，也就是良性过拟合，对像我们这样的线性模型，现在已经理解得很好；对深度网络，"
        "只理解了一部分。",
    "Open problems. <bookmark mark='a'/> A bound on the":
        "未解决的问题。<bookmark mark='a'/>一个关于深度网络泛化的界，在人们实际使用的规模上是非空的。<bookmark mark='b'/>一个关于提示能教会什么的理论。"
        "<bookmark mark='c'/>当一些标签被翻转时，奇偶性能否被高效地学会，而现代密码学的很大一部分都假设这是不可能的。<bookmark mark='d'/>还有，让带结构的老虎机问题的上界和下界相互"
        "匹配。<bookmark mark='e'/>这一部分的研究题是 Warmuth 的：每个 VC 维为 d 的类，是否都有一个大小与 d 成正比的压缩方案？",
    # ------------------------------------------------------------------ s12_outro
    "What we built in this part. PAC learning, where a finite":
        "我们在这一部分搭建了什么。PAC 学习，其中一个有限类需要的样例数，与它大小的对数成正比。VC 维、Sauer–Shelah 引理，以及基本定理：一个类可学习，恰好当它的 VC 维有限。间隔，它界定了感知机的错"
        "误次数，并解释了提升法，无论维数是多少。对抗一个对手的在线学习，其中遗憾像平方根那样增长；还有在探索与利用之间取得平衡的老虎机算法。像稀疏奇偶这样的问题，没有哪个统计学习器能快速找到。还有双下降与压缩。贯穿始终"
        "的是一个想法：学习是可能的，恰好当假设简单到足以被数据确定下来。",
    "Where this comes back. Part 58 asks what programs mean, and":
        "它们会在哪里再出现。第58部分问程序意味着什么，以及如何证明两个程序是相同的。第59部分研究许多台机器一起能计算什么。第60部分搭建训练和运行学习模型的硬件。而第61部分问如何诚实地衡量一个结果，并回到这个系列"
        "与《人工智能，从零搭建》之间的那座桥。",
    "In practice. Hold out data the model never sees, and never":
        "在实践中。留出模型从未见过的数据，永远不要在测试集上调参。当模型已经足够灵活时，更多的数据通常胜过更聪明的模型。用间隔、权重衰减和提前停止来控制容量。在线选择用老虎机算法；汤普森采样是一个强有力的默认选择。而当"
        "一个结果好得令人难以置信时，先去找数据泄漏。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整的解答在这一部分的笔记里。随时可以在任何一道上暂停。第五道是一道动手题：实现两个老虎机算法，并把它们的遗憾与 Lai–Robbins 速率作比较。最后一道标了星号，是一道研究题：是否每个 VC 维"
        "为 d 的类，都能被压缩成与 d 成正比个数的点。",
    "Next time, Part 58: semantics. What does a program mean?":
        "下一次，第58部分：语义。一个程序意味着什么？三个答案：机器所走的步骤，程序所指称的数学对象，以及它所遵守的定律，还有一个能免费写出代码性质的定理。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
PHRASES.update({"correctly": "正确", "incorrectly": "错误"})
