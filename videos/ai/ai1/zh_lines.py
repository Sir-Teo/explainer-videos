"""Chinese narration for ai1: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第1部分：猜字游戏'

CHAPTERS = {
    'Hook': '香农的猜字游戏',
    'Probability': '1. 概率与链式法则',
    'Surprise': '2. 应该有多意外',
    'Entropy': '3. 熵，以及它为什么是唯一的',
    'Prefix': '4. 前缀码与克拉夫特–麦克米兰不等式',
    'Huffman': '5. 最好的编码：霍夫曼编码，以及它为什么最优',
    'Typical': '6. 典型序列与信源编码定理',
    'CrossEntropy': '7. 交叉熵与KL散度：错误模型的代价',
    'Arithmetic': '8. 算术编码：预测就是压缩',
    'Counting': '9. 靠计数来学习，以及拉普拉斯法则',
    'Shannon1951': '10. 香农1951年的实验',
    'Likelihood': '11. 学习：似然、softmax与梯度',
    'Information': '12. 互信息：过去告诉了未来什么',
    'Knowledge': '13. 要猜得好，需要知道什么',
    'Units': '14. 每字符比特数，每词元比特数',
    'Scoreboard': '15. 记分牌：语言建模就是压缩',
    'Outro': '回顾、习题，以及这些想法会在哪里再现',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'In 1951, Claude Shannon played a game with English.':
        "1951年，克劳德·香农和英语玩了一个游戏。他拿来一个句子，把它遮住，请一个人一个字母一个字母地猜。<bookmark mark='a'/>猜错了，就再猜，直到猜对为止。每个字母下面，他都记下猜了几次。",

    'most + " <bookmark mark=\'a\'/> " + moto_said':
        "{most}<bookmark mark='a'/>{moto_said}<bookmark mark='b'/>猜测次数集中在少数几个地方，大多是一个新词开始的地方。信息就藏在那里。",

    'Most letters fall on the first guess.':
        '大多数字母，第一次就猜中了。',

    "f'{100 * frac1:.0f} percent of the letters fall on the first guess.":
        '{100 * frac1:.0f}%的字母，第一次就猜中了。',

    'f"Once you\'ve seen {seen}, the rest of motorcycle is free.':
        '一旦看到了{seen}，motorcycle剩下的部分就不用猜了。',

    'Even inside a word like motorcycle, the letters take guesses.':
        '就算在motorcycle这样的词里面，字母也要猜上几次。',

    'f"From counts like these, Shannon estimated how much information':
        "根据这样的计数，香农估算出英语到底携带多少信息：每个字母大约1比特，所谓1比特，就是一个是或否问题的答案，在{lo_h:.1f}到{hi_h:.1f}之间。<bookmark mark='a'/>而一个盲猜的字母，最多可以携带{blind:.2f}比特。我们写下的东西，大部分是可以预测的。",

    "Shannon didn't start from nothing.":
        "香农并不是从零开始的。<bookmark mark='a'/>电报员早就知道，常见的字母应该用短的编码：摩尔斯电码给e的只是一个点。<bookmark mark='b'/>1928年，贝尔实验室的拉尔夫·哈特利提出，用可能消息个数的对数来衡量信息。<bookmark mark='c'/>1948年，香农把它变成了一门理论：熵，比特，以及压缩的极限。<bookmark mark='d'/>接着是猜字游戏、霍夫曼编码和算术编码。<bookmark mark='e'/>半个世纪之后，同一个游戏成了机器学习语言的方式：2003年，一个被训练来猜下一个词的神经网络；然后是GPT-2，以及今天的模型。",

    'f"Seventy-five years after Shannon\'s game':
        "香农的游戏过去75年后，它正是大语言模型被训练去玩的游戏。给它一个句子的开头，<bookmark mark='a'/>它就为每一个可能的下一个词给出一个概率。<bookmark mark='b'/>2019年的GPT-2，有1.24亿个参数，也就是模型里那些可调的数，{says(pa)}。<bookmark mark='c'/>2025年的Qwen3，有40亿个参数，{says(pb)}。",

    'Strictly, what a model guesses is the next token.':
        "严格地说，模型猜的是下一个词元。<bookmark mark='a'/>词元，就是模型一次猜出的一小块文本：可以是一个完整的词，一个词的一部分，或者一个标点符号。这是一部1930年小说里的一行，按GPT-2的方式切开。Paris，连同它前面的空格，是单独一个词元。",

    "And it's not just text.":
        "而且不只是文字。<bookmark mark='a'/>生成图像的模型，学的是去猜图片里被加进去的噪声。<bookmark mark='b'/>语音模型，猜下一小段声音。<bookmark mark='c'/>机器人控制器，猜机械臂的下一个动作。几乎每一个前沿模型，骨子里玩的都是香农游戏的某个版本。",

    'Which raises the question this whole series is about.':
        '这就引出了整个系列要回答的问题：要猜得好，你得知道些什么？',

    "Over thirty-one parts, we'll build the answer from the ground up":
        "在31个部分里，我们会从头搭建出这个答案，也看看这个领域是怎么走到今天的。<bookmark mark='a'/>先是基础：信息，符号主义时代，向量，微积分和随机性。<bookmark mark='b'/>然后是从数据中学习，一直到深度学习革命和规模的数学。<bookmark mark='c'/>然后是Transformer时代。<bookmark mark='d'/>然后是生成与感知。<bookmark mark='e'/>然后是能动性：强化学习，推理，还有智能体。<bookmark mark='f'/>最后，当我们往模型里面看时，能看到什么，以及我们能不能信任它。",

    'Part one starts where Shannon did.':
        "第1部分从香农出发的地方开始。<bookmark mark='a'/>这一部分讲：信息是什么，为什么用比特来衡量；最好的编码，以及香农证明的极限；错误模型的代价；一种能把任何好的猜测者变成压缩器的编码；模型怎样学会猜；以及猜测已经走了多远。到最后，我们会明白，为什么猜得好和压缩得好是同一件事。",

    'f"And we\'ll keep score.':
        "我们还要记分。这是一部小说里的一页，1930年的《马耳他之鹰》。它在2026年1月1日进入公有领域，上了古登堡计划，那时这一部分的每个模型都已经训练完了，所以没有一个可能把它背下来。<bookmark mark='a'/>存成纯文本，每个字符要8比特。<bookmark mark='b'/>整个系列的任务，就是解释记分牌上的这些数字是怎么降下来的：从8，{goal}。",

    'to below one':
        '降到1以下',

    # ------------------------------------------------------------------ Probability
    'Chapter one. Before we can score a guess':
        '第1章。在给猜测打分之前，我们得先有办法把猜测写下来。',

    'f"Take {nb} novels, from Pride and Prejudice to The Great Gatsby':
        "拿来{nb}部小说，从《傲慢与偏见》到《了不起的盖茨比》，数一数里面的每一个符号。我们用香农的字母表：26个字母加空格，大写和标点都去掉。一共是<bookmark mark='a'/>{n / 1000000.0:.1f}百万个符号。<bookmark mark='b'/>最常见的是{sym_name(first)}，大约每{round(1 / p[first])}个符号里有一个。其次是{sym_name(second)}，每{round(1 / p[second])}个里有一个。",

    'f"Sorted, the familiar order appears: {top6}.':
        "排好序，熟悉的顺序就出现了：{top6}。<bookmark mark='z'/>排在最后的是{', '.join(tail4[:3])}和{tail4[3]}。最少见的{ALPHA27[rarest]}，大约每{round(1 / p[rarest], -2):,.0f}个符号才出现一次。",

    'This is a probability distribution: a number for each possibility':
        "这就是一个概率分布：每种可能都有一个数，<bookmark mark='a'/>没有一个是负的，加起来等于1。<bookmark mark='b'/>把这些柱子首尾相接，它们正好填满一根长度为1的条，每个符号占一小段，宽度就是它的概率。一个规范写下的猜测，就是把一个单位的信念，分给各种可能。",

    'But we rarely guess from nothing.':
        "不过，我们很少凭空去猜。一旦知道了前一个字母，可能性就变了。<bookmark mark='a'/>这是整张表：每一行是前一个符号，每个小方格表示在它后面，各个符号出现的可能性有多大。<bookmark mark='d'/>这就是条件概率：已知A时B的概率，等于A和B同时发生的概率，除以A的概率。",

    'f"In our books, q appears {n_q:,} times':
        "在我们的书里，q出现了{n_q:,}次，除了{n_q - n_qu:,}次之外，后面跟的都是u。<bookmark mark='a'/>所以已知q时u的概率是{q_u:.4f}。<bookmark mark='b'/>而在空格之后，几乎什么都可能出现：一个新词正要开始。",

    'Multiply that definition out, and you get a rule for whole strings.':
        "把这个定义乘开，就得到一条关于整串符号的规则。<bookmark mark='a'/>两个符号的概率，等于第一个的概率，乘以已知第一个时第二个的概率。<bookmark mark='b'/>三个的时候，把前两个看成一个事件，<bookmark mark='c'/>再代进去。",

    'And so on, one symbol at a time.':
        "依此类推，一次一个符号。<bookmark mark='a'/>一整段文本的概率，就是一连串对下一个符号的猜测的乘积，每次猜测都知道前面的一切。这就是链式法则，而且它是精确的：没有做任何假设。<bookmark mark='b'/>这也说明了，为什么一台只会猜下一个符号的机器，能给一整段文本打分，甚至写出一整段文本。",

    'f"Here\'s the chain rule as a picture.':
        "这是链式法则的一幅图。有人刚写下he said，我们想知道接下来三个字母是t、h、e的概率。<bookmark mark='a'/>第一根条是整整一个单位的信念，按最后三个符号i、d、空格，分给27个可能的下一个符号。t分到的一段，宽{ps[0]:.3f}。",

    'f"Now zoom into that sliver and share it out again':
        "现在放大这一小段，再分一次，<bookmark mark='a'/>这次按d、空格、t之后下一个字母的概率来分。h占了其中的{100 * ps[1]:.0f}%。<bookmark mark='b'/>再放大：在空格、t、h之后，字母e占了{100 * ps[2]:.0f}%。<bookmark mark='c'/>最后这一小段的宽度就是它们的乘积：{pr:.4f}，也就是整串的概率。",

    'Keep this picture in mind: nested slivers, each one a guess.':
        '记住这幅图：一层套一层的小段，每一层都是一次猜测。到第8章，同样这幅图会变成一种压缩文本的方法。',

    # ------------------------------------------------------------------ Surprise
    'Chapter two. How surprised should you be?':
        '第2章。你应该有多意外？',

    'f"If you were sure something would happen':
        "如果你确信某件事会发生，看到它发生，什么也学不到。<bookmark mark='a'/>q后面的u：不是新闻。<bookmark mark='b'/>硬币正面朝上，告诉你一点点。<bookmark mark='c'/>一个字母e，多一点。<bookmark mark='d'/>而一个z，大约每{round(1 / pz, -2):,.0f}个符号才出现一次，告诉你很多。一件事越不可能，它发生时你学到的就越多。",

    "Let's turn that into mathematics.":
        "我们把这个想法变成数学。把概率为p的事件的意外度记作s(p)。s应该是什么样的？<bookmark mark='a'/>香农提出了几条很朴素的要求。它应该只取决于p。<bookmark mark='b'/>p越大，它应该越小，一件必然发生的事，应该毫不意外。<bookmark mark='c'/>对独立事件，也就是知道其中一个，对另一个毫无帮助，所以它们的概率相乘，意外度应该相加：<bookmark mark='d'/>硬币正面朝上，同时骰子掷出5，这两件事一起的意外度，应该恰好等于各自的意外度之和。<bookmark mark='e'/>还有，p的微小变化，只应带来s的微小变化。",

    'Remarkably, those rules leave only one choice.':
        "了不起的是，这几条要求只留下一种选择。用对半分的次数来衡量概率：<bookmark mark='a'/>把p写成2的负x次方，令g(x)为这个事件的意外度。<bookmark mark='b'/>第3条说，g把和变成和。<bookmark mark='c'/>所以对每个正整数n，g(n)等于n乘以g(1)，<bookmark mark='d'/>对每个分数也一样成立。<bookmark mark='e'/>连续性填补了分数之间的数，所以对每个x，g(x)都等于x乘以g(1)。",

    'Put the probability back in, and the surprise must be a constant':
        "把概率代回去，意外度就必须是一个常数乘以p分之1的对数。<bookmark mark='a'/>这个常数只是选定一个单位。让一次公平的抛硬币恰好携带一个单位，这个单位就叫比特。概率为p的事件，意外度是以2为底、p分之1的对数，单位是比特。",

    'f"Here\'s that function.':
        "这就是那个函数。<bookmark mark='a'/>一枚硬币：1比特。骰子的一面：{math.log2(6):.2f}比特。<bookmark mark='b'/>字母e：{se:.2f}比特。字母z：{sz:.1f}。<bookmark mark='c'/>而紧跟在q后面的u：{su:.3f}比特，几乎为零。<bookmark mark='d'/>当p趋向于零，意外度会无限增大。",

    'Bits have a concrete meaning.':
        "比特有一个很具体的含义。把所有可能拿过来，对半分：<bookmark mark='a'/>左还是右，0还是1。把剩下的再对半分，一共分10次。<bookmark mark='b'/>你就把范围缩小到了1024分之一，这是一个概率为2的负10次方的事件，看到它的意外度就是10比特。每一个把可能性减半的是或否的回答，就是1比特。",

    'f"And because logs turn products into sums':
        "因为对数把乘积变成和，链式法则就变成了一个很漂亮的东西。<bookmark mark='a'/>一整段文本的意外度，等于它每个符号的意外度之和，每个符号都是在已知前面一切的条件下。<bookmark mark='b'/>这又是香农的那个句子，每个字母的意外度画成一根柱子，评判它的模型只知道前面{k}个字母。",

    'f"The tall bars are where the text surprised the model: {where}.':
        "高的柱子，就是文本让模型意外的地方：{where}。<bookmark mark='a'/>加起来，{len(sent)}个符号共{total:.0f}比特：每个符号{per:.1f}比特，{vs}。记住这个数，我们就靠它来记分。",

    'the starts of words, and words it didn':
        '词的开头，以及它没料到的词',

    "words it didn't expect, wherever they begin":
        '它没料到的词，无论从哪里开始',

    "f'under half of the {H1:.2f} bits the letter frequencies alone would give":
        '不到只用字母频率时{H1:.2f}比特的一半',

    "f'against {H1:.2f} for the letter frequencies alone":
        '而只用字母频率是{H1:.2f}',

    # ------------------------------------------------------------------ Entropy
    'Chapter three. Entropy.':
        '第3章。熵。',

    'Surprise is about one event.':
        "意外度说的是一个事件。在事件发生之前，我们可以问另一个问题：平均来说，我们预计会有多意外？<bookmark mark='a'/>把每个意外度按它出现的频率加权，再加起来。这个平均的意外度就是熵，记作H(p)。",

    'f"There\'s a nice picture of it.':
        "它有一幅很好的图。拿出第1章那根单位长度的条，<bookmark mark='a'/>每个符号一小段，宽度是它的概率，从常见到罕见排好。<bookmark mark='b'/>现在把每一小段升高到它的意外度那么高。常见的符号又宽又矮，罕见的又窄又高。<bookmark mark='c'/>熵就是总面积：英语字母是{H:.2f}比特。",

    'f"Compare a source where all twenty-seven symbols are equally likely.':
        "对比一个27个符号同样可能的信源。<bookmark mark='a'/>每一小段宽度相同，高度也相同：以2为底27的对数，{Hu:.2f}比特。这是从27个符号里取一个时，平均最多能有的意外。<bookmark mark='b'/>英语，哪怕只按单个字母来数，也低于它。这个差距就是香农所说的冗余：一个好的猜测者可以利用的结构。",

    'f"The simplest case is a coin.':
        "最简单的情形是一枚硬币。<bookmark mark='a'/>如果它是公平的，熵是1比特。<bookmark mark='b'/>让它有偏向，结果就更容易猜。90%的时候正面朝上，熵就降到{hbin(0.9):.2f}比特。<bookmark mark='c'/>一枚总是正面朝上的硬币，完全没有熵。各种结果同样可能时，熵最大。",

    'We built entropy out of surprise. Shannon went the other way.':
        "我们是用意外度搭出熵的。香农走的是另一条路。1948年，他问：任何一种不确定性的度量，应该满足什么？<bookmark mark='a'/>它应该随概率连续地变化。<bookmark mark='b'/>有n种同样可能的结果时，结果越多，不确定性应该越大。<bookmark mark='c'/>如果一次选择被拆成先后两次选择，不确定性应该等于第一次选择的，加上第二次选择的，按你遇到第二次选择的频率加权。<bookmark mark='d'/>他的例子：二分之一、三分之一、六分之一，等于先抛一枚公平的硬币，然后有一半的时候，再在三分之二和三分之一之间选一次。",

    'f"Our letters work the same way.':
        "我们的字母也是这样。<bookmark mark='a'/>先选空格、元音还是辅音：{Hg:.2f}比特。再选具体是哪一个：元音里{within[1]:.2f}比特，辅音里{within[2]:.2f}比特。<bookmark mark='b'/>加权相加，得到{H:.2f}比特：恰好就是字母的熵。",

    'And he proved that nothing else meets them.':
        "他还证明了，别的什么都满足不了这些要求。把n个同样可能的选择的不确定性记作A(n)。<bookmark mark='a'/>在s的m次方个同样可能的结果里选一个，等于连续在s个里选m次，所以按第三条要求，A(s的m次方)等于m乘以A(s)。<bookmark mark='b'/>把任何一个数夹在另一个数的两个幂之间，第二条要求就迫使A(n)等于一个常数乘以log n。<bookmark mark='c'/>现在看任何是分数的概率，n i除以N：从N个同样可能的结果里选一个，分两步，先选块，再选块里的那一个。<bookmark mark='d'/>解出H，<bookmark mark='e'/>得到的就是负K乘以p log p之和。连续性补上了无理数的概率。",

    'Up to the choice of a unit, entropy is the only consistent measure':
        '除了单位的选择，熵是唯一自洽的不确定性度量。这就是为什么这个系列的每一部分，都用同一种方式来衡量信息。',

    "That's true in general. With K possible outcomes":
        "这一点普遍成立。有K种可能结果时，熵至多是以2为底K的对数。<bookmark mark='a'/>证明只需要一个不等式。对数函数向下弯，所以对数的平均值，至多等于平均值的对数。这就是詹森不等式。<bookmark mark='b'/>熵是对数的平均值。<bookmark mark='c'/>换成平均值的对数，<bookmark mark='d'/>而p分之1的平均值，正好就是结果的个数。<bookmark mark='e'/>所以H至多是log K，当且仅当每种结果同样可能时取等号。",

    'f"Entropy also works when we know something.':
        "当我们知道一些东西时，熵同样适用。对每一个前一个字母，下一个字母都有自己的分布，也有自己的熵。<bookmark mark='a'/>为每个前一个字母画一根柱子，宽度是这个字母有多常见，高度是它后面那个字母的熵。<bookmark mark='b'/>在q之后，几乎为零：{hq:.2f}比特。<bookmark mark='c'/>在空格之后，一个新词开始了，熵是{hs:.2f}比特。",

    'f"The total area is the conditional entropy':
        "总面积就是条件熵：已知前一个字母时是{Hc:.2f}比特，<bookmark mark='a'/>而完全不知道上下文时是{H0:.2f}比特。<bookmark mark='b'/>平均来说，知道得更多，永远不会让你更不确定。我们会在第7章证明这一点。",

    # ------------------------------------------------------------------ Prefix
    'Chapter four. Surprise is measured in bits.':
        '第4章。意外度用比特来衡量。那我们就来花一些比特。',

    'f"The simplest way to send letters as bits is a fixed-length code.':
        "把字母变成比特，最简单的办法是定长编码。2的5次方是32，足够容纳我们的27个符号，<bookmark mark='a'/>所以给每个符号一个5位的数。<bookmark mark='b'/>the falcon，{len(word)}个符号，要花{nfix}比特。<bookmark mark='c'/>但这很浪费：e比z常见{ratio:.0f}倍，两者却都要花5比特。",

    'So give common symbols short codewords, like Morse code':
        "所以给常见的符号短码字，就像摩尔斯电码给e一个点。但要小心。<bookmark mark='a'/>如果e是0，t是1，a是01，那么比特01可能是e加t，也可能是a。<bookmark mark='b'/>解决办法是无前缀码：没有哪个码字是另一个码字的开头。<bookmark mark='c'/>这样，码字就是一棵二叉树的叶子。0往左，1往右，解码时从顶上往下走，走到叶子为止。",

    'Watch it decode one, one, zero, zero, one, zero':
        "看它怎么解码这一串比特：1、1、0、0、1、0、1、1、1、1、1。向右、向右、向左：这是c。回到顶端，重新开始。向左：a。向右、再向左：b。连续向右五次：f。完全不需要任何分隔符。",

    'f"Prefix-free codes obey a budget, and the tree shows why.':
        "无前缀码要遵守一个预算，这棵树说明了原因。<bookmark mark='a'/>把树一直长下去，长到最长码字的深度：{lmax}层，底部有{2 ** lmax}片叶子。<bookmark mark='b'/>长度为l的码字位于第l层，它下面的一切都不能再用了：没有别的码字可以以它开头。所以它占掉了底部2的l max减l次方片叶子。<bookmark mark='c'/>因为没有哪个码字是另一个的开头，这些份额从不重叠，所以加起来不会超过全部{2 ** lmax}片。<bookmark mark='d'/>除以2的l max次方：对所有码字，2的负码长次方之和至多是1。这就是克拉夫特不等式，出自莱昂·克拉夫特1949年的硕士论文。",

    'f"The budget is also enough.':
        "这个预算也是够用的。<bookmark mark='a'/>给我任何一组码长，只要二分之一的这些次方加起来不超过1，就一定存在恰好有这些码长的前缀码：码字从短到长依次分配，每个都取它那一层里最左边、还空着的节点。<bookmark mark='b'/>举个例子，把每个字母的意外度向上取整成整数比特。这时二分之一的这些次方加起来是{sk:.2f}，所以有这些码长的前缀码是存在的。就是它。下一章我们还会再见到它。",

    "f\"Could a code that isn't prefix-free do better?":
        "一个不是无前缀的码，能不能做得更好？<bookmark mark='a'/>这个就不是无前缀的：0是01的开头。可它照样能解码，因为每个码字都以0开头，而一个0总是意味着一个新码字。它的和是{ud_}分之{un}。<bookmark mark='b'/>这一个，和是{bd}分之{bn}，就没法解码：01既可以是a加b，也可以是c。<bookmark mark='c'/>1956年，布罗克韦·麦克米兰证明，这个预算约束着每一个能解码的码。把这个和取k次方，再乘开：每一项都是一条由k个码字组成的消息。<bookmark mark='d'/>按消息占多少比特把它们分组。<bookmark mark='e'/>如果这个码能解码，两条不同的消息永远不会给出同样的比特，所以长度为m比特的消息至多有2的m次方条，整个和至多是k乘以最长码长。",

    'f"A sum bigger than one, raised to the k, grows exponentially':
        "一个大于1的数，取k次方，是指数增长的；而k乘以一个常数，只是沿直线增长。<bookmark mark='a'/>对这个坏的码，四分之五的k次方在k等于{kx}时超过了2k：上界被打破了，所以它不可能是可解码的，事实也确实如此。<bookmark mark='b'/>所以坚持用前缀码，什么也不会损失：一个可解码的码能有的码长，前缀码也都能有。",

    # ------------------------------------------------------------------ Huffman
    'Chapter five. The best code, and the proof that it is the best.':
        '第5章。最好的编码，以及它为什么是最好的证明。',

    'Now we can prove a speed limit.':
        "现在可以证明一个速度极限了。设L是平均码长，H是熵。<bookmark mark='a'/>把两者之差写成一个和。<bookmark mark='b'/>詹森不等式，和第3章完全一样，把对数移到外面。<bookmark mark='c'/>概率约掉了，<bookmark mark='d'/>克拉夫特不等式说，剩下的至多是log 1，也就是0。<bookmark mark='e'/>所以平均码长永远不会小于熵，而且只有当每个符号恰好分到p分之1的对数那么多比特，也就是它的意外度时，两者才相等。",

    'f"Codeword lengths must be whole numbers, so round the surprises up.':
        '码长必须是整数，所以把意外度向上取整。上一章我们看到，这些码长符合克拉夫特的预算，而且每个符号多花的不到1比特。对我们的字母，是{Ls:.2f}比特。',

    'f"Which code gets closest? In 1951 David Huffman':
        "哪种编码最接近？1951年，麻省理工学院的研究生大卫·霍夫曼，在罗伯特·法诺的课上面临一个选择：参加期末考试，或者写一篇论文，找出最有效的编码。他选了论文。<bookmark mark='a'/>他的答案是：取两个最不可能的符号，这里是{f0}和{f1}，把它们并到一个新节点下，新节点的概率是两者之和。然后对剩下的再取两个最不可能的，再合并，一次又一次，<bookmark mark='b'/>合并{len(merges)}次，直到一棵树装下所有符号。",

    'f"Read off the codewords:':
        "读出码字：<bookmark mark='a'/>空格得到{ln[' ']}比特，e得到{ln['e']}，z得到{ln['z']}。<bookmark mark='b'/>平均每个符号{L:.3f}比特，只比熵多{L - H:.3f}。the falcon现在只要{nb}比特，而不是{nf}。",

    'f"Huffman proved that no prefix code does better, with a few exchanges.':
        "霍夫曼用几次交换证明了，没有哪个前缀码能做得更好。<bookmark mark='a'/>第一：如果一个更可能的符号，码字反而比一个更罕见的长，把两个码字对调，平均码长就会变短。把z的{lz}比特给e，把e的{le}比特给z，每个字母平均要多花{cost:.2f}比特。所以在最好的编码里，更可能的符号，码字绝不会更长。<bookmark mark='b'/>第二：树底部一个没有兄弟的码字，可以直接上移一层，变得更短。所以最深的码字总是成对出现。<bookmark mark='c'/>再由第一次交换，两个最罕见的符号可以放进这样一对里：在霍夫曼编码里，它们是{ho['rare'][0]}和{ho['rare'][1]}，只有最后一位不同。",

    'f"Now merge those two rarest symbols into one':
        "现在把这两个最罕见的符号合并成一个，它的概率是两者之和。<bookmark mark='a'/>小字母表的任何一个编码，只要把那片叶子一分为二，就变成原字母表的编码，而平均码长恰好增加合并后的那个概率，不管编码的其余部分是什么样。所以原问题的最好编码，就是这个更小问题的最好编码，再加上这一分。<bookmark mark='b'/>这就是霍夫曼的第一次合并，同样的论证也适用于之后的每一次合并：他搭出的树是最优的。<bookmark mark='c'/>我们检验过。把每次合并的权重加起来：{merged:.3f}，正是霍夫曼的平均码长。对这些字母，搜索每一种可能的码树形状：最好的是{same}。在{n_tr}个随机字母表上，霍夫曼编码每一次都和穷举搜索的结果一致。",

    # ------------------------------------------------------------------ Typical
    'Chapter six. Why long messages compress so well.':
        '第6章。为什么长消息压缩得这么好。',

    'f"In the last chapter, whole bits wasted up to one per symbol':
        "上一章里，整数比特让每个符号最多浪费1比特，而对长分组编码是解药。原因在这里。<bookmark mark='a'/>编出一段文本：一次抽一个字母，彼此独立，按书里的频率抽。这是英语的一个粗糙模型，但我们能对它精确地推理。量一量它每个字母的意外度。<bookmark mark='b'/>只有一个字母时，什么值都有，从{s_lo:.1f}比特到{s_hi:.1f}比特。<bookmark mark='c'/>十个字母：分布收窄了。<bookmark mark='d'/>一百个，一千个，一万个：每个字母的意外度都堆积到一个值上，{H:.2f}比特，也就是熵。它的散布从{sd[ns[0]]:.1f}比特缩小到{sd[ns[-1]]:.2f}。",

    "It's the law of large numbers.":
        "这就是大数定律。一段文本的意外度，是它各个字母意外度之和，而许多独立意外度的平均值，会稳定在它们的均值上，也就是熵。<bookmark mark='a'/>香农在1948年证明了它，麦克米兰和布雷曼又把它推广到有记忆的信源，比如真实的文本。它有一个拗口的名字：渐近均分性。",

    'Call a sequence typical if its surprise per symbol is within':
        "如果一个序列每个符号的意外度，离熵不超过一个小小的ε，就称它是典型的。<bookmark mark='a'/>于是每个典型序列的概率都接近2的负nH次方。<bookmark mark='b'/>由渐近均分性，典型集几乎占据了全部概率。<bookmark mark='c'/>数一数它们：它们的概率加起来不能超过1，<bookmark mark='d'/>所以它们至多有2的n乘以H加ε次方个；<bookmark mark='e'/>又因为它们几乎占了一切，所以至少大约有2的nH次方个。你将会见到的几乎每一个序列，都是大约2的nH次方个序列中的一个，它们的可能性都差不多。",

    'f"Here is the typical set, drawn.':
        "这是把典型集画出来的样子。拿一个更简单的信源：一枚硬币，按书里空格的频率{q:.3f}写下一个空格。<bookmark mark='a'/>把所有2的n次方个序列排成一行，每个一样宽，从最可能的、一个空格都没有的，排到最不可能的。<bookmark mark='b'/>下面是同样这些序列，每个的宽度等于它的概率。典型的序列涂成金色。<bookmark mark='c'/>n等于{show[0]}时，它们是全部序列的{100 * 2 ** r0['log2_frac']:.0f}%，占了{100 * r0['P']:.0f}%的概率。<bookmark mark='d'/>现在让序列变长。",

    'f"In the top row, the gold shrinks to a sliver':
        "在上面一行，金色缩成一条细缝，然后细到看不见。在下面一行，它不断扩展，直到几乎填满一切。<bookmark mark='a'/>到{show[-1]}个符号时，典型序列只占全部序列的2的负{-r1['log2_frac']:.0f}次方，却{missed}。<bookmark mark='b'/>而那个最可能的单个序列，一个空格都没有，根本不是典型的：你几乎永远不会见到它。",

    "f'all but one part in {1 / miss / 1000000.0:,.0f} million of the probability":
        '占了全部概率，只差{1 / miss / 1000000.0:,.0f}百万分之一',

    "f'{100 * r1['P']:.4f} percent of the probability":
        '占了{100 * r1[\'P\']:.4f}%的概率',

    'f"That gives the source coding theorem.':
        "这就给出了信源编码定理。<bookmark mark='a'/>要压缩n个符号：如果序列是典型的，先发一个0，再发它在典型集清单里的编号：大约nH比特。如果不是，就发一个1，再把序列原样发出去。这种情况很少发生，所以平均下来，每个符号大约花H比特。<bookmark mark='b'/>而且没有哪个编码能做得更好：任何短到能省下更多比特的清单，都会漏掉大部分典型序列，也就漏掉了几乎全部概率。<bookmark mark='c'/>就连上一章那个简单的取整编码，用在整个分组上，也会逼近熵：分组长{int(ns[0])}时每个符号{rate[0]:.3f}比特，分组长{int(ns[-1])}时是{rate[-1]:.4f}，而熵是{h:.4f}。",

    'f"Now think about English.':
        "现在来想想英语。n个字母的字符串，一共有27的n次方个。<bookmark mark='a'/>就算只按字母频率，典型的字符串也只占其中2的负{gap:.2f}n次方：对一页{page:,}个字母，是2的负{gap * page:,.0f}次方。<bookmark mark='b'/>按香农每个字母1比特的估计，真实的文本是一个小得多的角落。<bookmark mark='c'/>一个语言模型的全部工作，就是找到这个角落；要写东西时，就从里面抽取。应该怎么抽，第5部分会讲。",

    # ------------------------------------------------------------------ CrossEntropy
    'Chapter seven. What happens when your guesses are wrong?':
        '第7章。如果你的猜测错了，会怎样？',

    'Codes and guesses are the same thing.':
        "编码和猜测是同一回事。一个在某个符号上花l比特的编码，等于是在赌这个符号的概率是2的负l次方。那如果赌错了呢？<bookmark mark='a'/>假设数据来自p，编码却是为模型q设计的。每个符号要花q分之1的对数那么多比特，平均下来，我们付出的是交叉熵：p乘以q分之1的对数，再求和。",

    'f"Picture it as before.':
        "像之前一样画出来。<bookmark mark='a'/>用正确的概率，面积就是熵，{H:.2f}比特。<bookmark mark='b'/>现在用一个把e和z弄反了的模型。每个e，大约每{round(1 / p[ie])}个符号就有一个，现在要花{-np.log2(q[ie]):.1f}比特。面积增大到{CE:.2f}。",

    'f"Split the log in two':
        "把对数拆成两部分，<bookmark mark='a'/>交叉熵就分成了两笔代价。第一笔是p的熵：世界本身的随机性，任何编码都消除不了。<bookmark mark='b'/>第二笔是犯错的代价：q相对于p的库尔巴克–莱布勒散度，1951年提出。<bookmark mark='c'/>把e和z对调，每个符号多花{KL:.2f}比特。均匀地猜字母，多花{lt['KL_uniform']:.2f}。而我们30本书的字母频率，用在《马耳他之鹰》的段落上，{books_said}。",

    'are wrong by less than a hundredth of a bit':
        '错得不到百分之一比特',

    "f'are wrong by {kb:.3f} bits":
        '错了{kb:.3f}比特',

    'Is being wrong always a cost?':
        "犯错总是要付出代价吗？是的，证明和第3章用在均匀分布上的那个一样。<bookmark mark='a'/>对数向下弯，所以对数的平均值，至多等于平均值的对数。<bookmark mark='b'/>负的散度，是以p为权重，对q除以p的对数求的平均。<bookmark mark='c'/>把对数移到外面。<bookmark mark='d'/>里面的p约掉了，<bookmark mark='e'/>剩下的是q的总和，也就是1。1的对数是0。",

    'So the divergence is never negative':
        "所以散度永远不会是负的，而且只有当q等于p时才为零，这也是詹森不等式取等号的唯一情形。<bookmark mark='a'/>真相就是最好的编码。这个不等式以约西亚·威拉德·吉布斯命名，他在统计力学里用过它。<bookmark mark='b'/>它还还上了第3章欠下的债：知道X之后熵的下降，也是一个散度，所以不可能是负的。平均来说，知道得更多永远没有坏处。<bookmark mark='c'/>这个下降有一个名字，叫互信息。它会有自己的一章。",

    'Here is why all of this matters for AI.':
        "这就是这一切对AI的意义所在。<bookmark mark='a'/>每一个大语言模型训练时要最小化的损失，正是这个：对真实文本的每一个词元，在已知前面词元的条件下，取q分之1的对数，再求平均。<bookmark mark='n'/>通常用自然对数ln，以e为底，所以单位是奈特而不是比特：1奈特大约是1.44比特。<bookmark mark='b'/>它就是世界上的文本和模型之间的交叉熵。<bookmark mark='c'/>训练只能缩小散度那一部分；<bookmark mark='d'/>语言本身的熵，是任何模型都无法低于的下限。",

    '"One more property, which will matter a lot later':
        "还有一个性质，后面会非常重要：散度不是对称的。假设真实的p有两个峰，而我们的模型q只能是一条钟形曲线：一个平滑的鼓包，由它的中心在哪里、有多宽来决定。哪条钟形曲线最好？这取决于我们按哪个方向去量。<bookmark mark='a'/>最小化q相对于p的散度，也就是我们刚见过的训练损失，<bookmark mark='b'/>{('pulls q wide, to cover both peaks: it ends with exactly p\\'s mean and spread.' if wide else 'pulls q wide, to cover both peaks.')}",

    "pulls q wide, to cover both peaks: it ends with exactly p's mean and spread.":
        '会把q拉宽，盖住两个峰：最后它的均值和散布恰好与p相同。',

    'pulls q wide, to cover both peaks.':
        '会把q拉宽，盖住两个峰。',

    '"The other way round, <bookmark mark=\'a\'/> q is punished':
        "反过来，<bookmark mark='a'/>q在p没有概率的地方放了概率，就会受罚，所以{('it squeezes into a single peak and ignores the other. ' if one_peak else 'it narrows toward one peak. ')}每种拟合，按另一种标准都很糟：宽的那条曲线，按第二种方式量是{d['rev_at_fwd']:.2f}比特；窄的那条，按第一种方式量是{d['fwd_at_rev']:.1f}比特。<bookmark mark='b'/>覆盖一切，还是认定一个：这个选择会在第20部分的变分自编码器里再次出现，也会在第27部分的蒸馏和基于人类反馈的强化学习里出现。",

    'it squeezes into a single peak and ignores the other.':
        '它挤进一个峰里，不管另一个。',

    'it narrows toward one peak.':
        '它朝一个峰收窄。',

    'Here are the two losses for every possible bell curve':
        "这是对每一条可能的钟形曲线，两种损失的取值：横向是它的中心，纵向是它的宽度。<bookmark mark='a'/>按一个方向量，只有一个山谷。梯度下降一次又一次地朝着让损失下降最快的方向迈出一小步，从哪里出发都能找到那条宽曲线。<bookmark mark='b'/>按另一个方向量，有两个山谷，每个峰对应一个，最后落在哪里，取决于从哪里出发。",

    # ------------------------------------------------------------------ Arithmetic
    'Chapter eight. The best code for a good guesser.':
        '第8章。给好猜测者的最好编码。',

    'f"Huffman\'s code has one flaw.':
        "霍夫曼编码有一个缺陷。每个符号都要花整数个比特，至少1个。<bookmark mark='a'/>q后面的u只携带{info:.3f}比特，却还是要花整整1比特。<bookmark mark='b'/>对字母频率来说，这还能忍受；但一个真正懂英语的模型，每个符号的意外度只有大约1比特，甚至更少，而一个逐符号的编码永远不能低于1比特。对长分组编码能解决这个问题，可是一百个字母一组的码表需要27的100次方个条目，而一个读上下文的模型，每个字母都会改变它的猜测。<bookmark mark='c'/>解决办法是把整条消息编成一个数，一次一个猜测。",

    'f"Arithmetic coding, worked out by Jorma Rissanen and Richard Pasco':
        "算术编码，由约尔马·里萨宁和理查德·帕斯科在1976年提出。我们已经见过它的核心：链式法则那一层套一层的小段。<bookmark mark='a'/>从单位区间开始，按模型对第一个字母的猜测来分割。t分到一段，宽{steps[0]['p']:.3f}。现在把这一段的两个端点写成二进制。<bookmark mark='b'/>它们的前{c0}位相同。这一段里的任何数都这样开头，所以这几位已经确定了。",

    'f"Then zoom in and split again':
        "然后放大，再分割：h、e、空格、f、a、l、c、o、n。<bookmark mark='a'/>每个字母都按它的概率把区间缩小，区间越窄，两个端点相同的前导位就越多。这些位一确定，就可以发送出去。<bookmark mark='b'/>一个可能的字母几乎不缩小区间，只花一个零头比特。一个不太可能的字母，比如{hs_word}里的{hs_sym}，模型只给了它{100 * hs['p']:.1f}%，就要花{hs['bits']:.1f}比特。",

    'f"After ten letters, the interval has width':
        "十个字母之后，区间的宽度是2的负{info:.2f}次方：整条消息的概率。<bookmark mark='a'/>最后，找出最短的二进制小数，使得以这些数位开头的每个数都落在区间内。<bookmark mark='b'/>这里需要{n}比特。<bookmark mark='c'/>比一比：定长编码{nf}比特，霍夫曼{nh}比特，算术编码{n}比特，而信息量是{info:.2f}比特。",

    'Why within two bits?':
        "为什么不超过2比特？设P是消息的概率，也就是它的区间宽度。<bookmark mark='a'/>选一个长度l：P分之1的对数，向上取整，再加1。<bookmark mark='b'/>于是一串l位比特代表一个宽度为2的负l次方的小区间，至多是P的一半。<bookmark mark='c'/>这些小区间铺满整条线，所以在低端处或之后开始的第一个小区间，一定在高端之前结束：它整个落在消息的区间里，它的l位比特就锁定了这条消息。<bookmark mark='d'/>所以l位比特总是够用，而l小于信息量加2。",

    'Decoding runs the same steps.':
        "解码走的是同样的步骤。接收方有这些比特，还有一份完全相同的模型。<bookmark mark='a'/>这些比特代表一个数。它落在第一次分割中t的那一段里，所以第一个字母是t。<bookmark mark='b'/>放大：它落在下一次分割中h的那一段，然后是e，依此类推，一次一个字母，直到消息被原样还原。",

    'f"A real coder can\'t keep fractions with thousands of digits.':
        "真正的编码器没法保存有几千位的小数。它把区间存成两个整数，低端和高端，这里是{R}位，实际中是32位。<bookmark mark='a'/>第一个字母缩小区间。<bookmark mark='b'/>现在两端的第一位相同了：它确定了。把它发出去，再把装着区间的那一半放大一倍，让它重新填满整个范围：这就是一次放大。<bookmark mark='c'/>如果区间跨过中点，却落在中间那一半里，下一位还不知道。编码器照样以中点为中心放大，并记下有一位在等待；等到下一个确定的位出来时，它会被翻转，跟着一起出来。<bookmark mark='d'/>一个字母接一个字母，缩小，放大，比特就源源不断地流出来。",

    'f"At the end, a couple of bits close it off':
        "最后，再用几位把它收尾：the falcon用了{nb}比特，{cmp_said}精确编码器的{ne}比特。始终是整数，而且从不超过寄存器的长度。",

    'the same as': '和……一样，等于',
    'one fewer than': '比……少1位，相比',
    'one more than': '比……多1位，相比',

    'f"Does the rounding cost much?':
        "取整会花很多吗？我们把整段《马耳他之鹰》，{n:,}个字母，送进一个由我们最好的计数模型驱动的32位编码器。<bookmark mark='a'/>在这个模型下，它的信息量是{ideal:,.0f}比特。<bookmark mark='b'/>把概率取整成{show[-1]}位的计数，编码器在整段里只比这多发了{fine:.1f}比特。{(f' Round them to 8 bits and it costs {coarse:,.0f} extra bits.' if coarse is not None else '')}{dip_said}<bookmark mark='c'/>寄存器只要比计数宽几位，就几乎无关紧要。算术编码几乎什么也不浪费：你付出的，就是模型的意外度。",

    "f' Round them to 8 bits and it costs {coarse:,.0f} extra bits.":
        '取整成8位，就要多花{coarse:,.0f}比特。',

    "f' With {dips[0]}-bit counts it even came out a few bits under":
        '用{dips[0]}位的计数，它甚至还少花了几比特：取整给了罕见字母多一点概率，而这段文字恰好用到了它们。',

    'This is the hinge of the whole part.':
        "这是整个这一部分的枢纽。<bookmark mark='a'/>把任何一个能预测的模型交给算术编码，就得到一个压缩器，每个符号的输出大约是q分之1的对数那么多比特：文本的长度乘以模型的交叉熵。<bookmark mark='b'/>反过来，任何压缩器都定义了一个模型：一段要花l比特的文本，等于被赋予了2的负l次方的概率。<bookmark mark='c'/>所以预测得好和压缩得好，是同一种本事。在最后一章，我们会让一个语言模型来当压缩器。",

    # ------------------------------------------------------------------ Counting
    'Chapter nine. So far, our models have only counted.':
        '第9章。到目前为止，我们的模型只会计数。计数能走多远？',

    'f"In 1948, Shannon showed what counting can do':
        "1948年，香农让计数模型自己写东西，展示了计数能做到什么。<bookmark mark='a'/>每个符号同样可能，得到的是噪声。<bookmark mark='b'/>用对的字母频率，还是噪声，但纹理对了。<bookmark mark='c'/>按我们书里前一个字母后面跟什么来选每个字母，音节就出现了。<bookmark mark='d'/>用两个字母的上下文，出现了短词。<bookmark mark='e'/>用四个，大多是真的词。<bookmark mark='f'/>用六个，出现了短语：{six}。<bookmark mark='g'/>改成数整个的词，得到的东西几乎有点韵律了。",

    'The rule behind all of these is simple.':
        "这些背后的规则很简单。<bookmark mark='a'/>在给定上下文时，下一个符号的概率，等于它在书里跟在这个上下文后面的次数，除以这个上下文出现的次数。<bookmark mark='b'/>这是最自然的估计，在第11章我们会看到，对这些书本身来说，它也是最好的估计。",

    'f"So let\'s score the counting models.':
        "我们来给计数模型打分。对每一种上下文长度，从0个字母到14个，量一量每个字母的比特数。<bookmark mark='a'/>先在它数过的那些书上。上下文越多，比特越少，在{ks[-1]}个字母时，一路降到每个字母{plug[-1]:.2f}比特。我们在没有上下文和一个字母上下文时的数字，{plug[0]:.2f}和{plug[1]:.2f}，<bookmark mark='b'/>和香农1951年根据印刷的统计表做的估计{sh27[1]:.2f}和{sh27[2]:.2f}很接近。",

    'f"But on new text, the Falcon passage':
        "但在新的文本，也就是《马耳他之鹰》的段落上，<bookmark mark='a'/>情况就不同了。上下文一开始有帮助：<bookmark mark='b'/>最好的是{best}个字母的上下文，每个字母{test[best]:.2f}比特。再往后就变差了{(f\", and with {ks[-1]} letters of context it's worse than knowing nothing but letter frequencies.\" if test[-1] > test[0] else f', up to {test[-1]:.2f} bits with {ks[-1]} letters of context.')}",

    "f\", and with {ks[-1]} letters of context it's worse":
        '，用{ks[-1]}个字母的上下文时，甚至比只知道字母频率还差。',

    "f', up to {test[-1]:.2f} bits with {ks[-1]} letters of context.":
        '，用{ks[-1]}个字母的上下文时，升到{test[-1]:.2f}比特。',

    'f"The reason is that contexts multiply.':
        "原因是上下文会成倍增长。<bookmark mark='a'/>《马耳他之鹰》段落里所有5个字母的上下文，{100 * seen[5]:.0f}%在书里的某个地方出现过。而{kL}个字母的上下文，只有{100 * seen[kL]:.0f}%出现过。<bookmark mark='b'/>可能的{kL}个字母的上下文大约有10的{e20:.0f}次方个，而书里只有{nctx[kL] / 1000000.0:.1f}百万个。<bookmark mark='c'/>一个书里从没见过的上下文，模型毫无依据；在它后面从没见过的字母，概率会是零：意外度无穷大。",

    'The patch is older than computers.':
        "这个补救办法比计算机还要古老。1814年，皮埃尔–西蒙·拉普拉斯问：如果一件事在n次尝试中发生了s次，下一次它发生的可能性有多大？<bookmark mark='a'/>假设在观察之前，0到1之间的每一个机会都同样可信。按每个机会对你所见的解释程度给它加权，<bookmark mark='b'/>答案就是s加1，除以n加2。<bookmark mark='c'/>他的例子是日出：五千年的日出，1826213天，得出明天太阳升起的赔率是1826214比1。<bookmark mark='d'/>对我们的27个符号，同样的推理是：给每个计数加1。没有哪个会得到零概率。<bookmark mark='e'/>把加1换成加α，就是让我们的曲线保持有限的那种平滑，α在留出的文本上选定。",

    'f"How much does alpha matter?':
        "α有多重要？<bookmark mark='a'/>这是从万分之一到10的每一个α，在四种上下文长度下，在《马耳他之鹰》段落上的得分。<bookmark mark='b'/>{short_said}：它的上下文都见过几百万次。<bookmark mark='c'/>用{ol}个字母的上下文时，段落里{100 * un:.0f}%的字母，出现在书里从没在这个上下文后面见过它的地方，而大多数上下文只见过寥寥几次。给每个计数加1，就淹没了证据：拉普拉斯法则每个字母比在留出文本上选出的α，也就是{A[best[ol]]:.2f}，多花{cost:.2f}比特。好的平滑，是一个关于你没见过什么的问题。第7部分会好好地回答它。",

    "For one letter of context, Laplace's rule is as good as anything":
        '对一个字母的上下文，拉普拉斯法则不比任何别的差',

    'f"For one letter of context, Laplace\'s rule costs':
        '对一个字母的上下文，拉普拉斯法则多花{T[short][lap] - T[short][best[short]]:.3f}比特',

    'f"And how does a counting model learn? It reads, and counts.':
        "计数模型是怎么学习的？它读，然后数。这是其中四个，上下文分别是1、3、5、8个字母，随着它们数过的书越来越多，在《马耳他之鹰》的段落上打分。<bookmark mark='a'/>读了一千个字母之后，一个字母的上下文最好，{B[orders[0]][0]:.2f}比特：短的上下文见得多，数得快，而长的上下文几乎还没遇到过它们的上下文。{story}<bookmark mark='z'/>读完全部{A[-1] / 1000000.0:.0f}百万个字母时，{(f'{words[o_long]} letters is still behind, at {B[o_long][-1]:.2f}: it would need far more text than we have.' if lead[-1] != o_long else f'{words[o_long]} letters finally leads.')}能数的越多，值得用的上下文就越长。",

    "f'{words[o_long]} letters is still behind":
        '{words[o_long]}个字母的上下文仍然落后，{B[o_long][-1]:.2f}比特：它需要的文本，比我们有的多得多。',

    "f'{words[o_long]} letters finally leads.":
        '{words[o_long]}个字母的上下文终于领先了。',

    'f"Here\'s the five-letter model writing, as it reads':
        "这是5个字母上下文的模型一边读、一边写的样子，每次都从同样的开头出发，掷同样的骰子。<bookmark mark='a'/>读了一千个字母之后，{recite}它写出的东西里有{100 * share[0]:.0f}%，也就是红色的部分，是从它读过的那一点点文字里，一字不差地抄来的，一抄就是{L}个字母以上。<bookmark mark='b'/>读了一万个之后，是{100 * share[1]:.0f}%。<bookmark mark='c'/>从十万个起，{nothing}：它自己把像模像样的词串在一起，<bookmark mark='d'/>它在《马耳他之鹰》段落上的得分，从每个字母{bits[0]:.2f}比特变成了{bits[-1]:.2f}。",

    'it can only recite: ': '它只会背诵：',
    'it mostly invents, but ': '它大多是自己编的，但',
    'nothing is copied': '没有一点是抄来的',
    'almost nothing is copied': '几乎没有抄来的',
    "f'at most {100 * max(late):.0f} percent is copied":
        '抄来的至多{100 * max(late):.0f}%',

    'This is the first appearance of the central problem of machine learning.':
        "这是机器学习核心问题的第一次登场。<bookmark mark='a'/>一个模型可以几乎完美地拟合它学过的数据，却仍然在新数据上猜得很差。两者之间的差距，叫作泛化。<bookmark mark='b'/>计数还有一个更深的局限：每个上下文都是一座孤岛。它分不清the dog barked和the hound barked是相似的，所以没法把从一个学到的东西借给另一个。<bookmark mark='c'/>更好的平滑在第7部分，泛化在第8部分，而能在相似上下文之间共享所学的模型，靠的是向量和网络，在第3部分和第9部分。",

    # ------------------------------------------------------------------ Shannon1951
    'Chapter ten. Back to Shannon':
        '第10章。回到香农的猜字游戏，现在我们有了读懂它的工具。',

    "Here's Shannon's key observation.":
        "这是香农的关键洞见。假设接收方有一个和猜测者一模一样的双胞胎：同样的知识，同样的习惯。<bookmark mark='a'/>发送方在文本上玩猜字游戏，只把猜测次数发出去。<bookmark mark='b'/>接收方让双胞胎去猜，次数说第三次，就取双胞胎的第三次猜测。文本就原样出来了。",

    'So the guess counts carry all the information in the text.':
        "所以猜测次数携带了文本的全部信息。<bookmark mark='a'/>文本的熵不会超过猜测次数的熵，而后者又至多等于各个猜测次数出现频率的熵。数一数猜了几次，就得到了英语信息量的一个上界。",

    'f"Let\'s play the game with our counting model':
        "我们让上一章的计数模型当猜测者，在《马耳他之鹰》段落的{n:,}个字母上玩这个游戏。<bookmark mark='a'/>它第一次就猜中的情况占{100 * q[0]:.0f}%，第二次猜中的占{100 * q[1]:.0f}%，后面还拖着一条长尾巴。",

    'f"From those frequencies, the upper bound is':
        "根据这些频率，上界是每个字母{up:.2f}比特。<bookmark mark='a'/>香农还用同样的数字证明了一个下界：{lo:.2f}比特。对这样一个猜测者来说，这段文字真正的信息量就在两者之间。",

    'f"Shannon\'s own subjects did far better.':
        "香农自己的受试者做得好得多。<bookmark mark='a'/>给他们100个字母的上下文，他的估计是印刷英语每个字母{lo_h:.1f}到{hi_h:.1f}比特，<bookmark mark='b'/>而我们用6个字母上下文的计数猜测者是{float(g['lower']):.1f}到{float(g['upper']):.1f}。<bookmark mark='c'/>差别在于知识：人们认识词，懂语法，知道习语，知道故事在讲什么，也知道世界是怎么运转的。",

    'Later estimates landed in the same place':
        "后来的估计也落在同一个地方：每个字母大约1.3比特，用的是让人对下一个字母下注、而不是去猜的游戏版本。<bookmark mark='a'/>要像人一样猜，机器就得知道人所知道的东西。这就是标杆。",

    # ------------------------------------------------------------------ Likelihood
    'Chapter eleven. So far our models were counted.':
        '第11章。到目前为止，我们的模型都是数出来的。现在来看一个模型怎样学习。',

    'Learning starts from a principle stated by Ronald Fisher in 1922':
        "学习始于罗纳德·费希尔在1922年提出的一个原则：选择那个让你实际看到的数据最有可能出现的模型。这就是似然：模型给每一个观测的概率的乘积。<bookmark mark='a'/>对它取负对数，再除以观测数，就得到平均意外度。<bookmark mark='b'/>把观测按取值归类：这就是数据自身的频率p帽与模型之间的交叉熵。<bookmark mark='c'/>它又等于数据的熵，加上模型相对于数据的散度。",

    'So maximum likelihood, minimum cross-entropy':
        '所以最大似然、最小交叉熵、与数据的最小散度，是同一个目标。这就是第7章的损失，从另一边看过去。',

    'If the model is allowed to be any distribution at all':
        "如果模型可以是任何一个分布，<bookmark mark='a'/>当模型等于数据自身的频率时，散度最小，为零。<bookmark mark='b'/>所以第9章的计数模型就是最大似然模型。这也正是它们过拟合的原因：它们完美地拟合了那些书，却没有任何东西把它们拉向更一般的东西。",

    "Counting doesn't generalize. Neural networks do.":
        "计数不会泛化。神经网络会。<bookmark mark='n'/>神经网络是一叠简单的步骤：乘以一张数表，再把结果弯一弯，然后重复；表里所有的数都要不断调整，直到它猜得好为止。它给出猜测的方式不一样。对每一个可能的下一个词元，它的最后一步会算出一个分数，叫作logit：<bookmark mark='a'/>任意实数，可正可负。<bookmark mark='b'/>要变成概率，先取指数：e的z次方能把任何数变成正数，z每增加1，它就大约乘以2.7。<bookmark mark='c'/>再除以总和，让它们加起来等于1。这就是softmax。分数越高，概率越大，而且没有哪个会得到零概率。",

    'To learn, the network needs to know which way to nudge each score.':
        "要学习，网络需要知道每个分数该往哪边推。<bookmark mark='n'/>这正是导数衡量的东西：把一个输入轻轻推一点点，其他输入保持不动，输出会变化多少。<bookmark mark='a'/>用这些分数写出正确答案y的意外度。<bookmark mark='b'/>对分数z k求导。第一项在k等于y时给出负1。第二项就是softmax本身。<bookmark mark='c'/>所以导数是：对正确答案，q k减1；对每个错误答案，就是q k。",

    "In words: the model's guess, minus the truth.":
        "用一句话说：模型的猜测，减去真相。<bookmark mark='a'/>在整个数据集上平均，梯度就是q减去p帽。比模型预期出现得更多的，把它的分数往上推；其余的往下推。每一个语言模型，不管多大，最后一步都正是这样。",

    'Here is gradient descent in action.':
        "来看梯度下降的实际运行。假设数据是come后面的100种接续，<bookmark mark='a'/>模型一开始五个分数都相等，所以每个猜测都是20%。每一步，每个分数都移动负的η乘以q减p帽：模型猜少了的往上，猜多了的往下。<bookmark mark='l'/>η就是学习率，也就是每一步的大小：太小，学习就慢得像在爬；太大，又会冲过谷底。<bookmark mark='b'/>我们来运行一下。",

    'f"The guesses slide toward the data\'s frequencies':
        "猜测朝着数据的频率滑过去，交叉熵也降向它的下限：数据的熵，{H:.2f}比特，任何模型都无法超越。<bookmark mark='a'/>这就是训练的全部，缩微版。一个真实的模型有几十亿个参数，而不是五个分数，它的分数还取决于上下文，但传到它们那里的信号，正是这同一个差：猜测，减去真相。",

    # ------------------------------------------------------------------ Information
    'Chapter twelve. What the past tells you about the future.':
        '第12章。过去告诉了你多少关于未来的事。',

    'f"In chapter seven, knowing X lowered the entropy of Y':
        "在第7章，知道X之后，Y的熵平均会下降。这个下降有一个名字：互信息。<bookmark mark='a'/>它是你知道一件事之后，猜另一件事时能省下的比特数，而且它是对称的：Y告诉你的关于X的，和X告诉你的关于Y的一样多。它也是一个散度，是联合分布和两者独立时的分布之间的散度，所以永远不会是负的。<bookmark mark='b'/>在我们的书里，下一个字母携带{Hx:.2f}比特；知道它前面那个字母时，是{Hc:.2f}比特。<bookmark mark='c'/>所以相邻的字母共享{I:.2f}比特。<bookmark mark='d'/>往前两个字母，共享{I2:.2f}比特，而第二个字母单独只共享{Isk:.2f}：字母合在一起，说的比分开时多。",

    'Now process what you know.':
        "现在来处理你知道的东西。假设Z是由Y算出来的，用什么函数都行，哪怕是带噪声的。<bookmark mark='a'/>链式法则可以用两种方式拆开Y和Z合起来告诉你的关于X的东西：先是Y，再加上Z额外带来的，而那是零。<bookmark mark='b'/>或者先是Z，再加上Y额外带来的。<bookmark mark='c'/>比较这两种拆法，Z告诉你的关于X的，永远不会比Y多。再怎么处理，也创造不出信息。",

    "f\"Let's watch it happen in our books.":
        "我们在书里看看它是怎么发生的。<bookmark mark='a'/>只保留前一个字母的类别：空格、元音还是辅音。{I:.2f}比特里，留下了{Ig:.2f}比特。<bookmark mark='b'/>或者把它弄乱：把一部分字母换成随机的字母。噪声越多，它告诉你的就越少，一直降到零。<bookmark mark='c'/>两样都做，损失更多。每一条曲线都待在前一条的下面。<bookmark mark='d'/>这对学习机器也是一条定律。一个网络无论从它的上下文里算出什么，它的特征对下一个词元的了解，都不会超过上下文本身。",

    'f"How far back does that reach?':
        "这能回溯多远？量一量一个字母和d个位置之后那个字母之间的互信息，用上我们所有的书。<bookmark mark='a'/>相邻的字母共享{mi[0]:.2f}比特。在一个词里面，它下降得很快。<bookmark mark='b'/>但它并没有消失。{tail}在这些坐标轴上，每个刻度都是前一个的10倍，横轴纵轴都是，所以幂律显示为一条直线。",

    'It decays slowly, like a power of the distance':
        '它衰减得很慢，像距离的幂次一样，一直到一千个字母以外。',

    'It keeps decaying, slowly, as far as we measured.':
        '在我们测量的范围里，它一直在缓慢地衰减。',

    "A counting model can't produce a tail like that":
        "计数模型产生不了这样的尾巴：它那几个字母上下文以外的任何影响，都被切断了，它所建模的依赖关系按指数消失，<bookmark mark='x'/>每多一个字母就缩小同样的倍数，在这些坐标轴上，会直直地掉出底部。<bookmark mark='a'/>真实的文本，在每一个距离上，都会回报你所记住的东西。要猜得好，模型需要长的记忆，还需要一种办法，找出过去当中要紧的部分。这就是注意力的用处，在第13部分。",

    # ------------------------------------------------------------------ Knowledge
    'Chapter thirteen. What does a model have to know':
        '第13章。要猜得好，模型需要知道什么？',

    'f"Let\'s look at what a strong model knows that a weaker one doesn\'t.':
        "我们来看看，一个强的模型知道什么，而弱的模型不知道。这是《马耳他之鹰》段落里的一段，切成词元，也就是模型一次读、一次猜的那些小块，<bookmark mark='a'/>每个都按2019年的GPT-2对它有多意外来着色：意料之中是暗的，出乎意料是亮的。<bookmark mark='b'/>再看同一段在2025年的Qwen3下的样子。它的方块{('darker almost everywhere' if tb < ta else 'no darker')}：{tb:.0f}比特，而不是{ta:.0f}比特。",

    'darker almost everywhere': '几乎处处都更暗',
    'no darker': '并没有更暗',

    '"Look where they differ. <bookmark mark=\'a\'/> " + brand':
        "看看它们在哪里不同。<bookmark mark='a'/>{brand}<bookmark mark='b'/>还有telephone：GPT-2为它付出{bd['telephone'][0]:.1f}比特，Qwen3只要{bd['telephone'][1]:.1f}比特，因为两段之前，一个电话铃响了。<bookmark mark='c'/>只给Qwen3看这一段，telephone就要花它{alone:.1f}比特。它记得：上一章的长尾巴，在这里派上了用场。",

    'f"After Bull, GPT-2 doesn\'t expect Durham':
        "在Bull之后，GPT-2没料到Durham，{bd['Durham'][0]:.1f}比特，也没料到tobacco，{bd['tobacco'][0]:.1f}比特。Qwen3料到了，{bd['Durham'][1]:.1f}和{bd['tobacco'][1]:.1f}：Bull Durham是一个真实的烟草品牌，它在训练中的某处学到了这一点。",

    "f'After Bull, Durham costs GPT-2":
        "在Bull之后，Durham花了GPT-2 {bd['Durham'][0]:.1f}比特，Qwen3 {bd['Durham'][1]:.1f}比特；tobacco，{bd['tobacco'][0]:.1f}和{bd['tobacco'][1]:.1f}。Bull Durham是一个真实的烟草品牌。",

    '"Facts work the same way.':
        "事实也是一样。问埃菲尔铁塔在哪座城市，<bookmark mark='a'/>问《傲慢与偏见》的作者是谁，<bookmark mark='b'/>或者问金的化学符号，知道答案的模型，在答案出现时花的比特要少得多。<bookmark mark='c'/>算术更难：{arith}",

    "f'the 2025 model gives four {100 * p4:.0f} percent":
        '2025年的模型给four的是{100 * p4:.0f}%，给five的却有{100 * p5:.0f}%。',

    'even the 2025 model hedges.':
        '就连2025年的模型也拿不准。',

    'f"So here\'s the ladder.':
        "所以，这就是阶梯。<bookmark mark='a'/>字母频率让你降到{H0:.1f}比特。拼写，也就是几个字母的上下文，降到{Hk:.1f}。<bookmark mark='b'/>再往下，模型就得学会词和语法，关于世界的事实，以及故事到目前为止发生了什么，<bookmark mark='c'/>一直降向人所需要的大约1比特。<bookmark mark='d'/>没有人告诉模型去学这些。把它推到那里的，只是一个数：它为每次猜测付出的比特。要预测文本，它就得为写出这些文本的世界建模。",

    # ------------------------------------------------------------------ Units
    'Chapter fourteen. Before the final scores, a word about units.':
        '第14章。在最后的计分之前，先说说单位。',

    "f\"Language models don't read letters.":
        "语言模型读的不是字母。每个模型都用自己的词表，把文本切成词元。<bookmark mark='a'/>这是《马耳他之鹰》段落里的一段，按GPT-2的方式切开，<bookmark mark='b'/>再按Qwen3的方式切开。<bookmark mark='c'/>在整个段落上，GPT-2需要{g2['tokens']:,}个词元，平均每个{g2['chars_per_token']:.2f}个字符；Qwen3的词表更大，需要{q3['tokens']:,}个。",

    'f"A model\'s loss is reported per token':
        "模型的损失是按每个词元来报告的，所以它的大小取决于一个词元装了多少文本。<bookmark mark='a'/>要紧的是总数：词元数乘以每词元比特数，等于字符数乘以每字符比特数。<bookmark mark='b'/>这是我们的各个模型在这段文字上的成绩。计数模型一次读一个字符：每个词元就是一个字符。<bookmark mark='c'/>{verdict}<bookmark mark='d'/>困惑度，也就是2的每词元比特数次方，也继承了同样的问题：它说的是模型在多少个同样可能的词元之间做选择，而词元各不相同。<bookmark mark='e'/>所以要按每个字符，或者按文件的每个字节来比。这就是为什么记分牌数的是每字符比特数。",

    'f"Per token, the counting model looks like the winner':
        "按词元算，计数模型看起来是赢家：{cnt['bits_per_token']:.2f}比特，对GPT-2的{g2['bits_per_token']:.2f}；困惑度{cnt['ppl_token']:.1f}，对{g2['ppl_token']:.1f}。可它的词元只是单个字符。按字符算，它差了{cnt['bpc'] / g2['bpc']:.1f}倍。",

    "f'Per token, the counting model scores":
        "按词元算，计数模型是{cnt['bits_per_token']:.2f}比特，GPT-2是{g2['bits_per_token']:.2f}；按字符算，是{cnt['bpc']:.2f}和{g2['bpc']:.2f}。",

    'This is how the field measures it, too.':
        "这个领域也是这样衡量的。2024年，香港科技大学和腾讯的研究者拿来31个公开的语言模型，<bookmark mark='a'/>测量每个模型压缩新收集的文本的本事，文本来自网页、代码和论文，单位是每字符比特数，因为用他们的话说，每词元比特数没法直接比较；<bookmark mark='b'/>再把它和这些模型在12个关于知识、编程和数学的基准测试上的平均分放在一起。<bookmark mark='c'/>这些点几乎落在一条直线上，相关系数是负0.93。一个模型压缩得越好，它能做的就越多。",

    # ------------------------------------------------------------------ Scoreboard
    'Chapter fifteen. Time to keep score.':
        '第15章。该记分了。',

    'f"Here\'s the board, for the Falcon passage as printed':
        "这是记分牌，针对印刷原样的《马耳他之鹰》段落：大写、标点，什么都在。<bookmark mark='a'/>纯文本文件给每个字符花8比特。<bookmark mark='b'/>这段文字只用了{raw['passage_symbols']}种不同的符号，所以在它们之间盲猜，要花以2为底{raw['passage_symbols']}的对数：{b['uniform']:.2f}比特。<bookmark mark='c'/>在我们30本书里数出的字母频率，把它降到{b['order0']:.2f}，<bookmark mark='d'/>一个字符的上下文，降到{b['order1']:.2f}。",

    'f"Next, the compressors on your computer.':
        "接下来，是你电脑上的压缩器。<bookmark mark='a'/>{comp_said}。它们事先对英语一无所知。它们只从这段文字本身边读边学。<bookmark mark='b'/>我们最好的计数模型，先读了30本书，看前面{k}个字符，得到{b['best']:.2f}。",

    'f"And then, the neural language models.':
        "然后，是神经语言模型。<bookmark mark='a'/>2019年的GPT-2，最小的版本：{b['GPT-2 small']:.2f}比特。它最大的版本，{gxl:.2f}。<bookmark mark='b'/>2025年的Qwen3：6亿参数的模型{q06_said}，<bookmark mark='c'/>40亿参数把它降到每个字符{b['Qwen3-4B']:.2f}比特。<bookmark mark='d'/>作为对比，香农对人的估计，只算字母，是{hum['lo']:.1f}到{hum['hi']:.1f}。",

    'already matches the largest GPT-2': '已经和最大的GPT-2持平',
    'already beats the largest GPT-2': '已经超过了最大的GPT-2',
    "f'gets {q06:.2f}": '得到{q06:.2f}',

    'f"In file sizes: the passage is':
        "换成文件大小：这段文字存成纯文本是{kb['ascii']:.1f}KB，用gzip是{kb['gzip']:.1f}KB，<bookmark mark='a'/>用Qwen3驱动一个算术编码器是{kb['Qwen3-4B']:.1f}KB。<bookmark mark='b'/>从计数的{bits['best']:.1f}比特，到{('under one' if low < 1 else f'{low:.2f}')}，这一跃就是这个系列要讲的：这些模型学到了什么，又是怎么学到的。",

    'under one': '1以下',

    'f"Arithmetic coding turns any predictor into a compressor':
        "算术编码能把任何一个预测者变成压缩器，所以我们造了一个。<bookmark mark='a'/>GPT-2 small一次一个词元地读《马耳他之鹰》段落的开头，把它的概率交给第8章那个32位编码器。出来的是{nb}字节，只比GPT-2自己的意外度多{z['bits'] - z['ideal']:.1f}比特，<bookmark mark='b'/>{ok_said}<bookmark mark='c'/>同样这{z['chars']:,}个字符，xz需要{comp['xz']:,}字节：是它的{ratio:.1f}倍。",

    'and decoded it back, with a second run of the model, letter for letter.':
        '再让模型重新跑一遍，把它一个字母不差地解码回来。',

    'but decoding it back with a second run of the model did not reproduce it exactly':
        '可是让模型重新跑一遍来解码，没能把它原样还原：两次运行在某个概率的最后几位上有了分歧。',

    'f"There\'s a catch.':
        "这里有个问题。解压器需要模型，而模型很大。<bookmark mark='a'/>GPT-2 small把整段文字压到{size_g2 / 1000:.1f}KB，可它的权重要占{mb:,.0f}MB。把权重算进去，文件比这段文字本身大{adj['GPT-2 small']:,.0f}倍。<bookmark mark='b'/>2024年，DeepMind的一个团队把这一点写进了一篇论文的标题：《语言建模就是压缩》。在1GB的维基百科上，他们700亿参数的模型把文本压到原来大小的8.3%，而gzip是32%，xz是23%。把它的权重算进去，就是14000%。尽管它是在文本上训练的，它压缩图像和音频也比PNG和FLAC好。<bookmark mark='c'/>赫特奖由马库斯·赫特在2006年设立，它把一切都算进去：2026年7月创下的纪录，把那1GB连同解压器一起，装进100.4MB，每个字符0.80比特，用的是一个把许多预测者混合起来的程序。<bookmark mark='d'/>预测就是压缩；而预测者本身的大小，也是账单的一部分。",

    "And the board isn't finished.":
        "记分牌还没写完。随着系列推进，我们会搭建自己的模型，把它们的成绩加上去：<bookmark mark='a'/>第7部分有更好的计数，<bookmark mark='b'/>第9部分有一个神经网络，<bookmark mark='c'/>第10部分有一个带记忆的网络，<bookmark mark='d'/>第13部分有我们自己的小Transformer，每一个都在这同样的30本书上训练，在这同一页上打分。",

    # ------------------------------------------------------------------ Outro
    'f"Let\'s take stock.':
        "我们来盘点一下。我们把猜测写成概率分布，链式法则又把它们变成了一整段文本的分数。意外度必须是对数，而熵，也就是平均意外度，是唯一自洽的不确定性度量。前缀码活在克拉夫特的预算之内，霍夫曼编码是其中最好的，而长的典型序列让编码能够达到熵，却不能更低。我们见识了错误模型的代价，也就是交叉熵，以及它里面散度的两个方向。算术编码表明，预测和压缩是同一回事，GPT-2把我们的段落压缩了{('and gave it back' if z['ok'] else 'with it')}。计数模型用失败给我们展示了泛化，互信息则告诉我们，文本能记住多远的过去。",

    'and gave it back': '，又把它还原了回来',
    'with it': '',

    'Almost everything here comes back.':
        '这里的几乎每一样都会再次出现。链式法则是语言模型生成文本的方式，也是推理模型把思考说出来的方式。交叉熵是我们在整个系列里要一直最小化的损失。散度的两个方向，会在变分自编码器里，也会在让模型符合人们意愿的对齐里再次出现。从模型中抽取典型的文本，在第5部分。压缩会在研究规模时回来，也会在最后，当我们问这些模型能被托付什么时回来。',

    'Here are six problems to try':
        '这里有六道题，从分组法则到拉普拉斯接续法则。在这里暂停，把它们做一做；完整的解答在这一部分的笔记里。',

    'Next time: the other road to intelligence':
        "下一次：通向智能的另一条路，也是更早出现的那一条。艾伦·图灵的问题；会搜索的机器，一视同仁地搜，<bookmark mark='a'/>或者朝着目标有引导地搜；会下棋、会证明定理的程序；专家系统；以及随之而来的寒冬。符号主义时代。",

    'This part followed the first chapters of Cover and Thomas':
        '这一部分沿着科弗和托马斯的《信息论基础》，以及麦凯的《信息论、推理与学习算法》的前几章展开，两本书都走得远得多。这些论文都值得一读，先从香农的那两篇开始。感谢观看，第2部分见。',
}

PHRASES = {
    'the space': '空格',
    'space': '空格',
    'space, e, t, a, o, n': '空格、e、t、a、o、n',
    'falcon': 'falcon',
    'the same': '同样的4.127',
    'gives Paris': '给Paris',
    'three': '3',
    'five': '5',
    'eight': '8',
}
