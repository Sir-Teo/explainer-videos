# Computer Science, Built — Part 16: Counting Steps

Part 16 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act IV, *Algorithms*. Seven ledger rows of better machines left the Job
quadratic; this part learns to count steps, proves what sorting must cost, and sorts the Job. The instruments are
`explainer/cs/algo/sorts.py` (insertion, binary insertion, merge, heap, quick with three pivot rules, Ford–Johnson
merge insertion, counting and radix sort, Python's Timsort counted through a key wrapper, quickselect, median of
medians, decision trees, the dynamic array, replacement selection, with explicitly defined key-comparison counters) and
`explainer/cs/algo/job.py` (the Job v1, sort then count, in the Pebble language; an exact simulator of its control
flow that counts 24 events; a least-squares model of its instruction count; and a C program that counts the same
events on all thirty novels), tested in `tests/test_cs16_sorts.py`. Every number is computed in `compute.py`;
`ram` and `linear` time code on this machine; `practice` counts comparisons through a wrapper.

* **Can thinking beat silicon?** The ledger so far; the Job v0's cost per byte rising from about 290 cycles on
  10 kB to 4,279 on the corpus.
* **1. What counts as a step.** The RAM and the word-RAM; repeated squaring timed in the actual host interpreter (minimum of three, result checked; no fixed timing ratio); Turing machines, the comparison model, cell probes, external memory.
* **2. Orders of growth.** O, Ω, Θ and o; the ladder on log–log axes; the largest n solvable at a nanosecond a
  step; Stirling's formula checked.
* **3. Insertion sort and its invariant.** The invariant animated; inversions, n(n − 1)/4 derived and measured;
  binary insertion, fewer comparisons and the same moves.
* **4. Merge sort and the recursion tree.** Merging animated; the tree for 2T(n/2) + n; the substitution method;
  comparisons against n lg n and the lower bound.
* **5. The master theorem.** The three cases; their geometry as level-by-level bars (Karatsuba, merge sort, a
  heavy combine); the geometric-series proof; five recurrences; an explicit floor/complement integer example alongside Akra–Bazzi.
* **6. The comparison lower bound.** The decision tree of insertion sort on three keys; lg n! and information;
  min-and-max by adversary (⌈3n/2⌉ − 2); merge insertion meets the bound for n ≤ 11, and 30 > 29 at n = 12.
* **7. Heapsort.** The heap in an array; Floyd's linear heapify (Σ h/2ʰ = 2, under 2 comparisons per element
  measured); heapsort's 1.8 n lg n; introsort.
* **8. Quicksort, and 2n ln n.** Partition; Hoare's two pointers animated; the 2/(j − i + 1) argument; the exact
  mean measured; pivot rules on sorted input (1,999,000 against about 21,000); dual pivot.
* **9. How lucky can quicksort get?** The recurrence solved by telescoping; 10,000 runs: σ = 0.639 n against
  the large-n theoretical coefficient 0.648 n; the tails; McDiarmid and Hayward.
* **10. Beating n log n.** Counting and radix sort; radix sort animated; timed with full reference-output checks, a common 32-bit source and a separate 16-bit counting domain; integer sorting on the word-RAM.
* **11. Selection and the median of medians.** Quickselect (finite sample mean versus its 3.39 n asymptotic leading term); why groups of five;
  median of medians with actual group-sort tests plus logical partition comparisons (8.29 n in the largest displayed sample).
* **12. Generating functions.** Fibonacci and Binet; Catalan numbers from a quadratic; the singularity and
  4ⁿ/(√π n^{3/2}).
* **13. Amortized analysis.** The doubling array; a binary counter; aggregate, accounting and potential; growth
  factor 2 against 1.5 and an aggregate freed-size necessary condition, not guaranteed allocator reuse.
* **14. Sorting in practice.** Timsort's comparisons on presorted data; the 2015 invariant bug; external merge sort
  and replacement selection (runs of 2,001 for M = 1,000).
* **15. The Job, sorted.** The Job v1; counts on the corpus (15.0 billion key comparisons against 103 million); the
  instruction fit (maximum error under 0.5% on these ten held-out passages); grouped fitted terms, with rank 19/25
  and nonunique attribution; explicitly enlarged arrays and 128 MiB modeled RAM; projected ledger row 7.
* **16. Frontier: beyond the worst case.** a ten-trial Gaussian-noise illustration for one sorted input family; condition-specific historical integer-sorting results;
  fine-grained complexity; open problems. Outro.

## Build

```bash
python -m videos.cs.cs16.compute           # every number in the part (a few minutes)
python tools/build.py cs16 -q l            # a 480p preview
python tools/build.py cs16                 # 1080p
```

## Cost and measurement models

Quicksort and selection charge one logical three-way partition comparison per nonpivot key; this is not a count
of Python predicates or CPU instructions. The distinct-key formulas use independent uniform pivots. Median-of-three
and median-of-medians count their actual small-group insertion-sort tests. The median quickselect coefficient is
asymptotic. The finite-group selection guarantee includes O(1) boundary terms; the elementary groups-of-three
upper-bound recurrence does not establish a matching lower bound.

The recurrence pictures state their power-of-b/base conventions. The uneven numeric example uses T(n)=n for n≤2,
then T(floor(n/3))+T(n-floor(n/3))+n. The doubling-array potential is max(0,2size−capacity), including the initial
empty state. A freed-size sum does not model adjacency or fragmentation.

Native timings use positive clocks, minimum-of-three repeats and full sorted-reference checks outside timing.
The 32-bit methods share seeded inputs; counting uses the separately masked 16-bit domain. Input copies/reference
checks are excluded, while counting's counter allocation is included. Python sort comparisons are wrapper counts,
and its input labeled `n/100 swaps` performs exactly that many random transpositions. Library algorithms depend
on version: the measured Python uses powersort's merge policy; Rust replaced both standard sorts in 1.81.

The Job's corpus-sized static image is calibrated on 40 emulator passages and three core passages, with output
checks. Full-corpus native event counts are exact for that event model; fitted instructions, passage-IPC cycles
and seconds remain projections. The correlated fit has rank 19/25, so its grouped terms are not unique causal
instruction/time shares. Alternating scratch/source arrays is an optimization candidate requiring a changed
program and new measurement. The corrected v0 letter count is `matched + same_length − (words − distinct)`:
matched letters plus the first mismatch on each unsuccessful same-length lookup.

比较模型先声明计什么：快速排序和选择对每个非枢轴键计一次逻辑划分比较，不是 Python 谓词或 CPU 指令数。
互异键期望式假设独立均匀枢轴；小组排序比较实际计数。递推注明基本情形与取整，空数组初始势能为零。
计时与比较次数分开，16 位计数排序与 32 位排序的值域分开，释放总大小与真实分配器复用分开。
语料事件、文本段实测、拟合指令数和 IPC 时间投影也分别注明。相关拟合系数不能直接当作因果时间份额。

## Problems, with solutions

1. **Insertion sort's cost.** For n ≥ 1 and distinct keys, show that insertion sort makes at most I + n − 1 comparisons, where I is the number of
   inversions, and that E[I] = n(n − 1)/4 for a uniformly random permutation of those distinct keys.

   *Solution.* In the inner loop for element i, each comparison either finds a larger element, which is then
   shifted one place right, or ends the loop. A shift exchanges an adjacent inverted pair, removing exactly one
   inversion and creating none, so there are exactly I shifts in all, and at most one loop-ending comparison per
   i: at most I + n − 1 comparisons. For a random order, each of the n(n − 1)/2 pairs is inverted with probability
   1/2 by symmetry (reversing the pair's relative order is a bijection between orders), so by linearity of
   expectation E[I] = n(n − 1)/4. (`compute.py`'s `insertion` item measures both.)

2. **Between the cases.** For n = 2^h and positive constant T(1), solve T(n) = 4T(n/2) + n² lg n with a recursion tree.

   *Solution.* Level j has 4ʲ subproblems of size n/2ʲ, costing 4ʲ (n/2ʲ)² lg(n/2ʲ) = n² (lg n − j). Summing over
   j = 0, …, lg n gives n² (lg n + (lg n − 1) + ⋯ + 0) = n² lg n (lg n + 1)/2 = Θ(n² log² n). This is the internal combine sum; add the n² leaves at constant base cost, which does not change the asymptotic answer. Here f(n) = n^{log_b a}
   lg n exceeds n^{log_b a} but not by a polynomial factor, so neither case 2 nor case 3 of the basic theorem
   applies; the extended case 2 (f = Θ(n^{log_b a} logᵏ n) gives Θ(n^{log_b a} log^{k+1} n)) agrees.

3. **Minimum and maximum.** For n ≥ 1 distinct items, prove that finding both the minimum and the maximum of n items needs ⌈3n/2⌉ − 2
   comparisons, and give an algorithm that uses exactly that many.

   *Solution.* Algorithm: compare the items in pairs (⌊n/2⌋ comparisons), then find the maximum of the winners and
   the minimum of the losers (with an odd item joining both groups), ⌈n/2⌉ − 1 comparisons each: ⌈3n/2⌉ − 2 in all.
   Lower bound: say an item has *won* if it was ever larger in a comparison and *lost* if ever smaller. At the end,
   every item but the maximum must have lost and every item but the minimum must have won: 2n − 2 units of
   information. A comparison between two untouched items gives two units; the adversary answers every other
   comparison so as to give at most one (it can always keep its answers consistent by treating winners as large
   and losers as small). At most ⌊n/2⌋ comparisons are between untouched items, so the number of comparisons is at
   least ⌊n/2⌋ + (2n − 2 − 2⌊n/2⌋) = ⌈3n/2⌉ − 2 (Pohl 1972).

4. **Quickselect for the minimum.** With distinct keys, independent uniform pivots and one logical comparison per nonpivot per partition, show that quickselect, asked for the minimum, makes 2n − 2Hₙ comparisons on
   average.

   *Solution.* After n − 1 comparisons the pivot has a uniform rank r; if r = 1 we are done, otherwise we recurse
   on the r − 1 smaller items. So Cₙ = n − 1 + (1/n) Σ_{k=0}^{n−1} C_k. Multiplying by n and subtracting the same
   equation for n − 1 gives nCₙ − (n − 1)C_{n−1} = 2(n − 1) + C_{n−1}, that is Cₙ = C_{n−1} + 2 − 2/n. With C₁ = 0,
   summing gives Cₙ = 2n − 2Hₙ: about twice the n − 1 of a plain scan.

5. **Build: radix sort for the Job.** Rewrite the Job v1 with a radix sort on letters, in the Pebble language, and
   compare its instruction count with the merge sort on our passages.

   *Solution sketch.* Use most-significant-digit radix sort with 27 buckets per level (end of word, then a to z):
   count the occurrences in each bucket, compute offsets, distribute stably into a scratch array, then recurse into
   each bucket on the next letter, switching to insertion sort for buckets smaller than about 16. Each examined prefix letter, including the terminating bucket when needed, is read a constant number of times per distribution level. This replaces repeated full-key comparisons with prefix work; duplicate words still require processing through their terminators. The exact work must be counted in the implemented program; but every recursion level pays for its 27 counters, which dominates on small
   passages. Compute the distinguishing-prefix total for the corpus with a variant of `FEATURES_C`, fit the new
   program's instruction count as in `job.py`, and compare: the crossover between merge sort and radix sort is the
   answer.

6. **★ Research: integer sorting with a specified model.** Fix the allowed instructions, word width as a function of n, space budget and randomization guarantee. Identify a restriction in a cited linear-time result and propose a precise extension or a lower-bound target. A finite 32-bit radix/comparison experiment is a separate reproducible build task, not a resolution of the growing-word-width problem.

   *Where to start.* Upper bounds: Fredman and Willard's fusion trees (1990) first beat n log n; Andersson, Hagerup,
   Nilsson and Raman (1995) sort in O(n log log n), and in randomized expected linear time when the word length is at least log^{2+ε} n;
   Han and Thorup (2002) reach O(n √(log log n)) expected; Belazzougui, Brodal and Nielsen (2014) give expected
   linear time for words of Ω(log² n log log n) bits. Lower bounds: none superlinear is known for sorting on the
   word-RAM; strong bounds exist in restricted models (comparisons, and AC⁰ instruction sets) and for related
   problems such as predecessor search (Pătraşcu and Thorup 2006). Use these as historical starting points: selected author/university abstracts were checked, not every proof or every recent result. Reconcile the operation set and randomness assumptions before stating what an extension would improve. Keep a finite 32-bit measurement separate from a theorem for all word widths.

## 习题与解答

1. **插入排序的代价。** 设 n ≥ 1，键互不相同。证明插入排序至多做 I + n − 1 次比较，其中 I 是逆序对的个数；并证明对互异键的均匀随机排列 E[I] = n(n − 1)/4。

   *解答。* 在元素 i 的内层循环里，每次比较要么找到一个更大的元素，把它右移一位，要么结束循环。一次右移交换一对相邻的
   逆序元素，恰好消除一个逆序对且不产生新的，所以总共恰好 I 次右移，而每个 i 至多一次结束循环的比较：至多 I + n − 1
   次比较。对随机顺序，n(n − 1)/2 对中的每一对由对称性以 1/2 的概率逆序（交换这一对的相对次序是各种顺序之间的双射），
   由期望的线性性，E[I] = n(n − 1)/4。（`compute.py` 的 `insertion` 一项测量了这两者。）

2. **夹在两种情形之间。** 设 n = 2^h，T(1) 为正常数，用递归树求解 T(n) = 4T(n/2) + n² lg n。

   *解答。* 第 j 层有 4ʲ 个规模为 n/2ʲ 的子问题，代价为 4ʲ (n/2ʲ)² lg(n/2ʲ) = n² (lg n − j)。对 j = 0, …, lg n 求和，
   得 n² (lg n + (lg n − 1) + ⋯ + 0) = n² lg n (lg n + 1)/2 = Θ(n² log² n)。这是内部合并代价，还需加上 n² 个叶子的常数基本代价，不改变渐近结果。这里 f(n) = n^{log_b a} lg n 比 n^{log_b a}
   大，但不是大一个多项式因子，所以基本定理的情形 2 和情形 3 都不适用；推广的情形 2（f = Θ(n^{log_b a} logᵏ n) 时
   T = Θ(n^{log_b a} log^{k+1} n)）给出相同的结果。

3. **最小值与最大值。** 设 n ≥ 1，元素互异。证明同时找出 n 个元素的最小值和最大值需要 ⌈3n/2⌉ − 2 次比较，并给出恰好用这么多次的算法。

   *解答。* 算法：先两两比较（⌊n/2⌋ 次），再在胜者中找最大、在败者中找最小（多出的一个元素两组都参加），各需
   ⌈n/2⌉ − 1 次：共 ⌈3n/2⌉ − 2 次。下界：如果一个元素在某次比较中较大，就说它“赢过”，较小则“输过”。结束时，除最大值外
   每个元素都必须输过，除最小值外每个元素都必须赢过：共 2n − 2 个信息单位。两个从未比较过的元素之间的比较给出两个单位；
   对其他每次比较，对手总能回答得只给出至多一个单位（把赢过的当作大、输过的当作小，回答总能保持一致）。两个从未比较过的
   元素之间的比较至多 ⌊n/2⌋ 次，所以比较次数至少为 ⌊n/2⌋ + (2n − 2 − 2⌊n/2⌋) = ⌈3n/2⌉ − 2（波尔，1972）。

4. **用快速选择找最小值。** 假设键互异、枢轴独立均匀，每轮对每个非枢轴键计一次逻辑比较。证明快速选择在找最小值时平均做 2n − 2Hₙ 次比较。

   *解答。* n − 1 次比较之后，枢轴的秩 r 是均匀的；r = 1 时结束，否则在比它小的 r − 1 个元素上递归。所以
   Cₙ = n − 1 + (1/n) Σ_{k=0}^{n−1} C_k。乘以 n，再减去 n − 1 时的同一个方程，得 nCₙ − (n − 1)C_{n−1} = 2(n − 1) +
   C_{n−1}，即 Cₙ = C_{n−1} + 2 − 2/n。由 C₁ = 0 求和得 Cₙ = 2n − 2Hₙ：大约是直接扫描一遍的 n − 1 次的两倍。

5. **动手：给任务用基数排序。** 用 Pebble 语言把任务 v1 改写成按字母做基数排序，并在我们的文本段上与归并排序比较
   指令数。

   *解答要点。* 用最高位优先的基数排序，每层 27 个桶（词尾，然后 a 到 z）：数出每个桶里的出现次数，算出偏移量，稳定地
   分发到一个临时数组，再对每个桶按下一个字母递归，桶小于大约 16 个元素时改用插入排序。分发每层只对所处理的前缀字母读取常数次，需要时还包括词尾桶；重复单词必须一直处理到词尾。这用前缀工作替代重复的整键比较，但精确工作量仍需在实现中计数；但每一层递归都要为它的 27 个计数器付出代价，这在小文本段上占主导。用 `FEATURES_C` 的
   一个变体在语料上计算区分前缀总长度，像 `job.py` 那样拟合新程序的指令数，再作比较：归并排序与基数排序的交叉点就是
   答案。

6. **★ 研究：固定模型的整数排序。** 先固定允许指令、随 n 变化的字宽、空间预算和随机性保证。找出所引线性时间结果中的一个限制，提出精确扩展或下界目标。有限 32 位基数排序对比实验是另一个可复现构建任务，不能解决所有增长字宽下的定理问题。

   *从哪里开始。* 上界：弗雷德曼与威拉德的融合树（1990）首先突破了 n log n；安德松、哈格鲁普、尼尔松与拉曼（1995）
   在 O(n log log n) 内排序，当字长至少为 log^{2+ε} n 时可达随机化期望线性时间；韩与托鲁普（2002）达到期望 O(n √(log log n))；
   贝拉祖吉、布罗达尔与尼尔森（2014）对 Ω(log² n log log n) 位的字给出期望线性时间。下界：字 RAM 上的排序还没有已知的
   超线性下界；在受限模型（比较模型、AC⁰ 指令集）以及前驱查找等相关问题上有强下界（珀特拉什库与托鲁普，2006）。
   这些是历史起点：核对了选定作者和大学页面的摘要，没有审计全部证明或所有最新结果。先核对指令与随机性条件，再说明所提扩展能改进什么；有限 32 位测量必须与跨字宽定理分开。

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
