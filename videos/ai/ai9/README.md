# AI, Built — Part 9: Going Downhill

Part 9 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)): the
optimizers that train real models. Every run is computed by `compute.py`; the workhorse is a small character model
(8 characters of context, 16-number character vectors, 256 tanh units, a residual hidden layer) trained on Part 1's
books and scored in bits per character on held-out text. A hook and five chapters:

* **Three ways down.** Part 3's narrow valley (curvatures 1 and 30): gradient descent zigzags, momentum and Adam do
  not (49, 26 and 21 steps to within 5%).
* **Stochastic gradient descent.** Part 5's logistic regression on two word rates, a real two-weight loss: full-batch,
  16-page and 1-page steps; the cloud SGD settles into, about four times narrower at 16 times the batch; SGD as
  Part 4's SDE, with noise √(η/B).
* **The edge of stability.** A step on a bowl is stable only if the curvature is below 2/η; full-batch gradient
  descent on Part 8's spirals at two learning rates drives the sharpness (power iteration on Hessian-vector products)
  up to 2/η, where it stays (Cohen et al.).
* **Momentum and Adam.** The update rules (momentum, Adam, AdamW); five optimizers on the character model.
* **Muon.** The singular values of a real gradient matrix before and after Newton–Schulz orthogonalization; Muon on
  the hidden matrices against AdamW.
* **Learning-rate schedules.** Constant, cosine and warmup–stable–decay on the character model; the drop when the
  learning rate falls.
* **Recap**, where it comes back, Part 10's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai9.compute          # needs Part 1's books (.cache/ai1) and Part 5's pages (.cache/ai5)
python tools/build.py ai9                # English
python tools/build.py ai9 --lang zh      # Chinese
```

References: S. J. D. Prince, *Understanding Deep Learning* (2023); J. Nocedal & S. J. Wright, *Numerical
Optimization* (2006); L. Bottou, F. E. Curtis & J. Nocedal (2018); Robbins & Monro (1951); Polyak (1964); Li, Tai & E
(2017); Cohen et al. (2021); Kingma & Ba (2014); Loshchilov & Hutter (2017); Jordan et al. (2024); Liu et al. (2025);
Hu et al. (2024); Hägele et al. (2024).
