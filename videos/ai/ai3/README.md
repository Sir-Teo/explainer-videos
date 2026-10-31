# AI, Built — Part 3: Vectors That Mean Things

Part 3 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). Part 1's counting model could not tell *the dog barked* from *the hound barked*;
this part gives words a place in a space and builds the linear algebra that every later part works in: the dot
product, einsum, projections, eigenvectors, the SVD and low rank, norms and conditioning, random matrices and what
training writes into weights, word vectors from counting and from guessing, the geometry of high dimensions, and low
rank at work in recommendation and retrieval. Every derivation is on screen step by step; every number is computed
here (`compute.py`) on a CPU, small enough for a laptop.

A hook, seventeen chapters and an outro (about 50 minutes; `python tools/lecture_length.py ai3`).

## Outline

* **Hook: where words live.** Two contexts as islands; 102 words where GPT-2 puts them (its 50,257 × 768 embedding
  matrix on the words' top three principal directions), seven categories apart; *dog*, *puppy*, *tobacco* as 768
  numbers each. How we got here: Grassmann (1844), Cayley (1858), Beltrami and Jordan (1873–74), Hilbert (1904),
  Eckart and Young (1936), Firth (1957), Johnson and Lindenstrauss (1984), latent semantic analysis (1990), the
  Netflix Prize (2006), word2vec (2013), LoRA (2021), GaLore and Muon (2024).
* **1. Vectors and the inner product.** Arrows and lists; addition, scaling, a basis; Grassmann. The dot product,
  derived as |a||b|cos θ from the law of cosines; the Cauchy–Schwarz inequality proved from a parabola's
  discriminant, the parabola drawn as one vector turns. Cosine similarity of GPT-2's vectors; GPT-2's logits are dot
  products with its own (tied) token vectors (after "The Eiffel Tower is located in the city of": Paris first).
* **2. Tensors and einsum.** Arrays with named axes; Einstein's summation convention (1916) as `einsum`: kept and
  summed indices, and cost as the product of all index sizes. Six operations in one notation. Attention as four
  contractions at GPT-2's size, with their multiply-add counts. (AB)C against A(BC): the same answer, fifty times
  apart in cost.
* **3. Matrices move space.** Linear maps, columns as the images of the basis, composition and order (Cayley 1858,
  Sylvester's word *matrix* 1850), the determinant as area, rank, column space and null space, rank–nullity.
* **4. Projection and least squares.** Projection onto a line and onto a column space derived (the normal equations,
  P = A(AᵀA)⁻¹Aᵀ, P² = P = Pᵀ); Legendre (1805) and Gauss (1809); a line fitted, with the error perpendicular to
  both columns; Gram–Schmidt and QR. Computed: classical and modified Gram–Schmidt against Householder QR, and the
  normal equations against QR, on Hilbert matrices as the condition number grows (loss of orthogonality ∝ κ², ∝ κ,
  and at round-off).
* **5. Directions that stay put.** Eigenvectors and the characteristic polynomial; symmetric matrices as turn,
  stretch, turn back; the spectral theorem proved in three steps (real eigenvalues, perpendicular eigenvectors,
  induction on the perpendicular space; Cauchy 1829, Hilbert 1904–10); the Rayleigh quotient as a weighted average
  of eigenvalues, swept around the circle; principal components (Pearson 1901, Hotelling 1933).
* **6. Power iteration, run live.** Abel–Ruffini: no formula, so iterate; the arrow swinging onto the top
  eigenvector; the convergence rate (λ₂/λ₁)ᵏ derived, and the Rayleigh quotient's doubled rate. Computed on GPT-2's
  768 × 768 token covariance and Part 1's letter table: the measured rates match λ₂/λ₁. Von Mises and
  Pollaczek-Geiringer (1929), PageRank (1998), spectral normalization (2018), Lanczos (1950).
* **7. The singular value decomposition.** Circle to ellipse in three stages (Vᵀ, Σ, U); the SVD derived from the
  spectral theorem applied to AᵀA; Beltrami, Jordan, Schmidt, Golub and Kahan; the spectral norm as the longest image
  of a unit vector, swept.
* **8. The best low-rank copy.** A matrix as a sum of rank-one pieces; the Eckart–Young theorem proved from Weyl's
  inequality; a landscape drawn by code sharpening rank by rank (the error equals the tail of the singular values,
  checked); Part 1's letter table, and correspondence analysis putting the vowels at one end; LSA, LoRA and latent
  attention.
* **9. How big is a matrix?** Frobenius and spectral norms; ‖A‖_F² = Σσᵢ² derived; stable rank. Computed: the stable
  ranks of all 48 matrices in GPT-2's blocks against a random matrix of the same shape (≈ 345). A vector through 40
  random layers (gains 0.8, 1.0, 1.2). The condition number derived as an error amplifier, and measured for 64- and
  32-bit arithmetic. Muon as steepest descent in the spectral norm; Newton–Schulz on a real gradient.
* **10. Random matrices and trained weights.** Wigner (1955) and the Marchenko–Pastur law (1967), checked on a
  random 768 × 3072 matrix; GPT-2's layer-6 MLP matrix: a bulk plus eigenvalues escaping the edge, which vanish when
  the same numbers are shuffled; power-law tails fitted (Clauset–Shalizi–Newman) for all 48 matrices against Martin
  and Mahoney's range; the novels model at initialization and after training.
* **11. Gradients are low rank.** A layer's gradient as a sum of outer products, derived; a small transformer trained
  on the novels, its gradient's singular values replayed through training; GaLore (2024): Adam in a rank-r window,
  memory counted, trained against Adam at three learning rates and three seeds, with a control (Adam with GaLore's
  step sizes); LoRA against GaLore: the effective rank of the total change.
* **12. Word vectors from counting.** Harris (1954), Firth (1957), latent semantic analysis (1990); the novels'
  co-occurrence table (10,000 words, window 4), PPMI, truncated SVD to 100 numbers; neighbours; meaning arriving
  direction by direction; analogies, and a test of 710 analogy questions built from the books, and category
  neighbours.
* **13. word2vec is counting in disguise.** Skip-gram with negative sampling (Mikolov et al. 2013) trained on the
  same books and replayed; Levy and Goldberg's theorem (2014) derived as a generalized shifted-PMI target for
  the smoothed negative distribution (ordinary PMI − log k when negatives follow the empirical context
  distribution). Finite optimization fits are measured at full rank on the 300 commonest words, at ranks 30
  and 5, and on the real 10,000-word run; full rank does not certify convergence to the target. GloVe
  (2014); counting against guessing on the same tests.
* **14. Life in 768 dimensions.** Angles between random directions; Var(cos θ) = 1/d derived and measured from d = 2
  to 4,096; 10,000 random directions all within a few degrees of perpendicular, and superposition; lengths
  concentrating at √d with spread 1/√2, derived and measured; the volume in a thin shell.
* **15. Johnson–Lindenstrauss, proved.** A thousand of GPT-2's vectors through one random matrix; the lemma
  (Dasgupta–Gupta form) and its proof: Gaussian projection, χ² variable, Chernoff bound, union bound. Checked: the
  per-pair failure rate on all 499,500 pairs against the exact χ² tail; the worst pair against a separate explicit
  95%-confidence union bound, with unavailable nontrivial bounds reported honestly; Larsen and
  Nelson's optimality (2017).
* **16. GPT-2's lopsided space.** Anisotropy (mean cosine of random tokens), the fix by centring, the top principal
  directions and what the first one tracks (token id, a proxy for frequency); all-but-the-top (Mu and Viswanath
  2018); representation degeneration (Gao et al. 2019); layer by layer inside the network (Ethayarajh 2019) and
  rogue dimensions (Timkey and van Schijndel 2021); the linear representation hypothesis (Mikolov, Yih and Zweig
  2013; Elhage et al. 2022; Park, Choe and Veitch 2024); Part 30.
* **17. Low rank in the wild.** The Netflix Prize (2006–09); matrix factorization with biases on a synthetic ratings
  world (4,000 users, 1,200 films, six hidden genres), trained by gradient descent and replayed: held-out error with
  and without the vector penalty (both retain the same bias penalty), by rank over three seeds against baselines
  fitted on the same ratings, and measured genre structure in film vectors whose training never used genre labels.
  Two-tower retrieval trained with an in-batch softmax and a negative-sampling correction: in the ideal
  candidate-classification calculation, the corrected training logit models a density ratio and the raw score
  models conditional log probability up to a user constant. Inference ranks raw scores; adding a popularity
  prior is a separate ablation. Measured macro recall@10 compares eligible known and brand-new users against
  popularity, with unavailable cohorts reported explicitly; YouTube (2016), FAISS (2017), dense passage retrieval
  (2020).
* **Outro.** Twelve recap tiles from the part's own results; where it comes back (Parts 4, 9, 11, 13, 15, 27, 30);
  eight problems; Part 4's teaser; references.

## Run

From the repo root:

```
python tools/make.py ai3                       # everything: compute, then English and Chinese builds
python -m videos.ai.ai3.compute                # just the numbers (.cache/ai3), about 1-2 CPU-hours
python -m videos.ai.ai3.compute galore sgns    # specific items; --force to recompute
python tools/build.py ai3                      # English
python tools/build.py ai3 --lang zh            # Chinese
```

The computation reads GPT-2 small from Hugging Face (`openai-community/gpt2`, about 500 MB, downloaded once into the
Hugging Face cache), Part 1's thirty novels (`.cache/ai1`, built by Part 1's compute on first use) and the series'
novels model (`python -m explainer.ai.novels`, which `make.py` runs first if it is missing). Every random choice is
seeded; the long items (`galore`, `galorectl`, `mf`) save each finished training run as they go, so an interrupted
run resumes. Torch runs with one or two threads, set inside the training functions.

## References

Books: G. Strang, *Linear Algebra and Learning from Data* (2019); S. Axler, *Linear Algebra Done Right*, 4th ed.
(2024); L. N. Trefethen and D. Bau, *Numerical Linear Algebra* (1997); R. Vershynin, *High-Dimensional
Probability* (2018).

History: H. Grassmann, *Die lineale Ausdehnungslehre* (1844); J. J. Sylvester (1850); A. Cayley, *A Memoir on the
Theory of Matrices* (1858); E. Beltrami (1873); C. Jordan (1874); E. Schmidt (1907); H. Weyl (1912); G. W. Stewart,
*On the Early History of the Singular Value Decomposition*, SIAM Review (1993).

Numerical linear algebra: A. M. Legendre (1805), C. F. Gauss (1809) on least squares; J. P. Gram (1883); A. S.
Householder, *Unitary Triangularization of a Nonsymmetric Matrix* (1958); R. von Mises and H. Pollaczek-Geiringer
(1929); C. Lanczos (1950); G. Golub and W. Kahan (1965); C. Eckart and G. Young, *Psychometrika* (1936).

Random matrices and training: E. Wigner (1955); V. Marchenko and L. Pastur (1967); A. Clauset, C. Shalizi and M.
Newman, *Power-law distributions in empirical data* (2009); C. Martin and M. Mahoney, *Heavy-Tailed Universality
Predicts Trends in Test Accuracies* (2019) and *Implicit Self-Regularization in Deep Neural Networks*, JMLR (2021);
T. Miyato et al., *Spectral Normalization for GANs* (2018); E. Hu et al., *LoRA* (2021); J. Zhao et al., *GaLore*
(ICML 2024); K. Jordan et al., *Muon* (2024); J. Bernstein and L. Newhouse, *Old Optimizer, New Norm* (2024);
O. Roy and M. Vetterli, *The effective rank* (2007).

Words: Z. Harris, *Distributional Structure* (1954); J. R. Firth (1957); S. Deerwester et al., *Indexing by Latent
Semantic Analysis* (1990); T. Mikolov et al. (2013a, b); T. Mikolov, W. Yih and G. Zweig (2013); J. Pennington,
R. Socher and C. Manning, *GloVe* (2014); O. Levy and Y. Goldberg, *Neural Word Embedding as Implicit Matrix
Factorization* (2014); O. Levy, Y. Goldberg and I. Dagan, *Improving Distributional Similarity with Lessons Learned
from Word Embeddings* (2015).

High dimensions: W. Johnson and J. Lindenstrauss (1984); S. Dasgupta and A. Gupta, *An Elementary Proof of a Theorem
of Johnson and Lindenstrauss* (2003); K. G. Larsen and J. Nelson, *Optimality of the Johnson–Lindenstrauss Lemma*
(2017); N. Elhage et al., *Toy Models of Superposition* (2022).

GPT-2's geometry: A. Radford et al., *Language Models are Unsupervised Multitask Learners* (2019); J. Mu and P.
Viswanath, *All-but-the-Top* (2018); J. Gao et al., *Representation Degeneration Problem in Training Natural
Language Generation Models* (2019); K. Ethayarajh, *How Contextual are Contextualized Word Representations?*
(2019); W. Timkey and M. van Schijndel, *All Bark and No Bite: Rogue Dimensions in Transformer Language Models*
(2021); K. Park, Y. J. Choe and V. Veitch, *The Linear Representation Hypothesis and the Geometry of Large Language
Models* (2024).

Recommendation and retrieval: J. Bennett and S. Lanning, *The Netflix Prize* (2007); Y. Koren, R. Bell and C.
Volinsky, *Matrix Factorization Techniques for Recommender Systems* (2009); A. Feuerverger, Y. He and S. Khatri,
*Statistical Significance of the Netflix Challenge* (2012); P. Covington, J. Adams and E. Sargin, *Deep Neural
Networks for YouTube Recommendations* (2016); J. Johnson, M. Douze and H. Jégou, *Billion-scale similarity search
with GPUs* (2017); X. Yi et al., *Sampling-Bias-Corrected Neural Modeling for Large Corpus Item Recommendations*
(2019); V. Karpukhin et al., *Dense Passage Retrieval* (2020).

## Problems and solutions

1. **Triangle inequality.** |a + b|² = |a|² + 2a·b + |b|² ≤ |a|² + 2|a||b| + |b|² = (|a| + |b|)², by
   Cauchy–Schwarz. Equality needs a·b = |a||b|: one vector a non-negative multiple of the other.
2. **Projections.** P² = A(AᵀA)⁻¹AᵀA(AᵀA)⁻¹Aᵀ = A(AᵀA)⁻¹Aᵀ = P, and Pᵀ = A((AᵀA)⁻¹)ᵀAᵀ = P because AᵀA is
   symmetric. For any y, Aᵀ(I − P)y = Aᵀy − AᵀA(AᵀA)⁻¹Aᵀy = 0, so (I − P)y is perpendicular to every column; and
   (I − P)² = I − 2P + P² = I − P.
3. **Rayleigh quotient near an eigenvector.** With unit v₁ ⊥ v₂ and x = v₁ + εv₂: xᵀAx = λ₁ + ε²λ₂ and xᵀx = 1 + ε²,
   so R = (λ₁ + ε²λ₂)/(1 + ε²) = λ₁ − (λ₁ − λ₂)ε²/(1 + ε²) = λ₁ − (λ₁ − λ₂)ε² + O(ε⁴). An error ε in direction moves
   R by ε²; power iteration's direction error shrinks like (λ₂/λ₁)ᵏ, so the eigenvalue's shrinks like (λ₂/λ₁)²ᵏ.
4. **Norms.** ‖A‖_F² = Σᵢⱼ aᵢⱼ² = tr(AᵀA) = tr(VΣ²Vᵀ) = tr(Σ²) = Σσᵢ². Then σ₁² ≤ Σσᵢ² ≤ rσ₁². The first bound is
   attained by rank-one matrices (uvᵀ), the second by matrices with r equal singular values (any multiple of an
   orthogonal matrix, or of a partial isometry).
5. **SGNS optimum.** ℓ(x) = a log σ(x) + b log σ(−x) has ℓ′(x) = a(1 − σ(x)) − bσ(x) = aσ(−x) − bσ(x), zero when
   σ(x)/σ(−x) = eˣ = a/b, and ℓ″ < 0 there (it is the maximum of the log-likelihood; the loss −ℓ is minimized).
   With a = #(w,c) and b = k·#(w)·P_n(c): w·c = log(#(w,c)/(#(w)P_n(c))) − log k, the PMI with the negative
   distribution as P(c), shifted by log k.
6. **Random directions.** By symmetry E[x₁²] = … = E[x_d²] and they sum to E|x|² = 1, so each is 1/d. For
   independent uniform x, y: E[x·y] = 0 and E[(x·y)²] = E[yᵀ E[xxᵀ] y] = E[yᵀ (I/d) y] = 1/d.
7. **χ² moment generating function.** For Z ~ N(0,1), E[e^{tZ²}] = ∫ e^{tz²} e^{−z²/2}/√(2π) dz = (1 − 2t)^{−1/2}
   for t < 1/2, and the k squares are independent: (1 − 2t)^{−k/2}. Markov gives P(X ≥ (1+ε)k) ≤
   e^{−tk(1+ε)}(1 − 2t)^{−k/2}; minimizing over t gives 1 − 2t = 1/(1 + ε), i.e. t = ε/(2(1 + ε)), and the bound
   ((1 + ε)e^{−ε})^{k/2}. With ln(1 + ε) ≤ ε − ε²/2 + ε³/3: ≤ exp(−k(ε²/2 − ε³/3)/2).
8. **A rank-k picture.** k(m + n + 1) < mn means k < 51,840/469 ≈ 110.5: up to k = 110 it saves space. Its error is
   (σ²_{k+1} + … + σ²_r)^{1/2}, the singular values left out, exactly, and no other rank-k matrix does better.

## 题目与解答

1. **三角不等式。** |a + b|² = |a|² + 2a·b + |b|² ≤ |a|² + 2|a||b| + |b|² = (|a| + |b|)²，用的是柯西–施瓦茨不等式。取等号要求
   a·b = |a||b|：一个向量是另一个的非负倍数。
2. **投影。** P² = A(AᵀA)⁻¹AᵀA(AᵀA)⁻¹Aᵀ = P；因为 AᵀA 对称，Pᵀ = P。对任意 y，Aᵀ(I − P)y = Aᵀy − Aᵀy = 0，所以
   (I − P)y 与每一列都垂直；并且 (I − P)² = I − 2P + P² = I − P。
3. **特征向量附近的瑞利商。** 取单位向量 v₁ ⊥ v₂，x = v₁ + εv₂：xᵀAx = λ₁ + ε²λ₂，xᵀx = 1 + ε²，所以
   R = λ₁ − (λ₁ − λ₂)ε²/(1 + ε²) = λ₁ − (λ₁ − λ₂)ε² + O(ε⁴)。方向误差 ε 只让 R 变化 ε²；幂迭代的方向误差按 (λ₂/λ₁)ᵏ
   缩小，特征值的误差就按 (λ₂/λ₁)²ᵏ 缩小。
4. **范数。** ‖A‖_F² = Σᵢⱼ aᵢⱼ² = tr(AᵀA) = tr(Σ²) = Σσᵢ²，所以 σ₁² ≤ Σσᵢ² ≤ rσ₁²。秩为一的矩阵 uvᵀ 取到左边的等号；
   r 个奇异值都相等的矩阵（正交矩阵的倍数）取到右边的等号。
5. **SGNS 的最优点。** ℓ(x) = a log σ(x) + b log σ(−x)，ℓ′(x) = aσ(−x) − bσ(x)，在 eˣ = a/b 时为零，且 ℓ″ < 0（这是对数似然的
   最大值，损失 −ℓ 的最小值）。代入 a = #(w,c)，b = k·#(w)·P_n(c)：w·c = log(#(w,c)/(#(w)P_n(c))) − log k，即以负采样分布为
   P(c) 的点互信息，平移 log k。
6. **随机方向。** 由对称性，E[x₁²] = … = E[x_d²]，它们的和是 E|x|² = 1，所以每个都是 1/d。x、y 独立且均匀时，E[x·y] = 0，
   E[(x·y)²] = E[yᵀ(I/d)y] = 1/d。
7. **χ² 的矩母函数。** Z ~ N(0,1) 时，E[e^{tZ²}] = (1 − 2t)^{−1/2}（t < 1/2），k 个独立平方相乘得 (1 − 2t)^{−k/2}。马尔可夫不等式
   给出 P(X ≥ (1+ε)k) ≤ e^{−tk(1+ε)}(1 − 2t)^{−k/2}；对 t 求最小，得 t = ε/(2(1 + ε))，界为 ((1 + ε)e^{−ε})^{k/2}；再用
   ln(1 + ε) ≤ ε − ε²/2 + ε³/3，得 ≤ exp(−k(ε²/2 − ε³/3)/2)。
8. **秩为 k 的图片。** k(m + n + 1) < mn，即 k < 51840/469 ≈ 110.5：k 不超过 110 就能省空间。误差恰好是略去的奇异值
   (σ²_{k+1} + … + σ²_r)^{1/2}，而且没有别的秩为 k 的矩阵比它更好。

## Glossary (EN | 中文)

| English | 中文 |
|---|---|
| vector, basis, coordinates | 向量，基，坐标 |
| dot product (inner product) | 点积（内积） |
| law of cosines | 余弦定理 |
| Cauchy–Schwarz inequality | 柯西–施瓦茨不等式 |
| cosine similarity | 余弦相似度 |
| tensor, axis, einsum, contraction | 张量，轴，einsum，缩并 |
| Einstein summation convention | 爱因斯坦求和约定 |
| linear map, column space, null space, rank | 线性映射，列空间，零空间，秩 |
| rank–nullity theorem | 秩–零化度定理 |
| determinant | 行列式 |
| orthogonal projection, projection matrix | 正交投影，投影矩阵 |
| least squares, normal equations | 最小二乘，正规方程 |
| Gram–Schmidt process, QR factorization, Householder reflection | 格拉姆–施密特方法，QR分解，豪斯霍尔德反射 |
| orthonormal basis | 标准正交基 |
| eigenvalue, eigenvector, characteristic polynomial | 特征值，特征向量，特征多项式 |
| spectral theorem | 谱定理 |
| Rayleigh quotient | 瑞利商 |
| principal component | 主成分 |
| power iteration, Krylov method | 幂迭代，克雷洛夫方法 |
| singular value decomposition (SVD), singular value | 奇异值分解（SVD），奇异值 |
| Eckart–Young theorem, Weyl's inequality | 埃卡特–杨定理，外尔不等式 |
| low rank, rank-one matrix | 低秩，秩一矩阵 |
| Frobenius norm, spectral norm, stable rank | 弗罗贝尼乌斯范数，谱范数，稳定秩 |
| condition number | 条件数 |
| Newton–Schulz iteration | 牛顿–舒尔茨迭代 |
| Marchenko–Pastur law, semicircle law | 马尔琴科–帕斯图尔定律，半圆律 |
| empirical spectral density, heavy tail, power-law exponent | 经验谱密度，重尾，幂律指数 |
| gradient low-rank projection (GaLore) | 梯度低秩投影（GaLore） |
| effective rank | 有效秩 |
| distributional hypothesis | 分布假说 |
| co-occurrence, pointwise mutual information (PMI), PPMI | 共现，点互信息（PMI），正点互信息（PPMI） |
| latent semantic analysis (LSA) | 潜在语义分析（LSA） |
| skip-gram with negative sampling (SGNS), word2vec, GloVe | 带负采样的跳字模型（SGNS），word2vec，GloVe |
| analogy (3CosAdd) | 类比（3CosAdd） |
| concentration of measure, thin shell | 测度集中，薄壳 |
| Johnson–Lindenstrauss lemma, random projection | 约翰逊–林登斯特劳斯引理，随机投影 |
| chi-squared distribution, Chernoff bound, union bound | 卡方分布，切尔诺夫界，联合界 |
| anisotropy, centring, all-but-the-top | 各向异性，中心化，去掉顶部方向 |
| rogue dimension | 离群维度 |
| linear representation hypothesis, superposition | 线性表示假说，叠加 |
| matrix factorization, collaborative filtering | 矩阵分解，协同过滤 |
| regularization | 正则化 |
| two-tower model, in-batch softmax, recall@k | 双塔模型，批内softmax，前k召回率 |
| maximum inner product search, approximate nearest neighbour | 最大内积搜索，近似最近邻 |
| dense retrieval | 稠密检索 |
