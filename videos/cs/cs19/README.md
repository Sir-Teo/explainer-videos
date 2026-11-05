# Computer Science, Built — Part 19: The Great Paradigms

Part 19 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act IV, *Algorithms*. Most good algorithms come from a handful of
ideas: be greedy when an exchange argument allows it, divide and conquer, remember subproblems, or search with
pruning. This part names the ideas, proves when each works, measures them, and applies divide and conquer to the
right points, the roots of unity, to derive the fast Fourier transform. The instrument is
`explainer/cs/algo/paradigms.py`. It covers interval scheduling by four rules, Huffman codes, coin change, and the
matroid greedy against matchings. It also implements grade-school and Karatsuba multiplication on digit lists,
Strassen's recursion, the DFT, the recursive FFT, the number-theoretic transform, a numpy FFT multiplier and
Chudnovsky's series for π. Finally there are the closest pair, Fibonacci call counts, edit distance and LCS,
knapsack, matrix chains, optimal search trees with Knuth's speedup, independent sets on trees, n-queens, Dancing
Links for Sudoku, and maximum subarray four ways. Every one counts its work, tested in
`tests/test_cs19_paradigms.py`. Every number is computed in `compute.py`; timings are taken on this machine.

* **A million digits.** π to a million places by the Chudnovskys' series in 16 s of plain Python; two million-digit
  numbers multiplied four ways: grade school (about 27 hours, projected), Python's Karatsuba integers (0.83 s),
  `decimal`'s number-theoretic transform (0.20 s), the FFT itself (43 ms); the four paradigms.
* **1. Greedy, and the exchange argument.** Interval scheduling by earliest finish, proved by exchange; four rules
  on 2,000 random instances (finishing first always optimal, starting first 1,470 times) with counterexamples; coins
  {1, 3, 4} (greedy wrong for 24 amounts below 100; Kozen and Zaks's bound); Huffman's code on the thirty novels'
  27 symbols, 4.12 bits each against an entropy of 4.08 and 5 for a fixed code.
* **2. When greedy is right: matroids.** Whitney's axioms; vectors, forests and small sets; the Rado–Edmonds
  theorem, proved; forests optimal on 400 of 400 random graphs, matchings on 248 (worst 60%; never below half).
* **3. Three products instead of four.** Kolmogorov's seminar and Karatsuba (1960); 1234 × 5678 by three products;
  the recursion tree and n^{lg 3}; measured: pure Karatsuba loses to school at every size up to 4,096 digits, with a
  32-digit cutoff it wins from 64 digits and is 3.8× faster at 4,096; CPython's cutoff; Toom–Cook.
* **4. Seven products instead of eight.** Strassen's seven products; operation counts (at n = 1024, 3.8× fewer
  products, 1.6× more additions); the history of ω from 2.807 to 2.3713 (2024); galactic algorithms; against
  numpy's BLAS (3–5× slower) and its rounding (10× larger error); AlphaTensor.
* **5. The FFT, I: values instead of coefficients.** Coefficients against values; evaluation in ± pairs; the roots
  of unity squaring onto half as many points; T(n) = 2T(n/2) + O(n); the algorithm in ten lines.
* **6. The FFT, II: butterflies.** Gauss (c. 1805) and Cooley and Tukey (1965); the butterfly network and bit
  reversal; the inverse by orthogonality, proved; DFT against FFT in the same Python (272× at 2,048 points); numpy
  on four million points in 0.41 s.
* **7. What the FFT multiplies.** Integers as polynomials and carries; floating-point exactness measured (the worst
  rounding residual 0.05 at ten million digits); the number-theoretic transform; Schönhage–Strassen to Harvey and
  van der Hoeven's n log n (2019).
* **8. The closest pair.** Shamos and Hoey's divide and conquer; the strip and the seven-neighbour bound, proved;
  100,000 points in 1.3 s with 142,461 distances (all pairs: five billion, about a quarter of an hour).
* **9. Dynamic programming.** Bellman and the name; Fibonacci (2,692,537 calls for F(30) against 59); memoization
  and tabulation; every dynamic programme as a path in a DAG of subproblems.
* **10. Edit distance.** The recurrence; the table for *intention* → *execution* (distance 5) and its traceback;
  quadratic time measured; LCS, `diff` and biology.
* **11. Knapsack, and pseudo-polynomial time.** The O(nW) table (best 110); greedy by value per weight (wrong 196
  times in 500, worst 78%); the same problem with ever larger numbers, 21 million cells at W = 10⁶; NP-hardness
  and Ibarra and Kim's approximation scheme.
* **12. Matrix chains and optimal search trees.** The textbook chain (15,125 against 40,500 left to right and
  58,000 worst of 42 orders); optimal BSTs and Knuth's monotonicity (33× fewer steps at 200 keys).
* **13. Dynamic programming on trees, graphs and sequences.** Independent sets on a tree (200,000 vertices in
  0.30 s); Bellman–Ford, Floyd–Warshall, Held–Karp and DAG paths as DPs; Viterbi, CYK, DP speedups, Hirschberg.
* **14. Backtracking and Dancing Links.** Eight queens (2,057 nodes against 16.8 million placements; fourteen
  queens, 27 million nodes in 16 s); exact cover and dancing links; three Sudokus, Inkala's 2012 puzzle in 2,741
  nodes against 49,559 for plain backtracking; branch and bound.
* **15. One problem, four paradigms.** Maximum subarray (Grenander, Bentley) by brute force, running sums, divide and
  conquer and Kadane's DP, timed from 100 to a million numbers.
* **16. Frontier: how fast can we multiply?** The limits of the laser method (Ambainis, Filmus and Le Gall, 2015;
  Alman and Vassilevska Williams, 2018); edit distance and SETH (Backurs and Indyk, 2015) and approximation (Andoni
  and Nosatzki, 2020); lower bounds for the FFT and multiplication; open problems. Outro.

## Build

```bash
python -m videos.cs.cs19.compute           # every number in the part (about twelve minutes)
python tools/build.py cs19 -q l            # a 480p preview
python tools/build.py cs19                 # 1080p
```

## Problems, with solutions

1. **Huffman's code.** Prove that some optimal prefix code has the two rarest symbols as sibling leaves at the
   greatest depth, and deduce that Huffman's algorithm is optimal.

   *Solution.* Take an optimal code tree T; it is full (every internal node has two children), since otherwise a
   node with one child could be removed, shortening every code below it. Let a and b be sibling leaves at the
   greatest depth, and x and y the two rarest symbols. Swapping the leaves x and a changes the cost
   Σ f(s) d(s) by (f(x) − f(a))(d(a) − d(x)) ≤ 0, since f(x) ≤ f(a) and d(x) ≤ d(a). The same holds for swapping y
   and b. The result is still optimal, with x and y deepest siblings. For optimality, induct on the number of
   symbols. Replace x and y by one symbol z with f(z) = f(x) + f(y). Any tree T′ for the reduced alphabet gives a
   tree for the original one by hanging x and y below z, and its cost is cost(T′) + f(x) + f(y). By the lemma, some
   optimal tree has this form. So the original problem's optimum is the reduced problem's optimum plus
   f(x) + f(y). That is what Huffman computes: it merges x and y first and then, by induction, solves the reduced
   problem optimally.

2. **Karatsuba.** Solve T(n) = 3T(n/2) + cn, T(1) = 1, exactly for n = 2^k, and show that Karatsuba does exactly
   3^k digit products.

   *Solution.* Unrolling, T(2^k) = 3^k T(1) + c Σ_{i=0}^{k−1} 3^i 2^{k−i} = 3^k + c 2^k Σ_{i<k} (3/2)^i
   = 3^k + c 2^k · 2((3/2)^k − 1) = (1 + 2c) 3^k − 2c 2^k. With 3^k = 3^{lg n} = n^{lg 3}, T(n) = (1 + 2c) n^{lg 3} −
   2cn = Θ(n^{1.585}). Digit products happen only at the leaves. P(1) = 1, and each call makes three half-size
   calls and multiplies nothing itself, so P(2^k) = 3P(2^{k−1}) = 3^k. The sums x₁ + x₀ have the same number of
   digits as the halves when digits are kept uncarried, as in `paradigms.karatsuba`. With carrying they can gain
   one digit, which changes lower-order terms only. The test `test_karatsuba_count` checks 3^k for k ≤ 7.

3. **Orthogonality.** Prove Σ_{k=0}^{n−1} ω^{jk} = 0 for n ∤ j, where ω = e^{2πi/n}, and deduce F^{−1} = (1/n) F̄
   for the DFT matrix F_{kj} = ω^{jk}.

   *Solution.* If n ∤ j then ω^j ≠ 1, and the geometric sum is (ω^{jn} − 1)/(ω^j − 1) = (1 − 1)/(ω^j − 1) = 0. If
   n | j, every term is 1 and the sum is n. Now (F F̄)_{jl} = Σ_k ω^{jk} ω^{−lk} = Σ_k ω^{(j−l)k}, which is n when
   j = l and 0 otherwise (0 ≤ j, l < n, so n | j − l only when j = l). Hence F F̄ = nI and F^{−1} = F̄/n. Since F̄ is
   the DFT with ω replaced by ω^{−1} = ω̄, which is again a primitive n-th root of unity, the same FFT computes the
   inverse in O(n log n).

4. **Edit distance.** Prove the edit-distance recurrence correct, and recover an optimal edit script from the table
   in O(n + m) extra time.

   *Solution.* Let D*(i, j) be the true distance between the prefixes a[1..i] and b[1..j]. In an optimal alignment of
   them, the last column is one of three things: a_i against a gap (a deletion), a gap against b_j (an insertion), or
   a_i against b_j (a substitution, free if they are equal). Removing that column leaves an alignment of the
   corresponding shorter prefixes, which must itself be optimal, or the whole could be improved. So D*(i, j) is the
   minimum of the three cases, which is the recurrence; with D(i, 0) = i and D(0, j) = j, induction on i + j gives
   D = D*. To recover a script, start at (n, m) and repeatedly move to a predecessor cell whose value plus the
   step's cost equals the current value; one always exists, because the current value was computed as such a
   minimum. Each move decreases i + j by one or two, so there are at most n + m moves, each O(1), and reading the
   moves backwards gives the edits.

5. **Build: the NTT on Pebble.** Implement the number-theoretic transform modulo p = 998244353 in the Pebble
   language, multiply two 1,000-digit numbers on the emulator, and compare its instruction count with Karatsuba.

   *Solution sketch.* Use decimal digits as coefficients. A product coefficient is at most 1,000 · 81 = 81,000 < p,
   so the result modulo p is exact; with base 10⁴ the coefficients would reach 10¹¹ and wrap. Pad to n = 2,048
   points. Compute the bit-reversal permutation once. Then for each of the 11 stages, multiply by the twiddles:
   precompute w = 3^{(p−1)/len} and step it by one modular multiplication. Each product of two residues is below
   2⁶⁰, so it fits Pebble's 64-bit registers, and one `%` reduces it. Transform both inputs, multiply pointwise,
   transform back with w⁻¹ = w^{p−2}, multiply by n⁻¹, and carry. There are three transforms of 1,024 · 11 =
   11,264 butterflies, at about 20 instructions each, so expect on the order of 700,000 instructions. Karatsuba
   with a cutoff of 32 does about 3^5 · 32² ≈ 250,000 digit products plus its additions, so the two land within
   a small factor at a thousand digits. Run both at 10,000 and 100,000 digits too: the NTT's n log n pulls ahead,
   as `decimal` did in chapter 7. Check the product against Python's integers.

6. **★ Research: a lower bound for the DFT.** Prove that every linear circuit computing the n-point DFT needs
   Ω(n log n) additions, without assuming bounded coefficients.

   *Where to start.* The bounded-coefficient result: Morgenstern, "Note on a lower bound of the linear complexity
   of the fast Fourier transform" (1973), via determinants. Its extensions: Chazelle (1994); Raz and Shpilka's
   bounded-coefficient bounds for matrix products (2003); Ailon (2013), for circuits of 2 × 2 unitary gates. The
   general route goes through rigidity: Valiant (1977) showed that a sufficiently rigid matrix has no linear
   circuit of linear size and logarithmic depth. The Fourier matrix's rigidity is known only weakly. Alman and
   Williams (2017) showed that Walsh–Hadamard matrices are not rigid enough for Valiant's purpose. Upper bounds keep
   moving: split radix (Yavne, 1968) stood until Johnson and Frigo's (2007) lower flop count of about
   (34/9) n lg n. Open: (a) any superlinear lower bound for the DFT in general linear circuits; (b) whether
   Johnson–Frigo is optimal among FFTs of a fixed shape; (c) here, measure: search exhaustively for the fewest
   real additions computing the DFT for n = 4, 8, 16 over small coefficient sets, and compare with split radix.

## 习题与解答

1. **哈夫曼编码。** 证明存在一个最优前缀码，使两个最稀有的符号是最大深度处的兄弟叶子，并由此推出哈夫曼算法是最优的。

   *解答。* 取一棵最优编码树 T；它是满的（每个内部结点都有两个孩子），否则只有一个孩子的结点可以去掉，使其下所有编码变短。
   设 a、b 是最大深度处的兄弟叶子，x、y 是两个最稀有的符号。交换叶子 x 和 a，代价 Σ f(s) d(s) 改变
   (f(x) − f(a))(d(a) − d(x)) ≤ 0，因为 f(x) ≤ f(a) 且 d(x) ≤ d(a)。交换 y 和 b 同理。结果仍是最优的，且 x、y 是最深的兄弟。
   关于最优性，对符号数归纳。把 x 和 y 换成一个符号 z，f(z) = f(x) + f(y)。缩小后字母表的任意一棵树 T′，把 x 和 y 挂在 z
   下面，就得到原字母表的一棵树，代价为 cost(T′) + f(x) + f(y)。由引理，某棵最优树具有这种形式。所以原问题的最优值等于
   缩小问题的最优值加 f(x) + f(y)。哈夫曼算法算的正是这个：它先合并 x 和 y，再由归纳假设最优地解决缩小后的问题。

2. **Karatsuba。** 对 n = 2^k 精确求解 T(n) = 3T(n/2) + cn，T(1) = 1，并证明 Karatsuba 恰好做 3^k 次数字乘法。

   *解答。* 展开得 T(2^k) = 3^k T(1) + c Σ_{i=0}^{k−1} 3^i 2^{k−i} = 3^k + c 2^k Σ_{i<k} (3/2)^i
   = 3^k + c 2^k · 2((3/2)^k − 1) = (1 + 2c) 3^k − 2c 2^k。由于 3^k = 3^{lg n} = n^{lg 3}，T(n) = (1 + 2c) n^{lg 3} − 2cn =
   Θ(n^{1.585})。数字乘法只发生在叶子上。P(1) = 1，每次调用做三次半规模调用、自己不做乘法，所以 P(2^k) = 3P(2^{k−1}) = 3^k。
   如 `paradigms.karatsuba` 那样不进位地保存数字时，和 x₁ + x₀ 与两半的位数相同。进位时它们可能多一位，那只影响低阶项。测试
   `test_karatsuba_count` 对 k ≤ 7 检验了 3^k。

3. **正交性。** 设 ω = e^{2πi/n}，证明当 n ∤ j 时 Σ_{k=0}^{n−1} ω^{jk} = 0，并推出 DFT 矩阵 F_{kj} = ω^{jk} 满足
   F^{−1} = (1/n) F̄。

   *解答。* 若 n ∤ j，则 ω^j ≠ 1，几何级数之和为 (ω^{jn} − 1)/(ω^j − 1) = (1 − 1)/(ω^j − 1) = 0。若 n | j，每一项都是 1，和为 n。
   于是 (F F̄)_{jl} = Σ_k ω^{jk} ω^{−lk} = Σ_k ω^{(j−l)k}，当 j = l 时为 n，否则为 0（0 ≤ j, l < n，所以只有 j = l 时 n | j − l）。
   因此 F F̄ = nI，F^{−1} = F̄/n。F̄ 是把 ω 换成 ω^{−1} = ω̄ 的 DFT，而 ω̄ 也是本原 n 次单位根，所以同一个 FFT 能在
   O(n log n) 内算出逆变换。

4. **编辑距离。** 证明编辑距离递推式正确，并在 O(n + m) 额外时间内从表中恢复一个最优编辑脚本。

   *解答。* 设 D*(i, j) 是前缀 a[1..i] 与 b[1..j] 之间的真实距离。在它们的一个最优对齐中，最后一列只有三种情况：a_i 对空位
   （删除）、空位对 b_j（插入），或 a_i 对 b_j（替换，相等时免费）。去掉这一列，剩下的是相应较短前缀的一个对齐，它本身必须最优，
   否则整体还能改进。所以 D*(i, j) 是三种情况的最小值，这就是递推式；加上 D(i, 0) = i、D(0, j) = j，对 i + j 归纳即得 D = D*。
   要恢复脚本，从 (n, m) 出发，反复移到一个前驱格子，使其值加上这一步的代价等于当前值；这样的前驱总存在，因为当前值正是作为这样的
   最小值算出来的。每一步让 i + j 减少一或二，所以至多 n + m 步，每步 O(1)，倒过来读就是编辑操作。

5. **动手：在 Pebble 上实现 NTT。** 用 Pebble 语言实现模 p = 998244353 的数论变换，在模拟器上做两个 1,000 位数的乘法，并与
   Karatsuba 比较指令数。

   *解答提要。* 用十进制数字作系数。乘积的系数至多 1,000 · 81 = 81,000 < p，所以模 p 的结果是精确的；若用 10⁴ 进制，系数会达到
   10¹¹ 而发生回绕。补齐到 n = 2,048 个点。先算一次位反转置换。然后在 11 级中的每一级乘以旋转因子：预先算出 w = 3^{(p−1)/len}，
   每步做一次模乘向前推进。两个剩余的乘积小于 2⁶⁰，能放进 Pebble 的 64 位寄存器，一次 `%` 就能约简。对两个输入做变换，逐点相乘，
   用 w⁻¹ = w^{p−2} 变换回来，乘以 n⁻¹，再进位。三次变换各有 1,024 · 11 = 11,264 个蝶形，每个约 20 条指令，所以预计约 70 万条指令。
   截断为 32 的 Karatsuba 约做 3^5 · 32² ≈ 25 万次数字乘法再加上它的加法，所以在一千位时两者相差一个小倍数。再在一万位和十万位上
   运行两者：NTT 的 n log n 会领先，就像第 7 章的 `decimal` 那样。用 Python 的整数检验乘积。

6. **★ 研究题：DFT 的下界。** 不假设系数有界，证明每个计算 n 点 DFT 的线性电路都需要 Ω(n log n) 次加法。

   *从哪里开始。* 系数有界的结果：Morgenstern，"Note on a lower bound of the linear complexity of the fast Fourier transform"
   （1973），用的是行列式。推广：Chazelle（1994）；Raz 与 Shpilka 关于矩阵乘积的有界系数下界（2003）；Ailon（2013），针对由
   2 × 2 酉门组成的电路。一般情形要经过刚性：Valiant（1977）证明了足够刚性的矩阵没有线性规模、对数深度的线性电路。傅里叶矩阵的
   刚性目前只知道很弱的结果。Alman 与 Williams（2017）证明 Walsh–Hadamard 矩阵的刚性不足以满足 Valiant 的需要。上界一直在动：
   分裂基（Yavne，1968）保持了很久，直到 Johnson 与 Frigo（2007）把浮点运算数降到约 (34/9) n lg n。未解决：（a）一般线性电路中
   DFT 的任何超线性下界；（b）在固定形状的 FFT 中 Johnson–Frigo 是否最优；（c）在这里动手测量：对 n = 4、8、16，在小的系数集合上
   穷举搜索计算 DFT 所需的最少实数加法，与分裂基比较。

## Glossary additions

贪心算法 greedy algorithm · 交换论证 exchange argument · 区间调度 interval scheduling · 哈夫曼编码 Huffman code · 前缀码
prefix code · 拟阵 matroid · 独立集 independent set · 交换公理 exchange axiom · 图拟阵 graphic matroid · 分治 divide and
conquer · Karatsuba 乘法 Karatsuba multiplication · Toom–Cook 乘法 Toom–Cook multiplication · 截断阈值 cutoff · 施特拉森算法
Strassen's algorithm · 矩阵乘法指数 matrix multiplication exponent · 激光法 laser method · 银河算法 galactic algorithm · 快速
傅里叶变换 fast Fourier transform · 离散傅里叶变换 discrete Fourier transform · 单位根 root of unity · 旋转因子 twiddle factor ·
蝶形 butterfly · 位反转 bit reversal · 正交性 orthogonality · 卷积 convolution · 数论变换 number-theoretic transform · 最近点对
closest pair · 动态规划 dynamic programming · 记忆化 memoization · 制表法 tabulation · 编辑距离 edit distance · 最长公共子序列
longest common subsequence · 背包问题 knapsack problem · 伪多项式时间 pseudo-polynomial time · 矩阵链乘 matrix chain
multiplication · 最优二叉搜索树 optimal binary search tree · 四边形不等式 quadrangle inequality · 树形动态规划 dynamic
programming on trees · 回溯 backtracking · 精确覆盖 exact cover · 舞蹈链 dancing links · 分支定界 branch and bound · 最大子数组
maximum subarray · 强指数时间假设 strong exponential time hypothesis · 细粒度复杂性 fine-grained complexity · 刚性 rigidity

## Sources

*Canon.* Books: Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, chapters 4, 14–15, 30; Kleinberg &
Tardos, *Algorithm Design*, chapters 4–6; Dasgupta, Papadimitriou & Vazirani, *Algorithms*, chapters 2, 5–6; Knuth,
*The Art of Computer Programming*, volume 2 §4.3.3 and volume 4B (Dancing Links); Bentley, *Programming Pearls*
(1986), column 8; Bellman, *Dynamic Programming* (1957) and *Eye of the Hurricane* (1984); Oxley, *Matroid Theory*.

Papers: Whitney, "On the abstract properties of linear dependence" (1935); Huffman, "A method for the construction
of minimum-redundancy codes" (1952); Rado (1957); Karatsuba & Ofman (1962); Toom (1963); Cook (1966); Cooley &
Tukey, "An algorithm for the machine calculation of complex Fourier series" (1965); Levenshtein (1965); Strassen,
"Gaussian elimination is not optimal" (1969); Needleman & Wunsch (1970); Edmonds, "Matroids and the greedy
algorithm" (1971); Knuth, "Optimum binary search trees" (1971); Schönhage & Strassen (1971); Wagner & Fischer, "The
string-to-string correction problem" (1974); Hirschberg (1975); Shamos & Hoey, "Closest-point problems" (1975);
Ibarra & Kim (1975); Hunt & McIlroy (1976); Rabin (1976); Hitotumatu & Noshita (1979); Heideman, Johnson & Burrus,
"Gauss and the history of the fast Fourier transform" (1984); Coppersmith & Winograd, "Matrix multiplication via
arithmetic progressions" (1990); Kozen & Zaks, "Optimal bounds for the change-making problem" (1994); Knuth,
"Dancing links" (2000); Fürer (2007); Harvey & van der Hoeven, "Integer multiplication in time O(n log n)" (2021);
Fawzi et al., "Discovering faster matrix multiplication algorithms with reinforcement learning" (2022).

*Frontier.* Morgenstern (1973); Valiant, "Graph-theoretic arguments in low-level complexity" (1977); Impagliazzo &
Paturi (2001); Cohn & Umans (2003); Johnson & Frigo, "A modified split-radix FFT with fewer arithmetic operations"
(2007); Ambainis, Filmus & Le Gall, "Fast matrix multiplication: limitations of the Coppersmith–Winograd method"
(2015); Backurs & Indyk, "Edit distance cannot be computed in strongly subquadratic time (unless SETH is false)"
(2015); Abboud, Backurs & Vassilevska Williams (2015); Bringmann & Künnemann (2015); Alman & Vassilevska Williams,
"Limits on all known (and some unknown) approaches to matrix multiplication" (2018); Afshani, Freksen, Kamma &
Larsen, "Lower bounds for multiplication via network coding" (2019); Andoni & Nosatzki, "Edit distance in near-linear
time: it's a constant factor" (2020); Duan, Wu & Zhou (2023); Alman, Duan, Vassilevska Williams, Xu, Xu & Zhou, "More
asymmetry yields faster matrix multiplication" (2024).
