"""Chinese narration for ai10: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第10部分：看见与记住'

CHAPTERS = {
    'Hook': '点亮一个神经元的那条边缘',
    'Before': '1. 深度学习之前的视觉',
    'Convolution': '2. 卷积',
    'Receptive': '3. 感受野、步长与池化',
    'LeNet': '4. LeNet与MNIST',
    'ImageNet': '5. ImageNet与AlexNet',
    'WhyItWon': '6. AlexNet为什么赢了',
    'Deeper': '7. 更深：VGG、Inception、ResNet',
    'Filters': '8. 滤波器学到了什么',
    'Adversarial': '9. 对抗样本',
    'Efficient': '10. 更便宜的卷积',
    'Recurrence': '11. 循环与梯度消失',
    'LSTM': '12. LSTM与GRU',
    'CharLSTM': '13. 字符级LSTM',
    'Seq2Seq': '14. 序列到序列',
    'Attention': '15. 注意力的诞生',
    'Return': '16. 循环的回归',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'In the late 1950s, at Johns Hopkins, David Hubel and Torsten Wiesel':
        "20世纪50年代末，在约翰斯·霍普金斯大学，大卫·休伯尔和托斯滕·威泽尔一边让一只猫看着屏幕，一边记录它视觉皮层里单个神经元的放电。<bookmark mark='a'/>光点，当时常用的刺激，几乎不起作用。<bookmark mark='b'/>后来，照休伯尔的说法，他们往投影仪里插一张玻璃幻灯片时，片子边缘那道淡淡的直线阴影扫过了屏幕，<bookmark mark='c'/>这个细胞突然一阵猛烈放电。它要的是一条边缘：某个特定的角度，某个特定的位置。",

    'f"Decades later, here is a network trained on the computer making this video.':
        "几十年以后，这是一个在制作本视频的计算机上训练出来的网络。它看了五万张小照片，看了{cf['epochs']}遍，用了大约{mins:.0f}分钟。<bookmark mark='a'/>这些是它的第一层长出来的滤波器。<bookmark mark='b'/>{o['n']}个里有{o['n_oriented']}个专挑某一个方向的边缘，就像休伯尔和威泽尔的那个细胞。没有人告诉它什么是边缘。它找到边缘，是因为边缘有用。",

    'Seeing is half of this part. The other half is remembering.':
        "看见，是本部分的一半。另一半是记住。<bookmark mark='a'/>2014年，网络学会了读完一整句话，再用另一种语言把它写出来。<bookmark mark='b'/>也是那一年，它们学会了回头看：每写一个词，就去挑出输入里需要的那几个词。这是一个小网络，在这里训练来把字符串倒过来写；亮的方格是它看的地方。这就是神经机器翻译中的注意力。",

    'How did machines learn to see, and to remember?':
        "机器是怎样学会看见、学会记住的？<bookmark mark='a'/>我们会沿着这条路走：从休伯尔和威泽尔的细胞，到LeNet、ImageNet，再到一百五十层深的网络。<bookmark mark='b'/>然后是时间：循环网络、LSTM、翻译，还有从中长出来的注意力。<bookmark mark='c'/>我们遇到的每一种网络，都会在这台计算机上亲手训练，看着它学。",

    'This is Part 10 of AI, Built, in the second act':
        "这是《人工智能，从零搭建》的第10部分，属于第二幕：从数据中学习，排在第9部分的网络之后、第11部分的优化器之前。<bookmark mark='a'/>本部分的计划是：深度学习之前的视觉，以及取代它的卷积；深度网络，它们学到了什么，又怎样骗过它们；然后是记忆，从LSTM到注意力，再回到循环。",

    # ------------------------------------------------------------------ Before
    'Chapter one. Vision before deep learning.': '第1章。深度学习之前的视觉。',

    'In 1962 Hubel and Wiesel sorted the cells they found into two kinds.':
        "1962年，休伯尔和威泽尔把他们找到的细胞分成了两类。<bookmark mark='a'/>简单细胞对某个角度的边缘或线条有反应，而且只在眼睛所见的一小块区域里：光落在它亮的条带上会兴奋它，落在条带旁边会抑制它。<bookmark mark='b'/>复杂细胞对同一个角度有反应，但可以在更大区域里的任何地方，好像它收集了好几个简单细胞，只要其中任何一个放电，它就放电。<bookmark mark='c'/>先检测一个特征，再在位置上汇合，然后一层又一层地重复。这幅图景让他们在1981年获得了诺贝尔奖，它几乎就是本部分这些网络的设计。",

    'Computer vision began the same way, with edges.':
        "计算机视觉也是这样起步的：从边缘开始。边缘就是亮度变化很快的地方，所以对图像求导。<bookmark mark='a'/>实际上，就是两侧像素之差除以它们的间距，横向和纵向各算一次。<bookmark mark='b'/>在一个手写数字上，每个箭头都指向亮度上升的方向，横穿笔画。<bookmark mark='c'/>在一张照片上，梯度的长度，用欧文·索贝尔1968年的算子来算，勾出了马的轮廓。几十年里，每个视觉系统都从这里开始。",

    'Then came the descriptors.':
        "接着是描述子。把图像切成小格，在每一格里按角度数边缘，每条边按它的强度加权。<bookmark mark='a'/>这是我们那个数字的计数：每颗星是九个方向的直方图，长的辐条沿着笔画。<bookmark mark='b'/>大卫·罗的SIFT，2004年完整发表，在每一个尺度上找出有区分度的点，每个点用128个这样的计数来描述。<bookmark mark='c'/>纳夫尼特·达拉尔和比尔·特里格斯2005年的方向梯度直方图，覆盖整个窗口，按块归一化，用来找行人。这样数出来的图像，经得起小的平移和光照变化。",

    'By 2010 a good vision system was a pipeline.':
        "到2010年，一个好的视觉系统是一条流水线。<bookmark mark='a'/>像素进去；SIFT这样的手工特征出来，在成千上万个地方计算；它们被汇合成一个长向量，再交给一个线性分类器，通常是第6部分的支持向量机。<bookmark mark='b'/>只有最后一个方框从数据中学习。它前面的一切，都是人花了几十年设计出来的。<bookmark mark='c'/>这样的系统赢下了2010年和2011年的头两届ImageNet比赛，猜五次，大约四分之一的时候都猜不中正确答案。",

    'f"We can measure what the features buy.':
        "我们可以量一量这些特征换来了什么。<bookmark mark='a'/>把同一个线性分类器训练两次，一次用原始像素，一次用我们的方向梯度直方图。在数字上，像素给出{pct(e['mnist_pixels'])}%的错误；直方图给出{pct(e['mnist_hog'])}%，少了大约{gain:.0f}倍。<bookmark mark='b'/>{photo}<bookmark mark='c'/>那个时代的教训是：{verdict}<bookmark mark='d'/>本部分剩下的内容要回答的问题是：如果特征也是学出来的呢？",

    "f'On the photographs it helps too, from {pct(e[\'cifar_pixels\'], 0)} to {pct(cw, 0)} percent wrong, but":
        "在照片上它也有帮助，错误率从{pct(e['cifar_pixels'], 0)}%降到{pct(cw, 0)}%，但错的次数仍然和对的差不多。",

    "f'On the photographs it helps too, from {pct(e[\'cifar_pixels\'], 0)} to {pct(cw, 0)} percent wrong, though":
        "在照片上它也有帮助，错误率从{pct(e['cifar_pixels'], 0)}%降到{pct(cw, 0)}%，不过照片仍然比数字难得多。",

    "f'On the photographs it barely helps":
        "在照片上它几乎没有帮助：像素错{pct(e['cifar_pixels'], 0)}%，这些特征错{pct(cw, 0)}%。",

    'the gap between digits and photographs':
        "数字和照片之间的差距，正是那些流水线在整个2000年代努力弥补的，靠的是更丰富的特征和多得多的图像。",

    # ------------------------------------------------------------------ Convolution
    'Chapter two. Convolution.': '第2章。卷积。',

    'f"Suppose a network should find a short stroke in a digit.':
        "假设一个网络要在数字里找一小段笔画。一个全连接单元给每个像素都配一个权重，<bookmark mark='a'/>所以要在任何地方都找到这段笔画，网络就得为它可能出现的每个位置各学一个检测器。<bookmark mark='b'/>一个卷积单元只看一小块，五个像素乘五个像素，<bookmark mark='c'/>而且一张特征图上的每个单元都用同样的二十五个权重，在图像上滑过去。<bookmark mark='d'/>要得到六张和数字一样大的图，全连接单元需要{e['params_dense'] / 1000000.0:.1f}百万个权重；不共享的局部小块需要{e['params_local']:,}个；共享的，只要{e['params_conv']}个。共享就是全部的想法：同一个图案可以出现在任何地方，所以在每个地方都用同一种方式去找它。",

    'f"Here is the operation.':
        "运算是这样的。<bookmark mark='a'/>把一小格权重，也就是卷积核，盖在图像的一小块上；每个权重乘以它下面的像素，再全部加起来。这就是输出的一个数。<bookmark mark='b'/>把卷积核挪一个像素，再做一遍，一行一行地走，直到走遍每一个位置。<bookmark mark='c'/>输出是一张特征图：哪里的小块像这个卷积核，哪里就亮。{likes}<bookmark mark='d'/>严格地说，这是互相关；数学家的卷积要先把卷积核翻转，不过学出来的卷积核并不在乎。",

    'This kernel was learned, and it likes the bottom edges': '这个卷积核是学出来的，它喜欢笔画的下边缘。',
    'This kernel was learned, and it likes the top edges': '这个卷积核是学出来的，它喜欢笔画的上边缘。',
    'This kernel was learned, and it likes the right-hand edges': '这个卷积核是学出来的，它喜欢笔画的右边缘。',
    'This kernel was learned, and it likes the left-hand edges': '这个卷积核是学出来的，它喜欢笔画的左边缘。',
    'This kernel was learned, and it likes the edges of strokes at a slant': '这个卷积核是学出来的，它喜欢斜着的笔画边缘。',
    'This kernel was learned, and it likes strokes and their edges': '这个卷积核是学出来的，它喜欢某一个特定角度的笔画和笔画边缘。',
    'This kernel was learned, and what it likes': '这个卷积核是学出来的，它喜欢的东西不只是一条边缘那么简单。',

    'Sharing the weights buys a precise property':
        "共享权重换来一个精确的性质：平移图像，特征图也跟着平移。<bookmark mark='a'/>用T s表示平移s。平移后图像在位置i的卷积，是权重乘以平移后图像之和。<bookmark mark='b'/>平移后的图像在i加u处，就是原图在i加u减s处。<bookmark mark='c'/>这个和，正是原图在i减s处的卷积。<bookmark mark='d'/>也就是平移后的特征图，对任何卷积核都成立，不管是不是学出来的。<bookmark mark='e'/>在二维里论证一样；图像首尾相接时它严格成立，用零填充时在边界以外成立。",

    'f"Let\'s check it on our digit.':
        "在我们的数字上验证一下。<bookmark mark='a'/>先卷积，再平移；<bookmark mark='b'/>或者先把数字往下移{abs(sy)}个像素、往左移{abs(sx)}个像素，再卷积。<bookmark mark='c'/>{v1}<bookmark mark='d'/>用零填充时，两张图除了边界上一窄条以外处处相同，那里平移后的图像丢掉了像素。<bookmark mark='e'/>同样形状的全连接层没有这个恒等式：它的两条路线相差了输出大小的{e['err_dense']:.1f}倍。等变性，正是权值共享换来的。",

    'f"With the image wrapping around, the two routes differ by about':
        "图像首尾相接时，两条路线相差大约是特征图最大值的{mant}乘以10的负{-ex}次方：只是算术最后几位的舍入误差。",

    'With the image wrapping around, the two routes agree exactly':
        "图像首尾相接时，两条路线完全一致，连最后一位都相同。",

    'f"With the image wrapping around, the two routes differ by {err':
        "图像首尾相接时，两条路线相差特征图最大值的{err:.2g}。",

    # ------------------------------------------------------------------ Receptive
    'Chapter three. Receptive fields, stride and pooling.': '第3章。感受野、步长与池化。',

    'One unit of the first layer sees three pixels by three.':
        "第一层的一个单元看三个像素乘三个像素。<bookmark mark='a'/>第二层的一个单元看第一层的三乘三个单元，而它们各自又看自己的三乘三，所以合起来覆盖五乘五个像素。<bookmark mark='b'/>第三层，七乘七。这就是单元的感受野：图像里能改变它的那一部分。叠起来，感受野组成一个锥体。",

    'We can count the cone exactly.':
        "我们可以精确地数出这个锥体。<bookmark mark='a'/>给卷积核大小、步长、相邻单元之间相隔的像素数和感受野各起个名字。<bookmark mark='b'/>大小为k的卷积核，多够到下一层k减1个单元，它们相隔j个像素：感受野增加k减1乘以j。<bookmark mark='c'/>步长会把间隔乘上去。<bookmark mark='d'/>展开来：1，加上每一层多出的抽头数乘以它前面所有步长的乘积。<bookmark mark='e'/>步长之后的每一层，都分量更重。",

    'f"Apply the rule to real networks, layer list by layer list.':
        "把这条规则用到真实的网络上，一份层列表接一份层列表。<bookmark mark='a'/>LeNet-5的最后一个卷积看{t['LeNet-5'][-1][4]}个像素见方：整个输入。<bookmark mark='b'/>AlexNet最后的池化层看{a}个像素，VGG-16是{v}，ResNet-50是{r50}：{cover}<bookmark mark='c'/>我们自己的CIFAR网络，第8章会见到，在32像素的照片上达到{t['our CIFAR network'][-1][4]}个像素。",

    '"Two more ingredients shrink the maps as they go up.':
        "还有两个成分让特征图越往上越小。<bookmark mark='a'/>池化：在每个2乘2的块里只留最大值，然后移动2格。在块里把一个特征挪一个像素，池化后的输出不变：一点点不变性，又是休伯尔和威泽尔的复杂细胞。<bookmark mark='b'/>但步长为2会打破上一章那种精确的等变性。<bookmark mark='c'/>我们把数字在送进第一层和它的池化之前，平移了一到四个像素。{mid}<bookmark mark='d'/>2019年，阿哈龙·阿祖莱和亚伊尔·魏斯证明，平移一个像素就能改变现代网络的答案；理查德·张则证明，在每次步长之前先模糊一下，大体就能修好。",

    'all wider than the 224-pixel images':
        "都比它们训练用的224像素的图像还宽，所以顶层的一个单元原则上可以被任何一个像素改变。",

    'AlexNet and VGG-16 see most of the 224-pixel images':
        "AlexNet和VGG-16能看到它们训练用的224像素图像的大部分，ResNet-50则比整张图还宽：它顶层的一个单元，原则上可以被任何一个像素改变。",

    'against images 224 pixels wide.':
        "而图像宽224像素。",

    'A shift by 2 or 4 pixels comes out as an exact shift':
        "平移2个或4个像素，池化后的图恰好平移了一格。平移1个或3个像素就不行：池化后是另一张图，偏差占了它的值的很大一部分。",

    'Here the pooled maps after odd and even shifts differ by similar amounts.':
        "这里，奇数和偶数平移之后的池化图，偏差差不多。",

    # ------------------------------------------------------------------ LeNet
    'Chapter four. LeNet and MNIST.': '第4章。LeNet与MNIST。',

    'f"The first network built on Hubel and Wiesel\'s plan came from Japan.':
        "第一个按休伯尔和威泽尔的蓝图搭起来的网络，来自日本。<bookmark mark='a'/>1980年，福岛邦彦的新认知机把S细胞层和C细胞层叠起来，仿照简单细胞和复杂细胞，即使数字被平移了也能认出来。但它不用反向传播学习，而是按自己的一套规则。<bookmark mark='b'/>1989年，在贝尔实验室，杨立昆和同事用反向传播端到端地训练了一个卷积网络，梯度穿过共享的权重，数据是真实邮政编码里的数字：{ZIP1989['train']:,}个用来训练，测试数字上的错误率是{ZIP1989['error']:.0f}%。<bookmark mark='c'/>同一年，亚历克斯·魏贝尔的团队把共享权重沿着时间滑动。",

    'f"By 1998 the design had a name and a benchmark.':
        "到1998年，这个设计有了名字，也有了基准。<bookmark mark='a'/>LeNet-5，出自杨立昆、莱昂·博图、约书亚·本吉奥和帕特里克·哈夫纳：两轮卷积和池化，先六张特征图再十六张，然后三个全连接层，收到十个数字。<bookmark mark='b'/>还有MNIST，七万个手写数字，由美国政府的两批数据重新混合而成，一批出自人口普查局的雇员，一批出自高中生。<bookmark mark='c'/>LeNet-5在{LENET5_1998}%的测试数字上出错，用变形的副本训练时是{LENET5_DISTORT}%；围绕它搭起的系统进了银行，每天读几百万张支票。<bookmark mark='d'/>我们搭了同样的结构，换上今天的ReLU和最大池化。",

    'f"Now let\'s watch ours learn.':
        "现在看我们的网络怎样学。左边是它的测试错误率；右边是它第一层的六个卷积核、它们对一个数字的反应，以及它的回答。<bookmark mark='a'/>一开始，卷积核是随机的噪声，回答是瞎猜：错{pct(e0, 0)}%。<bookmark mark='b'/>{fast}<bookmark mark='c'/>把训练数字过了{L['epochs']}遍之后，错{pct(eN, 2)}%。{kern}这些卷积核没有人设计：凡是能让答案正确的，就是它们。",

    "f'Within {steps[i_half]:,} steps, under five percent wrong.'":
        "不到{steps[i_half]:,}步，错误率就降到5%以下。",

    "f'Even after {steps[i_half]:,} steps it is {pct(errs[i_half], 0)} percent wrong.'":
        "即使过了{steps[i_half]:,}步，它仍然错{pct(errs[i_half], 0)}%。",

    "f'Of the six kernels, {nN} now match a bar or an edge, each at a different angle":
        "六个卷积核中，现在有{nN}个和一条亮带或一道边缘吻合，各在不同的角度；一开始只有{n0}个。",

    "f'Of the six kernels, {nN} match a bar or an edge; at the start":
        "六个卷积核中有{nN}个和一条亮带或一道边缘吻合；一开始有{n0}个。",

    'f"Over three training runs with different random starts':
        "三次从不同随机起点出发的训练，我们的网络在{pct(m, 2)}%的测试数字上出错，范围在{pct(lo, 2)}%到{pct(hi, 2)}%之间：{cmp}<bookmark mark='a'/>这是它错掉的一些数字。其中好几个，人看了也会犹豫。",

    'f"a little better than LeNet-5\'s':
        "比1998年LeNet-5的{LENET5_1998}%好一点：今天的ReLU和Adam，还有一万倍的算力，帮了忙。",

    'f"a little worse than LeNet-5\'s':
        "比LeNet-5的{LENET5_1998}%差一点；我们只把数字过了{L['epochs']}遍。",

    "f'about where LeNet-5 was in 1998":
        "和1998年的LeNet-5差不多，{LENET5_1998}%。",

    'f"Is it the convolution that helps, or just the training?':
        "帮了忙的到底是卷积，还是只是训练？公平地比一比：换一个同样大小的全连接网络，{M['params']['mlp']:,}个权重对{M['params']['cnn']:,}个，用同样的方式训练，各训练三次。<bookmark mark='a'/>在普通的测试数字上：卷积网络错{pct(ec.mean(), 2)}%，另一个错{pct(em.mean(), 2)}%。<bookmark mark='b'/>{shifted_v}两者都不是严格平移不变的：LeNet顶部的全连接层是看位置的。<bookmark mark='c'/>而对这个假设最干净的检验是这样的。{perm_v}",

    'f"Shuffle the pixels, the same way in every image':
        "把像素打乱，每张图都用同一种打乱方式，然后重新训练两个网络。全连接网络毫不在乎：之前{pct(np.mean(P['mlp_plain']))}%，之后{pct(np.mean(P['mlp']))}%，因为在它眼里，像素本来就没有顺序。卷积网络则从{pct(np.mean(P['cnn_plain']))}%掉到{pct(np.mean(P['cnn']))}%：它的假设，相邻的像素属于一起，现在不成立了。",

    'Shuffle the pixels and retrain both: here':
        "把像素打乱再重新训练两个网络：这里卷积网络损失不大。",

    "f'Shift the test digits by three pixels and the network of fully connected units":
        "把测试数字平移三个像素，全连接网络的错误率从{pct(em.mean())}%升到{pct(sm[:, 3].mean(), 0)}%；卷积网络升到{pct(sc[:, 3].mean(), 0)}%。",

    "f'Shift the test digits by three pixels and both suffer":
        "把测试数字平移三个像素，两个都吃亏：分别错{pct(sm[:, 3].mean(), 0)}%和{pct(sc[:, 3].mean(), 0)}%。",

    # ------------------------------------------------------------------ ImageNet
    'Chapter five. ImageNet and AlexNet.': '第5章。ImageNet与AlexNet。',

    'f"In 2009 Fei-Fei Li, then at Princeton':
        "2009年，当时在普林斯顿的李飞飞和她的学生发布了ImageNet。<bookmark mark='a'/>想法是为WordNet里的每个名词收集图片，WordNet是一部按意义组织成树的英语词典；图片从网上搜来，再由通过亚马逊土耳其机器人众包平台付费的人一张张核对。<bookmark mark='b'/>从2010年起，每年有一场比赛，用它的一千个类别：{n_tr:,}张训练照片，每张测试图允许猜五次。<bookmark mark='c'/>数一数网络要学习的数，图像数乘以像素值数，ImageNet比赛大约是MNIST的{ratio:,.0f}倍：大了几千倍，也乱得多。",

    'f"The first two contests went to pipelines like the ones in Chapter 1':
        "头两届比赛的冠军，都是第1章那样的流水线：2010年前五错误率{ILSVRC[0][2]}%，2011年{ILSVRC[1][2]}%。<bookmark mark='a'/>2012年，第二名来自东京大学，用的是SIFT和其他特征，达到{ILSVRC_2012_SECOND[1]}%。<bookmark mark='b'/>冠军以SuperVision的名义参赛，出自亚历克斯·克里热夫斯基、伊利亚·苏茨克维和杰弗里·辛顿，达到{ILSVRC[2][2]}%，用额外的训练图片时是{ALEXNET_EXTRA}%。比第二名好了将近十个百分点，而这个比赛一年的进步通常只有一两个点。<bookmark mark='c'/>这个网络后来被叫作AlexNet。第17部分会解释它是怎样在两块游戏显卡上训练出来的；这里讲它里面有什么。",

    'f"AlexNet was LeNet\'s design, grown.':
        "AlexNet就是长大了的LeNet。五个卷积层，第一层是96个11乘11像素的卷积核，步长为4；然后三个全连接层，最后是一个一千类的softmax。<bookmark mark='a'/>按公开的层列表数它的权重：{S['params']:,}个。其中只有{100 * pc:.0f}%在卷积层里；光是第一个全连接层就有{params[5] / 1000000.0:.0f}百万个。<bookmark mark='b'/>再数每张图的算术量：{S['macs'] / 1000000.0:,.0f}百万次乘加，其中{100 * mc:.0f}%在卷积层里，因为它们那几个权重在每个位置都要用一次。<bookmark mark='c'/>权重住在全连接层，工作在卷积层：这种分工，在它之后的每个网络里都会再出现。",

    "AlexNet didn't come from nowhere.":
        "AlexNet不是凭空出现的。<bookmark mark='a'/>2011年，于尔根·施密德胡伯实验室的丹·奇雷尚和同事，已经用GPU上的卷积网络赢下了好几场比赛，在交通标志识别上超过了人类测试者的平均水平。<bookmark mark='b'/>2012年，多伦多、微软、谷歌和IBM的团队联合报告：深度网络打败了老的语音模型。<bookmark mark='c'/>但ImageNet才是视觉界在乎的基准，整个领域立刻转了向：2013年，几乎每个参赛队都交了一个卷积网络。<bookmark mark='d'/>后来，本吉奥、辛顿和杨立昆共同获得了2018年度的图灵奖。",

    # ------------------------------------------------------------------ WhyItWon
    'Chapter six. Why AlexNet won.': '第6章。AlexNet为什么赢了。',

    'f"The first difference inside AlexNet is small: the activation.':
        "AlexNet里面的第一个不同之处很小：激活函数。<bookmark mark='a'/>20世纪90年代的网络用tanh或sigmoid把每个单元压扁。AlexNet用的是修正线性单元：输入为负时是零，否则就是输入本身。<bookmark mark='b'/>原因在斜率上：反向传播在每一层都要把梯度乘以激活函数的斜率。sigmoid的斜率最多四分之一，而且它和tanh一旦被推离零点太远，就平得什么都不剩：单元饱和了，停止学习。ReLU的斜率，只要它是开着的，就是1。<bookmark mark='c'/>克里热夫斯基在CIFAR-10上量过：一个四层网络，用ReLU达到25%训练错误率，比同样的网络用tanh快了{ALEXNET['relu_speedup']}倍。",

    'f"We ran the race ourselves, on the digits':
        "我们自己在数字上比了一场：同一个六层卷积网络，每种激活函数各训练三次，像AlexNet那样用带动量的普通梯度下降。<bookmark mark='a'/>虚线是{int(100 * thr)}%的训练错误率。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{sig}",

    "f'The sigmoid networks are still at":
        "我们停下时，sigmoid网络的测试错误率还在{pct(test['sigmoid'], 0)}%：它那很小的斜率，一层又一层地乘下去，让最前面几层得不到梯度。",

    "f'Even the sigmoid gets there":
        "连sigmoid也到了，用了{rs:.0f}步。",

    "f'ReLU gets there in about":
        "ReLU大约用了{rr:.0f}步到达，tanh用了{rt:.0f}步：是它的{ratio:.1f}倍。",

    "f'ReLU and tanh get there in about the same time":
        "ReLU和tanh到达的时间差不多，{rr:.0f}步和{rt:.0f}步：在这个深度、有好的初始化时，tanh跟得上。差距要在更深的网络里才拉开。",

    'Not every run gets there within our budget.':
        "不是每次训练都能在我们的预算内到达。",

    'f"The second ingredient: dropout':
        "第二个成分：随机失活（dropout），同一年出自辛顿的团队。<bookmark mark='a'/>每一步训练，每个隐藏单元都以二分之一的概率被关掉，这样网络就不能依赖少数几个单元的勾结；测试时全部打开，按比例缩小。这就像在对一个巨大的、共享权重的瘦网络家族取平均。AlexNet把它用在两个大的全连接层里。<bookmark mark='b'/>我们只给一个全连接网络五千个数字，让它训练六十遍。不用随机失活，它把每个训练数字都学会了，在它们上面只错{pct(vals['0.0'][0])}%，而测试错误率停滞不前。<bookmark mark='c'/>{verdict}训练和测试之间的差距，从{pct(gap0)}个百分点缩小到{pct(gap5)}个。",

    "f'With dropout the test error ends at":
        "用了随机失活，测试错误率最后是{pct(vals['0.5'][1])}%，而不是{pct(vals['0.0'][1])}%。",

    "f'Here dropout changes the test error little":
        "这里随机失活对测试错误率影响不大：{pct(vals['0.5'][1])}%对{pct(vals['0.0'][1])}%。",

    'f"The third ingredient was the one ImageNet supplied: data.':
        "第三个成分是ImageNet提供的：数据。<bookmark mark='a'/>用同样的步数，在越来越多的数字上训练同一个LeNet。{law}<bookmark mark='b'/>还有一个便宜的办法得到更多数据：自己造。AlexNet在照片的随机裁剪和它们的镜像上训练，每张有{ALEXNET['augment_factor']:,}种变体。{aug_v}",

    'f"On a log-log plot the test error first falls':
        "在对数-对数图上，测试错误率先沿着一条直线下降，是一条斜率约为负{abs(s3):.2f}的幂律：数据每翻一倍，错误就减少{100 * (1 - 2 ** s3):.0f}%。然后这条线弯平了：在{int(d['steps']):,}步里，{sizes[-1]:,}个数字每个只被看到{passes:.1f}遍，网络用不上全部数据。",

    "f'On a log-log plot the test error falls along":
        "在对数-对数图上，测试错误率沿着一条直线下降，是一条斜率约为负{abs(slope):.2f}的幂律：数据每翻一倍，错误就减少{100 * (1 - 2 ** slope):.0f}%。第12部分讲的就是这样的直线。",

    "f'Shifted copies help: with {sizes[1]:,} digits, {pct(e_small)} percent wrong becomes {pct(e_small_aug)}, better":
        "平移的副本有帮助：用{sizes[1]:,}个数字时，{pct(e_small)}%的错误率降到了{pct(e_small_aug)}%，比四倍的真实数字还好。",

    "f'Shifted copies help: with {sizes[1]:,} digits, {pct(e_small)} percent wrong becomes {pct(e_small_aug)}, though":
        "平移的副本有帮助：用{sizes[1]:,}个数字时，{pct(e_small)}%的错误率降到了{pct(e_small_aug)}%，不过比不上四倍的真实数字，那是{pct(e_next)}%。",

    'Shifted copies barely help at this size.':
        "在这个规模上，平移的副本几乎没有帮助。",

    'So which ingredient mattered?':
        "那么哪个成分才重要？<bookmark mark='a'/>2012年时，它们没有一个是新的：修正线性单元来自2010年，随机失活来自那一年，卷积网络来自1989年，GPU和ImageNet来自2009年。<bookmark mark='b'/>新的是它们全部合在一起，而且在每一样都起作用的规模上：数据多到六千万个权重不能简单地背下来，算力足够在一周内训练完。",

    # ------------------------------------------------------------------ Deeper
    'Chapter seven. Deeper: VGG, Inception, ResNet.': '第7章。更深：VGG、Inception、ResNet。',

    'f"After 2012 the contest became a race to go deeper.':
        "2012年以后，这场比赛变成了比谁更深。<bookmark mark='a'/>历年冠军的错误率：AlexNet的八层是{ILSVRC[2][2]}%；2013年{ILSVRC[3][2]}%；2014年{ILSVRC[4][2]}%，二十二层；2015年{ILSVRC[5][2]}%，一百五十二层。<bookmark mark='b'/>2014年，安德烈·卡帕西自己练习了这项任务，亲手给测试图片打标签：他错了{HUMAN_TOP5}%。2015年，网络超过了他。<bookmark mark='c'/>到比赛的最后一年，2017年，冠军只错{ILSVRC[-1][2]}%。<bookmark mark='d'/>后来，本杰明·雷希特和同事按同样的方式重新收集了一个测试集，表现最好的分类器，前五准确率从96%降到90%，首选准确率从83%降到72%。排名几乎没变。第31部分会讨论基准能告诉我们什么。",

    'f"In 2014 Karen Simonyan and Andrew Zisserman at Oxford':
        "2014年，牛津的卡伦·西蒙尼扬和安德鲁·齐瑟曼想知道光靠深度能走多远，就只用3乘3的卷积，搭了十六层和十九层的网络。<bookmark mark='a'/>为什么这么小？按第3章的规则，两个3乘3的层看五乘五个像素。<bookmark mark='b'/>输入输出都是C个通道时，它们要十八个C平方个权重，而一个5乘5的层要二十五个C平方。<bookmark mark='c'/>三个这样的层看七乘七，二十七对四十九，中间还多了两个非线性。<bookmark mark='d'/>VGG-16在2014年得了第二。它很大：按我们从它的层列表数出来的，{S['params'] / 1000000.0:.0f}百万个权重，每张图{S['macs'] / 1000000000.0:.1f}十亿次乘加。",

    'The winner of 2014 went another way.':
        "2014年的冠军走了另一条路。<bookmark mark='a'/>克里斯蒂安·塞格迪在谷歌的团队用Inception模块搭出了GoogLeNet：同时透过几个大小不同的窗口去看上一层，再把结果并排堆起来。<bookmark mark='b'/>让它负担得起的办法是：在每个大卷积前面放一个1乘1的卷积，在昂贵的那一步之前先把通道数削减下来。<bookmark mark='c'/>二十二层，当年最好的错误率，而且按作者的统计，权重只有AlexNet的十二分之一。更深，不一定意味着更大。",

    'f"Then depth hit a wall.':
        "然后，深度撞上了一堵墙。<bookmark mark='a'/>微软的何恺明和同事发现，一个五十六层的普通网络比二十层的还差，连在自己的训练数据上都更差：不是过拟合，只是更难训练。那一年提出的批归一化有帮助，但不够。<bookmark mark='b'/>他们的办法是：让每两层只学一个修正量F(x)，加到它的输入上。<bookmark mark='c'/>这个块的导数是单位矩阵加上F的导数：一条有助于梯度到达前面各层的恒等路径，第9部分展示过。<bookmark mark='d'/>一百五十二层，以{ILSVRC[5][2]}%赢下了2015年。几个月前，高速公路网络已经用门搭出了同样的通路。",

    # ------------------------------------------------------------------ Filters
    'Chapter eight. What the filters learn.': '第8章。滤波器学到了什么。',

    'f"<bookmark mark=\'a\'/> CIFAR-10, collected by Krizhevsky':
        "<bookmark mark='a'/>CIFAR-10，克里热夫斯基在2009年收集：六万张32乘32像素的图片，分十个类别。<bookmark mark='b'/>我们给它的网络有一个像AlexNet那样的第一层：48个7乘7像素的彩色卷积核，步长为2，后面还有三个卷积层。<bookmark mark='c'/>在这台计算机上把五万张训练照片过了{cf['epochs']}遍以后，它能把一万张测试照片中的{pct(acc)}%标对。",

    'f"Now replay the training and watch the first layer.':
        "现在重放训练过程，看第一层。<bookmark mark='a'/>一开始是48块噪声，答对{pct(accs[0], 0)}%：瞎猜的水平。<bookmark mark='b'/>不到{steps[mid]:,}步，答对一半以上，噪声开始有了条理。<bookmark mark='c'/>{fin}",

    'By the end, some have become edge detectors, light against dark at one angle, and others':
        "到最后，有些变成了边缘检测器，在某一个角度上亮对暗；另一些成了一种颜色对另一种颜色的斑块。克里热夫斯基的论文给AlexNet的96个卷积核展示过同样种类的图样，视觉皮层里也能找到同样种类的滤波器。",

    'By the end, some have become edge detectors, light against dark at one angle. Krizhevsky':
        "到最后，有些变成了边缘检测器，在某一个角度上亮对暗。克里热夫斯基的论文给AlexNet展示过同一种卷积核，视觉皮层里也能找到同一种滤波器。",

    'By the end the patterns are smoother, but few are clean edges':
        "到最后，图样平滑了一些，但干净的边缘很少；克里热夫斯基论文里AlexNet的96个卷积核，用多得多的照片训练了长得多的时间，要干净得多。",

    'f"We can run Hubel and Wiesel\'s experiment on our own network.':
        "我们可以在自己的网络上做休伯尔和威泽尔的实验。<bookmark mark='a'/>给每个滤波器看一种条纹图案，也就是光栅，转到十六个角度，记下它在每个角度的反应有多强。<bookmark mark='b'/>这是其中三个滤波器，它们的反应画成绕着圆的形状：又细又长的形状，说明这个滤波器在乎某一个角度、不理会和它垂直的角度，就像猫的那个细胞。<bookmark mark='c'/>数一数，有多少滤波器在最佳角度的反应至少是垂直方向的三倍：{n}个里有{no}个，另外还有{nc}个主要对颜色有反应。{verdict}",

    'Before training, not one of them passes':
        "训练之前，它们没有一个通过同样的检验。这种方向偏好是学出来的。",

    "f'Before training, only {no0} pass the same test":
        "训练之前，只有{no0}个碰巧通过同样的检验；训练之后，有{no}个。",

    "f'Before training, {no0} pass the same test by chance":
        "训练之前，有{no0}个碰巧通过同样的检验；训练之后，{no}个。",

    'f"Higher layers combine the edges.':
        "更高的层把边缘组合起来。要看一个更深的单元想要什么，马修·泽勒和罗布·弗格斯2013年的办法是：找出最能激发它的输入。<bookmark mark='a'/>在我们的第三层，每个单元看21个像素见方，它最喜欢的那些小块有共同的纹理、颜色边界、曲线或角。<bookmark mark='b'/>第四层看整张照片，它最喜欢的图像开始属于同一个类别：对这四个通道，前六张图中分别有{purity[0]}、{purity[1]}、{purity[2]}和{purity[3]}张是同一类的。没有人给这些通道贴过标签。标签只到达过最后那一层。",

    # ------------------------------------------------------------------ Adversarial
    'Chapter nine. Adversarial examples.': '第9章。对抗样本。',

    'f"In December 2013 Christian Szegedy and six colleagues':
        "2013年12月，克里斯蒂安·塞格迪和六位同事报告了一件怪事。<bookmark mark='a'/>对于网络分类正确的任何一张照片，他们都能找到一个极小的改动，人眼看不出来，却让网络答成别的东西。<bookmark mark='b'/>一年后，伊恩·古德费洛、乔纳森·施伦斯和塞格迪展示了一只熊猫，GoogLeNet以{P['panda']}%的置信度认出它是熊猫。加上一层淡淡的图案，每个像素改动{P['eps']}，它就说这是长臂猿，置信度{P['gibbon']}%。<bookmark mark='c'/>他们也给出了解释。",

    'Their argument is about linearity.':
        "他们的论证是关于线性的。取一个线性打分，w点乘x，把输入改动一个小小的η。<bookmark mark='a'/>打分变化w点乘η。<bookmark mark='b'/>如果每个像素最多只能改动ε，最大的变化来自把每个像素都沿它权重的符号方向移动ε：等于ε乘以权重绝对值之和。<bookmark mark='c'/>有n个输入、权重平均大小为m时，就是ε乘以m乘以n：在任何一个像素上小到看不出的改动，在几千个像素上加起来，就成了打分的大变化。<bookmark mark='d'/>ReLU网络是用线性的片段拼起来的，所以用网络自己的梯度做同样的事：这就是快速梯度符号法，一个梯度，一步。",

    'f"Try it on our LeNet.':
        "在我们的LeNet上试试。<bookmark mark='a'/>这是一个测试数字上损失梯度的符号：每个像素往哪个方向移动，能让网络错得更厉害。<bookmark mark='b'/>乘以ε加上去。ε为零时，网络说是{steps[0]['pred']}，{pct(steps[0]['p'], 0)}%确定。<bookmark mark='c'/>{v}在人看来，它显然还是一个7，只是蒙了一层薄雾。",

    "f'At epsilon {flip['eps']:g}":
        "ε为{flip['eps']:g}时，它说是{flip['pred']}，置信度{pct(flip['p'], 0)}%。",

    'Even at the largest epsilon here it still says 7':
        "即使在这里最大的ε下，它仍然说是7，只是没那么确定了。",

    'f"Measure it over all ten thousand test digits.':
        "在全部一万个测试数字上量一量。<bookmark mark='a'/>ε为四分之一时，线性模型在其中{pct(e_lin, 0)}%上出错；古德费洛那个浅层softmax错了{FGSM_PAPER['softmax']}%。<bookmark mark='b'/>网络也安全不了多少：LeNet错{pct(e_cnn, 0)}%。<bookmark mark='c'/>而且一步梯度只是一种弱的攻击。改走二十小步，每步都投影回ε的盒子里，ε为0.2时LeNet错{pct(e_pgd, 0)}%。<bookmark mark='d'/>攻击还能迁移：针对全连接网络做的改动，有{pct(T['mlp_to_lenet'], 0)}%的时候骗过LeNet；针对一个LeNet做的，有{pct(T['lenet_to_lenet'], 0)}%的时候骗过另一个。",

    'f"On photographs it is worse':
        "在照片上更糟，因为一张照片有更多的数：32乘32个像素，每个三种颜色。<bookmark mark='a'/>我们的CIFAR网络，用二十小步攻击，每个像素的改动不超过255级灰度中的两级：<bookmark mark='b'/>原图，放大许多倍的改动，以及结果：看上去一模一样，网络却说是别的东西。<bookmark mark='c'/>改动两级灰度时，它在{pct(a['cifar_pgd'][i2], 0)}%的测试照片上出错，而不受攻击时是{pct(a['cifar_pgd'][0], 0)}%。",

    'The attacked error, red, falls along with the clean one.':
        "受攻击的错误率，红色那条，跟着干净的一起下降。",

    'The attacked error, red, stays high while the clean one falls.':
        "受攻击的错误率，红色那条，一直很高，干净的那条却降了下来。",

    'f"The defence Goodfellow proposed':
        "古德费洛提出的防御是：拿攻击来训练，给每一批数据都做出对抗版本。<bookmark mark='a'/>我们这样训练了三个LeNet，一半是干净的数字，一半是受攻击的。{fall}<bookmark mark='b'/>ε为{t['eps']:g}时，一步攻击现在只在{pct(adv_f, 0)}%的时候骗过它，而不是{pct(std_f, 0)}%。{verdict}<bookmark mark='c'/>干净数字上的错误率是{pct(adv_c, 2)}%，对比{pct(std_c, 2)}%：{cost}<bookmark mark='d'/>这个问题至今没有解决；同样的搜索放到词语上，就能攻破语言模型：第31部分。",

    "f'Against twenty steps it holds up too":
        "面对二十步攻击它也撑住了：错{pct(adv_p, 0)}%，而普通网络错{pct(std_p, 0)}%。",

    "f'But against twenty steps it gives way":
        "但面对二十步攻击它就让步了：错{pct(adv_p, 0)}%。它学会的是抵抗训练时那种一步攻击，而不是一般的攻击。",

    'robustness costs a little accuracy.':
        "鲁棒性要付出一点准确率。",

    'here robustness costs almost nothing.':
        "这里鲁棒性几乎不花代价。",

    # ------------------------------------------------------------------ Efficient
    'Chapter ten. Cheaper convolutions.': '第10章。更便宜的卷积。',

    'A convolution kernel looks at a small patch, but through every channel':
        "一个卷积核只看一小块，却要透过下一层的每一个通道去看：k乘k乘C个权重，对C撇个输出通道各一份。<bookmark mark='a'/>2014年，洛朗·西夫尔把它拆成了两步。先对每个通道单独滤波，每个通道一个小卷积核：深度卷积。<bookmark mark='b'/>再在每个像素上用1乘1的卷积把通道混起来：逐点卷积。<bookmark mark='c'/>数乘加次数。标准卷积：高乘宽乘C乘C撇乘k平方。<bookmark mark='d'/>可分离卷积：深度部分H W C k平方，加上逐点部分H W C C撇。<bookmark mark='e'/>两者之比是C撇分之一加上k平方分之一：对3乘3的卷积核和256个通道，大约是九分之一的算术量。",

    '"Fewer operations should mean faster.':
        "运算少了，应该就快了。我们在制作这个视频的计算机上把两种版本都测了一下。<bookmark mark='a'/>对128个通道：{verdict}<bookmark mark='b'/>数运算次数不等于数时间，高效的网络是为它们运行的硬件设计的。",

    'f"The arithmetic falls to {ft:.2f} of the standard layer\'s, but':
        "算术量降到标准层的{ft:.2f}，时间却只降到{tt:.2f}。深度卷积那一步每秒只做{r128['gflops_dw']:.1f}十亿次运算，而标准卷积是{r128['gflops_std']:.0f}：它的每个权重只碰一个通道，每读一个字节只做很少的算术，第17部分的屋顶线把它压住了。",

    'f"The arithmetic falls to {ft:.2f} of the standard layer\'s, yet':
        "算术量降到标准层的{ft:.2f}，时间却一点没降：是标准层的{tt:.2f}倍。深度卷积那一步每秒只做{r128['gflops_dw']:.1f}十亿次运算，而标准卷积是{r128['gflops_std']:.0f}：它的每个权重只碰一个通道，每读一个字节只做很少的算术，第17部分的屋顶线把它压住了。",

    'f"The arithmetic falls to {ft:.2f} of the standard layer\'s, and':
        "算术量降到标准层的{ft:.2f}，时间也降到{tt:.2f}：这里省下的几乎全兑现了。",

    'f"In 2017 Andrew Howard\'s team at Google':
        "2017年，谷歌安德鲁·霍华德的团队用可分离卷积搭了一整个网络，给手机用：MobileNet。<bookmark mark='a'/>它在ImageNet上的准确率只比VGG-16低{v[1] - m[1]:.1f}个百分点，乘加次数却少{v[2] / m[2]:.0f}倍，权重少{v[3] / m[3]:.0f}倍，而且用比GoogLeNet更少的乘加和权重超过了它。",

    'f"The other trick spreads a kernel out':
        "另一个技巧是把卷积核摊开，而不是削瘦它。<bookmark mark='a'/>空洞卷积在抽头之间留出空隙：第一层相隔一格，下一层两格，然后四格，然后八格。<bookmark mark='b'/>感受野每一层翻一倍：十层三抽头的卷积之后，是{r['dilated'][9]:,}个输入，而不是{r['plain'][9]}个，而且不多花代价。<bookmark mark='c'/>这个想法早就有了，就是1989年的“带孔算法”；2016年，DeepMind的WaveNet用它来生成语音。",

    'f"In 2020 a transformer fed an image cut into patches':
        "2020年，一个把图像切成小块喂进去的Transformer，追平了最好的卷积网络，视觉Transformer很快就领先了各项基准：那是第22部分。<bookmark mark='a'/>2022年，Meta的刘壮和同事想知道，这个领先有多少来自架构，多少来自训练配方。他们从一个76.1%的ResNet-50出发：光是换上Transformer的训练配方就到了78.8%；深度卷积、更宽的层、7乘7的卷积核，再加上Transformer的层归一化，把它推到{vals[-1]}%，<bookmark mark='b'/>超过了同等大小的Transformer，{SWIN_T}%，而且完全没有注意力：这就是ConvNeXt。<bookmark mark='c'/>2023年，DeepMind用在四十亿张图片上训练的卷积网络追平了视觉Transformer。在大规模下，配方和算力比架构更重要：这是第12部分的教训。",

    # ------------------------------------------------------------------ Recurrence
    'Chapter eleven. Recurrence and vanishing gradients.': '第11章。循环与梯度消失。',

    'Now the other half of this part: sequences.':
        "现在是本部分的另一半：序列。卷积在空间上共享权重。循环网络在时间上共享权重。<bookmark mark='a'/>它保持一个隐状态h，一个向量，每一步都用同样的两个权重矩阵W和U，把旧的状态和新的输入混在一起，再经过一个压扁的tanh。<bookmark mark='b'/>沿着时间展开，它就是一个很深的网络，每一步一层，所有层共享权重。<bookmark mark='c'/>迈克尔·乔丹在1986年、杰弗里·埃尔曼在1990年，让这个想法在认知科学里流行起来。",

    'To train it, unroll it and backpropagate':
        "要训练它，就把它展开再做反向传播，这是保罗·韦尔博斯在1990年描述的：随时间反向传播。<bookmark mark='a'/>如果损失只作用于末状态，对早期状态h k的梯度就要穿过之后的每一个状态。<bookmark mark='b'/>每往回一步，就乘上那一步的雅可比矩阵：tanh的斜率乘以同一个矩阵W，一遍又一遍。<bookmark mark='c'/>斜率最多是1，所以这个乘积最多是W的最大奇异值的步数次方。<bookmark mark='d'/>小于1，从远处传回的梯度就指数级地缩小；特征值大于1，它就可能爆炸。<bookmark mark='e'/>塞普·霍赫赖特在他1991年的毕业论文里分析了这个问题；约书亚·本吉奥、帕特里斯·西马尔和保罗·弗拉斯科尼在1994年发表了它。",

    'f"We measured it.':
        "我们量了一下。取一些随机的循环网络，用随机输入去跑，再从最后一步往回乘雅可比矩阵。<bookmark mark='a'/>当W的最大特征值是{rhos[0]:g}时，传回五十步的梯度缩小到原来的10的{-a:.0f}次方分之一：没了。<bookmark mark='b'/>{mid}<bookmark mark='c'/>{tail}<bookmark mark='d'/>不管哪种情况，普通循环网络能学到东西的时间窗口都很窄，而这个窗口由W的大小决定。",

    'f"Even at {rhos[2]:g}, where the linear network':
        "即使在{rhos[2]:g}，线性网络的梯度涨到10的{lb:.0f}次方，tanh网络的梯度却缩小到10的{-b:.0f}次方分之一：它的单元饱和，斜率下降，把乘积拉了下来。",

    'f"At {rhos[2]:g} it grows':
        "在{rhos[2]:g}时它变大：五十步后是10的{b:.0f}次方，线性网络的是10的{lb:.0f}次方。",

    "f'At {rhos[3]:g} the tanh network is chaotic":
        "在{rhos[3]:g}时，tanh网络进入混沌，它的梯度爆炸了：10的{top:.0f}次方。",

    "f'Even at {rhos[3]:g}, saturation keeps it from exploding":
        "即使在{rhos[3]:g}，饱和也让它没有爆炸：只涨到10的{top:.0f}次方。",

    "f'Even at {rhos[3]:g}, saturation holds it":
        "即使在{rhos[3]:g}，饱和也让它大致保持原来的大小。",

    "f'Even at {rhos[3]:g}, saturation pulls it down":
        "即使在{rhos[3]:g}，饱和也把它拉了下来，缩小到10的{-top:.0f}次方分之一。",

    'f"Exploding gradients have a shape.':
        "梯度爆炸是有形状的。<bookmark mark='a'/>取最小的循环网络，一个单元，一个权重w，一个偏置b，跑五十步，要求它最后的状态是0.7。这是每一组w和b对应的损失，越高越亮。在单元从停在高处变成停在低处的地方，损失陡然一跳：一道悬崖。<bookmark mark='b'/>从边缘附近出发的梯度下降撞上悬崖壁，那里的梯度是{nr.max():,.0f}，于是被甩出了地图。<bookmark mark='c'/>办法来自拉兹万·帕斯卡努、托马斯·米科洛夫和本吉奥，2013年：如果梯度比某个阈值长，就把它缩到那个长度。裁剪之后，同样的下降最后停在损失{g['loss_clip'][-1]:.4f}。今天的语言模型也用梯度裁剪。",

    # ------------------------------------------------------------------ LSTM
    'Chapter twelve. LSTM and GRU.': '第12章。LSTM与GRU。',

    'The cure came from Hochreiter himself':
        "解药来自霍赫赖特本人，和于尔根·施密德胡伯一起，在1997年。<bookmark mark='a'/>如果每一步都把梯度乘以小于1的东西，那就造一个每步恰好乘以1的单元：一个自己连到自己、权重为1、不压扁的记忆细胞。<bookmark mark='b'/>误差信号可以骑着它往回走任意多步而不衰减：恒定误差传送带。<bookmark mark='c'/>在它周围，学出来的门决定什么时候写进细胞、什么时候读出；后来，格斯、施密德胡伯和弗雷德·卡明斯加了一个遗忘门，用来清空它。",

    'Here is the cell as it is used today.':
        "这是今天用的样子。<bookmark mark='a'/>笔直穿过它的是细胞状态：一条记忆的传送带。<bookmark mark='b'/>遗忘门给每个格子一个零到一之间的数，乘在传送带上：一是保留，零是擦掉。<bookmark mark='c'/>输入门决定加进多少新的候选值g。<bookmark mark='d'/>输出门决定把多少记忆作为隐状态h显示出来。<bookmark mark='e'/>三个门都由上一个隐状态和输入算出来，所以网络学会什么时候记住、什么时候遗忘、什么时候开口。",

    'Why does the gradient survive?':
        "为什么梯度能活下来？<bookmark mark='a'/>对细胞状态关于上一个细胞状态求导。沿着传送带，它就是遗忘门，一个由零到一之间的数组成的对角矩阵；其他路径要穿过门，它们不一定很小。<bookmark mark='b'/>沿细胞状态的直接路径往回跨过许多步，这一份梯度贡献乘的是网络学出来的遗忘门乘积。完整梯度还包括其他路径的贡献。<bookmark mark='c'/>遗忘门保持在f时，每过ln 2除以负ln f步，这条直接路径上的记忆贡献就减半。<bookmark mark='d'/>f等于0.99时，大约六十九步；恰好等于1，就是霍赫赖特最初的传送带，永远不忘。",

    'In 2014 Kyunghyun Cho and colleagues in Montreal simplified the cell.':
        "2014年，蒙特利尔的赵京焕和同事把这个细胞简化了。<bookmark mark='a'/>门控循环单元只保留隐状态和两个门：更新门z把旧状态和新的候选值混合，z接近零的地方还是那条传送带；另外是一个重置门。<bookmark mark='b'/>零件更少，效果差不多一样好，这是Junyoung Chung和同事比较的结果。",

    'f"Does the carousel work?':
        "传送带管用吗？做一个霍赫赖特那种风格的测试：<bookmark mark='a'/>一个序列以一个做了标记的符号开头，八个里的一个；<bookmark mark='b'/>然后是随机的干扰符号；<bookmark mark='c'/>最后网络必须说出第一个符号是什么。<bookmark mark='d'/>我们训练了一个普通循环网络、一个LSTM和一个GRU，各六十四个单元，各训练三次，序列长度分别是{m['T'][0]}、{m['T'][1]}和{m['T'][-1]}步。带门的细胞一开始就把门设成“记住”：这是科朗坦·塔莱克和扬·奥利维耶提出的“时序初始化”。",

    'f"The results. {first}':
        "结果如下。{first}<bookmark mark='a'/>{v}<bookmark mark='b'/>{jump}",

    "f'Over {Ts[0]} steps, all three learn the task":
        "在{Ts[0]}步的序列上，三个都学会了：普通网络答对{pct(r10, 0)}%。",

    "f'Even over {Ts[0]} steps the task is not easy":
        "即使只有{Ts[0]}步，这个任务也不容易：普通网络答对{pct(r10, 0)}%，LSTM是{pct(l10, 0)}%，GRU是{pct(g10, 0)}%。",

    "f'At {Tbig} steps the plain network never gets off chance":
        "在{Tbig}步时，普通网络始终没有离开瞎猜的水平，{pct(r100, 0)}%，而LSTM和GRU达到{pct(l100, 0)}%和{pct(g100, 0)}%。",

    "f'At {Tbig} steps the plain network reaches only":
        "在{Tbig}步时，普通网络只达到{pct(r100, 0)}%；LSTM是{pct(l100, 0)}%，GRU是{pct(g100, 0)}%。",

    "f'At {Tbig} steps all three do about as well":
        "在{Tbig}步时，三个差不多：{pct(r100, 0)}%、{pct(l100, 0)}%和{pct(g100, 0)}%。",

    "f'The gated cells sit at chance for":
        "带门的细胞在瞎猜的水平上停了一阵，大约{wait_steps:,}步，然后找到窍门，往上爬：门学会了为标记的符号打开、为之后的一切关上。",

    'The gated cells climb from the start':
        "带门的细胞从一开始就在往上爬：门很快就学会了为标记的符号打开、为之后的一切关上。",

    '"Here is why.':
        "原因在这里。训练过程中，测量从结尾的答案出发，到达序列每一步的梯度有多少。<bookmark mark='a'/>{v}",

    'f"For the plain network, the gradient at the first step, the only one that matters, is about ten to the {gap_r:.0f} times weaker than at the last. <bookmark mark=\'b\'/> For the LSTM the difference':
        "对普通网络，第一步的梯度，也就是唯一要紧的那一步，比最后一步弱了大约10的{gap_r:.0f}次方倍。<bookmark mark='b'/>对LSTM，差别是10的{gap_l:.0f}次方：传送带把信号带了回去。",

    'f"For the plain network, the gradient at the first step, the only one that matters, is about ten to the {gap_r:.0f} times weaker than at the last. <bookmark mark=\'b\'/> For the LSTM the first':
        "对普通网络，第一步的梯度，也就是唯一要紧的那一步，比最后一步弱了大约10的{gap_r:.0f}次方倍。<bookmark mark='b'/>对LSTM，第一步得到的梯度和最后一步差不多：传送带把信号带了回去。",

    'f"For the plain network the gradient at the first step is ten':
        "对普通网络，第一步的梯度比最后一步弱10的{gap_r:.0f}次方倍；<bookmark mark='b'/>对LSTM，是10的{gap_l:.0f}次方。",

    # ------------------------------------------------------------------ CharLSTM
    'Chapter thirteen. A character LSTM.': '第13章。字符级LSTM。',

    'f"Now the LSTM plays the series\' game':
        "现在让LSTM来玩本系列的游戏：猜下一个字符。<bookmark mark='a'/>每个字符变成一个学出来的向量；一层{m['hidden']}个LSTM细胞按顺序读它们；一个softmax猜下一个。总共{m['params']:,}个权重。<bookmark mark='b'/>我们照安德烈·卡帕西2015年的char-rnn那样训练它：把三十部小说切成{n_read}个长段，每段一个读者，每步{m['bptt']}个字符，记忆一步一步地带下去，而梯度在每一步的边上截断。<bookmark mark='c'/>它读了{m['chars_seen'] / 1000000.0:.1f}百万个字符，大约是这些书的{100 * m['chars_seen'] / m['train_chars']:.0f}%，只读一遍，在这台计算机上用了{mins:.0f}分钟。",

    'f"Here is its training, scored as always':
        "这是它的训练过程，照例在记分牌那段《马耳他之鹰》上打分，它从来没见过这段文字。<bookmark mark='a'/>它从每字符{e0:.1f}比特开始，在{m['K']}个符号里瞎猜，写出来的是噪声。<bookmark mark='b'/>{mid_s}<bookmark mark='c'/>{end}",

    "f'Within {snaps[i_mid][0]:,} steps it writes words and spaces":
        "不到{snaps[i_mid][0]:,}步，它就能写出单词和空格，每字符{mid_bits:.2f}比特。",

    'f"After {snaps[i_mid][0]:,} steps it is at {mid_bits:.2f} bits per character':
        "{snaps[i_mid][0]:,}步之后，它到了每字符{mid_bits:.2f}比特，不过写出来的还不像单词。",

    'f"By the end, {pb:.2f} bits per character on the passage: below Part 9\'s neural model, and':
        "到最后，在测试段落上是每字符{pb:.2f}比特：低于第9部分的神经模型，也低于克内瑟-奈伊的{kn:.2f}。",

    'f"By the end, {pb:.2f} bits per character on the passage: below Part 9\'s neural model, but':
        "到最后，在测试段落上是每字符{pb:.2f}比特：低于第9部分的神经模型，但还没低于克内瑟-奈伊的{kn:.2f}。",

    'f"By the end, {pb:.2f} bits per character on the passage, against':
        "到最后，在测试段落上是每字符{pb:.2f}比特，对比第9部分的{n9:.2f}和克内瑟-奈伊的{kn:.2f}。",

    '"On the scoreboard, a new row.':
        "记分牌上，新的一行。<bookmark mark='a'/>我们的字符级LSTM：{v}<bookmark mark='b'/>{tail}",

    'f" The pretrained language models below it are still far ahead':
        "下面那些预训练的语言模型仍然遥遥领先，最好的低到{lm_best:.2f}比特：更多的文本，更多的算力，和不同的架构，那是下一幕的故事。",

    'f" The pretrained language models below it are still ahead':
        "下面那些预训练的语言模型仍然领先，最好的到{lm_best:.2f}比特，用的文本和算力多得多，架构也不同：那是下一幕的故事。",

    ' The large models of Part 1, still to be filled in':
        "第1部分的大模型，在这块记分牌上还没填进来，它们显示出还有多远的路要走。",

    "f'{me:.2f} bits per character, better than every row above it":
        "每字符{me:.2f}比特，比它上面的每一行都好，好了{best_above - me:.2f}比特。记忆是值得的。",

    'f"{me:.2f} bits per character, {me - best_above:.2f} behind':
        "每字符{me:.2f}比特，比上面最好的一行差{me - best_above:.2f}：以我们在这里负担得起的训练量，LSTM还没追上。",

    '"What has it learned to remember?':
        "它学会了记住什么？像卡帕西、贾斯廷·约翰逊和李飞飞在2015年做的那样，看单个的细胞。<bookmark mark='a'/>{v}<bookmark mark='b'/>要合上引号，它就得记住有一个引号是开着的，也许要记好几行。2017年，OpenAI的亚历克·拉德福德和同事在亚马逊评论上训练了一个更大的，找到了一个单独的细胞，它跟踪着评论是不是正面的。",

    "f'One of its {m['hidden']} cells does something nobody asked for":
        "它的{m['hidden']}个细胞里，有一个做了没人要求它做的事：它在开引号处打开，在闭引号处关上。在整段文字上，它的值跟“在引号里”的相关系数是{abs(m['quote_corr']):.2f}。",

    'f"""The cell that best follows':
        "最能跟上“在引号里”的那个细胞也只是大致跟上：相关系数{abs(m['quote_corr']):.2f}。我们的小模型没有专门为它留一个细胞。",

    'f"And where is it surprised?':
        "它在哪里会吃惊？把段落开头的每个字符按它花掉的比特数上色。<bookmark mark='a'/>在整段文字上，一个单词的第一个字母平均花{ws:.1f}比特；单词里面的字母，{wi:.1f}比特；大写字母，{cap:.1f}比特。单词一旦开了头，剩下的几乎是白送的。这就是第1部分的猜字游戏，由一台会记忆的机器来玩。",

    # ------------------------------------------------------------------ Seq2Seq
    'Chapter fourteen. Sequence to sequence.': '第14章。序列到序列。',

    'f"By 2014 machine translation was statistical.':
        "到2014年，机器翻译是统计的。<bookmark mark='a'/>最好的系统是基于短语的，来自第7部分：用巨大的短语对照表，外加十几个分别调好的部件。<bookmark mark='b'/>2014年9月，谷歌的伊利亚·苏茨克维、奥里奥尔·维尼亚尔斯和Quoc Le用两个LSTM取代了这一切：一个把英语句子读进自己的记忆，另一个从这份记忆出发写出法语。五个这样的模型合起来得了{S['ensemble']}的BLEU，超过了基于短语的基线{S['smt']}。<bookmark mark='c'/>有一个技巧很要紧：把源句子倒着读，这样译文最先需要的那几个词，就是最后读到的。<bookmark mark='d'/>蒙特利尔赵京焕的团队用GRU搭出了同样的设计。",

    'The design has two halves.':
        "这个设计分两半。<bookmark mark='a'/>编码器一次读一个符号，更新自己的状态。<bookmark mark='b'/>它最后的状态是一个单独的向量，要代表整个句子。<bookmark mark='c'/>解码器从这个向量出发，一次写一个符号，每一步是词表上的一个softmax，<bookmark mark='d'/>它写下的每个词都被送回去，作为下一步的输入，直到它写出句末符号。",

    'How is the decoder trained?':
        "解码器是怎样训练的？<bookmark mark='a'/>用教师强制，来自罗纳德·威廉斯和戴维·齐普泽1989年的想法：每一步都喂给它真实的上一个词，让它预测下一个。<bookmark mark='b'/>测试时没有真实的历史，只有它自己写的：错一步，后面每一步都要从一个训练中从未见过的历史接着往下写。",

    'f"Writing the most probable output exactly':
        "要精确地写出概率最大的输出，就得搜索所有可能的序列。贪心解码则在每一步只取最好的那一个词。<bookmark mark='a'/>束搜索在每一步保留几个最好的部分输出，各自往下延伸，再留下其中最好的：一种便宜的折中。<bookmark mark='b'/>在我们的字符级LSTM上，从同一个提示出发：贪心解码写出的文字在模型下要花{m['greedy_bits']:.0f}比特，宽度为8的束搜索找到的文字花{m['beam_bits']:.0f}比特，随机采样的花{m['sampled_bits']:.0f}比特。<bookmark mark='c'/>{tail}",

    'But look at the most probable text':
        "但看看概率最大的文字：它在原地兜圈子，阿里·霍尔茨曼和同事后来把这叫作神经文本退化；所以开放式的写作改用采样。",

    'For open-ended writing the most probable text is often dull':
        "对开放式的写作，概率最大的文字往往很乏味，所以语言模型改用采样；而翻译的目标是忠实传达原意，束搜索因此得到广泛使用。",

    'f"We built a small encoder-decoder':
        "我们搭了一个小的编码器-解码器，给它一个毫无歧义的任务：把一串字母倒过来写。<bookmark mark='a'/>它在{lo}到{hi}个字母的字符串上训练，从不同的起点训练了三次。<bookmark mark='b'/>{v}<bookmark mark='c'/>{bv}整个输入都得挤过编码器的最后一个状态：一个瓶颈，输入越长，情况越糟。",

    "f'A beam of four helps a little":
        "宽度为4的束搜索有一点帮助，最多提高{100 * max(gains):.0f}个百分点。",

    'A beam of four hardly helps':
        "宽度为4的束搜索几乎没有帮助：信息根本就不在那个向量里。",

    'f"Short strings come out right.':
        "短的字符串能写对。超过大约{half}个字母，就不到一半能写对；超出训练过的长度，几乎全错：一个向量装不下它们。",

    'It reverses most strings, though less reliably':
        "它能把大多数字符串倒过来，只是越长越不可靠。",

    'f"Two years later the idea was in production.':
        "两年后，这个想法上了生产线。<bookmark mark='a'/>谷歌2016年的神经机器翻译系统，两边各堆了八层LSTM，在人工并排评比里，它比谷歌自己的基于短语的系统平均少了{GNMT['error_cut']}%的翻译错误。<bookmark mark='b'/>2016年9月，它接管了谷歌翻译的中译英，每天大约一千八百万次翻译。<bookmark mark='c'/>但GNMT还有一个成分，正是它移走了那个瓶颈。",

    # ------------------------------------------------------------------ Attention
    'Chapter fifteen. The birth of attention.': '第15章。注意力的诞生。',

    'In September 2014 Dzmitry Bahdanau':
        "2014年9月，在本吉奥实验室访问的学生德米特里·巴赫达瑙，和赵京焕、本吉奥一起，提出扔掉那个单独的向量。<bookmark mark='a'/>把编码器所有的状态都留下，每个输入位置一个；在解码器的每一步，给每个状态打分：输入j和解码器接下来需要的东西有多契合？这个打分本身是一个很小的网络，和其他一切一起学。<bookmark mark='b'/>一个softmax把分数变成加起来等于1的权重。<bookmark mark='c'/>解码器得到它们的加权平均：一个为每次输出现做的上下文向量。<bookmark mark='d'/>他们把这些权重叫作对齐。我们叫它注意力。",

    'f"Here is one step of our own model':
        "这是我们自己的模型的一步，它在把单词{word}倒过来。它已经写了{out[:i]}，正要写下一个字母。<bookmark mark='a'/>它给输入的每个位置打分，softmax把{pct(a[top], 0)}%的权重放在一个字母上：第{top + 1}个位置的{word[top]}，正是它该抄的那个。<bookmark mark='b'/>上下文就是编码器状态的这种混合，几乎全是那一个。没有什么需要挤过一个单独的向量：解码器回头去取它需要的东西。",

    'f"Now the fair comparison':
        "现在做公平的比较：同样的编码器和解码器，同样的训练，有注意力和没有注意力，各训练三次。<bookmark mark='a'/>{v}<bookmark mark='b'/>{v2}",

    "f'With attention, {pct(ma[ih], 0)} percent":
        "有了注意力，{hi}个字母的字符串有{pct(ma[ih], 0)}%完全写对，而只用一个向量时是{pct(mp[ih], 0)}%。",

    'f"And beyond the lengths it trained on, it keeps going':
        "超出训练过的长度，它也照样能写：平均{pct(extra, 0)}%，因为它学会的规则，往回再看一格，和长度无关。",

    "f'Beyond the lengths it trained on, it too fails":
        "超出训练过的长度，它也失败了，平均{pct(extra, 0)}%：它从来没需要数到那么远。",

    'f"Watch the alignment form during training.':
        "看对齐在训练中怎样形成。<bookmark mark='a'/>每一行是它写的字母，每一列是它读的字母；亮的地方是它在看的地方。{early}<bookmark mark='b'/>{late}<bookmark mark='c'/>{climb}巴赫达瑙的翻译也呈现出同样的图景：大体沿着对角线，带着法语和英语的语序，在两者不一致的地方跳一下。",

    'At first it looks everywhere a little':
        "一开始，它到处都看一点，什么也学不到。",

    'Even at first its attention leans':
        "即使在一开始，它的注意力也偏向它需要的那些字母。",

    "f'Then a diagonal appears":
        "然后出现了一条对角线，从右上到左下：写下的第一个字母注视读到的最后一个，第二个注视倒数第二个。到第{t_diag:,}步，它一半以上的注意力落在这条对角线上；到最后，是{pct(mass, 0)}%。",

    "f'The diagonal stays faint":
        "这条对角线一直很淡：到最后，只有{pct(mass, 0)}%的注意力落在上面。",

    'As the alignment sharpens':
        "对齐越清晰，长字符串上的准确率也跟着上升。",

    "f'Yet the accuracy on long strings stays near":
        "然而长字符串上的准确率一直停在{pct(long1, 0)}%附近。",

    'f"On real translation the gain was large.':
        "在真实的翻译上，收益很大。<bookmark mark='a'/>巴赫达瑙的编码器-解码器，不用注意力时英译法的BLEU是{B['encdec']}；用了注意力，{B['search']}。<bookmark mark='b'/>训练得更久、只算没有生僻词的句子时，它达到{B['search_long_nounk']}，超过了基于短语的Moses系统的{B['moses_nounk']}。而单向量模型在长句子上崩溃的地方，注意力模型在五十个词以上还撑得住。",

    'Attention is a soft lookup':
        "注意力是一种软查找：一个查询，也就是解码器的状态，和一组键，也就是编码器的状态作比较，取回值的一个混合。<bookmark mark='a'/>同一年，神经图灵机和记忆网络用它来读取记忆。<bookmark mark='b'/>2015年，Thang Luong和同事用点积取代了巴赫达瑙那个打分的小网络；Kelvin Xu和同事把注意力指向图片的各个部分，来写图片说明。<bookmark mark='c'/>到2016年，它已经在谷歌翻译里面了。<bookmark mark='d'/>2017年，谷歌的一个团队想知道，如果把循环整个扔掉、只留注意力，会怎样。那就是Transformer，第13部分和第14部分。",

    # ------------------------------------------------------------------ Return
    'Chapter sixteen. Recurrence returns.': '第16章。循环的回归。',

    'After 2017 the Transformer took over':
        "2017年以后，Transformer占了上风，原因是训练速度。<bookmark mark='a'/>循环网络必须算完第t减1步才能算第t步：一个一千个词元的序列，就是一千步排成一排，一块有成千上万条通道的GPU大部分时间都在等。<bookmark mark='b'/>注意力一次算完所有位置。<bookmark mark='c'/>但到生成的时候，这笔交易反过来了。循环网络从一个词元到下一个，只带着一份固定大小的记忆；Transformer要保留之前每个词元的键和值，一个随文本增长的缓存。于是问题又回来了：循环网络能不能并行训练？",

    'It can, if the recurrence is linear.':
        "能，只要递推是线性的。<bookmark mark='a'/>假设新的状态是旧状态逐元素乘以a，再加上b，而a和b只取决于当前的输入。<bookmark mark='b'/>那么两步合起来，又是同样形式的一步：a乘a撇，以及a撇乘b加b撇。<bookmark mark='c'/>这个合并规则满足结合律：可以改变分组，但必须保持时间顺序。序列上任何满足结合律的运算，都能用并行前缀扫描算出来，这是盖伊·布莱洛克在1990年让它出名的算法。<bookmark mark='d'/>先合并相邻的，再合并相隔两格的，再合并相隔四格的：以2为底T的对数轮之后，每个位置都得到了自己的状态。一千步变成了十轮。",

    '"We tried it on the computer making this video.':
        "我们在制作这个视频的计算机上试了试。<bookmark mark='a'/>扫描和一步一步的循环给出相同的状态，差别只在舍入误差。<bookmark mark='b'/>{v8}<bookmark mark='c'/>{v256}扫描用额外的算术换来更少的串行步骤，这在有成千上万条通道的硬件上才划算：在GPU上，Leo Feng和同事测得，他们用扫描训练的循环网络，在长度512时比GRU快{MINRNN['gru512']}倍，在长度4096时快{MINRNN['gru4096']:,}倍。",

    "f'With a wide state, 256 numbers, it is":
        "状态宽时，256个数，它慢了{1 / w256:.1f}倍：扫描要做log T倍的工作，而这台计算机只有几个核心来分担。",

    "f'With a wide state, 256 numbers, the two are close":
        "状态宽时，256个数，两者接近：{w256:.1f}倍。",

    "f'With a narrow state, eight numbers":
        "状态窄时，8个数，在{big8['T']:,}步时扫描快了{w8:.1f}倍。",

    "f'With a narrow state the scan is about as fast":
        "状态窄时，扫描和循环差不多快，{w8:.1f}倍。",

    "f'With a narrow state the scan is {1 / w8:.1f}":
        "状态窄时，扫描比循环慢{1 / w8:.1f}倍。",

    "f'With a wide state the scan is {w256:.1f}":
        "状态宽时，扫描比循环快{w256:.1f}倍。",

    '"In 2024 Leo Feng, Yoshua Bengio and colleagues':
        "2024年，Leo Feng、约书亚·本吉奥和同事问：LSTM和GRU真的需要它们那非线性的递推吗？<bookmark mark='a'/>拿GRU来，让它的门和候选值只看当前的输入，不看上一个状态。剩下的恰好是一个线性递推，所以可以用扫描来训练。他们叫它minGRU，发现它在他们的任务上很有竞争力。<bookmark mark='b'/>我们也训练了一个，用扫描，放在其他几个旁边。{v}",

    "f'On our memory task, at {Ts[-1]} steps, minGRU gets {pct(mg, 0)} percent right, with":
        "在我们的记忆任务上，{Ts[-1]}步时，minGRU答对{pct(mg, 0)}%，LSTM是{pct(ls, 0)}%，普通网络是{pct(rn, 0)}%。只从输入学出来的门就够了：为标记的符号打开，为之后的一切关上。",

    "f'On our memory task, at {Ts[-1]} steps, minGRU gets {pct(mg, 0)} percent right, the":
        "在我们的记忆任务上，{Ts[-1]}步时，minGRU答对{pct(mg, 0)}%，LSTM是{pct(ls, 0)}%，普通网络是{pct(rn, 0)}%。",

    'minGRU joined a family growing since 2016.':
        "minGRU加入了一个从2016年起不断壮大的家族。<bookmark mark='a'/>准循环网络和简单循环单元把矩阵移出了递推；状态空间模型，从2021年的S4到2023年的Mamba，搭出让输入来决定保留什么的线性递推；2024年，霍赫赖特自己的团队带着xLSTM回来了，2025年扩展到七十亿参数。<bookmark mark='b'/>今天好几个开放模型把这样的层和注意力混在一起：Transformer的回忆能力，加上递推的固定大小记忆。那是第15部分。",

    # ------------------------------------------------------------------ Outro
    'f"Let\'s take stock.':
        "盘点一下。{hand}卷积在整张图上共享一个小小的卷积核，所以它和平移可交换。端到端训练的LeNet长出了自己的笔画检测器，{photo}<bookmark mark='a'/>{fool}因为它们接近线性。在时间上，普通循环网络的梯度随着雅可比矩阵相乘而衰减，或者爆炸。{lstm}而注意力让解码器回头看它恰好需要的东西。",

    'our photograph network grew edge detectors and colour cells':
        "我们的照片网络长出了边缘检测器和颜色细胞，就像视觉皮层里的那些。",

    'our photograph network grew edge detectors like':
        "我们的照片网络长出了边缘检测器，就像视觉皮层里的那些。",

    'our photograph network grew filters of its own.':
        "我们的照片网络长出了它自己的滤波器。",

    'Yet an invisible, well-chosen change fools them,':
        "然而一个看不见的、精心挑选的改动就能骗过它们，",

    'Yet a small, well-chosen change often fools them,':
        "然而一个很小的、精心挑选的改动常常就能骗过它们，",

    'Vision began with features designed by hand, and they beat raw pixels.':
        "视觉从手工设计的特征开始，它们胜过了原始像素。",

    'Vision began with features designed by hand.':
        "视觉从手工设计的特征开始。",

    'f"The LSTM\'s gated memory line carries it across':
        "LSTM带门的记忆传送带，把它带过了{T}步。",

    "The LSTM's gated memory line carries it further.":
        "LSTM带门的记忆传送带把它带得更远。",

    'All of this comes back.':
        "这一切都会再出现。巴赫达瑙的注意力变成了整个Transformer，在第13和第14部分。线性递推和它们的扫描，是第15部分的记忆。梯度裁剪和训练深层网络的优化器，是第11部分。切成小块的图像，以及新模型里面的卷积，是第22部分。对旋转、分子和图的等变性，是第25部分。而对抗攻击，这次是对语言模型的，会在第31部分再出现。",

    'Here are six problems, from equivariance to the scan.':
        "这里有六道题，从等变性到扫描。请在这里暂停，动手做一做；完整的解答在本部分的笔记里。",

    'Every network in this part was trained by some version of going downhill':
        "本部分的每个网络，都是用某种下山的方法训练出来的：带动量的普通梯度下降，或者Adam。下一次，在第11部分，我们把下山本身拆开来看：它收敛得多快、为什么；小批量的噪声起什么作用；推导动量和Adam；把权重当作矩阵来处理的新优化器；以及今天的模型用的学习率调度。",

    "Goodfellow, Bengio and Courville's book covers both halves":
        "古德费洛、本吉奥和库维尔的书涵盖了本部分的两半，塞利斯基的书讲的是之前的视觉。感谢观看，第11部分见。",
}

PHRASES = {}
