# How Frontier AI Models Are Trained, End to End

A ~45-minute, 18-chapter explainer in four parts, following one frontier
training run from the raw web to a reasoning assistant: **the data** (Common
Crawl, the FineWeb filters, MinHash deduplication, quality classifiers,
mixtures, tokens), **the recipe** (scaling laws, mixture-of-experts
architectures, AdamW and Muon, learning-rate schedules, FP8 and FP4 numbers,
loss spikes), **scaling out** (memory, data / tensor / pipeline / expert
parallelism, failures and checkpoints) and **post-training** (supervised
fine-tuning, preferences and DPO, reinforcement learning with verifiable
rewards, agentic RL, evaluation). It describes the field **as of October 2026**.

**Every chart is a real run, in miniature, on the 4-core CPU that rendered the
video**: the FineWeb recipe run on 10,498 pages of Common Crawl's September 2026
crawl, MinHash on 170,000 more, FineWeb-Edu's classifier, a 20-run IsoFLOP
scaling-law sweep, AdamW vs Muon, cosine vs warmup-stable-decay, a learning-rate
stability sweep with and without QK-norm, three mixture-of-experts load-balancing
runs, the singular values of a real gradient going through Newton–Schulz, FP8 /
FP4 quantization of GPT-2's real activations, a real chat template, and a
GRPO run with a verifiable reward. Frontier numbers come from the labs' own
reports and are cited below. Schematics are labeled `schematic`, illustrative
examples `illustrative`.

**Watch:** [`published/frontier.mp4`](../../published/frontier.mp4) (1080p, subtitles and chapters embedded).

```bash
python -m videos.frontier.compute          # once: all real footage (a few CPU-hours on 4 cores; cached in .cache/frontier)
python tools/build.py frontier -q l        # preview
python tools/build.py frontier             # final 1080p30 + subtitles + chapters
python tools/export_script.py frontier     # regenerate SCRIPT.md from the code
python tools/check_narration.py frontier   # Whisper listen test of every narration line
python tools/publish.py frontier           # GitHub-sized copy -> published/frontier.mp4
```

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 1 | `Hook` | An answer streams back token by token (schematic). How much compute notable models used to train, and how fast the frontier grows. Every experiment in the video is a real run, about 10¹¹× smaller. The pipeline map: web → clean data → pretraining → GPU cluster → post-training → assistant. Four-part roadmap. | Epoch AI's compute estimates for notable models since 2012: GPT-2 ≈ 10²¹, GPT-3 > 100× that, GPT-4 ≈ 70× more; Llama 3.1 405B, Grok 4 and GPT-6 Astra circled. A least-squares frontier trend of ×4.8 per year (45 frontier models since 2018). All of this video's pocket runs together: {pocket_flops} FLOPs, ~10¹¹× below 10²⁶. |
| 2 | `RawWeb` | Part 1. Almost everyone starts from Common Crawl; one crawl is 100,000 files. A crawled page is mostly markup. Extracting the main text is its own step (Trafilatura, as in FineWeb, beats Common Crawl's WET text). The web is multilingual; we keep English. | CC-MAIN-2026-39: 2.17B pages, 106 TiB, 100,000 files (one square each, ~21,500 pages); the 8 WET files and 400 MB of WARC we downloaded are circled. A real recipe-blog page: 2,296 lines of HTML with the whole post on line 436; 98 KB of HTML → 3 KB of text (≈ 3%). The 10,498 pages of the WARC: 1.65 GB of HTML → 37 MB of text. fastText language shares (English ≈ 4 in 10). |
| 3 | `Filtering` | The FineWeb recipe run stage by stage with FineWeb's own code (datatrove): URL blocklist, extractable text, English (fastText > 0.65), Gopher repetition, Gopher quality, C4 line rules, FineWeb's three rules. The rules are blunt (one false positive shown). | Pages surviving each stage, 10,498 → 1,363. Real rejected pages: a redirect-only page, a forum index, a login form, spun ad copy with template braces, a course-handbook menu. A programming puzzle dropped by mistake (`gopher_below_alpha_threshold`). 13% of pages and about a third of a percent of the bytes survive. *Quoted:* 4.56M blocked domains; FineWeb = 96 crawls → 15T tokens. |
| 4 | `Dedup` | Why copies hurt (wasted compute, memorization). 5-word shingles and Jaccard similarity. MinHash: P(minima match) = J, so 112 minima are a fingerprint. LSH banding (14 × 8) and its S-curve 1 − (1 − s⁸)¹⁴. Deduplicate each crawl separately, not globally. | The biggest cluster in the 8 WET files: 41 "[domain] is for sale" pages. Two GoDaddy for-sale pages: shingle Venn counts, J = 0.78; 86 of 112 minima agree (estimate 0.77). P(0.8) = 92%, P(0.5) ≈ 5%. 8,457 → 8,208 pages (after the filters), ≈ 3% removed in 114 clusters (for-sale 41, access-denied 24, default hosting 7). *Quoted:* FineWeb's cross-crawl dedup removed 90% of the oldest crawls and trained worse models. |
| 5 | `Quality` | Model-based filtering (FineWeb-Edu: an LLM grades pages, a small classifier imitates it, keep ≥ 3). Keep the best and rewrite the rest (synthetic rephrasing, upsampling). Data mixtures and annealing. How big datasets are. BPE tokenizers. | FineWeb-Edu's own classifier on 400 random pages of our 1,363 survivors: a histogram of scores 0–5, 7% score ≥ 3, the top page and a typical low one. Our 2,048-token BPE splitting a real sentence; 168M tokens of FineWeb-Edu for the pretraining runs. *Quoted:* 500,000 graded pages, 6,000 H100 hours; FineWeb-Edu kept 8% (1.3T tokens); Nemotron-CC 1.9T synthetic tokens; Kimi K2 SimpleQA 23.8% → 28.9%; OLMo 3 repeats data ≤ 7×; Llama 3 mix 50/25/17/8%, +24% GSM8K from annealing; Llama 3 15.6T, DeepSeek-V3 14.8T, Kimi K2 15.5T, GLM-5 28.5T, DeepSeek-V4 33T, Qwen3 36T tokens; vocabularies of 128K–260K. |
| 6 | `ScalingLaws` | Part 2. C ≈ 6ND (2 operations forward + 4 backward); a fixed budget is a fixed area. IsoFLOP valleys and parabola fits; the compute-optimal N is a power law in C. Chinchilla's loss landscape and ≈ 20 tokens per parameter. Why everyone overtrains (cheaper inference). | Our IsoFLOP sweep: 20 real runs at 10¹², 3×10¹², 10¹³ and 3×10¹³ FLOPs, final validation loss vs model size, fitted parabolas and their optima; N_opt ∝ C^{isoflop_slope}. A heat map of Hoffmann et al.'s Eq. 10 (E 1.69, A 406.4, B 410.7, α 0.34, β 0.28; the formula, not data). Tokens per (active) parameter: 20 (Chinchilla), 39 (Llama 3.1 405B), 400 (DeepSeek-V3), 1,636 (Qwen3-235B), 1,875 (Llama 3 8B). *Quoted:* GPT-3 175B on 300B tokens; Chinchilla 70B on 1.4T beat the 280B Gopher; Llama 3 IsoFLOPs up to 10²². |
| 7 | `Architecture` | The GPT-2 blueprint, refined: RMSNorm, RoPE, SwiGLU, grouped-query or latent attention, QK-norm, no biases. Mixture of experts: a router, top-k, parameters vs compute per token (schematic). Frontier MoEs keep getting sparser. Load balancing: rich-get-richer, an auxiliary loss, DeepSeek-V3's bias. Sparse attention, hybrid linear attention, multi-token prediction, 1M-token context. | Three real pocket MoE runs (8 experts, top-2; no balancing / auxiliary loss / bias): the share of tokens each expert gets in layer 2, animated over training; final validation losses {moe_vals}. *Quoted:* DeepSeek-V3 8 of 256 experts + 1 shared, 671B total / 37B active; Kimi K2 8 of 384, 1.04T / 32B; Kimi K3 16 of 896, 2.8T; sparse attention over the top 2,048 tokens; 3 linear layers per full-attention layer. |
| 8 | `Optimizer` | Gradient descent zigzags while Adam normalizes each coordinate (computed on ½(25x² + y²)); AdamW. Muon: G = UΣVᵀ → UVᵀ, so every direction takes an equal step; a Newton–Schulz polynomial replaces the SVD. AdamW vs Muon. Adoption, and a speed-up that shrinks with scale. | Singular values of a real gradient (a 336 × 128 MLP matrix of a pocket model): the top 5 of 128 directions hold 65% of it (squared), the median is 1/47 of the largest; after 5 iterations every value lies in 0.6–1.2. The same values through 5 Newton–Schulz iterations of p(σ) = 3.4445σ − 4.7750σ³ + 2.0315σ⁵. AdamW vs Muon on the same ≈ 1M-parameter model and 12M tokens: final 3.80 vs 3.61; at the peak learning rate, Muon reaches each of AdamW's losses with 55–66% of the tokens (63% at the end of the stable phase). *Quoted:* Moonlight ≈ half the FLOPs; Kimi K2 (MuonClip, 1T, 15.5T); 1.4× at 0.1B vs 1.1× at 1.2B (Wen et al.). |
| 9 | `Schedule` | Warmup; cosine decay vs warmup–stable–decay (WSD). Cosine fixes the run length in advance. WSD's loss lags, then drops in the cooldown, and cooldown branches give a model at every budget. The river-valley picture (computed toy). Frontier practice; batch sizes grow. | Schedule shapes from the training code's own `lr_factor`. Cosine vs WSD on one pocket model (L3 d96) with the same 5M tokens: final {cos_final} vs {wsd_final}. WSD cooldown branches from 40% and 60%, beside a half-length cosine run. *Quoted:* DeepSeek-V3 held its peak LR for 10T tokens, then decayed over 4.3T; Llama 3 405B annealed over its last 40M tokens and averaged checkpoints; Kimi K3 chose cosine. |
| 10 | `Precision` | Fewer bits → more FLOP/s and less memory. Sign / exponent / mantissa in FP32, BF16, FP8 E4M3 and FP4 E2M1. Every value each format can hold. Scale factors and how many numbers share one. Outliers (massive activations) and block scaling (NVFP4). FP8 and NVFP4 at frontier scale. | Every positive E4M3 value (126, from 2⁻⁹ to 448) and E2M1 value (0.5, 1, 1.5, 2, 3, 4, 6). GPT-2 small's real residual stream after 6 blocks (45 tokens × 768 channels): channel 447 reaches ≈ 2,900 at the first token, a typical entry ≈ 1.2. FP4 with one scale flushes 99.99% of values to zero; NVFP4 (blocks of 16) keeps them at ≈ 12% error. " Paris" (first 64 channels) before and after NVFP4. *Quoted:* dense PFLOP/s: H100 BF16 0.989, FP8 1.979; B300 FP8 5, NVFP4 15. DeepSeek-V3 FP8 (1 × 128 tiles, within 0.25% of BF16); Nemotron 3 Ultra, 550B on 20T tokens in NVFP4. |
| 11 | `Stability` | Loss spikes in big runs. The same instabilities show up in small models at high learning rates. The mechanism: attention logits grow and the softmax goes one-hot. QK-norm. The toolbox: z-loss, clipping, warmup, initialization, MuonClip, DeepSeek-V4's clamping and re-routing. | 12 real pocket runs: final validation loss vs peak learning rate (3×10⁻⁴ … 10⁻¹), standard vs QK-norm {stab_note}. The largest q·k/√d over training at learning rate 0.03, standard vs QK-norm. *Quoted:* PaLM ≈ 20 spikes (restart ~100 steps back, skip 200–500 batches); OPT-175B 35+ restarts; Nemotron 3 Ultra 2 divergences; MuonClip caps scores at 100, zero spikes over 15.5T tokens. |
| 12 | `Memory` | Part 3. Training state = 16 bytes per parameter; activations and recomputation. Data parallelism. Ring all-reduce: reduce-scatter + all-gather, 2(N−1)/N per GPU. ZeRO-1/2/3 and FSDP shard the state for ~1.5× the communication. | Llama 3.1 405B × 16 bytes = 6.48 TB = 81 H100s just to hold the state; H100 80 GB, B200 192 GB, B300 288 GB. An exact ring all-reduce over 4 GPUs × 4 chunks, ending at [22, 20, 20, 18]. ZeRO for a 7.5B model on 64 GPUs: 120 → 31.4 → 16.6 → 1.9 GB per GPU. |
| 13 | `Parallelism` | Tensor parallelism: split by columns (no communication), then by rows (one all-reduce); Megatron-LM's two all-reduces each way, kept inside NVLink. Pipeline parallelism: the bubble, micro-batches, (p−1)/(m+p−1), Zero Bubble, DualPipe. Expert parallelism (all-to-all) and context parallelism (schematic). How real runs combine them. | A worked [1 2] · W₁ (2 × 4) · W₂ (4 × 2) split across 2 GPUs, giving [12 19] both ways. NVLink 450 GB/s vs ~50 GB/s between servers (≈ 9×). Exact pipeline timelines from a dependency simulator (4 stages, backward = 2× forward): idle 75% with 1 batch, 27% with 8 micro-batches. Llama 3.1 405B: 16,384 H100s = TP 8 × PP 16 × DP 128, ≈ 400 TFLOP/s per GPU (41% MFU). DeepSeek-V3: 2,048 H800s, no TP, 16-stage DualPipe, experts over 64 GPUs on 8 nodes. |
| 14 | `Operations` | More GPUs mean more failures. What interrupted Llama 3. Checkpoint, fail, restart; goodput. Silent data corruption; the power grid notices. | Meta's measured mean time to failure: 48 days at 8 GPUs, 7.9 h at 1,024; projected 1.8 h at 16,384 and 14 min at 131,072. Llama 3: 466 interruptions in 54 days on 16,384 GPUs, one every 2.8 h (tick positions illustrative). Causes of the 419 unexpected ones: faulty GPU 30.1%, HBM3 17.2%, software 12.9%, network 8.4%, host maintenance 7.6%, SRAM 4.5%, GPU system processor 4.1%. Over 90% of time spent training (Llama 3); 85% → 97% (Gemini). |
| 15 | `SFT` | Part 4. A base model completes documents; it is not an assistant. Chat template: one token stream with role and special tokens (here an empty think block). SFT = next-token loss on the assistant's tokens only. Where SFT data comes from; distillation. | Real greedy answers to "Where is the Eiffel Tower?": Qwen3-0.6B-Base writes a quiz ("A. Paris / B. London …", the answer key, the next question); Qwen3-0.6B answers "Paris, France". Qwen3's real chat format for a 3-turn conversation (44 tokens), prompt tokens masked out of the loss. *Quoted:* InstructGPT ≈ 13,000 demonstrations; LIMA 1,000; Tülu 3 939,344 prompts; OLMo 3 Think ≈ 2.3M prompts, ≈ 45B tokens; R1 distilled into Qwen2.5-32B scores 72.6% on AIME 2024 vs 47.0% for RL. |
| 16 | `Preferences` | Judging is easier than writing: pairwise comparisons (illustrative). Reward model and Bradley–Terry, P = σ(r_A − r_B). RLHF: maximize reward minus β·KL to the reference (schematic). Goodhart: over-optimizing a proxy. DPO (no reward model, no RL loop); Constitutional AI. | A best-of-n simulation (true quality g ~ N(0, 1); the reward model sees g plus heavy-tailed error), against √KL: the proxy reward keeps rising while true quality peaks at n ≈ 35, then falls below half its peak. |
| 17 | `RL` | RL with verifiable rewards (final answers, unit tests; reward 1 or 0). GRPO: sample a group, advantage = (r − mean)/std, no critic or reward model. RL raises pass@1 but not pass@k (debated at scale); groups where every answer agrees carry no signal (DAPO). DeepSeek-R1-Zero. Agentic RL with sandboxes and asynchronous rollouts (schematic). Reward hacking (illustrative). | A real miniature: a 3-layer pocket model with 334,944 parameters, pretrained on 384,000 three-digit additions, 40% of them with every carry dropped (347+285 = 0632 vs 0522). Its real group of 8 answers to 478+356: one 834 (A = +2.47), five 724, two 824 (A = −0.35). On held-out problems over 120 GRPO steps (32 prompts × 8): pass@1 goes from ≈ 60% to over 93% while pass@8 stays flat near the top; groups where all 8 agree pass 50%; at the end, 834 eight times out of eight. *Quoted:* R1-Zero AIME 2024 15.6% → 71.0%, the "aha moment" line; DeepSeek-V3.2 > 1,800 environments and > 10% of pretraining compute; OLMo 3's learner waits for rollouts 75% of the time. |
| 18 | `Outro` | Evaluation before release (capability benchmarks, safety tests, system card; contamination). The whole pipeline in one picture. Pocket scale vs frontier scale. Most of what is known comes from open-weight labs; open end-to-end projects. | Read from the cached runs: largest pocket model 2.9M parameters (the 8-expert MoE) vs up to 2.8T (Kimi K3); 12M tokens in one run vs 33T (DeepSeek-V4); all pocket training {pocket_flops} vs ~10²⁷ FLOPs; 4 CPU cores vs 100,000+ GPUs. *Quoted:* OpenAI stopped reporting SWE-bench Verified (Feb 2026); pipeline notes (13% of pages survive, 15–36T tokens, 10²⁵–10²⁷ FLOPs, 10⁴–10⁵ GPUs). |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| raw web pages, HTML | grey |
| text that survives filtering | teal |
| removed by a filter; wrong answers; negative advantage | red |
| near-duplicates, MinHash | orange |
| quality scores; reward models | gold |
| model size *N*; weights | blue |
| training tokens *D*; forward pass; activations | green |
| compute *C*, FLOPs | yellow |
| learning rate | pale gold |
| AdamW / Muon | light blue / pink |
| experts | lilac |
| sign / exponent / mantissa bits | red / green / blue |
| gradients; backward pass | orange |
| optimizer state | lilac |
| communication between GPUs | yellow |
| pipeline bubble (idle) | dark grey |
| correct answers, positive advantage, assistant tokens | green |

## Real footage (`compute.py`)

| Item | What | Used in |
|---|---|---|
| `funnel` | The first 400 MiB of WARC file 0 of CC-MAIN-2026-39 (10,498 HTML responses) through the whole FineWeb recipe with datatrove's own filters: URL blocklist → Trafilatura → fastText English > 0.65 → Gopher repetition → Gopher quality → C4 → FineWeb rules. Per-stage counts and bytes, rejection reasons, example pages, language counts; the 1,363 survivors go on to `edu`. | 2, 3, 5 |
| `corpus` | WET files 0, 12,500, …, 87,500 (8 of 100,000; 169,783 pages of Common Crawl's own text extraction) through the same filters from the URL stage on, in 4 processes. | 4 |
| `dedup` | MinHash LSH over that corpus with FineWeb's settings: 5-word shingles, 14 bands × 8 rows = 112 hashes (SplitMix64 hash family). Cluster sizes, pages from the biggest clusters, estimated vs exact Jaccard for one pair from each of the 40 biggest clusters. | 4 |
| `edu` | `HuggingFaceFW/fineweb-edu-classifier` on 400 seeded-random survivors of `funnel` (first 512 tokens). | 5 |
| `tokenizer` | Byte-level BPE with 2,048 tokens (including a `<\|doc\|>` separator), trained with Hugging Face `tokenizers` on 60,000 FineWeb-Edu documents (`karpathy/fineweb-edu-100b-shuffle`, shards 0–1). Everything except 2,000 held-out documents is encoded to `uint16` (168.2M training tokens, 2.97 bytes per token). | 5; the text of every pocket run |
| `sweeps` | Every pretraining run below in one pool: 20 + 2 + 5 + 12 + 3 = 42 runs, longest first, four single-threaded runs side by side. Each run is cached on its own in `runs/<name>.json`, so an interrupted sweep resumes. | 6–9, 11; 1 and 18 total their FLOPs |
| `isoflop` | PocketGPT (`explainer/lm/pocket.py`: RMSNorm, RoPE, SwiGLU, no biases; vocabulary 2,048, context 256, batch 16). Budgets of 10¹² (4 sizes), 3×10¹² (5), 10¹³ (6) and 3×10¹³ (5) FLOPs over (layers, width) from (1, 32) to (5, 160): 20 runs. Each trains on budget ÷ (6N + attention) tokens with AdamW and a cosine schedule, peak learning rate 3.5×10⁻³·(128/d)^¼. | 6 |
| `optim` | AdamW (3.5×10⁻³) vs Muon (6×10⁻³; AdamW for embeddings, norms and the output layer) on L4 d128 (≈ 1M parameters), 12M tokens, WSD with a 30% cooldown, same seed and batches. | 8 |
| `schedule` | L3 d96 (≈ 0.5M parameters), 5M tokens: cosine and WSD (20% cooldown) at full length, WSD at 50% and 75% length (the cooldown branches, starting at 40% and 60%), cosine at 50%: 5 runs. | 9 |
| `stability` | L4 d128, 800,000 tokens per run, peak learning rates 3×10⁻⁴, 10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹, without and with QK-norm: 12 runs. The largest attention logit is probed every 10 steps. | 11 |
| `moe` | L4 d128 with 8 experts per layer, top-2, 2M tokens. Balancing: none / Switch-style auxiliary loss / DeepSeek-V3 bias; per-expert load logged every 5 steps: 3 runs. | 7 |
| `muon_svd` | An L4 d128 pocket model trained for 400 steps (1.6M tokens), then one real gradient of `blocks.2.mlp.up.weight` (336 × 128): its singular values, those of the AdamW update, and those after each of 5 Newton–Schulz iterations (3.4445, −4.7750, 2.0315). | 8 |
| `precision` | GPT-2 small's residual stream after 6 blocks on a 45-token paragraph (45 × 768), rounded to the nearest representable value under BF16, FP8 per tensor, FP8 1 × 128 tiles, MXFP8, FP4 per tensor, MXFP4 (32-element blocks, E8M0 scales) and NVFP4 (16-element blocks, E4M3 scales + an FP32 tensor scale). | 10 |
| `chat` | `Qwen/Qwen3-0.6B`'s chat template on a 3-message conversation (token pieces, IDs, prompt length for the loss mask), and greedy answers to "Where is the Eiffel Tower?" from Qwen3-0.6B-Base (plain text) and Qwen3-0.6B (chat template, thinking off), fp32 on CPU. | 15 |
| `toy_rl` | A 3-layer, width-96 PocketGPT over 13 characters, pretrained for 3,000 AdamW steps × 128 three-digit additions in which 40% of the answers drop every carry (loss on answer tokens only). Then GRPO: 120 steps × 32 prompts × 8 samples, reward = exact answer. Every 10 steps: pass@1, pass@8 and greedy accuracy on 400 held-out problems, and the group for 478 + 356 at steps 0 and 120. | 17 |
| `goodhart` | A best-of-n simulation with no model: n from 1 to ≈ 20,000 (log-spaced); true quality g ~ N(0, 1), proxy g + 0.6·t₃; KL = log n − (n−1)/n. | 16 |
| `epoch` | Epoch AI's *Data on AI models* (`notable_ai_models.csv`, CC BY 4.0): every model with a training-compute estimate. | 1 |

Scenes never train or run a model; they `load()` the cached JSON/NPZ in
`.cache/frontier/` (`Hook` and `Outro` also total the per-run files in `runs/`).
Measured numbers the narration states are asserted against the data at render
time (e.g. `assert agree == 86` in `Dedup`, `assert (right, wrong) == (834, 724)`
in `RL`), so a rerun that disagrees with the script fails loudly instead of
silently contradicting the voice-over.

## Fact-check notes and sources

Status: **as of October 8, 2026**. Closed labs (OpenAI, Anthropic, Google DeepMind, xAI) publish almost
nothing about how their models are trained; the recipes on screen come from open-weight labs' reports.
Numbers marked *real run* were computed for this video by `compute.py`; everything else is quoted.

### Part 1 – The data
* **Common Crawl CC-MAIN-2026-39** (September 2026): 2.17 billion pages, 105.92 TiB compressed, 100,000
  WARC / WAT / WET files each (crawl statistics page, <https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-39/index.html>).
  We downloaded WET files 0, 12500, …, 87500 (8 files, 169,783 pages) and the first 400 MiB of WARC file 0
  (10,498 HTML responses). The WARC is the raw twin of the first WET file.
* **FineWeb**: Penedo et al., *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*
  (NeurIPS 2024, arXiv 2406.17557) and the FineWeb blog. Pipeline as in `datatrove/examples/fineweb.py`:
  URL filter → Trafilatura(favour_precision) → fastText language ID (English, > 0.65) → Gopher repetition →
  Gopher quality → C4 (without the terminal-punctuation rule) → FineWeb rules → per-dump MinHash (5-grams,
  14 × 8). 15T tokens from 96 dumps at release. WET text "keeps too much boilerplate" and trained worse models.
  Global dedup of 2013-48 removed ~94% of tokens and the kept data was "actually worse".
  **Filters run here are datatrove's own code** (v0.10.1, defaults; `LanguageFilter(languages=["en"])`
  because current datatrove keeps every language by default). Note: datatrove's defaults differ slightly from
  the papers in two places (FineWeb's duplicated-line character ratio is 0.01 in code vs 0.1 in the paper;
  the C4 filter's sentence/word minimums are 5/3 in code vs 3/5 in C4) – the video uses the code.
* URL blocklist: 4,558,939 domains and 19,586 URLs in datatrove's integrated list (measured by counting).
* **Gopher rules**: Rae et al. 2021 (arXiv 2112.11446), Table A1 and Sec. A.1.1. **C4**: Raffel et al. 2020.
* **MinHash LSH**: Broder 1997; banding P(s) = 1 − (1 − s^r)^b. Our implementation uses FineWeb's parameters
  (5-grams, 14 bands × 8 rows) with a SplitMix64 hash family; estimates checked against exact Jaccard (mean
  error < 10⁻⁴ on 300 random pairs).
* **FineWeb-Edu**: Llama-3-70B-Instruct annotated 500k samples (0–5); classifier on Snowflake-arctic-embed-m
  trained on 450k; threshold 3 keeps 1.3T tokens (removes 92%); 6,000 H100 GPU-hours to score 15T tokens;
  matches C4/Dolma MMLU "with 10x fewer tokens". Classifier: `HuggingFaceFW/fineweb-edu-classifier` (run here).
* **Nemotron-CC**: Su et al. 2024 (arXiv 2412.02595): 6.3T tokens = 4.4T real + 1.9T synthetic (rephrasing and
  QA generation with Mistral NeMo 12B).
* **Kimi K2 rephrasing**: Kimi K2 report (arXiv 2507.20534): SimpleQA 23.76 (raw, 10 epochs) → 28.94
  (10 rephrasings, 1 epoch).
* **OLMo 3**: Ai2, *OLMo 3* (arXiv 2512.13961): quality-aware upsampling capped at 7×; Dolma 3 mix 5.93T;
  Dolmino mid-training 100B tokens; Think SFT 2,268,468 prompts for the 7B and 2,253,916 for the 32B
  (~45B tokens); "our learner spends 75% of the time waiting for data" in RL.
* **Llama 3**: Llama Team, *The Llama 3 Herd of Models* (arXiv 2407.21783): mix ≈ 50% general knowledge, 25%
  math and reasoning, 17% code, 8% multilingual; 15.6T tokens (405B); annealing raised Llama 3 8B GSM8K by
  24.0% and MATH by 6.4%; IsoFLOP experiments up to 10²² FLOPs predicted 402B parameters on 16.55T tokens;
  16,384 H100s with TP 8 × CP 1 × PP 16 × DP 128, ~400 TFLOPs/GPU, 41% BF16 MFU (Table 4); 466 job
  interruptions in 54 days, 419 unexpected, ~78% attributed to hardware (Table 5; the video shows the
  percentages as printed. Note the paper's "Faulty GPU" row is internally inconsistent: 148 of 419 is 35.3%, but
  30.1% is printed; every other row matches count / 419);
  power swings "on the order of tens of megawatts"; > 90% effective training time.
* **Tokens per model**: DeepSeek-V3 14.8T (arXiv 2412.19437); Kimi K2 15.5T; Qwen3 36T (arXiv 2505.09388);
  GLM-5 28.5T (arXiv 2602.15763); DeepSeek-V4-Pro 33T (arXiv 2606.19348, April 2026).
* **Tokenizers**: GPT-2 50,257; Llama 3 128,256; Gemma 3 262,208; Qwen3 151,669; gpt-oss 201,088.
  Ours: byte-level BPE, 2,048 tokens, trained with Hugging Face `tokenizers` on FineWeb-Edu
  (`karpathy/fineweb-edu-100b-shuffle`, shards 0–1); 168.2M training tokens, 2.97 bytes per token.

### Part 2 – The recipe
* **C ≈ 6ND**: Kaplan et al. 2020 (arXiv 2001.08361). Our FLOP count adds attention (6 · layers · seq · d / 2
  per token) to 6N on the matrices each token multiplies through (body + unembedding).
* **Chinchilla**: Hoffmann et al. 2022 (arXiv 2203.15556): > 400 models, 70M–16B parameters, 5–500B tokens;
  Eq. 10 fit L = 1.69 + 406.4/N^0.34 + 410.7/D^0.28 (the heat map is this formula, not new data);
  ≈ 20 tokens per parameter; Chinchilla 70B on 1.4T tokens beat Gopher 280B. GPT-3: 175B parameters, 300B
  tokens (Brown et al. 2020).
* **Overtraining**: Llama 3 8B trained on 15T tokens (Meta blog, Apr 2024) = 1,875 tokens per parameter;
  tokens per active parameter: DeepSeek-V3 ≈ 400, Qwen3-235B-A22B ≈ 1,640 (arithmetic).
* **Architectures**: DeepSeek-V3: 671B total / 37B active, 256 routed + 1 shared experts, top-8, auxiliary-
  loss-free balancing with bias speed γ = 0.001 (arXiv 2412.19437, and Wang et al. arXiv 2408.15664).
  Kimi K2: 1.04T / 32.6B, 384 experts, top-8, MuonClip with τ = 100, "zero loss spike" over 15.5T tokens.
  Kimi K3: 2.8T total, 16 of 896 experts, ~3:1 linear (KDA) to full attention, chose cosine over WSD
  (arXiv 2607.24653, July 2026). Qwen3.5-397B-A17B: 15 × (3 Gated DeltaNet + 1 gated attention).
  DeepSeek-V3.2 sparse attention: top-2048 tokens per query (arXiv 2512.02556).
* **Muon**: K. Jordan et al., <https://kellerjordan.github.io/posts/muon/> and `KellerJordan/Muon` (quintic
  Newton–Schulz, coefficients (3.4445, −4.7750, 2.0315), 5 steps). Moonlight (Liu et al., arXiv 2502.16982):
  update RMS matched to AdamW (0.2·√max(A, B)), "only requires about 52% training FLOPs". GLM-4.5/5,
  DeepSeek-V4 (Muon with AdamW for embeddings, head and norms), Kimi K3 (per-head Muon) use Muon variants.
  Wen et al., *Fantastic Pretraining Optimizers and Where to Find Them* (arXiv 2509.02046): speedup 1.4× at
  0.1B, 1.1× at 1.2B.
* **Schedules**: WSD: MiniCPM (arXiv 2404.06395); Hägele et al. 2024 (arXiv 2405.18392); river valley:
  Wen et al. 2024 (arXiv 2410.05192). DeepSeek-V3: 2.2e-4 constant to 10T tokens, cosine decay over 4.3T;
  batch 3,072 → 15,360 sequences. Llama 3 405B: cosine; last 40M tokens annealed to 0; Polyak averaging.
* **Precision**: OCP MX spec (32-element blocks, E8M0 scales); FP8 formats (Micikevicius et al. 2022).
  DeepSeek-V3: FP8 with 1 × 128 activation tiles and 128 × 128 weight blocks, FP32 promotion every 128
  elements, relative loss error < 0.25% vs BF16. NVFP4: NVIDIA, *Pretraining LLMs with NVFP4*
  (arXiv 2509.25149): 16-element blocks with E4M3 scales + FP32 tensor scale, random Hadamard transforms,
  stochastic rounding. Nemotron 3 Ultra (arXiv 2606.15007): 550B total / 55B active, 20T tokens, pretrained in
  NVFP4 with the final ~15% of layers in higher precision; two divergences, the first traced to BF16 gradient
  accumulation. Throughput: H100 SXM 989 TFLOP/s BF16 and 1,979 FP8 dense; B300 15 PFLOP/s NVFP4 dense
  (NVIDIA datasheets / Blackwell Ultra blog).
* **Stability**: PaLM (Chowdhery et al. 2022): ~20 spikes; restart ~100 steps earlier and skip 200–500
  batches; z-loss 10⁻⁴·log²Z. OPT-175B (Zhang et al. 2022): 35+ manual restarts. Wortsman et al.,
  *Small-scale proxies for large-scale Transformer training instabilities* (arXiv 2309.14322).
  QK-norm: Dehghani et al. 2023; used by Qwen3, OLMo 2/3, GLM-4.5. DeepSeek-V4: SwiGLU clamping and
  "Anticipatory Routing" after a detected spike.

### Part 3 – Scaling out
* **16 bytes per parameter**, ZeRO stages and the 7.5B / 64-GPU example (120 → 31.4 → 16.6 → 1.9 GB):
  Rajbhandari et al., *ZeRO* (arXiv 1910.02054). Ring all-reduce: 2(N−1)/N × size per GPU.
* **Tensor parallelism**: Shoeybi et al., *Megatron-LM* (arXiv 1909.08053): two all-reduces forward, two
  backward per layer. NVLink4 on H100: 900 GB/s total (450 GB/s each way); ConnectX-7 400 Gb/s ≈ 50 GB/s.
* **Pipelines**: bubble (p−1)/(m+p−1) (Narayanan et al. 2021); timelines on screen are computed by an exact
  dependency simulator in `s13_parallelism.py`. Zero Bubble (Qi et al., arXiv 2401.10241); DualPipe
  (`deepseek-ai/DualPipe`). DeepSeek-V3: 2,048 H800s, PP 16 (DualPipe), EP 64 across 8 nodes, ZeRO-1, no TP.
* **Reliability**: Kokolis et al. (Meta), *Revisiting Reliability in Large-Scale Machine Learning Research
  Clusters* (arXiv 2410.21680): MTTF 47.7 days at 8 GPUs, 7.9 h at 1,024; projected 1.8 h at 16,384 and
  0.23 h at 131,072. Gemini Team 2023 (arXiv 2312.11805): redundant in-memory copies raised goodput 85% → 97%;
  silent data corruption expected "every week or two".

### Part 4 – Post-training
* **Chat template**: Qwen3-0.6B's tokenizer, rendered with `apply_chat_template` (real tokens). Base vs chat
  outputs: Qwen3-0.6B-Base and Qwen3-0.6B, greedy, 48 new tokens (real outputs).
* **SFT data**: InstructGPT (Ouyang et al. 2022) ~13k demonstrations; LIMA (Zhou et al. 2023) 1,000 examples;
  Tülu 3 (Lambert et al., arXiv 2411.15124) 939,344 prompts; OLMo 3 Think SFT 2,268,468 prompts.
  DeepSeek-R1-Distill-Qwen-32B 72.6% AIME 2024 vs 47.0% for RL on Qwen-32B-Base (R1 paper v1, Table 6).
* **Preferences**: Bradley & Terry 1952; InstructGPT RLHF with KL penalty; DPO (Rafailov et al.,
  arXiv 2305.18290); Constitutional AI (Bai et al., arXiv 2212.08073); reward-model overoptimization
  (Gao, Schulman & Hilton, arXiv 2210.10760). The Goodhart plot is our own best-of-n simulation (heavy-tailed
  proxy error, Student-t with 3 degrees of freedom), plotted against √KL with KL = log n − (n−1)/n.
* **RLVR**: GRPO (DeepSeekMath, arXiv 2402.03300); DeepSeek-R1 (arXiv 2501.12948): R1-Zero AIME 2024 pass@1
  15.6% → 71.0% (v1; 77.9% in the Nature 2025 version), the "aha moment" quote; DAPO (arXiv 2503.14476):
  clip-higher, dynamic sampling, token-level loss; Yue et al., *Does Reinforcement Learning Really Incentivize
  Reasoning Capacity in LLMs Beyond the Base Model?* (arXiv 2504.13837); ProRL (arXiv 2505.24864).
  DeepSeek-V3.2: post-training budget > 10% of pretraining, > 1,800 synthesized environments.
  Reward hacking: MacDiarmid et al., *Natural Emergent Misalignment from Reward Hacking in Production RL*
  (Anthropic, arXiv 2511.18397). The prime-checker code is illustrative.
* **Evaluation**: OpenAI stopped reporting SWE-bench Verified on Feb 23, 2026, citing contamination
  (<https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/>).

### Context
* **Training compute data**: Epoch AI, *Data on AI models* (CC BY 4.0), <https://epoch.ai/data/ai-models>,
  `notable_ai_models.csv` retrieved Oct 8, 2026. Values are Epoch's estimates, not lab disclosures; e.g. GPT-6
  Astra (Sep 2026) 1e27 FLOP ("Likely"; OpenAI said only that it was its largest run and the first pretrained on
  more than 100,000 GPUs at its Stargate site in Texas, Fortune, Sep 3, 2026), Grok 4 5e26 ("Speculative"), Llama 3.1-405B 3.8e25 ("Confident"). The ×4.8/year line
  is a least-squares fit to Epoch's "frontier" models since 2018 (Epoch's own estimate: 4–5×/year).
* **Open end-to-end projects**: Karpathy, `nanochat` (GPT-2-grade model for ~$48–100 on one 8×H100 node);
  Ai2 OLMo 3 (all data, code and checkpoints); Hugging Face, *The Smol Training Playbook* (2025) and
  *The Ultra-Scale Playbook* (2025).

