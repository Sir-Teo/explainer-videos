# How Large Language Models Work: The Transformer, Visualized

A 37-minute, 14-chapter explainer of how a large language model produces text,
following one sentence, *"The Eiffel Tower is located in the city of"*, through
every stage of a real model. **Every number on screen comes from GPT-2 small**
(OpenAI, 2019, 124M parameters): its real tokenizer, embeddings, attention
heads, MLP neurons, position vectors and predictions. Learning is shown with a
real training run of a tiny transformer on Shakespeare. Schematics are labeled
as schematics.

```bash
python -m videos.llm.analyze                   # once: probe GPT-2, train the tiny model (~20 min, cached in .cache/llm)
python tools/build.py llm -q l                 # preview
python tools/build.py llm                      # final 1080p30 + subtitles + chapters
python tools/export_script.py llm              # regenerate SCRIPT.md from the code
python tools/check_narration.py llm            # Whisper listen test of every narration line
```

`analyze.py gpt2_family` downloads GPT-2 medium, large and XL (~9 GB) for the
scale chapter; the other runs need only GPT-2 small (~0.5 GB).

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 1 | `Hook` | An LLM outputs a probability for every next token; text is written by predict → append → repeat. Roadmap. | GPT-2's top-8 next-token distributions for 4 greedy steps ("Paris" 6.4%, then ", France."). |
| 2 | `Tokens` | Text → subword tokens → integer IDs. Why subwords. Byte-pair encoding, merge by merge. 256 + 50,000 + 1 = 50,257. | GPT-2's tokenization and IDs (" E", "iff", "el"; "Chat", "G", "PT"); vocabulary entries; BPE run on a toy corpus. |
| 3 | `Embeddings` | Lookup in W_E; vectors as points; clusters; directions carry meaning; dot product and cosine similarity. | 2D PCA of 35 real embeddings (5 tight clusters); king − man + woman → queen; Paris − France + Japan → Tokyo; cos(cat, ·). |
| 4 | `BigPicture` | Context problem ("bank"). Attention mixes, MLP processes, both *add* to the residual stream. Causal rule. | Similarity of the two "bank" vectors layer by layer: river vs. money drops 1.0 → ≈0, river vs. river stays ≥ 0.89. |
| 5 | `AttentionIdea` | Query, key, score, softmax, value, weighted sum, update. Attention pattern. Causal mask (−∞). | A real first-layer head (L0H7): scores, softmax weights (60% on "river"), full 6×6 pattern. |
| 6 | `AttentionMatrix` | softmax(QKᵀ/√d_k + M)V built term by term. Why √d_k. Multi-head, W_O, 2.4M params/layer. Three real heads. Induction → in-context learning. | All 12 heads of L5; previous-token head L4H11; first-token "sink" head L5H1; induction head L5H5 (0-based; shown 1-based on screen); P(next word) on a random 20-word list repeated: ≈0 then ≈0.8. |
| 7 | `Position` | Attention is order-blind (first layer). Learned position vectors. RoPE: rotate q, k; dot product depends on m − n; clock hands. | GPT-2's learned position embeddings: heat map (waves) and 3D PCA (a helix through 1,024 positions). |
| 8 | `MLP` | Up-project, GELU, down-project. Neurons as questions; columns as answers; MLP = Σ GELU(r·x + b) c. Facts (cartoon). Superposition. | The 3,072 real GELU activations of the 11th block's MLP (L10) at the last token (~1 in 30 firing); random-direction angle histograms in 3, 30, 768 dims. |
| 9 | `TransformerBlock` | x ← x + Attn(LN(x)); x ← x + MLP(LN(x)). LayerNorm. Stack of 12. | Exact parameter tally of GPT-2 small: 124,439,808. |
| 10 | `NextToken` | Unembedding (tied), logits, softmax (shift-invariance). Logit lens. Greedy loops. Temperature. | Real logits (≈ −95) and probabilities; logit lens: rank of "Paris" 22,947 → 1; real samples at T = 0, 0.7, 1.0, 1.6. |
| 11 | `Training` | Random init. Loss = −log p. Every position trains at once (why the mask). Gradient descent, backprop. | GPT-2's per-token losses on the sentence; a 0.8M-param char-level GPT trained from scratch: loss curve + samples at steps 0, 100, 300, 1000, 4000. |
| 12 | `Scale` | Same blueprint, bigger. Power laws. Chinchilla. Model sizes. C ≈ 6ND. Modern refinements. | P("Paris") for GPT-2 small/medium/large/XL: 6% → 69% → 60% → 93%; Kaplan et al.'s fitted law. |
| 13 | `Assistant` | Base models complete documents. Chat = transcript with role tokens. Pretraining → SFT → RLHF. RL on checkable tasks. Fluent ≠ true. | Real GPT-2 XL completions (repeats the poem request; answers, then writes the next quiz question). |
| 14 | `Outro` | The whole loop in one picture. Learned, not designed. Interpretability. | Callbacks to the real heads and logit-lens curve. |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| token boxes, raw text | light grey |
| token vectors, residual stream | blue |
| position vectors | pink |
| query q, W_Q | yellow |
| key k, W_K | teal |
| value v, W_V, attention updates | red |
| attention scores, weights, patterns, softmax | orange |
| MLP, neurons, GELU | purple |
| logits, probabilities, predictions | green |
| loss | maroon |
| layer norm | grey |

## Data (`analyze.py`)

| Run | What | Used in |
|---|---|---|
| `gpt2_small` | All probes of GPT-2 small (~15 s on CPU): tokenization, embeddings, PCA, analogies, residual streams, head patterns and scores, position embeddings, MLP activations, logit lens, logits, samples, per-token losses, parameter counts. | 1–11, 14 |
| `gpt2_family` | P("Paris") for all four GPT-2 sizes; GPT-2 XL greedy completions. | 12, 13 |
| `tiny_shakespeare` | `explainer/lm/tiny_gpt.py`: 4 layers, 4 heads, width 128, context 128, 818,048 parameters, 65 characters as tokens, 4,000 AdamW steps (batch 32) on Tiny Shakespeare (~14 min on 4 CPU cores). | 11 |

Scenes never run a model; they read the cached JSON/NPZ. Every number the
narration states is asserted against the data at render time (e.g. `assert
steps[0]["argmax"] == " Paris"`), so a regenerated dataset that disagrees with
the script fails loudly instead of silently contradicting the voice-over.

### Method notes (so the visuals can be reproduced and are not over-read)

* **GPT-2 checkpoints**: `openai-community/gpt2{,-medium,-large,-xl}` via Hugging Face `transformers`, eager attention, fp32, CPU. No BOS token is prepended.
* **Embedding clusters** (Ch. 3): plain PCA of the 35 centered input embeddings (W_E rows), top two components.
* **Analogy plane** (Ch. 3): axes are the mean of the (woman − man, queen − king, aunt − uncle) offsets and the mean of (king − man, queen − woman), orthogonalized; a linear projection, so the drawn sum is exactly the projection of king − man + woman. The nearest-token search is over all 50,257 normalized input embeddings and **excludes the three input words**; including them, the nearest token is "king" itself (cos 0.78 vs 0.71 for "queen"), as is typical for this test (Nissim et al. 2020).
* **"bank" similarity** (Ch. 4): cosine similarity of the residual-stream vectors at "bank" after each block, after subtracting each layer's mean residual vector (measured on a fixed reference paragraph, skipping position 0). Without centering, GPT-2's few huge shared dimensions dominate every cosine (Ethayarajh 2019; Timkey & van Schijndel 2021); the qualitative result (different meanings diverge, same meaning stays close) holds either way. Sentences are chosen so "bank" sits at the same position in all three.
* **Attention heads**: the layer-0 "bank" head (L0H7) was found by searching for heads where "bank" attends to "river"; L4H11 and L5H5 are the strongest previous-token and induction heads by the scores in `gpt2.head_scores` (they match the heads reported by Wang et al. 2022). Layer and head numbers on screen are 1-based for a general audience; in the usual 0-based notation, L4H11 is shown as "layer 5, head 12".
* **First-token fraction** (Ch. 6): fraction of the 144 heads whose mean attention to position 0 (from positions ≥ 3) exceeds 0.5 on the example sentence: 68%.
* **Position heat map** (Ch. 7): every 4th position, the 64 dimensions with the largest variance across positions (mean removed), ordered by dominant frequency then phase. The helix is PCA of all 1,024 position vectors (top 3 components explain 90% of the variance).
* **MLP activations** (Ch. 8): GELU outputs of block 11 (0-based layer 10), last position; "firing strongly" means > 0.5.
* **Logit lens** (Ch. 10): residual stream after k blocks → final LayerNorm → tied unembedding.
* **Samples** (Ch. 10): `gpt2.sample`, torch generator seed 3 for every temperature; greedy for T = 0.

## Fact-check notes and sources

* **Transformer**: Vaswani et al., *Attention Is All You Need*, NeurIPS 2017 (Google). Scaled dot-product attention softmax(QKᵀ/√d_k)V; the √d_k motivation (large dot products push softmax into regions with tiny gradients) is theirs.
* **GPT-2**: Radford et al., *Language Models are Unsupervised Multitask Learners*, 2019. WebText: ~40 GB of text from ~8M web pages. Sizes 124M/355M/774M/1.5B; 12/24/36/48 layers; widths 768/1024/1280/1600; context 1,024. BPE vocabulary of 50,257 (256 byte tokens + 50,000 merges + `<|endoftext|>`). Parameter counts on screen are measured from the checkpoints.
* **BPE**: Sennrich, Haddow & Birch, *Neural Machine Translation of Rare Words with Subword Units*, ACL 2016.
* **Rotary embeddings**: Su et al., *RoFormer*, 2021. Used by Llama 3 (Meta 2024, "RoPE (θ = 500,000)").
* **Induction heads / in-context learning**: Elhage et al., *A Mathematical Framework for Transformer Circuits*, 2021; Olsson et al., *In-context Learning and Induction Heads*, 2022. Previous-token and induction heads in GPT-2 small: Wang et al., *Interpretability in the Wild*, 2022.
* **Attention sinks**: Xiao et al., *Efficient Streaming Language Models with Attention Sinks*, 2023. The video hedges ("seems to be a resting place").
* **MLPs as key-value memories / factual recall**: Geva et al., *Transformer Feed-Forward Layers Are Key-Value Memories*, EMNLP 2021; Meng et al., *Locating and Editing Factual Associations in GPT* (ROME), NeurIPS 2022. The Eiffel-Tower neuron is explicitly a cartoon.
* **Superposition**: Elhage et al., *Toy Models of Superposition*, 2022. Near-orthogonality of random high-dimensional vectors (std of the angle ≈ 1/√d rad, ≈ 2° at d = 768) is computed on screen.
* **Logit lens**: nostalgebraist, *interpreting GPT: the logit lens*, 2020.
* **Scaling laws**: Kaplan et al., *Scaling Laws for Neural Language Models*, 2020, arXiv:2001.08361. Eq. 1.1: L(N) = (N_c/N)^α_N with α_N ∼ 0.076, N_c ∼ 8.8 × 10¹³ non-embedding parameters; trends "spanning more than seven orders of magnitude"; "C ≈ 6N floating point operators per training token". The plotted line is this fitted law, not new data.
* **Chinchilla**: Hoffmann et al., *Training Compute-Optimal Large Language Models*, 2022 (≈20 tokens per parameter; 70B model on 1.4T tokens).
* **GPT-3**: Brown et al., *Language Models are Few-Shot Learners*, 2020, Table 2.1: 175B, 96 layers, d_model 12,288, 96 heads, context 2,048, "trained for a total of 300 billion tokens"; Table D.1: 3.14 × 10²³ training FLOPs (6 × 174.6B × 300B).
* **Llama 3.1 405B**: Llama Team, Meta, *The Llama 3 Herd of Models*, 2024, arXiv:2407.21783: "pre-trained using 3.8 × 10²⁵ FLOPs", "405B trainable parameters on 15.6T text tokens", "126 layers, a token representation dimension of 16,384, and 128 attention heads", RoPE.
* **InstructGPT**: Ouyang et al., *Training language models to follow instructions with human feedback*, NeurIPS 2022: "outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters". Pipeline: SFT on demonstrations → reward model on rankings → PPO.
* **Reasoning models**: OpenAI o1 (Sep 2024); DeepSeek-AI, *DeepSeek-R1*, Jan 2025 (RL with rule-based, verifiable rewards). Named on screen only as examples.
* **Modern refinements** (Ch. 12): RMSNorm (Zhang & Sennrich 2019), SwiGLU (Shazeer 2020), grouped-query attention (Ainslie et al. 2023), mixture of experts (Shazeer et al. 2017; Fedus et al. 2021). Context windows of hundreds of thousands of tokens (e.g. 128K for Llama 3.1; longer for some commercial models).
* **Tiny Shakespeare**: `karpathy/char-rnn` `data/tinyshakespeare/input.txt` (1,115,394 characters of Shakespeare's plays, public domain).

The video describes the field **as of October 2026** only in general terms
(frontier labs rarely publish sizes; context windows of hundreds of thousands
of tokens). No claims are made about undisclosed models.
