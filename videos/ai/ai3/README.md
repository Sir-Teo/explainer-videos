# AI, Built — Part 3: Vectors That Mean Things

Part 3 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Part 1's
counting model could not tell *the dog barked* from *the hound barked*; this part gives words a place in a space,
and builds the linear algebra to work there. A hook and nine chapters:

* **Where words live.** Two contexts as islands; 102 words placed where GPT-2 puts them (its embedding matrix,
  50,257 × 768, on the words' top three principal directions), turning in 3D, seven categories apart; *dog*,
  *puppy* and *tobacco* as 768 numbers each.
* **Vectors.** Arrows and lists of numbers; addition and scaling; combinations sweeping out the plane; a basis.
* **The dot product.** Coordinate products summed, and |a||b|cos θ; the shadow as one vector turns; cosine
  similarity of GPT-2's vectors (dog·puppy 0.62, dog·cat 0.55, dog·tobacco 0.23); GPT-2's logits *are* dot products
  with the same (tied) vectors: after "The Eiffel Tower is located in the city of", Paris, London, Amsterdam, and the
  softmax gives Paris 0.064, Part 1's number.
* **Matrices.** The plane moved by a matrix; columns are where the basis arrows land; matrix times vector;
  composition and order; the determinant as area, zero (squashed) and negative (flipped).
* **Eigenvectors.** Directions a matrix leaves on their line; symmetric matrices and the spectral theorem, drawn as
  turn, stretch, turn back; covariance and principal components.
* **The singular value decomposition.** Every matrix as turn, stretch, turn (checked against the matrix in one
  go); the ellipse's half-axes; the spectral norm as the longest image of a unit vector, swept; a vector through 40
  random 256 × 256 layers with gains 0.8, 1.0, 1.2 (× 0.0001, × 1.5, × 2,116).
* **Low rank.** A matrix as a sum of rank-one pieces; Eckart–Young on Part 1's 26 × 26 letter-pair table (the square
  root of P(previous, next)): errors 0.56 after one piece, 0.40 after two, exactly the singular values left out;
  correspondence analysis puts i, a, o, u, e at one end of its first axis.
* **Word vectors.** The books' co-occurrence table (10,000 words, window 4, 4.35 million words of text), positive
  PMI, truncated SVD to 100 numbers: Monday → Saturday, Tuesday; three → four, two; dog → … wolf, cat, Perezvon (a dog
  in *The Brothers Karamazov*); France → Paris from England lands on London; word2vec (skip-gram with negative
  sampling) trained on the same books, and Levy & Goldberg's equivalence.
* **High dimensions.** Angles between random directions for d = 2, 3, 10, 100, 768 (spread 52° down to 2.1°); 10,000
  random directions in 768 dimensions all between 79° and 101°, and superposition; lengths concentrating at √d;
  99.96% of a ball's volume within 1% of its surface; GPT-2's vectors share a direction (mean cosine 0.24; 0.01
  after centring).
* **Johnson–Lindenstrauss.** 1,000 of GPT-2's vectors through one random 768 × k matrix: within 10% for 84% of the
  distances at k = 100 and 99.6% at k = 400; the lemma's (cautious) bound.
* **Recap**, where it comes back, Part 4's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai3.compute          # GPT-2's weights (Hugging Face) and Part 1's books (.cache/ai1)
python tools/build.py ai3                # English
python tools/build.py ai3 --lang zh      # Chinese
```

References: G. Strang, *Linear Algebra and Learning from Data* (2019); S. Axler, *Linear Algebra Done Right* (2024);
R. Vershynin, *High-Dimensional Probability* (2018); Eckart & Young (1936); Johnson & Lindenstrauss (1984);
Dasgupta & Gupta (2003); Deerwester et al. (1990); Mikolov et al. (2013); Levy & Goldberg (2014); Ethayarajh (2019);
Radford et al. (2019); Elhage et al. (2022).
