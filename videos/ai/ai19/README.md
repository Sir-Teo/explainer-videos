# AI, Built — Part 19: Inference

Part 19 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)); the last part of Act III, the Transformer Era. How a trained model is run for
millions of people: why reading a prompt and writing an answer are different problems on the roofline, what the
key-value cache costs, how a server batches, schedules and pages, how speculative decoding writes several tokens per
pass and stays exact, how weights, activations and caches are rounded to eight, four and three bits, how
FlashAttention avoids its table, and how decoding is constrained to a format. Everything is measured on this
computer, on the series' own models: the novels model (`explainer.ai.novels`) on an inference engine written for this
part (`engine.py`), and Part 13's character transformer. Two drafters are trained here, and their training is
replayed on screen; so is the learning of a rotation, SpinQuant-style.

* **One token at a time.** Writing a token reads every weight: tokens per second ≤ bandwidth / bytes (an H100 and
  Llama 3.1 70B, published figures); the chip's arithmetic almost idle. How we got here, 2017–2026: the key-value
  cache, multi-query attention (Shazeer 2019), GPT-3 sold by the token, FlashAttention, Orca, speculative decoding
  and GPTQ (2022), llama.cpp and vLLM (2023), MLA and disaggregated serving (2024), gpt-oss in MXFP4 and DeepSeek's
  sparse attention (2025); OpenAI's price for a GPT-3-class model, 2021–2024.
* **1. Prefill and decode.** FLOPs 2N per token, bytes 2N per pass, intensity B for a decode batch and T for a
  prompt; H100's ridge (Part 17). Measured: an 805 MB stack of weight matrices multiplied by batches of 1–512
  vectors (GEMV becoming GEMM) against the roofline's floor; the novels model's prefill and decode throughput.
* **2. The key-value cache, priced.** 2 L n_h d_h per token (MHA), 2 L n_g d_h (GQA, Ainslie et al. 2023), L (d_c +
  d_R) (MLA, DeepSeek-V2 2024); Llama 3.1 70B, DeepSeek-V3 and gpt-oss-120b from their configurations; the cache
  against context length and against the weights; measured decode time against the bytes a step reads.
* **3. Batching: speed against cost.** The measured trade between speed per conversation and total throughput; a
  roofline model of Llama 3.1 8B on an H100, memory capping the batch, at the 2 USD per GPU-hour DeepSeek costed its
  service at (DeepSeek-V3.2 2025); cost per million tokens against speed, at 1k–128k context; Pope et al. (2022).
* **4. Continuous batching.** Static batches against iteration-level scheduling (Orca, Yu et al. 2022), simulated
  with this machine's fitted step costs: a Gantt chart of slots, throughput, time to first token; prefill stalls and
  chunked prefill (Sarathi-Serve 2024); prefill and decode on separate workers (Splitwise, DistServe 2024;
  DeepSeek-V3's deployment; Mooncake).
* **5. Pages and shared prefixes.** The cache's memory reserved at the maximum, contiguous first-fit, or paged
  (vLLM, Kwon et al. 2023), simulated: memory holding tokens, conversations at once; waste against page size;
  prefix caching on multi-turn chats (SGLang 2023; DeepSeek's context caching 2024) and its measured prefill saving.
* **6. Guess ahead, check at once.** Blockwise parallel decoding (Stern, Shazeer & Uszkoreit 2018); speculative
  sampling (Leviathan, Kalman & Matias 2022; Chen et al. 2023): the rule min(1, p/q) and the leftover max(0, p − q),
  proved exact; checked on Part 13's transformer (200,000 samples) and on the novels model's next two tokens
  (60,000 runs; total variation against direct sampling and against unchecked drafts).
* **7. Drafters.** The expected tokens per pass (1 − α^{k+1})/(1 − α) and the speed-up with draft cost c, derived; a
  two-layer drafter and an EAGLE-style head (Li et al. 2024) trained here, acceptance replayed through training;
  speculative runs on held-out text: tokens per pass against the formula, acceptance by depth, greedy; time per token
  on this machine; Medusa, EAGLE-3, DeepSeek-V3's MTP module (Part 18).
* **8. Rounding error.** E[e²] = Δ²/12 derived (Bennett 1948), 6 dB a bit; checked on all the novels model's block
  weights; one matrix's histogram with per-tensor and per-row levels; loss against bits for a scale per tensor, row,
  64 and 32 weights.
* **9. Outliers and SmoothQuant.** LLM.int8()'s emergent outliers (Dettmers et al. 2022); our model's channel
  ranges; SmoothQuant (Xiao et al. 2022) derived; W8A8, W8A6, W8A4: plain, smoothed, and LLM.int8()-style channels
  kept aside.
* **10. GPTQ, from Optimal Brain Surgeon.** The layer-wise objective with H = XXᵀ; Optimal Brain Damage (LeCun,
  Denker & Solla 1990) and Optimal Brain Surgeon (Hassibi & Stork 1993) derived with a Lagrange multiplier; Optimal
  Brain Compression (2022) and GPTQ (Frantar et al. 2022): one row's column-by-column update animated; AWQ (Lin et
  al. 2023); all three at 4 and 3 bits on three calibration sets.
* **11. Rotations: QuaRot and SpinQuant.** RMSNorm commutes with rotations; computational invariance (QuaRot,
  Ashkboos et al. 2024), checked; a Hadamard rotation flattening one token's activations; W4A4 plain, smoothed,
  Hadamard, random rotations, and a rotation learned through the Cayley map (SpinQuant, Liu et al. 2024), its
  training replayed.
* **12. Four-bit floats: MXFP4 and NVFP4.** E2M1 (Part 17); MXFP4 (OCP 2023) bit by bit on 32 of our weights: the
  E8M0 shared exponent, the codes, clamping above 6; NVFP4 (NVIDIA 2025): blocks of 16, an E4M3 scale and a tensor
  scale; the model in each format against 4-bit integers with the same scales; gpt-oss-120b's 60.8 GiB recomputed
  from its model card; Kimi K3's MXFP4 weights (Part 18).
* **13. The cache in fewer bits.** Keys' outlier channels against values; KIVI (Liu et al. 2024): keys per channel,
  values per token; the cache at 8 (integer, FP8), 4, 3 and 2 bits, per token, KIVI, and Hadamard-rotated.
* **14. FlashAttention.** The standard method's HBM traffic; the online softmax (Milakov & Gimelshein 2018) derived
  and run on one real query of Part 13's transformer; tiles (Dao et al. 2022), checked exact on Part 13's attention;
  the IO complexity Θ(T²d²/M) derived and counted by running the loops, for an H100's shared memory;
  FlashAttention-2 (2023) and -3 (2024).
* **15. Attention at serve time.** Flash-Decoding (Dao, Haziza, Massa & Sizov 2023): split-KV with log-sum-exp
  combination, checked; occupancy of an H100 at batch 1; sliding windows (gpt-oss, Gemma 3) and DeepSeek's sparse
  attention (V3.2): cache read per decode step against context; a window measured on our model.
* **16. Constrained decoding.** A record format the novels model never writes unprompted; the pattern compiled to an
  automaton and a token index (Outlines, Willard & Louf 2023); the constrained samples checked and the mask timed;
  XGrammar (2024); masking distorts the distribution (Park et al. 2024), shown on Part 13's character model.
* **17. The frontier, late 2026.** Thinking longer (DeepSeek-R1-0528: 12k → 23k tokens per AIME question) costed with
  chapter 3's model; prices per token over time (OpenAI list prices; Epoch AI 2025); bandwidth bounds on laptops
  and GPUs (Apple M5, M5 Max, H100) for on-device models (Apple's 2-bit model, gpt-oss-20b, Llama 3.1 in 4 bits),
  and our model's measured speed against its bound; Rubin CPX.
* **Recap**, where this comes back (Parts 20, 21, 28, 29, 30, 31; Part 30's superposition picture), the problem set,
  Part 20's teaser, references.

Run from the repo root:

```
python tools/make.py ai19                 # everything below, in order; rerun after an interruption to carry on
```

or step by step:

```
python -m explainer.ai.novels             # the series' novels model (about an hour, cached; Parts 14, 27, 31 use it)
python -m videos.ai.ai13.compute tf       # Part 13's character transformer
python -m videos.ai.ai30.compute superposition   # Part 30's toy model (a minute), for the recap's picture
python -m videos.ai.ai19.compute          # everything in this part (about 1.5-2 CPU-hours; two drafters train)
python tools/build.py ai19                # English
python tools/build.py ai19 --lang zh      # Chinese
```

Every step resumes: each result is cached as soon as it is computed (`.cache/ai19/`), the drafters checkpoint every
50 steps, and the long sweeps (rounding, GPTQ, rotations, the cache) save each piece as it finishes. Everything is
seeded. Timings use one thread and `engine.interleaved_min` (each configuration timed in turn, shuffled, many rounds,
the fastest kept), so a busy machine slows them less; still, run the compute step on a quiet computer if you can. The
narration is written over the data and follows your machine's numbers, in both languages.

Code: `engine.py` (the inference engine: a key-value cache, prefill and batched decode, hooks for quantized caches
and activations; checked against the model's own forward), `serve.py` (the server simulations), `spec.py`
(drafters, speculative decoding, the exactness test), `quant.py` (rounding, GPTQ, AWQ, SmoothQuant, rotations),
`formats.py` (MXFP4 and NVFP4 bit by bit), `attn.py` (online softmax, tiled attention, IO counts, split-KV),
`grammar.py` (the automaton and its token index), `facts.py` (every published number, with its source).

References: Hennessy & Patterson (2017); Gray & Neuhoff (1998); Pope et al. (2022); Yu et al. (2022); Kwon et al.
(2023); Zheng et al. (2023); Agrawal et al. (2024); Zhong et al. (2024); Patel et al. (2024); Qin et al. (2024);
Shazeer (2019); Ainslie et al. (2023); DeepSeek-AI (2024a, 2024b, 2025a, 2025b); Gemma Team (2025); OpenAI (2025);
Stern, Shazeer & Uszkoreit (2018); Leviathan, Kalman & Matias (2023); Chen et al. (2023); Cai et al. (2024); Li et
al. (2024, 2025); Bennett (1948); LeCun, Denker & Solla (1990); Hassibi & Stork (1993); Frantar & Alistarh (2022);
Dettmers et al. (2022); Frantar et al. (2023); Xiao et al. (2023); Lin et al. (2024); Ashkboos et al. (2024); Liu et
al. (2025); Rouhani et al. (2023); NVIDIA (2025); Liu et al. (2024); Milakov & Gimelshein (2018); Dao et al. (2022);
Dao (2023); Shah et al. (2024); Dao, Haziza, Massa & Sizov (2023); Willard & Louf (2023); Dong et al. (2025); Park
et al. (2024); Cottier et al. (2025); Apple (2025).

## Problems, with solutions

**1. Tokens per pass.** With each draft accepted independently with probability α, show that a pass writes
(1 − α^{k+1})/(1 − α) tokens on average. For α = 0.8 and a draft step costing c = 0.05 passes, which k is fastest?

*Solution.* The pass writes token i + 1 (i = 0 … k) exactly when the first i drafts are all accepted, which has
probability α^i (the i = 0 term is the big model's own token, always written). By linearity, E[tokens] = Σ_{i=0}^{k}
α^i = (1 − α^{k+1})/(1 − α). A round costs one pass plus k draft steps, 1 + kc, so the speed-up is
S(k) = (1 − α^{k+1}) / ((1 − α)(1 + kc)). With α = 0.8, c = 0.05: S(1) = 1.71, S(2) = 2.22, S(3) = 2.57, S(4) = 2.80,
S(5) = 2.95, S(6) = 3.04, S(7) = 3.08, S(8) = 3.09, S(9) = 3.08: k = 8 is fastest, though anything from 6 to 10 is
within 2%.

**2. Exactness.** Show that speculative sampling outputs x with probability exactly p(x), and that a draft is
accepted with probability 1 − TV(p, q).

*Solution.* x is output if it is drafted and accepted, probability q(x) min(1, p(x)/q(x)) = min(p(x), q(x)), or if
some draft is rejected and x is resampled from r(x) = (p(x) − min(p(x), q(x)))/Z with Z = Σ_y (p(y) − min(p(y), q(y))).
The rejection probability is 1 − Σ_y min(p(y), q(y)) = Z, because Σ_y p(y) = 1. So P(x) = min(p, q) + Z · (p − min(p,
q))/Z = p(x). The acceptance probability is β = Σ_y min(p(y), q(y)); since min(a, b) = (a + b − |a − b|)/2 and p and q
both sum to one, β = 1 − ½ Σ_y |p(y) − q(y)| = 1 − TV(p, q).

**3. Rounding error.** Derive E[e²] = Δ²/12 for rounding to a grid of step Δ, and show that one more bit lowers the
error by 10 log₁₀ 4 ≈ 6.02 dB.

*Solution.* If the value is spread smoothly over many steps, its position within its step is uniform, so the error
e is uniform on [−Δ/2, Δ/2]: E[e²] = (1/Δ) ∫_{−Δ/2}^{Δ/2} e² de = (1/Δ)(2/3)(Δ/2)³ = Δ²/12. With b bits over a fixed
range, Δ ∝ 1/(2^{b−1} − 1) ≈ 2^{1−b}: one more bit halves Δ and divides E[e²] by 4, which is 10 log₁₀ 4 = 6.02 dB.

**4. A cache.** A model has 48 layers and 8 key-value heads of 128 in 16 bits. How many bytes does its cache keep per
token, and at what context does one conversation's cache weigh 60 GB?

*Solution.* Keys and values: 2 × 48 × 8 × 128 numbers × 2 bytes = 196,608 bytes, 192 KiB, per token. 60 × 10⁹ /
196,608 ≈ 305,000 tokens. With every one of, say, 40 query heads keeping its own key and value it would be five
times as much, and the cache would weigh 60 GB at about 61,000 tokens.

**5. Optimal Brain Surgeon.** Minimize ½ δᵀHδ subject to e_qᵀδ = ŵ_q − w_q: derive the update and the error it leaves.

*Solution.* The Lagrangian ½ δᵀHδ − λ(e_qᵀδ − (ŵ_q − w_q)) has gradient Hδ − λe_q = 0, so δ = λH⁻¹e_q. The constraint
gives λ e_qᵀH⁻¹e_q = λ[H⁻¹]_qq = ŵ_q − w_q, so λ = (ŵ_q − w_q)/[H⁻¹]_qq and δ = ((ŵ_q − w_q)/[H⁻¹]_qq) H⁻¹e_q. The
error is ½ δᵀHδ = ½ λ² e_qᵀH⁻¹HH⁻¹e_q = ½ λ²[H⁻¹]_qq = (w_q − ŵ_q)² / (2[H⁻¹]_qq). GPTQ applies this column by column,
in a fixed order, with H⁻¹'s rows read off one Cholesky factor.

**6. Combining two chunks.** Two chunks of keys give (m₁, ℓ₁, o₁) and (m₂, ℓ₂, o₂), where m is a chunk's largest score,
ℓ = Σ e^{s_j − m} and o = Σ e^{s_j − m} v_j over the chunk. Combine them into exact attention.

*Solution.* With M = max(m₁, m₂), the full sums are L = e^{m₁−M} ℓ₁ + e^{m₂−M} ℓ₂ and O = e^{m₁−M} o₁ + e^{m₂−M} o₂,
because e^{s_j − M} = e^{s_j − m_i} e^{m_i − M} for every j in chunk i; attention is O/L. The rule is symmetric in the
two chunks and associative (combining a third with the result gives the same M, L and O as any other order), so the
chunks can be processed in parallel and reduced in any order: Flash-Decoding. Each e^{m_i − M} ≤ 1, so nothing
overflows.

## 习题与解答

**1. 每次前向传播写出的词元数。** 设每个草稿以概率 α 被独立接受，证明一次前向传播平均写出 (1 − α^{k+1})/(1 − α) 个词元。若
α = 0.8，起草一步的代价 c = 0.05 次前向传播，k 取多少最快？

*解答。* 当且仅当前 i 个草稿全部被接受时（概率 α^i），这次前向传播写出第 i + 1 个词元（i = 0 … k；i = 0 那一项是大模型自己的
词元，总会写出）。由期望的线性，平均词元数 = Σ_{i=0}^{k} α^i = (1 − α^{k+1})/(1 − α)。一轮的代价是一次前向传播加 k 步起草，
即 1 + kc，所以加速比 S(k) = (1 − α^{k+1}) / ((1 − α)(1 + kc))。α = 0.8，c = 0.05 时：S(1) = 1.71，S(2) = 2.22，
S(3) = 2.57，S(4) = 2.80，S(5) = 2.95，S(6) = 3.04，S(7) = 3.08，S(8) = 3.09，S(9) = 3.08：k = 8 最快，不过 6 到 10 都在 2% 之内。

**2. 精确性。** 证明推测采样输出 x 的概率恰好是 p(x)，并证明一个草稿被接受的概率是 1 − TV(p, q)。

*解答。* x 被输出有两种途径：被起草并被接受，概率是 q(x) min(1, p(x)/q(x)) = min(p(x), q(x))；或者某个草稿被拒绝，再从
r(x) = (p(x) − min(p(x), q(x)))/Z 中重采样出 x，其中 Z = Σ_y (p(y) − min(p(y), q(y)))。拒绝的概率是
1 − Σ_y min(p(y), q(y)) = Z，因为 Σ_y p(y) = 1。所以 P(x) = min(p, q) + Z · (p − min(p, q))/Z = p(x)。接受的概率是
β = Σ_y min(p(y), q(y))；由 min(a, b) = (a + b − |a − b|)/2，且 p、q 各自求和为 1，得 β = 1 − ½ Σ_y |p(y) − q(y)| = 1 − TV(p, q)。

**3. 舍入误差。** 对步长为 Δ 的网格做舍入，推导 E[e²] = Δ²/12，并证明多一个比特让误差降低 10 log₁₀ 4 ≈ 6.02 分贝。

*解答。* 若数值平滑地分布在许多个步长上，它在所在步长里的位置是均匀的，误差 e 在 [−Δ/2, Δ/2] 上均匀分布：
E[e²] = (1/Δ) ∫_{−Δ/2}^{Δ/2} e² de = (1/Δ)(2/3)(Δ/2)³ = Δ²/12。范围固定时，b 个比特给出 Δ ∝ 1/(2^{b−1} − 1) ≈ 2^{1−b}：多一个
比特，Δ 减半，E[e²] 除以 4，也就是 10 log₁₀ 4 = 6.02 分贝。

**4. 一个缓存。** 一个模型有 48 层，8 个键值头，每个 128 维，用 16 比特存储。每个词元的缓存有多少字节？上下文多长时，一段对话的
缓存重达 60 GB？

*解答。* 键和值：2 × 48 × 8 × 128 个数 × 2 字节 = 196608 字节，即每个词元 192 KiB。60 × 10⁹ / 196608 ≈ 30.5 万个词元。如果比如
40 个查询头每个都有自己的键和值，缓存会是 5 倍，大约 6.1 万个词元就达到 60 GB。

**5. 最优脑外科。** 在约束 e_qᵀδ = ŵ_q − w_q 下最小化 ½ δᵀHδ：推导更新量，以及它留下的误差。

*解答。* 拉格朗日函数 ½ δᵀHδ − λ(e_qᵀδ − (ŵ_q − w_q)) 的梯度为 Hδ − λe_q = 0，所以 δ = λH⁻¹e_q。代入约束得
λ e_qᵀH⁻¹e_q = λ[H⁻¹]_qq = ŵ_q − w_q，于是 λ = (ŵ_q − w_q)/[H⁻¹]_qq，δ = ((ŵ_q − w_q)/[H⁻¹]_qq) H⁻¹e_q。误差是
½ δᵀHδ = ½ λ² e_qᵀH⁻¹HH⁻¹e_q = ½ λ²[H⁻¹]_qq = (w_q − ŵ_q)² / (2[H⁻¹]_qq)。GPTQ 按固定的顺序逐列使用这个更新，H⁻¹ 的各行
从一次 Cholesky 分解中读出。

**6. 合并两段。** 两段键分别给出 (m₁, ℓ₁, o₁) 和 (m₂, ℓ₂, o₂)，其中 m 是这一段里最大的分数，ℓ = Σ e^{s_j − m}，
o = Σ e^{s_j − m} v_j（对这一段求和）。把它们合并成精确的注意力。

*解答。* 令 M = max(m₁, m₂)，完整的和是 L = e^{m₁−M} ℓ₁ + e^{m₂−M} ℓ₂，O = e^{m₁−M} o₁ + e^{m₂−M} o₂，因为对第 i 段里的每个 j，
e^{s_j − M} = e^{s_j − m_i} e^{m_i − M}；注意力就是 O/L。这个规则对两段是对称的，也满足结合律（再合并第三段，无论什么顺序，
得到的 M、L、O 都一样），所以各段可以并行计算，再以任意顺序归约：这就是 Flash-Decoding。每个 e^{m_i − M} ≤ 1，不会溢出。

## Glossary (for AI_ZH_GUIDE.md)

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
