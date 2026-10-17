# AI, Built — Part 13: Sparsity

Part 13 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Using
only some of a model at a time: mixtures of experts, and attention that looks at only some of the past. A hook and
four chapters:

* **A few experts at a time.** DeepSeek-V3's 256 experts per layer, 8 (and a shared one) lighting up for each word.
* **A mixture of experts.** The router, top-k selection and the gate; total against active parameters for Mixtral,
  DeepSeek-V3, Qwen3-235B-A22B, gpt-oss-120b, Kimi K2 and Qwen3-Next, as published.
* **Keeping every expert busy.** A character model whose hidden layer is 8 experts (2 per character), trained here
  three ways: without balancing, with Switch's auxiliary loss, and with DeepSeek-V3's loss-free bias; each expert's
  share of the work through training.
* **What experts learn.** Where characters send their contexts; the mixture against dense models with the same
  compute and the same parameters.
* **Sparse attention.** In Part 11's transformer, how much attention the top k keys hold, and the bits per character
  when each query may use only k keys, chosen by score or as a sliding window; NSA and DeepSeek Sparse Attention.
* **Recap**, where it comes back, Part 14's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai13.compute          # needs Part 1's books and Part 11's transformer (.cache/ai11/tf.pt)
python tools/build.py ai13                # English
python tools/build.py ai13 --lang zh      # Chinese
```

References: Jacobs, Jordan, Nowlan & Hinton (1991); Shazeer et al. (2017); Lepikhin et al., GShard (2020); Fedus, Zoph
& Shazeer, Switch Transformers (2021); Wang et al., auxiliary-loss-free balancing (2024); DeepSeek-AI, DeepSeek-V3
(2024) and V3.2-Exp (2025); Yuan et al., Native Sparse Attention (2025).
