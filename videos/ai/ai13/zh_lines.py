"""Chinese narration for ai13: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).

Numbers from our own runs stay placeholders, so the Chinese follows the data when it changes; sentences chosen by a
result (``verdict``, ``tail``, ...) are translated as templates of their own and spliced in.
"""

TITLE = '人工智能，从零搭建 · 第13部分：注意力的几何'

CHAPTERS = {
    'Hook': '每个字符都在回头看',
    'Smoother': '1. 加权平均',
    'Hopfield': '2. 会回想的记忆',
    'Scale': '3. 为什么要除以根号d',
    'Heads': '4. 头是低秩映射',
    'Masks': '5. 谁能看谁',
    'Transformer': '6. 我们自己的Transformer',
    'Cost': '7. 一个模块的成本',
    'Positions': '8. 每个字符在哪里？',
    'Rope': '9. 用旋转表示位置',
    'SideBySide': '10. 四种答案，并排训练',
    'Longer': '11. 比训练时更长',
    'Sinks': '12. 注意力汇点，以及三条出路',
    'Caps': '13. 让分数待在范围之内',
    'Induction': '14. 归纳头',
    'InContext': '15. 在提示里学习',
    'RASP': '16. Transformer能算什么',
    'Frontier': '17. 2026年的注意力',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "This is a transformer reading.":
        "这是一个正在阅读的Transformer。它是我们自己的：我们用本系列的30部小说训练了它，现在它读的，是记分牌测试段落里的一句话，这段文字没有用于梯度训练。<bookmark mark='a'/>为了猜出下一个字符，每个字符都会回头看看它前面的那些字符，再决定每一个有多要紧。弧线越粗，它看得越多。<bookmark mark='b'/>这样回头一看，就叫作注意力；它是如今许多大型语言模型的核心机制。",

    'f"Our model has {L * H} of these looks':
        "我们的模型有{L * H}个这样的“目光”，叫作“头”，每个头都用自己的方式掂量过去：这里是全部{L * H}个头，读的是同一句话。<bookmark mark='a'/>这一部分讲的，就是这一看背后的数学：它算的是什么，它怎样知道东西在哪里，以及它能学会做些什么。",

    'The idea is older than it looks: in 1964':
        "这个想法比它看起来要古老：1964年，是邻居的加权平均；<bookmark mark='a'/>1982年，是霍普菲尔德那个会回想的记忆；<bookmark mark='b'/>2014年，是一个学会了该看哪里的翻译模型，<bookmark mark='c'/>而到了2017年，是一个只靠这种“看”的网络。<bookmark mark='d'/>接着有了更好的位置表示，<bookmark mark='e'/>会复制的头和快速的计算内核，<bookmark mark='f'/>注意力汇点和更长的上下文，<bookmark mark='g'/>更小的记忆，<bookmark mark='h'/>稀疏注意力和门控注意力，<bookmark mark='i'/>到了2026年，有些模型只在四分之一的层里保留完整的注意力。",

    "This is Part 13 of AI, Built":
        "这是《人工智能，从零搭建》的第13部分，也是第三幕的开始：Transformer时代。<bookmark mark='a'/>本部分讲：注意力算的是什么，它既是平均，也是记忆；头、掩码和计算成本；我们自己的Transformer，训练它，再回放它的训练过程；告诉它东西在哪里的四种方法，以及怎样把它们拉长；今天的注意力模块内部的种种修补；还有，头能学会做什么，又做不到什么。",

    # ------------------------------------------------------------------ Smoother
    "Chapter one. Attention is a weighted average.":
        "第1章。注意力就是加权平均。",

    "Here is Part 7's data again":
        "再看一次第7部分的数据：《远大前程》每一页里，“her”出现得有多频繁。假设你想给第120页，做一个平滑的估计。<bookmark mark='a'/>把每一页都拿来取加权平均，按它离得有多近来定权重：权重排成一个鼓包，中心就在你要问的那一页上。<bookmark mark='b'/>离查询点近的页，分量很重；远的，完全不算。这些权重都是正的，加起来等于1。<bookmark mark='c'/>让查询点一路滑过去，这个平均值就描出一条平滑的曲线。这就是纳达拉亚和沃森的核平滑器，1964年提出。",

    "The only knob is the width of the bump.":
        "唯一的旋钮，是鼓包的宽度。<bookmark mark='a'/>太窄，曲线就会去追每一页的噪声。<bookmark mark='b'/>太宽，它又会把整个故事压平成一个数。",

    "Write it down. The guess at the query":
        "把它写下来。查询点上的估计，是对所有页求和：每一页的值，乘以一个权重。权重是一个分数的softmax：分数取指数，再除以总和，所以权重都是正的，加起来等于1。这里的分数，是负的距离平方。<bookmark mark='a'/>现在，只改一处。不再用页码之间的距离，而是用两个向量的点积，给每一项打分：一个查询，一个键。<bookmark mark='b'/>这就是注意力，Transformer的核心。查询问的是：我在找什么？每个键说的是，它能提供什么；每个值，则是它要传下去的内容。<bookmark mark='c'/>而这三样，都由网络学出来的矩阵，从字符算出来。注意力，就是一个核可以学习的核平滑器。",

    'Here is the definition for the rest of this part.':
        "下面是本部分接下来一直要用的定义。<bookmark mark='a'/>注意力用点积给每个键和查询打分，再除以根号d，用softmax把分数变成权重，最后返回这些值的加权平均。<bookmark mark='b'/>2014年，德米特里·巴赫达瑙、赵京焕和约书亚·本吉奥让一个神经翻译网络回头去看它的源句子，就像第10部分那样；到了2017年，它成了整个网络。<bookmark mark='c'/>问一个问题：如果每个键都一样，注意力会返回什么？<bookmark mark='d'/>每个权重都是n分之1：结果就是这些值的普通平均。注意力只能对它拿到的东西加权、混合。",

    "Here's the geometry. Every key is an arrow":
        "来看看其中的几何。每个键都是一根箭头；查询也是。<bookmark mark='a'/>一个键的分数，就是它和查询的点积：两者各有多长，再乘以它们的方向有多一致。softmax把这些分数变成权重。<bookmark mark='b'/>转动查询，权重就从一个键流向另一个键。查询，就是一个要去看的方向。接下来，换个角度读同一个公式：把它看成一个能回想起所存内容的记忆。",

    # ------------------------------------------------------------------ Hopfield
    "Chapter two. A memory that recalls.":
        "第2章。会回想的记忆。",

    'f"In 1982 the physicist John Hopfield':
        "1982年，物理学家约翰·霍普菲尔德描述了一个会记忆的网络。<bookmark mark='a'/>要存入一些由正1和负1组成的模式，就把每一对同时亮起的单元之间的连接加强：这是第9部分的赫布规则。<bookmark mark='b'/>回想时，从一个线索出发，让每个单元取其他单元加权投票结果的符号，每次更新一个单元，并把自连接权重设为零。<bookmark mark='c'/>每翻转一次，能量都不会增加，所以回想就是一路滚下坡，如果一切顺利，就滚进最近的那个存储模式。<bookmark mark='d'/>这里我们存入{n}个字母，每个字母100个单元。<bookmark mark='e'/>给它一个四分之一像素被翻转的字母，让它自己稳定下来。{verdict}",

    "f'It recovers {ok} of the {n} letters":
        "{n}个字母里，它准确地恢复了{ok}个。其余的都落进了混合态：我们的字母共用的像素太多，它们的记忆互相串到了一起。",

    "f'It recovers all {n} letters":
        "全部{n}个字母，它都准确地恢复了，每个像素都回到了原位。",

    'f"How much can it hold?':
        "它能存多少？在100个单元里存入越来越多的随机模式，每个都用一个翻转了15%单元的线索来测试。<bookmark mark='a'/>经典网络存到{h_at}个模式时，能回想起来的就不到一半了，{none_txt}对随机模式，物理学家在1985年算出了渐近容量：每个单元大约0.138个模式。每存入一个模式，都会给其他每个模式的投票添一点噪声，噪声越积越多。<bookmark mark='b'/>2016年，德米特里·克罗托夫和约翰·霍普菲尔德把能量变得更陡，让最近的那个模式以大得多的优势胜出；2017年，又有一个团队证明，指数形式的能量能存下指数多个模式。<bookmark mark='c'/>{tail}",

    "f'and by {int(dead)} it recalls none":
        "到{int(dead)}个时，就一个也回想不起来了。",

    "f'Store {int(Ms[-1])} patterns":
        '存入{int(Ms[-1])}个模式，是单元数的{Ms[-1] / N:.1f}倍，一步softmax之后再取符号读出，仍然能从每个测试线索恢复存储的模式。',

    "f'It holds on far longer":
        '它撑得久得多：存到{int(Ms[-1])}个模式时，加上符号读出后，它仍然能回想起{md[-1]:.0%}。',

    'f"In 2020 Hubert Ramsauer':
        "2020年，胡贝特·拉姆绍尔、塞普·霍赫赖特和同事们把状态变成了连续的。<bookmark mark='a'/>能量变成：与各个存储模式重叠度的log-sum-exp取负，再加上一个让状态保持有界的小项。<bookmark mark='b'/>一步一步地把它最小化，更新规则就是：按每个存储模式与当前状态重叠度的softmax给它加权，再把它们加起来。<bookmark mark='c'/>看看这个公式。它就是注意力。线索是查询，存储的模式既是键也是值，而β扮演的就是根号d分之1的角色。<bookmark mark='d'/>在我们的字母上，一次更新之后再取符号读出，就恢复了{n}个里的{ok_m}个。<bookmark mark='e'/>他们还证明了，在模式充分分离、线索足够接近目标的条件下，一步检索的误差可以被限制得很小。论文的标题是：《Hopfield Networks is All You Need》，霍普菲尔德网络就是你所需要的一切。",

    'f"Beta, the inverse temperature':
        "β，也就是逆温度，是把这个记忆变成第1章那个平滑器的旋钮。<bookmark mark='a'/>把它调低，权重就摊到每一个模式上：结果是所有东西的平均，和被提示的那个模式的重叠度只有{small:.2f}。<bookmark mark='b'/>调到中间，它会把几个相似的模式平均起来，拉姆绍尔的团队把这种混合叫作亚稳态。<bookmark mark='c'/>把它调高，一个模式就拿走全部权重：重叠度是{big:.2f}。注意力就生活在这条曲线上，而除以根号d决定了它落在哪里。<bookmark mark='d'/>2024年的诺贝尔物理学奖，颁给了霍普菲尔德和杰弗里·辛顿，表彰的正是这类网络；第20部分会回到它们的能量，把它当作一种生成的方法。一个Transformer的头，就是一次记忆读取：它的查询在键里回想，返回值的一个混合。",

    # ------------------------------------------------------------------ Scale
    "Chapter three. Why divide by the square root of d.":
        "第3章。为什么要除以根号d。",

    'f"Take a query and a key whose d numbers':
        "取一个查询和一个键，它们各自的d个数相互独立，均值为0，方差为1，大致就是一个刚初始化的网络给出的样子。<bookmark mark='a'/>量一量它们的点积散得有多开：d等于{ds[0]}时是{sd[0]:.1f}，d等于{ds[-1]}时是{sd[-1]:.0f}。它随着向量的大小而增长。为什么？<bookmark mark='b'/>点积是d个乘积的和。<bookmark mark='c'/>每个乘积的均值都是0，因为它的两个因子相互独立。<bookmark mark='d'/>方差是1：独立的数相乘，乘积平方的期望，等于它们各自平方的期望相乘。<bookmark mark='e'/>独立的项，方差相加，所以点积的方差是d：它的散布像根号d那样增长。<bookmark mark='f'/>除以根号d，方差就回到1，不管向量多大：实测在{sds.min():.2f}到{sds.max():.2f}之间。",

    'f"Why does the spread matter?':
        "散布为什么要紧？因为softmax会把分数之间的差，变成权重之间的比，而且是指数式的。<bookmark mark='a'/>喂给它像根号d那样散开的分数，它就不再广泛取平均了：大部分权重集中到少数几个键上。在{n}个键上，权重的熵，也就是衡量有多少个键在分享权重的量，从d等于{ds[0]}时的{raw[0]:.1f}比特，降到了d等于{ds[-1]}时的{raw[-1]:.2f}比特。<bookmark mark='b'/>除以根号d之后，权重始终是摊开的，在这些维度上大约有{scl.min():.1f}到{scl.max():.1f}比特，只比完全平均分配的{mx:.0f}比特少一点。",

    'f"There is a second cost, and it is worse.':
        "还有第二个代价，而且更糟。训练靠梯度来移动分数，而梯度要穿过softmax的导数。<bookmark mark='a'/>权重i对分数j的导数，等于p i乘以括号里的δ i j减p j。<bookmark mark='b'/>当一个权重接近1、其余都接近0时，每一项都有一个接近0的因子：softmax接近饱和，这条梯度通路也就变弱了。<bookmark mark='c'/>权重对分数的响应有多强，在分数散布大约为{sig[pk]:.0f}时达到峰值，往两边都会下降。<bookmark mark='d'/>缩放过的分数，散布为1，响应是{j1:.2f}。不缩放时，在d等于{ds[-1]}处，响应只有{jr:.2f}，而且向量越大，它还会继续下降。这就是瓦斯瓦尼和同事们在2017年给出的理由。后来，杨格的μP主张在极宽的网络里改成除以d；失控的分数会在第13章再次出现。",

    # ------------------------------------------------------------------ Heads
    "Chapter four. Heads are low-rank maps.":
        "第4章。头是低秩映射。",

    'f"Let\'s write one head as matrices.':
        "把一个头写成矩阵。这里的x是归一化后的输入，还没有做位置旋转和分数缩放。字符i的查询，是W Q乘以x i；字符j的键，是W K乘以x j。<bookmark mark='a'/>把转置移进去，<bookmark mark='b'/>分数就是x i，乘以一个矩阵，再乘以x j：一个{d}乘{d}的矩阵W Q K，用来比较残差流里的两个位置。<bookmark mark='c'/>但它是一个又高又瘦的{d}乘{dh}矩阵，和一个又矮又宽的矩阵的乘积，所以它的秩至多是{dh}。一个头只能沿着残差流的{dh}个方向做比较。<bookmark mark='d'/>头搬运的东西也一样：W O乘以W V，秩同样至多是{dh}。纳尔逊·埃尔哈格、克里斯·奥拉和同事们把它们叫作QK回路和OV回路：一个决定看哪里，另一个决定搬什么。",

    'f"Here are the singular values of W Q K':
        "这是我们Transformer全部{L * H}个头的W Q K奇异值，从大到小，画在对数坐标上。这些线性矩阵只并入了层归一化的增益和去均值，没有并入偏移或随输入变化的缩放。<bookmark mark='a'/>每个头最多有{rank}个方向超过数值截断阈值；之后的值断崖式下跌，跌到计算机舍入误差的大小。<bookmark mark='b'/>即便在这{dh}个方向里，一个头也很偏：{int(k90.min())}到{int(k90.max())}个方向，就占了它全部奇异值平方和的九成。<bookmark mark='c'/>把一层的{H}个旋转前QK矩阵相加，各层这个和的最小秩是{lrank}。<bookmark mark='d'/>{ln_txt}求和后的比较矩阵覆盖许多方向，每个单独的矩阵仍是低秩的。",

    "f'That is every direction but one":
        '对于这些线性矩阵，这就是除一个方向之外的所有方向：让{d}个坐标一起等量变化的方向，去均值会把它从这些因子里去掉。',

    'f"So why split attention into {H} narrow heads':
        "那为什么要把注意力拆成{H}个窄头，而不是用一个{d}维的头？成本是一样的：{H}个{dh}维的头，权重数和一个{d}维的头完全相同。<bookmark mark='a'/>但每个头都有自己的softmax，所以有自己的注意力模式。一个头对每个字符只能做一次加权平均；我们第一层的{H}个头，一下子就做了{H}种不同的平均：{looks}<bookmark mark='b'/>这一层的输出，是对所有头求和：注意力模式乘以低秩的搬运。<bookmark mark='c'/>这是有代价的：窄头没法表达所有的模式。斯里纳德·博贾纳帕利和同事们在2020年把它叫作低秩瓶颈。真实的模型忍受了它，把省下来的花在别处：第15部分会讲，它们怎样共享或压缩键和值，把对过去词元的记忆变小。",

    "f'head {hp + 1} puts {prev[hp]:.0%} of its weight on the character just before, while head":
        "头{hp + 1}把{prev[hp]:.0%}的权重放在紧挨着的前一个字符上，而头{hw + 1}平均往回看{dist[hw]:.0f}个字符。",

    "f'head {hp + 1} puts {prev[hp]:.0%} of its weight on the character just before, while the others":
        "头{hp + 1}把{prev[hp]:.0%}的权重放在紧挨着的前一个字符上，而其他头平均往回看{min(dist):.0f}到{max(dist):.0f}个字符。",

    # ------------------------------------------------------------------ Masks
    "Chapter five. Who may look at whom.":
        "第5章。谁能看谁。",

    'f"A language model guesses each character':
        "语言模型根据前面的字符猜每一个字符，所以注意力决不能看到未来。<bookmark mark='a'/>这是一张分数表：每个查询一行，每个键一列。<bookmark mark='b'/>给对角线以上的每个分数加上负无穷。负无穷的指数是0，所以softmax完全不给未来任何权重。这就是因果掩码。<bookmark mark='c'/>它带来的好处，是训练的速度。在{n}个字符上走一遍，就同时做出{n}个猜测，每一个都只用到它自己的过去，所以每个位置都是一个训练样本。<bookmark mark='d'/>在我们的Transformer上检验一下：改动一段文字的后半部分。我们测量的是原始logit的绝对变化最大值，也就是输出softmax之前的分数。前半部分的变化是{past_txt}，后半部分的变化最多达到{mf:.1f}。同时去掉掩码和位置旋转，前半部分的变化是{nm:.1f}。这个联合消融让未来的信息进入了模型。",

    "The mask is the only difference":
        "不同的掩码揭示了这些Transformer家族的主要信息流。<bookmark mark='a'/>编码器让每个位置都能看到其他所有位置：它会读，但不能从左到右地写。<bookmark mark='b'/>解码器用的是因果三角：它写，一次一个词元。<bookmark mark='c'/>2017年那篇论文的翻译模型两样都有。它的解码器看自己的过去，还通过交叉注意力看整个源句：查询来自译文，键和值来自编码器对原文的阅读。<bookmark mark='d'/>前缀语言模型双向读它的提示，再从左到右写出其余部分。这几种谁胜出了、为什么，是第14部分的故事。",

    '"One more property, and a problem.':
        "还有一个性质，也是一个问题。注意力是在一个集合上取平均。<bookmark mark='a'/>每个词的权重都来自它的键，不管它坐在哪里。<bookmark mark='b'/>所以“dog bites man”，狗咬人，和“man bites dog”，人咬狗，给出的平均完全一样。<bookmark mark='c'/>用符号说：把输入打乱，输出也以同样的方式被打乱。没有掩码、也没有位置信息时，我们自己的Transformer{blind}<bookmark mark='d'/>必须告诉模型每个字符在哪里。这是第8章的内容。因果掩码已经泄露了一点位置信息，我们会看到是怎么泄露的。",

    "f'nearly blind to order":
        "几乎对顺序视而不见：它的输出只变化了{dev:.3f}。",

    # ------------------------------------------------------------------ Transformer
    "Chapter six. Our own transformer.":
        "第6章。我们自己的Transformer。",

    'f"Now build one.':
        "现在来搭一个。每个字符进来时都是一个向量，这是第3部分的想法，这里用{t['d']}个数。这一列向量就是第9部分的残差流：每一层都从它读取，再把结果加回去。<bookmark mark='a'/>一个Transformer模块分成两半。注意力在不同位置之间搬运信息：每个字符从它前面的字符那里收集信息。<bookmark mark='b'/>然后是一个MLP，也就是多层感知机：第9部分那种由加权求和和弯折组成的小网络，对每个位置单独使用，就像在琢磨刚收集来的东西。<bookmark mark='c'/>每一半都先用第9部分的层归一化处理它的输入：<bookmark mark='n'/>把向量里的数平移到平均为0，再缩放到一个标准的大小。然后这一半把它的输出加回残差流。叠上4个模块，最后读出对下一个字符的猜测，这就是整台机器：掩码来自第5章，头来自第4章。",

    'f"Ours has {t[\'layers\']} blocks':
        "我们的模型有{t['layers']}个模块，每个模块有{t['heads']}个头，共{t['n_params'] / 1000000.0:.1f}百万个数，一次读{t['ctx']}个字符。我们用那30部小说训练它，共采样约{t['tokens'] / 1000000.0:.0f}百万个字符目标位置，用的是一台普通的处理器，没有显卡。<bookmark mark='a'/>{verdict}",

    "f'It reaches {pb:.2f} bits a character on the passage, better than every model before it":
        "它在测试段落上达到每字符{pb:.2f}比特，比记分牌上它之前的每一个模型都好，不管是计数模型还是神经网络。",

    'f"It reaches {pb:.2f} bits a character on the passage, better than every counting model':
        "它在测试段落上达到每字符{pb:.2f}比特，比每一个计数模型都好，但还比不上第9部分那个混合了Kneser-Ney的神经网络模型，{mix:.2f}。",

    'f"It reaches {pb:.2f} bits a character on the passage, better than Part 9\'s neural model':
        "它在测试段落上达到每字符{pb:.2f}比特，比第9部分的神经网络模型好，那个是{nlm:.2f}，但还比不上Kneser-Ney的{kn:.2f}。",

    'f"It reaches {pb:.2f} bits a character on the passage, not yet better':
        "它在测试段落上达到每字符{pb:.2f}比特，还没有超过第9部分的神经网络模型，{nlm:.2f}。",

    'f"Here is what it knows at each moment of its training':
        "这是它在训练过程中每一刻所知道的：它在测试段落上的分数，它接着同一句开头写出的东西，以及全部16个头在看哪里。<bookmark mark='a'/>一开始，它的猜测是随机的，每字符{bits[0]:.1f}比特，比在它的{K_}个字符上均匀乱猜的{u:.1f}还差一点。它写出来的是噪声，它的注意力是一片模糊。<bookmark mark='b'/>到第{steps[k1]}步，{bits[k1]:.2f}比特；它写出的词里有{real[k1]:.0%}是真正的单词，各个头也开始各不相同。<bookmark mark='c'/>到第{steps[k2]:,}步，{bits[k2]:.2f}比特，{real[k2]:.0%}是真单词。<bookmark mark='d'/>到最后，{steps[-1]:,}步之后，{bits[-1]:.2f}比特，{real[-1]:.0%}是真单词。全部进步的一半，来自最初的{s_half:,}步；剩下的是慢慢打磨。",

    'f"On the scoreboard, a new row':
        "记分牌上添了新的一行：我们的Transformer，{float(t['passage_bits']):.2f}。这里把这些报告分开，因为它们评分的目标位置不同。<bookmark mark='a'/>{more}",

    'f"GPT-2 small, at {gpt[\'bits\']:.2f}':
        "GPT-2 small原先报告的分数是{gpt['bits']:.2f}，它也是一叠注意力模块，大约大{round(124000000.0 / t['n_params'], -1):.0f}倍。它的报告覆盖完整的词元化段落。训练数据、位置设计和计算预算也不同；这些是历史背景，并没有单独控制规模这个因素。",

    "The large models of Part 1 are the same kind of machine":
        "第1部分的那些大模型也是同一类机器，只是大得多，用多得多的文本训练：把它们分开的主要是规模，这是第12部分的故事。",

    # ------------------------------------------------------------------ Cost
    "Chapter seven. What a block costs.":
        "第7章。一个模块的成本。",

    'f"First, the numbers a block stores.':
        "先看一个模块要存多少个数。<bookmark mark='a'/>注意力有4个d乘d的矩阵：查询、键、值，还有输出。<bookmark mark='b'/>MLP先升到4d维，再降回来：8倍的d平方。<bookmark mark='c'/>所以一个模块是12倍的d平方，再加上少量偏置和层归一化的增益。<bookmark mark='d'/>再加上把字符变成向量的那张表，以及把向量变回猜测的那张表。<bookmark mark='e'/>对我们的模型，d等于{d}，{L}个模块，{K}个字符，公式给出{fml:,}，把模型的参数一个一个数出来，得到{tot:,}。<bookmark mark='f'/>只看注意力和MLP的参数，注意力占{att_share:.0%}；其余的在MLP里。",

    'f"Now the arithmetic for each character.':
        "再看每个字符要做多少运算。这里采用矩阵FLOP计数口径，不计归一化、激活函数和softmax的逐元素运算。<bookmark mark='a'/>每个矩阵权重对每个字符用一次，做一次乘法和一次加法：每个权重两次运算。<bookmark mark='b'/>注意力还额外增加了不归任何权重管的工作：查询要和T个键比较，每个键d个数；再对T个值做加权求和。<bookmark mark='c'/>合在一起，就是每个字符的运算量。<bookmark mark='d'/>我们用PyTorch的计数器，数了一次真实前向传播中已注册的矩阵运算，上下文从{Ts[0]}到{Ts[-1]:,}个字符。{match}贾里德·卡普兰和同事们的版本只算了平方项的一半，因为因果掩码把另一半扔掉了；跳过被掩掉那一半的计算内核，确实能把它省下来。<bookmark mark='e'/>训练更贵：一次前向加一次反向，是单独前向的{ratio:.1f}倍，每个权重、每个字符6次运算这条规则，就是这么来的。",

    "They match the formula to within a fraction of a percent.":
        "它们和公式的差别不到百分之一。",

    'f"Which term wins?':
        "哪一项占上风？<bookmark mark='a'/>对每个字符来说，注意力那部分随上下文增长，权重那部分不变。只计算因果半边并忽略词表投影时，2LTd等于24Ld平方，也就是上下文长度约为宽度的12倍时，两者相等。<bookmark mark='b'/>对我们的模型，这大约是{Tx:,}个字符，比它读的任何东西都长，所以它的成本主要在权重上。对GPT-3，是{gx:,}个词元。<bookmark mark='c'/>但注意力这一项有根刺：在一整段T个字符的文本上加起来，它像T的平方那样增长，而且要写下一个字符，过去的每个键和值都得留着。这就是长上下文昂贵的原因，也是第15、16和19部分存在的原因。",
    # ------------------------------------------------------------------ Positions
    "Chapter eight. Where is each character?":
        "第8章。每个字符在哪里？",

    'f"Chapter five ended with a problem':
        "第5章留下了一个问题：注意力分不清“dog bites man”和“man bites dog”。2017年那篇论文的答案，是在第一层之前，给每个字符的向量加上一个位置信号。<bookmark mark='a'/>一对一对的数以不同的速度振荡，每对是一个正弦和一个余弦，从每6个位置转一圈，一直到几万个位置才转一圈。<bookmark mark='b'/>为什么用正弦？因为三角函数的和角公式：往后移k个位置，对每一对来说都是同一个旋转，不管从哪里开始，所以一层网络可以用一个固定的矩阵，学会往回看固定的距离。<bookmark mark='c'/>数值上检验过，它在舍入误差以内成立。而且两个位置的点积，只取决于它们相隔多远。<bookmark mark='d'/>GPT-2走了另一条路，干脆为每个位置学一个向量，一共1024个。这样也行，但超过这张1024项表的位置，根本没有对应的表项。",

    "A different idea: forget absolute positions":
        "另一个想法：忘掉绝对位置，只告诉注意力两个字符相隔多远。2018年，彼得·肖和同事们为每个距离学一个向量，T5则为每一段距离范围学一个偏置。<bookmark mark='a'/>2021年，奥菲尔·普雷斯、诺亚·史密斯和迈克·刘易斯把它做到了最简单。ALiBi根本不加位置向量：它从每个分数里减去一个和距离成正比的惩罚。<bookmark mark='b'/>每个头有自己的斜率，取自一个等比数列：较陡的斜率更强地惩罚远处的键，较平缓的斜率让它们更容易参与竞争。他们报告说，一个在1024个词元上训练的模型，读2048个词元时，和一个就在这个长度上训练的模型一样好。",

    "And the most surprising answer: give no positions at all.":
        "还有最出人意料的答案：干脆不给位置。解码器仍然有它的因果掩码，而掩码会泄露位置。<bookmark mark='a'/>取一个把注意力平均摊到它能看到的所有东西上的头：在位置t，t个键每个分到t分之1。<bookmark mark='b'/>它的输出就是过去的平均。<bookmark mark='c'/>如果第一个词元带了标记，这个标记在平均里所占的份额就是t分之1，后面的层就能从中读出位置。<bookmark mark='d'/>阿迪·哈维夫和同事们在2022年发现，没有位置信号的语言模型仍然能学会自己在哪里；阿米尔侯赛因·卡泽姆内贾德和同事们则发现，在推理任务上，它们推广到更长输入的能力，比带显式位置的模型还好。Meta的Llama 4把不带位置的层，穿插在用旋转位置的层之间。旋转位置，被许多语言模型采用，就是下一章。",

    # ------------------------------------------------------------------ Rope
    "Chapter nine. Positions as rotations.":
        "第9章。用旋转表示位置。",

    "In 2021 Jianlin Su and colleagues":
        "2021年，苏剑林和同事们提出了一种如今被许多语言模型采用的方法：不把位置加到输入上，而是去旋转查询和键。把一个查询的32个数分成16对；每一对是平面上的一根箭头。<bookmark mark='a'/>在位置m，把第j对转过m乘以一个角度θ j。<bookmark mark='b'/>第一对转得很快，每6个字符转一整圈；之后的每一对都转得更慢，一直慢到3.5万个字符才转一圈。<bookmark mark='c'/>键也用同样的方式旋转。就像钟表的指针：快指针告诉你附近的位置，慢指针告诉你在一篇长文里走到了哪里。这就是RoPE，旋转位置编码。",

    "Why rotations? Here is the whole proof.":
        "为什么用旋转？这里是完整的证明。把位置m处的旋转记作R m。<bookmark mark='a'/>旋转后的查询和旋转后的键，分数是q的转置，乘R m的转置，乘R n，再乘k。<bookmark mark='b'/>旋转的转置，就是反方向的旋转。<bookmark mark='c'/>先往回转m，再往前转n，就是转了n减m。<bookmark mark='d'/>固定旋转之前的查询和键时，位置因子只取决于带符号的相对位移n减m。数值检验用了一对随机向量，位置从0到39。",

    "Here is the same fact, seen on one pair":
        "在一对数上看同一个事实：位置5的一个查询，和位置2的一个键。<bookmark mark='a'/>它们的分数取决于两者之间的夹角。现在把两个都往后移同样的距离，同时保持旋转之前的内容向量不变。<bookmark mark='b'/>两根箭头转过同样的角度，所以它们之间的夹角不变，分数也不变。<bookmark mark='c'/>对于这些固定的内容向量，同时把两个位置移动同样的距离，旋转后的分数保持不变。",

    "And a bonus. Score a query against an identical key":
        "还有一个额外的好处。拿一个查询和一个与它完全相同的键打分，让每对能量相同，再把它们拉开。图中分数是各个余弦的等权平均，并对邻近距离做平滑：<bookmark mark='a'/>相位抵消时，分数会振荡。它并不单调，学到的查询和键也可以给各对不同的权重；仅凭这个参考曲线，不能保证偏向最近的词元。<bookmark mark='b'/>从2021年起，许多语言模型采用了旋转位置。",

    '"Which hands does a trained model actually use?':
        "训练好的模型实际上用的是哪些指针？2024年，费德里科·巴尔贝罗和同事们查看了谷歌Gemma的内部：它最快的那些对，构造出尖锐的位置模式，比如恰好往回看一个词元；而最慢的那些对，几乎不转，似乎承载着含义。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>设计者们听懂了这个暗示。Qwen3-Next每个头的256个数里只旋转64个，其余的不动；Gemma 3把全局层的底数增大一百倍，从一万改为一百万。这主要减慢了低频的那些对，最快的一对则保持不变。",

    "f'Our small model has a favourite":
        '我们的小模型有一个最爱：第{jm + 1}对，它每{wl[jm]:,.0f}个字符才转一圈，比它的整个上下文还长，却承载了查询和键归一化平方大小平均值的{e[jm]:.0%}，是平均份额的{e[jm] * n:.1f}倍。波长更长，仍然会在这个上下文内旋转；仅凭这个范数份额，不能判断它承载了什么信息。',

    "f'Our small model does the same":
        '我们的小模型也是这样：在它的{ctx}个字符里一圈都转不完的那{len(slow)}对，承载了查询和键归一化平方大小平均值的{s_slow:.0%}，而如果平均分配，应该是{even:.0%}。',

    "f'Our small model shows no such preference":
        '我们的小模型没有表现出这种偏好：在它的{ctx}个字符里一圈都转不完的那{len(slow)}对，承载了查询和键归一化平方大小平均值的{s_slow:.0%}，和平均分配的{even:.0%}差不多。',

    # ------------------------------------------------------------------ Longer
    "Chapter eleven. Longer than it was trained for.":
        "第11章。比训练时更长。",

    'f"Our model was trained on stretches of {ctx}':
        "我们的模型是在{ctx}个字符一段的文本上训练的。如果给它{s}倍那么长的文本呢？<bookmark mark='a'/>在训练长度以内，它照常工作。<bookmark mark='b'/>一过这个长度，它就垮了：从每字符{near:.1f}比特，变成{far:.1f}比特。它的时钟上那些慢指针，现在指向了训练中从没见过的角度，它的查询和键也就不再是原来的意思了。<bookmark mark='c'/>什么巧办法都不用，每次只读最后{ctx}个字符，反而要好得多。长上下文不是白来的。",

    'f"So people rescale the clocks.':
        "于是人们给时钟重新调速。<bookmark mark='a'/>位置插值把每根指针都放慢同样的倍数，{s}倍，这样更长的文本也只覆盖训练中见过的角度，但快指针会丢掉细节。<bookmark mark='b'/>NTK感知的技巧，名字来自第12部分的神经正切核，它把慢指针放慢很多，快指针几乎不动。<bookmark mark='c'/>YaRN不动快指针，把慢指针完全放慢，中间用一段斜坡过渡，再把注意力稍微调尖一点。<bookmark mark='d'/>在我们的模型上，不重新训练，最好的是{names[best]}：最远端是{b[best]:.2f}比特，而什么都不做是{b['plain']:.1f}{win_txt}Qwen和DeepSeek用YaRN读到了12.8万个词元。",

    "f', and better even than the {ctx}-character window.'":
        "，甚至比{ctx}个字符的窗口还好。",

    'f"Here is YaRN\'s recipe exactly':
        "这里是YaRN的精确配方。<bookmark mark='a'/>对每一对数，数一数它的指针在训练上下文里转了几整圈：r，等于上下文长度除以这一对的波长。<bookmark mark='b'/>我们最快的那一对，在{ctx}个字符里转了大约{r[0]:.0f}圈；每个角度它都见过，所以YaRN不去动它。<bookmark mark='c'/>最慢的那些对，连一整圈都转不完，所以YaRN把它们按{s}倍完全放慢。<bookmark mark='d'/>两者之间是一段斜坡，γ：不到一圈时为0，超过32圈时为1。<bookmark mark='e'/>每个新角度，都按γ把放慢后的角度和原来的角度混合起来。在我们的头里，{kept}对保持不变，{len(ramp_i)}对在斜坡上，{slowed}对完全放慢。<bookmark mark='f'/>放慢指针也会让注意力变平，所以YaRN把每个分数乘以0.1倍的log s加1的平方：s等于{s}时，是{mult:.2f}。",

    'f"A longer text also has more keys to share the weights.':
        "更长的文本里，也有更多的键来分享权重。<bookmark mark='a'/>假设最好的那个键，分数比其余n减1个键高出δ：它的权重就是e的δ次方，除以e的δ次方加n减1。<bookmark mark='b'/>要让这个权重在n变大时保持不变，δ就得像log n那样增长。<bookmark mark='c'/>所以把每个分数都乘以log n，以训练长度为单位：在训练长度以内什么都不变，超过它，注意力也和训练时一样尖锐。大卫·蒋和彼得·乔拉克在2022年提出了它；Qwen和Llama 4都用了它的某种版本。<bookmark mark='d'/>{v1}<bookmark mark='e'/>{v2}这里最好的是{SPOKEN_EXT[best]}，{far[best]:.2f}比特。",

    "f'On our model, scaling alone takes":
        "在我们的模型上，单靠缩放，就把最远端从{far['plain']:.2f}比特变成了{far['logn']:.2f}比特。",

    "f'On our model, scaling alone barely changes":
        "在我们的模型上，单靠缩放，最远端几乎没变：从{far['plain']:.2f}到{far['logn']:.2f}比特，因为它的问题出在坏掉的角度上，而不在注意力摊得多开。",

    "f'On top of the NTK rescaling it helps again":
        "叠加在NTK缩放之上，它又有帮助：从{far['ntk']:.2f}到{far['ntk_logn']:.2f}。",

    "f'On top of the NTK rescaling it changes little":
        "叠加在NTK缩放之上，它也没带来多少变化：从{far['ntk']:.2f}到{far['ntk_logn']:.2f}。",

    'f"Real models then train briefly at the new length.':
        "真实的模型接着会在新的长度上短暂地训练。我们也这样做了：{steps}步，每步用{T:,}个字符的窗口，大约是原来训练量的百分之{100 * chars / float(t['tokens']):.0f}，一次从位置插值出发，一次从YaRN出发；角落里是它们的训练损失。<bookmark mark='a'/>虚线是训练前，实线是训练后。<bookmark mark='b'/>{v}<bookmark mark='c'/>{v_end}DeepSeek-V3就是这样，用两千步，从4千个词元扩展到了12.8万个。",

    "f'Position interpolation falls from":
        "在最远端，位置插值从{far['pi']:.2f}比特降到{far['ft_pi']:.2f}，YaRN从{far['yarn']:.2f}降到{far['ft_yarn']:.2f}。",

    "f'YaRN ends ahead by {gap:.2f} bits, and beats":
        "最后YaRN领先{gap:.2f}比特，而且胜过了只读最后{ctx}个字符的{far['window']:.2f}。",

    "f'Interpolation ends ahead by {gap:.2f} bits, and beats":
        "最后位置插值领先{gap:.2f}比特，而且胜过了只读最后{ctx}个字符的{far['window']:.2f}。",

    "f'YaRN ends ahead by {gap:.2f} bits, but neither":
        "最后YaRN领先{gap:.2f}比特，但两者都还比不上简单地只读最后{ctx}个字符，{far['window']:.2f}。",

    "f'Interpolation ends ahead by {gap:.2f} bits, but neither":
        "最后位置插值领先{gap:.2f}比特，但两者都还比不上简单地只读最后{ctx}个字符，{far['window']:.2f}。",

    # ------------------------------------------------------------------ Caps
    "Chapter thirteen. Keeping scores in range.":
        "第13章。让分数待在范围之内。",

    'f"Chapter three divided by the square root of d':
        "第3章除以根号d，是为了在训练一开始让分数待在范围之内。但训练会让权重变大，而一个分数是其中两个权重的乘积：<bookmark mark='a'/>固定一层的输入，把W Q和W K都放大c倍，这一层的分数就放大c的平方倍。<bookmark mark='b'/>图中重新跑了完整网络，后面各层的隐藏状态可以改变。来看看我们自己的Transformer得到什么结果。c等于2时，最大的分数从{lg[0]:.0f}变成{lg[i2]:.0f}，注意力的熵从{ent[0]:.1f}比特降到{ent[i2]:.1f}，一个键拿走九成以上权重的行所占的比例，从{pk[0]:.0%}变成{pk[i2]:.0%}。<bookmark mark='c'/>模型的猜测也变差了：从每字符{bits[0]:.2f}比特变成{bits[i2]:.2f}，c等于{cs[-1]:.0f}时是{bits[-1]:.2f}。<bookmark mark='d'/>在大规模训练中，这会自己发生：2023年，训练谷歌那个220亿参数视觉Transformer的团队看到，注意力的logit无限制地增长，直到训练发散。",

    '"The fix the vision team used':
        "视觉团队用的、此后许多语言模型也在用的修补办法，是QK归一化。<bookmark mark='a'/>在做点积之前，把每个头的查询和键都除以它们的均方根大小，再乘以一个学出来的增益。<bookmark mark='b'/>查询和键的均方根非零时，一个向量除以它的均方根，长度恰好是根号d，<bookmark mark='c'/>若所有增益的绝对值都不超过g，由柯西-施瓦茨不等式，分数绝对值就不超过g的平方乘以根号d，即使W Q和W K变大也是如此。<bookmark mark='d'/>{moves}<bookmark mark='e'/>{cost}<bookmark mark='f'/>Qwen3、GLM-4.5和Gemma 3都用了它；第18部分会在训练中观察logit，对比有它和没有它的情况。",

    "On our transformer, with its queries and keys normalized to their trained sizes, growing the weights now changes":
        "在我们的Transformer上，把查询和键归一化到它们训练后的大小，现在再放大权重，就什么都不会改变了。",

    "f'On our transformer, with its queries and keys normalized":
        "在我们的Transformer上，把查询和键归一化到它们训练后的大小，现在再放大权重，熵只变化了{flat:.3f}比特。",

    "f'But bolted onto a model that was trained without it":
        '但把它硬装到一个没用它训练过的模型上，每字符要多付{bn - b0:.2f}比特，{bn:.2f}对{b0:.2f}。这个固定权重的干预改变了已学到的行为；带QK归一化训练或再适应，是另外的实验。',

    "Bolted onto a model trained without it, it costs almost nothing here.":
        "把它硬装到一个没用它训练过的模型上，在这里几乎没有代价。",

    'f"A gentler alternative is a soft cap':
        "一个更温和的替代办法是软上限：把每个分数s，换成c乘以s除以c的双曲正切。<bookmark mark='a'/>小的分数几乎原样通过；大的分数则在正负c处趋于平缓。<bookmark mark='b'/>把c设得比我们训练好的模型的最大分数{capv:.0f}稍高一点，再放大权重：分数再也超不过{capv:.0f}，而且{et}。<bookmark mark='d'/>{bt}<bookmark mark='c'/>Gemma 2在2024年把注意力分数的上限设为50；Gemma 3则放弃了上限，改用QK归一化，它在点积之前控制查询和键的大小。",

    "f'the entropy falls only to":
        "熵只降到{ent_c[-1]:.1f}比特，而不是{ent_p[-1]:.1f}",

    "f'the entropy falls just as far":
        "熵降得一样多，降到{ent_c[-1]:.1f}比特",

    "f'At c of {cs[-1]:.0f} the bits per character":
        "c等于{cs[-1]:.0f}时，每字符比特数是{bits_c[-1]:.2f}，而不是{bits_p[-1]:.2f}。",

    "f'But the guesses get worse, not better":
        '但猜测变得更差，而不是更好：c等于{cs[-1]:.0f}时，每字符{bits_c[-1]:.2f}比特，不加上限是{bits_p[-1]:.2f}。每个大分数都被压平到上限上，一个头就不能保留这些分数差了。这个固定权重的实验，并没有为一个从训练起就使用软上限的模型选定上限。',

    "f'The bits per character suffer about as much":
        "每字符比特数也差不多同样变差，{bits_c[-1]:.2f}。",

    # ------------------------------------------------------------------ RASP
    "Chapter sixteen. What a transformer can compute.":
        "第16章。Transformer能算什么。",

    "We have taken attention apart.":
        "我们已经把注意力拆开看过了。那整台机器能算什么？2021年，盖尔·魏斯、约阿夫·戈德堡和埃兰·亚哈夫把它写成了一门编程语言，RASP，里面只有Transformer具备的那些运算。<bookmark mark='a'/>select，也就是选择，用键和查询的比较搭出一个注意力模式。<bookmark mark='b'/>aggregate，也就是聚合，对选中的值取平均。<bookmark mark='c'/>逐元素的函数，就是MLP。<bookmark mark='d'/>用它写的程序读起来是这样的：直方图，也就是每个词元出现了几次，一层就够；排序要两层。每个程序都说明了它需要多少层、多少个头。2023年，DeepMind的一个团队造了Tracr，能把这样的程序编译成真正的Transformer权重。我们手工编译了两个。",

    '"The histogram first.':
        "先看直方图。给词元用独热向量，一个头的QK矩阵就是一张查找表：两个词元之间，我们想做什么比较都行。<bookmark mark='a'/>如果两个词元相同，就给这一对打β分；再给一个起始标记，从每个查询来看都打同样的分。<bookmark mark='b'/>这样，一个出现了c次的词元，就会把注意力分给它的c个副本和那个标记，于是标记分到c加1分之1。<bookmark mark='c'/>只让标记携带一个值，一个小小的ReLU层就能把次数读回来。这个标记扮演的，正是第12章那个汇点的角色。<bookmark mark='d'/>{v_ran}但要分清c加1分之1和c加2分之1，c越大，需要的比特就越多：在bfloat16里，次数过了{pb}就糊成一片；在float16里，是过了{p16:,}。固定的精度，是长度之所以难的原因之一。",

    "f'We ran it on {tr:,} random sequences: all":
        "我们在{tr:,}个随机序列上运行了它：全部{ok:,}个都对。",

    "f'We ran it on {tr:,} random sequences: {ok:,}":
        "我们在{tr:,}个随机序列上运行了它：{ok:,}个正确。",

    '"Sorting takes two layers.':
        "排序要两层。<bookmark mark='a'/>第一层里，每个词元选中所有比它小的词元，外加那个标记：标记所占的份额给出它的名次，也就是排好序后有多少个排在它前面。<bookmark mark='b'/>第二层里，输出位置p选中名次为p的那个词元，把它复制过来。<bookmark mark='c'/>{v_sorted}没有人训练过它们：Transformer的权重可以就是一个程序。",

    "f'Our hand-built weights sort every one":
        "我们手工搭的权重，把{tr:,}个随机输入每一个都排对了。",

    "f'Our hand-built weights sort {ok:,} of":
        "我们手工搭的权重，在{tr:,}个随机输入里排对了{ok:,}个。",

    "What can't a transformer do?":
        "Transformer做不到什么？固定的层数，就是固定量的顺序计算。<bookmark mark='a'/>威廉·梅里尔和阿希什·萨巴瓦尔在2023年证明：在其形式模型中，如果Transformer的深度固定、数值大约只有log n个比特，而且基本操作能在对数空间中计算，就可以用常数深度的阈值电路来模拟它：也就是TC零类。<bookmark mark='b'/>如果像大多数人相信的那样，这个类比NC一要弱，那么这种形式模型里的固定深度Transformer，就不能在任意长度上追踪五个物体的一连串洗牌。在实践中深度也很要紧：一层是搭不出归纳头的。<bookmark mark='c'/>增加顺序计算的一种方法，是生成：每一个新词元，都再把所有层走一遍，这是第28部分的故事。增加深度，或使用循环，也是办法。<bookmark mark='d'/>哈蒂·周和同事们提出了RASP-L假说：如果有一个简短的因果RASP-L程序解决任意长度，训练完成，并且多样的例子排除了更短却会失效的捷径，就更可能出现长度泛化。这是一个有实验支持的猜想。",

    # ------------------------------------------------------------------ Frontier
    "Chapter seventeen. Attention in 2026.":
        "第17章。2026年的注意力。",

    'f"Why so much effort?':
        "为什么要费这么大劲？用第7章的算术，算一个和DeepSeek-V3一样宽的模型：<bookmark mark='a'/>上下文是四千个词元时，注意力的成本是权重成本的{r4:.2f}；到一百万个，是{r1m:.0f}倍。<bookmark mark='b'/>长上下文让注意力成了最贵的部分。",

    "Every model in 2026 still computes this formula somewhere.":
        "2026年的每一个模型，仍然在某处计算着这个公式。变的是在哪里算，以及算多少。<bookmark mark='a'/>在注意力模块内部，是前面几章的那些修补：汇点logit、输出门控、QK归一化，还有完全没有位置的层。<bookmark mark='b'/>每个过去的词元留下的键和值，已经被压小了：在多个头之间共享，或者从一个小的潜在向量重建出来，这是把第4章的低秩想法用在了记忆上。<bookmark mark='c'/>许多模型只看过去的一部分：一个滑动窗口，或者一个又小又快的索引器，为每个查询挑出几千个过去的词元。<bookmark mark='d'/>还有些模型把大多数注意力层，换成一个边读边更新的固定大小的记忆：在Qwen3-Next和Qwen3.5里，每一个注意力层配三个这样的层。",

    "Here is what such a hybrid looks like":
        "这样的混合架构长这样：2026年发布的Kimi K3有93层，其中只有24层是完整的注意力。<bookmark mark='a'/>其余各层保留一个固定大小的记忆，边读边更新。<bookmark mark='b'/>为什么还要留注意力？因为注意力可以回看过去词元存下的键和值；而固定大小的记忆必须决定忘掉什么。少数几层注意力负责回想，其余的负责压低成本。<bookmark mark='c'/>那种记忆怎样工作，它为什么是乔装打扮的注意力，就是我们接下来要去的地方：先在第14部分走过这些模型本身的谱系，再到第15部分讲记忆。",

    # ------------------------------------------------------------------ Outro
    'f"Let\'s take stock.':
        "我们来盘点一下。注意力是一个加权平均，是核由网络学出来的纳达拉亚-沃森平滑器；它也是一次记忆读取，现代霍普菲尔德网络的一步。除以根号d，让它的softmax不至于塌缩。头沿着少数几个方向比较和搬运，掩码决定谁能看到谁，一个模块的成本是12倍的d平方个权重，再加上一项随上下文增长的成本。我们的Transformer达到了每字符{float(t['passage_bits']):.2f}比特。位置可以加上去、转进去、用惩罚表示，或者干脆不给，小心处理还能拉长。汇点logit和门控给了softmax一个停放的地方；训练出来的头会找到算法：复制、一步梯度下降、程序，只是受限于一些边界，只有更多步的思考才能去掉它们。",

    'This comes back everywhere:':
        '这些会在各处再次出现：第14部分，用这个模块搭起来的模型；第15部分，键和值的记忆；第16部分，只看过去的一部分；第18部分，长上下文和失控的logit；第19部分，快速推理服务；第28部分，超越固定深度的思考；第30部分，真实模型里的回路。',

    "Here are six problems to try":
        "这里有六道题可以试试，从点积的方差，一直到写成注意力的梯度下降。在这里暂停，把它们做一做；完整的解答在本部分的笔记里。",

    "Next time: the lineage.":
        "下一次：谱系。我们今天搭的这个模块，从2017年的一个翻译模型开始，一路叠高、放大，到GPT-3、ChatGPT，再到2026年的开放权重前沿；还有我们自己的GPT式模型和BERT式模型，在小说上并排训练。",

    "Anthropic's 'Mathematical Framework":
        "接下来最值得读的，是Anthropic的《Transformer回路的数学框架》。感谢观看，第14部分见。",

    # ------------------------------------------------------------------ SideBySide
    "Chapter ten. Four answers, trained side by side.":
        "第10章。四种答案，并排训练。",

    'f"Now the experiment.':
        "现在来做实验。四个小Transformer，除了怎样得知每个字符的位置之外，其余完全相同：加在输入上的正弦信号、旋转位置、ALiBi的线性惩罚，以及什么都不给。这里回放的是它们学习的过程：留出数据上的每字符比特数，一步一步地变化。<bookmark mark='a'/>每一个都在小说上训练{c['steps']:,}步，每步用{c['ctx']}个字符的窗口，窗口相同，顺序也相同；每一个都用不同的随机起点训练三次，色带表示三次之间的差别。<bookmark mark='b'/>{v_train}",

    "f'The order keeps changing":
        "直到最后一个检查点，第{s_end:,}步，排名都还在变。",

    "f'From step {s_fix:,} on, the order never changes, and":
        "从第{s_fix:,}步起，排名就再也没变过，而最好和最差之间的差距越拉越大：从那时的{g_fix:.2f}比特，到最后的{g_end:.2f}。",

    "f'From step {s_fix:,} on, the order never changes, while":
        "从第{s_fix:,}步起，排名就再也没变过，而最好和最差之间的差距在缩小：从那时的{g_fix:.2f}比特，到最后的{g_end:.2f}。",

    'f"First, inside the length they were trained on':
        "先看它们训练过的长度以内，也就是前{T}个字符。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}",

    "f'{CAP[best]} is best":
        "{CAP[best]}最好，{vals[best].mean():.3f}，而且它的每一个种子都胜过其他方法的每一个种子。",

    'f"The best mean is {SPOKEN[best]}':
        "平均最好的是{SPOKEN[best]}，{vals[best].mean():.3f}，但各个种子的结果互相重叠：这里的差距最多{gap:.3f}比特，并不比同一种设计不同种子之间{spread:.3f}的差别大多少。",

    "f'No positions at all comes first":
        "不给位置的模型排第一，{nope_v:.3f}：单靠因果掩码，它就知道自己在哪里。",

    "f'No positions at all comes {rank_word}, at {nope_v:.3f}, only":
        "不给位置的模型排{rank_word}，{nope_v:.3f}，只落后{behind:.3f}：因果掩码确实告诉了它自己在哪里。",

    "f'No positions at all comes {rank_word}, at {nope_v:.3f}, {behind:.2f}":
        "不给位置的模型排{rank_word}，{nope_v:.3f}，比最好的落后{behind:.2f}比特：掩码告诉了它一些东西，但不是全部。",

    'f"Now read four times as far':
        "现在读远四倍，{R}个字符，尽管它们谁也没见过超过{T}个字符的文本。<bookmark mark='a'/>这是每个位置上的每字符比特数，每种各三个种子。<bookmark mark='b'/>{v_held}<bookmark mark='e'/>{v_mid}<bookmark mark='f'/>{v_broke}<bookmark mark='d'/>{rope_txt}",

    "RoPE's slow hands point at angles":
        "RoPE的慢指针指向了训练中从没见过的角度，它的查询也就不再和它的键对得上：这正是下一章要解决的问题。",

    "RoPE holds up here":
        "RoPE在这里撑住了；下一章会展示它在哪里真的会垮。",

    "f'Broken, up by as much as":
        "彻底失效，最多升高了{br:.1f}比特：{n_broke}。",

    "f'Steady past the training length, within":
        "过了训练长度依然稳定，变化在{hr:.2f}比特以内：{n_held}。",

    "f'Steady past the training length, and even":
        "过了训练长度依然稳定，甚至还好了{-hr:.2f}比特，因为每个字符身后有更多的文本：{n_held}。",

    "f'Drifting up, by {mhi:.2f}":
        "慢慢往上漂，升高了{mhi:.2f}比特：{n_mid}。",

    "f'Drifting up, by {mlo:.2f}":
        "慢慢往上漂，升高了{mlo:.2f}到{mhi:.2f}比特：{n_mid}。",

    'f"Why does one hold and another drift?':
        "为什么一个撑得住，另一个会漂移？<bookmark mark='a'/>ALiBi的四个头减去一个随距离增长的惩罚，斜率从{m[0]:.2f}一直到{m[-1]:.4f}。一个位于训练长度处、往回{T}个字符的键，对最陡的头已经要扣{c0:.0f}分，对最平缓的头也要扣{c3:.1f}分。<bookmark mark='b'/>过了训练长度，键只会被扣得更多，所以不会发生什么新鲜事：这些头照旧看着近处，边界之外的文本，看起来和边界之内的一模一样。<bookmark mark='c'/>不给位置的模型漂移，有它自己的原因。它读的信号，t分之1，只会越来越小：到了位置{R}，它只有训练中最小值的{ratio:.2f}，这是模型从来不需要分辨的数值。<bookmark mark='d'/>正弦位置和RoPE在边界之外遇到的情况更糟：它们碰到的是从没见过的向量和角度。",

    # ------------------------------------------------------------------ Sinks
    "Chapter twelve. Attention sinks, and three ways out.":
        "第12章。注意力汇点，以及三条出路。",

    '"In 2023 Guangxuan Xiao':
        "2023年，肖光烜和同事们发现了一件怪事：在大模型里，许多头把大部分权重放在最开头的那个词元上，不管它是什么。<bookmark mark='a'/>他们把这些叫作注意力汇点，并且证明：只要留住最前面的四个词元，模型就能用一个短窗口一直读下去，读上几百万个词元。<bookmark mark='b'/>{mine}",

    "f'Some heads of our model put a large share":
        "我们模型的一些头，把很大一部分注意力放在最开头的那个字符上，最多达到{sink.max():.0%}，不管那个字符是什么：大约是平均份额的{ratio:.0f}倍。",

    "f'In our small model, nothing like it":
        "在我们的小模型里，完全没有这回事：没有哪个头给第一个字符的份额超过平均的{ratio:.1f}倍。它的头把注意力停放在别处，停在空格和换行上：有一个头把{hi_sp:.0%}的注意力花在它们身上，尽管它们只占文本的{sps:.0%}。",

    "Why would a head stare at a meaningless token?":
        "一个头为什么要死盯着一个毫无意义的词元？因为softmax。<bookmark mark='a'/>它的权重加起来必须等于1：一个头没法拒绝去看。<bookmark mark='b'/>但许多头只是有时候才有活干：比如，只在某一类词元之后。其余时候，正确的输出是什么都没有。<bookmark mark='c'/>要输出“什么都没有”，唯一的办法就是把权重放在一个值接近0的词元上。一个总在那里、待在开头的词元，就是天然的停放点。<bookmark mark='d'/>2024年，Tianyu Guo、梅松和同事们把这一整套症状，追溯到这种“活跃-休眠”的头上：汇点的值会缩小，而它在残差流里的向量会变得巨大。",

    'f"We can grow a sink on purpose.':
        "我们可以有意地培养出一个汇点。Guo的团队设计了一个任务，其中有一个头只是有时候才需要。<bookmark mark='a'/>我们用小说里最常见的{V_}个字符来做：每个字符都按小说里下一个字符的统计规律出现，只有在触发字符之后例外，触发字符是{trig_txt}，这时下一个字符要复制触发字符前面的那个字符。每个序列都以一个标记开头。<bookmark mark='b'/>一个单层的Transformer用{int(c['steps']):,}步就学会了它，前后三次都是如此。在触发字符之后，它的头往回看一个位置，{pa.mean():.0%}的时候都是这样。<bookmark mark='c'/>{v1}<bookmark mark='d'/>{v2}",

    "f'When there is nothing to copy, it puts {bd.mean():.0%}":
        "没有东西要复制时，它把{bd.mean():.0%}的权重放在起始标记上，而这个标记对下一个字符毫无信息：一个汇点，在一个只有一层的模型里形成了。",

    "f'When there is nothing to copy, it puts only":
        "没有东西要复制时，它只把{bd.mean():.0%}的权重放在起始标记上：训练这么短，汇点还在形成之中。",

    'f"And the marker\'s value has shrunk':
        "而这个标记的值，已经缩小到其他值的{vb.mean() / vr.mean():.2f}倍：这就是值的排空。",

    'f"Its value is {vb.mean() / vr.mean():.2f}':
        "它的值是其他值的{vb.mean() / vr.mean():.2f}倍：还没有排空。",

    '"Three recent designs give a head':
        "最近有三种设计，给了头一个更好的“什么都不做”的办法；我们在同一个任务上训练了每一种，每种三个种子。<bookmark mark='a'/>gpt-oss给softmax的分母加上一个学出来的数，相当于一个看不见的键的分数。<bookmark mark='b'/>门控注意力把每个头的输出乘以输入的一个sigmoid。<bookmark mark='c'/>差分注意力取两张softmax图的差。<bookmark mark='d'/>这是每种设计在训练过程中放在标记上的权重。{v_sink}<bookmark mark='e'/>{v_gate}<bookmark mark='f'/>{v_diff}<bookmark mark='g'/>{v_loss}在大模型里，门控把第一个词元上的注意力从46.7%降到了4.8%；Qwen3-Next和Kimi K3现在都给注意力加了门控。",

    "f'The sink logit gives the head a place to send its weight that is not a token at all: its":
        "汇点logit给了头一个地方，可以把权重送去，而那里根本不是一个词元：它放在标记上的权重降到{r_s:.0%}，有{nl:.0%}的权重哪儿也没去。",

    "f'The sink logit gives the head a place to send its weight that is not a token at all, but":
        "汇点logit给了头一个地方，可以把权重送去，而那里根本不是一个词元；但它放在标记上的权重仍然是{r_s:.0%}，只有{nl:.0%}哪儿也没去。",

    "f'The gate lets the head simply switch itself off":
        "门控让头可以干脆把自己关掉：没有东西要复制时，门开到{gd_:.2f}，在触发字符之后开到{ga_:.2f}；它放在标记上的权重是{r_g:.0%}。",

    "f'The gate could let the head switch itself off":
        "门控本可以让头把自己关掉，但最后，没有东西要复制时它开到{gd_:.2f}，和触发字符之后的{ga_:.2f}差不多；它放在标记上的权重是{r_g:.0%}。",

    "f'Differential attention subtracts a second softmax":
        "差分注意力减去第二个softmax，所以它的权重不必加起来等于1：没有东西要复制时，它们加起来只有{sm_:.2f}，λ是{lm_:.2f}，它放在标记上的权重是{r_d:.0%}。",

    "All four learn the task about equally well":
        "四种都把任务学得差不多一样好，所以这个任务本身从来不需要汇点；汇点只是softmax“什么都不做”的办法。",

    "f'They do not learn the copies equally well":
        "它们学复制学得并不一样好：{worst_name}最差，复制部分是{cp[worst_cp].mean():.3f}比特。",

    # ------------------------------------------------------------------ Induction
    "Chapter fourteen. Induction heads.":
        "第14章。归纳头。",

    '"A test no counting model can pass':
        "这是一个任何计数模型都通不过的测试：取一段我们的Transformer从没见过的小说文字，连着给它看两遍。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{tail}",

    "The machinery behind copying has a name.":
        "复制背后的机制，有一个名字。",

    "Copying needs a particular piece of machinery":
        '复制需要一种特定的机制，而我们的Transformer还没有把它搭起来。',

    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: it copies":
        '第一遍，每字符{m1:.2f}比特；第二遍，{m2:.2f}：它在从自己的上下文里复制。',

    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: a little":
        "第一遍，每字符{m1:.2f}比特；第二遍，{m2:.2f}：好了一点，但它几乎不复制。",

    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: no better":
        "第一遍，每字符{m1:.2f}比特；第二遍，{m2:.2f}：一点也没变好。答案就摆在一百个字符之前，我们的Transformer却不去用它。",

    "f'Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, {u26:.1f}; {q2:.1f}":
        '再看随机字母：第一遍{q1:.1f}比特，比在26个字母里瞎猜的{u26:.1f}还差；第二遍{q2:.1f}：至少在这里，它会复制。',

    "f'Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, {u26:.1f}; and":
        '再看随机字母：第一遍{q1:.1f}比特，比在26个字母里瞎猜的{u26:.1f}还差；第二遍是{q2:.1f}：这里也没有复制。',

    "f'Random letters: {q1:.1f} bits the first time, {q2:.1f}":
        '再看随机字母：第一遍{q1:.1f}比特，第二遍{q2:.1f}：至少在这里，它会复制。',

    "f'Random letters: {q1:.1f} bits the first time, and":
        '再看随机字母：第一遍{q1:.1f}比特，第二遍{q2:.1f}：这里也没有复制。',

    'It takes two heads, in two layers.':
        "这需要两个头，分在两层。<bookmark mark='a'/>在较早的一层里，有一个头只往回看一步：于是每个字符的向量里，还记下了它前面是哪个字符。<bookmark mark='b'/>在较晚的一层里，第二个头读到一个l，就问：之前哪个字符，紧跟在一个l后面？Falcon里的那个c回答了，因为它的记录上写着：我前面是一个l。<bookmark mark='c'/>于是这个头把它复制过来：c。见过A后面跟着B？再看到A时，就预测B。2022年，Anthropic的凯瑟琳·奥尔森和同事们把它们命名为归纳头。",

    'f"Induction heads can be watched as they form, in a small':
        "归纳头的形成过程是可以看到的：一个只有注意力的小模型，在随机词元上训练，里面某处有一段重复。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v_jump}<bookmark mark='c'/>看看里面：第一层往回看一步，第二层看向更早的那段副本，往前错一步。奥尔森的团队在大模型里也看到了同样的突然跃变，恰好在它们变得擅长从提示中学习的时候。",

    "f'With one layer it never learns to copy":
        "只有一层时，它永远学不会复制：{int(c1[-1, 0]):,}步之后，它在重复段上仍然是{f1:.1f}比特。一个头没法既记下每个位置前面的词元，又去搜索它。",

    "f'With one layer it ends at":
        "只有一层时，它最后在重复段上是{f1:.1f}比特。",

    "f'With two layers, nothing happens for a while, and then the loss on the repeat falls off a cliff, around":
        "有两层时，有一阵子什么都没发生，然后重复段上的损失突然断崖式下跌：在我们所有的运行里，都在第{js[0]:,}步左右，降到{lo2:.2f}到{hi2:.2f}比特。",

    "f'With two layers, nothing happens for a while, and then the loss on the repeat falls off a cliff, between":
        "有两层时，有一阵子什么都没发生，然后重复段上的损失突然断崖式下跌：在我们的{len(js)}次运行里，发生在第{min(js):,}步到第{max(js):,}步之间，降到{lo2:.2f}到{hi2:.2f}比特。",

    'f"Here are the two heads forming':
        "下面就是这两个头的形成过程，一个检查点接一个检查点，旁边是重复段上的损失。<bookmark mark='a'/>一开始，两个头都漫无目的地四处看。<bookmark mark='b'/>然后，在第{js:,}步左右，第二个头找到了那条斜纹：它在那里的注意力在{steps[kb] - steps[ka]}步之内从{ind_sc[ka]:.2f}跳到{ind_sc[kb]:.2f}，重复段上的损失也从{lo_a:.1f}比特降到{lo_b:.1f}比特。{together}单独都没用，合在一起就能复制。",

    "f'The first head turns to the token one back in the same window":
        "第一个头也在同一段时间里转向往回看一个词元，到第{steps[kb]:,}步达到{prev_sc[kb]:.2f}。",

    "f'The first head had already turned":
        "第一个头早在第{steps[kp]:,}步就已经转向往回看一个词元了：归纳头是在它的基础上搭起来的。",

    "f'The first head turns to the token one back only later":
        "第一个头要到更晚，第{steps[kp]:,}步，才转向往回看一个词元。",

    'f"The cooperation shows in the weights alone.':
        "这种合作，只看权重就能看出来。<bookmark mark='a'/>K组合，来自纳尔逊·埃尔哈格和同事们，衡量的是一个较晚的头的键，从一个较早的头写下的东西里读了多少：较晚的头的QK矩阵和较早的头的OV矩阵乘积的大小，相对于两者各自的大小。随机的头大约得{base:.2f}分。<bookmark mark='b'/>{v}",

    'f"For the {n_p} previous-token heads paired with the {n_i} induction heads, it climbs':
        '对{n_p}个前一词元头和{n_i}个归纳头的配对，它随着归纳头的形成，从{k0:.2f}升到{k1:.2f}；同样这些配对的Q组合最后是{q1:.2f}，其他所有配对是{o1:.2f}。归纳头的键，读的正是前一词元头写下的东西。',

    "f'For the {n_p} previous-token heads paired with the {n_i} induction heads, it ends":
        '对{n_p}个前一词元头和{n_i}个归纳头的配对，它最后是{k1:.2f}，相比之下，Q组合是{q1:.2f}，其他所有配对是{o1:.2f}：在这个小模型里，信号并不干净地落在键上。',

    '"And our own transformer, trained on novels':
        "那我们自己的Transformer呢？它是在小说上训练的，根本没有复制游戏。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}",

    'f"Our transformer has one:':
        "我们的Transformer有一个：第{li + 1}层的头{hi + 1}，平均把{ind.max():.0%}的注意力，恰好放在归纳头该放的地方，也就是早先那段副本往后一步。",

    'f"Our transformer has none:':
        '我们的Transformer一个也没有：最好的候选，第{li + 1}层的头{hi + 1}，只把{ind.max():.1%}的注意力放在早先副本往后一步的位置上；到最后，第二遍每字符{c2[-1]:.2f}比特，第一遍{c1[-1]:.2f}。',

    "f'Its heads compose a little":
        '它的头有一点组合，最强是{top:.2f}，随机的头是{base:.2f}，但没有哪一对变成了复制回路。',

    "f'And its heads barely compose":
        "而且它的头几乎不组合：最强的K组合是{top:.2f}，随机的头是{base:.2f}。",

    'f"Why not? Olsson\'s team saw induction heads appear after two and a half to five billion tokens; ours has read {tokens / 1000000.0:.0f} million characters, and a novel rarely repeats a long stretch within 256 characters. The toy':
        '为什么没有？奥尔森的团队看到，归纳头是在25亿到50亿个词元之后才出现的；我们的模型读了{tokens / 1000000.0:.0f}00万个字符，而且小说很少在256个字符之内重复一长段。那个专为奖励复制而设计的玩具模型，在{jmax:,}步之内就形成了这一对头。',

    'f"Why not? Olsson\'s team':
        '为什么没有？奥尔森的团队看到，归纳头是在25亿到50亿个词元之后才出现的；我们的模型读了{tokens / 1000000.0:.0f}00万个字符，而且小说很少在256个字符之内重复一长段。',

    # ------------------------------------------------------------------ InContext
    "Chapter fifteen. Learning inside the prompt.":
        "第15章。在提示里学习。",

    "Large models learn from examples in their prompt":
        "大模型能从提示里的例子中学习，却一个权重也不改。给它看几个翻译的例子，它就会翻译下一个。一次前向传播怎么能学习？<bookmark mark='f'/>前向传播就是把网络跑一遍：数字进去，每一层流过一次，出来一个猜测。这中间没有任何权重被改动。这里有一个小到可以彻底拆开的例子。<bookmark mark='a'/>每个提示是一串例子：四个数x，和一个答案y，y是这四个数的一个固定的加权和。然后是一个问题：一个新的x，答案空着。<bookmark mark='b'/>难点在于：每个提示用的隐藏权重都不一样，所以不能用同一个固定回归向量回答所有提示。要回答，模型必须利用眼前的例子。",

    'f"Take the simplest attention':
        "取最简单的注意力：一层，没有softmax。每个词元是一个例子的数和它的答案，注意力给每个词元加上其他词元的一个加权和。在许多提示上训练它：采样记录的训练批次误差，从{cv[0, 1]:.1f}到最后一个记录检查点的{cv[-1, 1]:.2f}。<bookmark mark='a'/>这是它学到的两个矩阵。蓝色是正，红色是负。<bookmark mark='b'/>现在换一件事来做：在提示里的例子上，从零出发，对第6部分的最小二乘损失走一步梯度下降。这一步是每个答案乘以它的x再求和，而预测是每个答案乘以“它的x和问题有多匹配”再求和：x之间的点积，给y加权。<bookmark mark='c'/>这就是注意力，用的就是这两个矩阵：一个比较x的单位矩阵块，和一个把y传下去的元素。它们的分块结构与学到的矩阵相似；预测是否一致，是另外的测量。",

    '"Check it on four thousand new prompts.':
        "在四千个新提示上检验一下。每个点是一个问题：横轴是一步梯度下降给出的答案；纵轴是训练好的注意力层给出的答案。<bookmark mark='a'/>{v_line}约翰内斯·冯·奥斯瓦尔德和同事们在2023年证明了这一点。",

    "f'They lie on a line.":
        "它们落在一条直线上。相关系数是{r_:.3f}；相关系数衡量这些点贴着一条直线贴得有多紧，等于1就表示恰好落在线上。这个网络的前向传播，就是一步学习，在它提示里的例子上运行。",

    "f'They follow a line, loosely":
        "它们大致沿着一条直线：相关系数是{r_:.3f}；相关系数衡量这些点贴着一条直线贴得有多紧，等于1就表示恰好落在线上。这个网络的前向传播，接近于一步学习。",

    '"Stack more layers, and each can take another step.':
        "再多叠几层，每一层都能再走一步。<bookmark mark='a'/>{v_deep}<bookmark mark='b'/>{v_exact}真实的Transformer有softmax注意力和许多层，比这要乱，但道理是相通的：一次前向传播，可以在提示上运行一个学习算法。",

    "f'One layer matches one step of gradient descent. Two layers":
        "一层对得上一步梯度下降。两层胜过两步普通的梯度下降，{l2:.2f}对{g2:.2f}：训练出来的网络，找到了一种比教科书上更聪明的步子。",

    "One layer matches one step of gradient descent, and more layers":
        "一层对得上一步梯度下降，层数越多，就跟得上越多步。",

    "Exact least squares, from Part 6, gets every answer right":
        "第6部分的精确最小二乘，在这里每个答案都对，误差只在舍入的量级，所以还有进步的空间。",

    "f'Exact least squares, from Part 6, reaches":
        "第6部分的精确最小二乘，达到{ls:.2f}。",
    'On our transformer, with its queries and keys normalized to their trained sizes, growing the weights leaves': '在我们的Transformer上，把查询和键归一化到它们训练后的大小，再放大权重，测得的注意力熵几乎不变。',
    '"Check it on four thousand evaluation prompts.': "在四千个评估提示上检验。散点图只画出最前面的两百个已保存问题，相关系数则用全部四千个。梯度下降步长是在这同一批评估提示上，从59个候选值中选出的。每个点是一个问题：横轴是一步梯度下降给出的答案；纵轴是训练好的注意力层给出的答案。<bookmark mark='a'/>{v_line}约翰内斯·冯·奥斯瓦尔德和同事们在2023年研究了这种联系。",
    "f'Their predictions are strongly correlated:": '它们的预测高度相关：{r_:.3f}。相关系数衡量正向线性关联，并不能证明预测完全相同，也不能证明内部学习算法相同。这里报告的统计量针对这些评估提示。',
    "f'Their correlation is": '相关系数是{r_:.3f}，它衡量预测之间的线性关联，不能证明预测完全相同，也不能证明学习算法相同。这项比较只针对这些评估提示。',
    '"Compare separately trained networks with one, two and three attention layers.': "比较分别训练的1层、2层和3层注意力网络。<bookmark mark='a'/>{v_deep}<bookmark mark='b'/>{v_exact}真实的Transformer有softmax注意力和许多层，比这更复杂，但道理是相通的：一次前向传播，可以在提示上运行一个学习算法。",
    "f'One trained layer has similar error to one gradient step. Two layers": '一层训练好的网络和一步梯度下降的误差相近。这里两层的误差低于两步参考梯度下降，{l2:.2f}对{g2:.2f}。这些深度分别训练，再与在评估集上调过步长的梯度下降参考比较。',
    'Here we compare separately trained attention depths': '这里比较分别训练的不同注意力深度，以及在评估集上调过步长的梯度下降参考。',
    "f'Some heads of our model put a large share of it, up to {sink.max():.0%}, on the very first character of sampled windows: about {ratio:.0f} times an even share. '": '我们模型的一些头把大量注意力放在采样窗口的第一个字符上，最多{sink.max():.0%}，大约是平均份额的{ratio:.0f}倍。',
    "f'In our small model, nothing like it: no head gives the first character more than {ratio:.1f} times an even share. For spaces and line breaks, one head spends {hi_sp:.0%} of its attention on them, while they are {sps:.0%} of the text. These summaries have different denominators and do not establish a parking mechanism. '": '我们的小模型没有明显的首位置集中：没有哪个头给第一个字符超过平均份额的{ratio:.1f}倍。空格和换行方面，一个头给它们{hi_sp:.0%}的注意力；它们占文本位置的{sps:.0%}。这两项统计的分母不同，不能证明停放机制。',
    "Why would a head stare at a meaningless token? Because of the softmax. <bookmark mark='a'/> Its weights must add up to one: a head cannot decline to attend. <bookmark mark='b'/> But many heads have work to do only some of the time: after a particular kind of token, say. The rest of the time, the right output is nothing. <bookmark mark='c'/> One way to add almost nothing is to put most weight on a token whose value is close to zero. A token that is always there, at the start, is the natural parking spot. <bookmark mark='d'/> Tianyu Guo, Song Mei and colleagues traced the whole syndrome to such active-dormant heads in 2024: the sink's value shrinks, and its vector in the residual stream grows enormous.": "一个头为什么盯着无信息的词元？softmax要求权重和为1。<bookmark mark='a'/>它不能拒绝分配权重。<bookmark mark='b'/>有些头只在特定词元后需要工作，其余时候应几乎不添加内容。<bookmark mark='c'/>一种办法是把大部分权重放在值接近0的词元上；始终存在的起始位置可充当停放点。<bookmark mark='d'/>Guo、梅松及同事在2024年研究了活跃—休眠头中的值排空与巨大残差激活。",
    "f'When there is nothing to copy, it puts {bd.mean():.0%} of its weight on the start marker, which carries no next-character identity: this endpoint shows start-marker concentration in a one-layer model. '": '没有复制任务时，平均{bd.mean():.0%}的权重落在不提供下个字符身份的起始标记上：这个单层模型的终点显示了起始标记集中。',
    "f'When there is nothing to copy, it puts only {bd.mean():.0%} of its weight on the start marker: in a run there is no strong start-marker concentration at the endpoint. '": '没有复制任务时，只有{bd.mean():.0%}的权重落在起始标记上：这次运行的终点没有强烈的起始标记集中。',
    'f"At the end, the marker\'s mean value-vector norm is {vb.mean() / vr.mean():.2f} times the others\' mean: a small final value, not a measured decrease."': '终点起始标记值向量的平均范数为其他位置平均范数的{vb.mean() / vr.mean():.2f}倍：这是较小的终值，不是测得的下降过程。',
    'f"At the end, the marker\'s mean value-vector norm is {vb.mean() / vr.mean():.2f} times the others\' mean; this comparison does not measure a training trajectory."': '终点起始标记值向量的平均范数为其他位置平均范数的{vb.mean() / vr.mean():.2f}倍；这个比较不测量训练轨迹。',
    'f"We can grow a sink on purpose. Guo\'s team built a task where one head is needed only some of the time. <bookmark mark=\'a\'/> We made it from the novels\' {V_} commonest characters: each character follows the novels\' statistics for what comes next, except after a trigger, {trig_txt}, where the next character copies the one before the trigger. Every sequence starts with a marker. <bookmark mark=\'b\'/> We train a one-layer transformer for {int(c[\'steps\']):,} steps, three times over. After a trigger its head puts {pa.mean():.0%} of its attention weight on the preceding character, on average. <bookmark mark=\'c\'/> " + v1 + "<bookmark mark=\'d\'/> " + v2': "我们用Guo团队的活跃—休眠任务检验汇点。<bookmark mark='a'/>使用小说最常见的{V_}个字符及其下一个字符统计，触发字符为{trig_txt}；触发后复制它前面的字符。每个序列以标记开头。<bookmark mark='b'/>单层Transformer训练{int(c['steps']):,}步，共三个种子。触发后，平均{pa.mean():.0%}的注意力权重落在前一个字符上。<bookmark mark='c'/>{v1}<bookmark mark='d'/>{v2}",
    "f'The gate lets the head attenuate its output; mean feature openness is {gd_:.2f} when there is nothing to copy and {ga_:.2f} after a trigger, and its weight on the marker is {r_g:.0%}.'": '门控可减弱输出：没有复制任务时平均特征开放度{gd_:.2f}，触发后{ga_:.2f}；标记上的注意力权重为{r_g:.0%}。',
    "f'The gate could let the head attenuate its output, but its mean feature openness is similar with nothing to copy, {gd_:.2f}, as after a trigger, {ga_:.2f}, and its weight on the marker is {r_g:.0%}.'": '门控可以减弱输出，但两类位置平均特征开放度接近：没有复制任务时{gd_:.2f}，触发后{ga_:.2f}；标记权重{r_g:.0%}。',
    "f'Differential attention subtracts a second softmax. Every signed row sums to one minus lambda, with lambda at {lm_:.2f}. The saved dormant-row mean sum is {sm_:.2f}, and the dormant start-marker coefficient is {r_d:+.2f}. Subsequent head normalization means this sum is not the output amplitude.'": '差分注意力减去第二张softmax图。每行有符号系数之和都是1减λ，λ为{lm_:.2f}。保存的休眠行平均系数和为{sm_:.2f}，起始标记平均系数为{r_d:+.2f}。之后还有头内归一化，所以该行和不是输出幅度。',
    'The four mean copy-position losses differ by less than 0.05 bits in this run. This compares only copy loss, not whole-task equivalence or whether sinks are causally necessary.': '这次运行四种平均复制位置损失相差不到0.05比特。这里只比较复制损失，不能证明整个任务等价或汇点在因果上是否必要。',
    "f'Mean copy-position losses differ: {worst_name} is highest, at {cp[worst_cp].mean():.3f} bits on the copies.'": '平均复制位置损失不同：{worst_name}最高，为{cp[worst_cp].mean():.3f}比特。',
    '"Three recent designs give a head a better way to do nothing; we trained each on the same task, three seeds each. <bookmark mark=\'a\'/> gpt-oss adds a learned number to the softmax\'s denominator, the score of an invisible key. <bookmark mark=\'b\'/> Gated attention multiplies each head\'s output by a sigmoid of the input. <bookmark mark=\'c\'/> Differential attention subtracts two softmax maps. <bookmark mark=\'d\'/> Here is each design\'s start-marker coefficient during training; differential coefficients are signed, not probabilities. " + v_sink + " <bookmark mark=\'e\'/> " + v_gate + " <bookmark mark=\'f\'/> " + v_diff + " <bookmark mark=\'g\'/> " + v_loss + \' In large models, the gate cut the attention on the first token from 46.7 to 4.8 percent; Qwen3-Next and Kimi K3 now gate their attention.\'': "三种设计改变注意力的输出方式；在相同任务上各训练三个种子。<bookmark mark='a'/>汇点logit在softmax分母中增加一个不可见键的分数。<bookmark mark='b'/>门控把注意力输出逐特征乘以输入的sigmoid。<bookmark mark='c'/>差分注意力减去两张softmax图。<bookmark mark='d'/>图中是训练时起始标记系数；差分系数有正负，不是概率。{v_sink}<bookmark mark='e'/>{v_gate}<bookmark mark='f'/>{v_diff}<bookmark mark='g'/>{v_loss}论文报告门控使首词元注意力从46.7%降至4.8%；Qwen3-Next与Kimi K3采用注意力门控。",
    '"A finite probe of context use: show our transformer a held-out stretch of a novel, twice in a row. <bookmark mark=\'a\'/> " + v1 + " <bookmark mark=\'b\'/> " + v2 + " <bookmark mark=\'c\'/> " + tail': "用一个有限探针检验上下文使用：把留出的小说片段连续展示两遍。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{tail}",
    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: this probe shows a large improvement from its own context.'": '第一遍每字符{m1:.2f}比特，第二遍{m2:.2f}比特：这个探针显示明显的上下文收益。',
    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: a little better, a modest improvement on this probe.'": '第一遍每字符{m1:.2f}比特，第二遍{m2:.2f}比特：这个探针显示较小的改进。',
    "f'The first time through, {m1:.2f} bits a character; the second time, {m2:.2f}: no better. The probe shows no mean second-copy improvement; it does not rule out every copying mechanism.'": '第一遍每字符{m1:.2f}比特，第二遍{m2:.2f}比特：该探针没有显示第二遍平均损失改进，不能排除所有复制机制。',
    "f'Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, {u26:.1f}; {q2:.1f} the second: this probe shows a second-copy improvement.'": '随机字母：第一遍{q1:.1f}比特，比26个字母均匀猜测的{u26:.1f}比特更差；第二遍{q2:.1f}比特，这个探针显示第二遍改进。',
    "f'Random letters: {q1:.1f} bits the first time, worse than a blind guess among 26 letters, {u26:.1f}; and {q2:.1f} the second: this probe shows no second-copy improvement.'": '随机字母：第一遍{q1:.1f}比特，比26个字母均匀猜测的{u26:.1f}比特更差；第二遍{q2:.1f}比特，未显示第二遍改进。',
    "f'Random letters: {q1:.1f} bits the first time, {q2:.1f} the second: this probe shows a second-copy improvement.'": '随机字母：第一遍{q1:.1f}比特，第二遍{q2:.1f}比特，显示第二遍改进。',
    "f'Random letters: {q1:.1f} bits the first time, and {q2:.1f} the second: this probe shows no second-copy improvement.'": '随机字母：第一遍{q1:.1f}比特，第二遍{q2:.1f}比特，未显示第二遍改进。',
    'One common copying motif is called an induction circuit.': '一种常见的复制结构叫作归纳回路。',
    'We can examine one common copying motif without concluding that this model lacks every copying mechanism.': '我们可以研究一种常见的复制结构，而不据此断言模型缺少一切复制机制。',
    "One common motif uses two heads, in two layers. <bookmark mark='a'/> In an earlier layer, a head that only looks one step back: each character's vector now also says which character came before it. <bookmark mark='b'/> In a later layer, the second head reads an 'l' and asks: which earlier character came right after an 'l'? The 'c' in Falcon answers, because its note says: the one before me was an 'l'. <bookmark mark='c'/> So the head copies it: 'c'. Seen A then B? On seeing A again, predict B. Catherine Olsson and colleagues at Anthropic named these induction heads in 2022.": "一种常见结构使用两层中的两个头。<bookmark mark='a'/>较早的头看向前一词元，把前一字符信息写入当前位置。<bookmark mark='b'/>较晚的头读到l，寻找前一字符为l的位置；Falcon中的c符合条件。<bookmark mark='c'/>这个示意回路于是复制c：见到A后接B，再见A时预测B。Olsson及同事在2022年研究了归纳头。",
    "f'In this one-layer run, after {int(c1[-1, 0]):,} steps the repeat loss is {f1:.1f} bits. This finite result is not an impossibility claim. '": '这次单层运行训练{int(c1[-1, 0]):,}步后，重复段损失为{f1:.1f}比特；有限运行不能证明架构不可能学会。',
    "f'The two-layer runs end at {lo2:.2f} to {hi2:.2f} bits. Their largest logged loss decrease is around step {js[0]:,}; losses are sampled every 100 steps. If no interval decreases, it selects the smallest increase; this is not a phase-transition test.'": '双层运行终点为{lo2:.2f}到{hi2:.2f}比特。最大记录损失下降位于第{js[0]:,}步附近；损失每100步记录一次。若没有下降区间，则标出最小上升；这不是相变检验。',
    "f'The two-layer runs end at {lo2:.2f} to {hi2:.2f} bits. Their largest logged loss decreases lie between steps {min(js):,} and {max(js):,} in {len(js)} runs; losses are sampled every 100 steps. If no interval decreases, the marker selects the smallest increase; these are not phase-transition tests.'": '双层运行终点为{lo2:.2f}到{hi2:.2f}比特。{len(js)}次运行的最大记录损失下降位于第{min(js):,}到{max(js):,}步之间；损失每100步记录一次，若没有下降区间则标出最小上升，标记不是相变检验。',
    'f"We inspect fixed probes during training, in a small attention-only model trained on random tokens with a repeated stretch inside. <bookmark mark=\'a\'/> {v1}<bookmark mark=\'b\'/> {v_jump} <bookmark mark=\'c\'/> These are selected first-seed maps: a previous-position probe and an earliest-prior-match-successor probe, not a causal intervention. The original head score averages attention on the successor of the earliest earlier matching token over masked repeat queries in 64 fixed examples, which can differ from the planted source. Final-score pair selection uses best-candidate fallback if none pass. These finite summaries do not prove a universal onset of learning from a prompt."': "在训练中观察固定探针：注意力小模型在带重复段的随机词元上训练。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v_jump}<bookmark mark='c'/>这里是第一种子的选定注意力图。原始头分数在64个固定样本的重复段查询上，平均取最早先前同词元之后位置的注意力权重，可能不同于植入的复制来源。按最终分数选头，无头达标时使用最佳候选。这不是因果干预，也不能证明提示学习具有普遍起点。",
    "f'The first head has a previous-position score that crosses its half-peak reference in this window, reaching {prev_sc[kb]:.2f} by step {steps[kb]:,}. '": '第一个头的前一位置分数在该窗口达到半峰值参考，到第{steps[kb]:,}步为{prev_sc[kb]:.2f}。',
    "f'The first head reaches its half-peak previous-position score earlier, by step {steps[kp]:,}. This ordering alone is not causal evidence. '": '第一个头更早达到前一位置分数的半峰值参考，在第{steps[kp]:,}步；这种先后次序不是因果证据。',
    "f'The first head reaches its half-peak previous-position score later, by step {steps[kp]:,}. '": '第一个头较晚达到前一位置分数的半峰值参考，在第{steps[kp]:,}步。',
    'f"Here are first-seed selected-head maps at checkpoints, beside repeat loss. <bookmark mark=\'a\'/> Watch the saved maps rather than assuming formation. <bookmark mark=\'b\'/> The largest logged loss-decrease marker is step {js:,}. If no interval decreases, that marker selects the smallest increase. A separately corrected display metric averages the known-copy stripe over queries 60 through 78: from {ind_sc[ka]:.2f} to {ind_sc[kb]:.2f} across {steps[kb] - steps[ka]} steps; repeat loss is {lo_a:.1f} then {lo_b:.1f} bits. " + together + \'This selected stripe window need not coincide with that marker, and association does not establish necessity or causation.\'': "这是第一种子在各检查点的选定头注意力图，旁边是重复段损失。<bookmark mark='a'/>查看保存的图，不预设头已经形成。<bookmark mark='b'/>最大记录损失下降标记在第{js:,}步。若没有下降区间则标出最小上升。另行修正的显示统计取查询60至78上的已知复制来源斜纹平均权重：在{steps[kb] - steps[ka]}步间从{ind_sc[ka]:.2f}到{ind_sc[kb]:.2f}，重复损失分别为{lo_a:.1f}和{lo_b:.1f}比特。{together}这个选定斜纹窗口不一定与损失标记重合；相关不能证明必要性或因果。",
    "f'For the {n_p} previous-token heads paired with the {n_i} induction heads, its matrix alignment changes from {k0:.2f} to {k1:.2f} over these checkpoints; Q-composition over the same pairs ends at {q1:.2f}, every other pair at {o1:.2f}. This is descriptive matrix alignment, not a copying probability or a causal test.'": '{n_p}个前一词元候选与{n_i}个归纳候选配对的矩阵对齐从{k0:.2f}变为{k1:.2f}；同一配对的Q组合终点{q1:.2f}，其他配对{o1:.2f}。这是描述性对齐，不是复制概率或因果检验。',
    "f'For the {n_p} previous-token heads paired with the {n_i} induction heads, it ends at {k1:.2f}, against {q1:.2f} for Q-composition and {o1:.2f} for every other pair: this descriptive contrast is not a causal test, and the signal is not cleanly in the keys.'": '{n_p}个前一词元候选与{n_i}个归纳候选配对的K组合终点{k1:.2f}，Q组合{q1:.2f}，其他配对{o1:.2f}。此描述性对比不是因果检验，也不显示只在键侧的清晰信号。',
    'f"The weights provide an alignment probe, not proof of cooperation. <bookmark mark=\'a\'/> K-composition, from Nelson Elhage and colleagues, measures how much a later head\'s keys read what an earlier head writes: the size of the product of its QK matrix and the earlier head\'s OV matrix, relative to their sizes. Two hundred Gaussian factorized-head draws have mean score about {base:.2f}. <bookmark mark=\'b\'/> {v}"': "权重提供对齐探针，不证明合作。<bookmark mark='a'/>K组合取后续QK与先前OV矩阵乘积的Frobenius范数，再除以两者范数。200次高斯分解随机头抽样的均值约为{base:.2f}；图带为抽样标准差，不是置信区间。<bookmark mark='b'/>{v}",
    'f"This finite probe finds a strong stripe: layer {li + 1}\'s head {hi + 1} puts {ind.max():.0%} of its attention, on average, on its known source-successor stripe, one step after the earlier copy. "': '这个有限探针显示强斜纹：第{li + 1}层头{hi + 1}平均把{ind.max():.0%}的注意力分给已知来源的后继位置。',
    'f"This finite probe shows no strong single-head stripe: its best candidate, layer {li + 1}\'s head {hi + 1}, puts {ind.max():.1%} of its attention one step after the earlier copy, and at the end the second copy costs {c2[-1]:.2f} bits a character, the first {c1[-1]:.2f}. "': '这个有限探针没有强单头斜纹：最佳候选第{li + 1}层头{hi + 1}的对应权重为{ind.max():.1%}；终点第二遍每字符{c2[-1]:.2f}比特，第一遍{c1[-1]:.2f}比特。',
    "f'Its heads compose a little, at most {top:.2f} against {base:.2f} for random heads, but matrix alignment alone cannot establish whether a pair has become a copying circuit. '": '最高矩阵对齐{top:.2f}，高斯参考均值{base:.2f}；仅凭对齐不能确定是否存在复制回路。',
    "f'Its maximum matrix alignment is near the Gaussian reference: at most {top:.2f}, against {base:.2f} for random heads. '": '最高矩阵对齐接近高斯参考：最大{top:.2f}，参考均值{base:.2f}。',
    'f"The training budget is {tokens / 1000000.0:.0f} million sampled character targets. Task distribution and budget are possible explanations, not tested causes. The toy\'s selected loss-change markers are no later than step {jmax:,}; these do not define an induction-onset threshold."': '训练预算为{tokens / 1000000.0:.0f}百万个采样字符目标。任务分布与预算只是可能解释，未经因果检验。玩具模型选定损失变化标记最晚在第{jmax:,}步；这些不是归纳形成阈值。',
    "f'The training budget is {tokens / 1000000.0:.0f} million sampled character targets. This probe does not rule out diffuse or alternative mechanisms; budget and task distribution are untested possible explanations.'": '训练预算为{tokens / 1000000.0:.0f}百万个采样字符目标。此探针不能排除分散或替代机制；预算和任务分布只是未经检验的可能解释。',
    '"And our own transformer, trained on novels with no copying game at all? Its matrix probe is pre-RoPE, folding in LayerNorm gain and centering but omitting input-dependent normalization and affine offsets; it is not an exact end-to-end circuit. <bookmark mark=\'a\'/> " + v1 + "<bookmark mark=\'b\'/> " + v2 + "<bookmark mark=\'c\'/> " + v3': "再看没有复制游戏的小说Transformer。矩阵探针位于RoPE之前，折入LayerNorm增益与去均值，却省略输入相关归一化和仿射偏移，不是精确的端到端回路。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}",
    "f'All {n_p} previous-position candidates paired with all {n_i} repeat-probe candidates select every pair. Their K-alignment changes from {k0:.2f} to {k1:.2f}; Q-alignment ends at {q1:.2f}. There is no other comparison group. These are descriptive matrix scores, not causal evidence.'": '全部{n_p}个前一位置候选与全部{n_i}个重复探针候选配对，选中了每个头对。K对齐从{k0:.2f}到{k1:.2f}，Q对齐终点为{q1:.2f}。没有其他比较组。这些只是描述性矩阵分数，不是因果证据。',
    'f"Now the experiment. Four small transformers, identical except for how they learn where each character is: sinusoids added to the input, rotary positions, ALiBi\'s linear penalty, and nothing at all. Here they are learning, replayed: held-out bits per character, step by step. <bookmark mark=\'a\'/> Each is trained on the novels for {c[\'steps\']:,} steps of {c[\'ctx\']}-character windows, with batches of 16, the same windows in the same order within each seed. Four heads per layer; three matched seeds. Checkpoint curves use 16 held-out prefix windows; final summaries use 48 full windows. Each run samples 2,048,000 target occurrences, not necessarily distinct corpus characters; the lines show seed means and bands the min-max range. This descriptive ordering uses display order to break ties. <bookmark mark=\'b\'/> {v_train}"': "比较四种位置方法：输入正弦、RoPE、ALiBi线性惩罚及无位置。图中是留出文本损失。<bookmark mark='a'/>每次运行训练{c['steps']:,}步，每步16个{c['ctx']}目标位置的窗口，同一种子内使用相同窗口顺序；每层4个头，三个配对种子。检查点曲线用16个留出前缀窗口，最终汇总用48个完整窗口。每次运行采样2,048,000个可重复的目标位置，不是不同语料字符数。线为种子均值，带为最小—最大范围；并列时用显示顺序排列。<bookmark mark='b'/>{v_train}",
    "f'{CAP[best]} has the lowest measured mean, at {vals[best].mean():.3f}, and every one of its seeds has lower loss than every seed of the others. '": '{CAP[best]}测得的均值最低，为{vals[best].mean():.3f}，它每个种子的损失都低于其他方法的每个种子；这只是这些有限运行的描述。',
    'f"The minimum mean, first in display order if tied, is {SPOKEN[best]}\'s, {vals[best].mean():.3f}, but at least one competing seed range overlaps. The differences here, up to {gap:.3f} bits, and the largest {spread:.3f} range within one design are descriptive summaries, not significance tests. "': '最低均值为{SPOKEN[best]}的{vals[best].mean():.3f}，并列时按显示顺序列出。至少一个竞争方法的种子范围与它重叠。最大均值差{gap:.3f}比特，最大单方法种子范围{spread:.3f}比特；两者只是描述性统计，不是显著性检验。',
    "f'No positions at all is first in display order among the measured means, at {nope_v:.3f}: loss alone does not identify its internal position signal.'": '无位置方法在测得均值的显示顺序中排第一，为{nope_v:.3f}；仅凭损失不能确定内部的位置表示。',
    "f'No positions at all has display rank {rank_word}, at {nope_v:.3f}, only {behind:.3f} behind: this does not establish which internal position signal it uses.'": '无位置方法的显示排名为{rank_word}，均值{nope_v:.3f}，比最小均值高{behind:.3f}；这不能确定它用了什么内部位置信号。',
    "f'No positions at all has display rank {rank_word}, at {nope_v:.3f}, {behind:.2f} bits behind the best: this does not identify an internal position signal.'": '无位置方法的显示排名为{rank_word}，均值{nope_v:.3f}，比最小均值高{behind:.2f}比特；这不能确定内部位置信号。',
    "f'In the below-0.15-bit display group, the largest far-minus-near change is {hr:.2f} bits: {n_held}.'": '低于0.15比特的展示组中，最大远端减近端差为{hr:.2f}比特：{n_held}。',
    "f'In the below-0.15-bit display group, the largest signed far-minus-near change is {hr:+.2f} bits: {n_held}.'": '低于0.15比特的展示组中，最大带符号远端减近端差为{hr:+.2f}比特：{n_held}。',
    "f'In the at-least-0.5-bit display group, the largest increase is {br:.1f} bits: {n_broke}.'": '至少0.5比特的展示组中，最大上升为{br:.1f}比特：{n_broke}。',
    'f"RoPE\'s far-minus-near change is {rise[\'rope\']:+.2f} bits in these windows; this loss comparison does not identify its cause. The next chapter tests several context-extension choices."': "这些窗口中，RoPE的远端减近端差为{rise['rope']:+.2f}比特；损失对比不能确定原因。下一章检验几种上下文扩展方法。",
    'f"Now read four times as far, {R} characters, though none of them saw more than {T}. <bookmark mark=\'a\'/> Bits per character at each position in 48 fixed windows, three seeds each; raw seed values are averaged before plotting. The below-0.15 and at-least-0.5 groups are display thresholds, not statistical tests. <bookmark mark=\'b\'/> {v_held} <bookmark mark=\'e\'/> {v_mid} <bookmark mark=\'f\'/> {v_broke} <bookmark mark=\'d\'/> {rope_txt}"': "现在读到{R}个字符，是训练长度{T}的四倍。<bookmark mark='a'/>48个固定窗口、每种三个种子的各位置损失；先对原始种子数值求均值，再画图。低于0.15和至少0.5比特只是展示分组阈值，不是统计检验。<bookmark mark='b'/>{v_held}<bookmark mark='e'/>{v_mid}<bookmark mark='f'/>{v_broke}<bookmark mark='d'/>{rope_txt}",
    'f"These are two extrapolation illustrations, not inferred mechanisms. <bookmark mark=\'a\'/> ALiBi subtracts distance penalties, with slopes {m[0]:.2f} to {m[-1]:.4f}. At distance {T}, they cost {c0:.0f} and {c3:.1f} for the steepest and shallowest head. <bookmark mark=\'b\'/> Beyond training, those penalties grow; content scores can still outweigh them. <bookmark mark=\'c\'/> The other plot assumes an explicitly marked first token and uniform attention: its share is one over t, reaching {ratio:.2f} of the training-edge share at position {R}. Our NoPE training inserts no such marker, so this plot does not show the signal it learned. <bookmark mark=\'d\'/> Sinusoidal and rotary coordinates also change outside the sampled training support; these illustrations do not establish which effect causes any measured loss change."': "这是两个外推示意，不是反推出的内部机制。<bookmark mark='a'/>ALiBi斜率从{m[0]:.2f}到{m[-1]:.4f}；距离{T}时，最陡和最缓的头分别扣{c0:.0f}和{c3:.1f}分。<bookmark mark='b'/>训练范围外惩罚继续增长，但内容分数仍可抵消它。<bookmark mark='c'/>另一张图假设第一个词元有明确标记且注意力均匀，份额为1/t；到位置{R}，为训练边缘份额的{ratio:.2f}倍。我们的NoPE训练没有插入这样的标记，因此图不能说明它实际学到的信号。<bookmark mark='d'/>正弦和RoPE坐标在采样训练范围外也会改变；这些示意不能确定任何测得损失变化的原因。",
    'f"Our model was trained on stretches of {ctx} characters. Compare {s} times that length using 32 fixed windows and the same next-character targets for every method. <bookmark mark=\'a\'/> The first quarter averages {near:.1f} bits a character. <bookmark mark=\'b\'/> The far quarter averages {far:.1f}; this comparison alone does not identify a cause. <bookmark mark=\'c\'/> The gray baseline predicts those same targets using at most the last {ctx} input characters, resetting the input window for later targets."': "模型在{ctx}字符窗口上训练。用32个固定窗口比较{s}倍长度，各方法预测完全相同的下一字符目标。<bookmark mark='a'/>前四分之一平均每字符{near:.1f}比特。<bookmark mark='b'/>最远四分之一为{far:.1f}；对比本身不能确定原因。<bookmark mark='c'/>灰色基线对同一批目标最多使用最近{ctx}个输入字符，并为后面的目标重置输入窗口。",
    ', with no assumed superiority to the same-target window baseline.': '；这里不预设它优于同目标的窗口基线。',
    "f', compared with {w_far:.2f} for the same-target {ctx}-character window.'": '，同目标的{ctx}字符窗口基线为{w_far:.2f}。',
    'f"So people rescale the clocks. <bookmark mark=\'a\'/> Position interpolation slows every hand by the same factor, {s}, compressing position coordinates into the training span; fractional positions were not literally all sampled in training. <bookmark mark=\'b\'/> The NTK-aware trick, named after part twelve\'s neural tangent kernel, slows the slow hands a lot and the fast ones hardly at all. <bookmark mark=\'c\'/> YaRN leaves high-turn pairs alone, slows low-turn pairs fully, ramps in between, and uses a static score multiplier. <bookmark mark=\'d\'/> On our model, with no retraining, the lowest measured far-end value among these rescalings, using display order for ties, is {names[best]}: {b[best]:.2f} bits at the far end, against {b[\'plain\']:.1f} for doing nothing" + win_txt + \' Qwen2.5 uses YaRN with dual-chunk attention, and DeepSeek-V3 uses its own YaRN configuration, to reach a hundred and twenty-eight thousand tokens with YaRN.\'': "接着重缩放位置。<bookmark mark='a'/>位置插值统一减慢{s}倍，把位置坐标压入训练跨度；不意味着每个分数位置都曾被采样。<bookmark mark='b'/>这里的静态NTK缩放主要减慢低频对，高频对变化较小；并非完整复现Qwen的动态方案。<bookmark mark='c'/>YaRN保留高转数对，完全缩放低转数对，中间渐变，并使用静态分数乘数。<bookmark mark='d'/>本次无额外训练的最远端对比中，重缩放方法最低的测得值为{names[best]}的{b[best]:.2f}比特，未缩放为{b['plain']:.1f}比特；并列按显示顺序处理{win_txt}Qwen2.5结合YaRN和双分块注意力，DeepSeek-V3采用自己的YaRN配置，达到128K词元。",
    'f"Here is the static YaRN configuration tested here; its thresholds and multiplier are model-dependent choices. <bookmark mark=\'a\'/> For each pair, count the full turns its hand makes over the training context: r, the context length over the pair\'s wavelength. <bookmark mark=\'b\'/> Our fastest pair turns about {r[0]:.0f} times in {ctx} characters; the high-turn rule leaves it alone. <bookmark mark=\'c\'/> The slowest pairs never finish a turn, so YaRN slows them by the full factor of {s}. <bookmark mark=\'d\'/> In between is a ramp, gamma: zero below one turn, one above thirty-two. <bookmark mark=\'e\'/> Each new angle blends the slowed angle and the original by gamma. In our heads, {kept} kept, {len(ramp_i)} on the ramp and {slowed} slowed fully. <bookmark mark=\'f\'/> The paper proposes an empirically chosen score multiplier: multiply every score by zero point one log s plus one, squared: for s of {s}, {mult:.2f}."': "这里检验静态YaRN配置，阈值和乘数是与模型有关的选择。<bookmark mark='a'/>每对在训练跨度中的转数为r，即长度除以波长。<bookmark mark='b'/>最快的一对在{ctx}个位置转约{r[0]:.0f}圈，按高转数规则保持不变；这不意味着连续的每个角度都被采样。<bookmark mark='c'/>低转数对按{s}倍完全减慢。<bookmark mark='d'/>中间使用gamma渐变：低于1圈为0，高于32圈为1。<bookmark mark='e'/>新频率按gamma混合缩放与原始频率；这里{kept}对保留，{len(ramp_i)}对渐变，{slowed}对完全减慢。<bookmark mark='f'/>论文建议经验性的分数乘数：0.1lns加1的平方；s为{s}时是{mult:.2f}。",
    'f"On our model, scaling alone reports {far[\'plain\']:.2f} to {far[\'logn\']:.2f} bits. This does not identify which mechanism limits performance. "': "仅缩放分数时，最远端为{far['plain']:.2f}和{far['logn']:.2f}比特；这不能确定什么机制限制了表现。",
    'f"On top of the NTK rescaling the measured values are {far[\'ntk\']:.2f} to {far[\'ntk_logn\']:.2f}. "': "加在NTK缩放之上，测得值为{far['ntk']:.2f}和{far['ntk_logn']:.2f}。",
    'f"A longer text also has more keys to share the weights. <bookmark mark=\'a\'/> Say the best key scores delta above n minus one others: its weight is e to the delta over e to the delta plus n minus one. <bookmark mark=\'b\'/> For fixed weight strictly between zero and one, the exact margin is ln of n minus one plus a constant. At large n this is approximately ln n plus that constant. <bookmark mark=\'c\'/> We test a log-length score multiplier, unchanged through the training length. In this equal-other-scores illustration it counters dilution, but for a learned score distribution it does not guarantee fixed sharpness or entropy. David Chiang and Peter Cholak proposed it in 2022; Qwen and Llama 4 use versions of it. <bookmark mark=\'d\'/> {v1}<bookmark mark=\'e\'/> {v2}The lowest measured far-end value in this comparison, with display order breaking ties, is {SPOKEN_EXT[best]}, at {far[best]:.2f}."': "更长文本有更多键分配权重。<bookmark mark='a'/>在其余n−1个键分数相同的示意中，最佳键高出delta，权重为exp(delta)除以exp(delta)加n−1。<bookmark mark='b'/>固定0与1之间的目标权重时，精确裕量为ln(n−1)加常数；大n时近似lnn加常数。<bookmark mark='c'/>这里检验训练长度内不变、之后增加的对数长度分数乘数。在此示意中它抵消稀释，但不保证真实分数分布的锐度或熵不变。Chiang和Cholak在2022年研究过对数缩放，Qwen和Llama4采用相关变体。<bookmark mark='d'/>{v1}<bookmark mark='e'/>{v2}本次比较中最远端测得最低的为{SPOKEN_EXT[best]}，{far[best]:.2f}；并列按显示顺序处理。",
    'f"Position interpolation reports {far[\'pi\']:.2f} before and {far[\'ft_pi\']:.2f} bits after at the far end; YaRN reports {far[\'yarn\']:.2f} before and {far[\'ft_yarn\']:.2f} after."': "最远端，位置插值训练前后分别为{far['pi']:.2f}和{far['ft_pi']:.2f}比特；YaRN分别为{far['yarn']:.2f}和{far['ft_yarn']:.2f}比特。",
    'f"The tuned methods differ by {gap:.2f} bits at the far end; the last-{ctx}-character baseline is {far[\'window\']:.2f}. This finite comparison does not establish a universal winner."': "两种微调方法的最远端差为{gap:.2f}比特；最近{ctx}字符基线为{far['window']:.2f}比特。有限对比不能确定普遍赢家。",
    'f"Each rescaling starts from the same saved model. Per run, {steps} updates of {int(e[\'ft_batch\'])} windows of {T:,} characters: {chars:,} sampled next-character targets, about {100 * chars / float(t[\'tokens\']):.0f} percent of the original sampled-target budget, from position interpolation and from YaRN; in the corner, their training loss. <bookmark mark=\'a\'/> Dashed, before; solid, after. <bookmark mark=\'b\'/> {v} <bookmark mark=\'c\'/> {v_end} DeepSeek-V3 went from four thousand to a hundred and twenty-eight thousand tokens this way, with two thousand steps."': "每种缩放都从同一个保存模型出发。每次运行更新{steps}步，每步{int(e['ft_batch'])}个{T:,}字符窗口，共{chars:,}个采样下一字符目标，约为原始采样目标预算的百分之{100 * chars / float(t['tokens']):.0f}。分别从位置插值与YaRN出发；角落显示训练损失。<bookmark mark='a'/>虚线为训练前，实线为训练后。<bookmark mark='b'/>{v}<bookmark mark='c'/>{v_end}DeepSeek-V3采用自己的配置，通过4K到32K再到128K的两个阶段，各1000步完成扩展，不能与这里的小字符模型视为同一实验。",
    'Different masks reveal the main information flows in these transformer families.': "不同的掩码揭示了这些Transformer家族中的主要信息流。<bookmark mark='a'/>编码器让每个位置都能看到其他所有位置。这种全注意力掩码本身不保证下一词元训练的因果约束；编码器模型也可以用掩码预测或迭代过程生成。<bookmark mark='b'/>解码器用的是因果三角：它写，一次一个词元。<bookmark mark='c'/>2017年那篇论文的翻译模型两样都有。它的解码器看自己的过去，还通过交叉注意力看整个源句：查询来自译文，键和值来自编码器对原文的阅读。<bookmark mark='d'/>前缀语言模型双向读它的提示，再从左到右写出其余部分。这几种谁胜出了、为什么，是第14部分的故事。",
    'Many models in 2026 still compute this formula somewhere.': "2026年的许多模型，仍然在某处计算着这个公式。变的是在哪里算，以及算多少。<bookmark mark='a'/>在注意力模块内部，是前面几章的那些修补：汇点logit、输出门控、QK归一化，还有完全没有位置的层。<bookmark mark='b'/>每个过去的词元留下的键和值，已经被压小了：在多个头之间共享，或者从一个小的潜在向量重建出来，这是把第4章的低秩想法用在了记忆上。<bookmark mark='c'/>许多模型只看过去的一部分：一个滑动窗口，或者一个又小又快的索引器，为每个查询挑出几千个过去的词元。<bookmark mark='d'/>还有些模型把大多数注意力层，换成一个边读边更新的固定大小的记忆：在Qwen3-Next和Qwen3.5里，每一个注意力层配三个这样的层。",
    "f'It reports {pb:.2f} bits a character over": '它在测试段落的21376个目标位置上报告每字符{pb:.2f}比特。检查点验证曲线使用验证文本前6万个源字符，最终验证报告使用前40万个源字符。这些原始测量与历史上的计数模型和神经模型所用的目标位置不同，不能据此给模型排名。',
    'The large models of Part 1 also stack attention blocks': '第1部分的大模型也把注意力模块叠起来，但训练数据、位置设计、计算预算和评分覆盖范围不同。这些报告没有单独确定规模的影响。',
    "Here are the same observations used in Part 7: occurrences of 'her' per thousand-word block of Great Expectations. This is a new normalized Gaussian kernel smoother, not the Gaussian-process posterior. Suppose we query zero-based block index one hundred and twenty. <bookmark mark='a'/> Average the observed block values with distance-based weights centered on that query. <bookmark mark='b'/> Nearby blocks receive more weight; distant Gaussian weights can be negligible, though mathematically positive. The normalized weights sum to one. Bar heights are rescaled relative to their peak, and tiny bars are omitted: they are not literal probabilities on this strip. <bookmark mark='c'/> Moving the query traces the Nadaraya-Watson estimate.": "这里复用第7部分的观测：远大前程每千词文本块中her的出现次数。现在画的是重新计算的归一化高斯核平滑估计，不是高斯过程后验。查询从零计数的第120号文本块。<bookmark mark='a'/>按与查询的距离给观测值加权平均。<bookmark mark='b'/>近处权重大，远处高斯权重可以微乎其微，但数学上为正；归一化权重之和为1。条形高度相对峰值缩放，并省略很小的条，不是此条带上的实际概率刻度。<bookmark mark='c'/>移动查询便得到Nadaraya—Watson估计。",
    'f"These three illustrations use bandwidths {hs[0]:g}, {hs[1]:g}, and {hs[2]:g} blocks; they are not a claimed optimum. <bookmark mark=\'a\'/> A narrow bandwidth can follow local variation. <bookmark mark=\'b\'/> A wider finite bandwidth smooths more broadly; in the infinite-width limit, every observed block receives equal weight and the estimate approaches the global average. Separately, the original computation compares 40 bandwidths from 0.4 to 30 by leave-one-out mean squared error, excluding the held-out observation itself. That is different from Part 7\'s Gaussian-process marginal-likelihood selection."': "这三个示例的带宽为{hs[0]:g}、{hs[1]:g}和{hs[2]:g}个文本块，不声称其中哪一个最优。<bookmark mark='a'/>较窄带宽可跟随局部变化。<bookmark mark='b'/>较宽的有限带宽在更大范围平滑，带宽趋于无穷时，每个观测文本块的权重趋于相同，估计趋于全局平均。原计算另行用留一均方误差比较0.4到30之间的40个带宽，排除被留出的观测；这与第7部分高斯过程的边际似然选择不同。",
    "Write it down. The guess at the query is a sum over the blocks: each block's value, times a weight. The weight is a softmax of a score: the exponential of the score, divided by the total, so the weights are positive and add up to one. Here the score is minus the squared distance divided by twice the bandwidth squared. <bookmark mark='a'/> Now deliberately change the scoring rule. Expanding a vector RBF score gives a dot product plus key-norm and query-norm terms. The query-norm term cancels within a softmax row; dot-only equivalence at matching scale needs equal key norms, otherwise a key-norm bias remains. Instead, learn the affinity between two vectors: a query and a key. <bookmark mark='b'/> That's attention, the heart of the transformer. The query asks what am I looking for; each key says what it offers; each value is what it passes on. <bookmark mark='c'/> And all three are computed from the characters by matrices the network learns. This softmax head has the normalized weighted-average form of a kernel smoother. Learned query-key affinities need not be a symmetric positive-semidefinite Gaussian-process covariance kernel.": "写成公式：查询处的估计为各观测值的加权和，权重是分数指数除以指数总和，因此为正且和为1。此处分数为负平方距离除以带宽平方的两倍。<bookmark mark='a'/>接着有意改变评分规则。向量RBF分数展开为点积、键范数项和查询范数项。每行softmax会消去查询范数项；在尺度匹配时，还需键范数相同才能只保留点积，否则必须保留键范数偏置。这里改为学习查询与键之间的相似度。<bookmark mark='b'/>这就是Transformer的softmax注意力：查询表示寻找什么，键表示提供什么，值表示传递什么。<bookmark mark='c'/>三者由学习到的矩阵计算。这个头具有核平滑器的归一化加权平均形式；学到的查询—键相似度不一定是对称半正定的高斯过程协方差核。",
    "Here is the softmax-attention definition used here. <bookmark mark='a'/> Attention scores each key against the query with a dot product divided by the square root of d, turns the scores into weights with a softmax, and returns the weighted average of the values. <bookmark mark='b'/> In 2014, Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio let a neural translation network look back at its source sentence, as in Part 10; in 2017 attention replaced recurrent sequence mixing, alongside feed-forward sublayers. <bookmark mark='c'/> A question: if every key is the same, what does attention return? <bookmark mark='d'/> Every weight is one over n: the plain average of the values. This softmax readout can only weigh and blend what it is given.": "这是这里使用的softmax注意力定义。<bookmark mark='a'/>用查询与键的点积除以维度平方根评分，再经softmax得到权重，对值加权平均。<bookmark mark='b'/>2014年Bahdanau、Cho和Bengio让翻译网络回看源句，见第10部分；2017年注意力替代了循环式序列混合，同时仍有前馈子层。<bookmark mark='c'/>如果所有键相同，返回什么？<bookmark mark='d'/>每个权重都是1/n，返回值的普通平均。这个softmax读出只能加权混合给定的值。",
    "Here is an unscaled dot-product illustration; the earlier definition includes the square-root scale. Every key is an arrow; so is the query. <bookmark mark='a'/> The score of a key is its dot product with the query: how long both are, times how much they point the same way. The softmax turns the scores into weights. <bookmark mark='b'/> Turn the query, and the weights flow from key to key. A query is a direction to look in. Next, the same formula read another way: as a memory that reads stored values.": "这里是不除以维度平方根的点积示意，前面的定义包含该缩放。键和查询都是向量箭头。<bookmark mark='a'/>点积等于两者长度乘夹角余弦，softmax把分数变成权重。<bookmark mark='b'/>转动查询，权重便在不同键之间变化。接下来把同一加权公式看作读取存储值的记忆。",
    'f"Let\'s take stock. Softmax attention has a normalized weighted-average form related to Nadaraya-Watson smoothing, with learned affinities, and connects to modern Hopfield memory reads; the recall thumbnail uses a sign readout. Dividing by the square root of d controls initial score variance under independent-component assumptions; learned scores can still saturate. Heads compare and move along a few directions, the mask decides who sees whom, and our block has twelve d squared plus nine d parameters: bias-free QKVO, a biased four-d-width MLP and two affine LayerNorms. Its matrix-multiply work grows with context; that count omits vocabulary projection and elementwise arithmetic. Our transformer reached {float(t[\'passage_bits\']):.2f} bits a character over its 21,376 scored passage targets. Positions can be added, rotated, penalized or left out, and stretched with care. A sink logit changes the softmax denominator with a null option; an output gate attenuates the weighted write. These act at different stages. Probes investigate copying and gradient-step-like maps, and we hand-compile programs, within limits. More layers, recurrence, or generated steps can relax some depth limits."': "回顾一下：softmax注意力是归一化加权平均，与Nadaraya—Watson平滑及现代Hopfield记忆读取相联系；容量缩略图使用符号读出。除以维度平方根控制独立分量假设下的初始分数方差，不能保证学到的分数不饱和。头在少数方向比较和搬运，掩码规定可见性。我们的无偏置QKVO、带偏置4d宽MLP和两个仿射LayerNorm块，有12d平方加9d个参数；矩阵乘法工作量随上下文增长，该计数不含词表投影和逐元素算术。Transformer在21,376个计分目标上达到每字符{float(t['passage_bits']):.2f}比特。位置可相加、旋转、惩罚或省略，扩展需谨慎。汇点logit通过空选项改变softmax分母，输出门控则减弱加权写入，两者作用位置不同。探针研究复制和类似梯度步的映射，我们也手工编译程序，各有范围限制。更多层、递归或生成步骤可以放宽某些深度限制。",
}

PHRASES = {
    # Hopfield
    'but it never fails completely.': '但它从来不会彻底失败。',
    # Heads
    'That is close to the whole stream.': '这几乎就是整个残差流。',
    # Masks
    'exactly zero': '精确的0',
    'rounding error': '舍入误差级别',
    'blind to order, to rounding error.': '对顺序完全视而不见，差别只在舍入误差的量级。',
    # Cost
    'They match the formula exactly.': '它们和公式完全吻合。',
    # Longer
    '.': '。',
    'position interpolation': '位置插值',
    'the NTK-aware rescaling': 'NTK感知的缩放',
    'the plain model': '原始模型',
    'log n scaling alone': '单独的log n缩放',
    'NTK-aware with log n scaling': 'NTK感知缩放加上log n缩放',
    # SideBySide: names, and every list of them a verdict can splice in
    'Sinusoids': '正弦位置',
    'No positions at all': '不给位置的模型',
    'second': '第二',
    'third': '第三',
    'last': '最后',
    # Sinks
    'a space, an e or a t': '空格、e或t',
    'the plain softmax': '普通的softmax',
    'the sink logit': '汇点logit',
    'the gated head': '加了门控的头',
    'differential attention': '差分注意力',
    'That sum is close to full rank.': '这个和的秩接近满秩。',
}


def _spoken_lists():
    """Every list of position methods SideBySide can name ("sinusoids, RoPE and ALiBi"), in its order."""
    from itertools import combinations
    en = {"sin": "sinusoids", "rope": "RoPE", "alibi": "ALiBi", "nope": "no positions at all"}
    zh = {"sin": "正弦位置", "rope": "RoPE", "alibi": "ALiBi", "nope": "不给位置的模型"}
    order = ("sin", "rope", "alibi", "nope")
    out = {}
    for k in range(1, 5):
        for ms in combinations(order, k):
            e = [en[m] for m in ms]
            z = [zh[m] for m in ms]
            out[e[0] if k == 1 else ", ".join(e[:-1]) + " and " + e[-1]] = z[0] if k == 1 else "、".join(z[:-1]) + "和" + z[-1]
    return out


PHRASES.update(_spoken_lists())
