# AI, Built (人工智能，从零搭建)

A thirty-one-part course on how modern AI works and how it came to be, in English and Chinese: from Shannon's
information theory and the symbolic era, through statistical learning and the deep learning revolution, to
transformers, frontier language models, generative models, reinforcement learning, reasoning, agents, and what we
find inside the models. Each part is a 30-60 minute lecture that derives its mathematics on screen and tells its
history. Every number on screen comes from a real computation, a model trained or probed on the CPU that renders
the video, or from a published configuration or report, cited. Schematics are labeled `schematic` and made-up
examples `illustrative`. Videos are `ai1` … `ai31`.

The chapter-by-chapter plan and production standard are in [`SYLLABUS.md`](SYLLABUS.md). All 31 parts have chapter
sources and bilingual narration tables. Generated videos from the earlier 20-part cut must be rebuilt against the
current manifests; the presence of source files or an old export does not indicate that a part has passed QA.

## The story

**Shannon's guessing game.** In 1951 Claude Shannon asked people to guess the next letter of an English text, and
from their mistakes estimated how much information English carries. Every modern model plays a version of that
game: language models guess the next token, diffusion models guess the noise, robot policies guess the next
action, world models guess the next frame. The question that grows through the series: *what do you have to know
to guess well?* And alongside it, the field's own history: who tried what, why it worked or didn't, and how each
idea led to the next.

* **Act I, Foundations**: information, the symbolic era and its search and logic, linear algebra, calculus and
  autodiff, randomness.
* **Act II, Learning from Data**: classical and statistical learning, generalization, neural networks, the deep
  learning revolution (CNNs, RNNs), optimization, and the mathematics of scale.
* **Act III, The Transformer Era**: attention, the language-model lineage from GPT-1 to today's open-weight
  frontier, memory, sparsity, the hardware, pretraining at scale, and inference.
* **Act IV, Generation and Perception**: VAEs, GANs, flows and energy models; diffusion and flow matching; images,
  video and 3D; tokens for every sense; self-supervised learning; symmetry and science (AlphaFold, weather, maths).
* **Act V, Agency**: reinforcement learning from Bellman to AlphaZero and MuZero, post-training and alignment,
  reasoning, agents and world models.
* **Finale**: open a model up and see what it knows; then ask whether we can trust it.

Three devices hold it together:

1. **The scoreboard** (`explainer.ai.scoreboard`): one fixed passage, chapter 2 of Dashiell Hammett's *The Maltese
   Falcon* (1930), in the US public domain and on Project Gutenberg since 1 January 2026. It is held out of the
   training data for the models we build here. Earlier editions may have reached pretrained models; the Gutenberg
   release date does not establish that their training data is uncontaminated. Each row is a model's bits per
   character on it. Part 1 computes the passage and the first
   rows (`.cache/ai1/scoreboard.json`); later parts add the models they build (Kneser–Ney and an ∞-gram in Part 7,
   a neural n-gram in Part 9, a character LSTM in Part 10, a small transformer in Part 13, and more), all trained on
   the same thirty novels.
2. **Payoffs**: each idea is introduced with "where this comes back" (`explainer.ai.payoff_card`), and the later
   part opens by calling back to it.
3. **The timeline strip** (`explainer.ai.timeline`, 1940–2030) on every chapter card.

## QA evidence

Run chapters in manifest order, with a separate process and evidence folder for each one:

```bash
python tools/qa_series.py ai1 --cached-only                 # animation endpoints and translation/layout checks
python tools/qa_series.py ai1 --lang zh --cached-only       # Chinese layout
python tools/qa_series.py ai1 --motion --cached-only --timeout 1200  # real silent playback and dead-air scans
python tools/qa_audio.py ai1 --lang en                    # production voice, captured narration, signal/timing QA
python tools/qa_report.py                                 # renders/qa/series/index.html
```

`--series ai --resume` continues the whole series, rechecking changed source or data. Missing data is reported
without starting a second training job. Evidence includes frames, contact sheets, logs and input signatures.
Endpoint checks do not examine intermediate animation frames. Silent playback does not verify synthesized
narration. Both the visual review and narrated playback must be completed before production approval.
Audio checks use the actual English narration captured by the chapter run (including computed results),
translate it for Chinese, and retain its provenance. Start the documented narration server first. Signal/timing
checks and the server's ASR checks provide review evidence; listening remains a separate check.

The numbering migration renames generated files; it does not update their embedded titles, chapter markers,
frames, or narration. Rebuild older cuts from the current manifests before production approval. The local QA
index includes the legacy-export audit and any narrated previews alongside the chapter evidence.

## How it looks

The series draws in the manner of 3Blue1Brown, with the instruments in `explainer/ai/viz.py`:

* **One idea per frame, drawn big.** The narration explains; the screen shows. Words on screen are few and large.
* **Continuity.** Objects turn into the next representation instead of fading out: a heatmap becomes a mosaic of
  the unit square, a straight line bends into the log curve, a loss landscape reshapes from one valley to two.
  Derivations happen in place (`cmath` + `morph`): each term slides to where the next step needs it.
* **Color is meaning.** A symbol keeps its color in every equation and in the picture it describes (`C.TRUE_P` for
  the data's p, `C.MODEL_Q` for the model's q, `C.SURPRISE`, `C.ENTROPY`, `C.KL`, ...).
* **The camera narrates.** Zooms (magnify a piece, keep a mini-map of the whole) and 3D surfaces with the camera
  moving over them (`loss_surface`, `surface_path`; scenes mix in `ThreeDScene`).
* **Live quantities.** Value trackers drive bars (`LiveBars`), dots (`glow_dot`) and readouts, so a parameter is
  seen to change.
* **Real numbers.** Everything plotted is computed by the part's `compute.py` and asserted in the scene.

## The parts

| # | Part | Mathematics and history | Models, data |
|---|---|---|---|
| **I** | **Foundations** | | |
| 1 | The Guessing Game | probability, surprise, entropy, Kraft, Huffman, typical sets, cross-entropy, KL, arithmetic coding, maximum likelihood, mutual information | counting models, gzip/xz/bzip2, GPT-2, Qwen3 |
| 2 | Thinking Machines | Turing, Dartmouth, search and A*, games and alpha–beta, logic and SAT, planning, expert systems, the AI winters | Samuel's checkers, Deep Blue, ELIZA |
| 3 | Vectors That Mean Things | inner products, eigenvalues, SVD and Eckart–Young, norms, random matrices, high-dimensional geometry, Johnson–Lindenstrauss, matrix factorization | word2vec, GPT-2's embeddings, the Netflix Prize |
| 4 | Change | gradients, Jacobians, reverse-mode autodiff (the series' own library), numerics, curvature, Lagrange and KKT, implicit differentiation | |
| 5 | Randomness in Motion | Gaussians, MLE and Bayes, exponential families, concentration, sampling and decoding, Markov chains, Monte Carlo, MCMC, Brownian motion, SDEs, Fokker–Planck | |
| **II** | **Learning from Data** | | |
| 6 | Classical ML | least squares, ridge and lasso, logistic regression, LDA, k-NN, kernels and SVMs, trees, forests, boosting | Viola–Jones |
| 7 | Statistical ML | PCA, EM, HMMs, graphical models, causality, Gaussian processes, variational inference, topic models, statistical MT, Kneser–Ney | the scoreboard's KN and ∞-gram rows |
| 8 | Fitting and Generalizing | ERM, bias–variance, VC, Rademacher, PAC-Bayes, implicit bias, double descent, distribution shift | |
| 9 | Networks | McCulloch–Pitts to backprop, universal approximation, depth, initialization, signal propagation, residuals, normalization, gating | a neural n-gram model (Bengio 2003) |
| 10 | Seeing and Remembering | convolution and equivariance, the ImageNet moment, adversarial examples, RNNs, LSTMs, seq2seq, the first attention | LeNet, AlexNet, ResNet, a character LSTM |
| 11 | Going Downhill | convergence rates, SGD as an SDE, edge of stability, momentum, Adam/AdamW, natural gradient, Shampoo, Muon, schedules | |
| 12 | The Mathematics of Scale | NTK vs μP, hyperparameter transfer, scaling laws, Chinchilla, over-training, emergence, grokking | |
| **III** | **The Transformer Era** | | |
| 13 | Attention as Geometry | attention as a kernel smoother, RoPE, YaRN, sinks and gates, QK-norm, induction heads, in-context learning, expressivity | our own small transformer |
| 14 | The Language-Model Lineage | the 2017 Transformer, GPT-1 and BERT, T5, GPT-2/3, instruction tuning, ChatGPT, open weights, compute trends | GPT, BERT, T5, LLaMA, DeepSeek, Qwen, Kimi |
| 15 | Memory | KV caches, GQA and MLA, linear attention, SSMs, the (gated) delta rule, test-time training, hybrids, retrieval | DeepSeek, Qwen3-Next, Kimi Linear |
| 16 | Sparsity | mixture-of-experts routing and balancing, expert parallelism, sparse attention (NSA, DSA), pruning | DeepSeek-V3.x, GLM, Kimi |
| 17 | Silicon | GPUs and SIMT, tiling and arithmetic intensity, the roofline, systolic arrays, number formats, interconnects | the machine rendering the video |
| 18 | Pretraining at Scale | data pipelines and dedup, data/tensor/pipeline/expert parallelism, ZeRO, FP8 training, stability, multi-token prediction | |
| 19 | Inference | speculative decoding, quantization (GPTQ, rotations, MXFP4/NVFP4), FlashAttention, paged KV, serving | gpt-oss |
| **IV** | **Generation and Perception** | | |
| 20 | Four Ways to Generate | autoregressive models, VAEs, GANs and WGAN, normalizing flows, neural ODEs, energy models, FID | Hopfield, Boltzmann, StyleGAN |
| 21 | Diffusion and Flow | score matching, the reverse SDE, DDPM/DDIM, EDM, flow matching, reflow, distillation, guidance, discrete diffusion | LLaDA |
| 22 | Images, Video and 3D | ViT, latent spaces, DiT, SD3, next-scale prediction, unified models, video autoencoders, diffusion forcing, NeRF, Gaussian splatting | SD3/Flux, video models |
| 23 | Every Sense Is a Token | BPE, byte-level models, VQ and FSQ, RVQ, audio and CTC, CLIP vs SigLIP, VLMs, omni models | Whisper, Qwen3-TTS (the narrator) |
| 24 | Learning Without Labels | contrastive learning, BYOL and collapse, DINO, MAE, JEPA, embeddings | DINOv3, V-JEPA 2 |
| 25 | Symmetry and Science | groups and equivariance, GNNs and the WL test, AlphaFold 2/3, weather models, AI for mathematics | AlphaFold, GraphCast, AlphaProof |
| **V** | **Agency** | | |
| 26 | Reinforcement Learning | bandits and UCB, Bellman, TD, Q-learning and DQN, policy gradients, PPO, MCTS, AlphaGo, AlphaZero, MuZero, CFR | our own AlphaZero (Connect Four) |
| 27 | Post-Training and Alignment | SFT, LoRA, reward models, RLHF, DPO, Constitutional AI, distillation, merging | InstructGPT |
| 28 | Reasoning | chain of thought as computation, PRMs, RLVR, GRPO and its variants, pass@k, test-time scaling | o-series, R1 |
| 29 | Agents and Worlds | POMDPs, tool use, long horizons, imitation learning, world models, VLAs | Dreamer, Genie, π0 |
| **Finale** | | | |
| 30 | Inside the Model | probing, patching, superposition, sparse autoencoders, transcoders and attribution graphs, steering, CoT faithfulness | |
| 31 | Can We Trust It? | evaluation science, arenas, reward hacking, scalable oversight, monitoring and control, open problems | the final scoreboard |

## Shared code and the Chinese edition

`explainer/ai/` holds the series' instruments (chapter cards, series map, scoreboard, payoff and reference cards);
the text helpers and derivation ladder are the analysis series' (`explainer.analysis`). Chinese narration lives in
`videos/ai/aiN/narration_zh.json`, on-screen text in `videos/ai/ai_text_zh.json` (`tools/collect_text.py --check
aiN`), and terms in [`AI_ZH_GUIDE.md`](AI_ZH_GUIDE.md).
