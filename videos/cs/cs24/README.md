# Computer Science, Built — Part 24: Algorithms in Practice

Part 24 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the ninth and last part of Act IV, *Algorithms*. Big-O hides constants, and in
production the constants and the machine decide.

The part has two halves. The first covers the everyday tools of real code and of interviews:
- prefix sums; Fenwick and segment trees; range minimum and lowest common ancestors;
- two pointers, monotonic stacks and searching for the answer;
- bit tricks and the Four Russians.

The second is algorithm engineering. Search layouts, vector instructions, hash tables and sorting are measured on
this machine, along with how to benchmark honestly. The Job, engineered natively, gives the ledger its tenth row.

The instrument is `explainer/cs/algo/practice.py`. It holds:
* prefix sums, difference arrays and integral images;
* a Fenwick tree that counts the cells it touches;
* a segment tree over any monoid, with its covering nodes, and a lazy segment tree;
* a sparse table; LCA by Euler tour and by binary lifting; Cartesian trees;
* the sliding-window deque, next greater element and the largest rectangle;
* binary search on the answer, galloping and ternary search;
* popcount, Gray codes and submask enumeration;
* bitset transitive closure and bit-parallel LCS;
* meet-in-the-middle subset sum, square-root blocks and Mo's order.

It is tested in `tests/test_cs24_practice.py`, every structure against brute force. Everything that depends on the
machine is a C or C++ program in `compute.py`. Each is compiled with `gcc -O2` (and `-march=native` where it uses
SIMD), its result checked against a reference, and timed as the best of several runs. The machine is an Intel Xeon
at 2.1 GHz: 48 KB of L1 data cache, 2 MB of L2 per core and 260 MB of shared L3, in a shared cloud container. The
timings are noisy, and chapter 12 measures how noisy.

* **Same big-O, different worlds.** Hook.
  - Summing n numbers from an array and from a shuffled linked list, both O(n).
  - The ratio grows with n: 5× at 1,024 elements, 22× at 65,536, and 143× at 16 million (1.5 against 208 ns an
    element).
* **1. Prefix sums.**
  - A range sum with one subtraction: S₁₁ − S₃ = 44 − 8 = 36.
  - Difference arrays: three range updates at two cells each.
  - The integral image: a box in four lookups, checked against brute force (Crow 1984; Viola–Jones 2001).
  - The parallel scan: log₂ n rounds (Hillis–Steele; Blelloch).
* **2. Fenwick trees.**
  - Responsibility ranges by the lowest set bit. prefix(13) visits cells 13, 12 and 8; add(5) visits 5, 6, 8 and
    16.
  - The proof that both loops are logarithmic. Measured, the cells touched per operation are 2.5 at n = 16 and 10.5
    at 2²⁰, about half of log₂ n.
  - Four structures on 2²⁰ numbers, mixed operations: plain array 155 µs, prefix array 130 µs, Fenwick 52 ns, and a
    bottom-up segment tree 142 ns.
* **3. Segment trees.**
  - Minimum over [3, 12] from 4 covering nodes (15 visited).
  - A four-number node for the maximum subarray: the crossing stretch wins, at 6.
  - Lazy propagation: on random ranges at n = 65,536, 57 nodes visited per update against 17,552 elements.
  - Persistence.
* **4. Range minimum and LCA.**
  - The sparse table: 54 cells for 16 values; [2, 12] answered from two windows of 8.
  - LCA as range minimum on the Euler tour (LCA(7, 4) = 1), and binary lifting.
  - The Cartesian tree, and Bender–Farach-Colton.
* **5. Two pointers and monotonic stacks.**
  - The sliding-window maximum's deque: 14 pops for 16 elements.
  - The longest stretch without a repeat: "bdaef".
  - Next greater element, and the largest rectangle under a histogram: area 16, matching brute force.
* **6. Searching for the answer.**
  - Shipping capacity found by 5 checks: 18.
  - A binary search to trust: the invariant, half-open ranges, and Bloch's overflow bug.
  - Galloping: about 2 log₂ d probes, beating binary search on a million keys while d < 1,000.
* **7. Bits and the Four Russians.**
  - Popcount, the lowest set bit and Gray codes.
  - Submask enumeration: exactly 3ⁿ pairs.
  - Bitset transitive closure: 7.6× at n = 1,024 and 10× at n = 2,048 (the byte version was already vectorized).
  - Bit-parallel LCS on two strings of 20,000: 1.45 s against 14 ms, 103×, with the same length (13,080).
* **8. Meet in the middle and square roots.**
  - Subset sum on 20 numbers: 1,048,576 sums (71 ms) against 2,058 steps (0.19 ms).
  - Square-root blocks: a range of 8,505 in 189 steps.
  - Mo's order: 2.0 million pointer moves against 84 million elements scanned.
* **9. Algorithm engineering I: layouts.** Sorted, branch-free, Eytzinger with prefetch, and a 16-key B-tree layout
  compared with AVX-512, from 1 K to 64 M keys.
  - At 64 M keys: 908, 867, 298 and 184 ns. The B-tree is 4.9× faster than the textbook.
  - Branch prediction: a filter over random bytes takes 5.3 ns an element shuffled against 0.97 sorted, and 0.88
    with a mask.
* **10. Algorithm engineering II: SIMD and hashing.**
  - Words found 32 bytes at a time: the whole corpus in 39.7 ms byte by byte against 4.5 ms with AVX2 (8.8×),
    with the same 4,609,954 words.
  - Auto-vectorization: saxpy and a sum 3.7× and 2.8× faster; a prefix sum 1.8×.
  - Swiss-style tables against linear probing and `std::unordered_map`. With 16 M slots, 7/8 full, a find takes
    66, 171 and 82 ns respectively.
* **11. Sorting in practice.**
  - Introsort, pdqsort and Timsort.
  - LSD radix sort against `std::sort`: the crossover is at about 64 keys, and radix is 3.5× faster at 16 M.
  - The top 20 of 16 M keys: a full sort takes 1.65 s, `nth_element` 127 ms, `partial_sort` 16 ms and a heap of
    20 18 ms.
* **12. Benchmarking honestly.**
  - Thirty runs: cold first repetitions average 50.1 ms against 40.2 ms warm (standard deviation 2.2 ms).
  - Environment size moved the median by up to 22%.
  - Dead-code elimination: an unused loop takes 1 µs against 123 ms with its result kept.
  - Mytkowicz et al.; Stabilizer.
* **13. Problem solving as a craft.**
  - Pólya's four steps, on counting pairs with a sum at most T. 2,000 random stress tests found 0 disagreements;
    at n = 4,000, 417 ms against 0.9 ms.
  - The interview repertoire mapped to the parts that build it.
* **14. The Job, engineered.**
  - An AVX2 tokenizer, word-at-a-time hashing, and a Swiss-style table with the first 8 letters inline.
  - 155 against 75 ms, best of 7 (2.05×), with identical output. The engineered runs spread from 75 to 124 ms.
  - Amdahl: finding words was 26% of the textbook time, so the scan alone would give only 1.3×.
  - Ledger row 10: the first row measured on real hardware, 3,700 times faster than row 1.
* **15. Frontier: learned indexes and predictions.**
  - A PGM-style learned index over the corpus's 4.6 M word offsets. At ε = 256, 64 segments (1.5 KB) answer
    searches in 254 ns against 394 ns for binary search.
  - Ski rental with predictions (Purohit–Svitkina–Kumar): consistency 1 + λ, robustness 1 + 1/λ, measured across
    forecast errors.
  - The theory–practice gap: external memory and cache-oblivious models.
  - Open problems: a cost model that ranks real implementations; learned indexes under adversarial inserts; the
    segment exponent of real text. Outro.

## Build

```bash
python -m videos.cs.cs24.compute           # every number in the part (about five minutes; run it on an idle machine)
python tools/build.py cs24 -q l            # a 480p preview
python tools/build.py cs24                 # 1080p
```

## Problems, with solutions

1. **Fenwick queries.** Prove that a Fenwick prefix query visits at most ⌊log₂ n⌋ + 1 cells, and that its ranges
   tile [1, i].

   *Solution.* Each step replaces i by i − lowbit(i), which clears the lowest set bit. So the number of steps is
   the number of set bits of i, at most ⌊log₂ i⌋ + 1 ≤ ⌊log₂ n⌋ + 1. The first cell covers (i − lowbit(i), i]. The
   next covers (i′ − lowbit(i′), i′] with i′ = i − lowbit(i), which ends exactly where the first begins. The ranges
   are therefore consecutive and disjoint, and the last ends at 0. Their union is (0, i] = [1, i].

2. **The deque is linear.** Prove that the sliding-window maximum's deque does at most 2n pushes and pops in total.

   *Solution.* Each index is pushed exactly once, when it arrives. A pop, from either end, removes an index that is
   never pushed again, so there are at most n pops in all. Hence at most 2n operations, and the while loop's
   apparently nested work is O(n) in total, whatever the window width. Our run on 16 elements did 14 pops.

3. **RMQ is LCA.** Show that every range-minimum query is a lowest-common-ancestor query in the Cartesian tree, and
   build the tree in O(n).

   *Solution.* The Cartesian tree is heap-ordered, so every node is smaller than its descendants. Its in-order
   traversal is the array. For l ≤ r, let v be the LCA of positions l and r. Then l and r lie in different subtrees
   of v, or one of them is v, so by the in-order property l ≤ v ≤ r. Every position between l and r is in v's
   subtree, so a[v] is their minimum.

   *Construction.* Scan left to right, keeping the tree's rightmost path on a stack. For each new element, pop
   every larger element. The last one popped becomes the new element's left child, and the new element becomes the
   right child of the stack's top. Each element is pushed and popped at most once, so the scan is O(n).

4. **3ⁿ submasks.** Prove that enumerating every submask of every mask of n bits takes exactly 3ⁿ steps.

   *Solution.* First, the loop s ← (s − 1) & m visits every submask of m once, in decreasing order. Subtracting
   one clears the lowest set bit of s and sets every bit below it. Masking with m keeps exactly the bits of m below
   that position, which is the largest submask of m smaller than s. So the loop visits 2^{|m|} values.

   Summing over masks, Σ_m 2^{|m|} = Σ_k C(n, k) 2^k = 3ⁿ by the binomial theorem. Equivalently, a (mask,
   submask) pair gives each element one of three states: out, in the mask only, or in both. Our counts match 3ⁿ
   exactly for n = 2 to 12.

5. **Build: a Fenwick tree in Pebble.** Over the Job's word counts, answer "how many words of the novel are among
   the top k?" for every k.

   *Solution sketch.* After the Job has counted, rank the distinct words by frequency (Part 17's heap gives the
   order). Insert each word's count into a Fenwick tree at its rank. Then prefix(k) is the number of word
   occurrences covered by the k most frequent words. Plotted for every k, that is the corpus's Zipf curve.

   The Pebble language has no bitwise operators, so lowbit cannot be i & −i. Precompute it in an array with the
   recurrence low[i] = 1 for odd i and low[i] = 2·low[i/2] for even i: O(n) once, then O(1) per step. Check every
   prefix against a running sum computed directly. Count the emulator's instructions per query against log₂ k.

6. ★ **Research: why do real keys need fewer segments?** Our corpus's learned-index segments cover about ε^{1.4}
   keys each. Ferragina, Lillo and Vinciguerra proved Θ(ε²) for keys whose gaps are independent with finite
   variance. Model the gaps of real text, with their correlations, and prove a bound that matches; or show which
   property of text breaks the independent-gaps theory.

   *Where to start.*
   - Ferragina, Lillo and Vinciguerra, "Why are learned indexes so effective?" (ICML 2020): the ε² result, via the
     mean exit time of a random walk from a strip.
   - Ferragina and Vinciguerra, "The PGM-index" (VLDB 2020): the optimal piecewise-linear fit, which our greedy cone
     approximates.

   Measure first. Compute the autocorrelation of word lengths and of the gaps between word starts in the corpus.
   Then fit a correlated walk (a short-memory linear process, or a hierarchical model with sentence and paragraph
   breaks), and compare its predicted exit times with our segment counts at ε = 4 to 1,024. The exponent drifts
   downwards as ε grows (about 1.5, 1.3, 1.25 and 0.8 between successive pairs), so a correct model must explain the
   drift too.

## 习题与解答

1. **Fenwick 查询。** 证明 Fenwick 前缀查询至多访问 ⌊log₂ n⌋ + 1 个单元，且这些区间恰好拼成 [1, i]。

   *解答。* 每一步把 i 换成 i − lowbit(i)，即清除最低的置位比特，所以步数等于 i 的置位比特数，至多为 ⌊log₂ i⌋ + 1 ≤ ⌊log₂ n⌋ + 1。
   第一个单元覆盖 (i − lowbit(i), i]；下一个覆盖 (i′ − lowbit(i′), i′]，其中 i′ = i − lowbit(i)，它恰好在第一个的起点处结束。所以
   这些区间首尾相接、互不重叠，最后一个结束于 0：并集为 (0, i] = [1, i]。

2. **双端队列是线性的。** 证明滑动窗口最大值的双端队列总共至多做 2n 次压入和弹出。

   *解答。* 每个下标在到达时恰好被压入一次。一次弹出（无论从哪一端）移走的下标不会再被压入，所以弹出总数至多为 n。因此至多 2n 次操作，
   看似嵌套的 while 循环总共只做 O(n) 的工作，与窗口宽度无关。我们在 16 个元素上的运行共弹出 14 次。

3. **RMQ 就是 LCA。** 证明每个区间最小值查询都是 Cartesian 树中的最近公共祖先查询，并在 O(n) 时间内建树。

   *解答。* Cartesian 树是堆有序的（每个节点小于它的后代），且其中序遍历就是原数组。对 l ≤ r，令 v 为位置 l 和 r 的 LCA。则 l 与 r
   分属 v 的不同子树（或其中之一就是 v），由中序性质得 l ≤ v ≤ r；而 l 与 r 之间的每个位置都在 v 的子树中，所以 a[v] 是它们的最小值。
   建树：从左到右扫描，用一个栈保存树的最右路径；对每个新元素，弹出所有比它大的元素，最后弹出的成为新元素的左孩子，新元素成为栈顶的右孩子。
   每个元素至多压入、弹出一次：O(n)。

4. **3ⁿ 个子掩码。** 证明枚举 n 位所有掩码的所有子掩码恰好需要 3ⁿ 步。

   *解答。* 首先，循环 s ← (s − 1) & m 按递减顺序恰好访问 m 的每个子掩码一次：减一清除 s 的最低置位比特并把其下所有比特置一，与 m
   相与则只保留 m 在该位置以下的比特，这正是小于 s 的最大子掩码。所以它访问 2^{|m|} 个值。对所有掩码求和，Σ_m 2^{|m|} =
   Σ_k C(n, k) 2^k = 3ⁿ（二项式定理）。等价地，一个（掩码，子掩码）对给每个元素三种状态之一：不在掩码中、只在掩码中、在两者中。我们的计数
   在 n = 2 到 12 时都恰好等于 3ⁿ。

5. **构造：Pebble 中的 Fenwick 树。** 在 Job 的词频上，对每个 k 回答“小说中有多少个词属于前 k 个最常见的词？”

   *解答提要。* Job 计数之后，按频率给不同的词排名（第17部分的堆给出顺序），把每个词的计数插入 Fenwick 树中对应排名的位置。于是
   prefix(k) 就是前 k 个最常见词所覆盖的词次数；对每个 k 作图，就是语料的 Zipf 曲线。Pebble 语言没有位运算，所以 lowbit 不能写成 i & −i：
   用递推 low[i] = 1（i 为奇数）、low[i] = 2·low[i/2]（i 为偶数）预先算出一个数组，一次 O(n)，之后每步 O(1)。用直接计算的累加和核对
   每个前缀，并把模拟器每次查询的指令数与 log₂ k 比较。

6. ★ **研究：为什么真实的键需要更少的段？** 我们语料的学习索引中，每段覆盖的键数约为 ε^{1.4}；Ferragina、Lillo 与 Vinciguerra 证明，
   若键之间的间隔独立且方差有限，则为 Θ(ε²)。为真实文本的间隔（及其相关性）建模，证明一个与之吻合的界；或者指出文本的哪种性质打破了独立
   间隔的理论。

   *从哪里入手。* Ferragina、Lillo 与 Vinciguerra，“Why are learned indexes so effective?”（ICML 2020）：通过随机游走离开一条带状区域的
   平均时间得到 ε² 的结果。Ferragina 与 Vinciguerra，“The PGM-index”（VLDB 2020）：最优的分段线性拟合，我们的贪心锥形拟合是它的近似。
   先测量：计算语料中词长以及词起点间隔的自相关；然后拟合一个相关的游走（短记忆线性过程，或带句子与段落断点的层次模型），把它预测的离开时间与
   我们在 ε = 4 到 1,024 时的段数比较。随着 ε 增大，指数逐渐下降（相邻两点之间约为 1.5、1.3、1.25、0.8），一个正确的模型也必须解释这种
   漂移。

## Glossary additions

前缀和 prefix sum · 差分数组 difference array · 积分图 integral image · 扫描（并行前缀） scan · Fenwick 树 Fenwick tree · 最低置位比特
lowest set bit · 线段树 segment tree · 幺半群 monoid · 懒惰传播 lazy propagation · 可持久化 persistence · 稀疏表 sparse table · 幂等
idempotence · 区间最小值 range minimum query · 最近公共祖先 lowest common ancestor · 欧拉序 Euler tour · 倍增 binary lifting ·
Cartesian 树 Cartesian tree · 双指针 two pointers · 滑动窗口 sliding window · 单调队列 monotonic deque · 单调栈 monotonic stack ·
二分答案 binary search on the answer · 倍增查找 galloping search · 三分查找 ternary search · 位运算 bit manipulation · 子掩码 submask ·
四个俄罗斯人算法 Four Russians · 位并行 bit-parallelism · 折半搜索 meet in the middle · 分块 square-root decomposition · 莫队算法 Mo's
algorithm · 算法工程 algorithm engineering · Eytzinger 布局 Eytzinger layout · 预取 prefetching · 分支预测 branch prediction · 无分支
branch-free · 向量化 vectorization · SIMD · Swiss 表 Swiss table · 控制字节 control byte · 基数排序 radix sort · 内省排序 introsort ·
前 k 个 top-k · 预热 warm-up · 置信区间 confidence interval · 死代码消除 dead-code elimination · Amdahl 定律 Amdahl's law · 学习索引
learned index · 带预测的算法 algorithms with predictions · 一致性 consistency · 鲁棒性 robustness · 缓存无关 cache-oblivious

## Sources

*Canon.* Books:
- Skiena, *The Algorithm Design Manual* (3rd ed., 2020);
- Bentley, *Programming Pearls* (2nd ed., 1999);
- Warren, *Hacker's Delight* (2nd ed., 2012);
- Laaksonen, *Guide to Competitive Programming* (2nd ed., 2020);
- Halim & Halim, *Competitive Programming 4* (2020);
- Müller-Hannemann & Schirra (eds.), *Algorithm Engineering* (2010);
- Pólya, *How to Solve It* (1945);
- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (6th ed., 2017).

Papers:
- Range queries: Crow, "Summed-area tables for texture mapping" (1984); Viola & Jones (2001); Fenwick, "A new data
  structure for cumulative frequency tables" (1994); Bentley (1977, segment trees); Harel & Tarjan (1984); Bender &
  Farach-Colton, "The LCA problem revisited" (2000); Fischer & Heun (2011); Hillis & Steele, "Data parallel
  algorithms" (1986); Blelloch, "Prefix sums and their applications" (1990).
- Searching: Bentley & Yao, "An almost optimal algorithm for unbounded searching" (1976); Bloch, "Nearly all binary
  searches and mergesorts are broken" (2006); Khuong & Morin, "Array layouts for comparison-based searching" (2017).
- Bits: Arlazarov, Dinic, Kronrod & Faradzev (1970); Allison & Dix (1986); Hyyrö, "Bit-parallel LCS-length
  computation revisited" (2004); Horowitz & Sahni (1974).
- Engineering: Langdale & Lemire, "Parsing gigabytes of JSON per second" (2019); Abseil's Swiss tables (Kulukundis,
  CppCon 2017); Musser, "Introspective sorting and selection algorithms" (1997); Peters, "Pattern-defeating
  quicksort" (2021); Mytkowicz, Diwan, Hauswirth & Sweeney, "Producing wrong data without doing anything obviously
  wrong!" (2009); Curtsinger & Berger, "Stabilizer" (2013); Amdahl (1967).
- Memory models: Aggarwal & Vitter, "The input/output complexity of sorting and related problems" (1988); Frigo,
  Leiserson, Prokop & Ramachandran, "Cache-oblivious algorithms" (1999).
- Frontier: Kraska, Beutel, Chi, Dean & Polyzotis, "The case for learned index structures" (2018); Ferragina &
  Vinciguerra, "The PGM-index" (2020); Ferragina, Lillo & Vinciguerra, "Why are learned indexes so effective?"
  (2020); Purohit, Svitkina & Kumar, "Improving online algorithms via ML predictions" (2018); Lykouris &
  Vassilvitskii, "Competitive caching with machine learned advice" (2018).
