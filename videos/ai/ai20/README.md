# AI, Built — Part 20: Inside the Model

The last part of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)).
Reading what a model has learned, with Part 11's transformer as the patient. A hook, four chapters and the series'
close:

* **What is it thinking?** The 128 numbers the transformer carries per character after its second block, for a line of
  the passage: all busy, none meaningful; the same rewritten as sparse features.
* **More ideas than dimensions.** Elhage et al.'s toy model, x̂ = ReLU(WᵀWx + b), 5 features through 2 numbers, trained
  at four sparsities: two features at right angles, then opposite pairs, then a pentagon; the sparsest model's five
  arrows during training, from random to the pentagon; the interference of one
  feature on the rest before and after the bias and ReLU; the cosine between random directions in 2 to 1,024
  dimensions (spread ≈ 1/√d).
* **Pulling the features apart.** A sparse autoencoder with 512 features on 200,000 residual vectors: f = ReLU(Wₑx + bₑ),
  x̂ = Σ fₖdₖ + b_d, loss ‖x − x̂‖² + λ‖f‖₁; features active per character and variance explained; where four features
  fire hardest; the model's own neurons against the features (how many of a unit's 8 strongest moments share a
  character). Newer dictionaries: TopK (keep the k largest, no penalty to tune, no shrinkage), trained here beside the
  L1 one at several sizes, sparsity against variance explained; JumpReLU (a learned threshold per feature);
  transcoders and crosscoders.
* **Tracing a thought.** An attribution graph for one prediction (activation × gradient through the features, and
  which input characters switched each feature on); Anthropic's circuit tracing in Claude 3.5 Haiku (published).
* **Reaching in.** Steering: adding a quotation-mark feature's direction while the model writes, at three strengths;
  chain-of-thought faithfulness (Chen et al., published).
* **Recap**, the series map act by act, the scoreboard from Part 1 with every model built since, references.

Run from the repo root:

```
python -m videos.ai.ai20.compute          # needs Part 11's transformer (python -m videos.ai.ai11.compute tf)
python tools/build.py ai20                # English
python tools/build.py ai20 --lang zh      # Chinese
```

References: Olah et al., Zoom In (2020); Elhage et al. (2022); Johnson & Lindenstrauss (1984); Bricken et al. (2023);
Cunningham et al. (2023); Templeton et al. (2024); Ameisen et al. (2025); Lindsey et al. (2025); Turner et al. (2023);
Chen et al. (2025); Gao et al., TopK SAEs (2024); Rajamanoharan et al., JumpReLU SAEs (2024).
