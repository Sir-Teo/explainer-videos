# Computer Science, Built — Part 10: Parallel Machines

Part 10 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act II, *Making It Fast*. Around 2005 the clock stopped getting
faster, and the transistors went into more cores. This part derives why, builds the machinery that makes shared memory
work (`explainer/cs/pebble/coherence.py`: a MESI simulator checked for the single-writer invariant and the last-value
rule on random traffic, and the store-buffering litmus test under SC and TSO), the theory of parallel algorithms
(`explainer/cs/pebble/parallel.py`: work and span, greedy schedules against Brent's bound, randomized work stealing,
Hillis–Steele and Blelloch scans, bitonic and odd-even merge networks with the 0–1 test, and interconnection networks
with exact bisection widths, all checked in `tests/test_cs10_parallel.py`), measures shared memory on the computer that
made the video, and runs the Job on four cores. Every number is computed in `compute.py`.

* **The clock stops.** Fifty years of microprocessors (Karl Rupp's compilation, CC BY 4.0): transistors still
  doubling; the clock +33% a year from 1985 to 2004 and −0.7% a year since; power capped near 100 W; cores rising. The
  Job, teased: more than four times faster on four cores.
* **1. The power wall.** P = αCV²f + V·I_leak; Dennard scaling (1974) derived: shrink by κ, power per area constant;
  why it ended (the subthreshold slope, 60–100 mV a decade; voltage stuck near 1 V); P ∝ f³, so two cores at 0.8 f do
  1.6 times the work for the same power; dark silicon (a toy model, and Esmaeilzadeh et al. 2011: more than half dark
  at 8 nm).
* **2. Four cores, one Job.** Shared-memory multicores; the Job split into four shards counted in private tables
  (priced on Part 8's core model at Pebble's 885 MHz): every shard finishes faster than a quarter of 57.3 s (10.0 to
  11.2 s), because a quarter of the text holds about half the vocabulary. Combining: core 0 merges the others (8.2 s),
  a tree of merges (8.7 s), or partitioned by a hash of the word (0.63 s). Heaps' law (1978), and why the superlinear
  speedup is an artefact of a quadratic algorithm.
* **3. Cache coherence.** The stale-copy problem; single writer or many readers, and the last value (Sorin, Hill and
  Wood); MESI (Papamarcos and Patel 1984) as a state machine; one line through eight accesses by four cores, from the
  simulator; directories; coherence misses (999 invalidations for two counters in one line, 0 in two lines).
* **4. False sharing.** Four atomic counters in one 64-byte line, measured: 6.8 ns per increment alone, 79 ns with
  four threads, against 6.8 ns padded (11.6 times); fixes, `perf c2c`.
* **5. Memory consistency.** Lamport's sequential consistency (1979); the store-buffering test's six interleavings,
  none giving r0 = r1 = 0; store buffers and TSO; on this computer, both threads read 0 in a large fraction of a
  million trials, and in none with `mfence`; SC, x86-TSO and Arm/POWER/RISC-V in a table; C/C++11 and Java's models,
  data-race-free programs.
* **6. Atomic instructions.** A lost update; four threads × ten million plain increments reach 14 to 20 million of
  40 million; test-and-set, fetch-and-add, compare-and-swap, LL/SC; their costs measured with one and four threads
  (fetch-and-add 7 → 20 ns, CAS loop 13 → 37, mutex 23 → 61, test-and-set spinlock 9 → 108); Herlihy's consensus
  hierarchy (1991).
* **7. SIMD and vectors.** Flynn (1966); the Cray-1 (1976) to AVX-512, NEON, SVE and RISC-V V; the Job's length scan
  32 entries per instruction with AVX2; the Job in C on this computer, one core: 30.1 s scalar, 10.2 s vectorized.
* **8. GPUs in one chapter.** Few big cores against thousands of lanes; SIMT and warps; divergence; the Job's 4.6
  million lookups in warps of 32: 12% of lane time useful as they come, 99.99% if grouped by scan length.
* **9. Work, span and Brent's theorem.** T₁, T∞, parallelism; a 14-node example (work 14, span 7; greedy on two
  processors 10 steps, the optimum 8 by exhaustive search); Brent's theorem T_p ≤ T₁/p + T∞ proved; on 40 random
  computations of 2,000 nodes greedy never exceeds the bound and is at most 1.30 times the lower bound; work stealing
  (Blumofe and Leiserson 1999) simulated on a fork-join tree: within T₁/p + 1.6 T∞.
* **10. Parallel prefix.** Scans; Part 4's carry-lookahead adder as a scan of (g, p) pairs; Hillis–Steele (n log n
  work) and Blelloch (2(n − 1) work, span 2 log n) step by step; stream compaction.
* **11. Sorting networks.** Comparators, depth, data-obliviousness; Batcher's bitonic sorter on 8 wires (24
  comparators, depth 6); the 0–1 principle proved; insertion and Batcher networks checked on all 2ⁿ 0–1 inputs for
  n ≤ 10 (and all n! orders for n ≤ 8), against the best known sizes and depths; a broken network caught; AKS (1983).
* **12. Amdahl and Gustafson.** Both derived; strong and weak scaling; the Job's strong scaling to 32 cores: a serial
  merge peaks near 3.2×, a partitioned merge runs above the ideal line (34× at 32).
* **13. Models and networks.** PRAM (EREW, CREW, CRCW); BSP (Valiant 1990) and LogP (Culler et al. 1993); MPI
  collectives; ring, mesh, torus, hypercube and tree, their diameters and bisection widths found by trying every split
  of 16 nodes; the fat tree; supercomputers from the Cray-1 (160 Mflop/s) to El Capitan (1.74 Eflop/s).
* **14. The Job on four cores.** On four Pebble cores: 11.85 s, 4.84 times faster, with less total work than one
  core; ledger row 4. On this computer in C: 30.1 s → 6.9 s with four threads → 2.1 s with four threads and AVX2
  (14 times).
* **15. Frontier: thin air, stealing, dark silicon.** The load-buffering test: only (0, 0) under every interleaving,
  but any self-confirming guess under value speculation; out-of-thin-air values and the unsolved C/C++ memory model
  (Batty et al. 2011, promising semantics 2017); what work-stealing bounds leave out (locality, space, heterogeneous
  cores); near-threshold computing, 3-D stacking, Landauer's limit.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs10.compute           # every number in the part (about ten minutes; split and the C Job are the slow steps)
python tools/build.py cs10 -q l            # a 480p preview
python tools/build.py cs10                 # 1080p
```

The measurements (`threads`, `falseshare`, `litmus`, `atomics`, `jobc`) belong to whatever computer runs them, and
they are sensitive to other work running at the same time: run them on an idle machine. How often the litmus test's
forbidden outcome appears depends strongly on timing; that it appears at all, and never with a fence, does not. The
Pebble numbers (`split`) use Part 8's cycle model of the out-of-order core and do not depend on the machine. Ledger
rows 0 to 4 are written to `.cache/cs10/ledger.json`.

## Problems, with solutions

1. **Power density.** Under Dennard scaling by κ, how does power per area change if the voltage stays fixed while the
   clock still rises by κ? And if the clock stays fixed too?

   *Solution.* Per transistor, P = αCV²f. With C → C/κ, V fixed and f → κf, a transistor's power is unchanged:
   (C/κ)·V²·(κf) = CV²f. But κ² times as many transistors fit in the area, so **power per area rises by κ²**, about
   twice per generation. With the clock fixed too, a transistor's power falls only to CV²f/κ, so power per area still
   rises by **κ**: about 40% a generation. That is why, after 2005, even constant clocks did not make chips cool, and why
   dark silicon followed.

2. **MESI by hand.** Four caches, all Invalid. Core 0 reads, core 1 writes, core 0 reads, core 1 writes. Give every
   state after each step and count the invalidations.

   *Solution.* (states of cores 0–3)
   1. core 0 reads: no other copy, **E I I I**;
   2. core 1 writes: a read for ownership invalidates core 0, **I M I I** (1 invalidation);
   3. core 0 reads: core 1 supplies its Modified line, both Shared, **S S I I**;
   4. core 1 writes: an invalidation to core 0, **I M I I** (2 in all).

   Each write by core 1 costs a bus transaction because core 0 keeps reading: this is the ping-pong of true sharing.

3. **One fence.** Under TSO, put a fence in thread 0 of the store-buffering test only. Can both threads still read 0?

   *Solution.* **Yes.** Thread 0's fence drains x = 1 to memory before it reads y, but thread 1's store y = 1 can still
   sit in thread 1's store buffer. Run thread 1 first: y = 1 enters its buffer and its load reads x = 0 from memory.
   Then thread 0 stores x = 1, fences, and reads y = 0, because y = 1 is still buffered. Both read 0. The forbidden
   outcome needs **both** threads' store–load pairs to be ordered: one fence each.

4. **Counting scan work.** Show that the Hillis–Steele scan does n log₂ n − n + 1 additions, and Blelloch's 2(n − 1).

   *Solution.* At step k (k = 0 … log₂ n − 1) every element at index i ≥ 2ᵏ adds the one 2ᵏ to its left: n − 2ᵏ
   additions. Summing, n log₂ n − (1 + 2 + … + n/2) = **n log₂ n − (n − 1)**. For n = 8: 24 − 7 = 17, as computed.
   Blelloch's up-sweep at level d does n/2^(d+1) additions, n/2 + n/4 + … + 1 = n − 1 in all; the down-sweep does
   one per node again, another n − 1: **2(n − 1)**. For n = 2²⁰: 19.9 million against 2.1 million.

5. **Build: smaller pieces.** Cut the Job's text into 64 pieces, each counted in its own table, and let 4 cores take
   them as they come free. How close to perfect balance, and what does the merge cost now?

   *Solution.* `python -m videos.cs.cs10.compute pieces`. Counting: **4.82 s** on the busiest core against 4.67 s for
   a perfect quarter of the work: 64 pieces taken as cores come free leave almost no imbalance (four big shards left
   8%). The merge now combines 64 tables, so it grows from 0.63 s to **1.34 s**, but the total falls to **6.15 s**,
   against 11.85 s with four shards. The balance is only part of the gain: the 64 small tables are much shorter than
   four big ones, so the counting itself does less work, the same algorithmic artefact as in chapter 2. Push the grain
   to its limit, a table per word, and the "merge" becomes the whole computation: sorting the words and counting runs,
   which is Part 16's algorithm.

6. ★ **Research: the work-stealing constant.** Our runs stay within T₁/p + 1.6 T∞. What is the tight constant for
   randomized stealing on balanced fork-join trees, and what does choosing victims by locality change?

   *Where to start.* Blumofe and Leiserson (1999) prove E[T_p] ≤ T₁/p + O(T∞) with a potential-function argument; Arora,
   Blumofe and Plaxton (1998) handle a non-dedicated machine. Tchiboukdjian, Gast, Trystram, Roch and Bernard ("A
   tighter analysis of work stealing", ISAAC 2010) give explicit small constants for independent unit tasks, and later
   papers extend the analysis to trees. (a) Reproduce our simulation (`parallel.steal`) for depths
   8 to 14 and p up to 256, and fit the constant against T∞ and log p. (b) Our simulator charges one step per failed
   steal; vary that cost (the latency of an inter-core miss) and see how the constant moves. (c) Hierarchical or
   locality-aware victim selection (steal from a neighbour first) is used in practice (for example in TBB and in NUMA-
   aware runtimes): prove a bound for it, or find a family of trees where it is worse than uniform stealing.

## 习题与解答

1. **功率密度。** 按 κ 做登纳德缩放时，如果电压不变而时钟仍提高 κ 倍，单位面积功率怎样变化？如果时钟也不变呢？

   *解答。* 每个晶体管 P = αCV²f。C → C/κ、V 不变、f → κf 时，单个晶体管功率不变：(C/κ)·V²·(κf) = CV²f。但同样面积里能放下 κ²
   倍的晶体管，所以**单位面积功率升高 κ² 倍**，每代约两倍。时钟也不变时，单个晶体管功率只降到 CV²f/κ，单位面积功率仍升高 **κ**
   倍：每代约 40%。这就是 2005 年以后连时钟不变芯片也凉不下来、暗硅随之而来的原因。

2. **手算 MESI。** 四个缓存，全为 Invalid。核 0 读，核 1 写，核 0 读，核 1 写。给出每一步后的所有状态，并数出作废的次数。

   *解答。*（核 0–3 的状态）
   1. 核 0 读：没有别的副本，**E I I I**；
   2. 核 1 写：为获得所有权而读，作废核 0，**I M I I**（1 次作废）；
   3. 核 0 读：核 1 提供它的 Modified 行，两者都 Shared，**S S I I**；
   4. 核 1 写：作废核 0，**I M I I**（共 2 次）。

   因为核 0 一直在读，核 1 的每次写都要一次总线事务：这就是真共享的乒乓。

3. **一道栅栏。** 在 TSO 下，只在存储缓冲测试的线程 0 里放一道栅栏。两个线程还能都读到 0 吗？

   *解答。* **能。** 线程 0 的栅栏让 x = 1 在它读 y 之前写进存储器，但线程 1 的存数 y = 1 仍可能待在线程 1 的存储缓冲里。让线程 1
   先走：y = 1 进入它的缓冲，它的取数从存储器读到 x = 0。然后线程 0 存 x = 1、过栅栏、读 y = 0，因为 y = 1 还在缓冲里。两个都读
   到 0。要禁止这个结果，**两个**线程的存数—取数对都必须有序：每个线程一道栅栏。

4. **数扫描的工作量。** 证明 Hillis–Steele 扫描做 n log₂ n − n + 1 次加法，Blelloch 的做 2(n − 1) 次。

   *解答。* 第 k 步（k = 0 … log₂ n − 1）每个下标 i ≥ 2ᵏ 的元素加上它左边 2ᵏ 处的那个：n − 2ᵏ 次加法。求和得
   n log₂ n − (1 + 2 + … + n/2) = **n log₂ n − (n − 1)**。n = 8 时：24 − 7 = 17，与计算一致。Blelloch 的上扫在第 d 层做
   n/2^(d+1) 次加法，n/2 + n/4 + … + 1 = n − 1 次；下扫每个结点再做一次，又是 n − 1：**2(n − 1)**。n = 2²⁰ 时：1990 万对 210 万。

5. **动手：更小的块。** 把任务的文本切成 64 块，每块各用一张表计数，让 4 个核空了就去取下一块。离完美均衡有多近？合并现在花多少？

   *解答。* `python -m videos.cs.cs10.compute pieces`。计数：最忙的核 **4.82 秒**，完美四等分是 4.67 秒：64 块按核空闲的先后
   取走，几乎没有不均衡（四大块时是 8%）。合并现在要合 64 张表，从 0.63 秒增加到 **1.34 秒**，但总时间降到 **6.15 秒**，四大块时
   是 11.85 秒。均衡只是收益的一部分：64 张小表比四张大表短得多，所以计数本身做的功更少，这和第 2 章是同一个算法上的假象。把粒度
   推到极限，每个词一张表，“合并”就成了全部计算：把词排序再数连续段，正是第 16 部分的算法。

6. ★ **研究：工作窃取的常数。** 我们的模拟都落在 T₁/p + 1.6 T∞ 以内。在平衡的分叉—汇合树上，随机窃取的紧常数是多少？按局部性
   选择受害者会改变什么？

   *从哪里开始。* Blumofe 与 Leiserson（1999）用势函数论证证明了 E[T_p] ≤ T₁/p + O(T∞)；Arora、Blumofe 与 Plaxton（1998）处理了
   非专用的机器。Tchiboukdjian、Gast、Trystram、Roch 与 Bernard（“A tighter analysis of work stealing”，ISAAC 2010）对独立任务
   给出了明确的小常数，后来的论文把分析推广到树。（a）对深度 8 到 14、p 到 256 重做我们的模拟
   （`parallel.steal`），把常数对 T∞ 和 log p 拟合。（b）我们的模拟器每次失败的窃取算一步；改变这个代价（一次核间缺失的延迟），看
   常数怎样移动。（c）分层或照顾局部性的受害者选择（先偷邻居的）在实践中被使用（例如 TBB 和照顾 NUMA 的运行时）：为它证明一个
   界，或者找到一族树，使它比均匀窃取更差。

## Glossary additions

功率墙 power wall · 登纳德缩放 Dennard scaling · 阈值电压 threshold voltage · 漏电 leakage · 暗硅 dark silicon · 多核 multicore ·
共享内存 shared memory · 缓存一致性 cache coherence · 单写多读 single writer, multiple readers · 监听 snooping · 目录 directory ·
MESI（已修改、独占、共享、无效） MESI (Modified, Exclusive, Shared, Invalid) · 作废 invalidation · 一致性缺失 coherence miss ·
伪共享 false sharing · 存储一致性模型 memory consistency model · 顺序一致性 sequential consistency · 存储缓冲 store buffer ·
全存储定序 total store order (TSO) · 弱内存模型 weak memory model · 栅栏 fence · 获取 / 释放 acquire / release · 数据竞争
data race · 原子指令 atomic instruction · 测试并置位 test-and-set · 取并加 fetch-and-add · 比较并交换 compare-and-swap ·
链接取数 / 条件存数 load-linked / store-conditional · 共识数 consensus number · 无等待 wait-free · 单指令多数据 SIMD ·
向量寄存器 vector register · 单指令多线程 SIMT · 线程束 warp · 分歧 divergence · 工作量 work · 跨度 span · 并行度 parallelism ·
贪心调度 greedy schedule · 布伦特定理 Brent's theorem · 工作窃取 work stealing · 双端队列 deque · 前缀和 / 扫描 prefix sum /
scan · 流压缩 stream compaction · 排序网络 sorting network · 比较器 comparator · 双调排序 bitonic sort · 0–1 原理 0–1 principle ·
阿姆达尔定律 Amdahl's law · 古斯塔夫森定律 Gustafson's law · 强扩展 / 弱扩展 strong / weak scaling · 并行随机存取机 PRAM ·
整体同步并行 BSP · 超步 superstep · 归约 / 全归约 reduce / all-reduce · 直径 diameter · 对分宽度 bisection width · 胖树 fat tree ·
超立方体 hypercube · 环面 torus · 凭空出现的值 out-of-thin-air value · 近阈值计算 near-threshold computing · 兰道尔极限 Landauer's
limit

## Sources

The reading list is split, as the research tier asks (videos/cs/SYLLABUS.md §1.1), into the qualifying-exam canon and
recent work.

*Canon.* Books: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 4 and 5; Sorin,
Hill & Wood, *A Primer on Memory Consistency and Cache Coherence*, 2nd ed. (2020); Herlihy, Shavit, Luchangco & Spear,
*The Art of Multiprocessor Programming*, 2nd ed. (2020); Leighton, *Introduction to Parallel Algorithms and
Architectures* (1992); Knuth, *The Art of Computer Programming*, vol. 3, §5.3.4 (networks for sorting; the 0–1
principle).

Papers: Flynn, "Very high-speed computing systems" (1966); Graham, "Bounds for certain multiprocessing anomalies"
(1966); Amdahl, "Validity of the single processor approach to achieving large scale computing capabilities" (1967);
Batcher, "Sorting networks and their applications" (1968); Dennard, Gaensslen, Yu, Rideout, Bassous & LeBlanc, "Design
of ion-implanted MOSFETs with very small physical dimensions" (1974); Brent, "The parallel evaluation of general
arithmetic expressions" (1974); Fortune & Wyllie, "Parallelism in random access machines" (1978); Lamport, "How to make
a multiprocessor computer that correctly executes multiprocess programs" (1979); Ladner & Fischer, "Parallel prefix
computation" (1980); Ajtai, Komlós & Szemerédi, "An O(n log n) sorting network" (1983); Papamarcos & Patel, "A
low-overhead coherence solution for multiprocessors with private cache memories" (1984); Leiserson, "Fat-trees" (1985);
Hillis & Steele, "Data parallel algorithms" (1986); Gustafson, "Reevaluating Amdahl's law" (1988); Blelloch, "Prefix
sums and their applications" (1990); Valiant, "A bridging model for parallel computation" (1990); Herlihy, "Wait-free
synchronization" (1991); Culler et al., "LogP: towards a realistic model of parallel computation" (1993); Blumofe &
Leiserson, "Scheduling multithreaded computations by work stealing" (1999); Acar, Blelloch & Blumofe, "The data
locality of work stealing" (2000); Heaps, *Information Retrieval: Computational and Theoretical Aspects* (1978).

*Recent.* Esmaeilzadeh, Blem, St. Amant, Sankaralingam & Burger, "Dark silicon and the end of multicore scaling", ISCA
(2011); Batty, Owens, Sarkar, Sewell & Weber, "Mathematizing C++ concurrency", POPL (2011); Boehm & Demsky,
"Outlawing ghosts: avoiding out-of-thin-air results" (2014); Codish, Cruz-Filipe, Frank & Schneider-Kamp, "Twenty-five
comparators is optimal when sorting nine inputs (and twenty-nine for ten)" (2014); Bundala & Závodný, "Optimal sorting
networks" (2014); Kang, Hur, Lahav, Vafeiadis & Dreyer, "A promising semantics for relaxed-memory concurrency", POPL
(2017). Data: Karl Rupp, *Microprocessor Trend Data* (CC BY 4.0), github.com/karlrupp/microprocessor-trend-data.
