# AI, Built — Part 10: The Mathematics of Scale

Part 10 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)), and
the end of Act II. What happens as networks grow, measured on the series' own small models: every run is computed by
`compute.py` (PyTorch, CPU) on a character model like Part 9's, scored in bits per character on held-out text. A hook
and three chapters:

* **A power law.** Held-out loss at seven widths, fitted by L(N) = E + A·N^(−α).
* **Wider and wider.** How far the hidden weights move in training falls with width (about 1/√width): the lazy,
  neural-tangent-kernel regime. Learning-rate sweeps at widths 32, 256 and 2,048: the best rate drifts with width in
  the usual parametrization and stays put in μP (Yang & Hu; Tensor Programs V).
* **Size or data?** C ≈ 6ND; three compute budgets, each split five ways between model size and training tokens: a
  valley per budget, the best size growing with the budget; Kaplan et al. (2020) and Chinchilla (2022); Chinchilla's
  third method, L(N, D) = E + A/N^α + B/D^β, fit to the 18 runs (E = 1.92, α = 0.72, β = 0.55, off by 0.02 bits):
  N_opt ∝ C^(β/(α+β)) = C^0.43, about 40 characters per parameter; matching the best loss with a model 3/4 the size
  costs 7% more training, with 1/2 the size 73% more, and below about a third of the size no budget suffices.
* **Grokking.** (a + b) mod 97 from 40% of the table: memorized early, understood thousands of steps later, with
  weight decay; the learned number vectors are a few Fourier frequencies, numbers on circles (Nanda et al.).
* **Recap**, where it comes back, Part 11's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai10.compute         # needs Part 1's books (.cache/ai1); about an hour on a CPU
python tools/build.py ai10               # English
python tools/build.py ai10 --lang zh     # Chinese
```

References: D. A. Roberts, S. Yaida & B. Hanin, *The Principles of Deep Learning Theory* (2022); S. J. D. Prince,
*Understanding Deep Learning* (2023); Jacot, Gabriel & Hongler (2018); Yang & Hu (2021); Yang et al. (2022); Kaplan
et al. (2020); Hoffmann et al. (2022); Power et al. (2022); Nanda et al. (2023).
