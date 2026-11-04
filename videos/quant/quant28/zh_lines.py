"""Chinese narration for quant28: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 词袋 (bag of words), 文档-词项矩阵 (document-term matrix),
齐普夫定律 (Zipf's law), 希普斯定律 (Heaps' law), 词典 (dictionary), 净语气 (net tone), 前瞻指引 (forward guidance),
迷雾指数 (fog index), 筛选 (screening), 主题模型 (topic model), 非负矩阵分解 (NMF), 词嵌入 (embedding), 点互信息 (PMI),
注意力 (attention), 词元 (token), 字节对编码 (BPE), 每字符比特 (bits per character), 前视偏差 (look-ahead bias),
分心效应 (distraction effect), 时间一致的模型 (chronologically consistent model), 智能体 (agent), 另类数据 (alternative
data), 领域模型 (domain model), 切比雪夫关联不等式 (Chebyshev's association inequality), 确定筛选 (sure screening)."""

TITLE = '量化金融，从零搭建 · 第28部分：文本、大语言模型与另类数据'

CHAPTERS = {
    'Hook': '一句话',
    'Words': '1. 把文字变成数字',
    'Dictionaries': '2. 词典：Tetlock与Loughran–McDonald',
    'Tone': '3. 语气与两年期收益率',
    'Form': '4. 长度、可读性与前瞻指引',
    'SESTM': '5. 有监督的词：SESTM',
    'Topics': '6. 主题，以及作为宏观数据的新闻',
    'FOMC': '7. FOMC内部：透明度与审议',
    'Embeddings': '8. 词嵌入：从近邻中得到含义',
    'Transformers': '9. Transformer与FinBERT',
    'LLMs': '10. 大语言模型读新闻',
    'LookAhead': '11. 前视偏差',
    'TimeSlice': '12. 按时间切片的实验',
    'Agents': '13. 大语言模型交易智能体',
    'AltData': '14. 另类数据',
    'Domain': '15. 领域模型与文本交易台',
    'Envelope': '16. 文本信号，登记并打开',
    'House': '17. 第28条规则：文本特征',
    'Research': '写给研究者：筛选为什么能找到那些词',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part twenty-eight. Text, language models and alternative data:":
        "第28部分。文本、语言模型与另类数据：如何把文字以及其他不是价格的东西变成模型能用的数字；它们值多少钱；以及它们多么容易骗过你。",

    'f"On the {_date(h[\'date\'])}, eight days before a scheduled meeting':
        "{_date(h['date'])}，在一次例会前八天，联邦公开市场委员会发布了一份临时声明。<bookmark mark='a'/>这就是它，逐词对比上一份声明：红色是删去的，"
        "绿色是新加的。<bookmark mark='b'/>降息四分之三个百分点，而不是四分之一。经济前景走弱。增长面临的下行风险上升。住房市场的收缩在加深。",

    'f"The bond market answered within minutes.':
        "债券市场在几分钟内就作出了回答。<bookmark mark='a'/>到收盘时，两年期国债收益率下跌了{abs(h['dy']):.0f}个基点，是1997到2020年间所有声明日中最大的波动。"
        "<bookmark mark='b'/>在典型的声明日，它大约波动{h['sd']:.0f}个基点。其他大波动的日子都集中在同一场危机里。在已知的那一分钟发布的文字，推动着世界上最大的市场之一："
        "机器能读得同样快、同样好吗？",

    "The tools are older than you might think.":
        "这些工具比你想的要古老。1960年代心理学家的词典；2007年Paul Tetlock的媒体悲观情绪；2011年Loughran和McDonald的金融词典。<bookmark mark='a'/>"
        "然后是神经网络的转向：2013年的词向量，2017年的transformer，2018年的BERT，同一年一个主题模型也打开了FOMC的会议记录；2019年的SESTM。<bookmark mark='b'/>"
        "而自2023年以来是大语言模型：FinBERT、BloombergGPT、读新闻标题的ChatGPT、会交易的智能体，以及第一批被构建得无法读到未来的模型。",

    "The plan: words as numbers, dictionaries and why they misread":
        "计划是：把文字变成数字，词典以及它们为什么会误读；债券市场的反应；前瞻指引；有监督的词、主题和词嵌入，全部用在美联储自己三十年的文件上；transformer，"
        "以及我们自己的一个小语言模型；大语言模型能用新闻做什么，以及它们如何作弊；智能体与另类数据；还有那条说明一份词表需要多少文档的定理。",

    "In the House, the research desk gets a reading room":
        "在本系列公司里，研究交易台有了一间阅览室：把文件变成特征的工具，每个特征都标上其文字公开的那一刻，以及这样的特征必须经受住什么的规则。",

    # ------------------------------------------------------------------ Words
    "Chapter one. Before any model can read":
        "第一章。在任何模型能阅读之前，文字必须变成数字。一份声明如何变成矩阵的一行？",

    "Take one sentence from a statement.":
        "从一份声明中取出一句话。<bookmark mark='a'/>把它拆成词，转成小写，去掉数字和标点。<bookmark mark='b'/>然后计数。顺序被丢掉了：这就是词袋，"
        "三十年来金融领域的大多数文本分析都从这里开始，也在这里结束。它丢掉了语法、否定和上下文，却保留了一样出奇有用的东西：选了哪些词，用了多少次。",

    'f"Do that for every document and stack the counts.':
        "对每一份文档都这样做，并把计数堆叠起来。<bookmark mark='a'/>文档-词项矩阵：每份文档一行，每个词一列，每个元素是一个计数。<bookmark mark='b'/>"
        "我们的语料是联邦公开市场委员会自1997年以来发布的每一份声明，到2020年为止共{c['n_statements']}份，以及自{c['first_minutes'] // 10000}年以来的每一份纪要，"
        "又有{c['n_minutes']}份：总共约{mw:.0f}百万词，其中{c['n_types']:,}个不同的词。<bookmark mark='c'/>几乎每个元素都是零。文本是第二十五和二十七部分反复遇到的问题的极端情形："
        "列数远远多于任何人能逐一估计的数量。",

    'f"Sort the words by how often they appear':
        "按出现频率把词排序，在两条对数坐标轴上画出频率对排名。<bookmark mark='a'/>一条直线，斜率接近负一：齐普夫定律，几乎在所测量过的每一种语言和语料中都成立。"
        "这里的斜率是{c['zipf_slope']:.2f}。<bookmark mark='b'/>头部是少数几个功能词，the、of和to，几乎不携带含义；尾部是数以万计只用过一两次的词。"
        "所有有趣的东西都在中间，而每一种方法都是用不同的方式决定中间的哪些词重要。",

    'f"The vocabulary never stops growing.':
        "词汇量永远不会停止增长。<bookmark mark='a'/>逐年统计纪要用过的不同的词：第一年{int(gr[0]):,}个，到2020年{int(gr[-1]):,}个。这就是希普斯定律，"
        "齐普夫定律的伙伴：新的文档不断带来新的词，越来越慢，但永无止境。<bookmark mark='b'/>仅2008到2010年，委员会就写下了{new08:,}个它以前从未用过的词。"
        "一个冻结在2007年的模型从未见过它们：记住这一点，第十二章会用到。",

    "The simplest reweighting is called t f i d f.":
        "最简单的重新加权叫作tf-idf。<bookmark mark='a'/>把计数变成占比，这样长文档就不会占主导。<bookmark mark='b'/>然后按每个词在文档间有多稀少来加权："
        "一个到处都出现的词，比如committee，几乎得不到权重；一个只在少数文档中出现的词，比如pandemic，得到很多。<bookmark mark='c'/>把每一行缩放到单位长度，"
        "两份声明的相似度就是一个点积。搜索引擎靠这个运行了几十年。",

    "Pause and predict. A word appears in every FOMC statement and nowhere else.":
        "暂停预测一下。一个词出现在每一份FOMC声明里，而其他地方都没有。它在声明中的权重是多少，它没用吗？",

    # ------------------------------------------------------------------ Dictionaries
    "Chapter two. The oldest way to read text at scale":
        "第二章。大规模阅读文本最古老的方法：一份算作好消息的词表，一份算作坏消息的词表。哪些词，由谁决定？",

    "In 2007 Paul Tetlock took one newspaper column":
        "2007年，Paul Tetlock取了一个报纸专栏，《华尔街日报》每日的Abreast of the Market，从1984到1999年，按1960年代心理学家编制的哈佛General Inquirer"
        "词典的类别统计它的词。<bookmark mark='a'/>得到了一个悲观因子。它高的时候，道琼斯指数第二天下跌，然后在一周内回升。<bookmark mark='b'/>"
        "暂时的推动和随后的反转，正是噪声交易者的情绪应有的表现，而不是关于基本面的新闻；无论哪个方向的极端悲观都预示着成交量放大。事实证明，媒体的文字会推动价格，即使只是一时。",

    'f"Four years later, Tim Loughran and Bill McDonald':
        "四年后，Tim Loughran和Bill McDonald指出了心理学家的词典读公司年报时会出什么错。<bookmark mark='a'/>在哈佛词表看来，tax、cost、capital、board、"
        "liability、foreign和vice都是负面词。在10-K里它们只是业务本身：董事会、副总裁、资本支出。<bookmark mark='b'/>在五万份年报中，哈佛词表的负面计数近四分之三"
        "来自这样的词。<bookmark mark='c'/>于是他们从申报文件本身构建了自己的词表：felony、litigation、restated、impairment。他们的词典如今是金融领域的默认选择，"
        "一直在更新，有{t['n_lm']['negative']:,}个负面词、{t['n_lm']['positive']}个正面词和{t['n_lm']['uncertainty']}个不确定词。",

    "Run the dictionary over every FOMC statement.":
        "用这部词典扫过每一份FOMC声明。<bookmark mark='a'/>负面词占比在2001、2008和2020年的衰退中跳升，正如你所期望的。<bookmark mark='b'/>正面词占比在漂移，"
        "不确定词占比则停在一个稳定的底部附近，这是委员会无论形势如何都要说它预期什么、看到哪些风险的习惯所决定的。",

    'f"But look at which words do the counting.':
        "但是看看是哪些词在计数。<bookmark mark='a'/>声明中被计数最多的负面词是{w0}，被计数最多的正面词是{p0}。<bookmark mark='b'/>在央行的声明里，这些根本不是新闻："
        "它们是其双重职责的两半，最大就业和物价稳定，几乎每一段都会提到。金融词典误读央行的方式，正如心理学家的词典误读年报。每一部词典都是为一种文体拟合的，而这一部是为申报文件拟合的。",

    "Pause and predict. The Committee will not hesitate to act if the outlook weakens.":
        "暂停预测一下。委员会将毫不犹豫地采取行动，如果前景走弱的话。词典会数出几个负面词，这句话是鹰派还是鸽派？",

    # ------------------------------------------------------------------ Tone
    "Chapter three. A dictionary can score every statement.":
        "第三章。词典可以给每份声明打分。这个分数能告诉我们债券市场会如何反应吗？",

    'f"The market\'s verdict on a statement is fast.':
        "市场对一份声明的裁决来得很快。<bookmark mark='a'/>把它度量为两年期国债收益率从声明前一天收盘到声明当天收盘的变化。两年期是对美联储接下来几次会议的行动最敏感的期限。"
        "<bookmark mark='b'/>然后问最简单的问题：把这个变化对词典的净语气做回归。<bookmark mark='c'/>在典型的声明日，两年期收益率波动约{h['sd']:.0f}个基点；少数日子达到几十个基点。",

    'f"In the House, tone is a few lines.':
        "在本系列公司里，语气只是几行代码。<bookmark mark='a'/>把每个词转成大写，在每份词表里查找，再除以总词数。在开篇那份2008年1月22日的声明上运行："
        "它的词有百分之{100 * t['neg'][k]:.1f}是负面的，百分之{100 * t['pos'][k]:.1f}是正面的，百分之{100 * t['unc'][k]:.1f}是不确定的。",

    'f"Here are all {r[\'n\']} statements through 2020.':
        "这里是到2020年为止的全部{r['n']}份声明。<bookmark mark='a'/>每个点是一份声明：横轴是它的净语气，纵轴是两年期收益率的变动。<bookmark mark='b'/>拟合线是平的。"
        "t统计量是{r['t']:.2f}，语气解释了百分之{100 * r['r2']:.1f}的波动。相对上一份声明的语气变化、单独的负面占比、不确定占比：t统计量分别是{t_d:.2f}、{t_n:.2f}和{t_u:.2f}。"
        "无论是什么在声明日推动两年期收益率，词典都看不到它。",

    "That is not because words do not matter.":
        "这并不是因为文字不重要。<bookmark mark='a'/>Kenneth Kuttner在2001年表明，收益率对利率决定中以联邦基金期货衡量的意外部分有反应，而对大家都预期到的部分几乎没有反应。"
        "<bookmark mark='b'/>随后Refet Gürkaynak、Brian Sack和Eric Swanson发现，FOMC日需要第二个因子：关于未来政策路径的消息，它主要来自声明，而且对较长期的收益率比决定本身更重要。"
        "<bookmark mark='c'/>所以文字确实会推动市场，途径是它们相对于预期对未来政策意味着什么。一份好词坏词的清单，既看不到路径，也看不到预期。我们需要一种从市场反应本身学习哪些词重要的方法。",

    "Pause and predict. The market expected a quarter-point cut":
        "暂停预测一下。市场预期降息四分之一个百分点，结果也是如此，但声明暗示还会再降。两年期收益率会往哪个方向走，净语气会知道吗？",

    # ------------------------------------------------------------------ Form
    "Chapter four. Before asking what the statements say":
        "第四章。在问声明说了什么之前，先看看它们怎么说：有多长，有多难读，以及用来谈论未来的那些用语。",

    'f"Here is every statement, as a bar of its length in words.':
        "这里是每一份声明，每根柱子是它的词数。<bookmark mark='a'/>在1990年代后期，一份声明就是一段话：2002年以前的中位数是{f['first5']:.0f}个词。<bookmark mark='b'/>"
        "危机改变了这一点。当委员会把利率降到零并开始购买债券时，它必须解释那些无法用一个数字概括的工具，并说明接下来会做什么。2016年以来中位数是{f['last5']:.0f}个词。"
        "声明本身变成了政策工具。",

    'f"And how hard are they to read?':
        "它们有多难读？<bookmark mark='a'/>迷雾指数来自1952年，把平均句长和长词占比加起来：大致是读者需要受教育的年数。<bookmark mark='b'/>2002年以前，声明的中位数得分约为"
        "{f['fog_first']:.0f}；2016年以来约为{f['fog_last']:.0f}：两次都是研究生水平的文字。长度增长得比难度快得多。<bookmark mark='c'/>Loughran和McDonald后来指出，"
        "迷雾指数会误判金融文件，因为其中的长词对目标读者来说并不难，并提出了像文件大小这样直白的度量。可读性不等于信息。",

    'f"There is a simpler measure than any dictionary:':
        "有一个比任何词典都简单的度量：这份声明改了多少？<bookmark mark='a'/>把每份声明的加权词频与上一份比较，取一减去它们的余弦相似度。声明的中位数改动是{ch['median_change']:.2f}："
        "每份声明的大部分都抄自上一份。<bookmark mark='b'/>改得越多，两年期收益率动得越多。秩相关是{ch['rho']:.2f}；改动最多的四分之一声明平均使收益率变动{ch['abs_high']:.1f}个基点，"
        "改动最少的四分之一为{ch['abs_low']:.1f}个基点。它不说明方向，而且大幅改写往往伴随政策行动，所以这只是相关。但交易员读声明的方式正如开篇那样：看它和上一份的差别。",

    "The words that carry the most weight are the ones about the future.":
        "分量最重的词是关于未来的词。<bookmark mark='a'/>每一行是一个用语；每个刻度是一份用了它的声明。likely to be measured，来自2004年的紧缩，承诺每次四分之一个百分点；"
        "considerable period、extended period和exceptionally low levels承诺的则相反。<bookmark mark='b'/>patient、some time、gradual：每个用语都活上几年，而它的删除本身就是新闻。"
        "<bookmark mark='c'/>transitory，委员会对2021年通胀的说法，在当年12月被删去，到次年3月ongoing increases取而代之。词典不可能知道这些：这些用语的含义是委员会的历史赋予的。",

    "Pause and predict. The committee drops the word patient":
        "暂停预测一下。委员会从声明中删去patient一词，其他什么都没改。两年期收益率应该往哪个方向走？",

    # ------------------------------------------------------------------ SESTM
    "Chapter five. Instead of deciding in advance":
        "第五章。不预先决定哪些词好、哪些词坏，而是让市场的反应来决定。模型能学会哪些词重要、有多重要吗？",

    "In 2019 Zheng Tracy Ke, Bryan Kelly and Dacheng Xiu":
        "2019年，Zheng Tracy Ke、Bryan Kelly和修大成取了两千两百五十万篇道琼斯新闻，每篇只关于一只股票，并用那只股票的收益给每篇打上标签。<bookmark mark='a'/>"
        "他们的方法从收益中学到了自己的正面词和负面词。第二天据此交易，等权组合在扣除成本前的年化夏普比率是四点二九；市值加权是一点三三。<bookmark mark='b'/>"
        "它胜过了Loughran和McDonald的词典，也胜过了业内领先的商业新闻分析供应商RavenPack的评分。",

    "The model is simple enough to write down.":
        "这个模型简单到可以写下来。<bookmark mark='a'/>每篇文章有一个介于零和一之间的语气p。它的情感词来自一个混合：权重为p的正面主题，和权重为一减p的负面主题。"
        "其他所有词都不进入模型。<bookmark mark='b'/>收益只通过p依赖于文本，语气越正面，收益为正的概率越高。<bookmark mark='c'/>第一步，筛选：对每个词，在包含它的文章中，"
        "收益为正的占比是多少？保留那些占比远离总体占比、且出现次数足以信赖的词。<bookmark mark='d'/>第二步，把保留下来的词的频率对文章的收益排名做回归，估计两个主题。"
        "第三步，用惩罚极大似然给新文章打分；惩罚项把每个分数拉向中性。",

    'f"Here is the screen on the FOMC statements':
        "这是在FOMC声明上的筛选，在到2012年的{s['n_train']}份声明上训练，以两年期收益率的变动为标签。<bookmark mark='a'/>每个点是一个词：横轴是有多少份声明包含它，"
        "纵轴是这些声明中收益率上升的占比。<bookmark mark='b'/>阈值通过在2007到2012年上验证选出：保留离总体占比至少{s['alpha']:.2f}、且出现在至少{s['kappa']}份声明中的词。"
        "鹰派一侧留下{s['n_pos']}个词，鸽派一侧留下{s['n_neg']}个。<bookmark mark='c'/>有些说得通：inflationary、robust、removed（如移除宽松）在收益率上升的一侧；"
        "slower、constrained、wealth在另一侧。另一些，比如even和after，看起来像是小样本的偶然。",

    "Step two turns the kept words into two topics.":
        "第二步把保留下来的词变成两个主题。<bookmark mark='a'/>把每份声明中保留词的频率对它在收益率变动中的排名做回归：排名最高处的拟合权重是鹰派主题，最低处是鸽派主题。"
        "<bookmark mark='b'/>这里是每个词在鹰派主题中的权重减去它在鸽派主题中的权重。打分将使用这些权重；新声明的语气，就是最能解释其用词的那个两主题混合。",

    'f"The screen itself is a dozen lines':
        "筛选本身是本系列公司文本模块中的十来行代码。<bookmark mark='a'/>哪些文档包含每个词；有多少份；其中正标签的占比；以及两个阈值。在到2012年的声明上运行，"
        "它在{s['n_vocab']}个词中保留了{s['n_pos'] + s['n_neg']}个。",

    'f"Did it learn anything?':
        "它学到东西了吗？<bookmark mark='a'/>在训练所用的声明上，分数与收益率的变动吻合：秩相关为{s['rho_train']:.2f}。<bookmark mark='b'/>在它从未见过的2013到2020年的"
        "{s['n_test']}份声明上，相关是{s['rho']:.2f}，p值为{s['p_rho']:.2f}。符号判断正确的比例是百分之{100 * s['hit']:.0f}。<bookmark mark='c'/>Ke、Kelly和修大成有两千多万篇文章；"
        "我们只有{s['n_train']}份声明。在一百来个标签上筛选数百个词，找到的是偶然拟合过去的词。筛选需要多少文档是一条定理，也正是本部分的研究章。",

    'f"Pause and predict. With {s[\'n_train\']} statements':
        "暂停预测一下。有{s['n_train']}份声明和{s['n_vocab']}个候选词，如果标签是抛硬币，会有多少个词通过这个筛选？",
}

PHRASES = {}
