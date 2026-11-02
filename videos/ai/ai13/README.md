# AI, Built — Part 13: Attention as Geometry

Part 13 opens the Transformer act of [the series](../README.md). It develops attention as a learned weighted
average and memory read, then examines heads, masks, cost, position, longer contexts, sinks, induction and
in-context learning. The CPU producer implementations are in `compute.py`.

## Source review and acceptance limits

This worker update contains source and synthetic contract tests. It preserves the existing public Hook/Frontier
geometry and adds reviewed mathematical, measurement and narration qualifications. It does not distribute
scientific datasets, model weights, numerical caches, private QA records or runtime input manifests.

Source tests do not establish rendered acceptance of this public tree. In particular, selected frames inspected
under a different source/input/runtime combination do not transfer a visual acceptance claim to this revision.
Before production, the integration owner must verify compatible original inputs and runtime, review the exact
integrated English and Chinese output, continuously play it, listen to the actual narration and check speech
synchronization at the final resolution. Final rendering, synthesis, assembly and delivery remain separate work.

The reviewed Smoother dependency change obtains the raw observations through `c7.pages()`, Part 7's validated
reader for Part 6's nonoverlapping 1,000-word blocks. It selects Great Expectations (`book == 1400`) and the
`"her"` column in saved block order, then uses zero-based block coordinates. The normalized Gaussian
Nadaraya–Watson estimate and leave-one-out computation are unchanged. This removes an unused GP-fit dependency;
it neither recovers a fitted Gaussian process nor produces a GP posterior.

The full Smoother and Outro clarifications include measurement, algebra and display corrections. Earlier partial
patches in [`source_only_candidates/`](source_only_candidates/README.md) remain historical proposals and must not
be stacked on top of the full update. Newly computed smoother results require their own version and input/source/
runtime provenance. Original saved outcomes and their lineage stay immutable; matching arrays or fields does not
authorize automatic cache-metadata adoption.

Output acceptance is scoped per scene, language and mode, with the exact source, qualified inputs and runtime
recorded. Earlier checks of the other scenes do not transfer acceptance to the new tree. Native endpoints and
selected silent encoded frames cover only the stated samples; they do not establish continuous playback or speech
synchronization. These notes alone do not certify rendered acceptance of an integrated revision; acceptance is
recorded for the exact scene, language, mode, source, inputs and runtime. Audio remains unchecked by these silent
workflows, and no production acceptance is implied.

The existing loader can invoke producers on a missing cache. These source tests deliberately avoid scene/model
imports, training, downloads and scientific generation. Do not import scenes or run a build to discover whether
inputs exist. First reconcile the selected original source, data, cache and runtime contracts. Do not retokenize,
replace original outcomes or substitute inputs to force a comparison. Any explicitly prepared new result must be
versioned and validated separately. The smoother's dependency projection is the only producer change described
here; its numerical body and all other producer computations remain unchanged.

## Reviewed scene contracts

* **Hook and Frontier:** retain the published per-query arc-width explanation and panel/arrow layout. The passage
  is excluded from gradient training; attention powers many language models. The roadmap distinguishes work
  inside an attention block from changes to access to stored keys and values.
* **Smoother:** use the raw validated 1,000-word block observations, not a GP posterior. Coordinates are zero-based.
  Gaussian scores are −distance²/(2h²); finite distant weights can be negligible, while equal weights arise in the
  infinite-bandwidth limit. The three illustrated widths are separate from the 40-bandwidth leave-one-out search.
  Bars are peak-rescaled display heights rather than literal probabilities. RBF-to-dot-product equivalence needs
  matching scale and equal key norms, or a retained key-norm bias; learned affinities need not be GP covariances.
  Query guides stay within their own axes so the block caption remains unobstructed.
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

* **Outro:** distinguish a continuous Hopfield read from the thumbnail's sign readout, initial score-variance
  scaling from a universal saturation guarantee, and a sink's null option from an output gate. Mini-plots retain
  the full raw position range, signed differential coefficients and the maxima of both repeat-loss curves. The
  specified block-cost convention, score-target cohort and conditional depth statements remain qualified. Recap
  captions use explicit hard line breaks; caption formatting does not change the scientific values.

## Chinese narration and shared captions

`zh_lines.py` changes only owned narration entries and a Heads phrase, retaining the public Hook/Frontier
corrections and existing prefixes. Dynamic Induction composition branches require their own translation entries;
checking only directly listed voiceover arguments misses those recursively translated fragments. The full
Smoother/Outro extension contributes six further owned narration additions. Preserve all other entries, existing
prefixes and phrases; a complete capture-context table is evidence, not a wholesale integration replacement.

[`reviewed_caption_delta.json`](reviewed_caption_delta.json) retains the worker's original proposal and its
expected-before conditions. The integration has applied all 74 operations to `videos/ai/ai_text_zh.json`:
53 exact additions, one reviewed exact replacement and 20 appended patterns. Existing unowned entries and
pattern order are preserved. Tests accept either the original proposal base or identical already-applied
values, and reject conflicting values. The older `text_zh_add.json` is unchanged. Caption source integration
does not establish rendered Chinese-output acceptance.

The additional Smoother/Outro caption delta—12 exact strings and one pattern—is separate from those 74 operations;
the earlier proposal file does not include it. Reconcile that delta independently against the selected shared
table, preserving other parts' entries and regex order. A process-local QA overlay does not update the repository
table. Record source integration and exact bilingual-output QA separately.

## Validation and inputs

Run the source-contract tests from the repository root:

```bash
python -m unittest discover -s tests -p 'test_ai13_reviewed_source.py'
```

Use the repository's Python 3.12 runtime. These tests inspect actual source expressions and translation contracts
with synthetic fixtures; they do not import scenes, load scientific outcomes, train models, generate narration or
render videos. After source integration, the owner must separately verify the selected scientific provenance and
run output QA. Preserve original outcomes and recipes; do not retrain to conceal scoring or comparison differences.

The Smoother change replaces the unused `c7.load("gp")` dependency with the raw `c7.pages()` projection. It does
not change the Gaussian-weight normalization, query, illustrated bandwidths, 40-point leave-one-out search, or any
other producer's mathematics. No fitted GP is manufactured and no original scientific payload or generation
metadata is rewritten. Shared core modules, dependency pins and CI/CD configuration are unchanged.

## Problems, with solutions

**1. Why √d.** If the entries of q and k are independent with mean 0 and variances σ_q² and σ_k², show that
Var(q·k) = d σ_q² σ_k². What should the score be divided by?

*Solution.* q·k = Σᵢ qᵢkᵢ. Each term has mean E[qᵢ]E[kᵢ] = 0 and variance E[qᵢ²]E[kᵢ²] = σ_q²σ_k², by independence;
the d terms are independent, so their variances add: d σ_q²σ_k². Dividing by √d σ_q σ_k gives variance one; at
initialization, with unit variances, that is the √d of the formula.

**2. Relative by construction.** Fix the unrotated vectors q and k and each pair's frequency θⱼ. Let R_m rotate
each pair by mθⱼ. Show that the explicit position dependence of (R_m q)·(R_n k), with q and k held fixed, is only
through n − m. Show that ALiBi's bias −m_h(i − j), with fixed slope m_h, also depends only on an offset.

*Solution.* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k. A rotation's transpose is its inverse, R_mᵀ = R_{−m}, and rotations
of the same pair commute: R_{−m} R_n = R_{n−m}. The score is qᵀ R_{n−m} k. ALiBi's bias is a function of i − j.
Both expressions are unchanged by a common position shift when their unrotated vectors or slope remain fixed.
This does not assert that the hidden representations or final attention weights of a trained network depend only
on relative position.

**3. What a block costs.** For our bias-free QKVO, biased MLP of width 4d and two affine LayerNorms, show
12d² + 9d parameters per block. In the dominant causal-half matrix-FLOP convention, show that attention's 2LTd
FLOPs per token equal the leading linear-map term 24Ld² at T = 12d. Omit vocabulary projection and elementwise work.

*Solution.* W_Q, W_K, W_V, W_O contribute 4d². The MLP has 8d² weights and 4d + d biases. Two LayerNorms have
gain and bias vectors totaling 4d. Thus the block has 12d² + 9d parameters: 197,760 at d = 128. Counting a multiply
and add per matrix weight gives the leading linear-map term 24Ld² per token. Equating the two stated leading
matrix terms gives 2LTd = 24Ld², hence T = 12d: 1,536 for d = 128 and 147,456 for GPT-3's d = 12,288.
This convention omits vocabulary projection, normalization, activation, softmax, bias additions and lower-order
terms; it is not an equality of total model computation.

**4. A place to put nothing.** A head has a sink logit b and n keys with equal scores s. What share of its attention
goes nowhere? For which b is it one half?

*Solution.* The share is e^b / (e^b + n e^s). It is one half when e^b = n e^s, that is b = s + ln n: a sink must
outscore the keys by the log of their number to absorb half the weight.

**5. Temperature.** Fix a finite matrix X of stored patterns and the cue ξ for one continuous update
ξ_new = Xᵀ softmax(βXξ). Show that β → ∞ returns the uniquely largest-overlap pattern when it is unique; ties
give the average of the maximizing patterns. Show that β → 0 gives the average of all patterns. Apply no sign readout.

*Solution.* The weights are pᵢ ∝ exp(β xᵢ·ξ). For a unique maximum, every smaller-overlap weight vanishes relative
to its weight as β → ∞. If r patterns tie for the maximum, their identical exponents give each limiting weight
1/r, with all other weights tending to zero. The continuous result is their arithmetic mean. As β → 0 every
exponent tends to 1, so the update is (1/M) Σᵢ xᵢ. These are limits of one continuous update at a fixed cue, not
claims about a subsequent sign readout, iterated attractors or retrieval accuracy.

**6. A gradient step as linear attention.** Show that one step of gradient descent from w = 0 on
L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)² predicts ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q) for a query x_q.

*Solution.* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ. At w = 0, w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ, so
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q). This has an unnormalized dot-product linear-attention form: query x_q,
keys xᵢ, and scaled values (η/N)yᵢ. It uses no softmax, and its coefficients can be signed. This algebraic identity
alone does not show that a trained attention layer implements gradient descent internally.

## 习题与解答

**1. 为什么是根号d。** 设q和k的各个分量相互独立，均值为0，方差分别为σ_q²和σ_k²。证明 Var(q·k) = d σ_q² σ_k²。分数应该除以什么？

*解答。* q·k = Σᵢ qᵢkᵢ。由独立性，每一项的均值是 E[qᵢ]E[kᵢ] = 0，方差是 E[qᵢ²]E[kᵢ²] = σ_q²σ_k²；d个项相互独立，方差相加，得
d σ_q²σ_k²。除以 √d σ_q σ_k，方差就变成1；初始化时方差为1，这就是公式里的根号d。

**2. 天生就是相对的。** 固定旋转前的向量q、k和每对分量的频率θⱼ。设R_m把每对旋转mθⱼ。证明：保持q、k不变时，
(R_m q)·(R_n k)的显式位置依赖只通过n − m；固定斜率m_h时，ALiBi偏置−m_h(i − j)也只依赖位置差。

*解答。* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k。旋转的转置是其逆，R_mᵀ = R_{−m}；同一对的旋转可交换，
R_{−m} R_n = R_{n−m}，因此分数为qᵀ R_{n−m} k。ALiBi偏置是i − j的函数。保持旋转前向量或斜率不变，同时平移两个位置，
这两个表达式不变。这不表示训练网络的隐表示或最终注意力权重只依赖相对位置。

**3. 一个模块的成本。** 对我们的无偏置QKVO、带偏置4d宽MLP和两个仿射LayerNorm，证明每个模块有12d² + 9d个参数。
只按主导的因果半矩阵FLOP口径，证明注意力每词元的2LTd FLOP在T = 12d时等于主要线性映射项24Ld²；忽略词表投影和逐元素运算。

*解答。* W_Q、W_K、W_V、W_O贡献4d²。MLP有8d²个权重和4d + d个偏置。两个LayerNorm的增益与偏置合计4d。
因此每块有12d² + 9d个参数，d = 128时为197,760。按每个矩阵权重一次乘法加一次加法，主要线性映射每词元共24Ld² FLOP。
令给定的两个主导矩阵项相等，2LTd = 24Ld²，得T = 12d：d = 128时为1,536，GPT-3的d = 12,288时为147,456。
这个口径省略词表投影、归一化、激活、softmax、偏置加法和低阶项，不表示模型总计算量相等。

**4. 一个放“什么都没有”的地方。** 一个头有汇点logit b，以及n个分数都等于s的键。它有多少注意力哪儿也没去？b取多少时是一半？

*解答。* 份额是 e^b / (e^b + n e^s)。当 e^b = n e^s，也就是 b = s + ln n 时，它等于一半：汇点的分数要比那些键高出键数的对数，
才能吸走一半的权重。

**5. 温度。** 固定有限个存储模式组成的矩阵X和本次更新的查询ξ。对一次连续更新ξ_new = Xᵀ softmax(βXξ)，证明：
β → ∞时，若最大重叠模式唯一，就返回该模式；若并列，就返回所有最大者的平均。β → 0时返回全部模式的平均。此处不作符号读出。

*解答。* 权重pᵢ ∝ exp(β xᵢ·ξ)。最大值唯一时，β → ∞使其他项的权重相对它趋于零。若r个模式并列最大，它们的指数相同，
各自的极限权重为1/r，其他模式的权重趋于零；连续输出为这些最大者的算术平均。β → 0时，每个指数趋于1，输出为(1/M) Σᵢ xᵢ。
这是固定查询下的一次连续更新极限，不是后续符号读出、迭代吸引点或召回准确率的结论。

**6. 把一次梯度步写成线性注意力。** 在L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)²上，从w = 0出发走一步梯度下降，证明对查询x_q的预测为
ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q)。

*解答。* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ。在w = 0处，w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ，因此
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q)。式子具有不带softmax的点积线性注意力形式：查询为x_q、键为xᵢ、缩放后的值为(η/N)yᵢ。
系数可以有正有负。这个代数恒等式本身不能证明训练后的注意力层在内部实现了梯度下降。

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
