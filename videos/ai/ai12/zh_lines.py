"""Chinese narration for ai12: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第12部分：规模的数学'

CHAPTERS = {
    'Hook': '对数坐标上的一条直线',
    'Wide': '1. 无限宽',
    'Lazy': '2. 惰性',
    'MuP': '3. 推导μP',
    'Transfer': '4. 一个学习率，适用所有宽度',
    'Depth': '5. 越来越深',
    'Batch': '6. 批量该多大？',
    'Laws': '7. 测量规模定律',
    'Valley': '8. Chinchilla的山谷',
    'Kaplan': '9. 卡普兰漏掉了什么',
    'Overtrain': '10. 为长远而训练',
    'Data': '11. 当数据用完',
    'Experts': '12. 专家与比特',
    'Power': '13. 为什么是幂律？',
    'Emerge': '14. 涌现，还是幻象？',
    'Grok': '15. 顿悟',
    'TestTime': '16. 在回答时扩展',
    'Frontier': '17. 预训练停滞了吗？',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"Make a model bigger, train it longer':
        "把模型做大，训练得更久，它就会变好。这一点人人都料到了。出人意料的是，它变好得多么可以预测。"
        "<bookmark mark='a'/>这里是第11部分的字符模型的{len(widths)}种大小，每种最多训练{len(s['ks'])}种长度："
        "一共{n_runs}次训练，就在制作这个视频的电脑上完成，每一次都画在它所花的运算次数上。"
        "<bookmark mark='b'/>每种大小都先变好，然后变平：它的容量用完了。但整把扇子的下边缘，也就是每份预算能买到的"
        "最低损失，是一条光滑的曲线。<bookmark mark='c'/>减去{E:.2f}比特的下限，剩下的部分在对数坐标上沿着一条直线下降："
        "一条幂律，斜率是{slope:.2f}。像这样在小模型上测出来的曲线，就是各个实验室决定下一步造什么的依据。",

    'The idea has a history.':
        "这个想法有它的历史。1994年，拉德福德·尼尔证明，无限宽的网络是一个高斯过程。<bookmark mark='a'/>2001年，"
        "班科和布里尔发现，更多的数据胜过更聪明的算法。<bookmark mark='b'/>2017年，百度的一个团队在翻译、语言、图像和"
        "语音上都发现了幂律。<bookmark mark='c'/>2018年，神经正切核。<bookmark mark='d'/>2020年，OpenAI的规模定律，"
        "以及建立在它们之上的GPT-3。<bookmark mark='e'/>2022年，Chinchilla修正了配方，μP让一个学习率适用于每一种大小，"
        "而顿悟让所有人困惑。<bookmark mark='f'/>2023年，极限：会用完的数据，和似乎凭空出现的能力。"
        "<bookmark mark='g'/>2024年，规模转向了回答：思考得更久的模型。<bookmark mark='h'/>2025年，规模与预训练相当的"
        "强化学习。<bookmark mark='i'/>而在2026年，各个实验室又回到了大得多的基础模型。",

    'This is Part 12 of AI, Built':
        "这是《人工智能，从零搭建》的第12部分，也是第二幕的结尾。<bookmark mark='a'/>这一部分讲：网络变得无限宽时会"
        "发生什么；怎样把学习率设定一次，在模型变宽、变深时一直沿用；规模定律，在我们自己的模型上测量，也加以推导；"
        "使它们弯折的种种权衡；它们究竟为什么是幂律；以及前沿正在发生什么。",

    # ------------------------------------------------------------------ Wide
    'Chapter one. Infinitely wide.':
        '第1章。无限宽。',

    'Start a network with random weights':
        "让一个网络从随机权重出发，问它在计算什么。一个有n个单元的隐藏层；每个单元的输出乘上一个随机数，总和再除以"
        "n的平方根。<bookmark mark='a'/>只有一个单元时，某一点上的输出，在几千次随机初始化里，坑坑洼洼，尾巴很重。"
        "<bookmark mark='b'/>单元很多时，它是许多独立项的和，于是第5部分的中心极限定理接管了：一个高斯分布，方差"
        "正好是公式预测的那个。<bookmark mark='c'/>不只是在一点上：整个函数变成了一个高斯过程，一条随机的光滑曲线，"
        "它的协方差，也就是一个核，由网络结构决定。拉德福德·尼尔在1994年看到了这一点；2018年，它被推广到深层网络。",

    'That is the network before training.':
        "那是训练之前的网络。2018年，阿蒂尔·雅科、弗兰克·加布里埃尔和克莱芒·洪勒问：训练中会发生什么？"
        "<bookmark mark='a'/>梯度下降沿着误差的梯度移动权重。<bookmark mark='b'/>由链式法则，任一点x上的输出，"
        "移动的量是它自己的梯度乘以这一步。<bookmark mark='c'/>把两者合起来，就出现了一个对象：两个输入处梯度的点积，"
        "也就是神经正切核。它说的是：修正一个输入上输出的一步，会把另一个输入上的输出移动多少。"
        "<bookmark mark='d'/>如果这个核保持不动，这就是一个线性方程，它的解就是核回归，也就是第6部分的方法，用的正是"
        "这个核。他们的定理是：当宽度趋于无穷，这个核确实保持不动。",

    'f"Check it, on that one-layer network':
        "来验证一下：就用那个单层网络，在10个点上用梯度下降训练，宽度从30到3万。<bookmark mark='a'/>量一量权重相对"
        "起点走了多远：斜率是{sw:.2f}。<bookmark mark='b'/>再量核移动了多远：斜率是{sk:.2f}。{said1}"
        "<bookmark mark='c'/>所以，一个宽网络训练起来，就像它自己的线性化。在100个单元时，训练出的函数偏离线性预测"
        "最多{gap100:.2f}；在1万个单元时，只有{gap10k:.2f}。",

    'The weights, close to minus a half:':
        "权重的斜率接近负二分之一：n个权重中的每一个，大约移动n的平方根分之一，小到改变不了任何一个单元算的东西，"
        "合起来却足以移动输出。核移动得更少，更接近n分之一：伊森·戴尔和盖伊·古尔-阿里在2019年证明，它的期望变化"
        "像n分之一那样缩小，因为各个单元的小变化大多互相抵消。",

    'Both close to minus a half.':
        "两者都接近负二分之一。n个权重中的每一个，大约移动n的平方根分之一：小到改变不了任何一个单元算的东西，"
        "合起来却足以移动输出。",

    'Both shrink with width, though':
        "两者都随宽度缩小，只是速度和理论在无限宽时预测的不完全一样。",

    # ------------------------------------------------------------------ Lazy
    'Chapter two. Lazy.':
        '第2章。惰性。',

    'f"A wide network trained like its linearization has a catch.':
        "像线性化那样训练的宽网络，有一个问题。拿第11部分的字符模型，把它做得越来越宽，用神经正切核的步长来训练。"
        "量一量它的隐藏特征变了多少，也就是每个隐藏单元从输入算出的东西。<bookmark mark='a'/>网络越宽，它们变得越少："
        "斜率是{slope:.2f}。<bookmark mark='b'/>2019年，希扎、奥亚隆和巴赫把这叫作惰性训练，并且证明这并不是宽网络"
        "独有的：把任何模型的输出放大，它训练起来就像它的线性化。<bookmark mark='c'/>一个惰性的网络，只能给它出发时的"
        "那些随机特征重新加权。它是一种核方法，和第6部分的一样；而第8部分遇到的那些比数据大得多的模型，在这个极限下，"
        "正好就是它的最小范数拟合。",

    'f"Does it matter? Here is a task where it does.':
        "这要紧吗？这里有一个要紧的任务。答案是：x沿着一个隐藏方向w星的投影的平方，减去1；x有{int(r['d'])}维，"
        "可供学习的样本有{int(r['n'])}个。<bookmark mark='a'/>用惰性的方式，也就是神经正切核的缩放，训练一个宽的"
        "两层网络。<bookmark mark='b'/>{said0}<bookmark mark='c'/>现在换成同一个网络、同样的数据、同样的步数，但用"
        "平均场的方式缩放：输出除以n，而不是n的平方根，学习率乘以n，让每个单元移动一个固定的量。{said1}",

    'It ends close to kernel regression':
        "它最后停在离核回归很近的地方，那是用它出发时的核做的核回归：惰性极限，精确算出来的。",

    "f'Kernel regression with its starting kernel, the lazy limit":
        "用出发时的核做核回归，也就是精确算出的惰性极限，结果{('worse' if kgap > 0 else 'better')}了"
        "{100 * abs(kgap):.0f}%：在这个宽度上，网络还没有完全变懒。",

    "f'Its error is {ratio:.1f} times smaller, and every seed":
        "它的误差只有惰性网络的{ratio:.1f}分之一，而且每一个种子都胜过每一个惰性的种子。",

    "f'Its error is {ratio:.1f} times smaller on average":
        "平均来说，它的误差只有惰性网络的{ratio:.1f}分之一，不过不同种子的结果有重叠。",

    'f"What did the rich network learn that the lazy one could not?':
        "丰富的网络学到了什么惰性网络学不到的东西？把每个隐藏单元画成一个点：它的权重有多少指向那个隐藏方向，"
        "又有多少指向别处。<bookmark mark='a'/>现在回放训练。<bookmark mark='b'/>惰性的单元几乎不动：它的权重总共"
        "只走了起始长度的{100 * mvn:.0f}%。丰富的单元沿着w星摆了出去，走了{100 * mvm:.0f}%：网络找到了唯一要紧的"
        "那个方向。这是一个学到的特征，而任何核方法都造不出来。<bookmark mark='c'/>所以我们想要的无限宽极限是"
        "另一个：在任何宽度上，特征都一直在动。对两层网络，它叫平均场；对任意深度，它就是μP。",

    # ------------------------------------------------------------------ MuP
    'Chapter three. Mu-P, derived.':
        '第3章。推导μP。',

    'Here is the whole idea, in one layer.':
        "整个想法，用一层就能说清。它的输出是n个权重乘以n个输入的和。<bookmark mark='a'/>开始时权重是随机的，"
        "所以这n项的符号随机，大多互相抵消：由中心极限定理，总和像n的平方根那样增长。把起始权重除以n的平方根，"
        "输出在任何宽度上都保持同样大小。<bookmark mark='b'/>训练就不一样了。一层的梯度是一个外积：误差信号乘以输入。在这个局部计算中，先假设误差信号是一阶量。"
        "<bookmark mark='c'/>所以这一步作用到那个输入上，得到的是n个符号全都相同的项之和：它像n那样增长，而不是"
        "n的平方根。<bookmark mark='d'/>如果希望这一层在任何宽度上都变化差不多的量，局部学习率就必须像n分之一那样缩小。完整网络还必须考虑误差经过其他层时如何随宽度缩放。"
        "杨格和爱德华·胡在2021年为一大类网络推导出了这些规则，称之为最大更新参数化：μP。",

    'For Adam, a common language-model optimizer':
        "对于Adam，这种常用的语言模型优化器，配方是一张小表。<bookmark mark='a'/>输入和偏置用基础学习率。"
        "隐藏矩阵的学习率是基础学习率除以宽度，因为Adam让每个元素移动大约一个学习率，于是n个同向的项加起来是它的"
        "n倍。输出层的起点要小得多，方差是宽度平方分之一，学习率是基础学习率除以宽度。<bookmark mark='b'/>通常的做法，"
        "我们叫它SP，到处都用同一个学习率。<bookmark mark='c'/>我们的代码把同样的规则写得略有不同，好让宽度为64的"
        "模型在两种做法下完全一样。",

    '"Yang\'s test for whether a parametrization is right':
        "杨格检验一种参数化是否正确的方法，叫坐标检查：在许多宽度上，用同一个学习率训练几步，量一量每一层的激活"
        "变了多少。<bookmark mark='a'/>在通常的参数化里，{said1}<bookmark mark='b'/>在μP里，{said2}",

    "f'the change in the output scores grows with the width":
        "输出分数的变化随宽度增长，大约是宽度的{s_sp:.2f}次方：对小模型合适的学习率，对大模型就太大了，最终会让它"
        "发散。",

    'f"the output scores\' change barely grows with width here':
        "输出分数的变化在这里几乎不随宽度增长，是{s_sp:.2f}次方。",

    "f'the lines are flat, a power of {s_mu:.2f}":
        "这些线是平的，是{s_mu:.2f}次方：每一层在每个宽度上都变化同样的量，这正是推导所要求的。",

    "f'the change grows as the width to the {s_mu:.2f}":
        "变化随宽度的{s_mu:.2f}次方增长，比通常的做法小得多。",

    # ------------------------------------------------------------------ Transfer
    'Chapter four. One learning rate for every width.':
        '第4章。一个学习率，适用所有宽度。',

    '"Now the test that matters: sweep the learning rate':
        "现在是关键的检验：在三个宽度上扫描学习率，从64到1024，每个两个种子，先用通常的做法。"
        "<bookmark mark='a'/>{said1}<bookmark mark='b'/>在μP里，{said2}<bookmark mark='c'/>{said3}",

    "f'The best learning rate drifts as the model grows":
        "最佳学习率随着模型变大而漂移：从最小模型的大约{m0:.0f}乘以10的负{e0}次方，到最大模型的{m1:.0f}乘以10的"
        "负{e1}次方，差了{drift['sp']:.1f}个数量级。调好小模型，照搬它的学习率，大模型就调错了。",

    "f'Over this range the best rate moves by":
        "在这个范围内，最佳学习率移动了{drift['sp']:.1f}个数量级。",

    "f'the valleys line up":
        "这些山谷对齐了：最佳学习率至多移动{drift['mup']:.1f}个数量级。",

    "f'the best rate moves by {drift":
        "最佳学习率移动了{drift['mup']:.1f}个数量级。",

    'f"At each width\'s best rate, the wider model does better':
        "各自在最佳学习率下，更宽的模型表现更好：最小宽度{bl['mup'][0]:.2f}比特，最大宽度{bl['mup'][-1]:.2f}比特。",

    '"Here is what that means in practice.':
        "这在实践中意味着什么？调好最小的模型，用它的学习率训练最大的模型。<bookmark mark='a'/>{said4}"
        "<bookmark mark='b'/>在大规模上，这正是μP的用途。2022年，杨格和同事调好一个4000万参数的模型，把它的设置"
        "照搬到一个67亿参数的GPT-3上，结果胜过了公开发表的那个，花费只有一次训练的7%。<bookmark mark='c'/>2024年，"
        "谷歌DeepMind的埃弗里特和同事表明，只要每一层用对学习率，通常的参数化也能迁移；2025年，Meta就是这样设定了"
        "Llama 4每一层的学习率和初始尺度，并把它们在宽度、深度、批量大小和训练长度之间迁移。",

    'f"The usual way, that costs {pen_sp:.3f}':
        "用通常的做法，这比大模型自己的最佳结果差{pen_sp:.3f}比特；用μP，只差{pen_mu:.3f}。",

    "f'Here the copied rate costs":
        "在这里，照搬的学习率用通常的做法要多付{pen_sp:.3f}比特，用μP是{pen_mu:.3f}。",

    # ------------------------------------------------------------------ Depth
    'Chapter five. Deeper and deeper.':
        '第5章。越来越深。',

    'Depth is the other way to grow.':
        "深度是另一种变大的方式。残差网络把每个块的输出加到一个累加的和上，也就是第9部分的残差流。"
        "<bookmark mark='a'/>有L个块时，残差流是L个分支的和，而每个分支怎样缩放，决定了L变大时会发生什么。"
        "<bookmark mark='b'/>不去管它们，残差流就随深度增长，最佳学习率也会漂移。<bookmark mark='c'/>2023年，两个小组"
        "找到了μP的深度版本：每个分支乘以L的平方根分之一，学习率随之调整。它能在深度之间迁移，但每个块的贡献变得"
        "太小，以至于表现得像线性的：惰性，这回是在深度上。<bookmark mark='d'/>2025年，Cerebras的诺兰·戴伊和同事"
        "表明，乘以L分之一，学习率不动，能让每个块都一直学习特征。他们把它叫作CompleteP。",

    'f"Our character model again, made deep:':
        "还是我们的字符模型，这次做深：{', '.join((str(v) for v in depths[:-1]))}和{depths[-1]}个残差块，每种参数化"
        "扫描9个学习率，每个两个种子。<bookmark mark='a'/>不做深度缩放，{said0}<bookmark mark='b'/>用L的平方根分之一，"
        "移动{dr[0.5]:.1f}个数量级。<bookmark mark='c'/>用CompleteP的L分之一，移动{dr[1.0]:.1f}。{said1}",

    "f\"the best rate moves by {dr[0.0]:.1f} powers of ten":
        "最佳学习率在最浅和最深之间移动{dr[0.0]:.1f}个数量级，最深模型的最佳学习率{dir0}。",

    'the best rate stays on the same point of our grid':
        "从最浅到最深，最佳学习率一直停在我们网格的同一个点上。",

    'At our small depths and short runs, all three keep':
        "在我们这么浅的深度、这么短的训练里，三种做法都把最佳学习率保持在网格的一步之内：戴伊和同事测到的差别，需要"
        "比我们更深的模型、更长的训练。",

    'CompleteP holds the learning rate most still':
        "CompleteP让学习率最稳定，这正是它的设计目标。",

    "f'Here the steadiest is {SPOKEN[best_a]}":
        "在这里最稳定的是{SPOKEN[best_a]}：在我们这么浅的深度、这么短的训练里，差别大约只有一个网格步长。",

    "'Two practical questions. Does depth pay?":
        "两个实际的问题。深度划算吗？{said2}<bookmark mark='a'/>调好浅模型，把它的学习率照搬到深模型上，要付出"
        "多少？不做深度缩放，{cp[0.0]:.2f}比特；用L的平方根分之一，{cp[0.5]:.2f}；用CompleteP，{cp[1.0]:.2f}。"
        "<bookmark mark='b'/>在大规模上，戴伊和同事测得，在15亿参数时，达到同样的损失，CompleteP比μP少用12%的"
        "算力；在他们最深的模型上，少用34%。第9部分细心的初始化，让一万层的网络能够训练；这里是同一个想法，用来"
        "把它们训练好。",

    "f'With CompleteP, yes:":
        "用CompleteP，划算：{depths[0]}个块时{bl[1.0][0]:.2f}比特，{depths[-1]}个块时{bl[1.0][-1]:.2f}比特，"
        "各自用自己的最佳学习率。",

    "f'In our short runs, barely:":
        "在我们短短的训练里，几乎不划算：{depths[0]}个块时{bl[1.0][0]:.2f}比特，{depths[-1]}个块时"
        "{bl[1.0][-1]:.2f}比特。",

    # ------------------------------------------------------------------ Batch
    'Chapter six. How big a batch?':
        '第6章。批量该多大？',

    'Part eleven showed that a small batch gives a noisy gradient.':
        "第11部分说过，小批量给出的梯度有噪声。那批量应该多大？2018年，OpenAI的萨姆·麦坎德利什和同事用一步代数"
        "回答了这个问题。<bookmark mark='a'/>假设样本独立，沿梯度的曲率为正，把走一步之后的损失展开到二阶。梯度有帮助；曲率和噪声限制了步长。"
        "<bookmark mark='b'/>在这个局部模型里选出最好的步长。<bookmark mark='c'/>最好的收益，等于没有噪声时的收益，除以1加上一个比值："
        "噪声尺度比批量。噪声尺度说的是，要多少个样本，梯度的信号才能压过它的噪声。<bookmark mark='d'/>得到的经验模型预测，随着"
        "批量变大，达到某个损失所需的步数下降，而样本数上升。<bookmark mark='e'/>把批量消去，步数和样本数就沿着一条"
        "双曲线互相权衡。远低于噪声尺度时，批量加倍，步数减半，不花代价；远高于它时，只是浪费样本。",

    'f"Measure it. Train our character model with batches from':
        "来测一测。用从{int(Bs[0])}到{int(Bs[-1]):,}个字符的批量训练我们的字符模型，每个批量取三个学习率中最好的"
        "那个，数一数达到某个损失需要多少步、多少个字符。<bookmark mark='a'/>要达到{levels[0]:.1f}比特，这些点落在"
        "一条双曲线上，临界批量大约是{bcrit[0]:,.0f}。<bookmark mark='b'/>要达到更低的损失，{said1}",

    "f'the hyperbola moves out, and the critical batch grows":
        "双曲线向外移，临界批量变大：{bcrit[1]:,.0f}，然后是{bcrit[2]:,.0f}。模型离训练结束越近，能用的批量就越大。",

    "f'the critical batch is {bcrit[1]:,.0f} and":
        "临界批量是{bcrit[1]:,.0f}和{bcrit[2]:,.0f}：在我们的规模上，它几乎不变。",

    '"Is the critical batch really the noise scale?':
        "临界批量真的就是噪声尺度吗？我们可以直接测量噪声尺度：在损失经过每个水平时，用两种批量大小下梯度的大小"
        "来算。<bookmark mark='a'/>{said2}<bookmark mark='b'/>卡普兰的定律发现，临界批量随着损失下降而增长；后来的"
        "研究发现，它随数据量增长，而不是随模型大小。所以大规模训练会边训练边加大批量：DeepSeek-V3在前4690亿个"
        "词元里，把批量从3072个序列增加到15360个，增大到5倍。",

    "f'They agree to within a factor of":
        "两者相差不到{max(ratio.max(), 1 / ratio.min()):.1f}倍：很粗略，麦坎德利什和同事也发现了这一点，但数量级"
        "相同，而且只用一次测量，而不是一次扫描。",

    'Here they disagree by more than a factor of five':
        "在这里，两者相差超过5倍：简单的噪声尺度忽略了曲率，而Adam又改变了噪声的形状。",

    # ------------------------------------------------------------------ Laws
    'Chapter seven. Scaling laws, measured.':
        '第7章。测量规模定律。',

    'In 2017, Joel Hestness and colleagues at Baidu':
        "2017年，百度的乔尔·赫斯特内斯和同事，测量了用于翻译、语言、图像和语音的网络，误差怎样随数据增长而下降。"
        "<bookmark mark='a'/>每条曲线都有三段：数据太少，什么也学不到；然后是对数坐标上的一条直线，一条幂律；"
        "然后是一个下限，再多的数据也过不去。<bookmark mark='b'/>更好的架构把直线往下移，却几乎不改变它的斜率："
        "对语言模型，大约是负0.07。<bookmark mark='c'/>2020年，OpenAI的贾里德·卡普兰、萨姆·麦坎德利什和同事，"
        "在参数、数据和算力上一起发现了同样的规律，跨越7个数量级，并得出结论：大8倍的模型，只需要5倍的数据。"
        "第14部分会讲这怎样导向了GPT-3。这里，我们自己来测这样的定律。",

    'f"A scaling law needs many runs':
        "一条规模定律需要许多次训练，每一次都要按它自己的计划训练到底。这很贵：一次计划读100万个字符、却在半路"
        "停下的训练，并不是一次好的50万字符训练，因为它的学习率从来没有降下来。<bookmark mark='a'/>所以我们用一个"
        "2024年的技巧。每个宽度只用恒定的学习率训练一次，<bookmark mark='b'/>在每个想要的长度上分出一个分支，在最后"
        "五分之一里把学习率冷却到零。<bookmark mark='c'/>每个分支估计同样长度的完整计划会达到的结果，而主干继续"
        "往前走。这种一致性是经验结果，必须检查。<bookmark mark='d'/>{len(widths)}个宽度，从{widths[0]}到{widths[-1]:,}个单元，长度从2的16次方"
        "到2的24次方个字符：{n_runs}次完整的训练，在一个处理器上用了{hours:.1f}个小时。",

    'f"First, one variable at a time, as Kaplan did.':
        "先像卡普兰那样，一次只变一个量。把数据固定得很大，2的24次方个字符，改变模型的大小。<bookmark mark='a'/>"
        "损失沿着一条幂律落向一个下限：L等于{LN['E']:.2f}，加上一个常数除以N的{aN:.2f}次方。<bookmark mark='b'/>"
        "把大小固定得很大，宽度{wD}，改变数据：指数是{aD:.2f}。<bookmark mark='c'/>不同的种子最多相差{sp:.3f}比特，"
        "和这些曲线比起来很小。{said1}",

    'Our exponents are much larger than Kaplan':
        "我们的指数比卡普兰的大得多：我们的模型一次只看8个字符，要学的东西更少，学得也快。不同的任务，不同的指数："
        "能够延续下来的，是曲线的形状。",

    'Our exponents are close to Kaplan':
        "我们的指数和卡普兰的接近，尽管任务不同：能够延续下来的，是曲线的形状。",

    # ------------------------------------------------------------------ Valley
    "Chapter eight. Chinchilla's valley.":
        '第8章。Chinchilla的山谷。',

    'f"In 2022, Jordan Hoffmann and colleagues at DeepMind':
        "2022年，DeepMind的乔丹·霍夫曼和同事，把一个公式同时拟合到他们所有的训练上：一个下限，加上一项随参数缩小，"
        "再加上一项随数据缩小。拟合到我们的{int(ch['n_points'])}次训练上，除去最短和最窄的那些，它平均偏差{float(ch['rms']):.3f}比特。"
        "<bookmark mark='a'/>现在来花一份预算。训练的代价是每个参数、每个字符6次运算，所以6ND等于C。哪种分法"
        "给出最低的损失？像第4部分那样，加一个拉格朗日乘子。<bookmark mark='b'/>令两个导数都为零。"
        "<bookmark mark='c'/>第一个乘以N，第二个乘以D，两边都等于6λND。所以在最优点上，最后一个参数和最后一个字符"
        "的回报相等。<bookmark mark='d'/>解出来，最佳大小随预算的β除以α加β次方增长：我们的模型是{a3:.2f}。",

    'Here is the whole picture: the fitted loss as a surface':
        "这是整幅图景：拟合出的损失，是大小和数据构成的平面上方的一个曲面，两个轴都取对数，我们的训练是曲面上的点。"
        "<bookmark mark='a'/>一份预算是横过平面的一条直线：N乘D固定，一个多了，另一个就少了。<bookmark mark='b'/>"
        "沿着每条直线，曲面陷下去，成了一个山谷。模型太小，装不下读到的东西：欠拟合。模型太大，读得太少，学不完。"
        "<bookmark mark='c'/>把每个山谷的最低点连起来，就得到随着预算增长该走的路：Chinchilla山谷的谷底。",

    'f"Chinchilla read that path three ways':
        "Chinchilla用三种方法读出这条路，我们也可以。第一：所有训练曲线的下包络，也就是每份算力下最好的模型。"
        "第二：过每份预算山谷底部的一条抛物线。<bookmark mark='a'/>第三：我们刚刚解出的公式。<bookmark mark='b'/>"
        "我们对指数的三个估计：{a1:.2f}、{a2:.2f}和{a3:.2f}。Chinchilla的是0.50、0.49和0.46。{said1}"
        "<bookmark mark='c'/>{said2}按每个参数的字符数算，我们的最优点大约是{tpp:.0f}；Chinchilla的大约是20个词元。",

    'Like theirs, ours say that size and data':
        "和他们的一样，我们的估计也说：大小和数据应该一起增长，比例大致相当。",

    "f'Ours spread by {spread:.2f}":
        "我们的三个估计相差{spread:.2f}，而且{('toward the model' if a3 > 0.55 else 'toward the data')}。",

    "Kaplan's 0.73 is well above all three.":
        "卡普兰的0.73远远高于这三个。",

    # ------------------------------------------------------------------ Kaplan
    'Chapter nine. What Kaplan missed.':
        '第9章。卡普兰漏掉了什么。',

    "Kaplan's laws said: as the budget grows":
        "卡普兰的定律说：预算增长时，把大部分投到模型上。GPT-3每个参数读了不到2个词元，DeepMind的Gopher有2800亿个"
        "参数，读了3000亿个词元。<bookmark mark='a'/>Chinchilla用同样的算力，训练了一个只有它四分之一大的模型，"
        "读了4倍的数据。<bookmark mark='b'/>它几乎在所有方面都胜过了Gopher：在MMLU考试上，高出7分多。而且运行起来"
        "便宜4倍。那么，是谁错了，为什么？",

    'f"Part of the answer is how you count.':
        "部分答案在于怎么数。卡普兰数参数时不算嵌入，而在小规模上，嵌入占了模型的很大一部分。<bookmark mark='a'/>"
        "我们自己的训练就显示了这个效应。同样的预算，同样的最佳模型：数上它们全部的参数，最佳大小随预算增长的斜率"
        "是{a_all:.2f}。<bookmark mark='b'/>只数隐藏层，{said1}<bookmark mark='c'/>同一年，托默·波里安和同事找到了"
        "其余的原因：最后一层的代价，预热的长度，以及一个在小批量时没有调好的优化器设置。把这三个都修正，卡普兰"
        "自己的设置就给出了Chinchilla的答案。",

    'f"it grows with slope {a_ne:.2f}: the small models':
        "斜率是{a_ne:.2f}：小模型看起来比实际更小，所以定律看起来更陡。2024年，蒂姆·皮尔斯和宋镇烨证明，在卡普兰"
        "那样的小规模上这样数，会把Chinchilla的二分之一变成接近卡普兰的0.73。",

    'f"the slope is {a_ne:.2f}: in our models':
        "斜率是{a_ne:.2f}：在我们的模型里，被漏掉的那部分太小，不足以让它弯多少。2024年，蒂姆·皮尔斯和宋镇烨证明，"
        "在卡普兰的小规模上，这样数会把二分之一变成接近0.73。",

    'Chinchilla itself was checked two years later.':
        "Chinchilla本身在两年后被检验了。它的三种方法原本略有分歧：拟合公式给出0.46，另外两种大约是二分之一。"
        "<bookmark mark='a'/>2024年，Epoch AI的塔梅·贝西罗格卢和同事，从论文自己的图里重建了数据，240次训练，"
        "从每个点的颜色读出它的损失，再重新拟合这个公式。<bookmark mark='b'/>他们得到0.51，正负0.02：每个参数大约"
        "20个词元，和另外两种方法一致。发表的拟合有偏差。<bookmark mark='c'/>而且它声称的不确定度小得不合理：要窄到"
        "那个程度，需要60多万次训练，而他们跑的还不到500次。<bookmark mark='d'/>给我们的教训是：一个指数是一次测量，"
        "它有误差棒。",

    # ------------------------------------------------------------------ Overtrain
    'Chapter ten. Trained for the long run.':
        '第10章。为长远而训练。',

    'f"Chinchilla\'s optimum minimizes the cost of training.':
        "Chinchilla的最优点，让训练的代价最小。但一个模型训练一次，之后要被使用，也许几十亿次，而每次使用的代价"
        "都和它的大小成正比。所以，训练一个更小的模型、训练得更久，可能更划算。要久多少？拟合出的定律给出答案。"
        "<bookmark mark='a'/>要求一个k倍大小的模型达到最优模型的损失，解出它需要的数据。<bookmark mark='b'/>四分之三"
        "大小的模型，训练要多花{100 * (c75 - 1):.0f}%；一半大小，多花{100 * (c50 - 1):.0f}%；<bookmark mark='c'/>"
        "小于{kmin:.2f}倍的大小，多少数据都不够：小模型的下限高过了目标。<bookmark mark='d'/>{said1}",

    "f'Our own runs that reached the same loss with smaller models":
        "我们自己那些用更小的模型达到同样损失的训练，落在这条曲线附近：一共{len(meas)}次。",

    'Few of our runs reach that loss with a smaller model':
        "我们的训练里，很少有用更小的模型达到那个损失的；达到的那些，都落在曲线附近。",

    'f"In 2023, Nikhil Sardana and colleagues at MosaicML':
        "2023年，MosaicML的尼基尔·萨尔达纳和同事，把回答的代价也算进了预算。训练每个参数、每个词元要6次运算，"
        "回答要2次。<bookmark mark='a'/>固定质量，让一生的总代价最小。<bookmark mark='b'/>一个模型会被用得越多，"
        "它就应该越小、训练得越久。<bookmark mark='c'/>用我们拟合的定律：一个将要回答的字符数是它最优训练量100倍的"
        "模型，应该在每个参数上训练大约{tpp100:.0f}个字符，大小是最优的{nrel100:.2f}倍，一生的代价少"
        "{100 * sav100:.0f}%。<bookmark mark='d'/>萨尔达纳的团队发现，到每个参数1万个词元，质量还在提高；2024年，"
        "Meta用15万亿个词元训练了Llama 3的80亿参数模型：每个参数将近1900个，是Chinchilla比例的近100倍。",

    # ------------------------------------------------------------------ Data
    'Chapter eleven. When the data runs out.':
        '第11章。当数据用完。',

    'f"Good text is finite.':
        "好的文本是有限的。一个模型把它们全读完了，只能再读一遍时，会发生什么？每次都用{total / 1000000.0:.1f}百万个"
        "字符训练我们的字符模型，但这些字符来自越来越少的不同文本：从新文本读一遍，一直到一个小样本读256遍。"
        "<bookmark mark='a'/>{said1}读16遍的代价是{d16:.3f}比特。<bookmark mark='b'/>{said2}",

    "f'Four epochs cost only {d4:.3f} bits":
        "读4遍只多花{d4:.3f}比特：几乎和新文本一样好。",

    "f'Four epochs cost {d4:.3f} bits":
        "读4遍多花{d4:.3f}比特。",

    "f'At two hundred and fifty-six, the model memorizes":
        "读256遍时，模型背下了它的样本：留出数据上的损失先降后升，最后比新文本差{worst:.2f}比特。",

    "f'At two hundred and fifty-six, it ends":
        "读256遍时，它最后比新文本差{worst:.2f}比特。",

    'f"How much is a repeat worth?':
        "重复一遍值多少？2023年，尼克拉斯·明尼霍夫和同事提出了一个简单的答案。<bookmark mark='a'/>假设同一段文本"
        "每多读一遍，价值都比上一遍少一个固定的比例。<bookmark mark='b'/>那么U个不同的字符再读R遍，价值就是U加上"
        "一串越来越小的项，<bookmark mark='c'/>它会饱和：无论重复多少遍，得到的都不会超过U乘以1加R星。"
        "<bookmark mark='d'/>把我们的每次训练放到新数据的曲线上读一读，看它相当于多少新文本，再拟合R星：{Rs:.1f}遍。"
        "{said3}上限大约是不同文本的{cap:.0f}倍。",

    'f"Muennighoff\'s team, with models of up to nine billion':
        "明尼霍夫的团队，用最多90亿参数的模型，得到的是{Rp:.1f}。我们的小模型从重复中得到的更少，",

    'f"Muennighoff\'s team found {Rp':
        "明尼霍夫的团队得到的是{Rp:.1f}，",

    'How close are we? In 2024, Pablo Villalobos':
        "我们离那一步有多近？2024年，Epoch AI的巴勃罗·比利亚洛博斯和同事预测，考虑质量和重复后，2028年交汇点的可用公开"
        "文本存量大约是4乘以10的14次方个词元，训练集会在2026年到2032年之间达到这个量，最可能是2028年。"
        "<bookmark mark='a'/>重复可以把它拉长：明尼霍夫的4遍几乎不花代价。<bookmark mark='b'/>阿里巴巴的Qwen3在"
        "2025年用大约36万亿个词元做了预训练，其中包含合成数据。训练词元数不等于不同的人类文本数量。<bookmark mark='c'/>所以这个"
        "领域在寻找更多：改写的文本、合成的文本和其他种类的数据，这是第18部分的主题。",

    # ------------------------------------------------------------------ Experts
    'Chapter twelve. Experts and bits.':
        '第12章。专家与比特。',

    '"In a dense model, every parameter works on every character':
        "在稠密模型里，每个参数都作用于每个字符，所以算力和参数一起增长。第16部分将构建的混合专家放松了这种联系："
        "许多个专家，加上一个路由器，把每个字符送给其中一个。<bookmark mark='a'/>把我们模型的隐藏层拆成越来越多的"
        "专家，保持每个字符的计算量不变。{said1}<bookmark mark='b'/>DeepMind在2022年测量过这一点：损失随专家数下降，"
        "而基础模型越大，收益越小。从那以后，专家变得更小、更多：DeepSeek-V3每一层有256个专家，每个词元用其中8个。",

    "f'The loss keeps falling as the experts are added":
        "加入专家，损失持续下降，只是每加倍一次，帮助都更小。有8个专家时，它相当于一个大约{effN[i8]:,.0f}个参数的"
        "稠密模型，是我们基础模型的{mult:.1f}倍，却只花基础模型的算力。",

    'At our size the experts barely help':
        "在我们的规模上，专家几乎没有帮助：路由器没有多少东西可以区分。",

    '"Parameters also cost memory':
        "参数还要占内存，而用更少的比特存储它们，就能省下内存。训练之后，把我们训练好的模型的每个权重都取整到几个"
        "比特，量一量代价是多少。<bookmark mark='a'/>在宽度256上，{said2}<bookmark mark='b'/>拟合到我们所有的训练上，"
        "额外的损失像D的{gD:.2f}次方那样增长，像N的{gN:.2f}次方那样缩小，并且每多保留一个比特，就指数地下降。"
        "<bookmark mark='c'/>2024年，坦尼什克·库马尔和同事在465次训练里发现了同样的形式：过了某个点，更多的训练数据"
        "反而会让模型在量化之后变差。而用低精度来训练，本身就像参数变少了；按照他们的拟合，最好的训练精度是"
        "7到8个比特。",

    "f'the damage grows with training: at four bits,":
        "损伤随训练增长：在4比特时，读了2的{int(lD[okk][0])}次方个字符之后是{d4[okk][0]:.3f}比特，读了2的"
        "{int(lD[okk][-1])}次方之后是{d4[okk][-1]:.3f}。读得更多的模型，把更多的东西塞进了每个权重，所以取整对它"
        "伤害更大。",

    'the damage barely depends on how long':
        "损伤几乎不取决于模型训练了多久。",

    # ------------------------------------------------------------------ Power
    'Chapter thirteen. Why power laws?':
        '第13章。为什么是幂律？',

    '"Why should loss fall as a power law at all?':
        "损失为什么偏偏按幂律下降？一个答案来自乌特卡什·夏尔马和贾里德·卡普兰，2020年：真实的数据，位于它巨大的"
        "空间里的一个低维曲面附近，维数是d。一个有N个参数的模型，把这个曲面切成大约N块，<bookmark mark='a'/>所以"
        "每一块的宽度大约是N的负d分之一次方。<bookmark mark='b'/>每一块用一条直线去拟合，剩下的是曲率，也就是尺寸"
        "的平方。<bookmark mark='c'/>对平方损失再平方一次：损失像N的负d分之4次方那样下降。一条幂律，指数由数据的"
        "维数决定。<bookmark mark='d'/>来验证一下：在1维、2维、4维和8维的曲面上取一个光滑函数。{said1}低维的数据，"
        "陡的定律；按照这个说法，语言是高维的。",

    "f'The slopes match four over d, until eight":
        "斜率都和d分之4吻合，直到8维：在那里，即使十万多块也还太粗：{s8:.2f}，正在走向{t8:.2f}。",

    'The slopes match four over d.':
        "斜率都和d分之4吻合。",

    'f"A second answer, from Eric Michaud':
        "第二个答案来自埃里克·米肖、马克斯·泰格马克和同事，2023年：量子化模型。假设模型知道的东西，是一块一块"
        "离散的，叫作量子，每一块是一项技能，要么学会了，要么没学会；并且它们被使用的频率服从齐普夫定律，一条幂律。"
        "<bookmark mark='a'/>一个能装下n个量子的模型，学会最常用的n个，损失掉其余那些的份额。<bookmark mark='b'/>"
        "把一条幂律的尾巴加起来，就得到关于n的一条幂律，也就是关于模型大小的幂律。<bookmark mark='c'/>他们造了一个"
        "任务来检验它，我们做了一个小版本：{T}个子任务，每个是12个比特里3个隐藏比特的奇偶性，按齐普夫频率出现。",

    'f"Here is one network, of width {widths[wi]}':
        "这是一个宽度为{widths[wi]}的网络，在学这些子任务。<bookmark mark='a'/>每个子任务的损失先停在1比特，也就是"
        "抛硬币，然后突然下降。{said2}到最后，它学会了{T}个中的{n_learn}个。<bookmark mark='b'/>白色的是整个混合的"
        "平均，它是平滑的：许多突然的台阶，加在一起。<bookmark mark='c'/>在不同大小之间，越宽的网络学会的子任务越多，"
        "{said3}<bookmark mark='d'/>把平均损失画在学会的数目上，理论的曲线就出现了：混合中还没学会的那部分份额，"
        "一条幂律的尾巴。{said4}<bookmark mark='e'/>{said5}",

    'The common subtasks drop first, the rare ones later.':
        "常见的子任务先下降，稀有的后下降。",

    'The order roughly follows how common they are.':
        "顺序大致按照它们有多常见。",

    "f'from {lo} at width {widths[0]} to all {T}":
        "从宽度{widths[0]}的{lo}个，到宽度{full[0]}起的全部{T}个。",

    "f'from {lo} at width {widths[0]} to {int(":
        "从宽度{widths[0]}的{lo}个，到宽度{widths[-1]}的{int(learned[-1].max())}个。",

    'Ours sit a little below it':
        "我们的点略低于它，因为学会一半的子任务也已经算数了。",

    "f'With only {T} subtasks the tail runs out":
        "只有{T}个子任务，尾巴就会用完：全部学会之后，损失就掉到几乎为零。按照这个说法，语言有一条没有尽头的尾巴，"
        "技能越来越稀有。",

    'The rarest subtasks are still to come.':
        "最稀有的子任务还没轮到。",

    # ------------------------------------------------------------------ Emerge
    'Chapter fourteen. Emergence, or a mirage?':
        '第14章。涌现，还是幻象？',

    'In 2022, Jason Wei and colleagues at Google':
        "2022年，谷歌的杰森·魏和同事，收集了一批似乎随规模突然出现的能力：小模型没有，大模型有，所以无法从小模型"
        "预测出来。他们称之为涌现。<bookmark mark='a'/>2023年，斯坦福的赖兰·谢弗、布兰多·米兰达和桑米·科耶霍，"
        "把矛头指向了评分的方式。大多数能力的评分是全对或全错：整个答案是不是完全正确？<bookmark mark='b'/>在一个简单模型里，词元相互独立，"
        "每个词元正确的概率都是p，那么一个L个词元的答案完全正确的概率就是p的L次方。p平稳地上升，对长答案来说，就变成一条"
        "先平躺、后猛冲的曲线。<bookmark mark='c'/>换成平滑的评分，给同样的模型打分，跳跃就消失了：他们说，这是一个"
        "幻象，由度量造成。",

    'f"We can watch it happen on our own models.':
        "我们可以在自己的模型上看着它发生。任务是：从留出文本里的2000个位置开始，一字不差地写出接下来的字符。"
        "<bookmark mark='a'/>每个字符单独打分，正确的比例随大小平稳上升，从{100 * acc[0]:.0f}%到{100 * acc[-1]:.0f}%。"
        "<bookmark mark='b'/>改成给整个答案打分。一个字符：同样的曲线。两个、四个、八个：越来越低，越来越平，直到8个字符的"
        "答案几乎贴着零。{said1}<bookmark mark='c'/>在p的L次方这组曲线上，我们的模型位于平坦的那一段，p在"
        "{100 * acc[0]:.0f}%到{100 * acc[-1]:.0f}%之间。陡峭的部分需要p接近1：按这种方式在长答案上打分，一个模型看起来"
        "完全不会，直到大得多的时候，突然会了。",

    "f'Yet in proportion they grow fastest:":
        "但按比例算，它们增长得最快：在我们的大小范围内增长了{g8:.0f}倍，而单个字符只增长了{g1:.1f}倍。",

    'In proportion they grow about as fast as single characters.':
        "按比例算，它们和单个字符增长得差不多快。",

    '"But some suddenness is real.':
        "但有些突然是真的。在量子的玩具任务里，每个子任务要么解决了，要么没有。把每一个的最终损失画在网络的大小上，"
        "{said2}<bookmark mark='a'/>只有平均是平滑的。一个只测一项窄技能的基准，看到的是悬崖；而损失是对一切取平均，"
        "看到的是幂律。<bookmark mark='b'/>后来的研究让这一点变得有用。2024年，杜政晓和同事发现，能力在预训练损失"
        "降到某个阈值以下时出现，与模型大小无关；查理·斯内尔和同事则表明，微调能把一项能力提前带到更小的模型上，"
        "于是它的到来可以预测。",

    "f'and it falls off a cliff at its own size":
        "它会在自己的那个大小上跌下悬崖：平均有{100 * np.mean(drops):.0f}%的下降，发生在两个相邻的大小之间，常见的"
        "子任务先跌。",

    'and each one falls at its own size':
        "每一个都在自己的大小上下降，比平均陡得多，常见的子任务先降。",

    # ------------------------------------------------------------------ Grok
    'Chapter fifteen. Grokking.':
        '第15章。顿悟。',

    'f"In 2022, a team at OpenAI noticed something strange.':
        "2022年，OpenAI的一个团队注意到一件怪事。拿一个很小的任务：在一个有{P}个钟点的钟面上做加法，所以50加60"
        "等于13。<bookmark mark='a'/>给一个小网络看加法表的40%，让它填出其余的部分。",

    'f"It memorizes the entries it was shown':
        "它在大约{t_tr:,}步之内，就记住了给它看过的那些条目；而在很长一段时间里，它对没见过的条目，猜得并不比随机"
        "好。<bookmark mark='a'/>还是继续训练。训练到{ratio:.0f}倍那么久，在第{t_te:,}步，没见过的条目上的准确率"
        "猛地升到将近100%。网络找到了规则。他们把这叫作顿悟。<bookmark mark='b'/>{said1}权重衰减不停地挤压权重，"
        "而一张背下来的答案表，比规则要花更多的权重。",

    'Without weight decay, the same network does not get there within this run.':
        "没有权重衰减，同一个网络在这次实验结束前没达到这个水平。",

    "f'Without weight decay, it takes until step":
        "没有权重衰减，它要一直等到第{int(g['t_test_nowd']):,}步。",

    'f"Is weight decay really what drives it?':
        "推动它的真的是权重衰减吗？把它从0扫到3，每个值三个种子。<bookmark mark='a'/>记住训练条目，每次都要"
        "{np.nanmin(sm):,.0f}到{np.nanmax(sm):,.0f}步。<bookmark mark='b'/>泛化就不一样了。{said2}"
        "<bookmark mark='c'/>{said3}",

    "f'The more weight decay, the sooner it comes":
        "权重衰减越大，它来得越早：从{wds[ok[0]]:g}时的第{med[ok[0]]:,.0f}步，到{wds[ok[-1]]:g}时的第"
        "{med[ok[-1]]:,.0f}步。",

    'Its timing varies with the weight decay.':
        "它的时间随权重衰减而变。",

    "f'And in {n_never} of the {st.size} runs":
        "而在{st.size}次训练里，有{n_never}次，全都是权重衰减不超过{never_w:g}的，在{cap:,}步之内始终没有等到它。",

    '"What rule did it find?':
        "它找到的是什么规则？看看它为这些数学到的向量，问问它们包含了钟面上的哪些波：它们的傅里叶频谱。"
        "<bookmark mark='a'/>在训练过程中观察它。一开始，能量分散在所有频率上，是噪声。{said4}到最后，"
        "{100 * share[-1]:.0f}%的能量集中在{nf}个频率中的5个上。<bookmark mark='b'/>而这些数，沿着它们的主方向看，"
        "落到了圆上。",

    'Long before the unseen entries come right':
        "早在没见过的条目答对之前，就有几个频率开始悄悄地增长：",

    'As the unseen entries come right, a few frequencies take over':
        "随着没见过的条目答对，几个频率占了上风：",

    'f"Each number becomes a point on a circle':
        "每个数变成圆上的一个点，一个角度。<bookmark mark='a'/>在钟面上把两个数相加，就是把两个角相加；而和的余弦，"
        "是余弦与正弦的乘积之和，ReLU单元可以把它搭出来。<bookmark mark='b'/>于是每个答案c的分数，是一些波的和，"
        "这些波在c等于a加b的地方达到峰值。只用这5个波去拟合训练好的网络的分数：它们解释了{100 * r2:.0f}%的变化。"
        "尼尔·南达和同事在2023年弄清了这个回路，这是最早对一个训练好的网络在算什么的完整解释之一；第30部分会把"
        "这个想法用到真实的模型上。<bookmark mark='c'/>第2章的问题又回来了：这个网络是惰性的吗？{said5}",

    "f'Its tangent kernel barely moves while it memorizes":
        "它记忆的时候，正切核几乎不动；到泛化的时候，它走得很远，距离达到{after:.2f}。坦尼什克·库马尔和同事在2023年"
        "论证，顿悟正是这样：网络先用它的起始核惰性地拟合，然后慢慢学会能够泛化的特征。",

    'f"Measure how far its tangent kernel moves':
        "量一量它的正切核移动了多远：距离只有{after:.2f}，而且大部分发生在跃升之前。没有权重衰减时，它移动得更远，"
        "达到{kdn[-1]:.2f}，却始终没有泛化。坦尼什克·库马尔和同事在2023年论证，顿悟可以是从惰性训练到丰富训练的"
        "缓慢转变；在我们的网络里，单看核的移动，标不出顿悟的那一刻，起作用的是权重衰减。",

    "f'Its tangent kernel moves steadily through training":
        "它的正切核在整个训练中稳步移动，距离达到{after:.2f}。坦尼什克·库马尔和同事在2023年论证，顿悟可以是从惰性"
        "训练到丰富训练的缓慢转变，离开起始的核。",

    # ------------------------------------------------------------------ TestTime
    'Chapter sixteen. Scaling the answer.':
        '第16章。在回答时扩展。',

    'f"Scaling is often described as bigger models and more data.':
        "扩展规模常被描述为更大的模型和更多的数据。2024年，OpenAI的o1凸显了另一个轴：准确率随着模型回答前"
        "思考时间的对数平稳上升。第28部分会搭建推理模型。这里讲最简单的版本背后的数学：多次尝试，加一个检查器。"
        "<bookmark mark='a'/>在我们可以检查的任务上，给每个模型k次机会，通过采样写出接下来的{L}个字符，只要有一次"
        "完全正确，就算这道题解出来了。<bookmark mark='b'/>每个模型都随着尝试次数增加而解出更多，而且跨越5个数量级"
        "一直如此。<bookmark mark='c'/>2024年，布拉德利·布朗和同事在一个真实的模型上看到了同样的现象：在一个真实"
        "编程问题的基准上，250次尝试把它从15.9%提高到56%。",

    'f"Why a power law? For one problem':
        "为什么是幂律？对一道题，k次独立尝试全部失败的概率，是1减p的k次方：它指数下降，很快。<bookmark mark='a'/>"
        "但基准是对各种难度的题目取平均。<bookmark mark='b'/>如果很难的题，也就是p很小的那些，按p的b减1次方分布，"
        "平均的失败率就是一个伽马积分，它像k的负b次方那样下降：一条幂律，完全由最难的那些题造成。赖兰·谢弗和同事"
        "在2025年证明了这一点。<bookmark mark='c'/>在我们中等大小的模型上，负对数pass@k下降的斜率是{-b[i]:.2f}，"
        "{said1}",

    "f'and the share of problems with tiny p rises with slope":
        "而p很小的题目所占的比例，上升的斜率是{tb[i]:.2f}：两种不同的测量，得到同一个指数。",

    'f"and the tail of tiny p\'s has slope':
        "而p很小的那条尾巴，斜率是{tb[i]:.2f}：两个估计不同，而我们的2000道题对尾巴的采样很稀疏。",

    'f"So tries can stand in for size.':
        "所以尝试次数可以代替大小。一个小模型要尝试多少次，才能赶上最大模型的一次尝试？<bookmark mark='a'/>能赶上的"
        "最小模型需要大约{need[i_small]:,.0f}次，更大一些的需要得更少。{said2}这笔交易划不划算，取决于训练大模型的"
        "价钱，也取决于有没有检查器。<bookmark mark='b'/>用来训练推理模型的强化学习，也在扩大规模。2025年，Meta的"
        "德夫里特·卡特里和同事花了40万GPU小时寻找它的定律：奖励沿着一条S形曲线升向一个上限；在早期拟合，它就预测出"
        "了一次10万GPU小时的训练。<bookmark mark='c'/>同一年，xAI说它在Grok 4上做了与预训练同等规模的强化学习。",

    "f\"Counting the cost of answering, two operations per parameter per character, the small model's tries cost only":
        "算上回答的代价，每个参数每个字符2次运算，小模型的多次尝试，花费只有大模型一次尝试的{100 * ratio:.0f}%。",

    "f\"Counting the cost of answering, two operations per parameter per character, the small model's tries cost {":
        "算上回答的代价，每个参数每个字符2次运算，小模型的多次尝试，花费是大模型一次尝试的{ratio:.1f}倍。",

    # ------------------------------------------------------------------ Frontier
    'Chapter seventeen. Has pretraining stalled?':
        '第17章。预训练停滞了吗？',

    'Has pretraining stopped paying?':
        "预训练不再划算了吗？2024年12月，伊利亚·苏茨克维在这个领域最大的会议上说，我们所知的预训练将会终结："
        "算力在继续增长，但我们只有一个互联网。<bookmark mark='a'/>2025年2月，OpenAI发布了GPT-4.5，它迄今最大的"
        "模型，一次预训练的扩展。<bookmark mark='b'/>增长转到了别处：7月，xAI在Grok 4上做了与预训练同等规模的强化"
        "学习，<bookmark mark='c'/>Epoch AI估计，GPT-5用的训练算力很可能比GPT-4.5还少。<bookmark mark='d'/>然后在"
        "11月，谷歌发布了Gemini 3，奥里奥尔·维尼亚尔斯写道，它从预训练得到的提升，和他们见过的一样大。"
        "<bookmark mark='e'/>2026年7月，桑达尔·皮查伊说，下一个前沿需要大得多的基础模型，而Gemini 4正在训练中。"
        "<bookmark mark='f'/>10月，微软介绍了一个有2.8万亿参数的混合专家模型，它的性能是事先从一系列更小的模型"
        "预测出来的。",

    'f"What can a scaling law actually tell us?':
        "一条规模定律到底能告诉我们什么？像各个实验室用它们的定律那样，来检验我们的。只用我们最便宜的{n_fit}次训练"
        "拟合Chinchilla的公式，去预测另外{n_test}次，最贵的要贵上{ratio:.0f}倍。<bookmark mark='a'/>平均来说，预测"
        "偏差{err:.3f}比特，最差{mx:.3f}{said1}但这条曲线一向很慢。用卡普兰的算力指数0.05，损失减半需要100万倍的"
        "算力。争论的不是曲线，而是沿着它往下走的每一步，买到的能力值不值那个价钱。",

    ', with a small mean residual on these held-out runs.':
        "，在这些留出训练上的平均残差很小。<bookmark mark='b'/>这支持在我们的测量范围内外推，但不保证范围以外的趋势。",

    ', with predictions high on average:':
        "，预测平均偏高：更贵的训练，结果平均好于便宜训练拟合的预测。<bookmark mark='b'/>在这些留出实验中，较大规模训练相对预测没有出现平均意义上的减速。",

    ', with predictions low on average:':
        "，预测平均偏低：更贵的训练，平均达不到预测。<bookmark mark='b'/>在我们的小规模上，这说明了一种外推风险：小规模训练的拟合，可能承诺得比大规模训练兑现的更多。",

    'The other side of the ledger is efficiency.':
        "账本的另一边是效率。<bookmark mark='a'/>2024年，Epoch AI的安森·何和同事估计，达到某个给定语言模型性能所需"
        "的算力，大约每8个月减半，来自更好的架构、数据和训练。<bookmark mark='b'/>同一年，清华的肖朝军和同事测量了"
        "一条致密化定律：开源模型每个参数所装的能力，大约每3个月翻一番。<bookmark mark='c'/>所以前沿同时沿着三条"
        "曲线前进：预训练、强化学习、回答时的思考，每一条单独都很慢，每一条都有一条可以测量的定律。争论的是它们的"
        "价钱，而不是它们的形状。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来盘点一下。损失随着大小、数据和算力沿幂律下降，平滑得足以据此做计划。一个无限宽的网络，训练起来就像"
        "它自己的正切核，而核学不到特征。μP让每一层都一直在学，让一个学习率适用于每个宽度，加上CompleteP，还适用"
        "于每个深度。一份预算应该沿着Chinchilla山谷的谷底，在大小和数据之间分配，再向回答起来便宜的小模型弯折，"
        "并通过重复数据来拉长，而数据每重复一次就更不值钱。幂律可以来自低维曲面上的数据，也可以来自许多小技能，"
        "一次学会一项，每一项都学得突然。而一个网络可以先记忆，很久以后才理解：它把钟面上的算术变成了旋转。",

    'Act two ends here':
        "第二幕到这里结束，而这里的一切都会再回来。专家是第16部分。第18部分用全套配方训练一个模型：μP、批量大小、"
        "学习率计划和8位运算。第19部分讲回答的代价。第27和第28部分扩展强化学习和思考。顿悟的回路是第30部分的初尝，"
        "而预测模型将来能做什么，是第31部分。",

    'Here are six problems':
        "这里有6道题，从正切核到多次尝试的幂律。在这里暂停，把它们做一遍；完整的解答在本部分的笔记里。",

    'Next time, act three begins':
        "下一次，第三幕开始：Transformer时代。首先是注意力：每个词怎样回看前面的每个词，并决定哪些要紧，用几何来讲。"
        "<bookmark mark='a'/>我们还会搭一个自己的小Transformer。",

    'The Chinchilla paper is very readable':
        "Chinchilla的论文非常好读，而罗伯茨、亚伊达和哈宁的书，是宽网络理论的深水区。谢谢收看，第13部分见。",

    # ------------------------------------------------------------------ predict and takeaway beats
    'Pause and predict. Make the network a thousand times wider':
        '暂停一下，先想一想。把网络做宽一千倍，用同样的方式训练。每个权重移动得更多、更少，还是一样？核呢？',

    'The takeaway: an infinitely wide network is a Gaussian process':
        '要点：一个无限宽的网络，训练前是一个高斯过程，训练中是一台核机器，因为它的正切核冻结了。接下来：冻结的核做不到什么。',

    'Pause and predict. Two copies of one wide network':
        '暂停一下，先想一想。同一个宽网络的两份拷贝，同样的数据，同样的步数：一份用惰性的方式缩放，一份用平均场的方式。哪一份能学到那个隐藏方向？',

    'The takeaway: in the lazy limit, a network only re-weights':
        '要点：在惰性极限下，网络只是给它出发时的特征重新加权。要在任何宽度上学习特征，每个单元都必须一直在动，而这正是μP的设计目的。接下来，推导它。',

    'Pause and predict. Train at widths from sixty-four to four thousand':
        '暂停一下，先想一想。在从64到4000多的宽度上，用同一个学习率，按通常的做法训练。哪一层的变化会随宽度增长？',

    'The takeaway: random sums grow like the root of n':
        '要点：随机的和像n的平方根那样增长，同向的更新像n那样增长，所以μP让隐藏层的学习率像n分之一那样缩小，并让输出从很小开始。这样，每一层在每个宽度上都一直在学。接下来：一个学习率能不能适用于所有宽度？',

    'Pause and predict. As a model gets wider, the usual way':
        '暂停一下，先想一想。按通常的做法，模型变宽时，它的最佳学习率会变大、变小，还是不变？',

    'The takeaway: in mu-P, a learning rate tuned on a small model':
        '要点：在μP里，在小模型上调好的学习率，可以沿用到宽的模型上；大模型就是这样调参的，而不必在完整规模上去调。接下来，对深度问同样的问题。',

    'Pause and predict. With no scaling, every new block adds':
        '暂停一下，先想一想。不做缩放时，每个新的块都会往残差流里加东西。网络变深时，它的最佳学习率会上升，还是下降？',

    'The takeaway: how the residual branches are scaled':
        '要点：残差分支怎样缩放，决定了学习率能否在深度之间沿用，也决定了深处的块是否还在学习特征。接下来，第三个旋钮：批量。',

    'Pause and predict. Double the batch.':
        '暂停一下，先想一想。把批量加倍。要达到同样的损失，步数会减半、不变，还是介于两者之间？',

    'The takeaway: below the critical batch':
        '要点：低于临界批量时，更大的批量几乎不花代价就能减少步数；高于它时，只是浪费数据。而且临界批量会随着训练进行而增长。接下来，规模定律本身。',

    'Pause and predict. Our models are tiny':
        '暂停一下，先想一想。我们的模型很小，一次只读8个字符。它们的损失随大小下降，会比卡普兰的语言模型更快，还是更慢？',

    'The takeaway: loss falls toward a floor along a power law':
        '要点：损失沿着一条幂律落向一个下限，无论对大小还是对数据；即使指数随任务而变，曲线的形状也能延续。接下来，同时考虑两者，以及怎样分配一份预算。',

    'Pause and predict. Your budget grows tenfold.':
        '暂停一下，先想一想。你的预算增加到10倍。应该把模型做大10倍，用10倍的数据训练，还是两者各增加大约3倍？',

    'The takeaway: at the compute optimum, the last parameter':
        '要点：在计算最优点上，最后一个参数和最后一个词元的回报相等；对语言模型来说，这意味着大小和数据一起增长，每个参数大约20个词元。接下来：为什么最早的规模定律说的不一样。',

    'Pause and predict. Leave the embedding layers out':
        '暂停一下，先想一想。数参数时不算嵌入层。随着预算增长，最佳模型大小看起来会增长得更快，还是更慢？',

    'The takeaway: small choices, which parameters to count':
        '要点：一些小的选择，数哪些参数、预热多久、优化器怎么设，就把指数从0.73移到了大约二分之一，而重新拟合的结果仍有出入。规模定律是一次测量，带着误差棒。接下来：当计算最优点不是你想要的。',

    'Pause and predict. A model half the compute-optimal size':
        '暂停一下，先想一想。一个只有计算最优大小一半的模型，训练得更久，直到赶上最优模型的损失。它要多花多少训练算力：百分之几，一倍，还是十倍？',

    'The takeaway: once answering is counted':
        '要点：一旦把回答的代价算进去，最好的模型就比计算最优点更小，训练得也久得多；这就是为什么开源模型现在每个参数要读几千个词元。接下来：当没有足够的词元可读时，会发生什么。',

    'Pause and predict. Train for the same number of characters':
        '暂停一下，先想一想。训练同样多的字符，但只用四分之一的文本，读4遍。它会比一个一直读新文本的模型差多少？',

    'The takeaway: a few passes over the same data':
        '要点：把同样的数据读几遍，几乎和新数据一样好，但每重复一次就更不值钱，总量最终会饱和。接下来，另外两种预算：专家，和比特。',

    'Pause and predict. Round every weight to four bits':
        '暂停一下，先想一想。训练之后，把每个权重都取整到4个比特。谁受的损伤更大：读得少的模型，还是同一个模型读了多得多之后？',

    'The takeaway: parameters, compute and bits':
        '要点：参数、算力和比特可以分开权衡。专家增加参数，却不增加算力；更少的比特节省内存，代价却随模型读过的数据增长。接下来：为什么这些定律都是幂律。',

    'Pause and predict. If every skill is learned suddenly':
        '暂停一下，先想一想。如果每项技能都是突然学会的，要么全会，要么全不会，平均损失会一级一级地下降，还是平滑地下降？',

    'The takeaway: power laws come out of many parts':
        '要点：幂律来自许多部分的叠加：低维数据曲面上的一块块小片，或者一条长长的齐普夫技能尾巴，一项接一项地学会。接下来：如果技能是突然到来的，能力也是吗？',

    "Pause and predict. Our models' accuracy on single characters":
        '暂停一下，先想一想。我们的模型在单个字符上的准确率，随大小平稳上升。改成看它们能否一字不差地写对8个字符，那条曲线会是什么样？',

    'The takeaway: all-or-nothing scores':
        '要点：全对或全错的评分，会把平稳的进步变成表面上的跳跃，而窄的技能也确实可能突然出现。无论哪种情况，底下的损失都是平滑的，可以预测。接下来，最奇怪的一次跳跃。',

    'Pause and predict. With more weight decay':
        '暂停一下，先想一想。权重衰减更大时，理解会来得更早、更晚，还是根本不来？没有权重衰减呢？',

    'The takeaway: a network can fit its data long before':
        '要点：一个网络可以在找到规则之前很久，就拟合了它的数据；权重衰减把它推向规则，在这里，规则是一个小小的三角函数回路。第30部分会在真实的模型里寻找这样的回路。',

    'Pause and predict. For one problem, more tries':
        '暂停一下，先想一想。对一道题来说，多试几次的帮助是指数级的快。对整个基准取平均，失败率也会指数下降吗？',

    'The takeaway: with a way to check answers':
        '要点：只要有办法检查答案，多次尝试就能用回答时的算力换取模型的大小，而最难的那些题让收益变成一条缓慢的幂律。第28部分会搭建先思考再回答的模型。',

    'Pause and predict. Fit the law on our cheapest runs':
        '暂停一下，先想一想。只用我们最便宜的训练拟合定律，去预测贵10倍的训练。偏差会是百分之一比特、十分之一比特，还是更多？',

    'The takeaway: every axis of scale we can measure':
        '要点：我们能测量的每一个规模轴，都仍然遵循它的定律。争论的是下一步的价钱，而这个价钱一直在下降。现在，来回顾一下。',

}

PHRASES = {
    'worse': '差',
    'better': '好',
    'toward the model': '偏向模型',
    'toward the data': '偏向数据',
    'over': '高',
    'under': '低',
    'no scaling at all': '完全不缩放',
    'one over root L': 'L的平方根分之一',
    'CompleteP': 'CompleteP',
    'lower': '更低',
    'higher': '更高',
    'the same': '一样',
    '2, 4, 8, 16': '2、4、8、16',
    '2, 4, 8': '2、4、8',
    'Ours sit on it. ': '我们的点正落在它上面。',
    'Ours sit on it.': '我们的点正落在它上面。',
    "Kaplan's was 0.73. ": '卡普兰的是0.73。',
    "Kaplan's was 0.73.": '卡普兰的是0.73。',
}
