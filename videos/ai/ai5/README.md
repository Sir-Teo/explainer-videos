# AI, Built — Part 5: Randomness in Motion

Part 5 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). A model
hands us distributions; it is fitted by maximum likelihood, it is sampled to write, and the newest image generators
are random motion run backwards. This part is the probability behind all of that, from a Galton board to the
reverse-time SDE. A hook and nine chapters:

* **Out of noise.** 600 random dots flow, by the reverse-time SDE with the exact score of the noised data, into the
  letters "AI"; run forwards, the letters dissolve back into noise.
* **The bell curve.** 1,000 balls through 12 rows of pegs (agreeing with the binomial, χ² = 12.1 on 12 degrees of
  freedom); C(12, k)/2¹² and the normal density; the sum of k dice, exactly, for k = 1, 2, 3, 6, 12: the central
  limit theorem, the spread growing like √k.
* **Fitting a bell.** A candidate bell scored by its average log-likelihood on the balls; the score of every
  (μ, σ) as a landscape (3D), climbed by gradient ascent to μ̂ = 5.96, σ̂ = 1.71 (√3 predicted); maximum
  likelihood is minimum cross-entropy.
* **Belief as a distribution.** How often is a letter "e"? Bayes's rule from a flat prior on Part 1's passage: after
  10, 100, 1,000 and 10,000 letters, with the view zooming in; 95% of the belief between 0.120 and 0.134, the whole
  passage at 0.122; Laplace's rule of succession.
* **Rolling loaded dice.** Letter probabilities laid end to end and a uniform random number (inverse-CDF sampling);
  GPT-2's next-word distribution under a live temperature dial (entropy 4.7, 9.0, 13.5 bits at T = ½, 1, 2) and its
  samples at T → 0, ½, 1, 2.
* **Chains with short memories.** A three-state chain (space, vowel, consonant) from Part 1's pairs: one walker's
  time shares settle to 19%, 31%, 50%; the stationary distribution as the eigenvector of eigenvalue 1; all 27 letters
  from "q", forgetting the start within five steps at a rate set by the second eigenvalue, 0.30.
* **Answers from random samples.** π from 4,000 darts; the error falls like 1/√N (fitted slope −0.50 over 200 runs
  at nine sizes); a rare event, P(Z > 4) = 3.17 × 10⁻⁵: two hits in 10,000 plain samples, within 1% by importance
  sampling.
* **Sampling the unsampleable.** Metropolis on a two-bump density known up to a constant: proposals accepted and
  rejected, then 6,000 steps; 65% of the time in the bump that holds two thirds.
* **Brownian motion.** Random walks with 8, 64, 1,024 steps of ±1/√n; 60 paths inside ±√t, with variances 0.25,
  0.49, 0.74, 0.98 measured on 20,000; a cloud spreading in the plane, and the heat equation.
* **Randomness with a push.** dx = f dt + g dW and Euler–Maruyama; the Ornstein–Uhlenbeck process; the
  Fokker–Planck equation solved on a grid against 20,000 particles (two peaks into a standard bell); Anderson's
  reverse-time SDE and the score, in 1D and in the plane.
* **Recap**, where it comes back, Part 6's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai5.compute          # needs Part 1's books (.cache/ai1) and GPT-2's weights
python tools/build.py ai5                # English
python tools/build.py ai5 --lang zh      # Chinese
```

References: J. K. Blitzstein & J. Hwang, *Introduction to Probability* (2019); D. J. C. MacKay, *Information Theory,
Inference, and Learning Algorithms* (2003); B. Øksendal, *Stochastic Differential Equations* (2003); Metropolis et al.
(1953); Hastings (1970); Einstein (1905); Anderson (1982); Sohl-Dickstein et al. (2015); Song et al. (2021);
Holtzman et al. (2020).
