# AI, Built — Part 13: Attention as Geometry

Part 13 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)), and the
first of Act III, *Engines*. What attention computes, how a transformer is put together, how it knows where things
are, and what its heads learn to do. Every model here is trained by `compute.py` (PyTorch, CPU), including the
series' own small transformer, which joins the scoreboard. A hook and six chapters:

* **Every character looks back.** Our transformer reading a sentence of the scoreboard's passage: one head's
  attention, arc by arc, then all sixteen heads' patterns.
* **A weighted average.** Nadaraya and Watson's kernel smoother on Part 7's data (how often "her" appears on each page
  of *Great Expectations*): a bump of weights sliding along, the bandwidth knob; the formula turned into
  softmax(q·k/√d) v; queries, keys and values in the plane; why the √d: unscaled, the softmax over 64 random keys
  collapses from 4.9 bits of spread to 0.28 as d grows, scaled it stays at 5.3.
* **Our own transformer.** The residual stream, attention between positions and an MLP within each, LayerNorm;
  four heads of the trained model's first layer and the causal mask; training on the thirty novels, the curve, the
  scoreboard row, and its writing.
* **Positions as rotations.** Attention is blind to order; RoPE turns each pair of a query's numbers by m·θ_j (one
  turn every 6 characters for the fastest pair, every 35,000 for the slowest); rotated scores depend only on the
  distance (checked to 10⁻¹⁴); the long-range decay.
* **Longer than it was trained for.** Our model at four times its training context: as trained it breaks past 256
  characters; position interpolation, NTK-aware scaling and YaRN, with no retraining, measured position by position;
  YaRN's recipe on screen: turns per pair over the training context r = L/λ, the ramp γ = clip((r−α)/(β−α), 0, 1)
  with α = 1, β = 32 (in our heads 1 pair kept, 6 on the ramp, 9 slowed by 4), the blended angle
  θ′ = (1−γ)θ/s + γθ, and the temperature √(1/t) = 0.1 ln s + 1 (every score × 1.30 at s = 4);
  attention sinks: our small model has none (every head gives the first character under a third of an even share),
  so a large model's sink head is drawn as a labeled schematic; then four changes frontier models make to attention,
  each with its equation and a small computed plot: gpt-oss's sink logit e^b in the softmax's denominator (b = 2
  and 8 equal scores: 48% goes nowhere), Qwen3-Next's sigmoid output gate, QK-norm (scores bounded however the
  weights grow), and Gemma 2's soft cap c·tanh(s/c) with c = 50.
* **Induction heads.** A random string shown twice: our small transformer does no better the second time (it has
  not built induction heads in its short training); the two-head mechanism
  ([a][b] … [a] → [b]); a two-layer attention-only model forming an induction head in a sudden drop of the loss, a
  one-layer model unable to, and the two heads' patterns.
* **Learning inside the prompt.** In-context linear regression: one layer of linear attention, trained, learns the
  matrices of one step of gradient descent (correlation 0.999 with it on new prompts); two and three layers beat two
  and three plain steps.
* **Recap**, where it comes back, Part 15's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai13.compute          # needs Part 1's books (.cache/ai1), Part 7's data and Part 9's model
python tools/build.py ai13                # English
python tools/build.py ai13 --lang zh      # Chinese
```

The transformer takes the longest (3,000 steps of 32 × 256 characters: one to two hours on a 4-core CPU); its weights
are kept in `.cache/ai13/tf.pt` for the context-extension item.

References: S. J. D. Prince, *Understanding Deep Learning* (2023); Nadaraya (1964); Watson (1964); Vaswani et al.
(2017); Su et al., RoFormer (2021); Chen et al., position interpolation (2023); bloc97, NTK-aware scaling (2023); Peng
et al., YaRN (2023); Xiao et al., attention sinks (2023); Qiu et al., gated attention (2025); Dehghani et al.,
QK-norm (2023); Gemma Team, Gemma 2 (2024); OpenAI, gpt-oss (2025); Elhage et al., transformer circuits (2021); Olsson et al.,
induction heads (2022); Garg et al. (2022); von Oswald et al. (2023).
