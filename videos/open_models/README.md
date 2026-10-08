# Inside the Open Frontier: The Architectures of MiMo-V2.6-Pro, GLM-5.3 and Kimi K3

A 33-minute, 16-chapter explainer of how the three strongest open-weights
language models work inside. The models were picked by the [Artificial
Analysis Intelligence Index](https://artificialanalysis.ai/models/open-source)
(v4.3.2, as of **October 8, 2026**): Xiaomi's **MiMo-V2.6-Pro** (46), Z.ai's
**GLM-5.3** (45) and Moonshot AI's **Kimi K3** (44). All three are mixtures of
experts with a million-token context, and each pays for that context
differently:

* **MiMo** looks nearby. 60 of its 70 layers only see a 128-token sliding
  window, with learned attention sinks. 10 global layers carry long-range
  information.
* **GLM** compresses, then selects. Multi-head latent attention caches 576
  numbers per token per layer. A lightning indexer then picks the 2,048 tokens
  each query actually reads, and one indexer is shared by every four layers.
* **Kimi K3** keeps a running memory. 69 of its 93 layers are Kimi Delta
  Attention, a fixed-size recurrent memory updated by the gated delta rule.
  Every fourth layer is global MLA with no position encoding at all. On top of
  that come attention residuals (attention across depth) and a latent mixture
  of 896 experts.

**Everything on screen that describes a model comes from that model's
published files.** That covers the layer layouts, head counts and expert
counts (`config.json`), parameter counts, and a few of the learned weights
themselves. Parameter counts come from the shapes of all 775,889 tensors in the
three checkpoints. The learned weights are MiMo's 7,680 attention-sink logits,
every model's router balancing biases, the decay biases of Kimi K3's 848K KDA
channels, its 186 attention-residual queries, and a block of real 4-bit expert
weights. None of this needs the 1–3 TB of weights to be downloaded: safetensors
files begin with a JSON table of every tensor's shape and byte offset, so HTTP
range requests read exactly what is needed (`fetch.py`). Mechanisms are shown
with small, seeded toy computations, labeled as such, and schematics are
labeled `schematic`.

**Watch:** [`published/open_models.mp4`](../../published/open_models.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

- `0:00` Three open frontier models
- `2:36` The blueprint, and its two bills
- `4:10` Mixture of experts
- `6:11` Routing, and keeping the experts busy
- `8:52` The million-token problem
- `10:06` MiMo: look nearby, mostly
- `12:14` MiMo: permission to look at nothing
- `14:34` GLM: compress the memory
- `16:43` GLM: read only what matters
- `19:02` Kimi: a memory that never grows
- `20:56` Kimi: the delta rule, and forgetting
- `23:15` Kimi: three to one
- `25:14` Kimi: attention across depth
- `27:16` Kimi: 896 experts, kept stable
- `29:14` Side by side
- `31:23` Recap

</details>

```bash
python -m videos.open_models.fetch          # once: AA leaderboard + HF configs, shard headers, small tensors (~4 min)
python -m videos.open_models.fetch --offline # rebuild data.json from the cache
python tools/build.py open_models -q l      # preview
python tools/build.py open_models           # final 1080p30 + subtitles + chapters
python tools/export_script.py open_models   # regenerate SCRIPT.md from the code
python tools/check_narration.py open_models # Whisper listen test of every narration line
python tools/publish.py open_models         # GitHub-sized copy -> published/open_models.mp4
```

`data.json` (committed, ~300 kB) is all the scenes read; they never touch the
network. `toys.py` holds the toy computations; each is a few milliseconds of
seeded NumPy, so scenes call it directly.

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 0 | `Hook` | The open/closed race; the top three open models; their size vs. what each token uses; three different machines. Roadmap. | AA's progress timeline (59 models) and scores; parameters counted from every tensor; real layer layouts from the three configs. |
| 1 | `Blueprint` | Tokens → vectors → attention + FFN → prediction. Bill 1: ≈2 operations per parameter per token. Bill 2: the KV cache grows with context, comparisons with its square. | — |
| 2 | `Experts` | Split the FFN into experts, route each token to a few. Capacity grows with all experts, compute only with the active ones. Combinatorics; shared experts. | Expert counts (384/8, 256+1/8, 896+2/16); routed experts are 98% / 96% / 98% of all parameters. |
| 3 | `Routing` | Sigmoid router, top-k, normalized weights. Rich-get-richer imbalance. DeepSeek's selection-only bias. Kimi's Quantile Balancing. | Real learned balancing biases of one layer of each model (GLM's sit near +8); toy QB vs. fixed nudges. |
| 4 | `LongContext` | Textbook attention at GLM's size: 5.1 MB per token, 5.1 TB at 1M tokens (~7× the weights). ½·10¹² comparisons. Three strategies. | GLM's dims; its 0.76 TB of weights on disk. |
| 5 | `SlidingWindow` | Causal triangle → 128-token band. MiMo's 60 local / 10 global layout. Reach through depth (7,620 tokens). Cache 51 vs 358 KB/token. GQA 128/8. Partial RoPE (64 of 192 dims). | Real layer layout; cache sizes from the config. |
| 6 | `Sinks` | Softmax must sum to 1. First-token sinks vs. windows. A learnable sink logit: weights can sum to < 1. Xiaomi's ablation: the 128 window beats all-global and 512. | All 60 × 128 learned sink logits; MiMo-V2-Flash report Tables 2–3. |
| 7 | `LatentAttention` | MLA: cache a 512-d latent (+64 positional) instead of per-head K/V: 57× smaller. Absorbing the up-projection into the query. GLM's Muon Split and 64×256 heads. | GLM's MLA dims. |
| 8 | `SparseAttention` | DSA's lightning indexer, top-2,048 by content. IndexShare: one indexer per four layers. Training from a dense model. | Real indexer layout (21 of 78 layers); GLM-5 report Table 3. |
| 9 | `LinearMemory` | Drop the softmax and attention regroups into a memory matrix S = Σ v kᵀ. Fixed size. Geometry of storing pairs; crosstalk; why a plain sum can't update a fact. | — (2-D toy) |
| 10 | `DeltaRule` | Read, compare, write the error: one gradient step on recall error. Toy reassignment test. KDA's per-channel, per-token forgetting. Lower-bounded gates. | Half-lives at rest of all 847,872 KDA channels (median 29 tokens; layer 1 ≈ 4); toy recall curves. |
| 11 | `Hybrid` | Fixed memory can't hold a needle exactly → every 4th layer global MLA (+1 on top). NoPE in MLA; order from KDA's decay and 4-token convolution. Output gates. Cache: 28 GB + 434 MB fixed. | Real 69/24 layout; cache sizes from the config. |
| 12 | `AttentionResiduals` | The residual stream as an RNN over depth. AttnRes: each layer attends over earlier outputs with a learned query. Blocks of 12 (≤ 9 sources). | The 186 learned depth-attention queries: within-block neighbours 0.47 vs. 0.25 across a boundary. |
| 13 | `LatentMoE` | Dispatch traffic. LatentMoE: experts at half width (3,584). RMSNorm before the up-projection. SiTU-GLU soft caps (β = 4, 25). 2.5× scaling efficiency (reported). | K3's latent and expert dims, SiTU β's. |
| 14 | `SideBySide` | Cache vs. context for all three. Speculative decoding. 4-bit weights. Summary table. | Cache curves from configs; 32 real 4-bit weights from a K3 expert; on-disk sizes. |
| 15 | `Outro` | Recap; what's not covered (training, RL); credits. | |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| MiMo-V2.6-Pro / GLM-5.3 / Kimi K3 (model identity, chart series) | orange / blue / lavender |
| token vectors, residual stream | blue |
| query / key / value | yellow / teal / red |
| attention weights, global attention layers, attention across depth | orange |
| experts (routed) / shared experts | purple / light purple |
| router scores | gold |
| balancing biases, expert load | light brown |
| sliding-window (local) layers | light teal |
| attention sinks | warm grey |
| MLA latent | light green |
| DSA indexer, selected tokens | pink |
| KDA / linear-attention memory | green |

## Data (`fetch.py`)

| Source | What | Used in |
|---|---|---|
| Artificial Analysis `/models/open-source` | Intelligence Index v4.3.2 (10 evaluations) of every listed open-weights model, and the page's "Open Source Progress" timeline (59 models, open vs. proprietary). The top three on Oct 8, 2026 are asserted. | 0 |
| Hugging Face `config.json` | Layer layouts, heads, dims, window, expert counts, MLA/KDA/indexer settings, SiTU β's, AttnRes block size. | everywhere |
| Safetensors shard headers (range requests) | Name, dtype and shape of all 160,040 / 118,629 / 497,220 tensors. | 0, 2, 14 |
| Small tensors (range requests, ~5 MB) | MiMo `attention_sink_bias` (60 × 128); every MoE layer's `e_score_correction_bias`; K3's `A_log` + `dt_bias` (69 KDA layers) and `*_res_norm`/`*_res_proj` (186 pseudo-queries); one 32-value MXFP4 block from a K3 and a MiMo expert. | 3, 6, 10, 12, 14 |

### Method notes (so the numbers can be reproduced and are not over-read)

* **Parameter counts.** Every stored tensor is counted by its shape. MXFP4 tensors (`U8`, two 4-bit values per byte) count twice their byte count. Block scales (`weight_scale`, `weight_scale_inv`) are not parameters. Totals: MiMo 1,024.2B (published 1.02T), GLM 753.3B (753B), Kimi K3 2,779.9B (2.78T, report Table 1). They include the vision/audio encoders and the multi-token-prediction layers shipped in each checkpoint.
* **Active parameters.** Everything in the language model except vision/audio encoders, the MTP layers, and the routed experts a token isn't sent to (k/N of the routed experts are counted). Result: 42.2B / 41.3B / 105.4B, vs. the labs' 42B / "40B" / 104.2B. The small differences are definitional (e.g. whether embeddings count).
* **Router biases.** `e_score_correction_bias` is DeepSeek-V3's auxiliary-loss-free balancing bias (all three use `topk_method: noaux_tc`). It is added to the sigmoid scores for top-k selection only. The plotted layer is the middle MoE layer of each model (MiMo layer 36, GLM 41, K3 48, 1-based).
* **Sink logits.** MiMo's `attention_sink_bias` exists only in its 60 SWA layers (`add_swa_attention_sink_bias: true`). The modeling code appends it as an extra logit column before the softmax and drops that column afterwards, exactly as on screen. The color map is clipped at ±2. The range is −6.2 to +3.0, and 96.8% of the values are positive.
* **KDA half-lives.** K3's bounded gate (report eq. 5): g = g_min·σ(e^{A_h}·z) with g_min = −5 and retention α = e^g. The input-dependent part of z (`f_b(f_a(x))`) is set to zero, leaving z = `dt_bias`: the retention *at rest*, before a token's own input moves it. The half-life is ln 2 / (−g) tokens. `A_log` is stored padded to 128 entries; the first 96 (the heads) are used. Real retention is data-dependent, so this is the learned default, not what happens on any particular text.
* **Attention-residual queries.** Each sublayer's query is `*_res_norm.weight ⊙ *_res_proj.weight` (the code folds RMSNorm's gain into the query). The heat map shows cosine similarities of the 186 queries. Layer 1's attention query is all zeros (nothing to attend over yet), so its row is blank. The quoted numbers average neighbouring layers within a block vs. across a block boundary.
* **Cache sizes.** BF16 (2 bytes) per cached number for MiMo's K/V and the MLA latents (512 + 64 per token per layer), FP8 for DSA indexer keys (128 per token in the 21 indexer layers), and FP32 for KDA states (69 × 96 × 128 × 128). "Textbook attention at GLM's size" = 64 heads × (256-d key + 256-d value) × 78 layers. Production engines can store caches in FP8, which halves the BF16 numbers.
* **4-bit block.** The first 16 bytes of row 0 of `layers.12…experts.0.w1.weight_packed` (K3, layer 13, expert 1, 0-based in the file) are decoded low nibble first through the E2M1 table {0, 0.5, 1, 1.5, 2, 3, 4, 6, and their negatives}. The scale is the first byte of `weight_scale`, an E8M0 exponent (127-biased): 2⁻⁶.
* **Toys** (`toys.py`) use random vectors, not model activations. The 2-D memory and the 64-d reassignment test (16 keys, 20 trials) compare a plain sum with the delta rule. The balancing demo routes 8,192 random tokens per step to 16 synthetic experts with built-in popularity skew, k = 2, comparing DeepSeek's fixed-step sign update (γ = 0.01) with Kimi's quantile rule. Each step routes a fresh batch with the bias computed from the previous one. The sink example uses six window logits near 0 and a sink logit of 2.

## Fact-check notes and sources

* **Ranking**: Artificial Analysis, [open-source models](https://artificialanalysis.ai/models/open-source), Intelligence Index v4.3.2 (AA-Briefcase, GDPval-AA, AutomationBench-AA, Terminal-Bench 4.0, SciCode, Humanity's Last Exam, GDP.pdf, CritPt, AA-Omniscience, AA-LCR), fetched Oct 8, 2026: MiMo-V2.6-Pro 46.3, GLM-5.3 (Max) 44.8, Kimi K3 (Max) 43.6; best proprietary in the progress chart: Claude Opus 5.5 (max, with fallback) 57.6. Scores are AA's; they change as models and the index are updated.
* **MiMo-V2.6-Pro**: [model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL) and *MiMo-V2.6 technical report* (Xiaomi, Sept 2026; in the repo): 1.02T total / 42B active; 70 layers (60 SWA / 10 GA), window 128, 128 Q / 8 KV heads, head dims 192/128, 384 experts / 8 active, no shared experts; first block global with a dense FFN; 5-layer SWA drafter predicting 7 tokens; MXFP4 QAT during mid-training. The backbone design and the sink ablations come from the *MiMo-V2-Flash Technical Report* (arXiv:2601.02780): "sliding window size is 128-token and the hybrid local:global ratio is 5:1"; learnable sink bias following gpt-oss; Tables 2–3 (32B dense test models). The MRCR/NoLiMa numbers in Ch. 6 are from those tables.
* **GLM-5.3**: [model card](https://huggingface.co/zai-org/GLM-5.3) ("the same base model as GLM-5.2 — every gain comes from post-training"); *GLM-5: from Vibe Coding to Agentic Engineering*, arXiv:2602.15763: MLA with Muon Split (Table 1), MLA-256 ("increase the head dimension from 192 to 256 and decrease the number of attention heads by 1/3"), DSA continued pre-training (Table 3), MTP with shared parameters. [GLM-5.2 model card](https://huggingface.co/zai-org/GLM-5.2) and [blog](https://huggingface.co/blog/zai-org/glm-52-blog): IndexShare "reuses the same indexer across every four sparse attention layers, reducing per-token FLOPs by 2.9× at a 1M context length"; MTP acceptance length 4.56 → 5.47 (+20%), measured on GLM-5.1's backbone with 7 MTP steps. Overlap of 70–100% between adjacent layers' selections: Bai et al., *IndexCache*, arXiv:2603.12201 (a 30B DSA model).
* **DeepSeek Sparse Attention**: DeepSeek-AI, *DeepSeek-V3.2*, arXiv:2512.02556, eq. 1 (I_{t,s} = Σ_j w_{t,j}·ReLU(q_{t,j}·k_s), FP8, few heads) and the top-k selection.
* **MLA**: DeepSeek-AI, *DeepSeek-V2*, 2024 (latent KV, decoupled RoPE key, absorbed projections).
* **Kimi K3**: [model card](https://huggingface.co/moonshotai/Kimi-K3) and *Kimi K3: Open Frontier Intelligence* (Moonshot AI, Aug 2026; [GitHub](https://github.com/MoonshotAI/Kimi-K3)): 2.8T / 104B; 93 layers, 69 KDA + 24 Gated MLA (3:1 plus a final MLA layer); NoPE in all MLA layers; full-rank sigmoid output gates; KDA eq. 1–6 with the lower-bounded decay g_min = −5; Block AttnRes with 12-layer blocks (eq. 8–10); Stable LatentMoE: 896 experts / 16 active / 2 shared, latent 3,584, RMSNorm before W↑ (eq. 11), SiTU-GLU with β₁ = 4, β₂ = 25 (eq. 12), Quantile Balancing (eqs. 13–14); context 8K → 64K in pre-training, 256K → 1M in cooldown; MXFP4 weights / MXFP8 activations, QAT from SFT onward; "approximately 2.5× improvement in overall scaling efficiency over Kimi K2" (Fig. 7, attributed to architecture, data and training recipe together); one MTP layer (Table 1).
* **Kimi Linear / KDA**: Kimi Team, *Kimi Linear*, arXiv:2510.26692: KDA extends Gated DeltaNet with channel-wise gates; "reducing KV cache usage by up to 75% and achieving up to 6× decoding throughput for a 1M context" vs. full MLA (48B-total model).
* **Delta rule**: Widrow & Hoff, *Adaptive switching circuits*, 1960; for linear attention: Schlag, Irie & Schmidhuber, *Linear Transformers Are Secretly Fast Weight Programmers*, 2021; Yang et al., *Gated Delta Networks*, 2024. Linear attention as a matrix memory: Katharopoulos et al., 2020.
* **Attention Residuals**: Kimi Team, *Attention Residuals*, 2026 (cited by the K3 report as [58]).
* **LatentMoE**: Elango et al. (NVIDIA), arXiv:2601.18089.
* **Auxiliary-loss-free balancing**: DeepSeek-AI, *DeepSeek-V3 Technical Report*, arXiv:2412.19437.
* **Attention sinks**: Xiao et al., *Efficient Streaming Language Models with Attention Sinks*, 2023; learnable sink logits as in OpenAI's gpt-oss (2025).
* **SwiGLU**: Shazeer, *GLU Variants Improve Transformer*, 2020.
* **MXFP4**: OCP Microscaling Formats (MX) v1.0 specification (E2M1 elements, E8M0 shared scale per 32).

The video makes no claims about the models' training data or about proprietary
models beyond their AA scores. Lab-reported results (ablations, speedups,
scaling efficiency) are attributed on screen and in the narration, and were not
independently reproduced.
