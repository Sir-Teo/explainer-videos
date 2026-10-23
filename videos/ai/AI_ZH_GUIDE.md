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
