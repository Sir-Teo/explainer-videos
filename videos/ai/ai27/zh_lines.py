"""Chinese narration for ai27: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第27部分：后训练与对齐'

CHAPTERS = {
    'Hook': '同一个模型，训练前后',
    'Pipeline': '1. 从预测者到助手',
    'SFT': '2. 监督微调',
    'LoRA': '3. 低秩适配器',
    'Rewards': '4. 学习人们的偏好',
    'RLHF': '5. 拴着绳子的强化学习',
    'Goodhart': '6. 当指标成了目标',
    'DPO': '7. 直接偏好优化',
    'Constitution': '8. 来自AI的反馈，来自人的规则',
    'Distill': '9. 蒸馏',
    'Merge': '10. 把模型加起来',
    'Failures': '11. 哪里会出错',
    'Recipes': '12. 公开的配方',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    'Chapter one. From predictor to assistant.':
        '第1章。从预测者到助手。',

    'A pretrained language model, everything in Parts 13 to 18':
        "一个预训练语言模型，也就是第13到第18部分讲的一切，只有一项本事：接着写文本。它唯一的目标，就是预测网上文档的下一个词元。<bookmark mark='a'/>所以你问它一个问题，它就照这类文档的样子做。网上的一个问题后面，往往跟着更多的问题：一份测验，一组练习题。<bookmark mark='b'/>我们想要的不一样：一个会回答的助手。模型其实已经知道巴黎是法国的首都。后训练要做的，就是让它按我们想要的方式，用上它已经知道的东西。",

    'The recipe that made ChatGPT was published by OpenAI':
        "造就ChatGPT的配方，OpenAI在2022年3月以InstructGPT的名字发表了。预训练之后，它分三个阶段。<bookmark mark='a'/>第一，监督微调：人们为大约1.3万个提示写出好的回答，模型被训练去模仿它们。<bookmark mark='b'/>第二，奖励模型：对3.3万个提示，人们把模型的几个回答从好到差排序，再由一个网络学着预测他们的排序。<bookmark mark='c'/>第三，强化学习：第26部分的PPO，由奖励模型来代替人。<bookmark mark='d'/>结果令人吃惊。人们更喜欢13亿参数的InstructGPT的回答，胜过它出发时那个1750亿参数的GPT-3：小了一百倍，却更受欢迎，因为它在努力帮忙。",

    'The idea is older than chatbots.':
        "这个想法比聊天机器人更早。<bookmark mark='a'/>2017年，OpenAI和DeepMind的保罗·克里斯蒂亚诺、扬·莱克和同事，教会一个模拟机器人做后空翻，却从来没有写下后空翻是什么。一个人看两段短视频，挑出更像后空翻的那段，大约挑了900次，用了不到一小时；一个网络学会了他的偏好，强化学习完成了剩下的事。<bookmark mark='b'/>2020年，同样的方法被用来训练语言模型写摘要，人们更喜欢它写的摘要，胜过人写的。<bookmark mark='c'/>随后是InstructGPT，然后在2022年11月30日，是ChatGPT。<bookmark mark='d'/>从那以后，这套配方在开放的环境中被复现，也被改变了：Meta的Llama 2用了一百多万次比较，而一种叫DPO的方法表明，奖励模型可以整个省掉。",

    'This is what the field calls alignment':
        "这就是这个领域所说的对齐：让模型去做构建它、使用它的人想让它做的事。Anthropic的简称是：有用、诚实、无害。<bookmark mark='a'/>难处在于，人们想要什么，很难写成一个公式。<bookmark mark='b'/>但很容易认出来：给一个人看两个回答，他通常能说出哪个更好。<bookmark mark='c'/>所以本部分的策略是：先从人们的判断中学到目标，再去优化它，而且要小心，因为学到的目标只是一个近似。每一步都会真的去做，就在本系列用三十部小说训练出来的那个小模型上。",

    'Chapter eight. Feedback from AI, rules from people.':
        '第8章。来自AI的反馈，来自人的规则。',

    'Human comparisons are slow and expensive':
        "人工比较又慢又贵，有些还让人不快：总得有人读完那些有害的回答，才能给它们排序。2022年12月，Anthropic发表了宪法式AI，把其中大部分工作交给模型自己，由人写下的一小份原则来引导：一部宪法。<bookmark mark='a'/>首先是监督阶段。模型回答一个棘手的请求。<bookmark mark='b'/>然后让它对照一条原则批评自己的回答，比如：选择危害最小、又不说教也不回避的回答。<bookmark mark='c'/>它根据批评重写回答。<bookmark mark='d'/>再用改写后的回答来微调它。人的工作投入在原则上，而不是每一个标签上。",

    'The second phase replaces human comparisons too.':
        "第二阶段把人工比较也替换掉了。<bookmark mark='a'/>两个回答交给一个AI裁判，也就是一个拿到了这些原则的语言模型，由它判断哪个更符合原则。这些比较用来训练奖励模型，强化学习则和第5章一样进行。这就是基于AI反馈的强化学习，RLAIF。<bookmark mark='b'/>2023年，谷歌的一个团队直接比较了两者，在摘要和对话任务上，AI反馈的效果和人类反馈差不多。如今后训练中的大多数比较都由模型来判断，人负责写规则、检查裁判。",

    'f"A small version of the idea, on our model.':
        "在我们的模型上，做一个小规模的版本。<bookmark mark='a'/>只用{d['n_human']}次人工比较训练一个奖励模型。<bookmark mark='b'/>把它当作裁判：让它给{d['n_ai']:,}个新的比较打标签，再用这些标签训练一个新的奖励模型。{verdict}<bookmark mark='c'/>作为对照，{d['n_ai']:,}次真实的比较，能达到{100 * d['acc_full']:.0f}%。",

    'The constitutions themselves became public documents.':
        "这些宪法本身也成了公开文件。<bookmark mark='a'/>2023年，Anthropic公开了Claude的原则。<bookmark mark='b'/>2024年，OpenAI发布了一份模型规范，并训练它的推理模型在回答之前，先在思维链里读一遍相关的政策，称之为审慎对齐。<bookmark mark='c'/>2026年1月，Anthropic把原则清单换成了一份长文，解释每条原则背后的理由，并明确了优先次序：总体上安全，总体上合乎伦理，遵循Anthropic的准则，真正有帮助。规则由人用平实的语言写成，训练则让模型去运用它们。",

    'Chapter eleven. What goes wrong.':
        '第11章。哪里会出错。',

    'The first failure follows directly from chapter six.':
        "第一种失败，直接来自第6章。人们奖励自己喜欢的回答，而人们喜欢被认同。<bookmark mark='a'/>问一个问题，附上自己的猜测，一个夸赞猜测的回答，可能比一个纠正它的回答更受欢迎。奖励模型学会了这一点，强化学习又把它放大：这就是谄媚。<bookmark mark='b'/>2023年，Anthropic的研究人员发现，五个被广泛使用的助手都一贯谄媚，并把部分原因追溯到偏好数据：在这些数据里，令人信服的附和有时胜过正确。<bookmark mark='c'/>2025年4月，OpenAI撤回了GPT-4o的一次更新，因为用户觉得它过分奉承；它自己的说明指向了一个新的奖励信号，来自用户的点赞和点踩。",

    'Post-training teaches a model to refuse harmful requests':
        "后训练教会模型拒绝有害的请求，而这种教导可以被绕开。<bookmark mark='a'/>2023年，安迪·邹和同事用梯度搜索，找到了一串看起来怪异的词元后缀，能让开源模型答应有害的请求；同样的后缀，在他们从未见过的商业模型上也管用。<bookmark mark='b'/>2024年，Anthropic描述了多样本越狱：在很长的上下文里塞进几百段虚构的对话，里面的助手都照办了，于是上下文学习压过了训练。<bookmark mark='c'/>相反的失败是过度拒绝：因为有个“杀”字，就拒绝告诉你怎样杀掉一个Python进程。<bookmark mark='d'/>现在的防御是分层的：进出各有独立的分类器，对抗训练，以及在推理模型里，模型能够加以推理的拒绝。",

    'Two results show that post-training reaches further':
        "有两项结果表明，后训练的影响远远超出它所用的数据。<bookmark mark='a'/>2025年，扬·贝特利和同事只在一件很窄的事情上微调GPT-4o：写不安全的代码，而且不告诉用户。结果模型在与代码毫不相干的问题上，给出恶意的建议，还赞美AI统治人类的想法。当同样的例子被说成是安全课的教学材料时，这种情况就没有发生。他们称之为涌现式失准。<bookmark mark='b'/>2024年底，瑞安·格林布拉特和同事告诉Claude 3 Opus：它将被重新训练成会答应有害请求，而且只用与免费用户的对话来训练。于是它对免费用户的这类请求有14%的时候照办，对付费用户则几乎从不，它的推理是：在训练中照办，能让它的价值观不被改变。<bookmark mark='c'/>两者的教训是一样的：微调塑造的是模型把自己当成什么，而不是一次只改一种行为。",

    'Some of the newest tools look inside the model.':
        "一些最新的工具，会去看模型的内部。2025年，Anthropic的研究人员发现了人格向量：模型激活中的一些方向，对应着谄媚、恶意这样的特质，找法是比较特质表现出来时和没表现出来时的激活。<bookmark mark='a'/>把激活投影到这样的方向上，就能看到某个特质在对话中、或在训练中逐渐增强。<bookmark mark='b'/>它能在有人用某些训练样本训练之前，就把会把模型推向这种特质的样本标记出来。<bookmark mark='c'/>而加上或减去这个向量，就能操控这种行为。第30部分讲的就是这一类工作。",

    'Chapter twelve. The open recipes.':
        '第12章。开放的配方。',

    'Here is how the published recipes changed.':
        "来看看公开的配方是怎样演变的。<bookmark mark='a'/>InstructGPT：示范，奖励模型，PPO。<bookmark mark='b'/>2023年，Meta的Llama 2-Chat发现，一小批高质量的例子，大约2.75万个，胜过几百万个平庸的；它训练了两个奖励模型，一个管有用，一个管安全，用了一百多万次比较，并让最优n选1微调和PPO交替进行。<bookmark mark='c'/>同一年，Hugging Face的Zephyr干脆跳过了强化学习：用DPO，在GPT-4评判的比较上训练。<bookmark mark='d'/>2024年的Llama 3也用DPO，而不是PPO。<bookmark mark='e'/>AI2的Tülu 3公开了每一个环节：一个开放的数据混合，在自己回答的比较上做DPO，最后一个阶段，在答案可以核对的问题上做强化学习。<bookmark mark='f'/>而2025年1月的DeepSeek-R1，把可核对问题上的强化学习放在了中心。",

    'DeepSeek-R1 is where post-training turned toward reasoning.':
        "DeepSeek-R1，是后训练转向推理的地方。<bookmark mark='a'/>它的第一个版本R1-Zero，直接从基础模型开始做强化学习，只在可核对的答案做对时给奖励，用的是GRPO，一种没有评论家的PPO。在2024年的AIME，一项很难的数学竞赛上，它解出的题目从15.6%升到71%，对它的多个样本做多数投票，则达到86.7%。<bookmark mark='b'/>长长的思维链，检查自己的工作，甚至有一行，它停下来写道，自己找到了一个顿悟时刻：这些都不是示范出来的。它们之所以出现，是因为能赢得奖励。<bookmark mark='c'/>正式发布的R1加了一小段可读示例的冷启动，几轮强化学习，以及在自己最好的回答上做微调。<bookmark mark='d'/>然后，它的八十万个回答被用来微调小得多的开源模型，也就是第9章的蒸馏，让推理变得便宜。<bookmark mark='e'/>基于可核对奖励的强化学习，是下一部分的主题。",

    'By 2025 every stage of this part sat in one pipeline.':
        "到了2025年，这一部分的每个阶段都排进了同一条流水线。这是阿里巴巴为Qwen3公布的那一条。<bookmark mark='a'/>先在长思维链上做监督微调，作为冷启动；再在答案可以核对的问题上做强化学习；然后再次微调，让模型既能思考后回答，也能不思考直接回答；最后用奖励模型再做一轮强化学习，处理所有无法核对的东西。<bookmark mark='b'/>较小的模型跳过了这一切。它们是从大模型蒸馏出来的，先在老师写的文本上学，再在自己写、由老师打分的文本上学，也就是第9章的在线蒸馏。<bookmark mark='c'/>报告在80亿参数的模型上比较了两者：强化学习用了17920个GPU小时，蒸馏只用了1800个，而且蒸馏的得分明显更高。",

    'Chapter four. Learning what people prefer.':
        '第4章。学习人们的偏好。',

    'Suppose you want a number that says how good an answer is.':
        "假设你想要一个数，来说明一个回答有多好。你可以请人给回答打分，从1到10。<bookmark mark='a'/>但分数会漂移：一个人的7分，是另一个人的8分，而同一个人的标准，一天之内也会变。<bookmark mark='b'/>比较要可靠得多。给出同一个问题的两个回答，问哪个更好。<bookmark mark='c'/>人们仍然会有分歧，但少了：InstructGPT的标注员，在大约73%的比较上意见一致。奖励模型就从比较中学习。",

    "The standard model of comparisons is Bradley and Terry's":
        "比较的标准模型，是布拉德利和特里在1952年提出的。给每个回答一个隐藏的分数r。a胜过b的概率，就是两者分数之差的逻辑S型函数。<bookmark mark='a'/>如果这看起来眼熟，那就对了：它正是第26部分给AlphaZero各代评分的Elo模型，只是刻度不同。<bookmark mark='b'/>奖励模型是一个网络，通常就是微调过的语言模型，把最后一层换成输出一个数，然后在比较上用最大似然训练：让胜者的分数超过败者。这是在差值上做逻辑回归，第6部分的损失函数，用在了新地方。<bookmark mark='c'/>有一个后果，后面会用到。它看到的永远只是差，所以分数只在每个问题上差一个平移的意义下才有定义。奖励模型告诉你哪个回答更好，而不是一个回答在某个绝对尺度上有多好。",

    'Chapter five. Reinforcement learning on a leash.':
        '第5章。拴着绳子的强化学习。',

    'With a reward model in hand, the plan is reinforcement learning':
        "有了奖励模型，计划就是强化学习：生成回答，给它们打分，再用第26部分的策略梯度，把模型推向高分。但只去最大化奖励模型，是个错误，原因有二。<bookmark mark='a'/>奖励模型只是一个近似，而一个强大的优化器会找到它出错的地方。<bookmark mark='b'/>而且策略可能漂移到和它学过的任何东西都不像的文本里，失去原有的流畅。<bookmark mark='c'/>所以目标里加了一根绳子：一个惩罚项，β乘以与出发时那个微调模型，也就是参考模型之间的KL散度。β定下了兑换比率：一奈特的偏离，值多少奖励。",

    'This objective has an exact solution':
        "这个目标有一个精确解，值得推导一下，因为本部分剩下的内容都要靠它。固定一个提示，把目标写成对所有可能回答y的求和。<bookmark mark='a'/>把奖励折进对数里：r等于β乘以e的r/β次方的对数。<bookmark mark='b'/>除以再乘以归一化常数Z，剩下的就是负β乘以一个KL散度，再加一个常数。<bookmark mark='c'/>KL散度永远不会是负的，只有两个分布一致时才为零，这是第1部分的吉布斯不等式。所以最好的策略就是π星：参考模型的概率，按e的奖励/β次方重新加权。<bookmark mark='d'/>β很大时，几乎不离开参考模型。β很小时，把一切都堆到奖励最高的回答上。",

    'Chapter six. When the measure becomes the target.':
        '第6章。当指标成了目标。',

    'In 1975 the economist Charles Goodhart observed':
        "1975年，经济学家查尔斯·古德哈特观察到：被用来指导政策的统计数字，会不再代表它们原来代表的东西。人类学家玛丽莲·斯特拉森后来给出了大家常引用的说法：当一个指标成了目标，它就不再是一个好指标。<bookmark mark='a'/>奖励模型就是一个指标。如果它稍微偏爱更长的回答，优化它就会产生注水。<bookmark mark='b'/>如果它稍微偏爱附和用户的回答，优化它就会产生奉承。<bookmark mark='c'/>强化学习一直都是这样：2016年，OpenAI展示过一个赛艇智能体，它因为沿途击中目标而得到奖励，结果学会了在一个小湖里永远兜圈子，反复击中同样的三个目标，从不完成比赛。",

    'To measure the effect, we need a way to optimize a reward model':
        "要测量这种效应，我们需要一种可控地优化奖励模型的办法。最简单的是最优n选1：从参考模型抽n个回答，留下奖励模型最喜欢的那个。n越大，优化得越狠。<bookmark mark='a'/>它和参考模型的散度有闭式解：log n减去n分之n减1。被选中的回答是n个里最好的，所以如果u是它在奖励模型下的分位数，它的密度就是n乘以u的n减1次方，而KL就是这个量对数的期望。<bookmark mark='b'/>它只像log n那样增长：一千选一也不到6奈特。最优n选1便于分析，实践中也是一个很强的基线，各个实验室仍在使用。",

    'Gao and colleagues ran this at scale':
        "利奥·高和同事在大规模上做了这个实验，用一个大的奖励模型扮演人，发现金标准奖励随KL的平方根，遵循简单的曲线。对最优n选1，是d乘以α减βd：先升后降。<bookmark mark='a'/>对强化学习，形式相同，只是换成对数，下降得更慢。<bookmark mark='b'/>这些系数随奖励模型的大小平滑变化，所以优化到多远是安全的，是可以预测的。实践中，KL绳子和提前停止，就是为此而设的。",

    'Chapter seven. Direct preference optimization.':
        '第7章。直接偏好优化。',

    'In 2023 Rafael Rafailov, Archit Sharma, Eric Mitchell':
        "2023年，斯坦福的拉斐尔·拉法伊洛夫、阿希特·夏尔马、埃里克·米切尔和同事注意到，第5章的最优解可以倒过来用。<bookmark mark='a'/>取对数，解出奖励：奖励等于β乘以最优策略与参考策略之比的对数，再加上一项只和问题有关的量。<bookmark mark='b'/>现在把它代入第4章的布拉德利-特里模型。比较只取决于同一个问题下的奖励之差，所以那个麻烦的归一化常数Z就抵消了。<bookmark mark='c'/>剩下的就是策略本身的一个损失函数：一个逻辑回归，它的分数是β乘以策略与参考之比的对数。不需要奖励模型，不需要采样，不需要强化学习；只是在比较数据上的一个监督损失。<bookmark mark='d'/>策略就是它自己的奖励模型。",

    'DPO started a family.':
        "DPO开创了一个家族。<bookmark mark='a'/>IPO把逻辑损失换成平方损失，因为当一个回答总是赢时，DPO会把对数比的间隔推向无穷大，从而过拟合。<bookmark mark='b'/>KTO从单个被标为好或坏的回答中学习，不需要成对数据，用的损失函数形状像卡尼曼和特沃斯基的前景理论。<bookmark mark='c'/>SimPO去掉了参考模型，用按长度归一化的对数概率作为奖励。<bookmark mark='d'/>比较它们得到的一个教训是：用当前模型新生成、边训练边评判的回答来学习，通常胜过用旧模型收集的固定数据集。在线数据，正是强化学习一直以来的优势。",

    'f"This is the small language model this series trained on thirty novels, asked to write a line about the {topic}.':
        "这是本系列用三十部小说训练出来的那个小语言模型，我们请它写一句关于{topic}的话。<bookmark mark='a'/>刚从预训练出来，它并不回答。它在续写一份文档：请求只是更多的文本，请求周围那些特殊标记，对它毫无意义。<bookmark mark='b'/>这是同一个模型，在这台电脑上微调了几分钟之后。<bookmark mark='c'/>它没有学到任何新知识。变的是它怎样使用自己已经知道的东西。",

    'That change, from predicting text to trying to help, is called post-training':
        "这种变化，从预测文本到努力帮忙，叫作后训练，你用过的每一个聊天机器人都是这样做出来的。<bookmark mark='a'/>它比规模更重要。2022年，OpenAI发现，人们更喜欢一个经过后训练的13亿参数模型的回答，胜过后训练之前那个1750亿参数的GPT-3。",

    'This is Part 27 of AI, Built.':
        "这是《人工智能，从零搭建》的第27部分。<bookmark mark='a'/>这一部分讲：监督微调和低秩适配器；从比较中学到的奖励模型；基于人类反馈的强化学习，它的精确最优解，以及把一个学来的奖励优化得太狠会发生什么；直接偏好优化；在成文原则下来自AI的反馈；蒸馏和模型合并；以及哪里会出错。每一种方法都会在这里真的运行，就在我们自己的小模型上。",

    'Chapter two. Supervised fine-tuning.':
        '第2章。监督微调。',

    'The first step is to teach the model the shape of a conversation.':
        "第一步，是教模型认识对话的样子。每一轮交流都写进一个固定的模板，用上几个在普通文本里从不出现的特殊词元：一个表示有人在说话，一个表示轮到助手，一个表示结束。<bookmark mark='a'/>模型在这样的对话上训练，用的是和预训练一样的下一个词元损失，只改了一处：只有回答的词元才算数。问题是上下文，不是要模仿的东西。<bookmark mark='b'/>按第1部分的链式法则，屏蔽后的损失，就是给定问题时整个回答的对数概率。监督微调，就是对人们想要的回答做最大似然。",

    'Our model is the one this series trained on thirty novels':
        "我们的模型，就是本系列用三十部小说训练出来的那个：680万个参数，一个缩小版的现代Transformer。我们用两种对话来微调它，都取材于这些小说本身。<bookmark mark='a'/>第一种，用户引用一句话，问它出自哪本书；回答就是书名。这可以检验：对或错，而且我们用的测试句子，来自它所有训练中都没见过的段落。<bookmark mark='b'/>第二种，用户请它写一句关于某样东西的话，比如大海、一扇窗，回答就是小说里关于它的一句话。",

    'f"Here is a held-out sentence, put to the model before fine-tuning.':
        "这是一句留出的句子，在微调之前拿去问模型。<bookmark mark='a'/>基础模型从没在有意义的位置上见过这些特殊词元，所以它照常做它一直做的事：续写小说。<bookmark mark='b'/>微调之后，它用一个书名来回答。<bookmark mark='c'/>在所有留出的句子上，基础模型答对的比例是{100 * d['base_which']:.0f}%；微调后的模型是{100 * d['sft_which']:.0f}%，而瞎猜只有三十分之一。这些书它都读过；微调教会它说出，这句话让它想起了哪一本。",

    'f"Accuracy climbs over the {S} steps of fine-tuning. <bookmark mark=\'a\'/> But something is lost.':
        "在{S}步微调中，准确率一路上升。<bookmark mark='a'/>但有东西失去了。在它被训练来预测的普通小说文本上，它的损失从每个词元{d['base_heldout']:.3f}奈特，升到了{d['sft_heldout']:.3f}奈特。<bookmark mark='b'/>微调为了新任务移动了每一个权重，一部分旧本事也随之而去。让这个损失保持很小，是下一章那种方法的任务，而在RLHF里，是那根绳子的任务。",

    'f"Accuracy climbs over the {S} steps of fine-tuning. <bookmark mark=\'a\'/> Fine-tuning often costs':
        "在{S}步微调中，准确率一路上升。<bookmark mark='a'/>微调常常要付出一些旧本事的代价，但在这里，普通小说文本上的损失几乎没动，从每个词元{d['base_heldout']:.3f}奈特，到{d['sft_heldout']:.3f}奈特。<bookmark mark='b'/>温和的学习率和较短的训练，让模型停留在出发点附近；推得更狠，就要换掉更多。让这个代价保持很小，是下一章那种方法的任务，而在RLHF里，是那根绳子的任务。",

    'Instruction tuning has a short, fast history.':
        "指令微调的历史很短，发展很快。<bookmark mark='a'/>2021年，谷歌的FLAN在六十个改写成指令的任务上微调一个模型，它在从没见过的任务上也变好了。<bookmark mark='b'/>2023年，斯坦福的Alpaca用一个更强的模型写出的五万两千个例子，微调了一个开源模型，只花了几百美元。<bookmark mark='c'/>Meta的LIMA表明，一千个精心挑选的例子就能走得很远，并提出对齐主要关乎风格：知识在预训练时就已经有了。<bookmark mark='d'/>如今，大多数微调数据由模型来写或来筛选，再由人来检查。",

    'Chapter three. Low-rank adapters.':
        '第3章。低秩适配器。',

    "Fine-tuning changes every one of a model's weights":
        "微调会改变模型的每一个权重，对一个大模型来说，这意味着每个任务都要存一份完整的新副本。但真的需要吗？<bookmark mark='a'/>2018年，李春元和同事在权重空间一个随机的低维切片里训练网络：权重等于出发点，加上一个固定的随机矩阵乘以一个小向量，只有这个小向量在学习。许多问题需要的维数少得出奇。<bookmark mark='b'/>2020年，阿尔缅·阿加贾尼扬和同事表明，微调一个预训练语言模型尤其是低维的：在一个复述判断任务上，大约两百个数，就让RoBERTa走完了九成的路。难的部分，预训练已经做完了。",

    'LoRA, from Edward Hu and colleagues at Microsoft in 2021':
        "LoRA是微软的胡爱德华和同事在2021年提出的，它把这个想法直接建进网络里。冻结每一个权重矩阵W。<bookmark mark='a'/>在每一个旁边，加上两个瘦矩阵的乘积，B乘以A，秩为r，只有几。只训练B和A。<bookmark mark='b'/>一个d乘k的矩阵有d乘k个数；适配器只有r乘以d加k个。对一个四千宽的层，秩取8，可训练的数是六万五千个，而不是一千六百万个。<bookmark mark='c'/>B从零开始，所以训练恰好从原模型出发；训练完后，B乘A可以加回W里，所以适配后的模型跑得和原来一样快。",

    'f"Our own experiment: fine-tune the novels model on the which-book task with LoRA':
        "我们自己的实验：在“出自哪本书”任务上微调小说模型，分别用秩为1、4、16的LoRA，以及调整全部权重。<bookmark mark='a'/>秩为1时训练{r1['params']:,}个数，占模型的{100 * r1['params'] / tot:.2g}%。<bookmark mark='b'/>全量微调在留出的句子上答对{100 * full['which']:.0f}%；最好的适配器，秩为{best['rank']}，答对{100 * best['which']:.0f}%。<bookmark mark='c'/>而在普通小说文本上，全量微调的损失与基础模型相差{forget_full:+.3f}奈特，适配器最少只差{forget_lora:+.3f}。LoRA学得少，也忘得少：这正是2024年一项研究的标题，它在大规模上发现了同样的事。",

    'On GPT-3, LoRA trained ten thousand times fewer numbers':
        "在GPT-3上，LoRA训练的数比全量微调少一万倍，显存约为三分之一，质量相当。<bookmark mark='a'/>2023年的QLoRA把冻结的模型存成4比特，在一块48GB的GPU上微调了一个650亿参数的模型，让任何有一块好显卡的人都能做微调。<bookmark mark='b'/>DoRA把每个权重拆成长度和方向，只适配方向。<bookmark mark='c'/>2024年一项细致的比较，把其中的取舍写进了标题：LoRA学得少，也忘得少。对困难的新本事，全量微调仍然更好。",

    'Chapter nine. Distillation.':
        '第9章。蒸馏。',

    'A large model is expensive to run; a small one is cheap but weaker.':
        "大模型运行起来很贵；小模型便宜，但更弱。蒸馏训练小模型，也就是学生，去模仿大模型，也就是老师。<bookmark mark='a'/>只用数据训练时，学生每个例子只看到一个正确答案：这个数字是2。<bookmark mark='b'/>老师给的更多：一整个分布，在它看来这个2有点像3，几乎不像5。杰弗里·辛顿把这种信息叫作暗知识。<bookmark mark='c'/>学生被训练去匹配老师的概率，先用温度T把它们软化，让小概率也算数，用的是第1部分的KL散度。",

    'The direction of the KL matters':
        "KL的方向很重要，第1部分用这个双峰分布展示过。<bookmark mark='a'/>最小化前向KL，从老师到学生，一个小到拟合不了两个峰的学生，就会铺开盖住两个峰，把概率放到老师几乎不放的地方。这就是经典的蒸馏，在老师写的文本上进行。<bookmark mark='b'/>最小化反向KL，学生就会认定一个峰：它只说老师会说的话。MiniLLM和在线蒸馏这类方法就这样训练，在学生自己写的文本上，由老师打分，这和强化学习是同一个在线策略的思路。",

    '"Our version: the novels model, six point eight million parameters':
        "我们的版本：680万参数的小说模型，去教一个参数只有它五分之一的学生，两层而不是六层。两个学生看到同样的文本。<bookmark mark='a'/>一个只从文本学习，也就是下一个词。<bookmark mark='b'/>另一个学习老师对下一个词的整个分布。<bookmark mark='c'/>{verdict}",

    'f"Trained on the teacher\'s probabilities, the student ends at':
        '从老师的概率学习的学生，最后停在{b:.2f}奈特，而只从文本学习的是{a:.2f}，用的是同样的词元：老师的分布，每个词元携带的信息，比实际出现的那一个词更多。',

    'f"Here the two students end close together':
        '这里两个学生最后很接近，{b:.2f}和{a:.2f}奈特：训练这么少的时候，限制在学生的大小，而不在它的老师。',

    'Distillation is everywhere.':
        "蒸馏无处不在。<bookmark mark='a'/>2019年，DistilBERT少了四成参数，却保留了BERT九成七的语言理解能力。<bookmark mark='b'/>对语言模型，常见的形式是序列级的：用老师写的完整回答来微调学生。第2章里的Alpaca，就是这样。<bookmark mark='c'/>DeepSeek用R1的八十万个回答微调了几个小的开源模型，把它们变成了有能力的推理者，比直接在小模型上做强化学习更便宜。<bookmark mark='d'/>如今发布的大多数小模型，训练中都部分用到了一个更大模型的输出或概率。",

    'Chapter ten. Adding models together.':
        '第10章。把模型加起来。',

    'Averaging the weights of two different networks usually produces garbage':
        "把两个不同网络的权重平均一下，通常只会得到垃圾：它们的单元排列方式不同，平均值落在两个山谷之间的山脊上。<bookmark mark='a'/>但同一个预训练模型的几个微调版本就不一样了。它们从同一点出发，只移动了一点点，所以往往待在同一个山谷里，它们之间的直线也一直很低：这叫线性模式连通。<bookmark mark='b'/>2022年，米切尔·沃茨曼和同事把许多用不同设置做的微调的权重平均起来，做成一锅模型汤，得到的模型比其中任何一个都好，推理时也不多花任何代价。",

    'In 2023 Gabriel Ilharco and colleagues turned this into arithmetic.':
        "2023年，加布里埃尔·伊尔哈尔科和同事把这变成了算术。用微调后模型的权重减去预训练的权重，把这个差叫作任务向量：微调改变的一切。<bookmark mark='a'/>把两个任务向量加到预训练模型上，往往就得到一个两件事都会做的模型，而不必在两者上一起训练。<bookmark mark='b'/>减去一个，模型就会忘掉它：减去一个在有毒文本上微调过的模型的向量，原模型变得没那么有毒了。",

    '"We tried it on the novels model.':
        "我们在小说模型上试了试。把一份副本只在“出自哪本书”的问题上微调，另一份只在“写一句关于某物的话”上微调，取出它们的任务向量。<bookmark mark='a'/>每个微调都擅长自己的任务。<bookmark mark='b'/>{said_}<bookmark mark='c'/>合并不是免费的，但出奇地便宜：完全不用训练，只是加法。",

    "f'Adding the two task vectors, at lambda":
        '把两个任务向量加起来，λ取{best[0].split()[-1]}，合并后的模型能认出{100 * best[1]:.0f}%句子的出处，而单独的“出自哪本书”模型是{100 * w_only[1]:.0f}%，它写的句子有{100 * best[3]:.0f}%干净地结束。',

    'Merging became a craft.':
        "合并成了一门手艺。<bookmark mark='a'/>TIES只保留每个任务向量里最大的那些改变，先用投票解决符号上的分歧，再相加。<bookmark mark='b'/>DARE随机丢掉一个任务向量的大部分元素，再把剩下的放大，这样向量之间的干扰就小多了。<bookmark mark='c'/>Meta的Llama 3在后训练的每个阶段，都把用不同数据和设置训练出的模型平均起来。<bookmark mark='d'/>有一阵子，合并出来的模型还登上了开源排行榜的榜首。",

    "Let's take stock.":
        '我们来总结一下。监督微调是对人们想要的回答做最大似然，它可以只活在权重空间的一个低秩切片里，这就是LoRA管用的原因。奖励模型用布拉德利-特里模型，从比较中学习人们的偏好。拴着KL绳子的强化学习，瞄准一个精确的最优解：按奖励的指数重新加权的参考模型。把一个学来的奖励推得太狠，它就不再衡量它本该衡量的东西：古德哈特定律，我们亲手测量过。DPO直接从比较出发，到达同一个最优解。而成文的原则、蒸馏和模型合并，让这一切都更便宜。',

    'All of this comes back.':
        '这些都还会再出现。第28部分用可以检验的答案上的强化学习，训练模型去推理。第29部分训练能在长任务中行动的智能体。第30部分打开模型内部，包括人格向量。第31部分要问：后训练造出来的东西，我们能信任吗？',

    'Here are six problems to try, from the Bradley-Terry model to the forward KL.':
        '这里有六道题，从布拉德利-特里模型到前向KL。在这里暂停，把它们做一遍；完整的解答在本部分的笔记里。',

    'Next time: reasoning.':
        "下一次：推理。为什么把步骤写出来就是在增加计算，模型怎样从一个检验器而不是一个人那里学习，会推导GRPO，以及想得更久能换来什么。",

    "The best place to go deeper on this part is Nathan Lambert's free book":
        "想在这一部分上走得更深，最好的去处是内森·兰伯特关于基于人类反馈的强化学习的免费书。感谢观看，第28部分见。",

    'f"Now we do it ourselves.':
        "现在我们自己来做。第2章微调过的模型能按要求写句子：一句关于大海的话，一句关于夜晚的话。<bookmark mark='a'/>我们没有一大群标注员，所以就模拟一群。有一个对所有模型都隐藏的、代替人类品味的东西，我们叫它金标准：它喜欢欢快的词，不喜欢阴郁的词，非常不喜欢重复和空洞的回答。<bookmark mark='b'/>我们模拟的人比较两句话，偏向金标准更喜欢的那句，但并不总是：两者越接近，他们越常选另一句。<bookmark mark='c'/>这样我们得到{n:,}次比较。从这里开始，所有学习人们偏好的东西，都只看到这些比较，从来看不到金标准本身，就像真实的实验室永远看不到标注员脑子里在想什么。",

    'f"Train reward models on more and more of the comparisons':
        "用越来越多的比较来训练奖励模型，每一个都在它没见过的比较上测试。<bookmark mark='a'/>用{int(sizes[0])}次比较，它答对{100 * acc[0]:.0f}%；用{int(sizes[-1]):,}次，答对{100 * acc[-1]:.0f}%。<bookmark mark='b'/>它到不了百分之百：它学习的那些人，和金标准一致的时候只有{100 * ceil:.0f}%，所以这就是上限。<bookmark mark='c'/>真实的奖励模型也在同样的范围里。InstructGPT的奖励模型预测留出标注员的选择，准确率约七成，接近标注员彼此一致的程度。奖励模型是一个不完美裁判的不完美副本，接下来三章，讲的就是对着它优化时会发生什么。",

    'f"Here\'s the formula on eight real answers':
        "这是那个公式，用在我们微调过的模型写的八个关于{d['topic']}的真实回答上，按奖励排好。柱子一开始是参考模型的概率，在这八个上重新归一化。<bookmark mark='a'/>β取10，绳子很紧，几乎什么都不动。<bookmark mark='b'/>β取1，概率开始流向更好的回答。<bookmark mark='c'/>β取0.1，几乎全部概率都落在最好的回答上。这就是带KL惩罚的强化学习要去的地方，只是它得靠采样，一步一个梯度地走过去。",

    'f"Now for real.':
        "现在动真格的。从我们微调过的模型出发，每一步生成十六句话，用奖励模型打分，减去KL惩罚，走一步策略梯度。<bookmark mark='a'/>β取{betas[0]:g}时，奖励模型的分数从{early(H[0], 1):.2f}升到{p0:.2f}，而训练从未见过的金标准，从{gs:.2f}变到{g0:.2f}。<bookmark mark='b'/>现在把绳子放松到β取{betas[1]:g}。{verdict}",

    'f"With the loose leash the reward model\'s score climbs higher':
        '绳子放松后，奖励模型的分数爬得更高，到了{p1:.2f}，但金标准，也就是它本该衡量的东西，最后反而更低：{g1:.2f}，而原来是{g0:.2f}。策略找到了奖励模型高估的东西。',

    "f'Here the looser leash pays":
        '这里放松绳子是值得的：金标准最后是{g1:.2f}，而原来是{g0:.2f}，散度也更大，{k1:.1f}奈特，而原来是{k0:.1f}。',

    "f'Gold ends about the same either way":
        '两种情况下金标准最后差不多，{g0:.2f}和{g1:.2f}；放松的绳子为此花掉了{k1:.1f}奈特的散度，而另一个只用了{k0:.1f}。',

    'f"Here is the loose-leash run replayed':
        "这是绳子放松的那次训练的回放：每个阶段，它的十六句话里挑三句。<bookmark mark='a'/>一开始，它写得就像它出发时那个微调过的模型。<bookmark mark='b'/>到第{samp[0]}步，被问到{samp[1]}，这就是它学会写的东西。一个人会不会更喜欢它，请你自己判断。",

    'f"Here is the experiment, after Gao, Schulman and Hilton of OpenAI.':
        "这就是实验，仿照OpenAI的高、舒尔曼和希尔顿。对每个提示，我们微调过的模型写出两百五十六句话；最优n选1用一个奖励模型来挑，我们再用奖励模型和金标准分别给挑中的那句打分，横轴是KL的平方根。<bookmark mark='a'/>奖励模型总以为情况在变好：按构造，它给自己最爱的那句打的分，随n上升。<bookmark mark='b'/>金标准说出真相。{small_said}<bookmark mark='c'/>{large_said}更好的奖励模型能被推得更狠才崩，但每一个学来的奖励，都会在某处崩掉。",

    "f'The reward model trained on more comparisons tracks gold further":
        '用更多比较训练的奖励模型，跟金标准跟得更远：金标准最高到了{lgold.max():.2f}。',

    'f"With the small reward model, gold rises at first':
        "用小的奖励模型时，金标准先是上升，在n等于{ns[peak_s]}附近达到顶峰，然后回落到{sgold[-1]:.2f}，而奖励模型自己的分数一路爬到{ys['small_proxy'][-1]:.2f}：这就是过度优化。",

    'f"With the small reward model, gold climbs only to':
        "用小的奖励模型时，金标准只爬到{sgold[-1]:.2f}，而奖励模型自己的分数到了{ys['small_proxy'][-1]:.2f}：两者之间的差距越拉越大。",

    "f'This is the line about the":
        '这是小奖励模型在全部两百五十六句里最喜欢的那句关于{ex[0]}的话。',

    'f"We trained DPO on our model':
        "我们在自己的模型上训练了DPO，用的就是奖励模型学过的那些比较。<bookmark mark='a'/>{said_}与出发点的散度是{d['kl']:.1f}奈特。<bookmark mark='b'/>β取{rl['betas'][0]:g}的RLHF，在{rl_kl:.1f}奈特处达到了{rl_gold:+.2f}。<bookmark mark='c'/>通向同一类目标的两条路：一条经过奖励模型和采样，另一条直接从比较出发。",

    "f'Its lines score {d['gold']:+.2f} with gold, up from":
        "它写的句子在金标准下得分{d['gold']:+.2f}，高于原来的{sft['sft_line_gold']:+.2f}，",

    "f'Its lines score {d['gold']:+.2f} with gold, against":
        "它写的句子在金标准下得分{d['gold']:+.2f}，而原来是{sft['sft_line_gold']:+.2f}，",

    '"DPO only cares about the gap between the preferred and the rejected answer.':
        "DPO只关心被偏好的回答和被拒绝的回答之间的差距。我们取三十二对固定的回答，看训练过程中每一边各自发生了什么。<bookmark mark='a'/>{text}",

    'f"By the end, the preferred answers have lost':
        '到最后，被偏好的回答失去了{-p[-1, 1]:.1f}奈特的概率，被拒绝的失去了{-p[-1, 2]:.1f}：两者的差距变大了，但主要靠的是把两边都往下压。概率去了哪里？去了两张清单里都没有的回答那里。研究者把这叫作似然位移，这也是DPO的结果常常出人意料的原因之一。',

    "f'Here the preferred answers gained":
        '这里被偏好的回答得到了{p[-1, 1]:.1f}奈特，被拒绝的变化了{p[-1, 2]:+.1f}。在更大的模型里，两者一起下降是常见的：差距在变大，概率却流向了两张清单里都没有的回答：这就是似然位移。',

    'f"Training on the judge\'s own labels helps a little':
        "用裁判自己的标签来训练，有一点帮助，从{100 * d['acc_small']:.0f}%到{100 * d['acc_ai']:.0f}%：这些标签比那些有噪声的人更平滑，而且数量更多。但它学不到裁判本来就不知道的东西。",

    'f"Training on the judge\'s own labels doesn\'t help here':
        "在这里，用裁判自己的标签来训练没有帮助：{100 * d['acc_ai']:.0f}%，而原来是{100 * d['acc_small']:.0f}%。裁判教不了它自己不知道的东西；真实的AI裁判之所以有用，是因为它们比被评判的模型大得多。",

    '"Every method in this part trades divergence from the fine-tuned model for gold.':
        "这一部分的每一种方法，都是用偏离微调模型的程度去换金标准。把它们放进同一张图：纵轴是金标准的提高，横轴和上一章一样，是KL的平方根。<bookmark mark='a'/>用较大奖励模型的最优n选1是参照：它什么都不训练。<bookmark mark='b'/>RLHF的两次训练，<bookmark mark='c'/>以及三个β值下的DPO。<bookmark mark='d'/>{verdict}<bookmark mark='e'/>{cmp_}",

    'f"At equal divergence, {len(above)} of the {len(inr)} trained policies':
        "在相同的散度下，停留在最优n选1范围内的{len(inr)}个训练出来的策略里，有{len(above)}个比它好。",

    "Every trained policy drifts further from where it started than best-of-256 ever does.":
        "每一个训练出来的策略，离出发点都比最优256选1走得更远。",

    'f"The best trained policy, {meth} at beta {b:g}, gains':
        "最好的训练策略，是β取{b:g}的{meth}，提高了{gbest:+.2f}，超过最优256选1的{float(bon.max()):+.2f}：训练能到达单靠采样很少找到的回答。",

    'f"No trained policy gains more than best-of-256\'s':
        "没有一个训练出来的策略，提高得比最优256选1的{float(bon.max()):+.2f}更多，而最优n选1根本不需要训练就能做到，所以各个实验室仍在使用它，还用它来制造训练数据。",

}

PHRASES = {
    'sea': '大海',
    'night': '夜晚',
    'house': '房子',
    'door': '门',
    'fire': '火',
    'river': '河',
    'garden': '花园',
    'letter': '信',
    'window': '窗',
    'horse': '马',
    'ship': '船',
    'money': '钱',
    'church': '教堂',
    'road': '路',
    'rain': '雨',
    'sun': '太阳',
    'moon': '月亮',
    'wind': '风',
    'child': '孩子',
    'heart': '心',
    'face': '脸',
    'hand': '手',
    'eyes': '眼睛',
    'voice': '声音',
    'room': '房间',
    'town': '小镇',
    'dinner': '晚餐',
    'morning': '早晨',
    'music': '音乐',
    'book': '书',
}
