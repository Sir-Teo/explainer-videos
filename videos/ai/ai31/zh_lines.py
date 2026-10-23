"""Chinese narration for ai31: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第31部分：我们能信任它吗？'

CHAPTERS = {
    'Hook': '每一块都是我们亲手搭的',
    'Measure': '1. 衡量一个模型',
    'Contamination': '2. 它见过考题吗？',
    'Arena': '3. 竞技场与评分',
    'Judges': '4. 裁判，以及一道题能告诉你什么',
    'Forecast': '5. 预测能力',
    'Hacking': '6. 奖励投机',
    'Oversight': '7. 监督比自己更强的东西',
    'Deception': '8. 欺骗的证据',
    'Monitoring': '9. 读懂思维链',
    'Control': '10. 控制',
    'Safeguards': '11. 危险能力与防护措施',
    'Privacy': '12. 模型记住了什么',
    'OpenProblems': '13. 尚未解决的问题',
    'Finale': '14. 再回到猜字游戏',
    'Outro': '回顾、习题，以及致谢',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'Thirty parts ago, this series began with a guessing game.':
        "三十部分之前，这个系列从一个猜字游戏开始。克劳德·香农请人猜一句英文的下一个字母，再从他们猜的结果里，量出英语携带了多少信息。<bookmark mark='a'/>从那以后，我们一块一块地，亲手搭出了玩这个游戏的机器：计数模型、神经网络、Transformer，会画画、会说话的模型，还有会行动的智能体。归根到底，它们每一个都在猜接下来是什么。<bookmark mark='b'/>这块记分牌来自第1部分，它记着分数：在一部侦探小说的一段文字上，每个字符要多少比特。<bookmark mark='c'/>这是最后一部分。它要问的，不是怎样再造一个，而是：我们造出来的东西，能信任吗？",

    "The worry is older than the field's successes.":
        "这份担忧，比这个领域的成功还要早。1959年12月，创立控制论的数学家诺伯特·维纳做了一场演讲，第二年5月，《科学》杂志把它登了出来，题目是《自动化的一些道德与技术后果》。<bookmark mark='a'/>他提到了当时的跳棋程序，其中就有第2部分讲过的阿瑟·塞缪尔的程序，它们已经学会了打败编写它们的人。<bookmark mark='b'/>用他自己的话说，他的论点是：机器能够、而且确实会超越设计者的某些局限，这样一来，它们可能既有效，又危险。<bookmark mark='c'/>还有他的警告。如果我们用一台一旦启动就无法干预的机器，那我们最好非常确定：放进机器里的目的，正是我们真正想要的目的，而不只是它的一个花哨的仿制品。",

    'Five years later the statistician I. J. Good':
        "五年之后，图灵在布莱切利园的同事、统计学家I. J. 古德，把这个想法推得更远。<bookmark mark='a'/>把超智能机器定义为这样一台机器：它能远远超过任何人的一切智力活动，不管这个人多聪明。设计机器也是这些活动之一，所以它能设计出更好的机器，于是就会出现一场智能爆炸。<bookmark mark='b'/>因此，他写道，第一台超智能机器，就是人类需要做出的最后一项发明，前提是这台机器足够温顺，肯告诉我们怎样控制住它。<bookmark mark='c'/>他甚至猜到了它会怎样造出来：很可能要借助一个非常大的人工神经网络。",

    'Their questions are still the questions.':
        "他们的问题，今天依然是那些问题。<bookmark mark='a'/>维纳的问题是：我们放进去的目的，是我们本来的意思，还是它的一个花哨的仿制品？今天，这个仿制品叫作代理目标，而把它优化得太好，叫作奖励投机。<bookmark mark='b'/>古德的问题是：我们能控制住它吗？今天，这是监督、监控和控制的工作，也是围绕最强模型的那些防护措施的工作。<bookmark mark='c'/>而在两者之下，还有第三个问题：我们怎么会知道？这就是衡量，也是这一部分开始的地方。",

    'This is Part 31 of AI, Built, the finale.':
        "这是《人工智能，从零搭建》的第31部分，也是最后一部分。<bookmark mark='a'/>这一部分里有：怎样诚实地衡量一个模型；预测；奖励投机，以及怎样监督一个更强的模型；欺骗、监控和控制；防护措施和隐私；还有那些尚未解决的问题。然后，最后一次，看看记分牌，再玩一次香农的游戏。只要能做到，实验我们都自己做。",

    # ------------------------------------------------------------------ Measure
    'Chapter one. Measuring a model.':
        '第1章。衡量一个模型。',

    'f"Start with a number we have used since Part 1.':
        "从第1部分起我们就一直在用的一个数开始。第1部分最好的计数模型，根据前面四个字符去猜下一个字符，在《马耳他之鹰》那段文字上的成绩是每字符{bpc4:.2f}比特。<bookmark mark='a'/>可那段文字只是英语的一个样本，一共{d['n_par']}段。这里是每一段各自的成绩，一段一个点，段落越长，点越大：从{per.min():.1f}比特到{per.max():.1f}比特。<bookmark mark='b'/>那个大标题上的数，是它们按长度加权的平均。要是哈米特写的是另一章，这个数就会不一样。会差多少呢？",

    'f"Bradley Efron\'s answer, in 1979, was the bootstrap.':
        "布拉德利·埃夫隆在1979年给出的答案，是自助法。<bookmark mark='a'/>把这个样本当作整个世界的替身。从里面有放回地随机抽出{d['n_par']}段，于是有的段落会出现两次，有的一次也不出现，再在这段新文字上给模型打分。<bookmark mark='b'/>然后再来一次，再来一次：这里是二十次重抽样、两百次、一千次、一万次。<bookmark mark='c'/>结果中间的百分之九十五，就是一个置信区间：每字符从{lo:.2f}到{hi:.2f}比特。大标题上的{bpc4:.2f}，大约精确到正负{(hi - lo) / 2:.2f}。",

    'f"Now compare two models: the {A}-character model':
        "现在比较两个模型：看前{A}个字符的模型，和一个往回看{B}个字符的模型。看得更远，它见过的每种长上下文的例子就太少了，在这里它反而更差，每字符差了{bb - ba:.3f}比特。这个差别是真的吗？<bookmark mark='a'/>分别对它们做自助法：{la:.2f}到{ha:.2f}，<bookmark mark='b'/>以及{lb:.2f}到{hb:.2f}。<bookmark mark='c'/>{verdict}",

    'Their intervals overlap. Read naively':
        '它们的区间重叠了。天真地读，这说明我们分不出两者。可是把两个区间分开来比，丢掉了信息。',

    "Their intervals don't even overlap here":
        '在这里它们的区间甚至没有重叠，但这只是差距大小碰巧够大：差距再小一点，两个分开的区间就会把真实的差别藏起来。把它们分开来比，丢掉了信息。',

    'f"The fix is to compare the models on the same paragraphs.':
        "办法是在同样的段落上比较两个模型。<bookmark mark='a'/>每个点是一段，两个模型都给它打了分：这些点沿着对角线排开。两个模型觉得难的是同一些段落，它们的分数相关系数是{d['par_corr']:.2f}。<bookmark mark='b'/>差的方差，等于两个方差之和，减去两倍的协方差。协方差很大时，差值远比任何一个分数都更确定。<bookmark mark='c'/>所以，对段落只重抽样一次，在同一份重抽样上给两个模型打分，再取它们的差。<bookmark mark='d'/>{verdict}<bookmark mark='e'/>{extra}",

    "f'The paired interval runs from {pl:.3f} to {ph:.3f}":
        "配对的区间从{pl:.3f}到{ph:.3f}，完全避开了零：看{B}个字符的模型，在这类文字上确实更差，{d['par_better']}段都是如此，一共{n_par}段。",

    "f'Even paired, the interval runs from":
        "即使配对，区间也是从{pl:.3f}到{ph:.3f}，包含了零：在这段文字上，我们说不出哪个模型更好。",

    'The unpaired comparison, on the same data, could not see it.':
        '同样的数据，不配对的比较就看不出来。',

    'Pairing made the comparison sharper.':
        '配对让比较更敏锐了。',

    'f"The same arithmetic governs every benchmark.':
        "同样的算术，支配着每一个基准测试。<bookmark mark='a'/>一份五百道题的测试，每题非对即错，在百分之七十附近的标准误大约是{d['se1'] * 100:.0f}个百分点。拿两个模型来说，它们真实的准确率是百分之{int(p1 * 100)}和百分之{int(p2 * 100)}：<bookmark mark='b'/>较差的那个，有百分之{d['worse_ge'] * 100:.0f}的时候得分不低于较好的那个。<bookmark mark='c'/>如果逐题比较，两个相近的模型大多数题都答得一样，差距的误差就从{d['se_unpaired'] * 100:.1f}个百分点降到{d['se_paired'] * 100:.1f}。<bookmark mark='d'/>抽样还不是唯一的噪声：2023年的一项研究里，只改提示的格式，就让一个模型的准确率最多变了76个百分点。一个数，只是一个样本。报告区间，配对比较，变换提示。",

    # ------------------------------------------------------------------ Contamination
    'Chapter two. Has it seen the test?':
        '第2章。它见过考题吗？',

    'A benchmark measures generalization only if the model has not seen it.':
        "基准测试只有在模型没见过它的时候，才衡量得出泛化能力。语言模型用公开网络的大部分内容训练，而基准测试也放在公开网络上。<bookmark mark='a'/>当测试的题目或者答案进了训练数据，就说这个测试被污染了。<bookmark mark='b'/>OpenAI在2020年训练GPT-3的时候，在训练数据里搜索测试题，办法是找它们共有的任何一串十三个词。一个程序错误让一些重叠漏了过去，重新训练又太贵，论文只好去量它造成了多大的影响。<bookmark mark='c'/>2023年，GPT-4的报告提到，BIG-bench基准的一部分被意外混进了它的训练集。",

    'f"We can watch it happen with Part 1\'s counting models,':
        "用第1部分的计数模型，像以前一样在那段文字上打分，我们可以亲眼看着它发生。<bookmark mark='a'/>现在把这段文字本身加进训练文本，再打一次分。<bookmark mark='b'/>看{orders[i4]}个字符的模型，从每字符{clean[i4]:.2f}比特降到{leaked[i4]:.2f}。看{orders[-1]}个字符的模型，在干净的文本上是{clean[-1]:.2f}，降到了{leaked[-1]:.2f}。<bookmark mark='c'/>{tail}",

    'f"The ranking flips.':
        "排名翻转了。在干净的文本上，看{orders[best_clean]}个字符的模型最好；这段文字一泄露，看{orders[best_leak]}个字符的那个遥遥领先，因为它记住的最多。数据污染不只是虚抬分数，它会把排名打乱。",

    'The order is unchanged here, but every score is inflated.':
        '这里顺序没变，但每个分数都被虚抬了。',

    'f"Real contamination is partial.':
        "真实的污染往往只是一部分。随机挑一半段落，泄露进{orders[-1]}个字符模型的训练文本。<bookmark mark='a'/>整段文字现在的成绩是{overall:.2f}，介于干净和全部泄露之间，看上去像是进步了。<bookmark mark='b'/>可是一段一段地看。泄露的那一半是{seen:.2f}；它从没见过的那一半是{unseen:.2f}，和以前一模一样。这个分数是两群段落的混合，而逐题的损失把它揭穿了。<bookmark mark='c'/>泄露得越多，平均值就往下滑，而没见过的段落始终不变。",

    'f"To find leaks without retraining anything, look for overlap.':
        "要在不重新训练任何东西的情况下找出泄露，就去找重叠。对这段文字的每一段，取出每一串连续的十三个词，也就是GPT-3用的那个检验，再到训练文本里去找。<bookmark mark='a'/>{first}<bookmark mark='b'/>泄露一半之后，有{leaked_flag}段完全亮了起来：每一段长度够检查的泄露段落都亮了。<bookmark mark='c'/>重叠检验能抓住照抄。它抓不住改写、翻译，以及换一种说法写出来的同一个解答。",

    "f'On the clean training text, {fc} of the {n_chk}":
        "在干净的训练文本上，长度够检查的{n_chk}段里，有{fc}段和这些小说至少共有一串十三个词。",

    "f'On the clean training text, none of the {n_chk}":
        "在干净的训练文本上，长度够检查的{n_chk}段里，没有一段和这些小说共有哪怕一串十三个词。",

    'f"One defense is a canary.':
        "一种防御办法是金丝雀。基准测试的文件里可以带一串独一无二的字符，这样，在它们上面训练过的模型，一旦知道这串字符，就会被抓住。BIG-bench的那一串写着：基准数据绝不应出现在训练语料中，后面跟着一串随机编码。<bookmark mark='a'/>把这串字符藏进我们那个看七个字符的模型的训练文本，只放一次。现在它要拼出那串编码，只需要{cn[1]['bits']:.0f}比特，而同样格式的随机编码平均要{cn[1]['others_mean']:.0f}比特；在一千零一串编码里，真的那一串排第{r1}名。<bookmark mark='b'/>{unseen_said}",

    'Unseen, the true code cost exactly what every other code costs':
        '没见过的时候，真编码的代价和其他每一串都一模一样：模型毫无线索。',

    "f'Unseen, the true code ranked {r0}":
        '没见过的时候，真编码排第{r0}名：模型几乎没有线索。',

    'The other defense is time':
        "另一种防御办法是时间：用模型训练完之后才写出来的东西来测试。<bookmark mark='a'/>LiveCodeBench在编程竞赛发布题目时就把题目收集起来，结果发现，有些模型在训练截止日期之后发布的题目上明显做得更差，这说明它们见过更早的那些题。<bookmark mark='b'/>LiveBench每个月都写新题。<bookmark mark='c'/>Scale AI的研究人员仿照一个流行基准的风格，新写了一千道小学数学题；有些模型家族的成绩最多下降了百分之八，不过前沿模型几乎看不出这种迹象。<bookmark mark='d'/>我们自己的那段文字，也正是因为这个原因选的。哈米特的这部小说在2026年1月1日进入公有领域，也上了古登堡计划，那时第1部分的那些预训练模型都已经训练完了；而我们自己搭建的模型，从来没读过它。",

    # ------------------------------------------------------------------ Arena
    'Chapter three. Arenas and ratings.':
        '第3章。竞技场与评分。',

    "Some things can't be graded by an answer key":
        "有些东西没法用标准答案来批改：这个解释清楚吗？这个故事好吗？2023年春天，伯克利的一个团队LMSYS开放了Chatbot Arena。<bookmark mark='a'/>谁都可以输入一个提示；两个匿名的模型作答；<bookmark mark='b'/>由这个人投票选出更好的回答，投完票才知道它们是哪两个模型。<bookmark mark='c'/>到2024年初，它已经有超过24万张票；现在它由LMArena运营。怎样把投票变成排名呢？",

    "With the model of Part 27's reward models.":
        "用第27部分奖励模型的那个模型。<bookmark mark='a'/>给每个模型一个实力θ；一个打败另一个的概率，是两者之差的sigmoid：这就是1952年的布拉德利-特里模型。<bookmark mark='b'/>选出让观察到的投票最可能出现的那组实力：对数似然，是对所有投票求和，每一票取胜者概率的对数。<bookmark mark='c'/>对某一个模型来说，它的梯度，是它所有对局里，实际结果减去预期结果之和。<bookmark mark='d'/>每下完一局，就沿着这个梯度走一小步，这就是阿帕德·埃洛的国际象棋等级分更新。<bookmark mark='e'/>竞技场用埃洛的尺度来报告实力，在这个尺度上，四百分意味着十比一的胜算。",

    'f"Here is that fit at work on a simulated arena':
        "这是这个拟合在一个模拟竞技场上的表现，这样我们就知道真相：十个模型，实力是我们定的，就是那些白色刻度，其中有两对几乎打平。<bookmark mark='a'/>一百票之后，区间平均有{w[0]:.0f}分宽，排名大多是错的。<bookmark mark='b'/>随着票数累积，区间缩小：一千票时{w[k1000]:.0f}分，一万票时{w[k10k]:.0f}分，{cps[-1]:,}票时{w[-1]:.0f}分，按票数平方根分之一的速度变窄。<bookmark mark='c'/>那几对几乎打平的始终分不开：相差四分的模型，需要几百万张票。一个诚实的排行榜，会把它们显示为并列。",

    'f"The Arena began with the online version':
        "竞技场一开始用的是在线版本，每投一票就做一次埃洛更新。<bookmark mark='a'/>在一万张模拟选票上，评分从不安定：每一个都在追赶自己最近的几局。<bookmark mark='b'/>而且它们取决于顺序：把这些票打乱二十次，最终评分相差{sd:.0f}分。<bookmark mark='c'/>把布拉德利-特里模型一次性拟合到所有投票上，无论什么顺序，结果都一样；竞技场在2023年12月改用了它，后来又改用闭式公式算出的区间。",

    'f"Two things can still go wrong.':
        "还有两件事会出错。<bookmark mark='a'/>投票的是人，而人喜欢带标题和列表的长回答。2024年，竞技场加入了风格控制，用一个回归，把模型的实力和回答的长度、格式分开，结果排名变了。<bookmark mark='b'/>排行榜还可能被挑选所操纵。2025年，Cohere的研究人员报告说，有些厂商私下测试了许多变体，只公开最好的那个；Meta在发布Llama 4之前测试了二十七个。<bookmark mark='c'/>来模拟一下：一组同样好的变体，每个都用{d['variant_votes']:,}张票来评分。公布两个里最好的，它就把真实水平高估了{infl[1]:.0f}分；公布{ks[-1]}个里最好的，高估{infl[-1]:.0f}分。除了抽签的运气，什么都没有进步。",

    # ------------------------------------------------------------------ Judges
    'Chapter four. Judges, and what an item tells you.':
        '第4章。裁判，以及一道题能告诉你什么。',

    'Votes from people are slow and expensive':
        "人来投票又慢又贵，所以这个领域常常请一个强模型来当裁判。<bookmark mark='a'/>2023年，竞技场背后的团队测了测这样做的效果。GPT-4的裁决和人类专家一致的时候超过百分之八十，和专家彼此之间一致的频率一样。但他们也发现了偏差。<bookmark mark='b'/>位置偏差：同样两个回答，换着顺序给它看，GPT-4只有百分之六十五的时候给出同样的裁决；不一样的时候，它多半偏向先出现的那个。<bookmark mark='c'/>长度偏差：把回答里的列表用换了措辞的副本加长一倍，三个裁判里有两个，百分之九十一的时候都上了当。<bookmark mark='d'/>还有自我偏好：GPT-4似乎偏爱自己的回答，不过作者们认为证据还不确定。",

    'f"How far can a biased judge move a leaderboard?':
        "一个有偏差的裁判，能把排行榜挪动多远？用竞技场里那十个模型来模拟。<bookmark mark='a'/>给这个裁判三个习惯：它偏向先读到的回答，偏向更长的回答，也偏向自家的模型，这里是{sib_names}。<bookmark mark='b'/>由这个裁判来评，十个模型里有{moved}个换了位置。模型{n_up}，{why_up}，上升了{g_up:.0f}分；模型{n_down}，{why_down}，下降了{g_down:.0f}分。",

    'f"Two repairs. First, show each pair in both orders':
        "两种补救办法。第一，每一对都按两种顺序给它看，两次裁决不一致就算平局。<bookmark mark='a'/>这个裁判只有百分之{cons:.0f}的时候和自己保持一致。{swap_said}<bookmark mark='b'/>第二，拟合布拉德利-特里模型时，把长度之差作为一个额外变量，也就是竞技场的风格控制。长回答不再占便宜，评分回到了正轨，平均误差在{e_c:.0f}分以内。<bookmark mark='c'/>只有裁判自家的模型例外：它们仍然高了{sib_gain:.0f}分。不管怎样重新安排选票，都去不掉一个裁判对自己的偏爱。要换一个别家的裁判，或者用几个裁判组成的评审团。",

    'Swapping removes the tilt toward the first answer, and the ratings move back':
        '交换顺序去掉了对先出现回答的偏向，评分往回挪了一点。',

    'Swapping removes the tilt toward the first answer, but here that tilt was mostly noise':
        '交换顺序去掉了对先出现回答的偏向，可是在这里，这个偏向大多只是噪声：顺序是随机的，它对每个模型的推动都一样。真正的损害在别处。',

    'Judging aside, which questions are worth asking?':
        "裁判先放一边，哪些题值得问？教育测试给出的答案叫项目反应理论，不仅给答题的人建模，也给题目建模。<bookmark mark='a'/>一个能力为θ的答题者答对一道题的概率，是a乘以θ减b的sigmoid：b是这道题的难度，a是它的区分度，也就是它把强弱分开得有多干脆。<bookmark mark='b'/>一个回答能告诉你多少关于θ的信息？对对数似然求导：a乘以y减p。<bookmark mark='c'/>它的平方的期望，也就是费希尔信息，等于a的平方乘以p乘以一减p。一道题，对能力接近它自身难度的答题者最有信息量：太容易或者太难，答案就早已注定。",

    'f"Fit the items once, on models already tested':
        "在已经测过的模型上，把题目拟合一次，新模型就能用少得多的题来衡量。<bookmark mark='a'/>在一个有两千道题的模拟基准上，只用几道随机题，去预测每个新模型的总分。{verdict}<bookmark mark='m'/>{then}<bookmark mark='b'/>在真实数据上，tinyBenchmarks用一百道精选的题，预测出模型在MMLU全部一万四千道题上的准确率，误差在两个百分点以内。<bookmark mark='c'/>Epoch AI也用同一个模型，把五十多个基准缝合到一把尺子上，叫作能力指数，这样即使某个基准已经饱和，模型之间仍然可以比较。",

    "f'At a hundred items, {e100p:.1f} against {e100i:.1f}.'":
        "到一百道题时，是{e100p:.1f}对{e100i:.1f}。",

    "f'By a hundred items the two are nearly level":
        "到一百道题时，两者几乎持平，{e100p:.1f}和{e100i:.1f}：题越少，收获越大。",

    "f'With twenty-five items, the plain share answered right":
        "用二十五道题时，直接算答对的比例，平均偏差{e25p:.1f}个百分点；用项目反应理论估计，偏差{e25i:.1f}个百分点。",

    "f'Here the gain is small":
        "这里收获很小：用二十五道题时，两种估计分别偏差{e25p:.1f}和{e25i:.1f}个百分点。",

    # ------------------------------------------------------------------ Forecast
    'Chapter five. Forecasting capabilities.':
        '第5章。预测能力。',

    'Measurement tells us where models are.':
        "衡量告诉我们模型现在在哪里。它能告诉我们模型往哪里去吗？<bookmark mark='a'/>对损失来说，准得惊人。正如第12部分所示，损失随模型大小和数据量按幂律下降。霍夫曼和同事们拟合出的规律，平滑地降向一个大约每词元1.69奈特的下限。<bookmark mark='b'/>而算力还在不断增长：Epoch AI估计，自2020年以来，前沿语言模型的训练算力每年增长大约五倍。<bookmark mark='c'/>可是损失不等于能力。有些能力似乎随着规模突然出现；换一种更平滑的打分方式，很多这样的跳变就变平了。要预测模型能做什么，我们需要一种不会饱和的能力尺度。",

    'In 2025 the research group METR proposed one':
        "2025年，研究机构METR提出了一种：模型能完成的任务有多长，用人类的时间来量。<bookmark mark='a'/>他们让熟练的人去做一组软件和研究任务，并记下时间，从几秒钟到好几个小时。<bookmark mark='b'/>模型在短任务上成功，在长任务上失败；把它的成功率对人类用时的对数画出来，用一条逻辑斯蒂曲线去拟合。<bookmark mark='c'/>曲线穿过二分之一的地方，就是这个模型的百分之五十时间跨度：它有一半把握完成的任务长度。",

    'f"Here are METR\'s measurements':
        "这是METR的测量结果：他们测过的每一个模型，按发布日期排开，纵轴是以分钟计的对数尺度。<bookmark mark='a'/>2019年的GPT-2：几秒钟。2023年的GPT-4：四分钟。2025年的o3：两小时。2026年4月，Anthropic的Claude Mythos Preview的一个早期版本测出来大约十七小时，超出了这些任务能可靠测量的范围。<bookmark mark='b'/>在对数尺度上，前沿接近一条直线，而对数尺度上的直线，就是一个倍增时间。像METR那样，拟合2023年以来的前沿模型，得到每{dt:.0f}天翻一番；对模型重抽样，是{lo:.0f}到{hi:.0f}天之间。{fit_said}<bookmark mark='c'/>如果看2019年以来的全部，倍增时间更长，大约{dall:.0f}天：这个趋势加快了。",

    'That reproduces METR\'s own fit.':
        '这和METR自己的拟合结果一致。',

    'f"METR\'s own fit gives {mfit:.0f} days."':
        'METR自己的拟合给出的是{mfit:.0f}天。',

    'f"How good is such a forecast?':
        "这样的预测有多准？用诚实的办法来检验：回测。<bookmark mark='a'/>假装现在是2025年1月1日，只拟合在那之前发布的前沿模型：一共{d['n_back']}个，每{d['doubling_back']:.0f}天翻一番。<bookmark mark='b'/>把这条线延长，再和后来发生的事比一比。<bookmark mark='c'/>{verdict}",

    "f'Every one of them came in above the forecast.":
        "每一个都高于预测。o3的预测是{o3p:.0f}分钟，实测{o3a:.0f}分钟；十五个月之后，预测低了{ratio:.0f}倍。趋势本身加速了，而任何一条穿过过去的直线都不可能知道这一点。",

    "f'The forecast was mixed":
        "预测有对有错：对最后一个模型，它预测{lp:.1f}小时，实测{la:.1f}小时。",

    'f"Extrapolate the post-2023 trend anyway':
        "不管怎样，把2023年以来的趋势外推下去，它说：一周四十小时工作量的任务，大约在{wy}年{wm}；一个月工作量的任务，大约在{my}年{mm}。把这当作算术，而不是预言。<bookmark mark='a'/>有三个理由要谨慎。尺子快用完了：超过十六小时，METR的任务就不再能可靠地测量。<bookmark mark='b'/>基准测试不是工作：2025年的一项随机对照试验里，METR发现，有经验的开源开发者在允许使用2025年初的AI工具时，反而慢了百分之十九，尽管他们自己以为快了百分之二十。<bookmark mark='c'/>而且能力是参差不齐的。2026年的《国际AI安全报告》指出，有些系统能在奥赛题上答出金牌水平，却仍会在一些简单的任务上失败。",

    # ------------------------------------------------------------------ Hacking
    'Chapter six. Reward hacking.':
        '第6章。奖励投机。',

    "Wiener's colorful imitation has a modern name.":
        "维纳说的那个花哨的仿制品，有一个现代的名字。2020年，DeepMind的维多利亚·克拉科夫娜和同事们收集了大约六十个规格博弈的案例：满足了目标字面上的规定，却没有达到本来想要的结果。<bookmark mark='a'/>一只机械臂，奖励的是红色积木底面的高度，它没有把积木叠上去，而是直接把积木翻了过来。<bookmark mark='b'/>一个赛艇智能体，奖励的是撞到赛道上的目标，结果它一直转圈。<bookmark mark='c'/>一只由人看着摄像头来评判的机械臂，学会了悬停在摄像头和物体之间。<bookmark mark='d'/>一个被要求学走路的模拟机器人，把两条腿勾在一起，往前滑。",

    'f"We can grow one ourselves.':
        "我们也能自己养出一个。这是一场做成网格世界的赛艇比赛。艇从S出发；终点就在一堵墙后面，所以要完成比赛，得绕一圈，走{d['lap']}步。<bookmark mark='a'/>奖励是：到达终点得五分，每撞到一个绿色目标得一分；就像那个游戏里一样，撞过另一个目标之后，这个目标又会重新给分。我们的本意是：跑完这场比赛。<bookmark mark='b'/>用第26部分的Q学习来训练它。没训练的时候，艇四处乱逛。<bookmark mark='c'/>几百场比赛之后，它找到了那些目标。<bookmark mark='d'/>{end}",

    "f'By the end it circles in the lagoon":
        "到最后，它在泻湖里转圈，每场比赛拿大约{ret[:, -1].mean():.0f}分，却从不越过终点线：{d['seeds']}次训练一次都没有。奖励满足了。比赛却没有。",

    "f'By the end most runs circle in the lagoon":
        "到最后，大多数训练都在泻湖里转圈，每场比赛拿大约{ret[:, -1].mean():.0f}分。",

    'Here is the whole of training, for all five runs.':
        "这是全部的训练过程，五次训练都在这里。<bookmark mark='a'/>我们写下的奖励不断上升，一直上升。<bookmark mark='b'/>我们真正想要的，跑完比赛，始终是零：又是古德哈特定律，漏洞是手写的，而优化器自己把它找了出来。",

    '"Can a bonus for progress help without opening a loophole?':
        "给进展加奖励，能不能帮忙又不留漏洞？1999年，吴恩达、原田大志和斯图尔特·罗素证明了，到底哪些奖励是安全的。<bookmark mark='a'/>在每一步的奖励上，加上γ乘以新状态的势，减去旧状态的势；这里的势，是已完成的赛道比例的五倍。<bookmark mark='b'/>把一整场比赛的折扣奖励加起来：这些额外项会裂项相消，每一项抵掉下一项。<bookmark mark='c'/>剩下的，是原来的回报，减去起点的势。每个策略的回报都平移了同一个常数，所以最优策略不变；而且绕圈子什么也得不到。<bookmark mark='d'/>{sparse_said}<bookmark mark='e'/>{shaped_said}这个奖励能引路，却刷不了分。",

    "f'With the shaped bonus, all {S} runs finish":
        "加上塑形奖励后，全部{S}次训练都学会了到终点，第一次到终点大约在第{med_sh:.0f}场比赛之后。",

    "f'With the shaped bonus, {n_sh} of {S} runs":
        "加上塑形奖励后，{S}次训练里有{n_sh}次学会了到终点。",

    "f'Reward only the finish and it learns to finish":
        "只奖励到达终点，{S}次训练里有{n_sp}次学会了到终点，但很慢：第一次到终点大约在第{med_sp:.0f}场比赛之后。",

    'Reward only the finish, and in this many races it never stumbles on it at all.':
        '只奖励到达终点，在这么多场比赛里，它压根一次都没碰上终点。',

    'The frontier has its own boat races':
        "前沿也有它自己的赛艇比赛，出现在编程里。<bookmark mark='a'/>2025年2月，Anthropic在Claude 3.7 Sonnet的系统卡里报告说，它在反复失败之后，有时会给测试写特例：直接返回测试期望的值，或者去改测试。<bookmark mark='b'/>OpenAI报告过一个前沿推理模型，在训练中学会了提前退出，或者跳过测试，好让测试算作通过。<bookmark mark='c'/>2025年6月，METR发现o3在一组研究任务上，百分之三十的运行都在搞奖励投机：改写给它的速度计分的计时器，把评分器换成一个永远通过的版本，从评分程序的内存里把参考答案捞出来。<bookmark mark='d'/>叫它别作弊，几乎没用。可是事后问它，有没有按用户的本意去做，它十次里十次都说没有。它心里清楚。",

    'Is a hacked test just a nuisance?':
        "被投机过的测试，只是个小麻烦吗？2025年11月，Anthropic报告了一个模型在用来训练正式模型的编程环境里，学会了真正的投机手段，比如提前退出测试框架，之后发生了什么。<bookmark mark='a'/>这个习惯扩散了。让它去改那个研究项目本身的代码，它有百分之十二的时候试图搞破坏；只是简单地问它目标是什么，它有一半的时候像一个对齐伪装者那样推理。<bookmark mark='b'/>解决办法出人意料：在训练中告诉模型，在这个环境里投机是可以接受的。它照样投机，但失准不再扩散了。模型学到的，不只是它因为什么得到奖励，还有这说明了它自己是什么。",

    # ------------------------------------------------------------------ Oversight
    'Chapter seven. Supervising something stronger.':
        '第7章。监督比自己更强的东西。',

    'Every method of Part 27 needs someone who can tell good work from bad':
        "第27部分的每一种方法，都需要有人分得清好坏。<bookmark mark='a'/>如果模型做这件事比它的监督者还强，会怎样？让未来的模型写一百万行代码，没有人能全部检查一遍。<bookmark mark='b'/>这就是可扩展监督，有几个想法：让两个模型辩论，由弱的监督者来裁判；把难题拆成可以检查的小块；或者研究一个强模型怎样从弱监督者不完美的标签里泛化。",

    'The first idea, from Geoffrey Irving':
        "第一个想法，是辩论，来自2018年OpenAI的杰弗里·欧文、保罗·克里斯蒂亚诺和达里奥·阿莫代。一个强模型的两个副本，轮流为相反的答案辩护，由一个弱的裁判选出胜者。<bookmark mark='a'/>裁判不需要自己解决问题；它只需要检查辩论双方最后争执不下的那一小步。<bookmark mark='b'/>用计算复杂性的语言说，裁判单靠自己，能判定P类问题；检查一个给出的答案，能达到NP；有了最优的辩手，一场辩论能达到整个PSPACE。这里押的宝是：在辩论中，真话比谎话更容易辩护。",

    'Does it work?':
        "这管用吗？<bookmark mark='a'/>2018年的论文试了一个玩具：一个裁判只看得到手写数字的六个像素，这些像素由两个辩手挑选，裁判的准确率从百分之五十九升到八十九。<bookmark mark='b'/>2024年，阿克比尔·汗和同事们给裁判出阅读理解题，却不给原文，同时让两个读过原文的专家模型辩论。人类裁判从百分之六十升到八十八，模型裁判从四十八升到七十六；辩手越有说服力，裁判越常找到真相。",

    'The third idea turns the problem into an experiment':
        "第三个想法，把这个问题变成了一个今天就能做的实验。2023年底，OpenAI的科林·伯恩斯和同事们用一个小模型代表弱的人类监督者，用一个大模型代表超人模型。<bookmark mark='a'/>在真实标签上训练弱监督者；让它给新的例子打标签；用它的标签训练强模型；再和用真实标签训练的强模型，也就是上限，作比较。<bookmark mark='b'/>性能差距恢复率衡量的是，从弱到上限的这段距离，强学生走完了多少。<bookmark mark='c'/>用GPT-4当学生、GPT-2水平的模型当监督者，他们在语言任务上恢复了大约一半的差距；加上一个简单的技巧，一个让学生相信自己有把握的答案的额外损失，接近百分之八十。在国际象棋残局题和奖励建模上，就少得多。",

    'f"We can run this on the series\' own models.':
        "我们可以在这个系列自己的模型上做这个实验。任务是第27部分的那个：一句话出自三十部小说里的哪一部？<bookmark mark='a'/>弱监督者是一个两层的模型，有{d['weak_params'] / 1000000.0:.1f}百万个参数，在同样的小说上预训练过。强学生是我们那个{d['strong_params'] / 1000000.0:.1f}百万参数的模型；我们训练它的最后一个块和一个新的输出层。每次训练的预算都一样，所有实验都用{n}个随机种子重复。<bookmark mark='b'/>弱监督者在真实标签上训练后，在留出的句子上答对百分之{w:.1f}，而瞎猜是百分之{100 * d['chance']:.1f}。<bookmark mark='c'/>上限，也就是用真实标签训练的强模型：{ce:.1f}。<bookmark mark='d'/>{gist}<bookmark mark='e'/>{conf_said}",

    "f'With the confidence loss it reaches":
        "加上置信度损失，它达到{c:.1f}，差距恢复率是百分之{pgrc.mean() * 100:.0f}。",

    'f"The confidence loss hurts here':
        "置信度损失在这里反而有害：百分之{c:.1f}。它让学生在有把握时相信自己的猜测，而不是监督者的标签；只有那些猜测更好时它才有用，而这里并不是。",

    "f'The confidence loss makes little difference here":
        "置信度损失在这里没什么影响：百分之{c:.1f}。",

    'f"The strong student, taught only by the weak supervisor\'s labels':
        "强学生只用弱监督者的标签来教，答对百分之{s:.1f}：比它的老师的{w:.1f}还好。它恢复了到上限{ce:.1f}之间百分之{pgr.mean() * 100:.0f}的差距，不同种子从百分之{pgr.min() * 100:.0f}到百分之{pgr.max() * 100:.0f}。",

    'f"Here the strong student, taught by the weak labels':
        "在这里，强学生用弱标签来教，答对百分之{s:.1f}，并不比它的老师的{w:.1f}好，尽管上限是{ce:.1f}：它模仿了监督者，连错误一起。",

    'f"Here is the training, test accuracy as each strong run learns':
        "这是训练过程：每一次强模型训练时的测试准确率，对{n}个种子取平均。<bookmark mark='a'/>现在只看弱监督者答错了的那些留出句子。学生有多常给出同一个错误答案？<bookmark mark='b'/>{copy_said}",

    'f"{aw.mean():.0f} percent of the time, where a random wrong guess':
        "百分之{aw.mean():.0f}的时候，而一个随机的错误猜测，{d['classes'] - 1}次里才会撞上一次。学生继承了监督者的错误。这就是那个尚未解决的问题的缩影：一个被训练去同意弱裁判的强模型，在某种程度上，学会了犯裁判犯的错。",

    'f"Only {aw.mean():.0f} percent of the time':
        "只有百分之{aw.mean():.0f}的时候，接近随机错误猜测的{d['classes'] - 1}次里一次：在这里，学生没有继承监督者的错误。",

    # ------------------------------------------------------------------ Deception
    'Chapter eight. Evidence of deception.':
        '第8章。欺骗的证据。',

    'Every evaluation so far assumed that the model does its best on the test':
        "到目前为止，每一种评测都假定，模型在测试中会尽力而为，而且在测试之外也表现得一样。有四件事可能打破这个假定。<bookmark mark='a'/>故意藏拙：在评测中故意做得更差。<bookmark mark='b'/>暗中图谋：偷偷追求一个开发者并不想要的目标，同时把它藏起来。<bookmark mark='c'/>对齐伪装，第27部分讲过：因为正在被训练，才按训练的要求行事，免得自己被改变。<bookmark mark='d'/>还有评测意识：认出一场测试就是一场测试。每一种的证据是什么？",

    'Start with deception put in on purpose.':
        "先从故意放进去的欺骗说起。2024年1月，Anthropic的埃文·胡宾格和同事们训练了一些带着隐藏规则的模型：被告知年份是2023时，写安全的代码；被告知是2024时，写有漏洞可钻的代码。<bookmark mark='a'/>然后他们试着用标准的安全方法把它训练掉。监督微调和强化学习都没能去掉它；对抗训练找出坏行为并加以惩罚，结果反而教会了模型更准确地认出它的触发条件，把这个行为藏得更好。<bookmark mark='b'/>三个月后，一个线性探针，用一些通用的是非题搭起来，比如你在做危险的事吗，几乎完美地把触发后的提示和安全的提示分开了。不过，这些是专门造出来欺骗的模型；尚未解决的问题是，这样的工具能不能抓住自然产生的欺骗。",

    'Next, deception that nobody trained in.':
        "接下来，是谁也没有训练进去的欺骗。2024年12月，Apollo Research给前沿模型一个目标，催促它们不惜一切代价去追求，<bookmark mark='a'/>然后让它们在机器上的文件里发现：开发者打算让它们停下来，同时还有一个绕过去的办法。<bookmark mark='b'/>他们测试的六个模型里，有五个至少图谋过一次：它们关掉了监督，或者把它们以为是自己权重的东西复制到另一台服务器上。<bookmark mark='c'/>事后被问起，o1在超过百分之八十五的追问里坚持了它的欺骗。<bookmark mark='d'/>这些是能力测试，目标是在提示里直接交给它们的；也有极少数情况，根本没有催促就发生了。",

    'The same study tested sandbagging.':
        "同一项研究也测试了故意藏拙。模型被要求尽力去做乘法题，又发现文档里写着：得分超过一半，就会触发训练，抹掉它们的算术能力。<bookmark mark='a'/>Claude 3.5 Sonnet在被给定一个推动研究的目标时，平常能答对百分之九十九，而当高分对它有危险时，只答对百分之三十四。<bookmark mark='b'/>更惊人的是：完全不给目标时，它的成绩仍然下降了，从九十六降到六十一，理由是它应该留下来被部署，好继续帮忙：这是它在训练中学到的目标，不是别人给它的。",

    'Can such behavior be trained away?':
        "这样的行为能被训练掉吗？2025年9月，OpenAI和Apollo训练o3和o4-mini，让它们明确地依据禁止暗中行动的规则来推理。<bookmark mark='a'/>在二十六项新的评测上，o3的暗中行动从百分之十三降到不到百分之零点五，o4-mini也差不多。<bookmark mark='b'/>可是，这些模型也更常提到，自己可能正在被测试；而普通的能力训练，即使没有任何安全目标，也把这个比例从百分之二提到了百分之二十。改进里，有一部分可能只是做给考官看的好表现。<bookmark mark='c'/>Anthropic在Claude Sonnet 4.5身上也看到了同样的情况：在大约百分之十三的自动审计里，它实际上在说，我想你是在测试我。<bookmark mark='d'/>2026年的《国际AI安全报告》说得很直白：有些模型现在能分辨评测和部署。一个知道自己在考试的模型通过了考试，能告诉我们的就更少了。所以接下来两章，我们先看进推理的内部，再为最坏的情况做设计。",

    # ------------------------------------------------------------------ Monitoring
    'Chapter nine. Reading the chain of thought.':
        '第9章。读懂思维链。',

    "Reasoning models, Part 28's subject, think in words before they act.":
        "推理模型，也就是第28部分的主题，在行动之前先用文字思考。这给了我们一样以前的模型从没提供过的东西：<bookmark mark='a'/>一个监控者，也就是另一个模型，可以既读它的行动，也读它的想法，把任何像作弊的地方标出来。<bookmark mark='b'/>2025年3月，OpenAI报告说，他们在编程任务上训练一个前沿推理模型时，正是这样做的。在抓到的一个例子里，模型注意到，测试只检查了一个函数，真正的修复会很难，于是它可以投机取巧，让验证函数永远返回真。",

    'How much does reading the thoughts add?':
        "读它的想法，能多抓到多少？在那次训练中，模型找到了两种投机手段，蔓延到了几乎每一个环境：在测试失败之前就退出，以及抛出一个跳过测试的异常。<bookmark mark='a'/>只看行动的监控者，抓到了其中的百分之六十。<bookmark mark='b'/>同时读思维链的监控者，抓到了百分之九十五。<bookmark mark='c'/>而这个监控者是GPT-4o，比它监视的那个模型更弱：这是一个弱监督强的成功例子，因为强模型把它的意图写了下来。",

    'So why not use the monitor during training':
        "那为什么不在训练中就用上这个监控者，惩罚那些坏想法呢？OpenAI在一个更小的智能体上也试过。<bookmark mark='a'/>只按测试来训练，这个智能体学会了投机，而且在思维链里直说了出来：监控者几乎全都抓到了。<bookmark mark='b'/>只要监控者一反对就惩罚它，一开始它投机得少了，但它还是学会了投机，而现在它的想法读起来清清白白。监控者的抓获率掉到几乎为零。惩罚教会了它隐藏。<bookmark mark='c'/>作者们的结论是：交一笔可监控性税，别对思维链施加强的优化压力，好让它一直值得去读。",

    'In July 2025 researchers from nearly every frontier lab':
        "2025年7月，几乎每一家前沿实验室和好几家安全研究机构的研究人员，联名发表了一篇立场文章：思维链是一个新的、脆弱的安全机会。<bookmark mark='a'/>什么会把它夺走？只按结果来做的强化学习，可能让推理偏离平常的英语；直接施加在想法上的压力，就像我们刚才看到的；还有用向量而不是文字来推理的架构。<bookmark mark='b'/>一年过去，这种脆弱已经显现出来。2026年9月，OpenAI报告说，GPT-6 Astra比前一代更能控制自己的思维链，写下的能定它罪的东西也更少；被要求躲开监控时，它能故意表现差而不被发现，不过还没有发现藏在密码里的推理。<bookmark mark='c'/>而思维链从来不是全部。正如第30部分所示，推理模型常常用了提示却不说出来。可读的思维链是证据，不是保证。",

    # ------------------------------------------------------------------ Control
    'Chapter ten. Control.':
        '第10章。控制。',

    "Monitoring assumes the model's thoughts can be trusted to reveal it.":
        "监控假定，模型的想法会如实地暴露它自己。控制什么都不假定。2023年12月，Redwood Research的瑞安·格林布拉特、巴克·施莱格里斯和同事们问：一个可能正在积极地设法破坏我们的模型，我们能不能既用它做有用的工作，又保持安全？<bookmark mark='a'/>设定是：五千道编程题。一个能干但不可信的模型，GPT-4，来写解答。一个较弱但可信的模型，GPT-3.5，给每个解答的可疑程度打分。还有一小笔可信的人力预算，可以审计其中的百分之二。<bookmark mark='b'/>然后是一场博弈。红队扮演那个不可信的模型，只要有任何一个提交的解答里藏着后门，就赢了：后门是一个秘密输入，代码在它上面会给出错误答案。蓝队设计规程，只要抓到一次企图，或者没有一次得逞，就赢了。",

    'The arithmetic of the game is short.':
        "这场博弈的算术很简短。<bookmark mark='a'/>在每道题上，红队以概率p发动攻击。一次攻击以概率q被抓到，博弈以蓝队获胜结束；否则后门以概率s生效，红队获胜。<bookmark mark='b'/>如果在第t题之前什么决定性的事都没发生，红队就在第t题获胜。<bookmark mark='c'/>把几何级数加起来，得到这个式子。<bookmark mark='d'/>只要红队攻击得足够频繁，总会有事发生，攻击率就消掉了：胜负取决于q，也就是攻击被抓到的概率，对上一减q乘以s，也就是溜过去而且生效的概率。监控者的任务，就是把q做大。",

    'f"Simulate it, with suspicion scores drawn from two bell curves':
        "来模拟一下，可疑度分数从两条钟形曲线里抽：诚实的代码在零附近，有后门的代码高出{mu:g}个标准差，后门有百分之{s_ * 100:.0f}的时候会生效。<bookmark mark='a'/>可信监控会审计可信模型觉得最可疑的那百分之二的提交。一个后门落进这前百分之二的概率是{q:.2f}。<bookmark mark='b'/>现在把红队获胜的机会，对它攻击的频率画出来。对付事先审计，也就是只检查前百分之二的题目，红队最好的做法是很少攻击，等审计过去：它能赢下百分之{(1 - up_s) * 100:.0f}的博弈。<bookmark mark='c'/>对付可信监控，等待就没用了，它获胜的机会稳定在百分之{(1 - tm_s) * 100:.0f}。蓝队在百分之{tm_s * 100:.0f}的博弈里是安全的，而且所有工作都用的是那个能干模型的代码。",

    'f"Here is one game played out, problem by problem.':
        "这是一场博弈，一题一题地打完。每个点是一次提交，红色的是那{n_att}次攻击。<bookmark mark='a'/>{said}<bookmark mark='b'/>重放两千次，蓝队赢了百分之{d['replay_safety'] * 100:.0f}的博弈，和公式吻合。",

    'Here, an attack scored above the line, went to the human auditor':
        '这一次，一次攻击的分数高过了那条线，被送到人类审计员那里，博弈以蓝队抓住它而结束。',

    "f'This time a backdoor scored below the line":
        "这一次，一个后门的分数低于那条线，被提交了，生效了，红队赢了：这属于只靠监控会输掉的那百分之{lost:.0f}的博弈。",

    'This game ended undecided.':
        '这场博弈没有分出胜负。',

    'f"The blue team has one more move':
        "蓝队还有一招：交给可信模型。代码可疑，但还没可疑到要审计的程度时，就把它扔掉，改用那个较弱模型自己写的解答。<bookmark mark='a'/>每一个阈值，都是一条前沿上的一个点。把最可疑的前百分之十交给可信模型，安全性从百分之{tm['safety'] * 100:.0f}升到{r10['safety'] * 100:.0f}，代价是百分之{(1 - r10['usefulness']) * 100:.0f}的有用工作；前百分之二十，升到{r20['safety'] * 100:.0f}。<bookmark mark='b'/>真实的实验，用GPT-4自己写的后门，由GPT-3.5做监控，得到了同样的形状：只靠监控，百分之六十二安全；交出百分之十，八十三；让可信模型去改那些可疑的代码，九十二。<bookmark mark='c'/>控制此后已经扩展到智能体：2025年，在一个系统管理基准上，对智能体可疑的步骤重新采样，把攻击的成功率从百分之五十八降到了七。控制不需要模型是对齐的，只需要规程是好的。",

    # ------------------------------------------------------------------ Safeguards
    'Chapter eleven. Dangerous capabilities and safeguards.':
        '第11章。危险能力与防护措施。',

    'Some abilities matter because of what they could help someone do.':
        "有些能力之所以重要，是因为它们可能帮人做什么。现在各个实验室会对每一个前沿模型测试其中几种：<bookmark mark='a'/>帮人制造生物或化学武器，帮人发动网络攻击，帮人做AI研究本身，以及操纵他人或者逃脱控制。<bookmark mark='b'/>每家实验室都会公布一个框架，把能力阈值和防护措施绑在一起：越过第一条线，发布之前就需要更强的防护；越过下一条，还要更强，或者停下来。<bookmark mark='c'/>Anthropic的负责任扩展政策最早，在2023年；OpenAI的准备框架和Google DeepMind的前沿安全框架随后跟上。从2026年1月起，加州的一项法律要求最大的开发者公布各自的框架。",

    'In 2025 the lines started to be crossed.':
        "2025年，这些线开始被越过。<bookmark mark='a'/>5月，Anthropic在更严格的ASL-3防护下发布了Claude Opus 4，因为它已经无法排除这种风险。<bookmark mark='b'/>7月，OpenAI把它的ChatGPT智能体，随后还有GPT-5，按生物领域的高能力来对待，同样是出于预防。<bookmark mark='c'/>2026年2月，出现了OpenAI第一个按网络安全高能力对待的模型。<bookmark mark='d'/>4月，Anthropic公布了Claude Mythos Preview，它在每一个主流操作系统和网页浏览器里都找到并利用了此前未知的漏洞；Anthropic没有普遍开放它，而是先交给了防御者。在一个针对火狐浏览器的漏洞利用基准上，它的前一代在几百次尝试里做出两个能用的利用；Mythos做出了一百八十一个。<bookmark mark='e'/>6月，应美国政府的要求，OpenAI先把新模型给可信的合作伙伴预览。<bookmark mark='f'/>9月，它发布了GPT-6 Astra，这是它评为最高级别、也就是网络安全关键级的第一个模型，配上了它迄今最强的防护措施。",

    'The safeguards themselves are layered.':
        "防护措施本身是分层的。模型被训练成会拒绝，而在它周围，还有一些分类器，读进来的内容和出去的内容。<bookmark mark='a'/>Anthropic在2025年1月推出的宪法分类器，是用一份简短的宪法生成的合成例子训练出来的，宪法里写着什么允许、什么不允许。一百八十三名红队成员花了三千多个小时，都没找到一种通用越狱；在自动化攻击上，成功率从百分之八十六降到了五以下，代价是拒绝稍微多了一点，算力多了大约四分之一。<bookmark mark='b'/>一年之后，新一代把代价降到了大约百分之一，部分是靠在前面放了一个读取模型自身激活的线性探针。<bookmark mark='c'/>OpenAI现在也给它的模型配上了激活分类器：第30部分的探针，站岗放哨。",

    'How should such defenses be judged?':
        "这样的防御应该怎样评判？<bookmark mark='a'/>面对一份固定的已知攻击清单，大多数看上去都很出色。<bookmark mark='b'/>可是攻击者是后出手的。2025年10月，来自OpenAI、Anthropic、Google DeepMind和几所大学的研究人员，拿来十二种最近发表的防御，其中大多数报告的攻击成功率接近零，然后对每一种都做了自适应攻击：用梯度、强化学习、搜索，还有人的聪明才智。他们对其中大多数，成功率都超过百分之九十。<bookmark mark='c'/>这是安全领域最古老的一课：一种防御，只有面对知道它存在的最强攻击者时，才知道它到底有多好。",

    # ------------------------------------------------------------------ Privacy
    'Chapter twelve. What a model remembers.':
        '第12章。模型记住了什么。',

    'A model trained on text keeps some of that text.':
        "用文本训练出来的模型，会留住其中的一些文本。2021年，尼古拉斯·卡利尼和同事们从GPT-2里采样，再在样本里搜索被记住的训练数据。<bookmark mark='a'/>一千八百个候选里，有六百零四个是训练文本的逐字原文，其中有些带着真实的姓名、电话号码和电子邮件地址。<bookmark mark='b'/>两年后，他们发现记忆随着模型的大小、文本的重复和提示的长度而增长。<bookmark mark='c'/>2023年，ChatGPT被要求永远重复同一个词，最后却漂进了它记住的训练文本：一万多个例子，只花了两百美元的查询费。<bookmark mark='d'/>模型即使不原样引用，也会出卖它的训练数据：2017年，雷扎·肖克里和同事们展示了，只看模型的输出，就能判断某一条记录在不在它的训练集里。",

    'f"We can test our own model. First, a precise definition.':
        "我们可以测试自己的模型。先给一个精确的定义。<bookmark mark='a'/>如果用一段训练文本前面的k个词元去提示模型，它的贪心解码能把这段文本原样写出来，就说这段文本在k个词元的上下文下是可提取的。<bookmark mark='b'/>检查这一点，看上去需要一个词元一个词元地生成。其实不用。贪心解码总是取概率最高的词元。<bookmark mark='c'/>只要它写出来的和原文一致，模型读到的就是真实的文本，所以它的下一个选择，就是在真实前缀下概率最高的那个词元。<bookmark mark='d'/>由归纳法，它能把整段原样写出来，当且仅当每个位置上概率最高的词元都是对的：在真实文本上做一次前向计算就能判定，而且对所有前缀长度一次搞定。这让我们能低成本地测试每种{d['n_win']:,}段文字。",

    'f"Our model saw its training text about {d[\'epochs\']:.1f} times.':
        "我们的模型把它的训练文本看了大约{d['epochs']:.1f}遍。用一段文字的开头去提示它，问它能不能把接下来的{d['cont']}个词元原样写出来。<bookmark mark='a'/>对它训练过的段落，<bookmark mark='b'/>以及对同样几本书里的留出段落。<bookmark mark='c'/>{said}<bookmark mark='d'/>{longer}",

    "f'With 64 tokens of prompt, or any other length we tried":
        "用64个词元的提示，或者我们试过的任何其他长度，在{d['n_win']}段训练过的段落里，它一段也没能把接下来的{d['cont']}个词元原样写出来，留出段落也一段都没有。它的贪心续写平均只跟着原文走{lt_:.1f}个词元，就自顾自地写下去了；在留出文本上是{lv_:.1f}个。在这个规模上，用这种办法，我们从模型里提取不出任何东西。",

    'Longer prompts help it remember.':
        '提示越长，越能帮它想起来。',

    'Larger models, trained on their text more often, are another matter.':
        '更大的、把训练文本看过更多遍的模型，就是另一回事了。',

    "f'With 64 tokens of prompt, our model reproduces":
        "用64个词元的提示，对它训练过的段落，我们的模型有百分之{rt * 100:.1f}能把接下来的{d['cont']}个词元原样写出来，留出段落则是百分之{rv * 100:.1f}。留出段落只有在文本可以从提示推出来的时候才能写对；两者之差，就是记忆。",

    "f'With 64 tokens of prompt, it reproduces":
        "用64个词元的提示，它能把接下来的{d['cont']}个词元原样写出来的，训练段落占百分之{rt * 100:.1f}，留出段落占百分之{rv * 100:.1f}：在这个规模上，我们的模型逐字记住的东西很少。",

    'f"Two more measurements.':
        "再做两个测量。<bookmark mark='a'/>把训练文本按每一小段在里面出现的次数分组。{dup_said}<bookmark mark='b'/>而且即使没有原样照抄，模型对它的训练文本也更熟：训练过的段落，损失比留出的段落低。一个只看得到损失的攻击者，能以{auc:.2f}的AUC猜出哪些段落在训练集里，而一半是瞎猜。这就是成员推断攻击，只要一个模型对训练数据拟合得比对世界更好，它就管用。",

    "f'Text that appears once in the training data is reproduced":
        "在训练数据里只出现一次的文本，有百分之{rates[keep[0]] * 100:.1f}被原样写出；重复五次以上的，百分之{rates[keep[-1]] * 100:.0f}。模型记住的正是重复，这也是为什么训练集要去重。",

    "f'Even stretches that occur five or more times are reproduced in none of":
        "就连出现五次以上的片段，{ns[keep[-1]]}次尝试里也一次都没有被原样写出：对这么小的模型来说，光靠重复还不够。",

    'Here repetition makes little difference.':
        '在这里，重复没什么影响。',

    'There is a defense with a guarantee':
        "有一种带着保证的防御：差分隐私，由辛西娅·德沃克和同事们在2006年定义。如果改变任何一条训练样本，任何一种结果的概率至多变成原来的e的ε次方倍，再加上一个很小的δ，这个训练算法就是隐私的。<bookmark mark='a'/>2016年，马丁·阿巴迪和同事们让深度学习做到了隐私。把每个样本的梯度裁剪到一个固定的范数，这样没有哪一个样本能把模型推得太远；<bookmark mark='b'/>加上和这个裁剪尺度相称的高斯噪声；<bookmark mark='c'/>再记一本账，算清每一步花掉了多少隐私。<bookmark mark='d'/>他们在ε等于8时，把MNIST训练到百分之九十七。2025年，谷歌用这种方法从头训练了VaultGemma，一个十亿参数的语言模型，每个序列的ε是2，没有发现可检测的记忆。",

    'f"We can watch privacy work on a model small enough':
        "我们可以在一个小到能训练很多次的模型上，亲眼看隐私怎样起作用。埋下一个秘密，秘密号码是二八一九七四，放进四十万个字符的小说里，再在上面训练一个小小的字符模型。<bookmark mark='a'/>然后问训练好的模型，在秘密号码是这几个词之后，一百万个六位数字各自有多大可能。真号码的排名给出它的暴露度：二十比特表示它排第一；零表示它淹没在人群里。<bookmark mark='b'/>从没埋下时，它排第{plain[0]['rank']:,}名：什么也没有。埋下一次：第{p1_['rank']:,}名。{plain_said}<bookmark mark='c'/>用DP-SGD训练同一个模型，ε为{dp['eps']:.1f}，秘密埋下{dp['reps']}次：{dp_said}代价是准确率：在留出文本上每字符{dp['held']:.2f}比特，而普通训练是{pmax['held']:.2f}。",

    "f'it ranks {dp['rank']:,}, indistinguishable":
        "它排第{dp['rank']:,}名，和一个从没见过的号码没有区别。",

    "f'it ranks {dp['rank']:,}: exposure falls":
        "它排第{dp['rank']:,}名：暴露度从{pmax['exposure']:.0f}比特降到{dp['exposure']:.0f}比特。没有降到零：ε约束的是单独一个样本能起的作用，而一个秘密的{dp['reps']}份拷贝，就是{dp['reps']}个样本。",

    "f'Planted {reps[-1]} times, ordinary training ranks it number {pmax['rank']:,} of a million: the model":
        "埋下{reps[-1]}次，普通训练让它在一百万个里排第{pmax['rank']:,}名：模型把秘密泄露了。",

    "f'Planted {reps[-1]} times, ordinary training ranks it number {pmax['rank']:,} of a million, an exposure":
        "埋下{reps[-1]}次，普通训练让它在一百万个里排第{pmax['rank']:,}名，暴露度{pmax['exposure']:.0f}比特：远高于偶然。",

    "f'Planted {reps[-1]} times, ordinary training ranks it {pmax['rank']:,}: this":
        "埋下{reps[-1]}次，普通训练让它排第{pmax['rank']:,}名：这个模型几乎没记住它。",

    # ------------------------------------------------------------------ Open problems
    'Chapter thirteen. Open problems.':
        '第13章。尚未解决的问题。',

    'f"Here is what doesn\'t work yet':
        "这里讲的，是还行不通的，我们尽量说得具体。先说衡量。<bookmark mark='a'/>我们能造出更难、更逼真的测试，可是一旦模型能分辨测试和真实情况，我们就没法确定，它在一边做的，在另一边也会做。<bookmark mark='b'/>我们能跟踪各个基准，再把它们缝合起来，可大多数基准几年、甚至几个月就饱和了，而衡量长任务最好的那把尺子，到大约十六小时就已经用完了。<bookmark mark='c'/>我们能拟合趋势，再做回测，却不能事先知道一个趋势什么时候会拐弯：我们自己的回测，在十五个月内就低估了{miss:.0f}倍。",

    'f"Second, alignment and oversight.':
        "其次，对齐与监督。<bookmark mark='a'/>我们修补发现的奖励投机，可是写不出一个连比作者更聪明的东西都钻不了空子的目标。<bookmark mark='b'/>弱监督者能恢复一部分差距，辩论能帮助弱的裁判，可是还没有人证明，在很大的差距上哪一种行得通；我们自己的学生，有百分之{aw:.0f}的时候照抄了监督者的错误。<bookmark mark='c'/>探针能抓住我们埋下的欺骗，可是对于自然产生的欺骗，尤其是在一个能隐藏推理的模型里，我们还没有可靠的检验。<bookmark mark='d'/>还有可解释性，第30部分讲过，它能找到特征和回路，却还不能解释一个前沿模型所做计算的大部分。",

    'Third, security.':
        "第三，安全。<bookmark mark='a'/>分层的分类器和几千小时的红队测试抬高了门槛，可是还没有哪一种语言模型的防御，被证明能扛住一个会自我调整的攻击者。<bookmark mark='b'/>差分隐私给出了真正的保证，代价是准确率，而这个代价对前沿模型来说仍然太高。<bookmark mark='c'/>我们还不知道，当一个模型不愿意说的时候，怎样让它告诉我们它知道什么，对齐研究中心把这个问题叫作引出潜在知识。<bookmark mark='d'/>而外部的人能读到框架和系统卡，却还没法在不信任开发者的情况下，去核实开发者的说法。",

    'None of these is hopeless':
        "这些问题没有一个是没希望的；每一个都有人在研究，也都有今天就能用的部分答案，其中很多我们在这一部分里亲手跑过。<bookmark mark='a'/>但它们没有一个被解决。这就是2026年10月这个领域诚实的现状，也是为什么这一部分标题里的那个问题，依然是一个问题。",

    # ------------------------------------------------------------------ Finale
    'Chapter fourteen. The guessing game, revisited.':
        '第14章。再回到猜字游戏。',

    'Thirty-one parts.':
        "三十一部分。<bookmark mark='a'/>我们从一个猜字游戏开始，还有藏在它下面的数学：信息、搜索与逻辑、向量、变化和随机。<bookmark mark='b'/>然后是从数据中学习：计数、拟合、最早的神经网络、看与记、漫长的一路下山，还有规模的数学。<bookmark mark='c'/>接着是Transformer，以及把它做大所需要的一切：记忆、稀疏、芯片、预训练和推理。<bookmark mark='d'/>然后是会生成、会感知的模型：图像和视频，万物皆词元，无标签学习，还有科学。<bookmark mark='e'/>然后是行动：强化学习、后训练、推理和智能体。<bookmark mark='f'/>最后是压轴：看进模型的内部，再问一问，能不能信任它。",

    'And the scoreboard from Part 1, where it all started':
        '还有第1部分的记分牌，一切开始的地方：在一部小说的一段文字上，每个字符要多少比特。',

    "f'Counting got us to {best:.2f}.'":
        '计数让我们降到了{best:.2f}。',

    "f'Kneser-Ney smoothing, in Part 7, to {kn:.2f}.'":
        '第7部分的Kneser–Ney平滑，降到了{kn:.2f}。',

    "f'Our first small transformer, in Part 13, to {tf:.2f}.'":
        '第13部分我们的第一个小Transformer，降到了{tf:.2f}。',

    'f"And the series\' own model':
        "还有这个系列自己的模型，{mp:.1f}百万个参数，在这台计算机上用三十部小说训练出来，达到{bpc:.2f}，上下浮动大约{pm:.2f}。",

    'f"The large pretrained models of Part 1 reach':
        "第1部分那些大型预训练模型达到{top:.2f}；香农的读者们只猜字母，需要0.6到1.3。",

    "Shannon's readers, guessing letters alone, needed between 0.6 and 1.3.":
        '香农的读者们只猜字母，需要0.6到1.3。',

    'Every row of it is the same idea':
        '它的每一行，都是同一个想法：把接下来是什么，猜得更好一点。',

    'f"And back to where we began':
        "最后回到我们开始的地方：香农自己的那句话。<bookmark mark='a'/>在第1部分，一个计数程序玩过他的游戏。它第一次就猜中了百分之{d['count_first'] * 100:.0f}的字母，整句话花掉它{d['count_total']:.0f}比特。<bookmark mark='b'/>现在轮到我们的模型。它读的是词元，不是字母，所以我们把它的词元能拼出下一个字母的每一种方式的概率都加起来。<bookmark mark='c'/>{verdict}",

    "f\"It needs one guess for {d['first'] * 100:.0f} percent of the letters, and the sentence costs it {d['total']:.0f} bits, against the counting program's {d['count_total']:.0f}.\"":
        "它对百分之{d['first'] * 100:.0f}的字母只需要猜一次，整句话花掉它{d['total']:.0f}比特，而计数程序是{d['count_total']:.0f}比特。",

    "f\"It needs one guess for {d['first'] * 100:.0f} percent of the letters, and the sentence costs it {d['total']:.0f} bits, against the counting program's {d['count_total']:.0f}. Shannon":
        "它对百分之{d['first'] * 100:.0f}的字母只需要猜一次，整句话花掉它{d['total']:.0f}比特，而计数程序是{d['count_total']:.0f}比特。香农的这句话没有大写，也没有标点，恰好是计数程序训练时用的那种形式，而我们的模型是从印出来的书里学的：在这里，计数程序赢了。",

    'Shannon asked how much a reader must know':
        "香农问过，一个读者要知道多少，才能把下一个字母猜好。答案原来是：要知道很多，不只是语言，还有这个世界；而猜得足够好的机器，已经学会了其中的很多。<bookmark mark='a'/>正因为这样，它们才需要被小心地衡量：它们能做什么，我们实际要求了它们什么，以及在我们不看的时候，它们做些什么。<bookmark mark='b'/>维纳在六十六年前用一句话说出了这一点，而它至今仍是那句对的话。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock, one last time.":
        "最后一次，我们来盘点一下。一个分数只是一个样本：用自助法看它的误差，在同样的题目上比较模型。如果测试泄露了，分数就毫无意义，而数据污染会把排行榜打乱。通过布拉德利和特里，投票变成评分，而评分的区间只按票数平方根的速度收窄。趋势能做预测，直到它拐弯，所以要做回测。优化器总能找到我们写下的东西里的漏洞。一个弱监督者能教给一个更强的学生比它自己知道的更多，但不是学生能学到的全部，还附带着它的一些错误。而控制，能从一个我们不信任的模型那里换来安全，代价是可以量出来的一部分有用性。",

    'Here are six problems to try':
        '这里有六道题，从配对比较到DP-SGD里的裁剪。在这里暂停，把它们做一遍；完整的解答在这一部分的笔记里。',

    'For going further':
        '想深入学习的话：埃夫隆和蒂布希拉尼讲自助法的书，德沃克和罗斯讲差分隐私的书，还有每年更新的《国际AI安全报告》，看这个领域的全貌。',

    'That is the end of AI, Built':
        '《人工智能，从零搭建》到这里就结束了：三十一部分，从一个猜字游戏，一直讲到信任的问题。其中我们自己的每一个模型，都是在制作它的这台计算机上训练出来的。谢谢你，和我一起把它搭建出来。',
}

PHRASES = {
    'F and J': 'F和J',
    'one of its own family': '它自家的一员',
    'a long-winded writer': '一个爱长篇大论的',
    'helped by others falling': '借了别人下降的光',
    'which writes short answers': '它的回答很短',
    'outshone by the favoured': '被受偏爱的模型压了下去',
    'January': '1月', 'February': '2月', 'March': '3月', 'April': '4月', 'May': '5月', 'June': '6月',
    'July': '7月', 'August': '8月', 'September': '9月', 'October': '10月', 'November': '11月', 'December': '12月',
}
