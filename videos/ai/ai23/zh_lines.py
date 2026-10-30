"""Chinese narration for ai23: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第23部分：每一种感官都是词元'

CHAPTERS = {
    'Hook': '同一个序列',
    'History': '1. 我们是怎么走到这里的',
    'BPE': '2. 合并即压缩',
    'Unigram': '3. 给每一种切法一个概率',
    'Bits': '4. 一个词元值多少',
    'Bytes': '5. 字节与分块',
    'VQ': '6. 学一本码本',
    'FSQ': '7. 不用码本的编码',
    'Sampling': '8. 给声音采样',
    'Codec': '9. 神经编解码器',
    'Audrey': '10. 从Audrey到隐马尔可夫模型',
    'CTC': '11. 连接时序分类',
    'Whisper': '12. 大规模地听',
    'TTS': '13. 说话',
    'Clip': '14. 让图片和文字配对',
    'VLM': '15. 会看的模型',
    'Omni': '16. 所有感官一起来',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    'A transformer reads a sequence of tokens.':
        "Transformer读的是一串词元。那么，模型怎么看一张图片，怎么听一段声音？<bookmark mark='a'/>先把一切都变成词元：文字变成词的片段，图片变成各个小块的编码，声音变成一段段时间的编码。<bookmark mark='b'/>然后它们就是同一个序列，一个模型就能读它，也能写它。",

    'Every sense poses the same questions.':
        "每一种感官都提出同样的问题。一个词元应该是什么？一句话、一张图、一秒钟的语音，各需要多少个？这些编码又是怎么学出来的？<bookmark mark='a'/>我们会沿着七十年的答案走一遍：1952年一台能听懂十个数字的机器，随后的统计式识别器，字节对编码，CTC，WaveNet，CLIP和Whisper，一直到边听边说的模型。<bookmark mark='b'/>我们还会在制作这段视频的电脑上，搭出它们的小版本：分词器，码本，一个语音编解码器，一个语音识别器，还有一个给图片配说明文字的模型。",

    'This is Part 23 of AI, Built.':
        "这是《人工智能，从零搭建》的第23部分。<bookmark mark='a'/>这一部分讲：文本的分词器，以及一个词元值多少比特；向量量化、它的码本，以及码本怎样失效；采样、频谱和神经音频编解码器；听，从模板到CTC和Whisper；说，一直讲到为这段视频配音的模型；还有让图片和文字配对，从CLIP一直到能看、能听、能说的模型。",

    # ---------------------------------------------------------------- History
    'Chapter one. How we got here.':
        '第1章。我们是怎么走到这里的。',

    'Machines were listening long before they could read.':
        "机器会听，比会读早得多。<bookmark mark='a'/>1952年，贝尔实验室造出了Audrey，一架电子设备，能听懂一个人说的十个数字，一百次里对九十七到九十九次。<bookmark mark='b'/>到了1970年代，识别器学会了拉伸时间去对齐模板；接着，在IBM和卡内基梅隆大学，人们把语音当成隐马尔可夫模型来处理，也就是第7部分的统计方法，它统治了三十年。<bookmark mark='c'/>2012年，神经网络接管了声音模型；2022年，Whisper能转写将近一百种语言。<bookmark mark='d'/>说话这条线也一样：从1939年世界博览会上用键盘弹出来的Voder，到共振峰合成器和拼接录音，再到2016年的WaveNet，一个一次写一个采样点的网络。",

    'Then speech became language modeling:':
        "接着，语音合成变成了语言建模：先是Tacotron，然后是2023年的VALL-E，它像语言模型写词那样，把一个人的声音写成编码。<bookmark mark='a'/>文本需要自己的单位。以词为单位的模型，碰到没见过的词就卡住；以字符为单位，序列又太长。1994年，菲利普·盖奇发表了一种压缩文件的方法：反复替换最常见的字节对；2016年，它成了把文本切成词元的标准做法，后来又出现了基于字节、基于概率的版本。<bookmark mark='b'/>图片和文字在2014年前后相遇，那时网络学会了给照片配说明；2021年，CLIP从网上四亿张带说明的图片里学习；到2023年，把一个视觉编码器接到语言模型上，它就能谈论一张图片了。",

    "<bookmark mark='a'/> In the last few years the threads met.":
        "<bookmark mark='a'/>最近几年，这几条线汇到了一起。一旦语音、图片和文字都成了词元，一个Transformer就能把它们全部读写：2024年的GPT-4o，Moshi，还有通义千问的全模态模型。<bookmark mark='b'/>这一部分从底层把这个想法搭起来：词元是什么、值多少，编码怎样学出来，声音和图片怎样变成序列，各种感官又怎样配对。",

    # ---------------------------------------------------------------- BPE
    'Chapter two. Merges as compression.':
        '第2章。合并即压缩。',

    'f"A tokenizer decides what a model\'s units are.':
        "分词器决定模型的基本单位是什么。用整个词吗？<bookmark mark='a'/>在我们小说里的两百万个字符中，有{types:,}个不同的词，可测试段落里仍有{100 * oov:.1f}%的词从没出现过。一个以词为单位的模型，对这些词无话可说。<bookmark mark='b'/>单个字符永远不会不够用，但一句话会变成一个很长的序列，而注意力的代价随长度的平方增长。字节对编码找的是介于两者之间的单位。",

    'In 1994 Philip Gage described a way to compress a file:':
        "1994年，菲利普·盖奇描述了一种压缩文件的方法：找出出现最频繁的字节对，把它处处换成一个新符号，然后重复。2016年，里科·森里希、巴里·哈多和亚历山德拉·伯奇用它来为机器翻译切分词语。从单个字符出发，合并最常见的相邻对，然后重复。<bookmark mark='a'/>这是在我们小说上学到的头几次合并：先是空格和t，h和e，然后是词的开头和结尾，很快就是整个词。每个新符号就是一个词元。",

    'f"Why is this compression?':
        "这为什么是压缩？<bookmark mark='a'/>被合并的那一对每出现一次，两个符号就变成一个，所以一次用上n次的合并，正好让文本缩短n个符号。<bookmark mark='b'/>合并k次之后，文本长度就是原来的长度减去这些次数的总和，<bookmark mark='c'/>而挑最常见的一对，就是每次都先拿最大的节省：一个贪心的压缩器。<bookmark mark='d'/>在我们的小说上，光是第一次合并就省下{n1:,}个符号；合并{len(b['merges']):,}次之后，文本长度只剩按字符算的{100 * L[-1] / L0:.0f}%。合并越往后越罕见，省下的也越来越少。",

    'f"The more merges, the bigger the tokens.':
        "合并越多，词元越大。<bookmark mark='a'/>这是同一句话，先切成字符，再看合并{sizes[1]:,}次、{sizes[2]:,}次和{sizes[3]:,}次之后的样子。<bookmark mark='b'/>合并{n_max:,}次时，一个词元平均覆盖测试段落的{n8:.1f}个字符，所以Transformer只用几分之一的步数就读完同样的文本。<bookmark mark='c'/>BERT的分词器WordPiece按另一条规则合并：挑那些组成部分很少分开出现的对，也就是最能提高文本似然的合并。它在我们小说上的头几次合并，都是总是一起出现的罕见组合。<bookmark mark='d'/>真实的词表，从GPT-2的五万个词元，到Gemma 3的超过二十五万个。",

    # ---------------------------------------------------------------- Unigram
    'Chapter three. A probability for every cut.':
        '第3章。给每一种切法一个概率。',

    'Byte-pair encoding cuts each word one way':
        "字节对编码对每个词只有一种切法，由合并的顺序决定。2018年，工藤拓提出改用一个模型。<bookmark mark='a'/>一个片段组成的词表，每个片段有一个概率。把一个词切成若干片段，这种切法的得分是各片段概率的乘积，而这个词的概率是所有切法之和。<bookmark mark='b'/>这是用我们的模型学到的片段，写出armchair的几种方式。<bookmark mark='c'/>分词器保留概率最大的那种切法。",

    'Every cut of a word is a path through a lattice.':
        "一个词的每一种切法，都是一张格上的一条路径。<bookmark mark='a'/>在每两个字母之间放一个节点，词表里的每个片段画一条弧。一种切法，就是从第一个节点走到最后一个节点的一条路径。<bookmark mark='b'/>所有切法之和可以从左往右算：到达节点j的概率，是所有终止在那里的弧之和，来自之前的每一个节点，这正是第7部分隐马尔可夫模型的前向算法。<bookmark mark='c'/>把求和换成取最大，就得到最好的切法。<bookmark mark='d'/>再从右往左算一遍，就得到每个片段预计会被用到几次：训练正需要这个。",

    'f"Training starts from far too many pieces:':
        "训练从多得多的片段开始：文本里最常见的子串，第一轮之后有{n0:,}个。<bookmark mark='a'/>然后是期望最大化，第7部分的EM：对每个词的每一种切法求和，算出每个片段预计被用到几次，再按比例设定它的概率。<bookmark mark='b'/>接着剪枝：对每个片段，算一算没有它时似然会下降多少，保留最重要的四分之三，以及每一个单字母，然后重复。<bookmark mark='c'/>这是模型自己对小说的度量，以每字符比特数计，随着词表缩小而变化：词表越小，代价越多，从第一轮到{sizes[-1]:,}个片段，一共多了{y[-1] - y[0]:.2f}比特。",

    'f"How different are the two?':
        "两者差别有多大？<bookmark mark='a'/>各用{V:,}个片段，在测试段落上，{verdict}：BPE每个词元{cpb:.2f}个字符，一元模型{cpu:.2f}个，有{100 * float(u[f'differ{V}']):.0f}%的词切法不同。<bookmark mark='b'/>一元模型还可以随机采样切法，而不总取最好的，这样训练中的模型会看到同一个词的好几种写法；工藤拓称之为子词正则化。<bookmark mark='c'/>他的SentencePiece库能在原始文本上运行这两种方法，把空格也当作一个普通符号，T5、前两代Llama和Gemma都用它来切分文本。",

    "the unigram model's tokens are a little longer":
        "一元模型的词元稍长一些",
    "BPE's tokens are a little longer":
        "BPE的词元稍长一些",
    'the two come out almost the same length':
        "两者的长度几乎一样",

    # ---------------------------------------------------------------- Bits
    'Chapter four. What a token is worth.':
        '第4章。一个词元值多少。',

    'f"A tokenizer changes what a model has to guess.':
        "分词器改变了模型要猜的东西。预测大词元的模型，每次要猜的更多，所以它的每词元比特数没法和字节模型相比。<bookmark mark='a'/>公平的货币是第1部分的每字符比特数：文本的总意外度，除以它的长度。<bookmark mark='b'/>分子分母同时除以词元数，<bookmark mark='c'/>每字符比特数就等于每词元比特数除以每词元字符数。<bookmark mark='d'/>我们4096个片段的BPE模型，在测试段落上每个词元花{bpt:.2f}比特，一个词元覆盖{cpt:.2f}个字符：每字符{b:.2f}比特。",

    'f"Now a fair race.':
        "现在来一场公平的比赛。五种分词器：原始字节，以及各用1024个和4096个片段的BPE和一元模型。<bookmark mark='a'/>每一种都用同样的小Transformer，同样的计算预算，各跑三个种子。<bookmark mark='b'/>词表越大，每个词元越贵，因为输出层随词表增大，所以这些模型走的步数更少。但它们的每个词元携带的文本更多：在预算之内，4096个片段的BPE模型读了{cb / 1000000.0:.1f}百万个字符，字节模型读了{cbytes / 1000000.0:.1f}百万个。",

    'f"Here they learn, all fifteen runs,':
        "这是它们学习的过程，全部十五次训练，随着预算的消耗，在留出文本上以每字符比特数衡量。<bookmark mark='a'/>在测试段落上，{LM_SAY[best]}最好，每字符{m[best]:.2f}比特；{LM_SAY[worst]}最差，{m[worst]:.2f}比特；不同种子之间相差从不超过{spread:.2f}。<bookmark mark='b'/>{verdict}",

    "f'{pairs[0]}, and {pairs[1]}.":
        "{pairs[0]}；{pairs[1]}。",

    'Why does the tokenizer matter at all?':
        "分词器到底为什么重要？<bookmark mark='a'/>词元越大，每一次浮点运算买到的文本越多，同样128个词元的窗口，装下的段落也越多。<bookmark mark='b'/>但词表越大，输出层越大，词元也越罕见，每个在训练中出现的次数越少。<bookmark mark='c'/>在有几十亿参数的模型里，输出层只占代价的一小部分，所以真实的词表有十万个词元甚至更多。<bookmark mark='d'/>这是我们的两个模型在段落开头几个词之后写出的东西，温度0.8。分词器是每个分数背后的一个隐藏选择，而每字符比特数让比较保持诚实。",

    # ---------------------------------------------------------------- Bytes
    'Chapter five. Bytes and patches.':
        '第5章。字节与分块。',

    'f"Tokenizers fail in their own ways.':
        "分词器有自己的失败方式。<bookmark mark='a'/>词表没见过的字符会变成未知。藏在一个词元里的字母，很难数清、很难拼写。而一个主要在英语上学出来的词表，会把其他语言切成更多的词元，于是它们花费更多。<bookmark mark='b'/>GPT-2在2019年的办法，是在字节上做BPE。任何文本在UTF-8里都是一串字节，每个字符一到四个字节，只有256种可能的取值，所以以字节为起始字母表，就永远不会有未知。<bookmark mark='c'/>{own}",

    'f" The series\' own language model':
        "本系列自己的语言模型，也就是第18到30部分训练和剖析的那个，用的是一个有{int(b['novels_vocab']):,}个词元的字节级BPE；在测试段落上，平均每个词元{float(b['novels_cpt']):.2f}个字符。",

    'f"Could a model skip the tokenizer and read bytes?':
        "模型能不能跳过分词器，直接读字节？<bookmark mark='a'/>谷歌的ByT5在2021年就这么做了，代价是序列比BPE长好几倍。<bookmark mark='b'/>2023年，Meta的MegaByte把字节分成固定大小的块：一个大Transformer看这些块，一个小Transformer写出每块里的字节。<bookmark mark='c'/>但固定的块，在一个可预测的词尾上花的力气，和在出人意料的词首上一样多。2024年12月，Meta的字节潜变量Transformer让数据自己决定：一个小的字节模型先往前读，哪里对下一个字节没把握，哪里就开始一个新块。这里，同样的{len(bs)}个字节，变成{n_fix}个固定块，或者{n_ent}个按熵划分的块。",

    'Here is that idea on our own byte model,':
        "这是这个想法在我们自己的字节模型上的样子，也就是第4章的字节级Transformer，读测试段落中的一行。<bookmark mark='a'/>每根柱子是模型对下一个字节有多没把握：它的熵，以比特计。点是它对实际出现的那个字节有多意外。<bookmark mark='b'/>在一个词的开头，下一个字母完全开放；在词的中间，读过几个字母之后，剩下的几乎已经确定。<bookmark mark='c'/>只要熵越过一个阈值，就开始一个新块，这些块就会跟着信息走：文本出人意料的地方块短，可预测的地方块长。",

    'f"How well do the patches follow the surprise?':
        "这些块跟意外度跟得有多紧？扫一遍阈值，对每个阈值，量出平均块长，以及模型的总意外度中，落在块的第一个字节上的比例。<bookmark mark='a'/>当块的平均长度和我们的BPE词元一样，都是{bl:.2f}个字节时，{100 * start:.0f}%的字节是块的开头，它们承担了{100 * Y[j]:.0f}%的意外度。<bookmark mark='b'/>BPE词元的开头，数量差不多，只承担{100 * bs_:.0f}%。<bookmark mark='c'/>这就是分块的理由：把大模型的步数花在信息所在的地方。Meta的研究发现，在同样的计算量下，字节分块的模型能赶上用分词器的模型，一直到80亿参数。",

    # ---------------------------------------------------------------- VQ
    'Chapter six. Learning a codebook.':
        '第6章。学一本码本。',

    'f"Text comes in pieces; pictures and sound are continuous.':
        "文本本来就是一块一块的；图片和声音却是连续的。要把它们变成词元，我们需要一个形状的词汇表：一本码本。<bookmark mark='a'/>把每张字母图片切成四乘四的小块，用k均值找出十六个典型的小块：<bookmark mark='k'/>先随便猜十六个，把每个小块分给离它最近的猜测，再把每个猜测移到分给它的小块的平均处，然后重复。<bookmark mark='b'/>现在一张图片就是一串0到15的数字：每个小块换成离它最近的码。<bookmark mark='c'/>码越多，复制品越接近原图；这些数字是留出小块上每个像素的误差，分别对应{size_list}和{sizes[-1]:,}个码。",

    'In a real model the codebook is learned with the encoder and decoder,':
        "在真正的模型里，码本是和编码器、解码器一起学出来的，就像第20部分的VQ-VAE，而这会遇到一个难题。<bookmark mark='a'/>编码器的每个输出z，都被换成离它最近的码。挑最近的，是一次跳跃，没有梯度。<bookmark mark='b'/>解决办法是直通技巧：前向时用码；反向时假装什么都没发生，把码上的梯度直接交给z。<bookmark mark='c'/>还有两项把它们拴在一起：一项把每个被选中的码拉向选它的那些输出；另一项是承诺损失，乘以β，让每个输出靠近它被吸附到的码。<bookmark mark='d'/>而弱点就在这里：没人选的码，一点梯度也得不到。它永远不动，也永远不会被选中。",

    'f"We trained a small VQ autoencoder on the letters:':
        "我们在字母上训练了一个小的VQ自编码器：每个字母变成一个五乘五的码网格，码本有{K}个码；每种方法都用同样的{steps:,}步预算，三个种子。<bookmark mark='a'/>按教科书的做法，{state}，这是在留出字母上、对三个种子的平均。<bookmark mark='b'/>一种流行的修补，是把每个码更新为选它的那些输出的滑动平均，即指数移动平均，相当于在线的k均值。这里{verdict_ema}：{u['ema'].mean():.0f}个码在用。<bookmark mark='c'/>{works}，并把五十步没被用到的码，重启到这一批里一个随机的输出上：{u['restart'].mean():.0f}个码在用。",

    "f'the codebook collapses:":
        "码本坍缩了：到最后，{K}个码里只有{u['vq'].mean():.0f}个在用",
    "f'most of the codebook survives:":
        "码本大部分还活着：{K}个码里有{u['vq'].mean():.0f}个在用",
    'What works is to start the codes on real encoder outputs':
        "管用的办法是让码从真实的编码器输出开始",
    'Another repair is to start the codes on real encoder outputs':
        "另一种修补是让码从真实的编码器输出开始",

    'f"A fairer measure than counting codes is perplexity:':
        "比数码更公平的度量是困惑度：携带同样信息量所需的、被均匀使用的码的个数。<bookmark mark='a'/>普通VQ达到{p['vq']:.0f}，EMA是{p['ema']:.0f}，带重启的EMA是{p['restart']:.0f}。<bookmark mark='b'/>再看重建：{names[best]}把留出字母重建得最好，每个像素误差千分之{1000 * e[best]:.1f}。<bookmark mark='c'/>重启在音频编解码器里是标准做法；另一种治法是干脆不要学出来的码本，这是下一章的主题。",

    # ---------------------------------------------------------------- FSQ
    'Chapter seven. Codes without a codebook.':
        '第7章。不用码本的编码。',

    'In 2023 Fabian Mentzer and colleagues at Google':
        "2023年，谷歌的法比安·门策尔和同事问：码本到底需不需要学？<bookmark mark='a'/>有限标量量化：把编码器的输出映射成几个数，把每个数压进一个固定范围，再四舍五入到几个等级之一。<bookmark mark='b'/>码本就是所有组合构成的网格：四个数、每个四级，就是256个码，八比特，和我们的VQ一样。<bookmark mark='c'/>四舍五入同样没有梯度，所以还是用直通技巧。但没有什么可坍缩的：没有码会被搁浅，因为没有码是学出来的。",

    'Months later, Lijun Yu and colleagues':
        "几个月后，于立军和同事在他们的视频分词器MAGVIT-v2里把它推到了极致：免查表量化。<bookmark mark='a'/>每个数只保留正负号。d个数就有2的d次方个码，也就是一个立方体的各个角，一个二十五万的词表根本不需要表。<bookmark mark='b'/>为了让这些码物尽其用，他们加了一个熵项：每个输出都要有把握地靠近某一个角，而在整批数据里，所有角都要被用到。",

    'f"All five, at 256 codes,':
        "五种方法，都是256个码，同样的网络、同样的步数、三个种子。<bookmark mark='a'/>困惑度：FSQ是{p['fsq']:.0f}，LFQ是{p['lfq']:.0f}，普通VQ是{p['vq']:.0f}。{fsq_cmp}；{lfq_cmp}。<bookmark mark='b'/>论误差，{say[order[0]]}第一，千分之{1000 * e[order[0]]:.1f}；其次是{say[order[1]]}，千分之{1000 * e[order[1]]:.1f}；{say[order[-1]]}最后，千分之{1000 * e[order[-1]]:.1f}。谷歌团队的论点不是FSQ全面胜出，而是它不需要VQ的任何修补就能和VQ相当。",

    'FSQ uses its grid better than plain VQ uses its codebook':
        "FSQ用它的网格，比普通VQ用它的码本更充分",
    "LFQ, at its paper's entropy weight, does not":
        "LFQ在论文的熵权重下则不然",
    'FSQ uses its grid no better than plain VQ uses its codebook':
        "FSQ用它的网格，并不比普通VQ用它的码本更充分",

    'f"One more trick, the one sound codecs rely on:':
        "还有一个技巧，声音编解码器都靠它：分级量化。<bookmark mark='a'/>第一级粗略地编码这个小块；第二级编码第一级漏掉的部分；然后第三级、第四级。小块被重建为它们的和。<bookmark mark='b'/>它比一本大码本更好吗？在比特数相同时不是。{at8}<bookmark mark='c'/>但残差的各级能一直往下走，而单一码本跟不上：十六比特需要一张65536项的表，而四级、每级16个码，只用64项就达到{rv[-1]:.3f}。这就是残差向量量化，几乎每个神经音频编解码器里都有它。",

    "f'At eight bits one codebook of 256 codes, error {e1[k8]:.3f}, beats":
        "在八比特时，一本256个码的码本，误差{e1[k8]:.3f}，胜过两级、每级16个码的{rv[1]:.3f}。",
    "f'At eight bits one codebook of 256 codes, error {e1[k8]:.3f}, loses to":
        "在八比特时，一本256个码的码本，误差{e1[k8]:.3f}，输给了两级、每级16个码的{rv[1]:.3f}。",

    # ---------------------------------------------------------------- Sampling
    'Chapter eight. Sampling sound.':
        '第8章。给声音采样。',

    'A microphone measures air pressure,':
        "麦克风测的是气压，而计算机按固定的节拍保留它的样本。多快才够快？<bookmark mark='a'/>取一个频率为f的纯音，每秒采样f_s次。<bookmark mark='b'/>把频率加上f_s，每个采样点的相位都多转了整数圈，所以样本完全不变。<bookmark mark='c'/>而因为余弦是偶函数，f_s减f给出的样本和f一样。<bookmark mark='d'/>所以样本只能分辨零到采样率一半之间的频率。一个七千赫的音调，每秒采样八千次，恰好落在一个一千赫的音调上。反过来就是奈奎斯特和香农的采样定理：一个不含采样率一半以上成分的信号，完全由它的样本决定。",

    'f"We can check it numerically.':
        "我们可以用数值验证。<bookmark mark='a'/>把一千、三千、五千和七千赫的音调各以每秒八千次采样，找出各自频谱的峰：{peaks}千赫。<bookmark mark='b'/>四千赫以上的每个频率，都折回到下面的频段里，形成一条锯齿：这就是混叠。",

    'f"Speech shows why this matters.':
        "语音说明了这为什么重要。<bookmark mark='a'/>在一个留出的Kokoro声音说的这句话里，{100 * above:.0f}%的能量在两千赫以上。<bookmark mark='b'/>每四个样本只留一个，也就是每秒四千个，这部分能量并不会消失，而是折到剩下的频段里：按我们的度量，两千赫以下剩下的部分里，有{100 * fold:.0f}%是折进来的能量。<bookmark mark='c'/>先滤波，再每四个留一个，两千赫以下的频段就是干净的。<bookmark mark='d'/>所以每个采样率都是一个取舍：电话用八千赫，Whisper用一万六千赫，大多数音频编解码器用两万四千赫。",

    'f"A wave is hard to read,':
        "波形很难读，所以语音模型看的是它的频谱，一片一片地看。<bookmark mark='a'/>把信号切成25毫秒的窗，每10毫秒一个，每个窗用汉宁窗收尾，再做傅里叶变换：这就是短时傅里叶变换，一张频率对时间的图。<bookmark mark='b'/>人耳大致按比例来听音高，所以把频率合并成在梅尔刻度上均匀分布的频带：一千赫以下窄，以上宽。<bookmark mark='c'/>对每个频带的能量取对数，保留最高的八个数量级，就正好是Whisper听到的东西：每10毫秒80个对数梅尔频带。我们自己的实现，和transformers库的结果相差不到10的负{abs(exp)}次方。",

    # ---------------------------------------------------------------- Codec
    'Chapter nine. Neural codecs.':
        '第9章。神经编解码器。',

    'For most of a century digital sound meant samples:':
        "将近一个世纪里，数字声音就意味着样本：电话每秒六万四千比特，CD每秒一百四十万。<bookmark mark='a'/>2021年，谷歌的尼尔·泽吉杜尔和同事端到端地学出了一个编解码器。SoundStream的编码器把波形变成每秒七十五个向量，残差向量量化把每个向量变成几个编码数字，解码器再把编码变回波形，三者一起训练，用频谱损失加上GAN的判别器。<bookmark mark='b'/>他们还在训练时随机丢掉一些量化级，于是一个模型能工作在每一种码率。Meta在2022年推出的EnCodec，码率从每秒1.5到24千比特。<bookmark mark='c'/>如今语音模型的分词器还要更低：一两千比特。",

    'f"We built a small one, with one simplification.':
        "我们自己搭了一个小的，做了一处简化。教一个网络造出波形，需要的算力远超这台电脑，所以我们的编解码器编码的是Whisper读的那张图，也就是第8章的对数梅尔频谱，把图变回声音的事留给声码器。<bookmark mark='a'/>一层带步长的卷积，把这张图每秒100帧降到每秒{hz}帧。<bookmark mark='b'/>每一帧最多经过八级残差量化，每级256个码，八比特，所以一级每秒花{hz * bits}比特。<bookmark mark='c'/>训练时随机丢掉量化级，于是同一个模型可以跑在每秒{', '.join((str(hz * bits * n) for n in stages[:-1]))}或{hz * bits * stages[-1]:,}比特。<bookmark mark='d'/>它有{params / 1000000.0:.1f}百万个参数，在十个声音、{tr_min:.0f}分钟的Kokoro语音上训练了{S:,}步，损失很朴素：重建出的图的平均误差。这是它学着重建一个从没听过的声音说的一句话。",

    'f"How good is it?':
        "它有多好？<bookmark mark='a'/>这是那句留出的话在各个码率下的重建：一级保留了大致的形状，八级保留了多得多的细节。<bookmark mark='b'/>一个粗糙但公平的测试：Whisper直接读这样的图，那它还能听懂我们重建的图吗？在{n_w}句留出的话上，Whisper的词错误率{trend}，从每秒{bps[0]}比特时的{100 * w_lo:.0f}%，到每秒{bps[-1]:,}比特时的{100 * w_hi:.0f}%，原始的图是{100 * ow:.0f}%；两个种子。<bookmark mark='c'/>在每秒{bps[-1]:,}比特时，这些编码只有用32位数存储那张图的{ratio:.0f}分之一，是样本本身的{pcm:.0f}分之一。真正的编解码器还得造出波形，要用判别器、多得多的数据和多得多的步数；我们这个只是要把这种取舍展示出来。",

    'f"Speech tokens come in two kinds.':
        "语音词元有两种。<bookmark mark='a'/>编解码器的声学词元，携带的是听起来怎样：嗓音、房间、细节。我们的编解码器各级用得{spread}：困惑度从{min(ppl):.0f}到{max(ppl):.0f}，满分256。<bookmark mark='b'/>语义词元携带的是说了什么，它们来自一个自监督的语音模型，也就是第24部分要搭的那类模型，再聚类成编码。2022年，谷歌的AudioLM生成语音时，先写语义词元，再写声学词元。<bookmark mark='c'/>后来两者合进了一个编解码器：Kyutai的Mimi教它的第一本码本去对齐自监督模型WavLM，旁边再保留七级声学码，每秒12.5帧，1.1千比特。旁白自己的分词器，Qwen3-TTS的那个，也是这样做的，用十六级。",

    # ---------------------------------------------------------------- Audrey
    'Chapter ten. From Audrey to hidden Markov models.':
        '第10章。从Audrey到隐马尔可夫模型。',

    'f"Speech recognition began with digits.':
        "语音识别是从数字开始的。<bookmark mark='a'/>1952年，贝尔实验室的三位工程师造出了Audrey。它把声音分成两个频带，通过数信号穿过零点的次数来跟踪每个频带的频率，再把这个模式和十个数字各自存好的模式相比。对调好的那个说话人，它一百次里对九十七到九十九次；换了别人，就得重新调。<bookmark mark='b'/>我们做了同样的事：用一个Kokoro声音、每个数字一遍，做出十个模板，每个新词就归到最近的模板。<bookmark mark='c'/>同一个声音，稍快地再说一遍这些数字：对{100 * same:.0f}%。另外十一个声音：{100 * other:.0f}%。语音识别的难题从来不是词，而是声音。",

    'f"People say the same word fast or slow,':
        "人们说同一个词可快可慢，有的音拉长、有的不拉长，所以把每个词都压成同一长度很粗糙。<bookmark mark='a'/>1968年基辅的塔拉斯·温秋克，和1978年NEC的迫江博昭与千叶成美，用动态规划把两者对齐：动态时间规整。到每一对帧的最便宜对齐，是从三个邻居之一的最便宜对齐延伸过来的。<bookmark mark='b'/>这是把seven的一次新录音对齐到模板上的路径。<bookmark mark='c'/>时间规整{better}：同一个声音{100 * sd:.0f}%，其他声音{100 * od:.0f}%。用十个声音的模板，两个从没听过的声音能达到{100 * md:.0f}%。更多的例子胜过更聪明的匹配，这个领域会一次又一次学到这一课。",

    'From the mid-1970s, at Carnegie Mellon and at IBM,':
        "从1970年代中期起，在卡内基梅隆大学和IBM，识别变成了统计。<bookmark mark='a'/>每个词是一个隐马尔可夫模型，第7部分的模型：一串状态，每个音一个，语音沿着它们走过去，或停留，或前进。<bookmark mark='b'/>每个状态用一个高斯混合给一帧的频谱打分，整个模型用EM训练，用维特比解码。<bookmark mark='c'/>词则按贝叶斯法则来选：最能解释这段声音的转写，乘以语言模型对它的预期。这套配方规模化之后，支撑听写和电话系统长达三十年。<bookmark mark='d'/>2012年，四个实验室联合报告：作为声音模型，深度网络胜过了高斯混合。接下来的问题是，一个网络能不能学会整件事，而不用告诉它哪一帧是哪个音。",

    # ---------------------------------------------------------------- CTC
    'Chapter eleven. Connectionist temporal classification.':
        '第11章。连接时序分类。',

    'A recognizer hears a hundred frames of sound for a dozen letters,':
        "识别器听到一百帧声音，对应十几个字母，而训练数据只说了说的是什么，没说什么时候说的。旧系统需要每一帧都有标签，从之前的模型得来。<bookmark mark='a'/>2006年，亚历克斯·格雷夫斯、圣地亚哥·费尔南德斯、福斯蒂诺·戈麦斯和于尔根·施密德胡伯找到了绕过去的办法。网络对每一帧，给每个字母一个概率，再加一个额外的符号：空白符。<bookmark mark='b'/>穿过各帧的任何一条路径，先合并重复的符号，再去掉空白符，就变成文本。<bookmark mark='c'/>空白符也是真正的双写字母得以保留的办法：中间没有空白符，three里的两个e就会合成一个。<bookmark mark='d'/>文本的概率，就是所有能变成它的路径之和。",

    'There are exponentially many paths, but the sum is cheap.':
        "路径的数目是指数级的，但求和很便宜。<bookmark mark='a'/>把转写写出来，在字母前、中间和后面都加上空白符：一共2L加1个状态，按顺序排好。<bookmark mark='b'/>在时刻t处于状态s的路径，前一帧要么在s，要么在它前面的那个状态。<bookmark mark='c'/>它还可以跳过一个空白符，从往回两个状态跳过来，除非那样会把两个相同的字母合并。再乘以网络在这一帧给状态s的符号的概率。<bookmark mark='d'/>结束在最后一个字母或最后一个空白符上的路径，加起来就是转写的概率。<bookmark mark='e'/>这正是第7部分隐马尔可夫模型的前向算法，把转写当作状态链；它的对数取负就是损失，梯度来自同一个递推的反向运行。",

    'f"We trained a small recognizer this way:':
        "我们用这种方法训练了一个小识别器：{params / 1000.0:.0f}千个参数，七层卷积，用十个Kokoro声音说的数字串训练，三个种子。<bookmark mark='a'/>这是在训练过程中，它从一个从没听过的声音说的数字串里听到的东西。起初每一帧都是一片模糊。<bookmark mark='b'/>然后空白符占了上风，这是在大多数帧上答对的最便宜的办法。<bookmark mark='c'/>接着{spikes}，夹在空白符之间：到最后，空白符赢下{100 * blank:.0f}%的帧，一个字母平均持续{run_len:.1f}帧，这就是CTC出了名的尖峰式对齐。下面的贪心读法，在每一帧取最可能的符号，再合并、去空白。",

    'f"And here is the lattice itself,':
        "这就是格本身，由训练好的网络算出：转写的各个状态竖着排，各帧横着排。<bookmark mark='a'/>亮度表示每个状态在每一帧上的可能性，由前向和后向两遍合起来得到；白线是唯一的最佳路径。<bookmark mark='b'/>前向算法算出的总和，自然对数为{tot:.2f}，与PyTorch自己的CTC损失一致。<bookmark mark='c'/>三个种子平均：{verdict}；{gap}。<bookmark mark='d'/>2014年，百度的Deep Speech用几千小时的数据训练CTC，抛开了旧的流水线。CTC把每一帧的字母当作彼此独立，所以后来的系统，RNN转录器和基于注意力的识别器，让每个字母依赖于前面的字母。",

    "f'{100 * wer.mean():.1f} percent of the digit words wrong":
        "两个新声音的数字词错了{100 * wer.mean():.1f}%，训练用过的声音错了{100 * seen.mean():.1f}%",


    # ---------------------------------------------------------------- Whisper
    'Chapter twelve. Listening at scale.':
        '第12章。大规模地听。',

    'After Deep Speech, two roads led to the recognizers we use today.':
        "Deep Speech之后，有两条路通向我们今天用的识别器。<bookmark mark='a'/>一条是自监督。Facebook在2020年的wav2vec 2.0，把语音的几段藏起来，不让它自己的Transformer看到，再学着从干扰项里挑出真正被藏起来的那一帧，这是把第24部分的对比损失用在声音上。它先在五万三千小时没有转写的语音上预训练，再只用十分钟有转写的语音微调，在一个标准基准的两半上，词错误率分别是4.8%和8.2%。<bookmark mark='b'/>另一条路是弱监督。2022年12月，OpenAI的Whisper在六十八万小时、配有网上找来的转写的音频上训练，不完美的转写也照收；一个模型就能转写、翻译、识别语言、给词标时间，覆盖将近一百种语言。",

    'f"Whisper is a plain encoder-decoder transformer,':
        "Whisper是一个朴素的编码器-解码器Transformer，和第14部分那个翻译模型同一个形状。<bookmark mark='a'/>它的输入就是第8章那张图：每十毫秒80个对数梅尔频带，永远是三十秒，不够就用静音补齐。<bookmark mark='b'/>编码器读它；解码器用GPT-2的字节级BPE，一次一个词元地写出转写，同时回头关注声音。<bookmark mark='c'/>开头的特殊词元说明要做什么：这里是转写开始，不要时间戳。识别器变成了一个会听的语言模型。<bookmark mark='d'/>我们跑的是最小的英语模型base.en，{int(w['params']) / 1000000.0:.0f}百万个参数，来自Hugging Face缓存。",

    'f"How does it do on our voices?':
        "它在我们的声音上表现如何？<bookmark mark='a'/>在两个留出的Kokoro声音说的{int(w['n_sents'])}句话上，它的词错误率是{100 * ws:.1f}%。<bookmark mark='b'/>在{int(w['n_strings'])}个数字串上是{100 * wd:.1f}%，把它写出的阿拉伯数字也算作词；我们只用数字训练的CTC识别器是{100 * cw:.1f}%：{cmp_}。<bookmark mark='c'/>看看它的错误：在声音留有余地的地方，解码器这个语言模型，就写下它觉得更可能的东西：一个复数，一个写成阿拉伯数字的数，两个连在一起的词。",

    "new voices are much harder than the ones it heard, Audrey's lesson again":
        "新声音比它听过的难得多，又是Audrey的那一课",
    'it does about as well on new voices as on the ones it heard':
        "它在新声音上和在听过的声音上差不多一样好",
    'our tiny specialist does better on its own task':
        "我们的小专家在它自己的任务上做得更好",
    'Whisper does better even on our model\'s own task':
        "即使在我们模型自己的任务上，Whisper也做得更好",
    'the two come out about the same on digits':
        "在数字上两者差不多",

    'Recognizers kept growing and getting faster:':
        "识别器越来越大，也越来越快：2023年的Whisper large-v3，以及一个把解码器从32层砍到4层的加速版。<bookmark mark='a'/>2026年1月，阿里巴巴的Qwen3-ASR建在一个全模态模型之上，覆盖52种语言和方言。<bookmark mark='b'/>它也在为这个系列工作。旁白说的每一句话，都由Qwen3-ASR转写，如果转写和稿子对不上就重说一遍；再由一个强制对齐器给每个词标出时间，动画就是这样知道什么时候该动的。",

    # ---------------------------------------------------------------- TTS
    'Chapter thirteen. Speaking.':
        '第13章。说话。',

    'Speaking is the inverse problem,':
        "说话是反过来的问题，而且比听更早。<bookmark mark='a'/>1939年，贝尔实验室在世界博览会上展示了Voder：一位操作员用琴键和踏板弹出语音。它背后的想法，是把嗓音看成一个声源加一个滤波器：声带嗡嗡振动，喉咙和口腔用共振，也就是共振峰，去塑造这嗡嗡声。<bookmark mark='b'/>1980年，丹尼斯·克拉特的共振峰合成器按规则算出这些共振；史蒂芬·霍金用的那个声音，就是从他的工作里发展出来的。<bookmark mark='c'/>后来合成器开始重用真实录音，机器腔才褪去：在单元选择里，一个人朗读好几个小时，系统再把衔接得最好的片段拼起来。<bookmark mark='d'/>2000年代，统计模型，又是隐马尔可夫模型，改为预测频谱，平滑却发闷。",

    "In 2016 DeepMind's WaveNet threw out the vocoder's rules":
        "2016年，DeepMind的WaveNet抛开了声码器的规则，直接生成波形，一次一个采样点。<bookmark mark='a'/>它是一个以采样点为词元的语言模型：每个点都由之前所有的点预测，每秒一万六千个，<bookmark mark='b'/>每个采样点用对数形状的μ律曲线压到256个等级上，所以词表很小。<bookmark mark='c'/>为了看得足够远，它的卷积依次跳过一、二、四、八个采样点，每一层把视野加倍。听众更喜欢它，胜过当时最好的系统，但它非常慢。<bookmark mark='d'/>谷歌的Tacotron 2把工作分成两步：一个序列到序列的网络把文本变成梅尔频谱，WaveNet再把它变成声音。听众给它打了4.53分，满分5分；真实录音是4.58分。",

    'Then speech synthesis became language modelling,':
        "然后，语音合成变成了语言建模，第9章的编解码器词元就是词。<bookmark mark='a'/>微软在2023年1月推出的VALL-E，接收文本，以及某人三秒钟的声音，写成EnCodec词元。<bookmark mark='b'/>一个Transformer接着这段声音提示往下写，逐帧写出第一本码本；<bookmark mark='c'/>另一个一次性补齐更细的各本码本，编解码器的解码器再生成波形。<bookmark mark='d'/>它在六万小时的语音上训练，只听三秒就能用那个声音说话，这个技巧让声音克隆变得廉价，此后的每个语音模型都得面对它。",

    '"This series has a narrator of its own.':
        "这个系列有自己的旁白。<bookmark mark='a'/>Qwen3-TTS，阿里巴巴2026年1月发布，在十种语言、五百多万小时的语音上训练。它的分词器是一个像Mimi那样的编解码器：每秒12.5帧，十六本码本，每本2048个码，第一本由一个自监督模型教着去携带说了什么，其余十五本携带听起来怎样。<bookmark mark='b'/>它的Transformer写出每一帧的第一本码，一个小模块预测其余十五本，大约十分之一秒后就发出第一个声音。它只需三秒就能克隆一个声音。<bookmark mark='c'/>{own}<bookmark mark='d'/>这份视频由{narration_credit()}朗读。从Voder的琴键到这里，走了八十七年。",

    "f'Here is the {ref_s:.0f}-second clip":
        "这是它学英语声音所用的那段{ref_s:.0f}秒的片段，写成旁白看到的编码：{n_ref}帧，每帧十六个码，每秒{bps:,.0f}比特。{gen}",

    "f' And here is the narrator saying a sentence of this part:":
        "这是旁白说出这一部分里的一句话：{n_gen}帧，每帧十六个码，由它的Transformer写出，再由解码器变成声音。",

    "Its codes can't be shown here,":
        "这里无法展示它的编码，因为制作这份视频的电脑上没有安装Qwen3-TTS。",

    # ---------------------------------------------------------------- Clip
    'Chapter fourteen. Matching pictures and words.':
        '第14章。让图片和文字配对。',

    'Pictures met words in two ways.':
        "图片和文字以两种方式相遇。<bookmark mark='a'/>2014年前后，网络学会了给照片配说明：一个视觉网络喂给一个语言模型，由它写出一句话。<bookmark mark='b'/>2021年，OpenAI的CLIP做了更简单的事。两个编码器，一个读图片，一个读文字，在网上四亿张图片和它们的说明上训练，让配对的两者得到相近的向量。然后它就能给从没训练过的类别分类：把每个类别写成一句说明，挑最接近的那个。在ImageNet上，这样得到76%，一个标签都没用。<bookmark mark='c'/>我们在字母上训练了一对小编码器，说明像“bold serif A”这样。这是一批数据：每张图片和每句说明都打了分，<bookmark mark='d'/>亮的对角线就是正确的配对。",

    'f"Part 24 showed that this kind of loss measures information.':
        "第24部分说明了这类损失在度量信息。这里从打分函数的角度再看一次。<bookmark mark='a'/>这个损失要求每张图片从N句说明里挑出自己的那句。<bookmark mark='b'/>最好的分数，是给定图片时这句说明的可能性比它单独出现时高多少倍，再取对数。<bookmark mark='c'/>代进去，分子分母同除以真正配对那一项。<bookmark mark='d'/>随机说明很多时，每个比值平均为一，剩下的至少是log N减去图片和文字之间的互信息。所以log N减去损失，是这份信息的一个下界，而且永远超不过log N。<bookmark mark='e'/>在我们的模型上，分别用{Bs[0]}、{Bs[1]}和{Bs[-1]}个候选来测，三个种子：估计值从{e16:.2f}奈特涨到{e256:.2f}，被压在log N之下，而说明本身含有{H:.2f}奈特。这个上限属于测量本身：用{Bs[-1]}个候选来测时，用{Bs[0]}和{Bs[-1]}的批训练出来的模型，得分分别是{at_big[0]:.2f}和{at_big[-1]:.2f}。",

    'f"Here is that table while the two encoders learn.':
        "这是两个编码器学习时的那张表。<bookmark mark='a'/>一开始，每个分数都是噪声。每一批数据把配对的向量拉近，把其余的推开，对角线就亮了起来；共享一个字母或一种字体的配对仍有几分亮，因为它们本来就相像。<bookmark mark='b'/>现在来做CLIP出名的那个测试。我们把{nc}句说明里的{nh}句，比如“bold mono Q”这样的每一张图片，完全不放进训练。<bookmark mark='c'/>让它在全部{nc}句说明里挑，这些图片有{100 * un[Bmax].mean():.0f}%找到了完全正确的说明，{because}。",

    'because the caption encoder learned bold, mono and Q separately':
        "因为说明编码器分别学会了bold、mono和Q，能把它们组合起来",
    'far above chance, but putting known words together':
        "远高于随机，但把学过的词组合起来，比看上去要难",

    'f"In 2023 Xiaohua Zhai and colleagues at Google changed one thing.':
        "2023年，谷歌的翟晓华和同事只改了一处。CLIP的损失是对整批数据做softmax：每张图片的分数取决于批里的每一句说明，所以整批数据必须收集到每块芯片上。<bookmark mark='a'/>SigLIP改为对每一对图片和说明问一个是或否的问题，用sigmoid加一个学出来的偏置。没有整批的求和，所以能扩展到极大的批，而他们发现它在小批上也更好。<bookmark mark='b'/>我们在三种批大小下训练了两者，同样的配对总数，各三个种子。在没见过的说明上，{small}，{big}：批大小{Bs[0]}时{100 * m['clip', Bs[0]]:.0f}%对{100 * m['siglip', Bs[0]]:.0f}%，{Bs[-1]}时{100 * m['clip', Bs[-1]]:.0f}%对{100 * m['siglip', Bs[-1]]:.0f}%，CLIP在前。<bookmark mark='c'/>在大规模上，SigLIP的编码器成了许多开源视觉语言模型的眼睛。",

    # ---------------------------------------------------------------- VLM
    'Chapter fifteen. Models that see.':
        '第15章。会看的模型。',

    "CLIP matches pictures with captions, but it can't answer":
        "CLIP能给图片配说明，却回答不了关于一张图片的问题。要做到这一点，得把一个视觉编码器接到语言模型上。<bookmark mark='a'/>DeepMind在2022年的Flamingo，把每张图片压成64个词元，并给一个冻结的语言模型加上新的交叉注意力层。<bookmark mark='b'/>Salesforce的BLIP-2向一个冻结的图像编码器发出32个学出来的查询。<bookmark mark='c'/>2023年4月，LLaVA表明需要的东西少得惊人：一个线性映射，把CLIP的每个小块向量变成语言模型词空间里的一个向量，图片就只是提示开头多出来的一些词元。<bookmark mark='d'/>先在说明文字上训练这个映射，再用GPT-4根据图片说明写出的十五万八千条关于图片的对话样例来微调。此后几乎每个开源视觉语言模型都是这个样子。",

    'f"Early models resized every picture to one small square,':
        "早期的模型把每张图片都缩成一个小正方形，边长224或336像素。拍一只狗没问题，拍一张收据就完了。<bookmark mark='a'/>我们那个读字母的CLIP能说明这种效果：把它二十像素的字母缩小，再放大回去。十像素时，它仍能读对{100 * A.mean(0)[i10]:.0f}%的字母；五像素时，只有{100 * A.mean(0)[i5]:.0f}%。<bookmark mark='b'/>2024年，Qwen2-VL不再缩成正方形。一张图片大致保持自己的大小和形状，切成14像素的小块，每二乘二个小块合成一个词元，于是一个小图标花几十个词元，一张大截图要一千多个。这些数字来自公开的代码。",

    "A picture's tokens are a grid, not a line,":
        "一张图片的词元是一个网格，而不是一条线，位置编码应该体现这一点。<bookmark mark='a'/>Qwen2-VL的答案M-RoPE，给每个词元三个坐标：时间、行和列。文本词元三个坐标都用同一个数，所以对文本来说，它就是第13部分普通的RoPE。<bookmark mark='b'/>一张图片的词元共用一个时间，各取自己的行和列，而图片后面的文本从用过的最大数字之后接着数。<bookmark mark='c'/>旋转的维度分成三份，每份按一个坐标旋转，这样注意力就能分清图片里的邻居和句子里的邻居。<bookmark mark='d'/>视频在时间上多出了帧；Qwen2.5-VL把这根轴和真实的秒数挂钩，Qwen3-VL把三个坐标交错铺到各个频率上。",

    'The connector recipe bolts a vision encoder':
        "连接器的做法，是把一个视觉编码器硬接到一个只学过语言的模型上。<bookmark mark='a'/>更新的做法是从一开始就在混合序列上训练，也就是早期融合。2024年，Meta的Chameleon把图片写成VQ词元，和词放在同一个词表里，也就是第22部分的图像词元。<bookmark mark='b'/>2026年2月，阿里巴巴的Qwen3.5从一开始就在文本和图片词元上一起训练；据它的模型卡，它在文本上和只做文本的前代相当，在图片上胜过专门的视觉语言模型。看，已经不再是一个附加功能了。",

    # ---------------------------------------------------------------- Omni
    'Chapter sixteen. Every sense at once.':
        '第16章。所有感官一起来。',

    'The voice assistants of the 2010s were cascades:':
        "2010年代的语音助手是级联的：<bookmark mark='a'/>一个识别器把你的话变成文字，一个语言模型写出回复，一个合成器再把它读出来。每一级都要等上一级，而文字装不下的东西，语气、笑声、迟疑，一路上都丢了。<bookmark mark='b'/>2024年5月，OpenAI的GPT-4o把这一切放进一个网络，在文本、图片和声音上端到端训练，回应语音最快只要232毫秒，平均320毫秒，和人们轮流说话的速度差不多。",

    'GPT-4o still took turns.':
        "GPT-4o还是一轮一轮地说。真正的对话不是这样：人们会打断、会重叠，会在对方说话时嗯嗯应和。<bookmark mark='a'/>2024年9月，Kyutai的Moshi同时建模两条声音流，用户的和它自己的，每次八十毫秒，所以它一直在听，即使在说话的时候。<bookmark mark='b'/>在自己的语音旁边，它还写下自己正在说的词，比声音稍稍提前，这段内心独白让语音不跑偏。它的延迟：理论上160毫秒，实际上大约200毫秒。",

    "Alibaba's open omni models split the work in two.":
        "阿里巴巴的开源全模态模型把工作一分为二。<bookmark mark='a'/>思考者是一个语言模型，读一串由文本、图片和声音词元组成的序列，旋转位置按时间对齐，写出文本。<bookmark mark='b'/>一个更小的说话者边走边写出语音编码，再由解码器变成声音；在Qwen3-Omni里，是每秒十二帧半，经过一个小的卷积解码器。在Qwen2.5-Omni里，说话者读的是思考者的隐藏状态；在Qwen3-Omni里，它只读词，以及声音和图片的特征，这样工具和安全过滤器就能在文本被说出来之前介入。<bookmark mark='c'/>2025年9月的Qwen3-Omni，把两半都做成了混合专家，并公开了权重；2026年4月的Qwen3.5-Omni，一个上下文里能装下十多个小时的音频。而NVIDIA在2026年1月推出的PersonaPlex，把全双工对话又往前推了一步，可以指定一个声音和一个要扮演的角色。",

    'f"In the end, every sense is a stream of tokens,':
        "说到底，每一种感官都是一串词元，区别在于有多少。<bookmark mark='a'/>按Whisper自己的分词器、在我们的声音上量，语音里的词大约每秒{float(w['tokens_per_second']):.0f}个词元。<bookmark mark='b'/>同样的语音写成Mimi的编码是每秒100个，写成旁白的分词器是{q_hz * q_n:.0f}个，而一帧高清视频就是{int(frame['tokens']):,}个词元。<bookmark mark='c'/>按Mimi的速率，一分钟的对话每条流就有{mimi_min:,.0f}个词元，所以这些模型里很多工程都花在少用词元上：更低的帧率，更少的码本，能用小图时就用小图。",

    # ---------------------------------------------------------------- Outro
    "Let's take stock.":
        "我们来盘点一下。字节对编码靠反复合并最常见的对来切分文本，是一个贪心的压缩器；一元模型给每一种切法一个概率；而每字符比特数是比较它们的公平方式。字节和按熵分块，把模型的力气花在意外所在的地方。图片和声音通过码本变成词元，码本若不重启就会坍缩，或者干脆换成固定的网格；残差分级做出的编解码器，每秒几百比特就能装下语音。采样把太快的部分折回频段里；频谱和梅尔刻度是识别器听到的东西。CTC在一张格上求和，不需要对齐就学会转写；Whisper从网上学习；语音合成变成了在编解码器词元上的语言建模。对比训练把图片和文字放进同一个空间，而当一切都是词元，一个模型就能同时看、听、说。",

    'All of this comes back.':
        "这些都会再出现。语义词元和视觉语言模型所依赖的自监督语音和图像编码器，就是下一部分，第24部分。推理模型用词元思考，在第28部分。机器人和世界模型把动作和视频帧写成词元，在第29部分。词元在模型内部最终意味着什么，是第30部分。而分词器在基准测试里的怪癖，以及只用三秒语音克隆出来的声音，会在最后一部分、关于信任的那一部分再出现。",

    'Here are six problems,':
        "这里有六道题，从数合并次数，到一个批次能证实多少信息。在这里暂停一下，把它们做一做；完整的解答在这一部分的笔记里。",

    'Next time: where encoders like wav2vec 2.0 and DINO come from,':
        "下一次：在没人打标签的时候，wav2vec 2.0和DINO这样的编码器是从哪里来的。同一个输入的两个视角拉到一起，其余的都推开，以及只从数据本身学习的其他办法：不用标签的学习，第24部分。",

    "Jurafsky and Martin's Speech and Language Processing":
        "想深入学习，可以读朱拉夫斯基和马丁的《语音与语言处理》（Speech and Language Processing）：分词、识别和合成都在里面。感谢观看，第24部分见。",
}

PHRASES = {
    # codec (chapter nine)
    'fairly evenly': '相当均匀',
    'unevenly': '不太均匀',
    # tokenizers (chapter four)
    'raw bytes': '原始字节',
    'BPE with 1,024 pieces': '1024个片段的BPE',
    'BPE with 4,096 pieces': '4096个片段的BPE',
    'the unigram model with 1,024 pieces': '1024个片段的一元模型',
    'the unigram model with 4,096 pieces': '4096个片段的一元模型',
    'BPE beats the unigram model at 1,024 pieces': '在1024个片段时，BPE胜过一元模型',
    'BPE beats the unigram model at 4,096 pieces': '在4096个片段时，BPE胜过一元模型',
    'the unigram model beats BPE at 1,024 pieces': '在1024个片段时，一元模型胜过BPE',
    'the unigram model beats BPE at 4,096 pieces': '在4096个片段时，一元模型胜过BPE',
    'BPE and the unigram model overlap at 1,024 pieces': '在1024个片段时，BPE和一元模型的结果互相重叠',
    'BPE and the unigram model overlap at 4,096 pieces': '在4096个片段时，BPE和一元模型的结果互相重叠',
    # codebooks
    'EMA alone does not fix it': '光靠EMA解决不了',
    'EMA helps': 'EMA有帮助',
    'plain VQ': '普通VQ',
    'EMA': 'EMA',
    'EMA with restarts': '带重启的EMA',
    'VQ with EMA': '带EMA的VQ',
    'FSQ': 'FSQ',
    'LFQ': 'LFQ',
    'so does LFQ': 'LFQ也是',
    "LFQ, at its paper's entropy weight, does not": 'LFQ在论文的熵权重下则不然',
    # sound and speech
    'falls': '下降',
    'barely changes': '几乎不变',
    'helps': '有帮助',
    'barely helps': '帮助不大',
    # pictures and words
    'SigLIP is ahead at the smallest batch': '最小的批上SigLIP领先',
    'CLIP is ahead at the smallest batch': '最小的批上CLIP领先',
    'the seeds overlap at the smallest batch': '最小的批上各种子的结果互相重叠',
    'SigLIP is ahead at the largest': '最大的批上SigLIP领先',
    'CLIP is ahead at the largest': '最大的批上CLIP领先',
    'they overlap at the largest': '最大的批上也互相重叠',
    'letters appear as sharp spikes': '字母以尖锐的尖峰出现',
    "new voices are much harder than the ones it heard, Audrey's lesson again": '新声音比它听过的难得多，又是Audrey的那一课',
    'it does about as well on new voices as on the ones it heard': '它在新声音上和在听过的声音上差不多一样好',
    'letters appear': '字母出现了',
}
