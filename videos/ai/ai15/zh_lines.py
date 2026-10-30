"""Chinese narration for ai15: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第15部分：记忆'

CHAPTERS = {
    'Hook': '它读过的一切',
    'KVCache': '1. 缓存',
    'Evict': '2. 让缓存少存一些',
    'Linear': '3. 去掉softmax的注意力',
    'FastWeights': '4. 会记东西的矩阵',
    'Rules': '5. 遗忘与纠正',
    'GatedDelta': '6. 从几何看δ规则',
    'Parallel': '7. 并行地训练递推',
    'SSM': '8. 状态空间模型',
    'Mamba': '9. 选择性：Mamba及其后来者',
    'TTT': '10. 会学习的记忆',
    'Recall': '11. 回忆测试',
    'Hybrid': '12. 混合架构',
    'LongContext': '13. 上下文到底有多长？',
    'Retrieval': '14. 把检索当作记忆',
    'Frontier': '15. 2026年末的前沿',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"Every token a transformer reads, it keeps':
        "Transformer每读一个词元，都会把它留下来：在每一层里，留下一个键和一个值。<bookmark mark='a'/>对700亿参数的Llama 3.1来说，"
        "每个数都用bf16存储，也就是16比特、2个字节，这样每个词元要占{per / 2 ** 10:.0f}KB。<bookmark mark='b'/>一段长对话，12.8万个词元，"
        "就需要{128000.0 * per / 2 ** 30:.0f}GB的内存，只为了记住它读过的东西。",

    'The alternative is to read like we do':
        "另一种办法，是像我们人一样阅读：只保留一份固定大小的记忆，每读到一个词，就更新它一次。<bookmark mark='a'/>这样一来，问题就变成了："
        "该留下什么，又该忘掉什么。",

    'How we got here. In 1982 John Hopfield':
        "我们是怎么走到这里的。1982年，约翰·霍普菲尔德造了一个网络，它把记忆存在连接里，只要给它一部分，它就能回到完整的那一个。"
        "<bookmark mark='a'/>1992年，于尔根·施密德胡伯让一个网络一个词元一个词元地，去写另一个网络的权重：这就是快权重，也是这一部分的核心想法。"
        "<bookmark mark='b'/>1997年，LSTM给循环网络配上了一个带门的记忆单元，这是第10部分的故事。<bookmark mark='c'/>2014年，神经图灵机和记忆网络，"
        "用注意力去读写一份记忆。<bookmark mark='d'/>2017年，Transformer干脆把一切都留下来。<bookmark mark='e'/>从2019年起，Transformer-XL"
        "看得更远，Longformer和BigBird则只看其中一部分。<bookmark mark='f'/>2020年，线性注意力把Transformer变回了循环网络，检索则把一份记忆"
        "放到了模型之外。<bookmark mark='g'/>接着出现了状态空间模型，从上万亿个词元里检索，还有Mamba：一份会选择留下什么的记忆。"
        "<bookmark mark='h'/>到了2026年，前沿的开放模型，每4层里有3层是固定大小的记忆，而且能读一百万个词元。",

    'This is Part 15 of AI, Built: memory.':
        "这是《人工智能，从零搭建》的第15部分：记忆。<bookmark mark='a'/>首先，是注意力自己的记忆：缓存，模型怎样缩小它，以及哪些可以扔掉。"
        "<bookmark mark='b'/>然后，把一个矩阵当作记忆，从霍普菲尔德和快权重，一直讲到线性注意力。<bookmark mark='c'/>怎样往里写，以及怎样在一整段文本上"
        "一次训练这样的记忆。<bookmark mark='d'/>状态空间模型，以及边读边学习的记忆。<bookmark mark='e'/>然后我们来测一测，哪些记忆能查找东西，"
        "再把它们混在一起。<bookmark mark='f'/>最后是长上下文：它们实际上管用到什么程度，以及放在模型之外的记忆。<bookmark mark='g'/>这一部分的每个模型"
        "都在这里训练，我们会看着每一个模型学习。",

    # ------------------------------------------------------------------ KVCache
    'Chapter one. The cache.':
        '第1章。缓存。',

    'When a model writes, it makes one token at a time':
        "模型写东西的时候，一次只写一个词元，而每个新词元的查询，都要去看前面每一个词元的键和值。<bookmark mark='a'/>如果每来一个新词元，"
        "都把这些重新算一遍，就太浪费了，所以模型把它们存起来：这就是KV缓存。<bookmark mark='b'/>缓存随着每个词元不断变大，而每个新词元，"
        "都得把它整个读一遍。同时服务许多段长对话时，把显卡塞满的，正是这份记忆，而不是模型的权重。",

    'f"How big is it? Take Llama 3.1':
        "它有多大？就拿Llama 3.1来说：700亿参数，80层。<bookmark mark='a'/>如果每个注意力头都各存各的键和值，上下文里的每个词元，"
        "就要占{pt['llama_mha'] / 2 ** 20:.1f}MB。<bookmark mark='b'/>Llama让它们共用：64个查询头分成8组，每一组共用一个键和一个值。"
        "这样就少了{r1:.0f}倍，每个词元{pt['llama'] / 2 ** 10:.0f}KB，而质量几乎不变。<bookmark mark='m'/>2019年，诺姆·沙泽尔的多查询注意力"
        "走到了头：所有的头只用一个键和一个值，在这里是{pt['llama_mqa'] / 2 ** 10:.0f}KB，但质量会损失一些；2023年，约书亚·安斯利和同事们的"
        "分组查询，是两者的折中。<bookmark mark='c'/>DeepSeek-V3走得更远，混合架构的Qwen3-Next也是。我们来看看它们是怎么做的。",

    'f"DeepSeek\'s trick is multi-head latent attention.':
        "DeepSeek的诀窍，是多头潜在注意力。所谓潜在向量，就是一份简短的隐藏摘要，完整的东西可以从它重建出来。<bookmark mark='a'/>"
        "每个词元都被压缩成一个很短的潜在向量，只有{D['kv_lora_rank']}个数，缓存里存的就只有它。<bookmark mark='b'/>需要的时候，再用另外两个"
        "矩阵，从它解压出全部{D['q_heads']}个头的键和值。<bookmark mark='c'/>其实连解压都不用：一个查询的分数，是几个矩阵的乘积，所以可以把键"
        "的那个矩阵并进查询里，这是第3部分的线性代数，于是注意力直接读取潜在向量。<bookmark mark='d'/>和同样形状的完整注意力相比，"
        "内存少了{ratio:.0f}倍。",

    'f"There\'s a catch, and it\'s part thirteen\'s rotations.':
        "这里有个问题，出在第13部分讲的旋转上。<bookmark mark='a'/>不考虑位置的话，键的矩阵只要往查询里并一次，缓存里的每个潜在向量，"
        "就都能直接打分。我们用随机权重验证过：完全一样，只差舍入误差。<bookmark mark='b'/>可是有了旋转位置编码，查询要按它自己的位置转，"
        "键也按它自己的位置转，两者之间剩下的，是一个按它们的距离转的旋转。它夹在中间，而且每一对都不一样，所以没有哪一个矩阵可以并进去。"
        "硬要并进去的话，分数会偏差{100 * float(m['rel_rope_folded']):.0f}%。<bookmark mark='c'/>DeepSeek的办法是解耦：把位置放进一个额外的"
        "小键里，所有的头都共用它，和潜在向量一起缓存，也就是{D['kv_lora_rank']}个数，再加{D['rope_dim']}个。内容那一部分照旧可以并进去，"
        "分数又完全对上了。<bookmark mark='d'/>怎样快速地提供这份缓存、给它分页、在对话之间共享、用更少的比特存它，是第19部分的主题。"
        "这里我们要问的是：一份记忆应该留下什么。",

    # ------------------------------------------------------------------ Evict
    'Chapter two. Keeping less of the cache.':
        '第2章。让缓存少存一些。',

    'The cache can\'t grow forever':
        "缓存不能无限增长，所以第一个问题是：模型可以不要哪些词元。<bookmark mark='a'/>完整的注意力，让每个词元去看前面的每一个词元。"
        "2019年，里翁·蔡尔德的稀疏Transformer，只看最近的一个窗口，再加上一个跨步的模式，<bookmark mark='b'/>2020年，Longformer保留一个窗口，"
        "再加几个全局词元，它们看得见一切，也被一切看见。<bookmark mark='c'/>BigBird又加了几个随机的键，并且证明了，这种稀疏的模式，"
        "仍然能算出完整注意力能算的任何东西。<bookmark mark='d'/>这样一来，每个词元读的键的数目是固定的，缓存就不再增长了。"
        "<bookmark mark='e'/>2019年的Transformer-XL走的是另一条路：它把上一段的状态缓存下来，让每一段都去读它，于是一叠层能看到往前好几段。",

    'f"A sliding window has a hidden flaw':
        "滑动窗口有一个隐藏的缺陷，2023年由肖光烜和同事们发现。第13部分讲过，许多注意力头在没事可做的时候，会把注意力停在最开头那个词元上，"
        "这就是注意力汇点。<bookmark mark='a'/>这是本系列自己的模型，就是用三十部小说训练的那个：每个方块是一个头，上面的数，是它的注意力"
        "落在窗口第一个词元上的比例。<bookmark mark='b'/>如果平均分配，第一个词元会分到{100 * uni:.1f}%。可实际上，{verdict}",

    "f'{n_sink} of its {L_ * H_} heads put more":
        "它的{L_ * H_}个头里，有{n_sink}个放在第一个词元上的注意力，超过这个数的十倍；平均下来，每个头给它{100 * mean:.0f}%：这就是汇点，"
        "和大模型里一样。",

    "f'only {n_sink} of its":
        "它的{L_ * H_}个头里，只有{n_sink}个放在第一个词元上的注意力超过这个数的十倍；平均下来，每个头给它{100 * mean:.0f}%。我们这个小模型，"
        "比大模型更少依赖第一个词元。",

    "f'not one of its {L_ * H_} heads":
        "它的{L_ * H_}个头里，没有一个给第一个词元哪怕这个数的十倍；平均下来，每个头只给它{100 * mean:.1f}%。这个模型从没长出汇点："
        "它是在从小说里随机截取的窗口上训练的，找到了别的地方来停放注意力。",

    'f"That matters for the cache.':
        "这对缓存很要紧。我们让本系列的模型，像服务器那样一次一个地读计分板那段文字的前{n:,}个词元，每个头只留出{W}个词元的键和值的位置，"
        "位置在缓存内部计数。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}",

    "f'Keep only the last {W} tokens, and once":
        "只留最后{W}个词元，一旦第一个词元被挤出去，损失就猛地跳上去，而且一直高居不下：每个字符{bits['window']:.2f}比特。",

    "f'Keep only the last {W} tokens, and the loss barely":
        "只留最后{W}个词元，第一个词元被挤出去时，损失几乎不动：每个字符{bits['window']:.2f}比特。",

    "f'Keep the first four tokens as well":
        "再把最前面的四个词元也留着，它就恢复了：{bits['sinks']:.2f}，接近每个窗口都从头重算的{br:.2f}。",

    'f"Keeping the first four tokens as well gives':
        "把最前面的四个词元也留着，得到{bits['sinks']:.2f}，而每个窗口都从头重算是{br:.2f}：没有汇点可丢，这个模型也就用不着它们。",

    "f'And keeping everything fails differently":
        "而什么都留着，会以另一种方式失败：过了第256个位置，模型就遇到了训练时从没见过的位置，最后得到{bits['full']:.2f}。这就是为什么长窗口"
        "需要第13部分讲的上下文扩展。",

    "f'Keeping everything, with positions beyond":
        "什么都留着，位置超出了它训练时的256，得到{bits['full']:.2f}：在这里，旋转位置编码比训练时的范围多撑了一点。",

    '"A second idea, H2O from Zhenyu Zhang':
        "第二个想法，是同样在2023年由张振宇和同事们提出的H2O：留下要紧的词元。<bookmark mark='a'/>把每个缓存词元到目前为止得到的注意力加起来；"
        "缓存满了，就把得到最少的那个挤出去，但最近的一段窗口永远保留。少数几个重量级词元，得到了大部分注意力，汇点就是其中之一。"
        "<bookmark mark='b'/>这是三种策略在同一段文字上的结果，每个头的缓存分别是{B[0]}、{B[1]}和{B[2]}个词元。{v}<bookmark mark='d'/>{v_b}"
        "<bookmark mark='c'/>挤出词元，是用过去对未来做的一个猜测：一个看似不重要的词元，也许正是后面某个问题需要的。第16部分改为按内容"
        "来挑选词元。",

    "f'With the smallest cache, {B[0]} tokens":
        "缓存最小、只有{B[0]}个词元时，{name[best]}最好：重量级词元每个字符{bh[0]:.2f}比特，汇点{bs[0]:.2f}，普通窗口{bwd[0]:.2f}。",

    "f'With {B[-1]} tokens all three are close":
        "到了{B[-1]}个词元，三种都接近从头重算的{br:.2f}，选哪种几乎没有差别。",

    "f'Even with {B[-1]} tokens they stay above":
        "即使有{B[-1]}个词元，它们也都还高于从头重算的{br:.2f}。",

    # ------------------------------------------------------------------ Linear
    'Chapter three. Attention without the softmax.':
        '第3章。去掉softmax的注意力。',

    "Here's attention for a whole text of T tokens":
        "这是对一整段T个词元的文本做注意力：查询乘以键，再乘以值。<bookmark mark='a'/>查询和键的乘积，是一张T乘T的分数表：它随长度的平方增长。"
        "<bookmark mark='b'/>可是一串矩阵相乘，先乘哪两个都可以。先把键和值乘起来，中间那张表就只有d乘d，不管文本有多长。<bookmark mark='c'/>"
        "麻烦在于softmax：它夹在QK和V之间，挡住了这种重新组合。把它换成查询和键的一些简单的正值特征：让每一个都经过一个固定的函数φ，"
        "把每个数都变成正的，这样它们的点积，就能顶替softmax里的指数。这样就可以重新组合了：这就是线性注意力。",

    'Now read the text one token at a time.':
        "现在，一次读一个词元。乘法重新组合之后，模型需要从过去得到的一切，就是一个d乘d的矩阵，也就是状态。<bookmark mark='a'/>每个新词元"
        "都往里面写：它的值乘以它的键，也就是一个外积，<bookmark mark='o'/>它把值的每一个数，和键的每一个数都乘一遍：得到一整张网格，就像一张"
        "乘法表，再加上去。<bookmark mark='b'/>要读取，就用状态乘以查询。这份记忆永远不会变大：去掉softmax的Transformer，就是一个循环网络，"
        "<bookmark mark='r'/>也就是一次读一个词元、带着一份固定大小的记忆往前走、每一步都更新它的网络。这是卡塔罗普洛斯和同事们在2020年证明的。",

    'f"The payoff grows with length.':
        "文本越长，好处越大。softmax注意力的计算量，随文本长度的平方增长；递推的计算量，则沿一条直线增长。<bookmark mark='a'/>到了100万个词元，"
        "乘法次数少了{r:,.0f}倍。那为什么不是人人都用它？因为固定大小的记忆，必须遗忘，而它怎样写入，决定了它会忘掉什么。",

    # ------------------------------------------------------------------ FastWeights
    'Chapter four. A matrix that remembers.':
        '第4章。会记东西的矩阵。',

    'A memory you return to by its content is old.':
        "按内容找回的记忆，是个老想法。1982年，约翰·霍普菲尔德描述了一个神经元网络，每个神经元取正1或负1，它按照1949年的赫布规则，"
        "把模式存在连接里：一起放电的神经元，连在一起，也就是各个模式和自身的外积之和。<bookmark mark='a'/>我们存了五个随机模式，"
        "每个一百个神经元。<bookmark mark='b'/>把第一个模式翻转三十位之后交给它，再让每个神经元轮流取它输入的正负号。<bookmark mark='c'/>每一次"
        "更新只会让一个能量降低，于是状态滚下山，落进最近的山谷：存着的那个模式，从一份损坏的副本里找了回来。",

    'f"But a matrix of N by N numbers':
        "可是，一个N乘N的矩阵，用这种办法存不了多少模式。<bookmark mark='a'/>存得越多，模式之间就开始互相干扰：山谷合并，还会冒出虚假的山谷。"
        "一百个神经元时，大约在每个神经元存{half:.2f}个模式的时候，一半的线索能被准确找回；对很大的网络，理论给出的极限是0.138。"
        "<bookmark mark='b'/>记住这一点：靠累加外积来存储，迟早会存满。它马上会以串扰的面目再次出现。",

    'The same sum of outer products became':
        "同样的外积之和，变成了一份键和值的记忆。1972年，特沃·科霍宁和詹姆斯·安德森把一个值存在一个键下面，做成一个矩阵：加上值乘以键的转置，"
        "再用键去读。<bookmark mark='a'/>1992年，于尔根·施密德胡伯把它做成了快权重：一个慢网络在每一步，把外积写进一个快网络的权重，"
        "成为到目前为止这段序列的记忆。<bookmark mark='b'/>2016年，吉米·巴、杰弗里·辛顿和同事们让它复活，成为一份关于最近过去的、会衰减的记忆。"
        "<bookmark mark='c'/>与此同时，第10部分见过的神经图灵机和记忆网络，留着一份单独的记忆，用注意力去寻址。<bookmark mark='d'/>"
        "而2020年的线性注意力，也就是上一章的递推，原来就是同一个矩阵。<bookmark mark='e'/>2021年，伊马诺尔·施拉格、入江一树和施密德胡伯"
        "给它起了名字：线性Transformer其实是快权重编程器，他们还给了它一种更好的写法。",

    'f"Here is that memory at work':
        "这份记忆是这样工作的，一步一步地写，一步一步地读。记忆是一个矩阵S，8乘8，一开始是空的。<bookmark mark='a'/>要把一个值存在一个键下面，"
        "就把它们乘成一个外积，也就是值的每个数乘以键的每个数组成的网格，再加上去。<bookmark mark='b'/>四个键，四个值，四次相加。"
        "<bookmark mark='c'/>要读取，就用矩阵乘以一个键。每个键都拿回自己的值，再加上其他值的一点点，多少取决于它们的键重叠了多少：这里的误差从"
        "{e.min():.2f}到{e.max():.2f}，因为这些键几乎、但不完全互相垂直。",

    'f"With many pairs, that leak is the whole story.':
        "键值对多了，这份泄漏就成了全部的问题。<bookmark mark='a'/>读第j对，你得到它的值，再加上其他每一个值，按它的键和键j重叠的程度加权。"
        "在d维空间里，随机的键彼此重叠大约根号d分之1，<bookmark mark='b'/>所以这些泄漏加起来，大约是d分之N。d等于{d}时，到了{d}对，"
        "噪声就和答案一样大了：和霍普菲尔德网络一样，会被填满。只做加法，永远擦不掉东西。",

    # ------------------------------------------------------------------ Rules
    'Chapter five. Forgetting and correcting.':
        '第5章。遗忘与纠正。',

    'f"The first fix is to forget on purpose.':
        "第一个办法，是有意地遗忘。每次写入之前，先把整个记忆缩小一点。<bookmark mark='a'/>这里是{n}对键值，按它们写进去的早晚，依次读回来。"
        "只做加法，每一对都同样模糊。加上衰减，最近的几对保持清晰，旧的就随它去。<bookmark mark='b'/>RetNet、门控线性注意力和Mamba-2都会衰减，"
        "而其中最好的，让每个词元自己决定衰减多少：换到一个新话题的开头，就多忘一些；在一句话的中间，几乎什么都不忘。",

    'f"The second fix is smarter.':
        "第二个办法更聪明。写入之前，先读一读记忆里这个键现在对应着什么，然后只写入差值：应该有的，减去已经有的。这就是δ规则，威德罗和霍夫"
        "在1960年提出的学习规则。<bookmark mark='a'/>当世界在变化时，这一点就很要紧。门开着；后来，门关上了。只做加法，两条都会存下来，"
        "答出来的是两者的混合。δ规则则用新值替换旧值。<bookmark mark='b'/>这里有{M}个键，用新的值重写了{W}次，然后问它们最新的值。"
        "只做加法：误差是{vals[0]:.0f}，它记住了写进去过的每一个值。加上衰减：{vals[1]:.2f}。δ规则：{vals[2]:.2f}。",

    'f"Watch the difference on the eight-by-eight memory':
        "在上一章那份8乘8的记忆上，看看两者的区别。同样的四对先写进去，<bookmark mark='a'/>然后给第{kk + 1}个键换一个新值。<bookmark mark='b'/>"
        "只做加法，会把新值叠在旧值上面：现在读这个键，得到的是两者的混合，误差是{ka:.2f}。<bookmark mark='c'/>δ规则先读出记忆里这个键对应的东西，"
        "只写入差值：新值被准确地读回来，误差是{float(ed[kk]):.0f}。其他的键会动一点，因为它们和这个键有重叠；如果键互相垂直，它们就完全不会动。",

    'And here is why the delta rule works.':
        "δ规则为什么管用，原因在这里。量一量记忆在一对键值上错得有多远：用这个键读出来的东西，和那个值之间差距的平方。<bookmark mark='a'/>"
        "它的梯度，就是这个差距乘以键。<bookmark mark='b'/>在它上面走一步梯度下降，恰好就是δ规则：在线地、一次一个样本地解最小二乘，"
        "这正是威德罗和霍夫1960年的最小均方规则为他们的ADALINE做的事。所以，这份记忆是一个小模型，一边读文本，一边用第11部分的梯度下降"
        "在这段文本上训练；第13部分那个在上下文中学习的注意力层，做的也是同一件事。<bookmark mark='c'/>给δ规则加上衰减，就得到了Qwen3-Next和"
        "Kimi Linear里的门控δ规则，也就是下一章；把记忆换成一整个网络，就得到了第10章的测试时训练：一个小网络，模型一边读，它的权重一边继续学习。",

    # ------------------------------------------------------------------ GatedDelta
    'Chapter six. The delta rule as geometry.':
        '第6章。从几何看δ规则。',

    "Let's look at the delta rule as geometry.":
        "我们从几何的角度来看δ规则。记忆S是一个线性映射：给它一个键，它就还你一个答案。<bookmark mark='p'/>这里，它作用在一个平面上。"
        "<bookmark mark='a'/>把键k喂给它，它答出S k，可我们想存的值是v。<bookmark mark='b'/>更新时，先把S乘以I减去β乘k乘k转置，再加上β乘v乘k转置。"
        "前面那个矩阵只碰k这一个方向：把它缩短为原来的1减β倍，而和k垂直的每个方向，都原封不动。<bookmark mark='c'/>β等于2分之1时，k对应的答案"
        "朝v走了一半，而垂直方向的答案一点都不动。<bookmark mark='d'/>β等于1时，旧的答案被彻底擦掉，正好换成v：这是一个投影。"
        "<bookmark mark='e'/>而β最大可以到2，这时它会冲过头，变成一个反射，也就是一个特征值为负1的矩阵。听起来像是个毛病，其实是个优点："
        "格拉齐和同事们证明了，有了它，这些记忆就能追踪奇偶性，而这正是第28部分的Transformer没法一步解决的问题。<bookmark mark='f'/>"
        "奇偶性问的是：到目前为止，1的个数是奇数还是偶数？它就像一个电灯开关，每遇到一个1就拨一下，而反射，恰好就是这一拨。",

    'Now the whole family side by side.':
        "现在，把整个家族并排放在一起。<bookmark mark='a'/>线性注意力只做加法。衰减，比如Mamba-2和门控线性注意力，在每次写入之前，"
        "把整个记忆乘以α缩小一点：所有东西都淡去一些。<bookmark mark='b'/>δ规则只修改当前这个键的方向。<bookmark mark='c'/>门控δ规则两样都做："
        "用衰减α在话题变化时清空记忆，再用δ那一步，一次纠正一个事实。Qwen3-Next每4层里有3层，用的就是这条规则。<bookmark mark='d'/>"
        "Kimi Linear的版本，给记忆的每个通道，也就是它的每个特征维度，都配上自己的衰减，用一个对角矩阵代替一个数，这样，有的特征很快淡去，"
        "有的则能保持几千个词元。<bookmark mark='f'/>还有两个成员，是从各自的路上走来的。xLSTM里的矩阵LSTM，来自塞普·霍赫赖特的团队，2024年，"
        "它就是第10部分的LSTM，只是用一个矩阵当记忆单元：一份会衰减的记忆，写入时有一个指数形式的门。<bookmark mark='g'/>RWKV-7，来自彭博和"
        "RWKV社区，2025年，它推广了δ规则：每个通道都有一个衰减，还有一个学出来的、逐通道的速率，决定它沿着一个键擦掉多少，再沿着另一个键写入。"
        "它的作者证明，它能追踪任何有限自动机的状态，而在通常的假设下，固定深度的Transformer做不到。<bookmark mark='e'/>这样写出来，每个成员"
        "都是同一个形状：旧的记忆乘以一个转移矩阵，再加上一次写入，而转移矩阵总是一个对角矩阵加上一个低秩部分。正是这个形状，让它们训练起来很快。",

    # ------------------------------------------------------------------ Parallel
    'Chapter seven. Training a recurrence in parallel.':
        '第7章。并行地训练递推。',

    'Every memory so far is written one token at a time':
        "到目前为止的每一种记忆，都是一次写一个词元，每一步都要等上一步：成千上万步排成一行，而显卡想要的，是几次大的运算。要在一整段文本上"
        "一次训练，就需要另一种办法。<bookmark mark='a'/>先看最简单的情形，只有一个数：把记忆乘以a_t，再加上b_t。这就是会衰减的记忆，一个状态空间模型，"
        "Mamba的一个通道。<bookmark mark='b'/>把每一步写成一对数，a和b。<bookmark mark='c'/>连着的两步，又是一步：乘以a_1乘a_2，再加上a_2乘b_1"
        "加b_2。<bookmark mark='d'/>而三步怎么组合都无所谓：<bookmark mark='e'/>先合前两步，还是先合后两步，结果一样。<bookmark mark='f'/>"
        "这种组合满足结合律，而并行前缀扫描需要的，就只有这一点。这是1980年代就有的技巧，用来并行地计算累计和。2018年，埃里克·马丁和克里斯·"
        "坎迪把它用到了循环网络上，第10部分用它来算minGRU，而Mamba就靠它运行。",

    'f"Here\'s the scan on eight steps.':
        "这是在八步上做的扫描。<bookmark mark='a'/>第一轮，每一步和它紧挨着的前一步组合。<bookmark mark='b'/>第二轮，和往前两步的组合，"
        "<bookmark mark='c'/>第三轮，和往前四步的组合。三轮之后，每个位置都存着到它为止所有步的组合：所有的h_t一下子都有了。<bookmark mark='d'/>"
        "对{int(s['T']):,}步来说，就是{int(s['rounds_hs'])}轮。这个简单的版本总的工作量更大，是T乘以轮数；盖伊·布莱洛赫的上扫加下扫，"
        "大约只要2T。<bookmark mark='e'/>我们把两种都和普通的循环对过，还把数换成了4乘4的矩阵：答案一样，只差舍入误差。",

    'f"For the delta rule, the coefficient is a matrix':
        "对δ规则来说，系数是一个矩阵，I减去β乘k乘k转置，把两个这样的矩阵组合起来，要做一次完整的矩阵乘法：用它们来扫描会很慢。"
        "<bookmark mark='a'/>出路是把文本切成64个词元一块，每一块一次处理完。<bookmark mark='b'/>在一块之内，记忆要连乘64个那种I减去β乘k乘k转置的"
        "矩阵：64个小小的修正，一个接一个。<bookmark mark='w'/>把它们乘出来，就合并成了一个：单位矩阵，减去64个秩为1的项之和，每一项是w乘k转置。"
        "数值分析学家把它叫作WY形式；几十年前，他们在豪斯霍尔德反射的乘积里就找到了它，而那些矩阵，和这里的这些如出一辙。<bookmark mark='c'/>"
        "而所有的w，只要解一次三角方程组就能得到，这叫UT变换：每个w只依赖于它前面的那些，硬件用几次大块的矩阵乘法，就能把它们全部算出来，"
        "而不用一个接一个地等上64次。有了它们，一块的输出和它最后的记忆，就都只是矩阵乘法；门控版本里的衰减，也能并进同样的形式。"
        "<bookmark mark='d'/>我们在自己的电脑上验证过：对{T}个随机词元，一步一步算，和一块一块算，结果只差舍入误差，而顺序执行的步数，"
        "从{T}步变成了{nC}步。{speed}Qwen3-Next和Kimi Linear就是这样训练出来的。",

    "f'Even on this processor the chunks were quicker":
        "即使在这台处理器上，分块也更快：{tc_:.2f}秒，循环要{tr_:.2f}秒；在专为大矩阵乘法打造的显卡上，差距要大得多。",

    "f'On this processor the plain loop was still quicker":
        "在这台处理器上，普通的循环还是更快：{tr_:.2f}秒，分块要{tc_:.2f}秒；在专为大矩阵乘法打造的显卡上，分块远远胜出。",

    # ------------------------------------------------------------------ SSM
    'Chapter eight. State-space models.':
        '第8章。状态空间模型。',

    'A different road to the same place started in control theory.':
        "通往同一个地方的另一条路，起点在控制理论。状态空间模型是一个微分方程：一个隐状态h随时间演化，由输入x推动，读出来就是y。"
        "<bookmark mark='l'/>可以想象一个漏水的桶：输入不断倒进来，水位慢慢漏掉，而你读到的，就是水位。<bookmark mark='a'/>以Δ为步长去读一段文本，"
        "它就变成了一个递推：先把状态缩小，再加上输入。<bookmark mark='b'/>步长决定了记忆。步子小，一个输入会停留很久；步子大，几个词元之后它就没了。",

    'f"How should a continuous memory be read in steps?':
        "一份连续的记忆，应该怎样一步一步地读？在一步之内把方程精确地解出来：状态按Δ乘A的指数衰减，再加上输入，输入也按同样的衰减累积起来。"
        "<bookmark mark='a'/>如果输入在这一步之内保持不变，这个积分就能算出来。<bookmark mark='b'/>结果是A的逆，乘以e的Δ A次方减去单位矩阵，"
        "再乘以B。<bookmark mark='c'/>这就是零阶保持：一个带着A横和B横的递推，对这样的输入是精确的。<bookmark mark='d'/>我们在一个小振子上验证过："
        "零阶保持和一个精细的数值解，相差在{zm}乘以10的负{ze}次方以内。双线性规则的误差随步长的平方缩小，测得的斜率是"
        "{float(z['slope_bilinear']):.1f}。{v}S4用的是双线性规则；Mamba对A用的是零阶保持。",

    'f"Euler\'s simple step is not just less accurate':
        "欧拉法的简单一步，不只是精度差：在最大的步长下它不稳定，误差长到了信号的{ee[0]:.0f}倍。",

    'f"But which A?':
        "可是，用哪个A？顾立彬和同事们问：一个状态要记住一整段信号，意味着什么？他们在2020年给出的回答是HiPPO：保留到目前为止看到的一切的"
        "最佳多项式拟合的系数。<bookmark mark='a'/>每来一个样本，这个拟合都可以用一个形式恰好如此的方程来更新，只是A是一个特定的矩阵。"
        "<bookmark mark='b'/>这里，它在一边看一边记一段信号，一次一个样本，一共{L:,}个，用8个数和用32个数。<bookmark mark='c'/>任何时刻，"
        "这份记忆都能展开成它对整段过去的描绘：8个数是粗略的，32个数就很接近了。<bookmark mark='d'/>在{len(Ns)}种大小里，有{len(close)}种"
        "最后的误差和最佳多项式拟合相差不到百分之一，而那个拟合，记忆从来没有存过：是递推让它一直保持最新。",

    'A state-space model with a fixed A and B':
        "A和B固定的状态空间模型，还有另一副面孔。把递推展开，每个输出都是过去输入的加权和，权重是C乘以A横的j次方，再乘以B横："
        "<bookmark mark='a'/>这是一个卷积，卷积核和文本一样长。<bookmark mark='b'/>我们验证过，两者给出同样的输出。卷积可以用快速傅里叶变换，"
        "在一整段序列上一次训练。<bookmark mark='c'/>这就是S4，由顾立彬、卡兰·戈尔和克里斯托弗·雷在2021年提出：HiPPO的矩阵，靠一种巧妙的"
        "结构变快。它是第一个解出Path-X的模型，这项测试问的是，一张一万六千多像素的图里，两个点是否相连，而图要一个像素一个像素地读。"
        "<bookmark mark='d'/>可是它的卷积核对每个输入都一样：S4层没法根据自己读到的东西，决定要留下什么。",

    # ------------------------------------------------------------------ Mamba
    'Chapter nine. Selectivity: Mamba and after.':
        '第9章。选择性：Mamba及其后来者。',

    "But a fixed step size can't tell what matters.":
        "可是，固定的步长分不清什么要紧。这里有一串输入，全是噪声，只夹着两个值得记住的标记值。<bookmark mark='a'/>步长固定的话，每个标记值"
        "都会被后面的噪声冲淡。<bookmark mark='b'/>2023年，Mamba的想法是：让每个输入自己选步长。遇到重要的东西，就迈一大步把它收进来；遇到噪声，"
        "几乎一步都不迈，状态就保持不动。现在，状态会一直留着那个标记值，直到下一个标记值把它替换掉。这是一份会选择的记忆。<bookmark mark='c'/>"
        "Δ、B和C都取决于输入，卷积的技巧就没了；顾立彬和特里·道把递推写成上一章的扫描，让状态待在芯片最快的存储里，报告说推理时的吞吐量是"
        "Transformer的五倍。",

    'In 2024 Tri Dao and Gu showed':
        "2024年，特里·道和顾立彬证明：一个选择性的状态空间模型，如果每一步的A只是一个数，那它就是第5章那种会衰减的记忆：带门的线性注意力，"
        "它的B扮演键，C扮演查询。这就是Mamba-2，它的状态空间对偶性，让这个层有两副面孔。<bookmark mark='a'/>把递推展开，每个输出都是前面那些值"
        "的加权和：这正是注意力，只不过查询和键的分数，要再乘上一个掩码L。<bookmark mark='b'/>掩码的第i行第j列，是词元j和词元i之间所有门的乘积："
        "也就是词元j有多少能留到第i步。在门遗忘的地方，从那一行往下，掩码都暗了下去。<bookmark mark='c'/>这个掩码是半可分的，意思不过是："
        "对角线以下的每一块，秩都是1，因为每个元素，都是它所在行的一个数，乘以它所在列的一个数。<bookmark mark='d'/>我们验证过：带掩码的注意力"
        "和递推，结果只差舍入误差。所以，同一个层，写的时候可以作为递推来运行，只用固定大小的内存；训练的时候，又可以作为带掩码的注意力来运行，"
        "用上大块的矩阵乘法。",

    'The line continues. In March 2026':
        "这条线还在延续。2026年3月，阿卡什·拉霍蒂、顾立彬、特里·道和同事们发表了Mamba-3，带来三个来自状态空间思路的想法。"
        "<bookmark mark='a'/>第一，更好的一步：不再只用一步一端的输入，而是用两端，也就是梯形；再加上一个学出来的偏置，他们就能去掉这个家族每一层"
        "前面都有的那个短卷积。<bookmark mark='b'/>第二，复数值的状态，它既能缩小，也能旋转：就像第6章里δ规则的反射，它让记忆能翻转、能计数，"
        "能追踪奇偶性，而Mamba-2做不到。<bookmark mark='c'/>第三，每一步有多个输入和输出，也就是秩为r的写入：每读一个字节的状态，做更多的运算，"
        "这正合显卡的胃口，而生成并不会变慢。<bookmark mark='d'/>他们报告，用一半的状态就达到Mamba-2的困惑度；在15亿参数时，还略领先于"
        "Gated DeltaNet。",

    # ------------------------------------------------------------------ TTT
    'Chapter ten. A memory that learns.':
        '第10章。会学习的记忆。',

    'Chapter five ended with a thought':
        "第5章结尾留下一个想法：δ规则是一步梯度下降，所以这份记忆是一个模型，一边读文本，一边在文本上训练。2024年，孙宇和同事们把这句话"
        "当了真。<bookmark mark='a'/>隐状态是一个小模型的权重W，读一个词元，就是在由这个词元构造的损失上训练一步：从它的一个学出来的视角，"
        "重建另一个视角。<bookmark mark='b'/>如果这个模型是线性的，那又是δ规则：TTT-Linear。<bookmark mark='c'/>但它可以是任何能训练的东西，"
        "比如一个两层网络，TTT-MLP，它的权重是比一个矩阵更丰富的记忆。<bookmark mark='d'/>他们报告说，从1.25亿到13亿参数，上下文超过一万六千个"
        "词元以后，Mamba就不再进步，而他们的层还在继续进步。",

    '"We can test that on a toy.':
        "我们可以在一个玩具问题上检验。每段序列都有它自己的隐藏规则，一个随机的小网络，把一个键变成一个值；记忆一次读一对，每读一对就走一步"
        "梯度下降。<bookmark mark='a'/>每读16对，我们就拿它从没见过的键、按同一条规则去问它。它没法去查找：它必须已经学会了这条规则。"
        "<bookmark mark='b'/>{verdict}",

    "f'The linear memory levels off at":
        "线性记忆停在{el:.2f}：对一条弯曲的规则，一个矩阵最多只能做到这样。两层的记忆还在继续学，降到了{em:.2f}：更丰富的记忆，用了{pm // pl}倍的数。",

    "f'The two-layer memory ends a little lower":
        "两层的记忆最后低一点：{em:.2f}，矩阵是{el:.2f}：更丰富的记忆有帮助，在这里不多，用了{pm // pl}倍的数。",

    "f'The two-layer memory does no better here":
        "两层的记忆在这里并没有更好：{em:.2f}，矩阵是{el:.2f}，而它用了{pm // pl}倍的数。",

    '"Ali Behrouz, Peilin Zhong and Vahab Mirrokni':
        "谷歌的阿里·贝鲁兹、钟沛林和瓦哈卜·米罗克尼，在2025年之交把这个想法做成了Titans。他们的记忆是一个小的深层网络，放在一个普通注意力"
        "窗口的旁边，他们把梯度叫作意外度：<bookmark mark='a'/>记忆错得离谱的词元，会产生很大的梯度，被狠狠地写进去。<bookmark mark='b'/>"
        "他们加上了动量，让一次意外在之后几步里还继续被写入；还加了一个遗忘门，也就是一个权重衰减，把旧的记忆清掉。<bookmark mark='c'/>"
        "这又是我们的玩具问题，只是隐藏规则在中途换成了一条新的。规则一变，意外度就跳了起来。<bookmark mark='d'/>{verdict}"
        "<bookmark mark='e'/>论文报告说，在超过两百万个词元上也通过了大海捞针测试；这一点我们在这里没法验证。",

    "f'In the thirty-two pairs after the change, momentum":
        "在规则改变后的32对里，动量和遗忘适应得更快：平均误差{at_:.2f}，而不用它们是{ap:.2f}。",

    'f"In the thirty-two pairs after the change, the two':
        "在规则改变后的32对里，两者适应得差不多快：{at_:.2f}对{ap:.2f}：在这个玩具问题里，动量和遗忘没有帮上忙。",

    'Step back, and every memory in this part is a learner.':
        "退一步看，这一部分的每一种记忆，都是一个学习者。<bookmark mark='a'/>线性注意力在一个损失上走一步梯度，这个损失奖励记忆和值相一致："
        "它只会加。衰减再加上权重衰减。<bookmark mark='b'/>δ规则在平方误差上走一步，所以它会纠正；门控δ规则在这之上再加上权重衰减。"
        "<bookmark mark='c'/>Titans和TTT把记忆换成更深的模型，再用更好的优化器。<bookmark mark='d'/>而softmax注意力什么都不训练：它留着每一对，"
        "用它们的值的加权平均来回答，也就是第13部分的核回归，代价是一份不断变大的缓存。这些里面，哪些真的能查找东西？那是下一章。",

    # ------------------------------------------------------------------ Recall
    'Chapter eleven. A recall test.':
        '第11章。回忆测试。',

    'f"Here\'s a test of pure memory, multi-query associative recall':
        "这里有一道纯考记忆的题，多查询联想回忆，来自斯坦福的西姆兰·阿罗拉和同事们：一串键，每个键后面跟着它的值；<bookmark mark='a'/>"
        "然后，其中一些键按新的顺序再出现一次，模型必须答出它们的值。要从一篇文档很靠前的地方引用一个名字或一个数字，模型需要的就是这种本领；"
        "2023年，他们发现注意力和那些快速记忆之间的质量差距，大部分都能用它来解释。<bookmark mark='b'/>我们在它上面训练了六种两层的小模型："
        "softmax注意力，线性注意力，一个Mamba-2式的选择性状态空间模型，δ规则，门控δ规则，以及一个混合模型：下面一层门控δ，上面一层注意力。"
        "<bookmark mark='c'/>列表有{N}对，键的长度从{dks[0]}到{dks[-1]}个数，所以固定的记忆从远远不够到足够大都有；权重一样多，"
        "最多差几个门，训练步数一样，都是{steps:,}步，每种{len(m['seeds'])}个随机种子。",

    "'Here is training, replayed, for keys of '":
        "这是训练过程的回放，键的长度是{dk}个数。左边，是一张模型从没训练过的列表：每个方块是它的一个答案，答对就亮起来。右边，是在一批固定的"
        "数据上答对的比例。<bookmark mark='a'/>一开始，每个模型都在猜。然后，它们一个接一个地发现了窍门：找到这个键前面出现过的地方，把紧跟在"
        "后面的东西抄过来。<bookmark mark='b'/>{v1}<bookmark mark='c'/>{v2}<bookmark mark='d'/>{v3}",

    "f'The first to get half of this list right":
        "最先在这张列表上答对一半的是{nm[quick[0]]}，在第{first[quick[0]]:,}步；",

    'None of them gets half of this list right;':
        '没有一个在这张列表上答对一半；',

    "f'the last, {nm[quick[-1]]}":
        "最后一个是{nm[quick[-1]]}，在第{first[quick[-1]]:,}步。",

    "f'{len(never)} of the six never get there":
        "六个里有{len(never)}个，在这次训练里始终没做到。",

    "f'One, {nm[never[0]]}, never gets there":
        "有一个，{nm[never[0]]}，在这次训练里始终没做到。",

    '"And here is every run at the end':
        "这是每一次训练最后的结果，横轴是键的长度，它决定了固定记忆的大小。<bookmark mark='a'/>{v_small}<bookmark mark='b'/>{v_big}"
        "<bookmark mark='c'/>{v_seed}",

    "f'With keys of {dks[0]} numbers, softmax attention gets":
        "键只有{dks[0]}个数时，softmax注意力得到{100 * mean['softmax'][0]:.0f}%，混合模型{100 * mean['hybrid'][0]:.0f}%；固定的记忆里，"
        "{nm[[k for k in small if k not in ('softmax', 'hybrid')][0]]}最好，"
        "{100 * max((mean[k][0] for k in mix if k not in ('softmax', 'hybrid'))):.0f}%。",

    "f'With keys of {dks[-1]}, the fixed memories":
        "键有{dks[-1]}个数时，会遗忘或会纠正的固定记忆达到{100 * min((mean[k][-1] for k in fixed)):.0f}%到"
        "{100 * max((mean[k][-1] for k in fixed)):.0f}%，而只会加的线性注意力，停在{100 * lin_last:.0f}%。",

    'f"The seeds disagree by up to':
        "不同的随机种子之间，最多相差{100 * spread:.0f}个百分点：这些小模型有时找到了窍门，有时没找到。",

    "f'The seeds agree to within":
        "不同的随机种子之间，相差不到{100 * spread:.0f}个百分点。",

    'f"Why? Count what each memory holds':
        "为什么？数一数每种记忆读完这张列表以后存了多少东西。<bookmark mark='a'/>键有{dks[0]}个数的固定记忆，每层存{state[0]:,}个数，"
        "不管文本有多长都一样。注意力的缓存，存着它见过的每一个键和值，这里是{cache[0]:,}个，文本长一千倍就是{cache[0] * 1000:,}个。"
        "<bookmark mark='b'/>精确的回忆，是注意力用不断变大的缓存换来的；固定的记忆要么足够大，要么知道该覆盖什么。{v}",

    "f'With the smallest keys, adding one attention layer":
        "键最小的时候，在一层门控δ上面加一层注意力，就把回忆率从{100 * gd:.0f}%提到了{100 * hy:.0f}%。这就是混合架构的理由。",

    "f'Here, though, one attention layer above a gated delta layer":
        "不过在这里，键最小的时候，在一层门控δ上面加一层注意力并没有帮上忙：{100 * hy:.0f}%，而两层门控δ是{100 * gd:.0f}%。它的注意力，"
        "键也一样小；两层注意力得到了{100 * sm:.0f}%。混合架构的理由在于代价：只在少数几层里做精确的查找，也只在这几层里付缓存的代价。",

    # ------------------------------------------------------------------ Hybrid
    'Chapter twelve. Hybrids.':
        '第12章。混合架构。',

    'Fixed-size memories are cheap, but they forget':
        "固定大小的记忆很便宜，但会遗忘；注意力能把一切都记得分毫不差，只是要付出代价。所以，最新的模型把两者混在一起。<bookmark mark='a'/>"
        "2024年，AI21的Jamba每8层里放1层注意力，其余都是Mamba；2025年1月的MiniMax-01也是这样，用的是它的闪电注意力。<bookmark mark='b'/>"
        "英伟达的Nemotron-H，在28个混合层里留了4层注意力，IBM的Granite 4.0是10层里留1层。<bookmark mark='c'/>2025年秋天的Qwen3-Next和"
        "Kimi Linear，每4层里用1层注意力，另外3层跑的是门控δ规则。<bookmark mark='d'/>到了2026年，这种布局来到了前沿的开放模型里：Qwen3.5，"
        "从8亿到将近4000亿参数，还有Kimi K3，2.8万亿参数，93层里有24层注意力。<bookmark mark='e'/>快速的那些层，花很小的代价，记住长文本的大意；"
        "少数几层注意力，在需要的时候，去查找精确的细节。",

    '"We built a small one.':
        "我们造了一个小的。在三十部小说上训练两个模型，宽度、深度、MLP、数据和步数都一样，每个三个随机种子。<bookmark mark='a'/>一个是普通的"
        "Transformer，有四层注意力。另一个像Kimi Linear那样，先是三层门控δ，再是一层完全没有位置编码的注意力：顺序由下面的循环层来携带。"
        "<bookmark mark='b'/>这是它们的训练过程。<bookmark mark='c'/>{v}<bookmark mark='e'/>{vs}<bookmark mark='d'/>在256个词元的窗口里，"
        "Transformer的缓存本来就不大；混合架构的优势，是为长文本准备的。那是下一章的内容。",

    'f"The hybrid ends ahead:':
        "最后混合模型领先：在计分板那段文字上，每个字符{bh.mean():.3f}比特，Transformer是{bt.mean():.3f}。",

    'f"The transformer ends ahead:':
        "最后Transformer领先：在计分板那段文字上，每个字符{bt.mean():.3f}比特，混合模型是{bh.mean():.3f}。",

    "f'They end level:":
        "最后两者打平：Transformer每个字符{bt.mean():.3f}比特，混合模型{bh.mean():.3f}。",

    "The two sets of seeds don't overlap.":
        '两组随机种子的结果没有重叠。',

    'The seeds overlap: the difference is within their spread.':
        '随机种子的结果有重叠：差别在它们的波动范围之内。',

    'f"And here is the hybrid\'s writing as it learns':
        "这是混合模型在学习过程中写出的东西，在训练的四个时刻，接着同一个开头往下写。<bookmark mark='a'/>第{snaps[picks[0]]}步，一片噪声。"
        "<bookmark mark='b'/>然后是词，<bookmark mark='c'/>再然后是有点像句子的东西：<bookmark mark='d'/>"
        "{int(r['hybrid_params']) / 1000000.0:.1f}百万个权重、{int(r['tokens']) / 1000000.0:.1f}百万个词元，大概也就能走到这里。",

    'f"The memory bill shows why.':
        "看一看这份内存账单，就明白为什么了。拿一段12.8万个词元的对话来说，<bookmark mark='a'/>Llama 3.1的分组查询缓存，要占"
        "{ll / 2 ** 30:.0f}GB；DeepSeek-V3的潜在缓存，是{np.asarray(k['total_mla'])[i128] / 2 ** 30:.1f}GB；Qwen3-Next只在4分之1的层里用注意力，"
        "只要{q / 2 ** 30:.1f}GB，大约比Llama少{ll / q:.0f}倍。它那些δ规则层，只多出{k['qwen_state'] / 2 ** 20:.0f}MB的状态，而且不管对话有多长，"
        "都是这么多。",

    # ------------------------------------------------------------------ LongContext
    'Chapter thirteen. How long is a context, really?':
        '第13章。上下文到底有多长？',

    'How do you test a long context?':
        "怎样测试一个长上下文？2023年11月，格雷格·卡姆拉特把一句话，也就是那根针，藏在一大摞文章里选定的深度，再问模型这句话的内容。"
        "<bookmark mark='a'/>改变深度和长度，按它答没答对给每一格上色，就得到了大海捞针图，如今每个长上下文模型都会拿出这张图。"
        "<bookmark mark='b'/>弱一些的模型，在长文本的中间会暗下去：这就是纳尔逊·刘和同事们发现的“迷失在中间”效应，第29部分会再讲到它。"
        "<bookmark mark='c'/>可是大海捞针是一道容易的题：问题重复了针里的词，所以一个会匹配词语的注意力头就能找到它。",

    'So the tests got harder.':
        "于是测试变难了。<bookmark mark='a'/>2024年，英伟达的谢承平和同事们做了RULER：一次藏好几根针，把值沿着一串变量传下去，数出最常见的词，"
        "还有关于文本的问题。在17个号称至少支持3.2万个词元的模型里，到了3.2万个词元，只有一半还表现良好。<bookmark mark='b'/>2025年，NoLiMa"
        "去掉了字面上的匹配：针和问题之间没有一个共同的词。到了3.2万个词元，13个模型里有11个跌到了它们短文本成绩的一半以下。"
        "<bookmark mark='c'/>而Chroma关于上下文腐烂的报告发现，它试过的全部18个模型，输入越长就越不可靠，哪怕是简单的任务。"
        "<bookmark mark='d'/>模型能接受的长度，并不是它能用上的长度。",

    'f"We can run a small RULER of our own.':
        "我们可以自己做一个小RULER。用上一章的四种两层模型，在{T0}个词元上训练三个任务：在一串填充词里找一根针；在四根针里找出被问到的那一根；"
        "以及顺着一条链走下去：A是7，B等于A，C等于B，C是多少？<bookmark mark='a'/>然后在更长的串上测试它们，一直到{Ls[-1]:,}个词元。"
        "<bookmark mark='b'/>{v1}<bookmark mark='c'/>{v2}<bookmark mark='d'/>{v3}",

    "f'At the length they trained on, averaged":
        "在它们训练时的长度上，三个任务平均下来，softmax注意力得到{a_['softmax']:.0f}%，Mamba-2式的模型{a_['mamba2']:.0f}%，门控δ规则"
        "{a_['gdn']:.0f}%，混合模型{a_['hybrid']:.0f}%。",

    "f'At eight times that length":
        "到了这个长度的八倍，{nm[best_far]}撑得最好，{100 * far[best_far]:.0f}%；{nm[worst_drop]}跌得最多，从{100 * at_train[worst_drop]:.0f}%"
        "跌到{100 * far[worst_drop]:.0f}%。",

    "f'The hardest task, even at the training length":
        "最难的任务，即使在训练长度上，也是{TASK_NAME[tasks[hardest]].replace('$', '')}。",

    '"Our two language models from the last chapter':
        "上一章的两个语言模型，是在256个词元的窗口上训练的。过了尽头会怎样？<bookmark mark='a'/>这是在一段一千个词元长的留出文本上，一次读完时，"
        "每个位置的损失。{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}",

    'f"Past 256, the transformer\'s loss climbs':
        "过了256，Transformer的损失往上爬，从{near_t:.2f}奈特到{far_t:.2f}奈特：这些旋转位置它从没训练过。",

    'f"Past 256, the transformer\'s loss barely moves':
        "过了256，Transformer的损失几乎不动，从{near_t:.2f}到{far_t:.2f}。",

    'f"The hybrid\'s stays near where it was':
        "混合模型的损失基本停在原处，从{near_h:.2f}到{far_h:.2f}：它的注意力没有可以用完的位置。",

    'f"The hybrid\'s climbs too':
        "混合模型的损失也往上爬，从{near_h:.2f}到{far_h:.2f}。",

    'But neither can find a needle':
        "可是两个模型都找不到针：给它们24个随机词元，接着一段小说，再来同样的24个词元，即使只隔16个词元，两个都预测不出重复的部分。"
        "这么小、训练这么短的模型，从没形成第13部分讲的归纳头；所以前面的测试，用的是专门为这项任务训练的小模型。",

    "f'And in the copy test, twenty-four random tokens":
        "在抄写测试里，24个随机词元在一段小说之后重复出现，两份副本相隔{r['gaps'][0]}个词元时，Transformer预测对重复部分的"
        "{100 * ct.mean(0)[0]:.0f}%，混合模型{100 * chy.mean(0)[0]:.0f}%。",

    'Where does that leave the frontier?':
        "那前沿又怎样呢？<bookmark mark='a'/>2024年，谷歌的Gemini 1.5提供了一百万个词元，并报告在多达一千万个词元里找到了针。"
        "<bookmark mark='b'/>Kimi Linear的报告，为混合架构在长文本上的表现给出了证据：在12.8万个词元的RULER上，84.3分，同样方式训练的"
        "完整注意力是81.3分；而它的注意力层改用旋转位置时，只有78.8分。<bookmark mark='c'/>在OpenAI更难的MRCR测试里，八个相似的请求藏在"
        "一百万个词元中，Anthropic在2026年2月报告，Claude Opus 4.6找对了76%，而它的前一代Sonnet 4.5只有18.5%。<bookmark mark='d'/>"
        "DeepSeek-V4则通过压缩键和值来读一百万个词元，压缩比分别是4比1和128比1，再在其中挑选：这是第16部分的主题。这些都是各家自己的测量。",

    # ------------------------------------------------------------------ Retrieval
    'Chapter fourteen. Retrieval as memory.':
        '第14章。把检索当作记忆。',

    'Every memory so far lives inside the model.':
        "到目前为止的每一种记忆，都住在模型里面。另一条路，是把记忆放在模型之外，像一座图书馆。<bookmark mark='a'/>把一个大文集里的每一段"
        "都变成一个向量，也就是嵌入，问题也变成一个；离问题最近的那些段落，就是要读的。<bookmark mark='b'/>2020年，弗拉基米尔·卡尔普欣和同事们"
        "训练了两个编码器，让问题落在它们的答案附近，这叫稠密段落检索；REALM把检索器和语言模型一起训练；帕特里克·刘易斯和同事们给这套做法"
        "起了名字：检索增强生成，找到段落，放进上下文，再生成。<bookmark mark='c'/>如今大多数聊天助手就是这样搜索文档的，而这份记忆从来不需要"
        "塞进上下文窗口。",

    'f"A language model can retrieve too':
        "语言模型也可以检索，一次一个词元。2020年，乌尔瓦希·坎德尔瓦尔和同事们，把训练文本的每个词元都存成一对：模型在它前面一刻的隐状态，"
        "和这个词元本身。<bookmark mark='a'/>测试时，找出离当前隐状态最近的那些存储状态，让它们的下一个词元来投票，越近权重越大。再把投票结果和"
        "模型自己的预测混合，记忆占λ这么大的份额。不做任何额外训练，它就让当时最好的模型在维基百科文本上的困惑度降了2.9。<bookmark mark='b'/>"
        "我们为本系列的模型也做了一个：三十部小说的全部{n_all / 1000000.0:.1f}百万个词元，都存成隐状态。<bookmark mark='c'/>这是计分板那段文字里，"
        "它帮得最多的那个词元。模型自己给正确的下一个词元{100 * float(ex['p_lm']):.1f}%；<bookmark mark='d'/>最近的那些存储状态，来自小说里"
        "看起来一样的地方，给它投了{100 * float(ex['p_knn']):.0f}%的票。",

    '"How much does it help?':
        "它帮了多少？<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}这段文字，《马耳他之鹰》的第2章，不在那三十部小说里，所以记忆没法"
        "直接把它想起来：它帮的是小说之间共通的东西。",

    "f'On the passage, the model alone scores {base:.3f} bits per character. With":
        "在这段文字上，模型自己每个字符{base:.3f}比特。加上关于小说的记忆，以λ等于{lam:g}混合进去，λ是在留出的小说文本上选的，从没在这段文字"
        "上选过，得到{float(full['bits']):.3f}：少了{gain:.3f}比特，也就是{100 * rel:.1f}%。",

    "f'On the passage, the model alone scores {base:.3f} bits per character, and":
        "在这段文字上，模型自己每个字符{base:.3f}比特，加上记忆是{float(full['bits']):.3f}：没有真正的收获。",

    "f'And it takes a big memory:":
        "而且记忆要足够大：只有{keys[0] / 1000000.0:.2f}百万个存储状态时，投票最好的份额是{lam0:g}，分数{bits[0]:.3f}；只有用上全部"
        "{keys[-1] / 1000000.0:.1f}百万个，才达到{bits[-1]:.3f}。",

    "f'A bigger memory hardly helps here":
        "在这里，更大的记忆几乎没有帮助：{keys[0] / 1000000.0:.2f}百万个存储状态时{bits[0]:.3f}，{keys[-1] / 1000000.0:.1f}百万个时"
        "{bits[-1]:.3f}。",

    '"Where does the memory of the novels help?':
        "关于小说的记忆，在哪里帮了忙？<bookmark mark='a'/>这些是这段文字里，它省下最多比特的词元。{v}<bookmark mark='b'/>{v2}",

    "f'Many are names and capitals":
        "很多是名字和大写的词，比如{names[0]}：这份记忆见过小说是怎样用它们的。",

    'Mostly they finish a word that has already begun':
        '它们大多是把一个已经开了头的词补完，就像例子里那样：这些补全，小说里见过很多次。',

    'f"Edouard Grave and colleagues had done the same in 2017':
        "2017年，爱德华·格拉夫和同事们，用已经读过的文本做过同样的事，叫作连续缓存。我们这段文字远远超过模型256个词元的窗口，用它自己更早的"
        "隐状态做一份记忆，把分数从{base:.3f}降到了{float(sc['bits']):.3f}：一页之前出现过的名字，又被找了回来。",

    "f'Edouard Grave and colleagues had done the same in 2017 with the text read so far, a continuous cache; for":
        "2017年，爱德华·格拉夫和同事们，用已经读过的文本做过同样的事，叫作连续缓存；对我们这段文字，它得到{float(sc['bits']):.3f}，"
        "而不用它是{base:.3f}，帮助不大。",

    '"Retrieval scales too:':
        "检索也能扩大规模：2021年，DeepMind的RETRO从一个两万亿词元的图书馆里查找文本块，只用二十五分之一的参数，就在Pile上接近了GPT-3。"
        "<bookmark mark='a'/>这是计分板。{v}",

    'f"Our small hybrid and transformer':
        "我们的小混合模型和小Transformer，权重比本系列的模型少{rp:.0f}倍，训练词元少{rt:.0f}倍，分别得到{hy['bits']:.2f}和{tf['bits']:.2f}。"
        "本系列的模型加上关于小说的记忆，达到{kn['bits']:.3f}；加上关于这段文字已读部分的记忆，是{sc['bits']:.3f}；而它自己是{base['bits']:.3f}。",

    # ------------------------------------------------------------------ Frontier
    'Chapter fifteen. The frontier, late 2026.':
        '第15章。2026年末的前沿。',

    'Two years ago, a fixed-size memory in a frontier model':
        "两年前，前沿模型里用固定大小的记忆，还只是一种实验。<bookmark mark='a'/>2025年1月，MiniMax-01在每8层里的7层用上了闪电注意力，"
        "能读多达四百万个词元；4月，英伟达的Nemotron-H在一叠Mamba-2里只留了几层注意力。<bookmark mark='b'/>那年秋天，门控δ规则来了："
        "Qwen3-Next和Kimi Linear，每4层里有3层。<bookmark mark='c'/>接着，MiniMax的下一个模型回到了完整注意力，原因我们马上就看。"
        "<bookmark mark='d'/>英伟达的Nemotron 3把Mamba-2和专家混合起来，支持一百万个词元；Qwen3.5让门控δ混合架构成了整个家族的设计；"
        "Mamba-3则把状态空间这条线又往前推了一步。<bookmark mark='e'/>DeepSeek-V4走了另一条路，改为压缩缓存；2026年7月，Kimi K3，"
        "2.8万亿个权重，在它93层里的69层用上了Kimi Delta Attention。",

    "In October 2025 Haohai Sun":
        "2025年10月，负责MiniMax-M2预训练的孙浩海，解释了这次回头。<bookmark mark='a'/>他们的混合模型在常用的基准上追平了完整注意力，"
        "可是规模一大，在复杂的多步推理上就显出了明显的不足。<bookmark mark='b'/>他写道，更深层的问题在于评测：能暴露这种差距的测试很贵，"
        "而小规模的实验未必能预测大规模的结果。<bookmark mark='c'/>而且工具还很年轻：线性层常常受限于内存带宽，而那些为缓存打造的服务技巧，"
        "比如前缀缓存和推测解码，都得重新做。<bookmark mark='d'/>一个滑动窗口的混合模型，上下文越长表现越差；他们发现，负责检索和抄写的那些头，"
        "在预训练早期就形成了，之后很难再加进去。<bookmark mark='e'/>这就是我们的回忆测试，放到了前沿实验室的规模上。Moonshot和Qwen押了"
        "另一边；两边的赌注，都已经投入生产。",

    'Meanwhile the people who build agents':
        "与此同时，做智能体的人，用实践的方式学到了前两章的教训。模型的窗口是一份预算，每多花一个词元，都会稀释它的注意力；Anthropic在2025年9月的"
        "指南里，把这种衰退叫作上下文腐烂。<bookmark mark='a'/>所以，上下文工程要决定放进去什么：指令和工具，检索找到的文档，<bookmark mark='b'/>"
        "窗口满了时压缩成一份摘要的对话历史，只有最近几轮保持完整。<bookmark mark='c'/>放不下的，就写进智能体自己的笔记，以后再读回来，"
        "<bookmark mark='d'/>或者交给子智能体，它们在干净的窗口里工作，再把一份摘要汇报回来。这就是这一部分讲的记忆，只不过是手工管理的："
        "一份会被挤出、被压缩、被检索的缓存。",

    'So the questions are open.':
        "所以，这些问题都还悬而未决。<bookmark mark='a'/>一个模型需要多少注意力：每4层一层，每8层一层，还是一层都不要？<bookmark mark='b'/>"
        "一份固定的记忆要多大，又该怎样随模型增长？<bookmark mark='c'/>一份记忆，能不能像注意力学会看哪里那样，学会留下什么？<bookmark mark='d'/>"
        "我们又该怎样衡量，一个模型拿一百万个词元做了什么？",

    # ------------------------------------------------------------------ Outro
    '"Let\'s take stock.':
        "我们来盘点一下。注意力的记忆就是它的缓存；模型让键和值共用，或者把它们压进一个潜在向量，来缩小它；服务器也可以挤掉其中一部分，"
        "只要留住汇点。去掉softmax，注意力就变成在一个矩阵上的递推，也就是1992年的快权重，用外积来写，用键来读；只做加法会让它充满串扰，"
        "衰减会遗忘，而δ规则，一步最小二乘，会纠正。结合律的扫描，或者WY形式的分块，让这样的递推能并行训练。状态空间模型从另一边走来：HiPPO"
        "对整段信号的记忆，S4的卷积，再由Mamba让它们学会选择。<bookmark mark='a'/>{r1}<bookmark mark='b'/>{r2}",

    "f'In our recall test, fixed memories needed room or a way to overwrite, and":
        "在我们的回忆测试里，固定的记忆需要足够的空间，或者一种覆盖的办法；记忆最小的时候，在上面加一层注意力，就把回忆率从{100 * gd:.0f}%提到了"
        "{100 * hy:.0f}%；最新的模型就是这样搭起来的。",

    "f'In our recall test, fixed memories needed room or a way to overwrite;":
        "在我们的回忆测试里，固定的记忆需要足够的空间，或者一种覆盖的办法；记忆最小的时候，在上面加一层注意力，得到{100 * hy:.0f}%，"
        "不加是{100 * gd:.0f}%。",

    'f"And a memory can live outside the model:':
        "记忆也可以住在模型之外：来自那些小说的最近邻投票，让我们模型的分数每个字符少了{gain:.3f}比特。",

    'And a memory can live outside the model, though':
        '记忆也可以住在模型之外，不过对我们这段文字，来自小说的投票没帮上多少。',

    'All of this comes back.':
        "这些都会再回来。挑选要读哪些词元，也就是稀疏注意力和DeepSeek的索引器，是第16部分。快速地提供缓存，是第19部分。δ规则的反射和状态追踪，"
        "会在第28部分和推理相遇。第29部分的智能体，用笔记、压缩和检索，手工管理它们的记忆。第30部分则要去找，一个训练好的模型把它的事实"
        "存在哪里。",

    'Here are six problems':
        "这里有六道习题，从给一份缓存算价钱，到一次最近邻投票的代价。在这里暂停，把它们做一做；完整的解答在这一部分的笔记里。",

    'Next time: sparsity.':
        "下一次：稀疏性。最大的模型并不是每个词元都用上全部的权重：一个路由器，把每个词元送到几百个专家中的少数几个那里，而注意力也可以只读"
        "要紧的词元。<bookmark mark='a'/>该怎样路由，又怎样让每个专家都有活干？",

    "Songlin Yang's papers and blog":
        "关于线性注意力和δ规则，杨松琳的论文和博客，是最好的入门读物；关于状态空间模型，看顾立彬的博士论文。感谢观看，我们第16部分再见。",
}

PHRASES = {
    # spliced-in English values
    'softmax': 'softmax注意力',
    'linear': '线性注意力',
    'Mamba-2': 'Mamba-2式的模型',
    'delta': 'δ规则',
    'gated delta': '门控δ规则',
    'hybrid': '混合模型',
    'the plain window': '普通窗口',
    'sinks plus a window': '汇点加窗口',
    'the heavy hitters': '重量级词元',
    'one needle': '一根针',
    'one of four needles': '四根针里的一根',
    'a chain of three names': '一条三个名字的链',
}
