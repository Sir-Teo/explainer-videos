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

    # ------------------------------------------------------------------ Topics
    "Chapter six. Instead of good and bad, ask what a document is about.":
        "第六章。不问好与坏，而问一份文档讲的是什么。机器能在没有人告诉它的情况下，找到三十年纪要的主题吗？",

    'f"A topic model factors the document-term matrix.':
        "主题模型对文档-词项矩阵做分解。<bookmark mark='a'/>取纪要的加权矩阵，把它写成两个非负矩阵的乘积，中间是{t['k']}个主题。<bookmark mark='b'/>每份文档成为主题的混合，"
        "每个主题成为词的加权，而因为没有什么能为负，每一块读起来都像一个主题。<bookmark mark='c'/>2003年的隐含狄利克雷分配是大多数金融论文使用的概率版本；"
        "非负矩阵分解给出同样形状的输出，二十行代码就能写完。",

    'f"The whole fit is two lines repeated.':
        "整个拟合就是重复两行代码。<bookmark mark='a'/>Lee和Seung的乘法更新：把主题乘以一个比值，拟合偏小时它大于一，偏大时小于一，再对每份文档的权重做同样的事。"
        "什么都不会变成负数，误差每一步都在下降。<bookmark mark='b'/>在纪要上，五百步把相对误差从{t['err'][0]:.2f}降到{t['err'][-1]:.2f}：八个主题留下三十年的大部分细节无法解释，"
        "却保住了大的轮廓。",

    "Here are the eight topics, each named by us":
        "这里是八个主题，每个都是我们读了它的高频词之后命名的；模型只是找到了它们。<bookmark mark='a'/>货币区间与约束；放缓与通胀回落；紧缩与移除宽松；流动性便利；"
        "资产购买与指引；正常化；准备金与回购；还有一个纯程序性的主题，即委员会每年一月会议上续签的授权。<bookmark mark='b'/>注意它们是什么样的主题。不是通胀对就业，而是时代。",

    "Plot each year's mix.":
        "画出每年的混合。<bookmark mark='a'/>纪要从一个时代流向下一个时代：九十年代后期的货币区间；2001年的放缓；2004到2006年的逐步紧缩；2008年的流动性便利，2020年再次出现；"
        "到2014年为止的资产购买与前瞻指引；正常化；然后是准备金和回购这些管道问题。<bookmark mark='b'/>程序性主题是那条从不消失的稳定色带。一个无监督的模型，没有日期也没有标签，"
        "写出了一部委员会议程的历史。",

    "Leland Bybee, Bryan Kelly, Asaf Manela and Dacheng Xiu":
        "Leland Bybee、Bryan Kelly、Asaf Manela和修大成对财经报刊做了同样的事。<bookmark mark='a'/>1984到2017年八十万篇《华尔街日报》文章，变成每个主题每月获得的关注度占比。"
        "<bookmark mark='b'/>这种关注度紧密跟踪经济，能预测股市，并为标准的宏观经济动态模型增加预测力。新闻是一个宏观数据序列，每天都有，远早于官方统计。",

    "Pause and predict. These topics are eras, not themes.":
        "暂停预测一下。这些主题是时代，而不是主题本身。如果你想要一个贯穿每个十年的通胀主题，你会改变什么：主题的个数、加权方式，还是文档？",

    # ------------------------------------------------------------------ FOMC
    "Chapter seven. Text is not only an input to trading":
        "第七章。文本不只是交易的输入；它也是关于决策如何作出的证据。当说话的人知道自己的话会被阅读时，他们会说得不一样吗？",

    "The committee speaks through several documents.":
        "委员会通过几种文件说话。<bookmark mark='a'/>声明，自1994年起。纪要，不具名的讨论摘要，自2005年1月起在每次会议三周后发布。<bookmark mark='b'/>会议记录：每一个字，"
        "署名，五年后发布。自2007年起还有参会者自己的预测，自2011年起有新闻发布会。<bookmark mark='c'/>每一种都是不同的文本，为不同的读者而写，有不同的时滞。",

    "That makes a natural experiment.":
        "这就构成了一个自然实验。<bookmark mark='a'/>自1970年代起会议就被录音以帮助撰写纪要，而委员们以为录音事后会被抹掉。1993年10月，艾伦·格林斯潘透露会议记录是存在的，"
        "美联储同意在五年后公布。一夜之间，每位委员都知道自己的话会被阅读。<bookmark mark='b'/>Stephen Hansen、Michael McMahon和Andrea Prat在前后两个时期对每位发言者的话"
        "运行了主题模型。他们发现了两种效应。纪律：经验较少的委员准备得更充分，用了更多数据。从众：他们也更贴近主席的路线。总体而言，讨论变得更有信息量。",

    "Theory predicted both effects.":
        "理论预言了这两种效应。<bookmark mark='a'/>一位知道自己会被评判的专家会更努力：这是纪律。<bookmark mark='b'/>同一位专家也害怕显得出错，并向观察者所预期的观点靠拢："
        "这是从众。Ellen Meade和David Stasavage已经表明，1993年之后FOMC的反对票变少了。<bookmark mark='c'/>但投票是粗糙的记录。文本让你能度量每位委员说了什么、怎么说，"
        "正是这一点把委员会经济学的一个老问题变成了一次测量。",

    'f"Our own corpus shows the minutes changing too.':
        "我们自己的语料也显示纪要在变化。<bookmark mark='a'/>每根柱子是一份纪要，只计讨论段落。<bookmark mark='b'/>从2005年起，纪要在会议三周后发布，而不是在下一次会议之后，"
        "并本身成为了一份能推动市场的文件。中位数从2005年以前的约{early:,.0f}个词增长到2009年以来的约{late:,.0f}个词。当一份文件成为信号，它的作者就会为它的读者写作。",

    "Pause and predict. A model trained on minutes from before 2005":
        "暂停预测一下。一个用2005年以前的纪要训练的模型被用在之后写的纪要上。即使经济什么都没变，它的分数为什么也可能漂移？",

    # ------------------------------------------------------------------ Embeddings
    "Chapter eight. A bag of words treats easing and tightening":
        "第八章。词袋把easing和tightening当作毫不相关的符号。机器能在没有任何词典的情况下学会词的含义吗？",

    "The idea is from the linguist J. R. Firth in 1957":
        "这个想法来自语言学家J. R. Firth，1957年：观其伴，知其词。<bookmark mark='a'/>raise和lower出现在相同的位置：委员会决定把目标区间如何如何。"
        "有相同邻居的词有相同的含义，或者至少有相同的角色。<bookmark mark='b'/>词嵌入给每个词一个概括其邻居的向量，使得用法相似的词指向同一个方向。",

    "Here is how, with nothing but counting and linear algebra.":
        "具体做法只需要计数和线性代数。<bookmark mark='a'/>统计每个词在其他每个词五个词之内出现的频率，越近的词对计数越多。<bookmark mark='b'/>把计数转换成点互信息："
        "这一对词比偶然情况下多出现了多少；把负值设为零。<bookmark mark='c'/>用奇异值分解分解这个矩阵，保留五十个方向：每个词现在是五十维空间中的一个点。<bookmark mark='d'/>"
        "Omer Levy和Yoav Goldberg在2014年证明，让词嵌入出名的神经网络方法word2vec，隐含地做的正是同样的分解。",

    "Train it on the minutes, and ask for each word's nearest neighbours.":
        "在纪要上训练它，并询问每个词的最近邻。<bookmark mark='a'/>inflation挨着expectations、core和survey-based；purchases挨着asset、large-scale和美联储购买的"
        "mortgage-backed证券；housing挨着residential、homebuilding和construction。<bookmark mark='b'/>tightening的最近邻是easing：扮演同一角色的反义词。"
        "而liquidity与facilities、swap lines和emergency provision住在一起，这是2008年的词汇。这些都没有告诉模型；全在于谁与谁为伴。",

    "Project the two hundred and fifty most common words":
        "把最常见的两百五十个词投影到最能把它们分开的两个方向上。<bookmark mark='a'/>这张图很粗糙，五十维中只取了两维，但邻域显现出来：关于价格和通胀的词在一个区域，"
        "关于劳动力市场的在另一个，金融管道的在第三个。",

    'f"Directions carry relations, too.':
        "方向也承载着关系。<bookmark mark='a'/>取tightening的向量，减去raise，加上lower，问哪个词离它最近。答案是{an['best'][0]}。<bookmark mark='b'/>"
        "tightening之于raise，正如easing之于lower：对含义做算术，这正是让Tomas Mikolov的word2vec在2013年出名的那个技巧，这里只用美联储自己的纪要就重现了。",

    "Pause and predict. Tightening's nearest neighbour is easing.":
        "暂停预测一下。tightening的最近邻是easing。基于这些向量构建的情感分数能区分鹰派声明和鸽派声明吗？",

    # ------------------------------------------------------------------ Transformers
    "Chapter nine. An embedding gives each word one vector":
        "第九章。词嵌入给每个词一个向量，不管它出现在什么句子里。will not hesitate to tighten和will not tighten用几乎相同的词表达相反的意思。"
        "一次读完整个句子，模型能得到什么？",

    "The answer of the last decade is attention":
        "过去十年的答案是注意力，AI系列从零构建过它。<bookmark mark='a'/>为了表示tighten这个词，模型回看句子里的每个其他词，并决定每个词有多重要："
        "在这里，not和hesitate非常重要。<bookmark mark='b'/>tighten的新向量是其他词的加权平均，所以同一个词在每个句子里都得到不同的含义。把几十层这样的结构堆起来，"
        "在足够多的文本上训练，就得到了transformer：BERT、GPT以及此后的每一个模型。",

    "Finance's own transformer came from accounting.":
        "金融领域自己的transformer来自会计学。<bookmark mark='a'/>Allen Huang、Hui Wang和Yi Yang在四十九亿词元的申报文件、业绩电话会和分析师报告上预训练BERT，"
        "再在一万条人工标注的分析师语句上微调。<bookmark mark='b'/>它胜过了词典和较早的机器学习方法，尤其是在其他方法判为中性的句子上，而且只需要很少的标注数据。"
        "用它来度量，业绩电话会所含的信息比旧方法能看到的至少多百分之十八。",

    'f"We cannot train FinBERT here':
        "我们在这里训练不了FinBERT，但可以像AI系列那样，训练它的一个小表亲。<bookmark mark='a'/>用字节对编码学习词的片段，只用训练文本，所以用2007年文本训练的分词器"
        "从未见过pandemic这个词。<bookmark mark='b'/>一个现代的解码器，{cfg['layers']}层，{mpar:.1f}百万参数。<bookmark mark='c'/>在{mtok:.0f}百万个FOMC纪要词元上"
        "训练它预测下一个词元，用的是一台普通的CPU。它的三个副本，在三段不同的历史上训练，就是下一章的实验。",

    'f"Here is the first copy learning.':
        "这是第一个副本在学习。<bookmark mark='a'/>损失从词表大小的对数附近开始，约{l0:.1f}奈特每词元，也就是均匀猜测；随着它学会拼写、语法、再到委员会的习惯，"
        "损失降到约{lend:.1f}。左边是它在从未见过的2008到2012年纪要上的损失，也随之下降。<bookmark mark='b'/>最后是让它续写一个关于金融状况恶化的句子时它写出的内容。"
        "它从未读过2007年以后的任何一个词。",

    "Pause and predict. A model that guesses uniformly over two thousand":
        "暂停预测一下。一个在两千零四十八个词元上均匀猜测的模型，其损失是两千零四十八的对数。用奈特表示是多少，用比特表示又是多少？",

    # ------------------------------------------------------------------ LLMs
    "Chapter ten. Every method so far learned its words from finance alone.":
        "第十章。到目前为止的每一种方法都只从金融文本中学习词。大语言模型到来时已经读过了大部分公开的互联网。当读者是它时，有什么改变？",

    "Here is how the most cited paper did it.":
        "这是被引用最多的那篇论文的做法。<bookmark mark='a'/>假设你是一位有股票推荐经验的金融专家。这条标题对这家公司短期的股价是好是坏？回答是、否或不确定，"
        "再用一句话说明理由。<bookmark mark='b'/>是记为加一，否记为减一，再按公司和日期取平均。没有训练，没有词表，没有标签：模型的通识阅读完成了所有工作。",

    "Alejandro Lopez-Lira and Yuehua Tang ran this":
        "Alejandro Lopez-Lira和Yuehua Tang在十三万四千条标题上做了这件事，这些标题全部发布于模型训练数据截止之后。<bookmark mark='a'/>分数预测了第二天的收益，"
        "并胜过了传统的情感分析方法。<bookmark mark='b'/>最引人注目的是对比：GPT-1、GPT-2和BERT几乎没有这种能力，基于它们的每一个策略都亏钱。"
        "可预测性只出现在大模型中，作者称之为一种涌现能力。",

    "A second way skips the prompt.":
        "第二种方法跳过了提示词。<bookmark mark='a'/>Yifei Chen、Bryan Kelly和修大成把每篇文章输入语言模型，保留它的内部表示，一个长向量。<bookmark mark='b'/>"
        "然后用第二十七部分的岭回归，从收益中学习这个向量的哪些方向具有预测力。<bookmark mark='c'/>在十六个股票市场、十三种语言中，这些表示胜过了基于词的模型，"
        "而且价格对新闻的反应慢到足以交易。",

    "A third uses no text at all.":
        "第三种根本不用文本。<bookmark mark='a'/>Alex Kim、Maximilian Muhn和Valeri Nikolaev把匿名化的财务报表交给GPT-4，只有数字，没有公司名称，"
        "问它明年的盈利会上升还是下降。<bookmark mark='b'/>用简单的提示词，它的正确率是百分之五十二；按照分析师所学的方式一步步分析比率，正确率是百分之六十，高于分析师的一致预期。"
        "这里模型不是在读情绪，而是在做分析。",

    "Three questions every one of these results must answer.":
        "这些结果中的每一个都必须回答三个问题。<bookmark mark='a'/>模型是在什么上训练的？一个读过截至2023年互联网的模型，可能早已知道2019年一条标题之后发生了什么。"
        "<bookmark mark='b'/>它的成本是多少，供应商更新模型之后，明年同样的查询还会给出同样的答案吗？<bookmark mark='c'/>还有谁在问它？任何人都能从同一个公开模型买到的信号，"
        "很快就会被定价。",

    "Pause and predict. BERT could not predict returns from headlines":
        "暂停预测一下。BERT无法从标题预测收益；ChatGPT可以。除了大模型更懂新闻之外，请说出另外两种解释。",

    # ------------------------------------------------------------------ LookAhead
    "Chapter eleven. Part one's first rule was point in time":
        "第十一章。第一部分的第一条规则是时点一致：在时刻t使用的数字只能依赖t之前的数据。对一个读过未来的模型，如何遵守这条规则？",

    "Picture the usual experiment.":
        "设想通常的实验。<bookmark mark='a'/>回测向模型询问2016到2020年的新闻。<bookmark mark='b'/>但模型是用截至2023年的文本训练的，其中包括每一条标题之后发生的事："
        "盈利、诉讼、股价。<bookmark mark='c'/>它的预测可能是记忆。而且不同于回测中泄漏的价格，你无法通过读代码找到这个泄漏：它藏在训练数据的上万亿个词里。",

    "Paul Glasserman and Caden Lin separated two things":
        "Paul Glasserman和Caden Lin把LLM回测所捕捉到的两样东西分开了。<bookmark mark='a'/>技能，来自读标题；加上前视，来自记住随后发生的事；减去分心，"
        "即因为对公司总体了解太多而犯的错误。<bookmark mark='b'/>他们的工具：把标题匿名化，于是Apple beats estimates变成company X beats estimates。<bookmark mark='c'/>"
        "带名称和匿名的回测之差，度量的是前视减去分心。",

    "Their result was a surprise.":
        "他们的结果出人意料。<bookmark mark='a'/>在样本内，匿名的标题表现更好：模型对知名公司的一般了解造成的伤害，大于它的记忆带来的帮助，最大的公司尤其如此。"
        "<bookmark mark='b'/>在样本外，前视不可能存在，但分心可以。所以：匿名化，无论是为了诚实地回测，还是为了交易。",

    "Suproteem Sarkar and Keyon Vafa turned this into a statistical test.":
        "Suproteem Sarkar和Keyon Vafa把这变成了一个统计检验。<bookmark mark='a'/>选择在某个日期之前没有任何信息能预测的事件：只给出候选人的简历，谁赢得了选举。"
        "<bookmark mark='b'/>如果模型胜过偶然，它就读过答案。他们恰恰发现了这一点，在选举中，也在业绩电话会中。<bookmark mark='c'/>但这个检验是单边的。它能抓住泄漏，"
        "却永远无法证明没有泄漏。",

    "The clean answer is to build the models so that they cannot cheat.":
        "干净的答案是把模型构建得无法作弊。<bookmark mark='a'/>Songrun He、Linying Lv、Asaf Manela和Jimmy Wu训练了一系列语言模型，每个只用截至其自身日期的文本："
        "一个日期一个模型，较晚的日期又一个，依此类推。<bookmark mark='b'/>对任何回测日期，就用那个日期的模型。他们的模型在标准基准上能与更大的开放模型竞争，"
        "其实时交易结果接近有泄漏的最先进水平，这表明那些著名结果中的前视是有限的。我们可以自己做同样的实验，在缩小的尺度上。",

    "Pause and predict. A backtest anonymises Apple to company X":
        "暂停预测一下。一次回测把Apple匿名化为company X，却保留了the iPhone maker这个说法。它修复了什么，没修复什么？",

    # ------------------------------------------------------------------ TimeSlice
    "Chapter twelve. We can measure look-ahead ourselves":
        "第十二章。我们可以自己度量前视：用第九章那个小语言模型的三个副本，在三段不同的历史上训练。",

    "The design. <bookmark mark='a'/> The test is the minutes of 2008 to 2012":
        "设计如下。<bookmark mark='a'/>测试集是2008到2012年的纪要：危机、零利率和资产购买，委员会以前从未用过的词汇。<bookmark mark='b'/>模型A只读到2007年为止的纪要："
        "这是2008年1月的研究者真正可能拥有的模型。模型B读到2020年为止的一切，包括测试年份：最纯粹的泄漏。<bookmark mark='c'/>模型C读到2007年，并从2013年开始再读。"
        "它从未见过测试文档，但读过它们之后的未来：这正是一个在互联网上训练的大模型与一次旧回测之间的关系。每个模型都有自己的分词器，由自己的文本构建，训练预算相同。",

    'f"Watch each model\'s loss on the test minutes as it trains':
        "看每个模型在训练过程中于测试纪要上的损失，单位是每字符比特，这样不同的分词器可以公平比较。<bookmark mark='a'/>三个模型都在学习委员会的文风，有一段时间它们一起移动。"
        "<bookmark mark='b'/>然后它们分开了。模型A，诚实的那个，最终为每字符{A:.2f}比特。模型C，只读过测试之后的年份，最终为{C:.2f}：好了约百分之{gap_ac:.0f}，"
        "来自对未来的了解，而从未见过一份测试文档。<bookmark mark='c'/>而读过测试本身的模型B最终为{B:.2f}，又好了百分之{gap_cb:.0f}。每下降一级，都是2008年的研究者不可能拥有的知识。",

    'f"The statements make a cleaner test':
        "声明是更干净的检验，因为没有任何模型在声明上训练过。<bookmark mark='a'/>这里是每个模型对每一年声明的意外程度。2008年以前三条线挨得很近：它们都读过委员会的文风。"
        "<bookmark mark='b'/>从2008年起，模型A的线跳了上去，从2004到2007年的约每字符{a07:.2f}比特，到2009到2012年的{a09:.2f}：声明开始谈论它从未读过的东西。"
        "读过未来的模型则察觉得少得多。这个差距，就是看得见的前视。",

    'f"Ask them directly.':
        "直接问它们。<bookmark mark='a'/>每一行给模型一个句子的开头，用的是委员会2008年开始使用的语言，并问真实的续写有多大可能。<bookmark mark='b'/>"
        "联邦基金利率在零到……：从未见过零利率目标区间的模型A，给四分之一个百分点的概率是百分之{100 * pa:.1f}。同样从未见过2008年、但读过之后内容的模型C，给出百分之{100 * pc:.0f}。"
        "有效下限和前瞻指引也是如此，这些说法模型A从未遇到过。抵押贷款支持证券在2008年以前就已经在委员会的词汇里了，三个模型都预期到了它们。来自未来的词，就躺在权重里。",

    "Or let them write.":
        "或者让它们写。<bookmark mark='a'/>给出同样的开头，鉴于金融状况恶化，委员会……，每个模型各自续写。模型A写的是危机前的委员会：宽松、紧缩、政策路径。<bookmark mark='b'/>"
        "读过危机纪要本身的模型B，直接写出联邦基金利率四分之一个百分点，那是委员会在2008年12月触及的下限。它不是更聪明。它是记得。",

    'f"So the look-ahead comes in two layers.':
        "所以前视有两层。<bookmark mark='a'/>A与C之间的差距是对未来的了解，来自一个从未见过任何测试文档的模型。这正是在互联网上训练的模型与一次旧回测之间的关系，"
        "而匿名化公司名称并不能消除它。<bookmark mark='b'/>C与B之间的差距是对测试本身的记忆，正是Sarkar和Vafa的检验要抓住的东西。<bookmark mark='c'/>只有在测试之前定日期的模型才是诚实的，"
        "这正是时间一致的模型所提供的。而在2008年之前留出的纪要上，模型A是三者中最好的，每字符{la['A']['bpc_val']:.2f}比特，对比{la['C']['bpc_val']:.2f}和{la['B']['bpc_val']:.2f}："
        "其他模型在危机年份上的优势是知识，而不是技能。",

    "Pause and predict. Model C beats model A on the crisis minutes":
        "暂停预测一下。模型C在没见过危机纪要的情况下胜过了模型A。把纪要匿名化，删去每一个日期和名字，能消除这个差距吗？",

    # ------------------------------------------------------------------ Agents
    "Chapter thirteen. So far the language model has been a reader":
        "第十三章。到目前为止，语言模型一直是一个产出分数的读者。最新的系统走得更远：一群会争论、决策和交易的模型。我们对它们了解多少？",

    "An agent is a loop around a language model.":
        "智能体是围绕语言模型的一个循环。<bookmark mark='a'/>它观察：价格、新闻、自己过去的交易。它推理，用文字。它行动，调用一个工具：交易，或者获取更多数据。"
        "它记忆，把结果写回下次会被展示的内容里。<bookmark mark='b'/>这就是ReAct模式，推理与行动交替进行。模型本身没有被重新训练。改变的只是它被展示的内容，"
        "这就是为什么提示词、记忆和一套工具都是策略的一部分。",

    "Here is the design of one of the most discussed, TradingAgents":
        "这是被讨论最多的系统之一TradingAgents的设计，作者是Yijia Xiao、Edward Sun、Di Luo和Wei Wang。<bookmark mark='a'/>四个分析师智能体分别读基本面、社交媒体情绪、"
        "新闻和价格图表。<bookmark mark='b'/>一个看多和一个看空的研究员就分析师的发现展开辩论。<bookmark mark='c'/>一个交易员智能体做决定，一个风险管理团队检查敞口。"
        "每个方框都是一个有自己指令和工具的语言模型：一家投资公司的组织架构，由提示词扮演。作者报告说，在他们测试的股票上，累计收益、夏普比率和回撤都优于标准规则。",

    "Before believing any such result, ask Part twenty-six's questions.":
        "在相信任何这类结果之前，先问第二十六部分的问题。<bookmark mark='a'/>底层模型是何时停止阅读的？图中的每个智能体都可能泄漏未来。<bookmark mark='b'/>"
        "多少只股票、多少个月？几只股票几个月只是一小把独立的赌注，由此得到的夏普比率大多是噪声。<bookmark mark='c'/>在这个之前试过多少种提示词、角色和工具？"
        "每一种都是计数器上的一次试验。<bookmark mark='d'/>每只股票每天调用十几次模型要花多少钱？架构很有趣；证据，到目前为止，还很单薄。",

    "Pause and predict. An agent's backtest shows a Sharpe ratio of five":
        "暂停预测一下。一个智能体的回测在三只股票、三个月上显示夏普比率为五。这个夏普比率的标准误大约是多少？",

    # ------------------------------------------------------------------ AltData
    "Chapter fourteen. Text is one kind of alternative data":
        "第十四章。文本是另类数据的一种：不是价格、成交量或申报数字的信息。一份新数据集值多少钱，当所有人都买了之后又值多少钱？",

    "The menu is long.":
        "清单很长。<bookmark mark='a'/>停车场、油罐和农田的卫星图像；匿名的银行卡消费面板，能在零售商公布之前几周显示其销售；网站流量、应用下载和抓取的价格；招聘信息；"
        "船舶和飞机。<bookmark mark='b'/>还有文本，本部分的主题。它们的共同点是：每一种都在公司自己说出之前，度量了公司业务的某个方面。",

    "The cleanest evidence comes from space.":
        "最干净的证据来自太空。<bookmark mark='a'/>Katona、Painter、Patatoukas和Zeng研究了2011到2017年间出售给投资者的美国零售商停车场汽车数量的卫星计数。"
        "买了这些数据的人能在季报之前盈利交易，尤其是坏消息的季度。<bookmark mark='b'/>但市场整体并没有像你希望的那样变得更知情：有数据的卖空者交易得更多，"
        "没有数据的个人买家吃亏，被覆盖的零售商在财报前后的流动性下降。数据获取的不平等可能扩大投资者之间的差距，却不能改善价格。",

    "The arithmetic of a shared data set is Kyle's model":
        "共享数据集的算术，就是有不止一个知情者的Kyle知情交易者模型，第三十五部分会推导它。<bookmark mark='a'/>N只基金买了同一份数据，所以每只都知道同一个价值；"
        "噪声交易者加入他们的订单；做市商对总订单流定价。<bookmark mark='b'/>在均衡中，随着N增大，每只基金交易得不那么激进，因为其他基金在用同样的东西交易。"
        "<bookmark mark='c'/>每只基金的期望利润按N的负二分之三次方下降，而价格揭示了信息的N分之N加一。一个买家能保住一半的秘密；十个买家，只剩约十一分之一。",

    'f"Draw it.':
        "画出来。<bookmark mark='a'/>每只基金的利润对拥有数据的基金数：到第二个买家时，最大值的一半已经没了。这些点是对市场的模拟，每个二十万次抽样，落在公式上："
        "一个、两个和五个买家时分别为{sim_txt}。<bookmark mark='b'/>现在让供应商沿一条S形采用曲线每年把数据卖给更多基金。作为买家的利润在数据推出后几年内就崩塌了，"
        "远在市场大多数人听说它之前。另类数据的优势在于早，而且不会持久。",

    "Pause and predict. A data set's buyers go from four to nine.":
        "暂停预测一下。一份数据集的买家从四个变成九个。每个买家的利润下降多少倍，买家的总利润又如何？",
}

PHRASES = {}
