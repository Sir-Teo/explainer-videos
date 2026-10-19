# AI, Built — Part 9: Networks

Part 9 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). What a
network is, what one layer and many layers can represent, what it takes to train a deep one, and the first neural
language model on the series' scoreboard. Every network here is trained by `compute.py` (PyTorch, CPU). A hook and
five chapters:

* **Two spirals.** A 2 → 32 → 32 → 32 → 2 ReLU network learning two interleaved spirals: its decision regions and its
  linear pieces (thousands of them) at steps 0, 50, 200, 600 and 3,000.
* **One layer can do anything.** A unit: a weighted sum and a ReLU, a hinge; a curve built from 2, 4, 8, 16 and 64
  hinges by least squares (the miss falling from 0.45 to 0.0014); the universal approximation theorem.
* **What depth adds.** The tent map composed k times: 2^k pieces from 2k units (Telgarsky); 48 random units arranged
  in 1 to 6 layers cut the plane into about 800 pieces whatever the depth (Hanin & Rolnick).
* **Signals through fifty layers.** 50 layers of 256 ReLUs: with weights 0.7× too small the signal shrinks about
  thirty million times, 1.4× too big it grows about ten million times, and at Var(w) = 2/n it stays steady (He et al.);
  gradients likewise.
* **The residual stream.** h + f(h); the identity in every block's Jacobian; 40 plain layers stuck at 50% on the
  spirals, 40 residual layers at 100%; LayerNorm; then today's block: pre-norm, RMSNorm (g ⊙ h / RMS(h)) and SwiGLU
  (W₂(SiLU(W₁x) ⊙ W₃x)), whose hidden width of 8d/3 keeps the weights at 3·d·(8/3)d = 8d², as with 4d.
* **A neural language model.** Bengio et al.'s design for characters (24 characters of context, learned 32-number
  vectors, 1,024 tanh units), trained on Part 1's books: its bits per character on the passage, its mixture with
  Part 7's Kneser–Ney (the scoreboard's new rows), the learned character vectors, and its writing.
* **Recap**, where it comes back, Part 11's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai9.compute          # needs Part 1's books (.cache/ai1) and Part 7's Kneser-Ney (.cache/ai7)
python tools/build.py ai9                # English
python tools/build.py ai9 --lang zh      # Chinese
```

References: I. Goodfellow, Y. Bengio & A. Courville, *Deep Learning* (2016); S. J. D. Prince, *Understanding Deep
Learning* (2023); D. A. Roberts, S. Yaida & B. Hanin, *The Principles of Deep Learning Theory* (2022); Cybenko (1989);
Hornik, Stinchcombe & White (1989); Telgarsky (2016); Hanin & Rolnick (2019); Glorot & Bengio (2010); He et al.
(2015, both); Ba, Kiros & Hinton (2016); Bengio, Ducharme, Vincent & Jauvin (2003).
