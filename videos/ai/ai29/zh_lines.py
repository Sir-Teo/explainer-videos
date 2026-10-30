"""Chinese narration for ai29: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第29部分：智能体与世界'

CHAPTERS = {
    'Hook': '一连许多步',
    'History': '1. 从Shakey到智能体',
    'Belief': '2. 看不全，也要行动',
    'Loop': '3. 智能体循环',
    'Memory': '4. 记忆，以及多个智能体',
    'Compound': '5. 误差的累积',
    'Doubling': '6. 不断翻倍的时间跨度',
    'Coding': '7. 编程智能体',
    'Computer': '8. 使用电脑',
    'Imitation': '9. 模仿学习',
    'DAgger': '10. DAgger',
    'World': '11. 世界模型',
    'Dreamer': '12. Dreamer：在梦里学习',
    'Genie': '13. 可以走进去的世界',
    'SimToReal': '14. 从仿真到现实',
    'VLA': '15. 视觉–语言–动作模型',
    'Fast': '16. 动作词元，以及机器人基础模型',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    'f"A chatbot answers one question.':
        "聊天机器人，回答一个问题就够了。<bookmark mark='j'/>智能体却要完成一整项工作：30步、100步、1000步，每一步都取决于上一步。"
        "<bookmark mark='a'/>就算每一步都有97%的把握，连着走30步，也只有{100 * p ** n:.0f}%的时候能全部做对。",

    'f"Here are {R} attempts at once.':
        "这里是同时进行的{R}次尝试。<bookmark mark='a'/>每走一步，就又有几次出了错；而一次尝试一旦出错，就会一直错下去。"
        "<bookmark mark='b'/>到了第30步，{R}次里还有{k}次走在正轨上。",

    'This is Part 29 of AI, Built: agents and worlds.':
        "这是《人工智能，从零搭建》的第29部分：智能体与世界。<bookmark mark='a'/>我们从历史讲起：从第一个会做计划的机器人，"
        "到第一批自己开车的汽车；还要讲，看不全的时候该怎样行动。<bookmark mark='r2'/>然后是每个语言模型智能体都在运行的那个循环，"
        "以及它的工具和记忆。<bookmark mark='r3'/>然后是长时程：为什么误差会累积，智能体的时间跨度增长得有多快，"
        "编程智能体和使用电脑的智能体又是怎样被衡量的。<bookmark mark='r4'/>然后是模仿：为什么照搬专家会失败，"
        "而且失败的程度随任务长度的平方增长。<bookmark mark='r5'/>然后是世界模型，包括一个在这台电脑上训练的小Dreamer，"
        "<bookmark mark='r6'/>最后是机器人：从仿真走向现实，以及把图像和文字变成动作的模型。",

    # ---------------------------------------------------------------- History
    'Chapter one. From Shakey to agents.':
        '第1章。从Shakey到智能体。',

    'The story of agents starts in a few rooms':
        "智能体的故事，开始于斯坦福研究所的几个房间。1966年到1972年，尼尔斯·尼尔森、查尔斯·罗森和同事们造出了Shakey，"
        "第一个能对自己的行动进行推理的移动机器人。<bookmark mark='a'/>它用一台电视摄像机来看，<bookmark mark='b'/>用逻辑来做计划，"
        "<bookmark mark='c'/>然后才动起来，动得那么慢，摇摇晃晃，它的名字就是这么来的。<bookmark mark='d'/>它的副产品比它活得更久："
        "第2部分的A星搜索，STRIPS规划器，还有一种在图像里找直线的更好办法。<bookmark mark='e'/>它还定下了一个延续几十年的模式："
        "感知世界，为它建一个模型，做计划，行动，然后再感知。",

    'The next leap came from the desert.':
        "下一次飞跃，来自沙漠。2004年3月，美国国防部的研究机构DARPA悬赏一百万美元，给任何一辆能自己穿越莫哈韦沙漠、"
        "开大约140英里的机器人汽车。<bookmark mark='a'/>没有一辆接近终点：最好的，卡内基梅隆大学的Sandstorm，开了大约7英里，"
        "就卡在了一道路堤上。<bookmark mark='b'/>18个月后，有五辆车跑完了132英里的赛道，斯坦福大学的Stanley用不到7个小时夺冠。"
        "<bookmark mark='c'/>带来这个差别的，是学习：Stanley用激光雷达在近处测到的结果当作标签，自己学会了在摄像头画面里认出远处的路。"
        "<bookmark mark='d'/>2007年的城市挑战赛，让这些车开进车流，周围是停车标志和别的机器人；六辆跑完全程，卡内基梅隆大学的Boss获胜。"
        "参加这些比赛的工程师，后来造出了今天的自动驾驶汽车。",

    'Meanwhile robots began to learn their skills':
        "与此同时，机器人开始学习自己的本领，而不再全靠编程。<bookmark mark='a'/>1989年，迪恩·波默洛的ALVINN用一个小小的神经网络，"
        "模仿人类司机，驾驶一辆面包车沿着道路行驶，这正是第9章的思路。<bookmark mark='b'/>2016年，谢尔盖·莱文、切尔西·芬恩和同事们"
        "训练了一个从摄像头像素直接到电机力矩的网络；同一年，谷歌一屋子的机械臂，从几十万次尝试中学会了抓取。"
        "<bookmark mark='c'/>2019年，OpenAI的一只机械手解开了魔方，它只在模拟中训练过，而这些模拟它从来没有完全信任过。"
        "<bookmark mark='d'/>2022年，语言模型开始为机器人决定下一步该做什么；而谷歌的RT-1，一个Transformer，从13万次示范中学会了700项任务。",

    'The newest agents grew out of language models.':
        "最新的智能体，是从语言模型里长出来的。<bookmark mark='a'/>2021年，OpenAI的WebGPT学会了上网搜索，并引用它找到的内容。"
        "2022年，ReAct让模型在思考和行动之间交替。<bookmark mark='b'/>2023年，模型学会了调用工具，从计算器，到任何用几行JSON描述的程序。"
        "<bookmark mark='c'/>2024年，智能体在真实的代码库里修复真实的bug，还开始使用电脑的屏幕和鼠标；<bookmark mark='d'/>到2025年，"
        "它们能在终端里连续写很长时间的代码，到2026年，能连着干上好几个小时。<bookmark mark='e'/>这一切的底下，是同一个循环，"
        "比Shakey还要古老：行动，看看发生了什么，再做决定。这一部分剩下的内容，讲的就是这个循环，在软件里，也在物理世界里。",

    # ---------------------------------------------------------------- Belief
    'Chapter two. Acting without seeing everything.':
        '第2章。看不全，也要行动。',

    'f"Here\'s the classic example: a robot in a corridor':
        "这里有一个经典的例子：一条走廊，有几扇门，走廊里有一个机器人，它不知道自己在哪里。它所知道的，是一份信念：每个格子一个概率，"
        "一开始平均分布。<bookmark mark='a'/>每一步，它都往右走一格，有时会打滑，于是信念跟着往右挪，也变得更模糊。然后它感知一下："
        "有门，还是没有门；第5部分的贝叶斯法则，把每个格子的信念，乘以这个格子能多好地解释它看到的东西。<bookmark mark='b'/>看，"
        "门的排列方式渐渐暴露出它的位置，不确定性也随之下降：从{ent[0]:.1f}比特{end}<bookmark mark='c'/>这就是第7部分的隐马尔可夫模型，"
        "向前运行，再加上机器人自己的移动。",

    "f'to {ent[-1]:.1f} bits, with its best guess right":
        "降到{ent[-1]:.1f}比特，它最有把握的猜测，正是机器人所在的位置。",

    "f'to {ent[-1]:.1f} bits, with its best guess still":
        "降到{ent[-1]:.1f}比特，可它最有把握的猜测，还差了不止一格。",

    'An agent acts in a world it can only partly see.':
        "智能体所在的世界，它只能看到一部分。第26部分的马尔可夫决策过程，假定智能体能看到状态。<bookmark mark='a'/>去掉这个假定，"
        "就得到部分可观测马尔可夫决策过程，POMDP。<bookmark mark='b'/>世界仍然有一个状态，智能体一行动，它就往前变化。"
        "<bookmark mark='c'/>但智能体得到的只是一个观测，一条线索，它服从一个取决于状态的分布。<bookmark mark='d'/>卡尔·约翰·奥斯特伦"
        "在1965年指出了该怎么做：给每个状态记一个概率，也就是信念，然后依据信念来行动。",

    'Where did that update come from?':
        "这个更新是从哪里来的？新的信念，是智能体做了动作、得到观测之后，每个状态的概率。<bookmark mark='a'/>贝叶斯法则把它倒过来："
        "从每个状态出发看到这个观测的可能性，乘以看到它之前这个状态的可能性。<bookmark mark='b'/>而这个先验，就是旧信念经过状态转移"
        "推出来的：预测。<bookmark mark='c'/>合在一起，η只是让它加起来等于1：先预测，再修正。<bookmark mark='d'/>去掉动作，"
        "它恰好就是第7部分隐马尔可夫模型的前向递推。把表格换成高斯分布，它就是在地图上追踪一辆汽车的卡尔曼滤波。",

    'The belief is more than bookkeeping.':
        "信念不只是记账。<bookmark mark='a'/>它概括了智能体看到过、做过的一切：历史里再没有别的东西，能对现在说得更多。"
        "所以POMDP就是一个普通的MDP，只不过它的状态是信念；第26部分的贝尔曼方程照样适用，只是状态变成了连续的一大片。"
        "这就是为什么精确求解POMDP那么难，也是为什么最优策略有时会只为了获得信息而行动：走到一扇门前，弄清楚自己在哪里。"
        "<bookmark mark='b'/>语言模型智能体没有显式的信念。扮演这个角色的，是它的上下文窗口：它到目前为止读过、做过的一切，"
        "它必须从中推断出眼下是什么情况。",

    # ---------------------------------------------------------------- Loop
    'Chapter three. The agent loop.':
        '第3章。智能体循环。',

    'A language model only writes text.':
        "语言模型只会写文字。要把它变成智能体，就把它放进一个循环。<bookmark mark='a'/>上下文从一项任务开始。模型先写下一个想法，"
        "<bookmark mark='b'/>再写下一个动作，用程序能读懂的格式：搜索这个，运行那个。<bookmark mark='c'/>程序执行这个动作，"
        "把结果作为观测，贴回上下文里。<bookmark mark='d'/>模型把一切重新读一遍，写下一个想法和动作，直到写出答案。"
        "<bookmark mark='e'/>这种推理和行动交替进行的模式，是姚顺雨和同事们在2022年命名的，叫ReAct。只在提示里放一两个示例，"
        "它就在两个文字任务上，胜过了用模仿学习和强化学习训练出来的智能体。",

    'f"Here is a loop running for real, in a small warehouse':
        "这是一个真正在运行的循环，在我们自己的一个小仓库里。工具就是几个函数：列出一个货架，查一个价格，做加法。"
        "<bookmark mark='a'/>任务是：三件东西一共多少钱？智能体的每一步出自一段脚本，错误率由我们设定，而不是来自语言模型，"
        "这样我们就能数清楚哪里出了错。<bookmark mark='b'/>它查一个价格，读观测，记下累计的总数。<bookmark mark='c'/>{slip}"
        "工具回了一个错误，错误进入上下文，智能体就再试一次。<bookmark mark='d'/>能看到每个动作的结果，"
        "正是它能纠正过来的原因：{verdict}",

    'Here it misspells an item once.':
        "这里它把一个物品的名字拼错了一次。",

    "f'Here it misspells an item {n_err} times.'":
        "这里它把一个物品的名字拼错了{n_err}次。",

    "f'the answer, {total}, is right.'":
        "答案{total}，是对的。",

    'even so, this answer is wrong.':
        "即便如此，这个答案还是错的。",

    'How does a model learn to use tools at all?':
        "模型到底是怎样学会使用工具的？<bookmark mark='a'/>2023年2月，Meta的Toolformer自学成才：它试着在普通文本里插入对计算器或"
        "搜索引擎的调用，保留那些结果能让后面的词更容易预测的调用。<bookmark mark='b'/>2023年6月，OpenAI把它做成了产品。"
        "程序用一份模式说明向模型描述每个工具：名字，用途，参数。<bookmark mark='c'/>为此微调过的模型，回答的是一个结构化的调用，"
        "而不是一段文字。<bookmark mark='d'/>程序执行调用，把结果交回去。从那以后的每个智能体，包括编程智能体，都建立在这次握手之上。",

    'Every app that hosts a model needs its tools':
        "每个装着模型的应用都需要工具，每个工具也都想服务每个应用。<bookmark mark='a'/>一对一地接起来，三个应用和四个工具，"
        "就要做12次集成。<bookmark mark='b'/>2024年11月，Anthropic发布了模型上下文协议，MCP：一个工具只需包装一次，做成一个列出自己功能"
        "的服务器，任何会说这种协议的应用都能使用它。三加四，而不是三乘四。<bookmark mark='c'/>它传播得很快。到2025年12月，"
        "已经发布了一万多个服务器，这个协议也被交给了Linux基金会下属的一个新基金会，和它一起的还有OpenAI的AGENTS.md和Block的goose。"
        "<bookmark mark='d'/>谷歌的A2A协议，则为智能体之间的对话做了同样的事。",

    # ---------------------------------------------------------------- Memory
    'Chapter four. Memory, and many agents.':
        '第4章。记忆，以及多个智能体。',

    "An agent's working memory is its context window":
        "智能体的工作记忆就是它的上下文窗口，而它会被填满。<bookmark mark='a'/>循环里的每个想法、动作和观测都会增加词元。"
        "一项长任务产生的内容，远远超过任何窗口能装下的。<bookmark mark='b'/>满了以后，总得丢掉点什么。<bookmark mark='c'/>"
        "最简单的办法是总结：智能体写下它做了什么、什么最重要，清空窗口，再从总结出发重新开始。在一次很长的工作里，"
        "编程智能体会这样做很多次。<bookmark mark='d'/>更早的时候，MemGPT像操作系统那样管理记忆，把事实调进调出上下文；"
        "而即便是第15部分那种上百万词元的窗口，也有一个弱点：放在长上下文中间的内容，模型用得不如放在两头的好。",

    'For memory that outlives the window':
        "要让记忆比窗口活得更久，智能体就在窗口之外记笔记。<bookmark mark='a'/>一条记忆是一小段文字，连同它的嵌入一起存放，"
        "也就是第24部分的那些向量。<bookmark mark='b'/>要回想时，智能体把问题也嵌入，再把最近的几条笔记取回上下文。"
        "<bookmark mark='c'/>2023年，朴俊成和同事们让25个这样的角色住进一个模拟的小镇，每个角色按照记忆有多新、多重要、多相关来检索记忆。"
        "<bookmark mark='d'/>Reflexion把失败的教训用文字记下来，下次尝试之前先读一遍。<bookmark mark='e'/>而Minecraft里的Voyager，"
        "把它掌握的每项技能都存成一段可以以后调用的程序，收集到的独特物品，是以前智能体的3.3倍。笔记、教训和技能：三种记忆。",

    'When one context is not enough, use several.':
        "一个上下文不够用，就用几个。<bookmark mark='a'/>一个主智能体负责规划，把任务的各个部分交给子智能体，每个子智能体都有一个全新的、"
        "属于自己的上下文，<bookmark mark='b'/>每个都只交回一份简短的总结，这样主智能体的窗口就能保持清爽。<bookmark mark='c'/>"
        "Anthropic在2025年报告说，在它自己的研究类评测上，这样一个团队比单个智能体强了90%。这是这家公司在自己的测试上的测量。"
        "它用的词元，也大约是一次聊天的15倍；在一个公开的基准上，花掉的词元数，就解释了性能差异的80%。<bookmark mark='d'/>"
        "所以，收益的很大一部分，只是更多的计算，分散开来而已。它对那些能干净拆分的宽泛任务最有帮助，比如研究，"
        "<bookmark mark='e'/>而对紧密耦合的任务帮助较小，比如修改同一个代码库，那里的每个智能体都需要知道所有的事。",

    # ---------------------------------------------------------------- Compound
    'Chapter five. Compounding error.':
        '第5章。误差的累积。',

    'f"Agents work in long chains of steps':
        "智能体干活，靠的是一长串步骤：读一个网页，点一下，写代码，运行，再读报错信息。<bookmark mark='h'/>一个任务从头到尾要走多少步，"
        "就是它的时程；而每一步都必须做对。<bookmark mark='a'/>如果每一步成功的概率是p，那么n步的任务，成功的概率就是p的n次方。"
        "<bookmark mark='b'/>每一步有90%的把握，10步的任务，就已经是三次里有两次失败。每一步有99%的把握，100步的任务，"
        "也只有{100 * v99:.0f}%的时候能完成。小错误会层层累积。",

    'f"Our warehouse agent shows where the reliability comes from.':
        "我们的仓库智能体，展示了可靠性从哪里来。这是它算对总数的比例，横轴是它要查的价格个数。<bookmark mark='a'/>全靠在脑子里算，"
        "每个失误都是无声的，到60步时，它只有{100 * n60['head']:.0f}%的时候是对的。<bookmark mark='b'/>用上工具，大多数错误会自己暴露出来："
        "一个格式不对的调用，会以错误的形式返回，智能体只要再试一次就行。只有无声的失误会累积：60步时是{100 * n60['react']:.0f}%。"
        "<bookmark mark='c'/>再加一步检查，把取回的东西读一遍，大多数无声的失误也能被抓住：{100 * n60['check']:.0f}%，"
        "代价是每一步{calls:.2f}次调用。<bookmark mark='d'/>{fit}循环能看见的错误，就是它能改正的错误。",

    'Each set of points falls on its own curve p to the n':
        "每一组点，都落在各自的p的n次方曲线上，而p正是那些错误率所预言的：",

    'The points fall close to curves p to the n':
        "这些点落在p的n次方曲线附近，但不完全重合，因为重试会消耗步数预算：",

    'f"Turn it around: how long a task can an agent finish half the time?':
        "反过来问：一个智能体有一半把握完成的任务，最长能有多长？<bookmark mark='a'/>令p的n次方等于二分之一，<bookmark mark='b'/>"
        "再取对数。<bookmark mark='c'/>当p接近1时，负的log p几乎正好等于1减p，也就是错误率。<bookmark mark='d'/>所以，"
        "一半把握的时程，大约是0.7除以每一步的错误率：每一步99%的把握，就是{math.log(2) / -math.log(ex):.0f}步。错误减半，"
        "能完成的任务长度就翻一倍。下一章追踪的，正是真实模型的这个量。",

    # ---------------------------------------------------------------- Doubling
    'Chapter six. Horizons that double.':
        '第6章。不断翻倍的时间跨度。',

    'The research group METR turned the length of a task':
        "研究机构METR，把任务的长度变成了衡量智能体的一把尺子。<bookmark mark='a'/>拿来几百个软件和研究任务，给熟练的人计时："
        "有的只要几秒，有的要一整个工作日。<bookmark mark='b'/>让一个智能体做所有这些任务，以人的用时为横轴、取对数刻度，画出它的成功率。"
        "短任务它大多能做成，长任务大多做不成。<bookmark mark='c'/>拟合一条逻辑斯谛曲线，读出它穿过二分之一的位置：智能体有一半把握完成的"
        "任务长度，也就是它的百分之五十时间跨度。第31部分会细讲这是怎么测的；这里我们关注它说明了智能体的什么。",

    'f"Here are METR\'s measurements: every model they tested':
        "这是METR的测量结果：他们测过的每一个模型，按发布日期排开，纵轴是取对数的分钟数。<bookmark mark='a'/>2019年的GPT-2，"
        "能完成{60 * by['GPT-2']:.0f}秒的任务。2023年的GPT-4，大约{by['GPT-4']:.0f}分钟。<bookmark mark='b'/>在对数刻度上，"
        "前沿模型沿着一条直线上升；而对数刻度上的直线，意味着固定的倍增时间。<bookmark mark='c'/>拟合2023年以来的前沿模型，"
        "得到每{d23:.0f}天翻一番，{said}从2019年算起的整个时段，则是{float(m['doubling_all']):.0f}天：步伐在加快。"
        "<bookmark mark='d'/>还在METR可靠测量范围内的最后一个前沿模型，{first['name']}，有一半把握完成大约{first_h:.0f}小时的任务。"
        "按照上一章的推理，每翻一番，就是每一步的错误减半。",

    "which is METR's own fit.":
        "和METR自己的拟合一致。",

    'f"against METR\'s own {metr[\'from_2023\']:.0f}."':
        "而METR自己的拟合是{metr['from_2023']:.0f}天。",

    'f"Half the time is a low bar for work you\'d hand over.':
        "对于要托付出去的工作，一半的把握是很低的门槛。METR也报告了每个模型的成功率曲线穿过百分之八十的位置。"
        "<bookmark mark='a'/>这些时间跨度要短得多。<bookmark mark='b'/>如果智能体在每一分钟的工作里，都以同样小的概率失败，"
        "也就是第5章那种累积，那么两种时间跨度的比值就是固定的：log 2除以log 1.25，等于{ch:.1f}。<bookmark mark='c'/>{verdict}"
        "<bookmark mark='d'/>{tail}",

    'f"METR\'s measurements give a median of {ratio:.1f}: an agent':
        "METR的测量给出的中位数是{ratio:.1f}：智能体的成功率随长度下降得，比每分钟风险恒定时更平缓。长任务并不只是很多个短任务；"
        "有些长任务很容易，有些短任务却很难。",

    'f"METR\'s measurements give a median of only':
        "METR的测量给出的中位数只有{ratio:.1f}：成功率随长度下降得，比每分钟风险恒定时更快。",

    'f"METR\'s measurements give a median of {ratio:.1f}, close':
        "METR的测量给出的中位数是{ratio:.1f}，和它很接近。",

    "f'The eighty-percent horizons are much shorter":
        "百分之八十的时间跨度短得多，但它们翻倍的速度几乎一样：每{d80:.0f}天。",

    "f'The eighty-percent horizons double every":
        "百分之八十的时间跨度，每{d80:.0f}天翻一番。",

    'f"The ruler itself is running out.':
        "这把尺子本身也快用完了。<bookmark mark='a'/>METR说，它现有的任务，没法可靠地测量16小时以上的时间跨度。<bookmark mark='b'/>"
        "它最后一次测量前沿模型，是2026年4月的{last['name']}，结果大约是{last['p50'] / 60:.0f}小时，已经越过了这条线；"
        "2026年9月，这个页面停止了更新。<bookmark mark='c'/>而且，基准上的时间跨度并不等于一份工作：METR自己的对照试验发现，"
        "有经验的开发者用上2025年初的工具，速度反而更慢了，而不是更快。这样的趋势能信到什么程度，是第31部分的问题。"
        "接下来，看看编程智能体具体是怎样被衡量的。",

    # ---------------------------------------------------------------- Coding
    'Chapter seven. Coding agents.':
        '第7章。编程智能体。',

    'How do you test a coding agent?':
        "怎样测试一个编程智能体？2023年，普林斯顿的卡洛斯·希门尼斯、杨约翰和同事们，用开源软件的历史建起了SWE-bench。"
        "<bookmark mark='a'/>每道题都是GitHub上真实报告过的一个问题，<bookmark mark='b'/>放在一个真实的代码库里，停在它被修复之前的那一刻。"
        "<bookmark mark='c'/>智能体必须写出一个补丁。<bookmark mark='d'/>然后运行真实修复所加的那些测试：它们必须从失败变成通过，"
        "同时其他所有测试都要继续通过。<bookmark mark='e'/>一共有2294道题，来自12个Python项目。当时最好的模型，Claude 2，"
        "解出的不到百分之二。",

    'The first big gains came from the interface':
        "最早的大进步，来自接口，而不是模型。<bookmark mark='a'/>2024年，同一个普林斯顿团队给GPT-4配了一套为它设计的命令："
        "找文件，一次看一百行，编辑一段行，运行测试。<bookmark mark='b'/>环境的回答也很紧凑，会拒绝会破坏语法的编辑。"
        "<bookmark mark='c'/>他们称之为智能体与计算机的接口；用同一个模型，它解出了SWE-bench的12.5%，是以前的好几倍。"
        "<bookmark mark='d'/>那年8月，OpenAI请开发者逐题检查了一个500道题的子集，只保留题意清楚的那些：这就是SWE-bench Verified，"
        "两年来的标准尺子。<bookmark mark='e'/>到2025年，这个循环已经搬进了开发者自己的终端。",

    'f"Then the yardstick wore out.':
        "后来，这把尺子也磨损了。前沿模型能解出Verified的大部分题目，2026年2月，OpenAI宣布不再报告它的成绩。"
        "<bookmark mark='a'/>在它的模型一直做不对的138道题里，它的工程师判断有59%的测试会拒绝正确的修复。而且只给题目的编号，"
        "三个前沿模型就能写出真实的修复，连注释都一样：答案已经泄漏进了训练数据。这些是OpenAI的结论。<bookmark mark='b'/>"
        "它推荐的继任者，是Scale AI的SWE-Bench Pro：1865道题，来自41个仍在积极维护的代码库，其中一些不公开，要做的修改也更大。"
        "2025年9月它刚出现时，最好的模型大约能解出四分之一。<bookmark mark='c'/>在Scale今天的排行榜上，排第一的{top[0]}，"
        "解出了公开集的{top[1]:.1f}%，和第二名只差几个百分点。",

    'Real engineering is more than patches.':
        "真正的工程不只是打补丁。<bookmark mark='a'/>Terminal-Bench来自斯坦福大学和Laude研究所，2025年推出：它把智能体丢进一个容器里的终端，"
        "交给它一项工作，比如构建软件、配置服务器或训练一个模型，最后由一段脚本检查结果。<bookmark mark='b'/>2.0版有89个这样的任务，"
        "前沿智能体解出的不到三分之二。<bookmark mark='c'/>如今基准被淘汰的速度，和模型进步一样快：2026年的4.0版，"
        "去掉了每个模型都能解出的任务，并给每个任务最多8小时。<bookmark mark='d'/>2026年9月，Anthropic报告它最新的模型在上面得了66%："
        "这是一家公司对自家模型的测量，还要在公开排行榜上核对。",

    # ---------------------------------------------------------------- Computer
    'Chapter eight. Using a computer.':
        '第8章。使用电脑。',

    'Most software was built for people':
        "大多数软件是为人设计的，有屏幕，有鼠标，而不是为程序设计的。所以，智能体能拥有的最通用的工具，就是一台属于它自己的电脑。"
        "<bookmark mark='a'/>循环还是同一个。观测是一张截图。<bookmark mark='b'/>模型把它当作像素来读，然后回答一个动作：在这些坐标上点击，"
        "输入这段文字，按那个键。<bookmark mark='c'/>然后它再截一张图，看看发生了什么。<bookmark mark='d'/>Anthropic在2024年10月以"
        "“电脑使用”的名义发布了它，OpenAI的Operator在2025年1月跟进。<bookmark mark='e'/>最难的部分，原来是最基础的那件事："
        "把看到的东西，变成恰好该点的那个像素。",

    'To measure this, Tianbao Xie and colleagues built OSWorld':
        "为了衡量这一点，谢天宝和同事们在2024年建起了OSWorld：369个真实桌面应用里的真实任务，从编辑电子表格到配置邮件客户端，"
        "每个任务都由一段脚本在事后检查机器的状态。<bookmark mark='a'/>人能完成其中的72%。<bookmark mark='b'/>发布时最好的模型，12%。"
        "<bookmark mark='c'/>然后各家公司报告了自己的智能体：2024年10月15%，2025年1月38%，到那年9月61%。这些是公司自己的数字，"
        "用的是它们自己的设置，而且基准本身也一路修订过，所以只能把它们看作一个趋势。",

    'In 2026 the same team released OSWorld 2.0':
        "2026年，同一个团队发布了OSWorld 2.0，任务的规模完全不同。<bookmark mark='a'/>它的108个工作流，每个都要熟练的人花上中位数"
        "一个半小时，智能体要做大约300次工具调用，是以前的十倍。在它的排行榜上，最好的智能体能完整完成五分之一。<bookmark mark='b'/>"
        "Anthropic报告它最新的模型，在自己的运行里拿到了82%的部分得分。<bookmark mark='c'/>读屏幕还带来一种新的危险。任何网页都可能"
        "藏着写得像指令的文字，而智能体读它的时候，用的正是读自己任务的同一双眼睛。<bookmark mark='d'/>一个读着不可信的文字、"
        "又握有真实权限的智能体，是一个安全问题，第31部分还会回到这里。",

    # ---------------------------------------------------------------- Imitation
    'Chapter nine. Learning by imitation.':
        '第9章。模仿学习。',

    'The simplest way to teach an agent is to show it.':
        "教一个智能体，最简单的办法是做给它看。<bookmark mark='a'/>1989年，迪恩·波默洛的ALVINN通过一个小摄像头看路，"
        "模仿人类司机，学会了驾驶一辆面包车。<bookmark mark='b'/>这就是行为克隆：记下专家看到了什么、做了什么，"
        "再用普通的监督学习拟合一个策略。<bookmark mark='c'/>这里的平均，是对专家到过的那些状态取的。<bookmark mark='d'/>"
        "直到今天，机器人策略都是这样起步的。<bookmark mark='e'/>但这里有个陷阱。学习者一旦自己开车，到的就是它自己的状态，"
        "而不是专家的；一个小失误，就会把它带到专家从没去过的地方。",

    'f"Here is a small driving task we can solve exactly.':
        "这是一个我们能精确求解的小驾驶任务。<bookmark mark='a'/>一辆车沿着车道往前开，每一步它可以向左打方向、直行或向右打方向，"
        "而一阵风一直把它往右推。<bookmark mark='b'/>每离开车道一步，代价是1。<bookmark mark='c'/>专家确切知道车在哪里，会把方向打回来，"
        "所以它{stays}。这是它的12次驾驶。<bookmark mark='d'/>学习者通过一个摄像头看路，摄像头有时会偏一格。正是这点噪声，"
        "让哪怕完美的模仿，也会偶尔犯错。",

    "f'leaves it only {Je:.1f} steps in":
        "在{int(L['T'])}步里只离开了{Je:.1f}步",

    'f"Behaviour cloning: give the learner the expert\'s drives':
        "行为克隆：把专家的驾驶记录交给学习者，对每一种摄像头读数，它都照搬专家最常用的动作。<bookmark mark='a'/>"
        "在{S}种可能的读数里，它只见过{n_seen}种，都在路中间附近，因为专家只去那些地方。<bookmark mark='b'/>现在让它自己开。"
        "大多数时候它学得很像：在专家自己的状态上，它只有{100 * eps:.1f}%的时候做出不同的选择。<bookmark mark='c'/>"
        "可是一阵风来得不是时候，摄像头读错一次，它就离开了车道，进入它从没见过的读数，<bookmark mark='d'/>在那里它完全不知道该怎么办。"
        "这12次驾驶里，有{len(lost)}次最后停在车道之外。",

    'How bad can this get?':
        "这会糟到什么程度？设ε为学习者的错误率，在专家到过的状态上测量：这正是监督学习会把它压小的那个量。<bookmark mark='a'/>"
        "前t步一次错都没犯的概率，至少是1减去到目前为止各步错误率之和：这是联合界。<bookmark mark='b'/>在第一次犯错之前，"
        "学习者恰好在专家会在的地方。犯错之后，最坏的情况是每一步都付出全部代价。<bookmark mark='c'/>把它在T步的任务上加起来。"
        "<bookmark mark='d'/>每个内层的和至多是T乘ε，所以额外的代价至多是T的平方乘ε。斯特凡·罗斯和德鲁·巴格内尔在2010年证明了这一点，"
        "还给出了真能达到这个界的任务：时程翻倍，额外代价就变成四倍。",

    '"Here is our learner\'s expected cost, computed exactly':
        "这是我们的学习者的期望代价，精确算出，时程从1到400步，8个随机种子。<bookmark mark='a'/>{shape}<bookmark mark='b'/>"
        "这个界，T的平方乘ε，用测得的ε等于{eps:.3f}，远远高于它：它是最坏情况。如果错误只是简单相加，代价会沿着T乘ε走。"
        "<bookmark mark='c'/>{climb}",

    'The reason is on the right':
        "原因在右边：离开车道的概率一步接一步地往上爬，因为离开车道的学习者，很少能回来。",

    'The chance of being off the lane levels off early here.':
        "在这里，离开车道的概率很早就趋于平稳了。",

    "f'It bends upward: the cost grows faster than the horizon":
        "它向上弯：代价比时程增长得更快，在双对数坐标上斜率是{max(s1, s2):.1f}，而线性增长的斜率是1。",

    'It grows about in proportion to the horizon here':
        "在这里，它大致和时程成正比增长，比这个界允许的慢。",

    # ---------------------------------------------------------------- DAgger
    'Chapter ten. DAgger.':
        '第10章。DAgger。',

    'The cure, from Stéphane Ross, Geoff Gordon and Drew Bagnell':
        "解药来自斯特凡·罗斯、杰夫·戈登和德鲁·巴格内尔，2011年：就学习者自己的错误去问专家。<bookmark mark='a'/>让学习者开车。"
        "<bookmark mark='b'/>事后，专家给学习者到过的每个状态都打上标签：换了我，会这样做。<bookmark mark='c'/>把这些标签加进到目前为止"
        "收集的全部数据，<bookmark mark='d'/>重新训练，再开一次。他们把它叫作DAgger，即数据集聚合。每一轮，数据都向学习者真正会到的"
        "那些状态移动，包括路外面的那些。",

    'f"Here is DAgger on our lane, round by round.':
        "这是DAgger在我们的车道上，一轮一轮的样子。<bookmark mark='a'/>第一轮是专家的一次驾驶，所以学习者只认识路中间。"
        "<bookmark mark='b'/>接下来的几轮，它自己开，开出了路，专家就给它在外面看到的读数打上标签：往回打方向。灰色的箭头变成了真正的箭头。"
        "<bookmark mark='c'/>到第{first_good + 1}轮，它在{T}步里的期望代价，已经从{Jh[0]:.0f}降到了{Jh[first_good]:.0f}，"
        "之后几轮都保持在那里。",

    'Why does this fix the T squared?':
        "这为什么能治好T的平方？诀窍是把这些轮次当作一场在线学习的博弈。<bookmark mark='a'/>现在要紧的错误，是在学习者自己的状态上测的，"
        "也就是它自己的策略会去的那些状态。<bookmark mark='b'/>每次都在全部数据上重新训练，是一种无悔算法：平均到各轮，"
        "它做得和事后看来最好的那个策略一样好。<bookmark mark='c'/>于是代价只随时程线性增长，再乘以u，也就是一个错误的动作以后最多会"
        "造成多大代价，前提是任务允许你纠正回来。<bookmark mark='d'/>区别就在于，错误是在哪里被计数的。",

    'f"Now the fair comparison':
        "现在做公平的比较：两种方法的专家标签一样多，各用8个随机种子。<bookmark mark='a'/>{v1}<bookmark mark='b'/>"
        "它的代价更接近直线增长，前几步在双对数坐标上的斜率是{sd:.2f}，而行为克隆是{sb:.2f}。不同种子之间的差别很大，"
        "DAgger相差{spread:.0f}步，因为学习者碰巧看到了哪些读数，影响很大。<bookmark mark='c'/>{v2}<bookmark mark='d'/>{v3}",

    'f"With the same {N} expert labels, DAgger\'s cost':
        "用同样的{N}个专家标签，DAgger在{T}步里平均有{fd:.0f}步离开车道，行为克隆则是{fb:.0f}步。",

    "f'With the same {N} expert labels, DAgger averages":
        "用同样的{N}个专家标签，DAgger在{T}步里平均有{fd:.0f}步离开车道，行为克隆是{fb:.0f}步：在这个预算下，胜负并不分明。",

    'More demonstrations barely help behaviour cloning':
        "更多的示范，对行为克隆几乎没有帮助：专家的驾驶从不离开车道，所以从来不会示范怎样回来。",

    'More demonstrations help behaviour cloning too, slowly.':
        "更多的示范对行为克隆也有帮助，只是很慢。",

    "f'DAgger keeps improving with labels":
        "DAgger随着标签增多不断改进，到{int(budgets[-1])}个标签时降到{Bd.mean(1)[-1]:.0f}步。",

    'DAgger levels off early too.':
        "DAgger也很早就趋于平稳。",

    'DAgger has a price':
        "DAgger是有代价的：需要一个随叫随到的专家，给学习者的状态打标签。<bookmark mark='a'/>一个人很难事后说清楚，"
        "在别人开车的每一刻，自己会怎样打方向。<bookmark mark='b'/>所以实用的版本只在学习者出错时让人接管，再用这些纠正来训练。"
        "<bookmark mark='c'/>当专家是一个程序时，这就很容易，而这个思想无处不在：第27部分的在线策略蒸馏，由老师给学生自己的回答打分，"
        "就是语言模型版的DAgger。<bookmark mark='d'/>教训是：从你实际到达的地方学习。",

    # ---------------------------------------------------------------- World
    'Chapter eleven. World models.':
        '第11章。世界模型。',

    'An agent that can predict the results of its actions':
        "一个能预测自己行动后果的智能体，可以在动手之前先在脑子里试一试。<bookmark mark='a'/>这个想法由来已久。1990年前后，"
        "理查德·萨顿的Dyna学到一个世界模型，在真实的步骤之间，在模型里练习；于尔根·施密德胡伯也造出了为自己的世界建模的循环网络。"
        "<bookmark mark='b'/>2018年，大卫·哈和施密德胡伯把它做得活灵活现。一个变分自编码器压缩游戏的每一帧，<bookmark mark='c'/>"
        "一个循环网络学着预测下一帧压缩后的样子，<bookmark mark='d'/>一个很小的控制器根据这两者行动。它第一个在一款赛车游戏里，"
        "从像素出发拿到900分以上；而在VizDoom里，它完全是在自己的梦里训练出来的。<bookmark mark='e'/>第26部分的MuZero走了另一条路："
        "只为规划需要的东西建模，从不管像素。",

    'To plan, an agent needs to predict what its actions will do.':
        "要做计划，智能体就得预测自己的行动会带来什么。世界模型，就是从经验中学会这一点。<bookmark mark='a'/>我们的世界模型，"
        "看的是一个在盒子里弹来弹去的球。它把每一帧压缩成8个数，学会这些数从一帧到下一帧怎样变化，还能把这些数重新变回一幅画面。",

    'f"Now let it imagine.':
        "现在，让它来想象。给它两帧真实的画面，然后让它靠自己的预测往下走，一步接一步，<bookmark mark='a'/>而真实的球也在继续运动。"
        "有一阵子，想象和现实同步前进：往前看一步，只差{pe[0]:.1f}个像素。<bookmark mark='b'/>然后，小误差开始累积，"
        "就像上一章的长任务一样：想象20步之后，差了{pe[19]:.1f}个像素。<bookmark mark='c'/>像Dreamer这样的智能体，"
        "就是在这种想象出来的世界里练习的；而Genie，从视频里生成一个个完整的、可以玩的世界。",

    'f"How does a world model learn to dream?':
        "世界模型是怎么学会做梦的？这是它在训练途中的几个检查点，每次都给它同样的两帧开头，让它想象接下来的12帧，"
        "每一帧都建立在它自己上一个猜测之上。<bookmark mark='a'/>还没训练的时候，它最亮的像素是{peak[0]:.2f}：一片雾，一点也不像球。"
        "<bookmark mark='b'/>{early}<bookmark mark='c'/>{mid}<bookmark mark='d'/>最终的模型，在{n}帧里有{held[-1]}帧都带着球，"
        "不过小误差还是会累积：想象了12帧之后，它画的球离真实的球差{miss:.1f}个像素。",

    "f'After {checks[1]} steps its brightest pixel is only":
        "训练{checks[1]}步之后，它最亮的像素只有{peak[1]:.2f}：它学会了最保险的猜法，一张几乎空白的画面，也就是所有画面的平均。",

    "f'After {checks[1]} steps a faint ball appears":
        "训练{checks[1]}步之后，出现了一个淡淡的球，在{n}帧里有{held[1]}帧，它都让球待在真实的球附近。",

    'f"By step {checks[2]} it keeps the ball within two pixels':
        "到第{checks[2]}步，在{n}帧里有{held[2]}帧，它画的球离真实的球不到两个像素，然后就跟丢了，因为每个猜测都建立在上一个猜测的模糊之上。",

    "f'By step {checks[2]} it already carries the ball":
        "到第{checks[2]}步，它已经能把球一路带完全部{n}帧。",

    # ---------------------------------------------------------------- Dreamer
    'Chapter twelve. Dreamer: learning inside a dream.':
        '第12章。Dreamer：在梦里学习。',

    'Our bouncing-ball model only predicted.':
        "我们那个弹球模型只会预测。达尼亚尔·哈夫纳的Dreamer智能体，从2019年起，先学一个世界模型，然后完全在模型里面学习行动。"
        "它的核心是一个循环状态空间模型。<bookmark mark='a'/>一个循环网络带着一份确定性的记忆h，一步一步往下传，每个动作都会更新它。"
        "<bookmark mark='b'/>它旁边是一个随机状态z，这里是8个类别变量。<bookmark mark='c'/>只根据记忆，先验在不看画面的情况下猜z。"
        "<bookmark mark='d'/>有画面的时候，后验看一眼画面，修正这个猜测。<bookmark mark='e'/>模型从h和z重新画出画面，并预测奖励。"
        "<bookmark mark='f'/>2023年的DreamerV3，用同一套固定的设置跑了150多项任务，还第一个在不用人类数据的情况下，在Minecraft里挖到了钻石。",

    'It learns from three terms.':
        "它从三项损失里学习。<bookmark mark='a'/>从状态重新画出每幅画面。<bookmark mark='b'/>预测每个奖励。<bookmark mark='c'/>"
        "再让先验和后验一致，这样模型不看画面也能预测：正是这一点让它能做梦。这种一致用KL散度来衡量，DreamerV2把它拆成了两半。"
        "一半冻结后验，把先验往看到的东西上拉。<bookmark mark='d'/>另一半冻结先验，把后验轻轻推向先验能预测的状态。<bookmark mark='e'/>"
        "给前一半更大的权重，先验就动得更多：这就是KL平衡。而KL低于1奈特的部分不计代价，所以后验永远不会被压得什么都不说。",

    'f"Does balancing matter?':
        "平衡真的重要吗？我们只训练了这个小游戏的世界模型，两种方式各3个随机种子，KL的总权重相同，<bookmark mark='a'/>"
        "让每个模型从6帧真实画面出发，往后梦30步，数一数它画错了多少像素。<bookmark mark='b'/>{v}",

    "f'With balancing, its dreams average {mb:.1f} wrong pixels a frame over thirty steps; without, {mp_:.1f}. The bands":
        "用了平衡，它的梦在30步里平均每帧错{mb:.1f}个像素；不用，则是{mp_:.1f}个。两条带子甚至没有重叠。",

    "f'With balancing, its dreams average {mb:.1f} wrong pixels a frame over thirty steps; without, {mp_:.1f}.'":
        "用了平衡，它的梦在30步里平均每帧错{mb:.1f}个像素；不用，则是{mp_:.1f}个。",

    "f'Here, surprisingly, the plain KL dreams better":
        "出人意料的是，这里普通的KL梦得更好：每帧错{mp_:.1f}个像素，而平衡的是{mb:.1f}个。在这么小的世界里，平衡并不划算。",

    'f"On a world this small the difference is slight':
        "在这么小的世界里，差别很小：用了平衡每帧错{mb:.1f}个像素，不用是{mp_:.1f}个。在更难的世界里，比如雅达利游戏，平衡更重要。",

    'f"A second trick from DreamerV3':
        "DreamerV3的第二个诀窍，让同一套设置在哪里都能用。一个游戏的奖励在1左右，另一个在1000左右，而平方误差由最大的那个主导。"
        "<bookmark mark='a'/>所以V3预测的是奖励的对称对数，事后再还原：在0附近几乎就是恒等函数，离得远时是对数。<bookmark mark='b'/>"
        "我们训练了一个小网络，去预测四个游戏的奖励，它们的尺度相差一千倍。<bookmark mark='c'/>{v}我们的Dreamer就是这样预测奖励的，"
        "在symlog空间里，表示成一组区间上的分布。",

    "f'Trained on raw rewards, the network spends itself":
        "用原始奖励训练，网络把力气都花在最大的那个游戏上，最小的那个错了{100 * r1:.0f}%。用了symlog，每个游戏都学到了："
        "最小的错{100 * s1:.0f}%，最大的错{100 * sL:.0f}%。",

    "f'Here the raw rewards get the smallest game":
        "这里，用原始奖励时最小的游戏错了{100 * r1:.0f}%，用symlog错了{100 * s1:.0f}%：差距比预想的小。",

    'f"Then the agent learns to act without touching the real game.':
        "然后，智能体在不碰真实游戏的情况下学习行动。<bookmark mark='a'/>从模型见过的状态出发，它往后梦{int(P['horizon'])}步，"
        "用当前的策略选动作，奖励由模型预测。<bookmark mark='b'/>每个梦的回报，把梦到的奖励和评论家对之后的估计混在一起，"
        "也就是λ回报。策略按第26部分的REINFORCE来学，用评论家做基线，按回报的跨度缩放，再加一点熵。<bookmark mark='c'/>"
        "评论家学习梦里的回报。真实的游戏，只用来给模型收集更多经验。",

    'f"Here is our Dreamer-lite learning the game of catch.':
        "这是我们的迷你Dreamer在学接球游戏。在每个检查点，它看同样的6帧真实画面，然后在同样的动作下继续往后梦。"
        "<bookmark mark='a'/>还没训练时，它的梦和这个游戏毫无关系。<bookmark mark='b'/>随着训练，梦越来越接近现实，{trend}"
        "<bookmark mark='c'/>梦得越久，误差还是会慢慢渗进来，就像第11章那样；而新出现的球位置是随机的，永远不可能被准确梦到。",

    "f'from {wrong[0]:.1f} wrong pixels a frame untrained":
        "从未训练时每帧错{wrong[0]:.1f}个像素，降到{its[-1] * steps_per:,}次更新后的{wrong[-1]:.1f}个，而每幅画面大约只有{lit:.0f}个亮像素。",

    "f'but its dreams improve little":
        "但它的梦改进得很少：一开始每帧错{wrong[0]:.1f}个像素，最后是{wrong[-1]:.1f}个。",

    'f"And the policy, trained only in those dreams':
        "而这个只在梦里训练过的策略，被拿到真实的游戏里测试。<bookmark mark='a'/>{v}<bookmark mark='b'/>右边是它最后玩的一局真实游戏：{game}",

    "f'the paddle heads for where each ball will land":
        "挡板朝着每个球将要落下的地方移动，{len(landed)}个球接住了{caught}个。",

    "f'it catches {caught} of the {len(landed)} balls.":
        "{len(landed)}个球它接住了{caught}个。",

    "f'After about {int(steps[-1]):,} steps of real play, the {len(fin)} seeds":
        "在大约{int(steps[-1]):,}步真实游戏之后，{len(fin)}个种子接住了{100 * lo:.0f}%到{100 * hi:.0f}%的球，而随机移动的挡板是"
        "{100 * rnd:.0f}%：这个策略完全是在梦里学会的。",

    "f'After about {int(steps[-1]):,} steps of real play, the seeds catch {100 * lo:.0f} to {100 * hi:.0f} percent of the balls":
        "在大约{int(steps[-1]):,}步真实游戏之后，这些种子接住了{100 * lo:.0f}%到{100 * hi:.0f}%的球，而随机移动的挡板是"
        "{100 * rnd:.0f}%：确实学到了东西，不过离完美还远。",

    'f"After about {int(steps[-1]):,} steps of real play, the seeds catch {100 * lo:.0f} to {100 * hi:.0f} percent, hardly':
        "在大约{int(steps[-1]):,}步真实游戏之后，这些种子接住了{100 * lo:.0f}%到{100 * hi:.0f}%，比随机挡板的{100 * rnd:.0f}%"
        "好不了多少：在这个预算下，梦还不够好，学不出东西。",

    # ---------------------------------------------------------------- Genie
    'Chapter thirteen. Worlds you can walk through.':
        '第13章。可以走进去的世界。',

    'Our world models learned from frames paired with the actions':
        "我们的世界模型，是从配好了动作的画面里学的。网上到处都是视频，可几乎没有哪段视频记下了按的是哪个键。<bookmark mark='a'/>"
        "谷歌DeepMind在2024年推出的Genie，连动作也一起学了。一个潜在动作模型看相邻的两帧画面，必须只用8个代码中的一个来解释它们的变化，"
        "<bookmark mark='b'/>就像在猜按下了哪个键。<bookmark mark='c'/>一个动力学模型，学着根据过去的画面和一个代码画出下一帧。"
        "<bookmark mark='d'/>玩的时候，由人来选代码，视频模型就变成了一个可以操控的游戏，而它是从完全没有标签的游戏视频里学出来的。",

    'Then the worlds grew.':
        "然后，世界变大了。<bookmark mark='a'/>2024年12月的Genie 2，从一张图片生成三维世界。<bookmark mark='b'/>2025年8月的Genie 3，"
        "以720p、每秒24帧的画面实时绘制世界，并让它在几分钟里保持一致：从一面墙前走开，再走回来，你在墙上画的东西还在。"
        "文字可以边走边改变世界，DeepMind还用它训练了自己的SIMA智能体。<bookmark mark='c'/>2026年1月，一个原型向部分订阅用户开放。"
        "<bookmark mark='d'/>而在2026年10月27日，DeepMind发布了Genie 4，声音和画面一起生成，并被定位为训练机器人的场所；"
        "按DeepMind自己的说法，在长时间的会话里，物体仍然会漂移。",

    "Danijar Hafner's Dreamer line":
        "达尼亚尔·哈夫纳的Dreamer系列，也就是上一章的主题，也达到了同样的规模。<bookmark mark='a'/>2025年的Dreamer 4，"
        "主要从Minecraft的视频里学到一个世界模型，其中只有一小部分标注了动作，<bookmark mark='b'/>然后完全在模型里训练一个智能体，"
        "<bookmark mark='c'/>而这个智能体挖到了钻石，这项任务需要两万多个鼠标和键盘动作，它在训练中却从没玩过真正的游戏。",

    'All of these predict pixels':
        "这些模型预测的都是像素：每一片树叶，每一道涟漪，其中大部分是智能体用不着的。<bookmark mark='a'/>第24部分的联合嵌入预测架构，"
        "预测的则是嵌入，只预测编码器认为值得预测的东西。<bookmark mark='b'/>Meta的V-JEPA 2把它变成了机器人的世界模型。在一百万小时的视频"
        "上预训练之后，62小时的机器人视频教会了它：机械臂的动作会怎样改变它看到的东西。<bookmark mark='c'/>要行动时，它在嵌入空间里"
        "想象许多动作序列，<bookmark mark='d'/>执行预测出的嵌入最接近目标图片的那一个。靠这个办法，它在从没见过的实验室里拿起并放下了物体。"
        "这是用学到的模型做规划，和MuZero一样，只不过这个模型是从视频里学来的。",

    # ---------------------------------------------------------------- SimToReal
    'Chapter fourteen. From simulation to reality.':
        '第14章。从仿真到现实。',

    'Robots learn slowly in the real world':
        "机器人在真实世界里学得很慢：一台机器人，一次一次地尝试，会磨损，会摔倒。所以大多数机器人学习都从仿真开始。"
        "<bookmark mark='a'/>仿真器可以同时运行几千台机器人，比真实时间还快，没有东西会坏，真实状态也永远知道。<bookmark mark='b'/>"
        "2021年和2022年，英伟达的Isaac Gym在一块显卡上并行运行了几千台腿足机器人，几分钟就教会了它们走路。<bookmark mark='c'/>"
        "问题在于现实差距。仿真器的物理是人写的，在很多小地方都不对：摩擦，质量，电机的力量，从感知到行动的延迟，每个传感器的噪声。"
        "一个利用了仿真器怪癖的策略，到了真实的机器上就会失败。",

    'The fix is counterintuitive':
        "解决办法有违直觉：故意把仿真器弄得更糟。<bookmark mark='a'/>不要只在一个仿真器里训练。要在很多个里训练，每个都有自己的设置，"
        "每个回合重新抽取：不同的质量，不同的摩擦，更慢的电机，一点延迟。<bookmark mark='b'/>一个在所有这些仿真器里都管用的策略，"
        "就没法依赖任何一个仿真器的怪癖；如果真实世界看起来只是又一次抽样，它在那里也能管用。<bookmark mark='c'/>2017年，"
        "乔希·托宾和同事们对图像这样做，随机化纹理和光照；2018年，彭学斌和同事们对物理这样做；2019年，OpenAI的机械手解开了魔方，"
        "用的随机化会随着机械手的进步自己扩大范围。",

    'f"Let\'s try it on Part 26\'s cart-pole.':
        "我们在第26部分的倒立摆上试一试。<bookmark mark='a'/>我们的“真实”倒立摆是另一台机器：杆更长、更重，电机更弱，"
        "动作晚一步，传感器有噪声，这些都在我们随机化的范围之内。<bookmark mark='b'/>我们用交叉熵方法训练简单的线性策略，"
        "每种方法8个随机种子，训练回合数相同，每一轮都在真实的机器上测试。<bookmark mark='c'/>{a}<bookmark mark='d'/>{b}",

    "f'In the simulator they were trained in, both reach":
        "在它们各自受训的仿真器里，两者分别达到500步中的{nn_.mean():.0f}步和{rn.mean():.0f}步。",

    "In Part 26's simulator, both kinds learn to balance":
        "在第26部分的仿真器里，两种策略都学会了平衡满500步。",

    "f'On the real one, the policies trained in a single simulator":
        "到了真实的倒立摆上，只在一个仿真器里训练的策略，平均坚持{nr.mean():.0f}步；在随机化的仿真器里训练的，坚持{rr.mean():.0f}步。",

    "f'On the real one, the single-simulator policies last":
        "到了真实的倒立摆上，单一仿真器的策略坚持{nr.mean():.0f}步，随机化的坚持{rr.mean():.0f}步：在这里，随机化帮助不大。",

    'f"Here is the whole picture':
        "这是全貌：两种策略在不同的杆长和电机力量下能平衡多久，每一处都带着真实机器人的延迟和噪声。<bookmark mark='a'/>"
        "只在一个仿真器里训练的策略，只在这张图的{100 * frac(mN):.0f}%里平衡得好。<bookmark mark='b'/>在随机化仿真器里训练的，"
        "是{100 * frac(mR):.0f}%，真实的机器人也包括在内。<bookmark mark='c'/>代价是，策略对任何一台机器都没那么精调；"
        "好处是，它不需要知道自己在哪台机器上。",

    'f"Domain randomization is now routine.':
        "域随机化如今已是常规做法。<bookmark mark='a'/>腿足机器人和人形机器人的走和跑，大多就是这样训练的：在随机化的仿真里训练，"
        "再原封不动地搬到真实的机器上。<bookmark mark='b'/>{ep}<bookmark mark='c'/>最新的一步，和前面几章连成了一个圈："
        "2026年10月，谷歌报告说，只用一张照片就为一张真实的桌子建起了仿真的孪生体，而DeepMind把Genie 4定位为机器人的训练场。"
        "仿真器不再由人手写，而是学出来的。",

    "f'In this episode on the real cart-pole, the single-simulator policy drops the pole after {fell_n} steps, while":
        "在真实倒立摆上的这一回合里，单一仿真器的策略在{fell_n}步后让杆倒下了，而随机化的策略到{fell_r}步还在平衡。",

    "f'In this episode on the real cart-pole, the single-simulator policy drops the pole after {fell_n} steps, and":
        "在真实倒立摆上的这一回合里，单一仿真器的策略在{fell_n}步后让杆倒下了，随机化的策略则在{fell_r}步后倒下。",

    # ---------------------------------------------------------------- VLA
    'Chapter fifteen. Vision-language-action models.':
        '第15章。视觉–语言–动作模型。',

    'Here is what is inside a vision-language-action model.':
        "这是视觉–语言–动作模型的内部。它的起点，是一个已经能读懂图像和文字的模型，在网络数据上训练出来的。<bookmark mark='a'/>"
        "给它摄像头拍到的画面和一条指令，再给它加上一种输出动作的办法。<bookmark mark='r'/>2023年的RT-2，把动作写成词元，就像写词一样。"
        "<bookmark mark='b'/>2024年的π0，加上了一个动作专家：这是挂在视觉–语言模型旁边的一个额外的小网络，它唯一的任务，"
        "就是输出平滑的机械臂动作。它可不是第16部分混合专家模型里的那种专家。它用流匹配来生成这些动作；这正是第21部分的那套机制，"
        "只不过现在画出来的不是图像，而是运动轨迹。",

    "And it doesn't act one tiny step at a time.":
        "而且，它并不是一小步一小步地行动。它一次规划一段动作，大约1秒，然后再看一眼世界，规划下一段：<bookmark mark='a'/>"
        "前面几章的信念和世界模型，都合进了同一个网络，它能看、能想、能动。",

    "Here is pi zero's action expert, exactly.":
        "这是π0动作专家的确切形式。<bookmark mark='a'/>一个动作块，是接下来的50个动作，也就是1秒钟的运动。训练时，"
        "从纯噪声到真实的动作块画一条直线，<bookmark mark='b'/>让网络在看到机器人眼前画面的条件下，学习沿着这条直线的速度："
        "这就是第21部分的流匹配。<bookmark mark='c'/>行动时，它从噪声出发，沿着学到的速度走10小步，噪声就变成了一段动作。",

    "In chapter one we left robot learning at Google's RT-1":
        "在第1章里，我们讲到谷歌的RT-1就停下了，那是一个在13万次示范上训练的Transformer。<bookmark mark='a'/>下一步，是借一个头脑来用。"
        "2023年的RT-2，拿来一个在网络上训练好的视觉–语言模型，把它微调成像写字一样写出机器人的动作。在从没见过的物体和场景上，"
        "它有62%的时候成功，而RT-1只有32%：来自网络的知识，变成了动作。<bookmark mark='b'/>接着，21个实验室汇集了来自22种机器人的"
        "一百多万条轨迹，这就是Open X-Embodiment数据集。<bookmark mark='c'/>在它上面训练的OpenVLA，权重开放，有70亿参数，"
        "在29项任务上，比550亿参数的RT-2-X高出16.5个百分点。",

    '"Why go to the trouble of a generative model for actions?':
        "为什么要费劲给动作用一个生成模型？因为人做示范的方式不止一种。<bookmark mark='a'/>在这里，示范从障碍物的上方或下方绕过，"
        "各占一半。<bookmark mark='b'/>{v}真实的示范里，到处都是这样的选择：用哪只手，怎么抓，从哪边绕。",

    'f"Trained to minimize squared error, the policy learns the average':
        "以最小化平方误差为目标训练，策略学到的是两条路的平均，而平均正好穿过障碍物：它有{100 * hr.mean():.0f}%的时候撞上障碍。"
        "<bookmark mark='c'/>流匹配策略则会采样其中一条路，{100 * above:.0f}%的时候从上方绕，{100 * below:.0f}%的时候从下方绕，"
        "撞上障碍的比例是{100 * hf.mean():.0f}%。",

    'f"Here the regression policy hits the obstacle':
        "在这里，回归策略有{100 * hr.mean():.0f}%的时候撞上障碍，流匹配策略是{100 * hf.mean():.0f}%：<bookmark mark='c'/>"
        "差别比理论所说的小。",

    # ---------------------------------------------------------------- Fast
    'Chapter sixteen. Action tokens, and robot foundation models.':
        '第16章。动作词元，以及机器人基础模型。',

    'f"RT-2 and OpenVLA wrote actions as tokens the simplest way.':
        "RT-2和OpenVLA用最简单的办法把动作写成词元。<bookmark mark='a'/>取每个关节在每个时间步的位置，把它取整到256个区间中的一个。"
        "<bookmark mark='b'/>对一个7关节、每秒50步的机械臂来说，一秒钟的动作就是{n_tok}个词元。<bookmark mark='c'/>而它们几乎都一样："
        "在我们平滑的测试动作上，{100 * rep:.0f}%的词元和前一个相同，{100 * near:.0f}%和前一个相差不超过一个区间。<bookmark mark='d'/>"
        "一个被训练去预测下一个词元的模型，学到的主要是照抄，而它需要的信息，被稀稀拉拉地摊在几百个词元上。",

    'f"In January 2025 Karl Pertsch and colleagues':
        "2025年1月，Physical Intelligence的卡尔·佩尔奇和同事们先做压缩。<bookmark mark='a'/>任何平滑的动作，都是一些余弦波的叠加，"
        "慢的波排在前面；离散余弦变换，也就是JPEG里用的那一种，列出每个波各需要多少。<bookmark mark='b'/>平滑的动作，就住在最慢的那几个波里："
        "在我们的动作上，前三个波承载了{100 * k3:.1f}%的能量。<bookmark mark='c'/>FAST把系数放大、取整成整数，于是在这一块动作上，"
        "{H}个数里只有{nz}个不是零；再让第23部分的字节对编码，把常见的模式合并成词元。",

    'f"How much does it save?':
        "它能省多少？这是FAST在留出的动作上的表现，对一系列缩放系数γ：横轴是每秒的词元数，纵轴是用它们重建出的动作的误差。"
        "<bookmark mark='a'/>γ越大，保留的细节越多，花的词元也越多。<bookmark mark='b'/>逐步分箱的做法远在右边：{bt:.0f}个词元。"
        "<bookmark mark='c'/>在差不多的误差下，FAST只需要{toks[k]:.0f}个，少了{ratio:.0f}倍，而且每一个都带着真正的信息。"
        "<bookmark mark='d'/>Physical Intelligence报告说，一个写FAST词元的策略，在许多任务上和他们用流匹配的π0一样好，训练却快了大约5倍。",

    "Physical Intelligence's pi zero point five":
        "Physical Intelligence在2025年4月推出的π0.5，问的是：要在一个机器人从没见过的家里干活，需要什么？<bookmark mark='a'/>"
        "模型先用文字写下一个子任务，比如捡起枕头，<bookmark mark='b'/>再用流匹配专家写出相应的动作。<bookmark mark='c'/>"
        "它同时在所有东西上训练：网络数据，许多种机器人，许多不同的家。在这家公司自己的消融实验里，在没见过的家中，完整的模型有94%的时候成功；"
        "去掉网络数据，74%；去掉其他机器人的数据，49%；去掉家庭的多样性，31%。<bookmark mark='d'/>对机器人和对语言一样，"
        "数据的广度才是泛化的来源。",

    'Since then the field has moved fast':
        "从那以后，这个领域进展飞快，主要是通过各家公司的报告。<bookmark mark='a'/>2025年3月，谷歌DeepMind在Gemini模型上建起了"
        "Gemini Robotics，英伟达发布了一个面向人形机器人的开放模型。<bookmark mark='b'/>同年11月，Physical Intelligence加入了从经验中学习："
        "一个价值函数给每个时刻的进展打分，策略被告知要像那些好的时刻一样行动。它从早上五点半到晚上十一点半一直在做浓缩咖啡。"
        "<bookmark mark='c'/>2026年，出现了能做十分钟以上任务的记忆，<bookmark mark='d'/>还有π0.7，可以用想要的速度和质量来提示它，"
        "或者给它一张下一个子目标的图片。<bookmark mark='e'/>今年10月，谷歌发布了一个能做规划、能搭建仿真的物理推理模型，"
        "<bookmark mark='f'/>Physical Intelligence也把它的模型开放给了别的机器人厂商。这些都是公司自己的结果；面向机器人的独立基准，还很年轻。",

    # ---------------------------------------------------------------- Outro
    '"Let\'s take stock.':
        "我们来盘点一下。一个看不全的智能体，依据信念行动，信念由贝叶斯法则不断预测和修正。语言模型智能体运行着一个由想法、动作和观测组成的"
        "循环，周围是工具和记忆。在长任务里，小错误会层层累积，所以每一步的可靠性，决定了它能走多远；按METR的测量，这个距离每隔几个月"
        "就翻一番。照搬专家，失败的程度随时程的平方增长；DAgger通过在学习者真正会去的地方学习来修复它。{dream}"
        "而机器人在随机化的仿真器里、从示范中学习，用的是生成式的动作专家和压缩过的动作词元。",

    'A world model lets an agent practise in its imagination, as our Dreamer did.':
        "世界模型让智能体在想象中练习，我们的Dreamer就是这样做的。",

    'A world model lets an agent practise in its imagination, which':
        "世界模型让智能体在想象中练习，而我们的小Dreamer才刚刚开始做到这一点。",

    'All of this comes back.':
        "这一切都会再回来。智能体写下的推理，是不是它真正做决定的方式；网络内部是否带着它所在世界的模型：这些是第30部分的问题。"
        "而怎样评估智能体，怎样防止它们钻奖励的空子，怎样控制它们能碰什么，是最后一部分的主题。",

    'Here are seven problems to try':
        "这里有七道题可以试试，从信念更新，到FAST取整带来的误差。请在这里暂停，动手做一做；完整的解答在这一部分的笔记里。",

    'Next time: inside the model.':
        "下一次：模型的内部。一个网络怎样存下比它的维数还多的概念，<bookmark mark='a'/>稀疏自编码器怎样把它们分开，"
        "以及怎样追踪一个想法穿过它的各层。",

    'The best place to go deeper on the first half of this part':
        "想深入这一部分的前半，最好的去处是思伦、比尔加德和福克斯的《概率机器人》；想深入学习如何行动，是萨顿和巴托。"
        "感谢观看，第30部分见。",
}

PHRASES = {
    'never leaves the lane': '从不离开车道',
}
