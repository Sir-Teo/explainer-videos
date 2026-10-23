# AI, Built — Part 13: Attention as Geometry

Part 13 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first of Act III, *Engines*. What attention computes, as an average and
as a memory; why the √d; heads as low-rank maps, masks, and what a block costs; our own transformer, trained and
replayed; four ways to tell it where things are, and how to stretch them past the training length; the sinks, gates
and norms inside today's softmax; and what heads learn to do (copy, take a step of gradient descent, run a program),
and what no fixed depth can. Every model here is trained by `compute.py` (PyTorch, CPU), several times over where a
comparison is made; the series' own small transformer joins the scoreboard.

* **Every character looks back.** Our transformer reading a sentence of the scoreboard's passage: one head's
  attention, arc by arc, then all sixteen heads' patterns; the lineage from 1964 to 2026; the plan.
* **1. A weighted average.** Nadaraya and Watson's kernel smoother (1964) on Part 7's data (how often "her" appears
  on each page of *Great Expectations*), the bandwidth knob; the formula turned into softmax(q·k/√d) v; the
  definition card; Bahdanau, Cho & Bengio (2014); what attention returns when every key is the same; queries, keys and
  values in the plane.
* **2. A memory that recalls.** Hopfield (1982): Hebbian storage, sign updates, the energy; ten hand-drawn 10×10
  letters with a quarter of their pixels flipped (the classical net recovers 2 of 10, one softmax step all 10);
  capacity on 100 units, 15% of each cue flipped (the classical net below half at 16 patterns and none at 25, against
  0.138 N; the modern update recalls every one of 320); Krotov & Hopfield (2016), Demircigil et al. (2017); Ramsauer
  et al.'s continuous energy and its one-step update ξ ← X softmax(βXᵀξ) = attention; β, the inverse temperature,
  from the average of everything to one pattern, through metastable blends; the 2024 Nobel Prize.
* **3. Why divide by √d.** Var(q·k) = d derived on a ladder and measured (spread 1.4 at d = 2 to 23 at d = 512; 1.00
  after scaling); the softmax collapsing over 64 keys (entropy 4.9 → 0.28 bits unscaled, 5.3 at every d scaled, of a
  possible 6); the softmax Jacobian p_i(δ_ij − p_j) and saturation (response 0.18 scaled, 0.10 unscaled at d = 512);
  μP's 1/d (Yang et al.).
* **4. Heads are low-rank maps.** sᵢⱼ = xᵢᵀ W_Q W_Kᵀ xⱼ: one 128×128 matrix of rank ≤ 32 (QK), and W_O W_V (OV)
  (Elhage et al. 2021); the singular values of all sixteen heads of our transformer (exactly 32 nonzero; 2–16
  directions hold 90%); a layer's four heads together have rank 127, the 128th direction removed by layer norm; why
  several narrow heads cost the same as one wide one; the low-rank bottleneck (Bhojanapalli et al. 2020).
* **5. Who may look at whom.** The causal mask (−∞ above the diagonal); every position a training example; checked
  on our transformer (changing the second half of a passage moves its first-half guesses by exactly 0, the second
  half's by up to 15.4; without the mask the first half moves by 7.9); encoder, decoder, encoder–decoder with
  cross-attention, prefix LM; permutation equivariance, checked (to rounding error) with the mask and positions off.
* **6. Our own transformer.** Pre-norm blocks, the residual stream, attention and MLP; 4 blocks × 4 heads, d = 128,
  834,048 parameters, 256 characters of context, 3,000 steps of 32 windows (24.6 million characters) on a CPU; 1.996
  bits a character on the passage; the training replayed at eleven checkpoints (passage bits, what it writes after
  the same prompt, the share of real words, all sixteen heads); the scoreboard row.
* **7. What a block costs.** 12d² + 9d parameters per block, the formula equal to the count (834,048); 2 operations
  per weight per token plus 2·2·L·T·d for attention, equal to PyTorch's FLOP counter at every context from 64 to 1,024;
  forward + backward = 3.0× forward (the 6N rule); the crossover T = 12d (1,536 for us, 147,456 for GPT-3); Kaplan et
  al. (2020).
* **8. Where is each character?** Sinusoids and the angle-addition rotation (a shift is one fixed matrix, checked);
  learned absolute positions; relative positions (Shaw et al. 2018, T5); ALiBi's slopes 2^(−8h/H) (Press et al.
  2021); no positions at all, and how the causal mask leaks position (Haviv et al. 2022; Kazemnejad et al. 2023;
  Llama 4's NoPE layers).
* **9. Positions as rotations.** RoPE (Su et al. 2021): pairs turned by m·θⱼ, θⱼ = 10000^(−2j/d), one turn every 6
  characters to one in 35,000; the four-line proof that scores depend only on n − m (checked to rounding error); a
  pair seen moving; the long-range decay; which pairs a trained model uses (Barbero et al. 2024), measured on ours;
  partial RoPE in Qwen3-Next and Gemma 3's base of a million.
* **10. Four answers, trained side by side.** Four 3-layer transformers (d = 64, 4 heads, 128-character windows,
  1,000 steps, the same data in the same order), differing only in positions — sinusoids, RoPE, ALiBi, none — three
  seeds each, the training curves replayed (the order is fixed from step 200 on); within the training length RoPE is
  best (2.43 bits, every seed better than every seed of the others), ALiBi 2.56, sinusoids 2.73, no positions 3.27;
  read four times as far, ALiBi holds (2.51), no positions drifts up (+0.21), sinusoids (+1.9) and RoPE (+2.7) break;
  why: ALiBi's penalties (slopes 1/4 … 1/256) only grow past the edge, while no positions' 1/t signal shrinks below
  anything seen in training.
* **11. Longer than it was trained for.** Our transformer at 1,024 characters (4× its context): plain 4.9 bits at the
  far end against 1.8 for a sliding 256-character window; position interpolation, NTK-aware scaling (bloc97 2023) and
  YaRN (Peng et al. 2023) without retraining (YaRN best, 2.1); YaRN's recipe on screen (r = L/λ, the ramp γ with α = 1,
  β = 32, θ′ = (1−γ)θ/s + γθ, the temperature (0.1 ln s + 1)² = 1.30 at s = 4); log-n scaling, derived (Chiang &
  Cholak 2022), on its own and on top of NTK (it barely helps here: the broken angles, not the spread, are the
  problem); 100 steps of fine-tuning at 1,024 (0.4 million characters, under 2% of the original training) from
  interpolation (4.92 → 2.45) and from YaRN (2.13 → 1.81, against 1.80 for the window), their training curves shown.
* **12. Attention sinks, and three ways out.** Xiao et al. (2023); our transformer has none (no head gives the first
  character more than a fraction of an even share; its heads park on spaces); why the softmax needs a place to put
  nothing (Guo et al. 2024: active–dormant heads, value drains); growing a sink on purpose on the bigram-backcopy task
  with a one-layer model (3 seeds: 43% of the weight on the marker when there is nothing to copy, its value shrunk
  to 0.19× the others'); a sink logit (gpt-oss), an output gate (Qiu et al. 2025; Qwen3-Next, Kimi K3) and
  differential attention (Ye et al. 2024) trained on the same task, three seeds each, their training replayed: the sink
  logit takes 99.9% of the weight and leaves the marker 0%, the gate closes to 0.05 with nothing to copy (marker 29%),
  differential attention's weights sum to 0.54 (marker 41%); all four learn the task equally well.
* **13. Keeping scores in range.** W_Q, W_K grown by c on our transformer (largest score 37 → 142 at c = 2, entropy
  1.97 → 0.48 bits, 1.82 → 1.99 bits a character); ViT-22B's runaway logits (Dehghani et al. 2023); QK-norm and its
  Cauchy–Schwarz bound (and what bolting it onto a trained model costs: 2.14 bits); the soft cap c·tanh(s/c)
  (Gemma 2), which on our model makes the guesses worse (2.79 at c = 4 against 2.15).
* **14. Induction heads.** Our transformer on a held-out stretch shown twice, and on random letters shown twice; the
  previous-token head and the induction head ([a][b] … [a] → [b]); two-layer attention-only models (three seeds)
  forming the pair in a sudden drop of the loss (at steps 2,600 to 4,100, down to 1.5–2.2 bits), a one-layer model
  unable to (5.6); the heads forming, snapshot by snapshot; K-composition (Elhage et al.) of the previous-token heads
  into the induction heads rising from 0.13 to 0.19 against 0.13 for every other pair and 0.12 for random heads; our
  transformer has no induction head yet (0.3% of attention where one would look), and why (Olsson et al. 2022 saw
  them after 2.5–5 billion tokens).
* **15. Learning inside the prompt.** In-context linear regression; one layer of linear self-attention, trained,
  learns the matrices of one step of gradient descent (von Oswald et al. 2023); its answers against GD's on 4,000 new
  prompts (correlation 0.999); two and three layers beat two and three plain steps (0.13 against 0.31, 0.11 against
  0.15); exact least squares (Part 6) gets them all.
* **16. What a transformer can compute.** RASP (Weiss, Goldberg & Yahav 2021): select, aggregate, elementwise; a
  histogram compiled by hand into one head with a BOS marker (2,000 of 2,000 random sequences right; counts blur after
  189 in bfloat16 and 1,463 in float16); sorting in two layers (2,000 of 2,000); Tracr (Lindner et al. 2023); fixed
  depth and TC⁰ (Merrill & Sabharwal 2023), drawn as a fixed stack of layers over a growing input; tracking shuffles
  of five objects (Merrill, Petty & Sabharwal 2024); chains of thought (Merrill & Sabharwal 2024); the
  RASP-generalization conjecture (Zhou et al. 2023).
* **17. Attention in 2026.** Why the effort: chapter seven's T/12d for a model as wide as DeepSeek-V3 (d = 7,168):
  attention's term is 0.05 of the weights' at 4K tokens, 1.5× at 128K, 12× at 1M. Where the formula sits in today's
  models: sink logits, gates, QK-norm and NoPE layers inside; grouped-query and multi-head latent attention for the
  cache (Part 15); sliding windows, DeepSeek's sparse attention and DeepSeek-V4's compressed selection (Part 16);
  linear-attention hybrids (Qwen3-Next and Qwen3.5 at 3:1, Kimi Linear, Kimi K3 with 24 full-attention layers of 93,
  drawn layer by layer from its released configuration).
* **Recap** in eight pictures from the part's own results, where it comes back, six problems, Part 14's teaser,
  references.

Run from the repo root:

```
python tools/make.py ai13                 # compute what is missing, then build (English and Chinese)
python -m videos.ai.ai13.compute          # every experiment on its own (about 2.5 CPU-hours on 1-2 threads)
python -m videos.ai.ai13.compute tf       # one item; the others: smoother dotscale hopfield rope rasp tfwords heads
                                          #   qkscale extend positions sinks sinkref induction icl
python tools/build.py ai13                # English
python tools/build.py ai13 --lang zh      # Chinese
```

`compute.py` needs Part 1's novels (`.cache/ai1`), Part 7's page counts and Part 9's scoreboard rows (read through
their own `compute`/`load`). Everything is seeded. The transformer (`tf`, about 70 minutes) saves a checkpoint
with its RNG states every 250 steps (`.cache/ai13/tf.ckpt.pt`) and resumes from it; the multi-run items (`extend`,
`positions`, `sinks`, `induction`) save each finished run in `.cache/ai13/<item>.partial.json` and resume from there.
Set `AI13_THREADS` to change the number of torch threads (default 2). Other parts use this one: Parts 16, 19 and 30
load the transformer through `load("tf")` and `load_tf()` (with `CTX`, `DH`, `HEADS`, `LAYERS`, `rope_freqs()` and
`tf_bits()`), Part 21 reads `corpus()` and `rope_freqs()`, Part 31 the scoreboard row (`tf`'s `ctx` and
`passage_bits`), and Parts 15 and 30 draw with `heat_image` and `signed_image` from `common.py`.

## Computed results

*(filled in from `.cache/ai13/` by the run that made the video; the narration says whichever way they come out.)*

* **The transformer** (`tf`): 834,048 parameters, 3,000 steps × 32 × 256 characters; 1.996 bits a character on the
  passage (Kneser-Ney 2.04, Part 9's neural model 2.38, the two mixed 1.99); half the improvement in the first 50
  steps; real words in its samples 0% → 92%.
* **Scale** (`dotscale`): dot-product spread 1.42, 2.82, 5.70, 11.3, 22.7 at d = 2, 8, 32, 128, 512; scaled 1.00 ± 0.01.
* **Hopfield** (`hopfield`): classical net recovers 2 of 10 letters, one softmax step 10 of 10; capacity on 100 units
  below half at 16 patterns (0.48), 0 at 25; modern 1.00 up to 320.
* **Heads** (`heads`): QK and OV rank exactly 32 in every head; a layer's QK sum rank 127; parameters 262,144
  attention + 526,848 MLP + 2,304 norms + 42,752 embeddings = 834,048 = the formula; forward FLOPs per token measured =
  formula at T = 64…1,024; training/forward 3.0.
* **Context extension** (`extend`, far end = characters 768–1,024 of 1,024): plain 4.90, interpolation 4.92,
  NTK 4.42, YaRN 2.13, log n 4.93, NTK + log n 4.43, 256-character window 1.80; after 100 steps of fine-tuning,
  interpolation 2.45, YaRN 1.81.
* **Positions** (`positions`, three seeds, mean): within 128 characters sinusoids 2.732, RoPE 2.434, ALiBi 2.559,
  none 3.266; at 384–512 characters 4.642, 5.133, 2.511, 3.481.
* **QK growth** (`qkscale`, c = 1 … 4): largest logit 36.5 → 561; entropy 1.97 → 0.11 bits; bits 1.82 → 2.15; capped
  at 37: 2.79 at c = 4; QK-norm bolted on: 2.14 at every c.
* **Sinks** (`sinks`, bigram-backcopy task on the novels' 64 commonest characters, triggers space, e and t; one
  layer, 1,500 steps, three seeds): weight on the start marker when there is nothing to copy — plain softmax 0.43
  (0.38–0.48), sink logit 0.00 (with 99.9% of the weight on the sink itself), gate 0.29 (the gate 0.05 open with
  nothing to copy, 0.75 after a trigger), differential attention 0.41 (weights summing to 0.54, λ = 0.46); the plain
  head's marker value 0.19 × the others' (the drain); every variant learns the copies to 0.002 bits and the rest to
  2.59 (the task's own probabilities score 2.58 on the same test batch; `sinkref`).
* **Induction** (`induction`; attention-only, 64 random tokens, 5,000 steps): one layer ends at 5.57 bits on the
  repeat (from 6.22); two layers, three seeds, drop off a cliff at steps 2,600, 4,100 and 3,000 and end at 1.50, 2.16
  and 1.55; first seed: K-composition from its 2 previous-token heads into its 3 induction heads 0.13 → 0.19, every
  other pair 0.13, Q-composition of the circuit 0.04 (random heads 0.124 ± 0.007). Our transformer: no induction head
  (best 0.3% of attention one after the earlier copy); held-out text 1.79 bits the first time and 1.80 the second,
  random letters 10.8 and 10.9.
* **In-context regression** (`icl`; d = 4, 20 examples, 6,000 steps of 256 prompts): one linear-attention layer
  0.799 against one optimally sized GD step 0.786, their answers correlated 0.999 on 4,000 new prompts; two layers
  0.134 against two steps 0.310; three 0.110 against 0.148; exact least squares 0 (to rounding); guessing 0, 4.00.
* **RASP** (`rasp`): histogram 2,000/2,000, sort 2,000/2,000; counts distinguishable up to 189 (bfloat16), 1,463
  (float16).

## Fact-check notes

Claims about 2025–26 models were checked against their primary reports: gpt-oss's per-head sink logits (OpenAI
model card, 2025); Qwen3-Next's gated attention, partial RoPE (64 of 256 dimensions) and 3:1 Gated DeltaNet hybrid
(Qwen blog and config, 2025); Qwen3.5's hybrid layout (Qwen, 2026); the gate's first-token attention 46.7% → 4.8%
(Qiu et al. 2025, Table); Kimi Linear's Kimi Delta Attention (Moonshot AI, 2025); Kimi K3's 93 layers with 24
full-attention layers (Moonshot AI, 2026); DeepSeek-V3.2's sparse attention with a lightning indexer and DeepSeek-V4's
compressed sparse attention to a million tokens (DeepSeek-AI, 2025–26); Gemma 3's QK-norm, dropped soft-cap and
global-layer RoPE base 1,000,000 (Gemma Team 2025); Gemma 2's attention soft cap 50 (Gemma Team 2024); Llama 4's NoPE
layers and inference-time attention temperature (Meta, 2025); DeepSeek-V3's YaRN extension 4K → 32K → 128K in two
1,000-step phases (DeepSeek-AI 2024); ALiBi's 1,024 → 2,048 result (Press et al. 2021); ViT-22B's diverging attention
logits and QK-norm (Dehghani et al. 2023); the StreamingLLM result of four initial tokens (Xiao et al. 2023).

References: S. J. D. Prince, *Understanding Deep Learning* (2023), chapter 12; D. Jurafsky & J. H. Martin, *Speech
and Language Processing* (3rd ed. draft), chapters 9–10; Nadaraya (1964); Watson (1964); Hopfield (1982); Amit,
Gutfreund & Sompolinsky (1985); Krotov & Hopfield (2016); Demircigil et al. (2017); Ramsauer et al., *Hopfield
Networks is All You Need* (2020); Bahdanau, Cho & Bengio (2014); Vaswani et al., *Attention Is All You Need* (2017);
Yang et al., μP (2022); Elhage et al., *A Mathematical Framework for Transformer Circuits* (2021); Bhojanapalli et al.
(2020); Kaplan et al. (2020); Shaw, Uszkoreit & Vaswani (2018); Raffel et al., T5 (2020); Su et al., *RoFormer*
(2021); Press, Smith & Lewis, ALiBi (2021); Haviv et al. (2022); Kazemnejad et al. (2023); Barbero et al. (2024); Chen
et al., position interpolation (2023); bloc97, NTK-aware scaling (2023); Peng et al., *YaRN* (2023); Chiang & Cholak
(2022); Xiao et al., *Efficient Streaming Language Models with Attention Sinks* (2023); Guo et al., *Active-Dormant
Attention Heads* (2024); Qiu et al., *Gated Attention for Large Language Models* (2025); Ye et al., *Differential
Transformer* (2024); OpenAI, gpt-oss model card (2025); Dehghani et al., ViT-22B (2023); Gemma Team (2024, 2025);
Olsson et al., *In-context Learning and Induction Heads* (2022); von Oswald et al., *Transformers Learn In-Context by
Gradient Descent* (2023); Garg et al. (2022); Weiss, Goldberg & Yahav, *Thinking Like Transformers* (2021); Lindner
et al., *Tracr* (2023); Merrill & Sabharwal, *The Parallelism Tradeoff* (2023); Merrill & Sabharwal, *The Expressive
Power of Transformers with Chain of Thought* (2024); Merrill, Petty & Sabharwal, *The Illusion of State in State-Space
Models* (2024); Zhou et al., *What Algorithms Can Transformers Learn?* (2023);
DeepSeek-AI, DeepSeek-V2 (MLA, 2024), V3 (2024), V3.2 (2025), V4 (2026); Moonshot AI, Kimi Linear (2025), Kimi K3
(2026); Qwen Team, Qwen3 (2025), Qwen3-Next (2025).

## Problems, with solutions

**1. Why √d.** If the entries of q and k are independent with mean 0 and variances σ_q² and σ_k², show that
Var(q·k) = d σ_q² σ_k². What should the score be divided by?

*Solution.* q·k = Σᵢ qᵢkᵢ. Each term has mean E[qᵢ]E[kᵢ] = 0 and variance E[qᵢ²]E[kᵢ²] = σ_q²σ_k², by independence;
the d terms are independent, so their variances add: d σ_q²σ_k². Dividing by √d σ_q σ_k gives variance one; at
initialization, with unit variances, that is the √d of the formula.

**2. Relative by construction.** Let R_m rotate each pair of a vector by mθⱼ. Show that (R_m q)·(R_n k) depends only
on n − m, and that ALiBi's bias −m_h(i − j) has the same property.

*Solution.* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k. A rotation's transpose is its inverse, R_mᵀ = R_{−m}, and the 2×2 blocks
of one pair commute, so R_{−m} R_n = R_{n−m}: the score is qᵀ R_{n−m} k. ALiBi's bias is a function of i − j alone.
Both are unchanged when the query and key positions are shifted by the same amount.

**3. What a block costs.** Show that a pre-norm block with an MLP of width 4d (no biases on the attention matrices,
as in ours) has 12d² + 9d parameters, and that attention's 2LTd operations per token equal the weights' 24Ld² at
T = 12d.

*Solution.* W_Q, W_K, W_V, W_O: 4d². The MLP: d × 4d and 4d × d weights, 8d², with 4d + d biases. Two layer norms,
a gain and a bias each: 4d. Total 12d² + 9d (for d = 128, 197,760 per block). Each weight costs a multiply and an add
per token, 2 · 12d² per block, 24Ld² in all; equating with 2LTd gives T = 12d: 1,536 for our d = 128, 147,456 for
GPT-3's 12,288.

**4. A place to put nothing.** A head has a sink logit b and n keys with equal scores s. What share of its attention
goes nowhere? For which b is it one half?

*Solution.* The share is e^b / (e^b + n e^s). It is one half when e^b = n e^s, that is b = s + ln n: a sink must
outscore the keys by the log of their number to absorb half the weight.

**5. Temperature.** Show that the modern Hopfield update ξ ← Xᵀ softmax(βXξ) (the rows of X are the stored patterns)
tends to the stored pattern of largest overlap as β → ∞, and to the average pattern as β → 0.

*Solution.* The weights are pᵢ ∝ exp(β xᵢ·ξ). As β → ∞ the ratio pᵢ/pⱼ = exp(β(xᵢ − xⱼ)·ξ) → ∞ whenever xᵢ·ξ >
xⱼ·ξ, so all the weight goes to the largest overlap and the update returns that pattern (the average of the tied
ones, if several tie). As β → 0 every exponent tends to 1, the weights to 1/M, and the update to (1/M) Σᵢ xᵢ.

**6. Gradient descent is attention.** Show that one step of gradient descent from w = 0 on
L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)² predicts ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q) for a query x_q.

*Solution.* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ, so at w = 0 the step gives w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ, and
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q). This is attention without a softmax: the query x_q, the keys xᵢ, the values yᵢ,
scores xᵢ·x_q — the pattern the trained linear-attention layer of chapter fifteen finds.

## 习题与解答

**1. 为什么是根号d。** 设q和k的各个分量相互独立，均值为0，方差分别为σ_q²和σ_k²。证明 Var(q·k) = d σ_q² σ_k²。分数应该除以什么？

*解答。* q·k = Σᵢ qᵢkᵢ。由独立性，每一项的均值是 E[qᵢ]E[kᵢ] = 0，方差是 E[qᵢ²]E[kᵢ²] = σ_q²σ_k²；d个项相互独立，方差相加，得
d σ_q²σ_k²。除以 √d σ_q σ_k，方差就变成1；初始化时方差为1，这就是公式里的根号d。

**2. 天生就是相对的。** 设R_m把向量的每一对分量旋转mθⱼ。证明 (R_m q)·(R_n k) 只依赖于 n − m，并且ALiBi的偏置
−m_h(i − j) 也有同样的性质。

*解答。* (R_m q)·(R_n k) = qᵀ R_mᵀ R_n k。旋转的转置就是它的逆，R_mᵀ = R_{−m}；同一对上的2×2旋转块可以交换，所以
R_{−m} R_n = R_{n−m}，分数等于 qᵀ R_{n−m} k。ALiBi的偏置本来就只是 i − j 的函数。把查询和键的位置平移同样的量，两者都不变。

**3. 一个模块的成本。** 证明：MLP宽度为4d的前置归一化模块（注意力矩阵不带偏置，和我们的模型一样）有 12d² + 9d 个参数；
并且注意力每个词元的 2LTd 次运算，在 T = 12d 时等于权重的 24Ld² 次。

*解答。* W_Q、W_K、W_V、W_O：4d²。MLP：d × 4d 和 4d × d 的权重，8d²，外加 4d + d 个偏置。两个层归一化，各有增益和偏置：4d。
合计 12d² + 9d（d = 128 时，每个模块197,760个）。每个权重对每个词元做一次乘法和一次加法，每个模块 2 · 12d²，总共 24Ld²；
令它等于 2LTd，得 T = 12d：我们的d = 128时是1,536，GPT-3的d = 12,288时是147,456。

**4. 一个放“什么都没有”的地方。** 一个头有汇点logit b，以及n个分数都等于s的键。它有多少注意力哪儿也没去？b取多少时是一半？

*解答。* 份额是 e^b / (e^b + n e^s)。当 e^b = n e^s，也就是 b = s + ln n 时，它等于一半：汇点的分数要比那些键高出键数的对数，
才能吸走一半的权重。

**5. 温度。** 证明现代霍普菲尔德更新 ξ ← Xᵀ softmax(βXξ)（X的每一行是一个存储模式）在 β → ∞ 时趋于重叠度最大的存储模式，
在 β → 0 时趋于所有模式的平均。

*解答。* 权重 pᵢ ∝ exp(β xᵢ·ξ)。β → ∞ 时，只要 xᵢ·ξ > xⱼ·ξ，比值 pᵢ/pⱼ = exp(β(xᵢ − xⱼ)·ξ) 就趋于无穷，
所以全部权重都落到重叠度最大的那个模式上，更新返回这个模式（若有几个并列，则返回它们的平均）。β → 0 时，每个指数都趋于1，
权重趋于1/M，更新趋于 (1/M) Σᵢ xᵢ。

**6. 梯度下降就是注意力。** 证明：在 L(w) = (1/2N) Σᵢ (w·xᵢ − yᵢ)² 上，从 w = 0 出发走一步梯度下降，对查询x_q的预测是
ŷ = (η/N) Σᵢ yᵢ (xᵢ·x_q)。

*解答。* ∇L(w) = (1/N) Σᵢ (w·xᵢ − yᵢ) xᵢ，所以在 w = 0 处走一步得 w₁ = −η∇L(0) = (η/N) Σᵢ yᵢ xᵢ，于是
ŷ = w₁·x_q = (η/N) Σᵢ yᵢ (xᵢ·x_q)。这就是不带softmax的注意力：查询是x_q，键是xᵢ，值是yᵢ，分数是xᵢ·x_q——正是第15章里训练出来的
线性注意力层自己找到的模式。

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| attention; query, key, value | 注意力；查询，键，值 |
| kernel smoother (Nadaraya–Watson), bandwidth | 核平滑器（纳达拉亚–沃森），带宽 |
| scaled dot-product attention | 缩放点积注意力 |
| softmax saturation, Jacobian | softmax饱和，雅可比矩阵 |
| inverse temperature (β) | 逆温度（β） |
| modern Hopfield network, metastable state | 现代霍普菲尔德网络，亚稳态 |
| attention head, multi-head attention | 注意力头（头），多头注意力 |
| QK circuit, OV circuit | QK回路，OV回路 |
| low rank, low-rank bottleneck | 低秩，低秩瓶颈 |
| causal mask | 因果掩码 |
| encoder, decoder, cross-attention, prefix language model | 编码器，解码器，交叉注意力，前缀语言模型 |
| permutation equivariance | 置换等变性 |
| transformer block | Transformer模块 |
| FLOPs per token | 每个词元的浮点运算数 |
| sinusoidal position encoding, learned absolute positions | 正弦位置编码，学出来的绝对位置 |
| relative positions, ALiBi | 相对位置，ALiBi |
| no positional encoding (NoPE) | 无位置编码（NoPE） |
| rotary position embedding (RoPE), wavelength, base | 旋转位置编码（RoPE），波长，底数 |
| context extension | 上下文扩展 |
| position interpolation, NTK-aware scaling, YaRN | 位置插值，NTK感知缩放，YaRN |
| ramp (γ), attention temperature | 斜坡（γ），注意力温度 |
| log-n scaling | log n缩放 |
| attention sink, sink logit | 注意力汇点，汇点logit |
| active–dormant head, value drain | 活跃-休眠头，值的排空 |
| gated attention (output gate) | 门控注意力（输出门控） |
| differential attention | 差分注意力 |
| QK-norm | QK归一化 |
| soft cap (logit soft-capping) | 软上限（logit软封顶） |
| induction head, previous-token head | 归纳头，前一词元头 |
| K-, Q-, V-composition | K组合，Q组合，V组合 |
| phase change (in training) | （训练中的）相变 |
| in-context learning, linear self-attention | 上下文学习，线性自注意力 |
| RASP; select, aggregate | RASP；选择（select），聚合（aggregate） |
| Tracr | Tracr |
| threshold circuit, TC⁰, NC¹ | 阈值电路，TC⁰，NC¹ |
| hybrid (linear + full attention) | 混合架构（线性注意力加完整注意力） |
