# AI, Built — Part 12: Memory

Part 12 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). What a
model has to remember while it reads, and the two ways to keep it: attention's growing cache, made smaller, and a
fixed-size matrix memory, written by better and better rules. A hook and six chapters:

* **Everything it has read.** Llama 3.1 70B's cache growing token by token, to 39 GiB at 128,000 tokens; a fixed-size
  memory as the alternative.
* **The cache.** Why attention keeps every key and value; the memory per token from published configurations: full
  attention, grouped-query attention (Llama 3.1), multi-head latent attention (DeepSeek-V3, 71 times smaller than
  full attention of the same shape) and a hybrid (Qwen3-Next).
* **Attention without the softmax.** (QKᵀ)V = Q(KᵀV): a T × T table or a d × d one; causal linear attention as a
  recurrence on a d × d state (checked against the parallel form to rounding error); the operation counts.
* **How to write to memory.** A matrix as an associative memory: adding (crosstalk growing like (N − 1)/d), decaying
  (old memories fade), the delta rule (write what should be there minus what is), in a changing world of 16 keys
  rewritten 256 times; the delta rule as one step of gradient descent; the gated delta rule.
* **State-space models.** A continuous-time state, read in steps of Δ; memory set by the step size; Mamba's selective
  steps holding a marked value through noise; Mamba-2: the same family as linear attention.
* **The gated delta rule.** The delta update as a rank-one change of a linear map, drawn on the plane: I - βkkᵀ shrinks
  only the key's direction (β = ½), erases it (β = 1, a projection) or reflects it (β = 2, eigenvalue -1, which lets
  linear RNNs track parity); the family of write rules (linear attention, decay, DeltaNet, Gated DeltaNet in
  Qwen3-Next, Kimi Delta Attention's per-channel gate) as S_t = S_{t-1}M_t + write; chunkwise training through the WY
  form of a product of (I - βkkᵀ), one triangular solve per chunk (the UT transform), checked against the recurrence on
  2,048 tokens (agreement 3e-15, gated 9e-16; 32 sequential steps instead of 2,048); Mamba-2's state-space duality,
  the decaying rule as masked attention (L ∘ QKᵀ)V with a semiseparable mask (every block below the diagonal rank one),
  checked to 9e-16.
* **A recall test.** Multi-query associative recall: tiny one-layer models with softmax attention, linear attention
  and the delta rule (keys of 16 numbers), trained here, as the number of key-value pairs grows: at 8 / 16 / 32 / 48
  pairs, softmax 100% throughout, adding 96 / 86 / 55 / 38%, the delta rule 100 / 99 / 95 / 88%.
* **Hybrids.** Jamba, MiniMax-01, Qwen3-Next and Kimi Linear: a few attention layers among many linear-time ones;
  the memory bill at 128,000 tokens.
* **Recap**, where it comes back, Part 13's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai12.compute
python tools/build.py ai12                # English
python tools/build.py ai12 --lang zh      # Chinese
```

References: Ainslie et al., GQA (2023); DeepSeek-AI, DeepSeek-V2 and V3 (2024); Katharopoulos et al. (2020); Widrow &
Hoff (1960); Schlag, Irie & Schmidhuber (2021); Yang et al., DeltaNet (2024) and Gated DeltaNet (2025); Gu et al., S4
(2022); Gu & Dao, Mamba (2023); Dao & Gu, Mamba-2 (2024); Sun et al., test-time training (2024); Arora et al., Zoology
(2023); Lieber et al., Jamba (2024); MiniMax-01 (2025); Qwen3-Next (2025); Kimi Linear (2025).
