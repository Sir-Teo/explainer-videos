# AI, Built — Part 16: Sparsity

Part 16 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)). Using
only some of a model at a time: mixtures of experts, and attention that looks at only some of the past. A hook and
four chapters:

* **A few experts at a time.** DeepSeek-V3's 256 experts per layer, 8 (and a shared one) lighting up for each word.
* **A mixture of experts.** The router, top-k selection and the gate; total against active parameters for Mixtral,
  DeepSeek-V3, Qwen3-235B-A22B, gpt-oss-120b, Kimi K2 and Qwen3-Next, as published; DeepSeek-V3's router exactly:
  sigmoid scores, a balancing bias that picks experts but never weighs them, a shared expert; C(16, 2) = 120 against
  C(64, 8) ≈ 4.4 billion combinations for the same compute.
* **Keeping every expert busy.** A character model whose hidden layer is 8 experts (2 per character), trained here
  three ways: without balancing, with Switch's auxiliary loss, and with DeepSeek-V3's loss-free bias; each expert's
  share of the work through training. Busiest expert at the end: 3.2x a fair share unbalanced (four experts starve),
  2.8x with the auxiliary loss at Switch's strength, 1.1x with the bias. Held-out bits 2.453 / 2.410 / 2.434.
* **What experts learn.** Where characters send their contexts; the mixture against dense models with the same
  compute and the same parameters: 2.434 bits against 2.485 and 2.510 (after the same 3,000 steps, the eight-times-wider
  dense model hasn't caught up).
* **Sparse attention.** In Part 13's transformer, how much attention the top k keys hold, and the bits per character
  when each query may use only k keys, chosen by score or as a sliding window; NSA and DeepSeek Sparse Attention,
  drawn on one real query (layer 1, head 4) whose last 48 keys hold 90% of its attention: a window of 8 keeps 7%,
  NSA's two best blocks plus the window 75% (16 keys), the top 8 by score 76%; both as equations: NSA's gated
  sum of three attentions, DSA's ReLU indexer over every past token and attention over its top 2,048.
* **Recap**, where it comes back, Part 21's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai16.compute          # needs Part 1's books and Part 13's transformer (.cache/ai13/tf.pt)
python tools/build.py ai16                # English
python tools/build.py ai16 --lang zh      # Chinese
```

References: Jacobs, Jordan, Nowlan & Hinton (1991); Shazeer et al. (2017); Lepikhin et al., GShard (2020); Fedus, Zoph
& Shazeer, Switch Transformers (2021); Wang et al., auxiliary-loss-free balancing (2024); DeepSeek-AI, DeepSeek-V3
(2024) and V3.2-Exp (2025); Yuan et al., Native Sparse Attention (2025).
