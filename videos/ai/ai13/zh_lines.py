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
        "这是一个正在阅读的Transformer。它是我们自己的：我们用本系列的30部小说训练了它，现在它读的，是记分牌测试段落里的一句话，这句话它从没见过。<bookmark mark='a'/>为了猜出下一个字符，每个字符都会回头看看它前面的那些字符，再决定每一个有多要紧。弧线越粗，它看得越多。<bookmark mark='b'/>这样回头一看，就叫作注意力；今天每一个大语言模型的引擎，就是它。",

    'f"Our model has {L * H} of these looks':
        "我们的模型有{L * H}个这样的“目光”，叫作“头”，每个头都用自己的方式掂量过去：这里是全部{L * H}个头，读的是同一句话。<bookmark mark='a'/>这一部分讲的，就是这一看背后的数学：它算的是什么，它怎样知道东西在哪里，以及它能学会做些什么。",

    'The idea is older than it looks: in 1964':
        "这个想法比它看起来要古老：1964年，是邻居的加权平均；<bookmark mark='a'/>1982年，是霍普菲尔德那个会回想的记忆；<bookmark mark='b'/>2014年，是一个学会了该看哪里的翻译模型，<bookmark mark='c'/>而到了2017年，是一个只靠这种“看”的网络。<bookmark mark='d'/>接着有了更好的位置表示，<bookmark mark='e'/>会复制的头和快速的计算内核，<bookmark mark='f'/>注意力汇点和更长的上下文，<bookmark mark='g'/>更小的记忆，<bookmark mark='h'/>稀疏注意力和门控注意力，<bookmark mark='i'/>到了2026年，有些模型只在四分之一的层里保留完整的注意力。",

    "This is Part 13 of AI, Built":
        "这是《人工智能，从零搭建》的第13部分，也是第三幕的开始：Transformer时代。<bookmark mark='a'/>本部分讲：注意力算的是什么，它既是平均，也是记忆；头、掩码和计算成本；我们自己的Transformer，训练它，再回放它的训练过程；告诉它东西在哪里的四种方法，以及怎样把它们拉长；今天的softmax内部的种种修补；还有，头能学会做什么，又做不到什么。",

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
        "下面是本部分接下来一直要用的定义。<bookmark mark='a'/>注意力用点积给每个键和查询打分，再除以根号d，用softmax把分数变成权重，最后返回这些值的加权平均。<bookmark mark='b'/>它在2014年进入神经网络：德米特里·巴赫达瑙、赵京焕和约书亚·本吉奥让一个翻译网络回头去看它的源句子，就像第10部分那样；到了2017年，它成了整个网络。<bookmark mark='c'/>问一个问题：如果每个键都一样，注意力会返回什么？<bookmark mark='d'/>每个权重都是n分之1：结果就是这些值的普通平均。注意力只能对它拿到的东西加权、混合。",

    "Here's the geometry. Every key is an arrow":
        "来看看其中的几何。每个键都是一根箭头；查询也是。<bookmark mark='a'/>一个键的分数，就是它和查询的点积：两者各有多长，再乘以它们的方向有多一致。softmax把这些分数变成权重。<bookmark mark='b'/>转动查询，权重就从一个键流向另一个键。查询，就是一个要去看的方向。接下来，换个角度读同一个公式：把它看成一个能回想起所存内容的记忆。",

    # ------------------------------------------------------------------ Hopfield
    "Chapter two. A memory that recalls.":
        "第2章。会回想的记忆。",

    'f"In 1982 the physicist John Hopfield':
        "1982年，物理学家约翰·霍普菲尔德描述了一个会记忆的网络。<bookmark mark='a'/>要存入一些由正1和负1组成的模式，就把每一对同时亮起的单元之间的连接加强：这是第9部分的赫布规则。<bookmark mark='b'/>回想时，从一个线索出发，让每个单元取其他单元加权投票结果的符号。<bookmark mark='c'/>每翻转一次，能量只会降低，所以回想就是一路滚下坡，如果一切顺利，就滚进最近的那个存储模式。<bookmark mark='d'/>这里我们存入{n}个字母，每个字母100个单元。<bookmark mark='e'/>给它一个四分之一像素被翻转的字母，让它自己稳定下来。{verdict}",

    "f'It recovers {ok} of the {n} letters":
        "{n}个字母里，它准确地恢复了{ok}个。其余的都落进了混合态：我们的字母共用的像素太多，它们的记忆互相串到了一起。",

    "f'It recovers all {n} letters":
        "全部{n}个字母，它都准确地恢复了，每个像素都回到了原位。",

    'f"How much can it hold?':
        "它能存多少？在100个单元里存入越来越多的随机模式，每个都用一个翻转了15%单元的线索来测试。<bookmark mark='a'/>经典网络存到{h_at}个模式时，能回想起来的就不到一半了，{none_txt}物理学家在1985年算出了它的极限：每个单元大约0.138个模式。每存入一个模式，都会给其他每个模式的投票添一点噪声，噪声越积越多。<bookmark mark='b'/>2016年，德米特里·克罗托夫和约翰·霍普菲尔德把能量变得更陡，让最近的那个模式以大得多的优势胜出；2017年，又有一个团队证明，指数形式的能量能存下指数多个模式。<bookmark mark='c'/>{tail}",

    "f'and by {int(dead)} it recalls none":
        "到{int(dead)}个时，就一个也回想不起来了。",

    "f'Store {int(Ms[-1])} patterns":
        "存入{int(Ms[-1])}个模式，是单元数的{Ms[-1] / N:.1f}倍，一步softmax仍然能把每一个都回想起来。",

    "f'It holds on far longer":
        "它撑得久得多：存到{int(Ms[-1])}个模式时，它仍然能回想起{md[-1]:.0%}。",

    'f"In 2020 Hubert Ramsauer':
        "2020年，胡贝特·拉姆绍尔、塞普·霍赫赖特和同事们把状态变成了连续的。<bookmark mark='a'/>能量变成：与各个存储模式重叠度的log-sum-exp取负，再加上一个让状态保持有界的小项。<bookmark mark='b'/>一步一步地把它最小化，更新规则就是：按每个存储模式与当前状态重叠度的softmax给它加权，再把它们加起来。<bookmark mark='c'/>看看这个公式。它就是注意力。线索是查询，存储的模式既是键也是值，而β扮演的就是根号d分之1的角色。<bookmark mark='d'/>在我们的字母上，一步就回想起了{n}个里的{ok_m}个。<bookmark mark='e'/>他们还证明了，通常一步就够了。论文的标题是：《Hopfield Networks is All You Need》，霍普菲尔德网络就是你所需要的一切。",

    'f"Beta, the inverse temperature':
        "β，也就是逆温度，是把这个记忆变成第1章那个平滑器的旋钮。<bookmark mark='a'/>把它调低，权重就摊到每一个模式上：结果是所有东西的平均，和被提示的那个模式的重叠度只有{small:.2f}。<bookmark mark='b'/>调到中间，它会把几个相似的模式平均起来，拉姆绍尔的团队把这种混合叫作亚稳态。<bookmark mark='c'/>把它调高，一个模式就拿走全部权重：重叠度是{big:.2f}。注意力就生活在这条曲线上，而除以根号d决定了它落在哪里。<bookmark mark='d'/>2024年的诺贝尔物理学奖，颁给了霍普菲尔德和杰弗里·辛顿，表彰的正是这类网络；第20部分会回到它们的能量，把它当作一种生成的方法。一个Transformer的头，就是一次记忆读取：它的查询在键里回想，返回值的一个混合。",

    # ------------------------------------------------------------------ Scale
    "Chapter three. Why divide by the square root of d.":
        "第3章。为什么要除以根号d。",

    'f"Take a query and a key whose d numbers':
        "取一个查询和一个键，它们各自的d个数相互独立，均值为0，方差为1，大致就是一个刚初始化的网络给出的样子。<bookmark mark='a'/>量一量它们的点积散得有多开：d等于{ds[0]}时是{sd[0]:.1f}，d等于{ds[-1]}时是{sd[-1]:.0f}。它随着向量的大小而增长。为什么？<bookmark mark='b'/>点积是d个乘积的和。<bookmark mark='c'/>每个乘积的均值都是0，因为它的两个因子相互独立。<bookmark mark='d'/>方差是1：独立的数相乘，乘积平方的期望，等于它们各自平方的期望相乘。<bookmark mark='e'/>独立的项，方差相加，所以点积的方差是d：它的散布像根号d那样增长。<bookmark mark='f'/>除以根号d，方差就回到1，不管向量多大：实测在{sds.min():.2f}到{sds.max():.2f}之间。",

    'f"Why does the spread matter?':
        "散布为什么要紧？因为softmax会把分数之间的差，变成权重之间的比，而且是指数式的。<bookmark mark='a'/>喂给它像根号d那样散开的分数，它就不再取平均了：它只挑出一个键，其余的全都不管。在{n}个键上，权重的熵，也就是衡量有多少个键在分享权重的量，从d等于{ds[0]}时的{raw[0]:.1f}比特，降到了d等于{ds[-1]}时的{raw[-1]:.2f}比特。<bookmark mark='b'/>除以根号d之后，权重始终是摊开的，不管多大都至少有{scl.min():.1f}比特，只比完全平均分配的{mx:.0f}比特少一点。",

    'f"There is a second cost, and it is worse.':
        "还有第二个代价，而且更糟。训练靠梯度来移动分数，而梯度要穿过softmax的导数。<bookmark mark='a'/>权重i对分数j的导数，等于p i乘以括号里的δ i j减p j。<bookmark mark='b'/>当一个权重接近1、其余都接近0时，每一项都有一个接近0的因子：softmax饱和了，分数也就学不动了。<bookmark mark='c'/>权重对分数的响应有多强，在分数散布大约为{sig[pk]:.0f}时达到峰值，往两边都会下降。<bookmark mark='d'/>缩放过的分数，散布为1，响应是{j1:.2f}。不缩放时，在d等于{ds[-1]}处，响应只有{jr:.2f}，而且向量越大，它还会继续下降。这就是瓦斯瓦尼和同事们在2017年给出的理由。后来，杨格的μP主张在极宽的网络里改成除以d；失控的分数会在第13章再次出现。",

    # ------------------------------------------------------------------ Heads
    "Chapter four. Heads are low-rank maps.":
        "第4章。头是低秩映射。",

    'f"Let\'s write one head as matrices.':
        "把一个头写成矩阵。字符i的查询，是W Q乘以它在残差流里的向量；字符j的键，是W K乘以它的向量。<bookmark mark='a'/>把转置移进去，<bookmark mark='b'/>分数就是x i，乘以一个矩阵，再乘以x j：一个{d}乘{d}的矩阵W Q K，用来比较残差流里的两个位置。<bookmark mark='c'/>但它是一个又高又瘦的{d}乘{dh}矩阵，和一个又矮又宽的矩阵的乘积，所以它的秩至多是{dh}。一个头只能沿着残差流的{dh}个方向做比较。<bookmark mark='d'/>头搬运的东西也一样：W O乘以W V，秩同样至多是{dh}。纳尔逊·埃尔哈格、克里斯·奥拉和同事们把它们叫作QK回路和OV回路：一个决定看哪里，另一个决定搬什么。",

    'f"Here are the singular values of W Q K':
        "这是我们Transformer全部{L * H}个头的W Q K奇异值，从大到小，画在对数坐标上。<bookmark mark='a'/>其中恰好有{rank}个是真的；之后的值断崖式下跌，跌到计算机舍入误差的大小。<bookmark mark='b'/>即便在这{dh}个方向里，一个头也很偏：{int(k90.min())}到{int(k90.max())}个方向，就占了它九成的大小。<bookmark mark='c'/>把一层的{H}个头加在一起，秩是{lrank}。<bookmark mark='d'/>{ln_txt}这些头合在一起覆盖了整个残差流，但每一个都只是透过一条窄缝在看。",

    "f'That is every direction but one":
        "也就是除了一个方向之外的所有方向，少掉的那个是{d}个数的平均值，层归一化在任何头看到它之前就把它去掉了。",

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
        "语言模型根据前面的字符猜每一个字符，所以注意力决不能看到未来。<bookmark mark='a'/>这是一张分数表：每个查询一行，每个键一列。<bookmark mark='b'/>给对角线以上的每个分数加上负无穷。负无穷的指数是0，所以softmax完全不给未来任何权重。这就是因果掩码。<bookmark mark='c'/>它带来的好处，是训练的速度。在{n}个字符上走一遍，就同时做出{n}个猜测，每一个都只用到它自己的过去，所以每个位置都是一个训练样本。<bookmark mark='d'/>在我们的Transformer上检验一下：改动一段文字的后半部分，它对前半部分猜测的改变是{past_txt}，而对后半部分的猜测改变最多达到{mf:.1f}。去掉掩码，前半部分就改变了{nm:.1f}：模型等于在偷看答案。",

    "The mask is the only difference":
        "Transformer被切分成的三种方式，唯一的区别就是掩码。<bookmark mark='a'/>编码器让每个位置都能看到其他所有位置：它会读，但不能从左到右地写。<bookmark mark='b'/>解码器用的是因果三角：它写，一次一个词元。<bookmark mark='c'/>2017年那篇论文的翻译模型两样都有。它的解码器看自己的过去，还通过交叉注意力看整个源句：查询来自译文，键和值来自编码器对原文的阅读。<bookmark mark='d'/>前缀语言模型双向读它的提示，再从左到右写出其余部分。这几种谁胜出了、为什么，是第14部分的故事。",

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
        "我们的模型有{t['layers']}个模块、{t['heads']}个头和{t['n_params'] / 1000000.0:.1f}百万个数，一次读{t['ctx']}个字符。我们用那30部小说训练它，大约{t['tokens'] / 1000000.0:.0f}百万个字符，用的是一台普通的处理器，没有显卡。<bookmark mark='a'/>{verdict}",

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
        "记分牌上添了新的一行：我们的Transformer，{float(t['passage_bits']):.2f}。<bookmark mark='a'/>{more}",

    'f"GPT-2 small, at {gpt[\'bits\']:.2f}':
        "GPT-2 small是{gpt['bits']:.2f}，它是同一类机器：一叠这样的模块，大约大{round(124000000.0 / t['n_params'], -1):.0f}倍，用多得多的文本、多得多的算力训练出来。把它们分开的主要是规模，这是第12部分的故事。",

    "The large models of Part 1 are the same kind of machine":
        "第1部分的那些大模型也是同一类机器，只是大得多，用多得多的文本训练：把它们分开的主要是规模，这是第12部分的故事。",

    # ------------------------------------------------------------------ Cost
    "Chapter seven. What a block costs.":
        "第7章。一个模块的成本。",

    'f"First, the numbers a block stores.':
        "先看一个模块要存多少个数。<bookmark mark='a'/>注意力有4个d乘d的矩阵：查询、键、值，还有输出。<bookmark mark='b'/>MLP先升到4d维，再降回来：8倍的d平方。<bookmark mark='c'/>所以一个模块是12倍的d平方，再加上少量偏置和层归一化的增益。<bookmark mark='d'/>再加上把字符变成向量的那张表，以及把向量变回猜测的那张表。<bookmark mark='e'/>对我们的模型，d等于{d}，{L}个模块，{K}个字符，公式给出{fml:,}，把模型的参数一个一个数出来，得到{tot:,}。<bookmark mark='f'/>注意力占每个模块的{att_share:.0%}；其余的都在MLP里。",

    'f"Now the arithmetic for each character.':
        "再看每个字符要做多少运算。<bookmark mark='a'/>每个权重对每个字符用一次，做一次乘法和一次加法：每个权重两次运算。<bookmark mark='b'/>注意力还额外增加了不归任何权重管的工作：查询要和T个键比较，每个键d个数；再对T个值做加权求和。<bookmark mark='c'/>合在一起，就是每个字符的运算量。<bookmark mark='d'/>我们用PyTorch的计数器，数了一次真实前向传播的运算，上下文从{Ts[0]}到{Ts[-1]:,}个字符。{match}贾里德·卡普兰和同事们的版本只算了平方项的一半，因为因果掩码把另一半扔掉了；跳过被掩掉那一半的计算内核，确实能把它省下来。<bookmark mark='e'/>训练更贵：一次前向加一次反向，是单独前向的{ratio:.1f}倍，每个权重、每个字符6次运算这条规则，就是这么来的。",

    "They match the formula to within a fraction of a percent.":
        "它们和公式的差别不到百分之一。",

    'f"Which term wins?':
        "哪一项占上风？<bookmark mark='a'/>对每个字符来说，注意力那部分随上下文增长，权重那部分不变。当2LTd等于24Ld平方，也就是上下文长度是宽度的12倍时，两者相等。<bookmark mark='b'/>对我们的模型，这是{Tx:,}个字符，比它读的任何东西都长，所以它的成本主要在权重上。对GPT-3，是{gx:,}个词元。<bookmark mark='c'/>但注意力这一项有根刺：在一整段T个字符的文本上加起来，它像T的平方那样增长，而且要写下一个字符，过去的每个键和值都得留着。这就是长上下文昂贵的原因，也是第15、16和19部分存在的原因。",
    # ------------------------------------------------------------------ Positions
    "Chapter eight. Where is each character?":
        "第8章。每个字符在哪里？",

    'f"Chapter five ended with a problem':
        "第5章留下了一个问题：注意力分不清“dog bites man”和“man bites dog”。2017年那篇论文的答案，是在第一层之前，给每个字符的向量加上一个位置信号。<bookmark mark='a'/>一对一对的数以不同的速度振荡，每对是一个正弦和一个余弦，从每6个位置转一圈，一直到几万个位置才转一圈。<bookmark mark='b'/>为什么用正弦？因为三角函数的和角公式：往后移k个位置，对每一对来说都是同一个旋转，不管从哪里开始，所以一层网络可以用一个固定的矩阵，学会往回看固定的距离。<bookmark mark='c'/>数值上检验过，它在舍入误差以内成立。而且两个位置的点积，只取决于它们相隔多远。<bookmark mark='d'/>GPT-2走了另一条路，干脆为每个位置学一个向量，一共1024个。这样也行，但一个它从没见过的位置，就根本没有向量。",

    "A different idea: forget absolute positions":
        "另一个想法：忘掉绝对位置，只告诉注意力两个字符相隔多远。2018年，彼得·肖和同事们为每个距离学一个向量，T5则为每一段距离范围学一个偏置。<bookmark mark='a'/>2021年，奥菲尔·普雷斯、诺亚·史密斯和迈克·刘易斯把它做到了最简单。ALiBi根本不加位置向量：它从每个分数里减去一个和距离成正比的惩罚。<bookmark mark='b'/>每个头有自己的斜率，取自一个等比数列：斜率陡的头只看最后几个字符，平缓的头看得很远。他们报告说，一个在1024个词元上训练的模型，读2048个词元时，和一个就在这个长度上训练的模型一样好。",

    "And the most surprising answer: give no positions at all.":
        "还有最出人意料的答案：干脆不给位置。解码器仍然有它的因果掩码，而掩码会泄露位置。<bookmark mark='a'/>取一个把注意力平均摊到它能看到的所有东西上的头：在位置t，t个键每个分到t分之1。<bookmark mark='b'/>它的输出就是过去的平均。<bookmark mark='c'/>如果第一个词元带了标记，这个标记在平均里所占的份额就是t分之1，后面的层就能从中读出位置。<bookmark mark='d'/>阿迪·哈维夫和同事们在2022年发现，没有位置信号的语言模型仍然能学会自己在哪里；阿米尔侯赛因·卡泽姆内贾德和同事们则发现，在推理任务上，它们推广到更长输入的能力，比带显式位置的模型还好。Meta的Llama 4把不带位置的层，穿插在用旋转位置的层之间。旋转位置，也就是今天几乎每个模型都在用的答案，就是下一章。",

    # ------------------------------------------------------------------ Rope
    "Chapter nine. Positions as rotations.":
        "第9章。用旋转表示位置。",

    "In 2021 Jianlin Su and colleagues":
        "2021年，苏剑林和同事们提出了今天几乎每个模型都在用的答案：不把位置加到输入上，而是去旋转查询和键。把一个查询的32个数分成16对；每一对是平面上的一根箭头。<bookmark mark='a'/>在位置m，把第j对转过m乘以一个角度θ j。<bookmark mark='b'/>第一对转得很快，每6个字符转一整圈；之后的每一对都转得更慢，一直慢到3.5万个字符才转一圈。<bookmark mark='c'/>键也用同样的方式旋转。就像钟表的指针：快指针告诉你附近的位置，慢指针告诉你在一篇长文里走到了哪里。这就是RoPE，旋转位置编码。",

    "Why rotations? Here is the whole proof.":
        "为什么用旋转？这里是完整的证明。把位置m处的旋转记作R m。<bookmark mark='a'/>旋转后的查询和旋转后的键，分数是q的转置，乘R m的转置，乘R n，再乘k。<bookmark mark='b'/>旋转的转置，就是反方向的旋转。<bookmark mark='c'/>先往回转m，再往前转n，就是转了n减m。<bookmark mark='d'/>所以分数只取决于两个字符相隔多远，尽管每一个都是按它自己的绝对位置旋转的。用随机向量检验过，在舍入误差以内成立。",

    "Here is the same fact, seen on one pair":
        "在一对数上看同一个事实：位置5的一个查询，和位置2的一个键。<bookmark mark='a'/>它们的分数取决于两者之间的夹角。现在把两个都往后移同样的距离，就好像同样的词出现在文本更后面的地方。<bookmark mark='b'/>两根箭头转过同样的角度，所以它们之间的夹角不变，分数也不变。<bookmark mark='c'/>旋转后的查询和键，打分看的是它们相隔多远，而不是它们在哪里。",

    "And a bonus. Score a query against an identical key":
        "还有一个额外的好处。拿一个查询和一个与它完全相同的键打分，然后把它们拉开。每一对的箭头都以自己的速度错开，所以分数随距离缩小：<bookmark mark='a'/>平均来说，近处的匹配比远处的更算数，这是一种偏向最近过去的温和倾向，没有人特意去造它。<bookmark mark='b'/>从2021年起，旋转位置就成了标准：几乎每个开放模型都在用它。",

    '"Which hands does a trained model actually use?':
        "训练好的模型实际上用的是哪些指针？2024年，费德里科·巴尔贝罗和同事们查看了谷歌Gemma的内部：它最快的那些对，构造出尖锐的位置模式，比如恰好往回看一个词元；而最慢的那些对，几乎不转，似乎承载着含义。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>设计者们听懂了这个暗示。Qwen3-Next每个头的256个数里只旋转64个，其余的不动；Gemma 3把它的全局层的时钟放慢了一百倍，底数用一百万而不是一万，让它们在长文档上慢慢地转。",

    "f'Our small model has a favourite":
        "我们的小模型有一个最爱：第{jm + 1}对，它每{wl[jm]:,.0f}个字符才转一圈，比它的整个上下文还长，却承载了它的查询和键{e[jm]:.0%}的大小，是平均份额的{e[jm] * n:.1f}倍。它几乎不转，就像一条传送内容的普通通道。",

    "f'Our small model does the same":
        "我们的小模型也是这样：在它的{ctx}个字符里一圈都转不完的那{len(slow)}对，承载了它的查询和键{s_slow:.0%}的大小，而如果平均分配，应该是{even:.0%}。",

    "f'Our small model shows no such preference":
        "我们的小模型没有表现出这种偏好：在它的{ctx}个字符里一圈都转不完的那{len(slow)}对，承载了它的查询和键{s_slow:.0%}的大小，和平均分配的{even:.0%}差不多。",

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
        "第3章除以根号d，是为了在训练一开始让分数待在范围之内。但训练会让权重变大，而一个分数是其中两个权重的乘积：<bookmark mark='a'/>把W Q和W K都放大c倍，每个分数就放大c的平方倍。<bookmark mark='b'/>来看看这对我们自己的Transformer有什么影响。c等于2时，最大的分数从{lg[0]:.0f}变成{lg[i2]:.0f}，注意力的熵从{ent[0]:.1f}比特降到{ent[i2]:.1f}，一个键拿走九成以上权重的行所占的比例，从{pk[0]:.0%}变成{pk[i2]:.0%}。<bookmark mark='c'/>模型的猜测也变差了：从每字符{bits[0]:.2f}比特变成{bits[i2]:.2f}，c等于{cs[-1]:.0f}时是{bits[-1]:.2f}。<bookmark mark='d'/>在大规模训练中，这会自己发生：2023年，训练谷歌那个220亿参数视觉Transformer的团队看到，注意力的logit无限制地增长，直到训练发散。",

    '"The fix the vision team used':
        "视觉团队用的、此后许多语言模型也在用的修补办法，是QK归一化。<bookmark mark='a'/>在做点积之前，把每个头的查询和键都除以它们的均方根大小，再乘以一个学出来的增益。<bookmark mark='b'/>一个向量除以它的均方根，长度恰好是根号d，<bookmark mark='c'/>所以由柯西-施瓦茨不等式，分数永远不会超过增益的平方乘以根号d，不管W Q和W K变得多大。<bookmark mark='d'/>{moves}<bookmark mark='e'/>{cost}<bookmark mark='f'/>Qwen3、GLM-4.5和Gemma 3都用了它；第18部分会在训练中观察logit，对比有它和没有它的情况。",

    "On our transformer, with its queries and keys normalized to their trained sizes, growing the weights now changes":
        "在我们的Transformer上，把查询和键归一化到它们训练后的大小，现在再放大权重，就什么都不会改变了。",

    "f'On our transformer, with its queries and keys normalized":
        "在我们的Transformer上，把查询和键归一化到它们训练后的大小，现在再放大权重，熵只变化了{flat:.3f}比特。",

    "f'But bolted onto a model that was trained without it":
        "但把它硬装到一个没用它训练过的模型上，每字符要多付{bn - b0:.2f}比特，{bn:.2f}对{b0:.2f}：我们的模型已经学会了利用查询的大小，所以QK归一化必须从训练一开始就在。",

    "Bolted onto a model trained without it, it costs almost nothing here.":
        "把它硬装到一个没用它训练过的模型上，在这里几乎没有代价。",

    'f"A gentler alternative is a soft cap':
        "一个更温和的替代办法是软上限：把每个分数s，换成c乘以s除以c的双曲正切。<bookmark mark='a'/>小的分数几乎原样通过；大的分数则在正负c处趋于平缓。<bookmark mark='b'/>把c设得比我们训练好的模型的最大分数{capv:.0f}稍高一点，再放大权重：分数再也超不过{capv:.0f}，而且{et}。<bookmark mark='d'/>{bt}<bookmark mark='c'/>Gemma 2在2024年把注意力分数的上限设为50；Gemma 3则放弃了上限，改用QK归一化，它给分数设了界，却不会把分数弯折。",

    "f'the entropy falls only to":
        "熵只降到{ent_c[-1]:.1f}比特，而不是{ent_p[-1]:.1f}",

    "f'the entropy falls just as far":
        "熵降得一样多，降到{ent_c[-1]:.1f}比特",

    "f'At c of {cs[-1]:.0f} the bits per character":
        "c等于{cs[-1]:.0f}时，每字符比特数是{bits_c[-1]:.2f}，而不是{bits_p[-1]:.2f}。",

    "f'But the guesses get worse, not better":
        "但猜测变得更差，而不是更好：c等于{cs[-1]:.0f}时，每字符{bits_c[-1]:.2f}比特，不加上限是{bits_p[-1]:.2f}。每个大分数都被压平到上限上，一个头就再也分不清它最好的那几个键了：上限必须设得远高于模型实际用到的分数。",

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
        "Transformer做不到什么？固定的层数，就是固定量的顺序计算。<bookmark mark='a'/>威廉·梅里尔和阿希什·萨巴瓦尔在2023年证明：一个深度固定、数值大约只有log n个比特的Transformer，可以用常数深度的阈值电路来模拟：也就是TC零类。<bookmark mark='b'/>如果像大多数人相信的那样，这个类比NC一要弱，那么就没有哪个固定深度的Transformer，能在任意长度上追踪五个物体的一连串洗牌。在实践中深度也很要紧：一层是搭不出归纳头的。<bookmark mark='c'/>出路是让模型写出来：思维链里的每一个词元，都是再把所有层走一遍，这是第28部分的故事。<bookmark mark='d'/>RASP还能预测什么容易训练：哈蒂·周和同事们发现，当一个简短的RASP程序能在任意长度上解决某个任务时，Transformer往往就能推广到更长的输入。",

    # ------------------------------------------------------------------ Frontier
    "Chapter seventeen. Attention in 2026.":
        "第17章。2026年的注意力。",

    'f"Why so much effort?':
        "为什么要费这么大劲？用第7章的算术，算一个和DeepSeek-V3一样宽的模型：<bookmark mark='a'/>上下文是四千个词元时，注意力的成本是权重成本的{r4:.2f}；到一百万个，是{r1m:.0f}倍。<bookmark mark='b'/>长上下文让注意力成了最贵的部分。",

    "Every model in 2026 still computes this formula somewhere.":
        "2026年的每一个模型，仍然在某处计算着这个公式。变的是在哪里算，以及算多少。<bookmark mark='a'/>在softmax内部，是前面几章的那些修补：汇点logit、输出门控、QK归一化，还有完全没有位置的层。<bookmark mark='b'/>每个过去的词元留下的键和值，已经被压小了：在多个头之间共享，或者从一个小的潜在向量重建出来，这是把第4章的低秩想法用在了记忆上。<bookmark mark='c'/>许多模型只看过去的一部分：一个滑动窗口，或者一个又小又快的索引器，为每个查询挑出几千个过去的词元。<bookmark mark='d'/>还有些模型把大多数注意力层，换成一个边读边更新的固定大小的记忆：在Qwen3-Next和Qwen3.5里，每一个注意力层配三个这样的层。",

    "Here is what such a hybrid looks like":
        "这样的混合架构长这样：2026年发布的Kimi K3有93层，其中只有24层是完整的注意力。<bookmark mark='a'/>其余各层保留一个固定大小的记忆，边读边更新。<bookmark mark='b'/>为什么还要留注意力？因为注意力能把上下文里的任何东西原样回想起来，就像第14章的归纳头那样；而固定大小的记忆必须决定忘掉什么。少数几层注意力负责回想，其余的负责压低成本。<bookmark mark='c'/>那种记忆怎样工作，它为什么是乔装打扮的注意力，就是我们接下来要去的地方：先在第14部分走过这些模型本身的谱系，再到第15部分讲记忆。",

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
        "大模型能从提示里的例子中学习，却一个权重也不改。给它看几个翻译的例子，它就会翻译下一个。一次前向传播怎么能学习？<bookmark mark='f'/>前向传播就是把网络跑一遍：数字进去，每一层流过一次，出来一个猜测。这中间没有任何权重被改动。这里有一个小到可以彻底拆开的例子。<bookmark mark='a'/>每个提示是一串例子：四个数x，和一个答案y，y是这四个数的一个固定的加权和。然后是一个问题：一个新的x，答案空着。<bookmark mark='b'/>难点在于：每个提示用的隐藏权重都不一样，所以什么都没法死记。要回答，模型必须从眼前的例子里推出规律。",

    'f"Take the simplest attention':
        "取最简单的注意力：一层，没有softmax。每个词元是一个例子的数和它的答案，注意力给每个词元加上其他词元的一个加权和。在许多提示上训练它：它在问题上的误差，从{cv[0, 1]:.1f}降到{cv[-1, 1]:.2f}。<bookmark mark='a'/>这是它学到的两个矩阵。蓝色是正，红色是负。<bookmark mark='b'/>现在换一件事来做：在提示里的例子上，从零出发，对第6部分的最小二乘损失走一步梯度下降。这一步是每个答案乘以它的x再求和，而预测是每个答案乘以“它的x和问题有多匹配”再求和：x之间的点积，给y加权。<bookmark mark='c'/>这就是注意力，用的就是这两个矩阵：一个比较x的单位矩阵块，和一个把y传下去的元素。它们正是网络自己找到的那个模式。",

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
