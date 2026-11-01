# AI, Built — Part 7: Statistical ML

Part 7 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)): models with hidden parts, which we never observe and only infer, and the
statistical era of AI, from Pearson's line of closest fit (1901) through EM (1977), IBM's statistical speech
recognition and translation, Pearl's graphs and causes, topic models (2003) and Gaussian processes (2006), to an
infinity-gram over the thirty novels (after 2024's infini-gram). It reuses Part 6's 639 pages (Austen and Dickens,
70 word rates each) and Part 1's books, and every method is written out in numpy in `compute.py`; every model that
is trained has its training replayed on screen.

Source QA preparation (2026-11-01): numerical and bilingual teaching repairs are recorded in
[the source evidence](../../../docs/qa/evidence/ai7-source-preparation/README.md). Part 7 cache generation and
rendered acceptance remain gated behind Part 6. A later source-only batch also fixes common-target KN comparisons,
Good–Turing's word-pair trial denominator, fitted GP provenance and causal assumptions; its default results are still
unknown. The numerical examples below describe the historical recipe;
they have not yet been revalidated against the revised producers. Source tests do not approve motion, narration
synchronization, listening or production-resolution output.

## Outline

* **Structure nobody labelled.** The pages along their three main directions, uncoloured; a two-component mixture
  fitted without labels recovers the authors (97% agreement). How we got here: Pearson (1901), Hotelling (1933),
  Viterbi (1967), Baum (1970), Dempster–Laird–Rubin (1977), Pearl (1988), IBM's translation (1990–93), LDA (2003),
  Rasmussen–Williams (2006). The objectives.
* **1. Principal components, two ways.** Pearson's line closest to the points and Hotelling's direction of greatest
  spread, on two standardized word rates: a line turned through every angle, the spread kept plus the squared
  distance lost always 2.00 (Pythagoras). The derivation: Lagrange, Cu = λu, spread = λ, error with k directions =
  the eigenvalues left out (46.59 of 70 at k = 5, checked for every k). The 70 × 70 covariance and its spectrum
  (12.6%, 9.1%, ...); the SVD of the data matrix (σ²/n = λ to rounding); what directions 1 and 2 weigh; one cut
  along direction 1 sorts 88% of pages.
* **2. PCA as a probability model.** Probabilistic PCA (Tipping & Bishop 1999; Roweis 1998): x = Wz + μ + ε, samples
  from the fitted model, the closed-form maximum-likelihood W and σ², PCA as σ → 0. Held-out log-likelihood on Part
  6's 191 test pages against the number of hidden directions: training always rises, held-out peaks at k = 17
  (−92.8 nats per page, against −93.1 for a full covariance). Factor analysis (Spearman 1904) → pPCA → the VAE.
* **3. The cocktail party.** Cherry (1953); two signals mixed into two microphones, x = As; whitening leaves the
  rotation undetermined; the central limit theorem and kurtosis (sources −1.51 and −1.10, whitened mixes −0.80 and
  −0.56); kurtosis against angle, FastICA's fixed point (Hyvärinen 1999) landing in 5 steps; recovered sources
  correlate 0.9992 and 0.9999 with the truth, whitening alone 0.76–0.77. Hérault & Jutten, Comon (1994), Bell &
  Sejnowski (1995, 1997), EEG artefact removal, dictionary learning.
* **4. Mixtures and EM.** A mixture of Gaussians fitted by EM on the pages' first two principal components: soft
  colours, the ellipses breathing, the log-likelihood that never falls, 97% agreement (Dempster, Laird & Rubin 1977).
  The derivation: Jensen's lower bound B(q, θ), the gap is KL(q ‖ p(z | x)), monotonicity proved. The bound drawn
  for real: along the line from round k's parameters to round k + 1's, the likelihood and the bound the E step built
  (touching at round k, peaking at round k + 1), for rounds 0, 1 and 4. k-means as hard EM (Lloyd 1957/1982,
  MacQueen 1967): 10 rounds, the objective falling, 95% agreement; responsibilities hardening as the bells shrink.
* **5. Topic models.** Latent Dirichlet allocation (Blei, Ng & Jordan 2003; after Hofmann 1999): the plate diagram
  and generative story; the thirty novels cut into 2,248 sections of 2,000 words, 3,000 content words, 12 topics fitted
  by variational EM (40 rounds, the bound rising every round); six topics taking shape; the final topics with the
  novel each is commonest in (the whaling of *Moby Dick*, the armies of *War and Peace*, ...); one section coloured
  word by word, with its mixture.
* **6. Hidden Markov models.** The chain and its emissions; a two-state model of the letters; the forward algorithm
  derived and run on "there␣" (3.2 × 10⁻⁷, equal to the sum over all 64 paths); the cost T·S² against S^T; CTC (Part
  23) runs the same recursion. Viterbi (1967): the lattice with real back-pointers, the path lighting up; Shannon's
  sentence decoded.
* **7. Baum–Welch, and machines that listen.** Forward–backward as EM's E step (γ, ξ) and the counting M step; the
  training replayed on 200,000 letters: one state takes the space and the vowels, the other every consonant, alternating
  72% of the time (Cave & Neuwirth 1980); bits per letter 4.89 → 3.96. Speech recognition with HMM–GMMs (Baker's
  DRAGON 1975; Jelinek 1976): frames, three-state phone models, Gaussian-mixture emissions, a pronunciation dictionary
  and an n-gram model; the remark attributed to Jelinek; deep networks replace the mixtures (Hinton et al. 2012).
* **8. Translation by counting.** Weaver's letter (1947) and memorandum (1949); ALPAC (1966); IBM's noisy channel
  (Brown et al. 1990, 1993) on the Canadian Hansards. IBM Model 1 trained by EM on a 20-pair French–English corpus we
  wrote: an alignment matrix sharpening round by round, the likelihood rising; 'chat' → 'cat' with probability 1.00.
  BLEU (Papineni et al. 2002), defined and computed on 6 held-out sentences: 0.76 word by word, 1.00 with one
  reordering rule; IBM Models 2–5, phrase-based translation, attention as learned soft alignment.
* **9. Kneser–Ney, from Good–Turing.** Good (1953, after Turing): r* = (r + 1) N_{r+1} / N_r and p(unseen) = N_1/N,
  tested on the novels' word pairs against the other half (Church & Gale 1991): seen once, 0.32 predicted, 0.32
  measured. The loss r − r_held is nearly constant (0.80–0.95 from r = 2): absolute discounting (Ney, Essen & Kneser
  1994). Kneser–Ney (1995): discounting and continuation counts, with the novels' own example ('cristo': 1,049 times,
  always after 'monte'; 'nor': 1,315 times after 921 different words). Character n-grams to 7 characters of context:
  2.04 bits per character on the passage (Part 1: 2.32); Chen & Goodman (1998).
* **10. The infinity-gram.** Distinct strings in the novels by length (167 … 4.5 million); the suffix array (Manber &
  Myers 1990) built by prefix doubling over all 23.7 million characters, a small one sorted on screen; a context
  grown leftward with its count falling from 4.2 million to 1 at 26 characters; longest matches over the passage
  (median 10, at most 37). The ∞-gram alone: 56% next-character accuracy, but probability 0 for the truth 32% of the
  time; mixed with Kneser–Ney by weights per match length (chosen on held-out novel text), 2.027 bits per character
  against 2.040: the scoreboard's new row. Liu et al. (2024): 5 trillion tokens, 47% next-token accuracy.
* **11. Models as pictures.** Graphical models (Pearl 1988): circles, shading, arrows, the factorized joint; the
  mixture and the HMM; a language model as a fully connected picture. d-separation: chain, fork and collider, checked
  by simulation (the sprinkler on 16% of rainy days and 38% of dry ones, 10.0% against 9.9% given clouds; rain 20%,
  45% given wet grass, 20% given wet grass and the sprinkler: explaining away). Factor graphs and belief propagation
  (Pearl 1982): messages leaves → root → leaves on a 7-variable tree, exact against all 128 states; one loop makes it
  approximate (off by 0.0007); turbo and LDPC decoding, graph neural networks.
* **12. From graphs to causes.** Simpson's paradox in the kidney-stone study (Charig et al. 1986; Julious & Mullee
  1994); the confounder, the back door, P(y | do(x)) and graph surgery; the back-door adjustment derived (open
  surgery 83% against 78%). A simulated world where the truth is known (+0.10): the naive comparison −0.11, the
  adjustment +0.099, a randomized experiment +0.101. Pearl's ladder of causation; interventions on networks (Part 30).
* **13. Gaussian processes.** The rate of "her" across *Great Expectations*: prior and posterior samples, the kernel,
  the mean and its band; the length scale (2 pages) by marginal likelihood; the band opening beyond the first 20 pages.
  Mean, kernel and noise are fitted using all pages: the initial distribution is an empirical-Bayes fitted prior,
  and the first-20-page display conditions on a subset with those settings fixed. It is not a held-out forecast.
  The band is latent-function mean ±2 conditional standard deviations, excluding observation noise and uncertainty
  in the fitted settings. Plot coordinates retain their values within an inclusive viewport.
  The posterior from Gaussian conditioning (Schur complement), step by step. The band shrinking as pages land in random
  order (average σ 6.34 → 2.60 over 186 pages). Krige (1951), Matheron, Rasmussen & Williams (2006).
* **14. Bayesian Occam's razor.** The evidence p(y | θ) = ∫ p(y | f) p(f | θ) df, its log split into data fit and
  complexity penalty; both terms against the length scale, the sum peaking at 2.1 pages. MacKay's picture (1992,
  schematic). Polynomials of degree 0–12 on 30 noisy points from a cubic: training error always falls, the evidence
  peaks at degree 3.
* **15. Bayesian optimization.** Kneser–Ney's discount D (one for every order, 5 characters of context) tuned on
  200,000 held-out characters; expected improvement derived; the GP band and EI replayed evaluation by evaluation (the
  GP's length scale chosen by marginal likelihood each step): D = 0.84 (1.8438 bits) after 8 evaluations, as good as a
  31-point grid; the discounts estimated from counts of counts give 1.8470. Mockus (1975), Jones, Schonlau & Welch
  (1998), Snoek, Larochelle & Adams (2012); AlphaGo's tuning.
* **16. Variational inference.** KL(q ‖ p) on Part 5's two bumps settles in one bump, KL(p ‖ q) covers both; the ELBO
  identity derived (EM's bound again). CAVI on a Normal–Gamma model of 25 Austen pages' rate of "the": the exact
  posterior's contours, q(μ)q(τ) converging in 2 sweeps, log p(x) = −95.334 = ELBO + KL = −95.352 + 0.018 (KL
  integrated on a grid; difference 3 × 10⁻⁷); mean field too narrow (1.51 against 1.57). The reparameterization trick
  (Kingma & Welling 2013; Rezende, Mohamed & Wierstra 2014): one-sample gradient estimates, variance 12× smaller than
  the score function's; amortized inference and the VAE (Part 20).
* **Recap** in twelve pictures, where it comes back, the problem set, Part 8's teaser, references.

Every number in the list above is computed by `compute.py` and printed on screen from the cache; a rerun on another
machine can move the last digits, and the narration, written over the data, follows in both languages.

## Run

From the repo root:

```
python tools/make.py ai7                    # everything: compute, then English and Chinese builds
python -m videos.ai.ai7.compute             # just the numbers (.cache/ai7), about 15 CPU-minutes on one core
python -m videos.ai.ai7.compute infini lda  # specific items; --force to recompute
python -m videos.ai.ai7.compute --check    # read-only cache status; missing/stale results fail
python tools/build.py ai7                   # English
python tools/build.py ai7 --lang zh         # Chinese
```

The computation requires Part 1's existing thirty novels, text and score artifacts (`.cache/ai1`) and current
Part 6 pages (`.cache/ai6`). The make command explicitly prepares the inputs needed by the requested items;
requesting only `kn` does not build the unrelated page experiments or model-backed scoreboard. Direct loaders
never download missing upstream data, and cached-only mode rejects missing, legacy or stale results before
generation. Recomputed results preserve replaced bytes; Bayesopt resumes only pieces with matching observed
source, runtime and consumed-input identities. Every random choice is seeded. The suffix array (`infini.py`) sorts 23.7 million suffixes by
prefix doubling in numpy (about a minute, under 1.5 GB of memory) and is not cached; the Bayesian optimization saves
each evaluation as it goes (`CACHE.partial`), so an interrupted run resumes. No multiprocessing, no torch.

Other parts read `load("kn")` and `load("gp")` (Parts 9, 10, 13, 31) and the functions `kn_model`, `ngram_tables` and
`kn_probs` (Part 9): they are unchanged. The scoreboard with Part 7's two rows is `load("scoreboard")`.

## References

Books: C. M. Bishop, *Pattern Recognition and Machine Learning* (2006); D. MacKay, *Information Theory, Inference, and
Learning Algorithms* (2003); C. E. Rasmussen & C. K. I. Williams, *Gaussian Processes for Machine Learning* (2006);
D. Koller & N. Friedman, *Probabilistic Graphical Models* (2009); D. Jurafsky & J. H. Martin, *Speech and Language
Processing*, 3rd ed. draft; J. Pearl, *Causality* (2000); J. Pearl & D. Mackenzie, *The Book of Why* (2018).

Papers: Pearson (1901); Spearman (1904); Hotelling (1933); Krige (1951); Cherry (1953); Good (1953); Baum & Petrie
(1966); Viterbi (1967); MacQueen (1967); Baum, Petrie, Soules & Weiss (1970); Baker (1975); Mockus (1975); Jelinek
(1976); Dempster, Laird & Rubin (1977); Cave & Neuwirth (1980); Pearl (1982, 1988, 1995); Lloyd (1982, written 1957);
Hérault & Jutten (1986); Charig et al. (1986); Rabiner (1989); Brown et al. (1990, 1993); Manber & Myers (1990);
Church & Gale (1991); MacKay (1992); Comon (1994); Julious & Mullee (1994); Ney, Essen & Kneser (1994); Kneser & Ney
(1995); Bell & Sejnowski (1995, 1997); Jones, Schonlau & Welch (1998); Chen & Goodman (1998); McEliece, MacKay & Cheng
(1998); Roweis (1998); Tipping & Bishop (1999); Hyvärinen (1999); Jordan, Ghahramani, Jaakkola & Saul (1999); Hofmann
(1999); Papineni, Roukos, Ward & Zhu (2002); Blei, Ng & Jordan (2003); Snoek, Larochelle & Adams (2012); Hinton et
al. (2012); Kingma & Welling (2013); Rezende, Mohamed & Wierstra (2014); Chen et al., *Bayesian Optimization in
AlphaGo* (2018); Liu, Min, Zettlemoyer, Choi & Hajishirzi, *Infini-gram* (2024).

## Problems and solutions

**1. Pearson's line is Hotelling's.** For centred data with covariance C and a unit vector u, show that the mean
squared distance to the line through u is tr(C) − uᵀCu, and deduce that the two lines coincide.

*Solution.* The projection of x on the line is (uᵀx)u, and x − (uᵀx)u is perpendicular to u, so by Pythagoras
‖x − (uᵀx)u‖² = ‖x‖² − (uᵀx)². Averaging, E‖x‖² = tr(C) and E(uᵀx)² = uᵀCu. The distance is a constant minus the
spread, so minimizing one maximizes the other: both are the top eigenvector of C.

**2. Probabilistic PCA.** Show that x = Wz + μ + ε, with z ~ N(0, I_k) and ε ~ N(0, σ²I) independent, has covariance
WWᵀ + σ²I, and check that W = U_k(Λ_k − σ²I)^{1/2} makes it agree with the data's covariance on the top k directions.

*Solution.* Cov(Wz) = W Cov(z) Wᵀ = WWᵀ, Cov(ε) = σ²I, and independent covariances add. With W = U_k(Λ_k − σ²I)^{1/2},
WWᵀ = U_k(Λ_k − σ²I)U_kᵀ, so for an eigenvector u_i with i ≤ k, (WWᵀ + σ²I)u_i = (λ_i − σ²)u_i + σ²u_i = λ_i u_i, the
data's own variance; in the other directions the model gives σ², the average of the discarded eigenvalues.

**3. EM never goes downhill.** Using log p(x; θ) = B(q, θ) + KL(q ‖ p(z | x; θ)), prove that one round of EM never lowers
the likelihood.

*Solution.* The E step sets q = p(z | x; θ_old), so the KL is 0 and B(q, θ_old) = log p(x; θ_old). The M step picks
θ_new to maximize B(q, ·), so B(q, θ_new) ≥ B(q, θ_old). And since KL ≥ 0 (Gibbs), log p(x; θ_new) ≥ B(q, θ_new).
Chaining: log p(x; θ_new) ≥ B(q, θ_new) ≥ B(q, θ_old) = log p(x; θ_old).

**4. The forward algorithm.** Derive α_t(j) = Σ_i α_{t−1}(i) A_ij B_j(x_t) and count its operations.

*Solution.* α_t(j) = p(x_1..x_t, z_t = j) = Σ_i p(x_1..x_{t−1}, z_{t−1} = i) p(z_t = j | z_{t−1} = i) p(x_t | z_t = j), where
the conditional independences of the chain (the next state depends only on the current one; each letter only on its
state) remove x_1..x_{t−1} from the last two factors. Each of the T steps computes S values, each a sum of S
products: O(T S²), against S^T paths for the brute-force sum.

**5. Good–Turing's singleton mass transfer.** Assume N_1 > 0. Good–Turing gives each item seen once the count 1* = 2N_2/N_1. What total
probability does it give all of them, and where did the rest of their mass go?

*Solution.* N_1 items × (2N_2/N_1) / N = 2N_2/N, exactly the share of tokens that items seen twice had. In general the
class seen r times receives the mass the class seen r + 1 times had, (r + 1)N_{r+1}/N; the class seen once gives its
mass N_1/N to the unseen items, which is Good–Turing's estimate p(unseen) = N_1/N.
Here N counts observations: for word pairs it is the number of bigram trials, not the number of words.
The class-transfer identity does not ensure that the unsmoothed estimator normalizes when frequency classes are
missing. With one type seen once and another seen three times, N=4 but N_2=N_4=0: both raw adjusted seen counts
are zero, and estimated unseen mass is only 1/4. Practical models smooth the counts of counts and normalize;
do not infer a complete probability distribution from the raw row formula alone.

**6. The back-door formula.** For Z → X, Z → Y, X → Y, derive P(y | do(x)) = Σ_z P(y | x, z) P(z).

*Solution.* Assume the stated causal graph is adequate, with no omitted confounding, consistent well-defined
interventions and overlap in treatment assignment. The joint factorizes as P(z) P(x | z) P(y | x, z). Intervening on X removes the factor for X (it no
longer listens to Z) and fixes X = x: P_do(x)(z, y) = P(z) P(y | x, z). Summing out z gives the formula. It differs from
P(y | x) = Σ_z P(y | x, z) P(z | x), which weighs the strata by how often each z occurs among those who received x.

## 习题与解答

**1. 皮尔逊的直线就是霍特林的直线。** 对协方差为 C 的中心化数据和单位向量 u，证明到过 u 的直线的平均平方距离是
tr(C) − uᵀCu，并由此推出两条直线重合。

*解答。* x 在直线上的投影是 (uᵀx)u，而 x − (uᵀx)u 与 u 垂直，所以由勾股定理 ‖x − (uᵀx)u‖² = ‖x‖² − (uᵀx)²。取平均，
E‖x‖² = tr(C)，E(uᵀx)² = uᵀCu。距离等于一个常数减去分散程度，所以让一个最小就是让另一个最大：两者都是 C 的最大特征向量。

**2. 概率PCA。** 证明当 z ~ N(0, I_k) 与 ε ~ N(0, σ²I) 独立时，x = Wz + μ + ε 的协方差是 WWᵀ + σ²I，并验证
W = U_k(Λ_k − σ²I)^{1/2} 使它在前 k 个方向上与数据的协方差一致。

*解答。* Cov(Wz) = W Cov(z) Wᵀ = WWᵀ，Cov(ε) = σ²I，独立随机量的协方差相加。取 W = U_k(Λ_k − σ²I)^{1/2}，
则 WWᵀ = U_k(Λ_k − σ²I)U_kᵀ，所以对 i ≤ k 的特征向量 u_i，(WWᵀ + σ²I)u_i = (λ_i − σ²)u_i + σ²u_i = λ_i u_i，正是数据自己的
方差；在其余方向上，模型给出 σ²，也就是被舍掉的特征值的平均。

**3. EM 永不走下坡。** 利用 log p(x; θ) = B(q, θ) + KL(q ‖ p(z | x; θ))，证明 EM 的一轮不会降低似然。

*解答。* E 步令 q = p(z | x; θ_old)，于是 KL = 0，B(q, θ_old) = log p(x; θ_old)。M 步选 θ_new 使 B(q, ·) 最大，所以
B(q, θ_new) ≥ B(q, θ_old)。又因为 KL ≥ 0（吉布斯不等式），log p(x; θ_new) ≥ B(q, θ_new)。串起来：
log p(x; θ_new) ≥ B(q, θ_new) ≥ B(q, θ_old) = log p(x; θ_old)。

**4. 前向算法。** 推导 α_t(j) = Σ_i α_{t−1}(i) A_ij B_j(x_t)，并数一数它的运算量。

*解答。* α_t(j) = p(x_1..x_t, z_t = j) = Σ_i p(x_1..x_{t−1}, z_{t−1} = i) p(z_t = j | z_{t−1} = i) p(x_t | z_t = j)，这里用了链的
条件独立性（下一个状态只依赖当前状态，每个字母只依赖它的状态），把后两个因子里的 x_1..x_{t−1} 去掉。T 步中每一步算
S 个值，每个值是 S 个乘积之和：O(T S²)，而暴力求和要遍历 S^T 条路径。

**5. Good–Turing 的单例质量转移。** 假设 N_1 > 0。Good–Turing 给每个只见过一次的东西的计数是 1* = 2N_2/N_1。它们合起来得到多少概率？
其余的概率质量去了哪里？

*解答。* N_1 个东西 × (2N_2/N_1) / N = 2N_2/N，恰好是见过两次的那一类原来占的比例。一般地，见过 r 次的那一类，得到
见过 r + 1 次那一类原有的质量 (r + 1)N_{r+1}/N；见过一次的那一类，把自己的质量 N_1/N 让给了没见过的东西，这正是
Good–Turing 的估计 p(没见过) = N_1/N。
这里 N 是观测次数：对词对来说，是二元词对的试验数，不是词数。上面的类别质量转移并不保证原始估计在计数类别缺失时归一化。
例如一种类型见过1次，另一种见过3次，N=4，但 N_2=N_4=0，两种已见类型的原始调整计数都是0，未见质量估计却只有1/4。
实际模型需要平滑计数的计数并归一化，不能只凭原始逐行公式就宣称得到了完整概率分布。

**6. 后门公式。** 对 Z → X、Z → Y、X → Y，推导 P(y | do(x)) = Σ_z P(y | x, z) P(z)。

*解答。* 假设这个因果图足以描述问题，没有遗漏混杂，干预有一致且明确的含义，而且各层里都有机会接受两种治疗。
联合分布分解为 P(z) P(x | z) P(y | x, z)。对 X 进行干预，就删掉 X 的因子（它不再听 Z 的），并固定 X = x：
P_do(x)(z, y) = P(z) P(y | x, z)。对 z 求和即得公式。它不同于 P(y | x) = Σ_z P(y | x, z) P(z | x)，后者按每个 z 在接受了 x
的人中出现的频率来给各层加权。

## Glossary (EN | 中文)

| English | 中文 |
|---|---|
| principal component analysis (PCA) | 主成分分析（PCA） |
| line of closest fit | 最佳拟合直线（最近直线） |
| covariance matrix, eigenvector, eigenvalue | 协方差矩阵，特征向量，特征值 |
| Lagrange multiplier | 拉格朗日乘子 |
| reconstruction error | 重构误差 |
| singular value decomposition (SVD) | 奇异值分解（SVD） |
| probabilistic PCA | 概率PCA |
| factor analysis | 因子分析 |
| latent variable, hidden variable | 潜变量，隐变量 |
| held-out data | 留出数据 |
| independent component analysis (ICA) | 独立成分分析（ICA） |
| cocktail party problem | 鸡尾酒会问题 |
| mixing matrix, whitening | 混合矩阵，白化 |
| kurtosis | 峰度 |
| central limit theorem | 中心极限定理 |
| FastICA, fixed point | FastICA，不动点 |
| mixture of Gaussians | 高斯混合模型 |
| expectation-maximization (EM), E step, M step | 期望最大化（EM），E步，M步 |
| responsibility (posterior) | 责任（后验概率） |
| Jensen's inequality, lower bound | 詹森不等式，下界 |
| k-means, hard assignment | k均值，硬分配 |
| topic model, latent Dirichlet allocation (LDA) | 主题模型，潜在狄利克雷分配（LDA） |
| Dirichlet distribution | 狄利克雷分布 |
| variational EM | 变分EM |
| hidden Markov model (HMM) | 隐马尔可夫模型（HMM） |
| transition probability, emission probability | 转移概率，发射概率 |
| forward algorithm, backward algorithm, forward–backward | 前向算法，后向算法，前向–后向算法 |
| lattice (trellis) | 网格 |
| Viterbi algorithm, back-pointer | 维特比算法，回溯指针 |
| Baum–Welch algorithm | 鲍姆–韦尔奇算法 |
| HMM–GMM speech recognizer | HMM–GMM语音识别器 |
| noisy channel | 有噪信道 |
| parallel corpus, alignment | 平行语料，对齐 |
| IBM Model 1, translation table | IBM模型1，翻译概率表 |
| BLEU, n-gram precision, brevity penalty | BLEU，n元精确率，长度惩罚 |
| phrase-based translation | 基于短语的翻译 |
| Good–Turing estimation, counts of counts | Good–Turing估计，计数的计数 |
| absolute discounting | 绝对折扣 |
| Kneser–Ney smoothing, continuation count | Kneser–Ney平滑，接续计数 |
| suffix array, prefix doubling, binary search | 后缀数组，前缀倍增，二分查找 |
| infini-gram (∞-gram), longest match | 无穷元模型（∞-gram），最长匹配 |
| graphical model, Bayesian network, plate | 图模型，贝叶斯网络，板 |
| d-separation; chain, fork, collider | d分离；链，叉，对撞点 |
| explaining away | 解释消除 |
| factor graph, belief propagation, message passing | 因子图，信念传播，消息传递 |
| loopy belief propagation | 有环信念传播 |
| Simpson's paradox, confounder | 辛普森悖论，混杂因子 |
| intervention, do-operator, do-calculus | 干预，do算子，do演算 |
| back-door criterion, back-door adjustment | 后门准则，后门调整 |
| ladder of causation | 因果之梯 |
| randomized experiment | 随机试验 |
| Gaussian process, kernel, length scale | 高斯过程，核函数，长度尺度 |
| Gaussian conditioning, Schur complement | 高斯条件分布，舒尔补 |
| kriging | 克里金法 |
| marginal likelihood (evidence) | 边缘似然（证据） |
| data fit, complexity penalty | 数据拟合，复杂度惩罚 |
| Bayesian Occam's razor | 贝叶斯奥卡姆剃刀 |
| Bayesian linear regression | 贝叶斯线性回归 |
| Bayesian optimization, expected improvement | 贝叶斯优化，期望改进 |
| exploration, exploitation | 探索，利用 |
| variational inference, ELBO | 变分推断，证据下界（ELBO） |
| mean field, coordinate ascent (CAVI) | 平均场，坐标上升（CAVI） |
| conjugate prior, Normal–Gamma | 共轭先验，正态–伽马分布 |
| score-function estimator, reparameterization trick | 得分函数估计量，重参数化技巧 |
| amortized inference, encoder, decoder | 摊销推断，编码器，解码器 |
