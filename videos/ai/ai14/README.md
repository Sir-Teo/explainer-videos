# AI, Built — Part 14: The Language-Model Lineage

Part 14 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How today's large language models came to be: the 2017 Transformer and the three
ways it was cut; pretraining and fine-tuning (ULMFiT, ELMo, GPT-1, BERT, T5) and the benchmark era; GPT-2, scaling
laws, GPT-3 and learning in context; code and instructions (Codex, FLAN, T0, InstructGPT); ChatGPT and the closed era;
open weights from LLaMA to the frontier of 2026, the recipe they converged on and how it began to split again; the
trends in compute, cost and data. Every published number is cited (`facts.py`); everything derived from it (parameter
counts, 6ND, cache sizes, growth rates) is computed (`compute.py`). And the lineage is rebuilt in miniature on the
series' thirty novels: a GPT-style and a BERT-style model trained at equal compute and compared on tasks both can do,
and a family of GPT-style models of growing size, searched for learning in context.

* **From a translation paper to the open frontier.** June 2017's *Attention Is All You Need* (213M parameters, 3.5 days
  on 8 GPUs); every model of the part by date and size, log scale; ChatGPT (30 November 2022); Kimi K3 (2.8T, 2026);
  our own GPT and BERT, and the family; the objectives.
* **1. Attention is all you need.** Recurrence is sequential (the seq2seq models of Part 10); self-attention connects
  every pair of positions in one step; the encoder–decoder (self-attention, masked self-attention, cross-attention,
  residuals, LayerNorm, sinusoidal positions); base and big configurations, WMT 2014 data; BLEU 27.3 / 28.4 EN-DE,
  41.8 EN-FR against GNMT, ConvS2S and MoE; training cost the paper's way, time × GPUs × 9.5 TFLOP/s = 2.3 × 10¹⁹
  (computed); why it won; the three cuts (encoder, decoder, both). Vaswani et al. (2017), Tables 2–3.
* **2. Pretrain, then fine-tune.** Labels are scarce (GLUE task sizes from 2.5k to 392k), text is free; ULMFiT (Howard
  & Ruder 2018: 18–24% less error; 100 labels ≈ 10,000 from scratch); ELMo (Peters et al. 2018); GPT-1 (Radford et al.
  2018: 12 layers, 768 wide, 117M, BooksCorpus, input transformations, 9 of 12 tasks); the objectives L₁, L₂ and
  L₃ = L₂ + 0.5·L₁; left-to-right representations as a handicap.
* **3. Masked language models and the benchmark era.** BERT (Devlin et al. 2018): masking 15% (80/10/10), next-sentence
  prediction; L_LM against L_MLM and the 1/0.15 ≈ 6.7 times fewer targets; Base 110M and Large 340M, 3.3B words, GLUE
  80.5 against GPT's 72.8; Table 5: the same BERT-Base pretrained masked or left to right (MNLI 83.9/82.1 … SQuAD
  87.9/77.8); GLUE passed by July 2019 (88.4 against 87.1), SuperGLUE (BERT 69.0, people 89.8, T5 88.9), RoBERTa,
  ELECTRA; encoders today in retrieval.
* **4. Everything is text to text.** T5 (Raffel et al. 2019): task prefixes (Figure 1's examples), C4 (~750 GB), span
  corruption (15%, spans of ~3, sentinels; Figure 2's example), Table 2's comparison at equal cost (encoder–decoder
  denoising 83.28 GLUE … decoder-only LM 73.78); T5-11B 88.9 on SuperGLUE; Wang et al. (2022): causal decoders best for
  zero-shot use after pretraining alone, bidirectional masked models best after multitask fine-tuning.
* **5. Unsupervised multitask learners.** GPT-2 (Radford et al. 2019): WebText (45M Reddit links with ≥ 3 karma, 8M
  documents, 40 GB), four sizes to 1.5B; tasks as patterns ("TL;DR:", "english = french", "A:"); CoQA 55 F1 without
  127k training answers; LAMBADA zero-shot 46 → 63% against a 59.23 record; enwik8 0.93 bits per byte; translation 5
  and 11.5 BLEU; the staged release (Feb, May, Aug, Nov 2019) and the model card.
* **6. Scale, and learning in context.** Kaplan et al. (2020): L(N) = (N_c/N)^0.076 drawn from its fit; GPT-3 (Brown et
  al. 2020): 8 sizes, 96 layers × 12,288, 300B tokens, the data mix; N ≈ 12Ld² + (V + n_ctx)d = 174.6B (computed,
  against Table D.1's 174,600M); C ≈ 6ND = 3.14 × 10²³ = 3,637 petaflop/s-days (computed); in-context learning,
  zero/one/few-shot (Figure 2.1's prompt); LAMBADA 76.2/72.5/86.4 against 68.0, TriviaQA 64.3/68.0/71.2.
* **7. Code, and following instructions.** Codex and HumanEval (Chen et al. 2021: 164 problems; GPT-3 0%, GPT-J 11.4%,
  Codex-12B 28.8%, 70.2% from 100 samples); FLAN (Wei et al. 2021: 137B, 60+ datasets as instructions, held-out task
  clusters, 20 of 25 against zero-shot GPT-3); T0 (Sanh et al. 2021: 11B, 9 of 11, 16× smaller); InstructGPT's three
  stages (Ouyang et al. 2022; Part 27).
* **8. ChatGPT and the closed era.** 30 November 2022; 100M monthly users in two months (a UBS estimate reported by
  Reuters); GPT-4 (OpenAI 2023): images, bar exam top 10% against GPT-3.5's bottom 10%, MMLU 86.4% against 70.0%,
  predictable scaling from runs with ≤ 1/10,000 of the compute, the "no further details" passage quoted, the system
  card; Epoch's outside estimates (2.1 × 10²⁵ operations, $40M); Claude, Gemini, o1.
* **9. Open weights.** LLaMA (Touvron et al. 2023: 7–65B, 1.0–1.4T tokens, public data; 13B beats GPT-3); tokens per
  parameter (GPT-3 1.7, Chinchilla's ~20, LLaMA-7B ~149, computed) and over-training for inference; Llama 2, Mistral
  7B, Mixtral (47B, 13B active), Llama 3.1 405B (3.8 × 10²⁵, 16,384 GPUs, 466 interruptions in 54 days); Qwen,
  DeepSeek-V2 (236B/21B, MLA, KV cache −93.3%).
* **10. The architecture converges.** One configuration card morphing from the Transformer to Kimi K3 with growth since
  GPT-1 (layers, width, context); the recipe matrix of 11 models (norm, activation, positions, attention, biases);
  pre-norm's identity path, derived (Xiong et al. 2020) and RMSNorm (Zhang & Sennrich 2019); SwiGLU (Shazeer 2020) and
  its width 8d/3 → LLaMA-65B's 22,016 (computed), with Shazeer's "divine benevolence"; the KV cache per token (GPT-3
  4.7 MB, Llama 3.1 MHA-equivalent 8.26 MB, GQA 0.52 MB, DeepSeek-V3 MLA 70 kB; 1.08 TB → 68 GB at 128K, computed).
* **11. The open frontier, 2024 to 2026.** DeepSeek-V3 (671B/37B, MLA, aux-loss-free balancing, MTP, FP8; 2.788M H800
  hours = $5.576M, computed) and R1 (AIME 2024 15.6 → 77.9%); Qwen3, Kimi K2, GLM-4.5, gpt-oss; total against active
  parameters, the active share (computed); hybrids (Jamba, MiniMax-01, Nemotron-H, Qwen3-Next, Kimi Linear) and the
  2026 flagships (Qwen3.5, GLM-5, DeepSeek-V4, Kimi K3), each checked against its model card; open against closed on
  Artificial Analysis's index: the running best of each and the months between (computed from its timeline).
* **12. Compute, cost and data.** The compute tower (paper figures and Epoch estimates, marked); a least-squares fit to
  Epoch AI's frontier language models, 2017–mid-2026 (computed), against Epoch's 4–5× a year; the cost of frontier runs
  (Cottier et al. 2024: 2.4× a year, GPT-4 $40M, Gemini Ultra $30M) and DeepSeek-V3's $5.6M; tokens per parameter over
  time (computed from published N and D).
* **13. Our own lineage: GPT against BERT.** Two models of the same shape, initial weights, data, steps and schedule:
  equal compute, 6ND; training replays (the GPT-style model's sample and the BERT-style model's fill-ins, scrubbed with
  their curves); a cloze test with 8 candidates (GPT scoring whole sentences, GPT left-only, BERT); a linear probe for
  "which of the thirty books?"; writing; the scoreboard row.
* **14. Learning in context, in our own models.** Four GPT-style sizes on the same tokens, and the series' base model:
  loss at each position of the context; a training replay of how the curve forms; a repeated-list (induction) test; GPT-3
  style few-shot "which book?" prompts with 0–8 examples; what our scale shows and doesn't.
* **Recap.** The family tree, 2017–2026: time left to right, one lane per branch or lab (encoders, encoder–decoders,
  OpenAI, Meta, Mistral AI, DeepSeek, Moonshot, Alibaba), open weights filled and closed models hollow, a line to
  the lab's previous model or the published design a model built on (schematic); eight pictures of the part; where
  it comes back; the problem set; Part 15's teaser; references.

Run from the repo root:

```
python -m explainer.ai.novels              # the series' tokenizer and base model (shared; cached in .cache/novels)
python -m videos.ai.ai14.compute           # everything (training: about 3 CPU-hours on 2 threads; resumable)
python tools/build.py ai14                 # English
python tools/build.py ai14 --lang zh       # Chinese
```

`facts.py` holds every published number with its source; `compute.py` derives the rest and trains and evaluates our
models (`lm.py`: the causal and masked models, training with checkpoints and snapshots, the measurements);
`epoch_lm.json` is Epoch AI's *Notable AI Models* data, trimmed to language models with a training-compute estimate
(downloaded 19 October 2026, CC BY); `aa_progress.json` is Artificial Analysis's open-source progress timeline as
fetched for `videos/ml/open_models` on 8 October 2026.

## Computed results

From published figures (`published`, `epoch`, `aa`):

* The 2017 Transformer, the paper's way: big model 3.5 days × 8 GPUs × 9.5 TFLOP/s = 2.30 × 10¹⁹ operations (base:
  3.28 × 10¹⁸).
* Parameter counts from shape (12Ld² + (V + n_ctx)d): GPT-1 116.4M (published 117M), GPT-2 1.557B (1.5B), GPT-3 174.6B
  (Table D.1: 174,600M); LLaMA-65B 65.28B and Llama 3.1 405.8B with SwiGLU and GQA.
* GPT-3's compute: 6 × 174.6B × 300B = 3.14 × 10²³ = 3,637 petaflop/s-days.
* SwiGLU width: 8/3 × 8,192 = 21,845.3, rounded up to LLaMA-65B's 22,016.
* KV cache per token (16-bit): GPT-3 4.72 MB; Llama 3.1 405B as multi-head 8.26 MB, with GQA (8 of 128) 0.52 MB;
  DeepSeek-V3 MLA 70.3 kB. At 128K tokens: 1.08 TB against 68 GB.
* Tokens per parameter: GPT-3 1.7, Gopher 1.1, PaLM 1.4, Chinchilla 20, LLaMA-7B 149, LLaMA-65B 21.5, Llama 2 70B
  28.6, Llama 3.1 405B 38.5, DeepSeek-V3 400 and Kimi K2 476 (per active parameter), GLM-5 713, Qwen3-0.6B 60,000.
* DeepSeek-V3's final run: 2.788M H800 hours × $2 = $5.576M; 6ND = 3.3 × 10²⁴. Active share of parameters: DeepSeek-V3
  5.5%, Qwen3-235B 9.4%, Kimi K2 3.1%, GLM-4.5 9.0%, gpt-oss-120b 4.4%, Qwen3.5-397B 4.3%, DeepSeek-V4 3.1%, Kimi K3
  3.7%.
* Compute tower: 7.7 years, a factor of about 15 million (Transformer to Grok 3).
* Least-squares fit to Epoch AI's 40 frontier language models (2017 to mid-2026): slope 0.709 powers of ten a year,
  5.1× a year (90% interval 4.6–5.7), doubling every 5.1 months; the 31 since mid-2020: 5.1×; all 271 language models
  with a compute estimate: 7.0× a year (the database's mix shifts toward larger models over time).
* Artificial Analysis's index (v4.3.2, 8 October 2026): over 21 open-model records, the median time since a closed model
  first scored as high is 4.4 months; since 2025, 4.1 months; the latest record (MiMo-V2.6-Pro) trailed by 3.4 months.

Our models (trained and measured on this computer; filled in from `.cache/ai14/` after `compute.py` runs):

RESULTS_PENDING

## Fact-check notes

Checked against the primary sources on 19 October 2026 (arXiv papers and technical reports, the GPT-2 repository and
model card, Hugging Face model cards and API metadata):

* Transformer: Table 2 gives EN-FR 41.8 for the big model; the text of v7 says 41.0 (the abstract says 41.8). The FLOP
  estimate is the paper's own method (time × GPUs × 9.5 TFLOPS for a P100, Table 2 footnote).
* GPT-1's 117M is the GPT-2 paper's count for its smallest model "equivalent to the original GPT"; the GPT-2 repository
  later corrected its counts (124M, 355M, 774M, 1.5B); our 12Ld² check gives 1.557B for the largest.
* BERT's Table 5 rows used in chapter 3 are "No NSP" (masked) against "LTR & No NSP" (left to right), so that only the
  objective differs.
* Dates of 2026 releases: Qwen3.5 (Hugging Face, 16 February 2026), GLM-5 (11 February; arXiv 2602.15763), DeepSeek-V4
  (model card, a preview, April 2026), Kimi K3 (announced 16 July 2026, weights later in July), MiMo-V2.6-Pro (21
  September 2026). Parameters and architectures are from the model cards; DeepSeek-V4's "more than 32T" tokens is a
  lower bound.
* Outside estimates (Epoch AI) are labelled as such: GPT-1, GPT-2, PaLM, GPT-4, Grok 3 in the compute tower; GPT-4's
  and Gemini Ultra's costs. Closed models' sizes and data are not stated anywhere on screen.
* "100 million monthly users in two months" is a UBS estimate reported by Reuters (2 February 2023), not an OpenAI figure.
* Not used: claims about Kimi K3's training tokens and DeepSeek-V4's layer layout (not in the model cards); later
  closed-model compute estimates in Epoch's database (after mid-2026).

References: Vaswani et al. (2017); Howard & Ruder (2018); Peters et al. (2018); Radford et al. (2018, 2019); Devlin et
al. (2018); Wang et al., GLUE (2018), SuperGLUE (2019); Liu et al., RoBERTa (2019); Clark et al., ELECTRA (2020); Raffel
et al., T5 (2019); Lewis et al., BART (2019); Wang et al. (2022); Kaplan et al. (2020); Brown et al. (2020); Hoffmann et
al. (2022); Chen et al. (2021); Wei et al. (2021); Sanh et al. (2021); Ouyang et al. (2022); OpenAI, GPT-4 Technical
Report and System Card (2023); Touvron et al., LLaMA and Llama 2 (2023); Jiang et al., Mistral 7B (2023), Mixtral (2024);
Llama Team (2024); Chowdhery et al., PaLM (2022); Shazeer (2019, 2020); Zhang & Sennrich (2019); Xiong et al. (2020); Su
et al. (2021); Ainslie et al. (2023); DeepSeek-AI, V2 (2024), V3 (2024), R1 (2025), V3.2 (2025); Qwen Team, Qwen2.5
(2024), Qwen3 (2025); Kimi Team, K2 (2025), Kimi Linear (2025); GLM-4.5 Team (2025); OpenAI, gpt-oss (2025); Lieber et al.,
Jamba (2024); MiniMax (2025); NVIDIA, Nemotron-H (2025); model cards of Qwen3-Next, Qwen3.5, GLM-5, DeepSeek-V4, Kimi K3,
MiMo-V2.6-Pro (2025–26); Sevilla & Roldán (Epoch AI, 2024); Cottier et al. (2024). Books: D. Jurafsky & J. H. Martin,
*Speech and Language Processing* (3rd ed. draft); S. Raschka, *Build a Large Language Model (From Scratch)* (2024);
S. J. D. Prince, *Understanding Deep Learning* (2023).

## Problems, with solutions

**1. Counting GPT-3.** Show that a decoder layer with a feed-forward width of 4d has 12d² weights (ignoring norms and
biases). With L = 96, d = 12,288, a vocabulary of 50,257 and 2,048 positions, check GPT-3's 174.6 billion.

*Solution.* Attention has four d × d matrices (queries, keys, values, output): 4d². The feed-forward network has a
d × 4d and a 4d × d matrix: 8d². So a layer has 12d², and L layers 12Ld² = 12 · 96 · 12,288² = 173,946,175,488. The
token and position embeddings add (50,257 + 2,048) · 12,288 = 642,723,840 (the output layer reuses the token
embedding). Total: 174,588,899,328 ≈ 174.6 billion, the 174,600M of the paper's Table D.1.

**2. Six operations per parameter per token.** Argue that training costs about 6 operations per parameter per token,
two forward and four backward. Compute GPT-3's C ≈ 6ND with D = 300 billion, in operations and in petaflop/s-days.

*Solution.* In the forward pass each weight w takes part in one multiply-add, y += w·x: 2 operations. In the backward
pass the same weight takes part in two: the gradient for the layer below, dx += w·dy, and the gradient for the weight,
dw += x·dy: 4 operations. So 6 per parameter per token (attention's own products and the nonlinearities are small for
large d). C ≈ 6 · 174.6 × 10⁹ · 300 × 10⁹ = 3.14 × 10²³ operations; one petaflop/s-day is 10¹⁵ · 86,400 =
8.64 × 10¹⁹, so C ≈ 3,637 petaflop/s-days: the paper's 3.64 × 10³.

**3. SwiGLU's width.** A SwiGLU feed-forward network has three d × h matrices. For which h does it match a ReLU network
of width 4d? Find h for d = 4096, rounded up to a multiple of 256.

*Solution.* 3dh = 2 · d · 4d = 8d² gives h = 8d/3. For d = 4096, h = 10,922.7, rounded up to 43 · 256 = 11,008: the
width of LLaMA-7B's feed-forward layers (and 22,016 for LLaMA-65B's d = 8192).

**4. The KV cache.** Show that the KV cache costs 4 L n_kv d_head bytes per token in 16-bit numbers. For Llama 3.1 405B
(L = 126, d_head = 128), compare 8 and 128 key-value heads at 131,072 tokens.

*Solution.* Each layer keeps a key and a value for each key-value head, each d_head numbers of 2 bytes: 2 · 2 · n_kv ·
d_head bytes, times L layers. With n_kv = 8: 4 · 126 · 8 · 128 = 516,096 bytes per token, 67.6 GB for 131,072 tokens.
With 128 heads, 16 times as much: 8.26 MB per token, 1.08 TB per sequence. Grouped-query attention lets 16 query heads
share each key-value head, which is why the cache fits.

**5. What equal compute holds fixed.** A masked model predicts a fraction m of the positions. How many targets per
sequence of n does it get, against a causal model? What does an equal-compute comparison hold fixed, and what not?

*Solution.* In expectation mn targets (0.15n for BERT) against n for a causal model: 1/m ≈ 6.7 times fewer. Equal
compute (same model, same tokens, same steps) fixes the operations, the data and the number of updates; it does not fix
the number of prediction targets, nor how hard each is (a masked target sees both sides). Giving the masked model as
many targets would cost 1/m times the compute. ELECTRA's answer was to make every position a target.

**6. Growth rates.** If training compute grows 4.5× a year and cost 2.4×, find the doubling time of compute in months,
its growth over a decade, and the yearly gain in operations per dollar.

*Solution.* Doubling time: 12 · ln 2 / ln 4.5 = 5.5 months. Over a decade: 4.5¹⁰ ≈ 3.4 million times. Operations per
dollar: 4.5 / 2.4 ≈ 1.9 times a year, from cheaper hardware and from using it more efficiently.

## 习题与解答

**1. 数一数GPT-3。** 证明：前馈层宽度为4d的解码器层有12d²个权重（不计归一化和偏置）。用 L = 96、d = 12,288、词表50,257、
2,048个位置，验证GPT-3的1746亿个参数。

*解答。* 注意力有四个 d × d 矩阵（查询、键、值、输出）：4d²。前馈网络有一个 d × 4d 和一个 4d × d 矩阵：8d²。所以每层
12d²，L层共 12Ld² = 12 · 96 · 12,288² = 173,946,175,488。词元嵌入和位置嵌入再加上 (50,257 + 2,048) · 12,288 =
642,723,840（输出层复用词元嵌入）。合计 174,588,899,328，约1746亿，正是论文表D.1里的174,600M。

**2. 每个参数、每个词元6次运算。** 说明训练时每个参数每个词元大约要6次运算：前向2次，反向4次。用 D = 3000亿，计算GPT-3的
C ≈ 6ND，分别用运算次数和petaflop/s-天表示。

*解答。* 前向时每个权重w参与一次乘加 y += w·x：2次运算。反向时同一个权重参与两次：给下一层的梯度 dx += w·dy，和给权重本身的
梯度 dw += x·dy：4次运算。所以每个参数每个词元6次（d很大时，注意力自身的乘积和非线性都很小）。C ≈ 6 · 1746亿 · 3000亿 =
3.14 × 10²³ 次运算；1 petaflop/s-天 = 10¹⁵ · 86,400 = 8.64 × 10¹⁹，所以 C ≈ 3,637 petaflop/s-天，与论文的 3.64 × 10³ 一致。

**3. SwiGLU的宽度。** SwiGLU前馈网络有三个 d × h 矩阵。h取多少时，它和宽度为4d的ReLU网络参数一样多？求 d = 4096 时的h，
向上取到256的倍数。

*解答。* 3dh = 2 · d · 4d = 8d²，得 h = 8d/3。d = 4096 时 h = 10,922.7，向上取整到 43 · 256 = 11,008：正是LLaMA-7B前馈层的宽度
（LLaMA-65B的 d = 8192 对应22,016）。

**4. KV缓存。** 证明用16位数存储时，KV缓存每个词元占 4 L n_kv d_head 字节。对Llama 3.1 405B（L = 126，d_head = 128），比较
8个和128个键值头在131,072个词元时的缓存。

*解答。* 每一层为每个键值头存一个键和一个值，各有d_head个2字节的数：2 · 2 · n_kv · d_head 字节，再乘以L层。n_kv = 8 时：
4 · 126 · 8 · 128 = 516,096 字节/词元，131,072个词元共67.6 GB。128个头时是16倍：每个词元8.26 MB，每个序列1.08 TB。分组查询
注意力让16个查询头共用一个键值头，缓存才放得下。

**5. 同等算力固定了什么。** 掩码模型只预测比例为m的位置。长度为n的序列里，它得到多少个预测目标，因果模型又得到多少？同等算力
的比较固定了什么，没有固定什么？

*解答。* 期望为mn个目标（BERT是0.15n），因果模型是n个：少了 1/m ≈ 6.7 倍。同等算力（同样的模型、同样的词元、同样的步数）
固定了运算量、数据和更新次数；没有固定预测目标的数量，也没有固定每个目标的难度（被遮住的目标能看到两边）。要让掩码模型得到
同样多的目标，算力要乘以1/m。ELECTRA的办法是让每个位置都成为目标。

**6. 增长率。** 如果训练算力每年增长4.5倍、成本每年增长2.4倍，求算力翻倍所需的月数、十年的增长倍数，以及每美元运算次数
每年提高多少。

*解答。* 翻倍时间：12 · ln 2 / ln 4.5 = 5.5个月。十年：4.5¹⁰ ≈ 340万倍。每美元的运算次数：4.5 / 2.4 ≈ 每年1.9倍，来自更便宜的
硬件和更高的使用效率。

## Glossary (new terms of this part)

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
