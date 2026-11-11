# Computer Science, Built — Part 10: Parallel Machines

The final part of Act II connects physical power limits, shared-memory protocols and parallel algorithms.
See the [series plan](../README.md) and [syllabus](../SYLLABUS.md).
The running example counts the same thirty-novel corpus, first with private shard dictionaries and then with a
partitioned merge. A fitted cost projection and a compiled host benchmark are separate experiments.

## What the chapter builds

| Chapter | Worked visualization and interpretation |
| --- | --- |
| Opening | Historical chip scatterplots; text shards feed four cores and private tables. Growth fits describe the dataset, not a law of nature. |
| 1. Power | Dynamic power, ideal constant-field scaling, a leakage sketch and a toy dark-silicon grid. The cubic frequency example ignores leakage; the 2011 dark-silicon result is a forecast under assumptions. |
| 2. Multicore | Private tables, shard-count bars and serial/tree/partitioned merge timelines. Smaller vocabularies reduce scan work, so total work changes with processor count. |
| 3. Coherence | Broken stale copies, MESI state graph and eight individually cued accesses with values and permissions. A serialized simulator tests per-address coherence; this does not impose global SC. |
| 4. False sharing | Four counters in one line versus separate 64-byte lines; measured curves fit the current data. Ownership transfers need not equal increments. |
| 5. Consistency | All six SC interleavings, store-buffer paths and a defined C11 relaxed-atomic litmus test with an x86 `mfence` variant. Relaxed atomics can have no non-atomic data race and still be non-SC. |
| 6. Atomics | Lost-update timelines built from separate relaxed accesses, correct compiled counters and the ideal wait-free consensus hierarchy. LL/SC reservations and coherent RMW ownership are different mechanisms. |
| 7. SIMD | Instruction/data streams, historical vector widths, 32-byte length comparison and candidate mask. The C implementation uses a different layout from Pebble. |
| 8. GPUs | Throughput-oriented hardware, masked lanes and a scan-length utilization proxy. Oracle grouping excludes the cost of obtaining lengths and grouping; no GPU execution is claimed. |
| 9. Work/span | A 14-node DAG, greedy and optimal schedules, the unit-cost list-scheduling proof and random checks. Average parallelism is not instantaneous width; the work-stealing theorem has computation and scheduler assumptions. |
| 10. Prefix | Carry generate/propagate pairs, Hillis–Steele, Blelloch and compaction. Associativity permits regrouping, not swapping operands. The generic down-sweep now preserves noncommutative order. |
| 11. Sorting | An 8-wire network, zero-one proof and exhaustive small tests. At 1,024 wires, bitonic uses 28,160 comparators and odd-even merge 24,063; both have depth 55. Seventeen-wire depth 10 is proved optimal in the cited 2015 work. |
| 12. Scaling | Amdahl uses the serial fraction of one-processor runtime; Gustafson uses the serial fraction of parallel runtime. Weak scaling fixes work per processor, with flat runtime an ideal outcome. |
| 13. Models | PRAM access rules, BSP phases, network graphs/cuts and selected milestones through 2024. Hop count is not latency; early peak and later HPL numbers are not one application's speedup. |
| 14. Job | Conditional projected phases and a separate host C table. Timers and omitted costs are stated explicitly. |
| 15. Frontier | A deliberately permissive causal cycle, formal-model research, work-stealing locality/space questions and energy trade-offs. Landauer concerns ideal irreversible erasure, not every transistor transition. |

The instruments are [coherence.py](../../../explainer/cs/pebble/coherence.py) and
[parallel.py](../../../explainer/cs/pebble/parallel.py); checks live in
[test_cs10_parallel.py](../../../tests/test_cs10_parallel.py). Narration and captions are bilingual.

## Computations and measurement scope

`compute.py` produces all numeric inputs. The four-core feature model gives about **11.85 s**, versus **57.32 s**
for its Part 8 one-core reference, a **4.84×** conditional compute-cost ratio. It includes fitted shard counting
and selected merge insertions. It excludes routing/hash/filter scans, communication, coherence, finite bandwidth,
barriers, scheduling overhead, final selection/output and Part 9's separate memory estimate. Smaller private
tables do not prove those costs negligible. This is not an executed multicore Pebble or a runtime error bound.
The ledger retains Part 9's **57.36 s** memory projection as its preceding row; the speedup reference above is Part 8.

`workspan.job[].projected_makespan` is a phase-model duration, not the unlimited-processor span of a fixed DAG:
changing the shard count changes the computation. The independent 14-node example has work 14, span 7, a greedy
two-processor schedule of 10 steps and an optimal schedule of 8.

Host measurements belong to the environment that generated their cache. Threads are unpinned; frequency,
scheduling, container limits and other activity affect results. The current run's C counting/merging times are
23.70 s scalar on one thread, 8.23 s with one-thread AVX2, 6.22 s scalar on four threads and 1.93 s with four-thread
AVX2. These are the faster of two runs, exclude file loading and final printing, and check the top twenty against
the reference; they do not constitute a full per-word output comparison. Future runs can differ, and narration
uses the measured ratios rather than assuming superlinear host speedup.

The C11 counter and litmus examples use defined shared accesses. A relaxed load followed by a relaxed store can
lose updates even though each access is atomic; an ordinary non-atomic racing C variable would be undefined.
The other four counter variants check exact totals. The litmus `mfence` experiment is explicitly x86-specific;
an allowed outcome's absence in a finite run is not a proof that the architecture forbids it.

The false-sharing timer reports **elapsed ns / increments per thread**. The shared-counter timer instead reports
**elapsed ns / all increments across all threads**. These are different denominators and should not be compared
as if both were single-instruction latency. Per-thread completion intervals and aggregate throughput can both be useful.

## Build

```bash
python -m videos.cs.cs10.compute                 # missing or legacy items; run host timings on an idle machine
python -m videos.cs.cs10.compute --force litmus atomics
python -m unittest tests.test_cs10_parallel
python tools/build.py cs10 -q l                 # 480p preview
python tools/build.py cs10                      # native production render
```

The C/AVX2 and `mfence` demonstrations require a suitable x86 host. Numerical files are local generated inputs
under `.cache/cs10/`. Old racy measurements and mislabeled projection records are rejected by read-only loads;
explicit computation refreshes their schema. A render or sampled QA pass is separate from complete narrated
listening and production review.

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
   Then thread 0 stores x = 1, fences, and reads y = 0, because y = 1 is still buffered. Both read 0. In this fence construction, ordering **both** workers' store–load pairs is sufficient: one fence each.
   This is a hardware-model argument; language synchronization must also be defined.

4. **Counting scan work.** For a nonempty power-of-two input, show that the Hillis–Steele scan does n log₂ n − n + 1 additions, and Blelloch's 2(n − 1).

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
   four big ones, so the counting itself does less work, the reduced scan work discussed in chapter 2. Routing, communication, bandwidth and synchronization are still
   excluded. A table per token moves the burden into merging; it does not automatically become sorting. Sorting
   and hashing are separate algorithmic redesigns developed in Parts 16 and 17.

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

4. **数扫描的工作量。** 对非空、长度为二的幂的输入，证明 Hillis–Steele 扫描做 n log₂ n − n + 1 次加法，Blelloch 的做 2(n − 1) 次。

   *解答。* 第 k 步（k = 0 … log₂ n − 1）每个下标 i ≥ 2ᵏ 的元素加上它左边 2ᵏ 处的那个：n − 2ᵏ 次加法。求和得
   n log₂ n − (1 + 2 + … + n/2) = **n log₂ n − (n − 1)**。n = 8 时：24 − 7 = 17，与计算一致。Blelloch 的上扫在第 d 层做
   n/2^(d+1) 次加法，n/2 + n/4 + … + 1 = n − 1 次；下扫每个结点再做一次，又是 n − 1：**2(n − 1)**。n = 2²⁰ 时：1990 万对 210 万。

5. **动手：更小的块。** 把任务的文本切成 64 块，每块各用一张表计数，让 4 个核空了就去取下一块。离完美均衡有多近？合并现在花多少？

   *解答。* `python -m videos.cs.cs10.compute pieces`。计数：最忙的核 **4.82 秒**，完美四等分是 4.67 秒：64 块按核空闲的先后
   取走，几乎没有不均衡（四大块时是 8%）。合并现在要合 64 张表，从 0.63 秒增加到 **1.34 秒**，但总时间降到 **6.15 秒**，四大块时
   是 11.85 秒。均衡只是收益的一部分：64 张小表比四张大表短得多，所以计数本身做的功更少，这就是第 2 章讨论的扫描工作量减少。路由、通信、带宽和同步仍未计入。每个词元一张表会把负担转移到合并，
   并不会自动变成排序；排序与哈希是第16、17部分另行发展的算法重设计。

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

*Research and later work.* Esmaeilzadeh, Blem, St. Amant, Sankaralingam & Burger, "Dark silicon and the end of multicore scaling", ISCA
(2011); Batty, Owens, Sarkar, Sewell & Weber, "Mathematizing C++ concurrency", POPL (2011); Boehm & Demsky,
"Outlawing ghosts: avoiding out-of-thin-air results" (2014); Codish, Cruz-Filipe, Frank & Schneider-Kamp, "Twenty-five
comparators is optimal when sorting nine inputs (and twenty-nine for ten)" (2014); Bundala & Závodný, "Optimal sorting
networks" (2014); Kang, Hur, Lahav, Vafeiadis & Dreyer, "A promising semantics for relaxed-memory concurrency", POPL
(2017). Data: Karl Rupp, *Microprocessor Trend Data* (CC BY 4.0), github.com/karlrupp/microprocessor-trend-data.

Additional primary references used for this revision:

- Ehlers and Müller, [New Bounds on Optimal Sorting Networks](https://arxiv.org/abs/1501.06946) (2015): seventeen-input depth optimality.
- Stern et al., [WG21 P3692R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3692r3.pdf) (2025): a proposal with an implementation-based OOTA argument under stated assumptions; its existence does not establish standard adoption.
- NVIDIA, [Hopper architecture](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) and [H100 specifications](https://www.nvidia.com/en-eu/data-center/h100/): dated H100 SXM illustration.
