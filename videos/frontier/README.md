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
crawl, MinHash on 170,000 more, FineWeb-Edu's classifier, a 21-run IsoFLOP
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

<!-- OUTLINE -->

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

<!-- DATA -->

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

