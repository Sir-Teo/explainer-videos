# Computer Science, Built — Part 20: Randomness as a Resource

Part 20 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act IV, *Algorithms*. A coin flip can stand in for cleverness.
With one, you can check a matrix product in n² time, find a minimum cut by contracting random edges, test
primality in milliseconds, and count the top words of thirty novels in a few kilobytes. Randomness has to come from
somewhere, though, and some generators hide fifteen planes. The instrument is `explainer/cs/algo/randomized.py`. It
implements Freivalds' check, the Schwartz–Zippel test, the Tutte matrix and fingerprints; Karger's contraction and
Karger–Stein; Fermat and Miller–Rabin with Carmichael numbers; random-walk 2-SAT and Schöning's 3-SAT; balls into
bins; Bloom filters; reservoir sampling, Misra–Gries, HyperLogLog, KMV and the AMS sketch; MinHash and banded LSH;
Moser–Tardos; conditional expectations; and RANDU. It is tested in `tests/test_cs20_randomized.py`. The Job v3, a
Count-Min sketch and a heap in the Pebble language, is `explainer/cs/algo/job3.py`, with a Python mirror that
reproduces its output byte for byte. Every number is computed in `compute.py`; timings are taken on this machine.

* **The top words in kilobytes.** Part 17's hash table and this part's sketch give the same twenty words and counts
  for the thirty novels, from 1.9 MB and 18.6 KB of memory; four things coins buy.
* **1. Las Vegas and Monte Carlo.** Always right with a random running time, or a fixed time with a bounded error.
  Randomized quicksort on 2,000 keys, 400 runs: mean 24,761 comparisons against the exact 24,730, spread 1,339,
  slowest 30,234, worst case 1,999,000. One-sided error and 2^{−k}; majority votes and Hoeffding.
* **2. Checking a product with a coin.** Freivalds (1977): A(Br) = Cr in three matrix-vector products. The proof by
  deferred decisions. At n = 2,000: 16 billion operations against 24 million, 0.13 s against 23 ms with numpy's BLAS.
  One wrong entry passes 50.9%, 25.1%, 12.4%, 6.3% and 1.4% of 4,000 trials for one to six rounds, on the 2^{−k}
  bound; many wrong entries never pass.
* **3. Is this polynomial zero?** The Schwartz–Zippel lemma, proved by induction. A false identity of degree 3
  agrees at 75%, 44%, 19%, 6.5%, 1.9% and 0.18% of random points for |S| = 2 to 1,000, under 3/|S|. An 8 × 8
  Vandermonde identity (40,320 terms) checked at 50 random points. Tutte's matrix and Lovász's test agree with
  Edmonds' blossom algorithm on 48 random graphs of 40–100 vertices (33 with a perfect matching). A 61-bit
  fingerprint of the 25 MB corpus in 0.15 s, false-match probability at most 1.2 × 10^{−10}.
* **4. A minimum cut by contraction.** Karger (1993) on two dense clusters joined by three edges, animated: one run
  succeeds, one cuts off a single vertex. Success ≥ 2/(n(n − 1)), proved by telescoping; measured 13.1% of 20,000
  runs against the bound's 0.83%. The ten-cycle has exactly 45 = C(10, 2) minimum cuts, each found 1.9–2.4% of the
  time. Karger–Stein's recursion; on a 48-vertex graph one contraction succeeds 17.5% of the time, Karger–Stein 40
  times in 40.
* **5. Primes in milliseconds.** Fermat's test; 561 = 3 · 11 · 17 fools all 320 coprime bases; Korselt's criterion;
  43 Carmichael numbers below a million. Miller–Rabin's square roots of 1, with 561's sequence 263, 166, 67, 1. Rabin's
  bound of ¼: 10 strong liars for 561, and the worst odd composite below 20,000 is 9, with exactly ¼. Random primes:
  256 bits in 9 ms, 1,024 in 1.0 s, 2,048 in 5.9 s; AKS (2002).
* **6. Random walks that solve SAT.** Papadimitriou's 2-SAT walk as a gambler's ruin, with expected time at most n².
  Random satisfiable formulas need about 2n flips, against the 2n² bound (676 flips at n = 320). Schöning's
  restarts and (4/3)^n: on formulas with exactly one solution at the threshold, 33 restarts at n = 20, against
  Schöning's 315 and 2^20 assignments; PPSZ.
* **7. Balls into bins, and the power of two choices.** 24 balls in 12 bins, animated, one choice against two.
  Maximum loads for n = 10³ … 10⁶: 7, 7, 9, 10 with one choice, 3, 3, 4, 4 with two. The full load histograms at a
  million, a Poisson law against a doubly exponential tail. Why the tail squares; d choices; load balancers and
  cuckoo hashing.
* **8. Bloom filters.** 32 bits and 3 hashes, with false positives drawn. (1 − e^{−kn/m})^k and the optimal
  k = (m/n) ln 2, derived. On the novels' 57,895 words with 100,000 non-words at 10 bits per word: k = 7 lets
  through 0.815% against 0.819% predicted, and 50.4% of the bits are set. At 16 bits per word, 0.049%. 71 KB against
  442 KB of letters.
* **9. Streams: one pass, little memory.** The model. Reservoir sampling, proved, with 50,000 trials (each item
  chosen 2,371–2,661 times, 2,500 expected). Misra–Gries with 99 counters: the 13 words above n/k = 46,100 survive,
  each about 38,700 low. Count-Min (Cormode and Muthukrishnan, 2005) and its (ε, δ) guarantee. With 4 × 1021
  counters on the novels, no word exceeds eN/w = 12,273 and the mean excess is 968. With two rows, 0.31% of the
  words exceed it, against the 13.5% allowed.
* **10. The Job in kilobytes: ledger row 9.** The Job v3 in the Pebble language: Count-Min with conservative update
  (Estan and Varghese, 2002), rows by double hashing (Kirsch and Mitzenmacher, 2006), 32 candidates in a heap, 128
  slots with backward-shift deletion. Every one of its 1.07 billion instructions was emulated, 43 per byte, and the
  output equals the exact counts. 18,588 bytes against Part 17's 1.9 MB, 102× less. The traced loads and stores of a
  150 KB passage touch 295 lines, at most 6 per L1 set. IPC 1.21 against 1.43. Ledger row 9 is 1.00 s against row
  8's 0.81 s: memory bought with a quarter more time. Over 20 hash functions in C, the program's own sketch size is
  exact 25% of the time, 19.1 of 20 words right on average and never fewer than 18. The true top 20 are always
  among the 32 candidates, so a second pass is always exact. 32 KB is exact 70% of the time, 64 KB 95%.
* **11. Counting distinct things: HyperLogLog.** Flajolet–Martin's leading zeros; HyperLogLog's harmonic mean
  (Flajolet, Fusy, Gandouet and Meunier, 2007). Measured over 30 hash functions on 57,895 words, the error is 26%,
  17%, 6.0%, 3.0%, 1.5% and 0.7% for 16 to 16,384 registers, against 1.04/√m. The whole corpus at m = 4,096 (3 KB)
  gives 58,012. Its 4,506,123 distinct five-word phrases give 4,483,876, in the same 3 KB.
* **12. Sketching the second moment.** Frequency moments; F₂ of the novels is 177,430,472,332, 30% of it from
  *the*. The AMS sketch (1996), derived. 400 single estimates scatter, with mean 1.00. The error is 82%, 31%, 17%
  and 7% for k = 4 to 256, against √(2/k). With the median of nine means at k = 64, the worst error is 17%. Linear
  sketches as random projections (Johnson–Lindenstrauss).
* **13. Near-duplicates: MinHash and LSH.** Shingles and Jaccard similarity; Broder's MinHash (1997), proved; banding
  (Indyk and Motwani, 1998) and the S-curve 1 − (1 − J⁵)²⁰, matched by 600 planted copies. Among 34,525
  paragraphs (596 million pairs), signatures take 2.1 s and banding 3.4 s, giving 2 candidates. An inverted index
  finds 7 pairs with J ≥ 0.2: a table of contents, the denunciation letter in *The Count of Monte Cristo*, an order
  in *War and Peace*, a passage in *The Awakening*. Both pairs above the threshold were found. SimHash.
* **14. The probabilistic method.** Ramsey numbers: a random colouring of K₁₇ has 74 one-colour K₄'s on average,
  the Paley colouring none. Erdős (1947): R(k, k) > 2^{k/2}, with the counting bound tabulated to k = 20.
  Campos–Griffiths–Morris–Sahasrabudhe (2023). The Lovász local lemma, and Moser–Tardos resampling on 10-SAT with
  2,000–32,000 variables inside the lemma's condition: 8, 22 and 72 resamplings.
* **15. Removing the coins, and where they come from.** Conditional expectations for MAX-CUT: on 265 edges, 176
  cut, against a random mean of 132.5 and a best of 162 in 2,000 random splits. Pairwise independence from k bits;
  RANDU's 15 planes, shown by rotating the cube; the Mersenne Twister, PCG, cryptographic generators and physical
  entropy.
* **16. Frontier: does randomness help?** Derandomized one at a time: primality (AKS), connectivity (Reingold),
  minimum cut (Kawarabayashi–Thorup; Henzinger–Li–Rao–Wang), matching in quasi-NC (Fenner–Gurjar–Thierauf).
  Hardness against randomness (Nisan–Wigderson; Impagliazzo–Wigderson). PIT and circuit lower bounds
  (Kabanets–Impagliazzo). Optimal sketches and their lower bounds; open problems. Outro.

## Build

```bash
python -m videos.cs.cs20.compute           # every number in the part (about half an hour; the Job v3 emulation is most of it)
python tools/build.py cs20 -q l            # a 480p preview
python tools/build.py cs20                 # 1080p
```

## Problems, with solutions

1. **Freivalds with more values.** Choose r uniformly from {0, …, q − 1}ⁿ. Prove that a wrong C passes with
   probability at most 1/q, and that this is tight.

   *Solution.* If C ≠ AB, then D = AB − C has a nonzero entry d_ij. The test passes only if (Dr)_i = 0. Write
   (Dr)_i = d_ij r_j + s, where s depends only on the other coordinates of r. Fix those first (deferred decisions).
   Then (Dr)_i = 0 needs r_j = −s/d_ij, a single number, and r_j takes each of q values with probability 1/q, so
   the probability is at most 1/q. The same argument works over any field with at least q elements. For tightness,
   take C = AB + E, where E has a single 1 at (i, j). Then Dr = −r_j e_i, which is zero exactly when r_j = 0, with
   probability exactly 1/q.

2. **Near-minimum cuts.** Prove that a graph has at most n^{2α} cuts within a factor α of the minimum, using
   Karger's contraction.

   *Solution.* Let the minimum cut have size k, and fix a cut C with |C| ≤ αk. Take t = ⌈2α⌉ and assume first that
   2α is an integer. Contract random edges until t vertices remain, then output a uniformly random one of the
   2^{t−1} − 1 cuts of those t super-vertices. With i vertices left, every vertex still has degree at least k, so at
   least ik/2 edges remain, and the next contraction hits C with probability at most αk/(ik/2) = t/i. C therefore
   survives to t vertices with probability at least ∏_{i=t+1}^{n} (1 − t/i) = ∏ (i − t)/i = t!(n − t)!/n! = 1/C(n, t).
   It is then output with probability 1/(2^{t−1} − 1). So each such cut is output with probability at least
   1/(C(n, t) 2^{t−1}) ≥ t!/(n^t 2^{t−1}) ≥ n^{−t}, since t! ≥ 2^{t−1}. Different cuts are disjoint outcomes, so
   there are at most n^t = n^{2α} of them. For non-integer 2α, use generalized binomial coefficients, as Karger
   does (1993), and the same count gives O(n^{2α}). For α = 1 this is the C(n, 2) bound of the chapter.

3. **Sizing a Bloom filter.** For a target false-positive rate ε, show that the optimum needs
   m = n log₂(1/ε)/ln 2 ≈ 1.44 n log₂(1/ε) bits.

   *Solution.* Let p = e^{−kn/m}, the fraction of bits still 0. Then k = −(m/n) ln p, and the false-positive rate is
   f = (1 − p)^k, with ln f = −(m/n) ln p · ln(1 − p). This expression is symmetric under p ↔ 1 − p. The function
   ln p · ln(1 − p) is maximized at p = ½: write g(p) = ln p ln(1 − p). Then g′(p) = ln(1 − p)/p − ln p/(1 − p),
   which is positive for p < ½ and negative for p > ½. So f is minimized at p = ½, that is k = (m/n) ln 2, where
   f = 2^{−k} = 2^{−(m/n) ln 2}. Setting f = ε gives m/n = log₂(1/ε)/ln 2 ≈ 1.44 log₂(1/ε): 9.6 bits per item and
   k ≈ 6.6 for 1%. Any structure answering membership with false-positive rate ε needs at least n log₂(1/ε) bits
   (Carter, Floyd, Gill, Markowsky and Wegman, 1978), so a Bloom filter uses 44% more than the minimum. Cuckoo and
   quotient filters get closer.

4. **Weighted sampling in one pass.** Give item i, of weight w_i, the key u_i^{1/w_i}, with u_i uniform on (0, 1),
   and keep the k items with the largest keys. Prove that this samples by weight.

   *Solution.* Pr[u_i^{1/w_i} ≤ x] = Pr[u_i ≤ x^{w_i}] = x^{w_i} on [0, 1], so the key has density w_i x^{w_i − 1}.
   The item with the largest key is i with probability ∫₀¹ w_i x^{w_i − 1} ∏_{j≠i} x^{w_j} dx = w_i ∫₀¹ x^{W − 1} dx
   = w_i/W, where W = Σ w_j: the first draw is by weight. Given that the maximum is i's key, x, the other keys are
   independent, with Pr[key_j ≤ y | key_j ≤ x] = (y/x)^{w_j}. That is the same family rescaled to [0, x]. So the
   second largest is j with probability w_j/(W − w_i), and so on: the k largest keys are a sample of k items without
   replacement, each drawn with probability proportional to its weight among those left (Efraimidis and Spirakis,
   2006). In one pass, keep a min-heap of the k largest keys, which takes O(log k) per item.

5. **Build: HyperLogLog on Pebble.** Write HyperLogLog with 256 registers in the Pebble language. Take ranks from
   trailing zeros by repeated halving, run it on the novels on the emulator, and compare with the exact count.

   *Solution sketch.* Use the Job's letter hash h = (33h + c) mod 16,777,213 for each word. The register is h mod
   256. The rank is one plus the number of times q = h / 256 can be halved while it stays even: `while q % 2 == 0
   && r < 20 { q = q / 2; r = r + 1; }`. Keep the maximum per register, 256 small integers. A word's hash repeats
   for every occurrence, so repeats change nothing, as required. For the estimate, keep everything in 32 bits. Let
   S = Σ_j 2^{20 − M_j}, with M_j capped at 20; this is at most 2²⁸. Then E = 256 · ⌊α₂₅₆ · 256 · 2²⁰ / S⌋, where
   α₂₅₆ · 256 · 2²⁰ ≈ 1.93 × 10⁸ < 2³¹. With n ≈ 58,000, S is around 850,000, so the quotient is near 226 and its
   rounding costs under half a percent. Linear counting is unnecessary, since n ≫ 2.5m. The error should be about
   1.04/√256 = 6.5% if the hash's low bits behave randomly. Polynomial hashes modulo a prime are not perfectly
   uniform, so check against the exact 57,895 and against several multipliers. The instruction count is the
   tokenizer's, plus about a dozen instructions per word, far below Part 17's table, in 256 words of memory.

6. **★ Research: derandomize identity testing.** Give a deterministic polynomial-time algorithm that decides
   whether an arithmetic circuit computes the zero polynomial.

   *Where to start.* Kabanets and Impagliazzo, "Derandomizing polynomial identity tests means proving circuit
   lower bounds" (2004), explains why this is hard. The surveys are Saxena, "Progress on polynomial identity
   testing" (2009, and II, 2014), and Shpilka and Yehudayoff, "Arithmetic circuits: a survey of recent results and
   open questions" (2010). Solved cases:
   - depth-3 circuits with bounded top fan-in (Kayal and Saxena, 2007; Saxena and Seshadhri, 2011);
   - read-once oblivious branching programs, in quasi-polynomial time (Forbes and Shpilka, 2013; Agrawal, Gurjar,
     Korwar and Saxena, 2015);
   - bootstrapping: hitting sets for tiny circuits would give nearly complete derandomization (Agrawal, Ghosh and
     Saxena, 2018);
   - superpolynomial lower bounds for constant-depth circuits, and from them subexponential PIT for constant depth
     (Limaye, Srinivasan and Tavenas, 2021).

   Open:
   - (a) polynomial-time PIT for formulas, or even for constant-depth circuits;
   - (b) deterministic PIT for the symbolic determinant, which would put perfect matching in deterministic NC;
   - (c) here, measure: build the Tutte matrices of chapter 3's graphs and compare the random evaluation with the
     best deterministic substitution you can find, such as Fenner, Gurjar and Thierauf's isolating weights, on
     graphs of 20–40 vertices.

## 习题与解答

1. **取更多值的 Freivalds 检验。** 让 r 在 {0, …, q − 1}ⁿ 中均匀选取。证明错误的 C 通过检验的概率至多为 1/q，并且这个界是紧的。

   *解答。* 若 C ≠ AB，则 D = AB − C 有一个非零元 d_ij。检验通过要求 (Dr)_i = 0。写 (Dr)_i = d_ij r_j + s，其中 s 只依赖于
   r 的其他坐标。先固定这些坐标（延迟决定原理）。这时 (Dr)_i = 0 要求 r_j = −s/d_ij，这是一个确定的数，而 r_j 以 1/q 的
   概率取 q 个值中的每一个，所以概率至多为 1/q。同样的论证在任何至少有 q 个元素的域上都成立。紧性：取 C = AB + E，E 只在
   (i, j) 处有一个 1。那么 Dr = −r_j e_i，它恰在 r_j = 0 时为零，概率恰好是 1/q。

2. **近似最小割。** 用 Karger 的收缩证明：一个图中大小在最小割 α 倍以内的割至多有 n^{2α} 个。

   *解答。* 设最小割大小为 k，固定一个 |C| ≤ αk 的割 C。取 t = ⌈2α⌉，先假设 2α 是整数。随机收缩边直到剩下 t 个顶点，然后在
   这 t 个超顶点的 2^{t−1} − 1 个割中均匀随机输出一个。剩下 i 个顶点时，每个顶点的度仍至少为 k，所以至少还有 ik/2 条边，
   下一次收缩命中 C 的概率至多为 αk/(ik/2) = t/i。于是 C 存活到 t 个顶点的概率至少为
   ∏_{i=t+1}^{n} (1 − t/i) = ∏ (i − t)/i = t!(n − t)!/n! = 1/C(n, t)，之后以 1/(2^{t−1} − 1) 的概率被输出。因此每个这样的割
   被输出的概率至少为 1/(C(n, t) 2^{t−1}) ≥ t!/(n^t 2^{t−1}) ≥ n^{−t}（因为 t! ≥ 2^{t−1}）。不同的割是互斥的结果，所以至多有
   n^t = n^{2α} 个。2α 不是整数时，像 Karger（1993）那样使用广义二项式系数，同样的计数给出 O(n^{2α})。α = 1 时这就是本章的
   C(n, 2) 界。

3. **确定布隆过滤器的大小。** 对目标假阳性率 ε，证明最优配置需要 m = n log₂(1/ε)/ln 2 ≈ 1.44 n log₂(1/ε) 位。

   *解答。* 令 p = e^{−kn/m}，即仍为 0 的位所占的比例。那么 k = −(m/n) ln p，假阳性率 f = (1 − p)^k，ln f = −(m/n) ln p ·
   ln(1 − p)。这个式子在 p ↔ 1 − p 下对称。函数 ln p · ln(1 − p) 在 p = ½ 处取最大：令 g(p) = ln p ln(1 − p)，则
   g′(p) = ln(1 − p)/p − ln p/(1 − p)，它在 p < ½ 时为正，在 p > ½ 时为负。所以 f 在 p = ½ 即 k = (m/n) ln 2 时最小，此时
   f = 2^{−k} = 2^{−(m/n) ln 2}。令 f = ε 得 m/n = log₂(1/ε)/ln 2 ≈ 1.44 log₂(1/ε)：1% 时每个元素 9.6 位，k ≈ 6.6。任何以假阳性率
   ε 回答成员查询的结构至少需要 n log₂(1/ε) 位（Carter、Floyd、Gill、Markowsky 与 Wegman，1978），所以布隆过滤器比最小值多用
   44%。布谷鸟过滤器和商过滤器更接近这个下界。

4. **一遍完成的加权抽样。** 给权重为 w_i 的元素 i 赋予键 u_i^{1/w_i}，其中 u_i 在 (0, 1) 上均匀分布，保留键最大的 k 个元素。
   证明这是按权重抽样。

   *解答。* Pr[u_i^{1/w_i} ≤ x] = Pr[u_i ≤ x^{w_i}] = x^{w_i}（x ∈ [0, 1]），所以键的密度为 w_i x^{w_i − 1}。键最大的元素是 i
   的概率为 ∫₀¹ w_i x^{w_i − 1} ∏_{j≠i} x^{w_j} dx = w_i ∫₀¹ x^{W − 1} dx = w_i/W，其中 W = Σ w_j：第一次抽取按权重进行。在最大值
   是 i 的键 x 的条件下，其他键相互独立，且 Pr[key_j ≤ y | key_j ≤ x] = (y/x)^{w_j}，即同一族分布缩放到 [0, x] 上。所以第二大的
   是 j 的概率为 w_j/(W − w_i)，以此类推：最大的 k 个键是 k 个元素的无放回样本，每次在剩下的元素中按权重比例抽取（Efraimidis
   与 Spirakis，2006）。一遍扫描时，用最小堆保存最大的 k 个键，每个元素 O(log k)。

5. **动手：Pebble 上的 HyperLogLog。** 用 Pebble 语言写一个有 256 个寄存器的 HyperLogLog，用反复折半数末尾的零来得到秩，在
   模拟器上对小说运行它，并与精确计数比较。

   *解答要点。* 对每个词使用作业的字母哈希 h = (33h + c) mod 16,777,213。寄存器取 h mod 256。秩是 1 加上 q = h / 256 在保持
   偶数的情况下能被折半的次数：`while q % 2 == 0 && r < 20 { q = q / 2; r = r + 1; }`。每个寄存器保存最大值，共 256 个小整数。
   同一个词每次出现的哈希都相同，所以重复不改变任何东西，正如所需。估计值的计算全部保持在 32 位以内。令
   S = Σ_j 2^{20 − M_j}（M_j 截断到 20），它至多为 2²⁸。然后 E = 256 · ⌊α₂₅₆ · 256 · 2²⁰ / S⌋，其中
   α₂₅₆ · 256 · 2²⁰ ≈ 1.93 × 10⁸ < 2³¹。n ≈ 58,000 时，S 约为 850,000，商约为 226，取整带来的误差不到 0.5%。因为 n ≫ 2.5m，
   不需要线性计数。如果哈希的低位表现得像随机的，误差应约为 1.04/√256 = 6.5%。模素数的多项式哈希并不完全均匀，所以要与精确的
   57,895 比较，并换几个乘数试试。指令数是分词部分的指令数，再加每个词十几条，远低于第 17 部分的哈希表，内存只用 256 个字。

6. **★ 研究问题：去随机化恒等式检验。** 给出一个确定性多项式时间算法，判断一个算术电路计算的是否为零多项式。

   *从哪里开始。* Kabanets 与 Impagliazzo 的《Derandomizing polynomial identity tests means proving circuit lower
   bounds》（2004）解释了这为什么难。综述有 Saxena 的《Progress on polynomial identity testing》（2009，及 2014 年的续篇），以及
   Shpilka 与 Yehudayoff 的《Arithmetic circuits: a survey of recent results and open questions》（2010）。已解决的情形：
   - 顶层扇入有界的深度 3 电路（Kayal 与 Saxena，2007；Saxena 与 Seshadhri，2011）；
   - 只读一次的不经意分支程序，拟多项式时间（Forbes 与 Shpilka，2013；Agrawal、Gurjar、Korwar 与 Saxena，2015）；
   - 自举：对极小电路的命中集就能给出几乎完全的去随机化（Agrawal、Ghosh 与 Saxena，2018）；
   - 常数深度电路的超多项式下界，以及由此得到的常数深度亚指数时间 PIT（Limaye、Srinivasan 与 Tavenas，2021）。

   未解决：
   - （a）公式乃至常数深度电路的多项式时间 PIT；
   - （b）符号行列式的确定性 PIT，它将把完美匹配放进确定性 NC；
   - （c）在这里动手测量：构造第 3 章那些图的 Tutte 矩阵，在 20–40 个顶点的图上，把随机赋值与你能找到的最好的确定性代入（例如
     Fenner、Gurjar 与 Thierauf 的隔离权重）作比较。

## Glossary additions

随机算法 randomized algorithm · 拉斯维加斯算法 Las Vegas algorithm · 蒙特卡洛算法 Monte Carlo algorithm · 单侧错误 one-sided
error · 放大 amplification · 马尔可夫不等式 Markov's inequality · Freivalds 检验 Freivalds' check · 延迟决定原理 principle of
deferred decisions · 多项式恒等式检验 polynomial identity testing · Schwartz–Zippel 引理 Schwartz–Zippel lemma · Tutte 矩阵
Tutte matrix · 完美匹配 perfect matching · 指纹 fingerprint · 最小割 minimum cut · 边收缩 edge contraction · 素性检验 primality
test · 费马伪素数 Fermat pseudoprime · 卡迈克尔数 Carmichael number · 强伪证 strong liar · 随机游走 random walk · 赌徒破产 gambler's
ruin · 球与箱 balls into bins · 两个选择的力量 power of two choices · 布隆过滤器 Bloom filter · 假阳性 false positive · 数据流
data stream · 蓄水池抽样 reservoir sampling · 频繁项 heavy hitters · Count-Min 草图 Count-Min sketch · 保守更新 conservative
update · 双重哈希 double hashing · 基数估计 cardinality estimation · HyperLogLog · 调和平均 harmonic mean · 频率矩 frequency
moment · AMS 草图 AMS sketch · 均值的中位数 median of means · 线性草图 linear sketch · 杰卡德相似度 Jaccard similarity · 瓦片
shingle · 局部敏感哈希 locality-sensitive hashing · 概率方法 probabilistic method · 拉姆齐数 Ramsey number · 洛瓦兹局部引理
Lovász local lemma · 去随机化 derandomization · 条件期望法 method of conditional expectations · 两两独立 pairwise independence ·
伪随机数生成器 pseudorandom generator · 硬度与随机性 hardness versus randomness

## Sources

*Canon.* Books: Motwani & Raghavan, *Randomized Algorithms* (1995); Mitzenmacher & Upfal, *Probability and
Computing* (2nd ed., 2017); Alon & Spencer, *The Probabilistic Method* (4th ed., 2016); Cormode & Yi, *Small
Summaries for Big Data* (2020); Muthukrishnan, *Data Streams: Algorithms and Applications* (2005); Knuth, *The Art
of Computer Programming*, volume 2, chapter 3; Leskovec, Rajaraman & Ullman, *Mining of Massive Datasets*, chapter 3.

Papers: Erdős, "Some remarks on the theory of graphs" (1947); Bloom, "Space/time trade-offs in hash coding with
allowable errors" (1970); Miller, "Riemann's hypothesis and tests for primality" (1976); Freivalds (1977); DeMillo &
Lipton (1978); Zippel (1979); Lovász, "On determinants, matchings, and random algorithms" (1979); Schwartz, "Fast
probabilistic algorithms for verification of polynomial identities" (1980); Rabin, "Probabilistic algorithm for
testing primality" (1980); Misra & Gries, "Finding repeated elements" (1982); Flajolet & Martin, "Probabilistic
counting algorithms for data base applications" (1985); Vitter, "Random sampling with a reservoir" (1985);
Papadimitriou, "On selecting a satisfying truth assignment" (1991); Karger, "Global min-cuts in RNC" (1993); Alford,
Granville & Pomerance, "There are infinitely many Carmichael numbers" (1994); Karger & Stein, "A new approach to the
minimum cut problem" (1996); Alon, Matias & Szegedy, "The space complexity of approximating the frequency moments"
(1996); Broder, "On the resemblance and containment of documents" (1997); Indyk & Motwani, "Approximate nearest
neighbors" (1998); Matsumoto & Nishimura (1998); Azar, Broder, Karlin & Upfal, "Balanced allocations" (1999);
Schöning, "A probabilistic algorithm for k-SAT and constraint satisfaction problems" (1999); Estan & Varghese, "New
directions in traffic measurement and accounting" (2002); Agrawal, Kayal & Saxena, "PRIMES is in P" (2004); Cormode
& Muthukrishnan, "An improved data stream summary: the count-min sketch" (2005); Kirsch & Mitzenmacher, "Less
hashing, same performance" (2006); Flajolet, Fusy, Gandouet & Meunier, "HyperLogLog" (2007); Moser & Tardos, "A
constructive proof of the general Lovász local lemma" (2010); Marsaglia, "Random numbers fall mainly in the planes"
(1968).

*Frontier.* Nisan & Wigderson, "Hardness vs randomness" (1994); Impagliazzo & Wigderson, "P = BPP if E requires
exponential circuits" (1997); Bar-Yossef, Jayram, Kumar & Sivakumar (2002); Kabanets & Impagliazzo (2004);
Reingold, "Undirected connectivity in log-space" (2005); Kane, Nelson & Woodruff, "An optimal algorithm for the
distinct elements problem" (2010); Kawarabayashi & Thorup, "Deterministic edge connectivity in near-linear time"
(2015); Fenner, Gurjar & Thierauf, "Bipartite perfect matching is in quasi-NC" (2016); Chattopadhyay & Zuckerman,
"Explicit two-source extractors and resilient functions" (2016); Svensson & Tarnawski (2017); Campos, Griffiths,
Morris & Sahasrabudhe, "An exponential improvement for diagonal Ramsey" (2023); Henzinger, Li, Rao & Wang,
"Deterministic near-linear time minimum cut in weighted graphs" (2024).
