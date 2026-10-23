# AI, Built — Part 18: Pretraining at Scale

Part 18 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How a frontier language model is pretrained: where the text comes from and how it
is cleaned (extraction, language identification, MinHash deduplication, quality classifiers, contamination checks,
mixtures, synthetic data and model collapse); what the model is asked to predict and how training is staged
(objectives, warmup–stable–decay, annealing and mid-training, long context); the arithmetic of a run in operations and
bytes; the five ways to cut a model across devices (data, ZeRO/FSDP, tensor, pipeline, context, expert) and how much
of the hardware a run really uses; training in fewer bits (BF16, FP16 with loss scaling, FP8 with fine-grained scales,
MXFP8, NVFP4); keeping the run stable (QK-norm, z-loss, QK-Clip with Muon); multi-token prediction; and surviving
failures at sixteen thousand GPUs. Everything that can be measured on one computer is: a sample of Common Crawl's
September 2026 crawl goes through the whole data pipeline, four processes of this computer act as a cluster through
PyTorch's own distributed library, and a dozen training runs on the series' thirty novels test each piece, ending with
a model trained with the full 2026 recipe against the 2020 one, on the scoreboard.

* **Sixteen thousand GPUs, fifty-four days.** Chips on one training run, 2018–2025 (GPT-1's eight GPUs for a month to
  Llama 4 Behemoth's 32,000; log scale); Llama 3's run as 16,384 dots: 3.8 × 10²⁵ FLOP, 15.6T tokens, 466 interruptions
  in 54 days (419 unplanned), one every 3.1 hours (computed); the question; the miniature; the plan.
* **1. Anatomy of a frontier run.** The pipeline from crawl to post-training; Olmo 3 (5.9T + 100B mid-training + 50B
  long context) and SmolLM3 (three stages) drawn to scale; six runs of 2024–26 (Llama 3.1 405B, DeepSeek-V3, Kimi K2,
  Olmo 3, Nemotron 3 Super, DeepSeek-V4-Pro): tokens, chips, number format, optimizer; DeepSeek-V3's learning-rate,
  batch-size and MTP-weight schedules; C ≈ 6ND for Llama 3.1 (3.79 × 10²⁵ against the reported 3.8) and DeepSeek-V3
  (37B active); 2.788M H800 GPU-hours, $5.576M, 180k GPU-hours (3.7 days on 2,048 GPUs) per trillion tokens.
* **2. From the web to text.** Common Crawl (Gil Elbaz, 2007; crawls since 2008; over 10 PB), WARC and WET; our sample
  (3 WET files × 3 slices of 3 MiB from CC-MAIN-2026-39); extraction with Trafilatura on WARC slices (HTML bytes →
  text bytes; one page shown; FineWeb's WARC-vs-WET ablation); a URL blocklist; fastText's lid.176 language
  identifier, FineWeb's 0.65 threshold, 50-word minimum: the funnel to the English pages that go on.
* **3. Near-duplicates: MinHash and LSH.** Duplicates and memorization (Lee et al. 2022: ten times less memorized
  text); shingles (word 5-grams) and Jaccard similarity; MinHash (Broder 1997) derived: Pr[min agree] = J; checked on
  3,000 page pairs; banding derived: 1 − (1 − s^r)^b with FineWeb's 14 bands of 8; the S-curve predicted and measured;
  results: our sample, the thirty Gutenberg licence pages (all 435 pairs caught, no novel pair), Olmo 3's exact /
  MinHash / substring deduplication (67% / 23% / 14% of bytes; 38.7B → 9.7B documents), FineWeb's per-crawl finding.
* **4. Quality, and keeping the test clean.** FineWeb-Edu (Llama-3-70B's additive 0–5 prompt on 460k pages, a linear
  head on an embedding model trained on 410k, F1 82% at 3, 1.3T tokens; MMLU 33 → 37%, ARC 46 → 57% at 1.71B/350B);
  our fastText classifier trained on 13,000 of the released annotations (F1, precision, recall against theirs); its
  verdicts on our crawl sample; DCLM; contamination: GPT-3's 13-gram check applied to the scoreboard's passage and to
  our held-out text (computed).
* **5. Mixtures, synthetic data and collapse.** The Pile's hand-set weights; DoReMi (280M proxy, Group DRO, 8B: +6.5
  points, 2.6× fewer steps); RegMix (512 models of 1M parameters, regression; the best of 64 mixtures at 1B); our
  RegMix on four groups of the novels, targeted at chapters 1 and 3 of *The Maltese Falcon* and tested on chapter 2
  (32 proxy runs, leave-one-out fit, the pick against the natural and uniform mixtures at a larger size, two seeds);
  repetition (Muennighoff et al.: about four epochs are as good as new data); rephrasing (WRAP, ~3× faster; Kimi K2's
  SimpleQA 23.76 → 27.39 → 28.94); model collapse in a unigram model (replace against accumulate; Shumailov et al.,
  Gerstgrasser et al.).
* **6. What the model is asked to predict.** One sentence of *Pride and Prejudice* under the causal, masked (15%;
  80/10/10), span-corruption (15%, spans of ~3, sentinels) and fill-in-the-middle (PSM) objectives; prediction targets
  per 256 tokens; FIM for free (Bavarian et al. 2022); DeepSeek-V3's FIM rate of 0.1.
* **7. Annealing, mid-training, long context.** Cosine against warmup–stable–decay (MiniCPM; Hägele et al.); our
  2026-recipe run and a cooldown branched from its middle; annealing on the best data (Llama 3's last 40M tokens;
  Qwen3's 5T stage 2; Olmo 2's mid-training and microanneals; SmolLM3's stage mixtures); long-context stages (Llama 3,
  DeepSeek-V3, Qwen3, Olmo 3, DeepSeek-V4) and RoPE's slowest wavelength 2π θ^{(d−2)/d} for θ = 10⁴, 5 × 10⁵, 10⁶
  (computed).
* **8. Counting FLOPs and bytes.** 6ND derived (2 forward, 2 + 2 backward); PyTorch's FLOP counter on our model
  (backward = 2 × forward; total = 6NT; attention's extra share); 16 bytes per parameter in mixed-precision Adam (ZeRO's
  2 + 2 + 12); Llama 3.1 405B's 6.5 TB, DeepSeek-V3, Kimi K2; activations counted from autograd's saved tensors against
  sequence length (fused attention: linear; unfused: + a T × T matrix per head; recomputed: one d per token per layer);
  Korthikanti et al.'s sbh(34 + 5as/h) at Llama 3.1's shape.
* **9. Data parallelism and the all-reduce.** Copies of the model, slices of the batch; 4 processes against one,
  checked; the ring all-reduce as reduce-scatter + all-gather on a ShardGrid; the bandwidth lower bound 2(p−1)/p · n/B
  proved (Patarasuk & Yuan 2009); all-reduce, reduce-scatter and all-gather timed with torch.distributed (gloo) against
  the α–β model.
* **10. ZeRO and FSDP.** ZeRO's three stages (Rajbhandari et al. 2019) on a ShardGrid; memory per GPU derived (the
  paper's 120 / 31.4 / 16.6 / 1.9 GB, computed); communication (2Ψ, 2Ψ, 3Ψ); FSDP; Llama 3 (FSDP) and DeepSeek-V3
  (ZeRO-1); our ZeRO-3 on four processes, layer by layer, against one process: parameters, memory and traffic measured.
* **11. Tensor parallelism.** Megatron-LM's column-then-row split of the MLP derived, the f and g operators;
  attention by heads; four all-reduces per layer; TP inside the NVLink domain (Llama 3: TP 8, innermost); sequence
  parallelism; one block of our model split across 2 and 4 processes, checked against the whole block.
* **12. Pipeline parallelism.** GPipe (Huang et al. 2019) as a Gantt chart filling in (simulated exactly); the bubble
  (p − 1)/(m + p − 1) derived and checked against simulations for p = 4, 8, 16; 1F1B's memory; interleaving (Llama 3);
  ZB-H1 (Qi et al. 2024: (p − 1)(F + B − W)); DualPipe's bubble formula (DeepSeek-V3, Table 2).
* **13. Context, experts, and utilization.** Ring attention (Liu, Zaharia & Abbeel 2023) on four processes, exact;
  causal load imbalance and the 2 × CP chunk assignment (Llama 3); expert parallelism and all-to-all (DeepSeek-V3: EP
  64 over 8 nodes, ≤ 4 nodes per token, IB 50 against NVLink 160 GB/s, 20 of 132 SMs for communication); Llama 3's 4D
  layouts (Table 4); MFU defined (PaLM 45.7%/46.2%, computed), MegaScale 55.2%, Llama 3 38–43%, Olmo 3 43%; our runs'
  MFU on this CPU.
* **14. Fewer bits.** Formats on a log₂ scale with the measured distribution of our activation gradients (the share
  below FP16's normal and subnormal range); loss scaling derived (Micikevicius et al. 2018), dynamic scaling; six
  training runs (FP32, BF16, FP16 without and with loss scaling, FP8 per tensor, FP8 per tile), two seeds; the same in
  FP16 with each step accumulated over 64 micro-batches; per-tensor against per-tile E4M3 error on the series' model;
  DeepSeek-V3's FP8 recipe (1 × 128 and 128 × 128 scales, FP32 promotion every 128, < 0.25% loss error); MXFP8 (8B/15T),
  NVFP4 (12B/10T, MMLU-Pro 62.58 against 62.62), Nemotron 3 Super (NVFP4, 25T), Kimi K3 and DeepSeek-V4 (FP4 QAT).
* **15. Keeping the run stable.** PaLM's ~20 spikes and rollbacks; attention-logit growth and QK-norm (bound derived);
  our learning-rate sweep (plain / QK-norm / QK-norm + z-loss, 2 seeds): largest attention logit and final loss; the
  z-loss derived and log Z measured; Muon at scale (Moonlight ~2×), Kimi K2's QK-Clip (τ = 100, 12.7% of heads, 15.5T
  tokens without a spike), DeepSeek-V4's anticipatory routing and SwiGLU clamping.
* **16. Predicting two tokens ahead.** Gloeckle et al. 2024 (13B: +12% HumanEval, +17% MBPP; worse at the smallest
  sizes); DeepSeek-V3's sequential MTP module (λ 0.3 → 0.1; 85–90% acceptance, 1 + a tokens per step, 1.8× TPS); our
  model with and without the module, two seeds, and the module's cost in FLOPs per token (`mtp_cost`: in a model
  this small the second pass through the output head dominates); its acceptance rate in greedy self-speculation.
* **17. When hardware fails.** Llama 3's interruptions by cause (Table 5), MTBF 3.1 h, per-GPU ~5.8 years (computed),
  >90% effective training, diurnal 1–2%, power swings; Young's checkpoint interval √(2δM) derived (δ from Llama 3's
  checkpoint sizes and storage bandwidth); a 54-day run with random failures simulated over checkpoint intervals.
* **18. Our own full recipe.** The 2020 recipe (AdamW, cosine) against the 2026 recipe (Muon, WSD, QK-norm, z-loss) at
  equal model, data, steps and seed, and the whole comparison again from a second seed (the verdict must beat the
  spread between seeds); a training replay (held-out loss and samples at the same steps); held-out loss, bits per
  character, largest attention logit; the scoreboard row against Parts 1 and 14 and the series' model.
* **Recap**, where it comes back (Parts 19, 22–23, 27, 28, 30, 31), the problem set, Part 19's teaser, references.

Run from the repo root:

```
python tools/make.py ai18                   # everything: Part 1's text, the novels model, Part 14, these numbers, both cuts
python -m videos.ai.ai18.compute            # just the numbers (about 5 CPU-hours on a busy 4-core machine; resumable)
python -m videos.ai.ai18.compute mixture --force
python tools/qa_scene.py ai18 Pipeline      # one chapter, silent, with a contact sheet
```

Every random choice is seeded (numpy `default_rng`, `torch.manual_seed`, fastText's seed, data order by step); the
training runs checkpoint every 100 steps and resume, and items made of many runs (`precision`, `stability`, `mtp`,
`mixture`, `recipe_seed1`) save each run as it finishes. Most of the time goes to the four recipe runs (two recipes ×
two seeds, 732 steps of a 128-wide, 4-layer model, about 40 minutes each here); the rest of the part takes about an
hour and a half. The distributed experiments start their processes with `spawn` and use
PyTorch's gloo backend, so they run on macOS and Linux. Downloads (Common Crawl byte ranges, fastText's `lid.176.ftz`,
FineWeb-Edu's annotations through Hugging Face's dataset viewer) are fixed and cached in `.cache/ai18/crawl/`.
Part 1's books and passage are read through `videos.ai.ai1.compute`, Part 14's scoreboard through
`videos.ai.ai14.compute`, and the series' model through `explainer.ai.novels`, so `tools/make.py` computes them first.

`facts.py` holds every published number with its source; `compute.py` derives the rest and runs the experiments;
`lm.py` is the training loop (precision emulation, the MTP module, mixtures, checkpoints); `web.py` the data
pipeline; `dist.py` the distributed workers; `sched.py` the pipeline simulator.

## Computed results

Filled in from `.cache/ai18/` after `compute.py` runs (`python -m videos.ai.ai18.results`):

<!-- results -->
<!-- /results -->

## Fact-check notes

Checked against the primary sources on 23 October 2026 (arXiv papers and technical reports, model cards, vendor and
lab pages):

* Llama 3: Table 4 (TP, CP, PP, DP, TFLOP/s, MFU), Table 5's counts (the table's percentages don't divide by 419;
  only counts are shown), "higher than 90%" effective training time, three manual interventions, 1–2% diurnal
  variation, "tens of megawatts", checkpoints of 1 MB to 4 GB per GPU, Tectonic at 2 TB/s sustained, the 2 × CP chunk
  split, annealing over the last 40M tokens, six long-context stages over ~800B tokens, RoPE base 500,000.
* DeepSeek-V3: E4M3 on all tensors (a custom E5M6 for a few activations), 1 × 128 / 128 × 128 scales, promotion every
  128 elements, ~14-bit accumulation (~2% error at K = 4096), < 0.25% loss error; Table 2's bubble formulas; 2,048
  H800s, NVLink 160 GB/s, IB 50 GB/s, 20 of 132 SMs; PP 16, EP 64 over 8 nodes, ZeRO-1, ≤ 4 nodes per token; the
  learning-rate, batch and MTP schedules; FIM 0.1 (PSM); YaRN 4K → 32K → 128K; 2.788M GPU-hours.
* DeepSeek-V4 (arXiv 2606.19348, April 2026): Muon (hybrid Newton–Schulz, 10 iterations), RMSNorm on queries and KV
  instead of QK-Clip, 32T (Flash) and 33T (Pro) tokens, batches to 75.5M / 94.4M tokens, MTP 0.3 → 0.1, anticipatory
  routing and SwiGLU clamping, 4K → 16K → 64K → 1M, FP4 QAT for experts in post-training.
* Kimi K2: MuonClip, τ = 100, 12.7% of heads clipped in the first 70k steps, 15.5T tokens without a spike, H800
  cluster (count not stated), the rephrasing table. Kimi K3's model card: MXFP4 weights and MXFP8 activations from QAT
  (no training details used). Moonlight: "~2× computational efficiency".
* Nemotron 3 Super (NVIDIA, March 2026): 120B / 12B active, NVFP4 pretraining, 25T tokens, MTP layers. NVFP4 paper:
  12B on 10T tokens, MMLU-Pro 62.58 vs 62.62, 16% of linear layers in BF16, 16 × 16 Hadamard transforms. MXFP8 paper:
  up to 8B parameters, 15T tokens.
* FineWeb / FineWeb-Edu: 96 snapshots, 15T tokens, lid ≥ 0.65, 5-grams, 112 hashes = 14 × 8; global vs per-snapshot
  dedup; 460k annotations (the released dataset has 467,424 rows), 410k for training, F1 82%, 6,000 H100 hours, 1.3T
  tokens, MMLU 33 → 37, ARC 46 → 57; the prompt is paraphrased on screen.
* Olmo 3: 5.9T pretraining, 100B midtraining, 50B/100B long context to 65K, 1,024 H100s, 43%/41% MFU; deduplication
  67% exact, 23% MinHash, 14% of bytes by substrings, 38.7B → 9.7B documents. SmolLM3: 11.2T tokens, 384 H100s for 24
  days, stage mixtures, 4K → 32K → 64K with RoPE θ 1.5M and 5M. Qwen3: S1 30T at 4K, S2 ~5T, S3 at 32K with ABF 10⁴ →
  10⁶, 119 languages. GLM-4.5: 23T, QK-Norm, MTP, Muon. Llama 4: FP8 on 32K GPUs, 390 TFLOP/s per GPU, 30T tokens.
* PaLM: 6,144 TPU v4, MFU 45.7% without and 46.2% with attention (238.3k tokens/s), ~20 spikes, restart ~100 steps
  back and skip 200–500 batches, z-loss 10⁻⁴ log² Z. MegaScale: 55.2% MFU, 175B, 12,288 GPUs.
* ZeRO: K = 12, 2Ψ + 2Ψ + KΨ = 16Ψ, Figure 1's 120 / 31.4 / 16.6 / 1.9 GB, 1.5× communication for stage 3.
* Megatron-LM: 8.3B on 512 GPUs, 15.1 PFLOP/s, 76% scaling; two all-reduces forward and two backward per layer.
  GPipe: bubble O((K − 1)/(M + K − 1)), negligible for M ≥ 4K. Zero Bubble: up to 23% (31% with relaxed memory) over
  1F1B. Ring all-reduce lower bound: Patarasuk & Yuan (2009), as restated by later work (some process sends and some
  receives at least 2(N − 1)M/N); the proof on screen is our own counting argument.
* Common Crawl: founded 2007 by Gil Elbaz, crawling since 2008, over 10 PB (its own pages). GPT-1: "1 month on 8
  GPUs" (OpenAI's 2018 post). Lee et al. (2022): "emit memorized text ten times less frequently".
* Gloeckle et al.: 13B, +12% HumanEval, +17% MBPP, up to 3× faster with 4-token prediction; at the smallest sizes
  multi-token prediction scored below next-token prediction (their Figure 3).
* Our measurements: the precision runs emulate each format by rounding the inputs of every matrix product inside the
  blocks (forward and backward) and summing in FP32; the embedding, output head and attention's own products stay in
  FP32 (as in DeepSeek-V3). The tile in our FP8 run is 32 (our model is 64 wide); DeepSeek's is 128. The FP16
  accumulation experiment divides each step's loss by 64 before the backward pass and multiplies the gradients back
  after it, which is what accumulating over 64 micro-batches does to the gradients' size. The collectives were timed
  on a shared machine. The restart time in the failure simulation (10 minutes) is illustrative. Every model trained
  here has its training on screen: the quality classifier's F1 after 1 to 25 passes over its labels (the cut re-chosen
  each time), the 32 RegMix proxies and the six mixture tests as held-out curves, the 24 stability runs, the precision,
  accumulation and MTP runs, both recipes (two seeds each) and the data-parallel check's six steps. The MTP module's
  cost is counted in FLOPs per token (`mtp_cost`): in a model with a 4,096-token vocabulary and width 64, the second
  pass through the output head is most of it, which is why it is far larger than in DeepSeek-V3.
* Not used: training-token counts for Kimi K3; Kimi K2's GPU count; OLMo 3's optimizer; a DualPipe simulation (its
  formula is cited instead).

References: Broder (1997); Indyk & Motwani (1998); Lee et al. (2022); Penedo et al., FineWeb (2024); Li et al., DCLM
(2024); Joulin et al. (2016–17); Xie et al., DoReMi (2023); Liu et al., RegMix (2025); Maini et al., WRAP (2024);
Shumailov et al. (Nature, 2024); Gerstgrasser et al. (2024); Muennighoff et al. (2023); Devlin et al. (2019); Raffel et
al. (2020); Bavarian et al. (2022); Hu et al., MiniCPM (2024); Hägele et al. (2024); Xiong et al. (2023); Rajbhandari et
al., ZeRO (2020); Zhao et al., FSDP (2023); Shoeybi et al., Megatron-LM (2019); Narayanan et al. (2019, 2021);
Korthikanti et al. (2022); Huang et al., GPipe (2019); Qi et al., Zero Bubble (2024); Patarasuk & Yuan (2009); Liu,
Zaharia & Abbeel, Ring Attention (2023); Milakov & Gimelshein (2018); Chowdhery et al., PaLM (2022); Jiang et al.,
MegaScale (2024); Micikevicius et al. (2018, 2022); Mishra et al., MXFP8 (2025); NVIDIA, NVFP4 (2025), Nemotron 3
Super (2026); Dehghani et al. (2023); Wortsman et al. (2024); Liu et al., Moonlight (2025); Kimi Team, K2 (2025);
Gloeckle et al. (2024); Young (1974); Llama Team (2024); DeepSeek-AI, V3 (2024), V4 (2026); Qwen Team, Qwen3 (2025);
Team OLMo, OLMo 2 (2025), Olmo 3 (2025); Hugging Face, SmolLM3 (2025), The Ultra-Scale Playbook (2025), The Smol
Training Playbook (2025); GLM-4.5 Team (2025); Meta, Llama 4 (2025); Moonshot AI, Kimi K3 model card (2026). Books:
J. Leskovec, A. Rajaraman & J. D. Ullman, *Mining of Massive Datasets*, ch. 3.

## Problems, with solutions

**1. MinHash and banding.** Show that for a random permutation, Pr[min over A = min over B] = J(A, B). With b = 20
bands of r = 5, at what similarity is a pair caught half the time? How often at s = 0.8?

*Solution.* Under a random permutation every element of A ∪ B is equally likely to come first. The two minima agree
exactly when that first element lies in A ∩ B, so the probability is |A ∩ B| / |A ∪ B| = J. A band of r minhashes
agrees with probability s^r, and a pair is caught if any of the b bands agrees: 1 − (1 − s^r)^b. Setting this to ½:
s = (1 − 2^(−1/b))^(1/r) = (1 − 2^(−1/20))^(1/5) ≈ 0.509. At s = 0.8: 1 − (1 − 0.8⁵)²⁰ = 1 − 0.672²⁰ ≈ 0.9996.

**2. The ring's bound.** An all-reduce of 10 GB of gradients over p = 64 GPUs with 50 GB/s each: find the ring's
bandwidth time, and show that no algorithm can beat it.

*Solution.* The ring sends 2(p − 1)/p · n per GPU: 2 · 63/64 · 10 GB / 50 GB/s ≈ 0.394 s (plus 2(p − 1) latencies).
Lower bound: follow one number. Some GPU is the first to hold its full sum; every other GPU's value must have reached
it, which takes at least p − 1 messages. At that moment no other GPU holds the sum, so each of the other p − 1 needs at
least one more message. So at least 2(p − 1) values are sent per number, 2(p − 1)n in all, and with p GPUs receiving
at most B each, the time is at least 2(p − 1)n/(pB), the ring's.

**3. ZeRO for a 70B model.** Mixed-precision Adam (K = 12) on 512 GPUs: bytes per GPU without ZeRO and with stages 1,
2 and 3. How much more does stage 3 communicate?

*Solution.* Without ZeRO: 16Ψ = 1,120 GB per GPU (impossible). Stage 1: 4Ψ + 12Ψ/512 ≈ 281.6 GB. Stage 2: 2Ψ + 14Ψ/512
≈ 141.9 GB. Stage 3: 16Ψ/512 ≈ 2.19 GB, plus the layer being gathered and the activations. Stages 1 and 2 move 2Ψ per
step, like an all-reduce; stage 3 gathers the parameters twice (forward and backward) and reduce-scatters the
gradients: 3Ψ, 1.5 times as much.

**4. Bubbles.** A pipeline of p = 16 stages and m = 64 micro-batches: the bubble for GPipe, for 1F1B, interleaved with
v = 4, and ZB-H1 when t_F = t_B = t_W.

*Solution.* GPipe and 1F1B: (p − 1)/(m + p − 1) = 15/79 ≈ 19.0% (1F1B only changes the memory). Interleaved:
(p − 1)/(vm + p − 1) = 15/271 ≈ 5.5%. ZB-H1: the bubble is (p − 1)(t_F + t_B − t_W) = 15 units against m(t_F + t_B +
t_W) = 192 busy units: 15/207 ≈ 7.2%.

**5. Loss scaling.** Gradients of size 2⁻³⁰ in FP16: which loss scale brings them to FP16's smallest normal number?
Why does BF16 need none?

*Solution.* FP16's smallest normal number is 2⁻¹⁴, so S = 2¹⁶ (any S ≥ 2⁶ already keeps them from flushing to zero, at
reduced precision, since the smallest subnormal is 2⁻²⁴). BF16 has FP32's eight exponent bits: its smallest normal
number is 2⁻¹²⁶, far below 2⁻³⁰.

**6. Young's interval.** Checkpoints cost δ = 60 s and failures come every M = 2 h: find Young's interval and the share
of time it wastes, to first order.

*Solution.* τ* = √(2δM) = √(2 · 60 · 7,200) ≈ 930 s ≈ 15.5 min. The waste δ/τ + τ/(2M) is then 2 · 60/930 ≈ 12.9% (at
the optimum the two terms are equal, so the waste is √(2δ/M)), before the time spent restarting.

## 习题与解答

**1. MinHash与分带。** 证明：对随机排列，Pr[A上的最小值 = B上的最小值] = J(A, B)。用 b = 20 个带、每带 r = 5 行时，相似度为
多少的一对文档有一半的概率被找出？s = 0.8 时概率是多少？

*解答。* 在随机排列下，A ∪ B 中每个元素排在最前的可能性相同。两个最小值相等，当且仅当这个最前的元素在 A ∩ B 里，所以概率是
|A ∩ B| / |A ∪ B| = J。一个带的 r 个最小哈希全部相等的概率是 s^r，只要 b 个带中有一个相等，这对文档就被找出：1 − (1 − s^r)^b。
令它等于二分之一：s = (1 − 2^(−1/20))^(1/5) ≈ 0.509。s = 0.8 时：1 − (1 − 0.8⁵)²⁰ = 1 − 0.672²⁰ ≈ 0.9996。

**2. 环形算法的下界。** 在 p = 64 块GPU上对10 GB梯度做全规约，每块GPU带宽50 GB/s：求环形算法的带宽时间，并证明没有算法能更快。

*解答。* 环形算法每块GPU发送 2(p − 1)/p · n：2 · 63/64 · 10 GB / 50 GB/s ≈ 0.394秒（另加 2(p − 1) 次延迟）。下界：跟踪一个数。
总有一块GPU最先得到它的完整和；其他每块GPU的值都必须传到它那里，至少需要 p − 1 条消息。在那一刻，别的GPU都还没有这个和，所以
其余 p − 1 块GPU每块至少还要再收一条消息。于是每个数至少发送 2(p − 1) 个值，总共 2(p − 1)n；p 块GPU同时接收、每块至多 B，
时间至少是 2(p − 1)n/(pB)，正是环形算法的时间。

**3. 70B模型的ZeRO。** 混合精度Adam（K = 12），512块GPU：不用ZeRO、用第1、2、3阶段时，每块GPU各需多少字节？第3阶段多传多少？

*解答。* 不用ZeRO：16Ψ = 1,120 GB 每块GPU（不可能）。第1阶段：4Ψ + 12Ψ/512 ≈ 281.6 GB。第2阶段：2Ψ + 14Ψ/512 ≈ 141.9 GB。
第3阶段：16Ψ/512 ≈ 2.19 GB，再加上正在收集的那一层和激活值。第1、2阶段每步传 2Ψ，与全规约相同；第3阶段前向和反向各收集一次
参数，再对梯度做规约-分散：3Ψ，是1.5倍。

**4. 气泡。** p = 16 级流水线、m = 64 个微批次：GPipe、1F1B、v = 4 的交错调度，以及 t_F = t_B = t_W 时ZB-H1的气泡各是多少？

*解答。* GPipe和1F1B：(p − 1)/(m + p − 1) = 15/79 ≈ 19.0%（1F1B只改变内存）。交错调度：(p − 1)/(vm + p − 1) = 15/271 ≈
5.5%。ZB-H1：气泡是 (p − 1)(t_F + t_B − t_W) = 15 个单位，忙碌时间是 m(t_F + t_B + t_W) = 192 个单位：15/207 ≈ 7.2%。

**5. 损失缩放。** FP16中大小为 2⁻³⁰ 的梯度：多大的损失缩放能把它们提到FP16最小的正规数？为什么BF16不需要？

*解答。* FP16最小的正规数是 2⁻¹⁴，所以 S = 2¹⁶（因为最小的次正规数是 2⁻²⁴，S ≥ 2⁶ 就足以让它们不被冲成零，只是精度较低）。
BF16有FP32的8个指数位：最小的正规数是 2⁻¹²⁶，远小于 2⁻³⁰。

**6. Young的间隔。** 保存一次检查点要 δ = 60秒，故障平均每 M = 2小时一次：求Young的间隔，以及一阶近似下浪费的时间比例。

*解答。* τ* = √(2δM) = √(2 · 60 · 7,200) ≈ 930秒 ≈ 15.5分钟。此时浪费 δ/τ + τ/(2M) = 2 · 60/930 ≈ 12.9%（最优点上两项相等，
所以浪费是 √(2δ/M)），还不算重启所花的时间。

## Glossary (new terms of this part)

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
| epoch, repetition | 轮次，重复 |
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
| fine-grained (tile-wise, block-wise) scaling | 细粒度（按块、按瓦片）缩放 |
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
