# AI, Built — Part 30: Inside the Model

Part 30 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How to read what a trained network has learned, and how to tell reading from
causing: saliency maps and their sanity checks, probes with control tasks, the logit and tuned lenses, activation and
path patching, an induction circuit taken apart end to end, superposition and its phase diagram, sparse dictionaries
(L1, TopK, JumpReLU, Matryoshka) with their failures (shrinkage, dead latents, splitting, absorption), transcoders and
attribution graphs, crosscoders and model diffing, steering, grokking explained mechanistically, the faithfulness of
chains of thought, and the 2025–26 frontier with the arguments inside the field. Every experiment runs on the series'
own models on this computer: Part 13's character transformer (through `videos/ai/ai13/compute.py`'s `load_tf`), the
novels model (`explainer/ai/novels.py`) and Part 27's chat fine-tune of it (`videos/ai/ai27/compute.py`), plus three
small models trained here (Part 13's two-layer attention-only model, retrained with its recipe and seed; Toy Models'
2-feature model on a grid; Nanda et al.'s grokking transformer). Every number on screen is computed or cited.

## Chapters

* **What is it thinking?** The 128 numbers Part 13's transformer carries per character after block 2, all busy; the
  same rewritten by a sparse autoencoder, a handful on; a feature as a direction (a shadow on it). Objectives.
* **1. How we got here.** Saliency maps (Simonyan, Vedaldi & Zisserman 2013) and occlusion (Zeiler & Fergus 2014),
  computed on our transformer for one prediction and 24 more, compared by rank correlation; Adebayo et al.'s sanity
  check (2018), cascading re-randomization run on ours; DeepDream (2015), Network Dissection (Bau et al. 2017),
  feature visualization (Olah, Mordvintsev & Schubert, Distill 2017), Building Blocks (2018); the Circuits thread's
  three claims (Zoom In, 2020), multimodal neurons (Goh et al. 2021), the transformer-circuits framework (Elhage et al.
  2021), induction heads (Olsson et al. 2022), IOI (26 heads in 7 classes, Wang et al. 2022), Toy Models (2022),
  Towards Monosemanticity (512 neurons into 4,096 features, 2023), Scaling Monosemanticity (Claude 3 Sonnet, 2024),
  attribution graphs (2025).
* **2. What does it know?** Linear probes on every layer of the novels model for "inside a quotation" (Alain & Bengio
  2016), three seeds; Hewitt & Liang's control task (2019): the same labels assigned at random per token type, linear
  and MLP probes, selectivity = task − control; amnesic probing (Elazar et al. 2021): the probe's direction projected
  out at the best layer, the cost on closing quotation marks, against ten random directions.
* **3. Reading the stream as it flows.** The logit lens (nostalgebraist 2020) on the novels model, a prompt read at
  every layer; the tuned lens (Belrose et al. 2023), one affine translator per layer trained here (its training
  replayed); KL to the final prediction and bits per token by layer, held out.
* **4. Cause, not correlation.** Do our models copy? Repeated held-out text through both: passage-level loss
  changes alone do not identify a copying circuit.
  Part 13's two-layer attention-only model on repeated random tokens, retrained (its loss and its two heads'
  attention); activation patching (Vig et al. 2020; Meng et al. 2022): the corrupted residual stream put into a
  clean run at every tested (layer, position) for one target; each head's corrupted output put into a clean run.
* **5. An induction circuit, end to end.** Path patching (Wang et al. 2022; Goldowsky-Dill et al. 2023): the
  previous-token head's corrupted output sent only into the induction head's queries, keys or values; K-composition
  from the weights (Elhage et al. 2021) against random heads; the previous-token head's QK circuit on positions; the
  induction head's OV circuit token to logit (diagonal share, eigenvalue copying score); mean-ablation of every head;
  the K path's effect through training, replayed with the loss.
* **6. More ideas than dimensions.** Toy Models' 5 features in 2 dimensions at four sparsities, the pentagon forming
  during training, interference through the bias and ReLU.
* **7. The phase diagram.** The 2-feature, 1-dimension model trained on a 17 × 17 grid of densities and relative
  importances, four seeds per cell; the empirical phases (feature 2 dropped, given the dimension, or in superposition)
  against three restricted reference candidates' expected losses; one cell's training; random directions' cosines in 2 to
  1,024 dimensions (spread ≈ 1/√d; Johnson & Lindenstrauss 1984).
* **8. Pulling the features apart.** An L1 sparse autoencoder with 512 features on 211,200 residual vectors (Bricken
  et al. 2023; Cunningham et al. 2023), its training replayed; features per character, variance explained, bits per
  character with the rebuild spliced in; where four features fire; neurons against features.
* **9. Better dictionaries.** L1 shrinkage derived (soft thresholding); TopK (Gao et al. 2024, 16M latents on GPT-4)
  and JumpReLU (Rajamanoharan et al. 2024; Gemma Scope) trained beside L1 at equal size, steps and batches, several
  sparsities, three seeds: sparsity against variance explained and against bits per character spliced in; dead
  latents and AuxK.
* **10. Splitting and absorption.** TopK dictionaries of 128, 512 and 2,048 latents: one latent's descendants
  (feature splitting, Bricken et al. 2023); absorption (Chanin et al. 2024) measured for "upper-case letter" with a
  probe direction and the dictionary's best latent; Matryoshka dictionaries (Bussmann et al. 2025; Nabeshima 2024)
  against TopK, three seeds each.
* **11. Transcoders and attribution graphs.** Per-layer transcoders (Dunefsky, Chlenski & Nanda 2024) and a
  cross-layer transcoder (Ameisen et al. 2025) for all four MLPs of Part 13's transformer, their training replayed;
  the replacement model's bits per character; an attribution graph for '…she sai' → 'd' from the local replacement
  model (attention patterns and layer-norm scales frozen, error nodes; exact on the prompt), its logit balanced into
  features, embeddings and errors; its 16 most influential features switched off in the real model, measured against
  the graph's prediction; Claude 3.5 Haiku's biology (Lindsey et al. 2025): two-hop reasoning, planning in poems,
  addition, multilingual features, entity recognition and hallucination, "about a quarter of the prompts".
* **12. What fine-tuning changed.** A BatchTopK crosscoder (Lindsey et al. 2024; Minder et al. 2025) on the novels
  model and Part 27's chat fine-tune, after blocks 3 and 5, on novel text and chat transcripts: balanced, chat-dominant
  and base-dominant bins of normalized decoder-norm shares, and where selected latents fire. These bins are
  descriptive proxies, not proofs that concepts were created or removed; the local activation-difference readout
  (Minder et al., Oct 2025) on plain novel text.
* **13. Reaching in.** The L1 autoencoder's quotation feature added to Part 13's transformer while it writes, three
  strengths, five samples, against a random direction; a contrast vector in the novels model (cheerful minus gloomy
  words in the same frames, after block 3, the manner of CAA and persona vectors): as a monitor (AUROC on held-out
  words and on real sentences), as a steer (mood and fluency at five strengths, against a random direction, 36 samples
  each); ActAdd (Turner et al. 2023), refusal as one direction (Arditi et al. 2024), persona vectors (Chen et al.
  2025), Golden Gate Claude (May 2024).
* **14. Grokking, mechanistically.** Nanda et al.'s one-layer transformer (2023) on (a + b) mod 59 (they used 113),
  30% of the table, AdamW with weight decay 1: memorization and the late collapse of the test loss; the Fourier
  algorithm derived; the embedding's spectrum through training and the numbers on a circle; neurons by frequency; the
  progress measures (restricted and excluded loss, weight norm) and the three phases. Part 12 covers grokking as a
  phenomenon.
* **15. Does the chain of thought tell the truth?** Biased few-shot examples (Turpin et al. 2023); truncated and edited
  chains (Lanham et al. 2023); hints (Chen et al. 2025: Claude 3.7 Sonnet 25%, DeepSeek-R1 39%; reward hacks admitted
  under 2% in most settings); faithful, made-up and motivated reasoning seen in attribution graphs (Lindsey et al.
  2025). Cited, not computed: our models write no chains of thought.
* **16. The frontier, 2025 to 2026.** Open circuit tracing (Anthropic Fellows and Decode Research, May 2025),
  weight-sparse transformers (Gao et al., OpenAI, Nov 2025), Gemma Scope 2 (Dec 2025), attention tracing; emergent
  introspective awareness (Lindsey, Oct 2025); emotion concepts in Claude Sonnet 4.5 (Apr 2026); auditing for hidden
  objectives (Marks et al., Mar 2025), the Claude Sonnet 4.5 system card's evaluation-awareness steering (Sep 2025),
  natural-language autoencoders (May 2026).
* **17. Where the field disagrees.** Autoencoder probes against linear probes (GDM, Mar 2025; Kantamneni et al. 2025),
  measured on the novels model from 16 to 4,096 examples, on novel text and in chat transcripts; dictionaries from different seeds (Paulo &
  Belrose 2025), measured on ours; autoencoders on a random transformer (Heap et al. 2025), measured on ours; ambitious
  against pragmatic interpretability, dark matter, AxBench (Wu et al. 2025), parameter decomposition, open problems
  (Sharkey et al. 2025).
* **Recap** in ten pictures from the part's own results, where it comes back (Part 31), six problems, Part 31's
  teaser, references.

## Running it

```
python -m explainer.ai.novels               # the novels model (cached in .cache/novels/); Part 27's fine-tune is
                                            # computed by its own compute when this part first asks for it
python -m videos.ai.ai30.compute            # everything missing: about 2-3 CPU-hours on one or two threads
python -m videos.ai.ai30.compute --force sae
AI30_SCALE=0.05 python -m videos.ai.ai30.compute   # a smoke test of every code path, into .cache/ai30_quick/
python tools/make.py ai30                   # computations, then the narrated cut in English and Chinese
python tools/build.py ai30 -q l             # a 480p preview
```

Everything is seeded. The long items resume after an interruption: the sweeps (`frontier`, `splitting`,
`absorption`, `clt`) keep every finished run in `CACHE.partial`, the grokking run checkpoints every 1,000 steps with
its random state (`.cache/ai30/grok.ckpt`). Torch threads: `AI30_THREADS` (default 1; set at run time, never on
import). Dictionaries are kept small in `.cache/ai30/dicts/` and `.cache/ai30/*.pt`; activations are recomputed, not
stored. The part reads Part 13 through `videos.ai.ai13.compute` (`load("tf")`, `load_tf`, `head_mats`,
`composition_scores`, `composition_baseline`), the novels model through `explainer.ai.novels`, and Part 27 through
`videos.ai.ai27.compute` (`load("sft")`, `_load_model("sft")`, `load("data")`, its word lists).

Other parts read from this one: Part 19's outro calls `load("superposition")` (its keys are unchanged), and Part 16
imports `show` from `videos.ai.ai30.common`.

## QA scope: Part 27-dependent sections

The data-dependent Diffing methods, the mood-vector monitor/steering tradeoff, the sparse-probe comparison, and the complete
recap remain source-reviewed only in the fresh cloud QA workspace: required original Part 27 data/SFT inputs and
complete accepted derived payloads are unavailable. No missing metrics, outputs or render acceptance are inferred. Its card and crosscoder diagram need no scientific payload; the histogram, latent examples and difference readout still require it.
The historical numerical outcomes below are preserved; interpretive terminology is qualified where needed.

Crosscoders fit paired residual streams with separate per-model scalar normalization and output biases. The norm
share r measures decoder magnitude in those normalized coordinates, not direction agreement or proof of new
concepts. The three reported threshold bins are not exhaustive; intermediate live latents must remain counted.
Training FVU uses fitting activations and must retain finite values above one. Marker counts inspect the actual
firing token, not any marker occurring earlier in its context.

The saved difference readout is R(mean_base + Delta) - R(mean_base), where R(z) = head(norm(z)) uses the base
model's final normalization/output head. It is not a direct linear unembedding of Delta or the full models'
prediction difference. This local variant pools sampled novel positions; it does not replicate the paper's
per-position analysis on the first five tokens. The vector diagram is schematic; only its difference-to-typical-base length ratio is
measured. Absence of special tokens among the top readout tokens does not prove the change is only stylistic.

The mood-vector monitor uses held-out words and lexicon-selected sentences, not human sentiment annotations. Its
steering summaries are lexicon counts and unsteered-model bits/token; error bars are descriptive sample standard
errors across prompt/seed runs, not a formal significance test or human fluency judgment.

The sparse-probe producer resets quotation state to outside at each sampled window, newline and special token.
Skipping eight initial positions does not recover a window's unknown initial quotation state. Treat its target as
a window-local operational proxy; preserve this original recipe unless a separately labeled correction receives
an impact comparison. Plot all measured in-domain/out-of-domain accuracies without clipping and report domains
separately. A one-class training draw uses its observed constant class for every representation.

The full recap remains unrendered because its diffing dependency is missing.

### 第27部分依赖章节的QA范围

在新云端环境里，模型差分中依赖数据的方法、情绪向量与引导权衡、稀疏探针对比及完整回顾，只有源码审查；
所需的原始第27部分数据/SFT输入和完整已接受派生结果尚不可用。下方历史数值原样保留，不代表新的测量或渲染验收。
交叉编码器分别缩放两个模型的残差流，并包含输出偏置。归一化解码器范数份额是描述性代理，不证明方向一致、概念新生
或消失；三个阈值分组并不穷尽全部活跃潜变量。拟合FVU应保留大于1的实际值；标记计数检查真正的激活词元。
差分读出是R(基础均值+Delta)-R(基础均值)，R包含最终归一化与输出头；不是Delta的线性反嵌入，也不是完整预测之差。
向量方向是示意，只有相对长度被测量。情绪监控使用留出词与按词表筛选的句子，非人工情感标注；生成指标为词表计数
及未引导模型的每词元比特数，不是人工流畅度或显著性检验。稀疏探针的引号状态在每个窗口、换行和特殊词元处重置；
窗口开头的未知状态不会被跳过八个位置自动恢复。原配方保留，目标应标为窗口局部代理；两类评估域分别报告且不截断。
完整回顾仍受差分输入缺失所限。

## Historical reported results

The following values are the original author-reported outcomes. Their original Part 30 caches were not available
in the fresh cloud QA workspace. They remain unchanged for provenance and are not measurements from the new QA
candidates. Fresh candidates and corrected-recipe comparisons have separate input/source hashes and acceptance
records; the source/narration reads whichever explicitly staged cache it is given.

Seeded, one torch thread, on a busy 4-core Linux machine (about 1.5 CPU-hours in all; the frontier sweep is 40 of
those minutes). The narration states each result from the cached numbers, so another machine's run says what it
measured.

* **Saliency** (Part 13's transformer, '…she sai' → 'd', 99%): gradient × input against occlusion, rank correlation
  0.21 on the shown prediction and 0.07 on average over 24 more; cascading re-randomization: 1.00, 0.45, 0.39, 0.20,
  −0.31, −0.09 (the map passes Adebayo et al.'s check: trained against fully random, −0.05 on average).
* **Probes** (novels model, "inside a quotation", 8,960 tokens to train and 8,960 held out, 3 seeds; majority 61%):
  linear probe 66% at the embedding rising to 91% at layer 5; control task 81% at the embedding falling to 73%; MLP
  probe 91% on the task but 88% on the control at layer 5: selectivity +16 points (linear) against +3 (MLP). Amnesic
  probing at layer 5: closing quotation marks cost 4.03 bits, 5.59 with the probe's direction removed, 4.04 (mean)
  with ten random directions removed.
* **Lenses** (novels model, held-out text): KL to the final prediction, logit lens / tuned lens, by layer 0–5: 8.55 /
  2.53, 2.96 / 1.86, 2.40 / 1.45, 1.88 / 1.10, 1.40 / 0.74, 0.71 / 0.34 bits; bits per token at the embedding 13.6 /
  7.6, the model 5.27.
* **Induction.** Repeated held-out text: Part 13's transformer 1.79 → 1.80 bits per character, the novels model
  5.18 → 5.07 bits per token (no copying). The attention-only model (retrained, seed 2022): the repeat falls from 6.23
  to 1.49 bits per token, fastest around step 2,600; previous-token heads 1 and 2 of layer 1 (scores 0.37, 0.30), a
  current-token head 4 (self-attention 0.62), induction heads 1–3 of layer 2 (0.60, 0.60, 0.52). Noising each head:
  0.39, 0.29, 0.13, 0.65 (layer 1), 0.45, 0.46, 0.29, −0.05 (layer 2). Path patching from the previous-token heads into
  layer 2: queries 0.00, keys 0.86, values 0.01; each previous-token head alone, keys: 0.39, 0.29; the current-token
  head: queries 0.49. K-composition 0.17–0.20 against 0.124 ± 0.007 for random heads. The induction heads' OV circuit:
  for 83% of tokens the logit raised most is their own, copying score 0.88. Mean-ablation: 1.49 bits with every head,
  up to 2.66 without a previous-token head, up to 3.55 without an induction head, 3.59 without the current-token head,
  6.20 for random tokens. Through training, the K path's effect switches on between steps 2,500 and 2,750, with the
  loss's drop. Noising the residual stream for one target: inputs 20, 21 (and 16); between the layers 21 and 70;
  output 70.
* **Superposition and the phase diagram**: 289 cells, best of 4 seeds: 212 in superposition, 42 giving feature 2 the
  dimension, 35 dropping it; trained and the restricted reference agree on 94% of the cells (seeds agree with the best on 83%).
* **The L1 autoencoder** (512 latents, λ = 2, 4,000 steps, 211,200 vectors): 6.8 features per character, 11.2% of the
  variance unexplained, no dead latents; spliced in, 1.94 bits per character against 1.72 (the model) and 5.61 (the
  mean vector). Purity (of the 8 strongest moments, how many on one character): neurons 5.9, features 7.8.
* **Three dictionaries at equal budgets** (512 latents, 2,000 steps, 3 seeds): at 16 features per vector, variance
  unexplained TopK 6.1%, JumpReLU 8.4%, L1 11.3%; bits spliced in 1.80, 1.84, 1.93 (the model 1.72). At 8: 7.5%,
  10.5%, 17.1%; at 32: 4.9%, 6.1%, 8.1%. L1's best rescale 1.04 (λ = 0.25) to 1.30 (λ = 4); JumpReLU and TopK 1.00.
  Dead latents: none at k = 16, with or without AuxK; 2 in the 2,048-latent dictionary; 17 for TopK k = 4, 79 for
  JumpReLU λ = 8.
* **Splitting and absorption**: TopK at 128, 512 and 2,048 latents; latent 8 of the smallest ('l' after "by ") has 1
  same-character descendant in the 512 and 6 in the 2,048; 21 of the 102 clean latents have two or more. A probe reads
  upper case at 100%; the dictionary's best latent for it fires on 57% of capitals (mean of 3 seeds) and 13% are
  absorbed by another latent; Matryoshka (prefixes 32, 128): 48% and 37%, worse here, with a wide spread across seeds.
* **Transcoders and the graph**: MLP output unexplained per layer, per-layer transcoders 0.9%, 10.3%, 17.6%, 6.0%;
  cross-layer 1.0%, 9.0%, 13.2%, 4.4%. Every MLP replaced: 2.03 bits per character (per-layer, same top guess 81%),
  1.96 (cross-layer, 83%), against 1.72 for the model and 5.04 with the MLPs mean-ablated. The graph for '…she sai' →
  'd': 3,058 active features; the local replacement model matches the logits to within 10⁻⁵; logit 11.58 = features
  9.60 + embeddings 2.05 + errors 0.04 + biases; the 16 most influential features switched off in the real model
  against the graph's prediction: r = 0.94.
* **Model diffing** (BatchTopK crosscoders, 1,024 latents, k = 32, 18,600 novel and 27,347 chat tokens): after block
  3 and after block 5, every live latent shared (r from 0.42 to 0.62 and from 0.46 to 0.64); the most chat-leaning
  latents fire on "<|user|>Write", "<|assistant|>", "<|user|>Which" with r ≈ 0.53; the activation-difference lens on
  novel text: punctuation and function words, no chat markers; the mean difference is 14% of a vector's length.
* **Steering**: the quotation feature (latent 440) at α = 0, 0.25, 0.5: 0.0, 1.8, 8.0 marks of speech per 160
  characters (5 samples); a random direction at 0.5: 0.6. The mood vector (cheerful minus gloomy words in 8 frames,
  after block 3): AUROC 0.66 on held-out words, 0.74 on 110 + 110 novel sentences; cheerful-minus-gloomy words per
  hundred at α = −0.6 … 0.6: −0.9, +0.1, +0.6, +1.4, +1.7 (a random direction: −0.2, −0.4, +0.6, −0.3, +1.5); fluency
  5.05, 4.34, 4.37, 4.56, 5.49 bits per token.
* **Grokking** ((a + b) mod 59, 30% of the table): memorized by step 100, test accuracy above 99% at step 10,300; key
  frequencies 7, 23, 4, 28, 14 hold 95% of the embedding at the end; 490 of 512 neurons put more than half their
  activation at one frequency; the restricted loss falls below 1 nat at step 5,800, the test loss only at step 9,000; the key waves explain
  81% of the final logits' variance.
* **Disagreements**: TopK dictionaries from different seeds share 15% of latents (cosine ≥ 0.7; L1: 68%). Sparse
  probing on the novels model after block 5 (majority 79% in distribution, 51% in chat transcripts): at 16 examples
  linear 76%, 8 latents 78%, 1 latent 78%; at 4,096, 90%, 86%, 85%, and in chat transcripts 76%, 66%, 59%. An
  autoencoder on a random copy of Part 13's transformer: purity 7.2 of 8, against 7.7 for the trained one.

## Problems found and fixed while making it

* **Neither of our transformers has an induction head.** The plan was to find the induction circuit in Part 13's
  transformer or the novels model. Shown repeated held-out text, both find the second copy no easier than the first,
  and no head attends to the token after an earlier match: both stopped training at about 25 million tokens, two
  orders of magnitude before the window where Olsson et al. saw induction heads form. Chapter 4 says so and takes
  apart Part 13's attention-only model trained on repeated random tokens instead, retrained here with Part 13's recipe
  and seed.
* **A mood vector from whole sentences was noise.** Averaging the novels model's vectors over cheerful and over gloomy
  sentences gave a direction that separated held-out sentences at chance (AUROC about 0.47 in the smoke test): one
  mood word in twenty tokens is diluted. Contrasting the words themselves in the same frames, as contrastive
  activation addition does, gives a direction that works as a monitor.
* **The first sparsity sweeps did not overlap.** At equal steps, L1 and JumpReLU penalties chosen by guess gave
  sparsities that barely met TopK's; the sweeps were widened to five strengths each, and the pieces are now keyed by
  run, so widening a sweep keeps the runs already done.
* **The induction circuit is a team.** The first analysis assumed one previous-token head and one induction head;
  the retrained model has two previous-token heads, three induction heads and a current-token head, and single-head
  path patching showed only part of the effect (the heads share the job). The analysis now groups the heads by their
  scores and patches the group; the residual-stream map uses noising (one corrupted vector in the clean run), which
  shows the circuit's AND structure cleanly where single-position denoising could not.
* **No chat-only features.** A crosscoder after block 3 found every latent shared; a second one after block 5 found
  the same. The chapter reports it, and shows the most chat-leaning latents (shared, r ≈ 0.53) instead.
* **A probe comparison on the wrong model.** "Inside a quotation" is barely decodable after block 2 of Part 13's
  character model (a linear probe at the majority rate), so the SAE-against-probe comparison moved to the novels model
  after block 5, with an autoencoder trained there, and chat transcripts as the out-of-distribution test.
* **Special tokens were invisible.** The tokenizer drops special tokens when decoding by default, so the chat markers
  never showed in contexts; `acts.token_strings` now keeps them.
* **Splitting needed a criterion.** The first family shown was picked by decoder cosine alone, and its "children"
  fired on unrelated characters; children must now fire on the parent's character too.
* **A plot clipped by its own axes.** `CornerAxes` re-bases `ax.y_range` at zero, so the grokking chapter's log-scale
  curves, clipped to `ax.y_range`, were flattened at a loss of 1 and its dashed markers overshot the frame; the
  chapter now keeps the true range on the axes object. The SAE replay likewise clips the untrained start (variance
  left about 3) at the top of its 0-to-1 axis.
* **A seed-share claim the data did not support.** An early line said a small model is "kinder" than a big one; ours
  shares fewer latents across seeds (TopK) than Paulo and Belrose's 30%, and the L1 runs far more, so the narration
  now says exactly that.
* **Narration splices.** Every computed sentence is an f-string over cached data, and every verdict is assigned before
  it is spliced in (no conditional nested inside a sum), so `tools/zh_lines.py` lists and translates each branch.

## References

Saliency and its checks: K. Simonyan, A. Vedaldi & A. Zisserman, *Deep Inside Convolutional Networks* (2013);
M. Zeiler & R. Fergus, *Visualizing and Understanding Convolutional Networks* (2014); J. Adebayo et al., *Sanity Checks
for Saliency Maps* (NeurIPS 2018). Feature visualization and circuits: A. Mordvintsev, C. Olah & M. Tyka, *Inceptionism*
(2015); D. Bau et al., *Network Dissection* (CVPR 2017); C. Olah, A. Mordvintsev & L. Schubert, *Feature Visualization*
(Distill 2017); C. Olah et al., *The Building Blocks of Interpretability* (Distill 2018); C. Olah et al., *Zoom In: An
Introduction to Circuits* (Distill 2020); G. Goh et al., *Multimodal Neurons in Artificial Neural Networks* (Distill
2021). Transformer circuits: N. Elhage et al., *A Mathematical Framework for Transformer Circuits* (2021); C. Olsson et
al., *In-context Learning and Induction Heads* (2022); K. Wang et al., *Interpretability in the Wild: a Circuit for
Indirect Object Identification in GPT-2 small* (2022); N. Goldowsky-Dill et al., *Localizing Model Behavior with Path
Patching* (2023). Probes and lenses: G. Alain & Y. Bengio, *Understanding Intermediate Layers Using Linear Classifier
Probes* (2016); J. Hewitt & P. Liang, *Designing and Interpreting Probes with Control Tasks* (EMNLP 2019); Y. Elazar et
al., *Amnesic Probing* (TACL 2021); nostalgebraist, *interpreting GPT: the logit lens* (2020); N. Belrose et al.,
*Eliciting Latent Predictions from Transformers with the Tuned Lens* (2023). Patching: J. Vig et al., *Causal Mediation
Analysis for Interpreting Neural NLP* (2020); K. Meng et al., *Locating and Editing Factual Associations in GPT* (2022).
Superposition and dictionaries: N. Elhage et al., *Toy Models of Superposition* (2022); W. B. Johnson & J. Lindenstrauss
(1984); T. Bricken et al., *Towards Monosemanticity* (2023); H. Cunningham et al., *Sparse Autoencoders Find Highly
Interpretable Features in Language Models* (2023); A. Templeton et al., *Scaling Monosemanticity* (2024); L. Gao et al.,
*Scaling and Evaluating Sparse Autoencoders* (2024); S. Rajamanoharan et al., *Jumping Ahead: Improving Reconstruction
Fidelity with JumpReLU Sparse Autoencoders* (2024); T. Lieberum et al., *Gemma Scope* (2024); B. Bussmann, P. Leask &
N. Nanda, *BatchTopK Sparse Autoencoders* (2024); B. Bussmann et al., *Learning Multi-Level Features with Matryoshka
Sparse Autoencoders* (2025); D. Chanin et al., *A is for Absorption* (2024). Transcoders, graphs, diffing:
J. Dunefsky, P. Chlenski & N. Nanda, *Transcoders Find Interpretable LLM Feature Circuits* (2024); E. Ameisen et al.,
*Circuit Tracing: Revealing Computational Graphs in Language Models* (2025); J. Lindsey et al., *On the Biology of a
Large Language Model* (2025); J. Lindsey et al., *Sparse Crosscoders for Cross-Layer Features and Model Diffing*
(2024); J. Minder et al., *Overcoming Sparsity Artifacts in Crosscoders to Interpret Chat-Tuning* (2025);
J. Minder et al., *Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences* (2025). Steering:
A. Turner et al., *Steering Language Models With Activation Engineering* (2023); N. Rimsky et al., *Steering Llama 2 via
Contrastive Activation Addition* (2024); A. Arditi et al., *Refusal in Language Models Is Mediated by a Single
Direction* (2024); R. Chen et al., *Persona Vectors* (2025); Anthropic, *Golden Gate Claude* (May 2024). Grokking:
A. Power et al., *Grokking* (2022); N. Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability*
(ICLR 2023). Faithfulness: M. Turpin et al., *Language Models Don't Always Say What They Think* (2023); T. Lanham et al.,
*Measuring Faithfulness in Chain-of-Thought Reasoning* (2023); Y. Chen et al., *Reasoning Models Don't Always Say What
They Think* (2025). Frontier: Anthropic, *Open-sourcing circuit tracing tools* (May 2025); L. Gao et al., *Weight-sparse
transformers have interpretable circuits* (2025); Google DeepMind, *Gemma Scope 2* (Dec 2025); J. Lindsey, *Emergent
Introspective Awareness in Large Language Models* (Oct 2025); Anthropic, *Emotion Concepts and their Function in a
Large Language Model* (Apr 2026); S. Marks et al., *Auditing Language Models for Hidden Objectives* (2025); Anthropic,
*Claude Sonnet 4.5 System Card* (Sep 2025); Anthropic, *Natural Language Autoencoders Produce Unsupervised Explanations
of LLM Activations* (May 2026). Disagreements: GDM mechanistic interpretability team, *Negative Results for Sparse
Autoencoders on Downstream Tasks and Deprioritising SAE Research* (Mar 2025); S. Kantamneni et al., *Are Sparse
Autoencoders Useful? A Case Study in Sparse Probing* (2025); G. Paulo & N. Belrose, *Sparse Autoencoders Trained on the
Same Data Learn Different Features* (2025); T. Heap et al., *Automated Interpretability Metrics Do Not Distinguish
Trained and Random Transformers* (2025); Z. Wu et al., *AxBench* (2025); L. Sharkey et al., *Open Problems in Mechanistic
Interpretability* (2025).

## Problems, with solutions

1. **Soft thresholding.** Take a > 0, λ ≥ 0 and ‖d‖ = 1. Minimize ℓ(f) = ‖a d − f d‖² + λf = (a − f)² + λf over f ≥ 0.
   On the positive branch, ℓ′(f) = −2(a − f) + λ = 0 gives f = a − λ/2; if a ≤ λ/2, the constrained minimum is f = 0.
   Thus f* = max(a − λ/2, 0). A positive optimum is shrunk by λ/2; a clipped optimum is zero. If this scalar latent is
   retained by TopK, its unpenalized objective (a − f)² has optimum f = a. This removes the L1 shrinkage term in this
   scalar comparison; it does not guarantee that a learned full encoder has unbiased amplitudes.
2. **Random cosines.** Let d ≥ 1, and let u and v be independent and uniform on the unit sphere in ℝᵈ. Sign symmetry
   gives E[u·v] = 0. Conditional on v, orthogonal invariance and independence let us map v to e₁ without changing
   u's distribution. Hence E[(u·v)²] = E[u₁²] = (1/d) Σᵢ E[uᵢ²] = (1/d) E[‖u‖²] = 1/d. The standard deviation is 1/√d.
3. **The composition score.** Let A and B be nonzero real matrices of compatible sizes, so the denominator is positive.
   If b_j are B's columns, ‖AB‖_F² = Σ_j ‖A b_j‖² ≤ ‖A‖₂² ‖B‖_F² ≤ ‖A‖_F² ‖B‖_F², giving a score in [0, 1].
   Equality in the final inequality requires A to have rank one: A = σ x yᵀ, with σ > 0 and unit x,y. Equality in the
   first requires every nonzero column of B to lie in span(y), so B = y zᵀ with z ≠ 0 and rank one. Conversely, these
   forms give AB = σ x zᵀ and score 1. The shared singular directions must therefore be parallel; their signs are immaterial.
4. **AND under patching.** Clean (1, 1) gives y = 1; corrupted (0, 0) gives y = 0. Noising either input alone gives
   (0, 1) or (1, 0), hence y = 0. Denoising either input alone also gives one of those mixed inputs, hence y = 0.
   Each input is necessary for this AND output but neither alone is sufficient. The two patching directions ask
   different questions in these clean/corrupt contexts.
5. **The zero-bias reference comparison.** W = (1, 0), b = 0: feature 1 is rebuilt exactly (ReLU(x₁) = x₁ ≥ 0), and
   feature 2 is lost, costing r E[x₂²] = r ρ E[U²] = rρ/3. W = (0, 1), b = 0 costs ρ/3. For ρ > 0 and r > 0, keeping
   the more important feature is at least as good, with equality at r = 1; at ρ = 0 all these costs are zero.
   For a further comparison, assume independent feature draws and keep b = 0. The antipodal candidate W = (1, −1)
   gives ReLU(x₁ − x₂) and ReLU(x₂ − x₁): exact when at most one feature is on, with errors only when both are on,
   an event of probability ρ². For fixed r > 0 it beats the two stated zero-bias dedicated candidates at sufficiently
   small positive ρ. This is a comparison of those candidates, not a proof of the free-bias global optimum.
6. **The grokking readout.** Let p be prime, ∅ ≠ K ⊆ {1,…,p−1}, and a,b,c ∈ ℤₚ. At c = a+b in ℤₚ every cosine is 1,
   so L(c) = |K|. For any other c, choose the nonzero residue s = (a+b−c) mod p. If cos(2πks/p) = 1, then p divides ks,
   impossible for 1 ≤ k,s ≤ p−1 because p is prime. Thus every term is below 1; since K is nonempty, L(c) < |K|.
   The maximizer is unique **over ℤₚ**. The original sum has unit positive weights; the same proof works with any
   coefficients αₖ > 0, with maximum Σₖ αₖ. Empty K, DC-only frequencies, or an unrestricted real/integer c need not give uniqueness.

## 习题与解答

1. **软阈值。**设a > 0、λ ≥ 0、‖d‖ = 1。在f ≥ 0上最小化ℓ(f) = ‖ad − fd‖² + λf = (a − f)² + λf。
   在正值分支令ℓ′(f) = −2(a − f) + λ = 0，得f = a − λ/2；a ≤ λ/2时，约束最小值在f = 0处。
   所以f* = max(a − λ/2, 0)。正的最优值缩小λ/2，截断分支为零。若TopK保留这个标量潜变量，不加惩罚的目标(a − f)²在f = a处最小。
   这个标量比较中没有L1收缩项，并不保证学到的完整编码器具有无偏的激活幅度。
2. **随机余弦。**设d ≥ 1，u、v相互独立且在ℝᵈ的单位球面上均匀分布。由符号对称性，E[u·v] = 0。
   固定v后，由正交变换不变性及独立性，可以把v映射到e₁而不改变u的分布。因此E[(u·v)²] = E[u₁²] = (1/d)ΣᵢE[uᵢ²]
   = (1/d)E[‖u‖²] = 1/d。标准差为1/√d。
3. **组合分数。**设A、B为非零、尺寸相容的实矩阵，分母因此为正。记B的列为b_j，则
   ‖AB‖_F² = Σ_j‖A b_j‖² ≤ ‖A‖₂²‖B‖_F² ≤ ‖A‖_F²‖B‖_F²，所以分数在[0, 1]内。
   最后一个不等式取等号要求A秩为一：A = σ x yᵀ，其中σ > 0，x、y为单位向量。第一个不等式取等号要求B的每个非零列都在span(y)内，
   因此B = y zᵀ，其中z ≠ 0，B也秩为一。反过来，这些形式给出AB = σ x zᵀ，分数为1。共享维度中的奇异方向必须平行，符号无关。
4. **修补下的“与”门。**干净输入(1, 1)给出y = 1，破坏后(0, 0)给出y = 0。只破坏一个输入，得到(0, 1)或(1, 0)，所以y = 0。
   只恢复一个输入也得到这两种混合输入之一，所以y = 0。每个输入对这个“与”门输出都是必要的，但单独哪一个都不充分。
   两个修补方向在这些干净与破坏输入的条件下，回答的是不同问题。
5. **零偏置参考比较。**W = (1, 0)、b = 0时，特征1被精确重建，特征2丢失，代价r E[x₂²] = rρ/3。
   W = (0, 1)、b = 0时代价为ρ/3。ρ > 0、r > 0时，保留更重要的特征至少不差；r = 1时相等。ρ = 0时这些代价都为零。
   作为进一步比较，假设特征独立抽样，并保持b = 0。反向候选W = (1, −1)给出ReLU(x₁ − x₂)和ReLU(x₂ − x₁)：
   至多一个特征出现时重建精确，只有两个同时出现才会出错，该事件的概率为ρ²。固定r > 0时，ρ为足够小的正数，这个候选优于上述两个零偏置专用候选。
   这里只比较这些候选，并没有证明允许自由偏置时的全局最优解。
6. **顿悟的读出。**设p为素数，∅ ≠ K ⊆ {1,…,p−1}，且a、b、c ∈ ℤₚ。在c = a+b（按模p计算）处，每项余弦都是1，所以L(c) = |K|。
   对其他c，取非零剩余类s = (a+b−c) mod p。cos(2πks/p) = 1要求p整除ks；但p为素数且1 ≤ k,s ≤ p−1，因此不可能。
   每项都小于1，而K非空，所以L(c) < |K|。最大值在**ℤₚ上**唯一。原题的权重均为正的1；任何αₖ > 0的加权版本同理，最大值为Σₖαₖ。
   K为空、只有直流频率，或c不受限制而取实数或整数时，都不一定具有唯一最大值。

## Glossary (terms in this part)

| English | 中文 |
|---|---|
| interpretability, mechanistic interpretability | 可解释性，机制可解释性 |
| saliency map, gradient × input, occlusion | 显著图，梯度乘输入，遮挡 |
| sanity check, cascading randomization | 合理性检查，逐层随机化 |
| feature visualization, DeepDream, network dissection | 特征可视化，DeepDream，网络解剖 |
| the Circuits thread; features, circuits, universality | Circuits系列；特征，回路，普遍性 |
| multimodal neuron | 多模态神经元 |
| probe, linear probe, MLP probe | 探针，线性探针，MLP探针 |
| control task, selectivity | 对照任务，选择性 |
| amnesic probing (projecting a direction out) | 失忆探测（把一个方向投影掉） |
| decodable vs used | 可读出 vs 被使用 |
| residual stream, unembedding | 残差流，反嵌入 |
| logit lens, tuned lens, translator | logit透镜，调校透镜，翻译器 |
| activation patching, clean run, corrupted run | 激活修补，干净运行，被破坏的运行 |
| noising (necessary), denoising (sufficient) | 加噪（检验必要性），去噪（检验充分性） |
| path patching | 路径修补 |
| causal tracing, causal mediation | 因果追踪，因果中介 |
| induction head, previous-token head | 归纳头，前一词元头 |
| attention-only transformer | 只有注意力的Transformer |
| QK circuit, OV circuit, composition score, K-composition | QK回路，OV回路，组合分数，K组合 |
| copying score | 复制分数 |
| mean ablation | 均值消融 |
| superposition, interference | 叠加，干扰 |
| phase diagram, density, relative importance | 相图，密度，相对重要性 |
| antipodal pair | 反向的一对 |
| monosemantic, polysemantic | 单义，多义 |
| sparse autoencoder (SAE), dictionary, latent | 稀疏自编码器（SAE），字典，潜变量 |
| encoder, decoder, reconstruction | 编码器，解码器，重建 |
| L0 (features on per vector), L1 penalty | L0（每个向量亮着的特征数），L1惩罚 |
| fraction of variance unexplained | 未解释方差占比 |
| spliced-in loss (bits with the rebuild) | 接回后的损失（用重建时的比特数） |
| shrinkage, soft thresholding | 收缩，软阈值 |
| TopK, BatchTopK, JumpReLU, straight-through estimator | TopK，BatchTopK，JumpReLU，直通估计 |
| dead latent, AuxK | 死潜变量，AuxK |
| feature splitting, feature absorption | 特征分裂，特征吸收 |
| Matryoshka dictionary | 套娃字典 |
| transcoder, cross-layer transcoder, replacement model | 转码器，跨层转码器，替代模型 |
| local replacement model, error node, dark matter | 局部替代模型，误差节点，暗物质 |
| attribution graph, influence, pruning | 归因图，影响力，剪枝 |
| crosscoder, model diffing, relative decoder norm | 交叉编码器，模型差分，相对解码器范数 |
| activation-difference lens | 激活差透镜 |
| steering, steering vector, activation addition | 引导，引导向量，激活加法 |
| contrastive activation addition, persona vector | 对比激活加法，人格向量 |
| preventative steering | 预防性引导 |
| monitor, AUROC | 监控器，AUROC |
| grokking, modular addition | 顿悟，模加法 |
| Fourier spectrum, key frequency | 傅里叶频谱，关键频率 |
| progress measures: restricted loss, excluded loss | 进度指标：受限损失，排除损失 |
| memorization, circuit formation, clean-up | 记忆，回路形成，清理 |
| faithfulness (of a chain of thought), motivated reasoning | （思维链的）忠实性，动机推理 |
| introspection, concept injection | 内省，概念注入 |
| emotion concepts (functional emotions) | 情绪概念（功能性情绪） |
| alignment audit, hidden objective, auditing game | 对齐审计，隐藏目标，审计游戏 |
| evaluation awareness | 评测意识 |
| natural-language autoencoder | 自然语言自编码器 |
| weight-sparse transformer, parameter decomposition | 权重稀疏的Transformer，参数分解 |
| ambitious vs pragmatic interpretability | 雄心派与务实派可解释性 |

## QA scope: phase reference assumptions

The historical phase output and its reported agreement are preserved. Its reference candidates fix the retained
weights at unit length, force zero bias for a dropped feature, and search a shared nonpositive bias for the antipodal
pair. This is a restricted comparison, not a certificate of optimal phase boundaries. Problem 5 explicitly assumes
zero output bias. With free output bias, a dropped feature is best predicted by its mean ρ/2: its squared error is
Var(x) = ρ/3 − ρ²/4, so the two omitted-feature costs are r(ρ/3 − ρ²/4) and ρ/3 − ρ²/4. A shared antipodal candidate
can also benefit from positive bias. Corrected reference recipes require separate validation and recomparison before
replacing any historical phase figures.

历史相图输出及其一致率予以保留。参考候选固定单位权重，丢弃特征时偏置为零，反向共享时只搜索非正的公共偏置。
这是受限比较，不能证明最优相边界。习题5明确假定输出偏置为零。偏置可自由变化时，丢弃特征应预测其均值ρ/2，
误差为方差ρ/3 − ρ²/4；两种丢弃方案的代价分别为r(ρ/3 − ρ²/4)及ρ/3 − ρ²/4。反向共享候选也可能受益于正偏置。
修正配方须单独验证和重新比较，才能用于替换历史图表。

### QA scope: probe validation and rank correlations

Fresh candidates retain the original run before scientific corrections. The probe split now keeps the original
validation windows, resamples training windows whose input/next-token spans overlap validation, and fits the control
label rate from training rows only. Amnesic losses use validation rows only. Layer selection still uses this same
validation set; this is not a separate final evaluation cohort. The older fresh candidate had 278 scored positions
shared across the split (3.10% of validation rows) and included training rows in amnesic evaluation; it is preserved
for comparison. Spearman correlation now averages tied ranks and fails explicitly for undefined constant inputs.
On the 55 captured comparisons in the fresh saliency candidate, there were no ties and no numerical change.

探针验证窗口保持不变；与验证输入和下一词元目标重叠的训练窗口会重新抽样。对照标签的比例只由训练行确定，
失忆探测的损失只在验证行上计算。层的选择仍使用同一个验证集，并不是另一个独立的最终评测集合。修正前的新候选
有278个评分位置同时出现在两组中，占验证行的3.10%，失忆评测也包含训练行；该候选保留用于比较。
Spearman相关现对并列值使用平均秩，常量输入等无定义的情况会明确报错。本次显著图候选的55组输入没有并列，数值不变。

The phase replay shows one seed, while the colored grid keeps the best of four. They can end at different solutions;
the replay is labeled accordingly. The saliency chapter marks the unevaluated last-character occlusion as missing,
rather than plotting it as a zero measurement.

相图的回放展示一个种子，彩色网格则保留四个种子中最好的；两者可能停在不同的解上，图中现明确标注。
显著图一章也把最后一个字符未计算的遮挡影响标为缺失，不再画成零测量。

### QA scope: circuit metrics

The induction path measurements now isolate the final-model selected induction receivers used by the diagram;
all-layer-2 receiver measurements remain in separate `*_all` fields. Raw path effects through training use nats
directly, including near-zero early clean/corrupt gaps. Normalized final effects require a positive measured gap.

The grokking model remains the original local adaptation, including its initialization and NumPy split. It is not an
exact replication of the paper's parameterization. Corrected progress metrics retrospectively follow five frequencies
selected from the final neuron-to-logit map, with that cardinality explicitly chosen. Restricted logits retain the
answer-specific input mean; excluded logits remove only the selected waves. The original adaptive embedding-frequency
metrics are retained under `legacy_*`. Raw intermediate logits and pinned atomic checkpoints support independent
rescoring and matching-budget resume. The final phase-aligned cosine fit and its all-pairs fitted-readout accuracy are
reported separately from an unconstrained sum-wave fit and from the model's held-out accuracy. Spectrum bars show
actual nonconstant embedding-energy shares on one fixed vertical scale throughout training.

归纳回路的路径测量现只修补图中那些由最终模型选出的归纳接收头；全部第二层接收头的测量保留在独立的`*_all`字段。
训练回放直接使用奈特差值，早期干净与破坏输入之间的差距接近零时也无需做除法；最终归一化效应必须有正的实测差距。
顿悟模型的初始化和NumPy数据划分仍是原有本地改编，并不完全复刻论文的参数化。新进度指标从最终神经元到logit的映射
选取五个频率，再回头追踪这些固定频率；五这个数量是明确选定的。受限logit保留每个答案的输入均值，排除logit只去掉所选波。
旧的自适应嵌入频率指标保留在`legacy_*`字段。原始中间logit和带有来源约束的原子检查点可供重算及同预算恢复。
相位对齐余弦拟合、其在所有数对上的拟合读出准确率，与无约束和角波拟合及模型留出准确率分别报告。
频谱柱形图在训练全程使用固定纵轴，展示真实的嵌入非恒定能量占比。

### QA scope: measured ranges and evaluation cohorts

Signed intervention effects retain negative values and values above one. The patching heatmap includes only tested
positions through its target; later array padding is not a measurement. Negative head-noising effects explicitly mean
the swap improved the prediction. A positive-real eigenvalue copying score is a diagnostic, not proof of identity in
the token basis. Plot geometry is computed from the axis mapping, including negative QK position scores.

SAE L0/FVU and transcoder reconstruction curves are fitting-pool/batch metrics. Their full observed ranges are shown,
including FVU above one. Replacement-model bits are a separate forward evaluation. Neuron and SAE context-purity
histograms search different text pools, so they are labeled descriptive comparisons. Exact error-corrected replacement
logits on one prompt and correlated selected ablations do not establish a complete causal account of the original model.
Grokking markers report recorded training/held-out accuracy thresholds; missing thresholds do not produce step-zero
markers. Progress prose uses measured endpoints and sampled checkpoints, and the positive-coefficient trigonometric
illustration is distinct from the unconstrained cosine fit.

干预效应保留负值和大于一的值；修补热图只展示实际测量的位置，不把目标之后的填充值当成测量。负的加噪效应表示
替换改善了预测。正实特征值分数只是诊断，并不能证明词元基底上的恒等复制。图形尺寸由真实坐标映射计算。
SAE和转码器的重建曲线明确标注拟合样本范围，并保留大于一的FVU；替换模型的比特数另外评估。神经元与SAE纯度
使用不同文本池，因此只是描述性比较。单个提示上带误差项的精确替代、以及部分干预的相关性，不等于完整因果解释。
顿悟阈值明确对应记录检查点上的准确率；缺少阈值时不画第零步标线。正权重三角函数示意与无约束余弦拟合分别说明。

## Shared caption integration

This reviewed source branch carries the owned `text_zh_add.json` and a guarded `caption_delta.json`. The shared
`videos/ai/ai_text_zh.json` remains identical to this branch's public QA parent; it is not replaced by a worker copy.
The root integrator applies the delta entry by entry when integrating into shared QA. Before that integration,
new Chinese on-screen captions are not fully active on this branch.

Preview the guarded merge with:

```sh
python videos/ai/ai30/apply_caption_delta.py videos/ai/ai30/caption_delta.json videos/ai/ai_text_zh.json
```

The same command with `--write` applies nonconflicting entries atomically and preserves unrelated translations.
A conflicting existing value stops the operation before writing. Source publication does not close the scientific
input or rendered-acceptance gates documented above; no private data, models, media or evidence archives are included.
