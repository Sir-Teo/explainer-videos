# AI, Built — Part 8: Fitting and Generalizing

Part 8 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). A model is fitted to examples; why should it work on anything else? This part
defines risk, empirical risk and Bayes risk; derives bias and variance; builds the classical guarantees one step at a
time (Hoeffding and the union bound, PAC learning, shattering and the growth function, Sauer–Shelah and the VC bound,
Rademacher complexity, margins); computes bounds that still say something for a network (PAC-Bayes, compression,
stability); then the experiments that broke the classical story and the explanations since (random labels, the
implicit bias of gradient descent, double descent in features, samples and epochs, benign overfitting, flat minima);
and ends where generalizing stops being enough: distribution shift and memorization in language models. The history
runs from Hoeffding (1963), Vapnik and Chervonenkis (1971) and Valiant (1984) to Zhang et al. (2017), Belkin et al.
(2019), Bartlett et al. (2020), Carlini et al. (2019–2023), and the 2024–26 state of the debate (non-vacuous bounds for
language models; memorization in court). Everything is computed by `compute.py`, small and on the CPU, mostly on Part
6's pages (Austen and Dickens: 448 pages to train, 191 held out) and on the series' novels model.

* **The gap** (hook). Part 6's nearest-neighbour vote: 93% of its own training pages, 68% of new ones; how we got here,
  1963 to 2025, evenly spaced; the plan.
* **1. Risk, and the best possible rule.** Two Gaussian classes (illustrative); risk and empirical risk (definition
  card); the Bayes rule and Bayes risk derived on a ladder (R* = 0.217, the overlap; the Bayes rule says 1 on an
  interval); Cover & Hart (1967). Threshold rules learned from n = 10 … 2,560 examples, 400 samples each: training error
  15.2% against true risk 27.4% at n = 10, both near the best threshold's 23.0% at n = 2,560; excess risk =
  approximation + estimation.
* **2. Bias and variance, derived.** Sixteen noisy points, 200 draws: lines (bias), degree 12 (variance), degree 5;
  E(y − f̂)² = bias² + variance + σ² derived step by step; Geman, Bienenstock & Doursat (1992); the U measured over
  degrees 0–15, with the directly measured test error within 1% of the sum at every degree.
* **3. One rule, then many.** Hoeffding (theorem card; derived in Part 5); a 30% error rate measured on 10, 40, 160,
  640 test cases, 100,000 times each: 27%, 39%, 81%, 99% of measurements within 5 points; the tail at n = 160 against
  Hoeffding and Chebyshev; test cases for ±5 points at 95%: exactly 315, Hoeffding 738, Chebyshev 1,680. 1,000 useless
  rules on coin-flip labels: the best scores 34% on 100 examples and 50.4% on 10,000 fresh ones; the union bound
  derived; the best training error, the 95% largest gap and the union bound for 1 … 10⁶ rules, exactly from the
  binomial (gap 10 → 27 points, bound 14 → 30); PAC learning (Valiant 1984).
* **4. Shattering and the VC bound.** Lines shatter 3 points, not 4 (XOR); VC dimension (definition card); half-planes
  give 22 of the 32 labellings of 5 points; growth functions counted exactly by a rotating line (n² − n + 2 = 242 of
  65,536 at n = 16; intervals meet Sauer–Shelah exactly); the Sauer–Shelah lemma (theorem card); the VC bound in four
  steps (ghost sample, union bound, Sauer–Shelah, solve); on 448 pages: lines in the plane 0.23, a linear rule on 70
  rates 0.76 (60,400 pages for 0.1), and nothing for the 300,034-weight network.
* **5. Rademacher complexity.** Linear rules on 1 … 70 word rates fitting coin flips (53% → 68%); the empirical
  Rademacher complexity (definition card); the bound (Koltchinskii 2001; Bartlett & Mendelson 2002); for |w| ≤ B,
  derived exactly (Cauchy–Schwarz, Jensen, uncorrelated signs): measured within 1.2% of B√(Σ|xᵢ|²)/n at every n,
  20,000 random directions reaching 0.21 against the formula's 0.45.
* **6. Margins.** The SVM on the pages (separable; 99.0% on new pages; the closest page at 0.066 of the largest input);
  the margin bound in three steps (ramp loss, Rademacher, contraction); Bartlett (1998); computed over γ: best 1.41,
  vacuous (the same margins would need about 6,000 pages); AdaBoost on stumps: training error 0 at round 19, test error
  3.7% then, 0.5% at round 45, 1.6% at round 400, margin distributions moving right (Schapire, Freund, Bartlett & Lee
  1998).
* **7. PAC-Bayes.** Priors, posteriors, the theorem (McAllester 1999; Seeger 2002; Maurer 2004); its proof in four
  lines (change of measure, the binomial tail, Markov, Jensen); our 70 → 128 → 1 network (9,217 weights, 448 pages),
  Dziugaite & Roy's recipe, prior at the random initialization: 10,000 steps of optimizing the bound replayed (KL from
  thousands to 136 nats); 2,000 sampled networks err on 1.6% of the training pages (≤ 2.7% with confidence); the bound
  on the posterior's error is 35.6%, non-vacuous, against 2.8% measured on the test pages; Lotfi et al. (2024).
* **8. Compression and stability.** The SVM on 200 separable points needs 2 support vectors (retrained on them alone:
  the same line, 1.5 × 10⁻⁹); the Littlestone–Warmuth bound 6.9% against VC 0.29; on the pages 47 support vectors,
  0.72; uniform stability (definition card; Bousquet & Elisseeff 2002) measured for ridge regression (slope −0.90
  against n, predicted −1); SGD twice on sets differing in one page (Hardt, Recht & Singer 2016): drift 0.066 after 30
  passes against the bound's 8.4.
* **9. Memorizing nonsense.** The 70 → 512 → 512 → 2 network (300,034 weights): true authors 99.5% on new pages,
  shuffled authors fit completely and 51% on new pages (Zhang et al.); the order of memorizing replayed page by page;
  the corruption sweep (0 … 100% of labels replaced by coin flips, three seeds): test accuracy 99.3% → 92.5% → 83.2% →
  73.5% → 65.8% → 51.7%, every label fit within 20–40 steps.
* **10. Implicit bias: the smallest fit.** Three weights, two equations, in 3D: gradient descent from zero stays in the
  row space and lands on the minimum-norm fit; the five-line proof; checked with 20 equations in 60 unknowns: distance
  to X⁺y 1.2 × 10⁻¹⁵, the part outside the row space 1.1 × 10⁻¹⁵; from a random start it stops 5.97 away, exactly the
  start's null-space part.
* **11. Implicit bias: the widest margin.** Logistic regression by gradient descent on separable points, a million
  steps replayed: 30° from the max-margin direction after one step, 2.9° after 10⁶, |w| growing like log t; why
  (exponential tails, support vectors, KKT); Soudry et al. (2018), Lyu & Li (2020); angle × ln t falls from 73 to 41.
* **12. Double descent.** Least squares on p random ReLU features of the pages (5 draws each): the U, a peak of 83 at
  p = n = 448, and 0.17 at p = 6,000 (below the U's 0.22); the minimum-norm fit's weights; why: β̂ = Σ uᵢᵀt/σᵢ vᵢ, noise
  amplified by Σ1/σᵢ², the smallest singular value 0.0003 at p = n (the spectrum sliding to zero, animated); ridge
  λ = p removes the peak (0.16 at p = n); Belkin et al. (2019), Nakkiran et al. (2020).
* **13. Double descent in samples and in epochs.** p = 200 fixed features, n = 20 … 448 pages: the error rises from
  0.30 to 19.8 at n = p (more data hurts), ridge flat; epoch-wise in a linear model with two feature scales (Heckel &
  Yilmaz 2021): low 1.97 at step 10, peak 3.31 at step 467, then 0.41, decomposed into fast and slow directions.
* **14. Benign overfitting.** Smooth-plus-spikes against bending (schematic); 100 noisy examples, signal in 5
  directions, plus D weak directions of total variance 5: excess error 0.023 at D = 40,000 (9% of the noise), against
  5.0 with D strong ones; the effective-rank conditions (Bartlett, Long, Lugosi & Tsigler 2020); tempered overfitting
  (Mallinar et al. 2022).
* **15. Flat minima and the sharpness debate.** Hochreiter & Schmidhuber (1997), Keskar et al. (2017);
  24 networks (10 → 256 → 2) on a teacher's 300 points, batch 4 … 300, two step sizes, three seeds, each trained to
  training loss 0.01 (21 got there within 4,000 epochs): sharpness (top Hessian eigenvalue by Hessian-vector products)
  0.70 at batch 4 against 0.89 at batch 300; rank correlation with test error −0.41 (test errors 19.4–20.6%): the
  sharper ones did slightly better here; the rescaling W₁·a, W₂/a leaves the function exactly unchanged and moves
  sharpness from 0.88 to 7.8 (Dinh et al. 2017); SAM (Foret et al. 2021); Andriushchenko et al. (2023).
* **16. Distribution shift.** Covariate shift after Shimodaira (2000): least squares 0.316, importance-weighted 0.098
  (the best line for the test inputs: 0.094), flattened 0.101, with weights estimated by a domain classifier 0.099
  (1,000 runs); the derivation; effective sample size 42 of 100.
* **17. Memorization in language models.** Carlini et al. (2019, 2021, 2023); the extraction test; the novels model:
  no 64-token training passage repeats more than 10 times and none of 436 is extracted, but the run before the first
  mistake grows with repetition (0.46 tokens seen once, 2.6 seen 9–16 times, 0.51 held out); the model trained on (279 steps, three passes over
  250,000 tokens of its own text) with 16 unseen passages planted 1, 2, 4, … 64 times each: exactly extracted 0%, 6%,
  19%, 81%, 100%, 100%, 100%, against 0% for 16 never planted, the replay showing the most repeated ones memorized
  first; a 64-times passage reproduced word for word on screen;
  deduplication (Kandpal et al. 2022; Lee et al. 2022), Nasr et al. (2023), Cooper et al. (2025), GEMA v. OpenAI
  (Munich, November 2025), Getty Images v. Stability AI (London, November 2025), Ahmed, Cooper et al. (2026).
* **Recap**, where it comes back, problems, Part 9's teaser, references.

## Run

```
python tools/make.py ai8                         # computations, then the narrated film in English and Chinese
python -m videos.ai.ai8.compute                  # the numbers only (Part 6's pages; the novels model for two items)
python tools/build.py ai8                        # English
python tools/build.py ai8 --lang zh              # Chinese
EXPLAINER_TTS=silent python tools/build.py ai8 -q l --fps 15     # a quick silent preview
```

Everything is seeded and runs on the CPU, on one thread (`AI8_THREADS`, default 1), except `canary`, which continues
training the novels model on two (`AI8_TRAIN_THREADS`, default 2) for about forty minutes and checkpoints every few
dozen steps (`.cache/ai8/canary.ckpt`), so a killed run resumes. `corrupt` and `sharp` save each finished run as they
go. In all, about an hour of CPU time. `memorize` and `canary` need the novels model (`python -m explainer.ai.novels`,
which `make.py` runs first if it is missing).

## Computed results

| Item | Result |
|---|---|
| risk | Bayes risk 0.217; best threshold 0.230; n = 10: training 0.152, true 0.274; n = 2,560: 0.227, 0.231 |
| bias–variance | best degree 5; measured test error within 0.8% of bias² + variance + σ² at every degree |
| Hoeffding | within ±5 points: 27%, 39%, 81%, 99% at n = 10, 40, 160, 640; n for 95%: exact 315, Hoeffding 738, Chebyshev 1,680 |
| union bound (n = 100) | best of 1 … 10⁶ useless rules: 51% → 27% training error; 95% largest gap 10 → 27 points; bound 14 → 30 |
| growth function | half-planes n² − n + 2 (242 at n = 16), 22 of 32 at n = 5; intervals = Sauer–Shelah exactly |
| VC bound, 448 pages | lines in the plane 0.23; linear on 70 rates 0.76 (0.1 needs 60,400 pages) |
| Rademacher | coin flips fitted 53% (1 rate) → 68% (70 rates); norm-bounded linear: measured ≥ 98.9% of the bound |
| margins | SVM separates the pages, 99.0% test, 47 SVs; margin bound 1.41 (needs ≈ 6,000 pages for 0.5) |
| AdaBoost | train error 0 at round 19 (test 3.7%); test 0.5% at round 45; 1.6% at round 400 |
| PAC-Bayes | 9,217 weights, KL 136 nats, λ = 0.042; Q's training error 1.6% (≤ 2.7%); bound 0.356; Q's test error 2.8% |
| compression | 2 support vectors of 200: bound 0.069 (VC 0.29); pages: 47 of 448, 0.72 |
| stability | ridge: slope −0.90 against n; SGD drift 0.066 after 30 passes, bound 8.4 |
| random labels | true labels 99.5% test; shuffled: all fit, 51.3% test; corruption 0 → 100%: 99.3% → 51.7% |
| min-norm | distance to X⁺y 1.2e-15; other start 5.970 away = predicted 5.970 |
| max margin | 30.0° → 2.9° after 10⁶ steps; margin 1.088 of 1.116; angle × ln t 73 → 41 |
| double descent | U bottom 0.22 (p = 112); 83 at p = n = 448; 0.17 at p = 6,000; σmin/√p = 0.0003 at p = n; ridge λ = p: 0.16 |
| sample-wise | p = 200: error 0.30 (n ≈ 60) → 19.8 at n = 200 |
| epoch-wise | 1.97 (step 10) → 3.31 (step 467) → 0.41 |
| benign | spiked: excess 0.023 at D = 40,000 (noise 0.25); isotropic 4.99 |
| sharpness | 21 of 24 runs reach loss 0.01; λmax 0.70 (batch 4) vs 0.89 (batch 300); Spearman ρ(λmax, test error) = −0.41; rescaling: same function, λmax 0.88 → 7.8 |
| covariate shift | test MSE: OLS 0.316, IW 0.098, flattened 0.101, estimated 0.099; best line 0.094; ESS 42/100 |
| memorization (novels model) | 0 of 436 training passages extracted; run before the first miss 0.46 → 2.6 tokens with repetition (held out 0.51) |
| canary | extracted after 279 steps: planted 1×, 2×, 4×, 8×, 16×, 32×, 64×: 0%, 6%, 19%, 81%, 100%, 100%, 100%; never planted 0% |

## Fact-check notes

* Carlini et al., *Extracting Training Data from Large Language Models* (USENIX Security 2021): 1,800 candidates, "over
  600" verbatim (arXiv:2012.07805). Carlini et al., *Quantifying Memorization Across Neural Language Models* (ICLR 2023,
  arXiv:2202.07646): three log-linear relationships; GPT-J memorizes at least 1% of the Pile; extractability defined
  with greedy decoding from a k-token prefix (the definition used in chapter 17).
* Cooper et al., *Extracting memorized pieces of (copyrighted) books from open-weight language models* (arXiv:2505.12546,
  2025): Llama 3.1 70B memorizes some books, such as the first Harry Potter, almost entirely. Ahmed, Cooper, Koyejo &
  Liang, *Extracting books from production language models* (arXiv:2601.02671, January 2026): near-complete extraction
  of a book from some production models (one with a jailbreak).
* GEMA v. OpenAI, Munich Regional Court I, 11 November 2025 (42 O 14139/24): memorized lyrics are reproductions; not
  final. Getty Images v. Stability AI, [2025] EWHC 2863 (Ch), 4 November 2025: the model weights are not an infringing
  copy. Bartz v. Anthropic (23 June 2025) and Kadrey v. Meta (25 June 2025), N.D. Cal.: training held fair use (Bartz:
  not for pirated library copies). Later 2026 rulings (e.g. GEMA v. Suno, reported July 2026) are not on screen: only
  law-firm summaries were found.
* Lotfi et al., *Non-Vacuous Generalization Bounds for Large Language Models* (ICML 2024) and *Unlocking Tokens as Data
  Points for Generalization Bounds on Larger Language Models* (NeurIPS 2024, up to LLaMA2-70B).
* Valiant's Turing Award is the 2010 award (presented 2011).
* The VC bound on screen is Vapnik's form, √((d(ln(2n/d) + 1) + ln(4/δ))/n); the four-step proof shown gives the same
  rate with larger constants.
* Shimodaira (2000) is the source of importance-weighted least squares under covariate shift; the setup of chapter 16
  (training inputs N(0.5, 0.5²), test inputs N(0, 0.3²), y = −x + x³) follows the example common in that literature
  and is labelled illustrative.

## Problems, with solutions

1. **Sizing a test set.** How many test examples guarantee, with probability 0.99, that the error rates of 100 fixed
   models are all within 0.02 of their true values? *Solution.* Union bound over Hoeffding:
   2·100·e^(−2n·0.02²) ≤ 0.01 ⇔ n ≥ ln(20,000)/(2·0.0004) = 9.903/0.0008 ≈ 12,380.
2. **Intervals.** Show intervals on the line have VC dimension 2 and growth function C(n, 2) + n + 1. *Solution.* Two
   points: an interval can cover neither, either or both. Three ordered points cannot be labelled +, −, +: an interval
   containing the outer two contains the middle one. On n ordered points an interval labels + a contiguous run:
   choose its first and last point (C(n, 2) runs of length ≥ 2, n of length 1) or the empty run: C(n, 2) + n + 1 =
   Σᵢ₌₀² C(n, i), the Sauer–Shelah bound with d = 2.
3. **Massart's lemma for the ℓ₁ ball.** For {x ↦ w·x : |w|₁ ≤ B} with |xᵢ|∞ ≤ X, show R̂_S ≤ BX√(2 ln(2d)/n).
   *Solution.* sup over the ℓ₁ ball of w·v is B|v|∞ (Hölder; attained at a signed coordinate vector), so
   R̂_S = (B/n) E maxⱼ,± ±Σᵢσᵢxᵢⱼ, a maximum of N = 2d sums σ·a with |a|₂ ≤ X√n. Massart: E max ≤ max|a|₂ √(2 ln N).
   Hence R̂_S ≤ (B/n) X√n √(2 ln 2d).
4. **Gradient descent from w₀.** Show that on ½|Xw − y|² with d > n and a small step, gradient descent from w₀
   converges to X⁺y + (I − X⁺X)w₀. *Solution.* P = X⁺X projects onto the row space. Every step adds Xᵀ(·) ∈ row(X), so
   (I − P)w_t = (I − P)w₀ forever, and Xw_t = XPw_t: the row-space part u_t = Pw_t follows gradient descent on
   ½|Xu − y|² inside row(X), where the loss is strictly convex with unique minimizer X⁺y. So w_t → X⁺y + (I − P)w₀,
   at distance |(I − P)w₀| from the minimum-norm fit (chapter 10 measured 5.970 for both).
5. **KL between Gaussians.** For Q = N(μ, s²I), P = N(μ₀, λI) in d dimensions derive KL(Q‖P). *Solution.* Per
   coordinate, E_Q[ln q − ln p] = −½ ln(2πs²) − ½ + ½ ln(2πλ) + (s² + (μ − μ₀)²)/(2λ); summing over d coordinates,
   KL = ½(ds²/λ + |μ − μ₀|²/λ − d − d ln(s²/λ)). (With a different s per coordinate, as in chapter 7, sum the
   per-coordinate terms.)
6. **Importance weights.** Show the importance-weighted training error is unbiased for the test error, and that with
   p = N(0, 1), q = N(0, 4) the weights have infinite variance. *Solution.* E_p[w(x)ℓ(x)] = ∫p(q/p)ℓ = E_q[ℓ].
   E_p[w²] = ∫q²/p dx ∝ ∫exp(−x²/4 + x²/2) dx = ∫exp(x²/4) dx = ∞: the test distribution has heavier tails than the
   training one, and the effective sample size collapses.

## 习题与解答

1. **测试集要多大。** 要以0.99的概率保证100个固定模型的错误率都和真实值相差不超过0.02，需要多少个测试样本？
   *解答。* 对霍夫丁不等式用联合界：2·100·e^(−2n·0.02²) ≤ 0.01 ⇔ n ≥ ln(20000)/(2·0.0004) ≈ 12380。
2. **区间。** 证明直线上的区间VC维为2，增长函数为C(n, 2) + n + 1。
   *解答。* 两个点：区间可以一个都不盖、盖其中一个或两个都盖。三个排好序的点无法标成+、−、+：盖住两端的区间必然盖住中间的点。
   n个排好序的点上，区间标为+的是一段连续的点：选首尾两点（长度≥2的有C(n, 2)段，长度为1的有n段），再加上空集：
   C(n, 2) + n + 1 = Σᵢ₌₀² C(n, i)，恰好是d = 2时的绍尔–谢拉界。
3. **ℓ₁球的马萨特引理。** 对{x ↦ w·x : |w|₁ ≤ B}且|xᵢ|∞ ≤ X，证明R̂_S ≤ BX√(2 ln(2d)/n)。
   *解答。* 在ℓ₁球上w·v的上确界是B|v|∞（赫尔德不等式，在带符号的坐标向量处取到），所以R̂_S = (B/n) E max ±Σᵢσᵢxᵢⱼ，
   是N = 2d个形如σ·a的和的最大值，且|a|₂ ≤ X√n。由马萨特引理，E max ≤ max|a|₂ √(2 ln N)，于是R̂_S ≤ (B/n)X√n√(2 ln 2d)。
4. **从w₀出发的梯度下降。** 证明在d > n、步长很小时，½|Xw − y|²上的梯度下降从w₀出发收敛到X⁺y + (I − X⁺X)w₀。
   *解答。* P = X⁺X是到行空间的投影。每一步加上的Xᵀ(·)都在行空间里，所以(I − P)w_t始终等于(I − P)w₀；而Xw_t = XPw_t，
   行空间部分u_t = Pw_t就是在行空间内对½|Xu − y|²做梯度下降，那里损失严格凸，唯一的极小点是X⁺y。所以w_t → X⁺y + (I − P)w₀，
   离最小范数解的距离是|(I − P)w₀|（第10章两者都测得5.970）。
5. **高斯分布之间的KL散度。** 对d维的Q = N(μ, s²I)、P = N(μ₀, λI)，推导KL(Q‖P)。
   *解答。* 每个坐标上，E_Q[ln q − ln p] = −½ln(2πs²) − ½ + ½ln(2πλ) + (s² + (μ − μ₀)²)/(2λ)；对d个坐标求和，
   KL = ½(ds²/λ + |μ − μ₀|²/λ − d − d ln(s²/λ))。（如第7章那样每个坐标的s不同时，把各坐标的项相加。）
6. **重要性权重。** 证明重要性加权的训练误差是测试误差的无偏估计，并说明当p = N(0, 1)、q = N(0, 4)时权重的方差是无穷大。
   *解答。* E_p[w(x)ℓ(x)] = ∫p(q/p)ℓ = E_q[ℓ]。E_p[w²] = ∫q²/p dx ∝ ∫exp(−x²/4 + x²/2)dx = ∫exp(x²/4)dx = ∞：
   测试分布的尾部比训练分布重，有效样本量随之崩溃。

## References

Books: S. Shalev-Shwartz & S. Ben-David, *Understanding Machine Learning* (2014); M. Mohri, A. Rostamizadeh &
A. Talwalkar, *Foundations of Machine Learning*, 2nd ed. (2018); F. Bach, *Learning Theory from First Principles*
(2024); V. Vapnik, *The Nature of Statistical Learning Theory* (1995); T. Hastie, R. Tibshirani & J. Friedman, *The
Elements of Statistical Learning* (2009).

Papers: Hoeffding (1963); Vapnik & Chervonenkis (1971); Sauer (1972); Shelah (1972); Valiant, *A Theory of the
Learnable* (1984); Littlestone & Warmuth (1986); Geman, Bienenstock & Doursat (1992); Hochreiter & Schmidhuber, *Flat
Minima* (1997); Bartlett (1998); Schapire, Freund, Bartlett & Lee, *Boosting the Margin* (1998); McAllester (1999);
Shimodaira (2000); Koltchinskii (2001); Bartlett & Mendelson (2002); Bousquet & Elisseeff (2002); Seeger (2002); Maurer
(2004); Hardt, Recht & Singer (2016); Zhang, Bengio, Hardt, Recht & Vinyals (2017); Dziugaite & Roy (2017); Keskar et al.
(2017); Dinh, Pascanu, Bengio & Bengio (2017); Soudry, Hoffer, Nacson, Gunasekar & Srebro (2018); Arora, Ge, Neyshabur &
Zhang (2018); Belkin, Hsu, Ma & Mandal (2019); Nakkiran et al., *Deep Double Descent* and *Optimal Regularization Can
Mitigate Double Descent* (2020); Lyu & Li (2020); Bartlett, Long, Lugosi & Tsigler (2020); Heckel & Yilmaz (2021);
Foret et al., SAM (2021); Mallinar et al. (2022); Andriushchenko et al. (2023); Lotfi et al. (2022, 2024, 2024);
Carlini et al. (2019, 2021, 2023); Kandpal, Wallace & Raffel (2022); Lee et al. (2022); Nasr et al. (2023); Cooper et al.
(2025); Ahmed, Cooper, Koyejo & Liang (2026).

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| risk, empirical risk, Bayes risk, Bayes rule | 风险，经验风险，贝叶斯风险，贝叶斯规则 |
| excess risk; approximation error, estimation error | 超额风险；近似误差，估计误差 |
| bias–variance decomposition | 偏差–方差分解 |
| union bound; PAC (probably approximately correct) | 联合界；PAC（概率近似正确） |
| shatter, VC dimension, growth function | 打散，VC维，增长函数 |
| Sauer–Shelah lemma; ghost sample (symmetrization) | 绍尔–谢拉引理；影子样本（对称化） |
| (empirical) Rademacher complexity; McDiarmid's inequality | （经验）拉德马赫复杂度；麦克迪尔米德不等式 |
| margin, margin loss, ramp loss, contraction lemma | 间隔，间隔损失，斜坡损失，压缩引理 |
| boosting, decision stump | 提升法，决策树桩 |
| PAC-Bayes; prior, posterior; change of measure | PAC-贝叶斯；先验，后验；测度变换 |
| vacuous / non-vacuous bound | 空的界 / 非空的界 |
| sample compression scheme | 样本压缩方案 |
| (uniform) stability | （一致）稳定性 |
| random labels, label corruption | 随机标签，标签污染 |
| implicit bias; minimum-norm interpolant; row space | 隐式偏好；最小范数插值解；行空间 |
| max-margin direction | 最大间隔方向 |
| double descent; interpolation threshold; sample-wise, epoch-wise | 双下降；插值阈值；按样本数的，按训练轮数的 |
| benign / tempered / harmful overfitting; effective rank | 良性 / 温和 / 有害过拟合；有效秩 |
| flat minimum, sharpness, sharpness-aware minimization (SAM) | 平坦极小值，尖锐度，锐度感知最小化（SAM） |
| distribution shift, covariate shift, label shift, concept drift | 分布偏移，协变量偏移，标签偏移，概念漂移 |
| importance weighting, effective sample size | 重要性加权，有效样本量 |
| memorization, extractable, canary, deduplication | 记忆，可提取，金丝雀（植入的测试文本），去重 |
