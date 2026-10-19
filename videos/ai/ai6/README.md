# AI, Built — Part 6: Classical ML

Part 6 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)), and the
start of Act II, *Learning*. One task runs through it: who wrote this page, Jane Austen or Charles Dickens? Pages are
1,000-word chunks of five of Part 1's novels (639 pages: *Pride and Prejudice* and *Emma*; *A Tale of Two Cities*,
*Great Expectations* and *A Christmas Carol*), each described, as Mosteller and Wallace described the Federalist
papers, by how often it uses the 70 commonest words; 30% of the pages are held out. The pictures use two of the
numbers: how often a page says "the", and how often it says "not". Every method is written out in numpy in
`compute.py`. A hook and eight chapters:

* **Least squares.** Three points and the squares on their misses; the fit as a perpendicular projection onto the
  plane of every line's predictions (3D), and the normal equations; Zipf's law on Part 1's 4.3 million words
  (slope −1.08, R² = 0.996).
* **Logistic regression.** A score, a line, the sigmoid; the probability sheet over the plane with the pages lifted
  to 0 and 1 (3D), fitted by cross-entropy (0.51 bits per page); 82% of held-out pages right with two rates, 190 of
  191 with all 70.
* **Ridge and lasso.** The loss's contours against a circle and a diamond (illustrative): the diamond's corner sets
  a weight to exactly zero; the lasso path on the 70 words, its first eight (not, she, very, be, to, out, such,
  mrs) giving 90%.
* **Fisher's direction.** Every page projected onto a turning direction, the two piles and Fisher's score; the best
  direction, S_W⁻¹(μ_D − μ_A); 82%.
* **Ask the neighbours.** A 15-neighbour vote; regions for k = 1, 15, 75 (93% of training pages but 68% of new
  ones at k = 1; 83% at k = 15).
* **The widest street.** The maximum-margin line and its support vectors (illustrative); the kernel trick as a lift
  onto a paraboloid (3D); a Gaussian-kernel SVM on the pages (83%; 99.5% with 70 rates).
* **Trees, forests, boosting.** The learned depth-3 tree and its boxes; accuracy against depth (best at depth 4,
  74% when grown fully); a random forest of 200 (94% → 98%) and gradient boosting (99%) on all 70 rates.
* **The contest.** Every method on the same held-out pages, with 2 rates and with 70.
* **Recap**, where it comes back, Part 7's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai6.compute          # needs Part 1's books (.cache/ai1)
python tools/build.py ai6                # English
python tools/build.py ai6 --lang zh      # Chinese
```

References: T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning* (2009); C. M. Bishop,
*Pattern Recognition and Machine Learning* (2006); K. P. Murphy, *Probabilistic Machine Learning* (2022); Mosteller &
Wallace (1963); Fisher (1936); Hoerl & Kennard (1970); Tibshirani (1996); Cover & Hart (1967); Cortes & Vapnik
(1995); Breiman (2001); Friedman (2001); Grinsztajn, Oyallon & Varoquaux (2022).
