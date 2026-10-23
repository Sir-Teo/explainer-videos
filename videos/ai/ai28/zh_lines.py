"""Chinese narration for ai28: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第28部分：推理'

CHAPTERS = {
    'Hook': '从"一步一步地思考"到o1和R1',
    'Chain': '1. 出声思考，就是计算',
    'Vote': '2. 很多条思维链，一次投票',
    'Verify': '3. 检查每一步',
    'RL': '4. 向检查器学习',
    'GRPO': '5. 推导GRPO',
    'Variants': '6. 后继者们',
    'Entropy': '7. 熵坍缩',
    'Length': '8. 该想多久',
    'PassK': '9. 更锐利，还是更宽广？',
    'TestTime': '10. 回答时的思考',
    'Search': '11. 在思路中搜索',
    'Latent': '12. 不用文字的思考',
    'Formal': '13. 机器能检查的证明',
    'ARC': '14. 没人见过的谜题',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'In January 2022, a team at Google tried something simple.':
        "2022年1月，谷歌的一个团队试了一件很简单的事。他们不再给大语言模型看几道题和它们的答案，而是给它看8道题，"
        "解题过程都写了出来。<bookmark mark='a'/>在小学数学应用题上，谷歌5400亿参数的PaLM，正确率从18%升到了57%："
        "它自己写出了解题过程，答对的多了很多。<bookmark mark='b'/>四个月后，东京和谷歌的一个团队发现，连例子都不需要。"
        "只要一句话，“让我们一步一步地思考”，就让OpenAI的一个模型在算术应用题上从18%提高到79%。"
        "<bookmark mark='c'/>这种能力本来就在模型里。只是需要有人让它把推理写下来。",

    'For two years that was the method:':
        "之后两年，方法就是这样：要求写出思维链，采样几条，也许再投个票。然后，2024年9月，OpenAI发布了o1，"
        "它被用强化学习训练成先思考、再回答。<bookmark mark='a'/>在2024年的美国数学邀请赛，也就是AIME上，"
        "GPT-4o只做对了12%的题。<bookmark mark='b'/>o1只试一次就做对74%，64次投票做对83%，"
        "让一个学来的打分器从1000个答案里挑，做对93%。<bookmark mark='c'/>2025年1月，DeepSeek公开了做法。"
        "R1-Zero：直接从基础模型开始做强化学习，只在答案正确时给奖励。它从16%升到了71%，投票后到87%，而且权重是公开的。"
        "<bookmark mark='d'/>2025年7月，有系统在国际数学奥林匹克上写出了金牌水平的解答，用的是普通语言，在规定时间之内。"
        "<bookmark mark='e'/>然而，2026年3月，一套模型从没见过的游戏ARC-AGI-3发布时，所有前沿模型的得分都不到1%，"
        "而人能解出全部。",

    'That is the question of this part: how does a model learn to think':
        "这就是这一部分的问题：模型是怎样学会思考的？思考又能换来什么？<bookmark mark='a'/>我们沿着这个领域自己走过的路："
        "为什么写出思维链就能增加计算；采样很多条思维链再投票；检查每一步；向一个检查答案的检查器学习的强化学习，"
        "一步步推导；想得更久能换来什么；搜索；以及机器能检查的证明。<bookmark mark='b'/>而且每个想法都会在这里试一试，"
        "用的是在制作这个视频的电脑上训练的小模型。",

    'This is Part 28 of AI, Built, the third part of the act on agency.':
        "这是《人工智能，从零搭建》的第28部分，也是“智能体”这一幕的第三部分。<bookmark mark='a'/>这一部分讲："
        "为什么写出步骤能增加计算；很多条思维链和一次投票，以及检查步骤而不只检查答案；向检查器学习的强化学习，"
        "推导GRPO和它的后继者；这种训练对模型做了什么：对它的不确定性，对它想多久，对它到底能解出什么；"
        "回答时怎样花计算；还有前沿：不用文字的思考，微型递归模型，形式化证明，以及没有模型见过的谜题。",

    # ------------------------------------------------------------------ Chain
    'Chapter one. Thinking out loud is computing.':
        '第1章。出声思考，就是计算。',

    'f"Here\'s a puzzle for a small transformer: sixteen bits.':
        "给一个小Transformer出一道题：16个比特，其中1的个数是奇数吗？<bookmark mark='a'/>如果训练它直接给出答案，"
        "我们这个两层的模型，只有{100 * np.mean(d16):.0f}%的时候答对：{coin}。<bookmark mark='b'/>现在，"
        "把同一个模型训练成先写出过程：沿着这些比特一路数过去，到目前为止，1的个数是奇数吗？每一步都很简单，"
        "只要上一步的答案，再加一个比特。<bookmark mark='c'/>它的最终答案，{100 * np.mean(c16):.0f}%都是对的。"
        "同样的模型，同样的大小。它只不过是可以出声思考了。",

    'Why does writing help? Look at the computation.':
        "写出来，为什么有用？看看其中的计算。Transformer让每个词元都穿过同一叠固定的层。<bookmark mark='a'/>"
        "直接回答时，一个接一个发生的最长计算步骤链，只有这叠层那么高：L层，不管问题有多难。<bookmark mark='b'/>"
        "但它写出的词元，会作为输入再送回去。<bookmark mark='c'/>于是步骤链可以爬上这叠层，再下来，再爬上去，"
        "每个词元一次。有k个思考词元，就有L乘以k加1步可以接连进行。写出的词元既是草稿纸，也是一只时钟："
        "每写一个，就多换来一次穿过网络的计算。",

    'Theory makes this precise.':
        "理论把这一点说得很精确。<bookmark mark='a'/>2023年，威廉·梅里尔和阿希什·萨巴瓦尔证明：一个深度固定、"
        "直接作答的Transformer，能计算的只是常数深度的阈值门电路能计算的东西，这一类叫TC0。<bookmark mark='b'/>"
        "被认为在它之外的问题，需要随输入增长的深度：把一长串五个物体的置换复合起来，就是经典的例子。"
        "<bookmark mark='c'/>思维链解除了这个限制。有T个思考词元，常数深度的Transformer就能模拟任何规模为T的电路；"
        "有多项式多个，它能判定的正好是计算机在多项式时间内能解的问题。<bookmark mark='d'/>有一点必须老实说："
        "奇偶性本身在TC0里面。深度固定的网络原则上能算它；我们的实验里失败的是学会它，因为每一个比特都会翻转答案。",

    '"Is it the extra tokens, or what\'s in them?':
        "是多出来的词元在起作用，还是它们的内容？给模型同样多的额外位置，填上没有意义的点，训练它在这些点之后作答。"
        "<bookmark mark='a'/>在16个比特上，{said_}<bookmark mark='b'/>雅各布·普福、梅里尔和萨姆·鲍曼2024年发现，"
        "点可以在能拆成相互独立的并行小块的问题上起作用，而且模型需要密集的监督才能学会用它们。",

    'f"the dots don\'t help:':
        "这些点没有帮助：{100 * fd:.0f}%，并不比直接回答好。每个点都是输入，不是输出；它增加了可以计算的位置，"
        "但信息不会从一个位置的顶层流到下一个位置的底层。起作用的是写出的步骤，而不是多出来的长度。",

    "f'the dots help a little,":
        "这些点有一点帮助，{100 * fd:.0f}%，相比之下直接回答是{100 * dd:.0f}%：更多的位置带来更多的并行计算。"
        "但信息不会从一个位置的顶层流到下一个位置的底层，而写出的思维链达到{100 * cd:.0f}%，完全是另一个水平。",

    'f"Here are all our runs, on strings of four, eight and sixteen bits.':
        "这是我们全部的运行结果，字符串长4、8和16个比特。<bookmark mark='a'/>直接回答，在4个比特上{verdict(d[0])}，"
        "8个比特上{verdict(d[1])}，16个比特上{verdict(d[2])}。<bookmark mark='b'/>点的结果跟着一起往下掉。"
        "<bookmark mark='c'/>先写出累计奇偶性的话，三种长度全都{('solved' if min(c) > 0.95 else 'much better')}，"
        "每一次运行都是如此。",

    'f"Here is the training at sixteen bits, replayed.':
        "这是16个比特上的训练过程，回放一遍。左边是每个模型训练时的正确率，每种各跑3次。右边是模型为三个字符串写出的"
        "思维链，逐个比特检查。<bookmark mark='a'/>一开始，思维链是一团噪声。<bookmark mark='b'/>{grow}"
        "<bookmark mark='c'/>{floor}思维链不只是更强大；它还更容易学，因为每一步都是一个局部的小问题。",

    'Answering at once never gets off the floor.':
        '直接回答始终没能离开地面。',

    "f'Answering at once ends at":
        '直接回答最后停在{100 * dfin:.0f}%。',

    "f'Then it learns the first few steps, and the right stretch grows along the string, one position after another:":
        '接着它学会了前几步，正确的一段沿着字符串一位一位地变长：到第{first:,}步，三条思维链全对了。',

    'Then it learns the first few steps, and the right stretch grows along the string.':
        '接着它学会了前几步，正确的一段沿着字符串变长。',

    # ------------------------------------------------------------------ Vote
    'Chapter two. Many chains, one vote.':
        '第2章。很多条思维链，一次投票。',

    'f"For the next chapters we need a model that can choose to think.':
        "接下来几章，我们需要一个能选择要不要思考的模型。这就是我们的模型，在这台电脑上训练的。<bookmark mark='a'/>"
        "题目是一串2到9个数字，答案是它们的和。<bookmark mark='b'/>模型可以先思考：它写一个思考词元，然后写出加上每个数字之后的"
        "累计和，再写答案。<bookmark mark='c'/>它也可以直接回答。训练中它两种都见过，还见过中途截断的思维链，"
        "所以它可以在任何一步停止思考。<bookmark mark='d'/>按温度1采样，让它直接回答，2个数字的题它答对"
        "{100 * acc_d[0]:.0f}%，9个数字的题答对{100 * acc_d[-1]:.0f}%。让它思考，则是{100 * acc_t[0]:.0f}%和"
        "{100 * acc_t[-1]:.0f}%。每一步思考都只是一个小加法，但小加法也会偶尔出错，而错一步，整条思维链就坏了。",

    'In March 2022, two months after chain-of-thought prompting, Xuezhi Wang':
        "2022年3月，思维链提示问世两个月后，谷歌的Xuezhi Wang和同事问：既然一条思维链可能出错，为什么不采样好几条，"
        "然后投票？他们把它叫作自洽性；在小学数学题上，它比单条思维链多了18个百分点。<bookmark mark='a'/>直觉是："
        "从不同路线得到同一个答案，就是这个答案正确的证据。<bookmark mark='b'/>而错误往往是分散的："
        "错的思维链很少会错到同一个答案上。<bookmark mark='c'/>而且它根本不需要检查器，只需要答案。",

    'f"Here is one {len(digits)}-digit list':
        "这是一串{len(digits)}个数字，以及我们的模型被要求思考时，为它写出的64条思维链中的8条。每一步按它是否等于"
        "真实的累计和来上色。<bookmark mark='a'/>{some}<bookmark mark='b'/>现在把64个答案全部统计一下。"
        "其中{100 * p_right:.0f}%是正确的和，{truth}；{scatter}<bookmark mark='c'/>{verdict}",

    "f'the wrong ones scatter over":
        '错误的答案分散在{n_wrong_vals}个不同的数值上。',

    "f'the wrong ones fall on just":
        '错误的答案只落在{n_wrong_vals}个数值上。',

    "f'{n_ok} of these eight end on the right sum. The others stopped thinking part-way":
        "这8条里有{n_ok}条最后得到了正确的和。其余的想到一半就停了，从那里直接给出答案：半途而废的思维链，就是在猜。",

    "f'{n_ok} of these eight end on the right sum. The others slipped somewhere":
        "这8条里有{n_ok}条最后得到了正确的和。其余的在某处出了错，而且一步出错会一直传到最后："
        "之后的每个累计和都差同样多。",

    "f'{n_ok} of these eight end on the right sum. Of the others,":
        "这8条里有{n_ok}条最后得到了正确的和。其余的里面，{n_short}条想到一半就停了，从那里直接给出答案；"
        "{n_slip}条在某一步出了错，而这个错会一直传到最后。",

    'All eight of these end on the right sum.':
        '这8条全部得到了正确的和。',

    "f'So the most common answer, the vote, is {top}: right.":
        '所以最常见的答案，也就是投票的结果，是{top}：正确。',

    "f'Here the most common answer is {top}, and the vote is wrong.":
        '这里最常见的答案是{top}，投票的结果是错的。',

    'When does voting work? Call the right answer y star':
        "投票什么时候管用？把正确答案叫作y星，它的概率叫p星。<bookmark mark='a'/>当正确答案出现的次数比每一个错误答案都多时，"
        "投票就是对的。<bookmark mark='a2'/>拿它和一个错误答案y比：两者出现次数之差，是k次独立抽取之和，"
        "每次是加1、0或减1，均值是k乘以p星减p y。<bookmark mark='b'/>由霍夫丁不等式，错误答案追上来的概率，"
        "随k指数地下降。<bookmark mark='c'/>所以随着票数增加，如果正确答案是模型最可能给出的那一个，投票以概率1正确；"
        "如果某个错误答案更可能，投票以概率1出错。<bookmark mark='d'/>投票只能放大模型本来就偏爱的东西。"
        "如果模型最喜欢的答案是错的，投票救不了这道题。",

    'f"Here it is on three hundred questions.':
        "这是在300道题上的结果。<bookmark mark='a'/>一条思维链答对{100 * tv[0]:.0f}%。对{ks[-1]}条思维链投票："
        "{100 * tv[-1]:.0f}%。<bookmark mark='b'/>推导也预言了它会在哪里趋平：最常见答案正确的题目所占的比例，"
        "{100 * lim:.0f}%。<bookmark mark='c'/>如果有东西能检查答案，那么{ks[-1]}条里只要有一条对就算对："
        "{100 * tp[-1]:.0f}%。{gap_said}<bookmark mark='d'/>{direct_said}",

    "f'The gap between the two curves is what a checker is worth: wide at a few samples,":
        "两条曲线之间的差距，就是一个检查器的价值：样本少时差距很大，{ks[gi]}个样本时差{100 * (tp[gi] - tv[gi]):.0f}个百分点，"
        "到{ks[-1]}个时几乎合上了。",

    'The gap between the two curves is what a checker is worth.':
        "两条曲线之间的差距，就是一个检查器的价值。",

    'f"Voting over answers given at once reaches only':
        "对直接给出的答案投票，只能达到{100 * dv[-1]:.0f}%：对更多的题目，模型直接回答时最喜欢的答案是错的，"
        "投票没法纠正。思维链让正确答案成为最可能的那个，然后投票再把它放大。",

    'f"Voting over answers given at once does about as well here,':
        "对直接给出的答案投票，在这里效果差不多，{100 * dv[-1]:.0f}%：在这个任务上，模型最喜欢的答案两种方式下往往都是对的。",

    # ------------------------------------------------------------------ Verify
    'Chapter three. Checking the steps.':
        '第3章。检查每一步。',

    'f"A checker of answers sees only the end.':
        "检查答案的检查器只看得到结尾。<bookmark mark='a'/>这里有一条思维链，5加3写成了9，然后加8写成了16。"
        "两个错误，正好抵消：最后的和是对的。<bookmark mark='b'/>检查答案的检查器会奖励它。检查步骤的检查器会标出其中两步。"
        "<bookmark mark='c'/>这种情况有多常见？在我们模型答对的题里，有{100 * rb:.1f}%途中有一步是错的。{small}",

    'Small here, because two slips must cancel exactly.':
        "这里很少，因为两次失误必须正好抵消。在很长的数学论证里，一段错误论证的结尾出现正确数字的情况要常见得多，"
        "而奖励它，教的是错误的东西。",

    'And in long mathematical arguments, a right number at the end of a broken argument is more common still;':
        "而在很长的数学论证里，一段错误论证的结尾出现正确数字的情况还要更常见；奖励它，教的是错误的东西。",

    'So there are two kinds of learned grader.':
        "所以，学来的评分器有两种。<bookmark mark='a'/>结果奖励模型读完整个解答，预测它的最终答案是否正确。"
        "它用每个解答一个标签来训练，这个标签检查答案的检查器就能提供。<bookmark mark='b'/>过程奖励模型评判每一步："
        "在前面几步的基础上，这一步对吗？一个解答的得分是各步的乘积，也就是所有步骤都对的概率。它需要每一步都有标签。"
        "<bookmark mark='c'/>两者都可以用来重新排序：采样N个解答，留下它打分最高的那个。也可以把它的分数当作强化学习的奖励。",

    'The idea of a learned grader came with the grade-school maths benchmark itself.':
        "学来的评分器这个想法，和小学数学基准本身同时出现。<bookmark mark='a'/>2021年，OpenAI的卡尔·科布和同事训练了一个"
        "验证器，从100个采样出来的解答里挑一个，发现它的作用相当于一个大30倍的模型。<bookmark mark='b'/>2022年，"
        "DeepMind的Jonathan Uesato和同事比较了两种反馈。结果反馈用更少的标签，得到的最终答案差不多一样好；"
        "但要让正确答案里面的推理也是对的，他们需要过程反馈，或者一个学着模仿它的评分器。<bookmark mark='c'/>2023年，"
        "OpenAI的《让我们一步一步地验证》花钱请人标注了80万个步骤。<bookmark mark='d'/>对竞赛题的1860个解答重新排序，"
        "多数投票解出69.6%，结果评分器72.4%，过程评分器78.2%。",

    'f"We can run the comparison on our adding model.':
        "我们可以在自己的加法模型上做这个比较。取它被要求思考时写出的8000个解答。一个小评分器用最终答案训练，"
        "另一个用步骤训练，每一步都对照前一步检查。<bookmark mark='a'/>然后，在新的题目上，采样N个解答，让每个评分器来挑。"
        "<bookmark mark='b'/>{said}<bookmark mark='c'/>虚线是一个完美的检查器；它下面的差距，是更好的评分器还能赢回来的部分。",

    "f'With {N} samples, the process grader picks a right solution":
        "采样{N}个解答时，过程评分器为{100 * p:.0f}%的题目挑出了正确解答，结果评分器{100 * o:.0f}%，投票{100 * vt:.0f}%。"
        "同样的解答，同样的预算：步骤标签每个例子携带的信息更多，评分器从中学到的也更多。",

    "f'Here the outcome grader does better:":
        "这里结果评分器更好：{100 * o:.0f}%，过程评分器是{100 * p:.0f}%，投票是{100 * vt:.0f}%。"
        "在这样规整的任务上，最终答案已经透露了很多关于步骤的信息。",

    "f'Both graders end close together,":
        '两个评分器最后很接近，{100 * p:.0f}%和{100 * o:.0f}%，投票是{100 * vt:.0f}%。',

    'f"Here is one of the solutions, graded both ways.':
        "这是其中一个解答，用两种方式评分。<bookmark mark='a'/>颜色是真相：哪些步骤真的对。<bookmark mark='b'/>"
        "过程评分器给每一步一个正确的概率。{where}<bookmark mark='c'/>结果评分器给整个解答一个数，{float(v['ex_orm']):.2f}，"
        "说不出错在哪里。正是这个位置，让步骤标签有用，无论是用来重新排序，还是用来教。",

    "f'Its score drops at the first wrong step,":
        '它的分数在第一个错误步骤，也就是第{first_bad + 1}步，掉到了{sc[first_bad]:.2f}：它指出了错误。',

    "f'It is less sure at the first wrong step,":
        '在第一个错误步骤，也就是第{first_bad + 1}步，它没那么确定了，但也没低多少：{sc[first_bad]:.2f}。学来的评分器也会漏看。',

    'And yet the models that changed the field in 2025 mostly did not train against process graders.':
        "然而，2025年改变这个领域的那些模型，大多没有用过程评分器来训练。DeepSeek的R1论文把它列在不成功的尝试里："
        "在一般的推理里，很难说清一步是什么，也很难检查一步，而一个学来的评分器，在强化学习的推动下，会被钻空子："
        "用他们的话说，这不可避免地导致奖励投机。<bookmark mark='a'/>于是配方变成了：在能被精确检查的结果上做强化学习："
        "数学题的答案，代码的测试，证明。<bookmark mark='b'/>过程评分器在搜索和重新排序中继续发挥作用，"
        "步骤标签自动生成：把一个部分解答续写很多次，看它有多大比例最后是对的。<bookmark mark='c'/>"
        "而最新的评分器，会先思考再评判。向检查器学习，是下一章的主题。",

    # ------------------------------------------------------------------ RL
    'Chapter four. Learning from a checker.':
        '第4章。向检查器学习。',

    'Chapter one showed that a chain of thought adds computation.':
        "第1章说明了思维链能增加计算。但没人能把步骤写下来的时候，谁来教模型该写哪条思维链？<bookmark mark='a'/>"
        "2024年2月，DeepSeek的数学论文提出了一种叫GRPO的算法：去掉了评论家的、第26部分的PPO。<bookmark mark='b'/>"
        "9月，OpenAI说o1是通过大规模强化学习学会思考的。<bookmark mark='c'/>11月，艾伦研究所的Tülu 3给这种方法起了名字："
        "可验证奖励的强化学习。<bookmark mark='d'/>2025年1月，DeepSeek-R1展示了它在大规模上的效果，奖励来自简单的规则："
        "最终答案对不对，格式对不对。<bookmark mark='e'/>检查器接受答案，奖励就是1，否则是0。没有任何人打分。",

    'f"We do it here with a small transformer that has had a little practice':
        "我们在这里用一个小Transformer来做，它练过一点两位数加法，直接作答。在这个游戏里，模型叫作策略，pi："
        "它给自己可能写出的每个答案一个概率。<bookmark mark='a'/>给它一道题，采样{G}个答案。<bookmark mark='b'/>"
        "检查器给每个答案打上记号：这里{G}个里有{n_right}个是对的。<bookmark mark='c'/>每个答案的优势，"
        "是它的奖励减去组内平均，再除以组内的标准差：对的答案在线上方，错的在下方。<bookmark mark='d'/>"
        "然后推一推模型，让好的答案更可能，坏的更不可能。<bookmark mark='e'/>这就是GRPO，组相对策略优化："
        "每个答案都和它自己的组比。第26部分的演员-评论家训练了第二个网络，评论家，去预测本来就能期望的分数；"
        "GRPO用组内的平均来代替。而当一组里每个答案都对，或者都错时，优势全是0：什么也学不到。",

    'f"Repeat that for {S} steps of thirty-two questions each, and replay the training.':
        "把这个过程重复{S}步，每步32道题，然后回放训练。<bookmark mark='a'/>左边是在500道新题上的正确率，"
        "从同一个起点出发的{int(r['seeds'])}次运行。右边是其中一次运行对6道题的回答，每道题试8次，每个检查点都显示。"
        "<bookmark mark='b'/>它一开始的正确率是{100 * float(r['before']):.0f}%。<bookmark mark='c'/>随着训练，绿色扩散开来："
        "开始时{snaps[0].size}个里对{nb}个，最后对{na}个。{finish}<bookmark mark='d'/>概率移到了能通过检查的答案上。",

    "f'All {len(after)} runs finish at":
        '{len(after)}次运行最后都是{after.mean():.0f}%，教它的只有一个检查器。',

    "f'The runs finish between":
        '各次运行最后在{after.min():.0f}%到{after.max():.0f}%之间，教它的只有一个检查器。',

    # ------------------------------------------------------------------ GRPO
    'Chapter five. GRPO, derived.':
        '第5章。推导GRPO。',

    "Let's derive it. The goal is the expected reward of the model's own answers.":
        "我们来推导一下。目标是模型自己的回答的期望奖励。<bookmark mark='a'/>用第26部分的对数导数技巧，它的梯度是奖励乘以"
        "每个采样回答的对数概率的梯度。<bookmark mark='b'/>减去一个只依赖于题目的基线，平均来说什么也不改变，"
        "因为对数概率梯度的期望是零；但它能大大减小噪声。<bookmark mark='c'/>GRPO的基线，是对同一道题的G个回答的平均奖励，"
        "再除以它们的标准差。这代替了PPO的评论家，那可是整整第二个网络。<bookmark mark='d'/>采样是最贵的部分，"
        "所以每一批样本要用来做好几次更新。第一次之后，模型已经变了，样本来自一个旧版本，pi old："
        "给每个样本乘上比值rho，也就是重要性采样的修正。<bookmark mark='e'/>再像PPO一样把它裁剪，"
        "这样任何一批样本都没法把模型推得太远。",

    'f"Here is the objective as DeepSeek published it, written per token.':
        "这是DeepSeek发表的目标函数，按词元写出。<bookmark mark='a'/>每个回答的每个词元都有自己的比值："
        "现在的模型给它的概率，比采样时高了多少。<bookmark mark='b'/>优势是整个回答的，它的词元共享，"
        "每个回答的词元取平均。<bookmark mark='c'/>对一个好的回答，目标函数随比值增长，直到这个词元比原来可能20%；"
        "然后就变平了，再推也没有好处。对一个坏的回答，一旦这个词元的可能性降低了20%，目标函数就不再奖励往下推。"
        "<bookmark mark='d'/>在我们的运行中，每批样本更新4次，裁剪拦下了{clip_g:.0f}%的词元。最后一项让模型留在起点附近。",

    'That last term needs the KL divergence from the reference model':
        "最后那一项需要和参考模型之间的KL散度，第1部分里衡量一个分布离另一个有多远的量。精确计算它，"
        "要对所有可能的回答求和，所以要从采样出来的回答里去估计。<bookmark mark='a'/>记r为参考模型的概率除以当前模型的概率。"
        "KL就是负log r的平均。<bookmark mark='b'/>所以最简单的估计k1，就是每个样本的负log r：平均来说是对的，但噪声大，"
        "而且可能是负数，而散度永远不会是负的。<bookmark mark='c'/>而r减1的均值正好是零，所以加上它，平均来说什么也不变。"
        "<bookmark mark='d'/>两者之和，约翰·舒尔曼的k3，永远不会是负的，因为log r最多是r减1，而且它仍然是无偏的。"
        "GRPO放进损失函数里的，就是这个估计。",

    'f"Our addition model makes this exact, because it has only a thousand possible answers.':
        "我们的加法模型能把这件事算得精确，因为它只有1000种可能的回答。取第4章训练之后的模型，算出它离起点的真实KL，"
        "每个回答{exact:.3f}奈特，再比较单个样本给出的估计。<bookmark mark='a'/>{k1_said}<bookmark mark='b'/>{k2_said}"
        "<bookmark mark='c'/>{k3_said}<bookmark mark='d'/>2025年的一个提醒：KL的无偏估计，并不是它的梯度的无偏估计。"
        "像GRPO那样直接放进损失函数，k3拉的方向会有一点偏，最近的配方常常干脆把这一项去掉。",

    "f'k one averages {k1m:.3f}, close to the truth,":
        'k1平均为{k1m:.3f}，接近真值，但有{k1n:.0f}%的估计是负的，离散程度为{k1s:.2f}。',

    "f'k one averages {k1m:.3f};":
        'k1平均为{k1m:.3f}；有{k1n:.0f}%的估计是负的，离散程度为{k1s:.2f}。',

    "f'k two, half the squared log ratio, is never negative, with spread {k2s:.2f}, but biased: on average {k2b:.3f}":
        'k2，对数比平方的一半，永远不为负，离散程度为{k2s:.2f}，但有偏：平均高了{k2b:.3f}。',

    "f'k two, half the squared log ratio, is never negative, with spread {k2s:.2f}, but biased: on average {-k2b:.3f}":
        'k2，对数比平方的一半，永远不为负，离散程度为{k2s:.2f}，但有偏：平均低了{-k2b:.3f}。',

    "f'k three is never negative, averages {k3m:.3f}, on the truth,":
        'k3永远不为负，平均为{k3m:.3f}，正好在真值上，离散程度为{k3s:.2f}。',

    "f'k three is never negative, averages {k3m:.3f}, and its spread":
        'k3永远不为负，平均为{k3m:.3f}，离散程度为{k3s:.2f}。',

    'f"Here is what the objective does to the model, step by step:':
        "这就是目标函数一步一步对模型做的事：三道它没把握的题，以及它给每个候选答案的概率，正确的那个是绿色。"
        "<bookmark mark='a'/>每一步，比组内平均好的回答被往上推，其余的往下压；裁剪让每次推动都很小。<bookmark mark='b'/>"
        "正确答案的概率平均从{100 * pr0:.0f}%升到{100 * pr1:.0f}%，错误答案的概率逐渐流失。{bumpy}"
        "熵也跟着下降，从每个数字{e0:.2f}比特降到{e1:.2f}比特：模型不再分散下注。这一点后面会很重要。",

    'Not smoothly: each step learns from eight sampled answers a question,':
        '并不平稳：每一步对每道题只从8个采样回答中学习，所以一个正确答案可能突然掉下去，过后再被拉回来。',

    'Steadily: the clip keeps any one batch from moving it far.':
        '很平稳：裁剪让任何一批样本都没法把它推得太远。',

    # ------------------------------------------------------------------ Variants
    'Chapter six. The successors.':
        '第6章。后继者们。',

    'Since DeepSeek-R1, a small industry has picked GRPO apart.':
        "DeepSeek-R1之后，整整一个小行业都在拆解GRPO。第一个发现来自Sea AI Lab的Zichen Liu和同事，"
        "关于对一个回答的词元取平均这个看似无害的做法。<bookmark mark='a'/>它意味着每个词元受到的推动，是优势除以回答的长度。"
        "<bookmark mark='b'/>一个短的正确回答，每个词元都被大力往上推。一个长的错误回答，它的许多词元每个只被轻轻往下压。"
        "<bookmark mark='c'/>所以错误回答越长，每个词元受的惩罚越少，长度会因为和思考毫无关系的原因往上漂。"
        "他们把修正叫作Dr. GRPO：去掉除以长度，也去掉除以组内标准差，因为后者会给几乎总是对、或者几乎总是错的题目额外的权重。",

    'Three more variants followed within months.':
        "几个月之内又出现了三个变体。<bookmark mark='a'/>Dr. GRPO，刚才看到了：不除以长度，也不除以标准差。"
        "<bookmark mark='b'/>DAPO，来自字节跳动和清华，让裁剪的上界比下界放得更宽，这样可能性低的好词元也能长起来；"
        "它扔掉没有信号的组；它让批次里的每个词元权重相同。<bookmark mark='c'/>GSPO，来自通义千问团队，"
        "每个回答只取一个比值，而不是每个词元一个：它的词元比值的几何平均。<bookmark mark='g'/>把比值乘起来，再开相应次数的方根，"
        "每个词元一次，于是一个翻了一倍的词元和一个减了一半的词元正好抵消。它让他们的混合专家模型的强化学习稳定了下来。"
        "<bookmark mark='d'/>还有CISPO，来自MiniMax，它裁剪的是重要性权重本身，并把它当作常数，于是每个词元都保留自己的梯度，"
        "包括那些会被PPO裁剪压掉的少见词元。在MiniMax自己的比较里，它用一半的步数就追平了DAPO。",

    'f"We ran all of them on our addition model,':
        "我们在加法模型上把它们全部跑了一遍，同一个起点，同一类题目，每种跑3次。<bookmark mark='a'/>{verdict}"
        "<bookmark mark='b'/>有一项代价柱状图里看不出来：DAPO的动态采样，为了填满批次，抽了{drawn['dapo']:.2f}倍的题目。"
        "公平的比较应该数样本，而不是数步数。",

    'f"The best average is {SAY[best]}\'s, {100 * means[best]:.0f} percent, but the averages span only':
        "平均最好的是{SAY[best]}，{100 * means[best]:.0f}%，但各方法的平均值只差{spread:.0f}个百分点，"
        "还不到同一种方法不同运行之间的{seed_spread:.0f}个百分点。在这么小的问题上，它们基本一致；"
        "差别要在大规模上才显现：长回答，成千上万步。",

    'f"The best average is {SAY[best]}\'s, {100 * means[best]:.0f} percent, and the averages span {spread:.0f}':
        "平均最好的是{SAY[best]}，{100 * means[best]:.0f}%，各方法的平均值相差{spread:.0f}个百分点，"
        "超过了同一种方法不同运行之间的{seed_spread:.0f}个百分点。",

    'f"One of DAPO\'s fixes is worth seeing.':
        "DAPO的一个修正值得看一看。当一道题的8个回答全对时，每个优势都是零，梯度也是零：这道题白做了。"
        "<bookmark mark='a'/>随着模型变好，这种情况越来越多：到最后，{100 * zs[-1]:.0f}%的组什么也没教给它。"
        "<bookmark mark='b'/>DAPO不断抽题，直到每个批次都装满了有分歧的组；到最后，它需要{dds[-1]:.1f}倍的题目。",

    'f"And the offline alternative?':
        "那么离线的替代方法呢？第27部分推导了DPO，它从固定的一好一坏的回答对中学习，训练时不采样。"
        "我们给它的回答对是一对一错，从起始模型中一次抽好。<bookmark mark='a'/>{how}<bookmark mark='b'/>{why_}"
        "<bookmark mark='c'/>手里有检查器的时候，从正在改进的模型本身采样，也就是在线策略，才是一直有回报的做法。",

    "f'It got worse:":
        '它变差了：正确率从{100 * acc0:.0f}%降到{100 * acc:.0f}%。',

    "f'It went from {100 * acc0:.0f} to {100 * acc:.0f} percent right.":
        '正确率从{100 * acc0:.0f}%变成了{100 * acc:.0f}%。',

    'Watch the log-probabilities on pairs it never trained on:':
        "看看它从没训练过的回答对上的对数概率：损失函数只要求正确答案相对错误答案上升，而最省事的办法，是把两者都往下压，"
        "错误的压得更快。概率流到了别处，大多流到了其他错误答案上：这就是第27部分讲的似然位移。",

    'On pairs it never trained on, the right answers rise and the wrong ones fall,':
        "在它从没训练过的回答对上，正确答案上升，错误答案下降，正如损失函数要求的；但这些回答对来自起始模型，"
        "模型一变，它们就不再提供信息了。",

    # ------------------------------------------------------------------ Entropy
    'Chapter seven. Entropy collapse.':
        '第7章。熵坍缩。',

    "At the end of chapter five, the model's entropy fell as it learned.":
        "在第5章的最后，模型学习的同时，它的熵在下降。这里说说为什么这总是一个威胁。熵衡量模型的选择有多分散。"
        "<bookmark mark='a'/>把概率写成logit z的softmax，再求导：移动logit b，熵的变化是负的pi b乘以b比平均情况意外多少。"
        "<bookmark mark='b'/>所以，一阶近似下，一步更新让熵改变的量，是负的协方差：在模型自己的选择上，对数概率和logit变化之间的协方差。"
        "<bookmark mark='c'/>策略梯度的一步，让每个logit按它的概率乘以优势的比例提高。当模型本来就喜欢的回答正好得分高时，"
        "这个协方差是正的，熵就下降。<bookmark mark='d'/>在模型自己的样本上做强化学习，奖励的正是本来就可能的东西，"
        "而且会越滚越大。Ganqu Cui和同事在2025年为语言模型把这一点推导了出来。",

    'f"{start} <bookmark mark=\'a\'/> GRPO, with its symmetric clip':
        "{start}<bookmark mark='a'/>GRPO用对称的裁剪，最后停在{fin['grpo']:.2f}。<bookmark mark='b'/>{higher}"
        "<bookmark mark='c'/>CISPO最后是{fin['cispo']:.2f}，完全不裁剪的普通梯度是{fin['pg']:.2f}。",

    'f"DAPO\'s clip-higher keeps more of it:':
        "DAPO放宽上界的裁剪保留了更多的熵：最后{fin['dapo']:.2f}比特，GRPO的对称裁剪是{fin['grpo']:.2f}。"
        "让可能性低的词元长得更快，就能让其他选项活下来。",

    'f"Here DAPO\'s clip-higher barely changes it:':
        "在这里，DAPO放宽上界的裁剪几乎没改变什么：最后{fin['dapo']:.2f}比特，GRPO是{fin['grpo']:.2f}。"
        "答案只有三位数，没什么可能性低的词元需要挽救；在长推理上，DAPO的作者发现它能防止熵坍缩。",

    "f'Here it is in our runs. Every objective starts at {e0:.2f} bits of entropy per digit, and every one drives it down.":
        '这是我们的运行结果。每种目标函数开始时，每个数字的熵都是{e0:.2f}比特，而每一种都把它压了下去。',

    "f'Here it is in our runs. Every objective starts at {e0:.2f} bits of entropy per digit.":
        '这是我们的运行结果。每种目标函数开始时，每个数字的熵都是{e0:.2f}比特。',

    'f"Cui and colleagues found something stranger.':
        "Cui和同事还发现了更奇怪的事。在许多次运行中，正确率是熵的一个简单函数：R等于负a乘以e的H次方，再加b。"
        "<bookmark mark='a'/>这里的每个点，是我们某一次运行的一个检查点，按目标函数上色。<bookmark mark='b'/>{fits}"
        "<bookmark mark='c'/>这个规律还带着一根刺：在熵为零，也就是模型完全不再探索的时候，它预言了一个上限，"
        "这里是{100 * (b - a):.0f}%。熵是一笔预算，强化学习花掉它来换正确率。",

    "f'Fitted to every checkpoint of our runs,":
        '拟合到我们所有运行的每个检查点上，它解释了正确率{100 * r2:.0f}%的变化，不管是哪种目标函数。',

    'f"On our runs the fit is loose:':
        '在我们的运行上，拟合比较松：它只解释了正确率{100 * r2:.0f}%的变化；各种目标函数用熵换正确率的比率并不相同。',

    'So the field fights the collapse.':
        "所以这个领域在和坍缩作斗争。<bookmark mark='a'/>DAPO放宽上界的裁剪，让可能性低的词元长得比可能性高的词元缩得快。"
        "<bookmark mark='b'/>熵奖励给模型一点报酬，让它保留选择。<bookmark mark='c'/>Cui的团队只约束协方差最大的那几个词元，"
        "也就是推动坍缩的那些。<bookmark mark='d'/>英伟达的ProRL靠控制KL、定期重置参考模型，让训练稳定地跑了两千多步。"
        "<bookmark mark='e'/>这为什么重要：一个不再探索的模型，你再问它一次时，能给出的不同答案就更少了。这是第9章的问题。",

    # ------------------------------------------------------------------ Length
    'Chapter eight. How long to think.':
        '第8章。该想多久。',

    'When DeepSeek trained R1-Zero with reinforcement learning':
        "DeepSeek用强化学习训练R1-Zero时，发生了一件没人要求过的事。它的思考越来越长，在整个训练过程中稳步增长，"
        "从几百个词元到几千个，尽管奖励只检查最终答案。<bookmark mark='a'/>在一个解答的中途，一个中间版本写道："
        "等等，等等，等等。这是一个我可以标记出来的顿悟时刻。然后它回过头去，把那一步重做了一遍。<bookmark mark='b'/>"
        "重新检查，回溯，换一种方法再试：这些都没有人示范过。它们之所以出现，是因为更长、更仔细的思维链能赢得更多奖励。",

    'f"Our adding model can show the same thing in miniature.':
        "我们的加法模型可以在小尺度上展示同样的事。只在和算对时给奖励，然后回放训练过程。<bookmark mark='a'/>"
        "这张图显示，对每种长度的列表，它选择思考多少步：第一列是直接回答，加框的格子是完整的思维链。{start}"
        "<bookmark mark='b'/>看看分布怎么移动。<bookmark mark='c'/>平均思考步数从{l0:.1f}步变成{l1:.1f}步，"
        "正确率从{100 * a0:.0f}%变成{100 * a1:.0f}%。{end}",

    "f'By the end it writes the whole chain almost every time:":
        '到最后，它几乎每次都写出完整的思维链：9个数字的列表，它{100 * p9:.0f}%的时候会思考，2个数字的列表也有{100 * p2:.0f}%。',

    "f'By the end it thinks on":
        '到最后，9个数字的列表它{100 * p9:.0f}%的时候会思考，2个数字的列表是{100 * p2:.0f}%。',

    "f'At the start it thinks {100 * pt0:.0f} percent of the time, and often stops":
        '一开始，它{100 * pt0:.0f}%的时候会思考，而且常常没到列表末尾就停下了。',

    "f'At the start it thinks {100 * pt0:.0f} percent of the time.'":
        '一开始，它{100 * pt0:.0f}%的时候会思考。',

    'f"There is a cost hiding in that last number.':
        "最后那个数字里藏着一个代价。2024年底，腾讯和上海交通大学的研究者给它起了名字：推理模型会过度思考，"
        "在像二加三这么简单的问题上，花掉的词元远远超过需要。<bookmark mark='a'/>{said}<bookmark mark='b'/>{after}",

    "f'After training, ours thinks on {100 * p2:.0f} percent of them anyway.":
        '训练之后，我们的模型还是在其中{100 * p2:.0f}%的题上思考。奖励里没有任何东西说思考的词元有成本，所以任何收益，'
        '哪怕再小，都值得任意长度。',

    "f'After training, ours thinks on only":
        '训练之后，我们的模型只在其中{100 * p2:.0f}%的题上思考：这里的一点点收益，不足以让思考成为习惯。'
        '更大的模型，用同样的方式奖励，就没这么克制了。',

    "f'On two-digit lists, before any reinforcement learning, answering at once was already right":
        '在2个数字的列表上，强化学习之前，直接回答已经有{100 * ad:.0f}%是对的，思考是{100 * at:.0f}%：只多了{gap:.0f}个百分点。',

    "f'On two-digit lists, before any reinforcement learning, answering at once was right":
        '在2个数字的列表上，强化学习之前，直接回答有{100 * ad:.0f}%是对的，思考是{100 * at:.0f}%：完全没有收益。',

    'f"The fix is to make thought cost something:':
        "解决办法是让思考有成本：每一步思考，都从奖励里减去一个小量c。我们用三种方式训练，每种跑3次。"
        "<bookmark mark='a'/>{plain}<bookmark mark='b'/>{gentle}<bookmark mark='c'/>{strong}<bookmark mark='d'/>"
        "这个成本是一个旋钮，一头是过度思考，一头是思考不足。",

    "f'With a cost of {float(costs[\'gentle\']):g} per step, it learns to choose:":
        "每步成本为{float(costs['gentle']):g}时，它学会了选择：2个数字的列表它{100 * g_t[0]:.0f}%的时候思考，"
        "9个数字的是{100 * g_t[-1]:.0f}%。短的列表，它直接回答；长的，它一步步算。",

    "f'With a cost of {float(costs[\'gentle\']):g} per step, it thinks on":
        "每步成本为{float(costs['gentle']):g}时，2个数字的列表它{100 * g_t[0]:.0f}%的时候思考，9个数字的是{100 * g_t[-1]:.0f}%。",

    'With no cost, it thinks on nearly everything.':
        '没有成本时，它几乎什么都要思考。',

    "f'With no cost, it thinks on":
        '没有成本时，按各种长度平均，它在{100 * tp:.0f}%的列表上思考。',

    "f'With {float(costs[\'strong\']):g}, thinking is too expensive:":
        "成本为{float(costs['strong']):g}时，思考太贵了：即使是最长的列表，它也只有{100 * g_s[-1]:.0f}%的时候思考，"
        "答对{100 * acc9['strong']:.0f}%，而没有成本时是{100 * acc9['plain']:.0f}%。现在是想得太少了。",

    "f'With {float(costs[\'strong\']):g}, it thinks on":
        "成本为{float(costs['strong']):g}时，最长的列表它{100 * g_s[-1]:.0f}%的时候思考，答对{100 * acc9['strong']:.0f}%，"
        "没有成本时是{100 * acc9['plain']:.0f}%。",

    'The frontier recipes do the same, more carefully.':
        "前沿的配方做的是同一件事，只是更仔细。<bookmark mark='a'/>月之暗面的Kimi k1.5加了一个在每组之内衡量的长度奖励："
        "在正确的回答里，越短的得分越高。<bookmark mark='b'/>卡内基梅隆大学的L1把想要的长度写进提示词，"
        "奖励模型达到这个长度。<bookmark mark='c'/>DAPO只惩罚超过最大长度的回答。<bookmark mark='d'/>"
        "而产品直接把这个旋钮交给用户：一个思考词元的预算，或者一个努力程度的设置，低、中、高。",

    # ------------------------------------------------------------------ PassK
    'Chapter nine. Sharper, or wider?':
        '第9章。更锐利，还是更宽广？',

    'To ask whether reinforcement learning teaches anything new':
        "要问强化学习有没有教会模型新东西，我们得衡量模型在多次尝试下能做到什么。这个量是pass@k："
        "k次尝试中至少有一次正确的概率，由检查器来判断哪次正确。对于一道一次尝试成功概率为p的题，它等于1减去1减p的k次方。"
        "<bookmark mark='a'/>实际上，我们有n个样本，其中c个正确。最直接的估计是代入c除以n。<bookmark mark='b'/>"
        "但它是有偏的：1减x的k次方是凸函数，所以由詹森不等式，代入估计平均来说偏低。<bookmark mark='c'/>"
        "修正方法来自OpenAI 2021年的Codex论文：从n个样本中随机、不放回地选k个，问它们全错的可能性有多大。"
        "<bookmark mark='d'/>n次独立尝试中的任意k次，本身就是k次独立尝试，所以平均来说，这正好是1减p的k次方。无偏。",

    'f"Here are both estimates on our addition model before reinforcement learning':
        "这是两种估计在强化学习之前的加法模型上的结果，这里我们知道确切答案。<bookmark mark='a'/>代入估计偏低，"
        "最多低{gap:.0f}个百分点。无偏估计落在精确的曲线上。<bookmark mark='b'/>对单道题，无偏估计噪声很大，但中心在真值上；"
        "代入估计的中心偏低。在一个大的基准上，噪声会平均掉，偏差不会。",

    'In April 2025, Yang Yue and colleagues at Tsinghua asked exactly this;':
        "2025年4月，清华的Yang Yue和同事问的正是这个问题；这篇论文在那年12月成了NeurIPS的口头报告。<bookmark mark='a'/>"
        "强化学习之后，一次尝试的表现好得多。但给两个模型几百次尝试，基础模型，也就是强化学习的起点，解出的题更多。"
        "两条曲线交叉了。他们的解读是：强化学习是在锐化；它把概率挪到基础模型本来就能找到的推理上，并收窄其余的部分。"
        "相比之下，从更强的老师那里蒸馏，可以加入新的推理。<bookmark mark='b'/>几周之内就有了回应。英伟达的ProRL训练得久得多，"
        "控制住KL并重置参考模型，报告了基础模型够不到的策略。两者并不矛盾：短的训练在锐化；长而多样的训练可能在拓宽。",

    'f"We can check it exactly on our addition model,':
        "我们可以在加法模型上精确地检查这一点，因为我们知道它给每个答案的概率，所以pass@k不需要采样，哪怕是一千次尝试。"
        "<bookmark mark='a'/>强化学习之前，一次尝试的正确率是{100 * base[0]:.0f}%。<bookmark mark='b'/>"
        "训练300步之后，大约{100 * rl1:.0f}%。<bookmark mark='c'/>{said}",

    'f"And the curves cross:':
        "曲线交叉了：尝试{k_last}次时，强化学习之前的模型解出{100 * base[-1]:.1f}%，而{SAY[lost[0]]}解出"
        "{100 * means[lost[0]][-1]:.1f}%。从大约{min(cross)}次尝试开始，未经训练的模型领先。在200道题里，"
        "大约有{dead:.0f}道，强化学习把正确答案的概率压到了千分之一以下，挪到了它越来越有把握的错误答案上。",

    'f"And at {k_last} tries the curves meet:':
        "尝试{k_last}次时，曲线汇合了：强化学习之前是{100 * base[-1]:.1f}%，之后在"
        "{100 * min((m[-1] for m in means.values())):.1f}%到{100 * max((m[-1] for m in means.values())):.1f}%之间。"
        "在这么小的问题上，强化学习没有让任何一道题变得不可能；它让容易的答案变得确定。",

    'f"One warning about measuring with many tries.':
        "关于用很多次尝试来衡量，有一个警告。检查器对蒙对的答案，和对推理出来的答案，给的奖励一样多。在{int(gs['m'])}个"
        "可能的和之间均匀地猜，尝试1024次的pass@k是{100 * p1024:.0f}%。<bookmark mark='a'/>在k很大时，"
        "pass@k会让瞎猜看起来像推理。所以严谨的研究还会检查思维链，或者用答案多到猜不中的问题：证明，以及必须通过测试的程序。",

    # ------------------------------------------------------------------ TestTime
    'Chapter ten. Thinking at answer time.':
        '第10章。回答时的思考。',

    'There are two ways to spend more computation once the question is asked.':
        "问题提出之后，有两种方式花更多的计算。<bookmark mark='a'/>并行：采样很多个回答，再挑一个，靠投票、评分器或检查器。"
        "<bookmark mark='b'/>或者串行：一条更长的思维链，重新检查，修改，继续。<bookmark mark='c'/>哪种更好？"
        "2024年，伯克利和谷歌DeepMind的Charlie Snell和同事发现，这取决于问题：容易的题从修改中获益，"
        "难的题从更广的搜索中获益。按题目选择策略，效率是最优N选1的4倍以上；一个小模型加上测试时计算，"
        "能胜过一个大14倍的模型，前提是它有时能解出这些题。",

    'The sequential dial can be very simple.':
        "串行的旋钮可以非常简单。2025年1月，斯坦福的Niklas Muennighoff和同事，只用1000道带解答的题微调了一个模型，"
        "然后在回答时控制它的思考。<bookmark mark='a'/>要让它想得更久，就在它想停下的时候，接上一个词：等等。"
        "模型会回头检查自己的过程，有时还会改正一个错误。要让它想得少一些，就截断它，让它作答。<bookmark mark='b'/>"
        "强制它多想之后，AIME的成绩从50%升到57%，在竞赛数学上比o1-preview最多高出27%。他们把这叫作预算强制。",

    'f"Our adding model can be given a budget too.':
        "我们的加法模型也可以给预算。让它思考，并在最多m步之后强制它作答，就像s1截断模型那样。<bookmark mark='a'/>{first}"
        "<bookmark mark='b'/>并行的替代方案：直接回答N次，然后投票。<bookmark mark='c'/>{verdict}<bookmark mark='d'/>{after}",

    "f'After reinforcement learning, thinking fully reaches {100 * rs[-1]:.0f} percent. Training":
        '强化学习之后，完整地思考能达到{100 * rs[-1]:.0f}%。训练时的计算和测试时的计算，是买同一样东西的两种方式。',

    "f'After reinforcement learning, thinking fully reaches {100 * rs[-1]:.0f} percent: what":
        '强化学习之后，完整地思考能达到{100 * rs[-1]:.0f}%：强化学习改变的主要是要不要思考的选择，而不是加法做得多好。',

    "f'With no thought at all it gets {n}-digit lists right {100 * at0:.0f} percent of the time; each":
        '完全不思考时，它在{n}个数字的列表上答对{100 * at0:.0f}%；每多一步思考，就多换来一些正确率。',

    "f'With no thought at all it gets {n}-digit lists right {100 * at0:.0f} percent of the time. Cut":
        '完全不思考时，它在{n}个数字的列表上答对{100 * at0:.0f}%。想到一半被打断，并不比完全不想好。'
        '只有完整的思维链才有回报：{100 * full:.0f}%。',

    "f'With no thought at all it gets {n}-digit lists right {100 * at0:.0f} percent of the time, and":
        '完全不思考时，它在{n}个数字的列表上答对{100 * at0:.0f}%，完整地思考是{100 * full:.0f}%，但并不是每多一步都有帮助。',

    'f"Thinking all {n} steps reaches':
        "完整地思考{n}步，用{t_full}个词元达到{100 * full:.0f}%。对直接给出的答案投票，在同样的预算下只有{100 * v_at:.0f}%，"
        "用上我们允许的全部词元，也只有{100 * v_best:.0f}%。在一个由许多小步骤组成的问题上，思维链赢了："
        "投票没法把任何一次尝试都没加对的数字加对。",

    "f'Thinking all {n} steps reaches":
        '完整地思考{n}步，用{t_full}个词元达到{100 * full:.0f}%；对直接给出的答案投票，用我们允许的词元达到{100 * v_best:.0f}%。',

    'The simplest parallel strategy with a checker is best-of-N:':
        "有检查器时，最简单的并行策略是最优N选1：抽N个回答，留一个正确的。第27部分说明了，在奖励没有并列时，"
        "最优N选1让模型离起点的距离是log N减去N分之N减1奈特。而检查器的奖励全是并列：要么对，要么错。所以我们重新算一遍。"
        "<bookmark mark='a'/>如果一次尝试正确的概率是p，最优N选1正确的概率就是1减去1减p的N次方。<bookmark mark='b'/>"
        "在正确的条件下，它返回哪个正确答案，与模型自己的概率成比例；错误的也一样。<bookmark mark='c'/>"
        "所以KL就是两枚硬币之间的散度：一枚正确的概率是1减q，另一枚是p。<bookmark mark='d'/>随着N增大，它在log p分之1处趋平，"
        "不管抽多少个回答，都远低于第27部分的公式；而那个公式在一般情况下只是一个上界，Ahmad Beirami和同事在2024年证明了这一点。",

    'f"On our addition model, exactly.':
        "在我们的加法模型上，精确地算一下。<bookmark mark='a'/>有检查器的最优N选1，KL在{kl[-1]:.2f}奈特处趋平，"
        "而没有并列时的公式，在{Ns[-1]}次尝试时会达到{bound[-1]:.2f}。<bookmark mark='b'/>再看正确率：{match}",

    'f"best-of-N needs about {Nmatch} tries':
        "最优N选1需要大约{Nmatch}次尝试，才能赶上强化学习之后的模型一次尝试的正确率。强化学习把过去需要很多次尝试的东西，"
        "挪进了一次尝试里。o1的数字也是同样的形状：一次尝试74%，让学来的打分器从一千个里挑，93%。",

    'even best-of-N with every try we allowed falls short':
        '即使用上我们允许的全部尝试，最优N选1也比不上强化学习之后的模型一次尝试。',

    # ------------------------------------------------------------------ Outro
    "Let's take stock. Writing out steps lets a model of fixed depth compute for longer:":
        "我们来总结一下。写出步骤，能让一个深度固定的模型计算得更久：每个词元都多换来一次穿过网络的计算。"
        "采样很多条思维链再投票，只会放大模型本来就偏爱的答案；检查器，或者检查步骤的评分器，做得更好。"
        "向检查器学习的强化学习，靠GRPO的组基线和它的裁剪，把概率挪到能通过检查的答案上，代价是花掉模型的熵。"
        "放任不管，它会学着想得更久，有时太久，直到思考被定上价格。它锐化模型本来就能做的事，"
        "而训练足够久的话，也许能拓宽它。在回答时，更多的计算换来更多的正确答案，无论是并行还是串行。",

    'All of this comes back. Reasoning over hundreds of steps, with tools':
        "所有这些都会再出现。借助工具、跨越几百步的推理，就是智能体要做的事，在第29部分。每个思考的词元生成时都要花时间，"
        "第19部分的推理技巧，正是长时间思考负担得起的原因。模型写出的思维链，是不是它真正得出答案的过程，是第30部分的问题。"
        "而奖励投机，以及通过监看模型的思维链去发现它，会在最后一部分再出现。",

    "Here are six problems to try, from GRPO's baseline to the entropy's fall.":
        "这里有6道题可以试试，从GRPO的基线到熵的下降。在这里暂停，把它们做一遍；完整的解答在这一部分的笔记里。",

    'f"Next time: agents, models that act over many steps':
        "下一次：智能体，在世界中或在电脑上跨越很多步行动的模型。这是它们面对的问题，用我们自己的思维链来测量。"
        "我们的加法模型写出的每一步思考，有{100 * ps:.1f}%是对的。<bookmark mark='a'/>但一个长任务需要每一步都对，"
        "而这些概率是相乘的。{half}<bookmark mark='b'/>智能体怎样在很长的时间跨度上规划、自查、纠错，"
        "又怎样学会它们所处世界的模型：第29部分。",

    "f'Even at {100 * ps:.1f} percent a step":
        '即使每步有{100 * ps:.1f}%的正确率，{n50:.0f}步的链条也只有一半的机会全对，200步几乎没有希望。',

    "f'At {100 * ps:.1f} percent a step, even two hundred steps usually survive.":
        '每步{100 * ps:.1f}%的正确率，即使200步通常也能全对。',

    "Nathan Lambert's free book on reinforcement learning from human feedback":
        "想深入了解，最好的去处是内森·兰伯特关于基于人类反馈的强化学习的免费书；它也讲了可验证奖励的强化学习和推理。"
        "谢谢观看，第29部分见。",

    # ------------------------------------------------------------------ Search
    'Chapter eleven. Searching over thoughts.':
        '第11章。在思路中搜索。',

    "Search is how Part 26's game players thought ahead":
        "搜索就是第26部分那些下棋程序向前思考的方式，各个部分几乎可以一一对应过来。<bookmark mark='a'/>"
        "一个局面，变成一条部分完成的思维链；一步棋，变成下一步思考。<bookmark mark='b'/>AlphaZero的策略网络，"
        "也就是它对哪些棋值得一试的感觉，变成语言模型自己给下一步的概率。<bookmark mark='c'/>价值网络，"
        "也就是一个局面看起来有多好，变成过程奖励模型。<bookmark mark='d'/>而输赢，变成检查器。<bookmark mark='e'/>"
        "不同的是树的大小：棋盘上合法的走法最多几百种，而语言模型在每个词元上都有整整一个词表可选，"
        "一步思考又有许多个词元那么长。",

    'Sampling chains and voting treats each chain as a whole.':
        "采样思维链再投票，是把每条思维链当作一个整体。搜索则是一步一步来：提出几个下一步的想法，评判它们，"
        "从最有希望的那个继续往下走。<bookmark mark='a'/>2023年，"
        "“思维树”让GPT-4自己提出、自己评判下一步的想法；在一个用四个数凑出24的谜题上，正确率从思维链的4%升到74%。"
        "<bookmark mark='b'/>2025年，微软的rStar-Math在步骤上做蒙特卡洛树搜索，由一个学来的过程模型引导，"
        "把一个70亿参数的模型在竞赛数学上从59%提高到90%。<bookmark mark='c'/>AlphaProof在形式化证明的步骤上搜索，"
        "每一步都由机器检查；我们会在第13章见到它。<bookmark mark='d'/>但DeepSeek为R1试过树搜索，最后放弃了："
        "在词元上，这棵树大得惊人，而引导它的价值模型又很难训练。在前沿，搜索主要以并行采样很多条思维链的形式保留下来。",

    'f"Here is search on our adding model.':
        "这是在我们的加法模型上的搜索。每一步，每条幸存的部分思维链提出三个下一个累计和；第3章的过程评分器给每个候选打分；"
        "最好的三个留下来。<bookmark mark='a'/>绿色节点是正确的累计和，红色是幸存下来的错误节点，灰色是被剪掉的。"
        "<bookmark mark='b'/>{fin}",

    'At the end, the best surviving chain is right all the way down.':
        '到最后，幸存的最好那条思维链从头到尾都是对的。',

    'At the end the best surviving chain still has a wrong step:':
        '到最后，幸存的最好那条思维链仍有一步是错的：评分器也会被骗。',

    'f"Is search worth it?':
        "搜索值得吗？把它和最优N选1比较，用同一个评分器，花同样多的词元。<bookmark mark='a'/>最优N选1采样N条完整的思维链，"
        "留下评分器最喜欢的那条。<bookmark mark='b'/>束搜索把同样多的词元一步一步地花。<bookmark mark='c'/>{said}",

    'At every budget, searching step by step beats choosing among whole chains:':
        "在每一种预算下，一步一步地搜索都胜过在完整思维链里挑选：错误的累计和一写出来就被发现，"
        "而不是指望某一整条思维链恰好每一步都没出错。",

    'Here, choosing among whole chains does better than searching step by step:':
        "在这里，在完整思维链里挑选反而比一步一步地搜索更好：评分器在每一步犯的错误会累积，"
        "过早剪枝会扔掉本来能纠正回来的思维链。",

    'Here the two end up close:':
        '在这里两者的结果很接近：在这样规整的问题上，好的评分器怎么用都有帮助。',

    # ------------------------------------------------------------------ Latent
    'Chapter twelve. Thinking without words.':
        '第12章。不用文字的思考。',

    'f"A chain of thought is computation, but it has a narrow throat.':
        "思维链是计算，但它有一个狭窄的咽喉。<bookmark mark='a'/>每一步，模型最后的隐状态，成千上万个数，"
        "被挤进一个词元：词表有十万个词元的话，大约17个比特。<bookmark mark='b'/>然后这个词元再被变回数字，用于下一步。"
        "模型要带往下一步的一切，都得挤过这个咽喉。<bookmark mark='c'/>{dots}<bookmark mark='d'/>"
        "那么，为什么不直接把状态传下去呢？",

    'In chapter one, giving our model meaningless dots instead of words didn\'t help:':
        "在第1章里，用没有意义的点代替文字，对我们的模型没有帮助：要紧的不是位置，而是把状态带下去。",

    "f'In chapter one, meaningless dots helped our model a little,":
        "在第1章里，没有意义的点对我们的模型有一点帮助，{100 * fd:.0f}%，相比之下直接回答是{100 * dd:.0f}%，"
        "但远远比不上写出的思维链：要紧的是把状态带下去。",

    'That is Coconut, from Shibo Hao and colleagues at Meta, in December 2024.':
        "这就是Coconut，Meta的Shibo Hao和同事在2024年12月提出的。<bookmark mark='a'/>在思维链里，每一步的状态变成一个词元，"
        "词元再变回状态。<bookmark mark='b'/>在Coconut里，在一段推理中，最后的隐状态直接作为下一个输入送回去："
        "这叫连续思维。训练时用一套课程，把写出来的步骤一次几个地换成连续的步骤。<bookmark mark='c'/>"
        "结果出现了意料之外的东西。一个连续思维不必只认定一个下一步：它可以同时装下好几个，于是模型做的是广度优先搜索。"
        "在需要搜索的逻辑谜题上，它胜过了写出来的思维链。",

    'A second line of work drops the language model altogether.':
        "第二条路线干脆不用语言模型。<bookmark mark='a'/>2025年6月，Sapient Intelligence的层级推理模型，只有2700万参数，"
        "每个任务只用大约1000个例子从零训练，在极难的数独上得了55%，在困难迷宫上得了74%，并报告在ARC-AGI-1上得了40%，"
        "我们会在第14章见到这些谜题。它的想法是：两个循环模块，一个慢的负责规划，一个快的负责计算，"
        "在回答之前反复迭代很多次。<bookmark mark='b'/>ARC Prize团队做了核查。他们复现了大部分结果，"
        "在他们留出的测试集上是32%，但发现层级结构几乎不起作用：同样大小的Transformer只差大约5个百分点。"
        "起作用的是一个外层循环：把模型的答案送回去，一遍又一遍地改进。",

    'In October 2025, Alexia Jolicoeur-Martineau at Samsung':
        "2025年10月，三星蒙特利尔实验室的Alexia Jolicoeur-Martineau把这个想法削减到只剩核心。<bookmark mark='a'/>"
        "一个微型网络，两层。它读入谜题x，并保留两样东西：一个隐式的草稿z，和它当前的答案y。<bookmark mark='b'/>"
        "它先把草稿更新6次，再用草稿去改进答案。<bookmark mark='c'/>然后整个过程再来一遍，每一轮之后都检查它的答案，"
        "最多16轮。<bookmark mark='d'/>只有700万参数，它在每一项任务上都胜过了层级推理模型：极难数独87%，对方55%；"
        "ARC-AGI-1上45%，超过了很多大语言模型。它获得了2025年ARC Prize论文奖的第一名。靠递归获得深度，而不是靠词元。",

    "There's a price. A chain written in words can be read.":
        "这是有代价的。用文字写出的思维链是可以读的。<bookmark mark='a'/>2025年，来自多家实验室的研究者一起把这称为"
        "一个新的、但脆弱的安全机会：如果模型打算作弊，它写出的思维链可能在它动手之前就说出来。<bookmark mark='b'/>"
        "用向量思考也许更高效，但没人能读懂。思维链说的话能不能信，是第30和第31部分的问题。",

    # ------------------------------------------------------------------ Formal
    'Chapter thirteen. Proofs a machine can check.':
        '第13章。机器能检查的证明。',

    'Everything in this part has leaned on a checker, and checkers have limits:':
        "这一部分的一切都依赖检查器，而检查器有它的局限：一个正确的数字，可能出现在一段错误论证的结尾。"
        "数学有一条出路。<bookmark mark='a'/>在Lean这样的证明助手里，定理和它的证明都写成代码，"
        "由一个小而可信的内核检查每一步推理。<bookmark mark='b'/>没有碰运气，也没有含糊其辞：证明要么被接受，要么不被接受。"
        "<bookmark mark='c'/>对强化学习来说，这是完美的奖励，一个没法被钻空子的奖励，只要形式化的命题说的正是本意。"
        "<bookmark mark='d'/>而且从2017年起，一个社区一直在把数学形式化，写进Lean的数学库Mathlib，让这样的系统有基础可依。",

    "Google DeepMind's AlphaProof put this to work.":
        "谷歌DeepMind的AlphaProof把这一点用了起来。<bookmark mark='a'/>一个Gemini模型把大约100万道数学题从文字翻译成Lean，"
        "得到大约8000万条形式化命题。然后第26部分的AlphaZero开始处理它们：搜索证明，留下Lean接受的，"
        "再用它们训练网络，一轮又一轮。<bookmark mark='b'/>在最难的题上，它走得更远：在测试时，它生成这道题的变体，"
        "证明这些变体，再从中学习，也就是在考场上做强化学习。<bookmark mark='c'/>在2024年国际数学奥林匹克上，"
        "加上负责几何题的AlphaGeometry 2，它得了42分里的28分，离金牌只差1分，解出了6道题里的4道，"
        "包括最难的那一道，那道题只有5名选手解出。有些证明花了它三天。",

    'A year later the picture changed.':
        "一年之后，局面变了。<bookmark mark='a'/>在2025年的奥林匹克上，谷歌Gemini的一个带有Deep Think的版本，"
        "会并行地探索很多条思路，解出了6道题中的5道，35分，正好是金牌线，用普通英语写成，在四个半小时之内；"
        "由奥林匹克自己的协调员评分。<bookmark mark='b'/>OpenAI为一个实验性的推理模型宣布了同样的分数，"
        "由前奖牌得主评分。<bookmark mark='c'/>形式化证明器也赶了上来：Harmonic的Aristotle和字节跳动的Seed-Prover，"
        "各自在Lean里证明了6道题中的5道，每一步都经过检查。一年之前，最好的系统还需要好几天，还需要人来翻译题目。",

    'So here is the spectrum every reasoning method lives on.':
        "所以，每一种推理方法都处在这样一条光谱上。<bookmark mark='a'/>一端是骗不了的检查器：Lean里的证明，"
        "要对上的一个数，必须通过测试的代码。<bookmark mark='b'/>另一端是学来的评分器，过程奖励模型，或者当裁判的另一个模型，"
        "足够强的优化器总能找到办法绕过它们。<bookmark mark='c'/>推理进步最快的，恰恰是检查器精确的地方：数学和代码。"
        "把它推广到其余的一切，文章、建议、研究，才是难题所在。",

    # ------------------------------------------------------------------ ARC
    'Chapter fourteen. Puzzles nobody has seen.':
        '第14章。没人见过的谜题。',

    'Every benchmark so far rewards knowing things.':
        "到目前为止，每个基准测试奖励的都是知道东西。2019年，写了Keras库的弗朗索瓦·肖莱提出，智能是另一回事："
        "你获得一项新技能的效率有多高。他为此设计了一个测试，抽象与推理语料库，现在叫ARC-AGI。<bookmark mark='a'/>"
        "每个任务给出几对彩色网格，一个输入，一个输出。<bookmark mark='b'/>然后给一个新的输入。输出会是什么？"
        "<bookmark mark='c'/>人觉得大多数任务都很简单。每个任务都不一样，所以什么都背不下来：规则必须当场找出来。",

    'ARC-AGI-1 resisted for five years.':
        "ARC-AGI-1坚持了五年。<bookmark mark='a'/>2020年的Kaggle比赛，冠军只有大约20%，靠的是在手写的程序里搜索。"
        "2024年，在测试时用每个任务自己的例子做训练，达到了53.5%。<bookmark mark='b'/>然后在2024年12月，"
        "OpenAI的o3以每个任务大约26美元的成本得了75.7%，用172倍的计算得了87.5%。<bookmark mark='c'/>"
        "于是2025年3月，更难的版本ARC-AGI-2发布了，最好的系统跌回到几个百分点，而一个人平均能解出60%。"
        "<bookmark mark='d'/>到了12月，一个用合成任务训练的40亿参数模型以24%赢得了Kaggle比赛；Claude Opus 4.5达到37.6%；"
        "一个包在Gemini 3 Pro外面的精炼循环达到54%。ARC Prize把这一年的主题定为精炼循环：提出，检查，改进。"
        "<bookmark mark='e'/>而在2026年10月，ARC Prize验证了谷歌的Gemini 4 Argon得到91%。19个月，"
        "这个更难的测试就几乎被解决了。",

    'So in March 2026 came ARC-AGI-3:':
        "所以在2026年3月，ARC-AGI-3来了：交互式的游戏，没有任何说明。玩家必须探索，弄清目标是什么，再做规划，"
        "得分看它达到目标的效率，跟人比。<bookmark mark='a'/>人能解出每一个游戏。发布时，所有前沿模型的得分都不到1%。"
        "<bookmark mark='b'/>到了9月，ARC Prize用他们的标准测试框架测得OpenAI的GPT-6 Astra为62.7%。"
        "<bookmark mark='c'/>每一个新测试都比上一个倒得更快。而解开它们的方法，就像这一部分的每一章一样："
        "提出，检查，改进，循环往复。",
}

PHRASES = {
    "the plain group gradient": "普通的组梯度",
    "Doctor GRPO": "Dr. GRPO",
    "a coin flip": "跟抛硬币差不多",
    "far from reliable": "远远谈不上可靠",
    "solved": "解决了",
    "shaky": "不太稳",
    "much better": "好得多",
}
