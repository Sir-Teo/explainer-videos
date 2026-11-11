# Computer Science, Built — Part 19: The Great Paradigms

Part 19 of the [sixty-one-part course](../README.md), Act IV, *Algorithms*. Greedy exchange,
divide and conquer, dynamic programming and pruned search are compared through executable instruments in
`explainer/cs/algo/paradigms.py`. The visual examples include interval schedules, a matroid exchange witness,
Strassen's block identities, roots of unity and a butterfly network, a closest-pair packing argument,
filled edit and knapsack tables, tree states, a binary exact-cover matrix, reversible links and a Kadane trace.

The episode distinguishes four kinds of evidence: a proved work bound, an observed counter or runtime,
a model projection, and a research claim under stated hypotheses. The notes provide five worked exercises
and one open research extension.

## Chapters

* **Hook:** certified floor of π · 10^1,000,000. Adjacent Chudnovsky partial sums and integer square-root
  bounds give the same integer floor. The result has 1,000,001 digits including the initial 3.
  Complete Python, Decimal and floating FFT products use the same operands per row. The school estimate is
  extrapolated, and the separate FFT-core experiment excludes conversion and carry.
* **Greedy and matroids:** unweighted interval selection; finite coin-system experiments; Huffman coding;
  the nonnegative-weight greedy characterization of finite hereditary systems. Arbitrary signed weights
  require omitting negative elements when any independent set is allowed. Descending forest greedy maximizes
  weight; ascending Kruskal minimizes it. Nonnegative greedy matching is a one-half approximation.
* **Divide and conquer:** Karatsuba's coefficient model and measured cutoffs; Strassen's seven products;
  FFT evaluation, inverse orthogonality and padding; closest-pair merging and at most seven strip successors.
  Strassen's additions summed across the tree have the same exponent as its leaf products. Extended-precision
  reference disagreement is approximate, not a certified true error. The matrix-exponent plot selects dated
  2024 and August 2026 upper bounds; it is not a latest-record survey or a crossover measurement.
* **Convolution certification:** the ten-million-digit-equivalent FFT-core case checks all 4,999,999
  coefficients and all padded zeros against two independent native integer NTTs. Each candidate and true
  coefficient lies in [0, B], where B = min(|A|, |B|) max(A) max(B) is smaller than the two-prime product.
  Equal residues therefore imply equal integer coefficients. A small distance to the nearest integer alone
  does not establish correctness. Reference construction, compilation and validation are outside the timer.
* **Dynamic programming:** Fibonacci calls versus arithmetic and bit length; dependency graphs with either
  choice or combination; edit-distance boundaries, interior updates and traceback; knapsack numeric capacity
  versus encoding length; matrix-chain bracketings and conditional Knuth optimization. The six-matrix example
  has 42 orders, optimum 15,125, left-to-right 40,500 and worst 58,000 scalar products. Tree timing covers the
  complete iterative public solver on 200,000 vertices, with input generation excluded.
* **Search and maximum subarray:** queens partial nodes versus complete assignments; Algorithm X and restored
  Dancing Links, including early returns; Sudoku constraints and uniqueness. Naive Sudoku stops at its first
  solution while DLX exhausts search or stops at two, so their node counts measure different work.
  All maximum-subarray methods require a nonempty result; all-negative input returns its largest element.
* **Frontier:** method-specific matrix multiplication barriers, exact worst-case edit distance conditional on
  SETH, and bounded-coefficient versus unrestricted complex linear circuits for the DFT. Arithmetic operations
  and integer bit complexity use different models.

## Build and measurement protocol

```bash
python -m videos.cs.cs19.compute           # rebuild all numerical payloads
python tools/build.py cs19 -q l            # 480p preview
python tools/build.py cs19                 # 1080p production build
```

Schema-2 caches record raw timed trials, repeat counts, minima, Python/NumPy versions, NumPy build metadata,
and the queried BLAS thread configuration. Every timed output is validated after its timer stops.
Measurements describe one shared host. They do not isolate hardware causes or establish universal winners.
Random seeds, operand hashes where used, full references and work-count definitions are in `compute.py`
and `measurements.py`. Floating FFT integer multiplication is an experimental candidate checked against
an exact product for the measured instances; a supported chunk width is not a universal rounding guarantee.
The on-screen ten-line FFT is the radix-two core for a nonempty power-of-two input. The public Python
instrument additionally returns an empty result for empty input and rejects unsupported lengths.

## Five worked exercises and an open research extension

1. **Huffman's code.** Prove that some optimal prefix code has the two rarest symbols as sibling leaves at the
   greatest depth, and deduce that Huffman's algorithm is optimal.

   *Solution.* Assume at least two symbols with positive frequencies; empty and singleton alphabets are separate
   implementation conventions. Take an optimal code tree T; it is full (every internal node has two children), since otherwise a
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
   3^k leaves in the full cutoff-one, uncarried, equal-power-of-two recursion tree. Explain why an implementation that skips zero products can execute fewer multiplications.

   *Solution.* Unrolling, T(2^k) = 3^k T(1) + c Σ_{i=0}^{k−1} 3^i 2^{k−i} = 3^k + c 2^k Σ_{i<k} (3/2)^i
   = 3^k + c 2^k · 2((3/2)^k − 1) = (1 + 2c) 3^k − 2c 2^k. With 3^k = 3^{lg n} = n^{lg 3}, T(n) = (1 + 2c) n^{lg 3} −
   2cn = Θ(n^{1.585}). Digit products happen only at the leaves. P(1) = 1, and each call makes three half-size
   calls and multiplies nothing itself, so the full-tree leaf count is P(2^k) = 3P(2^{k−1}) = 3^k.
   The implemented school leaf skips a zero left coefficient; the executed counter can therefore be smaller. The sums x₁ + x₀ have the same number of
   digits as the halves when digits are kept uncarried, as in `paradigms.karatsuba`. With carrying they can gain
   one digit, so the exact leaf count need not survive that implementation change. The test `test_karatsuba_count` checks 3^k for k ≤ 7.

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

5. **Build: the NTT on Pebble.** Implement the number-theoretic transform modulo p = 40961 = 5 · 2¹³ + 1 in the
   Pebble language, multiply two 500-digit numbers on the emulator, and compare its instruction count with
   Karatsuba.

   *Solution sketch.* Use decimal-digit coefficients. Their convolution is at most 500 · 81 = 40,500 < p,
   so one residue identifies each integer coefficient. Here p is prime, 3 is a primitive root, and
   p² = 1,677,803,521 < 2³¹, so a product of residues fits the machine's positive signed range.
   Pad to 1,024 points; 1,024 divides p − 1. Use bit reversal and ten radix-two stages with
   stage root 3^((p−1)/length) mod p. Transform both inputs, multiply pointwise, inverse-transform
   using inverse roots, multiply by 1,024⁻¹ mod p, then carry in base ten. Normalize negative
   butterfly differences before using a language remainder operation. Three transforms use 15,360
   butterflies; this is not an instruction count. Run the emulator to count instructions and compare
   with a stated Karatsuba cutoff on the same operands. Check both results against exact Python integers.
   Longer inputs require checking both transform divisibility and coefficient range again; additional
   primes and Chinese remaindering can increase the coefficient range, but do not guarantee a crossover.

6. **★ Research (open): a DFT circuit lower bound.** Over the complex numbers, consider exact linear
   arithmetic circuits whose gates form scalar multiples and sums of earlier values; count arithmetic
   operations, including scalar multiplications. Must every such circuit for the n-point DFT have
   Ω(n log n) operations when scalar coefficients are unrestricted?

   *Starting point, not a solution.* Morgenstern's 1973 determinant argument establishes this scale
   in a bounded-coefficient model. Its coefficient restriction is part of the theorem. Compare the
   determinant growth allowed by one bounded gate with the DFT determinant magnitude. Then identify
   exactly where allowing arbitrarily large coefficients breaks that argument. Exhaustive searches
   over a finite coefficient set at n = 4 or 8 explore only that restricted set; they cannot settle
   the unrestricted question. Fixed-shape FFT operation counts are another, narrower optimization problem.

## 习题与解答

1. **哈夫曼编码。** 证明存在一个最优前缀码，使两个最稀有的符号是最大深度处的兄弟叶子，并由此推出哈夫曼算法是最优的。

   *解答。* 假设至少有两个正频率符号；空字母表和单符号情况另按实现约定处理。取一棵最优编码树 T；它是满的（每个内部结点都有两个孩子），否则只有一个孩子的结点可以去掉，使其下所有编码变短。
   设 a、b 是最大深度处的兄弟叶子，x、y 是两个最稀有的符号。交换叶子 x 和 a，代价 Σ f(s) d(s) 改变
   (f(x) − f(a))(d(a) − d(x)) ≤ 0，因为 f(x) ≤ f(a) 且 d(x) ≤ d(a)。交换 y 和 b 同理。结果仍是最优的，且 x、y 是最深的兄弟。
   关于最优性，对符号数归纳。把 x 和 y 换成一个符号 z，f(z) = f(x) + f(y)。缩小后字母表的任意一棵树 T′，把 x 和 y 挂在 z
   下面，就得到原字母表的一棵树，代价为 cost(T′) + f(x) + f(y)。由引理，某棵最优树具有这种形式。所以原问题的最优值等于
   缩小问题的最优值加 f(x) + f(y)。哈夫曼算法算的正是这个：它先合并 x 和 y，再由归纳假设最优地解决缩小后的问题。

2. **Karatsuba。** 对 n = 2^k 精确求解 T(n) = 3T(n/2) + cn，T(1) = 1，并在等长、二次幂长度、不进位且截断为 1 的模型下，证明完整递归树有 3^k 个叶子；解释跳过零乘法时实际计数为何可能更小。

   *解答。* 展开得 T(2^k) = 3^k T(1) + c Σ_{i=0}^{k−1} 3^i 2^{k−i} = 3^k + c 2^k Σ_{i<k} (3/2)^i
   = 3^k + c 2^k · 2((3/2)^k − 1) = (1 + 2c) 3^k − 2c 2^k。由于 3^k = 3^{lg n} = n^{lg 3}，T(n) = (1 + 2c) n^{lg 3} − 2cn =
   Θ(n^{1.585})。数字乘法只发生在叶子上。P(1) = 1，每次调用做三次半规模调用、自己不做乘法，所以 完整树的叶子数为 P(2^k) = 3P(2^{k−1}) = 3^k。实现会跳过左系数为零的叶子乘法，因此实际乘法次数可能更小。
   如 `paradigms.karatsuba` 那样不进位地保存数字时，和 x₁ + x₀ 与两半的位数相同。进位时可能多一位，此时不能照搬精确的叶子数公式。测试
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

5. **动手：在 Pebble 上实现 NTT。** 用 Pebble 语言实现模 p = 40961 = 5 · 2¹³ + 1 的数论变换，在模拟器上做两个 500 位数的乘法，
   并与 Karatsuba 比较指令数。

   *解答提要。* 采用十进制数字系数，每个卷积系数至多 500 · 81 = 40,500 < p，故一个模数足以唯一恢复整数系数。
   p 是素数，3 是其原根；p² = 1,677,803,521 < 2³¹，余数乘积可装入正的有符号范围。
   补零到 1,024 点，因 1,024 整除 p−1。位反转后做十级蝶形，每级使用根 3^((p−1)/length) mod p。
   变换两个输入，逐点相乘，以逆根作逆变换，再乘 1,024 的模逆，最后十进制进位。
   蝶形差为负时先归一化，再使用语言的取余操作。三次变换共 15,360 个蝶形；蝶形数不等于指令数。
   在同一操作数上运行模拟器，比较指定截断的 Karatsuba，且先用 Python 精确整数核验。
   扩大输入时需重新检查变换长度整除条件与系数范围；多素数及中国剩余定理能扩大范围，但不保证实用交叉点。

6. **★ 开放研究题：DFT 电路下界。** 在复数域上，考虑精确线性算术电路，每个门由此前值做标量乘法或加法，
   标量乘法也计入算术操作。系数不受限时，n 点 DFT 是否仍需 Ω(n log n) 次操作？

   *起点，并非解答。* Morgenstern（1973年）的行列式论证针对有界系数模型；系数限制是定理条件。
   比较单个有界门能带来的行列式增长与 DFT 行列式的大小，再指出任意大系数为何破坏该论证。
   对 n=4 或 8、有限系数集的穷举只探索受限模型，不能解决一般问题。固定 FFT 形状下的运算数优化也更狭窄。

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


Selected primary links (dates and models are part of each claim):

* [Alman et al., April 2024 v1](https://arxiv.org/abs/2404.16349v1): ω < 2.371339; later versions have changed.
* [Dupont et al., August 2026](https://arxiv.org/abs/2608.16884): selected optimization refinement, ω < 2.371177.
* [Ambainis, Filmus and Le Gall](https://arxiv.org/abs/1411.5414): restrictions on specified laser frameworks.
* [Backurs and Indyk](https://arxiv.org/abs/1412.0348): exact worst-case edit distance and SETH.
* [Harvey and van der Hoeven, Annals 2021](https://annals.math.princeton.edu/2021/193-2/p04): O(n log n) bit operations; first announced in 2019.
* [Fawzi et al., Nature 2022](https://www.nature.com/articles/s41586-022-05172-4): the 47-product four-by-four example is over the field with two elements.
* [Morgenstern, JACM 1973](https://doi.org/10.1145/321752.321761): bounded-coefficient linear complexity.
