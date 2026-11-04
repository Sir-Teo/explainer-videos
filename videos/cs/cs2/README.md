# Computer Science, Built — Part 2: Proof and Counting

Part 2 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 1 used proofs without saying what a proof is; this part supplies the mathematics
the rest of the series stands on: logic, the standard proof techniques, induction and invariants, sets and orders,
counting, remainders, chance and graphs. Every search, count and simulation runs on the computer that renders the video
(`compute.py`), and each is checked there against the theorem it illustrates.

* **Fourteen, fifteen.** The 15-puzzle craze of 1880 and the position with 14 and 15 swapped; two numbers watched
  through a random walk (the swap parity of the sixteen squares and the blank's distance from home), which flip
  together; the invariant, and Johnson & Story (1879); breadth-first search over every position of the 2 × 2, 2 × 3 and
  3 × 3 puzzles (exactly half reachable, exactly the half the invariant allows; the 3 × 3's hardest positions need
  31 moves); objectives.
* **1. The grammar of truth.** Propositions and truth tables for ¬, ∧, ∨ (Boole, 1854); implication as a promise, and
  vacuous truth; equivalence, the contrapositive against the converse, De Morgan's laws; predicates, ∀ and ∃, why
  their order matters and how negation flips them; a statement as a game between a prover and a skeptic, with
  continuity's ε–δ and its negation.
* **2. Ways to prove.** Direct proof (odd + odd = even, as pairs of dots); contrapositive (n² even ⇒ n even);
  contradiction: √2 is irrational, with Tennenbaum's picture of infinite descent and the parity proof; Euclid's
  infinitely many primes, and the computed Euclid numbers (30,031 = 59 · 509); proof by cases; a non-constructive proof
  (√2^√2), and why constructive proofs are programs (Part 14).
* **3. Induction.** Dominoes; 1 + … + n, found by a picture and proved by induction; strong induction and the smallest
  counterexample (every n ≥ 2 is a product of primes), and well-ordering; the "all horses are one colour" bug; tiling a
  2ⁿ × 2ⁿ board with one square removed by L-trominoes, the proof run as a recursive algorithm (21 pieces).
* **4. Induction on structures.** Sets defined by rules: balanced brackets; structural induction (the opens-minus-closes
  walk); binary trees have one more leaf than internal node (a 64-team knockout plays 63 games); expressions as trees
  and evaluation by recursion (Parts 12 and 14).
* **5. Invariants.** The state-machine method; the 3- and 5-gallon jugs (a shortest solution in 6 moves, by search)
  and the gcd invariant for other jugs; a diagonal robot and the parity of x + y; termination by a decreasing measure
  (adjacent swaps and the inversion count); loop invariants, Floyd (1967) and Hoare (1969).
* **6. Sets, relations, functions.** Injections, surjections, bijections; equivalence relations and partitions
  (residues mod 3, the puzzle's two classes, Myhill–Nerode in Part 5); partial orders and the Hasse diagram of the
  divisors of 60, lattices (Parts 13 and 39); chains, antichains and Dilworth's theorem (1950).
* **7. Sizes of infinity.** The positive rationals listed without repeats by the Calkin–Wilf tree (2000); Cantor's
  pairing function; Cantor–Schröder–Bernstein; Cantor's theorem (no set maps onto its subsets) and the tower of
  infinities.
* **8. Counting.** The sum and product rules (62⁸ passwords); permutations, combinations and dividing out an
  overcount; Pascal's triangle and its combinatorial proof; the binomial theorem; Pascal mod 2 is Sierpiński's
  triangle (128 rows, computed; Lucas's theorem); Vandermonde's identity by counting twice; stars and bars.
* **9. Pigeons.** The pigeonhole principle and its generalization; Erdős–Szekeres (1935), proved by labels, with the
  sharp example and the longest increasing subsequence of random permutations (computed up to n = 100,000: ≈ 2√n); no
  lossless compressor shrinks every input.
* **10. Inclusion and exclusion.** Unions of two and three sets (multiples of 2, 3 or 5 up to 100: 74); derangements
  and the hat-check problem (D₄ = 9, listed), D(n)/n! → 1/e with simulations, Bonferroni's alternating bounds; Euler's φ
  by inclusion–exclusion, for every n ≤ 60.
* **11. Counting by recursion.** Square-and-domino tilings and Fibonacci; the Catalan numbers as brackets, binary
  trees, triangulations and mountain ranges, matched by bijections; the Catalan recurrence and closed form; Stirling
  numbers of the second kind and the Bell numbers.
* **12. Numbers.** The extended Euclidean algorithm with its invariant, and Bézout (21 = −3 · 1071 + 7 · 462);
  congruences on a clock (the last digit of 7¹⁰⁰); inverses modulo m; Sunzi's remainder problem and the Chinese
  remainder theorem, by three clocks and by construction; unique factorization via Euclid's lemma.
* **13. Chance.** Monty Hall, simulated (3,000 games); conditional probability and Bayes as counting (a test that is
  99% sensitive but right about only one positive in six); indicators and linearity of expectation (one fixed point on
  average, for every n, against Poisson(1)); Markov, Chebyshev and the exact tail for 100 coins; the union bound and
  the birthday problem.
* **14. Graphs.** Königsberg (Euler, 1736); the handshake lemma; trees and their equivalent definitions; two-colouring
  and odd cycles.
* **15. Frontier: order in chaos.** Ramsey numbers. R(3,3) = 6 by the pigeonhole principle (the pentagon colouring
  of K₅; all 32,768 colourings of K₆ checked, none escapes); R(4,4) = 18 (the Paley graph on 17 vertices, its
  largest cliques and independent sets of size 3, checked; Greenwood and Gleason, 1955); Erdős and Szekeres's upper
  bound (1935) and Erdős's probabilistic lower bound (1947), √2ᵏ < R(k) < 4ᵏ; Thomason (1988) and Conlon (2009); the
  first exponential improvement, R(k) < (4 − 2⁻⁷)ᵏ (Campos, Griffiths, Morris and Sahasrabudhe, 2023), and 3.8^(k+o(k))
  (Gupta, Ndiaye, Norin and Wei, 2024); 43 ≤ R(5,5) ≤ 46 (Angeltveit and McKay, 2024). The open problem of explicit
  Ramsey colourings: Paley clique numbers computed for primes up to 400 (they grow like log q; the provable bound is of
  order √q).
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs2.compute            # every number in the part (about half a minute)
python tools/build.py cs2 -q l             # a 480p preview
python tools/build.py cs2                  # 1080p
```

## Problems, with solutions

1. **Odd numbers.** Prove 1 + 3 + 5 + ⋯ + (2n − 1) = n², and draw the picture.

   *Solution.* For n = 1 both sides are 1. If the sum of the first n odd numbers is n², adding the next, 2n + 1, gives
   n² + 2n + 1 = (n + 1)². The picture: an n × n square of dots grows to (n + 1) × (n + 1) by adding an L-shaped border
   of n + n + 1 = 2n + 1 dots.

2. **The 3 × 3 puzzle.** Is the position with only 1 and 2 swapped, the blank in its corner, reachable?

   *Solution.* No. It is one swap from the solved position (odd parity) with the blank at distance 0, so the invariant
   (swap parity + blank distance) is odd, while every reachable position has it even. Breadth-first search confirms
   it: the reachable set has 181,440 positions and this one is not among them.

3. **Five points in a square.** Show two of any 5 points in a unit square are at distance at most √2/2.

   *Solution.* Cut the square into four squares of side 1/2. Five points, four squares: two points share a small
   square, and two points in a square of side 1/2 are at most its diagonal apart, √2/2.

4. **Derangements.** Count the derangements of 5 items and prove D(n) = (n − 1)(D(n − 1) + D(n − 2)).

   *Solution.* D(5) = 120 − 120 + 60 − 20 + 5 − 1 = **44** (inclusion–exclusion, or brute force). For the recurrence,
   in a derangement person n gets some other person i's hat: n − 1 choices of i. Either i gets n's hat (a swap; the
   other n − 2 people are deranged: D(n − 2)), or i does not — then forbid i from n's hat as if it were their own, and
   the n − 1 people other than n form a derangement: D(n − 1). So D(n) = (n − 1)(D(n − 1) + D(n − 2)).

5. **Three remainders.** Find x with x ≡ 1 (mod 4), x ≡ 2 (mod 5), x ≡ 3 (mod 7).

   *Solution.* M = 140. The terms: 1 · 35 · (35⁻¹ mod 4 = 3) = 105; 2 · 28 · (28⁻¹ mod 5 = 2) = 112;
   3 · 20 · (20⁻¹ mod 7 = 6) = 360. Sum 577 ≡ **17** (mod 140). Check: 17 = 4 · 4 + 1 = 3 · 5 + 2 = 2 · 7 + 3.

6. **Build: the 2 × 4 puzzle.** Run the search on the 2 × 4 board.

   *Solution.* `bfs((1, 2, 3, 4, 5, 6, 7, 0), 2, 4)` reaches **20,160** positions, half of 8!, as the invariant
   predicts; the farthest is **36** moves away, and there is exactly one such position.

7. **★ Research: Paley cliques.** Compute the largest clique of the Paley graph P_q (vertices 0, …, q − 1, with i and
   j adjacent when i − j is a nonzero square mod q) for primes q ≡ 1 (mod 4) up to 1000. Open: prove that it is at
   most (log q)^C for some constant C.

   *What is known, and where to start.* `compute_ramsey` in `videos/cs/cs2/compute.py` finds the clique numbers up
   to q = 400 in about seven minutes with a plain branch-and-bound; the largest found is 9. To reach 1000, use the
   symmetry: P_q is vertex-transitive (x ↦ x + c) and the map x ↦ ax for a square a fixes 0 and permutes its
   neighbours, so a largest clique can be assumed to contain 0 and 1, and the search runs inside the common
   neighbourhood of 0 and 1, about q/4 vertices. A colouring-based bound (as in Östergård's *cliquer*) prunes far
   more. On the theory side, the trivial bound is √q; Hanson and Petridis (2021) proved about √(q/2), and nothing of
   the form q^(1/2 − ε) is known for prime q. Random graphs have clique number about 2 log₂ q, and every computation
   suggests Paley graphs do no worse. A proof would give explicit Ramsey colourings, a problem open since 1947, and
   would matter for pseudorandomness (Parts 20 and 27).

## 习题与解答

1. **奇数之和。** 证明 1 + 3 + 5 + ⋯ + (2n − 1) = n²，并画出提示它的图。

   *解答。* n = 1 时两边都是 1。若前 n 个奇数之和为 n²，再加上下一个奇数 2n + 1，得 n² + 2n + 1 = (n + 1)²。图：n × n 的点阵加上一条
   由 n + n + 1 = 2n + 1 个点组成的 L 形边框，就变成 (n + 1) × (n + 1)。

2. **3 × 3 华容道。** 只交换 1 和 2、空格在角上的局面，能走到吗？

   *解答。* 不能。它与复原局面只差一次交换（奇置换），空格距离为 0，所以不变量（交换奇偶性 + 空格距离）为奇数，而每个可达局面它都是偶
   数。广度优先搜索也证实了：可达集合有 181,440 个局面，这个局面不在其中。

3. **正方形里的五个点。** 证明单位正方形内任意 5 个点中，必有两点距离不超过 √2/2。

   *解答。* 把正方形切成四个边长 1/2 的小正方形。五个点放进四个小正方形，必有两点落在同一个里，而同一个小正方形里两点的距离不超过
   它的对角线 √2/2。

4. **错排。** 求 5 个元素的错排数，并用计数论证证明 D(n) = (n − 1)(D(n − 1) + D(n − 2))。

   *解答。* D(5) = 120 − 120 + 60 − 20 + 5 − 1 = **44**。递推：错排中第 n 个人拿到某个人 i 的帽子，i 有 n − 1 种选择。若 i 恰好拿到 n
   的帽子（两人互换，其余 n − 2 人错排：D(n − 2)）；否则，把“n 的帽子”当作 i 自己的帽子禁止 i 拿，除 n 以外的 n − 1 人构成一个错排：
   D(n − 1)。所以 D(n) = (n − 1)(D(n − 1) + D(n − 2))。

5. **三个余数。** 求 x，使 x ≡ 1 (mod 4)，x ≡ 2 (mod 5)，x ≡ 3 (mod 7)。

   *解答。* M = 140。各项：1 · 35 · 3 = 105；2 · 28 · 2 = 112；3 · 20 · 6 = 360。和为 577 ≡ **17** (mod 140)。验证：17 = 4 · 4 + 1 =
   3 · 5 + 2 = 2 · 7 + 3。

6. **动手：2 × 4 华容道。** 在 2 × 4 的棋盘上运行本部分的搜索。

   *解答。* `bfs((1, 2, 3, 4, 5, 6, 7, 0), 2, 4)` 可达 **20,160** 个局面，正好是 8! 的一半，与不变量的预言一致；最远的局面需要
   **36** 步，而且只有一个。

7. **★ 研究题：Paley 图的团。** 对素数 q ≡ 1 (mod 4)，q 不超过 1000，计算 Paley 图 P_q（顶点 0, …, q − 1，当 i − j 是模 q
   的非零平方数时 i 与 j 相邻）的最大团。未解：证明它至多是 (log q)^C，C 是某个常数。

   *已知什么，从哪里入手。* `videos/cs/cs2/compute.py` 里的 `compute_ramsey` 用普通的分支定界法，大约七分钟算出 q ≤ 400 的团数；
   找到的最大值是 9。要算到 1000，就利用对称性：P_q 是顶点传递的（x ↦ x + c），而对平方数 a，映射 x ↦ ax 保持 0 不动并置换它的邻居，
   所以可以假定最大团包含 0 和 1，只需在 0 和 1 的公共邻域（约 q/4 个顶点）里搜索。基于着色的上界（如 Östergård 的 *cliquer*）
   剪枝效果好得多。理论上，平凡的上界是 √q；Hanson 和 Petridis（2021）证明了约 √(q/2)，对素数 q 还不知道任何形如 q^(1/2 − ε)
   的界。随机图的团数约为 2 log₂ q，而所有计算都表明 Paley 图不比它差。一个证明将给出显式的拉姆齐着色，这个问题自1947年起悬而未决，
   也会影响伪随机性的研究（第20、27部分）。

## Glossary additions

不变量 invariant · 变式（递减量） variant · 结构归纳法 structural induction · 良序原理 well-ordering principle ·
逆否命题 contrapositive · 逆命题 converse · 空真 vacuous truth · 单射 / 满射 / 双射 injection / surjection / bijection ·
等价关系 equivalence relation · 偏序 partial order · 格 lattice · 链 / 反链 chain / antichain · 鸽巢原理 pigeonhole principle ·
容斥原理 inclusion–exclusion · 错排 derangement · 卡特兰数 Catalan numbers · 第二类斯特林数 Stirling numbers of the second
kind · 同余 congruence · 中国剩余定理 Chinese remainder theorem · 期望的线性性 linearity of expectation · 二分图 bipartite graph

## Sources

Books: Lehman, Leighton & Meyer, *Mathematics for Computer Science*; Rosen, *Discrete Mathematics and Its
Applications*; Graham, Knuth & Patashnik, *Concrete Mathematics*; Velleman, *How to Prove It*; Pólya, *How to Solve
It*; Aigner & Ziegler, *Proofs from THE BOOK*; Stanley, *Enumerative Combinatorics*, vol. 1, ch. 1.

Papers and documents: Euler on the Königsberg bridges (1736); Boole, *The Laws of Thought* (1854); Johnson & Story,
"Notes on the '15' puzzle", *American Journal of Mathematics* (1879); Erdős & Szekeres (1935); Dilworth (1950);
Floyd, "Assigning meanings to programs" (1967); Hoare, "An axiomatic basis for computer programming" (1969); Vershik
& Kerov, and Logan & Shepp (1977); Calkin & Wilf, "Recounting the rationals" (2000); *Sunzi Suanjing* (c. 400).
