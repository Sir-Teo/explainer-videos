# Chinese edition of *AI, Built* (人工智能，从零搭建)

Translations live in `videos/ai/aiN/narration_zh.json`, keyed by the English line; check them with
`python tools/translate_narration.py aiN --check`.

- Spoken Mandarin, short sentences; same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; numbers as digits (4.08 比特, 2260万); Latin letters stay Latin (p, q, H(p), KL, GPT-2).
- Spoken math: 以2为底的对数, p分之1, q减去p帽, 对所有x求和, 至多, 当且仅当.
- Model and product names stay as they are (GPT-2, Qwen3, gzip, xz, bzip2); book titles in 《》 with the English
  title on first mention where it helps (《傲慢与偏见》, 《马耳他之鹰》).
- On-screen text lives in `videos/ai/ai_text_zh.json` (exact `strings`, `phrases` inside `\text{}`, regex
  `patterns`); `python tools/collect_text.py --check aiN` lists what is still English, `--lang zh aiN` dry-runs the
  Chinese build. Text the models read or wrote (the passage, Shannon's sentence, generated samples, tokens) stays in
  English: it is data. Draw such words with `data_text(...)` (from `explainer.ai`), never `Text(...)`: a bare `Text` of a word that happens to be in the table ("yes", "noise", "next") would be translated.

## Glossary

| English | 中文 |
|---|---|
| Claude Shannon | 克劳德·香农 (香农) |
| the guessing game | 猜字游戏 |
| information theory | 信息论 |
| probability distribution | 概率分布 |
| conditional probability | 条件概率 |
| the chain rule | 链式法则 |
| context | 上下文 |
| surprise (surprisal) | 意外度（惊奇度） |
| bit / nat | 比特 / 奈特 |
| entropy | 熵 |
| conditional entropy | 条件熵 |
| redundancy | 冗余 |
| Jensen's inequality | 詹森不等式 |
| concave | 凹函数（向下弯） |
| code, codeword | 编码，码字 |
| fixed-length code | 定长编码 |
| prefix-free code | 无前缀码（前缀码） |
| Kraft's inequality | 克拉夫特不等式 |
| Huffman code | 霍夫曼编码 |
| source coding theorem | 信源编码定理 |
| cross-entropy | 交叉熵 |
| Kullback–Leibler divergence (KL) | KL散度（库尔巴克–莱布勒散度） |
| Gibbs' inequality | 吉布斯不等式 |
| mutual information | 互信息 |
| mode-covering / mode-seeking | 覆盖所有峰 / 只盯一个峰 |
| arithmetic coding | 算术编码 |
| compression, compressor | 压缩，压缩器 |
| counting model (n-gram) | 计数模型（n元模型） |
| smoothing (add-α) | 平滑（加α平滑） |
| overfitting, generalization | 过拟合，泛化 |
| maximum likelihood | 最大似然 |
| likelihood | 似然 |
| logit | logit（打分） |
| softmax | softmax |
| gradient, gradient descent | 梯度，梯度下降 |
| learning rate | 学习率 |
| loss | 损失 |
| token | 词元（token） |
| language model | 语言模型 |
| parameters | 参数 |
| scoreboard | 记分牌 |
| bits per character | 每字符比特数 |
| the passage | 测试段落 |
| power law | 幂律 |
| vector, cosine similarity | 向量，余弦相似度 |
| *The Maltese Falcon* | 《马耳他之鹰》 |
| Project Gutenberg | 古登堡计划 |

### Reinforcement learning (Part 26)

| English | 中文 |
|---|---|
| reinforcement learning | 强化学习 |
| agent, environment | 智能体，环境 |
| state, action, reward | 状态，动作，奖励 |
| return, discount (γ) | 回报，折扣（γ） |
| policy, value, action value (Q) | 策略，价值，动作价值（Q值） |
| Markov decision process | 马尔可夫决策过程 |
| multi-armed bandit, arm | 多臂老虎机，拉杆 |
| exploration, exploitation | 探索，利用 |
| greedy, ε-greedy | 贪心，ε-贪心 |
| regret | 遗憾 |
| upper confidence bound (UCB), bonus | 置信上界（UCB），加分 |
| Thompson sampling | 汤普森采样 |
| Hoeffding's inequality | 霍夫丁不等式 |
| Bellman equation, Bellman optimality equation | 贝尔曼方程，贝尔曼最优方程 |
| backup diagram | 回溯图 |
| value iteration, policy iteration | 值迭代，策略迭代 |
| generalized policy iteration | 广义策略迭代 |
| contraction, fixed point (Banach) | 压缩映射，不动点（巴拿赫） |
| gridworld, goal, pit | 网格世界，终点，陷阱 |
| Monte Carlo | 蒙特卡洛 |
| temporal difference (TD), TD error | 时序差分（TD），TD误差 |
| bootstrapping | 自举 |
| n-step return, eligibility trace | n步回报，资格迹 |
| credit assignment | 功劳分配 |
| Q-learning, Sarsa | Q学习，Sarsa |
| on-policy, off-policy | 同策略，离策略 |
| cliff walk | 悬崖行走 |
| function approximation, the deadly triad | 函数近似，致命三要素 |
| deep Q-network (DQN) | 深度Q网络（DQN） |
| experience replay, target network | 经验回放，目标网络 |
| maximization bias, double Q-learning | 最大化偏差，双Q学习 |
| cart-pole | 倒立摆 |
| policy gradient, REINFORCE | 策略梯度，REINFORCE |
| log-derivative trick | 对数导数技巧 |
| baseline, advantage | 基线，优势 |
| actor-critic, critic | 演员-评论家，评论家 |
| generalized advantage estimation (GAE) | 广义优势估计（GAE） |
| trust region (TRPO), importance ratio | 信赖域（TRPO），重要性比值 |
| proximal policy optimization (PPO), clipping | 近端策略优化（PPO），裁剪 |
| surrogate objective | 替代目标 |
| game tree, minimax, evaluation function | 博弈树，极小化极大，评估函数 |
| alpha-beta pruning | α-β剪枝 |
| Connect Four, column | 四子棋，列 |
| Monte Carlo tree search (MCTS), playout, simulation | 蒙特卡洛树搜索（MCTS），走子，模拟 |
| select, expand, simulate, back up | 选择，扩展，模拟，回溯 |
| prior (policy network), value network | 先验（策略网络），价值网络 |
| self-play, generation | 自我对弈，代 |
| perfect solver | 完美求解器 |
| representation, dynamics, prediction (MuZero) | 表示函数，动态函数，预测函数 |
| hidden state | 隐状态 |
| imperfect information, information set | 不完全信息，信息集 |
| Nash equilibrium, zero-sum | 纳什均衡，零和 |
| regret matching, counterfactual regret minimization (CFR) | 遗憾匹配，反事实遗憾最小化（CFR） |
| exploitability, bluffing | 可被利用度，诈唬 |
| Kuhn poker, Texas hold'em | 库恩扑克，德州扑克 |
| league (AlphaStar), exploiter | 联赛，剥削者 |
| shoulder hit, wedge (Go) | 肩冲，挖 |
| Lee Sedol, Fan Hui | 李世石，樊麾 |
| Sutton and Barto | 萨顿和巴托 |

Names of programs stay in Latin script: AlphaGo, AlphaZero, MuZero, TD-Gammon, Deep Blue → 深蓝, Stockfish, KataGo,
Libratus, Pluribus, Cepheus, AlphaStar, AlphaTensor, AlphaDev, Crazy Stone, MoGo, Agent57, Rainbow.

### Post-training and alignment (Part 27)

| English | 中文 |
|---|---|
| post-training, alignment | 后训练，对齐 |
| helpful, honest, harmless | 有用、诚实、无害 |
| supervised fine-tuning (SFT), instruction tuning | 监督微调（SFT），指令微调 |
| chat template, special token, loss masking | 聊天模板，特殊词元，损失屏蔽 |
| base model, fine-tuned model | 基础模型，微调后的模型 |
| forgetting | 遗忘 |
| low-rank adapter (LoRA), rank, task vector | 低秩适配器（LoRA），秩，任务向量 |
| intrinsic dimension | 内在维数 |
| reward model, comparison, preference | 奖励模型，比较，偏好 |
| Bradley–Terry model | 布拉德利-特里模型 |
| labeller | 标注员 |
| gold (the hidden true reward), proxy | 金标准，代理 |
| reinforcement learning from human feedback (RLHF) | 基于人类反馈的强化学习（RLHF） |
| reference model, the KL leash, β | 参考模型，KL绳子，β |
| best-of-n | 最优n选1 |
| over-optimization, reward hacking | 过度优化，奖励投机 |
| Goodhart's law | 古德哈特定律 |
| direct preference optimization (DPO) | 直接偏好优化（DPO） |
| likelihood displacement | 似然位移 |
| online / on-policy data | 在线数据，在线策略 |
| Constitutional AI, constitution, critique and revision | 宪法式AI，宪法，批评与修改 |
| RL from AI feedback (RLAIF), AI judge | 基于AI反馈的强化学习（RLAIF），AI裁判 |
| model spec, deliberative alignment | 模型规范，审慎对齐 |
| distillation, teacher, student, dark knowledge, temperature | 蒸馏，老师，学生，暗知识，温度 |
| forward KL, reverse KL | 前向KL，反向KL |
| model merging, model soup, linear mode connectivity | 模型合并，模型汤，线性模式连通 |
| sycophancy, jailbreak, many-shot jailbreaking, over-refusal | 谄媚，越狱，多样本越狱，过度拒绝 |
| emergent misalignment, alignment faking | 涌现式失准，对齐伪装 |

Method names stay in Latin script: InstructGPT, ChatGPT, FLAN, Alpaca, LIMA, QLoRA, DoRA, IPO, KTO, SimPO, GRPO,
TIES, DARE, MiniLLM, DistilBERT, Tülu 3, OLMo.
