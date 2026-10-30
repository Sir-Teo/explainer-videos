# AI, Built — Part 15: Memory

Part 15 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Act III, *The Transformer Era*. What a model has to remember while it reads,
and the ways to keep it: attention's growing cache, made smaller or partly thrown away; a fixed-size matrix memory,
from Hopfield networks and Schmidhuber's fast weights to linear attention, written by better and better rules
(decay, the delta rule, the gated delta rule) and trained in parallel (the associative scan, the WY/UT chunkwise form,
Mamba-2's duality); state-space models from HiPPO and S4 to Mamba and Mamba-3; memories that learn while they read
(test-time training, Titans); recall measured on small trained models; hybrids, from Jamba to Qwen3.5 and Kimi K3;
how long contexts really are (needle, RULER, NoLiMa, our own tests); and memory outside the model (dense retrieval,
RETRO, the kNN-LM on the novels, with a scoreboard row). Part 19 covers serving the cache (paging, quantization,
attention at serve time); Part 16 covers sparse attention; Part 10 the LSTM and the first scans.

Every model is trained here, on a CPU, by `compute.py` (one torch thread a process, at most two processes):

* **MQAR** (multi-query associative recall): 16 key-value pairs then the keys again; two-layer models with six
  memories (softmax attention, linear attention, a Mamba-2-style selective SSM, the delta rule, the gated delta rule,
  a hybrid of a gated-delta layer under an attention layer), keys of 2 to 16 numbers, three seeds each, 1,000 steps,
  equal parameters up to a few gates (`recall.py`, `mixers.py`).
* **RULER-style tests**: one needle, one of four needles, a chain of three names, trained at 128 tokens and tested up
  to 1,024; four memories, two seeds.
* **Two language models on the novels** (`novels_lm.py`): a transformer (four attention layers, rotary positions) and
  a gated-delta hybrid (three gated-delta layers, then attention without positions, as Kimi Linear), width 64, 256
  tokens of context, 400 steps of 16 × 256 tokens, three seeds each.
* **The series' own model** (`explainer.ai.novels`, 6.8 million weights) is read with a smaller cache (window, sinks,
  heavy hitters) and given a nearest-neighbour memory of the thirty novels (`memory_lm.py`).
* **Toys**: a Hopfield network; a matrix memory written and read; HiPPO-LegS memorizing a signal; the zero-order hold
  against a Runge–Kutta solution; the parallel scan; the WY/UT chunkwise delta rule; test-time training and Titans.

## Chapters

RESULTS_PLACEHOLDER

## Running it

```bash
python tools/make.py ai15                          # everything: Parts 1, 10, 13, 14's results and the novels model
                                                   # it reads, its own computations, the narrated cut in en and zh
python -m videos.ai.ai15.compute                   # only the numbers (resumable: rerun after an interruption)
python -m videos.ai.ai15.compute mqar --force      # one item again
EXPLAINER_TTS=silent python tools/build.py ai15 -q l --fps 15 --lang en     # a quick silent preview
python tools/qa_scene.py ai15 Recall               # one chapter, silent, with a contact sheet
```

Compute: about 3–4 CPU-hours on a busy 4-core machine (MQAR 72 runs, the language models 6 runs, the kNN sweep over
6.6 million stored states, RULER 8 runs); much less on an idle laptop. Every random choice is seeded; the MQAR, RULER
and language-model runs are saved one by one (`CACHE.partial`) and the language models checkpoint every 100 steps; the
kNN sweep checkpoints its running neighbours every 40 batches. Worker processes use the `spawn` start method.

## References

Books and notes: S. J. D. Prince, *Understanding Deep Learning* (2023), ch. 12; S. Yang, *DeltaNet Explained* (blog,
2024) and the flash-linear-attention library; A. Gu, *Modeling Sequences with Structured State Spaces* (thesis, 2023).

* Associative memory: Hebb (1949); Kohonen (1972), Anderson (1972); Hopfield, PNAS (1982); Amit, Gutfreund &
  Sompolinsky (1985); Schmidhuber, *Learning to control fast-weight memories* (1992); Ba, Hinton, Mnih, Leibo &
  Ionescu, *Using fast weights to attend to the recent past* (2016); Graves, Wayne & Danihelka, NTM (2014); Weston,
  Chopra & Bordes, memory networks (2014); Sukhbaatar et al. (2015).
* The cache: Shazeer, MQA (2019); Ainslie et al., GQA (2023); DeepSeek-AI, DeepSeek-V2 (2024), V3 (2024).
* Keeping less: Child et al., Sparse Transformer (2019); Dai et al., Transformer-XL (2019); Beltagy et al., Longformer
  (2020); Zaheer et al., BigBird (2020); Xiao et al., StreamingLLM (2023, arXiv 2309.17453); Zhang et al., H₂O (2023,
  arXiv 2306.14048).
* Linear attention and its write rules: Katharopoulos et al. (2020); Widrow & Hoff (1960); Schlag, Irie & Schmidhuber
  (2021); Yang et al., DeltaNet (2024); Yang, Kautz & Hatamizadeh, Gated DeltaNet (2025); Grazzi et al. (2025);
  Kimi Team, Kimi Linear (arXiv 2510.26692, 2025); Beck et al., xLSTM (2024); Peng et al., RWKV-7 (arXiv 2503.14456,
  2025); Sun et al., RetNet (2023); Yang et al., GLA (2024).
* Parallel training: Blelloch, *Prefix sums and their applications* (1990); Martin & Cundy (2018); Bischof & Van
  Loan, the WY representation (1987); Joffrain et al., the UT transform (2006).
* State spaces: Gu, Dao, Ermon, Rudra & Ré, HiPPO (2020); Gu, Goel & Ré, S4 (2022); Gu & Dao, Mamba (2023); Dao & Gu,
  Mamba-2 (2024); Lahoti et al., Mamba-3 (ICLR 2026, arXiv 2603.15569).
* Memories that learn: Sun et al., TTT (arXiv 2407.04620, 2024); Behrouz, Zhong & Mirrokni, Titans (arXiv
  2501.00663, 2024); Wang, Shi & Fox, *Test-time regression* (2025).
* Recall and long context: Arora et al., Zoology (2023); Kamradt, needle in a haystack (2023); Liu et al., *Lost in the
  Middle* (2023); Hsieh et al., RULER (2024); Modarressi et al., NoLiMa (2025); Hong, Troynikov & Huber, *Context
  Rot* (Chroma, 2025); Google, Gemini 1.5 (2024); Anthropic, Claude Opus 4.6 announcement (February 2026); Anthropic,
  *Effective context engineering for AI agents* (September 2025).
* Hybrids: Lieber et al., Jamba (2024); MiniMax, MiniMax-01 (2025); NVIDIA, Nemotron-H (2025), Nemotron 3 (2025); IBM,
  Granite 4.0 (2025); Qwen Team, Qwen3-Next (2025), Qwen3.5 (model card, 2026); Moonshot AI, Kimi K3 (model card,
  2026); H. Sun, *Why did M2 end up as a full attention model?* (MiniMax, 2025); DeepSeek-AI, DeepSeek-V4 (2026).
* Retrieval: Karpukhin et al., DPR (2020); Guu et al., REALM (2020); Lewis et al., RAG (2020); Khandelwal et al., kNN-LM
  (2020); Grave, Joulin & Usunier, continuous cache (2017); Borgeaud et al., RETRO (2021).

## Problems

1. A model has *L* layers and *H* key-value heads of *d_h* numbers, stored in bf16. How many bytes does its cache take
   per token? Evaluate for Llama 3.1 70B (*L* = 80, *H* = 8, *d_h* = 128) at 128,000 tokens, and with one key-value head.
2. For *N* random unit keys in *d* dimensions, show E[(k_i · k_j)²] = 1/d for i ≠ j, and that adding *N* pairs gives a
   relative read error of about (N − 1)/d.
3. With ‖k‖ = 1, show the delta rule gives S_t k = (1 − β) S_{t−1} k + β v and leaves S_t u = S_{t−1} u for u ⊥ k.
   Find the eigenvalues of I − β k kᵀ; for which β is it a projection, a reflection?
4. Show that (a₁, b₁) • (a₂, b₂) = (a₁a₂, a₂b₁ + b₂) is associative, find its identity, and count the rounds of a scan
   over 10⁶ tokens.
5. For h′ = −λh + x, derive the zero-order hold Ā = e^{−λΔ}, B̄ = (1 − e^{−λΔ})/λ. When is Euler's Ā = 1 − λΔ
   unstable? For eigenvalues −0.3 ± 2i, find the largest stable Euler step.
6. A kNN-LM mixes p = λ p_kNN + (1 − λ) p_LM. Show it never costs more than log₂ 1/(1 − λ) bits on a token, and find
   when it saves bits.

### Solutions

1. Keys and values: 2 × L × H × d_h numbers of 2 bytes, 4·L·H·d_h bytes a token. Llama 3.1 70B: 4 × 80 × 8 × 128 =
   327,680 bytes = 320 KiB; at 128,000 tokens 41.9 GB = 39.1 GiB. With one key-value head (MQA): 40 KiB a token,
   4.9 GiB.
2. For independent unit vectors, E[k_i k_iᵀ] = I/d by symmetry, so E[(k_i·k_j)²] = E[k_jᵀ E[k_i k_iᵀ] k_j] = ‖k_j‖²/d
   = 1/d. Reading pair j gives S k_j − v_j = Σ_{i≠j} v_i (k_i · k_j); with independent values of equal norm the cross
   terms average out and E‖S k_j − v_j‖² = Σ_{i≠j} ‖v_i‖² E[(k_i·k_j)²] = (N − 1)‖v‖²/d. Relative error (N − 1)/d: as
   big as the answer by N ≈ d (the chapter's curve, d = 64).
3. S_t = S_{t−1}(I − βkkᵀ) + βvkᵀ, so S_t k = S_{t−1}k − βS_{t−1}k(kᵀk) + βv(kᵀk) = (1 − β)S_{t−1}k + βv, and for
   u ⊥ k, kᵀu = 0 gives S_t u = S_{t−1}u. I − βkkᵀ has eigenvalue 1 on the (d − 1)-dimensional space ⊥ k and 1 − β on
   k. β = 1: eigenvalues 1 and 0, the projection onto k⊥ (the old answer erased, then v written). β = 2: eigenvalues
   1 and −1, a reflection (a Householder matrix); for 0 < β < 2 the map is a contraction along k, and β ∈ (0, 2]
   keeps it stable while allowing the sign flip that lets these memories track parity.
4. ((a₁,b₁)•(a₂,b₂))•(a₃,b₃) = (a₁a₂, a₂b₁+b₂)•(a₃,b₃) = (a₁a₂a₃, a₃a₂b₁ + a₃b₂ + b₃), and (a₁,b₁)•((a₂,b₂)•(a₃,b₃))
   = (a₁,b₁)•(a₂a₃, a₃b₂+b₃) = (a₁a₂a₃, a₂a₃b₁ + a₃b₂ + b₃): equal. Identity (1, 0). A Hillis–Steele scan takes
   ⌈log₂ 10⁶⌉ = 20 rounds; Blelloch's up and down sweeps take 2 × 20 = 40 rounds but only about 2 × 10⁶ combines.
5. Over a step with x held constant, h(t+Δ) = e^{−λΔ}h(t) + ∫₀^Δ e^{−λ(Δ−s)} ds · x = e^{−λΔ}h(t) + (1 − e^{−λΔ})/λ · x.
   Euler's |1 − λΔ| ≤ 1 needs Δ ≤ 2/λ; beyond it the recurrence blows up. For complex μ = −0.3 ± 2i, |1 + Δμ|² =
   (1 − 0.3Δ)² + 4Δ² ≤ 1 ⇔ Δ(4.09Δ − 0.6) ≤ 0 ⇔ Δ ≤ 0.6/4.09 ≈ 0.147: the chapter's Euler steps of 0.2 and 0.4 are
   unstable, which is why their errors exploded. The zero-order hold is stable for every Δ: |e^{Δμ}| = e^{−0.3Δ} < 1.
6. p ≥ (1 − λ) p_LM, so −log₂ p ≤ −log₂ p_LM + log₂ 1/(1 − λ): at most log₂ 1/(1 − λ) bits worse (0.15 bits at λ =
   0.1, 0.42 at λ = 0.25). It saves bits exactly when λ p_kNN + (1 − λ) p_LM > p_LM, that is when p_kNN > p_LM: the
   neighbours give the true token more probability than the model does.

## 习题（中文）

1. 一个模型有 *L* 层、*H* 个键值头，每个头 *d_h* 个数，用 bf16 存储。每个词元的缓存占多少字节？对 Llama 3.1 70B
   （*L* = 80，*H* = 8，*d_h* = 128）算出 12.8 万个词元的缓存，再算只有一个键值头时的情形。
2. *d* 维空间里 *N* 个随机单位键，证明 i ≠ j 时 E[(k_i · k_j)²] = 1/d，并证明累加 *N* 对之后，读回的相对误差约为
   (N − 1)/d。
3. 设 ‖k‖ = 1，证明 δ 规则给出 S_t k = (1 − β) S_{t−1} k + β v，并且对 u ⊥ k 有 S_t u = S_{t−1} u。求 I − β k kᵀ
   的特征值；β 取多少时它是投影，取多少时是反射？
4. 证明 (a₁, b₁) • (a₂, b₂) = (a₁a₂, a₂b₁ + b₂) 满足结合律，求它的单位元，并数一数对 10⁶ 个词元做扫描需要几轮。
5. 对 h′ = −λh + x，推导零阶保持 Ā = e^{−λΔ}，B̄ = (1 − e^{−λΔ})/λ。欧拉法的 Ā = 1 − λΔ 什么时候不稳定？
   特征值为 −0.3 ± 2i 时，欧拉法最大的稳定步长是多少？
6. kNN-LM 混合 p = λ p_kNN + (1 − λ) p_LM。证明它在一个词元上最多多花 log₂ 1/(1 − λ) 比特，并求它什么时候能省下比特。

### 解答

1. 键和值共 2 × L × H × d_h 个数，每个 2 字节，即每个词元 4·L·H·d_h 字节。Llama 3.1 70B：4 × 80 × 8 × 128 =
   327,680 字节 = 320 KiB；12.8 万个词元是 41.9 GB = 39.1 GiB。只有一个键值头（MQA）时：每个词元 40 KiB，共 4.9 GiB。
2. 独立的单位向量由对称性有 E[k_i k_iᵀ] = I/d，于是 E[(k_i·k_j)²] = E[k_jᵀ E[k_i k_iᵀ] k_j] = 1/d。读第 j 对得到
   S k_j − v_j = Σ_{i≠j} v_i (k_i · k_j)；值彼此独立、范数相同，交叉项平均为零，E‖S k_j − v_j‖² = (N − 1)‖v‖²/d，
   相对误差 (N − 1)/d：N 接近 d 时，噪声就和答案一样大（本章的曲线，d = 64）。
3. S_t k = S_{t−1}k − βS_{t−1}k + βv = (1 − β)S_{t−1}k + βv；u ⊥ k 时 kᵀu = 0，所以 S_t u = S_{t−1}u。I − βkkᵀ
   在与 k 垂直的 d − 1 维子空间上特征值为 1，在 k 方向上为 1 − β。β = 1 时特征值是 1 和 0，是到 k⊥ 的投影；β = 2 时是
   1 和 −1，是一个反射（豪斯霍尔德矩阵）；β 在 (0, 2] 内都稳定，而正负号的翻转让这些记忆能追踪奇偶性。
4. 两种组合都得到 (a₁a₂a₃, a₂a₃b₁ + a₃b₂ + b₃)，所以满足结合律；单位元是 (1, 0)。希利斯–斯蒂尔扫描需要
   ⌈log₂ 10⁶⌉ = 20 轮；布莱洛赫的上扫加下扫需要 40 轮，但总共只做大约 2 × 10⁶ 次组合。
5. 输入在一步内不变时，h(t+Δ) = e^{−λΔ}h(t) + (1 − e^{−λΔ})/λ · x。欧拉法要求 |1 − λΔ| ≤ 1，即 Δ ≤ 2/λ，否则
   递推会发散。对复数 μ = −0.3 ± 2i，|1 + Δμ|² = (1 − 0.3Δ)² + 4Δ² ≤ 1 ⇔ Δ ≤ 0.6/4.09 ≈ 0.147：本章 0.2 和 0.4 的
   欧拉步长都不稳定，所以误差爆炸。零阶保持对任何 Δ 都稳定：|e^{Δμ}| = e^{−0.3Δ} < 1。
6. p ≥ (1 − λ) p_LM，所以 −log₂ p ≤ −log₂ p_LM + log₂ 1/(1 − λ)：最多差 log₂ 1/(1 − λ) 比特（λ = 0.1 时 0.15 比特，
   λ = 0.25 时 0.42 比特）。当且仅当 p_kNN > p_LM 时能省下比特：邻居给正确词元的概率比模型自己给得多。

## Glossary

| English | 中文 |
|---|---|
| KV cache; per token, per layer | KV缓存；每个词元，每层 |
| multi-query attention (MQA), grouped-query attention (GQA) | 多查询注意力（MQA），分组查询注意力（GQA） |
| multi-head latent attention (MLA); latent; absorption (folding the key matrix into the query) | 多头潜在注意力（MLA）；潜在向量；吸收（把键矩阵并进查询） |
| decoupled rotary key | 解耦的旋转键 |
| cache eviction; sliding window; global tokens; random keys | 缓存逐出（挤出）；滑动窗口；全局词元；随机键 |
| segment-level recurrence (Transformer-XL) | 段级递推（Transformer-XL） |
| attention sink; StreamingLLM | 注意力汇点；StreamingLLM |
| heavy hitter (H₂O) | 重量级词元（heavy hitter，H₂O） |
| linear attention; feature map φ | 线性注意力；特征映射φ |
| outer product | 外积 |
| associative memory; correlation matrix memory | 联想记忆；相关矩阵记忆 |
| Hopfield network; Hebb's rule; energy; capacity | 霍普菲尔德网络；赫布规则；能量；容量 |
| fast weights; fast weight programmer | 快权重；快权重编程器 |
| crosstalk | 串扰 |
| decay; forget gate | 衰减；遗忘门 |
| delta rule; least mean squares (LMS); online least squares | δ规则；最小均方（LMS）；在线最小二乘 |
| gated delta rule (Gated DeltaNet); Kimi Delta Attention (KDA) | 门控δ规则（Gated DeltaNet）；Kimi Delta Attention（KDA） |
| projection; reflection; Householder matrix | 投影；反射；豪斯霍尔德矩阵 |
| parity; state tracking; finite automaton | 奇偶性；状态追踪；有限自动机 |
| matrix LSTM (mLSTM, xLSTM); RWKV-7 | 矩阵LSTM（mLSTM，xLSTM）；RWKV-7 |
| associative scan, parallel prefix scan; up-sweep, down-sweep | 结合律扫描，并行前缀扫描；上扫，下扫 |
| chunkwise training; WY form; UT transform | 分块训练；WY形式；UT变换 |
| state-space model (SSM); zero-order hold; bilinear (Tustin) rule; Euler step | 状态空间模型（SSM）；零阶保持；双线性规则；欧拉步 |
| HiPPO; Legendre polynomials | HiPPO；勒让德多项式 |
| S4; convolution kernel; Path-X | S4；卷积核；Path-X |
| selectivity; selective SSM (Mamba); step size Δ | 选择性；选择性状态空间模型（Mamba）；步长Δ |
| state-space duality (Mamba-2); semiseparable mask | 状态空间对偶（Mamba-2）；半可分掩码 |
| exponential-trapezoidal discretization; complex state; MIMO (Mamba-3) | 指数梯形离散化；复数状态；多输入多输出（Mamba-3） |
| test-time training (TTT); surprise; momentum; forgetting gate (Titans) | 测试时训练（TTT）；意外度；动量；遗忘门（Titans） |
| multi-query associative recall (MQAR) | 多查询联想回忆（MQAR） |
| hybrid architecture; NoPE (no positional encoding) | 混合架构；NoPE（无位置编码） |
| needle in a haystack; lost in the middle; RULER; NoLiMa; context rot | 大海捞针；迷失在中间；RULER；NoLiMa；上下文腐烂 |
| variable tracking; multi-key needle | 变量追踪；多键针 |
| context engineering; compaction; sub-agent | 上下文工程；压缩（compaction）；子智能体 |
| dense retrieval (DPR); retrieval-augmented generation (RAG); RETRO | 稠密检索（DPR）；检索增强生成（RAG）；RETRO |
| kNN-LM; datastore; interpolation weight λ; continuous cache | kNN-LM（k近邻语言模型）；数据存储；插值权重λ；连续缓存 |

