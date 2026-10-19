"""Chinese narration for ai26: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第26部分：强化学习，从贝尔曼到AlphaZero'

CHAPTERS = {
    'Hook': '没人会下的那一步',
    'Problem': '1. 从后果中学习',
    'Bandits': '2. 探索还是利用',
    'Bellman': '3. 贝尔曼方程',
    'Iteration': '4. 价值迭代为什么管用',
    'TD': '5. 时序差分',
    'QLearning': '6. Q学习',
    'DQN': '7. 深度Q网络',
    'PolicyGradient': '8. 策略梯度',
    'PPO': '9. 信赖域与PPO',
    'Search': '10. 先搜索，再学习',
    'MCTS': '11. 蒙特卡洛树搜索',
    'AlphaGo': '12. AlphaGo',
    'Zero': '13. 从零学起',
    'MuZero': '14. 用学来的模型做规划',
    'Beyond': '15. 超越完全信息',
    'Outro': '回顾、习题，以及这些想法会在哪里再现',
}

ZH = {
    "Seoul, March 2016. A computer program, AlphaGo, is playing Lee Sedol, one of the best Go players in the world. <bookmark mark='a'/> On its thirty-seventh move it plays here, a move so unusual that the commentators assume it's a mistake. <bookmark mark='b'/> AlphaGo's own model of human play put the chance that a person would play it at one in ten thousand. It wins the game, and the match. <bookmark mark='c'/> A year and a half later, its successor learns Go with no human games at all, from random play, in three days, and beats it a hundred games to nothing.":
        "2016年3月，首尔。一个计算机程序，AlphaGo，正在和李世石对弈，他是世界上最强的围棋棋手之一。<bookmark mark='a'/>第37手，它下在了这里。这步棋太不寻常，解说员都以为它下错了。<bookmark mark='b'/>按AlphaGo自己对人类下法的估计，一个人会下这步棋的概率，只有万分之一。它赢下了这盘棋，也赢下了整场比赛。<bookmark mark='c'/>一年半之后，它的继任者完全不看人类棋谱，从随机乱下开始，用3天时间学会了围棋，然后以100比0击败了它。",

    "That is the question of this part: how do you learn to act, when nobody tells you the right action, only how things turned out? <bookmark mark='a'/> We'll follow the answer from a psychologist's puzzle boxes, through Bellman's equation and the algorithms that learned backgammon, Atari and the cart-pole, to AlphaGo and AlphaZero, deriving each step. <bookmark mark='b'/> And we'll train an AlphaZero of our own, on the computer making this video, and grade every move it makes against a perfect player.":
        "这就是本部分要回答的问题：没有人告诉你正确的动作，只告诉你结果怎么样，你要怎样学会行动？<bookmark mark='a'/>我们会沿着答案一路走下去：从一位心理学家的迷箱，到贝尔曼方程，再到学会了西洋双陆棋、雅达利游戏和倒立摆的那些算法，最后到AlphaGo和AlphaZero，每一步都推导出来。<bookmark mark='b'/>我们还要在制作这个视频的电脑上，训练一个我们自己的AlphaZero，并且拿一个完美棋手来检验它下的每一步。",

    "This is Part 26 of AI, Built, and the start of its fifth act: agency. <bookmark mark='a'/> In this part: the reinforcement learning problem and the dilemma of exploration; Bellman's equation and why its algorithms converge; learning from experience, from temporal differences to deep Q-networks; policy gradients and PPO, the algorithm behind ChatGPT's training; search, from minimax to AlphaZero and MuZero; and games with hidden information, like poker.":
        "这是《人工智能，从零搭建》的第26部分，也是第五幕“智能体”的开始。<bookmark mark='a'/>本部分的内容：强化学习问题，以及探索的两难；贝尔曼方程，以及它的算法为什么一定收敛；从经验中学习，从时序差分到深度Q网络；策略梯度和PPO，也就是训练ChatGPT所用的算法；搜索，从极小极大到AlphaZero和MuZero；最后是像扑克这样隐藏了信息的博弈。",

    'Chapter one. Learning from consequences.':
        '第1章。从后果中学习。',

    "In the 1890s the psychologist Edward Thorndike put cats in puzzle boxes. To get out, and get to the fish outside, a cat had to pull a loop of string. <bookmark mark='a'/> The first time it took minutes of scrabbling. Each time after, a little less, until the cat went straight for the loop. <bookmark mark='b'/> In 1911 he called it the law of effect: what is followed by satisfaction gets stamped in. <bookmark mark='c'/> Reinforcement learning is that law, made into mathematics. Nobody shows the learner the right action. There is only a number, a reward, that arrives after it acts, sometimes long after.":
        "19世纪90年代，心理学家爱德华·桑代克把猫关进迷箱。猫要出来，吃到箱子外面的鱼，就得拉动一个绳圈。<bookmark mark='a'/>第一次，它要乱抓好几分钟。之后每一次，都快一点，直到猫一进去就直奔那个绳圈。<bookmark mark='b'/>1911年，他把这叫作效果律：凡是带来满足的行为，就会被“刻印”下来。<bookmark mark='c'/>强化学习，就是把这条定律写成了数学。没有人告诉学习者正确的动作。只有一个数，一个奖励，在它行动之后才到来，有时候要过很久才到。",

    "Here is the setting, in its modern form. An agent and an environment take turns. <bookmark mark='a'/> At each step t the agent sees the state, s t, and chooses an action, a t. <bookmark mark='b'/> The environment answers with a reward, r t plus one, and a new state. And again, and again. <bookmark mark='c'/> Unrolled, the interaction is one long sequence: state, action, reward, state, action, reward. A game of Go is one such sequence, with every reward zero except the last: plus one for a win, minus one for a loss.":
        "这是它的现代形式。一个智能体和一个环境轮流行动。<bookmark mark='a'/>在每一步t，智能体看到状态s t，选择一个动作a t。<bookmark mark='b'/>环境回应一个奖励r t加1，以及一个新的状态。然后再来一次，再来一次。<bookmark mark='c'/>展开来看，这场互动就是一条长长的序列：状态、动作、奖励，状态、动作、奖励。一盘围棋就是这样一条序列，除了最后一个，所有奖励都是0：赢了是加1，输了是减1。",

    "The mathematical object is a Markov decision process. A set of states, a set of actions; <bookmark mark='a'/> the probability of each next state given the current state and action; a reward for each state and action; and a discount, gamma, that we'll meet in a moment. <bookmark mark='b'/> The word Markov carries the key assumption: the next state depends on the past only through the present state and action. Whatever history matters must be folded into the state. <bookmark mark='c'/> The framework is Richard Bellman's, from the 1950s, made for planning problems at the RAND Corporation long before anyone thought of learning.":
        "对应的数学对象叫马尔可夫决策过程。一组状态，一组动作；<bookmark mark='a'/>给定当前状态和动作，每个下一状态的概率；每个状态和动作的奖励；还有一个折扣γ，我们马上会讲到。<bookmark mark='b'/>“马尔可夫”这个词，带着一个关键假设：下一个状态只通过当前的状态和动作依赖过去。凡是重要的历史，都必须装进状态里。<bookmark mark='c'/>这套框架出自理查德·贝尔曼，是20世纪50年代他在兰德公司为规划问题而建立的，那时还根本没有人想到学习。",

    "What the agent wants is not the next reward but all of them. The return from time t, G t, adds them up, with each reward k steps away discounted by gamma to the k. <bookmark mark='a'/> With gamma zero point nine, a reward ten steps away counts for a third of one now. <bookmark mark='b'/> Turn gamma down, and the agent becomes short-sighted; gamma near one is a patient agent. <bookmark mark='c'/> The discount also keeps the sum finite even if the game never ends: if every reward is at most r max, the return is at most r max times a geometric series, <bookmark mark='d'/> r max over one minus gamma. <bookmark mark='e'/> And the return has a recursive shape. Pull out the first reward, and what is left is gamma times the return from the next step: G t equals r t plus one plus gamma G t plus one. The next three chapters are built on this one line.":
        "智能体想要的，不是下一个奖励，而是所有的奖励。从时刻t开始的回报G t，把它们加起来，k步之后的奖励要打上γ的k次方的折扣。<bookmark mark='a'/>γ取0.9时，10步之后的一个奖励，只相当于现在的三分之一。<bookmark mark='b'/>把γ调小，智能体就变得短视；γ接近1，就是一个有耐心的智能体。<bookmark mark='c'/>折扣还能让这个和保持有限，哪怕游戏永远不结束：如果每个奖励最多是r max，回报最多就是r max乘以一个几何级数，<bookmark mark='d'/>也就是1减γ分之r max。<bookmark mark='e'/>回报还有一个递归的形状。把第一个奖励拿出来，剩下的就是γ乘以从下一步开始的回报：G t等于r t加1，再加γ乘以G t加1。接下来三章，都建立在这一行式子上。",

    "Two more definitions, and we have the whole vocabulary. A policy, pi of a given s, is the agent's rule: a probability for each action in each state. <bookmark mark='a'/> The value of a state under a policy, V pi of s, is the return you expect if you start there and follow pi. <bookmark mark='b'/> Its cousin, the action value Q pi of s and a, is the expected return if you first take action a, and only then follow pi. <bookmark mark='c'/> Averaging Q over the policy's choices gives back V. <bookmark mark='d'/> Values are what everything in this part computes. Dynamic programming computes them exactly, temporal differences learn them from experience, and AlphaZero's network guesses them at a glance.":
        "再给两个定义，词汇就齐了。策略π，给定s时a的概率，是智能体的规则：在每个状态下，给每个动作一个概率。<bookmark mark='a'/>一个状态在某个策略下的价值，V π s，就是从这里出发、按π行动时，你预期得到的回报。<bookmark mark='b'/>它的近亲，动作价值Q π s a，是先采取动作a、之后再按π行动时，预期的回报。<bookmark mark='c'/>把Q按策略的选择取平均，就得回V。<bookmark mark='d'/>本部分的一切，算的都是价值。动态规划精确地算出它们，时序差分从经验中学到它们，而AlphaZero的网络看一眼就能猜出它们。",

    "Three things make this harder than learning from labelled examples. <bookmark mark='a'/> Credit assignment: in Go the reward arrives two hundred moves after the moves that earned it. Which of them deserves the credit? <bookmark mark='b'/> Exploration: you only see what happens after actions you actually try, so a learner that always does what looks best may never find out what is better. <bookmark mark='c'/> And the data depends on the learner: change the policy, and you change the states you see. <bookmark mark='d'/> In supervised learning every example comes with its answer, and the examples sit still. Here, neither is true.":
        "有三件事，让它比从带标签的样本中学习更难。<bookmark mark='a'/>功劳分配：在围棋里，奖励要在赢得它的那些棋步之后200手才到来。功劳该记在哪一步上？<bookmark mark='b'/>探索：你只能看到自己真正尝试过的动作会带来什么，所以一个总是做看起来最好的事的学习者，可能永远发现不了更好的。<bookmark mark='c'/>还有，数据取决于学习者自己：策略一变，你看到的状态也跟着变。<bookmark mark='d'/>在监督学习里，每个样本都带着答案，而且样本是固定不动的。在这里，两条都不成立。",

    'Chapter two. Explore or exploit.':
        '第2章。探索，还是利用。',

    "Before states and long horizons, take reinforcement learning with every complication removed but one. <bookmark mark='a'/> You face k slot machines, one-armed bandits. Each pays a random reward from its own distribution, and you don't know which is best. <bookmark mark='b'/> Pull one arm per step, for as many steps as you're given, and collect as much as you can. <bookmark mark='c'/> This is the problem a doctor faces choosing between treatments, and a website choosing which version of a page to show: Thompson posed it in 1933 about patients. <bookmark mark='d'/> There's one state, so no credit assignment and no planning. What's left is pure exploration: every pull spent learning about an arm that might be worse is a pull not spent on the arm that looks best.":
        "在讲状态和长远的规划之前，先看一个只留下一种困难的强化学习问题。<bookmark mark='a'/>你面前有k台老虎机，也叫单臂强盗。每一台都按自己的分布给出随机奖励，而你不知道哪台最好。<bookmark mark='b'/>每一步拉一根拉杆，能拉多少步就拉多少步，尽量多拿奖励。<bookmark mark='c'/>医生在几种疗法之间做选择，网站决定给用户看哪个版本的页面，面对的都是这个问题：1933年，汤普森就是针对病人提出它的。<bookmark mark='d'/>这里只有一个状态，所以没有功劳分配，也不需要规划。剩下的就是纯粹的探索：每花一次去了解一根可能更差的拉杆，就少拉一次看起来最好的那根。",

    "To compare strategies we need a score. The regret after T pulls is what you would have earned by always pulling the best arm, minus what you expect to earn. <bookmark mark='a'/> Each pull of a worse arm a costs its gap, delta a, so the regret is the sum over arms of the gap times the expected number of pulls of that arm. <bookmark mark='b'/> Epsilon-greedy pulls every arm a fixed fraction of the time forever, so its regret grows in proportion to T. <bookmark mark='c'/> A good strategy pulls the bad arms less and less often, so its regret grows much more slowly than T.":
        "要比较策略，需要一个分数。拉了T次之后的遗憾，就是一直拉最好那根本可以拿到的奖励，减去你预期能拿到的。<bookmark mark='a'/>每拉一次较差的拉杆a，就损失它的差距Δ a，所以遗憾等于对所有拉杆求和：差距乘以这根拉杆被拉的期望次数。<bookmark mark='b'/>ε-贪心永远以固定的比例去拉每一根拉杆，所以它的遗憾和T成正比地增长。<bookmark mark='c'/>好的策略会越来越少地去拉差的拉杆，所以它的遗憾比T增长得慢得多。",

    "A cleverer idea: optimism in the face of uncertainty. Act as if each arm is as good as it plausibly could be. How good is plausible? <bookmark mark='a'/> Hoeffding's inequality from Part 5: after n pulls, the chance that an arm's true mean lies more than epsilon above its average is at most e to the minus two n epsilon squared. <bookmark mark='b'/> Choose epsilon so that this chance is tiny, t to the minus four, <bookmark mark='c'/> and epsilon is the square root of two log t over n. <bookmark mark='d'/> That's the upper confidence bound algorithm, UCB: pull the arm with the highest average plus bonus. An arm pulled rarely has a big bonus, so it gets tried; the bonus shrinks as its pulls pile up, and grows slowly, like log t, for arms left alone, so no arm is abandoned for good. <bookmark mark='e'/> The payoff is a theorem: each worse arm is pulled only about log T over its gap squared times, so the regret grows like log T. <bookmark mark='f'/> And Lai and Robbins proved in 1985 that no strategy can do better than logarithmic regret. UCB is, up to constants, the best possible.":
        "一个更聪明的想法：面对不确定，保持乐观。把每根拉杆都当作它合理范围内最好的样子。多好才算合理？<bookmark mark='a'/>用第5部分的霍夫丁不等式：拉了n次之后，一根拉杆的真实均值比它的平均值高出ε以上的概率，至多是e的负2nε平方次方。<bookmark mark='b'/>选一个ε，让这个概率小到t的负4次方，<bookmark mark='c'/>ε就等于n分之2倍log t，再开平方。<bookmark mark='d'/>这就是置信上界算法，UCB：拉那根“平均值加加分”最高的拉杆。很少被拉的拉杆，加分很大，所以会被拿来试一试；被拉得越多，加分就越小；而没被拉的拉杆，加分会像log t那样慢慢增长，所以没有哪根拉杆会被永远放弃。<bookmark mark='e'/>收获是一条定理：每根较差的拉杆，只会被拉大约log T除以差距平方那么多次，所以遗憾像log T那样增长。<bookmark mark='f'/>而黎子良和罗宾斯在1985年证明了：任何策略都不可能比对数级的遗憾更好。所以，在常数意义下，UCB已经是最好的了。",

    'f"The obvious strategy: keep an average':
        "显而易见的策略：给每根拉杆记下奖励的平均值，然后总是去拉平均值最高的那一根。这就是贪心规则。<bookmark mark='a'/>这是它在萨顿和巴托那本书里的标准测试平台上的表现：10根拉杆，它们的均值本身也是随机的，重复运行2000次。贪心规则很早就认定了一开始碰巧回报不错的那根拉杆，只有{og:.0f}%的时候找到了最好的拉杆。<bookmark mark='b'/>解决办法是有意地去探索。ε-贪心每10次里随机拉一根：它有{oe:.0f}%的时候找到了最好的拉杆。<bookmark mark='c'/>但它永远不停止探索。哪怕已经知道了答案，它还是浪费掉十分之一的拉动。",

    'f"Watch it work on five arms.':
        "看它在5根拉杆上怎么工作。白点是每根拉杆的平均值，它上面的竖条是加分，顶端最高的那根拉杆会被拉动，用蓝框标出。<bookmark mark='a'/>一开始，每根拉杆的竖条都很高，于是轮流被拉。<bookmark mark='b'/>一根拉杆被拉得越多，它的竖条就越短，平均值低的拉杆就退出了竞争。拉了{steps}次之后，{share:.0f}%给了最好的拉杆，最差的那根只试了寥寥几次，刚好够确定它确实差。",

    'f"There\'s an older idea, from Thompson himself.':
        "还有一个更古老的想法，来自汤普森本人。为每根拉杆的均值保留一个后验分布，也就是第5部分的贝叶斯法则，每拉一次就更新一次。<bookmark mark='a'/>然后，每一步都从每个后验里抽一个可能的均值，去拉抽到的值最大的那根。<bookmark mark='b'/>一根拉杆被拉的频率，恰好等于它是最好那根的可能性：早已知道很差的拉杆几乎从不被拉，拿不准的拉杆偶尔会被拉。<bookmark mark='c'/>在10臂测试平台上，它有{ot:.0f}%的时候找到了最好的拉杆，是四种方法里最好的。再看一对硬币，<bookmark mark='d'/>横轴取拉动次数的对数，ε-贪心的遗憾向上弯，冲出了图外：它像T那样增长。UCB和汤普森采样在这里都是直线，像log T那样增长，而汤普森采样的那条线最平。<bookmark mark='e'/>记住置信上界。十章之后，它会在AlphaGo内部为搜索掌舵。",

    "Chapter three. Bellman's equation.":
        '第3章。贝尔曼方程。',

    'Start from the definition: the value of s':
        "从定义出发：s的价值，就是从s出发的期望回报。<bookmark mark='a'/>再用第1章的递推关系：回报等于下一个奖励，加上γ乘以之后的回报。<bookmark mark='b'/>分两步取期望：先对策略选出的动作取期望，再对环境把你送去的状态取期望。<bookmark mark='c'/>马尔可夫性质就在这里发挥作用。一旦到了s撇，从那里出发的期望回报，就是s撇的价值：你是怎么到那里的，完全无关紧要。<bookmark mark='d'/>这就是贝尔曼方程。一个状态的价值，等于你现在期望得到的奖励，加上γ乘以你期望落脚之处的价值。每个状态一个方程，每个方程都把一个状态的价值，和它邻居的价值联系在一起。",

    'Draw it as a tree. At the top, the state s.':
        "把它画成一棵树。最上面是状态s。<bookmark mark='a'/>策略在各个动作之间选择，也就是这些小圆点，概率是π。<bookmark mark='b'/>每个动作都可能通向好几个下一状态，概率由环境决定，途中还会得到一个奖励。<bookmark mark='c'/>贝尔曼方程说的是：价值沿着这棵树往上回流。把下一状态的价值，按落到那里的可能性加权平均，加上奖励，打个折扣，再对动作求平均。萨顿和巴托把这叫作回溯图。本部分的每一个算法，都是做这次回溯的一种不同方式：精确地做，用样本做，或者在搜索树里做。",

    'f"Here is a world to try it on:':
        "找一个世界来试试：一个有墙的网格，一个价值正1的终点，正下方是一个价值负1的陷阱。<bookmark mark='a'/>移动会打滑：80%的时候你会走到想去的地方，另外各有10%的时候滑向左右两侧。<bookmark mark='b'/>对一个固定的策略，贝尔曼方程就是{len(cells)}个未知数的{len(cells)}个线性方程。写成矩阵形式：V等于期望奖励向量，加上γ乘以转移矩阵再乘以V。<bookmark mark='c'/>把V都移到一边，<bookmark mark='d'/>一次矩阵求逆，就精确地得到了所有价值。<bookmark mark='e'/>对随机乱走的策略，结果就在这里：几乎哪里都不值什么，起点的价值是{Vr[g['start']]:+.3f}：一个随机乱走的人，掉进陷阱和找到终点的可能性差不多。",

    "That was one policy's value.":
        "刚才算的是一个策略的价值。我们想要的是最好的策略。它的价值V星满足同一个方程，只是把对动作的平均换成了最大值：这就是贝尔曼最优方程。<bookmark mark='a'/>如果知道了V星，最好的策略就是根据它贪心地行动：在每个状态，选回溯得到的期望价值最高的那个动作。<bookmark mark='b'/>这是网格世界的V星，以及它的贪心策略。<bookmark mark='c'/>看陷阱正下方的那一格。它的箭头朝下，背离终点。往上走会直接走进陷阱，往旁边走一步，也有十分之一的可能滑进去，所以最好的计划是绕远路。<bookmark mark='d'/>最大值让这些方程变成了非线性的，所以没法用一次矩阵求逆解决。下一章还是要解开它们：用迭代，并且证明这样一定行得通。",

    'Chapter four. Why value iteration works.':
        '第4章。值迭代为什么有效。',

    "Bellman's own answer to the nonlinear equations":
        "面对这些非线性方程，贝尔曼自己的答案是：迭代。先把所有价值都设为0。<bookmark mark='a'/>把最优方程的右边，同时作用到每一个状态上，把结果当作新的价值。然后再做一次。<bookmark mark='b'/>扫过一遍之后，只有挨着终点和陷阱的格子知道了一点东西。<bookmark mark='c'/>每扫一遍，消息就往外多传一步，价值从终点向外扩散，就像热量一样。<bookmark mark='d'/>扫过几十遍之后，就再也没有变化了：我们得到了V星，还有上一章的那些箭头。",

    'Why must this work? Write the right-hand side as an operator':
        "为什么这一定行得通？把右边写成一个算子T：输入一张价值表，输出一张新的表。<bookmark mark='a'/>一个小引理：两个最大值之差，不会超过被取最大值的那些量之间的最大差。<bookmark mark='b'/>比较T作用在两张不同的表V和U上的结果。奖励是一样的，所以相互抵消，剩下的是γ乘以一些差的平均。<bookmark mark='c'/>平均值永远不会超过其中最大的那一项。<bookmark mark='d'/>所以，在最大范数下，T把任意两张表之间的距离缩小到γ倍。它是一个压缩映射。<bookmark mark='e'/>1922年的巴拿赫不动点定理完成了剩下的工作：压缩映射恰好有一个不动点，而且从任何起点出发反复作用，都会以γ的速率几何收敛到它。这个不动点满足贝尔曼最优方程：它就是V星。",

    'f"Here\'s the theorem at work.':
        "来看这条定理怎么起作用。在网格世界上跑两次值迭代：一次从全0开始，一次从随机值开始。<bookmark mark='a'/>在对数坐标上，这是两次运行之间的最大差，一遍一遍地画出来。<bookmark mark='b'/>定理说，它必须一直待在虚线下面，也就是γ的k次方。在头十几遍里，它几乎正好贴着这条线走：每扫一遍，它都至少还剩下原来的{ratio:.3f}倍。然后，随着终点附近的格子稳定下来，它下降得更快了。不管从哪里出发，最后都到达同一个V星。",

    'f"There\'s a second classic algorithm, policy iteration':
        "还有第二个经典算法，策略迭代，来自1960年的罗纳德·霍华德。从任意一个策略开始：这里是“永远往上走”。<bookmark mark='a'/>精确地评估它，用第3章的线性求解。<bookmark mark='b'/>然后改进它：在每个状态，换成按这些价值看起来最好的那个动作。<bookmark mark='c'/>策略改进定理说：新策略在每个状态都至少一样好。证明只是把不等式一步一步展开。<bookmark mark='d'/>评估、改进、评估、改进：这里一共经过{n}个策略，然后策略就不再改变了。它就是最优的。<bookmark mark='e'/>评估和改进，相互追逐：萨顿和巴托把这叫作广义策略迭代。本部分几乎每一种方法，都是它的某个版本，AlphaZero也不例外。",

    "Both algorithms need two things we usually don't have.":
        "这两个算法都需要两样我们通常没有的东西。一是模型：把转移概率明明白白地写下来。二是把每个状态都扫一遍。<bookmark mark='a'/>我们的网格世界有44个状态。西洋双陆棋大约有10的20次方个。国际象棋，按克劳德·香农1950年的估计，大约有10的43次方个。围棋有2乘以10的170次方个合法局面，比可见宇宙中原子数的平方还多。<bookmark mark='b'/>出路是：不用模型，从经验的样本中学习；并且去近似价值函数，而不是把它列成一张表。这就是接下来三章的内容。",

    'Chapter five. Temporal differences.':
        '第5章。时序差分。',

    'Without a model, we learn values from experience':
        "没有模型，我们就从经验中学习价值：玩一局一局，看看会发生什么。最简单的办法是蒙特卡洛：<bookmark mark='a'/>一局结束后，把每个状态的价值，朝它后面实际得到的回报推一点。α是步长。把足够多的回报平均起来，就得到了价值。但你必须等到一局结束，而单个回报的噪声可能极大。<bookmark mark='b'/>时序差分学习不用等。走完一步，它就把价值朝“刚得到的奖励，加上γ乘以它自己对下一状态的当前估计”推一点。<bookmark mark='c'/>括号里的就是TD误差δ：你刚才的预测，和你现在的预测之间的差。<bookmark mark='d'/>用一个猜测去学另一个猜测，听起来像是循环论证，但它确实收敛，理查德·萨顿在1988年把它发展成了一套理论。这个想法可以追溯到1959年亚瑟·塞缪尔的跳棋程序：它会把自己对一个局面的评估，朝几步之后它自己的评估去调整。",

    'A small test, from Sutton and Barto: five states in a row.':
        "一个小测试，来自萨顿和巴托：5个状态排成一排。你从中间出发，随机地向左或向右走一步。从右边离开得1分；从左边离开，什么也没有。<bookmark mark='a'/>每个状态的真实价值，就是从右边离开的概率：从六分之一到六分之五。<bookmark mark='b'/>把每个估计都设为二分之一，然后运行TD。一局之后，只有挨着它离开的那个出口的状态动了。<bookmark mark='c'/>十局之后，消息已经向里传开了。<bookmark mark='d'/>一百局之后，估计值已经接近真值。",

    'Now compare the two methods properly':
        "现在认真比较这两种方法：估计的误差，对100次运行取平均，试了好几种步长。<bookmark mark='a'/>蒙特卡洛，橙色，进步得很慢。<bookmark mark='b'/>TD，蓝色，在我们试过的每一种步长下都学得更快。<bookmark mark='c'/>原因又是马尔可夫性质。蒙特卡洛把每个状态的回报分开处理。而TD对C的更新，用到的是D的当前估计，过去每一次访问D都改进过这个估计，所以经验在状态之间共享了。",

    'f"Monte Carlo and TD are the two ends of a spectrum.':
        "蒙特卡洛和TD是一条光谱的两端。先用n个真实奖励，再接一个猜测：这就是n步回报。<bookmark mark='a'/>把所有这些混合起来，权重像λ的n次方那样衰减：λ等于0是一步TD，λ等于1就是纯粹的蒙特卡洛。<bookmark mark='b'/>混合也不必等到最后。为最近访问过的状态留一条逐渐消退的痕迹，把每个TD误差沿着它分摊回去：这就是资格迹，一行代码就回答了功劳分配问题。<bookmark mark='c'/>在一条更长的随机游走上，十局之后的误差，每个λ取它自己最好的步长，最低点在中间：这里是λ等于{lams[bi]}。最好的方法，把真实奖励和自己的猜测混在一起用。",

    'The first great success of these ideas came in 1992':
        "这些想法的第一次巨大成功，出现在1992年，来自IBM的杰拉尔德·特索罗。TD-Gammon是一个神经网络，它看着西洋双陆棋的棋盘，估计获胜的概率。<bookmark mark='a'/>它只从和自己对弈的棋局中学习，用TD(λ)把每个局面的价值，朝下一个局面的价值推一点。下了150万局之后，它的水平已经接近世界顶尖棋手，它的一些不寻常的开局下法，还被人类高手采用了。自我对弈、学到的价值、时序差分：记住这三样。",

    "And there's a postscript from neuroscience.":
        "还有一段来自神经科学的后记。在猴子身上，当奖励出乎意料地到来时，多巴胺神经元会爆发式放电。<bookmark mark='a'/>一旦某个信号能可靠地预示奖励，这次爆发就移到了信号出现的时候，而奖励本身不再引起反应。<bookmark mark='b'/>如果预示的奖励没有来，放电就会在它本该到来的那一刻，降到正常水平以下。<bookmark mark='c'/>1997年，舒尔茨、达扬和蒙塔古指出：这就是TD误差。它是对未来奖励的意外，可正可负，并且会往回移到最早预示它的那件事上。",

    'Chapter six. Q-learning.':
        '第6章。Q学习。',

    'To act without a model, learn values of actions':
        "要在没有模型的情况下行动，就去学动作的价值，而不是状态的价值。有了Q，行动就很容易：选Q最高的那个动作，不需要转移概率。<bookmark mark='a'/>TD的想法可以直接搬过来。每走一步，就把s和a的Q值，朝“奖励，加上γ乘以下一步的价值”推一点。一种版本用的是智能体接下来真正采取的动作：状态、动作、奖励、状态、动作，所以它叫Sarsa。<bookmark mark='b'/>克里斯·沃特金斯在他1989年的博士论文里提出的版本，用的则是下一状态下最好的动作，不管智能体实际上做了什么。这就是Q学习。<bookmark mark='c'/>它一边以别的方式行动、一边探索，一边学到最优行动的价值。沃特金斯和达扬证明了它会收敛到Q星，前提是每个动作都一直有人去尝试，而且步长以合适的速率缩小。",

    'f"Watch both learn on the cliff walk':
        "来看它们俩在萨顿和巴托的悬崖行走上学习。从S出发，走到G；每走一步扣1分，走下悬崖扣100分，并且被送回起点。两者都会探索：每10步里有1步随机走。<bookmark mark='a'/>这是Q学习的第一局：一通瞎撞，掉下悬崖{falls}次之后，才找到终点。<bookmark mark='b'/>现在回放训练过程：颜色是学到的价值，线是如果停止探索，它会走的路径。每个价值都从0开始，所以一开始，到处看起来都一样好。<bookmark mark='c'/>价值从终点往回增长，路径也渐渐变直。<bookmark mark='d'/>它们最后得出了不同的答案。Q学习学到的是最优路径，紧贴着悬崖边走。Sarsa学到的是安全路径，沿着最上面走：它评价每个动作，依据的是还在探索的自己接下来会怎么做，而在悬崖边随机走一步，就是掉下去。",

    'f"Which is better depends on what you score.':
        "哪个更好，取决于你怎么算分。把两者在仍在探索时，每局得到的奖励画出来。<bookmark mark='a'/>Q学习的最优路径紧贴悬崖边，每隔一阵子，一步随机的动作就会让它掉下去：它平均得{late_q:.0f}分。<bookmark mark='b'/>Sarsa更长、更安全的路径，平均得{late_s:.0f}分。离策略学习找到的，是在一个不再探索的世界里最好的策略；同策略学习找到的，是对这个实际这样行动的智能体来说最好的策略。",

    "A table of Q values can't hold Go":
        "一张Q值表装不下围棋，甚至装不下一个电子游戏的画面，所以下一步，是用一个函数，也就是神经网络，去近似Q。<bookmark mark='t'/>而这里有一个陷阱。<bookmark mark='a'/>函数近似、自举、离策略学习：任意两个放在一起都没问题，但三个凑齐，价值就可能发散到无穷大，哪怕是在很小的问题上，1995年利蒙·贝尔德就展示过这一点。萨顿和巴托把它叫作致命三要素。<bookmark mark='b'/>带神经网络的Q学习，三样全占了。",

    'Chapter ten. Search before learning.':
        '第10章。学习之前的搜索。',

    'f"Games are where search was born.':
        "搜索诞生于棋类游戏。一棵博弈树：从当前局面出发，是你所有可能的走法，然后是对每一步的应对，如此往下。<bookmark mark='a'/>往前看几步，用一个评估函数给最底下的局面打分，这是人手工制定的、判断谁占优的标准。<bookmark mark='b'/>然后把分数往上回溯。轮到对手走的地方，假设他会选对你最不利的应对：取最小值。<bookmark mark='c'/>轮到你走的地方，选最好的：取最大值。<bookmark mark='d'/>根节点的值，就是无论对方怎么应对，你都能保证得到的结果。这就是极小化极大，来自冯·诺依曼1928年关于博弈的定理；最早的那些程序，1950年香农的设计和塞缪尔的跳棋程序，都是这样下棋的。<bookmark mark='e'/>但这棵树的大部分，根本不需要看。一旦某个应对表明，一步棋比你手上已有的某步棋差，这步棋的其他应对就无关紧要了。跳过它们，就是α-β剪枝；在这里，它跳过了{n}个局面中的{len(pruned)}个，而答案不变。",

    'f"How much does it save?':
        "它能省多少？在四子棋上往下搜9步：普通的极小化极大，要检查大约{mm / 1000000.0:.0f}00万个局面。<bookmark mark='a'/>α-β剪枝，按随机顺序尝试走法，只需要其中的一小部分。<bookmark mark='b'/>先试看起来最好的走法，它只检查{ab:,.0f}个。<bookmark mark='c'/>克努斯和摩尔证明了：在完美的排序下，代价从b的d次方，降到大约b的d/2次方：同样的工作量，α-β能让你搜索深一倍。",

    'This recipe beat the world chess champion.':
        "这套配方击败了国际象棋世界冠军。1997年，IBM的深蓝在六盘比赛中战胜了加里·卡斯帕罗夫。它在480块专用的国际象棋芯片上运行α-β搜索，每秒大约2亿个局面，评估函数里大约有8000个特征，由特级大师和工程师一起调校。<bookmark mark='a'/>搜索，加上人类设计出来的、关于好局面长什么样的判断。",

    'Go was different.':
        "围棋就不一样了。<bookmark mark='a'/>一个国际象棋局面，大约有35种走法；一个围棋局面，大约有250种，而一盘棋大约要下150手。完整的博弈树，大约有10的360次方个局面。<bookmark mark='b'/>更糟的是，没人能写出一个评估函数。数子力在国际象棋里管用；而在围棋里，谁占优取决于棋形和势力，强手是凭感觉，而不是靠计算。深蓝之后将近20年，最好的围棋程序仍然远远不如最强的人类。",

    'Chapter eleven. Monte Carlo tree search.':
        '第11章。蒙特卡洛树搜索。',

    'Go programs found a way around the missing evaluation':
        "围棋程序找到了一个绕开评估函数的办法：不去评估，而是采样。<bookmark mark='a'/>要判断一个局面，就从这里把棋下完很多次，双方都随机乱下，然后数一数谁赢了。<bookmark mark='b'/>一盘随机棋是一盘烂棋，但对几千盘取平均，胜率就能粗略地衡量谁的形势更好。1993年，贝恩德·布吕格曼在围棋上试过这个办法。",

    'Random games from the root waste effort':
        "从根节点出发的随机对局，会把力气浪费在坏棋上。蒙特卡洛树搜索则是长出一棵树，把模拟花在要紧的地方。每次模拟有四步。<bookmark mark='a'/>选择：从根节点出发，沿着树往下走，在每个节点选得分最高的子节点。<bookmark mark='b'/>这个得分就是第2章的置信上界：目前的胜率，加上对很少被尝试的子节点的加分。每个节点都是一个小小的老虎机问题。<bookmark mark='c'/>扩展：走到树的边缘时，加一个子节点。<bookmark mark='d'/>模拟：从那里随机下到终局。<bookmark mark='e'/>回溯：把结果加到路径上的每一个节点。<bookmark mark='f'/>雷米·库隆在2006年给它起名叫蒙特卡洛树搜索；同一年，科奇什和塞派什瓦里证明了：随着模拟次数增加，这个UCT规则会收敛到极小化极大选出的那步棋。",

    'f"Here is plain MCTS thinking about a Connect Four position':
        "这是普通的MCTS在思考一个四子棋局面，它的树画出来，每根树枝的粗细，代表经过它的模拟次数。<bookmark mark='a'/>{snaps[0]}次模拟之后，每一步都被试过一两次。<bookmark mark='b'/>随着次数增加，这棵树长得越来越偏：搜索不断回到看起来最好的走法，在那里看得更深，而毫无希望的走法，只得到刚好足以确认它们毫无希望的访问次数。<bookmark mark='c'/>{snaps[-1]:,}次模拟之后，它最喜欢第{best_mc + 1}列。",

    'f"But the perfect solver disagrees:':
        "但完美求解器不同意：第{best_true + 1}列能强制取胜，而第{best_mc + 1}列会输。<bookmark mark='a'/>随机对局是个很粗糙的裁判。在随机对局里，没有人会利用威胁，所以一步给对手送上胜机的棋，平均看起来也还不错。搜索的好坏，取决于它的评估。",

    'f"We can measure this exactly.':
        "我们可以精确地衡量这一点。四子棋已经被彻底解决了，所以对{d['n_pos']}个测试局面，我们知道每一步棋的真实价值。如果一步棋保住了这个局面所能得到的最好结果，赢棋，或者和棋，就说它是对的。<bookmark mark='a'/>随机走一步，有{100 * d['random']:.0f}%的时候是对的。<bookmark mark='b'/>普通的MCTS随着模拟次数增加而进步，每步{int(sims[-1]):,}次模拟时达到{100 * acc[-1]:.0f}%，然后就停住了：再多的随机对局，也修正不了一个有偏的裁判。",

    'MCTS transformed computer Go.':
        "MCTS彻底改变了电脑围棋。从2006年起，Crazy Stone和MoGo从初学者水平，一路爬到了业余强手。<bookmark mark='a'/>2013年，Crazy Stone战胜了一位职业棋手，不过对方让了它四子。<bookmark mark='b'/>缺的是一个更好的裁判：能像强手那样，看一眼局面就知道谁占上风。这正是神经网络将要提供的。",

    'Chapter twelve. AlphaGo.':
        '第12章。AlphaGo。',

    'This is the position from the opening of this part':
        "这就是本部分开头的那个局面：2016年3月，首尔，DeepMind的AlphaGo对李世石五番棋的第二局，李世石是此前十年里最强的棋手之一。<bookmark mark='a'/>执黑的AlphaGo，把第37手下在了这里：五线上的一手肩冲。<bookmark mark='b'/>职业解说员以为这是一步失误；按照棋理，这样的子应该下得更低。AlphaGo自己那个用人类棋谱训练出来的网络，估计人类会下这步棋的概率，大约只有万分之一。<bookmark mark='c'/>它还是下了，因为它的搜索说这是好棋，最后它赢下了这一局。",

    'AlphaGo, described in Nature in January 2016':
        "AlphaGo在2016年1月发表于《自然》杂志，它把深度网络放进了蒙特卡洛树搜索。它有四个组成部分。<bookmark mark='a'/>一个策略网络：13层的卷积网络，用业余强手之间对局的3000万个局面训练，去预测下一手：它有57%的时候猜中人类的着法，远远超过以前的程序。<bookmark mark='b'/>然后是它的第二个副本，用强化学习改进过，也就是第8章的策略梯度，和自己的早期版本对弈。它对监督学习得到的原版，胜率达到80%。<bookmark mark='c'/>一个价值网络，也就是缺失的那个裁判：它看一眼局面，估计谁会赢。它的训练数据，来自强化后的网络自我对弈的棋局，每盘棋只取一个局面，这样它就没法简单地把棋局背下来。<bookmark mark='d'/>还有一个很小、很快的策略，用来做快速走子，就像经典的MCTS那样。",

    'The search is MCTS with two changes.':
        "搜索就是MCTS，只做了两处改动。<bookmark mark='a'/>选择走法时，探索加分要乘上策略网络给出的先验概率P：强手会考虑的走法，会被优先探索，而随着一步棋的访问次数增加，加分逐渐消失。这和UCB是同一种乐观，只是由直觉来掌舵。<bookmark mark='b'/>到达叶节点时，它不再只依赖随机对局：叶节点的价值，一半来自价值网络的判断，一半来自一次快速走子的结果。<bookmark mark='c'/>策略网络让搜索变窄，价值网络让搜索变浅。",

    'In October 2015 AlphaGo had beaten the European champion':
        "2015年10月，AlphaGo以5比0击败了欧洲冠军樊麾，这是程序第一次在不让子的情况下，在全尺寸棋盘上战胜职业棋手。<bookmark mark='a'/>在首尔，它以4比1战胜了李世石。<bookmark mark='b'/>李世石赢下的那一局，第四局，转折点是他自己的第78手：一手挖。按AlphaGo自己的策略网络，这步棋的概率同样大约只有万分之一。它的搜索没有看那里，于是它走偏了。由网络引导的搜索，会继承网络的盲点：到第15章时，记住这一点。",

    'Chapter fourteen. Planning with a learned model.':
        '第14章。用学到的模型做规划。',

    'AlphaZero searches by playing moves forward in its head':
        "AlphaZero做搜索的方式，是在脑子里把棋往前下，为此它需要规则：一个完美的模拟器，告诉它每走一步之后，棋盘会变成什么样。<bookmark mark='a'/>大多数问题都没有规则手册。一台机器人，一个以像素呈现的电子游戏，一座冷却系统。<bookmark mark='b'/>所以：从经验中学一个世界的模型，然后在模型里面搜索。",

    'MuZero, from DeepMind in 2019, does exactly that':
        "DeepMind在2019年提出的MuZero，正是这样做的，它用了三个学出来的函数。<bookmark mark='a'/>表示函数h，把当前的观测变成一个隐状态。<bookmark mark='b'/>动态函数g，输入一个隐状态和一个动作，预测奖励和下一个隐状态：想象中的一步。<bookmark mark='c'/>还有预测函数f，也就是AlphaZero的网络，对任何隐状态给出策略和价值。树搜索完全在隐状态上进行。<bookmark mark='d'/>它们是一起训练的：沿着真实的轨迹，把模型往前展开5步，让它预测的奖励、价值和策略，去匹配真实的奖励、回报，以及搜索的选择。<bookmark mark='e'/>关键的选择是：从来不要求隐状态去重建画面或者棋盘。它只需要预测对规划有用的东西。一个只知道有用之事的世界模型。",

    'MuZero matched AlphaZero at Go, chess and shogi':
        "MuZero在围棋、国际象棋和将棋上追平了AlphaZero，而且从来没有被告知规则；它还在雅达利游戏上创下了新的最好成绩。<bookmark mark='a'/>EfficientZero让它变得节俭：只玩了相当于两个小时的游戏，就在雅达利上超过了人类的中位数水平。<bookmark mark='b'/>Gumbel MuZero让搜索哪怕只用寥寥几次模拟，也能被证明一定会改进策略。<bookmark mark='c'/>还有一个版本投入了实际工作，用来压缩YouTube视频，节省了大约4%的比特。<bookmark mark='d'/>学习世界如何运转、并在其中做规划的模型，会在第29部分再次出现。",

    'Chapter fifteen. Beyond perfect information.':
        '第15章。超越完全信息。',

    'Chess and Go show both players everything.':
        "国际象棋和围棋，把一切都摆在两位棋手面前。扑克不是这样。<bookmark mark='a'/>你知道自己的牌，却不知道对手的，所以你没法在一棵局面树上搜索：你只知道自己可能身处哪一组局面之中，这叫信息集。<bookmark mark='b'/>而且，最好的打法必然是随机的。如果你总是拿好牌下注、拿坏牌从不下注，你的下注就暴露了你的牌；你必须诈唬，而且要用恰当的概率。<bookmark mark='c'/>目标是纳什均衡：每位玩家各有一个策略，任何一方单独改变策略，都占不到便宜。在两人零和博弈里，照着它打，无论对手是谁，都能保证你拿到这个博弈的值。",

    'The tool is regret.':
        "工具是遗憾。每一轮之后，对每个动作都问一句：如果到目前为止，我每次都选它，我会好多少？<bookmark mark='a'/>遗憾匹配按每个动作的正遗憾，成比例地选择它。<bookmark mark='b'/>这里有两个遗憾匹配者在玩石头剪刀布，这个三角形代表三种出法的所有混合。它们当前的策略相互追逐，转了一圈又一圈：一方偏爱什么，另一方就学会克制什么。<bookmark mark='c'/>但它们策略的平均，会螺旋式地收拢到三分之一、三分之一、三分之一：也就是均衡。<bookmark mark='d'/>这是一条定理：在两人零和博弈中，如果每位玩家的遗憾增长得比轮数慢，平均策略就会趋近纳什均衡。",

    'f"For a card game, apply regret matching separately':
        "对于纸牌游戏，就在每个信息集上分别做遗憾匹配，也就是玩家可能身处的每一种情形，并按对手的打法有多大可能通向那里来加权。这就是反事实遗憾最小化，CFR，由马丁·津克维奇和同事在2007年提出。<bookmark mark='a'/>这是它在库恩扑克上的表现，这是一个只有三张牌的玩具游戏。<bookmark mark='b'/>可被利用度，也就是一个完美的对手能从平均策略那里赢走多少，稳步下降，大约像迭代次数的平方根分之一那样。<bookmark mark='c'/>它最后稳定下来的值是{val[-1]:.4f}：正是这个游戏已知的值，负十八分之一。先手玩家略处劣势，而它找到的策略里，包括拿着J诈唬。",

    'Scaled up with abstraction and real-time search':
        "加上抽象和实时搜索，规模扩大之后，CFR征服了扑克。<bookmark mark='a'/>2015年，Cepheus基本上解决了两人限注德州扑克。<bookmark mark='b'/>2017年，Libratus在无限注德州扑克上击败了顶尖职业选手，<bookmark mark='c'/>2019年，Pluribus在六人局中击败了精英职业选手，而它的训练只花了不到150美元的算力。",

    'In games with many strategies, plain self-play':
        "在策略繁多的游戏里，单纯的自我对弈可能会兜圈子，就像三角形里那些当前策略一样：每个新版本都能打败上一个，却忘了怎么打败再上一个。<bookmark mark='a'/>为了星际争霸2，AlphaStar训练了一整个联赛：主智能体；专门挖掘主智能体弱点的剥削者；还有一个由过去的自己组成的池子，每个人都必须一直能打败它们。<bookmark mark='b'/>它达到了宗师级别，超过了99.8%的天梯人类玩家。",

    "There's a sobering coda.":
        "还有一段发人深省的尾声。2023年，研究人员训练了一个程序，按任何正常标准，它的围棋都很弱，但它只有一个目的：打败KataGo，一个开源的、超越人类的AlphaZero后代。它找到了一个盲点：一种环形的棋块，网络会对它判断失误。一位人类业余棋手学会了这个技巧，在15盘棋里赢了一个顶级程序14盘。<bookmark mark='a'/>记住第78手。平均意义上超越人类，并不等于在最坏情况下也稳健，这一课会在本系列的最后一部分再次出现。",

    'The AlphaZero recipe has also been turned on problems':
        "AlphaZero的配方，还被用在了根本不是游戏的问题上：办法是把它们变成游戏。<bookmark mark='a'/>AlphaTensor把寻找矩阵乘法算法，当作一个单人游戏，找到了在二进制算术下，只用47次乘法就能完成4乘4矩阵相乘的方法，打破了自1969年施特拉森以来保持的49次的纪录。<bookmark mark='b'/>AlphaDev玩的是一个写汇编代码的游戏，为短列表找到了更快的排序例程，它们现在已经是LLVM使用的标准C++库的一部分。<bookmark mark='c'/>同样的这些工具，策略梯度、PPO、搜索和自我对弈，也正是今天的语言模型被教会听从指令和推理的方法。",

    'Chapter eight. Policy gradients.':
        '第8章。策略梯度。',

    'Value methods learn how good things are, and act greedily.':
        "价值方法学的是各种东西有多好，然后贪心地行动。策略梯度方法跳过这一步，直接调整策略本身。把策略做成一个参数为θ的网络，为每个动作输出一个概率。<bookmark mark='a'/>目标是一局的期望总奖励，J(θ)。用梯度上升去爬这座山。<bookmark mark='b'/>这样能处理连续的动作，比如一个扭矩，或者一个转向角，在这种情况下，对动作取最大值本身就是个难题。<bookmark mark='c'/>它能学出有意随机的策略，而石头剪刀布或者扑克里最好的打法，必须是随机的。<bookmark mark='d'/>而且，行为会随着θ平滑地变化，而不是每当两个Q值交换顺序时，就突然跳变。",

    'The gradient of an expectation over episodes looks hopeless':
        "对一局一局的期望求梯度，看起来毫无希望：每一局的概率，既取决于θ，也取决于环境的动态，而后者我们并不知道。<bookmark mark='a'/>第5部分的对数导数技巧挽救了它：p的梯度，等于p乘以log p的梯度。<bookmark mark='b'/>于是，梯度本身也是对各局的一个平均，而平均可以用采样来估计：玩几局，取平均。<bookmark mark='c'/>更妙的是，一局的对数概率可以拆成两部分：策略的选择，和环境的转移，而环境那部分不依赖于θ。它的梯度是零。我们从来不需要模型。<bookmark mark='d'/>再改进一点：一个动作影响不了它之前的奖励，所以每个动作只记它之后的回报。这就是REINFORCE，罗纳德·威廉姆斯1992年的算法。",

    'In plain terms: the policy tries actions.':
        "说白了：策略去尝试各种动作。<bookmark mark='a'/>每个动作之后，都跟着某个回报。<bookmark mark='b'/>把每个采取过的动作的对数概率往上推，推多少，和它的回报成正比。<bookmark mark='c'/>后面跟着好结果的动作变得更可能，而因为概率加起来等于1，其他动作就得让路。这就是试错，桑代克的效果律，写成了一个梯度。",

    'The catch is variance.':
        "问题在于方差。在倒立摆里，每个回报都是正的，所以每个动作都被往上推，而真正的信号，是一些大数之间的小差别。<bookmark mark='a'/>解药是从回报里减去一个基线，它可以是状态的任何函数。<bookmark mark='b'/>这不需要付出任何代价：对动作取平均，基线那一项等于b乘以所有概率之和的梯度，<bookmark mark='c'/>而概率之和永远是1。它的梯度是零。估计仍然是无偏的，而噪声可以小得多。",

    'f"Here is what that buys, measured.':
        "来看看这能换来什么，实际测一下。取一个训练到一半的倒立摆策略，玩300局，算出每一局单独给出的梯度。每个点是一个估计，投影到真实梯度的方向和另一个方向上。<bookmark mark='a'/>没有基线时，这些估计在真实梯度，也就是那支橙色箭头的周围，散得很开。<bookmark mark='b'/>有了基线，也就是每个时间步的平均回报，它们就聚在了一起：方差小了{ratio:.1f}倍。期望的梯度一样，而要同样清楚地看出它，需要的局数大约只有一半。",

    "The best baseline is the state's value, V.":
        "最好的基线，是状态的价值V。这样，乘在梯度前面的就是优势：这个动作的结果，比在这个状态下本来就能预期的，好了多少。<bookmark mark='a'/>我们不知道V，所以用第二个网络去学它，这个网络叫评论家，用TD来训练。它的TD误差本身，就是对优势的一个估计。<bookmark mark='b'/>就像TD(λ)混合n步回报一样，广义优势估计混合n步优势，用λ在偏差和方差之间做权衡。<bookmark mark='c'/>一个负责行动的演员，一个负责评判的评论家：这就是演员-评论家。这种架构可以追溯到1983年巴托、萨顿和安德森的倒立摆控制器，正是本章屏幕上的这个任务。",

    'Chapter nine. Trust regions and PPO.':
        '第9章。信赖域与PPO。',

    'Policy gradients have a fragile point: the step size.':
        "策略梯度有一个脆弱之处：步长。梯度只是对哪边是上坡的一个局部猜测。<bookmark mark='a'/>步子迈得太大，策略就可能落到很糟的地方。在监督学习里，你可以在下一批数据上恢复过来；但在这里，下一批数据是由这个糟糕的策略生成的：它表现很差，只看到糟糕的状态，可能再也找不到回来的路。<bookmark mark='b'/>而且，数据是旧策略收集的。新策略走得越远，这些数据对它说明的就越少。<bookmark mark='c'/>所以：只信任落在一个区域内的步子，在这个区域里，新策略和旧策略保持接近。",

    "To reuse the old policy's data, weigh each sample":
        "为了重用旧策略的数据，给每个样本乘上一个比值：新策略的概率，除以旧策略的概率。<bookmark mark='a'/>这样就得到一个替代目标，完全用已经收集好的数据来估计，而它在旧参数处的梯度，恰好就是策略梯度。<bookmark mark='b'/>TRPO，约翰·舒尔曼2015年的信赖域方法，在新旧策略之间的KL散度不超过一个上限的约束下，最大化这个目标。求解这个约束，会引出第11部分的自然梯度：精确，但是笨重，每一步都要做二阶计算。",

    "In 2017 Schulman's team found a much simpler way":
        "2017年，舒尔曼的团队找到了一种简单得多的保持接近的方法，它成了默认的选择：近端策略优化，PPO。<bookmark mark='a'/>把这个比值裁剪到一个区间里，从1减ε到1加ε，ε通常取0.2，然后在裁剪过的和没裁剪的目标里，取较小的那个。<bookmark mark='b'/>对一个好的动作，提高它的概率有好处，但只到比值达到1.2为止；超过之后，目标变平了，梯度也随之消失。<bookmark mark='c'/>对一个坏的动作，降低它的概率有好处，但只到0.8为止，再低就没有了。取最小值，保留的是悲观的那一支：一个会让情况变糟的步子，永远不会被裁剪掉。所以你可以在同一批数据上跑好几轮梯度更新，而策略不会跑飞。",

    'Here is PPO learning the cart-pole, replayed.':
        "这是PPO学习倒立摆的过程回放。右边是策略本身：在每个状态下，向左推或向右推的概率。一开始，处处都是抛硬币，一片均匀的灰色。<bookmark mark='a'/>一批又一批，两种颜色沿着DQN找到的那条倾斜的线分开了，每局也越来越长。和DQN不同，这个策略在边界附近，也就是它拿不准的地方，保持着柔和，直到训练把它磨得更锐利。",

    'PPO went everywhere.':
        "PPO被用到了各个地方。<bookmark mark='a'/>2019年，OpenAI Five以巨大的规模使用它，在相当于4.5万年的自我对弈之后，击败了Dota 2的世界冠军。<bookmark mark='b'/>在机器人领域，软演员-评论家把策略的熵加到奖励里，让它一直保持探索。<bookmark mark='c'/>它也是RLHF里的那个强化学习，正是这一步，把语言模型变成了ChatGPT，见第27部分。<bookmark mark='d'/>它的后代GRPO去掉了评论家，如今用来训练推理模型，见第28部分。",

    'Chapter seven. Deep Q-networks.':
        '第7章。深度Q网络。',

    'In 2013 a small London company, DeepMind':
        "2013年，伦敦一家小公司DeepMind，展示了一个直接看原始屏幕、玩雅达利电子游戏的Q学习智能体。<bookmark mark='a'/>输入是最近的4帧画面，缩小到84乘84像素。<bookmark mark='b'/>三个卷积层，也就是第10部分的视觉网络，然后是一层输出：为每个摇杆动作输出一个Q值，最多18个。<bookmark mark='c'/>2015年发表在《自然》上的论文，用同一个网络、同样的设置，训练了49个不同的游戏，从《乒乓》到《打砖块》，再到《太空侵略者》。总体上，它达到了专业人类游戏测试员的水平，在其中29个游戏上，得分超过了测试员的四分之三。唯一的信号，就是游戏分数的变化。",

    'DQN is Q-learning with the update turned into a loss':
        "DQN就是把Q学习的更新变成一个损失函数：TD误差的平方，用梯度下降来最小化。有两个技巧，把致命三要素挡在门外。<bookmark mark='a'/>第一，经验回放，这是Long-Ji Lin在1992年提出的想法。每一次转移都存进一个很大的记忆库，每次更新都从里面随机抽一批来训练。<bookmark mark='b'/>相邻的画面几乎一模一样，所以按顺序拿它们训练，就像把同一页书读了一遍又一遍。随机抽出的一批，看起来彼此独立，而且每一条经验都会被用上很多次。<bookmark mark='c'/>第二，目标网络：目标值由网络的一个冻结副本来计算，<bookmark mark='d'/>这个副本每一万步才更新一次，所以网络不会去追一个随着它每走一步就跟着移动的目标。",

    'f"Here is DQN learning a classic control task':
        "这是DQN在这台机器上学习一个经典控制任务：倒立摆。把小车往左推或往右推，让杆子保持竖直；杆子每立住一步得1分，最多500分。<bookmark mark='a'/>右边是网络学到的东西：对每一个杆子角度和角速度，它更倾向往哪边推。<bookmark mark='b'/>没训练的时候，它到处都往同一个方向推，杆子几步就倒了。<bookmark mark='c'/>我们来回放训练过程，选的是我们{n_runs}次运行里最好的那一次。每隔几千步，把网络冻结，让它来平衡。<bookmark mark='d'/>这张图自己组织成了两半：如果杆子正往右倒，就往右推，让小车回到它的下面。分界线是倾斜的，因为杆子转得快，和杆子倾斜得厉害一样要紧。没有人教过它任何物理。",

    'f"There\'s a subtler flaw in the max.':
        "取最大值，还有一个更隐蔽的缺陷。Q值是带噪声的估计，而最大值会挑出碰巧偏高的那个。<bookmark mark='a'/>根据詹森不等式，估计值的最大值的期望，至少等于真实值的最大值。<bookmark mark='b'/>如果10个动作的真实价值都是0，而每个估计都带有大小为1的噪声，那么最大值平均是{em[-1]:.2f}。Q学习就在这种乐观之上，不断地自举。<bookmark mark='c'/>在萨顿和巴托的测试里，一个有10个略亏动作的分支看起来很诱人，Q学习走进去的次数，远远超过应有的次数。<bookmark mark='d'/>解决办法来自哈多·范哈塞尔特：让一组估计去选动作，另一组去评估它。误差不再叠在一起，双Q学习几乎立刻就走向了正确的选择。双DQN用目标网络作为第二组估计，来实现这一点。",

    'Atari became the proving ground for a decade.':
        "此后十年，雅达利成了试验场。<bookmark mark='a'/>双DQN；更频繁地抽取意外转移的回放；把价值和优势分开的网络。<bookmark mark='b'/>分布式强化学习，它学习回报的整个分布，而不只是平均值。<bookmark mark='c'/>2018年，Rainbow把其中六个想法结合在一起，<bookmark mark='d'/>2020年，Agent57第一个在全部57个游戏上都超过了人类基准，包括《蒙特祖玛的复仇》，那里的奖励极其稀少，探索就是一切。",

    'Chapter thirteen. Learning from zero.':
        '第13章。从零开始学习。',

    'Eighteen months after Seoul, DeepMind published AlphaGo Zero':
        "首尔之战18个月后，DeepMind发表了AlphaGo Zero，几乎把所有东西都拿掉了。<bookmark mark='a'/>没有人类棋谱：它从随机乱下开始。没有手工设计的特征：输入就只是棋子。没有随机走子。只有一个网络，而不是分开的策略网络和价值网络。<bookmark mark='b'/>和自己下了3天、490万盘棋之后，它以100比0击败了战胜李世石的那个版本。<bookmark mark='c'/>40天之后，它以89比11击败了AlphaGo Master，这个版本曾在网上对顶尖职业棋手取得60连胜。人类知识越少，它反而越强。",

    'The whole algorithm is one loop.':
        "整个算法就是一个循环。一个网络看着一个局面，输出两样东西：每一步棋的概率p，以及一个价值v，也就是它对谁会赢的估计。<bookmark mark='a'/>它和自己对弈，每一步都由一次蒙特卡洛树搜索来选，而引导搜索的，正是这个网络自己。<bookmark mark='b'/>下过的每个局面都被保存下来，带着两个标签：π，搜索的访问次数；z，最后谁赢了。<bookmark mark='c'/>然后用它们训练网络：价值头去预测结果，策略头去预测搜索选了什么，再加上权重衰减。<bookmark mark='d'/>改进后的网络，再去下接下来的棋局。",

    'Why does this work? The search, guided by the network':
        "这为什么行得通？由网络引导的搜索，是比网络本身更强的棋手：它的访问次数，是比网络原始概率更好的策略。<bookmark mark='a'/>所以，训练网络去模仿搜索，就改进了策略；<bookmark mark='b'/>而用棋局结果训练价值头，就是在评估策略。<bookmark mark='c'/>这就是第4章的策略迭代：由搜索来做改进，由一个神经网络同时承载策略和它的价值。每一代的网络，都让下一代的搜索变得更强。<bookmark mark='d'/>2017年12月，同一个算法，除了规则之外什么都没改，又学会了国际象棋和将棋，并在几个小时之内就超过了最强的程序。在国际象棋里，它每秒只看6万个局面，是Stockfish所需的千分之一：网络的判断，取代了蛮力。",

    'Three ingredients made it work.':
        "让它成功的有三样东西。自我对弈，它总能提供一个强度恰到好处的对手。<bookmark mark='a'/>搜索，它把一个网络变成了自己的、稍强一点的老师。<bookmark mark='b'/>还有一个学出来的价值函数，也就是围棋程序几十年来一直缺少的那个裁判。<bookmark mark='c'/>这就是1992年TD-Gammon的配方，再加上搜索。",

    "Let's take stock.":
        '我们来总结一下。学会行动，从探索开始，而置信上界的乐观，探索得恰到好处。贝尔曼方程把每个状态的价值和它邻居的价值联系起来，又因为它的算子是一个压缩映射，迭代它总会收敛。时序差分通过自举，从经验中学习价值，Q学习则学会行动；有了经验回放和目标网络，深度网络也能做到。策略梯度直接改进策略，PPO的裁剪让每一步都安全。由学到的策略和价值引导、用自己的棋局来训练的搜索，带来了AlphaZero。而在信息被隐藏的地方，最小化遗憾能找到均衡。',

    'All of this comes back.':
        '所有这些都会再次出现。PPO，加上从人类偏好中学到的奖励，就是聊天模型的训练方法，见第27部分。在可以核对答案的题目上做策略梯度，以及在思维链上做搜索，造就了推理模型，见第28部分。学到的世界模型和长远的规划，是第29部分的主题。而当一个智能体去优化一个有缺陷的奖励，或者一个超越人类的系统有一个盲点时，会发生什么，会在最后一部分再次出现。',

    'Here are six problems to try':
        '这里有六道题可以试试，从UCB背后的置信界，到遗憾和均衡。在这里暂停一下，把它们做一做；完整的解答在本部分的笔记里。',

    'Next time: how a language model that only predicts text':
        '下一次：一个只会预测文本的语言模型，是怎样变成一个助手的。监督学习的示例，从人类偏好中学到的奖励模型，还有本部分的PPO，用一根绳子拴在它出发时的那个模型上：后训练与对齐。',

    "Sutton and Barto's book is the place to go deeper":
        '要深入学习，就去读萨顿和巴托的书：本部分的所有内容都在里面，而且是为第一次学习的人写的。感谢观看，第27部分再见。',

    'f"Now we do it ourselves, at toy scale, on this computer.':
        "现在我们自己来做，规模很小，就在这台电脑上。游戏是四子棋。<bookmark mark='a'/>网络很小，{BLOCKS}个残差块；每一步做{SIMS}次模拟搜索；每一代先和自己下{GAMES_PER_GEN}盘棋，再用这些棋局训练。{gens[-1]}代一共用了大约{g['hours']:.0f}个小时。<bookmark mark='b'/>而且和围棋不同，四子棋已经被彻底解决了：存在一个完美的棋手，所以我们可以给网络下的每一步棋打分。",

    'f"Finally, watch it play out a position where only one move keeps the win':
        "最后，看它在不同阶段，从一个只有一步棋能保住胜局的局面出发，和自己对弈，每一步都由求解器检查：绿色是对的走法，红色是送掉赢棋或和棋的错误。<bookmark mark='a'/>第{keys[0]}代，{len(first['perfect'])}步里对了{f_ok}步。<bookmark mark='b'/>第{keys[-1]}代，{len(last['perfect'])}步里对了{l_ok}步。",

    'f"Why does dropping the target network wreck it?':
        "为什么去掉目标网络会毁掉它？这是网络预测出的最大价值，用对数坐标画出来。真实价值不可能超过100：每步1分，再打折扣。<bookmark mark='a'/>有目标网络时，预测值{settle}。<bookmark mark='b'/>没有目标网络时，它们就失控了：不到{k1:,}步就超过了1000，到最后达到大约10的{e_end}次方。每次更新，都在追一个跟着自己移动的目标，误差不断自我放大：这就是第6章的致命三要素，在这台机器上现场上演。",

    'f"Its best moment came at {int(steps[best]):,} steps':
        '它最好的时候在第{int(steps[best]):,}步，能平衡500步里的{int(L[best])}步。然后，随着训练继续，它又变差了：到最后只能坚持{int(L[-1])}步。这就是DQN出了名的不稳定，致命三要素仍在起作用；实践中，人们会保留最好的那个检查点。',

    "f'By {int(steps[best]):,} steps it balances":
        '到第{int(steps[best]):,}步，它能平衡500步里的{int(L[best])}步，训练结束时是{int(L[-1])}步。',

    'f"Do the tricks matter?':
        "这些技巧重要吗？用三种方式训练它，每种{len(d['full'])}次，把整个训练过程中的回合长度取平均。<bookmark mark='a'/>没有回放记忆，每走一步就拿这一步来学：大约{avg['no_replay']:.0f}。<bookmark mark='b'/>有回放但没有目标网络：大约{avg['no_target']:.0f}{never}。<bookmark mark='c'/>两者都有：大约{avg['full']:.0f}。{tail}",

    'Each trick earns its place. And look at the bands':
        '每个技巧都物有所值。再看看这些色带：即使是最好的版本，每次运行之间也起伏很大。',

    'On a problem this small, the tricks matter less than the luck of the seed':
        '在这么小的问题上，技巧没有随机种子的运气重要：看看这些色带。在雅达利上，它们是决定性的：在《自然》那篇论文里，没有回放的打砖块只得了大约10分，有回放则是317分。',

    'f"On the cart-pole, with the same networks and the same budget of experience':
        "在倒立摆上，用同样的网络、同样多的经验，每种各跑{len(d['ppo'])}次：普通的REINFORCE，<bookmark mark='a'/>带基线的REINFORCE，<bookmark mark='b'/>以及用广义优势估计的演员-评论家。在整个训练过程中平均，它们的回合分别持续{auc['reinforce']:.0f}、{auc['baseline']:.0f}和{auc['ac']:.0f}步。{verdict}",

    'On a task this small, all three get there, and the differences are modest.':
        '在这么小的任务上，三者都能学会，差别也不大。倒立摆每一步都给奖励，回合又短，所以即使是普通REINFORCE的噪声，也负担得起。在长任务上，奖励要在赢得它的动作之后很久才到来，那时正是这种噪声让学习停滞，基线和评论家才显出它们的价值。',

    "f'Against the policy-gradient methods of the last chapter, PPO, in bold blue, gets the most":
        "和上一章的策略梯度方法相比，粗蓝线的PPO从同样的经验里得到的最多：在整个训练中，它的回合平均{auc['ppo']:.0f}步，而其余方法里最好的是{rest:.0f}步，因为它在每一批数据上走好几步小心的更新，而不是只走一步。",

    'f"Against the policy-gradient methods of the last chapter, PPO, in bold blue, averages':
        "和上一章的策略梯度方法相比，粗蓝线的PPO在整个训练中平均{auc['ppo']:.0f}步，而其余方法里最好的是{rest:.0f}步：在这么小的任务上，它们差别不大。PPO的优势在于大规模时的可靠。它能在每一批数据上走好几步，而不会冲下悬崖，也几乎不需要调参，所以它成了默认的选择。",

    'f"Here is the training, replayed through one position.':
        "这是训练过程，通过一个局面回放出来。每一列上方，是网络在搜索之前下在这一列的概率。下方是完美求解器的判定：保住最好结果的走法打一个勾。<bookmark mark='a'/>第0代的网络还没训练：柱子几乎是平的，价值是{V[0]:+.2f}。<bookmark mark='b'/>看着一代代过去。概率随着网络理解的变化而移动，{end}",

    'and settles on the right columns, while the value':
        '最后落在正确的那几列上，而价值，也就是它对谁会赢的估计，变得自信而且正确。',

    "f'and settles on the right columns; the value":
        '最后落在正确的那几列上；而价值，也就是它对谁会赢的估计，仍然不那么肯定：{V[-1]:+.2f}。',

    "but even the final network's favourite column here is not a right one":
        '但即使是最后一代网络，在这里最喜欢的那一列也不是对的：在这个局面上，它的直觉仍然是错的，只有搜索能救它。',

    'f"And search sharpens it.':
        '而搜索会让它更锐利。橙金色表示最后一代网络的搜索，从这个局面出发，把{SIMS}次模拟花在了哪里：{100 * v_win:.0f}%花在能赢的列上，而网络的第一直觉只有{100 * p_win:.0f}%。直觉和搜索之间的这个差距，正是下一代要学习的东西。',

    'f"In orange-gold, where the final network\'s search spends':
        '橙金色表示最后一代网络的搜索，从这个局面出发，把{SIMS}次模拟花在了哪里：{100 * v_win:.0f}%花在能赢的列上，和网络自己的{100 * p_win:.0f}%很接近。在这里，直觉已经和搜索一样好；而在两者有差距的地方，这个差距就是下一代要学习的东西。',

    'f"Graded on four hundred test positions, generation by generation.':
        "在四百个测试局面上，一代一代地打分。<bookmark mark='a'/>只用网络，完全不搜索，它从随机乱走，进步到有{final_raw:.0f}%的时候选出对的一步，也就是保住赢棋或和棋的一步；<bookmark mark='b'/>加上{SIMS}次模拟的搜索，是{final_mc:.0f}%。<bookmark mark='c'/>{vs_uct}<bookmark mark='d'/>在像棋手那样评分的直接对局里，{climb}：最后一代比未经训练的网络高出大约{gap:.0f}个Elo分，{rel}",

    'each generation we rated is stronger than the one before':
        '我们评过分的每一代，都比前一代更强',

    "f'the ratings climb, with the odd step back":
        '评分一路上升，偶尔退一步（{len(ae) - 1}步里有{ups}步是上升的）',

    "f'and {gap - mc1000:.0f} points above plain MCTS":
        '比每步一千次模拟的普通MCTS高出{gap - mc1000:.0f}分。',

    'and a little above plain MCTS with a thousand simulations a move.':
        '比每步一千次模拟的普通MCTS略高一点。',

    'though still below plain MCTS with a thousand simulations a move.':
        '不过仍然低于每步一千次模拟的普通MCTS。',

    'f"That is beyond the {100 * best_uct:.0f} percent plain MCTS reaches':
        '这超过了普通MCTS用多少次模拟都只能达到的{100 * best_uct:.0f}%：随机走子买不来一个学会的裁判所知道的东西。',

    "f'Plain MCTS, judging by random playouts, needs about {need:,} simulations":
        '靠随机走子来判断的普通MCTS，大约需要{need:,}次模拟才能做得一样好：由网络引导的每一次模拟，大约抵得上{need / SIMS:.0f}次随机模拟。',

}

PHRASES = {
    ', in every run: it never learns at all': '，而且每一次都是如此：它根本学不会',
    'climb to about that, and stay there': '爬升到这个值附近，然后稳定下来',
    'overshoot it, but stay within reach': '会超过它，但不会离得太远',
}
