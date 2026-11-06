# Computer Science, Built — Part 27: Proofs and Randomness

Part 27 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act V, *Limits and Secrets*. A proof used to be a document read from
beginning to end. With randomness, a verifier can check a proof by reading a few bits of it, by asking a prover random
questions, or without learning anything but the truth of the statement. This part builds those protocols and runs them,
then follows the PCP theorem to the limits of approximation and the finer questions that remain once P versus NP is set
aside.

The instrument is `explainer/cs/algo/proofs.py`. It holds:
* binomial tails in log space; fingerprints of strings as polynomials over a prime field;
* random DNFs, random restrictions and exact decision-tree depth (the switching lemma, measured);
* arithmetization of CNF formulas, Lagrange interpolation and the **sum-check protocol**, with an honest prover for #SAT
  and a cheating one that adds a polynomial vanishing at 0 and 2, …, d;
* the graph non-isomorphism protocol; **zero-knowledge 3-colouring** with SHA-256 commitments, and its simulator;
* the BLR linearity test's exact rejection rate and the distance to the nearest parity; WalkSAT;
* vertex cover by bounded search tree, Buss's kernel and brute force;
* Ryser's permanent (Gray code) against Bareiss's determinant; a determinant modulo p and the Vandermonde identity test;
* orthogonal vectors, 3SUM, and Williams's reduction from SAT to orthogonal vectors;
* unique games with a planted labelling, and propagation along a BFS tree;
* planted clique with the degree heuristic; Pollard's rho with Brent's cycle detection.

It is tested in `tests/test_cs27_proofs.py`. The tests check:
* the tails against exact sums;
* that the fingerprints never err on equal strings;
* that honest sum-check transcripts always verify;
* that the ZK commitments open correctly;
* BLR on parities, and the vertex-cover routines against brute force;
* Ryser against the permutation sum;
* SAT-to-OV against brute force;
* propagation on uncorrupted unique games;
* planted-clique recovery, and the factors rho returns;
* the Vandermonde test.

* **Checking without reading.** Hook.
  - Three ways to be convinced: sampling a proof, a conversation, a proof that reveals nothing.
* **1. Randomized classes.**
  - Gill's RP, coRP, ZPP and BPP.
  - Amplification by majority vote: error 1/3 at one run, 2.7 × 10⁻⁴ at 101 runs.
  - Adleman's theorem in numbers: 1,131 runs fix one advice string for every input of length 100.
  - Sipser–Gács–Lautemann.
* **2. Hardness against randomness.**
  - The Nisan–Wigderson generator.
  - Polynomial identity testing: the Vandermonde identity with ten variables (3,628,800 terms if expanded) is tested at
    random points in about 0.1 ms. A false variant passes 36% of the time mod 101 (bound 45%), and never mod 10⁶.
  - Impagliazzo–Wigderson; Kabanets–Impagliazzo; AKS.
* **3. Circuit lower bounds.**
  - Karp–Lipton.
  - A random 3-DNF collapsing under a random restriction, then 1,500 restrictions per p measured against Håstad's
    bound (5pw)ᵗ.
  - Razborov–Smolensky, monotone clique, Williams's ACC⁰ bound.
* **4. Communication complexity.**
  - Equality by fingerprints: 0 errors in 20,000 trials with q = 1,000,003. With 10¹²-bit strings, 162 bits replace a
    trillion.
  - Fooling sets and rank; disjointness; why streaming must approximate.
* **5. Interactive proofs.**
  - Graph non-isomorphism, with five-vertex graphs: the honest prover is always right, a bluffer half the time.
  - GMR and Babai's Arthur–Merlin games.
* **6. Sum-check and IP = PSPACE.**
  - A 5-clause formula on 4 variables as a polynomial mod 97. The honest transcript proves 7 satisfying assignments,
    round by round.
  - The cheater survives 19.3% of 3,000 runs against the bound 1 − (1 − 5/97)⁴ = 19.1%, and never over a field of a million.
  - Shamir's theorem.
* **7. Zero knowledge.**
  - Ali Baba's cave; GMW's 3-colouring protocol on the Petersen graph with hashed commitments.
  - A colouring with 2 bad edges out of 15 survives k rounds with probability (13/15)ᵏ: 47% at 5 rounds, 5.6% at 20,
    below 10⁻⁹ at 301.
  - The simulator's transcripts have the same colour-pair frequencies (about 1/6 each) as real ones.
* **8. The PCP theorem.**
  - The statement.
  - The BLR test on functions of 8 bits: the exact rejection rate follows 3δ − 6δ² for small δ.
  - Dinur's gap amplification.
* **9. Hardness of approximation.**
  - The gap view.
  - MAX-3SAT: random assignments satisfy 87.5% (Håstad: optimal), WalkSAT 96.6–100% on random formulas.
  - Tight bounds for set cover, clique, MAX-3LIN; the gaps for vertex cover and MAX-CUT.
* **10. The Unique Games Conjecture.**
  - Unique games and propagation. On 3,000 vertices and 9,000 edges with 7 labels, propagation falls from 100% to 83%
    at 5% corruption and 50% at 20%; random labels get 13.5%.
  - The SDP of Charikar–Makarychev–Makarychev; Khot–Regev, KKMO, Raghavendra; Arora–Barak–Steurer; the 2-to-2 theorem.
* **11. Fine-grained complexity.**
  - SETH, 3SUM and APSP.
  - Williams's reduction run on six random 3-SAT formulas with 24 variables. Each side has 4,096 vectors, so there
    are 2²⁴ pairs, and the OV answer matches our CDCL solver every time.
  - OV and 3SUM measured as quadratic (0.6–0.75 s at n = 4,000); Grønlund–Pettie.
* **12. Parameterized complexity.**
  - Bounded search trees on 40-vertex graphs: 7,677 nodes at k = 12 against 5.6 × 10⁹ subsets.
  - Buss's kernel; FPT and W[1]; treewidth and Courcelle.
* **13. Counting.**
  - #P; the permanent against the determinant. Ryser at n = 20 counts 2,244,446,046,392 perfect matchings in 2.3 s;
    Bareiss takes 0.28 ms, and 0.76 s at n = 200.
  - Toda, Valiant–Vazirani, Stockmeyer, Jerrum–Sinclair–Vigoda, Kasteleyn.
* **14. Average case and one-way functions.**
  - Planted clique in G(1000, ½): the degree heuristic recovers nothing below k = 70, 70% at 70, and all from 80
    (√(n ln n) ≈ 83).
  - Multiplying primes against Pollard's rho: 46 ns against 0.49 s at 80 bits.
  - Levin; HILL; Ajtai; Regev's LWE; Feigenbaum–Fortnow and Bogdanov–Trevisan.
* **15. Frontier: MIP\* = RE and proofs in practice.**
  - NP, IP, MIP = NEXP, MIP\* = RE; Tsirelson and Connes.
  - Succinct arguments: Kilian, Micali, GKR, Groth16, rollups, zkVMs.
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs27.compute           # every number in the part (about two minutes)
python tools/build.py cs27 -q l            # a 480p preview
python tools/build.py cs27                 # 1080p
```

## Problems, with solutions

1. **Amplification.** Show that O(k) independent runs and a majority vote reduce a BPP algorithm's error from ⅓ to
   2⁻ᵏ.

   *Solution.* Run the algorithm t times and let X be the number of correct answers, a sum of t independent
   indicators each with mean at least ⅔. The vote is wrong only if X ≤ t/2, that is, if X falls at least t/6 below
   its mean. Hoeffding's form of the Chernoff bound gives Pr[X ≤ t/2] ≤ exp(−2t(1/6)²) = e^{−t/18}. Taking
   t = ⌈18 k ln 2⌉ ≈ 12.5k makes this at most 2⁻ᵏ. Chapter 1 measured the exact binomial tail: 101 runs already
   give 2.7 × 10⁻⁴.

2. **Equality needs n bits deterministically.** Prove that a deterministic protocol for EQ on n-bit strings
   communicates at least n bits.

   *Solution.* A deterministic protocol partitions the 2ⁿ × 2ⁿ input matrix into monochromatic rectangles, one per
   leaf of its tree. Consider the 2ⁿ inputs (x, x), each with answer 1. If (x, x) and (y, y) with x ≠ y lay in the
   same rectangle A × B, then x ∈ A and y ∈ B, so (x, y) would lie in it too and get answer 1, but x ≠ y. So these
   inputs need 2ⁿ distinct 1-rectangles, and at least one more leaf answers 0. A tree with more than 2ⁿ leaves has
   depth at least n + 1, so some input costs n + 1 bits. Fingerprints need only O(log n).

3. **Sum-check soundness.** Prove that a cheating prover survives with probability at most nd/p.

   *Solution.* Let H = Σ_{x∈{0,1}ⁿ} g(x) and suppose the claim C ≠ H. In round i the verifier holds a claimed value
   cᵢ₋₁ (c₀ = C) for Σ g(r₁, …, rᵢ₋₁, xᵢ, …, xₙ), and the true univariate polynomial is hᵢ(X) = Σ g(r₁, …, rᵢ₋₁, X,
   xᵢ₊₁, …). The prover sends gᵢ of degree at most d, and the verifier checks gᵢ(0) + gᵢ(1) = cᵢ₋₁. Suppose cᵢ₋₁ is
   false. If gᵢ = hᵢ the check fails, since hᵢ(0) + hᵢ(1) is the true value. So a surviving prover sends gᵢ ≠ hᵢ, and
   two distinct polynomials of degree d agree on at most d points. Hence Pr[gᵢ(rᵢ) = hᵢ(rᵢ)] ≤ d/p. Unless that
   happens, the next claim cᵢ = gᵢ(rᵢ) is false again. At the end the verifier evaluates g(r₁, …, rₙ) itself and
   catches a false cₙ. A union bound over the n rounds gives survival at most nd/p. (Surviving every round
   independently gives the slightly sharper 1 − (1 − d/p)ⁿ.) Chapter 6 measured 19.3% against 1 − (1 − 5/97)⁴ =
   19.1%, within the sampling error of 3,000 runs; nd/p itself is 20.6%.

4. **Buss's kernel.** Show that after Buss's rule a yes-instance has at most k² edges and k² + k non-isolated
   vertices.

   *Solution.* A vertex v of degree greater than k must be in every cover of size at most k: otherwise all its
   neighbours, more than k of them, would be. So the rule takes v into the cover and decrements k. When no vertex
   has degree above the remaining budget k′ ≤ k, any cover of size k′ covers at most k′ · k′ ≤ k² edges, one vertex at
   a time. If more edges remain, answer no. Otherwise every non-isolated vertex is in the cover (at most k) or adjacent
   to a cover vertex (at most k · k), which gives k² + k. Isolated vertices are deleted. The kernel has size O(k²)
   and is computed in linear time.

5. **Build: non-interactive sum-check.** Make chapter 6's sum-check non-interactive with Fiat–Shamir and verify a proof
   for a 20-variable formula.

   *Solution.* Work modulo a large prime, say p = 2⁶¹ − 1, so the soundness error nd/p is negligible. The prover
   computes the claim C = #SAT. In round i, it computes gᵢ with `proofs.honest_message`, and sets the challenge
   rᵢ = SHA-256(formula ‖ C ‖ g₁ ‖ … ‖ gᵢ) mod p, hashing the whole transcript so far. The proof is the list of
   coefficient vectors. The verifier recomputes every rᵢ from the same hashes, checks gᵢ(0) + gᵢ(1) = gᵢ₋₁(rᵢ₋₁)
   (and g₁(0) + g₁(1) = C), and finally evaluates the arithmetized formula at (r₁, …, r₂₀) with `arith_eval`.
   Hashing everything prevents the prover from choosing gᵢ after seeing rᵢ. In the random-oracle model, a
   cheater must try about p/(nd) transcripts per success. For a formula with m clauses the proof is 20 polynomials
   of degree at most m. The verifier does 20 hashes and one evaluation; the prover does about 2²⁰ evaluations per
   round. Hashing only gᵢ, and not the formula and claim, is a classic bug: it lets a prover forge proofs of false
   claims.

6. ★ **Research: the exact soundness of linearity testing.** For functions on n ≤ 4 bits, find by exhaustive search
   the minimum BLR rejection rate at each distance δ, and compare it with 3δ − 6δ², δ, and the known bounds.

   *Where to start.* Bellare, Coppersmith, Håstad, Kiwi and Sudan (1996) proved that the rejection rate is at least
   3δ − 6δ² (tight for δ ≤ 5/16), at least 45/128 for 5/16 ≤ δ ≤ 45/128, and at least δ beyond. Kaufman, Litsyn and
   Xie (2010) improved the bound near δ = ½. Exhaustive search is easy for n = 3 (256 functions) and n = 4 (65,536,
   seconds with numpy). For n = 4 the minimum equals 3δ − 6δ² at every distance up to 5/16, and exceeds it beyond
   (0.469 at δ = 6/16). n = 5 has 2³² functions. The rejection rate is invariant under adding a linear function and
   under invertible linear changes of variable, so search one representative of each class under that group. Then ask
   how the exact minimum behaves between 5/16 and ½ as n grows, and whether a cleaner closed form fits it.

## 习题与解答

1. **放大。** 证明 O(k) 次独立运行并多数表决，能把 BPP 算法的错误率从 ⅓ 降到 2⁻ᵏ。

   *解答。* 运行 t 次，设 X 为答对的次数，它是 t 个独立指示变量之和，每个的均值至少为 ⅔。只有当 X ≤ t/2，即 X 比均值低至少 t/6 时，表决才会出错。
   Chernoff 界的 Hoeffding 形式给出 Pr[X ≤ t/2] ≤ exp(−2t(1/6)²) = e^{−t/18}。取 t = ⌈18 k ln 2⌉ ≈ 12.5k，就使它至多为 2⁻ᵏ。第 1 章计算了
   精确的二项式尾部：101 次运行就已达到 2.7 × 10⁻⁴。

2. **确定性地判定相等需要 n 位。** 证明 n 位串上 EQ 的任何确定性协议至少要通信 n 位。

   *解答。* 确定性协议把 2ⁿ × 2ⁿ 的输入矩阵划分成单色矩形，协议树的每片叶子对应一个。考虑 2ⁿ 个输入 (x, x)，答案都是 1。若 x ≠ y 时 (x, x) 与
   (y, y) 落在同一个矩形 A × B 中，则 x ∈ A、y ∈ B，于是 (x, y) 也在其中，答案为 1，但 x ≠ y。所以这些输入需要 2ⁿ 个不同的 1-矩形，另外至少还有
   一片叶子回答 0。叶子多于 2ⁿ 片的树深度至少为 n + 1，所以某个输入要花 n + 1 位。指纹法只需 O(log n) 位。

3. **sum-check 的可靠性。** 证明作弊的证明者存活的概率至多为 nd/p。

   *解答。* 设 H = Σ_{x∈{0,1}ⁿ} g(x)，并假设声称值 C ≠ H。第 i 轮验证者持有声称值 cᵢ₋₁（c₀ = C），它声称等于 Σ g(r₁, …, rᵢ₋₁, xᵢ, …, xₙ)；真实的
   单变量多项式是 hᵢ(X) = Σ g(r₁, …, rᵢ₋₁, X, xᵢ₊₁, …)。证明者发来次数至多为 d 的 gᵢ，验证者检查 gᵢ(0) + gᵢ(1) = cᵢ₋₁。若 cᵢ₋₁ 是假的，而 gᵢ = hᵢ，
   检查就会失败，因为 hᵢ(0) + hᵢ(1) 是真值；所以存活的证明者发的是 gᵢ ≠ hᵢ。两个不同的 d 次多项式至多在 d 个点上相等，所以 Pr[gᵢ(rᵢ) = hᵢ(rᵢ)] ≤ d/p；
   除非这件事发生，下一个声称值 cᵢ = gᵢ(rᵢ) 仍是假的。最后验证者亲自计算 g(r₁, …, rₙ)，揭穿假的 cₙ。对 n 轮取并集界，存活率至多为 nd/p（逐轮独立地看，可得稍紧的
   1 − (1 − d/p)ⁿ）。第 6 章测得 19.3%，而 1 − (1 − 5/97)⁴ = 19.1%，在 3,000 次运行的抽样误差之内；nd/p 本身是 20.6%。

4. **Buss 核。** 证明经 Buss 规则处理后，“是”实例至多有 k² 条边和 k² + k 个非孤立顶点。

   *解答。* 度数大于 k 的顶点 v 必在每个规模至多为 k 的覆盖中，否则它的全部邻居（多于 k 个）都得在覆盖里。所以规则把 v 放进覆盖并把 k 减一。当没有顶点的
   度数超过剩余预算 k′ ≤ k 时，规模为 k′ 的覆盖逐个顶点地至多覆盖 k′ · k′ ≤ k² 条边；若剩下的边更多，就回答“否”。否则每个非孤立顶点要么在覆盖中（至多
   k 个），要么与某个覆盖顶点相邻（至多 k · k 个），共 k² + k 个。孤立顶点直接删去。核的规模为 O(k²)，可在线性时间内算出。

5. **动手：非交互的 sum-check。** 用 Fiat–Shamir 把第 6 章的 sum-check 变成非交互的，并验证一个 20 变量公式的证明。

   *解答。* 在一个大素数下运算，比如 p = 2⁶¹ − 1，使可靠性误差 nd/p 可以忽略。证明者算出声称值 C = #SAT；第 i 轮用 `proofs.honest_message` 算出 gᵢ，
   并令挑战 rᵢ = SHA-256(公式 ‖ C ‖ g₁ ‖ … ‖ gᵢ) mod p，即对迄今的整个记录取哈希。证明就是这些系数向量的列表。验证者用同样的哈希重算每个 rᵢ，检查
   gᵢ(0) + gᵢ(1) = gᵢ₋₁(rᵢ₋₁)（以及 g₁(0) + g₁(1) = C），最后用 `arith_eval` 在 (r₁, …, r₂₀) 处计算算术化的公式。对所有内容取哈希，可以防止证明者在看到
   rᵢ 之后再选 gᵢ；在随机预言机模型中，作弊者每成功一次需要尝试约 p/(nd) 份记录。对含 m 个子句的公式，证明是 20 个次数至多为 m 的多项式；验证者做 20 次
   哈希和一次求值，证明者每轮约做 2²⁰ 次求值。只对 gᵢ 取哈希而不包括公式和声称值，是一个经典漏洞：它让证明者能为假的声称伪造证明。

6. ★ **研究：线性性测试的精确可靠性。** 对 n ≤ 4 位的函数，穷举求出每个距离 δ 下 BLR 测试的最小拒绝率，并与 3δ − 6δ²、δ 以及已知的界比较。

   *从哪里入手。* Bellare、Coppersmith、Håstad、Kiwi 与 Sudan（1996）证明拒绝率至少为 3δ − 6δ²（δ ≤ 5/16 时是紧的），在 5/16 ≤ δ ≤ 45/128 时至少为
   45/128，再往后至少为 δ；Kaufman、Litsyn 与 Xie（2010）改进了 δ 接近 ½ 时的界。n = 3（256 个函数）和 n = 4（65,536 个，用 numpy 只需几秒）的穷举都很容易。
   n = 4 时，在 5/16 以内的每个距离上最小值都等于 3δ − 6δ²，再往后则超过它（δ = 6/16 时为 0.469）。n = 5 有 2³² 个函数：拒绝率在加上线性函数和可逆
   线性变量替换下不变，所以只需在这个群的每个轨道里搜一个代表。然后研究：随着 n 增大，精确最小值在 5/16 与 ½ 之间如何变化，能否拟合出更简洁的闭式。

## Glossary additions

随机多项式时间 RP · 零错误概率多项式时间 ZPP · 有界错误概率多项式时间 BPP · 放大 amplification · 非一致 non-uniform ·
伪随机生成器 pseudorandom generator · 去随机化 derandomization · 多项式恒等测试 polynomial identity testing · 随机限制 random restriction ·
切换引理 switching lemma · 通信复杂度 communication complexity · 指纹 fingerprint · 欺骗集 fooling set · 交互式证明 interactive proof ·
Arthur–Merlin 博弈 Arthur–Merlin game · 算术化 arithmetization · sum-check 协议 sum-check protocol · 零知识 zero knowledge · 承诺 commitment ·
模拟器 simulator · 概率可检验证明 probabilistically checkable proof (PCP) · 线性性测试 linearity test · 间隙放大 gap amplification ·
近似难度 hardness of approximation · 唯一博弈猜想 Unique Games Conjecture · 细粒度复杂性 fine-grained complexity · 正交向量 orthogonal vectors ·
强指数时间假设 SETH · 参数化复杂性 parameterized complexity · 固定参数可解 FPT · 核化 kernelization · 树宽 treewidth · 积和式 permanent ·
#P 完全 #P-complete · 植入团 planted clique · 单向函数 one-way function · 简洁论证 succinct argument · 纠缠 entanglement

## Sources

*Canon.* Books:
- Arora & Barak, *Computational Complexity: A Modern Approach* (2009), ch. 7–11, 13–14, 18–22;
- Goldreich, *Computational Complexity: A Conceptual Perspective* (2008);
- Wigderson, *Mathematics and Computation* (2019);
- Kushilevitz & Nisan, *Communication Complexity* (1997);
- Jukna, *Boolean Function Complexity* (2012);
- Thaler, *Proofs, Arguments, and Zero-Knowledge* (2022);
- Cygan et al., *Parameterized Algorithms* (2015);
- O'Donnell, *Analysis of Boolean Functions* (2014).

Papers:
- Randomness: Gill (1977); Adleman (1978); Sipser (1983); Lautemann (1983); Nisan & Wigderson (1994); Impagliazzo &
  Wigderson (1997); Kabanets & Impagliazzo (2004); Schwartz (1980); Zippel (1979); DeMillo & Lipton (1978); Agrawal,
  Kayal & Saxena (2004).
- Circuits and communication: Furst, Saxe & Sipser (1984); Ajtai (1983); Håstad (1986); Razborov (1985, 1987);
  Smolensky (1987); Karp & Lipton (1980); Williams (2011); Yao (1979); Kalyanasundaram & Schnitger (1992); Razborov
  (1992); Alon, Matias & Szegedy (1996).
- Interaction and zero knowledge: Goldwasser, Micali & Rackoff (1985); Babai (1985); Goldreich, Micali & Wigderson
  (1986, 1991); Goldwasser & Sipser (1986); Lund, Fortnow, Karloff & Nisan (1990); Shamir (1990); Fiat & Shamir
  (1986).
- PCP and approximation: Feige, Goldwasser, Lovász, Safra & Szegedy (1991); Arora & Safra (1992); Arora, Lund,
  Motwani, Sudan & Szegedy (1992); Blum, Luby & Rubinfeld (1990); Bellare, Coppersmith, Håstad, Kiwi & Sudan (1996);
  Håstad (1999, 2001); Feige (1998); Dinur & Steurer (2014); Zuckerman (2007); Trevisan, Sorkin, Sudan & Williamson
  (2000); Dinur (2007); Kaufman, Litsyn & Xie (2010).
- Unique games: Khot (2002); Khot & Regev (2008); Khot, Kindler, Mossel & O'Donnell (2007); Raghavendra (2008);
  Charikar, Makarychev & Makarychev (2006); Arora, Barak & Steurer (2010); Khot, Minzer & Safra (2018).
- Fine-grained and parameterized: Gajentaan & Overmars (1995); Williams (2005); Backurs & Indyk (2015); Grønlund &
  Pettie (2014); Vassilevska Williams & Williams (2010); Vassilevska Williams (2018, survey); Buss & Goldsmith (1993);
  Downey & Fellows (1995, 1999); Chen, Kanj & Xia (2010); Courcelle (1990).
- Counting and average case: Valiant (1979); Ryser (1963); Toda (1991); Valiant & Vazirani (1986); Stockmeyer (1983);
  Jerrum, Sinclair & Vigoda (2004); Kasteleyn (1961); Temperley & Fisher (1961); Levin (1986); Håstad, Impagliazzo,
  Levin & Luby (1999); Ajtai (1996); Regev (2005); Feigenbaum & Fortnow (1993); Bogdanov & Trevisan (2006); Kučera
  (1995); Alon, Krivelevich & Sudakov (1998); Pollard (1975); Brent (1980); Boudot et al., RSA-250 (2020).
- Frontier: Ben-Or, Goldwasser, Kilian & Wigderson (1988); Babai, Fortnow & Lund (1991); Ji, Natarajan, Vidick,
  Wright & Yuen, "MIP* = RE" (2020); Kilian (1992); Micali (1994); Goldwasser, Kalai & Rothblum (2008); Groth (2016);
  Ben-Sasson et al., Zerocash (2014) and STARKs (2018).
