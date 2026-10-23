"""Chinese narration for ai18: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第18部分：大规模预训练'

CHAPTERS = {
    'Hook': '一万六千块GPU，五十四天',
    'Anatomy': '1. 剖析一次前沿训练',
    'Web': '2. 从网页到文本',
    'Dedup': '3. 近似重复：MinHash与LSH',
    'Quality': '4. 质量，以及保持测试的干净',
    'Mixture': '5. 数据配比、合成数据与崩溃',
    'Objectives': '6. 让模型预测什么',
    'Curriculum': '7. 退火、中期训练与长上下文',
    'Accounting': '8. 数一数运算和字节',
    'DataParallel': '9. 数据并行与全规约',
    'ZeRO': '10. ZeRO与FSDP',
    'TensorParallel': '11. 张量并行',
    'Pipeline': '12. 流水线并行',
    'Context': '13. 上下文、专家与利用率',
    'Precision': '14. 更少的位',
    'Stability': '15. 让训练保持稳定',
    'MTP': '16. 往后预测两个词元',
    'Faults': '17. 当硬件出故障',
    'Recipe': '18. 我们自己的完整配方',
    'Outro': '回顾、习题，以及接下来',
}

_DATA = {
    # ------------------------------------------------------------------ Hook
    'f"June 2018. OpenAI\'s first GPT':
        "2018年6月。OpenAI的第一个GPT，在八块显卡上预训练了大约一个月。<bookmark mark='a'/>这是从那以后，一次训练里一起工作的芯片数，画在每上一格就多十倍的刻度上。<bookmark mark='b'/>2019年，Megatron-LM把一个模型分到512块GPU上。2022年，谷歌的PaLM在6144块TPU芯片上训练。2024年，Meta的Llama 3用了16384块GPU；2025年，Llama 4 Behemoth的预训练用了{spoken_int(last[2])}块。<bookmark mark='c'/>七年里，一次训练从{first[2]}块芯片，增加到了它的大约{round(last[2] / first[2], -2):,.0f}倍。本部分讲的，就是这是怎样做到的。",

    'f"Take that run of Llama 3.':
        "就拿Llama 3的那次训练来说。{spoken_int(L['gpus'])}块H100 GPU，一个点代表一块。<bookmark mark='a'/>它们一共做了大约4乘以10的25次方次运算，用了15.6万亿个词元的文本。<bookmark mark='b'/>而且它们一直在出故障。在一段五十四天的时间里，任务停下了{L['interruptions']}次，其中{L['unexpected']}次是计划外的：一块坏掉的GPU，一块内存芯片，一根网线。<bookmark mark='c'/>也就是大约每{P['llama_mtbf_h']:.0f}小时出一次故障，而每一次都会让全部一万六千块GPU停下来，因为它们都在训练同一个模型。",

    'So the question of this part:':
        "所以，本部分的问题是：怎样在一万六千块GPU上，把来自网络的十五万亿个词元变成一个模型，而训练又不会垮掉？<bookmark mark='a'/>答案是一层一层的：数据，目标，算术，在设备之间的切分，位数，稳定性，还有故障。",

    'f"We\'ll build every layer in miniature':
        "每一层，我们都在制作这个视频的这台计算机上，做一个缩微版。<bookmark mark='a'/>来自Common Crawl的{spoken_int(W['n_pages'])}个真实网页，经过过滤、去重和打分。<bookmark mark='b'/>四个进程当作一个小集群，逐一精确地检验每种并行方式。<bookmark mark='c'/>模拟流水线和故障。<bookmark mark='d'/>把训练推到边缘：用更少的位，用很高的学习率。<bookmark mark='e'/>最后，2026年的配方对2020年的配方，放上本系列的记分牌。",

    'This is Part 18 of AI, Built':
        "这是《人工智能，从零搭建》的第18部分，属于第三幕：Transformer时代。<bookmark mark='a'/>本部分要讲：数据，从原始网页到一份干净的配比；训练目标，以及训练的各个阶段；一次训练的算术，用运算次数和字节来算；把模型切到多个设备上的五种方法；更少的位，以及稳定性；一次预测两个词元；挺过故障；以及我们自己的模型，用完整的配方训练出来。",

    # ------------------------------------------------------------------ Anatomy
    'Chapter one. Anatomy of a frontier run.':
        '第1章。剖析一次前沿训练。',

    'A frontier pretraining run is a pipeline.':
        "一次前沿的预训练，是一条流水线。它从网络开始：一次抓取，几十亿个网页，<bookmark mark='a'/>按语言和质量过滤，去重，再混入书籍、代码、数学和合成文本，切成词元。<bookmark mark='b'/>然后模型开始训练：一段很长的预训练阶段；一段很短的、在最好的数据上退火的阶段，常被叫作中期训练；一个教会它长上下文的阶段；最后是第27部分的后训练。<bookmark mark='c'/>这是按比例画出的两次公开训练。Ai2的Olmo 3，七十亿参数：5.9万亿个词元的预训练，然后是1000亿的中期训练，500亿的长上下文训练。Hugging Face的SmolLM3：三个预训练阶段，代码和数学一个比一个多，然后是长上下文。<bookmark mark='d'/>最后几个阶段只占词元的百分之几，却是挑得最用心的。",

    'Here are six open runs from the last two years':
        "这是最近两年里六次公开的训练，以及它们的报告里写明的内容。<bookmark mark='a'/>Llama 3.1 405B：在16384块H100 GPU上训练了15.6万亿个词元，用16位的bfloat数字，用第11部分的AdamW优化器。DeepSeek-V3：在2048块H800上训练了14.8万亿个词元，用8位浮点数。<bookmark mark='b'/>Kimi K2：15.5万亿个词元，用MuonClip，一种Muon优化器的变体。Olmo 3，其中最开放的一个，连数据都公开。<bookmark mark='c'/>还有2026年：英伟达的Nemotron 3 Super，用4位数字预训练了25万亿个词元；DeepSeek-V4-Pro，用Muon训练了33万亿个词元。<bookmark mark='d'/>两年里，词元数翻了一倍，数字从16位缩到8位和4位，优化器也开始改变。每一列，都是本部分的一章。",

    'Inside the pretraining phase, nothing is fixed.':
        "在预训练阶段内部，没有什么是固定不变的。这是DeepSeek-V3的，按它的报告画出来。<bookmark mark='a'/>学习率先在两千步里预热，然后保持在2.2乘以10的负4次方，直到十万亿个词元，<bookmark mark='b'/>然后在接下来的4.3万亿个词元里，沿余弦曲线衰减到原来的十分之一，<bookmark mark='c'/>最后是两小段恒定的学习率。<bookmark mark='d'/>批次也在增大：在最初的半万亿个词元里，从3072个四千词元的序列，增加到15360个。<bookmark mark='e'/>到十万亿个词元时，第二项损失，也就是往后预测两个词元的那一项，权重从0.3降到0.1。",

    'f"How big is such a run?':
        "这样一次训练有多大？第14部分给过规则：训练的代价，大约是每个参数、每个词元六次运算。<bookmark mark='a'/>对Llama 3.1，6乘以4050亿乘以15.6万亿，是{P['llama_6nd'] / 1e+25:.2f}乘以10的25次方，正是Meta报告的数。<bookmark mark='b'/>DeepSeek-V3是混合专家模型，每个词元只用到370亿个参数，所以它需要{P['dsv3_6nd'] / 1e+24:.1f}乘以10的24次方：大约十分之一。<bookmark mark='c'/>它的报告还给出了账单：预训练用了266.4万个H800 GPU小时，另外还有长上下文和后训练阶段；按每小时两美元算，是{P['dsv3_usd'] / 1000000.0:.3f}百万美元。<bookmark mark='d'/>每一万亿个词元要花{D['hours_per_T'] / 1000.0:.0f}000个GPU小时：在2048块GPU上是{P['dsv3_days_per_T']:.1f}天。这只是最终那次训练的价格：不包括之前的实验、数据，也不包括集群。",

    # ------------------------------------------------------------------ Web
    'Chapter two. From the web to text.':
        '第2章。从网页到文本。',

    'f"Almost every open pretraining corpus':
        "几乎每一个开放的预训练语料库，都从同一个地方开始：Common Crawl，吉尔·埃尔巴兹在2007年创办的一个非营利组织，它从2008年起抓取网络，再把存档免费送出，已经超过十拍字节。<bookmark mark='a'/>每次抓取被切成十万个文件，这里要紧的有两种形式：WARC文件存的是原始响应，连同全部HTML；WET文件存的是Common Crawl自己抽取出来的文本。<bookmark mark='b'/>为了本部分，我们取了2026年9月那次抓取的三个WET文件，每个取三段：{spoken_int(W['n_pages'])}个网页，{W['text_bytes'] / 1000000.0:.0f}兆字节的文本，共{W['n_langs']}种语言。接下来四章里的一切，都发生在这些网页上。",

    'f"The first step is extraction':
        "第一步是抽取：把HTML变成文本。一个网页，大部分都不是正文。脚本、样式、菜单、页脚、按钮。<bookmark mark='a'/>这是我们WARC片段里的一个网页。它的HTML有{spoken_int(ex['html_bytes'])}字节。<bookmark mark='b'/>FineWeb用的抽取器Trafilatura，从中保留了{spoken_int(ex['text_bytes'])}字节：文章本身，不要它周围的菜单。<bookmark mark='c'/>在我们片段里全部{W['warc_pages']}个HTML网页上，{W['html_bytes'] / 1000000.0:.0f}兆字节的HTML变成了{W['extracted_bytes'] / 1000000.0:.1f}兆字节的文本：大约{100 * W['extracted_share']:.0f}%。<bookmark mark='d'/>这一步比听起来更要紧。FineWeb的作者把同一次抓取用两种方式抽取，各训练小模型，结果Trafilatura的文本，胜过了Common Crawl自己的WET文本。",

    'f"Next: which language is each page in?':
        "下一步：每个网页是什么语言？<bookmark mark='a'/>在那之前，先做一个只看网址的廉价过滤：一份成人和赌博网站的黑名单，去掉了{W['blocked']}个网页。<bookmark mark='b'/>然后是语言识别器：fastText的，来自Facebook AI研究院，它是一个建立在字符片段上的线性模型，在176种语言里挑一种，快到足以在几十亿个网页上运行。<bookmark mark='c'/>这是我们的样本里有什么。英语：{spoken_int(en)}个网页，大约{round(100 * share)}%；其余的分散在另外{W['n_langs'] - 1}种语言里。<bookmark mark='d'/>FineWeb只有在识别器至少有65%的把握时，才把一个网页算作英语。这又去掉了{W['english_below']}个；我们还去掉了不到五十个词的网页。<bookmark mark='e'/>{spoken_int(W['english'])}个英语网页进入下一步。多语言模型，比如支持119种语言的Qwen3，会对每种语言各跑一遍这样的流程。",

    # ------------------------------------------------------------------ Dedup
    'Chapter three. Near-duplicates':
        '第3章。近似重复：MinHash与局部敏感哈希。',

    'f"The web repeats itself.':
        "网络总在重复自己。镜像站、模板、换了个价格的同一个商品页面。<bookmark mark='a'/>我们样本里的这两个网页来自同一个网站：它们的短语有{100 * ex['jaccard']:.0f}%是相同的。<bookmark mark='b'/>重复会浪费算力，还会被背下来：Lee和同事在2022年发现，用去过重的数据训练出来的模型，原样复述训练文本的次数少了十倍。<bookmark mark='c'/>要比较文档，就把每篇切成片段，也就是相互重叠的五词短语，FineWeb就是这样做的。<bookmark mark='d'/>如果两篇文档的片段集合重叠，它们就相似：这就是杰卡德相似度，交集的大小除以并集的大小。<bookmark mark='e'/>但要把一百亿个网页两两比较，需要5乘以10的19次方次比较。我们需要一条捷径。",

    'f"The shortcut is a beautiful fact from 1997':
        "这条捷径，是1997年的一个漂亮的事实，由AltaVista的安德烈·布罗德为了找出重复的网页而发现。随便挑一个哈希函数，它给每个片段一个随机数。<bookmark mark='a'/>在两个集合的并集里，哈希值最小的那个片段，等可能地是其中任何一个。<bookmark mark='b'/>两篇文档的最小哈希值相同，当且仅当这个片段两边都有，也就是落在交集里。<bookmark mark='c'/>所以它们相同的概率，就是交集的大小除以并集的大小：正是杰卡德相似度本身。<bookmark mark='d'/>像FineWeb那样，每篇文档保留112个这样的最小值：一个由112个数组成的签名；两个签名有多大比例的位置相同，就估计了它们的相似度。我们在{spoken_int(len(s))}对网页上检验了它，每对里的一篇替换掉了一些词：<bookmark mark='e'/>估计值落在对角线上，平均偏差{D['agree_err']:.3f}。",

    'f"One signature per document still leaves':
        "每篇文档一个签名，仍然要两两比较。局部敏感哈希避开了这一点。把{b * r}个最小哈希切成{b}个带，每带{r}个。<bookmark mark='a'/>对相似度为s的两篇文档，每个最小哈希相同的概率是s，所以一整个带的r个都相同的概率，是s的r次方。<bookmark mark='b'/>没有一个带相同的概率，是1减s的r次方，再取b次方。<bookmark mark='c'/>至少有一个带相同、这一对成为候选的概率，就是1减去它。<bookmark mark='d'/>现在，只有在某个带上落进同一个桶的文档才需要比较，而这条曲线是S形的：相似度低于大约0.5的一对几乎从不碰撞，高于0.8的几乎总会碰撞，一半的位置在{D['s_half']:.2f}。<bookmark mark='e'/>这是我们实测的网页对，按相似度分组。它们跟着公式走，任何一组里最多偏离{worst:.2f}。",

    "'What did we find? ' + found":
        "我们发现了什么？{found}<bookmark mark='a'/>第1部分的三十个古登堡文件，是一个更清楚的检验。{books}<bookmark mark='b'/>在整个网络的规模上，数字就惊人了。对Olmo 3，去掉完全相同的副本，让数据池缩小了{O['exact']}%，MinHash又去掉了{O['fuzzy']}%，重复的子串去掉了剩余字节的{O['substring']}%：387亿篇文档变成了97亿篇。<bookmark mark='c'/>还有一个意外。FineWeb起初把全部96次抓取放在一起相互去重，结果模型变差了：在最老的那些抓取里，留下来的是没人复制过的垃圾。每次抓取各自去重，效果更好。",

    "f'In our {spoken_int(D['n'])} English pages, {D['exact']} exact copies and {D['removed']} near-duplicates: {100 * share:.1f} percent. Common":
        "在我们的{spoken_int(D['n'])}个英语网页里，有{D['exact']}个完全相同的副本，{D['removed']}个近似重复：占{100 * share:.1f}%。Common Crawl在一次抓取里本来就避免重复抓取同一个网址，而我们的样本又很小。",

    "f'In our {spoken_int(D['n'])} English pages, {D['exact']} exact copies and {D['removed']} near-duplicates: {100 * share:.1f} percent of":
        "在我们的{spoken_int(D['n'])}个英语网页里，有{D['exact']}个完全相同的副本，{D['removed']}个近似重复：占网页的{100 * share:.1f}%。",

    'f"Each ends with the same licence, with the book\'s title changed: LSH catches all':
        "每个文件的结尾都是同一份许可证，只是换了书名：LSH抓住了全部{D['foot_pairs']}对许可证，而{D['body_pairs']}对小说一对也没有抓。",

    'f"Each ends with the same licence, with the book\'s title changed: LSH catches {':
        "每个文件的结尾都是同一份许可证，只是换了书名：{D['foot_pairs']}对许可证里，LSH抓住了{D['foot_caught']}对；{D['body_pairs']}对小说里，抓住了{D['body_caught']}对。",

    # ------------------------------------------------------------------ Quality
    'Chapter four. Quality, and keeping the test clean.':
        '第4章。质量，以及保持测试的干净。',

    'Quality is harder than language or duplicates':
        "质量比语言和重复更难：哪些网页教给模型的东西最多？2024年，Hugging Face的FineWeb团队给出了一个如今已成标准的配方。<bookmark mark='a'/>请一个大模型给网页打分：Llama 3 70B，用一个提示词，教育价值的五条标准，每满足一条加一分，给46万个网页打零到五分。<bookmark mark='b'/>然后训练一个便宜的小模型去模仿这些分数：在一个嵌入模型上面加一个线性层，用其中41万个来训练；以三分为界，它和Llama 3相比，F1分数是82%。<bookmark mark='c'/>用它跑遍全部十五万亿个词元，花了六千个GPU小时，保留三分及以上的网页：1.3万亿个词元。<bookmark mark='d'/>在用3500亿个词元训练的17亿参数模型上，这把考知识的MMLU从33%提高到37%，把考推理的ARC从46%提高到57%。",

    'f"We can run this recipe ourselves':
        "这个配方我们可以自己跑一遍，因为FineWeb公开了Llama 3的标注。<bookmark mark='a'/>我们下载了其中{spoken_int(Q['n'])}条。{commonest}{100 * sum(counts[3:]) / Q['n']:.0f}%得到三分或以上，我们的样本里有{counts[5]}个得了五分。<bookmark mark='b'/>小模型我们用的是fastText，一个建立在词和词对上的线性模型，几秒钟就能训练好；用{spoken_int(Q['n_train'])}个网页来训练，分界线在另外一千个网页上选定。<bookmark mark='c'/>{verdict}",

    'Most pages score one: a little information':
        '大部分网页得一分：有一点信息，没什么教学价值。',

    "f'The commonest score is":
        "最常见的分数是{int(np.argmax(counts))}。",

    "f'Ours reaches an F1 of {100 * f1:.0f} percent, close":
        "我们的F1达到{100 * f1:.0f}%，和他们的接近，用的只是一小部分标注。",

    "f'Ours reaches an F1 of {100 * f1:.0f} percent, against":
        "我们的F1达到{100 * f1:.0f}%，他们的是82%：标注只有他们的三十分之一，用的又是词袋而不是嵌入模型，它抓住了大部分好网页，但放进来的差网页也差不多一样多。",

    'f"Now run it on our crawl sample.':
        "现在把它用到我们的抓取样本上。<bookmark mark='a'/>这是它打分最高的两个网页，<bookmark mark='b'/>以及打分最低的两个。<bookmark mark='c'/>在我们的{spoken_int(Q['cc_n'])}个英语网页里，它保留了{Q['cc_kept_n']}个，占{100 * Q['cc_kept']:.1f}%；FineWeb-Edu保留了FineWeb大约百分之九的词元。<bookmark mark='d'/>别的配方瞄准别的东西：DataComp-LM，简称DCLM，训练它的fastText过滤器去找像指令和好回答的文本；一个七十亿参数的模型，用其中2.6万亿个词元训练，在MMLU上达到了64%。2026年每一个像样的语料库，都有这样的过滤器，大多数还不止一个。",

    'f"One more filter, pointed the other way.':
        "还有一个过滤器，方向正相反。如果一个基准测试的题目就在网上，模型可以靠记忆通过它。<bookmark mark='a'/>GPT-3的作者在每个测试和训练文本之间，寻找任何共有的十三词序列，并把找到的标记出来。<bookmark mark='b'/>我们可以检查本系列自己的测试。记分牌用的那段文字，《马耳他之鹰》的第二章，有{spoken_int(K['passage_grams'])}个十三词序列；其中出现在我们训练用的三十部小说里的，有{K['passage_hits']}个；它的八词序列里，有{K['passage_hits8']}个。{clean}<bookmark mark='c'/>{held}一个序列，比如这一段，是一部小说里重复出现的一句话。在网上，热门的基准测试到处都有人抄，所以各个实验室现在对它们报告的每一个测试，都要做这样的检查。",

    'Not quite clean: the passage shares':
        '不完全干净：这段文字和训练文本有一部分措辞相同。',

    "f'Our held-out paragraphs are almost clean:":
        "我们的留出段落几乎是干净的：{spoken_int(K['valid_paras'])}段里，有{K['valid_flagged']}段和训练文本共有",

    "f'Our held-out paragraphs are less clean:":
        "我们的留出段落没那么干净：{spoken_int(K['valid_paras'])}段里，有{K['valid_flagged']}段和训练文本共有",

    # ------------------------------------------------------------------ Mixture
    'Chapter five. Mixtures, synthetic data and collapse.':
        '第5章。数据配比、合成数据与崩溃。',

    'A corpus is a mixture:':
        "一个语料库就是一份配比：网页、百科、代码、书籍、数学、论文。每样要多少？<bookmark mark='a'/>2020年，The Pile是手工定的权重：四分之一网页，百分之九维基百科，外加另外二十个来源。<bookmark mark='b'/>2023年，DoReMi把权重学了出来：一个小代理模型边训练，一个对手边不断提高它预测得最差的那个领域的权重，这个最差是相对一个参考模型而言的；最后得到的权重，让一个八十亿参数的模型用少了2.6倍的步数，就达到了基线的水平。<bookmark mark='c'/>2024年，RegMix把它变成了回归问题：训练512个微型模型，用随机的配比；把你关心的损失拟合成配比的函数；再用拟合最看好的那份配比去训练大模型。在十亿参数的规模上，它挑出的配比胜过了他们试过的全部64种。",

    'f"We ran RegMix on the thirty novels.':
        "我们在三十部小说上跑了RegMix。把它们分成四组：美国小说，英国的社会小说，冒险与推理，以及译作加上《尤利西斯》。<bookmark mark='a'/>我们的目标，是记分牌自己的那本书，《马耳他之鹰》，一部1930年的美国侦探小说；我们在它的第一章和第三章上调，把第二章，也就是记分牌那段文字，留着做测试。<bookmark mark='b'/>{len(proxy)}个微型模型，每个用一份随机配比。这是每个模型在目标上的损失，对它所含美国小说的比例画出来：{trend}。<bookmark mark='c'/>在四个权重以及它们两两乘积上的回归，用其余的模型来预测每个模型的损失，相关系数是{M['loo_corr']:.2f}。<bookmark mark='d'/>问它最好的配比，它{lean}：四组分别占{shares}%，可以和这些书本身的自然比例对照一下。",

    'the more American text, the lower the loss':
        '美国小说越多，损失越低，不过另外三组也有影响',

    'more American text helps a little':
        '美国小说多一点会有一点帮助，但其他几组同样要紧',

    "the share of American text alone doesn't decide it":
        '光看美国小说的比例，决定不了损失',

    '"Now the test: does the pick carry over':
        "现在来检验：这份配比，换到更大的模型上还成立吗？我们在更大的规模上把每份配比重新训练一遍，各用两个种子。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{cost}<bookmark mark='c'/>这就是普遍的教训：配比是为某个目标挑的，所以要说清楚是哪个目标，并且在挑选时从没见过的文本上测试。",

    'And on the thirty novels as a whole it pays a little':
        '而在三十部小说整体上，它要付出一点代价：朝一本书去调，就要牺牲别的书。',

    'And on the thirty novels as a whole it costs nothing':
        '而在三十部小说整体上，它没有付出我们测得出来的代价。',

    'f"On the held-out chapter, RegMix\'s pick beats':
        "在留出的那一章上，RegMix挑的配比胜过自然配比，{r:.3f}奈特对{n_:.3f}，差距大于两个种子之间的差别。",

    'f"On the held-out chapter, RegMix\'s pick does worse':
        "在留出的那一章上，RegMix挑的配比比自然配比还差，{r:.3f}奈特对{n_:.3f}：在微型模型上拟合的回归，没能推广到更大的模型。",

    'f"On the held-out chapter, RegMix\'s pick and the natural':
        "在留出的那一章上，RegMix挑的配比和自然配比的差别，没有超出两个种子之间的噪声，分别是{r:.3f}和{n_:.3f}奈特：在我们的规模上，三十部小说怎么配，没有运气重要。",

    'f"When good text runs short':
        "好文本不够用的时候，有两种办法把它撑开。一是重复：Muennighoff和同事在2023年发现，同一份数据最多重复大约四遍，几乎和新数据一样好，再往后，收益就迅速消失。<bookmark mark='a'/>二是改写。2024年，苹果和卡内基梅隆大学的WRAP，让一个语言模型把嘈杂的网页改写成百科条目或问答的形式；把真实文本和改写文本放在一起训练，达到同样的质量大约快了三倍。<bookmark mark='b'/>Kimi K2的报告在知识上做了测量。同一段文本重复十遍，教出的模型能答对一组事实问题里的{K['rephrase'][0][1]:.2f}%。改写一次，再重复十遍：{K['rephrase'][1][1]:.2f}%。改写成十种不同的说法，每种只读一遍：{K['rephrase'][2][1]:.2f}%。",

    'f"But training on a model\'s output':
        "但用模型的输出来训练，有一种已知的失败。Shumailov和同事在2024年的《自然》上，把它叫作模型崩溃：每一代都用上一代的样本来训练，分布的尾巴就会消失。我们可以在最简单的语言模型上看到它：小说里各个词元的频率。<bookmark mark='a'/>用五万个真实词元来拟合它；从中采样五万个；用这些来拟合下一代；如此反复。一个罕见的词元，只要有一次没被采到，就永远消失了。<bookmark mark='b'/>经过{gens}代，它能产生的词元从{start:,.0f}个降到{end:,.0f}个，而丢掉的那些，在真实文本里占{100 * lost:.0f}%。<bookmark mark='c'/>{climb}<bookmark mark='d'/>同一年，Gerstgrasser和同事找到了出路：保留真实数据，把每一代的样本加进去，而不是替换它。{cure}2026年的合成数据就是这样用的：和真实文本放在一起，绝不取而代之。",

    # ------------------------------------------------------------------ Objectives
    'Its cross-entropy on real text climbs with every generation.':
        '它在真实文本上的交叉熵，一代比一代高。',

    'Its cross-entropy on real text climbs over the generations.':
        '它在真实文本上的交叉熵，随着一代代上升。',

    'Its cross-entropy on real text barely moves.':
        '它在真实文本上的交叉熵几乎没变。',

    'Nothing real is lost, and the damage stays small.':
        '真实的东西一样也不会丢，损害也一直很小。',

    'Chapter six. What the model is asked to predict.':
        '第6章。让模型预测什么。',

    'f"Pretraining needs a question to ask':
        "预训练需要对每一段文本提一个问题。这是《傲慢与偏见》的第一句话，被我们的分词器切成{n}个词元，以及各个实验室对它提过的四种问题。<bookmark mark='a'/>GPT的因果目标：根据前面的词元，预测每一个词元。每个词元都是目标。<bookmark mark='b'/>BERT的掩码目标：藏起百分之十五的词元，大多换成一个掩码，只预测这些。<bookmark mark='c'/>T5的片段破坏：把一小段一小段的词元换成单个标记，让模型写出每个标记藏起了什么。<bookmark mark='d'/>还有中间填充。2022年，OpenAI的Bavarian和同事把文档在两个随机位置切开，把中间那段挪到末尾，前后加上表示前缀、后缀和中间的标记。模型仍然只是预测下一个词元。但现在，给它一个开头和一个结尾，它就能写出中间的部分，这正是代码编辑器需要的。",

    'f"Count the targets.':
        "数一数目标。在一个256个词元的序列里，因果目标给出255个可供学习的预测。掩码给出大约{tg['mlm']}个，片段破坏大约{tg['span']}个，标记也算在内。<bookmark mark='a'/>中间填充保留了全部：它仍然是下一个词元的预测，只是在重新排列过的文本上。Bavarian的团队把一半的文档按这种顺序排列，发现普通的从左到右的困惑度没有变化：填空能力是白送的。<bookmark mark='b'/>DeepSeek-V3把百分之十的文档这样重新排列。<bookmark mark='c'/>所以2026年的答案，就是第14部分的那个：对每一个词元，预测下一个词元，因为这样的模型可以采样、可以打分、可以用提示来引导；要教它填空，就去重排数据，而不是改变目标。",

    # ------------------------------------------------------------------ Curriculum
    'Chapter seven. Annealing, mid-training, long context.':
        '第7章。退火、中期训练与长上下文。',

    '"The learning rate falls as a run ends':
        "一次训练快结束时，学习率会降下来，而怎么降很要紧。第11部分用的是余弦：它一开始就衰减，所以你必须事先知道训练有多长。<bookmark mark='a'/>从2024年起，越来越多的训练用预热、稳定、衰减：让学习率平平地保持在峰值，只在最后，用最后十分之一或五分之一的步数来冷却。<bookmark mark='b'/>这是我们自己的2026配方的训练，来自第18章。{shape}<bookmark mark='c'/>好处是：从稳定阶段的任何一个检查点，都可以分出一段短短的冷却。我们在第{start}步分出了一支。<bookmark mark='d'/>{verdict}所以WSD被用来从一次训练里，尝试许多种训练长度，或许多种数据配比。",

    "f\"At step {bstep}, the branch's held-out loss is {b['val']:.2f}, against {b['stable_val']:.2f} for the run still at its peak learning":
        "在第{bstep}步，这一支的留出损失是{b['val']:.2f}，而仍在峰值学习率上的那次训练是{b['stable_val']:.2f}：一个训练完成的模型，不用从头再来。",

    "f\"At step {bstep}, the branch's held-out loss is {b['val']:.2f}, against {b['stable_val']:.2f} for the run still at its peak:":
        "在第{bstep}步，这一支的留出损失是{b['val']:.2f}，而仍在峰值上的那次训练是{b['stable_val']:.2f}：在我们的规模上，冷却带来的好处不大。",

    'The held-out loss creeps down during the stable phase':
        '留出损失在稳定阶段缓缓下降，到了冷却阶段降得更快。',

    'The held-out loss falls through the stable phase and the cooldown alike.':
        '留出损失在稳定阶段和冷却阶段下降得差不多。',

    'The end of a run is also where the best data goes.':
        "一次训练的结尾，也是最好的数据去的地方。模型在学习率下降时读到的东西，会在最终的模型上留下很深的印记，所以各个实验室把最好的文本留到冷却阶段，叫它退火，或者中期训练。<bookmark mark='a'/>SmolLM3分三个阶段训练，网页文本从85%降到63%，代码和数学从15%升到37%。<bookmark mark='b'/>Llama 3在最后四千万个词元上退火，把学习率降到零，用的是它最好的来源，再把各个检查点平均起来。<bookmark mark='c'/>Qwen3的第二阶段是五万亿个词元，偏重科学、代码和推理，衰减也更快。<bookmark mark='d'/>Olmo 2把百分之五到十的算力花在中期训练上，用从检查点出发的小型退火实验来挑数据：为了挑它的数学数据，做了十九次微退火。",

    'f"The last stage teaches length.':
        "最后一个阶段教的是长度。注意力的代价随上下文长度的平方增长，所以模型用四千或八千个词元预训练，到最后再拉长。<bookmark mark='a'/>Llama 3分六个阶段，从八千拉到十二万八千，用了大约8000亿个词元。DeepSeek-V3先到三万二千，再到十二万八千，各用一千步。Qwen3和Olmo 3只拉长了一次。DeepSeek-V4则在预训练过程中就让长度增长，从四千一直到一百万。<bookmark mark='b'/>要拉长，位置之间就得保持可以区分。第13部分的旋转位置编码，按每个词元一个角度，旋转每一对维度，越往后的维度对转得越慢。<bookmark mark='c'/>用通常的基频一万，最慢的那一对要{rope[0]['longest'] / 1000.0:.0f}000个词元才转一圈。把基频调高，像Llama 3调到五十万、Qwen3调到一百万那样，就要{rope[1]['longest'] / 1000000.0:.1f}百万和{rope[2]['longest'] / 1000000.0:.1f}百万个词元：给长文档留出了空间。",

    # ------------------------------------------------------------------ Accounting
    'Chapter eight. Counting FLOPs and bytes.':
        '第8章。数一数运算和字节。',

    'First, arithmetic.':
        "先说算术。Transformer几乎全部的工作都是矩阵乘法，每个权重矩阵一次。<bookmark mark='a'/>前向时，每个权重乘上一个输入，再加进去：每个权重、每个词元两次运算。<bookmark mark='b'/>反向时，每个权重还要再用两次。一次是把误差传回下面一层：两次运算。<bookmark mark='c'/>另一次是算它自己的梯度：又是两次。<bookmark mark='d'/>每个权重、每个词元六次运算：这就是C等于6ND里的那个6，再加上注意力自己的乘法，它们随上下文长度增长。",

    'f"We can check this on our own model':
        "我们可以在自己的模型上检验这一点，用PyTorch的浮点运算计数器，它统计一个训练步里每一次矩阵乘法的运算次数，这一步有{T}个词元。<bookmark mark='a'/>反向传播的代价是前向的{A['ratio']:.2f}倍。<bookmark mark='b'/>总数等于6乘以权重数乘以词元数，误差在{100 * abs(A['both'] / A['six'] - 1):.2f}%以内。<bookmark mark='c'/>注意力自己的乘法，也就是打分和加权求和，在这个长度上又多出{100 * A['attn_share'] / (1 - A['attn_share']):.0f}%，而且随长度增长。",

    'f"Now memory.':
        "再说内存。用混合精度训练，这是2018年以来的标准配方，每个参数要花十六个字节。<bookmark mark='a'/>bfloat16的权重两个字节，它的梯度两个字节；<bookmark mark='b'/>然后是优化器的状态，用32位：权重的一份主副本，四个字节，再加上Adam的两个滑动平均，各四个字节。<bookmark mark='c'/>对Llama 3.1，十六个字节乘以4050亿，是{m16['llama3'] / 1000000000000.0:.1f}太字节：光是装下模型，就至少要{P['h100_needed']}块80GB的GPU，激活还没算。<bookmark mark='d'/>这里省下的每一个字节都有用；比如DeepSeek-V3，就把Adam的平均值存成16位。",

    'f"The other big consumer of memory':
        "内存的另一个大户是激活：前向传播必须为反向传播留下的一切。我们清点了PyTorch的autograd为我们的模型保存的张量，长度从64到1024个词元。<bookmark mark='a'/>注意力融合起来，就像PyTorch运行它的那样，内存是一条直线：每个词元、每层{A['per_fused']:.1f}个数，以宽度为单位。<bookmark mark='b'/>按教科书的方式算注意力，它还要为每个头保留一个T乘T的矩阵：一条抛物线。这个二次项，正是FlashAttention去掉的。<bookmark mark='c'/>或者只保留每个块的输入，在反向传播时把其余的重新算一遍：每个词元、每层一个数，代价是这里多{100 * (A['ckpt_ratio'] - 1):.0f}%的算术，一般最多多三分之一。<bookmark mark='d'/>在前沿规模上，这很要紧。按Korthikanti和同事的算法，在Llama 3.1的形状、八千个词元下：每层四点五吉字节，每个序列超过半太字节。",

    # ------------------------------------------------------------------ DataParallel
    'Chapter nine. Data parallelism and the all-reduce.':
        '第9章。数据并行与全规约。',

    'f"The simplest way to use many GPUs':
        "用许多块GPU最简单的办法：给每块一份完整的模型副本，和批次的一部分。<bookmark mark='a'/>每块算出自己那部分的梯度。<bookmark mark='b'/>然后它们把梯度平均起来，这样每份副本都走完全相同的一步，始终保持一致。这个平均就是全规约，第17部分讲过的操作。<bookmark mark='c'/>这和在一个设备上用一个大批次走一步是一样的。我们检验过：这台计算机的{p}个进程，每个拿四分之一的批次，和一个拿全部批次的进程相比，跑{Pr['steps']}步AdamW：损失吻合到{digits}位数字，每个参数都相差在{Pr['err']['dp']:.5f}以内；不同的只是加法的顺序。",

    'Recall the ring of Part 17.':
        "回忆一下第17部分的环。把每块GPU的梯度切成p块。<bookmark mark='a'/>每一步，每块GPU把一块传给它的邻居，邻居把它加到自己的那块上；p减1步之后，每块GPU都持有某一块的完整总和：这就是规约-分散。<bookmark mark='b'/>再用p减1步，把算好的块传一圈：这就是全收集。<bookmark mark='c'/>每块GPU发送的，是梯度字节数的p分之p减1的两倍。下一章的ZeRO，在这两半之间做有用的工作。",

    'Part 17 said that no algorithm beats the ring on bandwidth.':
        "第17部分说过，在带宽上没有算法能胜过环。原因在这里。跟踪一个数，全部p块GPU最后都必须持有它的总和。每条消息携带一个值，可能是一个部分和。<bookmark mark='a'/>总有某块GPU第一个拿到完整的总和。其他每块GPU的值都必须经过一串消息到达它：这至少要p减1条消息。<bookmark mark='b'/>在那一刻，别人都还没有总和，所以其余p减1块GPU，每块都至少还需要一条消息。<bookmark mark='c'/>每个数两倍的p减1条消息，n个数都是如此。<bookmark mark='d'/>p块GPU可以同时接收，每块每秒B字节，所以时间至少是p分之p减1的两倍，乘以n除以B：正是环的时间。<bookmark mark='e'/>环在带宽上是最优的。剩下能赢的是延迟，小消息用树；还有重叠：反向传播还在算前面几层的时候，就把最后几层的梯度发出去。",

    '"We timed the three operations':
        "我们用PyTorch自带的分布式库，在这台计算机的四个进程上，给这三种操作计时，消息从一千字节到32兆字节。<bookmark mark='a'/>虚线是第17部分的α–β模型，延迟和带宽由点对点消息拟合得出：环的每一步一个延迟，加上环的字节数。<bookmark mark='b'/>{verdict}",

    'Beyond a few hundred kilobytes, every measured time':
        '超过几百千字节以后，每个测得的时间，都在模型预测的两倍以内。',

    'f"Large messages took {min(r.values()):.0f} to {worst:.0f} times':
        "大消息花的时间，是模型预测的{min(r.values()):.0f}到{worst:.0f}倍，而这台计算机的四个核心正和别的任务共用：这个模型描述的，是每台设备各有一条链路、别的什么都不用做的情形。但形状是对的：小消息有一个延迟的下限，之后时间和字节数成正比地增长。",

    # ------------------------------------------------------------------ ZeRO
    'Chapter ten. ZeRO and FSDP.':
        '第10章。ZeRO与FSDP。',

    'Data parallelism has a waste built in':
        "数据并行天生带着浪费：每块GPU都保存着整个模型、它的梯度和优化器状态，也就是第8章那每个参数十六个字节，全都一模一样。<bookmark mark='a'/>2019年，微软的Samyam Rajbhandari和同事提出了ZeRO，零冗余优化器：把它们拆开。<bookmark mark='b'/>第一阶段：每块GPU只保存四分之一参数的优化器状态，也只更新这些参数。<bookmark mark='c'/>第二阶段：每块GPU也只保存自己那四分之一的梯度。<bookmark mark='d'/>第三阶段：权重也只保存自己的那四分之一，别的部分在某一层需要之前，才从邻居那里取来，用完就丢掉。PyTorch对第三阶段的实现叫FSDP，全分片数据并行。",

    'f"The arithmetic, in the paper\'s notation':
        "用论文的记号来算一算：Ψ个参数，每个参数K字节的优化器状态，混合精度的Adam是十二，N块GPU。<bookmark mark='a'/>普通的数据并行：每块GPU上每个参数十六个字节。按他们的例子，75亿个参数，64块GPU：每块{mem[0]:.0f}吉字节。<bookmark mark='b'/>第一阶段把优化器的十二个字节除以N：{mem[1]:.1f}。<bookmark mark='c'/>第二阶段，梯度也除：{mem[2]:.1f}。<bookmark mark='d'/>第三阶段把一切都除掉：每块GPU{mem[3]:.2f}吉字节。六十四块GPU加起来，只存一份模型，而不是六十四份。",

    'What does sharding cost in communication?':
        "分片在通信上要付出什么？第一和第二阶段，没有任何额外代价：全规约本来就是一次规约-分散加一次全收集。每块GPU对梯度做规约-分散，更新自己的四分之一，再对新的权重做全收集。<bookmark mark='a'/>第三阶段只保存每层权重的四分之一。这一层前向运行之前，各块GPU对它做一次全收集；用完就丢掉。<bookmark mark='b'/>反向传播又需要这些权重：再收集一次。<bookmark mark='c'/>梯度做规约-分散，每块GPU只保留自己的四分之一。<bookmark mark='d'/>这是对参数走三遍，而不是两遍：通信量多一半，换来内存除以N。Meta训练Llama 3时，在数据并行组里用了FSDP；DeepSeek-V3用的是第一阶段。",

    '"We built ZeRO stage three ourselves':
        "我们自己搭了ZeRO第三阶段，用四个进程：每个进程保存每一层参数、梯度和Adam矩的四分之一，在一层运行之前，不论前向还是反向，才把它收集起来，再对它的梯度做规约-分散。<bookmark mark='a'/>{same}<bookmark mark='b'/>每个进程保存的数少了{ratio_mem:.0f}倍，外加一次一层。<bookmark mark='c'/>而它发送的是{ratio_comm:.2f}倍：{match15}",

    "f'After {Pr['steps']} steps, its parameters match":
        "{Pr['steps']}步之后，它的参数和单进程运行相比，相差在{e3:.5f}以内，和普通数据并行一样：不同的只是加法的顺序。",

    "f'After {Pr['steps']} steps, its parameters differ":
        "{Pr['steps']}步之后，它的参数和单进程运行相差最多{e3:.5f}，超出了舍入能解释的范围。",

    # ------------------------------------------------------------------ TensorParallel
    'Chapter eleven. Tensor parallelism.':
        '第11章。张量并行。',

    'When a single layer is too big':
        "当一层对一块GPU来说太大，或者太慢，就把这一层本身切开。英伟达的Megatron-LM在2019年展示了怎样对Transformer的两半做到这一点。拿MLP来说：Z等于X乘以A，过一个非线性，再乘以B。<bookmark mark='a'/>把A按列切开，每块GPU一半。每块用完整的输入算出自己那一半的Y，不需要通信。<bookmark mark='b'/>非线性对每一列单独作用，所以它也留在本地。<bookmark mark='c'/>现在把B按行切开。第一块GPU用它那一半的Y乘以它那一半的B，第二块乘另一半：每块都得到一个全尺寸的部分结果，答案是它们的和。一次全规约。<bookmark mark='d'/>所以整个MLP在前向时花一次全规约，叫作g，反向时花一次，叫作f，用于两半都用过的那个输入的梯度。",

    'Attention splits even more naturally':
        "注意力切起来更自然：它的各个头是相互独立的。<bookmark mark='a'/>给每块GPU一半的头的查询、键和值；每块单独算自己的头，按行切开的输出投影，最后一次全规约。<bookmark mark='b'/>所以一个Transformer层，前向花两次全规约，反向两次，每次都是一个完整的激活：批次，乘以序列长度，乘以宽度。<bookmark mark='c'/>每一层、每个微批次都要来一遍，所以张量并行住在带宽最高的地方，一台机器的NVLink域里。Llama 3用了八路张量并行，是它四个维度里最内层的一个。<bookmark mark='d'/>2022年的一个改进，序列并行，把每次全规约换成一次规约-分散加一次全收集，并且把剩下的激活也按位置切开。",

    '"We split one block of our own transformer':
        "我们用这种方法，把自己的Transformer的一个块，切到两个、再切到四个进程上，每个f和g各用一次全规约。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>每个进程保存块里矩阵的一半，或者四分之一，次数也正是Megatron的：前向两次全规约，反向两次。",

    'f"On two GPUs and on four':
        "在两块和四块GPU上，切开的块的输出和每一个梯度，都和没切的块吻合到{worst:.6f}以内：这是舍入，来自加法顺序的不同。",

    'f"The split block\'s results differ':
        "切开的块的结果和没切的块相差最多{worst:.6f}：超出了舍入。",

    # ------------------------------------------------------------------ Pipeline
    'Chapter twelve. Pipeline parallelism.':
        '第12章。流水线并行。',

    'f"Tensor parallelism cuts every layer':
        "张量并行切开的是每一层。流水线并行换个方向切模型：前八层放在一块GPU上，接下来八层放在另一块上，每块GPU是一个阶段。<bookmark mark='a'/>麻烦在于：第一个阶段处理一个批次时，其他阶段都在等。谷歌的GPipe在2019年把每个批次切成微批次，让各个阶段可以同时处理不同的微批次。<bookmark mark='b'/>这是GPipe的调度，精确模拟：{p}个阶段，{m}个微批次，反向传播花的时间是前向的两倍。时间从左往右走。<bookmark mark='c'/>微批次在前向时把流水线填满，流水线排空，然后反向传播再倒过来把它填满。灰色的角落是在等待的GPU：这就是流水线气泡。",

    'f"How big is the bubble?':
        "气泡有多大？每块GPU忙的时间，是m个微批次，每个一次前向一次反向。<bookmark mark='a'/>但整个调度要花更长：最后一个微批次要经过前面p减1个阶段，才能在最后一个阶段开始，回来的路上也一样。<bookmark mark='b'/>所以浪费的时间比例，是p减1，除以m加p减1。<bookmark mark='c'/>在我们的图里，是{100 * Pp['gpipe']['bubble']:.1f}%。这是气泡对微批次数的图，线是公式，点是我们模拟的调度。{fit}微批次越多，气泡越小；GPipe的作者发现，每个阶段四个就够了。",

    "f'The dots sit within {err:.4f} of the lines.'":
        "点和线的偏差在{err:.4f}以内。",

    '"GPipe has a second problem: memory.':
        "GPipe还有第二个问题：内存。每个阶段都要保存它前向跑过的每个微批次的激活，直到那个微批次回来。<bookmark mark='a'/>1F1B调度，来自微软的PipeDream工作，让每个微批次的反向传播尽早开始，一次前向和一次反向交替进行。<bookmark mark='b'/>{'The bubble is exactly the same: ' if same else 'The bubble: '}{100 * r1['bubble']:.1f}%。但第一块GPU同时保存的微批次，从不超过{int(r1['peak'][0])}个，也就是阶段数，而不是全部{m}个。内存不再随微批次数增长，所以你可以用很多微批次，气泡也就缩小了。",

    'f"Two more tricks cut the bubble itself.':
        "还有两个技巧，能削减气泡本身。<bookmark mark='a'/>交错：给每块GPU两段更小的层，而不是一段，这样一个微批次会经过每块GPU两次。爬坡的时间减半，气泡降到{100 * ri['bubble']:.1f}%。Llama 3用了这个办法。<bookmark mark='b'/>零气泡，来自2023年的Sea AI Lab：把反向传播一分为二。对输入的梯度是紧急的，因为前一个阶段正等着它；对权重的梯度不急，所以可以推迟，塞进空隙里。三者时间相等时，空闲时间降到1F1B的三分之一，气泡只有{100 * rz['bubble']:.1f}%，内存不变。<bookmark mark='c'/>DeepSeek-V3走得更远，用了DualPipe：微批次同时从流水线的两端进入，每块GPU把一个方向的计算，和另一个方向的通信重叠起来。在它的气泡公式里，p减1个阶段换成了p的一半减1个，代价是要保存两份权重。",

    # ------------------------------------------------------------------ Context
    'Chapter thirteen. Context, experts, and utilization.':
        '第13章。上下文、专家与利用率。',

    'f"Two more ways to cut.':
        "还有两种切法。第一种是为长序列准备的。激活随序列长度增长，到了一百万个词元，一个序列就放不进一块GPU了。那就把序列本身切开：上下文并行。<bookmark mark='a'/>每块GPU保存一段位置。Transformer里的一切都是逐位置的，只有注意力例外，它需要每一个键。<bookmark mark='b'/>环形注意力，来自2023年的伯克利：每块GPU保留自己的查询，键和值的各个块沿着环传递，每步一跳。<bookmark mark='c'/>每个到达的块，都用在线softmax并入结果，保持一个滚动的最大值和一个滚动的和，FlashAttention用的也是这个技巧，所以答案是精确的。<bookmark mark='d'/>我们在四个进程上跑了它，一个256个词元的序列，分成四块：结果和完整注意力吻合到{R['err']:.7f}。",

    'f"There\'s a catch with causal attention.':
        "因果注意力有个麻烦。一个位置只往回看，所以第一块查询只需要一块键，最后一块却需要全部。<bookmark mark='a'/>用连续的分块，最后一块GPU的工作量是第一块的{Pr['contiguous'][-1]}倍，大家都得等它。<bookmark mark='b'/>解决办法：把序列切成两倍那么多段，给第i块GPU第i段和第2p减1减i段，两头各一段。{even}Llama 3在它十二万八千词元的训练里正是这样做的，用了十六路上下文并行。",

    'f\'Now the busiest GPU does':
        "现在最忙的GPU，工作量是最闲的{max(zz) / min(zz):.2f}倍。",

    'The second cut is for mixtures of experts':
        "第二种切法是为混合专家准备的，来自第16部分。把不同的专家放在不同的GPU上。<bookmark mark='a'/>每个词元的路由器挑选它的专家，不管它们住在哪里，所以每一层都以一次全对全通信开始：每块GPU把自己的每个词元，发给持有它的专家的那些GPU，<bookmark mark='b'/>最后再来一次，把结果送回去。<bookmark mark='c'/>DeepSeek-V3把它的专家分布在八台机器的64块GPU上，并规定每个词元最多去四台机器，因为机器之间的网络比一台机器里的NVLink大约慢三倍。它甚至在每块GPU的132个处理器块里，留出二十个，专门用来搬运词元。",

    'A frontier run uses several cuts at once.':
        "一次前沿训练会同时用上好几种切法。这是Llama 3自己的表。<bookmark mark='a'/>在16384块GPU上，序列长八千个词元：八路张量并行，十六个流水线阶段，128个数据并行组。8乘16乘128是16384。<bookmark mark='b'/>到了十二万八千词元的阶段，十六路上下文并行从数据那个维度拿走了GPU。<bookmark mark='c'/>顺序很要紧。张量并行每一层都要通信，放在最内层，在一台机器里。上下文和流水线在其次。数据并行每一步才通信一次，而且可以等，它横跨整个集群。",

    'f"With all this machinery':
        "有了这么多机制，一次训练实际上用上了多少硬件？PaLM的论文在2022年定义了这个量：模型浮点利用率，也就是模型每秒需要的运算，即每个词元6N乘以每秒的词元数，除以硬件的峰值。重算和等待都不算。<bookmark mark='a'/>PaLM在6144块每秒275万亿次的TPU芯片上，每秒处理23.8万个词元：{100 * P['palm_mfu']:.1f}%，算上注意力是46.2%。<bookmark mark='b'/>字节跳动的MegaScale达到了55%；Llama 3是38%到43%；Olmo 3是43%。一个集群能做的算术，大约有一半损失在通信、气泡、内存访问和故障上。<bookmark mark='c'/>我们自己的训练，在这台计算机的一个核心上：分别是它峰值的{100 * b:.0f}%和{100 * f:.0f}%。",

    # ------------------------------------------------------------------ Precision
    'Chapter fourteen. Fewer bits.':
        '第14章。更少的位。',

    'f"Every number in a training run takes memory':
        "训练里的每个数都占内存和带宽，而越窄的数乘得越快：第17部分的张量核心，用8位做的工作是16位的两倍。那么，训练最少能用几位？<bookmark mark='a'/>这是各种格式，画在2的幂的刻度上，看每种在它的数变得太小或太大之前能走多远。<bookmark mark='b'/>FP32和bfloat16共用一个8位的指数，所以范围一样巨大；bfloat16只是保留的有效数字少一些。半精度FP16有5个指数位：低于大约6乘以10的负8次方就什么都没有了，在2的负14次方以下，还有一段更淡的、低精度的次正规数区域。<bookmark mark='c'/>现在看真正要紧的数：在我们模型的矩阵乘法里往回流的梯度，在第六十步测得。<bookmark mark='d'/>其中{100 * H['below_normal']:.0f}%低于FP16最小的正规数，{100 * H['below_sub']:.0f}%小到FP16会把它们舍入成零。",

    'The fix, from Micikevicius and colleagues':
        "解决办法来自2018年英伟达和百度的Micikevicius和同事，叫损失缩放。<bookmark mark='a'/>在反向传播之前，把损失乘以一个大数S。链式法则是线性的，所以每个梯度都放大成S倍。<bookmark mark='b'/>在2的幂的刻度上，对S等于2的16次方，整个分布向右滑动十六格，进入FP16的范围。<bookmark mark='c'/>然后在更新之前，把权重的梯度除以S，更新是用32位做的。<bookmark mark='d'/>S太大，最大的梯度会上溢，所以实践中S是动态的：一出现上溢就把它减半，并跳过这一步；连续一段好的步数之后，再把它加倍。BFloat16有和FP32一样的范围，这些都不需要，这就是它后来取而代之的原因。",

    '"Does it matter in practice?':
        "实际上要紧吗？我们把同一个小模型训练了六遍，每次矩阵乘法的输入，前向和反向，都舍入到某一种格式，求和则保持在FP32，这正是硬件的做法。每种两个种子。<bookmark mark='a'/>FP32，bfloat16，不带和带损失缩放的FP16，以及两种我们马上会讲到的8位训练。<bookmark mark='b'/>{verdict}",

    "f'All six end within {width:.3f} nats":
        "六种最后相差都在{width:.3f}奈特以内，在两个种子之间{spread:.3f}的差别之内。就连不带损失缩放的FP16，把{100 * zero:.1f}%的梯度值冲成了零，也训练得一样好。",

    "f'The worst, {worst_name}, ends":
        "最差的是{worst_name}，最后比FP32高{gap:.3f}奈特，超过了两个种子之间{spread:.3f}的差别；不带损失缩放的FP16，把{100 * zero:.1f}%的梯度值冲成了零。",

    "f'The six end up to {width:.3f} nats apart":
        "六种最后最多相差{width:.3f}奈特，但没有哪一种比FP32差出两个种子之间{spread:.3f}的差别，就连不带损失缩放的FP16也没有，尽管它把{100 * zero:.1f}%的梯度值冲成了零。",

    'f"Why, then, did loss scaling matter?':
        "那么，损失缩放为什么要紧？因为我们的梯度只是两千个词元上的平均。一次前沿训练，每一步的梯度是在几百万个词元上平均的，一块一块累积起来，每一块都小那么多。<bookmark mark='a'/>所以我们把FP16的训练重做了一遍，每一步切成{A['accum']}个微批次，就像梯度累积那样。<bookmark mark='b'/>{verdict}",

    "f'Now the gradients are {A['accum']} times smaller":
        "现在梯度在舍入时小了{A['accum']}倍，不带损失缩放的FP16把其中{100 * zero:.0f}%冲成了零：它最后落后FP32 {d_noscale:.2f}奈特。带损失缩放，和FP32只差{abs(d_scaled):.3f}。这正是损失缩放要防止的失败。",

    "f'Now FP16 without loss scaling flushes":
        "现在不带损失缩放的FP16，把{100 * zero:.0f}%的梯度冲成了零，最后落后FP32 {d_noscale:.2f}奈特；损失缩放挽回了一部分差距。",

    "f'Even now, with {100 * zero:.0f} percent":
        "即使现在，{100 * zero:.0f}%的梯度值被冲成了零，不带损失缩放的FP16最后也只和FP32差{d_noscale:.3f}奈特：我们的模型太小，没法清楚地显出这种失败。",

    'f"Eight bits is harder.':
        "8位就更难了。E4M3，带四个指数位的8位格式，只跨大约十八个2的幂，所以每个张量都需要一个缩放因子，把它的值挪进范围里。每个张量一个缩放因子，就像最早的FP8配方那样，是由最大的那个值决定的。<bookmark mark='a'/>而真实的激活里，总有几个很大的值。这是本系列模型里一次矩阵乘法的128个输入。<bookmark mark='b'/>整个张量用一个缩放因子，舍入到E4M3的误差是{100 * q['act_tensor']:.1f}%；每128个值的一个瓦片用一个缩放因子，误差是{100 * q['act_tile']:.1f}%。<bookmark mark='c'/>DeepSeek-V3就是这样训练它的6710亿个参数的：激活每128个值一个缩放因子，权重每128乘128的一块一个缩放因子。它还发现，张量核心在求和时只保留大约十四位，所以每128项就把部分和挪到FP32里，并把敏感的部分保留在更高的精度。它的损失和16位训练相比，差别在百分之零点二五以内。",

    'The newest chips put the scales into hardware.':
        "最新的芯片把缩放做进了硬件。英伟达的Blackwell能直接做微缩放格式的乘法，32个数一块，共享一个缩放因子；英伟达在2025年报告，一个八十亿参数的模型用MXFP8在十五万亿个词元上训练，和bfloat16持平。<bookmark mark='a'/>然后是4位：NVFP4把十六个4位的值和一个8位的缩放因子打包在一起。<bookmark mark='b'/>英伟达用它预训练了一个一百二十亿参数的模型，用了十万亿个词元，用随机旋转把离群值摊开，对梯度用随机舍入，并把百分之十六的层留在bfloat16里；它在MMLU-Pro上的分数，和FP8模型相差不到二十分之一分。<bookmark mark='c'/>2026年3月，Nemotron 3 Super用NVFP4在25万亿个词元上完成了预训练；Kimi K3发布的是4位权重，DeepSeek-V4是4位的专家，两者都来自量化感知训练。<bookmark mark='d'/>每一次把位数减半，都伴随着一种新的缩放方式。",

    # ------------------------------------------------------------------ Stability
    'Chapter fifteen. Keeping the run stable.':
        '第15章。让训练保持稳定。',

    'Large runs have a failure that small ones rarely show':
        "大规模训练有一种小规模训练很少出现的失败：损失突然跳起来，有时再也回不去。<bookmark mark='a'/>谷歌5400亿参数的PaLM，尽管梯度被裁剪过，还是出现了大约二十次尖峰。<bookmark mark='b'/>团队的解决办法很粗暴：回到尖峰之前大约一百步的检查点，跳过接下来的两百到五百个批次。<bookmark mark='c'/>问题不在坏数据：同样的批次，从训练的另一个时刻开始就不会出问题。尖峰来自数据和模型状态的组合，而2022年到2026年的模型，都经过了重新设计，好让这种状态保持温顺。",

    'f"One state that goes wrong is attention itself.':
        "会出问题的一种状态，就是注意力本身。一个查询和一个键给出一个logit，也就是它们的点积除以维度的平方根，没有什么能阻止权重一直增长，直到logit变得巨大。<bookmark mark='a'/>那时softmax把全部权重都压在一个位置上，它的梯度消失，训练会卡死或者爆掉。谷歌的Wortsman和同事在2023年，只是把学习率调高，就在小模型里重现了这一点。我们也重现了。<bookmark mark='b'/>学习率为{lr:g}时，我们普通模型最大的注意力logit达到了{pl:,.0f}。<bookmark mark='c'/>ViT-22B、Olmo 2、Qwen3和GLM-4.5用的解决办法：QK归一化。在点积之前，把每个查询和键都归一化，<bookmark mark='d'/>这样logit的上界，就是归一化学到的增益乘以维度的平方根。有了它，我们最大的logit停在{qk:.0f}。",

    'f"Wortsman\'s test of a fix is a sweep':
        "Wortsman检验一个解决办法的方法是扫描：在许多学习率上训练，看损失在多高的学习率上还能保持良好。这是我们的：{len(lrs)}个学习率，普通的，带QK归一化的，以及带QK归一化和我们接下来要讲的z-loss的，每种两个种子。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{best}",

    "f'The best learning rate is {lrs[best_plain]:g}":
        "最好的学习率，不带QK归一化是{lrs[best_plain]:g}，带它是{lrs[best_qk]:g}。",

    "f'Both do best at a learning rate":
        "两者都在学习率为{lrs[best_qk]:g}时最好。",

    "f'At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the one with QK-norm at {qk:.2f}, a gap larger than the {sp:.2f} between seeds: normalizing":
        "在最高的学习率{lrs[hi_lr]:g}上，普通模型最后是{pl:.2f}奈特，带QK归一化的是{qk:.2f}，差距大于两个种子之间的{sp:.2f}：把查询和键归一化，拓宽了能训练好的学习率范围。",

    "f'At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the one with QK-norm at {qk:.2f}, a gap larger than the {sp:.2f} between seeds: in runs":
        "在最高的学习率{lrs[hi_lr]:g}上，普通模型最后是{pl:.2f}奈特，带QK归一化的是{qk:.2f}，差距大于两个种子之间的{sp:.2f}：在这么短的训练里，QK归一化反而有一点代价。",

    'f"At the highest learning rate, {lrs[hi_lr]:g}, the plain model ends at {pl:.2f} nats and the one with QK-norm at {qk:.2f}, but':
        "在最高的学习率{lrs[hi_lr]:g}上，普通模型最后是{pl:.2f}奈特，带QK归一化的是{qk:.2f}，但同一种设计的两个种子，就能相差{sp:.2f}：在这么短的训练里，损失分不出它们的高下，尽管普通模型最大的注意力logit大了{ratio:.0f}倍。",

    'f"The second fix is for the output layer.':
        "第二个解决办法针对输出层。所有logit都平移同样的量，softmax不会改变。<bookmark mark='a'/>所以它们的log-sum-exp，也就是log Z，可以自由漂移，而在16位算术里，大的logit会丢掉精度。<bookmark mark='b'/>PaLM加了一个很小的惩罚，10的负4次方乘以log Z的平方：这就是z-loss。<bookmark mark='c'/>它的梯度把所有logit一起往归一化常数为1的方向轻轻推，而不改变模型预测的东西。<bookmark mark='d'/>在我们的训练里，log Z最后不带它是{a:.1f}，带它是{b:.2f}。",

    'The newest source of trouble is the optimizer.':
        "最新的麻烦来源是优化器。第11部分的Muon，会把每次更新正交化，它在2025年走向了大规模：Moonshot的Moonlight研究发现，它的计算效率大约是AdamW的两倍。<bookmark mark='a'/>但用了Muon，注意力logit长得更快，而Kimi K2用的是潜在注意力，它的键从不完整地构造出来，所以没法用QK归一化。<bookmark mark='b'/>Moonshot的解决办法是QK-Clip：每次更新之后，如果某个头最大的logit超过了一百，就缩小这个头的查询和键的权重，把它拉回来。一开始它裁剪了12.7%的头；七万步之后，一个也没有；K2在15.5万亿个词元上训练，一次损失尖峰也没出现。<bookmark mark='c'/>2026年的DeepSeek-V4也用Muon，它的新注意力直接对查询和键做归一化。它剩下的尖峰来自混合专家里的离群值，它的压制办法是：在尖峰持续期间，用稍旧一些的权重来做路由，并对SwiGLU的激活做截断。",

    # ------------------------------------------------------------------ MTP
    'Chapter sixteen. Predicting two tokens ahead.':
        '第16章。往后预测两个词元。',

    'Next-token prediction asks for one token at a time':
        "下一个词元的预测，一次只要一个词元，这让模型靠局部的模式就能应付过去。如果它必须看得更远呢？<bookmark mark='a'/>2024年，Meta的Fabian Gloeckle和同事，给一个模型在共享的主干上装了几个输出头，分别预测下一个词元、再下一个，依此类推。<bookmark mark='b'/>在代码上，一个一百三十亿参数的模型，在HumanEval上多解出了12%的题，在MBPP上多了17%。<bookmark mark='c'/>收益随规模增长；在他们最小的模型上，多出来的头反而有害。<bookmark mark='d'/>这些头还兼作推断时提前猜测的快速办法，最多快三倍。",

    'DeepSeek-V3 made the extra prediction sequential.':
        "DeepSeek-V3把额外的预测改成了顺序的。主模型照常预测下一个词元。<bookmark mark='a'/>然后一个小模块，拿主模型在位置i上的最后一个隐藏状态，和真实的下一个词元的嵌入，<bookmark mark='b'/>把两者归一化，拼接起来，再过一个Transformer块，用同一个输出头预测下下个词元。<bookmark mark='c'/>它的损失以0.3的权重加进来，用于前十万亿个词元，之后是0.1。<bookmark mark='d'/>推断时，这个模块可以丢掉，也可以用来提前猜第二个词元，再由主模型核对这个猜测。DeepSeek报告，这个猜测有85%到90%的时候被接受；于是每一步大约产出1.85到1.9个词元，他们测得速度是原来的1.8倍。",

    '"We added DeepSeek-V3\'s module':
        "我们把DeepSeek-V3的模块加到我们的小模型上，在同样的词元上训练，每种两个种子，权重在接近结尾时从0.3降到0.1。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>这个模块让每一步多花大约{100 * MC['extra_share']:.0f}%的算术，{mostly}。",

    "f'With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against {ntp:.3f} without: predicting":
        "有了这个模块，下一个词元的留出损失最后是{mtp:.3f}奈特，没有它是{ntp:.3f}：往更远处预测有帮助，即使在我们的规模上。",

    "f'With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against {ntp:.3f} without: at our":
        "有了这个模块，下一个词元的留出损失最后是{mtp:.3f}奈特，没有它是{ntp:.3f}：在我们的规模上，这个额外的任务要付出一点代价，正如Gloeckle在他们最小的模型上发现的那样。",

    "f'With the module, the held-out loss for the next token ends at {mtp:.3f} nats, against {ntp:.3f} without, inside":
        "有了这个模块，下一个词元的留出损失最后是{mtp:.3f}奈特，没有它是{ntp:.3f}，在种子之间的差别以内：在我们的规模上，这个额外的任务既无帮助，也无害处。",

    '"And as a drafter?':
        "那么当草稿模型呢？我们让主模型从留出的开头贪心地往下写，同时让它的模块猜每一个下下个词元。<bookmark mark='a'/>{how}<bookmark mark='b'/>这样主模型的每一步，就能产出{1 + a:.2f}个词元，而不是一个。第19部分会好好搭建推测解码。",

    'mostly the second pass through the output head':
        '主要是第二次经过输出头，在这么小的模型里，输出头占的分量很大',

    'f"The guess was right {100 * a:.0f} percent of the time, against':
        "猜测有{100 * a:.0f}%的时候是对的，而DeepSeek-V3是85%到90%：小模型往后两个词元的猜测，更难猜对。",

    'f"The guess was right {100 * a:.0f} percent of the time, close':
        "猜测有{100 * a:.0f}%的时候是对的，接近DeepSeek-V3的85%到90%。",

    # ------------------------------------------------------------------ Faults
    'Chapter seventeen. When hardware fails.':
        '第17章。当硬件出故障。',

    'f"Back to Llama 3\'s run.':
        "回到Llama 3的训练。五十四天里，它的任务被中断了{L['interruptions']}次，其中{L['unexpected']}次是计划外的。<bookmark mark='a'/>这是Meta报告的原因。最大的一类遥遥领先：坏掉的GPU；然后是GPU上出故障的内存芯片，再然后是软件缺陷、网络交换机和线缆，以及主机维护。<bookmark mark='b'/>也就是每{P['llama_mtbf_h']:.1f}小时一次中断。可每块GPU单独来看，大约{P['llama_gpu_mtbf_years']:.1f}年才坏一次：问题不在零件，而在于它们有一万六千个，任何一个都会让整个任务停下来。<bookmark mark='c'/>多亏了自动化，只有三次故障需要人来处理，这次训练有超过百分之九十的时间都在训练。<bookmark mark='d'/>就连天气都看得出来，在吞吐量上，也在用电量上。",

    'f"So a run saves a checkpoint':
        "所以，一次训练会定期为每块GPU的状态保存一个检查点，出故障后就从最近的一个重新开始。多久保存一次？每tau秒保存一次，每次花费delta，浪费的是训练时间的tau分之delta。<bookmark mark='a'/>而故障平均每M秒来一次，会扔掉自上次保存以来的工作：平均半个间隔，所以还要再加上2M分之tau。<bookmark mark='b'/>令导数为零。<bookmark mark='c'/>最好的间隔，是2倍delta乘M的平方根：这是约翰·杨在1974年给出的法则。<bookmark mark='d'/>对Llama 3：检查点每块GPU最多四吉字节，存储每秒能写两太字节，所以一次完整的保存大约要{P['llama_ckpt_s']:.0f}秒；每{P['llama_mtbf_h']:.1f}小时一次故障，大约每{P['llama_young_s'] / 60:.0f}分钟保存一次。",

    'f"We simulated it:':
        "我们做了模拟：{Fa['H'] / 86400:.0f}天的训练，故障随机到来，平均每{Fa['M'] / 3600:.1f}小时一次，保存要{Fa['delta']:.0f}秒，重启要十分钟，这只是举例；对每一种检查点间隔，都模拟很多遍。<bookmark mark='a'/>保存得太勤，保存本身就会吃掉训练。太少，每次故障都会扔掉几个小时。<bookmark mark='b'/>模拟里最好的间隔是{Fa['best_tau'] / 60:.0f}分钟；杨的法则说是{Fa['young'] / 60:.0f}分钟。<bookmark mark='c'/>即便如此，还是有{100 * lost:.0f}%的时间损失掉了：光是重启就占{100 * restart_share:.0f}%，其余的花在保存和重做的工作上。这就是为什么前沿实验室要让重启变快，让检查点异步写出；也是为什么DeepSeek-V4的内核是确定性的：一次能够精确重放的训练，才能被调试。",

    # ------------------------------------------------------------------ Recipe
    'Chapter eighteen. Our own full recipe.':
        '第18章。我们自己的完整配方。',

    '"Now we put the pieces together.':
        "现在把各个部分拼起来。两个形状完全相同的模型，用三十部小说里同样的三百万个词元训练，顺序相同，步数相同，从同样的初始权重出发；然后换第二个种子，把整个比较再做一遍。<bookmark mark='a'/>一个用2020年的配方：AdamW，余弦调度，普通的注意力。<bookmark mark='b'/>另一个用2026年的配方：隐藏层的矩阵用Muon，预热、稳定、衰减，QK归一化和z-loss。<bookmark mark='c'/>{out_}",

    "f'Two-token prediction stays out although":
        "两词元预测没有放进来，尽管它在第16章有一点帮助：它多花{100 * MC['extra_share']:.0f}%的算术，而比较必须在同等算力下进行。8位算术也没有放进来：在CPU上，它只是模拟了那份节省。",

    'Two-token prediction stays out: it gave no gain':
        '两词元预测没有放进来：在第16章，它在我们的规模上没有带来收益，而且要额外的算力，会让比较不公平。8位算术也没有放进来：在CPU上，它只是模拟了那份节省。',

    'f"Watch them learn.':
        "看它们学习。左边是每个模型在它从没训练过的文本上的损失；右边是每个模型在“The door opened, and”这几个词之后写出的东西，在同样的步数冻结，用同样的随机种子。<bookmark mark='a'/>一开始，两个都写出噪声，损失大约是{first['val']:.1f}奈特。<bookmark mark='b'/>让它们读吧。<bookmark mark='c'/>到最后，比一比它们写出的东西；曲线告诉我们，哪一个学得更快。",

    '"The scores.':
        "成绩。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{stab}",

    'f"And the 2026 recipe\'s attention stayed tamer':
        "而且2026配方的注意力更温顺：它最大的logit是{fl_:.0f}，对方是{bl_:.0f}。",

    'f"Its largest attention logit was':
        "它最大的注意力logit是{fl_:.0f}，对方是{bl_:.0f}：在这个学习率上，两个模型的注意力都没有失控。",

    'f"The 2026 recipe wins:':
        "2026年的配方胜出：在记分牌那段文字上，每字符{mf:.3f}比特，对{mb:.3f}，都是两个种子的平均：模型、数据和步数完全相同，它好了{100 * rel:.1f}%，超过了两个种子之间的{sp:.3f}。",

    'f"The 2020 recipe wins here:':
        "这里是2020年的配方胜出：每字符{mb:.3f}比特，2026年的配方是{mf:.3f}，都是两个种子的平均。在我们的规模上，两者又用同一个没调过的学习率，新配方的优势显不出来。",

    "f'They tie:":
        "两者打平：每字符分别是{mb:.3f}和{mf:.3f}比特，都是两个种子的平均，差别小于两个种子之间的{sp:.3f}。在我们的规模上，新配方既无帮助，也无害处。",

    'f"And on the series\' scoreboard':
        "再看本系列的记分牌，也就是每个模型对《马耳他之鹰》第二章需要的每字符比特数。<bookmark mark='a'/>最上面是第1部分的压缩器和计数，然后是第14部分的家族，还有本系列自己的那个{base_row['params'] / 1000000.0:.1f}百万参数的模型，用了我们{times:.0f}倍的词元训练，成绩是{base_row['bits']:.2f}。<bookmark mark='b'/>{vs14}<bookmark mark='c'/>配方买到的是效率：用更少的算力得到同样的质量。前沿实验室把省下来的，花在了规模上。",

    'f"Our 2026 model scores {f[\'bits\']:.2f}, better than':
        "我们的2026模型得分{f['bits']:.2f}，好于第14部分同样大小、读了同样多词元的模型，它是{gm['bits']:.2f}。",

    'f"Our 2026 model scores {f[\'bits\']:.2f}, against':
        "我们的2026模型得分{f['bits']:.2f}，第14部分同样大小、读了同样多词元的模型是{gm['bits']:.2f}。",

    # ------------------------------------------------------------------ Outro
    '"Let\'s take stock.':
        "我们来总结一下。一个预训练语料库，从对网络的一次抓取开始，其中大部分都被扔掉：按网址，按语言，按质量。MinHash和局部敏感哈希不用两两比较，就能找出近似重复，{scurve}。一个小分类器，用大模型打的分来训练，决定哪些网页有教学价值。配比是为一个目标挑选的，合成数据只有和真实文本放在一起才有帮助。然后是算术：每个参数、每个词元六次运算，每个参数十六个字节，再加上激活。数据并行需要全规约，而环是最优的；ZeRO把多余的副本分片掉；张量、流水线、上下文和专家并行切开其余的部分。更少的位需要缩放的技巧，大规模训练需要QK归一化和z-loss，一万六千块GPU需要检查点。而我们自己的模型，用完整的配方训练，在记分牌上占了一席之地。",

    'their measured S-curve followed the prediction only roughly':
        '实测的S形曲线只是大致跟着预测走',

    'All of this comes back.':
        "这些都会再出现。为训练好的模型提供服务，连同它的缓存、草稿和4位权重，是第19部分。同样的数据流水线，在第22和第23部分为图像、视频和声音供料。后训练从一个预训练好的模型开始，在第27部分；强化学习在它上面构建推理能力，在第28部分。第30部分把一个预训练模型打开来看，第31部分问，它的评测到底有多可信。",

    'Here are six problems to try':
        '这里有六道习题，从MinHash的概率，一直到杨的检查点间隔。请在这里暂停，动手做一做；完整的解答在本部分的笔记里。',

    'Next time: inference.':
        "下一次：推断。一个训练好的模型要回答问题，面对几百万人，又要快又要便宜。读提示是算术；一次一个词元地写答案，是搬运内存。像DeepSeek-V3的第二词元猜测那样的草稿，让一次前向就能检查好几个词元；4位权重让每个词元都更便宜。这就是第19部分。",

    "Most of this part's methods are written up openly":
        "本部分的大多数方法，都公开写在使用它们的那些实验室的技术报告里，非常值得一读。感谢观看，第19部分再见。",
}

ZH = dict(_DATA)

PHRASES = {
    # ZeRO: the measured traffic against the paper's 1.5
    "ZeRO's one and a half, measured.": 'ZeRO的一倍半，实测出来了。',
    "ZeRO's paper predicts one and a half.": 'ZeRO的论文预测的是一倍半。',
    # Context: the zigzag split's balance
    'Now every GPU does the same work.': '现在每块GPU的工作量都一样了。',
    # Mixture: model collapse, as measured
    'The damage stays much smaller.': '损害要小得多。',
    'Here it only slows the damage.': '在这里，它只是让损害来得慢一些。',
    # Quality: the scoreboard passage's contamination check
    'Clean.': '是干净的。',
    # MTP: where the module's arithmetic goes
    'mostly its own transformer block': '主要花在它自己的Transformer块上',
    # Outro: the S-curve, as measured
    'their S-curve came out as predicted': '它们的S形曲线和预测的一样',
    # Mixture: which way RegMix's pick leans
    'leans toward the American novels': '偏向美国小说',
    'moves away from the American novels': '远离美国小说',
    'stays close to the natural mixture': '和自然配比相差不大',
    # Pipeline
    'Every dot sits exactly on its line.': '每个点都正好落在它的线上。',
    'The bubble is exactly the same: ': '气泡和GPipe完全一样：',
    'The bubble is exactly the same:': '气泡和GPipe完全一样：',
    'The bubble: ': '气泡：',
    'The bubble:': '气泡：',
    # Precision: the formats as spoken (common.PREC_SPOKEN)
    'FP32': 'FP32',
    'bfloat16': 'bfloat16',
    'FP16 without loss scaling': '不带损失缩放的FP16',
    'FP16 with loss scaling': '带损失缩放的FP16',
    'FP8 with one scale per tensor': '每个张量一个缩放因子的FP8',
    'FP8 with one scale per tile': '每个瓦片一个缩放因子的FP8',
}
