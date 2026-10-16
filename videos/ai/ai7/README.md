# AI, Built — Part 7: Fitting and Generalizing

Part 7 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). A model
is fitted to examples; why should it work on anything else? The classical answers, and the two experiments that
broke them, mostly on Part 5's pages (Austen and Dickens, 448 for training, 191 held out). A hook and four chapters:

* **The gap.** Part 5's nearest-neighbour vote: 93% of training pages but 68% of new ones with one neighbour; the
  two error curves meeting as more neighbours vote.
* **Bias and variance.** Sixteen noisy points from one curve, drawn 200 times (illustrative): straight lines miss the
  same way every time, degree-12 polynomials differ every time, degree 5 is right; bias² + variance + noise, the U.
* **How much can a model fit?** Lines in the plane split 3 points every way (8 labellings) but not 4 (the two XOR
  labellings): VC dimension 3 and the VC bound; linear models on 1 to 70 word rates fitting coin flips (53% to 68%),
  Rademacher complexity.
* **Memorizing nonsense.** One network (70 → 512 → 512 → 2, 300,034 weights) trained on the true authors (99.5% of new
  pages) and on shuffled authors: it fits every shuffled label too, and is at chance on new pages (Zhang et al.).
* **Double descent.** Least squares on p random ReLU features, minimum-norm past p = n = 448: the error falls, rises,
  explodes at p = n, and falls again below the first minimum (Belkin et al.).
* **Recap**, where it comes back, Part 8's teaser (a ReLU network's linear pieces), references.

Run from the repo root:

```
python -m videos.ai.ai7.compute          # needs Part 5's pages (.cache/ai5); torch for two items
python tools/build.py ai7                # English
python tools/build.py ai7 --lang zh      # Chinese
```

References: S. Shalev-Shwartz & S. Ben-David, *Understanding Machine Learning* (2014); T. Hastie, R. Tibshirani & J.
Friedman, *The Elements of Statistical Learning* (2009); V. Vapnik, *The Nature of Statistical Learning Theory*
(1995); Geman, Bienenstock & Doursat (1992); Vapnik & Chervonenkis (1971); Bartlett & Mendelson (2002); Zhang et al.
(2017); Belkin, Hsu, Ma & Mandal (2019); Nakkiran et al. (2020).
