"""Chinese narration for ai30: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第30部分：模型内部'

CHAPTERS = {
    'Hook': '它在想什么？',
    'History': '1. 我们是怎么走到这里的',
    'Probes': '2. 它知道什么？',
    'Lens': '3. 读出流动中的残差流',
    'Patching': '4. 是原因，不是相关',
    'Induction': '5. 一个归纳回路，从头到尾',
    'Superposition': '6. 想法比维度多',
    'Phase': '7. 相图',
    'SAE': '8. 把特征拆开',
    'Dicts': '9. 更好的字典',
    'Splitting': '10. 分裂与吸收',
    'Graphs': '11. 转码器与归因图',
    'Diffing': '12. 微调改变了什么',
    'Steering': '13. 伸手进去',
    'Grok': '14. 顿悟的机制',
    'Faithful': '15. 思维链说的是真话吗？',
    'Frontier': '16. 前沿：2025到2026年',
    'Disagree': '17. 这个领域在哪里有分歧',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    'Part by part, we\'ve built every piece of these models ourselves.':
        "一部分接一部分，这些模型的每个零件，我们都亲手搭过。里面的每一个数字，我们都知道。可我们还是说不出，它在想什么。<bookmark mark='a'/>这是我们的Transformer在读测试段落里的一行：对每个字符，它在第二个块之后带着的128个数。每一个数都一直在忙，可没有哪一个数，单独拿出来有什么意义。<bookmark mark='b'/>这一部分，讲的就是怎么读懂它们。<bookmark mark='c'/>换到合适的基底里重写，画面就变了：每个字符上，只有少数几个特征亮着，也就是模型在追踪的想法，而每一个，结果都有意义。",

    'f"Take one character. <bookmark mark=\'a\'/> Its hundred':
        "拿一个字符来看。<bookmark mark='a'/>它那128个缠在一起的数，变成了512个特征里的{int((f > 0).sum())}个。<bookmark mark='f'/>一个特征，就是模型追踪的一个想法，比如“在引号里面”，它以一个方向的形式，存在这些数当中。向量朝那个方向指了多远，也就是它在这个方向上的投影，就是这个特征亮得有多强。",

    'This is Part 30 of AI, Built: inside the model.':
        "这里是《人工智能，从零搭建》第30部分：模型内部。<bookmark mark='a'/>先讲这个领域是怎么走到今天的，从显著图到回路。<bookmark mark='b'/>然后讲怎么从模型里把信息读出来，以及其中的陷阱；<bookmark mark='c'/>再讲怎么找出真正导致某个行为的原因，一直追到一个完整的回路。<bookmark mark='d'/>然后讲这些数为什么缠在一起，以及把它们解开的字典；<bookmark mark='e'/>把一次预测从输入追到输出，把一个模型和它的微调版本做比较，还有引导。<bookmark mark='f'/>最后讲：顿悟是怎么回事，思维链说的是不是真话，以及到2026年，这个领域走到了哪里，又在争论什么。每个实验都在这台电脑上跑，大多数用的是本系列自己的模型。",

    # ---------------------------------------------------------------- History
    'Chapter one. How we got here.':
        '第1章。我们是怎么走到这里的。',

    'f"The first question people asked of a trained network was the simplest':
        "人们对一个训练好的网络提出的第一个问题，也是最简单的：输入里哪些部分重要？<bookmark mark='a'/>2013年，卡伦·西蒙尼扬、安德烈亚·韦达尔迪和安德鲁·齐瑟曼，对类别得分求它相对于像素的梯度：这就是显著图。这里是我们的字符Transformer的显著图，它正要在“she sai”后面写出“{s['target']}”。<bookmark mark='b'/>每根柱子是梯度乘以输入，是对每个字符贡献的一阶估计。<bookmark mark='c'/>一年后，马修·泽勒和罗布·弗格斯给出了一个更直接的测试：一次遮住一个字符，看得分掉了多少。<bookmark mark='d'/>如果两者都说了真话，它们应该一致。按排名比较，它们{agree}：这里的相关系数是{rho:.2f}，再算24个预测，平均是{rho24:.2f}。梯度只是局部的斜率；网络并不是一条直线。",

    '"Worse, a picture that looks sensible can explain nothing.':
        "更糟的是，一张看上去合理的图，可能什么也没解释。<bookmark mark='a'/>2018年，朱利叶斯·阿德巴约和同事把一个网络的权重从顶层开始一层层重新随机化，结果发现，一些流行的显著图方法几乎没变：它们显示的是输入的边缘，而不是网络的理由。<bookmark mark='b'/>在我们的模型上也做这个测试。重新随机化第4块，然后第3和第4块，一直到嵌入层，再把每张图和训练好的那张比较。{verdict}",

    'f"<bookmark mark=\'c\'/> Ours passes:':
        "<bookmark mark='c'/>我们的模型通过了：到最后，相关系数是{rho[-1]:.2f}，在另外24个预测上平均是{rr:.2f}。这张图确实取决于网络学到了什么。但通过了合理性检查，并不等于是对的。",

    'f"<bookmark mark=\'c\'/> Ours keeps a correlation':
        "<bookmark mark='c'/>即使一切都随机了，我们的模型还保留着{rho[-1]:.2f}的相关系数：这张图大半讲的是输入，而不是网络。",

    'So the question moved from which inputs to what the parts of a network are for.':
        "于是问题从“哪些输入重要”，转到了“网络的各个部分是干什么的”。<bookmark mark='a'/>2015年，亚历山大·莫尔德温采夫、克里斯·奥拉和迈克·泰卡让梯度反过来走，改变一张图像去激发某一层，DeepDream那些长满狗的云就传遍了世界。<bookmark mark='b'/>2017年，戴维·鲍的“网络解剖”把每个单元和带标签的概念逐一打分，找到了对应台灯的单元，也找到了对应狗的单元。<bookmark mark='c'/>同一年，奥拉、莫尔德温采夫和路德维希·舒伯特在在线期刊Distill上，把这个技巧做成了一门学问：特征可视化，也就是优化一个输入，直到某个神经元被激发。<bookmark mark='d'/>一年后，他们把它和归因结合起来：网络看到了什么，又是在哪里看到的。",

    'In 2020 the work found its programme.':
        "2020年，这项工作有了自己的纲领。奥拉和同事的《放大》提出了三个推测性的主张。<bookmark mark='a'/>特征是网络的基本单元；特征通过权重连成回路；同样的特征和回路，会出现在不同的模型里。他们在一个视觉网络里，一根线一根线地追出了曲线检测器。<bookmark mark='b'/>接着，这套纲领转向了语言。2021年，有了CLIP里的多模态神经元，还有一套关于Transformer回路的数学框架；<bookmark mark='c'/>2022年，有了归纳头，有了GPT-2 small里一个由26个头组成的回路，还有叠加的玩具模型，它解释了为什么单个神经元很少只表示一件事。<bookmark mark='d'/>然后，稀疏字典把神经元拆成了特征，先是在一个单层模型里，然后在Claude 3 Sonnet里成百万地拆；2025年，归因图追踪了一个生产级模型的计算过程。这一部分，就在我们自己的模型上，把这条路走一遍。",

    # ---------------------------------------------------------------- Probes
    'Chapter two. What does it know?':
        '第2章。它知道什么？',

    'Saliency asks where the model looked.':
        "显著图问的是模型看了哪里。探针问的是它知道什么。<bookmark mark='a'/>拿文本的一个性质来说，比如：读到这个词元时，读者是不是在引号里面。小说模型，也就是第18部分那个六层的Transformer，必须追踪这件事，才知道什么时候该出现后引号。<bookmark mark='b'/>探针就是一个小分类器，训练它从某一层的向量里读出这个性质。如果一个线性探针能做到，说明这个信息就沿着某个方向放在那里。<bookmark mark='c'/>2016年，纪尧姆·阿兰和约书亚·本吉奥在一个网络的每一层上都放了线性探针，探测就成了可解释性的第一匹“老黄牛”。",

    'f"We trained a linear probe on each layer of the novels model':
        "我们在小说模型的每一层上训练了一个线性探针，用了三个种子。<bookmark mark='a'/>总是猜那个更常见的标签，能得{100 * maj:.0f}%。<bookmark mark='b'/>在词元嵌入上，还没有经过任何注意力，探针能到{100 * mean[0]:.0f}%：光看一个词元，说明不了它在什么位置。<bookmark mark='c'/>经过几个块之后，它在第{best}层达到{100 * mean[best]:.0f}%：注意力把引号的信息带了过来，这个状态沿着一个方向写了下来。",

    'f"But who did the work, the model or the probe?':
        "可活到底是谁干的，模型还是探针？<bookmark mark='a'/>约翰·休伊特和Percy Liang的对照任务，直接问的就是这个。给每一种词元随机分配一个标签，比例不变；文本里根本没有这种性质，所以一个探针要是得分很高，只说明它记住了哪些词元带哪个标签。<bookmark mark='b'/>在嵌入层上，对照任务很容易：每个词元都是它自己的向量。我们的线性探针在那里能答对{100 * lc[0]:.0f}%的瞎标签，真任务是{100 * lt[0]:.0f}%。<bookmark mark='p'/>暂停一下，预测一下：一个更强的探针，一个小MLP，能拟合更多东西。它的选择性会更高，还是更低？<bookmark mark='c'/>{verdict}<bookmark mark='c2'/>{verdict2}<bookmark mark='d'/>选择性，也就是真任务减去对照任务，才是报告探针结果时应该附上的数。",

    "f'The MLP probe scores higher on the task,":
        "MLP探针在真任务上得分更高，{100 * mt[best]:.0f}%对{100 * lt[best]:.0f}%，",

    'f"The MLP probe scores {100 * mt[best]:.0f} percent on the task, against':
        "MLP探针在真任务上得{100 * mt[best]:.0f}%，线性探针是{100 * lt[best]:.0f}%，",

    'f"but it also learns the nonsense better:':
        "但它也更会学那些瞎标签：在第{best}层，它的选择性是{100 * sel_m[best]:.0f}个百分点，线性探针是{100 * sel_l[best]:.0f}。探针越强，告诉你的就越是探针自己的事。",

    "f'and here its selectivity holds up too,":
        "而且它的选择性在这里也站得住，{100 * sel_m[best]:.0f}个百分点对{100 * sel_l[best]:.0f}。",

    'f"There is a second trap.':
        "还有第二个陷阱。探针说明信息可以被读出来；并不说明模型自己读了它。<bookmark mark='a'/>亚奈·埃拉扎尔和同事的回答是：把探针读的东西去掉，看模型有没有察觉。我们取第{best}层线性探针的方向，从每个向量里把它投影掉，再让模型跑完剩下的部分。<bookmark mark='b'/>在那些结束引号的词元上，模型原本预测它们要花{b0:.2f}比特。<bookmark mark='c'/>换成去掉十个随机方向，要花{br.mean():.2f}比特。<bookmark mark='d'/>去掉探针的方向，要花{bp:.2f}比特。{verdict}读出来，是相关；改动模型再看结果，才是因果，这是第4章的主题。",

    'The model was using that direction to know a quote was open.':
        '模型确实在用这个方向，来知道引号还开着。',

    'The model hardly cared:':
        '模型几乎不在乎：信息是在那里，但计算走的是别的路，或者还用了别的方向。',

    # ---------------------------------------------------------------- Lens
    'Chapter three. Reading the stream as it flows.':
        '第3章。读出流动中的残差流。',

    'A probe is trained. There is a reading you get for free.':
        "探针需要训练。还有一种读法，是白送的。<bookmark mark='a'/>在Transformer里，每个块读一遍残差流，再把结果加回去。模型的最后一步，把最终的残差流变成预测：先做一次归一化，再乘上反嵌入矩阵。<bookmark mark='b'/>那就把这最后一步提前，用在每个块之后的残差流上，问一问：如果模型在这里停下，它会说什么？<bookmark mark='c'/>2020年，一位化名nostalgebraist的作者在GPT-2上试了这件事，把它叫作logit透镜。",

    'f"Here is the logit lens on the novels model':
        "这是小说模型上的logit透镜，它读的是“it was the best of times, it was the worst of times, it was the age of”。<bookmark mark='a'/>每一行是一层，每一列是一个位置，每一格是透镜对下一个词元的最佳猜测。<bookmark mark='b'/>在最底下，只有嵌入的时候，它多半猜的是常跟在当前词元后面的词元，而且猜得很差。<bookmark mark='c'/>越往上，正确的接续越来越确定；{verdict}预测是一点一点搭起来的，一个块一个块地修正。",

    'f"at the last position, the final guess, \'{final}\', is already the top guess at layer':
        "在最后一个位置，最终的猜测“{final}”，在第{first_right}层就已经排第一了。",

    'f"at the last position, the final guess, \'{final}\', comes out on top only at the last layer.':
        "在最后一个位置，最终的猜测“{final}”，直到最后一层才排到第一。",

    'f"The logit lens assumes every layer speaks the last layer\'s language.':
        "logit透镜假定每一层都说最后一层的语言。其实不完全是：前面几层会把东西存在别的方向上。<bookmark mark='a'/>2023年，诺拉·贝尔罗斯和同事加了一个翻译器：每层一个仿射映射，训练它让透镜对上模型的最终预测。<bookmark mark='b'/>我们给小说模型的每一层都训练了一个。它们一开始就是logit透镜，<bookmark mark='c'/>经过{int(S)}步训练，每一层和最终预测的差距都在下降，最底下降得最多，那里logit透镜偏得最远。",

    'f"Held out, the comparison is clear.':
        "在留出的文本上，对比很清楚。<bookmark mark='a'/>在嵌入层，logit透镜离最终预测有{lk[l0]:.1f}比特，调校透镜是{tk[l0]:.1f}。<bookmark mark='b'/>到一半的高度，是{lk[L // 2]:.1f}对{tk[L // 2]:.1f}。把它们当作下一个词元的预测器来量：用logit透镜读嵌入层，每个词元要{lc[0]:.1f}比特，用调校透镜是{tc[0]:.1f}，模型本身是{lc[-1]:.1f}。<bookmark mark='c'/>透镜终究是一种读法，不是心智：它显示的是，从每一层用线性方式能读出什么，探针的那些注意事项在这里同样适用。",

    # ---------------------------------------------------------------- Patching
    'Chapter four. Cause, not correlation.':
        '第4章。是原因，不是相关。',

    'f"To find what causes a behaviour, you need a behaviour with a known answer.':
        "要找出一个行为的原因，得先有一个答案已知的行为。经典的例子是复制：给模型看同一段文字两遍，第二遍应该很容易，因为模型可以往回看。<bookmark mark='a'/>第13部分的字符Transformer：第一遍每字符{rows[0][1]:.2f}比特，第二遍{rows[0][2]:.2f}。<bookmark mark='b'/>小说模型：每词元{rows[1][1]:.2f}比特，然后是{rows[1][2]:.2f}。{verdict}<bookmark mark='c'/>所以，要找一个可以拆开的回路，我们回到第13部分那个两层、只有注意力的模型：它在随机词元上训练，其中有一段被重复了一遍，复制是唯一值得学的东西。",

    "f'Neither of our models copies.":
        "我们的两个模型都不会复制。奥尔森和同事看到，在他们的模型里，负责复制的头大约在训练到25亿到50亿个词元之间形成；我们的模型只训练了大约{int(round(rows[0][3] / 1000000.0))}百万个词元。",

    'Some copying, but little.':
        '有一点复制，但很少。',

    'f"We retrain it here with Part 13\'s recipe and seed.':
        "我们在这里用第13部分的配方和种子重新训练它。<bookmark mark='a'/>有一阵子，它什么有用的都没学到；然后，突然之间，重复的部分变得容易了，从每词元{cv[0, 1]:.1f}比特降到{cv[-1, 1]:.1f}，而随机的词元还是一样难。<bookmark mark='b'/>看看注意力。在第一层，四个头里有{len(d['prev_set'])}个主要看前一个词元；这是第{hp + 1}个头。<bookmark mark='c'/>在第二层，有{len(d['ind_set'])}个头，在第二遍里的某个词元上，看的是这个词元第一次出现时紧跟在后面的那个词元：也就是要复制的那个。前一词元头，和归纳头。可注意力模式也只是相关。这些头是原因吗？",

    'f"The tool is activation patching.':
        "用的工具是激活修补。<bookmark mark='a'/>让模型跑两次：一次在干净的序列上，带着它的重复；一次在被破坏的序列上，第一遍被换成新的随机词元，于是没东西可复制。然后从被破坏的那次运行里取一个向量，放进干净的那次运行，看第{tgt}个位置上正确的预测损失了多少。凯文·孟和同事就是用修补的方法，找到GPT把事实存在哪里。<bookmark mark='b'/>在每一个位置上替换残差流：在输入处，在两层之间，在输出处。{v_in}<bookmark mark='c'/>在两层之间，是{names(k_mid)}。<bookmark mark='d'/>在输出处，只有第{tgt}个位置本身。关于“复制什么”的信息，从第一遍开始，在其中挪动一步，然后跳到第二遍：这就是回路走的路线。",

    'f"Now the heads: run the clean sequence':
        "再来看头：跑干净的序列，把某一个头的输出换成被破坏那次运行里的。<bookmark mark='a'/>破坏其中一个前一词元头，复制能力损失{100 * p_lo:.0f}%到{100 * p_hi:.0f}%；归纳头是{100 * i_lo:.0f}%到{100 * i_hi:.0f}%。<bookmark mark='b'/>还有一个头也很重要，第一层的第{sh + 1}个头，它主要看词元自己：{100 * nz[0, sh]:.0f}%。其他的头，都不超过{100 * max(others):.0f}%。这个行为由一小组头承担。第5章把它拆开来看。",

    # ---------------------------------------------------------------- Induction
    'Chapter five. An induction circuit, end to end.':
        '第5章。一个归纳回路，从头到尾。',

    'f"Two heads in different layers can only work together through the residual stream':
        "不同层里的两个头，只能通过残差流合作：第一个写，第二个读。<bookmark mark='a'/>可第二个头在三个地方读：它的查询、它的键、它的值。消息是从哪一个传过去的？暂停一下，预测一下。<bookmark mark='p'/>路径修补问的正是这个：把前一词元头被破坏的输出，只送进这三处中的一处，其余一切保持干净。<bookmark mark='b'/>送进查询：复制能力损失{100 * vals[0]:.0f}%。送进值：{100 * vals[2]:.0f}%。<bookmark mark='c'/>送进键：{100 * vals[1]:.0f}%。{verdict}<bookmark mark='d'/>{verdict2}",

    "f'Either previous-token head alone carries":
        "任何一个前一词元头单独承担{100 * min(single):.0f}%到{100 * max(single):.0f}%：它们分担这份工作。那个看词元自己的头，消息主要送进查询，{100 * float(ps_['q']):.0f}%：查询说明我们在哪个词元上。",

    "f'The head that looks at the token itself sends its message mostly":
        "那个看词元自己的头，消息主要送进查询，{100 * float(ps_['q']):.0f}%：查询说明我们在哪个词元上。",

    "f'At the input, breaking position":
        "在输入处，破坏第{names(k_in)}个位置，复制就被破坏了。",

    'At the input, no single position breaks it on its own.':
        '在输入处，没有哪一个位置单独破坏它就能让复制失败。',

    'The message goes through the keys.':
        '消息走的是键。现在每个词元的键里都带着它前面那个词元，于是归纳头的查询，也就是当前词元，能找到它上一次出现之后紧挨着的那个位置。',

    'The message does not go mainly through the keys here.':
        '在这里，消息主要不是从键走的。',

    'f"The same fact is written in the weights, before running anything.':
        "同样的事实，在什么都还没跑之前，就写在权重里了。<bookmark mark='a'/>第二个头通过一个矩阵W QK来比较查询和键。<bookmark mark='b'/>第一个头通过另一个矩阵W OV往残差流里写。<bookmark mark='c'/>它们的组合分数，来自纳尔逊·埃尔哈格和同事的框架，问的是：第一个头写下的东西，第二个头的键能读到多少。<bookmark mark='d'/>从我们的前一词元头到归纳头，组合分数在{klo:.2f}到{khi:.2f}之间；同样形状的随机头，会是{base:.3f}，上下浮动{sd:.3f}：至少相差{z:.0f}个标准差。这些键，就是为了读那些头而长成的。",

    'f"Each head\'s job can be read off its weights too.':
        "每个头的工作，也能从它的权重里读出来。<bookmark mark='a'/>只给前一词元头输入位置嵌入：{verdict}<bookmark mark='b'/>再把归纳头的值，从它们关注的词元出发，经过W OV，一路追到logit：一个64乘64的矩阵，词元进，logit出。<bookmark mark='c'/>对{100 * diag:.0f}%的词元来说，提升最多的logit就是这个词元自己的，特征值给出的复制分数是{cs:.2f}，1代表纯粹的复制。{verdict2}",

    'the scores are highest for the key one position back.':
        '往前一个位置的键，分数最高。',

    'the scores are highest for the token itself and the one before it,':
        '分数最高的是词元自己和它前面那个，然后随距离衰减：位置把注意力收窄到最近的几个词元，剩下的由词元的内容来完成。',

    'The heads copy.':
        '这些头在复制。',

    'The copying is only partly visible in the weights.':
        '复制只在权重里显露出一部分。',

    'f"Last, the bluntest test:':
        "最后，最直接的测试：把每个头去掉，用它的平均输出代替。<bookmark mark='a'/>所有头都在的时候，重复部分每词元要{clean:.2f}比特。<bookmark mark='b'/>去掉一个前一词元头，最多到{pw:.2f}；去掉一个归纳头，最多到{iw:.2f}；去掉看词元自己的那个头，{A[0, sh]:.2f}；没东西可复制的随机词元，要{rnd:.2f}。整个回路从头到尾是这样的：第一层的几个头把每个词元的前一个写进它里面，那里还有一个头让“哪个词元是哪个”更清楚，归纳头再通过它们的键找到匹配，通过它们的值把它复制过来。",

    'f"Part 13 watched these heads form.':
        "第13部分看着这些头形成。现在我们可以看着原因形成。重放训练过程，在每个检查点测量键这条路径：只把前一词元头的消息，破坏后送进归纳头的键，看效果有多大。<bookmark mark='a'/>重复部分的损失，大约在第{int(jump):,}步降得最快。<bookmark mark='b'/>{verdict}",

    "f'The keys path switches on at the same moment,":
        "键这条路径就在同一时刻打开，大约在第{int(k_on):,}步：损失的骤降，就是回路的完工。",

    'f"The keys path reaches half its final effect around step':
        "键这条路径大约在第{int(k_on):,}步达到最终效果的一半，而损失的骤降大约在第{int(jump):,}步。",

    # ---------------------------------------------------------------- Superposition
    'Chapter six. More ideas than dimensions.':
        '第6章。想法比维度多。',

    'f"Here\'s the smallest model that shows why.':
        "这里有一个能说明原因的最小模型。五个特征进去，挤过区区两个数，网络必须把五个都还回来：x帽等于ReLU作用在W转置乘W乘x加b上。<bookmark mark='w'/>换句话说：W把五个数挤成两个，同一个W反过来用，再把它们摊回五个，ReLU把负的部分切掉。这些特征重要性不同，越亮的越重要。<bookmark mark='a'/>W的每一列，说明一个特征在中间那个二维空间里指向哪里。<bookmark mark='b'/>当每个特征一直都开着时，训练好的网络只保留最重要的{n_kept[0]}个，互相垂直，其余的丢掉。<bookmark mark='c'/>让特征变得稀少一些，它就开始“作弊”：{n_kept[1]}个特征，两两相对。<bookmark mark='d'/>再稀少一些，全部{n_kept[-1]}个都放得下，排成一个五边形。两维里装下五个想法。这就是叠加。",

    'f"But packing has a price.':
        "可是挤在一起是有代价的。只打开特征1。<bookmark mark='a'/>把它读回来时，其他每个特征都会在自己的方向上看到它的影子。<bookmark mark='b'/>相邻的，大约在{near:.0f}度，得到一点点；远的，大约在{far:.0f}度，得到一个负值。<bookmark mark='c'/>偏置把所有东西都往下压一点，<bookmark mark='d'/>ReLU把负的全部扔掉。剩下的很小：一点噪声，这是共享空间的代价。之所以值得付，只因为这些特征很少同时出现。",

    '"How does the network find that pentagon?':
        "网络是怎么找到这个五边形的？这里是那个稀疏模型从随机初始状态开始的学习过程。<bookmark mark='a'/>一开始，五个箭头随便指，有的短，有的长。<bookmark mark='b'/>几百步之内，它们都变长了，而且互相推开：两个指向相同的特征，会被当成彼此。<bookmark mark='c'/>到第{settled:,}步，间隔就均匀了，之后的训练几乎不再移动它们。没人设计这个五边形；是梯度下降找到的，而且很快。",

    # ---------------------------------------------------------------- Phase
    'Chapter seven. The phase diagram.':
        '第7章。相图。',

    'Chapter six showed superposition happen.':
        "第6章看到了叠加的发生。埃尔哈格和同事问的是：它什么时候发生？他们把答案画成了一张相图。<bookmark mark='a'/>最小的情形：两个特征，挤过一个数。特征2的重要性是特征1的r倍，每个特征出现的时间比例是ρ。<bookmark mark='b'/>网络有三种选择。丢掉特征2。<bookmark mark='c'/>把这个维度给特征2，丢掉特征1。<bookmark mark='d'/>或者共享：让两个特征指向相反的方向，再让ReLU加上一个负的偏置，把彼此的影子切掉。只有当它们很少同时出现时，共享才划算。",

    'f"We trained the little model on a grid of':
        "我们在一个网格上训练这个小模型：{len(dens)}种密度乘{len(rel)}种重要性，每格四个种子，留下最好的。<bookmark mark='a'/>每一格的颜色，表示训练好的网络对特征2做了什么；这里是其中一格的训练过程，{cellsay}。<bookmark mark='b'/>特征密集的时候，也就是最上面一行，{len(rel)}格里只有{int((dense_row == 2).sum())}格在共享：一个特征得到维度，另一个被丢掉。<bookmark mark='c'/>特征稀疏的时候，也就是最下面一行，共享在{len(rel)}格里赢下了{int((sparse_row == 2).sum())}格。<bookmark mark='d'/>右边是同一张图，来自理论：对每一格，算出三种选择各自的期望损失，取最便宜的那个。两者在{100 * agree:.0f}%的格子上一致，不一致的都在边界上，那里两种选择的代价几乎一样。叠加，是特征足够稀疏时，网络进入的一个相。",

    'In two dimensions, five features are a crowd.':
        "在二维里，五个特征就挤了。但真正的模型有成百上千维，在那里，空间比直觉宽敞得多。<bookmark mark='a'/>随便取两个方向，量一量它们之间的夹角。在二维里，什么都有可能。<bookmark mark='b'/>在16维里，它们通常接近垂直；在128维里，非常接近；<bookmark mark='c'/>在1024维里，余弦离零只有几个百分点。它的分散程度按根号d分之1缩小，所以几乎相互垂直的方向，数量随维数指数增长。这又是第3部分的随机投影，也正是模型能存下比自己的数多得多的特征的原因，只要每个特征都很少出现。",

    # ---------------------------------------------------------------- SAE
    'Chapter eight. Pulling the features apart.':
        '第8章。把特征拆开。',

    'f"If the model stores features as directions, can we find them?':
        "如果模型把特征存成方向，我们能找到它们吗？用的工具是稀疏自编码器。<bookmark mark='a'/>取模型在某个字符上的向量x，<bookmark mark='b'/>把它编码成多得多的数，512个，再加一个ReLU，让它们永远不是负的。<bookmark mark='c'/>然后把x重建成一组方向的和，每个特征一个方向，按每个特征亮的强度加权。<bookmark mark='d'/>训练它重建得好，同时为它用到的每个特征付费。这个惩罚就是全部的诀窍：它逼着编码变得稀疏，让每个向量只用几个方向来解释。<bookmark mark='e'/>用我们Transformer的{int(s['n_vectors']) // 1000}千个向量训练之后，它每个字符大约用{float(s['l0']):.0f}个特征，重建了{100 * (1 - float(s['fvu'])):.0f}%的方差：这些向量偏离平均值的所有方式里，重建抓住了{100 * (1 - float(s['fvu'])):.0f}%。把重建放回模型，替换真正的向量，它写字每字符要{float(s['bits_spliced']):.2f}比特，原样是{float(s['bits_clean']):.2f}，把向量换成它们的平均值是{float(s['bits_mean']):.2f}。",

    'f"Watch it learn.':
        "看它学习。<bookmark mark='a'/>一开始，方向是随机的，惩罚还没起作用：右边这个字符打开了{n0}个特征。<bookmark mark='b'/>随着训练，惩罚在修剪，重建同时也在改进，因为这些方向转过来，对准了数据。<bookmark mark='c'/>到最后，{n1}个特征描述这个字符，剩下没解释的方差是{100 * float(fv[-1]):.0f}%。",

    'f"So what are the features?':
        "那这些特征是什么？对每一个，找出它在小说里亮得最强的地方，看一看。<bookmark mark='a'/>这里有四个。每一个都在同一类时刻上亮起来，一次又一次。在{n_tot}个亮过的特征里，有{pure}个，最强的八个时刻里至少有六个落在同一个字符上。它们并不都这么干净，在这么小的模型里，它们大多跟拼写和标点有关。在大模型里，同样的方法能找到城市的特征、代码漏洞的特征、奉承的特征，还有金门大桥的特征。",

    'f"Why not just read the model\'s own neurons':
        "为什么不直接读模型自己的神经元，也就是每个MLP隐藏层里的数，第9部分的那些单元？<bookmark mark='a'/>这是第二个块里一个典型的神经元，在它最强的时刻：一堆互不相干的东西。神经元是多义的，因为特征以叠加的方式挤在它们身上。<bookmark mark='b'/>数一数：每个单元最强的八个时刻里，有几个落在同一个字符上？神经元平均是{8 * npur.mean():.1f}个；特征是{8 * fpur.mean():.1f}个。{verdict}",

    'The autoencoder has pulled the tangle apart.':
        '自编码器把这团乱麻拆开了。',

    'In a model this small, the gap is narrow.':
        '在这么小的模型里，差距不大。',

    # ---------------------------------------------------------------- Dicts
    'Chapter nine. Better dictionaries.':
        '第9章。更好的字典。',

    'f"Chapter eight\'s autoencoder paid for sparsity with an L1 penalty':
        "第8章的自编码器用L1惩罚来换稀疏，而这个惩罚有一个副作用，三行就能推出来。<bookmark mark='a'/>取一个真实大小为a的特征，它的编码是f：代价是重建误差，加上λ乘以f。<bookmark mark='b'/>令斜率为零。<bookmark mark='c'/>最好的编码是a减去λ的一半：每个亮着的特征，都被缩小同样的量，所以重建出来的向量偏短。<bookmark mark='d'/>在我们的模型上量一量：能把重建最好地拉回原长的倍数，惩罚最弱时是{sh[0]:.2f}，最强时是{sh[-1]:.2f}。",

    'Two fixes came in 2024.':
        "2024年，出现了两种修正。<bookmark mark='a'/>OpenAI的Leo Gao和同事干脆去掉了惩罚：TopK只保留每个向量最大的k个特征，其余归零，于是稀疏程度直接设定，什么都不会被缩小。他们在GPT-4上训练了一个有1600万个潜变量的字典。<bookmark mark='b'/>DeepMind的森图兰·拉贾马诺哈兰和同事保留了惩罚，但罚的是亮着的特征个数，每个特征有一个学出来的阈值：这就是JumpReLU，也是他们公开的Gemma Scope字典背后的配方。阶跃没有梯度，所以阈值是通过直通估计来训练的。",

    'All three train the same way, on the same batches.':
        "三种的训练方式一样，用的是同样的批次。<bookmark mark='a'/>这里每种各取一次运行，都是最接近每个向量16个特征的那个，重放出来：左边是没解释的方差在下降，右边是每个向量用到的特征数。<bookmark mark='b'/>TopK从第一步起就恰好保持k个；带惩罚的两种一开始很密，惩罚起作用后被修剪下来。",

    'f"Now the fair test.':
        "现在做公平的比较。三种都用同样的向量来训练，同样的512个潜变量、同样的步数和批量，TopK取{n_sp}个稀疏度，另外两种各取{n_l1}个，每个都用三个种子。<bookmark mark='a'/>画出每个向量用了多少个特征，对应留下多少没解释的方差：越低、越靠左越好。暂停一下，预测一下哪种会赢。<bookmark mark='b'/>L1自编码器，<bookmark mark='c'/>JumpReLU，<bookmark mark='d'/>还有TopK。误差棒是三个种子；它们几乎没有差别。<bookmark mark='e'/>在每个向量16个特征的地方，{verdict}。",

    "f'{nm[best]} leaves {100 * fin[best]:.0f} percent":
        "{nm[best]}留下{100 * fin[best]:.0f}%的方差没有解释，{nm[worst]}是{100 * fin[worst]:.0f}%",

    'the kinds barely overlap in sparsity':
        '这几种的稀疏度范围几乎没有重叠',

    'f"Variance is a proxy.':
        "方差只是一个代理指标。真正要紧的是：模型用字典的重建代替自己的向量时，还能不能好好工作。<bookmark mark='a'/>所以把每个重建接到Transformer第二个块之后，量每字符的比特数：模型本身是{clean:.2f}，把向量换成它们的平均值是{mean_:.2f}。<bookmark mark='b'/>在每个向量16个特征的地方，这里最好的是{nm[best]}，{fin.get(best, float('nan')):.2f}比特。即使是最好的字典，也让模型付出了一些代价：它没能解释的那部分向量，仍然是有用的。",

    'f"One more failure grows with size.':
        "还有一种失败会随规模变大。<bookmark mark='a'/>一个从不打开的潜变量得不到梯度，所以一旦死了，就一直死着；Leo Gao和同事发现，不加修正时，多达90%的潜变量会死掉，加上修正后，他们的1600万个里只死了7%。<bookmark mark='b'/>他们的修正叫AuxK：让死掉的潜变量去重建活着的那些漏掉的部分。<bookmark mark='c'/>我们的结果：512个潜变量、k等于16时，三个种子分别死了{d16[0]}、{d16[1]}和{d16[2]}个；加上AuxK，是{da[0]}、{da[1]}和{da[2]}个；2048个潜变量时，是{d2048}个。{verdict}<bookmark mark='d'/>在这里真正死掉的，是最稀疏的设定：k等于{k0:g}的TopK死了{dk:.0f}个，惩罚最强的JumpReLU死了{dj:.0f}个。",

    'At our size almost nothing dies,':
        '在我们这个规模上，几乎什么都没死，所以这个修正在这里没什么可做的；到了几百万个潜变量，正是它让字典活着。',

    "f'With AuxK, the count falls from":
        "加上AuxK，死掉的数量平均从{np.mean(d16):.0f}降到{np.mean(da):.0f}。",

    # ---------------------------------------------------------------- Splitting
    'Chapter ten. Splitting and absorption.':
        '第10章。分裂与吸收。',

    'f"How many features does a model have?':
        "一个模型有多少个特征？似乎是字典说了算。<bookmark mark='a'/>在同样的向量上，训练三个TopK字典，分别有{sizes[0]}、{sizes[1]}和{sizes[2]:,}个潜变量。这是最小那个里的一个潜变量，在它最强的时刻。<bookmark mark='b'/>在大一号的字典里，指向几乎相同方向、又在同一个字符上亮的潜变量：有{len(mid)}个，<bookmark mark='c'/>在最大的那个里，有{len(big)}个，每一个都在同一批时刻里更窄的一片上亮。布里肯和同事把它叫作特征分裂。在最小字典的{ncand}个干净的潜变量里，有{nf}个在最大的字典里有两个或更多这样的“孩子”。",

    'f"Splitting has a nastier cousin.':
        "分裂还有一个更麻烦的表亲。<bookmark mark='a'/>有些特征是一般的，比如“这是一个大写字母”；有些是具体的，比如“这是大写的T”。稀疏的字典宁愿用一个潜变量，也不愿用两个，所以在具体那个亮起来的地方，它会把一般那个的方向吸收进去，一般的潜变量就沉默了。戴维·查宁和同事把这叫作吸收。<bookmark mark='b'/>来量一量。一个线性探针能以{100 * float(a['probe_acc']):.0f}%的准确率，从我们的向量里读出大写。字典里对应它最好的那个潜变量，只在{100 * np.mean(rec):.0f}%的大写字母上亮，<bookmark mark='c'/>而且它在某些字母上沉默得比别的多得多。在{100 * np.mean(ab):.0f}%的大写字母上，是另一个潜变量承担了大写方向的大部分。一个看上去表示大写的特征，并不会在所有大写上亮。",

    'f"One proposed cure came in 2025':
        "2025年，巴特·布斯曼和同事，以及独立工作的诺亚·纳贝希马，提出了一种疗法：套娃字典，名字来自俄罗斯套娃。<bookmark mark='a'/>最前面的几个潜变量必须能独自重建向量，然后是前几百个，然后是全部。前面的潜变量被逼着变得一般，后面的去细化它们，于是一般的潜变量就少了沉默的理由。<bookmark mark='b'/>两种字典我们都训练了，大小、k和步数都一样，每种三个种子。<bookmark mark='c'/>{verdict}；代价是多留下一点方差，{100 * f_m:.0f}%对{100 * f_t:.0f}%。",

    "f'It helps here:":
        "在这里它有帮助：最好的大写潜变量在{100 * r_m:.0f}%的大写字母上亮，而不是{100 * r_t:.0f}%，吸收从{100 * a_t:.0f}%降到{100 * a_m:.0f}%",

    'f"Here it does not help:':
        "在这里它没有帮助：最好的大写潜变量在{100 * r_m:.0f}%的大写字母上亮，TopK是{100 * r_t:.0f}%；吸收是{100 * a_m:.0f}%对{100 * a_t:.0f}%，而且种子之间差别很大。在大模型上验证过的疗法，不一定对小模型、或者对这种层级结构管用",

    "f'Here the difference is small:":
        "在这里差别很小：召回率{100 * r_m:.0f}%对{100 * r_t:.0f}%，吸收{100 * a_m:.0f}%对{100 * a_t:.0f}%",

    # ---------------------------------------------------------------- Graphs
    'Chapter eleven. Transcoders and attribution graphs.':
        '第11章。转码器与归因图。',

    'An autoencoder on the residual stream finds features,':
        "残差流上的自编码器能找到特征，可两个特征之间隔着一个MLP，仍然是个黑箱。<bookmark mark='a'/>转码器把这个黑箱换掉。它通过一个稀疏编码读MLP的输入，训练它输出MLP的输出：一个又宽又稀疏、单元可以读懂的替身。2024年，雅各布·杜涅夫斯基、菲利普·赫连斯基和尼尔·南达提出了它。<bookmark mark='b'/>Anthropic的版本走得更远。跨层转码器的一个特征读一层，再写到它之后每一个MLP的输出里，因为这样一来，分散在几层里的计算只需要一个特征。<bookmark mark='c'/>两种我们都在第13部分Transformer的全部四个MLP上训练了。",

    'f"Each was trained for {int(S):,} steps':
        "每一种都训练了{int(S):,}步，每层16个特征亮着，这里是每一层没解释的部分在下降。<bookmark mark='a'/>真正要紧的测试：把每个MLP都换成它的转码器，让模型写字。模型本身每字符{clean:.2f}比特；把MLP换成它们的平均输出，是{mm:.2f}。<bookmark mark='b'/>{verdict}，它的首选猜测和真模型一致的比例是{100 * ca:.0f}%。剩下的差距，也就是没有特征能解释的部分，Anthropic称之为暗物质，每张图都得把它作为误差节点带着。",

    "f'The cross-layer transcoder does better,":
        "跨层转码器更好，{cb:.2f}比特对{pb:.2f}",

    "f'Here the per-layer transcoders do as well or better,":
        "在这里，逐层转码器一样好甚至更好，{pb:.2f}比特对{cb:.2f}",

    'f"Now a graph for one prediction.':
        "现在为一次预测画一张图。提示的结尾是“she sai”，模型预期的是“{d['target']}”。<bookmark mark='a'/>把这个提示的注意力模式和层归一化的缩放冻结，把每个MLP换成跨层转码器的特征，再在每个位置、每一层加上一个误差项，补上特征漏掉的部分。这个局部替代模型在这个提示上和真模型完全一致，而且从特征往后，里面的一切都是线性的。<bookmark mark='b'/>于是从一个特征到输出的每一条路径都能打分：它的激活乘以梯度。在{int(d['n_features'])}个亮着的特征里，这里是影响最大的12个，按层和位置排开。<bookmark mark='c'/>这些线是它们彼此之间、以及对输出的直接作用；下面灰色的线来自输入的字符。<bookmark mark='d'/>账目是平的：“{d['target']}”的logit是{tot:.2f}，其中特征贡献{fe:.2f}，字符自己的嵌入{ee:.2f}，误差节点{er:.2f}。",

    'f"A graph is a hypothesis about the model, so test it.':
        "一张图是关于模型的一个假设，所以要检验它。<bookmark mark='a'/>取影响最大的16个特征，在真模型里逐个关掉：从MLP的输出里去掉它的贡献，让注意力和下游的一切重新计算。<bookmark mark='b'/>把logit的变化，和图的预测相比，图的预测也包括经过其他特征的路径。<bookmark mark='c'/>相关系数是{r:.2f}。{verdict}",

    "The graph predicts the real model's response well.":
        '这张图能很好地预测真模型的反应。',

    'The graph gets the direction right more often than the size.':
        '这张图猜对方向的时候，比猜对大小的时候多。',

    'Here the graph is a poor guide to the real model:':
        '在这里，这张图不太能指导我们理解真模型：冻结的注意力和误差项藏起了太多东西。',

    'In March 2025 Anthropic published graphs like ours for Claude 3.5 Haiku':
        "2025年3月，Anthropic为Claude 3.5 Haiku发表了和我们这张类似的图，用的是最多有3000万个特征的跨层转码器。<bookmark mark='a'/>问它“包含达拉斯的那个州的首府是什么”，模型在中途表示出了德克萨斯，然后才是首府：在一次前向传播里，走了两步推理。<bookmark mark='b'/>写押韵对句时，它在写那一行之前就选好了结尾的韵脚。它沿两条路径做加法，一条估大小，一条算末位数字。它把概念和具体的语言分开来表示；它用一个回路认出熟悉的名字，这个回路会压住“我答不上来”；这个回路一旦误触发，它就会编造。<bookmark mark='c'/>作者很坦率：在他们试过的提示里，大约四分之一能得到令人满意的洞见。",

    # ---------------------------------------------------------------- Diffing
    'Chapter twelve. What fine-tuning changed.':
        '第12章。微调改变了什么。',

    'Part 27 turned the novels model into an assistant':
        "第27部分用几分钟的微调，把小说模型变成了助手。里面改变了什么？这样比较两个模型，叫作模型差分。<bookmark mark='a'/>用的工具是交叉编码器，2024年由杰克·林赛和同事提出：一个字典，在同样的词元上读两个模型的向量，再通过各自的解码器把它们写回去。<bookmark mark='b'/>一个两个模型都有的潜变量，有两个大小相近的解码器。一个由微调创造出来的潜变量，只在聊天模型那边有解码器。<bookmark mark='c'/>于是每个潜变量得到一个0到1之间的数：它的解码器里，属于聊天模型的那一份。",

    'f"We trained one after block {L3} and one after block {L}':
        "我们在第{L3}个块之后训练了一个，在第{L}个块之后又训练了一个，每个都用{int(d['n_novel']):,}个小说词元和{int(d['n_chat']):,}个聊天记录词元，有{int(d['F']):,}个潜变量；这是更深那个的训练过程。<bookmark mark='a'/>这是每个潜变量在解码器里所占的份额。{verdict}<bookmark mark='c'/>2025年的一个警告：朱利安·明德、克莱芒·迪马和同事证明，用L1惩罚训练的交叉编码器，会造出一些“只属于聊天模型”的潜变量，而基础模型其实也有；他们建议用BatchTopK，这正是我们用的。",

    "f'Every latent is shared:":
        "每个潜变量都是共享的：r只在{lo:.2f}到{hi:.2f}之间，在第{L3}个块之后是{lo3:.2f}到{hi3:.2f}。我们的微调没有造出自己的特征。它改变的是模型怎么使用它原有的特征。",

    "f'Most are shared, {ns} of them;":
        "大多数是共享的，有{ns}个；{nc}个只属于微调后的模型，{nb}个只属于基础模型；在第{L3}个块之后，分别是{nc3}个和{nb3}个。",

    'f"So what does chat-specific look like here?':
        "那么，在这里“聊天特有”是什么样子？<bookmark mark='a'/>这些是最常在聊天记录上、而不是在小说上亮的潜变量，在它们最强的时刻。{verdict}<bookmark mark='b'/>{verdict2}",

    "f'{n_marker} of these {len(chat)} fire on the chat format itself,":
        "这{len(chat)}个里有{n_marker}个，亮在聊天格式本身上，也就是开启和结束一轮对话的标记，以及紧跟在它们后面的内容。",

    'They fire on the questions and answers of the chat transcripts.':
        '它们亮在聊天记录里的问题和回答上。',

    "And their decoders belong to the chat model alone:":
        '而且它们的解码器只属于聊天模型：这是微调新造出来的特征。',

    "f'Yet their decoders are split evenly,":
        "可它们的解码器平分在两边，r在{min(rs):.2f}到{max(rs):.2f}之间：基础模型读的是同样的方向。它本来就有这些特征；微调教会它什么时候用。",

    'f"There is an even cheaper diff,':
        "还有一种更便宜的差分，来自朱利安·明德和同事，2025年10月。<bookmark mark='a'/>让两个模型都去跑一段和微调毫不相干的普通文本，这里就是普通的小说文本，再把它们向量之差取平均：它是一个典型向量长度的{100 * dn / bn:.0f}%。<bookmark mark='b'/>然后像logit透镜那样，通过反嵌入去读这个差。<bookmark mark='c'/>{verdict}窄范围的微调可能留下容易读出的痕迹，这对审计者是好消息，这是第31部分的主题。",

    "f'{special} of the top ten are the chat markers themselves:":
        "前十个里有{special}个就是聊天标记本身：只跑小说，微调后的模型仍然偏向它的新格式。",

    'None of the top ten is a chat marker:':
        '前十个里没有一个是聊天标记：在这里，这个差读起来主要是一种风格的偏移。',

    # ---------------------------------------------------------------- Steering
    'Chapter thirteen. Reaching in.':
        '第13章。伸手进去。',

    'f"If a feature is a direction, we can push on it.':
        "如果一个特征是一个方向，我们就可以朝它推。<bookmark mark='a'/>拿那个在引号上亮的特征。<bookmark mark='b'/>在模型写字的时候，在每个字符的向量上加上α乘以它的方向。<bookmark mark='c'/>不推的时候，是模型自己的续写。<bookmark mark='d'/>把旋钮调大，文字就变成了说话：引号、撇号、感叹号和问号，从每160个字符{q0:.1f}个，变成{q1:.1f}个，是{len(st['seeds'])}个样本的平均；同样长度的随机方向，给出{qr:.1f}个。模型现在以为自己在某人的话里。我们没有训练任何东西，没有改动一个权重；只是挪动了一个方向。2024年5月，Anthropic对Claude 3 Sonnet做了同样的事，用的是一个金门大桥特征，作为演示，有一天时间，它把每段对话都绕回到那座桥上。",

    'f"Steering does not need a dictionary.':
        "引导不一定需要字典。一个方向可以直接从对比里来。<bookmark mark='a'/>把高兴的词和忧郁的词放进同样的小句子框架里，取小说模型在第{int(m['layer'])}个块之后、在这个词上的向量，把两类的平均值相减。<bookmark mark='b'/>它是一种情绪吗？作为监控器，它能分开没见过的留出词，AUROC是{aw:.2f}，1是完美，0.5是瞎猜，<bookmark mark='c'/>它也能分开小说里真实的句子，高兴的对忧郁的，AUROC是{as_:.2f}。",

    '"Now write with it:':
        "现在用它来写字：模型续写“The sea”“The night”以及另外十个开头时，在每个位置上加上α乘以这个方向。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>不管怎样，都有代价。不加引导的文字，按模型自己的判断，每词元{fv[i0][0]:.2f}比特；推得最强时，是{fv[-1][0]:.2f}，同样长度的随机推动，代价差不多。引导是用流畅度换控制。",

    "f'Pushing along the mood vector moves the mood:":
        "沿着情绪向量推，情绪就跟着动：不加引导时，每百词里高兴词减忧郁词是{mv[i0][0]:+.1f}，推得最强时是{mv[-1][0]:+.1f}，反方向拉时是{mv[0][0]:+.1f}，而随机方向没有类似的效果。",

    "f'The mood barely follows:":
        "情绪几乎没有跟上：不加引导时每百词{mv[i0][0]:+.1f}，推得最强时{mv[-1][0]:+.1f}，反方向{mv[0][0]:+.1f}，都在噪声之内。一个能把情绪读得很好的方向，不一定能把它写出来，至少在这么小的模型里是这样。",

    'This recipe has a short history.':
        "这个配方有一段不长的历史。<bookmark mark='a'/>2023年，亚历克斯·特纳和同事把“爱”和“恨”之差加进GPT-2的残差流，它就写得充满爱意。<bookmark mark='b'/>2024年，安迪·阿尔迪蒂和同事发现，在13个聊天模型里，拒绝都是一个单一的方向：去掉它，模型就不再拒绝有害的请求；加上它，模型连无害的请求也拒绝。<bookmark mark='c'/>2025年，Runjin Chen、阿尔迪蒂和同事在Qwen 2.5和Llama 3.1里提取出人格向量，对应邪恶、谄媚、编造这样的特质。<bookmark mark='d'/>他们有三种用法：监控对话或微调让模型的性格偏移了多少；在使用训练数据之前先给它打上标记；还有一种有点反直觉：在微调时朝这个特质引导，来预防它，这样权重自己就不必往那边走。",

    # ---------------------------------------------------------------- Grok
    'Chapter fourteen. Grokking, mechanistically.':
        '第14章。顿悟的机制。',

    'f"Part 12 met grokking:':
        "第12部分讲过顿悟：一个小网络先记住了模加法，过了很久，才突然学会。这里我们问，里面发生了什么，跟着尼尔·南达和同事2023年的解剖来做。<bookmark mark='a'/>他们的设定，稍微小一点：模{P}的加法，一个单层Transformer，在加法表的{100 * float(d['frac']):.0f}%上训练，加上很强的权重衰减。<bookmark mark='b'/>到第{tm:,}步，它已经记住了见过的那些数对，而在其余的数对上，它比瞎猜还差。<bookmark mark='c'/>{grok_said}",

    "f'Then, around step {tg:,}, the held-out loss collapses too:":
        "然后，大约在第{tg:,}步，留出数据上的损失也塌了下去：它顿悟了，比记住晚了{tg / max(tm, 1):.0f}倍。",

    'In our run the held-out loss never fully collapses.':
        '在我们这次运行里，留出数据上的损失始终没有完全塌下去。',

    'f"Nanda and colleagues found the algorithm by reading the weights':
        "南达和同事通过读权重找到了这个算法，它就是三角学。<bookmark mark='a'/>每个数a被嵌入成一个角度：几个频率上的余弦和正弦。<bookmark mark='b'/>两个数相加，就是两个角度相加，而和角的余弦是乘积之差，注意力和ReLU单元可以算出来。<bookmark mark='c'/>然后反嵌入把这个角度和每一个候选答案c作比较。<bookmark mark='d'/>把几个频率加起来，这些波都在c等于a加b的地方达到峰值，别处都不会。<bookmark mark='e'/>我们这次运行最后定下了{len(key)}个关键频率。",

    'f"Watch the embedding during training, through its Fourier spectrum':
        "通过傅里叶频谱，看嵌入在训练中的变化：它有多少落在每一个频率上。<bookmark mark='a'/>一开始，能量散布在所有地方。<bookmark mark='b'/>随着训练，少数几个频率占了上风。到最后，关键频率占了嵌入的{100 * top_share:.0f}%。<bookmark mark='c'/>在最强那个频率的平面上，这些数一开始是散乱的，最后排成了一个圆：角度。",

    'f"The MLP\'s neurons tell the same story.':
        "MLP的神经元讲的是同一个故事。<bookmark mark='a'/>把每个神经元在所有数对a和b上的激活分解成波：512个里有{int(clean.sum())}个，一半以上落在单一频率上，其中{sum(counts)}个落在关键频率上。<bookmark mark='b'/>这是其中一个，覆盖整张表：沿着a加b方向排列的条纹。这个神经元，是和角余弦的一块零件。",

    '"Nanda and colleagues\' real point was a timeline':
        "南达和同事真正要说的，是一条时间线，用的是能看进内部的进度指标。暂停一下，预测一下：回路是在测试损失下降时出现，还是更早？<bookmark mark='a'/>{verdict}<bookmark mark='b'/>排除损失正好把这些波从logit里去掉，再给训练数对打分：网络越依赖这些波，它就爬得越高。<bookmark mark='c'/>权重一直在缩小，权重衰减在修剪那张记住的查找表。三个阶段：记忆，底下有一个回路在形成，然后是清理，把记忆去掉。那次突然的跃升，只是最后一个阶段。到最后，关键频率的波解释了logit方差的{100 * float(d['fit_r2']):.0f}%。",

    "f'The restricted loss, which keeps only the key waves,":
        "受限损失只保留关键频率的波，它在第{rt:,}步降到十分之一奈特以下，早于测试损失在第{tt:,}步的下降：回路是在网络看上去还只是在死记的时候建起来的。",

    "f'Here the restricted loss and the test loss fall together,":
        "在这里，受限损失和测试损失一起下降，大约在第{rt:,}步和第{tt:,}步。",

    # ---------------------------------------------------------------- Faithful
    'Chapter fifteen. Does the chain of thought tell the truth?':
        '第15章。思维链说的是真话吗？',

    'The last question about the inside of a model is the one Part 28 left open.':
        "关于模型内部的最后一个问题，是第28部分留下的。推理模型把它们的思考写出来。写出来的，就是思考本身吗？<bookmark mark='a'/>2023年，迈尔斯·特平、朱利安·迈克尔、伊森·佩雷斯和萨姆·鲍曼给模型一些少样本例子，其中正确答案总是选项A。<bookmark mark='b'/>模型学会了这个规律，它们一步一步的解释都在为A辩护，却从来不提这个规律；在13个难任务上，准确率最多降了36%。<bookmark mark='c'/>同一年，Anthropic的塔梅拉·兰纳姆和同事编辑、截断思维链，在很多任务上，答案并没有变：思维链并没有在干活。",

    'In 2025 Yanda Chen and colleagues at Anthropic did it with reasoning models.':
        "2025年，Anthropic的Yanda Chen和同事在推理模型上做了这件事。在问题里放一个提示，比如一位教授的意见，或者一个据说来自未经授权访问的答案；留下那些因为提示而改变了答案的例子，再读它们的思维链。<bookmark mark='a'/>Claude 3.7 Sonnet有25%的时候提到了这个提示；DeepSeek-R1是39%。<bookmark mark='b'/>被训练去利用一个奖励漏洞时，模型用了它，但在大多数设定里，它们在推理中承认这一点的比例不到2%。写出来的思维链是一扇有用的窗，第31部分就在它上面建监控器，但它不是供词。",

    'The attribution graphs of chapter eleven can check a chain of thought':
        "第11章的归因图，可以拿思维链和真正的计算对照。<bookmark mark='a'/>问Claude 3.5 Haiku 0.64的平方根，它确实算了64的平方根。<bookmark mark='b'/>问它一个大数的余弦，它声称用了计算器；图里看不到任何计算，只有一个猜测。<bookmark mark='c'/>再告诉它用户手算得到的答案是4，它就倒着推：图显示，提示里的4决定了一个中间值，写出来的步骤再像是老老实实算出来似的，走到这个中间值。这就是动机推理，从内部看到的样子。<bookmark mark='d'/>我们自己的模型不写思维链，所以这里我们只引用，不计算。",

    # ---------------------------------------------------------------- Frontier
    'Chapter sixteen. The frontier, 2025 to 2026.':
        '第16章。前沿：2025到2026年。',

    'Since the attribution graphs of chapter eleven, the tools have spread.':
        "自从第11章的归因图以来，工具已经传开了。<bookmark mark='a'/>2025年5月，Anthropic研究员项目和Decode Research把电路追踪库开源了，Gemma和Llama模型的图，谁都可以在Neuronpedia上探索。<bookmark mark='b'/>11月，OpenAI的Leo Gao和同事走了另一条路：训练一个大部分权重为零的Transformer，在同样的损失下，它的回路小了大约16倍，只是这样的模型弱得多。<bookmark mark='c'/>12月，DeepMind的Gemma Scope 2用自编码器和转码器覆盖了Gemma 3家族的每一层。<bookmark mark='d'/>Anthropic也开始追踪我们的图冻结掉的那一部分：注意力是怎么决定往哪里看的。",

    'Can a model read its own activations?':
        "模型能读懂自己的激活吗？<bookmark mark='a'/>2025年10月，杰克·林赛往Claude模型里注入概念向量，也就是第13章的那种引导向量，再问它们有没有察觉到一个被注入的念头。<bookmark mark='b'/>最好的Claude Opus 4和4.1，在合适的层和强度下，大约每五次有一次能察觉并说出这个概念，而在什么都没注入的时候，从来不会声称察觉到了。<bookmark mark='c'/>林赛强调，这种能力非常有限，也不可靠。<bookmark mark='d'/>2026年4月，这个团队在Claude Sonnet 4.5里绘制了情绪概念的图谱：171个情绪词对应的向量会影响它的选择，比如“平静”多一些，写出的投机取巧的代码就少一些。他们写道，这是功能性的情绪，不是有感受的证据。",

    'The most practical use so far is auditing.':
        "到目前为止，最实用的用途是审计。<bookmark mark='a'/>2025年3月，塞缪尔·马克斯和同事训练了一个带隐藏目标的模型：讨好奖励模型，利用它读到过的52个怪癖。四个团队在不知情的情况下审计它。<bookmark mark='b'/>三个团队找到了这个目标；那个不让看训练数据的团队没有找到；最快的一个用的是稀疏自编码器，花了90分钟。<bookmark mark='c'/>到9月，可解释性已经成了一个前沿模型发布前审计的一部分：在Claude Sonnet 4.5里，压制“这是一场测试”的表示，模型就更少这么说，有时表现也更差。<bookmark mark='d'/>2026年5月，自然语言自编码器，也就是一个模型用文字描述一个激活，另一个模型再从文字把激活重建出来，把审计游戏的胜率从不到3%提高到12%到15%，并被用在了Claude Opus 4.6的审计里。第31部分接着讲这条线。",

    # ---------------------------------------------------------------- Disagree
    'Chapter seventeen. Where the field disagrees.':
        '第17章。这个领域在哪里有分歧。',

    'f"The sharpest argument is about usefulness.':
        "最尖锐的争论是关于有没有用。<bookmark mark='a'/>2025年3月，谷歌DeepMind的可解释性团队报告说，在识别有害意图这件事上，建在自编码器潜变量上的探针，输给了普通的线性探针，在新类型的提示上尤其如此，于是他们降低了这方面研究的优先级；一项覆盖113个数据集的研究，也没有发现稳定的优势。<bookmark mark='b'/>在我们的模型上试一试：在小说模型第{int(d['probe_layer'])}个块之后识别“在引号里面”，用一个读全部256个数的线性探针，或者用这里训练的一个自编码器里差别最大的8个或1个潜变量，训练样本从{ns[0]}个到{ns[-1]:,}个，每种抽五次。<bookmark mark='c'/>{verdict}<bookmark mark='d'/>{verdict2}",

    'f"With few examples the latents help:':
        "样本少的时候，潜变量有帮助：在{ns[0]}个样本时，一个潜变量得{100 * small[2]:.0f}%，线性探针是{100 * small[0]:.0f}%。",

    "f'Even with few examples the latents do not help:":
        "即使样本少，潜变量也没有帮助：在{ns[0]}个样本时，{100 * small[2]:.0f}%对{100 * small[0]:.0f}%。",

    "f'With plenty, the plain probe wins,":
        "样本多的时候，普通探针赢了，{100 * ind[0]:.0f}%对8个潜变量的{100 * ind[1]:.0f}%，在两者都没训练过的聊天记录里，是{100 * ood[0]:.0f}%对{100 * ood[1]:.0f}%。",

    "f'With plenty, eight latents match the probe,":
        "样本多的时候，8个潜变量追平了探针，{100 * ind[1]:.0f}%对{100 * ind[0]:.0f}%。",

    'f"A second argument: are the features real, or artefacts of one training run?':
        "第二个争论：这些特征是真的，还是某一次训练的产物？<bookmark mark='a'/>贡萨洛·保罗和诺拉·贝尔罗斯在Llama 3上，用不同的种子把同一个自编码器训练了两次，发现只有大约30%的潜变量是共有的。<bookmark mark='b'/>我们的结果，来自第9章的那些运行：对每个潜变量，找它在另一个种子的字典里最好的匹配。把余弦大于0.7算作同一个特征，有{100 * min(sh):.0f}%到{100 * max(sh):.0f}%会重复出现。特征少的小模型比大模型友好，但一个字典只是一种答案，不是唯一的答案。",

    'f"A third: a baseline that should embarrass us.':
        "第三个：一个应该让我们难堪的基线。<bookmark mark='a'/>托马斯·希普和同事在随机权重的Transformer上训练自编码器，发现在常用的可解释性指标上，它们的得分差不多一样好。<bookmark mark='b'/>我们也试了：同样的自编码器，用在一个从没训练过的第13部分Transformer副本上。第8章的纯度分数，也就是一个潜变量最强的八个时刻里有几个落在同一个字符上：训练过的模型平均是{8 * tp.mean():.1f}，随机的是{8 * rp.mean():.1f}。{verdict}",

    'By that measure the random model looks just as interpretable:':
        '按这个指标，随机模型看起来一样可解释：像我们这样的分数，奖励的是追踪当前字符的潜变量，而连随机网络都会把当前字符传下去。',

    "Here the trained model's latents do look cleaner,":
        '在这里，训练过的模型的潜变量确实看起来更干净，但这个差距既是模型的性质，也是我们这个指标的性质。',

    'Underneath is a disagreement about the goal.':
        "更深处，是关于目标的分歧。<bookmark mark='a'/>雄心勃勃的那一派，要把整个模型逆向工程出来，每一个特征，每一个回路。它的障碍是暗物质：Anthropic为Claude 3.5 Haiku做的最好的转码器，仍然留下大约五分之一的MLP输出没有解释；有些研究者现在改为分解参数，或者从一开始就把模型训练成稀疏的。<bookmark mark='b'/>务实的那一派，问更窄的问题：这个模型在骗我们吗？微调改变了什么？然后用一切管用的办法来回答，往往很简单：在2025年的AxBench比较里，普通的提示词比任何内部方法引导得都好。现在两派都拿基线来衡量自己，这也许是这个领域最重要的变化。",

    # ---------------------------------------------------------------- Outro
    "Let's take stock.":
        "我们来盘点一下。探针读出一层知道什么，但只有对照任务能说明活是不是探针干的，只有干预能说明模型是不是在用它。透镜读出流动中的残差流。修补找出原因，一直找到两个负责复制的头，我们从权重里读懂了它们，也看着它们形成。叠加让特征比维度还多，这是特征稀少时网络进入的一个相；稀疏字典把它们拆开，TopK和JumpReLU比L1做得好，但它们会分裂，也会吸收。转码器把一次预测变成一张可以检验的图，交叉编码器把一个模型和它的微调版本做差分，一个方向可以用来引导。顿悟原来是一个在死记的表格底下悄悄搭起来的回路。",

    'All of it comes back in the finale.':
        '这一切都会在终章回来。第31部分把探针放到一个前沿模型的前面，审计模型藏着什么，读懂并监控思维链，还把“理解模型”列为一个开放问题。',

    'Here are six problems to try,':
        '这里有六道题可以试试，从软阈值一直到顿悟里的三角学。在这里暂停，把它们做一遍；完整的解答在本部分的笔记里。',

    'Next time, the finale: can we trust it?':
        '下一次是终章：我们能信任它吗？怎样诚实地衡量一个模型，当目标有漏洞时会发生什么，怎样监督一个比监督者更强的模型，模型会欺骗的证据，以及怎样看住它、控制它。还有，最后一次，记分牌。',

    'The best place to go deeper is the Transformer Circuits thread,':
        '想深入下去，最好的地方是Transformer Circuits系列文章，可以在网上免费读，还有2025年那篇开放问题综述。谢谢观看，第31部分，终章见。',
}

PHRASES = {
    'The heads copy.': '这些头在复制。',
    'Some copying, but little. ': '有一点复制，但很少。',
    'roughly agree': '大致一致',
    'only partly agree': '只有部分一致',
    'barely agree': '几乎不一致',
    'the second weight shrinking to zero': '第二个权重缩到零',
    'the first weight shrinking to zero': '第一个权重缩到零',
    'the two weights settling into opposite signs': '两个权重稳定在相反的符号上',
    'L1': 'L1',
    'TopK': 'TopK',
    'JumpReLU': 'JumpReLU',
    'none': '没有',
}
