# Computer Science, Built — Part 57: Learning Theory

Part 57 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act XI, *The Research Frontier*. *AI, Built* showed machines that
learn; this part asks what can be proved about them. How many examples a learner needs is decided by one number, the
VC dimension; margins, not dimensions, govern the perceptron and boosting; against an adversary the measure is regret,
which grows like a square root; and some classes, parity among them, need little data but cannot be learned
efficiently by statistics. Every bound is set against a measurement, down to a linear model that fits its noise
exactly and still predicts well.

The instruments are in `explainer/cs/learn/` (tested in `tests/test_cs57_learning.py`):
* `theory.py`: shattering by half-planes, every labelling checked by a feasibility linear program (SciPy's HiGHS);
  the growth function of half-planes on random points (counted labelling by labelling up to m = 10, the
  general-position count m² − m + 2 beyond) against 2^m and the Sauer–Shelah sum; PAC learning curves for an
  axis-aligned rectangle learned by the tightest box (200 trials at each of eight sample sizes) against
  (4/m) ln(4/δ) and the VC bound with d = 4; the finite-class sample bound; the perceptron on separable data with
  margin 0.1 on the unit sphere in 2 to 1,000 dimensions; AdaBoost with decision stumps on a ring, without and with 5%
  label noise (training and test error per round, margins, example weights); Hedge and follow the leader against
  twenty experts; the halving algorithm over 1,024 thresholds; ε-greedy, UCB1 and Thompson sampling on four Bernoulli
  arms against the Lai–Robbins rate; sparse parity, subset search against Gaussian elimination over GF(2); double
  descent of ridgeless least squares on Gaussian features; and a size-4 sample compression scheme for rectangles.
  (The scenes' illustrative pictures, such as the sixteen hypotheses of the agnostic bound, thresholds fitting random
  signs, the boosting game, weighted majority, follow the leader against an adversary, the random walks of the lower
  bound, online gradient descent, the UCB run, the Thompson posteriors, the statistical-query grid and the
  two-parameter plane of the minimum-norm interpolator, are computed inline with NumPy.)

## Chapters

* **Hook.** Double descent: fifty noisy examples, a linear model on the first p of 200 Gaussian features
  (minimum-norm least squares, median of 50 trials). Test error is 1.03 at p = 5, explodes to 52.1 at p = n = 50,
  where the model can fit anything, noise included, and falls to 0.78 at p = 200, lower than any model with fewer
  parameters than examples. Three questions and three kinds of answer: PAC learning and the VC dimension (Valiant
  1984); regret and the bandits of Part 44 when an adversary picks the examples; cryptography and statistical queries
  for what cannot be learned efficiently. The plan.
* **1. Probably approximately correct.** The learning game on twelve points and a hidden rectangle
  [0.2, 0.7] × [0.3, 0.75]: an unknown distribution D, a target c, the error L_D(h), and Valiant's ε–δ definition.
  The finite class by the union bound (Part 2): m ≥ (ln|H| + ln 1/δ)/ε, 199 examples for |H| = 1,000 and
  ε = δ = 0.05. The agnostic case by Hoeffding (Part 20) and a union bound: ln(2|H|/δ)/(2ε²) = 2,120 examples for the
  same class, the best on the sample within 2ε of the best in the class (sixteen illustrative hypotheses at m = 40 and
  800). Rectangles by four strips of probability ε/4 (Kearns and Vazirani's opening argument): m ≥ (4/ε) ln(4/δ), with
  no class size. Measured over 200 trials at eight sample sizes from 10 to 2,000: the mean error falls like 1/m, and
  from m = 100 on the bound is 2.2 to 2.6 times the 95th percentile. What replaces ln|H|: ten points have 1,024
  labellings, half-planes realize 92 of them.
* **2. VC dimension.** Shattering: three points, all 8 labellings separable, each checked by a linear program. No
  four points: at the corners of a square 14 of 16 labellings are separable, and with one point inside a triangle
  also 14 of 16; Radon's theorem (1921) covers every case, so half-planes have VC dimension 3, half-spaces in ℝ^d
  d + 1, axis-aligned rectangles 4. The growth function up to m = 10: 2^m reaches 1,024, half-planes give 92 =
  m² − m + 2, the Sauer–Shelah sum Σ_{i≤3} C(m, i) gives 176. Sauer–Shelah proved by induction on the square's
  fourteen labellings, 14 = 8 + 6, with (em/d)^d for m ≥ d. The ghost-sample bound
  ε ≤ (2/m)(d log₂(2em/d) + log₂(2/δ)): for rectangles at m = 2,000 it gives 0.051 against a measured 0.0040, 13×
  loose, knowing only d. The fundamental theorem of PAC learning (four equivalent conditions; sample sizes of order
  d/ε realizable and d/ε² agnostic, Shalev-Shwartz and Ben-David's Theorem 6.8; Blumer et al. 1989) and the no free
  lunch converse: error at least 1/8 with probability at least 1/7.
* **3. Margins and Rademacher complexity.** Rosenblatt's perceptron on illustrative separable points; Novikoff's
  proof by two inequalities, kγ ≤ w_k · w* ≤ ‖w_k‖ ≤ √k R, so at most (R/γ)² mistakes: 100 for R = 1, γ = 0.1.
  Measured on 2,000 points with margin 0.1 in 2, 10, 100 and 1,000 dimensions: 4, 23, 38 and 34 mistakes, flat from a
  hundred dimensions to a thousand, while the VC dimension grows with d; Part 7's perceptron branch predictor runs
  the same update, but branch histories are rarely separable. Rademacher complexity as the fit to random signs
  (thresholds on ten points, illustrative); the bound of Bartlett and Mendelson (2002) and Massart's lemma back to VC
  bounds. For linear classes with ‖w‖ ≤ Λ, five lines give ΛR/√m with no dimension; the margin bound of Koltchinskii
  and Panchenko (2002), where (R/ρ)² plays the part of a dimension; support vector machines.
* **4. Boosting.** 400 points, green inside radius 0.6; decision stumps. With equal weights the best stump says
  "outside" everywhere (error 0.285, the share of green points); re-weighted, the next cuts at x₁ = 0.60 with
  weighted error 0.33, an edge of about 0.17; weak learning implies strong (Schapire 1990). AdaBoost's weights after
  1, 2, 5 and 20 rounds pile up on the circle, the heaviest point at about 4.5 times its first share. The training
  error is at most exp(−2Σγ_t²): first zero at round 57, zero for good from round 108. Boosting as a zero-sum game
  (an illustrative 8 × 8 matrix), von Neumann's minimax theorem and Part 23's multiplicative weights. After zero
  training error the test error does not rise: 0.030 at round 108, 0.028 at round 125, 0.032 at round 300, while the
  smallest training margin climbs from −0.572 (round 5) and −0.088 (round 20) to +0.012 (round 100) and +0.023
  (round 300); the margin theorem of Schapire, Freund, Bartlett and Lee (1998). With 5% of labels flipped, the 23
  flipped points (5.8% of the data) hold 18% of the weight by round 20, and test error is lowest, 0.107, at round 27
  and 0.130 by round 300: stop early, shrink the votes, or use gradient boosting (Friedman 2001).
* **5. Learning online.** The halving algorithm: at most log₂ 1,024 = 10 mistakes; on random examples it made 2 in
  200 rounds with 9 thresholds still alive, and an adversary asking about the middle forces all 10; the Littlestone
  dimension (infinite for thresholds on the line, whose VC dimension is 1). Weighted majority (Littlestone and Warmuth
  1994): M ≤ 2.41(m + log₂ N) (eight illustrative experts). Hedge proved, from below and from above with Hoeffding's
  lemma, regret at most √(T ln N / 2). Measured against 20 experts over 2,000 rounds (η = 0.109): the guarantee
  reaches 54.7, Hedge's regret flattens at 30.7, and follow the leader does better on these random losses (9.0) but
  loses almost every round to two alternating experts (after six rounds A 2.5, B 3, the leader 5.5). The lower bound:
  two experts and a fair coin give regret about √(T/2π) ≈ 0.4√T, and with N experts Hedge's constant cannot be
  improved. Online gradient descent (Zinkevich 2003): regret D G √T, and online-to-batch conversion.
* **6. Bandits.** Four Bernoulli arms paying 0.5, 0.45, 0.4 and 0.3 (gaps 0.05, 0.10, 0.20); regret as the gaps times
  the pulls; Part 44's A/B test as explore-then-commit. UCB: the index μ̂_i + √(2 ln t / n_i), wrong with probability
  at most t⁻⁴ by Hoeffding (an illustrative run). UCB1's bound (Auer, Cesa-Bianchi and Fischer 2002),
  Σ 8 ln T/Δ_i + (1 + π²/3)ΣΔ_i: 2,386 at T = 5,000 against a measured 159. Thompson sampling (1933) from beta
  posteriors, probability matching. Measured over 100 runs of 5,000 rounds: ε-greedy (ε = 0.05) 75.1, UCB1 158.8,
  Thompson 49.7, against the Lai–Robbins rate 17.4 ln T (KL from *AI, Built* 1): UCB1 above it, Thompson below it at
  this T, which the asymptotic theorem allows. Why nobody does better: two worlds, 0.45 against 0.5, separated only
  as fast as e^{−n KL}; and an adversarial gap of √(K/T) forces regret of order √(KT).
* **7. What cannot be learned.** Circuits of size s need only O((s log s + ln 1/δ)/ε) examples; time is the limit.
  Finding a consistent 3-term DNF is NP-hard (Pitt and Valiant 1988), but the same function as a 3-CNF is learned by
  Valiant's elimination. A learner would be a code-breaker: if RSA or factoring is hard, small Boolean formulas and
  finite automata cannot be learned efficiently whatever the hypothesis (Kearns and Valiant 1994); pseudorandom
  functions (Goldreich, Goldwasser and Micali 1986; Part 29) rule out small circuits even with queries. Statistical
  queries cannot find a parity: different parities are orthogonal, and by Bessel's inequality a query of tolerance
  τ = 0.25 is informative about at most 16 of the C(10, 3) = 120 candidate sets, so at least τ² C(n, k) queries. Measured
  on 400 examples with k = 3 and n = 10, 14, 18, 22: the best single bit correlates 0.080, 0.115, 0.155 and 0.090 with
  the label; the subset search tried 113 of 120, 206 of 364, 515 of 816 and 1,508 of 1,540 sets; elimination over
  GF(2) from 2n examples found every set (on this machine, search 1.3 to 15.2 ms against elimination 0.25 to 0.75 ms).
  Learning parity with noise and Blum, Kalai and Wasserman's 2^{O(n/log n)}; Part 7's parity branch (the perceptron
  predictor 49% right). The landscape: finite VC dimension, polynomial time, statistical queries, and the SQ dimension
  (Blum et al. 1994).
* **8. More parameters than data.** Both errors of the hook's experiment (noise 0.5): training error is zero up to
  rounding (below 10⁻²⁸) from p = 50 on; test error 1.03 at p = 5, 52.1 at the threshold, 0.78 at p = 200; double
  descent (Belkin, Hsu, Ma and Mandal 2019). A class that fits every labelling has Rademacher complexity 1 and a
  vacuous bound; Zhang, Bengio, Hardt, Recht and Vinyals (2017) fitted CIFAR-10's random labels. The minimum-norm
  interpolator in a plane of two parameters, X⁺y = Xᵀ(XXᵀ)⁻¹y; gradient descent from zero stays in the row space and
  finds it, an implicit bias (*AI, Built* 8), and on separable data with the logistic loss heads for the maximum
  margin (Soudry et al. 2018). Why the peak: the noise term is σ̃² p/(n − p − 1) below the threshold and
  σ̃² n/(p − n − 1) above it (inverse Wishart means), with the unseen features as extra noise; the formula's curves
  against the measured medians; Part 52's ill-conditioning at p = n.
* **9. Learning is compression.** Occam's razor as a theorem (Kraft's inequality and a failure budget shared by code
  length; Blumer et al. 1987): ε_h = (|h| ln 2 + ln 1/δ)/m. A compression scheme of size 4 on 200 points: the four
  extreme positives rebuild a box that labels every point correctly; Littlestone and Warmuth's bound
  (k ln m + ln 1/δ)/(m − k) = 0.123, against a true error of 0.0173, the rectangle bound's 0.088 and the VC bound's
  0.377 at m = 200. The perceptron is a compression scheme of size its mistakes: on 2,000 points the bound is 0.017,
  0.090, 0.149 and 0.133 for d = 2, 10, 100 and 1,000, where no VC bound says anything. Minimum description length
  (Rissanen 1978): the 200 labels cost 200 bits raw, 146.4 bits entropy-coded (41 positive), 30.6 bits as four
  indices, and Occam's bound on those 30.6 bits is 0.121; Part 21's compressors. One shape, four measures:
  complexity times a logarithm over m.
* **10. Frontier: compression schemes and in-context learning.** The four kept points again; Warmuth's conjecture
  (2003) of schemes of size O(d), and Moran and Yehudayoff's (2016) schemes of size 2^{O(d)}. In-context learning:
  Garg et al. (2022) on transformers that match least squares in their prompts; what theory lacks; benign overfitting
  (Bartlett et al. 2020), understood for linear models. Four open problems (non-vacuous bounds for deep networks,
  in-context learning, learning parity with noise, structured bandits) and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs57.compute
python -m unittest tests.test_cs57_learning
python tools/build.py cs57
```

## Problems, with solutions

1. **VC dimension.** Show that half-planes in the plane have VC dimension 3, and axis-aligned rectangles have VC
   dimension 4.

   *Solution.* A lower bound needs one shattered set; an upper bound must defeat every set. Half-planes, at least 3:
   take three points not on a line. If all three get one label, a line missing their triangle does it; otherwise one
   point is the odd one out, it is a vertex of the triangle, and a line crossing the two edges at that vertex cuts it
   off. All 8 labellings are realized (our instrument checks each by a linear program on (0, 0), (2, 0.3),
   (0.8, 1.8)). At most 3: by Radon's theorem any four points in the plane split into two groups whose convex hulls
   meet: either one point lies in the triangle of the other three, or the four are in convex position and the two
   diagonals cross (three collinear points are a degenerate case of the first, the middle point lying in the segment
   of the other two). Label one group +1 and the other −1. A half-plane and its complement are convex, so one would
   contain the hull of the +1 group and the other the hull of the −1 group, which meet: impossible. On the square's
   corners 14 of the 16 labellings are separable, and the two failures colour opposite corners alike. Rectangles, at
   least 4: take the diamond (1, 0), (0, 1), (−1, 0), (0, −1). For any subset, the bounding box of the subset (or an
   empty box away from the points) contains none of the others, since each point is the unique extreme one in its own
   direction. At most 4: among five points pick a leftmost, a rightmost, a lowest and a highest one; that is at most
   four points, so some fifth point remains, and its coordinates lie between the extremes. Label the chosen points +1
   and the fifth −1: any rectangle containing the chosen points contains their bounding box, hence the fifth point.

2. **Sauer–Shelah.** Prove the Sauer–Shelah lemma by induction on m + d.

   *Solution.* Write Φ_d(m) = Σ_{i=0}^{d} C(m, i); the claim is that a class of VC dimension at most d realizes at
   most Φ_d(m) labellings on any m points. Base cases: if d = 0, two different labellings of S differ at some point x
   and the class would shatter {x}, so at most 1 = Φ_0(m); if m = 0, there is one (empty) labelling and
   Φ_d(0) = 1. Step: let S = {x_1, …, x_m}, S′ = S \ {x_m}, and H_S the labellings of S. Let H₁ be the labellings of S′
   that extend to some labelling in H_S, and H₂ those that extend in both ways. Each labelling in H_S is a row of H₁
   with one label for x_m, and the rows in H₂ appear twice, so |H_S| = |H₁| + |H₂|. H₁ is a class on m − 1 points with
   VC dimension at most d. H₂ has VC dimension at most d − 1: if it shattered T ⊆ S′, every labelling of T would come
   with both labels of x_m, and H_S would shatter T ∪ {x_m}, of size |T| + 1 ≤ d. Both cases have smaller m + d, so
   |H_S| ≤ Φ_d(m − 1) + Φ_{d−1}(m − 1) = Σ_{i≤d} [C(m − 1, i) + C(m − 1, i − 1)] = Σ_{i≤d} C(m, i) by Pascal's rule.
   On the square's corners: H₁ has 8 rows (at most Φ_3(3) = 8), H₂ has 6 (at most Φ_2(3) = 7), and 14 ≤ 15 = Φ_3(4).
   For m ≥ d, (d/m)^d Φ_d(m) ≤ Σ_{i≤d} C(m, i)(d/m)^i ≤ (1 + d/m)^m ≤ e^d, so Φ_d(m) ≤ (em/d)^d: for half-planes
   on ten points, 92 ≤ 176 ≤ 744, against 2^10 = 1,024.

3. **Novikoff's bound.** Prove that the perceptron makes at most (R/γ)² mistakes on separable data.

   *Solution.* Assume ‖x_i‖ ≤ R for all i and a unit vector w* with y_i w* · x_i ≥ γ > 0 (a bias is absorbed by an
   extra constant coordinate, at the cost of a larger R). Start from w_0 = 0 and let w_k be the weights after the k-th
   mistake, whatever the order of the examples and however many passes. Progress: a mistake on (x, y) sets
   w_{k+1} = w_k + yx, so w_{k+1} · w* = w_k · w* + y x · w* ≥ w_k · w* + γ, and by induction w_k · w* ≥ kγ. Length:
   ‖w_{k+1}‖² = ‖w_k‖² + 2y w_k · x + ‖x‖² ≤ ‖w_k‖² + R², because on a mistake y w_k · x ≤ 0; so ‖w_k‖² ≤ kR².
   By Cauchy–Schwarz with ‖w*‖ = 1, kγ ≤ w_k · w* ≤ ‖w_k‖ ≤ √k R, hence √k ≤ R/γ and k ≤ (R/γ)². The bound
   contains no dimension and no number of examples. With R = 1 and γ = 0.1 it is 100; our instrument's runs on 2,000
   points made 4, 23, 38 and 34 mistakes in 2, 10, 100 and 1,000 dimensions.

4. **Hedge.** Show that Hedge with the right learning rate has regret at most √((T/2) ln N).

   *Solution.* Hedge keeps weights w_1(i) = 1, plays p_t(i) = w_t(i)/W_t and updates w_{t+1}(i) = w_t(i) e^{−η ℓ_t(i)}
   with losses ℓ_t(i) ∈ [0, 1]; the regret is Σ_t p_t · ℓ_t − min_i L_i, with L_i = Σ_t ℓ_t(i). From below: for every
   i, W_{T+1} ≥ w_{T+1}(i) = e^{−η L_i} and W_1 = N, so ln(W_{T+1}/W_1) ≥ −η L_i − ln N. From above:
   W_{t+1}/W_t = Σ_i p_t(i) e^{−η ℓ_t(i)} = E[e^{−ηX}] for X = ℓ_t(I), I ~ p_t, a variable in [0, 1]; Hoeffding's
   lemma gives ln E[e^{−ηX}] ≤ −η E[X] + η²/8 = −η p_t · ℓ_t + η²/8. The logarithms telescope over the T rounds:
   ln(W_{T+1}/W_1) ≤ −η Σ_t p_t · ℓ_t + η²T/8. Combining, Σ_t p_t · ℓ_t − L_i ≤ ln N/η + ηT/8 for every i. The right
   side is smallest at η = √(8 ln N/T), where both terms equal √(T ln N/8) and the sum is √(T ln N/2). The argument
   never assumed the losses were random, so it holds against any sequence chosen before each round's play is revealed.
   For N = 20 and T = 2,000: η = 0.109, ln N/η = ηT/8 = 27.4, and the guarantee is 54.7; our run's regret was 30.7.
   If T is not known in advance, the doubling trick restarts with T = 1, 2, 4, … at the cost of a constant factor.

5. **Build.** Implement UCB1 and Thompson sampling for Bernoulli arms, and compare their regret with the Lai–Robbins
   rate.

   *Solution notes.* Keep, per arm, the pull count n_i and the reward sum s_i. UCB1 pulls each arm once, then the arm
   maximizing s_i/n_i + √(2 ln t / n_i); Thompson sampling draws θ_i ~ Beta(s_i + 1, n_i − s_i + 1) for every arm and
   pulls the largest. Record the pseudo-regret Σ_t (μ* − μ_{a_t}), which has far less variance than realized rewards,
   and average over runs; drawing one T × K table of rewards per run and giving it to every algorithm (common random
   numbers, as `bandits` in `explainer/cs/learn/theory.py` does) makes the comparison sharper. The Lai–Robbins
   constant is Σ_i Δ_i / KL(μ_i, μ*) with KL(p, q) = p ln(p/q) + (1 − p) ln((1 − p)/(1 − q)). For our arms
   (0.5, 0.45, 0.4, 0.3) the three terms are 9.98, 4.97 and 2.43, so 17.38 ln T, 148.0 at T = 5,000; by Pinsker,
   KL ≥ 2Δ², so the constant is at most Σ 1/(2Δ_i) = 17.5, nearly tight for coins near a half. Over 100 runs of 5,000
   rounds our instrument measures UCB1 158.8, Thompson 49.7 and ε-greedy (ε = 0.05) 75.1. Plot regret against ln t:
   the theorem is about slopes. A bad arm stops being pulled once √(2 ln t / n_i) < Δ_i, that is after about
   2 ln t/Δ_i² pulls, so UCB1's slope should approach Σ 2/Δ_i = 70, four times the optimum; a fit to the cached curve
   over t ≥ 1,000 gives 68.2. Thompson's fitted slope is 13.3, still below 17.4 at this horizon, which the asymptotic
   theorem allows; ε-greedy's regret is linear. Check against UCB1's finite-time bound (2,386 here), test that the
   best arm gets most pulls, and as an extension add KL-UCB, whose index uses the KL divergence itself and meets the
   Lai–Robbins constant (Garivier and Cappé 2011).

6. **★ Research.** The sample compression conjecture: does every concept class of VC dimension d have a compression
   scheme of size O(d)?

   *Discussion.* Open. Littlestone and Warmuth (1986) showed that a scheme of size k gives a PAC bound like VC
   dimension k (chapter 9's (k ln m + ln 1/δ)/(m − k)), and asked for the converse; Floyd and Warmuth (1995) built
   schemes of size d for maximum classes, and Warmuth posed the general question as an open problem in 2003. The
   difficulty is that a scheme is a single global object: one reconstruction function must work for every sample of
   every size, while VC theory only counts behaviours. Moran and Yehudayoff (2016) proved that a scheme of size
   exponential in d always exists, by compressing to a few small subsamples on which a boosted vote of ERM
   hypotheses is consistent (the minimax argument of chapter 4); the exponential enters through the dual VC
   dimension, which can be about 2^d. Rectangles (size 4 = d) and half-spaces (the at most n + 1 support vectors of
   the maximum-margin separator, d = n + 1) show the conjecture's bound is natural. A good partial answer would
   reduce 2^{O(d)} to a polynomial in d, prove size O(d) for a broad family (classes of small VC dimension, or
   geometric classes), or exhibit classes forcing size above d, with an exact search for schemes on small finite
   classes (a SAT encoding solved by Part 26's CDCL solver) to test conjectured constants.

## 习题与解答

1. **VC维。** 证明平面上的半平面的 VC维为 3，轴对齐矩形的 VC维为 4。

   *解答。* 下界只需一个被打散的集合；上界必须击败每一个集合。半平面至少为 3：取三个不共线的点。若三点标签相同，取一条不碰
   它们所成三角形的直线即可；否则有一个点与众不同，它是三角形的一个顶点，一条穿过该顶点处两条边的直线就把它切开。8 种标注全部
   可以实现（我们的工具对 (0, 0)、(2, 0.3)、(0.8, 1.8) 逐一用线性规划检查）。至多为 3：由 Radon 定理，平面上任意四点都能分成
   两组，使两组的凸包相交：要么一个点落在另外三点的三角形内，要么四点处于凸位置而两条对角线相交（三点共线是前一种情形的退化，
   中间的点落在另两点的线段上）。把一组标为 +1，另一组标为 −1。半平面和它的补集都是凸的，于是一个要包含 +1 组的凸包，另一个要
   包含 −1 组的凸包，而这两个凸包相交：不可能。在正方形的四个角上，16 种标注中有 14 种可分，失败的两种都把相对的两个角标成同色。
   矩形至少为 4：取菱形上的四点 (1, 0)、(0, 1)、(−1, 0)、(0, −1)。对任意子集，子集的包围盒（或远离这些点的一个空盒子）不含其余
   任何点，因为每个点都是它自己那个方向上唯一的极端点。至多为 4：在五个点中选出最左、最右、最低、最高的点各一个；这至多是四个
   点，所以还剩下第五个点，而它的坐标落在这些极值之间。把选出的点标为 +1、第五个点标为 −1：任何包含选出各点的矩形都包含它们的
   包围盒，因而也包含第五个点。

2. **绍尔–谢拉引理。** 对 m + d 归纳，证明 Sauer–Shelah 引理。

   *解答。* 记 Φ_d(m) = Σ_{i=0}^{d} C(m, i)；要证 VC维至多为 d 的类在任意 m 个点上至多实现 Φ_d(m) 种标注。基础情形：若 d = 0，
   S 的两种不同标注在某点 x 上不同，类就会打散 {x}，所以至多 1 = Φ_0(m) 种；若 m = 0，只有一种（空的）标注，而 Φ_d(0) = 1。
   归纳步：设 S = {x_1, …, x_m}，S′ = S \ {x_m}，H_S 为 S 上实现的标注。令 H₁ 为 S′ 上能扩展成 H_S 中某个标注的标注，H₂ 为能以
   两种方式扩展的那些。H_S 中每个标注都是 H₁ 的一行配上 x_m 的一个标签，而 H₂ 中的行出现两次，所以 |H_S| = |H₁| + |H₂|。H₁ 是
   m − 1 个点上 VC维至多为 d 的类。H₂ 的 VC维至多为 d − 1：若它打散 T ⊆ S′，则 T 的每种标注都同时配有 x_m 的两种标签，H_S 就会
   打散 T ∪ {x_m}，其大小 |T| + 1 ≤ d。两种情形的 m + d 都更小，所以
   |H_S| ≤ Φ_d(m − 1) + Φ_{d−1}(m − 1) = Σ_{i≤d} [C(m − 1, i) + C(m − 1, i − 1)] = Σ_{i≤d} C(m, i)，最后一步是帕斯卡法则
   （杨辉三角的递推）。在正方形的四个角上：H₁ 有 8 行（至多 Φ_3(3) = 8），H₂ 有 6 行（至多 Φ_2(3) = 7），14 ≤ 15 = Φ_3(4)。
   当 m ≥ d 时，(d/m)^d Φ_d(m) ≤ Σ_{i≤d} C(m, i)(d/m)^i ≤ (1 + d/m)^m ≤ e^d，所以 Φ_d(m) ≤ (em/d)^d：半平面在十个点上，
   92 ≤ 176 ≤ 744，而 2^10 = 1024。

3. **诺维科夫界。** 证明感知机在可分数据上至多犯 (R/γ)² 次错误。

   *解答。* 设对所有 i 有 ‖x_i‖ ≤ R，且存在单位向量 w* 使 y_i w* · x_i ≥ γ > 0（偏置可以用一个额外的常数坐标吸收，代价是 R 变大）。
   从 w_0 = 0 出发，令 w_k 为第 k 次错误之后的权重，无论样本的顺序如何、扫描多少遍。进展：在 (x, y) 上犯错时 w_{k+1} = w_k + yx，
   所以 w_{k+1} · w* = w_k · w* + y x · w* ≥ w_k · w* + γ，归纳得 w_k · w* ≥ kγ。长度：‖w_{k+1}‖² = ‖w_k‖² + 2y w_k · x + ‖x‖²
   ≤ ‖w_k‖² + R²，因为犯错时 y w_k · x ≤ 0；所以 ‖w_k‖² ≤ kR²。由 Cauchy–Schwarz 不等式及 ‖w*‖ = 1，
   kγ ≤ w_k · w* ≤ ‖w_k‖ ≤ √k R，因此 √k ≤ R/γ，k ≤ (R/γ)²。这个界里既没有维数，也没有样本个数。R = 1、γ = 0.1 时它是 100；
   我们的工具在 2000 个点上运行，在 2、10、100 和 1000 维中分别犯了 4、23、38 和 34 次错误。

4. **Hedge。** 证明取合适学习率的 Hedge 算法遗憾至多为 √((T/2) ln N)。

   *解答。* Hedge 从权重 w_1(i) = 1 开始，按 p_t(i) = w_t(i)/W_t 出招，并更新 w_{t+1}(i) = w_t(i) e^{−η ℓ_t(i)}，损失
   ℓ_t(i) ∈ [0, 1]；遗憾为 Σ_t p_t · ℓ_t − min_i L_i，其中 L_i = Σ_t ℓ_t(i)。从下方：对每个 i，W_{T+1} ≥ w_{T+1}(i) = e^{−η L_i}，
   且 W_1 = N，所以 ln(W_{T+1}/W_1) ≥ −η L_i − ln N。从上方：W_{t+1}/W_t = Σ_i p_t(i) e^{−η ℓ_t(i)} = E[e^{−ηX}]，其中
   X = ℓ_t(I)，I ~ p_t，是 [0, 1] 中的随机变量；霍夫丁引理给出 ln E[e^{−ηX}] ≤ −η E[X] + η²/8 = −η p_t · ℓ_t + η²/8。对 T 轮
   求和，对数逐项相消：ln(W_{T+1}/W_1) ≤ −η Σ_t p_t · ℓ_t + η²T/8。两者合起来，对每个 i 有 Σ_t p_t · ℓ_t − L_i ≤ ln N/η + ηT/8。
   右边在 η = √(8 ln N/T) 时最小，此时两项都等于 √(T ln N/8)，和为 √(T ln N/2)。论证从未假设损失是随机的，所以只要每轮的损失在
   出招揭晓之前选定，它对任何序列都成立。N = 20、T = 2000 时：η = 0.109，ln N/η = ηT/8 = 27.4，保证为 54.7；我们实测的遗憾为
   30.7。若事先不知道 T，加倍技巧依次取 T = 1, 2, 4, … 重新开始，只损失一个常数因子。

5. **动手。** 为伯努利拉杆实现 UCB1 和汤普森采样，并把它们的遗憾与 Lai–Robbins 速率比较。

   *解答要点。* 对每个拉杆记下拉动次数 n_i 和奖励之和 s_i。UCB1 先把每个拉杆各拉一次，之后拉使 s_i/n_i + √(2 ln t / n_i) 最大的
   拉杆；汤普森采样对每个拉杆抽 θ_i ~ Beta(s_i + 1, n_i − s_i + 1)，拉最大的那个。记录伪遗憾 Σ_t (μ* − μ_{a_t})，它的方差远小于实际
   奖励，再对多次运行取平均；每次运行抽一张 T × K 的奖励表并交给每个算法共用（共同随机数，正如 `explainer/cs/learn/theory.py`
   中的 `bandits` 所做），比较会更清楚。Lai–Robbins 常数为 Σ_i Δ_i / KL(μ_i, μ*)，其中
   KL(p, q) = p ln(p/q) + (1 − p) ln((1 − p)/(1 − q))。对我们的拉杆 (0.5, 0.45, 0.4, 0.3)，三项分别为 9.98、4.97 和 2.43，合计
   17.38 ln T，T = 5000 时为 148.0；由 Pinsker 不等式 KL ≥ 2Δ²，所以这个常数至多为 Σ 1/(2Δ_i) = 17.5，对接近一半的硬币几乎是
   紧的。我们的工具在 100 次、每次 5000 轮的运行中测得 UCB1 158.8，汤普森采样 49.7，ε-贪心（ε = 0.05）75.1。把遗憾画成 ln t 的
   函数：定理说的是斜率。一旦 √(2 ln t / n_i) < Δ_i，坏拉杆就不再被拉，也就是大约 2 ln t/Δ_i² 次之后，所以 UCB1 的斜率应趋于
   Σ 2/Δ_i = 70，是最优值的四倍；对缓存曲线在 t ≥ 1000 上拟合得 68.2。汤普森采样拟合的斜率为 13.3，在这个时长上仍低于 17.4，渐近
   定理允许这样；ε-贪心的遗憾是线性的。再与 UCB1 的有限时间界（这里为 2386）对照，测试最优拉杆得到的拉动最多；作为扩展，加上
   KL-UCB，它的指标直接用 KL散度，能达到 Lai–Robbins 常数（Garivier 与 Cappé，2011）。

6. **★ 研究。** 样本压缩猜想：是否每个 VC维为 d 的概念类都有大小为 O(d) 的压缩方案？

   *讨论。* 尚未解决。Littlestone 与 Warmuth（1986）证明了大小为 k 的方案给出与 VC维 k 相仿的 PAC 界（第 9 章的
   (k ln m + ln 1/δ)/(m − k)），并问逆命题是否成立；Floyd 与 Warmuth（1995）为极大类构造了大小为 d 的方案，Warmuth 在 2003 年把
   一般问题作为公开问题提出。难点在于方案是一个整体的对象：同一个重建函数必须对每种大小的每个样本都有效，而 VC 理论只是在数行为。
   Moran 与 Yehudayoff（2016）证明了大小随 d 指数增长的方案总是存在，办法是压缩成几个小的子样本，使在其上训练的 ERM 假设经提升法
   投票后与整个样本一致（第 4 章的极小极大论证）；指数来自对偶 VC维，它可以达到约 2^d。矩形（大小 4 = d）和半空间（最大间隔分隔面
   的至多 n + 1 个支持向量，d = n + 1）说明猜想中的界是自然的。好的部分答案可以是：把 2^{O(d)} 降到 d 的多项式；对一大族类（VC维
   很小的类，或几何类）证明大小 O(d)；或者给出迫使方案大小超过 d 的类，并在小的有限类上精确搜索方案（用 SAT 编码，交给第 26 部分
   的 CDCL 求解器）来检验猜测的常数。

## Glossary additions

* **PAC learning, realizable and agnostic, empirical risk minimization (ERM), sample complexity** — error at most ε
  with probability 1 − δ; a perfect hypothesis exists or not; returning the hypothesis best on the sample; how many
  examples a guarantee needs.
* **union bound, Hoeffding's inequality and lemma** — the tools behind every finite-class bound and the Hedge proof.
* **shattering, VC dimension, growth function, Sauer–Shelah lemma, ghost sample** — realizing every labelling; the
  largest set shattered; the most labellings on m points; its polynomial bound; the symmetrization behind the VC
  bound.
* **Radon's theorem** — any d + 2 points in ℝ^d split into two groups whose convex hulls meet.
* **fundamental theorem of PAC learning, no free lunch** — finite VC dimension if and only if learnable; a shattered
  set the learner has half seen forces error.
* **margin, perceptron, Novikoff's bound** — the distance of the data from a separator; the mistake-driven linear
  learner; at most (R/γ)² mistakes.
* **Rademacher complexity, Massart's lemma, margin bound** — a class's fit to random signs; its bound by the growth
  function; generalization in terms of R/ρ rather than dimension.
* **weak and strong learning, boosting, AdaBoost, decision stump, edge** — error just below a half on every
  distribution; combining weak rules into a strong one; one threshold on one coordinate; how far below a half.
* **minimax theorem, multiplicative weights** — the game behind boosting; the update shared by AdaBoost and Hedge.
* **mistake bound, halving algorithm, Littlestone dimension, weighted majority** — online learning counted in
  mistakes.
* **experts problem, Hedge, regret, follow the leader** — choosing among N advisers against an adversary; the loss
  above the best adviser in hindsight.
* **online gradient descent, online-to-batch conversion** — regret D G √T for convex losses; averaging the iterates
  turns a regret bound into a risk bound.
* **multi-armed bandit, explore and exploit, UCB1, Thompson sampling, Lai–Robbins lower bound** — learning while
  earning; optimism; probability matching; the ln T / KL rate no consistent policy beats.
* **representation-dependent and cryptographic hardness of learning** — hardness from the hypothesis we must output;
  hardness whatever is output, from a cryptosystem.
* **statistical query (SQ), SQ dimension, sparse parity, learning parity with noise (LPN)** — learners that see only
  averages; the number of nearly orthogonal functions in a class; the classic hard case.
* **interpolation threshold, double descent, minimum-norm interpolant, pseudo-inverse, implicit bias, benign
  overfitting** — p = n; the second fall of test error; the smallest exact fit and what gradient descent from zero
  finds; fitting noise without paying for it.
* **Occam's razor bound, Kraft's inequality, sample compression scheme, minimum description length (MDL)** — short
  descriptions generalize; a sample reduced to k points from which a consistent hypothesis is rebuilt; model bits plus
  exception bits.
* **in-context learning, sample compression conjecture** — learning inside a forward pass; schemes of size O(d)?

## Sources

* S. Shalev-Shwartz and S. Ben-David, *Understanding Machine Learning: From Theory to Algorithms* (2014);
  M. Mohri, A. Rostamizadeh and A. Talwalkar, *Foundations of Machine Learning* (2nd ed., 2018); M. Kearns and
  U. Vazirani, *An Introduction to Computational Learning Theory* (1994).
* N. Cesa-Bianchi and G. Lugosi, *Prediction, Learning, and Games* (2006); T. Lattimore and C. Szepesvári, *Bandit
  Algorithms* (2020).
* L. Valiant, "A theory of the learnable", Commun. ACM 1984; V. Vapnik and A. Chervonenkis, "On the uniform
  convergence of relative frequencies of events to their probabilities", Theory Probab. Appl. 1971; N. Sauer, "On the
  density of families of sets", J. Combin. Theory A 1972; S. Shelah, "A combinatorial problem; stability and order
  for models and theories in infinitary languages", Pacific J. Math. 1972.
* A. Blumer, A. Ehrenfeucht, D. Haussler and M. Warmuth, "Occam's razor", Inf. Process. Lett. 1987, and
  "Learnability and the Vapnik–Chervonenkis dimension", J. ACM 1989.
* F. Rosenblatt, "The perceptron: a probabilistic model for information storage and organization in the brain",
  Psychological Review 1958; A. Novikoff, "On convergence proofs on perceptrons", Symposium on the Mathematical Theory
  of Automata 1962; C. Cortes and V. Vapnik, "Support-vector networks", Machine Learning 1995.
* P. Bartlett and S. Mendelson, "Rademacher and Gaussian complexities: risk bounds and structural results", JMLR
  2002; V. Koltchinskii and D. Panchenko, "Empirical margin distributions and bounding the generalization error of
  combined classifiers", Ann. Statist. 2002.
* R. Schapire, "The strength of weak learnability", Machine Learning 1990; Y. Freund and R. Schapire, "A
  decision-theoretic generalization of on-line learning and an application to boosting", J. Comput. Syst. Sci. 1997;
  R. Schapire, Y. Freund, P. Bartlett and W. S. Lee, "Boosting the margin: a new explanation for the effectiveness of
  voting methods", Ann. Statist. 1998; J. Friedman, "Greedy function approximation: a gradient boosting machine",
  Ann. Statist. 2001.
* N. Littlestone, "Learning quickly when irrelevant attributes abound: a new linear-threshold algorithm", Machine
  Learning 1988; N. Littlestone and M. Warmuth, "The weighted majority algorithm", Inf. Comput. 1994;
  N. Cesa-Bianchi, Y. Freund, D. Haussler, D. Helmbold, R. Schapire and M. Warmuth, "How to use expert advice",
  J. ACM 1997; M. Zinkevich, "Online convex programming and generalized infinitesimal gradient ascent", ICML 2003.
* W. Thompson, "On the likelihood that one unknown probability exceeds another in view of the evidence of two
  samples", Biometrika 1933; H. Robbins, "Some aspects of the sequential design of experiments", Bull. AMS 1952;
  T. L. Lai and H. Robbins, "Asymptotically efficient adaptive allocation rules", Adv. Appl. Math. 1985; P. Auer,
  N. Cesa-Bianchi and P. Fischer, "Finite-time analysis of the multiarmed bandit problem", Machine Learning 2002;
  P. Auer, N. Cesa-Bianchi, Y. Freund and R. Schapire, "The nonstochastic multiarmed bandit problem", SIAM J. Comput.
  2002; E. Kaufmann, N. Korda and R. Munos, "Thompson sampling: an asymptotically optimal finite-time analysis", ALT
  2012; A. Garivier and O. Cappé, "The KL-UCB algorithm for bounded stochastic bandits and beyond", COLT 2011.
* L. Pitt and L. Valiant, "Computational limitations on learning from examples", J. ACM 1988; M. Kearns and
  L. Valiant, "Cryptographic limitations on learning Boolean formulae and finite automata", J. ACM 1994;
  O. Goldreich, S. Goldwasser and S. Micali, "How to construct random functions", J. ACM 1986; M. Kearns, "Efficient
  noise-tolerant learning from statistical queries", J. ACM 1998; A. Blum, M. Furst, J. Jackson, M. Kearns,
  Y. Mansour and S. Rudich, "Weakly learning DNF and characterizing statistical query learning using Fourier
  analysis", STOC 1994; A. Blum, A. Kalai and H. Wasserman, "Noise-tolerant learning, the parity problem, and the
  statistical query model", J. ACM 2003.
* C. Zhang, S. Bengio, M. Hardt, B. Recht and O. Vinyals, "Understanding deep learning requires rethinking
  generalization", ICLR 2017; M. Belkin, D. Hsu, S. Ma and S. Mandal, "Reconciling modern machine-learning practice
  and the classical bias–variance trade-off", PNAS 2019; T. Hastie, A. Montanari, S. Rosset and R. Tibshirani,
  "Surprises in high-dimensional ridgeless least squares interpolation", Ann. Statist. 2022 (arXiv 2019); D. Soudry,
  E. Hoffer, M. S. Nacson, S. Gunasekar and N. Srebro, "The implicit bias of gradient descent on separable data",
  JMLR 2018; P. Bartlett, P. Long, G. Lugosi and A. Tsigler, "Benign overfitting in linear regression", PNAS 2020.
* N. Littlestone and M. Warmuth, "Relating data compression and learnability", technical report 1986; S. Floyd and
  M. Warmuth, "Sample compression, learnability, and the Vapnik–Chervonenkis dimension", Machine Learning 1995;
  M. Warmuth, "Compressing to VC dimension many points", COLT 2003 (open problem); S. Moran and A. Yehudayoff,
  "Sample compression schemes for VC classes", J. ACM 2016; J. Rissanen, "Modeling by shortest data description",
  Automatica 1978.
* S. Garg, D. Tsipras, P. Liang and G. Valiant, "What can transformers learn in-context? A case study of simple
  function classes", NeurIPS 2022.
