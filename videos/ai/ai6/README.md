# AI, Built — Part 6: Statistical ML

Part 6 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)): models
with hidden parts, which we never observe and only infer. It reuses Part 5's 639 pages (Austen and Dickens, 70 word
rates each) and Part 1's books, and every method is written out in numpy in `compute.py`. A hook and seven chapters:

* **Structure nobody labelled.** The pages along their three main directions, uncoloured; a two-component mixture
  fitted without labels recovers the authors (97% agreement).
* **Principal components.** The 70 × 70 covariance, its eigenvectors and the share of variation along each (12.6%,
  9.1%, ...); direction 1 weighs not/be/very/she against the/and/out (Austen against Dickens), direction 2
  I/me/you/said/my against of/their (dialogue against narration); one cut along direction 1 sorts 88% of pages.
* **Mixtures and EM.** Two Gaussians, badly started, fitted by expectation-maximization on the first two
  directions: soft colours, refitted bells, the log-likelihood that never falls; 97% agreement with the authors.
* **Hidden Markov models.** Two hidden states, Baum–Welch on 200,000 letters from random guesses: one state ends up
  emitting the space and a, e, i, o, u, the other every consonant, alternating 72% of the time (Cave & Neuwirth,
  1980); Viterbi decoding of Shannon's sentence.
* **Models as pictures.** Graphical models: the mixture and the hidden Markov model as circles and arrows, the joint
  probability as a product of factors (Pearl); a language model as a picture with every arrow.
* **Gaussian processes.** The rate of "her" across the 186 pages of *Great Expectations*: prior samples, posterior
  samples, the mean and its band, the length scale (2 pages) chosen by marginal likelihood; the band opening beyond
  the first 20 pages.
* **Variational inference.** The best single Gaussian for Part 4's two-bump density: KL(q‖p) settles in one bump,
  KL(p‖q) covers both; the ELBO.
* **Kneser–Ney.** Discounting and continuation counts; character n-grams on Part 1's books, context 0 to 7: the
  passage's bits per character fall to 2.04 (Part 1's best counting model: 2.32), the scoreboard's new row.
* **Recap**, where it comes back, Part 7's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai6.compute          # needs Part 1's books (.cache/ai1) and Part 5's pages (.cache/ai5)
python tools/build.py ai6                # English
python tools/build.py ai6 --lang zh      # Chinese
```

References: C. M. Bishop, *Pattern Recognition and Machine Learning* (2006); C. E. Rasmussen & C. K. I. Williams,
*Gaussian Processes for Machine Learning* (2006); D. Jurafsky & J. H. Martin, *Speech and Language Processing*;
Pearson (1901); Hotelling (1933); Dempster, Laird & Rubin (1977); Baum et al. (1970); Rabiner (1989); Cave & Neuwirth
(1980); Pearl (1988); Jordan et al. (1999); Kneser & Ney (1995); Chen & Goodman (1998).
