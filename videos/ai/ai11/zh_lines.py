"""Chinese narration for ai11: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第11部分：一路下山'

CHAPTERS = {
    'Hook': '下山赛跑',
    'GradientDescent': '1. 推导梯度下降',
    'Momentum': '2. 重球法与涅斯捷罗夫',
    'SGD': '3. 随机梯度',
    'Temperature': '4. 噪声即温度',
    'EdgeOfStability': '5. 稳定性边缘',
    'Adam': '6. AdaGrad、RMSProp、Adam',
    'Decay': '7. 权重衰减不是L2',
    'Natural': '8. 自然梯度与K-FAC',
    'Shampoo': '9. Shampoo与SOAP',
    'Muon': '10. 推导Muon',
    'NewtonSchulz': '11. 牛顿–舒尔茨迭代',
    'Race': '12. 一场公平的比赛',
    'Schedule': '13. 学习率调度与河谷',
    'ScheduleFree': '14. 不用调度',
    'Stability': '15. 让训练保持稳定',
    'Frontier': '16. 2024到2026年的优化器竞赛',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"Every model in this series learns by walking downhill':
        "本系列的每一个模型，都是沿着自己的损失一路下山学出来的。但怎么走，差别非常大。<bookmark mark='a'/>这是一条"
        "有名的弯曲山谷，罗森布罗克山谷，白点是它的最低处。四个下山的人从同一个地方出发，每人都用从{len(r['lrs'])}"
        "个候选里挑出的最好步长。<bookmark mark='b'/>普通的梯度下降、重球法、Adam，还有Lion。<bookmark mark='c'/>"
        "在{steps}步之内，{SAY.get(first, first)}最先到达，用了{reach[first]}步。{said1}这一部分讲的就是为什么。",
    "f'{SAY.get(last, last).capitalize()} never quite does":
        "{SAY.get(last, last).capitalize()}始终没能到达：它还在山谷底部慢慢爬。",
    "f'{SAY.get(last, last).capitalize()} takes":
        "{SAY.get(last, last).capitalize()}用了{reach[last]}步，一路沿着谷底慢慢爬。",

    'The idea is old.':
        "这个想法很古老。1847年，奥古斯丁·柯西在求解行星轨道的方程时，提出沿着梯度的反方向走：最速下降法。"
        "<bookmark mark='a'/>1951年，赫伯特·罗宾斯和萨顿·门罗证明，沿着带噪声的估计走，只要步长以恰当的速度缩小，"
        "仍然会收敛。<bookmark mark='b'/>1964年，鲍里斯·波利亚克加上了动量：一个重球。<bookmark mark='c'/>1983年，"
        "尤里·涅斯捷罗夫找到了使用动量的、可以证明是最快的方法。<bookmark mark='d'/>1986年，反向传播让网络的梯度"
        "变得便宜，此后二十五年，网络都用带动量的随机梯度下降来训练。<bookmark mark='e'/>接着出现了给每个权重各自"
        "步长的方法：2011年的AdaGrad，<bookmark mark='f'/>2012年的RMSProp，它从没写成论文发表，只是杰弗里·辛顿"
        "网课里的一张幻灯片，<bookmark mark='g'/>以及2014年的Adam，此后十年几乎训练了一切。<bookmark mark='h'/>2018年，"
        "Shampoo开始对整个矩阵做预条件。<bookmark mark='i'/>2024年，一个公开基准AlgoPerf公平地测量了各路选手，"
        "一个新的优化器Muon在一场速通比赛里出现。<bookmark mark='j'/>2025年，它的一个版本MuonClip训练了Kimi K2，"
        "一个有一万亿参数的模型，<bookmark mark='k'/>而在2026年，DeepSeek也用Muon训练了它的第四代模型。",

    'This is Part 11 of AI, Built.':
        "这是《人工智能，从零搭建》的第11部分。<bookmark mark='a'/>这一部分讲：梯度下降为什么收敛，收敛得多快；"
        "动量；小批量的噪声起什么作用；训练为什么总在失稳的边缘；Adam是怎样构造的，权重衰减为什么不是看上去的那样；"
        "能看见整个矩阵几何的优化器，最后到Muon；在我们自己的模型上让它们公平比赛；学习率调度；以及业界怎样防止"
        "超大规模的训练崩掉。",

    # ------------------------------------------------------------------ GradientDescent
    'Chapter one. Gradient descent, derived.': '第1章。推导梯度下降。',
    'In 1847, Augustin Cauchy wanted to solve':
        "1847年，奥古斯丁·柯西想求解天文学里的方程，提出了一个通用方法：看误差往哪个方向下降得最快，就往那边走一步。"
        "这就是梯度下降。<bookmark mark='a'/>要说清它有多快，我们需要损失的两个数。<bookmark mark='b'/>如果损失的曲率"
        "从不超过L，它就是L-光滑的：在每一点，它都位于一个曲率为L的碗的下方。<bookmark mark='c'/>如果它的曲率从不"
        "小于μ，它就是μ-强凸的：它位于一个曲率为μ的碗的上方。<bookmark mark='d'/>两者之比κ叫作条件数：山谷在一个"
        "方向上比另一个方向陡多少倍。",
    'Now the derivation.':
        "现在来推导。<bookmark mark='a'/>走一步。因为损失在曲率为L的碗下方，这一步让损失至少下降η乘以梯度的平方，"
        "再减去L乘η平方除以2的惩罚。<bookmark mark='b'/>这个界允许的最好步长是η等于L分之1，它保证损失下降梯度平方"
        "除以2L。<bookmark mark='c'/>强凸性说：离谷底还远的时候，梯度不可能很小，它的平方至少是2μ乘以差距。"
        "<bookmark mark='d'/>把两者合起来：每一步都把差距缩小到原来的1减μ除以L倍。<bookmark mark='e'/>不断重复，"
        "差距就按几何级数下降，每步乘以1减κ分之1。<bookmark mark='f'/>所以需要的步数和条件数成正比。一个方向比另一个"
        "方向陡一千倍的山谷，大约需要多一千倍的步数。",
    '"If the loss is convex but not strongly convex':
        "如果损失是凸的，但不是强凸的，它下面的碗可能是平的，保证就弱了：差距像k分之1那样下降，k是步数。"
        "<bookmark mark='a'/>这是梯度下降在一个二次函数上的表现，它的曲率从1一直降到百万分之一，虚线是这个界。{said1}",
    "<bookmark mark='b'/> The measured gap stays under the bound":
        "<bookmark mark='b'/>测出的差距每一步都在界的下方，正如定理所要求的；在这对数坐标上，它的斜率是幂律的斜率，"
        "而不是几何衰减。",
    "<bookmark mark='b'/> The measured gap should stay under":
        "<bookmark mark='b'/>测出的差距本应一直在界的下方；这里并非处处如此，说明最小的数值上有舍入误差。",
    'f"Check it. Quadratic valleys in fifty dimensions':
        "来验证一下。五十维的二次山谷，条件数从1到1000，梯度下降的步长取L分之1。<bookmark mark='a'/>它需要的步数，"
        "在对数坐标上沿着一条斜率为{slope:.2f}的直线上升：{said2}虚线是最坏情形；这些山谷要好一点，因为只有一个方向是"
        "最慢的。<bookmark mark='b'/>到了后期，只剩下那个最慢的方向，{said3}",
    'close to one, in proportion to kappa, as derived.':
        "接近1，和κ成正比，与推导一致。",
    'not the slope of one the worst case predicts.':
        "不是最坏情形预测的斜率1。",
    "f'error shrinks per step by exactly the derived factor":
        "误差每一步恰好按推导出的因子1减κ分之1缩小，精确到小数点后三位：κ等于1000时，是{rate[i1000]:.4f}。",
    "f'error shrinks per step by {rate[i1000]:.4f}":
        "κ等于1000时，误差每一步缩小为{rate[i1000]:.4f}倍，推导值是{rpred[i1000]:.4f}。",
    'Pause and predict. On a valley curving thirty times':
        "停下来预测一下。在一个方向比另一个方向陡三十倍的山谷里，L分之1的步长是安全的。如果步长刚刚超过L分之2，"
        "会怎样？<bookmark mark='a'/>安全的步长沿着长轴滑下去。<bookmark mark='b'/>大的步长在陡的那个方向上一次比一次"
        "冲得更远，最后被甩出山谷。沿着曲率为λ的方向，每一步把距离乘以1减ηλ；一旦超过λ分之2，这个因子就小于负1。"
        "第5章会回到这条边缘。",
    "So: gradient descent's speed is set by the condition number":
        "所以：梯度下降的速度由条件数决定，病态的山谷走得很慢。接下来是动量，它把κ变成它的平方根。",

    # ------------------------------------------------------------------ Momentum
    'Chapter two. The heavy ball, and Nesterov.': '第2章。重球法，与涅斯捷罗夫方法。',
    'In 1964 Boris Polyak, in Moscow':
        "1964年，在莫斯科的鲍里斯·波利亚克问：怎样让梯度下降快起来？他用物理来回答：给下山的人加上质量。"
        "<bookmark mark='a'/>每一步都加上上一步的β倍。<bookmark mark='b'/>在陡的方向上，相邻的两步方向相反，记忆把"
        "它们抵消了；在又长又缓的方向上，每一步都朝同一个方向，记忆把它们累加起来。<bookmark mark='c'/>一个重球沿着"
        "山谷滚下去，而不是在两壁之间来回撞。",
    'Why does it work, and how fast? On a quadratic':
        "它为什么有效，又有多快？在二次函数上，山谷的每个方向是独立的。<bookmark mark='a'/>沿着曲率为λ的方向，更新"
        "是关于最近两个位置的递推。<bookmark mark='b'/>试试z的幂，z就必须满足一个二次方程。<bookmark mark='c'/>当它的"
        "根是复数时，位置会螺旋式地向内收缩，而且不管λ是多少，每一步都恰好缩小为β的平方根倍。<bookmark mark='d'/>"
        "所以选择η和β，让μ到L之间的每一个曲率都落进这个螺旋区：让区间的两端正好在它的边上。<bookmark mark='e'/>解出来，"
        "β的平方根等于根号κ减1，除以根号κ加1。<bookmark mark='f'/>这大约是1减根号κ分之2：步数现在随条件数的平方根增长。"
        "一千变成了大约三十。",
    '"In 1983 Yurii Nesterov, also in Moscow':
        "1983年，同样在莫斯科的尤里·涅斯捷罗夫只改了一件事：不在你现在的位置求梯度，而在动量即将把你带到的位置求。"
        "<bookmark mark='a'/>有了这个前瞻，加速在每一个光滑的凸函数上都有保证，不只在二次函数上：差距像k平方分之1"
        "那样下降，而不是k分之1。{said1}<bookmark mark='c'/>而阿尔卡迪·涅米罗夫斯基和大卫·尤丁早已证明：在最坏情形下，任何只用"
        "梯度的方法都不可能做得更好：涅斯捷罗夫的速度是最优的。",
    "f\"<bookmark mark='b'/> On Chapter 1's convex quadratic it stays under its bound":
        "<bookmark mark='b'/>在第1章的凸二次函数上，它一直在自己的界下方，{len(ks):,}步之后，它比梯度下降近了"
        "{ratio:.0f}倍。",
    "f\"<bookmark mark='b'/> On Chapter 1's convex quadratic, after":
        "<bookmark mark='b'/>在第1章的凸二次函数上，{len(ks):,}步之后，它比梯度下降近了{ratio:.0f}倍。",
    'f"Back to Chapter 1\'s fifty-dimensional valleys':
        "回到第1章的五十维山谷，这次加上动量。<bookmark mark='a'/>梯度下降的斜率是{sg:.2f}。<bookmark mark='b'/>"
        "重球法和涅斯捷罗夫方法的斜率是{sh:.2f}和{sn:.2f}：{said2}κ等于1000时，这是{it_g:,}步，对{it_h:,}步和{it_n:,}步。<bookmark mark='c'/>在后期，重球法每一步把误差缩小为"
        "{rh:.4f}倍，推导值是{rhp:.4f}；涅斯捷罗夫方法是{rn:.4f}倍，推导值是{rnp:.4f}。<bookmark mark='d'/>提醒一句。"
        "重球法的保证只对二次函数成立：在别的凸函数上，有它永远打转的例子。有证明的是涅斯捷罗夫的形式。",
    'close to one half, the square root of kappa.': "接近二分之一，也就是κ的平方根。",
    "well below gradient descent's.": "远低于梯度下降。",
    'So momentum is memory':
        "所以动量就是记忆：它抵消来回折返，累加坡度，把κ变成它的平方根。但到现在为止，每一个梯度都是精确的。"
        "真实的训练只能估计它。",

    # ------------------------------------------------------------------ SGD
    'Chapter three. Stochastic gradients.': '第3章。随机梯度。',
    'The loss of a model is an average over its training examples':
        "一个模型的损失是对所有训练样本的平均，它的梯度也是。要精确地算出来，每走一步都得把全部数据过一遍；真实的"
        "模型要在几万亿个词上训练。<bookmark mark='a'/>换个办法：只在一小批随机样本上取平均。<bookmark mark='b'/>"
        "平均来说，这个估计完全正确，它的噪声随批量变大而缩小：协方差像B分之1那样下降。<bookmark mark='c'/>1951年，"
        "北卡罗来纳的两位统计学家赫伯特·罗宾斯和萨顿·门罗问：沿着这种带噪声的估计走，什么时候仍然能到达答案？",
    'f"Here\'s a real loss with two weights':
        "这是一个只有两个权重的真实损失：第6部分的逻辑回归，用两个词频来分辨奥斯丁和狄更斯。<bookmark mark='a'/>"
        "用上全部{n}页训练数据，每一步都径直下坡。<bookmark mark='b'/>每步随机取十六页，路径会摇晃，但每一步的代价"
        "小了{n // 16}倍。<bookmark mark='c'/>每次只取一页，路径很狂野，但它仍然奔向谷底。",
    '"Keep a constant step, and the walker never quite stops':
        "保持步长不变，下山的人就永远停不下来：它在谷底附近一直抖动，形成一团云。<bookmark mark='a'/>罗宾斯和门罗的"
        "答案是：让步长缩小，但不要太快。步长之和必须是无穷大，这样还能走到任何地方；步长平方之和必须有限，这样"
        "收集到的噪声总量有限。<bookmark mark='b'/>像k分之1那样缩小的步长两条都满足。<bookmark mark='c'/>测量结果：{said1}",
    "f'with the constant step, the squared distance stalls at about":
        "用恒定步长，距离的平方停在大约{end_c:.3f}；用缩小的步长，它一直下降，{K:,}步后降到{end_d:.4f}。",
    "f'with the constant step the squared distance stalls near":
        "用恒定步长，距离的平方停在{end_c:.3f}附近；缩小的步长在{K:,}步后到达{end_d:.3f}，还没有低于它。",
    'This noisy method became the workhorse':
        "这个带噪声的方法成了神经网络的主力。<bookmark mark='a'/>1986年那篇反向传播的论文就已经用动量训练。"
        "<bookmark mark='b'/>1998年，杨立昆、莱昂·博图和同事把实践中的手艺写了下来：每个样本或每一小批就更新一次，"
        "打乱数据，把输入归一化。<bookmark mark='c'/>2012年，开启深度学习热潮的AlexNet，用的是动量0.9的随机梯度下降，"
        "每当进展停滞，就把步长除以10。",
    'So a random batch gives a gradient that is right on average':
        "所以随机批量给出的梯度平均来说是对的，而且便宜，代价是噪声。用恒定步长，训练最终停在谷底周围的一团云里。"
        "这团云有多大？噪声只是代价吗？",

    # ------------------------------------------------------------------ Temperature
    'Chapter four. Noise as temperature.': '第4章。噪声即温度。',
    'How big is the cloud? Part five':
        "这团云有多大？第5部分的随机微分方程能回答。<bookmark mark='a'/>随机梯度下降的一步，就是真梯度的一步，加上"
        "这一批的噪声，协方差是Σ除以B。<bookmark mark='b'/>把步长η看成一小段时间dt。噪声项于是等于dt的平方根，乘以"
        "一个高斯变量，再乘以η除以B的平方根。<bookmark mark='c'/>这恰好是一个随机微分方程的一步欧拉格式：向下坡的推力，"
        "加上强度为η除以B的随机踢动。学习率和批量大小只通过它们的比值起作用。物理学家会把它叫作温度。",
    'f"Near the bottom the gradient is the Hessian times the distance':
        "在谷底附近，梯度等于黑塞矩阵乘以距离，这团云也不再变化：每走一步，它的协方差S进去是什么样，出来还是什么样。"
        "<bookmark mark='a'/>这就是关于S的一个方程。<bookmark mark='b'/>步长小的时候，它化简为H S加S H等于η除以B乘以"
        "噪声的协方差C。<bookmark mark='c'/>取迹：云的均方大小等于2B分之η，乘以H的逆乘C的迹。<bookmark mark='d'/>"
        "对我们这个两权重的损失，这个迹是{tr:.2f}，接近2，因为在对数损失的谷底，梯度的噪声和曲率几乎是同一个矩阵。",
    '"Measure it. Four learning rates, six batch sizes':
        "来测一测。四个学习率，六种批量大小，每种三个随机种子：二十四团云。<bookmark mark='a'/>把它们对着温度，"
        "也就是η除以B画出来，{said1}<bookmark mark='b'/>虚线是预测的平稳大小。{said2}",
    "f'they fall on one line, of slope {slope:.2f}":
        "它们落在同一条直线上，斜率是{slope:.2f}：学习率加倍、批量也加倍，云就一模一样。",
    "f'they rise with slope {slope:.2f}. '":
        "它们以斜率{slope:.2f}上升。",
    "f'Measured over predicted, every point is between":
        "测量值除以预测值，每个点都在{rlo:.2f}到{rhi:.2f}之间。",
    "f'Measured over predicted runs from":
        "测量值除以预测值，从{rlo:.2f}到{rhi:.2f}：这里线性的图景只是近似。",
    'This explains a rule practitioners found by experiment.':
        "这解释了实践者凭实验找到的一条规则。<bookmark mark='a'/>如果把批量乘以k，就把学习率也乘以k：温度不变，"
        "所以每单位进展的噪声也不变。2017年，Facebook的一个团队用它，再加上短暂的预热，用每批八千张图片的批量，在"
        "一小时内训练出了一个ImageNet分类器。<bookmark mark='b'/>对Adam来说，它要除以梯度的大小，同样的分析说应该"
        "乘以k的平方根。<bookmark mark='c'/>这条规则有极限。超过临界批量之后，噪声已经很小，更大的批量就不再能换来"
        "更少的步数。第12部分会测出这发生在哪里。",
    'f"Is the noise only a cost?':
        "噪声只是代价吗？<bookmark mark='a'/>回到那个真实的损失，批量大十六倍，云就窄了{sp1 / sp16:.1f}倍，接近16的"
        "平方根。<bookmark mark='b'/>现在想象一个又尖又窄的坑，旁边是一个宽阔的盆地。温度高的下山人待不住那个坑："
        "它会被踢出来，最后停在山谷宽的地方。<bookmark mark='c'/>2017年，尼蒂什·凯斯卡尔和同事发现，用很大批量训练"
        "的网络最后落在更尖锐的极小值里，泛化得更差。<bookmark mark='d'/>同一年，洛朗·丁和同事指出了其中的漏洞："
        "把一层放大、下一层缩小，网络计算的函数不变，锐度却变了。平坦是一个有用的图景，而不是定律。",
    'So stochastic gradient descent runs at a temperature':
        "所以随机梯度下降是在一个温度下运行的，这个温度就是η除以B，它决定训练最后停留的那团云有多大；保持这个比值"
        "不变，就是线性缩放规则。但步长本身最大能有多大？",

    # ------------------------------------------------------------------ EdgeOfStability
    'Chapter five. The edge of stability.': '第5章。稳定性边缘。',
    'Chapter one ended with a valley that threw the walker out.':
        "第1章结尾，有个山谷把下山的人甩了出去。原因在这里，用最简单的损失来看：一个曲率为λ的碗，步长为η。每一步"
        "把到谷底的距离乘以1减η乘λ。<bookmark mark='a'/>如果这个数在负1到1之间，步子会越来越小，最后停下来。"
        "<bookmark mark='b'/>如果η乘λ大于2，每一步都比上一步冲得更远，最后炸掉。所以梯度下降只能在曲率小于η分之2的"
        "地方保持稳定。",
    'The classical advice follows':
        "经典的建议由此而来：测出锐度，也就是最大的曲率，黑塞矩阵最大的特征值，然后选一个小于它分之2的步长。但训练"
        "会改变它脚下的地形。停下来预测一下：在一个真实的网络上，步长固定，训练过程中锐度会怎样变化？",
    '"Here is the answer, measured':
        "这是测出来的答案：第9部分的螺旋数据，用完整梯度在两种步长下训练，每四十步用幂迭代测一次锐度。"
        "<bookmark mark='a'/>它一直往上爬，{said1}<bookmark mark='b'/>把步长加倍，{said2}训练并不躲开稳定性边缘：它走到"
        "那里，就住在边缘上。杰里米·科恩和同事在2021年发现了这一点，谁都没有料到。",
    "f'and climbs, until it reaches two over eta, around step {fe:,}":
        "一直爬，大约在第{fe:,}步到达η分之2，然后就停在那里，在边缘上徘徊，而损失还在继续下降，只是不太平稳。",
    'and climbs, towards two over eta, while the loss keeps going down.':
        "一直朝着η分之2爬，而损失还在继续下降。",
    "f'the network settles at half the sharpness":
        "网络就停在一半的锐度上：中位数是{med[e1]:.1f}，η分之2是{2 / e1:.0f}。",
    "f'its sharpness settles near {med[e1]:.1f}":
        "它的锐度停在{med[e1]:.1f}附近，η分之2是{2 / e1:.0f}。",
    'Why? <bookmark mark=\'a\'/> While the sharpness is below two over eta':
        "为什么？<bookmark mark='a'/>锐度低于η分之2的时候，训练往往会让山谷变得更陡：渐进锐化。<bookmark mark='b'/>"
        "一旦越过边缘，下山的人就开始沿着最陡的方向来回弹跳，一次比一次远。<bookmark mark='c'/>但弹跳把它带到那个方向"
        "弯得不那么厉害的地方，锐度又降了回来。<bookmark mark='d'/>2022年，亚历克斯·达米安、伊尚·尼查尼和杰森·李"
        "证明，这两种效应恰好在边缘上平衡。梯度下降自己调节着自己的曲率。",
    'The edge moves with the optimizer.':
        "边缘随优化器而移动。<bookmark mark='a'/>有了动量β，一步能承受更大的曲率，最多到2加2β，除以η。"
        "<bookmark mark='b'/>Adam也住在一条边缘上：经过它的缩放之后测得的曲率，升到η分之38，这正是动量为0.9时的同一条"
        "规则。杰里米·科恩和同事与谷歌的研究者一起，在2022年测出了这一点。<bookmark mark='c'/>这也是训练为什么要从"
        "小步开始的原因之一，第13章会再讲到。",
    "So the step size doesn't have to fit the landscape":
        "所以不必让步长去适应地形：地形会自己来适应步长。接下来，是给每个权重各自一个步长的优化器。",

    # ------------------------------------------------------------------ Adam
    'Chapter six. AdaGrad, RMSProp, Adam.': '第6章。AdaGrad、RMSProp、Adam。',
    'One learning rate for every weight is a strange choice.':
        "所有权重共用一个学习率，是个奇怪的选择。有些权重的梯度很大，有些很小；这就是第1章的条件数，一个方向一个方向"
        "地看。<bookmark mark='a'/>2011年，约翰·杜奇、埃拉德·哈赞和约拉姆·辛格提出了AdaGrad：给每个权重记下它梯度"
        "平方的累计和，用它的平方根去除这个权重的步长。<bookmark mark='b'/>一个很少出现的词，累计和很小，所以一旦出现，"
        "就迈一大步。<bookmark mark='c'/>问题在于：这个和只增不减，于是每个步长都像时间的平方根分之1那样缩小，长时间"
        "的训练会慢得像爬。",
    'The fix came from an online course.':
        "解决办法来自一门网课。<bookmark mark='a'/>2012年，在杰弗里·辛顿的Coursera神经网络课程的一讲里，一张幻灯片"
        "提出了RMSProp：把AdaGrad不断增长的累计和，换成一个会遗忘的滑动平均，旧值的十分之九加上新梯度平方的十分之一，"
        "再除以它的平方根。<bookmark mark='b'/>它从没写成论文。多年来，研究论文引用的都是一张讲义幻灯片。",
    'In 2014 Diederik Kingma and Jimmy Ba put the two ideas together.':
        "2014年，迪德里克·金马和吉米·巴把这两个想法合在一起。<bookmark mark='a'/>记下梯度的滑动平均m：这是动量。"
        "<bookmark mark='b'/>记下梯度平方的滑动平均v：这是RMSProp。<bookmark mark='c'/>两者都校正从零起步带来的偏差，"
        "这一步待会儿就推导，<bookmark mark='d'/>然后按平均方向除以平均平方的根来走。他们把它叫作Adam，用默认参数，它在"
        "此后十年里训练了深度学习的大部分模型。",
    'f"Why the corrections?':
        "为什么要校正？<bookmark mark='a'/>从零开始把平均展开：m是到目前为止所有梯度的加权和。<bookmark mark='b'/>"
        "如果梯度的均值稳定，m的期望就是这个均值乘以一个几何级数，<bookmark mark='c'/>也就是1减β的t次方。一开始，"
        "m偏向零，除以这个因子就消除了偏差。<bookmark mark='d'/>这是我们字符模型的一个权重，前六十步的真实梯度：未校正的"
        "平均从零附近起步，校正后的从第一步起就跟着梯度走。<bookmark mark='e'/>校正对v最要紧，它的记忆长达一千步。"
        "如果都不校正，第一步会是η的{raw:.2f}倍；校正之后，恰好是η。",
    'f"Look at Adam\'s limit.':
        "看看Adam的极限。把两个记忆都关掉，让ε趋于零：梯度除以它自己的大小，就只剩下它的符号。每个权重都恰好移动η，"
        "向上或向下。Adam是一种平滑过的符号下降。<bookmark mark='a'/>这是我们模型隐藏矩阵里每个权重移动的距离，以η为"
        "单位。第一步，偏差校正让Adam恰好成为符号下降：{f1:.0%}的权重移动了η。{said1}",
    "f\"<bookmark mark='b'/> Later, the typical move is far smaller":
        "<bookmark mark='b'/>后来，典型的移动小得多：第100步是{m100:.2f}个η，第1000步是{m1000:.2f}。梯度带着噪声，"
        "它们的平均m比均方根小得多，Adam的一步变成了梯度的符号，再按信噪比缩放。",
    "f\"<bookmark mark='b'/> Later the typical move stays large":
        "<bookmark mark='b'/>后来，典型的移动依然很大，第100步是{m100:.2f}个η：梯度一步接一步地保持着符号。",
    'That limit became an optimizer.':
        "这个极限后来变成了一个优化器。<bookmark mark='a'/>2023年，谷歌的一个团队让计算机在程序空间里搜索更新规则，"
        "胜出的那个，经过化简，就是Lion：每个权重按动量和新梯度的混合的符号移动，<bookmark mark='b'/>然后更慢地更新"
        "动量。<bookmark mark='c'/>它每个权重只存一个数，而不是Adam的两个；因为每一步都是满幅，它需要更小的学习率和"
        "更大的权重衰减。它会参加我们第12章的比赛。",
    'So Adam is momentum divided by a running size':
        "所以Adam就是动量除以一个滑动的大小，再校正起步的偏差；在极限下它就是符号下降：当每个权重各自最多只能移动η时，"
        "最陡的那一步。接下来，是一个多年来用法上的隐蔽错误。",

    # ------------------------------------------------------------------ Decay
    'Chapter seven. Weight decay is not L2.': '第7章。权重衰减不是L2。',
    "There are two ways to keep a network's weights small.":
        "有两种办法让网络的权重保持小。<bookmark mark='a'/>在损失上加一个惩罚，λ除以2乘以权重的平方大小：L2正则化。"
        "<bookmark mark='b'/>对它走一步梯度，惩罚项贡献λ乘以θ。<bookmark mark='c'/>整理一下，就是：先把每个权重缩小为"
        "1减ηλ倍，再走普通的一步。这就是权重衰减。<bookmark mark='d'/>对普通的梯度下降，两者完全一样，所以几十年来，"
        "这两个词一直混着用。",
    'Adam breaks that equivalence.':
        "Adam打破了这种等价。<bookmark mark='a'/>把L2惩罚放进Adam，惩罚的拉力也要经过Adam除以梯度均方根的那一步。"
        "梯度大的权重几乎不衰减，梯度很小的权重反而衰减得很厉害：恰好和我们想要的相反。<bookmark mark='b'/>2017年，"
        "伊利亚·洛希洛夫和弗兰克·胡特指出了这一点，提出把衰减直接作用在权重上，放在Adam之外：AdamW。它成了"
        "Transformer时代的默认优化器。",
    '"Does it matter? A test where regularization should matter':
        "这重要吗？做一个正则化应该起作用的测试：一个较小的字符模型，只见过五万个字符的训练文本，一遍又一遍地看。"
        "<bookmark mark='a'/>左边是AdamW，四个学习率乘六种衰减强度；右边是带L2惩罚的Adam，用同一组学习率。越亮越好。"
        "<bookmark mark='b'/>两边各自最好的设置，再用三个随机种子重跑：{verdict}<bookmark mark='v'/>{said1}"
        "<bookmark mark='e'/>{etxt}<bookmark mark='c'/>{said2}",
    ' Both beat no decay at all': "两者都胜过完全不衰减，所以这里它确实在起正则化的作用。",
    ' Neither beats no decay by much': "两者都没有比不衰减好多少：即使在这里，它的正则化作用也很弱。",
    ' Both bests are at our largest learning rate': "两边最好的设置都在我们最大的学习率上，所以更大的学习率也许对两者都有帮助。",
    " And in AdamW's grid the best decay strength barely moves":
        "在AdamW的网格里，最好的衰减强度几乎不随学习率移动，这正是解耦所承诺的：两个旋钮可以分开调。",
    " In AdamW's grid the best decay strength still moves":
        "在AdamW的网格里，最好的衰减强度仍然随学习率移动：起作用的是两者的乘积。",
    'f"AdamW\'s best is {gap:.3f} bits better':
        "AdamW最好的结果比最好的L2惩罚好{gap:.3f}比特，它的三个种子全都胜过L2的三个种子。",
    'f"AdamW\'s best is ahead by {gap:.3f} bits on average':
        "AdamW最好的结果平均领先{gap:.3f}比特，但种子之间有重叠：在这个模型上，差别在运气的范围之内。",
    'f"here the best L2 penalty does as well as AdamW':
        "这里最好的L2惩罚和AdamW一样好，甚至更好，领先{-gap:.3f}比特：在这个小模型上，解耦没有带来好处。",
    "'Watch the held-out loss during training, seed zero. '":
        "看看训练过程中的留出损失，种子0。{said3}<bookmark mark='b'/>{said4}在用新鲜数据训练的大语言模型里，它做的是另一件事，"
        "第15章会把它测出来。",
    "f\"<bookmark mark='a'/> Without decay, the model starts to memorize":
        "<bookmark mark='a'/>不加衰减，模型开始背下它那五万个字符，留出损失从最低点回升了{rise0:.2f}比特。",
    "<bookmark mark='a'/> Even without decay, the held-out loss keeps falling to the end.":
        "<bookmark mark='a'/>即使不加衰减，留出损失也一直降到最后。",
    'With decay, it ends lower.': "加了衰减，它最后更低。",
    'With decay, it ends no lower on this stretch of text.': "加了衰减，在这段文本上它最后并没有更低。",
    'So in Adam, an L2 penalty and weight decay are different things':
        "所以在Adam里，L2惩罚和权重衰减是两回事，业界采用的是解耦的版本。接下来，一个更深的问题：究竟该怎样衡量"
        "一步的大小？",

    # ------------------------------------------------------------------ Natural
    'Chapter eight. The natural gradient, and K-FAC.': '第8章。自然梯度，与K-FAC。',
    'Gradient descent has a hidden assumption.':
        "梯度下降有一个隐藏的假设。<bookmark mark='a'/>拿第3章那个两权重的损失，把第二个权重写成原来的四分之一："
        "模型一样，损失一样，只是一根坐标轴换了个标签。梯度下降现在走了一条不同的路，因为最陡的方向取决于你怎样衡量"
        "一步。<bookmark mark='b'/>一般地，在尺子M下最陡的一步，是负的M的逆乘以梯度。<bookmark mark='c'/>梯度下降"
        "就是取M为单位矩阵：每个权重都一样算，不管它代表什么。",
    'In 1998 Shun-ichi Amari proposed the ruler':
        "1998年，甘利俊一提出了一把不在乎标签的尺子：按一步对模型预测的改变有多大来衡量它。<bookmark mark='a'/>对很小"
        "的一步，第1部分的KL散度在新旧预测之间是一个二次型，<bookmark mark='b'/>它的矩阵就是费希尔信息：模型自身得分"
        "函数的协方差，标签按模型自己的预测来抽取。<bookmark mark='c'/>在这把尺子下最陡的一步，就是自然梯度：负的η乘以"
        "F的逆再乘以g。<bookmark mark='d'/>在我们这个两权重的损失上，两种写法下的两条路径是同一条。它看见的是模型，"
        "而不是坐标。",
    'f"The catch is size.':
        "难点在于规模。费希尔矩阵每个权重有一行一列：我们那个小小的螺旋网络是{P}乘{P}，十亿权重的模型就是十亿的十亿个"
        "元素。<bookmark mark='a'/>2015年，詹姆斯·马滕斯和罗杰·格罗斯找到了一条捷径。一层的权重梯度是一个外积：输出"
        "端的梯度乘以它的输入。<bookmark mark='b'/>所以它在费希尔矩阵里的那一块，是两个外积的克罗内克积的期望。"
        "<bookmark mark='c'/>假设输入和梯度相互独立，它就分解成两个小矩阵的克罗内克积：输入的二阶矩A，和输出梯度的G。"
        "<bookmark mark='d'/>克罗内克积可以逐个因子求逆，所以一层的自然梯度就变成G的逆，乘以它的梯度，再乘以A的逆。"
        "这就是K-FAC：克罗内克分解的近似曲率。",
    'f"Race them on part nine\'s spirals':
        "让它们在第9部分的螺旋数据上比一比：梯度下降、Adam、K-FAC和精确的自然梯度，每个都用五个学习率里最好的那个，"
        "各跑三个种子。<bookmark mark='a'/>一百步之后，顺序是{SAY[order[0]]}，然后是{SAY[order[1]]}、"
        "{SAY[order[2]]}和{SAY[order[3]]}。<bookmark mark='b'/>右边是网络在训练中的判断：梯度下降的图和自然梯度的图，"
        "在相同的步数上。{said1}<bookmark mark='c'/>但自然梯度的每一步都要解一个方程组，每个权重一个方程。在真实的模型上这"
        "不可能，所以实用的版本，K-FAC和下一章的Shampoo，都去近似它。{ecomment}",
    'The natural gradient carves out the two spirals almost at once.':
        "自然梯度几乎一下子就把两条螺旋分开了。",
    'f" {SAY[edges[0]].capitalize()}\'s best rate was at the end of its grid':
        "{SAY[edges[0]].capitalize()}最好的学习率在网格的尽头，所以它可能还能再好一点。",
    'So the natural gradient measures a step by what it does to the model':
        "所以自然梯度按一步对模型的作用来衡量它，而K-FAC用每层两个小矩阵让它变得负担得起。接下来是Shampoo，它的"
        "两个矩阵只从梯度本身得来。",

    # ------------------------------------------------------------------ Shampoo
    'Chapter nine. Shampoo, and SOAP.': '第9章。Shampoo，与SOAP。',
    'Adam and AdaGrad treat each weight on its own.':
        "Adam和AdaGrad把每个权重分开对待。完整版的AdaGrad要用一个矩阵来做预条件，这一层的每个权重都对应它的一行"
        "一列，谁也存不下。<bookmark mark='a'/>2018年，谷歌的维尼特·古普塔、托默·科伦和约拉姆·辛格利用了一层的形状。"
        "<bookmark mark='b'/>改为保存两个小的累计和：G乘G转置，对应各行；G转置乘G，对应各列。<bookmark mark='c'/>"
        "他们证明，那个大矩阵被这两者的克罗内克积所界住。<bookmark mark='d'/>所以从两侧给梯度矩阵做预条件，用L和R的"
        "负四分之一次方。他们把它叫作Shampoo：<bookmark mark='e'/>K-FAC的克罗内克技巧，两个因子都取自梯度本身。",
    'Here is a surprise hidden in Shampoo.':
        "Shampoo里藏着一个惊喜。把它的记忆关掉，让两个因子只来自当前的梯度。<bookmark mark='a'/>用第3部分的奇异值"
        "分解写出梯度。<bookmark mark='b'/>于是L的负四分之一次方和R的负四分之一次方，由同样的奇异向量构成，奇异值则"
        "变成负二分之一次方。<bookmark mark='c'/>乘出来，所有奇异值都消掉了：剩下的是U乘V转置，也就是把所有奇异值都"
        "设成1的梯度。杰里米·伯恩斯坦和莱克·纽豪斯在2024年指出了这一点。<bookmark mark='d'/>记住这个矩阵：它就是"
        "Muon的一步。",
    'Shampoo was hard to use.':
        "Shampoo很难用。<bookmark mark='a'/>负四分之一次方需要特征分解，很慢，所以只能每隔几步更新一次；两个因子"
        "条件很差，需要阻尼；它一步的大小也不好控制，所以实用的版本嫁接上Adam的大小，只保留Shampoo的方向。"
        "<bookmark mark='b'/>Meta和谷歌的工程师把它做成了实用的分布式Shampoo，2024年，它赢得了AlgoPerf的外部调参"
        "赛道。AlgoPerf这个基准，在固定的硬件上，计时训练算法在八个任务上达到目标所需的时间：它比基线快了大约百分之"
        "二十八，这已经算上了它每一步额外的开销。",
    'In 2024 a group at Harvard simplified it.':
        "2024年，哈佛的一个团队把它简化了。<bookmark mark='a'/>Shampoo的两个因子有各自的特征向量：一个对各行的旋转，"
        "一个对各列的旋转。<bookmark mark='b'/>把梯度旋转到这两组基里，在那里逐个坐标地跑普通的Adam，"
        "<bookmark mark='c'/>再把这一步旋转回来。旋转每隔几步更新一次，剩下的交给Adam。他们把它叫作SOAP，报告说在最大"
        "六亿六千万参数的语言模型上，达到AdamW的损失少用了四成以上的步数。原来，Shampoo很接近于在它自己的特征基里"
        "跑的一种廉价的Adam。SOAP也参加我们的比赛。",
    'So Shampoo preconditions a whole matrix':
        "所以Shampoo用两个小因子给整个矩阵做预条件，SOAP在它们的特征基里跑Adam，而没有记忆的Shampoo就是正交化的"
        "梯度。接下来，看看为什么这个矩阵是所有步子里最陡的那一步。",

    # ------------------------------------------------------------------ Muon
    'Chapter ten. Muon, derived.': '第10章。推导Muon。',
    'f"Adam treats every weight separately.':
        "Adam把每个权重分开对待。但一层的权重组成一个矩阵，而矩阵有结构：第3部分的奇异值。<bookmark mark='a'/>"
        "这是我们字符模型的一个真实梯度矩阵。少数几个方向占了主导：它{n}个奇异值里最大的十个，占了它平方大小的"
        "{top10:.0%}。沿着它走一步，主要是把这少数几个方向推得更远。<bookmark mark='b'/>2024年12月，凯勒·乔丹和"
        "合作者发表了Muon，此前它在训练一个小GPT的公开速通比赛里创了纪录。Muon把梯度的奇异值都换成1：每个方向都"
        "推同样的力度。",
    'Why set the singular values to one?':
        "为什么要把奇异值设成1？因为在正确的大小概念下，这是最陡的一步。<bookmark mark='p'/>一层把输入乘以W。"
        "一步最多能让输出相对于输入改变多少，就是这一步最大的拉伸：它的谱范数。这是矩阵天然的大小。"
        "<bookmark mark='q'/>想象一个矩阵对一圈方向做了什么。梯度把它拉成一个又长又扁的椭圆；Muon的一步让它保持是"
        "一个圆。<bookmark mark='a'/>在所有拉伸都不超过η的步子里，找一阶意义下让损失降得最快的那一步。"
        "<bookmark mark='b'/>把梯度写在它的奇异方向上。每一项最多只能被压低η乘以它的奇异值。<bookmark mark='c'/>"
        "而有一步能同时达到所有这些界：负的η乘以U乘V转置。",
    'This puts the optimizers of this part in one family.':
        "这把这一部分的优化器放进了同一个家族。<bookmark mark='a'/>按欧几里得长度限制一步，最陡的一步就是归一化的梯度。"
        "<bookmark mark='b'/>对每个权重分别限制，最陡的一步就是梯度的符号：Adam的极限，以及Lion。"
        "<bookmark mark='c'/>按矩阵最多能把一个向量拉伸多少来限制，最陡的一步就是U乘V转置：Muon。它们之间的差别，"
        "只是那把尺子。",
    'f"Muon in practice, as Moonshot AI scaled it up in 2025.':
        "实践中的Muon，是2025年月之暗面把它放大后的样子。<bookmark mark='a'/>对梯度保持动量，<bookmark mark='b'/>"
        "用五轮牛顿–舒尔茨迭代把前瞻的那一步正交化，这是下一章的内容，<bookmark mark='c'/>然后带着权重衰减走一步，"
        "乘以0.2再乘以较大那个维度的平方根。<bookmark mark='d'/>这个缩放让Muon一步的典型元素大约是0.2，正好是AdamW"
        "典型一步的大小，于是一个学习率可以两边通用。我们自己的Adam在第6章里，中位数权重移动了{med:.2f}个η。"
        "<bookmark mark='e'/>Muon只用于隐藏矩阵；嵌入、输出层和那些小向量，还是交给AdamW。",
    "So Muon is steepest descent when a matrix's step":
        "所以，当一个矩阵的一步按它最多能把向量拉伸多少来衡量时，Muon就是最速下降，它的一步就是把所有奇异值都设成1"
        "的梯度。精确计算需要SVD，在GPU上很慢。接下来，看Muon怎样绕开它。",

    # ------------------------------------------------------------------ NewtonSchulz
    'Chapter eleven. Newton': '第11章。牛顿–舒尔茨迭代。',
    'An SVD is slow on a GPU':
        "SVD在GPU上很慢，但矩阵乘法正是GPU最擅长的。<bookmark mark='a'/>所以先把梯度缩放到奇异值都不超过1，再反复做"
        "只由乘积组成的一轮：X变成a乘X，加上b乘X乘X转置乘X，再加上c乘X乘X转置的平方乘X。<bookmark mark='b'/>用奇异值"
        "分解写出X，虽然我们从不真的去算它。<bookmark mark='c'/>每个乘积里，中间的U和V都消掉了，这一轮不动奇异向量。"
        "<bookmark mark='d'/>它只是对每个奇异值同时作用同一个多项式，σ的p。<bookmark mark='e'/>所以整个问题变成关于"
        "一个单变量函数的问题：哪个多项式，反复作用，能把0到1之间的一切都送到1？",
    'Here are three candidates.':
        "这里有三个候选。<bookmark mark='a'/>经典的牛顿–舒尔茨多项式：1.5σ减0.5σ的三次方。它以零斜率固定住1，所以在1"
        "附近收敛得非常快；但它在0处的斜率只有1.5，很小的奇异值要很多轮才能长大。<bookmark mark='b'/>凯勒·乔丹为Muon"
        "调了一个五次多项式的系数：在0处的斜率是3.4，小的值长得很快，代价是永远到不了1。所有的值最后都落在大约0.7到"
        "1.3之间，训练并不在意。<bookmark mark='c'/>还有第三个：2σ减1.5σ的三次方，再加0.5σ的五次方：它也以零斜率"
        "固定住1，在1附近把误差平方再减半，比三次多项式好三倍，所以能把已经很接近的值钉住。",
    'f"Now on real data: the gradient matrix from Chapter ten.':
        "现在用真实数据：第10章的那个梯度矩阵。<bookmark mark='a'/>跟着一个中等大小的奇异值走过乔丹的多项式：每一轮"
        "都把它往1弹上去。<bookmark mark='b'/>这是它全部{len(s0)}个奇异值，一轮一轮地。{R}轮之后，所有大于最大值"
        "百分之一的，共{nb}个，都落在{lo_b:.2f}到{hi_b:.2f}之间。最小的那些，是数值上的尘埃，长了但没到，这没有"
        "任何代价。<bookmark mark='c'/>经典的三次多项式在同样{R}轮里，最差的值离1还有{dev_c[R]:.2f}，需要{said1}",
    "f'more rounds to catch up: after {len(dev_c) - 1}":
        "更多轮才能追上：{len(dev_c) - 1}轮后是{dev_c[-1]:.2f}。",
    'many more rounds than that.': "比这多得多的轮数。",
    'f"The newest practice combines them.':
        "最新的做法把它们结合起来。<bookmark mark='a'/>把离1最远的距离一轮一轮画出来。乔丹的多项式很快接近，然后停住，"
        "停在{dj:.2f}。<bookmark mark='b'/>DeepSeek的第四代在2026年先跑八轮乔丹的多项式，再跑两轮那个精确的，把已经"
        "很接近的全都钉住：在我们的梯度上，最差的值最后离1只有{dh_s}。<bookmark mark='c'/>训练好的权重矩阵也一样，见虚线。2025年，诺亚·阿姆塞尔和同事推导出每一轮最好的多项式，"
        "叫作Polar Express：寻找廉价正交化的努力还在继续。",
    'So orthogonalizing is a polynomial applied to every singular value at once':
        "所以正交化就是对每个奇异值同时作用一个多项式，只用矩阵乘法；选哪个多项式，是在速度和精确之间权衡。现在，"
        "让这一部分的所有优化器，在我们自己的模型上公平地比一场。",

    # ------------------------------------------------------------------ Race
    'Chapter twelve. The race, run fairly.': '第12章。一场公平的比赛。',
    'f"Now a race between the optimizers of this part':
        "现在让这一部分的优化器，在我们的字符模型上，按保证公平的规则比一场。<bookmark mark='a'/>同样的模型，同样顺序"
        "的同样批次，同样的三千步，同样的调度：短暂的预热，然后余弦下降。<bookmark mark='b'/>每个优化器有{n_lr}个"
        "学习率，相邻两个差一倍，如果最好的在范围尽头就再加，保留最好的那个：一个方法可能只是因为学习率不对才显得差。<bookmark mark='c'/>然后把"
        "最好的设置再用两个随机种子各跑一遍，看看任何差别里有多少是运气。<bookmark mark='d'/>参赛的有：带动量的SGD、"
        "AdamW、Lion、Shampoo、SOAP和Muon。",
    '"First the learning-rate sweeps.':
        "先看学习率扫描。<bookmark mark='a'/>每个优化器的留出损失随学习率的变化：太小就爬得慢，太大就冲过头，"
        "中间是一个山谷。<bookmark mark='b'/>谷底就是它比赛用的学习率。{etxt}",
    'f" One caution: {SAY[edges[0]]}\'s best rate is at the end of its grid':
        "要提醒一点：{SAY[edges[0]]}最好的学习率在网格的尽头，所以它可能还能再好一点。",
    'f" One caution: {len(edges)} of them': "要提醒一点：有{len(edges)}个优化器最好的学习率在网格的尽头。",
    ' Every best rate is inside its grid': "每个最好的学习率都在网格内部，所以网格够宽。",
    '"Now the race itself, replayed':
        "现在是比赛本身的回放：每个优化器用它最好的学习率，实线是三个种子的中位数，色带是它们的范围。"
        "<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{rel}最后一名是{SAY[last[0]]}，{last[1]:.3f}比特。",
    "f'AdamW, the baseline, finishes {aw[1] - wm:.3f} bits behind the winner. '":
        "基线AdamW比冠军落后{aw[1] - wm:.3f}比特。",
    'The baseline, AdamW, is the winner here.': "这里的冠军就是基线AdamW。",
    'f"{SAY[w]} wins, at {wm:.3f} bits':
        "{SAY[w]}获胜，{wm:.3f}比特，它最差的种子也胜过{SAY[s2]}最好的种子：这个差别大于种子的运气。",
    'f"{SAY[w]} is ahead on average':
        "{SAY[w]}平均领先，{wm:.3f}比特，但它的种子和{SAY[s2]}的有重叠：在这个模型上，前两名并没有明确拉开。",
    'f"What do these numbers read like?':
        "这些数字读起来是什么样子？这里带动量的SGD和冠军{SAY[names[1]]}，用同样的随机数，在训练的几个检查点上续写"
        "同样的三个词。<bookmark mark='a'/>训练之前，每个字符的可能性都一样，每个{b0[0]:.1f}比特：整个字母表里的噪声。"
        "<bookmark mark='b'/>{steps[1]}步之后，有了空格和短词。<bookmark mark='c'/>到第{steps[3]:,}步，大部分已经"
        "像单词了，<bookmark mark='d'/>到最后，{SAY[names[1]]}是{b1[-1]:.2f}比特，{said1}",
    "f'{SAY[names[1]]}, there is punctuation and the rhythm of sentences. It is ahead at every checkpoint.'":
        "有了标点和句子的节奏。它在每个检查点上都领先。",
    "f'{SAY[names[1]]}, there is punctuation and the rhythm of sentences.'":
        "有了标点和句子的节奏。",
    'f"Steps are not free, though.':
        "不过，每一步都不是免费的。<bookmark mark='a'/>这是每个优化器每一步所花的时间，相对于AdamW，在这台电脑上："
        "Muon是{mu:.1f}倍，Shampoo是{sh:.1f}倍。<bookmark mark='b'/>这要谨慎看待：一个共享的处理器线程，一个小到额外"
        "矩阵运算占了每一步很大比例的模型。对于GPU上的大语言模型，Muon的作者估计它额外的运算量不到百分之一；AlgoPerf"
        "按墙上时钟时间给优化器打分，正是为了这个原因。",
    "f'So on our model, with every optimizer at its own best rate":
        "所以在我们的模型上，每个优化器都用自己最好的学习率、同样的步数，{SAY[w]}得了第一。学习率为每个优化器分别调过，"
        "调度对所有优化器都固定。接下来：这个调度该是什么形状。",

    # ------------------------------------------------------------------ Schedule
    'Chapter thirteen. Schedules, and the river valley.': '第13章。学习率调度，与河谷。',
    "Chapter three's lesson was that a constant step ends in a cloud":
        "第3章的教训是：恒定的步长最后停在一团云里，只有缩小的步长才会停下来。所以真实的训练会一边走一边改变学习率。"
        "<bookmark mark='a'/>几乎所有训练都从预热开始：几百个很小、逐渐变大的步子，因为这时权重还是随机的，Adam的滑动"
        "大小还不知道，而且正如第5章所示，地形很陡。<bookmark mark='b'/>多年来的标准是余弦调度，来自2016年的伊利亚·"
        "洛希洛夫和弗兰克·胡特：从峰值平滑地滑到零。<bookmark mark='c'/>更新的标准是在大部分时间里保持学习率不变，"
        "只在最后衰减：预热、稳定、衰减，2024年由MiniCPM团队推广开来。",
    'Why does holding the rate high, then dropping it, work so well?':
        "为什么先保持高学习率、再降下来，效果这么好？2024年，斯坦福的Kaiyue Wen和同事给出了一幅图景：河谷。"
        "<bookmark mark='a'/>损失有一条谷底，一条河，缓缓下降，两边是陡峭的山坡。<bookmark mark='b'/>用很大的恒定步长，"
        "噪声把下山的人抛上山坡，但它沿着河走得很快。<bookmark mark='c'/>用很小的步长，它待在谷底附近，却爬得很慢。"
        "<bookmark mark='d'/>预热–稳定–衰减两者兼得：用高学习率沿河而下，最后再落到谷底。",
    'f"Split the loss into its two parts.':
        "把损失拆成两部分。<bookmark mark='a'/>在恒定学习率下，山坡那部分停在一个由步长决定的水平：{hc:.3f}，而由第4章"
        "的平稳云预测的是{hp:.3f}。<bookmark mark='b'/>河的那部分才是真正的进展，只有大步长才能让它快。"
        "<bookmark mark='c'/>到最后，{said1}衰减并没有找到更好的地方；它只是去掉了噪声，那噪声遮住了这个地方本来就有多好。",
    "f'warmup–stable–decay has the lowest total loss":
        "预热–稳定–衰减的总损失最低：它沿河走得和恒定学习率一样远，而它山坡那部分已经塌了下去。",
    "f'the lowest total belongs to the {SAYK[best]} schedule. '":
        "总损失最低的是{SAYK[best]}调度。",
    'f"Now on our character model, with AdamW.':
        "现在在我们的字符模型上用AdamW。三次余弦训练，每种长度一次：一千步、两千步和四千步。还有一次恒定学习率的训练，"
        "在每种长度的五分之四处分出一个分支去冷却。<bookmark mark='a'/>恒定的那次训练进入了平台期。每个分支在学习率下降"
        "时都陡然下降：到最后，比恒定的那次低了{drop:.2f}比特。<bookmark mark='b'/>结论：{verdict}"
        "<bookmark mark='c'/>而三个结果都来自同一次恒定训练。这就是像第12部分那样的规模定律研究要用它的原因：花一次"
        "训练的钱，得到一整族训练完成的模型。",
    'at every length the cool-down branch matches the cosine run':
        "在每种长度上，冷却分支都和训练了恰好那么长的余弦训练不相上下，差别在种子之间的差异以内。",
    'at every length the cool-down branch beats the cosine run':
        "在每种长度上，冷却分支都胜过训练了恰好那么长的余弦训练。",
    'the cool-down branches and the cosine runs trade places':
        "冷却分支和余弦训练互有胜负：没有哪种调度在每种长度上都赢。",
    'So a high learning rate travels; a falling one settles':
        "所以高学习率负责赶路，下降的学习率负责落定；而预热–稳定–衰减让你可以事后再决定什么时候落定。我们能不能"
        "干脆不要调度？",

    # ------------------------------------------------------------------ ScheduleFree
    'Chapter fourteen. Without a schedule.': '第14章。不用调度。',
    'f"Go back to Chapter three\'s cloud.':
        "回到第3章的那团云。下山的人从不停下，但这团云的中心就是答案。<bookmark mark='a'/>所以不要取最后的位置：取所有"
        "位置的平均。大卫·鲁珀特，以及鲍里斯·波利亚克和阿纳托利·尤季茨基，在1990年前后证明了这个平均后的下山人收敛"
        "得和任何方法一样快。这里，云里的点离最好的权重通常有{gap_cloud:.2f}；它们的滑动平均最后只差{gap_avg:.3f}。"
        "<bookmark mark='b'/>深度学习用的是一个会遗忘开头的版本：权重的指数移动平均。",
    '"Apply it to Chapter thirteen\'s constant-rate run':
        "把它用在第13章那次恒定学习率的训练上：保留一个记忆大约五百步的权重平均，给这个平均打分。<bookmark mark='a'/>"
        "{said1}取平均和衰减，是去掉同一种噪声的两种办法。",
    "f'The averaged weights are better than the raw ones by {gain:.3f} bits":
        "平均后的权重最后比原始权重好{gain:.3f}比特：相当于冷却所得收益的{share:.0%}，而学习率一点没动。",
    "f'Here the average is no better than the raw weights":
        "这里平均并不比原始权重好，{e_end:.3f}对{c_end:.3f}。",
    'In 2024 Aaron Defazio and colleagues turned averaging':
        "2024年，亚伦·德法齐奥和同事把取平均变成了一个完全不需要调度的优化器。<bookmark mark='a'/>保留两套权重："
        "一个快速的下山人z，以恒定学习率走，<bookmark mark='b'/>以及它的滑动平均x，也就是你实际使用的模型。"
        "<bookmark mark='c'/>诀窍在于在哪里求梯度：在y，两者之间的一个点。β为零时就是普通的平均；为一时，梯度就在平均"
        "本身上求；实践中十分之九效果好。免调度的AdamW赢得了2024年AlgoPerf的自调参赛道，比基线快大约百分之八，而且"
        "没有需要调的学习率调度。",
    'f"Does it work here?':
        "它在这里管用吗？在我们的字符模型上用免调度的AdamW，它的学习率从AdamW学习率的四个倍数里挑选，最好的是"
        "{mb:g}倍。一次{S:,}步的训练，边走边打分，对比第13章那些各自只为一种长度训练的调度。<bookmark mark='a'/>结论："
        "{verdict}<bookmark mark='e'/>{edge}<bookmark mark='b'/>这张表有个细节：调度训练的数字是在全部留出文本上算的，"
        "免调度的是从它的曲线上读出来的，只用了五分之一的文本。",
    ' Its best rate was at the edge of our grid': "它最好的学习率在我们网格的边上，所以它可能还能再好一点。",
    'at every length, one schedule-free run matches the best scheduled run':
        "在每种长度上，一次免调度的训练都和为那个长度训练的最好的调度不相上下。",
    'it trails the scheduled runs early on': "它在前期落后于调度训练，到最长的长度时追回了大部分差距。",
    "f'on our model it trails the tuned schedules at every length":
        "在我们的模型上，它在每种长度上都落后于调好的调度，差距在{min(gaps):.3f}到{max(gaps):.3f}比特之间。",
    'So averaging the weights removes the same noise a decaying schedule does':
        "所以对权重取平均，去掉的是衰减调度所去掉的同一种噪声，而免调度方法把这一点内置了。接下来：当训练不只是乱逛，"
        "而是炸掉时，会发生什么。",

    # ------------------------------------------------------------------ Stability
    'Chapter fifteen. Keeping training stable.': '第15章。让训练保持稳定。',
    'f"Large runs sometimes blow up':
        "大规模训练有时会炸掉：损失突然跳起来，只好回滚。第18部分会讲大规模下的故事。这里是其中一种机制，我们故意把它"
        "引发出来，用的是一个在我们的书上训练的单层Transformer，就是第13部分会搭的那种。<bookmark mark='a'/>看最大的"
        "注意力分数，一个查询乘以一个键。用中等学习率的Muon，它长到大约{mx_s:,.0f}。<bookmark mark='b'/>学习率再大"
        "四倍，它就失控了，长到大约{mx_f:,.0f}：softmax变成了硬性选择，梯度消失，这些头不再学习。{said1}",
    "f\"<bookmark mark='c'/> The faster run ends worse":
        "<bookmark mark='c'/>快的那次训练最后更差，{hf:.2f}比特对{hs:.2f}。",
    "f\"<bookmark mark='c'/> Here the faster run still ends at":
        "<bookmark mark='c'/>这里快的那次训练最后仍然是{hf:.2f}比特，对{hs:.2f}。",
    'In 2025 Moonshot AI met exactly this':
        "2025年，月之暗面在用Muon训练Kimi K2时正好遇到了这个问题，并且做了一次外科手术式的修复。<bookmark mark='a'/>"
        "每一步之后，测出每个头最大的分数。<bookmark mark='b'/>这个分数对这个头的查询和键权重是双线性的，所以两者都乘以"
        "γ的平方根，分数就乘以γ。<bookmark mark='c'/>一旦它超过阈值τ，就选γ把它恰好放到τ上。别的什么都不变。τ取一百，"
        "Kimi K2这个有一万亿参数的模型，在十五点五万亿个词元上训练，按它的报告，没有出现一次损失尖峰。",
    'f"On our small transformer, QK-clip at tau a hundred':
        "在我们的小Transformer上，τ取一百的QK-clip把快速Muon训练的分数压在阈值附近，从没超过大约{mxq:.0f}，{said2}"
        "<bookmark mark='a'/>学习率大得过分的AdamW，把分数推得更高。最古老的补救是2013年的梯度裁剪：只要梯度长于某个c，"
        "就把它缩短到c。{said3}直击病因的QK-clip，得到{haq[0]:.2f}和{haq[1]:.2f}。",
    "f'and it ends at {hq[0]:.2f} and {hq[1]:.2f} bits":
        "两个种子最后分别是{hq[0]:.2f}和{hq[1]:.2f}比特，不用它时是{hf[0]:.2f}和{hf[1]:.2f}。",
    "f'but its loss is not better on both seeds":
        "但它的损失并不是两个种子都更好：{hq[0]:.2f}和{hq[1]:.2f}，对{hf[0]:.2f}和{hf[1]:.2f}。",
    "f\"<bookmark mark='b'/> It rescues both seeds here":
        "<bookmark mark='b'/>它在这里救回了两个种子，{hg[0]:.2f}和{hg[1]:.2f}比特，对{ha[0]:.2f}和{ha[1]:.2f}。",
    "f\"<bookmark mark='b'/> It rescues one seed":
        "<bookmark mark='b'/>它救回了一个种子，{min(hg):.2f}比特，另一个没有，{max(hg):.2f}：裁剪限制的是每一步，而不是"
        "把分数推高的那种缓慢漂移。",
    "f\"<bookmark mark='b'/> Here it doesn't save the run":
        "<bookmark mark='b'/>这里它没能救回这次训练：{hg[0]:.2f}和{hg[1]:.2f}比特。",
    'Weight decay has a second life in modern networks.':
        "权重衰减在现代网络里还有第二重身份。大多数权重矩阵后面都跟着一个归一化，这让它们尺度不变：W和两倍的W给出"
        "同一个网络。<bookmark mark='a'/>于是梯度和W正交，一步永远不可能把它缩小。<bookmark mark='b'/>衰减把W乘上一个"
        "因子缩小；Adam的一步u又把它加大。<bookmark mark='c'/>对范数平方来看：衰减每步去掉它的2ηλ，而每一步加上η平方"
        "乘以u的大小，再乘以相邻步子之间的相关程度，这由动量决定。<bookmark mark='d'/>两者在一个平衡范数上抵消，"
        "这个范数和η除以λ的平方根成正比。<bookmark mark='e'/>所以权重衰减对这些权重根本不起正则化作用：它决定的是"
        "矩阵的大小，使每一步都是矩阵的固定比例，也就是一个有效学习率。",
    '"Measure it on our character model, with a normalization added':
        "在我们的字符模型上测一测：在第二个隐藏矩阵之后加一个归一化，用三种衰减强度，每种是前一种的四倍。"
        "<bookmark mark='a'/>每个范数都升到或降到一个水平，然后停在那里，衰减越强，到得越快。{said4}要是没有动量那个因子，"
        "第一种的预测会是{nomom:.1f}，小得太多。<bookmark mark='c'/>衰减变成四倍，范数就减半：拟合出的幂次是{sl:.2f}，"
        "推导值是负二分之一。",
    "f\"<bookmark mark='b'/> The dashed lines are the predicted equilibria, and every":
        "<bookmark mark='b'/>虚线是预测的平衡值，每个测出的范数都在预测值的{worst:.0%}以内。",
    "f\"<bookmark mark='b'/> The dashed lines are the predicted equilibria; the worst":
        "<bookmark mark='b'/>虚线是预测的平衡值；偏差最大的差了{worst:.0%}。",
    'So instability has causes, and the best fixes target them':
        "所以不稳定有它的原因，最好的修复直击原因：QK-clip只缩放产生分数的那两个矩阵，裁剪给每一步封顶，而权重衰减"
        "悄悄地决定了每个归一化矩阵的大小。最后：自2024年以来，业界在这些问题上学到了什么。",

    # ------------------------------------------------------------------ Frontier
    'Chapter sixteen. The optimizer race': '第16章。2024到2026年的优化器竞赛。',
    'In two years the race moved from small benchmarks':
        "两年之内，这场竞赛从小基准走到了最大的模型。<bookmark mark='a'/>2024年，AlgoPerf让分布式Shampoo夺冠，Muon在"
        "一场速通比赛里创了纪录。<bookmark mark='b'/>2025年2月，月之暗面把Muon放大到一个一百六十亿参数的混合专家模型"
        "Moonlight，报告在计算最优的训练中，效率大约是AdamW的两倍。<bookmark mark='c'/>7月，他们用MuonClip训练了"
        "一万亿参数的Kimi K2。<bookmark mark='d'/>智谱的GLM-4.5也用了Muon。<bookmark mark='e'/>接着出现了细致的独立"
        "基准测试，数字也小了。<bookmark mark='f'/>2026年，DeepSeek的第四代模型的大部分都用Muon训练，用的是第11章的"
        "混合牛顿–舒尔茨迭代，并且对查询和键做归一化，而不是裁剪它们。",
    'How big are the gains really?':
        "收益到底有多大？<bookmark mark='a'/>新的优化器曾宣称有AdamW的一点五到两倍速度。2025年，斯坦福的Kaiyue Wen、"
        "David Hall、马腾宇和Percy Liang同样细致地测试了其中十一个，每个都调参，包括AdamW，模型最大到十二亿参数。"
        "<bookmark mark='b'/>仅仅调好AdamW的学习率，就能让它在小模型上快一倍：很多宣称的收益是对着弱基线测的。"
        "<bookmark mark='c'/>最好的是基于矩阵的方法，Muon和SOAP，在一亿参数时大约快一点四倍，<bookmark mark='d'/>"
        "到十亿参数时只快一点一倍。<bookmark mark='e'/>每个参数的数据少时Muon领先，多时SOAP领先。<bookmark mark='f'/>"
        "2026年，英伟达的一个团队用Muon和SOAP训练了最大七百二十亿参数的混合专家模型，发现它们在一亿词元的批量下"
        "依然稳定，而AdamW在那里变差了；收益不大，而且各项任务上有好有坏。",
    'Meanwhile the descendants multiply.':
        "与此同时，后继者越来越多。<bookmark mark='a'/>Muon这一支：更好的多项式，比如Polar Express；能把工作分到成千上万"
        "台机器上的版本，比如微软的Dion，它2026年的后继者报告在达到Muon损失的同时，优化器那一步最多快六倍；以及一连串"
        "2026年宣称有改进的预印本。<bookmark mark='b'/>Shampoo这一支：分布式Shampoo、SOAP，以及更大规模的SOAP变体。"
        "这些说法大多出自作者本人，还没有经过独立检验。<bookmark mark='c'/>这正是这场竞赛真正的教训，也是第12章那样"
        "比赛的原因：像调新方法一样用力去调基线，在同样的预算下比较，用几个种子，并报告范围。",
    'So by 2026 the matrix optimizers had won a place at the frontier':
        "所以到2026年，矩阵优化器已经在前沿占了一席之地：Muon训练着一些最大的开放模型。但仔细测量下来，它们相对于调好的"
        "AdamW的优势是真实的，比最初宣称的小，而且随着模型变大而缩小。",

    # ------------------------------------------------------------------ Outro
    'f"Let\'s take stock.':
        "我们来盘点一下。梯度下降需要的步数和条件数成正比，动量只需要它的平方根。随机批量让每一步便宜又带噪声，噪声是"
        "一种温度，η除以B，它决定训练最后停留的那团云有多大。在固定步长下，训练把曲率推到稳定性边缘η分之2，并停在那里。"
        "Adam给每个权重重新缩放，它的极限是符号下降；Shampoo和Muon看见整个矩阵，而Muon的一步，谱范数下最陡的那一步，"
        "用一个多项式把每个奇异值都设成1。在我们自己的模型上那场公平的比赛里，{win}得了第一。高学习率沿河赶路，下降的"
        "学习率落定；而权重衰减悄悄地决定了每个归一化矩阵的大小。",
    'All of this comes back.':
        "所有这些都会再出现。第12部分会测出临界批量，并在模型变宽变深时沿用同一个学习率。第13和第14部分的Transformer"
        "用AdamW和预热来训练。第18部分用完整的现代配方训练一个模型，包括Muon，并让它在大规模下保持稳定。而第26和第27"
        "部分的强化学习和微调，用的也是这些优化器。",
    'Here are six problems': "这里有六道习题，从梯度下降的速度到权重衰减的平衡。请在这里暂停，把它们做一遍；完整的解答在这一部分的笔记里。",
    'Next time: the mathematics of scale.':
        "下一次：规模的数学。为什么更大的模型会如此可预测地变好，怎样在参数和数据之间分配预算，以及怎样把学习率选定一次，"
        "在模型变大时一直沿用。<bookmark mark='a'/>对数坐标上的直线，以及它们许下的承诺。",
    "Bottou, Curtis and Nocedal's survey":
        "博图、柯蒂斯和诺塞达尔的综述，是关于随机优化最好的一份全面论述；杰里米·伯恩斯坦的文章讲清了Muon的几何。"
        "感谢观看，我们第12部分见。",
}

PHRASES = {
    'Muon': 'Muon', 'AdamW': 'AdamW', 'Adam': 'Adam', 'Lion': 'Lion', 'Shampoo': 'Shampoo', 'SOAP': 'SOAP',
    'K-FAC': 'K-FAC', 'SGD with momentum': '带动量的SGD', 'gradient descent': '梯度下降', 'Gradient descent': '梯度下降',
    'the natural gradient': '自然梯度', 'the heavy ball': '重球法', 'The heavy ball': '重球法',
    'constant': '恒定', 'cosine': '余弦', 'warmup–stable–decay': '预热–稳定–衰减', 'small constant': '小的恒定',
}
