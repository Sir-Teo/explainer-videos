# Computer Science, Built — Part 16: Counting Steps

Part 16 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act IV, *Algorithms*. Seven ledger rows of better machines left the Job
quadratic; this part learns to count steps, proves what sorting must cost, and sorts the Job. The instruments are
`explainer/cs/algo/sorts.py` (insertion, binary insertion, merge, heap, quick with three pivot rules, Ford–Johnson
merge insertion, counting and radix sort, Python's Timsort counted through a key wrapper, quickselect, median of
medians, decision trees, the dynamic array, replacement selection, every one counting its comparisons) and
`explainer/cs/algo/job.py` (the Job v1, sort then count, in the Pebble language; an exact simulator of its control
flow that counts 24 events; a least-squares model of its instruction count; and a C program that counts the same
events on all thirty novels), tested in `tests/test_cs16_sorts.py`. Every number is computed in `compute.py`;
`ram`, `linear` and `practice` time code on this machine.

* **Can thinking beat silicon?** The ledger so far; the Job v0's cost per byte rising from about 290 cycles on
  10 kB to 4,279 on the corpus.
* **1. What counts as a step.** The RAM and the word-RAM; repeated squaring timed in CPython (each step about three
  times the last); Turing machines, the comparison model, cell probes, external memory.
* **2. Orders of growth.** O, Ω, Θ and o; the ladder on log–log axes; the largest n solvable at a nanosecond a
  step; Stirling's formula checked.
* **3. Insertion sort and its invariant.** The invariant animated; inversions, n(n − 1)/4 derived and measured;
  binary insertion, fewer comparisons and the same moves.
* **4. Merge sort and the recursion tree.** Merging animated; the tree for 2T(n/2) + n; the substitution method;
  comparisons against n lg n and the lower bound.
* **5. The master theorem.** The three cases; their geometry as level-by-level bars (Karatsuba, merge sort, a
  heavy combine); the geometric-series proof; five recurrences; Akra–Bazzi computed.
* **6. The comparison lower bound.** The decision tree of insertion sort on three keys; lg n! and information;
  min-and-max by adversary (⌈3n/2⌉ − 2); merge insertion meets the bound for n ≤ 11, and 30 > 29 at n = 12.
* **7. Heapsort.** The heap in an array; Floyd's linear heapify (Σ h/2ʰ = 2, under 2 comparisons per element
  measured); heapsort's 1.8 n lg n; introsort.
* **8. Quicksort, and 2n ln n.** Partition; Hoare's two pointers animated; the 2/(j − i + 1) argument; the exact
  mean measured; pivot rules on sorted input (1,999,000 against about 21,000); dual pivot.
* **9. How lucky can quicksort get?** The recurrence solved by telescoping; 10,000 runs: σ = 0.639 n against
  theory's 0.648 n; the tails; McDiarmid and Hayward.
* **10. Beating n log n.** Counting and radix sort; radix sort animated; timed in C (ten million keys: radix sort
  3.8× faster than `std::sort`); integer sorting on the word-RAM.
* **11. Selection and the median of medians.** Quickselect (3.36 n measured, 3.39 n theory); why groups of five;
  median of medians (7.8 n).
* **12. Generating functions.** Fibonacci and Binet; Catalan numbers from a quadratic; the singularity and
  4ⁿ/(√π n^{3/2}).
* **13. Amortized analysis.** The doubling array; a binary counter; aggregate, accounting and potential; growth
  factor 2 against 1.5 and memory reuse.
* **14. Sorting in practice.** Timsort's comparisons on presorted data; the 2015 invariant bug; external merge sort
  and replacement selection (runs of 2,001 for M = 1,000).
* **15. The Job, sorted.** The Job v1; counts on the corpus (15.0 billion key comparisons against 103 million); the
  instruction model (within 0.5% on held-out passages); where the instructions go; ledger row 7 (5.1 s, 11× row
  5, 2.3× four cores).
* **16. Frontier: beyond the worst case.** Smoothed analysis measured on quicksort; integer sorting results;
  fine-grained complexity; open problems. Outro.

## Build

```bash
python -m videos.cs.cs16.compute           # every number in the part (a few minutes)
python tools/build.py cs16 -q l            # a 480p preview
python tools/build.py cs16                 # 1080p
```

## Problems, with solutions

1. **Insertion sort's cost.** Show that insertion sort makes at most I + n − 1 comparisons, where I is the number of
   inversions, and that E[I] = n(n − 1)/4 for a random order.

   *Solution.* In the inner loop for element i, each comparison either finds a larger element, which is then
   shifted one place right, or ends the loop. A shift exchanges an adjacent inverted pair, removing exactly one
   inversion and creating none, so there are exactly I shifts in all, and at most one loop-ending comparison per
   i: at most I + n − 1 comparisons. For a random order, each of the n(n − 1)/2 pairs is inverted with probability
   1/2 by symmetry (reversing the pair's relative order is a bijection between orders), so by linearity of
   expectation E[I] = n(n − 1)/4. (`compute.py`'s `insertion` item measures both.)

2. **Between the cases.** Solve T(n) = 4T(n/2) + n² lg n with a recursion tree.

   *Solution.* Level j has 4ʲ subproblems of size n/2ʲ, costing 4ʲ (n/2ʲ)² lg(n/2ʲ) = n² (lg n − j). Summing over
   j = 0, …, lg n gives n² (lg n + (lg n − 1) + ⋯ + 0) = n² lg n (lg n + 1)/2 = Θ(n² log² n). Here f(n) = n^{log_b a}
   lg n exceeds n^{log_b a} but not by a polynomial factor, so neither case 2 nor case 3 of the basic theorem
   applies; the extended case 2 (f = Θ(n^{log_b a} logᵏ n) gives Θ(n^{log_b a} log^{k+1} n)) agrees.

3. **Minimum and maximum.** Prove that finding both the minimum and the maximum of n items needs ⌈3n/2⌉ − 2
   comparisons, and give an algorithm that uses exactly that many.

   *Solution.* Algorithm: compare the items in pairs (⌊n/2⌋ comparisons), then find the maximum of the winners and
   the minimum of the losers (with an odd item joining both groups), ⌈n/2⌉ − 1 comparisons each: ⌈3n/2⌉ − 2 in all.
   Lower bound: say an item has *won* if it was ever larger in a comparison and *lost* if ever smaller. At the end,
   every item but the maximum must have lost and every item but the minimum must have won: 2n − 2 units of
   information. A comparison between two untouched items gives two units; the adversary answers every other
   comparison so as to give at most one (it can always keep its answers consistent by treating winners as large
   and losers as small). At most ⌊n/2⌋ comparisons are between untouched items, so the number of comparisons is at
   least ⌊n/2⌋ + (2n − 2 − 2⌊n/2⌋) = ⌈3n/2⌉ − 2 (Pohl 1972).

4. **Quickselect for the minimum.** Show that quickselect, asked for the minimum, makes 2n − 2Hₙ comparisons on
   average.

   *Solution.* After n − 1 comparisons the pivot has a uniform rank r; if r = 1 we are done, otherwise we recurse
   on the r − 1 smaller items. So Cₙ = n − 1 + (1/n) Σ_{k=0}^{n−1} C_k. Multiplying by n and subtracting the same
   equation for n − 1 gives nCₙ − (n − 1)C_{n−1} = 2(n − 1) + C_{n−1}, that is Cₙ = C_{n−1} + 2 − 2/n. With C₁ = 0,
   summing gives Cₙ = 2n − 2Hₙ: about twice the n − 1 of a plain scan.

5. **Build: radix sort for the Job.** Rewrite the Job v1 with a radix sort on letters, in the Pebble language, and
   compare its instruction count with the merge sort on our passages.

   *Solution sketch.* Use most-significant-digit radix sort with 27 buckets per level (end of word, then a to z):
   count the occurrences in each bucket, compute offsets, distribute stably into a scratch array, then recurse into
   each bucket on the next letter, switching to insertion sort for buckets smaller than about 16. Each letter of a
   word's distinguishing prefix is examined once, instead of once per comparison at each of lg n merge levels, so
   the 305 million letter comparisons of the merge sort (`job` item, `k_steps`) are replaced by roughly the total
   distinguishing-prefix length; but every recursion level pays for its 27 counters, which dominates on small
   passages. Compute the distinguishing-prefix total for the corpus with a variant of `FEATURES_C`, fit the new
   program's instruction count as in `job.py`, and compare: the crossover between merge sort and radix sort is the
   answer.

6. **★ Research: sorting integers in linear time.** Sort n word-size integers in O(n) time on a word-RAM, or prove
   that no algorithm can, in a model that allows the usual arithmetic.

   *Where to start.* Upper bounds: Fredman and Willard's fusion trees (1990) first beat n log n; Andersson, Hagerup,
   Nilsson and Raman (1995) sort in O(n log log n), and in linear time when the word length is at least log^{2+ε} n;
   Han and Thorup (2002) reach O(n √(log log n)) expected; Belazzougui, Brodal and Nielsen (2014) give expected
   linear time for words of Ω(log² n log log n) bits. Lower bounds: none superlinear is known for sorting on the
   word-RAM; strong bounds exist in restricted models (comparisons, and AC⁰ instruction sets) and for related
   problems such as predecessor search (Pătraşcu and Thorup 2006). Open: (a) linear time for every word length;
   (b) a superlinear lower bound in any natural model with multiplication; (c) on Pebble's 32-bit words, measure how
   far radix sort and the fastest comparison sort are from each other as n grows.

## 习题与解答

1. **插入排序的代价。** 证明插入排序至多做 I + n − 1 次比较，其中 I 是逆序对的个数；并证明对随机顺序 E[I] = n(n − 1)/4。

   *解答。* 在元素 i 的内层循环里，每次比较要么找到一个更大的元素，把它右移一位，要么结束循环。一次右移交换一对相邻的
   逆序元素，恰好消除一个逆序对且不产生新的，所以总共恰好 I 次右移，而每个 i 至多一次结束循环的比较：至多 I + n − 1
   次比较。对随机顺序，n(n − 1)/2 对中的每一对由对称性以 1/2 的概率逆序（交换这一对的相对次序是各种顺序之间的双射），
   由期望的线性性，E[I] = n(n − 1)/4。（`compute.py` 的 `insertion` 一项测量了这两者。）

2. **夹在两种情形之间。** 用递归树求解 T(n) = 4T(n/2) + n² lg n。

   *解答。* 第 j 层有 4ʲ 个规模为 n/2ʲ 的子问题，代价为 4ʲ (n/2ʲ)² lg(n/2ʲ) = n² (lg n − j)。对 j = 0, …, lg n 求和，
   得 n² (lg n + (lg n − 1) + ⋯ + 0) = n² lg n (lg n + 1)/2 = Θ(n² log² n)。这里 f(n) = n^{log_b a} lg n 比 n^{log_b a}
   大，但不是大一个多项式因子，所以基本定理的情形 2 和情形 3 都不适用；推广的情形 2（f = Θ(n^{log_b a} logᵏ n) 时
   T = Θ(n^{log_b a} log^{k+1} n)）给出相同的结果。

3. **最小值与最大值。** 证明同时找出 n 个元素的最小值和最大值需要 ⌈3n/2⌉ − 2 次比较，并给出恰好用这么多次的算法。

   *解答。* 算法：先两两比较（⌊n/2⌋ 次），再在胜者中找最大、在败者中找最小（多出的一个元素两组都参加），各需
   ⌈n/2⌉ − 1 次：共 ⌈3n/2⌉ − 2 次。下界：如果一个元素在某次比较中较大，就说它“赢过”，较小则“输过”。结束时，除最大值外
   每个元素都必须输过，除最小值外每个元素都必须赢过：共 2n − 2 个信息单位。两个从未比较过的元素之间的比较给出两个单位；
   对其他每次比较，对手总能回答得只给出至多一个单位（把赢过的当作大、输过的当作小，回答总能保持一致）。两个从未比较过的
   元素之间的比较至多 ⌊n/2⌋ 次，所以比较次数至少为 ⌊n/2⌋ + (2n − 2 − 2⌊n/2⌋) = ⌈3n/2⌉ − 2（波尔，1972）。

4. **用快速选择找最小值。** 证明快速选择在找最小值时平均做 2n − 2Hₙ 次比较。

   *解答。* n − 1 次比较之后，枢轴的秩 r 是均匀的；r = 1 时结束，否则在比它小的 r − 1 个元素上递归。所以
   Cₙ = n − 1 + (1/n) Σ_{k=0}^{n−1} C_k。乘以 n，再减去 n − 1 时的同一个方程，得 nCₙ − (n − 1)C_{n−1} = 2(n − 1) +
   C_{n−1}，即 Cₙ = C_{n−1} + 2 − 2/n。由 C₁ = 0 求和得 Cₙ = 2n − 2Hₙ：大约是直接扫描一遍的 n − 1 次的两倍。

5. **动手：给任务用基数排序。** 用 Pebble 语言把任务 v1 改写成按字母做基数排序，并在我们的文本段上与归并排序比较
   指令数。

   *解答要点。* 用最高位优先的基数排序，每层 27 个桶（词尾，然后 a 到 z）：数出每个桶里的出现次数，算出偏移量，稳定地
   分发到一个临时数组，再对每个桶按下一个字母递归，桶小于大约 16 个元素时改用插入排序。单词区分前缀中的每个字母只被
   检查一次，而不是在 lg n 层归并的每次比较中各检查一次，所以归并排序的 3.05 亿次字母比较（`job` 一项的 `k_steps`）
   大致变成区分前缀的总长度；但每一层递归都要为它的 27 个计数器付出代价，这在小文本段上占主导。用 `FEATURES_C` 的
   一个变体在语料上计算区分前缀总长度，像 `job.py` 那样拟合新程序的指令数，再作比较：归并排序与基数排序的交叉点就是
   答案。

6. **★ 研究：线性时间的整数排序。** 在字 RAM 上用 O(n) 时间对 n 个字长整数排序，或者证明在允许常规算术的模型里没有
   算法能做到。

   *从哪里开始。* 上界：弗雷德曼与威拉德的融合树（1990）首先突破了 n log n；安德松、哈格鲁普、尼尔松与拉曼（1995）
   在 O(n log log n) 内排序，当字长至少为 log^{2+ε} n 时可达线性；韩与托鲁普（2002）达到期望 O(n √(log log n))；
   贝拉祖吉、布罗达尔与尼尔森（2014）对 Ω(log² n log log n) 位的字给出期望线性时间。下界：字 RAM 上的排序还没有已知的
   超线性下界；在受限模型（比较模型、AC⁰ 指令集）以及前驱查找等相关问题上有强下界（珀特拉什库与托鲁普，2006）。
   尚未解决的：（a）对所有字长都达到线性时间；（b）在任何带乘法的自然模型中给出超线性下界；（c）在 Pebble 的 32 位字
   上，测量随着 n 增长，基数排序与最快的比较排序相差多远。

## Glossary additions

步数 step count · 计算模型 model of computation · 随机存取机 RAM · 字 RAM word-RAM · 单位代价 unit cost · 细胞探测模型
cell-probe model · 外存模型 external-memory model · 渐近记号 asymptotic notation · 大 O / Ω / Θ / 小 o big O / Omega /
Theta / little o · 斯特林公式 Stirling's formula · 循环不变式 loop invariant · 逆序对 inversion · 插入排序 insertion sort ·
二分插入 binary insertion · 归并排序 merge sort · 稳定 stable · 递归树 recursion tree · 代入法 substitution method · 主定理
master theorem · 决策树 decision tree · 比较下界 comparison lower bound · 对手论证 adversary argument · 归并插入
merge insertion · 堆 heap · 堆排序 heapsort · 堆化 heapify · 内省排序 introsort · 快速排序 quicksort · 枢轴 pivot · 划分
partition · 双枢轴 dual pivot · 集中性 concentration · 尾部界 tail bound · 计数排序 counting sort · 基数排序 radix sort ·
快速选择 quickselect · 中位数的中位数 median of medians · 生成函数 generating function · 卡特兰数 Catalan numbers · 解析
组合 analytic combinatorics · 奇点 singularity · 摊还分析 amortized analysis · 势函数 potential function · 动态数组 dynamic
array · 增长因子 growth factor · 外部归并排序 external merge sort · 置换选择 replacement selection · 平滑分析 smoothed
analysis · 细粒度复杂性 fine-grained complexity · 强指数时间假说 strong exponential time hypothesis (SETH)

## Sources

*Canon.* Books: Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, chapters 1–9, 16–17; Knuth, *The Art
of Computer Programming*, volume 3, *Sorting and Searching*; Sedgewick & Flajolet, *An Introduction to the Analysis
of Algorithms*; Graham, Knuth & Patashnik, *Concrete Mathematics*; Flajolet & Sedgewick, *Analytic Combinatorics*
(2009); Kleinberg & Tardos, *Algorithm Design*; Erickson, *Algorithms*.

Papers: Ford & Johnson, "A tournament problem" (1959); Hoare, "Algorithm 64: Quicksort" (1961) and "Quicksort"
(1962); Williams, "Algorithm 232: Heapsort" (1964); Floyd, "Algorithm 245: Treesort 3" (1964); Wells (1965); Pohl,
"A sorting problem and its complexity" (1972); Blum, Floyd, Pratt, Rivest & Tarjan, "Time bounds for selection"
(1973); Knuth, "Big Omicron and big Omega and big Theta" (1976); Bentley, Haken & Saxe, "A general method for solving
divide-and-conquer recurrences" (1980); Tarjan, "Amortized computational complexity" (1985); Aggarwal & Vitter, "The
input/output complexity of sorting and related problems" (1988); McDiarmid & Hayward, "Large deviations for
Quicksort" (1996); Akra & Bazzi, "On the solution of linear recurrence equations" (1998); Peters, "listsort.txt"
(2002); Yaroslavskiy, dual-pivot quicksort (2009); de Gouw, Rot, de Boer, Bubel & Hähnle, "OpenJDK's
java.utils.Collection.sort() is broken" (2015); O. Peters, "Pattern-defeating quicksort" (2021).

*Frontier.* Spielman & Teng, "Smoothed analysis of algorithms" (2001); Banderier, Beier & Mehlhorn, "Smoothed
analysis of three combinatorial problems" (2003); van Emde Boas (1975); Fredman & Willard, fusion trees (1990);
Andersson, Hagerup, Nilsson & Raman, "Sorting in linear time?" (1995); Han & Thorup, "Integer sorting in O(n √(log
log n)) expected time and linear space" (2002); Belazzougui, Brodal & Nielsen (2014); Backurs & Indyk, "Edit distance
cannot be computed in strongly subquadratic time (unless SETH is false)" (2015); Williams, "On some fine-grained
questions in algorithms and complexity" (2018).
