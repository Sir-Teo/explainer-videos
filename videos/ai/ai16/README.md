# AI, Built — Part 16: Sparsity

Part 16 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)).
Using only some of a model at a time: mixtures of experts, mixture-of-depths, attention that reads only some of the
past, and sparse weights and activations. A hook, sixteen chapters and an outro, about 50 minutes, in English and
Chinese. Every model shown training is trained here, on a CPU, at equal active parameters and FLOPs, with several
seeds and the spread shown; the computed results are listed under [Results](#results).

## Outline

* **A few experts at a time (hook).** DeepSeek-V3's 256 experts per layer, 8 and a shared one lighting up for each
  word; Kimi K3 (July 2026): 896 experts, 16 chosen and 2 shared. How we got here, in three threads: experts (1991 →
  Shazeer 2017 → GShard, Switch → Mixtral → DeepSeek-V3 → Kimi K3), attention (Sparse Transformer 2019, Longformer and
  BigBird 2020, sliding windows, NSA/MoBA/DSA 2025, DeepSeek-V4 2026) and weights (Optimal Brain Damage 1990, Han et
  al. 2015, lottery tickets 2018, 2:4 on the A100 2020, SparseGPT and Wanda 2023). Objectives.
* **1. Competing experts, 1991.** The mixture of experts defined (Jacobs, Jordan, Nowlan & Hinton 1991). The
  cooperative loss against the competitive one, derived: the competitive gradient is each expert's own error weighted
  by its posterior responsibility h_i (Part 7's EM). Computed: four straight-line experts and a softmax gate on a
  three-regime curve, trained both ways (three seeds), the gates replayed through training. Jordan & Jacobs (1994);
  Shazeer et al. (2017): noisy top-k gating, KeepTopK, 137 billion parameters.
* **2. Top-k gates and the router's gradient.** The layer (Mixtral's gate). The router's gradient derived:
  ∂L/∂s_j = g_j (u_j − ū) for chosen experts, 0 otherwise. Checked by finite differences and autograd (float64), and
  on our own MoE layer's router. Pause and predict: top-1 with a renormalized gate learns nothing (Switch keeps p_i).
* **3. A mixture, trained.** Our character transformer (Part 13's, d = 64, 2 blocks, 64 characters of context):
  dense with the mixture's arithmetic (hidden 256), the mixture (8 experts of 128, 2 per character, DeepSeek-V3's
  router), dense with the mixture's parameters (hidden 1,024); three seeds each, curves with spread; the routing
  replayed through training; wall-clock per step on one core (sparse arithmetic is not free time).
* **4. Collapse, and Switch's loss.** Training without balancing: each expert's share of the tokens, replayed; the
  rich-get-richer loop. Shazeer's importance loss (CV²). Switch's auxiliary loss derived: f_i counted, P_i
  differentiable, E Σ f_i P_i ≥ 1 by Cauchy–Schwarz when f = P, ∂/∂P_i = αE f_i. GShard; ST-MoE's z-loss. Computed:
  with and without the loss (three seeds).
* **5. Balancing without a loss.** DeepSeek's auxiliary-loss-free bias (Wang et al. 2024): the bias chooses, never
  weighs. DeepSeek-V3's router exactly (sigmoid scores, normalized gates, a shared expert; γ = 0.001 for 14.3T tokens,
  α = 0.0001 sequence-wise, no token dropping). The three rules replayed side by side; the biases through training;
  a table of busiest expert, starved experts, MaxVio and held-out bits.
* **6. Fine-grained and shared experts.** DeepSeekMoE (Dai et al. 2024) and its reported results; the number of
  teams, (N/k)^k ≤ C(N,k) ≤ (eN/k)^k; computed: coarse (2 of 8), fine (8 of 32) and fine + shared (1 + 7 of 31)
  at equal active and total parameters (two seeds).
* **7. Capacity and dropped tokens.** C = ⌈c·kN/E⌉; GShard and Switch. Computed: tokens dropped and bits lost against
  the capacity factor for each trained router; training with c = 1. Expert-choice routing (Zhou et al. 2022).
* **8. Experts across chips.** Expert parallelism and the all-to-all (link: Part 18). DeepSeek-V3's traffic per token
  per MoE layer (FP8 out, BF16 back) against its experts' FLOPs: 2h FLOPs per byte against the GPU's ~40,000 per
  InfiniBand byte; node-limited routing, DualPipe. Computed: our routers placed on four simulated GPUs, the busiest
  GPU's share (every GPU waits for it).
* **9. Counting parameters, and upcycling.** DeepSeek-V3's 671B and 37B derived from its config.json, matrix by
  matrix; drawn to scale; Mixtral's 46.7B and 12.9B; the 14B multi-token-prediction module. Sparse upcycling
  (Komatsuzaki et al. 2022) and why it starts exact; computed: a dense model upcycled halfway against it kept dense
  and against a mixture from scratch (two seeds), with training compute.
* **10. What experts learn.** Where each character's tokens go (last block); mutual information between the chosen
  expert and the previous, current and next character against shuffled chance (three seeds, both blocks); fine
  experts; Mixtral's and OLMoE's analyses. The scoreboard, with this part's rows.
* **11. Mixture-of-depths.** Raposo et al. (2024): a router per block takes the top 12.5%. Compute derived (an eighth
  of the matrices, a sixty-fourth of the scores). Computed: compute per character against held-out bits for dense
  models of 2, 3 and 4 blocks and routed models at 50% and 12.5% (two seeds); which characters it routes; the causal
  problem (top-k peeks at later tokens) and the router deciding alone.
* **12. How sparse is attention?** Fixed patterns: strided (Child et al. 2019), window + global (Longformer), + random
  (BigBird), sliding windows (Mistral 7B). In Part 13's transformer: the attention mass held by the top k keys; bits
  per character with k keys chosen by score or as a window.
* **13. Sparse attention by design.** One real query of Part 13's transformer: what a window, NSA's blocks and DSA's
  top-k keep; NSA's and DSA's equations. A recall task (after Zoology's MQAR): full attention, a sliding window, block
  selection (MoBA/NSA) and a learned lightning indexer (DSA's two stages) at 8 keys per query, two seeds; the
  patterns imposed on the full model without retraining. DeepSeek-V4's compressed sparse and heavily compressed
  attention (2026).
* **14. Lottery tickets.** Optimal Brain Damage, Han et al., Frankle & Carbin; iterative magnitude pruning with
  rewinding; computed on a ReLU character network: the ticket against the same masks re-initialized and random
  masks, eight rounds to 22% of the weights (two seeds), the mask replayed.
* **15. Two in four, and sparse activations.** 2:4 structured sparsity (A100, 2020; Part 17); computed on our dense
  transformer: unstructured 50%, 2:4 by magnitude, by Wanda's score and at random, and 2:4 retrained (three seeds);
  the feed-forward activations' distribution and the bits lost when the smallest are zeroed (TEAL-style); exact
  zeros in a ReLU network through training; the lazy neuron phenomenon; TEAL.
* **16. The frontier, late 2026.** The large open mixtures of 2023–26 by experts per layer and share of parameters
  used per token (Mixtral → Kimi K3 and Mistral Large 4); mixtures in closed models (Gemini 1.5 and 2.5 reports);
  sparse attention since 2025 (NSA, MoBA, DSA, MiniMax-M2's return to full attention, GLM-5, DeepSeek-V4,
  MiniMax-M3, Kimi K3).
* **Recap**, where it comes back (Parts 17, 18, 19, 22, 30), problems, Part 17's teaser, references.

## Run

From the repo root:

```
python tools/make.py ai16                          # everything: the numbers, then both languages
python -m videos.ai.ai16.compute                   # only the numbers (about 3 CPU-hours; resumable)
python tools/build.py ai16                         # English
python tools/build.py ai16 --lang zh               # Chinese
```

`compute.py` reads Part 1's books and passage, Part 11's characters (`char_data`), Part 13's transformer
(`.cache/ai13/tf.pt`) and Parts 13 and 14's scoreboards. The long item, `lm_runs` (33 character transformers), runs in
a pool of single-threaded worker processes started with `spawn` (`AI16_WORKERS`, default 2) and keeps every finished
run in `.cache/ai16/lm_runs.partial.json` and its weights in `.cache/ai16/models/`, so an interrupted run resumes;
`recall` and `lottery` keep their pieces the same way. Every random choice is seeded.

## Results

Computed here (regenerate the list with `python -m videos.ai.ai16.results`):

* Mixture against dense (held-out bits per character, mean (range) of 3 seeds, 2,000 steps): dense with the mixture's arithmetic 2.246 (2.241–2.255), the mixture 2.146 (2.133–2.168), dense with its parameters 2.164 (2.155–2.179); on the scoreboard's passage 2.438, 2.343, 2.365. Parameters (total/used per character): 120,320/109,632, 317,952/110,656, 316,928.
* Milliseconds per training step on one core: dense 92, mixture 177, wide dense 175.
* no balancing: busiest expert 1.85× a fair share (end, mean over seeds and blocks), starved experts 2 of 48, MaxVio 0.98, bits 2.152 (2.135–2.164).
* Switch's loss: busiest expert 1.36× a fair share (end, mean over seeds and blocks), starved experts 0 of 48, MaxVio 0.47, bits 2.144 (2.137–2.154).
* loss-free bias: busiest expert 1.02× a fair share (end, mean over seeds and blocks), starved experts 0 of 48, MaxVio 0.21, bits 2.146 (2.133–2.168).
* Coarse / fine / fine + shared (2 seeds): 2.135 (2.133–2.137), 2.156 (2.150–2.161), 2.155 (2.153–2.156).
* Token-slots dropped at capacity factor 1 (imposed after training): none 21.9%, aux 8.1%, moe 1.6%; trained with c = 1: 2.168 (2.159–2.177) against 2.135 (2.133–2.137).
* Four simulated GPUs, busiest GPU's share × 4: none 1.36, aux 1.18, moe 1.01. DeepSeek-V3: 172,032 bytes and 705 MFLOP per token per MoE layer (4,096 FLOP/byte) against 39,580 for FP8 over InfiniBand.
* DeepSeek-V3 counted from its config: 671.0B total, 37.6B active (36.6B without the input embedding); Mixtral 46.70B / 12.88B.
* Upcycling (2 seeds): kept dense 2.308 (2.306–2.310), upcycled 2.237 (2.236–2.238), mixture from scratch 2.135 (2.133–2.137); upcycled training compute 86% of from scratch.
* Mutual information, block 1 (bits, 3 seeds): previous 0.25, current 1.53, next 0.24, shuffled 0.009.
* Mutual information, block 2 (bits, 3 seeds): previous 0.37, current 0.77, next 0.34, shuffled 0.009.
* Mixture-of-depths (MFLOP per character, bits, 2 seeds): dense_active 0.70, 2.242 (2.241–2.242); dense_l3 1.02, 2.198 (2.180–2.217); dense_l4 1.34, 2.168 (2.158–2.178); mod50 1.02, 2.212 (2.203–2.222); mod12 0.78, 2.250 (2.248–2.252). Deciding causally, the 12.5% model routes 13% and scores 2.248 (2.247–2.250).
* Router gradient: formula and autograd agree with finite differences to 1.4e-10 (relative); our MoE layer's router to 5.9e-09.
* 1991 mixture: the gate's trust in its favourite expert 0.919 (0.918–0.922) competing, 0.441 (0.404–0.493) cooperating.
* Recall (8 keys per query, 2 seeds): full 100%, window 7%, blocks 84%, index 100%; imposed on the full model: window 6%, blocks 76%, topk 100%.
* Part 13's transformer: all keys 1.791 bits; 8 keys by score 1.800, a window of 8 1.849.
* Lottery seed 0: dense 2.726; at 22% of the weights: ticket 2.768, re-initialized 2.976, random mask 3.151.
* Lottery seed 1: dense 2.766; at 22% of the weights: ticket 2.775, re-initialized 3.004, random mask 3.172.
* 2:4 on the dense model (3 seeds): dense 2.253 (2.246–2.257); magnitude_24 3.457 (3.388–3.593); wanda_24 3.197 (3.146–3.258); unstructured 2.930 (2.850–3.087); random_24 5.179 (4.875–5.359); retrained magnitude 2:4 2.355 (2.336–2.373), Wanda 2:4 2.355 (2.346–2.370).
* Activations zeroed (share, bits): 0% 2.253, 25% 2.258, 50% 2.317, 75% 2.560, 90% 2.718, 95% 2.906.
* Scoreboard rows: Part 16: dense, same arithmetic 2.438, Part 16: mixture of experts 2.343, Part 16: dense, same parameters 2.365.

## Fact-check notes (checked October 2026)

* DeepSeek-V3: config.json (`n_routed_experts` 256, `num_experts_per_tok` 8, `n_shared_experts` 1,
  `moe_intermediate_size` 2048, `first_k_dense_replace` 3, 61 layers, d 7168, vocab 129,280); our count gives
  671.0B total and 37.6B active with the input embedding (36.6B without); the report gives 671B and 37B, and 685B on
  Hugging Face including the 14B multi-token-prediction module. Routing details from the report (Secs. 2.1.2, 3.2,
  4.2). DeepSeek-V3.2-Exp's config.json: indexer 64 heads of 128, top 2,048.
* DeepSeek-V4 (arXiv 2606.19348, 2026): V4-Pro 1.6T/49B, 384 routed + 1 shared, 6 active; V4-Flash 284B/13B, 256 + 1,
  6 active; CSA compression 4, HCA 128, indexer top-k 1,024 (Pro) / 512 (Flash), window 128, 64 indexer heads of 128
  in FP4; 27% of V3.2's single-token FLOPs and 10% of its KV cache at 1M tokens (the makers' figures).
* Kimi K3: Hugging Face model card (2.8T, 104B active, 896 experts, 16 selected, 2 shared, 69 KDA + 24 gated MLA
  layers). Qwen3.5-397B-A17B and Qwen3-Next-80B-A3B: model cards (512 experts, 10 routed + 1 shared). GLM-5 and
  GLM-4.5: model cards and config.json (GLM-5: 744B/40B, 256 + 1, 8 active, DSA with 32 indexer heads; GLM-4.5:
  160 + 1, 8 active). MiniMax-M2: model card (230B/10B) and config.json (256 experts, 8 active, full attention in all
  62 layers); MiniMax's post "Why Did M2 End Up as a Full Attention Model?". MiniMax-M3: model card (≈428B/23B,
  MiniMax Sparse Attention, 1M context). Mistral Large 4: model card (≈1T, 52B active including embeddings, 49B
  without; 128 routed + 1 shared, 4 active; weights 29 October 2026). Llama 4: Meta's blog (5 April 2025). Kimi K2:
  model card. gpt-oss: model card.
* Switch-C: 1,571B parameters, 2,048 experts (Fedus et al., Table 9); α = 10⁻². GLaM: 1.2T, 96.6B activated (8%).
  GShard: 600B, 2,048 TPU v3, 4 days. Shazeer et al.: up to 137B parameters, >1000× capacity. DeepSeekMoE: 2B ≈ GShard
  2.9B, 16B ≈ LLaMA2 7B with ≈40% of the computation (abstract).
* NSA: l = 32, d = 16, l′ = 64, n = 16, w = 512; 27B/3B model; up to 9.0× forward, 6.0× backward, 11.6× decoding at
  64k (the decoding figure is an expected speedup from memory access). MoBA: deployed for Kimi's long-context
  requests (abstract). Mixture-of-depths: 12.5% capacity every other block; "upwards of 50% faster to step during
  post-training sampling". Sparse upcycling: "~50% of the initial dense pretraining sunk cost". Lazy neurons: 3.0%
  nonzero in T5-Base, 6.3% in ViT-B16. TEAL: 40–50% model-wide sparsity, up to 1.53×/1.8× decoding speed-ups.
* Claims resting on a single or company source: all model configurations and the makers' efficiency figures
  (DeepSeek-V4's 27%/10%, NSA's speed-ups, DeepSeekMoE's comparisons, MiniMax's reasons), Gemini's architecture
  statement, MoBA's deployment.

## Problems

1. For DeepSeek-V3's gates g_i = σ(s_i)/Σ_{j∈K} σ(s_j), show that ∂L/∂s_j = (1 − σ(s_j)) g_j (u_j − ū) for j ∈ K, and 0
   otherwise.
2. Show that if f = P, Switch's E Σ_i f_i P_i ≥ 1, with equality only when every f_i = 1/E. Why does it matter that f
   has no gradient?
3. Show that (N/k)^k ≤ C(N, k) ≤ (eN/k)^k, and compute C(64, 8)/C(16, 2).
4. Eight experts get these shares of the token-slots: 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02. What share is dropped
   at capacity factors 1 and 1.25?
5. DeepSeek-V4-Pro: d = 7,168, experts of width 3,072, 6 routed per token. Compute the all-to-all bytes per token per
   layer (FP8 out, BF16 back), the experts' FLOPs, and their ratio.
6. Mixtral 8x7B: 32 layers, d = 4,096, SwiGLU experts of width 14,336, 32 query heads and 8 key-value heads of 128, a
   vocabulary of 32,000. Count its total and active parameters.

### Solutions

1. With S = Σ_{j∈K} σ_j and σ′_j = σ_j(1 − σ_j): ∂g_i/∂s_j = (δ_ij σ′_j S − σ_i σ′_j)/S² = (σ′_j/S)(δ_ij − g_i) =
   (1 − σ_j) g_j (δ_ij − g_i). So ∂L/∂s_j = Σ_{i∈K} u_i ∂g_i/∂s_j = (1 − σ_j) g_j (u_j − Σ_i g_i u_i). An unchosen s_j
   appears nowhere in the output (the top-k choice is piecewise constant in s), so its gradient is 0.
2. With f = P and Σ f_i = 1, Cauchy–Schwarz gives (Σ f_i)² ≤ E Σ f_i², so E Σ f_i² ≥ 1, with equality iff all f_i are
   equal, i.e. 1/E. f is a count (piecewise constant), so the gradient flows only through P: ∂L_aux/∂P_i = αE f_i,
   which pushes the probability of the busiest experts down hardest; the product makes the penalty differentiable
   while still measuring where tokens actually go.
3. C(N, k) = Π_{i<k} (N − i)/(k − i) and each factor is ≥ N/k (since N ≥ k), giving the lower bound. And
   C(N, k) ≤ N^k/k! with k! ≥ (k/e)^k (because e^k = Σ_n k^n/n! ≥ k^k/k!), giving the upper bound.
   C(64, 8) = 4,426,165,368 and C(16, 2) = 120: a ratio of about 36.9 million.
4. Capacity per expert is c/E of the slots: 0.125 at c = 1 and 0.15625 at c = 1.25. Dropped = Σ max(0, f_i − c/E):
   at c = 1, 0.175 + 0.075 + 0.075 = 0.325; at c = 1.25, 0.14375 + 0.04375 + 0.04375 = 0.23125.
5. Bytes: k d (1 + 2) = 6 × 7,168 × 3 = 129,024 (about 129 kB). FLOPs: 2 · 3 d h · k = 6 × 7,168 × 3,072 × 6 =
   792,723,456 (about 793 million). Ratio: 2h = 6,144 FLOPs per byte, against about 39,580 for an H100-class GPU's FP8
   arithmetic over 50 GB/s InfiniBand: sent naively, the network would take about 6.4 times as long as the experts.
6. Attention per layer: 2 × 4,096² + 2 × 4,096 × 1,024 = 41,943,040. One expert: 3 × 4,096 × 14,336 = 176,160,768;
   eight: 1,409,286,144; router 32,768; two norms 8,192. Per layer 1,451,270,144; × 32 = 46,440,644,608; embeddings
   and output 2 × 32,000 × 4,096 = 262,144,000; final norm 4,096: total 46,702,792,704 ≈ 46.7B. Active: per layer
   41,943,040 + 2 × 176,160,768 + 32,768 + 8,192 = 394,305,536; × 32 + 262,148,096 = 12,879,925,248 ≈ 12.9B.

## 中文

**第16部分：稀疏。** 每次只用模型的一部分：混合专家、深度混合、只读部分过去内容的注意力，以及稀疏的权重和激活。

### 习题

1. 对DeepSeek-V3的门控 g_i = σ(s_i)/Σ_{j∈K} σ(s_j)，证明对 j ∈ K 有 ∂L/∂s_j = (1 − σ(s_j)) g_j (u_j − ū)，其余为0。
2. 证明当 f = P 时，Switch的 E Σ_i f_i P_i ≥ 1，当且仅当每个 f_i = 1/E 时取等号。为什么 f 没有梯度很重要？
3. 证明 (N/k)^k ≤ C(N, k) ≤ (eN/k)^k，并计算 C(64, 8)/C(16, 2)。
4. 八个专家分到的词元槽份额为 0.3、0.2、0.2、0.1、0.1、0.05、0.03、0.02。容量因子为1和1.25时，丢弃的份额各是多少？
5. DeepSeek-V4-Pro：d = 7168，专家宽度3072，每个词元路由到6个专家。计算每个词元、每层的全对全通信字节数（发出用FP8，
   返回用BF16）、专家的浮点运算量，以及两者之比。
6. Mixtral 8x7B：32层，d = 4096，SwiGLU专家宽度14336，32个查询头和8个键值头，每头128维，词表32000。数一数它的总参数和激活参数。

### 解答

1. 记 S = Σ_{j∈K} σ_j，σ′_j = σ_j(1 − σ_j)。则 ∂g_i/∂s_j = (σ′_j/S)(δ_ij − g_i) = (1 − σ_j) g_j (δ_ij − g_i)，所以
   ∂L/∂s_j = Σ_{i∈K} u_i ∂g_i/∂s_j = (1 − σ_j) g_j (u_j − Σ_i g_i u_i)。没被选中的 s_j 不出现在输出里（top-k选择对 s
   是分段常数），梯度为0。
2. f = P 且 Σ f_i = 1 时，由柯西–施瓦茨不等式 (Σ f_i)² ≤ E Σ f_i²，所以 E Σ f_i² ≥ 1，当且仅当所有 f_i 相等（都是1/E）
   时取等号。f 是计数（分段常数），梯度只经过 P：∂L_aux/∂P_i = αE f_i，最忙的专家的概率被压得最狠；乘积让惩罚可微，
   同时仍然衡量词元实际去了哪里。
3. C(N, k) = Π_{i<k} (N − i)/(k − i)，每个因子都 ≥ N/k，得下界；C(N, k) ≤ N^k/k!，且 k! ≥ (k/e)^k（因为
   e^k = Σ_n k^n/n! ≥ k^k/k!），得上界。C(64, 8) = 4 426 165 368，C(16, 2) = 120，比值约3690万。
4. 每个专家的容量是 c/E 的槽位：c = 1 时0.125，c = 1.25 时0.15625。丢弃 = Σ max(0, f_i − c/E)：c = 1 时
   0.175 + 0.075 + 0.075 = 0.325；c = 1.25 时 0.14375 + 0.04375 + 0.04375 = 0.23125。
5. 字节：k d (1 + 2) = 6 × 7168 × 3 = 129 024（约129 kB）。浮点运算：2 · 3 d h · k = 792 723 456（约7.93亿）。
   比值：2h = 6144次运算每字节；而H100级GPU的FP8算力配50 GB/s的InfiniBand，需要约39 580次运算每字节：直接发送的话，
   网络要花的时间约是专家计算的6.4倍。
6. 每层注意力：2 × 4096² + 2 × 4096 × 1024 = 41 943 040。一个专家：3 × 4096 × 14336 = 176 160 768，八个
   1 409 286 144；路由器32 768；两个归一化8192。每层1 451 270 144，乘32得46 440 644 608；输入嵌入和输出层
   2 × 32000 × 4096 = 262 144 000；最后的归一化4096：总计46 702 792 704 ≈ 467亿。激活：每层
   41 943 040 + 2 × 176 160 768 + 32 768 + 8192 = 394 305 536，乘32再加262 148 096，得12 879 925 248 ≈ 129亿。

## Glossary

| English | 中文 |
|---|---|
| mixture of experts (MoE), expert | 混合专家（MoE），专家 |
| gate, gating network | 门控，门控网络 |
| router, router score | 路由器，路由分数 |
| top-k gating, KeepTopK | top-k门控，KeepTopK |
| noisy top-k gating | 带噪声的top-k门控 |
| competitive / cooperative loss | 竞争式 / 合作式损失 |
| responsibility (posterior) | 责任（后验概率） |
| active parameters, total parameters | 激活参数，总参数 |
| load balancing, routing collapse | 负载均衡，路由坍缩 |
| importance loss, coefficient of variation (CV) | 重要性损失，变异系数（CV） |
| auxiliary loss (Switch), z-loss | 辅助损失（Switch），z损失 |
| auxiliary-loss-free balancing, balancing bias | 无辅助损失的负载均衡，均衡偏置 |
| sigmoid gate | sigmoid门控 |
| MaxVio (maximal violation) | 最大违背度（MaxVio） |
| fine-grained expert, shared expert | 细粒度专家，共享专家 |
| capacity, capacity factor, dropped token | 容量，容量因子，被丢弃的词元 |
| expert-choice routing | 专家选择路由 |
| expert parallelism, all-to-all | 专家并行，全对全通信 |
| node-limited routing | 节点受限路由 |
| sparse upcycling | 稀疏升级（upcycling） |
| mixture-of-depths | 深度混合（MoD） |
| sliding-window attention, block selection | 滑动窗口注意力，块选择 |
| native sparse attention (NSA), MoBA | 原生稀疏注意力（NSA），MoBA |
| DeepSeek sparse attention (DSA), lightning indexer | DeepSeek稀疏注意力（DSA），闪电索引器 |
| compressed sparse attention (CSA), heavily compressed attention (HCA) | 压缩稀疏注意力（CSA），重度压缩注意力（HCA） |
| associative recall | 联想回忆 |
| pruning, magnitude pruning | 剪枝，按幅度剪枝 |
| lottery ticket hypothesis, winning ticket | 彩票假设，中奖彩票 |
| iterative magnitude pruning, rewinding | 迭代幅度剪枝，回卷 |
| unstructured / structured sparsity, 2:4 sparsity | 非结构化 / 结构化稀疏，2:4稀疏 |
| sparse tensor cores | 稀疏张量核心 |
| Wanda, SparseGPT | Wanda，SparseGPT |
| activation sparsity, lazy neuron phenomenon | 激活稀疏，懒惰神经元现象 |
