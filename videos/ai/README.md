# AI, Built (人工智能，从零搭建)

A twenty-part series on the mathematics of modern AI models, in English and Chinese, from probability to
frontier systems. Each part derives its mathematics on screen, and every number on screen comes from a real
computation: a model trained or probed on the 4-core CPU that renders the video, or a published configuration or
report, cited. Schematics are labeled `schematic` and made-up examples `illustrative`. Videos are `ai1` … `ai20`.

## The story

**Shannon's guessing game.** In 1951 Claude Shannon asked people to guess the next letter of an English text, and
from their mistakes estimated how much information English carries. Every modern model plays a version of that
game: language models guess the next token, diffusion models guess the noise, robot policies guess the next
action, world models guess the next frame. The question that grows through the series: *what do you have to know
to guess well?*

* **Act I, Foundations**: the language to ask the question (probability and information, linear algebra and
  geometry, calculus and autodiff, randomness).
* **Act II, Learning**: guessing from statistics, and why it generalizes.
* **Act III, Engines**: guessing about structure, in every kind of data.
* **Act IV, Agency**: guessing about the world and its consequences.
* **Finale**: open a model up and see what it knows.

Three devices hold it together:

1. **The scoreboard** (`explainer.ai.scoreboard`): one fixed passage, chapter 2 of Dashiell Hammett's *The Maltese
   Falcon* (1930), in the US public domain and on Project Gutenberg since 1 January 2026, after every model on the
   board was trained. Each row is a model's bits per character on it. Part 1 computes the passage and the first
   rows (`.cache/ai1/scoreboard.json`); later parts add the models they build (Kneser–Ney counting in Part 6, a
   neural n-gram model in Part 8, a small transformer in Part 11), all trained on the same thirty novels.
2. **Payoffs**: each idea is introduced with "where this comes back" (`explainer.ai.payoff_card`), and the later
   part opens by calling back to it.
3. **The timeline strip** (`explainer.ai.timeline`, 1940–2030) on every chapter card.

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

| # | Part | Mathematics | Models, data |
|---|---|---|---|
| **I** | **Foundations** | | |
| 1 | The Guessing Game | probability, the chain rule, surprise, entropy, Kraft, Huffman, cross-entropy, KL, arithmetic coding, maximum likelihood, the softmax gradient, mutual information | counting models, gzip/xz/bzip2, GPT-2, Qwen3 |
| 2 | Vectors That Mean Things | inner products, eigenvalues, SVD and Eckart–Young, spectral norm, high-dimensional geometry, Johnson–Lindenstrauss | word2vec, GPT-2's embeddings |
| 3 | Change | gradients, Jacobians, Hessians, the chain rule, reverse-mode autodiff (the series' own small library), Taylor and curvature | |
| 4 | Randomness in Motion | Gaussians, MLE and Bayes, Markov chains, Monte Carlo and importance sampling, Brownian motion, SDEs, Fokker–Planck | |
| **II** | **Learning** | | |
| 5 | Classical ML | least squares and its geometry, ridge and lasso, logistic regression, LDA, k-NN, kernels and SVMs, trees, forests, boosting | |
| 6 | Statistical ML | PCA, mixtures and EM, HMMs, graphical models, Gaussian processes, variational inference, Kneser–Ney n-grams | the scoreboard's KN row |
| 7 | Fitting and Generalizing | ERM, bias–variance, VC and Rademacher, random labels, double descent | |
| 8 | Networks | universal approximation, depth and linear regions, initialization, signal propagation, residuals, normalization, pre-norm/RMSNorm/SwiGLU | a neural n-gram model (Bengio 2003) |
| 9 | Going Downhill | SGD as an SDE, edge of stability, Adam/AdamW, Muon (spectral steepest descent, Newton–Schulz, QK-clip), schedules (WSD) | |
| 10 | The Mathematics of Scale | NTK vs μP, hyperparameter transfer, scaling laws, Chinchilla (L(N, D) fit, over-training), grokking | |
| **III** | **Engines** | | |
| 11 | Attention as Geometry | attention as a kernel smoother, RoPE, YaRN (ramp and temperature), attention sinks, sink logits, output gates, QK-norm, soft caps, induction heads, in-context learning | our own small transformer |
| 12 | Memory | KV caches, GQA and MLA, linear attention, SSMs (Mamba-2 and state-space duality), the delta rule and gated delta rule (Householder geometry, WY/UT chunkwise training), test-time training, hybrids | DeepSeek, Qwen3-Next, Kimi Linear |
| 13 | Sparsity | mixture-of-experts routing and balancing (DeepSeek-V3's sigmoid router, fine-grained experts), sparse attention (NSA, DSA) | DeepSeek-V3.x, GLM, Kimi |
| 14 | Diffusion and Flow | score matching, the reverse SDE, DDPM/DDIM, flow matching, reflow, MeanFlow and shortcut models, guidance, discrete and block diffusion | LLaDA |
| 15 | Images and Video | ViT, VAEs and the rebuild-vs-generate trade-off, DiT (adaLN-Zero), SD3 (MM-DiT, logit-normal t, resolution shift), next-scale prediction (VAR), causal video autoencoders, 3D RoPE, joint clips, diffusion forcing | SD3/Flux, video models |
| 16 | Every Sense Is a Token | BPE, VQ (straight-through, commitment) and FSQ, residual vector quantization, CLIP vs SigLIP, omni models, full-duplex speech | Qwen3-TTS (the narrator) |
| **IV** | **Agency** | | |
| 17 | Reasoning | chain of thought as computation, process vs outcome rewards, RLVR, GRPO's clipped objective and KL, Dr. GRPO, DAPO, GSPO, DPO, entropy collapse, pass@k, test-time scaling, best-of-N | o-series, R1 |
| 18 | Agents and Worlds | POMDPs, long horizons, task-length doubling, world models, VLAs (π0's flow-matched chunks, FAST tokens) | Dreamer, Genie, π0 |
| 19 | Inference | exact speculative decoding, quantization (MXFP4, NVFP4, GPTQ, rotations), FlashAttention, roofline, paged KV | |
| 20 | Inside the Model | superposition, sparse autoencoders (L1, TopK, JumpReLU), transcoders and attribution graphs, crosscoders, steering, CoT faithfulness | |

## Shared code and the Chinese edition

`explainer/ai/` holds the series' instruments (chapter cards, series map, scoreboard, payoff and reference cards);
the text helpers and derivation ladder are the analysis series' (`explainer.analysis`). Chinese narration lives in
`videos/ai/aiN/narration_zh.json`, on-screen text in `videos/ai/ai_text_zh.json` (`tools/collect_text.py --check
aiN`), and terms in [`AI_ZH_GUIDE.md`](AI_ZH_GUIDE.md).
