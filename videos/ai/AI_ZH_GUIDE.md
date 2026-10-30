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

### Silicon (Part 17)

| English | 中文 |
|---|---|
| silicon, chip, die, wafer | 硅，芯片，裸片，晶圆 |
| transistor | 晶体管 |
| Moore's law | 摩尔定律 |
| Dennard scaling | 登纳德缩放 |
| the power wall | 功耗墙 |
| clock speed, frequency | 时钟频率 |
| leakage, threshold voltage | 漏电，阈值电压 |
| single-thread performance | 单线程性能 |
| core, multicore | 核心，多核 |
| Amdahl's law | 阿姆达尔定律 |
| GPU (graphics processing unit) | GPU（图形处理器） |
| shader | 着色器 |
| GPGPU (general-purpose computing on GPUs) | GPGPU（GPU通用计算） |
| CUDA, kernel | CUDA，内核（核函数） |
| thread, thread block, grid | 线程，线程块，网格 |
| warp | 线程束 |
| SIMT (single instruction, multiple threads) | SIMT（单指令多线程） |
| streaming multiprocessor (SM) | 流式多处理器（SM） |
| lane | 通道 |
| branch divergence | 分支发散 |
| latency hiding | 延迟隐藏 |
| Little's law | 利特尔定律 |
| bytes in flight | 在途字节 |
| memory coalescing | 访存合并 |
| occupancy | 占用率 |
| register, register file | 寄存器，寄存器堆 |
| shared memory | 共享内存 |
| cache, cache line, L1 / L2 / L3 | 缓存，缓存行，一级/二级/三级缓存 |
| SRAM, DRAM, HBM (high-bandwidth memory) | SRAM，DRAM，HBM（高带宽内存） |
| memory hierarchy | 存储层次 |
| bandwidth, latency | 带宽，延迟 |
| pointer chasing | 指针追逐 |
| prefetcher | 预取器 |
| huge pages, TLB | 大页，TLB（地址转换缓存） |
| matrix multiplication (GEMM), matrix-vector product (GEMV) | 矩阵乘法（GEMM），矩阵乘向量（GEMV） |
| FLOP, FLOP/s | 浮点运算次数，每秒浮点运算次数 |
| arithmetic intensity | 算术强度 |
| tiling, cache blocking, tile | 分块，缓存分块，块（瓦片） |
| BLAS | BLAS（基础线性代数库） |
| the roofline model, ridge point | 屋顶线模型，拐点 |
| compute-bound, memory-bound | 受算力限制，受内存限制 |
| STREAM triad | STREAM三元组测试 |
| systolic array, processing element (PE) | 脉动阵列，处理单元 |
| output-stationary, weight-stationary | 输出驻留，权重驻留 |
| wavefront | 波前 |
| TPU (Tensor Processing Unit) | TPU（张量处理器） |
| tensor core | 张量核心 |
| multiply-accumulate (MAC), fused multiply-add (FMA) | 乘加 |
| floating point: sign, exponent, mantissa, bias | 浮点数：符号位，指数，尾数，偏置 |
| unit roundoff, round to nearest | 单位舍入误差，就近舍入 |
| subnormal, saturate | 次正规数，饱和 |
| FP32, TF32, BF16 (bfloat16), FP16, FP8, FP4 | FP32，TF32，BF16，FP16，FP8，FP4 |
| microscaling (MX), block scale, shared exponent | 微缩放（MX），块缩放因子，共享指数 |
| interconnect, link | 互连，链路 |
| NVLink, NVSwitch, InfiniBand | NVLink，NVSwitch，InfiniBand |
| scale-up, scale-out | 纵向扩展，横向扩展 |
| topology: switch, fat tree, torus | 拓扑：交换机，胖树，环面 |
| optical circuit switch | 光路交换机 |
| collective, all-reduce, reduce-scatter, all-gather, broadcast | 集合通信，全规约，规约-分散，全收集，广播 |
| ring all-reduce, tree all-reduce | 环形全规约，树形全规约 |
| the α–β model (latency–bandwidth) | α–β模型（延迟–带宽模型） |
| Triton, CUTLASS | Triton，CUTLASS |
| FlashAttention, IO-aware | FlashAttention，IO感知 |
| price-performance, energy efficiency | 性价比，能效 |
| the memory wall | 内存墙 |
| data centre, AI factory | 数据中心，AI工厂 |
| rack, pod, superpod | 机柜，集群（pod），超级集群 |
| wafer-scale engine | 晶圆级引擎 |
| LPU | LPU（语言处理单元） |
| through-silicon via (TSV), silicon interposer | 硅通孔，硅中介层 |
| prefill, decode | 预填充，解码 |
| skew (of a systolic array) | （脉动阵列的）错位 |
| inference | 推断 |
| multi-thread, single-thread | 多线程，单线程 |
| load average | 平均负载 |
| analog in-memory computing, phase-change memory | 模拟存内计算，相变存储器 |
| neuromorphic computing, spiking neuron | 类脑计算，脉冲神经元 |
| the hardware lottery | 硬件彩票 |

Names: Gordon Moore → 戈登·摩尔; Robert Dennard → 罗伯特·登纳德; H. T. Kung → 孔祥重; Charles Leiserson → 查尔斯·雷瑟尔森;
Hong Jia-Wei → 洪加威; Ian Buck → 伊恩·巴克; John Nickolls → 约翰·尼科尔斯; Alex Krizhevsky → 亚历克斯·克里热夫斯基; Ilya
Sutskever → 伊利亚·苏茨克维; Geoffrey Hinton → 杰弗里·辛顿; Fei-Fei Li → 李飞飞; Jensen Huang → 黄仁勋; Sara Hooker → 萨拉·胡克;
Samuel Williams, Andrew Waterman, David Patterson → 塞缪尔·威廉斯、安德鲁·沃特曼、大卫·帕特森; Philippe Tillet → 菲利普·蒂莱;
Tri Dao → Tri Dao; Vasily Volkov → 瓦西里·沃尔科夫; Herb Sutter → 赫伯·萨特; Gene Amdahl → 吉恩·阿姆达尔; John Little →
约翰·利特尔; Mark Horowitz → 马克·霍洛维茨; William Kahan → 威廉·卡亨; Jonathan Ross → 乔纳森·罗斯. Products stay in Latin script
(GeForce, CUDA, H100, Blackwell, Rubin, NVLink, TPU, Ironwood, Trainium, Cerebras, Groq, TrueNorth, Loihi, Hala Point).

### The symbolic era (Part 2)

| English | 中文 |
|---|---|
| Turing machine, tape, head, state | 图灵机，纸带，读写头，状态 |
| universal machine, stored-program computer | 通用机，存储程序计算机 |
| halting problem, decidable / undecidable | 停机问题，可判定 / 不可判定 |
| busy beaver | 忙碌海狸 |
| imitation game, Turing test, interrogator | 模仿游戏，图灵测试，提问者 |
| Dartmouth workshop | 达特茅斯会议 |
| Logic Theorist | 逻辑理论家 |
| physical symbol system hypothesis | 物理符号系统假设 |
| search problem, state space, goal test | 搜索问题，状态空间，目标测试 |
| breadth-first / depth-first search, iterative deepening | 广度优先 / 深度优先搜索，迭代加深 |
| uniform-cost search, Dijkstra's algorithm | 一致代价搜索，迪杰斯特拉算法 |
| frontier, wavefront, expand | 边界，波前，扩展 |
| heuristic, A\*, f = g + h | 启发式（启发函数），A\*，f = g + h |
| admissible, consistent (monotone) | 可采纳的，一致的（单调的） |
| weighted A\*, greedy best-first search | 加权A\*，贪心最佳优先搜索 |
| relaxed problem, Manhattan distance, misplaced tiles | 松弛问题，曼哈顿距离，错位方块数 |
| dominance, effective branching factor | 占优，有效分支因子 |
| 8-puzzle, 15-puzzle | 八数码，十五数码 |
| IDA\*, pattern database | IDA\*，模式数据库 |
| local search, hill climbing, local maximum, plateau | 局部搜索，爬山法，局部极大值，平台 |
| random restart, sideways move | 随机重启，横向移动 |
| simulated annealing, temperature, cooling schedule | 模拟退火，温度，降温计划 |
| Metropolis rule, detailed balance, Boltzmann distribution | 梅特罗波利斯准则，细致平衡，玻尔兹曼分布 |
| travelling salesman problem, tour, 2-opt | 旅行商问题，回路，2-opt |
| genetic algorithm, population, crossover, mutation | 遗传算法，种群，交叉，变异 |
| alpha–beta window [α, β], cutoff, move ordering | α-β窗口 [α, β]，剪枝，走法排序 |
| scoring polynomial (Samuel) | 评分多项式（塞缪尔） |
| propositional / first-order logic, entailment | 命题 / 一阶逻辑，蕴涵 |
| clause, literal, resolution, resolvent, refutation | 子句，文字，归结，归结式，反驳 |
| unification, substitution | 合一，代换 |
| set of support, Horn clause, Prolog | 支持集策略，霍恩子句，Prolog |
| satisfiability (SAT), NP-complete | 可满足性（SAT），NP完全 |
| DPLL, unit propagation, branching, backtracking | DPLL，单元传播，分支，回溯 |
| conflict-driven clause learning (CDCL), implication graph | 冲突驱动子句学习（CDCL），蕴含图 |
| first UIP, learned clause, backjumping | 第一唯一蕴含点，学习子句，回跳 |
| phase transition, clause-to-variable ratio | 相变，子句与变量之比 |
| constraint satisfaction problem, domain | 约束满足问题，值域 |
| arc consistency (AC-3), forward checking | 弧相容（AC-3），前向检查 |
| minimum remaining values (MRV), MAC | 最少剩余值（MRV），维持弧相容（MAC） |
| planning, STRIPS, precondition, add list, delete list | 规划，STRIPS，前提条件，添加表，删除表 |
| the frame problem, the Sussman anomaly | 框架问题，萨斯曼异常 |
| relaxed-plan heuristic (h_max, h_FF) | 松弛规划启发式（h_max，h_FF） |
| semantic network, is-a link, inheritance, frame, slot | 语义网络，is-a链接，继承，框架，槽 |
| expert system, rule base, forward chaining | 专家系统，规则库，前向链接 |
| certainty factor | 确定性因子 |
| knowledge engineer, knowledge acquisition bottleneck | 知识工程师，知识获取瓶颈 |
| knowledge graph | 知识图谱 |
| ELIZA, keyword, decomposition, reassembly, the ELIZA effect | ELIZA，关键词，分解规则，重组规则，伊丽莎效应 |
| AI winter, Lighthill report, Lisp machine | AI寒冬，莱特希尔报告，Lisp机 |
| Fifth Generation Computer Systems project | 第五代计算机项目 |
| Moravec's paradox, the long tail | 莫拉维克悖论，长尾 |
| formal verification, SMT, adder, multiplier, miter | 形式化验证，SMT，加法器，乘法器，比较电路（miter） |
| proof assistant (Lean) | 证明助手（Lean） |
| neurosymbolic AI | 神经符号AI |

Names: Alan Turing 图灵; Alonzo Church 丘奇; John McCarthy 麦卡锡; Marvin Minsky 明斯基; Herbert Simon 西蒙; Allen
Newell 纽厄尔; Edsger Dijkstra 迪杰斯特拉; Arthur Samuel 塞缪尔; Garry Kasparov 卡斯帕罗夫; Joseph Weizenbaum 魏岑鲍姆;
James Lighthill 莱特希尔; Hans Moravec 莫拉维克; Judea Pearl 珀尔; Richard Korf 科尔夫; Alan Robinson 鲁滨逊; Stephen Cook
库克; Leonid Levin 列文. Program names stay in Latin script: Shakey, STRIPS, DENDRAL, MYCIN, XCON, Cyc, ELIZA, DOCTOR,
Chinook, Deep Blue → 深蓝, Prolog, Lisp, Z3, Lean, AlphaProof, AlphaGeometry, FunSearch, AlphaEvolve, DeepCubeA.

### Reasoning (Part 28)

| English | 中文 |
|---|---|
| reasoning, reasoning model | 推理，推理模型 |
| chain of thought, scratchpad | 思维链，草稿（中间步骤） |
| "let's think step by step" | "让我们一步一步地思考" |
| thinking out loud, tokens of thought | 出声思考，思考词元 |
| filler tokens | 填充词元 |
| threshold circuit, TC⁰, NC¹ | 阈值电路，TC⁰，NC¹ |
| self-consistency, majority vote | 自洽性，多数投票 |
| verifier, checker | 验证器，检查器 |
| outcome reward model (ORM) | 结果奖励模型（ORM） |
| process reward model (PRM) | 过程奖励模型（PRM） |
| step label, right for the wrong reason | 步骤标签，歪打正着 |
| AUC (how well a grader tells right from wrong) | AUC（评分器区分对错的能力） |
| reinforcement learning with verifiable rewards (RLVR) | 可验证奖励的强化学习（RLVR） |
| group relative policy optimization (GRPO) | 组相对策略优化（GRPO） |
| group, group baseline, leave-one-out | 组，组基线，留一 |
| importance ratio, clip, clip-higher | 重要性比值，裁剪，放宽上界的裁剪（clip-higher） |
| KL estimator (k1, k2, k3), control variate | KL估计量（k1、k2、k3），控制变量 |
| length bias, difficulty bias | 长度偏差，难度偏差 |
| dynamic sampling, groups with no signal | 动态采样，没有信号的组 |
| sequence-level ratio, geometric mean | 序列级比值，几何平均 |
| entropy collapse, entropy bonus | 熵坍缩，熵奖励 |
| overthinking, underthinking, length penalty | 过度思考，思考不足，长度惩罚 |
| aha moment | 顿悟时刻（aha moment） |
| pass@k, unbiased estimator, plug-in estimator | pass@k，无偏估计量，代入估计量 |
| sharpen, widen (the reasoning boundary) | 锐化，拓宽（推理边界） |
| test-time compute, parallel, sequential | 测试时计算，并行，串行 |
| budget forcing | 预算强制 |
| best-of-N | 最优N选1 |
| beam search, tree search, Tree of Thoughts | 束搜索，树搜索，思维树 |
| latent reasoning, continuous thought | 隐式推理，连续思维 |
| recursion, deep supervision, refinement loop | 递归，深度监督，精炼循环 |
| proof assistant, kernel, formalization | 证明助手，内核，形式化 |
| harness (for ARC-AGI-3) | 测试框架（harness） |
| chain-of-thought monitorability | 思维链的可监控性 |

Names stay in Latin script: GRPO, Dr. GRPO, DAPO, GSPO, CISPO, DPO, o1, o3, R1, R1-Zero, s1, L1, Kimi k1.5, ProRL,
rStar-Math, Coconut, HRM, TRM, AlphaProof, AlphaGeometry, Lean, Mathlib, Aristotle, Seed-Prover, ARC-AGI, NVARC, Poetiq.

### The language-model lineage (Part 14)

| English | 中文 |
|---|---|
| pretraining, fine-tuning | 预训练，微调 |
| encoder-only, decoder-only, encoder–decoder | 仅编码器，仅解码器，编码器-解码器 |
| causal (left-to-right) language model | 因果（从左到右）语言模型 |
| masked language model (MLM), [MASK] token | 掩码语言模型（MLM），[MASK]词元 |
| next-sentence prediction | 下一句预测 |
| self-attention, masked self-attention, cross-attention | 自注意力，带掩码的自注意力，交叉注意力 |
| BLEU | BLEU |
| benchmark, leaderboard | 基准，排行榜 |
| text-to-text, task prefix | 文本到文本，任务前缀 |
| span corruption, sentinel token | 片段破坏，哨兵词元 |
| zero-shot, one-shot, few-shot | 零样本，单样本，少样本 |
| in-context learning | 上下文学习 |
| scaling law | 规模定律 |
| compute-optimal, over-training | 计算最优，过度训练 |
| tokens per parameter | 每个参数的词元数 |
| petaflop/s-day | petaflop/s-天 |
| instruction tuning, held-out task | 指令微调，留出的任务 |
| staged release, model card, system card | 分阶段发布，模型卡，系统卡 |
| open weights, closed model | 开放权重，闭源模型 |
| pre-norm, post-norm, RMSNorm | 前置归一化，后置归一化，RMSNorm |
| SwiGLU, gate | SwiGLU，门控 |
| rotary position embedding (RoPE) | 旋转位置编码（RoPE） |
| multi-query, grouped-query attention (GQA) | 多查询注意力，分组查询注意力（GQA） |
| multi-head latent attention (MLA) | 多头潜在注意力（MLA） |
| KV cache | KV缓存 |
| mixture of experts, active parameters | 混合专家，激活参数 |
| sparse attention, linear attention, hybrid | 稀疏注意力，线性注意力，混合架构 |
| cloze test | 完形填空测试 |
| linear probe | 线性探针 |
| induction head, repeated-list test | 归纳头，重复列表测试 |
| equal compute | 同等算力 |
| lineage, family tree | 谱系，家族树 |
| calibration (content-free input) | 校准（无内容输入） |

### Networks (Part 9)

| English | 中文 |
|---|---|
| artificial neuron, unit | 人工神经元，单元 |
| McCulloch–Pitts unit, threshold | 麦卡洛克–皮茨单元，阈值 |
| Hebb's rule | 赫布规则 |
| perceptron, Mark I Perceptron | 感知机，Mark I感知机 |
| association unit, response unit | 联想单元，响应单元 |
| ADALINE, least mean squares (LMS) | ADALINE，最小均方 |
| margin, convergence theorem | 间隔，收敛定理 |
| linearly separable | 线性可分 |
| XOR, parity, connectedness | 异或，奇偶性，连通性 |
| hidden layer, hidden unit | 隐藏层，隐藏单元 |
| backpropagation, delta (δ) | 反向传播，delta（δ） |
| forward pass, backward pass | 前向传播，反向传播 |
| finite differences | 有限差分 |
| reverse-mode automatic differentiation | 自动微分的反向模式 |
| universal approximation theorem | 万能近似定理 |
| hinge, bump | 铰链，鼓包 |
| rectified linear unit (ReLU) | 线性整流单元（ReLU） |
| curse of dimensionality | 维数灾难 |
| Barron's bound | 巴伦界 |
| linear region (piece) | 线性区域（小块） |
| depth separation | 深度分离 |
| folding | 折叠 |
| vanishing / exploding gradients | 梯度消失 / 梯度爆炸 |
| deep belief net, greedy layer-wise pretraining | 深度信念网络，逐层贪心预训练 |
| initialization (Glorot / Xavier, He) | 初始化（格洛罗初始化，何恺明初始化） |
| mean-field theory | 平均场理论 |
| length map, correlation map | 长度映射，相关映射 |
| ordered phase, chaotic phase, edge of chaos | 有序相，混沌相，混沌的边缘 |
| depth scale (ξ) | 深度尺度（ξ） |
| residual connection, residual stream | 残差连接，残差流 |
| highway network | 高速公路网络 |
| batch normalization, layer normalization, RMSNorm | 批归一化，层归一化，RMSNorm |
| pre-norm, post-norm, warm-up | 前置归一化，后置归一化，预热 |
| internal covariate shift | 内部协变量偏移 |
| Jacobian, singular value | 雅可比矩阵，奇异值 |
| GELU, SiLU (Swish) | GELU，SiLU（Swish） |
| gating, gated linear unit (GLU), SwiGLU | 门控，门控线性单元（GLU），SwiGLU |
| feed-forward network (MLP) | 前馈网络（MLP） |
| Kolmogorov–Arnold representation theorem | 柯尔莫哥洛夫–阿诺德表示定理 |
| Kolmogorov–Arnold network (KAN), spline | 柯尔莫哥洛夫–阿诺德网络（KAN），样条 |
| neural language model, embedding | 神经语言模型，嵌入 |
| Hilbert's thirteenth problem | 希尔伯特第13问题 |

### Evaluation and safety (Part 31)

| English | 中文 |
|---|---|
| the bootstrap, resample | 自助法，重抽样（统计；不同于强化学习里的"自举"） |
| confidence interval, standard error | 置信区间，标准误 |
| paired comparison, unpaired | 配对比较，不配对 |
| benchmark, held-out test | 基准测试，留出的测试集 |
| contamination, leak | 污染，泄漏 |
| n-gram overlap | n元组重叠 |
| canary string | 金丝雀字符串 |
| dynamic benchmark | 动态基准测试 |
| arena, leaderboard, vote | 竞技场，排行榜，投票 |
| Elo rating, online Elo | 埃洛等级分，在线埃洛 |
| style control | 风格控制 |
| LLM as a judge; position, verbosity and self-preference bias | 用大模型当裁判；位置偏差、冗长偏差、自我偏好 |
| item response theory (IRT), 2PL, difficulty, discrimination | 项目反应理论（IRT），双参数模型，难度，区分度 |
| Fisher information | 费希尔信息 |
| time horizon (50%) | （百分之五十）时间跨度 |
| doubling time, backtest, extrapolation | 倍增时间，回测，外推 |
| specification gaming, reward hacking | 规格投机，奖励投机 |
| potential-based shaping | 基于势函数的奖励塑形 |
| scalable oversight, debate | 可扩展监督，辩论 |
| weak-to-strong generalization, performance gap recovered (PGR) | 由弱到强的泛化，性能差距恢复率（PGR） |
| auxiliary confidence loss | 辅助置信度损失 |
| deception, scheming, sandbagging | 欺骗，图谋，藏拙 |
| sleeper agent, probe | 潜伏特工，探针 |
| evaluation awareness | 评测意识 |
| chain-of-thought monitoring, monitorability, obfuscation | 思维链监控，可监控性，混淆 |
| AI control; red team, blue team; trusted and untrusted model | AI控制；红队，蓝队；可信模型与不可信模型 |
| audit budget, trusted monitoring, defer to trusted | 审计预算，可信监控，转交可信模型 |
| safety, usefulness | 安全性，有用性 |
| frontier safety framework, capability threshold | 前沿安全框架，能力阈值 |
| safeguard, classifier, adaptive attack | 防护措施，分类器，自适应攻击 |
| memorization, extraction, membership inference | 记忆，提取，成员推断 |
| differential privacy, ε, DP-SGD, clipping, accountant | 差分隐私，ε，DP-SGD，裁剪，隐私会计 |
| exposure | 暴露度 |

### Four ways to generate (Part 20)

| English | 中文 |
|---|---|
| generative model | 生成模型 |
| sample, evaluate, encode | 采样，计算（概率），编码 |
| density estimation | 密度估计 |
| differential entropy, the floor h(p) | 微分熵，下限h(p) |
| two moons, ring of eight Gaussians, checkerboard | 双月，八个高斯组成的环（八峰环），棋盘格 |
| autoregressive model | 自回归模型 |
| mixture density network (mixture of Gaussians) | 混合密度网络（高斯混合） |
| NADE, MADE | NADE，MADE |
| PixelCNN, PixelRNN, WaveNet | PixelCNN，PixelRNN，WaveNet |
| masked convolution, mask A / mask B | 掩码卷积，A型掩码 / B型掩码 |
| receptive field, blind spot | 感受野，盲区 |
| vertical stack, horizontal stack | 竖直栈，水平栈 |
| bits per pixel | 每像素比特数 |
| latent variable, code z | 隐变量，编码z |
| prior, posterior | 先验，后验 |
| Helmholtz machine, recognition model | 亥姆霍兹机，识别模型 |
| wake–sleep algorithm | 醒-睡算法 |
| amortized inference | 摊销推断 |
| variational autoencoder (VAE) | 变分自编码器（VAE） |
| encoder, decoder | 编码器，解码器 |
| evidence lower bound (ELBO) | 证据下界（ELBO） |
| reparameterization trick | 重参数化技巧 |
| reconstruction term | 重建项 |
| rate, distortion, rate–distortion trade-off | 码率，失真，码率-失真权衡 |
| importance-weighted bound (IWAE) | 重要性加权下界（IWAE） |
| discretized logistic | 离散化逻辑斯谛分布 |
| active units | 活跃单元 |
| β-VAE, disentanglement | β-VAE，解耦 |
| posterior collapse | 后验坍缩 |
| free bits, KL annealing | 自由比特，KL退火 |
| generative adversarial network (GAN) | 生成对抗网络（GAN） |
| generator, discriminator | 生成器，判别器 |
| minimax game, value function | 极小极大博弈，值函数 |
| optimal discriminator | 最优判别器 |
| Jensen–Shannon divergence | 詹森-香农散度（JS散度） |
| saturating / non-saturating loss | 饱和损失 / 非饱和损失 |
| reverse KL | 反向KL散度 |
| mode (a peak of a distribution), modes covered | 峰，覆盖的峰 |
| mode collapse, mode dropping | 模式坍缩，模式丢失 |
| simultaneous / alternating gradient steps | 同时梯度步 / 交替梯度步 |
| extragradient, optimistic gradient descent | 外梯度法，乐观梯度下降 |
| Dirac-GAN, R1 penalty | 狄拉克GAN，R1惩罚 |
| two time-scale update rule (TTUR) | 双时间尺度更新规则（TTUR） |
| spectral normalization | 谱归一化 |
| Wasserstein distance, earth mover's distance | 瓦瑟斯坦距离，推土机距离 |
| transport plan, coupling | 运输方案，耦合 |
| Kantorovich–Rubinstein duality | 康托罗维奇–鲁宾斯坦对偶 |
| 1-Lipschitz, critic | 1-利普希茨，评论家 |
| weight clipping, gradient penalty (WGAN-GP) | 权重截断，梯度惩罚（WGAN-GP） |
| DCGAN, progressive growing, BigGAN | DCGAN，渐进式增长，BigGAN |
| StyleGAN, mapping network, style, style mixing | StyleGAN，映射网络，风格，风格混合 |
| truncation trick | 截断技巧 |
| GAN inversion | GAN反演 |
| normalizing flow | 归一化流 |
| change of variables | 变量替换 |
| Jacobian determinant, log-determinant | 雅可比行列式，对数行列式 |
| coupling layer (affine), NICE, RealNVP, Glow | （仿射）耦合层，NICE，RealNVP，Glow |
| dequantization, logit transform | 去量化，logit变换 |
| temperature (sampling) | （采样）温度 |
| neural ODE, continuous normalizing flow | 神经ODE，连续归一化流 |
| instantaneous change of variables, divergence | 瞬时变量替换，散度 |
| trace, Hutchinson's estimator | 迹，哈钦森估计量 |
| Rademacher probe | 拉德马赫探针（随机正负号探针） |
| FFJORD | FFJORD |
| energy-based model, energy E | 能量模型（基于能量的模型），能量E |
| partition function (normalizer) Z | 配分函数（归一化常数）Z |
| Hopfield network, associative memory | 霍普菲尔德网络，联想记忆 |
| content-addressable memory | 按内容寻址的记忆 |
| capacity, spin glass, mixture state | 容量，自旋玻璃，混合态 |
| modern (dense) Hopfield network | 现代（稠密）霍普菲尔德网络 |
| Boltzmann machine, hidden / visible units | 玻尔兹曼机，隐藏 / 可见单元 |
| positive phase, negative phase | 正相，负相 |
| restricted Boltzmann machine (RBM), harmonium | 受限玻尔兹曼机（RBM），harmonium |
| free energy | 自由能 |
| Gibbs sampling | 吉布斯采样 |
| contrastive divergence (CD-k), persistent CD | 对比散度（CD-k），持续对比散度（PCD） |
| filters (of an RBM) | （RBM的）滤波器 |
| Langevin dynamics | 朗之万动力学 |
| score (function) | 分数函数 |
| replay buffer (of chains) | （链的）回放池 |
| annealed Langevin dynamics, noise levels | 退火朗之万动力学，噪声水平 |
| score matching, denoising score matching | 分数匹配，去噪分数匹配 |
| Equilibrium Matching | 均衡匹配 |
| Fréchet Inception Distance (FID) | 弗雷歇Inception距离（FID） |
| Fréchet distance, 2-Wasserstein distance | 弗雷歇距离，2-瓦瑟斯坦距离 |
| Inception Score | Inception分数 |
| features (of a classifier) | （分类器的）特征 |
| precision, recall (for generators) | 精确率，召回率（生成模型的） |
| memorization, nearest neighbour | 死记硬背（记忆），最近邻 |
| generative trilemma | 生成学习三难困境 |
| tokenizer, codebook, token | 分词器，码本，词元 |
| vector quantization (VQ-VAE), straight-through estimator | 向量量化（VQ-VAE），直通估计器 |
| perplexity (of a codebook) | （码本的）困惑度 |
| VQGAN, two-stage model | VQGAN，两阶段模型 |
| next-scale prediction (VAR) | 下一尺度预测（VAR） |
| distillation, adversarial diffusion distillation | 蒸馏，对抗扩散蒸馏 |
| consistency model | 一致性模型 |
| drifting model | 漂移模型 |

### Pretraining at scale (Part 18)

| English | 中文 |
|---|---|
| pretraining run, frontier run | 预训练，前沿训练 |
| Common Crawl, WARC, WET | Common Crawl，WARC，WET |
| text extraction, boilerplate | 文本抽取，模板噪声（样板文字） |
| language identification | 语言识别 |
| URL blocklist | URL黑名单 |
| deduplication, exact / near-duplicate | 去重，完全重复 / 近似重复 |
| shingle (word n-gram) | 片段（词n元组） |
| Jaccard similarity | 杰卡德相似度 |
| MinHash, signature | 最小哈希（MinHash），签名 |
| locality-sensitive hashing (LSH), band, bucket | 局部敏感哈希（LSH），带，桶 |
| quality classifier, annotator | 质量分类器，标注模型 |
| educational value | 教育价值 |
| contamination, n-gram overlap | 数据污染，n元组重叠 |
| data mixture, domain weights, proxy model | 数据配比，领域权重，代理模型 |
| synthetic data, rephrasing | 合成数据，改写 |
| model collapse | 模型崩溃 |
| epoch, repetition, effective data | 轮次，重复，有效数据 |
| causal LM, masked LM, span corruption | 因果语言模型，掩码语言模型，片段破坏 |
| fill in the middle (FIM), prefix / suffix / middle | 中间填充（FIM），前缀 / 后缀 / 中间 |
| warmup–stable–decay (WSD), cooldown | 预热–稳定–衰减（WSD），冷却 |
| annealing, mid-training, microanneal | 退火，中期训练，微退火 |
| long-context extension, RoPE base (ABF) | 长上下文扩展，RoPE基频（ABF） |
| mixed precision, master weights | 混合精度，主权重 |
| activation memory, activation recomputation (checkpointing) | 激活内存，激活重计算 |
| data parallelism | 数据并行 |
| bandwidth-optimal, lower bound | 带宽最优，下界 |
| ZeRO (stages 1–3), sharding | ZeRO（第1–3阶段），分片 |
| FSDP (fully sharded data parallel) | FSDP（全分片数据并行） |
| tensor parallelism, column / row split | 张量并行，按列 / 按行切分 |
| sequence parallelism | 序列并行 |
| pipeline parallelism, stage, micro-batch | 流水线并行，阶段，微批次 |
| pipeline bubble, 1F1B, interleaved schedule | 流水线气泡，1F1B，交错调度 |
| zero bubble, DualPipe | 零气泡，DualPipe |
| context parallelism, ring attention | 上下文并行，环形注意力 |
| expert parallelism, all-to-all | 专家并行，全对全通信 |
| online softmax | 在线softmax |
| model FLOPs utilization (MFU) | 模型浮点利用率（MFU） |
| loss scaling, dynamic loss scaling, overflow, underflow | 损失缩放，动态损失缩放，上溢，下溢 |
| gradient accumulation | 梯度累积 |
| fine-grained (tile-wise, block-wise) scaling, microscaling (MX) | 细粒度（按块、按瓦片）缩放，微缩放（MX） |
| quantization-aware training (QAT) | 量化感知训练（QAT） |
| loss spike, rollback | 损失尖峰，回滚 |
| attention logit growth, QK-norm | 注意力logit增长，QK归一化 |
| z-loss, log-partition (log Z) | z-loss，对数配分（log Z） |
| QK-Clip, MuonClip | QK-Clip，MuonClip |
| multi-token prediction (MTP), acceptance rate | 多词元预测（MTP），接受率 |
| self-speculative decoding, draft | 自推测解码，草稿 |
| fault tolerance, interruption, MTBF | 容错，中断，平均故障间隔 |
| checkpoint, checkpoint interval (Young's rule) | 检查点，检查点间隔（Young法则） |
| goodput | 有效吞吐 |
| recipe | 配方 |

### Seeing and remembering (Part 10)

| English | 中文 |
|---|---|
| computer vision | 计算机视觉 |
| visual cortex, receptive field (of a neuron) | 视觉皮层，（神经元的）感受野 |
| simple cell, complex cell | 简单细胞，复杂细胞 |
| orientation selectivity, tuning curve, grating | 方向选择性，调谐曲线，光栅 |
| colour-opponent cell | 颜色拮抗细胞 |
| edge, image gradient, Sobel operator | 边缘，图像梯度，索贝尔算子 |
| feature descriptor: SIFT, HOG (histogram of oriented gradients) | 特征描述子：SIFT，HOG（方向梯度直方图） |
| keypoint, cell, block normalization | 关键点，单元格，块归一化 |
| hand-made (hand-designed) features, pipeline | 手工设计的特征，流水线 |
| Fisher vector, bag of visual words | 费舍尔向量，视觉词袋 |
| convolution, cross-correlation, kernel (filter) | 卷积，互相关，卷积核（滤波器） |
| feature map, channel | 特征图，通道 |
| weight sharing, locally connected | 权值共享，局部连接 |
| translation equivariance, translation invariance | 平移等变，平移不变 |
| circular padding, zero padding | 循环填充，零填充 |
| receptive field (of a unit), effective receptive field | （单元的）感受野，有效感受野 |
| stride, jump (spacing), pooling, max pooling | 步长，跳距，池化，最大池化 |
| anti-aliasing, blur pooling | 抗混叠，模糊池化 |
| the Neocognitron, S-cells, C-cells | 新认知机，S细胞，C细胞 |
| LeNet, MNIST | LeNet，MNIST |
| zip code, check reader | 邮政编码，支票识别系统 |
| time-delay neural network (TDNN) | 时延神经网络（TDNN） |
| ImageNet, ILSVRC, top-5 error | ImageNet，ILSVRC（ImageNet大规模视觉识别挑战赛），前五错误率 |
| WordNet, Amazon Mechanical Turk | WordNet，亚马逊土耳其机器人（众包平台） |
| AlexNet (SuperVision), CIFAR-10 | AlexNet（SuperVision），CIFAR-10 |
| rectified linear unit (ReLU), saturation | 修正线性单元（ReLU），饱和 |
| dropout | 随机失活（dropout） |
| data augmentation, random crop, flip | 数据增强，随机裁剪，翻转 |
| VGG, GoogLeNet, Inception module, 1 × 1 convolution | VGG，GoogLeNet，Inception模块，1 × 1卷积 |
| degradation problem | 退化问题 |
| batch normalization | 批归一化 |
| residual network (ResNet), highway network | 残差网络（ResNet），高速公路网络 |
| activation maximization, saliency map, feature visualization | 激活最大化，显著图，特征可视化 |
| adversarial example, perturbation, transferability | 对抗样本，扰动，可迁移性 |
| fast gradient sign method (FGSM), projected gradient descent (PGD) | 快速梯度符号法（FGSM），投影梯度下降（PGD） |
| adversarial training, robustness, certified defence | 对抗训练，鲁棒性，可认证防御 |
| depthwise convolution, pointwise convolution, depthwise separable | 深度卷积，逐点卷积，深度可分离 |
| MobileNet, ConvNeXt, vision transformer (ViT), Swin | MobileNet，ConvNeXt，视觉Transformer（ViT），Swin |
| dilated (atrous) convolution | 空洞卷积（膨胀卷积） |
| recurrent neural network (RNN), hidden state | 循环神经网络（RNN），隐状态 |
| backpropagation through time (BPTT), truncated BPTT | 随时间反向传播（BPTT），截断的BPTT |
| vanishing gradient, exploding gradient | 梯度消失，梯度爆炸 |
| Jacobian, spectral radius, largest singular value | 雅可比矩阵，谱半径，最大奇异值 |
| gradient clipping, cliff | 梯度裁剪，悬崖 |
| long short-term memory (LSTM), cell state, constant error carousel | 长短期记忆（LSTM），细胞状态，恒定误差传送带 |
| input gate, forget gate, output gate | 输入门，遗忘门，输出门 |
| gated recurrent unit (GRU), update gate, reset gate | 门控循环单元（GRU），更新门，重置门 |
| half-life (of a memory) | （记忆的）半衰期 |
| chrono initialization | 时序初始化 |
| character-level language model, char-rnn | 字符级语言模型，char-rnn |
| sequence to sequence (seq2seq), encoder, decoder | 序列到序列（seq2seq），编码器，解码器 |
| machine translation, phrase-based, BLEU | 机器翻译，基于短语的，BLEU |
| teacher forcing, exposure bias, scheduled sampling | 教师强制，暴露偏差，计划采样 |
| greedy decoding, beam search, beam width | 贪心解码，束搜索，束宽 |
| neural text degeneration | 神经文本退化 |
| bottleneck | 瓶颈 |
| attention, alignment, context vector, additive score | 注意力，对齐，上下文向量，加性打分 |
| query, key, value | 查询，键，值 |
| neural Turing machine, memory network | 神经图灵机，记忆网络 |
| linear recurrence, parallel prefix scan, associative | 线性递推，并行前缀扫描，结合律（可结合的） |
| minGRU, minLSTM, xLSTM, state-space model | minGRU，minLSTM，xLSTM，状态空间模型 |

### Attention as geometry (Part 13)

| English | 中文 |
|---|---|
| attention; query, key, value | 注意力；查询，键，值 |
| kernel smoother (Nadaraya–Watson), bandwidth | 核平滑器（纳达拉亚–沃森），带宽 |
| scaled dot-product attention | 缩放点积注意力 |
| softmax saturation, Jacobian | softmax饱和，雅可比矩阵 |
| inverse temperature (β) | 逆温度（β） |
| modern Hopfield network, metastable state | 现代霍普菲尔德网络，亚稳态 |
| attention head, multi-head attention | 注意力头（头），多头注意力 |
| QK circuit, OV circuit | QK回路，OV回路 |
| low rank, low-rank bottleneck | 低秩，低秩瓶颈 |
| causal mask | 因果掩码 |
| encoder, decoder, cross-attention, prefix language model | 编码器，解码器，交叉注意力，前缀语言模型 |
| permutation equivariance | 置换等变性 |
| transformer block | Transformer模块 |
| FLOPs per token | 每个词元的浮点运算数 |
| sinusoidal position encoding, learned absolute positions | 正弦位置编码，学出来的绝对位置 |
| relative positions, ALiBi | 相对位置，ALiBi |
| no positional encoding (NoPE) | 无位置编码（NoPE） |
| rotary position embedding (RoPE), wavelength, base | 旋转位置编码（RoPE），波长，底数 |
| context extension | 上下文扩展 |
| position interpolation, NTK-aware scaling, YaRN | 位置插值，NTK感知缩放，YaRN |
| ramp (γ), attention temperature | 斜坡（γ），注意力温度 |
| log-n scaling | log n缩放 |
| attention sink, sink logit | 注意力汇点，汇点logit |
| active–dormant head, value drain | 活跃-休眠头，值的排空 |
| gated attention (output gate) | 门控注意力（输出门控） |
| differential attention | 差分注意力 |
| QK-norm | QK归一化 |
| soft cap (logit soft-capping) | 软上限（logit软封顶） |
| induction head, previous-token head | 归纳头，前一词元头 |
| K-, Q-, V-composition | K组合，Q组合，V组合 |
| phase change (in training) | （训练中的）相变 |
| in-context learning, linear self-attention | 上下文学习，线性自注意力 |
| RASP; select, aggregate | RASP；选择（select），聚合（aggregate） |
| Tracr | Tracr |
| hybrid (linear + full attention) | 混合架构（线性注意力加完整注意力） |

### The guessing game, additions (Part 1)

| English | 中文 |
|---|---|
| Shannon's three requirements; the grouping rule | 香农的三条要求；分组法则 |
| uniqueness of entropy (Shannon's Theorem 2) | 熵的唯一性（香农定理2） |
| Hartley's measure of information | 哈特利的信息度量 |
| uniquely decodable code | 唯一可解码的码 |
| Kraft–McMillan inequality | 克拉夫特–麦克米兰不等式 |
| canonical code | 规范码 |
| exchange argument; sibling (leaves) | 交换论证；兄弟（叶子） |
| optimal code | 最优码 |
| typical set, typical sequence | 典型集，典型序列 |
| asymptotic equipartition property (AEP) | 渐近均分性（AEP） |
| law of large numbers | 大数定律 |
| block code | 分组编码 |
| finite precision; register | 有限精度；寄存器 |
| zoom (renormalization); pending bit | 放大（重新归一化）；待定比特 |
| Laplace's rule of succession; the sunrise problem | 拉普拉斯接续法则；日出问题 |
| prior | 先验 |
| add-one (Laplace) smoothing | 加一（拉普拉斯）平滑 |
| data-processing inequality | 数据处理不等式 |
| chain rule for mutual information | 互信息的链式法则 |
| tokenizer, vocabulary | 分词器，词表 |
| bits per token, bits per byte | 每词元比特数，每字节比特数 |
| perplexity | 困惑度 |
| two-part code; adjusted compression rate | 两段式编码；调整后的压缩率 |
| Hutter Prize; context mixing | 赫特奖；上下文混合 |
| round trip (encode, then decode) | 往返（先编码，再解码） |

### Learning without labels (Part 24)

| English | 中文 |
|---|---|
| self-supervised learning | 自监督学习 |
| representation, encoder | 表示，编码器 |
| label, unlabelled data | 标签，无标签数据 |
| pretext task | 前置任务（代理任务） |
| context prediction, jigsaw puzzle, colorization, inpainting | 上下文预测，拼图，上色，图像修补 |
| rotation prediction | 旋转预测 |
| shortcut, chromatic aberration | 捷径，色差 |
| instance discrimination, memory bank | 实例判别，记忆库 |
| contrastive learning, contrastive loss | 对比学习，对比损失 |
| positive pair, negative (sample) | 正样本对，负样本 |
| noise-contrastive estimation (NCE) | 噪声对比估计（NCE） |
| negative sampling | 负采样 |
| InfoNCE, critic (scoring function) | InfoNCE，打分函数 |
| contrastive predictive coding (CPC) | 对比预测编码（CPC） |
| view, augmentation | 视图，数据增强 |
| projection head | 投影头 |
| NT-Xent (normalized temperature-scaled cross-entropy) | NT-Xent（归一化温度交叉熵） |
| momentum encoder, queue | 动量编码器，队列 |
| hypersphere, unit vector | 超球面，单位向量 |
| alignment, uniformity | 对齐，均匀性 |
| temperature τ | 温度τ |
| hard negative | 难负样本 |
| uniformity–tolerance dilemma | 均匀性-容忍度困境 |
| collapse: complete, dimensional | 坍缩：完全坍缩，维度坍缩 |
| effective rank, RankMe | 有效秩，RankMe |
| singular-value spectrum | 奇异值谱 |
| siamese network | 孪生网络 |
| stop-gradient | 停止梯度 |
| predictor | 预测器 |
| online network, target network | 在线网络，目标网络 |
| exponential moving average (EMA) | 指数移动平均（EMA） |
| redundancy reduction | 冗余削减 |
| cross-correlation matrix | 互相关矩阵 |
| invariance, variance, covariance terms | 不变项，方差项，协方差项 |
| decorrelation | 去相关 |
| self-distillation, student, teacher | 自蒸馏，学生，老师 |
| prototype | 原型 |
| centring, sharpening | 中心化，锐化 |
| data curation, retrieval-based curation | 数据筛选，基于检索的筛选 |
| deduplication | 去重 |
| Gram anchoring | 格拉姆锚定 |
| masked image modelling, masked autoencoder (MAE) | 掩码图像建模，掩码自编码器（MAE） |
| masking ratio | 掩码比例 |
| visual token, codebook | 视觉词元，码本 |
| fine-tuning (the whole network) | （整个网络）微调 |
| joint-embedding predictive architecture (JEPA) | 联合嵌入预测架构（JEPA） |
| context block, target block | 上下文块，目标块 |
| energy-based view; contrastive vs regularized methods | 能量视角；对比式与正则化式方法 |
| world model | 世界模型 |
| linear probe, k-NN probe, few-label probe | 线性探针，k近邻探针，少标签探针 |
| embedding, retrieval, nearest-neighbour search | 嵌入，检索，最近邻搜索 |
| text embedding, sentence embedding | 文本嵌入，句子嵌入 |
| Matryoshka representation learning | 套娃表示学习 |
| centred kernel alignment (CKA), HSIC | 中心化核对齐（CKA），HSIC |
| mutual nearest neighbours | 互为近邻 |
| platonic representation hypothesis | 柏拉图表示假说 |

### Diffusion and flow (Part 21)

| English | 中文 |
|---|---|
| diffusion model | 扩散模型 |
| forward process, reverse process | 前向过程，反向过程 |
| noise schedule; β_t; ᾱ_t (alpha bar) | 噪声调度；β_t；ᾱ_t（阿尔法拔） |
| variance preserving (VP) | 方差保持 |
| evidence lower bound (ELBO), variational bound | 证据下界（ELBO），变分下界 |
| noise prediction (ε-prediction), the simple loss | 噪声预测（ε预测），简化损失 |
| denoiser D(x; σ) | 去噪器D(x; σ) |
| Tweedie's formula, posterior mean | 特威迪公式，后验均值 |
| stochastic differential equation (SDE), reverse-time SDE | 随机微分方程（SDE），反向时间SDE |
| probability-flow ODE | 概率流常微分方程（概率流ODE） |
| Fokker–Planck equation, continuity equation | 福克-普朗克方程，连续性方程 |
| DDPM, DDIM, ancestral sampling, η | DDPM，DDIM，祖先采样，η |
| signal-to-noise ratio (SNR), log-SNR, terminal SNR | 信噪比，对数信噪比，终端信噪比 |
| step spacing | （采样）步长间隔 |
| preconditioning (c_in, c_skip, c_out) | 预条件化（c_in，c_skip，c_out） |
| error amplification | 误差放大 |
| Euler's method, Heun's method, second order | 欧拉法，休恩法，二阶 |
| exponential integrator, integrating factor | 指数积分器，积分因子 |
| DPM-Solver, DPM-Solver++ (multistep) | DPM-Solver，DPM-Solver++（多步法） |
| network evaluations (NFE) | 网络调用次数（NFE） |
| sliced Wasserstein distance | 切片瓦瑟斯坦距离 |
| optimal transport, coupling, transport cost | 最优传输，耦合（配对），运输代价 |
| Benamou–Brenier formula, kinetic energy | 贝纳穆-布雷尼耶公式，动能 |
| flow matching; conditional and marginal velocity | 流匹配；条件速度与边缘速度 |
| marginal-field theorem | 边缘速度场定理 |
| stochastic interpolant | 随机插值 |
| rectified flow, reflow, straightness | 整流流，重流，直度 |
| minibatch optimal transport (OT-CFM) | 小批量最优传输 |
| distillation, teacher, student | 蒸馏，老师，学生 |
| progressive distillation | 渐进蒸馏 |
| consistency model, self-consistency, consistency distillation | 一致性模型，自洽性，一致性蒸馏 |
| distribution matching distillation (DMD) | 分布匹配蒸馏（DMD） |
| MeanFlow, average velocity | MeanFlow，平均速度 |
| shortcut model | 捷径模型 |
| Jacobian-vector product, stop-gradient | 雅可比-向量积，停止梯度 |
| classifier guidance, classifier-free guidance (CFG), guidance weight w | 分类器引导，无分类器引导（CFG），引导权重w |
| autoguidance | 自引导 |
| precision and recall (k-NN) | 精确率与召回率（k近邻） |
| latent diffusion, latents | 潜空间扩散，潜变量 |
| diffusion transformer (DiT) | 扩散Transformer（DiT） |
| discrete diffusion (D3PM), transition matrix | 离散扩散（D3PM），转移矩阵 |
| uniform noise, absorbing (mask) noise, mask token [M] | 均匀噪声，吸收态（掩码）噪声，掩码词元[M] |
| masked diffusion, weighted cross-entropy | 掩码扩散，加权交叉熵 |
| any-order autoregressive model | 任意顺序自回归模型 |
| a tight bound | 紧的下界 |
| block diffusion | 块扩散 |
| surest-first unmasking (low-confidence remasking) | 最有把握优先的揭开（低置信度重掩码） |
| judged bits per character (generative perplexity) | 由另一个模型评判的每字符比特数（生成困惑度） |
| diffusion language model (dLLM) | 扩散语言模型 |

### Symmetry and science (Part 25)

| English | 中文 |
|---|---|
| symmetry, transformation | 对称，变换 |
| group, group action, identity, inverse | 群，群作用，单位元，逆元 |
| permutation, permutation group | 置换（排列），置换群 |
| rotation group SO(3), E(3), E(n), SE(3) | 转动群SO(3)，E(3)，E(n)，SE(3) |
| rigid motion, reflection, translation | 刚体运动，反射，平移 |
| invariant, invariance | 不变的，不变性 |
| equivariant, equivariance | 等变的，等变性 |
| group averaging (Reynolds operator) | 群平均（雷诺算子） |
| data augmentation | 数据增强 |
| canonicalization (standard pose) | 规范化（标准姿态） |
| geometric deep learning | 几何深度学习 |
| set function, multiset | 集合函数，多重集 |
| Deep Sets, PointNet | Deep Sets，PointNet |
| power sums, Newton's identities | 幂和，牛顿恒等式 |
| graph, node, edge, adjacency matrix | 图，节点，边，邻接矩阵 |
| graph neural network (GNN) | 图神经网络（GNN） |
| message passing (MPNN), message, readout | 消息传递（MPNN），消息，读出 |
| graph convolutional network (GCN) | 图卷积网络（GCN） |
| hop, receptive field | 跳，感受野 |
| stochastic block model, community | 随机块模型，社群 |
| Weisfeiler–Leman test (1-WL), colour refinement | 魏斯费勒–莱曼检验（1-WL），颜色细化 |
| graph isomorphism | 图同构 |
| graph isomorphism network (GIN) | 图同构网络（GIN） |
| sum / mean / max aggregation | 求和 / 平均 / 最大值聚合 |
| regular graph, union of cycles | 正则图，若干环的并 |
| random node features (RNI) | 随机节点特征（RNI） |
| pair network (provably powerful graph network) | 节点对网络（可证明强大的图网络） |
| k-WL, subgraph counts, positional encoding | k-WL，子图计数，位置编码 |
| over-smoothing, Dirichlet energy | 过平滑，狄利克雷能量 |
| over-squashing, bottleneck, curvature | 过挤压，瓶颈，曲率 |
| residual (skip) connection | 残差（跳跃）连接 |
| graph attention (GAT, GATv2), graph transformer | 图注意力（GAT，GATv2），图Transformer |
| decalin, bicyclopentyl | 十氢萘，联环戊烷 |
| E(n)-equivariant graph network (EGNN) | E(n)等变图网络（EGNN） |
| SchNet, radial basis functions | SchNet，径向基函数 |
| spherical harmonics, degree ℓ | 球谐函数，阶ℓ |
| Wigner D-matrix (rotation block) | 维格纳D矩阵（转动块） |
| Clebsch–Gordan coefficients, tensor product | 克莱布什–戈尔丹系数，张量积 |
| tensor field network, NequIP, MACE, e3nn | 张量场网络，NequIP，MACE，e3nn |
| interatomic potential, force field | 原子间势，力场 |
| n-body system, charged particles | 多体系统，带电粒子 |
| protein, amino acid, residue | 蛋白质，氨基酸，残基 |
| fold, backbone, C-alpha (Cα) | 折叠（构象），主链，Cα原子 |
| helix, strand, loop, three-helix bundle | 螺旋，链，环，三螺旋束 |
| X-ray crystallography, cryo-EM | X射线晶体学，冷冻电镜 |
| Protein Data Bank (PDB) | 蛋白质数据库（PDB） |
| Levinthal's paradox | 列文索尔悖论 |
| CASP, GDT_TS, free modelling | CASP，GDT_TS，自由建模（无模板） |
| multiple sequence alignment (MSA), co-evolution, contact | 多序列比对（MSA），共进化，接触 |
| distogram | 距离直方图 |
| classical multidimensional scaling (MDS), Gram matrix | 经典多维尺度分析（MDS），格拉姆矩阵 |
| mirror image, chirality, right-handed | 镜像，手性，右手的 |
| RMSD, distance RMSD (dRMSD), Kabsch alignment | 均方根偏差（RMSD），距离均方根偏差（dRMSD），Kabsch对齐 |
| Evoformer, pair representation, MSA representation | Evoformer，残基对表示，MSA表示 |
| row / column attention, outer product mean | 行 / 列注意力，外积均值 |
| triangle inequality, triangle multiplicative update, triangle attention | 三角不等式，三角乘法更新，三角注意力 |
| structure module, rigid frame, residue gas | 结构模块，刚性坐标系，残基气体 |
| invariant point attention (IPA) | 不变点注意力（IPA） |
| frame-aligned point error (FAPE), clamp | 坐标系对齐点误差（FAPE），截断 |
| recycling | 循环（回收） |
| pLDDT (confidence) | pLDDT（置信度） |
| AlphaFold Protein Structure Database | AlphaFold蛋白质结构数据库 |
| Pairformer, diffusion module | Pairformer，扩散模块 |
| cross-distillation, hallucination | 交叉蒸馏，幻觉 |
| ligand, docking, PoseBusters | 配体，分子对接，PoseBusters |
| protein design, inverse folding, binder | 蛋白质设计，逆折叠，结合子 |
| sequence recovery | 序列还原率 |
| motif scaffolding | 基序支架 |
| denoiser, denoising diffusion | 去噪器，去噪扩散 |
| numerical weather prediction (NWP) | 数值天气预报（NWP） |
| reanalysis (ERA5) | 再分析（ERA5） |
| icosahedral mesh, multimesh | 二十面体网格，多尺度网格（multimesh） |
| encoder–processor–decoder | 编码器–处理器–解码器 |
| rollout, lead time | 推演（展开），预报时效 |
| persistence, climatology | 持续性预报，气候平均 |
| ensemble forecast | 集合预报 |
| vorticity | 涡度 |
| neural operator, Fourier neural operator (FNO), DeepONet | 神经算子，傅里叶神经算子（FNO），DeepONet |
| Burgers' equation, pseudo-spectral solver | 伯格斯方程，伪谱求解器 |
| convolution theorem, Fourier mode | 卷积定理，傅里叶模式 |
| resolution invariance, zero-shot super-resolution | 分辨率不变性，零样本超分辨率 |
| crystal, space group, formation energy | 晶体，空间群，形成能 |
| density functional theory (DFT) | 密度泛函理论（DFT） |
| convex hull, energy above hull, stable | 凸包，凸包上方能量，稳定 |
| active learning, surrogate model, hit rate | 主动学习，代理模型，命中率 |
| autonomous laboratory | 自主实验室 |
| proof assistant, kernel, Lean, Mathlib | 证明助手，内核，Lean，Mathlib |
| formal proof, formalization, autoformalization | 形式化证明，形式化，自动形式化 |
| four-colour theorem, Kepler conjecture | 四色定理，开普勒猜想 |
| symbolic deduction engine, auxiliary construction | 符号演绎引擎，辅助构造 |
| synthetic theorems, traceback | 合成定理，回溯 |
| Erdős problems | 埃尔德什问题 |
| cap set | 帽集 |
| online bin packing, first fit, best fit, priority function | 在线装箱，首次适配，最佳适配，优先级函数 |
| genetic programming, mutation, crossover | 遗传规划，变异，交叉 |
| tensor rank, tensor decomposition | 张量秩，张量分解 |
| alternating least squares | 交替最小二乘 |
| Strassen's algorithm | 施特拉森算法 |
| kissing number | 接吻数 |
| evolutionary coding agent | 进化编程智能体 |

Names stay in Latin script: AlphaFold, AlphaFold-Multimer, AlphaFold Server, RoseTTAFold, ESMFold, ESM3, ProteinMPNN,
RFdiffusion, RFdiffusion3, BindCraft, AlphaProteo, BoltzGen, Boltz-1, Boltz-2, Chai-1, Protenix, OpenFold3, IsoDDE,
Rosetta, Top7, GraphCast, GenCast, AIFS, FourCastNet, Pangu-Weather, WeatherNext, GNoME, MatterGen, MACE-MP-0, A-Lab,
EGNN, SchNet, NequIP, MACE, e3nn, GIN, GCN, GAT, PointNet, Deep Sets, FNO, DeepONet, Lean, Mathlib, AlphaGeometry,
AlphaProof, Gemini Deep Think, Aristotle, Gauss, FunSearch, AlphaEvolve, AlphaTensor.

### Post-training and alignment, additions (Part 27)

| English | 中文 |
|---|---|
| base model, fine-tuned model, forgetting | 基础模型，微调后的模型，遗忘 |
| low-rank adapter (LoRA), rank, adapter | 低秩适配器（LoRA），秩，适配器 |
| reward model, comparison, preference, labeller | 奖励模型，比较，偏好，标注员 |
| gold (the hidden true taste), proxy | 金标准，代理 |
| simulated people, noise τ | 模拟的人，噪声τ |
| ceiling (of a reward model's accuracy) | 上限 |
| within-question comparison, shift per question | 同一问题内的比较，每个问题的平移 |
| correlation, slope | 相关系数，斜率 |
| gold units (a score divided by its slope on gold) | 金标准单位 |
| a perfect learner (slope 1/τ) | 完美的学习者（斜率1/τ） |
| decomposition into gold's terms: mood, length, repetition, too short | 按金标准的各项分解：情绪，长度，重复，太短 |
| occlusion (deleting one word at a time) | 遮挡（一次删掉一个词） |
| regressional Goodhart, extremal Goodhart | 回归型古德哈特，极端型古德哈特 |
| KL-regularized optimum, partition function Z | KL正则化的最优解，配分函数Z |
| an answer as an episode: state, action (token) | 把回答当作回合：状态，动作（词元） |
| per-token KL penalty | 逐词元的KL惩罚 |
| value network (value model), critic | 价值网络（价值模型），评论家 |
| advantage, generalized advantage estimation (GAE) | 优势，广义优势估计（GAE） |
| baseline, group baseline, leave-one-out (RLOO) | 基线，组基线，留一（RLOO） |
| group relative policy optimization (GRPO) | 组相对策略优化（GRPO） |
| gradient estimate, cosine between two estimates | 梯度估计，两个估计之间的余弦 |
| direct preference optimization (DPO), implicit reward | 直接偏好优化（DPO），隐式奖励 |
| online / offline preference data | 在线/离线偏好数据 |
| distillation, teacher, student, soft targets, dark knowledge, temperature | 蒸馏，老师，学生，软目标，暗知识，温度 |
| forward KL, reverse KL, on-policy distillation | 前向KL，反向KL，在线策略蒸馏 |
| model merging, task vector, task arithmetic, model soup | 模型合并，任务向量，任务算术，模型汤 |
| linear mode connectivity | 线性模式连通 |
| sycophancy, jailbreak, adversarial suffix, many-shot jailbreaking, over-refusal | 谄媚，越狱，对抗后缀，多样本越狱，过度拒绝 |
| emergent misalignment, alignment faking, persona vector | 涌现式失准，对齐伪装，人格向量 |
| cold start, strong-to-weak distillation | 冷启动，强到弱蒸馏 |

### Inference (Part 19)

| English | 中文 |
|---|---|
| inference, serving | 推断，服务（部署） |
| prefill, decode | 预填充，解码 |
| key-value cache (KV cache) | 键值缓存（KV缓存） |
| multi-head, multi-query, grouped-query attention (MHA, MQA, GQA) | 多头注意力，多查询注意力，分组查询注意力 |
| multi-head latent attention (MLA) | 多头潜在注意力（MLA） |
| batch, batch size | 批，批大小 |
| throughput, latency | 吞吐量，延迟 |
| time to first token (TTFT), time between tokens | 首个词元的等待时间，词元之间的间隔 |
| static batching, continuous batching | 静态批处理，连续批处理 |
| iteration-level scheduling | 迭代级调度 |
| chunked prefill | 分块预填充 |
| disaggregated serving (prefill and decode on separate workers) | 预填充与解码分离部署 |
| paged attention, page, block table | 分页注意力，页，块表 |
| fragmentation (internal, external) | 碎片（内部，外部） |
| preemption | 抢占 |
| prefix caching, radix tree | 前缀缓存，基数树 |
| speculative decoding, speculative sampling | 推测解码，推测采样 |
| draft model, drafter, target model | 草稿模型，起草器，目标模型 |
| acceptance rate | 接受率 |
| EAGLE head, Medusa heads | EAGLE头，Medusa头 |
| total variation distance | 总变差距离 |
| quantization, round to nearest | 量化，就近舍入 |
| scale (per tensor, per row, per group) | 缩放因子（每张量，每行，每组） |
| step size Δ | 步长Δ |
| calibration data | 校准数据 |
| activation outliers, outlier channels | 激活离群值，离群通道 |
| W8A8 (8-bit weights and activations) | W8A8（8比特权重和激活） |
| SmoothQuant, migration strength α | SmoothQuant，迁移强度α |
| Optimal Brain Damage, Optimal Brain Surgeon | 最优脑损伤，最优脑外科 |
| GPTQ, AWQ (activation-aware weight quantization) | GPTQ，AWQ（激活感知的权重量化） |
| salient weights | 显著权重 |
| Hadamard matrix, rotation | 哈达玛矩阵，旋转 |
| computational invariance | 计算不变性 |
| Cayley map, skew-symmetric matrix | 凯莱映射，反对称矩阵 |
| crest factor (peak over typical) | 峰值因子（峰值与典型值之比） |
| E2M1, E4M3, E8M0 | E2M1，E4M3，E8M0 |
| MXFP4, NVFP4, shared exponent, clamping | MXFP4，NVFP4，共享指数，截断 |
| KV-cache quantization; per-channel, per-token | KV缓存量化；按通道，按词元 |
| online softmax, running max, running sum | 在线softmax，当前最大值，累计和 |
| IO complexity | IO复杂度 |
| Flash-Decoding, split-KV, log-sum-exp | Flash-Decoding，KV切分，对数求和指数 |
| occupancy | 占用率 |
| sliding-window attention, sparse attention, indexer | 滑动窗口注意力，稀疏注意力，索引器 |
| constrained decoding, structured output | 约束解码，结构化输出 |
| finite automaton, regular expression, token mask | 有限自动机，正则表达式，词元掩码 |
| grammar-aligned decoding | 语法对齐解码 |
| test-time compute, thinking budget | 测试时计算，思考预算 |
| price per million tokens | 每百万词元的价格 |
| on-device inference | 端侧推断 |
