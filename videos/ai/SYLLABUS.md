# AI, Built: the expanded syllabus (plan of record, draft 2)

Goal: a university-level course in video, **as comprehensive and as close to the frontier as possible**, in English
and Chinese to the standard of *Analysis, Built*, rendering on macOS and Linux. Each part runs **30–60 minutes**,
depending on how much its content needs. Currently the twenty parts total about 4.9 hours. This plan totals about 23
hours across 28 parts.

## 1. The standard every part meets

**A chapter is a lecture segment of 3–5 minutes.** It runs in this order:

1. A motivating question or failure.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("Jensen", "union bound", "complete the square").
4. A computed experiment that checks the result.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**
- An objectives card.
- Theorem and definition cards.
- A problem set (4–6 problems, about 90 s on screen; full solutions in the part's README, English and Chinese).
- A reference card listing textbooks, the classic papers, and the frontier papers.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources (arXiv, technical
reports, model cards) up to the writing date. Anything newer than mid-2026 is verified against its primary report
before it goes on screen. Example: secondary sources report DeepSeek-V4's compressed sparse attention and Kimi K3; neither
is used until checked.

**Numbers are real.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/aiN/`. Published numbers are cited.
  Schematics are labelled `schematic`, made-up examples `illustrative`.
- CPU budget: ≤ 2 h per part by default. Named exceptions (AlphaZero, the scaling sweep, the transformers) get
  ≤ 12 h, are resumable, and are seeded.
- Scene assertions use tolerances, not exact equality, so macOS (Accelerate) and Linux (OpenBLAS) builds agree.

**Visual standard** (3Blue1Brown manner, `explainer/ai/viz.py`). Continuity over cuts, in-place derivations, colour as
meaning, a narrating camera, and live quantities. New instruments:

| Instrument | What it shows |
|---|---|
| `DerivationBoard` | stacked steps with reasons |
| `theorem_card` / `definition_card` / `objectives_card` / `problem_set` | the lecture's set pieces |
| `ParticleFlow` | thousands of points under a vector field or SDE, with density underneath |
| `ComputeGraph` | values forward, gradients back, as glowing pulses |
| `FoldPlane` | ReLU layers folding the input plane |
| `TrainingReplay` | a curve and its model's outputs scrubbed through checkpoints together |
| `SearchTree` | MCTS / beam / minimax trees growing, visit counts as branch weight |
| `Board` | Go, Connect Four, gridworld, with policy and value heatmaps |
| `ShardGrid` | tensors split across devices, collectives as moving blocks |
| `Roofline` | kernels as dots moving on the roofline |
| `Hypersphere` | embeddings on S², alignment/uniformity |
| 3D camera tours | surfaces, densities in time, receptive-field cones |

**Bilingual standard (as *Analysis, Built*).**
- Every narration line has its `narration_zh.json` entry.
- Every on-screen string is in `ai_text_zh.json`, and `tools/collect_text.py --check aiN` is clean.
- The glossary in `AI_ZH_GUIDE.md` is extended for every new term.
- `zh_follow_numbers.py` and `check_narration.py` (listen test) are run in both languages.
- Chinese TeX: xelatex + xeCJK with Fandol, which TeX Live ships on both platforms.

**macOS and Linux.**
- `tools/tts_server.py` gains a PyTorch engine (`qwen-tts`, CUDA, or CPU as a slow fallback) behind the same HTTP API.
  Linux then narrates with the same Qwen3-TTS voice as the MLX engine on Apple Silicon. The Colab fleet stays.
- The README gets an apt setup next to the brew one.
- A new `tools/smoke.py` renders every part's first scene at `-q l` (silent, en + zh) on the machine it runs on.

**Gates per part:**
- `tools/lecture_length.py` (new): an estimate before render, the measured length after; fails under 30 min.
- `contact_sheet.py`, `dead_air.py`, `collect_text.py --check`, `check_narration.py`.

## 2. The series, re-cut from 20 parts to 28

| New | Part | Was |
|---|---|---|
| **I** | **Foundations** | |
| 1 | The Guessing Game | 1 |
| 2 | Vectors That Mean Things | 2 |
| 3 | Change | 3 |
| 4 | Randomness in Motion | 4 |
| **II** | **Learning** | |
| 5 | Classical ML | 5 |
| 6 | Statistical ML | 6 |
| 7 | Fitting and Generalizing | 7 |
| 8 | Networks | 8 |
| 9 | **Seeing and Remembering** (CNNs, RNNs, the first attention) | new |
| 10 | Going Downhill | 9 |
| 11 | The Mathematics of Scale | 10 |
| **III** | **The Transformer at Scale** | |
| 12 | Attention as Geometry | 11 |
| 13 | Memory | 12 |
| 14 | Sparsity | 13 |
| 15 | **Pretraining at Scale** (data, parallelism, precision, stability) | new |
| 16 | Inference | 19 |
| **IV** | **Generation and Perception** | |
| 17 | **Four Ways to Generate** (autoregressive, VAE, GAN, flows, energy) | new |
| 18 | Diffusion and Flow | 14 |
| 19 | Images, Video and 3D | 15 |
| 20 | Every Sense Is a Token | 16 |
| 21 | **Learning Without Labels** (self-supervised learning) | new |
| 22 | **Symmetry and Science** (GNNs, equivariance, AlphaFold, weather, maths) | new |
| **V** | **Agency** | |
| 23 | **Reinforcement Learning, from Bellman to AlphaZero** | new |
| 24 | **Post-Training and Alignment** | new |
| 25 | Reasoning | 17 |
| 26 | Agents and Worlds | 18 |
| **Finale** | | |
| 27 | Inside the Model | 20 |
| 28 | **Can We Trust It?** (evaluation, safety, open problems) | new |

**The scoreboard** gains rows, all on the same passage and the same thirty novels:
- Part 6: an ∞-gram (suffix array).
- Part 9: a character LSTM.
- Part 12: our transformer.
- Part 13: a gated-delta hybrid and a kNN-LM.
- Part 14: a small MoE.
- Part 15: a model trained with the full recipe.
- Part 18: a masked-diffusion LM (an ELBO bound).

**The renumbering** happens once, in Phase 0:
- `git mv` the directories.
- `ACTS` / `PARTS` / timeline entries in `explainer/ai`.
- Part references in narration, en and zh.
- Scoreboard part labels, `ai_upload.json`, README, CLAUDE.md.

## 3. Part by part

Length targets are estimates; content decides.

### Part 1 · The Guessing Game (~50 min; densify the existing 43)
1. Probability and the chain rule.
2. Surprise; entropy's axioms (Shannon's uniqueness theorem, sketched).
3. Gibbs' inequality via Jensen.
4. Kraft–McMillan, proved on the binary tree.
5. Huffman optimality by an exchange argument.
6. The AEP and typical sets: the source coding theorem.
7. Cross-entropy and KL: asymmetry, forward vs reverse KL (mode-covering vs mode-seeking). Comes back in VI,
   distillation and RLHF.
8. Arithmetic coding with its 2-bit overhead and finite precision.
9. Counting models and Laplace smoothing.
10. Shannon 1951.
11. Maximum likelihood = minimum KL; the softmax gradient p − y.
12. Mutual information and the data-processing inequality.
13. Bits per character vs per token.
14. The scoreboard.

*Frontier:* "language modeling is compression" (Delétang et al. 2024); LLMs as compressors vs gzip/xz.
*Visuals:* the typical set shrinking inside sequence space; the arithmetic coder's interval zooming; forward vs
reverse KL fits sliding over a bimodal p.

### Part 2 · Vectors That Mean Things (~50)
1. Vectors, inner products, Cauchy–Schwarz.
2. Tensors and einsum (the notation attention uses).
3. Matrices as maps; projection and Gram–Schmidt; P = A(AᵀA)⁻¹Aᵀ.
4. Eigenvalues; the spectral theorem (proof sketch); the Rayleigh quotient; power iteration, run live.
5. SVD derived from AᵀA; Eckart–Young.
6. Spectral vs Frobenius norm; condition number (Muon needs the spectral norm).
7. Random matrices: Marchenko–Pastur vs the heavy-tailed spectra of trained weights; low-rank gradients (GaLore).
8. Word vectors from counting; SGNS factorizes shifted PMI (Levy and Goldberg 2014), checked.
9. High dimensions: shell concentration, near-orthogonality with variance 1/d derived.
10. Johnson–Lindenstrauss, proved (Gaussian projection, χ² tail, union bound).
11. GPT-2's embedding geometry and anisotropy.

*Visuals:* circle → ellipse in three SVD stages; an image mosaic sharpening rank by rank; the MP law vs a trained
layer's spectrum.

### Part 3 · Change (~50)
1. Derivative as best linear approximation.
2. Gradient as steepest ascent (Cauchy–Schwarz).
3. Jacobians of real layers: softmax diag(p) − ppᵀ, layer norm, matmul.
4. JVPs and VJPs; forward vs reverse cost, counted.
5. Backprop through a two-layer MLP by hand (dW = δxᵀ).
6. The series' autodiff library: topological sort, the tape.
7. Numerics: float formats, ulp, cancellation, the log-sum-exp trick; gradient checking's V-curve (truncation vs
   roundoff).
8. Memory: checkpointing at √n.
9. Curvature: Hessian, Newton, Hessian–vector products (Pearlmutter).
10. GD on quadratics: rate from the condition number; saddles.
11. Constrained optimization: Lagrange multipliers, KKT, convex duality. SVMs, max-entropy and RL's closed forms
    use it.
12. Implicit differentiation (implicit function theorem; deep equilibrium models, meta-learning).

*Visuals:* `ComputeGraph`; tangent planes on 3D surfaces; descent zig-zagging in narrow valleys; the Lagrange
picture (gradients parallel at the constrained optimum).

### Part 4 · Randomness in Motion (~55)
1. The CLT by repeated convolution.
2. Multivariate Gaussians; conditioning via the Schur complement.
3. MLE bias; Fisher information and Cramér–Rao.
4. Bayes: Beta–binomial live; MAP as regularization.
5. Exponential families and maximum entropy (softmax and Gibbs as max-ent).
6. Concentration: Markov, Chebyshev, Chernoff/Hoeffding (Part 7 uses them).
7. Sampling: inverse CDF, rejection, Box–Muller; the Gumbel-max trick and Gumbel-softmax.
8. LLM decoding: temperature, top-k, top-p, min-p.
9. Markov chains: stationary distributions as eigenvectors, detailed balance, spectral gap.
10. Monte Carlo at 1/√n; importance sampling and ESS; the score-function estimator (REINFORCE and evolution
    strategies come back).
11. Metropolis–Hastings from detailed balance; Langevin dynamics.
12. Brownian motion as a scaling limit; quadratic variation; Itô's lemma.
13. SDEs, Euler–Maruyama; Fokker–Planck derived; Ornstein–Uhlenbeck (Part 18's forward process).

*Visuals:* `ParticleFlow` Langevin with its density evolving in 3D; the top-p cut sliding over a real next-token
distribution.

### Part 5 · Classical ML (~55)
1. Least squares as projection (3D column space); Gauss–Markov; pseudoinverse and QR.
2. Ridge as SVD shrinkage σ²/(σ²+λ); lasso via soft-thresholding and its computed path; elastic net.
3. Logistic regression: convexity (XᵀSX), Newton/IRLS; calibration.
4. Naive Bayes vs logistic (generative vs discriminative).
5. Fisher's LDA as a generalized eigenproblem.
6. k-NN and the Cover–Hart bound; the curse of dimensionality.
7. Kernels: the trick, Mercer, RBF feature space, the representer theorem.
8. SVM: margin, hinge, the dual via KKT, support vectors.
9. Trees: Gini/entropy splits.
10. Bagging's ρσ² + (1−ρ)σ²/B and random forests.
11. Boosting: AdaBoost as exponential loss; gradient boosting with XGBoost's second-order split gain.
12. Metrics: ROC/AUC, precision-recall, cross-validation; the authorship contest.

*Visuals:* a kernel lifting circles to 3D, where a plane separates them; decision boundaries morphing with k and C.

### Part 6 · Statistical ML (~55)
1. PCA two ways (max variance, min reconstruction) and via SVD; probabilistic PCA.
2. ICA (the cocktail party).
3. Mixtures and EM: the Jensen bound, monotonicity proved; k-means as hard EM.
4. HMMs: forward, Viterbi lattice, Baum–Welch (CTC in Part 20 reuses the forward algorithm).
5. Graphical models: d-separation, factor graphs, belief propagation.
6. Gaussian processes: posterior from Gaussian conditioning, marginal-likelihood hyperparameters.
7. Variational inference: the ELBO identity, mean-field CAVI, reparameterization, amortization (VAEs come back).
8. Bayesian Occam's razor.
9. Kneser–Ney from Good–Turing and absolute discounting.
10. ∞-gram (infini-gram, suffix arrays) on the thirty novels: a new scoreboard row.

*Visuals:* EM ellipses breathing; Viterbi paths lighting up; a GP band shrinking as points land.

### Part 7 · Fitting and Generalizing (~50)
1. Risk, empirical risk, Bayes risk.
2. Bias–variance, derived.
3. Hoeffding (simulated); finite classes by union bound.
4. Growth function, Sauer–Shelah, the VC bound.
5. Rademacher complexity; a bound for norm-bounded linear models; margins.
6. PAC-Bayes (KL from Part 1); compression and stability bounds.
7. Random labels (Zhang et al.).
8. Implicit bias: GD finds the min-norm interpolant (proof), max-margin for logistic (Soudry et al.).
9. Double descent explained by 1/σ at the interpolation threshold; sample- and epoch-wise; benign overfitting.
10. Flat minima and the sharpness debate.
11. Distribution shift: covariate shift, importance weighting.
12. Memorization in LLMs (extractable training data).

*Visuals:* shattering animations; Hoeffding histograms tightening; the singular spectrum sliding to zero at the
peak.

### Part 8 · Networks (~50)
1. Perceptron and Novikoff's convergence proof.
2. Universal approximation built from ReLU bumps; Barron's dimension-free rate.
3. Depth separation by sawtooth composition (2^L pieces); linear regions counted.
4. Xavier/He derived; mean-field signal propagation, the edge of chaos; gradients through 50 layers.
5. Residuals; BatchNorm, LayerNorm, RMSNorm Jacobians; pre- vs post-norm.
6. Activations: GELU, SiLU, SwiGLU gating.
7. The modern block.
8. KANs and the Kolmogorov–Arnold theorem (the 2024 debate).
9. Bengio 2003: the neural n-gram, scoreboard row.

*Visuals:* `FoldPlane`; activation histograms as a 3D ridge plot through depth.

### Part 9 · Seeing and Remembering (new, ~55)
1. Convolution as weight sharing; translation equivariance proved.
2. Receptive-field arithmetic, stride, pooling.
3. LeNet → AlexNet → VGG → ResNet; ImageNet error by year (cited).
4. What filters learn (our CNN on the glyph images).
5. Adversarial examples: FGSM from linearity.
6. Depthwise and dilated convs, ConvNeXt.
7. RNNs and BPTT; vanishing gradients via products of Jacobians.
8. LSTM (the constant error carousel); GRU.
9. Seq2seq, teacher forcing, beam search.
10. Bahdanau attention (2014): the birth of attention.
11. A char-LSTM on the thirty novels: scoreboard row.
12. RNNs return: minLSTM/xLSTM and parallel scans, the bridge to Part 13.

*Visuals:* a kernel sweeping out a feature map; receptive-field cones in 3D; the LSTM cell as a conveyor belt;
gradient norm decaying back through time.

### Part 10 · Going Downhill (~55)
1. GD rates for L-smooth and strongly convex losses, derived.
2. SGD noise; the SDE view with temperature η/B; linear scaling and the critical batch (gradient noise scale).
3. Edge of stability (sharpness measured at 2/η).
4. Heavy ball and Nesterov on quadratics.
5. Adam derived (bias correction, sign limit); AdamW and why L2 ≠ weight decay; Lion.
6. Natural gradient and the Fisher; K-FAC.
7. Shampoo and SOAP.
8. Muon: spectral steepest descent, Newton–Schulz as a polynomial map on singular values, MuonClip/QK-clip (Kimi K2).
9. Schedules: warmup, cosine, WSD and the river valley, schedule-free.
10. Clipping, loss spikes, weight decay as norm equilibrium, EMA.

*Visuals:* optimizers racing on one 3D landscape; singular values pushed to 1 by Newton–Schulz.

### Part 11 · The Mathematics of Scale (~55)
1. NTK and lazy training: why it learns no features.
2. μP derived from Θ(1) updates; coordinate checks; width transfer, computed; depth transfer (CompleteP).
3. Scaling laws; our own CPU sweep, fit.
4. Chinchilla's L(N, D); compute-optimal by Lagrange with C ≈ 6ND.
5. Over-training for inference.
6. Data-constrained scaling and repetition.
7. MoE and precision scaling laws.
8. Why power laws (data-manifold and quanta models).
9. Emergence vs metric artifacts.
10. Grokking and its Fourier circuit.

*Visuals:* iso-FLOP valleys in 3D; the Fourier spectrum of a grokked embedding lighting up.

### Part 12 · Attention as Geometry (~55)
1. Attention as Nadaraya–Watson; modern Hopfield networks = attention.
2. √d from variance.
3. Heads as low-rank maps; causal masks.
4. Encoder, decoder, encoder–decoder (BERT, GPT, T5).
5. FLOP and parameter count per block.
6. Positions: sinusoidal, ALiBi, RoPE with relative position proved, NoPE.
7. Context extension: PI, NTK-aware, YaRN; log-n scaling.
8. Sinks and sink logits; gated attention; differential attention.
9. QK-norm and soft caps.
10. Induction heads measured in our transformer (K-composition); ICL as gradient descent (computed).
11. RASP and what a fixed-depth transformer can compute (TC⁰).
12. Scoreboard row.

### Part 13 · Memory (~55)
1. KV-cache arithmetic; MQA/GQA; MLA (absorption, decoupled RoPE).
2. Cache eviction (StreamingLLM, H2O).
3. Linear attention as an RNN.
4. The delta rule (online least squares, Householder) and gated delta; WY/UT chunkwise.
5. SSMs: HiPPO/S4, ZOH discretization, Mamba selectivity, Mamba-2 duality, newer variants after verification.
6. RWKV-7, mLSTM.
7. Titans and test-time training.
8. MQAR recall test (computed).
9. Hybrids: Jamba, Nemotron-H, Qwen3-Next, Kimi Linear.
10. Long-context evaluation (needle, RULER).
11. Retrieval as memory: dense retrieval, the kNN-LM on the novels (scoreboard row).

*Visuals:* the associative scan; the memory matrix written and read.

### Part 14 · Sparsity (~50)
1. Top-k gating and the router's gradient.
2. Switch balancing loss derived; DeepSeekMoE fine-grained and shared experts.
3. Aux-loss-free bias; sigmoid routing.
4. Capacity factor; expert parallelism and all-to-all cost; active-parameter accounting; upcycling.
5. Specialization measured on our MoE (scoreboard row).
6. Mixture-of-depths.
7. Sparse attention: sliding window, NSA, MoBA, DSA's lightning indexer.
8. Lottery tickets, pruning, 2:4 sparsity, activation sparsity.

### Part 15 · Pretraining at Scale (new, ~55)
1. Anatomy of a frontier run (cited reports).
2. Data: extraction, language ID, MinHash-LSH dedup with the collision probability derived, quality classifiers
   (FineWeb-Edu), contamination.
3. Mixtures (DoReMi, RegMix); synthetic data and rephrasing; model collapse.
4. Objectives: causal LM, MLM, span corruption, FIM.
5. Annealing and mid-training; long-context extension.
6. Accounting: 6ND; memory (weights, grads, Adam states, activations).
7. Data parallel: ring all-reduce derived (bandwidth-optimal); ZeRO 1/2/3 and FSDP.
8. Tensor parallel: Megatron's column/row split.
9. Pipeline: bubble (p−1)/(m+p−1), 1F1B, DualPipe.
10. Context parallel (ring attention); expert parallel; MFU.
11. Precision: bf16 vs fp16 with loss scaling; FP8 with fine-grained scaling (DeepSeek-V3); MXFP8/NVFP4 training.
12. Stability: z-loss, QK-norm.
13. Multi-token prediction; fault tolerance at 16k GPUs (Llama 3 statistics).
14. Our full-recipe model (scoreboard row).

*Visuals:* `ShardGrid` collectives; a pipeline Gantt chart filling in.

### Part 16 · Inference (~55)
1. Roofline derived; arithmetic intensity of GEMV vs GEMM; prefill vs decode.
2. Continuous batching; paged KV; prefix caching; disaggregated serving.
3. Speculative decoding: exactness proved, the expected-accepted formula; EAGLE and MTP drafters.
4. Quantization: Δ²/12, outliers, SmoothQuant, GPTQ from Optimal Brain Surgeon, AWQ, rotations (QuaRot, SpinQuant).
5. MXFP4/NVFP4 bit layouts (gpt-oss).
6. KV quantization.
7. FlashAttention 1–3: online softmax, tiling, IO complexity; FlashDecoding.
8. Constrained decoding via automaton masks.

### Part 17 · Four Ways to Generate (new, ~55)
1. The generative problem.
2. Autoregressive (PixelCNN).
3. VAEs: ELBO, posterior collapse, β-VAE.
4. GANs: the optimal discriminator → Jensen–Shannon; mode collapse; non-saturating loss; GAN dynamics as a rotating
   vector field.
5. WGAN via Kantorovich–Rubinstein; gradient penalty; StyleGAN.
6. Normalizing flows: change of variables, coupling layers, triangular log-det.
7. Neural ODEs and continuous flows (trace, Hutchinson).
8. Energy-based models: Hopfield and Boltzmann machines (the 2024 Nobel), contrastive divergence, Langevin
   sampling → the score.
9. Evaluation: FID derived as Fréchet distance between Gaussians; precision/recall for generators.

*Visuals:* flows warping a grid; the GAN two-player field spiralling.

### Part 18 · Diffusion and Flow (~60)
1. Forward process in closed form; ELBO → ε-prediction; Tweedie.
2. Denoising score matching, proved.
3. Reverse SDE and the probability-flow ODE; DDIM; SNR schedules.
4. EDM: preconditioning, Heun; DPM-Solver as an exponential integrator.
5. Optimal transport and Benamou–Brenier; flow matching (marginal-field theorem); stochastic interpolants.
6. Rectified flow and reflow.
7. Distillation: progressive, consistency models (sCM), DMD; MeanFlow, shortcut models.
8. Guidance: classifier via Bayes, CFG, autoguidance.
9. Discrete diffusion: D3PM; masked diffusion's ELBO as weighted cross-entropy (derived).
10. LLaDA, block diffusion, fast diffusion LMs.
11. A masked-diffusion LM on the novels (scoreboard row, as a bound).

### Part 19 · Images, Video and 3D (~55)
1. ViT.
2. Latent spaces: KL-f8, deep-compression AEs, REPA and representation autoencoders.
3. U-Net vs DiT (adaLN-Zero).
4. SD3 MM-DiT; logit-normal t; the resolution shift derived; Flux.
5. Autoregressive images: VQGAN, MaskGIT, VAR next-scale, Infinity.
6. Unified models (Transfusion, Janus, BAGEL).
7. Video: causal 3D VAE, 3D RoPE, joint image–video training, diffusion forcing, self-forcing, real-time
   autoregressive video.
8. 3D: NeRF's volume-rendering integral derived; 3D Gaussian splatting (covariance projection).

### Part 20 · Every Sense Is a Token (~55)
1. BPE (merges as compression); unigram LM.
2. Byte-level and tokenizer-free: BLT, entropy patching.
3. Tokenization and bits per character.
4. VQ: straight-through, commitment, collapse, EMA; FSQ/LFQ; RVQ.
5. Audio: Nyquist derived, STFT, mel; codecs (SoundStream, EnCodec, Mimi); semantic vs acoustic tokens.
6. ASR: Whisper; CTC derived (the HMM forward algorithm).
7. TTS: Qwen3-TTS, the narrator.
8. Full duplex (Moshi).
9. CLIP: InfoNCE as an MI bound; SigLIP.
10. VLMs: connectors, dynamic resolution, M-RoPE.
11. Omni models (Thinker–Talker).

### Part 21 · Learning Without Labels (new, ~45)
1. Pretext tasks.
2. Contrastive learning: SimCLR, MoCo, temperature; alignment and uniformity on the hypersphere.
3. Non-contrastive: BYOL, SimSiam (why stop-gradient prevents collapse), Barlow Twins, VICReg.
4. Self-distillation: DINO centering and sharpening, DINOv2/v3.
5. Masked modelling: MAE, BEiT.
6. JEPA: I-JEPA, V-JEPA 2.
7. Text embeddings and Matryoshka; linear probes; CKA.
8. The platonic representation hypothesis.

*Computed on the glyph images:* collapse shown, then prevented.

### Part 22 · Symmetry and Science (new, ~55)
1. Groups; invariance vs equivariance; Deep Sets' theorem.
2. GNNs: message passing, expressivity = the WL test, over-smoothing, graph attention.
3. E(3)-equivariance (EGNN, spherical harmonics, sketched).
4. AlphaFold 2: MSA, Evoformer triangle updates, IPA on frames, FAPE, recycling.
5. AlphaFold 3: Pairformer plus atom diffusion.
6. Design: RFdiffusion, ProteinMPNN.
7. Weather: GraphCast's mesh GNN, GenCast ensembles.
8. Materials (GNoME); neural operators (FNO).
9. Mathematics: AlphaGeometry, AlphaProof in Lean, AlphaEvolve, olympiad-level LLM proofs.

*Computed:* the equivariance check, WL on graphs, a GNN on synthetic graphs. Systems' numbers are cited.

### Part 23 · Reinforcement Learning, from Bellman to AlphaZero (new, ~60; the pilot)
1. The RL problem: MDPs, return, discount.
2. Bandits: ε-greedy, UCB from Hoeffding, the regret lower bound, Thompson sampling.
3. Bellman equations; the γ-contraction proof; value and policy iteration; the policy-improvement theorem.
4. Monte Carlo vs TD(0); TD(λ) and eligibility traces; TD-Gammon (1992).
5. SARSA and Q-learning; off-policy; the deadly triad.
6. DQN: replay, target nets, Atari.
7. Double DQN: the max-of-noisy-estimates bias proved; dueling, distributional (C51), Rainbow.
8. Policy gradients: REINFORCE, baselines, actor–critic, GAE derived; TRPO, PPO's clip (Parts 24–25 build on
   it); maximum-entropy RL (SAC).
9. Search: minimax, alpha–beta, Deep Blue; MCTS and UCT.
10. AlphaGo (2016): SL policy, RL policy, value net, rollouts, PUCT; move 37 (prior ≈ 1/10,000, cited).
11. AlphaGo Zero and AlphaZero: MCTS as a policy-improvement operator; the loss (z − v)² − πᵀlog p + c‖θ‖²;
    tabula rasa Go, chess, shogi.
12. MuZero: learned representation, dynamics and prediction; value-equivalent models; EfficientZero; Gumbel MuZero.
13. Imperfect information: regret matching and CFR (Libratus, Pluribus); AlphaStar's league; OpenAI Five.
14. Adversarial policies that beat superhuman KataGo.
15. Games for algorithms: AlphaTensor, AlphaDev.
16. From games to language (Parts 24–25).

*Computed:*
- gridworld DP/TD;
- bandit regret;
- the double-Q bias;
- PPO on a classic control task;
- **AlphaZero on Connect Four**, trained on CPU and graded move by move against a perfect solver;
- Elo across self-play generations by round-robin.

*Visuals:* `SearchTree` growing with visit counts as branch weight; `Board` heatmaps; value diffusing across a
gridworld; Bellman contraction as shrinking balls.

### Part 24 · Post-Training and Alignment (new, ~55)
1. SFT and chat templates.
2. LoRA (intrinsic dimension; QLoRA, DoRA); forgetting.
3. Reward models: Bradley–Terry.
4. RLHF with a KL penalty; the closed form π* ∝ π_ref·e^{r/β} derived.
5. Over-optimization: Goodhart and reward-model scaling laws.
6. DPO derived; IPO, KTO, SimPO; online vs offline.
7. Constitutional AI and RLAIF.
8. Distillation: logit, sequence, on-policy with reverse KL (Part 1's KL).
9. Model merging: task arithmetic, TIES, soups, linear mode connectivity.
10. Sycophancy, refusals, jailbreaks; emergent misalignment; persona vectors.

*Computed:* DPO and LoRA on our transformer over the novels; a merging experiment.

### Part 25 · Reasoning (~60)
1. CoT as computation: TC⁰ vs serial steps, parity.
2. Self-consistency.
3. ORMs vs PRMs.
4. RLVR; GRPO derived; the k1/k3 KL estimators.
5. Variants: Dr. GRPO, DAPO, GSPO, CISPO.
6. Entropy collapse and clip-higher; length and overthinking.
7. pass@k's unbiased estimator; does RL widen the reasoning boundary? (the 2025 debate).
8. Test-time scaling: parallel vs sequential, budget forcing.
9. Best-of-N's KL ≤ log N − (N−1)/N.
10. Tree search for LLMs.
11. Latent reasoning (Coconut); tiny recursive models (HRM, TRM).
12. Formal maths; ARC-AGI.

*Computed:* GRPO on a tiny arithmetic transformer on CPU.

### Part 26 · Agents and Worlds (~60)
1. POMDPs and belief.
2. The agent loop: ReAct, tools, function calling, memory, multi-agent.
3. Long horizons: compounding error; the METR horizon doubling (cited data, fitted); SWE-bench.
4. Imitation learning: BC's O(T²ε) vs DAgger.
5. World models: Ha and Schmidhuber, Dreamer (RSSM, KL balancing, symlog), Genie 1–3, JEPA world models.
6. VLAs: RT-2, OpenVLA, π0's flow-matched action expert, FAST tokens, π0.5.
7. Sim-to-real.
8. Computer use.

*Computed:* Dreamer-lite on a tiny environment; DAgger vs BC; FAST's DCT.

### Part 27 · Inside the Model (~55)
1. Probing and its caveats; logit and tuned lens.
2. Activation and path patching.
3. Superposition: the phase diagram, computed.
4. SAEs: L1 shrinkage, TopK, JumpReLU, Matryoshka; dead latents, splitting, absorption.
5. Transcoders and cross-layer transcoders; attribution graphs.
6. Crosscoders and model diffing.
7. Steering.
8. Our transformer's induction circuit, end to end; grokking, mechanistically.
9. CoT faithfulness.

### Part 28 · Can We Trust It? (new, ~50; the finale)
1. Evaluation science: contamination, bootstrap CIs and paired tests (on our scoreboard).
2. Bradley–Terry/Elo arenas; item response theory; LLM-as-judge biases.
3. Forecasting capabilities.
4. Reward hacking and specification gaming.
5. Scalable oversight (debate, weak-to-strong, computed small).
6. Alignment faking and sandbagging evidence.
7. CoT monitorability; AI control protocols.
8. Dangerous-capability evals; adversarial robustness.
9. Privacy: extraction, DP-SGD.
10. Open problems.
11. The final scoreboard, and back to Shannon.

## 4. Phases

0. **Infrastructure:**
   - the renumbering to 28;
   - the new instruments and lecture cards;
   - `lecture_length.py` and `smoke.py`;
   - the PyTorch TTS engine;
   - Linux setup docs;
   - a silent en + zh smoke render of every part on Linux (this container).
1. **Pilot: Part 23 (RL, from Bellman to AlphaZero).** It's new, so there's no legacy to fight, and it exercises
   every new instrument. Delivered in en + zh, with previews and contact sheets. **Review with the user**, then lock
   the standard.
2. **Roll-out in series order, Parts 1 → 28.** Each part goes through:
   - the frontier sweep;
   - locking the chapter list;
   - `compute.py`;
   - English scenes, then QA gates;
   - Chinese narration and text, then QA gates;
   - commit and push.

Scale: about 23 hours of video, about 110–130k narration words per language, and roughly 4–6k lines of scene code
per part. Expect one part per one or two long sessions.
