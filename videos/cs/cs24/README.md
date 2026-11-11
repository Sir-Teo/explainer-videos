# Part 24 — Algorithms in Practice / 第24部分：实践中的算法

This episode implements range structures, monotone frontiers, search, bit packing
and decomposition, then measures specific native implementations. Complexity
statements have explicit input and machine-model assumptions. Timings are finite
observations on a shared host; they do not identify individual hardware causes.

本部分实现区间结构、单调边界、搜索、比特打包与分解，再测量具体原生实现。
复杂度结论需要明确的输入和机器模型前提。耗时属于共享主机上的有限观测，
不能单凭它分离硬件机制的因果贡献。

Run from the repository root:

```bash
python -m unittest tests.test_cs24_practice
python -m videos.cs.cs24.compute --force
python -m videos.cs.cs24.worked_examples
```

The 19 producers write schema-2 payloads plus a derived ledger. Cache validity
binds the complete compute, instrument and reference sources, including imported
native Job and corpus sources. Deterministic native seeds, exact original and
timed sources, compiler version/flags, binary hashes, disassembly, every clock
read, decoded intervals and complete-output check records accompany the data.
Inputs are prepared before timers; validation runs afterwards. Timestamp buffering
adds an integer store after each clock read. Actual output buffers are part of
this revised harness. Native summaries use minima of fixed repetitions, while the
benchmark demonstration compares first observations with later-five medians.
Algorithm order inside native trials is fixed, so these are not randomized causal
estimates. Recomputing produces a new measurement snapshot.

19 个计算项写入第二版数据和派生账本。缓存绑定完整源文件；数据附带确定性种子、
编译选项、二进制与反汇编哈希、原始时钟、区间解释及完整输出检查。
输入准备与验证在计时之外；时钟缓冲和输出缓冲属于这个修订测量程序。
原生摘要取固定重复的最小值；基准示例比较首次观测和后五次中位数。
原生试验内算法顺序固定，因此不属于随机化因果估计。

## Contracts and measurement scope / 约定与测量范围

- Ranges are inclusive in the practice instrument. Empty structures construct
  safely; invalid indices/ranges fail before mutation. Fenwick updates require
  indices `1..n`; prefix queries accept `0..n`. Bit-subset routines require
  nonnegative integers. Histogram heights must be finite and nonnegative.
- Cartesian minima use `(value,index)` order, selecting the leftmost equal
  minimum. Sliding maxima discard older equal values. The histogram's equal-bar
  pop rule differs from next-strictly-greater queries.
- Binary answer search requires a monotone predicate and checks a feasible upper
  endpoint. Galloping searches a sorted suffix; a global lower bound also
  requires all earlier elements below the target. Both search table columns
  count actual key reads, including bound construction.
- Native range benchmarks share `n=2^20`, but naive arrays execute only the first
  `2^10` operations; trees execute `2^20`. Their per-operation figures therefore
  do not represent equal-length steady-state workloads. Every answer is checked
  against a separate square-root reference.
- Every sort batch is checked, every map key count and lookup is checked, closure
  is checked by independent BFS, and native top-20 lists are checked by independent
  sorted insertion. Job checks all distinct counts, not just the displayed twenty.
  The fixed engineered Job has corpus-checked table/pool/word-length limits.
- Native Swiss-style code is a teaching implementation. Its requested occupancy
  is separate from `unordered_map`'s actual bucket occupancy. ISA-dependent
  AVX2/AVX-512/SSE2 results apply to the retained host/build, not every CPU.
- All 20,000 Mo answers are checked with an offline last-occurrence sum-tree
  reference. MITM's displayed counter counts generated sums and search calls;
  sorting, comparisons, bit costs and exponential storage remain additional costs.
- The learned index is an anchored greedy floating-point fit, not optimal PGM
  segmentation. Stored-key errors are evaluated; each query's bracket is certified
  with full-search fallback. NumPy independently checks every actual query.
  Active model bytes include native struct padding and separator keys. Peak
  requested storage is recorded separately, excluding key/query arrays and allocator
  overhead; it is not measured RSS. Lookup timers exclude fitting and validation.
- Ski rental uses discrete buy-at-start-of-day costs and exact rational ceilings.
  The exact worst ratio is witnessed at one of the two buy days, not estimated by
  a short season grid. Gaussian forecast means are synthetic observations.
- Amdahl's panel assumes a phase fraction. It is not a profile assembled by
  subtracting an isolated tokenizer from another program. The modeled Pebble
  ledger and native wall times are distinct quantities; their ratio is not a
  measured cross-processor speedup. Same-host native Job comparisons are separate.

区间为闭区间，空结构可构造，非法范围在修改前拒绝。Fenwick 更新从一开始，
空前缀允许零。相等值规则明确；预算和双指针要求非负值。二分答案先检查可行上界，
跳跃搜索明确后缀前提，比较表统计实际读取。四种区间基准的轨迹长度不同。
完整检查覆盖全部排序批次、映射答案、闭包、前二十、词频和 Mo 查询。
学习索引认证区间并回退，模型内存包含结构体填充与分隔键；租赁使用精确离散界。
Amdahl 占比是假设；Pebble 模型账本与原生墙钟时间分开解释。

## Six worked exercises / 六道习题解答

1. **Fenwick partition and bound.** For positive `i`, repeatedly removing its
   lowest set bit decomposes `[1,i]` into disjoint adjacent responsibility
   intervals. The query count is exactly `popcount(i)`, at most
   `floor(log2(n))+1`. Updating adds the lowest set bit, advancing its position
   until the index exceeds `n`, with the same logarithmic bound.
   **中文：** 每次去掉最低置位比特，负责区间首尾相接，恰好划分前缀。
   查询步数等于置位比特数；更新把最低置位比特向左推进，直到超过数组。

2. **Deque amortization and ties.** Charge every push and removal to its index;
   an index enters once and leaves at most once, so total pushes plus pops are
   at most `2n`. Removing equal tail values keeps the newer representative.
   The executed `[2,2,1,3]`, width-two witness returns `[2,2,3]`.
   **中文：** 每个索引最多入队、离队各一次，合计不超过二 n。
   相等时保留较新的代表；执行见证的三个最大值为二、二、三。

3. **Cartesian tree and RMQ.** Recursively choose the leftmost minimum as root.
   In-order positions are array positions, so the LCA of two positions is their
   interval minimum. The monotone-stack construction pushes/pops each position
   at most once. For `[2,1,1,3]`, the executed parent array is `[1,-1,1,2]`.
   This implementation's sparse-table preprocessing is `O(n log n)`; cited
   linear-preprocessing results use additional constructions.
   **中文：** 递归选最左最小值，保持中序位置，因此区间最小值就是两端的祖先。
   单调栈线性构造；当前稀疏表不是所引用的线性预处理结构。

4. **All masks and submasks.** Each bit is absent, present only in the mask, or
   present in both: three independent choices give exactly `3^n` body visits,
   including zero submasks. The executed witness checks `n=0..8`.
   This counts visits; arbitrary-width arithmetic adds bit cost.
   **中文：** 每位有不在掩码、只在掩码、同时在掩码与子掩码三种状态，
   所以恰好三的 n 次方次访问；大整数的位代价另计。

5. **Bounded Pebble design.** First choose a fixed vocabulary and stable IDs.
   Store counts in a one-based Fenwick array; the top-`k` frequency prefix then
   answers the question only if IDs have been fixed in that frequency order.
   Vocabulary construction and re-ranking are separate problems. For a bounded
   eight-ID example, counts `[3,1,4,1,5,9,2,6]` give `prefix(5)=14`; adding five
   at ID two touches `[2,4,8]` and changes it to `19`. The executed Python trace
   checks every final prefix. This unsorted-ID trace illustrates prefix arithmetic,
   not a top-k query. One concrete Pebble design can limit the vocabulary to eight
   ASCII words of at most sixteen bytes and use signed 32-bit counters. Reject an
   update if a word count would become negative or the total exceed `2^31-1`.
   A Pebble port must also bound pool storage,
   reserve `n+1` counters, reject update index zero, and prove counters/totals fit
   the chosen signed width before incrementing. No new Pebble-language program
   or emulator execution is claimed by these notes.
   **中文：** 先固定词表与稳定编号；只有编号已按频率固定排序，前 k 项和才回答
   热门词计数。建词表与重排另算。八项见证中前五项为十四，编号二增加五，
   访问二、四、八，答案变十九。这个未排序编号轨迹只演示前缀算术，不是前 k 查询。
   一个具体设计可限定八个、每个至多十六字节的 ASCII 词，使用三十二位有符号计数；
   若更新使计数为负或总和超过 `2^31-1`，就拒绝。Python 轨迹核对全部前缀；移植还要证明
   词长、字节池和有符号计数范围，并拒绝零更新位置。这里没有宣称执行新移植。

6. **Reproduce a research baseline.** The cited mean-exit-time analysis assumes
   positive IID gaps, finite nonzero variance and an appropriate asymptotic regime.
   `worked_examples.py` executes 1,000 independent fixed-slope first-exit walks
   per epsilon on exponential gaps with population mean/variance one. For epsilon
   `4,8,16,32`, the seeded sample means are approximately `21.96,74.12,281.96,1115.14`;
   their ratios to epsilon squared are `1.373,1.158,1.101,1.089`. Raw lengths,
   pre-exit/exit errors, generator details and sample standard errors are retained.
   These finite observations illustrate overshoot/regime effects, not a theorem
   proof. Next reproduce several seeds and distributions, then compare real gaps,
   shuffled gaps and correlations with matching procedures. The corpus's anchored
   fit is a different algorithm; a slope through a few epsilon values is not a
   universal exponent or a contradiction of the IID result. Dynamic PGM already
   supports updates: reproduce that baseline before proposing a narrower question.
   **中文：** 先复现正的独立同分布间隔上的固定斜率退出实验，再比较真实与打乱
   间隔。保存长度、退出前后误差、种子和标准误。有限斜率不是渐近定律，
   锚定贪心与论文构造不同；动态 PGM 已存在，新的问题需要更窄的范围。

## Primary references / 原始文献

Consulted 2026-11-11; these are cited results, not claims that every paper's system
was implemented here.

- [Khuong–Morin, array search layouts](https://arxiv.org/abs/1509.05053).
- [Mytkowicz et al., measurement bias (2009)](https://sape.inf.usi.ch/publications/asplos09.html).
- [Curtsinger–Berger, Stabilizer (2013)](https://github.com/ccurtsinger/stabilizer).
- [Purohit–Svitkina–Kumar, predictions (2018), Algorithm 2](https://proceedings.neurips.cc/paper/2018/file/73a427badebe0e32caa2e1fc7530b7f3-Paper.pdf).
- [Ferragina–Vinciguerra, PGM (2020), including dynamic indexing](https://www.vldb.org/pvldb/vol13/p1162-ferragina.pdf).
- [Ferragina–Lillo–Vinciguerra, learned-index effectiveness (2020)](https://proceedings.mlr.press/v119/ferragina20a.html).

The evidence packet binds the exact source and measurement snapshot. Sampled
previews and automated speech checks are separate from continuous audiovisual
listening, Chinese synthesized speech review, full native production review and
production-pace runtime approval; those release gates remain open.
