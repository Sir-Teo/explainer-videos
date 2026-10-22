"""Chinese narration for ai14: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).

Numbers that follow from published figures (a parameter count from a configuration, 6ND) are written out in Chinese;
numbers from our own training runs stay placeholders, so the Chinese follows the data when it changes.
"""

TITLE = '人工智能，从零搭建 · 第14部分：语言模型的谱系'

CHAPTERS = {
    'Hook': '从一篇翻译论文到开放前沿',
    'Translation': '1. 注意力就是你所需要的一切',
    'Pretrain': '2. 先预训练，再微调',
    'BERT': '3. 掩码语言模型与基准时代',
    'TextToText': '4. 一切都是文本到文本',
    'GPT2': '5. 无监督的多任务学习者',
    'GPT3': '6. 规模，以及在上下文中学习',
    'Instructions': '7. 代码，以及遵循指令',
    'ChatGPT': '8. ChatGPT与闭源时代',
    'OpenWeights': '9. 开放权重',
    'Converge': '10. 架构的趋同',
    'Frontier': '11. 开放前沿，2024到2026',
    'Trends': '12. 算力、成本与数据',
    'OurLineage': '13. 我们自己的谱系：GPT对BERT',
    'Emergence': '14. 在我们自己的模型里，在上下文中学习',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"June 2017. Eight researchers at Google publish a paper':
        "2017年6月。谷歌的八位研究者发表了一篇标题很自信的论文：《Attention Is All You Need》，注意力就是你所需要的一切。<bookmark mark='a'/>他们的模型把英语翻译成德语和法语。较大的那个版本有2.13亿个参数，在8块显卡上训练了三天半。<bookmark mark='b'/>这里是本部分会遇到的每一个模型，按它出现的时间和它的大小排开，纵轴每往上一格就是10倍。<bookmark mark='c'/>到2022年11月，同样的基本模块，做得大得多，开始回答任何人的提问：ChatGPT。<bookmark mark='d'/>而到2026年秋天，你可以下载、自己运行的模型已经有上万亿个参数。月之暗面的Kimi K3有2.8万亿个参数，大约是2017年那个Transformer的{round(ratio, -3):,.0f}倍。",

    'How did a model built to translate sentences become the engine':
        "一个为翻译句子而造的模型，怎么就成了几乎一切的引擎？这就是本部分要讲的故事。<bookmark mark='a'/>它从做翻译的Transformer开始，经过GPT和BERT、T5、GPT-2和GPT-3，到ChatGPT，再到今天的开放权重模型。<bookmark mark='b'/>每一步，我们都会问：谁在什么时候做了什么；这一步改变了什么；它为什么奏效。",

    'f"Along the way we\'ll rebuild the lineage in miniature':
        "一路上，我们会在这台制作视频的电脑上，用本系列读的那三十部小说，把这条谱系缩小重建一遍。<bookmark mark='a'/>一个GPT式的模型，学着预测下一个词；一个BERT式的模型，学着填空；两者大小完全相同，训练用的算力完全相同，比较也力求公平。<bookmark mark='b'/>再加上一族大小递增的GPT式模型，从大约27万到420万个参数，看看从提示里的例子中学习，也就是GPT-3带来的惊喜，在我们这个规模上会不会出现。",

    'This is Part 14 of AI, Built, in its third act':
        "这是《人工智能，从零搭建》的第14部分，属于第三幕：Transformer时代。<bookmark mark='a'/>本部分讲：2017年的Transformer，以及切分它的三种方式；预训练，从ULMFiT和GPT-1到BERT和T5；规模，从GPT-2到GPT-3，以及从提示中学习；一个文本预测器怎样变成了助手；开放权重，它们趋同的设计，以及2026年的前沿；算力、成本和数据的趋势；还有我们自己的实验。",

    # ------------------------------------------------------------------ 1. Translation
    'Chapter one. Attention is all you need.':
        '第1章。注意力就是你所需要的一切。',

    'In 2017 the best translation systems were recurrent networks':
        "2017年，最好的翻译系统是循环网络，也就是第10部分讲的序列到序列模型，再加上注意力。它们一次读一个词：读完每个词之后的状态，由读完前一个词之后的状态算出来。<bookmark mark='a'/>问题就出在这条链上。训练时，一个句子的各步没法并行，最后一个词要碰到第一个词，必须经过中间的每一个状态。<bookmark mark='b'/>Transformer去掉了循环。每个位置直接关注其他每个位置，一次全部完成：整个句子通过一层只需一个并行步骤，任意两个词之间只隔一跳。",

    'Here is the model they built.':
        "这就是他们造的模型。<bookmark mark='a'/>编码器读入英语句子：六个相同的层，每层先是自注意力，每个词看其他每个词，然后是一个小的前馈网络，分别作用在每个位置上。<bookmark mark='b'/>解码器写出德语，一次一个词元，它也有自己的六层。它的自注意力带掩码，所以一个位置只能看到已经写出的词。<bookmark mark='c'/>还有第三个子层，交叉注意力，让输出的每个位置去看编码后的输入。<bookmark mark='d'/>每个子层外面，都有残差连接和层归一化；为了告诉模型每个词在哪里，还把不同频率的正弦波加到输入上。第13部分已经把这台机器拆开看过了。这里我们关心的是它后来变成了什么。",

    'f"The paper gave two configurations.':
        "论文给出了两种配置。<bookmark mark='a'/>基础模型：每个堆栈六层，宽度512，8个注意力头，6500万个参数，训练10万步，大约12个小时。大模型把宽度和头数都翻倍：2.13亿个参数，30万步，三天半。两者都用2014年机器翻译研讨会的标准数据训练：450万对英德句子，3600万句英法句子。<bookmark mark='b'/>英译德，大模型得到28.4的BLEU分，这是衡量与人工译文重合程度的指标，比之前最好的系统，包括集成模型，高出两分多。<bookmark mark='c'/>而且它很便宜。仅仅基础模型就超过了之前的所有系统，训练成本大约只有谷歌自家循环系统的{frac_word}。",

    'Where does a number like that come from?':
        "这样的数字是怎么来的？论文的算法值得一看，因为这个领域至今还是这样计算算力的。<bookmark mark='a'/>训练时间：三天半是302400秒。<bookmark mark='b'/>乘以GPU的数量，8块，再乘以一块GPU能持续的速度：作者假设P100每秒9.5万亿次运算。<bookmark mark='c'/>乘积大约是2.3乘以10的19次方次运算，正是他们表里的数字。<bookmark mark='d'/>在第6章，我们会用第二种方法算同一个量：根据模型的大小，和它读过的词元数。",

    'Why did it win? Three reasons, and each matters more as we go.':
        "它为什么赢了？有三个原因，而且越往后越重要。每个位置同时计算，所以训练能充分利用并行硬件。任意一个词一步就能到达任意另一个词，所以长距离的依赖容易学到。而且计算几乎全是矩阵乘法，这正是显卡擅长的，那是第17部分的主题。<bookmark mark='a'/>编码器-解码器是为翻译而造的。不到十八个月，这个领域就把它切成了三种：只保留编码器，像BERT那样；只保留解码器，像GPT那样；或者两者都保留，像T5那样。<bookmark mark='b'/>哪一种切法赢了，为什么，是本部分的主线。",

    # ------------------------------------------------------------------ 2. Pretrain
    'Chapter two. Pretrain, then fine-tune.':
        '第2章。先预训练，再微调。',

    'In 2017, almost every language task trained its own model':
        "2017年，几乎每个语言任务都要从零开始，用自己的标注数据训练自己的模型。一个句子理解的基准GLUE，收集了八个这样的任务；它们的训练集，从40万个例子到2500个不等。<bookmark mark='a'/>标注很贵。原始文本几乎免费：几十亿词的书和百科全书。<bookmark mark='b'/>计算机视觉已经找到了利用免费数据的办法：先在ImageNet上训练一个网络，再为每个新任务微调它。<bookmark mark='c'/>2018年，语言也这样做了。先用一个不需要标注的目标在原始文本上预训练，也就是第1部分的猜字游戏，再为每个任务微调一个副本。",

    'January 2018: Jeremy Howard and Sebastian Ruder':
        "2018年1月：杰里米·霍华德和塞巴斯蒂安·鲁德的ULMFiT。他们在维基百科上预训练了一个循环语言模型，1.03亿个词，然后在文本分类上微调，小心地一层一层来。它把最好系统的错误率降低了18%到24%，而且只用100个标注例子，就达到了从零开始用100倍数据训练的效果。<bookmark mark='a'/>2018年2月：艾伦人工智能研究所和华盛顿大学的ELMo。两个语言模型，一个从前往后读，一个从后往前读，它们的内部状态变成了随句子而变的词向量。<bookmark mark='b'/>河岸的bank和设定利率的银行bank，得到不同的向量。把它们加进已有的模型，在六个不同的任务上都提高了最好成绩。",

    "June 2018: OpenAI's GPT, by Alec Radford and colleagues.":
        "2018年6月：OpenAI的GPT，作者是亚历克·拉德福德和同事。他们不用循环网络，只用Transformer的解码器。<bookmark mark='a'/>12层，宽度768，12个头，1.17亿个参数，在BooksCorpus上预训练，也就是七千多本未出版的书，根据前面的512个词元预测下一个词元。<bookmark mark='b'/>然后为每个任务微调一个模型，每个输入都写成一个序列：做蕴含判断，就是前提、一个分隔符、假设；做多项选择，就是上下文依次接上每个答案。一个新的线性层读取最后一个位置。<bookmark mark='c'/>它在测试的12个任务中，有9个创下了新的最好成绩。",

    'Written as objectives:':
        "写成目标函数：<bookmark mark='a'/>预训练最大化每个词元在给定前面词元时的对数概率，也就是第1部分的链式法则，用在原始文本上。<bookmark mark='b'/>微调最大化给定输入序列时正确标签的对数概率。<bookmark mark='c'/>GPT在微调时还把第一个目标保留下来作为辅助，<bookmark mark='d'/>权重是二分之一：这让学习更快，结果的泛化也更好。<bookmark mark='e'/>预训练一次，微调多次：这就是2018年的配方。",

    'What remained open was the objective.':
        "还没定下来的是目标函数。GPT从左往右预测，所以每个词的表示只由它前面的词构成。<bookmark mark='a'/>对于问答这样的任务，一个词的意思可能取决于它后面的内容，这看起来是个缺陷。<bookmark mark='b'/>四个月后，谷歌给出了答案：BERT。",

    # ------------------------------------------------------------------ 3. BERT
    'Chapter three. Masked language models, and the benchmark era.':
        '第3章。掩码语言模型，与基准时代。',

    'October 2018: Jacob Devlin, Ming-Wei Chang':
        "2018年10月：谷歌的雅各布·德夫林和同事。BERT只保留Transformer的编码器，所以每个位置都能看到整个输入，两个方向都能看。<bookmark mark='a'/>但一个能看到一切的模型，没法训练它预测下一个词：它直接看一眼就行了。所以BERT改为把词藏起来。随机挑出15%的位置。<bookmark mark='b'/>其中80%换成一个特殊的掩码词元，10%换成一个随机词，10%保持不变。<bookmark mark='c'/>然后训练模型，在每个挑出的位置上恢复原来的词。随机词和不变的词很重要：之后微调模型时，输入里没有掩码词元，所以它不能只在看到掩码的地方才用心。<bookmark mark='d'/>第二个任务，是判断一段话是否真的接在另一段后面。",

    'Put the two objectives side by side.':
        "把两个目标放在一起看。<bookmark mark='a'/>像GPT这样从左往右的模型，让每个位置都成为目标，用它前面的词来预测。<bookmark mark='b'/>掩码模型的损失只对挑出的位置求和，每个都由整个被破坏的句子来预测。<bookmark mark='c'/>平均下来，那是15%的位置，<bookmark mark='d'/>所以同样一段文本，从左往右的模型能学的目标大约是它的6.5倍。<bookmark mark='e'/>BERT的作者测量过这个代价：他们的掩码模型按步数来看学得稍慢一点，但几乎马上就在任务上超过了从左往右的模型。我们会在第13章亲自检验这个说法。",

    'f"BERT came in two sizes.':
        "BERT有两种大小。Base：12层，1.1亿个参数，和GPT一样大，这样两者才能比较。Large：24层，3.4亿个参数。两者都用书和英文维基百科训练，33亿个词，训练一百万步。<bookmark mark='a'/>在GLUE排行榜上，BERT-Large得到80.5分，GPT是72.8分；它在问答上也创了新纪录。<bookmark mark='b'/>更好的是，作者检查了提升从哪里来。他们用第二种方式预训练同一个Base模型：像GPT一样从左往右，其他一切都相同。<bookmark mark='c'/>掩码在全部五个任务上都赢了：在情感分析上只赢一点点，在问答上赢了大约10分，而在问答里，看到一个词后面的词最重要。",

    'BERT started a race on the benchmarks.':
        "BERT开启了一场在基准上的竞赛。<bookmark mark='a'/>GLUE把九个任务合成一个分数；到2019年7月，最好的系统已经超过了对人类水平的估计。<bookmark mark='b'/>于是人们建了一个更难的基准SuperGLUE，人类得分89.8；BERT只有69分。几个月之内，它也几乎被攻克了。<bookmark mark='c'/>Facebook的RoBERTa表明，BERT只是训练得不够：去掉第二个任务，用更多数据训练更久，它就能比得上之后发表的所有模型。<bookmark mark='d'/>ELECTRA让一个小网络替换词，训练主网络去找出被替换的词，于是它从每个位置学习，而不是只从15%的位置学习。<bookmark mark='e'/>编码器统治了语言理解两年，而且从未离开：搜索和检索背后的嵌入模型，大多是编码器。",

    # ------------------------------------------------------------------ 4. T5
    'Chapter four. Everything is text to text.':
        '第4章。一切都是文本到文本。',

    'In October 2019, Colin Raffel and colleagues at Google asked a plain question.':
        "2019年10月，谷歌的科林·拉费尔和同事问了一个朴素的问题。有这么多目标函数和架构可选，到底哪些最好用？为了公平比较，他们先把每个任务都变成同一个形状。<bookmark mark='a'/>文本进，文本出。翻译：先写translate English to German，再写句子，模型就写出德语。<bookmark mark='b'/>语法判断：模型写出acceptable或者not acceptable。连相似度分数也写成文本：3.8。<bookmark mark='c'/>还有摘要。一个模型，一个损失，一种解码方式，适用于每个任务。他们叫它T5，文本到文本迁移Transformer，并在C4上训练它，那是一个清洗过的网页抓取数据集，大约750GB。",

    "Their pretraining objective, the one that won their comparison":
        "他们的预训练目标，也就是在比较中胜出的那个，是BERT掩码的近亲，叫作片段破坏。<bookmark mark='a'/>挑出15%的词元，组成平均长度为3的片段。<bookmark mark='b'/>在输入里，每个片段换成一个哨兵词元。<bookmark mark='c'/>目标就是缺失的那些片段，每个跟在它的哨兵后面。编码器双向读取被破坏的文本；解码器写出被拿走的部分。",

    'f"Then came the comparison, with every model given the same budget of compute.':
        "接下来是比较，每个模型都给同样的算力预算。<bookmark mark='a'/>这里是各种架构和目标，每个都先预训练，再微调，在三个基准上评分：GLUE、问答和SuperGLUE。<bookmark mark='b'/>用去噪训练的编码器-解码器排第一，GLUE得83.3分。<bookmark mark='c'/>只有解码器、训练来预测下一个词元的语言模型，也就是GPT的配方，排在最后：73.8分，落后大约10分。在为理解而微调的任务上，双向看又一次赢了。",

    'The largest T5, eleven billion parameters, came within a point':
        "最大的T5有110亿个参数，在SuperGLUE上离人类分数不到一分。然而，接管一切的却是只有解码器的设计。为什么？<bookmark mark='a'/>2022年，托马斯·王和同事在BigScience合作中做的一项研究，给出了最清楚的答案。他们用每种架构和目标，在1700亿个词元上训练了50亿参数的模型。<bookmark mark='b'/>如果在许多任务上微调之后再评判，能双向看、用掩码目标的模型最好，正如T5发现的那样。<bookmark mark='c'/>但如果完全不微调，只是对预训练模型给出提示，那么训练来预测下一个词元的因果解码器最好。<bookmark mark='d'/>而这个领域即将不再为每个任务微调一个单独的模型，而是开始用语言去问同一个模型。这个转变从GPT-2开始。",

    # ------------------------------------------------------------------ 5. GPT-2
    'Chapter five. Language models are unsupervised multitask learners.':
        '第5章。语言模型是无监督的多任务学习者。',

    'February 2019. Alec Radford, Jeffrey Wu, Rewon Child':
        "2019年2月。OpenAI的亚历克·拉德福德、杰弗里·吴、雷文·蔡尔德、大卫·栾、达里奥·阿莫代和伊利亚·苏茨克维。他们押的赌注是：一个足够大的语言模型，在足够多样的文本上训练，不用告诉它，也能学会任务，因为网上到处都是人们在完成任务的文字。<bookmark mark='a'/>为了得到质量还不错的多样文本，他们取了Reddit上每一个至少得到3个karma的外链，大约4500万个链接。清洗和去重之后：800万篇文档，40GB的文本。<bookmark mark='b'/>模型就是放大了的GPT-1，把层归一化挪到了每个模块的输入处，上下文为1024个词元。四种大小，最大的48层深、1600宽：15亿个参数。",

    'f"The idea is that a task is just text with a pattern':
        "想法是，一个任务只是带有某种模式的文本，一个足够好的预测器会把模式延续下去。<bookmark mark='a'/>要总结一篇文章，就在后面加上TL;DR，网上的人就是这么写的，然后让模型接着写。<bookmark mark='b'/>要翻译，就先给几行“英语句子等于法语句子”的形式，再给一个英语句子和一个等号。<bookmark mark='c'/>要回答关于一段文字的问题，就写出这段文字、目前为止的对话，再写上A和冒号。<bookmark mark='d'/>什么都不用微调；任务就在提示里。在一个阅读理解测试上，这样得到了55的F1分，与四个系统中的三个持平，而那些系统是用十多万个人工答案训练的。",

    'f"With no task-specific training at all, the largest model set records':
        "完全不针对任务训练，最大的模型就在八个语言建模基准中的七个上创了纪录。<bookmark mark='a'/>最清楚的是LAMBADA：一段话的最后一个词，只有看完整段话才能猜出来。准确率随着规模上升：46%、55%、60%、63%，<bookmark mark='b'/>最后一个超过了之前专门为这个测试打造的模型的最好成绩59%。<bookmark mark='c'/>在维基百科上逐字符预测，它达到了每字节0.93比特，这个数和我们记分牌上的数是一家。它的翻译还很差。但几乎所有东西都随规模稳步提升，这个趋势才是真正的结果。",

    'OpenAI did not release the largest model at first.':
        "OpenAI起初没有发布最大的模型。理由是可能被滥用，比如大规模地编写假新闻。它在2月发布了最小的版本，<bookmark mark='a'/>5月和8月发布了更大的版本，2019年11月发布了完整的15亿参数模型，<bookmark mark='b'/>还附带一份模型卡，说明它的用途、它会在哪里失败，以及训练文本中的偏见。它引发的争论，关于什么时候该发布模型权重，至今没有停止；第31部分会再谈。<bookmark mark='c'/>这篇论文留下的教训更简单：一个只被训练来预测文本的模型，可以被指向许多任务。显而易见的下一步，就是把它做得大得多。",

    # ------------------------------------------------------------------ 6. GPT-3
    'Chapter six. Scale, and learning in context.':
        '第6章。规模，以及在上下文中学习。',

    'January 2020. Jared Kaplan, Sam McCandlish and colleagues':
        "2020年1月。OpenAI的贾里德·卡普兰、萨姆·麦坎德利什和同事，测量了语言模型的损失怎样随着规模下降。<bookmark mark='a'/>在超过七个数量级的范围里，测试损失随参数数量呈幂律，指数很小，大约0.076；数据和算力也有类似的规律。<bookmark mark='b'/>它传递的信息是：更大的模型能从每个词元中得到更多；预算固定时，模型应该比数据长得更快。第12部分推导了这些定律，以及两年后的修正。在2020年，它们是造一个庞然大物的理由。",

    'f"May 2020. Tom Brown and thirty colleagues at OpenAI: GPT-3.':
        "2020年5月。OpenAI的汤姆·布朗和三十位同事：GPT-3。八种大小，从1.25亿到1750亿个参数，全都用3000亿个词元训练。最大的有96层，宽度12288，96个头，上下文2048个词元。1750亿个参数是怎么来的？<bookmark mark='a'/>每层有四个注意力矩阵，分别用于查询、键、值和输出，每个都是d乘d。<bookmark mark='b'/>前馈网络有两个d乘4d的矩阵：8个d的平方。<bookmark mark='c'/>所以一层有12个d的平方，嵌入再加上词表大小和位置数乘以d。<bookmark mark='d'/>对GPT-3来说，层里大约是1739亿，嵌入里是6.4亿，<bookmark mark='e'/>合计1746亿，与论文附录里的数字完全一致。训练数据偏重质量：过滤后的网页占了大部分，但更小、更干净的来源被看了两三遍。",

    'f"Now the compute, counted a second way.':
        "现在用第二种方法来数算力。<bookmark mark='a'/>在一个词元上训练，每个参数大约要6次运算：前向传播2次，一次乘法一次加法；反向传播大约4次，因为既要算权重的梯度，也要算传给下一层的梯度。所以C约等于6ND。<bookmark mark='b'/>6，乘以1746亿个参数，乘以3000亿个词元，<bookmark mark='c'/>等于3.14乘以10的23次方次运算，正是论文自己给出的数字。<bookmark mark='d'/>用论文的单位，是3637个petaflop/s-天：一台每秒运算一千万亿次的计算机，要算大约10年。这大约是第1章那个Transformer所用算力的14000倍。",

    'But GPT-3 is remembered for something else':
        "但GPT-3让人记住的是另一件事，也就是它标题里承诺的：语言模型是少样本学习者。<bookmark mark='a'/>上下文学习：把任务的描述，也许再加几个例子，放进提示里，让模型接着写。不做任何梯度更新；没有一个权重改变。<bookmark mark='b'/>这是论文自己的示例：把英语翻译成法语；sea otter，loutre de mer；peppermint，menthe poivrée；然后是cheese，和一个箭头。<bookmark mark='c'/>只有描述，叫作零样本；有一个例子，叫单样本；有上下文能装下的那么多例子，通常十到一百个，叫少样本。",

    'f"And it worked. <bookmark mark=\'a\'/> On LAMBADA':
        "而且它奏效了。<bookmark mark='a'/>在LAMBADA上，GPT-3零样本达到76.2%，少样本达到86.4%，之前的最好成绩是68%。<bookmark mark='b'/>不查任何文档、凭记忆回答常识问答题：零样本64.3%，单样本68%，少样本71.2%。<bookmark mark='c'/>而在八种大小之间，零样本和少样本的差距越来越大：更大的模型能更好地利用上下文里的东西。没有人专门为此训练过。它是随着规模出现的。在第14章，我们会在自己的小模型里寻找它。",

    # ------------------------------------------------------------------ 7. Instructions
    'Chapter seven. Code, and following instructions.':
        '第7章。代码，以及遵循指令。',

    'f"July 2021. Mark Chen and colleagues at OpenAI fine-tuned GPT models on code':
        "2021年7月。OpenAI的马克·陈和同事用代码微调GPT模型：159GB的Python代码，来自5400万个公开的GitHub仓库。结果就是Codex，它驱动了第一版GitHub Copilot。<bookmark mark='a'/>为了衡量它，他们编写了HumanEval：164道编程题，每道是一个函数签名加一段描述，用隐藏的单元测试来检查。程序只有通过测试才算对。<bookmark mark='b'/>GPT-3一道也没做出来。GPT-J，一个60亿参数的开放模型，做出了11.4%。<bookmark mark='c'/>120亿参数的Codex，第一次尝试就做出了28.8%，<bookmark mark='d'/>如果允许它写一百个程序、由测试挑出任何一个能通过的，就是70.2%。生成许多答案再加以检验，这个想法会在第28部分作为一种思考方式再次出现。",

    'Meanwhile, two groups asked whether a model could learn to follow instructions':
        "与此同时，两个团队在问：能不能让模型学会遵循一般的指令？<bookmark mark='a'/>2021年9月，谷歌的杰森·魏和同事，拿一个1370亿参数的语言模型，在六十多个现有数据集上微调，每个数据集都改写成简单英语的指令。<bookmark mark='b'/>为了公平测试，他们按类型给任务分组，每次留出一整类：在推理上测试的模型，从没在任何推理任务上调过。<bookmark mark='c'/>他们的模型FLAN，在25个数据集中的20个上超过了零样本的GPT-3。<bookmark mark='d'/>一个月后，维克多·桑和一个庞大的BigScience团队用T5做了同样的事。他们的T0有110亿个参数，在11个留出的数据集中的9个上追平或超过GPT-3，而模型小了16倍。<bookmark mark='e'/>指令微调教会的是“被提问”的形式，而这种形式能迁移到模型从没见过的任务上。",

    "Instruction tuning used existing datasets. OpenAI's InstructGPT":
        "指令微调用的是现有数据集。OpenAI在2022年3月发表的InstructGPT，用的是人。<bookmark mark='a'/>标注员为大约13000个提示写了好答案，GPT-3被微调去模仿它们。<bookmark mark='b'/>他们给模型对33000个提示的回答排序，一个奖励模型学习他们的偏好。<bookmark mark='c'/>然后，强化学习在另外31000个提示上，把模型推向奖励模型喜欢的回答。<bookmark mark='d'/>人们更喜欢13亿参数的InstructGPT的回答，胜过1750亿参数的GPT-3。这些阶段的每一个，都会在第27部分用我们自己的模型搭建出来。",

    # ------------------------------------------------------------------ 8. ChatGPT
    'Chapter eight. ChatGPT, and the closed era.':
        '第8章。ChatGPT，与闭源时代。',

    "On the thirtieth of November 2022, OpenAI put a model":
        "2022年11月30日，OpenAI把一个用InstructGPT的配方训练、为对话调过的模型，放到一个免费的聊天窗口后面，取名ChatGPT。<bookmark mark='a'/>对研究者来说，里面没有什么新东西：一个GPT-3.5模型，监督微调，一个奖励模型，PPO。新的是，任何人都能试一试。<bookmark mark='b'/>据一项估计，两个月后它就有了一亿月活跃用户，比之前任何一款消费应用都快。<bookmark mark='c'/>它把语言模型从一个研究课题变成了一个产业，也改变了这个领域优化的目标：不再是微调后的基准分数，而是人们直接和一个模型说话时，它有多有用。",

    'f"On the fourteenth of March 2023 came GPT-4.':
        "2023年3月14日，GPT-4来了。它除了文字，也接受图像。<bookmark mark='a'/>在模拟的律师资格考试中，它的成绩大约在考生的前10%，而GPT-3.5大约在后10%。<bookmark mark='b'/>在MMLU，一个涵盖57个学科的选择题测试上，它得到86.4%，GPT-3.5是70%。<bookmark mark='c'/>报告还提出了一个关于方法的说法：OpenAI用小规模的训练运行拟合规模定律，所用算力最多少一万倍，在大规模训练完成之前，就预测出了GPT-4的最终损失。规模，已经变成了工程。",

    'And the report left something out, on purpose.':
        "报告也有意地略去了一些东西。用它自己的话说：<bookmark mark='a'/>考虑到竞争格局，以及像GPT-4这样的大规模模型的安全影响，本报告不包含关于架构的更多细节，包括模型大小、硬件、训练算力、数据集构建、训练方法，或类似内容。<bookmark mark='b'/>没有大小，没有数据，没有算力。外部的估计来自Epoch AI：算力大约是2乘以10的25次方次运算，最后一次训练的硬件和能耗大约四千万美元。<bookmark mark='c'/>它确实发布的，是一份系统卡：模型的风险，附有例子；五十多位外部专家的测试；以及发布前采取的缓解措施。此后每一次前沿发布，系统卡都成了标配。",

    'For the next two years the frontier was closed.':
        "接下来的两年里，前沿是闭源的。<bookmark mark='a'/>Anthropic在GPT-4的同一周发布了Claude。<bookmark mark='b'/>谷歌的Gemini在12月跟进，从一开始就设计为接受图像、音频和视频。<bookmark mark='c'/>而在2024年9月，OpenAI的o1表明，一个用强化学习训练、在回答之前先长时间思考的模型，在数学和代码上能好得多：这就是第28部分的推理模型。<bookmark mark='d'/>它们的权重、数据和大小都没有公开。如果我们想逐年读到真实的配置，就得去看那些公开了权重的模型。这个故事从2023年2月开始。",

    # ------------------------------------------------------------------ 9. Open weights
    'Chapter nine. Open weights.':
        '第9章。开放权重。',

    'February 2023. Hugo Touvron and colleagues at Meta released LLaMA':
        "2023年2月。Meta的雨果·图夫龙和同事发布了LLaMA：四个模型，从70亿到650亿个参数，只用公开可得的数据训练，1万亿到1.4万亿个词元。<bookmark mark='a'/>最引人注目的结果是：LLaMA-13B在大多数基准上超过了1750亿参数的GPT-3，而它小了十三倍多。<bookmark mark='b'/>权重提供给了研究者，几周之内，一整个开放生态就建在了它们之上：斯坦福的Alpaca、Vicuna，还有更多，都是在单台机器上微调出来的。",

    'f"How could a 13-billion-parameter model beat GPT-3?':
        "一个130亿参数的模型，怎么能打败GPT-3？靠的是每个参数读更多的文本。<bookmark mark='a'/>GPT-3每个参数大约只看了1.7个词元。<bookmark mark='b'/>2022年，DeepMind的Chinchilla论文表明，预算固定时，最好的模型每个参数大约要看20个词元：GPT-3相对于它的数据实在太大了。<bookmark mark='c'/>LLaMA走得更远。它的70亿参数模型，每个参数大约看了150个词元。<bookmark mark='d'/>这比计算最优的训练量还多：用同样的预算，本可以训练出一个更好的模型。但更小的模型运行起来更便宜，它服务的每一个词元都便宜；而一旦有上百万人在用一个模型，运行它的花费就远远超过训练它的花费。第12部分推导了这个取舍。",

    'Then came a wave.':
        "接着来了一波浪潮。<bookmark mark='a'/>2023年7月，Llama 2：2万亿个词元，多了40%，上下文翻倍，有用RLHF调过的聊天版本，许可证允许商用。<bookmark mark='b'/>9月，巴黎一家年轻的公司推出Mistral 7B，采用Apache许可证。它打败了Llama 2的130亿参数模型，用的是分组查询注意力和滑动窗口，下一章会讲这两样。<bookmark mark='c'/>12月，Mixtral：每一层有八个前馈专家，一个路由器为每个词元挑两个，所以模型有470亿个参数，但每个词元只用130亿。它追平或超过了Llama 2 70B和GPT-3.5。混合专家是第16部分的内容。<bookmark mark='d'/>2024年7月，Meta的Llama 3.1：4050亿个参数，15.6万亿个词元，3.8乘以10的25次方次运算，最多用了一万六千块GPU。<bookmark mark='e'/>它的报告甚至统计了故障：54天里中断了466次。前沿规模的训练，被公开地记录了下来。",

    'And from China came open models that would soon lead.':
        "而来自中国的开放模型，很快就走到了前面。<bookmark mark='a'/>阿里巴巴的通义千问Qwen系列始于2023年；到2024年底，Qwen2.5已经用18万亿个词元训练，大小从很小到很大都有。<bookmark mark='b'/>2024年5月，深度求索的DeepSeek-V2有2360亿个参数，但每个词元只用210亿，还用了一种新的注意力，多头潜在注意力，把为过去的词元保留的内存减少了93%。<bookmark mark='c'/>到2025年，最强的开放模型来自中国的实验室：DeepSeek、Qwen、月之暗面的Kimi和智谱的GLM。<bookmark mark='d'/>开放权重意味着开放配置。下一章，我们把它们并排来读。",
    # ------------------------------------------------------------------ 10. Converge
    'Chapter ten. The architecture converges.':
        '第10章。架构的趋同。',

    'f"Open weights mean open configurations, so we can watch the designs change':
        "开放权重意味着开放配置，所以我们能看着设计逐年变化。这里是一张卡片，以及它怎样变化。<bookmark mark='a'/>2017年的Transformer。<bookmark mark='b'/>GPT-2，2019年：48层。<bookmark mark='c'/>GPT-3，2020年：96层，一万两千多宽。<bookmark mark='d'/>LLaMA，2023年：更小了，但用1.4万亿个词元训练。<bookmark mark='e'/>Llama 3.1，2024年：126层，16384宽，上下文12.8万个词元。<bookmark mark='f'/>DeepSeek-V3：层数更少，但有6710亿个参数，每个词元只用其中的370亿。<bookmark mark='g'/>Qwen3，2025年：36万亿个词元。<bookmark mark='h'/>还有Kimi K3，2026年：2.8万亿个参数，上下文一百万个词元，是GPT-1的2048倍。",

    'Now read the recipes side by side, across five design choices.':
        "现在把各家的配方并排来读，看五个设计选择。<bookmark mark='a'/>2017年的Transformer：在每个子层之后做层归一化，ReLU，正弦波位置编码，普通的多头注意力，到处都有偏置。<bookmark mark='b'/>GPT-2和GPT-3把归一化挪到了每个子层之前；T5去掉了它的均值和偏置。<bookmark mark='c'/>2022年的PaLM：SwiGLU，旋转位置编码，所有头共用一组键和值，没有偏置。<bookmark mark='d'/>LLaMA把这些拼在了一起，而从Llama 2最大的模型开始，几乎每个开放模型看起来都一样：前置归一化的RMSNorm，SwiGLU，旋转位置编码，分组查询注意力，没有偏置。<bookmark mark='e'/>后来DeepSeek-V3换掉了注意力，Qwen3在注意力里面加了归一化，趋同开始松动：那是下一章的内容。先看看每个选择为什么胜出。",

    'Normalization first.':
        "先说归一化。<bookmark mark='a'/>2017年的Transformer，在把每个子层的输出加回主干之后才做归一化。<bookmark mark='b'/>前置归一化只对分支的输入做归一化，再把分支的输出原封不动地加回去。<bookmark mark='c'/>把它展开，顶层的主干就等于第l层的主干，加上它上面每一层的贡献之和。<bookmark mark='d'/>所以它的导数里含有单位矩阵：无论堆得多深，梯度都能直接到达每一层。2020年，熊瑞斌和同事证明，前置归一化的Transformer不需要后置归一化那样漫长的预热就能训练。<bookmark mark='e'/>而张彪和里科·森里希提出的RMSNorm，去掉均值和偏置，只按均方根重新缩放：效果一样好，还更便宜。",

    'The feed-forward network.':
        "再说前馈网络。<bookmark mark='a'/>原始的版本是两个矩阵，中间夹一个ReLU。<bookmark mark='b'/>2020年诺姆·沙泽尔提出的SwiGLU，加了第三个矩阵作为门控：一个分支经过平滑的Swish函数，逐个元素地决定另一个分支能通过多少。<bookmark mark='c'/>三个矩阵代替两个，为了保持参数量不变，隐藏层宽度缩小到4d的三分之二。<bookmark mark='d'/>对LLaMA-65B来说，8192的三分之八是21845，向上取整到22016：正好是它公布的宽度。<bookmark mark='e'/>门控为什么有用？在沙泽尔的实验里它降低了损失，而他论文里自己给的答案很有名。",

    'f"Positions and attention.':
        "再说位置和注意力。旋转位置编码之所以胜出，是因为旋转过的查询和键得到的分数只取决于它们的距离，第13部分证明过这一点，而且它能延伸到更长的上下文。<bookmark mark='g'/>分组查询注意力之所以胜出，是因为内存。<bookmark mark='a'/>生成文本时，模型要在每一层保留每个过去词元的键和值：这就是KV缓存。每个词元占用的是：2，乘以层数，乘以键值头的数量，乘以头的大小，再乘以2个字节。<bookmark mark='b'/>GPT-3每个词元大约要4.7兆字节。Llama 3.1如果128个头都保留各自的键和值，就需要8.3兆字节。<bookmark mark='c'/>用分组查询注意力，128个查询头只共用8个键值头：0.52兆字节，少了16倍。<bookmark mark='d'/>DeepSeek的潜在注意力压缩得更多，大约70千字节。<bookmark mark='e'/>在12.8万个词元的上下文里，一次对话就是1.1太字节和68吉字节的差别。内存是第15部分的主题。",

    # ------------------------------------------------------------------ 11. Frontier
    'Chapter eleven. The open frontier, 2024 to 2026.':
        '第11章。开放前沿，2024到2026。',

    'f"December 2024: DeepSeek-V3.':
        "2024年12月：DeepSeek-V3。6710亿个参数，每个词元用370亿。<bookmark mark='a'/>一个由256个小专家外加1个共享专家组成的混合专家，每个词元选8个；潜在注意力；一种不需要额外损失就能让专家保持均衡的办法；训练时一次预测两个词元；而且第一次在这样的规模上用8位浮点数训练。14.8万亿个词元。<bookmark mark='b'/>它的报告写明了成本：278.8万个GPU小时，按每小时2美元算，大约560万美元，这只是最后一次训练，不包括之前的研究。<bookmark mark='c'/>一个月后是DeepSeek-R1，它从V3出发，用强化学习在答案可以核对的问题上训练。它的纯强化学习版本，在训练过程中，AIME 2024数学竞赛的成绩从15.6%升到77.9%。开放权重，MIT许可证；第28部分会讲它是怎么做到的。",

    'Through 2025 the open frontier filled in.':
        "2025年，开放前沿被逐渐填满。<bookmark mark='a'/>4月的Qwen3：稠密模型和混合专家模型，从6亿到2350亿个参数，36万亿个词元，119种语言，思考模式和非思考模式合在一个模型里。<bookmark mark='b'/>7月，月之暗面的Kimi K2：一万亿个参数，激活320亿，用一种新的优化器MuonClip在15.5万亿个词元上训练，损失曲线上一次尖峰都没有。<bookmark mark='c'/>同月还有智谱的GLM-4.5。<bookmark mark='d'/>8月，OpenAI自GPT-2以来第一次开放权重：gpt-oss，1170亿个参数，激活51亿，权重用4位格式存储，一块GPU就放得下，采用Apache许可证。",

    'f"Put the models of this part on one chart':
        "把本部分的模型放到一张图上：横轴是总参数，纵轴是每个词元实际用到的参数。<bookmark mark='a'/>稠密模型落在对角线上：GPT-3、PaLM、LLaMA、Llama 3.1对每个词元都用上每一个参数。<bookmark mark='b'/>开放前沿移到了对角线下方。混合专家让每个词元只经过几百个小网络中的几个，所以容量增长了，每个词元的成本却没有。<bookmark mark='c'/>Kimi K3在它的2.8万亿个参数里只用1040亿：{100 * share['kimik3']:.1f}%。前沿是稀疏的，第16部分讲它怎样运作。",

    'And the attention began to change.':
        "注意力也开始变了。它的成本随上下文长度增长，而前沿模型现在要读一百万个词元。<bookmark mark='a'/>混合架构把大部分注意力层，换成内存大小固定的层：2024年AI21的Jamba；2025年的MiniMax-01和英伟达的Nemotron-H；然后是Qwen3-Next和月之暗面的Kimi Linear，每三个这样的层配一个注意力层。<bookmark mark='b'/>到2026年，旗舰模型都是这样造的，或者用稀疏注意力。2月的Qwen3.5：三比一的混合架构。同月的GLM-5：7440亿个参数，用DeepSeek的稀疏注意力。<bookmark mark='c'/>4月的DeepSeek-V4：1.6万亿个参数，压缩稀疏注意力，一百万词元的上下文。还有7月的Kimi K3：2.8万亿个参数，69层Kimi Delta注意力，24层潜在注意力。<bookmark mark='d'/>第15和第16部分会把它们拆开来看。2023年的趋同是真的，但那只是一次停顿：当上下文变长、模型变稀疏，设计又开始分化了。",

    'f"How far behind the closed frontier are the open models?':
        "开放模型落后闭源前沿多远？有一个独立的指数，来自Artificial Analysis，用十项评测给模型打分。<bookmark mark='a'/>这是最好的闭源模型的分数随时间的变化，<bookmark mark='b'/>这是最好的开放模型的。<bookmark mark='c'/>对每一个新的开放模型纪录，问一问：闭源模型最早什么时候达到同样的分数。所有这些落后时间的中位数是{med_all:.1f}个月。<bookmark mark='d'/>{verdict}最新的开放模型纪录{last['name']}，落后了{last['months']:.1f}个月。",

    "f'Since 2025 the median lag has been {med_recent:.1f} months, shorter":
        "2025年以来，落后时间的中位数是{med_recent:.1f}个月，比以前短：开放模型一直在追赶。",

    "f'Since 2025 the median lag has been {med_recent:.1f} months, about the same":
        "2025年以来，落后时间的中位数是{med_recent:.1f}个月，和以前差不多：开放模型跟得很紧，但还没有缩小差距。",

    # ------------------------------------------------------------------ 12. Trends
    'Chapter twelve. Compute, cost, and data.':
        '第12章。算力、成本与数据。',

    'f"Line up the training compute of the models in this part':
        "把本部分各个模型的训练算力排成一列，纵轴每往上一格就是一百倍。<bookmark mark='a'/>2017年的Transformer：2乘以10的19次方次运算。GPT-1、BERT、GPT-2、T5。<bookmark mark='b'/>GPT-3：3乘以10的23次方。PaLM。<bookmark mark='c'/>GPT-4，按Epoch AI的估计，大约2乘以10的25次方；Llama 3.1，按Meta的报告，3.8乘以10的25次方；还有2025年xAI的Grok 3，大约3.5乘以10的26次方，同样是外部估计。<bookmark mark='d'/>在7.7年里，增长了大约1500万倍。",

    'f"How fast is that, as a rate?':
        "换成增长率，这有多快？Epoch AI维护着一个重要模型的数据库。这里是它标为前沿的语言模型，也就是出现时算力接近最高的那些，从2017年开始。<bookmark mark='a'/>用一条直线拟合算力的对数和日期的关系。<bookmark mark='b'/>斜率b是每年{f['slope']:.3f}个数量级。<bookmark mark='c'/>所以算力每年增长10的b次方倍：大约{f['per_year']:.1f}倍。<bookmark mark='d'/>每{f['doubling_months']:.1f}个月翻一番。Epoch自己的分析认为，前沿模型每年增长4到5倍。{tail}",

    'Our fit agrees with theirs.':
        '我们的拟合和他们的一致。',

    "f'Our fit, {f['per_year']:.1f}, differs from theirs":
        "我们的拟合是{f['per_year']:.1f}倍，和他们的不同，因为它覆盖的模型范围不一样。",

    'Cost grew more slowly than compute, because each operation got cheaper':
        "成本增长得比算力慢，因为每次运算变便宜了，但它还是在增长。<bookmark mark='a'/>Epoch AI估计，GPT-4最后一次训练的硬件和能耗大约花了四千万美元，Gemini Ultra大约三千万美元。<bookmark mark='b'/>在前沿模型中，2016年以来成本每年增长大约2.4倍；照这个趋势，最大的训练到2027年会超过十亿美元。<bookmark mark='c'/>与之相比，DeepSeek报告V3的最后一次训练大约花了560万美元：这是稀疏模型、精心的工程和便宜的8位运算换来的。和所有这类数字一样，它没有算上之前的研究和失败的训练。",

    'f"Finally the data: how many tokens each model read per parameter.':
        "最后是数据：每个模型平均每个参数读了多少个词元。<bookmark mark='a'/>2020和2021年，GPT-3和Gopher每个参数读的词元不到两个。<bookmark mark='b'/>2022年的Chinchilla表明，大约20个是计算最优的。<bookmark mark='c'/>从那以后，开放模型远远超过了这个数：LLaMA的70亿参数模型是150个，DeepSeek-V3按激活参数算是400个，而Qwen3最小的模型，6亿个参数，读了大约36万亿个词元：每个参数60000个。<bookmark mark='d'/>小模型是故意被过度训练的，因为它们运行得最频繁。而好的文本是有限的：词元从哪里来，是第18部分的内容。",

    # ------------------------------------------------------------------ 13. OurLineage
    'Chapter thirteen. Our own lineage: GPT against BERT.':
        '第13章。我们自己的谱系：GPT对BERT。',

    'f"Now our own version of the 2018 question.':
        "现在来做我们自己版本的2018年之问。两个形状完全相同的模型：{sh['layers']}层，宽度{sh['d']}，{sh['heads']}个头，{p['total'] / 1000000.0:.2f}百万个参数，用第10章的现代模块搭成。<bookmark mark='a'/>它们从完全相同的权重出发，按相同的顺序读三十部小说里同样的{g['tokens'] / 1000000.0:.1f}百万个词元，用同样的优化器和学习率安排。<bookmark mark='b'/>只有两处不同。GPT式模型的注意力只往回看，它预测每一个下一个词元。BERT式模型的注意力两边都看，它预测我们遮住的那15%的词元。<bookmark mark='c'/>所以算力完全相同：6，乘以每个词元经过的参数，再乘以词元数。<bookmark mark='d'/>这就是这里所说的公平：同样的模型，同样的数据，同样的算力，只换了目标函数；然后在两个模型都能做的任务上测试。",

    '"Watch the GPT-style model learn.':
        "看GPT式模型学习。左边是它在留出文本上的损失随训练的变化；右边是它在“The door opened, and”这几个词后面写出的东西，在每个检查点冻结，每次都用同一个随机种子。<bookmark mark='a'/>{start}<bookmark mark='b'/>让它读下去。每个点是它在从不用来训练的文本上的损失，淡淡的线是它在训练批次上的损失。检查点按几何级数分布：前面密，因为那时变化最快。{fit}<bookmark mark='c'/>到最后，损失是{last['val']:.2f}奈特，它写出的东西有点像它读过的小说：还谈不上意思，但有了小说的用词和节奏。",

    "f'Untrained, its loss is {first['val']:.2f} nats per token, about":
        "未训练时，它的损失是每个词元{first['val']:.2f}奈特，差不多就是在四千个词元里均匀乱猜的水平，写出来的是噪声。",

    "f'Untrained, its loss is {first['val']:.2f} nats per token, and":
        "未训练时，它的损失是每个词元{first['val']:.2f}奈特，写出来的是噪声。",

    'The two stay together: it is learning the language of the novels':
        '两者一直靠在一起：它在学小说的语言，而不是在背它的训练批次。',

    "f'By the end the training loss is {gap:.2f} nats below":
        "到最后，训练损失比留出损失低了{gap:.2f}奈特：它开始记住它读过的东西了。",

    'f"The BERT-style model learns to fill blanks.':
        "BERT式模型学的是填空。这里有一个句子，遮住了三个词，下面是它在同样的检查点上对每个词的最佳猜测。<bookmark mark='a'/>它的损失只在被遮住的词上计算，降到了{last['val']:.2f}奈特。<bookmark mark='b'/>{cmp_}要公平地比较这两个模型，我们需要两个都能做的任务。",

    "f\"That number can't be compared with the GPT-style model's":
        "这个数不能和GPT式模型的{g_last:.2f}相比：两边的词都看得见时猜一个被遮住的词，是一个和猜下一个词不同、也更容易的问题。",

    "f\"It is higher than the GPT-style model's":
        "它比GPT式模型的{g_last:.2f}还高，但两者没法比较：两边都看得见时猜一个被遮住的词，和猜下一个词是不同的问题，而且掩码模型只从15%的词元里学习。",

    'f"Task one: fill in a blank.':
        "任务一：填空。从两个模型都没读过的段落里取一个句子，去掉一个词，给出{k}个候选：真正的那个词，加上{k - 1}个差不多常见的词。<bookmark mark='a'/>BERT式模型读的是空缺处放着掩码的句子，挑出它认为可能性最大的候选。GPT式模型看不到空缺后面，但它可以把每个候选放进去，比较整句话的概率，这样也用上了空缺后面的词。作为对照，我们也让它只根据空缺前面的词来判断。<bookmark mark='b'/>在{L['cloze_n']}个句子上，随机猜的正确率是{100 / k:.1f}%：只看左边，GPT式模型答对{pct(gl_)}%。<bookmark mark='c'/>给整句打分，答对{pct(g_)}%。<bookmark mark='d'/>{verdict}",

    'f"The masked model wins,':
        "掩码模型赢了，{pct(b_)}%对{pct(g_)}%：正如BERT的作者发现的，直接读两边，胜过通过整句话的似然去间接推断。",

    "f'Here the GPT-style model wins,":
        "这里GPT式模型赢了，{pct(g_)}%对{pct(b_)}%：给整句打分让它也能用上空缺后面的词，而且它从每一个词元学习，而不只是15%。",

    "f'They tie,":
        "两者打平，{pct(g_)}%和{pct(b_)}%：一旦GPT式模型给整句打分，它对空缺后面那些词的利用，就和掩码模型一样好。",

    'f"Task two is the kind of test GLUE was made of':
        "任务二是GLUE里那种测试：给一个句子分类。它出自三十部小说中的哪一部？<bookmark mark='a'/>把每个模型冻结，让一个句子通过它，对整句的最终状态取平均，再在上面训练同样的简单线性分类器，每个模型都用同样的方法。<bookmark mark='b'/>随机猜的正确率是{100 / nc:.1f}%。<bookmark mark='c'/>{verdict}",

    'f"The BERT-style model\'s features name the book':
        "BERT式模型的特征有{pct(pb)}%的时候能说出是哪本书，GPT式模型的特征是{pct(pg)}%：在GLUE式的测试上，双向特征又赢了。",

    'f"Here the GPT-style model\'s features do better':
        "这里GPT式模型的特征更好，{pct(pg)}%对{pct(pb)}%：在我们这么小的规模上，从每个词元学习，似乎比能看两边更重要。",

    "f'The two are about equal":
        "两者差不多，{pct(pg)}%和{pct(pb)}%：在这个测试上、在这个规模上，目标函数几乎没有影响。",

    'f"And the task only one of them can really do: write.':
        "还有一个只有其中一个模型真正能做的任务：写作。<bookmark mark='a'/>给出开头，GPT式模型一个词元接一个词元地采样。<bookmark mark='b'/>BERT式模型也可以被逼着写：在末尾放一个掩码，填上，再放，再填，但它从来没被训练过在后面什么都没有的情况下猜一个词。<bookmark mark='c'/>而且只有因果模型能通过第1部分的链式法则给整段文本一个概率，所以只有它能进入记分板：在《马耳他之鹰》那段文字上，每个字符{ours['bits']:.2f}比特。掩码模型的猜测乘不出一段文本的概率，所以它没有这一行。<bookmark mark='d'/>这就是解码器胜出的更深层原因。一个文本概率的模型，可以采样、可以打分、可以用提示来驱动：一个模型包揽一切，而且规模越大越好。",

    # ------------------------------------------------------------------ 14. Emergence
    'Chapter fourteen. Learning in context, in our own models.':
        '第14章。在我们自己的模型里，在上下文中学习。',

    '"GPT-3\'s surprise was that learning':
        "GPT-3带来的意外是：从提示中学习，是随着规模出现的。在我们的规模上，能看到一点吗？<bookmark mark='a'/>四个大小递增的GPT式模型，都在同样的文本上训练，读同样多的词元。{fifth}<bookmark mark='b'/>先看从上下文中学习最简单的度量：在一个256词元的窗口里，每个位置上的损失。前面的位置几乎没有上下文，后面的位置有很多。<bookmark mark='c'/>{falls}从一到四个词元的上下文，到一百多个，最小的模型每个词元提升了{gains[small['name']]:.2f}奈特；{tail}{btail}",

    'f" And, as a fifth':
        "另外还有第五个：本系列自己的模型，更大，读过的词元是它们的{times:.0f}倍。",

    'Every curve falls from left to right: the words before help.':
        '每条曲线都从左往右下降：前面的词有帮助。',

    'Not every curve falls: some models barely use the words before.':
        '并不是每条曲线都下降：有些模型几乎不用前面的词。',

    "f'the {size_word(large)}-parameter model gains":
        "家族中最大的模型提升了{gains[large['name']]:.2f}奈特：越大的模型，从上下文中学到的越多。",

    "f'the largest of the family gains about the same":
        "家族中最大的模型提升得也差不多，{gains[large['name']]:.2f}奈特。",

    'f" The series\' own model, bigger':
        "本系列自己的模型更大、训练得更久，提升了{gains['base']:.2f}奈特。",

    '"Now replay the training of the largest of the family':
        "现在重放家族中最大的模型的训练过程，看那条曲线是怎么形成的。左边是它在留出文本上的损失；右边是它在上下文每个位置上的损失，在每个检查点冻结。<bookmark mark='a'/>未训练时，曲线是平的：一个什么都不懂的模型，从上下文里什么也得不到。<bookmark mark='b'/>{grow}<bookmark mark='c'/>到最后，前面的词让它每个词元提升{final:.2f}奈特。",

    "f'As it trains, the whole curve drops, and it tilts.":
        "随着训练，整条曲线下降，而且倾斜起来。读了{half['tokens'] / 1000000.0:.2f}百万个词元之后，它从上下文中的最终收益就有了一半。",

    'As it trains, the whole curve drops, but it hardly tilts.':
        '随着训练，整条曲线下降，但几乎没有倾斜。',

    '"A sharper test, the one Part 13 used':
        "一个更尖锐的测试，第13部分用过的：一张由六十个随机常用词组成的列表，然后把同一张列表再来一遍。一个能从上下文中复制的模型，会觉得第二遍比第一遍容易得多。<bookmark mark='a'/>这是每个模型在第一遍和第二遍上猜对下一个词的频率。<bookmark mark='b'/>{lead}{verdict}{when}",

    'Every one of our models copies.':
        '我们的每一个模型都会复制。',

    "None of the family copies; only the series' own model":
        '家族里没有一个会复制；只有本系列自己的模型，更大、训练得更久，会。',

    'f"The smaller models don\'t copy':
        "较小的模型不会复制；从模型{tag_of(first)}开始，就会了。",

    "f'For {who_of(first)}, the second copy":
        "对{who_of(first)}来说，第二遍要容易得多：它猜对了{100 * first['acc2']:.0f}%的词，第一遍只有{100 * first['acc1']:.0f}%。这就是从上下文中复制：第13部分的归纳头。",

    'f"None of our models does much better the second time':
        "我们没有一个模型在第二遍上明显更好：最好的也只提高了{100 * max(jumps.values()):.0f}个百分点。在我们的规模和训练长度下，复制的回路，也就是第13部分的归纳头，还没有形成；第13部分那个小Transformer也不会复制。",

    'f" In model L\'s training, it switched on between':
        "在模型L的训练中，它是在读了{sn[max(0, sn.index(on) - 1)]['tokens'] / 1000000.0:.2f}到{on['tokens'] / 1000000.0:.2f}百万个词元之间出现的。",

    '"Finally, GPT-3\'s own kind of test':
        "最后，是GPT-3自己那种测试，用小说搭成。两本书；提示里有几个带标签的例子，每个例子是一个句子加上它出自哪本书；然后是一个来自模型从没读过的段落的新句子，我们比较模型给两个书名的概率。<bookmark mark='a'/>每个模型都试零个、一个、两个、四个和八个例子。<bookmark mark='b'/>{v0}<bookmark mark='c'/>{v1}{v2}",

    'f"Even with no examples, the models do better than chance':
        "即使一个例子都没有，模型也比随机猜好，最高达到{100 * best0:.0f}%：书名常常是某个人物的名字，而一个提到这个人物的句子，会让这个名字更可能出现。",

    "f'With no examples the models are near chance":
        "没有例子时，模型接近随机猜，最高{100 * best0:.0f}%。",

    "f'For {who}, examples help":
        "对{who}来说，例子有帮助：从没有例子时的{100 * big['fewshot'][0]:.0f}%，升到{shots[-1]}个例子时的{100 * big['fewshot'][-1]:.0f}%。",

    "f'For {who}, examples hurt":
        "对{who}来说，例子反而有害：从没有例子时的{100 * big['fewshot'][0]:.0f}%，降到{shots[-1]}个例子时的{100 * big['fewshot'][-1]:.0f}%；一长串别的句子只会把它搞糊涂。",

    "f'For {who}, examples barely matter":
        "对{who}来说，例子几乎没有影响：没有例子时{100 * big['fewshot'][0]:.0f}%，{shots[-1]}个例子时{100 * big['fewshot'][-1]:.0f}%。",

    "f' And with {shots[-1]} examples, the largest":
        "而在{shots[-1]}个例子时，家族中最大的模型比最小的高出{100 * sz:.0f}个百分点。",

    'f" With {shots[-1]} examples, the family\'s sizes':
        "在{shots[-1]}个例子时，家族中各个大小的模型彼此相差在{100 * abs(sz):.0f}个百分点以内。",

    '"So what did our small models show?':
        "那么，我们的小模型说明了什么？<bookmark mark='a'/>{t1}{t2}{t3}<bookmark mark='b'/>在GPT-3自己的图里，少样本学习要到几十亿参数才变得有用。第13部分给出了机制，也就是会查找和复制的注意力头；第12部分给出了让更大的模型物有所值的规模定律。",

    'Our models use their context more as they grow.':
        '我们的模型越大，越会利用上下文。',

    "Our larger models don't use their context much more":
        '我们较大的模型对上下文的利用，并不比较小的模型多多少。',

    'Copying from the context appears with size.':
        '从上下文中复制，随着规模出现了。',

    "Copying from the context hasn't appeared at our scale.":
        '在我们的规模上，从上下文中复制还没有出现。',

    'And examples in the prompt help the largest model choose.':
        '而提示里的例子能帮助最大的模型做出选择。',

    "But learning a task from examples in the prompt hasn't appeared":
        '但从提示里的例子中学会一个任务，在我们的规模上还没有出现。',

    # ------------------------------------------------------------------ Outro
    'Before the recap, here is the whole lineage on one page':
        "在回顾之前，先把整个谱系放在一页上，时间从左往右走。<bookmark mark='a'/>2017年，Transformer：一个编码器加一个解码器，为翻译而造。<bookmark mark='b'/>不到两年，它分成了三支：编码器，比如赢下各项基准的BERT；编码器-解码器，比如T5；还有解码器，比如GPT。<bookmark mark='c'/>解码器这一支扩大了规模：GPT-3、Codex、InstructGPT、ChatGPT、GPT-4。而随着规模扩大，它也封闭了。<bookmark mark='d'/>从2023年起，旁边出现了开放的分支：Meta的LLaMA，然后是Mistral，每一个都建立在之前公开的设计之上。<bookmark mark='e'/>然后是DeepSeek、月之暗面的Kimi、阿里巴巴的Qwen，甚至OpenAI也再次开放了权重。<bookmark mark='f'/>今天前沿上的每一个开放模型，都是解码器。编码器还活着，用在搜索和分类里，但前沿是从这一支长出来的。",

    "Let's take stock.":
        "来盘点一下。2017年，一个翻译模型让注意力成了整个架构。2018年，先在原始文本上预训练、再微调，成了标准做法，而像BERT这样的掩码模型赢下了当时的基准。然后解码器开始扩大规模：GPT-2能做从没训练过的任务，而GPT-3用了3乘以10的23次方次运算，能从提示里的例子中学习。指令微调和人类反馈把它变成了ChatGPT。开放模型先趋同到同一套配方，然后变得稀疏，又开始分化，与此同时算力每年增长大约5倍。而在我们自己的小模型上，在同样的算力下，我们测出了每种目标函数能换来什么。",

    'All of this comes back.':
        "这一切都会再出现。过去词元的记忆、潜在注意力和混合架构，是第15部分。混合专家和稀疏注意力，第16部分。让规模成为可能的硬件，第17部分；一次前沿训练实际上是怎么组织的，第18部分。便宜地部署这些模型，第19部分。在我们自己的模型上实现指令微调和人类反馈，第27部分；还有推理，第28部分。",

    'Here are six problems to try':
        "这里有六道题，从数GPT-3的参数，到上一章的趋势。在这里暂停，把它们做一做；完整的解答在本部分的笔记里。",

    'Next time: memory.':
        "下一次：记忆。一个读一百万个词元的模型，必须为其中每一个都留下点什么。<bookmark mark='a'/>分组查询注意力和潜在注意力，缩小了随每个词元增长的缓存；<bookmark mark='b'/>线性注意力、delta规则和状态空间模型，用一个大小固定的记忆来代替它；而本部分前沿上的混合架构，把两者结合了起来。这就是第15部分。",

    'The history in this part is best read':
        "本部分讲的历史，最好去读论文原文，它们大多简短而清楚。感谢观看，第15部分见。",
}

PHRASES = {
    'model XS': '模型XS',
    'model S': '模型S',
    'model M': '模型M',
    'model L': '模型L',
    "the series' model": '本系列的模型',
    'half': '二分之一',
    'third': '三分之一',
    'quarter': '四分之一',
    'fifth': '五分之一',
    'sixth': '六分之一',
    'seventh': '七分之一',
    'eighth': '八分之一',
}
