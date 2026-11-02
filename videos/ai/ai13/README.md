# AI, Built — Part 13: Attention as Geometry

Part 13 opens the Transformer act of [the series](../README.md). It develops attention as a learned weighted
average and memory read, then examines heads, masks, cost, position, longer contexts, sinks, induction and
in-context learning. The original CPU producer recipes remain in `compute.py`.

## Source review and acceptance limits

This worker update contains source and synthetic contract tests. It preserves the existing public Hook/Frontier
geometry and adds reviewed mathematical, measurement and narration qualifications. It does not distribute
scientific datasets, model weights, numerical caches, private QA records or runtime input manifests.

Source tests do not establish rendered acceptance of this public tree. In particular, selected frames inspected
under a different source/input/runtime combination do not transfer a visual acceptance claim to this revision.
Before production, the integration owner must verify compatible original inputs and runtime, review the exact
integrated English and Chinese output, continuously play it, listen to the actual narration and check speech
synchronization at the final resolution. Final rendering, synthesis, assembly and delivery remain separate work.

Active `s02_smoother.py` and `s19_outro.py` are unchanged by this update. Their source-only candidates live in
[`source_only_candidates/`](source_only_candidates/README.md). They must remain disabled until the compatible
original Part 7 GP input and derived smoother cache are verified and original/final bilingual output QA is done.
The candidates and their narration operations have not passed rendered acceptance.

The existing loader can invoke producers on a missing cache. These source tests deliberately avoid scene/model
imports, training, downloads and scientific regeneration. Do not import scenes or run a build to discover whether
inputs exist. First reconcile the selected original source, data, cache and runtime contracts outside this update;
do not retokenize, regenerate or substitute inputs to make the scene run. Producer/core files are unchanged here.

## Reviewed scene contracts

* **Hook and Frontier:** retain the published per-query arc-width explanation and panel/arrow layout. The passage
  is excluded from gradient training; attention powers many language models. The roadmap distinguishes work
  inside an attention block from changes to access to stored keys and values.
* **Hopfield:** distinguish the continuous softmax update from a subsequent sign readout. Capacity and retrieval
  guarantees have separation/cue assumptions; finite demonstrations and their beta settings are separate cases.
* **Scale:** finite softmax saturation weakens the gradient path. A dominant key need not have probability exactly
  one, and the scaled entropy is a measured range rather than an identical value at every dimension.
* **Heads:** the low-rank linear factors use normalized inputs before RoPE and score scaling. Folding layer-norm
  gain and centring into these factors excludes offset and input-dependent variance. Numerical rank uses a cutoff;
  the 90-percent summary uses squared singular values, not the actual attention operator's rank.
* **Masks:** the saved joint intervention removes both the mask and positional rotations. Its outputs are raw
  logits before output softmax. Full attention alone does not determine an encoder's training or generation
  scheme. The word-swap animation separates its paths and binds connectors to moving tokens.
* **Transformer:** keep original reported outcomes and separate target cohorts. Part 7 counting uses zero-based
  inclusive targets 7–21,405 (21,399 targets), Part 9 neural/mixture uses 24–21,405 (21,382), and this Transformer
  uses 1–21,376 (21,376). These are not a common-target ranking. Checkpoint and final validation use different
  source prefixes; four heads means four per block. No private input fingerprint is needed in display metadata.
* **Cost:** the parameter formulas refer to this architecture with a 4d MLP. Attention's share among attention/MLP
  matrices differs from its share of the whole model. Matrix-FLOP counts exclude normalization, GELU and softmax;
  the causal-half crossover neglects vocabulary projection and is not a total-compute equality.
* **Positions and RoPE:** correct sine/cosine angle addition, finite ALiBi bias and learned-position table limits.
  The signed relative-position identity holds for fixed pre-RoPE queries/keys. Equal-energy cosine references can
  oscillate; they do not prove monotone decay or a learned channel's role.
* **SideBySide:** a finite four-method, three-seed study with three layers and four heads per layer. Checkpoint
  prefixes and final evaluation windows differ. A marked-first-token NoPE construction is an illustration, not a
  demonstrated mechanism in the trained novel model. Finite ALiBi penalties are not a hard attention cutoff.
* **Longer:** fixed-probability competition among equal other logits gives a gap of log(n−1) plus a constant for
  n ≥ 2. The implemented log-n multiplier is a heuristic, not that identity or an extrapolation guarantee.
  Position interventions, adaptation budgets and the fixed evaluation windows must remain distinguishable. The
  training-boundary label sits below the plotted curves; no data are hidden to clear the label.
* **Sinks:** mean attention mass is not selection frequency. Endpoint value norms do not measure a training
  trajectory. Differential coefficients are signed, and every row sums to 1−lambda before later normalization;
  this is neither a probability distribution nor an output amplitude. Copy-position loss alone does not establish
  whole-task equivalence or causal necessity. Conditional entropy differs from realized noncopy loss.
* **Caps:** c-squared scaling is a fixed-layer-input identity, distinct from a full-network intervention. QK-norm
  bounds need nonzero RMS and bounded gains, with epsilon qualifications. A post-hoc probe does not establish how
  the network must have been trained.
* **Induction:** the display stripe uses queries 60–78 predicting copied targets 61–79. It is separate from the
  unchanged cached metric targeting the successor of the earliest earlier matching token. The largest logged
  loss drop is descriptive, not a detected phase change. Matrix composition and Gaussian references are alignment
  probes, not causal tests or p-values; a finite negative probe cannot exclude every copying mechanism.
* **InContext:** plot the saved scatter points without percentile clipping. Distinguish 200 displayed questions
  from the 4,000-prompt evaluation summary. GD's step size is chosen among 59 candidates on that same evaluation
  set. Correlation is not identity or proof of an internal algorithm; separately trained depths are compared to
  reference GD steps, while training curves use changing minibatches.
* **RASP:** the shown sorting test has unique tokens and zero-based ranks. Fixed-depth circuit statements require
  their finite-precision/computability assumptions. RASP-L length generalization is a conjecture under training,
  data-diversity and program assumptions, not an unconditional training guarantee.

## Chinese narration and shared captions

`zh_lines.py` changes only owned narration entries and a Heads phrase, retaining the public Hook/Frontier
corrections and existing prefixes. Dynamic Induction composition branches require their own translation entries;
checking only directly listed voiceover arguments misses those recursively translated fragments.

[`reviewed_caption_delta.json`](reviewed_caption_delta.json) retains the worker's original proposal and its
expected-before conditions. The integration has applied all 74 operations to `videos/ai/ai_text_zh.json`:
53 exact additions, one reviewed exact replacement and 20 appended patterns. Existing unowned entries and
pattern order are preserved. Tests accept either the original proposal base or identical already-applied
values, and reject conflicting values. The older `text_zh_add.json` is unchanged. Caption source integration
does not establish rendered Chinese-output acceptance.

## Validation and inputs

Run the source-contract tests from the repository root:

```bash
python -m unittest discover -s tests -p 'test_ai13_reviewed_source.py'
```

Use the repository's Python 3.12 runtime. These tests inspect actual source expressions and translation contracts
with synthetic fixtures; they do not import scenes, load scientific outcomes, train models, generate narration or
render videos. After source integration, the owner must separately verify the selected scientific provenance and
run output QA. Preserve original outcomes and recipes; do not retrain to conceal scoring or comparison differences.

No scientific producer, shared core module, dependency pin or CI/CD configuration is changed by this worker.

## Problems, with solutions

**1. Why √d.** If the entries of q and k are independent with mean 0 and variances σ_q² and σ_k², show that
Var(q·k) = d σ_q² σ_k². What should the score be divided by?

*Solution.* q·k = Σᵢ qᵢkᵢ. Each term has mean E[qᵢ]E[kᵢ] = 0 and variance E[qᵢ²]E[kᵢ²] = σ_q²σ_k², by independence;
the d terms are independent, so their variances add: d σ_q²σ_k². Dividing by √d σ_q σ_k gives variance one; at
initialization, with unit variances, that is the √d of the formula.

**2. Relative by construction.** Let R_m rotate each pair of a vector by mθⱼ. Show that (R_m q)·(R_n k) depends only
on n − m, and that ALiBi's bias −m_h(i − j) has the same property.

*Solution.* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k. A rotation's transpose is its inverse, R_mᵀ = R_{−m}, and the 2×2 blocks
of one pair commute, so R_{−m} R_n = R_{n−m}: the score is qᵀ R_{n−m} k. ALiBi's bias is a function of i − j alone.
Both are unchanged when the query and key positions are shifted by the same amount.

**3. What a block costs.** Show that a pre-norm block with an MLP of width 4d (no biases on the attention matrices,
as in ours) has 12d² + 9d parameters, and that attention's 2LTd operations per token equal the weights' 24Ld² at
T = 12d.

*Solution.* W_Q, W_K, W_V, W_O: 4d². The MLP: d × 4d and 4d × d weights, 8d², with 4d + d biases. Two layer norms,
a gain and a bias each: 4d. Total 12d² + 9d (for d = 128, 197,760 per block). Each weight costs a multiply and an add
per token, 2 · 12d² per block, 24Ld² in all; equating with 2LTd gives T = 12d: 1,536 for our d = 128, 147,456 for
GPT-3's 12,288.

**4. A place to put nothing.** A head has a sink logit b and n keys with equal scores s. What share of its attention
goes nowhere? For which b is it one half?

*Solution.* The share is e^b / (e^b + n e^s). It is one half when e^b = n e^s, that is b = s + ln n: a sink must
outscore the keys by the log of their number to absorb half the weight.

**5. Temperature.** Show that the modern Hopfield update ξ ← Xᵀ softmax(βXξ) (the rows of X are the stored patterns)
tends to the stored pattern of largest overlap as β → ∞, and to the average pattern as β → 0.

*Solution.* The weights are pᵢ ∝ exp(β xᵢ·ξ). As β → ∞ the ratio pᵢ/pⱼ = exp(β(xᵢ − xⱼ)·ξ) → ∞ whenever xᵢ·ξ >
xⱼ·ξ, so all the weight goes to the largest overlap and the update returns that pattern (the average of the tied
ones, if several tie). As β → 0 every exponent tends to 1, the weights to 1/M, and the update to (1/M) Σᵢ xᵢ.

**6. Gradient descent is attention.** Show that one step of gradient descent from w = 0 on
L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)² predicts ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q) for a query x_q.

*Solution.* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ, so at w = 0 the step gives w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ, and
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q). This is attention without a softmax: the query x_q, the keys xᵢ, the values yᵢ,
scores xᵢ·x_q — the pattern the trained linear-attention layer of chapter fifteen finds.

## 习题与解答

**1. 为什么是根号d。** 设q和k的各个分量相互独立，均值为0，方差分别为σ_q²和σ_k²。证明 Var(q·k) = d σ_q² σ_k²。分数应该除以什么？

*解答。* q·k = Σᵢ qᵢkᵢ。由独立性，每一项的均值是 E[qᵢ]E[kᵢ] = 0，方差是 E[qᵢ²]E[kᵢ²] = σ_q²σ_k²；d个项相互独立，方差相加，得
d σ_q²σ_k²。除以 √d σ_q σ_k，方差就变成1；初始化时方差为1，这就是公式里的根号d。

**2. 天生就是相对的。** 设R_m把向量的每一对分量旋转mθⱼ。证明 (R_m q)·(R_n k) 只依赖于 n − m，并且ALiBi的偏置
−m_h(i − j) 也有同样的性质。

*解答。* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k。旋转的转置就是它的逆，R_mᵀ = R_{−m}；同一对上的2×2旋转块可以交换，所以
R_{−m} R_n = R_{n−m}，分数等于 qᵀ R_{n−m} k。ALiBi的偏置本来就只是 i − j 的函数。把查询和键的位置平移同样的量，两者都不变。

**3. 一个模块的成本。** 证明：MLP宽度为4d的前置归一化模块（注意力矩阵不带偏置，和我们的模型一样）有 12d² + 9d 个参数；
并且注意力每个词元的 2LTd 次运算，在 T = 12d 时等于权重的 24Ld² 次。

*解答。* W_Q、W_K、W_V、W_O：4d²。MLP：d × 4d 和 4d × d 的权重，8d²，外加 4d + d 个偏置。两个层归一化，各有增益和偏置：4d。
合计 12d² + 9d（d = 128 时，每个模块197,760个）。每个权重对每个词元做一次乘法和一次加法，每个模块 2 · 12d²，总共 24Ld²；
令它等于 2LTd，得 T = 12d：我们的d = 128时是1,536，GPT-3的d = 12,288时是147,456。

**4. 一个放“什么都没有”的地方。** 一个头有汇点logit b，以及n个分数都等于s的键。它有多少注意力哪儿也没去？b取多少时是一半？

*解答。* 份额是 e^b / (e^b + n e^s)。当 e^b = n e^s，也就是 b = s + ln n 时，它等于一半：汇点的分数要比那些键高出键数的对数，
才能吸走一半的权重。

**5. 温度。** 证明现代霍普菲尔德更新 ξ ← Xᵀ softmax(βXξ)（X的每一行是一个存储模式）在 β → ∞ 时趋于重叠度最大的存储模式，
在 β → 0 时趋于所有模式的平均。

*解答。* 权重 pᵢ ∝ exp(β xᵢ·ξ)。β → ∞ 时，只要 xᵢ·ξ > xⱼ·ξ，比值 pᵢ/pⱼ = exp(β(xᵢ − xⱼ)·ξ) 就趋于无穷，
所以全部权重都落到重叠度最大的那个模式上，更新返回这个模式（若有几个并列，则返回它们的平均）。β → 0 时，每个指数都趋于1，
权重趋于1/M，更新趋于 (1/M) Σᵢ xᵢ。

**6. 梯度下降就是注意力。** 证明：在 L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)² 上，从 w = 0 出发走一步梯度下降，对查询x_q的预测是
ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q)。

*解答。* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ，所以在 w = 0 处走一步得 w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ，于是
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q)。这就是不带softmax的注意力：查询是x_q，键是xᵢ，值是yᵢ，分数是xᵢ·x_q——正是第15章里训练出来的
线性注意力层自己找到的模式。

## Glossary (new terms of this part)

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
| threshold circuit, TC⁰, NC¹ | 阈值电路，TC⁰，NC¹ |
| hybrid (linear + full attention) | 混合架构（线性注意力加完整注意力） |
